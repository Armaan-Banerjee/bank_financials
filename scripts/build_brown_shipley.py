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
# ST- rollout (batch ST-014): Balance Sheet, P&L, Statement of Changes in
# Equity, Asset Quality, RWA Breakdown. Sourced from the same 4 Companies
# House filings already cited above (AR20XX_URL) - each year's OWN
# originally-published report is used (project convention), not a later
# comparative column. This matters here: the FY2023 Annual Report
# "re-presents" its own FY2022 comparative column (Other receivables
# £8,615k vs FY2022's own report's £8,569k, a +£46k presentation
# reclassification that also nudges Total assets/Other liabilities by the
# same £46k) - this workbook uses each year's own originally-published
# figures throughout (matching the Cash Flow Statement sheet's existing
# convention), not the later re-presented version. FY2021's own report
# and its FY2022 comparative appearance both tie exactly (no restatement
# that year).
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - Brown Shipley & Co. Limited's own Income Statement / Statement of Financial Position / Statement "
    "of Changes in Equity, transcribed from each year's own Companies House filing (not a later year's "
    "comparative column):\n"
    f"FY2024: Annual Report 2024, pp.38,40-41 - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, pp.35,37-38 - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, pp.34,36-37 - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, pp.32,34-35 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: the FY2023 Annual Report's own FY2022 comparative column re-presents Other receivables "
    "as £8,615k (vs £8,569k in FY2022's own originally-published report) with matching +£46k nudges to Total "
    "assets (£1,507,146k re-presented vs £1,507,100k as originally published) and Other liabilities - a genuine "
    "but immaterial presentation reclassification disclosed by the Bank itself, not a restatement of profit or "
    "equity. This workbook uses each year's own originally-published figures throughout (project convention), so "
    "FY2022's column here shows £8,569k/£1,507,100k, not the later re-presented £8,615k/£1,507,146k. Separately: "
    "the FY2024 Statement of Changes in Equity's own 'Balance at end of year' total reads £132,954k, £1k more "
    "than its own four column figures actually sum to (£81,824k + £10,000k + £41,129k = £132,953k, matching the "
    "Balance Sheet's own Total Equity figure) - an immaterial £1k rounding artifact in the Bank's own source "
    "table, shown here as £132,953k for cross-sheet consistency. The Defined Benefit Pension Scheme surplus/"
    "deficit swaps sides of the Balance Sheet across the 4 years - an asset (£1,922k/£441k/£187k) FY2022-24, a "
    "liability ('Pensions', £4,423k) FY2021 - both shown as reported, not netted together. 'Current tax' and "
    "'Deferred tax' appear as separate Balance Sheet asset lines only in some years (both FY2021; Deferred tax "
    "only FY2022; neither disclosed as a distinct asset line FY2023-24) - blank cells where a year's own report "
    "doesn't show that specific line."
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2024": 292700, "FY2023": 528997, "FY2022": 456835, "FY2021": 236409}),
    ("DATA", "Loans and advances to banks", {"FY2024": 290450, "FY2023": 276949, "FY2022": 222163, "FY2021": 86610}),
    ("DATA", "Loans and advances to customers", {"FY2024": 483277, "FY2023": 554649, "FY2022": 646794, "FY2021": 565574}),
    ("DATA", "Derivative financial instruments - held for trading", {"FY2024": 3785, "FY2023": 4148, "FY2022": 5795, "FY2021": 1952}),
    ("DATA", "Investments - non-trading at fair value through profit or loss", {"FY2024": 764, "FY2023": 405, "FY2022": 359, "FY2021": 698}),
    ("DATA", "Debt securities at amortised cost", {"FY2024": 105293, "FY2023": 111833, "FY2022": 117333, "FY2021": 188307}),
    ("DATA", "Other receivables", {"FY2024": 8062, "FY2023": 11639, "FY2022": 8569, "FY2021": 12597}),
    ("DATA", "Property and equipment", {"FY2024": 9248, "FY2023": 11612, "FY2022": 14021, "FY2021": 14917}),
    ("DATA", "Goodwill and other intangible assets", {"FY2024": 22250, "FY2023": 28205, "FY2022": 34538, "FY2021": 42818}),
    ("DATA", "Investment in subsidiaries", {"FY2024": 293, "FY2023": 293, "FY2022": 293, "FY2021": 293}),
    ("DATA", "Current tax asset", {"FY2021": 385}),
    ("DATA", "Deferred tax asset", {"FY2022": 213, "FY2021": 1717}),
    ("DATA", "Defined Benefit Pension Scheme (asset)", {"FY2024": 1922, "FY2023": 441, "FY2022": 187}),
    ("TOTAL", "Total assets", {"FY2024": 1218044, "FY2023": 1529171, "FY2022": 1507100, "FY2021": 1152277}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2024": 7138, "FY2023": 9131, "FY2022": 13740, "FY2021": 4713}),
    ("DATA", "Deposits from customers", {"FY2024": 1046365, "FY2023": 1353609, "FY2022": 1321391, "FY2021": 971736}),
    ("DATA", "Derivative financial instruments - held for trading", {"FY2024": 11, "FY2023": 1417, "FY2022": 1846, "FY2021": 207}),
    ("DATA", "Other liabilities", {"FY2024": 29447, "FY2023": 34773, "FY2022": 36539, "FY2021": 37230}),
    ("DATA", "Defined Benefit Pension Scheme (liability)", {"FY2021": 4423}),
    ("DATA", "Provisions", {"FY2024": 371, "FY2023": 143, "FY2022": 2719, "FY2021": 6893}),
    ("DATA", "Current tax liability", {"FY2024": 1757, "FY2023": 929, "FY2022": 184}),
    ("DATA", "Deferred tax liability", {"FY2024": 2, "FY2023": 30}),
    ("TOTAL", "Total liabilities", {"FY2024": 1085091, "FY2023": 1400032, "FY2022": 1376419, "FY2021": 1025202}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2024": 81824, "FY2023": 81824, "FY2022": 81824, "FY2021": 81824}),
    ("DATA", "Additional Tier 1 Equity Capital", {"FY2024": 10000, "FY2023": 10000, "FY2022": 10000, "FY2021": 10000}),
    ("DATA", "Retained earnings", {"FY2024": 41129, "FY2023": 37315, "FY2022": 38857, "FY2021": 35251}),
    ("TOTAL", "Total equity", {"FY2024": 132953, "FY2023": 129139, "FY2022": 130681, "FY2021": 127075}),
    ("TOTAL", "Total liabilities and equity", {"FY2024": 1218044, "FY2023": 1529171, "FY2022": 1507100, "FY2021": 1152277}),
]

bw.add_balance_sheet_sheet(
    title="Brown Shipley & Co. Limited — Statement of Financial Position",
    subtitle="Company (entity-level) basis, £'000. FY2025 not yet available - see source note.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=68,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2024": 83170, "FY2023": 90709, "FY2022": 33998, "FY2021": 13124}),
    ("DATA", "Interest and similar expense", {"FY2024": -58552, "FY2023": -63253, "FY2022": -16047, "FY2021": -3827}),
    ("TOTAL", "Net interest income", {"FY2024": 24618, "FY2023": 27456, "FY2022": 17951, "FY2021": 9297}),
    ("DATA", "Fee and commission income", {"FY2024": 58352, "FY2023": 60023, "FY2022": 59780, "FY2021": 64976}),
    ("DATA", "Fee and commission expense", {"FY2024": -3494, "FY2023": -3136, "FY2022": -2120, "FY2021": -1824}),
    ("TOTAL", "Net fee and commission income", {"FY2024": 54858, "FY2023": 56887, "FY2022": 57660, "FY2021": 63152}),
    ("DATA", "Dividend income", {"FY2024": 7, "FY2023": 7, "FY2022": 8, "FY2021": 8}),
    ("DATA", "Net gains from financial instruments at fair value through profit or loss", {"FY2024": 4620, "FY2023": 3356, "FY2022": 7718, "FY2021": 3559}),
    ("DATA", "Net losses from financial instruments not measured at fair value through profit or loss", {"FY2021": 0}),
    ("DATA", "Other operating income", {"FY2024": 11318, "FY2023": 8017, "FY2022": 9688, "FY2021": 14866}),
    ("TOTAL", "Net operating income", {"FY2024": 95421, "FY2023": 95723, "FY2022": 93025, "FY2021": 90882}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Staff expenses", {"FY2024": -44065, "FY2023": -53830, "FY2022": -53667, "FY2021": -52755}),
    ("DATA", "General administrative expenses", {"FY2024": -33199, "FY2023": -31153, "FY2022": -27501, "FY2021": -23574}),
    ("DATA", "Depreciation of property and equipment", {"FY2024": -3563, "FY2023": -3392, "FY2022": -3123, "FY2021": -2695}),
    ("DATA", "Amortisation of intangible assets", {"FY2024": -3177, "FY2023": -3501, "FY2022": -3805, "FY2021": -3939}),
    ("DATA", "Net (increase)/decrease in provisions", {"FY2024": -361, "FY2023": 850, "FY2022": 0, "FY2021": -2516}),
    ("TOTAL", "Total operating expenses", {"FY2024": -84365, "FY2023": -91026, "FY2022": -88096, "FY2021": -85479}),
    ("DATA", "Impairment of assets", {"FY2024": -3253, "FY2023": -3474, "FY2022": -2594, "FY2021": -96}),
    ("TOTAL", "Profit before tax", {"FY2024": 7803, "FY2023": 1223, "FY2022": 2335, "FY2021": 5307}),
    ("DATA", "Income tax (charge)/credit", {"FY2024": -3719, "FY2023": -1835, "FY2022": -1224, "FY2021": -2399}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2024": 4084, "FY2023": -612, "FY2022": 1111, "FY2021": 2908}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Actuarial gain/(loss) on Defined Benefit Pension Scheme", {"FY2024": 1154, "FY2023": -63, "FY2022": 4391, "FY2021": 2131}),
    ("DATA", "Deferred tax (debit)/credit on pension scheme", {"FY2024": -288, "FY2023": 16, "FY2022": -1245, "FY2021": -75}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2024": 4950, "FY2023": -659, "FY2022": 4257, "FY2021": 4964}),
]

bw.add_income_statement_sheet(
    title="Brown Shipley & Co. Limited — Income Statement",
    subtitle="Company (entity-level) basis, £'000. FY2025 not yet available - see source note.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=78,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological)
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "At 1 January 2021", (81824, 10000, 30922, 122746)),
    ("DATA", "Additional Tier 1 Equity Capital coupon paid to parent (FY2021)", (None, None, -635, -635)),
    ("DATA", "Total comprehensive income for the year (FY2021)", (None, None, 4964, 4964)),
    ("TOTAL", "At 31 December 2021", (81824, 10000, 35251, 127075)),
    ("DATA", "Additional Tier 1 Equity Capital coupon paid to parent (FY2022)", (None, None, -651, -651)),
    ("DATA", "Total comprehensive income for the year (FY2022)", (None, None, 4257, 4257)),
    ("TOTAL", "At 31 December 2022", (81824, 10000, 38857, 130681)),
    ("DATA", "Additional Tier 1 Equity Capital coupon paid to parent (FY2023)", (None, None, -883, -883)),
    ("DATA", "Total comprehensive loss for the year (FY2023)", (None, None, -659, -659)),
    ("TOTAL", "At 31 December 2023", (81824, 10000, 37315, 129139)),
    ("DATA", "Additional Tier 1 Equity Capital coupon paid to parent (FY2024)", (None, None, -1136, -1136)),
    ("DATA", "Total comprehensive income for the year (FY2024)", (None, None, 4950, 4950)),
    ("TOTAL", "At 31 December 2024", (81824, 10000, 41129, 132953)),
]

