"""SEO stránky s partnerskými odkazy (backlog docs/backlog-seo-affiliate.md, fáze 2, 27. 11. 2026).
Jen pro vyhledávání: žádné odkazy z patičky, menu, rozcestníků ani běžných stránek. Prolinkované jen mezi sebou.
Partnerské odkazy vedou přes /go/<slug>/ (src/data/affil.json), mají rel="sponsored nofollow" a stránka nese viditelnou poznámku.
Ceny a poplatky jen z oficiálních ceníků s datem ověření, žádná vymyšlená čísla."""
import datetime
import json
from pathlib import Path

from typy import e, hero
from seo import ld, crumbs_ld, cta_split, SITE, ORG
from seo_extra import chips_rel
from seo_more import cards, ticks, section, answer

OVERENO = "27. 11. 2026"
MOD = "2026-11-27"
PLUG = "/doporucene-pluginy/"

PAGES = [  # (cesta, krátký název) – vzájemné prolinkování
    ("/e-shop/platebni-brany-srovnani/", "Srovnání platebních bran"),
    ("/software/fakturoid-vs-idoklad/", "Fakturoid, nebo iDoklad?"),
    ("/wordpress/learndash-recenze/", "LearnDash v praxi"),
    ("/wordpress/learndash-vs-moodle/", "LearnDash, nebo Moodle?"),
    ("/e-shop/slevy-a-akce-ve-woocommerce/", "Slevy a akce ve WooCommerce"),
    ("/slevove-kody/", "Slevové kódy a akce"),
]

_AFFIL = {}


def affil(src):
    global _AFFIL
    _AFFIL = {k: v for k, v in json.loads((src / "data" / "affil.json").read_text(encoding="utf-8")).items() if not k.startswith("_")}


def out(slug, text, cls="link"):
    """Odkaz na službu: aktivní partnerský přes /go/, jinak přímý bez provize."""
    a = _AFFIL[slug]
    if a["aktivni"]:
        return f'<a href="/go/{slug}/" class="{cls}" rel="sponsored nofollow noopener" target="_blank">{e(text)}</a>'
    return f'<a href="{a["url"]}" class="{cls}" rel="noopener" target="_blank">{e(text)}</a>'


def disclosure():
    return '''  <section class="section section--tight">
    <div class="wrap"><p class="note note--small">Některé odkazy na této stránce jsou partnerské. Když si přes ně službu objednáte, dostaneme malou provizi a vás to nestojí nic navíc. Pořadí a hodnocení podle provize neupravujeme.</p></div>
  </section>
'''


def table(head, rows, note=""):
    th = "".join(f"<th>{e(h)}</th>" for h in head)
    tr = "".join("<tr><th>" + r[0] + "</th>" + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>" for r in rows)
    n = f'<p class="note note--small">{note}</p>' if note else ""
    return f'<div class="vs-wrap"><table class="vs-table vs-table--auto"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>{n}'


def faq_ld(q):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in q]}


def article(path, headline, md, cr, q):
    return ld([{"@context": "https://schema.org", "@type": "Article", "headline": headline, "description": md, "author": ORG,
                "publisher": ORG, "inLanguage": "cs", "mainEntityOfPage": SITE + path, "dateModified": MOD},
               crumbs_ld(cr), faq_ld(q)])


def related(path, extra=()):
    return chips_rel(list(extra) + [(u, t) for u, t in PAGES if u != path], "Související:")


def meta(path, title, md, head, og):
    return {"title": title, "description": md, "path": path, "head": head, "nav": "", "ogtype": "article", "og": og}


