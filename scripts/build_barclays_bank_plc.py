import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/01026167/filing-history"
AR25_URL = f"{CH_BASE}/MzUyMzkyMDY5MmFkaXF6a2N4/document?format=pdf&download=0"
AR24_URL = f"{CH_BASE}/MzQ2OTM2NDcwM2FkaXF6a2N4/document?format=pdf&download=0"
AR22_URL = f"{CH_BASE}/MzM4Mjg0NjA2M2FkaXF6a2N4/document?format=pdf&download=0"

CASH_FLOW_SOURCES = (
    "Sources — Barclays Bank PLC (the non ring-fenced bank; company no. 01026167) consolidated cash flow "
    "statement, £m, as filed with Companies House:\n"
    f"FY2025, FY2024 & FY2023: Barclays Bank PLC Annual Report 2025 (Group accounts made up to 31 Dec 2025, "
    f"filed 02 Jun 2026), p.289 (Consolidated cash flow statement) — {AR25_URL}\n"
    f"FY2022 & FY2021: Barclays Bank PLC Annual Report 2022 (Group accounts made up to 31 Dec 2022, filed 21 "
    f"Jun 2023), p.171 (Consolidated cash flow statement) — {AR22_URL}\n"
    "Note: FY2021 figures are presented on a restated basis — Barclays Bank PLC restated its FY2021 results "
    "(including litigation and conduct charges) to reflect the impact of the 2022 Over-issuance of Securities "
    "matter in the US; see Note 1a (Restatement of financial statements) in the FY2022 Annual Report. FY2022 "
    "and FY2023 totals are cross-checked and consistent across the FY2022/FY2024/FY2025 Annual Report vintages."
)

def p3_sources(note_extra=""):
    return (
        "Sources — Barclays Bank PLC solo-consolidated capital/liquidity disclosures, from the 'Treasury and "
        "Capital risk' section of the Risk review, as filed with Companies House:\n"
        f"FY2025 & FY2024: Barclays Bank PLC Annual Report 2025, p.220-222 (Liquidity risk: Liquidity Pool/LCR/NSFR) "
        f"and p.231 (Capital risk: Capital ratios/resources/RWAs/Leverage ratio) — {AR25_URL}\n"
        f"FY2023: Barclays Bank PLC Annual Report 2024, p.213-222 (Liquidity risk / Capital risk) — {AR24_URL}\n"
        f"FY2022 & FY2021: Barclays Bank PLC Annual Report 2022, p.115-126 (Liquidity risk / Capital risk) — {AR22_URL}"
        + note_extra
    )

AR24_URL_STATEMENTS = (
    "https://find-and-update.company-information.service.gov.uk/company/01026167/"
    "filing-history/MzQ2OTM2NDcwM2FkaXF6a2N4/document?format=pdf&download=0"
)

