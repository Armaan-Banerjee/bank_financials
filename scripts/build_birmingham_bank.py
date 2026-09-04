import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first - only 4 years exist
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/00555071"
AR2024_URL = CH_URL + "/filing-history/MzQ2MDU0MTMzM2FkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = CH_URL + "/filing-history/MzQxNDU2Njk3NGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = CH_URL + "/filing-history/MzM5NzY1NjE1N2FkaXF6a2N4/document?format=pdf&download=0"
P3_URL = "https://www.birminghambank.com/hubfs/Birmingham%20Bank%202024%20Theme/PDFs/09i-Pillar-3-Disclosures-Report-as-at-140425.pdf"
SR2023_URL = AR2023_URL  # Strategic Report KPI table is in the same FY2023 Annual Report filing

ENTITY_NOTE = (
    "Entity note: company 00555071, formerly Hardware Federation Finance Company Limited (1955-1990), "
    "then Bira Finance Limited (2011-2013), then Bira Bank Limited (2013-2021), renamed Birmingham Bank "
    "Limited 26 Jan 2021 - same company throughout, FRN 204478 confirmed on the bank's own site footer, "
    "matching the bank list exactly. Only 3 Companies House accounts filings exist (FY2022-FY2024, calendar "
    "year-end) - no FY2025 filing yet as of this build (likely not yet due) and no FY2021-specific standalone "
    "filing (the FY2022 filing's own FY2021 comparative column is the only source for FY2021). The Bank "
    "raised fresh capital (a GBP20m injection completing a change of control) in April 2023 and paused new "
    "lending for most of 2023 to build infrastructure - explains the large FY2023 capital-ratio jump."
)

STATEMENTS_SOURCES = (
    "Sources - Birmingham Bank Limited's own primary financial statements (FRS 102), all figures GBP'000:\n"
    f"FY2024: Full accounts made up to 31 Dec 2024 (filed 31 Mar 2025), Statement of Comprehensive Income "
    f"p.22, Statement of Financial Position p.23, Statement of Changes in Equity p.24 - {AR2024_URL}\n"
    f"FY2023: Full accounts made up to 31 Dec 2023 (filed 20 Mar 2024), same statements pp.22-24 - "
    f"{AR2023_URL}\n"
    f"FY2022 & FY2021: Amended full accounts made up to 31 Dec 2022 (filed 25 Oct 2023), Income Statement "
    f"p.25, Statement of Financial Position p.26, Statement of Changes in Equity p.27 - {AR2022_URL}. This "
    "filing reports in exact GBP (not GBP'000) with a FY2021 comparative column - both years converted to "
    "GBP'000 here (divided by 1,000, rounded) for consistency with the later filings' own units; no other "
    "conversion applied. Each year's own primary filing is used as that year's column (not a later filing's "
    "restated comparative), matching this project's standing convention.\n"
    + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: independently rounding each £'000 line (rather than rounding a pre-summed exact-£ "
    "total) occasionally leaves a component sum GBP1k off its own total row for FY2022/FY2021 (e.g. FY2022 "
    "Total assets: components sum to GBP17,058k vs the reported GBP17,059k) - both figures are shown exactly "
    "as each filing's own numbers round to; not forced to tie. No Additional Tier 1/Tier 2 capital or "
    "off-balance-sheet items are disclosed in any year."
)

PL_NOTE = (
    "The 'Net (loss)/gain on financial instruments held at fair value through profit and loss' line only "
    "appears from FY2024 onward (GBP27k) - not disclosed as a separate line in FY2021-FY2023, where it did "
    "not exist or was immaterial/nil."
)

ASSET_QUALITY_NOTE = (
    "The Bank reports under FRS 102 (incurred-loss impairment model), not IFRS 9 - no Stage 1/2/3 or "
    "non-performing-loan split is disclosed in any year's Annual Report or the one Pillar 3 document "
    "published; only a single 'bad debt provisions' balance (with a separate 'general' provision component "
    "in FY2021, reduced to nil during 2021) and a maturity-band breakdown of the gross loan book. Coverage "
    "ratio shown is Bad debt provisions / Gross loans and advances to customers - a coverage proxy, not an "
    "NPL ratio, since no non-performing/past-due balance is disclosed."
)

