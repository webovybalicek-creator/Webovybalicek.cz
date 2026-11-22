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
src/data/klienti.json    loga klientů → značka {{clients}} (soubory v assets/img/klienti/)
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
VERSION = "238"  # zvýšit při změně CSS/JS (cache busting)
STAGING = os.environ.get("STAGING", "1") != "0"

# Google profil (g.page/webovybalicek-cz) – při nové recenzi stačí přepsat tady
GOOGLE = {"rating": "4,8", "count": 24, "since": 2019}


def roky(n):
    return f"{n} rok" if n == 1 else f"{n} roky" if 2 <= n <= 4 else f"{n} let"


def recenze(n):
    return f"{n} recenze" if 2 <= n <= 4 else f"{n} recenzí"

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


LOCK = '<svg class="shot-lock" viewBox="0 0 12 12" aria-hidden="true"><path d="M3.5 5V3.6a2.5 2.5 0 0 1 5 0V5M2.6 5h6.8v5H2.6z" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg>'


def render_projects(items):
    """Vybrané projekty jako harmonika (main.js, [data-proj]). Prázdná pole (text, číslo) se nevypíšou;
    zavřený pruh = screenshot webu, otevřená karta = fotka z assets/img/projekty/ (pole foto)."""
    out = []
    for i, r in enumerate(items):
        img = f"/assets/img/reference/{r['s']}.webp?v={VERSION}"
        foto = (f'<img class="proj-photo" src="/assets/img/projekty/{html.escape(r["foto"])}?v={VERSION}" alt="" decoding="async">'
                if r.get("foto") else "")
        tags = "".join(f"<li>{html.escape(t)}</li>" for t in r.get("tags", []))
        txt = f'<p class="proj-text">{html.escape(r["p"])}</p>' if r.get("p") else ""
        stat = (f'<p class="proj-stat"><strong>{html.escape(r["num"])}</strong><span>{html.escape(r["lbl"])}</span></p>'
                if r.get("num") else "")
        out.append(
            f'<li class="proj{" is-open" if i == 0 else ""}" tabindex="0" aria-label="{html.escape(r["n"])}">'
            f'<img src="{img}" alt="" loading="lazy" decoding="async">{foto}<span class="proj-shade"></span>'
            f'<span class="proj-num">{i + 1:02d}</span><span class="proj-side">{html.escape(r["n"])}</span>'
            f'<div class="proj-body"><ul class="proj-tags">{tags}</ul><h3>{html.escape(r["h"])}</h3>{txt}{stat}'
            f'<a class="link-utility" href="{html.escape(r["u"])}" target="_blank" rel="noopener">Otevřít {html.escape(r["n"])}</a></div></li>'
        )
    return f'<ul class="projs" data-proj>{"".join(out)}</ul>'


def render_shots(vyber, snimky, limit=None, big=False, demo=False):
    """Okna s dlouhým snímkem webu, který se sám pomalu posouvá (main.js, [data-shot])."""
    out = []
    for r in vyber[:limit]:
        # první okna v pruhu jsou vidět hned, načíst je bez čekání; ostatní až u obrazovky
        lazy = 'loading="lazy" ' if big or demo or len(out) >= 6 else 'fetchpriority="high" ' if len(out) < 4 else ""
        m = snimky.get(r["s"])
        if not m or m["h"] < 900:
            continue
        host = re.sub(r"^www\.", "", re.sub(r"^https?://", "", r["u"]).strip("/"))
        typ = {"bar": "b", "media": "m", "text": "t", "btn": "k"}
        bloky = html.escape(json.dumps([[typ[b["t"]], b["x"], b["y"], b["w"], b["h"]] for b in m.get("bloky", [])], separators=(",", ":")))
        out.append(
            f'<li><a class="shot" href="{html.escape(r["u"])}" target="_blank" rel="noopener" data-shot data-blocks="{bloky}">'
            f'<span class="shot-frame"><span class="shot-bar"><i></i><i></i><i></i><b>{LOCK}{html.escape(host)}</b><s aria-hidden="true" data-t="{html.escape(r["t"])}">↗</s></span>'
            f'<span class="shot-win"><img src="/assets/img/reference/{r["s"]}.webp?v={VERSION}" width="{m["w"]}" height="{m["h"]}" '
            f'{lazy}decoding="async" alt="Náhled webu {html.escape(host)}"><u class="shot-type" aria-hidden="true">{html.escape(r["t"])}</u></span></span>'
            f'<span class="shot-meta"><strong>{html.escape(r["n"])}</strong><em>{html.escape(r["t"])}</em>'
            f'<span>{html.escape(r["d"])}</span></span></a></li>'
        )
    if demo:
        return f'<ul class="shots shots--demo">{"".join(out)}</ul>'
    if big:
        return f'<ul class="shots shots--grid">{"".join(out)}</ul>'
    # pruh: nekonečná smyčka od kraje do kraje – druhá kopie jen pro plynulé navázání
    items = "".join(out)
    kopie = items.replace("<a ", '<a tabindex="-1" ').replace(' fetchpriority="high"', ' loading="lazy"')
    return (f'<div class="shots-loop"><ul class="shots shots--strip">{items}</ul>'
            f'<ul class="shots shots--strip" aria-hidden="true">{kopie}</ul></div>')


