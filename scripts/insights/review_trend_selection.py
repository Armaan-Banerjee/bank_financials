"""Create the IN-004 exception report for manual row/basis review.

Reads research/insights.db by default (the source of truth); `--csv` is an
explicit fallback for reading a specific flat-file export instead - see
scripts/analyze_trends.py's module docstring for why this is a separate,
explicit flag rather than a silent default.
"""

import argparse
import csv
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from analyze_trends import METRICS, year
import build_insights_db

DEFAULT_DB = os.path.join(os.path.dirname(__file__), "..", "..", "research", "insights.db")
DEFAULT_OUTPUT = os.path.join(os.path.dirname(__file__), "..", "..", "research", "in004_selection_review.md")


def load_rows(path="research/bank_metrics.csv"):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def collision_rows(rows, metric, spec):
    sheet, pattern, excluded = spec
    found = defaultdict(list)
    for row in rows:
        if row["sheet"] != sheet or row["is_numeric"] != "1":
            continue
        if not pattern.search(row["row_label"]):
            continue
        if any(word in row["row_label"].lower() for word in excluded):
            continue
        fiscal_year = year(row["year"])
        if fiscal_year is not None:
            found[(row["frn"], fiscal_year)].append(row)
    return {key: values for key, values in found.items() if len({(r["row_label"], r["year"]) for r in values}) > 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=DEFAULT_DB, help="SQLite database to read metrics from")
    parser.add_argument("--csv", default=None,
                        help="explicit fallback: read metrics from this CSV instead of --db")
    parser.add_argument("--out", default=DEFAULT_OUTPUT, help="output markdown path")
    args = parser.parse_args()

    if args.csv:
        rows = load_rows(args.csv)
        source_note = f"`{os.path.relpath(args.csv)}` (explicit CSV fallback)"
        print(f"Metrics source: CSV fallback ({args.csv})")
    else:
        from analysis_queries import AnalysisQueries
        rows = AnalysisQueries(args.db).observations()
        source_note = f"`{os.path.relpath(args.db)}` (source of truth)"
        print(f"Metrics source: database ({args.db})")

    lines = [
        "# IN-004 trend-selection exception review",
        "",
        "This report lists same-FRN/same-fiscal-year rows where more than one",
        "label or period variant was available. It is the manual-review queue",
        "for deciding whether the current explicit priorities are appropriate.",
        f"Rows are from {source_note}; no workbook was read or changed.",
        "",
    ]
    total = 0
    for metric in ("Leverage ratio", "Operating cash flow"):
        collisions = collision_rows(rows, metric, METRICS[metric])
        total += len(collisions)
        lines.extend([f"## {metric} ({len(collisions)} FRN-year collisions)", ""])
        if not collisions:
            lines.append("None.")
            lines.append("")
            continue
        lines.extend(["| FRN | Bank | Year | Candidate label | Value | Basis note |", "|---:|---|---:|---|---:|---|"])
        for (frn, fiscal_year), candidates in sorted(collisions.items(), key=lambda item: (item[0][0], item[0][1])):
            for row in sorted(candidates, key=lambda item: (item["row_label"].lower(), item["year"])):
                note = (row["basis_note"] or "").replace("|", "\\|").replace("\n", " ")
                label = row["row_label"].replace("|", "\\|")
                lines.append(f"| {frn} | {row['bank']} | {fiscal_year} | {label} | {row['value_numeric']} | {note} |")
        lines.append("")
    lines.extend([
        "## How to review",
        "",
        "For each FRN-year, confirm whether the unqualified `FY####` row is the",
        "intended annual series. If not, note the preferred label and reporting",
        "basis. Pay particular attention to central-bank-claims variants in",
        "leverage and group-versus-bank or restatement variants in cash flow.",
        "The aggregate trend counts should not be treated as final for affected",
        "metrics until material exceptions are resolved.",
        "",
        f"Total exception groups: {total}.",
    ])
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print(f"Wrote {args.out}: {total} exception groups")


if __name__ == "__main__":
    main()