# ---------------------------------------------------------------- platební brány
def brany():
    path = "/e-shop/platebni-brany-srovnani/"
    md = "Srovnání platebních bran Comgate, GoPay, ThePay, Stripe a GP webpay pro e-shop: poplatky z oficiálních ceníků, napojení na WooCommerce a kterou kdy zvolit."
    cr = [("Domů", "/"), ("Srovnání platebních bran", path)]
    body = hero([("Domů", "/"), ("Srovnání platebních bran", None)], "Platební brány pro e-shop: *srovnání* poplatků a napojení",
                "Comgate, GoPay, ThePay, Stripe i brána od banky. Co stojí platba kartou, co se platí navíc a jak bránu napojit na WooCommerce. Poplatky jsme vzali z oficiálních ceníků, napojení známe z e-shopů, které stavíme.",
                '<p class="hero-actions"><a href="#poplatky" class="btn btn--primary">Porovnat poplatky</a><a href="/kontakt/" class="btn btn--outline">Napojíme bránu za vás</a></p>')
    body += answer("Krátká odpověď", "Pro běžný český e-shop dávají největší smysl Comgate, GoPay a ThePay: české ceníky, výplaty v korunách, bankovní tlačítka a hotové pluginy pro WooCommerce. U malého obratu rozhoduje hlavně měsíční poplatek a úvodní akce, u většího procento z platby. Stripe se hodí pro prodej do zahraničí a předplatné.")
    body += f'''  <section class="section" id="poplatky">
    <div class="wrap">
      <div class="section-head"><p class="pill">Poplatky</p><h2>Kolik stojí platba kartou</h2><p>Základní sazby pro běžné spotřebitelské karty vydané v EU. Ceny jsou bez DPH a platí pro nové obchodníky, ověřeno {OVERENO}.</p></div>
      {table(["Brána", "Platba kartou", "Měsíční poplatek", "Úvodní akce"], [
        ["Comgate Easy", "1 % + 0 Kč", "100 Kč, zdarma při obratu nad 100 000 Kč měsíčně", "tarif Start: 6 měsíců karty zdarma do 50 000 Kč měsíčně, pak Easy"],
        ["Comgate Profi", "0,67 % + 1 Kč", "100 Kč, zdarma při obratu nad 100 000 Kč měsíčně", "výhodnější při vyšších objednávkách"],
        ["GoPay", "0,95 % + 0 Kč", "podle tarifu", "tarif Start: 12 měsíců zdarma pro nové obchodníky"],
        ["ThePay", "podle ceníku nebo individuální nabídky", "bez poplatku za zřízení a vedení", "bez pevných poplatků za transakci"],
        ["Stripe", "1,5 % + 6,50 Kč", "bez měsíčního poplatku", "karty mimo EHP 3,25 % + 6,50 Kč"],
        ["GP webpay", "podle smlouvy s bankou", "podle banky", "bránu zprostředkovává vaše banka"],
      ], 'Zdroje: <a href="https://www.comgate.cz/cenik" class="link" rel="noopener" target="_blank">ceník Comgate</a>, <a href="https://www.gopay.com/cena/" class="link" rel="noopener" target="_blank">ceník GoPay</a>, <a href="https://www.thepay.eu/" class="link" rel="noopener" target="_blank">ThePay</a>, <a href="https://stripe.com/cz/pricing" class="link" rel="noopener" target="_blank">ceník Stripe</a>. Comgate garantuje ceny svého ceníku nejméně do 31. 12. 2026. Spor o platbu (chargeback) stojí u Comgate i GoPay 990 Kč.')}
    </div>
  </section>
'''
    body += section("Na co se dívat", "Procento z platby není celý účet", cards([
        ("Měsíční poplatek", "Při malém obratu může paušál stát víc než samotné platby. Spočítejte si reálný měsíc, ne jen sazbu."),
        ("Pevná částka za platbu", "Korunový poplatek navíc se projeví hlavně u levných objednávek. U drahých naopak vyhraje nižší procento."),
        ("Výplaty a měna", "Jak často a v jaké měně peníze chodí na účet a jestli se za převod platí."),
        ("Platební metody", "Karty, Apple Pay a Google Pay umí všechny. Rozdíl je v bankovních tlačítkách, platbách na splátky a odložených platbách."),
        ("Vratky a spory", "Kolik stojí vrácení peněz a chargeback a jestli se vratka dá udělat přímo z administrace e-shopu."),
        ("Napojení na e-shop", "Hotový plugin s podporou ušetří víc než desetina procenta z poplatků."),
    ]))
    body += f'''  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Brány jednotlivě</p><h2>Kterou bránu kdy zvolit</h2></div>
      <div class="grid-cards">
        <article class="card pay-card"><h3>Comgate</h3><p>Nejširší nabídka metod v jedné bráně: karty, peněženky, bankovní tlačítka pro CZ, SK i PL, splátky a odložené platby. Dva tarify podle velikosti objednávek.</p><p>{out("comgate", "Registrace do Comgate")} · <a href="{PLUG}comgate/" class="link">plugin pro WooCommerce</a></p></article>
        <article class="card pay-card"><h3>GoPay</h3><p>Rozšířená česká brána, platba může proběhnout přímo na stránce e-shopu (inline). Dlouhá úvodní akce pro nové obchodníky.</p><p>{out("gopay", "Web GoPay")} · <a href="{PLUG}gopay/" class="link">plugin GoPay Inline</a></p></article>
        <article class="card pay-card"><h3>ThePay</h3><p>Bez poplatků za zřízení a vedení, opakované i odložené platby a řada měn. Vhodná i pro předplatné.</p><p>{out("thepay", "Registrace do ThePay")} · <a href="{PLUG}thepay/" class="link">plugin ThePay 2.0</a></p></article>
        <article class="card pay-card"><h3>Stripe</h3><p>Světový standard pro prodej do zahraničí, předplatné a SaaS. Bez měsíčního poplatku, ale s pevnou částkou za platbu a bez českých bankovních tlačítek.</p><p>{out("stripe", "Web Stripe")}</p></article>
        <article class="card pay-card"><h3>GP webpay a banky</h3><p>Brána, kterou vám zprostředkuje banka. Dává smysl, když už s bankou máte podmínky vyjednané. Podobně funguje i brána ČSOB.</p><p><a href="{PLUG}gp-webpay/" class="link">plugin GP webpay</a> · <a href="{PLUG}csob/" class="link">plugin ČSOB</a></p></article>
      </div>
    </div>
  </section>
'''
    body += section("Napojení", "Jak bránu napojit na WooCommerce", ticks([
        "Založte si účet u brány a projděte ověřením firmy. Bez smlouvy brána nepustí ostré platby.",
        "Nainstalujte plugin. Na e-shopech používáme pluginy Toret: jsou česky, umí refundace z administrace a správně mění stavy objednávek.",
        "Vyzkoušejte platby v testovacím režimu včetně zamítnuté platby a vratky.",
        "Zkontrolujte e-maily zákazníkovi, stav objednávky po zaplacení a napojení na fakturaci.",
        "Teprve pak přepněte na ostrý režim.",
    ]))
    q = [
        ("Která platební brána je nejlevnější?", "Záleží na obratu a velikosti objednávek. Při malém obratu rozhoduje měsíční poplatek a úvodní akce, při velkém procento z platby. U levných objednávek prodraží platbu pevná korunová částka. Spočítejte si jeden typický měsíc podle oficiálních ceníků."),
        ("Potřebuju platební bránu, když mám dobírku a převod?", "Nemusíte, ale platba kartou a Apple Pay nebo Google Pay výrazně zrychlí nákup. Převod navíc musíte ručně párovat, pokud nemáte napojenou fakturaci."),
        ("Můžu mít na e-shopu dvě brány?", "Ano. Někdy dává smysl česká brána pro běžné platby a Stripe pro zahraniční zákazníky nebo předplatné."),
        ("Kolik stojí napojení brány?", "Plugin Toret pro bránu stojí 1 690 Kč ročně (ČSOB 1 990 Kč). Napojení, otestování a nastavení e-mailů zvládneme v rámci tvorby nebo správy e-shopu."),
    ]
    body += cta_split("Časté dotazy", "Platební brány: na co se ptáte", "Napojíme bránu na váš e-shop, otestujeme platby, vratky i fakturaci. Nebo postavíme celý e-shop.", q)
    body += disclosure() + related(path, [(PLUG + "#platby", "Pluginy pro platby"), ("/kolik-stoji-e-shop/", "Kolik stojí e-shop")])
    head = article(path, "Srovnání platebních bran pro e-shop", md, cr, q)
    return (meta(path, "Platební brány pro e-shop: srovnání poplatků 2026 | webovybalicek", md, head,
                 {"k": "Srovnání", "h": "Platební *brány*", "tags": ["Comgate", "GoPay", "ThePay"]}), body)