CASH_FLOW_SOURCES = (
    "Sources - Birmingham Bank Limited's own Statement of Cash Flows (FRS 102), all figures GBP'000:\n"
    f"FY2024: Full accounts made up to 31 Dec 2024 (filed 31 Mar 2025), p.25 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Full accounts made up to 31 Dec 2023 (filed 20 Mar 2024), p.26 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022 & FY2021: Amended full accounts made up to 31 Dec 2022 (filed 25 Oct 2023), p.28 (Statement of "
    f"Cash Flows) - {AR2022_URL}. This filing reports in exact GBP (not GBP'000) with a FY2021 comparative "
    "column - both years converted to GBP'000 here (divided by 1,000, rounded) for consistency with the "
    "later filings' own units; no other conversion applied.\n"
    + ENTITY_NOTE + "\n\n"
    "DATA NOTE: the FY2024 filing's own 'Analysis of the balances of cash' table mislabels its opening-balance "
    "column '01.01.2023' (should read 01.01.2024) - the VALUE (GBP3,866k) is used as printed, since it exactly "
    "matches FY2023's own reported closing balance; only the column label in the source appears to be a "
    "typo, not the figure. Separately, the FY2022 filing's own closing balance (GBP1,896k, rounded from the "
    "exact GBP1,895,707) differs by an immaterial GBP1k from FY2023's own filing's stated opening balance "
    "(GBP1,897k) for the same date - both are shown here exactly as each filing states them, not forced to "
    "match. FY2021's own opening cash balance is not available in any filing found (the FY2022 filing's "
    "comparative column starts from FY2021's closing balance only) - left blank, not estimated."
)


def p3_sources():
    return (
        "Sources - Birmingham Bank Limited Pillar 3 disclosures (Bank-solo basis, only document ever "
        "published):\n"
        f"FY2024 & FY2023: Pillar 3 Disclosures Report as at 14 Apr 2025 (covers year ended 31 Dec 2024, "
        f"FY2023 comparative), Section 1.4 'Summary Analysis' (headline figures) and Section 5 (RWA/Pillar 1 "
        f"detail table) - {P3_URL}\n"
        f"FY2022: Strategic Report 'key financial performance indicators' table in the Full accounts made up "
        f"to 31 Dec 2023 (filed 20 Mar 2024), p.4 - {SR2023_URL}. Ratio only - no GBP capital/RWA breakdown "
        "was published for FY2022 (the bank's only Pillar 3 document covers FY2023-FY2024 only).\n"
        "FY2021: not disclosed anywhere found - no Pillar 3 document covers this year, and no capital ratio "
        "appears in any Annual Report's Strategic Report for FY2021.\n"
        "The Bank has no Additional Tier 1 or Tier 2 capital in any year (per the Pillar 3 report's own "
        "statement), so CET1 Capital = Tier 1 Capital = Total Capital, and CET1 Ratio = Tier 1 Ratio = Total "
        "Capital Ratio, throughout."
    )


RWA_NOTE = (
    "FY2023 RWA shown here (GBP5,229k) is the Pillar 3 report's own Section 1.4 'Summary Analysis' headline "
    "figure. Its Section 5 RWA detail table (credit risk GBP4,056k + operational risk GBP1,045k = GBP5,101k) "
    "gives a slightly different total for the same year - both are the entity's own genuine disclosures, "
    "~2.5% apart; the headline summary figure is used for consistency with how FY2024 is sourced."
)

