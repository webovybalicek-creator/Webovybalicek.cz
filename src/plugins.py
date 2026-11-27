"""Generátor stránek doporučených pluginů (Toret affiliate)."""
import html
import json
import re
from pathlib import Path

REF = "67"
BASE = "/doporucene-pluginy/"

# Partnerské registrace služeb (mimo Toret) – cíle odkazů jsou v src/data/affil.json
EXTRA = {
    "idoklad": ("Registrace do iDokladu", "/go/idoklad/"),
    "comgate": ("Registrace do Comgate", "/go/comgate/"),
    "thepay": ("Registrace do ThePay", "/go/thepay/"),
}

WHY = {
    "doprava": "Napojení na dopravce je věc, kterou na e-shopech řešíme nejčastěji. Pluginy Toret používáme, protože jsou česky, pravidelně se aktualizují podle změn u dopravců a mají rychlou podporu.",
    "platby": "Platební brány od Toretu nasazujeme na e-shopy roky. Spolehlivě mění stavy objednávek, umí refundace a fungují s ostatními pluginy Toret.",
    "fakturace": "Ruční vystavování faktur je zbytečná práce a zdroj chyb. Tyhle pluginy ji za vás udělají automaticky a o účetnictví máte klid.",
    "marketing": "Bez dat se marketing řídí naslepo. Tyhle pluginy dostanou vaše produkty na srovnávače, do e-mailů i do AI vyhledávání a ukážou, co funguje.",
    "eshop": "Drobnosti v pokladně a na produktu rozhodují o tom, jestli zákazník nákup dokončí. Tyhle pluginy řeší legislativu i komfort zákazníka.",
}

EXT_ATTR = 'rel="sponsored noopener" target="_blank"'


def buy_url(p):
    return f"https://toret.cz/produkt/{p['s']}/ref/{REF}/"


def price(p):
    return "zdarma" if not p["p"] else f"{p['p']:,} Kč/rok".replace(",", " ")


def e(s):
    return html.escape(s, quote=True)


def hero(crumbs, title, lead, actions=""):
    cr = "".join(f'<li><a href="{u}">{e(t)}</a></li>' if u else f"<li>{e(t)}</li>" for t, u in crumbs)
    return f'''  <section class="page-hero">
    <div class="wrap">
      <ol class="crumbs">{cr}</ol>
      <h1>{re.sub(r"\*(.+?)\*", r"<em>\1</em>", e(title))}</h1>
      <p class="lead">{e(lead)}</p>
      {actions}
    </div>
  </section>
'''


def plugin_visual(p, cats):
    """Vlastní úvodní obrázek karty v našem brandu (bez cizích obrázků): WooCommerce + název pluginu."""
    cat = cats.get(p["c"], {}).get("n", "")
    return (f'<span class="pv"><span class="pv-cat">{e(cat)}</span>'
            f'<span class="pv-woo">WooCommerce</span><span class="pv-plus" aria-hidden="true">+</span>'
            f'<span class="pv-name">{e(p["n"])}</span></span>')


def card(p, cats):
    return f'''<article class="card plugin" data-cat="{p['c']}">
  <a href="{BASE}{p['u']}/" class="plugin-media" tabindex="-1" aria-hidden="true">{plugin_visual(p, cats)}</a>
  <div class="plugin-head"><h3><a href="{BASE}{p['u']}/" class="plugin-link">{e(p['n'])}</a></h3><span class="plugin-price">{price(p)}</span></div>
  <p>{e(p['t'])}</p>
  <p class="plugin-links"><a href="{BASE}{p['u']}/" class="btn btn--outline btn--sm">Co umí</a><a href="{buy_url(p)}" class="btn btn--ghost btn--sm" {EXT_ATTR}>Koupit</a></p>
</article>'''


