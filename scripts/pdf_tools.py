"""
Small CLI helper for researching bank annual report / Pillar 3 PDFs when
building a new "<BANK> FINANCIALS.xlsx" workbook (see bank_workbook.py).
Saves re-writing the same curl + fitz boilerplate for every source document.

Usage:
    python3 pdf_tools.py download <url> <out.pdf>
        Fetch a PDF with a browser-like User-Agent.

    python3 pdf_tools.py find <file.pdf> <term> [term2 ...]
        Print the (0-indexed) page number and a short snippet for every page
        containing ANY of the given terms (case-insensitive). Page indices
        printed here are what `text`/`render` expect - NOT necessarily the
        document's own printed page number (check the snippet/text for that).

    python3 pdf_tools.py text <file.pdf> <idx> [idx2 ...]
        Print the full extracted text of one or more pages (0-indexed).

    python3 pdf_tools.py render <file.pdf> <idx> <out.png>
        Render a page to PNG at 200dpi - use this for pages with 0 text
        blocks and >=1 image (common for "signed" statutory statement pages
        that flatten a signature block to an image); view the PNG with the
        Read tool.

    python3 pdf_tools.py scan <file.pdf>
        Print every page's (text_block_count, image_count) - a quick way to
        spot image-only pages across a whole document before hunting for a
        specific table.
"""
import sys

import fitz  # PyMuPDF


def download(url, out_path):
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(out_path, "wb") as f:
        f.write(resp.read())
    print(f"Saved {out_path}")


def find(pdf_path, terms):
    doc = fitz.open(pdf_path)
    terms_low = [t.lower() for t in terms]
    for i, page in enumerate(doc):
        text = page.get_text()
        low = text.lower()
        if any(t in low for t in terms_low):
            snippet = text[:120].replace("\n", " ")
            print(f"{i}: {snippet}")


def text(pdf_path, idxs):
    doc = fitz.open(pdf_path)
    for i in idxs:
        print(f"--- idx {i} ---")
        print(doc[int(i)].get_text())
        print()


def render(pdf_path, idx, out_path):
    doc = fitz.open(pdf_path)
    pix = doc[int(idx)].get_pixmap(dpi=200)
    pix.save(out_path)
    print(f"Saved {out_path} ({pix.width}x{pix.height})")


def scan(pdf_path):
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        blocks = len(page.get_text("blocks"))
        imgs = len(page.get_images())
        flag = "  <-- image-only" if blocks == 0 and imgs > 0 else ""
        print(f"{i}: text_blocks={blocks} images={imgs}{flag}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "download":
        download(args[0], args[1])
    elif cmd == "find":
        find(args[0], args[1:])
    elif cmd == "text":
        text(args[0], args[1:])
    elif cmd == "render":
        render(args[0], args[1], args[2])
    elif cmd == "scan":
        scan(args[0])
    else:
        print(__doc__)
        sys.exit(1)
