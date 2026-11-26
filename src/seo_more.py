"""SEO stránky 3 (25. 11. 2026, obsahový plán pro poptávky):
- /kontrola-webu-zdarma/          lead magnet s formulářem (type=kontrola, pole site)
- /kolik-stoji-e-shop/, /kolik-stoji-sprava-webu/, /kolik-stoji-redesign-webu/
- /geo-optimalizace/              web v odpovědích ChatGPT a Google AI
- /spoluprace-pro-agentury/       white-label a subdodávky pro agentury a freelancery
- /projekty/ + /projekty/<slug>/  případové studie (data src/data/pripadovky.py – jen ověřená fakta, žádná vymyšlená čísla)
Každá stránka je prolinkovaná (patička, rozcestníky, související)."""
import runpy

from typy import e, em, hero
from seo import ld, crumbs_ld, cta_split, faq, SITE, ORG
from seo_extra import chips_rel

ACTIONS = '<p class="hero-actions"><a href="/kontakt/" class="btn btn--primary">Chci nezávaznou nabídku</a></p>'


def cards(items, cls="grid-cards"):
    return f'<div class="{cls}">' + "".join(f'<article class="card pay-card"><h3>{e(a)}</h3><p>{e(b)}</p></article>' for a, b in items) + "</div>"


def ticks(items):
    return '<ul class="sv-ticks">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def section(pill, title, inner, lead=""):
    lead = f"<p>{e(lead)}</p>" if lead else ""
    return f'''  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">{e(pill)}</p><h2>{e(title)}</h2>{lead}</div>
      {inner}
    </div>
  </section>
'''


def answer(pill, text):
    return f'''  <section class="section">
    <div class="wrap"><div class="answer"><p class="pill">{e(pill)}</p><p>{e(text)}</p></div></div>
  </section>
'''


def lead_form(title, sub, type_, msg_ph, site=True, button="Odeslat"):
    site_f = '<label>Adresa webu <input type="url" name="site" required placeholder="https://"></label>' if site else ""
    return f'''<form class="form" action="#" method="post">
          <div class="form-head"><h2>{e(title)}</h2><p>{e(sub)}</p></div>
          <input type="hidden" name="type" value="{type_}">
          {site_f}
          <label>Jméno <input type="text" name="name" autocomplete="name"></label>
          <label>E-mail <input type="email" name="email" autocomplete="email" required placeholder="vas@email.cz"></label>
          <label>Telefon <input type="tel" name="phone" autocomplete="tel"></label>
          <label>Zpráva <textarea name="message" rows="4" placeholder="{e(msg_ph)}"></textarea></label>
          <button type="submit" class="btn btn--primary btn--block">{e(button)}</button>
        </form>'''


def service_ld(name, path, desc, crumbs, stype="Tvorba webových stránek"):
    return ld([{"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": stype, "url": SITE + path,
                "provider": ORG, "description": desc, "areaServed": {"@type": "Country", "name": "Česko"}}, crumbs_ld(crumbs)])


def article_ld(headline, path, desc, crumbs):
    return ld([{"@context": "https://schema.org", "@type": "Article", "headline": headline, "description": desc, "author": ORG,
                "publisher": ORG, "inLanguage": "cs", "mainEntityOfPage": SITE + path, "dateModified": "2026-11-25"}, crumbs_ld(crumbs)])


