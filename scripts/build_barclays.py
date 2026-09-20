import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018"]  # most recent first
# HD-019: extended back to FY2018 (confirmed true floor per HD-001's deep dive - Barclays Bank UK
# PLC was incorporated in 2015 but did not begin operating as the ring-fenced retail bank until
# April 2018; FY2015-FY2017 predate this entity's operation in its current form and are
# deliberately NOT sourced or transcribed).

AR25_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2025/Barclays-Bank-UK-PLC-Annual-Report-2025.pdf"
AR23_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2023/Barclays-Bank-UK-Annual-Report-2023-Results-committee.pdf"
AR21_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2021/Barclays-Bank-UK-PLC-2021-Annual-Report.pdf"
AR20_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2020/Barclays-Bank-UK-PLC-2020-Annual-Report.pdf"
AR19_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2019/Barclays%20Bank%20UK%20PLC%20Annual%20Report%202019.pdf"
AR18_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2018/2018-barclays-bank-uk-plc-annual-report.pdf"

P3_25_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/ResultAnnouncements/FullYear2025Results/FY25-BBUKPLC-Pillar-3.pdf"
P3_23_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2023/BB-UK-Pillar-3-Report-2023.pdf"
P3_21_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2021/Barclays-Bank-UK-PLC-Pillar-3-Report-2021.pdf"
P3_20_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2020/Barclays%20Bank%20UK%20PLC%20Pillar%203%20Report%202020.pdf"
P3_19_URL = "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2019/Barclays%20Bank%20UK%20PLC%20Pillar%203%20Report.pdf"
# Note: Barclays Bank UK PLC did not publish its own standalone Pillar 3 report for FY2018 - the
# entity was only regulated by the PRA on an individual basis from its April 2018 stand-up, and its
# first dedicated Pillar 3 report is FY2019's (see P3_19_URL above). For FY2018, the equivalent key
# capital/leverage/liquidity metrics were instead disclosed directly within the FY2018 Annual
# Report's "Capital risk" and "Liquidity risk" sections (AR18_URL, pp.80/74) - see each FY2018
# metric sheet's own source note for the exact page reference. No RWA-by-risk-type (OV1-style)
# breakdown is available for FY2018 at the BBUKPLC entity level for this reason.

CASH_FLOW_SOURCES = (
    "Sources — all figures are Barclays Bank UK Group consolidated cash flow statement, £m:\n"
    f"FY2025 & FY2024: Barclays Bank UK PLC Annual Report 2025, p.201 (Consolidated cash flow statement) — {AR25_URL}\n"
    f"FY2023 & FY2022: Barclays Bank UK PLC Annual Report 2023, p.166 (Consolidated cash flow statement) — {AR23_URL}\n"
    f"FY2021: Barclays Bank UK PLC Annual Report 2021, p.138 (Consolidated cash flow statement) — {AR21_URL}\n"
    f"FY2020: Barclays Bank UK PLC Annual Report 2020, p.127 (Consolidated cash flow statement) — {AR20_URL}\n"
    f"FY2019: Barclays Bank UK PLC Annual Report 2019, p.108 (Consolidated cash flow statement) — {AR19_URL}\n"
    f"FY2018: Barclays Bank UK PLC Annual Report 2018, p.109 (Consolidated cash flow statement) — {AR18_URL}\n"
    "Note: Barclays changed cash flow statement presentation granularity across these report vintages "
    "(e.g. FY2025/FY2024 split some line items — such as repurchase/reverse repurchase agreements and trading "
    "portfolio assets/liabilities — that FY2023/FY2022/FY2021 report on a combined basis; FY2019/FY2018 combined "
    "deposits and debt securities in issue into one movement, a split FY2020 onward reports separately). Blank "
    "cells indicate that year's report did not disclose that specific split; where a coarser combined figure was "
    "reported instead, it appears on its own row. Each year's figures are exactly as originally reported in that "
    "year's own Annual Report (not a later restated comparative) - Barclays subsequently restated FY2019's cash "
    "flow presentation (reclassifying cash collateral within cash and cash equivalents, reducing the FY2019 and "
    "FY2018 closing cash balances by £532m and £409m respectively) and separately restated FY2018's other "
    "non-cash movements for an exchange-rate effects disclosure introduced from FY2019; as a result FY2018's own "
    "reported closing cash balance (£44,334m), FY2019's own reported closing balance (£28,042m), and FY2020's own "
    "reported opening balance (£27,510m, i.e. the restated FY2019 closing position) do not exactly chain together "
    "- each is reproduced as originally published, consistent with this workbook's sourcing convention throughout. "
    "Section totals (net cash from operating/investing/financing activities, cash and cash equivalents) are "
    "otherwise consistent and comparable across all 8 years."
)

def p3_sources(part_label_25="Table 6: KM1 - Key metrics - Part 1", page_25="11",
               part_label_23="Table 6: UK KM1 - Key metrics - Part 1", page_23="11",
               part_label_21="Table 4: Key Metrics (KM1 / IFRS 9-FL)", page_21="9",
               # CITATION CORRECTED 2026-09-16 (KM1-007): these two were "7". The Key Metrics table is on
               # printed page 8 of BOTH the FY2019 and FY2020 reports - each page's own footer reads
               # "Barclays Bank UK PLC Pillar 3 report 2019   8" (and ...2020   8), with the preceding and
               # following sheets footed 7 and 9, so the folio matches the PDF sheet index in these
               # editions. The same wrong page number appeared in two places in this file; both fixed.
               part_label_20="Table 4: Key Metrics (KM1/IFRS 9-FL)", page_20="8",
               part_label_19="Table 4: Key Metrics (KM1/IFRS9-FL)", page_19="8",
               part_label_18="Annual Report 2018 capital risk disclosures (no standalone Pillar 3 report)", page_18="80"):
    return (
        "Sources — Barclays Bank UK Group consolidated (Pillar 3) basis:\n"
        f"FY2025 & FY2024: Barclays Bank UK PLC Pillar 3 Report 2025, p.{page_25} ({part_label_25}) — {P3_25_URL}\n"
        f"FY2023 & FY2022: Barclays Bank UK PLC Pillar 3 Report 2023, p.{page_23} ({part_label_23}) — {P3_23_URL}\n"
        f"FY2021: Barclays Bank UK PLC Pillar 3 Report 2021, p.{page_21} ({part_label_21}) — {P3_21_URL}\n"
        f"FY2020: Barclays Bank UK PLC Pillar 3 Report 2020, p.{page_20} ({part_label_20}) — {P3_20_URL}\n"
        f"FY2019: Barclays Bank UK PLC Pillar 3 Report 2019, p.{page_19} ({part_label_19}) — {P3_19_URL}\n"
        f"FY2018: Barclays Bank UK PLC Annual Report 2018, p.{page_18} ({part_label_18}) — {AR18_URL}"
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
    f"FY2020: Barclays Bank UK PLC Annual Report 2020, pp.123 (income statement), 125 (balance sheet), "
    f"126 (statement of changes in equity) — {AR20_URL}\n"
    f"FY2019: Barclays Bank UK PLC Annual Report 2019, pp.104 (income statement), 106 (balance sheet), "
    f"107 (statement of changes in equity) — {AR19_URL}\n"
    f"FY2018: Barclays Bank UK PLC Annual Report 2018, pp.105 (income statement), 107 (balance sheet), "
    f"108 (statement of changes in equity) — {AR18_URL}\n"
    "Balance sheet note: FY2018-FY2021 do not split loans and advances at amortised cost into a bank/customer "
    "split, do not disclose a separate debt securities at amortised cost line, and report deposits at amortised "
    "cost as a single combined line - the combined figures appear on their own row for those years only; "
    "FY2022-2025 all split these. FY2020 is the only year with a separate 'Current tax assets' line (a small net "
    "asset position; other years report a nil/immaterial current tax asset position folded into other lines). "
    "Income statement note: FY2018-FY2021 place credit impairment charges/(releases) before operating expenses "
    "(subtotalled as 'Net operating income'), while FY2022-2025 place it after operating expenses (subtotalled as "
    "'Profit before impairment') - a genuine presentation restructuring, not a transcription error; each year's own "
    "subtotals are reproduced as reported. FY2020 and FY2021 both separately disclose a 'Profit on disposal of "
    "subsidiaries, associates and joint ventures' line before profit before tax. Figures for FY2018-FY2020 are "
    "each reproduced exactly as originally reported in that year's own Annual Report, not as later restated "
    "comparatives (e.g. Barclays restated FY2018's tax charge by £28m from FY2019 onward following an IAS 12 "
    "update on AT1 coupon tax relief) - consistent with this workbook's sourcing convention throughout."
)

