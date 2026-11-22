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
  let label = btn ? btn.innerHTML : '';
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (btn) label = btn.innerHTML; // text tlačítka se mění podle záložky
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
  // pruh: při každém načtení jiné pořadí webů (obě kopie smyčky stejně, aby na sebe navazovaly)
  document.querySelectorAll('.shots-loop').forEach((loop) => {
    const lists = [...loop.querySelectorAll('.shots--strip')].map((l) => [l, [...l.children]]);
    const n = lists[0][1].length, order = [...Array(n).keys()];
    for (let i = n - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [order[i], order[j]] = [order[j], order[i]]; }
    lists.forEach(([list, items]) => { if (items.length === n) order.forEach((k) => list.append(items[k])); });
    // první okna jsou vidět hned: nenechat je čekat na líné načtení
    lists[0][0].querySelectorAll('li:nth-child(-n+6) img').forEach((img) => { img.loading = 'eager'; });
  });
  const shots = [...document.querySelectorAll('[data-shot]')].map((el) => ({
    el, win: el.querySelector('.shot-win'), img: el.querySelector('img'), y: 0, dir: 1, wait: 0, goal: null, seen: false, state: 'idle',
  }));
  if (!shots.length) return;
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  // barvy značky: [jmenovka, barva kurzoru a rámečku, barva textu jmenovky, obrys šipky]
  const CREW = [['Návrh', '#0a1217', '#fff', '#fff'], ['Texty', '#cdfe00', '#0a1217', '#cdfe00'], ['Kód', '#54595d', '#fff', '#fff'], ['AI', '#c3c6c8', '#0a1217', '#0a1217']];
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
    s.el.addEventListener('pointermove', (e) => { if (s.state !== 'built' || s.el.closest('.is-dragging')) return; const r = s.win.getBoundingClientRect(); s.goal = Math.min(1, Math.max(0, (e.clientY - r.top) / r.height)); });
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
  // Pruh: nekonečná smyčka, která jede sama a dá se táhnout myší i prstem (se setrvačností)
  document.querySelectorAll('.shots-loop').forEach((loop) => {
    if (calm) return; // při omezeném pohybu zůstává obyčejný vodorovný posuv
    const lists = [...loop.querySelectorAll('.shots--strip')]; if (lists.length < 2) return;
    loop.classList.add('is-js');
    const SPEED = 0.045; // px za ms
    let x = 0, w = 0, vx = 0, drag = null, moved = 0, hover = false, seen = true, prev = performance.now();
    const measure = () => { w = lists[0].offsetWidth; };
    measure(); addEventListener('resize', measure, { passive: true });
    new IntersectionObserver((es) => { seen = es[0].isIntersecting; }).observe(loop);
    loop.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') hover = true; });
    loop.addEventListener('pointerleave', () => { hover = false; });
    loop.addEventListener('pointerdown', (e) => {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      drag = { id: e.pointerId, sx: e.clientX, x0: x, lx: e.clientX, lt: performance.now() }; moved = 0; vx = 0;
    });
    loop.addEventListener('pointermove', (e) => {
      if (!drag || e.pointerId !== drag.id) return;
      const dx = e.clientX - drag.sx; moved = Math.max(moved, Math.abs(dx));
      if (moved > 6 && !loop.classList.contains('is-dragging')) { loop.classList.add('is-dragging'); try { loop.setPointerCapture(e.pointerId); } catch (err) {} }
      if (moved <= 6) return;
      const now = performance.now(); vx = 0.7 * vx + 0.3 * ((e.clientX - drag.lx) / Math.max(1, now - drag.lt));
      drag.lx = e.clientX; drag.lt = now; x = drag.x0 + dx;
    });
    const end = (e) => {
      if (!drag || e.pointerId !== drag.id) return;
      if (performance.now() - drag.lt > 120) vx = 0; // puštěno po zastavení: bez setrvačnosti
      drag = null; setTimeout(() => loop.classList.remove('is-dragging'), 0);
    };
    loop.addEventListener('pointerup', end); loop.addEventListener('pointercancel', end);
    // po tažení neotevírat odkaz, na kterém tah skončil
    loop.addEventListener('click', (e) => { if (moved > 6) { e.preventDefault(); e.stopPropagation(); } }, true);
    loop.addEventListener('dragstart', (e) => e.preventDefault());
    const run = (now) => {
      const dt = Math.min(64, now - prev); prev = now;
      if (seen && w) {
        if (!drag) { if (Math.abs(vx) > 0.01) { x += vx * dt; vx *= Math.pow(0.995, dt); } else { vx = 0; if (!hover) x -= SPEED * dt; } }
        x = ((x % w) - w) % w; // drží se v (-w, 0], druhá kopie navazuje
        const t = `translate3d(${x.toFixed(1)}px,0,0)`; lists.forEach((l) => { l.style.transform = t; });
      }
      requestAnimationFrame(run);
    };
    requestAnimationFrame(run);
  });
})();