def render_clients(data):
    """Pás log klientů: dvě stejné řady za sebou, aby se posun plynule opakoval."""
    items = []
    for c in data:
        ratio = c["w"] / c["h"]
        # opticky vyrovnaná velikost: široká loga nižší, vysoká vyšší (stejná plocha)
        # "s" v klienti.json dorovnává váhu kresby: tučná loga < 1, tenká > 1
        height = round(25 * (4 / ratio) ** 0.5 * c.get("s", 1))
        items.append(
            f'<li><span class="logo-tile"><span class="logo-mark" style="--src:url(/assets/img/klienti/{c["f"]}.svg)"><img src="/assets/img/klienti/{c["f"]}.svg" alt="{html.escape(c["n"])}" '
            f'width="{round(height * ratio)}" height="{height}" style="--h:{height / 16:g}em" '
            f'loading="lazy" decoding="async"></span></span></li>'
        )
    row = "".join(items)
    return (
        '<div class="logos" role="group" aria-label="Naši klienti">'
        f'<ul class="logos-track">{row}</ul>'
        f'<ul class="logos-track" aria-hidden="true">{re.sub(r'alt="[^"]*"', 'alt=""', row)}</ul>'
        "</div>"
    )


def render_reviews(data):
    """Pás recenzí z Googlu: miniatura (f = soubor v assets/img/recenze/, jinak iniciály), jméno, hvězdy, text.
    Od 8 recenzí dvě řady proti sobě, jinak jedna."""
    def card(r):
        initials = "".join(w[0] for w in r["n"].split()[:2])
        src = r["f"] if r.get("f", "").startswith("http") else f'/assets/img/recenze/{r.get("f", "")}'
        # při nedostupné fotce z Googlu se ukážou iniciály
        face = (f'<img src="{html.escape(src)}" alt="" width="24" height="24" decoding="async" referrerpolicy="no-referrer" '
                f'onerror="this.replaceWith(Object.assign(document.createElement(\'span\'),{{textContent:\'{html.escape(initials)}\'}}))">'
                if r.get("f") else f'<span aria-hidden="true">{html.escape(initials)}</span>')
        stars = "★" * r.get("s", 5)
        return (f'<li><figure class="review"><blockquote>{html.escape(r["t"])}</blockquote>'
                f'<figcaption><span class="review-face">{face}</span><span class="review-name">{html.escape(r["n"])}</span>'
                f'<span class="review-stars" aria-label="{r.get("s", 5)} z 5">{stars}</span></figcaption></figure></li>')

    def row(items, reverse=False):
        cards = "".join(card(r) for r in items)
        dup = re.sub(r'aria-label="[^"]*"', "", cards)
        cls = "reviews-row reviews-row--rev" if reverse else "reviews-row"
        return (f'<div class="{cls}"><ul class="reviews-track">{cards}</ul>'
                f'<ul class="reviews-track" aria-hidden="true">{dup}</ul></div>')

    data = [r for r in data if r.get("f")]  # jen recenze s fotkou
    if not data:
        return ""
    if len(data) >= 8:
        half = (len(data) + 1) // 2
        rows = row(data[:half]) + row(data[half:], reverse=True)
    else:
        rows = row(data)
    return f'<div class="reviews" role="group" aria-label="Recenze klientů na Googlu">{rows}</div>'


def design_data():
    """Data pro /design/ – doplní cestu k náhledu, pokud existuje (assets/img/design/<slug>.webp)."""
    data = json.loads((SRC / "data" / "design.json").read_text(encoding="utf-8"))
    for items in data.values():
        for i in items:
            s = re.sub(r"[^a-z0-9]+", "-", re.sub(r"^https?://(www\.)?", "", i["url"].lower())).strip("-")
            if not i.get("img") and (ROOT / "assets/img/design" / f"{s}.webp").exists():
                i["img"] = f"/assets/img/design/{s}.webp"
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")



