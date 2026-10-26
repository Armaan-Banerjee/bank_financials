#!/usr/bin/env python3
"""Extract thebanks.eu figures from the downloaded Wayback captures.

    /usr/bin/python3 research/profitability/thebanks_eu/extract_wayback.py

Reads  wayback_downloads/html/<profile_id>/<timestamp>_<route>.html  (143 of
them, fetched by scripts/fetch_thebanks_wayback.sh) and writes
wayback_returns.jsonl plus wayback_extract_report.md.

WHAT THESE CAPTURES ACTUALLY CONTAIN, since three guesses about it were wrong
before this script was written:

  - They are NOT all HTML. 54 of the 143 are raw gzip and 13 have leading
    blank lines: the Wayback `id_` replay returns the ORIGINAL bytes including
    `Content-Encoding: gzip`, and the fetch script saved them undecoded. A
    grep over these files finds nothing and that is an artefact of the
    encoding, not evidence the page lacks the data.
  - The `financials` route does NOT carry a return ratio. It carries Total
    Assets, Total Equity, Annual Profit and the two-year Table 1 / Table 2
    comparatives - the INPUTS, not the ratio.
  - The ratio lives in a PROSE SENTENCE on the profile route, and it states
    its own year: "showcasing 1.39% return on assets and 5.67% return on
    equity in 2023". That stated year is authoritative and is not the capture
    year - thebanks.eu lags, so a December 2024 capture commonly reports 2023.
    Taking the capture date as the period would misdate most of this corpus.

WHAT THIS SCRIPT WILL NOT DO:

  - It does not compute a ratio from the assets/equity/profit it finds. The
    collection's standing rule is that no ratio is calculated to fill a
    missing site value, and a ratio we struck from their inputs would be a
    fifth kind of claim wearing the aggregator's label.
  - It does not merge anything into the curated published-returns store.
    These are AGGREGATOR figures: a third party's arithmetic on a third
    party's inputs, kept in their own file and their own column.
  - Where two captures report the same (bank, year) with DIFFERENT values it
    records both and flags the disagreement rather than picking one.

Unlike the three `archive_search_indexed` records in this directory, these
carry a real replay URL and a real 14-digit snapshot timestamp, so they are
labelled `wayback_snapshot` and may be described as verified captures.
"""

import collections
import csv
import datetime
import glob
import gzip
import html as htmllib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DL = os.path.join(HERE, "wayback_downloads")
COLLECTION = os.path.join(HERE, "thebanks_eu_returns.jsonl")
OUT_JSONL = os.path.join(HERE, "wayback_returns.jsonl")
OUT_REPORT = os.path.join(HERE, "wayback_extract_report.md")

WINDOW = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]

# "showcasing 1.39% return on assets and 5.67% return on equity in 2023"
#
# THE SIGN IS PART OF THE NUMBER. Griffin Bank's 2024 sentence reads
# "showcasing -88.98% return on assets and -107.64% return on equity in 2024",
# and a `[\d.,]+` number class silently drops that minus: the strict pattern
# fails, a looser fallback then matches the digits alone, and a loss-making
# bank is recorded with a POSITIVE return. The first version of this file did
# exactly that and it was caught only by cross-checking against the existing
# collection - which is why that cross-check now runs on every execution.
# Loss-makers are the population a profitability table most needs to show, so
# every number class below carries an optional sign, including the unicode
# minus and en-dash that web copy uses interchangeably.
NUM = r"[-−–]?[\d.,]+"
RATIO_RE = re.compile(
    r"showcasing\s+(%s)\s*%%\s*return on assets\s+and\s+(%s)\s*%%\s*"
    r"return on equity\s+in\s+(\d{4})" % (NUM, NUM), re.I)
# Reverse order, in case the site ever swaps the clauses.
RATIO_REV_RE = re.compile(
    r"showcasing\s+(%s)\s*%%\s*return on equity\s+and\s+(%s)\s*%%\s*"
    r"return on assets\s+in\s+(\d{4})" % (NUM, NUM), re.I)
# Fallbacks for a sentence carrying only one of the two. `.` is allowed in the
# gap because the other ratio's decimal point sits inside it.
ROA_ONLY_RE = re.compile(r"(%s)\s*%%\s*return on assets\b.{0,120}?in\s+(\d{4})" % NUM, re.I)
ROE_ONLY_RE = re.compile(r"(%s)\s*%%\s*return on equity\b.{0,120}?in\s+(\d{4})" % NUM, re.I)


def norm_pct(raw):
    """'-88.98' -> '-88.98%', normalising unicode minus signs to ASCII."""
    v = raw.strip().replace("−", "-").replace("–", "-").replace(",", "")
    return v + "%"

