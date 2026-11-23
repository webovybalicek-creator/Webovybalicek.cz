#!/usr/bin/env python3
"""Menší varianty obrázků pro srcset (rychlejší web): reference 480 px, fotky projektů 960 px.
Spouštět po každé změně snímků referencí nebo fotek projektů:  python3 tools/varianty.py
build.py použije variantu jen tehdy, když existuje (jinak zůstane původní obrázek)."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
JOBS = [(ROOT / "assets/img/reference", 480, 74), (ROOT / "assets/img/projekty", 960, 76)]

for folder, width, q in JOBS:
    out = folder / str(width)
    out.mkdir(exist_ok=True)
    n = 0
    for f in sorted(folder.glob("*.webp")):
        dst = out / f.name
        if dst.exists() and dst.stat().st_mtime >= f.stat().st_mtime:
            continue
        im = Image.open(f)
        if im.width <= width:
            continue
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(dst, "WEBP", quality=q, method=6)
        n += 1
    print(f"{folder.relative_to(ROOT)}: {n} nových variant {width}px")
