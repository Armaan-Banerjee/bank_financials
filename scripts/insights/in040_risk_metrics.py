"""Derived risk metrics for IN-040.

Reads `research/insights.db` directly and emits a JSON payload covering the
four risk signals chartered for IN-040: loan concentration/quality, RWA
density, leverage, and income volatility. Writes no new database tables -
this is an analysis module in the existing `in0NN_*.py` family
(`in012_absolute_analysis.py`, `in022_ratio_decomposition.py`), not a
pipeline step.

Row-label prefixes from IN-039's section-disambiguation fix (e.g. "Assets -
Derivative financial instruments", "Credit risk - Of which: standardised
approach") mean every selector here matches against the full prefixed label,
never a bare metric name.
"""

import argparse
import os
import re
from collections import defaultdict
from statistics import pstdev

from in009_analysis import _select_metric_observations
from in012_absolute_analysis import write_json_atomic
from statement_row_selection import bare_label as _bare_label, select_labeled_rows as _select_labeled_rows

STATEMENT_SHEETS = ("Balance Sheet", "Profit & Loss", "Asset Quality", "RWA Breakdown")


def _numeric(observation):
    return observation is not None and observation.get("value_status") in ("numeric", "special_numeric") and observation.get("value_numeric") is not None


_TOTAL_ASSETS_RE = re.compile(r"total assets$", re.I)
_TOTAL_EQUITY_RE = re.compile(r"total equity$", re.I)
_LOANS_TO_CUSTOMERS_RE = re.compile(r"loans and advances to customers$", re.I)

_PROFIT_LOSS_EXACT = {
    "profit for the year", "loss for the year",
    "(loss)/profit for the year", "profit/(loss) for the year",
    "(loss) for the year", "profit for the period", "loss for the period",
}
_PROFIT_LOSS_RE = re.compile(r"(profit|loss)\s+for\s+the\s+(year|period)", re.I)
_PROFIT_LOSS_EXCLUDE_RE = re.compile(r"discontinued|comprehensive|before tax", re.I)
# "attributable"/"minority"/"non-controlling" used to be hard-excluded
# alongside the above, to avoid picking a parent-only or NCI-split figure
# over a bank's real group-level headline when BOTH exist. But several
# banks with no minority interest at all (Unity Trust) disclose ONLY
# "Profit for the year attributable to shareholders" - there, that line
# IS the headline, not an NCI split, and the hard exclusion left the whole
# bank-year with no profit figure despite one being clearly disclosed
# (found via a 2026-09-04 user report). Kept as a soft/fallback exclusion
# in income_volatility() instead - used only when nothing else in the
# bank-year matched.
_PROFIT_LOSS_SOFT_EXCLUDE_RE = re.compile(r"attributable|minority|non-controlling", re.I)

