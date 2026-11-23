"""SEO stránky: lokality (/tvorba-webu-<mesto>/ + /kde-pusobime/), srovnání (/srovnani/<slug>/, /kolik-stoji-web/)
a samostatné pojmy slovníčku (/slovnicek/<slug>/). Data: src/data/seo-*.py. Každá stránka je prolinkovaná
(patička, rozcestníky, související), žádné osiřelé stránky. Náhledovky z meta["og"] tvoří tools/og.py."""
import html
import json
import re
import runpy
from pathlib import Path

from typy import e, em, hero, type_list, load as load_typy

SITE = "https://webovybalicek.cz"
ORG = {"@id": SITE + "/#org"}


def ld(items):
    return "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in items)


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}


def faq(q, name="faq"):
    body = "".join(f'<details name="{name}"{" open" if i == 0 else ""}><summary>{e(a)}</summary><p>{e(b)}</p></details>'
                   for i, (a, b) in enumerate(q))
    return f'<div class="accordion">{body}</div>'


def slug(s):
    s = s.lower().translate(str.maketrans("áčďéěíňóřšťúůýž", "acdeeinorstuuyz"))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def cta_split(pill, title, text, q):
    return f'''
  <section class="section section--mist">
    <div class="wrap split">
      <div class="section-head section-head--sticky">
        <p class="pill">{e(pill)}</p>
        <h2>{e(title)}</h2>
        <p>{e(text)}</p>
        <p class="hero-actions"><a href="/kontakt/" class="btn btn--primary">Chci nezávaznou nabídku</a><a href="/cenik/" class="btn btn--outline">Ceník</a></p>
      </div>
      {faq(q)}
    </div>
  </section>
'''


# ---------------------------------------------------------------- lokality
def lokality(src, by_key):
    L = runpy.run_path(str(src / "data" / "seo-lokality.py"))["L"]
    out = []
    for k, x in L.items():
        path = f"/tvorba-webu-{k}/"
        body = hero([("Domů", "/"), ("Kde působíme", "/kde-pusobime/"), (x["n"], None)], x["h"], x["l"],
                    '<p class="hero-actions"><a href="/kontakt/" class="btn btn--primary">Domluvit schůzku</a><a href="#cena" class="btn btn--outline">Kolik to stojí</a></p>')
        cards = "".join(f'<article class="card pay-card"><h3>{e(a)}</h3><p>{e(b)}</p></article>' for a, b in x["why"])
        body += f'''  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">{e(x["n"])}</p><h2>Proč webovybalicek {e(x["kde"])}</h2></div>
      <div class="grid-cards">{cards}</div>
      <p class="note">Působíme mimo jiné: {e(x["area"])}.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head section-head--row">
        <div><p class="pill">Co stavíme</p><h2>Weby pro firmy {e(x["kde"])}</h2></div>
        <a href="/tvorba-webu/" class="btn btn--outline">Všechny typy webů</a>
      </div>
      {type_list([by_key[t] for t in x["typy"] if t in by_key])}
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Reference</p><h2>Weby, které jsme postavili</h2></div>
      {{{{shots_pick:{",".join(x["refs"])}|Reference}}}}
    </div>
  </section>
'''
        body += cta_split("Cena", "Web od 20 000 Kč",
                          "AI web od 20 000 Kč, prezentační web na WordPressu od 25 000 Kč, e-shop od 35 000 Kč. Přesnou cenu pošleme po krátké konzultaci zdarma.",
                          x["q"]).replace('section section--mist"', 'section section--mist" id="cena"', 1)
        others = "".join(f'<li><a href="/tvorba-webu-{o}/">{e(v["n"])}</a></li>' for o, v in L.items() if o != k)
        body += f'''
  <section class="section section--tight">
    <div class="wrap"><p class="note">Další lokality:</p><ul class="chips">{others}</ul></div>
  </section>
'''
        head = ld([{"@context": "https://schema.org", "@type": "Service", "name": x["kw"], "serviceType": "Tvorba webových stránek",
                    "url": SITE + path, "provider": ORG, "description": x["md"],
                    "areaServed": {"@type": "AdministrativeArea", "name": x["n"]}},
                   crumbs_ld([("Domů", "/"), ("Kde působíme", "/kde-pusobime/"), (x["n"], path)])])
        out.append(({"title": f"{x['kw']} – weby a e-shopy na míru | webovybalicek", "description": x["md"], "path": path,
                     "head": head, "nav": "", "og": {"k": "Kde působíme", "h": x["h"], "tags": ["Design", "AI", "SEO"]}}, body))

    tiles = "".join(f'<article class="card pay-card"><h3><a href="/tvorba-webu-{k}/" class="link">{e(x["n"])}</a></h3><p>{e(x["area"][:140].rsplit(",", 1)[0])}…</p></article>'
                    for k, x in L.items())
    body = hero([("Domů", "/"), ("Kde působíme", None)], "Kde *působíme*",
                "Sídlíme v Říčanech u Prahy. Weby stavíme pro firmy z celé republiky i ze zahraničí, osobně se nejčastěji potkáváme v Praze a Středočeském kraji.")
    body += f'''  <section class="section">
    <div class="wrap">
      <div class="grid-cards">{tiles}</div>
      <p class="note">Jste odjinud? Spolupráce běží online stejně dobře. <a href="/kontakt/" class="link">Napište nám</a>.</p>
    </div>
  </section>
'''
    out.append(({"title": "Kde působíme – tvorba webů Praha a Středočeský kraj | webovybalicek",
                 "description": "Tvorba webů a e-shopů v Praze, Říčanech, okresech Praha-východ a Praha-západ a ve Středočeském kraji. Osobní schůzka i online spolupráce.",
                 "path": "/kde-pusobime/", "nav": "", "head": ld([crumbs_ld([("Domů", "/"), ("Kde působíme", "/kde-pusobime/")])]),
                 "og": {"k": "Kde působíme", "h": "Praha a *Středočeský kraj*", "tags": ["Osobně", "Online", "Říčany"]}}, body))
    return out


