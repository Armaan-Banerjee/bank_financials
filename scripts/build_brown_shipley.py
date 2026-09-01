import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Brown Shipley & Co. Limited (Companies House 00398426, FRN 124548), a UK
# subsidiary of Quintet Private Bank (Luxembourg), calendar fiscal year-end.
# FY2025 accounts were filed with Companies House on 26 Aug 2026 but are still
# "being processed" (no document available yet) as of this build - workbook
# therefore covers FY2021-FY2024 (4 years), not the usual 5.
YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/00398426/filing-history"
AR2024_URL = f"{CH_BASE}/MzQ3ODk2Mjk5OWFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = f"{CH_BASE}/MzQzMTg2OTM1MGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = f"{CH_BASE}/MzM5MTEwMDM3NGFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = f"{CH_BASE}/MzM0NzY3MjI5MmFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: Brown Shipley & Co. Limited (Companies House 00398426, FRN 124548) is a UK-authorised private "
    "bank, a subsidiary of Quintet Private Bank (Europe) S.A. (Luxembourg). It files full statutory accounts "
    "(income statement, statement of comprehensive income, statement of financial position, statement of changes "
    "in equity, cash flow statement, notes 1-37) under UK-adopted international accounting standards - no FRS 101/"
    "102 cash-flow exemption applies. Companies House filing history shows accounts to 31 December 2025 were "
    "filed 26 Aug 2026 but remained 'being processed' with no document available as of this build; this workbook "
    "therefore covers FY2021-FY2024 (4 years of cash flow and Pillar 3 data), not the usual 5. All Companies "
    "House-filed accounts documents for this entity are image-only PDFs (no text layer) - figures were "
    "transcribed via page-image review of each year's own filing. The Statement of Financial Position confirms "
    "Additional Tier 1 Equity Capital of £10,000k alongside CET1-eligible equity (called-up share capital + "
    "retained earnings) in every year shown - i.e. Brown Shipley's capital structure includes AT1 instruments, so "
    "unlike some smaller banks in this series CET1 capital/ratio cannot be assumed equal to Tier 1 or Total "
    "Capital. Brown Shipley's own statutory accounts, however, do not disclose a full Pillar 3-style capital "
    "template (no CET1/Tier 1/Total Capital £ amounts, no Total RWAs, no Tier 1/Total Capital ratios, no "
    "Leverage Ratio, no NSFR, no MREL Ratio in any year 2021-2024) - each year's Strategic Report includes only a "
    "brief narrative 'Regulatory measures' KPI stating the CET1 ratio and Liquidity Coverage Ratio (LCR) as bare "
    "percentages, with no supporting £ figures. No standalone Pillar 3 disclosure document was found on Brown "
    "Shipley's own website (which links only to Quintet Group-level annual reports and TCFD/sustainability "
    "documents, not a Brown Shipley-specific Pillar 3 filing) - Brown Shipley likely relies on Quintet Group-"
    "level Pillar 3 disclosure rather than publishing its own UK solo template. Metrics beyond CET1 Ratio and LCR "
    "are therefore filled with 'Not publicly disclosed' rather than guessed."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Brown Shipley & Co. Limited's own Cash Flow Statement, transcribed from each "
    "year's own Companies House filing (not a later year's comparative column, per this project's convention):\n"
    f"FY2024: Annual Report 2024 (filed 28 Aug 2025), p.42 (Cash Flow Statement) - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023 (filed 19 Aug 2024), p.39 (Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022 (filed 01 Sep 2023), p.38 (Cash Flow Statement) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021 (filed 04 Aug 2022), p.36 (Cash Flow Statement) - {AR2021_URL}\n"
    "Cross-checked against each figure's appearance as the following year's comparative column - all figures "
    "matched exactly except for cosmetic line-caption relabelling (e.g. FY2022's own report captions one line "
    "'Gain on deferred consideration - NWB' where FY2023's report captions the identical FY2022 comparative "
    "figure, (965), as 'Loss on deferred consideration - NWB'; and 'Proceeds on sale of Court of Protection "
    "business' in FY2022's own report vs. 'Gain on sale of Court of Protection business' for the same £567k in "
    "FY2023's report). No FY2020 comparative is shown (outside this workbook's FY2021-FY2024 window).\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Brown Shipley & Co. Limited's own Strategic Report 'Regulatory measures' KPI disclosure "
        "(narrative percentages only, no supporting £/RWA breakdown published), transcribed from each year's own "
        "Companies House filing:\n"
        f"FY2024: Annual Report 2024, p.6 (Strategic Report, 'Regulatory measures') - {AR2024_URL}\n"
        f"FY2023: Annual Report 2023, p.6 (Strategic Report, 'Regulatory measures') - {AR2023_URL}\n"
        f"FY2022: Annual Report 2022, p.6 (Strategic Report, 'Regulatory measures' (c)) - {AR2022_URL}\n"
        f"FY2021: Annual Report 2021, p.6 (Strategic Report, 'Regulatory measures' (c)) - {AR2021_URL}\n"
        "Cross-checked against each figure's appearance as a prior-year comparative in the following year's own "
        "report - all matched exactly (e.g. FY2021 CET1 19.6%/LCR 253% as stated in both the FY2021 report itself "
        "and as the FY2021 comparative in FY2022's report), except FY2023 CET1: FY2023's own report states 22.3%, "
        "while FY2024's report states the FY2023 comparative as 22.2% (a 0.1pp discrepancy in the Bank's own "
        "filings) - FY2023's own report's 22.3% is used here, per this project's convention of preferring each "
        "year's own report over a later comparative.\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Brown Shipley & Co. Limited", years=YEARS, year_label=YEAR_LABEL, header_color="5C4033")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Net profit before tax on continuing activities", {"FY2024": 7803, "FY2023": 1223, "FY2022": 2335, "FY2021": 5307}),
    ("DATA", "Changes in operating assets", {"FY2024": 99240, "FY2023": -12578, "FY2022": -67317, "FY2021": -149872}),
    ("DATA", "Changes in operating liabilities", {"FY2024": -317156, "FY2023": 30240, "FY2022": 349131, "FY2021": 164590}),
    ("DATA", "Dividend receivable", {"FY2024": -7, "FY2023": -7, "FY2022": -8, "FY2021": -8}),
    ("DATA", "Loss/(gain) on sale of prior year acquisitions", {"FY2022": 97, "FY2021": 5}),
    ("DATA", "Profit on sale of the pensions activities", {"FY2022": -400, "FY2021": -3600}),
    ("DATA", "Loss/(gain) on deferred consideration - NWB", {"FY2024": 0, "FY2023": 1442, "FY2022": -965, "FY2021": -3003}),
    ("DATA", "Net gains from financial instruments at fair value", {"FY2024": -4620, "FY2023": -3356, "FY2022": -6993, "FY2021": -3559}),
    ("DATA", "Impairment", {"FY2024": 3253, "FY2023": 3474, "FY2022": 2594, "FY2021": 96}),
    ("DATA", "Income taxes paid", {"FY2024": -3206, "FY2023": -829, "FY2022": -393, "FY2021": -1631}),
    ("DATA", "Depreciation of property and equipment", {"FY2024": 3563, "FY2023": 3392, "FY2022": 3123, "FY2021": 2695}),
    ("DATA", "Amortisation of intangible assets", {"FY2024": 3177, "FY2023": 3501, "FY2022": 3805, "FY2021": 3939}),
    ("DATA", "Loss on disposal of property and equipment", {"FY2024": 8, "FY2023": 4, "FY2022": 8, "FY2021": 70}),
    ("DATA", "(Profit)/loss on deferred consideration - TRP", {"FY2021": -3}),
    ("DATA", "Gain on sale of non-core Affluent client book", {"FY2024": -3318}),
    ("DATA", "Proceeds on sale of Court of Protection business / pensions administration activities", {"FY2024": 802, "FY2023": 567, "FY2022": 800, "FY2021": 3200}),
    ("DATA", "Proceeds on sale of a portfolio of assets", {"FY2023": 632, "FY2022": 600}),
    ("DATA", "Changes in provisions", {"FY2024": 229, "FY2023": -2576, "FY2022": -4174, "FY2021": 1582}),
    ("DATA", "Changes in Defined Benefit Pension Scheme surplus/(deficit)", {"FY2024": -327, "FY2023": -317, "FY2022": -219, "FY2021": -1431}),
    ("TOTAL", "Net cash (used in)/from operating activities", {"FY2024": -210559, "FY2023": 24812, "FY2022": 282024, "FY2021": 18377}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Dividend received", {"FY2024": 7, "FY2023": 7, "FY2022": 8, "FY2021": 8}),
    ("DATA", "Proceeds on sale of equity investments", {"FY2022": 725}),
    ("DATA", "Deferred consideration paid on prior year acquisitions", {"FY2023": -3200, "FY2022": -106, "FY2021": -3265}),
    ("DATA", "Proceeds on sale of non-core Affluent client book", {"FY2024": 2416}),
    ("DATA", "Purchase of property and equipment (excludes leased assets)", {"FY2024": -89, "FY2023": -916, "FY2022": -1402, "FY2021": -1405}),
    ("DATA", "Purchase of intangible assets", {"FY2024": -2, "FY2023": -16, "FY2022": 0, "FY2021": -4}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2024": 2332, "FY2023": -4125, "FY2022": -775, "FY2021": -4666}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Coupon paid to shareholder of Additional Tier 1 equity capital", {"FY2024": -1136, "FY2023": -883, "FY2022": -651, "FY2021": -635}),
    ("DATA", "Repayment of principal portion of lease liabilities", {"FY2024": -2359, "FY2023": -2194, "FY2022": -2040, "FY2021": -1857}),
    ("TOTAL", "Net cash used in financing activities", {"FY2024": -3495, "FY2023": -3077, "FY2022": -2691, "FY2021": -2492}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2024": -211722, "FY2023": 17610, "FY2022": 278558, "FY2021": 11219}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2024": 586631, "FY2023": 569021, "FY2022": 290463, "FY2021": 279244}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2024": 374909, "FY2023": 586631, "FY2022": 569021, "FY2021": 290463}),
    ("SECTION", "Components of cash and cash equivalents", {}),
    ("DATA", "Cash and balances at central banks", {"FY2024": 292700, "FY2023": 528997, "FY2022": 456835, "FY2021": 236409}),
    ("DATA", "Loans and advances to banks repayable on demand and less than 3 months", {"FY2024": 89347, "FY2023": 66766, "FY2022": 125926, "FY2021": 58767}),
    ("DATA", "Deposits from banks repayable on demand and less than 3 months", {"FY2024": -7138, "FY2023": -9132, "FY2022": -13740, "FY2021": -4713}),
    ("TOTAL", "Total components of cash and cash equivalents", {"FY2024": 374909, "FY2023": 586631, "FY2022": 569021, "FY2021": 290463}),
]

