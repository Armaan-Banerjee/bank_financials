import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04152338/filing-history/MzUyNjMyOTE4OGFkaXF6a2N4/document?download=0&format=pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/04152338/filing-history/MzQ3MDI0ODU4NWFkaXF6a2N4/document?download=0&format=pdf"
AR2023_URL = "https://vpr.hkma.gov.hk/statics/assets/doc/100273/ar_23/ar_23_eng.pdf"
AR2022_URL = "https://vpr.hkma.gov.hk/statics/assets/doc/100273/ar_22/ar_22_eng.pdf"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/04152338/filing-history/MzM0MzE1NzIzOWFkaXF6a2N4/document?download=0&format=pdf"

ENTITY_NOTE = (
    "ENTITY AND REPORTING BASIS: Melli Bank plc (company 04152338, FRN 207380, LEI "
    "213800BC4TEGCCQH9V07) is an active UK public limited company and PRA-authorised bank, "
    "incorporated in England and Wales. Companies House identifies the registered office as "
    "98a Kensington High Street, London W8 4SG and the latest accounts as made up to 31 December "
    "2025. The Bank's functional and reporting currency is EUR; amounts are therefore retained in "
    "EUR thousands/millions, consistent with the source accounts. The figures are standalone Melli "
    "Bank plc entity figures, not Bank Melli Iran group figures."
)

CASH_FLOW_SOURCES = (
    "Sources - Melli Bank plc entity-level Statements of Cash Flows:\n"
    f"FY2025: Annual Report and Accounts 2025, Statement of Cash Flows p.26 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Accounts 2024, p.24; also shown as the FY2025 report's own comparative column, "
    f"p.26 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts 2023, p.24 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts 2023 comparative column, p.24 - {AR2023_URL}\n"
    "FY2021: genuinely not disclosed, confirmed by two independent checks of the Annual Report 2021 - its "
    "accounting policy note (ii) 'Cash flow exemptions' (p.23) states the Company applied the FRS 102 exemption "
    "from producing a statement of cash flows because it was consolidated with Bank Melli Iran, and its own "
    "Contents page (p.2) lists no Statement of Cash Flows among the report's financial statements at all. This "
    "is a structural non-disclosure at the source, not a retrieval gap - re-confirmed this batch by re-reading "
    f"the full PDF - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Melli Bank plc entity-level regulatory KPI and capital disclosures:\n"
        f"FY2024/FY2023: Annual Report and Accounts 2024, KPI p.9 and capital management p.49 - {AR2024_URL}\n"
        f"FY2023/FY2022/FY2021: Annual Report and Accounts 2023, KPI p.9 and capital management p.49 - {AR2023_URL}\n"
        f"FY2021 comparative context: Annual Report 2021, KPI p.8 and capital management p.46 - {AR2021_URL}\n"
        f"FY2025: the Companies House filing is listed, but the PDF was not retrievable in this run - {AR2025_URL}\n"
        "The 2022-2024 reports state that Pillar 3 disclosure is available on request; no public current "
        "Pillar 3/KM1 document or defensible entity-level interim series was located."
    )


bw = BankWorkbook(
    bank_name="Melli Bank plc",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="6E4B3A",
)

# ---------------------------------------------------------------
# Statement sources - entity-level Annual Report statements, all 5 years
# now reachable this session (FY2025's Companies House PDF, previously
# noted as "not retrievable in this run" for the Cash Flow Statement sheet,
# was successfully downloaded and read for this batch - see the Balance
# Sheet/P&L/Equity/Asset Quality sheets below; the Cash Flow Statement
# sheet itself is left unchanged per this ticket's scope).
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - Melli Bank plc entity-level Balance Sheet/Profit and Loss Account/Statement of Change in "
    "Equity/Notes 9 and 11 (Loans and advances - customers / Impairment provisions):\n"
    f"FY2025: Annual Report and Accounts 2025, Balance Sheet p.24, Profit and Loss Account p.22, Statement of "
    f"Change in Equity p.25, Note 9 p.39-40, Note 11 p.41 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Accounts 2024, Balance Sheet p.22, Profit and Loss Account p.20, Statement of "
    f"Change in Equity p.23, Note 9 p.34-35, Note 11 p.36 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts 2023, Balance Sheet p.22, Profit and Loss Account p.20, Statement of "
    f"Change in Equity p.23, Note 9 p.34-35, Note 11 p.36 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts 2023 comparative column (same pages as FY2023 above) - {AR2023_URL}\n"
    f"FY2021: Annual Report 2021, Balance Sheet p.21, Profit and Loss Account p.19, Statement of Comprehensive "
    f"Income p.20, Statement of Change in Equity p.22, Note 9 p.32-33 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder confirmed: every year's own
