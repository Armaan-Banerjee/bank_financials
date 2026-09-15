import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]

AR24_URL = "https://find-and-update.company-information.service.gov.uk/company/11429127/filing-history/MzQ4MzYzODUzNmFkaXF6a2N4/document?download=0&format=pdf"
AR23_URL = "https://find-and-update.company-information.service.gov.uk/company/11429127/filing-history/MzQyNTg5Mjk5OWFkaXF6a2N4/document?download=0&format=pdf"
AR22_URL = "https://find-and-update.company-information.service.gov.uk/company/11429127/filing-history/MzM4MDE0Nzg1OGFkaXF6a2N4/document?download=0&format=pdf"
AR21_URL = "https://find-and-update.company-information.service.gov.uk/company/11429127/filing-history/MzM0MjczNjEyNGFkaXF6a2N4/document?download=0&format=pdf"
AR20_URL = "https://find-and-update.company-information.service.gov.uk/company/11429127/filing-history/MzMwNzExODk0NmFkaXF6a2N4/document?download=0&format=pdf"
AR19_URL = "https://find-and-update.company-information.service.gov.uk/company/11429127/filing-history/MzI3OTM5NTc3NGFkaXF6a2N4/document?download=0&format=pdf"
DORMANT18_URL = "https://find-and-update.company-information.service.gov.uk/company/11429127/filing-history/MzIzMjgzMTgxMmFkaXF6a2N4/document?download=0&format=pdf"
P3_24_URL = "https://www.rcibank.co.uk/sites/default/files/2025-12/Pillar%20III%20Disclosures%20FY%202024%20-%20External.pdf"
P3_23_URL = "https://www.rcibank.co.uk/sites/default/files/2024-11/Pillar%20III%20Disclosures%20FY%202023%20-%20final%20%28external%20version%29%20signed%201_0.pdf"
FACTS_URL = "https://www.rcibank.co.uk/about-us/facts-and-figures"

ENTITY_NOTE = (
    "ENTITY NOTE: RCI Bank UK Limited (company 11429127; FRN 815220) is the PRA/FCA-authorised bank. "
    "The cash-flow statement uses the Group column of RCI Bank UK Limited's statutory accounts: RCI Bank UK, "
    "100%-owned RCI Financial Services Limited, 85%-owned Mobilize Lease & Co UK Limited and controlled "
    "securitisation SPVs. The accounts also print a Company column, but the Group column is used consistently "
    "because the bank's lending and lease operations sit in its subsidiaries. FY2024 is the latest available "
    "statutory filing; FY2025 accounts were not yet filed at the time of build. All six reports are scanned PDFs "
    "and were OCR-processed; values were cross-checked against the printed totals and later comparative columns.\n\n"
    "FY2018 SELF-SKIP: RCI Bank UK Limited was incorporated on 22 June 2018 and remained dormant for the whole "
    "of that period - its FY2018 statutory filing is a 2-page 'Accounts for a dormant company' under s.480 "
    "Companies Act 2006, showing net assets of GBP1 (called-up share capital not paid) and no profit-and-loss, "
    "balance-sheet, cash-flow or capital/liquidity disclosure of any kind - "
    f"{DORMANT18_URL}. This is a genuine absence of a trading year, re-verified from the actual filing rather "
    "than assumed from an earlier scan, so FY2018 is excluded from YEARS rather than shown blank.\n\n"
    "FY2019 PERIOD NOTE: RCI Bank UK Limited only became the Group parent on 6 March 2019, when it acquired "
    "100%-owned RCI Financial Services Limited (and, through it, securitisation SPV Cars Alliance 2015 Limited) "
    "from parent RCI Banque SA in a common-control transaction, and on 14 March 2019 also took on the UK branch "
    "of RCI Banque SA's savings/deposit-taking business. The FY2019 Group results therefore cover a 10-month "
    "period (6 March-31 December 2019), not a full 12 months, and the FY2018 Group comparative column in the "
    "FY2019 statutory accounts is a genuine nil (dormant Company, no Group existed) - both are the bank's own "
    "as-reported basis, not a workbook estimate. The FY2019 statutory accounts state the FY2018 comparative "
    "figures were unaudited (prior period was dormant-company accounts, not subject to audit)."
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
    f"(PDF pp.32-33) - {AR20_URL}\n"
    f"FY2019 (10-month Group period, 6 March-31 December 2019): Annual Report and Financial Statements for year "
    f"ended 31 December 2019, printed p.33 (PDF p.33, no cover-page offset in this filing), Cash Flow Statements, "
    f"Group column - {AR19_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "DATA QUALITY NOTE: The OCR of the FY2022 report rendered the Group FY2022 proceeds from investment "
    "securities as £4,024,803. The FY2023 report's clean comparative column prints £1,024,803, which agrees "
    "with the reported FY2022 investing subtotal of (£898) and the cash movement. The corrected £1,024,803 is "
    "used here; this is a source/OCR correction, not an estimate.\n\n"
    "FY2019 PRESENTATION NOTE: The FY2019 cash flow statement uses some line labels not seen in later years - "
    "'Gain on sale of property, plant and equipment', 'Residual value provisions for HP & PCP' (an operating add-"
    "back, not the later years' balance-sheet contra-asset treatment - see the Balance Sheet source note), and a "
    "one-off 'Cash on transfer of Branch/acquisition of Subsidiary' bridging line (GBP154,682k) between the nil "
    "opening cash balance (dormant Company at 1 January 2019) and the GBP120,556k closing balance. All FY2019 "
    "subtotals below tie exactly to the as-reported figures with no plug required."
)

bw = BankWorkbook(bank_name="RCI Bank UK Limited", years=YEARS, header_color="174A5B")

rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2024": 37515, "FY2023": 63631, "FY2022": 131197, "FY2021": 127547, "FY2020": 71623, "FY2019": 75988}),
    ("DATA", "Depreciation and amortisation", {"FY2024": 104189, "FY2023": 92713, "FY2022": 52443, "FY2021": 35811, "FY2020": 28245, "FY2019": 23686}),
    ("DATA", "Net book value of property, plant and equipment disposed", {"FY2021": 36583, "FY2020": 45774}),
    ("DATA", "Gain on sale of property, plant and equipment", {"FY2019": -251}),
    ("DATA", "Impairment of financial assets", {"FY2024": 57, "FY2023": 57, "FY2022": 37, "FY2021": 65, "FY2020": -151, "FY2019": -2115}),
    ("DATA", "Loss/(gain) on fair value adjustment - derivatives", {"FY2023": 30339, "FY2021": -11969, "FY2020": 55, "FY2019": 3353}),
    ("DATA", "Derivative financial instruments", {"FY2024": 18732, "FY2022": -47914, "FY2020": 228, "FY2019": 3841}),
    ("DATA", "Interest income", {"FY2022": 2018, "FY2021": -23, "FY2020": -1458}),
    ("DATA", "Interest expenses", {"FY2023": 7864, "FY2022": -2051, "FY2021": 1732, "FY2020": 1737, "FY2019": 1438}),
    ("DATA", "Profit on disposal of investment securities", {"FY2024": -6008, "FY2023": -4940}),
    ("DATA", "Provision for liabilities", {"FY2024": 73644}),
    ("DATA", "Other non-cash or non-operating items", {"FY2024": -462, "FY2023": 100}),
    ("DATA", "Loans and advances to customers", {"FY2024": -245366, "FY2023": -635081, "FY2022": -890629, "FY2021": 72609, "FY2020": 412363, "FY2019": 134813}),
    ("DATA", "NBV of vehicles transferred to inventory", {"FY2024": 125434, "FY2023": 83828, "FY2022": 74920}),
    ("DATA", "Inventory", {"FY2024": -28631, "FY2023": -8468, "FY2022": -6497, "FY2021": 12434, "FY2020": 14535, "FY2019": -19210}),
    ("DATA", "Other assets", {"FY2024": -70864, "FY2023": -30614, "FY2022": -18531, "FY2021": -18531, "FY2020": -20422, "FY2019": -79904}),
    ("DATA", "Other liabilities", {"FY2024": 2516, "FY2023": 5379, "FY2022": 73787, "FY2021": -25651, "FY2020": -4527, "FY2019": 69191}),
    ("DATA", "Residual value provisions for HP & PCP", {"FY2019": -1457}),
    ("DATA", "Pension contributions paid and amounts recognised in income statement", {"FY2024": -2468, "FY2023": -2366, "FY2022": -128, "FY2021": -104, "FY2020": -103, "FY2019": -47}),
    ("DATA", "Customer deposits", {"FY2024": 183943, "FY2023": 654141, "FY2022": 1211022, "FY2021": -219850, "FY2020": 195717, "FY2019": 110055}),
    ("DATA", "Bank deposits", {"FY2024": -440, "FY2023": -200051, "FY2022": -89121, "FY2021": 704439, "FY2020": -37451, "FY2019": 187533}),
    ("DATA", "Loan to subsidiary", {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Other operating items included in reported subtotal", {"FY2024": 227, "FY2021": -2594, "FY2020": -47952}),
    ("TOTAL", "Cash generated by operations", {"FY2024": 192018, "FY2023": 56532, "FY2022": 490553, "FY2021": 712498, "FY2020": 658213, "FY2019": 506914}),
    ("DATA", "Income taxes paid", {"FY2024": -31905, "FY2023": -17777, "FY2022": -18403, "FY2021": -23266, "FY2020": -15308, "FY2019": -5000}),
    ("TOTAL", "Net cash from operating activities", {"FY2024": 160113, "FY2023": 38755, "FY2022": 472150, "FY2021": 689232, "FY2020": 642905, "FY2019": 501914}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2024": -334148, "FY2023": -331888, "FY2022": -265940, "FY2021": -132014, "FY2020": -122580, "FY2019": -64655}),
    ("DATA", "Intangible asset", {"FY2024": -980, "FY2023": -1000}),
    ("DATA", "Purchasing of investment securities", {"FY2024": -244257, "FY2023": -231803, "FY2022": -761812, "FY2021": -430074, "FY2020": -1437759, "FY2019": -2085873}),
    ("DATA", "Proceeds from investment securities", {"FY2024": 232036, "FY2023": 290000, "FY2022": 1024803, "FY2021": 10000, "FY2020": 1988828, "FY2019": 1539635}),
    ("DATA", "Profit on disposal of investment securities", {"FY2022": 2051}),
    ("DATA", "Investment in associate", {"FY2023": -15980}),
    ("DATA", "Non-controlling interest subscription", {"FY2023": 225}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2021": 0, "FY2020": 49409, "FY2019": 54227}),
    ("DATA", "Interest income", {"FY2021": 23, "FY2020": -1458, "FY2019": -3374}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2024": -347349, "FY2023": -290446, "FY2022": -898, "FY2021": -552065, "FY2020": 476440, "FY2019": -560040}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Proceeds from subordinated debt", {"FY2020": 40000, "FY2019": 40000}),
    ("DATA", "Debt securities issued/(redeemed)", {"FY2024": 100000, "FY2023": 100000, "FY2021": -400000, "FY2020": -200000, "FY2019": -200000}),
    ("DATA", "Issuing of ordinary share capital", {"FY2019": 184000}),
    ("DATA", "Dividends paid", {"FY2021": -86862, "FY2020": -51400}),
    ("DATA", "Property lease rent paid", {"FY2024": -1188, "FY2023": -672, "FY2022": -654, "FY2021": -935}),
    ("DATA", "Interest on property lease", {"FY2024": -198, "FY2023": -221, "FY2022": -242}),
    ("DATA", "Other financing items included in reported subtotal", {"FY2022": -7133, "FY2020": 60000}),
    ("TOTAL", "Net cash (used in)/generated from financing activities", {"FY2024": 98614, "FY2023": 99107, "FY2022": -8029, "FY2021": -487797, "FY2020": -151400, "FY2019": 24000}),
    ("TOTAL", "Net increase/(decrease) in cash and cash at central banks", {"FY2024": -88622, "FY2023": -152584, "FY2022": 463223, "FY2021": -350630, "FY2020": 967945, "FY2019": -34126}),
    ("DATA", "Cash and cash at central banks at 1 January", {"FY2024": 1048510, "FY2023": 1201094, "FY2022": 737871, "FY2021": 1088501, "FY2020": 120556, "FY2019": 0}),
    ("DATA", "Cash on transfer of Branch/acquisition of Subsidiary", {"FY2019": 154682}),
    ("TOTAL", "Cash and cash at central banks at 31 December", {"FY2024": 959888, "FY2023": 1048510, "FY2022": 1201094, "FY2021": 737871, "FY2020": 1088501, "FY2019": 120556}),
]

BS_SOURCES = (
    "Sources - RCI Bank UK Limited Group consolidated balance sheet, £'000 (Group column):\n"
    f"FY2024 & FY2023 comparative: Annual Report and Financial Statements for year ended 31 December 2024, "
    f"printed p.43 (PDF p.42), Company and Consolidated Balance Sheet - {AR24_URL}\n"
    f"FY2022 & FY2021 comparative: Annual Report and Financial Statements for year ended 31 December 2022, "
    f"printed p.34 (PDF p.33), Company and Consolidated Balance Sheet - {AR22_URL}\n"
    f"FY2020: Annual Report and Financial Statements for year ended 31 December 2020, printed p.31 (PDF p.30), "
    f"Company and Consolidated Balance Sheet - {AR20_URL}\n"
    f"FY2019: Annual Report and Financial Statements for year ended 31 December 2019, printed p.31 (PDF p.31, no "
    f"cover-page offset in this filing), Consolidated and Company Balance Sheets, Group column - {AR19_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    "INVESTMENT SECURITIES NOTE: the Group's Investment securities balance is 100% UK Treasury Bills held at "
    "fair value through OCI (no amortised-cost leg at Group level - that leg in Note 15b/14b is Company-only, "
    "relating to Notes issued through Cars Alliance Master UK plc) in every disclosed year - Note 15/15a "
    "'Investment securities'/'Financial assets at FVOCI' (FY2024 Annual Report, PDF p.83), Note 14/'Investment "
    f"Securities held by the Company...include GBP157.9m of Treasury Bills' (FY2022 Annual Report - {AR22_URL}), "
    "and Note 'Investment Securities - UK Treasury bills'/'Financial Assets at FVOCI' (FY2020 Annual Report, "
    f"printed p.15 of the notes - {AR20_URL}).\n\n"
    "PRESENTATION NOTE: Deferred tax asset, Investment in associate and Intangible assets are only disclosed as "
    "separate Group balance sheet lines from FY2023 (associate) / FY2025-vintage FY2024 report (intangibles) "
    "onward; earlier years genuinely did not carry these balances as separate lines and are left blank, not "
    "zero. FY2020's Group Investment securities line is a genuine nil ('-' in the source) while FY2019's "
    "comparative was £548,818k - this is a real year-on-year balance sheet movement, not a data gap.\n\n"
    "FY2019 PRESENTATION NOTE: The FY2019 Group balance sheet carries a separate 'Residual value provisions for "
    "HP & PCP' liability line (GBP63,707k) that is deducted directly from the loan asset in FY2020 onward instead "
    "(see the Asset Quality sheet) - both are the bank's own as-reported basis for that year, not a workbook "
    "reclassification. The FY2019 Group 'Loans and advances to customers' asset of GBP3,916,076k is therefore "
    "gross loans less ECL allowance only (no RV deduction), reconciling exactly to Note 13 of the FY2019 accounts."
)

BS_ROWS = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash at central banks", {"FY2024": 959888, "FY2023": 1048510, "FY2022": 1201094, "FY2021": 737871, "FY2020": 1088501, "FY2019": 120556}),
    ("DATA", "Derivative financial instruments", {"FY2024": 11829, "FY2023": 37622, "FY2022": 55475, "FY2021": 10254, "FY2020": 1388, "FY2019": 35}),
    ("DATA", "Investment securities - UK Treasury Bills at FVOCI", {"FY2024": 123749, "FY2023": 105575, "FY2022": 157926, "FY2021": 419939, "FY2020": 0, "FY2019": 548818}),
    ("DATA", "Inventory", {"FY2024": 46891, "FY2023": 18260, "FY2022": 9792, "FY2021": 3295, "FY2020": 15729, "FY2019": 30264}),
    ("DATA", "Loans and advances to customers", {"FY2024": 5170678, "FY2023": 4925312, "FY2022": 4290231, "FY2021": 3414627, "FY2020": 3487236, "FY2019": 3916076}),
    ("DATA", "Property, plant and equipment", {"FY2024": 679541, "FY2023": 575015, "FY2022": 419670, "FY2021": 266068, "FY2020": 206448, "FY2019": 157891}),
    ("DATA", "Current tax asset", {"FY2022": 0, "FY2021": 1273}),
    ("DATA", "Deferred tax asset", {"FY2024": 31036, "FY2023": 18541, "FY2022": 7203, "FY2021": 4748, "FY2020": 3967, "FY2019": 2621}),
    ("DATA", "Other assets", {"FY2024": 257616, "FY2023": 186752, "FY2022": 156138, "FY2021": 137607, "FY2020": 119076, "FY2019": 237961}),
    ("DATA", "Investment in associate", {"FY2024": 16311, "FY2023": 15901}),
    ("DATA", "Intangible assets", {"FY2024": 1712, "FY2023": 1000}),
    ("TOTAL", "Total assets", {"FY2024": 7299251, "FY2023": 6932488, "FY2022": 6297529, "FY2021": 4995682, "FY2020": 4922345, "FY2019": 5014222}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from customers", {"FY2024": 4978566, "FY2023": 4794623, "FY2022": 4140482, "FY2021": 2929460, "FY2020": 3149310, "FY2019": 2953593}),
    ("DATA", "Deposits from banks", {"FY2024": 564909, "FY2023": 565349, "FY2022": 765400, "FY2021": 854521, "FY2020": 150082, "FY2019": 187533}),
    ("DATA", "Derivative financial instruments", {"FY2024": 5900, "FY2023": 12961, "FY2022": 475, "FY2021": 3168, "FY2020": 8865, "FY2019": 7229}),
    ("DATA", "Debt securities issued", {"FY2024": 700000, "FY2023": 600000, "FY2022": 500000, "FY2021": 400000, "FY2020": 800000, "FY2019": 900000}),
    ("DATA", "Current tax liabilities", {"FY2024": 5723, "FY2023": 13994, "FY2022": 6544, "FY2020": 452, "FY2019": 5076}),
    ("DATA", "Residual value provisions for HP & PCP", {"FY2019": 63707}),
    ("DATA", "Other liabilities", {"FY2024": 246255, "FY2023": 245125, "FY2022": 232934, "FY2021": 158024, "FY2020": 182878, "FY2019": 277745}),
    ("DATA", "Provision for liabilities", {"FY2024": 73644}),
    ("DATA", "Retirement benefit liability", {"FY2024": 785, "FY2023": 4297, "FY2022": 4827, "FY2021": 9172, "FY2020": 14121, "FY2019": 10886}),
    ("TOTAL", "Total liabilities", {"FY2024": 6575782, "FY2023": 6236349, "FY2022": 5650662, "FY2021": 4354345, "FY2020": 4305708, "FY2019": 4405769}),
    ("SECTION", "Equity", {}),
    ("DATA", "Issued/ordinary share capital", {"FY2024": 290400, "FY2023": 290400, "FY2022": 290400, "FY2021": 290400, "FY2020": 290400, "FY2019": 290400}),
    ("DATA", "Retained earnings", {"FY2024": 436990, "FY2023": 409935, "FY2022": 360048, "FY2021": 358442, "FY2020": 338171, "FY2019": 328034}),
    ("DATA", "Non-controlling interests", {"FY2024": -337, "FY2023": 125}),
    ("DATA", "Other reserves", {"FY2024": -3584, "FY2023": -4321, "FY2022": -3581, "FY2021": -7505, "FY2020": -11934, "FY2019": -9981}),
    ("TOTAL", "Total equity", {"FY2024": 723469, "FY2023": 696139, "FY2022": 646867, "FY2021": 641337, "FY2020": 616637, "FY2019": 608453}),
    ("TOTAL", "Total liabilities and equity", {"FY2024": 7299251, "FY2023": 6932488, "FY2022": 6297529, "FY2021": 4995682, "FY2020": 4922345, "FY2019": 5014222}),
]

bw.add_balance_sheet_sheet(
    title="RCI Bank UK Limited - Group Balance Sheet",
    subtitle="Company and Consolidated Statement of Financial Position, Group column, £'000; FY2019-FY2024 (FY2019 is a 10-month Group period - see source note). See source note.",
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
    f"FY2019 (10-month Group period, 6 March-31 December 2019): Annual Report and Financial Statements for year "
    f"ended 31 December 2019, printed p.29 (PDF p.29, no cover-page offset in this filing), Consolidated "
    f"Statement of Profit or Loss - {AR19_URL}\n"
    f"Other comprehensive income lines: the equivalent Consolidated Statement of Other Comprehensive Income in "
    f"each of the above reports (one page after the Statement of Profit or Loss).\n\n" + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: FY2020's income statement used an older structure ('Other profits/(losses) from the "
    "sale of Operating Lease vehicles' and 'from the sale of HP & PCP vehicles', no separate Cost of sales line "
    "or Revenue on sale of inventories line); FY2021 onward use 'Revenue on sale of inventories' and 'Cost of "
    "sales' instead. Both are the bank's own as-reported structure for that year, not a reclassification by "
    "this workbook. 'Profit after tax for the financial year' is the Group total (i.e. after minority interest), "
    "matching 'Profit for the year' on the Statement of Other Comprehensive Income and the Statement of Changes "
    "in Equity.\n\n"
    "FY2019 PRESENTATION NOTE: FY2019 is even more condensed than FY2020 - operating lease rentals and proceeds "
    "from car sales are combined into a single 'Other revenue' line (GBP87,716k, split GBP34,736k lease rentals / "
    "GBP52,980k sale proceeds per Note 4) rather than being shown separately; this combined figure is shown on "
    "its own row below rather than force-split across the later years' two rows. This is the bank's own "
    "as-reported FY2019 structure, not a workbook estimate."
)

PL_ROWS = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2024": 437390, "FY2023": 354682, "FY2022": 198217, "FY2021": 136838, "FY2020": 179280, "FY2019": 170847}),
    ("DATA", "Interest expense", {"FY2024": -313697, "FY2023": -243245, "FY2022": -95917, "FY2021": -43321, "FY2020": -64873, "FY2019": -60746}),
    ("TOTAL", "Net interest income", {"FY2024": 123693, "FY2023": 111437, "FY2022": 102300, "FY2021": 93517, "FY2020": 114407, "FY2019": 110101}),
    ("DATA", "Fee and commission income", {"FY2024": 12118, "FY2023": 12651, "FY2022": 9211, "FY2021": 9764, "FY2020": 7287, "FY2019": 6261}),
    ("DATA", "Fee and commission expense", {"FY2024": -931, "FY2023": -689, "FY2022": -119, "FY2021": -870, "FY2020": -535, "FY2019": -1558}),
    ("TOTAL", "Net fee and commission income", {"FY2024": 11187, "FY2023": 11962, "FY2022": 9092, "FY2021": 8894, "FY2020": 6752, "FY2019": 4703}),
    ("DATA", "Operating lease rentals", {"FY2024": 141203, "FY2023": 105791, "FY2022": 71833, "FY2021": 50490, "FY2020": 43027}),
    ("DATA", "Revenue on sale of inventories", {"FY2024": 115479, "FY2023": 70967, "FY2022": 71702, "FY2021": 114906}),
    ("DATA", "Other profits/(losses) from sale of Operating Lease vehicles", {"FY2020": 3987}),
    ("DATA", "Other profits/(losses) from sale of HP & PCP vehicles", {"FY2020": 28761, "FY2019": -2670}),
    ("DATA", "Other revenue (operating lease rentals and sale of assets, as reported)", {"FY2019": 87716}),
    ("TOTAL", "Total income", {"FY2024": 391562, "FY2023": 300157, "FY2022": 254927, "FY2021": 267807, "FY2020": 164186, "FY2019": 202520}),
    ("SECTION", "Costs and provisions", {}),
    ("DATA", "Cost of sales", {"FY2024": -115943, "FY2023": -59187, "FY2022": -47242, "FY2021": -83972}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2024": -104189, "FY2023": -92713, "FY2022": -52443, "FY2021": -35811, "FY2020": -28245, "FY2019": -23686}),
    ("DATA", "Operating expenses", {"FY2024": -70151, "FY2023": -59749, "FY2022": -43281, "FY2021": -44355, "FY2020": -55162, "FY2019": -100395}),
    ("DATA", "Change in provision for liabilities", {"FY2024": -73644}),
    ("DATA", "Change in provision for residual value on HP & PCP vehicles", {"FY2024": 12209, "FY2023": 21368, "FY2022": -10579, "FY2021": -3305, "FY2020": -18291, "FY2019": 1457}),
    ("DATA", "Change in provision for expected credit losses on loans and advances to customers", {"FY2024": -1301, "FY2023": -9075, "FY2022": -11912, "FY2021": 15279, "FY2020": -23709, "FY2019": 2266}),
    ("DATA", "Change in provision for expected credit losses on investment securities", {"FY2024": 16, "FY2023": 57, "FY2022": -37, "FY2021": -65, "FY2020": 151, "FY2019": -151}),
    ("DATA", "(Loss)/profit on derivatives - fair value adjustments", {"FY2024": -7561, "FY2023": -41989, "FY2022": 39713, "FY2021": 11969, "FY2020": -55, "FY2019": -3353}),
    ("DATA", "Profit on disposal of investment securities", {"FY2024": 6008, "FY2023": 4940, "FY2022": 2051}),
    ("DATA", "Income from equity method investments", {"FY2024": 509, "FY2023": -178}),
    ("TOTAL", "Profit before tax", {"FY2024": 37515, "FY2023": 63631, "FY2022": 131197, "FY2021": 127547, "FY2020": 71623, "FY2019": 75988}),
    ("DATA", "Tax expense", {"FY2024": -10922, "FY2023": -13844, "FY2022": -22458, "FY2021": -20414, "FY2020": -10086, "FY2019": -14421}),
    ("TOTAL", "Profit after tax for the financial year", {"FY2024": 26593, "FY2023": 49787, "FY2022": 108739, "FY2021": 107133, "FY2020": 61537, "FY2019": 61567}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income/(loss), net of tax", {"FY2024": 737, "FY2023": -740, "FY2022": 3924, "FY2021": 4429, "FY2020": -1953, "FY2019": -3893}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2024": 27330, "FY2023": 49047, "FY2022": 112663, "FY2021": 111562, "FY2020": 59584, "FY2019": 57674}),
]

bw.add_income_statement_sheet(
    title="RCI Bank UK Limited - Group Profit & Loss",
    subtitle="Consolidated Statement of Profit or Loss (and Other Comprehensive Income), Group column, £'000; FY2019-FY2024 (FY2019 is a 10-month Group period - see source note). See source note.",
    rows=PL_ROWS, sources_text=PL_SOURCES, first_col_width=68, source_height=210, unit_suffix=" (£'000)",
)

EQUITY_SOURCES = (
    "Sources - RCI Bank UK Limited Group consolidated statement of changes in equity, £'000 (Group column):\n"
    f"FY2024 & FY2023: Annual Report and Financial Statements for year ended 31 December 2024, printed p.45 "
    f"(PDF p.44), Company and Consolidated Statement of Changes in Equity - {AR24_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements for year ended 31 December 2022, printed p.35 "
    f"(PDF p.34), Company and Consolidated Statement of Changes in Equity - {AR22_URL}\n"
    f"FY2020 (and its 1 January 2020 opening balance): Annual Report and Financial Statements for year ended 31 "
    f"December 2020, printed p.32 (PDF p.31), Company and Consolidated Statement of Equity - {AR20_URL}\n"
    f"FY2019 (10-month Group period from formation on 6 March 2019): Annual Report and Financial Statements for "
    f"year ended 31 December 2019, printed p.32 (PDF p.32, no cover-page offset in this filing), Consolidated "
    f"Statement of Changes in Equity, Group column - {AR19_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    "Every closing balance below ties both to the next year's opening balance and to that year's own Group "
    "Balance Sheet Total equity - zero undocumented plug rows across all 6 years. Non-controlling interests "
    "first appear in FY2023 following the incorporation of 85%-owned Mobilize Lease & Co UK Limited in May 2023; "
    "the merger reserve that exists at Company level is eliminated on consolidation and never appears in the "
    "Group columns above, so it is omitted from this sheet. The Group's opening balance at 1 January 2019 is nil "
    "across every column (RCI Bank UK Limited was a dormant shell with GBP1 net assets throughout FY2018); the "
    "Group came into existence on 6 March 2019 through the acquisition of RCI Financial Services Limited "
    "(brought in at net book value under common control accounting - see the Balance Sheet source note and AR2019 "
    "Note 12), so the 'Acquisition of subsidiary' row below is the Group's true opening equity position, not a "
    "plug."
)

EQUITY_HEADERS = ["Ordinary share capital", "Other reserves", "Retained earnings", "Non-controlling interests", "Total"]

EQUITY_ROWS = [
    ("TOTAL", "Balance at 1 January 2019", (0, 0, 0, None, 0)),
    ("DATA", "Acquisition of subsidiary (RCI Financial Services Limited, common control)", (None, -6088, 266467, None, 260379)),
    ("DATA", "Other shares issued during the year", (184000, None, None, None, 184000)),
    ("DATA", "Profit for the year", (None, None, 61567, None, 61567)),
    ("DATA", "Other comprehensive income/(loss)", (None, -3893, None, None, -3893)),
    ("TOTAL", "Total comprehensive income for the year", (None, -3893, 61567, None, 57674)),
    ("TOTAL", "Balance at 31 December 2019 and 1 January 2020", (290400, -9981, 328034, None, 608453)),
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
    subtitle="Group column, £'000; chronological, 1 January 2019 - 31 December 2024. See source note.",
    headers=EQUITY_HEADERS, rows=EQUITY_ROWS, sources_text=EQUITY_SOURCES, first_col_width=52, source_height=200,
)

bw.add_cash_flow_sheet(
    title="RCI Bank UK Limited - Group Cash Flow Statement",
    subtitle="Group/consolidated basis, £'000; FY2019-FY2024 (FY2019 is a 10-month Group period - see source note). See source note.",
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
    f"pp.54-56) - {AR20_URL}\n"
    f"FY2019: Annual Report and Financial Statements for year ended 31 December 2019, printed pp.58-62 (PDF "
    f"pp.58-62, no cover-page offset in this filing), Note 13 'Loans and advances to customers' - {AR19_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: A separate 'Finance Lease' product line existed alongside HP & PCP and Wholesale through "
    "FY2021; during 2022 the Group reclassified c.£15m of Finance Lease receivables from Loans and advances to "
    "customers into Property, Plant and Equipment (shown as Lease Hire assets), so FY2022 onward carries only "
    "HP & PCP and Wholesale. Gross carrying amount by IFRS 9 stage (rather than by product) is only disclosed at "
    "this granularity for HP & PCP contracts in the FY2022 and FY2021 filings; the ECL loss allowance by stage "
    "is disclosed for all 6 years and is used below for the coverage/Stage 3 metrics, applied to the whole book.\n\n"
    "FY2019 PRESENTATION NOTE: In FY2019, 'Residual value provisions for HP & PCP' (GBP63,707k) is a separate "
    "Group balance sheet liability, not a deduction from the loan asset - so unlike FY2020 onward, the FY2019 "
    "'Net loans and advances to customers' row below is Gross loans less the ECL allowance only, with no RV row "
    "populated for that year (left blank rather than zero, since it genuinely is not part of this note's netting "
    "in FY2019 - see the Balance Sheet source note for where the GBP63,707k appears instead)."
)

AQ_ROWS = [
    ("SECTION", "Gross loans and advances to customers, by product", {}),
    ("DATA", "HP & PCP", {"FY2024": 4166131, "FY2023": 4007471, "FY2022": 3513916, "FY2021": 3079780, "FY2020": 2910212, "FY2019": 2961330}),
    ("DATA", "Finance Lease", {"FY2021": 15291, "FY2020": 11799, "FY2019": 5994}),
    ("DATA", "Wholesale", {"FY2024": 1102294, "FY2023": 1033829, "FY2022": 911100, "FY2021": 437250, "FY2020": 700687, "FY2019": 985887}),
    ("TOTAL", "Gross loans and advances to customers", {"FY2024": 5268425, "FY2023": 5041300, "FY2022": 4425016, "FY2021": 3532321, "FY2020": 3622698, "FY2019": 3953211}),
    ("SECTION", "Expected credit loss (ECL) allowance, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2024": -11318, "FY2023": -15813, "FY2022": -19177, "FY2021": -10376, "FY2020": -19264, "FY2019": -11621}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2024": -4547, "FY2023": -7921, "FY2022": -4898, "FY2021": -3893, "FY2020": -14889, "FY2019": -8671}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2024": -19576, "FY2023": -17738, "FY2022": -14827, "FY2021": -18121, "FY2020": -19310, "FY2019": -16843}),
    ("TOTAL", "Total ECL allowance", {"FY2024": -35441, "FY2023": -41472, "FY2022": -38902, "FY2021": -32390, "FY2020": -53463, "FY2019": -37135}),
    ("DATA", "Residual value provision for HP & PCP", {"FY2024": -62306, "FY2023": -74516, "FY2022": -95883, "FY2021": -85304, "FY2020": -81999}),
    ("TOTAL", "Net loans and advances to customers", {"FY2024": 5170678, "FY2023": 4925312, "FY2022": 4290231, "FY2021": 3414627, "FY2020": 3487236, "FY2019": 3916076}),
    ("SECTION", "Derived asset-quality ratios", {}),
    ("DATA", "ECL coverage ratio (Total ECL allowance / Gross loans)", {"FY2024": "0.67%", "FY2023": "0.82%", "FY2022": "0.88%", "FY2021": "0.92%", "FY2020": "1.48%", "FY2019": "0.94%"}),
    ("DATA", "Stage 3 ECL allowance as % of total ECL allowance", {"FY2024": "55.2%", "FY2023": "42.8%", "FY2022": "38.1%", "FY2021": "55.9%", "FY2020": "36.1%", "FY2019": "45.4%"}),
]