# ---------------------------------------------------------------- srovnání
def table(a, b, rows, us="Web od nás"):
    tr = "".join(f'<tr><th scope="row">{e(r[0])}</th><td data-l="{e(a)}">{e(r[1])}</td><td data-l="{e(b)}">{e(r[2])}</td>'
                 + (f'<td class="is-us" data-l="{e(us)}">{e(r[3])}</td>' if len(r) > 3 else "") + "</tr>" for r in rows)
    has = any(len(r) > 3 for r in rows)
    th_us = f'<th class="is-us"><span class="vs-badge">Doporučujeme</span>{e(us)}</th>' if has else ""
    return f'<div class="vs-wrap"><table class="vs-table{" vs-table--3" if has else ""}"><thead><tr><th></th><th>{e(a)}</th><th>{e(b)}</th>{th_us}</tr></thead><tbody>{tr}</tbody></table></div>'


def srovnani(src):
    D = runpy.run_path(str(src / "data" / "seo-srovnani.py"))
    S, C = D["S"], D["CENA"]
    out = []
    links = [(f"/srovnani/{k}/", f"{x['a']}, nebo {x['b']}?") for k, x in S.items()] + [("/kolik-stoji-web/", "Kolik stojí web?")]
    for k, x in S.items():
        path = f"/srovnani/{k}/"
        body = hero([("Domů", "/"), ("Srovnání", "/srovnani/"), (x["kw"], None)], x["h"], x["l"])
        ticks = lambda items: "".join(f"<li>{e(i)}</li>" for i in items)
        body += f'''  <section class="section">
    <div class="wrap">
      <div class="answer"><p class="pill">Krátká odpověď</p><p>{e(x["verdict"])}</p></div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Srovnání</p><h2>{e(x["a"])}, {e(x["b"])} a web od nás bod po bodu</h2></div>
      {table(x["a"], x["b"], x["rows"])}
      <p class="note">Ceny třetích stran jsou orientační (listopad 2026), aktuální najdete u poskytovatele.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="grid-cards grid-cards--3">
        <article class="card pay-card"><h3>Kdy zvolit {e(x["a"])}</h3><ul class="sv-ticks">{ticks(x["a_when"])}</ul></article>
        <article class="card pay-card"><h3>Kdy zvolit {e(x["b"])}</h3><ul class="sv-ticks">{ticks(x["b_when"])}</ul></article>
        <article class="card pay-card pay-card--us"><p class="pill">Doporučujeme</p><h3>Kdy zvolit nás</h3><ul class="sv-ticks">{ticks(x["us_when"])}</ul><p><a href="/kontakt/" class="btn btn--primary">Chci nezávaznou nabídku</a></p></article>
      </div>
    </div>
  </section>
'''
        body += cta_split("Naše doporučení", "Co doporučujeme my", x["rec"], x["q"])
        rel = "".join(f'<li><a href="{u}">{e(t)}</a></li>' for u, t in links if u != path)
        body += f'''
  <section class="section section--tight">
    <div class="wrap"><p class="note">Další srovnání:</p><ul class="chips">{rel}<li><a href="/srovnani/">AI web, prezentační web, nebo e-shop?</a></li></ul></div>
  </section>
'''
        head = ld([{"@context": "https://schema.org", "@type": "Article", "headline": f"{x['kw']}: srovnání", "description": x["md"],
                    "author": ORG, "publisher": ORG, "inLanguage": "cs", "mainEntityOfPage": SITE + path, "dateModified": "2026-11-23"},
                   crumbs_ld([("Domů", "/"), ("Srovnání", "/srovnani/"), (x["kw"], path)])])
        out.append(({"title": f"{x['kw']}: co vybrat v roce 2026 | webovybalicek", "description": x["md"], "path": path, "head": head,
                     "ogtype": "article", "nav": "", "og": {"k": x["k"], "h": x["h"], "tags": [x["a"], "vs", x["b"]]}}, body))

    # kolik stojí web
    path = "/kolik-stoji-web/"
    body = hero([("Domů", "/"), ("Kolik stojí web", None)], C["h"], C["l"],
                '<p class="hero-actions"><a href="/kontakt/" class="btn btn--primary">Chci cenu na míru</a><a href="/cenik/" class="btn btn--outline">Ceník</a></p>')
    one = "".join(f'<article class="card pay-card"><p class="pill">{e(p)}</p><h3><a href="{u}" class="link">{e(n)}</a></h3><p>{e(t)}</p></article>' for n, p, t, u in C["one"])
    yr = "".join(f"<tr><th scope=\"row\">{e(a)}</th><td>{e(b)}</td></tr>" for a, b in C["yearly"])
    fac = "".join(f'<article class="card pay-card"><h3>{e(a)}</h3><p>{e(b)}</p></article>' for a, b in C["factors"])
    body += f'''  <section class="section">
    <div class="wrap">
      <div class="answer"><p class="pill">Krátká odpověď</p><p>{e(C["verdict"])}</p></div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Jednorázově</p><h2>Cena za tvorbu webu</h2></div>
      <div class="grid-cards">{one}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Každý rok</p><h2>Provozní náklady</h2><p>Platíte je dodavatelům napřímo, bez naší přirážky.</p></div>
      <div class="vs-wrap"><table class="vs-table vs-table--2"><tbody>{yr}</tbody></table></div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Co ovlivňuje cenu</p><h2>Proč jeden web stojí víc než jiný</h2></div>
      <div class="grid-cards">{fac}</div>
    </div>
  </section>
'''
    body += cta_split("Časté dotazy", "Na co se ptáte", "Pošlete nám pár vět o tom, co potřebujete, a do 24 hodin dostanete odhad ceny.", C["q"])
    rel = "".join(f'<li><a href="{u}">{e(t)}</a></li>' for u, t in links if u != path)
    body += f'''
  <section class="section section--tight">
    <div class="wrap"><p class="note">Srovnání:</p><ul class="chips">{rel}</ul></div>
  </section>
'''
    head = ld([{"@context": "https://schema.org", "@type": "Article", "headline": "Kolik stojí web v roce 2026", "description": C["md"],
                "author": ORG, "publisher": ORG, "inLanguage": "cs", "mainEntityOfPage": SITE + path, "dateModified": "2026-11-23"},
               crumbs_ld([("Domů", "/"), ("Kolik stojí web", path)])])
    out.append(({"title": "Kolik stojí web v roce 2026? Ceny a náklady | webovybalicek", "description": C["md"], "path": path, "head": head,
                 "ogtype": "article", "nav": "", "og": {"k": "Ceny 2026", "h": "Kolik stojí *web*?", "pill": "od 20 000 Kč", "tags": ["Web", "Doména", "Hosting"]}}, body))
    return out