# ---------------------------------------------------------------- Fakturoid vs iDoklad
def fakturace():
    path = "/software/fakturoid-vs-idoklad/"
    md = "Fakturoid, nebo iDoklad? Srovnání cen, tarifů, párování plateb a napojení na e-shop. Kdy se vyplatí který fakturační program, podle oficiálních ceníků."
    cr = [("Domů", "/"), ("Fakturoid, nebo iDoklad?", path)]
    body = hero([("Domů", "/"), ("Fakturoid, nebo iDoklad?", None)], "Fakturoid, nebo *iDoklad*?",
                "Dva nejrozšířenější české fakturační programy. Oba napojujeme na e-shopy a weby klientů. Tady je, v čem se liší cenou, funkcemi a napojením, abyste si vybrali bez zkoušení obou.",
                '<p class="hero-actions"><a href="#ceny" class="btn btn--primary">Porovnat ceny</a><a href="/kontakt/" class="btn btn--outline">Napojíme fakturaci na e-shop</a></p>')
    body += answer("Krátká odpověď", "Fakturoid je levnější pro živnostníka, který fakturuje sám a chce jednoduchou aplikaci. iDoklad se vyplatí, když do fakturace sahá víc lidí nebo potřebujete ceník a sklad. Pro e-shop na WooCommerce jsou oba napojitelné stejně dobře přes plugin Toret.")
    body += f'''  <section class="section" id="ceny">
    <div class="wrap">
      <div class="section-head"><p class="pill">Ceny</p><h2>Kolik stojí</h2><p>Ceny z oficiálních ceníků, ověřeno {OVERENO}.</p></div>
      {table(["", "Fakturoid", "iDoklad"], [
        ["Verze zdarma", "ano, s omezením na 5 kontaktů", "ano, s omezeními"],
        ["Nejlevnější placený tarif", "Na lehko: 164 Kč bez DPH měsíčně (199 Kč s DPH)", "Základní: 240 Kč bez DPH měsíčně, 187 Kč při roční platbě"],
        ["Párování plateb s bankou", "tarif Na každý den", "tarif Oblíbený: 430 Kč bez DPH měsíčně, 358 Kč při roční platbě"],
        ["Nejvyšší tarif", "Na maximum", "Prémiový: 750 Kč bez DPH měsíčně, 625 Kč při roční platbě"],
        ["Další uživatel", "99 Kč bez DPH měsíčně", "více uživatelů v ceně vyšších tarifů"],
        ["Vyzkoušení", "30 dní všech funkcí zdarma", "60 dní zdarma"],
      ], 'Zdroje: <a href="https://www.fakturoid.cz/cenik" class="link" rel="noopener" target="_blank">ceník Fakturoidu</a>, <a href="https://www.idoklad.cz/cenik" class="link" rel="noopener" target="_blank">ceník iDokladu</a> (ceny platné od 1. 5. 2025).')}
    </div>
  </section>
'''
    body += section("Rozdíly", "V čem se liší v praxi", cards([
        ("Pro koho je Fakturoid", "Živnostníci a malé firmy, které chtějí rychlou a přehlednou aplikaci. Webfaktura, QR platba a robot, který hlídá ARES a nespolehlivé plátce."),
        ("Pro koho je iDoklad", "Firmy, kde do fakturace sahá víc lidí, potřebují ceník a sklad nebo spolupracují s účetní v programu Money (oba patří pod Seyfor)."),
        ("Párování plateb", "Oba umí spárovat platby z banky s fakturami a poslat upomínky. U Fakturoidu je to od prostředního tarifu, u iDokladu od tarifu Oblíbený."),
        ("API a napojení", "Oba mají API. iDoklad ukončil 8. 9. 2026 starou verzi API v2, starší napojení je potřeba převést na novou verzi."),
    ]))
    body += f'''  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">E-shop</p><h2>Napojení na WooCommerce</h2><p>Faktury, proformy a dobropisy pak vznikají samy z objednávek a platby převodem se párují s objednávkami.</p></div>
      <div class="grid-cards">
        <article class="card pay-card"><h3>Fakturoid pro WooCommerce</h3><p>Automatické vystavení a odeslání dokladů, webfaktura s PDF a ISDOC, režim OSS.</p><p><a href="{PLUG}fakturoid/" class="link">Plugin Fakturoid</a> · {out("fakturoid", "Web Fakturoidu")}</p></article>
        <article class="card pay-card"><h3>iDoklad pro WooCommerce</h3><p>Faktury a proformy podle platební metody, dobropisy, párování plateb a faktura v zákaznickém účtu.</p><p><a href="{PLUG}idoklad/" class="link">Plugin iDoklad</a> · {out("idoklad", "Registrace do iDokladu")}</p></article>
      </div>
    </div>
  </section>
'''
    q = [
        ("Je Fakturoid levnější než iDoklad?", "Pro jednoho uživatele ano. Jakmile potřebujete víc přístupů, může vyjít levněji iDoklad, protože víc uživatelů má v ceně vyšších tarifů."),
        ("Můžu přejít z jednoho programu na druhý?", "Ano. Kontakty a položky ceníku přenesete exportem a importem. Staré faktury je dobré si stáhnout a archivovat."),
        ("Který program je lepší pro e-shop?", "Oba se napojí na WooCommerce přes plugin Toret (1 690 Kč ročně) a umí automatické faktury i párování plateb. Rozhodněte podle toho, s čím pracuje vaše účetní."),
        ("Potřebuju placený tarif?", "Pro pár faktur měsíčně stačí verze zdarma. Placený tarif se vyplatí kvůli párování plateb, upomínkám a exportům pro účetní."),
    ]
    body += cta_split("Časté dotazy", "Fakturace: na co se ptáte", "Napojíme fakturaci na váš e-shop nebo web, aby faktury vznikaly samy z objednávek.", q)
    body += disclosure() + related(path, [(PLUG + "#fakturace", "Pluginy pro fakturaci")])
    head = article(path, "Fakturoid, nebo iDoklad? Srovnání", md, cr, q)
    return (meta(path, "Fakturoid, nebo iDoklad? Srovnání cen a funkcí 2026 | webovybalicek", md, head,
                 {"k": "Srovnání", "h": "Fakturoid, nebo *iDoklad*?", "tags": ["Fakturace", "Ceny", "E-shop"]}), body)