bw = BankWorkbook(bank_name="Birmingham Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="946B2D")

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash at Bank", {"FY2024": 11172, "FY2023": 3866, "FY2022": 1896, "FY2021": 2506}),
    ("DATA", "Treasury Bills and similar securities", {"FY2024": 43093, "FY2023": 20250, "FY2022": 6500, "FY2021": 9750}),
    ("DATA", "Loans and advances to Banks", {"FY2022": 1275, "FY2021": 1271}),
    ("DATA", "Loans and advances to customers", {"FY2024": 90310, "FY2023": 4195, "FY2022": 6867, "FY2021": 8868}),
    ("DATA", "Tangible fixed assets", {"FY2024": 70, "FY2023": 66, "FY2022": 70, "FY2021": 85}),
    ("DATA", "Intangible fixed assets", {"FY2024": 2101, "FY2023": 324}),
    ("DATA", "Other assets", {"FY2024": 3617, "FY2023": 431, "FY2022": 239, "FY2021": 120}),
    ("DATA", "Prepayments and accrued income", {"FY2024": 691, "FY2023": 463, "FY2022": 211, "FY2021": 177}),
    ("DATA", "Derivative financial asset", {"FY2024": 27}),
    ("TOTAL", "Total assets", {"FY2024": 151081, "FY2023": 29595, "FY2022": 17059, "FY2021": 22777}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {"FY2024": 106868, "FY2023": 9299, "FY2022": 10399, "FY2021": 13916}),
    ("DATA", "Other liabilities", {"FY2024": 6098, "FY2023": 1337, "FY2022": 454, "FY2021": 498}),
    ("TOTAL", "Total liabilities", {"FY2024": 112966, "FY2023": 10636, "FY2022": 10853, "FY2021": 14415}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2024": 60138, "FY2023": 30138, "FY2022": 10138, "FY2021": 8207}),
    ("DATA", "Share Premium", {"FY2024": 2862, "FY2023": 2862, "FY2022": 2862, "FY2021": 2793}),
    ("DATA", "Retained earnings", {"FY2024": -24885, "FY2023": -14041, "FY2022": -6794, "FY2021": -2637}),
    ("TOTAL", "Total equity", {"FY2024": 38115, "FY2023": 18959, "FY2022": 6206, "FY2021": 8363}),
    ("TOTAL", "Total liabilities and equity", {"FY2024": 151081, "FY2023": 29595, "FY2022": 17059, "FY2021": 22777}),
]

bw.add_balance_sheet_sheet(
    title="Birmingham Bank Limited — Balance Sheet",
    subtitle="Bank-solo basis, FRS 102, £'000 (FY2022/FY2021 converted from the source's exact-£ figures)",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income arising from debt securities", {"FY2024": 1756, "FY2023": 313, "FY2022": 530, "FY2021": 602}),
    ("DATA", "Other interest receivable and similar income", {"FY2024": 2680, "FY2023": 805, "FY2022": 228, "FY2021": 14}),
    ("TOTAL", "Total income", {"FY2024": 4436, "FY2023": 1118, "FY2022": 758, "FY2021": 616}),
    ("DATA", "Net (loss)/gain on financial instruments at fair value through profit and loss", {"FY2024": 27}),
    ("DATA", "Interest payable", {"FY2024": -1997, "FY2023": -213, "FY2022": -90, "FY2021": -115}),
    ("TOTAL", "Net income", {"FY2024": 2466, "FY2023": 905, "FY2022": 668, "FY2021": 500}),
    ("DATA", "Administrative expenses", {"FY2024": -13155, "FY2023": -8475, "FY2022": -4817, "FY2021": -3858}),
    ("DATA", "Depreciation and amortisation", {"FY2024": -237, "FY2023": -32, "FY2022": -24, "FY2021": -42}),
    ("DATA", "Impairment charge for loan losses", {"FY2024": -22, "FY2023": -4, "FY2022": -21, "FY2021": -34}),
    ("TOTAL", "Loss on ordinary activities before taxation", {"FY2024": -10948, "FY2023": -7606, "FY2022": -4194, "FY2021": -3434}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2024": 104, "FY2023": 359, "FY2022": 38, "FY2021": 0}),
    ("TOTAL", "Loss for the financial year", {"FY2024": -10844, "FY2023": -7247, "FY2022": -4156, "FY2021": -3434}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income", {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2024": -10844, "FY2023": -7247, "FY2022": -4156, "FY2021": -3434}),
]

bw.add_income_statement_sheet(
    title="Birmingham Bank Limited — Profit & Loss",
    subtitle="Bank-solo basis, FRS 102, £'000 (FY2022/FY2021 converted from the source's exact-£ figures)",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PL_NOTE,
    first_col_width=76,
    source_height=300,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Called up Share Capital", "Share Premium", "Retained Earnings", "Total Equity"]

equity_changes_rows = [
    ("TOTAL", "At 1 January 2021", (2000, 0, 796, 2796)),
    ("DATA", "Capital injection", (6207, 2793, 0, 9000)),
    ("DATA", "Total comprehensive income", (0, 0, -3434, -3434)),
    ("TOTAL", "At 31 December 2021", (8207, 2793, -2637, 8363)),
    ("DATA", "Capital injection", (1931, 69, 0, 2000)),
    ("DATA", "Total comprehensive income", (0, 0, -4156, -4156)),
    ("TOTAL", "At 31 December 2022", (10138, 2862, -6794, 6206)),
    ("DATA", "Issue of new shares", (20000, 0, 0, 20000)),
    ("DATA", "Total comprehensive income", (0, 0, -7247, -7247)),
    ("TOTAL", "At 31 December 2023", (30138, 2862, -14041, 18959)),
    ("DATA", "Issue of new shares", (30000, 0, 0, 30000)),
    ("DATA", "Total comprehensive income", (0, 0, -10844, -10844)),
    ("TOTAL", "At 31 December 2024", (60138, 2862, -24885, 38115)),
]

bw.add_equity_changes_sheet(
    title="Birmingham Bank Limited — Statement of Changes in Equity",
    subtitle="Bank-solo basis, FRS 102, £'000, chronological, 1 January 2021 - 31 December 2024",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES
    + "\n\nThe capital-raise row is labelled 'Capital injection' in the bank's own 2021/2022 filings and "
    "'Issue of new shares' in its 2023/2024 filings - same underlying event (a share capital + share premium "
    "increase), the bank's own wording just changed year to year; reproduced here as each filing states it.",
    first_col_width=50,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of operating (loss) to net operating cash flows", {}),
    ("DATA", "Loss on ordinary activities after taxation", {"FY2024": -10844, "FY2023": -7247, "FY2022": -4156, "FY2021": -3434}),
    ("DATA", "Increase in prepayments and accrued income", {"FY2024": -228, "FY2023": -252, "FY2022": -34, "FY2021": -238}),
    ("DATA", "Increase in derivative financial asset", {"FY2024": -27}),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {"FY2024": 4761, "FY2023": 883, "FY2022": -44, "FY2021": 396}),
    ("DATA", "Increase/(decrease) in provision for bad and doubtful debts", {"FY2024": 22, "FY2023": -4, "FY2022": -21, "FY2021": -8}),
    ("DATA", "Loans and advances written off net of recoveries", {"FY2022": 0, "FY2021": 0}),
    ("DATA", "Depreciation and amortisation", {"FY2024": 237, "FY2023": 32, "FY2022": 24, "FY2021": 42}),
    ("DATA", "Taxation - credit", {"FY2024": -104, "FY2023": -123, "FY2022": -38, "FY2021": 0}),
    ("TOTAL", "Net cash outflow from trading activities", {"FY2024": -6183, "FY2023": -6711, "FY2022": -4270, "FY2021": -3242}),
    ("DATA", "Net (increase)/decrease in loans and advances to credit institutions and customers", {"FY2024": -86137, "FY2023": 3951, "FY2022": 2018, "FY2021": 1328}),
    ("DATA", "Decrease/(increase) in financial assets / treasury bills", {"FY2024": -22843, "FY2023": -13750, "FY2022": 3250, "FY2021": -4250}),
    ("DATA", "Increase/(decrease) in deposits by customers", {"FY2024": 97569, "FY2023": -1100, "FY2022": -3518, "FY2021": -1837}),
    ("DATA", "Increase/(decrease) in other assets", {"FY2024": -3082, "FY2023": 167, "FY2022": -81, "FY2021": 8}),
    ("TOTAL", "Net cash outflow from operating activities", {"FY2024": -20676, "FY2023": -17679, "FY2022": -2601, "FY2021": -7994}),
    ("SECTION", "Cash flow from investing activities", {}),
    ("DATA", "Purchase of fixed assets", {"FY2024": -36, "FY2023": -45, "FY2022": -9, "FY2021": -42}),
    ("DATA", "Purchase of intangible assets", {"FY2024": -1982, "FY2023": -307, "FY2022": 0}),
    ("TOTAL", "Net cash outflow from investing activities", {"FY2024": -2018, "FY2023": -352, "FY2022": -9, "FY2021": -42}),
    ("SECTION", "Cash flow from financing activities", {}),
    ("DATA", "Called up share capital additions", {"FY2024": 30000, "FY2023": 20000, "FY2022": 2000, "FY2021": 9000}),
    ("TOTAL", "Net cash inflow from financing activities", {"FY2024": 30000, "FY2023": 20000, "FY2022": 2000, "FY2021": 9000}),
    ("TOTAL", "Increase/(decrease) in cash and cash equivalents", {"FY2024": 7306, "FY2023": 1969, "FY2022": -610, "FY2021": 964}),
    ("SECTION", "Analysis of the balances of cash", {}),
    ("DATA", "Cash at bank at beginning of year", {"FY2024": 3866, "FY2023": 1897, "FY2022": 2506}),
    ("TOTAL", "Cash at bank at end of year", {"FY2024": 11172, "FY2023": 3866, "FY2022": 1896, "FY2021": 2506}),
]

bw.add_cash_flow_sheet(
    title="Birmingham Bank Limited — Statement of Cash Flows",
    subtitle="Bank-solo basis, FRS 102, £'000 (FY2022/FY2021 converted from the source's exact-£ figures)",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers", {}),
    ("DATA", "Gross loans and advances to customers", {"FY2024": 90352, "FY2023": 4215, "FY2022": 6879, "FY2021": 8901}),
    ("DATA", "Bad debt provisions", {"FY2024": -42, "FY2023": -20, "FY2022": -12, "FY2021": -33}),
    ("TOTAL", "Net loans and advances to customers", {"FY2024": 90310, "FY2023": 4195, "FY2022": 6867, "FY2021": 8868}),
    ("SECTION", "Gross loan book by maturity", {}),
    ("DATA", "Repayable on demand", {"FY2024": 5, "FY2023": 5, "FY2022": 13, "FY2021": 44}),
    ("DATA", "Repayable within 3 months", {"FY2024": 277, "FY2023": 409, "FY2022": 927, "FY2021": 1182}),
    ("DATA", "Repayable between 3 months and one year", {"FY2024": 611, "FY2023": 1198, "FY2022": 2374, "FY2021": 2919}),
    ("DATA", "Repayable between one year and five years", {"FY2024": 89459, "FY2023": 2603, "FY2022": 3564, "FY2021": 4758}),
    ("SECTION", "Coverage", {}),
    ("DATA", "Bad debt provision coverage (Provision / Gross loans)", {"FY2024": "0.05%", "FY2023": "0.47%", "FY2022": "0.17%", "FY2021": "0.37%"}),
]

bw.add_asset_quality_sheet(
    title="Birmingham Bank Limited — Asset Quality",
    subtitle="Bank-solo basis, FRS 102, £'000. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + ASSET_QUALITY_NOTE,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=52, source_height=190)


TOTAL_CAPITAL = {"FY2024": 35985, "FY2023": 18617}
CAPITAL_RATIO = {"FY2024": "76%", "FY2023": "365%", "FY2022": "91%"}
RWA = {"FY2024": 47333, "FY2023": 5229}
LEVERAGE = {"FY2024": "24%", "FY2023": "63%"}
LCR = {"FY2024": "725%", "FY2023": "11,351%", "FY2022": "2,983%"}

SINGLE_TIER_NOTE = "No Additional Tier 1 or Tier 2 capital in any year - equals CET1 Capital exactly."

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", TOTAL_CAPITAL)])
metric("CET1 Ratio", "%", [("CET1 Ratio (= Capital Adequacy Ratio)", CAPITAL_RATIO)])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", TOTAL_CAPITAL)], note=SINGLE_TIER_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 Capital ratio", CAPITAL_RATIO)])
metric("Total Capital", "£'000", [("Total capital", TOTAL_CAPITAL)], note=SINGLE_TIER_NOTE)
metric("Total Capital Ratio", "%", [("Total Capital Ratio (= Capital Adequacy Ratio)", CAPITAL_RATIO)])
metric("Total RWAs", "£'000", [("Total risk-weighted assets", RWA)], note=RWA_NOTE)