_RWA_CATEGORY_EXCLUDE_RE = re.compile(r"of which|total", re.I)
_STAGE_RE = re.compile(r"stage\s*([123])\b", re.I)
_COVERAGE_NPL_RE = re.compile(r"coverage ratio|npl ratio|non-?performing loan", re.I)
# Boilerplate IFRS 9 stage-basis wording ("12-month ECL", "lifetime ECL",
# "credit-impaired", "SICR") restates which stage a row belongs to - it's
# redundant given _STAGE_RE already captured the stage number, and it
# differs per stage BY DEFINITION (stage 1 = 12-month ECL, stage 2 = SICR/
# lifetime ECL not credit-impaired, stage 3 = lifetime ECL credit-impaired).
# Keeping it in the category name therefore doesn't distinguish anything -
# it just fragments what should be one category ("Gross carrying amount by
# IFRS 9 stage") into three different category strings, one per stage
# (Unity Trust, Secure Trust Bank and others, found via a 2026-09-04 user
# report that a bank's own worksheet clearly had Stage 1/2/3 data the
# comparison page claimed didn't exist).
_STAGE_BASIS_SUFFIX = r"(?:not\s+)?(?:sicr|credit[\s-]?impaired)"
_STAGE_BASIS_CORE = rf"(?:subject to\s+)?(?:12[\s-]?months?|lifetime)\s+ecl(?:\s*[-,]\s*{_STAGE_BASIS_SUFFIX})?"
# Matched as one whole parenthesised group first ("(12 month ECL)",
# "(Lifetime ECL - SICR)") so the group's own internal " - " separator
# (between "Lifetime ECL" and "SICR"/"credit impaired") is consumed along
# with it, rather than left behind as a stray "-" segment once the two
# halves are stripped independently (Unity Trust's Stage 2 category
# reduced to "Gross carrying amount by IFRS 9 stage - -", found in the
# same 2026-09-04 investigation as the mangled-fragment bug above). A bare
# (unparenthesised) form catches the same wording when a bank writes it
# without parens (Secure Trust Bank: "subject to 12-month ECL").
#
# Matches everything up to the closing paren once the ECL-basis wording is
# seen, rather than requiring the trailing suffix to match one of a fixed
# list of phrasings - British Arab Commercial Bank's Stage 3 parenthetical
# is "(lifetime ECL, credit-impaired / default)", where the extra
# "/ default" after "credit-impaired" fell outside _STAGE_BASIS_SUFFIX's
# closed vocabulary, so the whole parenthetical was left unstripped and
# Stage 3's category string ended up different from Stage 1/2's - fragmenting
# the category and making Stage 3 vanish from the primary chart (found via a
# 2026-09-04 user report that BACB's chart looked narrower than others').
_STAGE_BASIS_PAREN_RE = re.compile(
    r"\(\s*(?:subject to\s+)?(?:12[\s-]?months?|lifetime)\s+ecl[^)]*\)", re.I
)
_STAGE_BASIS_BARE_RE = re.compile(_STAGE_BASIS_CORE, re.I)
# A separate, stage-redundant classification some banks add alongside (or
# instead of) the ECL-basis wording - "non-performing"/"performing"/
# "default" is just another name for stage 3 / stages 1-2, so it fragments
# categories the same way if left in (FirstBank UK's "Stage 3 / Default"
# left a dangling "/ Default" fragment once "Stage 3" and its trailing
# parenthetical were stripped, giving Stage 3 a different category string
# than Stage 1/2 and dropping it from the primary chart - found via a
# 2026-09-04 user report that FirstBank UK's chart looked narrower than
# others').
_STAGE_BASIS_EXTRA_RE = re.compile(
    r"\(?\s*sicr\s*\)?|\bcredit[\s-]?impaired\b|\bnon[\s-]?performing\b|\bunderperforming\b|\bperforming\b|"
    r"/?\s*\bdefault\b",
    re.I,
)
# A scope footnote some banks attach only to their Stage 3 row ("(incl.
# POCI where separately disclosed)") - it's a disclosure-scope note, not a
# distinguishing category, so left in place it fragments Stage 3 into its
# own category apart from Stage 1/2 (Barclays Bank UK PLC: Stage 3's gross
# exposure and impairment-allowance rows vanished from the shared category
# entirely, found in the same 2026-09-04 investigation as the BACB paren
# fix above).
_STAGE_SCOPE_NOTE_RE = re.compile(r"\(\s*incl\.?\s+poci[^)]*\)", re.I)


def _profit_loss_rank(label):
    return 0 if _bare_label(label).lower() in _PROFIT_LOSS_EXACT else 1


def _stage_num_and_category(label):
    """Find the "Stage N" marker anywhere in a row label, and derive the
    category from everything else. bare_label() strips only the LAST " - "
    segment (built for a single IN-039 section prefix), which silently
    drops the stage number whenever it sits in a middle segment rather than
    the last one - e.g. HSBC UK Bank's "Loans and advances to customers at
    amortised cost, by IFRS 9 stage - Stage 1 - gross carrying amount"
    reduces to just "gross carrying amount" under bare_label(), so the
    stage regex never matched and this bank (plus Metro Bank, Standard
    Chartered Bank, and others sharing this label shape) silently showed no
    loan-concentration chart despite having real Stage 1/2/3 gross balances
    in the database - found via a 2026-09-04 user report that too many
    banks looked empty.

    Removes only the matched "Stage N" text from the FULL label (not a
    whole " - "-split segment) - splitting on " - " first and discarding
    the whole segment mangles any descriptor that itself contains " - "
    (Unity Trust's "Stage 2 (Lifetime ECL - SICR)" reduced to the reordered
    fragment "SICR) - (Lifetime ECL", found in the same 2026-09-04 report).
    The stage-basis boilerplate left over after that ("(12 month ECL)",
    "(Lifetime ECL - SICR)") is then stripped entirely (see
    _STAGE_BASIS_PAREN_RE/_STAGE_BASIS_BARE_RE) rather than kept as part of the category,
    since it's redundant with the stage number and differs per stage by
    IFRS 9's own definitions - keeping it fragments what should be one
    category ("Gross carrying amount by IFRS 9 stage") into three, one per
    stage. A genuine metric-type descriptor that ISN'T stage-basis
    boilerplate (Metro Bank's "gross carrying amount") survives unchanged."""
    match = _STAGE_RE.search(label)
    if not match:
        return None, None
    without_stage = label[:match.start()] + label[match.end():]
    without_stage = _STAGE_BASIS_PAREN_RE.sub("", without_stage)
    without_stage = _STAGE_BASIS_BARE_RE.sub("", without_stage)
    without_stage = _STAGE_BASIS_EXTRA_RE.sub("", without_stage)
    without_stage = _STAGE_SCOPE_NOTE_RE.sub("", without_stage)
    segments = [s.strip(" ,:()") for s in without_stage.split(" - ")]
    category = " - ".join(s for s in segments if s) or "Total"
    return match.group(1), category


