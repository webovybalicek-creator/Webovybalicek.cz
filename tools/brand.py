"""Generuje src/pages/brand.html – knihovnu komponent ze živých stránek v dist/.
Spuštění: python3 build.py && python3 tools/brand.py && python3 build.py"""
import html, copy
from bs4 import BeautifulSoup
D = 'dist'
_cache = {}
def soup(page):
    if page not in _cache:
        p = f'{D}/index.html' if page == '' else f'{D}/{page}/index.html'
        _cache[page] = BeautifulSoup(open(p, encoding='utf-8').read(), 'html.parser')
    return _cache[page]

def grab(page, sel, wrap=True):
    s = soup(page); el = s.select_one(sel)
    if el is None: raise SystemExit(f'Nenalezeno: {page} {sel}')
    el = copy.copy(el)
    if el.has_attr('id'): del el['id']
    if el.name == 'section':
        el['class'] = el.get('class', []) + ['br-demo']; return str(el)
    if sel == '.plugins':
        for c in el.select(':scope > .card')[4:]: c.decompose()
    out = str(el)
    if wrap:
        sec = s.select_one(sel).find_parent('section')
        cls = ' '.join(c for c in (sec.get('class', []) if sec else ['section']))
        out = f'<section class="{cls} br-demo"><div class="wrap">{out}</div></section>'
    return out

PAGES = {'': 'Homepage', 'cenik': 'Ceník', 'o-nas': 'O nás', 'ai-weby': 'AI weby', 'srovnani': 'Srovnání',
         'sprava-webu': 'Správa webu', 'nastroje': 'Nástroje', 'doporucene-pluginy': 'Doporučené pluginy',
         'jak-probiha-tvorba-webu-a-nase-spoluprace': 'Spolupráce', 'digital-project-manager-consultant': 'Honza',
         'nejcastejsi-dotazy': 'Časté dotazy'}

ICONS = ['<path d="M11.2 2 4.8 11h4.4l-1 7 6.4-9H10.2z"/>',
         '<rect x="2.5" y="3.5" width="15" height="11" rx="1.5"/><path d="M7 17.5h6M10 14.5v3M2.5 7h15"/>',
         '<path d="M3 4h2l1.6 8.5h9L17 6.5H6"/><circle cx="8" cy="16" r="1.2"/><circle cx="14" cy="16" r="1.2"/>',
         '<path d="M10 2.5 3.5 5v5c0 4 2.8 6.6 6.5 7.5 3.7-.9 6.5-3.5 6.5-7.5V5z"/><path d="m7 10 2 2 4-4"/>']
ico = lambda p: f'<svg class="pillar-ico" viewBox="0 0 20 20" aria-hidden="true">{p}</svg>'

# ---------- Základ (ručně) ----------
colors = [('ink', 'Inkoust – text, tmavé panely'), ('paper', 'Papír – pozadí'), ('gray', 'Šedá – karty'), ('hairline', 'Linka'),
          ('stone', 'Kámen – popisky'), ('graphite', 'Grafit – text odstavců'), ('lime', 'Limetka – akce, zvýraznění'), ('material', 'Béžová – doplňková')]
Z = []
Z.append(('Z01', 'Barvy', ':root --ink …', '<div class="br-swatches">' + ''.join(
    f'<div><span style="background:var(--{k})"></span><strong>--{k}</strong><small>{d}</small></div>' for k, d in colors)
    + '<div><span class="br-pearl"></span><strong>perleť</strong><small>--pearl-rim – kapky, akcenty</small></div></div>'))
