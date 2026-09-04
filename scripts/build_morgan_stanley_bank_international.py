import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# Morgan Stanley Bank International Limited, company 03722571, FRN 195430.
# The legal entity and FRN are confirmed against Banks List 2608.xlsx,
# Companies House, and Morgan Stanley's UK office/FCA information.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR_URLS = {
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzUxNTMzMjAyMmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzQ2MjkyNzg4N2FkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzQyMDQ2MzQxOGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzM3ODM5NTg1NmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzMzODIzODA1MmFkaXF6a2N4/document?format=pdf&download=0",
}

ENTITY_NOTE = (
    "ENTITY NOTE: Morgan Stanley Bank International Limited (company 03722571, FRN 195430) is the legal entity "
    "listed in Banks List 2608.xlsx. Companies House confirms the active UK private limited company, incorporated "
    "23 February 1999, with registered office at 25 Cabot Square, London E14 4QA. The figures below are standalone "
    "Company figures from the entity's own annual reports, not Morgan Stanley International group figures."
)


def annual_sources():
    return (
        ENTITY_NOTE + "\n\n"
        "Sources — Morgan Stanley Bank International Limited Annual Reports and Financial Statements, "
        "Strategic Report capital/liquidity tables and financial statements:\n"
        f"FY2025: Annual Report and Financial Statements for year ended 31 December 2025, pp.5, 8-10, 47 — {AR_URLS['FY2025']}\n"
        f"FY2024: Annual Report and Financial Statements for year ended 31 December 2024, pp.5, 8-10 — {AR_URLS['FY2024']}\n"
        f"FY2023: Annual Report and Financial Statements for year ended 31 December 2023, pp.5, 8-10 — {AR_URLS['FY2023']}\n"
        f"FY2022: Annual Report and Financial Statements for year ended 31 December 2022, pp.5, 8-10 — {AR_URLS['FY2022']}\n"
        f"FY2021: Annual Report and Financial Statements for year ended 31 December 2021, pp.6, 9-10 — {AR_URLS['FY2021']}\n"
        "The annual reports state that the Company takes the FRS 101 reduced-disclosure exemption from presenting a "
        "cash-flow statement. Blank or non-disclosed entries are not estimates or zeros."
    )


bw = BankWorkbook("Morgan Stanley Bank International Limited", YEARS, header_color="1F4E79")