def loan_concentration_quality(observations):
    """Asset Quality: IFRS 9 stage balances by category, plus any disclosed
    coverage/NPL ratios. Genuinely heterogeneous across banks - reported as
    a catalogue of what each bank actually discloses, not forced into one
    shared shape."""
    stage_rows = defaultdict(lambda: defaultdict(dict))
    stage_banks = set()
    for item in observations:
        if item.get("sheet") != "Asset Quality" or not item.get("annual_eligible"):
            continue
        if item.get("value_status") not in ("numeric", "special_numeric"):
            continue
        label = item.get("row_label", "")
        stage_num, category = _stage_num_and_category(label)
        if stage_num is None:
            continue
        stage = f"stage_{stage_num}"
        stage_rows[item["frn"]][item["fiscal_year"]].setdefault(category, {})[stage] = float(item["value_numeric"])
        stage_banks.add(item["frn"])

    coverage_npl = defaultdict(list)
    for item in observations:
        if item.get("sheet") != "Asset Quality" or not item.get("annual_eligible"):
            continue
        if item.get("value_status") not in ("numeric", "special_numeric"):
            continue
        if not _COVERAGE_NPL_RE.search(item.get("row_label", "")):
            continue
        coverage_npl[item["frn"]].append({
            "year": item["fiscal_year"], "label": item["row_label"],
            "value": float(item["value_numeric"]), "value_raw": item.get("value_raw"),
        })

    return {
        "stage_balances": {frn: {year: cats for year, cats in years.items()} for frn, years in stage_rows.items()},
        "coverage_and_npl_ratios": dict(coverage_npl),
        "coverage": {
            "banks_with_stage_data": len(stage_banks),
            "banks_with_coverage_or_npl_disclosure": len(coverage_npl),
        },
    }