# ---------------------------------------------------------------- kontrola webu zdarma
def kontrola():
    path = "/kontrola-webu-zdarma/"
    md = "Kontrola webu zdarma: projdeme rychlost, SEO, připravenost na AI vyhledávače, mobil a to, proč z webu nechodí poptávky. Výsledek do 48 hodin."
    body = hero([("Domů", "/"), ("Kontrola webu zdarma", None)], "Kontrola webu *zdarma*",
                "Pošlete adresu webu a do 48 hodin dostanete krátké shrnutí 5 věcí, které vám nejvíc berou zákazníky, a co s nimi. Bez závazků a bez obecného automatického reportu: web projde člověk.",
                '<p class="hero-actions"><a href="#kontrola" class="btn btn--primary">Chci kontrolu webu</a></p>')
    body += section("Co zkontrolujeme", "Pět oblastí, které rozhodují o poptávkách", cards([
        ("Srozumitelnost", "Pochopí návštěvník během pár vteřin, co nabízíte, pro koho a co má udělat dál?"),
        ("Důvěra", "Reference, ceny, kontakty a fotky: má zákazník důvod vám věřit víc než konkurenci?"),
        ("Rychlost a mobil", "Jak rychle se web načítá a jak se s ním pracuje na telefonu, kde je dnes většina návštěv."),
        ("SEO a AI vyhledávače", "Najde vás Google, Seznam i ChatGPT na to, co zákazníci hledají?"),
        ("Formulář a kontakt", "Kolik kroků dělí návštěvníka od poptávky a co ho cestou může odradit."),
    ]))
    body += f'''  <section class="section section--mist" id="kontrola">
    <div class="wrap split">
      <div class="section-head section-head--sticky">
        <p class="pill">Zdarma, do 48 hodin</p>
        <h2>Pošlete nám adresu webu</h2>
        <p>Výsledek dostanete e-mailem jako krátké video nebo shrnutí. Pokud budete chtít, navrhneme i řešení a cenu. Když nic dalšího nepotřebujete, nic po vás nechceme.</p>
        {ticks(["Web projde člověk, ne automat", "Konkrétní doporučení místo obecných rad", "Bez závazků"])}
      </div>
      {lead_form("Chci kontrolu webu", "Ozveme se do 48 hodin.", "kontrola", "Co vás na webu trápí? (nepovinné)", button="Zkontrolovat web zdarma")}
    </div>
  </section>
'''
    body += cta_split("Časté dotazy", "Jak kontrola probíhá", "Kontrolu děláme ručně, proto jich zvládneme jen pár týdně. Odpovídáme v pořadí, jak přijdou.", [
        ("Je kontrola opravdu zdarma?", "Ano. Je to nejlepší způsob, jak vám ukázat, jak přemýšlíme. Pokud se rozhodnete pro úpravy, naceníme je předem."),
        ("Zkontrolujete i e-shop?", "Ano, u e-shopu se díváme navíc na produktové stránky, košík a pokladnu."),
        ("Musí být web od vás?", "Ne. Kontrolujeme jakýkoli web: WordPress, Wix, Webnode, Shoptet i weby na míru."),
        ("Co když web potřebuje celý předělat?", "Řekneme vám to na rovinu i s tím, kolik by stál nový web. Někdy ale stačí pár úprav na současném webu."),
    ])
    body += chips_rel([("/reseni/web-nechodi-poptavky/", "Z webu nechodí poptávky"), ("/reseni/redesign-webu/", "Redesign webu"),
                       ("/reseni/pomaly-wordpress/", "Pomalý WordPress"), ("/geo-optimalizace/", "Web v odpovědích AI"), ("/reseni/", "Řešíme problémy s webem")], "Související:")
    head = service_ld("Kontrola webu zdarma", path, md, [("Domů", "/"), ("Kontrola webu zdarma", path)], "Audit webu")
    return ({"title": "Kontrola webu zdarma – co vám bere zákazníky | webovybalicek", "description": md, "path": path, "head": head,
             "nav": "", "cta": "no", "og": {"k": "Zdarma", "h": "Kontrola webu *zdarma*", "pill": "do 48 hodin", "tags": ["Rychlost", "SEO", "Poptávky"]}}, body)


