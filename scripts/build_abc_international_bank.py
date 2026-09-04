import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: ABC International Bank plc (company 02564490, FRN 149025)
# is a qualifying entity under FRS 101 and takes the "requirements of IAS 7 Statement
# of Cash Flows" exemption every year - explicitly stated in note 1.2 of its FY2024
# Annual Report: "there is no requirement to prepare a statement of cash flows in
# accordance with Financial Reporting Standard 101." No Statement of Cash Flows
# exists in any year's accounts. Pillar 3 / capital disclosures are available for all
# 5 years - FY2025's Total RWA/Capital/ratios come from the FY2025 Annual Report's own
# Financial Highlights table (same table used for FY2021-FY2022; visually transcribed,
# see AR2025_URL note below), not a separate Pillar 3 report - no FY2025 Pillar 3 OV1/
# leverage/LCR/NSFR breakdown could be located, so those 4 sheets stay FY2021-FY2024
# only. This follows the BNY Mellon International precedent: standard 13-sheet
# structure, but the Cash Flow Statement sheet documents the exemption instead of line
# items, and the Overview sheet omits the cash-flow chart.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

AR2024_URL = "https://www.bank-abc.com/en/ShareholderRelations/Annual%20Reports/ABC%20IB%20Annual%20Report%202024%20_%20Spreads%20for%20web.pdf"
AR2022_URL = "https://www.bank-abc.com/en/ShareholderRelations/Annual%20Reports/ABCIB%20Annual%20Report%202022.pdf"
P3_2024_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/ABCIB%20Pillar%203%20final%20Board%202024%20.pdf"
P3_2023_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/BH2407109%20-%20Bank%20ABC%20Pillar%203%20Disclosures%202023%20-%20Final%20website%20version.pdf"
# FY2025 Companies House filing (accounts made up to 31 December 2025, filed 2026) IS available - it is
# scanned/image-only (no text layer), so figures below were transcribed by rendering each page to PNG and
# reading it visually (pdf_tools.py render + Read) rather than by text extraction. No separate FY2025 Pillar 3
# report or updated Financial Highlights-format Pillar 3 breakdown (OV1/leverage/LCR/NSFR) could be located on
# ABCIB's website - only the Annual Report's own "Financial Highlights" table (same table used for FY2021/
# FY2022), which gives Total RWA/Capital base/ratios but no category breakdown, leverage, LCR or NSFR.
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/02564490/filing-history"  # Companies House filing history (2026 accounts filing, scanned/image-only PDF)