STATEMENTS_SOURCES = (
    ENTITY_NOTE + "\n\n"
    "Sources — Morgan Stanley Bank International Limited Annual Reports and Financial Statements "
    "(Income Statement, Statement of Comprehensive Income, Statement of Financial Position, Statement of Changes "
    "in Equity, and Note 28 credit risk disclosures):\n"
    f"FY2025: Annual Report and Financial Statements for year ended 31 December 2025, pp.43-46, 76-77 — {AR_URLS['FY2025']}\n"
    f"FY2024: Annual Report and Financial Statements for year ended 31 December 2024, pp.42-45, 74-75 — {AR_URLS['FY2024']}\n"
    f"FY2023: Annual Report and Financial Statements for year ended 31 December 2023 (via FY2024 report's own "
    f"FY2023 comparative columns, pp.42-45, 74-75) — {AR_URLS['FY2024']}\n"
    f"FY2022: Annual Report and Financial Statements for year ended 31 December 2022, pp.39-43, 71-72 — {AR_URLS['FY2022']}\n"
    f"FY2021: Annual Report and Financial Statements for year ended 31 December 2021 (via FY2022 report's own "
    f"FY2021 comparative columns, pp.39-43, 71-72) — {AR_URLS['FY2022']}\n"
    "The Company takes the FRS 101 reduced-disclosure exemption from presenting a cash-flow statement. Blank or "
    "non-disclosed entries are not estimates or zeros."
)

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. All 5 years tie exactly to the equity statement's own
# opening/closing balances - zero plug rows needed anywhere.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 24687, "FY2024": 17404, "FY2023": 6870, "FY2022": 47133, "FY2021": 20144}),
    ("DATA", "Secured financing", {"FY2025": 836854, "FY2024": 1163336, "FY2023": 1150162, "FY2022": 1330363, "FY2021": 1139856}),
    ("DATA", "Loans and advances to banks", {"FY2025": 140542, "FY2024": 212774, "FY2023": 187090, "FY2022": 175841, "FY2021": 129608}),
    ("DATA", "Loans and advances to customers", {"FY2025": 422190, "FY2024": 775727, "FY2023": 760186, "FY2022": 1227715, "FY2021": 380124}),
    ("DATA", "Trading financial assets", {"FY2025": 3022186, "FY2024": 3746151, "FY2023": 3613350, "FY2022": 4868282, "FY2021": 3358044}),
    ("DATA", "Investment securities", {"FY2025": 23, "FY2024": 472, "FY2023": 463, "FY2022": 23, "FY2021": 679}),
    ("DATA", "Investment in subsidiary undertaking", {"FY2021": 105374}),
    ("DATA", "Tangible fixed assets", {"FY2025": 681, "FY2024": 926, "FY2023": 1093, "FY2022": 1382, "FY2021": 567}),
    ("DATA", "Other receivables", {"FY2025": 26119, "FY2024": 23892, "FY2023": 34100, "FY2022": 30374, "FY2021": 22811}),
    ("DATA", "Current tax assets", {"FY2025": 1218, "FY2024": 282, "FY2023": 296, "FY2022": 2451, "FY2021": 287}),
    ("DATA", "Deferred tax assets", {"FY2025": 75, "FY2024": 1961, "FY2023": 7415, "FY2022": 7698, "FY2021": 8696}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 126, "FY2024": 157, "FY2023": 156, "FY2022": 172, "FY2021": 127}),
    ("TOTAL", "Total assets", {"FY2025": 4474701, "FY2024": 5943082, "FY2023": 5761181, "FY2022": 7691434, "FY2021": 5166317}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 279651, "FY2024": 462429, "FY2023": 251784, "FY2022": 440764, "FY2021": 153851}),
    ("DATA", "Customer accounts", {"FY2025": 632759, "FY2024": 783693, "FY2023": 1246212, "FY2022": 1814583, "FY2021": 1502764}),
    ("DATA", "Secured borrowing", {"FY2025": 103105, "FY2024": 123656, "FY2023": 86502, "FY2022": 128224, "FY2021": 85181}),
    ("DATA", "Trading financial liabilities", {"FY2025": 2409008, "FY2024": 3311515, "FY2023": 2957832, "FY2022": 4081489, "FY2021": 2270962}),
    ("DATA", "Other payables", {"FY2025": 18473, "FY2024": 20906, "FY2023": 27230, "FY2022": 45937, "FY2021": 41460}),
    ("DATA", "Accruals and deferred income", {"FY2025": 4080, "FY2024": 9391, "FY2023": 2059, "FY2022": 1497, "FY2021": 2290}),
    ("DATA", "Current tax liabilities", {"FY2025": 19853, "FY2024": 11677, "FY2023": 13754, "FY2022": 10758, "FY2021": 37356}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 1079, "FY2024": 0}),
    ("DATA", "Retirement benefit liability", {"FY2025": 394, "FY2024": 424, "FY2023": 126, "FY2022": 111, "FY2021": 287}),
    ("DATA", "Provisions for liabilities and charges", {"FY2025": 178, "FY2024": 179, "FY2023": 193, "FY2022": 203, "FY2021": 183}),
    ("DATA", "Subordinated debt", {"FY2025": 258220, "FY2024": 408727, "FY2023": 409506, "FY2022": 401644, "FY2021": 250000}),
    ("TOTAL", "Total liabilities", {"FY2025": 3726800, "FY2024": 5132597, "FY2023": 4995198, "FY2022": 6925210, "FY2021": 4344334}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 340000, "FY2024": 340000, "FY2023": 340000, "FY2022": 340000, "FY2021": 340000}),
    ("DATA", "Capital contribution reserve", {"FY2025": 89654, "FY2024": 89654, "FY2023": 89654, "FY2022": 89654, "FY2021": 89654}),
    ("DATA", "Foreign currency revaluation reserve", {"FY2025": 35165, "FY2024": 35368, "FY2023": 36668, "FY2022": 37201, "FY2021": 37213}),
    ("DATA", "Profit and loss account", {"FY2025": 283082, "FY2024": 345463, "FY2023": 299661, "FY2022": 299369, "FY2021": 355116}),
    ("TOTAL", "Equity shareholders' funds", {"FY2025": 747901, "FY2024": 810485, "FY2023": 765983, "FY2022": 766224, "FY2021": 821983}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 4474701, "FY2024": 5943082, "FY2023": 5761181, "FY2022": 7691434, "FY2021": 5166317}),
]