# ---------------------------------------------------------------- ceny
CENY = {
    "/kolik-stoji-e-shop/": dict(
        crumb="Kolik stojí e-shop", h="Kolik stojí *e-shop*?", og="od 35 000 Kč",
        title="Kolik stojí e-shop v roce 2026? Cena tvorby a provozu | webovybalicek",
        md="Kolik stojí e-shop v roce 2026: cena tvorby e-shopu na míru od 35 000 Kč, roční provozní náklady, poplatky platebních bran a co cenu ovlivňuje.",
        l="E-shop na míru u nás stojí od 35 000 Kč. Kolik zaplatíte vy, záleží hlavně na počtu produktů a variant, napojení na sklad a účetnictví a na tom, kolik obsahu připravíme za vás.",
        verdict="Menší e-shop na WooCommerce s platební bránou, Zásilkovnou a fakturací stojí od 35 000 Kč. E-shop s velkoobchodem, napojením na sklad nebo ERP obvykle od 45 000 Kč výš. Provoz vyjde na hosting a doménu (od zhruba 1 500 Kč ročně), poplatky platební brány za transakce a volitelně správu od 600 Kč měsíčně. Na rozdíl od pronajatých e-shopů neplatíte měsíční tarif podle počtu produktů.",
        one=[("E-shop", "od 35 000 Kč", "WooCommerce na míru: platební brána, dopravci, fakturace, design v ceně.", "/tvorba-webu/e-shop/"),
             ("B2B e-shop a velkoobchod", "od 45 000 Kč", "Ceny pro velkoobchodní zákazníky, registrace firem, napojení na sklad.", "/tvorba-webu/b2b-e-shop/"),
             ("Přechod z jiné platformy", "podle počtu produktů", "Převod produktů, zákazníků a objednávek ze Shoptetu, Shopify nebo Wixu.", "/reseni/prechod-ze-shoptetu-na-woocommerce/")],
        yearly=[("Doména", "Zhruba 200 až 400 Kč ročně."), ("Hosting", "Od 1 200 Kč ročně, u větších e-shopů víc podle výkonu."),
                ("Platební brána", "Poplatek z každé platby kartou podle poskytovatele (GoPay, Comgate, ThePay…)."),
                ("Prémiové pluginy", "Dopravci, fakturace nebo feedy, často jednotky stovek až tisíc korun ročně za plugin."),
                ("Správa e-shopu", "Volitelně od 600 Kč měsíčně: aktualizace, zálohy, bezpečnost a drobné úpravy.")],
        factors=[("Počet produktů a variant", "Desítky produktů naplníme ručně, tisíce importujeme z feedu nebo od dodavatele."),
                 ("Napojení", "Sklad, ERP, účetnictví, srovnávače zboží a marketingové nástroje."),
                 ("Jazyky a měny", "Prodej na Slovensko nebo do dalších zemí znamená překlady, měny a jiné dopravce."),
                 ("Obsah", "Popisky produktů, fotky a texty můžete dodat vy, nebo je připravíme s pomocí AI.")],
        q=[("Proč je e-shop dražší než web?", "Kromě stránek obsahuje košík, platby, dopravce, fakturaci, e-maily zákazníkům a právní náležitosti. Všechno musí fungovat spolu a být otestované."),
           ("Vyplatí se radši Shoptet?", "Pro úplný začátek s pár produkty může. Jakmile chcete vlastní design, funkce na míru nebo nechcete platit tarif podle počtu produktů, vychází lépe vlastní e-shop."),
           ("Jak se platí?", "Záloha 50 % při objednávce, zbytek po dokončení.")],
        rel=[("/srovnani/woocommerce-vs-shoptet/", "WooCommerce, nebo Shoptet?"),
             ("/srovnani/shopify-vs-woocommerce/", "Shopify, nebo WooCommerce?"), ("/doporucene-pluginy/", "Doporučené pluginy")]),
    "/kolik-stoji-sprava-webu/": dict(
        crumb="Kolik stojí správa webu", h="Kolik stojí *správa webu*?", og="od 600 Kč/měs.",
        title="Kolik stojí správa webu? Cena a co obsahuje | webovybalicek",
        md="Kolik stojí správa webu: od 600 Kč měsíčně. Aktualizace, zálohy, bezpečnost, drobné úpravy a prémiové pluginy v ceně. Pro WordPress i AI weby.",
        l="Správa webu u nás stojí od 600 Kč měsíčně. Za to máte aktualizace, zálohy, ochranu a drobné úpravy, takže se o web nemusíte starat a nehrozí, že ho jednoho dne najdete nefunkční nebo napadený.",
        verdict="Základní správa webu stojí od 600 Kč měsíčně, přesná cena záleží na velikosti a složitosti webu (e-shop je náročnější než vizitka). Obsahuje aktualizace minimálně jednou až dvakrát měsíčně, zálohy, ochranu proti virům a spamu, kontrolu hostingu, domény a SSL a drobné úpravy do 15 minut měsíčně. U WordPressu jsou v ceně prémiové pluginy jako Elementor Pro nebo Crocoblock.",
        one=[("Správa webu", "od 600 Kč/měs.", "Aktualizace, zálohy, bezpečnost a drobné úpravy pro WordPress i AI weby.", "/sprava-webu/"),
             ("Převzetí webu", "podle stavu webu", "Web od jiného webaře nejdřív projdeme a řekneme, co je potřeba opravit.", "/reseni/prevzeti-webu/"),
             ("Úpravy navíc", "vždy předem naceněné", "Větší změny naceníme a pustíme se do nich až po vašem souhlasu.", "/kontakt/")],
        yearly=[("Aktualizace", "Systém, pluginy a knihovny minimálně jednou až dvakrát měsíčně."), ("Zálohy", "Pravidelné zálohy webu i obsahu."),
                ("Bezpečnost", "Ochrana proti virům a spamu včetně jejich odstranění."), ("Kontrola", "Hosting, doména, SSL certifikát a funkčnost na mobilu i počítači."),
                ("Drobné úpravy", "Konzultace a úpravy do 15 minut měsíčně.")],
        factors=[("Typ webu", "AI web bez pluginů je jednodušší na údržbu než WordPress s desítkami pluginů."),
                 ("E-shop", "Objednávky, platby a dopravci znamenají víc kontroly po každé aktualizaci."),
                 ("Stav webu", "Starý nebo neaktualizovaný web je potřeba nejdřív dát do pořádku."),
                 ("Kolik úprav chcete", "Pokud měníte obsah často, domluvíme větší měsíční rozsah.")],
        q=[("Potřebuju správu, když web skoro neměním?", "Ano. Aktualizace a zálohy nejde vynechat ani u webu, který se nemění. Neaktualizovaný WordPress je nejčastější cesta k napadení."),
           ("Spravujete i weby, které jste nedělali?", "Ano. Nejdřív web projdeme a řekneme, jestli ho převezmeme a co je potřeba před převzetím opravit."),
           ("Můžu správu kdykoli zrušit?", "Ano, web i přístupy jsou vaše a předáme je. Podmínky výpovědi najdete v obchodních podmínkách.")],
        rel=[("/sprava-webu/", "Správa webu"), ("/reseni/prevzeti-webu/", "Převzetí webu"), ("/reseni/napadeny-web/", "Napadený web"), ("/kolik-stoji-web/", "Kolik stojí web")]),
    "/kolik-stoji-redesign-webu/": dict(
        crumb="Kolik stojí redesign webu", h="Kolik stojí *redesign webu*?", og="od 20 000 Kč",
        title="Kolik stojí redesign webu v roce 2026? | webovybalicek",
        md="Kolik stojí redesign webu: AI web od 20 000 Kč, prezentační web na WordPressu od 25 000 Kč, e-shop od 35 000 Kč. Co ovlivňuje cenu a kdy stačí menší úpravy.",
        l="Redesign webu u nás stojí od 20 000 Kč. Kolik zaplatíte vy, záleží na rozsahu webu, na tom, jestli zůstáváte na stejném systému, a kolik obsahu připravíme znovu.",
        verdict="Redesign prezentačního webu jako AI web stojí od 20 000 Kč, na WordPressu od 25 000 Kč, redesign e-shopu od 35 000 Kč. V ceně je nový design na míru, převod obsahu, přesměrování starých adres a příprava na SEO i AI vyhledávače. Někdy stačí menší úpravy současného webu, proto začínáme krátkou kontrolou zdarma.",
        one=[("Redesign na AI web", "od 20 000 Kč", "Nový design i technologie, rychlý web bez pluginů, hotový během dnů.", "/ai-weby/"),
             ("Redesign na WordPressu", "od 25 000 Kč", "Nový vzhled a struktura s administrací, kterou si spravujete sami.", "/reseni/redesign-webu/"),
             ("Redesign e-shopu", "od 35 000 Kč", "Nový vzhled, rychlejší nákup a převod produktů i zákazníků.", "/tvorba-webu/e-shop/")],
        yearly=[("Doména", "Zůstává stejná, platíte jen obnovu."), ("Hosting", "Od 1 200 Kč ročně, často zůstává stávající."),
                ("Správa", "Volitelně od 600 Kč měsíčně.")],
        factors=[("Rozsah webu", "Pět stránek se převádí jinak než web se stovkami článků nebo produktů."),
                 ("Změna systému", "Přechod z Wixu, Webnode nebo Shoptetu znamená přenos obsahu a přesměrování adres."),
                 ("Nové texty a fotky", "Texty připravíme s pomocí AI, fotky může nafotit náš fotograf."),
                 ("Nové funkce", "Rezervace, kalkulačky, členská sekce nebo napojení na jiné systémy.")],
        q=[("Musí se web při redesignu stavět znovu?", "Ne vždy. Po kontrole doporučíme levnější cestu, pokud dává smysl, třeba nový design na současném WordPressu."),
           ("Přijdu po redesignu o pozice v Googlu?", "Při správném přesměrování starých adres ne. Rychlejší web s lepší strukturou se často posune výš."),
           ("Jak dlouho redesign trvá?", "AI web během dnů, větší web nebo e-shop obvykle 3 až 6 týdnů.")],
        rel=[("/reseni/redesign-webu/", "Redesign webu"), ("/kontrola-webu-zdarma/", "Kontrola webu zdarma"), ("/reseni/prevod-webu-z-wixu/", "Převod z Wixu"),
             ("/reseni/prevod-webu-z-webnode/", "Převod z Webnode"), ("/kolik-stoji-web/", "Kolik stojí web")]),
}


