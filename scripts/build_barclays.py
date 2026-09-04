import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR25_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2025/Barclays-Bank-UK-PLC-Annual-Report-2025.pdf"
AR23_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2023/Barclays-Bank-UK-Annual-Report-2023-Results-committee.pdf"
AR21_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2021/Barclays-Bank-UK-PLC-2021-Annual-Report.pdf"

P3_25_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/ResultAnnouncements/FullYear2025Results/FY25-BBUKPLC-Pillar-3.pdf"
P3_23_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2023/BB-UK-Pillar-3-Report-2023.pdf"
P3_21_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2021/Barclays-Bank-UK-PLC-Pillar-3-Report-2021.pdf"

CASH_FLOW_SOURCES = (
    "Sources — all figures are Barclays Bank UK Group consolidated cash flow statement, £m:\n"
    f"FY2025 & FY2024: Barclays Bank UK PLC Annual Report 2025, p.201 (Consolidated cash flow statement) — {AR25_URL}\n"
    f"FY2023 & FY2022: Barclays Bank UK PLC Annual Report 2023, p.166 (Consolidated cash flow statement) — {AR23_URL}\n"
    f"FY2021: Barclays Bank UK PLC Annual Report 2021, p.138 (Consolidated cash flow statement) — {AR21_URL}\n"
    "Note: Barclays changed cash flow statement presentation granularity across these report vintages "
    "(e.g. FY2025/FY2024 split some line items — such as repurchase/reverse repurchase agreements and trading "
    "portfolio assets/liabilities — that FY2023/FY2022/FY2021 report on a combined basis). Blank cells indicate "
    "that year's report did not disclose that specific split; where a coarser combined figure was reported instead, "
    "it appears on its own row. Section totals (net cash from operating/investing/financing activities, "
    "cash and cash equivalents) are consistent and comparable across all 5 years."
)

def p3_sources(part_label_25="Table 6: KM1 - Key metrics - Part 1", page_25="11",
               part_label_23="Table 6: UK KM1 - Key metrics - Part 1", page_23="11",
               part_label_21="Table 4: Key Metrics (KM1 / IFRS 9-FL)", page_21="9"):
    return (
        "Sources — Barclays Bank UK Group consolidated (Pillar 3) basis:\n"
        f"FY2025 & FY2024: Barclays Bank UK PLC Pillar 3 Report 2025, p.{page_25} ({part_label_25}) — {P3_25_URL}\n"
        f"FY2023 & FY2022: Barclays Bank UK PLC Pillar 3 Report 2023, p.{page_23} ({part_label_23}) — {P3_23_URL}\n"
        f"FY2021: Barclays Bank UK PLC Pillar 3 Report 2021, p.{page_21} ({part_label_21}) — {P3_21_URL}"
    )

bw = BankWorkbook(bank_name="Barclays Bank UK Group", years=YEARS, header_color="1F3864")

STATEMENTS_SOURCES = (
    "Sources — all figures are Barclays Bank UK Group consolidated (audited), £m:\n"
    f"FY2025 & FY2024: Barclays Bank UK PLC Annual Report 2025, pp.197 (income statement), 199 (balance sheet), "
    f"200 (statement of changes in equity) — {AR25_URL}\n"
    f"FY2023 & FY2022: Barclays Bank UK PLC Annual Report 2023, pp.162 (income statement), 164 (balance sheet), "
    f"165 (statement of changes in equity) — {AR23_URL}\n"
    f"FY2021: Barclays Bank UK PLC Annual Report 2021, pp.134 (income statement), 136 (balance sheet), "
    f"137 (statement of changes in equity) — {AR21_URL}\n"
    "Balance sheet note: FY2021 does not split loans and advances at amortised cost into a bank/customer split, "
    "does not disclose a separate debt securities at amortised cost line, and reports deposits at amortised cost "
    "as a single combined line - the combined figures appear on their own row for that year only; FY2022-2025 all "
    "split these. Income statement note: FY2021 places credit impairment releases/(charges) before operating "
    "expenses (subtotalled as 'Net operating income'), while FY2022-2025 place it after operating expenses "
    "(subtotalled as 'Profit before impairment') - a genuine presentation restructuring, not a transcription error; "
    "both years' own subtotals are reproduced as reported."
)