rwa_breakdown_rows = [
    ("DATA", "Credit risk", {"FY2024": 46037, "FY2023": 4056}),
    ("DATA", "Operational risk", {"FY2024": 1296, "FY2023": 1045}),
    ("TOTAL", "Total RWAs (Pillar 1)", {"FY2024": 47333, "FY2023": 5101}),
]

bw.add_rwa_breakdown_sheet(
    title="Birmingham Bank Limited — RWA Breakdown",
    subtitle="Bank-solo basis, £'000. See source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources()
    + "\n\nThe Bank has no exposure to market risk under Pillar 1 (per the Pillar 3 report's own statement) "
    "- credit risk and operational risk are the only two categories. FY2022/FY2021 not disclosed: no Pillar 3 "
    "document covers those years (matches the gap already documented on the Total RWAs sheet).",
    first_col_width=46,
    source_height=200,
    unit_suffix=" (£'000)",
)

metric("Leverage Ratio", "%", [("Leverage ratio", LEVERAGE)])
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)],
       note="FY2022/FY2023 figures (2,983% / 11,351%) are genuinely this large - a small, low-loan-volume "
            "bank holding a large liquidity buffer relative to its (paused) lending book during its 2023 "
            "infrastructure-build year. Not a transcription error - see ENTITY_NOTE on the Cash Flow sheet.")

bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={
        "NSFR": "Not found in any Annual Report or the one Pillar 3 document published.",
        "MREL Ratio": "Not found - the Bank is small enough to plausibly sit below the BoE's MREL threshold, but no explicit statement to that effect was found either.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2024": 151081, "FY2023": 29595, "FY2022": 17059, "FY2021": 22777}),
        ("Total liabilities", {"FY2024": 112966, "FY2023": 10636, "FY2022": 10853, "FY2021": 14415}),
        ("Total equity", {"FY2024": 38115, "FY2023": 18959, "FY2022": 6206, "FY2021": 8363}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {"FY2024": 4436, "FY2023": 1118, "FY2022": 758, "FY2021": 616}),
        ("Loss for the financial year", {"FY2024": -10844, "FY2023": -7247, "FY2022": -4156, "FY2021": -3434}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Total equity (period end)", {"FY2024": 38115, "FY2023": 18959, "FY2022": 6206, "FY2021": 8363}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash outflow from operating activities", {"FY2024": -20676, "FY2023": -17679, "FY2022": -2601, "FY2021": -7994}),
        ("Net cash outflow from investing activities", {"FY2024": -2018, "FY2023": -352, "FY2022": -9, "FY2021": -42}),
        ("Net cash inflow from financing activities", {"FY2024": 30000, "FY2023": 20000, "FY2022": 2000, "FY2021": 9000}),
        ("Cash at bank at end of year", {"FY2024": 11172, "FY2023": 3866, "FY2022": 1896, "FY2021": 2506}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE),
        ("LCR", LCR),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Only 4 years of history exist (FY2021-FY2024) - "
         "the entity's own accounts filing history and Pillar 3 disclosures don't go back further.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BIRMINGHAM BANK FINANCIALS.xlsx")