bw.add_asset_quality_sheet(
    title="RCI Bank UK Limited - Group Asset Quality",
    subtitle="Loans and advances to customers, Group column, £'000; FY2019-FY2024 (FY2019 is a 10-month Group period - see source note). See source note.",
    rows=AQ_ROWS, sources_text=AQ_SOURCES, first_col_width=68, source_height=210, unit_suffix=" (£'000)",
)

P3_NONEXISTENCE_NOTE = (
    "FY2022, FY2021 AND FY2020 ARE A SOURCED NEGATIVE, NOT AN OPEN GAP - CLOSED 2026-09-15. RCI Bank UK has "
    "published exactly TWO Pillar 3 disclosures in its history, and both say so themselves, in matching "
    "sentences under the 'Frequency of disclosures' heading of their Scope sections:\n"
    "  - FY2023 edition, section 1.4 'Scope of the Report', printed p.9: \"Our Pillar 3 Disclosures are "
    "published annually with this being the FIRST iteration of the document for MFS UK.\"\n"
    "  - FY2024 edition, section 1.3 'Scope of the Report', PDF p.9 (printed p.8): \"Our Pillar 3 Disclosures "
    "are published annually with this being the SECOND iteration of the document for RCI Bank UK.\"\n"
    "(Emphasis added; the two documents are otherwise near-identical in wording, and the FY2024 cover page "
    "independently carries 'Version 2.0'.) These are the Bank's own statements that no Pillar 3 disclosure "
    "exists for any year before FY2023. No further edition can therefore be found for FY2022, FY2021 or FY2020, "
    "because none was ever produced. Anything still blank for those years on the capital-amount, RWA, leverage, "
    "LCR or NSFR sheets is blank permanently, and should NOT be re-chased in future gap reviews - the only "
    "residual source for those years is the statutory annual report, which discloses ratios but no amounts.\n"
    "Corroborated by enumeration as well as by self-description, so the conclusion does not rest on the "
    "sentence alone: (a) the Bank's own publications index at "
    "https://www.rcibank.co.uk/about-us/facts-and-figures was scraped this session and links exactly two "
    "Pillar 3 PDFs, the FY2023 and FY2024 editions cited above, and no earlier one; (b) an unfiltered Wayback "
    "CDX scan of the whole rcibank.co.uk domain (6,645 unique captures) returns exactly three Pillar 3 URLs, "
    "which are those same two documents (the FY2023 file appears twice, once under an older "
    "/staging/import/ufile/ path).\n"
    "TRAP, EXPLICITLY REJECTED: the same facts-and-figures page also hosts '2021 RCI Business Report EN.pdf', "
    "'RCI_BANQUE_MOBILIZE_Business Report 2022.pdf', 'rci2020_business_report_2020_12.pdf' and "
    "'RCI2023_MOBILIZE_RAPPORT_ACTIVITE_EN_MEL-2_2024_02_19.pdf'. Those are the business reports of RCI Banque "
    "SA / Mobilize Financial Services, the FRENCH PARENT GROUP, not of RCI Bank UK Limited. They cover a "
    "different consolidation in a different currency and must never be used to fill any cell in this workbook, "
    "however tempting their year coverage looks against the FY2020-FY2022 blanks."
)