Z.append(('Z02', 'Typografie', 'h1 · h2 · h3 · .lead · .mono', '''<div class="br-type">
<p class="mono">H1 – nadpis stránky</p><h1 style="margin:0">Prezentační weby <em>a e-shopy</em></h1>
<p class="mono">H2 – nadpis sekce</p><h2 style="margin:0">Co pro vás zařídíme</h2>
<p class="mono">H3 – nadpis karty</p><h3 style="margin:0">Rychlejší dodání</h3>
<p class="mono">.lead – úvodní odstavec</p><p class="lead" style="margin:0">Umělou inteligenci používáme tam, kde šetří čas a peníze.</p>
<p class="mono">Odstavec</p><p style="margin:0;max-width:60ch">Běžný text odstavce. Nezajímá nás počet stránek, ale co web přinese: poptávky, objednávky, rezervace.</p>
<p class="mono">.mono – technické popisky</p><p class="mono" style="margin:0;color:var(--ink)">rychle a výhodně</p></div>'''))
Z.append(('Z03', 'Vodní zvýraznění', 'h1 em · .manifest em', '<div class="br-type"><h1 class="br-water" style="margin:0">Jaký web <em>je pro vás?</em></h1><p class="mono">Slovo v *hvězdičkách* nebo &lt;em&gt; v H1 se po načtení zalije limetkovou vlnou.</p></div>'))
Z.append(('Z04', 'Zaoblení', '--r-card · --r-feature · --r-pill', '<div class="br-radii">' + ''.join(
    f'<div><span style="border-radius:var(--{k})"></span><strong>--{k}</strong><small>{d}</small></div>' for k, d in
    [('r-card', '8 px – všechny karty'), ('r-feature', '24 px – velké panely'), ('r-pill', 'pilulky, tlačítka')]) + '</div>'))
P = []
P.append(('P01', 'Tlačítka', '.btn--primary · --outline · --ghost · --sm · --block', '''<div class="br-row">
<a class="btn btn--primary" href="#">Primární</a><a class="btn btn--outline" href="#">Obrysové</a><a class="btn btn--ghost" href="#">Průhledné</a><a class="btn btn--primary btn--sm" href="#">Malé</a></div>
<div class="br-row br-row--ink"><a class="btn btn--primary" href="#">Primární na černé</a><a class="btn btn--outline" href="#">Obrysové na černé</a></div>
<div style="max-width:360px;margin-top:16px"><a class="btn btn--primary btn--block" href="#">Na celou šířku</a></div>'''))
P.append(('P02', 'Štítky AI / člověk', '.tg .t-ai · .t-hum · .t-mix · .t-done', '<div class="br-row"><span class="tg t-ai">AI</span><span class="tg t-hum">člověk</span><span class="tg t-mix">AI + člověk</span><span class="tg t-done">hotovo</span></div>'))
P.append(('P03', 'Stavové štítky', '.badge--draft · --review · --input · --done', '<div class="br-row"><span class="badge badge--draft">AI</span><span class="badge badge--review">člověk</span><span class="badge badge--input">AI + člověk</span><span class="badge badge--done">hotovo</span></div>'))
P.append(('P04', 'Čipy', '.chips · .chips--dark', '<ul class="chips br-row" style="padding:0;list-style:none"><li>Kalkulačka ceny</li><li>AI chatbot</li><li>Napojení na API</li></ul><div class="br-row br-row--ink"><ul class="chips chips--dark" style="padding:0;list-style:none;margin:0"><li>Kalkulačka ceny</li><li>AI chatbot</li></ul></div>'))
P.append(('P05', 'Ikony v kolečku', '.pillar-ico', '<div class="br-row">' + ''.join(ico(i) for i in ICONS) + '</div>'))
P.append(('P06', 'Fajfky', '.sv-ticks', '<ul class="sv-ticks" style="max-width:420px"><li>Výrazně rychlejší dodání</li><li>Nižší cena díky rychlejší tvorbě</li><li>Zaškolení a správa po spuštění</li></ul>'))
P.append(('P07', 'Parametry', '.sv-spec', '<dl class="sv-spec" style="max-width:420px"><div><dt>Dodání</dt><dd>dny až týdny</dd></div><div><dt>Vlastní administrace</dt><dd>ano</dd></div></dl>'))
P.append(('P08', 'Sloupce času', '.bars', grab('ai-weby', '.bars', False)))