// Hlavička: výška do CSS (úvod pod ni zajíždí) a stav po odscrollování
(() => {
  const header = document.querySelector('.site-header'); if (!header) return;
  const size = () => document.documentElement.style.setProperty('--header-h', header.offsetHeight + 'px');
  size(); addEventListener('resize', size, { passive: true });
  const onScroll = () => header.classList.toggle('is-scrolled', header.getBoundingClientRect().top <= 0 && scrollY > 8);
  onScroll(); addEventListener('scroll', onScroll, { passive: true });
})();
// Úvod, varianta „roj“: kurzory v barvách značky kreslí do pozadí obrysy, které po chvíli zmizí
(() => {
  const hero = document.querySelector('[data-air]'); const layer = hero?.querySelector('.air-swarm'); if (!layer) return;
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let seen = true; new IntersectionObserver((es) => { seen = es[0].isIntersecting; }).observe(hero);
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const cursor = (name, color, ink, stroke) => {
    const c = document.createElement('span'); c.className = 'swarm-cur'; c.style.color = color; c.style.opacity = '0';
    c.innerHTML = `<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M1.5 1.2l4.6 12.6 2-5.3 5.3-2z" fill="currentColor" stroke="${stroke}" stroke-width="1.1" stroke-linejoin="round"/></svg><b style="-webkit-text-fill-color:${ink}">${name}</b>`;
    layer.append(c); return c;
  };
  const busy = () => hero.dataset.bg !== 'swarm' || calm || document.hidden || !seen;
  const size = () => { const W = layer.clientWidth, H = layer.clientHeight; return { W, H, wide: W > 900 }; };
  const move = (c, x, y, ms = 900) => { c.style.transition = `transform ${ms}ms cubic-bezier(.3,.7,.2,1), opacity 300ms ease`; c.style.transform = `translate(${x}px,${y}px)`; };

  // Návrh: kreslí rámečky, střídavě limetkový a černý, v pásu mezi textem a bublinou (na mobilu nad nadpisem)
  const design = async (c) => {
    await sleep(500);
    for (let n = 0; ; n++) {
      if (busy()) { await sleep(600); continue; }
      const { W, H, wide } = size(), color = n % 2 ? '#0a1217' : '#cdfe00';
      const w = wide ? 90 + Math.random() * 150 : 50 + Math.random() * 80, h = wide ? 50 + Math.random() * 90 : 30 + Math.random() * 40;
      const x = wide ? W * 0.42 + Math.random() * (W * 0.26 - w) : 14 + Math.random() * Math.max(10, W * 0.5 - w);
      const y = wide ? H * 0.46 + Math.random() * (H * 0.4 - h) : 118 + Math.random() * Math.max(6, 92 - h);
      c.style.opacity = '1'; move(c, x, y); await sleep(950);
      const box = document.createElement('span'); box.className = 'air-box';
      box.style.cssText = `left:${x}px;top:${y}px;width:0;height:0;color:${color};transition:width 700ms cubic-bezier(.3,.7,.2,1),height 700ms cubic-bezier(.3,.7,.2,1),opacity 1600ms ease`;
      layer.prepend(box); void box.offsetWidth; box.style.width = w + 'px'; box.style.height = h + 'px';
      move(c, x + w, y + h); await sleep(1000);
      setTimeout(() => { box.classList.add('is-out'); setTimeout(() => box.remove(), 1700); }, 2800);
      await sleep(1400 + Math.random() * 1200);
    }
  };

  // Texty a Kód: kurzor píše na své místo krátký text, chvíli ho nechá a smaže
  const typist = async (c, cls, delay, spot, lines) => {
    const out = document.createElement('span'); out.className = 'air-type ' + cls; layer.prepend(out);
    await sleep(delay);
    for (let n = 0; ; n++) {
      if (busy()) { await sleep(600); continue; }
      const { W, H, wide } = size(), [x, y] = spot(W, H, wide), text = lines(wide)[n % lines(wide).length];
      out.style.left = x + 'px'; out.style.top = y + 'px'; out.textContent = '';
      c.style.opacity = '1'; move(c, x, y + out.offsetHeight * 0.2); await sleep(1000);
      for (let i = 1; i <= text.length; i++) {
        out.textContent = text.slice(0, i); move(c, x + out.offsetWidth + 2, y + 4, 80);
        await sleep(text[i - 1] === ' ' ? 110 : 45 + Math.random() * 70);
      }
      await sleep(3200);
      for (let i = text.length - 1; i >= 0; i--) { out.textContent = text.slice(0, i); move(c, x + out.offsetWidth + 2, y + 4, 60); await sleep(22); }
      await sleep(1600 + Math.random() * 1200);
    }
  };

  design(cursor('Návrh', '#0a1217', '#fff', '#fff'));
  typist(cursor('Texty', '#cdfe00', '#0a1217', '#cdfe00'), 'air-type--text', 1600,
    (W, H, wide) => wide ? [W * 0.6, H * 0.34] : [W - 232, 232],
    (wide) => wide ? ['Klikněte na bublinu', 'Potáhněte bublinu →'] : ['Klepněte na bublinu ↗']);
  typist(cursor('Kód', '#54595d', '#fff', '#fff'), 'air-type--code', 3200,
    (W, H, wide) => wide ? [W * 0.7, H * 0.8] : [16, 92],
    () => ['<html lang="cs">', '<h1>Tvorba webů</h1>', '<a href="#kontakt">', 'npm run build']);
})();

