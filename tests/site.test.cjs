const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { JSDOM } = require('jsdom');
const axe = require('axe-core');
const html = readFileSync('docs/index.html', 'utf8');
function setup(options = {}) {
  const dom = new JSDOM(html, { url: 'https://example.com/ritamghosh1/', runScripts: 'outside-only', pretendToBeVisual: true });
  const { window: w } = dom;
  const media = new Map();
  w.matchMedia = (query) => {
    if (!media.has(query)) {
      const m = new w.EventTarget();
      m.matches = query.includes('reduced-motion') ? !!options.reduced : false;
      m.media = query;
      media.set(query, m);
    }
    return media.get(query);
  };
  if (options.storageDenied) Object.defineProperty(w, 'localStorage', { get() { throw new Error('Denied'); } });
  else if (options.saved) w.localStorage.setItem('portfolio-theme', options.saved);
  const scrolling = [];
  w.HTMLElement.prototype.scrollTo = function(value) { this.scrollLeft = value.left; scrolling.push(value); };
  const projects = [...w.document.querySelectorAll('.project')];
  projects.forEach((p) => Object.defineProperty(p, 'offsetLeft', { get: () => projects.filter(x => !x.hidden).indexOf(p) * 1000 }));
  const observers = [];
  w.IntersectionObserver = class {
    constructor(callback) { this.callback = callback; observers.push(this); }
    observe() {} unobserve() {} disconnect() { this.disconnected = true; }
  };
  const animations=[];
  w.HTMLElement.prototype.animate = function() {
    const a={finished: new Promise(() => {}), cancelled: false, cancel() { this.cancelled=true; }};
    animations.push(a); return a;
  };
  Object.defineProperty(w.navigator,'clipboard',{value:{writeText:async value => { if(options.copyDenied) throw new Error('Denied'); w.copied=value; }}});
  w.eval(readFileSync('docs/theme.js','utf8'));
  w.eval(readFileSync('docs/script.js','utf8'));
  return { w, d:w.document, dom, media, scrolling, animations, observers };
}
test('project navigation reaches finite boundaries and supports keyboard Home/End', () => {
  const {d,w,dom}=setup();
  assert.equal(d.querySelector('#project-prev').disabled,true);
  d.querySelector('#project-next').click();
  assert.match(d.querySelector('#project-position').textContent,/02 \/ 03 — AlgoCoach/);
  d.querySelector('#project-next').click();
  assert.equal(d.querySelector('#project-next').disabled,true);
  const track=d.querySelector('#project-track');
  track.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Home',bubbles:true}));
  assert.match(d.querySelector('#project-position').textContent,/01 \/ 03/);
  track.dispatchEvent(new w.KeyboardEvent('keydown',{key:'End',bubbles:true}));
  assert.match(d.querySelector('#project-position').textContent,/03 \/ 03/);
  dom.window.close();
});
test('filters reset the rail, update accessible count, and preserve case-study links', () => {
  const {d,dom}=setup();
  d.querySelector('#project-next').click();
  d.querySelector('[data-filter="web"]').click();
  assert.match(d.querySelector('#filter-status').textContent,/2 projects shown/);
  assert.match(d.querySelector('#project-position').textContent,/01 \/ 02 — AlgoCoach/);
  assert.equal(d.querySelector('[data-name="Ask the Book"]').hidden,true);
  assert.equal(d.querySelector('[data-filter="web"]').getAttribute('aria-pressed'),'true');
  d.querySelector('[data-filter="all"]').click();
  assert.equal(d.querySelectorAll('.project:not([hidden])').length,3);
  assert.equal(d.querySelectorAll('a[href^="work/"]').length,3);
  dom.window.close();
});
test('empty categories have a visible recovery message and no usable arrows', () => {
  const {d,dom}=setup();
  const filter=d.querySelector('[data-filter="web"]');filter.dataset.filter='none';filter.click();
  assert.equal(d.querySelector('#empty-projects').hidden,false);
  assert.equal(d.querySelector('#project-next').disabled,true);
  assert.equal(d.querySelector('#project-prev').disabled,true);
  dom.window.close();
});
test('keyboard focus on another project brings that card into view without vertical scrolling', () => {
  const {d,w,scrolling,dom}=setup();
  d.querySelectorAll('.project a')[3].dispatchEvent(new w.FocusEvent('focusin',{bubbles:true}));
  const link=d.querySelector('[data-name="Arrakis"] a');
  link.dispatchEvent(new w.FocusEvent('focusin',{bubbles:true}));
  assert.match(d.querySelector('#project-position').textContent,/03 \/ 03 — Arrakis/);
  assert.equal(scrolling.at(-1).left,2000);
  assert.equal('top' in scrolling.at(-1),false);
  dom.window.close();
});
test('theme persists and storage denial leaves a working in-session theme', () => {
  for (const storageDenied of [false,true]) {
    const {d,w,dom}=setup({storageDenied,saved:'dark'});
    if(!storageDenied) assert.equal(d.documentElement.dataset.theme,'dark');
    const select=d.querySelector('#theme');select.value='dark';select.dispatchEvent(new w.Event('change'));
    assert.equal(d.documentElement.dataset.theme,'dark');
    assert.equal(d.querySelector('meta[name="theme-color"]').content,'#11232e');
    if(!storageDenied) assert.equal(w.localStorage.getItem('portfolio-theme'),'dark');
    dom.window.close();
  }
});
test('reduced motion starts without animations and a live change cancels current motion', () => {
  const first=setup({reduced:true});
  assert.equal(first.animations.length,0);
  first.d.querySelector('#project-next').click();
  assert.equal(first.scrolling.at(-1).behavior,'instant');
  first.dom.window.close();
  const second=setup();
  assert.ok(second.animations.length>0);
  const m=second.media.get('(prefers-reduced-motion: reduce)');m.matches=true;m.dispatchEvent(new second.w.Event('change'));
  assert.equal(second.animations.every(a=>a.cancelled),true);
  assert.equal(second.observers[0].disconnected,true);
  second.dom.window.close();
});
test('copy email reports success and a useful fallback when clipboard is denied', async () => {
  for (const copyDenied of [false,true]) {
    const {d,w,dom}=setup({copyDenied});d.querySelector('#copy-email').click();
    await new Promise(resolve=>setImmediate(resolve));
    assert.match(d.querySelector('#copy-status').textContent,copyDenied ? /mail app/ : /copied/);
    if(!copyDenied) assert.equal(w.copied,'ritamghosh548@gmail.com');
    dom.window.close();
  }
});
test('without JavaScript all project stories and resume/contact links remain accessible', () => {
  const dom=new JSDOM(html);const d=dom.window.document;
  assert.equal(d.querySelectorAll('.project[hidden]').length,0);
  assert.equal(d.querySelector('#project-track').classList.contains('is-carousel'),false);
  assert.equal(d.querySelectorAll('.project a[href^="work/"]').length,3);
  assert.ok(d.querySelector('a[download]'));
  assert.ok(d.querySelector('a[href^="mailto:"]'));
  assert.equal(d.querySelector('.theme-control').hidden,true);
  dom.window.close();
});
test('all generated pages pass automated semantic accessibility checks', async () => {
  for(const path of ['docs/index.html','docs/work/ask-the-book.html','docs/work/algocoach.html','docs/work/arrakis.html']) {
    const dom=new JSDOM(readFileSync(path,'utf8'),{runScripts:'outside-only'});
    // Canvas rendering is unavailable in jsdom; contrast is checked separately.
    dom.window.HTMLCanvasElement.prototype.getContext = () => null;
    dom.window.eval(axe.source);
    const results=await dom.window.axe.run(dom.window.document,{rules:{'color-contrast':{enabled:false}}});
    assert.equal(results.violations.length,0,path + ': ' + JSON.stringify(results.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)}))));
    dom.window.close();
  }
});