# ---------------------------------------------------------------
# Balance Sheet (Consolidated Statement of Financial Position), £m
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 21208, "FY2024": 29819, "FY2023": 34948, "FY2022": 54208, "FY2021": 69488}),
    ("DATA", "Cash collateral and settlement balances", {"FY2025": 6120, "FY2024": 6002, "FY2023": 5507, "FY2022": 5194, "FY2021": 5067}),
    ("DATA", "Debt securities at amortised cost", {"FY2025": 13492, "FY2024": 17983, "FY2023": 17794, "FY2022": 18537}),
    ("DATA", "Loans and advances at amortised cost to banks", {"FY2025": 228, "FY2024": 281, "FY2023": 1213, "FY2022": 1391}),
    ("DATA", "Loans and advances at amortised cost to customers", {"FY2025": 215634, "FY2024": 206435, "FY2023": 200782, "FY2022": 203279}),
    ("DATA", "Loans and advances at amortised cost (combined, as reported)", {"FY2021": 220271}),
    ("DATA", "Reverse repurchase agreements and other similar secured lending at amortised cost", {"FY2025": 6001, "FY2024": 5894, "FY2023": 3567, "FY2022": 477, "FY2021": 65}),
    ("DATA", "Trading portfolio assets", {"FY2025": 385, "FY2024": 242, "FY2023": 43, "FY2022": 54, "FY2021": 169}),
    ("DATA", "Financial assets at fair value through the income statement", {"FY2025": 1413, "FY2024": 1543, "FY2023": 1716, "FY2022": 1980, "FY2021": 2767}),
    ("DATA", "Derivative financial instruments", {"FY2025": 890, "FY2024": 1901, "FY2023": 1566, "FY2022": 611, "FY2021": 890}),
    ("DATA", "Financial assets at fair value through other comprehensive income", {"FY2025": 31572, "FY2024": 27045, "FY2023": 20409, "FY2022": 19970, "FY2021": 14945}),
    ("DATA", "Goodwill and intangible assets", {"FY2025": 3933, "FY2024": 3948, "FY2023": 3870, "FY2022": 3528, "FY2021": 3526}),
    ("DATA", "Property, plant and equipment", {"FY2025": 287, "FY2024": 239, "FY2023": 261, "FY2022": 382, "FY2021": 562}),
    ("DATA", "Deferred tax assets", {"FY2025": 884, "FY2024": 1212, "FY2023": 1296, "FY2022": 1916, "FY2021": 1368}),
    ("DATA", "Retirement benefit assets", {"FY2025": 69}),
    ("DATA", "Other assets", {"FY2025": 708, "FY2024": 635, "FY2023": 587, "FY2022": 652, "FY2021": 577}),
    ("TOTAL", "Total assets", {"FY2025": 302824, "FY2024": 303179, "FY2023": 293559, "FY2022": 312179, "FY2021": 319695}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits at amortised cost from banks", {"FY2025": 125, "FY2024": 85, "FY2023": 6, "FY2022": 59}),
    ("DATA", "Deposits at amortised cost from customers", {"FY2025": 244666, "FY2024": 244376, "FY2023": 241218, "FY2022": 258058}),
    ("DATA", "Deposits at amortised cost (combined, as reported)", {"FY2021": 260732}),
    ("DATA", "Cash collateral and settlement balances", {"FY2025": 828, "FY2024": 1779, "FY2023": 1370, "FY2022": 553, "FY2021": 774}),
    ("DATA", "Repurchase agreements and other similar secured borrowing at amortised cost", {"FY2025": 13600, "FY2024": 15506, "FY2023": 15265, "FY2022": 17702, "FY2021": 18160}),
    ("DATA", "Debt securities in issue", {"FY2025": 4703, "FY2024": 2619, "FY2023": 3307, "FY2022": 8009, "FY2021": 8684}),
    ("DATA", "Subordinated liabilities", {"FY2025": 14049, "FY2024": 13512, "FY2023": 11499, "FY2022": 8268, "FY2021": 9516}),
    ("DATA", "Trading portfolio liabilities", {"FY2025": 908, "FY2024": 726, "FY2023": 908, "FY2022": 464, "FY2021": 878}),
    ("DATA", "Financial liabilities designated at fair value", {"FY2025": 1003, "FY2024": 2848, "FY2023": 196}),
    ("DATA", "Derivative financial instruments", {"FY2025": 195, "FY2024": 300, "FY2023": 398, "FY2022": 962, "FY2021": 814}),
    ("DATA", "Current tax liabilities", {"FY2025": 598, "FY2024": 954, "FY2023": 540, "FY2022": 578, "FY2021": 377}),
    ("DATA", "Provisions", {"FY2025": 364, "FY2024": 323, "FY2023": 364, "FY2022": 338, "FY2021": 536}),
    ("DATA", "Other liabilities", {"FY2025": 1507, "FY2024": 1566, "FY2023": 1627, "FY2022": 1775, "FY2021": 1824}),
    ("TOTAL", "Total liabilities", {"FY2025": 282546, "FY2024": 284594, "FY2023": 276698, "FY2022": 296766, "FY2021": 302295}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital and share premium", {"FY2025": 5, "FY2024": 5, "FY2023": 5, "FY2022": 5, "FY2021": 5}),
    ("DATA", "Other equity instruments", {"FY2025": 2227, "FY2024": 2425, "FY2023": 2429, "FY2022": 2560, "FY2021": 2560}),
    ("DATA", "Other reserves", {"FY2025": -38, "FY2024": -896, "FY2023": -1151, "FY2022": -2279, "FY2021": -366}),
    ("DATA", "Retained earnings", {"FY2025": 18084, "FY2024": 17051, "FY2023": 15578, "FY2022": 15127, "FY2021": 15201}),
    ("TOTAL", "Total equity", {"FY2025": 20278, "FY2024": 18585, "FY2023": 16861, "FY2022": 15413, "FY2021": 17400}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 302824, "FY2024": 303179, "FY2023": 293559, "FY2022": 312179, "FY2021": 319695}),
]

