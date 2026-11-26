# Backlog: SEO obsah s affiliate odkazy (stav 26. 11. 2026)

Cíl: pokrýt tematicky všechny služby, které na webech používáme a které mají affiliate/partnerský program. Stránky přivedou návštěvnost z vyhledávání, vydělají na provizích a zároveň vedou k poptávce („nechcete to řešit sami? postavíme / napojíme / přestěhujeme za vás“).

## Pravidla pro všechny stránky v backlogu
- **Jen pro vyhledávání:** žádné odkazy z patičky, menu ani rozcestníků běžného webu. Stránky jsou v sitemapě (+ IndexNow) a prolinkované mezi sebou (vlastní rozcestník clusteru je v pořádku, ale nikam se neodkazuje z navigace). Stejné jako `seo_only` stránky.
- **Označení affiliate:** každá stránka s affiliate odkazem má viditelnou poznámku („Některé odkazy jsou partnerské, při nákupu dostaneme provizi, vás to nic nestojí.“) a odkazy `rel="sponsored nofollow"`. Elementor to v podmínkách výslovně vyžaduje (jasné a viditelné označení, jinak ukončení spolupráce), ale platí to pro všechny.
- **Pořadí podle kvality, ne provize.** Pravidlo „nejlépe vychází náš web“ tu neplatí (nejsme hosting ani platební brána). Důvěryhodnost je to, co stránku drží v Googlu.
- **Žádná vymyšlená čísla.** Ceny, poplatky a parametry z oficiálních ceníků s datem ověření; vlastní měření jen skutečně naměřená.
- Každá URL má náhledovku (`meta["og"]`), schema Article/Review/FAQPage, krátkou odpověď nahoře a CTA na poptávku.

## Technický základ (udělat jako první)
1. `src/data/affil.json` – jediné místo s affiliate odkazy: `{"hostinger": {"url": "...", "aktivni": false}}`. Dokud není registrace, odkaz vede na běžnou adresu služby bez provize.
2. Odkazy přes `/go/<slug>/` (přesměrování 302 generované z affil.json do `.htaccess`) – jednotná správa a změna odkazu na jednom místě.
3. GA4 událost `affiliate_click` (slug služby, stránka) přes `wbTrack`.
4. Nový modul `src/seo_affil.py` + data `src/data/affil-*.py`, komponenty: srovnávací tabulka, karta služby (klady/zápory/cena/odkaz), blok „Jak jsme testovali“, affiliate poznámka.

## Affiliate programy – co je ověřené
| Služba | Program | Provize | Stav |
|---|---|---|---|
| Hostinger | affiliate + partnerský program pro agentury | od 40 %, roste s objemem; agentury opakované provize z obnov (hostinger.com/cz/affiliates, /cz/partner-program) | ověřeno |
| Wedos | affiliate | 50 % z NoLimit webhostingu, 25 % VPS/Cloud (blog.wedos.com) | ověřeno, aktuálnost sazeb zkontrolovat při registraci |
| Active24 | affiliate (jen CZ účty) | webhosting 10 %, domény 5 %, website builder 15 % (faq.active24.eu – článek z 2019) | ověřit aktuálnost |
| Elementor | affiliate | Elementor One 55 %, Pro a Elementor Host 45 % z první platby, cookie 45 dní (elementor.com/affiliates) | ověřeno |
| Crocoblock | affiliate | 50 % z každého prodeje (crocoblock.com/affiliates) | ověřeno |
| Shopify | affiliate | až 3 500 Kč za doporučení placeného plánu (shopify.com/cz blog) | ověřeno |
| Comgate | partnerský program | existuje (comgate.eu/partners), podmínky neuvedené | zjistit podmínky |
| GetResponse | affiliate | 40–60 % po dobu 12 měsíců (getresponse.com blog) | ověřeno |
| MailerLite | affiliate | existuje (mailerlite.com/affiliate), výplata od 100 USD | zjistit sazbu |
| Ecomail | affiliate přes Impact | uváděno 20 % (agregátor linkclicky.com) | ověřit přímo |
| Jotform | affiliate | 30 % (jotform.com/partnership/affiliate) | ověřeno |
| Forpsi, Websupport, Webglobe, Exon, GoPay, ThePay, Fakturoid, iDoklad, Vyfakturuj, SmartEmailing, Shoptet, Google Workspace, Smoobu, Reservio, Bricks, Toret | – | – | **neověřeno** – zjistit, zda program mají (Webglobe má reseller program, ne affiliate; Toret: máme dohodu, zjistit affiliate) |

Registrace dělá Vladimír (osobní a platební údaje), odkazy pak doplním do `affil.json`.

## Clustery a stránky

