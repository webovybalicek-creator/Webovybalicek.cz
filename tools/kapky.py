#!/usr/bin/env python3
"""Kresby „kapek“ (metaballs) ve stylu perleťové hmoty z úvodu – statické SVG.
Použití: python3 tools/kapky.py  → vypíše SVG varianty (plná, vrstevnice, raster) do tools/kapky/.
Hmota je přilepená v rohu (přesahuje přes okraj), pár kapek se od ní odtrhává."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

W, H = 400, 300
# kuličky (x, y, r) – hmota v pravém horním rohu + odtržené kapky
BALLS = [(420, -20, 110), (330, 30, 52), (385, 120, 55), (262, 18, 30), (300, 112, 22), (215, 92, 15), (352, 222, 17), (160, 40, 9), (255, 190, 8)]


def field(xs, ys):
    X, Y = np.meshgrid(xs, ys)
    f = np.zeros_like(X, dtype=float)
    for bx, by, r in BALLS:
        f += r * r / ((X - bx) ** 2 + (Y - by) ** 2 + 1e-6)
    return f


def paths(levels):
    xs, ys = np.linspace(-300, W + 500, 1000), np.linspace(-500, H + 300, 1000)
    f = field(xs, ys)
    cs = plt.contour(xs, ys, f, levels=levels)
    out = []
    for segs in cs.allsegs:
        ds = []
        for s in segs:
            s = s[::3]
            # jen tvary, které zasahují do výřezu
            if len(s) < 3 or s[:, 0].max() < -10 or s[:, 1].min() > H + 10 or s[:, 0].min() > W + 10 or s[:, 1].max() < -10:
                continue
            s = np.clip(s, [-40, -40], [W + 40, H + 40])
            ds.append("M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in s) + "Z")
        out.append("".join(ds))
    plt.close("all")
    return out


def plna(c):
    d = paths([1.0])[0]
    return f'<svg class="kapky" viewBox="0 0 {W} {H}" aria-hidden="true"><path d="{d}" fill="{c}"/></svg>'


def vrstevnice(c):
    ds = paths([0.3, 0.45, 0.65, 1.0, 1.6, 2.6])
    p = "".join(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.2" opacity="{0.35 + i * 0.13:.2f}"/>' for i, d in enumerate(ds))
    return f'<svg class="kapky" viewBox="0 0 {W} {H}" aria-hidden="true">{p}</svg>'


def raster(c):
    step = 11
    xs, ys = np.arange(step / 2, W, step), np.arange(step / 2, H, step)
    f = field(xs, ys)
    dots = []
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            v = f[j, i]
            if v > 0.6:
                r = min(4.4, 0.9 + (v - 0.6) * 2.6)
                dots.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}"/>')
    return f'<svg class="kapky" viewBox="0 0 {W} {H}" aria-hidden="true"><g fill="{c}">{"".join(dots)}</g></svg>'


if __name__ == "__main__":
    out = Path(__file__).parent / "kapky"
    out.mkdir(exist_ok=True)
    for name, fn in (("a", plna), ("b", vrstevnice), ("c", raster)):
        (out / f"{name}-ink.svg").write_text(fn("currentColor"))
    print("ok")