# ---------------------------------------------------------------
# Balance Sheet (Consolidated Statement of Financial Position), £m
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 21208, "FY2024": 29819, "FY2023": 34948, "FY2022": 54208, "FY2021": 69488, "FY2020": 35218, "FY2019": 24305, "FY2018": 40669}),
    ("DATA", "Cash collateral and settlement balances", {"FY2025": 6120, "FY2024": 6002, "FY2023": 5507, "FY2022": 5194, "FY2021": 5067, "FY2020": 4345, "FY2019": 4331, "FY2018": 3349}),
    ("DATA", "Debt securities at amortised cost", {"FY2025": 13492, "FY2024": 17983, "FY2023": 17794, "FY2022": 18537}),
    ("DATA", "Loans and advances at amortised cost to banks", {"FY2025": 228, "FY2024": 281, "FY2023": 1213, "FY2022": 1391}),
    ("DATA", "Loans and advances at amortised cost to customers", {"FY2025": 215634, "FY2024": 206435, "FY2023": 200782, "FY2022": 203279}),
    ("DATA", "Loans and advances at amortised cost (combined, as reported)", {"FY2021": 220271, "FY2020": 211649, "FY2019": 197569, "FY2018": 188565}),
    ("DATA", "Reverse repurchase agreements and other similar secured lending at amortised cost", {"FY2025": 6001, "FY2024": 5894, "FY2023": 3567, "FY2022": 477, "FY2021": 65, "FY2020": 133, "FY2019": 1761, "FY2018": 1759}),
    ("DATA", "Trading portfolio assets", {"FY2025": 385, "FY2024": 242, "FY2023": 43, "FY2022": 54, "FY2021": 169, "FY2020": 298, "FY2019": 860, "FY2018": 151}),
    ("DATA", "Financial assets at fair value through the income statement", {"FY2025": 1413, "FY2024": 1543, "FY2023": 1716, "FY2022": 1980, "FY2021": 2767, "FY2020": 3432, "FY2019": 3571, "FY2018": 3880}),
    ("DATA", "Derivative financial instruments", {"FY2025": 890, "FY2024": 1901, "FY2023": 1566, "FY2022": 611, "FY2021": 890, "FY2020": 550, "FY2019": 192, "FY2018": 241}),
    ("DATA", "Financial assets at fair value through other comprehensive income", {"FY2025": 31572, "FY2024": 27045, "FY2023": 20409, "FY2022": 19970, "FY2021": 14945, "FY2020": 26026, "FY2019": 19322, "FY2018": 6710}),
    ("DATA", "Goodwill and intangible assets", {"FY2025": 3933, "FY2024": 3948, "FY2023": 3870, "FY2022": 3528, "FY2021": 3526, "FY2020": 3527, "FY2019": 3530, "FY2018": 3534}),
    ("DATA", "Property, plant and equipment", {"FY2025": 287, "FY2024": 239, "FY2023": 261, "FY2022": 382, "FY2021": 562, "FY2020": 737, "FY2019": 893, "FY2018": 498}),
    ("DATA", "Current tax assets", {"FY2020": 75}),
    ("DATA", "Deferred tax assets", {"FY2025": 884, "FY2024": 1212, "FY2023": 1296, "FY2022": 1916, "FY2021": 1368, "FY2020": 780, "FY2019": 810, "FY2018": 792}),
    ("DATA", "Retirement benefit assets", {"FY2025": 69}),
    ("DATA", "Other assets", {"FY2025": 708, "FY2024": 635, "FY2023": 587, "FY2022": 652, "FY2021": 577, "FY2020": 728, "FY2019": 1254, "FY2018": 1157}),
    ("TOTAL", "Total assets", {"FY2025": 302824, "FY2024": 303179, "FY2023": 293559, "FY2022": 312179, "FY2021": 319695, "FY2020": 287498, "FY2019": 258398, "FY2018": 251305}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits at amortised cost from banks", {"FY2025": 125, "FY2024": 85, "FY2023": 6, "FY2022": 59}),
    ("DATA", "Deposits at amortised cost from customers", {"FY2025": 244666, "FY2024": 244376, "FY2023": 241218, "FY2022": 258058}),
    ("DATA", "Deposits at amortised cost (combined, as reported)", {"FY2021": 260732, "FY2020": 240535, "FY2019": 205696, "FY2018": 197485}),
    ("DATA", "Cash collateral and settlement balances", {"FY2025": 828, "FY2024": 1779, "FY2023": 1370, "FY2022": 553, "FY2021": 774, "FY2020": 455, "FY2019": 214, "FY2018": 239}),
    ("DATA", "Repurchase agreements and other similar secured borrowing at amortised cost", {"FY2025": 13600, "FY2024": 15506, "FY2023": 15265, "FY2022": 17702, "FY2021": 18160, "FY2020": 7178, "FY2019": 13420, "FY2018": 11978}),
    ("DATA", "Debt securities in issue", {"FY2025": 4703, "FY2024": 2619, "FY2023": 3307, "FY2022": 8009, "FY2021": 8684, "FY2020": 7503, "FY2019": 8271, "FY2018": 11172}),
    ("DATA", "Subordinated liabilities", {"FY2025": 14049, "FY2024": 13512, "FY2023": 11499, "FY2022": 8268, "FY2021": 9516, "FY2020": 9869, "FY2019": 7688, "FY2018": 7548}),
    ("DATA", "Trading portfolio liabilities", {"FY2025": 908, "FY2024": 726, "FY2023": 908, "FY2022": 464, "FY2021": 878, "FY2020": 1265, "FY2019": 1704, "FY2018": 1269}),
    ("DATA", "Financial liabilities designated at fair value", {"FY2025": 1003, "FY2024": 2848, "FY2023": 196}),
    ("DATA", "Derivative financial instruments", {"FY2025": 195, "FY2024": 300, "FY2023": 398, "FY2022": 962, "FY2021": 814, "FY2020": 880, "FY2019": 740, "FY2018": 419}),
    ("DATA", "Current tax liabilities", {"FY2025": 598, "FY2024": 954, "FY2023": 540, "FY2022": 578, "FY2021": 377, "FY2020": 0, "FY2019": 458, "FY2018": 984}),
    ("DATA", "Provisions", {"FY2025": 364, "FY2024": 323, "FY2023": 364, "FY2022": 338, "FY2021": 536, "FY2020": 880, "FY2019": 1660, "FY2018": 1380}),
    ("DATA", "Other liabilities", {"FY2025": 1507, "FY2024": 1566, "FY2023": 1627, "FY2022": 1775, "FY2021": 1824, "FY2020": 1906, "FY2019": 2034, "FY2018": 1888}),
    ("TOTAL", "Total liabilities", {"FY2025": 282546, "FY2024": 284594, "FY2023": 276698, "FY2022": 296766, "FY2021": 302295, "FY2020": 270471, "FY2019": 241885, "FY2018": 234362}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital and share premium", {"FY2025": 5, "FY2024": 5, "FY2023": 5, "FY2022": 5, "FY2021": 5, "FY2020": 5, "FY2019": 5, "FY2018": 5}),
    ("DATA", "Other equity instruments", {"FY2025": 2227, "FY2024": 2425, "FY2023": 2429, "FY2022": 2560, "FY2021": 2560, "FY2020": 2560, "FY2019": 2560, "FY2018": 2070}),
    ("DATA", "Other reserves", {"FY2025": -38, "FY2024": -896, "FY2023": -1151, "FY2022": -2279, "FY2021": -366, "FY2020": 473, "FY2019": 183, "FY2018": 76}),
    ("DATA", "Retained earnings", {"FY2025": 18084, "FY2024": 17051, "FY2023": 15578, "FY2022": 15127, "FY2021": 15201, "FY2020": 13989, "FY2019": 13765, "FY2018": 14792}),
    ("TOTAL", "Total equity", {"FY2025": 20278, "FY2024": 18585, "FY2023": 16861, "FY2022": 15413, "FY2021": 17400, "FY2020": 17027, "FY2019": 16513, "FY2018": 16943}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 302824, "FY2024": 303179, "FY2023": 293559, "FY2022": 312179, "FY2021": 319695, "FY2020": 287498, "FY2019": 258398, "FY2018": 251305}),
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
    ("DATA", "Interest and similar income", {"FY2025": 13136, "FY2024": 12588, "FY2023": 11024, "FY2022": 6981, "FY2021": 5775, "FY2020": 6201, "FY2019": 7218, "FY2018": 5267}),
    ("DATA", "Interest and similar expense", {"FY2025": -5371, "FY2024": -5851, "FY2023": -4597, "FY2022": -1340, "FY2021": -769, "FY2020": -1021, "FY2019": -1413, "FY2018": -830}),
    ("TOTAL", "Net interest income", {"FY2025": 7765, "FY2024": 6737, "FY2023": 6427, "FY2022": 5641, "FY2021": 5006, "FY2020": 5180, "FY2019": 5805, "FY2018": 4437}),
    ("DATA", "Fee and commission income", {"FY2025": 1565, "FY2024": 1507, "FY2023": 1605, "FY2022": 1689, "FY2021": 1466, "FY2020": 1375, "FY2019": 1674, "FY2018": 1315}),
    ("DATA", "Fee and commission expense", {"FY2025": -482, "FY2024": -411, "FY2023": -370, "FY2022": -322, "FY2021": -219, "FY2020": -310, "FY2019": -368, "FY2018": -273}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 1083, "FY2024": 1096, "FY2023": 1235, "FY2022": 1367, "FY2021": 1247, "FY2020": 1065, "FY2019": 1306, "FY2018": 1042}),
    ("DATA", "Net trading income/(expense)", {"FY2025": -48, "FY2024": -16, "FY2023": 35, "FY2022": 385, "FY2021": 40, "FY2020": 53, "FY2019": 33, "FY2018": 30}),
    ("DATA", "Net investment income/(expense)", {"FY2025": -7, "FY2024": 41, "FY2023": -91, "FY2022": 1, "FY2021": 181, "FY2020": 106, "FY2019": 172, "FY2018": 86}),
    ("DATA", "Gain on acquisition", {"FY2025": 0, "FY2024": 558}),
    ("DATA", "Other income", {"FY2025": 18, "FY2024": 7, "FY2023": 64, "FY2022": 3, "FY2021": 8, "FY2020": 20, "FY2019": 6, "FY2018": 11}),
    ("TOTAL", "Total income", {"FY2025": 8811, "FY2024": 8423, "FY2023": 7670, "FY2022": 7397, "FY2021": 6482, "FY2020": 6424, "FY2019": 7322, "FY2018": 5606}),
    ("DATA", "Credit impairment releases/(charges) (pre-opex, FY2018-FY2021)", {"FY2021": 371, "FY2020": -1427, "FY2019": -709, "FY2018": -624}),
    ("TOTAL", "Net operating income (FY2018-FY2021)", {"FY2021": 6853, "FY2020": 4997, "FY2019": 6613, "FY2018": 4982}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -1555, "FY2024": -1215, "FY2023": -1209, "FY2022": -1170, "FY2021": -1392, "FY2020": -1311, "FY2019": -1252, "FY2018": -1016}),
    ("DATA", "Infrastructure costs", {"FY2025": -300, "FY2024": -258, "FY2023": -343, "FY2022": -385, "FY2021": -389, "FY2020": -444, "FY2019": -382, "FY2018": -307}),
    ("DATA", "Administration and general expenses", {"FY2025": -3104, "FY2024": -2939, "FY2023": -3024, "FY2022": -2977, "FY2021": -2859, "FY2020": -2848, "FY2019": -2724, "FY2018": -2033}),
    ("DATA", "UK regulatory levies", {"FY2025": -85, "FY2024": -78}),
    ("DATA", "Litigation and conduct / provisions for litigation and conduct", {"FY2025": -49, "FY2024": -21, "FY2023": 9, "FY2022": -45, "FY2021": -51, "FY2020": -43, "FY2019": -1586, "FY2018": -78}),
    ("TOTAL", "Operating expenses", {"FY2025": -5093, "FY2024": -4511, "FY2023": -4567, "FY2022": -4577, "FY2021": -4691, "FY2020": -4646, "FY2019": -5944, "FY2018": -3434}),
    ("DATA", "Loss on disposal of subsidiaries, associates and joint ventures", {"FY2023": -124, "FY2022": 0}),
    ("DATA", "Profit on disposal of subsidiaries, associates and joint ventures (FY2020-FY2021 only)", {"FY2021": 1, "FY2020": 16}),
    ("TOTAL", "Profit before impairment (FY2022-FY2025 only)", {"FY2025": 3718, "FY2024": 3912, "FY2023": 2979, "FY2022": 2820}),
    ("DATA", "Credit impairment (charges)/releases (post-opex, FY2022-FY2025)", {"FY2025": -393, "FY2024": -352, "FY2023": -308, "FY2022": -268}),
    ("TOTAL", "Profit before tax", {"FY2025": 3325, "FY2024": 3560, "FY2023": 2671, "FY2022": 2552, "FY2021": 2163, "FY2020": 367, "FY2019": 669, "FY2018": 1548}),
    ("DATA", "Taxation", {"FY2025": -731, "FY2024": -940, "FY2023": -749, "FY2022": -745, "FY2021": -294, "FY2020": 12, "FY2019": -513, "FY2018": -433}),
    ("TOTAL", "Profit after tax", {"FY2025": 2594, "FY2024": 2620, "FY2023": 1922, "FY2022": 1807, "FY2021": 1869, "FY2020": 379, "FY2019": 156, "FY2018": 1115}),
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
    ("TOTAL", "Balance as at 1 January 2018", (5, 0, 20, 21, 46)),
    ("DATA", "Profit after tax", (None, 105, None, 1010, 1115)),
    ("DATA", "Financial assets at FVOCI reserve movement", (None, None, -17, None, -17)),
    ("DATA", "Cash flow hedges", (None, None, 20, None, 20)),
    ("TOTAL", "Total comprehensive income for the year (FY2018)", (None, 105, 3, 1010, 1118)),
    ("DATA", "Issue of new ordinary shares", (13044, None, None, None, 13044)),
    ("DATA", "Equity settled share schemes", (None, None, None, 19, 19)),
    ("DATA", "Net equity impact of the UK banking business transfer", (None, 2070, 53, 46, 2169)),
    ("DATA", "Capital reorganisation", (-13044, None, None, 13044, 0)),
    ("DATA", "Other equity instruments coupons paid", (None, -105, None, 28, -77)),
    ("DATA", "Vesting of employee share schemes", (None, None, None, -10, -10)),
    ("DATA", "Dividends paid", (None, None, None, -350, -350)),
    ("DATA", "Capital contribution from Barclays Bank PLC", (None, None, None, 983, 983)),
    ("DATA", "Other reserve movements", (None, None, None, 1, 1)),
    ("TOTAL", "Balance as at 31 December 2018", (5, 2070, 76, 14792, 16943)),
    ("DATA", "Profit after tax", (None, 153, None, 3, 156)),
    ("DATA", "Financial assets at FVOCI reserve movement", (None, None, 4, None, 4)),
    ("DATA", "Cash flow hedges", (None, None, 103, None, 103)),
    ("TOTAL", "Total comprehensive income for the year (FY2019)", (None, 153, 107, 3, 263)),
    ("DATA", "Issue and exchange of other equity instruments", (None, 490, None, None, 490)),
    ("DATA", "Equity settled share schemes", (None, None, None, 32, 32)),
    ("DATA", "Other equity instruments coupons paid", (None, -153, None, None, -153)),
    ("DATA", "Vesting of employee share schemes", (None, None, None, -12, -12)),
    ("DATA", "Dividends paid", (None, None, None, -1050, -1050)),
    ("TOTAL", "Balance as at 31 December 2019", (5, 2560, 183, 13765, 16513)),
    ("DATA", "Profit after tax", (None, 180, None, 199, 379)),
    ("DATA", "Financial assets at FVOCI reserve movement", (None, None, 72, None, 72)),
    ("DATA", "Cash flow hedges", (None, None, 218, None, 218)),
    ("DATA", "Other", (None, None, None, 1, 1)),
    ("TOTAL", "Total comprehensive income for the year (FY2020)", (None, 180, 290, 200, 670)),
    ("DATA", "Equity settled share schemes", (None, None, None, 31, 31)),
    ("DATA", "Other equity instruments coupons paid", (None, -180, None, None, -180)),
    ("DATA", "Vesting of employee share schemes", (None, None, None, -12, -12)),
    ("DATA", "Dividends paid", (None, None, None, -220, -220)),
    ("DATA", "Capital contribution from Barclays PLC", (None, None, None, 220, 220)),
    ("DATA", "Other reserve movements", (None, None, None, 5, 5)),
    ("TOTAL", "Balance as at 31 December 2020 / 1 January 2021", (5, 2560, 473, 13989, 17027)),
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
    ("DATA", "Profit before tax", {"FY2025": 3325, "FY2024": 3560, "FY2023": 2671, "FY2022": 2552, "FY2021": 2163, "FY2020": 367, "FY2019": 669, "FY2018": 1548}),
    ("DATA", "Credit impairment charges/(releases)", {"FY2025": 393, "FY2024": 352, "FY2023": 308, "FY2022": 268, "FY2021": -371, "FY2020": 1427, "FY2019": 709, "FY2018": 624}),
    ("DATA", "Depreciation, amortisation and impairment of property, plant, equipment and intangibles", {"FY2025": 97, "FY2024": 95, "FY2023": 146, "FY2022": 187, "FY2021": 169, "FY2020": 175, "FY2019": 150, "FY2018": 50}),
    ("DATA", "Loss on disposal of subsidiaries", {"FY2023": 124, "FY2022": 0}),
    ("DATA", "Other provisions (including pensions where noted)", {"FY2025": 144, "FY2024": 68, "FY2023": 69, "FY2022": 47, "FY2021": 25, "FY2020": 427, "FY2019": 1665, "FY2018": 104}),
    ("DATA", "Other non-cash items / exchange rate movements", {"FY2025": 375, "FY2024": 228, "FY2023": 2401, "FY2022": -878, "FY2021": -480, "FY2020": -1217, "FY2019": 110, "FY2018": -39}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Net (increase)/decrease in cash collateral and settlement balances", {"FY2025": -944, "FY2024": 414, "FY2023": 1108, "FY2022": 335, "FY2021": 322, "FY2020": 227, "FY2019": -531, "FY2018": -130}),
    ("DATA", "Net (increase)/decrease in loans and advances at amortised cost", {"FY2025": -9592, "FY2024": 3023, "FY2023": 4402, "FY2022": 2893, "FY2021": -4591, "FY2020": -15513, "FY2019": -10117, "FY2018": -4022}),
    ("DATA", "Net (increase) in reverse repurchase agreements and other similar secured lending", {"FY2025": -107, "FY2024": -2327, "FY2018": -421}),
    ("DATA", "Net (decrease)/increase in repurchase agreements and other similar secured borrowing", {"FY2025": -1906, "FY2024": 241, "FY2018": -171}),
    ("DATA", "Repurchase and reverse repurchase agreements (combined, as reported)", {"FY2023": -5527, "FY2022": -870, "FY2021": 11050, "FY2020": -4614, "FY2019": 1440}),
    ("DATA", "Net increase/(decrease) in deposits at amortised cost", {"FY2025": 330, "FY2024": -3686, "FY2023": -17016, "FY2022": -2615, "FY2021": 20197, "FY2020": 34839}),
    ("DATA", "Net increase/(decrease) in debt securities in issue", {"FY2025": 2084, "FY2024": -1242, "FY2023": -4702, "FY2022": -675, "FY2021": 1181, "FY2020": -768}),
    ("DATA", "Net increase in deposits and debt securities in issue (combined, as reported)", {"FY2019": 5310, "FY2018": 6532}),
    ("DATA", "Net decrease/(increase) in derivative financial instruments", {"FY2025": 906, "FY2024": -413, "FY2023": -1519, "FY2022": 427, "FY2021": -406, "FY2020": -218, "FY2019": 370, "FY2018": -5854}),
    ("DATA", "Net (increase) in trading portfolio assets", {"FY2025": -143, "FY2024": -199, "FY2018": -151}),
    ("DATA", "Net increase/(decrease) in trading portfolio liabilities", {"FY2025": 182, "FY2024": -182, "FY2018": -496}),
    ("DATA", "Trading assets and liabilities (combined, as reported)", {"FY2023": 455, "FY2022": -299, "FY2021": -258, "FY2020": 123, "FY2019": -274}),
    ("DATA", "Net decrease in financial assets at fair value through the income statement", {"FY2025": 130, "FY2024": 173}),
    ("DATA", "Net (decrease)/increase in financial liabilities designated at fair value", {"FY2025": -1845, "FY2024": 2652}),
    ("DATA", "Financial assets and liabilities at fair value through the income statement (combined, as reported)", {"FY2023": 264, "FY2022": 787, "FY2021": 665, "FY2020": 139, "FY2019": 309, "FY2018": 1736}),
    ("DATA", "Net (increase) in other assets and liabilities", {"FY2025": -215, "FY2024": -276, "FY2023": -52, "FY2022": -298, "FY2021": -299, "FY2020": -821, "FY2019": -1835, "FY2018": 561}),
    ("DATA", "Corporate income tax paid", {"FY2025": -1074, "FY2024": -522, "FY2023": -583, "FY2022": -395, "FY2021": -53, "FY2020": -597, "FY2019": -1086, "FY2018": -128}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": -7860, "FY2024": 1959, "FY2023": -17451, "FY2022": 1466, "FY2021": 29314, "FY2020": 13976, "FY2019": -3111, "FY2018": -257}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities at amortised cost", {"FY2025": -3727, "FY2024": -4615}),
    ("DATA", "Proceeds from redemption or sale of debt securities at amortised cost", {"FY2025": 8061, "FY2024": 3932}),
    ("DATA", "Debt securities at amortised cost (net, as reported)", {"FY2023": -178, "FY2022": -5796, "FY2021": -3695}),
    ("DATA", "Net cash acquired from the acquisition of the UK banking business (FY2018 only)", {"FY2018": 45940}),
    ("DATA", "Purchase of financial assets at fair value through other comprehensive income", {"FY2025": -20764, "FY2024": -21343, "FY2020": -5557, "FY2019": -11846, "FY2018": -8483}),
    ("DATA", "Proceeds from sale or redemption of financial assets at fair value through other comprehensive income", {"FY2025": 16812, "FY2024": 14959, "FY2018": 7584}),
    ("DATA", "Financial assets at fair value through other comprehensive income (net, as reported)", {"FY2023": -304, "FY2022": -6792, "FY2021": 10125}),
    ("DATA", "Financial liabilities designated at fair value (net, as reported)", {"FY2023": 196, "FY2022": 0}),
    ("DATA", "Purchase of property, plant and equipment and investment in intangibles", {"FY2025": -52, "FY2024": -13, "FY2023": -25, "FY2022": -13, "FY2021": 0, "FY2020": -17, "FY2019": -30, "FY2018": -40}),
    ("DATA", "Proceeds from sale of property, plant and equipment and intangibles (FY2018 only)", {"FY2018": 2}),
    ("DATA", "Acquisition of business, net of cash acquired", {"FY2025": 0, "FY2024": -228}),
    ("DATA", "Acquisition of subsidiaries, net of cash acquired", {"FY2023": -2378, "FY2022": 0}),
    ("DATA", "Disposal of subsidiaries, net of cash disposed", {"FY2023": -141, "FY2022": 0}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": 330, "FY2024": -7308, "FY2023": -2830, "FY2022": -12601, "FY2021": 6430, "FY2020": -5574, "FY2019": -11876, "FY2018": 45003}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid and other coupon payments on equity instruments", {"FY2025": -1639, "FY2024": -1173, "FY2023": -1482, "FY2022": -1888, "FY2021": -683, "FY2020": -400, "FY2019": -1203, "FY2018": -455}),
    ("DATA", "Capital contribution from Barclays PLC", {"FY2021": 0, "FY2020": 220, "FY2018": 0}),
    ("DATA", "Issuance of subordinated liabilities/debt", {"FY2025": 3600, "FY2024": 2277, "FY2023": 4393, "FY2022": 829, "FY2021": 1025, "FY2020": 3694, "FY2019": 157}),
    ("DATA", "Redemption of subordinated liabilities/debt", {"FY2025": -2703, "FY2024": -372, "FY2023": -1136, "FY2022": -2017, "FY2021": -1116, "FY2020": -1425}),
    ("DATA", "Issue of shares and other equity instruments", {"FY2025": 990, "FY2024": 618, "FY2023": 619, "FY2022": 0, "FY2019": 490}),
    ("DATA", "Repurchase/redemption of shares and other equity instruments", {"FY2025": -1188, "FY2024": -622, "FY2023": -750, "FY2022": 0}),
    ("DATA", "Lease liability payments", {"FY2025": -41, "FY2024": -53, "FY2023": -63, "FY2022": -71}),
    ("DATA", "Vesting of employee share schemes", {"FY2025": -28, "FY2024": -15, "FY2023": -16, "FY2022": -14, "FY2021": -11, "FY2020": -12, "FY2019": -12, "FY2018": -10}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": -1009, "FY2024": 660, "FY2023": 1565, "FY2022": -3161, "FY2021": -785, "FY2020": 2077, "FY2019": -568, "FY2018": -465}),
    ("DATA", "Effect of exchange rates on cash and cash equivalents", {"FY2021": 0, "FY2020": 428, "FY2019": -737}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -8539, "FY2024": -4689, "FY2023": -18716, "FY2022": -14296, "FY2021": 34959, "FY2020": 10907, "FY2019": -16292, "FY2018": 44281}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 35675, "FY2024": 40364, "FY2023": 59080, "FY2022": 73376, "FY2021": 38417, "FY2020": 27510, "FY2019": 44334, "FY2018": 53}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 27136, "FY2024": 35675, "FY2023": 40364, "FY2022": 59080, "FY2021": 73376, "FY2020": 38417, "FY2019": 28042, "FY2018": 44334}),
    ("SECTION", "Cash and cash equivalents at end of year comprise", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 21208, "FY2024": 29819, "FY2023": 34948, "FY2022": 54208, "FY2021": 69488, "FY2020": 35218, "FY2019": 24305, "FY2018": 40669}),
    ("DATA", "Loans and advances to banks with original maturity less than three months", {"FY2025": 178, "FY2024": 231, "FY2023": 291, "FY2022": 347, "FY2021": 46, "FY2020": 81, "FY2019": 87, "FY2018": 491}),
    ("DATA", "Cash collateral balances with central banks with original maturity less than three months", {"FY2025": 5750, "FY2024": 5625, "FY2023": 5125, "FY2022": 4525, "FY2021": 3842, "FY2020": 3118, "FY2019": 3650, "FY2018": 3174}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 27136, "FY2024": 35675, "FY2023": 40364, "FY2022": 59080, "FY2021": 73376, "FY2020": 38417, "FY2019": 28042, "FY2018": 44334}),
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
AQ_STAGE1_GROSS = {"FY2025": 194856, "FY2024": 179441, "FY2023": 173805, "FY2022": 175260, "FY2021": 193961, "FY2020": 182908, "FY2019": 171010, "FY2018": 157753}
AQ_STAGE2_GROSS = {"FY2025": 19509, "FY2024": 25400, "FY2023": 26471, "FY2022": 27637, "FY2021": 24639, "FY2020": 28078, "FY2019": 25595, "FY2018": 29423}
AQ_STAGE3_GROSS = {"FY2025": 3121, "FY2024": 3482, "FY2023": 3375, "FY2022": 3482, "FY2021": 3850, "FY2020": 3812, "FY2019": 3575, "FY2018": 4316}
AQ_TOTAL_GROSS = {"FY2025": 217486, "FY2024": 208323, "FY2023": 203651, "FY2022": 206379, "FY2021": 222450, "FY2020": 214798, "FY2019": 200180, "FY2018": 191492}
AQ_STAGE1_ALLOW = {"FY2025": 323, "FY2024": 433, "FY2023": 295, "FY2022": 339, "FY2021": 395, "FY2020": 322, "FY2019": 213, "FY2018": 199}
AQ_STAGE2_ALLOW = {"FY2025": 667, "FY2024": 679, "FY2023": 782, "FY2022": 815, "FY2021": 971, "FY2020": 1606, "FY2019": 1315, "FY2018": 1459}
AQ_STAGE3_ALLOW = {"FY2025": 634, "FY2024": 495, "FY2023": 579, "FY2022": 555, "FY2021": 813, "FY2020": 1221, "FY2019": 1083, "FY2018": 1269}
AQ_TOTAL_ALLOW = {"FY2025": 1624, "FY2024": 1607, "FY2023": 1656, "FY2022": 1709, "FY2021": 2179, "FY2020": 3149, "FY2019": 2611, "FY2018": 2927}
AQ_NPL_RATIO = {y: f"{AQ_STAGE3_GROSS[y] / AQ_TOTAL_GROSS[y] * 100:.1f}%" for y in YEARS if y in AQ_TOTAL_GROSS}
AQ_STAGE3_COVERAGE = {y: f"{AQ_STAGE3_ALLOW[y] / AQ_STAGE3_GROSS[y] * 100:.1f}%" for y in YEARS if y in AQ_STAGE3_GROSS}
AQ_TOTAL_COVERAGE = {y: f"{AQ_TOTAL_ALLOW[y] / AQ_TOTAL_GROSS[y] * 100:.1f}%" for y in YEARS if y in AQ_TOTAL_GROSS}

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
        f"FY2021: Annual Report 2021, p.66 — {AR21_URL}\n"
        f"FY2020: Annual Report 2020, p.60 (Loans and advances at amortised cost by product) — {AR20_URL}\n"
        f"FY2019: Annual Report 2019, p.51 (Loans and advances at amortised cost by product) — {AR19_URL}\n"
        f"FY2018: Annual Report 2018, p.52 (Loans and advances at amortised cost by product, Barclays Bank UK "
        f"Group table) — {AR18_URL}\n\n"
        "Note: NPL/coverage ratios are computed here (not the report's own headline ratio, though they tie closely "
        "to it - e.g. FY2021 Stage 3 coverage of 21.1% matches the report's own 'Total' Stage 3 coverage figure "
        "exactly). Product-level breakdown (e.g. mortgages vs. cards vs. corporate) isn't reproduced since the "
        "product taxonomy changed between FY2018-FY2021 (Home loans / Credit cards & other retail / Wholesale "
        "loans, called 'Corporate loans' in FY2018) and FY2022-2025 (Retail mortgages / Retail credit cards / "
        "Retail other / Corporate loans) - see each year's own source page for the full by-product split."
    ),
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# KM1 Key Metrics - two template generations, kept in separate blocks
# ---------------------------------------------------------------
# The FY2024 and FY2022 editions are not cited anywhere else in this script - the metric sheets take
# FY2024 from the FY2025 report and FY2022 from the FY2023 report, as comparatives. The KM1 sheet takes
# every year from its OWN edition, so those two editions need their own URLs. Both verified 200 /
# application/pdf / %PDF on 2026-09-16, resolved from the Barclays annual-reports index rather than guessed.
KM1_P3_24_URL = ("https://home.barclays/content/dam/home-barclays/documents/investor-relations/"
                 "ResultAnnouncements/FullYear2024Results/FY24-Barclays-Bank-UK-PLC-Pillar-3-Report.pdf")