STATEMENTS_SOURCES = (
    "Sources — Barclays Bank PLC consolidated financial statements (\"Barclays Bank Group\"), £m, as filed with "
    "Companies House:\n"
    f"FY2025 & FY2024: Barclays Bank PLC Annual Report 2025, p.284-289 (Consolidated income statement / statement "
    f"of comprehensive income / balance sheet / statement of changes in equity) — {AR25_URL}\n"
    f"FY2023 balance sheet & equity comparative: Barclays Bank PLC Annual Report 2024, p.268-271 — {AR24_URL}\n"
    f"FY2022 & FY2021 (restated): Barclays Bank PLC Annual Report 2022, p.166-170 — {AR22_URL}\n"
    "Note: FY2021 figures are restated (2022 Over-issuance of Securities matter in the US; see Note 1a in the "
    "FY2022 Annual Report), consistent with the Cash Flow Statement and Pillar 3 sheets in this workbook. "
    "'UK regulatory levies' was not a separate income statement line until FY2023 - blank for FY2022/FY2021 rather "
    "than folded into another line. FY2021's other comprehensive income detail (currency translation, FVOCI, cash "
    "flow hedge, retirement benefit, own credit rows) is sourced from the same FY2022 Annual Report's restated "
    "2021 comparative column in its Consolidated statement of comprehensive income (p.166); this cross-checks "
    "exactly against the FY2021 movements in the Statement of Changes in Equity."
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 208544, "FY2024": 180365, "FY2023": 189686, "FY2022": 202142, "FY2021": 169085}),
    ("DATA", "Cash collateral and settlement balances", {"FY2025": 124519, "FY2024": 113987, "FY2023": 103708, "FY2022": 107862, "FY2021": 88085}),
    ("DATA", "Debt securities at amortised cost", {"FY2025": 55153, "FY2024": 50227, "FY2023": 39046}),
    ("DATA", "Loans and advances at amortised cost to banks", {"FY2025": 9036, "FY2024": 8780, "FY2023": 9024}),
    ("DATA", "Loans and advances at amortised cost to customers", {"FY2025": 141750, "FY2024": 136047, "FY2023": 137177}),
    ("DATA", "Loans and advances at amortised cost (total, FY2022/FY2021 basis)", {"FY2022": 182507, "FY2021": 145259}),
    ("DATA", "Reverse repurchase agreements and other similar secured lending", {"FY2025": 17662, "FY2024": 3393, "FY2023": 1103, "FY2022": 725, "FY2021": 3177}),
    ("DATA", "Trading portfolio assets", {"FY2025": 189743, "FY2024": 166244, "FY2023": 174566, "FY2022": 133771, "FY2021": 146871}),
    ("DATA", "Financial assets at fair value through the income statement", {"FY2025": 185002, "FY2024": 191845, "FY2023": 204236, "FY2022": 211128, "FY2021": 188226}),
    ("DATA", "Derivative financial instruments", {"FY2025": 252192, "FY2024": 292356, "FY2023": 256111, "FY2022": 302976, "FY2021": 262291}),
    ("DATA", "Financial assets at fair value through other comprehensive income", {"FY2025": 42818, "FY2024": 51010, "FY2023": 51423, "FY2022": 45084, "FY2021": 45908}),
    ("DATA", "Investments in associates and joint ventures", {"FY2025": 14, "FY2024": 14, "FY2023": 22, "FY2022": 26, "FY2021": 24}),
    ("DATA", "Goodwill and intangible assets", {"FY2025": 1303, "FY2024": 1425, "FY2023": 1084, "FY2022": 1665, "FY2021": 1449}),
    ("DATA", "Property, plant and equipment", {"FY2025": 1603, "FY2024": 1546, "FY2023": 1262, "FY2022": 1379, "FY2021": 1248}),
    ("DATA", "Current tax assets", {"FY2025": 376, "FY2024": 785, "FY2023": 546, "FY2022": 737, "FY2021": 589}),
    ("DATA", "Deferred tax assets", {"FY2025": 2936, "FY2024": 4133, "FY2023": 3888, "FY2022": 4583, "FY2021": 2981}),
    ("DATA", "Retirement benefit assets", {"FY2025": 3240, "FY2024": 3263, "FY2023": 3667, "FY2022": 4743, "FY2021": 3879}),
    ("DATA", "Assets included in disposal group classified as held for sale", {"FY2025": 5932, "FY2024": 9854, "FY2023": 3916}),
    ("DATA", "Other assets", {"FY2025": 3650, "FY2024": 3250, "FY2023": 4701, "FY2022": 4209, "FY2021": 2706}),
    ("TOTAL", "Total assets", {"FY2025": 1245473, "FY2024": 1218524, "FY2023": 1185166, "FY2022": 1203537, "FY2021": 1061778}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits at amortised cost from banks", {"FY2025": 20393, "FY2024": 13252, "FY2023": 14598}),
    ("DATA", "Deposits at amortised cost from customers", {"FY2025": 324358, "FY2024": 306124, "FY2023": 287200}),
    ("DATA", "Deposits at amortised cost (total, FY2022/FY2021 basis)", {"FY2022": 291579, "FY2021": 262828}),
    ("DATA", "Cash collateral and settlement balances (liabilities)", {"FY2025": 116811, "FY2024": 104627, "FY2023": 92988, "FY2022": 96811, "FY2021": 79047}),
    ("DATA", "Repurchase agreements and other similar secured borrowing", {"FY2025": 18651, "FY2024": 29397, "FY2023": 28554, "FY2022": 11965, "FY2021": 12769}),
    ("DATA", "Debt securities in issue", {"FY2025": 57229, "FY2024": 35803, "FY2023": 45653, "FY2022": 60012, "FY2021": 48388}),
    ("DATA", "Subordinated liabilities", {"FY2025": 45239, "FY2024": 41875, "FY2023": 35903, "FY2022": 38253, "FY2021": 32185}),
    ("DATA", "Trading portfolio liabilities", {"FY2025": 56829, "FY2024": 56182, "FY2023": 57761, "FY2022": 72460, "FY2021": 53291}),
    ("DATA", "Financial liabilities designated at fair value", {"FY2025": 293527, "FY2024": 279777, "FY2023": 298573, "FY2022": 272055, "FY2021": 251131}),
    ("DATA", "Derivative financial instruments (liabilities)", {"FY2025": 240757, "FY2024": 279331, "FY2023": 249880, "FY2022": 289206, "FY2021": 256523}),
    ("DATA", "Current tax liabilities", {"FY2025": 611, "FY2024": 404, "FY2023": 411, "FY2022": 422, "FY2021": 688}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 1, "FY2024": 2, "FY2023": 3, "FY2022": 9, "FY2021": 6}),
    ("DATA", "Retirement benefit liabilities", {"FY2025": 157, "FY2024": 164, "FY2023": 173, "FY2022": 184, "FY2021": 246}),
    ("DATA", "Liabilities included in disposal group classified as held for sale", {"FY2025": 0, "FY2024": 3726, "FY2023": 3164}),
    ("DATA", "Provisions", {"FY2025": 766, "FY2024": 736, "FY2023": 817, "FY2022": 858, "FY2021": 1110}),
    ("DATA", "Other liabilities", {"FY2025": 7831, "FY2024": 7904, "FY2023": 8984, "FY2022": 10779, "FY2021": 7249}),
    ("TOTAL", "Total liabilities", {"FY2025": 1183160, "FY2024": 1159304, "FY2023": 1124662, "FY2022": 1144584, "FY2021": 1005461}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital and share premium", {"FY2025": 2346, "FY2024": 2348, "FY2023": 2348, "FY2022": 2348, "FY2021": 2348}),
    ("DATA", "Other equity instruments", {"FY2025": 10446, "FY2024": 9604, "FY2023": 10765, "FY2022": 10691, "FY2021": 9693}),
    ("DATA", "Other reserves", {"FY2025": -179, "FY2024": -1302, "FY2023": -363, "FY2022": -1464, "FY2021": 861}),
    ("DATA", "Retained earnings", {"FY2025": 49700, "FY2024": 48570, "FY2023": 47754, "FY2022": 47378, "FY2021": 43415}),
    ("TOTAL", "Total equity", {"FY2025": 62313, "FY2024": 59220, "FY2023": 60504, "FY2022": 58953, "FY2021": 56317}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 1245473, "FY2024": 1218524, "FY2023": 1185166, "FY2022": 1203537, "FY2021": 1061778}),
]

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 23409, "FY2024": 25780, "FY2023": 24261, "FY2022": 11779, "FY2021": 5672}),
    ("DATA", "Interest and similar expense", {"FY2025": -16115, "FY2024": -19035, "FY2023": -17608, "FY2022": -6381, "FY2021": -2599}),
    ("TOTAL", "Net interest income", {"FY2025": 7294, "FY2024": 6745, "FY2023": 6653, "FY2022": 5398, "FY2021": 3073}),
    ("DATA", "Fee and commission income", {"FY2025": 9879, "FY2024": 9486, "FY2023": 8708, "FY2022": 8171, "FY2021": 8581}),
    ("DATA", "Fee and commission expense", {"FY2025": -3326, "FY2024": -3215, "FY2023": -3247, "FY2022": -2745, "FY2021": -1994}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 6553, "FY2024": 6271, "FY2023": 5461, "FY2022": 5426, "FY2021": 6587}),
    ("DATA", "Net trading income", {"FY2025": 7104, "FY2024": 5900, "FY2023": 5980, "FY2022": 7624, "FY2021": 5788}),
    ("DATA", "Net investment income/(expense)", {"FY2025": -72, "FY2024": 69, "FY2023": 112, "FY2022": -323, "FY2021": -80}),
    ("DATA", "Other income", {"FY2025": 48, "FY2024": 52, "FY2023": 62, "FY2022": 69, "FY2021": 40}),
    ("TOTAL", "Total income", {"FY2025": 20927, "FY2024": 19037, "FY2023": 18268, "FY2022": 18194, "FY2021": 15408}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -5585, "FY2024": -5556, "FY2023": -5591, "FY2022": -5192, "FY2021": -4456}),
    ("DATA", "Infrastructure costs", {"FY2025": -816, "FY2024": -795, "FY2023": -1073, "FY2022": -900, "FY2021": -1054}),
    ("DATA", "Administration and general expenses", {"FY2025": -6192, "FY2024": -5894, "FY2023": -5606, "FY2022": -4879, "FY2021": -4375}),
    ("DATA", "UK regulatory levies", {"FY2025": -228, "FY2024": -242, "FY2023": -149}),
    ("DATA", "Litigation and conduct", {"FY2025": -284, "FY2024": -186, "FY2023": -44, "FY2022": -1427, "FY2021": -374}),
    ("TOTAL", "Total operating expenses", {"FY2025": -13105, "FY2024": -12673, "FY2023": -12463, "FY2022": -12398, "FY2021": -10259}),
    ("DATA", "Share of post-tax results of associates and joint ventures", {"FY2025": 0, "FY2024": 0, "FY2023": -4, "FY2022": 3, "FY2021": 4}),
    ("DATA", "Profit/(loss) on disposal of subsidiaries, associates and joint ventures", {"FY2025": -13, "FY2024": 0, "FY2023": 0, "FY2022": 1, "FY2021": -12}),
    ("TOTAL", "Profit before impairment", {"FY2025": 7809, "FY2024": 6364, "FY2023": 5801, "FY2022": 5800, "FY2021": 5141}),
    ("DATA", "Credit impairment (charges)/releases", {"FY2025": -1866, "FY2024": -1617, "FY2023": -1578, "FY2022": -933, "FY2021": 277}),
    ("TOTAL", "Profit before tax", {"FY2025": 5943, "FY2024": 4747, "FY2023": 4223, "FY2022": 4867, "FY2021": 5418}),
    ("DATA", "Taxation", {"FY2025": -1285, "FY2024": -999, "FY2023": -662, "FY2022": -485, "FY2021": -830}),
    ("TOTAL", "Profit after tax", {"FY2025": 4658, "FY2024": 3748, "FY2023": 3561, "FY2022": 4382, "FY2021": 4588}),
    ("SECTION", "Other comprehensive income/(loss)", {}),
    ("DATA", "Currency translation differences", {"FY2025": -1107, "FY2024": -143, "FY2023": -1242, "FY2022": 2411, "FY2021": -155}),
    ("DATA", "Currency translation tax", {"FY2025": -49, "FY2024": 50, "FY2023": 33, "FY2022": 0, "FY2021": 0}),
    ("DATA", "FVOCI debt securities: net gains/(losses) from changes in fair value", {"FY2025": 695, "FY2024": -840, "FY2023": 1142, "FY2022": -6376, "FY2021": -1383}),
    ("DATA", "FVOCI debt securities: net losses/(gains) transferred to net profit on disposal", {"FY2025": 201, "FY2024": -134, "FY2023": -102, "FY2022": 68, "FY2021": -248}),
    ("DATA", "FVOCI debt securities: net (gains)/losses related to (releases of) impairment", {"FY2025": -3, "FY2024": 1, "FY2023": -2, "FY2022": 8, "FY2021": -6}),
    ("DATA", "FVOCI debt securities: net gains/(losses) due to fair value hedging", {"FY2025": 30, "FY2024": 318, "FY2023": -849, "FY2022": 4627, "FY2021": 1105}),
    ("DATA", "FVOCI debt securities: tax", {"FY2025": -256, "FY2024": 181, "FY2023": -54, "FY2022": 449, "FY2021": 170}),
    ("DATA", "Cash flow hedging reserve: net gains/(losses) from changes in fair value", {"FY2025": 2654, "FY2024": -1349, "FY2023": 2506, "FY2022": -7290, "FY2021": -2212}),
    ("DATA", "Cash flow hedging reserve: net (gains)/losses transferred to net profit", {"FY2025": -506, "FY2024": 1950, "FY2023": 1158, "FY2022": 543, "FY2021": -327}),
    ("DATA", "Cash flow hedging reserve: tax", {"FY2025": -607, "FY2024": -154, "FY2023": -1002, "FY2022": 1808, "FY2021": 740}),
    ("TOTAL", "Other comprehensive income/(loss) that may be recycled to profit or loss", {"FY2025": 1052, "FY2024": -120, "FY2023": 1588, "FY2022": -3752, "FY2021": -2316}),
    ("DATA", "Retirement benefit remeasurements", {"FY2025": -13, "FY2024": -419, "FY2023": -1182, "FY2022": -755, "FY2021": 1299}),
    ("DATA", "Own credit", {"FY2025": 89, "FY2024": -1131, "FY2023": -983, "FY2022": 2092, "FY2021": -105}),
    ("DATA", "Own credit / retirement benefit tax", {"FY2025": -29, "FY2024": 430, "FY2023": 609, "FY2022": -156, "FY2021": -563}),
    ("TOTAL", "Other comprehensive income/(loss) not recycled to profit or loss", {"FY2025": 47, "FY2024": -1120, "FY2023": -1556, "FY2022": 1181, "FY2021": 631}),
    ("TOTAL", "Other comprehensive income/(loss) for the year", {"FY2025": 1099, "FY2024": -1240, "FY2023": 32, "FY2022": -2571, "FY2021": -1685}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2025": 5757, "FY2024": 2508, "FY2023": 3593, "FY2022": 1811, "FY2021": 2903}),
]

