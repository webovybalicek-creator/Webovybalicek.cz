#!/usr/bin/env python3
"""Náhledy pro osobní dashboard /design/: screenshot horní části každé stránky ze src/data/design.json
do assets/img/design/<slug>.webp. Běží v GitHub Action „Náhledy /design/“.
Bez argumentů dělá jen chybějící náhledy; `--vse` přefotí všechno; jinak slugy (např. mobbin-com)."""
import asyncio, io, json, re, sys
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

sys.path.insert(0, str(Path(__file__).parent))
from snimky import HIDE, LISTY  # schování cookie lišt a popupů – stejně jako u referencí

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/design"
DATA = json.loads((ROOT / "src/data/design.json").read_text(encoding="utf-8"))
W, H, OUTW = 1440, 900, 800


def slug(url):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"^https?://(www\.)?", "", url.lower())).strip("-")


async def foto(browser, url):
    ctx = await browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=1, locale="cs-CZ")
    pg = await ctx.new_page()
    try:
        await pg.goto(url, wait_until="domcontentloaded", timeout=45000)
        try:
            await pg.wait_for_load_state("networkidle", timeout=12000)
        except Exception:
            pass
        await pg.add_style_tag(content=HIDE)
        await pg.evaluate(LISTY)
        await pg.wait_for_timeout(2500)  # dojetí úvodních animací
        png = await pg.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
        im = Image.open(io.BytesIO(png)).convert("RGB")
        im = im.resize((OUTW, round(H * OUTW / W)), Image.LANCZOS)
        im.save(OUT / f"{slug(url)}.webp", "WEBP", quality=74, method=6)
        print("OK", url, flush=True)
    except Exception as e:
        print("CHYBA", url, repr(e)[:200], flush=True)
    finally:
        await ctx.close()


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    args = set(sys.argv[1:])
    vse = "--vse" in args
    jen = args - {"--vse"}
    urls = [i["url"] for items in DATA.values() for i in items if not i.get("img")]
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for url in urls:
            s = slug(url)
            if jen and s not in jen:
                continue
            if not vse and not jen and (OUT / f"{s}.webp").exists():
                continue
            await foto(b, url)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