ENTITY_NOTE = (
    "ENTITY NOTE: ABC International Bank plc (company 02564490, FRN 149025, incorporated 3 December 1990) is a "
    "wholly-owned subsidiary within the Bank ABC (Arab Banking Corporation B.S.C., Bahrain) group. FY2023 and FY2024 "
    "figures are on a CONSOLIDATED basis (ABCIB's own subsidiaries, e.g. Alphabet Nominees Limited - a nominee "
    "company, not a trading entity), taken from ABCIB's own UK KM1 Pillar 3 template. FY2021 and FY2022 figures are "
    "on a SOLO (entity-only) basis, taken from the Annual Report's 'Financial Highlights' table - no consolidated "
    "Pillar 3 KM1-format disclosure could be located for those two years (only the modern KM1 template, introduced "
    "for the FY2023 report onward, publishes a full metrics breakdown; earlier years' Pillar 3 documents could not "
    "be located on the bank's website or via Wayback Machine). This is a genuine basis break within the series, not "
    "a data-entry choice - flagged on every affected sheet."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: ABCIB's FY2024 Annual Report states (Note 1.2, Basis of preparation): \"ABCIB is "
    "not required to prepare group accounts since it qualifies for the exemptions available under Section 401 of "
    "the Companies Act 2006. In addition, there is no requirement to prepare a statement of cash flows in "
    "accordance with Financial Reporting Standard 101,\" and lists among the FRS 101 exemptions taken: \"The "
    f"requirements of IAS 7 Statement of Cash Flows.\" - ABC International Bank plc Annual Report 2024, p.55 - "
    f"{AR2024_URL}. No Statement of Cash Flows exists in any of the entity's published accounts for any year - this "
    "is a standing structural feature of the entity, not a one-off or a data gap. Per the project's established "
    "policy for this exemption (see The Bank of New York Mellon (International) Limited), this workbook is built "
    "as a PILLAR-3-ONLY variant: all 11 Pillar 3 metric sheets are populated below (5 years for the capital/RWA "
    "total and ratio sheets - FY2025 figures come from the FY2025 Annual Report's own Financial Highlights table, "
    "visually transcribed from a scanned filing, same as FY2021/FY2022; 4 of 5 years for Leverage Ratio/LCR/NSFR, "
    "which aren't in that table and have no separate FY2025 Pillar 3 report to draw from), but no cash flow "
    "figures exist to show. See the Overview sheet for the equivalent treatment there."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

BASIS_NOTE = (
    "FY2023-FY2024 shown on a CONSOLIDATED basis (ABCIB Pillar 3 Disclosures, UK KM1 template); FY2021-FY2022 and "
    "FY2025 shown on a SOLO basis (Annual Report Financial Highlights table - no consolidated Pillar 3 disclosure "
    "located for those years). See the Cash Flow Statement sheet's entity note for detail. FY2025's Financial "
    "Highlights table (Total RWA £3,132m, Capital base £517m, Tier 1 ratio 15.0%, Total ratio 16.5%) does not "
    "split CET1 from Tier 1, so CET1/Tier 1 capital £m figures for FY2025 are CALCULATED (RWA x Tier 1 ratio), "
    "same convention as FY2021/FY2022 - see the CET1 Capital sheet note. No Leverage Ratio, LCR or NSFR figure "
    "appears in the FY2025 Financial Highlights table (same gap as FY2021/FY2022), and no separate FY2025 Pillar "
    "3 report could be located, so those 3 sheets remain FY2021-blank/FY2024-only as before."
)


def p3_sources(extra=""):
    return (
        "Sources - ABC International Bank plc:\n"
        f"FY2024 & FY2023 (consolidated): ABC International Bank plc Pillar 3 Report 2024, Table \"UK KM1 - Key "
        f"metrics template\", p.14 - {P3_2024_URL}\n"
        f"FY2023 (consolidated, as originally reported): ABC International Bank plc Pillar 3 Disclosures 2023, "
        f"Table 3: Key Regulatory Metrics, p.13 - {P3_2023_URL}\n"
        f"FY2022 & FY2021 (solo): ABC International Bank plc Annual Report 2022, Financial Highlights, p.31 - "
        f"{AR2022_URL}\n"
        f"FY2025 (solo): ABC International Bank plc Annual Report 2025, Financial Highlights, p.20 (scanned "
        f"Companies House filing, visually transcribed) - {AR2025_URL}\n"
        + (extra + "\n" if extra else "") + BASIS_NOTE
    )


AR2023_URL = AR2024_URL  # FY2023/2024 primary statements both live in the 2024 Annual Report (comparative column)
AR2022B_URL = AR2022_URL  # FY2021/2022 primary statements both live in the 2022 Annual Report (comparative column)

STATEMENTS_ENTITY_NOTE = (
    "ENTITY NOTE: Balance Sheet, Profit & Loss and Statement of Changes in Equity are all prepared on ABCIB's own "
    "SOLO (entity, non-consolidated) FRS 101 basis for every year shown - ABCIB does not prepare group accounts "
    "(Companies Act 2006, Section 401 exemption; the 'Investment in subsidiary' line is the only trace of the "
    "wholly-owned subsidiary Alphabet Nominees Limited on these statements). This is a different basis to the "
    "Pillar 3 sheets, which are CONSOLIDATED for FY2023-FY2024 and SOLO for FY2021-FY2022/FY2025 (see the Cash "
    "Flow Statement sheet's entity note) - flagged here so the two blocks of sheets aren't assumed to be on the "
    "same basis. FY2025 figures were transcribed by rendering the scanned FY2025 Companies House filing to PNG "
    "and reading it visually (pdf_tools.py render + Read), not from a text layer - see AR2025_URL."
)

BALANCE_SHEET_SOURCES = (
    "Sources - ABC International Bank plc:\n"
    f"FY2025: ABC International Bank plc Annual Report 2025, Statement of Financial Position, p.46 (scanned "
    f"filing, visually transcribed) - {AR2025_URL}\n"
    f"FY2024 & FY2023: ABC International Bank plc Annual Report 2024, Statement of Financial Position, p.53 (FY2023 "
    f"restated - see Note 37) - {AR2024_URL}\n"
    f"FY2022 & FY2021: ABC International Bank plc Annual Report 2022, Statement of Financial Position, p.62 - "
    f"{AR2022_URL}\n"
    + STATEMENTS_ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: FY2025 introduces two lines not present in earlier years - 'Investment property' (£5,973k) "
    "and a 'Pension scheme liability' of £163k (FY2024 instead showed a net 'Pension scheme asset' of £1,347k, "
    "now nil) - both are new/changed, not omissions, and are shown as disclosed."
)

INCOME_STATEMENT_SOURCES = (
    "Sources - ABC International Bank plc:\n"
    f"FY2025: ABC International Bank plc Annual Report 2025, Statement of Comprehensive Income, p.45 (scanned "
    f"filing, visually transcribed) - {AR2025_URL}\n"
    f"FY2024 & FY2023: ABC International Bank plc Annual Report 2024, Statement of Comprehensive Income, p.52 "
    f"(FY2023 restated - see Note 37) - {AR2024_URL}\n"
    f"FY2022 & FY2021: ABC International Bank plc Annual Report 2022, Statement of Comprehensive Income, p.61 - "
    f"{AR2022_URL}\n"
    + STATEMENTS_ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: ABCIB's statement of comprehensive income is presented net of interest/fee income and "
    "expense from the top (\"Profit for the year attributable to owners\" is the first disclosed line, with "
    "expense items not broken out above it) - there is no Revenue/Net operating income subtotal structure "
    "disclosed for any year, unlike Monzo's workbook. \"Total comprehensive income for the year\" is the one row "
    "comparable and populated across all 5 years.\n\n"
    "DISCREPANCY FLAGGED (found while sourcing FY2025, not fixed - out of scope for this pass): AR2024's own OCI "
    "line items for FY2024 (as directly re-verified against the source PDF: Foreign exchange movement 155, "
    "Actuarial gain 36, tax (69), FVOCI tax (333), FVOCI change (1,044), reclassification 1,954, ECL 4, fair "
    "value hedging 423) sum to +1,126, but AR2024's own disclosed 'Total comprehensive income' row implies a "
    "total OCI of only +35 (34,148 - 34,113 profit) - the components do not reconcile to AR2024's own total, "
    "which is a defect in the primary source, not a transcription error (both re-verified directly against the "
    "PDF text). AR2025's FY2024 comparative column uses a different item set (no separate FX line; Actuarial "
    "(1,055) not 36; fair value hedging 578 not 423) that DOES reconcile to 35 exactly. The FY2024 figures below "
    "are left as originally sourced from AR2024 (each year sourced from its own primary report, per this "
    "project's convention) rather than silently swapped to AR2025's restated figures - a genuine unresolved "
    "reconciliation gap in ABCIB's own disclosures, flagged here for a human to judge. FY2021-FY2023 were not "
    "re-checked for the same issue (out of scope for this pass)."
)

EQUITY_CHANGES_SOURCES = (
    "Sources - ABC International Bank plc:\n"
    f"FY2021-FY2022 roll-forward: ABC International Bank plc Annual Report 2022, Statement of Changes in Equity, "
    f"p.62 - {AR2022_URL}\n"
    f"FY2023-FY2024 roll-forward: ABC International Bank plc Annual Report 2024, Statement of Changes in Equity, "
    f"p.54 (FY2023 restated - see Note 37; opening 1 Jan 2023 balance not materially affected) - {AR2024_URL}\n"
    f"FY2025 roll-forward: ABC International Bank plc Annual Report 2025, Statement of Changes in Equity, p.47 "
    f"(scanned filing, visually transcribed) - {AR2025_URL}\n"
    + STATEMENTS_ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - ABC International Bank plc:\n"
    f"FY2025 IFRS 9 stage roll-forward: ABC International Bank plc Annual Report 2025, Note 11 (Loans and advances "
    f"to customers), p.62 (scanned filing, visually transcribed) - {AR2025_URL}\n"
    f"FY2023-FY2024 IFRS 9 stage roll-forward: ABC International Bank plc Annual Report 2024, Note 11 (Loans and "
    f"advances to customers), p.76-77 - {AR2024_URL}\n"
    f"FY2021-FY2022 IFRS 9 stage roll-forward: ABC International Bank plc Annual Report 2022, Note 11, p.87-89 - "
    f"{AR2022_URL}\n"
    + STATEMENTS_ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: No by-product breakdown of the loan book is disclosed (a single 'Loans and advances to "
    "customers' line only) - only the IFRS 9 stage 1/2/3 breakdown, shown here. Ratios are calculated from the "
    "disclosed gross carrying amount and ECL allowance figures. FY2025's Stage 1/Stage 3 gross figures include "
    "£60.5m/£1.5m of credit enhancements via export credit agency guarantee respectively (per the Annual Report's "
    "own footnote) - shown gross, as disclosed, not netted down."
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - ABC International Bank plc (CONSOLIDATED basis, matching the Total RWAs sheet):\n"
    f"FY2024 & FY2023 (FY2023 as originally reported by the FY2024 report's own comparative column - no separate "
    f"OV1 breakdown exists in ABCIB's own FY2023 Pillar 3 Disclosures document, which only carries Table 3's "
    f"single Total RWA figure, not a category breakdown): ABC International Bank plc Pillar 3 Report 2024, Table "
    f"\"UK OV1 - Overview of risk weighted exposure amounts\", ABCIB CONSOLIDATED, p.14 - {P3_2024_URL}\n"
    "FY2022, FY2021 & FY2025: not available - no OV1-format RWA category breakdown exists for these years, only "
    "the single Total RWA figure in the Annual Report's Financial Highlights table (see Total RWAs sheet). No "
    "separate FY2025 Pillar 3 report could be located on ABCIB's website."
)


bw = BankWorkbook(bank_name="ABC International Bank plc", years=YEARS, year_label=YEAR_LABEL, header_color="0D7377")

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Consolidated -> actually SOLO, see entity note)
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 103934, "FY2024": 373606, "FY2023": 535241, "FY2022": 133298, "FY2021": 8395}),
    ("DATA", "Debt investments - FVOCI", {"FY2025": 562145, "FY2024": 550345, "FY2023": 494318, "FY2022": 574839, "FY2021": 466103}),
    ("DATA", "Loans and advances to banks", {"FY2025": 1164047, "FY2024": 896970, "FY2023": 604546, "FY2022": 1036596, "FY2021": 1002776}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1540521, "FY2024": 1368632, "FY2023": 1290334, "FY2022": 1101772, "FY2021": 1094131}),
    ("DATA", "Derivative financial assets", {"FY2025": 4859, "FY2024": 20825, "FY2023": 4038, "FY2022": 3704, "FY2021": 3606}),
    ("DATA", "Tangible fixed assets", {"FY2025": 29127, "FY2024": 35131, "FY2023": 35215, "FY2022": 35409, "FY2021": 36270}),
    ("DATA", "Investment property", {"FY2025": 5973}),
    ("DATA", "Current tax asset", {"FY2025": 1104, "FY2024": 889, "FY2022": 0, "FY2021": 127}),
    ("DATA", "Deferred tax asset", {"FY2022": 2149, "FY2021": 1574}),
    ("DATA", "Prepayments, accrued income and other debtors", {"FY2025": 44993, "FY2024": 75609, "FY2023": 62556, "FY2022": 88821, "FY2021": 27093}),
    ("DATA", "Pension scheme asset", {"FY2025": 0, "FY2024": 1347}),
    ("DATA", "Investment in subsidiary", {"FY2025": 171713, "FY2024": 163776, "FY2023": 171043, "FY2022": 174302, "FY2021": 165804}),
    ("TOTAL", "Total assets", {"FY2025": 3628416, "FY2024": 3487130, "FY2023": 3197291, "FY2022": 3150890, "FY2021": 2805879}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 1801577, "FY2024": 1793118, "FY2023": 1719290, "FY2022": 1604268, "FY2021": 1711980}),
    ("DATA", "Customer deposits", {"FY2025": 796992, "FY2024": 588657, "FY2023": 460063, "FY2022": 517193, "FY2021": 238737}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 1644, "FY2024": 1190, "FY2023": 13647, "FY2022": 10516, "FY2021": 635}),
    ("DATA", "Other liabilities, accruals and deferred income", {"FY2025": 61776, "FY2024": 208793, "FY2023": 168234, "FY2022": 195399, "FY2021": 102982}),
    ("DATA", "Current tax liability", {"FY2023": 491, "FY2022": 2286}),
    ("DATA", "Term borrowing", {"FY2025": 315538, "FY2024": 256013, "FY2023": 216093, "FY2022": 224794, "FY2021": 164793}),
    ("DATA", "Pension scheme liability", {"FY2025": 163, "FY2023": 209, "FY2022": 2733, "FY2021": 2621}),
    ("DATA", "Subordinated liabilities", {"FY2025": 48263, "FY2024": 51869, "FY2023": 51121, "FY2022": 50000, "FY2021": 50000}),
    ("DATA", "Deferred tax liability", {"FY2025": 1409, "FY2024": 1016, "FY2023": 11}),
    ("TOTAL", "Total liabilities", {"FY2025": 3027362, "FY2024": 2900656, "FY2023": 2629159, "FY2022": 2607189, "FY2021": 2271748}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 212296, "FY2024": 212296, "FY2023": 212296, "FY2022": 212296, "FY2021": 212296}),
    ("DATA", "Retained earnings", {"FY2025": 385710, "FY2024": 372922, "FY2023": 355584, "FY2022": 334086, "FY2021": 321493}),
    ("DATA", "Fair value reserve", {"FY2025": 3048, "FY2024": 1256, "FY2023": 252, "FY2022": -2681, "FY2021": 342}),
    ("TOTAL", "Total equity", {"FY2025": 601054, "FY2024": 586474, "FY2023": 568132, "FY2022": 543701, "FY2021": 534131}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 3628416, "FY2024": 3487130, "FY2023": 3197291, "FY2022": 3150890, "FY2021": 2805879}),
]