def overview(data):
    cats = {c["k"]: c for c in data["categories"]}
    b = data["bundle"]
    bundle_url = f"https://toret.cz/produkt/{b['s']}/ref/{REF}/"
    feats = "".join(f"<li>{e(f)}</li>" for f in b["f"])
    filt = '<button type="button" aria-pressed="true" data-cat="">Vše</button>' + "".join(
        f'<button type="button" aria-pressed="false" data-cat="{c["k"]}">{e(c["n"])}</button>' for c in data["categories"]
    )
    groups = []
    for c in data["categories"]:
        items = [p for p in data["plugins"] if p["c"] == c["k"]]
        groups.append(f'''<div class="plugin-group" data-group="{c['k']}" id="{c['k']}">
  <div class="plugin-group-head"><h2>{e(c['n'])}</h2><p>{e(c['d'])}</p></div>
  <div class="plugins">{''.join(card(p, cats) for p in items)}</div>
</div>''')

    body = hero(
        [("Domů", "/"), ("Doporučené pluginy", None)],
        "Pluginy, které na e-shopech opravdu *používáme*",
        f"Vybrali jsme {len(data['plugins'])} prověřených pluginů od českého vývojáře Toret pro dopravu, platby, fakturaci i marketing. U každého najdete, k čemu je, co umí a pro koho se hodí.",
        f'<p class="hero-actions"><a href="{bundle_url}" class="btn btn--primary" {EXT_ATTR}>Všechny pluginy v balíčku</a><a href="#sleva" class="btn btn--outline">Chci slevový kód</a></p>',
    )
    body += f'''  <section class="section">
    <div class="wrap">
      <div class="sleva" id="sleva">
        <div class="sleva-copy">
          <span class="sleva-tag">Sleva</span>
          <h2>Slevový kód na pluginy Toret</h2>
          <p>Nechte nám e-mail a pošleme vám náš slevový kód, který uplatníte v košíku na toret.cz.</p>
        </div>
        <form class="sleva-form" data-sleva novalidate>
          <label class="sleva-field"><span class="sr-only">E-mail</span><input type="email" name="email" required placeholder="vas@email.cz" autocomplete="email"></label>
          <button type="submit" class="btn btn--primary">Poslat kód</button>
          <p class="sleva-msg" role="status" aria-live="polite"></p>
        </form>
      </div>

      <div class="ref-filter cat-filter" role="group" aria-label="Filtrovat podle kategorie">{filt}</div>
      {''.join(groups)}

      <div class="plugin-group" id="dalsi">
        <div class="plugin-group-head"><h2>Další pluginy, se kterými pracujeme</h2><p>Mimo nabídku Toretu.</p></div>
        <div class="plugins">
          <article class="card plugin"><div class="plugin-head"><h3>Flycart</h3></div><p>Slevy, akce a pravidla cen pro WooCommerce.</p><p class="plugin-links"><a href="/go/flycart/" class="btn btn--outline btn--sm" {EXT_ATTR}>Zobrazit plugin</a></p></article>
          <article class="card plugin"><div class="plugin-head"><h3>LearnDash</h3></div><p>Online kurzy, lekce a testy přímo na WordPressu.</p><p class="plugin-links"><a href="/go/learndash/" class="btn btn--outline btn--sm" {EXT_ATTR}>Zobrazit plugin</a><a href="/go/learndash-registrace/" class="btn btn--ghost btn--sm" {EXT_ATTR}>Registrace</a></p></article>
        </div>
      </div>

      <div class="bundle obsidian bundle--end">
        <div>
          <span class="tag-mono">&lt;Balicek /&gt;</span>
          <h2>{e(b['n'])}</h2>
          <p>{e(b['t'])}</p>
          <ul class="ticks ticks--dark">{feats}</ul>
        </div>
        <div class="bundle-buy">
          <p class="bundle-price"><strong>{f"{b['p']:,}".replace(",", " ")}</strong> Kč/rok</p>
          <a href="{bundle_url}" class="btn btn--primary btn--block" {EXT_ATTR}>Koupit balíček</a>
          <p class="bundle-note">Vyplatí se už od 6 pluginů. S naším slevovým kódem ušetříte ještě víc.</p>
        </div>
      </div>


      <p class="note note--small">Odkazy na této stránce jsou partnerské. Když přes ně nakoupíte, dostaneme malou provizi a vás to nic navíc nestojí. Ceny jsou orientační za roční licenci, aktuální cenu uvidíte na toret.cz.</p>
    </div>
  </section>
'''
    meta = {
        "title": "Doporučené pluginy pro WooCommerce | webovybalicek",
        "description": f"{len(data['plugins'])} prověřených pluginů Toret pro české e-shopy: Zásilkovna, PPL, DPD, platební brány, iDoklad, Fakturoid, XML feedy a další. Sleva až 50 %.",
        "path": BASE,
        "og": {"k": "Doporučené pluginy", "h": "Prověřené pluginy pro *české e-shopy*", "pill": f"{len(data['plugins'])} pluginů",
               "tags": ["WooCommerce", "Doprava", "Platby"]},
    }
    return meta, body


