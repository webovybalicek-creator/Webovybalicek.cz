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

// Odlesk pod myší na kartách referencí, ceníku a cest: souřadnice pro CSS (--mx/--my)
if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
  document.addEventListener('pointermove', (e) => {
    const el = e.target.closest && e.target.closest('.ref, .price-card, .feature-card');
    if (!el) return;
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', `${e.clientX - r.left}px`);
    el.style.setProperty('--my', `${e.clientY - r.top}px`);
  }, { passive: true });
}

// Poptávkový formulář: odeslání přes poptavka.php, při odesílání perleťové kapky v tlačítku,
// po úspěchu se formulář rozostří a vyroste kapka s poděkováním. Při chybě zůstane formulář a ukáže se e-mail.
document.querySelectorAll('form.form').forEach((form) => {
  const started = Date.now();
  form.insertAdjacentHTML('afterbegin', '<label class="hp" aria-hidden="true">Web <input type="text" name="web" tabindex="-1" autocomplete="off"></label>');
  form.insertAdjacentHTML('beforeend', '<div class="form-done" aria-live="polite"><div class="pearl"><p>Díky, ozveme se do 24 hodin<small>Mezitím se můžete podívat na naše reference.</small></p></div></div>');
  const btn = form.querySelector('button[type="submit"]');
  const label = btn ? btn.innerHTML : '';
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    form.querySelector('.form-error')?.remove();
    const data = new FormData(form);
    data.set('t', String(Date.now() - started));
    data.set('page', location.pathname);
    if (btn) { btn.classList.add('is-busy'); btn.disabled = true; btn.innerHTML = '<span class="pearl-dots" aria-label="Odesílám"><span class="pearl"></span><span class="pearl"></span><span class="pearl"></span></span>'; }
    let ok = false;
    try {
      const res = await fetch('/poptavka.php', { method: 'POST', body: data, headers: { Accept: 'application/json' } });
      ok = res.ok && (await res.json()).ok === true;
    } catch (err) { ok = false; }
    if (btn) { btn.classList.remove('is-busy'); btn.disabled = false; btn.innerHTML = label; }
    if (ok) {
      form.classList.add('is-sent');
      form.reset();
    } else {
      btn?.insertAdjacentHTML('beforebegin', '<p class="form-error" role="alert">Zprávu se nepodařilo odeslat. Napište nám prosím na <a href="mailto:webovybalicek@gmail.com">webovybalicek@gmail.com</a> nebo zavolejte na <a href="tel:+420723933774">723 933 774</a>.</p>');
    }
  });
});

// Perleťová kulička jako „tečka“ za nadpisem sekce, kterou právě čtete. Při scrollu přeskočí obloukem
// na konec dalšího nadpisu – pomáhá v orientaci. Jen na úvodní stránce.
(() => {
  if (!document.querySelector('.hero-stage')) return;
  const heads = [...document.querySelectorAll('main .section-head h2, #kontakt h2')].filter((h) => !h.closest('dialog'));
  if (heads.length < 2) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const drop = document.createElement('div');
  drop.className = 'scroll-drop pearl';
  drop.setAttribute('aria-hidden', 'true');
  document.body.append(drop);
  let active = -1, pos = null, anim = null;

  // konec posledního řádku nadpisu (kde by stála tečka)
  const target = (h) => {
    const r = document.createRange();
    r.selectNodeContents(h);
    const rects = [...r.getClientRects()].filter((x) => x.width > 0);
    const last = rects[rects.length - 1] || h.getBoundingClientRect();
    const fs = parseFloat(getComputedStyle(h).fontSize);
    const size = Math.max(11, Math.round(fs * 0.27));
    return { x: last.right + fs * 0.12 + scrollX, y: last.bottom - fs * 0.2 - size + scrollY, size };
  };
  const place = (p) => {
    drop.style.width = drop.style.height = `${p.size}px`;
    drop.style.transform = `translate(${p.x}px, ${p.y}px)`;
  };
  const hop = (from, to) => {
    anim?.cancel();
    drop.style.width = drop.style.height = `${to.size}px`;
    if (reduced || !from) { place(to); return; }
    const dist = Math.hypot(to.x - from.x, to.y - from.y);
    const lift = Math.min(260, 60 + dist * 0.18);
    const mx = (from.x + to.x) / 2, my = Math.min(from.y, to.y) - lift;
    const t = (x, y, sx = 1, sy = 1) => ({ transform: `translate(${x}px, ${y}px) scale(${sx}, ${sy})` });
    anim = drop.animate([
      t(from.x, from.y, 1.15, 0.85),
      { ...t(from.x, from.y - 4, 0.9, 1.12), offset: 0.12 },
      { ...t(mx, my, 1, 1), offset: 0.5, easing: 'cubic-bezier(.5, 0, .9, .5)' },
      { ...t(to.x, to.y, 0.92, 1.1), offset: 0.88 },
      { ...t(to.x, to.y + 1, 1.25, 0.78), offset: 0.94 },
      t(to.x, to.y, 1, 1),
    ], { duration: Math.min(900, 480 + dist * 0.25), easing: 'cubic-bezier(.3, 0, .2, 1)' });
    anim.onfinish = () => { place(to); anim = null; };
  };
  const update = () => {
    const line = innerHeight * 0.45;
    let i = -1;
    heads.forEach((h, k) => { if (h.getBoundingClientRect().top < line) i = k; });
    // na konci stránky se poslední nadpis nemusí dostat nad čáru – vezmeme ten poslední viditelný
    if (scrollY + innerHeight >= document.documentElement.scrollHeight - 4) heads.forEach((h, k) => { if (h.getBoundingClientRect().top < innerHeight * 0.85) i = k; });
    drop.classList.toggle('is-on', i >= 0);
    if (i < 0) { active = -1; pos = null; return; }
    if (i !== active) {
      const to = target(heads[i]);
      hop(active >= 0 ? pos : null, to);
      active = i; pos = to;
    }
  };
  let tick = 0;
  addEventListener('scroll', () => { if (!tick) tick = requestAnimationFrame(() => { tick = 0; update(); }); }, { passive: true });
  const relayout = () => { if (active >= 0) { pos = target(heads[active]); if (!anim) place(pos); } };
  addEventListener('resize', relayout);
  document.fonts?.ready.then(relayout);
  update();
})();