# closing Total Equity ties exactly to both the next year's own opening
# balance and that year's own Statement of Change in Equity closing row.
# Zero plug rows needed anywhere across all 5 years.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 30504, "FY2024": 52378, "FY2023": 39289, "FY2022": 66955, "FY2021": 119058}),
    ("DATA", "Other financial balances (correspondent-bank balances not meeting the cash-equivalent criteria due to sanctions-related external restrictions - first appears FY2025)", {"FY2025": 71070}),
    ("DATA", "Loans and advances to banks", {"FY2025": 248695, "FY2024": 304655, "FY2023": 294073, "FY2022": 234811, "FY2021": 177182}),
    ("DATA", "Loans and advances to customers", {"FY2025": 3317, "FY2024": 3709, "FY2023": 8275, "FY2022": 8260, "FY2021": 8899}),
    ("DATA", "Tangible assets", {"FY2025": 3392, "FY2024": 3364, "FY2023": 3513, "FY2022": 3509, "FY2021": 3643}),
    ("DATA", "Intangible assets", {"FY2025": 109, "FY2024": 529, "FY2023": 81, "FY2022": 219, "FY2021": 513}),
    ("DATA", "Other assets (FY2021 shown per that year's own combined 'Debtors' line - see subtitle)", {"FY2025": 2545, "FY2024": 4473, "FY2023": 4176, "FY2022": 4970, "FY2021": 4438}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 3243, "FY2024": 6433, "FY2023": 5910, "FY2022": 1329}),
    ("DATA", "Derivative assets", {"FY2024": 0, "FY2023": 271, "FY2022": 136}),
    ("TOTAL", "Total assets", {"FY2025": 362875, "FY2024": 375541, "FY2023": 355588, "FY2022": 320189, "FY2021": 313733}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 95095, "FY2024": 108461, "FY2023": 91412, "FY2022": 54081, "FY2021": 50725}),
    ("DATA", "Customer accounts", {"FY2025": 2973, "FY2024": 3248, "FY2023": 3820, "FY2022": 3980, "FY2021": 4004}),
    ("DATA", "Other liabilities", {"FY2025": 1184, "FY2024": 1238, "FY2023": 505, "FY2022": 1079, "FY2021": 1033}),
    ("DATA", "Accruals and deferred income", {"FY2025": 4674, "FY2024": 3930, "FY2023": 3319, "FY2022": 4919, "FY2021": 2048}),
    ("DATA", "Derivative liabilities", {"FY2025": 104, "FY2021": 311}),
    ("TOTAL", "Total liabilities", {"FY2025": 104030, "FY2024": 116877, "FY2023": 99056, "FY2022": 64059, "FY2021": 58121}),
    ("SECTION", "Shareholder's funds", {}),
    ("DATA", "Called up share capital", {"FY2025": 264412, "FY2024": 264412, "FY2023": 264412, "FY2022": 264412, "FY2021": 264412}),
    ("DATA", "Retained earnings / Accumulated losses", {"FY2025": -5567, "FY2024": -5748, "FY2023": -7880, "FY2022": -8282, "FY2021": -8800}),
    ("DATA", "Other reserves", {"FY2021": 0}),
    ("TOTAL", "Total equity", {"FY2025": 258845, "FY2024": 258664, "FY2023": 256532, "FY2022": 256130, "FY2021": 255612}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 362875, "FY2024": 375541, "FY2023": 355588, "FY2022": 320189, "FY2021": 313733}),
]

bw.add_balance_sheet_sheet(
    title="Melli Bank plc — Balance Sheet",
    subtitle="Entity-level basis, EUR '000. FY2021's own accounts combine Other assets/Prepayments and accrued income/Derivative "
              "assets into a single 'Debtors' line (4,438) - shown here under Other assets, not blended with later years' split "
              "presentation. FY2025 introduces a new 'Other financial balances' line (correspondent-bank balances that no longer "
              "meet the cash-equivalent criteria due to sanctions-related external restrictions imposed 29 September 2025).",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=100,
    source_height=280,
    unit_suffix=" (EUR '000)",
)