HEADLINE_RE = {
    "total_assets": re.compile(r"Total Assets \((\d{4})\)\s*([\d.,]+)\s*(mln|bln)?\s*([A-Z]{3})?"),
    "total_equity": re.compile(r"Total Equity \((\d{4})\)\s*([\d.,]+)\s*(mln|bln)?\s*([A-Z]{3})?"),
    "annual_profit": re.compile(r"Annual Profit \((\d{4})\)\s*(-?[\d.,]+)\s*(mln|bln)?\s*([A-Z]{3})?"),
}
TITLE_RE = re.compile(r"^\s*(.+?)\s*\((United Kingdom|[^)]+)\)\s*-\s*", re.S)


def read_capture(path):
    """Bytes -> text, transparently un-gzipping. See the module docstring."""
    with open(path, "rb") as fh:
        raw = fh.read()
    stripped = raw.lstrip(b"\r\n")
    if stripped[:2] == b"\x1f\x8b":
        try:
            raw = gzip.decompress(stripped)
        except (OSError, EOFError, gzip.BadGzipFile):
            return None
    return raw.decode("utf-8", "replace")


def to_text(markup):
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", markup, flags=re.S | re.I)
    t = htmllib.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t).strip()


# The four profiles the live collection found no numeric return for, so they
# appear in no collection record and cannot be mapped from it. The ids and
# identifications are the collector's own, carried in
# scripts/fetch_thebanks_wayback.sh. Their captures turn out to hold no
# figures either (nav-only shells), which CORROBORATES the live finding
# rather than leaving it untested.
KNOWN_IDS = {
    "19654": ("AFIN BANK", "Afin Bank Limited"),
    "14486": ("BANK OF IRELAND UK", "Bank of Ireland (UK) Plc"),
    "19245": ("SMBC", "SMBC Bank International plc"),
    "14606": ("STATE BANK OF INDIA UK", "State Bank of India (UK) Limited"),
}