bw.add_balance_sheet_sheet(
    title="Morgan Stanley Bank International Limited — Balance Sheet",
    subtitle="Standalone Company basis (FRS 101). £'000. FY2021 uniquely shows an 'Investment in subsidiary "
              "undertaking' line (£105,374k) - disposed of during FY2022, generating that year's £93,978k 'Gain "
              "on disposal of subsidiary' on the Profit & Loss sheet and dropping to £nil from FY2022 onward. "
              "'Deferred tax liabilities' only appears as its own line from FY2024 (shown as '–'/nil that year, "
              "£1,079k in FY2025); FY2021-FY2023 disclose no such line at all (shown blank, not zero).",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2025": 111211, "FY2024": 150183, "FY2023": 176532, "FY2022": 67078, "FY2021": 17558}),
    ("DATA", "Interest payable and similar charges", {"FY2025": -67596, "FY2024": -93121, "FY2023": -124244, "FY2022": -46738, "FY2021": -2930}),
    ("TOTAL", "Net interest income", {"FY2025": 43615, "FY2024": 57062, "FY2023": 52288, "FY2022": 20340, "FY2021": 14628}),
    ("DATA", "Fee and commission income", {"FY2025": 9777, "FY2024": 10790, "FY2023": 9348, "FY2022": 2326, "FY2021": 21255}),
    ("DATA", "Fee and commission expense", {"FY2025": -5676, "FY2024": -6506, "FY2023": -16211, "FY2022": -14348, "FY2021": -12916}),
    ("DATA", "Net gain from financial instruments at fair value through profit or loss", {"FY2025": 23982, "FY2024": 30718, "FY2023": 21129, "FY2022": 36542, "FY2021": 42393}),
    ("DATA", "Net reversal of impairment loss on financial instruments", {"FY2022": 0, "FY2021": 416}),
    ("DATA", "Gain on disposal of subsidiary", {"FY2022": 93978}),
    ("DATA", "Administrative expenses", {"FY2025": -21070, "FY2024": -27722, "FY2023": -34895, "FY2022": -32647, "FY2021": -48725}),
    ("DATA", "Depreciation of tangible fixed assets", {"FY2025": -239, "FY2024": -229, "FY2023": -267, "FY2022": -270, "FY2021": -215}),
    ("TOTAL", "Profit before tax", {"FY2025": 50389, "FY2024": 64113, "FY2023": 31392, "FY2022": 105921, "FY2021": 16836}),
    ("DATA", "Income tax expense", {"FY2025": -12810, "FY2024": -18332, "FY2023": -31078, "FY2022": -11768, "FY2021": -6959}),
    ("TOTAL", "Profit for the year", {"FY2025": 37579, "FY2024": 45781, "FY2023": 314, "FY2022": 94153, "FY2021": 9877}),
    ("SECTION", "Other comprehensive income/(loss), net of tax", {}),
    ("DATA", "Remeasurement of net defined benefit liability", {"FY2025": 40, "FY2024": 21, "FY2023": -22, "FY2022": 100, "FY2021": 78}),
    ("DATA", "Foreign currency translation differences arising on foreign operations", {"FY2025": -8951, "FY2024": -19706, "FY2023": -15179, "FY2022": 10400, "FY2021": -14755}),
    ("DATA", "Gain/(loss) arising on hedging instruments designated in net investment hedges", {"FY2025": 8748, "FY2024": 18406, "FY2023": 14646, "FY2022": -10412, "FY2021": 14422}),
    ("TOTAL", "Other comprehensive income/(loss) after income tax", {"FY2025": -163, "FY2024": -1279, "FY2023": -555, "FY2022": 88, "FY2021": -255}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 37416, "FY2024": 44502, "FY2023": -241, "FY2022": 94241, "FY2021": 9622}),
]