bw.add_balance_sheet_sheet(
    title="Barclays Bank UK PLC — Consolidated Balance Sheet",
    subtitle="Barclays Bank UK Group (consolidated basis), £m",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=200,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss (Consolidated Income Statement), £m
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 13136, "FY2024": 12588, "FY2023": 11024, "FY2022": 6981, "FY2021": 5775}),
    ("DATA", "Interest and similar expense", {"FY2025": -5371, "FY2024": -5851, "FY2023": -4597, "FY2022": -1340, "FY2021": -769}),
    ("TOTAL", "Net interest income", {"FY2025": 7765, "FY2024": 6737, "FY2023": 6427, "FY2022": 5641, "FY2021": 5006}),
    ("DATA", "Fee and commission income", {"FY2025": 1565, "FY2024": 1507, "FY2023": 1605, "FY2022": 1689, "FY2021": 1466}),
    ("DATA", "Fee and commission expense", {"FY2025": -482, "FY2024": -411, "FY2023": -370, "FY2022": -322, "FY2021": -219}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 1083, "FY2024": 1096, "FY2023": 1235, "FY2022": 1367, "FY2021": 1247}),
    ("DATA", "Net trading income/(expense)", {"FY2025": -48, "FY2024": -16, "FY2023": 35, "FY2022": 385, "FY2021": 40}),
    ("DATA", "Net investment income/(expense)", {"FY2025": -7, "FY2024": 41, "FY2023": -91, "FY2022": 1, "FY2021": 181}),
    ("DATA", "Gain on acquisition", {"FY2025": 0, "FY2024": 558}),
    ("DATA", "Other income", {"FY2025": 18, "FY2024": 7, "FY2023": 64, "FY2022": 3, "FY2021": 8}),
    ("TOTAL", "Total income", {"FY2025": 8811, "FY2024": 8423, "FY2023": 7670, "FY2022": 7397, "FY2021": 6482}),
    ("DATA", "Credit impairment releases/(charges) (pre-opex, FY2021 only)", {"FY2021": 371}),
    ("TOTAL", "Net operating income (FY2021 only)", {"FY2021": 6853}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -1555, "FY2024": -1215, "FY2023": -1209, "FY2022": -1170, "FY2021": -1392}),
    ("DATA", "Infrastructure costs", {"FY2025": -300, "FY2024": -258, "FY2023": -343, "FY2022": -385, "FY2021": -389}),
    ("DATA", "Administration and general expenses", {"FY2025": -3104, "FY2024": -2939, "FY2023": -3024, "FY2022": -2977, "FY2021": -2859}),
    ("DATA", "UK regulatory levies", {"FY2025": -85, "FY2024": -78}),
    ("DATA", "Litigation and conduct / provisions for litigation and conduct", {"FY2025": -49, "FY2024": -21, "FY2023": 9, "FY2022": -45, "FY2021": -51}),
    ("TOTAL", "Operating expenses", {"FY2025": -5093, "FY2024": -4511, "FY2023": -4567, "FY2022": -4577, "FY2021": -4691}),
    ("DATA", "Loss on disposal of subsidiaries, associates and joint ventures", {"FY2023": -124, "FY2022": 0}),
    ("DATA", "Profit on disposal of subsidiaries, associates and joint ventures (FY2021 only)", {"FY2021": 1}),
    ("TOTAL", "Profit before impairment (FY2022-FY2025 only)", {"FY2025": 3718, "FY2024": 3912, "FY2023": 2979, "FY2022": 2820}),
    ("DATA", "Credit impairment (charges)/releases (post-opex, FY2022-FY2025)", {"FY2025": -393, "FY2024": -352, "FY2023": -308, "FY2022": -268}),
    ("TOTAL", "Profit before tax", {"FY2025": 3325, "FY2024": 3560, "FY2023": 2671, "FY2022": 2552, "FY2021": 2163}),
    ("DATA", "Taxation", {"FY2025": -731, "FY2024": -940, "FY2023": -749, "FY2022": -745, "FY2021": -294}),
    ("TOTAL", "Profit after tax", {"FY2025": 2594, "FY2024": 2620, "FY2023": 1922, "FY2022": 1807, "FY2021": 1869}),
]