# ---------- Bloky (ze živých stránek) ----------
B = [
 ('B01', 'Úvod podstránky', '.page-hero', 'srovnani', '.page-hero'),
 ('B02', 'Úvod s tlačítky', '.page-hero .hero-actions', 'sprava-webu', '.page-hero'),
 ('B03', 'Hlavička sekce', '.section-head', '', '#cesty .section-head'),
 ('B04', 'Karty tří cest', '.feature-cards', '', '.feature-cards'),
 ('B05', 'Umíme také (karta se štítkem)', '.web-types', '', '.web-types'),
 ('B06', 'Černý blok 150+', '.pa-a', '', '.pa-a'),
 ('B07', 'Manifest (text se zabarvením)', '.manifest', '', '.manifest'),
 ('B08', 'Limetkový blok No slop', '.noslop', '', '.noslop'),
 ('B09', 'Bento pilíře', '.pa-bento', '', '.pa-bento'),
 ('B10', 'Projekty – harmonika s fotkou', '.projs', '', '.projs'),
 ('B11', 'Služby – harmonika', '.accordion', '', '#sluzby .accordion'),
 ('B12', 'Proces – kroky', '.steps', '', '.steps'),
 ('B13', 'Ceník – balíčky', '.pricing', '', '#cenik .pricing'),
 ('B14', 'Mřížka karet', '.grid-cards', 'sprava-webu', '.grid-cards'),
 ('B15', 'Platební karty', '.pay-card', 'cenik', '.grid-cards'),
 ('B16', 'AI bento', '.ai-a', 'ai-weby', '.ai-a'),
 ('B17', 'Srovnání – tři karty', '.sv-a', 'srovnani', '.sv-a'),
 ('B18', 'Tým', '.team', 'o-nas', '.team'),
 ('B19', 'Jak pracujeme – bento', '.ob-a', 'o-nas', '.ob-a'),
 ('B20', 'Karta osoby', '.person', 'digital-project-manager-consultant', '.person'),
 ('B21', 'Dvě karty se štítky (Co si připravit)', '.prep', 'jak-probiha-tvorba-webu-a-nase-spoluprace', '.prep'),
 ('B22', 'Boční karta', '.aside-card', 'jak-probiha-tvorba-webu-a-nase-spoluprace', '.aside-card'),
 ('B23', 'Plugin – karta s dlaždicí', '.plugins .card', 'doporucene-pluginy', '.plugins'),
 ('B24', 'Slevový formulář', '.sleva', 'doporucene-pluginy', '.sleva'),
 ('B25', 'Nástroje – oběžná dráha', '.tools', 'nastroje', '.tools'),
 ('B26', 'Pás referencí', '.refstrip', '', '.refstrip'),
 ('B27', 'Recenze Google', '#recenze', '', '#recenze'),
 ('B28', 'Kontakt – formulář', '.contact-section', '', '#kontakt'),
]
G = [('G01', 'Ucho „Máte otázku?“', '.ear', 'Plovoucí pilulka vpravo dole. Na této stránce je vidět po odscrollování.'),
     ('G02', 'Výsuvný panel Umíme', '.sheet--b · data-open="umime"', '<button type="button" class="btn btn--outline" data-open="umime">Otevřít panel</button>'),
     ('G03', 'Video popup Elementor', '#video-elementor · data-open="video-elementor"', '<button type="button" class="btn btn--outline" data-open="video-elementor">Otevřít video</button>'),
     ('G04', 'Černé CTA pole', '{{cta}} · .cta', 'Velký blok „Pojďme probrat váš web“ nad patičkou – je dole na této stránce.'),
     ('G05', 'Oznamovací pruh a hlavička', '.announce · header', 'Nahoře na každé stránce.')]

def head(code, name, cls, src=None):
    s = f' · <a href="/{src}/">{PAGES.get(src, src)}</a>' if src else (' · <a href="/">Homepage</a>' if src == '' else '')
    return f'<header class="br-h"><span class="br-code">{code}</span><h3>{name}</h3><code>{html.escape(cls)}</code><small>{s.lstrip(" · ") if s else ""}</small></header>'

out = []
toc = []
def group(gid, title, items):
    toc.append(f'<li><a href="#{gid}">{title}</a><ol>' + ''.join(f'<li><a href="#{c.lower()}"><span>{c}</span> {n}</a></li>' for c, n, *_ in items) + '</ol></li>')
    out.append(f'<section class="br-group" id="{gid}"><div class="wrap"><h2>{title}</h2></div></section>')

group('zaklad', 'Základ', Z)
for c, n, cls, body in Z:
    out.append(f'<div class="br-item" id="{c.lower()}"><div class="wrap">{head(c, n, cls)}<div class="br-pad">{body}</div></div></div>')