KM1_P3_22_URL = ("https://home.barclays/content/dam/home-barclays/documents/investor-relations/"
                 "reports-and-events/annual-reports/2022/Pillar-3/Barclays-Bank-UK-PLC-Pillar-3-Report-2022.pdf")

KM1_SOURCES = (
    "Source - Barclays Bank UK PLC's own Pillar 3 Reports, each year taken from its OWN edition's year-end "
    "column, £m. Page numbers are the reports' own printed folios:\n"
    f"FY2025: Pillar 3 Report 2025, p.11 (Table 6: UK KM1 - Key metrics - Part 1) and p.12 (Part 2), "
    f"'As at 31.12.25' column - {P3_25_URL}\n"
    f"FY2024: Pillar 3 Report 2024, p.11 and p.12 (Table 6: UK KM1 - Key metrics (KM1 / IFRS9-FL), Parts 1 "
    f"and 2), 'As at 31.12.24' column - {KM1_P3_24_URL}\n"
    f"FY2023: Pillar 3 Report 2023, p.11 and p.12, 'As at 31.12.23' column - {P3_23_URL}\n"
    f"FY2022: Pillar 3 Report 2022, p.11 and p.12 (Table 6: UK KM1 - Key metrics (KM1 / IFRS9-FL / Article "
    f"468-FL / UK LR) - Part 1), 'As at 31.12.22' column - {KM1_P3_22_URL}\n"
    f"FY2021: Pillar 3 Report 2021, p.9 (Table 4: Key Metrics (KM1 / IFRS 9-FL / Article 468-FL)), "
    f"'31 Dec 21' column - {P3_21_URL}\n"
    f"FY2020: Pillar 3 Report 2020, p.8 (Table 4: Key Metrics (KM1/IFRS 9-FL)), '31 December 2020' column - "
    f"{P3_20_URL}\n"
    f"FY2019: Pillar 3 Report 2019, p.8 (Table 4: Key Metrics (KM1/IFRS9-FL)), '31 December 2019' column - "
    f"{P3_19_URL}\n\n"
    "THE COLUMNS IN THE SOURCE ARE QUARTER-ENDS, NOT YEARS. Each UK-era edition prints five columns - its own "
    "31 December followed by the three preceding quarter-ends and the prior 31 December (e.g. the 2025 report "
    "prints 31.12.25, 30.09.25, 30.06.25, 31.03.25, 31.12.24). Only each edition's own 31 December column is "
    "used here. The earlier editions print two to four columns on the same principle (the 2021 report prints "
    "31 Dec 21, 30 June 21, 31 Dec 20, 30 Jun 20). Picking the wrong column would look entirely plausible and "
    "be silently wrong, so every figure on this sheet comes from the first column of the edition named above.\n\n"
    "TWO TEMPLATE GENERATIONS, DELIBERATELY NOT MERGED. FY2022-FY2025 use the UK KM1 template; FY2019-FY2021 "
    "use the earlier Basel/EU 'KM1 / IFRS9-FL' template, which Barclays captions 'Table 4: Key Metrics'. THE "
    "ROW NUMBERS ARE NOT COMPARABLE BETWEEN THE TWO BLOCKS. In the earlier template a bare '7a' is the FULLY "
    "LOADED TOTAL CAPITAL RATIO; in the UK template 'UK 7a' is the ADDITIONAL CET1 SREP REQUIREMENT. They are "
    "different disclosures sharing a glyph, so the two generations are kept in separate captioned blocks and "
    "no row is carried across the break. The earlier template also has no NSFR rows at all (the NSFR became "
    "a UK requirement on 1 January 2022), so rows 18-20 are blank for FY2019-FY2021 rather than zero.\n\n"
    "ROWS 13 AND 14 ARE PRINTED TWICE IN EVERY UK-ERA EDITION, FOR TWO DIFFERENT ENTITIES, and the two copies "
    "genuinely differ. Part 2 carries a 'Barclays Bank UK Group' leverage block and then a 'Barclays Bank UK "
    "PLC' one - at 31.12.25, exposure of £277,958m against £278,131m. Both are reproduced below under their "
    "own captions. This workbook is the Barclays Bank UK GROUP consolidation throughout, so the Group block is "
    "this entity's own figure and the individual Leverage Ratio sheet carries it; the PLC block is included "
    "because the Bank publishes it, not as a substitute for the Group's. The LCR and NSFR blocks are printed "
    "once, under a repeated 'Barclays Bank UK Group' sub-heading. Rows UK 14c/14d/14e are printed only in the "
    "Group block, so they are blank on the PLC block rather than repeated across it.\n\n"
    "LABEL VARIATION RECORDED, NOT SMOOTHED: the FY2019 edition captions row 11 'Total of bank CET1 specific "
    "buffer requirements (%) (row 8 + 9 + SRB)', where the FY2020 and FY2021 editions say '(row 8 + 9 + "
    "O-SII)'. The label below is the later wording; the FY2019 figure is its own edition's.\n\n"
    "FY2018 IS NOT SHOWN. Barclays Bank UK PLC published no standalone Pillar 3 report for FY2018 and printed "
    "no KM1-shaped table that year, so FY2018 is omitted from this sheet entirely rather than shown as an "
    "empty column. Its capital figures remain on the individual metric sheets, cited to the FY2018 Annual "
    "Report's capital risk section.\n\n"
    "LATEST-EDITION CHECK, 2026-09-16: the Barclays annual-reports index "
    "(https://home.barclays/investor-relations/reports-and-events/annual-reports/) lists 58 Pillar 3 "
    "documents. The newest for this entity is FY25-BBUKPLC-Pillar-3.pdf, which this workbook holds; probes "
    "for an FY26 edition return an HTML soft-404, consistent with a 31 December year-end. None newer exists."
)