bw.add_income_statement_sheet(
    title="Barclays Bank UK PLC — Consolidated Income Statement",
    subtitle="Barclays Bank UK Group (consolidated basis), £m",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=200,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological), £m
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Called up share capital and share premium", "Other equity instruments", "Other reserves", "Retained earnings", "Total equity"]
equity_changes_rows = [
    ("TOTAL", "Balance as at 1 January 2021", (5, 2560, 473, 13989, 17027)),
    ("DATA", "Profit after tax", (None, 173, None, 1696, 1869)),
    ("DATA", "Financial assets at FVOCI reserve movement", (None, None, -67, None, -67)),
    ("DATA", "Cash flow hedges", (None, None, -772, None, -772)),
    ("TOTAL", "Total comprehensive income for the year (FY2021)", (None, 173, -839, 1696, 1030)),
    ("DATA", "Employee share schemes", (None, None, None, 37, 37)),
    ("DATA", "Other equity instruments coupons paid", (None, -173, None, None, -173)),
    ("DATA", "Vesting of employee share schemes", (None, None, None, -11, -11)),
    ("DATA", "Dividends paid", (None, None, None, -510, -510)),
    ("DATA", "Capital contribution from Barclays PLC", (None, None, None, 0, 0)),
    ("TOTAL", "Balance as at 31 December 2021", (5, 2560, -366, 15201, 17400)),
    ("DATA", "Profit after tax", (None, 173, None, 1634, 1807)),
    ("DATA", "Financial assets at FVOCI reserve movement", (None, None, -198, None, -198)),
    ("DATA", "Cash flow hedges", (None, None, -1715, None, -1715)),
    ("TOTAL", "Total comprehensive income for the year (FY2022)", (None, 173, -1913, 1634, -106)),
    ("DATA", "Employee share schemes", (None, None, None, 22, 22)),
    ("DATA", "Other equity instruments coupons paid", (None, -173, None, None, -173)),
    ("DATA", "Vesting of Barclays PLC shares under share based payment schemes", (None, None, None, -14, -14)),
    ("DATA", "Dividends paid", (None, None, None, -1715, -1715)),
    ("DATA", "Other reserve movements", (None, None, None, -1, -1)),
    ("TOTAL", "Balance as at 31 December 2022", (5, 2560, -2279, 15127, 15413)),
    ("DATA", "Profit after tax", (None, 177, None, 1745, 1922)),
    ("DATA", "Financial assets at FVOCI reserve movement", (None, None, 63, None, 63)),
    ("DATA", "Cash flow hedges", (None, None, 1065, None, 1065)),
    ("TOTAL", "Total comprehensive income for the year (FY2023)", (None, 177, 1128, 1745, 3050)),
    ("DATA", "Employee share schemes", (None, None, None, 22, 22)),
    ("DATA", "Issue and redemption of other equity", (None, -131, None, 2, -129)),
    ("DATA", "Other equity instruments coupons paid", (None, -177, None, None, -177)),
    ("DATA", "Vesting of Barclays PLC shares under share based payment schemes", (None, None, None, -16, -16)),
    ("DATA", "Dividends paid", (None, None, None, -1305, -1305)),
    ("DATA", "Other reserve movements", (None, None, None, 3, 3)),
    ("TOTAL", "Balance as at 31 December 2023", (5, 2429, -1151, 15578, 16861)),
    ("DATA", "Profit after tax", (None, 198, None, 2422, 2620)),
    ("DATA", "Financial assets at FVOCI reserve movement", (None, None, -33, None, -33)),
    ("DATA", "Cash flow hedges", (None, None, 288, None, 288)),
    ("TOTAL", "Total comprehensive income for the year (FY2024)", (None, 198, 255, 2422, 2875)),
    ("DATA", "Employee share schemes", (None, None, None, 42, 42)),
    ("DATA", "Issue and exchange of other equity", (None, -4, None, None, -4)),
    ("DATA", "Other equity instruments coupons paid", (None, -198, None, None, -198)),
    ("DATA", "Vesting of Barclays PLC shares under share based payment schemes", (None, None, None, -15, -15)),
    ("DATA", "Dividends paid", (None, None, None, -975, -975)),
    ("DATA", "Other reserve movements", (None, None, None, -1, -1)),
    ("TOTAL", "Balance as at 31 December 2024", (5, 2425, -896, 17051, 18585)),
    ("DATA", "Profit after tax", (None, 214, None, 2380, 2594)),
    ("DATA", "Financial assets at FVOCI reserve movement", (None, None, 106, None, 106)),
    ("DATA", "Cash flow hedges", (None, None, 752, None, 752)),
    ("DATA", "Pension remeasurement", (None, None, None, 46, 46)),
    ("TOTAL", "Total comprehensive income for the year (FY2025)", (None, 214, 858, 2426, 3498)),
    ("DATA", "Employee share schemes", (None, None, None, 72, 72)),
    ("DATA", "Issue and redemption of other equity", (None, -198, None, -9, -207)),
    ("DATA", "Other equity instruments coupons paid", (None, -214, None, None, -214)),
    ("DATA", "Vesting of Barclays PLC shares under share based payment schemes", (None, None, None, -28, -28)),
    ("DATA", "Dividends paid", (None, None, None, -1425, -1425)),
    ("DATA", "Other reserve movements", (None, None, None, -3, -3)),
    ("TOTAL", "Balance as at 31 December 2025", (5, 2227, -38, 18084, 20278)),
]

