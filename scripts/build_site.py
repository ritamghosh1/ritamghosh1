#!/usr/bin/env python3
"""Generate build-free portfolio HTML from the approved project content."""
import json
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = 'https://ritamghosh1.github.io/ritamghosh1/'
PROJECTS = json.loads((ROOT / 'content/projects.json').read_text())
RESUME = 'assets/resume/ritam-ghosh-resume.pdf'


def arrow(direction='↗'):
    return f'<span aria-hidden="true">{direction}</span>'


def tags(project):
    return '<ul class="tags" aria-label="Technologies">' + ''.join(f'<li>{e(t)}</li>' for t in project['stack']) + '</ul>'


def artwork(p):
    if p['slug'] == 'ask-the-book':
        inside = '''<div class="book-window"><div class="window-bar"><span>Ask the Book</span><span aria-hidden="true">•••</span></div>
        <p class="mini-label">DOCUMENT / ALGORITHMS.PDF</p><p class="book-question">What happens when<br>a hash table overflows?</p>
        <div class="answer-lines" aria-hidden="true"><i></i><i></i><i></i></div>
        <div class="citations"><span>Page 32</span><span>Page 33</span><span>↗ Sources</span></div></div>
        <div class="art-note">Retrieve <span>→</span> Rerank <span>→</span> Cite</div>'''
    elif p['slug'] == 'algocoach':
        inside = '''<div class="coach-window"><div class="window-bar"><span>AlgoCoach</span><span aria-hidden="true">↗</span></div>
        <p class="mini-label">YOUR NEXT CHALLENGE</p><p class="coach-question">Small steps.<br>Stronger solutions.</p>
        <div class="coach-bars" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>
        <div class="coach-axis"><span>Confidence</span><span>Target</span><span>Stretch</span></div></div>'''
    else:
        inside = '''<div class="arrakis-window"><div class="window-bar"><span>arrakis</span><span aria-hidden="true">✳</span></div>
        <p class="mini-label">IDEAS DESERVE AN AUDIENCE</p><p class="arrakis-question">Discover.<br>Try. Give feedback.</p>
        <div class="trial-tile"><span aria-hidden="true">↗</span><p>Small projects.<br>Real possibilities.</p></div></div>'''
    return f'<div class="project-art art-{p["slug"]}" role="img" aria-label="{e(p["name"])}: illustrative concept, not an application screenshot">{inside}<span class="illustration-label">Illustrative concept</span></div>'


def head(title, description, path='', prefix=''):
    url = BASE + path
    person = {'@context': 'https://schema.org', '@type': 'Person', 'name': 'Ritam Ghosh', 'url': BASE,
              'image': BASE + 'assets/images/ritam-ghosh.jpg', 'email': 'mailto:ritamghosh548@gmail.com',
              'sameAs': ['https://github.com/ritamghosh1', 'https://www.linkedin.com/in/ritamghosh548/', 'https://codeforces.com/profile/TheOrion']}
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}">
<meta name="theme-color" content="#f8f9f5"><meta name="color-scheme" content="light dark">
<link rel="canonical" href="{url}"><link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefix}assets/images/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="Ritam Ghosh">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/images/social-preview.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Ritam Ghosh — developer and problem solver, with a portrait">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{BASE}assets/images/social-preview.jpg">
<meta name="twitter:image:alt" content="Ritam Ghosh — developer and problem solver, with a portrait">
<script src="{prefix}theme.js"></script><link rel="stylesheet" href="{prefix}style.css"><script src="{prefix}script.js" defer></script>
<script type="application/ld+json">{json.dumps(person)}</script>
</head><body><a class="skip" href="#main">Skip to content</a>'''


def header(prefix='', home=False):
    h = '' if home else prefix + 'index.html'
    return f'''<header class="site-header"><div class="wrap header-inner">
<a href="{h or '#top'}" class="wordmark" aria-label="Ritam Ghosh home">rg<span>.</span></a>
<nav aria-label="Main navigation"><a href="{h}#work">Work</a><a href="{h}#about">About</a><a href="{prefix}{RESUME}">Resume</a><a href="{h}#contact">Let’s talk {arrow()}</a></nav>
<div class="theme-control" hidden><label for="theme">Theme</label><select id="theme"><option value="system">System</option><option value="light">Light</option><option value="dark">Dark</option></select></div>
</div></header>'''


def footer(prefix=''):
    return f'''<section id="contact" class="contact" aria-labelledby="contact-title"><div class="wrap">
