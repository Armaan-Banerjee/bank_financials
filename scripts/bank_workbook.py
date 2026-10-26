"""
Shared helpers for building "<BANK> FINANCIALS.xlsx" workbooks in banks/.

Standard structure (as of the ST- wayfinder map, see
wayfinder/statements/map.md - 18 sheets total): an "Overview" sheet
(headline Balance Sheet/P&L/Equity/Cash Flow figures plus Pillar 3 ratios -
see the "spend and risk" lens in the map's Destination), then "Balance
Sheet" (Consolidated Statement of Financial Position), "Profit & Loss"
(Consolidated Statement of Comprehensive Income), a "Statement of Changes
in Equity" sheet, a "Cash Flow Statement" sheet (full statement, period
columns, most-recent-first), an "Asset Quality" sheet (loan book by
product and IFRS 9 stage, plus NPL/coverage ratios), one sheet per Pillar 3
key metric (CET1 Capital, CET1 Ratio, Tier 1 Capital, Tier 1 Ratio, Total
Capital, Total Capital Ratio, Total RWAs, Leverage Ratio, LCR, NSFR, MREL
Ratio), and finally an "RWA Breakdown" sheet (placed right after Total
RWAs, not after MREL Ratio, since it's itself a Pillar 3 disclosure). Each
sheet ends in a single merged, wrapped source-citation cell rather than a
per-row citation column.

Usage:
    from bank_workbook import BankWorkbook, PILLAR3_SHEET_NAMES

    wb = BankWorkbook(
        bank_name="Example Bank Plc",
        years=["FY2025", "FY2024", "FY2023"],
        header_color="0A2540",
    )
    wb.add_overview_sheet(balance_sheet_totals=[...], balance_sheet_unit=..., income_statement_totals=[...],
                           income_statement_unit=..., equity_changes_totals=[...], equity_changes_unit=...,
                           cash_flow_totals=[...], cash_flow_unit=..., ratios=[...])
    wb.add_balance_sheet_sheet(title=..., subtitle=..., rows=[...], sources_text=...)
    wb.add_income_statement_sheet(title=..., subtitle=..., rows=[...], sources_text=...)
    wb.add_equity_changes_sheet(title=..., subtitle=..., headers=[...], rows=[...], sources_text=...)
    wb.add_cash_flow_sheet(title=..., subtitle=..., rows=[...], sources_text=...)
    wb.add_asset_quality_sheet(title=..., subtitle=..., rows=[...], sources_text=...)
    wb.add_metric_sheet("CET1 Capital", unit="£'000", rows_data=[...], sources_text=...)
    wb.add_rwa_breakdown_sheet(title=..., subtitle=..., rows=[...], sources_text=...)
    wb.add_long_form_sheet("Interim Pillar 3", headers=[...], rows=[...])
    ...
    wb.save("/Users/armaan/code/katalysis/banks/EXAMPLE BANK FINANCIALS.xlsx")

Row tuple formats:
    Cash flow / Balance Sheet / Profit & Loss / Asset Quality / RWA
        Breakdown `rows`: (kind, label, values) where kind is "SECTION"
        (label-only divider), "DATA" (a normal line item) or "TOTAL"
        (bolded subtotal/total). `values` is a dict of {year: number};
        omit a year to leave it blank. Asset Quality and RWA Breakdown
        ratio rows may use string values (e.g. "13.55%") the same way
        Metric sheet rows do.
    Equity changes `rows`: (kind, label, values) where kind is "DATA" or
        "TOTAL" (bolded - use for balance b/f-c/f and comprehensive-income
        rows). `values` is a tuple positionally aligned to the sheet's
        `headers` (equity components), not a year dict - this sheet reads
        chronologically oldest-to-newest, not year-columned.
    Metric sheet `rows_data`: (label, values) pairs, values as above. Use
        string values (e.g. "82.94%", "Not publicly disclosed") freely -
        cells are written as-is.
"""

import collections
import json
import os
import re
import sys

import openpyxl
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

# The bank's own UK KM1 "Key metrics" template. Kept OUT of
# PILLAR3_SHEET_NAMES for the same reason "RWA Breakdown" is: that list names
# the 11 single-metric sheets, whereas this is a published disclosure template
# reproduced whole. It sits immediately before those 11 sheets - sheet order
# follows call order in the build script, so call add_km1_sheet() before the
# first add_metric_sheet().
KM1_SHEET_NAME = "KM1 Key Metrics"

PILLAR3_SHEET_NAMES = [
    "CET1 Capital",
    "CET1 Ratio",
    "Tier 1 Capital",
    "Tier 1 Ratio",
    "Total Capital",
    "Total Capital Ratio",
    "Total RWAs",
    "Leverage Ratio",
    "LCR",
    "NSFR",
    "MREL Ratio",
]

_PERCENT_RE = re.compile(r"^\s*(-?[\d,]+\.?\d*)\s*%")


def _parse_percent(value):
    """Parse a displayed ratio value ("14.5%") into a float (14.5) for
    charting; returns None for non-numeric values ("Not disclosed", etc.)."""
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        m = _PERCENT_RE.match(value)
        if m:
            return float(m.group(1).replace(",", ""))
    return None


THIN = Side(style="thin", color="D9D9D9")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
SECTION_FONT = Font(bold=True)
TOTAL_FONT = Font(bold=True)
TITLE_FONT = Font(bold=True, size=13)
SUBTITLE_FONT = Font(italic=True, size=9, color="666666")
# openpyxl's hard cell cap is 32,767 characters; 32,000 leaves headroom
# for the "(continued)" marker a split adds. See _write_source_cell.
SOURCE_CELL_LIMIT = 32000

SOURCE_FONT = Font(italic=True, size=9, color="444444")

# Measured in Microsoft Excel (macOS) on 2026-10-10 by auto-fitting a grid of
# text lengths against column widths in the 9pt italic face both the note and
# the source cell use, then reading the heights back. See _fit_height.
WRAPPED_LINE_POINTS = 13.0
# 1.43 chars per width unit measured; held at 1.40 so the estimate errs tall.
# Real citation text wraps worse than the test's prose: it carries URLs that
# cannot break and explicit newlines that end a line early.
CHARS_PER_WIDTH_UNIT = 1.40
MIN_FITTED_HEIGHT = 30.0
# Excel will RENDER a row of any height a file gives it (a stored 1700 lays
# out at 1700 - verified by reading back row positions, which accumulate
# exactly). But ~409.5 is the tallest row Excel lets a PERSON set, and its own
# auto-fit saturates at 410, so a taller row is one the reader can never
# restore by hand once they touch it. Long text therefore SPILLS across
# several rows at this cap rather than living in one enormous one (user
# decision, 2026-10-10).
MAX_DISPLAY_HEIGHT = 409.0


def _norm_label(label):
    """Compare row labels the way check_overview_ties.py does."""
    return re.sub(r"\s+", " ", str(label)).strip().lower()


# -- Profitability (derived sheet) ---------------------------------------------
# The sheet name is a constant for the same reason KM1_SHEET_NAME is: a verifier
# and two checkers look for it, and a string typed in four places is a string
# that eventually differs in one of them.
PROFITABILITY_SHEET_NAME = "Profitability"

# What a contaminated cell says. GA-020: a statement cell must say WHICH
# outcome it is, and it must be SHORT - a data column is 15 width units, about
# 21 characters, and Excel clips the overflow against the next cell rather than
# widening it. "Not computed" is that word; WHY it was not computed is a
# paragraph, and a paragraph goes in the note, which auto-fits. (check_cell_fit
# audits merged note and source cells, not data cells, so this length is a
# judgement the library has to get right, not one a check will catch.)
REFUSED_MIXED_BASIS = "Not computed"

# Two sentinels, because None is a real answer here ("one native currency, the
# ratio cancels") and must not double as "nobody said". _FX_FROM_TABLE is the
# default: consult the audited table. _FX_UNAUDITED is what the table returns
# for a bank it has never been asked about, which is NOT the same as a bank it
# cleared.
_FX_FROM_TABLE = object()
_FX_UNAUDITED = object()

PUBLISHED_RETURNS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "research", "profitability", "published_returns.jsonl",
)

_BankReturns = collections.namedtuple(
    "_BankReturns",
    "published definitions deferred excluded examined none_finding",
)

_published_returns_cache = {}


def _read_published_returns(path=None):
    """-> {bank key: _BankReturns}, read once per process.

    `published` is {measure: {year: verbatim value}} for the records struck in
    the bank's OWN edition for that year. `deferred` holds the records that are
    a LATER edition's comparative: the own-edition rule keeps those out of the
    year's cell and puts them in the note, because a comparative restated in a
    later edition is a different claim from the figure the bank printed at the
    time. `excluded` holds records ruled out on entity or unit grounds, carried
    so nobody re-derives them. `examined` is every year the store holds any
    record for, which is the only thing that distinguishes "the bank did not
    print this that year" from "that year's report was never read" - and a
    blank cell cannot say which without it. `none_finding` is the verbatim
    positive finding that the bank publishes no return at all.
    """
    path = path or PUBLISHED_RETURNS_PATH
    if path in _published_returns_cache:
        return _published_returns_cache[path]
    banks = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if "_schema" in rec or not rec.get("bank"):
                continue
            # Built as mutable parts and frozen into the namedtuple at the
            # end, so a caller cannot accidentally mutate the process cache.
            cur = banks.setdefault(rec["bank"], ({}, {}, [], [], set(), [None]))
            published, definitions, deferred, excluded, examined, none_f = cur
            year = rec.get("year")
            if year:
                examined.add(year)
            if rec.get("excluded"):
                excluded.append(rec)
            elif rec.get("publishes_none"):
                none_f[0] = rec.get("finding") or none_f[0]
            elif rec.get("measure"):
                measure = rec["measure"]
                definitions.setdefault(
                    measure,
                    rec.get("definition") or rec.get("definition_verbatim"))
                if rec.get("own_edition") is False:
                    deferred.append(rec)
                else:
                    published.setdefault(measure, {})[year] = rec.get("value")
    out = {k: _BankReturns(v[0], v[1], v[2], v[3], v[4], v[5][0])
           for k, v in banks.items()}
    _published_returns_cache[path] = out
    return out


def _widest_spread(rows, years):
    """This bank's own widest average-vs-year-end divergence, named.

    Computed, not asserted: the two bases diverge most where the balance sheet
    moved fastest, and which year that is differs from bank to bank. Returns
    "" where the gap is under half a point, because then there is nothing to
    warn a reader about."""
    def pct(values, y):
        v = values.get(y)
        if isinstance(v, str) and v.endswith("%"):
            try:
                return float(v[:-1])
            except ValueError:
                return None
        return None
    by = dict(rows)
    avg = by.get("Return on equity - average equity basis", {})
    end = by.get("Return on equity - year-end equity basis", {})
    best = None
    for y in years:
        a, e = pct(avg, y), pct(end, y)
        if a is None or e is None:
            continue
        if best is None or abs(a - e) > best[0]:
            best = (abs(a - e), y, a, e)
    if best is None or best[0] < 0.5:
        return ""
    _gap, y, a, e = best
    return (f" The two diverge most in {y}, where return on equity is "
            f"{a:.2f}% on an average basis and {e:.2f}% on a year-end basis.")


