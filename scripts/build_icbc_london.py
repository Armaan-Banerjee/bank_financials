import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR25_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2025/ICBCReport2025.pdf"
AR24_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2024/ICBCReport2024.pdf"
AR23_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzQyNDQ0NTU5OWFkaXF6a2N4/document?format=pdf&download=0"
AR22_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzM4MTkxOTA4OGFkaXF6a2N4/document?format=pdf&download=0"
AR21_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzM0MDgwMDM4MGFkaXF6a2N4/document?format=pdf&download=0"

P3_25_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2025/2025_pillar_3_disclosure.pdf"
P3_24_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2024/2024_pillar_3_disclosure.pdf"

CASH_FLOW_SOURCES = (
    "Sources — all figures are ICBC (London) plc Statement of Cash Flows, $'000:\n"
    f"FY2025 & FY2024: ICBC (London) plc Annual Report and Financial Statements 2025, p.27 (Statement of Cash Flows) — {AR25_URL}\n"
    f"FY2024 comparative cross-checked against ICBC (London) plc Annual Report 2024, p.29 (Statement of Cash flows) — {AR24_URL}\n"
    f"FY2023: ICBC (London) plc Annual Report and Financial Statements 2023 (Companies House filing, full accounts), p.30 (Statement of Cash flows) — {AR23_URL}\n"
    f"FY2022: ICBC (London) plc Annual Report and Financial Statements 2022 (Companies House filing, full accounts), p.28 (Statement of Cash flows) — {AR22_URL}\n"
    f"FY2021: ICBC (London) plc Annual Report and Financial Statements 2021 (Companies House filing, full accounts), p.30 (Statement of Cash flows) — {AR21_URL}\n"
    "Note: the FY2021-2023 Companies House filings are scanned (image-only) documents; those years' figures were "
    "transcribed from page renders. All five years cross-reconcile exactly year-on-year (each year's closing cash and "
    "cash equivalents equals the following year's opening balance). 'Gain on sale of financial investments at FVOCI' "
    "was not a separate line in the FY2022/FY2023 statements (folded into the exchange gain/amortisation line); blank "
    "cells indicate that year's statement did not disclose that specific line. The source document's own labels "
    "('Net decrease in cash and cash equivalents', 'Net cash used in operating activities') are reproduced verbatim "
    "even in years where the reported figure is positive."
)

def p3_sources(note_disclosure_start=True):
    text = (
        "Sources — ICBC (London) plc (solo basis), Annex 2 — UK KM1 - Key metric template:\n"
        f"FY2025: ICBC (London) plc Pillar 3 Disclosures 2025, p.13-14 (31/12/2025 column) — {P3_25_URL}\n"
        f"FY2024: ICBC (London) plc Pillar 3 Disclosures 2024, p.12-13 (31/12/2024 column) — {P3_24_URL}\n"
        f"FY2023: ICBC (London) plc Pillar 3 Disclosures 2024, p.12-13 (31/12/2023 comparative column, the only "
        f"public source for this year) — {P3_24_URL}"
    )
    if note_disclosure_start:
        text += (
            "\nNote: ICBC (London) plc's Pillar 3 disclosures are only publicly available from FY2024 onward (the "
            "2025 document's own comparative columns reach back to 31/12/2024; the 2024 document's comparative "
            "columns reach back to 31/12/2023). No FY2022 or FY2021 Pillar 3 disclosure document exists on the "
            "bank's site. The FY2024 RWA/ratio figures used here are taken from the FY2024 disclosure's own current-"
            "period column rather than the FY2025 disclosure's restated comparative column, which shows a slightly "
            "different RWA (715,739.38 vs. 719,040.48) and CET1/Tier1/Total capital ratio (70.48% vs. 70.16%) for "
            "the same date despite an identical capital figure — both are the bank's own official disclosures."
        )
    return text

P3_23_KM1_NOTE = (
    " (KM1 comparative column only - the OV1 category-level RWA breakdown "
    "table is not available for FY2023 or earlier, only the aggregate Total "
    "RWA figure)"
)

