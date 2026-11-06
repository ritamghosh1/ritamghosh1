#!/usr/bin/env python3
"""Check static output, local anchors, metadata, and release constraints."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs'
BASE = 'https://ritamghosh1.github.io/ritamghosh1/'
class Page(HTMLParser):
    voids = set('area base br col embed hr img input link meta param source track wbr'.split())
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path=path; self.stack=[]; self.ids=set(); self.refs=[]; self.metas={}; self.canon=[]; self.headings=[]; self.mains=0; self.titles=0; self.json=False; self.structured=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'{self.path}: duplicate ID {a["id"]}'
            self.ids.add(a['id'])
        if tag=='title': self.titles+=1
        if tag=='main': self.mains+=1
        if re.fullmatch('h[1-6]',tag): self.headings.append(int(tag[1]))
        if tag=='img':
            assert 'alt' in a, f'{self.path}: missing image alt'
            assert 'width' in a and 'height' in a, f'{self.path}: image space not reserved'
        if tag=='meta':
            key=a.get('name') or a.get('property')
            if key:
                assert key not in self.metas, f'{self.path}: duplicate {key}'
                self.metas[key]=a.get('content','')
        if tag=='link' and a.get('rel')=='canonical': self.canon.append(a['href'])
        if tag in ('a','link','script','img','source'):
            self.refs += [a[k] for k in ('src','href') if k in a]
            self.refs += [v.strip().split()[0] for v in a.get('srcset','').split(',') if v.strip()]
        if tag=='script' and a.get('type')=='application/ld+json': self.json=True
        if tag not in self.voids: self.stack.append(tag)
    def handle_endtag(self,tag):
        if tag in self.voids: return
        assert self.stack and self.stack[-1]==tag, f'{self.path}: invalid nesting at {tag}: {self.stack[-3:]}'
        self.stack.pop()
        if tag=='script': self.json=False
    def handle_data(self,data):
        if self.json: self.structured.append(json.loads(data))
pages={}
for path in DOCS.rglob('*.html'):
    p=Page(path); text=path.read_text(); p.feed(text)
    assert not p.stack, f'{path}: unclosed markup'
    assert p.titles==1 and p.mains==1 and p.headings.count(1)==1,path
    for previous,current in zip(p.headings,p.headings[1:]):
        assert current <= previous+1, f'{path}: heading levels skipped {previous}→{current}'
    expected=BASE+('' if path==DOCS/'index.html' else path.relative_to(DOCS).as_posix())
    assert p.canon==[expected], f'{path}: canonical mismatch'
    for key in ('description','og:title','og:description','og:image','og:image:alt','twitter:card','twitter:image','twitter:image:alt'):
        assert p.metas.get(key),f'{path}: missing {key}'
    assert p.metas['og:url']==expected,path
    assert p.metas['og:image'].startswith('https://'),path
    assert p.structured[0]['name']=='Ritam Ghosh',path
    assert 'sentiment' not in text.lower() and 'playground' not in text.lower(),path
    pages[path.resolve()]=p
for path,page in pages.items():
    for ref in page.refs:
        url=urlsplit(ref)
        if url.scheme or url.netloc: continue
        target=(path.parent/unquote(url.path)).resolve() if url.path else path
        if target.is_dir(): target=target/'index.html'
        assert target.is_file(), f'{path}: missing asset {ref}'
        assert target.is_relative_to(DOCS.resolve()),f'{path}: reference outside docs {ref}'
        if url.fragment:
            assert target in pages and unquote(url.fragment) in pages[target].ids,f'{path}: missing anchor {ref}'
ET.parse(DOCS/'sitemap.xml')
for path in (DOCS/'assets/images').iterdir():
    assert path.stat().st_size < 250_000,f'{path}: exceeds 250 KB image budget'
# Contrast for both primary themes, including muted copy and accent controls.
def luminance(h):
    v=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    linear=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in v]
    return sum(c*w for c,w in zip(linear,(.2126,.7152,.0722)))
def contrast(a,b):
    a,b=sorted((luminance(a),luminance(b)))
    return (b+.05)/(a+.05)
pairs=[('#52636b','#f8f9f5'),('#52636b','#ffffff'),('#52636b','#eef0eb'),('#3158cf','#ffffff'),('#b3c1c6','#11232e'),('#b3c1c6','#192f3b'),('#b3c1c6','#172b35'),('#a7bbff','#11232e'),('#bac8d0','#142b38')]
for fg,bg in pairs: assert contrast(fg,bg)>=4.5,(fg,bg,contrast(fg,bg))
print(f'Passed {len(pages)} pages: markup, headings, anchors, assets, metadata, sitemap, image budgets, exclusions, and {len(pairs)} contrast pairs.')

# Optional real HTTP checks under the intended repository subpath, with no external service.
if '--http' in __import__('sys').argv:
    from functools import partial
    from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
    from tempfile import TemporaryDirectory
    from threading import Thread
    from urllib.request import urlopen
    from urllib.parse import urljoin
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *args): pass
    with TemporaryDirectory(prefix='portfolio-http-') as temp:
        (Path(temp)/'ritamghosh1').symlink_to(DOCS, target_is_directory=True)
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=temp))
        thread=Thread(target=server.serve_forever,daemon=True);thread.start()
        base=f'http://127.0.0.1:{server.server_port}/ritamghosh1/'
        checked=set()
        try:
            for path,page in pages.items():
                page_url=base+path.relative_to(DOCS.resolve()).as_posix()
                urls=[page_url]
                for ref in page.refs:
                    parsed=urlsplit(ref)
                    if not parsed.scheme and not parsed.netloc:
                        urls.append(urljoin(page_url,ref).split('#')[0])
                for url in urls:
                    if url in checked: continue
                    with urlopen(url,timeout=10) as response:
                        assert response.status==200,url
                        body=response.read()
                        if url.endswith('.pdf'):
                            assert response.headers.get_content_type()=='application/pdf',url
                            assert body==(DOCS/'assets/resume/ritam-ghosh-resume.pdf').read_bytes(),url
                    checked.add(url)
            print(f'Passed {len(checked)} local HTTP paths under /ritamghosh1/, including exact PDF bytes and content type.')
        finally:
            server.shutdown();server.server_close();thread.join()
