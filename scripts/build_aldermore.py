import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Aldermore Bank PLC (Companies House 00947662, FRN 204503) reports to a
# 30 June fiscal year end - "FY2025" below means the year ended 30 June 2025.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {
    "FY2025": "FY2025 (y/e 30 Jun 25)",
    "FY2024": "FY2024 (y/e 30 Jun 24)",
    "FY2023": "FY2023 (y/e 30 Jun 23)",
    "FY2022": "FY2022 (y/e 30 Jun 22)",
    "FY2021": "FY2021 (y/e 30 Jun 21)",
}

CH_2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzQ4NzM5MDg2MWFkaXF6a2N4/document?format=pdf&download=0"
CH_2024_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzQ0MDgwMDc3OWFkaXF6a2N4/document?format=pdf&download=0"
CH_2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzM5ODA0OTgzOWFkaXF6a2N4/document?format=pdf&download=0"
CH_2022_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzM1NTc2ODMxMmFkaXF6a2N4/document?format=pdf&download=0"
CH_2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzMxODkyMzc2MWFkaXF6a2N4/document?format=pdf&download=0"

P3_2025_URL = "https://www.aldermore.co.uk/media/sgufisw5/aldermore-group-plc-2025-pillar-3-disclosures.pdf"
P3_2024_URL = "https://www.aldermore.co.uk/media/jkkdbgnu/aldermore-group-plc-2024-pillar-3-disclosures.pdf"
P3_2022_URL = "https://www.aldermore.co.uk/media/hnhpw03l/pillar-3-2022_0.pdf"
INTERIM_P3_2025_URL = "https://www.aldermore.co.uk/media/xx1fg0me/half-year-pillar-3-disclosures-31-dec-2025.pdf"

CASH_FLOW_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo, not the Aldermore Group PLC holding company), "
    "Statement of cash flows from each year's full statutory accounts filed at Companies House "
    "(company no. 00947662), £m:\n"
    f"FY2025 & FY2024 (restated): Full accounts made up to 30 June 2025, filed 04 Nov 2025, p.55 — {CH_2025_URL}\n"
    f"FY2023: Full accounts made up to 30 June 2023, filed 27 Oct 2023, p.53 — {CH_2023_URL}\n"
    f"FY2022: Full accounts made up to 30 June 2022, filed 19 Oct 2022, p.60 — {CH_2022_URL}\n"
    f"FY2021: Full accounts made up to 30 June 2021, filed 04 Nov 2021, p.59 — {CH_2021_URL}\n"
    "(FY2024 accounts as originally filed are superseded by the FY2025 accounts' restated FY2024 comparative used here — "
    f"{CH_2024_URL})\n"
    "Note: the Bank reclassified its FY2024 comparative cash flow statement (see FY2025 accounts, p.55) to move interest "
    "received/paid on the intercompany loan, interest paid on subordinated notes, and interest received on debt "
    "securities from investing/financing activities into operating activities, and to reclassify proceeds from disposal "
    "of a non-current asset held for sale into operating activities; amounts relating to intercompany loans are also now "
    "presented gross rather than net. FY2023/FY2022/FY2021 below are presented as originally filed under the older "
    "(pre-reclassification) basis. Blank cells indicate a line item was not part of that year's classification of cash "
    "flows; section totals (net cash from operating/investing/financing activities, net change, opening/closing cash) "
    "are directly as reported and comparable across all 5 years. Minor (≤£0.1m) differences between individual line "
    "items and their printed subtotals in the FY2023/FY2022 source documents are presented as disclosed, not adjusted."
)

def p3_sources(page_25="4", page_24="4", page_22="4"):
    return (
        "Sources — Aldermore Bank PLC solo figures from the 'Key metrics' table (Bank columns), Aldermore Group PLC "
        "Pillar 3 Disclosures:\n"
        f"FY2025 & FY2024: Pillar 3 Disclosures for the year ended 30 June 2025, p.{page_25} (Key metrics) — {P3_2025_URL}\n"
        f"FY2023: Pillar 3 Disclosures for the year ended 30 June 2024, p.{page_24} (Key metrics, FY2023 comparative) — {P3_2024_URL}\n"
        f"FY2022 & FY2021: Pillar 3 Disclosures for the year ended 30 June 2022, p.{page_22} (Key metrics) — {P3_2022_URL}"
    )