bw.add_income_statement_sheet(
    title="Morgan Stanley Bank International Limited — Profit & Loss",
    subtitle="Standalone Company basis (FRS 101). £'000. FY2022's 'Gain on disposal of subsidiary' (£93,978k) is "
              "the disposal of the subsidiary undertaking held on the FY2021 Balance Sheet. FY2021/FY2022 disclose "
              "a 'Net reversal of impairment loss on financial instruments' line not shown FY2023-FY2025 (genuinely "
              "£nil/not disclosed those years, not omitted).",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=78,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder confirmed
# exactly across all 5 years (opening ties to prior closing, closing ties to
# that year's own Balance Sheet Total equity) via the FY2022 Annual Report's
# own FY2021 comparative for the FY2021 opening balance (at 1 January 2021).
# Zero plug rows needed anywhere.
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Capital contribution reserve",
                   "Foreign currency revaluation reserve", "Profit and loss account", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2021 (FY2021 opening)", (340000, 89654, 37546, 345161, 812361)),
    ("DATA", "Profit for the year", (None, None, None, 9877, 9877)),
    ("DATA", "Remeasurement gain on net defined benefit liability", (None, None, None, 78, 78)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, -14755, None, -14755)),
    ("DATA", "Gain arising on hedging instruments designated in net investment hedges", (None, None, 14422, None, 14422)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (340000, 89654, 37213, 355116, 821983)),
    ("DATA", "Profit for the year", (None, None, None, 94153, 94153)),
    ("DATA", "Remeasurement gain on net defined benefit liability", (None, None, None, 100, 100)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, 10400, None, 10400)),
    ("DATA", "(Loss) arising on hedging instruments designated in net investment hedges", (None, None, -10412, None, -10412)),
    ("DATA", "Dividend", (None, None, None, -150000, -150000)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (340000, 89654, 37201, 299369, 766224)),
    ("DATA", "Profit for the year", (None, None, None, 314, 314)),
    ("DATA", "Remeasurement loss on net defined benefit liability", (None, None, None, -22, -22)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, -15179, None, -15179)),
    ("DATA", "Gain arising on hedging instruments designated in net investment hedges", (None, None, 14646, None, 14646)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (340000, 89654, 36668, 299661, 765983)),
    ("DATA", "Profit for the year", (None, None, None, 45781, 45781)),
    ("DATA", "Remeasurement gain on net defined benefit liability", (None, None, None, 21, 21)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, -19706, None, -19706)),
    ("DATA", "Gain arising on hedging instruments designated in net investment hedges", (None, None, 18406, None, 18406)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (340000, 89654, 35368, 345463, 810485)),
    ("DATA", "Profit for the year", (None, None, None, 37579, 37579)),
    ("DATA", "Remeasurement gain on net defined benefit liability", (None, None, None, 40, 40)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, -8951, None, -8951)),
    ("DATA", "Gain arising on hedging instruments designated in net investment hedges", (None, None, 8748, None, 8748)),
    ("DATA", "Dividends", (None, None, None, -100000, -100000)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (340000, 89654, 35165, 283082, 747901)),
]

