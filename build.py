#!/usr/bin/env python3
"""
Jednoduchý build statického webu.

src/layout.html        společná kostra (hlavička, patička)
src/cta.html           závěrečná výzva, vkládá se na konec stránek (lze vypnout `cta: no`)
src/pages/*.html       obsah stránek s hlavičkou v HTML komentáři:
                       <!--
                       title: Titulek stránky
                       description: Meta popis
                       path: /cenik/
                       nav: cenik
                       cta: no
                       -->
src/data/reference.json  data referencí → značka {{references}}
assets/                kopíruje se beze změny

Výstup: dist/  (deploy na FTP)
Proměnná prostředí STAGING=0 vypne noindex (pro ostrou doménu).
"""
import html
import json
import os
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
SITE = "https://webovybalicek.cz"
VERSION = "20"  # zvýšit při změně CSS/JS (cache busting)
STAGING = os.environ.get("STAGING", "1") != "0"

FRONT = re.compile(r"^\s*<!--(.*?)-->\s*", re.S)


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    meta = {}
    m = FRONT.match(text)
    if m:
        for line in m.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text


def render_references(data):
    items = []
    for r in data:
        url = r["u"] or "#"
        host = re.sub(r"^https?://(www\.)?", "", url).rstrip("/")
        items.append(
            f'<li data-year="{r["y"]}"><a class="card ref" href="{html.escape(url)}" rel="noopener" target="_blank">'
            f'<span class="ref-top"><span class="ref-url">{html.escape(r["t"])}</span>'
            f'<span class="mono">{r["y"]}</span></span>'
            f'<span class="ref-desc">{html.escape(r["d"])}</span>'
            f'<span class="ref-host">{html.escape(host)}</span></a></li>'
        )
    years = sorted({r["y"] for r in data}, reverse=True)
    filters = '<button type="button" aria-pressed="true" data-year="">Vše</button>' + "".join(
        f'<button type="button" aria-pressed="false" data-year="{y}">{y}</button>' for y in years
    )
    return (
        f'<div class="ref-filter" role="group" aria-label="Filtrovat podle roku">{filters}</div>'
        f'<ul class="refs refs--all" data-ref-list>{"".join(items)}</ul>'
    )


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(ROOT / "assets", DIST / "assets")

    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    cta = (SRC / "cta.html").read_text(encoding="utf-8")
    refs = json.loads((SRC / "data" / "reference.json").read_text(encoding="utf-8"))

    import sys
    sys.path.insert(0, str(SRC))
    import plugins

    sources = [parse(page) + (page.stem,) for page in sorted((SRC / "pages").glob("*.html"))]
    sources += [(m, b, "") for m, b in plugins.pages(SRC)]

    urls = []
    for meta, body, stem in sources:
        meta.setdefault("nav", "")
        path = meta.get("path") or ("/" if stem == "index" else f"/{stem}/")
        body = body.replace("{{references}}", render_references(refs))
        body = body.replace("{{ref_count}}", str(len(refs)))
        body = body.replace("{{v}}", VERSION)

        out = layout
        nav = meta.get("nav", "")
        out = re.sub(r"\{\{nav:([\w-]+)\}\}", lambda m: ' aria-current="page"' if m.group(1) == nav else "", out)
        out = out.replace("{{title}}", html.escape(meta.get("title", "Webový balíček")))
        out = out.replace("{{description}}", html.escape(meta.get("description", "")))
        out = out.replace("{{path}}", path)
        out = out.replace("{{v}}", VERSION)
        out = out.replace("{{cta}}", "" if meta.get("cta") == "no" else cta)
        out = out.replace("{{content}}", body)
        if STAGING:
            out = out.replace("<head>\n", '<head>\n  <meta name="robots" content="noindex, nofollow">\n', 1)

        target = DIST / path.strip("/") / "index.html" if path != "/" else DIST / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(out, encoding="utf-8")
        urls.append(path)
        print(f"  {path}")

    today = date.today().isoformat()
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls]
    sitemap.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")

    robots = "User-agent: *\nDisallow: /\n" if STAGING else f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"
    (DIST / "robots.txt").write_text(robots, encoding="utf-8")
    print(f"Hotovo: {len(urls)} stránek → dist/ ({'staging, noindex' if STAGING else 'produkce'})")


if __name__ == "__main__":
    build()
