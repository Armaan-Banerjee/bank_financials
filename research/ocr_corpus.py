#!/usr/bin/env python3
"""OCR every cached source PDF that has no text layer, into research/ocr_text/<md5>.txt.

RESUMABLE: skips any document whose sidecar already exists and is non-trivial, so a
kill (rate limit, reboot, Ctrl-C) costs only the document in flight. Re-run the same
command to continue.

Inputs  : research/doc_cache/*.pdf   (preserved 2026-09-16 from the fetch session's
                                      scratchpad, which does not survive that session)
Outputs : research/ocr_text/<same basename>.txt
Skipped : files that already carry a text layer, and cache entries that are not PDFs
          at all (saved HTML error pages - see the NOT-A-PDF note in the report).
"""
import os, glob, subprocess, sys, concurrent.futures as cf

CACHE, OUT = "research/doc_cache", "research/ocr_text"
MIN_TEXT = 400          # chars in first 15pp below which we treat it as image-only
WORKERS = int(os.environ.get("OCR_WORKERS", "4"))

def needs_ocr(p):
    if open(p, "rb").read(5) != b"%PDF-":
        return False                                   # HTML error page, not a document
    r = subprocess.run(["pdftotext", "-l", "15", p, "-"], capture_output=True)
    return len(r.stdout.decode("utf-8", "replace").strip()) < MIN_TEXT

def done(side):
    return os.path.exists(side) and os.path.getsize(side) > 200

def work(p):
    side = os.path.join(OUT, os.path.basename(p)[:-4] + ".txt")
    if done(side):
        return ("skip", p)
    tmp = side + ".partial"                            # never leave a truncated sidecar
    r = subprocess.run(["ocrmypdf", "--force-ocr", "--sidecar", tmp, "-q",
                        "--output-type", "none", p, "-"],
                       capture_output=True, timeout=900)
    if r.returncode != 0 or not os.path.exists(tmp):
        return ("fail", p)
    os.replace(tmp, side)
    return ("ok", p)

if __name__ == "__main__":
    todo = [p for p in sorted(glob.glob(f"{CACHE}/*.pdf")) if needs_ocr(p)]
    os.makedirs(OUT, exist_ok=True)
    todo = [p for p in todo if not done(os.path.join(OUT, os.path.basename(p)[:-4] + ".txt"))]
    print(f"to OCR: {len(todo)} (workers={WORKERS})", flush=True)
    n = {"ok": 0, "fail": 0, "skip": 0}
    with cf.ThreadPoolExecutor(WORKERS) as ex:
        for i, (status, p) in enumerate(ex.map(work, todo), 1):
            n[status] += 1
            if i % 25 == 0 or status == "fail":
                print(f"  {i}/{len(todo)}  ok={n['ok']} fail={n['fail']}", flush=True)
    print(f"DONE ok={n['ok']} fail={n['fail']} skip={n['skip']}", flush=True)