bw.add_equity_changes_sheet(
    title="Morgan Stanley Bank International Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, standalone Company basis (FRS 101). £'000. Equity "
              "reconciliation ladder confirmed: every year's own closing balance ties exactly to both the next "
              "year's own opening balance and that year's own Balance Sheet Total equity - zero plug rows needed "
              "anywhere across all 5 years. FY2021 opening balance sourced from the FY2022 Annual Report's own "
              "'at 1 January 2021' comparative column.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
)

# ---------------------------------------------------------------
# Asset Quality - "Exposure to credit risk by class" (Note 28.2.3/28.2.4),
# external-counterparty exposures only. Morgan Stanley Group undertaking
# exposures are separately disclosed each year but are fully offset by
# intercompany collateral/guarantee arrangements (net exposure £nil) and are
# excluded from the totals below as they carry no third-party credit risk.
# Genuine finding: the Company's own Note 28.2.4 confirms ALL exposures
# subject to ECL are Stage 1 in every year reviewed, with £nil Stage 3/
# default balances - a wholesale/broker-dealer credit profile, not a retail
# loan book, so no NPL coverage ratios are meaningful here.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Exposure to credit risk by class, subject to ECL (external counterparties only)", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 24687, "FY2024": 17404, "FY2023": 6870, "FY2022": 47133, "FY2021": 20144}),
    ("DATA", "Loans and advances to banks — external counterparties", {"FY2025": 133463, "FY2024": 205239, "FY2023": 181342, "FY2022": 169755, "FY2021": 124091}),
    ("DATA", "Loans and advances to customers — external counterparties", {"FY2025": 156, "FY2024": 40747, "FY2023": 226, "FY2022": 285, "FY2021": 0}),
    ("DATA", "Other receivables", {"FY2025": 16304, "FY2024": 20082, "FY2023": 34100, "FY2022": 30374, "FY2021": 22811}),
    ("TOTAL", "Total gross credit exposure subject to ECL (external)", {"FY2025": 174610, "FY2024": 283472, "FY2023": 222538, "FY2022": 247547, "FY2021": 167046}),
    ("DATA", "Of which: Stage 1", {"FY2025": "100%", "FY2024": "100%", "FY2023": "100%", "FY2022": "100%", "FY2021": "100%"}),
    ("DATA", "Of which: Stage 3 / default (NPL ratio)", {"FY2025": "0.0%", "FY2024": "0.0%", "FY2023": "0.0%", "FY2022": "0.0%", "FY2021": "0.0%"}),
]

# The Company explicitly takes the FRS 101 exemption from presenting a cash-flow
# statement. Retain the standard tab and document the structural limitation.
bw.add_cash_flow_sheet(
    "Morgan Stanley Bank International Limited — Statement of Cash Flows",
    "Standalone Company basis; cash-flow statement not presented under the FRS 101 reduced-disclosure exemption",
    [("DATA", "Cash-flow statement not separately disclosed under FRS 101", {})],
    annual_sources(),
    first_col_width=72,
    source_height=220,
    unit_suffix=" (£'000)",
)

