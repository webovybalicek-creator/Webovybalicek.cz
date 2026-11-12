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

// Vlastní kurzor – malá tečka místo šipky a kruh, který na odkazech a tažitelných prvcích invertuje to, co je pod ním.
// Jen pro myš (hover + přesný ukazatel); na dotykových zařízeních se nic nemění.
(() => {
  if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const el = document.createElement('div');
  el.className = 'cursor';
  el.setAttribute('aria-hidden', 'true');
  el.innerHTML = '<span><b></b></span>';
  document.body.appendChild(el);
  const label = el.querySelector('b');
  document.documentElement.classList.add('has-cursor');

  const LABELS = [['.card.ref', 'Zobrazit']];
  const QUIET = '.btn--primary, .announce, .hero-msg-tag, input, textarea, select'; // limetkové plochy a formuláře: jen tečka
  const LINKS = 'a, button, summary, [role="tab"], label';
  let x = -100, y = -100, tx = -100, ty = -100, raf = 0;

  const tick = () => {
    const k = reduced ? 1 : 0.22;
    x += (tx - x) * k; y += (ty - y) * k;
    el.style.transform = `translate3d(${x}px,${y}px,0)`;
    raf = Math.abs(tx - x) + Math.abs(ty - y) > 0.1 ? requestAnimationFrame(tick) : 0;
  };
  const setState = (t) => {
    let text = '', link = false;
    if (t && t.closest && !t.closest(QUIET)) {
      const own = t.closest('[data-cursor]');
      if (own) text = own.dataset.cursor;
      else { const hit = LABELS.find(([sel]) => t.closest(sel)); if (hit) text = hit[1]; else link = !!t.closest(LINKS); }
    }
    if (text) label.textContent = text;
    el.classList.toggle('is-label', !!text);
    el.classList.toggle('is-link', !text && link);
  };
  window.addEventListener('pointermove', (e) => {
    if (e.pointerType !== 'mouse') return;
    tx = e.clientX; ty = e.clientY;
    if (x < -50) { x = tx; y = ty; }
    setState(e.target);
    if (!raf) raf = requestAnimationFrame(tick);
  }, { passive: true });
  window.addEventListener('pointerdown', () => el.classList.add('is-down'));
  window.addEventListener('pointerup', () => el.classList.remove('is-down'));
  document.documentElement.addEventListener('mouseleave', () => el.classList.remove('is-label', 'is-link'));
})();