EQUITY_HEADERS = ["Called up share capital and share premium", "Other equity instruments", "Other reserves", "Retained earnings", "Total equity"]

equity_changes_rows = [
    ("DATA", "Balance as at 1 January 2021", (2348, 8621, 3183, 39558, 53710)),
    ("DATA", "Profit after tax", (None, 631, None, 3957, 4588)),
    ("DATA", "Currency translation movements", (None, None, -155, None, -155)),
    ("DATA", "Fair value through other comprehensive income reserve", (None, None, -362, None, -362)),
    ("DATA", "Cash flow hedges", (None, None, -1799, None, -1799)),
    ("DATA", "Retirement benefit remeasurement", (None, None, None, 644, 644)),
    ("DATA", "Own credit reserve", (None, None, -13, None, -13)),
    ("TOTAL", "Total comprehensive income for the year", (None, 631, -2329, 4601, 2903)),
    ("DATA", "Issue and redemption of other equity instruments", (None, 1072, None, 3, 1075)),
    ("DATA", "Other equity instruments coupons paid", (None, -631, None, None, -631)),
    ("DATA", "Employee share schemes", (None, None, None, 436, 436)),
    ("DATA", "Vesting of Barclays PLC shares under share-based payment schemes", (None, None, None, -356, -356)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, -794, -794)),
    ("DATA", "Dividends on preference shares and other shareholders equity", (None, None, None, -27, -27)),
    ("DATA", "Other reserve movements", (None, None, 7, -6, 1)),
    ("TOTAL", "Balance as at 31 December 2021", (2348, 9693, 861, 43415, 56317)),
    ("DATA", "Profit after tax", (None, 732, None, 3650, 4382)),
    ("DATA", "Currency translation movements", (None, None, 2411, None, 2411)),
    ("DATA", "Fair value through other comprehensive income reserve", (None, None, -1224, None, -1224)),
    ("DATA", "Cash flow hedges", (None, None, -4939, None, -4939)),
    ("DATA", "Retirement benefit remeasurement", (None, None, None, -282, -282)),
    ("DATA", "Own credit reserve", (None, None, 1463, None, 1463)),
    ("TOTAL", "Total comprehensive income for the year", (None, 732, -2289, 3368, 1811)),
    ("DATA", "Issue and redemption of other equity instruments", (None, 998, None, 38, 1036)),
    ("DATA", "Other equity instruments coupons paid", (None, -732, None, None, -732)),
    ("DATA", "Employee share schemes", (None, None, None, 419, 419)),
    ("DATA", "Vesting of Barclays PLC shares under share-based payment schemes", (None, None, None, -413, -413)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, -200, -200)),
    ("DATA", "Dividends on preference shares and other shareholders equity", (None, None, None, -31, -31)),
    ("DATA", "Own credit realisation", (None, None, -36, 36, 0)),
    ("DATA", "Capital contribution from Barclays PLC", (None, None, None, 750, 750)),
    ("DATA", "Other reserve movements", (None, None, None, -4, -4)),
    ("TOTAL", "Balance as at 31 December 2022", (2348, 10691, -1464, 47378, 58953)),
    ("DATA", "Profit after tax", (None, 808, None, 2753, 3561)),
    ("DATA", "Currency translation movements", (None, None, -1209, None, -1209)),
    ("DATA", "Fair value through other comprehensive income reserve", (None, None, 135, None, 135)),
    ("DATA", "Cash flow hedges", (None, None, 2662, None, 2662)),
    ("DATA", "Retirement benefit remeasurement", (None, None, None, -846, -846)),
    ("DATA", "Own credit reserve", (None, None, -710, None, -710)),
    ("TOTAL", "Total comprehensive income for the year", (None, 808, 878, 1907, 3593)),
    ("DATA", "Issue and redemption of other equity instruments", (None, 74, None, -12, 62)),
    ("DATA", "Other equity instruments coupons paid", (None, -808, None, None, -808)),
    ("DATA", "Employee settled Barclays PLC share schemes", (None, None, None, 409, 409)),
    ("DATA", "Vesting of Barclays PLC shares under share-based payment schemes", (None, None, None, -442, -442)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, -1348, -1348)),
    ("DATA", "Dividends on preference shares and other shareholders equity", (None, None, None, -40, -40)),
    ("DATA", "Net equity impact on inter Barclays PLC Group transfers", (None, None, 220, -96, 124)),
    ("DATA", "Other reserve movements", (None, None, 3, -2, 1)),
    ("TOTAL", "Balance as at 31 December 2023", (2348, 10765, -363, 47754, 60504)),
    ("DATA", "Profit after tax", (None, 792, None, 2956, 3748)),
    ("DATA", "Currency translation movements", (None, None, -93, None, -93)),
    ("DATA", "Fair value through other comprehensive income reserve", (None, None, -474, None, -474)),
    ("DATA", "Cash flow hedges", (None, None, 447, None, 447)),
    ("DATA", "Retirement benefit remeasurement", (None, None, None, -298, -298)),
    ("DATA", "Own credit reserve", (None, None, -822, None, -822)),
    ("TOTAL", "Total comprehensive income for the year", (None, 792, -942, 2658, 2508)),
    ("DATA", "Issue and redemption of other equity instruments", (None, -1161, None, -92, -1253)),
    ("DATA", "Other equity instruments coupons paid", (None, -792, None, None, -792)),
    ("DATA", "Employee settled Barclays PLC share schemes", (None, None, None, 531, 531)),
    ("DATA", "Vesting of Barclays PLC shares under share-based payment schemes", (None, None, None, -448, -448)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, -1782, -1782)),
    ("DATA", "Dividends on preference shares and other shareholders equity", (None, None, None, -41, -41)),
    ("DATA", "Other reserve movements", (None, None, 3, -10, -7)),
    ("TOTAL", "Balance as at 31 December 2024", (2348, 9604, -1302, 48570, 59220)),
    ("DATA", "Profit after tax", (None, 783, None, 3875, 4658)),
    ("DATA", "Currency translation movements", (None, None, -1156, None, -1156)),
    ("DATA", "Fair value through other comprehensive income reserve", (None, None, 667, None, 667)),
    ("DATA", "Cash flow hedges", (None, None, 1541, None, 1541)),
    ("DATA", "Retirement benefit remeasurement", (None, None, None, -16, -16)),
    ("DATA", "Own credit reserve", (None, None, 63, None, 63)),
    ("TOTAL", "Total comprehensive income for the year", (None, 783, 1115, 3859, 5757)),
    ("DATA", "Issue and redemption of other equity instruments", (None, 842, None, -5, 837)),
    ("DATA", "Other equity instruments coupons paid", (None, -783, None, None, -783)),
    ("DATA", "Redemption of preference shares", (-2, None, 2, -270, -270)),
    ("DATA", "Employee settled Barclays PLC share schemes", (None, None, None, 667, 667)),
    ("DATA", "Vesting of Barclays PLC shares under share-based payment schemes", (None, None, None, -530, -530)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, -2570, -2570)),
    ("DATA", "Dividends on preference shares and other shareholders equity", (None, None, None, -32, -32)),
    ("DATA", "Other reserve movements", (None, None, 6, 11, 17)),
    ("TOTAL", "Balance as at 31 December 2025", (2346, 10446, -179, 49700, 62313)),
]