bw.add_balance_sheet_sheet(
    title="ABC International Bank plc — Statement of Financial Position",
    subtitle="Entity (solo) basis, all figures in £'000. Blank cells indicate that year's report did not disclose that specific line.",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Comprehensive income", {}),
    ("TOTAL", "Profit for the year attributable to owners", {"FY2025": 32616, "FY2024": 34113, "FY2023": 28022, "FY2022": 22069, "FY2021": 25344}),
    ("SECTION", "Items that cannot be reclassified to income statement", {}),
    ("DATA", "Foreign exchange movement", {"FY2024": 155, "FY2023": 22, "FY2022": -10}),
    ("DATA", "Actuarial gain / (loss) recognised on defined benefit pension scheme", {"FY2025": -3431, "FY2024": 36, "FY2023": -1055, "FY2022": -2676, "FY2021": 7756}),
    ("DATA", "Current and Deferred tax (charge) / credit relating to defined benefit pension scheme", {"FY2025": 703, "FY2024": -69, "FY2023": -37, "FY2022": 480, "FY2021": -1431}),
    ("SECTION", "Items that can be reclassified to income statement", {}),
    ("DATA", "Deferred tax (charge) / credit relating to change in fair value of debt investments at FVOCI", {"FY2025": -420, "FY2024": -333, "FY2023": -988, "FY2022": 964, "FY2021": 205}),
    ("DATA", "Change in fair value of debt investments at FVOCI", {"FY2025": 4060, "FY2024": -1044, "FY2023": 2406, "FY2022": -6637, "FY2021": -765}),
    ("DATA", "Reclassification to income statement: debt investments at FVOCI", {"FY2025": 549, "FY2024": 1954, "FY2023": 3421, "FY2022": -85, "FY2021": -282}),
    ("DATA", "Change in ECL allowance for debt investments at FVOCI", {"FY2025": 6, "FY2024": 4, "FY2023": -33, "FY2022": 12, "FY2021": 2}),
    ("DATA", "Net gain / (loss) due to fair value hedging", {"FY2025": -2403, "FY2024": 423, "FY2023": -1873, "FY2022": 2723, "FY2021": 145}),
    ("TOTAL", "Total comprehensive income for the year attributable to owners", {"FY2025": 31680, "FY2024": 34148, "FY2023": 31051, "FY2022": 16840, "FY2021": 30974}),
]