def _profitability_note(bw, published_key, own, refused, entity_note,
                        short_years, fx_basis, unit, rows, years, extra_note):
    """The sheet's note, assembled from what the store and the arithmetic
    actually establish. Generated rather than hand-written per bank on
    purpose: 145 hand-written notes drift from the figures beside them, and
    every claim here is one the build can still prove on its next run."""
    paras = []

    if own.published:
        paras.append(
            "TWO KINDS OF FIGURE, NEVER MERGED. The rows above are not one "
            "series. The 'Return on equity/assets' rows are THIS PROJECT'S "
            "OWN ARITHMETIC on the figures printed on this workbook's "
            "statement sheets. The rows marked '(as published)' are the bank's "
            "own published ratios, quoted verbatim, each struck on the bank's "
            "own definition - which differs from bank to bank and usually from "
            "ours, most often in whether the numerator is before or after tax "
            "and whether the denominator is average, opening or year-end "
            "equity, tangible equity or required equity. They are not "
            "averaged, reconciled, or substituted for one another, and where "
            "they disagree both stand: the disagreement is the finding."
        )
        defs = [
            f"{m}: " + (f"“{own.definitions[m]}”"
                        if own.definitions.get(m)
                        else "the document states no definition, and none is "
                             "supplied here.")
            for m in sorted(own.published)
        ]
        paras.append("THE BANK'S OWN DEFINITIONS, VERBATIM. " + " ".join(defs))
    else:
        paras.append(
            "COMPUTED, NOT PUBLISHED. " + (own.none_finding or (
                f"{bw.bank_name} publishes no return on equity, return on "
                f"tangible equity or return on assets in any edition held."))
            + " Every percentage above is therefore this project's own "
            "arithmetic on the figures printed on this workbook's statement "
            "sheets, and is labelled as such. That the bank publishes none is "
            "a POSITIVE FINDING, recorded in "
            "research/profitability/published_returns.jsonl, and not a failed "
            "search: for this bank the computed figure is the only figure "
            "there is."
        )

    paras.append(
        "WHY TWO BASES ARE PRINTED FOR EACH RATIO, AND NEITHER IS PREFERRED. "
        "The average basis divides by the mean of the opening and closing "
        "balance and is the fairer measure of a year in which the balance "
        "sheet moved a long way; the year-end basis divides by the closing "
        "balance alone and is what most outside sources quote. Both are shown "
        "so the reader can see which question a figure answers. They are not "
        "averaged and neither is 'the' return." + _widest_spread(rows, years)
    )

    if short_years:
        order = [y for y in years if y in short_years]
        paras.append(
            ("%s DOES NOT COVER TWELVE MONTHS, SO IT IS NOT AN ANNUAL RETURN."
             % order[0] if len(order) == 1 else
             "SOME COLUMNS DO NOT COVER TWELVE MONTHS, SO THEIR RATIOS ARE "
             "NOT ANNUAL RETURNS.")
            + " " + " ".join(f"{y} is {short_years[y]}." for y in order)
            + " A return divides a profit-and-loss FLOW by a balance-sheet "
            "STOCK, so where the flow covers more or less than a year the "
            "quotient is scaled by that period and cannot be read against the "
            "columns either side of it. The figures above are printed anyway, "
            "and deliberately: both inputs are figures the bank itself "
            "published, and the ratio of them is exact. What is wrong is only "
            "the interpretation, which this paragraph supplies. They are NOT "
            "annualised - a pro-rata adjustment would be this project's "
            "arithmetic on a period the bank never annualised, and would "
            "invent a figure with no published counterpart."
        )

    oldest = years[-1] if years else None
    if oldest:
        paras.append(
            f"{oldest} HAS NO AVERAGE-BASIS RATIO, AND THAT IS CORRECT. An "
            f"average denominator needs an opening balance, and {oldest} is "
            f"the oldest column this workbook carries, so there is no prior "
            f"year to open from. The blank is structural, not a missing "
            f"figure. The year-end basis is shown for {oldest} because it "
            f"needs only the closing balance."
        )

    if entity_note:
        paras.append(
            "WHY EVERY COMPUTED CELL SAYS 'NOT COMPUTED', AND IT IS NOT A "
            "CURRENCY PROBLEM. " + entity_note + " The two statement sheets "
            "print the same unit, so a ratio across them cancels its unit "
            "perfectly and would pass every check this project runs - and it "
            "would still be one entity's profit over another entity's balance "
            "sheet, which is not a return on anything. A group figure is a "
            "different claim from a solo figure, so the ratio is refused "
            "rather than printed with a caveat. The underlying figures are "
            "all on this workbook's statement sheets, each labelled with the "
            "entity it belongs to, for a reader who wants to strike a ratio "
            "on a single perimeter."
        )

    if refused:
        order = [y for y in years if y in refused]
        paras.append(
            "WHY SOME CELLS SAY 'NOT COMPUTED'. "
            + ("Every year above" if len(order) == len(years)
               else "The years " + ", ".join(order))
            + " is marked 'Not computed' rather than given a number, and the "
            "reason is a unit problem, not a missing figure. This workbook's "
            f"statement sheets print {unit.strip() or 'a converted unit'}: the "
            "figures were converted from the bank's reporting currency on this "
            "project's standing convention, which converts BALANCE SHEET "
            "stocks at the financial year-end SPOT rate and PROFIT AND LOSS "
            "flows at that year's AVERAGE rate - the right treatment for each "
            "statement taken on its own. A ratio struck ACROSS the two "
            "therefore divides a figure converted at one rate by a figure "
            "converted at another. Both sides are labelled in the same "
            "currency, so such a ratio looks sound and is self-consistent on "
            "every check this project runs, but it carries the whole "
            "spot-versus-average spread - on recent years a bias of roughly "
            "two per cent of the ratio, changing sign from year to year, so it "
            "distorts the trend as well as the level. The house rule is that a "
            "ratio cancels its unit only if both sides share it; where they do "
            "not, the honest output is a refusal rather than a number with a "
            "caveat attached. A reader who wants these ratios should strike "
            "them on the bank's own figures in its own reporting currency, "
            "where both sides do share a basis. "
            "(scripts/profitability_fx_basis.py records the basis verdict for "
            "every converted workbook in this corpus, and why that verdict "
            "cannot be read off the page or detected in the code.)"
        )
        if isinstance(fx_basis, (set, frozenset, list, tuple)):
            clean = [y for y in years if y not in refused]
            if clean:
                paras.append(
                    "THE REST OF THE SERIES IS COMPUTED, AND THAT IS NOT AN "
                    "INCONSISTENCY. " + ", ".join(clean) + " are shown as "
                    "percentages because in those years both statements rest "
                    "on a single basis, so the ratio does cancel. The split is "
                    "a property of this bank's own reporting history, not of "
                    "the method."
                )

    if own.deferred:
        bits = "; ".join(
            f"{r.get('year')} {r.get('measure')} {r.get('value')}"
            for r in own.deferred)
        paras.append(
            "FIGURES THE BANK PUBLISHED ONLY AS A LATER EDITION'S "
            "COMPARATIVE, AND WHY THEY ARE NOT IN THE CELLS ABOVE. " + bits +
            ". Each year's cell carries what that year's OWN annual report "
            "printed. A comparative restated in a later edition is a different "
            "claim - it may rest on a revised definition, a restated perimeter "
            "or a corrected prior figure - so it is recorded here rather than "
            "substituted into the year it refers to."
        )

    if own.excluded:
        bits = " ".join(
            f"{r.get('year')} {r.get('measure')}"
            + (f" = {r['value']}" if r.get("value") else "") + ": "
            + str(r.get("note") or r.get("finding")
                  or "excluded, no reason recorded")
            for r in own.excluded)
        paras.append("RULED OUT, AND RECORDED SO IT IS NOT RE-DERIVED. " + bits)

    if extra_note:
        paras.append(extra_note)
    return "\n\n".join(paras)


def _profitability_sources(bw, published_key, pat_label, eq_label, as_label,
                           balance_sheet, income_sheet, has_published,
                           extra_sources, equity_series_source=""):
    parts = [
        f"Computed by this workbook's own build script from the {income_sheet} "
        f"and {balance_sheet} sheets of this same workbook - the "
        f"{income_sheet} row “{pat_label}” and the {balance_sheet} "
        f"rows “{eq_label}” and “{as_label}”, resolved BY "
        f"LABEL at build time through the shared resolver "
        f"scripts/profitability_rows.py, so this sheet cannot drift from the "
        f"statements it summarises. Those rows are themselves transcribed from "
        f"{bw.bank_name}'s Annual Report and Accounts for each year; see the "
        f"source cells on the {balance_sheet} and {income_sheet} sheets for "
        f"the exact document, page and table behind every input to every "
        f"percentage above."
    ]
    if has_published:
        parts.append(
            f"The '(as published)' rows are quoted verbatim from "
            f"{bw.bank_name}'s own disclosures and are recorded, with the "
            f"exact document, page and verification state for each, in "
            f"research/profitability/published_returns.jsonl under "
            f"‘{published_key}’."
        )
    else:
        parts.append(
            f"The finding that {bw.bank_name} publishes no return of its own "
            f"is recorded in research/profitability/published_returns.jsonl "
            f"under ‘{published_key}’, verified against the bank's "
            f"own annual report rendered at 300 dpi."
        )
    if equity_series_source:
        parts.append(
            "WHERE THE EQUITY DENOMINATOR COMES FROM. This bank's own "
            "Statement of Financial Position prints no total-equity line, so "
            "the equity figures behind the ratios above were not resolved off "
            "the Balance Sheet sheet like every other bank's. " +
            equity_series_source)
    if extra_sources:
        parts.append(extra_sources)
    return "\n\n".join(parts)


# -- Overview derivation spec (standing objective (b)) -------------------------
# The Overview's money blocks are DERIVED from the detail sheets, resolved by
# the row's own label. This table covers the rows where that is not enough,
# and it is deliberately explicit rather than inferred at build time:
#
#   (bank_name, detail sheet, normalised Overview label) -> either
#       "detail row label"            - the Overview renames the row, or
#       ("row a", "row b", ...)       - the Overview AGGREGATES several rows
#                                       the detail sheet never totals itself.
#
# Discovered once by value-matching each unresolved Overview row against its
# detail sheet (see scripts/derive_overview_spec.py), then reviewed by hand.
# Inferring the mapping at every build would defeat the point: the match is
# made against the very literals being replaced, so it would silently fall
# back to the stale value the moment a detail sheet was corrected.
#   OVERVIEW_KEEP_LITERAL         - not derivable; the Overview figure
#                                   matches no detail row by label or by
#                                   value, and inventing a derivation would
#                                   be worse than leaving the disagreement
#                                   visible. Recorded, never silent.
OVERVIEW_KEEP_LITERAL = "<keep literal - see ticket>"

OVERVIEW_SPEC = {}

try:  # kept in its own module so this file stays the library, not the data
    from overview_spec import OVERVIEW_SPEC as _SPEC

    OVERVIEW_SPEC = _SPEC
except ImportError:  # pragma: no cover - spec not generated yet
    pass

# Populated in discovery runs only; see scripts/derive_overview_spec.py.
_unresolved = []

# Every Overview cell where the DERIVED value differs from the literal the
# build script passed. Each one is either a drift the derivation has just
# corrected, or a sign the mapping is wrong - so they are recorded and
# reviewed, never assumed to be improvements. See check_overview_derivation.py.
_derived_diffs = []

# Overview cells kept as literals because the DETAIL sheet has no value for
# that year - the detail sheet is the gap. See _keep_what_detail_lacks.
_detail_gaps = []


