# Backlog: SEO obsah s affiliate odkazy (stav 26. 11. 2026, doplněny stávající registrace)

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

## ✅ Už registrované (odkazy na webu, stránka /doporucene-pluginy/, `src/plugins.py`)
| Služba | Odkaz | Kde se používá |
|---|---|---|
| Toret (pluginy pro WooCommerce) | `https://toret.cz/produkt/<slug>/ref/67/` (`REF = "67"`) | všech 44 stránek pluginů + balíček |
| Comgate | `https://www.comgate.cz/?r=8NQF` | detail pluginu Comgate (`EXTRA`) |
| ThePay | `https://admin.thepay.cz/partner/save-token/DTGVodzETRTyscU2d2uX` | detail pluginu ThePay (`EXTRA`) |
| iDoklad | registrace s `Ref=7YpAEvJx…` | detail pluginu iDoklad (`EXTRA`) |
| Flycart (slevy a akce pro WooCommerce) | `https://www.flycart.org/?ref=ymvkyzm` | rozcestník pluginů, „Další pluginy“ |
| LearnDash (StellarWP přes síť Impact, účet 5070967) | `https://stellarwp.pxf.io/c/5070967/…` | rozcestník pluginů, „Další pluginy“ |
| Wedos (registrováno 27. 11. 2026, partner.wedos.as) | `https://www.wedos.cz/?ap=S5P38w` (affiliate ID `S5P38w`; další odkazy v sekci Textové kampaně) | zatím nikde – hosting cluster |
| Hostinger (žádost odeslána 27. 11. 2026, čeká na schválení) | – | – |
| Crocoblock (aktivní, account.crocoblock.com/affiliate-area) | `https://crocoblock.com/?ref=1176` (affiliate ID `1176`, generátor odkazů v panelu) | zatím nikde – WordPress cluster |
| Elementor (žádost odeslána 27. 11. 2026, čeká na schválení; účet webovybalicek@gmail.com) | – | – |

Odkazy už mají `rel="sponsored noopener"` a stránky pluginů poznámku o partnerských odkazech. Při stavbě `src/data/affil.json` je převést tam (jeden zdroj pravdy) a `plugins.py` číst odtud.
Pozn.: účet v síti Impact (LearnDash) – v Impactu mohou být i další značky (např. Ecomail uvádějí agregátory), stojí za to projít katalog inzerentů.

## Affiliate programy – co je ověřené
| Služba | Program | Provize | Stav |
|---|---|---|---|
| Hostinger | affiliate + partnerský program pro agentury | od 40 %, roste s objemem; agentury opakované provize z obnov (hostinger.com/cz/affiliates, /cz/partner-program) | ověřeno |
| Wedos | affiliate | 50 % z NoLimit webhostingu, 25 % VPS/Cloud (blog.wedos.com) | ověřeno, aktuálnost sazeb zkontrolovat při registraci |
| Active24 | affiliate (jen CZ účty) | webhosting 10 %, domény 5 %, website builder 15 % (faq.active24.eu – článek z 2019) | ověřit aktuálnost |
| Elementor | affiliate | Elementor One 55 %, Pro a Elementor Host 45 % z první platby, cookie 45 dní (elementor.com/affiliates) | ověřeno |
| Crocoblock | affiliate | 50 % z každého prodeje (crocoblock.com/affiliates) | ověřeno |
| Shopify | affiliate | až 3 500 Kč za doporučení placeného plánu (shopify.com/cz blog) | ověřeno |
| Comgate | partnerský program | podmínky nezveřejněné | **registrováno** (viz výše) |
| GetResponse | affiliate | 40–60 % po dobu 12 měsíců (getresponse.com blog) | ověřeno |
| MailerLite | affiliate | existuje (mailerlite.com/affiliate), výplata od 100 USD | zjistit sazbu |
| Ecomail | affiliate přes Impact | uváděno 20 % (agregátor linkclicky.com) | ověřit přímo |
| Jotform | affiliate | 30 % (jotform.com/partnership/affiliate) | ověřeno |
| Forpsi, Websupport, Webglobe, Exon, GoPay, Fakturoid, Vyfakturuj, SmartEmailing, Shoptet, Google Workspace, Smoobu, Reservio, Bricks | – | – | **neověřeno** – zjistit, zda program mají (Webglobe má reseller program, ne affiliate) |

