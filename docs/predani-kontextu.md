# Předání kontextu – web webovybalicek.cz (stav 26. 11. 2026, spuštěno na ostré doméně)

Redesign mého webu webovybalicek.cz je hotový a běží na https://webovybalicek.cz. Staging new.webovybalicek.cz i repo New.webovybalicek.cz jsou zrušené. **Komunikuj výhradně česky** (i průběžné poznámky), stručně a věcně.

## ⚠️ Pravidlo: SEO stránky mimo navigaci
Nové stránky jen pro SEO (od 25. 11. 2026) **nedávat do patičky ani do rozcestníků** – jsou jen v sitemapě (+ IndexNow) a prolinkované mezi sebou. U řešení a srovnání to řídí `seo_only=True` v datech (vyřadí je z `/reseni/`, z `/kolik-stoji-web/` a ze souvisejících u běžných stránek). Stránky ze `src/seo_more.py` se z běžných stránek neodkazují vůbec.
- Téma dotací Vladimír řešit nechce – stránka `/dotace-na-web-a-e-shop/` smazána (410 Gone v `static/.htaccess`).
- Pozn.: GitHub Actions 25. 11. blokoval billing; 26. 11. po zveřejnění repa znovu funguje.

## ⚠️ Pravidlo: náhledovka ke každé URL
Každá veřejná URL má vlastní náhledový obrázek pro sdílení (og:image 1200×630) ve stylu úvodu: perleťová hmota, limetkové kapky, tečkový rastr, kurzory se štítky, nadpis s limetkovým podtržením, logo jako v hlavičce. **Při každé nové stránce ho rovnou vytvoř:**
1. Stránka ze `src/pages/` → přidej řádek do `OG_PAGES` v build.py: `"/cesta/": ("NADTITULEK", "Nadpis s *podtrženým* slovem")`. Landing page typu webu, plugin nebo SEO stránka → `meta["og"]` v `src/typy.py` / `src/plugins.py` / `src/seo.py` / `src/seo_extra.py` / `src/seo_more.py` (k, h, pill, tags) – generuje se samo.
2. `python3 build.py` (zapíše `tools/og-jobs.json`) → `python3 tools/og.py` (vyrenderuje jen chybějící do `assets/img/og/p/<slug>.jpg`) → `python3 build.py` (stránka převezme obrázek) → commit + push.
3. Ověř obrázek (nadpis se nesmí potkat s kapkami) a na webu `og:image`.
- `python3 tools/og.py --vse` přegeneruje vše (po změně šablony), `python3 tools/og.py slug slug` jen vybrané. Úvodní stránka se kopíruje i do `assets/img/og/default.jpg`.
- Stejnou šablonou (`og.page(job)`) jdou vyrenderovat i fotky pro Firemní profil / sociální sítě s vlastními texty.
- Pozn.: náhledovky zatím zobrazují starou perleťovou hmotu (úvod ji od 24. 11. nemá) – případně přegenerovat v duchu nového úvodu (tečky).

## Indexace (25. 11. 2026)
- **Google:** sitemap přečtena 25. 11., objeveno 148 URL; vzorek 10 nových stránek napříč sekcemi – všechny v indexu. Report Indexování se teprve zpracovával. Search Console: fischer.vlada@gmail.com, služba `sc-domain:webovybalicek.cz`.
- **Bing:** 25. 11. odesláno ručně 100 URL; 26. 11. IndexNow při deployi ohlásil všech 166 URL (odpověď 202), pak znovu po úpravě patičky (200).
- **Seznam:** web je pod účtem webovybalicek@gmail.com (ne fischer.vlada). Ruční přidání URL (search.seznam.cz/wt/pridej-stranku) má CAPTCHA – Claude ji nevyplňuje. Seznam podporuje IndexNow, ohlašuje se automaticky.
- **IndexNow (automaticky při každém deployi):** `tools/indexnow.py` + klíč `static/4f1c9b7e2a6d48c3b0e5a91d7c2f6e38.txt`. V `deploy.yml` krok „priprav“ před FTP porovná otisky stránek (bez `?v=VERZE`) s `/indexnow-stav.json` na webu a zapíše nový stav do dist; krok „odesli“ po FTP pošle jen nové, změněné i smazané URL na api.indexnow.org (Bing, Seznam, Yandex…). Změna layoutu (patička) = ohlásí se celý web. Google IndexNow nepodporuje – čte sitemap.
- Doporučení: Google Search Console propojit s GA4 (GA4 to samo nabízí na úvodní stránce).