def rwa_density(observations):
    """RWA per category (RWA Breakdown) as a % of the bank-year's Total RWAs
    (sourced from the clean Pillar 3 Total RWAs sheet, not re-derived from
    RWA Breakdown's own free-text grand-total row, which has 57 distinct
    label variants and a real false-positive risk against category
    sub-totals like "Total Credit Risk-Weighted Assets (CRWA)")."""
    total_rwas = {(item["frn"], item["fiscal_year"]): item for item in _select_metric_observations(observations, "Total RWAs") if item.get("annual_eligible")}
    total_assets, _ = _select_labeled_rows(observations, "Balance Sheet", _TOTAL_ASSETS_RE)

    category_rows = defaultdict(list)
    # A bank-year whose EVERY RWA Breakdown row got excluded by
    # _RWA_CATEGORY_EXCLUDE_RE's "total" branch (e.g. Bank of the
    # Philippine Islands (Europe): "Total Credit Risk-Weighted Assets
    # (CRWA)"/"Total Market..."/"Total Operational..." are that bank's
    # ONLY level of disaggregation, no finer exposure-class breakdown
    # underneath) ends up with zero categories even though real per-risk-
    # type figures exist. Collected below as a same-key fallback pool, used
    # only when the primary filter leaves nothing at all.
    excluded_candidates = defaultdict(list)
    for item in observations:
        if item.get("sheet") != "RWA Breakdown" or not item.get("annual_eligible"):
            continue
        if item.get("value_status") not in ("numeric", "special_numeric"):
            continue
        label = item.get("row_label", "")
        bare = _bare_label(label)
        key = (item["frn"], item["fiscal_year"])
        rwa = total_rwas.get(key)
        if rwa is None or float(rwa["value_numeric"]) == 0:
            continue
        pct = round(float(item["value_numeric"]) / float(rwa["value_numeric"]) * 100, 2)
        row = {"label": label, "value": float(item["value_numeric"]), "pct_of_total_rwa": pct}
        if _RWA_CATEGORY_EXCLUDE_RE.search(bare):
            if "of which" not in bare.lower():
                excluded_candidates[key].append(row)
            continue
        category_rows[key].append(row)

    for key, candidates in excluded_candidates.items():
        if not category_rows[key]:
            # No primary (non-"total"-labeled) category survived at all
            # (Bank of the Philippine Islands (Europe): "Total Credit/
            # Market/Operational Risk-Weighted Assets" are its ONLY level
            # of disaggregation, no finer breakdown underneath). Identify
            # the row that IS the grand total by internal arithmetic, not
            # by label text (57 distinct label variants for "this is the
            # total" alone make text matching unreliable) or by proximity
            # to the external Total RWAs sheet figure (tried first, but
            # rejected - BPI Europe's Total RWAs sheet and its own RWA
            # Breakdown total disagree by ~7%, a same-workbook data-quality
            # wrinkle unrelated to this selection problem, which made its
            # Credit-risk-alone row look like "the total" against the
            # external figure while genuinely being just one category). A
            # candidate whose value equals the SUM of every other
            # candidate's value (both self-consistent within the same
            # sheet) is reliably the grand total; everything else is a
            # genuine per-risk-type category this bank just happens to
            # also name "Total X risk". Skip entirely when no candidate is
            # self-consistently the sum of the rest - that bank-year isn't
            # this pattern, left empty rather than guessed at.
            total_row = None
            for candidate in candidates:
                others_sum = sum(c["value"] for c in candidates if c is not candidate)
                if others_sum and abs(candidate["value"] - others_sum) / others_sum < 0.02:
                    total_row = candidate
                    break
            remainder = [r for r in candidates if r is not total_row] if total_row is not None else candidates
            remainder_sum = sum(r["pct_of_total_rwa"] for r in remainder)
            if 80 <= remainder_sum <= 120:
                category_rows[key] = remainder
        else:
            # Some primary categories already survived, but a genuine
            # category's ONLY figure happens to be named "Total X risk"
            # alongside real finer-grained categories elsewhere (Unity
            # Trust: "Operational risk" and "Credit Valuation Adjustment"
            # survive untouched, but its only credit-risk figure is named
            # "Total credit risk" and got excluded alongside the real grand
            # total "Total RWA", leaving credit risk - ~83% of the bank's
            # RWA - missing from the chart entirely). Distinguish that from
            # a genuine redundant subtotal (C. Hoare & Co: "Institutions" +
            # "Corporates" already cover the whole of "Total credit risk")
            # by value, not just headroom - a subtotal's value equals the
            # sum of exactly the categories already accepted, whereas a
            # genuinely missing category's value doesn't relate to them at
            # all. Headroom (not exceeding ~120% combined) is still the
            # backstop for any candidate that passes the value check.
            existing_value_sum = sum(r["value"] for r in category_rows[key])
            running_pct = sum(r["pct_of_total_rwa"] for r in category_rows[key])
            for candidate in sorted(candidates, key=lambda c: c["pct_of_total_rwa"]):
                if existing_value_sum and abs(candidate["value"] - existing_value_sum) / existing_value_sum < 0.02:
                    continue
                if running_pct + candidate["pct_of_total_rwa"] <= 120:
                    category_rows[key].append(candidate)
                    running_pct += candidate["pct_of_total_rwa"]

    # The Total RWAs sheet (add_metric_sheet, Pillar 3 KM1) never records a
    # per-row unit - unlike Balance Sheet, which does (£'000 for most banks,
    # £m for some, e.g. TSB Bank). Most banks transcribe RWA in the same
    # unit as their own Balance Sheet, so the ratio comes out right, but a
    # bank whose real source documents use a *different* unit across the two
    # disclosures (TSB Bank: Pillar 3 in £'000, statutory accounts in £m)
    # silently produces a nonsense ratio a full 1000x off with no unit field
    # to catch it. RWA density is essentially never seen above ~150% for a
    # real UK bank, so a wildly implausible result is a much stronger signal
    # of exactly this cross-sheet unit mismatch than of a genuine outlier -
    # excluded rather than published, consistent with leaving a year blank
    # over guessing at it. The same unit-less "Total RWAs" sheet produces the
    # mismatch in the other direction too (e.g. Investec: RWA transcribed in
    # £m against a Balance Sheet in £'000, yielding a 0.06% density) - real
    # UK banks always carry meaningful credit risk, so density near zero is
    # exactly as implausible as density above 300%. The bank-year population
    # is cleanly bimodal here (130 bank-years under 1%, then a gap, then the
    # legitimate distribution from ~5% up), so 1% is a real gap in the data,
    # not an arbitrary cutoff risking a genuine low-RWA bank.
    _IMPLAUSIBLE_RWA_DENSITY_PCT = 300
    _IMPLAUSIBLE_RWA_DENSITY_LOW_PCT = 1
    rwa_to_assets_pct = {}
    implausible_skipped = 0
    for key, rwa in total_rwas.items():
        assets = total_assets.get(key)
        if assets is None or float(assets["value_numeric"]) == 0:
            continue
        frn, year = key
        pct = round(float(rwa["value_numeric"]) / float(assets["value_numeric"]) * 100, 2)
        if pct > _IMPLAUSIBLE_RWA_DENSITY_PCT or pct < _IMPLAUSIBLE_RWA_DENSITY_LOW_PCT:
            implausible_skipped += 1
            continue
        rwa_to_assets_pct.setdefault(frn, {})[year] = pct

    # Same cross-sheet unit-mismatch risk as rwa_to_assets_pct above, but
    # here it's RWA Breakdown (has its own £'000/£m unit_suffix) divided by
    # the unit-less Total RWAs sheet - found in practice via ABC
    # International Bank, whose Total RWAs sheet is £m while its RWA
    # Breakdown is £'000: every category's pct_of_total_rwa came out ~1000x
    # too large (e.g. 91746% "Credit risk"). A legitimate bank's category
    # percentages sum to roughly 100% (up to ~210% seen for banks that
    # disclose overlapping "of which" sub-totals not caught by
    # _RWA_CATEGORY_EXCLUDE_RE); the mismatched bank-years sum to ~99,500-
    # 100,500% - a clean gap, not a fuzzy boundary. Drop the whole
    # bank-year's composition rather than publish a chart that can't sum
    # to 100%.
    _IMPLAUSIBLE_RWA_CATEGORY_SUM_PCT = 300
    implausible_category_skipped = 0
    filtered_category_rows = {}
    for key, rows in category_rows.items():
        if not rows:
            continue
        if sum(r["pct_of_total_rwa"] for r in rows) > _IMPLAUSIBLE_RWA_CATEGORY_SUM_PCT:
            implausible_category_skipped += 1
            continue
        filtered_category_rows[key] = rows

    return {
        "rwa_to_assets_pct": rwa_to_assets_pct,
        "rwa_category_composition": {f"{frn}:{year}": rows for (frn, year), rows in filtered_category_rows.items()},
        "coverage": {
            "bank_years_with_total_rwa": len(total_rwas),
            "bank_years_with_rwa_to_assets": sum(len(v) for v in rwa_to_assets_pct.values()),
            "bank_years_with_category_breakdown": len(filtered_category_rows),
            "implausible_rwa_to_assets_skipped": implausible_skipped,
            "implausible_rwa_category_sum_skipped": implausible_category_skipped,
        },
    }