bw.add_income_statement_sheet(
    title="ABC International Bank plc — Statement of Comprehensive Income",
    subtitle="Entity (solo) basis, all figures in £'000. Blank cells indicate that year's report did not disclose that specific line.",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity (chronological, oldest -> newest)
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Retained earnings", "Fair value reserve", "Total equity"]
equity_changes_rows = [
    ("TOTAL", "Balance at 1 January 2021", (212296, 289824, 1037, 503157)),
    ("DATA", "Profit for the year", (None, 25344, None, 25344)),
    ("DATA", "Other comprehensive income / (loss)", (None, 6325, -695, 5630)),
    ("TOTAL", "Balance at 31 December 2021", (212296, 321493, 342, 534131)),
    ("DATA", "Dividend paid", (None, -7270, None, -7270)),
    ("DATA", "Profit for the year", (None, 22069, None, 22069)),
    ("DATA", "Other comprehensive income / (loss)", (None, -2206, -3023, -5229)),
    ("TOTAL", "Balance at 31 December 2022", (212296, 334086, -2681, 543701)),
    ("DATA", "Dividend paid", (None, -6620, None, -6620)),
    ("DATA", "Profit for the year", (None, 28022, None, 28022)),
    ("DATA", "Other comprehensive income / (loss)", (None, 96, 2933, 3029)),
    ("TOTAL", "Balance at 31 December 2023", (212296, 355584, 252, 568132)),
    ("DATA", "Dividend paid", (None, -15806, None, -15806)),
    ("DATA", "Profit for the year", (None, 34113, None, 34113)),
    ("DATA", "Other comprehensive income / (loss)", (None, -969, 1004, 35)),
    ("TOTAL", "Balance at 31 December 2024", (212296, 372922, 1256, 586474)),
    ("DATA", "Dividend paid", (None, -17100, None, -17100)),
    ("DATA", "Profit for the year", (None, 32616, None, 32616)),
    ("DATA", "Other comprehensive income / (loss)", (None, -2728, 1792, -936)),
    ("TOTAL", "Balance at 31 December 2025", (212296, 385710, 3048, 601054)),
]

bw.add_equity_changes_sheet(
    title="ABC International Bank plc — Statement of Changes in Equity",
    subtitle="Entity (solo) basis, chronological, all figures in £'000.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="ABC International Bank plc — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=280,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers - gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 1508403, "FY2024": 1332380, "FY2023": 1225745, "FY2022": 979678, "FY2021": 944168}),
    ("DATA", "Stage 2 (underperforming / SICR)", {"FY2025": 5752, "FY2024": 6075, "FY2023": 41723, "FY2022": 108221, "FY2021": 160564}),
    ("DATA", "Stage 3 (credit-impaired / non-performing)", {"FY2025": 45704, "FY2024": 46882, "FY2023": 39868, "FY2022": 25547, "FY2021": 1311}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 1559859, "FY2024": 1385337, "FY2023": 1307336, "FY2022": 1113446, "FY2021": 1106043}),
    ("SECTION", "Loans and advances to customers - ECL allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1 ECL allowance", {"FY2025": 1164, "FY2024": 1524, "FY2023": 1096, "FY2022": 1569, "FY2021": 464}),
    ("DATA", "Stage 2 ECL allowance", {"FY2025": 33, "FY2024": 9, "FY2023": 31, "FY2022": 3636, "FY2021": 10137}),
    ("DATA", "Stage 3 ECL allowance", {"FY2025": 18141, "FY2024": 15172, "FY2023": 15875, "FY2022": 6469, "FY2021": 1311}),
    ("TOTAL", "Total ECL allowance", {"FY2025": 19338, "FY2024": 16705, "FY2023": 17002, "FY2022": 11674, "FY2021": 11912}),
    ("SECTION", "Loans and advances to customers - net carrying amount", {}),
    ("TOTAL", "Net carrying amount", {"FY2025": 1540521, "FY2024": 1368632, "FY2023": 1290334, "FY2022": 1101772, "FY2021": 1094131}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross)", {"FY2025": "2.93%", "FY2024": "3.38%", "FY2023": "3.05%", "FY2022": "2.29%", "FY2021": "0.12%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", {"FY2025": "39.69%", "FY2024": "32.36%", "FY2023": "39.82%", "FY2022": "25.32%", "FY2021": "100.00%"}),
    ("DATA", "Overall ECL coverage ratio (Total ECL / Total gross)", {"FY2025": "1.24%", "FY2024": "1.21%", "FY2023": "1.30%", "FY2022": "1.05%", "FY2021": "1.08%"}),
]

