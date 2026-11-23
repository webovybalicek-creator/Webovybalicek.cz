#!/usr/bin/env python3
"""Stáhne obrázky z webu do repozitáře a převede je na WebP (běží v Action „Stáhnout obrázky“).
Argumenty: dvojice URL=>cesta, např. https://…/foto.jpg=>assets/img/jakub/architektura.webp"""
import io, os, sys, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
for pair in (" ".join(sys.argv[1:]) or os.environ.get("OBRAZKY", "")).split():
    url, out = pair.split("=>")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=60).read()
    im = Image.open(io.BytesIO(data)).convert("RGB")
    im.thumbnail((1400, 1400), Image.LANCZOS)
    p = ROOT / out
    p.parent.mkdir(parents=True, exist_ok=True)
    im.save(p, "WEBP", quality=80, method=6)
    print("OK", out, im.size)