bw.add_equity_changes_sheet(
    title="Barclays Bank UK PLC — Consolidated Statement of Changes in Equity",
    subtitle="Barclays Bank UK Group (consolidated basis), £m",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=56,
    source_height=200,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 3325, "FY2024": 3560, "FY2023": 2671, "FY2022": 2552, "FY2021": 2163}),
    ("DATA", "Credit impairment charges/(releases)", {"FY2025": 393, "FY2024": 352, "FY2023": 308, "FY2022": 268, "FY2021": -371}),
    ("DATA", "Depreciation, amortisation and impairment of property, plant, equipment and intangibles", {"FY2025": 97, "FY2024": 95, "FY2023": 146, "FY2022": 187, "FY2021": 169}),
    ("DATA", "Loss on disposal of subsidiaries", {"FY2023": 124, "FY2022": 0}),
    ("DATA", "Other provisions (including pensions where noted)", {"FY2025": 144, "FY2024": 68, "FY2023": 69, "FY2022": 47, "FY2021": 25}),
    ("DATA", "Other non-cash items / exchange rate movements", {"FY2025": 375, "FY2024": 228, "FY2023": 2401, "FY2022": -878, "FY2021": -480}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Net (increase)/decrease in cash collateral and settlement balances", {"FY2025": -944, "FY2024": 414, "FY2023": 1108, "FY2022": 335, "FY2021": 322}),
    ("DATA", "Net (increase)/decrease in loans and advances at amortised cost", {"FY2025": -9592, "FY2024": 3023, "FY2023": 4402, "FY2022": 2893, "FY2021": -4591}),
    ("DATA", "Net (increase) in reverse repurchase agreements and other similar secured lending", {"FY2025": -107, "FY2024": -2327}),
    ("DATA", "Net (decrease)/increase in repurchase agreements and other similar secured borrowing", {"FY2025": -1906, "FY2024": 241}),
    ("DATA", "Repurchase and reverse repurchase agreements (combined, as reported)", {"FY2023": -5527, "FY2022": -870, "FY2021": 11050}),
    ("DATA", "Net increase/(decrease) in deposits at amortised cost", {"FY2025": 330, "FY2024": -3686, "FY2023": -17016, "FY2022": -2615, "FY2021": 20197}),
    ("DATA", "Net increase/(decrease) in debt securities in issue", {"FY2025": 2084, "FY2024": -1242, "FY2023": -4702, "FY2022": -675, "FY2021": 1181}),
    ("DATA", "Net decrease/(increase) in derivative financial instruments", {"FY2025": 906, "FY2024": -413, "FY2023": -1519, "FY2022": 427, "FY2021": -406}),
    ("DATA", "Net (increase) in trading portfolio assets", {"FY2025": -143, "FY2024": -199}),
    ("DATA", "Net increase/(decrease) in trading portfolio liabilities", {"FY2025": 182, "FY2024": -182}),
    ("DATA", "Trading assets and liabilities (combined, as reported)", {"FY2023": 455, "FY2022": -299, "FY2021": -258}),
    ("DATA", "Net decrease in financial assets at fair value through the income statement", {"FY2025": 130, "FY2024": 173}),
    ("DATA", "Net (decrease)/increase in financial liabilities designated at fair value", {"FY2025": -1845, "FY2024": 2652}),
    ("DATA", "Financial assets and liabilities at fair value through the income statement (combined, as reported)", {"FY2023": 264, "FY2022": 787, "FY2021": 665}),
    ("DATA", "Net (increase) in other assets and liabilities", {"FY2025": -215, "FY2024": -276, "FY2023": -52, "FY2022": -298, "FY2021": -299}),
    ("DATA", "Corporate income tax paid", {"FY2025": -1074, "FY2024": -522, "FY2023": -583, "FY2022": -395, "FY2021": -53}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": -7860, "FY2024": 1959, "FY2023": -17451, "FY2022": 1466, "FY2021": 29314}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities at amortised cost", {"FY2025": -3727, "FY2024": -4615}),
    ("DATA", "Proceeds from redemption or sale of debt securities at amortised cost", {"FY2025": 8061, "FY2024": 3932}),
    ("DATA", "Debt securities at amortised cost (net, as reported)", {"FY2023": -178, "FY2022": -5796, "FY2021": -3695}),
    ("DATA", "Purchase of financial assets at fair value through other comprehensive income", {"FY2025": -20764, "FY2024": -21343}),
    ("DATA", "Proceeds from sale or redemption of financial assets at fair value through other comprehensive income", {"FY2025": 16812, "FY2024": 14959}),
    ("DATA", "Financial assets at fair value through other comprehensive income (net, as reported)", {"FY2023": -304, "FY2022": -6792, "FY2021": 10125}),
    ("DATA", "Financial liabilities designated at fair value (net, as reported)", {"FY2023": 196, "FY2022": 0}),
    ("DATA", "Purchase of property, plant and equipment and investment in intangibles", {"FY2025": -52, "FY2024": -13, "FY2023": -25, "FY2022": -13, "FY2021": 0}),
    ("DATA", "Acquisition of business, net of cash acquired", {"FY2025": 0, "FY2024": -228}),
    ("DATA", "Acquisition of subsidiaries, net of cash acquired", {"FY2023": -2378, "FY2022": 0}),
    ("DATA", "Disposal of subsidiaries, net of cash disposed", {"FY2023": -141, "FY2022": 0}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": 330, "FY2024": -7308, "FY2023": -2830, "FY2022": -12601, "FY2021": 6430}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid and other coupon payments on equity instruments", {"FY2025": -1639, "FY2024": -1173, "FY2023": -1482, "FY2022": -1888, "FY2021": -683}),
    ("DATA", "Capital contribution from Barclays PLC", {"FY2021": 0}),
    ("DATA", "Issuance of subordinated liabilities/debt", {"FY2025": 3600, "FY2024": 2277, "FY2023": 4393, "FY2022": 829, "FY2021": 1025}),
    ("DATA", "Redemption of subordinated liabilities/debt", {"FY2025": -2703, "FY2024": -372, "FY2023": -1136, "FY2022": -2017, "FY2021": -1116}),
    ("DATA", "Issue of shares and other equity instruments", {"FY2025": 990, "FY2024": 618, "FY2023": 619, "FY2022": 0}),
    ("DATA", "Repurchase/redemption of shares and other equity instruments", {"FY2025": -1188, "FY2024": -622, "FY2023": -750, "FY2022": 0}),
    ("DATA", "Lease liability payments", {"FY2025": -41, "FY2024": -53, "FY2023": -63, "FY2022": -71}),
    ("DATA", "Vesting of employee share schemes", {"FY2025": -28, "FY2024": -15, "FY2023": -16, "FY2022": -14, "FY2021": -11}),
    ("DATA", "Effect of exchange rates on cash and cash equivalents", {"FY2021": 0}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": -1009, "FY2024": 660, "FY2023": 1565, "FY2022": -3161, "FY2021": -785}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -8539, "FY2024": -4689, "FY2023": -18716, "FY2022": -14296, "FY2021": 34959}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 35675, "FY2024": 40364, "FY2023": 59080, "FY2022": 73376, "FY2021": 38417}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 27136, "FY2024": 35675, "FY2023": 40364, "FY2022": 59080, "FY2021": 73376}),
    ("SECTION", "Cash and cash equivalents at end of year comprise", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 21208, "FY2024": 29819, "FY2023": 34948, "FY2022": 54208, "FY2021": 69488}),
    ("DATA", "Loans and advances to banks with original maturity less than three months", {"FY2025": 178, "FY2024": 231, "FY2023": 291, "FY2022": 347, "FY2021": 46}),
    ("DATA", "Cash collateral balances with central banks with original maturity less than three months", {"FY2025": 5750, "FY2024": 5625, "FY2023": 5125, "FY2022": 4525, "FY2021": 3842}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 27136, "FY2024": 35675, "FY2023": 40364, "FY2022": 59080, "FY2021": 73376}),
]

