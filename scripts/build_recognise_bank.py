import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022"]
AR26_URL = "https://recognisebank.co.uk/wp-content/uploads/274107-Recognise-Bank-Annual-Report-WEB.pdf"
AR24_URL = "https://recognisebank.co.uk/wp-content/uploads/2024-Annual-Report-Accounts.pdf"
AR23_URL = "https://recognisebank.co.uk/wp-content/uploads/2023/10/230821-Recognise-Bank-2023-Annual-Report-WEB.pdf"
AR22_URL = "https://recognisebank.co.uk/wp-content/uploads/2023/10/2022-Annual-Report-Recognise-Bank-Limited.pdf"
P3_26_URL = "https://recognisebank.co.uk/wp-content/uploads/Pillar-3-disclosure-March-2026-RBL-v1.1-To-BAC-updated_-1-1.pdf"
P3_24_URL = "https://recognisebank.co.uk/wp-content/uploads/Pillar-3-disclosure-March-2024-RBL.pdf"
P3_23_URL = "http://web.archive.org/web/20231210004904/https://www.recognisebank.co.uk/wp-content/uploads/2023/10/Pillar-3-disclosures-March-2023-RBL.pdf"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Recognise Bank Limited (Companies House 10603119; FRN 849404; LEI "
    "213800ZFTXJC7RV9UQ92) is the matched authorised bank entity. Cash flows are presented on "
    "the Company/standalone basis in £'000 throughout. The 2022-2024 reports also show Group "
    "columns, but the Company column is used consistently here. Recognise's sole remaining "
    "subsidiary, Credit Asset Management Limited (CAML), entered members' voluntary liquidation "
    "on 24 March 2025; the 2025 accounts therefore were not consolidated, and the 2026 report is "
    "standalone. FY2025 is taken from the clean comparative in the 2026 report because the bank's "
    "published 2025 PDF has an extraction/encoding problem; no figure is inferred. Blank cells "
    "mean not publicly disclosed, not zero."
)
CASH_SOURCES = (
    "Sources - Recognise Bank Limited Company/standalone cash flows, £'000:\n"
    f"FY2026 & FY2025: Annual Report 2026, printed p.52 - {AR26_URL}\n"
    f"FY2024 & FY2023: Annual Report 2024, printed p.46 (Company statement) - {AR24_URL}\n"
    f"FY2023 & FY2022: Annual Report 2023, printed p.42 (Company statement) - {AR23_URL}\n"
    f"FY2022 & FY2021 comparative: Annual Report 2022, printed p.44 (Company statement) - {AR22_URL}\n\n"
    + ENTITY_NOTE
)
BS_SOURCES = (
    "Sources - Recognise Bank Limited Company/standalone balance sheet, £'000:\n"
    f"FY2026 & FY2025: Annual Report 2026, printed p.50, Balance sheet - {AR26_URL}\n"
    f"FY2024 & FY2023: Annual Report 2024, printed p.42, Company balance sheet - {AR24_URL}\n"
    f"FY2023 & FY2022: Annual Report 2023, printed p.38, Company balance sheet - {AR23_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTE: Debt securities and Deferred tax asset only appear as separate lines from FY2025 and "
    "FY2026 respectively (not disclosed pre-FY2025; blank means not applicable/not disclosed, not zero, except "
    "where a report explicitly showed a nil dash, which is recorded as 0 - e.g. Lease liabilities FY2025 and "
    "Borrowings FY2026). Investment in subsidiaries appears only FY2023-FY2024 (Credit Asset Management Limited, "
    "CAML, was a subsidiary until its liquidation in March 2025). Borrowings appears only FY2025 (£503k). Company "
    "balance sheets pre-FY2025 also showed Group columns; the Company column is used consistently, matching the "
    "existing Cash Flow Statement convention."
)
PL_SOURCES = (
    "Sources - Recognise Bank Limited Statement of Comprehensive Income, £'000:\n"
    f"FY2026 & FY2025: Annual Report 2026, printed p.49, Statement of comprehensive income (Company/standalone "
    f"basis) - {AR26_URL}\n"
    f"FY2024 & FY2023: Annual Report 2024, printed p.40, Consolidated statement of comprehensive income - {AR24_URL}\n"
    f"FY2023 & FY2022: Annual Report 2023, printed p.36, Consolidated statement of comprehensive income - {AR23_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTE: Recognise Bank took advantage of s.408 Companies Act 2006 and did not present a "
    "standalone Company income statement for FY2022-FY2024 (only the Group/consolidated income statement was "
    "published in those years); the detail rows above for FY2022-FY2024 are therefore Group-level, not Company-"
    "level. The 'Profit/(loss) for the year' TOTAL row uses the Company-level bottom line for all 5 years, "
    "consistent with the Balance Sheet, Cash Flow Statement, and Statement of Changes in Equity elsewhere in this "
    "workbook (per the Company balance sheet's own footnote disclosure of the Company's loss after tax). For "
    "FY2022-FY2024 this Company bottom line does not foot exactly from the Group-level 'Profit/(loss) before tax' "
    "row above it (differs by roughly £250k-£370k) - a genuine, documented Group-vs-Company basis difference, not "
    "a calculation error. Restructuring costs only appear as a separate line from FY2025."
)
EQ_SOURCES = (
    "Sources - Recognise Bank Limited Company Statement of Changes in Equity, £'000:\n"
    f"FY2025-FY2026 movements & FY2024 closing balance: Annual Report 2026, printed p.51, Statement of changes in "
    f"equity - {AR26_URL}\n"
    f"FY2023-FY2024 movements: Annual Report 2024, printed p.44, Company statement of changes in equity - {AR24_URL}\n"
    f"FY2022-FY2023 movements & FY2021 opening balance: Annual Report 2023, printed p.40, Company statement of "
    f"changes in equity - {AR23_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nEvery year ties exactly to both the next year's opening balance and that year's own Company balance "
    "sheet Total equity - zero undocumented plug rows across all 5 years."
)
AQ_SOURCES = (
    "Sources - Recognise Bank Limited Company loan book by IFRS 9 stage, £'000:\n"
    f"FY2026 & FY2025: Annual Report 2026, printed p.67 (portfolio analysis by credit risk grade) and p.74 (note "
    f"18, loan movements) - {AR26_URL}\n"
    f"FY2024 & FY2023: Annual Report 2024, printed p.57 (Company portfolio analysis) - {AR24_URL}\n"
    f"FY2023 & FY2022: Annual Report 2023, printed p.62 (Company note 17, loan movements, incl. the FY2022 Group-"
    f"and-Company combined comparative) - {AR23_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nAll 5 years' Net loans and advances to customers ties exactly to the Balance Sheet's own Loans and "
    "advances to customers line. Stage 2 and Stage 3 were both nil in FY2022 and FY2023 (100% Stage 1) - a young, "
    "still-small loan book at that point, not an omission. Stage 3 (NPL) and coverage ratios are left blank for "
    "FY2022/FY2023 as not meaningful (zero Stage 3 exposure), not because they were undisclosed."
)
RWA_SOURCES = (
    "Sources - Recognise Bank Limited UK OV1 Overview of RWAs, £'000:\n"
    f"FY2026 & FY2025: Pillar 3 Disclosure March 2026, Table 2 UK OV1, printed p.4 - {P3_26_URL}\n"
    f"FY2024 & FY2023: Pillar 3 Disclosure March 2024, Table 2 UK OV1, printed p.4 - {P3_24_URL}\n"
    f"FY2023 & FY2022: Pillar 3 Disclosure March 2023, Table 2 UK OV1, printed p.4 (Wayback Machine archive, "
    f"capture 2023-12-10; not linked from the bank's current site) - {P3_23_URL}\n\n"
    "Counterparty credit risk (CCR) is only disclosed as a separate category from FY2025 (Recognise did not have "
    "material CCR exposure, or did not break it out, in FY2022-FY2024's OV1 tables - blank, not zero, for those "
    "years). All 5 years tie exactly to the Total risk-weighted exposure amount already on file in the CET1/Total "
    "RWAs metric sheets."
)
P3_SOURCES = (
    f"Source - Recognise Bank Limited Pillar 3 Disclosure 2026, Table 1 UK KM1, printed p.3 "
    f"(Mar-26 through Mar-22 comparatives) - {P3_26_URL}\n"
    "The 2026 KM1 table supplies all five requested year-ends on a bank/entity basis."
)