km1_rows = [
    ("SECTION", "UK KM1 TEMPLATE - AS PUBLISHED FY2022-FY2025 (Table 6: UK KM1 - Key metrics, Parts 1 and 2)", {}),
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital (£m)",
     {"FY2025": 12331, "FY2024": 11895, "FY2023": 10638, "FY2022": 10701}),
    ("DATA", "1a  Fully loaded common Equity Tier 1 (CET1) capital (£m)",
     {"FY2024": 11862, "FY2023": 10638, "FY2022": 10628}),
    ("DATA", "2  Tier 1 capital (£m)",
     {"FY2025": 14558, "FY2024": 14320, "FY2023": 13067, "FY2022": 13261}),
    ("DATA", "2a  Fully loaded tier 1 capital (£m)",
     {"FY2024": 14287, "FY2023": 13067, "FY2022": 13188}),
    ("DATA", "3  Total capital (£m)",
     {"FY2025": 16996, "FY2024": 17155, "FY2023": 15596, "FY2022": 15828}),
    ("DATA", "3a  Fully loaded total capital (£m)",
     {"FY2024": 17122, "FY2023": 15596, "FY2022": 15804}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4  Total risk-weighted exposure amount (£m)",
     {"FY2025": 85065, "FY2024": 83639, "FY2023": 72102, "FY2022": 72719}),
    ("DATA", "4a  Fully loaded total risk-weighted exposure amount (£m)",
     {"FY2024": 83637, "FY2023": 72102, "FY2022": 72707}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)",
     {"FY2025": "14.5%", "FY2024": "14.2%", "FY2023": "14.8%", "FY2022": "14.7%"}),
    ("DATA", "5a  Fully loaded common Equity Tier 1 ratio (%)",
     {"FY2024": "14.2%", "FY2023": "14.8%", "FY2022": "14.6%"}),
    ("DATA", "6  Tier 1 ratio (%)",
     {"FY2025": "17.1%", "FY2024": "17.1%", "FY2023": "18.1%", "FY2022": "18.2%"}),
    ("DATA", "6a  Fully loaded tier 1 ratio (%)",
     {"FY2024": "17.1%", "FY2023": "18.1%", "FY2022": "18.1%"}),
    ("DATA", "7  Total capital ratio (%)",
     {"FY2025": "20.0%", "FY2024": "20.5%", "FY2023": "21.6%", "FY2022": "21.8%"}),
    ("DATA", "7a  Fully loaded total capital ratio (%)",
     {"FY2024": "20.5%", "FY2023": "21.6%", "FY2022": "21.7%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirements (%)",
     {"FY2025": "2.6%", "FY2024": "2.9%", "FY2023": "2.9%", "FY2022": "2.8%"}),
    ("DATA", "UK 7b  Additional AT1 SREP requirements (%)",
     {"FY2025": "0.9%", "FY2024": "1.0%", "FY2023": "1.0%", "FY2022": "0.9%"}),
    ("DATA", "UK 7c  Additional T2 SREP requirements (%)",
     {"FY2025": "1.1%", "FY2024": "1.3%", "FY2023": "1.3%", "FY2022": "1.3%"}),
    ("DATA", "UK 7d  Total SREP own funds requirements (%)",
     {"FY2025": "12.6%", "FY2024": "13.2%", "FY2023": "13.2%", "FY2022": "13.0%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8  Capital conservation buffer (%)",
     {"FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.5%", "FY2022": "2.5%"}),
    ("DATA", "9  Institution specific countercyclical capital buffer (%)",
     {"FY2025": "2.0%", "FY2024": "2.0%", "FY2023": "2.0%", "FY2022": "1.0%"}),
    ("DATA", "UK 10a  Other Systemically Important Institution buffer (%)",
     {"FY2025": "1.0%", "FY2024": "1.0%", "FY2023": "1.0%", "FY2022": "1.0%"}),
    ("DATA", "11  Combined buffer requirement (%)",
     {"FY2025": "5.5%", "FY2024": "5.5%", "FY2023": "5.5%", "FY2022": "4.5%"}),
    ("DATA", "UK 11a  Overall capital requirements (%)",
     {"FY2025": "18.0%", "FY2024": "18.7%", "FY2023": "18.7%", "FY2022": "17.5%"}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "7.4%", "FY2024": "6.8%", "FY2023": "7.3%", "FY2022": "7.4%"}),
    ("SECTION", "Leverage ratio - Barclays Bank UK Group (the first of the two blocks the report prints)", {}),
    ("DATA", "13  Total exposure measure excluding claims on central banks (£m)",
     {"FY2025": 277958, "FY2024": 268452, "FY2023": 250163, "FY2022": 250092}),
    ("DATA", "14  Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "5.2%", "FY2024": "5.3%", "FY2023": "5.2%", "FY2022": "5.3%"}),
    ("DATA", "UK 14a  Fully loaded ECL accounting model leverage ratio excluding claims on central banks (%)",
     {"FY2025": "5.2%", "FY2024": "5.3%", "FY2023": "5.2%"}),
    ("DATA", "UK 14b  Leverage ratio including claims on central banks (%)",
     {"FY2025": "4.8%", "FY2024": "4.7%", "FY2023": "4.5%", "FY2022": "4.3%"}),
    ("DATA", "UK 14c  Average leverage ratio excluding claims on central banks (%)",
     {"FY2025": "5.4%", "FY2024": "5.4%", "FY2023": "5.2%", "FY2022": "5.3%"}),
    ("DATA", "UK 14d  Average leverage ratio including claims on central banks (%)",
     {"FY2025": "4.9%", "FY2024": "4.8%", "FY2023": "4.5%", "FY2022": "4.3%"}),
    ("DATA", "UK 14e  Countercyclical leverage ratio buffer (%)",
     {"FY2025": "0.7%", "FY2024": "0.7%", "FY2023": "0.7%", "FY2022": "0.3%"}),
    ("SECTION", "Leverage ratio - Barclays Bank UK PLC (the report's SECOND block; different figures, not a repeat)", {}),
    ("DATA", "13  Total exposure measure excluding claims on central banks - Barclays Bank UK PLC (£m)",
     {"FY2025": 278131, "FY2024": 268870, "FY2023": 250564}),
    ("DATA", "14  Leverage ratio excluding claims on central banks (%) - Barclays Bank UK PLC",
     {"FY2025": "5.2%", "FY2024": "5.3%", "FY2023": "5.2%"}),
    ("DATA", "UK 14a  Fully loaded ECL accounting model leverage ratio excl. central banks (%) - Barclays Bank UK PLC",
     {"FY2025": "5.2%", "FY2024": "5.3%", "FY2023": "5.2%"}),
    ("DATA", "UK 14b  Leverage ratio including claims on central banks (%) - Barclays Bank UK PLC",
     {"FY2025": "4.8%", "FY2024": "4.7%", "FY2023": "4.5%"}),
    ("SECTION", "Liquidity Coverage Ratio - Barclays Bank UK Group", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (Weighted value) (£m)",
     {"FY2025": 64552, "FY2024": 68446, "FY2023": 68533, "FY2022": 81791}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value (£m)",
     {"FY2025": 36199, "FY2024": 35356, "FY2023": 38982, "FY2022": 45306}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value (£m)",
     {"FY2025": 1586, "FY2024": 1477, "FY2023": 925, "FY2022": 1340}),
    ("DATA", "16  Total net cash outflows (adjusted value) (£m)",
     {"FY2025": 34613, "FY2024": 33879, "FY2023": 38057, "FY2022": 43966}),
    ("DATA", "17  Liquidity coverage ratio (%)",
     {"FY2025": "186.6%", "FY2024": "202.0%", "FY2023": "180%", "FY2022": "186%"}),
    ("DATA", "17a  Liquidity coverage ratio (%) (period end)",
     {"FY2022": "183%"}),
    ("SECTION", "Net Stable Funding Ratio - Barclays Bank UK Group", {}),
    ("DATA", "18  Total available stable funding (£m)",
     {"FY2025": 257230, "FY2024": 254755, "FY2023": 258620, "FY2022": 266421}),
    ("DATA", "19  Total required stable funding (£m)",
     {"FY2025": 168761, "FY2024": 160041, "FY2023": 156588, "FY2022": 158156}),
    ("DATA", "20  NSFR ratio (%)",
     {"FY2025": "152.4%", "FY2024": "159.3%", "FY2023": "165%", "FY2022": "168%"}),
    ("SECTION", "BASEL / EU KM1 TEMPLATE - AS PUBLISHED FY2019-FY2021 (Table 4: Key Metrics (KM1/IFRS9-FL)). ROW NUMBERS ARE NOT COMPARABLE WITH THE BLOCK ABOVE.", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) (£m)",
     {"FY2021": 10828, "FY2020": 11247, "FY2019": 10128}),
    ("DATA", "2  Tier 1 (£m)",
     {"FY2021": 13388, "FY2020": 13807, "FY2019": 12688}),
    ("DATA", "2a  Fully loaded ECL accounting model Tier 1 (£m)",
     {"FY2021": 13132, "FY2020": 13077, "FY2019": 12498}),
    ("DATA", "3  Total capital (£m)",
     {"FY2021": 16442, "FY2020": 17178, "FY2019": 16012}),
    ("DATA", "3a  Fully loaded ECL accounting model total capital (£m)",
     {"FY2021": 16359, "FY2020": 16677, "FY2019": 15990}),
    ("DATA", "4  Total risk-weighted assets (RWA) (£m)",
     {"FY2021": 71213, "FY2020": 72025, "FY2019": 75010}),
    ("DATA", "4a  Fully loaded ECL accounting model total risk-weighted assets (RWA) (£m)",
     {"FY2021": 71116, "FY2020": 72039, "FY2019": 75124}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)",
     {"FY2021": "15.2%", "FY2020": "15.6%", "FY2019": "13.5%"}),
    ("DATA", "5a  Fully loaded ECL accounting model Common Equity Tier 1 (%)",
     {"FY2021": "14.9%", "FY2020": "14.6%", "FY2019": "13.2%"}),
    ("DATA", "6  Tier 1 ratio (%)",
     {"FY2021": "18.8%", "FY2020": "19.2%", "FY2019": "16.9%"}),
    ("DATA", "6a  Fully loaded ECL accounting model Tier 1 ratio (%)",
     {"FY2021": "18.5%", "FY2020": "18.2%", "FY2019": "16.6%"}),
    ("DATA", "7  Total capital ratio (%)",
     {"FY2021": "23.1%", "FY2020": "23.9%", "FY2019": "21.3%"}),
    ("DATA", "7a  Fully loaded ECL accounting model total capital ratio (%)",
     {"FY2021": "23.0%", "FY2020": "23.1%", "FY2019": "21.3%"}),
    ("DATA", "8  Capital conservation buffer requirement (%)",
     {"FY2021": "2.5%", "FY2020": "2.5%", "FY2019": "2.5%"}),
    ("DATA", "9  Countercyclical buffer requirement (%)",
     {"FY2021": "0.0%", "FY2020": "0.0%", "FY2019": "1.0%"}),
    ("DATA", "11  Total of bank CET1 specific buffer requirements (%) (row 8 + 9 + O-SII)",
     {"FY2021": "3.5%", "FY2020": "3.5%", "FY2019": "4.5%"}),
    ("DATA", "12  CET1 available after meeting the bank's minimum capital requirements (%)",
     {"FY2021": "10.7%", "FY2020": "11.1%", "FY2019": "9.0%"}),
    ("DATA", "13  Total CRR leverage ratio exposure measure (£m)",
     {"FY2021": 324899, "FY2020": 294242, "FY2019": 264085}),
    ("DATA", "14  Transitional CRR leverage ratio (%)",
     {"FY2021": "4.1%", "FY2020": "4.7%", "FY2019": "4.8%"}),
    ("DATA", "IFRS9-FL 17  Leverage ratio as if IFRS 9 or analogous ECLs transitional arrangement had not been applied (%)",
     {"FY2021": "4.0%", "FY2020": "4.5%", "FY2019": "4.7%"}),
    ("DATA", "13a  Total average UK leverage ratio exposure measure (£m)",
     {"FY2021": 246849, "FY2020": 245992, "FY2019": 240057}),
    ("DATA", "14a  Transitional average UK leverage ratio (%)",
     {"FY2021": "5.5%", "FY2020": "5.6%", "FY2019": "5.2%"}),
    ("DATA", "13b  Total UK leverage ratio exposure measure (£m)",
     {"FY2021": 241173, "FY2020": 245176, "FY2019": 236026}),
    ("DATA", "14b  Transitional UK leverage ratio (%)",
     {"FY2021": "5.6%", "FY2020": "5.6%", "FY2019": "5.4%"}),
    ("DATA", "15  Total HQLA (£m)",
     {"FY2021": 85092, "FY2020": 58035, "FY2019": 41293}),
    ("DATA", "16  Total net cash outflows (£m)",
     {"FY2021": 41690, "FY2020": 36246, "FY2019": 28741}),
    ("DATA", "17  LCR ratio (%)",
     {"FY2021": "204%", "FY2020": "160%", "FY2019": "144%"}),
]

