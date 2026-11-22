"""Stáhne úvodní obrázek (og:image) každého pluginu z jeho stránky na toret.cz.
Ukládá assets/img/pluginy/<u>.webp (max 960 px na šířku). Spouští se ručně přes GitHub Actions."""
import io, json, re, sys, time, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/pluginy"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}

def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read()
        except Exception as ex:
            print("  znovu", url, ex); time.sleep(3 * (i + 1))
    return None

def main():
    data = json.loads((ROOT / "src/data/pluginy.json").read_text(encoding="utf-8"))
    only = set(sys.argv[1:])
    OUT.mkdir(parents=True, exist_ok=True)
    for p in data["plugins"]:
        if only and p["u"] not in only:
            continue
        page = get(f"https://toret.cz/produkt/{p['s']}/")
        if not page:
            print("X stránka", p["u"]); continue
        h = page.decode("utf-8", "ignore")
        m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', h) or \
            re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image', h)
        if not m:
            print("X bez og:image", p["u"]); continue
        img = get(m.group(1).replace("&amp;", "&"))
        if not img:
            print("X obrázek", p["u"]); continue
        im = Image.open(io.BytesIO(img)).convert("RGBA")
        bg = Image.new("RGBA", im.size, (240, 240, 240, 255))  # průhledné rohy na šedou jako karty
        im = Image.alpha_composite(bg, im).convert("RGB")
        im.thumbnail((960, 960))
        im.save(OUT / f"{p['u']}.webp", quality=80, method=6)
        print("OK", p["u"], im.size, m.group(1))
        time.sleep(1)

main()
