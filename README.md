# 💻 new.webovybalicek.cz

Nová verze webu webovybalicek.cz – statický web mimo WordPress, vzhled podle Clerk style reference.
Nasazení: push na `main` → GitHub Actions → `python3 build.py` → FTP (new.webovybalicek.cz).

## Struktura
```
build.py                 build: src/ → dist/ (sdílená hlavička/patička, sitemap, robots)
src/layout.html          společná kostra stránek
src/cta.html             závěrečná výzva na konci podstránek
src/pages/*.html         obsah stránek (hlavička v HTML komentáři: title, description, nav, cta)
src/data/reference.json  reference (převzato z WP API starého webu)
src/data/klienti.json    loga klientů v pásu na úvodu (SVG v assets/img/klienti/)
tools/blacken-loga.py    převod nových log do černé: python3 tools/blacken-loga.py <originály> assets/img/klienti
assets/                  CSS, JS
docs/                    archiv původního obsahu (nenasazuje se)
```

## Lokální build
```
python3 build.py            # staging: noindex + robots Disallow
STAGING=0 python3 build.py  # ostrá doména
```
Po změně CSS/JS zvyšte `VERSION` v build.py (cache busting).

## Zbývá doplnit
- Místa označená `[doplnit]` (čárkovaný rámeček): cena AI webu, editace AI webu, rok založení, bio Honzy
- Formuláře zatím nikam neodesílají – napojit
- Obchodní podmínky, GDPR, cookies – zatím odkaz na stávající web, převést 1:1
- Při přepnutí na ostrou doménu: `STAGING=0` ve workflow
