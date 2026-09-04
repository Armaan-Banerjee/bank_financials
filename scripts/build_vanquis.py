import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2021_URL = "https://www.vanquis.com/wp-content/uploads/2025/05/Vanquis_Bank_Ltd_31_12_2021_Signed.pdf"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/02558509/filing-history/MzQxNzkzNTkxNWFkaXF6a2N4/document?format=pdf&download=0"
AR2025_URL = "https://www.vanquis.com/wp-content/uploads/2026/03/VBL-stats-2025-FINAL-Fully-Signed.pdf"

P3_2021_URL = "https://www.vanquis.com/wp-content/uploads/2025/05/Provident_Financial_plc_Pillar_3_Disclosures_2021.pdf"
P3_2023_URL = "https://www.vanquis.com/wp-content/uploads/2025/05/04-04-24_Pillar-3-Disclosures-2023.pdf"
P3_2024_URL = "https://www.vanquis.com/wp-content/uploads/2025/05/Vanquis_Banking_Group_plc_Pillar_3_Disclosures_2024.pdf"
P3_2025_URL = "https://www.vanquis.com/wp-content/uploads/2026/02/DEC25_VANQ_Pillar-3-Disclosure_Annual_FINAL.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Vanquis Bank Limited (company number 02558509, FRN 221156) is the PRA-authorised entity and the "
    "principal banking subsidiary of the listed Vanquis Banking Group plc (renamed from Provident Financial plc in "
    "2021 - the Bank's own name has not changed). The Cash Flow Statement sheet is on Vanquis Bank Limited's own "
    "entity-level (Company) basis. Pillar 3 disclosures, however, are published ONLY at the wider Vanquis Banking "
    "Group plc consolidated level - the Group's Pillar 3 Disclosure Policy states explicitly that disclosures 'cover "
    "the Group as a whole' with no separate Bank-only breakout (unlike some other banks in this workbook series, "
    "e.g. Clydesdale, where a dedicated Bank-level Pillar 3 appendix exists). On 31 December 2024 the Group's two "
    "principal trading entities were Vanquis Bank Limited (the Bank) and Moneybarn No.1 Limited (a non-bank vehicle "
    "finance lender) - so every Pillar 3 sheet in this workbook is on a basis that includes Moneybarn as well as the "
    "Bank, and is NOT directly comparable to the Bank-only Cash Flow Statement sheet. This is a structural limitation "
    "of what Vanquis publicly discloses, not a choice made in compiling this workbook."
)

DISCONTINUED_NOTE = (
    "The Company sold its Personal Loans portfolio in March 2025, presented as a discontinued operation under IFRS "
    f"5 in the FY2025 Annual Report - this is the main driver of FY2025's much lower operating cash flow (£19.6m) "
    f"and investing outflow (net purchases of investment securities) versus FY2024 (Annual Report and Financial "
    f"Statements, year ended 31 December 2025, Note 2) - {AR2025_URL}."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Vanquis Bank Limited's own (Company) Statement of Cash Flows, £m:\n"
    f"FY2025 & FY2024: Vanquis Bank Limited Annual Report and Financial Statements, year ended 31 December 2025, "
    f"p.32 (Statement of Cash Flows; FY2024 restated - see Note 30) - {AR2025_URL}\n"
    f"FY2023 & FY2022: Vanquis Bank Limited Annual Report and Financial Statements, year ended 31 December 2023 "
    f"(Companies House filing, 18 Apr 2024), p.34 (Statement of Cash Flows; FY2022 reclassified between borrowings "
    f"proceeds/repayments - see note 1 on that statement) - {AR2023_URL}\n"
    f"FY2021: Vanquis Bank Limited Annual Report and Financial Statements, year ended 31 December 2021, p.59 "
    f"(Statement of Cash Flows) - {AR2021_URL}\n"
    "Note: presentation changed between report vintages - FY2021-FY2023 show 'Funding costs paid'/'Tax paid' as "
    "separate operating-activities lines and no loan-to-related-party financing lines; FY2024-FY2025 show 'Tax "
    "received'/no separate funding-costs line, and add 'Financing of loan to related party'/'Repayment of loan to "
    "related party' lines - each year's own as-reported presentation is preserved rather than forced into a common "
    "shape. Section totals and cash/cash equivalents figures are consistent and comparable across all 5 years "
    "(each year's opening balance matches the prior year's closing balance exactly). Note: FY2023's financing-"
    "activities line items sum to £809.2m against a printed 'Net cash generated from financing activities' total of "
    "£809.1m - an immaterial £0.1m artefact of each line being independently rounded to one decimal place in the "
    "source document itself (not a transcription error here); the printed total (£809.1m, used above) is the "
    "figure consistent with the overall net-change-in-cash reconciliation.\n\n"
    + ENTITY_NOTE + "\n\n" + DISCONTINUED_NOTE
)


def p3_sources(doc_label, doc_url, page_km1_1, page_km1_2=None):
    lines = [
        "Sources - Vanquis Banking Group plc (consolidated, includes Vanquis Bank Limited and Moneybarn No.1 "
        "Limited - see entity note on the Cash Flow Statement sheet) Pillar 3 basis:",
        f"{doc_label}: Vanquis Banking Group plc Pillar 3 Disclosures, p.{page_km1_1} - {doc_url}",
    ]
    if page_km1_2:
        lines.append(f"(liquidity metrics on p.{page_km1_2} of the same document)")
    return "\n".join(lines)


