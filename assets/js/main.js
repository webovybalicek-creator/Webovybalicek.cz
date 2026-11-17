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
// Reference: web v okně nejdřív „postaví“ roj kurzorů (kreslí bloky, píše nadpisy), pak se snímek sám pomalu posouvá
// a myš nad oknem ho projíždí podle své výšky. Vlastní implementace, inspirace: Swarm (Joel Califa) a Swarm Rebuild.
(() => {
  const shots = [...document.querySelectorAll('[data-shot]')].map((el) => ({
    el, win: el.querySelector('.shot-win'), img: el.querySelector('img'), y: 0, dir: 1, wait: 0, goal: null, seen: false, state: 'idle',
  }));
  if (!shots.length) return;
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  // barvy značky: [jmenovka, barva kurzoru a rámečku, barva textu jmenovky, obrys šipky]
  const CREW = [['Návrh', '#0a1217', '#fff', '#fff'], ['Texty', '#cdfe00', '#0a1217', '#0a1217'], ['Kód', '#54595d', '#fff', '#fff'], ['AI', '#c3c6c8', '#0a1217', '#0a1217']];
  const ARROW = (stroke) => `<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M1.5 1.2l4.6 12.6 2-5.3 5.3-2z" fill="currentColor" stroke="${stroke}" stroke-width="1.1" stroke-linejoin="round"/></svg>`;
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const mk = (cls, parent) => { const n = document.createElement('span'); n.className = cls; parent.append(n); return n; };

  // náhradní rozložení, když pro web nemáme změřené bloky
  const fallback = () => {
    const b = [['b', 0, 0, 1440, 90], ['t', 120, 260, 620, 150], ['t', 120, 440, 480, 70], ['k', 120, 560, 220, 60], ['m', 800, 200, 520, 520]];
    for (let r = 0; r < 2; r++) for (let c = 0; c < 3; c++) b.push(['m', 120 + c * 410, 860 + r * 420, 380, 260], ['t', 120 + c * 410, 1140 + r * 420, 300, 40]);
    return b;
  };

  async function build(s) {
    s.state = 'building';
    const k = s.win.clientWidth / 1440, H = s.win.clientHeight, W = s.win.clientWidth;
    let raw = []; try { raw = JSON.parse(s.el.dataset.blocks || '[]'); } catch (e) { raw = []; }
    if (raw.length < 5) raw = fallback();
    let blocks = raw.map(([t, x, y, w, h]) => ({ t, x: x * k, y: y * k, w: w * k, h: Math.min(h * k, H - y * k) })).filter((b) => b.y < H - 6 && b.w > 10 && b.h > 5);
    if (blocks.length > 26) blocks = blocks.slice(0, 26);
    // stavět shora dolů: hlavička, pak bloky podle výšky (v jednom řádku zleva doprava, fotky dřív než text)
    const row = (b) => Math.round(b.y / (H / 14));
    blocks.sort((a, b) => (a.t === 'b' ? -1 : b.t === 'b' ? 1 : row(a) - row(b) || (a.t === 'm' ? -1 : 0) - (b.t === 'm' ? -1 : 0) || a.x - b.x));
    // hotový web se odkrývá jako opona hned za rojem, aby nahoře nezůstávala prázdná místa
    const imgH = s.img.offsetHeight;
    const reveal = (y) => { s.img.style.clipPath = `inset(0 0 ${Math.max(0, imgH - y)}px 0)`; };
    s.img.style.transition = 'none'; reveal(0); s.win.classList.add('is-curtain');
    void s.img.offsetHeight; s.img.style.transition = '';
    const queue = blocks.slice(), open = new Set();
    const front = () => { let y = queue.length ? queue[0].y : H; for (const b of open) y = Math.min(y, b.y); reveal(Math.max(0, y - 2)); };
    const layer = mk('swarm', s.win);
    const src = s.img.currentSrc || s.img.src;
    const n = Math.max(2, Math.min(CREW.length, Math.ceil(blocks.length / 4)));
    const crew = CREW.slice(0, n).map(([name, color, ink, stroke], i) => {
      const c = mk('swarm-cur', layer); c.style.color = color; c.innerHTML = ARROW(stroke) + `<b style="-webkit-text-fill-color:${ink}">` + name + '</b>';
      const a = (i / n) * Math.PI * 2; c.pos = { x: W / 2 + Math.cos(a) * 26, y: H * 0.4 + Math.sin(a) * 26 };
      c.style.transform = `translate(${c.pos.x}px,${c.pos.y}px)`;
      return c;
    });
    const move = (c, x, y, ms, ease = 'cubic-bezier(.3,.7,.2,1)') => {
      const from = c.pos; c.pos = { x, y };
      return c.animate([{ transform: `translate(${from.x}px,${from.y}px)` }, { transform: `translate(${x}px,${y}px)` }], { duration: ms, easing: ease, fill: 'forwards' }).finished;
    };
    await sleep(250 + (shots.indexOf(s) % 4) * 220); // okna nezačínají naráz
    const speed = s.fast ? 0.55 : 1;
    const work = async (c) => {
      while (queue.length) {
        if (s.state !== 'building') return;
        const b = queue.shift(); open.add(b);
        const d = Math.hypot(b.x - c.pos.x, b.y - c.pos.y);
        await move(c, b.x, b.y, (160 + Math.min(260, d * 0.9)) * speed);
        const box = mk('swarm-box swarm-box--' + b.t, layer);
        box.style.cssText = `left:${b.x}px;top:${b.y}px;color:${c.style.color};background-image:url("${src}");background-size:${W}px auto;background-position:${-b.x}px ${-b.y}px`;
        const typed = b.t === 't' || b.t === 'k';
        const ms = (typed ? 200 + Math.min(420, b.w * 1.6) : 240 + Math.min(360, (b.w + b.h) * 0.7)) * speed;
        const from = typed ? { width: '0px', height: b.h + 'px' } : { width: '0px', height: '0px' };
        const grow = box.animate([from, { width: b.w + 'px', height: b.h + 'px' }], { duration: ms, easing: typed ? 'steps(' + Math.max(4, Math.round(b.w / 14)) + ')' : 'cubic-bezier(.3,.7,.2,1)', fill: 'forwards' }).finished;
        await Promise.all([grow, move(c, b.x + b.w, b.y + b.h, ms, typed ? 'linear' : undefined)]);
        box.classList.add('is-in');
        open.delete(b); front();
        await sleep(70 * speed);
      }
    };
    await Promise.all(crew.map((c) => work(c)));
    reveal(imgH);
    if (s.state !== 'building') { layer.remove(); return; }
    s.win.classList.add('is-built');
    crew.forEach((c, i) => { c.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 300, delay: i * 60, fill: 'forwards' }); });
    await sleep(650);
    layer.remove(); s.img.style.clipPath = ''; s.win.classList.remove('is-curtain');
    s.state = 'built'; s.wait = 900;
  }

  const start = (s) => {
    if (s.state !== 'idle' || !s.seen || !(s.img.complete && s.img.naturalWidth)) return;
    if (calm) { s.win.classList.add('is-built'); s.state = 'built'; return; }
    build(s);
  };
  const io = new IntersectionObserver((es) => es.forEach((e) => { const s = shots.find((x) => x.el === e.target); if (s) { s.seen = e.isIntersecting; start(s); } }), { threshold: 0.25 });
  shots.forEach((s) => {
    if (!calm) s.win.classList.add('is-swarm');
    io.observe(s.el);
    const ready = () => { s.win.classList.add('is-ready'); start(s); };
    if (s.img.complete && s.img.naturalWidth) ready(); else s.img.addEventListener('load', ready, { once: true });
    if (!fine) return;
    s.el.addEventListener('pointerenter', () => { s.fast = true; });
    s.el.addEventListener('pointermove', (e) => { if (s.state !== 'built') return; const r = s.win.getBoundingClientRect(); s.goal = Math.min(1, Math.max(0, (e.clientY - r.top) / r.height)); });
    s.el.addEventListener('pointerleave', () => { s.goal = null; s.wait = 500; });
  });
  // tlačítko na pracovní stránce: postavit všechna okna znovu
  document.querySelectorAll('[data-shots-replay]').forEach((btn) => btn.addEventListener('click', () => {
    shots.forEach((s) => { s.state = 'idle'; s.y = 0; s.dir = 1; s.fast = false; s.img.style.transform = ''; s.win.classList.remove('is-built', 'is-curtain'); s.img.style.clipPath = ''; s.win.querySelectorAll('.swarm').forEach((n) => n.remove()); });
    requestAnimationFrame(() => shots.forEach(start));
  }));

  let last = performance.now();
  const tick = (now) => {
    const dt = Math.min(64, now - last); last = now;
    for (const s of shots) {
      if (!s.seen || s.state !== 'built') continue;
      const max = s.img.offsetHeight - s.win.clientHeight;
      if (max <= 0) continue;
      if (s.goal !== null) s.y += (s.goal * max - s.y) * Math.min(1, dt / 140);
      else if (calm) continue;
      else if (s.wait > 0) { s.wait -= dt; continue; }
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
