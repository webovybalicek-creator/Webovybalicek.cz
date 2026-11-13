// Kontakt – celý panel sekce je perleťová hmota ve stejném materiálu jako úvod: nafouknutý obdélník
// s ostrým obrysem a pár jemnými výdutěmi, které pomalu dýchají. Bez WebGL zůstane šedý panel.
(() => {
  const panel = document.querySelector('[data-panel-blob]');
  if (!panel) return;
  const canvas = document.createElement('canvas');
  canvas.className = 'panel-blob-canvas';
  canvas.setAttribute('aria-hidden', 'true');
  panel.prepend(canvas);
  let gl = null;
  try { gl = canvas.getContext('webgl', { alpha: true, premultipliedAlpha: true, antialias: false }); } catch (e) { /* bez WebGL */ }
  if (!gl) { canvas.remove(); return; }

  const FS = `
precision highp float;
uniform vec2 uRes;uniform float uTime;uniform vec4 uBox;uniform float uRc;uniform vec4 uS[4];
const float F=2.2;const float CAM=5.0;const float R=0.32;
float smin(float a,float b,float k){float h=max(k-abs(a-b),0.0)/k;return min(a,b)-h*h*k*0.25;}
float rrect(vec2 p,vec2 b,float r){vec2 q=abs(p)-b+r;return length(max(q,0.0))+min(max(q.x,q.y),0.0)-r;}
float map(vec3 p){
  vec3 q=p-vec3(uBox.xy,0.0);
  float d2=rrect(q.xy,uBox.zw-R,max(uRc-R,0.01));
  float d=length(vec2(max(d2,0.0),q.z))+min(max(d2,abs(q.z)),0.0)-R;
  for(int i=0;i<4;i++){vec3 e=(p-uS[i].xyz)/vec3(uS[i].w,uS[i].w,R*1.1);d=smin(d,(length(e)-1.0)*min(uS[i].w,R*1.1),0.12);}
  return d+0.006*sin(1.7*p.x+uTime*0.5)*sin(1.9*p.y-uTime*0.4);}
vec3 pal(float t){return 0.5+0.5*cos(6.2832*(t+vec3(0.0,0.33,0.67)));}
vec3 tm(vec3 c){return pow(1.0-exp(-c*1.5),vec3(0.4545));}
void main(){
  vec2 uv=(gl_FragCoord.xy-0.5*uRes)/uRes.y*2.0;
  // pravoúhlá projekce: obrys přesně kopíruje panel, žádné rozšiřování do perspektivy
  vec3 ro=vec3(uv*CAM/F,CAM);vec3 rd=vec3(0.0,0.0,-1.0);
  float t=4.0;float md=1e5;bool hit=false;vec3 p=ro;vec3 pm=ro;
  for(int i=0;i<48;i++){p=ro+rd*t;float d=map(p);if(d<md){md=d;pm=p;}if(d<0.002){hit=true;break;}t+=d;if(t>6.0)break;}
  float al=hit?1.0:clamp(1.0-md/0.006,0.0,1.0);if(!hit)p=pm;
  vec3 col=vec3(0.0);
  if(al>0.0){
    vec2 e=vec2(0.003,-0.003);
    vec3 n=normalize(e.xyy*map(p+e.xyy)+e.yyx*map(p+e.yyx)+e.yxy*map(p+e.yxy)+e.xxx*map(p+e.xxx));
    float ndv=max(dot(n,-rd),0.0);float fr=pow(1.0-ndv,3.0);
    vec3 r=reflect(rd,n);vec3 L=normalize(vec3(-0.45,0.65,0.6));
    float ndl=max(dot(n,L),0.0);float sp=pow(max(dot(r,L),0.0),70.0);
    // plochý vršek jemně přechází do světla, aby nebyl mrtvě šedý
    vec2 sv=gl_FragCoord.xy/uRes;
    col=vec3(0.92)*(0.68+0.32*ndl)*(0.86+0.14*ndv)*(0.96+0.06*sv.y);
    col=mix(col,pal(fr*1.3+n.y*0.3+uTime*0.03)*0.75+0.2,fr*0.65)+vec3(sp*0.6);
    col=tm(col)*al;
  }
  vec2 q=gl_FragCoord.xy/uRes;float edge=smoothstep(0.0,0.1,min(min(q.x,1.0-q.x),min(q.y,1.0-q.y)));
  float a=al+exp(-max(md,0.0)*14.0)*(1.0-al)*0.16*edge;
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
  const U = { res: gl.getUniformLocation(prog, 'uRes'), time: gl.getUniformLocation(prog, 'uTime'), box: gl.getUniformLocation(prog, 'uBox'), rc: gl.getUniformLocation(prog, 'uRc'), s: gl.getUniformLocation(prog, 'uS[0]') };
  gl.clearColor(0, 0, 0, 0);
  panel.classList.add('has-gl');

  const F = 2.2, CAM = 5, RES = 0.75;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let W = 1, H = 1, k = 1, box = [0, 0, 1, 1], rc = 0.3, bumps = [], visible = false, raf = 0, last = 0;
  const sArr = new Float32Array(16);
  // svět v rovině z=0 → obrazovka; přední plocha (z=R) je o kousek blíž, proto ji zmenšujeme
  const toWorld = (px, py) => [((px - W / 2) / H * 2) * CAM / F, ((H / 2 - py) / H * 2) * CAM / F];

  const layout = () => {
    const cr = canvas.getBoundingClientRect(), pr = panel.getBoundingClientRect();
    W = cr.width; H = cr.height;
    canvas.width = Math.max(1, Math.round(W * RES)); canvas.height = Math.max(1, Math.round(H * RES));
    gl.viewport(0, 0, canvas.width, canvas.height);
    const [x0, y0] = toWorld(pr.left - cr.left, pr.top - cr.top), [x1, y1] = toWorld(pr.right - cr.left, pr.bottom - cr.top);
    k = (x1 - x0) / pr.width; // světových jednotek na pixel
    box = [(x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y0 - y1) / 2];
    rc = parseFloat(getComputedStyle(panel).borderTopLeftRadius) * k || 0.3;
    // výdutě: pravý horní roh (jako hmota v úvodu), levý dolní okraj, horní hrana
    k *= Math.min(1, pr.width / 1000); // na úzkém panelu menší výdutě
    bumps = [
      { x: x1 - 110 * k, y: y0 - 90 * k, r: 130 * k, ph: 0.0 },
      { x: x0 + 110 * k, y: y1 + 80 * k, r: 92 * k, ph: 2.1 },
      { x: x0 + (x1 - x0) * 0.62, y: y0 - 30 * k, r: 44 * k, ph: 4.2 },
      { x: 0, y: 0, r: 0.0001, ph: 0 },
    ];
    draw(performance.now());
  };
  const draw = (now) => {
    const t = reduced ? 0 : now / 1000;
    bumps.forEach((b, i) => sArr.set([b.x + Math.cos(t * 0.35 + b.ph) * b.r * 0.06, b.y + Math.sin(t * 0.3 + b.ph) * b.r * 0.06, -0.05, b.r * (1 + Math.sin(t * 0.5 + b.ph) * 0.05)], i * 4));
    gl.uniform2f(U.res, canvas.width, canvas.height); gl.uniform1f(U.time, t);
    gl.uniform4f(U.box, box[0], box[1], box[2], box[3]); gl.uniform1f(U.rc, rc); gl.uniform4fv(U.s, sArr);
    gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLES, 0, 3);
  };
  const loop = (now) => {
    raf = 0;
    if (!visible || reduced) return;
    if (now - last > 40) { last = now; draw(now); }
    raf = requestAnimationFrame(loop);
  };
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible && !raf && !reduced) raf = requestAnimationFrame(loop); }).observe(panel);
  new ResizeObserver(layout).observe(panel);
  canvas.addEventListener('webglcontextlost', (e) => { e.preventDefault(); panel.classList.remove('has-gl'); canvas.remove(); visible = false; });
})();