STATEMENTS_SOURCES = (
    "Sources — all figures are ICBC (London) plc Balance Sheet / Profit and Loss "
    "Account / Statement of Changes in Equity, $'000, as originally published in "
    "each year's own Annual Report (each year's own primary presentation, not a "
    "later restated comparative, except where noted):\n"
    f"FY2025 & FY2024: ICBC (London) plc Annual Report and Financial Statements 2025, "
    f"pp.23-26 (Profit and Loss Account, Statement of Comprehensive Income, Balance "
    f"Sheet, Statement of Changes in Equity) — {AR25_URL}\n"
    f"FY2023: ICBC (London) plc Annual Report and Financial Statements 2024, pp.25-28 "
    f"(2023 comparative column) — {AR24_URL}. Cross-checked against ICBC (London) plc "
    f"Annual Report and Financial Statements 2023 (Companies House filing), pp.26-29 "
    f"(own originally-published figures) — {AR23_URL}. Both sources agree exactly.\n"
    f"FY2022: ICBC (London) plc Annual Report and Financial Statements 2023 (Companies "
    f"House filing), pp.26-29 (2022 comparative column) — {AR23_URL}\n"
    f"FY2021: ICBC (London) plc Annual Report and Financial Statements 2022 (Companies "
    f"House filing), pp.24-27 (2021 comparative column) — {AR22_URL}\n"
    "Note: the FY2021-2023 Companies House filings are scanned (image-only) documents; "
    "those years' figures were transcribed from page renders. The Statement of Changes "
    "in Equity reconciles exactly at every year boundary (each year's own closing "
    "Total shareholder's funds equals the next year's own opening balance and that "
    "year's own Balance Sheet Total Share Capital and Reserves) - no plug rows were "
    "needed anywhere. 'Reimbursement of expenses attributable to the Branch' offsets "
    "operating expenses recharged to the Bank's own overseas Branch operation - a "
    "genuine feature of this entity's cost structure, not a data error."
)

ASSET_QUALITY_SOURCES = (
    "Sources — ICBC (London) plc, Loans and advances to customers, $'000, IFRS 9 "
    "stage-1/2/3 impairment allowance breakdown:\n"
    f"FY2025: Annual Report 2025, Note 11(i) — {AR25_URL}\n"
    f"FY2024: Annual Report 2025, Note 11(i) (2024 comparative) — {AR25_URL}. Cross-"
    f"checked against Annual Report 2024, Note 11(i) — {AR24_URL}\n"
    f"FY2023: Annual Report 2024, Note 11(i) (2023 comparative) — {AR24_URL}\n"
    f"FY2022: Annual Report 2023 (Companies House filing), Note 11(i) — {AR23_URL}\n"
    f"FY2021: Annual Report 2022 (Companies House filing), Note 11(i) — {AR22_URL}\n"
    "Gross carrying amount and net carrying amount for Loans and advances to customers "
    "sourced from each year's own Note 10 (or comparative column); confirmed by reading "
    "Note 11 in full for every year that the Bank's entire loans-and-advances-to-"
    "customers book sits in IFRS 9 Stage 1 throughout FY2021-FY2025 - no Stage 2 or "
    "Stage 3 balance has existed at any year-end in this range (a genuine feature of "
    "this book, not an omission - Stage 2 exposure of $4,594k did exist at the opening "
    "of FY2021 per the Bank's own comparative disclosure, but had cleared to nil by "
    "31 December 2021, before this workbook's coverage begins). Loans and advances to "
    "banks (inter-bank placements) are kept separate from the customer loan book above "
    "and are not included in this sheet's coverage or ratios, consistent with how "
    "other banks in this project separate Inter-Group/interbank placements from "
    "customer-facing credit risk."
)

