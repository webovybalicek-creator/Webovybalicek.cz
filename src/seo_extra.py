"""SEO stránky 2: obory (/web-pro-<obor>/ + /web-pro/), řešení problémů (/reseni/<slug>/ + /reseni/)
a kalkulačka ceny webu (/kalkulacka-ceny-webu/). Data: src/data/seo-obory.py, seo-reseni.py, seo-kalkulacka.py."""
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
                    '<p class="hero-actions"><a href="/kontakt/" class="btn btn--primary">Chci nezávaznou nabídku</a><a href="/kalkulacka-ceny-webu/" class="btn btn--outline">Spočítat cenu</a></p>')
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
                          "AI web od 20 000 Kč, prezentační web od 25 000 Kč, e-shop od 35 000 Kč. Orientační cenu si spočítáte v kalkulačce, přesnou pošleme do 24 hodin.", x["q"])
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
        body += chips_rel(x["links"] + [(f"/reseni/{o}/", v["n"]) for o, v in R.items() if o != k], "Související:")
        head = ld([{"@context": "https://schema.org", "@type": "Service", "name": x["n"], "serviceType": x["kw"],
                    "url": SITE + path, "provider": ORG, "description": x["md"], "areaServed": {"@type": "Country", "name": "Česko"}},
                   crumbs_ld([("Domů", "/"), ("Řešíme", "/reseni/"), (x["n"], path)])])
        out.append(({"title": f"{x['kw']} | webovybalicek", "description": x["md"], "path": path, "head": head, "nav": "",
                     "og": {"k": "Řešíme", "h": x["h"], "tags": ["Rychle", "Bez ztráty SEO", "Na míru"]}}, body))

    tiles = "".join(f'<article class="card pay-card"><h3><a href="/reseni/{k}/" class="link">{e(x["n"])}</a></h3><p>{e(x["signs"][0])}.</p></article>'
                    for k, x in R.items())
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


