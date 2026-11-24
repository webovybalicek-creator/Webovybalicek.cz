"""Brandmanuál → PDF.  python3 tools/brandmanual/build.py <složka s logy (SVG, Ikony, Emailovy-podpis)> <výstup.pdf>
Grafiku teček generuje ze stejného tvaru kapky jako úvod webu a náhledovky (tools/og.py)."""
import re, shutil, sys, tempfile, http.server, threading, functools
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import og

def kapky(fill, small=True):
    svg = og.dots_svg()
    svg = re.sub(r'<circle[^>]*fill="#(cdfe00|c8ccce)"/>', "", svg)          # bez kuliček a řetízku
    if not small:
        svg = re.sub(r'<circle[^>]*r="1\.25"[^>]*/>', "", svg)
    return svg.replace('fill="#dcdee0"', f'fill="{fill}"').replace('class="dots" ', 'xmlns="http://www.w3.org/2000/svg" ')

def main(src, out):
    src = Path(src)
    with tempfile.TemporaryDirectory() as t:
        d = Path(t) / "bm"; d.mkdir()
        shutil.copy(ROOT / "tools/brandmanual/index.html", d / "index.html")
        for sub in ("SVG", "Ikony", "Emailovy-podpis"):
            for f in (src / sub).glob("*"):
                if f.suffix in (".svg", ".png"): shutil.copy(f, d / f.name)
        shutil.copy(ROOT / "assets/img/og/default.jpg", d / "nahled-pro-sdileni-1200x630.jpg")
        shutil.copy(ROOT / "assets/img/brand/uvod-kulicky-b.jpg", d / "uvod-kulicky.jpg")
        (d / "kapky-svetle.svg").write_text(kapky("#dcdee0", False))
        (d / "kapky-tmave.svg").write_text(kapky("#3a4348", False))
        for p in ("assets/fonts",):
            shutil.copytree(ROOT / p, Path(t) / p)
        h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=t)
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h); port = srv.server_address[1]
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch(); pg = b.new_page()
            pg.goto(f"http://127.0.0.1:{port}/bm/index.html", wait_until="networkidle")
            pg.evaluate("document.fonts.ready"); pg.pdf(path=out, width="297mm", height="210mm", print_background=True)
            b.close()
        srv.shutdown()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