def rwa_sources():
    return (
        "Sources — ICBC (London) plc (solo basis), Annex 1 — UK OV1 template (Overview "
        "of risk weighted exposure amounts), $'000:\n"
        f"FY2025: ICBC (London) plc Pillar 3 Disclosures 2025, p.14-15 (31/12/2025 "
        f"column) — {P3_25_URL}\n"
        f"FY2024: ICBC (London) plc Pillar 3 Disclosures 2024, p.15-16 (31/12/2024 "
        f"column) — {P3_24_URL}\n"
        "Note: the OV1 category-level RWA breakdown table is only publicly available "
        "from FY2024 onward (same disclosure-start limitation as the other Pillar 3 "
        "sheets in this workbook - see the CET1/Tier 1/etc. sheets' own source note). "
        "No FY2023, FY2022 or FY2021 OV1 table exists; only the aggregate Total RWA "
        "figure for those years is disclosed (in the KM1 template, see the Total RWAs "
        "sheet), not a category-level split. FY2025's OV1 Total ($675,423.74k) and "
        "FY2024's OV1 Total ($719,040.48k, matching the Total RWAs sheet's disclosed "
        "figure exactly) both come from the Bank's own Pillar 3 documents; FY2025's OV1 "
        "Total differs slightly ($675,423.74k vs. $675,668k) from the Total RWAs sheet's "
        "KM1-sourced figure for the same date - both are the Bank's own official "
        "disclosures, reproduced as reported rather than force-reconciled."
    )

bw = BankWorkbook(bank_name="ICBC (London) plc", years=YEARS, header_color="2E5395")

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 1062471, "FY2024": 43857, "FY2023": 196360, "FY2022": 107136, "FY2021": 149090}),
    ("DATA", "Loans and advances to banks", {"FY2025": 511222, "FY2024": 934969, "FY2023": 523491, "FY2022": 612456, "FY2021": 537966}),
    ("DATA", "Loans and advances to customers", {"FY2025": 413326, "FY2024": 336256, "FY2023": 429281, "FY2022": 331484, "FY2021": 128348}),
    ("DATA", "Derivative financial instruments", {"FY2025": 0, "FY2024": 255, "FY2023": 66, "FY2022": 0, "FY2021": 21}),
    ("DATA", "Financial investments at FVOCI", {"FY2025": 320996, "FY2024": 313176, "FY2023": 251961, "FY2022": 263048, "FY2021": 350258}),
    ("DATA", "Financial investments at amortised cost", {"FY2025": 35803, "FY2024": 27177, "FY2023": 68805, "FY2022": 175266, "FY2021": 209357}),
    ("DATA", "Intangible assets", {"FY2025": 244, "FY2024": 220, "FY2023": 186, "FY2022": 162, "FY2021": 167}),
    ("DATA", "Tangible fixed assets", {"FY2025": 29460, "FY2024": 29928, "FY2023": 30669, "FY2022": 31651, "FY2021": 32585}),
    ("DATA", "Current tax assets", {"FY2022": 0, "FY2021": 28}),
    ("DATA", "Deferred tax assets", {"FY2025": 614, "FY2024": 614, "FY2023": 569, "FY2022": 3489}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 19810, "FY2024": 15677, "FY2023": 13332, "FY2022": 13447, "FY2021": 12868}),
    ("TOTAL", "Total Assets", {"FY2025": 2393946, "FY2024": 1702129, "FY2023": 1514720, "FY2022": 1538139, "FY2021": 1420688}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 1622117, "FY2024": 974702, "FY2023": 751531, "FY2022": 810645, "FY2021": 411211}),
    ("DATA", "Customer accounts", {"FY2025": 160911, "FY2024": 165625, "FY2023": 244297, "FY2022": 247933, "FY2021": 530469}),
    ("DATA", "Derivative financial instruments", {"FY2025": 2245, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 117}),
    ("DATA", "Other liabilities", {"FY2025": 12447, "FY2024": 10872, "FY2023": 11801, "FY2022": 8101, "FY2021": 8054}),
    ("DATA", "Accruals and deferred income", {"FY2025": 1924, "FY2024": 3121, "FY2023": 5343, "FY2022": 2751, "FY2021": 476}),
    ("DATA", "Provisions for liabilities", {"FY2022": 0, "FY2021": 1915}),
    ("DATA", "Current tax liabilities", {"FY2025": 27, "FY2024": 1705, "FY2023": 718, "FY2022": 830, "FY2021": 0}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 2859, "FY2024": 1454, "FY2023": 0, "FY2022": 0, "FY2021": 848}),
    ("TOTAL", "Total Liabilities", {"FY2025": 1802530, "FY2024": 1157479, "FY2023": 1013690, "FY2022": 1070260, "FY2021": 953090}),
    ("SECTION", "Share Capital and Reserves", {}),
    ("DATA", "Called up share capital", {"FY2025": 200000, "FY2024": 200000, "FY2023": 200000, "FY2022": 200000, "FY2021": 200000}),
    ("DATA", "Retained earnings", {"FY2025": 389313, "FY2024": 346433, "FY2023": 306770, "FY2022": 280635, "FY2021": 269268}),
    ("DATA", "Other reserves", {"FY2025": 2103, "FY2024": -1783, "FY2023": -5740, "FY2022": -12756, "FY2021": -1670}),
    ("TOTAL", "Total Share Capital and Reserves", {"FY2025": 591416, "FY2024": 544650, "FY2023": 501030, "FY2022": 467879, "FY2021": 467598}),
    ("TOTAL", "Total Liabilities and Share Capital and Reserves", {"FY2025": 2393946, "FY2024": 1702129, "FY2023": 1514720, "FY2022": 1538139, "FY2021": 1420688}),
]