bw.add_cash_flow_sheet(
    title="Barclays Bank UK PLC — Consolidated Cash Flow Statement",
    subtitle="Barclays Bank UK Group (consolidated basis), £m unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=90,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Asset Quality: loans and advances at amortised cost by IFRS 9 stage
# (Group total; the underlying by-product breakdown uses different product
# taxonomies year to year - Home loans/Credit cards & other retail/Wholesale
# loans in FY2021 vs Retail mortgages/Retail credit cards/Retail other/
# Corporate loans FY2022-2025 - so only the always-comparable Total-level
# stage split is reproduced here, not a forced-equivalence product mapping.
# Figures exclude debt securities at amortised cost (a small, separately
# disclosed line not part of the loan book) for comparability across years.
# ---------------------------------------------------------------
AQ_STAGE1_GROSS = {"FY2025": 194856, "FY2024": 179441, "FY2023": 173805, "FY2022": 175260, "FY2021": 193961}
AQ_STAGE2_GROSS = {"FY2025": 19509, "FY2024": 25400, "FY2023": 26471, "FY2022": 27637, "FY2021": 24639}
AQ_STAGE3_GROSS = {"FY2025": 3121, "FY2024": 3482, "FY2023": 3375, "FY2022": 3482, "FY2021": 3850}
AQ_TOTAL_GROSS = {"FY2025": 217486, "FY2024": 208323, "FY2023": 203651, "FY2022": 206379, "FY2021": 222450}
AQ_STAGE1_ALLOW = {"FY2025": 323, "FY2024": 433, "FY2023": 295, "FY2022": 339, "FY2021": 395}
AQ_STAGE2_ALLOW = {"FY2025": 667, "FY2024": 679, "FY2023": 782, "FY2022": 815, "FY2021": 971}
AQ_STAGE3_ALLOW = {"FY2025": 634, "FY2024": 495, "FY2023": 579, "FY2022": 555, "FY2021": 813}
AQ_TOTAL_ALLOW = {"FY2025": 1624, "FY2024": 1607, "FY2023": 1656, "FY2022": 1709, "FY2021": 2179}
AQ_NPL_RATIO = {y: f"{AQ_STAGE3_GROSS[y] / AQ_TOTAL_GROSS[y] * 100:.1f}%" for y in YEARS}
AQ_STAGE3_COVERAGE = {y: f"{AQ_STAGE3_ALLOW[y] / AQ_STAGE3_GROSS[y] * 100:.1f}%" for y in YEARS}
AQ_TOTAL_COVERAGE = {y: f"{AQ_TOTAL_ALLOW[y] / AQ_TOTAL_GROSS[y] * 100:.1f}%" for y in YEARS}

asset_quality_rows = [
    ("SECTION", "Loans and advances at amortised cost, gross exposure by IFRS 9 stage", {}),
    ("DATA", "Stage 1", AQ_STAGE1_GROSS),
    ("DATA", "Stage 2", AQ_STAGE2_GROSS),
    ("DATA", "Stage 3 (incl. POCI where separately disclosed)", AQ_STAGE3_GROSS),
    ("TOTAL", "Total gross exposure", AQ_TOTAL_GROSS),
    ("SECTION", "Impairment allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1", AQ_STAGE1_ALLOW),
    ("DATA", "Stage 2", AQ_STAGE2_ALLOW),
    ("DATA", "Stage 3 (incl. POCI where separately disclosed)", AQ_STAGE3_ALLOW),
    ("TOTAL", "Total impairment allowance", AQ_TOTAL_ALLOW),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / total gross exposure)", AQ_NPL_RATIO),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross)", AQ_STAGE3_COVERAGE),
    ("DATA", "Total coverage ratio (total allowance / total gross exposure)", AQ_TOTAL_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="Barclays Bank UK PLC — Asset Quality / Credit Risk Disclosures",
    subtitle="Barclays Bank UK Group (consolidated basis), £m unless stated. Loans and advances at amortised "
             "cost, excluding debt securities at amortised cost.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources — Barclays Bank UK Group 'Loans and advances at amortised cost by product' tables "
        "('Total loans and advances at amortised cost' row, excl. debt securities):\n"
        f"FY2025: Annual Report 2025, p.103 — {AR25_URL}\n"
        f"FY2024: Annual Report 2025, p.104 (comparative) — {AR25_URL}\n"
        f"FY2023: Annual Report 2023, p.82 — {AR23_URL}\n"
        f"FY2022: Annual Report 2023, p.83 (comparative) — {AR23_URL}\n"
        f"FY2021: Annual Report 2021, p.66 — {AR21_URL}\n\n"
        "Note: NPL/coverage ratios are computed here (not the report's own headline ratio, though they tie closely "
        "to it - e.g. FY2021 Stage 3 coverage of 21.1% matches the report's own 'Total' Stage 3 coverage figure "
        "exactly). Product-level breakdown (e.g. mortgages vs. cards vs. corporate) isn't reproduced since the "
        "product taxonomy changed between FY2021 (Home loans / Credit cards & other retail / Wholesale loans) and "
        "FY2022-2025 (Retail mortgages / Retail credit cards / Retail other / Corporate loans) - see each year's "
        "own source page for the full by-product split."
    ),
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Consolidated basis, {unit}" if unit else "Consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=42, source_height=90)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 12331, "FY2024": 11895, "FY2023": 10638, "FY2022": 10701, "FY2021": 10828})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "14.5%", "FY2024": "14.2%", "FY2023": "14.8%", "FY2022": "14.7%", "FY2021": "15.2%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 14558, "FY2024": 14320, "FY2023": 13067, "FY2022": 13261, "FY2021": 13388})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "17.1%", "FY2024": "17.1%", "FY2023": "18.1%", "FY2022": "18.2%", "FY2021": "18.8%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 16996, "FY2024": 17155, "FY2023": 15596, "FY2022": 15828, "FY2021": 16442})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "20.0%", "FY2024": "20.5%", "FY2023": "21.6%", "FY2022": "21.8%", "FY2021": "23.1%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 85065, "FY2024": 83639, "FY2023": 72102, "FY2022": 72719, "FY2021": 71213})],
    p3_sources(),
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2025": 68166, "FY2024": 68018, "FY2023": 58174, "FY2022": 58885, "FY2021": 54981}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 300, "FY2024": 419, "FY2023": 541, "FY2022": 1083, "FY2021": 1208}),
    ("DATA", "Securitisation exposures (non-trading book, after cap)", {"FY2025": 2517, "FY2024": 1644, "FY2023": 1445, "FY2022": 1437, "FY2021": 1268}),
    ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2025": 177, "FY2024": 228, "FY2023": 274, "FY2022": 233, "FY2021": 100}),
    ("DATA", "Operational risk", {"FY2025": 13905, "FY2024": 13330, "FY2023": 11668, "FY2022": 11081, "FY2021": 10892}),
    ("DATA", "Amounts below thresholds for deduction (subject to 250% risk weight)", {"FY2025": 2309, "FY2024": 2271, "FY2023": 2314, "FY2022": 2704, "FY2021": 2764}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 85065, "FY2024": 83639, "FY2023": 72102, "FY2022": 72719, "FY2021": 71213}),
]

