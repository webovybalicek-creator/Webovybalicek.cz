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
src/data/reference.json  všechny reference (názvy/popisy pro landing pages)
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
VERSION = "283"  # zvýšit při změně CSS/JS (cache busting)
STAGING = os.environ.get("STAGING", "1") != "0"

# Google profil (g.page/webovybalicek-cz) – při nové recenzi stačí přepsat tady
# Google Analytics 4 (G-XXXX): prázdné = měření vypnuté. Spustí se jen po souhlasu se statistickými cookies.
GA_ID = ""

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

    data = [r for r in data if r.get("f") or r.get("i")]  # jen recenze s fotkou (i = místo loga/fotky iniciály)
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


# --- náhledy pro sdílení (og:image) – texty pro stránky ze src/pages; LP a pluginy mají meta["og"] ---
# Každá veřejná URL má vlastní obrázek assets/img/og/p/<slug>.jpg (tools/og.py). Nová URL = doplnit sem řádek
# (nebo meta "og") a spustit tools/og.py – vyrenderuje jen chybějící obrázky.
OG_PAGES = {
    "/": ("Tvorba webů s pomocí AI", "Weby, za kterými jsou *výsledky*"),
    "/ai-weby/": ("AI weby", "Web hotový *během dnů*, kontroluje ho člověk"),
    "/cenik/": ("Ceník", "Férové ceny *bez skrytých* poplatků"),
    "/digital-project-manager-consultant/": ("Konzultace · Honza", "Projekt dotažený *k výsledkům*"),
    "/fotograf-a-videomaker/": ("Foto a video · Jakub", "Fotky a video, které *prodávají*"),
    "/jak-probiha-tvorba-webu-a-nase-spoluprace/": ("Spolupráce", "Jak probíhá *tvorba webu*"),
    "/kontakt/": ("Kontakt", "Napište nám, ozveme se *do 24 hodin*"),
    "/nastroje/": ("Nástroje", "Čím *stavíme weby*"),
    "/nejcastejsi-dotazy/": ("Časté dotazy", "Odpovědi na *nejčastější otázky*"),
    "/nejcastejsi-pojmy-ohledne-tvorby-webu/": ("Slovníček", "Pojmy kolem webu *srozumitelně*"),
    "/o-nas/": ("O nás", "Malý tým, *velké výsledky*"),
    "/obsah-cinnosti-pri-tvorbe-webu/": ("Tvorba webu krok za krokem", "Co všechno *obnáší* tvorba webu"),
    "/obchodni-podminky/": ("Právní informace", "Obchodní *podmínky*"),
    "/ochrana-informaci-gdpr/": ("Právní informace", "Ochrana *osobních údajů*"),
    "/zasady-cookies-eu/": ("Právní informace", "Zásady *cookies*"),
    "/recaptcha-navod/": ("Návod", "Jak získat klíče *Google reCAPTCHA*"),
    "/sprava-webu/": ("Správa webu", "Web v bezpečí a *vždy aktuální*"),
    "/srovnani/": ("Srovnání", "AI web, prezentační web, nebo *e-shop*?"),
}


def og_slug(path):
    return path.strip("/").replace("/", "-") or "index"


# --- strukturovaná data pro vyhledávače a AI odpovědi (GEO/AEO) ---
ORG = {
    "@context": "https://schema.org", "@type": "ProfessionalService", "@id": SITE + "/#org",
    "name": "webovybalicek", "url": SITE + "/", "logo": SITE + "/assets/img/brand/wb-avatar-lime.png",
    "image": SITE + "/assets/img/og/default.jpg",
    "description": "Tvorba prezentačních webů a e-shopů pro živnostníky, malé a střední firmy. AI zrychluje práci, kvalitu hlídá člověk.",
    "telephone": "+420723933774", "email": "webovybalicek@gmail.com", "founder": {"@type": "Person", "name": "Vladimír Fischer"},
    "address": {"@type": "PostalAddress", "addressLocality": "Říčany", "postalCode": "251 01", "addressCountry": "CZ"},
    "areaServed": [{"@type": "Country", "name": "Česko"}, {"@type": "Country", "name": "Slovensko"}],
    "taxID": "03051820", "priceRange": "od 25 000 Kč",
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": GOOGLE["rating"].replace(",", "."), "reviewCount": GOOGLE["count"], "bestRating": "5"},
    "sameAs": ["https://g.page/webovybalicek-cz/"],
}
WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#web", "name": "webovybalicek", "url": SITE + "/",
           "inLanguage": "cs", "publisher": {"@id": SITE + "/#org"}}


