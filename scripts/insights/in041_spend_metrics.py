"""Derived spend metrics for IN-041.

Reads `research/insights.db` directly and emits a JSON payload covering the
two "spend" readings chartered for IN-041: cost base (how expensive a bank
is to run) and capital deployment (where it puts its money). Writes no new
database tables - this is an analysis module in the existing `in0NN_*.py`
family, not a pipeline step. Output is computed now but NOT visualized this
round (see IN-047, deferred) - this module produces the JSON payload only.

Kept as two genuinely distinct metric families per this round's grilling
decision - merging cost base and capital deployment into one number would
blur two different questions ("how expensive is this bank to run" vs.
"where does it put its money").

Row-label prefixes from IN-039's section-disambiguation fix (e.g. "Assets -
Loans and advances to customers", "Operating expenses - Personnel expenses")
mean every selector here matches against the full prefixed label, never a
bare metric name.
"""

import argparse
import os
import re
from collections import defaultdict

from in012_absolute_analysis import classify_amount_unit, write_json_atomic
from statement_row_selection import bare_label, in_assets_section, select_labeled_rows

# Absolute P&L figures (personnel/other-opex/total-opex/revenue) are reported
# in whatever unit each bank's own filing uses - £'000 for most, £m for some
# (e.g. Barclays Bank UK) - and select_labeled_rows returns raw
# value_numeric with no unit normalization. Left unscaled, a cross-bank
# comparison silently mixes thousands and millions. Scale every absolute
# figure to actual GBP at the point it's read; ratios (cost_to_income_pct
# etc.) are unaffected since both sides of the ratio get the same treatment.
_UNIT_MULTIPLIER = {"GBP_thousand": 1_000, "GBP_million": 1_000_000, "GBP_unit": 1}


def _scaled_value(item):
    """Absolute £-displayed figure, scaled to true GBP - or None when the
    source unit isn't a recognized GBP variant (e.g. Standard Chartered
    Bank's Profit & Loss is $m). Defaulting an unrecognized/foreign unit to
    a 1x GBP multiplier would silently mislabel a dollar figure as pounds -
    a currency-mismatch bug, not just a missing scale factor - so this
    excludes rather than guesses, consistent with the project's "leave a
    year blank over guessing at it" convention."""
    mult = _UNIT_MULTIPLIER.get(classify_amount_unit(item.get("unit", "")))
    return None if mult is None else float(item["value_numeric"]) * mult


def _ratio_value(item):
    """Raw value for a ratio's numerator/denominator (e.g. cost / revenue) -
    unit-invariant since both sides of the same bank's Profit & Loss share
    one reporting currency and scale, so no unit lookup is needed here even
    when that unit isn't GBP."""
    return float(item["value_numeric"])


_PERSONNEL_RE = re.compile(r"personnel|staff costs", re.I)
_OTHER_OPEX_RE = re.compile(r"other operating expense", re.I)
_TOTAL_OPEX_RE = re.compile(r"total operating expense", re.I)
_TOTAL_OPEX_EXCLUDE_RE = re.compile(r"before ", re.I)
_OF_WHICH_RE = re.compile(r"of which", re.I)

_REVENUE_RE = re.compile(r"total operating income|total income|net operating income|operating income$", re.I)
_REVENUE_EXACT = {"total operating income", "total income"}
# "operating income$" is deliberately loose (94 label variants, no single
# canonical revenue line) but it must not fall through to "Other operating
# income" - a residual income line, not total revenue - when a bank's
# preferred total/net line is missing for a given year (seen for Monzo's
# FY2025 filing: "Net operating income" is null that year, so without this
# exclusion the selector picked "Other operating income" alone as revenue,
# producing a 1544% cost-to-income ratio).
_REVENUE_EXCLUDE_RE = re.compile(r"of which|from banking activities|other operating income", re.I)

_LOANS_RE = re.compile(r"loans (and advances )?to customers", re.I)
_TREASURY_RE = re.compile(r"treasury|investment securities|debt securities|financial investments|investment in debt securities", re.I)
_TREASURY_EXCLUDE_RE = re.compile(r"of which|revaluation reserve|fair value reserve|in issue", re.I)
# "cash and" doesn't cover every real phrasing - Cater Allen's own Balance
# Sheet row is "Cash, and other balances at central banks" (a comma plus
# "other" between "Cash" and "balances"), which the tighter pattern missed
# entirely, silently dropping its cash figure (found via a 2026-09-04 user
# report that Cater Allen's capital-deployment chart was missing).
_CASH_RE = re.compile(r"cash,?\s+and\s+(other\s+)?(cash equivalents|balances)", re.I)
_CASH_EXCLUDE_RE = re.compile(r"of which|restricted", re.I)
_TOTAL_ASSETS_RE = re.compile(r"total assets$", re.I)


def _revenue_rank(label):
    return 0 if bare_label(label).lower() in _REVENUE_EXACT else 1