bw.add_km1_sheet(
    title="Barclays Bank UK Group - KM1 Key Metrics",
    subtitle="Each year from its own Pillar 3 edition's year-end column - two template generations, kept separate",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=96,
    source_height=560,
    years=["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"],
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Consolidated basis, {unit}" if unit else "Consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=42, source_height=90)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 12331, "FY2024": 11895, "FY2023": 10638, "FY2022": 10701, "FY2021": 10828, "FY2020": 11247, "FY2019": 10128, "FY2018": 10700})],
    p3_sources(),
    note="FY2018 CET1 capital (£10.7bn, unaudited) is disclosed within the FY2018 Annual Report's capital risk "
         "section rather than a standalone Pillar 3 report - see p3_sources note on that year.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "14.5%", "FY2024": "14.2%", "FY2023": "14.8%", "FY2022": "14.7%", "FY2021": "15.2%", "FY2020": "15.6%", "FY2019": "13.5%", "FY2018": "14.2%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 14558, "FY2024": 14320, "FY2023": 13067, "FY2022": 13261, "FY2021": 13388, "FY2020": 13807, "FY2019": 12688, "FY2018": 12800})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "17.1%", "FY2024": "17.1%", "FY2023": "18.1%", "FY2022": "18.2%", "FY2021": "18.8%", "FY2020": "19.2%", "FY2019": "16.9%", "FY2018": "17.0%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 16996, "FY2024": 17155, "FY2023": 15596, "FY2022": 15828, "FY2021": 16442, "FY2020": 17178, "FY2019": 16012, "FY2018": 16100})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "20.0%", "FY2024": "20.5%", "FY2023": "21.6%", "FY2022": "21.8%", "FY2021": "23.1%", "FY2020": "23.9%", "FY2019": "21.3%", "FY2018": "21.3%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 85065, "FY2024": 83639, "FY2023": 72102, "FY2022": 72719, "FY2021": 71213, "FY2020": 72025, "FY2019": 75010, "FY2018": 75327})],
    p3_sources(),
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2025": 68166, "FY2024": 68018, "FY2023": 58174, "FY2022": 58885, "FY2021": 54981, "FY2020": 56891, "FY2019": 60490}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 300, "FY2024": 419, "FY2023": 541, "FY2022": 1083, "FY2021": 1208, "FY2020": 787, "FY2019": 625}),
    ("DATA", "Securitisation exposures (non-trading book, after cap)", {"FY2025": 2517, "FY2024": 1644, "FY2023": 1445, "FY2022": 1437, "FY2021": 1268, "FY2020": 737, "FY2019": 135}),
    ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2025": 177, "FY2024": 228, "FY2023": 274, "FY2022": 233, "FY2021": 100, "FY2020": 72, "FY2019": 178}),
    ("DATA", "Operational risk", {"FY2025": 13905, "FY2024": 13330, "FY2023": 11668, "FY2022": 11081, "FY2021": 10892, "FY2020": 11347, "FY2019": 11617}),
    ("DATA", "Amounts below thresholds for deduction (subject to 250% risk weight)", {"FY2025": 2309, "FY2024": 2271, "FY2023": 2314, "FY2022": 2704, "FY2021": 2764, "FY2020": 2191, "FY2019": 1965}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 85065, "FY2024": 83639, "FY2023": 72102, "FY2022": 72719, "FY2021": 71213, "FY2020": 72025, "FY2019": 75010}),
]