ASSET_QUALITY_NOTE = (
    "ASSET QUALITY NOTE - IFRS 9 stage breakdown from the 'Credit risk' section of the Risk review (Loans and "
    "advances at amortised cost, audited), each Annual Report's own tables, closing (31 December) balances only:\n"
    f"FY2025 & FY2024: Barclays Bank PLC Annual Report 2025, p.175-176 (FY2025 stage rollforward) and p.180 "
    f"(FY2024 comparative) — {AR25_URL}\n"
    f"FY2023 (& FY2022 comparative used for the FY2023 rollforward's opening balance): Barclays Bank PLC Annual "
    f"Report 2024, p.175 (Loans and advances at amortised cost stage rollforward, Retail mortgages / Retail "
    f"other / Corporate loans by-product breakdown, summed to a Total across products here) — {AR24_URL}\n"
    f"FY2022 & FY2021: Barclays Bank PLC Annual Report 2022, p.76 (Gross exposure / Impairment allowance / Net "
    f"exposure / Coverage ratio by stage, Home loans / Credit cards, unsecured loans and other retail lending / "
    f"Wholesale loans by-product breakdown, summed to a Total across products here) — {AR22_URL}\n"
    "PRESENTATION NOTE: FY2021-22's own tables use a 3-way product split (Home loans / Credit cards, unsecured "
    "loans and other retail lending / Wholesale loans) that differs from FY2023-25's split (Retail mortgages / "
    "Retail other / Corporate loans) - a genuine, disclosed business change, not a reclassification of the same "
    "book: the FY2024 Annual Report states 'Barclays Bank PLC does not have retail credit card lending', i.e. "
    "the credit card book present in the FY2021-22 'Credit cards, unsecured loans...' line was moved out of this "
    "entity's retail scope by FY2023. Each year's own total is reproduced as its own source states it, not forced "
    "onto a common product taxonomy; the 'Of which' subtotal row is labelled 'Corporate loans (FY2023-25) / "
    "Wholesale loans (FY2021-22)' to flag this is the closest analogous category, not a like-for-like match. "
    "Note the Credit risk section's own 'Loans and advances at amortised cost' gross exposure total (£248,447m "
    "FY2025) is materially larger than the Balance Sheet's 'Loans and advances at amortised cost to customers' "
    "line (£141,750m FY2025) - the Credit risk section evidently uses a broader internal credit-exposure "
    "definition (e.g. including reverse repos/cash collateral classified elsewhere on the Balance Sheet) than the "
    "statutory Balance Sheet caption; both are reproduced as their own source discloses them, not reconciled."
)

