#!/usr/bin/env python3
"""Výchozí náhled pro sdílení (assets/img/og/default.jpg) z brandových prvků:
perleťová hmota z úvodu (tools/og-blob.png = snímek hero canvasu), limetkové kapky, tečkový rastr, kurzory.
Spustit: (cd dist && python3 -m http.server 8765) & python3 tools/og_default.py"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
WAVE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 60' preserveAspectRatio='none'%3E"
        "%3Cpath d='M0 14 Q15 0 30 14 T60 14 T90 14 T120 14 T150 14 T180 14 T210 14 T240 14 V60 H0Z' fill='%23cdfe00'/%3E%3C/svg%3E\")")
CUR = '<svg viewBox="0 0 16 16" width="18" height="18"><path d="M2 1.5 14 7.2 8.6 8.6 6.9 14Z" fill="#0a1217" stroke="#fff" stroke-width="1.2" stroke-linejoin="round"/></svg>'

def tag(x, y, t, dark=False):
    return (f'<div class="tag" style="left:{x}px;top:{y}px">{CUR}'
            f'<span class="{"dark" if dark else ""}">{t}</span></div>')

HTML = f"""<!doctype html><meta charset="utf-8"><style>
@font-face {{ font-family: Geist; src: url(/assets/fonts/Geist-latin-ext.woff2) format("woff2"); font-weight: 100 900; }}
@font-face {{ font-family: Geist; src: url(/assets/fonts/Geist-latin.woff2) format("woff2"); font-weight: 100 900; unicode-range: U+0000-00FF; }}
@font-face {{ font-family: Aspekta; src: url(/assets/fonts/AspektaVF.woff2) format("woff2"); font-weight: 100 900; }}
.lg {{ display: inline-flex; align-items: center; gap: 8px; align-self: flex-start; color: #0a1217; }}
.lg svg {{ height: 30px; width: auto; display: block; }}
.lg span {{ font: 620 30px/1 Aspekta, sans-serif; letter-spacing: -0.022em; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 1200px; height: 630px; overflow: hidden; position: relative; font-family: Geist, sans-serif; color: #0a1217;
  background: #f6f6f6 radial-gradient(circle, rgba(10,18,23,.16) 1.1px, transparent 1.6px) 0 0 / 22px 22px; }}
.blob {{ position: absolute; left: 40px; top: -48px; width: 1200px; height: 630px; }}
.ball {{ position: absolute; border-radius: 50%;
  background: radial-gradient(circle at 34% 30%, #fbffd9 0 6%, #e6ff5c 22%, #cdfe00 48%, #a9d400 82%, #8db000 100%);
  box-shadow: 0 24px 40px -14px rgba(90,110,0,.45); }}
.tag {{ position: absolute; display: flex; align-items: flex-start; gap: 2px; }}
.tag span {{ margin-top: 14px; padding: 5px 10px; border-radius: 999px; background: #cdfe00; font: 600 15px/1 Geist, sans-serif; }}
.tag span.dark {{ background: #0a1217; color: #cdfe00; }}
.txt {{ position: absolute; left: 72px; top: 64px; bottom: 64px; width: 600px; display: flex; flex-direction: column; }}
.logo {{ height: 30px; width: auto; align-self: flex-start; }}
.kick {{ margin-top: auto; font: 500 17px/1 ui-monospace, Menlo, monospace; letter-spacing: .08em; text-transform: uppercase; color: #54595d; }}
h1 {{ margin-top: 20px; font-size: 68px; line-height: 1.02; letter-spacing: -0.035em; font-weight: 650; }}
h1 em {{ font-style: normal; background: {WAVE} left 0 bottom .12em / 200% .5em no-repeat; }}
.foot {{ margin-top: 34px; display: flex; gap: 14px; align-items: center; font-size: 20px; color: #54595d; }}
.pill {{ padding: 10px 18px; border-radius: 999px; background: #0a1217; color: #fff; font-weight: 600; }}
.pill b {{ color: #cdfe00; }}
</style><body>
<img class="blob" src="/og-blob.png">
<div class="ball" style="left:800px;top:430px;width:118px;height:118px"></div>
<div class="ball" style="left:690px;top:330px;width:46px;height:46px"></div>
<div class="ball" style="left:935px;top:560px;width:26px;height:26px"></div>
{tag(905, 380, "Design")}
{tag(735, 200, "AI", True)}
{tag(1040, 520, "SEO")}
<div class="txt">
  <div class="lg"><svg viewBox="0 0 400 263"><path fill="currentColor" d="M0 0h119.5L190 122.77 130 228zM280 0h120L250 263l-60-105.2z"/></svg><span>webovybalicek</span></div>
  <p class="kick">Tvorba webů s pomocí AI</p>
  <h1>Weby, za kterými<br>jsou <em>výsledky</em></h1>
  <div class="foot"><span class="pill"><b>★ 4,8</b> na Googlu</span><span>150+ webů · webovybalicek.cz</span></div>
</div>
</body>"""

(ROOT / "dist" / "og-default.html").write_text(HTML)
import shutil; shutil.copy(ROOT / "tools" / "og-blob.png", ROOT / "dist" / "og-blob.png")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.goto("http://localhost:8765/og-default.html"); pg.wait_for_timeout(600)
    pg.screenshot(path=str(ROOT / "assets/img/og/default.jpg"), type="jpeg", quality=88)
    b.close()
(ROOT / "dist" / "og-default.html").unlink(); (ROOT / "dist" / "og-blob.png").unlink()
