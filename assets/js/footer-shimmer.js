// Patička: obří „webovybalicek“ vyplněný živou perletí (jako duhová blána) – pomalu se přelévá.
// Text se vykreslí do masky, WebGL do ní maluje proudící duhový šum. Bez WebGL zůstane CSS přechod.
(() => {
  const el = document.querySelector('.footer-giant');
  if (!el || !document.fonts) return;
  const canvas = document.createElement('canvas');
  canvas.className = 'footer-giant-gl';
  canvas.setAttribute('aria-hidden', 'true');
  let gl = null;
  try { gl = canvas.getContext('webgl', { premultipliedAlpha: true, alpha: true, antialias: false }); } catch (e) { /* bez WebGL */ }
  if (!gl) return;

  const FS = `
precision highp float;
uniform vec2 uRes;uniform float uTime;uniform sampler2D uMask;
float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.0-2.0*f);
  return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}
float fbm(vec2 p){float v=0.0,a=0.5;for(int i=0;i<5;i++){v+=a*n(p);p=p*2.03+vec2(1.7,9.2);a*=0.5;}return v;}
void main(){
  vec2 uv=gl_FragCoord.xy/uRes;
  float m=texture2D(uMask,vec2(uv.x,1.0-uv.y)).a;
  if(m<0.003){gl_FragColor=vec4(0.0);return;}
  float t=uTime*0.06;
  vec2 p=vec2(uv.x*uRes.x/uRes.y,uv.y)*1.1;
  vec2 q=vec2(fbm(p+vec2(0.0,t)),fbm(p+vec2(5.2,1.3)-t));
  vec2 r=vec2(fbm(p+3.0*q+vec2(1.7,9.2)+t*0.7),fbm(p+3.0*q+vec2(8.3,2.8)-t*0.6));
  float f=fbm(p+3.5*r);
  // duhová perleť: pastelové barvy podle proudění, bílé „blány“ v místech zhuštění
  vec3 iri=0.74+0.26*cos(6.2832*(f*1.4+r.x*0.6+q.y*0.3+uTime*0.01+vec3(0.0,0.33,0.67)));
  vec3 col=mix(vec3(0.78,0.79,0.83),iri,0.45+0.3*r.y);
  col=mix(col,vec3(1.0),smoothstep(0.5,0.85,f)*0.6);
  col=mix(col,vec3(0.62,0.64,0.7),smoothstep(0.45,0.15,f)*0.35);
  col*=0.9+0.25*smoothstep(0.3,0.8,length(q));
  gl_FragColor=vec4(col*m,m);}`;
  const sh = (t, s) => { const o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); return gl.getShaderParameter(o, gl.COMPILE_STATUS) ? o : null; };
  const vs = sh(gl.VERTEX_SHADER, 'attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}'), fs = sh(gl.FRAGMENT_SHADER, FS);
  if (!vs || !fs) return;
  const prog = gl.createProgram(); gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
  gl.useProgram(prog);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const la = gl.getAttribLocation(prog, 'a'); gl.enableVertexAttribArray(la); gl.vertexAttribPointer(la, 2, gl.FLOAT, false, 0, 0);
  const uRes = gl.getUniformLocation(prog, 'uRes'), uTime = gl.getUniformLocation(prog, 'uTime');
  const tex = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, tex);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  gl.clearColor(0, 0, 0, 0);

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const mask = document.createElement('canvas');
  let visible = false, raf = 0, last = 0, ready = false;

  // maska = přesně ten text, jak ho vysází prohlížeč (stejné písmo, velikost i prostrkání)
  const layout = () => {
    const r = el.getBoundingClientRect();
    const dpr = Math.min(devicePixelRatio || 1, 1.5);
    const cs = getComputedStyle(el);
    const w = Math.max(1, Math.round(r.width * dpr)), hgt = Math.max(1, Math.round(r.height * dpr));
    canvas.width = mask.width = w; canvas.height = mask.height = hgt;
    canvas.style.width = `${r.width}px`; canvas.style.height = `${r.height}px`;
    canvas.style.left = `${el.offsetLeft}px`; canvas.style.top = `${el.offsetTop}px`;
    const probe = document.createElement('i');
    probe.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline';
    el.append(probe);
    const base = probe.getBoundingClientRect().top - r.top;
    probe.remove();
    const range = document.createRange(); range.selectNodeContents(el.firstChild);
    const tr = range.getBoundingClientRect();
    const ctx = mask.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, r.width, r.height);
    ctx.font = `${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    if ('letterSpacing' in ctx) ctx.letterSpacing = cs.letterSpacing;
    ctx.textBaseline = 'alphabetic'; ctx.fillStyle = '#000';
    ctx.fillText(el.textContent, tr.left - r.left, base);
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, mask);
    gl.viewport(0, 0, w, hgt);
    ready = true;
    draw(performance.now());
  };
  const draw = (now) => {
    if (!ready) return;
    gl.uniform2f(uRes, canvas.width, canvas.height); gl.uniform1f(uTime, reduced ? 20 : now / 1000);
    gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLES, 0, 3);
  };
  const loop = (now) => {
    raf = 0;
    if (!visible || reduced) return;
    if (now - last > 40) { last = now; draw(now); }
    raf = requestAnimationFrame(loop);
  };
  document.fonts.ready.then(() => {
    el.parentElement.append(canvas);
    el.classList.add('has-gl');
    layout();
    new ResizeObserver(layout).observe(el);
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible && !raf) raf = requestAnimationFrame(loop); }).observe(el);
  });
})();
