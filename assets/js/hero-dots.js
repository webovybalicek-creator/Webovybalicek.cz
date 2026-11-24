// Úvod – tečkový rastr pozadí, který se v rohu slévá do limetkové koule (halftone „naopak“: tečky nerostou
// do ztracena, ale spojují se do větší). Z koule se dají trhat kapky (tah za kouli) a řezat (tah přes kouli).
// Každá odtržená kapka = jeden bod z [data-hero-points]. Kreslí se obyčejným 2D plátnem – lehké, běží hned.
// Zatím jen náhled: aktivní s ?uvod=tecky (hero-blob.js se pak vypne).
(() => {
  if (!/[?&]uvod=tecky/.test(location.search)) return;
  const stage = document.querySelector('[data-hero]');
  if (!stage) return;
  const canvas = stage.querySelector('.hero-canvas');
  const labels = stage.querySelector('.hero-labels');
  const msg = stage.querySelector('[data-hero-msg]');
  const hintRow = stage.querySelector('.hero-hint');
  const hintEl = stage.querySelector('[data-hero-hint]');
  const resetBtn = stage.querySelector('[data-hero-reset]');
  const dotsBg = document.querySelector('.air-dots');
  const PARTS = [...stage.querySelectorAll('[data-hero-points] li')].slice(0, 6).map((li) => ({
    tag: li.dataset.tag,
    accent: li.hasAttribute('data-accent'),
    head: li.querySelector('strong').textContent,
    text: li.querySelector('span').textContent,
  }));
  if (PARTS.length !== 6) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const narrowMq = window.matchMedia('(max-width: 960px)');
  stage.classList.add('has-gl', 'has-dots');

  // ---- svět: stejné souřadnice jako dřív (kamera CAM, ohnisko F), ať sedí všechny polohy a chování ----
  const F = 11, CAM = 25, N = 8, CORE = 6, AUX = 7;
  const GRID = 11;                       // rozteč teček (polovina rastru pozadí 22 px – každá druhá tečka sedí na tu v pozadí)
  const LIME = [205, 254, 0], GREY = [185, 188, 191];
  const B = Array.from({ length: N }, () => ({ x: 0, y: 0, z: 0, vx: 0, vy: 0, vz: 0, r: 0.1, tx: 0, ty: 0, tz: 0, tr: 0.1 }));
  B[AUX].r = B[AUX].tr = -0.8;
  const lab = PARTS.map((p) => { const l = document.createElement('span'); l.textContent = p.tag; labels.appendChild(l); return l; });
  const det = [0, 0, 0, 0, 0, 0];
  const free = det.map(() => [0, 0]);
  let sel = -1, drag = null, slice = null, torn = false, picked = false, tease = 0;
  let W = 1, H = 1, aspect = 1, scale = 1, snapL = 3, A = [0, 0], dpr = 1, ox = 0, oy = 0, hdrW = 0;
  const ptr = { x: 0, y: 0 };

  const render = () => {
    const n = det.reduce((a, b) => a + b, 0);
    if (n > 0) torn = true;
    hintEl.textContent = n < 6 ? `Odtrženo ${n} z 6. Klikněte na kouli pro další.` : 'Odtrženo všech 6. Klikněte na kapku.';
    hintRow.hidden = n === 0; resetBtn.hidden = n === 0;
    if (sel >= 0) {
      const p = PARTS[sel];
      msg.querySelector('.hero-msg-tag').textContent = p.tag;
      msg.querySelector('.hero-msg-title').textContent = p.head;
      msg.querySelector('.hero-msg-text').textContent = p.text;
      msg.hidden = true; void msg.offsetWidth; msg.hidden = false;
    } else msg.hidden = true;
    lab.forEach((l, i) => l.classList.toggle('is-on', !!det[i]));
  };
  resetBtn.addEventListener('click', () => { det.fill(0); sel = -1; render(); });

  const toWorld = (px, py) => [((px - W / 2) / H * 2) * CAM / F, ((H / 2 - py) / H * 2) * CAM / F];
  const toScreen = (b) => { const k = F / (CAM - b.z); return [(b.x * k / 2) * H + W / 2, H / 2 - (b.y * k / 2) * H, Math.max(b.r, 0) * k / 2 * H]; };
  const clampP = (p, r) => { const hw = aspect * CAM / F - r, hh = CAM / F - r; return [Math.max(-hw, Math.min(hw, p[0])), Math.max(-hh, Math.min(hh, p[1]))]; };

  // kam kapka sama odpluje po kliknutí (v násobcích poloviny šířky a výšky panelu)
  const SPOTS = [[0.04, 0.5], [0.26, 0.04], [0.08, -0.58], [-0.42, 0.26], [0.34, -0.62], [0.56, 0.0]];
  const SPOTS_NARROW = [[-0.72, 0.82], [-0.3, 0.62], [0.74, -0.02], [0.3, 0.3], [0.7, -0.62], [0.72, -0.32]];
  const spread = (keep) => {
    const minD = 1.05 * scale;
    for (let it = 0; it < 6; it++) for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) {
      if (!det[i] || !det[j]) continue;
      let dx = free[j][0] - free[i][0], dy = free[j][1] - free[i][1], d = Math.hypot(dx, dy);
      if (d >= minD) continue;
      if (d < 1e-3) { dx = Math.cos(j * 2.4); dy = Math.sin(j * 2.4); d = 1; }
      const push = minD - d, ux = dx / d, uy = dy / d;
      const wi = i === keep ? 0 : j === keep ? 1 : 0.5, wj = 1 - wi;
      free[i] = clampP([free[i][0] - ux * push * wi, free[i][1] - uy * push * wi], 0.45 * scale);
      free[j] = clampP([free[j][0] + ux * push * wj, free[j][1] + uy * push * wj], 0.45 * scale);
    }
  };
  const release = (i) => {
    const s = (narrowMq.matches ? SPOTS_NARROW : SPOTS)[i];
    det[i] = 1; free[i] = clampP([s[0] * aspect * CAM / F, s[1] * CAM / F], 0.45 * scale); spread(i); sel = i; render();
  };

  const targets = (time) => {
    const hw = aspect * CAM / F, hh = CAM / F;
    scale = Math.min(1, Math.max(0.5, hw / 2.6)) * (aspect < 0.8 ? 0.67 : 1); snapL = 2.5 * scale;
    // pravý horní roh, ale celá koule pod hlavičkou (jinak by s ní splývalo limetkové tlačítko)
    A = [hw - 1.3 * scale, hh - hdrW - 1.3 * scale];
    const core = B[CORE]; core.tx = A[0]; core.ty = A[1]; core.tz = 0; core.tr = 0.98 * scale;
    const pull = drag && drag.moved && !det[drag.i] ? drag.i : -1;
    const P = toWorld(ptr.x, ptr.y), L = Math.hypot(P[0] - A[0], P[1] - A[1]);
    const shrink = Math.max(0.4, Math.min(1, 1.15 - L / snapL));
    const others = []; for (let j = 0; j < 6; j++) if (!det[j] && j !== pull) others.push(j);
    // dokud nikdo nic neodtrhl, jedna kapka se co chvíli sama vysune z koule a vrátí
    const ph = (time - 1.2) % 3.6;
    tease = !torn && !drag && ph >= 0 && ph < 1.1 ? Math.sin(ph / 1.1 * Math.PI) ** 2 : 0;
    for (let i = 0; i < 6; i++) {
      const b = B[i], wob = reduced ? 0 : Math.sin(time * 0.7 + i * 1.9) * 0.05;
      if (drag && drag.moved && drag.i === i) { b.tx = P[0]; b.ty = P[1]; b.tz = 0.3; b.tr = 0.36 * scale; }
      else if (det[i]) { b.tx = free[i][0]; b.ty = free[i][1] + wob; b.tz = sel === i ? 0.5 : 0; b.tr = (sel === i ? 0.42 : 0.32) * scale; }
      else if (pull >= 0) { const t = (others.indexOf(i) + 1) / (others.length + 1) * 0.9; b.tx = A[0] + (P[0] - A[0]) * t; b.ty = A[1] + (P[1] - A[1]) * t; b.tz = 0.1; b.tr = 0.36 * scale * shrink; }
      else {
        const an = (188 + i * 15) * Math.PI / 180, d = (1.1 + (i % 2) * 0.38 + wob + (PARTS[i].accent ? tease * 1.1 : 0)) * scale;
        b.tx = A[0] + Math.cos(an) * d; b.ty = A[1] + Math.sin(an) * d; b.tz = reduced ? 0 : Math.sin(time * 0.6 + i) * 0.15; b.tr = 0.4 * scale;
      }
    }
    const x = B[AUX];
    if (pull >= 0) { x.tx = A[0] + (P[0] - A[0]) * 0.5; x.ty = A[1] + (P[1] - A[1]) * 0.5; x.tz = 0.1; x.tr = 0.22 * scale * shrink; } else x.tr = -0.8;
  };
  const step = (dt) => {
    for (let i = 0; i < N; i++) {
      const b = B[i], fast = i === AUX || (drag && drag.moved && drag.i === i), k = fast ? 120 : (reduced ? 60 : 34), d = fast ? 20 : (reduced ? 16 : 5.2);
      b.vx += ((b.tx - b.x) * k - b.vx * d) * dt; b.vy += ((b.ty - b.y) * k - b.vy * d) * dt; b.vz += ((b.tz - b.z) * k - b.vz * d) * dt;
      b.x += b.vx * dt; b.y += b.vy * dt; b.z += b.vz * dt; b.r += (b.tr - b.r) * (1 - Math.exp(-dt * 8));
    }
  };
  const pick = (px, py) => {
    let best = -1, bd = 1e9;
    for (let i = 0; i < 6; i++) { const s = toScreen(B[i]), d = Math.hypot(px - s[0], py - s[1]); if (d < s[2] * 1.15 && d < bd) { bd = d; best = i; } }
    if (best < 0) {
      const c = toScreen(B[CORE]);
      if (Math.hypot(px - c[0], py - c[1]) < c[2] * 1.15) { bd = 1e9; for (let i = 0; i < 6; i++) if (!det[i]) { const s = toScreen(B[i]), d = Math.hypot(px - s[0], py - s[1]); if (d < bd) { bd = d; best = i; } } }
    }
    return best;
  };
  const crosses = (ax, ay, bx, by, cx, cy, dx, dy) => {
    const o = (px, py, qx, qy, rx, ry) => (qx - px) * (ry - py) - (qy - py) * (rx - px);
    return o(ax, ay, bx, by, cx, cy) * o(ax, ay, bx, by, dx, dy) < 0 && o(cx, cy, dx, dy, ax, ay) * o(cx, cy, dx, dy, bx, by) < 0;
  };
  const local = (e) => { const r = canvas.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };

  canvas.addEventListener('pointerdown', (e) => {
    const p = local(e); ptr.x = p[0]; ptr.y = p[1];
    const i = pick(p[0], p[1]);
    try { canvas.setPointerCapture(e.pointerId); } catch (err) { /* nevadí */ }
    if (i < 0) { drag = null; slice = { x: p[0], y: p[1] }; return; }
    drag = { i, sx: p[0], sy: p[1], moved: false };
  });
  canvas.addEventListener('pointermove', (e) => {
    const p = local(e); ptr.x = p[0]; ptr.y = p[1];
    if (drag) {
      if (!drag.moved && Math.hypot(p[0] - drag.sx, p[1] - drag.sy) > 6) { drag.moved = true; canvas.classList.add('is-drag'); delete canvas.dataset.cursor; }
      if (drag.moved && !det[drag.i]) { const w = toWorld(p[0], p[1]); if (Math.hypot(w[0] - A[0], w[1] - A[1]) > snapL) { det[drag.i] = 1; free[drag.i] = w; sel = drag.i; render(); } }
      return;
    }
    if (slice) {
      const a = toScreen(B[CORE]); let hit = false;
      for (let i = 0; i < 6; i++) if (!det[i]) {
        const s = toScreen(B[i]);
        if (crosses(slice.x, slice.y, p[0], p[1], a[0], a[1], s[0], s[1])) {
          const dx = B[i].x - A[0], dy = B[i].y - A[1], l = Math.hypot(dx, dy) || 1;
          det[i] = 1; free[i] = clampP([B[i].x + dx / l * 1.1 * scale, B[i].y + dy / l * 1.1 * scale], 0.5 * scale);
          B[i].vx += dx / l * 3; B[i].vy += dy / l * 3; hit = true;
        }
      }
      slice.x = p[0]; slice.y = p[1];
      if (hit) { spread(-1); render(); }
      return;
    }
    const over = pick(p[0], p[1]);
    canvas.classList.toggle('is-hit', over >= 0);
    // popisek pro vlastní kurzor (main.js) – jen do prvního odtržení a prvního výběru
    const tip = over < 0 ? '' : det[over] ? (picked ? '' : 'Vybrat') : (torn ? '' : 'Vytáhni');
    if (tip) canvas.dataset.cursor = tip; else delete canvas.dataset.cursor;
  });
  canvas.addEventListener('pointerup', (e) => {
    slice = null;
    if (!drag) { if (sel >= 0) { sel = -1; render(); } return; }
    const d = drag, p = local(e), w = toWorld(p[0], p[1]);
    drag = null; canvas.classList.remove('is-drag');
    if (!d.moved) { delete canvas.dataset.cursor; if (det[d.i]) { sel = d.i; picked = true; render(); } else release(d.i); return; }
    if (det[d.i]) {
      // kapka puštěná zpátky ke kouli se s ní slije – zmizí i její popisek a text
      if (Math.hypot(w[0] - A[0], w[1] - A[1]) < 1.8 * scale) { det[d.i] = 0; if (sel === d.i) sel = -1; }
      else { free[d.i] = clampP(w, 0.45 * scale); spread(d.i); sel = d.i; }
      render();
    }
  });
  canvas.addEventListener('pointercancel', () => { drag = null; slice = null; canvas.classList.remove('is-drag'); });

  const resize = () => {
    W = stage.clientWidth; H = stage.clientHeight;
    if (!W || !H) return;
    aspect = W / H;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.max(2, Math.round(W * dpr)); canvas.height = Math.max(2, Math.round(H * dpr));
    // tečky navazují na rastr pozadí (.air-dots, 22 px)
    const cr = canvas.getBoundingClientRect(), br = (dotsBg || stage).getBoundingClientRect();
    ox = ((br.left - cr.left) % GRID + GRID) % GRID; oy = ((br.top - cr.top) % GRID + GRID) % GRID;
    // výška hlavičky (překrývá horní okraj úvodu) ve světových jednotkách
    const hdr = document.querySelector('.site-header');
    const hb = hdr ? Math.max(0, hdr.getBoundingClientRect().bottom - cr.top) : 0;
    hdrW = hb / H * 2 * CAM / F;
    for (let i = 0; i < 6; i++) if (det[i]) free[i] = clampP(free[i], 0.45 * scale);
    spread(-1);
  };
  if (window.ResizeObserver) new ResizeObserver(resize).observe(stage); else window.addEventListener('resize', resize);
  resize();

  // ---- kreslení: tvar jako dřív (vzdálenostní pole koulí s měkkým spojením), převedený na rastr teček ----
  // uvnitř tvaru jsou tečky tak velké, že splynou v plochu; v pásu kolem tvaru se zmenšují a blednou do šedé
  // tečky pozadí – tečky se tedy „slévají“ do koule, místo aby se rozpadaly.
  const scr = new Float32Array(N * 3);
  const mix = (a, b, t) => a + (b - a) * t;
  const smin = (a, b, k) => { const h = Math.max(k - Math.abs(a - b), 0) / k; return Math.min(a, b) - h * h * k * 0.25; };
  const draw = () => {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    const core = toScreen(B[CORE]);
    const BAND = Math.max(44, core[2] * 0.42), K = Math.max(34, core[2] * 0.4); // šířka pásu teček a měkkost spojení (px)
    let n = 0, x0 = W, y0 = H, x1 = 0, y1 = 0;
    for (let i = 0; i < N; i++) {
      const s = toScreen(B[i]);
      if (s[2] <= 0.5) continue;
      scr[n * 3] = s[0]; scr[n * 3 + 1] = s[1]; scr[n * 3 + 2] = s[2]; n++;
      const reach = s[2] + BAND + K;
      x0 = Math.min(x0, s[0] - reach); y0 = Math.min(y0, s[1] - reach); x1 = Math.max(x1, s[0] + reach); y1 = Math.max(y1, s[1] + reach);
    }
    if (!n) return;
    const c0 = Math.max(0, Math.floor((x0 - ox) / GRID)), c1 = Math.min(Math.ceil((W - ox) / GRID), Math.ceil((x1 - ox) / GRID));
    const r0 = Math.max(0, Math.floor((y0 - oy) / GRID)), r1 = Math.min(Math.ceil((H - oy) / GRID), Math.ceil((y1 - oy) / GRID));
    const RMAX = GRID * 0.74; // > GRID/√2 → plné pokrytí uvnitř tvaru
    const STEPS = 10, paths = Array.from({ length: STEPS + 1 }, () => []);
    for (let r = r0; r <= r1; r++) {
      const py = oy + r * GRID;
      for (let c = c0; c <= c1; c++) {
        const px = ox + c * GRID;
        let d = 1e9;
        for (let k = 0; k < n; k++) d = smin(d, Math.hypot(px - scr[k * 3], py - scr[k * 3 + 1]) - scr[k * 3 + 2], K);
        if (d >= BAND) continue;
        const t = d <= 0 ? 1 : 1 - d / BAND, e = t * t * (3 - 2 * t);   // 1 uvnitř, 0 na kraji pásu
        const rad = d <= 0 ? RMAX : mix(1.2, RMAX * 0.95, e * e);
        const bin = Math.round(Math.min(1, e * 1.6) * STEPS);            // barva: šedá → limetková
        paths[bin].push(px, py, rad);
      }
    }
    for (let bI = 0; bI <= STEPS; bI++) {
      const arr = paths[bI]; if (!arr.length) continue;
      const t = bI / STEPS;
      ctx.fillStyle = `rgb(${Math.round(mix(GREY[0], LIME[0], t))},${Math.round(mix(GREY[1], LIME[1], t))},${Math.round(mix(GREY[2], LIME[2], t))})`;
      ctx.beginPath();
      for (let j = 0; j < arr.length; j += 3) { ctx.moveTo(arr[j] + arr[j + 2], arr[j + 1]); ctx.arc(arr[j], arr[j + 1], arr[j + 2], 0, 6.2832); }
      ctx.fill();
    }
  };
  window.__heroDots = { B, toScreen, CORE }; // pro testy

  let visible = true;
  if (window.IntersectionObserver) new IntersectionObserver((en) => { visible = en[0].isIntersecting; }).observe(stage);

  render();
  let seeded = false, time = 0, last = performance.now();
  const loop = (now) => {
    requestAnimationFrame(loop);
    const raw = (now - last) / 1000; last = now;
    if (stage.clientWidth !== W || stage.clientHeight !== H) resize();
    if (!visible || document.hidden || !W || !H) return;
    const dt = Math.max(0, Math.min(0.033, raw));
    if (!reduced) time += dt;
    if (!seeded) { targets(0); B.forEach((b) => { b.x = b.tx; b.y = b.ty; b.z = b.tz; b.r = b.tr; }); seeded = true; }
    targets(time); step(dt / 2); step(dt / 2);
    for (let i = 0; i < N; i++) {
      const b = B[i];
      if (![b.x, b.y, b.z, b.r, b.vx, b.vy, b.vz].every(Number.isFinite)) { b.x = b.tx; b.y = b.ty; b.z = b.tz; b.r = b.tr; b.vx = b.vy = b.vz = 0; }
      b.z = Math.max(-1, Math.min(1, b.z)); b.r = Math.max(-0.8, Math.min(1.4 * scale, b.r));
    }
    draw();
    for (let j = 0; j < 6; j++) if (det[j]) { const s = toScreen(B[j]); lab[j].style.transform = `translate(${Math.round(s[0])}px,${Math.round(s[1] + s[2] + 8)}px) translateX(-50%)`; }
  };
  requestAnimationFrame(loop);
})();