bw = BankWorkbook(bank_name="Aldermore Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="AD1457")

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Statement of Financial Position)
# ---------------------------------------------------------------
BALANCE_SHEET_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo, not the Aldermore Group PLC holding company), Statement of "
    "financial position from each year's full statutory accounts filed at Companies House (company no. 00947662), "
    "£m:\n"
    f"FY2025 & FY2024: Full accounts made up to 30 June 2025, filed 04 Nov 2025, p.54 — {CH_2025_URL}\n"
    f"FY2023 & FY2022: Full accounts made up to 30 June 2023, filed 27 Oct 2023, p.52 — {CH_2023_URL}\n"
    f"FY2021: Full accounts made up to 30 June 2021, filed 04 Nov 2021, p.58 — {CH_2021_URL}\n"
    "Note: minor (£0.1m) rounding differences appear between the Total equity figure on the face of the "
    "Statement of financial position and the Statement of Changes in Equity's closing balance in some years "
    "(e.g. FY2021: £987.1m here vs £987.2m per the FY2021 accounts' own Statement of Changes in Equity) — "
    "both are presented exactly as disclosed in their respective source tables, not reconciled."
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 1182.3, "FY2024": 2172.2, "FY2023": 1923.4, "FY2022": 838.3, "FY2021": 688.5}),
    ("DATA", "Loans and advances to banks", {"FY2025": 183.6, "FY2024": 170.1, "FY2023": 206.5, "FY2022": 132.8, "FY2021": 106.4}),
    ("DATA", "Amounts owed by / receivable from other Group undertakings", {"FY2025": 3779.6, "FY2024": 3720.5, "FY2023": 3525.1, "FY2022": 3072.5, "FY2021": 2303.8}),
    ("DATA", "Debt securities", {"FY2025": 2704.2, "FY2024": 2436.5, "FY2023": 2048.9, "FY2022": 2339.2, "FY2021": 1999.5}),
    ("DATA", "Derivatives held for risk management", {"FY2025": 170.1, "FY2024": 344.2, "FY2023": 666.3, "FY2022": 259.9, "FY2021": 18.9}),
    ("DATA", "Loans and advances to customers", {"FY2025": 12523.4, "FY2024": 11416.3, "FY2023": 10998.9, "FY2022": 10777.3, "FY2021": 10393.6}),
    ("DATA", "Fair value adjustment for portfolio hedged risk", {"FY2025": 18.8, "FY2024": -129.0, "FY2023": -400.1, "FY2022": -180.2, "FY2021": 15.2}),
    ("DATA", "Non-current assets held for sale", {"FY2023": 32.8}),
    ("DATA", "Other assets", {"FY2025": 2.8, "FY2024": 9.2, "FY2023": 6.0, "FY2022": 1.6, "FY2021": 2.0}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 23.6, "FY2024": 22.8, "FY2023": 17.8, "FY2022": 14.5, "FY2021": 13.3}),
    ("DATA", "Taxation asset", {"FY2025": 2.9, "FY2024": 2.2, "FY2023": 0, "FY2022": 7.0, "FY2021": 0.7}),
    ("DATA", "Deferred taxation", {"FY2025": 6.3, "FY2024": 5.7, "FY2023": 6.1, "FY2022": 2.6, "FY2021": 5.7}),
    ("DATA", "Property, plant and equipment", {"FY2025": 16.3, "FY2024": 20.5, "FY2023": 15.7, "FY2022": 20.8, "FY2021": 25.8}),
    ("DATA", "Intangible assets", {"FY2025": 4.3, "FY2024": 4.3, "FY2023": 4.3, "FY2022": 4.5, "FY2021": 9.6}),
    ("TOTAL", "Total assets", {"FY2025": 20618.2, "FY2024": 20195.5, "FY2023": 19051.7, "FY2022": 17290.8, "FY2021": 15583.0}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Amounts due to banks", {"FY2025": 795.8, "FY2024": 1365.3, "FY2023": 1681.9, "FY2022": 1341.8, "FY2021": 1326.6}),
    ("DATA", "Customers' accounts", {"FY2025": 17047.6, "FY2024": 16306.7, "FY2023": 15033.3, "FY2022": 14105.4, "FY2021": 12427.3}),
    ("DATA", "Derivatives held for risk management", {"FY2025": 94.1, "FY2024": 37.8, "FY2023": 62.5, "FY2022": 24.5, "FY2021": 40.0}),
    ("DATA", "Fair value adjustment for portfolio hedged risk", {"FY2025": 16.4, "FY2024": 6.5, "FY2023": -21.0, "FY2022": -12.7, "FY2021": 0}),
    ("DATA", "Amounts owed / payable to other Group undertakings", {"FY2025": 952.5, "FY2024": 909.2, "FY2023": 862.0, "FY2022": 531.5, "FY2021": 537.2}),
    ("DATA", "Other liabilities, accruals and deferred income", {"FY2025": 93.3, "FY2024": 96.7, "FY2023": 105.2, "FY2022": 97.9, "FY2021": 92.4}),
    ("DATA", "Taxation liability", {"FY2023": 6.0}),
    ("DATA", "Provisions", {"FY2025": 3.0, "FY2024": 0.6, "FY2023": 2.5, "FY2022": 3.8, "FY2021": 2.7}),
    ("DATA", "Debt securities in issue", {"FY2023": -0.2, "FY2022": -0.5}),
    ("DATA", "Subordinated notes", {"FY2025": 100.9, "FY2024": 100.9, "FY2023": 100.5, "FY2022": 100.5, "FY2021": 161.4}),
    ("TOTAL", "Total liabilities", {"FY2025": 17050.8, "FY2024": 18823.7, "FY2023": 17832.7, "FY2022": 16192.2, "FY2021": 14595.9}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 3.3, "FY2024": 3.3, "FY2023": 3.3, "FY2022": 3.3, "FY2021": 3.3}),
    ("DATA", "Share premium account", {"FY2025": 307.5, "FY2024": 307.5, "FY2023": 307.5, "FY2022": 307.5, "FY2021": 307.5}),
    ("DATA", "Additional Tier 1 capital", {"FY2025": 50.0, "FY2024": 61.0, "FY2023": 61.0, "FY2022": 61.0, "FY2021": 61.0}),
    ("DATA", "FVOCI / fair value through other comprehensive income reserve", {"FY2025": -5.0, "FY2024": -0.7, "FY2023": 3.3, "FY2022": 6.9, "FY2021": 8.3}),
    ("DATA", "Retained earnings", {"FY2025": 1158.8, "FY2024": 1000.7, "FY2023": 843.9, "FY2022": 719.9, "FY2021": 607.0}),
    ("TOTAL", "Total equity", {"FY2025": 1514.6, "FY2024": 1371.8, "FY2023": 1219.0, "FY2022": 1098.6, "FY2021": 987.1}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 20618.2, "FY2024": 20195.5, "FY2023": 19051.7, "FY2022": 17290.8, "FY2021": 15583.0}),
]

bw.add_balance_sheet_sheet(
    title="Aldermore Bank PLC — Statement of Financial Position",
    subtitle="Company (Bank solo) basis, £m, as at 30 June",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=72,
    source_height=150,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Income Statement + Statement of Comprehensive Income)