// Kontakt: záložky „Chci nový web“ / „Jsme agentura“ – mění text vlevo i formulář; /#spoluprace otevře rovnou agenturní
(() => {
  const tabs = [...document.querySelectorAll('[data-contact-tab]')]; if (!tabs.length) return;
  const panel = document.querySelector('[data-contact]'), form = panel.querySelector('form');
  const pick = (kind, focus) => {
    panel.dataset.contact = kind;
    tabs.forEach((t) => { const on = t.dataset.contactTab === kind; t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1; if (on && focus) t.focus(); });
    panel.querySelectorAll('[role="tabpanel"]').forEach((p) => { p.hidden = p.id !== 'kontakt-' + kind; });
    form.querySelectorAll('[data-only]').forEach((el) => { const on = el.dataset.only === kind; el.hidden = !on; el.querySelectorAll('select, input').forEach((f) => { f.disabled = !on; }); });
    form.querySelectorAll('[data-klient]').forEach((el) => { const v = el.dataset[kind]; if (el.matches('textarea, input')) el.placeholder = v; else el.textContent = v; });
    form.elements.segment.value = kind;
    form.classList.remove('is-sent');
  };
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => pick(t.dataset.contactTab));
    t.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); pick(tabs[(i + 1) % tabs.length].dataset.contactTab, true); } });
  });
  form.addEventListener('reset', () => setTimeout(() => { form.elements.segment.value = panel.dataset.contact; })); // po odeslání se formulář čistí, záložka ale zůstává
  const fromHash = () => { if (location.hash === '#spoluprace') { pick('agentura'); document.getElementById('kontakt')?.scrollIntoView(); } };
  fromHash(); addEventListener('hashchange', fromHash);
})();

// Průběh spolupráce: linka se při scrollu plní a dosažené kroky se rozsvítí
(() => {
  const lists = [...document.querySelectorAll('.steps[data-steps]')]; if (!lists.length) return;
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const update = () => lists.forEach((list) => {
    const r = list.getBoundingClientRect(), items = [...list.children];
    const p = calm ? 1 : Math.max(0, Math.min(1, (innerHeight * 0.62 - r.top) / Math.max(1, r.height * 0.85)));
    list.style.setProperty('--p', p.toFixed(4));
    items.forEach((li, i) => li.classList.toggle('is-on', p >= i / (items.length - 1) - 0.01));
  });
  lists.forEach((l) => l.classList.add('is-js'));
  addEventListener('scroll', update, { passive: true }); addEventListener('resize', update); update();
})();

// Vybrané projekty: harmonika – najetím (myš) nebo klepnutím/fokusem se otevře projekt
document.querySelectorAll('[data-proj]').forEach((box) => {
  const items = [...box.children];
  const open = (el) => items.forEach((i) => i.classList.toggle('is-open', i === el));
  items.forEach((el) => {
    el.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') open(el); });
    el.addEventListener('click', () => open(el));
    el.addEventListener('focus', () => open(el));
  });
});