<div class="contact-heading" data-reveal><div><p class="eyebrow">04 / A good idea starts with a conversation</p>
<h2 id="contact-title">Let’s build<br>something <em>useful.</em></h2></div><a class="contact-arrow" href="mailto:ritamghosh548@gmail.com" aria-label="Email Ritam Ghosh">{arrow()}</a></div>
<div class="contact-row"><a class="email" href="mailto:ritamghosh548@gmail.com">ritamghosh548@gmail.com</a><button id="copy-email" class="copy-button" type="button" hidden>Copy email {arrow('⧉')}</button></div>
<p id="copy-status" class="copy-status" role="status"></p>
<div class="contact-links"><a href="https://github.com/ritamghosh1">GitHub {arrow()}</a><a href="https://www.linkedin.com/in/ritamghosh548/">LinkedIn {arrow()}</a><a href="{prefix}{RESUME}" download="Ritam_Ghosh_Resume.pdf">Download resume (PDF) {arrow('↓')}</a></div>
<footer><span>© <span id="year">2026</span> Ritam Ghosh</span><span>Thoughtfully built. Always evolving.</span><a href="#top">Back to top {arrow('↑')}</a></footer>
</div></section></body></html>'''


def project_card(p):
    demo = f'<a class="text-link" href="{p["demo"]}">{e(p["demo_label"])} {arrow()}</a>' if p['demo'] else '<span class="project-status">Team concept</span>'
    return f'''<article class="project" data-category="{p['category']}" data-name="{e(p['name'])}" aria-labelledby="title-{p['slug']}">
{artwork(p)}<div class="project-copy"><p class="eyebrow">{p['number']} / {e(p['kind'])}</p><h3 id="title-{p['slug']}">{e(p['name'])}</h3>
<p class="project-headline">{e(p['headline'])}</p><p class="project-summary">{e(p['summary'])}</p>{tags(p)}
<p class="project-role">{e(p['role'])}</p><div class="project-actions"><a class="button primary" href="work/{p['slug']}.html">Read case study {arrow('→')}</a>{demo}</div>
<a class="source-link" href="{p['repo']}">View source on GitHub {arrow()}</a></div></article>'''


def home():
    s = head('Ritam Ghosh — Developer & problem solver', 'Computer Science at Jadavpur University. Full-stack applications, retrieval systems, and purposeful problem solving.') + header(home=True)
    s += '''<main id="main"><section id="top" class="hero wrap" aria-labelledby="hero-title">
<div class="hero-intro"><p class="eyebrow hero-kicker"><span class="dot" aria-hidden="true"></span> Developer. Problem solver. Always curious.</p>
<h1 id="hero-title">Ritam<br>Ghosh<span>.</span></h1><p class="hero-description">From difficult problems<br>to things people can use.</p>
<p class="hero-detail">Computer Science &amp; Engineering at Jadavpur University.<br>Building across the web, AI, and the space between.</p>
<div class="hero-actions"><a class="button primary" href="#work">Explore my work <span aria-hidden="true">↘</span></a>
<a class="button secondary" href="assets/resume/ritam-ghosh-resume.pdf">View resume <span aria-hidden="true">↗</span></a></div></div>
<figure class="hero-portrait"><div class="portrait-frame"><picture><source type="image/webp" srcset="assets/images/ritam-ghosh-480.webp 480w, assets/images/ritam-ghosh-960.webp 960w" sizes="(max-width: 760px) calc(100vw - 40px), (max-width: 1300px) 43vw, 510px">
<img src="assets/images/ritam-ghosh.jpg" alt="Ritam Ghosh wearing a navy blazer and white shirt" width="960" height="800" fetchpriority="high"></picture></div>
<figcaption><span>Based in Kolkata, India</span><span class="portrait-note">Think. Build. Iterate.</span></figcaption></figure>
<div class="hero-foot"><span>Full-stack development</span><span>Retrieval &amp; AI</span><span>Competitive programming</span><span class="scroll-note">Scroll to explore ↓</span></div></section>
<section id="work" class="work section wrap" aria-labelledby="work-title"><div class="section-heading" data-reveal><div><p class="eyebrow">01 / Selected work</p><h2>Built with curiosity.<br><em>Made to be used.</em></h2></div><a class="text-link" href="https://github.com/ritamghosh1?tab=repositories">All repositories <span aria-hidden="true">↗</span></a></div>
<div class="work-toolbar"><div class="filters" role="group" aria-label="Filter projects" hidden><button type="button" aria-pressed="true" data-filter="all">All work <span>03</span></button><button type="button" aria-pressed="false" data-filter="ai">AI &amp; retrieval</button><button type="button" aria-pressed="false" data-filter="web">Web &amp; systems</button></div><p class="rail-hint" hidden>Swipe or use the arrows <span aria-hidden="true">↔</span></p></div>
<div id="project-track" class="project-track" aria-label="Selected projects">'''
    s += ''.join(project_card(p) for p in PROJECTS)
    s += '''</div><p id="empty-projects" hidden>No projects in this category. Choose All work to see every project.</p>