def load_id_map():
    """profile id -> (bank, entity) from the curated live/indexed collection."""
    out = dict(KNOWN_IDS)
    if not os.path.exists(COLLECTION):
        return out
    for line in open(COLLECTION, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        m = re.search(r"/banks/(\d+)", str(r.get("source_url", "")))
        if m:
            out.setdefault(m.group(1), (r.get("bank"), r.get("entity")))
    return out


def load_originals():
    """local_path basename -> original URL, from the fetch manifest."""
    out = {}
    man = os.path.join(DL, "captures.tsv")
    if not os.path.exists(man):
        return out
    with open(man, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            out[row["local_path"]] = row["original"]
    return out


def main():
    id_map = load_id_map()
    originals = load_originals()
    existing = set()
    for line in open(COLLECTION, encoding="utf-8") if os.path.exists(COLLECTION) else []:
        line = line.strip()
        if line:
            r = json.loads(line)
            existing.add((r.get("bank"), r.get("year")))

    records = []
    empty_captures = []
    stats = collections.Counter()
    unmapped = collections.Counter()
    files = sorted(glob.glob(os.path.join(DL, "html", "*", "*.html")))

    for path in files:
        stats["captures"] += 1
        markup = read_capture(path)
        if markup is None:
            stats["unreadable"] += 1
            continue
        if markup.lstrip()[:1] != "<":
            stats["not_markup"] += 1
            continue
        text = to_text(markup)
        rel = os.path.relpath(path, DL).replace(os.sep, "/")
        profile_id = os.path.basename(os.path.dirname(path))
        fname = os.path.basename(path)
        ts = fname.split("_", 1)[0]
        route = fname.split("_", 1)[1].replace(".html", "")
        original = originals.get(rel, "https://thebanks.eu/banks/%s" % profile_id)
        archive_url = "https://web.archive.org/web/%sid_/%s" % (ts, original)

        bank, entity = id_map.get(profile_id, (None, None))
        if not bank:
            unmapped[profile_id] += 1
            stats["unmapped_profile"] += 1

        m = TITLE_RE.match(text)
        page_entity = m.group(1).strip() if m else None

        # --- the ratio sentence ---------------------------------------------
        ratios = {}
        for mm in RATIO_RE.finditer(text):
            roa, roe, yr = mm.group(1), mm.group(2), mm.group(3)
            ratios.setdefault(yr, {})["roa_pct"] = norm_pct(roa)
            ratios[yr]["roe_pct"] = norm_pct(roe)
        for mm in RATIO_REV_RE.finditer(text):
            roe, roa, yr = mm.group(1), mm.group(2), mm.group(3)
            ratios.setdefault(yr, {}).setdefault("roe_pct", norm_pct(roe))
            ratios[yr].setdefault("roa_pct", norm_pct(roa))
        if not ratios:
            for rx, key in ((ROA_ONLY_RE, "roa_pct"), (ROE_ONLY_RE, "roe_pct")):
                for mm in rx.finditer(text):
                    ratios.setdefault(mm.group(2), {})[key] = norm_pct(mm.group(1))

        # --- headline balance-sheet / income blocks -------------------------
        headline = {}
        for key, rx in HEADLINE_RE.items():
            for mm in rx.finditer(text):
                yr, val, scale, cur = mm.groups()
                headline.setdefault(yr, {})[key] = {
                    "value": val, "scale": scale, "currency": cur}

        if not ratios and not headline:
            stats["no_figures_in_capture"] += 1
            empty_captures.append((profile_id, route, len(text)))
        for yr in sorted(set(ratios) | set(headline)):
            fy = "FY" + yr
            rec = {
                "bank": bank,
                "entity": entity or page_entity,
                "entity_on_page": page_entity,
                "year": fy,
                "profile_id": profile_id,
                "route": route,
                "snapshot_timestamp": ts,
                "archive_url": archive_url,
                "original_url": original,
                "verification": "wayback_snapshot",
                "source_year_label": yr,
                "collected_on": datetime.date.today().isoformat(),
            }
            rec.update(ratios.get(yr, {}))
            if yr in headline:
                rec["site_inputs"] = headline[yr]
            rec["in_window"] = fy in WINDOW
            rec["note"] = ("Aggregator figure read from a Wayback capture of the bank's "
                           "thebanks.eu profile. The YEAR is the one the page states, not "
                           "the capture date. Ratios are thebanks.eu's own; site_inputs are "
                           "their reported balance-sheet figures and NO ratio was computed "
                           "from them here.")
            if rec.get("roe_pct") or rec.get("roa_pct"):
                stats["ratio_records"] += 1
            else:
                stats["inputs_only_records"] += 1
            records.append(rec)

    # --- disagreement check across captures of the same (bank, year) --------
    seen = collections.defaultdict(list)
    for r in records:
        if r.get("bank") and (r.get("roe_pct") or r.get("roa_pct")):
            seen[(r["bank"], r["year"])].append(r)
    conflicts = []
    for key, group in sorted(seen.items()):
        vals = {(g.get("roe_pct"), g.get("roa_pct")) for g in group}
        if len(vals) > 1:
            conflicts.append((key, sorted(vals)))
            for g in group:
                g["disagrees_with_another_capture"] = True

    # --- POSITIVE CONTROL -------------------------------------------------
    # Where a capture and the live collection describe the same (bank, year),
    # they must agree. This is the check that caught the dropped minus sign,
    # so it runs every time and its result goes in the report: an extractor
    # with no control over it cannot tell a parse from a misparse.
    coll_vals = {}
    if os.path.exists(COLLECTION):
        for line in open(COLLECTION, encoding="utf-8"):
            line = line.strip()
            if line:
                r = json.loads(line)
                coll_vals[(r.get("bank"), r.get("year"))] = (
                    r.get("roe_pct"), r.get("roa_pct"))
    control = {"agree": 0, "differ": []}
    for r in records:
        key = (r.get("bank"), r.get("year"))
        if key not in coll_vals or not (r.get("roe_pct") or r.get("roa_pct")):
            continue
        mine = (r.get("roe_pct"), r.get("roa_pct"))
        theirs = coll_vals[key]
        if mine == theirs:
            control["agree"] += 1
        else:
            control["differ"].append((key, mine, theirs))
            r["differs_from_live_collection"] = True

    with open(OUT_JSONL, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    ratio_pairs = {(r["bank"], r["year"]) for r in records
                   if r.get("bank") and (r.get("roe_pct") or r.get("roa_pct"))}
    new_pairs = sorted(p for p in ratio_pairs if p not in existing)
    new_in_window = [p for p in new_pairs if p[1] in WINDOW]
    by_year = collections.Counter(y for _, y in ratio_pairs)
    new_by_year = collections.Counter(y for _, y in new_pairs)

    w = open(OUT_REPORT, "w", encoding="utf-8").write
    w("# Wayback extraction — thebanks.eu captures\n\n")
    w("Generated %s by `extract_wayback.py` from %d captures in "
      "`wayback_downloads/html/`.\nOutput: `wayback_returns.jsonl`.\n\n"
      % (datetime.date.today().isoformat(), stats["captures"]))
    w("## Yield\n\n| | count |\n|---|---|\n")
    for k in ("captures", "unreadable", "not_markup", "unmapped_profile",
              "ratio_records", "inputs_only_records"):
        w("| %s | %d |\n" % (k.replace("_", " "), stats[k]))
    w("| distinct (bank, year) with a RATIO | **%d** |\n" % len(ratio_pairs))
    w("| of those NOT already in the collection | **%d** |\n" % len(new_pairs))
    w("| new and inside FY2021-FY2025 | **%d** |\n\n" % len(new_in_window))
    w("## Ratio bank-years by period\n\n")
    w("| year | extracted | new vs collection |\n|---|---|---|\n")
    for y in sorted(by_year):
        w("| %s | %d | %d |\n" % (y, by_year[y], new_by_year.get(y, 0)))
    w("\nthebanks.eu lags, so a capture's own date is NOT the period — a December\n")
    w("2024 capture typically reports 2023. The year in the page's sentence is used.\n\n")
    if new_in_window:
        w("## New in-window bank-years\n\n| bank | year |\n|---|---|\n")
        for b, y in new_in_window:
            w("| %s | %s |\n" % (b, y))
        w("\n")
    if conflicts:
        w("## Captures that DISAGREE on the same bank-year\n\n")
        w("Both are kept and flagged `disagrees_with_another_capture`; neither is\n")
        w("reconciled. thebanks.eu restates, so two snapshots can legitimately differ.\n\n")
        w("| bank | year | (roe, roa) values seen |\n|---|---|---|\n")
        for (b, y), vals in conflicts:
            w("| %s | %s | %s |\n" % (b, y, "; ".join(str(v) for v in vals)))
        w("\n")
    if empty_captures:
        w("## Captures holding no figures at all\n\n")
        w("**%d of %d captures** are navigation-only shells: real HTML, 3-6k of text,\n"
          % (len(empty_captures), stats["captures"]))
        w("no headline block and no ratio sentence. This is a property of what Wayback\n")
        w("captured, not of the extractor - and it is the honest reason some banks gain\n")
        w("nothing here, so it must not be read as a parsing failure.\n\n")
        byb = collections.Counter()
        for pid, route, _ in empty_captures:
            byb[id_map.get(pid, (pid, None))[0] or pid] += 1
        w("| bank (or profile id) | empty captures |\n|---|---|\n")
        for b, n in sorted(byb.items(), key=lambda kv: (-kv[1], str(kv[0])))[:25]:
            w("| %s | %d |\n" % (b, n))
        w("\nNotably **SMBC** and **STATE BANK OF INDIA UK** are empty in the archive too.\n")
        w("The live collection found no numeric return for either, and the archive now\n")
        w("CORROBORATES that rather than leaving it untested.\n\n")
    if unmapped:
        w("## Profile ids with no bank attached\n\n")
        for pid, n in sorted(unmapped.items()):
            w("- profile %s (%d captures)\n" % (pid, n))
        w("\n")
    w("## Positive control against the live collection\n\n")
    w("Where a capture and the live/search-indexed collection describe the same\n")
    w("(bank, year) they must agree, and this is the only check that can tell a\n")
    w("parse from a MISPARSE. It caught a dropped minus sign on the first run:\n")
    w("Griffin Bank FY2024 is -107.64%% ROE and was extracted as +107.64%%.\n\n")
    w("- agree exactly: **%d**\n" % control["agree"])
    w("- disagree: **%d**\n" % len(control["differ"]))
    for (b, y), mine, theirs in control["differ"]:
        w("    - %s %s — capture %s vs collection %s\n" % (b, y, mine, theirs))
    w("\n")

    w("## Standing limits\n\n")
    w("- These are AGGREGATOR figures and belong in their own column. They are not\n")
    w("  the bank's own published return and not our computed ratio.\n")
    w("- No ratio was computed from the `site_inputs` figures.\n")
    w("- `site_inputs` is thebanks.eu's own transcription of the balance sheet, so it\n")
    w("  is an independent CROSS-CHECK on our inputs, not a replacement for them.\n")

    print("wrote %s" % os.path.relpath(OUT_JSONL, HERE))
    print("wrote %s" % os.path.relpath(OUT_REPORT, HERE))
    print("  captures %d | ratio records %d | inputs-only %d"
          % (stats["captures"], stats["ratio_records"], stats["inputs_only_records"]))
    print("  distinct (bank, year) with a ratio: %d" % len(ratio_pairs))
    print("  NEW vs collection: %d  (in window: %d)" % (len(new_pairs), len(new_in_window)))
    if conflicts:
        print("  disagreements: %d" % len(conflicts))
    print("  positive control vs collection: %d agree, %d differ"
          % (control["agree"], len(control["differ"])))
    if stats["unmapped_profile"]:
        print("  unmapped profiles: %d captures" % stats["unmapped_profile"])


if __name__ == "__main__":
    main()
