"""SEO stránky 2: obory (/web-pro-<obor>/ + /web-pro/), řešení problémů (/reseni/<slug>/ + /reseni/)
 Data: src/data/seo-obory.py, seo-reseni.py."""
import runpy

from typy import e, hero, type_list
from seo import ld, crumbs_ld, cta_split, SITE, ORG


def chips_rel(items, label):
    li = "".join(f'<li><a href="{u}">{e(t)}</a></li>' for u, t in items)
    return f'''
  <section class="section section--tight">
    <div class="wrap"><p class="note">{e(label)}</p><ul class="chips">{li}</ul></div>
  </section>
'''


# ---------------------------------------------------------------- obory
def obory(src, by_key):
    O = runpy.run_path(str(src / "data" / "seo-obory.py"))["O"]
    out = []
    for k, x in O.items():
        path = f"/web-pro-{k}/"
        body = hero([("Domů", "/"), ("Weby podle oboru", "/web-pro/"), (x["n"], None)], x["h"], x["l"],
                    '<p class="hero-actions"><a href="/kontakt/" class="btn btn--primary">Chci nezávaznou nabídku</a></p>')
        cards = "".join(f'<article class="card pay-card"><h3>{e(a)}</h3><p>{e(b)}</p></article>' for a, b in x["need"])
        typy = [by_key[t] for t in x["typy"] if t in by_key]
        body += f'''  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">{e(x["kratce"])}</p><h2>Co musí umět web v tomhle oboru</h2></div>
      <div class="grid-cards">{cards}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Reference</p><h2>Weby, které jsme postavili</h2></div>
      {{{{shots_pick:{",".join(x["refs"])}|Reference}}}}
    </div>
  </section>
'''
        if typy:
            body += f'''
  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Související</p><h2>Co pro vás můžeme postavit</h2></div>
      {type_list(typy)}
    </div>
  </section>
'''
        body += cta_split("Časté dotazy", f"{x['kw']}: na co se ptáte",
                          "AI web od 20 000 Kč, prezentační web od 25 000 Kč, e-shop od 35 000 Kč. Přesnou cenu pošleme do 24 hodin.", x["q"])
        body += chips_rel([(f"/web-pro-{o}/", v["n"]) for o, v in O.items() if o != k] + [("/web-pro/", "Všechny obory")], "Další obory:")
        head = ld([{"@context": "https://schema.org", "@type": "Service", "name": x["kw"], "serviceType": "Tvorba webových stránek",
                    "url": SITE + path, "provider": ORG, "description": x["md"], "audience": {"@type": "Audience", "audienceType": x["n"]},
                    "areaServed": {"@type": "Country", "name": "Česko"}},
                   crumbs_ld([("Domů", "/"), ("Weby podle oboru", "/web-pro/"), (x["n"], path)])])
        out.append(({"title": f"{x['kw']} – web na míru od 20 000 Kč | webovybalicek", "description": x["md"], "path": path,
                     "head": head, "nav": "", "og": {"k": "Weby podle oboru", "h": x["h"], "tags": ["Design", "AI", "SEO"]}}, body))

    tiles = "".join(f'<article class="card pay-card"><h3><a href="/web-pro-{k}/" class="link">{e(x["n"])}</a></h3><p>{e(x["l"][:150].rsplit(" ", 1)[0])}…</p></article>'
                    for k, x in O.items())
    body = hero([("Domů", "/"), ("Weby podle oboru", None)], "Weby podle *oboru*",
                "Advokát potřebuje od webu něco jiného než kadeřnictví nebo chata. Vyberte svůj obor a podívejte se, co by váš web měl umět a co jsme pro podobné firmy už postavili.")
    body += f'''  <section class="section">
    <div class="wrap">
      <div class="grid-cards">{tiles}</div>
      <p class="note">Váš obor tu není? Weby stavíme pro všechny obory, <a href="/tvorba-webu/" class="link">podívejte se na typy webů</a> nebo nám <a href="/kontakt/" class="link">napište</a>.</p>
    </div>
  </section>
'''
    out.append(({"title": "Weby podle oboru – advokáti, terapeuti, salony, ubytování | webovybalicek",
                 "description": "Tvorba webů podle oboru: advokáti, terapeuti a kouči, lektoři, kadeřnictví, fotografové, interiéroví designéři, chaty a apartmány. Reference a ceny.",
                 "path": "/web-pro/", "nav": "", "head": ld([crumbs_ld([("Domů", "/"), ("Weby podle oboru", "/web-pro/")])]),
                 "og": {"k": "Weby podle oboru", "h": "Web pro *váš obor*", "tags": ["Advokáti", "Salony", "Ubytování"]}}, body))
    return out