bw = BankWorkbook(bank_name="Vanquis Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="0B4F6C")

STATEMENTS_ENTITY_NOTE = (
    "Balance Sheet, Profit & Loss, Statement of Changes in Equity and Asset Quality are all on Vanquis Bank "
    "Limited's own entity-level (Company) basis, £m - the same basis as the existing Cash Flow Statement sheet "
    "(see that sheet's entity note for the wider Pillar 3 basis mismatch, which does not affect these 4 sheets)."
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: the Company's income statement structure changed materially over this period. FY2022-"
    "FY2025 show a gross 'Interest income'/'Interest expense'/'Net interest income' split; FY2021's own Annual "
    "Report instead shows a single net 'Income' line, 'Funding costs', and 'Net interest margin' (the FY2021 "
    "value used on the Net interest income row, 379.5, is that year's own Net interest margin - functionally "
    "equivalent but not a like-for-like gross split) - Interest income/expense are left blank for FY2021 as this "
    "split was not published that year. FY2021's own 'Income' (405.4) and 'Funding costs' (25.9) lines are shown "
    "on their own rows since they don't map cleanly onto later years' structure. FY2023/FY2022's income "
    "statements also disclose Exceptional items and an 'Adjusted profit before tax' as a memo add-back below the "
    "primary statement (already embedded within Operating costs, not a separate deduction) - not reproduced as "
    "its own row for consistency with FY2024/FY2025, which don't disclose that split at all. From FY2024 onward "
    "the Company splits 'continuing'/'discontinued operations' (following the March 2025 sale of the Personal "
    "Loans portfolio, presented retrospectively in FY2024's own comparative) - FY2023/FY2022/FY2021 predate this "
    "split and show one unified profit figure. 'Profit for the year' and 'Total comprehensive income for the "
    "year' are the two rows populated and exactly comparable across all 5 years."
)

bw.add_balance_sheet_sheet(
    title="Vanquis Bank Limited — Balance Sheet",
    subtitle="Vanquis Bank Limited (Company) basis, £m.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and cash equivalents", {"FY2025": 745.8, "FY2024": 945.0, "FY2023": 680.1, "FY2022": 413.0, "FY2021": 413.4}),
        ("DATA", "Investment securities", {"FY2025": 254.6, "FY2024": 0}),
        ("DATA", "Amounts receivable from customers", {"FY2025": 2003.2, "FY2024": 1419.2, "FY2023": 1382.9, "FY2022": 1257.9, "FY2021": 1091.5}),
        ("DATA", "Trade and other receivables", {"FY2025": 121.2, "FY2024": 83.5, "FY2023": 67.4, "FY2022": 40.3, "FY2021": 30.5}),
        ("DATA", "Loan to related party / ultimate parent undertaking", {"FY2025": 359.2, "FY2024": 379.7, "FY2023": 398.4, "FY2022": 69.3, "FY2021": 69.3}),
        ("DATA", "Investments", {"FY2025": 2.4, "FY2024": 2.3, "FY2023": 5.4, "FY2022": 10.7, "FY2021": 9.1}),
        ("DATA", "Property, plant and equipment", {"FY2025": 7.2, "FY2024": 5.4, "FY2023": 4.9, "FY2022": 4.8, "FY2021": 5.0}),
        ("DATA", "Right-of-use assets", {"FY2025": 12.1, "FY2024": 9.0, "FY2023": 10.4, "FY2022": 18.0, "FY2021": 30.6}),
        ("DATA", "Intangible assets", {"FY2025": 55.4, "FY2024": 49.5, "FY2023": 38.4, "FY2022": 34.5, "FY2021": 24.5}),
        ("DATA", "Derivative financial instruments (asset)", {"FY2025": 4.4, "FY2024": 0.2, "FY2023": 1.2, "FY2022": 0}),
        ("DATA", "Current tax assets", {"FY2025": 0, "FY2024": 3.8, "FY2023": 8.3, "FY2022": 3.4, "FY2021": 1.4}),
        ("DATA", "Deferred tax assets", {"FY2025": 8.5, "FY2024": 9.8, "FY2023": 12.1, "FY2022": 15.5, "FY2021": 25.0}),
        ("TOTAL", "Total assets", {"FY2025": 3574.0, "FY2024": 2907.4, "FY2023": 2609.5, "FY2022": 1867.4, "FY2021": 1700.3}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Trade and other payables", {"FY2025": 76.7, "FY2024": 82.6, "FY2023": 61.6, "FY2022": 175.1, "FY2021": 81.3}),
        ("DATA", "Current tax liabilities", {"FY2025": 8.1, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("DATA", "Provisions", {"FY2025": 3.0, "FY2024": 9.1, "FY2023": 2.7, "FY2022": 2.2, "FY2021": 5.3}),
        ("DATA", "Lease liabilities", {"FY2025": 21.2, "FY2024": 21.1, "FY2023": 25.3, "FY2022": 30.8, "FY2021": 37.6}),
        ("DATA", "Retail deposits", {"FY2025": 3019.9, "FY2024": 2428.1, "FY2023": 1950.5, "FY2022": 1100.6, "FY2021": 1018.6}),
        ("DATA", "Derivative financial instruments (liability)", {"FY2025": 7.1, "FY2024": 0.6, "FY2023": 1.0, "FY2022": 0}),
        ("DATA", "Central bank facilities", {"FY2025": 0, "FY2024": 4.2}),
        ("DATA", "Collateralised loan", {"FY2023": 174.7, "FY2022": 173.7, "FY2021": 172.2}),
        ("TOTAL", "Total liabilities", {"FY2025": 3136.0, "FY2024": 2545.7, "FY2023": 2215.8, "FY2022": 1482.4, "FY2021": 1315.0}),
        ("SECTION", "Equity", {}),
        ("DATA", "Share capital", {"FY2025": 124.2, "FY2024": 124.2, "FY2023": 124.2, "FY2022": 124.2, "FY2021": 124.2}),
        ("DATA", "Share based payment reserve", {"FY2025": 1.7, "FY2024": 1.6, "FY2023": 1.8, "FY2022": 2.3, "FY2021": 1.9}),
        ("DATA", "Retained earnings", {"FY2025": 252.2, "FY2024": 235.9, "FY2023": 267.7, "FY2022": 258.5, "FY2021": 259.2}),
        ("DATA", "Other equity instruments", {"FY2025": 59.9, "FY2024": 0}),
        ("TOTAL", "Total equity", {"FY2025": 438.0, "FY2024": 361.7, "FY2023": 393.7, "FY2022": 385.0, "FY2021": 385.3}),
        ("TOTAL", "Total liabilities and equity", {"FY2025": 3574.0, "FY2024": 2907.4, "FY2023": 2609.5, "FY2022": 1867.4, "FY2021": 1700.3}),
    ],
    sources_text=(
        "Sources - Vanquis Bank Limited's own (Company) Statement of Financial Position, £m:\n"
        f"FY2025 & FY2024: Annual Report and Financial Statements, year ended 31 December 2025, p.30 - {AR2025_URL}\n"
        f"FY2023 & FY2022: Annual Report and Financial Statements, year ended 31 December 2023 (Companies House "
        f"filing, 18 Apr 2024), p.31 - {AR2023_URL}\n"
        f"FY2021: Annual Report and Financial Statements, year ended 31 December 2021, p.57 - {AR2021_URL}\n"
        "Note: 'Loan to related party' (FY2023-FY2025) was labelled 'Loan to ultimate parent undertaking' in "
        "FY2021-FY2022's own reports - same line, relabelled. 'Investment securities', 'Central bank facilities' "
        "and 'Other equity instruments' are new lines that only start appearing from FY2024/FY2025 (shown as 0 "
        "where the line exists that year at a nil balance, left blank where the line simply didn't exist yet). "
        "'Collateralised loan' (£172.2m-£174.7m, FY2021-FY2023) is not shown as a separate line in FY2024/FY2025's "
        "own Balance Sheet - not reproduced as a blank continuing line since it is genuinely absent from those "
        "years' own statements. Total assets = Total liabilities + Total equity exactly for all 5 years.\n\n"
        + STATEMENTS_ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£m)",
)

bw.add_income_statement_sheet(
    title="Vanquis Bank Limited — Profit & Loss",
    subtitle="Vanquis Bank Limited (Company) basis, £m. See presentation note at bottom re: structure changes across years.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest income", {"FY2025": 460.8, "FY2024": 434.8, "FY2023": 411.4, "FY2022": 354.7}),
        ("DATA", "Interest expense", {"FY2025": -121.1, "FY2024": -105.0, "FY2023": -69.8, "FY2022": -24.5}),
        ("TOTAL", "Net interest income", {"FY2025": 339.7, "FY2024": 329.8, "FY2023": 341.6, "FY2022": 330.2, "FY2021": 379.5}),
        ("DATA", "Income (FY2021 net presentation, pre-funding-costs)", {"FY2021": 405.4}),
        ("DATA", "Funding costs (FY2021 presentation)", {"FY2021": -25.9}),
        ("DATA", "Fee and commission income", {"FY2025": 36.7, "FY2024": 36.8, "FY2023": 44.2, "FY2022": 47.0}),
        ("DATA", "Fee and commission expense", {"FY2025": -2.4, "FY2024": -1.7, "FY2023": -1.7, "FY2022": -2.8}),
        ("TOTAL", "Net fee and commission income", {"FY2025": 34.3, "FY2024": 35.1, "FY2023": 42.5, "FY2022": 44.2}),
        ("DATA", "Other income", {"FY2025": 0.3, "FY2024": 1.4, "FY2023": 1.3, "FY2022": 1.0}),
        ("TOTAL", "Total income", {"FY2025": 374.3, "FY2024": 366.3, "FY2023": 385.4, "FY2022": 375.4}),
        ("SECTION", "Costs", {}),
        ("DATA", "Impairment charges", {"FY2025": -139.2, "FY2024": -124.7, "FY2023": -150.9, "FY2022": -25.3, "FY2021": -5.9}),
        ("TOTAL", "Risk-adjusted income", {"FY2025": 235.1, "FY2024": 241.6, "FY2023": 234.5, "FY2022": 350.1, "FY2021": 373.6}),
        ("DATA", "Operating costs", {"FY2025": -190.6, "FY2024": -236.6, "FY2023": -223.4, "FY2022": -219.7, "FY2021": -195.6}),
        ("TOTAL", "Statutory profit before taxation", {"FY2025": 44.5, "FY2024": 5.0, "FY2023": 11.1, "FY2022": 130.4, "FY2021": 178.0}),
        ("DATA", "Tax (charge)/credit", {"FY2025": -9.5, "FY2024": 1.2, "FY2023": -3.5, "FY2022": -36.6, "FY2021": -32.0}),
        ("TOTAL", "Statutory profit after tax from continuing operations", {"FY2025": 35.0, "FY2024": 6.2}),
        ("DATA", "Profit after taxation from discontinued operations", {"FY2025": 0.7, "FY2024": 1.3}),
        ("TOTAL", "Profit for the year", {"FY2025": 35.7, "FY2024": 7.5, "FY2023": 7.6, "FY2022": 93.8, "FY2021": 146.0}),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Fair value movements transferred to income statement", {"FY2021": -5.3}),
        ("DATA", "Tax on items taken directly to other comprehensive income", {"FY2021": 1.4}),
        ("TOTAL", "Other comprehensive (expense)/income for the year", {"FY2021": -3.9}),
        ("TOTAL", "Total comprehensive income for the year", {"FY2025": 35.7, "FY2024": 7.5, "FY2023": 7.6, "FY2022": 93.8, "FY2021": 142.1}),
    ],
    sources_text=(
        "Sources - Vanquis Bank Limited's own (Company) Income Statement, £m:\n"
        f"FY2025 & FY2024: Annual Report and Financial Statements, year ended 31 December 2025, p.29 (Income "
        f"Statement; there is no other comprehensive income for either year) - {AR2025_URL}\n"
        f"FY2023 & FY2022: Annual Report and Financial Statements, year ended 31 December 2023 (Companies House "
        f"filing, 18 Apr 2024), p.30 (Income Statement; there is no other comprehensive income for either year) - "
        f"{AR2023_URL}\n"
        f"FY2021: Annual Report and Financial Statements, year ended 31 December 2021, p.56 (Income Statement "
        f"and Statement of Comprehensive Income) - {AR2021_URL}\n\n"
        + PRESENTATION_NOTE + "\n\n" + STATEMENTS_ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=220,
    unit_suffix=" (£m)",
)

bw.add_equity_changes_sheet(
    title="Vanquis Bank Limited — Statement of Changes in Equity",
    subtitle="Vanquis Bank Limited (Company) basis, £m, chronological (oldest to newest).",
    headers=["Share capital", "Share-based payment reserve", "Fair value reserve", "Retained earnings", "Other equity instruments", "Total equity"],
    rows=[
        ("TOTAL", "At 31 December 2020 / At 1 January 2021", (124.2, 2.0, 3.9, 197.0, None, 327.1)),
        ("DATA", "Profit for the year", (None, None, None, 146.0, None, 146.0)),
        ("DATA", "Fair value movements transferred to income statement", (None, None, -5.3, None, None, -5.3)),
        ("DATA", "Tax on items taken directly to other comprehensive income", (None, None, 1.4, None, None, 1.4)),
        ("TOTAL", "Total comprehensive income for the year (FY2021)", (None, None, -3.9, 146.0, None, 142.1)),
        ("DATA", "Share-based payment charge", (None, 1.1, None, None, None, 1.1)),
        ("DATA", "Transfer of share-based payment reserve", (None, -1.2, None, 1.2, None, 0)),
        ("DATA", "Dividends", (None, None, None, -85.0, None, -85.0)),
        ("TOTAL", "At 31 December 2021 / At 1 January 2022", (124.2, 1.9, 0, 259.2, None, 385.3)),
        ("DATA", "Profit for the year", (None, None, None, 93.8, None, 93.8)),
        ("TOTAL", "Total comprehensive income for the year (FY2022)", (None, None, None, 93.8, None, 93.8)),
        ("DATA", "Share-based payment charge", (None, 1.0, None, None, None, 1.0)),
        ("DATA", "Transfer of share-based payment reserve", (None, -0.6, None, 0.6, None, 0)),
        ("DATA", "Dividends", (None, None, None, -95.1, None, -95.1)),
        ("TOTAL", "At 31 December 2022 / At 1 January 2023", (124.2, 2.3, None, 258.5, None, 385.0)),
        ("DATA", "Profit for the year", (None, None, None, 7.6, None, 7.6)),
        ("TOTAL", "Total comprehensive income for the year (FY2023)", (None, None, None, 7.6, None, 7.6)),
        ("DATA", "Share-based payment charge", (None, 1.1, None, None, None, 1.1)),
        ("DATA", "Transfer of share-based payment reserve", (None, -1.6, None, 1.6, None, 0)),
        ("TOTAL", "At 31 December 2023 / At 1 January 2024", (124.2, 1.8, None, 267.7, None, 393.7)),
        ("DATA", "Profit for the year", (None, None, None, 7.5, None, 7.5)),
        ("TOTAL", "Total comprehensive income for the year (FY2024)", (None, None, None, 7.5, None, 7.5)),
        ("DATA", "Share-based payment charge", (None, 0.5, None, None, None, 0.5)),
        ("DATA", "Transfer of share-based payment reserve", (None, -0.7, None, 0.7, None, 0)),
        ("DATA", "Dividends", (None, None, None, -40.0, None, -40.0)),
        ("TOTAL", "At 31 December 2024 / At 1 January 2025", (124.2, 1.6, None, 235.9, None, 361.7)),
        ("DATA", "Profit for the year", (None, None, None, 35.7, None, 35.7)),
        ("TOTAL", "Total comprehensive income for the year (FY2025)", (None, None, None, 35.7, None, 35.7)),
        ("DATA", "Share-based payment charge", (None, 0.7, None, None, None, 0.7)),
        ("DATA", "Transfer of share-based payment reserve", (None, -0.6, None, 0.6, None, 0)),
        ("DATA", "Issuance of other equity instruments", (None, None, None, None, 59.9, 59.9)),
        ("DATA", "Dividends", (None, None, None, -20.0, None, -20.0)),
        ("TOTAL", "At 31 December 2025", (124.2, 1.7, None, 252.2, 59.9, 438.0)),
    ],
    sources_text=(
        "Sources - Vanquis Bank Limited's own (Company) Statement of Changes in Shareholder's Equity, £m:\n"
        f"FY2021 opening & FY2021 movements: Annual Report and Financial Statements, year ended 31 December "
        f"2021, p.58 - {AR2021_URL}\n"
        f"FY2022 & FY2023 movements: Annual Report and Financial Statements, year ended 31 December 2023 "
        f"(Companies House filing, 18 Apr 2024), p.32 - {AR2023_URL}\n"
        f"FY2024 & FY2025 movements: Annual Report and Financial Statements, year ended 31 December 2025, p.31 - "
        f"{AR2025_URL}\n"
        "Note: the Fair value reserve fully unwound during FY2021 (£3.9m to £0.0m) and does not appear as a "
        "column in any later report - shown as None (not applicable) from FY2022 onward rather than a fabricated "
        "zero row. 'Other equity instruments' (£59.9m AT1 issuance) is unique to FY2025. Zero undocumented plug "
        "rows: every movement category is individually sourced (including easy-to-skip items - the FY2021 fair "
        "value/tax-on-OCI movements and the FY2025 AT1 issuance) and each closing balance ties exactly to both "
        "the next period's opening balance and to that year's own Balance Sheet Total equity.\n\n"
        + STATEMENTS_ENTITY_NOTE
    ),
    source_height=220,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Cash (used in)/generated from operations", {"FY2025": 15.5, "FY2024": 460.8, "FY2023": -494.1, "FY2022": 75.2, "FY2021": 212.9}),
    ("DATA", "Funding costs paid", {"FY2023": -33.8, "FY2022": -10.9, "FY2021": -25.9}),
    ("DATA", "Tax paid", {"FY2023": -6.1, "FY2022": -13.4, "FY2021": -6.1}),
    ("DATA", "Tax received", {"FY2025": 4.1, "FY2024": 8.2}),
    ("TOTAL", "Net cash (used in)/generated from operating activities", {"FY2025": 19.6, "FY2024": 469.0, "FY2023": -534.0, "FY2022": 50.9, "FY2021": 180.9}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property and equipment", {"FY2025": -1.4, "FY2024": -1.2, "FY2023": -1.9, "FY2022": -2.5, "FY2021": -0.7}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -14.6, "FY2024": -11.6, "FY2023": -12.5, "FY2022": -19.2, "FY2021": -16.9}),
    ("DATA", "Purchase of investment securities", {"FY2025": -291.8}),
    ("DATA", "Proceeds from maturity of investment securities", {"FY2025": 40.0}),
    ("DATA", "Proceeds from sale of investments", {"FY2024": 4.3, "FY2023": 6.4}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -267.8, "FY2024": -8.5, "FY2023": -8.0, "FY2022": -21.7, "FY2021": -17.6}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payment/capital elements of lease liabilities", {"FY2025": -6.8, "FY2024": -5.5, "FY2023": -6.0, "FY2022": -6.1, "FY2021": -6.1}),
    ("DATA", "Financing of loan to related party", {"FY2025": -163.0, "FY2024": -140.0}),
    ("DATA", "Repayment of loan to related party", {"FY2025": 183.9, "FY2024": 158.9}),
    ("DATA", "Proceeds from borrowings", {"FY2024": 5.0, "FY2023": 1100.0, "FY2022": 330.0, "FY2021": 295.8}),
    ("DATA", "Repayment of borrowings", {"FY2025": -5.0, "FY2024": -174.0, "FY2023": -284.8, "FY2022": -258.4, "FY2021": -788.2}),
    ("DATA", "Proceeds of issuance of other equity instruments", {"FY2025": 59.9}),
    ("DATA", "Dividends paid to company shareholder", {"FY2025": -20.0, "FY2024": -40.0, "FY2022": -95.1, "FY2021": -85.0}),
    ("TOTAL", "Net cash generated/(used in) financing activities", {"FY2025": 49.0, "FY2024": -195.6, "FY2023": 809.1, "FY2022": -29.6, "FY2021": -583.5}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -199.2, "FY2024": 264.9, "FY2023": 267.1, "FY2022": -0.4, "FY2021": -420.2}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 945.0, "FY2024": 680.1, "FY2023": 413.0, "FY2022": 413.4, "FY2021": 833.6}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 745.8, "FY2024": 945.0, "FY2023": 680.1, "FY2022": 413.0, "FY2021": 413.4}),
]