P3_SOURCES = (
    f"FY2024 and FY2023: RCI Bank UK / Mobilize Financial Services UK Pillar 3 Disclosures, UK KM1 table, "
    f"printed p.24 (FY2024 report) and p.22 (FY2023 report) - {P3_24_URL} - {P3_23_URL}\n"
    f"FY2022 (Pillar 3 basis, Total RWAs and Leverage Ratio only): RCI Bank UK / Mobilize Financial Services UK "
    f"Pillar 3 Disclosures FY2023 - the FY2022 comparative column of Table 1 (UK OV1), printed p.21, and the "
    f"prior-year figures printed on the report's introduction page (printed p.7), which gives CET1 13.98%, "
    f"Tier 1 13.98%, total capital 16.34%, UK leverage 11.10%, LCR 352%, NSFR 138% and RWA GBP4,246m as at "
    f"31 December 2022 - {P3_23_URL}\n"
    f"FY2022-FY2019: RCI Bank UK Annual Reports, Directors' Strategic Report, Capital and Liquidity section - "
    f"{AR22_URL} - {AR21_URL} - {AR20_URL} - {AR19_URL} (FY2019 figures printed p.6, first year of licensed "
    f"banking operations)\n"
    f"RCI Bank UK official facts and figures page (publication links and identity) - {FACTS_URL}\n\n"
    "FY2022 SOURCING NOTE (added 2026-09-15): although RCI Bank UK published no standalone FY2022 Pillar 3 "
    "disclosure, its FY2023 disclosure carries a full set of FY2022 comparatives. Those were re-read this "
    "session and supply two figures the annual reports do not disclose at all - Total RWAs (GBP4,246m) and the "
    "UK leverage ratio (11.10%). The FY2022 ratios already carried here from the annual report are confirmed "
    "unchanged by that comparative set (CET1 13.98%, total capital 16.34%, NSFR 138%), with one small "
    "divergence recorded on the LCR sheet. Absolute CET1/Tier 1/total capital amounts remain blank for "
    "FY2022-FY2019: the FY2023 report's UK CC1 own-funds table is single-column (31 December 2023 only) and "
    "the FY2022 annual report's Capital and Liquidity section was re-OCR'd this session and states only the "
    "two ratios plus 'including GBP100m subordinated debt'. Those amounts are NOT back-solved from ratio x RWA.\n\n"
    + P3_NONEXISTENCE_NOTE
)

