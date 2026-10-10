#!/usr/bin/env python3
"""Render PDF pages into the inputs used for transcription.

The LOC scan of the 1833 Book of Commandments is a photograph of a tiny book: each PDF page is
the book page lying open on a dark surface, with the cloth binding and page edges visible, the text
in a column covering only part of the image, and faint, uneven ink (often with the reverse side's
text showing through). So each page is cut into overlapping horizontal bands that exclude the right-hand
binding, and each band is converted to grayscale with auto-contrast, which makes faint type far easier
to read. Use --color to also keep the original-colour crops (useful for stains and handwriting).

For each page N this writes, under <out>/:
  img/pNNNN_0_overview.jpg   whole page, low resolution, original colour (layout only)
  img/pNNNN_1_top.jpg        top band, enhanced grayscale
  img/pNNNN_2_mid.jpg        middle band
  img/pNNNN_3_bottom.jpg     bottom band (bands overlap; do not duplicate lines seen in two)
  img/pNNNN_cK_*.jpg         (with --color) the same bands in original colour

Requires: pypdfium2 and Pillow. (The LOC scan has no text layer, so no OCR helper text is written.)

Usage:
  python3 tools/render_pages.py scan.pdf --out work               # all pages
  python3 tools/render_pages.py scan.pdf --out work --pages 1-16,102
  python3 tools/render_pages.py scan.pdf --out work --pages 40 --scale 4   # zoom for a doubtful spot
"""
import argparse
from pathlib import Path

import pypdfium2 as pdfium
from PIL import ImageOps

BANDS = 3
X0, X1 = 0.02, 0.97   # keep this horizontal fraction of the page (recto text reaches ~90%; the binding is only partly cropped)
OVERLAP = 0.06        # fraction of page height shared by neighbouring bands


def parse_pages(spec, total):
    if not spec:
        return list(range(1, total + 1))
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return pages


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", help="path to the scan PDF")
    ap.add_argument("--out", default="work", help="output directory (default: ./work)")
    ap.add_argument("--pages", help="pages to render, e.g. 1-16,102 (default: all)")
    ap.add_argument("--scale", type=float, default=2, help="render scale for the crops (default: 2)")
    ap.add_argument("--color", action="store_true", help="also save original-colour band crops")
    args = ap.parse_args()

    out = Path(args.out)
    (out / "img").mkdir(parents=True, exist_ok=True)

    doc = pdfium.PdfDocument(args.pdf)
    print(f"{len(doc)} pages in {args.pdf}")
    names = ["1_top", "2_mid", "3_bottom"]
    for n in parse_pages(args.pages, len(doc)):
        page = doc[n - 1]
        im = page.render(scale=args.scale).to_pil().convert("RGB")
        w, h = im.size
        im.resize((w // 3, h // 3)).save(out / "img" / f"p{n:04d}_0_overview.jpg", quality=70)
        x0, x1 = int(w * X0), int(w * X1)
        step = h / BANDS
        pad = int(h * OVERLAP)
        for i, name in enumerate(names):
            y0 = max(0, int(i * step) - pad)
            y1 = min(h, int((i + 1) * step) + pad)
            col = im.crop((x0, y0, x1, y1))
            ImageOps.autocontrast(col.convert("L"), cutoff=1).save(out / "img" / f"p{n:04d}_{name}.jpg", quality=88)
            if args.color:
                col.save(out / "img" / f"p{n:04d}_c{name}.jpg", quality=85)


if __name__ == "__main__":
    main()
