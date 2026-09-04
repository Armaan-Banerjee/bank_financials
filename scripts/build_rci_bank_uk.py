import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]

AR24_URL = "https://find-and-update.company-information.service.gov.uk/company/11429127/filing-history/MzQ4MzYzODUzNmFkaXF6a2N4/document?download=0&format=pdf"
AR23_URL = "https://find-and-update.company-information.service.gov.uk/company/11429127/filing-history/MzQyNTg5Mjk5OWFkaXF6a2N4/document?download=0&format=pdf"
AR22_URL = "https://find-and-update.company-information.service.gov.uk/company/11429127/filing-history/MzM4MDE0Nzg1OGFkaXF6a2N4/document?download=0&format=pdf"
AR21_URL = "https://find-and-update.company-information.service.gov.uk/company/11429127/filing-history/MzM0MjczNjEyNGFkaXF6a2N4/document?download=0&format=pdf"
AR20_URL = "https://find-and-update.company-information.service.gov.uk/company/11429127/filing-history/MzMwNzExODk0NmFkaXF6a2N4/document?download=0&format=pdf"
P3_24_URL = "https://www.rcibank.co.uk/sites/default/files/2025-12/Pillar%20III%20Disclosures%20FY%202024%20-%20External.pdf"
P3_23_URL = "https://www.rcibank.co.uk/sites/default/files/2024-11/Pillar%20III%20Disclosures%20FY%202023%20-%20final%20%28external%20version%29%20signed%201_0.pdf"
FACTS_URL = "https://www.rcibank.co.uk/about-us/facts-and-figures"

ENTITY_NOTE = (
    "ENTITY NOTE: RCI Bank UK Limited (company 11429127; FRN 815220) is the PRA/FCA-authorised bank. "
    "The cash-flow statement uses the Group column of RCI Bank UK Limited's statutory accounts: RCI Bank UK, "
    "100%-owned RCI Financial Services Limited, 85%-owned Mobilize Lease & Co UK Limited and controlled "
    "securitisation SPVs. The accounts also print a Company column, but the Group column is used consistently "
    "because the bank's lending and lease operations sit in its subsidiaries. FY2024 is the latest available "
    "statutory filing; FY2025 accounts were not yet filed at the time of build. All five reports are scanned PDFs "
    "and were OCR-processed; values were cross-checked against the printed totals and later comparative columns."
)

CASH_SOURCES = (
    "Sources - RCI Bank UK Limited Group consolidated cash flows, £'000 (Group column):\n"
    f"FY2024 & FY2023 comparative: Annual Report and Financial Statements for year ended 31 December 2024, "
    f"printed pp.46-47 (PDF pp.45-46) - {AR24_URL}\n"
    f"FY2023 & FY2022 comparative: Annual Report and Financial Statements for year ended 31 December 2023, "
    f"printed pp.39-40 (PDF pp.38-39) - {AR23_URL}\n"
    f"FY2022 & FY2021 comparative: Annual Report and Financial Statements for year ended 31 December 2022, "
    f"printed pp.36-37 (PDF pp.35-36) - {AR22_URL}\n"
    f"FY2021 & FY2020 comparative: Annual Report and Financial Statements for year ended 31 December 2021, "
    f"printed pp.37-38 (PDF pp.36-37) - {AR21_URL}\n"
    f"FY2020: Annual Report and Financial Statements for year ended 31 December 2020, printed pp.33-34 "
    f"(PDF pp.32-33) - {AR20_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "DATA QUALITY NOTE: The OCR of the FY2022 report rendered the Group FY2022 proceeds from investment "
    "securities as £4,024,803. The FY2023 report's clean comparative column prints £1,024,803, which agrees "
    "with the reported FY2022 investing subtotal of (£898) and the cash movement. The corrected £1,024,803 is "
    "used here; this is a source/OCR correction, not an estimate."
)

bw = BankWorkbook(bank_name="RCI Bank UK Limited", years=YEARS, header_color="174A5B")

rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2024": 37515, "FY2023": 63631, "FY2022": 131197, "FY2021": 127547, "FY2020": 71623}),
    ("DATA", "Depreciation and amortisation", {"FY2024": 104189, "FY2023": 92713, "FY2022": 52443, "FY2021": 35811, "FY2020": 28245}),
    ("DATA", "Net book value of property, plant and equipment disposed", {"FY2021": 36583, "FY2020": 45774}),
    ("DATA", "Impairment of financial assets", {"FY2024": 57, "FY2023": 57, "FY2022": 37, "FY2021": 65, "FY2020": -151}),
    ("DATA", "Loss/(gain) on fair value adjustment - derivatives", {"FY2023": 30339, "FY2021": -11969, "FY2020": 55}),
    ("DATA", "Derivative financial instruments", {"FY2024": 18732, "FY2022": -47914, "FY2020": 228}),
    ("DATA", "Interest income", {"FY2022": 2018, "FY2021": -23, "FY2020": -1458}),
    ("DATA", "Interest expenses", {"FY2023": 7864, "FY2022": -2051, "FY2021": 1732, "FY2020": 1737}),
    ("DATA", "Profit on disposal of investment securities", {"FY2024": -6008, "FY2023": -4940}),
    ("DATA", "Provision for liabilities", {"FY2024": 73644}),
    ("DATA", "Other non-cash or non-operating items", {"FY2024": -462, "FY2023": 100}),
    ("DATA", "Loans and advances to customers", {"FY2024": -245366, "FY2023": -635081, "FY2022": -890629, "FY2021": 72609, "FY2020": 412363}),
    ("DATA", "NBV of vehicles transferred to inventory", {"FY2024": 125434, "FY2023": 83828, "FY2022": 74920}),
    ("DATA", "Inventory", {"FY2024": -28631, "FY2023": -8468, "FY2022": -6497, "FY2021": 12434, "FY2020": 14535}),
    ("DATA", "Other assets", {"FY2024": -70864, "FY2023": -30614, "FY2022": -18531, "FY2021": -18531, "FY2020": -20422}),
    ("DATA", "Other liabilities", {"FY2024": 2516, "FY2023": 5379, "FY2022": 73787, "FY2021": -25651, "FY2020": -4527}),
    ("DATA", "Pension contributions paid and amounts recognised in income statement", {"FY2024": -2468, "FY2023": -2366, "FY2022": -128, "FY2021": -104, "FY2020": -103}),
    ("DATA", "Customer deposits", {"FY2024": 183943, "FY2023": 654141, "FY2022": 1211022, "FY2021": -219850, "FY2020": 195717}),
    ("DATA", "Bank deposits", {"FY2024": -440, "FY2023": -200051, "FY2022": -89121, "FY2021": 704439, "FY2020": -37451}),
    ("DATA", "Loan to subsidiary", {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Other operating items included in reported subtotal", {"FY2024": 227, "FY2021": -2594, "FY2020": -47952}),
    ("TOTAL", "Cash generated by operations", {"FY2024": 192018, "FY2023": 56532, "FY2022": 490553, "FY2021": 712498, "FY2020": 658213}),
    ("DATA", "Income taxes paid", {"FY2024": -31905, "FY2023": -17777, "FY2022": -18403, "FY2021": -23266, "FY2020": -15308}),
    ("TOTAL", "Net cash from operating activities", {"FY2024": 160113, "FY2023": 38755, "FY2022": 472150, "FY2021": 689232, "FY2020": 642905}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2024": -334148, "FY2023": -331888, "FY2022": -265940, "FY2021": -132014, "FY2020": -122580}),
    ("DATA", "Intangible asset", {"FY2024": -980, "FY2023": -1000}),
    ("DATA", "Purchasing of investment securities", {"FY2024": -244257, "FY2023": -231803, "FY2022": -761812, "FY2021": -430074, "FY2020": -1437759}),
    ("DATA", "Proceeds from investment securities", {"FY2024": 232036, "FY2023": 290000, "FY2022": 1024803, "FY2021": 10000, "FY2020": 1988828}),
    ("DATA", "Profit on disposal of investment securities", {"FY2022": 2051}),
    ("DATA", "Investment in associate", {"FY2023": -15980}),
    ("DATA", "Non-controlling interest subscription", {"FY2023": 225}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2021": 0, "FY2020": 49409}),
    ("DATA", "Interest income", {"FY2021": 23, "FY2020": -1458}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2024": -347349, "FY2023": -290446, "FY2022": -898, "FY2021": -552065, "FY2020": 476440}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Proceeds from subordinated debt", {"FY2020": 40000}),
    ("DATA", "Debt securities issued/(redeemed)", {"FY2024": 100000, "FY2023": 100000, "FY2021": -400000, "FY2020": -200000}),
    ("DATA", "Issuing of ordinary share capital", {}),
    ("DATA", "Dividends paid", {"FY2021": -86862, "FY2020": -51400}),
    ("DATA", "Property lease rent paid", {"FY2024": -1188, "FY2023": -672, "FY2022": -654, "FY2021": -935}),
    ("DATA", "Interest on property lease", {"FY2024": -198, "FY2023": -221, "FY2022": -242}),
    ("DATA", "Other financing items included in reported subtotal", {"FY2022": -7133, "FY2020": 60000}),
    ("TOTAL", "Net cash (used in)/generated from financing activities", {"FY2024": 98614, "FY2023": 99107, "FY2022": -8029, "FY2021": -487797, "FY2020": -151400}),
    ("TOTAL", "Net increase/(decrease) in cash and cash at central banks", {"FY2024": -88622, "FY2023": -152584, "FY2022": 463223, "FY2021": -350630, "FY2020": 967945}),
    ("DATA", "Cash and cash at central banks at 1 January", {"FY2024": 1048510, "FY2023": 1201094, "FY2022": 737871, "FY2021": 1088501, "FY2020": 120556}),
    ("TOTAL", "Cash and cash at central banks at 31 December", {"FY2024": 959888, "FY2023": 1048510, "FY2022": 1201094, "FY2021": 737871, "FY2020": 1088501}),
]

BS_SOURCES = (
    "Sources - RCI Bank UK Limited Group consolidated balance sheet, £'000 (Group column):\n"
    f"FY2024 & FY2023 comparative: Annual Report and Financial Statements for year ended 31 December 2024, "
    f"printed p.43 (PDF p.42), Company and Consolidated Balance Sheet - {AR24_URL}\n"
    f"FY2022 & FY2021 comparative: Annual Report and Financial Statements for year ended 31 December 2022, "
    f"printed p.34 (PDF p.33), Company and Consolidated Balance Sheet - {AR22_URL}\n"
    f"FY2020: Annual Report and Financial Statements for year ended 31 December 2020, printed p.31 (PDF p.30), "
    f"Company and Consolidated Balance Sheet - {AR20_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: Deferred tax asset, Investment in associate and Intangible assets are only disclosed as "
    "separate Group balance sheet lines from FY2023 (associate) / FY2025-vintage FY2024 report (intangibles) "
    "onward; earlier years genuinely did not carry these balances as separate lines and are left blank, not "
    "zero. FY2020's Group Investment securities line is a genuine nil ('-' in the source) while FY2019's "
    "comparative was £548,818k - this is a real year-on-year balance sheet movement, not a data gap."
)

BS_ROWS = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash at central banks", {"FY2024": 959888, "FY2023": 1048510, "FY2022": 1201094, "FY2021": 737871, "FY2020": 1088501}),
    ("DATA", "Derivative financial instruments", {"FY2024": 11829, "FY2023": 37622, "FY2022": 55475, "FY2021": 10254, "FY2020": 1388}),
    ("DATA", "Investment securities", {"FY2024": 123749, "FY2023": 105575, "FY2022": 157926, "FY2021": 419939, "FY2020": 0}),
    ("DATA", "Inventory", {"FY2024": 46891, "FY2023": 18260, "FY2022": 9792, "FY2021": 3295, "FY2020": 15729}),
    ("DATA", "Loans and advances to customers", {"FY2024": 5170678, "FY2023": 4925312, "FY2022": 4290231, "FY2021": 3414627, "FY2020": 3487236}),
    ("DATA", "Property, plant and equipment", {"FY2024": 679541, "FY2023": 575015, "FY2022": 419670, "FY2021": 266068, "FY2020": 206448}),
    ("DATA", "Current tax asset", {"FY2022": 0, "FY2021": 1273}),
    ("DATA", "Deferred tax asset", {"FY2024": 31036, "FY2023": 18541, "FY2022": 7203, "FY2021": 4748, "FY2020": 3967}),
    ("DATA", "Other assets", {"FY2024": 257616, "FY2023": 186752, "FY2022": 156138, "FY2021": 137607, "FY2020": 119076}),
    ("DATA", "Investment in associate", {"FY2024": 16311, "FY2023": 15901}),
    ("DATA", "Intangible assets", {"FY2024": 1712, "FY2023": 1000}),
    ("TOTAL", "Total assets", {"FY2024": 7299251, "FY2023": 6932488, "FY2022": 6297529, "FY2021": 4995682, "FY2020": 4922345}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from customers", {"FY2024": 4978566, "FY2023": 4794623, "FY2022": 4140482, "FY2021": 2929460, "FY2020": 3149310}),
    ("DATA", "Deposits from banks", {"FY2024": 564909, "FY2023": 565349, "FY2022": 765400, "FY2021": 854521, "FY2020": 150082}),
    ("DATA", "Derivative financial instruments", {"FY2024": 5900, "FY2023": 12961, "FY2022": 475, "FY2021": 3168, "FY2020": 8865}),
    ("DATA", "Debt securities issued", {"FY2024": 700000, "FY2023": 600000, "FY2022": 500000, "FY2021": 400000, "FY2020": 800000}),
    ("DATA", "Current tax liabilities", {"FY2024": 5723, "FY2023": 13994, "FY2022": 6544, "FY2020": 452}),
    ("DATA", "Other liabilities", {"FY2024": 246255, "FY2023": 245125, "FY2022": 232934, "FY2021": 158024, "FY2020": 182878}),
    ("DATA", "Provision for liabilities", {"FY2024": 73644}),
    ("DATA", "Retirement benefit liability", {"FY2024": 785, "FY2023": 4297, "FY2022": 4827, "FY2021": 9172, "FY2020": 14121}),
    ("TOTAL", "Total liabilities", {"FY2024": 6575782, "FY2023": 6236349, "FY2022": 5650662, "FY2021": 4354345, "FY2020": 4305708}),
    ("SECTION", "Equity", {}),
    ("DATA", "Issued/ordinary share capital", {"FY2024": 290400, "FY2023": 290400, "FY2022": 290400, "FY2021": 290400, "FY2020": 290400}),
    ("DATA", "Retained earnings", {"FY2024": 436990, "FY2023": 409935, "FY2022": 360048, "FY2021": 358442, "FY2020": 338171}),
    ("DATA", "Non-controlling interests", {"FY2024": -337, "FY2023": 125}),
    ("DATA", "Other reserves", {"FY2024": -3584, "FY2023": -4321, "FY2022": -3581, "FY2021": -7505, "FY2020": -11934}),
    ("TOTAL", "Total equity", {"FY2024": 723469, "FY2023": 696139, "FY2022": 646867, "FY2021": 641337, "FY2020": 616637}),
    ("TOTAL", "Total liabilities and equity", {"FY2024": 7299251, "FY2023": 6932488, "FY2022": 6297529, "FY2021": 4995682, "FY2020": 4922345}),
]

bw.add_balance_sheet_sheet(
    title="RCI Bank UK Limited - Group Balance Sheet",
    subtitle="Company and Consolidated Statement of Financial Position, Group column, £'000; FY2020-FY2024. See source note.",
    rows=BS_ROWS, sources_text=BS_SOURCES, first_col_width=58, source_height=200, unit_suffix=" (£'000)",
)

PL_SOURCES = (
    "Sources - RCI Bank UK Limited Group consolidated statement of profit or loss, £'000 (Group column):\n"
    f"FY2024 & FY2023 comparative: Annual Report and Financial Statements for year ended 31 December 2024, "
    f"printed p.41 (PDF p.40), Consolidated Statement of Profit or Loss - {AR24_URL}\n"
    f"FY2022 & FY2021 comparative: Annual Report and Financial Statements for year ended 31 December 2022, "
    f"printed p.32 (PDF p.31), Consolidated Statement of Profit or Loss - {AR22_URL}\n"
    f"FY2020: Annual Report and Financial Statements for year ended 31 December 2020, printed p.29 (PDF p.28), "
    f"Consolidated Statement of Profit or Loss - {AR20_URL}\n"
    f"Other comprehensive income lines: the equivalent Consolidated Statement of Other Comprehensive Income in "
    f"each of the above reports (one page after the Statement of Profit or Loss).\n\n" + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: FY2020's income statement used an older structure ('Other profits/(losses) from the "
    "sale of Operating Lease vehicles' and 'from the sale of HP & PCP vehicles', no separate Cost of sales line "
    "or Revenue on sale of inventories line); FY2021 onward use 'Revenue on sale of inventories' and 'Cost of "
    "sales' instead. Both are the bank's own as-reported structure for that year, not a reclassification by "
    "this workbook. 'Profit after tax for the financial year' is the Group total (i.e. after minority interest), "
    "matching 'Profit for the year' on the Statement of Other Comprehensive Income and the Statement of Changes "
    "in Equity."
)

PL_ROWS = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2024": 437390, "FY2023": 354682, "FY2022": 198217, "FY2021": 136838, "FY2020": 179280}),
    ("DATA", "Interest expense", {"FY2024": -313697, "FY2023": -243245, "FY2022": -95917, "FY2021": -43321, "FY2020": -64873}),
    ("TOTAL", "Net interest income", {"FY2024": 123693, "FY2023": 111437, "FY2022": 102300, "FY2021": 93517, "FY2020": 114407}),
    ("DATA", "Fee and commission income", {"FY2024": 12118, "FY2023": 12651, "FY2022": 9211, "FY2021": 9764, "FY2020": 7287}),
    ("DATA", "Fee and commission expense", {"FY2024": -931, "FY2023": -689, "FY2022": -119, "FY2021": -870, "FY2020": -535}),
    ("TOTAL", "Net fee and commission income", {"FY2024": 11187, "FY2023": 11962, "FY2022": 9092, "FY2021": 8894, "FY2020": 6752}),
    ("DATA", "Operating lease rentals", {"FY2024": 141203, "FY2023": 105791, "FY2022": 71833, "FY2021": 50490, "FY2020": 43027}),
    ("DATA", "Revenue on sale of inventories", {"FY2024": 115479, "FY2023": 70967, "FY2022": 71702, "FY2021": 114906}),
    ("DATA", "Other profits/(losses) from sale of Operating Lease vehicles", {"FY2020": 3987}),
    ("DATA", "Other profits/(losses) from sale of HP & PCP vehicles", {"FY2020": 28761}),
    ("TOTAL", "Total income", {"FY2024": 391562, "FY2023": 300157, "FY2022": 254927, "FY2021": 267807, "FY2020": 164186}),
    ("SECTION", "Costs and provisions", {}),
    ("DATA", "Cost of sales", {"FY2024": -115943, "FY2023": -59187, "FY2022": -47242, "FY2021": -83972}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2024": -104189, "FY2023": -92713, "FY2022": -52443, "FY2021": -35811, "FY2020": -28245}),
    ("DATA", "Operating expenses", {"FY2024": -70151, "FY2023": -59749, "FY2022": -43281, "FY2021": -44355, "FY2020": -55162}),
    ("DATA", "Change in provision for liabilities", {"FY2024": -73644}),
    ("DATA", "Change in provision for residual value on HP & PCP vehicles", {"FY2024": 12209, "FY2023": 21368, "FY2022": -10579, "FY2021": -3305, "FY2020": -18291}),
    ("DATA", "Change in provision for expected credit losses on loans and advances to customers", {"FY2024": -1301, "FY2023": -9075, "FY2022": -11912, "FY2021": 15279, "FY2020": -23709}),
    ("DATA", "Change in provision for expected credit losses on investment securities", {"FY2024": 16, "FY2023": 57, "FY2022": -37, "FY2021": -65, "FY2020": 151}),
    ("DATA", "(Loss)/profit on derivatives - fair value adjustments", {"FY2024": -7561, "FY2023": -41989, "FY2022": 39713, "FY2021": 11969, "FY2020": -55}),
    ("DATA", "Profit on disposal of investment securities", {"FY2024": 6008, "FY2023": 4940, "FY2022": 2051}),
    ("DATA", "Income from equity method investments", {"FY2024": 509, "FY2023": -178}),
    ("TOTAL", "Profit before tax", {"FY2024": 37515, "FY2023": 63631, "FY2022": 131197, "FY2021": 127547, "FY2020": 71623}),
    ("DATA", "Tax expense", {"FY2024": -10922, "FY2023": -13844, "FY2022": -22458, "FY2021": -20414, "FY2020": -10086}),
    ("TOTAL", "Profit after tax for the financial year", {"FY2024": 26593, "FY2023": 49787, "FY2022": 108739, "FY2021": 107133, "FY2020": 61537}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income/(loss), net of tax", {"FY2024": 737, "FY2023": -740, "FY2022": 3924, "FY2021": 4429, "FY2020": -1953}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2024": 27330, "FY2023": 49047, "FY2022": 112663, "FY2021": 111562, "FY2020": 59584}),
]

bw.add_income_statement_sheet(
    title="RCI Bank UK Limited - Group Profit & Loss",
    subtitle="Consolidated Statement of Profit or Loss (and Other Comprehensive Income), Group column, £'000; FY2020-FY2024. See source note.",
    rows=PL_ROWS, sources_text=PL_SOURCES, first_col_width=68, source_height=210, unit_suffix=" (£'000)",
)

EQUITY_SOURCES = (
    "Sources - RCI Bank UK Limited Group consolidated statement of changes in equity, £'000 (Group column):\n"
    f"FY2024 & FY2023: Annual Report and Financial Statements for year ended 31 December 2024, printed p.45 "
    f"(PDF p.44), Company and Consolidated Statement of Changes in Equity - {AR24_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements for year ended 31 December 2022, printed p.35 "
    f"(PDF p.34), Company and Consolidated Statement of Changes in Equity - {AR22_URL}\n"
    f"FY2020 (and its 1 January 2020 opening balance): Annual Report and Financial Statements for year ended 31 "
    f"December 2020, printed p.32 (PDF p.31), Company and Consolidated Statement of Equity - {AR20_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    "Every closing balance below ties both to the next year's opening balance and to that year's own Group "
    "Balance Sheet Total equity - zero undocumented plug rows across all 5 years. Non-controlling interests "
    "first appear in FY2023 following the incorporation of 85%-owned Mobilize Lease & Co UK Limited in May 2023; "
    "the merger reserve that exists at Company level is eliminated on consolidation and never appears in the "
    "Group columns above, so it is omitted from this sheet."
)

EQUITY_HEADERS = ["Ordinary share capital", "Other reserves", "Retained earnings", "Non-controlling interests", "Total"]

EQUITY_ROWS = [
    ("TOTAL", "Balance at 1 January 2020", (290400, -9981, 328034, None, 608453)),
    ("DATA", "Profit for the year", (None, None, 61537, None, 61537)),
    ("DATA", "Other comprehensive income/(loss)", (None, -1953, None, None, -1953)),
    ("TOTAL", "Total comprehensive income for the year", (None, -1953, 61537, None, 59584)),
    ("DATA", "Dividend paid", (None, None, -51400, None, -51400)),
    ("TOTAL", "Balance at 31 December 2020 and 1 January 2021", (290400, -11934, 338171, None, 616637)),
    ("DATA", "Profit for the year", (None, None, 107133, None, 107133)),
    ("DATA", "Other comprehensive income", (None, 4429, None, None, 4429)),
    ("TOTAL", "Total comprehensive income for the year", (None, 4429, 107133, None, 111562)),
    ("DATA", "Dividend paid", (None, None, -86862, None, -86862)),
    ("TOTAL", "Balance at 31 December 2021 and 1 January 2022", (290400, -7505, 358442, None, 641337)),
    ("DATA", "Profit for the year", (None, None, 108739, None, 108739)),
    ("DATA", "Other comprehensive income", (None, 3924, None, None, 3924)),
    ("TOTAL", "Total comprehensive income for the year", (None, 3924, 108739, None, 112663)),
    ("DATA", "Dividend paid", (None, None, -107133, None, -107133)),
    ("TOTAL", "Balance at 31 December 2022 and 1 January 2023", (290400, -3581, 360048, None, 646867)),
    ("DATA", "Profit for the year", (None, None, 49887, None, 49887)),
    ("DATA", "Other comprehensive income/(loss)", (None, -740, None, None, -740)),
    ("TOTAL", "Total comprehensive income for the year", (None, -740, 49887, None, 49147)),
    ("DATA", "Acquisition of subsidiary (Mobilize Lease & Co UK - NCI share)", (None, None, None, 225, 225)),
    ("DATA", "Loss attributable to minority interest", (None, None, None, -100, -100)),
    ("TOTAL", "Balance at 31 December 2023 and 1 January 2024", (290400, -4321, 409935, 125, 696139)),
    ("DATA", "Profit/(loss) for the year", (None, None, 27055, -462, 26593)),
    ("DATA", "Other comprehensive income", (None, 737, None, None, 737)),
    ("TOTAL", "Total comprehensive income for the year", (None, 737, 27055, -462, 27330)),
    ("TOTAL", "Balance at 31 December 2024", (290400, -3584, 436990, -337, 723469)),
]

bw.add_equity_changes_sheet(
    title="RCI Bank UK Limited - Group Statement of Changes in Equity",
    subtitle="Group column, £'000; chronological, 1 January 2020 - 31 December 2024. See source note.",
    headers=EQUITY_HEADERS, rows=EQUITY_ROWS, sources_text=EQUITY_SOURCES, first_col_width=52, source_height=200,
)

bw.add_cash_flow_sheet(
    title="RCI Bank UK Limited - Group Cash Flow Statement",
    subtitle="Group/consolidated basis, £'000; five latest available financial years FY2020-FY2024. See source note.",
    rows=rows, sources_text=CASH_SOURCES, first_col_width=68, source_height=210, unit_suffix=" (£'000)",
)

AQ_SOURCES = (
    "Sources - RCI Bank UK Limited Group loans and advances to customers, £'000 (Group column, note 'Loans and "
    "advances to customers'):\n"
    f"FY2024 & FY2023 comparative: Annual Report and Financial Statements for year ended 31 December 2024, "
    f"printed pp.74-79 (PDF pp.73-78) - {AR24_URL}\n"
    f"FY2022 & FY2021 comparative: Annual Report and Financial Statements for year ended 31 December 2022, "
    f"printed pp.61-66 (PDF pp.60-65) - {AR22_URL}\n"
    f"FY2020: Annual Report and Financial Statements for year ended 31 December 2020, printed pp.55-57 (PDF "
    f"pp.54-56) - {AR20_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: A separate 'Finance Lease' product line existed alongside HP & PCP and Wholesale through "
    "FY2021; during 2022 the Group reclassified c.£15m of Finance Lease receivables from Loans and advances to "
    "customers into Property, Plant and Equipment (shown as Lease Hire assets), so FY2022 onward carries only "
    "HP & PCP and Wholesale. Gross carrying amount by IFRS 9 stage (rather than by product) is only disclosed at "
    "this granularity for HP & PCP contracts in the FY2022 and FY2021 filings; the ECL loss allowance by stage "
    "is disclosed for all 5 years and is used below for the coverage/Stage 3 metrics, applied to the whole book."
)

AQ_ROWS = [
    ("SECTION", "Gross loans and advances to customers, by product", {}),
    ("DATA", "HP & PCP", {"FY2024": 4166131, "FY2023": 4007471, "FY2022": 3513916, "FY2021": 3079780, "FY2020": 2910212}),
    ("DATA", "Finance Lease", {"FY2021": 15291, "FY2020": 11799}),
    ("DATA", "Wholesale", {"FY2024": 1102294, "FY2023": 1033829, "FY2022": 911100, "FY2021": 437250, "FY2020": 700687}),
    ("TOTAL", "Gross loans and advances to customers", {"FY2024": 5268425, "FY2023": 5041300, "FY2022": 4425016, "FY2021": 3532321, "FY2020": 3622698}),
    ("SECTION", "Expected credit loss (ECL) allowance, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2024": -11318, "FY2023": -15813, "FY2022": -19177, "FY2021": -10376, "FY2020": -19264}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2024": -4547, "FY2023": -7921, "FY2022": -4898, "FY2021": -3893, "FY2020": -14889}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2024": -19576, "FY2023": -17738, "FY2022": -14827, "FY2021": -18121, "FY2020": -19310}),
    ("TOTAL", "Total ECL allowance", {"FY2024": -35441, "FY2023": -41472, "FY2022": -38902, "FY2021": -32390, "FY2020": -53463}),
    ("DATA", "Residual value provision for HP & PCP", {"FY2024": -62306, "FY2023": -74516, "FY2022": -95883, "FY2021": -85304, "FY2020": -81999}),
    ("TOTAL", "Net loans and advances to customers", {"FY2024": 5170678, "FY2023": 4925312, "FY2022": 4290231, "FY2021": 3414627, "FY2020": 3487236}),
    ("SECTION", "Derived asset-quality ratios", {}),
    ("DATA", "ECL coverage ratio (Total ECL allowance / Gross loans)", {"FY2024": "0.67%", "FY2023": "0.82%", "FY2022": "0.88%", "FY2021": "0.92%", "FY2020": "1.48%"}),
    ("DATA", "Stage 3 ECL allowance as % of total ECL allowance", {"FY2024": "55.2%", "FY2023": "42.8%", "FY2022": "38.1%", "FY2021": "55.9%", "FY2020": "36.1%"}),
]