# ---------------------------------------------------------------
INCOME_STATEMENT_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo, not the Aldermore Group PLC holding company), Income "
    "statement and Statement of comprehensive income from each year's full statutory accounts filed at "
    "Companies House (company no. 00947662), £m:\n"
    f"FY2025 & FY2024: Full accounts made up to 30 June 2025, filed 04 Nov 2025, p.53 — {CH_2025_URL}\n"
    f"FY2023 & FY2022: Full accounts made up to 30 June 2023, filed 27 Oct 2023, p.50-51 — {CH_2023_URL}\n"
    f"FY2021: Full accounts made up to 30 June 2021, filed 04 Nov 2021, p.56-57 — {CH_2021_URL}\n"
    "Note: FY2021's admin expenses line ('Other administrative expenses') is presented separately from "
    "'Depreciation and amortisation' and 'Provisions' that year; from FY2022 onward the Bank presents a "
    "single combined 'Administrative expenses' line plus separate 'Provisions' and folds depreciation into "
    "impairment/operating profit — both are transcribed as disclosed, not restated onto a common basis."
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 1240.5, "FY2024": 1234.8, "FY2023": 878.7, "FY2022": 533.4, "FY2021": 473.6}),
    ("DATA", "Interest expense", {"FY2025": -828.0, "FY2024": -808.1, "FY2023": -433.6, "FY2022": -152.5, "FY2021": -157.3}),
    ("TOTAL", "Net interest income", {"FY2025": 412.5, "FY2024": 426.7, "FY2023": 445.1, "FY2022": 380.9, "FY2021": 316.3}),
    ("DATA", "Fee and commission income / fee and other income", {"FY2025": 7.5, "FY2024": 7.1, "FY2023": 11.7, "FY2022": 6.0, "FY2021": 6.5}),
    ("DATA", "Fee and commission expense", {"FY2025": -9.5, "FY2024": -8.2, "FY2023": -5.4, "FY2022": -5.6, "FY2021": -5.4}),
    ("DATA", "Net gains/(losses) from derivatives and other financial instruments at fair value through profit or loss", {"FY2025": 12.6, "FY2024": -3.0, "FY2023": 12.6, "FY2022": -5.3, "FY2021": -3.1}),
    ("DATA", "Net gains on disposal of financial assets at fair value through other comprehensive income", {"FY2025": 1.1, "FY2024": 2.0, "FY2023": 2.1, "FY2022": 0.2, "FY2021": 0.7}),
    ("DATA", "Net gains on financial assets at amortised cost", {"FY2024": 0.2}),
    ("DATA", "Other operating income", {"FY2025": 49.2, "FY2024": 38.1, "FY2023": 10.1, "FY2022": 13.6, "FY2021": 8.4}),
    ("TOTAL", "Total operating income", {"FY2025": 473.4, "FY2024": 462.9, "FY2023": 476.2, "FY2022": 389.8, "FY2021": 323.4}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Provisions", {"FY2025": -3.0, "FY2024": 1.2, "FY2023": -2.0, "FY2022": -2.1, "FY2021": -1.7}),
    ("DATA", "Other expenses and staff costs / other administrative expenses", {"FY2025": -263.8, "FY2024": -265.0, "FY2023": -251.5, "FY2022": -221.9, "FY2021": -172.0}),
    ("DATA", "Depreciation and amortisation", {"FY2021": -7.3}),
    ("TOTAL", "Administrative expenses", {"FY2025": -266.8, "FY2024": -263.8, "FY2023": -253.5, "FY2022": -224.0, "FY2021": -173.7}),
    ("TOTAL", "Operating profit before impairment losses", {"FY2025": 206.6, "FY2024": 199.1, "FY2023": 222.6, "FY2022": 165.8, "FY2021": 142.4}),
    ("DATA", "Impairment releases/(losses) on loans and advances to customers", {"FY2025": 14.1, "FY2024": 19.1, "FY2023": -51.4, "FY2022": -5.1, "FY2021": -26.7}),
    ("DATA", "Impairment losses on lease modifications", {"FY2021": 0}),
    ("TOTAL", "Profit before taxation", {"FY2025": 220.7, "FY2024": 218.2, "FY2023": 171.2, "FY2022": 160.7, "FY2021": 115.7}),
    ("DATA", "Taxation", {"FY2025": -57.5, "FY2024": -56.1, "FY2023": -42.0, "FY2022": -42.7, "FY2021": -26.4}),
    ("TOTAL", "Profit after taxation — attributable to equity holders of the Company/Bank", {"FY2025": 163.2, "FY2024": 162.1, "FY2023": 129.2, "FY2022": 118.0, "FY2021": 89.3}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "FVOCI debt securities: Fair value movements", {"FY2025": -4.6, "FY2024": -3.3, "FY2023": -2.7, "FY2022": -2.2, "FY2021": 10.3}),
    ("DATA", "FVOCI debt securities: Amounts transferred to the income statement", {"FY2025": -1.1, "FY2024": -2.0, "FY2023": -2.1, "FY2022": -0.2, "FY2021": -0.7}),
    ("DATA", "Taxation on other comprehensive income", {"FY2025": 1.4, "FY2024": 1.3, "FY2023": 1.3, "FY2022": 1.0, "FY2021": -2.8}),
    ("TOTAL", "Total other comprehensive (expense)/income", {"FY2025": -4.3, "FY2024": -4.0, "FY2023": -3.6, "FY2022": -1.4, "FY2021": 6.8}),
    ("TOTAL", "Total comprehensive income attributable to equity holders of the Bank", {"FY2025": 158.9, "FY2024": 158.1, "FY2023": 125.7, "FY2022": 116.6, "FY2021": 96.1}),
]