// Popup s videem: iframe se načte až při otevření, při zavření se odstraní (zastaví přehrávání)
document.querySelectorAll('dialog[data-video]').forEach((d) => {
  const box = d.querySelector('.video-frame');
  new MutationObserver(() => {
    if (d.open && !box.firstChild) box.innerHTML = `<iframe src="${d.dataset.video}" title="Video" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`;
  }).observe(d, { attributes: true, attributeFilter: ['open'] });
  d.addEventListener('close', () => { box.innerHTML = ''; });
});

// Slevový kód Toret: e-mail -> slevovy-kod.php pošle stylový e-mail s kódem
document.querySelectorAll('form[data-sleva]').forEach((form) => {
  const started = Date.now();
  form.insertAdjacentHTML('afterbegin', '<label class="hp" aria-hidden="true">Web <input type="text" name="web" tabindex="-1" autocomplete="off"></label>');
  const btn = form.querySelector('button'), msg = form.querySelector('.sleva-msg'), input = form.querySelector('input[type=email]');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    msg.className = 'sleva-msg';
    if (!input.checkValidity()) { msg.textContent = 'Zkontrolujte prosím e-mail.'; msg.classList.add('is-err'); input.focus(); return; }
    const data = new FormData(form); data.set('t', String(Date.now() - started));
    btn.disabled = true; const label = btn.innerHTML; btn.textContent = 'Posílám…';
    let ok = false;
    try { const r = await fetch('/slevovy-kod.php', { method: 'POST', body: data, headers: { Accept: 'application/json' } }); ok = r.ok && (await r.json()).ok === true; } catch (err) { ok = false; }
    btn.disabled = false; btn.innerHTML = label;
    if (ok) { form.classList.add('is-sent'); msg.textContent = 'Hotovo, slevový kód vám posíláme e-mailem.'; msg.classList.add('is-ok'); form.reset(); }
    else { msg.innerHTML = 'Nepodařilo se odeslat. Napište nám na <a href="mailto:webovybalicek@gmail.com">webovybalicek@gmail.com</a>.'; msg.classList.add('is-err'); }
  });
});

// Úvod podstránky: zvýraznění v nadpisu se napustí po načtení, při odscrollování odteče, nahoře se znovu napustí
document.querySelectorAll('.page-hero h1 em').forEach((em) => {
  const h1 = em.closest('h1');
  const set = () => em.classList.toggle('is-full', h1.getBoundingClientRect().bottom > innerHeight * 0.2);
  setTimeout(() => { set(); addEventListener('scroll', () => requestAnimationFrame(set), { passive: true }); }, 250);
});

// Manifest: zvýraznění se napustí, když je věta vidět, a odteče, když odjede z obrazovky (druhé slovo s malým zpožděním)
document.querySelectorAll('.manifest').forEach((p) => {
  const ems = [...p.querySelectorAll('em')];
  new IntersectionObserver(([e]) => ems.forEach((em, i) => setTimeout(() => em.classList.toggle('is-full', e.isIntersecting), e.isIntersecting ? i * 350 : 0)),
    { rootMargin: '-15% 0px -15% 0px' }).observe(p);
});

// Ouško s fotkou: ukáže se skoro na konci stránky, schová se u kontaktního formuláře a patičky s výzvou (na stránce Kontakt vůbec)
(() => {
  const ear = document.querySelector('[data-ear]'); if (!ear) return;
  if (location.pathname.startsWith('/kontakt')) { ear.remove(); return; }
  const form = document.getElementById('kontakt');
  if (form) ear.href = '#kontakt';
  let formSeen = false;
  const seen = new Set(); // kontaktní formulář nebo patička s výzvou na obrazovce = ouško netřeba
  const io = new IntersectionObserver((es) => { es.forEach((e) => e.isIntersecting ? seen.add(e.target) : seen.delete(e.target)); formSeen = seen.size > 0; tick(); });
  [form, document.querySelector('.footer-cta .cta-actions')].forEach((el) => el && io.observe(el));
  function tick() {
    const doc = document.documentElement, left = doc.scrollHeight - (scrollY + innerHeight);
    const progress = scrollY / Math.max(1, doc.scrollHeight - innerHeight);
    ear.classList.toggle('is-on', !formSeen && scrollY > innerHeight * 0.8 && (progress > 0.55 || left < 1400));
  }
  addEventListener('scroll', () => requestAnimationFrame(tick), { passive: true });
  tick();
})();
