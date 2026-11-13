// Explorer „Tři cesty“ – přístupné záložky (šipky, Home/End)
document.querySelectorAll('[data-tabs]').forEach((root) => {
  const tabs = [...root.querySelectorAll('[role="tab"]')];
  const panelOf = (t) => document.getElementById(t.getAttribute('aria-controls'));

  const select = (tab, focus = false) => {
    if (tab.getAttribute('aria-selected') === 'true' && !focus) return;
    tabs.forEach((t) => {
      const on = t === tab;
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      const panel = panelOf(t);
      panel.hidden = !on;
      if (on) {
        panel.classList.remove('is-entering');
        void panel.offsetWidth; // restart animace
        panel.classList.add('is-entering');
      }
    });
    if (focus) tab.focus();
  };

  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => select(tab));
    tab.addEventListener('keydown', (e) => {
      const map = { ArrowDown: i + 1, ArrowRight: i + 1, ArrowUp: i - 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 };
      if (!(e.key in map)) return;
      e.preventDefault();
      select(tabs[(map[e.key] + tabs.length) % tabs.length], true);
    });
  });

  root.classList.add('is-ready');
  tabs.forEach((t) => { if (t.getAttribute('aria-selected') !== 'true') panelOf(t).hidden = true; });
});

// Mobilní menu – zavřít po kliknutí na odkaz
document.querySelectorAll('.mobile-nav a').forEach((a) =>
  a.addEventListener('click', () => a.closest('details').removeAttribute('open'))
);

// Reference – filtr podle roku
document.querySelectorAll('.ref-filter').forEach((bar) => {
  const list = bar.nextElementSibling;
  const items = [...list.querySelectorAll('li[data-year]')];
  bar.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-year]');
    if (!btn) return;
    bar.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', b === btn));
    const y = btn.dataset.year;
    items.forEach((li) => { li.hidden = y !== '' && li.dataset.year !== y; });
  });
});

// Pluginy – filtr podle kategorie
document.querySelectorAll('.cat-filter').forEach((bar) => {
  const groups = [...document.querySelectorAll('[data-group]')];
  bar.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-cat]');
    if (!btn) return;
    bar.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', b === btn));
    const c = btn.dataset.cat;
    groups.forEach((g) => { g.hidden = c !== '' && g.dataset.group !== c; });
  });
});

// Popupy přes nativní <dialog>: [data-open="id"] otevře, [data-focus] posune na položku a zvýrazní ji,
// zavírá křížek, Esc, klik mimo okno i odkaz s [data-close] (ten pak normálně pokračuje na svůj cíl).
(() => {
  const close = (d) => {
    if (!d.open || d.classList.contains('is-closing')) return;
    d.classList.add('is-closing');
    const done = () => { d.classList.remove('is-closing'); d.close(); };
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) done();
    else {
      const end = (e) => { if (e.target !== d) return; d.removeEventListener('animationend', end); done(); };
      d.addEventListener('animationend', end);
      setTimeout(() => { if (d.classList.contains('is-closing')) { d.removeEventListener('animationend', end); done(); } }, 400); // pojistka
    }
  };
  document.querySelectorAll('dialog.sheet').forEach((d) => {
    d.addEventListener('cancel', (e) => { e.preventDefault(); close(d); });
    d.addEventListener('click', (e) => {
      if (e.target === d) { close(d); return; }
      const c = e.target.closest('[data-close]');
      if (c) close(d);
    });
    d.addEventListener('close', () => document.documentElement.classList.remove('is-locked'));
  });
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-open]');
    if (!b) return;
    const d = document.getElementById(b.dataset.open);
    if (!d || d.open) return;
    e.preventDefault();
    document.documentElement.classList.add('is-locked');
    document.querySelectorAll('details.mobile-nav[open]').forEach((m) => m.removeAttribute('open'));
    d.showModal();
    d.scrollTop = 0;
    const t = b.dataset.focus && document.getElementById(b.dataset.focus);
    if (t) {
      requestAnimationFrame(() => {
        t.scrollIntoView({ block: 'center' });
        t.classList.remove('is-flash'); void t.offsetWidth; t.classList.add('is-flash');
      });
    }
  });
})();

// Mega menu „Co děláme“: na myši se otevře najetím (s malou prodlevou), jinak kliknutím; Esc a klik mimo zavírá.
document.querySelectorAll('.has-mega').forEach((li) => {
  const btn = li.querySelector('.nav-trigger');
  let t = 0;
  const set = (open) => { clearTimeout(t); li.classList.toggle('is-open', open); btn.setAttribute('aria-expanded', open); };
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  li.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse' && fine.matches) { clearTimeout(t); t = setTimeout(() => set(true), 80); } });
  li.addEventListener('pointerleave', (e) => { if (e.pointerType === 'mouse' && fine.matches) { clearTimeout(t); t = setTimeout(() => set(false), 180); } });
  btn.addEventListener('click', () => set(!li.classList.contains('is-open')));
  li.addEventListener('click', (e) => { if (e.target.closest('.mega a, .mega button')) set(false); });
  document.addEventListener('click', (e) => { if (!li.contains(e.target)) set(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && li.classList.contains('is-open')) { set(false); btn.focus(); } });
  li.addEventListener('focusout', (e) => { if (!li.contains(e.relatedTarget)) set(false); });
});