bw.add_income_statement_sheet(
    title="Aldermore Bank PLC — Income Statement and Statement of Comprehensive Income",
    subtitle="Company (Bank solo) basis, £m, year ended 30 June",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=78,
    source_height=150,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_CHANGES_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo) Statement of changes in equity from each year's full "
    "statutory accounts filed at Companies House (company no. 00947662), £m:\n"
    f"FY2025 & FY2024: Full accounts made up to 30 June 2025, filed 04 Nov 2025, p.56 — {CH_2025_URL}\n"
    f"FY2023 & FY2022: Full accounts made up to 30 June 2023, filed 27 Oct 2023, p.54 — {CH_2023_URL}\n"
    f"FY2021: Full accounts made up to 30 June 2021, filed 04 Nov 2021, p.60 — {CH_2021_URL}\n"
    "Chronological roll-forward, oldest to newest. 'As at 30 June 2021' shows £987.2m in the FY2021 accounts' "
    "own Statement of Changes in Equity vs £987.1m on the face of the FY2021 Statement of Financial Position "
    "— a £0.1m rounding difference in the Bank's own disclosures, both transcribed as reported."
)

EQUITY_HEADERS = ["Share capital", "Share premium account", "Additional Tier 1 capital", "FVOCI reserve", "Retained earnings", "Total"]

equity_changes_rows = [
    ("TOTAL", "As at 1 July 2020", (3.3, 307.6, 61.0, 1.5, 522.9, 896.2)),
    ("DATA", "Profit after taxation (FY2021)", (None, None, None, None, 89.3, 89.3)),
    ("DATA", "Other comprehensive income (FY2021)", (None, None, None, 6.8, None, 6.9)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2021)", (None, None, None, None, -5.2, -5.2)),
    ("TOTAL", "As at 30 June 2021", (3.3, 307.6, 61.0, 8.3, 607.0, 987.2)),
    ("DATA", "Profit after taxation (FY2022)", (None, None, None, None, 118.0, 118.0)),
    ("DATA", "Other comprehensive loss (FY2022)", (None, None, None, -1.4, None, -1.4)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2022)", (None, None, None, None, -5.2, -5.2)),
    ("TOTAL", "As at 30 June 2022", (3.3, 307.5, 61.0, 6.9, 719.8, 1098.5)),
    ("DATA", "Profit after taxation (FY2023)", (None, None, None, None, 129.2, 129.2)),
    ("DATA", "Other comprehensive loss (FY2023)", (None, None, None, -3.6, None, -3.6)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2023)", (None, None, None, None, -5.2, -5.2)),
    ("TOTAL", "As at 30 June 2023", (3.3, 307.5, 61.0, 3.3, 843.9, 1219.0)),
    ("DATA", "Profit after taxation (FY2024)", (None, None, None, None, 162.1, 162.1)),
    ("DATA", "Other comprehensive loss (FY2024)", (None, None, None, -4.0, None, -4.0)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2024)", (None, None, None, None, -5.3, -5.3)),
    ("TOTAL", "As at 30 June 2024", (3.3, 307.5, 61.0, -0.7, 1000.7, 1371.8)),
    ("DATA", "Profit after taxation (FY2025)", (None, None, None, None, 163.2, 163.2)),
    ("DATA", "Other comprehensive loss (FY2025)", (None, None, None, -4.3, None, -4.3)),
    ("DATA", "Redemption of Additional Tier 1 capital", (None, None, -61.0, None, None, -61.0)),
    ("DATA", "Issuance of Additional Tier 1 capital", (None, None, 50.0, None, None, 50.0)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2025)", (None, None, None, None, -5.1, -5.1)),
    ("TOTAL", "As at 30 June 2025", (3.3, 307.5, 50.0, -5.0, 1158.8, 1514.6)),
]