# ---------------------------------------------------------------
# Profit & Loss - each year's own reported structure preserved as-is
# (genuine structural differences across years, not blended).
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2025": 11658, "FY2024": 13344, "FY2023": 10089, "FY2022": 10725, "FY2021": 3694}),
    ("DATA", "Interest expense (FY2021's own account shows this as a positive net recovery, +14 - transcribed as reported)", {"FY2025": -994, "FY2024": -2016, "FY2023": -1558, "FY2022": -200, "FY2021": 14}),
    ("TOTAL", "Net interest income", {"FY2025": 10664, "FY2024": 11328, "FY2023": 8531, "FY2022": 10525, "FY2021": 3708}),
    ("DATA", "Fees and commission(s) receivable", {"FY2025": 2317, "FY2024": 1356, "FY2023": 55, "FY2022": 73, "FY2021": 80}),
    ("DATA", "Fees and commission(s) payable", {"FY2025": -57, "FY2024": -174, "FY2023": -253, "FY2022": -1171, "FY2021": -40}),
    ("DATA", "Foreign exchange gains/(losses)", {"FY2025": -638, "FY2024": 255, "FY2023": -44, "FY2022": -206, "FY2021": 28}),
    ("DATA", "Other operating income", {"FY2021": 1}),
    ("TOTAL", "Total revenue / Total net income (FY2025's own report relabels this subtotal 'Total net income' - same position in the account, not a different line)", {"FY2025": 12286, "FY2024": 12765, "FY2023": 8289, "FY2022": 9221, "FY2021": 3777}),
    ("DATA", "Administrative expenses", {"FY2025": -11439, "FY2024": -9065, "FY2023": -7495, "FY2022": -8202, "FY2021": -7711}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -666, "FY2024": -365, "FY2023": -392, "FY2022": -475, "FY2021": -743}),
    ("DATA", "Other charges - DB Pension Scheme / Other income (same underlying pension remeasurement item, presented as an add-back 'Other charges' in FY2024/FY2025's own account and as 'Other income' in FY2023/FY2022's own account)", {"FY2025": 0, "FY2024": 224, "FY2023": 228, "FY2022": 41, "FY2021": 12}),
    ("TOTAL", "Operating profit/(loss) (FY2021's own subtotal position, before Other charges)", {"FY2021": -4677}),
    ("TOTAL", "Profit before provision and taxation (FY2022/FY2023's own subtotal position, after Other income)", {"FY2023": 630, "FY2022": 585}),
    ("DATA", "Impairment - other / Impairment on loans and advances", {"FY2025": 0, "FY2024": -1203, "FY2023": 0, "FY2022": -26, "FY2021": -2643}),
    ("TOTAL", "Profit/(loss) before taxation", {"FY2025": 181, "FY2024": 2356, "FY2023": 630, "FY2022": 559, "FY2021": -7308}),
    ("DATA", "Tax", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Profit/(loss) for the financial year", {"FY2025": 181, "FY2024": 2356, "FY2023": 630, "FY2022": 559, "FY2021": -7308}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Remeasurements of net defined benefit pension obligations", {"FY2025": 0, "FY2024": -224, "FY2023": -228, "FY2022": -41, "FY2021": -12}),
    ("DATA", "Movement in other reserves", {"FY2021": 0}),
    ("TOTAL", "Other comprehensive income/(loss) for the year", {"FY2025": 0, "FY2024": -224, "FY2023": -228, "FY2022": -41, "FY2021": -12}),
    ("TOTAL", "Total comprehensive income/(loss) for the year, net of tax", {"FY2025": 181, "FY2024": 2132, "FY2023": 402, "FY2022": 518, "FY2021": -7320}),
]