bw.add_rwa_breakdown_sheet(
    title="Barclays Bank UK PLC — RWA Breakdown",
    subtitle="Barclays Bank UK Group (consolidated basis), £m",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(part_label_25="Table 10: OV1 - Overview of risk weighted exposure amounts", page_25="16-17",
                             part_label_23="Table 10: OV1 - Overview of risk weighted exposure amounts", page_23="16-17",
                             part_label_21="Table 8: OV1 - Overview of risk weighted assets by risk type and capital requirements", page_21="12-13",
                             part_label_20="Table 8: OV1 - Overview of risk weighted assets by risk type and capital requirements", page_20="11",
                             part_label_19="Table 8: OV1 - Overview of risk weighted assets by risk type and capital requirements", page_19="11")
    + "\nFY2018: CORRECTED 18 September 2026 (KM1-032). This note previously read 'not available - Barclays Bank "
      "UK PLC did not publish a standalone Pillar 3 report for FY2018, and the FY2018 Annual Report's capital "
      "risk section discloses only the total RWA figure (£75,327m), not a by-risk-type breakdown'. The first "
      "half is true; the second half was FALSE, and it was false because only the SUBSIDIARY's own documents "
      "had been searched. A by-risk-type breakdown for Barclays Bank UK PLC is published - in the PARENT's "
      "report, which had never been opened: 'Barclays PLC Pillar 3 Report 2018', Table 12a 'Risk weighted "
      "assets by significant subsidiaries', printed p.27, which states on p.9 that 'Significant subsidiaries "
      "disclosures are included in this report for Barclays Bank PLC and Barclays Bank UK PLC'. Its Barclays "
      "Bank UK PLC row, as at 31.12.18, £m: Credit risk Std 3,985; Credit risk A-IRB 59,484; Counterparty "
      "credit risk Std 266; CCR A-IRB '-'; Settlement risk '-'; CVA 11; Market risk Std 63; Market risk IMA "
      "'-'; Operational risk 11,518; Total RWAs 75,327. Those sum exactly to the 75,327 already carried on the "
      "Total RWAs sheet from the Annual Report, which is the control that confirms the row is the right "
      "entity's.\n"
      "WHY THE COLUMN IS STILL LEFT EMPTY HERE, deliberately and not for want of a source: Table 12a's "
      "categories are not this sheet's categories. Because its two credit-risk columns sum with CCR, market "
      "and operational risk to the full 75,327, they necessarily SUBSUME the securitisation exposures and the "
      "below-threshold 250%-risk-weight amounts that FY2019-FY2025 report on their own rows here. Spreading "
      "3,985 + 59,484 into this sheet's 'Credit risk (excluding CCR)' row would therefore print a figure "
      "defined differently from every other year in the same row, which is a worse defect than an empty "
      "column - the reproduce-don't-normalise rule. The figures are recorded above so a reader has them.\n"
      "BASIS BREAK, also recorded rather than reconciled: Table 12a is Barclays Bank UK PLC on the INDIVIDUAL "
      "(PRA solo) basis, whereas this sheet is headed Barclays Bank UK Group consolidated. The parent's own "
      "scope-of-consolidation section (printed p.9) gives the reason, and it is also the affirmative "
      "explanation for the absence of an FY2018 entity Pillar 3: 'Throughout 2018, Barclays Bank UK PLC (BBUK "
      "PLC) was regulated by the Prudential Regulation Authority (PRA) on an individual basis... BBUK PLC "
      "Group became regulated by the PRA from 1 January 2019.' The FY2019 first edition is therefore the "
      "first year the consolidated basis existed, not merely the first year a document was found.\n"
      "TRAP RECORDED FOR ANY LATER PASS: Table 12 on the same printed page is 'RWAs by risk type and "
      "BUSINESS' and its 'Barclays UK' row reads 75,181 - the business segment, not the legal entity. The "
      "entity figure is 75,327 in Table 12a. The two are adjacent, differ by 146, and the wrong one is "
      "entirely plausible.\n"
      "Source: https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/"
      "annual-reports/2018/Barclays%20PLC%20Pillar%203%20Report%202018.pdf (re-verified 2026-09-18: HTTP 200, "
      "application/pdf, %PDF-1.6, 2,174,817 bytes).",
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks (£m)", {"FY2025": 277958, "FY2024": 268452, "FY2023": 250163, "FY2022": 250092, "FY2021": 241173, "FY2020": 245176, "FY2019": 236026}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "5.2%", "FY2024": "5.3%", "FY2023": "5.2%", "FY2022": "5.3%", "FY2021": "5.6%", "FY2020": "5.6%", "FY2019": "5.4%"}),
        ("Leverage ratio including claims on central banks (%)", {"FY2025": "4.8%", "FY2024": "4.7%", "FY2023": "4.5%", "FY2022": "4.3%", "FY2021": "4.1%", "FY2020": "4.7%", "FY2019": "4.8%", "FY2018": "4.9%"}),
    ],
    p3_sources(part_label_25="Table 6: KM1 - Key metrics - Part 2", page_25="12",
               part_label_23="Table 6: KM1 - Key metrics - Part 2", page_23="12",
               part_label_21="Table 4: Key Metrics (KM1 / IFRS 9-FL)", page_21="9",
               # CITATION CORRECTED 2026-09-16 (KM1-007): these two were "7". The Key Metrics table is on
               # printed page 8 of BOTH the FY2019 and FY2020 reports - each page's own footer reads
               # "Barclays Bank UK PLC Pillar 3 report 2019   8" (and ...2020   8), with the preceding and
               # following sheets footed 7 and 9, so the folio matches the PDF sheet index in these
               # editions. The same wrong page number appeared in two places in this file; both fixed.
               part_label_20="Table 4: Key Metrics (KM1/IFRS 9-FL)", page_20="8",
               part_label_19="Table 4: Key Metrics (KM1/IFRS9-FL)", page_19="8",
               part_label_18="Annual Report 2018 capital risk disclosures, 'Capital Requirements Regulation (CRR) leverage ratio'", page_18="80"),
    note="FY2021-FY2019 exposure/ratios use the 'UK leverage ratio (Transitional)' and 'CRR leverage ratio "
         "(Transitional)' rows from each year's Pillar 3 report as the closest equivalents to the "
         "'excluding'/'including claims on central banks' framing introduced in later reports. FY2018 predates "
         "that UK/CRR leverage ratio split at the BBUKPLC entity level (no standalone Pillar 3 report was "
         "published for FY2018 - see p3_sources note); the FY2018 Annual Report discloses only a single 'CRR "
         "leverage ratio' of 4.9% (with £258bn of CRR leverage exposure), which is presented here on the "
         "'including claims on central banks' row as the closer equivalent - the 'excluding' row and exposure "
         "figure are left blank for FY2018 since no comparable UK-basis figure was disclosed that year.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (£m)", {"FY2025": 64552, "FY2024": 68446, "FY2023": 68533, "FY2022": 81791, "FY2021": 85092, "FY2020": 58035, "FY2019": 41293}),
        ("Total net cash outflows, adjusted value (£m)", {"FY2025": 34613, "FY2024": 33879, "FY2023": 38057, "FY2022": 43966, "FY2021": 41690, "FY2020": 36246, "FY2019": 28741}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "186.6%", "FY2024": "202.0%", "FY2023": "180%", "FY2022": "186%", "FY2021": "204%", "FY2020": "160%", "FY2019": "144%", "FY2018": "164%"}),
    ],
    p3_sources(part_label_25="Table 6: KM1 - Key metrics - Part 2", page_25="12",
               part_label_23="Table 6: KM1 - Key metrics - Part 2", page_23="12",
               part_label_21="Table 4: Key Metrics (KM1 / IFRS 9-FL)", page_21="9",
               # CITATION CORRECTED 2026-09-16 (KM1-007): these two were "7". The Key Metrics table is on
               # printed page 8 of BOTH the FY2019 and FY2020 reports - each page's own footer reads
               # "Barclays Bank UK PLC Pillar 3 report 2019   8" (and ...2020   8), with the preceding and
               # following sheets footed 7 and 9, so the folio matches the PDF sheet index in these
               # editions. The same wrong page number appeared in two places in this file; both fixed.
               part_label_20="Table 4: Key Metrics (KM1/IFRS 9-FL)", page_20="8",
               part_label_19="Table 4: Key Metrics (KM1/IFRS9-FL)", page_19="8",
               part_label_18="Annual Report 2018 liquidity risk disclosures, 'Barclays Bank UK Group liquidity coverage ratio'", page_18="74"),
    note="LCR is computed as a trailing average of the last 12 month-end observations from FY2019 onward. FY2018 "
         "predates the BBUKPLC entity's first standalone Pillar 3 report; the FY2018 Annual Report discloses only "
         "the headline LCR ratio (164%) within its liquidity risk section, without the underlying weighted "
         "HQLA/net cash outflow components in the KM1 format used from FY2019 - those two rows are left blank for "
         "FY2018 for that reason.",
)

