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
from statement_row_selection import bare_label, in_assets_section, own_label, select_labeled_rows

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
# Broadened 2026-09-07 from a literal "total operating expense" - 67 banks
# tag their aggregate opex row TOTAL under a label that doesn't contain the
# word "total" at all ("Operating expenses", "Net operating expenses",
# "Administrative expenses", "Total expenses", "Total operating costs" -
# found via a user report that Co-operative Bank's derived cost-to-income
# was empty, which led to auditing every bank and finding 108/145 had none
# at all). Safe to broaden this far ONLY because cost_base() below now
# passes require_kind="TOTAL" - "Operating expenses"/"Administrative
# expenses" are each used as the genuine TOTAL row for some banks and as a
# DATA sub-component (one cost line among several) for others, confirmed by
# reading every build_*.py script directly; row_kind (not label text) is
# what tells them apart, since matching on text alone would silently
# understate the ratio for whichever banks use the ambiguous label as a
# sub-component.
_TOTAL_OPEX_RE = re.compile(r"operating expense|administrative expense|operating cost|total expense", re.I)
# Narrowed 2026-09-07 from a blanket r"before " (which also killed genuine
# TOTAL opex rows like UBI UK's "Operating expenses before impairment loss
# allowances" and Arab Bank Europe/HBL Bank UK/Close Brothers' "before
# amortisation/provisions" variants - all legitimate opex totals under the
# standard convention of excluding credit losses/one-off items from opex).
# What this must still catch: a REVENUE row whose descriptive text happens
# to mention "before operating/administrative expenses" (LHV's and Persia
# International Bank's "Net operating income (... BEFORE operating
# expenses ...)" rows), which would otherwise get mistaken for the opex
# total itself since the phrase "operating expense" appears in their label.
_TOTAL_OPEX_EXCLUDE_RE = re.compile(
    r"before (operating|administrative) (expense|cost)|(?:^| - )other operating expenses?$", re.I,
)
# "(?:^| - )other operating expenses?$" added 2026-09-08 (Oxbury tags its own bare
# "Other Operating Expense" row TOTAL - a genuine bolded subtotal in its own
# filing, but only of the OTHER-expense sub-items, not of opex overall: it
# sits alongside a separate "Staff Costs" DATA row, and their sum plus
# Depreciation & Amortisation is what actually nets against Total Net Income
# to Operating Profit before ECL. Because require_kind="TOTAL" trusted the
# row_kind tag alone, this bare label was picked as total_operating_expense,
# leaving personnel_expense (Staff Costs) at 133% of it and other_operating
# at 100%, i.e. double-counted against a total that was really just the
# "other" component (personnel_pct 133.03%, other_pct -133.03% on the
# profit-loss.html expense chart). Anchored so it only excludes the BARE
# label, not a genuine combined total that happens to mention the phrase
# (e.g. Streambank's "Total operating expenses (sum of Staff costs + Other
# operating expenses + Depreciation and amortisation...)" still matches).
_OF_WHICH_RE = re.compile(r"of which", re.I)

_REVENUE_RE = re.compile(
    r"total operating income|total income|net operating income|operating income$"
    r"|net revenue|net income from operations|total net income|operating income before"
    r"|net interest and fee income|total revenue|operating income/profit",
    re.I,
)
_REVENUE_EXACT = {"total operating income", "total income"}
_REVENUE_PREFERRED_PREFIXES = (
    "total operating income", "total income", "total net income", "total revenue", "operating income/profit",
)
# "operating income/profit" added 2026-09-08 (Bank Saderat's own P&L labels
# its genuine pre-expense income total this way, then separately reports a
# "Net operating income" TOTAL row further down that's already net of
# Administrative expenses and Depreciation & amortisation - confirmed
# against the bank's own build script, where the two TOTAL rows straddle
# those expense DATA rows in statement order). Without this,
# "net operating income" alone matched and was selected as revenue,
# understating it by exactly those two expense lines and producing
# >100%-of-revenue composition percentages (net_interest_pct 398.97%,
# other_pct -302.06% on the profit-loss.html income chart). Confirmed via
# grep across every build_*.py that no other bank uses this exact label, so
# widening the match/preference is safe.
# "total revenue" added 2026-09-07 (ICICI Bank UK's and Melli Bank's own
# combined-income lines are captioned "Total revenue / Net Income" and
# "Total revenue / Total net income" respectively) - confirmed via grep
# across every build_*.py that "total revenue" is never used as a DATA
# sub-component elsewhere, only as these two banks' genuine TOTAL row.
# "net revenue"/"net income from operations"/"total net income" added
# 2026-09-07 (Credit Suisse International/UK, Mizuho International, Kingdom
# Bank each label their combined-income line this way instead of any of the
# phrases above) - confirmed via grep across every build_*.py that none of
# these three phrases is ever used as a DATA sub-component elsewhere, so
# there's no ambiguity risk like the opex broadening above.
# "operating income$" is deliberately loose (94 label variants, no single
# canonical revenue line) but it must not fall through to "Other operating
# income" - a residual income line, not total revenue - when a bank's
# preferred total/net line is missing for a given year (seen for Monzo's
# FY2025 filing: "Net operating income" is null that year, so without this
# exclusion the selector picked "Other operating income" alone as revenue,
# producing a 1544% cost-to-income ratio).
# Row labels retain their statement-section prefix (for example, UBP's
# "Other operating income - Total operating income").  Reject the residual
# *line* "Other operating income", but not a valid total merely because its
# parent section happens to have that name.
_REVENUE_EXCLUDE_RE = re.compile(
    r"of which|from banking activities|(?:^| - )other operating income(?:\s*\([^)]*\))?$",
    re.I,
)

