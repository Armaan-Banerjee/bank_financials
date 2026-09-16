#!/usr/bin/env python3
# PRESERVED 2026-09-16 from katalysis-d7's session scratchpad, which does not
# survive the session. Authored by that session during the Pillar 3 gap hunt;
# kept verbatim apart from the two path constants below, which were hardcoded
# to that scratchpad and are now overridable:
#
#   FCE_SCRATCH  output dir            (default: alongside this file)
#   FCE_CACHE    cached annual-report PDFs, named <md5(fetch_url)>.pdf
#
# Result when first run: 18 candidates across 2 banks, ZERO remuneration false
# positives. FCE Bank confirmed as the class (6 docs FY2015-FY2020); Clydesdale
# examined and RULED OUT (cites a separate Pillar 3 in 10 of 12 documents).
# REACH: 482 documents were searchable; 653 (58%) are scanned with no text layer
# and were NEVER SEARCHED. The result is "zero new instances among the 482
# searchable", NOT "no other bank embeds its Pillar 3".
"""Hunt the FCE CLASS: banks that embed their CAPITAL Pillar 3 INSIDE another document.

WHY THIS CLASS IS INVISIBLE: FCE Bank's annual report says "This chapter contains the remaining
Pillar 3 disclosures required by Part Eight of the CRR". There is no standalone Pillar 3 PDF and there
never will be, so a filename hunt fails forever while the disclosures sit in a document already held.
Such a bank looks identical, from outside, to one that never disclosed at all.

THE DISCRIMINATOR: "Part Eight of the CRR" IS the capital/prudential Pillar 3 requirement. Remuneration
disclosures come from CRD/the Remuneration Code, climate from TCFD. So Part Eight is a strong positive
for the capital disclosure specifically -- which matters because FCE carries BOTH a remuneration Pillar 3
mention and an embedded capital chapter. Filtering remuneration documents out wholesale would have
discarded the very document that defined the class. Flag both; never auto-exclude.

DISCIPLINE (earned tonight, expensively):
  - Normalise whitespace BEFORE matching. A line-fragmented text layer makes `x\\s*y` match the whole
    text but never a single line, which produced three separate false zeroes tonight.
  - A hit proves the DOCUMENT discusses Pillar 3. It does NOT prove the figures are in it. Those are
    separate claims needing separate evidence (the ICICI error). So every candidate is additionally
    probed for actual capital TABLES, and the two results are reported in different columns.
  - Report candidates, never verdicts.

Usage: fce_pattern.py <ar_hits.jsonl>
"""
import json, os, re, sys, subprocess, hashlib, collections

S = os.environ.get("FCE_SCRATCH") or os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("FCE_CACHE") or f"{S}/ar_cache"

# --- the embedded-disclosure signature -------------------------------------------------
PART8 = re.compile(r"Part\s+(Eight|8|VIII)\b[^.]{0,60}\bCRR\b|\bCRR\b[^.]{0,40}Part\s+(Eight|8|VIII)\b", re.I)
EMBEDDED = re.compile(
    r"(this|the)\s+(chapter|section|report|document|annual\s+report)\s+"
    r"(contains|sets?\s+out|includes?|provides?|comprises?)[^.]{0,90}?Pillar\s*3"
    r"|Pillar\s*3[^.]{0,90}?\b(are|is)\s+(included|contained|set\s+out|presented|incorporated|disclosed)"
    r"[^.]{0,70}?\b(in|within)\s+(this|these)\b"
    r"|Pillar\s*3[^.]{0,70}?(in\s+this\s+annual\s+report|in\s+these\s+financial\s+statements|herein)",
    re.I)
# The already-understood class: published SEPARATELY on a website. Not this hunt.
SEPARATE = re.compile(r"Pillar\s*3[^.]{0,90}?(web\s?site|www\.|separate\s+document|published\s+separately)", re.I)

# Does the document actually carry capital TABLES? Retrievability != availability.
CAPTAB = {
    "CET1 ratio": re.compile(r"(Common\s+Equity\s+Tier\s*1|CET\s*1)[^.\n]{0,40}ratio", re.I),
    "leverage": re.compile(r"[Ll]everage\s+ratio", re.I),
    "RWA": re.compile(r"[Rr]isk[- ]weighted\s+(assets|exposure)", re.I),
    "LCR": re.compile(r"[Ll]iquidity\s+[Cc]overage\s+[Rr]atio|\bLCR\b"),
    "own funds": re.compile(r"[Oo]wn\s+funds", re.I),
}

rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
seen, cands = set(), []
stats = collections.Counter()

for r in rows:
    furl = r.get("fetch_url") or r.get("url")
    if not furl or furl in seen:
        continue
    seen.add(furl)
    p = f"{CACHE}/{hashlib.md5(furl.encode()).hexdigest()}.pdf"
    if not os.path.exists(p):
        stats["no_cached_file"] += 1
        continue
    raw = subprocess.run(["pdftotext", "-layout", p, "-"],
                         capture_output=True).stdout.decode("utf-8", errors="replace")
    if len(raw.strip()) < 400:
        stats["scanned_no_text (blind spot)"] += 1
        continue
    stats["searchable"] += 1
    n = " ".join(raw.split())          # <-- normalise FIRST. Tonight's most expensive lesson.

    p8 = PART8.search(n)
    emb = EMBEDDED.search(n)
    if not (p8 or emb):
        continue
    stats["CANDIDATE"] += 1

    banks = sorted({t.split(":")[0].replace("build_", "").replace(".py", "")
                    for t in (r.get("cited_by") or [])})
    years = sorted({t.split(":")[1] for t in (r.get("cited_by") or []) if ":" in t})
    tables = [k for k, rx in CAPTAB.items() if rx.search(n)]
    cands.append({
        "banks": banks, "years": years, "url": r.get("url"),
        "part8": " ".join(p8.group(0).split())[:120] if p8 else None,
        "embedded": " ".join(emb.group(0).split())[:200] if emb else None,
        "also_says_separate": bool(SEPARATE.search(n)),
        "capital_tables": tables,
    })

with open(f"{S}/fce_candidates.jsonl", "w") as fh:
    for c in cands:
        fh.write(json.dumps(c) + "\n")

print("=" * 100)
print("FCE-CLASS HUNT — Pillar 3 embedded inside another document")
for k, v in stats.most_common():
    print(f"  {v:>5}  {k}")
print("=" * 100)

strong = [c for c in cands if c["part8"]]
weak = [c for c in cands if not c["part8"]]

print(f"\n### STRONG — cites Part Eight CRR (the CAPITAL Pillar 3 requirement): {len(strong)}")
for c in sorted(strong, key=lambda c: c["banks"]):
    print(f"\n  {','.join(c['banks']) or '?'} {','.join(c['years'])}")
    print(f"    PART8   : {c['part8']}")
    if c["embedded"]:
        print(f"    EMBEDDED: {c['embedded']}")
    print(f"    capital tables present: {', '.join(c['capital_tables']) or 'NONE — hit is not a figure'}")
    if c["also_says_separate"]:
        print("    NOTE: document ALSO refers to a separate/website Pillar 3 — read before concluding")
    print(f"    {(c['url'] or '')[:112]}")

print(f"\n### WEAKER — embedded phrasing only, no Part Eight: {len(weak)}")
for c in sorted(weak, key=lambda c: c["banks"])[:40]:
    print(f"  {','.join(c['banks']) or '?'} {','.join(c['years'])}  tables={','.join(c['capital_tables']) or 'none'}"
          f"{'  [also says separate]' if c['also_says_separate'] else ''}")
    print(f"      {c['embedded']}")