bw.add_income_statement_sheet(
    title="Melli Bank plc — Profit & Loss",
    subtitle="Entity-level basis, EUR '000. Structure genuinely differs year to year (Total revenue/Operating profit/Other income "
              "structure in FY2021-FY2023 vs Total net income/Other charges structure in FY2024-FY2025 - same pension remeasurement "
              "item presented on opposite sides of the account) - each year shown on its own reported basis, not forced into one "
              "template. FY2021's own account shows Interest expense as a small positive net recovery (+14), transcribed as reported.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=110,
    source_height=280,
    unit_suffix=" (EUR '000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - chronological roll-forward. Ladder
# confirmed: every year's own closing balance ties exactly to both the
# next year's own opening balance and that year's own Balance Sheet Total
# equity. Zero plug rows needed anywhere across all 5 years - the one
# genuine "easy to skip" movement caught by the mandated scan is FY2021's
# own €21k Other reserves write-off, bundled into that year's own "Loss
# for the financial year" retained-earnings/other-reserves split in the
# source table and reproduced here the same way.
# ---------------------------------------------------------------
equity_headers = ["Called-up share capital", "Retained earnings", "Other reserves", "Total"]
equity_rows = [
    ("TOTAL", "At 31 December 2020 (FY2021 opening)", (264412, -1480, 21, 262953)),
    ("DATA", "Loss for the financial year (includes a €21k write-off of the Other reserves balance, bundled into this row in the source table)", (None, -7308, -21, -7329)),
    ("DATA", "Other comprehensive loss for the year", (None, -12, None, -12)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (264412, -8800, 0, 255612)),
    ("DATA", "Profit for the financial year", (None, 559, None, 559)),
    ("DATA", "Other comprehensive loss for the year", (None, -41, None, -41)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (264412, -8282, 0, 256130)),
    ("DATA", "Profit for the financial year", (None, 630, None, 630)),
    ("DATA", "Other comprehensive loss for the year", (None, -228, None, -228)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (264412, -7880, 0, 256532)),
    ("DATA", "Profit for the financial year", (None, 2356, None, 2356)),
    ("DATA", "Other comprehensive loss for the year", (None, -224, None, -224)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (264412, -5748, 0, 258664)),
    ("DATA", "Profit for the financial year", (None, 181, None, 181)),
    ("DATA", "Other comprehensive income for the year", (None, 0, None, 0)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (264412, -5567, 0, 258845)),
]

bw.add_equity_changes_sheet(
    title="Melli Bank plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest. EUR '000. Equity reconciliation ladder confirmed: every year's own "
              "closing balance ties exactly to both the next year's own opening balance and that year's own Balance Sheet Total "
              "equity - zero plug rows needed anywhere across all 5 years.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

# Source cash-flow figures are EUR '000. FY2021 is blank because the 2021
# accounts expressly claim the FRS 102 qualifying-entity exemption (re-confirmed
# this batch - see CASH_FLOW_SOURCES). FY2025 added this batch from the
# Annual Report and Accounts 2025's own Statement of Cash Flows (p.26); its
# FY2024 comparative column there (13,753 / -664 / 13,089 / 39,289 / 52,378)
# matches this script's existing FY2024 figures exactly, cross-confirming both.
OPERATING = {"FY2025": -21600, "FY2024": 13753, "FY2023": -27408, "FY2022": -52056}
INVESTING = {"FY2025": -274, "FY2024": -664, "FY2023": -258, "FY2022": -47}
NET_CHANGE = {"FY2025": -21874, "FY2024": 13089, "FY2023": -27666, "FY2022": -52103}
OPENING = {"FY2025": 52378, "FY2024": 39289, "FY2023": 66955, "FY2022": 119058}
CLOSING = {"FY2025": 30504, "FY2024": 52378, "FY2023": 39289, "FY2022": 66955}

cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash from operating activities", OPERATING),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash from investing activities", INVESTING),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", NET_CHANGE),
    ("DATA", "Cash and cash equivalents at the beginning of the period", OPENING),
    ("TOTAL", "Cash and cash equivalents at the end of the period", CLOSING),
]

bw.add_cash_flow_sheet(
    title="Melli Bank plc — Statement of Cash Flows",
    subtitle="Entity-level basis, EUR '000; FY2021 has no Statement of Cash Flows under the FRS 102 exemption",
    rows=cash_rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=270,
    unit_suffix=" (EUR '000)",
)