bw.add_balance_sheet_sheet(
    title="ICBC (London) plc — Balance Sheet",
    subtitle="Solo basis, $'000 unless stated",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=75,
    source_height=170,
    unit_suffix=" ($'000)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 73022, "FY2024": 80464, "FY2023": 64844, "FY2022": 27188, "FY2021": 19740}),
    ("DATA", "Interest payable", {"FY2025": -17005, "FY2024": -24461, "FY2023": -28971, "FY2022": -8992, "FY2021": -4294}),
    ("TOTAL", "Net interest income", {"FY2025": 56017, "FY2024": 56003, "FY2023": 35873, "FY2022": 18196, "FY2021": 15446}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 2656, "FY2024": 2516, "FY2023": 1671, "FY2022": 1234, "FY2021": 1629}),
    ("DATA", "Fees and commissions payable", {"FY2025": -360, "FY2024": -403, "FY2023": -371, "FY2022": -369, "FY2021": -394}),
    ("TOTAL", "Net fees and commissions", {"FY2025": 2296, "FY2024": 2113, "FY2023": 1300, "FY2022": 865, "FY2021": 1235}),
    ("DATA", "Dealing (loss)/profit", {"FY2025": 709, "FY2024": 515, "FY2023": 375, "FY2022": -365, "FY2021": 422}),
    ("DATA", "Other operating income", {"FY2025": 9798, "FY2024": 6773, "FY2023": 5844, "FY2022": 6583, "FY2021": 6118}),
    ("TOTAL", "Other income", {"FY2025": 10507, "FY2024": 7288, "FY2023": 6219, "FY2022": 6218, "FY2021": 6540}),
    ("TOTAL", "Total operating income", {"FY2025": 68820, "FY2024": 65404, "FY2023": 43392, "FY2022": 25279, "FY2021": 23221}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -41255, "FY2024": -38325, "FY2023": -39301, "FY2022": -39373, "FY2021": -38201}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -1208, "FY2024": -1154, "FY2023": -1234, "FY2022": -1463, "FY2021": -1962}),
    ("DATA", "Other operating charges", {"FY2025": -10247, "FY2024": -10487, "FY2023": -9009, "FY2022": -7385, "FY2021": -8297}),
    ("DATA", "Reimbursement of expenses attributable to the Branch", {"FY2025": 41197, "FY2024": 39091, "FY2023": 39539, "FY2022": 38664, "FY2021": 38503}),
    ("TOTAL", "Operating expenses", {"FY2025": -11513, "FY2024": -10875, "FY2023": -10005, "FY2022": -10609, "FY2021": -3425}),
    ("DATA", "Impairment (losses)/releases", {"FY2025": -52, "FY2024": 312, "FY2023": 1180, "FY2022": -1052, "FY2021": 6532}),
    ("TOTAL", "Profit on ordinary activities before tax", {"FY2025": 57255, "FY2024": 54841, "FY2023": 34567, "FY2022": 14670, "FY2021": 19796}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": -14375, "FY2024": -15178, "FY2023": -8432, "FY2022": -3303, "FY2021": -4280}),
    ("TOTAL", "Profit for the financial year", {"FY2025": 42880, "FY2024": 39663, "FY2023": 26135, "FY2022": 11367, "FY2021": 15516}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Change in fair value of financial investments at FVOCI", {"FY2025": 5190, "FY2024": 5430, "FY2023": 10201, "FY2022": -15385, "FY2021": -5679}),
    ("DATA", "Impairment allowance on financial investments at FVOCI", {"FY2025": -7, "FY2024": -116, "FY2023": -88, "FY2022": 123, "FY2021": -416}),
    ("DATA", "Tax on components of other comprehensive income", {"FY2025": -1297, "FY2024": -1357, "FY2023": -3097, "FY2022": 4176, "FY2021": 1692}),
    ("TOTAL", "Other comprehensive income for the year, net of income tax", {"FY2025": 3886, "FY2024": 3957, "FY2023": 7016, "FY2022": -11086, "FY2021": -4403}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 46766, "FY2024": 43620, "FY2023": 33151, "FY2022": 281, "FY2021": 11113}),
]

