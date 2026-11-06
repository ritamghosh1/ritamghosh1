'use strict';
(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const year = document.querySelector('#year');
  if (year) year.textContent = new Date().getFullYear();

  const theme = document.querySelector('#theme');
  if (theme && window.portfolioTheme) {
    theme.value = window.portfolioTheme.preference;
    theme.closest('.theme-control').hidden = false;
    theme.addEventListener('change', () => window.portfolioTheme.set(theme.value));
  }

  const copy = document.querySelector('#copy-email');
  if (copy) {
    copy.hidden = false;
    copy.addEventListener('click', async () => {
      const status = document.querySelector('#copy-status');
      try {
        await navigator.clipboard.writeText('ritamghosh548@gmail.com');
        status.textContent = 'Email address copied.';
      } catch {
        status.textContent = 'Copy the email address above, or select it to open your mail app.';
      }
    });
  }

  const track = document.querySelector('#project-track');
  if (track) {
    const projects = [...track.querySelectorAll('[data-category]')];
    const filters = [...document.querySelectorAll('[data-filter]')];
    const previous = document.querySelector('#project-prev');
    const next = document.querySelector('#project-next');
    const position = document.querySelector('#project-position');
    const empty = document.querySelector('#empty-projects');
    let visible = projects.slice();
    let current = 0;
    let settle;

    const update = () => {
      previous.disabled = current === 0 || !visible.length;
      next.disabled = current >= visible.length - 1;
      const text = visible.length
        ? `${String(current + 1).padStart(2, '0')} / ${String(visible.length).padStart(2, '0')} — ${visible[current].dataset.name}`
        : 'No projects';
      if (position.textContent !== text) position.textContent = text;
    };
    const go = (index, behavior = reduced.matches ? 'instant' : 'smooth') => {
      if (!visible.length) return;
      current = Math.max(0, Math.min(index, visible.length - 1));
      const left = visible[current].offsetLeft;
      track.scrollTo({ left, behavior });
      update();
    };
    track.classList.add('is-carousel');
    track.tabIndex = 0;
    track.setAttribute('role', 'region');
    track.setAttribute('aria-roledescription', 'carousel');
    track.setAttribute('aria-label', 'Selected projects. Use left and right arrow keys to browse.');
    document.querySelector('.rail-controls').hidden = false;
    document.querySelector('.rail-hint').hidden = false;
    document.querySelector('.filters').hidden = false;
    previous.addEventListener('click', () => go(current - 1));
    next.addEventListener('click', () => go(current + 1));
    track.addEventListener('keydown', (event) => {
      if (event.target !== track || event.altKey || event.ctrlKey || event.metaKey) return;
      const positions = { ArrowLeft: current - 1, ArrowRight: current + 1, Home: 0, End: visible.length - 1 };
      if (event.key in positions) {
        event.preventDefault();
        go(positions[event.key]);
      }
    });
    track.addEventListener('focusin', (event) => {
      const project = event.target.closest('.project');
      const index = visible.indexOf(project);
      if (index !== -1 && index !== current) go(index, 'instant');
    });
    // Scroll only updates position feedback; it never drives a visual animation.
    track.addEventListener('scroll', () => {
      clearTimeout(settle);
      settle = setTimeout(() => {
        if (!visible.length) return;
        const offsets = visible.map((item) => Math.abs(item.offsetLeft - track.scrollLeft));
        current = offsets.indexOf(Math.min(...offsets));
        update();
      }, 100);
    }, { passive: true });
    for (const button of filters) {
      button.addEventListener('click', () => {
        clearTimeout(settle);
        for (const item of filters) item.setAttribute('aria-pressed', String(item === button));
        for (const project of projects) {
          project.hidden = button.dataset.filter !== 'all' && !project.dataset.category.split(' ').includes(button.dataset.filter);
        }
        visible = projects.filter((project) => !project.hidden);
        current = 0;
        empty.hidden = visible.length > 0;
        track.hidden = visible.length === 0;
        document.querySelector('#filter-status').textContent = `${visible.length} ${visible.length === 1 ? 'project' : 'projects'} shown.`;
        track.scrollTo({ left: 0, behavior: 'instant' });
        update();
      });
    }
    if ('ResizeObserver' in window) {
      const sizeObserver = new ResizeObserver(() => go(current, 'instant'));
      sizeObserver.observe(track);
    }
    reduced.addEventListener('change', () => go(current, 'instant'));
    update();
  }

  // Visible HTML is the baseline. Entrances start only when the observer fires.
  const revealDuration = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--motion-reveal')) || 550;
  const animations = new Set();
  let observer;
  const animate = (element, delay = 0) => {
    if (reduced.matches || !element.animate) return;
    const animation = element.animate(
      [{ opacity: 0, transform: 'translateY(16px)' }, { opacity: 1, transform: 'translateY(0)' }],
      { duration: revealDuration, delay, easing: 'ease-out', fill: 'backwards' },
    );
    animations.add(animation);
    const remove = () => animations.delete(animation);
    animation.finished.then(remove, remove);
  };
  const hero = document.querySelector('.hero-intro');
  if (hero) animate(hero);
  const reveal = [...document.querySelectorAll('[data-reveal]')];
  if (!reduced.matches && 'IntersectionObserver' in window) {
    let remaining = reveal.length;
    observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        observer.unobserve(entry.target);
        animate(entry.target);
        if (--remaining === 0) observer.disconnect();
      }
    }, { threshold: 0.12 });
    reveal.forEach((element) => observer.observe(element));
  }
  reduced.addEventListener('change', () => {
    if (reduced.matches) {
      observer?.disconnect();
      animations.forEach((animation) => animation.cancel());
      animations.clear();
    }
  });
  window.addEventListener('pagehide', () => animations.forEach((animation) => animation.cancel()));
})();