def ld(items):
    return "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in items)


def faq_ld(body):
    """FAQPage z <details><summary>Otázka</summary>odpověď</details> na stránce."""
    qa = []
    for q, a in re.findall(r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>", body, re.S):
        q = html.unescape(re.sub(r"<[^>]+>", "", q)).strip()
        a = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", a))).strip()
        if q and a:
            qa.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qa} if len(qa) >= 2 else None


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
    cookies = (SRC / "cookies.html").read_text(encoding="utf-8")
    analytics = ("  <script type=\"text/plain\" data-consent=\"analytics\" data-src=\"https://www.googletagmanager.com/gtag/js?id=%s\"></script>\n"
                 "  <script type=\"text/plain\" data-consent=\"analytics\">gtag('js', new Date());gtag('config', '%s');</script>" % (GA_ID, GA_ID)) if GA_ID else ""
    refs = json.loads((SRC / "data" / "reference.json").read_text(encoding="utf-8"))
    reviews = json.loads((SRC / "data" / "recenze.json").read_text(encoding="utf-8"))
    vyber = json.loads((SRC / "data" / "reference-vyber.json").read_text(encoding="utf-8"))
    projekty = json.loads((SRC / "data" / "projekty.json").read_text(encoding="utf-8"))
    snimky_p = SRC / "data" / "reference-snimky.json"
    snimky = json.loads(snimky_p.read_text(encoding="utf-8")) if snimky_p.exists() else {}

    import sys
    sys.path.insert(0, str(SRC))
    import plugins
    import typy

    sources = [parse(page) + (page.stem,) for page in sorted((SRC / "pages").glob("*.html"))]
    sources += [(m, b, "") for m, b in plugins.pages(SRC)]
    sources += [(m, b, "") for m, b in typy.pages(SRC)]

    # reference pro landing pages: výběr z homepage, jinak libovolný web z reference.json (jen se snímkem)
    vyber_by = {r["s"]: r for r in vyber}
    # weby, které nejsou v reference.json (jen pro landing pages): {slug: {u, t, d}}
    lp_extra_p = SRC / "data" / "reference-lp.json"
    lp_extra = json.loads(lp_extra_p.read_text(encoding="utf-8")) if lp_extra_p.exists() else {}
    refs_by = {re.sub(r"^www\.", "", re.sub(r"^https?://", "", r["u"]).strip("/")).replace(".", "-"): r for r in refs}

    def pick(k, label=None):
        if k in vyber_by:
            return vyber_by[k]
        r = refs_by.get(k) or (lp_extra.get(k) if "u" in lp_extra.get(k, {}) else None)
        if not r or k not in snimky:
            return None
        name = re.sub(r"\.(cz|com|eu|sk|nl|hu)$", "", r.get("t", k).split(" /")[0]).replace("-", " ")
        ov = lp_extra.get(k, {})
        return {"s": k, "u": ov.get("u", r["u"]), "n": ov.get("n") or name[:1].upper() + name[1:],
                "d": ov.get("d", r.get("d", "")).rstrip("."), "t": label or ""}

    def shots_pick(keys, label):
        """Reference na landing page: nejdřív weby z homepage, víc než 4 = posuvný pruh jako na homepage."""
        items = [pick(k, label) for k in sorted(dict.fromkeys(keys.split(",")), key=lambda k: k not in vyber_by)]
        items = [r for r in items if r]
        if len(items) > 4:  # pevné pořadí (nejhezčí z homepage první), bez náhodného míchání
            return render_shots(items, snimky).replace('<div class="shots-loop">', '<div class="shots-loop" data-order="fixed">', 1)
        return render_shots(items, snimky, demo=True).replace("shots--demo", "shots--pick")

    urls = []
    pages = []
    og_jobs = []
    for meta, body, stem in sources:
        meta.setdefault("nav", "")
        path = meta.get("path") or ("/" if stem == "index" else f"/{stem}/")
        body = body.replace("{{reviews}}", render_reviews(reviews))
        body = body.replace("{{shots_strip}}", render_shots(vyber, snimky))
        body = body.replace("{{projects}}", render_projects(projekty))
        body = re.sub(r"\{\{shots_pick:([\w,.-]+)(?:\|([^}]*))?\}\}", lambda m: shots_pick(m.group(1), m.group(2)), body)
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
        og_img = f"/assets/img/og/p/{og_slug(path)}.jpg"
        if not meta.get("image") and (ROOT / og_img.lstrip("/")).exists():
            meta["image"] = og_img
        out = out.replace("{{ogimage}}", SITE + meta.get("image", "/assets/img/og/default.jpg"))
        head = meta.get("head", "")
        extra = [ORG, WEBSITE] if path == "/" else []
        if "FAQPage" not in head and meta.get("hidden") != "yes":
            f = faq_ld(body)
            if f:
                extra.append(f)
        out = out.replace("{{head}}", head + ld(extra))
        out = out.replace("{{v}}", VERSION)
        out = out.replace("{{cta}}", "" if meta.get("cta") == "no" else cta)
        out = out.replace("{{content}}", body)
        out = out.replace("{{umime}}", umime)
        out = out.replace("{{cookies}}", cookies)
        out = out.replace("{{analytics}}", analytics)
        hidden = meta.get("hidden") == "yes"  # pracovní stránky: vždy noindex, mimo sitemapu
        if STAGING or hidden:
            out = out.replace("<head>\n", '<head>\n  <meta name="robots" content="noindex, nofollow">\n', 1)

        target = DIST / path.strip("/") / "index.html" if path != "/" else DIST / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(out, encoding="utf-8")
        if not hidden:
            urls.append(path)
            pages.append((path, meta.get("title", ""), meta.get("description", "")))
            og = meta.get("og") or ({"k": OG_PAGES[path][0], "h": OG_PAGES[path][1]} if path in OG_PAGES else None)
            if not og and path != "/404/":
                core = re.split(r" [|–] ", meta.get("title", ""))[0]
                og = {"k": "webovybalicek", "h": core}
            if og:
                og_jobs.append({"slug": og_slug(path), "path": path, **og})
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

    ai_bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended", "Bingbot"]
    robots = ("User-agent: *\nDisallow: /\n" if STAGING else
              "User-agent: *\nAllow: /\nDisallow: /design/\n\n# AI vyhledávače a asistenti – výslovně povoleno\n"
              + "".join(f"User-agent: {b}\n" for b in ai_bots) + "Allow: /\nDisallow: /design/\n\n"
              + f"Sitemap: {SITE}/sitemap.xml\n")
    (ROOT / "tools" / "og-jobs.json").write_text(json.dumps(og_jobs, ensure_ascii=False, indent=1), encoding="utf-8")
    if not STAGING:
        main = [p for p in pages if not p[0].startswith(("/doporucene-pluginy/", "/tvorba-webu/"))]
        lps = [p for p in pages if p[0].startswith("/tvorba-webu/")]
        def line(p):
            return f"- [{p[1].split(' | ')[0]}]({SITE}{p[0]}): {p[2]}"
        llms = ["# webovybalicek", "",
                "> Tvorba prezentačních webů a e-shopů pro živnostníky, malé a střední firmy v Česku a na Slovensku. "
                "AI zrychluje práci, kvalitu hlídá člověk. Prezentační web od 25 000 Kč, e-shop od 35 000 Kč. "
                "Vladimír Fischer, Říčany u Prahy, +420 723 933 774, webovybalicek@gmail.com.", "",
                "## Hlavní stránky", *[line(p) for p in main], "", "## Typy webů", *[line(p) for p in lps], ""]
        (DIST / "llms.txt").write_text("\n".join(llms), encoding="utf-8")
    (DIST / "robots.txt").write_text(robots, encoding="utf-8")
    print(f"Hotovo: {len(urls)} stránek → dist/ ({'staging, noindex' if STAGING else 'produkce'})")


if __name__ == "__main__":
    build()