# ---------------------------------------------------------------- LearnDash recenze
def learndash():
    path = "/wordpress/learndash-recenze/"
    md = "LearnDash v praxi: co umí plugin pro online kurzy na WordPressu, jak prodávat kurzy přes WooCommerce, kolik stojí a pro koho se hodí."
    cr = [("Domů", "/"), ("LearnDash v praxi", path)]
    body = hero([("Domů", "/"), ("LearnDash v praxi", None)], "LearnDash: online kurzy *na WordPressu*",
                "LearnDash je plugin, který z WordPressu udělá vzdělávací platformu: kurzy, lekce, testy, certifikáty a prodej. Kurzy i data zůstávají na vašem webu a z prodeje se neodvádí procenta.",
                f'<p class="hero-actions">{out("learndash", "Prohlédnout LearnDash", "btn btn--primary")}<a href="/kontakt/" class="btn btn--outline">Postavíme vám kurzy</a></p>')
    body += answer("Krátká odpověď", "LearnDash se vyplatí, když chcete kurzy prodávat pod vlastní značkou na svém webu a mít je propojené s e-shopem, newsletterem a fakturací. Pokud potřebujete jen pár videí za heslem, stačí jednodušší členská sekce. Pro velké firemní a školní vzdělávání s hodnocením a SCORM zvažte Moodle.")
    body += section("Co umí", "Hlavní funkce", cards([
        ("Stavba kurzu", "Kurz, lekce, témata a testy v přehledném editoru. Obsah může být video, text, soubory i úkoly."),
        ("Postupné odemykání", "Lekce se odemykají podle data nebo po dokončení předchozí. Žák nepřeskočí to podstatné."),
        ("Testy a certifikáty", "Různé typy otázek, bodování, opakování testu a certifikát v PDF po dokončení kurzu."),
        ("Prodej kurzů", "Jednorázový nákup, předplatné nebo skupiny. Přes WooCommerce s českými platebními bránami a fakturací."),
        ("Přehledy", "Kdo kurz začal, kde skončil a jak dopadl v testech."),
        ("Vaše data", "Kurzy, žáci i platby jsou na vašem webu. Žádná platforma vám nebere procenta z prodeje."),
    ]))
    body += section("Cena", "Kolik LearnDash stojí", f'''<div class="card pay-card"><p>LearnDash se platí roční licencí v amerických dolarech, z prodeje kurzů si nebere žádná procenta. V roce 2026 výrobce několikrát změnil tarify, proto uvádíme jen stav ke dni ověření ({OVERENO}): aktuální ceny najdete na {out("learndash", "oficiální stránce LearnDash")}. K licenci počítejte s hostingem, šablonou a případně WooCommerce pro prodej.</p></div>''')
    body += section("Zkušenost", "Na co si dát pozor", ticks([
        "Video nenahrávejte přímo do WordPressu. Patří na Vimeo, Bunny Stream nebo podobnou službu, jinak web zpomalí.",
        "Hosting dimenzujte na přihlášené uživatele, kteří obcházejí cache. Levný sdílený hosting při spuštění kurzu nestačí.",
        "Prodej přes WooCommerce dává smysl kvůli českým platebním bránám a automatickým fakturám.",
        "Vzhled kurzů sladíme s webem v Elementoru, aby kurz nepůsobil jako cizí aplikace.",
    ]))
    q = [
        ("Je LearnDash v češtině?", "Rozhraní pro žáky přeložíme do češtiny. Texty kurzů píšete sami, takže jsou česky od začátku."),
        ("Bere si LearnDash procenta z prodeje?", "Ne. Platíte roční licenci a poplatky platební brány, z ceny kurzu nic dalšího neodchází."),
        ("Jde prodávat kurz i na splátky nebo předplatné?", "Ano. Předplatné a opakované platby řeší WooCommerce s platební bránou, která opakované platby podporuje, třeba Comgate nebo ThePay."),
        ("Kolik stojí web s kurzy na míru?", "Podle rozsahu. Napište, kolik kurzů a žáků plánujete a jak chcete prodávat, a dostanete cenu předem."),
    ]
    body += cta_split("Časté dotazy", "LearnDash: na co se ptáte", "Postavíme web s kurzy na WordPressu: LearnDash, prodej přes WooCommerce, platební brána a faktury automaticky.", q)
    body += disclosure() + related(path, [("/tvorba-webu/online-kurzy/", "Weby pro online kurzy")])
    head = article(path, "LearnDash v praxi: online kurzy na WordPressu", md, cr, q)
    return (meta(path, "LearnDash recenze: online kurzy na WordPressu v praxi | webovybalicek", md, head,
                 {"k": "Recenze", "h": "LearnDash *v praxi*", "tags": ["Online kurzy", "WordPress", "WooCommerce"]}), body)


