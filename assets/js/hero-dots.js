// Úvod – tečky pozadí (mřížka 22 px) v pravém horním rohu pravidelně rostou (halftone od velkých v rohu
// k nejmenším = tečkám pozadí). Při najetí myší tečky pod kurzorem vtečou do jedné pravidelné kuličky, která
// okolní tečky odtlačuje. Z rohu jde vytáhnout 6 kuliček – každá = jeden bod z [data-hero-points]; každá ubere
// kousek z rohu, část ale zůstane vždy. 2D plátno (lehké, běží hned). Varianta C (šedé, limetková jen vybraná
// kulička); pro porovnání ?uvod=a (vše šedé) / ?uvod=b (limetkové kuličky).
(() => {
  const mode = (location.search.match(/[?&]uvod=([abc])\b/) || [])[1] || 'c'; // C = šedé, limetková jen vybraná kulička
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
  const GRID = 22;                                   // stejná mřížka jako tečky pozadí (.air-dots)
  const DOT = [185, 188, 191], BALL = [150, 156, 160], LIME = [205, 254, 0];
  const RMIN = 1.25, RMAX = GRID * 0.36;            // nejmenší = tečka pozadí, největší v rohu
  const mix = (a, b, t) => a + (b - a) * t;
  const sstep = (t) => (t <= 0 ? 0 : t >= 1 ? 1 : t * t * (3 - 2 * t));
  const rgb = (c) => `rgb(${Math.round(c[0])},${Math.round(c[1])},${Math.round(c[2])})`;
  const blend = (a, b, t) => [mix(a[0], b[0], t), mix(a[1], b[1], t), mix(a[2], b[2], t)];

  let W = 1, H = 1, dpr = 1, ox = 0, oy = 0, Rc = 500, Rc0 = 500, rb = 15, snapL = 200;
  const ptr = { x: -1e4, y: -1e4, in: false };
  const hov = { x: -1e4, y: -1e4, a: 0 };            // stažení sítě pod kurzorem (vyhlazené)
  // kuličky: st 0 = v rohu (schovaná), 1 = táhne se, 2 = volná; g = jak moc je vidět (0–1)
  const D = PARTS.map((p, i) => ({ i, st: 0, x: 0, y: 0, vx: 0, vy: 0, fx: 0, fy: 0, g: 0, lime: 0 }));
  const lab = PARTS.map((p) => { const l = document.createElement('span'); l.textContent = p.tag; labels.appendChild(l); return l; });
  let sel = -1, drag = null, slice = null, torn = false, picked = false, tease = 0, time = 0;

  // místo kuličky v rohu (úhel od rohu: 0 = podél horní hrany, 1 = podél pravé hrany)
  const AN = [0.10, 0.27, 0.44, 0.60, 0.76, 0.92];
  const at = (i, k) => { const t = (0.06 + AN[i] * 0.88) * Math.PI / 2; return [W - Rc * k * Math.cos(t), Rc * k * Math.sin(t)]; };
  const home = (i) => at(i, 0.42);                   // odkud se kulička vytahuje
  const narrow = () => W < 760;
  const SPOTS = [[0.50, 0.14], [0.56, 0.42], [0.66, 0.70], [0.42, 0.62], [0.80, 0.88], [0.92, 0.58]];
  const SPOTS_N = [[0.12, 0.06], [0.34, 0.18], [0.86, 0.36], [0.56, 0.30], [0.92, 0.12], [0.70, 0.08]];

  const render = () => {
    const n = D.filter((d) => d.st === 2).length;
    if (n > 0) torn = true;
    hintEl.textContent = n < 6 ? `Vytaženo ${n} z 6. Klikněte na tečky pro další.` : 'Vytaženo všech 6. Klikněte na kuličku.';
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

  const clampFree = (x, y) => [Math.max(rb * 2, Math.min(W - rb * 2, x)), Math.max(rb * 2, Math.min(H - rb * 2, y))];
  const spread = (keep) => {
    const minD = rb * 5;
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

  // pravidelný halftone: velikost tečky plynule klesá se vzdáleností od rohu
  const baseV = (x, y) => Math.max(0, 1 - Math.hypot(W - x, y) / Rc);

  const step = (dt) => {
    for (const d of D) {
      let tx, ty, gt;
      if (d.st === 1) { tx = ptr.x; ty = ptr.y; gt = 1; }
      else if (d.st === 2) { tx = d.fx; ty = d.fy + (reduced ? 0 : Math.sin(time * 0.8 + d.i * 1.7) * 3); gt = 1; }
      else {
        // v rohu schovaná; „Design“ se co chvíli sama vystrčí a zase vrátí
        const peek = PARTS[d.i].accent ? tease : 0, a = at(d.i, 0.42 + peek * 0.36);
        tx = a[0]; ty = a[1]; gt = peek;
      }
      const fast = d.st === 1, k = fast ? 170 : 42, damp = fast ? 22 : 8;
      d.vx += ((tx - d.x) * k - d.vx * damp) * dt; d.vy += ((ty - d.y) * k - d.vy * damp) * dt;
      d.x += d.vx * dt; d.y += d.vy * dt;
      if (!Number.isFinite(d.x + d.y)) { d.x = tx; d.y = ty; d.vx = d.vy = 0; }
      d.g += (gt - d.g) * (1 - Math.exp(-dt * 8));
      const lt = mode === 'b' ? 1 : mode === 'c' ? (sel === d.i ? 1 : 0) : 0;
      d.lime += (lt - d.lime) * (1 - Math.exp(-dt * 7));
    }
    const over = ptr.in && !drag && baseV(ptr.x, ptr.y) > 0.03;
    const kf = 1 - Math.exp(-dt * 9);
    hov.x += (ptr.x - hov.x) * kf; hov.y += (ptr.y - hov.y) * kf;
    hov.a += ((over ? 1 : 0) - hov.a) * (1 - Math.exp(-dt * (over ? 4 : 3)));
  };

  const pick = (px, py) => {
    let best = -1, bd = 1e9;
    for (const d of D) if (d.st === 2 || d.g > 0.3) {
      const dd = Math.hypot(px - d.x, py - d.y);
      if (dd < rb * 1.8 && dd < bd) { bd = dd; best = d.i; }
    }
    if (best < 0 && baseV(px, py) > 0.12) { // chycení kdekoli v tečkách: nejbližší kulička, která je ještě v rohu
      for (const d of D) if (d.st === 0) { const h = home(d.i), dd = Math.hypot(px - h[0], py - h[1]); if (dd < bd) { bd = dd; best = d.i; } }
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
    const d = D[i];
    if (d.st === 0) { d.x = p[0]; d.y = p[1]; d.vx = d.vy = 0; } // kulička se tvoří tam, kde ji chytil
    drag = { i, sx: p[0], sy: p[1], moved: false, was: d.st, hx: p[0], hy: p[1] };
  });
  canvas.addEventListener('pointermove', (e) => {
    const p = local(e); ptr.x = p[0]; ptr.y = p[1]; ptr.in = true;
    if (drag) {
      const d = D[drag.i];
      if (!drag.moved && Math.hypot(p[0] - drag.sx, p[1] - drag.sy) > 6) { drag.moved = true; d.st = 1; canvas.classList.add('is-drag'); delete canvas.dataset.cursor; }
      if (drag.moved && drag.was === 0 && Math.hypot(p[0] - drag.hx, p[1] - drag.hy) > snapL) { drag.was = 2; sel = drag.i; torn = true; render(); }
      return;
    }
    if (slice) {
      // řez: tah přes halftone uvolní kuličky, jejichž místo v rohu přeťal
      let hit = false;
      for (const d of D) if (d.st === 0) {
        const h = home(d.i), o = at(d.i, 0.9);
        if (crosses(slice.x, slice.y, p[0], p[1], h[0], h[1], o[0], o[1])) {
          d.st = 2; d.x = h[0]; d.y = h[1]; [d.fx, d.fy] = clampFree(o[0] + (o[0] - h[0]) * 0.3, o[1] + (o[1] - h[1]) * 0.3); hit = true;
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
    if (g.was === 0) { d.st = 0; return; }                              // neutrhla se – vteče zpátky do teček
    // kulička puštěná zpátky do teček se s nimi slije
    if (baseV(p[0], p[1]) > 0.3) { d.st = 0; if (sel === g.i) sel = -1; }
    else { d.st = 2; [d.fx, d.fy] = clampFree(p[0], p[1]); spread(g.i); sel = g.i; }
    render();
  });
  canvas.addEventListener('pointercancel', () => { if (drag) { const d = D[drag.i]; d.st = drag.was === 0 ? 0 : 2; } drag = null; slice = null; canvas.classList.remove('is-drag'); });

  const resize = () => {
    W = stage.clientWidth; H = stage.clientHeight;
    if (!W || !H) return;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.max(2, Math.round(W * dpr)); canvas.height = Math.max(2, Math.round(H * dpr));
    // tečky sedí přesně na mřížce pozadí
    const cr = canvas.getBoundingClientRect(), br = (dotsBg || stage).getBoundingClientRect();
    ox = ((br.left - cr.left + GRID / 2) % GRID + GRID) % GRID; oy = ((br.top - cr.top + GRID / 2) % GRID + GRID) % GRID;
    Rc0 = narrow() ? Math.min(W * 0.85, 340) : Math.min(Math.max(W * 0.45, 460), 720);
    if (!Rc || Rc === 500) Rc = Rc0;
    rb = narrow() ? 12 : 15; snapL = narrow() ? 110 : 170;
    D.forEach((d) => { if (d.st === 2) [d.fx, d.fy] = clampFree(d.fx, d.fy); });
    spread(-1);
  };
  if (window.ResizeObserver) new ResizeObserver(resize).observe(stage); else window.addEventListener('resize', resize);
  resize();

  // ---- kreslení ----
  const draw = () => {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    const HR = narrow() ? 40 : 50;                       // dosah, odkud tečky vtékají do kuličky
    const BR = narrow() ? 12 : 15;                       // velikost kuličky
    // uzly: kurzor (najetí) a kuličky, které se tvoří / táhnou z rohu – tečky do nich vtečou;
    // každá kulička (i volná) pak okolní tečky odtlačuje
    const sinks = [];
    if (hov.a > 0.01) sinks.push({ x: hov.x, y: hov.y, a: hov.a, r: HR, ball: -1, eat: true });
    for (const d of D) {
      if (d.st === 1 && drag && drag.was === 0) sinks.push({ x: drag.hx, y: drag.hy, a: 1, r: HR * 0.9, ball: d.i, eat: true });
      else if (d.st === 0 && d.g > 0.02) { const h = home(d.i); sinks.push({ x: h[0], y: h[1], a: d.g, r: HR * 0.8, ball: d.i, eat: true }); }
      if (d.st || d.g > 0.02) sinks.push({ x: d.x, y: d.y, a: d.st ? 1 : d.g, r: 0, ball: d.i, eat: false });
    }

    const c0 = Math.max(0, Math.floor((W - Rc - ox) / GRID)), c1 = Math.ceil((W - ox) / GRID);
    const r1 = Math.min(Math.ceil((H - oy) / GRID), Math.ceil((Rc - oy) / GRID));
    const absorbed = sinks.map(() => 0);
    ctx.fillStyle = rgb(DOT); ctx.beginPath();
    for (let r = 0; r <= r1; r++) {
      const py = oy + r * GRID;
      for (let c = c0; c <= c1; c++) {
        const px = ox + c * GRID, v = baseV(px, py);
        if (v <= 0) continue;
        let rad = mix(RMIN, RMAX, v), qx = px, qy = py;
        for (let s = 0; s < sinks.length; s++) {
          const S = sinks[s], dx = px - S.x, dy = py - S.y, dd = Math.hypot(dx, dy) || 0.001;
          // nejbližší tečky vtečou do kuličky (stáhnou se do středu a zmizí)
          if (S.eat && dd < S.r) {
            const h = S.a * sstep(1 - dd / S.r);
            absorbed[s] += rad * rad * h; qx -= dx * h; qy -= dy * h; rad *= 1 - h;
            continue;
          }
          // kulička odtlačuje okolní tečky: odsune je ven, ať je kolem ní volné místo
          const ring = (S.eat ? S.r : BR + GRID * 0.6), reach = ring + GRID * 2.2;
          if (dd < reach) {
            const k = S.a * (1 - Math.max(0, dd - BR) / (reach - BR)) ** 2;
            const push = k * GRID * 0.75;
            qx += dx / dd * push; qy += dy / dd * push; rad *= 1 - 0.25 * k;
          }
        }
        if (rad < 0.4) continue;
        ctx.moveTo(qx + rad, qy); ctx.arc(qx, qy, rad, 0, 6.2832);
      }
    }
    ctx.fill();

    const ball = (x, y, r, lime) => { ctx.fillStyle = rgb(blend(BALL, LIME, lime)); ctx.beginPath(); ctx.arc(x, y, r, 0, 6.2832); ctx.fill(); };
    // kulička pod kurzorem: pravidelná, roste podle toho, kolik teček do ní vteklo
    sinks.forEach((S, s) => {
      if (S.ball >= 0 || !S.eat) return;
      const r = Math.min(BR, Math.sqrt(absorbed[s]) * 0.85);
      if (r > 1) ball(S.x, S.y, r, mode === 'b' ? 1 : 0);
    });
    // krček: řetízek kuliček od místa, kde ji chytil, ke kuličce – čím dál, tím tenčí
    if (drag && drag.was === 0 && drag.moved) {
      const d = D[drag.i], L = Math.hypot(d.x - drag.hx, d.y - drag.hy), pull = Math.min(1, L / snapL);
      const n = Math.max(2, Math.ceil(L / 7)), r0 = rb * 0.7 * (1 - pull * 0.75);
      ctx.fillStyle = rgb(blend(BALL, LIME, d.lime)); ctx.beginPath();
      for (let k = 0; k <= n; k++) {
        const t = k / n, rr = r0 * (1 - 0.55 * Math.sin(t * Math.PI));
        if (rr < 0.6) continue;
        const x = mix(drag.hx, d.x, t), y = mix(drag.hy, d.y, t);
        ctx.moveTo(x + rr, y); ctx.arc(x, y, rr, 0, 6.2832);
      }
      ctx.fill();
    }
    for (const d of D) {
      const g = d.st ? 1 : d.g;
      if (g < 0.02) continue;
      ball(d.x, d.y, rb * (sel === d.i ? 1.15 : 1) * g, d.lime);
    }
  };
  window.__heroDots = { D, home, at }; // pro testy

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
    if (!seeded) { D.forEach((d) => { const h = home(d.i); d.x = h[0]; d.y = h[1]; }); seeded = true; }
    const ph = (time - 1.5) % 4.2;
    tease = !torn && !drag && !reduced && ph >= 0 && ph < 1.4 ? Math.sin(ph / 1.4 * Math.PI) ** 2 : 0;
    // každá vytažená kulička ubere kousek z rohu; část v rohu ale zůstane vždycky (~64 %)
    const out = D.filter((d) => d.st === 2 || (d.st === 1 && drag && drag.was === 2)).length;
    Rc += (Rc0 * (1 - 0.06 * out) - Rc) * (1 - Math.exp(-dt * 4));
    step(dt / 2); step(dt / 2);
    draw();
    for (const d of D) if (d.st === 2) lab[d.i].style.transform = `translate(${Math.round(d.x)}px,${Math.round(d.y + rb * 1.3 + 6)}px) translateX(-50%)`;
  };
  requestAnimationFrame(loop);
})();