def cost_base(observations):
    """Profit & Loss: Personnel expense, Other operating expense, Total
    operating expense, and each as a % of revenue (a cost-to-income style
    view). Revenue is selected via a priority list (94 loose label variants
    exist; "Total operating income"/"Total income" preferred over "Net
    operating income" or narrower "operating income" lines) since P&L has
    no single canonical revenue label across all 145 banks."""
    personnel, _ = select_labeled_rows(observations, "Profit & Loss", _PERSONNEL_RE, _OF_WHICH_RE)
    other_opex, _ = select_labeled_rows(observations, "Profit & Loss", _OTHER_OPEX_RE, _OF_WHICH_RE)
    total_opex, opex_ambiguous = select_labeled_rows(observations, "Profit & Loss", _TOTAL_OPEX_RE, _TOTAL_OPEX_EXCLUDE_RE)
    revenue, revenue_ambiguous = select_labeled_rows(observations, "Profit & Loss", _REVENUE_RE, _REVENUE_EXCLUDE_RE, rank=_revenue_rank)

    def series(rows):
        out = defaultdict(dict)
        for (frn, year), item in rows.items():
            out[frn][year] = _scaled_value(item)
        return dict(out)

    def pct_of_revenue(rows):
        out = defaultdict(dict)
        for key, item in rows.items():
            rev = revenue.get(key)
            if rev is None:
                continue
            rev_value = _ratio_value(rev)
            if rev_value == 0:
                continue
            frn, year = key
            out[frn][year] = round(abs(_ratio_value(item)) / abs(rev_value) * 100, 2)
        return dict(out)

    return {
        "personnel_expense": series(personnel),
        "other_operating_expense": series(other_opex),
        "total_operating_expense": series(total_opex),
        "revenue": series(revenue),
        "personnel_expense_pct_of_revenue": pct_of_revenue(personnel),
        "other_operating_expense_pct_of_revenue": pct_of_revenue(other_opex),
        "cost_to_income_pct": pct_of_revenue(total_opex),
        "coverage": {
            "banks_with_personnel": len({f for f, _ in personnel}),
            "banks_with_other_opex": len({f for f, _ in other_opex}),
            "banks_with_total_opex": len({f for f, _ in total_opex}),
            "banks_with_revenue": len({f for f, _ in revenue}),
            "ambiguous_total_opex_bank_years_skipped": opex_ambiguous,
            "ambiguous_revenue_bank_years_skipped": revenue_ambiguous,
        },
    }


def capital_deployment(observations):
    """Balance Sheet: loans / treasury investments / cash and equivalents
    each as a % of Total assets - "where does this bank put its money".
    Each category is selected as a single best-matching Assets-section row
    per bank-year (not summed across sub-splits), to avoid double-counting
    a parent total alongside its own components under a different label -
    a real risk given e.g. Treasury has 47 distinct label variants across
    banks. This is a deliberate accuracy-over-completeness tradeoff: some
    banks that split treasury across multiple sibling lines with no single
    total row will show reduced coverage rather than a risked double-count;
    coverage is reported honestly below, not padded."""
    loans, _ = select_labeled_rows(observations, "Balance Sheet", _LOANS_RE, _OF_WHICH_RE, extra_filter=in_assets_section)
    treasury, _ = select_labeled_rows(observations, "Balance Sheet", _TREASURY_RE, _TREASURY_EXCLUDE_RE, extra_filter=in_assets_section)
    cash, _ = select_labeled_rows(observations, "Balance Sheet", _CASH_RE, _CASH_EXCLUDE_RE, extra_filter=in_assets_section)
    total_assets, _ = select_labeled_rows(observations, "Balance Sheet", _TOTAL_ASSETS_RE)

    def pct_of_assets(rows):
        out = defaultdict(dict)
        for key, item in rows.items():
            assets = total_assets.get(key)
            if assets is None or float(assets["value_numeric"]) == 0:
                continue
            frn, year = key
            out[frn][year] = round(float(item["value_numeric"]) / float(assets["value_numeric"]) * 100, 2)
        return dict(out)

    loans_pct = pct_of_assets(loans)
    treasury_pct = pct_of_assets(treasury)
    cash_pct = pct_of_assets(cash)

    return {
        "loans_pct_of_assets": loans_pct,
        "treasury_investments_pct_of_assets": treasury_pct,
        "cash_pct_of_assets": cash_pct,
        "coverage": {
            "banks_with_loans": len(loans_pct),
            "banks_with_treasury": len(treasury_pct),
            "banks_with_cash": len(cash_pct),
            "banks_with_all_three": len(set(loans_pct) & set(treasury_pct) & set(cash_pct)),
            "bank_years_with_total_assets": len(total_assets),
        },
    }


def build_in041_payload(db_path):
    from analysis_queries import AnalysisQueries
    observations = AnalysisQueries(db_path).observations()
    banks = {item["frn"]: item.get("bank", item.get("canonical_bank", "")) for item in observations}
    return {
        "metadata": {"source": os.path.abspath(db_path), "banks": banks},
        "cost_base": cost_base(observations),
        "capital_deployment": capital_deployment(observations),
    }


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(root, "research", "insights.db"))
    parser.add_argument("--out", default=os.path.join(root, "research", "in041_spend_metrics.json"))
    args = parser.parse_args()
    write_json_atomic(build_in041_payload(args.db), args.out)
    print(f"Wrote IN-041 spend-metrics payload to {args.out}")


if __name__ == "__main__":
    main()