group('prvky', 'Prvky', P)
for c, n, cls, body in P:
    out.append(f'<div class="br-item" id="{c.lower()}"><div class="wrap">{head(c, n, cls)}<div class="br-pad">{body}</div></div></div>')
group('bloky', 'Bloky', B)
for c, n, cls, page, sel in B:
    src = page
    h = head(c, n, cls).replace('<small></small>', f'<small><a href="/{page + "/" if page else ""}">{PAGES[page]}</a></small>')
    out.append(f'<div class="br-item" id="{c.lower()}"><div class="wrap">{h}</div>{grab(page, sel)}</div>')
group('globalni', 'Globální prvky', G)
for c, n, cls, body in G:
    out.append(f'<div class="br-item" id="{c.lower()}"><div class="wrap">{head(c, n, cls)}<div class="br-pad"><p>{body}</p></div></div></div>')

CSS = '''<style>
.br-toc { columns: 4 220px; gap: 32px; margin: 0; padding: 0; list-style: none; font-size: 14px; }
.br-toc > li { break-inside: avoid; margin-bottom: 22px; } .br-toc > li > a { font-weight: 600; font-size: 15px; }
.br-toc ol { margin: 8px 0 0; padding: 0; list-style: none; display: grid; gap: 4px; } .br-toc ol a { color: var(--graphite); text-decoration: none; } .br-toc ol a:hover { color: var(--ink); }
.br-toc span, .br-code { font: 500 11px/1 var(--f-mono); padding: 3px 6px; border-radius: 4px; background: var(--lime); color: var(--ink); }
.br-group { padding: 96px 0 8px; } .br-group h2 { margin: 0; padding-bottom: 16px; border-bottom: 1px solid var(--ink); }
.br-item { padding: 48px 0 0; scroll-margin-top: 90px; }
.br-h { display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px 14px; padding: 0 0 18px; border-bottom: 1px dashed var(--hairline); margin-bottom: 0; }
.br-h h3 { margin: 0; font-size: 20px; } .br-h code { font: 400 12px var(--f-mono); color: var(--stone); } .br-h small { margin-left: auto; font-size: 13px; } .br-h small a { color: var(--stone); }
.br-pad { padding: 28px 0 0; }
.br-demo { outline: 1px dashed transparent; }
.br-demo.section { padding-top: 32px !important; padding-bottom: 32px; }
.br-row { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; } .br-row--ink { margin-top: 16px; padding: 22px; border-radius: var(--r-card); background: var(--ink); }
.br-swatches, .br-radii { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 16px; }
.br-swatches div, .br-radii div { display: grid; gap: 4px; font-size: 14px; } .br-swatches small, .br-radii small { color: var(--stone); font-size: 12px; }
.br-swatches span { height: 72px; border-radius: var(--r-card); box-shadow: inset 0 0 0 1px var(--hairline); margin-bottom: 6px; }
.br-pearl { background: var(--pearl-rim); }
.br-radii span { height: 72px; background: var(--gray); margin-bottom: 6px; }
.br-type { display: grid; gap: 10px; } .br-type .mono { margin: 14px 0 0; font: 400 12px var(--f-mono); color: var(--stone); }
</style>'''
page = f'''<!--
title: Brand a komponenty | webovybalicek
description: Interní přehled barev, prvků a bloků webu.
cta: yes
hidden: yes
-->
{CSS}
<section class="page-hero" data-nojump><div class="wrap"><ol class="crumbs"><li><a href="/">Domů</a></li><li>Brand</li></ol><h1>Brand a <em>komponenty</em></h1><p class="lead">Všechny barvy, prvky a bloky webu na jednom místě. Stačí říct kód, třeba „B09 na stránku Ceník“.</p></div></section>
<section class="section" style="padding-bottom:0"><div class="wrap"><ol class="br-toc">{''.join(toc)}</ol></div></section>
{''.join(out)}
<div style="height:80px"></div>
'''
open('src/pages/brand.html', 'w', encoding='utf-8').write(page)
print('brand.html:', len(Z) + len(P) + len(B) + len(G), 'položek')