asset_quality_rows = [
    ("SECTION", "Loans and advances at amortised cost, by IFRS 9 stage (gross exposure)", {}),
    ("DATA", "Stage 1", {"FY2025": 238476, "FY2024": 215878, "FY2023": 233240, "FY2022": 211001, "FY2021": 186418}),
    ("DATA", "Stage 2", {"FY2025": 7751, "FY2024": 8128, "FY2023": 8430, "FY2022": 14194, "FY2021": 12820}),
    ("DATA", "Stage 3", {"FY2025": 2220, "FY2024": 1795, "FY2023": 1822, "FY2022": 1802, "FY2021": 1731}),
    ("TOTAL", "Total gross exposure", {"FY2025": 248447, "FY2024": 225801, "FY2023": 243492, "FY2022": 226997, "FY2021": 200969}),
    ("SECTION", "Allowance for expected credit losses, by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2025": 133, "FY2024": 140, "FY2023": 178, "FY2022": 321, "FY2021": 221}),
    ("DATA", "Stage 2", {"FY2025": 191, "FY2024": 219, "FY2023": 265, "FY2022": 276, "FY2021": 197}),
    ("DATA", "Stage 3", {"FY2025": 571, "FY2024": 390, "FY2023": 610, "FY2022": 617, "FY2021": 769}),
    ("TOTAL", "Total allowance for expected credit losses", {"FY2025": 895, "FY2024": 749, "FY2023": 1053, "FY2022": 1214, "FY2021": 1187}),
    ("TOTAL", "Net exposure", {"FY2025": 247552, "FY2024": 225052, "FY2023": 242439, "FY2022": 225783, "FY2021": 199782}),
    ("SECTION", "Of which: Corporate loans (FY2023-25) / Wholesale loans (FY2021-22)", {}),
    ("DATA", "Gross exposure", {"FY2025": 240970, "FY2024": 218371, "FY2023": 236273, "FY2022": 215265, "FY2021": 189648}),
    ("DATA", "Allowance for expected credit losses", {"FY2025": 854, "FY2024": 700, "FY2023": 729, "FY2022": 739, "FY2021": 756}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "ECL coverage (Total allowance / Total gross exposure)", {"FY2025": "0.4%", "FY2024": "0.3%", "FY2023": "0.4%", "FY2022": "0.5%", "FY2021": "0.6%"}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / Total gross)", {"FY2025": "0.9%", "FY2024": "0.8%", "FY2023": "0.7%", "FY2022": "0.8%", "FY2021": "0.9%"}),
    ("DATA", "Stage 3 coverage (Stage 3 allowance / Stage 3 gross)", {"FY2025": "25.7%", "FY2024": "21.7%", "FY2023": "33.5%", "FY2022": "34.2%", "FY2021": "44.4%"}),
]

P3_2025_URL = (
    "https://home.barclays/content/dam/home-barclays/documents/investor-relations/ResultAnnouncements/"
    "FullYear2025Results/FY25-BBPLC-Pillar-3.pdf"
)
P3_2024_URL = (
    "https://home.barclays/content/dam/home-barclays/documents/investor-relations/ResultAnnouncements/"
    "FullYear2024Results/FY24-Barclays-Bank-PLC-Pillar-3-Report.pdf"
)
P3_2023_URL = (
    "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/"
    "annual-reports/2023/BB-PLC-Pillar-3-Report-2023.pdf"
)
P3_2022_URL = (
    "https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/"
    "annual-reports/2022/Pillar-3/Barclays-Bank-PLC-Pillar-3-Report%202022.pdf"
)