SUFFIX = (
    " FY2022-FY2020 ARE A PERMANENT SOURCED NEGATIVE, not an open gap: RCI Bank UK's FY2023 Pillar 3 states it is the 'first iteration of the document' and the FY2024 edition states it is the 'second iteration', so no Pillar 3 disclosure was ever produced for any year before FY2023 - see the sourced-negative section of the source note below. Do not re-chase these cells."
)

def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, P3_SOURCES, note=note, first_col_width=52, source_height=170)

metric("CET1 Capital", "£'000, UK KM1 / Group basis", [("Common Equity Tier 1 (CET1) capital", {"FY2024": 707000, "FY2023": 669000})], "Absolute CET1 capital is disclosed in the UK KM1 table only for FY2024-FY2023; the earlier annual reports disclose ratios but not the absolute capital amount."+SUFFIX)
# CET1 ratio, Pillar 3 UK KM1 basis where a KM1 exists (FY2024/FY2023), annual report
# thereafter. FY2024 CORRECTED 2026-09-15 from 13.69% to 13.46%: see CET1_RATIO_NOTE.
CET1_RATIO = {"FY2024": "13.46%", "FY2023": "13.81%", "FY2022": "13.98%", "FY2021": "15.16%", "FY2020": "15.94%", "FY2019": "14.59%"}
CET1_RATIO_AR = {"FY2024": "13.69%"}