class BankWorkbook:
    def __init__(self, bank_name, years, year_label=None, header_color="0A2540"):
        """
        bank_name: used as the "<Bank Name> — <Sheet>" title on metric sheets.
        years: list of year keys (e.g. "FY2025"), most recent first - this
            order drives column order on every sheet.
        year_label: optional {year_key: column_header_text} override, e.g. to
            append entity/period flags like "FY2024*". Defaults to the key.
        header_color: hex fill color (no '#') for the header row - vary this
            per bank so workbooks are visually distinguishable.
        """
        self.bank_name = bank_name
        self.years = years
        self.year_label = year_label or {y: y for y in years}
        self.header_fill = PatternFill(
            start_color=header_color, end_color=header_color, fill_type="solid"
        )
        self.header_font = Font(color="FFFFFF", bold=True)
        self.wb = openpyxl.Workbook()
        self._first_sheet_used = False
        # Objective (b): the Overview's money blocks and ratio block are
        # DERIVED from the detail sheets rather than hand-copied alongside
        # them. Every detail sheet records its rows here as it is built, and
        # add_overview_sheet - which all 145 build scripts call LAST, after
        # every detail sheet exists - reads values back out of it.
        self._detail_rows = {}   # sheet name -> {normalised label: {year: value}}
        self._sheet_units = {}   # sheet name -> the unit_suffix it printed

        self._metric_rows = {}   # metric sheet name -> [(label, {year: value})]

    # -- internal styling helpers -------------------------------------------------
    def _style_header(self, ws, row, ncols):
        for c in range(1, ncols + 1):
            cell = ws.cell(row=row, column=c)
            cell.fill = self.header_fill
            cell.font = self.header_font
            cell.alignment = Alignment(
                horizontal="left", vertical="center", wrap_text=True
            )

    def _autosize(self, ws, widths):
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w

    @staticmethod
    def _fit_height(text, width_units):
        """Points of row height needed to DISPLAY `text` wrapped across a
        merged cell `width_units` wide. Returns None when it cannot tell.

        An explicit row height disables Excel's auto-fit, so whatever does not
        fit is simply not shown - the text stays in the cell and in the
        formula bar, but never reaches the page a reader opens. That is
        GA-030: 1,743 such cells across 140 of 145 workbooks, because call
        sites hardcoded a height and the notes then grew underneath it.

        Auto-fit cannot be the answer here. Measured in Excel 2026-10-10:
        `autofit` on a MERGED cell collapses the row to a single line (15pt),
        which is the documented merged-cell limitation - so these rows must
        carry an explicit height, and that height has to be computed.

        The two constants below were MEASURED, not modelled: a grid of text
        lengths against column widths was auto-fitted by Excel itself and the
        resulting heights read back. The earlier estimate in the GA-030
        detector (12pt per line, 1.22 chars per width unit) was wrong in both
        terms and understated capacity by about 8%.

        Excel refuses heights above ~409.5 through its UI and its scripting
        API, but it RENDERS whatever a file gives it: a workbook storing 1700
        lays out at 1700 (verified by reading back row positions, which
        accumulate exactly). So a long note needs no splitting across rows -
        one tall row displays it.
        """
        if not text or not width_units:
            return None
        chars_per_line = max(10, int(width_units * CHARS_PER_WIDTH_UNIT))
        lines = 0
        for para in str(text).split("\n"):
            if not para.strip():
                lines += 1
                continue
            used = 0
            for token in para.split(" "):
                need = len(token) + (1 if used else 0)
                if used and used + need > chars_per_line:
                    lines += 1
                    used = len(token)
                else:
                    used += need
                # an unbreakable token - a URL - takes whole lines of its own
                # rather than being averaged away across the paragraph
                while used > chars_per_line:
                    lines += 1
                    used -= chars_per_line
            lines += 1
        return max(MIN_FITTED_HEIGHT, round(lines * WRAPPED_LINE_POINTS, 1))

    @classmethod
    def _split_to_height(cls, text, width_units, max_height=MAX_DISPLAY_HEIGHT):
        """Partition `text` so each piece displays within `max_height`.

        A PARTITION, never a reflow: each piece is a substring cut at a
        paragraph break, then a sentence end, then a space - the same
        preference order `_split_source_text` uses for the storage cap. No
        character is added, removed or re-wrapped, so the citation text is
        the text, just distributed over several rows.
        """
        if not text or not width_units:
            return [text]
        chunks = []
        rest = text
        while cls._fit_height(rest, width_units) > max_height:
            # largest prefix that still fits, then back off to a boundary
            lo, hi = 1, len(rest)
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if cls._fit_height(rest[:mid], width_units) <= max_height:
                    lo = mid
                else:
                    hi = mid - 1
            cut = lo
            window = rest[:cut]
            para = window.rfind("\n")
            sentence = max(window.rfind(". "), window.rfind("; "))
            space = window.rfind(" ")
            if para > cut // 2:
                cut = para + 1
            elif sentence > cut // 2:
                cut = sentence + 1
            elif space > cut // 2:
                cut = space + 1
            # else: no breakable point - hard cut rather than lose text
            chunks.append(rest[:cut].rstrip())
            rest = rest[cut:].lstrip()
            if not rest:
                return chunks
        chunks.append(rest)
        return chunks

    @classmethod
    def _write_merged_text_block(
        cls, ws, row, ncols, text, font, width_units, step=2
    ):
        """Write `text` across as many merged, wrapped rows as it needs.

        Returns the first row AFTER the block. `step` is the row stride
        between pieces - the source cell has always left a blank row between
        continuations, and that is preserved.
        """
        chunks = cls._split_to_height(text, width_units)
        written = []
        for i, chunk in enumerate(chunks):
            r = row + step * i
            value = chunk if i == 0 else "(continued)\n" + chunk
            cell = ws.cell(row=r, column=1, value=value)
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncols)
            cell.font = font
            cell.alignment = Alignment(
                wrap_text=True, vertical="top", horizontal="left"
            )
            ws.row_dimensions[r].height = cls._fitted(
                MIN_FITTED_HEIGHT, value, width_units
            )
            written.append(r)
        return (written[-1] if written else row) + 1

    @classmethod
    def _fitted(cls, requested, text, width_units):
        """The taller of what the call site asked for and what the text needs.

        Deliberately a floor, not an override: a call site may still ask for a
        roomier row, but it can no longer ask for one that hides its own
        content. This is what makes the ~1,200 hardcoded heights already in
        the build scripts safe to leave exactly as they are.
        """
        fit = cls._fit_height(text, width_units)
        if fit is None:
            return requested
        # Capped at the display limit, because text that needs more than one
        # row's worth now SPILLS into further rows instead of growing the
        # row. That makes the oversized hand-set heights from before the
        # spill (1700, 1580, ...) obsolete rather than wrong: they are
        # honoured only up to the cap, and the text they were protecting is
        # now carried by the extra rows.
        return min(max(requested or 0, fit), MAX_DISPLAY_HEIGHT)

    @staticmethod
    def _split_source_text(text, limit=SOURCE_CELL_LIMIT):
        """Split citation text into cell-sized chunks, longest-first.

        Prefers a paragraph break, then a sentence end, then a space, so a
        chunk never ends mid-word and a citation is never cut mid-figure.
        Returns [text] unchanged when it already fits, which is the case for
        all but two of the 145 workbooks - the one-cell form stays the
        default and its output stays byte-identical.
        """
        if not text or len(text) <= limit:
            return [text]
        chunks = []
        rest = text
        while len(rest) > limit:
            window = rest[:limit]
            cut = window.rfind("\n")
            if cut < limit // 2:
                cut = max(window.rfind(". "), window.rfind("; "))
                cut = cut + 1 if cut >= limit // 2 else -1
            if cut < limit // 2:
                cut = window.rfind(" ")
            if cut < limit // 2:  # no breakable point - hard cut rather than lose text
                cut = limit
            chunks.append(rest[:cut].rstrip())
            rest = rest[cut:].lstrip()
        chunks.append(rest)
        return chunks

    def _write_source_cell(self, ws, row, ncols, text, height=150, width_units=None):
        # openpyxl silently truncates any cell string past 32,767 chars (its
        # own hard limit) rather than raising - caught the hard way in HD-078
        # (Co-operative Bank), where citation text had grown past it unnoticed.
        #
        # Raising was the right call while that was the only option, but by
        # 2026-10-08 it had become a blocker rather than a guard (GA-025): UBP
        # UK sat at 99.9% of the cap and Co-operative Bank at 99.3%, so the
        # next substantive note on either would fail the build, and the way
        # through a failing build is to compact prose - which is invisible
        # afterwards, because NOTHING in this repo reads a source cell. A
        # trim that drops a folio citation passes all four checks.
        #
        # So the text now CONTINUES into further cells instead (user decision,
        # 2026-10-08). Nothing is lost and nothing is silent: the split is
        # announced on stderr, because a note crossing the cap is worth
        # knowing about even though it is no longer fatal.
        # Two separate caps apply, and only the first is about storage.
        # SOURCE_CELL_LIMIT is openpyxl's; MAX_DISPLAY_HEIGHT is how much one
        # row can show a reader who can still resize it by hand. Splitting on
        # the display cap subsumes the storage one at every width this repo
        # uses, so the storage split only runs when the width is unknown.
        if width_units:
            chunks = self._split_to_height(text, width_units)
        else:
            chunks = self._split_source_text(text)
        if len(chunks) > 1:
            print(
                f"note: source citation for sheet {ws.title!r} is "
                f"{len(text)} chars - continued across {len(chunks)} cells.",
                file=sys.stderr,
            )
        for i, chunk in enumerate(chunks):
            r = row + 2 * i
            value = chunk if i == 0 else "(continued)\n" + chunk
            cell = ws.cell(row=r, column=1, value=value)
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncols)
            cell.font = SOURCE_FONT
            cell.alignment = Alignment(
                wrap_text=True, vertical="top", horizontal="left"
            )
            ws.row_dimensions[r].height = self._fitted(height, value, width_units)

    def append_source_cell(self, ws, text, ncols=None, height=150):
        """Add a FURTHER merged source-citation cell below the one a sheet
        already has.

        Every sheet ends in a single merged citation cell, and openpyxl caps a
        cell at 32,767 characters - a ceiling the Co-operative Bank's shared
        statement-source block had already grown to within a few hundred
        characters of by 2026-09-19, which left no room to cite the 31 newly
        filled Profit & Loss years. Splitting the citation across two adjacent
        cells keeps every source on the sheet that uses it rather than pushing
        provenance out into a file the reader of the workbook never sees.

        Use this only when one cell genuinely cannot hold the citation; the
        one-cell form stays the default.
        """
        if ncols is None:
            ncols = ws.max_column
        self._write_source_cell(
            ws, ws.max_row + 2, ncols, text, height=height,
            width_units=self._width_units(ws, ncols),
        )
        return ws

    @staticmethod
    def _width_units(ws, ncols):
        """Total width of columns 1..ncols, read back off the sheet.

        Only usable AFTER _autosize has run; the sheet builders pass their
        widths list directly instead, because they set the source cell before
        sizing their columns.
        """
        total = 0.0
        for i in range(1, ncols + 1):
            dim = ws.column_dimensions.get(get_column_letter(i))
            total += (dim.width if dim is not None and dim.width else 8.43)
        return total

    def _style_chart_axes(self, chart):
        # openpyxl's TextAxis/NumericAxis both default axPos to "l", which
        # puts the category axis on top of the value axis - fix the category
        # (x) axis onto the bottom and make sure both axes actually draw
        # their tick labels and lines.
        chart.x_axis.axPos = "b"
        chart.y_axis.axPos = "l"
        chart.x_axis.tickLblPos = "nextTo"
        chart.y_axis.tickLblPos = "nextTo"
        chart.x_axis.delete = False
        chart.y_axis.delete = False
        chart.x_axis.majorTickMark = "out"
        chart.y_axis.majorTickMark = "out"

    def _reserve_bottom_legend(self, chart, legend_h, plot_h, plot_top=0.12):
        # Pin the legend to its own band at the very bottom of the chart
        # area and explicitly shrink the plotting rectangle above it, so
        # Excel's automatic layout can't let a wrapped multi-line legend
        # encroach on the axis tick labels above it.
        chart.legend.layout = Layout(
            manualLayout=ManualLayout(
                xMode="edge",
                yMode="edge",
                x=0.02,
                y=1.0 - legend_h,
                h=legend_h,
                w=0.96,
            )
        )
        # ChartBase._write() overwrites plot_area.layout with chart.layout at
        # save time, so the plot rectangle must be set here, not on plot_area.
        chart.layout = Layout(
            manualLayout=ManualLayout(
                layoutTarget="inner",
                xMode="edge",
                yMode="edge",
                x=0.10,
                y=plot_top,
                w=0.85,
                h=plot_h,
            )
        )

    # -- Overview derivation (standing objective (b)) --------------------------
    def _record_detail_rows(self, sheet_name, rows):
        """Remember a statement sheet's rows so the Overview can derive from
        them. First occurrence of a label wins: a few sheets print the same
        label twice (a section subtotal equal to the sheet total), and the
        Overview means the first one."""
        table = self._detail_rows.setdefault(sheet_name, {})
        for kind, label, values in rows:
            if kind == "SECTION":
                continue
            table.setdefault(_norm_label(label), dict(values))

    def _derive_block(self, sheet_name, rows, block, years=None):
        """Replace each Overview row's hand-passed values with the detail
        sheet's own, so the two cannot drift apart.

        The passed values are used ONLY to discover the mapping the first
        time (see OVERVIEW_SPEC); thereafter the detail sheet is the single
        authority. Resolution order: the row's own label, then an explicit
        alias, then an explicit SUM of detail rows. A row that resolves to
        none of those raises - it is never silently left as a literal,
        because a silent fallback is exactly the drift this removes.
        """
        table = self._detail_rows.get(sheet_name)
        if table is None:
            return rows  # workbook has no such detail sheet; nothing to derive
        out = []
        for label, values in rows:
            key = _norm_label(label)
            spec = OVERVIEW_SPEC.get((self.bank_name, sheet_name, key))
            if key in table and spec is None:
                out.append((label, dict(table[key])))
            elif spec is None:
                out.append((label, dict(values)))
                _unresolved.append(
                    (self.bank_name, sheet_name, block, label, dict(values),
                     {k: dict(v) for k, v in table.items()},
                     list(years) if years else None)
                )
            elif spec == OVERVIEW_KEEP_LITERAL:
                # Deliberately NOT derived, and never silently: the Overview
                # figure matches no row on the detail sheet by label or by
                # value, so there is nothing honest to derive it from. The
                # literal stands until the disagreement is settled against
                # the bank's own document.
                out.append((label, dict(values)))
            elif isinstance(spec, str):
                if _norm_label(spec) not in table:
                    raise ValueError(
                        f"{self.bank_name}: Overview row {label!r} is aliased "
                        f"to {spec!r} on {sheet_name}, which has no such row"
                    )
                out.append((label, dict(table[_norm_label(spec)])))
            else:
                out.append((label, self._sum_rows(sheet_name, table, spec, label)))
            label_out, derived = out[-1]
            if spec != OVERVIEW_KEEP_LITERAL:
                derived = self._keep_what_detail_lacks(
                    sheet_name, label, values, derived, years
                )
                out[-1] = (label_out, derived)
            self._record_derived_diff(
                sheet_name, label, values, derived, years
            )
        return out

    def _keep_what_detail_lacks(self, sheet_name, label, passed, derived,
                                years):
        """Derive every year the detail sheet HAS; keep the literal for any
        year it does not.

        Blanking a figure the Overview already shows would be a worse
        outcome than the drift this removes - and the cases are real: Bank
        of Beirut's Overview carries an FY2017 cash balance its Cash Flow
        Statement has no FY2017 column for. The detail sheet is the gap
        there, not the Overview, so the figure stays and the gap is
        RECORDED rather than quietly closed by deletion.

        check_overview_ties.py reports none of these (its section B is
        empty) because it only compares rows whose labels match exactly,
        and every one of these reaches its detail row through an alias.
        """
        merged = dict(derived)
        scope = set(years) if years else set(passed)
        for year, value in passed.items():
            if value is None or year not in scope:
                continue
            if merged.get(year) is None:
                merged[year] = value
                _detail_gaps.append(
                    (self.bank_name, sheet_name, label, year, value)
                )
        return merged

    def _record_derived_diff(self, sheet_name, label, passed, derived,
                             years=None):
        # only years the Overview actually PRINTS matter; a column the
        # per-block year trim drops is not a change a reader can see
        scope = set(years) if years else set(passed) | set(derived)
        for year in sorted((set(passed) | set(derived)) & scope):
            was, now = passed.get(year), derived.get(year)
            if isinstance(was, (int, float)) and isinstance(now, (int, float)):
                if abs(was - now) <= max(abs(was), abs(now), 1) * 1e-9:
                    continue
            elif was == now:
                continue
            _derived_diffs.append(
                (self.bank_name, sheet_name, label, year, was, now)
            )

    def _sum_rows(self, sheet_name, table, parts, label):
        """An Overview row that is an AGGREGATE the detail sheet never prints
        as a single line - e.g. 'total operating expense' summed from staff
        costs, other operating expenses and depreciation.

        A part may be a bare label, or a (label, coefficient) pair. The
        coefficient exists because one bank states the quantity as a
        RESIDUAL rather than a sum: Jordan International Bank's total
        operating expense is its total operating income less its profit
        before taxation, which no addition of printed rows reproduces.
        """
        pairs = [(p, 1) if isinstance(p, str) else (p[0], p[1]) for p in parts]
        missing = [p for p, _ in pairs if _norm_label(p) not in table]
        if missing:
            raise ValueError(
                f"{self.bank_name}: Overview row {label!r} sums rows that do "
                f"not exist on {sheet_name}: {missing}"
            )
        totals = {}
        for part, coeff in pairs:
            for year, value in table[_norm_label(part)].items():
                if isinstance(value, (int, float)):
                    totals[year] = totals.get(year, 0) + coeff * value
        # a float sum of printed figures carries binary noise; the detail
        # sheets print at most one decimal place
        return {y: round(v, 4) for y, v in totals.items()}

    def _derive_ratios(self, ratios, years=None):
        """The ratio block names the single-metric SHEETS, so each row takes
        that sheet's first value PRINTED AS A PERCENTAGE.

        "Printed as a percentage" means the cell carries a per-cent sign, and
        nothing weaker. `_parse_percent` is the wrong test here and using it
        was a real defect: it returns a float for ANY number, so it accepted
        the HQLA/exposure/funding amount these sheets lead with, and the
        Overview's LCR row took ABC International's 748.628 (HQLA, in
        millions) in place of its 250.1%. That is the trap CLAUDE.md names
        for exactly these three sheets, and check_overview_ties.py avoids it
        with the `"%" in str(v)` rule this now mirrors - deliberately the
        same rule, not a second guess at it.

        A year the metric sheet cannot supply keeps its literal, for the same
        reason `_keep_what_detail_lacks` exists: blanking a figure a reader
        can see today is worse than the drift derivation removes.
        """
        out = []
        for label, values in ratios:
            rows = self._metric_rows.get(label)
            if not rows:
                out.append((label, dict(values)))
                continue
            derived = {}
            for year in set().union(*(r[1].keys() for r in rows)):
                for _rl, rv in rows:
                    cell = rv.get(year)
                    if cell is not None and "%" in str(cell):
                        derived[year] = cell
                        break
            derived = self._keep_what_detail_lacks(
                label, label, values, derived, years
            )
            self._record_derived_diff(label, label, values, derived, years)
            out.append((label, derived))
        return out

    def _next_sheet(self, name):
        if not self._first_sheet_used:
            ws = self.wb.active
            ws.title = name[:31]
            self._first_sheet_used = True
            return ws
        return self.wb.create_sheet(title=name[:31])

    @staticmethod
    def _has_value(v):
        """True if a cell would print something a reader can read.

        A dash counts. The user's decision of 2026-09-18 is that a printed
        dash stays on the sheet as a literal "-", because it is the bank
        SAYING something ("this row does not apply to us") and is a different
        statement from silence. So a year whose only content is dashes is a
        year the bank published, and must keep its column.
        """
        if v is None:
            return False
        return not (isinstance(v, str) and not v.strip())

    def _trim_trailing_empty_years(self, years, value_dicts):
        """Drop year columns off the OLDEST end that no row on this sheet fills.

        The user's instruction of 2026-09-17 (`bank_probs.txt` general point 1,
        naming Alrayan's KM1, which printed FY2021 and FY2020 headers over two
        entirely empty columns):

            If no Km1 for 2021 and earlier, please dont put header for them in
            spreadsheet

        and the scope decision of 2026-09-18: **trailing only, and on every
        sheet, not only KM1.** The reason a column is empty at the old end is
        the same on every sheet - the disclosure did not exist that far back -
        so the treatment is the same on every sheet.

        TRAILING ONLY IS THE WHOLE POINT, AND THE ASYMMETRY IS DELIBERATE.
        An empty column at the NEWEST end means something completely
        different: the bank has very probably published and we have not
        transcribed it yet. Suppressing that would hide a real gap behind a
        tidy sheet, which is the opposite of what the reader needs - see
        `wayfinder/gaps/map.md`, where the corpus split 662 leading
        sheet-years (real gaps to chase) against 1,881 trailing ones (correct
        as they are). Leading empties keep their headers so they stay visible.

        A sheet where EVERY year is empty is left alone. Such a sheet is all
        leading and all trailing at once, and the honest reading is that it is
        a data gap rather than a presentation problem, so it keeps its columns
        and stays visible. Trimming it would leave a one-column sheet.

        Per-sheet, not per-workbook: year columns may therefore stop at
        different places on different sheets of one workbook. That is intended
        - every column carries its own year label, and no sheet should print a
        header it cannot fill.
        """
        dicts = [d for d in value_dicts if d]
        trimmed = list(years)
        while trimmed:
            if any(self._has_value(d.get(trimmed[-1])) for d in dicts):
                break
            trimmed.pop()
        return trimmed if trimmed else list(years)

    def patch_year_column(self, sheet_name, year, values_by_label, header_row=3):
        """Write one year's values into an ALREADY-BUILT sheet, by row label.

        Three scripts supply a year out-of-band rather than in `rows` - Bank of
        Beirut UK, Gatehouse and National Bank of Egypt UK all carry an FY2017
        block bolted on after the sheet is built, because that year comes from a
        different source than the rest. Each used to compute its target column
        as `1 + YEARS.index(year) + 1`.

        THAT BROKE THE MOMENT COLUMN TRIMMING LANDED, and it broke SILENTLY,
        which is the part worth remembering. `_trim_trailing_empty_years` looks
        at `rows`; a year supplied afterwards is invisible to it, so the column
        was trimmed away and the patch then wrote its values into the cell
        position the year USED to occupy - past the end of the header. The
        figures were still in the file, in a column with no year above them: 98
        cells across the three banks, present, plausible, and unlabelled.

        An index computed from one list and applied to another is only correct
        while nothing can change either list. Resolve the column from the sheet
        as it actually is, and if the year is not there, put it there.
        """
        ws = self.wb[sheet_name]
        headers = [ws.cell(row=header_row, column=c).value
                   for c in range(1, ws.max_column + 1)]
        want = self.year_label.get(year, year)
        col = None
        for i, h in enumerate(headers, start=1):
            # the header may carry a unit suffix - "FY2017 (£'000)" - so match
            # on the label being present rather than on equality
            if h is not None and str(want) in str(h):
                col = i
                break
        if col is None:
            # the year was trimmed (or never built): re-create the column,
            # copying the unit suffix from the neighbouring header so the new
            # one reads the same way as the rest of the row
            col = len(headers) + 1
            suffix = ""
            for h in reversed(headers):
                if h is None:
                    continue
                m = re.search(r"\((.*)\)\s*$", str(h))
                if m:
                    suffix = f" ({m.group(1)})"
                break
            ws.cell(row=header_row, column=col, value=f"{want}{suffix}")
            # reuse the sheet's own header styling rather than re-deriving it,
            # so a restored column is indistinguishable from an original one
            self._style_header(ws, header_row, col)
            ws.cell(row=header_row, column=col).border = BORDER

        labels = {str(ws.cell(row=r, column=1).value).strip(): r
                  for r in range(header_row + 1, ws.max_row + 1)}
        written = 0
        for label, value in values_by_label.items():
            r = labels.get(str(label).strip())
            if r is not None:
                ws.cell(row=r, column=col, value=value)
                ws.cell(row=r, column=col).border = BORDER
                written += 1
        return written

    def _assert_no_orphan_columns(self):
        """Refuse to save a sheet holding data in a column with no header.

        The failure this exists for wrote real figures into unlabelled columns
        and nothing complained: not `verify_workbook.py`, which reads headers
        out to `max_column` and simply reported `None` where a year should be;
        not `check_builds_current.py`, which only compares timestamps; not
        `audit_gaps.py`, which counts cells under headers it can name and so
        never saw them at all. A silent orphan beats every instrument in this
        repo, so the check belongs at the point of writing.
        """
        for ws in self.wb.worksheets:
            if ws.max_row < 4:
                continue
            headers = [ws.cell(row=3, column=c).value
                       for c in range(1, ws.max_column + 1)]
            if not headers or headers[0] is None:
                continue  # not a header-row-3 sheet (Overview, equity roll-forward)
            for c in range(len(headers), 0, -1):
                if headers[c - 1] is not None:
                    break
                orphans = [ws.cell(row=r, column=c).value
                           for r in range(4, ws.max_row + 1)]
                orphans = [v for v in orphans
                           if v is not None and str(v).strip() != ""]
                if orphans:
                    raise ValueError(
                        f"{self.bank_name}: sheet {ws.title!r} holds "
                        f"{len(orphans)} value(s) in column {c}, which has no "
                        f"header. A year column was almost certainly trimmed "
                        f"after something computed this column's index from an "
                        f"untrimmed year list - use patch_year_column() instead "
                        f"of an index into YEARS. First value: {orphans[0]!r}"
                    )

    # -- public API -----------------------------------------------------------
    def _add_statement_sheet(
        self,
        title,
        subtitle,
        rows,
        sources_text,
        sheet_name,
        first_col_width,
        source_height,
        unit_suffix,
        years=None,
    ):
        """Shared body for the full-statement sheets (Cash Flow, Balance
        Sheet, Profit & Loss): a title/subtitle, then a header row of years,
        then one row per (kind, label, values) tuple - kind in {"SECTION",
        "DATA", "TOTAL"} - ending in a merged wrapped source-citation cell.

        years: optional override of self.years for this sheet only - use
            when one sheet's historical depth has been extended further back
            than the rest of the workbook (e.g. a statutory-statement-only
            historical-depth extension that deliberately leaves Pillar 3 /
            Asset Quality / RWA Breakdown at the project-wide floor).
        """
        years = years if years is not None else self.years
        years = self._trim_trailing_empty_years(
            years, (values for _kind, _label, values in rows)
        )
        self._record_detail_rows(sheet_name, rows)
        # Remember the unit this sheet printed. A ratio struck across two
        # sheets cancels its unit only if both sides share one, and this is
        # the only place that fact is known.
        self._sheet_units[sheet_name] = unit_suffix
        ws = self._next_sheet(sheet_name)
        ws.freeze_panes = "B4"
        ws["A1"] = title
        ws["A1"].font = TITLE_FONT
        ws["A2"] = subtitle
        ws["A2"].font = SUBTITLE_FONT

        ncols = 1 + len(years)
        headers = ["Line item"] + [
            f"{self.year_label[y]}{unit_suffix}" for y in years
        ]
        header_row = 3
        for c, h in enumerate(headers, start=1):
            ws.cell(row=header_row, column=c, value=h)
        self._style_header(ws, header_row, ncols)

        r = header_row + 1
        for kind, label, values in rows:
            ws.cell(row=r, column=1, value=label)
            if kind == "SECTION":
                ws.cell(row=r, column=1).font = SECTION_FONT
            else:
                for ci, y in enumerate(years, start=2):
                    ws.cell(row=r, column=ci, value=values.get(y))
                if kind == "TOTAL":
                    for c in range(1, ncols + 1):
                        ws.cell(row=r, column=c).font = TOTAL_FONT
            for c in range(1, ncols + 1):
                ws.cell(row=r, column=c).border = BORDER
            r += 1

        widths = [first_col_width] + [15] * len(years)
        self._write_source_cell(
            ws, r + 1, ncols, sources_text, height=source_height,
            width_units=sum(widths),
        )
        self._autosize(ws, widths)
        return ws

    def add_cash_flow_sheet(
        self,
        title,
        subtitle,
        rows,
        sources_text,
        sheet_name="Cash Flow Statement",
        first_col_width=60,
        source_height=150,
        unit_suffix=" (£'000)",
        years=None,
    ):
        """
        rows: list of (kind, label, values) - kind in {"SECTION", "DATA", "TOTAL"}.
        years: optional override of self.years for this sheet only - see
            _add_statement_sheet's docstring.
        """
        return self._add_statement_sheet(
            title,
            subtitle,
            rows,
            sources_text,
            sheet_name,
            first_col_width,
            source_height,
            unit_suffix,
            years=years,
        )

    def add_balance_sheet_sheet(
        self,
        title,
        subtitle,
        rows,
        sources_text,
        sheet_name="Balance Sheet",
        first_col_width=60,
        source_height=150,
        unit_suffix=" (£'000)",
        years=None,
    ):
        """Consolidated Statement of Financial Position. Same row/column
        shape as add_cash_flow_sheet - see that docstring for `rows`/`years`."""
        return self._add_statement_sheet(
            title,
            subtitle,
            rows,
            sources_text,
            sheet_name,
            first_col_width,
            source_height,
            unit_suffix,
            years=years,
        )

    def add_income_statement_sheet(
        self,
        title,
        subtitle,
        rows,
        sources_text,
        sheet_name="Profit & Loss",
        first_col_width=60,
        source_height=150,
        unit_suffix=" (£'000)",
        years=None,
    ):
        """Consolidated Statement of Comprehensive Income. Same row/column
        shape as add_cash_flow_sheet - see that docstring for `rows`/`years`."""
        return self._add_statement_sheet(
            title,
            subtitle,
            rows,
            sources_text,
            sheet_name,
            first_col_width,
            source_height,
            unit_suffix,
            years=years,
        )

    def add_equity_changes_sheet(
        self,
        title,
        subtitle,
        headers,
        rows,
        sources_text,
        sheet_name="Statement of Changes in Equity",
        first_col_width=46,
        source_height=150,
        col_width=15,
    ):
        """Consolidated Statement of Changes in Equity.

        Unlike every other statement sheet, this one doesn't fit the
        year-column shape - it's an equity-component-column, movement-row
        roll-forward, read chronologically oldest-to-newest (opening
        balance, this year's movements, closing balance, next year's
        movements, ...), not most-recent-first like the rest of the
        workbook.

        headers: list of equity component names (e.g. "Share capital",
            "Share premium", "Other reserves", "Merger reserve", "Retained
            losses", "Total equity") - becomes the column headers after the
            leading "Movement" label column.
        rows: list of (kind, label, values) - kind in {"DATA", "TOTAL"};
            TOTAL bolds the row (use it for balance-brought/carried-forward
            rows and "Total comprehensive income/(loss) for the year" rows).
            `values` is a tuple/list positionally aligned to `headers`
            (not a year dict) - use None for a component not applicable to
            that row (e.g. Merger reserve before it existed).
        """
        ws = self._next_sheet(sheet_name)
        ws.freeze_panes = "A5"
        ws["A1"] = title
        ws["A1"].font = TITLE_FONT
        ws["A2"] = subtitle
        ws["A2"].font = SUBTITLE_FONT

        ncols = 1 + len(headers)
        col_headers = ["Movement"] + list(headers)
        header_row = 3
        for c, h in enumerate(col_headers, start=1):
            ws.cell(row=header_row, column=c, value=h)
        self._style_header(ws, header_row, ncols)

        r = header_row + 1
        for kind, label, values in rows:
            ws.cell(row=r, column=1, value=label)
            for ci, v in enumerate(values, start=2):
                ws.cell(row=r, column=ci, value=v)
            if kind == "TOTAL":
                for c in range(1, ncols + 1):
                    ws.cell(row=r, column=c).font = TOTAL_FONT
            for c in range(1, ncols + 1):
                ws.cell(row=r, column=c).border = BORDER
            r += 1

        widths = [first_col_width] + [col_width] * len(headers)
        self._write_source_cell(
            ws, r + 1, ncols, sources_text, height=source_height,
            width_units=sum(widths),
        )
        self._autosize(ws, widths)
        return ws

    def add_asset_quality_sheet(
        self,
        title,
        subtitle,
        rows,
        sources_text,
        sheet_name="Asset Quality",
        first_col_width=58,
        source_height=150,
        unit_suffix=" (£'000)",
        years=None,
    ):
        """Asset Quality / Credit Risk Disclosures: loan book breakdown by
        product and by IFRS 9 stage (1/2/3), plus derived coverage/NPL
        ratios. Same year-column row/column shape as add_cash_flow_sheet -
        see that docstring for `rows`. Ratio rows may use string values
        (e.g. "13.55%") the same way add_metric_sheet does. Placed right
        after Cash Flow Statement and right before the Pillar 3 sheets.
        years: optional per-sheet override - see _add_statement_sheet."""
        return self._add_statement_sheet(
            title,
            subtitle,
            rows,
            sources_text,
            sheet_name,
            first_col_width,
            source_height,
            unit_suffix,
            years=years,
        )

    def add_rwa_breakdown_sheet(
        self,
        title,
        subtitle,
        rows,
        sources_text,
        sheet_name="RWA Breakdown",
        first_col_width=54,
        source_height=150,
        unit_suffix=" (£'000)",
        years=None,
    ):
        """RWA breakdown by risk category (Pillar 3's UK OV1 template:
        credit risk, counterparty credit risk, securitisation, market risk,
        operational risk). Same year-column row/column shape as
        add_cash_flow_sheet - see that docstring for `rows`. Placed with the
        other Pillar 3 sheets (see PILLAR3_SHEET_NAMES), not with the other
        3 statement sheets, since it's itself a Pillar 3 disclosure.
        years: optional per-sheet override - see _add_statement_sheet."""
        return self._add_statement_sheet(
            title,
            subtitle,
            rows,
            sources_text,
            sheet_name,
            first_col_width,
            source_height,
            unit_suffix,
            years=years,
        )

    # -- Profitability (derived) ----------------------------------------------
    def add_profitability_sheet(
        self,
        published_key,
        fx_basis=_FX_FROM_TABLE,
        *,
        balance_sheet="Balance Sheet",
        income_sheet="Profit & Loss",
        sheet_name=PROFITABILITY_SHEET_NAME,
        extra_note="",
        extra_sources="",
        equity_series=None,
        equity_series_source="",
        store_path=None,
    ):
        """Return on equity and return on assets, DERIVED from this workbook.

        Nothing on this sheet is transcribed. Every percentage is computed
        from the 'profit for the year', 'total equity' and 'total assets'
        rows this workbook already prints, resolved out of `_detail_rows` at
        build time, so the sheet cannot drift from the statements it
        summarises - the Overview duplication defect (GA-031) in a new place.
        The inputs are deliberately NOT reprinted: they are already in full on
        the Balance Sheet and Profit & Loss sheets.

        Rows are resolved by `profitability_rows.pick`, the SAME code the
        research table uses, rather than by a label restated here. That is the
        rule the Overview ratio defect bought: when two pieces of code must
        apply the same rule, call the same code.

        `published_key` is the bank's key in published_returns.jsonl (the
        workbook filename without " FINANCIALS.xlsx"). It is required and not
        guessed: the store records, per bank, either the returns the bank
        publishes ITSELF or the positive finding that it publishes none, and
        both belong on this sheet. A key with no record raises, because a
        silent blank there would read as "publishes nothing" - which is a
        FINDING, and must come from the store, not from a lookup miss.

        Whether a ratio struck across the two sheets cancels its units is
        LOOKED UP in scripts/profitability_fx_basis.py by `published_key`,
        not inferred - read that file's header for why no code scan and no
        printed unit can establish it. A converted workbook missing from that
        table RAISES rather than computing. `fx_basis` exists only to settle a
        bank the table does not yet cover, and passing one that CONTRADICTS
        the table also raises:
            None            - the sheets are in one native currency
            "cancels"       - converted, but both sides on the same basis
            "mixed"         - every year's ratio is contaminated
            {"FY20xx", ...} - only these years are contaminated
        Where a year is contaminated the cell says "Not computed" and the note
        says why. It is NOT computed-and-caveated: the house rule is that a
        ratio cancels its unit only if both sides share it, so the honest
        output is a refusal. ENTITY_MISMATCH in the same file refuses on the
        separate ground that the two sheets describe different entities, which
        no unit test can see.
        """
        # Imported here, not at module scope, so that the 145 build scripts
        # which never call this keep working if the research tree moves.
        import profitability_rows as _pr
        from profitability_fx_basis import (
            ENTITY_MISMATCH, FX_RATIO_BASIS, NON_ANNUAL_PERIODS)

        bs = self._detail_rows.get(balance_sheet)
        pl = self._detail_rows.get(income_sheet)
        missing = [n for n, t in ((balance_sheet, bs), (income_sheet, pl))
                   if not t]
        if missing:
            raise ValueError(
                f"{self.bank_name}: Profitability derives from "
                f"{', '.join(missing)}, which this workbook has not built "
                f"yet - call add_profitability_sheet AFTER those sheets"
            )

        def _numeric(table):
            """{label: {year: float}} - a printed dash or statement is not a
            number and must not become one."""
            out = {}
            for label, values in table.items():
                vals = {}
                for y, v in values.items():
                    n = _pr.to_num(v)
                    if n is not None:
                        vals[y] = n
                if vals:
                    out[label] = vals
            return out

        years = list(self.years)
        pat_label, pat = _pr.pick(
            _numeric(pl), _pr.PROFIT_PATTERNS, _pr.PROFIT_EXCLUDE, years)
        eq_label, equity = _pr.pick(
            _numeric(bs), _pr.EQUITY_PATTERNS, _pr.EQUITY_EXCLUDE, years)
        as_label, assets = _pr.pick(
            _numeric(bs), _pr.ASSET_PATTERNS, _pr.ASSET_EXCLUDE, years)
        # A handful of banks present equity INSIDE total liabilities and so
        # print no total-equity line on the balance sheet at all - Citibank UK
        # Limited is one, and its own Statement of Changes in Equity still
        # closes to a published total every year. That figure is the bank's,
        # not ours, so it is allowed in; but it bypasses the shared resolver,
        # which is exactly the kind of exception that rots into an unexplained
        # literal, so the provenance is MANDATORY and this raises without it.
        if equity_series is not None:
            if not equity_series_source:
                raise ValueError(
                    f"{self.bank_name}: equity_series bypasses the shared "
                    f"resolver, so equity_series_source must say which "
                    f"statement, row and column the figures come from. An "
                    f"override with no provenance is an unexplained literal"
                )
            eq_label, equity = "(see note)", {
                y: v for y, v in equity_series.items() if v is not None}

        unresolved = [n for n, got in (("profit for the year", pat),
                                       ("total equity", equity),
                                       ("total assets", assets)) if got is None]
        if unresolved:
            raise ValueError(
                f"{self.bank_name}: no row on {income_sheet}/{balance_sheet} "
                f"matches {', '.join(unresolved)} - the Profitability sheet "
                f"would print blanks that read as 'the bank has no such "
                f"figure'. Resolve the label in scripts/profitability_rows.py "
                f"rather than hardcoding it here"
            )

        # -- does a ratio across these two sheets cancel its unit? ------------
        bs_unit = self._sheet_units.get(balance_sheet, "")
        pl_unit = self._sheet_units.get(income_sheet, "")
        if bs_unit != pl_unit:
            raise ValueError(
                f"{self.bank_name}: {balance_sheet} prints {bs_unit!r} and "
                f"{income_sheet} prints {pl_unit!r}. A ratio across them "
                f"divides one unit by another; it does not cancel. Settle the "
                f"two sheets' units before adding a Profitability sheet"
            )
        # The verdict is LOOKED UP, not inferred, and that is the whole point
        # of profitability_fx_basis.py. The tempting shortcut - treat a unit
        # that says "conv. from" as contaminated and a plain unit as clean -
        # was measured against the audited table and catches only 13 of the 18
        # contaminated banks: BANK MANDIRI EUROPE, CREDIT SUISSE INTERNATIONAL,
        # FCMB UK, GOLDMAN SACHS INTERNATIONAL BANK and JP MORGAN SECURITIES
        # all print a plain unit and would have computed, silently, on two
        # different rates. So the table decides, and a converted workbook the
        # table has never been asked about raises rather than guessing.
        verdict = FX_RATIO_BASIS.get(published_key, _FX_UNAUDITED)
        if fx_basis is _FX_FROM_TABLE:
            if verdict is not _FX_UNAUDITED:
                fx_basis = verdict
            elif "conv" in bs_unit.lower():
                raise ValueError(
                    f"{self.bank_name}: both statement sheets print "
                    f"{bs_unit!r}, so these figures were converted, and the "
                    f"house convention converts balance-sheet stocks at the "
                    f"year-end SPOT rate and profit-and-loss flows at that "
                    f"year's AVERAGE rate. Whether a ratio across them "
                    f"cancels therefore cannot be read off the page, and "
                    f"{published_key!r} is not in "
                    f"scripts/profitability_fx_basis.py. Read the build "
                    f"script, add the verdict to that table, and re-run - "
                    f"silence is not an answer here, which is why this raises"
                )
            else:
                fx_basis = None     # one native currency on both sides
        elif verdict is not _FX_UNAUDITED and fx_basis != verdict:
            raise ValueError(
                f"{self.bank_name}: this call passes fx_basis={fx_basis!r}, "
                f"but scripts/profitability_fx_basis.py records "
                f"{verdict!r} for {published_key!r} after reading the build "
                f"script. One of the two is wrong and it is not for this call "
                f"to decide quietly: settle it in the table, which is the "
                f"audited record, and then either drop the argument or make "
                f"it agree"
            )

        if fx_basis in (None, "cancels"):
            refused = set()
        elif fx_basis == "mixed":
            refused = set(years)
        elif isinstance(fx_basis, (set, frozenset, list, tuple)):
            refused = set(fx_basis)
            stray = refused - set(years)
            if stray:
                raise ValueError(
                    f"{self.bank_name}: fx_basis names {sorted(stray)}, which "
                    f"this workbook has no column for - a typo here silently "
                    f"leaves a contaminated year computed"
                )
        else:
            raise ValueError(
                f"{self.bank_name}: fx_basis={fx_basis!r} is not one of None, "
                f"'cancels', 'mixed' or a set of year keys"
            )

        # A unit test cannot see this one. KUWAIT FINANCE HOUSE and STANDARD
        # CHARTERED BANK print the same unit on both sheets, so the ratio
        # cancels perfectly - and still divides a GROUP profit by a SOLO
        # balance sheet, because neither entity publishes a standalone
        # company income statement. A group figure is a different claim
        # (entity discipline), so the ratio is refused on the same grounds as
        # a mixed rate, and the note says which of the two it is.
        fx_refused = set(refused)
        entity_note = ENTITY_MISMATCH.get(published_key)
        if entity_note:
            refused = set(years)

        # -- the arithmetic ---------------------------------------------------
        def prior(year):
            """self.years is most-recent-first, so the prior year is NEXT."""
            i = years.index(year)
            return years[i + 1] if i + 1 < len(years) else None

        def average(series, year):
            """Mean of opening and closing; None without an opening balance.

            The oldest column of any workbook has no prior year, so an
            average-basis ratio cannot exist for it. That blank is structural,
            not a gap to chase."""
            p = prior(year)
            closing, opening = series.get(year), series.get(p) if p else None
            if closing is None or opening is None:
                return None
            return (closing + opening) / 2.0

        def ratio(year, numerator, denominator):
            if year in refused:
                return REFUSED_MIXED_BASIS
            if numerator is None or not denominator:
                return None
            return f"{100.0 * numerator / denominator:.2f}%"

        rows = [
            ("Return on equity - average equity basis",
             {y: ratio(y, pat.get(y), average(equity, y)) for y in years}),
            ("Return on equity - year-end equity basis",
             {y: ratio(y, pat.get(y), equity.get(y)) for y in years}),
            ("Return on assets - average assets basis",
             {y: ratio(y, pat.get(y), average(assets, y)) for y in years}),
            ("Return on assets - year-end assets basis",
             {y: ratio(y, pat.get(y), assets.get(y)) for y in years}),
        ]

        # -- what the bank publishes itself -----------------------------------
        own = _read_published_returns(store_path).get(published_key)
        if own is None:
            raise ValueError(
                f"{self.bank_name}: published_key={published_key!r} is not in "
                f"published_returns.jsonl. That store holds, for every bank, "
                f"either its own published returns or the positive finding "
                f"that it publishes none - and 'publishes none' is a FINDING, "
                f"so it must be read from the store and never inferred from a "
                f"lookup miss"
            )
        if own.published:
            for measure in sorted(own.published):
                values = dict(own.published[measure])
                # A blank on a published row is ambiguous between "the bank
                # did not print this measure that year" and "that year's
                # report was never read for it", and GA-020 does not allow a
                # cell to leave the reader to guess. So a year the store
                # examined and found nothing for says so; a year the store
                # never covered stays blank, and the note names the window.
                for y in years:
                    if y not in values and y in own.examined:
                        values[y] = "Not published"
                rows.append((f"{measure} (as published)", values))
        else:
            rows.append((f"{self.bank_name}'s own published return",
                         {y: "Not published" for y in years}))

        # Only years that actually printed a ratio are worth a period
        # paragraph: a year trimmed off the oldest end, or refused, has no
        # figure for the reader to misread.
        printed = {y for _label, values in rows for y in years
                   if isinstance(values.get(y), str)
                   and values[y].endswith("%")}
        short_years = {
            y: desc
            for y, desc in NON_ANNUAL_PERIODS.get(published_key, {}).items()
            if y in printed
        }

        note = _profitability_note(
            self, published_key, own, fx_refused, entity_note, short_years,
            fx_basis, bs_unit, rows, years, extra_note,
        )
        sources = _profitability_sources(
            self, published_key, pat_label, eq_label, as_label,
            balance_sheet, income_sheet, bool(own.published), extra_sources,
            equity_series_source,
        )
        width = max(46, min(64, max(len(lab) for lab, _ in rows) + 2))
        return self.add_metric_sheet(
            sheet_name,
            "Return on equity and return on assets in per cent, computed from "
            "this workbook's own " + balance_sheet + " and " + income_sheet
            + " sheets.",
            rows,
            sources,
            note=note,
            first_col_width=width,
            source_height=170,
        )

    def add_km1_sheet(
        self,
        title,
        subtitle,
        rows,
        sources_text,
        sheet_name=KM1_SHEET_NAME,
        first_col_width=72,
        source_height=150,
        unit_suffix="",
        years=None,
    ):
        """The bank's own UK KM1 "Key metrics" template, metrics as rows and
        years as columns, placed immediately BEFORE the 11 individual Pillar 3
        metric sheets so a reader meets the published summary first and the
        single-metric sheets afterwards.

        Same (kind, label, values) row shape as add_cash_flow_sheet - see that
        docstring - but with two deliberate differences:

        `unit_suffix` DEFAULTS TO EMPTY, because KM1 is the one sheet that
        mixes units down a single column: amount rows are £'000 while ratio
        and buffer rows are percentages. Carry the unit on each row instead,
        either in the label (the template's own convention, e.g. "Total
        exposure measure (£'000)") or by writing ratio values as strings
        ("14.5%"), which _add_statement_sheet passes through unchanged.

        TRANSCRIBE THE TEMPLATE AS THE BANK PRINTED IT. KM1 is a prescribed
        template (CRR Article 447 / PRA Disclosure Rules), so fidelity means
        keeping the bank's own row order, its row labels, AND the template's
        row numbers as printed ("UK 7a", "8", "UK 9a", ...) - they are how a
        reader cross-refers to the source document. Keep rows the bank prints
        as blank, "-" or "N/A" rather than dropping them: an omitted row is
        indistinguishable from a row we failed to find. Use SECTION rows for
        the template's own headings ("Additional own funds requirements",
        "Combined buffer requirement", "Leverage ratio", "Liquidity Coverage
        Ratio", "Net Stable Funding Ratio").

        Do NOT reorder rows into this project's preferred sequence, do not
        merge the two sides of a basis break into one row (the 1 Jan 2022
        leverage change and the LCR average-vs-point-in-time split both
        surface here as separate template rows), and do not compute a row the
        bank left blank - a derived figure in a disclosure template reads as
        a disclosure.

        years: optional per-sheet override - see _add_statement_sheet."""
        return self._add_statement_sheet(
            title,
            subtitle,
            rows,
            sources_text,
            sheet_name,
            first_col_width,
            source_height,
            unit_suffix,
            years=years,
        )

    def add_metric_sheet(
        self,
        name,
        unit,
        rows_data,
        sources_text,
        note=None,
        first_col_width=46,
        source_height=150,
        note_height=60,
        years=None,
    ):
        """
        rows_data: list of (label, values) pairs, values a {year: value} dict
            (numbers or strings, e.g. "82.94%" / "Not publicly disclosed").
        years: optional per-sheet override - see _add_statement_sheet.
        """
        years = years if years is not None else self.years
        years = self._trim_trailing_empty_years(
            years, (values for _label, values in rows_data)
        )
        self._metric_rows[name] = [
            (label, dict(values)) for label, values in rows_data
        ]
        ws = self.wb.create_sheet(title=name[:31])
        ncols = 1 + len(years)
        ws["A1"] = f"{self.bank_name} — {name}"
        ws["A1"].font = TITLE_FONT
        ws["A2"] = unit or ""
        ws["A2"].font = SUBTITLE_FONT

        headers = ["Metric"] + [self.year_label[y] for y in years]
        header_row = 3
        for c, h in enumerate(headers, start=1):
            ws.cell(row=header_row, column=c, value=h)
        self._style_header(ws, header_row, ncols)

        r = header_row + 1
        for label, values in rows_data:
            ws.cell(row=r, column=1, value=label)
            for ci, y in enumerate(years, start=2):
                ws.cell(row=r, column=ci, value=values.get(y))
            for c in range(1, ncols + 1):
                ws.cell(row=r, column=c).border = BORDER
            r += 1

        widths = [first_col_width] + [15] * len(years)
        if note:
            # spills across further rows when one row cannot show it
            r = self._write_merged_text_block(
                ws, r, ncols, f"Note: {note}", SUBTITLE_FONT,
                sum(widths), step=1,
            )

        self._write_source_cell(
            ws, r + 1, ncols, sources_text, height=source_height,
            width_units=sum(widths),
        )
        self._autosize(ws, widths)
        return ws

    def add_long_form_sheet(
        self,
        name,
        headers,
        rows,
        title=None,
        subtitle=None,
        note=None,
        widths=None,
        hyperlink_cells=None,
        freeze_panes="A5",
    ):
        """Add an auxiliary long-form data sheet.

        This is intended for additional observations that do not fit the
        standard fixed annual columns, such as quarterly or semi-annual Pillar
        3 disclosures.

        ``headers`` is a list of column names and ``rows`` is a list of row
        lists/tuples with the same length.  ``hyperlink_cells`` is an optional
        mapping of ``(data_row_index, column_index)`` to URL, using zero-based
        indexes relative to the supplied data rows and headers.  ``widths`` is
        an optional list of column widths.
        """
        if not headers:
            raise ValueError("Long-form sheet requires at least one header")
        ncols = len(headers)
        for row in rows:
            if len(row) != ncols:
                raise ValueError(
                    f"Long-form row has {len(row)} values; expected {ncols}"
                )

        ws = self.wb.create_sheet(title=name[:31])
        ws["A1"] = title or f"{self.bank_name} — {name}"
        ws["A1"].font = TITLE_FONT
        ws["A2"] = subtitle or ""
        ws["A2"].font = SUBTITLE_FONT

        header_row = 4
        for col, header in enumerate(headers, start=1):
            ws.cell(row=header_row, column=col, value=header)
        self._style_header(ws, header_row, ncols)

        hyperlink_cells = hyperlink_cells or {}
        for row_index, values in enumerate(rows):
            excel_row = header_row + 1 + row_index
            for col_index, value in enumerate(values):
                cell = ws.cell(row=excel_row, column=col_index + 1, value=value)
                cell.border = BORDER
                url = hyperlink_cells.get((row_index, col_index))
                if url:
                    cell.hyperlink = url
                    cell.style = "Hyperlink"

        if note:
            note_row = header_row + 1 + len(rows) + 1
            self._write_merged_text_block(
                ws, note_row, ncols, note, SOURCE_FONT,
                sum(widths or [18] * ncols), step=1,
            )

        ws.freeze_panes = freeze_panes
        self._autosize(ws, widths or [18] * ncols)
        return ws

    def add_wide_interim_sheet(
        self,
        name,
        headers=None,
        rows=None,
        title=None,
        subtitle=None,
        note=None,
        widths=None,
        hyperlink_cells=None,
        freeze_panes="D5",
    ):
        """Add a wide interim Pillar 3 matrix from standard observation rows.

        ``rows`` uses the same eight-field records as ``add_long_form_sheet``:
        period, disclosure type, metric, value, unit, basis, source document,
        and page/table.  Periods become columns and metrics become rows.  Each
        populated value cell links to its source document; a compact source
        register below the matrix preserves disclosure type and page/table
        references.  ``hyperlink_cells`` may map the zero-based input row and
        source-document column (normally ``(row_index, 6)``) to a URL.  This
        keeps a readable source-document label in the workbook while using the
        official URL as the hyperlink target.
        """
        # Accept the existing long-form call shape as well as the simpler
        # ``rows=...`` form, so bank builders can be migrated mechanically.
        if rows is None:
            rows = headers
        if not rows:
            raise ValueError("Wide interim sheet requires at least one row")
        if any(len(row) != 8 for row in rows):
            raise ValueError("Wide interim rows must contain exactly 8 fields")

        periods = []
        metrics = []
        metric_meta = {}
        values = {}
        links = {}
        source_rows = []
        source_seen = set()
        hyperlink_cells = hyperlink_cells or {}
        for row_index, row in enumerate(rows):
            period, disclosure, metric, value, unit, basis, source, page = row
            if period not in periods:
                periods.append(period)
            if metric not in metrics:
                metrics.append(metric)
                metric_meta[metric] = (unit, basis)
            values[(metric, period)] = value
            # Only ever hyperlink a cell to a genuine URL. This used to fall
            # back to the plain source-document label text (e.g. "Q3 2022
            # Pillar 3 Supplement") whenever a build script didn't pass an
            # explicit URL for that row - openpyxl writes that text in
            # verbatim as `cell.hyperlink`, producing an invalid link Excel
            # either errors on or mistreats as a relative path, and it LOOKS
            # like a real citation (styled + clickable) even though it isn't
            # one. Leaving the cell as plain, unstyled text when no real URL
            # is available makes the gap visible instead of silently faking
            # a working citation - see IN-031.
            source_url = hyperlink_cells.get((row_index, 6))
            if source_url and not str(source_url).startswith(("http://", "https://")):
                source_url = None
            links[(metric, period)] = source_url
            source_key = (period, disclosure, source, page)
            if source_key not in source_seen:
                source_seen.add(source_key)
                source_rows.append((*source_key, source_url))

        ws = self.wb.create_sheet(title=name[:31])
        ws["A1"] = title or f"{self.bank_name} — {name}"
        ws["A1"].font = TITLE_FONT
        ws["A2"] = subtitle or ""
        ws["A2"].font = SUBTITLE_FONT

        headers = ["Metric", "Unit", "Basis"] + periods
        header_row = 4
        for col, header in enumerate(headers, start=1):
            ws.cell(row=header_row, column=col, value=header)
        self._style_header(ws, header_row, len(headers))

        for row_index, metric in enumerate(metrics):
            excel_row = header_row + 1 + row_index
            unit, basis = metric_meta[metric]
            row_values = [metric, unit, basis]
            for col_index, value in enumerate(row_values, start=1):
                cell = ws.cell(row=excel_row, column=col_index, value=value)
                cell.border = BORDER
            for period_index, period in enumerate(periods, start=4):
                value = values.get((metric, period))
                cell = ws.cell(row=excel_row, column=period_index, value=value)
                cell.border = BORDER
                source = links.get((metric, period))
                if source and value not in (None, ""):
                    cell.hyperlink = source
                    cell.style = "Hyperlink"

        source_header_row = header_row + len(metrics) + 3
        ws.cell(row=source_header_row, column=1, value="Source register")
        ws.cell(row=source_header_row, column=1).font = SUBTITLE_FONT
        source_headers = [
            "Period",
            "Disclosure type",
            "Source document",
            "Page / table",
        ]
        for col, header in enumerate(source_headers, start=1):
            ws.cell(row=source_header_row + 1, column=col, value=header)
        self._style_header(ws, source_header_row + 1, len(source_headers))
        for source_index, source_row in enumerate(source_rows):
            excel_row = source_header_row + 2 + source_index
            for col_index, value in enumerate(source_row[:4], start=1):
                cell = ws.cell(row=excel_row, column=col_index, value=value)
                cell.border = BORDER
                if col_index == 3 and source_row[4]:
                    cell.hyperlink = source_row[4]
                    cell.style = "Hyperlink"

        note_row = source_header_row + 2 + len(source_rows) + 1
        if note:
            self._write_merged_text_block(
                ws, note_row, len(headers), f"Note: {note}", SOURCE_FONT,
                sum([32, 18, 34] + [15] * len(periods)), step=1,
            )

        ws.freeze_panes = freeze_panes
        self._autosize(ws, [32, 18, 34] + [15] * len(periods))
        return ws

    def add_overview_sheet(
        self,
        cash_flow_totals,
        cash_flow_unit,
        ratios,
        note=None,
        balance_sheet_totals=None,
        balance_sheet_unit=None,
        income_statement_totals=None,
        income_statement_unit=None,
        equity_changes_totals=None,
        equity_changes_unit=None,
        years=None,
    ):
        """
        Inserts an "Overview" sheet as the first tab: summary tables of
        headline Balance Sheet / Profit & Loss / Statement of Changes in
        Equity / cash flow totals and headline Pillar 3 ratios across all
        years, plus a clustered column chart for each money block and a
        line chart for the ratios - all rendered oldest-year-first left to
        right regardless of the most-recent-first column order used
        everywhere else. Block order, top to bottom: Balance Sheet,
        Profit & Loss, Statement of Changes in Equity, Cash Flow, Ratios.

        balance_sheet_totals / income_statement_totals: list of
            (label, {year: number}) - e.g. Total assets/Loans and advances/
            Customer deposits/Total equity for the balance sheet; Revenue/
            Total operating expense/Profit for the year for the income
            statement. Omit or pass `None`/`[]` to skip that block entirely
            (e.g. for a workbook built before these sheets existed).
        balance_sheet_unit / income_statement_unit: unit string for that
            block's table heading and chart axis, e.g. "£'000". Ignored if
            the corresponding totals list is empty.
        equity_changes_totals: list of (label, {year: number}) - a per-year
            bridge summary of the Statement of Changes in Equity sheet
            (which is itself chronological, not year-columned - see
            add_equity_changes_sheet), e.g. Opening equity / Total
            comprehensive income(/loss) for the year / Other equity
            movements, net / Closing equity. Omit or pass `None`/`[]` to
            skip.
        equity_changes_unit: unit string for that block, e.g. "£'000".
            Ignored if equity_changes_totals is empty.
        cash_flow_totals: list of (label, {year: number}) - e.g. net cash
            from operating/investing/financing activities, cash at year end.
            Pass an empty list ([]) for a Pillar-3-only workbook (e.g. an
            entity taking the FRS 101/102 cash-flow-statement exemption) -
            the cash-flow table/chart are then omitted entirely; see the
            "Cash Flow Statement" sheet for the exemption note in that case.
        cash_flow_unit: unit string for the table heading and chart axis,
            e.g. "£m" or "£'000". Ignored if cash_flow_totals is empty.
        ratios: list of (label, {year: value}) - values as displayed
            (e.g. "14.5%" or "Not publicly disclosed"); values that aren't
            a plain percentage are parsed as None and simply leave a gap
            in the chart rather than being plotted. Pass an empty list ([])
            for a bank with no disclosed Pillar 3 ratios at all - the ratios
            table/chart are then omitted entirely (fixed 2026-08-28; earlier
            build scripts worked around this by passing empty-{}-valued
            entries instead, e.g. build_caf_bank.py/build_brown_shipley.py -
            that workaround still works too, no need to change them).
        """
        years = years if years is not None else self.years

        # Standing objective (b): these blocks are no longer hand-copied
        # duplicates of the detail sheets - they are derived FROM them, so
        # a correction applied to a detail sheet can no longer be missed
        # here. The arguments still choose WHICH rows the Overview features
        # and what each is called; only the values are taken over.
        #
        # The Statement of Changes in Equity block is deliberately NOT
        # derived: that sheet is a chronological roll-forward with no year
        # columns to read, which is the same reason check_overview_ties.py
        # leaves it out of BLOCK_TO_SHEET.
        if balance_sheet_totals:
            balance_sheet_totals = self._derive_block(
                "Balance Sheet", balance_sheet_totals, "balance sheet", years
            )
        if income_statement_totals:
            income_statement_totals = self._derive_block(
                "Profit & Loss", income_statement_totals, "profit & loss", years
            )
        if cash_flow_totals:
            cash_flow_totals = self._derive_block(
                "Cash Flow Statement", cash_flow_totals, "cash flow", years
            )
        if ratios:
            ratios = self._derive_ratios(ratios, years)

        ws = self.wb.create_sheet(title="Overview", index=0)
        ncols = 1 + len(years)
        headers = ["Line item"] + [self.year_label[y] for y in years]

        def _block_years(totals):
            """This block's own year axis, trimmed at the OLDEST end only.

            Added 2026-10-09 on the user's instruction: "if the data is not
            there but still has a year header, then please delete that".
            Until now every Overview block printed the FULL workbook year
            list, so a block routinely carried headers over columns it could
            never fill - the Overview was the one sheet that never got the
            trim `_trim_trailing_empty_years` has applied to detail sheets
            since 2026-09-18. Blocks are trimmed INDEPENDENTLY because they
            genuinely stop at different places (Paragon's equity block ends at
            FY2021 while its balance sheet runs to FY2017).

            TRAILING ONLY, for exactly the reason the detail-sheet rule gives:
            an empty column that is not at the oldest end is a REAL GAP and
            must stay visible. Paragon's Cash Flow Summary is the case that
            proves it - FY2020 and FY2019 are empty but FY2018 and FY2017
            carry figures, so those two are an interior gap in the bank's own
            disclosure, not a heading over nothing. Deleting them would hide
            it and would also make the chart's category axis misrepresent the
            spacing between years.
            """
            return self._trim_trailing_empty_years(
                years, [vals for _, vals in totals]
            )

        ws["A1"] = f"{self.bank_name} — Overview"
        ws["A1"].font = TITLE_FONT
        ws["A2"] = (
            "Headline balance sheet, profit & loss, cash flow and Pillar 3 figures across all years "
            "covered in this workbook - how the bank is using its money and the risk it is taking with it"
        )
        ws["A2"].font = SUBTITLE_FONT

        # -- money blocks: Balance Sheet, Profit & Loss, Equity Changes, Cash Flow (bar charts) --
        money_blocks = [
            (
                "bs",
                "Balance Sheet Summary",
                balance_sheet_totals or [],
                balance_sheet_unit,
            ),
            (
                "is",
                "Profit & Loss Summary",
                income_statement_totals or [],
                income_statement_unit,
            ),
            (
                "eq",
                "Statement of Changes in Equity Summary",
                equity_changes_totals or [],
                equity_changes_unit,
            ),
            ("cf", "Cash Flow Summary", cash_flow_totals or [], cash_flow_unit),
        ]
        not_applicable_text = {
            "bs": "Balance Sheet Summary: not applicable — this workbook was built before the Balance Sheet sheet existed.",
            "is": "Profit & Loss Summary: not applicable — this workbook was built before the Profit & Loss sheet existed.",
            "eq": "Statement of Changes in Equity Summary: not applicable — this workbook was built before the Statement of Changes in Equity sheet existed.",
            "cf": "Cash Flow Summary: not applicable — this entity does not publish a cash flow statement (see the Cash Flow Statement sheet for the exemption basis).",
        }

        row = 4
        block_table_info = {}  # key -> (header_row, data_end, block_years) or None
        for key, title, totals, unit in money_blocks:
            if totals:
                years_b = _block_years(totals)
                ncols_b = 1 + len(years_b)
                ws.cell(
                    row=row, column=1, value=f"{title} ({unit})"
                ).font = SECTION_FONT
                row += 1
                header_row = row
                for c, h in enumerate(
                    ["Line item"] + [self.year_label[y] for y in years_b], start=1
                ):
                    ws.cell(row=row, column=c, value=h)
                self._style_header(ws, row, ncols_b)
                row += 1
                for label, values in totals:
                    ws.cell(row=row, column=1, value=label)
                    for ci, y in enumerate(years_b, start=2):
                        ws.cell(row=row, column=ci, value=values.get(y))
                    for c in range(1, ncols_b + 1):
                        ws.cell(row=row, column=c).font = TOTAL_FONT
                        ws.cell(row=row, column=c).border = BORDER
                    row += 1
                block_table_info[key] = (header_row, row - 1, years_b)
            else:
                ws.cell(
                    row=row, column=1, value=not_applicable_text[key]
                ).font = SECTION_FONT
                row += 1
                block_table_info[key] = None
            row += 1

        if ratios:
            ws.cell(row=row, column=1, value="Pillar 3 Key Metrics").font = SECTION_FONT
            row += 1
            ratio_header_row = row
            ratio_years = _block_years(ratios)
            ratio_ncols = 1 + len(ratio_years)
            for c, h in enumerate(
                ["Line item"] + [self.year_label[y] for y in ratio_years], start=1
            ):
                ws.cell(row=row, column=c, value=h)
            self._style_header(ws, row, ratio_ncols)
            row += 1
            for label, values in ratios:
                ws.cell(row=row, column=1, value=label)
                for ci, y in enumerate(ratio_years, start=2):
                    ws.cell(row=row, column=ci, value=values.get(y))
                for c in range(1, ratio_ncols + 1):
                    ws.cell(row=row, column=c).border = BORDER
                row += 1
            ratio_data_end = row - 1
        else:
            ws.cell(
                row=row,
                column=1,
                value="Pillar 3 Key Metrics: not applicable — no ratios are disclosed for this "
                "entity (see the individual Pillar 3 metric sheets).",
            ).font = SECTION_FONT
            row += 1
            ratio_header_row = None

        widths = [42] + [15] * len(years)
        if note:
            row += 1
            text = f"Note: {note}"
            # Safe to grow or spill: the charts anchor at `chart_row = row + 2`
            # below, so extra rows push them down rather than overlapping.
            row = self._write_merged_text_block(
                ws, row, ncols, text, SUBTITLE_FONT, sum(widths), step=1
            )

        self._autosize(ws, widths)

        # -- hidden numeric staging areas, oldest-year-first, for the charts --
        # (built as separate chronological blocks rather than via a reversed
        # category axis, which flips the value axis to the wrong side in Excel)
        # No sheet-wide chrono_years/n_years any more: each block stages its
        # own trimmed axis (see _block_years), so a width taken from the full
        # year list would overrun a trimmed block's staging area and feed the
        # chart blank trailing categories.
        stage_col = ncols + 3
        # key -> (stage_header_row, stage_end, stage_col, n_years_for_this_block)
        block_stage_info = {}
        for key, title, totals, unit in money_blocks:
            info = block_table_info[key]
            if totals and info:
                header_row, _, years_b = info
                chrono_b = list(reversed(years_b))
                n_b = len(years_b)
                for ci, y in enumerate(chrono_b, start=1):
                    ws.cell(
                        row=header_row, column=stage_col + ci, value=self.year_label[y]
                    )
                r = header_row + 1
                for label, values in totals:
                    ws.cell(row=r, column=stage_col, value=label)
                    for ci, y in enumerate(chrono_b, start=1):
                        ws.cell(row=r, column=stage_col + ci, value=values.get(y))
                    r += 1
                block_stage_info[key] = (header_row, r - 1, stage_col, n_b)
                stage_col += n_b + 3
            else:
                block_stage_info[key] = None

        ratio_stage_col = stage_col
        if ratios:
            ratio_stage_header_row = ratio_header_row
            for prev_key in ("bs", "is", "eq", "cf"):
                if block_stage_info[prev_key]:
                    ratio_stage_header_row = block_stage_info[prev_key][0]
                    break
            chrono_ratio = list(reversed(ratio_years))
            n_ratio = len(ratio_years)
            for ci, y in enumerate(chrono_ratio, start=1):
                ws.cell(
                    row=ratio_stage_header_row,
                    column=ratio_stage_col + ci,
                    value=self.year_label[y],
                )
            r = ratio_stage_header_row + 1
            for label, values in ratios:
                ws.cell(row=r, column=ratio_stage_col, value=label)
                for ci, y in enumerate(chrono_ratio, start=1):
                    ws.cell(
                        row=r,
                        column=ratio_stage_col + ci,
                        value=_parse_percent(values.get(y)),
                    )
                r += 1
            ratio_stage_end = r - 1
            last_col = ratio_stage_col + n_ratio + 1
        else:
            last_col = stage_col

        for c in range(ncols + 3, last_col):
            ws.column_dimensions[get_column_letter(c)].hidden = True

        # -- charts --
        chart_row = row + 2
        bar_titles = {
            "bs": "Balance Sheet Summary",
            "is": "Profit & Loss Summary",
            "eq": "Statement of Changes in Equity Summary",
            "cf": "Cash Flow Summary",
        }
        for key, title, totals, unit in money_blocks:
            stage_info = block_stage_info[key]
            if not stage_info:
                continue
            stage_header_row, stage_end, block_stage_col, n_b = stage_info
            bar = BarChart()
            bar.type = "col"
            bar.grouping = "clustered"
            bar.title = f"{self.bank_name} — {bar_titles[key]} by Year"
            bar.y_axis.title = unit
            bar.height = 13
            bar.width = 24
            data = Reference(
                ws,
                min_col=block_stage_col,
                max_col=block_stage_col + n_b,
                min_row=stage_header_row + 1,
                max_row=stage_end,
            )
            bar.add_data(data, titles_from_data=True, from_rows=True)
            cats = Reference(
                ws,
                min_col=block_stage_col + 1,
                max_col=block_stage_col + n_b,
                min_row=stage_header_row,
                max_row=stage_header_row,
            )
            bar.set_categories(cats)
            bar.visible_cells_only = (
                False  # source data lives in hidden staging columns
            )
            self._style_chart_axes(bar)
            bar.legend.position = "b"
            self._reserve_bottom_legend(bar, legend_h=0.16, plot_h=0.55, plot_top=0.14)
            ws.add_chart(bar, f"A{chart_row}")
            chart_row += 22

        if not ratios:
            return ws

        line = LineChart()
        line.title = f"{self.bank_name} — Pillar 3 Key Metrics by Year"
        line.y_axis.title = "%"
        line.height = 16
        line.width = 24
        ldata = Reference(
            ws,
            min_col=ratio_stage_col,
            max_col=ratio_stage_col + n_ratio,
            min_row=ratio_stage_header_row + 1,
            max_row=ratio_stage_end,
        )
        line.add_data(ldata, titles_from_data=True, from_rows=True)
        lcats = Reference(
            ws,
            min_col=ratio_stage_col + 1,
            max_col=ratio_stage_col + n_ratio,
            min_row=ratio_stage_header_row,
            max_row=ratio_stage_header_row,
        )
        line.set_categories(lcats)
        line.visible_cells_only = False  # source data lives in hidden staging columns
        self._style_chart_axes(line)
        line.legend.position = "b"
        self._reserve_bottom_legend(line, legend_h=0.22, plot_h=0.50, plot_top=0.12)
        for s in line.series:
            s.smooth = False
        ws.add_chart(line, f"A{chart_row}")

        return ws

    def add_not_disclosed_metric_sheets(self, names, sources_text, per_note=None, years=None,
                                        source_height=150, statements=None):
        """Convenience for the common "no Pillar 3 doc exists" case - fills a
        list of metric sheets with a single "Not publicly disclosed" row each.
        per_note: optional {name: note_text} for sheet-specific notes.
        years: optional per-sheet override - see _add_statement_sheet.
        source_height: row height of the merged source-citation cell. The
        default matches _write_source_cell's own default; raise it when
        sources_text is long, since that cell has a fixed height and simply
        clips any citation text that overflows it.
        statements: optional {name: text} or {name: {year: text}} replacing the
        bare "Not publicly disclosed" with a statement that says WHICH outcome
        it is (GA-020): "Not published – <evidence>", "Not applicable –
        <reason>", "Unreached today – <what was tried>" or "Not published yet
        – <when due>". Omitted names/years keep the old bare text, so existing
        callers are unchanged."""
        per_note = per_note or {}
        statements = statements or {}
        years = years if years is not None else self.years
        for name in names:
            st = statements.get(name)
            cells = {}
            for y in years:
                if isinstance(st, dict):
                    cells[y] = st.get(y, "Not publicly disclosed")
                elif st:
                    cells[y] = st
                else:
                    cells[y] = "Not publicly disclosed"
            self.add_metric_sheet(
                name,
                None,
                [(name, cells)],
                sources_text,
                note=per_note.get(name),
                years=years,
                source_height=source_height,
            )

    def save(self, path):
        self._assert_no_orphan_columns()
        self.wb.save(path)
        print("Saved workbook with sheets:", self.wb.sheetnames)
        return path