# GA-020 (2026-09-19) evidenced statement texts. Checked that day: the FY2019, FY2020 and FY2021 Pillar 3
# reports (P3_19/20/21_URL; 592k-721k characters of text) contain no 'NSFR' or 'net stable funding' at all,
# and the FY2018-FY2021 Annual Reports mention the NSFR only as a forthcoming Basel III / CRR II standard.
BBUK_NSFR_NA_P3 = ("Not applicable – UK NSFR requirement began 1 Jan 2022; this year's Pillar 3 has no NSFR and the "
                   "annual report names it only as a forthcoming standard (checked 2026-09-19)")
BBUK_NSFR_NA_AR = ("Not applicable – UK NSFR requirement began 1 Jan 2022; FY2018 Annual Report (no standalone Pillar 3 "
                   "that year) names it only as a forthcoming standard (checked 2026-09-19)")
metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2025": 257230, "FY2024": 254755, "FY2023": 258620, "FY2022": 266421}),
        ("Total required stable funding (£m)", {"FY2025": 168761, "FY2024": 160041, "FY2023": 156588, "FY2022": 158156}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "152.4%", "FY2024": "159.3%", "FY2023": "165%", "FY2022": "168%", "FY2021": BBUK_NSFR_NA_P3, "FY2020": BBUK_NSFR_NA_P3, "FY2019": BBUK_NSFR_NA_P3, "FY2018": BBUK_NSFR_NA_AR}),
    ],
    p3_sources(part_label_25="Table 6: KM1 - Key metrics - Part 2", page_25="12",
               part_label_23="Table 6: KM1 - Key metrics - Part 2", page_23="12",
               part_label_21="Table 4: Key Metrics (KM1 / IFRS 9-FL)", page_21="9"),
    note="NSFR is computed as a trailing average of the last four spot quarter-end positions. It was not a Pillar 3 "
         "disclosure requirement as at FY2018-FY2021 (the UK NSFR regime took effect from 1 January 2022), so no "
         "FY2018-FY2021 figures are available.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed at this level" for y in YEARS})],
    p3_sources(),
    note="MREL disclosures are not applicable for Barclays Bank UK Group (the ring-fenced entity) in any of the "
         "eight years reviewed; MREL is disclosed at the Barclays PLC group level instead (see Barclays PLC "
         "Pillar 3 Report, Table 21: TLAC2).",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 302824, "FY2024": 303179, "FY2023": 293559, "FY2022": 312179, "FY2021": 319695, "FY2020": 287498, "FY2019": 258398, "FY2018": 251305}),
        ("Loans and advances at amortised cost to customers", {"FY2025": 215634, "FY2024": 206435, "FY2023": 200782, "FY2022": 203279, "FY2021": 220271, "FY2020": 211649, "FY2019": 197569, "FY2018": 188565}),
        ("Deposits at amortised cost from customers", {"FY2025": 244666, "FY2024": 244376, "FY2023": 241218, "FY2022": 258058, "FY2021": 260732, "FY2020": 240535, "FY2019": 205696, "FY2018": 197485}),
        ("Total equity", {"FY2025": 20278, "FY2024": 18585, "FY2023": 16861, "FY2022": 15413, "FY2021": 17400, "FY2020": 17027, "FY2019": 16513, "FY2018": 16943}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 8811, "FY2024": 8423, "FY2023": 7670, "FY2022": 7397, "FY2021": 6482, "FY2020": 6424, "FY2019": 7322, "FY2018": 5606}),
        ("Operating expenses", {"FY2025": -5093, "FY2024": -4511, "FY2023": -4567, "FY2022": -4577, "FY2021": -4691, "FY2020": -4646, "FY2019": -5944, "FY2018": -3434}),
        ("Profit after tax", {"FY2025": 2594, "FY2024": 2620, "FY2023": 1922, "FY2022": 1807, "FY2021": 1869, "FY2020": 379, "FY2019": 156, "FY2018": 1115}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 18585, "FY2024": 16861, "FY2023": 15413, "FY2022": 17400, "FY2021": 17027, "FY2020": 16513, "FY2019": 16943, "FY2018": 46}),
        ("Total comprehensive income for the year", {"FY2025": 3498, "FY2024": 2875, "FY2023": 3050, "FY2022": -106, "FY2021": 1030, "FY2020": 670, "FY2019": 263, "FY2018": 1118}),
        ("Other movements, net", {"FY2025": -1805, "FY2024": -1151, "FY2023": -1602, "FY2022": -1881, "FY2021": -657, "FY2020": -156, "FY2019": -693, "FY2018": 15779}),
        ("Closing equity", {"FY2025": 20278, "FY2024": 18585, "FY2023": 16861, "FY2022": 15413, "FY2021": 17400, "FY2020": 17027, "FY2019": 16513, "FY2018": 16943}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": -7860, "FY2024": 1959, "FY2023": -17451, "FY2022": 1466, "FY2021": 29314, "FY2020": 13976, "FY2019": -3111, "FY2018": -257}),
        ("Net cash from investing activities", {"FY2025": 330, "FY2024": -7308, "FY2023": -2830, "FY2022": -12601, "FY2021": 6430, "FY2020": -5574, "FY2019": -11876, "FY2018": 45003}),
        ("Net cash from financing activities", {"FY2025": -1009, "FY2024": 660, "FY2023": 1565, "FY2022": -3161, "FY2021": -785, "FY2020": 2077, "FY2019": -568, "FY2018": -465}),
        ("Cash and cash equivalents at end of year", {"FY2025": 27136, "FY2024": 35675, "FY2023": 40364, "FY2022": 59080, "FY2021": 73376, "FY2020": 38417, "FY2019": 28042, "FY2018": 44334}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "14.5%", "FY2024": "14.2%", "FY2023": "14.8%", "FY2022": "14.7%", "FY2021": "15.2%", "FY2020": "15.6%", "FY2019": "13.5%", "FY2018": "14.2%"}),
        ("Tier 1 Ratio", {"FY2025": "17.1%", "FY2024": "17.1%", "FY2023": "18.1%", "FY2022": "18.2%", "FY2021": "18.8%", "FY2020": "19.2%", "FY2019": "16.9%", "FY2018": "17.0%"}),
        ("Total Capital Ratio", {"FY2025": "20.0%", "FY2024": "20.5%", "FY2023": "21.6%", "FY2022": "21.8%", "FY2021": "23.1%", "FY2020": "23.9%", "FY2019": "21.3%", "FY2018": "21.3%"}),
        ("Leverage Ratio", {"FY2025": "5.2%", "FY2024": "5.3%", "FY2023": "5.2%", "FY2022": "5.3%", "FY2021": "5.6%", "FY2020": "5.6%", "FY2019": "5.4%", "FY2018": "4.9%*"}),
        ("LCR", {"FY2025": "186.6%", "FY2024": "202.0%", "FY2023": "180%", "FY2022": "186%", "FY2021": "204%", "FY2020": "160%", "FY2019": "144%", "FY2018": "164%"}),
        ("NSFR", {"FY2025": "152.4%", "FY2024": "159.3%", "FY2023": "165%", "FY2022": "168%", "FY2021": "Not disclosed", "FY2020": "Not disclosed", "FY2019": "Not disclosed", "FY2018": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Leverage ratio shown on the 'excluding claims on "
         "central banks' basis for comparability across years (see Leverage Ratio sheet for the 'including' "
         "variant and FY2021-FY2018 basis notes); FY2018's figure (marked *) is instead the single 'CRR leverage "
         "ratio' disclosed that year (an 'including claims on central banks' basis), since no UK-basis 'excluding' "
         "equivalent was published for FY2018 - see the Leverage Ratio sheet's own note. FY2018's 'Other "
         "movements, net' in the equity roll-forward is dominated by the £13,044m ordinary share issue and "
         "capital reorganisation and £2,169m net equity impact of the UK banking business transfer that "
         "established Barclays Bank UK Group in April 2018, not a comparable year-on-year 'other movements' figure.",
)

bw.save("/Users/armaan/code/katalysis/banks/BARCLAYS FINANCIALS.xlsx")