Registrace dělá Vladimír (osobní a platební údaje), odkazy pak doplním do `affil.json`.

## Clustery a stránky

### 1. 🖥️ Hosting (priorita 1 – nejvíc hledané, nejvíc programů)
Odlišení od konkurence: měření na klientských webech, které na hostinzích běží (TTFB, PageSpeed), a zkušenost se správou 150+ webů – cena obnovy, zálohy, podpora, jak se odchází.
- `/hosting/` – rozcestník clusteru (srovnávací tabulka, metodika, výsledky měření)
- `/hosting/pro-wordpress/` – nejlepší hosting pro WordPress
- `/hosting/pro-e-shop/` – hosting pro WooCommerce e-shop
- `/hosting/levny-hosting/` – levný hosting (s varováním na cenu obnovy)
- `/hosting/wedos/`, `/hosting/hostinger/`, `/hosting/active24/`, `/hosting/forpsi/`, `/hosting/websupport/`, `/hosting/exon/` – recenze s naměřenými daty
- `/hosting/wedos-vs-forpsi/`, `/hosting/hostinger-vs-wedos/` – nejhledanější dvojice
- `/hosting/kolik-stoji-hosting/`
- `/hosting/jak-prestehovat-web/` – návod + CTA „přestěhujeme za vás“ (poptávka)
- Hodnocení z klientských webů na daném hostingu + oficiální ceníky (testovací tarify nekupujeme).

### 2. 🧩 WordPress nástroje (priorita 2 – naše nejsilnější odbornost, vysoké provize)
- `/wordpress/elementor-pro-recenze/` – Elementor Pro vs Elementor One, co se vyplatí
- `/wordpress/crocoblock-recenze/` – Crocoblock a JetEngine v praxi (dynamický obsah, filtry, formuláře)
- `/wordpress/elementor-vs-gutenberg/`, `/wordpress/elementor-vs-bricks/`
- `/wordpress/jetformbuilder-vs-elementor-forms/`
- `/wordpress/nejlepsi-pluginy-pro-woocommerce/` – navázat na stávající `/doporucene-pluginy/` (jen odkazy ze SEO stránek)
- `/hosting/elementor-host/` – Elementor Host jako hosting (45 %)

### 3. 💳 Platby a e-shop platformy (priorita 3 – vede na poptávku e-shopu)
- `/e-shop/platebni-brany-srovnani/` – Comgate, GoPay, ThePay, Stripe, GP webpay: poplatky, napojení na WooCommerce, výplaty
- `/e-shop/comgate-recenze/`, `/e-shop/thepay-recenze/`, `/e-shop/gopay-recenze/` (Comgate a ThePay registrované; plugin pro bránu vždy přes Toret odkaz)
- `/e-shop/slevy-a-akce-ve-woocommerce/` – Flycart vs Toret (Flycart registrován)
- `/e-shop/shopify-vs-shoptet/`, `/e-shop/shopify-recenze/` (Shopify affiliate) – s jasným doporučením, kdy radši WooCommerce
- `/e-shop/jak-zalozit-e-shop/` – návod + CTA na tvorbu e-shopu

### 3b. 🎓 E-learning (registrováno: LearnDash)
- `/wordpress/learndash-recenze/` – LearnDash v praxi (kurzy, testy, prodej přes WooCommerce)
- `/wordpress/learndash-vs-moodle/` – řešíme reálně u KZPS
- `/wordpress/jak-prodavat-online-kurzy/` – návod + CTA na `/tvorba-webu/online-kurzy/` (jen ze SEO stránek)