ICO = [
    '<path d="M11.2 2 4.8 11h4.4l-1 7 6.4-9H10.2z"/>',
    '<path d="M3 17h14M5 14V10M9 14V7M13 14V9M17 4l-5 4-3-2-5 4"/><path d="M14 4h3v3"/>',
    '<path d="M10 2.5 3.5 5v5c0 4 2.8 6.6 6.5 7.5 3.7-.9 6.5-3.5 6.5-7.5V5z"/><path d="m7 10 2 2 4-4"/>',
    '<circle cx="10" cy="10" r="7"/><path d="M10 6v4l2.5 2.5"/>',
]


def sleva_block(name, free=False):
    return f'''<div class="sleva sleva--bar" id="sleva">
        <div class="sleva-copy">
          <span class="sleva-tag">Sleva</span>
          <h2>{'Sleva na další pluginy Toret' if free else f'Chcete plugin {e(name)} levněji?'}</h2>
          <p>Nechte nám e-mail a pošleme vám náš slevový kód na pluginy Toret. Uplatníte ho v košíku na toret.cz.</p>
        </div>
        <form class="sleva-form" data-sleva novalidate>
          <label class="sleva-field"><span class="sr-only">E-mail</span><input type="email" name="email" required placeholder="vas@email.cz" autocomplete="email"></label>
          <button type="submit" class="btn btn--primary">Poslat kód</button>
          <p class="sleva-msg" role="status" aria-live="polite"></p>
        </form>
      </div>'''


def seo_title(kw):
    for t in (f"{kw} – funkce, cena a sleva | webovybalicek", f"{kw} – cena a sleva | webovybalicek", f"{kw} – cena a sleva", kw):
        if len(t) <= 62:
            return t
    return kw


