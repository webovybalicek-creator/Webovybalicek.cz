#!/usr/bin/env python3
"""Náhledové obrázky pro sdílení (og:image, 1200×630) – landing pages typů webů, rozcestník a výchozí.
Spustit po změně textů v src/data/typy-webu.py:  python3 build.py && python3 tools/og.py
Výstup: assets/img/og/<slug>.jpg (commitují se, deploy je jen kopíruje)."""
import asyncio
import functools
import html
import http.server
import re
import sys
import threading
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import typy  # noqa: E402

OUT = ROOT / "assets" / "img" / "og"
KAPKA = (ROOT / "tools" / "kapky" / "a-ink.svg").read_text() if (ROOT / "tools" / "kapky" / "a-ink.svg").exists() else ""
WAVE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 60' preserveAspectRatio='none'%3E"
        "%3Cpath d='M0 14 Q15 0 30 14 T60 14 T90 14 T120 14 T150 14 T180 14 T210 14 T240 14 V60 H0Z' fill='%23cdfe00'/%3E%3C/svg%3E\")")

CSS = f"""
@font-face {{ font-family: Geist; src: url(/assets/fonts/Geist-latin-ext.woff2) format("woff2"); font-weight: 100 900; }}
@font-face {{ font-family: Geist; src: url(/assets/fonts/Geist-latin.woff2) format("woff2"); font-weight: 100 900; unicode-range: U+0000-00FF; }}
@font-face {{ font-family: Aspekta; src: url(/assets/fonts/AspektaVF.woff2) format("woff2"); font-weight: 100 900; }}
.lg {{ display: inline-flex; align-items: center; gap: 8px; align-self: flex-start; color: #0a1217; }}
.lg svg {{ height: 30px; width: auto; display: block; }}
.lg span {{ font: 620 30px/1 Aspekta, sans-serif; letter-spacing: -0.022em; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 1200px; height: 630px; overflow: hidden; font-family: Geist, sans-serif; color: #0a1217; background: #f1f1f1; position: relative; }}
.kapky {{ position: absolute; top: 0; right: 0; height: 330px; color: #0a1217; }}
.txt {{ position: absolute; left: 72px; top: 64px; bottom: 64px; width: 620px; display: flex; flex-direction: column; }}
.logo {{ height: 30px; width: auto; align-self: flex-start; }}
.pill {{ margin-top: auto; font: 500 17px/1 ui-monospace, Menlo, monospace; letter-spacing: .08em; text-transform: uppercase; color: #54595d; }}
h1 {{ margin: 20px 0 0; font-size: 64px; line-height: 1.04; letter-spacing: -0.03em; font-weight: 650; text-wrap: balance; }}
h1 em {{ font-style: normal; background: {WAVE} left 0 bottom .12em / 200% .5em no-repeat; }}
.foot {{ margin-top: 36px; display: flex; gap: 16px; align-items: center; font-size: 20px; color: #54595d; }}
.price {{ padding: 10px 18px; border-radius: 999px; background: #0a1217; color: #cdfe00; font-weight: 600; }}
.frame {{ position: absolute; left: 760px; top: 150px; width: 400px; height: 520px; border-radius: 16px; background: #fff;
  box-shadow: 0 0 0 1px #e6e7e8, 0 30px 60px -20px rgba(10,18,23,.35); overflow: hidden; }}
.bar {{ height: 34px; display: flex; align-items: center; gap: 6px; padding: 0 14px; border-bottom: 1px solid #e6e7e8; font-size: 12px; color: #85898b; }}
.bar i {{ width: 9px; height: 9px; border-radius: 50%; background: #e6e7e8; }}
.bar b {{ margin-left: 10px; font-weight: 400; }}
.frame img {{ width: 100%; display: block; }}
.ico {{ position: absolute; left: 820px; top: 230px; width: 280px; height: 280px; border-radius: 50%; background: #cdfe00; display: grid; place-items: center; }}
.ico svg {{ width: 120px; height: 120px; fill: none; stroke: #0a1217; stroke-width: 1.2; stroke-linecap: round; stroke-linejoin: round; }}
"""


def card(group, title, price, ref=None, svg=None):
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html.escape(title))
    right = ""
    if ref:
        host = re.sub(r"^https?://(www\.)?", "", ref["u"]).strip("/")
        right = f'<div class="frame"><div class="bar"><i></i><i></i><i></i><b>{host}</b></div><img src="/assets/img/reference/{ref["s"]}.webp"></div>'
    elif svg:
        right = f'<div class="ico">{re.sub(r'class="[^"]*"', "", svg, 1)}</div>'
    foot = (f'<span class="price">{html.escape(price)}</span>' if price else "") + "<span>webovybalicek.cz</span>"
    return (f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><body>{KAPKA}{right}'
            f'<div class="txt"><div class="lg"><svg viewBox="0 0 400 263"><path fill="currentColor" d="M0 0h119.5L190 122.77 130 228zM280 0h120L250 263l-60-105.2z"/></svg><span>webovybalicek</span></div><p class="pill">{html.escape(group)}</p>'
            f'<h1>{t}</h1><div class="foot">{foot}</div></div></body>')


async def main():
    import json
    vyber = {r["s"]: r for r in json.loads((ROOT / "src/data/reference-vyber.json").read_text())}
    items, svc = typy.load(ROOT / "src")
    jobs = []
    for t in items:
        price = t.get("price", svc[t["svc"]][1])
        ref = next((vyber[k] for k in t.get("refs", []) if k in vyber), None)
        jobs.append((t["s"], card(t["g"], t["h"], price, ref, t["svg"])))
    jobs.append(("tvorba-webu", card("Tvorba webů", "Weby pro *každý obor*", "29 typů webů", vyber.get("kabinykravak-cz"))))

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    handler.log_message = lambda *a: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    port = srv.server_address[1]
    tmp = ROOT / ".og-tmp.html"
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        for slug, doc in jobs:
            tmp.write_text(doc, encoding="utf-8")
            await pg.goto(f"http://127.0.0.1:{port}/.og-tmp.html?{slug}", wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=str(OUT / f"{slug}.jpg"), type="jpeg", quality=86)
        await b.close()
    tmp.unlink()
    srv.shutdown()
    print(f"{len(jobs)} obrázků → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    asyncio.run(main())