bw.add_cash_flow_sheet(
    title="Vanquis Bank Limited — Cash Flow Statement",
    subtitle="Vanquis Bank Limited (Company) basis, £m. See source note at bottom re: basis mismatch with Pillar 3 sheets.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=260,
    unit_suffix=" (£m)",
)

bw.add_asset_quality_sheet(
    title="Vanquis Bank Limited — Asset Quality",
    subtitle="Vanquis Bank Limited (Company) basis, £m. IFRS 9 stage split shown on Credit Cards (largest, most consistently disclosed product) except FY2021 (whole book).",
    rows=[
        ("SECTION", "Gross receivables by product", {}),
        ("DATA", "Credit Cards (gross)", {"FY2025": 1553.8, "FY2024": 1309.9, "FY2023": 1476.4, "FY2022": 1452.0}),
        ("DATA", "Personal Loans (gross)", {"FY2023": 117.5, "FY2022": 85.5}),
        ("DATA", "Second Charge Mortgages (gross)", {"FY2025": 619.4, "FY2024": 225.5, "FY2023": 2.8}),
        ("DATA", "Whole book (gross, FY2021 - not split by product that year)", {"FY2021": 1451.0}),
        ("TOTAL", "Gross amounts receivable from customers (continuing operations)", {"FY2025": 2173.2, "FY2024": 1535.4, "FY2023": 1596.7, "FY2022": 1537.5, "FY2021": 1451.0}),
        ("SECTION", "Allowance account by product", {}),
        ("DATA", "Credit Cards allowance", {"FY2025": -169.5, "FY2024": -160.0, "FY2023": -198.7, "FY2022": -270.4}),
        ("DATA", "Personal Loans allowance", {"FY2023": -15.1, "FY2022": -9.2}),
        ("DATA", "Second Charge Mortgages allowance", {"FY2025": -0.9, "FY2024": -0.2}),
        ("DATA", "Whole book allowance (FY2021 - not split by product that year)", {"FY2021": -359.5}),
        ("TOTAL", "Allowance account (continuing operations)", {"FY2025": -170.4, "FY2024": -160.2, "FY2023": -213.8, "FY2022": -279.6, "FY2021": -359.5}),
        ("TOTAL", "Net amounts receivable from customers (continuing operations)", {"FY2025": 2002.8, "FY2024": 1375.2, "FY2023": 1382.9, "FY2022": 1257.9, "FY2021": 1091.5}),
        ("DATA", "Fair value adjustment for portfolio hedged risk (Second Charge Mortgages)", {"FY2025": 0.4}),
        ("DATA", "Discontinued operations (Personal Loans, sold March 2025)", {"FY2024": 44.0}),
        ("TOTAL", "Reported amounts receivable from customers (per Balance Sheet)", {"FY2025": 2003.2, "FY2024": 1419.2, "FY2023": 1382.9, "FY2022": 1257.9, "FY2021": 1091.5}),
        ("SECTION", "Credit quality by IFRS 9 stage", {}),
        ("DATA", "Stage 1 (gross)", {"FY2025": 1351.5, "FY2024": 1136.6, "FY2023": 1200.8, "FY2022": 1116.6, "FY2021": 913.7}),
        ("DATA", "Stage 2 (gross)", {"FY2025": 139.1, "FY2024": 99.8, "FY2023": 161.4, "FY2022": 148.7, "FY2021": 342.8}),
        ("DATA", "Stage 3 / non-performing (gross)", {"FY2025": 63.2, "FY2024": 73.5, "FY2023": 114.2, "FY2022": 186.7, "FY2021": 194.5}),
        ("TOTAL", "Total gross (Credit Cards; FY2021 whole book)", {"FY2025": 1553.8, "FY2024": 1309.9, "FY2023": 1476.4, "FY2022": 1452.0, "FY2021": 1451.0}),
        ("DATA", "Stage 3 as % of gross - NPL ratio (derived)", {"FY2025": "4.07%", "FY2024": "5.61%", "FY2023": "7.74%", "FY2022": "12.86%", "FY2021": "13.40%"}),
        ("DATA", "Coverage ratio - allowance / gross (derived)", {"FY2025": "10.91%", "FY2024": "12.21%", "FY2023": "13.46%", "FY2022": "18.62%", "FY2021": "24.78%"}),
    ],
    sources_text=(
        "Sources - Vanquis Bank Limited's own (Company) Note 'Amounts receivable from customers', £m:\n"
        f"FY2025 & FY2024: Annual Report and Financial Statements, year ended 31 December 2025, note 12, p.56-60 "
        f"- {AR2025_URL}\n"
        f"FY2023 & FY2022: Annual Report and Financial Statements, year ended 31 December 2023 (Companies House "
        f"filing, 18 Apr 2024), note 11, p.53-58 - {AR2023_URL}\n"
        f"FY2021: Annual Report and Financial Statements, year ended 31 December 2021, note 10, p.79-80 - "
        f"{AR2021_URL}\n"
        "Note: FY2021's own note discloses only a combined (whole-book) gross/allowance/stage split, not broken "
        "out by product - Credit Cards/Personal Loans product-level figures only start from FY2022's report. "
        "Personal Loans was sold in March 2025 (presented as a discontinued operation in the FY2025 Annual "
        "Report) and is not stage-split in FY2024/FY2025's own disclosures (shown only as a lump-sum discontinued "
        "figure). The IFRS 9 stage split shown here is Credit Cards only for FY2022-FY2025 (the largest, most "
        "consistently disclosed product across all years) rather than the whole book - NOT a like-for-like basis "
        "with FY2021's whole-book split, documented rather than blended. NPL and coverage ratios are derived here "
        "(Stage 3 gross / Total gross; Allowance / Total gross) - not printed as ratios in the source documents.\n\n"
        + STATEMENTS_ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=240,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Vanquis Banking Group consolidated basis, {unit}" if unit else "Vanquis Banking Group consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=120)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 341.3, "FY2024": 344.3, "FY2023": 409.0, "FY2022": 478.8, "FY2021": 506.5})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22 (Appendix 1 - Own funds disclosures)", P3_2021_URL, "28"),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "16.5%", "FY2024": "18.8%", "FY2023": "20.5%", "FY2022": "26.4%", "FY2021": "29.1%"})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28"),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 400.0, "FY2024": 344.3, "FY2023": 409.0, "FY2022": 478.8, "FY2021": 506.5})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28"),
    note="FY2025 is the first year Tier 1 capital exceeds CET1 - the Group issued £59.9m of other (AT1) equity "
         "instruments during 2025 (see Cash Flow Statement sheet, financing activities). All other years shown have "
         "no Additional Tier 1 capital, so Tier 1 = CET1 exactly.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "19.3%", "FY2024": "18.8%", "FY2023": "20.5%", "FY2022": "26.4%", "FY2021": "29.1%"})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28"),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 541.5, "FY2024": 544.3, "FY2023": 609.0, "FY2022": 678.8, "FY2021": 706.5})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28"),
    note="DATA QUALITY NOTE: the FY2024 Pillar 3 Disclosures document's own comparative column for 31 Dec 2023 "
         "prints a 'Total capital' amount (£393.4m) that is inconsistent with that same document's own 31 Dec 2023 "
         "Total capital RATIO (30.0%) and RWA (£1,975.6m) - 30.0% x 1,975.6 implies Total capital of ~£592.7m, not "
         "£393.4m (and £393.4m simply repeats that column's CET1 figure, i.e. as if Tier 2 capital were zero, which "
         "contradicts row UK 7c showing a non-zero Additional T2 SREP requirement). The figures used here for FY2023 "
         "instead come from the FY2023 Pillar 3 Disclosures document's OWN as-originally-reported 31 Dec 2023 "
         "column (£609.0m), which is internally consistent (609.0 / 1,990.6 = 30.6%, matching its own stated ratio "
         "exactly) - this is also why FY2023's RWA here (£1,990.6m) differs slightly from the restated £1,975.6m "
         "shown as a comparative in the FY2024 document (a legitimate restatement, per that document's own footnote, "
         "for a Vehicle Finance Stage 3 ECL review - unrelated to the Total capital error).",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "26.1%", "FY2024": "29.7%", "FY2023": "30.6%", "FY2022": "37.5%", "FY2021": "40.6%"})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28"),
    note="See the Total Capital sheet's DATA QUALITY NOTE - this ratio row is unaffected (it is directly stated in "
         "each document, not derived from the erroneous amount), but is included here for context.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 2073.2, "FY2024": 1834.8, "FY2023": 1990.6, "FY2022": 1810.8, "FY2021": 1740.6})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28"),
    note="FY2023 (£1,990.6m) is as originally reported in the FY2023 Pillar 3 Disclosures; the FY2024 document later "
         "restated the 31 Dec 2023 comparative to £1,975.6m following a Vehicle Finance Stage 3 ECL methodology "
         "review - both figures are genuine, just on slightly different bases (see Total Capital sheet note).",
)