bw.add_cash_flow_sheet(
    title="Brown Shipley & Co. Limited — Cash Flow Statement",
    subtitle="£'000. Company (entity-level) basis. FY2025 not yet available - see source note.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=150)


CET1_RATIO = {"FY2024": "21.6%", "FY2023": "22.3%", "FY2022": "20.3%", "FY2021": "19.6%"}
LCR_RATIO = {"FY2024": "236%", "FY2023": "274%", "FY2022": "218%", "FY2021": "253%"}

NOT_DISCLOSED_NOTE = (
    "Brown Shipley's own statutory accounts do not disclose this metric in any year 2021-2024 - no standalone "
    "Pillar 3 template was found (see Entity note on the Cash Flow Statement sheet)."
)

bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital"],
    p3_sources(),
    per_note={"CET1 Capital": NOT_DISCLOSED_NOTE},
)

metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CET1_RATIO)], p3_sources())

bw.add_not_disclosed_metric_sheets(
    ["Tier 1 Capital", "Tier 1 Ratio", "Total Capital", "Total Capital Ratio", "Total RWAs", "Leverage Ratio"],
    p3_sources(),
    per_note={
        "Tier 1 Capital": NOT_DISCLOSED_NOTE + " Note: the Statement of Financial Position confirms £10,000k of "
                          "Additional Tier 1 Equity Capital exists in every year shown, so Tier 1 capital cannot "
                          "be assumed equal to CET1 capital - not calculated here without a disclosed RWA figure.",
        "Tier 1 Ratio": NOT_DISCLOSED_NOTE,
        "Total Capital": NOT_DISCLOSED_NOTE,
        "Total Capital Ratio": NOT_DISCLOSED_NOTE,
        "Total RWAs": NOT_DISCLOSED_NOTE,
        "Leverage Ratio": NOT_DISCLOSED_NOTE,
    },
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", LCR_RATIO)],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={"NSFR": NOT_DISCLOSED_NOTE, "MREL Ratio": NOT_DISCLOSED_NOTE},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash (used in)/from operating activities", {"FY2024": -210559, "FY2023": 24812, "FY2022": 282024, "FY2021": 18377}),
        ("Net cash from/(used in) investing activities", {"FY2024": 2332, "FY2023": -4125, "FY2022": -775, "FY2021": -4666}),
        ("Net cash used in financing activities", {"FY2024": -3495, "FY2023": -3077, "FY2022": -2691, "FY2021": -2492}),
        ("Cash and cash equivalents at end of year", {"FY2024": 374909, "FY2023": 586631, "FY2022": 569021, "FY2021": 290463}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Tier 1 Ratio", {}),
        ("Total Capital Ratio", {}),
        ("Leverage Ratio", {}),
        ("LCR", LCR_RATIO),
        ("NSFR", {}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. This workbook covers FY2021-FY2024 (4 years, not the "
         "usual 5) since Brown Shipley's FY2025 accounts were still 'being processed' at Companies House as of "
         "this build. Only CET1 Ratio and LCR are disclosed by Brown Shipley's own statutory accounts - all other "
         "Pillar 3 metrics (Tier 1/Total Capital, RWAs, Leverage Ratio, NSFR, MREL Ratio) are not publicly "
         "disclosed by this entity; see each metric sheet for detail.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BROWN SHIPLEY FINANCIALS.xlsx")