test('system theme follows OS changes and case-study enhancements initialize safely', async () => {
  const {w,d,media,dom}=setup();
  const system=media.get('(prefers-color-scheme: dark)');system.matches=true;system.dispatchEvent(new w.Event('change'));
  assert.equal(d.documentElement.dataset.theme,'dark');
  w.portfolioTheme.set('light');system.dispatchEvent(new w.Event('change'));
  assert.equal(d.documentElement.dataset.theme,'light');
  dom.window.close();
  const caseDom=new JSDOM(readFileSync('docs/work/algocoach.html','utf8'),{url:'https://example.com/work/algocoach.html',runScripts:'outside-only'});
  caseDom.window.matchMedia=()=>({matches:true,addEventListener(){}});
  caseDom.window.eval(readFileSync('docs/theme.js','utf8'));
  caseDom.window.eval(readFileSync('docs/script.js','utf8'));
  assert.equal(caseDom.window.document.querySelector('#copy-email').hidden,false);
  caseDom.window.close();
});
test('enhanced homepage has named controls and no semantic accessibility violations', async () => {
  const {w,d,dom}=setup();
  w.HTMLCanvasElement.prototype.getContext=()=>null;
  w.eval(axe.source);
  const result=await w.axe.run(d,{rules:{'color-contrast':{enabled:false}}});
  assert.equal(result.violations.length,0,JSON.stringify(result.violations.map(v=>v.id)));
  dom.window.close();
});
