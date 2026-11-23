#!/usr/bin/env python3
"""Menší varianty obrázků pro srcset (rychlejší web): reference 480 px, fotky projektů 960 px.
Spouští se AUTOMATICKY při každém deployi (deploy.yml) – ručně není potřeba nic hlídat.
Varianta se vytvoří znovu, kdykoli se změní obsah původního obrázku (kontrola podle otisku v .zdroj.json).
build.py použije variantu jen tehdy, když existuje (jinak zůstane původní obrázek)."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
JOBS = [(ROOT / "assets/img/reference", 480, 74), (ROOT / "assets/img/projekty", 960, 76)]

for folder, width, q in JOBS:
    out = folder / str(width)
    out.mkdir(exist_ok=True)
    man_path = out / ".zdroj.json"
    man = json.loads(man_path.read_text()) if man_path.exists() else {}
    n = 0
    for f in sorted(folder.glob("*.webp")):
        h = hashlib.md5(f.read_bytes()).hexdigest()
        dst = out / f.name
        if dst.exists() and man.get(f.name) == h:
            continue
        im = Image.open(f)
        if im.width <= width:
            dst.unlink(missing_ok=True)
            man.pop(f.name, None)
            continue
        im.resize((width, round(im.height * width / im.width)), Image.LANCZOS).save(dst, "WEBP", quality=q, method=6)
        man[f.name] = h
        n += 1
    for old in out.glob("*.webp"):  # varianta bez původního obrázku pryč
        if not (folder / old.name).exists():
            old.unlink(); man.pop(old.name, None)
    man_path.write_text(json.dumps(man, indent=0, sort_keys=True))
    print(f"{folder.relative_to(ROOT)}: {n} nových/obnovených variant {width}px")
