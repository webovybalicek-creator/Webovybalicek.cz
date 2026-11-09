// Přepínač „Tři cesty“ – přístupné záložky (šipky, Home/End)
document.querySelectorAll('[data-tabs]').forEach((root) => {
  const tabs = [...root.querySelectorAll('[role="tab"]')];
  const indicator = root.querySelector('.paths-indicator');

  const moveIndicator = (tab) => {
    if (!indicator) return;
    indicator.style.width = `${tab.offsetWidth}px`;
    indicator.style.transform = `translateX(${tab.offsetLeft}px)`;
  };

  const select = (tab, focus = false) => {
    tabs.forEach((t) => {
      const on = t === tab;
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      const panel = document.getElementById(t.getAttribute('aria-controls'));
      panel.hidden = !on;
      if (on) {
        panel.classList.remove('is-entering');
        void panel.offsetWidth; // restart animace
        panel.classList.add('is-entering');
      }
    });
    moveIndicator(tab);
    if (focus) tab.focus();
  };

  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => select(tab));
    tab.addEventListener('keydown', (e) => {
      const map = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 };
      if (!(e.key in map)) return;
      e.preventDefault();
      select(tabs[(map[e.key] + tabs.length) % tabs.length], true);
    });
  });

  root.classList.add('is-ready');
  const current = tabs.find((t) => t.getAttribute('aria-selected') === 'true') || tabs[0];
  tabs.forEach((t) => {
    if (t !== current) document.getElementById(t.getAttribute('aria-controls')).hidden = true;
  });
  // první umístění bez animace
  if (indicator) indicator.style.transition = 'none';
  moveIndicator(current);
  requestAnimationFrame(() => { if (indicator) indicator.style.transition = ''; });

  window.addEventListener('resize', () => moveIndicator(tabs.find((t) => t.getAttribute('aria-selected') === 'true')));
  document.fonts?.ready.then(() => moveIndicator(tabs.find((t) => t.getAttribute('aria-selected') === 'true')));
});

// Mobilní menu – zavřít po kliknutí na odkaz
document.querySelectorAll('.mobile-nav a').forEach((a) =>
  a.addEventListener('click', () => a.closest('details').removeAttribute('open'))
);