bw.add_equity_changes_sheet(
    title="Brown Shipley & Co. Limited — Statement of Changes in Equity",
    subtitle="Company (entity-level) basis, £'000. Chronological roll-forward, oldest to newest.",
    headers=["Called up share capital", "Additional Tier 1 Equity Capital", "Retained earnings", "Total"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=58,
    source_height=380,
)

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
# Asset Quality: Loans and advances to customers by purpose, and ECL
# allowance by IFRS 9 stage - from the Bank's own Note 14 "Loans and
# advances to customers" (each year's own report). Only the ECL
# ALLOWANCE is disclosed by stage; gross exposure by stage is not
# disclosed (only a partial "Stage 2 transfers" reconciliation, not a
# full gross-by-stage table) - confirmed by reading the note in full, not
# assumed. Stage 3/NPL exposure ratios therefore cannot be derived here;
# only an overall ECL coverage ratio (total allowance / total gross
# loans) is shown.
# ---------------------------------------------------------------
AQ_ON_DEMAND = {"FY2024": 171242, "FY2023": 192821, "FY2022": 179111, "FY2021": 132746}
AQ_PERSONAL = {"FY2024": 2252, "FY2023": 845, "FY2022": 1126, "FY2021": 427}
AQ_PROPERTY = {"FY2024": 279254, "FY2023": 320684, "FY2022": 378183, "FY2021": 311293}
AQ_LOMBARD = {"FY2024": 800, "FY2023": 13043, "FY2022": 26716, "FY2021": 24868}
AQ_OTHER_TERM = {"FY2024": 31295, "FY2023": 27801, "FY2022": 61728, "FY2021": 96302}
AQ_GROSS_TOTAL = {y: AQ_ON_DEMAND[y] + AQ_PERSONAL[y] + AQ_PROPERTY[y] + AQ_LOMBARD[y] + AQ_OTHER_TERM[y] for y in YEARS}

AQ_ECL_S1 = {"FY2024": 49, "FY2023": 117, "FY2022": 55, "FY2021": 51}
AQ_ECL_S2 = {"FY2024": 102, "FY2023": 7, "FY2022": 4, "FY2021": 0}
AQ_ECL_S3 = {"FY2024": 1415, "FY2023": 421, "FY2022": 13, "FY2021": 11}
AQ_ECL_TOTAL = {y: AQ_ECL_S1[y] + AQ_ECL_S2[y] + AQ_ECL_S3[y] for y in YEARS}

AQ_NET_TOTAL = {"FY2024": 483277, "FY2023": 554649, "FY2022": 646794, "FY2021": 565574}
AQ_COVERAGE = {y: f"{AQ_ECL_TOTAL[y] / AQ_GROSS_TOTAL[y] * 100:.3f}%" for y in YEARS}
AQ_STAGE3_SHARE_OF_ECL = {y: f"{AQ_ECL_S3[y] / AQ_ECL_TOTAL[y] * 100:.1f}%" for y in YEARS}

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, gross, by purpose", {}),
    ("DATA", "On demand and short notice facilities", AQ_ON_DEMAND),
    ("DATA", "Credit for personal consumption", AQ_PERSONAL),
    ("DATA", "Lending for property purchase or transformation", AQ_PROPERTY),
    ("DATA", "Loans secured on investment portfolios (Lombard loans)", AQ_LOMBARD),
    ("DATA", "Other term loans", AQ_OTHER_TERM),
    ("TOTAL", "Total gross loans and advances to customers", AQ_GROSS_TOTAL),
    ("SECTION", "Expected credit loss (ECL) allowance, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 allowance", {y: -v for y, v in AQ_ECL_S1.items()}),
    ("DATA", "Stage 2 allowance", {y: -v for y, v in AQ_ECL_S2.items()}),
    ("DATA", "Stage 3 allowance", {y: -v for y, v in AQ_ECL_S3.items()}),
    ("TOTAL", "Total ECL allowance", {y: -v for y, v in AQ_ECL_TOTAL.items()}),
    ("TOTAL", "Net loans and advances to customers", AQ_NET_TOTAL),
    ("SECTION", "Ratios", {}),
    ("DATA", "Overall ECL coverage ratio (total allowance / total gross loans)", AQ_COVERAGE),
    ("DATA", "Stage 3 allowance as % of total ECL allowance", AQ_STAGE3_SHARE_OF_ECL),
]

