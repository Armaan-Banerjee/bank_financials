"""Shared row-selection helpers for the new ST- statement sheets (Balance
Sheet, Profit & Loss, Asset Quality, RWA Breakdown), used by both
`in040_risk_metrics.py` and `in041_spend_metrics.py`.

Row-label prefixes from IN-039's section-disambiguation fix (e.g. "Assets -
Derivative financial instruments", "Credit risk - Of which: standardised
approach") mean every selector here matches against the full prefixed label,
never a bare metric name.
"""

from collections import defaultdict


def bare_label(label):
    """Strip an IN-039 section/parent prefix, returning the row's own text."""
    if " - " in (label or ""):
        return label.rsplit(" - ", 1)[-1].strip()
    return (label or "").strip()


def in_assets_section(label):
    """True when a Balance Sheet row's own section prefix names it an asset
    (not a liability or equity row) - lets a caller restrict a loose keyword
    match (e.g. "debt securities") to the Assets side of the sheet without
    also picking up "Liabilities - Debt securities in issue"."""
    section = label.split(" - ", 1)[0] if " - " in (label or "") else (label or "")
    import re
    return bool(re.search(r"assets", section, re.I)) and not re.search(r"liabilit|equity", section, re.I)


def select_labeled_rows(observations, sheet, include_re, exclude_re=None, rank=None, extra_filter=None):
    """Select one row per (frn, fiscal_year) whose label matches `include_re`
    (and not `exclude_re`), among annual, numeric-or-disclosed observations.

    `rank` is an optional `label -> int` function (lower wins); ties fall
    back to the shortest bare label, then alphabetical, for determinism.
    `extra_filter` is an optional `label -> bool` predicate (e.g.
    `in_assets_section`) applied alongside the regexes.
    Returns (selected: {(frn, year): observation}, ambiguous_count: int).
    """
    candidates = defaultdict(list)
    for item in observations:
        if item.get("sheet") != sheet or not item.get("annual_eligible"):
            continue
        if item.get("value_status") not in ("numeric", "special_numeric"):
            continue
        label = item.get("row_label", "")
        if not include_re.search(label):
            continue
        if exclude_re is not None and exclude_re.search(label):
            continue
        if extra_filter is not None and not extra_filter(label):
            continue
        candidates[(item["frn"], item["fiscal_year"])].append(item)

    selected = {}
    ambiguous = 0
    for key, rows in candidates.items():
        def sort_key(item):
            r = rank(item["row_label"]) if rank else 0
            return (r, len(bare_label(item["row_label"])), item["row_label"])
        rows_sorted = sorted(rows, key=sort_key)
        best = rows_sorted[0]
        if len(rows_sorted) > 1 and sort_key(rows_sorted[1])[:2] == sort_key(best)[:2]:
            ambiguous += 1
        selected[key] = best
    return selected, ambiguous