def page_jumps(body):
    """Úvod podstránky (design D): pod perex přidá rychlé skoky na hlavní nadpisy stránky.
    Jen když úvod nemá vlastní tlačítka/skoky a stránka má aspoň 2 nadpisy h2."""
    m = re.search(r'(<section class="page-hero"[^>]*>.*?)(\n    </div>\n  </section>)', body, re.S)
    if not m or 'hero-actions' in m.group(1) or 'page-jump' in m.group(1) or 'data-nojump' in m.group(1):
        return body
    heads = re.findall(r'<h2(?: id="([^"]+)")?>(.*?)</h2>', body[m.end():])
    if len(heads) < 2:
        return body
    links, rest = [], body[m.end():]
    for hid, text in heads[:6]:
        if not hid:
            hid = re.sub(r'[^a-z0-9]+', '-', text.lower().translate(str.maketrans('áčďéěíňóřšťúůýž', 'acdeeinorstuuyz'))).strip('-')
            rest = rest.replace(f'<h2>{text}</h2>', f'<h2 id="{hid}">{text}</h2>', 1)
        links.append(f'<li><a href="#{hid}" class="btn btn--outline btn--sm">{re.sub(r"<[^>]+>", "", text)}</a></li>')
    jump = f'\n      <ul class="page-jump">{"".join(links)}</ul>'
    return body[:m.start()] + m.group(1) + jump + m.group(2) + rest

def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(ROOT / "assets", DIST / "assets")
    # soubory do kořene webu (PHP pro formulář, .htaccess)
    for f in (ROOT / "static").iterdir():
        shutil.copy2(f, DIST / f.name)

    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    cta = (SRC / "cta.html").read_text(encoding="utf-8")
    umime = (SRC / "umime.html").read_text(encoding="utf-8")
    refs = json.loads((SRC / "data" / "reference.json").read_text(encoding="utf-8"))
    clients = json.loads((SRC / "data" / "klienti.json").read_text(encoding="utf-8"))
    reviews = json.loads((SRC / "data" / "recenze.json").read_text(encoding="utf-8"))
    vyber = json.loads((SRC / "data" / "reference-vyber.json").read_text(encoding="utf-8"))
    projekty = json.loads((SRC / "data" / "projekty.json").read_text(encoding="utf-8"))
    snimky_p = SRC / "data" / "reference-snimky.json"
    snimky = json.loads(snimky_p.read_text(encoding="utf-8")) if snimky_p.exists() else {}

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
        body = body.replace("{{clients}}", render_clients(clients))
        body = body.replace("{{reviews}}", render_reviews(reviews))
        body = body.replace("{{shots_strip}}", render_shots(vyber, snimky))
        body = body.replace("{{projects}}", render_projects(projekty))
        body = body.replace("{{shots_demo}}", render_shots(vyber, snimky, limit=4, demo=True))
        body = body.replace("{{shots_grid}}", render_shots(vyber, snimky, limit=6, big=True))
        years = date.today().year - GOOGLE["since"]
        body = body.replace("{{g_rating}}", GOOGLE["rating"])
        body = body.replace("{{g_count}}", recenze(GOOGLE["count"]))
        body = body.replace("{{g_since}}", str(GOOGLE["since"]))
        body = body.replace("{{g_years}}", roky(years))
        body = body.replace("{{v}}", VERSION)
        body = page_jumps(body)

        if meta.get("layout") == "none":  # samostatná stránka bez hlavičky/patičky webu (např. /design/)
            target = DIST / path.strip("/") / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            body = body.replace("{{design_data}}", design_data())
            target.write_text(body.replace("{{v}}", VERSION), encoding="utf-8")
            print(f"  {path} (samostatná, noindex)")
            continue

        out = layout
        nav = meta.get("nav", "")
        out = re.sub(r"\{\{nav:([\w-]+)\}\}", lambda m: ' aria-current="page"' if m.group(1) == nav else "", out)
        out = out.replace("{{title}}", html.escape(meta.get("title", "webovybalicek")))
        out = out.replace("{{description}}", html.escape(meta.get("description", "")))
        out = out.replace("{{path}}", path)
        out = out.replace("{{ogtype}}", meta.get("ogtype", "website"))
        out = out.replace("{{head}}", meta.get("head", ""))
        out = out.replace("{{v}}", VERSION)
        out = out.replace("{{cta}}", "" if meta.get("cta") == "no" else cta)
        out = out.replace("{{content}}", body)
        out = out.replace("{{umime}}", umime)
        hidden = meta.get("hidden") == "yes"  # pracovní stránky: vždy noindex, mimo sitemapu
        if STAGING or hidden:
            out = out.replace("<head>\n", '<head>\n  <meta name="robots" content="noindex, nofollow">\n', 1)

        target = DIST / path.strip("/") / "index.html" if path != "/" else DIST / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(out, encoding="utf-8")
        if not hidden:
            urls.append(path)
        print(f"  {path}")

    # stránka 404 i jako /404.html (ErrorDocument v .htaccess)
    if (DIST / "404" / "index.html").exists():
        shutil.copy2(DIST / "404" / "index.html", DIST / "404.html")

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