# ---------------------------------------------------------------- LearnDash vs Moodle
def moodle():
    path = "/wordpress/learndash-vs-moodle/"
    md = "LearnDash, nebo Moodle? Srovnání pro online kurzy a firemní vzdělávání: cena, provoz, prodej kurzů, hodnocení a SCORM. Kdy zvolit který systém."
    cr = [("Domů", "/"), ("LearnDash, nebo Moodle?", path)]
    body = hero([("Domů", "/"), ("LearnDash, nebo Moodle?", None)], "LearnDash, nebo *Moodle*?",
                "Oba systémy umí kurzy, testy a certifikáty. Každý ale vychází z jiného světa: LearnDash z webu, který prodává, Moodle ze škol a firemního vzdělávání. Tuhle volbu jsme řešili i s klienty.",
                '<p class="hero-actions"><a href="#srovnani" class="btn btn--primary">Srovnání</a><a href="/kontakt/" class="btn btn--outline">Poradíme s výběrem</a></p>')
    body += answer("Krátká odpověď", "Prodáváte kurzy veřejnosti a chcete je mít na svém webu se značkou, e-shopem a newsletterem? LearnDash. Vzděláváte zaměstnance nebo studenty, potřebujete podrobné hodnocení, role a SCORM balíčky a máte kapacitu na správu? Moodle.")
    body += f'''  <section class="section" id="srovnani">
    <div class="wrap">
      <div class="section-head"><p class="pill">Srovnání</p><h2>V čem se liší</h2></div>
      {table(["", "LearnDash", "Moodle"], [
        ["Co to je", "plugin pro WordPress", "samostatný systém pro řízení výuky (LMS)"],
        ["Licence", "placená roční licence", "open source zdarma, platíte provoz a správu"],
        ["Prodej kurzů", "přes WooCommerce s českými bránami a fakturací", "jde, ale není to jeho silná stránka"],
        ["Vzhled a web", "kurzy jsou součástí webu se stejným designem", "samostatná aplikace s vlastním vzhledem"],
        ["Hodnocení a role", "testy, úkoly, skupiny", "velmi podrobné: známkování, role, kompetence"],
        ["SCORM", "přes doplněk", "nativně"],
        ["Správa", "jako běžný WordPress", "náročnější, ideálně vlastní server a správce"],
      ])}
    </div>
  </section>
'''
    body += section("Rozhodnutí", "Kdy co zvolit", cards([
        ("LearnDash", "Online kurzy na prodej, kouči, lektoři, menší firmy. Web, e-shop a kurzy v jednom a bez procent z prodeje."),
        ("Moodle", "Školy, velké firmy, akreditované vzdělávání. Hodně uživatelů, podrobné hodnocení, SCORM a reporty pro vedení."),
        ("Ani jedno", "Pár videí za heslem nebo jednorázový webinář. Stačí členská sekce na webu nebo hotová platforma."),
    ]))
    q = [
        ("Je Moodle opravdu zdarma?", "Software ano. Platíte ale server, instalaci, aktualizace, zálohy a úpravy vzhledu. U větších instalací to bývá víc než licence LearnDash."),
        ("Dá se kurz přenést z Moodlu do LearnDash?", "Obsah ano, ručně nebo přes SCORM balíčky. Historii výsledků žáků je potřeba řešit zvlášť."),
        ("Co je SCORM?", "Standardní formát e-learningových balíčků. Hodí se, když kurzy kupujete od externích autorů nebo je chcete přenášet mezi systémy."),
        ("Pomůžete s výběrem?", "Ano. Popište, kdo se bude vzdělávat, kolik lidí a jestli chcete kurzy prodávat, a doporučíme řešení i s cenou."),
    ]
    body += cta_split("Časté dotazy", "E-learning: na co se ptáte", "Poradíme, jestli se vám víc hodí LearnDash, nebo Moodle, a postavíme řešení na klíč.", q)
    body += disclosure() + related(path)
    head = article(path, "LearnDash, nebo Moodle? Srovnání", md, cr, q)
    return (meta(path, "LearnDash, nebo Moodle? Srovnání pro online kurzy | webovybalicek", md, head,
                 {"k": "Srovnání", "h": "LearnDash, nebo *Moodle*?", "tags": ["E-learning", "WordPress", "LMS"]}), body)