bw.add_income_statement_sheet(
    title="ICBC (London) plc — Profit and Loss Account / Statement of Comprehensive Income",
    subtitle="Solo basis, $'000 unless stated",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=75,
    source_height=170,
    unit_suffix=" ($'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Retained earning", "Other reserves", "Total shareholder's funds"]

equity_rows = [
    ("DATA", "At 1 January 2021", (200000, 253752, 2733, 456485)),
    ("DATA", "Profit for the year", (None, 15516, None, 15516)),
    ("DATA", "Change in fair value of financial investments at FVOCI", (None, None, -5679, -5679)),
    ("DATA", "Impairment charged on financial investments at FVOCI", (None, None, -416, -416)),
    ("DATA", "Tax on other comprehensive income", (None, None, 1692, 1692)),
    ("TOTAL", "At 31 December 2021", (200000, 269268, -1670, 467598)),
    ("DATA", "At 1 January 2022 (= FY2021 closing)", (200000, 269268, -1670, 467598)),
    ("DATA", "Profit for the year", (None, 11367, None, 11367)),
    ("DATA", "Change in fair value of financial investments at FVOCI", (None, None, -15385, -15385)),
    ("DATA", "Impairment released on financial investments at FVOCI", (None, None, 123, 123)),
    ("DATA", "Deferred tax liability recognised through equity", (None, None, 4176, 4176)),
    ("TOTAL", "At 31 December 2022", (200000, 280635, -12756, 467879)),
    ("DATA", "At 1 January 2023 (= FY2022 closing)", (200000, 280635, -12756, 467879)),
    ("DATA", "Profit for the year", (None, 26135, None, 26135)),
    ("DATA", "Change in fair value of financial investments at FVOCI", (None, None, 10201, 10201)),
    ("DATA", "Impairment charged on financial investments at FVOCI", (None, None, -88, -88)),
    ("DATA", "Tax on other comprehensive income", (None, None, -3097, -3097)),
    ("TOTAL", "At 31 December 2023", (200000, 306770, -5740, 501030)),
    ("DATA", "At 1 January 2024 (= FY2023 closing)", (200000, 306770, -5740, 501030)),
    ("DATA", "Profit for the year", (None, 39663, None, 39663)),
    ("DATA", "Change in fair value of financial investments at FVOCI", (None, None, 5430, 5430)),
    ("DATA", "Impairment charged on financial investments at FVOCI", (None, None, -116, -116)),
    ("DATA", "Tax on other comprehensive income", (None, None, -1357, -1357)),
    ("TOTAL", "At 31 December 2024", (200000, 346433, -1783, 544650)),
    ("DATA", "At 1 January 2025 (= FY2024 closing)", (200000, 346433, -1783, 544650)),
    ("DATA", "Profit for the year", (None, 42880, None, 42880)),
    ("DATA", "Change in fair value of financial investments at FVOCI", (None, None, 5190, 5190)),
    ("DATA", "Impairment released on financial investments at FVOCI", (None, None, -7, -7)),
    ("DATA", "Tax on other comprehensive income", (None, None, -1297, -1297)),
    ("TOTAL", "At 31 December 2025", (200000, 389313, 2103, 591416)),
]

