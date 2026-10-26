#!/usr/bin/env python3
"""Merge sweep batch records into the curated published-returns store.

Run with /usr/bin/python3 (the interpreter that has openpyxl in this repo).

    /usr/bin/python3 research/profitability/merge_sweep.py            # dry run
    /usr/bin/python3 research/profitability/merge_sweep.py --apply    # write

WHY THIS FILE EXISTS. The 2026-10-11 merge of batches 1-3 was done by hand.
Two things went wrong that a tool prevents. The batch files kept being
corrected AFTER that merge - the 12-13 October retry rounds resolved Metro
Bank's RoTE series, Turkish Bank UK's five ROE years and five
`publishes_none` findings - and because the merge was a one-off action rather
than a repeatable one, those corrections never reached the store: 7 banks
from batches 1-3 sat outside it for two days. And the "evidence filter" that
merge applied lived only in whoever ran it, so `sweep/README.md` could only
tell the next session to "apply the same evidence filter" without being able
to say what it was. The filter is now code, below, and the merge is
idempotent, so re-running after any batch correction is always safe and is
the normal way to pick corrections up.

THE FILTER, and the reasoning each rule carries:

1. `ocr_lead` records are QUARANTINED, never merged. An ocr_lead is a lead,
   not a finding: it was read off a text layer or a low-resolution contact
   sheet, and this project's verification standard is a 300 dpi render that
   a human (or model) actually looked at. 40 such records exist across
   batches 4 and 7 (Arab Bank Europe alone holds 34). Merging them would
   silently reopen the OCR backlog that was deliberately cleared on
   2026-10-10, and the store's own `_schema` line promises every record in
   it is 300dpi, press_release or explicitly flagged. A quarantined record
   is reported by this script on every run so it stays visible.

2. De-duplication is on (bank, year, measure), the store's natural key - one
   record per thing a bank publishes for a period. A `publishes_none` record
   has measure null, so the same key covers it without a special case.
   EXISTING RECORDS WIN. A record already in the store has been through
   curation; a batch record has not, so this script never overwrites or
   edits, it only appends what is absent. That also means a genuine
   correction to an already-merged record is deliberately NOT applied here -
   editing a curated record is a hand decision, and this script prints those
   collisions rather than acting on them.

3. The `_schema` header line stays line 1.

This script only ever appends to `published_returns.jsonl`. It does not
touch any bank workbook, build script, extract or deliverable - rebuilding
those is a separate, explicit step (see README.md).
"""

import argparse
import collections
import glob
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(HERE, "published_returns.jsonl")
BATCHES = os.path.join(HERE, "sweep", "batch_*.jsonl")

# Verification states a record must carry to be eligible for the store.
# Deliberately a whitelist: a new, unrecognised state must be considered
# rather than inherited silently.
MERGEABLE_VERIFICATION = {"300dpi", "press_release"}
QUARANTINE_VERIFICATION = {"ocr_lead"}


def read_jsonl(path):
    """Return (schema_line_or_None, [records]). Blank lines are skipped."""
    schema = None
    records = []
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except ValueError as exc:
                sys.exit("%s line %d is not valid JSON: %s" % (path, lineno, exc))
            # The store's first line is a schema note, not a record.
            if "_schema" in rec and "bank" not in rec:
                schema = line
                continue
            if "bank" not in rec:
                sys.exit("%s line %d has no 'bank' field" % (path, lineno))
            records.append(rec)
    return schema, records


def key_of(rec):
    return (rec.get("bank"), rec.get("year"), rec.get("measure"))


def kind_of(rec):
    for flag in ("publishes_none", "excluded", "unresolved"):
        if rec.get(flag):
            return flag
    return "figure"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true",
                    help="write the merge (default is a dry run that changes nothing)")
    args = ap.parse_args()

    schema, store = read_jsonl(STORE)
    store_keys = {key_of(r) for r in store}

    added = []
    quarantined = []
    collisions = []
    unknown_verification = []
    per_batch = collections.OrderedDict()

    for path in sorted(glob.glob(BATCHES)):
        name = os.path.basename(path)
        _, records = read_jsonl(path)
        stats = collections.Counter()
        for rec in records:
            verification = rec.get("verification")
            if verification in QUARANTINE_VERIFICATION:
                quarantined.append((name, rec))
                stats["quarantined"] += 1
                continue
            if verification not in MERGEABLE_VERIFICATION:
                unknown_verification.append((name, rec))
                stats["unknown_verification"] += 1
                continue
            key = key_of(rec)
            if key in store_keys:
                collisions.append((name, rec))
                stats["already_in_store"] += 1
                continue
            rec = dict(rec)
            rec["merged_from"] = name
            added.append(rec)
            store_keys.add(key)
            stats["added"] += 1
        per_batch[name] = (len(records), stats)

    print("STORE before : %d records, %d banks"
          % (len(store), len({r.get("bank") for r in store})))
    print()
    print("%-18s %7s %7s %7s %12s" % ("batch", "records", "added", "dup", "quarantined"))
    for name, (total, stats) in per_batch.items():
        print("%-18s %7d %7d %7d %12d"
              % (name, total, stats["added"], stats["already_in_store"],
                 stats["quarantined"]))
    print()

    if quarantined:
        banks = sorted({r.get("bank") for _, r in quarantined})
        print("QUARANTINED (ocr_lead - a lead, NOT a finding, never merged): "
              "%d records across %d banks" % (len(quarantined), len(banks)))
        for bank in banks:
            n = sum(1 for _, r in quarantined if r.get("bank") == bank)
            print("   %-32s %d" % (bank, n))
        print("   To promote any of these, render the cited page at 300 dpi, read it,")
        print("   and set verification to 300dpi in the batch file. Never edit the")
        print("   state without doing the render.")
        print()

    if unknown_verification:
        print("REFUSED - unrecognised verification state (neither mergeable nor a known")
        print("quarantine state), so NOT merged; decide explicitly what each one is:")
        for name, rec in unknown_verification:
            print("   %s  %s %s  verification=%r"
                  % (name, rec.get("bank"), rec.get("year"), rec.get("verification")))
        print()

    if collisions:
        print("Already in store on (bank, year, measure): %d records. The store's copy"
              % len(collisions))
        print("wins and nothing was changed. A batch correction to an already-merged")
        print("record is a HAND decision - this script will not overwrite curation.")
        print()

    kinds = collections.Counter(kind_of(r) for r in added)
    print("TO ADD: %d records across %d banks  %s"
          % (len(added), len({r.get("bank") for r in added}), dict(kinds)))
    print("STORE after : %d records, %d banks"
          % (len(store) + len(added),
             len({r.get("bank") for r in store} | {r.get("bank") for r in added})))

    if not added:
        print()
        print("Nothing to add - the store is already current with the batch files.")
        return

    if not args.apply:
        print()
        print("DRY RUN - nothing written. Re-run with --apply to write.")
        return

    backup = STORE + ".bak"
    shutil.copy2(STORE, backup)
    with open(STORE, "a", encoding="utf-8") as fh:
        for rec in added:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print()
    print("WROTE %d records to %s" % (len(added), os.path.relpath(STORE)))
    print("Backup of the previous store: %s" % os.path.relpath(backup))
    print("The deliverable is NOT rebuilt by this script - see README.md.")


if __name__ == "__main__":
    main()
