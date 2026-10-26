#!/usr/bin/env python3
"""Promote quarantined ocr_lead records to a 300 dpi verified finding.

An ocr_lead is a LEAD, not a finding: the sweep agent located a figure in a
PDF's born-digital text layer but could not render the page, so nobody has
ever SEEN it. merge_sweep.py therefore quarantines them and they never reach
published_returns.jsonl. This tool does the one thing that closes that gap:
fetch the cited document, confirm it really is a PDF, and render the cited
page at 300 dpi so a human (or a vision-capable model) can read the figure
off the page as printed.

It deliberately stops there. It renders and reports; it does NOT decide that
a lead is confirmed, because the whole point of the 300dpi state is that
someone looked. Record the outcome with --record once you have looked.

Run order:
    promote_leads.py --fetch          # download + verify + render, writes manifest
    (look at the PNGs)
    promote_leads.py --record FILE    # merge confirmed records into the store

Traps this tool exists to avoid:
  * An HTTP 200 is not a PDF. Soft-404s here serve the bank's homepage with a
    200 and an HTML body; we check the %PDF magic bytes AND the Content-Type.
  * "PDF p.N" in a citation is the PDF's own page index, which is usually NOT
    the printed folio. Render the PDF index, then read the printed number off
    the render to confirm the citation names both correctly.
  * A lead whose entity is not the workbook perimeter is NOT promotable
    however clear the render is - it is a different claim. Those are reported
    separately as `excluded`, which is a finding, not a failure.
"""

import argparse
import collections
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SWEEP = os.path.join(ROOT, "sweep")
STORE = os.path.join(ROOT, "published_returns.jsonl")

# A PDF URL need NOT end in ".pdf". Secure Trust serves its 206-page
# annual report from a path ending "...reports-and-accounts-2025-final-
# 483796420288" with Content-Type application/pdf. An extension-anchored
# regex skipped it and reported the bank as having "no URL cited" when
# the citation was complete and correct. Take any http(s) URL and let
# fetch() decide what it is from the magic bytes - that is the only
# test that was ever load-bearing.
URL_RE = re.compile(r"(https?://[^\s,;)\]]+)", re.I)
PDFPAGE_RE = re.compile(r"PDF p\.(\d+)")
PRINTED_RE = re.compile(r"printed p\.(\d+)")

# An entity line the sweep agents wrote that says, in their own words, that
# the figure is NOT the workbook's perimeter. Matched on the explicit "not"
# phrasing they used rather than guessed at from the entity name.
NOT_PERIMETER_RE = re.compile(r"\bnot the workbook", re.I)


def load_leads():
    leads = []
    for path in sorted(glob.glob(os.path.join(SWEEP, "batch_*.jsonl"))):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                if rec.get("verification") == "ocr_lead":
                    rec["_batch"] = os.path.basename(path)
                    leads.append(rec)
    return leads


def bank_urls(leads):
    """Every distinct PDF URL any lead for this bank cites.

    Comparative records cite the document in prose without repeating the URL,
    so the URL must be pooled across the bank's leads, not read per record.
    """
    urls = collections.OrderedDict()
    for rec in leads:
        for url in URL_RE.findall(rec.get("source", "")):
            urls.setdefault(url, []).append(rec)
    return urls


def fetch(url, dest):
    """Download and prove it is a PDF. Returns (ok, content_type, note)."""
    proc = subprocess.run(
        ["curl", "-sS", "-L", "--max-time", "120",
         "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
         "-w", "%{content_type}|%{http_code}", "-o", dest, url],
        capture_output=True, text=True)
    if proc.returncode != 0:
        return False, "", "curl failed: %s" % proc.stderr.strip()[:200]
    meta = proc.stdout.strip().rsplit("|", 1)
    ctype = meta[0] if meta else ""
    code = meta[1] if len(meta) > 1 else "?"
    if not os.path.exists(dest) or os.path.getsize(dest) == 0:
        return False, ctype, "empty body (HTTP %s)" % code
    with open(dest, "rb") as fh:
        magic = fh.read(5)
    if magic[:4] != b"%PDF":
        return False, ctype, ("HTTP %s but body is not a PDF (magic %r) - "
                              "soft-404 or access control" % (code, magic))
    if "pdf" not in ctype.lower():
        return True, ctype, ("magic bytes are %PDF but Content-Type is %r - "
                             "serving quirk, treating as PDF" % ctype)
    return True, ctype, "HTTP %s, %s, %d bytes" % (
        code, ctype, os.path.getsize(dest))


def npages(path):
    proc = subprocess.run(["pdfinfo", path], capture_output=True, text=True)
    m = re.search(r"^Pages:\s+(\d+)", proc.stdout, re.M)
    return int(m.group(1)) if m else 0


