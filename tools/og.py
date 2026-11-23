#!/usr/bin/env python3
"""Náhledy pro sdílení (og:image 1200×630) pro KAŽDOU veřejnou URL webu.

Styl: perleťová hmota z úvodu (tools/og-blob.png = snímek hero canvasu), limetkové kapky,
tečkový rastr, kurzory se štítky, nadpis s limetkovým podtržením, logo jako v hlavičce.

Postup:
  python3 build.py            # zapíše tools/og-jobs.json (texty všech stránek)
  python3 tools/og.py         # vyrenderuje jen CHYBĚJÍCÍ obrázky → assets/img/og/p/<slug>.jpg
  python3 tools/og.py --vse   # přegeneruje všechny (po změně šablony)
  python3 tools/og.py cenik kontakt   # jen vybrané slugy
  python3 build.py            # znovu, aby stránky převzaly nové obrázky

Texty: stránky ze src/pages → OG_PAGES v build.py; landing pages a pluginy → meta["og"] v src/typy.py a src/plugins.py.
Úvodní stránka se ukládá i jako assets/img/og/default.jpg (výchozí náhled)."""
import functools
import hashlib
import html
import http.server
import json
import re
import shutil
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "og" / "p"
JOBS = ROOT / "tools" / "og-jobs.json"

WAVE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 60' preserveAspectRatio='none'%3E"
        "%3Cpath d='M0 14 Q15 0 30 14 T60 14 T90 14 T120 14 T150 14 T180 14 T210 14 T240 14 V60 H0Z' fill='%23cdfe00'/%3E%3C/svg%3E\")")
CUR = ('<svg viewBox="0 0 16 16" width="18" height="18"><path d="M2 1.5 14 7.2 8.6 8.6 6.9 14Z" fill="#0a1217" '
       'stroke="#fff" stroke-width="1.2" stroke-linejoin="round"/></svg>')
LOGO = ('<div class="lg"><svg viewBox="0 0 400 263"><path fill="currentColor" d="M0 0h119.5L190 122.77 130 228zM280 0h120L250 263l-60-105.2z"/>'
        '</svg><span>webovybalicek</span></div>')

CSS = f"""
@font-face {{ font-family: Geist; src: url(/assets/fonts/Geist-latin-ext.woff2) format("woff2"); font-weight: 100 900; }}
@font-face {{ font-family: Geist; src: url(/assets/fonts/Geist-latin.woff2) format("woff2"); font-weight: 100 900; unicode-range: U+0000-00FF; }}
@font-face {{ font-family: Aspekta; src: url(/assets/fonts/AspektaVF.woff2) format("woff2"); font-weight: 100 900; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 1200px; height: 630px; overflow: hidden; position: relative; font-family: Geist, sans-serif; color: #0a1217;
  background: #f6f6f6 radial-gradient(circle, rgba(10,18,23,.16) 1.1px, transparent 1.6px) 0 0 / 22px 22px; }}
.blob {{ position: absolute; left: 40px; top: -48px; width: 1200px; height: 630px; }}
.ball {{ position: absolute; border-radius: 50%;
  background: radial-gradient(circle at 34% 30%, #fbffd9 0 6%, #e6ff5c 22%, #cdfe00 48%, #a9d400 82%, #8db000 100%);
  box-shadow: 0 24px 40px -14px rgba(90,110,0,.45); }}
.tag {{ position: absolute; display: flex; align-items: flex-start; gap: 2px; }}
.tag span {{ margin-top: 14px; padding: 5px 10px; border-radius: 999px; background: #cdfe00; font: 600 15px/1 Geist, sans-serif; white-space: nowrap; }}
.tag span.dark {{ background: #0a1217; color: #cdfe00; }}
.txt {{ position: absolute; left: 72px; top: 64px; bottom: 64px; width: 600px; display: flex; flex-direction: column; }}
.lg {{ display: inline-flex; align-items: center; gap: 8px; align-self: flex-start; }}
.lg svg {{ height: 30px; width: auto; display: block; }}
.lg span {{ font: 620 30px/1 Aspekta, sans-serif; letter-spacing: -0.022em; }}
.kick {{ margin-top: auto; font: 500 17px/1.3 ui-monospace, Menlo, monospace; letter-spacing: .08em; text-transform: uppercase; color: #54595d; }}
h1 {{ margin-top: 20px; font-size: 68px; line-height: 1.04; letter-spacing: -0.035em; font-weight: 650; text-wrap: balance; }}
h1 em {{ font-style: normal; background: {WAVE} left 0 bottom .12em / 200% .5em no-repeat; }}
.foot {{ margin-top: 34px; display: flex; gap: 14px; align-items: center; font-size: 20px; color: #54595d; }}
.pill {{ padding: 10px 18px; border-radius: 999px; background: #0a1217; color: #fff; font-weight: 600; white-space: nowrap; }}
.pill b {{ color: #cdfe00; }}
"""


