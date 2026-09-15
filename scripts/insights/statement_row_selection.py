"""Shared row-selection helpers for the new ST- statement sheets (Balance
Sheet, Profit & Loss, Asset Quality, RWA Breakdown), used by both
`in040_risk_metrics.py` and `in041_spend_metrics.py`.

Row-label prefixes from IN-039's section-disambiguation fix (e.g. "Assets -
Derivative financial instruments", "Credit risk - Of which: standardised
approach") mean every selector here matches against the full prefixed label,
never a bare metric name.
"""

import re
from collections import defaultdict


def bare_label(label):
    """Strip an IN-039 section/parent prefix, returning the row's own text -
    from the LAST " - " in the label, so it CAN eat into the row's own text
    when that text itself contains " - " (e.g. a derived-row comment like
    "Total operating income (sum of the three income lines above - not
    itself a printed subtotal)" reduces to just "not itself a printed
    subtotal)"). Kept for its original purpose - the shortest-label tie-break
    in select_labeled_rows below now uses own_label() instead, which doesn't
    have this problem - but still used by callers that only need SOME
    stable stand-in for "the row's own text" and aren't sensitive to which
    end gets stripped when a label has multiple " - " segments."""
    if " - " in (label or ""):
        return label.rsplit(" - ", 1)[-1].strip()
    return (label or "").strip()


def own_label(label):
    """Strip only the SECTION prefix IN-039 adds - the part before the FIRST
    " - " - keeping the row's own text intact even when that text itself
    contains " - " (unlike bare_label above, which strips from the LAST
    " - " and so can chop into the row's own text).

    This is the label select_labeled_rows actually matches `include_re`
    against by default (see `require_own_match`) - found necessary via
    Punjab National Bank International, whose P&L places "Profit/(loss)
    before tax" inside a SECTION literally named "Operating expenses"
    (alongside the real "Total operating expenses" TOTAL row): the full
    label "Operating expenses - Profit/(loss) before tax" matched an opex
    regex purely because of the section-name prefix, entered the candidate
    pool, and won the tie-break over the genuine opex row (both bare labels
    came out the same length, and alphabetically "Profit..." sorts before
    "Total..."). The same class of bug independently reappeared in
    in040_risk_metrics.py's income_volatility(): a DATA row explicitly
    documented as "leave blank, different consolidation basis" for
    Co-operative Bank's FY1972-1980 was still selected as that bank's
    profit-for-the-year figure because it happened to contain the phrase
    "Profit for the year" within a longer sentence, and no TOTAL-only
    filter was applied there to exclude it."""
    return label.split(" - ", 1)[-1] if " - " in (label or "") else (label or "")


def in_assets_section(label):
    """True when a Balance Sheet row's own section prefix names it an asset
    (not a liability or equity row) - lets a caller restrict a loose keyword
    match (e.g. "debt securities") to the Assets side of the sheet without
    also picking up "Liabilities - Debt securities in issue"."""
    section = label.split(" - ", 1)[0] if " - " in (label or "") else (label or "")
    return bool(re.search(r"assets", section, re.I)) and not re.search(r"liabilit|equity", section, re.I)


def in_liabilities_section(label):
    """True when a Balance Sheet row's own section prefix names it a
    liability - the liabilities-side counterpart to in_assets_section
    above. Needed once a deposit-matching regex is loosened to a wildcard
    (e.g. "deposits?.*customers?" to also catch "Deposits at amortised
    cost from customers" phrasing) - a wildcard match is no longer
    anchored to one specific phrase order, so it can otherwise cross onto
    an asset-side row that happens to share the same words in a different
    sense (e.g. "Deposits with banks" as an ASSET - money the bank itself
    placed with other banks - vs "Deposits from banks" as a LIABILITY)."""
    section = label.split(" - ", 1)[0] if " - " in (label or "") else (label or "")
    return bool(re.search(r"liabilit", section, re.I)) and not re.search(r"assets|equity", section, re.I)


def in_equity_section(label):
    """True when a Balance Sheet row's own section prefix names it an
    equity row - the equity-side counterpart to in_assets_section above."""
    section = label.split(" - ", 1)[0] if " - " in (label or "") else (label or "")
    return bool(re.search(r"equity", section, re.I)) and not re.search(r"assets|liabilit", section, re.I)


def select_labeled_rows(observations, sheet, include_re, exclude_re=None, rank=None, extra_filter=None,
                         require_kind=None, require_own_match=True):
    """Select one row per (frn, fiscal_year) whose label matches `include_re`
    (and not `exclude_re`), among annual, numeric-or-disclosed observations.

    `rank` is an optional `label -> int` function (lower wins); ties fall
    back to the shortest own_label() (see below), then alphabetical, for
    determinism.
    `extra_filter` is an optional `label -> bool` predicate (e.g.
    `in_assets_section`) applied alongside the regexes.
    `require_kind` (added 2026-09-07) restricts candidates to a specific
    `row_kind` ("TOTAL" or "DATA", from extract_metrics.py's own bold-column-A
    read of the source workbook) - use it whenever the SAME bare label is
    genuinely a TOTAL row for some banks and a DATA sub-component for others
    (confirmed true of "Operating expenses"/"Administrative expenses" - a
    plain label-text regex can't tell those apart, and picking the wrong one
    silently understates a derived ratio rather than erroring).
    `require_own_match` (added 2026-09-07, default True) requires
    `include_re` to also match `own_label(label)` - the row's own text with
    only its IN-039 SECTION prefix stripped, not the full prefixed label.
    Without this, a row can enter the candidate pool purely because its
    SECTION happens to share wording with `include_re` (e.g. any row inside
    a section literally named "Operating expenses" matches an opex regex
    even if that row is "Profit before tax"), which silently corrupts
    ratios derived from the wrong row - found independently in both
    in041_spend_metrics.py's cost_base() and in040_risk_metrics.py's
    income_volatility(). Every current caller wants this protection, so it
    defaults on; set False only for a caller that has verified it genuinely
    needs a match to succeed via section-prefix context alone (no known
    case does, as of 2026-09-07 - the one case that looked like it needed
    this, UBP's "Other operating income - Total operating income", turned
    out to match on its own text "Total operating income" regardless).
    Returns (selected: {(frn, year): observation}, ambiguous_count: int).
    """
    candidates = defaultdict(list)
    for item in observations:
        if item.get("sheet") != sheet or not item.get("annual_eligible"):
            continue
        if item.get("value_status") not in ("numeric", "special_numeric"):
            continue
        if require_kind is not None and item.get("row_kind") != require_kind:
            continue
        label = item.get("row_label", "")
        if not include_re.search(label):
            continue
        if require_own_match and not include_re.search(own_label(label)):
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
            return (r, len(own_label(item["row_label"])), item["row_label"])
        rows_sorted = sorted(rows, key=sort_key)
        best = rows_sorted[0]
        if len(rows_sorted) > 1 and sort_key(rows_sorted[1])[:2] == sort_key(best)[:2]:
            ambiguous += 1
        selected[key] = best
    return selected, ambiguous