def ceny():
    out = []
    for path, C in CENY.items():
        cr = [("Domů", "/"), ("Kolik stojí web", "/kolik-stoji-web/"), (C["crumb"], path)]
        body = hero([("Domů", "/"), ("Kolik stojí web", "/kolik-stoji-web/"), (C["crumb"], None)], C["h"], C["l"],
                    '<p class="hero-actions"><a href="/kontakt/" class="btn btn--primary">Chci cenu na míru</a></p>')
        body += answer("Krátká odpověď", C["verdict"])
        one = "".join(f'<article class="card pay-card"><p class="pill">{e(p)}</p><h3><a href="{u}" class="link">{e(n)}</a></h3><p>{e(t)}</p></article>' for n, p, t, u in C["one"])
        yr = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td></tr>' for a, b in C["yearly"])
        body += section("Cena", "Kolik to stojí", f'<div class="grid-cards">{one}</div>')
        body += section("Co platíte průběžně", "Provoz a co je v ceně", f'<div class="vs-wrap"><table class="vs-table vs-table--2"><tbody>{yr}</tbody></table></div>',
                        "Doménu, hosting a poplatky platíte dodavatelům napřímo, bez naší přirážky.")
        body += section("Co ovlivňuje cenu", "Proč jeden projekt stojí víc než jiný", cards(C["factors"]))
        body += cta_split("Časté dotazy", "Na co se ptáte", "Napište nám pár vět o tom, co potřebujete, a do 24 hodin dostanete odhad ceny.", C["q"])
        body += chips_rel(C["rel"] + [(p, c["crumb"]) for p, c in CENY.items() if p != path], "Související:")
        head = article_ld(C["crumb"] + " v roce 2026", path, C["md"], cr)
        out.append(({"title": C["title"], "description": C["md"], "path": path, "head": head, "nav": "", "ogtype": "article",
                     "og": {"k": "Ceny 2026", "h": C["h"], "pill": C["og"], "tags": ["Cena", "Provoz", "Bez přirážky"]}}, body))
    return out


