#!/usr/bin/env python3
"""Převod klientských log do jednobarevné černé verze (SVG).
Použití: python3 -I blacken.py <složka s originály> <výstupní složka>
Bílé plochy uvnitř barevných log se stanou průhlednými výřezy (maska), ne černou plochou."""
import re, subprocess, sys, tempfile, os
import xml.etree.ElementTree as ET

SRC, OUT = sys.argv[1], sys.argv[2]
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

# zdroj -> (slug, bílé třídy/výplně, které se mají vyříznout)
LOGOS = {
    "Bohdasin-B-logo.svg": ("bohdasin", None),
    "Dorsen_logo_3.svg": ("dorsen", None),
    "dorintblack-logo.svg": ("dorint", None),
    "Logo_Frosch_3.svg": ("frosch", {"a"}),
    "inky-blue-2.svg": ("inky", {"st1"}),
    "Institutoriganum-logo-white.svg": ("institut-origanum", None),
    "IronOT-logo-black.svg": ("iron-ot", None),
    "Jamie-logo-2-black.svg": ("jamie-collection", None),
    "KZPS-logo-1.svg": ("kzps", None),
    "Logo-brown.svg": ("kabiny-kravak", None),
    "logo-carujeme.svg": ("carujeme", None),
    "mmnt-logo-2.svg": ("mmnt", None),
    "Residento-logo-cerne.svg": ("residento", None),
    "Sheio_logo_black.svg": ("sheio", None),
}
SHAPES = {"path", "polygon", "polyline", "rect", "circle", "ellipse", "line"}
tag = lambda e: e.tag.split("}")[-1]


def blacken(el, in_def=False):
    """Všechny viditelné tvary na černo; obsah clipPath/mask se nechává být."""
    t = tag(el)
    if t in ("clipPath", "mask"):
        return
    if t == "style" or t == "title":
        return
    if t in SHAPES:
        el.attrib.pop("class", None)
        st = el.attrib.get("style")
        if st:
            st = ";".join(p for p in st.split(";") if p.strip() and not p.strip().startswith("fill:"))
            if st: el.set("style", st)
            else: el.attrib.pop("style")
        el.set("fill", "#000")
    elif "fill" in el.attrib and t != "svg":
        el.set("fill", "#000")
    for c in el:
        blacken(c)


def knock_out(root, white, vb):
    """Bílé tvary (podle třídy) vyříznou vše, co bylo nakresleno před nimi – zachová pořadí vrstev."""
    x, y, w, h = vb
    defs = ET.Element(f"{{{NS}}}defs")
    done, pending, n = [], [], 0
    kids = [c for c in root if tag(c) not in ("defs", "style", "title")]
    for c in list(root):
        root.remove(c)

    def flush():
        nonlocal done, pending, n
        if pending and done:
            n += 1
            m = ET.SubElement(defs, f"{{{NS}}}mask", {"id": f"k{n}", "maskUnits": "userSpaceOnUse",
                              "x": str(x), "y": str(y), "width": str(w), "height": str(h)})
            ET.SubElement(m, f"{{{NS}}}rect", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "fill": "#fff"})
            for p in pending:
                p.attrib.pop("class", None); p.set("fill", "#000"); m.append(p)
            g = ET.Element(f"{{{NS}}}g", {"mask": f"url(#k{n})"})
            g.extend(done)
            done = [g]
        pending = []

    for c in kids:
        if c.get("class") in white:
            pending.append(c)
        else:
            flush()
            done.append(c)
    flush()
    if len(defs):
        root.append(defs)
    root.extend(done)


def render_bbox(path, vb):
    """Ořez viewBoxu na skutečnou kresbu (bez prázdných okrajů)."""
    x, y, w, h = vb
    scale = 2000 / w
    png = tempfile.mktemp(suffix=".png")
    subprocess.run(["rsvg-convert", "-w", "2000", path, "-o", png], check=True)
    out = subprocess.run(["convert", png, "-alpha", "extract", "-threshold", "2%", "-format", "%@", "info:"],
                         capture_output=True, text=True, check=True).stdout
    os.unlink(png)
    bw, bh, bx, by = map(int, re.match(r"(\d+)x(\d+)\+(\d+)\+(\d+)", out).groups())
    r = lambda v: round(v, 2)
    return (r(x + (bx - 1) / scale), r(y + (by - 1) / scale), r((bw + 2) / scale), r((bh + 2) / scale))


os.makedirs(OUT, exist_ok=True)
for src, (slug, white) in LOGOS.items():
    root = ET.parse(os.path.join(SRC, src)).getroot()
    vb = tuple(float(v) for v in re.split(r"[ ,]+", root.get("viewBox").strip()))
    for k in ("width", "height", "x", "y", "style", "id", "version", "{http://www.w3.org/XML/1998/namespace}space"):
        root.attrib.pop(k, None)
    for k in [k for k in root.attrib if "data-name" in k]:
        root.attrib.pop(k)
    # třídy s fill-rule:evenodd (díry v tvarech) přenést na atribut, než zmizí <style>
    css = " ".join(e.text or "" for e in root.iter() if tag(e) == "style")
    evenodd = set()
    for sel, body in re.findall(r"([^{}]+)\{([^}]*)\}", css):
        if "evenodd" in body:
            evenodd |= {c.strip().lstrip(".") for c in sel.split(",")}
    for e in root.iter():
        if e.get("class") in evenodd:
            e.set("fill-rule", "evenodd")
    for parent in root.iter():
        for c in list(parent):
            if tag(c) in ("title",) or (tag(c) == "style"):
                parent.remove(c)
    if white:
        knock_out(root, white, vb)
    for c in root:
        if tag(c) != "defs" or not white:
            blacken(c)
    root.attrib.pop("fill", None)
    dst = os.path.join(OUT, slug + ".svg")
    ET.ElementTree(root).write(dst, encoding="unicode")
    nvb = render_bbox(dst, vb)
    root.set("viewBox", " ".join(f"{v:g}" for v in nvb))
    txt = ET.tostring(root, encoding="unicode")
    txt = re.sub(r">\s+<", "><", txt)
    open(dst, "w", encoding="utf-8").write(txt + "\n")
    print(f"{slug}\t{nvb[2]:g}\t{nvb[3]:g}\t{nvb[2]/nvb[3]:.3f}")