bw.add_asset_quality_sheet(
    title="Brown Shipley & Co. Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Loans and advances to customers, £'000. Company (entity-level) basis.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Brown Shipley & Co. Limited's own Note 14 'Loans and advances to customers' (gross by "
        "purpose, ECL allowance by IFRS 9 stage), transcribed from each year's own Companies House filing:\n"
        f"FY2024: Annual Report 2024, p.57 - {AR2024_URL}\n"
        f"FY2023: Annual Report 2023 (comparative column cross-checked against FY2024's own note) - {AR2023_URL}\n"
        f"FY2022: Annual Report 2022, p.53 - {AR2022_URL}\n"
        f"FY2021: Annual Report 2021 (comparative column cross-checked against FY2022's own note) - {AR2021_URL}\n\n"
        "Note: only the ECL ALLOWANCE is disclosed by IFRS 9 stage - the Bank's own note analyses gross exposure "
        "by loan purpose (shown above) and separately discloses a partial 'Stage 2 transfers' reconciliation, but "
        "never a full gross-exposure-by-stage table for all three stages - confirmed by reading the note in full, "
        "not assumed. Stage 3/NPL exposure ratios (Stage 3 gross / total gross) therefore cannot be derived here; "
        "only the ratios shown above (overall ECL coverage, and Stage 3's share of the total allowance) are "
        "calculable from what's disclosed. The FY2022 gross total (£646,864k) is £2k above the Bank's own "
        "disclosed net-of-ECL figure plus ECL allowance (£646,792k) - an immaterial rounding gap already present "
        "in the Bank's own source tables, not a transcription error (cross-checked against the Balance Sheet's "
        "own Loans and advances to customers figure of £646,794k, which the Note 14 net total matches exactly).\n\n"
        + ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=340,
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
    ["Tier 1 Capital", "Tier 1 Ratio", "Total Capital", "Total Capital Ratio", "Total RWAs"],
    p3_sources(),
    per_note={
        "Tier 1 Capital": NOT_DISCLOSED_NOTE + " Note: the Statement of Financial Position confirms £10,000k of "
                          "Additional Tier 1 Equity Capital exists in every year shown, so Tier 1 capital cannot "
                          "be assumed equal to CET1 capital - not calculated here without a disclosed RWA figure.",
        "Tier 1 Ratio": NOT_DISCLOSED_NOTE,
        "Total Capital": NOT_DISCLOSED_NOTE,
        "Total Capital Ratio": NOT_DISCLOSED_NOTE,
        "Total RWAs": NOT_DISCLOSED_NOTE,
    },
)