<div class="rail-controls" hidden><p id="project-position" role="status" aria-live="polite" aria-atomic="true">01 / 03 — Ask the Book</p><div><button type="button" id="project-prev" aria-label="Previous project" aria-controls="project-track">←</button><button type="button" id="project-next" aria-label="Next project" aria-controls="project-track">→</button></div></div>
<p id="filter-status" class="sr-only" role="status" aria-atomic="true"></p></section>
<section id="about" class="about section" aria-labelledby="about-title"><div class="wrap about-grid"><div data-reveal><p class="eyebrow">02 / The person behind the projects</p><h2 id="about-title">Curiosity is<br>the common <em>thread.</em></h2><p class="about-lead">I like working at both ends of a problem: understanding the algorithm, then building the experience around it.</p>
<p class="body-copy">Competitive programming keeps me precise. Building applications gives those ideas somewhere to go. My current interests meet at full-stack systems, semantic search, and retrieval-augmented generation.</p>
<div class="coding-links"><p class="mini-label">FIND ME SOLVING PROBLEMS</p><a href="https://codeforces.com/profile/TheOrion">Codeforces ↗</a><a href="https://leetcode.com/u/AlgoRithmic91/">LeetCode ↗</a><a href="https://www.codechef.com/users/algo_rithm_91">CodeChef ↗</a><a href="https://atcoder.jp/users/AlgoRIthmic91">AtCoder ↗</a></div></div>
<div class="about-details" data-reveal><div class="detail-block"><p class="mini-label">EDUCATION / 2024–2028</p><h3>Jadavpur University</h3><p>Bachelor of Computer Science and Engineering</p><p class="detail-meta">CGPA 8.0 / 10.0 · from my supplied resume</p></div>
<div class="detail-block"><p class="mini-label">EXPERIENCE / JUNE 2026–PRESENT*</p><h3>Technology Intern</h3><p>Antahin Abha Foundation · Kolkata</p><p class="body-copy">Building AskAbha Chatbot v2 end-to-end: a RAG engine that retrieves and ranks context by document metadata to ground responses and improve relevance.</p><p class="detail-meta">*Role and dates as listed in my resume.</p></div>
<div class="skills"><div><h3>Build the experience</h3><p>React · TypeScript · JavaScript · HTML/CSS · Tailwind CSS</p></div><div><h3>Connect the system</h3><p>Python · FastAPI · Node.js · SQL · Redis</p></div><div><h3>Explore the possibilities</h3><p>RAG · LlamaIndex · ChromaDB · scikit-learn · Docker · Git</p></div></div></div></div></section>
<section class="achievements section wrap" aria-labelledby="achievements-title"><div class="section-heading" data-reveal><div><p class="eyebrow">03 / Practice, persistence, progress</p><h2 id="achievements-title">A few milestones.<br><em>A lot of practice.</em></h2></div><p class="section-aside">Highlights recorded in my resume.<br>These are not live ratings.</p></div>
<dl class="achievement-stats" data-reveal><div><dt>Codeforces · Expert</dt><dd>1732<span>max rating</span></dd></div><div><dt>CodeChef · 4-star</dt><dd>1816<span>max rating</span></dd></div><div><dt>LeetCode · Knight</dt><dd>2071<span>recorded rating</span></dd></div><div><dt>Across coding platforms</dt><dd>2000+<span>problems solved</span></dd></div></dl>
<ul class="achievement-list"><li data-reveal><span class="achievement-mark" aria-hidden="true">01</span><div><h3>Epochalypse · Srijan 2026</h3><p>1st place. Built an automated market maker algorithm for real-time liquidity provision.</p></div></li><li data-reveal><span class="achievement-mark" aria-hidden="true">01</span><div><h3>Uncode · Srijan 2026</h3><p>1st place. Solved reverse-engineered algorithmic challenges from input-output patterns.</p></div></li><li data-reveal><span class="achievement-mark" aria-hidden="true">271</span><div><h3>Codeforces Round 1089 (Div. 2)</h3><p>Global rank 271 among 15,000+ participants.</p></div></li><li data-reveal><span class="achievement-mark" aria-hidden="true">364</span><div><h3>Codeforces Educational Round 185</h3><p>Global rank 364 among 15,000+ participants.</p></div></li></ul></section></main>'''
    return s + footer()


def case(p):
    prefix = '../'
    s = head(f'{p["name"]} — Ritam Ghosh', p['summary'], f'work/{p["slug"]}.html', prefix) + header(prefix)
    demo = f'<a class="button secondary" href="{p["demo"]}">{e(p["demo_label"])} {arrow()}</a>' if p['demo'] else ''
    s += f'''<main id="main"><article id="top" class="case-study wrap"><a class="back-link" href="../index.html#work">{arrow('←')} All projects</a><div class="case-intro" data-reveal><p class="eyebrow">{p['number']} / {e(p['kind'])}</p><h1>{e(p['name'])}<span>.</span></h1><p class="case-deck">{e(p['summary'])}</p><p class="case-role">{e(p['role'])}</p>{tags(p)}<div class="case-actions"><a class="button primary" href="{p['repo']}">View source {arrow()}</a>{demo}</div><p class="detail-meta">{e(p['status'])}</p></div>