RWA_BREAKDOWN_SOURCES = (
    "Sources — Barclays Bank PLC's own dedicated Pillar 3 Reports (solo-consolidated basis, matching the Total "
    "RWAs sheet's own basis and figures every year below - confirmed by cross-checking each year's Total row "
    "against the Total RWAs sheet), not the Annual Report's Capital risk section (which discloses only the "
    "aggregate Total RWAs figure and capital ratios, no category breakdown):\n"
    f"FY2025 & FY2024 (DIRECTLY DISCLOSED): Barclays Bank PLC Pillar 3 Report 2025, Table 5 'UK OV1 - Overview of "
    f"risk weighted exposure amounts', p.11 (FY2025 own-year column and FY2024 comparative column, both £m) — "
    f"{P3_2025_URL}\n"
    f"FY2023 (DIRECTLY DISCLOSED, cross-checked against the FY2024 own-year Pillar 3 Report below): Barclays Bank "
    f"PLC Pillar 3 Report 2024, Table 6 'UK OV1 - Overview of risk weighted exposure amounts', p.12 (31.12.2023 "
    f"comparative column) — {P3_2024_URL}\n"
    f"FY2022 (DIRECTLY DISCLOSED): Barclays Bank PLC Pillar 3 Report 2022, Table 6 'UK OV1 - Overview of risk "
    f"weighted exposure amounts', p.11 (31.12.2022 column) — {P3_2022_URL}\n"
    "All four years reconcile exactly to their own Total row and to the Total RWAs sheet's own figure for that "
    "year (£222,247m / £223,648m / £211,193m / £203,833m respectively). Each report's own UK OV1 table additionally "
    "discloses a 'credit valuation adjustment (CVA)' sub-line (row UK8b: £2,150m/£1,938m/£2,510m/£2,465m for "
    "FY2025-FY2022 respectively) nested inside, and already included within, the Counterparty credit risk (CCR) "
    "row shown below - not broken out as its own row here, and not separately additive to the Total.\n\n"
    "FY2021 (DIRECTLY DISCLOSED, but a DIFFERENT table/categorisation - Barclays Bank PLC's dedicated Pillar 3 "
    "Report does not exist as a standalone document for FY2021, so this year is instead sourced from the FY2021 "
    "comparative column of the FY2022 Pillar 3 Report's own separate 'Table 5: RWAs by risk type' - not that "
    "report's UK OV1 table, which only carries a current-year/Q3 comparative, not FY2021): Barclays Bank PLC "
    f"Pillar 3 Report 2022, Table 5 'RWAs by risk type', p.10 ('As at 31 December 2021' row) — {P3_2022_URL}\n"
    "This table splits Credit risk / Counterparty credit risk (CCR) / Market risk each into their Standardised and "
    "internal-model-approach sub-columns (summed here into one Credit risk / CCR / Market risk row apiece) and, "
    "unlike the UK OV1 template, shows Credit valuation adjustment (CVA) as its own separate row rather than a "
    "sub-line nested inside CCR, and carries no separate Securitisation exposures row at all - so FY2021's row "
    "boundaries are NOT directly comparable line-for-line to the UK OV1 rows used for FY2022-FY2025 above (e.g. "
    "FY2021's 'Credit risk' may include exposures the OV1 years would classify as Securitisation); every FY2021 "
    "category is shown exactly as this table discloses it, in its own labelled section below, and its Total row "
    "reconciles exactly to the Total RWAs sheet's own FY2021 figure (£185,467m)."
)
rwa_breakdown_rows = [
    ("SECTION", "UK OV1 — Overview of risk weighted exposure amounts (solo-consolidated)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 109036, "FY2024": 106697, "FY2023": 99934, "FY2022": 105321}),
    ("DATA", "Counterparty credit risk (CCR, incl. CVA)", {"FY2025": 41109, "FY2024": 45839, "FY2023": 37163, "FY2022": 33746}),
    ("DATA", "Settlement risk", {"FY2025": 153, "FY2024": 115, "FY2023": 67, "FY2022": 53}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2025": 23512, "FY2024": 20407, "FY2023": 16159, "FY2022": 15043}),
    ("DATA", "Market risk (position, FX and commodities)", {"FY2025": 25534, "FY2024": 28172, "FY2023": 37010, "FY2022": 29642}),
    ("DATA", "Operational risk", {"FY2025": 22903, "FY2024": 22418, "FY2023": 20860, "FY2022": 20028}),
    ("TOTAL", "Total risk weighted exposure amount", {"FY2025": 222247, "FY2024": 223648, "FY2023": 211193, "FY2022": 203833}),
    ("SECTION", "Table 5: RWAs by risk type (Barclays Bank PLC's own table, solo-consolidated - different "
                "categorisation to the UK OV1 rows above, see sources note)", {}),
    ("DATA", "Credit risk (Standardised + AIRB approaches)", {"FY2021": 100280}),
    ("DATA", "Counterparty credit risk (Standardised + AIRB approaches)", {"FY2021": 31251}),
    ("DATA", "Credit valuation adjustment (CVA)", {"FY2021": 1862}),
    ("DATA", "Settlement risk", {"FY2021": 63}),
    ("DATA", "Market risk (Standardised + IMA approaches)", {"FY2021": 34827}),
    ("DATA", "Operational risk", {"FY2021": 17184}),
    ("TOTAL", "Total RWAs", {"FY2021": 185467}),
]

bw = BankWorkbook(bank_name="Barclays Bank PLC", years=YEARS, header_color="7B241C")

bw.add_balance_sheet_sheet(
    title="Barclays Bank PLC — Balance Sheet",
    subtitle="Barclays Bank PLC Group (consolidated basis), £m. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=220,
    unit_suffix=" (£m)",
)

bw.add_income_statement_sheet(
    title="Barclays Bank PLC — Profit & Loss",
    subtitle="Barclays Bank PLC Group (consolidated basis), £m. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=72,
    source_height=220,
    unit_suffix=" (£m)",
)

bw.add_equity_changes_sheet(
    title="Barclays Bank PLC — Statement of Changes in Equity",
    subtitle="Barclays Bank PLC Group (consolidated basis), £m, chronological, 1 January 2021 - 31 December 2025",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=220,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 5943, "FY2024": 4747, "FY2023": 4223, "FY2022": 4867, "FY2021": 5418}),
    ("SECTION", "Adjustment for non-cash items", {}),
    ("DATA", "Credit impairment charges/(releases)", {"FY2025": 1866, "FY2024": 1617, "FY2023": 1578, "FY2022": 933, "FY2021": -277}),
    ("DATA", "Depreciation, amortisation and impairment of property, plant, equipment and intangibles", {"FY2025": 362, "FY2024": 356, "FY2023": 489, "FY2022": 483, "FY2021": 683}),
    ("DATA", "Provisions and pension charges / other provisions", {"FY2025": 268, "FY2024": 195, "FY2023": 63, "FY2022": 1188, "FY2021": 85}),
    ("DATA", "Net loss/(profit) on disposal of investments and property, plant and equipment", {"FY2025": 13, "FY2024": 9, "FY2023": 7, "FY2022": 8, "FY2021": 12}),
    ("DATA", "Other non-cash movements including exchange rate movements", {"FY2025": 4863, "FY2024": 1835, "FY2023": 7567, "FY2022": -13491, "FY2021": 1968}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Net decrease/(increase) in cash collateral and settlement balances", {"FY2025": 2252, "FY2024": 2060, "FY2023": 31, "FY2022": -1078, "FY2021": 3633}),
    ("DATA", "Net (increase)/decrease in loans and advances at amortised cost", {"FY2025": -7782, "FY2024": -2556, "FY2023": 8313, "FY2022": -30617, "FY2021": -7190}),
    ("DATA", "Net increase/(decrease) in reverse repurchase agreements and other similar secured lending", {"FY2025": -14269, "FY2024": -2290, "FY2023": -378, "FY2022": 2452, "FY2021": 5804}),
    ("DATA", "Net increase in deposits at amortised cost", {"FY2025": 25375, "FY2024": 17578, "FY2023": 10219, "FY2022": 28751, "FY2021": 18132}),
    ("DATA", "Net increase/(decrease) in debt securities in issue", {"FY2025": 21426, "FY2024": -9850, "FY2023": -14359, "FY2022": 11624, "FY2021": 18965}),
    ("DATA", "Net (decrease)/increase in repurchase agreements and other similar secured borrowing", {"FY2025": -10746, "FY2024": 843, "FY2023": 16589, "FY2022": -804, "FY2021": 2326}),
    ("DATA", "Net decrease/(increase) in derivative financial instruments", {"FY2025": 1590, "FY2024": -6794, "FY2023": 7539, "FY2022": -8002, "FY2021": -3655}),
    ("DATA", "Net (increase)/decrease in trading portfolio assets", {"FY2025": -23499, "FY2024": 8322, "FY2023": -40795, "FY2022": 13100, "FY2021": -19207}),
    ("DATA", "Net increase/(decrease) in trading portfolio liabilities", {"FY2025": 647, "FY2024": -1579, "FY2023": -14699, "FY2022": 19169, "FY2021": 7152}),
    ("DATA", "Net increase/(decrease) in financial assets and liabilities at fair value through the income statement", {"FY2025": 20593, "FY2024": -6415, "FY2023": 33410, "FY2022": -1978, "FY2021": -14960}),
    ("DATA", "Net increase in other assets", {"FY2025": -167, "FY2024": -3962, "FY2023": -1301, "FY2022": -3311, "FY2021": -2235}),
    ("DATA", "Net decrease/increase in other liabilities", {"FY2025": -384, "FY2024": -1440, "FY2023": -1864, "FY2022": 1834, "FY2021": 2082}),
    ("DATA", "Corporate income tax paid", {"FY2025": -248, "FY2024": -685, "FY2023": -265, "FY2022": -144, "FY2021": -1239}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": 28103, "FY2024": 1991, "FY2023": 16367, "FY2022": 24984, "FY2021": 17497}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities at amortised cost", {"FY2025": -15658, "FY2024": -27617, "FY2023": -14901, "FY2022": -20014, "FY2021": -6931}),
    ("DATA", "Proceeds from redemption or sale of debt securities at amortised cost", {"FY2025": 9828, "FY2024": 16922, "FY2023": 2681, "FY2022": 12925, "FY2021": 2424}),
    ("DATA", "Purchase of financial assets at fair value through other comprehensive income", {"FY2025": -29747, "FY2024": -52347, "FY2023": -50254, "FY2022": -43139, "FY2021": -44058}),
    ("DATA", "Proceeds from sale or redemption of financial assets at fair value through other comprehensive income", {"FY2025": 38246, "FY2024": 51803, "FY2023": 44126, "FY2022": 42157, "FY2021": 47601}),
    ("DATA", "Purchase of property, plant and equipment and investment in intangibles", {"FY2025": -574, "FY2024": -512, "FY2023": -439, "FY2022": -540, "FY2021": -758}),
    ("DATA", "Acquisition of business", {"FY2025": 0, "FY2024": -232}),
    ("DATA", "Disposal of subsidiaries and associates, net of cash disposed", {"FY2022": 0, "FY2021": 65}),
    ("DATA", "Other cash flows associated with investing activities", {"FY2024": 2749, "FY2022": 0, "FY2021": 4}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": 2095, "FY2024": -9234, "FY2023": -18787, "FY2022": -8611, "FY2021": -1653}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid and other coupon payments on equity instruments", {"FY2025": -3385, "FY2024": -2615, "FY2023": -2196, "FY2022": -963, "FY2021": -1452}),
    ("DATA", "Issuance of subordinated liabilities", {"FY2025": 9808, "FY2024": 11222, "FY2023": 5986, "FY2022": 15381, "FY2021": 9099}),
    ("DATA", "Redemption of subordinated liabilities", {"FY2025": -5665, "FY2024": -5067, "FY2023": -7431, "FY2022": -8367, "FY2021": -7241}),
    ("DATA", "Issue of shares and other equity instruments", {"FY2025": 2770, "FY2024": 970, "FY2023": 2499, "FY2022": 3134, "FY2021": 1072}),
    ("DATA", "Repurchase of shares and other equity instruments", {"FY2025": -2198, "FY2024": -2131, "FY2023": -2425, "FY2022": -2136, "FY2021": 0}),
    ("DATA", "Capital contribution", {"FY2022": 750}),
    ("DATA", "Vesting of employee share schemes", {"FY2025": -530, "FY2024": -448, "FY2023": -442, "FY2022": -413, "FY2021": -356}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": 800, "FY2024": 1931, "FY2023": -4009, "FY2022": 7386, "FY2021": 1122}),
    ("DATA", "Effect of exchange rates on cash and cash equivalents", {"FY2025": -1740, "FY2024": -2405, "FY2023": -5013, "FY2022": 10235, "FY2021": -4231}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 29258, "FY2024": -7717, "FY2023": -11442, "FY2022": 33994, "FY2021": 12735}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 200695, "FY2024": 208412, "FY2023": 219854, "FY2022": 185860, "FY2021": 173125}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 229953, "FY2024": 200695, "FY2023": 208412, "FY2022": 219854, "FY2021": 185860}),
    ("SECTION", "Cash and cash equivalents at end of year comprise", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 208544, "FY2024": 180365, "FY2023": 189686, "FY2022": 202142, "FY2021": 169085}),
    ("DATA", "Loans and advances to banks with original maturity of three months or less", {"FY2025": 7802, "FY2024": 7758, "FY2023": 7117, "FY2022": 6229, "FY2021": 6473}),
    ("DATA", "Cash collateral balances with central banks with original maturity of three months or less", {"FY2025": 11625, "FY2024": 11025, "FY2023": 10325, "FY2022": 10625, "FY2021": 9690}),
    ("DATA", "Treasury and other eligible bills with original maturity of three months or less", {"FY2025": 1982, "FY2024": 1547, "FY2023": 1284, "FY2022": 858, "FY2021": 612}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 229953, "FY2024": 200695, "FY2023": 208412, "FY2022": 219854, "FY2021": 185860}),
]