bw.add_equity_changes_sheet(
    title="ICBC (London) plc — Statement of Changes in Equity",
    subtitle="$'000 - chronological, oldest to newest. Equity reconciliation ladder confirmed: every year's own "
              "closing balance ties exactly to both the next year's own opening balance and that year's own "
              "Balance Sheet Total Share Capital and Reserves - zero plug rows needed anywhere.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit for the year to net cash flows from operating activities", {}),
    ("DATA", "Profit for the year", {"FY2025": 42880, "FY2024": 39663, "FY2023": 26135, "FY2022": 11367, "FY2021": 15516}),
    ("DATA", "Depreciation of tangible fixed assets", {"FY2025": 1106, "FY2024": 1073, "FY2023": 1070, "FY2022": 1301, "FY2021": 1819}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 102, "FY2024": 81, "FY2023": 164, "FY2022": 162, "FY2021": 143}),
    ("DATA", "Impairment losses", {"FY2025": 52, "FY2024": -312, "FY2023": -1180, "FY2022": 1052, "FY2021": -6532}),
    ("DATA", "Interest income", {"FY2025": -73022, "FY2024": -80464, "FY2023": -64844, "FY2022": -27188, "FY2021": -19740}),
    ("DATA", "Interest expense", {"FY2025": 17005, "FY2024": 24461, "FY2023": 28971, "FY2022": 8992, "FY2021": 4294}),
    ("DATA", "Gain on sale of financial investments at FVOCI", {"FY2025": -139, "FY2024": 0, "FY2021": 0}),
    ("DATA", "Exchange gain and accretion of discounts and amortisation of premiums on financial investments", {"FY2025": 4619, "FY2024": 7528, "FY2023": -4149, "FY2022": 21189, "FY2021": 555}),
    ("DATA", "Revaluation (gain)/loss on financial derivatives", {"FY2025": 2500, "FY2024": -189, "FY2023": -66, "FY2022": -96, "FY2021": -497}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": 14375, "FY2024": 15178, "FY2023": 8432, "FY2022": 3303, "FY2021": 4280}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Loans to banks", {"FY2025": 764198, "FY2024": -436287, "FY2023": 136996, "FY2022": -160146, "FY2021": 149827}),
    ("DATA", "Loans and advances to customers", {"FY2025": -77176, "FY2024": 93250, "FY2023": -97842, "FY2022": -203380, "FY2021": 305578}),
    ("DATA", "Financial investments at FVOCI", {"FY2025": 408, "FY2024": -60711, "FY2023": 17973, "FY2022": 66827, "FY2021": 46073}),
    ("DATA", "Financial investments at amortised cost", {"FY2025": -9488, "FY2024": 41729, "FY2023": 106936, "FY2022": 35881, "FY2021": -13036}),
    ("DATA", "Other assets", {"FY2025": -3319, "FY2024": -957, "FY2023": 1104, "FY2022": -720, "FY2021": 1762}),
    ("DATA", "Deposits by banks", {"FY2025": 647415, "FY2024": 223171, "FY2023": -59118, "FY2022": 399437, "FY2021": -699204}),
    ("DATA", "Deposits from customers", {"FY2025": -4714, "FY2024": -78671, "FY2023": -3639, "FY2022": -282533, "FY2021": 143585}),
    ("DATA", "Other liabilities", {"FY2025": 1613, "FY2024": -1030, "FY2023": 3697, "FY2022": -1865, "FY2021": 1733}),
    ("DATA", "Interest received", {"FY2025": 72209, "FY2024": 79076, "FY2023": 63856, "FY2022": 27330, "FY2021": 20462}),
    ("DATA", "Interest paid", {"FY2025": -18202, "FY2024": -26683, "FY2023": -26378, "FY2022": -6721, "FY2021": -5095}),
    ("DATA", "Income tax paid", {"FY2025": -15945, "FY2024": -14140, "FY2023": -8715, "FY2022": -2607, "FY2021": -3266}),
    ("TOTAL", "Net cash used in operating activities", {"FY2025": 1366477, "FY2024": -174234, "FY2023": 129403, "FY2022": -108415, "FY2021": -51743}),
    ("SECTION", "Cash flow from investing activities", {}),
    ("DATA", "Acquisition of tangible fixed assets", {"FY2025": -638, "FY2024": -332, "FY2023": -87, "FY2022": -367, "FY2021": -660}),
    ("DATA", "Acquisition of intangible assets", {"FY2025": -126, "FY2024": -115, "FY2023": -188, "FY2022": -158, "FY2021": -133}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -764, "FY2024": -447, "FY2023": -275, "FY2022": -525, "FY2021": -793}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Net decrease in cash and cash equivalents", {"FY2025": 1365713, "FY2024": -174681, "FY2023": 129128, "FY2022": -108940, "FY2021": -52536}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 139627, "FY2024": 316971, "FY2023": 180382, "FY2022": 307556, "FY2021": 361540}),
    ("DATA", "Effects of exchange rates on cash and cash equivalents", {"FY2025": -6647, "FY2024": -2663, "FY2023": 7461, "FY2022": -18234, "FY2021": -1448}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 1498693, "FY2024": 139627, "FY2023": 316971, "FY2022": 180382, "FY2021": 307556}),
]

