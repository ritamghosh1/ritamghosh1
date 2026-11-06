#!/usr/bin/env python3
"""Verify the published static site matches the local release, including its PDF."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlsplit
import hashlib
ROOT=Path(__file__).resolve().parents[1]/'docs'
BASE='https://ritamghosh1.github.io/ritamghosh1/'
class Assets(HTMLParser):
    def __init__(self): super().__init__(); self.refs=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for key in ('src','href'):
            if key in a: self.refs.append(a[key])
        self.refs += [v.strip().split()[0] for v in a.get('srcset','').split(',') if v.strip()]
        if tag=='meta' and a.get('property')=='og:image': self.refs.append(a['content'])
urls={BASE:'index.html', BASE+'sitemap.xml':'sitemap.xml'}
for path in ROOT.rglob('*.html'):
    relative=path.relative_to(ROOT).as_posix()
    parser=Assets();parser.feed(path.read_text())
    page=BASE+relative
    urls[page]=relative
    for ref in parser.refs:
        target=urljoin(page,ref).split('#')[0]
        if target.startswith(BASE):
            suffix=target[len(BASE):]
            suffix=suffix or 'index.html'
            if (ROOT/suffix).is_file(): urls[target]=suffix
for url,relative in sorted(urls.items()):
    request=Request(url,headers={'User-Agent':'Portfolio-release-verification'})
    with urlopen(request,timeout=30) as response:
        assert response.status==200,(url,response.status)
        assert response.url.startswith('https://'),f'HTTPS redirect lost: {url}'
        content=response.read()
        expected=(ROOT/relative).read_bytes()
        assert hashlib.sha256(content).digest()==hashlib.sha256(expected).digest(),f'Stale or mismatched deployed content: {url}'
        if relative.endswith('.pdf'): assert response.headers.get_content_type()=='application/pdf'
    print('OK',relative)
print(f'Passed {len(urls)} published HTTPS paths with exact release content, including share assets and resume.')