def tag(x, y, t, dark=False):
    return f'<div class="tag" style="left:{x}px;top:{y}px">{CUR}<span class="{"dark" if dark else ""}">{html.escape(t)}</span></div>'


def headline(h):
    t = html.escape(h)
    if "*" in t:
        return re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    w = t.rsplit(" ", 1)  # bez hvězdiček podtrhne poslední slovo
    return f"{w[0]} <em>{w[1]}</em>" if len(w) == 2 else f"<em>{t}</em>"


def page(job):
    tags = job.get("tags") or ["Design", "AI", "SEO"]
    pill = job.get("pill")
    pill_html = f'<span class="pill"><b>{html.escape(pill)}</b></span>' if pill else '<span class="pill"><b>★ 4,8</b> na Googlu</span>'
    foot = pill_html + "<span>150+ webů · webovybalicek.cz</span>"
    return f"""<!doctype html><meta charset="utf-8"><style>{CSS}</style><body>
<img class="blob" src="/tools/og-blob.png">
<div class="ball" style="left:800px;top:430px;width:118px;height:118px"></div>
<div class="ball" style="left:690px;top:330px;width:46px;height:46px"></div>
<div class="ball" style="left:935px;top:560px;width:26px;height:26px"></div>
{tag(905, 380, tags[0])}{tag(735, 200, tags[1], True)}{tag(1040, 520, tags[2])}
<div class="txt">{LOGO}<p class="kick">{html.escape(job["k"])}</p><h1>{headline(job["h"])}</h1><div class="foot">{foot}</div></div>
<script>
// nadpis musí vejít mezi nadtitulek a patičku – zmenšuj, dokud přetéká
const h = document.querySelector('h1'); let s = 68;
while ((h.scrollHeight > 220 || h.getBoundingClientRect().right > 672) && s > 36) {{ s -= 2; h.style.fontSize = s + 'px'; }}
</script></body>"""


def main():
    args = sys.argv[1:]
    every = "--vse" in args
    only = {a for a in args if not a.startswith("--")}
    jobs = json.loads(JOBS.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    if only:
        todo = [j for j in jobs if j["slug"] in only]
    else:
        todo = [j for j in jobs if every or not (OUT / f"{j['slug']}.jpg").exists()]

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Quiet, directory=str(ROOT))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    port = srv.server_address[1]
    tmp = ROOT / ".og-tmp.html"
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for j in todo:
            tmp.write_text(page(j), encoding="utf-8")
            pg.goto(f"http://127.0.0.1:{port}/.og-tmp.html?{hashlib.md5(j['slug'].encode()).hexdigest()}", wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(50)
            pg.screenshot(path=str(OUT / f"{j['slug']}.jpg"), type="jpeg", quality=86)
        b.close()
    tmp.unlink(missing_ok=True)
    srv.shutdown()
    if (OUT / "index.jpg").exists():
        shutil.copy2(OUT / "index.jpg", ROOT / "assets/img/og/default.jpg")
    print(f"{len(todo)} nových náhledů → {OUT.relative_to(ROOT)} (celkem stránek: {len(jobs)})")


if __name__ == "__main__":
    main()
