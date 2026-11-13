// Kontakt – formulář „uvnitř“ perleťové hmoty z úvodu. Hmota se skládá z koulí rozložených pod formulářem,
// jemně dýchá a vyboulí se tam, kde je myš nebo aktivní pole. Bez WebGL zůstane obyčejná bílá karta.
(() => {
  const wrap = document.querySelector('[data-form-blob]');
  if (!wrap) return;
  const form = wrap.querySelector('form');
  const canvas = document.createElement('canvas');
  canvas.className = 'form-blob-canvas';
  canvas.setAttribute('aria-hidden', 'true');
  wrap.prepend(canvas);
  let gl = null;
  try { gl = canvas.getContext('webgl', { alpha: true, premultipliedAlpha: true, antialias: false }); } catch (e) { /* bez WebGL */ }
  if (!gl) { canvas.remove(); return; }

  const N = 16;
  const FS = `
precision highp float;
uniform vec2 uRes;uniform float uTime;uniform vec4 uB[${N}];
const float F=2.2;const float CAM=5.0;const float K=0.6;
float smin(float a,float b,float k){float h=max(k-abs(a-b),0.0)/k;return min(a,b)-h*h*k*0.25;}
float map(vec3 p){float d=1e5;
  for(int i=0;i<${N};i++){d=smin(d,length(p-uB[i].xyz)-uB[i].w,K);}
  return d+0.025*sin(2.4*p.x+uTime*0.9)*sin(2.7*p.y-uTime*0.7)*sin(2.1*p.z+uTime*0.6);}
vec3 pal(float t){return 0.5+0.5*cos(6.2832*(t+vec3(0.0,0.33,0.67)));}
vec3 tm(vec3 c){return pow(1.0-exp(-c*1.5),vec3(0.4545));}
void main(){
  vec2 uv=(gl_FragCoord.xy-0.5*uRes)/uRes.y*2.0;
  vec3 ro=vec3(0.0,0.0,CAM);vec3 rd=normalize(vec3(uv,-F));
  float t=2.2;float md=1e5;vec3 pm=ro;bool hit=false;vec3 p=ro;
  for(int i=0;i<48;i++){p=ro+rd*t;float d=map(p);if(d<md){md=d;pm=p;}if(d<0.004){hit=true;break;}t+=d*0.9;if(t>8.5)break;}
  float al=hit?1.0:clamp(1.0-md/0.02,0.0,1.0);if(!hit)p=pm;
  vec3 col=vec3(0.0);
  if(al>0.0){
    vec2 e=vec2(0.004,-0.004);
    vec3 n=normalize(e.xyy*map(p+e.xyy)+e.yyx*map(p+e.yyx)+e.yxy*map(p+e.yxy)+e.xxx*map(p+e.xxx));
    float ndv=max(dot(n,-rd),0.0);float fr=pow(1.0-ndv,3.0);
    vec3 r=reflect(rd,n);vec3 L=normalize(vec3(-0.45,0.65,0.6));
    float ndl=max(dot(n,L),0.0);float sp=pow(max(dot(r,L),0.0),70.0);
    col=vec3(0.84)*(0.64+0.36*ndl)*(0.84+0.16*ndv);
    col=mix(col,pal(fr*1.3+n.y*0.3+uTime*0.03)*0.75+0.2,fr*0.6)+vec3(sp*0.6);
    col=tm(col)*al;
  }
  vec2 q=gl_FragCoord.xy/uRes;float edge=smoothstep(0.0,0.12,min(min(q.x,1.0-q.x),min(q.y,1.0-q.y)));
  float a=al+exp(-max(md,0.0)*9.0)*(1.0-al)*0.14*edge;
  gl_FragColor=vec4(col,a);}`;
  const sh = (type, src) => { const o = gl.createShader(type); gl.shaderSource(o, src); gl.compileShader(o); return gl.getShaderParameter(o, gl.COMPILE_STATUS) ? o : null; };
  const vs = sh(gl.VERTEX_SHADER, 'attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}'), fs = sh(gl.FRAGMENT_SHADER, FS);
  if (!vs || !fs) { canvas.remove(); return; }
  const prog = gl.createProgram(); gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { canvas.remove(); return; }
  gl.useProgram(prog);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const la = gl.getAttribLocation(prog, 'a'); gl.enableVertexAttribArray(la); gl.vertexAttribPointer(la, 2, gl.FLOAT, false, 0, 0);
  const uRes = gl.getUniformLocation(prog, 'uRes'), uTime = gl.getUniformLocation(prog, 'uTime'), uB = gl.getUniformLocation(prog, 'uB[0]');
  gl.clearColor(0, 0, 0, 0);
  wrap.classList.add('has-gl');

  const F = 2.2, CAM = 5, RES = 0.6; // vykresluje se v nižším rozlišení, hmota je měkká
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let W = 1, H = 1, balls = [], visible = false, raf = 0, last = 0;
  const bArr = new Float32Array(N * 4);
  const ptr = { x: -1e4, y: -1e4, on: 0, k: 0 };
  const toWorld = (px, py) => [((px - W / 2) / H * 2) * CAM / F, ((H / 2 - py) / H * 2) * CAM / F];

  const layout = () => {
    const cr = canvas.getBoundingClientRect(), fr = form.getBoundingClientRect();
    W = cr.width; H = cr.height;
    canvas.width = Math.max(1, Math.round(W * RES)); canvas.height = Math.max(1, Math.round(H * RES));
    gl.viewport(0, 0, canvas.width, canvas.height);
    // obdélník formuláře v souřadnicích hmoty, trochu zvětšený, aby hrany hmoty zůstaly mimo text
    const pad = 14;
    const [x0, y0] = toWorld(fr.left - cr.left - pad, fr.top - cr.top - pad);
    const [x1, y1] = toWorld(fr.right - cr.left + pad, fr.bottom - cr.top + pad);
    const w = x1 - x0, h = y0 - y1;
    const ny = Math.max(3, Math.min(4, Math.round(h / (w / 3)))), nx = Math.max(2, Math.min(Math.floor((N - 3) / ny), Math.round(w / (h / ny))));
    const sx = w / nx, sy = h / ny, r = 0.6 * Math.max(sx, sy);
    balls = [];
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      balls.push({ x: x0 + sx * (i + 0.5), y: y0 - sy * (j + 0.5), r, ph: Math.random() * 6.28, amp: 0.05 });
    }
    // pár menších koulí na okrajích – nepravidelný obrys
    const extra = [[x0 - r * 0.2, y0 - h * 0.3, 0.55], [x0 - r * 0.05, y1 + h * 0.18, 0.5], [x0 + w * 0.35, y1 - r * 0.15, 0.45]];
    extra.forEach(([x, y, k]) => { if (balls.length < N) balls.push({ x, y, r: r * k, ph: Math.random() * 6.28, amp: 0.12 }); });
    while (balls.length < N) balls.push({ x: 0, y: 0, r: -1, ph: 0, amp: 0 });
    draw(performance.now());
  };

  const draw = (now) => {
    const t = now / 1000;
    ptr.k += ((ptr.on ? 1 : 0) - ptr.k) * 0.08;
    const [px, py] = toWorld(ptr.x, ptr.y);
    balls.forEach((b, i) => {
      if (b.r < 0) { bArr.set([0, 0, 0, -1], i * 4); return; }
      const breathe = reduced ? 0 : Math.sin(t * 0.6 + b.ph) * b.amp * b.r;
      const near = Math.exp(-((b.x - px) ** 2 + (b.y - py) ** 2) / (b.r * b.r * 0.8)) * ptr.k;
      bArr.set([b.x + Math.cos(t * 0.4 + b.ph) * b.amp * 0.3, b.y + Math.sin(t * 0.5 + b.ph) * b.amp * 0.3, near * 0.35, b.r + breathe + near * 0.08], i * 4);
    });
    gl.uniform2f(uRes, canvas.width, canvas.height); gl.uniform1f(uTime, reduced ? 0 : t); gl.uniform4fv(uB, bArr);
    gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLES, 0, 3);
  };
  const loop = (now) => {
    raf = 0;
    if (!visible || reduced) return;
    if (now - last > 33) { last = now; draw(now); } // ~30 fps stačí
    raf = requestAnimationFrame(loop);
  };
  const start = () => { if (!raf && visible && !reduced) raf = requestAnimationFrame(loop); };

  new IntersectionObserver(([e]) => { visible = e.isIntersecting; start(); }).observe(wrap);
  new ResizeObserver(() => layout()).observe(wrap);
  wrap.addEventListener('pointermove', (e) => { const cr = canvas.getBoundingClientRect(); ptr.x = e.clientX - cr.left; ptr.y = e.clientY - cr.top; ptr.on = 1; });
  wrap.addEventListener('pointerleave', () => { if (!form.contains(document.activeElement)) ptr.on = 0; });
  form.addEventListener('focusin', (e) => {
    const cr = canvas.getBoundingClientRect(), r = e.target.getBoundingClientRect();
    ptr.x = r.left + r.width / 2 - cr.left; ptr.y = r.top + r.height / 2 - cr.top; ptr.on = 1; if (reduced) draw(performance.now());
  });
  form.addEventListener('focusout', () => { ptr.on = 0; });
  canvas.addEventListener('webglcontextlost', (e) => { e.preventDefault(); wrap.classList.remove('has-gl'); canvas.remove(); visible = false; });
})();
