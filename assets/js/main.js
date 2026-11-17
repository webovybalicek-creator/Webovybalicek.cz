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
// Nástroje: najetí na řádek legendy zvýrazní bublinu na oběžné dráze a naopak
document.querySelectorAll('.tools').forEach((box) => {
  const set = (name, on) => box.querySelectorAll(`[data-t="${CSS.escape(name)}"]`).forEach((el) => el.classList.toggle('is-hi', on));
  box.addEventListener('pointerover', (e) => { const el = e.target.closest('[data-t]'); if (el) set(el.dataset.t, true); });
  box.addEventListener('pointerout', (e) => { const el = e.target.closest('[data-t]'); if (el) set(el.dataset.t, false); });
});
// Reference: snímek webu v okně se sám pomalu posouvá; myš nad oknem ho projíždí podle své výšky
(() => {
  const shots = [...document.querySelectorAll('[data-shot]')].map((el) => ({
    el, win: el.querySelector('.shot-win'), img: el.querySelector('img'), y: 0, dir: 1, wait: 0, goal: null, seen: false,
  }));
  if (!shots.length) return;
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const io = new IntersectionObserver((es) => es.forEach((e) => { const s = shots.find((x) => x.el === e.target); if (s) s.seen = e.isIntersecting; }), { rootMargin: '80px' });
  shots.forEach((s, i) => {
    io.observe(s.el);
    const ready = () => s.win.classList.add('is-ready');
    if (s.img.complete && s.img.naturalWidth) ready(); else s.img.addEventListener('load', ready, { once: true });
    s.wait = 600 + (i % 4) * 500; // okna nezačínají všechna naráz
    if (!fine) return;
    s.el.addEventListener('pointermove', (e) => { const r = s.win.getBoundingClientRect(); s.goal = Math.min(1, Math.max(0, (e.clientY - r.top) / r.height)); });
    s.el.addEventListener('pointerleave', () => { s.goal = null; s.wait = 500; });
  });
  let last = performance.now();
  const tick = (now) => {
    const dt = Math.min(64, now - last); last = now;
    for (const s of shots) {
      if (!s.seen) continue;
      const max = s.img.offsetHeight - s.win.clientHeight;
      if (max <= 0) continue;
      if (s.goal !== null) s.y += (s.goal * max - s.y) * Math.min(1, dt / 140);
      else if (calm) continue;
      else if (s.wait > 0) s.wait -= dt;
      else {
        s.y += s.dir * dt * 0.035;
        if (s.y >= max) { s.y = max; s.dir = -1; s.wait = 1400; } else if (s.y <= 0) { s.y = 0; s.dir = 1; s.wait = 1400; }
      }
      s.img.style.transform = `translate3d(0,${-s.y.toFixed(1)}px,0)`;
    }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
  document.querySelectorAll('.shots-wrap').forEach((wrap) => {
    const list = wrap.querySelector('.shots--strip'), [prev, next] = wrap.querySelectorAll('.shots-nav button');
    if (!list || !next) return;
    const step = () => (list.querySelector('li')?.offsetWidth || 300) * 2;
    const sync = () => { prev.disabled = list.scrollLeft < 8; next.disabled = list.scrollLeft > list.scrollWidth - list.clientWidth - 8; };
    prev.addEventListener('click', () => list.scrollBy({ left: -step(), behavior: 'smooth' }));
    next.addEventListener('click', () => list.scrollBy({ left: step(), behavior: 'smooth' }));
    list.addEventListener('scroll', sync, { passive: true }); sync();
  });
})();