# ---------------------------------------------------------------
# Asset Quality - FRS 102 entity, no IFRS 9 stage split disclosed; the
# Bank instead assesses impairment loan-by-loan against a small named
# book of Iranian-exposure legacy loans (Note 9's own past-due analysis /
# Note 11's own impairment-provision roll-forward). Coverage and past-due
# ratios computed here as the closest available proxy for NPL/coverage
# ratios given the disclosed granularity.
# ---------------------------------------------------------------
aq_rows = [
    ("SECTION", "Loans and advances to customers (Note 9)", {}),
    ("DATA", "Gross loans and advances to customers", {"FY2025": 23372, "FY2024": 25446, "FY2023": 27718, "FY2022": 27267, "FY2021": 22414}),
    ("DATA", "Impairment provisions (loans and advances to customers only - see Note 11)", {"FY2025": -20055, "FY2024": -21737, "FY2023": -19443, "FY2022": -19007, "FY2021": -13515}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 3317, "FY2024": 3709, "FY2023": 8275, "FY2022": 8260, "FY2021": 8899}),
    ("DATA", "of which: past due (any ageing bucket)", {"FY2025": 22164, "FY2024": 23410, "FY2023": 24395, "FY2022": 23373, "FY2021": 17683}),
    ("DATA", "Impairment provision coverage (impairment provisions / gross loans)", {"FY2025": "85.83%", "FY2024": "85.42%", "FY2023": "70.14%", "FY2022": "69.70%", "FY2021": "60.30%"}),
    ("DATA", "Past due ratio (past due / gross loans) - the closest available proxy for an NPL ratio at this entity's disclosed granularity (no IFRS 9 stage split; individually-assessed legacy loan book only)", {"FY2025": "94.83%", "FY2024": "91.99%", "FY2023": "88.01%", "FY2022": "85.73%", "FY2021": "78.90%"}),
    ("SECTION", "Total impairment loss provision, all classes (Note 11 - includes debt securities as well as loans)", {}),
    ("DATA", "Impairment loss provision at year end", {"FY2025": 20076, "FY2024": 22495, "FY2023": 20126, "FY2022": 19713, "FY2021": None}),
]

bw.add_asset_quality_sheet(
    title="Melli Bank plc — Asset Quality",
    subtitle="Entity-level basis, EUR '000. FRS 102 entity - no IFRS 9 stage split disclosed; impairment is assessed loan-by-loan "
              "against a small named book of legacy Iranian-exposure loans (Note 9), most of which are individually past due but "
              "either guaranteed/secured (not impaired) or 100% provided (fully impaired). Coverage and past-due ratios shown here "
              "as the closest available proxy for the usual NPL/coverage ratios given this entity's disclosed granularity.",
    rows=aq_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=100,
    source_height=260,
    unit_suffix=" (EUR '000)",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        p3_sources(),
        note=note,
        first_col_width=58,
        source_height=250,
    )


ELIGIBLE_CAPITAL = {
    "FY2025": 259000,
    "FY2024": 258360,
    "FY2023": 256049,
    "FY2022": 255912,
    "FY2021": 255099,
}
RWA = {"FY2025": 458000, "FY2024": 466000, "FY2023": 498000, "FY2022": 423000, "FY2021": 399000}
CAPITAL_RATIO = {"FY2025": "56%", "FY2024": "55%", "FY2023": "51%", "FY2022": "60%", "FY2021": "64%"}
LCR = {"FY2025": "679%", "FY2024": "697%", "FY2023": "529%", "FY2022": "617%"}

CAPITAL_NOTE = (
    "Eligible regulatory capital is 100% CET1 in the disclosed KPI/capital-management tables; "
    "the same disclosed amount is therefore shown for CET1, Tier 1 and Total Capital. Values are EUR '000. "
    "FY2025's own KPI table (Annual Report and Accounts 2025, p.10, 'Capital and Liquidity Position') is presented "
    "in whole EUR millions only (a changed presentation from prior years' more precise KPI table, coinciding with "
    "the September 2025 sanctions re-imposition) - the FY2025 figure (259) is therefore rounded to the nearest EUR "
    "million before conversion to EUR '000, one significant figure less precise than FY2021-FY2024's figures."
)
RATIO_NOTE = "The Bank discloses a single Total Capital Ratio and states all capital is CET1; the ratio is shown as the CET1, Tier 1 and Total Capital ratio."
RWA_NOTE = (
    "Total Risk Exposure Amount is the directly disclosed regulatory KPI, shown in EUR '000 (source table reports EUR millions "
    "for every year FY2021-FY2025, so no year loses precision relative to another here - unlike the Eligible Capital figure, "
    "see CET1 Capital sheet note)."
)
GAP_NOTE = (
    "Not publicly disclosed for this entity/year in the reviewed official source set. The Bank's reports state that "
    "Pillar 3 disclosure is available on request; no public current KM1 document was located."
)

