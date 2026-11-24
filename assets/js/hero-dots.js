// Úvod – halftone z teček přilepený k pravému hornímu rohu (stejný styl jako kapky-lime.svg, ale šedý).
// Při najetí myší se tečky stékají do sebe, kapky (shluky na okraji) jdou vytáhnout – každá = jeden bod
// z [data-hero-points], dokud nejsou venku všechny. Kreslí se 2D plátnem (lehké, běží hned).
// Zatím jen náhled: ?uvod=a | b | c (barevné varianty, viz /navrhy-uvod/). hero-blob.js se pak vypne.
(() => {
  const mode = (location.search.match(/[?&]uvod=([abc])\b/) || [])[1];
  if (!mode) return;
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
    tag: li.dataset.tag, accent: li.hasAttribute('data-accent'),
    head: li.querySelector('strong').textContent, text: li.querySelector('span').textContent,
  }));
  if (PARTS.length !== 6) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  stage.classList.add('has-gl', 'has-dots');

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const GRID = 11;                                   // rozteč jako v kapky-lime.svg; každá druhá tečka sedí na rastr pozadí (22 px)
  const GREY = [176, 181, 185], LIME = [205, 254, 0];
  const RIDLE = GRID * 0.4, RMERGE = GRID * 0.76;    // v klidu se tečky nedotýkají, slité splynou v plochu
  const mix = (a, b, t) => a + (b - a) * t;
  const sstep = (t) => (t <= 0 ? 0 : t >= 1 ? 1 : t * t * (3 - 2 * t));

  let W = 1, H = 1, dpr = 1, ox = 0, oy = 0, Rc = 400, rd = 26, snapL = 150;
  const ptr = { x: -1e4, y: -1e4, in: false };
  const hov = { x: -1e4, y: -1e4, a: 0 };            // stékání pod kurzorem (vyhlazené)
  // kapky: stav 0 = na okraji, 1 = táhne se, 2 = volná
  const D = PARTS.map((p, i) => ({ i, st: 0, x: 0, y: 0, vx: 0, vy: 0, fx: 0, fy: 0, m: 0, lime: 0 }));
  const lab = PARTS.map((p) => { const l = document.createElement('span'); l.textContent = p.tag; labels.appendChild(l); return l; });
  let sel = -1, drag = null, slice = null, torn = false, picked = false, tease = 0, time = 0;

  // kotva kapky na okraji halftonu (úhel od rohu: 0 = podél horní hrany, 1 = podél pravé hrany)
  const AN = [0.10, 0.27, 0.44, 0.60, 0.76, 0.92];
  const anchor = (i, k = 0.86) => { const t = (0.06 + AN[i] * 0.88) * Math.PI / 2; return [W - Rc * k * Math.cos(t), Rc * k * Math.sin(t)]; };
  const root = (i) => anchor(i, 0.62);
  const narrow = () => W < 760;
  // kam kapka odpluje po kliknutí (podíl šířky a výšky panelu)
  const SPOTS = [[0.50, 0.14], [0.56, 0.42], [0.66, 0.70], [0.42, 0.62], [0.80, 0.88], [0.92, 0.58]];
  const SPOTS_N = [[0.12, 0.06], [0.34, 0.18], [0.86, 0.36], [0.56, 0.30], [0.92, 0.12], [0.70, 0.08]];

  const render = () => {
    const n = D.filter((d) => d.st === 2).length;
    if (n > 0) torn = true;
    hintEl.textContent = n < 6 ? `Vytaženo ${n} z 6. Klikněte na tečky pro další.` : 'Vytaženo všech 6. Klikněte na kapku.';
    hintRow.hidden = n === 0; resetBtn.hidden = n === 0;
    if (sel >= 0) {
      const p = PARTS[sel];
      msg.querySelector('.hero-msg-tag').textContent = p.tag;
      msg.querySelector('.hero-msg-title').textContent = p.head;
      msg.querySelector('.hero-msg-text').textContent = p.text;
      msg.hidden = true; void msg.offsetWidth; msg.hidden = false;
    } else msg.hidden = true;
    lab.forEach((l, i) => l.classList.toggle('is-on', D[i].st === 2));
  };
  resetBtn.addEventListener('click', () => { D.forEach((d) => { d.st = 0; }); sel = -1; render(); });

  const clampFree = (x, y) => [Math.max(rd * 1.4, Math.min(W - rd * 1.4, x)), Math.max(rd * 1.4, Math.min(H - rd * 1.4, y))];
  const spread = (keep) => {
    const minD = rd * 3.2;
    for (let it = 0; it < 6; it++) for (let a = 0; a < 6; a++) for (let b = a + 1; b < 6; b++) {
      const A = D[a], B = D[b];
      if (A.st !== 2 || B.st !== 2) continue;
      let dx = B.fx - A.fx, dy = B.fy - A.fy, d = Math.hypot(dx, dy);
      if (d >= minD) continue;
      if (d < 1e-3) { dx = Math.cos(b * 2.4); dy = Math.sin(b * 2.4); d = 1; }
      const push = minD - d, ux = dx / d, uy = dy / d, wa = a === keep ? 0 : b === keep ? 1 : 0.5, wb = 1 - wa;
      [A.fx, A.fy] = clampFree(A.fx - ux * push * wa, A.fy - uy * push * wa);
      [B.fx, B.fy] = clampFree(B.fx + ux * push * wb, B.fy + uy * push * wb);
    }
  };
  const release = (i) => {
    const s = (narrow() ? SPOTS_N : SPOTS)[i], d = D[i];
    d.st = 2; [d.fx, d.fy] = clampFree(s[0] * W, s[1] * H); spread(i); sel = i; render();
  };

  // ---- pole: halftone rohu + kapky + krček při tahu + stékání pod kurzorem ----
  const baseV = (x, y) => {
    const n = 0.13 * Math.sin(x * 0.012 + 1.3) * Math.sin(y * 0.016 + 0.4) + 0.08 * Math.sin((x + y) * 0.029) + 0.05 * Math.sin(x * 0.047 - y * 0.021);
    const dc = Math.hypot(W - x, y) / Rc + n;            // 0 v rohu, ~1 na okraji
    return 1 - sstep((dc - 0.25) / 0.78);
  };
  const segD = (px, py, ax, ay, bx, by) => {
    const vx = bx - ax, vy = by - ay, l2 = vx * vx + vy * vy || 1, t = Math.max(0, Math.min(1, ((px - ax) * vx + (py - ay) * vy) / l2));
    return [Math.hypot(px - ax - vx * t, py - ay - vy * t), t];
  };

  const step = (dt) => {
    for (const d of D) {
      let tx, ty;
      if (d.st === 1) { tx = ptr.x; ty = ptr.y; }
      else if (d.st === 2) { tx = d.fx; ty = d.fy + (reduced ? 0 : Math.sin(time * 0.8 + d.i * 1.7) * 3); }
      else {
        const a = anchor(d.i, 0.86 + (PARTS[d.i].accent ? tease * 0.22 : 0) + (reduced ? 0 : Math.sin(time * 0.6 + d.i * 1.9) * 0.012));
        tx = a[0]; ty = a[1];
      }
      const fast = d.st === 1, k = fast ? 160 : 40, damp = fast ? 22 : 7.5;
      d.vx += ((tx - d.x) * k - d.vx * damp) * dt; d.vy += ((ty - d.y) * k - d.vy * damp) * dt;
      d.x += d.vx * dt; d.y += d.vy * dt;
      if (!Number.isFinite(d.x + d.y)) { d.x = tx; d.y = ty; d.vx = d.vy = 0; }
      // m: jak moc je kapka slitá (0 = shluk teček na okraji, 1 = plná kapka)
      const mt = d.st === 0 ? (PARTS[d.i].accent ? tease * 0.8 : 0) : 1;
      d.m += (mt - d.m) * (1 - Math.exp(-dt * 9));
      const lt = mode === 'b' ? (d.st ? 1 : (PARTS[d.i].accent ? tease : 0)) : mode === 'c' ? (sel === d.i ? 1 : 0) : 0;
      d.lime += (lt - d.lime) * (1 - Math.exp(-dt * 7));
    }
    const over = ptr.in && !drag;
    hov.x += (ptr.x - hov.x) * (1 - Math.exp(-dt * 10)); hov.y += (ptr.y - hov.y) * (1 - Math.exp(-dt * 10));
    hov.a += ((over ? 1 : 0) - hov.a) * (1 - Math.exp(-dt * (over ? 5 : 3)));
  };

  const pick = (px, py) => {
    let best = -1, bd = 1e9;
    for (const d of D) {
      const r = d.st === 2 ? rd * 1.5 : rd * 1.9, dd = Math.hypot(px - d.x, py - d.y);
      if (dd < r && dd < bd) { bd = dd; best = d.i; }
    }
    if (best < 0 && baseV(px, py) > 0.35) { // klik kamkoli do teček: nejbližší kapka, která je ještě na okraji
      for (const d of D) if (d.st === 0) { const dd = Math.hypot(px - d.x, py - d.y); if (dd < bd) { bd = dd; best = d.i; } }
    }
    return best;
  };
  const crosses = (ax, ay, bx, by, cx, cy, dx, dy) => {
    const o = (px, py, qx, qy, rx, ry) => (qx - px) * (ry - py) - (qy - py) * (rx - px);
    return o(ax, ay, bx, by, cx, cy) * o(ax, ay, bx, by, dx, dy) < 0 && o(cx, cy, dx, dy, ax, ay) * o(cx, cy, dx, dy, bx, by) < 0;
  };
  const local = (e) => { const r = canvas.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };

  canvas.addEventListener('pointerdown', (e) => {
    const p = local(e); ptr.x = p[0]; ptr.y = p[1]; ptr.in = true;
    const i = pick(p[0], p[1]);
    try { canvas.setPointerCapture(e.pointerId); } catch (err) { /* nevadí */ }
    if (i < 0) { drag = null; slice = { x: p[0], y: p[1] }; return; }
    drag = { i, sx: p[0], sy: p[1], moved: false, was: D[i].st };
  });
  canvas.addEventListener('pointermove', (e) => {
    const p = local(e); ptr.x = p[0]; ptr.y = p[1]; ptr.in = true;
    if (drag) {
      const d = D[drag.i];
      if (!drag.moved && Math.hypot(p[0] - drag.sx, p[1] - drag.sy) > 6) { drag.moved = true; d.st = 1; canvas.classList.add('is-drag'); delete canvas.dataset.cursor; }
      if (drag.moved && drag.was === 0) { const r = root(drag.i); if (Math.hypot(p[0] - r[0], p[1] - r[1]) > snapL) { drag.was = 2; sel = drag.i; torn = true; render(); } }
      return;
    }
    if (slice) {
      let hit = false;
      for (const d of D) if (d.st === 0) {
        const r = root(d.i);
        if (crosses(slice.x, slice.y, p[0], p[1], r[0], r[1], d.x, d.y)) {
          const ux = d.x - r[0], uy = d.y - r[1], l = Math.hypot(ux, uy) || 1;
          d.st = 2; [d.fx, d.fy] = clampFree(d.x + ux / l * rd * 3, d.y + uy / l * rd * 3); d.vx += ux / l * 260; d.vy += uy / l * 260; hit = true;
        }
      }
      slice.x = p[0]; slice.y = p[1];
      if (hit) { spread(-1); render(); }
      return;
    }
    const over = pick(p[0], p[1]);
    canvas.classList.toggle('is-hit', over >= 0);
    const tip = over < 0 ? '' : D[over].st === 2 ? (picked ? '' : 'Vybrat') : (torn ? '' : 'Vytáhni');
    if (tip) canvas.dataset.cursor = tip; else delete canvas.dataset.cursor;
  });
  canvas.addEventListener('pointerleave', () => { if (!drag) ptr.in = false; });
  canvas.addEventListener('pointerup', (e) => {
    slice = null;
    if (e.pointerType !== 'mouse') ptr.in = false;
    if (!drag) { if (sel >= 0) { sel = -1; render(); } return; }
    const g = drag, d = D[g.i], p = local(e);
    drag = null; canvas.classList.remove('is-drag');
    if (!g.moved) { delete canvas.dataset.cursor; if (d.st === 2) { sel = g.i; picked = true; render(); } else release(g.i); return; }
    if (g.was === 0) { d.st = 0; return; }                              // neutrhla se – vrátí se na okraj
    // kapka puštěná zpátky do teček se s nimi slije
    if (baseV(p[0], p[1]) > 0.45) { d.st = 0; if (sel === g.i) sel = -1; }
    else { d.st = 2; [d.fx, d.fy] = clampFree(p[0], p[1]); spread(g.i); sel = g.i; }
    render();
  });
  canvas.addEventListener('pointercancel', () => { if (drag) { const d = D[drag.i]; d.st = drag.was === 0 ? 0 : 2; } drag = null; slice = null; canvas.classList.remove('is-drag'); });

  const resize = () => {
    W = stage.clientWidth; H = stage.clientHeight;
    if (!W || !H) return;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.max(2, Math.round(W * dpr)); canvas.height = Math.max(2, Math.round(H * dpr));
    const cr = canvas.getBoundingClientRect(), br = (dotsBg || stage).getBoundingClientRect();
    ox = ((br.left - cr.left) % GRID + GRID) % GRID; oy = ((br.top - cr.top) % GRID + GRID) % GRID;
    Rc = narrow() ? Math.min(W * 0.72, 300) : Math.min(Math.max(W * 0.36, 380), 600);
    rd = narrow() ? 20 : 27; snapL = Rc * 0.55;
    D.forEach((d) => { if (d.st === 2) [d.fx, d.fy] = clampFree(d.fx, d.fy); });
    spread(-1);
  };
  if (window.ResizeObserver) new ResizeObserver(resize).observe(stage); else window.addEventListener('resize', resize);
  resize();

  // ---- kreslení ----
  const STEPS = 8;
  const draw = () => {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    const HR = narrow() ? 60 : 80;                       // poloměr stékání pod kurzorem
    // oblast, kde vůbec můžou být tečky: roh + volné kapky
    let x0 = W - Rc * 1.35, y1 = Rc * 1.35;
    for (const d of D) if (d.st) { x0 = Math.min(x0, d.x - rd * 3); y1 = Math.max(y1, d.y + rd * 3); }
    const c0 = Math.max(0, Math.floor((x0 - ox) / GRID)), c1 = Math.ceil((W - ox) / GRID);
    const r0 = 0, r1 = Math.min(Math.ceil((H - oy) / GRID), Math.ceil((y1 - oy) / GRID));
    const paths = Array.from({ length: STEPS + 1 }, () => []);
    const drag1 = drag && drag.was === 0 ? D[drag.i] : null;
    const rt = drag1 ? root(drag1.i) : null, L = drag1 ? Math.hypot(drag1.x - rt[0], drag1.y - rt[1]) : 0;
    for (let r = r0; r <= r1; r++) {
      const py = oy + r * GRID;
      for (let c = c0; c <= c1; c++) {
        const px = ox + c * GRID;
        let v = baseV(px, py), merge = 0, lime = 0;
        for (const d of D) {
          const dd = Math.hypot(px - d.x, py - d.y), b = sstep(1 - dd / (rd * 1.9));
          if (b <= 0) continue;
          // na okraji: shluk větších teček (jako v kapky-lime.svg); vytažená: uprostřed slitá, na kraji halftone
          v = Math.max(v, (d.st ? 0.5 : 0.55) + (d.st ? 0.5 : 0.45) * b);
          merge = Math.max(merge, d.m * sstep(1 - dd / (d.st ? rd : rd * 1.15)));
          lime = Math.max(lime, d.lime * b);
        }
        if (drag1 && drag1.st === 1) {
          // krček mezi okrajem a taženou kapkou – čím dál, tím tenčí
          const [ds, t] = segD(px, py, rt[0], rt[1], drag1.x, drag1.y), w = rd * 0.75 * Math.max(0.25, 1 - L / snapL) * (1 - 0.35 * Math.sin(t * Math.PI));
          if (ds < w * 1.8) { const b = sstep(1 - ds / (w * 1.8)); v = Math.max(v, 0.5 + 0.5 * b); merge = Math.max(merge, sstep(1 - ds / w)); lime = Math.max(lime, drag1.lime * b); }
        }
        if (v < 0.03) continue;
        // stékání: tečky pod kurzorem se zvětší a stáhnou ke kurzoru
        let qx = px, qy = py;
        if (hov.a > 0.01 && v > 0.08) {
          const dh = Math.hypot(px - hov.x, py - hov.y), h = hov.a * Math.exp(-(dh * dh) / (HR * HR)) * sstep(v * 1.6);
          if (h > 0.01) { merge = Math.max(merge, h); qx += (hov.x - px) * 0.22 * h; qy += (hov.y - py) * 0.22 * h; if (mode === 'b') lime = Math.max(lime, h); }
        }
        const rad = mix(mix(0.85, RIDLE, sstep(v)), RMERGE, sstep(merge));
        if (rad < 0.6) continue;
        paths[Math.round(Math.min(1, lime) * STEPS)].push(qx, qy, rad);
      }
    }
    for (let b = 0; b <= STEPS; b++) {
      const arr = paths[b]; if (!arr.length) continue;
      const t = b / STEPS;
      ctx.fillStyle = `rgb(${Math.round(mix(GREY[0], LIME[0], t))},${Math.round(mix(GREY[1], LIME[1], t))},${Math.round(mix(GREY[2], LIME[2], t))})`;
      ctx.beginPath();
      for (let j = 0; j < arr.length; j += 3) { ctx.moveTo(arr[j] + arr[j + 2], arr[j + 1]); ctx.arc(arr[j], arr[j + 1], arr[j + 2], 0, 6.2832); }
      ctx.fill();
    }
  };
  window.__heroDots = { D, anchor, root }; // pro testy

  let visible = true;
  if (window.IntersectionObserver) new IntersectionObserver((en) => { visible = en[0].isIntersecting; }).observe(stage);
  render();
  let seeded = false, last = performance.now();
  const loop = (now) => {
    requestAnimationFrame(loop);
    const raw = (now - last) / 1000; last = now;
    if (stage.clientWidth !== W || stage.clientHeight !== H) resize();
    if (!visible || document.hidden || !W || !H) return;
    const dt = Math.max(0, Math.min(0.033, raw));
    if (!reduced) time += dt;
    if (!seeded) { D.forEach((d) => { const a = anchor(d.i); d.x = a[0]; d.y = a[1]; }); seeded = true; }
    // dokud nikdo nic nevytáhl, kapka „Design“ se co chvíli sama vystrčí a vrátí
    const ph = (time - 1.5) % 4.2;
    tease = !torn && !drag && !reduced && ph >= 0 && ph < 1.3 ? Math.sin(ph / 1.3 * Math.PI) ** 2 : 0;
    step(dt / 2); step(dt / 2);
    draw();
    for (const d of D) if (d.st === 2) lab[d.i].style.transform = `translate(${Math.round(d.x)}px,${Math.round(d.y + rd * 1.5 + 6)}px) translateX(-50%)`;
  };
  requestAnimationFrame(loop);
})();