CET1_RATIO_NOTE = (
    "FY2024 CORRECTED 2026-09-15 (13.69% -> 13.46%), and the superseded value is retained on its own labelled "
    "row below rather than discarded. The workbook previously took FY2024's CET1 ratio (13.69%) from the annual "
    "report's narrative while taking FY2024's Tier 1 ratio (13.46%) from the Pillar 3 UK KM1 template. That "
    "combination is internally impossible: Tier 1 capital = CET1 + AT1, so the Tier 1 ratio can never be BELOW "
    "the CET1 ratio, yet the workbook showed 13.69% CET1 against 13.46% Tier 1. The FY2024 Pillar 3 UK KM1 "
    "table (printed p.24) settles it directly - row 5 'Common Equity Tier 1 ratio (%)' = 13.46% and row 6 "
    "'Tier 1 ratio (%)' = 13.46%, identical, against CET1 capital of GBP707m and Tier 1 capital of GBP707m "
    "(also identical, confirming AT1 is nil). The KM1 figure is the correct one for a Pillar 3 metric sheet and "
    "is now used on both sheets, which also makes them mutually consistent. The annual report's 13.69% is a "
    "different vintage/basis, not an error to hide, so it is shown separately. FY2022-FY2019 come from the "
    "annual reports (no Pillar 3 exists for those years - see the source note's sourced-negative section)."
)