bw = BankWorkbook(bank_name="Recognise Bank Limited", years=YEARS, header_color="51158C")

BS_ROWS = [
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and cash equivalents", {"FY2026": 160949, "FY2025": 238732, "FY2024": 164292, "FY2023": 138354, "FY2022": 36233}),
        ("DATA", "Debt securities", {"FY2026": 29999, "FY2025": 9932}),
        ("DATA", "Investment in subsidiaries", {"FY2024": 349, "FY2023": 3349}),
        ("DATA", "Loans and advances to customers", {"FY2026": 461863, "FY2025": 305596, "FY2024": 302710, "FY2023": 121441, "FY2022": 98941}),
        ("DATA", "Other assets", {"FY2026": 1603, "FY2025": 1418, "FY2024": 970, "FY2023": 3221, "FY2022": 516}),
        ("DATA", "Property, plant and equipment", {"FY2026": 89, "FY2025": 62, "FY2024": 165, "FY2023": 230, "FY2022": 70}),
        ("DATA", "Intangible assets", {"FY2026": 980, "FY2025": 1813, "FY2024": 1832, "FY2023": 1095, "FY2022": 980}),
        ("DATA", "Right-of-use assets", {"FY2026": 307, "FY2025": 3, "FY2024": 171, "FY2023": 372, "FY2022": 100}),
        ("DATA", "Deferred tax asset", {"FY2026": 7060}),
        ("TOTAL", "Total assets", {"FY2026": 662850, "FY2025": 557556, "FY2024": 470489, "FY2023": 268062, "FY2022": 136840}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits from customers", {"FY2026": 575545, "FY2025": 484311, "FY2024": 411667, "FY2023": 200251, "FY2022": 94994}),
        ("DATA", "Loans and advances from subsidiary", {"FY2024": 517, "FY2023": 5000, "FY2022": 468}),
        ("DATA", "Borrowings", {"FY2026": 0, "FY2025": 503}),
        ("DATA", "Lease liabilities", {"FY2026": 293, "FY2025": 0, "FY2024": 188, "FY2023": 413, "FY2022": 103}),
        ("DATA", "Other liabilities", {"FY2026": 4355, "FY2025": 3941, "FY2024": 3985, "FY2023": 4097, "FY2022": 3352}),
        ("TOTAL", "Total liabilities", {"FY2026": 580193, "FY2025": 488755, "FY2024": 416357, "FY2023": 209761, "FY2022": 98917}),
        ("SECTION", "Equity", {}),
        ("DATA", "Share capital", {"FY2026": 87531, "FY2025": 82531, "FY2024": 62530, "FY2023": 57530, "FY2022": 30578}),
        ("DATA", "Share premium", {"FY2026": 38722, "FY2025": 38722, "FY2024": 38722, "FY2023": 38722, "FY2022": 32513}),
        ("DATA", "Other reserves", {"FY2026": 90, "FY2025": 90, "FY2024": 90, "FY2023": 0, "FY2022": 226}),
        ("DATA", "Accumulated losses", {"FY2026": -43686, "FY2025": -52542, "FY2024": -47210, "FY2023": -37951, "FY2022": -25394}),
        ("TOTAL", "Total equity", {"FY2026": 82657, "FY2025": 68801, "FY2024": 54132, "FY2023": 58301, "FY2022": 37923}),
        ("TOTAL", "Total liabilities and equity", {"FY2026": 662850, "FY2025": 557556, "FY2024": 470489, "FY2023": 268062, "FY2022": 136840}),
]
bw.add_balance_sheet_sheet(
    title="Recognise Bank Limited - Company Balance Sheet",
    subtitle="Company/standalone basis, £'000; FY2022-FY2026 (31 March year-end).",
    rows=BS_ROWS,
    sources_text=BS_SOURCES,
    first_col_width=60,
    source_height=260,
    unit_suffix=" (£'000)",
)

PL_ROWS = [
        ("SECTION", "Income", {}),
        ("DATA", "Interest income", {"FY2026": 42754, "FY2025": 36294, "FY2024": 25554, "FY2023": 9206, "FY2022": 2380}),
        ("DATA", "Interest expense", {"FY2026": -22398, "FY2025": -20832, "FY2024": -13153, "FY2023": -3007, "FY2022": -824}),
        ("TOTAL", "Net interest income", {"FY2026": 20356, "FY2025": 15462, "FY2024": 12401, "FY2023": 6199, "FY2022": 1556}),
        ("DATA", "Fee and commission income", {"FY2026": 557, "FY2025": 412, "FY2024": 408, "FY2023": 175, "FY2022": 16}),
        ("DATA", "Fee and commission expense", {"FY2026": -34, "FY2025": -61, "FY2024": -102, "FY2023": -7, "FY2022": -16}),
        ("TOTAL", "Net operating income", {"FY2026": 20879, "FY2025": 15813, "FY2024": 12707, "FY2023": 6367, "FY2022": 1556}),
        ("DATA", "Other income", {"FY2026": 432, "FY2025": 1420, "FY2024": 777, "FY2023": 1, "FY2022": 0}),
        ("SECTION", "Operating expenses", {}),
        ("DATA", "Staff costs", {"FY2026": -10333, "FY2025": -10346, "FY2024": -10453, "FY2023": -11914, "FY2022": -8405}),
        ("DATA", "Other operating expenses", {"FY2026": -7759, "FY2025": -6884, "FY2024": -8277, "FY2023": -6802, "FY2022": -4831}),
        ("DATA", "Restructuring costs", {"FY2026": -910, "FY2025": -2325}),
        ("DATA", "Depreciation and amortisation", {"FY2026": -559, "FY2025": -699, "FY2024": -635, "FY2023": -789, "FY2022": -307}),
        ("DATA", "Net impairment gain/(loss) on financial assets", {"FY2026": 46, "FY2025": -2311, "FY2024": -3126, "FY2023": 162, "FY2022": -149}),
        ("TOTAL", "Total operating expense", {"FY2026": -19515, "FY2025": -22565, "FY2024": -22491, "FY2023": -19343, "FY2022": -13692}),
        ("TOTAL", "Profit/(loss) before tax", {"FY2026": 1796, "FY2025": -5332, "FY2024": -9007, "FY2023": -12975, "FY2022": -12136}),
        ("DATA", "Taxation credit/(expense) for the year", {"FY2026": 7060, "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0}),
        ("TOTAL", "Profit/(loss) for the year", {"FY2026": 8856, "FY2025": -5332, "FY2024": -9259, "FY2023": -12783, "FY2022": -12444}),
]
bw.add_income_statement_sheet(
    title="Recognise Bank Limited - Statement of Comprehensive Income",
    subtitle="FY2025-FY2026 Company/standalone basis; FY2022-FY2024 detail rows Group-level (see sources), £'000.",
    rows=PL_ROWS,
    sources_text=PL_SOURCES,
    first_col_width=62,
    source_height=280,
    unit_suffix=" (£'000)",
)

EQ_ROWS = [
        ("TOTAL", "Balance at 1 April 2021", (21210, 18931, -12950, 55, 27246)),
        ("DATA", "Issue of ordinary shares (FY2022)", (9368, 13582, None, None, 22950)),
        ("DATA", "Share-based payments (FY2022)", (None, None, None, 171, 171)),
        ("TOTAL", "Total comprehensive loss for the year (FY2022)", (None, None, -12444, None, -12444)),
        ("TOTAL", "Balance at 31 March 2022", (30578, 32513, -25394, 226, 37923)),
        ("TOTAL", "Total comprehensive loss for the year (FY2023)", (None, None, -12783, None, -12783)),
        ("DATA", "Transfer from Other reserves (FY2023)", (None, None, 226, -226, 0)),
        ("DATA", "Issue of ordinary shares (FY2023)", (26952, 6209, None, None, 33161)),
        ("TOTAL", "Balance at 31 March 2023", (57530, 38722, -37951, 0, 58301)),
        ("TOTAL", "Total comprehensive loss for the year (FY2024)", (None, None, -9259, None, -9259)),
        ("DATA", "Share-based payments (FY2024)", (None, None, None, 90, 90)),
        ("DATA", "Issue of ordinary shares (FY2024)", (5000, None, None, None, 5000)),
        ("TOTAL", "Balance at 31 March 2024", (62530, 38722, -47210, 90, 54132)),
        ("TOTAL", "Total comprehensive loss for the year (FY2025)", (None, None, -5332, None, -5332)),
        ("DATA", "Issue of ordinary shares (FY2025)", (20001, None, None, None, 20001)),
        ("TOTAL", "Balance at 31 March 2025", (82531, 38722, -52542, 90, 68801)),
        ("TOTAL", "Total comprehensive income for the year (FY2026)", (None, None, 8856, None, 8856)),
        ("DATA", "Issue of ordinary shares (FY2026)", (5000, None, None, None, 5000)),
        ("TOTAL", "Balance at 31 March 2026", (87531, 38722, -43686, 90, 82657)),
]
bw.add_equity_changes_sheet(
    title="Recognise Bank Limited - Company Statement of Changes in Equity",
    subtitle="Company/standalone basis, £'000; FY2022-FY2026 (31 March year-end), read chronologically.",
    headers=["Share capital", "Share premium", "Accumulated losses", "Other reserves", "Total equity"],
    rows=EQ_ROWS,
    sources_text=EQ_SOURCES,
    first_col_width=46,
    source_height=220,
)

rows = [
    ("SECTION", "Cash flow from operating activities", {}),
    ("DATA", "Profit/(loss) for the year", {"FY2026": 8856, "FY2025": -5332, "FY2024": -9259, "FY2023": -12783, "FY2022": -12444}),
    ("DATA", "Depreciation and amortisation", {"FY2026": 559, "FY2025": 699, "FY2024": 635, "FY2023": 789, "FY2022": 305}),
    ("DATA", "Intangible assets impairment", {"FY2026": 928}),
    ("DATA", "Recognition of deferred tax asset", {"FY2026": -7060}),
    ("DATA", "Interest earned during the year", {"FY2026": -42754, "FY2025": -36294, "FY2024": -25487, "FY2023": -9112, "FY2022": -2136}),
    ("DATA", "Interest expense during the year", {"FY2026": 22398, "FY2025": 20832, "FY2024": 13153, "FY2023": 2970, "FY2022": 803}),
    ("DATA", "Interest expense on leases", {"FY2026": 5, "FY2025": 10, "FY2024": 22, "FY2023": 29}),
    ("DATA", "Impairment (gain)/loss", {"FY2026": -46, "FY2025": 2311, "FY2024": 3339, "FY2023": 76, "FY2022": 148}),
    ("DATA", "Share-based incentive plan", {"FY2022": 171}),
    ("DATA", "Dividend income from CAML", {"FY2025": -400, "FY2024": 0, "FY2023": -468}),
    ("DATA", "Other income", {"FY2026": -431}),
    ("DATA", "Interest received", {"FY2026": 41682, "FY2025": 36170, "FY2024": 24429, "FY2023": 9210, "FY2022": 3608}),
    ("DATA", "Interest paid", {"FY2026": -11971, "FY2025": -11997, "FY2024": -4824, "FY2023": -2245, "FY2022": -457}),
    ("DATA", "Increase in debt securities", {"FY2026": -19928, "FY2025": -9656}),
    ("DATA", "Decrease/(increase) in debt securities", {"FY2022": 6500}),
    ("DATA", "Increase in loans and advances", {"FY2026": -155239, "FY2025": -5307, "FY2024": -183505, "FY2023": -22804, "FY2022": -93780}),
    ("DATA", "Increase in deposits from customers", {"FY2026": 80807, "FY2025": 63808, "FY2024": 203087, "FY2023": 104533, "FY2022": 94646}),
    ("DATA", "Increase/(decrease) in other assets", {"FY2026": -271, "FY2025": -78, "FY2024": -77, "FY2023": -248, "FY2022": -276}),
    ("DATA", "Increase/(decrease) in other liabilities", {"FY2026": 368, "FY2025": -60, "FY2024": -22, "FY2023": 745, "FY2022": 492}),
    ("TOTAL", "Net cash (used in)/generated from operating activities", {"FY2026": -82097, "FY2025": 54706, "FY2024": 21491, "FY2023": 70692, "FY2022": -2420}),
    ("SECTION", "Cash flow from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2026": -90, "FY2025": -7, "FY2024": -52, "FY2023": -259, "FY2022": -53}),
    ("DATA", "Disposal of property, plant and equipment", {"FY2022": 1}),
    ("DATA", "Distribution/dividend received from CAML", {"FY2026": 11, "FY2025": 60}),
    ("DATA", "Surplus funds sent from CAML", {"FY2025": 280, "FY2024": 800, "FY2023": 1000}),
    ("DATA", "Loans repaid by group companies", {"FY2022": 5017}),
    ("DATA", "Loans advanced to group companies", {"FY2022": -271}),
    ("DATA", "Purchase of intangible assets", {"FY2026": -562, "FY2025": -402, "FY2024": -1054, "FY2023": -571, "FY2022": -156}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {"FY2026": -641, "FY2025": -69, "FY2024": -306, "FY2023": 170, "FY2022": 4538}),
    ("SECTION", "Cash flow from financing activities", {}),
    ("DATA", "Interest paid on customer deposits", {"FY2022": 6}),
    ("DATA", "Finance lease payments", {"FY2026": -45, "FY2025": -198, "FY2024": -247, "FY2023": -225, "FY2022": -66}),
    ("DATA", "Gross proceeds from the issue of ordinary shares", {"FY2026": 5000, "FY2025": 20001, "FY2024": 5000, "FY2023": 31504, "FY2022": 22950}),
    ("DATA", "Costs of share issue", {"FY2023": -20}),
    ("TOTAL", "Net cash generated from financing activities", {"FY2026": 4955, "FY2025": 19803, "FY2024": 4753, "FY2023": 31259, "FY2022": 22890}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2026": -77783, "FY2025": 74440, "FY2024": 25938, "FY2023": 102121, "FY2022": 25008}),
    ("DATA", "Cash and cash equivalents brought forward", {"FY2026": 238732, "FY2025": 164292, "FY2024": 138354, "FY2023": 36233, "FY2022": 11225}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2026": 160949, "FY2025": 238732, "FY2024": 164292, "FY2023": 138354, "FY2022": 36233}),
]
bw.add_cash_flow_sheet(title="Recognise Bank Limited - Company Cash Flow Statement", subtitle="Company/standalone basis, £'000; FY2022-FY2026 (31 March year-end).", rows=rows, sources_text=CASH_SOURCES, first_col_width=66, source_height=230, unit_suffix=" (£'000)")

bw.add_asset_quality_sheet(
    title="Recognise Bank Limited - Asset Quality",
    subtitle="Company/standalone basis, loan book by IFRS 9 stage, £'000; FY2022-FY2026 (31 March year-end).",
    rows=[
        ("SECTION", "Gross loans and advances by IFRS 9 stage", {}),
        ("DATA", "Stage 1 (12-month ECL)", {"FY2026": 416693, "FY2025": 284884, "FY2024": 284104, "FY2023": 121660, "FY2022": 99094}),
        ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2026": 23895, "FY2025": 15458, "FY2024": 17405, "FY2023": 0, "FY2022": 0}),
        ("DATA", "Stage 3 (credit-impaired)", {"FY2026": 25835, "FY2025": 11094, "FY2024": 4748, "FY2023": 0, "FY2022": 0}),
        ("TOTAL", "Gross loans and advances to customers", {"FY2026": 466423, "FY2025": 311436, "FY2024": 306257, "FY2023": 121660, "FY2022": 99094}),
        ("SECTION", "Allowances for expected credit losses (ECL)", {}),
        ("DATA", "Stage 1 allowance", {"FY2026": -357, "FY2025": -526, "FY2024": -335, "FY2023": -219, "FY2022": -153}),
        ("DATA", "Stage 2 allowance", {"FY2026": -29, "FY2025": -265, "FY2024": -15, "FY2023": 0, "FY2022": 0}),
        ("DATA", "Stage 3 allowance", {"FY2026": -4174, "FY2025": -5049, "FY2024": -3197, "FY2023": 0, "FY2022": 0}),
        ("TOTAL", "Total allowances for ECLs", {"FY2026": -4560, "FY2025": -5840, "FY2024": -3547, "FY2023": -219, "FY2022": -153}),
        ("TOTAL", "Net loans and advances to customers", {"FY2026": 461863, "FY2025": 305596, "FY2024": 302710, "FY2023": 121441, "FY2022": 98941}),
        ("SECTION", "Asset quality ratios", {}),
        ("DATA", "Stage 3 (NPL) ratio, gross", {"FY2026": "5.54%", "FY2025": "3.56%", "FY2024": "1.55%", "FY2023": "0.00%", "FY2022": "0.00%"}),
        ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", {"FY2026": "16.16%", "FY2025": "45.51%", "FY2024": "67.35%"}),
    ],
    sources_text=AQ_SOURCES,
    first_col_width=58,
    source_height=230,
    unit_suffix=" (£'000)",
)

def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, P3_SOURCES, note=note, first_col_width=54, source_height=130)

km1 = {
    "FY2026": (74617, 356376, "20.9%", 509006, "14.7%", 220955, 82309, 8630, 73679, "299.9%", 520393, 295089, "176.4%"),
    "FY2025": (66988, 220421, "30.4%", 329206, "20.3%", 212180, 44148, 5456, 38692, "548.4%", 480437, 211608, "227.0%"),
    "FY2024": (52617, 200213, "26.3%", 316246, "16.6%", 149255, 39271, 10380, 28891, "516.6%", 440424, 213351, "206.4%"),
    "FY2023": (57482, 88249, "65.1%", 134402, "42.8%", 71930, 18358, 9363, 8996, "799.6%", 247010, 93289, "264.8%"),
    "FY2022": (37411, 87216, "42.9%", 109158, "34.3%", 20648, 13379, 8079, 5300, "389.6%", 128630, 78103, "164.7%"),
}
def col(i): return {y: km1[y][i] for y in YEARS}
metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", col(0))])
metric("CET1 Ratio", "%", [("Common Equity Tier 1 (CET1) ratio", col(2))])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", col(0))])
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", col(2))])
metric("Total Capital", "£'000", [("Total capital", col(0))])
metric("Total Capital Ratio", "%", [("Total capital ratio", col(2))])
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", col(1))])

bw.add_rwa_breakdown_sheet(
    title="Recognise Bank Limited - RWA Breakdown",
    subtitle="UK OV1 Overview of risk-weighted exposure amounts, £'000; FY2022-FY2026 (31 March year-end).",
    rows=[
        ("SECTION", "Risk-weighted exposure amounts by category", {}),
        ("DATA", "Credit risk (excluding CCR)", {"FY2026": 325441, "FY2025": 198530, "FY2024": 187320, "FY2023": 83185, "FY2022": 81924}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2026": 61, "FY2025": 91}),
        ("DATA", "Operational risk", {"FY2026": 30874, "FY2025": 21800, "FY2024": 12893, "FY2023": 5065, "FY2022": 5292}),
        ("TOTAL", "Total risk-weighted exposure amount", {"FY2026": 356376, "FY2025": 220421, "FY2024": 200213, "FY2023": 88249, "FY2022": 87216}),
    ],
    sources_text=RWA_SOURCES,
    first_col_width=54,
    source_height=220,
    unit_suffix=" (£'000)",
)

metric("Leverage Ratio", "£'000 / %", [("Total exposure measure excluding claims on central banks", col(3)), ("Leverage ratio excluding claims on central banks", col(4))])
metric("LCR", "£'000 / %", [("Total high-quality liquid assets (HQLA), weighted value - average", col(5)), ("Cash outflows - total weighted value", col(6)), ("Cash inflows - total weighted value", col(7)), ("Total net cash outflows (adjusted value)", col(8)), ("Liquidity coverage ratio", col(9))])
metric("NSFR", "£'000 / %", [("Total available stable funding", col(10)), ("Total required stable funding", col(11)), ("NSFR ratio", col(12))])
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No quantitative MREL ratio was located in the official Recognise Bank annual reports or Pillar 3 disclosures reviewed.")

def row_values(label, rows_list=rows):
    return next(values for kind, name, values in rows_list if name == label)

equity_opening = {"FY2026": 68801, "FY2025": 54132, "FY2024": 58301, "FY2023": 37923, "FY2022": 27246}
equity_other_movements = {"FY2026": 5000, "FY2025": 20001, "FY2024": 5090, "FY2023": 33161, "FY2022": 23121}

bw.add_overview_sheet(
    cash_flow_totals=[(label, row_values(label)) for label in ["Net cash (used in)/generated from operating activities", "Net cash (used in)/generated from investing activities", "Net cash generated from financing activities", "Cash and cash equivalents at end of year"]],
    cash_flow_unit="£'000",
    ratios=[("CET1 Ratio", col(2)), ("Total Capital Ratio", col(2)), ("Leverage Ratio", col(4)), ("LCR", col(9)), ("NSFR", col(12))],
    balance_sheet_totals=[
        ("Total assets", row_values("Total assets", BS_ROWS)),
        ("Loans and advances to customers", row_values("Loans and advances to customers", BS_ROWS)),
        ("Deposits from customers", row_values("Deposits from customers", BS_ROWS)),
        ("Total equity", row_values("Total equity", BS_ROWS)),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", row_values("Net operating income", PL_ROWS)),
        ("Total operating expense", row_values("Total operating expense", PL_ROWS)),
        ("Profit/(loss) for the year", row_values("Profit/(loss) for the year", PL_ROWS)),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", equity_opening),
        ("Total comprehensive income/(loss) for the year", {"FY2026": 8856, "FY2025": -5332, "FY2024": -9259, "FY2023": -12783, "FY2022": -12444}),
        ("Other equity movements (share issuances etc.), net", equity_other_movements),
        ("Closing equity", row_values("Total equity", BS_ROWS)),
    ],
    equity_changes_unit="£'000",
    note="Cash flows and Balance Sheet are Company/standalone figures. P&L detail rows are Group-level for FY2022-FY2024 (Company P&L not separately presented under s.408 exemption); 'Profit/(loss) for the year' is the Company-level figure throughout, consistent with the rest of the workbook. Pillar 3 metrics are Recognise Bank Limited UK KM1 figures. FY2025 accounts were not consolidated after CAML entered liquidation; the 2026 report supplies the FY2025 comparative. Blank cells mean not disclosed, not zero.",
)
bw.save("/Users/armaan/code/katalysis/banks/RECOGNISE BANK FINANCIALS.xlsx")