# ---------------------------------------------------------------- GEO
def geo():
    path = "/geo-optimalizace/"
    md = "GEO optimalizace: jak dostat firmu do odpovědí ChatGPT, Google AI a Perplexity. Strukturovaná data, llms.txt, obsah pro AI vyhledávače a měření."
    body = hero([("Domů", "/"), ("Web v odpovědích AI", None)], "Web v odpovědích *ChatGPT* a Google AI",
                "Lidé se čím dál častěji neptají Googlu, ale ChatGPT nebo Google AI. Připravíme váš web tak, aby mu AI vyhledávače rozuměly, uměly ho citovat a doporučit vás, když se někdo ptá na to, co děláte.", ACTIONS)
    body += answer("Krátká odpověď",
                   "GEO (Generative Engine Optimization) je optimalizace webu pro AI vyhledávače a asistenty. Stojí na stejných základech jako SEO, rychlém a technicky čistém webu, "
                   "a přidává k nim jasné odpovědi na otázky zákazníků, strukturovaná data, soubor llms.txt, povolení AI robotů a důvěryhodné zmínky o firmě mimo web. "
                   "U webů od nás je příprava na SEO, GEO i AEO v ceně, u stávajících webů ji doplníme.")
    body += section("Co děláme", "Jak web připravíme pro AI", cards([
        ("Technický základ", "Rychlost, čistý kód, sitemap a povolení robotů ChatGPT, Google, Perplexity a dalších v robots.txt."),
        ("Strukturovaná data", "Schema.org pro firmu, služby, ceny, časté dotazy, recenze a pojmy, aby AI přesně věděla, co nabízíte."),
        ("Odpovědi na otázky", "Stránky s krátkou jasnou odpovědí na to, na co se zákazníci ptají: ceny, srovnání, postupy, časté dotazy."),
        ("llms.txt", "Stručný přehled webu přímo pro jazykové modely: kdo jste, co nabízíte a kde najdou podrobnosti."),
        ("Zmínky mimo web", "Firemní profil Google, Firmy.cz, recenze a katalogy, ze kterých AI čerpá při doporučování firem."),
        ("Měření", "Sledujeme návštěvy z AI asistentů v Google Analytics a ověřujeme, jak vás AI popisuje."),
    ]))
    body += answer("Na vlastním webu", "Stejný postup používáme na webovybalicek.cz: strukturovaná data na každé stránce, krátké odpovědi u srovnání a cen, slovníček pojmů, llms.txt a robots.txt, který AI vyhledávače výslovně povoluje.")
    body += cta_split("Časté dotazy", "GEO: na co se ptáte", "Chcete vědět, jak vás dnes popisuje ChatGPT? Pošlete adresu webu na kontrolu zdarma.", [
        ("Jaký je rozdíl mezi SEO, GEO a AEO?", "SEO je optimalizace pro klasické výsledky vyhledávání, GEO pro odpovědi generativní AI (ChatGPT, Google AI) a AEO pro přímé odpovědi na otázky. Základ mají společný, liší se důrazem na strukturu a jasné odpovědi."),
        ("Můžete zaručit, že mě ChatGPT doporučí?", "Ne, to nemůže slíbit nikdo. Můžeme výrazně zvýšit šanci tím, že web bude AI srozumitelný, důvěryhodný a bude odpovídat na otázky vašich zákazníků."),
        ("Funguje to i pro malé firmy?", "Ano. U místních služeb a specializovaných oborů je konkurence v AI odpovědích zatím malá, takže dobře připravený web má výhodu."),
        ("Kolik to stojí?", "U nových webů je příprava v ceně. U stávajícího webu naceníme podle stavu po kontrole zdarma."),
    ])
    body += chips_rel([("/slovnicek/geo/", "Co je GEO"), ("/slovnicek/aeo/", "Co je AEO"), ("/slovnicek/strukturovana-data/", "Strukturovaná data"),
                       ("/kontrola-webu-zdarma/", "Kontrola webu zdarma"), ("/ai-weby/", "AI weby")], "Související:")
    head = service_ld("GEO optimalizace webu pro AI vyhledávače", path, md, [("Domů", "/"), ("Web v odpovědích AI", path)], "GEO optimalizace")
    return ({"title": "GEO optimalizace – web v odpovědích ChatGPT a Google AI | webovybalicek", "description": md, "path": path, "head": head,
             "nav": "", "og": {"k": "GEO a AEO", "h": "Web v odpovědích *AI*", "tags": ["ChatGPT", "Google AI", "Perplexity"]}}, body)