bw.add_cash_flow_sheet(
    title="ICBC (London) plc — Statement of Cash Flows",
    subtitle="Solo basis, $'000 unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=75,
    source_height=140,
    unit_suffix=" ($'000)",
)

# ---------------------------------------------------------------
# Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by IFRS 9 stage", {}),
    ("DATA", "Gross carrying amount", {"FY2025": 413561, "FY2024": 336385, "FY2023": 429636, "FY2022": 331794, "FY2021": 128414}),
    ("DATA", "Stage 1 loss allowance", {"FY2025": -235, "FY2024": -129, "FY2023": -355, "FY2022": -310, "FY2021": -66}),
    ("DATA", "Stage 2 loss allowance", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Stage 3 loss allowance", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Net carrying amount", {"FY2025": 413326, "FY2024": 336256, "FY2023": 429281, "FY2022": 331484, "FY2021": 128348}),
    ("DATA", "Stage 1 coverage ratio (Stage 1 allowance / gross carrying amount)", {"FY2025": "0.06%", "FY2024": "0.04%", "FY2023": "0.08%", "FY2022": "0.09%", "FY2021": "0.05%"}),
    ("DATA", "Stage 2/3 (impaired) exposure as % of gross carrying amount", {"FY2025": "0.00%", "FY2024": "0.00%", "FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
]

bw.add_asset_quality_sheet(
    title="ICBC (London) plc — Asset Quality",
    subtitle="Loans and advances to customers, solo basis, $'000 unless stated",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=75,
    source_height=170,
    unit_suffix=" ($'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Solo basis, {unit}" if unit else "Solo basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=140)

metric(
    "CET1 Capital", "$'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 547878, "FY2024": 504454, "FY2023": 474459})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "$'000",
    [("Tier 1 capital", {"FY2025": 547878, "FY2024": 504454, "FY2023": 474459})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%"})],
    p3_sources(),
)

metric(
    "Total Capital", "$'000",
    [("Total capital", {"FY2025": 547878, "FY2024": 504454, "FY2023": 474459})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "$'000",
    [("Total risk-weighted exposure amount", {"FY2025": 675668, "FY2024": 719040, "FY2023": 842738})],
    p3_sources(),
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 590477.63, "FY2024": 660913.86}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 748.81, "FY2024": 294.72}),
    ("DATA", "Operational risk", {"FY2025": 84197.30, "FY2024": 57831.90}),
    ("TOTAL", "Total risk weighted exposure amount", {"FY2025": 675423.74, "FY2024": 719040.48}),
]

bw.add_rwa_breakdown_sheet(
    title="ICBC (London) plc — RWA Breakdown",
    subtitle="Solo basis, UK OV1 template, $'000",
    rows=rwa_breakdown_rows,
    sources_text=rwa_sources(),
    first_col_width=60,
    source_height=170,
    unit_suffix=" ($'000)",
)

metric(
    "Leverage Ratio", "$'000 / %",
    [
        ("Leverage ratio total exposure measure ($'000)", {"FY2025": 1153889, "FY2024": 1493767, "FY2023": 1339718}),
        ("Leverage ratio (%)", {"FY2025": "47.48%", "FY2024": "33.77%", "FY2023": "35.41%"}),
    ],
    p3_sources(),
)

metric(
    "LCR", "$'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value ($'000)", {"FY2025": 1374779, "FY2024": 328482, "FY2023": 384069}),
        ("Total net cash outflows, adjusted value ($'000)", {"FY2025": 956680, "FY2024": 187564, "FY2023": 136060}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "143.70%", "FY2024": "175.13%", "FY2023": "282.28%"}),
    ],
    p3_sources(),
    note="LCR figures are single month-end (31 December) spot observations as disclosed in the KM1 template, not a "
         "12-month trailing average.",
)