# ---------------------------------------------------------------- slevy ve WooCommerce
def slevy_woo():
    path = "/e-shop/slevy-a-akce-ve-woocommerce/"
    md = "Jak nastavit slevy a akce ve WooCommerce: kupóny, množstevní slevy, 2+1 zdarma, slevy podle kategorie a velkoobchodní ceny. Co umí WooCommerce sám a kdy potřebujete plugin."
    cr = [("Domů", "/"), ("Slevy a akce ve WooCommerce", path)]
    body = hero([("Domů", "/"), ("Slevy a akce ve WooCommerce", None)], "Slevy a akce *ve WooCommerce*",
                "Kupóny, množstevní slevy, 2+1 zdarma, Black Friday nebo ceny pro velkoodběratele. Co zvládne WooCommerce sám, kdy sáhnout po pluginu a na co nezapomenout kvůli zákonu.",
                '<p class="hero-actions"><a href="#moznosti" class="btn btn--primary">Možnosti slev</a><a href="/kontakt/" class="btn btn--outline">Nastavíme to za vás</a></p>')
    body += answer("Krátká odpověď", "Jednoduché kupóny a zlevněnou cenu produktu umí WooCommerce sám. Na množstevní slevy, akce typu 2+1, slevy na kategorii nebo automatické slevy v košíku potřebujete plugin, nejčastěji Discount Rules od Flycartu. Ceny pro firmy řeší plugin Velkoobchod.")
    body += f'''  <section class="section" id="moznosti">
    <div class="wrap">
      <div class="section-head"><p class="pill">Možnosti</p><h2>Co čím nastavíte</h2></div>
      {table(["Typ slevy", "WooCommerce sám", "S pluginem"], [
        ["Akční cena produktu", "ano, i s časovým omezením", "ano"],
        ["Slevový kupón", "ano: procenta, pevná částka, doprava zdarma, omezení na produkty a e-maily", "ano"],
        ["Množstevní sleva", "ne", "Discount Rules: sleva podle počtu kusů s tabulkou na produktu"],
        ["2+1 zdarma, dárek k nákupu", "ne", "Discount Rules (BOGO pravidla)"],
        ["Sleva na celou kategorii", "jen ručně u každého produktu", "Discount Rules Pro"],
        ["Ceny pro velkoodběratele", "ne", "Velkoobchod od Toretu: registrace firem, vlastní ceny, platba na fakturu"],
      ])}
    </div>
  </section>
'''
    body += f'''  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="pill">Pluginy</p><h2>Které pluginy používáme</h2></div>
      <div class="grid-cards">
        <article class="card pay-card"><h3>Discount Rules for WooCommerce</h3><p>Od Flycartu. Základní verze je zdarma na WordPress.org, verze Pro přidá slevy na kategorie, akce typu kup X a dostaneš Y a další podmínky. Licence je roční.</p><p>{out("flycart", "Discount Rules Pro")}</p></article>
        <article class="card pay-card"><h3>Velkoobchod</h3><p>B2B prodej: registrace velkoodběratelů s kontrolou IČ, globální, individuální i množstevní slevy, minimální objednávka.</p><p><a href="{PLUG}velkoobchod/" class="link">Plugin Velkoobchod</a></p></article>
        <article class="card pay-card"><h3>Toolkit</h3><p>Hlídá zákonné povinnosti při slevách: zobrazí nejnižší cenu za posledních 30 dní a graf vývoje ceny.</p><p><a href="{PLUG}toolkit/" class="link">Plugin Toolkit</a></p></article>
      </div>
    </div>
  </section>
'''
    body += section("Pozor na zákon", "Sleva musí být poctivá", ticks([
        "Když oznamujete slevu, uvádějte ji z nejnižší ceny, za kterou jste zboží prodávali v posledních 30 dnech.",
        "Přeškrtnutá cena, která nikdy neplatila, je klamání zákazníka a hrozí za ni pokuta.",
        "Hlídání 30denní ceny je ruční práce. Plugin ji spočítá a zobrazí sám.",
        "U akcí s časovým omezením nastavte začátek i konec, ať sleva nezůstane běžet.",
    ]))
    q = [
        ("Jak udělat slevu na celou kategorii?", "Ručně byste museli upravit cenu u každého produktu. Plugin Discount Rules nastaví jedno pravidlo pro celou kategorii a po akci ho jen vypnete."),
        ("Jde kombinovat kupón a automatickou slevu?", "Ano. V Discount Rules se nastavuje, jestli se slevy sčítají, nebo platí jen ta nejvyšší."),
        ("Jak nastavit Black Friday?", "Pravidlo se slevou a datem začátku a konce. Nezapomeňte na nejnižší cenu za 30 dní a na kapacitu hostingu, protože návštěvnost vyskočí."),
        ("Nastavíte nám akce?", "Ano, nastavíme pravidla, otestujeme košík a pohlídáme zákonné náležitosti."),
    ]
    body += cta_split("Časté dotazy", "Slevy: na co se ptáte", "Nastavíme slevy, akce a ceny pro velkoodběratele tak, aby fungovaly a byly v souladu se zákonem.", q)
    body += disclosure() + related(path, [(PLUG, "Doporučené pluginy")])
    head = article(path, "Slevy a akce ve WooCommerce", md, cr, q)
    return (meta(path, "Slevy a akce ve WooCommerce: kupóny, 2+1, množstevní slevy | webovybalicek", md, head,
                 {"k": "Návod", "h": "Slevy *ve WooCommerce*", "tags": ["Kupóny", "Akce", "Pluginy"]}), body)