bw.add_equity_changes_sheet(
    title="Aldermore Bank PLC — Statement of Changes in Equity",
    subtitle="Company (Bank solo) basis, £m, chronological FY2021-FY2025",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=54,
    source_height=150,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": 220.7, "FY2024": 218.2, "FY2023": 171.2, "FY2022": 160.7, "FY2021": 115.7}),
    ("DATA", "Adjustments for non-cash items and other adjustments included within the income statement", {"FY2025": -223.6, "FY2024": -188.9, "FY2023": -49.2, "FY2022": -22.3, "FY2021": 17.0}),
    ("DATA", "Change/(increase) in operating assets", {"FY2025": -1145.9, "FY2024": -439.9, "FY2023": -519.2, "FY2022": -389.0, "FY2021": 265.0}),
    ("DATA", "Change/increase in operating liabilities", {"FY2025": 283.3, "FY2024": 992.8, "FY2023": 1539.6, "FY2022": 1526.0, "FY2021": 498.4}),
    ("DATA", "Interest received on intercompany loan (operating basis, FY2024-FY2025)", {"FY2025": 164.5, "FY2024": 135.8}),
    ("DATA", "Interest paid on intercompany loan (operating basis, FY2024-FY2025)", {"FY2025": -53.9, "FY2024": -38.0}),
    ("DATA", "Interest paid on subordinated notes (operating basis, FY2024-FY2025)", {"FY2025": -7.9, "FY2024": -6.4}),
    ("DATA", "Interest received on debt securities (operating basis, FY2024-FY2025)", {"FY2025": 95.2, "FY2024": 86.3}),
    ("DATA", "Proceeds from disposal of non-current assets held for sale (operating basis, FY2024-FY2025)", {"FY2025": 0, "FY2024": 32.8}),
    ("DATA", "Income tax paid", {"FY2025": -57.4, "FY2024": -62.6, "FY2023": -33.9, "FY2022": -59.7, "FY2021": -12.0}),
    ("TOTAL", "Net cash flows (used in)/generated from operating activities", {"FY2025": -725.0, "FY2024": 730.1, "FY2023": 1108.5, "FY2022": 1215.7, "FY2021": 884.1}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities", {"FY2025": -1618.2, "FY2024": -1184.9, "FY2023": -358.2, "FY2022": -723.4, "FY2021": -444.6}),
    ("DATA", "Proceeds from sale and/or maturity of debt securities", {"FY2025": 1278.3, "FY2024": 421.2, "FY2023": 299.3, "FY2022": 159.6, "FY2021": 333.1}),
    ("DATA", "Capital repayments of debt securities", {"FY2025": 81.4, "FY2024": 367.2, "FY2023": 351.3, "FY2022": 223.3, "FY2021": 61.4}),
    ("DATA", "Interest received on debt securities (investing basis, FY2021-FY2023)", {"FY2023": 15.2, "FY2022": 7.6, "FY2021": 6.8}),
    ("DATA", "Purchase of property, plant and equipment and intangible assets", {"FY2025": -1.0, "FY2024": -5.1, "FY2023": -1.0, "FY2022": -1.9, "FY2021": -11.7}),
    ("TOTAL", "Net cash flows (used in)/generated from investing activities", {"FY2025": -259.5, "FY2024": -401.6, "FY2023": 306.5, "FY2022": -334.8, "FY2021": -55.0}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of subordinated debt", {"FY2024": -100.0, "FY2022": -60.0}),
    ("DATA", "Proceeds from issue of subordinated debt", {"FY2024": 100.0}),
    ("DATA", "Redemption of Additional Tier 1 Capital", {"FY2025": -61.0}),
    ("DATA", "Issuance of Additional Tier 1 Capital", {"FY2025": 50.0}),
    ("DATA", "Capital repayments on debt securities issued", {"FY2023": 0.4}),
    ("DATA", "Amounts paid on new intercompany loan", {"FY2023": -394.3, "FY2022": -694.4, "FY2021": -686.2}),
    ("DATA", "Interest received on intercompany loan (financing basis, FY2021-FY2023)", {"FY2023": 68.0, "FY2022": 30.3, "FY2021": 20.1}),
    ("DATA", "Deposit placed by related Group companies", {"FY2021": -12.3}),
    ("DATA", "Coupons paid on Additional Tier 1 capital", {"FY2025": -5.1, "FY2024": -5.3, "FY2023": -5.2, "FY2022": -5.2, "FY2021": -5.2}),
    ("DATA", "Interest paid on subordinated notes (financing basis, FY2021-FY2023)", {"FY2022": -7.4, "FY2021": -9.9}),
    ("DATA", "Repayment of lease liabilities - principal", {"FY2025": -2.3, "FY2024": -3.0, "FY2022": -2.8, "FY2021": -4.0}),
    ("DATA", "Interest paid on lease liabilities", {"FY2023": -0.1, "FY2022": -0.1, "FY2021": -0.2}),
    ("TOTAL", "Net cash generated/(used in) financing activities", {"FY2025": -18.4, "FY2024": -8.3, "FY2023": -331.2, "FY2022": -739.7, "FY2021": -697.7}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -1002.9, "FY2024": 320.2, "FY2023": 1083.8, "FY2022": 141.2, "FY2021": 131.4}),
    ("DATA", "Cash and cash equivalents at start of the period", {"FY2025": 2219.6, "FY2024": 1899.4, "FY2023": 815.1, "FY2022": 674.0, "FY2021": 542.6}),
    ("TOTAL", "Cash and cash equivalents at end of the period", {"FY2025": 1216.7, "FY2024": 2219.6, "FY2023": 1899.4, "FY2022": 815.2, "FY2021": 674.0}),
]

bw.add_cash_flow_sheet(
    title="Aldermore Bank PLC — Statement of Cash Flows",
    subtitle="Company (Bank solo) basis, £m, year ended 30 June",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=140,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
ASSET_QUALITY_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: figures are from each year's own full statutory accounts' 'Analysis of gross loans "
    "and advances' and 'Analysis of loss allowances' notes (IFRS 9 stage roll-forward tables), Bank solo "
    "basis. 'By product' figures (Business Finance / Property Finance) use the Bank's internal risk-category "
    "disclosure (excludes Property Development, which is separately disclosed only for irrevocable "
    "commitments, not drawn balances) and are only available at this granularity for FY2025/FY2024 in the "
    "documents reviewed; FY2023/FY2022/FY2021 are left blank for the by-product split rather than estimated. "
    "Stage totals (gross and ECL allowance) are available and tie out for all 5 years. FY2024's stage-total "
    "gross loans (11,549.3) differs by £0.1m from the FY2024 Balance Sheet's own 'Loans and advances to "
    "customers' figure (11,416.3 net + 133.0 allowance = 11,549.3) — consistent; both are transcribed as "
    "disclosed."
)

ASSET_QUALITY_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo) 'Analysis of gross loans and advances' and 'Analysis of "
    "loss allowances' notes, £m:\n"
    f"FY2025 & FY2024 (by product, Business/Property Finance split): Full accounts made up to 30 June 2025, "
    f"filed 04 Nov 2025, p.24-26 (Credit quality and performance of loans) — {CH_2025_URL}\n"
    f"FY2025 & FY2024 (by IFRS 9 stage, gross and allowance): Full accounts made up to 30 June 2025, filed "
    f"04 Nov 2025, p.84-86 (Note 14, Analysis of gross loans and advances / Analysis of loss allowances) — {CH_2025_URL}\n"
    f"FY2023 & FY2022 (by IFRS 9 stage, gross and allowance): Full accounts made up to 30 June 2023, filed "
    f"27 Oct 2023, p.84 (Note 13, Analysis of gross loans and advances / Analysis of loss allowances) — {CH_2023_URL}\n"
    f"FY2021 (by IFRS 9 stage, gross and allowance): Full accounts made up to 30 June 2021, filed 04 Nov "
    f"2021, p.90-91 (Note 18, Analysis of gross loans and advances / Analysis of loss allowances) — {CH_2021_URL}\n\n"
    + ASSET_QUALITY_PRESENTATION_NOTE
)

