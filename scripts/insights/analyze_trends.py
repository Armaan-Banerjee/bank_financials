"""Reproducible, auditable IN-004 trend and parent-group checks.

Reads research/insights.db (the source of truth, per IN-008/CODING_STANDARDS.md)
by default. `--csv`/`--markdown` are explicit fallbacks for when you
specifically want the flat-file view (e.g. comparing against an older
export) - each is independent, so metrics and parent-group data are never
silently mixed from two different sources in one run; main() prints which
source it used for each half. NumPy is intentionally not needed: this is a
descriptive screening tool. It reports selection ambiguities and basis-note
coverage so narrative conclusions are not silently based on arbitrary
duplicate rows.
"""

import argparse
import csv
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
import build_insights_db
from in009_analysis import _is_percent_value, PERCENT_ONLY_SHEETS

DEFAULT_DB = os.path.join(os.path.dirname(__file__), "..", "..", "research", "insights.db")


METRICS = {
    "CET1 ratio": ("CET1 Ratio", re.compile(r"ratio", re.I), ("capital adequacy",)),
    "Total capital ratio": ("Total Capital Ratio", re.compile(r"ratio", re.I), ("capital adequacy",)),
    "Leverage ratio": ("Leverage Ratio", re.compile(r"leverage ratio", re.I), ("exposure", "measure")),
    "LCR": ("LCR", re.compile(r"liquidity.*ratio|^LCR$", re.I), ("outflow", "inflow")),
    "NSFR": ("NSFR", re.compile(r"NSFR|stable funding ratio", re.I), ("available stable", "required stable")),
    "Operating cash flow": (
        "Cash Flow Statement",
        re.compile(r"operating activities", re.I),
        (
            "investing", "financing", "before changes", "before taxation",
            "before payment", "adjustments", "assets relating", "liabilities relating",
        ),
    ),
}
YEAR_RE = re.compile(r"(20\d{2})")

# Prefer conventional headline labels when several valid labels have equal
# coverage. Remaining ties are surfaced by extract() instead of hidden.
LABEL_PRIORITY = {
    "CET1 ratio": ("common equity tier 1 (cet1) ratio", "cet1 ratio"),
    "Total capital ratio": ("total capital ratio", "total capital adequacy ratio"),
    "Leverage ratio": (
        "leverage ratio excluding claims on central banks (%)",
        "leverage ratio excluding claims on central banks",
        "leverage ratio excluding central banks",
        "leverage ratio (%)",
        "leverage ratio",
    ),
    "LCR": ("liquidity coverage ratio (%)", "liquidity coverage ratio", "lcr"),
    "NSFR": ("net stable funding ratio (%)", "net stable funding ratio", "nsfr"),
    "Operating cash flow": (
        "net cash from/(used in) operating activities",
        "net cash generated from/(used in) operating activities",
        "net cash used in operating activities",
        "net cash flow from operating activities",
        "net cashflow from/(used in) operating activities",
    ),
}


def year(value):
    match = YEAR_RE.search(value or "")
    return int(match.group(1)) if match else None


def load_rows(path="research/bank_metrics.csv"):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _period_priority(period):
    """Prefer an unqualified FY label over footnote/perimeter variants."""
    return 0 if re.fullmatch(r"FY20\d{2}", period or "") else 1


def _label_priority(metric, label):
    label = label.lower()
    for index, preferred in enumerate(LABEL_PRIORITY.get(metric, ())):
        if label == preferred:
            return index
    return len(LABEL_PRIORITY.get(metric, ()))


def extract(rows, metric, spec):
    """Return FRN -> year -> value plus diagnostics for selection decisions."""
    sheet, pattern, excluded = spec
    candidates = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    all_periods = defaultdict(lambda: defaultdict(set))
    basis = defaultdict(set)
    for row in rows:
        if row["sheet"] != sheet or row["is_numeric"] != "1":
            continue
        if not pattern.search(row["row_label"]):
            continue
        if any(word in row["row_label"].lower() for word in excluded):
            continue
        # A percent-only sheet (CET1/Total Capital/Leverage Ratio, LCR, NSFR)
        # also carries supporting absolute £m/£bn rows (exposure measures,
        # eligible-instrument amounts) whose labels can still match `pattern`
        # and evade `excluded` under unanticipated real-world phrasing (e.g.
        # "NSFR eligible liabilities (£m)" matches the NSFR pattern and isn't
        # in `excluded`). This is the same percent-vs-absolute row-selection
        # bug already found and fixed three times in in009_analysis.py/
        # in016_distribution.py - guard it here too rather than relying on
        # the regex/excluded-list alone. Does not apply to "Operating cash
        # flow" (Cash Flow Statement), which is genuinely an absolute figure.
        if sheet in PERCENT_ONLY_SHEETS and not _is_percent_value(row):
            continue
        y = year(row["year"])
        if y is None:
            continue
        candidates[row["frn"]][row["row_label"]][y].append(row)
        all_periods[row["frn"]][y].add((row["row_label"], row["year"]))

    selected = {}
    diagnostics = {"label_ties": 0, "period_collisions": 0, "basis_variants": 0}
    diagnostics["period_collisions"] = sum(
        len(periods) > 1 for periods_by_year in all_periods.values() for periods in periods_by_year.values()
    )
    for frn, labels in candidates.items():
        ranked = sorted(
            labels.items(),
            key=lambda item: (_label_priority(metric, item[0]), -len(item[1]), item[0].lower()),
        )
        if len(ranked) > 1 and len(ranked[0][1]) == len(ranked[1][1]):
            diagnostics["label_ties"] += 1
        label, periods = ranked[0]
        values = {}
        for y, options in periods.items():
            chosen = sorted(options, key=lambda row: (_period_priority(row["year"]), row["year"]))[0]
            values[y] = float(chosen["value_numeric"])
            basis[frn].add(chosen["basis_note"] or "(no basis note)")
        selected[frn] = values
    diagnostics["basis_variants"] = sum(len(notes) > 1 for notes in basis.values())
    return selected, diagnostics


