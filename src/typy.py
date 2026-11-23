"""Generátor prodejních landing pages pro typy webů (/tvorba-webu/<slug>/) a rozcestníku /tvorba-webu/.
Obsah: src/data/typy-webu.py, ikony a skupiny: src/umime.html, náhledy pro sdílení: tools/og.py."""
import html
import json
import re
import runpy
from pathlib import Path

BASE = "/tvorba-webu/"
SITE = "https://webovybalicek.cz"
ICO_SHIELD = '<path d="M10 2.5 3.5 5v5c0 4 2.8 6.6 6.5 7.5 3.7-.9 6.5-3.5 6.5-7.5V5z"/><path d="m7 10 2 2 4-4"/>'
ICO_CLOCK = '<circle cx="10" cy="10" r="7"/><path d="M10 6v4l2.5 2.5"/>'


def e(s):
    return html.escape(s, quote=True)


def em(s):
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", e(s))


def load(src: Path):
    """Typy webů v pořadí panelu Co umíme, doplněné o skupinu, ikonu a krátký popis z panelu."""
    data = runpy.run_path(str(src / "data" / "typy-webu.py"))
    umime = (src / "umime.html").read_text(encoding="utf-8")
    out = []
    for g in re.finditer(r'<section class="sheet-group"><h3 class="sheet-h">(.*?)</h3>(.*?)</section>', umime, re.S):
        for m in re.finditer(r'<li id="typ-([\w-]+)">(<svg.*?</svg>)<div><h4>(.*?)</h4><p>(.*?)</p>', g.group(2), re.S):
            k = m.group(1)
            if k in data["T"]:
                t = dict(data["T"][k], k=k, g=g.group(1), svg=m.group(2), n=html.unescape(re.sub(r"<[^>]+>", "", m.group(3))), d=html.unescape(m.group(4)))
                t["path"] = f"{BASE}{t['s']}/"
                out.append(t)
    return out, data["SVC"]


def ico(svg_inner_or_full):
    if svg_inner_or_full.startswith("<svg"):
        return svg_inner_or_full.replace('class="type-ico"', 'class="pillar-ico"')
    return f'<svg class="pillar-ico" viewBox="0 0 20 20" aria-hidden="true">{svg_inner_or_full}</svg>'


def type_list(items):
    """Dlaždice typů (stejný vzhled jako v panelu Co umíme), celé klikací."""
    li = "".join(
        f'<li class="type-link">{t["svg"]}<div><h3 class="type-h"><a href="{t["path"]}">{e(t["n"])}</a></h3><p>{e(t["d"])}</p></div></li>'
        for t in items)
    return f'<ul class="sheet-types sheet-types--page">{li}</ul>'


def hero(crumbs, title, lead, actions=""):
    cr = "".join(f'<li><a href="{u}">{e(t)}</a></li>' if u else f"<li>{e(t)}</li>" for t, u in crumbs)
    return f'''  <section class="page-hero">
    <div class="wrap">
      <ol class="crumbs">{cr}</ol>
      <h1>{em(title)}</h1>
      <p class="lead">{e(lead)}</p>
      {actions}
    </div>
  </section>
'''


def ld_script(items):
    return "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in items)


def title(kw):
    t = f"{kw} | webovybalicek"
    return t if len(t) <= 62 else kw