asset_quality_rows = [
    ("SECTION", "Gross loans and advances to customers, by product (excl. Property Development commitments)", {}),
    ("DATA", "Business Finance", {"FY2025": 3903.8, "FY2024": 3716.7}),
    ("DATA", "Property Finance", {"FY2025": 8728.4, "FY2024": 7832.5}),
    ("TOTAL", "Total gross loans and advances (by product)", {"FY2025": 12632.2, "FY2024": 11549.2}),
    ("SECTION", "Gross loans and advances to customers, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 11395.2, "FY2024": 10466.4, "FY2023": 10211.2, "FY2022": 9591.1, "FY2021": 9209.1}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": 814.8, "FY2024": 716.4, "FY2023": 664.9, "FY2022": 1026.0, "FY2021": 956.6}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": 422.2, "FY2024": 366.4, "FY2023": 287.3, "FY2022": 277.1, "FY2021": 343.9}),
    ("TOTAL", "Total gross loans and advances (by stage)", {"FY2025": 12632.2, "FY2024": 11549.3, "FY2023": 11163.4, "FY2022": 10894.2, "FY2021": 10509.6}),
    ("SECTION", "Allowance for impairment losses, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": -34.2, "FY2024": -50.2, "FY2023": -91.4, "FY2022": -48.3, "FY2021": -32.8}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": -22.6, "FY2024": -25.6, "FY2023": -25.2, "FY2022": -19.8, "FY2021": -24.1}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": -52.0, "FY2024": -57.2, "FY2023": -48.0, "FY2022": -48.7, "FY2021": -59.1}),
    ("TOTAL", "Total allowance for impairment losses", {"FY2025": -108.8, "FY2024": -133.0, "FY2023": -164.6, "FY2022": -116.8, "FY2021": -116.0}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "ECL coverage ratio (Total allowance / Total gross loans)", {"FY2025": "0.86%", "FY2024": "1.15%", "FY2023": "1.47%", "FY2022": "1.07%", "FY2021": "1.10%"}),
    ("DATA", "Stage 3 (NPL) ratio (Stage 3 gross loans / Total gross loans)", {"FY2025": "3.34%", "FY2024": "3.17%", "FY2023": "2.57%", "FY2022": "2.54%", "FY2021": "3.27%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross loans)", {"FY2025": "12.32%", "FY2024": "15.61%", "FY2023": "16.71%", "FY2022": "17.58%", "FY2021": "17.18%"}),
]

bw.add_asset_quality_sheet(
    title="Aldermore Bank PLC — Asset Quality / Credit Risk Disclosures",
    subtitle="Company (Bank solo) basis, £m",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=170,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Bank solo basis, {unit}" if unit else "Bank solo basis",
                         rows_data, sources_text, note=note, first_col_width=46, source_height=110)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1337.8, "FY2024": 1321.5, "FY2023": 1203.8, "FY2022": 1065.9, "FY2021": 947.0})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "18.4%", "FY2024": "19.2%", "FY2023": "18.5%", "FY2022": "17.0%", "FY2021": "15.9%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 1387.8, "FY2024": 1382.5, "FY2023": 1264.8, "FY2022": 1126.6, "FY2021": 1008.0})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "19.1%", "FY2024": "20.1%", "FY2023": "19.4%", "FY2022": "18.0%", "FY2021": "16.9%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 1487.8, "FY2024": 1482.5, "FY2023": 1364.8, "FY2022": 1226.6, "FY2021": 1168.0})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "20.5%", "FY2024": "21.6%", "FY2023": "21.0%", "FY2022": "19.6%", "FY2021": "19.6%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets (RWA)", {"FY2025": 7271.6, "FY2024": 6875.6, "FY2023": 6504.9, "FY2022": 6260.1, "FY2021": 5964.1})],
    p3_sources(),
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown (Pillar 3's UK OV1 template - placed next to
# Total RWAs, since it's itself a Pillar 3 disclosure)
# ---------------------------------------------------------------
RWA_BREAKDOWN_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: transcribed from each year's own Pillar 3 disclosures' 'Overview of RWA' table, Bank "
    "solo (not Group) column. This sheet's Total row ties out exactly to the Total RWAs sheet for all 5 years."
)

RWA_BREAKDOWN_SOURCES = (
    "Sources — Aldermore Bank PLC solo figures from the 'Overview of RWA' table, Aldermore Group PLC Pillar 3 "
    "Disclosures:\n"
    f"FY2025 & FY2024: Pillar 3 Disclosures for the year ended 30 June 2025, p.9 (Overview Of RWA, Bank "
    f"column) — {P3_2025_URL}\n"
    f"FY2023: Pillar 3 Disclosures for the year ended 30 June 2024, p.8 (Overview Of RWA, Bank column, "
    f"FY2023 comparative) — {P3_2024_URL}\n"
    f"FY2022 & FY2021: Pillar 3 Disclosures for the year ended 30 June 2022, p.7 (Overview of RWA, Bank "
    f"column) — {P3_2022_URL}\n\n" + RWA_BREAKDOWN_PRESENTATION_NOTE
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 6410.7, "FY2024": 6071.2, "FY2023": 5802.1, "FY2022": 5624.9, "FY2021": 5338.2}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 4.8, "FY2024": 20.9, "FY2023": 37.1, "FY2022": 0.9, "FY2021": 0.9}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2025": 25.5, "FY2024": 40.0, "FY2023": 22.5, "FY2022": 29.2, "FY2021": 23.1}),
    ("DATA", "Position, foreign exchange and commodities risks", {"FY2025": 0, "FY2024": 0.1, "FY2023": 1.8, "FY2022": 0.4, "FY2021": 0.1}),
    ("DATA", "Operational risk", {"FY2025": 830.6, "FY2024": 743.4, "FY2023": 641.4, "FY2022": 604.7, "FY2021": 601.8}),
    ("TOTAL", "Total risk-weighted assets (RWA)", {"FY2025": 7271.6, "FY2024": 6875.6, "FY2023": 6504.9, "FY2022": 6260.1, "FY2021": 5964.1}),
]