bw.add_asset_quality_sheet(
    title="Morgan Stanley Bank International Limited — Asset Quality",
    subtitle="Exposure to credit risk by class, external counterparties only. £'000. Morgan Stanley Group "
              "undertaking exposures (Secured financing, and large portions of Loans and advances to banks/"
              "customers) are separately disclosed each year but are fully covered by intercompany collateral or "
              "the Morgan Stanley parent guarantee, leaving £nil net exposure — excluded here as not "
              "third-party credit risk. All exposures subject to ECL are internally rated Stage 1 in every year "
              "reviewed (£nil Stage 3/default, per the Company's own Note 28.2.4 disclosure) — a wholesale/"
              "broker-dealer credit profile, not a retail loan book.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nFY2025: Note 28.2.3 'Exposure to credit risk by class' p.76, Note 28.2.4 'Exposure to Credit Risk by "
        "Internal Rating Grades' p.77. FY2024/FY2023: Note 27.2.3, p.75. FY2022/FY2021: Note 28.2.4 'Exposure to "
        "Credit Risk' p.72."
    ),
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, annual_sources(), note=note, first_col_width=54, source_height=220)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {
    "FY2025": 676229, "FY2024": 709078, "FY2023": 685522, "FY2022": 702944, "FY2021": 717693,
})])
metric("CET1 Ratio", "% of RWA", [("CET1 capital ratio", {
    "FY2025": "42.6%", "FY2024": "46.7%", "FY2023": "31.7%", "FY2022": "34.0%", "FY2021": "34.4%",
})])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {
    "FY2025": 676229, "FY2024": 709078, "FY2023": 685522, "FY2022": 702944, "FY2021": 717693,
})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 capital ratio", {
    "FY2025": "42.6%", "FY2024": "46.7%", "FY2023": "31.7%", "FY2022": "34.0%", "FY2021": "34.4%",
})])
metric("Total Capital", "£'000", [("Total capital resources", {
    "FY2025": 934449, "FY2024": 908739, "FY2023": 935655, "FY2022": 1003410, "FY2021": 916488,
})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {
    "FY2025": "58.9%", "FY2024": "59.8%", "FY2023": "43.3%", "FY2022": "48.5%", "FY2021": "44.0%",
})])
metric("Total RWAs", "£'000", [("Total risk-weighted assets", {
    "FY2025": 1586014, "FY2024": 1519269, "FY2023": 2161713, "FY2022": 2068356, "FY2021": 2081783,
})])

# RWA Breakdown - placed right after Total RWAs per the locked sheet order.
# Sourced from each year's own Strategic Report "RWAs" table (not a separate
# Pillar 3 document - this entity discloses its RWA category split within the
# Annual Report itself). All 5 years tie exactly to the Total RWAs figure above.
rwa_breakdown_rows = [
    ("DATA", "Credit RWAs", {"FY2025": 438035, "FY2024": 427744, "FY2023": 513578, "FY2022": 619276, "FY2021": 736089}),
    ("DATA", "Market RWAs", {"FY2025": 1004032, "FY2024": 964352, "FY2023": 1537651, "FY2022": 1254480, "FY2021": 1098855}),
    ("DATA", "Operational risk RWAs", {"FY2025": 143947, "FY2024": 127173, "FY2023": 110484, "FY2022": 194600, "FY2021": 246839}),
    ("TOTAL", "Total RWAs", {"FY2025": 1586014, "FY2024": 1519269, "FY2023": 2161713, "FY2022": 2068356, "FY2021": 2081783}),
]
bw.add_rwa_breakdown_sheet(
    title="Morgan Stanley Bank International Limited — RWA Breakdown",
    subtitle="Company's own 'RWAs' table (Strategic Report), by risk category. £'000. Ties exactly to the Total "
              "RWAs sheet in every year.",
    rows=rwa_breakdown_rows,
    sources_text=annual_sources(),
    first_col_width=54,
    source_height=220,
    unit_suffix=" (£'000)",
)