# ---------------------------------------------------------------- spolupráce pro agentury
def agentury():
    path = "/spoluprace-pro-agentury/"
    md = "Subdodávky webů pro agentury a freelancery: WordPress, WooCommerce, Elementor a AI weby pod vaší značkou. Spolehlivě, v termínu, s dlouhodobou podporou."
    body = hero([("Domů", "/"), ("Spolupráce pro agentury", None)], "Weby pro *agentury a freelancery*",
                "Máte klienta, ale nemáte kapacitu nebo vývojáře? Postavíme web, e-shop nebo složitější funkci pod vaší značkou. Vy držíte vztah s klientem, my dodáme práci včas a v kvalitě, za kterou se nemusíte stydět.",
                '<p class="hero-actions"><a href="/#spoluprace" class="btn btn--primary">Domluvit spolupráci</a><a href="tel:+420723933774" class="btn btn--outline">723 933 774</a></p>')
    body += section("Co dodáme", "S čím vám pomůžeme", cards([
        ("Weby na klíč pod vaší značkou", "Od návrhu po spuštění, klient komunikuje s vámi. Na požádání podepíšeme mlčenlivost."),
        ("WooCommerce a české služby", "E-shopy se Zásilkovnou, PPL, GoPay, Comgate, Fakturoidem nebo iDokladem, hotové a otestované."),
        ("Složité funkce", "Rezervace, kalkulačky, formuláře, členské sekce, Crocoblock a JetEngine, napojení přes API."),
        ("AI weby", "Rychlé weby na míru postavené s pomocí AI, když klient nepotřebuje WordPress."),
        ("Výpomoc s vývojem", "Dlouhodobá kapacita do vašeho týmu: úpravy, opravy, migrace a správa webů vašich klientů."),
        ("Pro freelancery", "PPC specialisté, copywriteři a grafici: vy přinesete klienta a obor, my postavíme web."),
    ]))
    body += section("Proč s námi", "Na co se můžete spolehnout", ticks([
        "Weby tvoříme od roku 2018, máme za sebou přes 150 klientských webů",
        "Spolupracujeme s dalšími agenturami, například STARLAB a Webofka",
        "Termíny a cenu dostanete předem a písemně",
        "Kód a přístupy předáváme, žádné uzamčení",
        "Správu webů po spuštění můžeme převzít za vás",
    ]))
    body += cta_split("Časté dotazy", "Spolupráce: na co se ptáte", "Napište, jaké projekty řešíte. Domluvíme si krátký hovor a nastavíme spolupráci, která sedí vám.", [
        ("Budete komunikovat s mým klientem?", "Jen pokud chcete. Běžně pracujeme jako tichý subdodavatel a s klientem mluvíte vy."),
        ("Jak se spolupráce účtuje?", "Za projekt podle předem schválené nabídky, nebo hodinově u dlouhodobé výpomoci. Cenu vždy víte předem."),
        ("Dáte na web své logo?", "Ne, pokud si to nepřejete. Web je pod vaší značkou."),
        ("Pracujete i se Shoptetem?", "Specializujeme se na WordPress, WooCommerce a AI weby. U Shoptetu pomůžeme hlavně s přechodem na WooCommerce."),
    ])
    body += chips_rel([("/srovnani/agentura-vs-freelancer/", "Agentura, nebo freelancer?"), ("/doporucene-pluginy/", "Doporučené pluginy"),
                       ("/nastroje/", "Nástroje a technologie"), ("/o-nas/", "O nás")], "Související:")
    head = service_ld("Subdodávky webů pro agentury a freelancery", path, md, [("Domů", "/"), ("Spolupráce pro agentury", path)], "White-label tvorba webů")
    return ({"title": "Subdodávky webů pro agentury a freelancery | webovybalicek", "description": md, "path": path, "head": head,
             "nav": "", "og": {"k": "Pro agentury", "h": "Weby pro *agentury*", "tags": ["White-label", "WooCommerce", "AI weby"]}}, body)