metric(
    "NSFR", "$'000 / %",
    [
        ("Total available stable funding ($'000)", {"FY2025": 581574, "FY2024": 608924, "FY2023": 694607}),
        ("Total required stable funding ($'000)", {"FY2025": 335509, "FY2024": 407762, "FY2023": 511527}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "173.34%", "FY2024": "149.33%", "FY2023": "135.79%"}),
    ],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(note_disclosure_start=False) + "\nMREL is not referenced anywhere in either available Pillar 3 disclosure document; "
    "ICBC (London) plc does not appear to be subject to a separate MREL requirement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total Assets", {"FY2025": 2393946, "FY2024": 1702129, "FY2023": 1514720, "FY2022": 1538139, "FY2021": 1420688}),
        ("Loans and advances to customers", {"FY2025": 413326, "FY2024": 336256, "FY2023": 429281, "FY2022": 331484, "FY2021": 128348}),
        ("Customer accounts", {"FY2025": 160911, "FY2024": 165625, "FY2023": 244297, "FY2022": 247933, "FY2021": 530469}),
        ("Total Share Capital and Reserves", {"FY2025": 591416, "FY2024": 544650, "FY2023": 501030, "FY2022": 467879, "FY2021": 467598}),
    ],
    balance_sheet_unit="$'000",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 68820, "FY2024": 65404, "FY2023": 43392, "FY2022": 25279, "FY2021": 23221}),
        ("Operating expenses", {"FY2025": -11513, "FY2024": -10875, "FY2023": -10005, "FY2022": -10609, "FY2021": -3425}),
        ("Profit for the financial year", {"FY2025": 42880, "FY2024": 39663, "FY2023": 26135, "FY2022": 11367, "FY2021": 15516}),
    ],
    income_statement_unit="$'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 544650, "FY2024": 501030, "FY2023": 467879, "FY2022": 467598, "FY2021": 456485}),
        ("Total comprehensive income for the year", {"FY2025": 46766, "FY2024": 43620, "FY2023": 33151, "FY2022": 281, "FY2021": 11113}),
        ("Closing equity", {"FY2025": 591416, "FY2024": 544650, "FY2023": 501030, "FY2022": 467879, "FY2021": 467598}),
    ],
    equity_changes_unit="$'000",
    cash_flow_totals=[
        ("Net cash used in operating activities", {"FY2025": 1366477, "FY2024": -174234, "FY2023": 129403, "FY2022": -108415, "FY2021": -51743}),
        ("Net cash used in investing activities", {"FY2025": -764, "FY2024": -447, "FY2023": -275, "FY2022": -525, "FY2021": -793}),
        ("Net cash from financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("Cash and cash equivalents at 31 December", {"FY2025": 1498693, "FY2024": 139627, "FY2023": 316971, "FY2022": 180382, "FY2021": 307556}),
    ],
    cash_flow_unit="$'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%"}),
        ("Tier 1 Ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%"}),
        ("Total Capital Ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%"}),
        ("Leverage Ratio", {"FY2025": "47.48%", "FY2024": "33.77%", "FY2023": "35.41%"}),
        ("LCR", {"FY2025": "143.70%", "FY2024": "175.13%", "FY2023": "282.28%"}),
        ("NSFR", {"FY2025": "173.34%", "FY2024": "149.33%", "FY2023": "135.79%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Pillar 3 ratios are only publicly disclosed from FY2023 onward "
         "(no FY2022/FY2021 Pillar 3 document exists); blank cells for those years are intentional, not zeros.",
)

bw.save("/Users/armaan/code/katalysis/banks/ICBC (LONDON) PLC FINANCIALS.xlsx")