# ---------------------------------------------------------------- řešení
def reseni(src):
    R = runpy.run_path(str(src / "data" / "seo-reseni.py"))["R"]
    out = []
    for k, x in R.items():
        path = f"/reseni/{k}/"
        body = hero([("Domů", "/"), ("Řešíme", "/reseni/"), (x["n"], None)], x["h"], x["l"],
                    '<p class="hero-actions"><a href="/kontakt/" class="btn btn--primary">Chci to vyřešit</a><a href="tel:+420723933774" class="btn btn--outline">723 933 774</a></p>')
        signs = "".join(f"<li>{e(i)}</li>" for i in x["signs"])
        steps = "".join(f'<article class="card pay-card"><p class="pill">{i + 1}. krok</p><h3>{e(a)}</h3><p>{e(b)}</p></article>' for i, (a, b) in enumerate(x["steps"]))
        body += f'''  <section class="section">
    <div class="wrap split">
      <div class="section-head"><p class="pill">Týká se vás to?</p><h2>Poznáte to podle toho, že…</h2></div>
      <div class="card pay-card"><ul class="sv-ticks">{signs}</ul></div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Postup</p><h2>Jak to vyřešíme</h2></div>
      <div class="grid-cards">{steps}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="answer"><p class="pill">Cena</p><p>{e(x["cena"])}</p></div>
    </div>
  </section>
'''
        body += cta_split("Časté dotazy", "Na co se ptáte", "Popište nám v pár větách, co se děje. Ozveme se do 24 hodin s postupem a cenou.", x["q"])
        body += chips_rel(x["links"] + [(f"/reseni/{o}/", v["n"]) for o, v in R.items() if o != k and (x.get("seo_only") or not v.get("seo_only"))], "Související:")
        head = ld([{"@context": "https://schema.org", "@type": "Service", "name": x["n"], "serviceType": x["kw"],
                    "url": SITE + path, "provider": ORG, "description": x["md"], "areaServed": {"@type": "Country", "name": "Česko"}},
                   crumbs_ld([("Domů", "/"), ("Řešíme", "/reseni/"), (x["n"], path)])])
        out.append(({"title": f"{x['kw']} | webovybalicek", "description": x["md"], "path": path, "head": head, "nav": "",
                     "og": {"k": "Řešíme", "h": x["h"], "tags": ["Rychle", "Bez ztráty SEO", "Na míru"]}}, body))

    tiles = "".join(f'<article class="card pay-card"><h3><a href="/reseni/{k}/" class="link">{e(x["n"])}</a></h3><p>{e(x["signs"][0])}.</p></article>'
                    for k, x in R.items() if not x.get("seo_only"))  # seo_only = jen pro SEO, ne v rozcestníku
    body = hero([("Domů", "/"), ("Řešíme", None)], "Co vás s webem *trápí*?",
                "Pomalý web, napadený WordPress, Wix, ze kterého nejde odejít, nebo webař, který přestal odpovídat. Tohle řešíme každý týden.")
    body += f'''  <section class="section">
    <div class="wrap"><div class="grid-cards">{tiles}</div></div>
  </section>
'''
    out.append(({"title": "Řešíme problémy s webem – Wix, redesign, rychlost, napadení | webovybalicek",
                 "description": "Převod z Wixu, redesign, zrychlení WordPressu, napojení Zásilkovny a plateb, oprava napadeného webu a převzetí webu po jiném webaři.",
                 "path": "/reseni/", "nav": "", "head": ld([crumbs_ld([("Domů", "/"), ("Řešíme", "/reseni/")])]),
                 "og": {"k": "Řešíme", "h": "Co vás s webem *trápí*?", "tags": ["Wix", "Rychlost", "Bezpečnost"]}}, body))
    return out


def pages(src, by_key):
    return obory(src, by_key) + reseni(src)