bw.add_cash_flow_sheet(
    title="Barclays Bank PLC — Consolidated Cash Flow Statement",
    subtitle="Barclays Bank PLC Group (consolidated basis), £m unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=100,
    unit_suffix=" (£m)",
)

bw.add_asset_quality_sheet(
    title="Barclays Bank PLC — Asset Quality",
    subtitle="Barclays Bank PLC Group (consolidated basis), £m. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_NOTE,
    first_col_width=62,
    source_height=220,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 / capital metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Solo-consolidated basis, {unit}" if unit else "Solo-consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=100)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 28177, "FY2024": 26995, "FY2023": 25470, "FY2022": 25907, "FY2021": 23928})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "12.7%", "FY2024": "12.1%", "FY2023": "12.1%", "FY2022": "12.7%", "FY2021": "12.9%"})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 (T1) capital", {"FY2025": 35848, "FY2024": 33787, "FY2023": 33864, "FY2022": 34139, "FY2021": 32395})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 (T1) ratio", {"FY2025": "16.1%", "FY2024": "15.1%", "FY2023": "16.0%", "FY2022": "16.7%", "FY2021": "17.5%"})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report.",
)

metric(
    "Total Capital", "£m",
    [("Total regulatory capital", {"FY2025": 42129, "FY2024": 40444, "FY2023": 40530, "FY2022": 42321, "FY2021": 37954})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total regulatory capital ratio", {"FY2025": "19.0%", "FY2024": "18.1%", "FY2023": "19.2%", "FY2022": "20.8%", "FY2021": "20.5%"})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk weighted assets (RWAs)", {"FY2025": 222247, "FY2024": 223648, "FY2023": 211193, "FY2022": 203833, "FY2021": 185467})],
    p3_sources(),
    note="FY2021 figure is restated (Over-issuance of Securities matter); see Note 1a in the FY2022 Annual Report. "
         "FY2024 comparative in the FY2025 Annual Report is calculated applying UK CRR transitional arrangements "
         "(IFRS 9 transitional relief and grandfathering of certain capital instruments), which ceased to apply "
         "from 1 January/29 June 2025.",
)