def leverage(observations):
    """Total equity / Total assets (Balance Sheet), reported alongside the
    existing Leverage Ratio Pillar 3 sheet - two genuinely different
    methodologies (a simple accounting ratio vs. a regulatory leverage
    exposure measure), presented side by side rather than reconciled or
    treated as a cross-check of each other."""
    total_assets, _ = _select_labeled_rows(observations, "Balance Sheet", _TOTAL_ASSETS_RE)
    total_equity, _ = _select_labeled_rows(observations, "Balance Sheet", _TOTAL_EQUITY_RE)
    reported = {(item["frn"], item["fiscal_year"]): item for item in _select_metric_observations(observations, "Leverage Ratio") if item.get("annual_eligible") and item.get("value_status") in ("numeric", "special_numeric")}

    equity_to_assets_pct = defaultdict(dict)
    for key, assets in total_assets.items():
        equity = total_equity.get(key)
        if equity is None or float(assets["value_numeric"]) == 0:
            continue
        frn, year = key
        equity_to_assets_pct[frn][year] = round(float(equity["value_numeric"]) / float(assets["value_numeric"]) * 100, 2)

    leverage_ratio_reported_pct = defaultdict(dict)
    for (frn, year), item in reported.items():
        leverage_ratio_reported_pct[frn][year] = float(item["value_numeric"])

    return {
        "equity_to_assets_pct": dict(equity_to_assets_pct),
        "leverage_ratio_reported_pct": dict(leverage_ratio_reported_pct),
        "coverage": {
            "banks_with_equity_to_assets": len(equity_to_assets_pct),
            "banks_with_reported_leverage_ratio": len(leverage_ratio_reported_pct),
            "banks_with_both": len(set(equity_to_assets_pct) & set(leverage_ratio_reported_pct)),
        },
    }