metric("CET1 Capital", "EUR '000", [("Common Equity Tier 1 / eligible regulatory capital", ELIGIBLE_CAPITAL)], note=CAPITAL_NOTE)
metric("CET1 Ratio", "%", [("CET1 capital ratio", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Tier 1 Capital", "EUR '000", [("Tier 1 / eligible regulatory capital", ELIGIBLE_CAPITAL)], note=CAPITAL_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 capital ratio", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Total Capital", "EUR '000", [("Total regulatory capital / eligible capital", ELIGIBLE_CAPITAL)], note=CAPITAL_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Total RWAs", "EUR '000", [("Total risk exposure amount", RWA)], note=RWA_NOTE)

bw.add_rwa_breakdown_sheet(
    title="Melli Bank plc — RWA Breakdown",
    subtitle="Not publicly disclosed at category level for any year. EUR '000.",
    rows=[("DATA", "RWA breakdown by risk category", {})],
    sources_text=p3_sources() + (
        "\n\nRWA BREAKDOWN: no category-level (credit risk / market risk / operational risk / CVA) breakdown was "
        "found in any of the 5 years' Annual Reports - each year's own 'Capital management' note (and, for FY2025, "
        "the 'Capital and Liquidity Position' KPI table on p.10) discloses only the aggregate Total Risk Exposure "
        "Amount shown on the Total RWAs sheet, consistent with the reports' own statement that full Pillar 3 "
        "disclosure is available on request rather than published. Confirmed a genuine non-disclosure, not an "
        "access gap - all 5 Annual Reports were fully read this session, including the current FY2025 report."
    ),
    first_col_width=54,
    source_height=280,
    unit_suffix=" (EUR '000)",
)

metric("Leverage Ratio", "%", [("Leverage ratio", {})], note=GAP_NOTE)
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)], note="Directly disclosed in the KPI table for FY2022-FY2025; no FY2021 value was located.")
bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={"NSFR": GAP_NOTE, "MREL Ratio": GAP_NOTE},
)

def _row_values(rows, label):
    for kind, lbl, values in rows:
        if lbl == label:
            return values
    raise KeyError(label)


bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", _row_values(bs_rows, "Total assets")),
        ("Loans and advances to customers", _row_values(bs_rows, "Loans and advances to customers")),
        ("Customer accounts", _row_values(bs_rows, "Customer accounts")),
        ("Total equity", _row_values(bs_rows, "Total equity")),
    ],
    balance_sheet_unit="EUR '000",
    income_statement_totals=[
        (
            "Total revenue / Total net income",
            _row_values(
                pl_rows,
                "Total revenue / Total net income (FY2025's own report relabels this subtotal 'Total net income' - same position in the account, not a different line)",
            ),
        ),
        ("Administrative expenses", _row_values(pl_rows, "Administrative expenses")),
        ("Profit/(loss) for the financial year", _row_values(pl_rows, "Profit/(loss) for the financial year")),
    ],
    income_statement_unit="EUR '000",
    equity_changes_totals=[
        ("Opening equity", {"FY2021": 262953, "FY2022": 255612, "FY2023": 256130, "FY2024": 256532, "FY2025": 258664}),
        ("Total comprehensive income/(loss) for the year", {"FY2021": -7320, "FY2022": 518, "FY2023": 402, "FY2024": 2132, "FY2025": 181}),
        ("Other equity movements, net", {"FY2021": -21, "FY2022": 0, "FY2023": 0, "FY2024": 0, "FY2025": 0}),
        ("Closing equity", {"FY2021": 255612, "FY2022": 256130, "FY2023": 256532, "FY2024": 258664, "FY2025": 258845}),
    ],
    equity_changes_unit="EUR '000",
    cash_flow_totals=[
        ("Net cash from operating activities", OPERATING),
        ("Net cash from investing activities", INVESTING),
        ("Cash and cash equivalents at end of year", CLOSING),
    ],
    cash_flow_unit="EUR '000",
    ratios=[("CET1 Ratio", CAPITAL_RATIO), ("LCR", LCR)],
    note="FY2021 has no Statement of Cash Flows at all in the source Annual Report - the Company applied the FRS 102 "
         "qualifying-entity exemption, confirmed by both its accounting policy note and its own Contents page. "
         "FY2025 cash flow figures were added this batch from the Annual Report and Accounts 2025's own Statement "
         "of Cash Flows (p.26).",
)

bw.save("/Users/armaan/code/katalysis/banks/MELLI BANK FINANCIALS.xlsx")