bw.add_asset_quality_sheet(
    title="ABC International Bank plc — Asset Quality / Credit Risk Disclosures",
    subtitle="Loans and advances to customers only, entity (solo) basis, all figures in £'000. IFRS 9 stage breakdown; no by-product split disclosed.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=150)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 469.8, "FY2024": 564.579, "FY2023": 547.665, "FY2022": 416.5, "FY2021": 418.8})],
    p3_sources(),
    note="FY2025/FY2022/FY2021 are calculated (RWA x Tier 1 ratio, all solo basis) - no separate CET1/Tier 1 £m "
         "figure is disclosed for those years, only the ratio and total 'Capital base'. Assumes CET1 = Tier 1 (no "
         "AT1 instruments in issue), consistent with the pattern directly confirmed in FY2023-FY2024.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "15.0%", "FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%"})],
    p3_sources(),
    note="FY2023 shown as originally reported (17.6%, consolidated); the FY2024 Pillar 3 Report's FY2023 "
         "comparative column restates this to 17.7% alongside a small RWA restatement (see Total RWAs sheet) - "
         "immaterial, but shown as originally reported per this project's convention. FY2022/FY2021/FY2025 "
         "labelled 'Tier 1 Capital Ratio' (a.k.a. 'Risk asset ratio - Tier 1') in the source (solo basis) - "
         "assumed equal to CET1 ratio, see CET1 Capital sheet note.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 469.8, "FY2024": 564.579, "FY2023": 547.665, "FY2022": 416.5, "FY2021": 418.8})],
    p3_sources(),
    note="Tier 1 = CET1 every year (no AT1 instruments in issue). FY2025/FY2022/FY2021 calculated - see CET1 "
         "Capital sheet note.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "15.0%", "FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%"})],
    p3_sources(),
    note="FY2023 shown as originally reported (consolidated) - see CET1 Ratio sheet note.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 517, "FY2024": 616.448, "FY2023": 598.786, "FY2022": 447, "FY2021": 460})],
    p3_sources(),
    note="FY2022/FY2021/FY2025 ('Capital base') and FY2023-FY2024 ('Total capital') are directly disclosed, not "
         "calculated.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "16.5%", "FY2024": "17.7%", "FY2023": "19.3%", "FY2022": "18.2%", "FY2021": "18.3%"})],
    p3_sources(),
    note="FY2025 labelled 'Risk asset ratio - Total' in the Financial Highlights table.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 3132, "FY2024": 3486.256, "FY2023": 3104.763, "FY2022": 2450, "FY2021": 2508})],
    p3_sources(),
    note="FY2023 shown as originally reported (consolidated, 3,104.763m); the FY2024 Pillar 3 Report's FY2023 "
         "comparative column restates this to 3,101.197m - immaterial (~0.1%), shown as originally reported per "
         "this project's convention. FY2025 (3,132m, solo basis, Financial Highlights table 'Risk weighted "
         "assets') is genuinely lower than FY2024's consolidated 3,486.256m - a basis effect (solo excludes "
         "Alphabet Nominees Limited), not a real risk reduction; see BASIS_NOTE.",
)