bw.add_asset_quality_sheet(
    title="RCI Bank UK Limited - Group Asset Quality",
    subtitle="Loans and advances to customers, Group column, £'000; FY2020-FY2024. See source note.",
    rows=AQ_ROWS, sources_text=AQ_SOURCES, first_col_width=68, source_height=210, unit_suffix=" (£'000)",
)

P3_SOURCES = (
    f"FY2024 and FY2023: RCI Bank UK / Mobilize Financial Services UK Pillar 3 Disclosures, UK KM1 table, "
    f"printed p.24 (FY2024 report) and p.22 (FY2023 report) - {P3_24_URL} - {P3_23_URL}\n"
    f"FY2022-FY2020: RCI Bank UK Annual Reports, Directors' Strategic Report, Capital and Liquidity section - "
    f"{AR22_URL} - {AR21_URL} - {AR20_URL}\n"
    f"RCI Bank UK official facts and figures page (publication links and identity) - {FACTS_URL}"
)

def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, P3_SOURCES, note=note, first_col_width=52, source_height=170)

metric("CET1 Capital", "£'000, UK KM1 / Group basis", [("Common Equity Tier 1 (CET1) capital", {"FY2024": 707000, "FY2023": 669000})], "Absolute CET1 capital is disclosed in the UK KM1 table only for FY2024-FY2023; the earlier annual reports disclose ratios but not the absolute capital amount.")
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {"FY2024": "13.69%", "FY2023": "13.81%", "FY2022": "13.98%", "FY2021": "15.16%", "FY2020": "15.94%"})])
metric("Tier 1 Capital", "£'000, UK KM1 / Group basis", [("Tier 1 capital", {"FY2024": 707000, "FY2023": 669000})], "Absolute Tier 1 capital is disclosed in the UK KM1 table only for FY2024-FY2023; earlier annual reports do not disclose the amount.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2024": "13.46%", "FY2023": "13.81%", "FY2022": "13.98%", "FY2021": "15.16%", "FY2020": "15.94%"})], "FY2024 is from the dedicated UK KM1 disclosure. The FY2024 annual-report narrative gives CET1 13.69% and total capital 15.66%, which are a different reporting basis/rounding vintage; the dedicated KM1 value is retained for this metric.")
metric("Total Capital", "£'000, UK KM1 / Group basis", [("Total capital", {"FY2024": 809000, "FY2023": 774000})], "Absolute total capital is disclosed in the UK KM1 table only for FY2024-FY2023; earlier annual reports do not disclose the amount.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2024": "15.42%", "FY2023": "15.99%", "FY2022": "16.34%", "FY2021": "16.31%", "FY2020": "17.16%"})])
metric("Total RWAs", "£'000, UK KM1 / Group basis", [("Total risk-weighted exposure amount", {"FY2024": 5247000, "FY2023": 4842000})], "Absolute RWA is disclosed in the UK KM1 table only for FY2024-FY2023; earlier annual reports disclose capital ratios but not RWA amounts.")