bw.add_rwa_breakdown_sheet(
    title="Brown Shipley & Co. Limited — RWA Breakdown",
    subtitle="Not publicly disclosed in any year - see note below.",
    rows=[
        ("SECTION", "RWA by risk category", {}),
        ("TOTAL", "Total RWAs", {y: "Not publicly disclosed" for y in YEARS}),
    ],
    sources_text=p3_sources() + "\n\n" + NOT_DISCLOSED_NOTE + " No RWA figure of any kind (total or by category) "
                 "is published by this entity - only the narrative CET1 ratio and LCR percentages described in "
                 "the Entity note.",
    first_col_width=54,
    source_height=200,
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio"],
    p3_sources(),
    per_note={"Leverage Ratio": NOT_DISCLOSED_NOTE},
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
    balance_sheet_totals=[
        ("Total assets", {"FY2024": 1218044, "FY2023": 1529171, "FY2022": 1507100, "FY2021": 1152277}),
        ("Loans and advances to customers", {"FY2024": 483277, "FY2023": 554649, "FY2022": 646794, "FY2021": 565574}),
        ("Deposits from customers", {"FY2024": 1046365, "FY2023": 1353609, "FY2022": 1321391, "FY2021": 971736}),
        ("Total equity", {"FY2024": 132953, "FY2023": 129139, "FY2022": 130681, "FY2021": 127075}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", {"FY2024": 95421, "FY2023": 95723, "FY2022": 93025, "FY2021": 90882}),
        ("Total operating expenses", {"FY2024": -84365, "FY2023": -91026, "FY2022": -88096, "FY2021": -85479}),
        ("Profit/(loss) for the year", {"FY2024": 4084, "FY2023": -612, "FY2022": 1111, "FY2021": 2908}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2024": 129139, "FY2023": 130681, "FY2022": 127075, "FY2021": 122746}),
        ("Total comprehensive income/(loss) for the year", {"FY2024": 4950, "FY2023": -659, "FY2022": 4257, "FY2021": 4964}),
        ("AT1 coupon paid, net", {"FY2024": -1136, "FY2023": -883, "FY2022": -651, "FY2021": -635}),
        ("Closing equity", {"FY2024": 132953, "FY2023": 129139, "FY2022": 130681, "FY2021": 127075}),
    ],
    equity_changes_unit="£'000",
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