# ---------------------------------------------------------------- případové studie
def projekty(src):
    P = runpy.run_path(str(src / "data" / "pripadovky.py"))["P"]
    out = []
    for k, x in P.items():
        path = f"/projekty/{k}/"
        cr = [("Domů", "/"), ("Případové studie", "/projekty/"), (x["n"], path)]
        body = hero([("Domů", "/"), ("Případové studie", "/projekty/"), (x["n"], None)], x["h"], x["l"],
                    f'<p class="hero-actions"><a href="{x["u"]}" class="btn btn--outline" target="_blank" rel="noopener">Prohlédnout web ↗</a></p>')
        tags = "".join(f'<li>{e(t)}</li>' for t in x["tags"])
        body += f'''  <section class="section section--tight">
    <div class="wrap"><ul class="chips">{tags}</ul></div>
  </section>
'''
        body += f'''  <section class="section">
    <div class="wrap split">
      <div class="section-head"><p class="pill">Zadání</p><h2>S čím klient přišel</h2></div>
      <div class="card pay-card"><p>{e(x["zadani"])}</p></div>
    </div>
  </section>
'''
        body += section("Řešení", "Co jsme postavili", cards(x["reseni"]))
        if x.get("vysledek"):
            body += answer("Výsledek", x["vysledek"])
        if x.get("citace"):
            body += answer(x.get("citace_od", "Klient"), "„" + x["citace"] + "“")
        if x.get("foto"):
            f = x["foto"]
            nahled = (f'<img class="case-photo" src="/assets/img/projekty/{f}?v={{{{v}}}}" srcset="/assets/img/projekty/960/{f}?v={{{{v}}}} 960w, /assets/img/projekty/{f}?v={{{{v}}}} 1800w" '
                      f'sizes="(max-width: 1440px) 92vw, 1400px" width="1800" height="1200" alt="{e(x["n"])} – ukázka webu" loading="lazy" decoding="async">')
        else:
            nahled = f'{{{{shots_pick:{x["ref"]}|{e(x["n"])}}}}}'
        body += f'''  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Náhled</p><h2>Jak web vypadá</h2></div>
      {nahled}
    </div>
  </section>
'''
        body += chips_rel(x["rel"] + [(f"/projekty/{o}/", v["n"]) for o, v in P.items() if o != k], "Související:")
        head = ld([{"@context": "https://schema.org", "@type": "Article", "headline": f"Případová studie: {x['n']}", "description": x["md"],
                    "author": ORG, "publisher": ORG, "inLanguage": "cs", "mainEntityOfPage": SITE + path, "dateModified": "2026-11-25",
                    "about": {"@type": "WebSite", "name": x["n"], "url": x["u"]}}, crumbs_ld(cr)])
        out.append(({"title": f"{x['n']}: {x['title']} | Případová studie | webovybalicek", "description": x["md"], "path": path, "head": head,
                     "nav": "", "ogtype": "article", "og": {"k": "Případová studie", "h": x["h"], "tags": x["tags"][:3]}}, body))

    tiles = "".join(f'<article class="card pay-card"><p class="pill">{e(x["tags"][0])}</p><h3><a href="/projekty/{k}/" class="link">{e(x["n"])}</a></h3><p>{e(x["title"])}.</p></article>'
                    for k, x in P.items())
    body = hero([("Domů", "/"), ("Případové studie", None)], "Případové *studie*",
                "Jak jsme řešili konkrétní zadání: od rezervací s platbou přes e-shopy až po náborové weby. Co klient potřeboval, co jsme postavili a jak to funguje.")
    body += f'''  <section class="section">
    <div class="wrap">
      <div class="grid-cards">{tiles}</div>
      <p class="note">Další weby najdete v <a href="/#reference" class="link">referencích</a>.</p>
    </div>
  </section>
'''
    out.append(({"title": "Případové studie – weby, e-shopy a rezervace v praxi | webovybalicek",
                 "description": "Případové studie webovybalicek: rezervace s platbou a prodej poukazů, e-shopy na WooCommerce a náborové weby. Zadání, řešení a ukázky.",
                 "path": "/projekty/", "nav": "", "head": ld([crumbs_ld([("Domů", "/"), ("Případové studie", "/projekty/")])]),
                 "og": {"k": "Reference", "h": "Případové *studie*", "tags": ["Rezervace", "E-shop", "Nábor"]}}, body))
    return out


def pages(src):
    return [kontrola(), *ceny(), geo(), agentury(), *projekty(src)]