# Broadened 2026-09-08 after a bug-sweep fork found 20 real label variants
# this missed entirely: singular "Loan and advances to customers", "to
# clients" (not "customers"), "... at amortised cost to customers" (extra
# text between "advances" and "to"), and bare "Loans and advances" with no
# "to X" suffix at all. The bare-form branch excludes anything followed by
# "to " (e.g. "Loans and advances to banks"/"to related parties"/"to group
# undertakings") so it only catches genuine customer-loan totals that simply
# don't spell out "to customers".
_LOANS_RE = re.compile(
    r"loans?\s+(and\s+advances\s+)?(at\s+amortised\s+cost\s+)?to\s+(customers|clients)"
    r"|loans\s+and\s+advances(?!\s+to\b)",
    re.I,
)
_TREASURY_RE = re.compile(
    r"treasury|investment securities|investment in securities|debt securities|debt investments"
    r"|financial investments|investment in debt securities",
    re.I,
)
_TREASURY_EXCLUDE_RE = re.compile(r"of which|revaluation reserve|fair value reserve|in issue", re.I)
# "cash and" doesn't cover every real phrasing - Cater Allen's own Balance
# Sheet row is "Cash, and other balances at central banks" (a comma plus
# "other" between "Cash" and "balances"), which the tighter pattern missed
# entirely, silently dropping its cash figure (found via a 2026-09-04 user
# report that Cater Allen's capital-deployment chart was missing).
# Broadened further 2026-09-08 after a bug-sweep fork found many more real
# variants the phrase-based pattern still missed ("Cash", "Cash and cash
# equivalent" singular, "Cash at Bank", "Cash in hand", "Cash and bank
# balances", "Cash and due from banks", "Cash, notes and coins", "Cash, cash
# balances at central banks and other demand deposits") - a bare keyword
# match is safe here since this only ever runs against the Balance Sheet
# sheet's Assets section (via extra_filter=in_assets_section below) and
# already excludes "of which"/"restricted" sub-lines.
_CASH_RE = re.compile(r"\bcash\b", re.I)
_CASH_EXCLUDE_RE = re.compile(r"of which|restricted", re.I)
_TOTAL_ASSETS_RE = re.compile(r"total assets$", re.I)

# A bank's own directly-disclosed cost:income ratio (currently only
# Co-operative Bank carries this row - added 2026-09-07 after a user report
# that the derived cost_to_income_pct below was empty for all but 3 years,
# since it depends entirely on a "Total operating expense" row this bank
# only itemises FY2014-FY2016). Preferred over the opex/revenue derivation
# wherever a bank discloses it directly, since it's the bank's own
# as-reported figure rather than a reconstruction - falls back to the
# derived ratio for every other bank-year.
_COST_INCOME_DISCLOSED_RE = re.compile(r"cost:?\s*income ratio\s*\(as reported\)", re.I)