## Měření poptávek (GA4, od commitu a9eb917)
- GA4 `G-NC8R87KWWH`, služba „webovybalicek.cz - GA4“ (účet webovybalicek.cz, ID služby 382291374, přístup fischer.vlada@gmail.com). Načítá se jen po souhlasu v cookie liště.
- `main.js` → `wbTrack(name, params)` (také `window.wbTrack`): pošle událost jen se souhlasem s analytikou. Události:
  - `generate_lead` – úspěšně odeslaný formulář přes poptavka.php (parametry `form_segment` klient/agentura, `form_type` = hodnota `type`, `from_calc` ano/ne, `page_path`)
  - `contact_phone`, `contact_email` – klik na `tel:` / `mailto:` odkaz kdekoli na webu
  - `calculator_use` – první změna v kalkulačce na stránce
  - `discount_code_request` – odeslaný formulář slevového kódu Toret
- Nasazeno 26. 11. 2026. **Zbývá:** v GA4 (Správce → Zobrazení dat → Události) označit hvězdičkou jako klíčové `generate_lead`, `contact_phone`, `contact_email`. V novém rozhraní to jde až poté, co událost poprvé dorazí (první skutečná poptávka / klik).
- `form_type` hodnoty: `ai`, `wordpress`, `eshop`, `hybrid`, `sprava`, `kontrola`, `a-*` (spolupráce).