def find_pages(pdf, recs, total):
    """Pages worth rendering: the cited one, plus any the text layer suggests.

    A citation may be absent or wrong, so this does not trust it alone: it
    also greps the text layer for each lead's own value string. pdftotext
    returning nothing is NOT evidence the figure is absent - the page may be
    a scan - so a cited page is always rendered even when the grep is silent.
    """
    pages = collections.OrderedDict()
    for rec in recs:
        m = PDFPAGE_RE.search(rec.get("source", ""))
        if m:
            p = int(m.group(1))
            if 1 <= p <= total:
                pages.setdefault(p, []).append("cited as PDF p.%d" % p)
    values = {str(r.get("value", "")).strip() for r in recs}
    values = {v for v in values if v}
    for page in range(1, total + 1):
        proc = subprocess.run(
            ["pdftotext", "-f", str(page), "-l", str(page), pdf, "-"],
            capture_output=True, text=True)
        text = proc.stdout
        if not text.strip():
            continue
        flat = re.sub(r"\s+", " ", text)
        hits = [v for v in values if v in flat or v.rstrip("%") in flat]
        if len(hits) >= 2 or (hits and re.search(
                r"return on (equity|assets|average)", flat, re.I)):
            pages.setdefault(page, []).append(
                "text layer carries %s" % ", ".join(sorted(hits)[:4]))
    return pages


def render(pdf, page, outdir, stem):
    base = os.path.join(outdir, "%s_p%03d" % (stem, page))
    proc = subprocess.run(
        ["pdftoppm", "-r", "300", "-f", str(page), "-l", str(page),
         "-png", pdf, base],
        capture_output=True, text=True)
    if proc.returncode != 0:
        return None, proc.stderr.strip()[:200]
    hits = sorted(glob.glob(base + "*.png"))
    return (hits[0] if hits else None), ""


def do_fetch(outdir):
    os.makedirs(outdir, exist_ok=True)
    leads = load_leads()
    by_bank = collections.defaultdict(list)
    for rec in leads:
        by_bank[rec["bank"]].append(rec)

    manifest = {"targets": [], "excluded": [], "unfetchable": []}
    print("%d ocr_lead records across %d banks\n" % (len(leads), len(by_bank)))

    for bank in sorted(by_bank):
        recs = by_bank[bank]
        wrong = [r for r in recs
                 if NOT_PERIMETER_RE.search(r.get("entity", ""))]
        if wrong and len(wrong) == len(recs):
            print("%-32s EXCLUDED - %s" % (bank, recs[0].get("entity", "")))
            manifest["excluded"].append({
                "bank": bank, "entity": recs[0].get("entity", ""),
                "records": len(recs),
                "reason": "entity is not the workbook perimeter; a different "
                          "claim, so no render can promote it"})
            continue

        urls = bank_urls(recs)
        if not urls:
            print("%-32s NO URL cited in any of its %d leads" % (bank, len(recs)))
            manifest["unfetchable"].append({
                "bank": bank, "records": len(recs),
                "reason": "no PDF URL in any citation"})
            continue

        bankstem = re.sub(r"[^A-Za-z0-9]+", "_", bank).strip("_").lower()
        for i, url in enumerate(urls):
            # The URL index MUST be in the render stem, not just the pdf name.
            # Two editions of one bank's report routinely carry the same
            # figure on the same PDF page (Weatherbys 2023 and 2024 both put
            # it on p.8), and without the index the second render silently
            # OVERWRITES the first - same path, no error, one document lost.
            stem = "%s_d%d" % (bankstem, i)
            dest = os.path.join(outdir, "%s.pdf" % stem)
            ok, ctype, note = fetch(url, dest)
            if not ok:
                print("%-32s FETCH FAILED %s\n%34s%s" % (bank, url, "", note))
                manifest["unfetchable"].append({
                    "bank": bank, "url": url, "reason": note})
                continue
            total = npages(dest)
            pages = find_pages(dest, recs, total)
            print("%-32s %s (%d pages) %s" % (bank, note, total, url))
            if not pages:
                print("%34s no page located - rendering nothing" % "")
                manifest["unfetchable"].append({
                    "bank": bank, "url": url,
                    "reason": "no cited page and no text-layer hit in %d pages"
                              % total})
                continue
            for page, why in sorted(pages.items()):
                png, err = render(dest, page, outdir, stem)
                if not png:
                    print("%34srender of p.%d failed: %s" % ("", page, err))
                    continue
                print("%34sp.%-4d %s" % ("", page, "; ".join(why)))
                print("%34s  -> %s" % ("", png))
                manifest["targets"].append({
                    "bank": bank, "url": url, "pdf_page": page,
                    "why_this_page": why, "png": png, "pdf": dest,
                    "pdf_pages": total,
                    "claims": [{"year": r.get("year"),
                                "measure": r.get("measure"),
                                "value": r.get("value"),
                                "definition": r.get("definition"),
                                "printed_page": (
                                    PRINTED_RE.search(r.get("source", "")).group(1)
                                    if PRINTED_RE.search(r.get("source", ""))
                                    else None),
                                "own_edition": r.get("own_edition"),
                                "entity": r.get("entity"),
                                "batch": r.get("_batch")} for r in recs]})

    path = os.path.join(outdir, "manifest.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
    print("\n%d render targets, %d excluded banks, %d unfetchable"
          % (len(manifest["targets"]), len(manifest["excluded"]),
             len(manifest["unfetchable"])))
    print("manifest: %s" % path)


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fetch", action="store_true",
                    help="download, verify and render the cited pages")
    ap.add_argument("--outdir", default=os.environ.get(
        "PROMOTE_OUTDIR", "/tmp/promote_leads"),
        help="where PDFs, renders and the manifest go (not the repo)")
    args = ap.parse_args(argv)
    if args.fetch:
        do_fetch(args.outdir)
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
