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
*, *::before, *::after { animation-duration: 0s !important; animation-delay: 0s !important; transition-duration: 0s !important; transition-delay: 0s !important; }
[data-aos], .wow, .animated, .reveal, .fade-in, .lazyload, .lazyloading { opacity: 1 !important; transform: none !important; visibility: visible !important; }
"""

BLOKY = """(H) => {
  const W = 1440, out = [];
  const vis = (e) => { const s = getComputedStyle(e); return s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0.05; };
  const add = (e, t) => {
    const r = e.getBoundingClientRect();
    const x = Math.max(0, r.left), y = r.top + scrollY, w = Math.min(W, r.right) - x;
    let h = r.height;
    if (w < 40 || h < 14 || y >= H || y + h <= 0 || y < 0 || !vis(e)) return;
    h = Math.min(h, H - y);
    out.push({ t, x: Math.round(x), y: Math.round(y), w: Math.round(w), h: Math.round(h) });
  };
  const head = document.querySelector('header, [role=banner], nav');
  if (head) add(head, 'bar');
  document.querySelectorAll('img, video, iframe, canvas').forEach((e) => { const r = e.getBoundingClientRect(); if (r.width >= 90 && r.height >= 70) add(e, 'media'); });
  let bg = 0;
  document.querySelectorAll('section, div, a, figure').forEach((e) => {
    if (bg > 10) return;
    const r = e.getBoundingClientRect();
    if (r.width < 220 || r.height < 160 || r.height > 1100) return;
    if (getComputedStyle(e).backgroundImage.includes('url(')) { add(e, 'media'); bg++; }
  });
  document.querySelectorAll('h1, h2, h3, h4').forEach((e) => { if (e.innerText.trim().length > 2) add(e, 'text'); });
  document.querySelectorAll('p, li').forEach((e) => { if (e.innerText.trim().length > 45 && !e.querySelector('p, li, img')) add(e, 'text'); });
  document.querySelectorAll('a, button').forEach((e) => {
    const r = e.getBoundingClientRect(), s = getComputedStyle(e);
    const solid = s.backgroundColor !== 'rgba(0, 0, 0, 0)' || parseFloat(s.borderTopWidth) > 0;
    if (solid && r.height >= 30 && r.height <= 84 && r.width >= 80 && r.width <= 420 && e.innerText.trim()) add(e, 'btn');
  });
  // vyhodit duplicity a bloky skoro přes celé okno
  const key = new Set(), res = [];
  for (const b of out) {
    const k = [b.t, Math.round(b.x / 12), Math.round(b.y / 12), Math.round(b.w / 12), Math.round(b.h / 12)].join();
    if (key.has(k)) continue; key.add(k);
    if (b.t !== 'bar' && b.w * b.h > W * H * 0.6) continue;
    res.push(b);
  }
  res.sort((a, b) => (a.t === 'bar' ? -1 : b.t === 'bar' ? 1 : a.y - b.y || a.x - b.x));
  return res.slice(0, 60);
}"""

# cookie lišty a vyskakovací okna: cokoli přilepeného k oknu, co mluví o cookies nebo souhlasu, pryč
LISTY = """() => {
  let n = 0;
  for (const e of document.querySelectorAll('body *')) {
    const s = getComputedStyle(e);
    if (s.position !== 'fixed' && s.position !== 'sticky') continue;
    const t = (e.innerText || '').slice(0, 1500);
    const lista = /cookie|soubory cookies|souhlas|súhlas|consent|gdpr/i.test(t) || (/odmítám|odmítnout|povolit|přijmout|prijať|accept|uložit nastavení/i.test(t) && t.length < 600);
    if (lista && e.getBoundingClientRect().height < innerHeight * 0.7 && !e.querySelector('nav, header') && !e.closest('header')) { e.remove(); n++; }
  }
  document.documentElement.style.overflow = ''; document.body.style.overflow = '';
  return n;
}"""
# líně načítané obrázky načíst hned (nativní lazy i běžné JS knihovny)
NACIST = """() => {
  document.querySelectorAll('img, source, iframe').forEach((e) => {
    if (e.loading === 'lazy') e.loading = 'eager';
    for (const [d, a] of [['data-src', 'src'], ['data-lazy-src', 'src'], ['data-original', 'src'], ['data-srcset', 'srcset'], ['data-lazy-srcset', 'srcset']]) {
      const v = e.getAttribute(d); if (v && e.getAttribute(a) !== v) e.setAttribute(a, v);
    }
  });
  document.querySelectorAll('[data-bg], [data-background-image]').forEach((e) => { const v = e.getAttribute('data-bg') || e.getAttribute('data-background-image'); if (v) e.style.backgroundImage = `url("${v}")`; });
}"""
# počkat, až se obrázky dotáhnou; vrátí počet těch, které se nenačetly
DOCKAT = """async () => {
  const imgs = [...document.images].filter((i) => i.getBoundingClientRect().width > 1);
  await Promise.race([Promise.all(imgs.map((i) => i.complete ? 0 : new Promise((r) => { i.onload = i.onerror = r; }))), new Promise((r) => setTimeout(r, 12000))]);
  return imgs.filter((i) => !i.complete || !i.naturalWidth).length;
}"""

def slug(url):
    return re.sub(r"^www\.", "", re.sub(r"^https?://", "", url).strip("/")).replace(".", "-")

async def snimek(browser, url):
    s = slug(url)
    ctx = await browser.new_context(viewport={"width": W, "height": H}, locale="cs-CZ",
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36")
    pg = await ctx.new_page()
    chyby = []
    pg.on("requestfailed", lambda r: chyby.append(f"FAIL {r.resource_type} {r.url[:110]} {r.failure}"))
    pg.on("response", lambda r: r.status >= 400 and chyby.append(f"{r.status} {r.request.resource_type} {r.url[:110]}"))
    try:
        await pg.goto(url, wait_until="load", timeout=60000)
        await pg.wait_for_timeout(2500)
        # hosting občas vrátí 429 (příliš mnoho požadavků): počkat a načíst znovu, úspěšné soubory už jsou v cache
        for pokus in range(4):
            if not any(c.startswith("429") for c in chyby): break
            print(f"  429, čekám a načítám znovu ({pokus + 1})", flush=True)
            await pg.wait_for_timeout(20000)
            chyby.clear()
            await pg.reload(wait_until="load", timeout=60000)
            await pg.wait_for_timeout(2500)
        await pg.add_style_tag(content=HIDE)
        await pg.evaluate(LISTY)
        meta = await pg.evaluate("""() => ({ title: document.title, desc: (document.querySelector('meta[name=description]')||{}).content || '',
            h1: (document.querySelector('h1')||{}).innerText || '' })""")
        # projet stránku kvůli lazy loadu a animacím při scrollu
        await pg.evaluate(NACIST)
        total = await pg.evaluate("Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)")
        y = 0
        while y < min(total, MAXH):
            await pg.evaluate(f"window.scrollTo(0, {y})"); await pg.wait_for_timeout(500); y += 400
        await pg.evaluate(NACIST)
        await pg.evaluate("window.scrollTo(0, 0)")
        try:
            await pg.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass
        listy = await pg.evaluate(LISTY)
        if listy: print("  odstraněné lišty:", listy, flush=True)
        nenacteno = await pg.evaluate(DOCKAT)
        await pg.wait_for_timeout(800)
        if nenacteno: print("  nenačtené obrázky:", nenacteno, flush=True)
        if nenacteno:
            for c in chyby[:8]: print("   ", c, flush=True)
            print("   ", await pg.evaluate("[...document.images].filter(i => !i.naturalWidth).slice(0, 4).map(i => (i.currentSrc || i.src || '(bez src)').slice(0, 120) + ' | ' + i.outerHTML.slice(0, 160))"), flush=True)
        total = await pg.evaluate("Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)")
        bloky = await pg.evaluate(BLOKY, 1800)
        png = await pg.screenshot(full_page=True, clip={"x": 0, "y": 0, "width": W, "height": min(total, MAXH)})
        im = Image.open(io.BytesIO(png)).convert("RGB")
        im = im.resize((OUTW, round(im.height * OUTW / im.width)), Image.LANCZOS)
        im.save(OUT / f"{s}.webp", "WEBP", quality=72, method=6)
        print("OK", url, im.size, flush=True)
        return s, {"url": url, "w": im.width, "h": im.height, **meta, "bloky": bloky}
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

if __name__ == "__main__":
    asyncio.run(main())