bw.add_rwa_breakdown_sheet(
    title="Aldermore Bank PLC — RWA Breakdown (Overview of Risk Weighted Assets)",
    subtitle="Bank solo basis, £m",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=140,
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks (£m)", {"FY2025": 15674.3, "FY2024": 14337.2, "FY2023": 13609.6, "FY2022": 13850.3, "FY2021": "n/a"}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "8.9%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "8.1%", "FY2021": "n/a"}),
    ],
    p3_sources(),
    note="FY2021 leverage ratio disclosure basis was introduced from 1 January 2022; the FY2022 Pillar 3 report explicitly "
         "marks FY2021 as 'n/a' with no comparative provided under the new template.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value average (£m)", {"FY2025": 3723.1, "FY2024": 4208.6, "FY2023": 3280.6, "FY2022": 2838.5, "FY2021": "n/a"}),
        ("Total net cash outflows, adjusted value (£m)", {"FY2025": 1968.3, "FY2024": 1959.4, "FY2023": 1686.4, "FY2022": 772.6, "FY2021": "n/a"}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "189.2%", "FY2024": "214.8%", "FY2023": "194.5%", "FY2022": "367.4%", "FY2021": "n/a"}),
    ],
    p3_sources(),
    note="LCR is computed as a 12-month average to the period end. FY2021 is 'n/a' — no comparative was provided under "
         "the disclosure template introduced from 1 January 2022 (see FY2022 Pillar 3 report).",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2025": 15972.4, "FY2024": 16133.4, "FY2023": 15490.2, "FY2022": 15667.6, "FY2021": "n/a"}),
        ("Total required stable funding (£m)", {"FY2025": 12166.9, "FY2024": 11778.0, "FY2023": 12161.3, "FY2022": 12169.6, "FY2021": "n/a"}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "131.3%", "FY2024": "137.0%", "FY2023": "127.4%", "FY2022": "128.7%", "FY2021": "n/a"}),
    ],
    p3_sources(),
    note="NSFR is computed as a 4-quarter average to the period end. FY2021 is 'n/a' — no comparative was provided under "
         "the disclosure template introduced from 1 January 2022 (see FY2022 Pillar 3 report).",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="MREL is not disclosed for Aldermore Bank PLC/Aldermore Group PLC in any Pillar 3 report reviewed — the Group "
         "sits below the balance-sheet threshold at which the Bank of England sets a bail-in MREL requirement above "
    "minimum capital requirements, so no separate MREL ratio is published.",
)

# ---------------------------------------------------------------
# Interim Pillar 3 disclosures
# ---------------------------------------------------------------
INTERIM_HEADERS = [
    "Period",
    "Disclosure type",
    "Metric",
    "Value",
    "Unit",
    "Basis",
    "Source document",
    "Page / table",
]

INTERIM_PERIODS = [
    ("31 Dec 2025", "H1 2025 interim (current period)"),
    ("30 Jun 2025", "H1 2025 interim (comparative)"),
    ("31 Dec 2024", "H1 2025 interim (comparative)"),
]

INTERIM_METRICS = [
    ("CET1 capital", [1342.5, 1337.8, 1306.1], "£m"),
    ("Tier 1 capital", [1392.5, 1387.8, 1367.1], "£m"),
    ("Total capital", [1692.5, 1487.8, 1467.1], "£m"),
    ("Total risk-weighted exposure amount", [7352.0, 7271.6, 6997.3], "£m"),
    ("CET1 ratio", ["18.3%", "18.4%", "18.7%"], "%"),
    ("Tier 1 ratio", ["18.9%", "19.1%", "19.5%"], "%"),
    ("Total capital ratio", ["23.0%", "20.5%", "21.0%"], "%"),
    ("Total exposure measure excluding claims on central banks", [15369.1, 15526.0, 14826.8], "£m"),
    ("Leverage ratio excluding claims on central banks", ["9.1%", "8.9%", "9.2%"], "%"),
    ("Total high-quality liquid assets (HQLA), weighted-value average", [3518.6, 3723.1, 4062.3], "£m"),
    ("Total net cash outflows (adjusted value)", [1964.8, 1968.3, 2047.1], "£m"),
    ("Liquidity coverage ratio", ["179.1%", "189.2%", "198.4%"], "%"),
    ("Total available stable funding", [16221.9, 15972.4, 16013.1], "£m"),
    ("Total required stable funding", [12699.7, 12166.9, 11856.4], "£m"),
    ("NSFR ratio", ["127.7%", "131.3%", "135.1%"], "%"),
    ("MREL ratio", ["Not disclosed", "Not disclosed", "Not disclosed"], "%"),
]

interim_rows = []
for period_index, (period, disclosure_type) in enumerate(INTERIM_PERIODS):
    for metric_name, values, unit in INTERIM_METRICS:
        interim_rows.append(
            [
                period,
                disclosure_type,
                metric_name,
                values[period_index],
                unit,
                "Aldermore Bank PLC (Bank solo)",
                "Aldermore Group PLC Interim Pillar 3 Disclosure — 31 December 2025",
                "p.4, Key Metrics (Bank column)",
            ]
        )