metric("Leverage Ratio", "£'000 / %", [
    ("Leverage exposure", {"FY2025": 2233488, "FY2024": 2436257, "FY2023": 2874295, "FY2022": 3795132, "FY2021": 2384965}),
    ("Leverage ratio", {"FY2025": "30.3%", "FY2024": "29.1%", "FY2023": "23.9%", "FY2022": "18.5%", "FY2021": "30.1%"}),
])
metric("LCR", "£'000 / %", [
    ("Liquidity buffer — HQLA", {"FY2025": 1110032, "FY2024": 1825386, "FY2023": 1190200, "FY2022": 1230539, "FY2021": 1240953}),
    ("Liquidity coverage ratio", {"FY2025": "412%", "FY2024": "417%", "FY2023": "250%", "FY2022": "191%", "FY2021": "226%"}),
], note="The reports state that the HQLA amounts are reported to the regulator in USD and converted to GBP using an average annual exchange rate; the ratios are calculated using the preceding twelve months.")
metric("NSFR", "£'000 / %", [
    ("Available stable funding", {"FY2025": 1485790, "FY2024": 1597110, "FY2023": 2191000, "FY2022": 2344000, "FY2021": "Not disclosed"}),
    ("Required stable funding", {"FY2025": 574724, "FY2024": 716541, "FY2023": 1346000, "FY2022": 1417000, "FY2021": "Not disclosed"}),
    ("Net Stable Funding Ratio", {"FY2025": "263%", "FY2024": "223%", "FY2023": "163%", "FY2022": "165%", "FY2021": "Not disclosed"}),
], note="The Company states that NSFR became a PRA requirement from 1 January 2022; no FY2021 NSFR was disclosed.")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    annual_sources() + "\nNo standalone MREL ratio was numerically disclosed in the five annual reports reviewed; group-level resolution disclosures were not substituted.",
)

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 4474701, "FY2024": 5943082, "FY2023": 5761181, "FY2022": 7691434, "FY2021": 5166317}),
        ("Loans and advances to customers", {"FY2025": 422190, "FY2024": 775727, "FY2023": 760186, "FY2022": 1227715, "FY2021": 380124}),
        ("Customer accounts", {"FY2025": 632759, "FY2024": 783693, "FY2023": 1246212, "FY2022": 1814583, "FY2021": 1502764}),
        ("Total equity", {"FY2025": 747901, "FY2024": 810485, "FY2023": 765983, "FY2022": 766224, "FY2021": 821983}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 43615, "FY2024": 57062, "FY2023": 52288, "FY2022": 20340, "FY2021": 14628}),
        ("Administrative expenses", {"FY2025": -21070, "FY2024": -27722, "FY2023": -34895, "FY2022": -32647, "FY2021": -48725}),
        ("Profit for the year", {"FY2025": 37579, "FY2024": 45781, "FY2023": 314, "FY2022": 94153, "FY2021": 9877}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 810485, "FY2024": 765983, "FY2023": 766224, "FY2022": 821983, "FY2021": 812361}),
        ("Total comprehensive income for the year", {"FY2025": 37416, "FY2024": 44502, "FY2023": -241, "FY2022": 94241, "FY2021": 9622}),
        ("Other equity movements, net", {"FY2025": -100000, "FY2024": 0, "FY2023": 0, "FY2022": -150000, "FY2021": 0}),
        ("Closing equity", {"FY2025": 747901, "FY2024": 810485, "FY2023": 765983, "FY2022": 766224, "FY2021": 821983}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "42.6%", "FY2024": "46.7%", "FY2023": "31.7%", "FY2022": "34.0%", "FY2021": "34.4%"}),
        ("Total Capital Ratio", {"FY2025": "58.9%", "FY2024": "59.8%", "FY2023": "43.3%", "FY2022": "48.5%", "FY2021": "44.0%"}),
        ("Leverage Ratio", {"FY2025": "30.3%", "FY2024": "29.1%", "FY2023": "23.9%", "FY2022": "18.5%", "FY2021": "30.1%"}),
        ("LCR", {"FY2025": "412%", "FY2024": "417%", "FY2023": "250%", "FY2022": "191%", "FY2021": "226%"}),
        ("NSFR", {"FY2025": "263%", "FY2024": "223%", "FY2023": "163%", "FY2022": "165%", "FY2021": "Not disclosed"}),
    ],
    note="The Company takes the FRS 101 exemption from presenting a cash-flow statement. Interim Morgan Stanley International Pillar 3 reports are group-level and do not provide defensible standalone MSBIL interim data.",
)

bw.save("/Users/armaan/code/katalysis/banks/MORGAN STANLEY BANK INTERNATIONAL FINANCIALS.xlsx")