bw.add_rwa_breakdown_sheet(
    title="Barclays Bank PLC — RWA Breakdown",
    subtitle="Solo-consolidated basis, £m. FY2025-FY2022 per the UK OV1 template; FY2021 per a differently-"
              "categorised table - see source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=240,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("UK leverage ratio (%)", {"FY2025": "5.8%", "FY2024": "5.8%", "FY2023": "6.0%", "FY2022": "4.6%", "FY2021": "3.7%"}),
        ("Tier 1 (T1) capital used in leverage calculation (£m)", {"FY2025": 56465, "FY2024": 54713, "FY2023": 55560, "FY2022": 34139, "FY2021": 32395}),
        ("UK leverage exposure (£m)", {"FY2025": 980935, "FY2024": 946809, "FY2023": 924826, "FY2022": 742730, "FY2021": 883371}),
    ],
    p3_sources(),
    note="Basis changes across the period: FY2021 is a CRR leverage ratio (Barclays Bank PLC was not subject to "
         "the UK leverage framework until 1 January 2022; the UK-framework equivalent was disclosed as 4.1%, "
         "£767.6bn exposure). FY2022 is a UK leverage ratio on a solo-consolidated basis. From FY2023 onward, "
         "leverage minimum requirements — and the disclosed ratio — moved to a Barclays Bank PLC sub-consolidated "
         "basis (PRA approval granted 20 December 2022, effective 1 January 2023). These bases are not directly "
         "comparable year-on-year.",
)

metric(
    "LCR", "£bn / %",
    [
        ("Barclays Bank PLC DoLSub Liquidity Pool (£bn)", {"FY2025": 229.9, "FY2024": 179.3, "FY2023": 176, "FY2022": 191, "FY2021": 167}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "149.7%", "FY2024": "147.9%", "FY2023": "151%", "FY2022": "148%", "FY2021": "140%"}),
    ],
    p3_sources(),
    note="LCR is an average of the last 12 spot month-end ratios for the Barclays Bank PLC Domestic Liquidity "
         "Sub-Group (DoLSub, comprising Barclays Bank PLC and Barclays Capital Securities Limited). Barclays "
         "prospectively changed its methodology for calculating net stress outflows on secured financing "
         "transactions from June 2025; the FY2025 Annual Report re-presents FY2024 on the new basis (147.9%, "
         "used here for comparability) — the FY2024 Annual Report originally reported FY2024 LCR as 157% "
         "(FY2023 comparator in that report: 151%, unchanged).",
)

metric(
    "NSFR", "£bn / %",
    [
        ("Total Available Stable Funding (£bn)", {"FY2025": 381, "FY2024": 372, "FY2023": 339, "FY2022": 310}),
        ("Total Required Stable Funding (£bn)", {"FY2025": 337, "FY2024": 333, "FY2023": 308, "FY2022": 288}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "113%", "FY2024": "112%", "FY2023": "110%", "FY2022": "108%", "FY2021": "Not publicly disclosed"}),
    ],
    p3_sources(),
    note="NSFR is an average of the last four spot quarter-end ratios. It was not a UK regulatory requirement "
         "as at FY2021 (the UK NSFR regime took effect from 1 January 2022), so no FY2021 figure is available.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "MREL (Minimum Requirement for own funds and Eligible Liabilities) is set and disclosed "
                      "at the Barclays PLC resolution-group level, not for Barclays Bank PLC as an individual "
                      "operating subsidiary. No MREL ratio for Barclays Bank PLC specifically was found in its "
                      "Annual Reports for FY2021-FY2025.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1245473, "FY2024": 1218524, "FY2023": 1185166, "FY2022": 1203537, "FY2021": 1061778}),
        ("Loans and advances at amortised cost to customers", {"FY2025": 141750, "FY2024": 136047, "FY2023": 137177}),
        ("Customer deposits", {"FY2025": 324358, "FY2024": 306124, "FY2023": 287200}),
        ("Total equity", {"FY2025": 62313, "FY2024": 59220, "FY2023": 60504, "FY2022": 58953, "FY2021": 56317}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 20927, "FY2024": 19037, "FY2023": 18268, "FY2022": 18194, "FY2021": 15408}),
        ("Total operating expenses", {"FY2025": -13105, "FY2024": -12673, "FY2023": -12463, "FY2022": -12398, "FY2021": -10259}),
        ("Profit after tax", {"FY2025": 4658, "FY2024": 3748, "FY2023": 3561, "FY2022": 4382, "FY2021": 4588}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 59220, "FY2024": 60504, "FY2023": 58953, "FY2022": 56317, "FY2021": 53710}),
        ("Total comprehensive income", {"FY2025": 5757, "FY2024": 2508, "FY2023": 3593, "FY2022": 1811, "FY2021": 2903}),
        ("Other movements, net", {"FY2025": -2664, "FY2024": -3792, "FY2023": -2042, "FY2022": 825, "FY2021": -296}),
        ("Closing equity", {"FY2025": 62313, "FY2024": 59220, "FY2023": 60504, "FY2022": 58953, "FY2021": 56317}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": 28103, "FY2024": 1991, "FY2023": 16367, "FY2022": 24984, "FY2021": 17497}),
        ("Net cash from investing activities", {"FY2025": 2095, "FY2024": -9234, "FY2023": -18787, "FY2022": -8611, "FY2021": -1653}),
        ("Net cash from financing activities", {"FY2025": 800, "FY2024": 1931, "FY2023": -4009, "FY2022": 7386, "FY2021": 1122}),
        ("Cash and cash equivalents at end of year", {"FY2025": 229953, "FY2024": 200695, "FY2023": 208412, "FY2022": 219854, "FY2021": 185860}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "12.7%", "FY2024": "12.1%", "FY2023": "12.1%", "FY2022": "12.7%", "FY2021": "12.9%"}),
        ("Tier 1 Ratio", {"FY2025": "16.1%", "FY2024": "15.1%", "FY2023": "16.0%", "FY2022": "16.7%", "FY2021": "17.5%"}),
        ("Total Capital Ratio", {"FY2025": "19.0%", "FY2024": "18.1%", "FY2023": "19.2%", "FY2022": "20.8%", "FY2021": "20.5%"}),
        ("Leverage Ratio", {"FY2025": "5.8%", "FY2024": "5.8%", "FY2023": "6.0%", "FY2022": "4.6%", "FY2021": "3.7%"}),
        ("LCR", {"FY2025": "149.7%", "FY2024": "147.9%", "FY2023": "151%", "FY2022": "148%", "FY2021": "140%"}),
        ("NSFR", {"FY2025": "113%", "FY2024": "112%", "FY2023": "110%", "FY2022": "108%", "FY2021": "Not publicly disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. FY2021 capital figures are restated (Over-issuance "
         "of Securities matter). Leverage ratio basis changes year-on-year (see Leverage Ratio sheet).",
)

bw.save("/Users/armaan/code/katalysis/banks/BARCLAYS BANK PLC FINANCIALS.xlsx")