### 1. 🖥️ Hosting (priorita 1 – nejvíc hledané, nejvíc programů)
Odlišení od konkurence: vlastní měření (stejný WordPress + Elementor na každém hostingu: TTFB, PageSpeed, dostupnost za 30 dní) a zkušenost se správou 150+ webů – cena obnovy, zálohy, podpora, jak se odchází.
- `/hosting/` – rozcestník clusteru (srovnávací tabulka, metodika, výsledky měření)
- `/hosting/pro-wordpress/` – nejlepší hosting pro WordPress
- `/hosting/pro-e-shop/` – hosting pro WooCommerce e-shop
- `/hosting/levny-hosting/` – levný hosting (s varováním na cenu obnovy)
- `/hosting/wedos/`, `/hosting/hostinger/`, `/hosting/active24/`, `/hosting/forpsi/`, `/hosting/websupport/`, `/hosting/exon/` – recenze s naměřenými daty
- `/hosting/wedos-vs-forpsi/`, `/hosting/hostinger-vs-wedos/` – nejhledanější dvojice
- `/hosting/kolik-stoji-hosting/`
- `/hosting/jak-prestehovat-web/` – návod + CTA „přestěhujeme za vás“ (poptávka)
- **Rozhodnutí pro Vladimíra:** koupit na 1 měsíc nejlevnější WordPress tarif u 5–6 hostingů kvůli měření (náklad zhruba stovky Kč/hosting), nebo vycházet jen z klientských webů, které už na nich běží.

### 2. 🧩 WordPress nástroje (priorita 2 – naše nejsilnější odbornost, vysoké provize)
- `/wordpress/elementor-pro-recenze/` – Elementor Pro vs Elementor One, co se vyplatí
- `/wordpress/crocoblock-recenze/` – Crocoblock a JetEngine v praxi (dynamický obsah, filtry, formuláře)
- `/wordpress/elementor-vs-gutenberg/`, `/wordpress/elementor-vs-bricks/`
- `/wordpress/jetformbuilder-vs-elementor-forms/`
- `/wordpress/nejlepsi-pluginy-pro-woocommerce/` – navázat na stávající `/doporucene-pluginy/` (jen odkazy ze SEO stránek)
- `/hosting/elementor-host/` – Elementor Host jako hosting (45 %)

### 3. 💳 Platby a e-shop platformy (priorita 3 – vede na poptávku e-shopu)
- `/e-shop/platebni-brany-srovnani/` – Comgate, GoPay, ThePay, Stripe, GP webpay: poplatky, napojení na WooCommerce, výplaty
- `/e-shop/comgate-recenze/`, `/e-shop/gopay-recenze/`
- `/e-shop/shopify-vs-shoptet/`, `/e-shop/shopify-recenze/` (Shopify affiliate) – s jasným doporučením, kdy radši WooCommerce
- `/e-shop/jak-zalozit-e-shop/` – návod + CTA na tvorbu e-shopu

### 4. 🧾 Fakturace a účetnictví (priorita 4)
- `/software/fakturoid-vs-idoklad/` (+ Vyfakturuj) – oba používáme, napojení na WooCommerce
- `/software/fakturace-pro-e-shop/`

### 5. 📬 E-mail marketing a firemní e-mail (priorita 5)
- `/software/ecomail-vs-smartemailing/`, `/software/mailerlite-recenze/`, `/software/nejlepsi-nastroj-na-newslettery/`
- `/software/firemni-email/` – Google Workspace vs Microsoft 365 vs e-mail od hostingu (řešíme u klientů neustále)

### 6. 🌐 Domény (priorita 6)
- `/domeny/jak-vybrat-domenu/`, `/domeny/kde-koupit-domenu/`, `/domeny/prevod-domeny/`, `/domeny/cz-vs-com/`
- Affiliate: Active24 (5 %), ostatní ověřit; Hostinger referral se na domény nevztahuje.

### 7. 🛎️ Ostatní nástroje (podle ověření programů)
- Rezervační systémy (Smoobu, Reservio – zkušenost z Kabin Kravák), formuláře (Jotform 30 % vs JetFormBuilder), AI tvorba webu (Hostinger Horizons – opatrně, je to konkurence AI webů; srovnání pojmout jako „kdy stačí builder a kdy web na míru“).

## Pořadí práce
| Fáze | Co | Poznámka |
|---|---|---|
| 1 | Technický základ (affil.json, /go/, affiliate_click, šablony) + registrace: Hostinger, Wedos, Elementor, Crocoblock | registrace Vladimír |
| 2 | Hosting: rozcestník, pro WordPress, pro e-shop, 4 recenze, Wedos vs Forpsi, jak přestěhovat web | měření běží 30 dní, stránky jdou ven hned s cenami a doplní se čísly |
| 3 | Elementor Pro, Crocoblock, Elementor vs Gutenberg/Bricks | |
| 4 | Platební brány + Shopify vs Shoptet + jak založit e-shop | dořešit Comgate/GoPay programy |
| 5 | Fakturace, e-mail marketing, firemní e-mail | |
| 6 | Domény, ostatní nástroje, zbytek recenzí hostingů | |
| průběžně | Po 4–6 týdnech Search Console: dotazy s vysokými zobrazeními → nové stránky; čtvrtletně aktualizovat ceny a sazby | |

## Otevřené otázky pro Vladimíra
- Měření hostingů: koupit testovací tarify, nebo jen data z klientských webů?
- URL struktura: navržené složky `/hosting/`, `/wordpress/`, `/e-shop/`, `/software/`, `/domeny/` – OK?
- U Hostinger Horizons (AI builder, 60 %) – chceš ho vůbec propagovat, když je to konkurence AI webů?