rwa_breakdown_rows = [
    ("SECTION", "UK OV1 — Overview of risk weighted exposure amounts (CONSOLIDATED)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2024": 3198514, "FY2023": 2842771}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2024": 45144, "FY2023": 55407}),
    ("DATA", "Of which: credit valuation adjustment (CVA)", {"FY2024": 10131, "FY2023": 11788}),
    ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2024": 14469, "FY2023": 5670}),
    ("DATA", "Operational risk", {"FY2024": 217998, "FY2023": 185561}),
    ("TOTAL", "Total risk weighted exposure amount", {"FY2024": 3486256, "FY2023": 3101197}),
]

bw.add_rwa_breakdown_sheet(
    title="ABC International Bank plc — RWA Breakdown",
    subtitle="CONSOLIDATED basis, all figures in £'000. Matches the Total RWAs sheet.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks (£m)", {"FY2024": 5540.164, "FY2023": 5155.039}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2024": "10.2%", "FY2023": "10.62%"}),
    ],
    p3_sources(),
    note="FY2022/FY2021/FY2025 not available - the Annual Report Financial Highlights table (the only source "
         "located for those years) does not include a leverage ratio.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value - average (£m)", {"FY2024": 854.893, "FY2023": 699.862}),
        ("Total net cash outflows, adjusted value (£m)", {"FY2024": 252.133, "FY2023": 189.675}),
        ("Liquidity Coverage Ratio (%)", {"FY2024": "339.1%", "FY2023": "369.0%"}),
    ],
    p3_sources(),
    note="FY2023 LCR is sourced from the FY2024 Pillar 3 Report's comparative column - ABCIB's own FY2023 Pillar 3 "
         "Disclosures document (Table 3) does not include LCR at all (only capital and leverage metrics). "
         "FY2022/FY2021/FY2025 not available.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2024": 2339.367, "FY2023": 2053.004}),
        ("Total required stable funding (£m)", {"FY2024": 1802.627, "FY2023": 1504.583}),
        ("Net Stable Funding Ratio (%)", {"FY2024": "129.8%", "FY2023": "136.4%"}),
    ],
    p3_sources(),
    note="FY2023 NSFR is sourced from the FY2024 Pillar 3 Report's comparative column - same reason as the LCR "
         "sheet. FY2022/FY2021/FY2025 not available.",
)

