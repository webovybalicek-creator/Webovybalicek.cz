#!/usr/bin/env python3
"""IndexNow: po deployi ohlásí Bingu, Seznamu (a dalším) jen nové a změněné stránky.

Použití (v deploy.yml):
  python3 tools/indexnow.py priprav   # před FTP: porovná dist/ s minulým stavem na webu, zapíše dist/indexnow-stav.json
  python3 tools/indexnow.py odesli    # po FTP: pošle změněné URL na api.indexnow.org

Stav (otisky stránek) leží na webu v /indexnow-stav.json, takže není potřeba nic commitovat.
Otisk ignoruje ?v=VERZE u CSS/JS, aby samotné zvýšení verze nehlásilo celý web.
Google IndexNow nepodporuje – ten si čte sitemap.xml.
"""
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

SITE = "https://webovybalicek.cz"
KEY = "4f1c9b7e2a6d48c3b0e5a91d7c2f6e38"
DIST = Path(__file__).resolve().parent.parent / "dist"
STAV = DIST / "indexnow-stav.json"
SEZNAM = Path("/tmp/indexnow-urls.json")


def sitemap_urls():
    xml = (DIST / "sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def otisk(url):
    path = url.replace(SITE, "").strip("/")
    f = DIST / path / "index.html" if path else DIST / "index.html"
    if not f.exists():
        return None
    html = f.read_text(encoding="utf-8")
    html = re.sub(r"\?v=\d+", "", html)
    return hashlib.sha1(html.encode("utf-8")).hexdigest()[:16]


def priprav():
    try:
        with urllib.request.urlopen(SITE + "/indexnow-stav.json", timeout=20) as r:
            minule = json.load(r)
    except Exception as e:  # první běh nebo nedostupné – ohlásí se vše
        print(f"Minulý stav nenačten ({e}), ohlásím všechny stránky.")
        minule = {}
    ted = {u: h for u in sitemap_urls() if (h := otisk(u))}
    zmenene = [u for u, h in ted.items() if minule.get(u) != h]
    zmenene += [u for u in minule if u not in ted]  # smazané stránky (vrací 404/410) – vyhledávače je vyřadí
    STAV.write_text(json.dumps(ted, ensure_ascii=False, indent=0), encoding="utf-8")
    SEZNAM.write_text(json.dumps(zmenene), encoding="utf-8")
    print(f"IndexNow: {len(zmenene)} nových/změněných z {len(ted)} stránek.")
    for u in zmenene[:30]:
        print("  " + u)


def odesli():
    urls = json.loads(SEZNAM.read_text(encoding="utf-8")) if SEZNAM.exists() else []
    if not urls:
        print("IndexNow: nic nového k ohlášení.")
        return
    body = json.dumps({
        "host": "webovybalicek.cz",
        "key": KEY,
        "keyLocation": f"{SITE}/{KEY}.txt",
        "urlList": urls[:10000],
    }).encode("utf-8")
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow: odesláno {len(urls)} URL, odpověď {r.status}.")
    except Exception as e:  # neúspěch nesmí shodit deploy
        print(f"IndexNow: odeslání se nepovedlo ({e}).")


if __name__ == "__main__":
    {"priprav": priprav, "odesli": odesli}[sys.argv[1] if len(sys.argv) > 1 else "priprav"]()