metric("CET1 Ratio", "% of RWA",
       [("Common Equity Tier 1 (CET1) ratio (Pillar 3 UK KM1 basis)", CET1_RATIO),
        ("Common Equity Tier 1 (CET1) ratio (annual report narrative basis - FY2024 only, superseded)", CET1_RATIO_AR)],
       CET1_RATIO_NOTE)
metric("Tier 1 Capital", "£'000, UK KM1 / Group basis", [("Tier 1 capital", {"FY2024": 707000, "FY2023": 669000})], "Absolute Tier 1 capital is disclosed in the UK KM1 table only for FY2024-FY2023; earlier annual reports do not disclose the amount."+SUFFIX)
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2024": "13.46%", "FY2023": "13.81%", "FY2022": "13.98%", "FY2021": "15.16%", "FY2020": "15.94%", "FY2019": "14.59%"})], "FY2024 and FY2023 are from the dedicated UK KM1 disclosure (rows 6 and 5 give an identical Tier 1 and CET1 ratio in both years, and rows 1 and 2 give identical CET1 and Tier 1 capital amounts, so AT1 is nil). The FY2024 annual-report narrative instead gives CET1 13.69% and total capital 15.66%, a different reporting basis/rounding vintage; the KM1 value is used here AND on the CET1 Ratio sheet as of the 2026-09-15 correction, so the two sheets are now mutually consistent - see the CET1 Ratio sheet's note for the full explanation and for the superseded annual-report value, which is preserved there on its own row. FY2022-FY2019 assume Tier 1 = CET1 (no AT1 capital is mentioned in any of these annual reports, and no Pillar 3 disclosure exists for those years - see the source note's sourced-negative section).")
metric("Total Capital", "£'000, UK KM1 / Group basis", [("Total capital", {"FY2024": 809000, "FY2023": 774000})], "Absolute total capital is disclosed in the UK KM1 table only for FY2024-FY2023; earlier annual reports do not disclose the amount."+SUFFIX)
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2024": "15.42%", "FY2023": "15.99%", "FY2022": "16.34%", "FY2021": "16.31%", "FY2020": "17.16%", "FY2019": "15.71%"})])
metric("Total RWAs", "£'000, UK KM1 / Group basis", [("Total risk-weighted exposure amount", {"FY2024": 5247000, "FY2023": 4842000, "FY2022": 4246000})], "FY2024-FY2023 are from the UK KM1 table. FY2022 is the comparative column of the FY2023 disclosure's UK OV1 table (printed p.21, row 29 'Total' = GBP4,246m), cross-checked against the same report's introduction page, which prints 'Risk Weighted Assets (RWA) ... (2022: GBP4,246m)'. The FY2021-FY2019 annual reports disclose capital ratios but not RWA amounts, and no Pillar 3 disclosure exists for those years - see the RWA Breakdown source note.")