RWA_SOURCES = (
    f"FY2024 & FY2023: RCI Bank UK / Mobilize Financial Services UK Pillar 3 Disclosures FY2024, Table 1 (UK "
    f"OV1 - Overview of risk weighted exposure amounts), printed p.23 - {P3_24_URL}\n"
    f"FY2022: RCI Bank UK / Mobilize Financial Services UK Pillar 3 Disclosures FY2023, Table 1 (UK OV1), "
    f"printed p.21, FY2022 comparative column - {P3_23_URL}\n\n"
    "PRESENTATION NOTE: RCI Bank UK's Pillar 3 disclosures were not made available as standalone documents "
    "before FY2023 (no dedicated document was located on the bank's site or via the Wayback Machine this "
    "session, despite retrying); the FY2021 and FY2020 annual reports disclose capital ratios in their "
    "Strategic Report but not a category-level RWA breakdown. This is a genuine access/non-existence gap, not "
    "an oversight - flagged for follow-up rather than estimated. All disclosed years tie exactly to the Total "
    "RWAs metric sheet."
)

bw.add_rwa_breakdown_sheet(
    title="RCI Bank UK Limited - RWA Breakdown",
    subtitle="Risk-weighted exposure amounts by category (UK OV1 template), Group basis, £'000. See source note.",
    rows=[
        ("SECTION", "Risk-weighted exposure amounts by category", {}),
        ("DATA", "Credit risk (excluding CCR)", {"FY2024": 4946000, "FY2023": 4543000, "FY2022": 3978000}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2024": 11000, "FY2023": 10000, "FY2022": 9000}),
        ("DATA", "Operational risk", {"FY2024": 288000, "FY2023": 280000, "FY2022": 259000}),
        ("TOTAL", "Total risk-weighted exposure amount", {"FY2024": 5247000, "FY2023": 4842000, "FY2022": 4246000}),
    ],
    sources_text=RWA_SOURCES, first_col_width=54, source_height=190, unit_suffix=" (£'000)",
)

metric("Leverage Ratio", "£'000 / %", [("Total exposure measure excluding claims on central banks", {"FY2024": 6642000, "FY2023": 6148000}), ("Leverage ratio excluding claims on central banks (%)", {"FY2024": "10.6%", "FY2023": "10.9%"})], "No leverage ratio was located in the FY2022-FY2020 annual-report narrative; the dedicated UK KM1 disclosure supplies FY2024-FY2023.")
metric("LCR", "£'000 / %", [("Total high-quality liquid assets (HQLA), weighted value - average", {"FY2024": 899000, "FY2023": 1035000}), ("Total net cash outflows (adjusted value)", {"FY2024": 365000, "FY2023": 467000}), ("Liquidity Coverage Ratio (%)", {"FY2024": "287%", "FY2023": "236%", "FY2022": "354%", "FY2021": "158%", "FY2020": "551%"})], "FY2024-FY2023 amounts and ratios are UK KM1. The FY2022-FY2020 headline ratios are from the statutory annual-report Capital and Liquidity sections.")
metric("NSFR", "£'000 / %", [("Total available stable funding", {"FY2024": 6115000, "FY2023": 5622000}), ("Total required stable funding", {"FY2024": 4863000, "FY2023": 4312000}), ("NSFR ratio (%)", {"FY2024": "126%", "FY2023": "130%", "FY2022": "138%", "FY2021": "109%", "FY2020": "138%"})], "FY2024-FY2023 amounts and ratios are UK KM1. The FY2022-FY2020 headline ratios are from the statutory annual-report Capital and Liquidity sections.")
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No quantitative MREL ratio was found in the RCI Bank UK annual reports, the RCI Bank UK Pillar 3 disclosures reviewed, or the official facts-and-figures page.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2024": 7299251, "FY2023": 6932488, "FY2022": 6297529, "FY2021": 4995682, "FY2020": 4922345}),
        ("Loans and advances to customers", {"FY2024": 5170678, "FY2023": 4925312, "FY2022": 4290231, "FY2021": 3414627, "FY2020": 3487236}),
        ("Deposits from customers", {"FY2024": 4978566, "FY2023": 4794623, "FY2022": 4140482, "FY2021": 2929460, "FY2020": 3149310}),
        ("Total equity", {"FY2024": 723469, "FY2023": 696139, "FY2022": 646867, "FY2021": 641337, "FY2020": 616637}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {"FY2024": 391562, "FY2023": 300157, "FY2022": 254927, "FY2021": 267807, "FY2020": 164186}),
        ("Total operating expense (cost of sales + operating costs)", {"FY2024": -290283, "FY2023": -211649, "FY2022": -142966, "FY2021": -164138, "FY2020": -83407}),
        ("Profit after tax for the financial year", {"FY2024": 26593, "FY2023": 49787, "FY2022": 108739, "FY2021": 107133, "FY2020": 61537}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Total comprehensive income for the year", {"FY2024": 27330, "FY2023": 49047, "FY2022": 112663, "FY2021": 111562, "FY2020": 59584}),
        ("Dividend paid", {"FY2022": -107133, "FY2021": -86862, "FY2020": -51400}),
        ("Total equity (closing)", {"FY2024": 723469, "FY2023": 696139, "FY2022": 646867, "FY2021": 641337, "FY2020": 616637}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2024": 160113, "FY2023": 38755, "FY2022": 472150, "FY2021": 689232, "FY2020": 642905}),
        ("Net cash generated from/(used in) investing activities", {"FY2024": -347349, "FY2023": -290446, "FY2022": -898, "FY2021": -552065, "FY2020": 476440}),
        ("Net cash (used in)/generated from financing activities", {"FY2024": 98614, "FY2023": 99107, "FY2022": -8029, "FY2021": -487797, "FY2020": -151400}),
        ("Cash and cash at central banks at 31 December", {"FY2024": 959888, "FY2023": 1048510, "FY2022": 1201094, "FY2021": 737871, "FY2020": 1088501}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2024": "13.69%", "FY2023": "13.81%", "FY2022": "13.98%", "FY2021": "15.16%", "FY2020": "15.94%"}),
        ("Total Capital Ratio", {"FY2024": "15.42%", "FY2023": "15.99%", "FY2022": "16.34%", "FY2021": "16.31%", "FY2020": "17.16%"}),
        ("LCR", {"FY2024": "287%", "FY2023": "236%", "FY2022": "354%", "FY2021": "158%", "FY2020": "551%"}),
        ("NSFR", {"FY2024": "126%", "FY2023": "130%", "FY2022": "138%", "FY2021": "109%", "FY2020": "138%"}),
    ],
    note="Cash flows are RCI Bank UK Group consolidated figures. Dedicated UK KM1 Pillar 3 amounts are available for FY2024-FY2023; earlier years use explicitly disclosed annual-report ratios. Blank cells mean not disclosed, not zero.",
)

bw.save("/Users/armaan/code/katalysis/banks/RCI BANK UK FINANCIALS.xlsx")