def _revenue_rank(label):
    # Broadened 2026-09-07 from an exact-match check (bare_label(label) ==
    # "total operating income"/"total income") to a startswith check on the
    # row's OWN text (see statement_row_selection.own_label) - found via
    # HSBC Bank Plc, whose own revenue TOTAL row is "Total operating income
    # (IFRS 4 presentation, pre-FY2023)": the trailing presentation-era
    # qualifier meant it never matched the old exact set, so it fell to the
    # same rank-1 tie as "Net operating income" (post credit-loss-charge)
    # and "Net operating income before change in expected credit losses" -
    # all three then tied on sort_key, and the SHORTEST own_label ("Net
    # operating income") won by default, silently preferring a post-ECL,
    # non-gross income figure over the bank's actual gross revenue total. A
    # prefix match keeps genuine "Total operating/net income (...)" variants
    # at top priority regardless of what descriptive text a bank appends.
    #
    # Middle rank (1, added 2026-09-08) for a "before change in expected
    # credit losses"/"before impairment" variant, ranked ABOVE a bare "Net
    # operating income" (rank 2): found via Marks and Spencer Financial
    # Services, whose own two TOTAL rows are "Net operating income" (124749,
    # already net of a -62260 impairment charge) and "Net operating income
    # before change in expected credit losses" (187009, the true gross
    # total). Both used to tie at rank 1 and lose to the SHORTER bare label,
    # selecting the impairment-netted figure as revenue even though
    # net_interest_pct/net_fee_pct are computed from gross, pre-impairment
    # income components elsewhere - so their sum came out to 145% of that
    # revenue, and the residual "other" swallowed the impairment charge as a
    # nonsensical -44.62% of income on the profit-loss.html chart. The gross
    # "before" variant is what's actually commensurate with those
    # components. Doesn't fire for HSBC Bank/HSBC UK Bank, which already win
    # via the preferred-prefix branch above through their own third row
    # ("Total operating income (IFRS 4 presentation...)").
    own = own_label(label).lower().strip()
    if own.startswith(_REVENUE_PREFERRED_PREFIXES):
        return 0
    if re.search(r"before.*(?:expected credit loss|impairment)", own, re.I):
        return 1
    return 2


def cost_base(observations):
    """Profit & Loss: Personnel expense, Other operating expense, Total
    operating expense, and each as a % of revenue (a cost-to-income style
    view). Revenue is selected via a priority list (94 loose label variants
    exist; "Total operating income"/"Total income" preferred over "Net
    operating income" or narrower "operating income" lines) since P&L has
    no single canonical revenue label across all 145 banks.

    total_opex/revenue rely on select_labeled_rows's require_own_match
    default (see statement_row_selection.py) to reject a row that only
    matches via its SECTION prefix (e.g. Punjab National Bank
    International's "Profit/(loss) before tax" sitting inside a SECTION
    literally named "Operating expenses") rather than its own text."""
    personnel, _ = select_labeled_rows(observations, "Profit & Loss", _PERSONNEL_RE, _OF_WHICH_RE)
    other_opex, _ = select_labeled_rows(observations, "Profit & Loss", _OTHER_OPEX_RE, _OF_WHICH_RE)
    total_opex, opex_ambiguous = select_labeled_rows(
        observations, "Profit & Loss", _TOTAL_OPEX_RE, _TOTAL_OPEX_EXCLUDE_RE, require_kind="TOTAL",
    )
    revenue, revenue_ambiguous = select_labeled_rows(
        observations, "Profit & Loss", _REVENUE_RE, _REVENUE_EXCLUDE_RE, rank=_revenue_rank,
    )
    disclosed_cost_to_income, _ = select_labeled_rows(observations, "Profit & Loss", _COST_INCOME_DISCLOSED_RE)

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

    cost_to_income_pct = defaultdict(dict)
    for (frn, year), item in disclosed_cost_to_income.items():
        cost_to_income_pct[frn][year] = float(item["value_numeric"])
    for frn, years in pct_of_revenue(total_opex).items():
        for year, value in years.items():
            cost_to_income_pct[frn].setdefault(year, value)

    return {
        "personnel_expense": series(personnel),
        "other_operating_expense": series(other_opex),
        "total_operating_expense": series(total_opex),
        "revenue": series(revenue),
        "personnel_expense_pct_of_revenue": pct_of_revenue(personnel),
        "other_operating_expense_pct_of_revenue": pct_of_revenue(other_opex),
        "cost_to_income_pct": dict(cost_to_income_pct),
        "coverage": {
            "banks_with_personnel": len({f for f, _ in personnel}),
            "banks_with_other_opex": len({f for f, _ in other_opex}),
            "banks_with_total_opex": len({f for f, _ in total_opex}),
            "banks_with_revenue": len({f for f, _ in revenue}),
            "banks_with_disclosed_cost_to_income": len({f for f, _ in disclosed_cost_to_income}),
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