## Obsahový plán pro poptávky (25. 11. 2026)
Analýza: Claude Doc „🔎 webovybalicek – indexace a obsahový plán pro poptávky“ (https://claude.ai/artifact/RP7tEzNSsYzheVzEueD3NF). Hotovo vše kromě bodu „Zákon o přístupnosti“ (Vladimír zatím nechce); dotace smazány (nechce řešit).
Nové SEO stránky (17 URL, celkem 165 stránek, nasazeno 26. 11.) – **mimo patičku a rozcestníky**:
- `/kontrola-webu-zdarma/` – lead magnet, formulář `type=kontrola` s polem `site` (adresa webu se propíše do e-mailu). Slib: odpověď do 48 hodin, web projde člověk.
- Ceny: `/kolik-stoji-e-shop/`, `/kolik-stoji-sprava-webu/`, `/kolik-stoji-redesign-webu/` (data `CENY` v seo_more.py; ceny z ceníku: AI web 20 000, prezentační 25 000, e-shop 35 000, B2B od 45 000, správa od 600 Kč/měs., hosting od 1 200 Kč/rok).
- Řešení (`src/data/seo-reseni.py`, blok „doplněno 25. 11.“): `prechod-ze-shoptetu-na-woocommerce`, `prevod-webu-z-webnode`, `web-nechodi-poptavky`.
- Srovnání (`src/data/seo-srovnani.py`): `ai-web-vs-wordpress`, `shopify-vs-woocommerce`, `agentura-vs-freelancer` (pravidlo „nejlépe vychází náš web“ dodrženo).
- `/geo-optimalizace/` – web v odpovědích ChatGPT a Google AI.
- `/spoluprace-pro-agentury/` – white-label a subdodávky (patička dál odkazuje na /#spoluprace).
- Případové studie `/projekty/` + `/projekty/kabiny-kravak/`, `/mmnt/`, `/jamie-collection/`, `/facer/` – data `src/data/pripadovky.py`. **Jen ověřená fakta**, pole `vysledek` a `citace` (+ `citace_od`) jsou prázdná a nevypisují se – Vladimír má doplnit čísla a citace klientů. U Kabin a MMNT velká fotka z `assets/img/projekty/` (pole `foto`), jinak náhled webu přes `shots_pick`.
- Patička ani rozcestníky na nové stránky neodkazují (pravidlo nahoře).
- Další kroky z plánu: Zákon o přístupnosti + audit (odloženo), lokality (Mníšek, Černošice, Beroun, Dobříš, Benešov, Brandýs) jen s vlastním obsahem, `/tvorba-webu-slovensko/`, obory podle referencí, CTA „Napojíme vám to“ na stránkách pluginů, kontextová CTA ve slovníčku. Po 4–6 týdnech projít Search Console (dotazy s vysokými zobrazeními a nízkým CTR).

## Úvod (homepage) – tečky v rohu (`assets/js/hero-dots.js`, od 24. 11. 2026)
- Perleťová WebGL bublina (hero-blob.js) je pryč. Místo ní: tečky pozadí (stejná mřížka 22 px jako `.air-dots`) v pravém horním rohu pravidelně rostou – halftone od velkých v rohu k nejmenším (= tečky pozadí), šedé.
- Najetí myší: tečky pod kurzorem vtečou do jedné pravidelné kuličky, ta okolní tečky odtlačuje (žádné uhýbání teček do díry).
- Z rohu jde vytáhnout 6 kuliček = 6 bodů z `[data-hero-points]` (Strategie, Know-how, Texty, Design, Technika, AI); při tahu řetízek, který se utrhne; klik do teček uvolní další, tah přes tečky „uřízne“, puštění zpět do rohu vrátí, „Spojit zpět“ vrátí vše; „Design“ se co chvíli sama vystrčí. Každá vytažená kulička ubere ~6 % rohu, část v rohu zůstane vždy.
- Barevná varianta **C** (vybrána Vladimírem): vše šedé, limetková jen vybraná kulička (ke které je zobrazený text). Pro porovnání `?uvod=a` (vše šedé) / `?uvod=b` (limetkové kuličky).
- 2D plátno, běží hned po načtení (žádné čekání), PageSpeed lokálně mobil ~96, desktop ~97.

## Rychlost webu
- Kurzory v úvodu startují hned po načtení (`window.wbGo`), reference (pruh i „stavění“ snímků) bez čekání. `window.wbTouch` (první akce návštěvníka) zůstává v main.js pro případnou těžkou animaci (WebGL apod.) – ta by se jinak propsala do PageSpeedu (laboratorní test běží bez GPU, s WebGL hned po načtení mobil ~60).
- Obrázky: menší varianty pro srcset (reference 480 px, fotky projektů 960 px) vytváří `tools/varianty.py` **automaticky při každém deployi** (deploy.yml, kontrola podle otisku v `.zdroj.json`) – ručně se nic hlídat nemusí. build.py použije variantu jen, když existuje.
- `.htaccess`: komprese, CSS/JS cache 1 rok (vždy s ?v=VERZE), obrázky a písma 30 dní. `assets/img/og/.htaccess` povoluje CORS (kvůli nahrávání náhledovek do Firemního profilu).
- CSS se při buildu minifikuje (rcssmin, v deploy.yml). JS se záměrně neminifikuje.
- Výchozí `--header-h` v CSS (114 px / 77 px na mobilu) brání posunu obsahu (CLS 0).

## Reference
- **Dočasně skryté reference: `src/data/reference-skryte.json`** – build je vyřadí všude (homepage, projekty, landing pages, lokality, obory, llms). Teď skryté: **LTC World Congress (ltc-congress-com)** – zatím nemá být veřejné; až Vladimír řekne, smazat řádek a deploy. (Z interní stránky /brand/ bylo LTC odstraněno ručně – při vrácení případně doplnit.)
- Snímky referencí: Action „Snímky referencí“ (`tools/snimky.py`); zmenšené varianty se pak vytvoří samy při deployi. Reference: HP `src/data/reference-vyber.json`; LP `reference-lp.json` + `refs` v `typy-webu.py`; případové studie `src/data/pripadovky.py`.

## SEO stránky (src/seo.py + src/seo_extra.py + src/seo_more.py, data src/data/seo-*.py a pripadovky.py)
- Lokality: `/tvorba-webu-praha/`, `-ricany/`, `-praha-vychod/`, `-praha-zapad/`, `-stredocesky-kraj/` + rozcestník `/kde-pusobime/` (odkaz v patičce). Každá musí mít vlastní obsah, ne jen vyměněné město (doorway pages).
- Srovnání: `/srovnani/wordpress-vs-wix/`, `/srovnani/woocommerce-vs-shoptet/`, `/srovnani/web-na-miru-vs-sablona/`, `/srovnani/ai-web-vs-wordpress/`, `/srovnani/shopify-vs-woocommerce/`, `/srovnani/agentura-vs-freelancer/`, `/kolik-stoji-web/` (+ cenové stránky v seo_more.py). Ceny třetích stran ověřeny 11/2026, aktualizovat jednou ročně.
  - **Pravidlo: v každém srovnání musí nejlépe vycházet náš web.** Tabulka má třetí zvýrazněný sloupec „Web od nás“ (4. prvek v `rows`, štítek „Doporučujeme“), karta „Kdy zvolit nás“ (`us_when`) s CTA a „Krátká odpověď“ končí doporučením nás. Údaje o konkurenci držet fakticky správné.
- Obory (`seo-obory.py`): `/web-pro-advokaty/`, `-terapeuty/`, `-lektory/`, `-kadernictvi/`, `-fotografy/`, `-interierove-designery/`, `-chaty-a-apartmany/` + rozcestník `/web-pro/`. Reference jen ty, které do oboru opravdu patří (popis ověřit v reference-weby.json).
- Řešení (`seo-reseni.py`): `/reseni/prevod-webu-z-wixu/`, `redesign-webu`, `pomaly-wordpress`, `napojeni-zasilkovny-a-plateb`, `napadeny-web`, `prevzeti-webu`, `prechod-ze-shoptetu-na-woocommerce`, `prevod-webu-z-webnode`, `web-nechodi-poptavky` + rozcestník `/reseni/`.
- `src/seo_more.py`: kontrola webu zdarma, cenové stránky, GEO, spolupráce pro agentury, případové studie (viz Obsahový plán).
- Kalkulačka `/kalkulacka-ceny-webu/` (`seo-kalkulacka.py` – ceny příplatků jsou ORIENTAČNÍ, Vladimír je má zkontrolovat; JS v main.js `[data-calc]`, výběr se propíše do formuláře → poptavka.php; na mobilu plovoucí lišta s cenou).
- Slovníček: každý pojem `/slovnicek/<slug>/` (29 stránek), krátká definice z `nejcastejsi-pojmy-ohledne-tvorby-webu.html` (dt odkazuje na detail), rozšíření v `seo-pojmy.py`.
- Žádné osiřelé stránky: každá nová SEO stránka musí mít odkaz ze souvisejících u jiných SEO stránek (ne z patičky ani rozcestníků – viz pravidlo nahoře) a být v sitemapě.

## Repo a technika
- Repo `webovybalicek-creator/Webovybalicek.cz` (veřejné kvůli zdarma Actions – žádná tajemství do gitu). V Claude session přidat přes add_repo s přístupem push; GitHub API jen přes REST (`gh api`), GraphQL ani secrets/variables přes proxy nejdou. Ostrý web z workspace curlem nejde (proxy) – ověřovat v prohlížeči. Rychlost lokálně: `lighthouse` (npm) nad `python3 -m http.server -d dist`; screenshoty lokálně přes Playwright s `/usr/bin/google-chrome`.
- Statický generátor `build.py`: `src/layout.html` + `src/pages/*.html` + `src/plugins.py` + `src/typy.py` + `src/seo.py` (+ `seo_extra.py`, `seo_more.py`) → `dist/` (165 stránek). `static/` kopíruje jen soubory (ne složky) do kořene webu. Lokálně `STAGING=0 python3 build.py` = produkční build (jinak noindex).
  - Hlavička stránky v HTML komentáři: `title:`, `description:`, `cta: no`, `hidden: yes` (skryté = bez indexace a mimo sitemapu), `image:` (vlastní og:image).
  - Každý deploy zvyš `VERSION` v build.py (cache busting CSS/JS). Aktuálně `310`.
- Formuláře: `form.form` → `static/poptavka.php` (typy v `$types`, nově `kontrola`, volitelné pole `site`), e-mail na webovybalicek@gmail.com + Slack webhook.
- Patička: sloupec „webovybalicek“ má odkaz „Napsat referenci ↗“ na Google recenzi (https://g.page/r/CQhSVNjhs3vbEBM/review). Pozor: v layout.html je odkaz „Reference“ i v menu – patička je až ten poslední.
- GEO/AEO: na HP schema ProfessionalService + WebSite; FAQPage automaticky z `<details><summary>`; srovnání, ceny a případové studie = Article, pojmy = DefinedTerm, lokality/obory/řešení/GEO/agentury/kontrola = Service, kalkulačka = WebApplication; `llms.txt`; robots.txt výslovně povoluje AI crawlery, blokuje /design/.
- Analytika: viz Měření poptávek.
- Styly `assets/css/style.css`, JS `assets/js/main.js`, přesměrování `static/.htaccess` (www a http → https://webovybalicek.cz, staré WP adresy).
- Deploy: push na `main` → Action `deploy.yml` (Pillow + varianty obrázků, build, brand, build, IndexNow příprava, FTP, IndexNow odeslání) nahraje `dist/` přes FTP rovnou na ostrý web (žádný staging – změny ověřovat lokálně nad dist/ před pushem). FTP účet webovybalicek@webovybalicek.cz zavřený v `public_html`. Secrety `SLEVA_KOD`, `SLACK_WEBHOOK`, FTP_*.
- Hosting Exon (cPanel cpanel.next04.exon.io, DNS na Exonu – v zóně TXT google-site-verification a CNAME 6ef3578246cc7aaac6697010d3c2f6f9 → verify.bing.com, nemazat).
- Search Console (fischer.vlada@gmail.com), Bing Webmaster Tools (přihlášení přes Google fischer.vlada) – obě se sitemapou /sitemap.xml. Seznam Webmaster (účet webovybalicek@gmail.com, reporter.seznam.cz/wm) ověřen meta tagem `seznam-wmt` v `src/layout.html` – nemazat.
- Firemní profil Google: odkaz na recenzi https://g.page/r/CQhSVNjhs3vbEBM/review. Fotky: titulní = náhledovka, logo, 10 fotek ve stylu náhledovky (23. 11.) + náhledovka znovu jako nejnovější fotka (24. 11., aby šla v náhledu dopředu – Google pořadí volí sám). Logo nenahrávat jako běžnou fotku. Šablony zpráv a plán příspěvků: soubor recenze-a-prispevky.md (předán Vladimírovi).
- iDoklad: barva vydaných a zálohových faktur #cdfe00 (Nastavení → Prodej → Vzhled a tisk dokladů). Platí pro nové doklady; staré se nepřebarvují.
- E-mailové podpisy: `tools/podpis.html` (Gmail webovybalicek@gmail.com) a `tools/podpis-karolina.html` (Roundcube karolina@webovybalicek.cz přes cPanel → Check Email). Obrázky `assets/img/email/`.
- Podklady ke značce: `G:\Můj disk\Webovy balíček\Logo nové` (SVG/PNG, ikony, favicony, písma, brandmanuál PDF – zdroj `tools/brandmanual/index.html`).
- Commity zakončuj řádky Co-Authored-By / Claude-Session dle aktuální instrukce.

## Jak se mnou pracovat
- Každou změnu ověř screenshotem (desktop i mobil) – lokálně před pushem, pak na ostrém webu.
- „Návrhy“ = skrytá stránka `src/pages/navrhy-<tema>.html` s variantami A/B/C; po výběru zapracovat a stránku smazat.
- Žádné „AI slop“, přeplácaný design ani fade-up efekty. Šipky tenké, lehce natočené.
- Co se dá zautomatizovat, zautomatizuj (nespoléhat na „nezapomenout spustit“).
- V obsahu nevymýšlet čísla, výsledky ani citace klientů.

## Brand
- Ink #0a1217, šedé, limetka #cdfe00, perleť jako akcent. Radius karet 8 px. Logo = značka W + „webovybalicek“ (Aspekta 620).
- Koncept: limetkové kuličky, tečkový rastr, halftone (tečky od velkých k menším), kurzory se štítky. Perleťová bublina z úvodu zrušena (24. 11.).
- Fajfky: černé kolečko s bílou fajfkou (`.sv-ticks`). Odrážky v právních textech: limetkové kuličky. Krátká odpověď: `.answer`, tabulka srovnání: `.vs-table` (`.vs-table--3` + `.is-us` pro náš sloupec, karta `.pay-card--us`). Kalkulačka: `.calc*`. Fotka případové studie: `.case-photo`.
- Cookie lišta: tenký bílý glass pruh dole (Consent Mode v2).

## Obsahová rozhodnutí
- AI-first: AI web / Prezentační web / E-shop. Chatbot není v ceně. Záloha 50 %, správa od 600 Kč/měs.
- Barter, ochrana designu v obchodních podmínkách, 150+ webů. E-mail všude webovybalicek@gmail.com.
- Slevový kód Toret je tajný. Tým jen křestní jména (na webu).

## Otevřené body
- V GA4 označit klíčové události, až poprvé dorazí (viz Měření).
- Doplnit do případových studií výsledky (čísla) a citace klientů (`src/data/pripadovky.py`, pole `vysledek`, `citace`, `citace_od`); u Facer, Jamie Collection a MMNT zkontrolovat, že popis řešení sedí.
- Propojit Search Console s GA4.
- Vrátit referenci LTC, až Vladimír řekne (`src/data/reference-skryte.json`).
- Zkontrolovat orientační příplatky v kalkulačce (`src/data/seo-kalkulacka.py`).
- Nabídnuto: stejné chování teček (vtečení do kuličky místo uhýbání) i na kartách s kapkami (`svg[data-kapky]`, „Na čem si zakládáme“) – čeká na odpověď.
- Náhledovky (og) a fotky ve Firemním profilu mají ještě perleťovou hmotu – zvážit přegenerování v duchu teček.
- Firmy.cz: založit/upravit firemní profil (účet webovybalicek@gmail.com).
- Příspěvky do Firemního profilu: návrhy textů čekají na schválení.
- Firemní profil: na Mapách se zobrazuje název „Tvorba webů a eshopů“ – zkontrolovat. Pokud náhled dál ukazuje fotku „Z Wixu…“, zvážit její smazání.
- Staré logo: profilová fotka Google účtů, Slack, Asana.
- Recenze na HP načítají fotky z lh3.googleusercontent.com i před souhlasem – zvážit stažení k sobě.
- Ceny „od“ u části LP jsou odhad; obchodní podmínky nechat projít advokátem.
- Odloženo: Zákon o přístupnosti + audit přístupnosti (stránka `/reseni/pristupnost-webu/`).
- Rychlost (volitelně): přístupnost 97 – jeden kontrast barev.

## Backlog SEO + affiliate (26. 11. 2026)
- Plán obsahu s affiliate odkazy: `docs/backlog-seo-affiliate.md` (v projektu `claude/backlog-seo-affiliate.md`). Jen pro vyhledávání – mimo patičku, menu a rozcestníky; affiliate odkazy viditelně označené, `rel="sponsored nofollow"`, přes `/go/<slug>/` z `src/data/affil.json`.