def income_volatility(observations):
    """Profit/loss for the year (Profit & Loss), selected via a priority
    list that prefers the bare headline row over attributable-to-owners or
    comprehensive-income variants (33 distinct label variants exist across
    banks) - ambiguous bank-years (multiple equally-ranked candidates) are
    counted and skipped rather than guessed. Year-over-year swings and a
    per-bank volatility measure (population stdev of YoY % change) are
    computed now; visualization is deferred to IN-046."""
    combined_exclude_re = re.compile(
        _PROFIT_LOSS_EXCLUDE_RE.pattern + "|" + _PROFIT_LOSS_SOFT_EXCLUDE_RE.pattern, re.I
    )
    selected, ambiguous = _select_labeled_rows(
        observations, "Profit & Loss", _PROFIT_LOSS_RE, combined_exclude_re, rank=_profit_loss_rank,
    )
    # Bank-years with no clean (non-attributable) match fall back to the
    # attributable/NCI-labeled line rather than being left empty - see the
    # soft-exclude comment above.
    fallback_selected, _ = _select_labeled_rows(
        observations, "Profit & Loss", _PROFIT_LOSS_RE, _PROFIT_LOSS_EXCLUDE_RE, rank=_profit_loss_rank,
    )
    for key, item in fallback_selected.items():
        selected.setdefault(key, item)

    series = defaultdict(dict)
    labels_used = defaultdict(dict)
    for (frn, year), item in selected.items():
        series[frn][year] = float(item["value_numeric"])
        labels_used[frn][year] = item["row_label"]

    yoy_changes = defaultdict(dict)
    volatility = {}
    for frn, values in series.items():
        years = sorted(values)
        changes = {}
        for left, right in zip(years, years[1:]):
            if values[left] == 0:
                continue
            changes[right] = round((values[right] - values[left]) / abs(values[left]) * 100, 2)
        if changes:
            yoy_changes[frn] = changes
        if len(changes) >= 2:
            volatility[frn] = round(pstdev(changes.values()), 2)

    return {
        "profit_or_loss_for_year": dict(series),
        "labels_used": dict(labels_used),
        "yoy_change_pct": dict(yoy_changes),
        "volatility_stdev_of_yoy_pct": volatility,
        "coverage": {
            "banks": len(series),
            "ambiguous_bank_years_skipped": ambiguous,
        },
    }


def build_in040_payload(db_path):
    from analysis_queries import AnalysisQueries
    observations = AnalysisQueries(db_path).observations()
    banks = {item["frn"]: item.get("bank", item.get("canonical_bank", "")) for item in observations}
    return {
        "metadata": {"source": os.path.abspath(db_path), "banks": banks},
        "loan_concentration_quality": loan_concentration_quality(observations),
        "rwa_density": rwa_density(observations),
        "leverage": leverage(observations),
        "income_volatility": income_volatility(observations),
    }


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(root, "research", "insights.db"))
    parser.add_argument("--out", default=os.path.join(root, "research", "in040_risk_metrics.json"))
    args = parser.parse_args()
    write_json_atomic(build_in040_payload(args.db), args.out)
    print(f"Wrote IN-040 risk-metrics payload to {args.out}")


if __name__ == "__main__":
    main()