def detail(t, by_key, svc):
    s_name, s_price, s_url, s_text = svc[t["svc"]]
    price = t.get("price", s_price)
    actions = ('<p class="hero-actions"><a href="/kontakt/" class="btn btn--primary">Chci nezávaznou nabídku</a>'
               '<a href="#cena" class="btn btn--outline">Kolik to stojí</a></p>')
    body = hero([("Domů", "/"), ("Tvorba webů", BASE), (t["n"], None)], t["h"], t["l"], actions)

    icons = [t["svg"], ICO_SHIELD, ICO_CLOCK]
    benefits = "".join(f'<article class="card pay-card">{ico(icons[i])}<h3>{e(a)}</h3><p>{e(b)}</p></article>'
                       for i, (a, b) in enumerate(t["b"]))
    feats = "".join(f"<li>{e(f)}</li>" for f in t["f"])
    body += f'''  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Přínosy</p><h2>Co vám takový web přinese</h2></div>
      <div class="grid-cards">{benefits}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Funkce</p><h2>Co web umí</h2><p>Funkce vybíráme podle toho, co opravdu využijete. Nic zbytečného, co by web zpomalovalo.</p></div>
      <ul class="feature-grid">{feats}</ul>
    </div>
  </section>
'''
    if t.get("refs") or t.get("dalsi"):
        body += f'''
  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Reference</p><h2>Weby, které jsme postavili</h2></div>
      {{{{shots_pick:{",".join(t["refs"] + t.get("dalsi", []))}|{t["n"]}}}}}
    </div>
  </section>
'''
    faqs = list(t["q"]) + [
        ("Jak tvorba probíhá?", "Začneme analýzou vašeho podnikání a cílů, ta je v ceně každého webu. Pak navrhneme strukturu a design, s pomocí AI připravíme texty a web postavíme. První verzi od AI nikdy nepřebíráme naslepo, vše kontroluje a ladí člověk."),
    ]
    faq_html = "".join(f'<details name="faq"{" open" if i == 0 else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>'
                       for i, (q, a) in enumerate(faqs))
    body += f'''
  <section class="section section--mist" id="cena">
    <div class="wrap split">
      <div class="section-head section-head--sticky">
        <p class="pill">Cena</p>
        <h2>{e(price[0].upper() + price[1:])}</h2>
        <p>Stavíme jako <a href="{s_url}" class="link">{e(s_name)}</a>. {e(s_text)} Přesnou cenu vám pošleme po krátké konzultaci zdarma.</p>
        <p class="hero-actions"><a href="/kontakt/" class="btn btn--primary">Chci nabídku</a><a href="/srovnani/" class="btn btn--outline">Srovnání služeb</a></p>
      </div>
      <div class="accordion">{faq_html}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head section-head--row">
        <div><p class="pill">Další typy webů</p><h2>Mohlo by vás zajímat</h2></div>
        <a href="{BASE}" class="btn btn--outline">Všechny typy webů</a>
      </div>
      {type_list([by_key[k] for k in t["rel"] if k in by_key])}
    </div>
  </section>
'''
    path = t["path"]
    ld = [
        {"@context": "https://schema.org", "@type": "Service", "name": t["kw"], "serviceType": t["n"],
         "description": t["md"], "url": SITE + path, "areaServed": [{"@type": "Country", "name": "Česko"}, {"@type": "Country", "name": "Slovensko"}],
         "provider": {"@type": "Organization", "name": "webovybalicek", "url": SITE + "/"},
         "offers": {"@type": "Offer", "priceCurrency": "CZK", "priceSpecification": {
             "@type": "PriceSpecification", "minPrice": int(re.sub(r"\D", "", price)), "priceCurrency": "CZK"}}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Domů", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Tvorba webů", "item": SITE + BASE},
            {"@type": "ListItem", "position": 3, "name": t["n"], "item": SITE + path}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]
    meta = {"title": title(t["kw"]), "description": t["md"], "path": path, "head": ld_script(ld),
            "image": f"/assets/img/og/{t["s"]}.jpg", "nav": ""}
    return meta, body


def overview(items):
    groups = []
    for g in dict.fromkeys(t["g"] for t in items):
        gid = re.sub(r"[^a-z]+", "-", g.lower().translate(str.maketrans("áčďéěíňóřšťúůýž", "acdeeinorstuuyz"))).strip("-")
        groups.append(f'''  <section class="section{" section--tight" if groups else ""}" id="{gid}">
    <div class="wrap">
      <div class="section-head"><h2>{e(g)}</h2></div>
      {type_list([t for t in items if t["g"] == g])}
    </div>
  </section>
''')
    body = hero([("Domů", "/"), ("Tvorba webů", None)], "Weby pro *každý obor*",
                "Od jednoduché prezentace po portál s platbami a členskou sekcí. Vyberte, jaký web potřebujete, a podívejte se, co umí a kolik stojí.")
    body += "".join(groups)
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "name": "Typy webů, které stavíme",
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t["n"], "url": SITE + t["path"]} for i, t in enumerate(items)]}]
    meta = {"title": "Tvorba webů na míru pro každý obor | webovybalicek",
            "description": "E-shopy, rezervace, kurzy, členské sekce, portály i firemní weby. Podívejte se, jaké weby stavíme s pomocí AI, co umí a kolik stojí.",
            "path": BASE, "head": ld_script(ld), "image": "/assets/img/og/tvorba-webu.jpg", "nav": ""}
    return meta, body


def pages(src: Path):
    items, svc = load(src)
    by_key = {t["k"]: t for t in items}
    return [overview(items)] + [detail(t, by_key, svc) for t in items]