RWA_SOURCES = (
    f"FY2024 & FY2023: RCI Bank UK / Mobilize Financial Services UK Pillar 3 Disclosures FY2024, Table 1 (UK "
    f"OV1 - Overview of risk weighted exposure amounts), printed p.23 - {P3_24_URL}\n"
    f"FY2022: RCI Bank UK / Mobilize Financial Services UK Pillar 3 Disclosures FY2023, Table 1 (UK OV1), "
    f"printed p.21, FY2022 comparative column - {P3_23_URL}\n\n"
    "PRESENTATION NOTE: RCI Bank UK's Pillar 3 disclosures were not made available as standalone documents "
    "before FY2023 (no dedicated document was located on the bank's site or via the Wayback Machine this "
    "session, despite retrying); the FY2021, FY2020 and FY2019 annual reports disclose capital ratios in their "
    "Strategic Report but not a category-level RWA breakdown. This is a genuine access/non-existence gap, not "
    "an oversight - flagged for follow-up rather than estimated. All disclosed years tie exactly to the Total "
    "RWAs metric sheet.\n\n"
    "RE-VERIFIED 2026-09-15 (independent check, harder evidence than the prior 'not located'): a full "
    "Wayback CDX sweep of the whole rcibank.co.uk domain filtered to URLs containing 'pillar' returns "
    "exactly three archived objects, and they are two documents: the FY2023 disclosure (captured twice, "
    "once under /sites/default/files/2024-11/ and once under a /staging/import/ufile/ path, identical "
    "digest CALW4RNPYXWJ7XYB6DQBRV4VHKQXG2DT) and the FY2024 disclosure. No FY2022, FY2021, FY2020 or "
    "FY2019 Pillar 3 document has EVER been archived on this domain. Six filename permutations for "
    "FY2022 and FY2021, built from the known FY2023/FY2024 URL patterns across plausible upload-month "
    "folders, all return the site's 38,928-byte soft-404 page. Conclusion: RCI Bank UK did not publish "
    "standalone Pillar 3 disclosures before FY2023, so the FY2021/FY2020 category-level RWA breakdown "
    "does not exist to be found - this is a genuine non-disclosure, not an access gap or a search miss, "
    "and should not be re-chased. (The group parent RCI Banque/Mobilize Financial Services publishes its "
    "own consolidated disclosures, but those are a different entity and must not be substituted here.)\n\n"
    "SECOND INDEPENDENT RE-VERIFICATION 2026-09-15, including the rebrand question: the check above was "
    "repeated from scratch without reusing its result, and widened in two ways. (1) The Wayback CDX sweep "
    "was run UNFILTERED over the entire rcibank.co.uk domain (limit 5,000 captures) rather than filtered to "
    "URLs containing 'pillar'. It returns exactly the same two Pillar 3 documents - FY2023 and FY2024 - and "
    "nothing earlier, so the earlier result was not an artefact of the filename filter. (2) The live "
    "publications index at the facts-and-figures page was read directly and lists those same two PDFs and no "
    "others. On the rebrand: RCI Bank UK did rebrand to Mobilize Financial Services UK, and the FY2023 and "
    "FY2024 disclosures are published under the Mobilize name - but on the SAME rcibank.co.uk domain and for "
    "the same legal entity (company 11429127), so no separate pre-FY2023 archive exists under a Mobilize "
    "domain. The facts-and-figures page does also carry 'RCI_BANQUE_MOBILIZE_Business Report 2022.pdf' and "
    "'RCI2023_MOBILIZE_RAPPORT_ACTIVITE_EN.pdf'; both are French PARENT-GROUP business reports for RCI "
    "Banque SA, not UK-entity disclosures, and are excluded under the entity rule rather than mined for "
    "FY2022/FY2021 figures.\n\n"
    "WHAT THIS SWEEP DID RECOVER: re-reading the FY2023 disclosure - a document already cited in this script "
    "- supplied the FY2022 UK OV1 column now shown above, and separately filled FY2022 on the Total RWAs and "
    "Leverage Ratio metric sheets. FY2021 and FY2020 remain genuinely undisclosed. All disclosed years tie "
    "exactly to the Total RWAs metric sheet."
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

metric("Leverage Ratio", "£'000 / %", [("Total exposure measure excluding claims on central banks", {"FY2024": 6642000, "FY2023": 6148000}), ("Leverage ratio excluding claims on central banks (%)", {"FY2024": "10.6%", "FY2023": "10.9%", "FY2022": "11.10%"})], "FY2024-FY2023 are from the dedicated UK KM1 disclosure. FY2022 is disclosed as a prior-year comparative on the introduction page of the FY2023 Pillar 3 report ('UK Leverage Ratio 10.9% (2022: 11.10%)'); the FY2023 report gives no FY2022 total exposure measure, so that row is left blank for FY2022 rather than back-solved. The FY2021-FY2019 annual reports disclose no leverage ratio in any form, and no Pillar 3 disclosure exists for those years.")
metric("LCR", "£'000 / %", [("Total high-quality liquid assets (HQLA), weighted value - average", {"FY2024": 899000, "FY2023": 1035000}), ("Total net cash outflows (adjusted value)", {"FY2024": 365000, "FY2023": 467000}), ("Liquidity Coverage Ratio (%)", {"FY2024": "287%", "FY2023": "236%", "FY2022": "354%", "FY2021": "158%", "FY2020": "551%", "FY2019": "221%"})], "FY2024-FY2023 amounts and ratios are UK KM1. The FY2022-FY2019 headline ratios are from the statutory annual-report Capital and Liquidity sections. BASIS NOTE: the FY2023 Pillar 3 report's introduction page prints the FY2022 LCR as 352%, two points below the 354% the FY2022 annual report states. The annual-report value is retained here for continuity with FY2021-FY2019, which have no Pillar 3 equivalent at all. The gap is rounding/restatement scale rather than a basis break (contrast the KM1 12-month-average vs point-in-time divergences seen at other banks, which run to tens or hundreds of points), so the series is not split into two rows.")
metric("NSFR", "£'000 / %", [("Total available stable funding", {"FY2024": 6115000, "FY2023": 5622000}), ("Total required stable funding", {"FY2024": 4863000, "FY2023": 4312000}), ("NSFR ratio (%)", {"FY2024": "126%", "FY2023": "130%", "FY2022": "138%", "FY2021": "109%", "FY2020": "138%", "FY2019": "122%"})], "FY2024-FY2023 amounts and ratios are UK KM1. The FY2022-FY2019 headline ratios are from the statutory annual-report Capital and Liquidity sections.")
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No quantitative MREL ratio was found in the RCI Bank UK annual reports, the RCI Bank UK Pillar 3 disclosures reviewed, or the official facts-and-figures page.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2024": 7299251, "FY2023": 6932488, "FY2022": 6297529, "FY2021": 4995682, "FY2020": 4922345, "FY2019": 5014222}),
        ("Loans and advances to customers", {"FY2024": 5170678, "FY2023": 4925312, "FY2022": 4290231, "FY2021": 3414627, "FY2020": 3487236, "FY2019": 3916076}),
        ("Deposits from customers", {"FY2024": 4978566, "FY2023": 4794623, "FY2022": 4140482, "FY2021": 2929460, "FY2020": 3149310, "FY2019": 2953593}),
        ("Total equity", {"FY2024": 723469, "FY2023": 696139, "FY2022": 646867, "FY2021": 641337, "FY2020": 616637, "FY2019": 608453}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {"FY2024": 391562, "FY2023": 300157, "FY2022": 254927, "FY2021": 267807, "FY2020": 164186, "FY2019": 202520}),
        ("Total operating expense (cost of sales + operating costs)", {"FY2024": -290283, "FY2023": -211649, "FY2022": -142966, "FY2021": -164138, "FY2020": -83407, "FY2019": -124081}),
        ("Profit after tax for the financial year", {"FY2024": 26593, "FY2023": 49787, "FY2022": 108739, "FY2021": 107133, "FY2020": 61537, "FY2019": 61567}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Total comprehensive income for the year", {"FY2024": 27330, "FY2023": 49047, "FY2022": 112663, "FY2021": 111562, "FY2020": 59584, "FY2019": 57674}),
        ("Dividend paid", {"FY2022": -107133, "FY2021": -86862, "FY2020": -51400}),
        ("Total equity (closing)", {"FY2024": 723469, "FY2023": 696139, "FY2022": 646867, "FY2021": 641337, "FY2020": 616637, "FY2019": 608453}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2024": 160113, "FY2023": 38755, "FY2022": 472150, "FY2021": 689232, "FY2020": 642905, "FY2019": 501914}),
        ("Net cash generated from/(used in) investing activities", {"FY2024": -347349, "FY2023": -290446, "FY2022": -898, "FY2021": -552065, "FY2020": 476440, "FY2019": -560040}),
        ("Net cash (used in)/generated from financing activities", {"FY2024": 98614, "FY2023": 99107, "FY2022": -8029, "FY2021": -487797, "FY2020": -151400, "FY2019": 24000}),
        ("Cash and cash at central banks at 31 December", {"FY2024": 959888, "FY2023": 1048510, "FY2022": 1201094, "FY2021": 737871, "FY2020": 1088501, "FY2019": 120556}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", {"FY2024": "15.42%", "FY2023": "15.99%", "FY2022": "16.34%", "FY2021": "16.31%", "FY2020": "17.16%", "FY2019": "15.71%"}),
        ("LCR", {"FY2024": "287%", "FY2023": "236%", "FY2022": "354%", "FY2021": "158%", "FY2020": "551%", "FY2019": "221%"}),
        ("NSFR", {"FY2024": "126%", "FY2023": "130%", "FY2022": "138%", "FY2021": "109%", "FY2020": "138%", "FY2019": "122%"}),
    ],
    note="Cash flows are RCI Bank UK Group consolidated figures. Dedicated UK KM1 Pillar 3 amounts are available for FY2024-FY2023; earlier years use explicitly disclosed annual-report ratios. FY2019 is a 10-month Group period (6 March-31 December 2019) and FY2018 is excluded - RCI Bank UK Limited was dormant that whole year (2-page nil dormant-company filing) - see the Cash Flow Statement source note for both. Blank cells mean not disclosed, not zero.",
)

bw.save("/Users/armaan/code/katalysis/banks/RCI BANK UK FINANCIALS.xlsx")