bw.add_rwa_breakdown_sheet(
    title="Vanquis Bank Limited — RWA Breakdown",
    subtitle="Vanquis Banking Group plc consolidated basis, £m (see entity note - same basis mismatch as the other Pillar 3 sheets).",
    rows=[
        ("DATA", "Credit risk (excluding CCR)", {"FY2025": 1931.5, "FY2024": 1696.8, "FY2023": 1848.8, "FY2022": 1656.5, "FY2021": 1595.0}),
        ("DATA", "Counterparty credit risk (CCR, incl. CVA)", {"FY2025": 3.0, "FY2024": 3.8, "FY2023": 10.6, "FY2022": 23.0, "FY2021": 4.1}),
        ("DATA", "Securitisation exposures", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0}),
        ("DATA", "Market risk", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("DATA", "Operational risk", {"FY2025": 138.7, "FY2024": 134.2, "FY2023": 131.2, "FY2022": 131.3, "FY2021": 141.5}),
        ("DATA", "Amounts below thresholds for deduction (memo, not summed into Total)", {"FY2025": 40.2, "FY2024": 46.5, "FY2023": 49.8, "FY2022": 29.4}),
        ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 2073.2, "FY2024": 1834.8, "FY2023": 1990.6, "FY2022": 1810.8, "FY2021": 1740.6}),
    ],
    sources_text=(
        "Sources - Vanquis Banking Group plc (consolidated) Pillar 3 UK OV1 disclosure, £m:\n"
        f"FY2025 & FY2024: Pillar 3 Disclosures 31 Dec 2025, UK OV1 table, p.8 - {P3_2025_URL}\n"
        f"FY2023 & FY2022: Pillar 3 Disclosures 2023, UK OV1 table (section 2.1), p.4 - {P3_2023_URL}\n"
        f"FY2021: Provident Financial plc Pillar 3 Disclosures 2021, Table 8 (5.3 Pillar 1 minimum requirement), "
        f"p.10 - {P3_2021_URL}\n"
        "Note: FY2021 predates the UK OV1 template (introduced from FY2022) - Provident Financial plc's own "
        "older CRR-era Table 8 groups risk categories slightly differently ('Credit risk (excluding CCR)', "
        "'Counterparty credit risk (CCR)', 'Operational risk', 'Market risk') but sums to the same Total RWEA "
        "(£1,740.6m) already on file on the Total RWAs sheet; no 'amounts below thresholds' memo line exists in "
        "that year's table. FY2025's/FY2024's/FY2023's/FY2022's category rows sum exactly to Total RWAs; the "
        "'amounts below thresholds for deduction' row is an informational memo per the source template's own "
        "footnote and is correctly excluded from the sum.\n\n"
        + ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=220,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure", {"FY2025": 3299.2, "FY2024": 2482.6, "FY2023": 2489.5, "FY2022": 2284.8, "FY2021": 2798.0}),
        ("Leverage ratio (%)", {"FY2025": "12.1%", "FY2024": "13.9%", "FY2023": "16.4%", "FY2022": "21.0%", "FY2021": "18.1%"}),
    ],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 6 (Leverage ratio)", P3_2021_URL, "9"),
    note="FY2022 onward use the UK KM1 template's 'leverage ratio excluding claims on central banks' basis. FY2021 "
         "predates that template and is calculated per CRR Article 429 instead (Table 6 of the 2021 Pillar 3 "
         "report) - a different, not directly comparable methodology, shown on its own basis rather than blended.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA) / liquidity buffer", {"FY2025": 930.0, "FY2024": 802.0, "FY2023": 512.0, "FY2022": 383.2, "FY2021": 439}),
        ("Total net cash outflows (adjusted value)", {"FY2025": 249.4, "FY2024": 116.4, "FY2023": 74.7, "FY2022": 48.0, "FY2021": 21}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "391.6%", "FY2024": "1,001.2%", "FY2023": "847.1%", "FY2022": "986.2%", "FY2021": "2,073%"}),
    ],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5", "6") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4", "5") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 20 (10.2.1 Liquidity coverage ratio)", P3_2021_URL, "24"),
    note="FY2022 onward use the UK KM1 template (12-month rolling average of month-end positions). FY2021 predates "
         "that template - its figures are the 31 December 2021 quarter's own values (£439m liquidity buffer, £21m "
         "net cash outflows, 2,073% LCR) from the pre-onshoring quarterly disclosure format, not a 12-month average.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2023": 2611.7, "FY2022": 2198.0}),
        ("Total required stable funding", {"FY2023": 1828.1, "FY2022": 1565.7}),
        ("NSFR ratio (%)", {"FY2025": "Not required", "FY2024": "Not required", "FY2023": "142.8%", "FY2022": "140.4%", "FY2021": "Not required"}),
    ],
    p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4", "5") + "\n"
    + p3_sources("FY2024/FY2025 and FY2021 basis note", P3_2024_URL, "6"),
    note="Not required for FY2021 (NSFR only became binding in the UK from 1 January 2022). Not required from the "
         "30 June 2024 reporting date onward: in March 2024 the Group was confirmed as a Small Domestic Deposit "
         "Taker consolidation entity, exempting it from NSFR reporting - so no FY2024 or FY2025 figures exist "
         "either, despite falling in the middle of the window where NSFR was otherwise required.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not applicable" for y in YEARS})],
    p3_sources("All years: Pillar 3 Disclosures 2021-2025 (no MREL section in any edition)", P3_2025_URL, "n/a"),
    note="No MREL disclosure of any kind (numeric or qualitative) appears in any Pillar 3 Disclosures document "
         "reviewed, FY2021-FY2025 - consistent with Vanquis Banking Group not being a resolution entity subject to "
         "a standalone MREL requirement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 3574.0, "FY2024": 2907.4, "FY2023": 2609.5, "FY2022": 1867.4, "FY2021": 1700.3}),
        ("Amounts receivable from customers", {"FY2025": 2003.2, "FY2024": 1419.2, "FY2023": 1382.9, "FY2022": 1257.9, "FY2021": 1091.5}),
        ("Retail deposits", {"FY2025": 3019.9, "FY2024": 2428.1, "FY2023": 1950.5, "FY2022": 1100.6, "FY2021": 1018.6}),
        ("Total equity", {"FY2025": 438.0, "FY2024": 361.7, "FY2023": 393.7, "FY2022": 385.0, "FY2021": 385.3}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 374.3, "FY2024": 366.3, "FY2023": 385.4, "FY2022": 375.4}),
        ("Impairment charges", {"FY2025": -139.2, "FY2024": -124.7, "FY2023": -150.9, "FY2022": -25.3, "FY2021": -5.9}),
        ("Operating costs", {"FY2025": -190.6, "FY2024": -236.6, "FY2023": -223.4, "FY2022": -219.7, "FY2021": -195.6}),
        ("Profit for the year", {"FY2025": 35.7, "FY2024": 7.5, "FY2023": 7.6, "FY2022": 93.8, "FY2021": 146.0}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 361.7, "FY2024": 393.7, "FY2023": 385.0, "FY2022": 385.3, "FY2021": 327.1}),
        ("Total comprehensive income for the year", {"FY2025": 35.7, "FY2024": 7.5, "FY2023": 7.6, "FY2022": 93.8, "FY2021": 142.1}),
        ("Other equity movements, net", {"FY2025": 40.6, "FY2024": -39.5, "FY2023": 1.1, "FY2022": -94.1, "FY2021": -83.9}),
        ("Closing equity", {"FY2025": 438.0, "FY2024": 361.7, "FY2023": 393.7, "FY2022": 385.0, "FY2021": 385.3}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 19.6, "FY2024": 469.0, "FY2023": -534.0, "FY2022": 50.9, "FY2021": 180.9}),
        ("Net cash from/(used in) investing activities", {"FY2025": -267.8, "FY2024": -8.5, "FY2023": -8.0, "FY2022": -21.7, "FY2021": -17.6}),
        ("Net cash from/(used in) financing activities", {"FY2025": 49.0, "FY2024": -195.6, "FY2023": 809.1, "FY2022": -29.6, "FY2021": -583.5}),
        ("Cash and cash equivalents at end of year", {"FY2025": 745.8, "FY2024": 945.0, "FY2023": 680.1, "FY2022": 413.0, "FY2021": 413.4}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.5%", "FY2024": "18.8%", "FY2023": "20.5%", "FY2022": "26.4%", "FY2021": "29.1%"}),
        ("Tier 1 Ratio", {"FY2025": "19.3%", "FY2024": "18.8%", "FY2023": "20.5%", "FY2022": "26.4%", "FY2021": "29.1%"}),
        ("Total Capital Ratio", {"FY2025": "26.1%", "FY2024": "29.7%", "FY2023": "30.6%", "FY2022": "37.5%", "FY2021": "40.6%"}),
        ("Leverage Ratio", {"FY2025": "12.1%", "FY2024": "13.9%", "FY2023": "16.4%", "FY2022": "21.0%", "FY2021": "18.1%"}),
        ("LCR", {"FY2025": "391.6%", "FY2024": "1,001.2%", "FY2023": "847.1%", "FY2022": "986.2%", "FY2021": "2,073%"}),
        ("NSFR", {"FY2023": "142.8%", "FY2022": "140.4%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. IMPORTANT: the Cash Flow Summary above is Vanquis Bank "
         "Limited's own entity-level (Company) basis, but the Pillar 3 Key Metrics below are Vanquis Banking Group "
         "plc consolidated basis (Bank + Moneybarn No.1 Limited) - Vanquis does not publish a Bank-only Pillar 3 "
         "breakdown. See the Cash Flow Statement sheet's entity note for detail.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/VANQUIS FINANCIALS.xlsx")