### 4. 🧾 Fakturace a účetnictví (priorita 4; registrováno: iDoklad)
- `/software/fakturoid-vs-idoklad/` (+ Vyfakturuj) – oba používáme, napojení na WooCommerce; iDoklad s partnerským odkazem, Fakturoid ověřit
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
| 1 | Technický základ (affil.json se stávajícími odkazy, /go/, affiliate_click, šablony) | převést odkazy z plugins.py |
| 2 | **Hned monetizovatelné (už registrované):** platební brány (Comgate, ThePay + Toret pluginy), iDoklad vs Fakturoid, LearnDash (recenze, vs Moodle, prodej kurzů), slevy ve WooCommerce (Flycart) | žádná nová registrace |
| 3 | Registrace Hostinger, Wedos, Elementor, Crocoblock (Vladimír) → hosting: rozcestník, pro WordPress, pro e-shop, recenze, Wedos vs Forpsi, jak přestěhovat web | data z klientských webů |
| 4 | Elementor Pro, Crocoblock, Elementor vs Gutenberg/Bricks | |
| 5 | Shopify vs Shoptet + jak založit e-shop, e-mail marketing, firemní e-mail | |
| 6 | Domény, ostatní nástroje, zbytek recenzí hostingů | |
| průběžně | Po 4–6 týdnech Search Console: dotazy s vysokými zobrazeními → nové stránky; čtvrtletně aktualizovat ceny a sazby | |

## Kde se registrovat (Vladimír, 27. 11. 2026)
| Pořadí | Služba | Registrace | Provize | Poznámka |
|---|---|---|---|---|
| 1 | Hostinger – affiliate | https://www.hostinger.com/cz/affiliates | od 40 % | schválení až 5 pracovních dní; zahrnuje i Hostinger Horizons |
| 2 | Hostinger – partnerský program pro agentury | hPanel → Centrum agentur → Partnerský program (https://www.hostinger.com/cz/partner-program) | opakované provize z obnov klientů | jen pokud budeš klientům zakládat hosting u Hostingeru |
| 3 | Wedos | https://wedos.as | 50 % webhosting, 5 % domény | provizní systém WEDOS.as |
| 4 | Elementor | https://elementor.com/affiliates/ | Elementor One 55 %, Pro a Host 45 % | |
| 5 | Crocoblock | https://crocoblock.com/affiliates/ | 50 % | |
| 6 | Shopify | https://www.shopify.com/affiliates (běží přes Impact – máš tam účet) | až 3 500 Kč za plán | schválení obvykle do 5 pracovních dní |
| 7 | MailerLite | https://www.mailerlite.com/affiliate | 30 % doživotně | |
| 8 | GetResponse | https://www.getresponse.com/affiliate-programs (přes PartnerStack) | 40 % 12 měsíců (od 50 prodejů víc) | |
| 9 | Jotform | https://www.jotform.com/partnership/affiliate | 30 % po dobu 1 roku | schválení do 1 pracovního dne |
| 10 | Active24 | v zákaznickém centru Active24 (info: https://faq.active24.eu/knowledge-base/affiliate-program-innovation-06-2019/) | hosting 10 %, domény 5 % (údaj z 2019) | jen CZ účty |
| 11 | Ecomail a další | katalog inzerentů v Impactu | – | ověřit, zda tam jsou |
Po registraci mi pošli odkazy (nebo ID partnera), doplním je do `src/data/affil.json`.

## Rozhodnutí (27. 11. 2026)
- Testovací tarify hostingů **nekupujeme** – srovnání stojí na datech z klientských webů, které na hostinzích už běží (rychlost měřit na nich), a na oficiálních cenících. Na stránkách to tak popsat („jak jsme hodnotili“), žádná vymyšlená čísla.
- URL struktura `/hosting/`, `/wordpress/`, `/e-shop/`, `/software/`, `/domeny/` schválena.
- Hostinger Horizons propagovat můžeme (srovnání „kdy stačí AI builder a kdy web na míru“).
- Fáze 2 (platební brány, iDoklad, LearnDash, Flycart) využije už registrované partnerské odkazy – Comgate, ThePay, iDoklad, Flycart, LearnDash a Toret.