def load_groups(path="research/bank_parent_groups.md"):
    groups = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.startswith("|") or line.startswith("|---") or "Bank/legal entity" in line:
                continue
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) >= 6 and parts[1].isdigit():
                groups[parts[1]] = (parts[0], parts[3], parts[4])
    return groups


def pairwise_counts(values, left, right):
    """Pure computation, no printing - the shared building block for any
    "N of M entities declined/rose" statistic. `values` is FRN -> year ->
    number (extract()'s first return value). Reused by report_pairwise()
    below and by the HTML/PDF deliverable generators (build_in005_prototype.py,
    build_in006_pdf.py) so a headline figure is never hand-typed separately
    from what this function would compute - see CODING_STANDARDS.md."""
    changes = [series[right] - series[left] for series in values.values() if left in series and right in series]
    down = sum(change < 0 for change in changes)
    up = sum(change > 0 for change in changes)
    same = len(changes) - down - up
    return {"down": down, "up": up, "same": same, "n": len(changes)}


def report_pairwise(name, values, left, right):
    c = pairwise_counts(values, left, right)
    print(f"{name}: FY{left}->FY{right}: n={c['n']}, down={c['down']}, up={c['up']}, unchanged={c['same']}")


def report_group_agreement(group, members, extracted, left, right):
    for name in ("CET1 ratio", "Total capital ratio", "LCR", "Operating cash flow"):
        comparable = [(bank, extracted[name].get(frn, {})) for frn, bank, _ in members]
        comparable = [(bank, data) for bank, data in comparable if left in data and right in data]
        if len(comparable) < 2:
            continue
        changes = [data[right] - data[left] for _, data in comparable]
        positive = sum(value > 0 for value in changes)
        negative = sum(value < 0 for value in changes)
        agreement = max(positive, negative) / len(changes)
        direction = "+" if positive > negative else "-" if negative > positive else "mixed"
        print(f"  {name} FY{left}->{right}: {direction}, agreement={agreement:.2f}, n={len(changes)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=DEFAULT_DB,
                        help="SQLite database to read from (default source for both "
                             "metrics and parent-group data)")
    parser.add_argument("--csv", default=None,
                        help="explicit fallback: read metrics from this CSV instead of --db")
    parser.add_argument("--markdown", default=None,
                        help="explicit fallback: read parent-group data from this markdown "
                             "file instead of --db")
    args = parser.parse_args()

    if args.csv:
        rows = load_rows(args.csv)
        print(f"Metrics source: CSV fallback ({args.csv})")
    else:
        from analysis_queries import AnalysisQueries
        rows = AnalysisQueries(args.db).observations()
        print(f"Metrics source: database ({args.db})")

    if args.markdown:
        groups = load_groups(args.markdown)
        print(f"Parent-group source: markdown fallback ({args.markdown})")
    else:
        from analysis_queries import AnalysisQueries
        groups = AnalysisQueries(args.db).groups()
        print(f"Parent-group source: database ({args.db})")

    print(f"Banks in normalized dataset: {len({row['frn'] for row in rows})}")
    extracted = {}
    for name, spec in METRICS.items():
        extracted[name], diagnostics = extract(rows, name, spec)
        print(f"{name}: {len(extracted[name])} banks with numeric series; {diagnostics}")
    print("\nYear-pair checks:")
    for name in METRICS:
        for left, right in ((2021, 2022), (2022, 2023), (2023, 2024), (2024, 2025)):
            report_pairwise(name, extracted[name], left, right)

    multi = defaultdict(list)
    for frn, (bank, group, caveat) in groups.items():
        multi[group].append((frn, bank, caveat))
    print("\nMulti-entity group agreement:")
    for group, members in sorted(multi.items(), key=lambda item: (-len(item[1]), item[0])):
        if len(members) < 2:
            continue
        print(f"{group} ({len(members)}): {', '.join(bank for _, bank, _ in members)}")
        for left, right in ((2021, 2022), (2022, 2023), (2023, 2024), (2024, 2025)):
            report_group_agreement(group, members, extracted, left, right)


if __name__ == "__main__":
    main()