metric(
    "MREL Ratio", "£m / %",
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL figure (numeric or qualitative) appears in either Pillar 3 Report reviewed for this entity - no "
         "reason is stated. ABCIB's balance sheet size (~£3.5-4.3bn) is well below the thresholds at which the "
         "Bank of England typically sets an independent MREL requirement, consistent with no disclosure existing.",
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 3628416, "FY2024": 3487130, "FY2023": 3197291, "FY2022": 3150890, "FY2021": 2805879}),
        ("Loans and advances to customers", {"FY2025": 1540521, "FY2024": 1368632, "FY2023": 1290334, "FY2022": 1101772, "FY2021": 1094131}),
        ("Customer deposits", {"FY2025": 796992, "FY2024": 588657, "FY2023": 460063, "FY2022": 517193, "FY2021": 238737}),
        ("Total equity", {"FY2025": 601054, "FY2024": 586474, "FY2023": 568132, "FY2022": 543701, "FY2021": 534131}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Profit for the year attributable to owners", {"FY2025": 32616, "FY2024": 34113, "FY2023": 28022, "FY2022": 22069, "FY2021": 25344}),
        ("Total comprehensive income for the year", {"FY2025": 31680, "FY2024": 34148, "FY2023": 31051, "FY2022": 16840, "FY2021": 30974}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 586474, "FY2024": 568132, "FY2023": 543701, "FY2022": 534131, "FY2021": 503157}),
        ("Total comprehensive income for the year", {"FY2025": 31680, "FY2024": 34148, "FY2023": 31051, "FY2022": 16840, "FY2021": 30974}),
        ("Other equity movements, net (dividends)", {"FY2025": -17100, "FY2024": -15806, "FY2023": -6620, "FY2022": -7270, "FY2021": 0}),
        ("Closing equity", {"FY2025": 601054, "FY2024": 586474, "FY2023": 568132, "FY2022": 543701, "FY2021": 534131}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.0%", "FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%"}),
        ("Tier 1 Ratio", {"FY2025": "15.0%", "FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%"}),
        ("Total Capital Ratio", {"FY2025": "16.5%", "FY2024": "17.7%", "FY2023": "19.3%", "FY2022": "18.2%", "FY2021": "18.3%"}),
        ("Leverage Ratio (excl. central bank claims)", {"FY2024": "10.2%", "FY2023": "10.62%"}),
        ("LCR", {"FY2024": "339.1%", "FY2023": "369.0%"}),
        ("NSFR", {"FY2024": "129.8%", "FY2023": "136.4%"}),
    ],
    note="ABC International Bank plc takes the FRS 101 cash-flow-statement exemption every year (see the Cash Flow "
         "Statement sheet), so no cash flow summary or chart is shown here - only the Balance Sheet / P&L / Equity "
         "blocks (all entity/solo basis) and the Pillar 3 Key Metrics trend chart below. Pillar 3 ratios are "
         "consolidated basis for FY2023-FY2024 and solo basis for FY2021-FY2022/FY2025 - a different basis to the "
         "statement blocks above, see the Cash Flow Statement sheet's entity note. FY2025's statement/asset-"
         "quality figures were transcribed from a scanned Companies House filing via visual reading (OCR-style); "
         "FY2025 Leverage Ratio/LCR/NSFR remain unavailable (not in the Annual Report's Financial Highlights "
         "table, and no separate FY2025 Pillar 3 report could be located) - see each sheet's own source citation.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ABC INTERNATIONAL BANK FINANCIALS.xlsx")