def detail(p, data, seo):
    cats = {c["k"]: c for c in data["categories"]}
    cat = cats[p["c"]]
    S = seo.get(p["u"], {})
    kw = S.get("kw", f"{p['n']} pro WooCommerce")
    lead = S.get("lead", p["t"])
    feats = "".join(f"<li>{e(f)}</li>" for f in p["f"])
    extra = ""
    if p["u"] in EXTRA:
        t, u = EXTRA[p["u"]]
        extra = f'<a href="{u}" class="btn btn--outline btn--block" {EXT_ATTR}>{e(t)}</a>'
    related = [x for x in data["plugins"] if x["c"] == p["c"] and x["s"] != p["s"]][:3]
    rel = "".join(card(x, cats) for x in related)
    free = not p["p"]
    cta_label = "Stáhnout zdarma" if free else f"Koupit {p['n']}"
    url = buy_url(p)
    h1 = kw.replace(p["n"], f"*{p['n']}*", 1) if p["n"] in kw else f"*{p['n']}*: {kw}"
    actions = (f'<p class="hero-actions"><a href="{url}" class="btn btn--primary" {EXT_ATTR}>{e(cta_label)}</a>'
               + ('' if free else '<a href="#sleva" class="btn btn--outline">Chci slevový kód</a>') + '</p>')
    body = hero(
        [("Domů", "/"), ("Doporučené pluginy", BASE), (cat["n"], f"{BASE}#{p['c']}"), (p["n"], None)],
        h1, lead, actions,
    )
    benefits = "".join(
        f'<article class="card pay-card"><svg class="pillar-ico" viewBox="0 0 20 20" aria-hidden="true">{ICO[i % 4]}</svg><h3>{e(t)}</h3><p>{e(x)}</p></article>'
        for i, (t, x) in enumerate(S.get("b", [])))
    own = list(S.get("q", []))
    has_price = any("stojí" in q for q, _ in own)
    faqs = own + ([] if has_price else [
        (f"Kolik stojí plugin {p['n']}?",
         "Plugin je zdarma." if free else f"Licence stojí {price(p)} a zahrnuje aktualizace a podporu Toretu. Se slevovým kódem, který vám pošleme, ušetříte.")]) + [
        ("Nainstalujete a nastavíte mi plugin?", "Ano. Plugin vám nainstalujeme, napojíme a nastavíme na míru vašemu e-shopu. Stačí nám napsat."),
        ("Je plugin kompatibilní s Elementorem a dalšími pluginy?", "Pluginy Toret jsou navzájem kompatibilní a fungují s Elementorem, Divi i Gutenbergem. Pravidelně se aktualizují."),
    ]
    faq_html = "".join(f'<details name="faq"{" open" if i == 0 else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>' for i, (q, a) in enumerate(faqs))

    body += f'''  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Přínosy</p><h2>Proč {e(p['n'])} na váš WooCommerce e-shop</h2></div>
      <div class="grid-cards">{benefits}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap with-aside">
      <div class="plugin-detail">
        <h2>K čemu plugin {e(p['n'])} je</h2>
        <p class="plugin-intro">{e(p['i'])}</p>

        <h2>Co plugin umí</h2>
        <ul class="feature-grid">{feats}</ul>

        <h2>Pro koho se hodí</h2>
        <p>{e(p['w'])}</p>

        <div class="why card">
          <span class="card-label">proč ho doporučujeme</span>
          <p>{e(WHY[p['c']])}</p>
        </div>
      </div>

      <aside class="card aside-card buy-card">
        <span class="tag-mono">toret.cz</span>
        <h3>{e(p['n'])}</h3>
        <p class="buy-price"><strong>{price(p)}</strong></p>
        <a href="{url}" class="btn btn--primary btn--block" {EXT_ATTR}>{e(cta_label)}</a>
        {extra}
        <ul class="buy-points">
          <li>Česky a s českou podporou</li>
          <li>Pravidelné aktualizace</li>
          <li>Funguje s ostatními pluginy Toret</li>
        </ul>
        {"" if free else '<p class="buy-note">Chcete slevu? <a href="#sleva" class="link">Pošleme vám slevový kód</a>.</p>'}
      </aside>
    </div>
  </section>

  <section class="section section--mist">
    <div class="wrap split">
      <div class="section-head section-head--sticky">
        <p class="pill">Časté dotazy</p>
        <h2>{e(p['n'])} pro WooCommerce: otázky a odpovědi</h2>
        <p><a href="{url}" class="btn btn--primary" {EXT_ATTR}>{e(cta_label)}</a></p>
      </div>
      <div class="accordion">{faq_html}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head section-head--row">
        <div><h2>Další pluginy: {e(cat['n'].lower())}</h2></div>
        <a href="{BASE}" class="btn btn--outline">Všechny pluginy</a>
      </div>
      <div class="plugins">{rel}</div>
      {sleva_block(p["n"], free)}
      <p class="note note--small">Odkazy jsou partnerské. Když přes ně nakoupíte, dostaneme malou provizi a vás to nic navíc nestojí. Cena je orientační za roční licenci, aktuální uvidíte na toret.cz.</p>
    </div>
  </section>
'''
    path = f"{BASE}{p['u']}/"
    site = "https://webovybalicek.cz"
    ld = [
        {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": f"{p['n']} pro WooCommerce",
         "applicationCategory": "BusinessApplication", "operatingSystem": "WordPress, WooCommerce",
         "description": lead, "url": site + path, "brand": {"@type": "Brand", "name": "Toret"},
         "offers": {"@type": "Offer", "price": str(p["p"] or 0), "priceCurrency": "CZK", "url": url,
                    "availability": "https://schema.org/InStock"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Domů", "item": site + "/"},
            {"@type": "ListItem", "position": 2, "name": "Doporučené pluginy", "item": site + BASE},
            {"@type": "ListItem", "position": 3, "name": p["n"], "item": site + path}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]
    head = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    meta = {
        "title": seo_title(kw),
        "description": S.get("md") or f"{p['t']} {p['i'][:110].rsplit(' ', 1)[0]}…",
        "path": path,
        "head": head,
        "ogtype": "article",
        "nav": "",
        "og": {"k": f"Plugin pro WooCommerce · {cat['n']}", "h": f"*{p['n']}* pro WooCommerce", "pill": "Zdarma" if free else "Sleva až 50 %",
               "tags": ["WooCommerce", "Plugin", "Toret"]},
    }
    return meta, body


def pages(src: Path):
    data = json.loads((src / "data" / "pluginy.json").read_text(encoding="utf-8"))
    out = [overview(data)]
    import runpy
    seo = runpy.run_path(str(src / "data" / "pluginy-seo.py"))["S"]
    out += [detail(p, data, seo) for p in data["plugins"]]
    return out