# ---------------------------------------------------------------- slevové kódy
def kody(src):
    path = "/slevove-kody/"
    md = "Slevové kódy a akce na pluginy pro WooCommerce, WordPress nástroje a služby pro weby: Toret, Crocoblock, Wedos a další. Ověřené akce s datem platnosti."
    cr = [("Domů", "/"), ("Slevové kódy a akce", path)]
    data = json.loads((src / "data" / "slevy.json").read_text(encoding="utf-8"))
    today = datetime.date.today().isoformat()
    akce = [a for a in data.get("akce", []) if not a.get("do") or a["do"] >= today]
    body = hero([("Domů", "/"), ("Slevové kódy a akce", None)], "Slevové kódy a *akce*",
                "Slevy na pluginy, nástroje a služby, které sami používáme na webech klientů. Uvádíme jen akce ověřené u výrobce, s datem platnosti.",
                '<p class="hero-actions"><a href="#toret" class="btn btn--primary">Sleva na pluginy Toret</a></p>')
    body += f'''  <section class="section" id="toret">
    <div class="wrap">
      <div class="sleva sleva--bar" id="sleva">
        <div class="sleva-copy">
          <span class="sleva-tag">Sleva 15 %</span>
          <h2>Pluginy Toret pro WooCommerce</h2>
          <p>Nechte nám e-mail a pošleme vám náš slevový kód na pluginy Toret: dopravci, platební brány, fakturace i marketing. Uplatníte ho v košíku na toret.cz.</p>
        </div>
        <form class="sleva-form" data-sleva novalidate>
          <label class="sleva-field"><span class="sr-only">E-mail</span><input type="email" name="email" required placeholder="vas@email.cz" autocomplete="email"></label>
          <button type="submit" class="btn btn--primary">Poslat kód</button>
          <p class="sleva-msg" role="status" aria-live="polite"></p>
        </form>
      </div>
    </div>
  </section>
'''
    if akce:
        tiles = "".join(
            f'<article class="card pay-card"><p class="pill">{e(_AFFIL[a["affil"]]["n"])}</p><h3>{e(a["n"])}</h3><p>{e(a.get("popis", ""))}</p>'
            + (f'<p>Kód: <strong>{e(a["kod"])}</strong></p>' if a.get("kod") else "")
            + f'<p class="note note--small">{"Platí do " + datetime.date.fromisoformat(a["do"]).strftime("%-d. %-m. %Y") + ". " if a.get("do") else ""}Ověřeno {datetime.date.fromisoformat(a["overeno"]).strftime("%-d. %-m. %Y")}.</p>'
            + f'<p>{out(a["affil"], "Využít akci")}</p></article>' for a in akce)
        body += section("Aktuálně", "Probíhající akce", f'<div class="grid-cards">{tiles}</div>')
    else:
        body += answer("Aktuálně", "Právě teď neevidujeme žádnou další ověřenou akci. Stránku průběžně aktualizujeme, jakmile výrobci akci vyhlásí.")
    sl = [("crocoblock", "Crocoblock", "JetEngine, JetSmartFilters, JetFormBuilder a další pluginy pro Elementor."),
          ("wedos", "Wedos", "Český webhosting a domény."),
          ("flycart", "Flycart", "Discount Rules a další pluginy pro WooCommerce."),
          ("learndash", "LearnDash", "Online kurzy na WordPressu."),
          ("comgate", "Comgate", "Platební brána pro e-shopy."),
          ("idoklad", "iDoklad", "Online fakturace s napojením na e-shop.")]
    tiles = "".join(f'<article class="card pay-card"><h3>{e(n)}</h3><p>{e(d)}</p><p>{out(k, "Na web " + n)}</p></article>' for k, n, d in sl)
    body += section("Služby", "Co doporučujeme", f'<div class="grid-cards">{tiles}</div>')
    q = [
        ("Jak často stránku aktualizujete?", "Každý týden kontrolujeme akce od výrobců. Akce po skončení platnosti ze stránky mizí."),
        ("Proč je kód na Toret posílaný e-mailem?", "Kód je neveřejný a dohodnutý s výrobcem. Pošleme vám ho hned po vyplnění e-mailu."),
        ("Platí kódy i pro prodloužení licence?", "Záleží na podmínkách konkrétní akce. Ověřte si je v košíku u výrobce."),
    ]
    body += cta_split("Časté dotazy", "Slevy: na co se ptáte", "Nechcete pluginy kupovat a nastavovat sami? Vybereme, koupíme se slevou a nastavíme je na váš e-shop.", q)
    body += disclosure() + related(path)
    head = ld([{"@context": "https://schema.org", "@type": "WebPage", "name": "Slevové kódy a akce", "description": md, "url": SITE + path,
                "publisher": ORG, "inLanguage": "cs", "dateModified": today}, crumbs_ld(cr), faq_ld(q)])
    return (meta(path, "Slevové kódy a akce: pluginy WooCommerce, WordPress, hosting | webovybalicek", md, head,
                 {"k": "Slevy", "h": "Slevové *kódy*", "tags": ["Toret", "WordPress", "Hosting"]}), body)


def pages(src: Path):
    affil(src)
    return [brany(), fakturace(), learndash(), moodle(), slevy_woo(), kody(src)]