bw.add_rwa_breakdown_sheet(
    title="Barclays Bank UK PLC — RWA Breakdown",
    subtitle="Barclays Bank UK Group (consolidated basis), £m",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(part_label_25="Table 10: OV1 - Overview of risk weighted exposure amounts", page_25="16-17",
                             part_label_23="Table 10: OV1 - Overview of risk weighted exposure amounts", page_23="16-17",
                             part_label_21="Table 8: OV1 - Overview of risk weighted assets by risk type and capital requirements", page_21="12-13"),
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks (£m)", {"FY2025": 277958, "FY2024": 268452, "FY2023": 250163, "FY2022": 250092, "FY2021": 241173}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "5.2%", "FY2024": "5.3%", "FY2023": "5.2%", "FY2022": "5.3%", "FY2021": "5.6%"}),
        ("Leverage ratio including claims on central banks (%)", {"FY2025": "4.8%", "FY2024": "4.7%", "FY2023": "4.5%", "FY2022": "4.3%", "FY2021": "4.1%"}),
    ],
    p3_sources(part_label_25="Table 6: KM1 - Key metrics - Part 2", page_25="12",
               part_label_23="Table 6: KM1 - Key metrics - Part 2", page_23="12",
               part_label_21="Table 4: Key Metrics (KM1 / IFRS 9-FL)", page_21="9"),
    note="FY2021 exposure/ratios use the 'UK leverage ratio (Transitional)' and 'CRR leverage ratio (Transitional)' rows "
         "from the 2021 Pillar 3 report as the closest equivalents to the 'excluding'/'including claims on central banks' "
         "framing introduced in later reports.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (£m)", {"FY2025": 64552, "FY2024": 68446, "FY2023": 68533, "FY2022": 81791, "FY2021": 85092}),
        ("Total net cash outflows, adjusted value (£m)", {"FY2025": 34613, "FY2024": 33879, "FY2023": 38057, "FY2022": 43966, "FY2021": 41690}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "186.6%", "FY2024": "202.0%", "FY2023": "180%", "FY2022": "186%", "FY2021": "204%"}),
    ],
    p3_sources(part_label_25="Table 6: KM1 - Key metrics - Part 2", page_25="12",
               part_label_23="Table 6: KM1 - Key metrics - Part 2", page_23="12",
               part_label_21="Table 4: Key Metrics (KM1 / IFRS 9-FL)", page_21="9"),
    note="LCR is computed as a trailing average of the last 12 month-end observations.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2025": 257230, "FY2024": 254755, "FY2023": 258620, "FY2022": 266421}),
        ("Total required stable funding (£m)", {"FY2025": 168761, "FY2024": 160041, "FY2023": 156588, "FY2022": 158156}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "152.4%", "FY2024": "159.3%", "FY2023": "165%", "FY2022": "168%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(part_label_25="Table 6: KM1 - Key metrics - Part 2", page_25="12",
               part_label_23="Table 6: KM1 - Key metrics - Part 2", page_23="12",
               part_label_21="Table 4: Key Metrics (KM1 / IFRS 9-FL)", page_21="9"),
    note="NSFR is computed as a trailing average of the last four spot quarter-end positions. It was not a Pillar 3 "
         "disclosure requirement as at FY2021 (the UK NSFR regime took effect from 1 January 2022), so no FY2021 figures "
         "are available.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed at this level" for y in YEARS})],
    p3_sources(),
    note="MREL disclosures are not applicable for Barclays Bank UK Group (the ring-fenced entity) in any of the five "
         "years reviewed; MREL is disclosed at the Barclays PLC group level instead (see Barclays PLC Pillar 3 Report, "
         "Table 21: TLAC2).",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 302824, "FY2024": 303179, "FY2023": 293559, "FY2022": 312179, "FY2021": 319695}),
        ("Loans and advances at amortised cost to customers", {"FY2025": 215634, "FY2024": 206435, "FY2023": 200782, "FY2022": 203279, "FY2021": 220271}),
        ("Deposits at amortised cost from customers", {"FY2025": 244666, "FY2024": 244376, "FY2023": 241218, "FY2022": 258058, "FY2021": 260732}),
        ("Total equity", {"FY2025": 20278, "FY2024": 18585, "FY2023": 16861, "FY2022": 15413, "FY2021": 17400}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 8811, "FY2024": 8423, "FY2023": 7670, "FY2022": 7397, "FY2021": 6482}),
        ("Operating expenses", {"FY2025": -5093, "FY2024": -4511, "FY2023": -4567, "FY2022": -4577, "FY2021": -4691}),
        ("Profit after tax", {"FY2025": 2594, "FY2024": 2620, "FY2023": 1922, "FY2022": 1807, "FY2021": 1869}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 18585, "FY2024": 16861, "FY2023": 15413, "FY2022": 17400, "FY2021": 17027}),
        ("Total comprehensive income for the year", {"FY2025": 3498, "FY2024": 2875, "FY2023": 3050, "FY2022": -106, "FY2021": 1030}),
        ("Other movements, net", {"FY2025": -1805, "FY2024": -1151, "FY2023": -1602, "FY2022": -1881, "FY2021": -657}),
        ("Closing equity", {"FY2025": 20278, "FY2024": 18585, "FY2023": 16861, "FY2022": 15413, "FY2021": 17400}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": -7860, "FY2024": 1959, "FY2023": -17451, "FY2022": 1466, "FY2021": 29314}),
        ("Net cash from investing activities", {"FY2025": 330, "FY2024": -7308, "FY2023": -2830, "FY2022": -12601, "FY2021": 6430}),
        ("Net cash from financing activities", {"FY2025": -1009, "FY2024": 660, "FY2023": 1565, "FY2022": -3161, "FY2021": -785}),
        ("Cash and cash equivalents at end of year", {"FY2025": 27136, "FY2024": 35675, "FY2023": 40364, "FY2022": 59080, "FY2021": 73376}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "14.5%", "FY2024": "14.2%", "FY2023": "14.8%", "FY2022": "14.7%", "FY2021": "15.2%"}),
        ("Tier 1 Ratio", {"FY2025": "17.1%", "FY2024": "17.1%", "FY2023": "18.1%", "FY2022": "18.2%", "FY2021": "18.8%"}),
        ("Total Capital Ratio", {"FY2025": "20.0%", "FY2024": "20.5%", "FY2023": "21.6%", "FY2022": "21.8%", "FY2021": "23.1%"}),
        ("Leverage Ratio", {"FY2025": "5.2%", "FY2024": "5.3%", "FY2023": "5.2%", "FY2022": "5.3%", "FY2021": "5.6%"}),
        ("LCR", {"FY2025": "186.6%", "FY2024": "202.0%", "FY2023": "180%", "FY2022": "186%", "FY2021": "204%"}),
        ("NSFR", {"FY2025": "152.4%", "FY2024": "159.3%", "FY2023": "165%", "FY2022": "168%", "FY2021": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Leverage ratio shown on the 'excluding claims on "
         "central banks' basis for comparability across years (see Leverage Ratio sheet for the 'including' "
         "variant and FY2021 basis note).",
)

bw.save("/Users/armaan/code/katalysis/banks/BARCLAYS FINANCIALS.xlsx")
