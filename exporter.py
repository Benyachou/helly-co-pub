"""Exporte la pub en MP4 (1920x1080, 30 i/s), image par image.

    python exporter.py                       -> helly-co-pub.mp4 (index.html)
    python exporter.py v1-helyco-bleu-orange -> v1-helyco-bleu-orange.mp4
    python exporter.py --apercu 3 7.5        -> captures PNG aux secondes données
"""
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ICI = Path(__file__).resolve().parent
FPS = 30


def main():
    args = sys.argv[1:]
    nom = "index"
    if args and not args[0].startswith("--"):
        nom = args.pop(0).removesuffix(".html")
    url = (ICI / f"{nom}.html").as_uri() + "?export"
    with sync_playwright() as p:
        nav = p.chromium.launch()
        page = nav.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(url)
        page.evaluate("document.fonts.ready")
        total = page.evaluate("window.__total")

        if args and args[0] == "--apercu":
            for s in args[1:]:
                page.evaluate(f"window.__render({float(s)})")
                page.screenshot(path=str(ICI / f"apercu-{s}.png"))
            nav.close()
            return

        sortie = ICI / ("helly-co-pub.mp4" if nom == "index" else f"{nom}.mp4")
        ff = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
             "-c:v", "libx264", "-preset", "slow", "-crf", "18",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(sortie)],
            stdin=subprocess.PIPE,
        )
        n = round(total * FPS)
        for i in range(n):
            page.evaluate(f"window.__render({i / FPS})")
            ff.stdin.write(page.screenshot(type="png"))
            if i % FPS == 0:
                print(f"\r{i // FPS}/{int(total)} s", end="", flush=True)
        ff.stdin.close()
        ff.wait()
        nav.close()
        print(f"\n-> {sortie}")


if __name__ == "__main__":
    main()
