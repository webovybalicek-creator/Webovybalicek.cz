# Samostatné stránky pojmů /slovnicek/<slug>/. Krátká definice se bere ze slovníčku
# (src/pages/nejcastejsi-pojmy-ohledne-tvorby-webu.html, <dt>/<dd>), tady je rozšíření:
# p = odstavce, tip = jak to řešíme my, rel = související pojmy (slugy), link = (text, url) odkaz na službu.

P = {
    "webhosting": dict(
        p=["Web je sada souborů a databáze, které musí někde nepřetržitě běžet. Hostingová společnost vám pronajme místo na svém serveru, stará se o jeho chod, zabezpečení a připojení k internetu.",
           "Hostingy se liší výkonem, umístěním serverů, zálohováním a podporou. Pro firemní web na WordPressu stačí kvalitní sdílený hosting, e-shop s větším provozem potřebuje víc výkonu."],
        tip="Hosting vybereme podle typu webu, nebo zajistíme vlastní. Weby provozujeme u českých hostingů se zálohami a rychlou podporou.",
        rel=["server", "domena", "dns", "ssl-certifikat"], link=("Správa webu", "/sprava-webu/")),
    "server": dict(
        p=["Server je výkonný počítač v datovém centru, který běží nonstop a obsluhuje požadavky z internetu. Když někdo otevře váš web, server mu pošle stránky, obrázky a data.",
           "Na jednom serveru běží často stovky webů (sdílený hosting). Velké projekty mívají vlastní virtuální nebo fyzický server."],
        tip="O servery se starat nemusíte. Hosting zvolíme tak, aby měl web dost výkonu i rezervu do budoucna.",
        rel=["webhosting", "databaze", "dns"], link=None),
    "domena": dict(
        p=["Doména je jméno, pod kterým lidé váš web najdou, například webovybalicek.cz. Neplatíte ji jednou, ale pronajímáte na rok nebo několik let u registrátora.",
           "Na doménu se vážou i firemní e-maily (vy@vasefirma.cz). Proto je dobré, aby byla registrovaná na vás a ne na dodavatele webu."],
        tip="Doménu vždy registrujeme na klienta. Pomůžeme vybrat název, zkontrolovat dostupnost a nastavit DNS i e-maily.",
        rel=["dns", "webhosting", "ssl-certifikat"], link=("Jak probíhá spolupráce", "/jak-probiha-tvorba-webu-a-nase-spoluprace/")),
    "dns": dict(
        p=["DNS je jako telefonní seznam internetu. Převádí název domény na adresu serveru, kde web běží, a určuje, kam doručovat e-maily.",
           "Při stěhování webu nebo změně e-mailů se mění právě záznamy v DNS. Chybné nastavení umí odstřihnout web nebo poštu, proto se vyplatí ho svěřit někomu, kdo ví, co dělá."],
        tip="DNS nastavujeme při spuštění webu i při stěhování hostingu tak, aby web ani e-maily nevypadly.",
        rel=["domena", "webhosting", "server"], link=None),
    "ssl-certifikat": dict(
        p=["SSL certifikát šifruje komunikaci mezi návštěvníkem a webem. Poznáte ho podle https:// a zámku v adresním řádku prohlížeče.",
           "Bez certifikátu prohlížeče web označí jako nezabezpečený a odradí návštěvníky. Google weby s https upřednostňuje a u formulářů a e-shopů je šifrování nutnost."],
        tip="SSL nastavujeme u každého webu zdarma (Let’s Encrypt) a hlídáme jeho automatické obnovování.",
        rel=["webhosting", "domena", "gdpr"], link=None),
    "databaze": dict(
        p=["Databáze je úložiště, ze kterého web skládá stránky: texty článků, produkty, objednávky, uživatele nebo nastavení.",
           "WordPress ukládá obsah do databáze MySQL nebo MariaDB. Pravidelné zálohy databáze jsou stejně důležité jako zálohy souborů."],
        tip="V rámci správy webu databázi pravidelně zálohujeme a čistíme, aby web zůstal rychlý.",
        rel=["cms", "wordpress", "server"], link=("Správa webu", "/sprava-webu/")),
    "cms": dict(
        p=["CMS (Content Management System) je redakční systém. Díky němu upravíte texty, obrázky nebo přidáte článek bez znalosti programování.",
           "Nejrozšířenější je WordPress, dále třeba Joomla nebo Drupal. Pronajímané systémy jako Wix nebo Shoptet mají vlastní CMS, ze kterého web nejde přenést jinam."],
        tip="Kde si chcete obsah spravovat sami, stavíme na WordPressu s Elementorem. U AI webů úpravy uděláme za vás.",
        rel=["wordpress", "plugin", "dynamicky-obsah"], link=("Srovnání: WordPress, nebo Wix?", "/srovnani/wordpress-vs-wix/")),
    "wordpress": dict(
        p=["WordPress pohání zhruba 40 % všech webů na světě. Je zdarma, má obrovskou komunitu a desítky tisíc rozšíření.",
           "Hodí se pro firemní weby, magazíny i e-shopy (s WooCommerce). Vyžaduje ale pravidelné aktualizace a zabezpečení, jinak zastarává."],
        tip="Na WordPressu s Elementorem stavíme prezentační weby a e-shopy a staráme se o jejich aktualizace.",
        rel=["cms", "plugin", "platebni-brana"], link=("Prezentační web na WordPressu", "/srovnani/")),
    "plugin": dict(
        p=["Plugin přidá do WordPressu funkci, kterou základní systém nemá: kontaktní formulář, e-shop, napojení na dopravce, fakturaci nebo SEO nástroje.",
           "Platí méně je více. Každý plugin zatěžuje web a je potřeba ho aktualizovat. Vybírat se vyplatí prověřené pluginy od spolehlivých autorů."],
        tip="Pro české e-shopy používáme prověřené pluginy od Toretu. Jejich přehled najdete na stránce Doporučené pluginy.",
        rel=["wordpress", "zasilkovna", "platebni-brana"], link=("Doporučené pluginy", "/doporucene-pluginy/")),
    "design-na-miru": dict(
        p=["Design na míru vzniká pro konkrétní firmu: vychází z její značky, zákazníků a cílů webu. Není to upravená hotová šablona.",
           "Výsledkem je web, který se odliší od konkurence, je rychlejší (bez zbytečného kódu) a dobře se rozšiřuje."],
        tip="Každý web navrhujeme na míru. AI nám zrychlí návrh i vývoj, takže design na míru máme od 20 000 Kč.",
        rel=["dynamicky-obsah", "slider-banner", "optimalizace-obrazku"], link=("Srovnání: web na míru, nebo šablona?", "/srovnani/web-na-miru-vs-sablona/")),
    "dynamicky-obsah": dict(
        p=["Dynamický obsah se na stránky vkládá automaticky z dat. Přidáte novou referenci, produkt nebo článek a objeví se všude, kde má.",
           "Ušetří to práci a hlídá jednotný vzhled. Typicky jde o výpisy referencí, produktů, akcí, nemovitostí nebo členů týmu."],
        tip="Výpisy a filtry stavíme tak, abyste nový obsah jen vyplnili do formuláře a o vzhled se nestarali.",
        rel=["filtr", "databaze", "cms"], link=None),
    "filtr": dict(
        p=["Filtr pomáhá návštěvníkovi rychle najít, co hledá: produkty podle ceny a velikosti, nemovitosti podle lokality nebo kurzy podle termínu.",
           "Dobrý filtr funguje bez načítání celé stránky a ukazuje jen možnosti, které dávají výsledky."],
        tip="Filtry stavíme pro e-shopy, katalogy i realitní weby, rychlé i na mobilu.",
        rel=["dynamicky-obsah", "databaze"], link=("Katalogy a vyhledávače", "/tvorba-webu/katalog-a-vyhledavac/")),
    "slider-banner": dict(
        p=["Slider je pás obrázků nebo sdělení, které se automaticky střídají, typicky nahoře na úvodní stránce.",
           "Vypadá efektně, ale návštěvníci většinou vidí jen první snímek a slidery zpomalují načítání. Často funguje lépe jedno silné sdělení."],
        tip="Slidery používáme jen tam, kde dávají smysl, třeba u galerie nebo referencí.",
        rel=["design-na-miru", "optimalizace-obrazku", "pop-up-okno"], link=None),
    "pop-up-okno": dict(
        p=["Pop-up je okno, které se otevře nad stránkou: nabídka slevy, přihlášení k newsletteru nebo upozornění.",
           "Dobře načasovaný pop-up zvýší konverze, otravný naopak návštěvníky odežene. Google penalizuje pop-upy, které na mobilu zakryjí obsah hned po příchodu."],
        tip="Pop-upy nastavujeme s rozumem: až po chvíli na webu nebo při odchodu, a vždy jdou snadno zavřít.",
        rel=["slider-banner", "cookie"], link=None),
    "optimalizace-obrazku": dict(
        p=["Obrázky tvoří většinu objemu webu. Optimalizace je zmenší a převede do moderních formátů (WebP, AVIF), aniž by viditelně ztratily kvalitu.",
           "Rychlejší web lépe konvertuje i lépe se umisťuje ve vyhledávání. Obrázky se navíc mají načítat až ve chvíli, kdy na ně návštěvník doroluje."],
        tip="Obrázky optimalizujeme u každého webu automaticky, včetně správných rozměrů pro mobil.",
        rel=["seo", "design-na-miru"], link=None),
    "platebni-brana": dict(
        p=["Platební brána zpracuje platbu kartou, Apple Pay, Google Pay nebo rychlý bankovní převod přímo na webu. Peníze pak přijdou na váš účet.",
           "V Česku jsou rozšířené například GoPay, Comgate, ThePay nebo Stripe. Liší se poplatky, rychlostí výplat a podporovanými metodami."],
        tip="Platební bránu vybereme podle obratu a typu prodeje a napojíme ji na e-shop i fakturaci.",
        rel=["zasilkovna", "xml-feed", "plugin"], link=("E-shopy", "/tvorba-webu/e-shop/")),
    "zasilkovna": dict(
        p=["Zásilkovna je jeden z nejoblíbenějších dopravců v Česku a na Slovensku, s tisíci výdejních míst a Z-BOXů.",
           "E-shop se na ni napojuje pluginem. Zákazník si v košíku vybere výdejní místo na mapě a vy tisknete štítky přímo z administrace."],
        tip="Napojení na Zásilkovnu, PPL, DPD i Balíkovnu řešíme prověřenými pluginy od Toretu.",
        rel=["platebni-brana", "plugin", "xml-feed"], link=("Plugin Zásilkovna pro WooCommerce", "/doporucene-pluginy/zasilkovna/")),
    "xml-feed": dict(
        p=["XML feed je soubor se seznamem produktů, cen a dostupnosti, který e-shop pravidelně generuje.",
           "Načítají si ho srovnávače zboží (Heureka, Zboží.cz, Google Nákupy) i reklamní systémy. Díky němu jsou vaše produkty vidět mimo e-shop."],
        tip="Feedy pro Heureku, Zboží.cz i Google nastavíme při spuštění e-shopu.",
        rel=["platebni-brana", "zasilkovna", "seo"], link=("Doporučené pluginy", "/doporucene-pluginy/")),
    "seo": dict(
        p=["SEO je soubor úprav, díky kterým vás vyhledávače lépe pochopí a ukážou výš: rychlost, struktura, texty, nadpisy, odkazy a technické nastavení.",
           "Dobré SEO začíná už při stavbě webu. Dodatečně opravovat špatnou strukturu bývá dražší než ji postavit správně hned."],
        tip="Základní SEO je součástí každého webu: struktura, rychlost, meta popisy, strukturovaná data a sitemapa.",
        rel=["geo", "aeo", "strukturovana-data"], link=("Co obnáší tvorba webu", "/obsah-cinnosti-pri-tvorbe-webu/")),
    "geo": dict(
        p=["GEO cílí na to, aby vás zmínily AI asistenty jako ChatGPT, Gemini, Perplexity nebo Claude, když se jich lidé ptají na doporučení.",
           "AI čerpají z webů, které jsou srozumitelné, mají jasná fakta (ceny, kontakty, služby), strukturovaná data a dobrou pověst na dalších webech."],
        tip="Weby připravujeme i pro AI: přehledné odpovědi, strukturovaná data, soubor llms.txt a povolený přístup AI vyhledávačů.",
        rel=["seo", "aeo", "strukturovana-data"], link=("AI weby", "/ai-weby/")),
    "aeo": dict(
        p=["AEO je optimalizace pro přímé odpovědi: úryvky ve výsledcích Googlu, odpovědi hlasových asistentů a AI souhrny nad výsledky.",
           "Pomáhají krátké jasné odpovědi na konkrétní otázky, sekce častých dotazů a strukturovaná data typu FAQ."],
        tip="Časté dotazy na webu označujeme strukturovanými daty, aby z nich vyhledávače mohly přímo odpovídat.",
        rel=["seo", "geo", "strukturovana-data"], link=("Časté dotazy", "/nejcastejsi-dotazy/")),
    "strukturovana-data": dict(
        p=["Strukturovaná data (schema.org) jsou popisky v kódu, které návštěvník nevidí. Vyhledávačům řeknou, že jde o firmu, produkt, cenu, recenzi nebo událost.",
           "Díky nim se ve výsledcích můžou objevit hvězdičky, ceny nebo otázky a odpovědi. Používají je i AI asistenti."],
        tip="Strukturovaná data doplňujeme u každého webu: firma, služby, produkty, časté dotazy a drobečková navigace.",
        rel=["seo", "geo", "aeo"], link=None),
    "google-analytics": dict(
        p=["Google Analytics ukazuje, kolik lidí na web přišlo, odkud (Google, sociální sítě, reklama), co si prohlíželi a jestli poptali nebo nakoupili.",
           "V EU smí měřit až po souhlasu návštěvníka v cookie liště. Bez měření se ale těžko pozná, co na webu funguje."],
        tip="Analytiku nastavujeme se souhlasem přes cookie lištu (Consent Mode v2) a měříme poptávky i nákupy.",
        rel=["cookie", "gdpr", "hotjar"], link=None),
    "hotjar": dict(
        p=["Hotjar ukazuje, jak se lidé na webu chovají: kam klikají, kam až scrollují a kde odcházejí. Umí nahrávat anonymní záznamy návštěv.",
           "Hodí se k odhalení míst, kde se návštěvníci zasekávají, třeba ve formuláři nebo v košíku."],
        tip="Nástroje jako Hotjar nebo Microsoft Clarity nasazujeme se souhlasem v cookie liště.",
        rel=["google-analytics", "cookie", "gdpr"], link=None),
    "cookie": dict(
        p=["Cookie je malý soubor, který si web uloží do prohlížeče návštěvníka: přihlášení, obsah košíku, nastavení nebo měření návštěvnosti.",
           "Nezbytné cookies smí web používat vždy, analytické a marketingové až po souhlasu. Proto weby v EU potřebují cookie lištu."],
        tip="Cookie lištu stavíme podle pravidel EU: bez souhlasu se nic neměří a volba jde kdykoli změnit.",
        rel=["gdpr", "google-analytics", "hotjar"], link=("Zásady cookies", "/zasady-cookies-eu/")),
    "gdpr": dict(
        p=["GDPR je evropské nařízení o ochraně osobních údajů. Týká se každého webu, který sbírá jména, e-maily, telefony nebo objednávky.",
           "Web musí informovat, jaké údaje zpracovává a proč, zabezpečit je a sbírat jen to, co opravdu potřebuje."],
        tip="Formuláře, cookie lištu a zabezpečení stavíme v souladu s GDPR. Texty zásad vám doporučíme nechat zkontrolovat právníkem.",
        rel=["cookie", "ssl-certifikat", "google-analytics"], link=("Ochrana osobních údajů", "/ochrana-informaci-gdpr/")),
    "ai-web": dict(
        p=["AI web je web na míru, při jehož stavbě nám umělá inteligence zrychlí návrh, texty i programování. Každý krok ale kontroluje a ladí člověk.",
           "Výsledkem je rychlý moderní web za nižší cenu a v kratším čase. Obsah upravujeme za vás, nebo si ho můžete měnit sami přes jednoduchou administraci."],
        tip="AI web stavíme od 20 000 Kč, obvykle hotový během dnů.",
        rel=["prezentacni-web", "ai-chatbot", "design-na-miru"], link=("AI weby", "/ai-weby/")),
    "prezentacni-web": dict(
        p=["Prezentační web představuje firmu, její služby, reference a kontakty. Jeho cílem je získat poptávky a důvěru.",
           "U nás ho stavíme na WordPressu s Elementorem, takže si texty, fotky a stránky upravujete sami."],
        tip="Prezentační web stavíme od 25 000 Kč, s designem na míru a základním SEO.",
        rel=["ai-web", "wordpress", "cms"], link=("Jaký web je pro vás?", "/srovnani/")),
    "ai-chatbot": dict(
        p=["AI chatbot odpovídá návštěvníkům nonstop na základě obsahu vašeho webu a podkladů: ceny, otevírací doba, postupy, dostupnost.",
           "Ušetří čas na opakované dotazy a zachytí poptávky i mimo pracovní dobu. Složité dotazy předá člověku."],
        tip="AI asistenta napojíme na váš obsah a nastavíme, kdy má předat konverzaci vám. Není součástí ceny webu.",
        rel=["ai-web", "geo"], link=("AI asistent a chatbot", "/tvorba-webu/ai-chatbot/")),
}