# ---------------------------------------------------------------- kalkulačka
def kalkulacka(src):
    K = runpy.run_path(str(src / "data" / "seo-kalkulacka.py"))
    kc = lambda n: f"{n:,}".replace(",", " ") + " Kč"
    base = "".join(f'<label class="calc-opt"><input type="radio" name="c-base" value="{k}" data-p="{p}" data-n="{e(n)}"{" checked" if i == 0 else ""}>'
                   f'<span><b>{e(n)}</b><small class="calc-from">od {kc(p)}</small><small>{e(d)}</small></span></label>' for i, (k, n, p, d) in enumerate(K["BASE"]))
    radio = lambda name, items: "".join(f'<label class="calc-chip"><input type="radio" name="{name}" data-p="{p}" data-n="{e(n)}"{" checked" if i == 0 else ""}><span>{e(n)}</span></label>' for i, (n, p) in enumerate(items))
    check = lambda items: "".join(f'<label class="calc-chip"><input type="checkbox" data-p="{p}" data-n="{e(n)}"><span>{e(n)}</span></label>' for n, p in items)
    path = "/kalkulacka-ceny-webu/"
    body = hero([("Domů", "/"), ("Kalkulačka ceny webu", None)], "Kalkulačka *ceny webu*",
                "Naklikejte, co potřebujete, a hned uvidíte orientační cenu. Výběr nám můžete rovnou poslat a do 24 hodin dostanete přesnou nabídku.")
    body += f'''  <section class="section">
    <div class="wrap calc" data-calc data-rush="{K["RUSH"]}">
      <div class="calc-form">
        <fieldset><legend>1. Jaký web potřebujete?</legend><div class="calc-base">{base}</div></fieldset>
        <fieldset><legend>2. Kolik bude mít stránek?</legend><div class="calc-chips">{radio("c-pages", K["PAGES"])}</div></fieldset>
        <fieldset><legend>3. V kolika jazycích?</legend><div class="calc-chips">{radio("c-langs", K["LANGS"])}</div></fieldset>
        <fieldset><legend>4. Funkce navíc</legend><div class="calc-chips">{check(K["FEATURES"])}</div></fieldset>
        <fieldset><legend>5. Obsah a termín</legend><div class="calc-chips">{check(K["CONTENT"])}<label class="calc-chip"><input type="checkbox" data-rush data-n="Potřebuji web rychle"><span>Potřebuji web rychle</span></label></div></fieldset>
      </div>
      <aside class="calc-result" id="cena-vysledek">
        <p class="pill">Orientační cena</p>
        <p class="calc-price" aria-live="polite" data-out>20 000 – 25 000 Kč</p>
        <p class="calc-note">Jednorázově za tvorbu. K tomu doména a hosting zhruba 1 500 až 4 000 Kč ročně, správa webu volitelně od 600 Kč měsíčně.</p>
        <form class="form calc-send" action="#" method="post">
          <div class="form-head"><h2>Chci přesnou cenu</h2><p>Pošleme ji do 24 hodin, nezávazně.</p></div>
          <input type="hidden" name="type" value="ai">
          <label>E-mail <input type="email" name="email" autocomplete="email" required placeholder="vas@email.cz"></label>
          <label>Telefon <input type="tel" name="phone" autocomplete="tel"></label>
          <label>Zpráva <textarea name="message" rows="6"></textarea></label>
          <input type="checkbox" name="urgent" hidden>
          <button type="submit" class="btn btn--primary btn--block">Poslat výběr</button>
        </form>
      </aside>
      <a href="#cena-vysledek" class="calc-bar"><span>Orientačně</span><b data-out>20 000 – 25 000 Kč</b><span class="calc-bar-go">Poslat →</span></a>
    </div>
  </section>
'''
    body += cta_split("Časté dotazy", "Jak kalkulačka počítá", "Kalkulačka ukazuje rozpětí podle toho, co obvykle stavíme. Konečná cena záleží na detailech, proto ji vždy pošleme předem a písemně.", [
        ("Je cena v kalkulačce závazná?", "Ne, je orientační. Přesnou cenu pošleme po krátké konzultaci zdarma a ta už se nemění, pokud se nezmění zadání."),
        ("Co když nevím, co přesně potřebuji?", "Nevadí. Pošlete výběr tak, jak je, a doplňte pár vět o firmě. Na konzultaci doporučíme, co dává smysl."),
        ("Jak se platí?", "Záloha 50 % při objednávce, zbytek po dokončení webu."),
        ("Jsou v ceně i doména a hosting?", "Ne, ty platíte napřímo poskytovateli, bez naší přirážky. Pomůžeme vše vybrat a nastavit.")])
    body += chips_rel([("/kolik-stoji-web/", "Kolik stojí web"), ("/cenik/", "Ceník"), ("/srovnani/", "Jaký web je pro vás?"), ("/web-pro/", "Weby podle oboru")], "Související:")
    head = ld([{"@context": "https://schema.org", "@type": "WebApplication", "name": "Kalkulačka ceny webu", "url": SITE + path,
                "applicationCategory": "BusinessApplication", "operatingSystem": "Web", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CZK"},
                "provider": ORG}, crumbs_ld([("Domů", "/"), ("Kalkulačka ceny webu", path)])])
    return [({"title": "Kalkulačka ceny webu – spočítejte si cenu za minutu | webovybalicek",
              "description": "Kalkulačka ceny webu: vyberte typ webu, počet stránek, jazyky a funkce a hned uvidíte orientační cenu. AI web od 20 000 Kč, e-shop od 35 000 Kč.",
              "path": path, "nav": "", "head": head, "cta": "no",
              "og": {"k": "Kalkulačka", "h": "Kolik bude stát *váš web*?", "pill": "za minutu", "tags": ["AI web", "E-shop", "Cena"]}}, body)]


def pages(src, by_key):
    return obory(src, by_key) + reseni(src) + kalkulacka(src)
