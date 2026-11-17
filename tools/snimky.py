#!/usr/bin/env python3
"""Pořídí dlouhé screenshoty referenčních webů do assets/img/reference/<slug>.webp
a zapíše src/data/reference-snimky.json (titulek, popis, rozměry). Běží v GitHub Action „Snímky referencí“."""
import asyncio, io, json, re, sys
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/reference"
WEBY = json.loads((ROOT / "src/data/reference-weby.json").read_text())
W, H, MAXH, OUTW = 1440, 900, 5600, 880

HIDE = """
:is([id*="cookie" i],[class*="cookie" i],[id*="consent" i],[class*="consent" i],[id*="cmplz" i],[class*="cmplz" i],
[id*="gdpr" i],[class*="gdpr" i],#CybotCookiebotDialog,.cky-consent-container,.cky-overlay,
.elementor-popup-modal,.pum,.pum-overlay,[id*="chat-widget" i],[class*="chat-widget" i],iframe[src*="tawk"],#smartsupp-widget-container):not(html):not(body):not(main):not(#page):not(.site)
{ display: none !important; visibility: hidden !important; }
html { scroll-behavior: auto !important; }
.elementor-invisible { visibility: visible !important; }
"""

def slug(url):
    return re.sub(r"^www\.", "", re.sub(r"^https?://", "", url).strip("/")).replace(".", "-")

async def snimek(browser, url):
    s = slug(url)
    ctx = await browser.new_context(viewport={"width": W, "height": H}, locale="cs-CZ",
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36")
    pg = await ctx.new_page()
    try:
        await pg.goto(url, wait_until="load", timeout=60000)
        await pg.wait_for_timeout(2500)
        await pg.add_style_tag(content=HIDE)
        meta = await pg.evaluate("""() => ({ title: document.title, desc: (document.querySelector('meta[name=description]')||{}).content || '',
            h1: (document.querySelector('h1')||{}).innerText || '' })""")
        # projet stránku kvůli lazy loadu a animacím při scrollu
        total = await pg.evaluate("Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)")
        y = 0
        while y < min(total, MAXH):
            await pg.evaluate(f"window.scrollTo(0, {y})"); await pg.wait_for_timeout(450); y += 450
        await pg.evaluate("window.scrollTo(0, 0)"); await pg.wait_for_timeout(800)
        total = await pg.evaluate("Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)")
        png = await pg.screenshot(full_page=True, clip={"x": 0, "y": 0, "width": W, "height": min(total, MAXH)})
        im = Image.open(io.BytesIO(png)).convert("RGB")
        im = im.resize((OUTW, round(im.height * OUTW / im.width)), Image.LANCZOS)
        im.save(OUT / f"{s}.webp", "WEBP", quality=72, method=6)
        print("OK", url, im.size, flush=True)
        return s, {"url": url, "w": im.width, "h": im.height, **meta}
    except Exception as e:
        print("CHYBA", url, repr(e)[:200], flush=True)
        return s, None
    finally:
        await ctx.close()

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    jen = set(sys.argv[1:])
    datap = ROOT / "src/data/reference-snimky.json"
    data = json.loads(datap.read_text()) if datap.exists() else {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for url in WEBY:
            if jen and slug(url) not in jen: continue
            s, m = await snimek(b, url)
            if m: data[s] = m
        await b.close()
    datap.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")

asyncio.run(main())