# ---------------------------------------------------------------- slovníček
def glossary_terms(src):
    page = (src / "pages" / "nejcastejsi-pojmy-ohledne-tvorby-webu.html").read_text(encoding="utf-8")
    return [(html.unescape(re.sub(r"<[^>]+>", "", dt)), html.unescape(re.sub(r"<[^>]+>", "", dd)))
            for dt, dd in re.findall(r"<dt>(.*?)</dt><dd>(.*?)</dd>", page)]


def pojmy(src):
    P = runpy.run_path(str(src / "data" / "seo-pojmy.py"))["P"]
    terms = glossary_terms(src)
    names = {slug(n): n for n, _ in terms}
    proper = {"WordPress", "Zásilkovna", "Google Analytics", "Hotjar"}
    out = []
    for n, d in terms:
        s = slug(n)
        ln = n if n in proper or (len(n) > 1 and n[1].isupper()) else n[0].lower() + n[1:]
        x = P.get(s)
        if not x:
            continue
        path = f"/slovnicek/{s}/"
        paras = "".join(f"<p>{e(p)}</p>" for p in x["p"])
        rel = "".join(f'<li><a href="/slovnicek/{r}/">{e(names.get(r, r))}</a></li>' for r in x["rel"] if r in names)
        link = f'<p><a href="{x["link"][1]}" class="link">{e(x["link"][0])} →</a></p>' if x.get("link") else ""
        body = hero([("Domů", "/"), ("Slovníček pojmů", "/nejcastejsi-pojmy-ohledne-tvorby-webu/"), (n, None)], f"Co je *{ln}*", d)
        body += f'''  <section class="section">
    <div class="wrap split">
      <div class="prose">
        <h2>{e(n)} srozumitelně</h2>
        {paras}
      </div>
      <aside class="answer">
        <p class="pill">Jak to řešíme my</p>
        <p>{e(x["tip"])}</p>
        {link}
      </aside>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap"><p class="note">Související pojmy:</p><ul class="chips">{rel}<li><a href="/nejcastejsi-pojmy-ohledne-tvorby-webu/">Celý slovníček</a></li></ul></div>
  </section>
'''
        head = ld([{"@context": "https://schema.org", "@type": "DefinedTerm", "name": n, "description": d, "url": SITE + path,
                    "inDefinedTermSet": {"@type": "DefinedTermSet", "name": "Slovníček pojmů kolem tvorby webu",
                                         "url": SITE + "/nejcastejsi-pojmy-ohledne-tvorby-webu/"}},
                   crumbs_ld([("Domů", "/"), ("Slovníček pojmů", "/nejcastejsi-pojmy-ohledne-tvorby-webu/"), (n, path)])])
        out.append(({"title": f"Co je {ln}? Vysvětlení srozumitelně | webovybalicek", "description": f"{d[:150].rsplit(' ', 1)[0]}…" if len(d) > 155 else d,
                     "path": path, "head": head, "ogtype": "article", "nav": "",
                     "og": {"k": "Slovníček pojmů", "h": f"Co je *{ln}*?", "tags": ["Web", "Pojem", "Srozumitelně"]}}, body))
    return out


def pages(src: Path):
    items, _ = load_typy(src)
    by_key = {t["k"]: t for t in items}
    return lokality(src, by_key) + srovnani(src) + pojmy(src)
