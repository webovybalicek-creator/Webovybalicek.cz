// Úvod – perleťová hmota přilepená v rohu. Dá se z ní trhat (tah za hmotu) a řezat (tah přes hmotu).
// Každá odtržená kapka = jeden bod z [data-hero-points]. Bez WebGL zůstane statický úvod.
(() => {
  const stage = document.querySelector('[data-hero]');
  if (!stage) return;
  const canvas = stage.querySelector('.hero-canvas');
  const labels = stage.querySelector('.hero-labels');
  const title = stage.querySelector('.hero-title');
  const lead = stage.querySelector('[data-hero-lead]');
  const msg = stage.querySelector('[data-hero-msg]');
  const hintRow = stage.querySelector('.hero-hint');
  const hintEl = stage.querySelector('[data-hero-hint]');
  const resetBtn = stage.querySelector('[data-hero-reset]');
  const PARTS = [...stage.querySelectorAll('[data-hero-points] li')].slice(0, 6).map((li) => ({
    tag: li.dataset.tag,
    accent: li.hasAttribute('data-accent'),
    head: li.querySelector('strong').textContent,
    text: li.querySelector('span').textContent,
  }));
  if (PARTS.length !== 6) return;

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const narrowMq = window.matchMedia('(max-width: 960px)');

  let gl = null;
  try { gl = canvas.getContext('webgl', { alpha: true, premultipliedAlpha: true, antialias: false }); } catch (e) { /* bez WebGL */ }
  if (!gl) return;

  const VS = 'attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}';
  const FS = `
precision highp float;
uniform vec2 uRes;uniform float uTime;
uniform sampler2D uText;
uniform vec4 uB[8];uniform vec3 uC[8];
const float F=2.2;const float CAM=5.0;const float K=0.55;
float smin(float a,float b,float k){float h=max(k-abs(a-b),0.0)/k;return min(a,b)-h*h*k*0.25;}
float map(vec3 p){float d=1e5;
  for(int i=0;i<8;i++){d=smin(d,length(p-uB[i].xyz)-uB[i].w,K);}
  d+=0.03*sin(2.6*p.x+uTime*1.1)*sin(2.9*p.y-uTime*0.9)*sin(2.3*p.z+uTime*0.7);
  return d;}
vec3 tint(vec3 p){vec3 c=vec3(0.0);float ws=0.0;
  for(int i=0;i<8;i++){float d=max(length(p-uB[i].xyz)-uB[i].w,0.0);float w=exp(-6.0*d)+1e-5;c+=uC[i]*w;ws+=w;}
  return c/ws;}
vec3 pal(float t){return 0.5+0.5*cos(6.2832*(t+vec3(0.0,0.33,0.67)));}
vec3 tm(vec3 c){return pow(1.0-exp(-c*1.5),vec3(0.4545));}
void main(){
  vec2 fc=gl_FragCoord.xy;vec2 suv=fc/uRes;
  vec2 uv=(fc-0.5*uRes)/uRes.y*2.0;
  vec3 ro=vec3(0.0,0.0,CAM);vec3 rd=normalize(vec3(uv,-F));
  float t=2.4;float md=1e5;vec3 pm=ro;bool hit=false;vec3 p=ro;
  for(int i=0;i<64;i++){p=ro+rd*t;float d=map(p);if(d<md){md=d;pm=p;}if(d<0.003){hit=true;break;}t+=d*0.85;if(t>8.5)break;}
  float al=hit?1.0:clamp(1.0-md/0.016,0.0,1.0);if(!hit)p=pm;
  vec3 col=vec3(0.0);float a=0.0;
  if(al>0.0){
    vec2 e=vec2(0.003,-0.003);
    vec3 n=normalize(e.xyy*map(p+e.xyy)+e.yyx*map(p+e.yyx)+e.yxy*map(p+e.yxy)+e.xxx*map(p+e.xxx));
    float ndv=max(dot(n,-rd),0.0);float fr=pow(1.0-ndv,3.0);
    vec3 tc=tint(p);vec3 r=reflect(rd,n);vec3 L=normalize(vec3(-0.45,0.65,0.6));
    float ndl=max(dot(n,L),0.0);float sp=pow(max(dot(r,L),0.0),70.0);
    col=tc*(0.62+0.38*ndl)*(0.82+0.18*ndv);
    col=mix(col,pal(fr*1.3+n.y*0.3+uTime*0.03)*0.75+0.2,fr*0.6)+vec3(sp*0.7);
    col=tm(col);
    // nadpis je přes hmotu vidět ohnutý, na hranách rozložený do barev
    vec2 o=-n.xy*0.085*(1.25-ndv);o.x*=uRes.y/uRes.x;
    vec3 k=0.9*vec3(texture2D(uText,suv+o).a,texture2D(uText,suv+o*1.07).a,texture2D(uText,suv+o*1.14).a);
    col=col*(1.0-k)+vec3(0.039,0.071,0.09)*k;
    col*=al;a=al;
  }
  a+=exp(-max(md,0.0)*4.5)*(1.0-al)*0.2;
  gl_FragColor=vec4(col,min(a,1.0));}`;

  const sh = (type, src) => { const o = gl.createShader(type); gl.shaderSource(o, src); gl.compileShader(o); return gl.getShaderParameter(o, gl.COMPILE_STATUS) ? o : null; };
  const vs = sh(gl.VERTEX_SHADER, VS), fs = sh(gl.FRAGMENT_SHADER, FS);
  if (!vs || !fs) return;
  const prog = gl.createProgram(); gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
  gl.useProgram(prog);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const la = gl.getAttribLocation(prog, 'a'); gl.enableVertexAttribArray(la); gl.vertexAttribPointer(la, 2, gl.FLOAT, false, 0, 0);
  const U = { res: gl.getUniformLocation(prog, 'uRes'), time: gl.getUniformLocation(prog, 'uTime'), b: gl.getUniformLocation(prog, 'uB[0]'), c: gl.getUniformLocation(prog, 'uC[0]') };
  const tex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tex);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
  gl.uniform1i(gl.getUniformLocation(prog, 'uText'), 0);
  gl.clearColor(0, 0, 0, 0);

  let alive = true;
  canvas.addEventListener('webglcontextlost', (e) => { e.preventDefault(); alive = false; stage.classList.remove('has-gl'); hintRow.hidden = true; });
  stage.classList.add('has-gl');
  hintRow.hidden = false;

  // ---- stav ----
  const F = 2.2, CAM = 5, N = 8, CORE = 6, AUX = 7;
  const WHITE = [0.8, 0.8, 0.8], LIME = [0.66, 1.08, 0.0];
  const B = Array.from({ length: N }, () => ({ x: 0, y: 0, z: 0, vx: 0, vy: 0, vz: 0, r: 0.1, tx: 0, ty: 0, tz: 0, tr: 0.1 }));
  B[AUX].r = B[AUX].tr = -0.8;
  const bArr = new Float32Array(N * 4), cArr = new Float32Array(N * 3).fill(0.8);
  const lab = PARTS.map((p) => { const l = document.createElement('span'); l.textContent = p.tag; labels.appendChild(l); return l; });
  const det = [0, 0, 0, 0, 0, 0];
  const free = det.map(() => [0, 0]);
  let sel = -1, drag = null, slice = null;
  let W = 1, H = 1, aspect = 1, scale = 1, quality = 0.8, snapL = 3, A = [0, 0];
  const ptr = { x: 0, y: 0 };
  const tcan = document.createElement('canvas'), tctx = tcan.getContext('2d');

  const render = () => {
    const n = det.reduce((a, b) => a + b, 0);
    hintEl.textContent = n === 0 ? 'Zkuste z hmoty kus odtrhnout. Nebo ji rozřízněte tahem.'
      : n < 6 ? `Odtrženo ${n} z 6. Klikněte na kapku, nebo trhejte dál.` : 'Odtrženo všech 6. Klikněte na kapku.';
    resetBtn.hidden = n === 0;
    if (sel >= 0) {
      const p = PARTS[sel];
      msg.querySelector('.hero-msg-tag').textContent = p.tag;
      msg.querySelector('.hero-msg-title').textContent = p.head;
      msg.querySelector('.hero-msg-text').textContent = p.text;
      lead.hidden = true; msg.hidden = true; void msg.offsetWidth; msg.hidden = false;
    } else { msg.hidden = true; lead.hidden = false; }
    lab.forEach((l, i) => l.classList.toggle('is-on', !!det[i]));
  };
  resetBtn.addEventListener('click', () => { det.fill(0); sel = -1; render(); });

  const toWorld = (px, py) => [((px - W / 2) / H * 2) * CAM / F, ((H / 2 - py) / H * 2) * CAM / F];
  const toScreen = (b) => { const k = F / (CAM - b.z); return [(b.x * k / 2) * H + W / 2, H / 2 - (b.y * k / 2) * H, Math.max(b.r, 0) * k / 2 * H]; };
  const clampP = (p, r) => { const hw = aspect * CAM / F - r, hh = CAM / F - r; return [Math.max(-hw, Math.min(hw, p[0])), Math.max(-hh, Math.min(hh, p[1]))]; };

  const drawText = () => {
    if (!alive || !W) return;
    tcan.width = canvas.width; tcan.height = canvas.height;
    tctx.clearRect(0, 0, tcan.width, tcan.height);
    const sr = stage.getBoundingClientRect(), k = canvas.width / W, cs = getComputedStyle(title), fs = parseFloat(cs.fontSize) * k;
    tctx.font = `${cs.fontWeight} ${fs}px Aspekta, Inter, sans-serif`;
    try { tctx.letterSpacing = `${parseFloat(cs.letterSpacing) * k}px`; } catch (e) { /* starší prohlížeče */ }
    tctx.fillStyle = '#fff'; tctx.textBaseline = 'alphabetic';
    const m = tctx.measureText('H'), asc = m.fontBoundingBoxAscent || fs * 0.8, desc = m.fontBoundingBoxDescent || fs * 0.2;
    title.querySelectorAll('span').forEach((sp) => {
      const r = sp.getBoundingClientRect(), lh = r.height * k;
      tctx.fillText(cs.textTransform === 'uppercase' ? sp.textContent.toUpperCase() : sp.textContent, (r.left - sr.left) * k, (r.top - sr.top) * k + (lh - (asc + desc)) / 2 + asc);
    });
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, tcan);
  };

  const targets = (time) => {
    const hw = aspect * CAM / F, hh = CAM / F, nar = narrowMq.matches;
    scale = Math.min(1, Math.max(0.5, hw / 2.6)); snapL = 3.3 * scale;
    // desktop: pravý horní roh, mobil: pravý dolní roh pod textem
    A = nar ? [hw - 0.15 * scale, -hh + 0.15 * scale] : [hw - 0.15 * scale, hh - 0.15 * scale];
    const core = B[CORE]; core.tx = A[0]; core.ty = A[1]; core.tz = 0; core.tr = 1.3 * scale;
    const pull = drag && drag.moved && !det[drag.i] ? drag.i : -1;
    const P = toWorld(ptr.x, ptr.y), L = Math.hypot(P[0] - A[0], P[1] - A[1]);
    const shrink = Math.max(0.4, Math.min(1, 1.15 - L / snapL));
    const others = []; for (let j = 0; j < 6; j++) if (!det[j] && j !== pull) others.push(j);
    for (let i = 0; i < 6; i++) {
      const b = B[i], wob = reduced ? 0 : Math.sin(time * 0.7 + i * 1.9) * 0.05;
      if (drag && drag.moved && drag.i === i) { b.tx = P[0]; b.ty = P[1]; b.tz = 0.3; b.tr = 0.46 * scale; }
      else if (det[i]) { b.tx = free[i][0]; b.ty = free[i][1] + wob; b.tz = sel === i ? 0.5 : 0; b.tr = (sel === i ? 0.56 : 0.42) * scale; }
      else if (pull >= 0) { const t = (others.indexOf(i) + 1) / (others.length + 1) * 0.9; b.tx = A[0] + (P[0] - A[0]) * t; b.ty = A[1] + (P[1] - A[1]) * t; b.tz = 0.1; b.tr = 0.46 * scale * shrink; }
      else {
        const an = (nar ? 98 + i * 15 : 188 + i * 15) * Math.PI / 180, d = (1.45 + (i % 2) * 0.5 + wob) * scale;
        b.tx = A[0] + Math.cos(an) * d; b.ty = A[1] + Math.sin(an) * d; b.tz = reduced ? 0 : Math.sin(time * 0.6 + i) * 0.15; b.tr = 0.54 * scale;
      }
    }
    const x = B[AUX];
    if (pull >= 0) { x.tx = A[0] + (P[0] - A[0]) * 0.5; x.ty = A[1] + (P[1] - A[1]) * 0.5; x.tz = 0.1; x.tr = 0.3 * scale * shrink; } else x.tr = -0.8;
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
      if (hit) render();
      return;
    }
    const over = pick(p[0], p[1]);
    canvas.classList.toggle('is-hit', over >= 0);
    // popisek pro vlastní kurzor (main.js)
    if (over < 0) delete canvas.dataset.cursor; else canvas.dataset.cursor = det[over] ? 'Vybrat' : 'Trhej';
  });
  canvas.addEventListener('pointerup', (e) => {
    slice = null;
    if (!drag) { if (sel >= 0) { sel = -1; render(); } return; }
    const d = drag, p = local(e), w = toWorld(p[0], p[1]);
    drag = null; canvas.classList.remove('is-drag');
    if (!d.moved) { if (det[d.i]) { sel = d.i; render(); } return; }
    if (det[d.i]) {
      // kapka puštěná tam, kde se s hmotou slije, se přilepí zpět – zmizí i její popisek a text
      if (Math.hypot(w[0] - A[0], w[1] - A[1]) < 2.4 * scale) { det[d.i] = 0; if (sel === d.i) sel = -1; }
      else { free[d.i] = clampP(w, 0.45 * scale); sel = d.i; }
      render();
    }
  });
  canvas.addEventListener('pointercancel', () => { drag = null; slice = null; canvas.classList.remove('is-drag'); });

  const resize = () => {
    W = stage.clientWidth; H = stage.clientHeight;
    if (!W || !H || !alive) return;
    aspect = W / H;
    const dpr = Math.min(window.devicePixelRatio || 1, W < 760 ? 2 : 1.5) * quality;
    canvas.width = Math.max(2, Math.round(W * dpr)); canvas.height = Math.max(2, Math.round(H * dpr));
    gl.viewport(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < 6; i++) if (det[i]) free[i] = clampP(free[i], 0.45 * scale);
    drawText();
  };
  if (window.ResizeObserver) new ResizeObserver(resize).observe(stage); else window.addEventListener('resize', resize);
  resize();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(drawText);

  let visible = true;
  if (window.IntersectionObserver) new IntersectionObserver((en) => { visible = en[0].isIntersecting; }).observe(stage);

  render();
  let seeded = false, time = 0, slow = 0, frames = 0, last = performance.now();
  const loop = (now) => {
    requestAnimationFrame(loop);
    const raw = (now - last) / 1000; last = now;
    if (!alive || !visible || document.hidden || !W || !H) return;
    const dt = Math.min(0.033, raw);
    if (!reduced) time += dt;
    if (!seeded) { targets(0); B.forEach((b) => { b.x = b.tx; b.y = b.ty; b.z = b.tz; b.r = b.tr; }); seeded = true; }
    // slabší zařízení: postupně snížit rozlišení
    if (++frames > 20) { if (raw > 0.034) slow++; else slow = Math.max(0, slow - 1); if (slow > 25 && quality > 0.4) { quality *= 0.8; slow = 0; resize(); } }
    targets(time); step(dt / 2); step(dt / 2);
    for (let i = 0; i < N; i++) {
      const b = B[i]; bArr[i * 4] = b.x; bArr[i * 4 + 1] = b.y; bArr[i * 4 + 2] = b.z; bArr[i * 4 + 3] = b.r;
      // limetkově svítí jen kapka označená data-accent (Design), a to od chvíle, kdy ji někdo vytahuje z hmoty
      const lit = i < 6 && PARTS[i].accent && (det[i] || (drag && drag.moved && drag.i === i));
      const c = lit ? LIME : WHITE, kc = reduced ? 1 : 1 - Math.exp(-dt * 7);
      for (let q = 0; q < 3; q++) cArr[i * 3 + q] += (c[q] - cArr[i * 3 + q]) * kc;
    }
    gl.uniform2f(U.res, canvas.width, canvas.height); gl.uniform1f(U.time, time);
    gl.uniform4fv(U.b, bArr); gl.uniform3fv(U.c, cArr);
    gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLES, 0, 3);
    for (let j = 0; j < 6; j++) if (det[j]) { const s = toScreen(B[j]); lab[j].style.transform = `translate(${Math.round(s[0])}px,${Math.round(s[1] + s[2] + 8)}px) translateX(-50%)`; }
  };
  requestAnimationFrame(loop);
})();