interim_hyperlinks = {(i, 6): INTERIM_P3_2025_URL for i in range(len(interim_rows))}
bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=interim_rows,
    hyperlink_cells=interim_hyperlinks,
    title="Aldermore Bank PLC — Interim Pillar 3",
    subtitle="Bank solo basis; amounts in £m and ratios in %, as disclosed in the official interim Key Metrics table",
    note=(
        "Source: Aldermore Group PLC Interim Pillar 3 Disclosure as at 31 December 2025, p.4, Key Metrics — Bank column. "
        f"Official PDF: {INTERIM_P3_2025_URL}\n"
        "The document reports 31 Dec 2025 and comparative 30 Jun 2025 and 31 Dec 2024 figures. No separate official "
        "half-year Pillar 3 document was located in the archive for 2021, 2022, 2023, or 2024; those periods are therefore "
        "not inferred or backfilled. MREL is not included in the Key Metrics table and is recorded as not disclosed."
    ),
)
# Keep the source register immediately after the matrix so the current
# verifier can discover it without changing the shared helper.
interim_ws = bw.wb["Interim Pillar 3"]
interim_ws.delete_rows(5 + len({row[2] for row in interim_rows}), 2)
for row_number in range(5, interim_ws.max_row + 1):
    if interim_ws.cell(row=row_number, column=1).value == "Source register":
        source_register_row = row_number
        break
    for column_number in range(4, interim_ws.max_column + 1):
        cell = interim_ws.cell(row=row_number, column=column_number)
        if cell.value not in (None, ""):
            cell.hyperlink = INTERIM_P3_2025_URL
            cell.style = "Hyperlink"
for row_number in range(source_register_row + 2, interim_ws.max_row + 1):
    if interim_ws.cell(row=row_number, column=1).value in (None, ""):
        break
    source_cell = interim_ws.cell(row=row_number, column=3)
    source_cell.hyperlink = INTERIM_P3_2025_URL
    source_cell.style = "Hyperlink"

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 20618.2, "FY2024": 20195.5, "FY2023": 19051.7, "FY2022": 17290.8, "FY2021": 15583.0}),
        ("Loans and advances to customers", {"FY2025": 12523.4, "FY2024": 11416.3, "FY2023": 10998.9, "FY2022": 10777.3, "FY2021": 10393.6}),
        ("Customers' accounts", {"FY2025": 17047.6, "FY2024": 16306.7, "FY2023": 15033.3, "FY2022": 14105.4, "FY2021": 12427.3}),
        ("Total equity", {"FY2025": 1514.6, "FY2024": 1371.8, "FY2023": 1219.0, "FY2022": 1098.6, "FY2021": 987.1}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 473.4, "FY2024": 462.9, "FY2023": 476.2, "FY2022": 389.8, "FY2021": 323.4}),
        ("Administrative expenses", {"FY2025": -266.8, "FY2024": -263.8, "FY2023": -253.5, "FY2022": -224.0, "FY2021": -173.7}),
        ("Profit after taxation", {"FY2025": 163.2, "FY2024": 162.1, "FY2023": 129.2, "FY2022": 118.0, "FY2021": 89.3}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1371.8, "FY2024": 1219.0, "FY2023": 1098.5, "FY2022": 987.1, "FY2021": 896.2}),
        ("Total comprehensive income", {"FY2025": 158.9, "FY2024": 158.1, "FY2023": 125.7, "FY2022": 116.6, "FY2021": 96.1}),
        ("Other equity movements, net", {"FY2025": -16.1, "FY2024": -5.3, "FY2023": -5.2, "FY2022": -5.2, "FY2021": -5.2}),
        ("Closing equity", {"FY2025": 1514.6, "FY2024": 1371.8, "FY2023": 1219.0, "FY2022": 1098.6, "FY2021": 987.1}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": -725.0, "FY2024": 730.1, "FY2023": 1108.5, "FY2022": 1215.7, "FY2021": 884.1}),
        ("Net cash from investing activities", {"FY2025": -259.5, "FY2024": -401.6, "FY2023": 306.5, "FY2022": -334.8, "FY2021": -55.0}),
        ("Net cash from financing activities", {"FY2025": -18.4, "FY2024": -8.3, "FY2023": -331.2, "FY2022": -739.7, "FY2021": -697.7}),
        ("Cash and cash equivalents at end of year", {"FY2025": 1216.7, "FY2024": 2219.6, "FY2023": 1899.4, "FY2022": 815.2, "FY2021": 674.0}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "18.4%", "FY2024": "19.2%", "FY2023": "18.5%", "FY2022": "17.0%", "FY2021": "15.9%"}),
        ("Tier 1 Ratio", {"FY2025": "19.1%", "FY2024": "20.1%", "FY2023": "19.4%", "FY2022": "18.0%", "FY2021": "16.9%"}),
        ("Total Capital Ratio", {"FY2025": "20.5%", "FY2024": "21.6%", "FY2023": "21.0%", "FY2022": "19.6%", "FY2021": "19.6%"}),
        ("Leverage Ratio", {"FY2025": "8.9%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "8.1%"}),
        ("LCR", {"FY2025": "189.2%", "FY2024": "214.8%", "FY2023": "194.5%", "FY2022": "367.4%"}),
        ("NSFR", {"FY2025": "131.3%", "FY2024": "137.0%", "FY2023": "127.4%", "FY2022": "128.7%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Fiscal year ends 30 June. Balance Sheet, Profit & Loss, "
         "Statement of Changes in Equity and Cash Flow figures are all Bank-solo; Pillar 3 ratios use the Bank-solo "
         "columns of Aldermore Group PLC's Pillar 3 disclosures (the only level at which Pillar 3 is published). "
         "'Other equity movements, net' combines Additional Tier 1 capital issuance/redemption and AT1 coupon "
         "payments. Leverage/LCR/NSFR have no FY2021 figure — see the Leverage Ratio/LCR/NSFR sheets for the "
         "disclosure-template basis note.",
)

bw.save("/Users/armaan/code/katalysis/banks/ALDERMORE FINANCIALS.xlsx")