<div class="case-art">{artwork(p)}</div><div class="case-body"><section data-reveal><p class="eyebrow">THE PROBLEM</p><h2>Start with the question.</h2><p>{e(p['problem'])}</p></section><section data-reveal><p class="eyebrow">THE APPROACH</p><h2>A decision that matters.</h2><p>{e(p['decision'])}</p></section>
<section class="architecture" aria-labelledby="flow-title" data-reveal><h2 id="flow-title">How it fits together</h2><ol class="flow">{''.join(f'<li><span>{i+1:02}</span>{e(step)}</li>' for i,step in enumerate(p['flow']))}</ol><p class="detail-meta">{'Intended product flow from the team plan.' if not p['demo'] else 'Simplified flow based on the documented implementation.'}</p></section>
<section data-reveal><p class="eyebrow">THE RESULT</p><h2>What the work shows.</h2><p>{e(p['result'])}</p></section><section data-reveal><p class="eyebrow">THE TAKEAWAY</p><h2>What I’m taking forward.</h2><p>{e(p['lesson'])}</p><p class="next-step"><strong>Next improvement</strong><br>{e(p['next'])}</p></section>
<p class="case-provenance">Based on the supplied resume and the <a href="{p['source']}">project README</a>, reviewed November 7, 2026. Next improvements are proposed follow-up work. Illustrations are not screenshots.</p></div>'''
    n = PROJECTS[(PROJECTS.index(p)+1) % len(PROJECTS)]
    s += f'<a class="next-project" href="{n["slug"]}.html"><span class="eyebrow">NEXT PROJECT</span><span>{e(n["name"])} {arrow("→")}</span></a></article></main>'
    return s + footer(prefix)


(DOCS/'work').mkdir(exist_ok=True)
(DOCS/'index.html').write_text(home())
for project in PROJECTS:
    (DOCS/'work'/f'{project["slug"]}.html').write_text(case(project))
urls = [''] + [f'work/{p["slug"]}.html' for p in PROJECTS]
(DOCS/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(f'<url><loc>{BASE}{url}</loc></url>' for url in urls) + '\n</urlset>\n')
(DOCS/'.nojekyll').touch()
print('Generated portfolio, three case studies, and sitemap.')
