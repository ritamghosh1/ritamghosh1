/* Apply the preference before CSS paints. Storage denial falls back to system. */
(() => {
  const allowed = ['light', 'dark', 'system'];
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  let preference = 'system';
  try {
    const saved = localStorage.getItem('portfolio-theme');
    if (allowed.includes(saved)) preference = saved;
  } catch { /* Private browsing can deny storage. */ }
  const apply = () => {
    const theme = preference === 'system' ? (system.matches ? 'dark' : 'light') : preference;
    document.documentElement.dataset.theme = theme;
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = theme === 'dark' ? '#11232e' : '#f8f9f5';
  };
  window.portfolioTheme = {
    get preference() { return preference; },
    set(value) {
      if (!allowed.includes(value)) return;
      preference = value;
      try { localStorage.setItem('portfolio-theme', value); } catch { /* Preference still works for this visit. */ }
      apply();
    },
  };
  system.addEventListener('change', () => { if (preference === 'system') apply(); });
  window.addEventListener('storage', (event) => {
    if (event.key === 'portfolio-theme') {
      preference = allowed.includes(event.newValue) ? event.newValue : 'system';
      apply();
      const select = document.querySelector('#theme');
      if (select) select.value = preference;
    }
  });
  apply();
})();
