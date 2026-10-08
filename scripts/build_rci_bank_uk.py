import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]

# The FY2025 accounts were filed at Companies House on 29 September 2026 (A08 barcode
# *AFBMZRSA*, #114) and are a PURE SCAN - pdftotext returns nothing, so every figure
# taken from them was read off a 300 dpi page image and re-read off an independent
# 400 dpi render. Companies House does not expose a stable per-document URL that can be
# cited here without guessing its filing-history id, so the filing-history index for
# company 11429127 is cited instead and the filing is identified by its barcode and date.
AR25_URL = "https://find-and-update.company-information.service.gov.uk/company/11429127/filing-history"
AR25_CITE = (
    "Annual Report and Financial Statements for the year ended 31 December 2025 "
    "(Companies House filing stamped A08 29/09/2026 #114, barcode AFBMZRSA; Board approval "
    "24 April 2026, Forvis Mazars LLP unqualified opinion signed 25 April 2026), company "
    f"11429127 - {AR25_URL}"
)

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
    "because the bank's lending and lease operations sit in its subsidiaries. FY2025 is the latest available "
    "statutory filing (filed 29 September 2026). All seven reports are scanned PDFs; the FY2019-FY2024 values were "
    "OCR-processed and cross-checked against the printed totals and later comparative columns, while every FY2025 "
    "figure was read directly off a 300 dpi page image and independently re-read off a 400 dpi render (the FY2025 "
    "filing has no text layer at all).\n\n"
    "FY2025 RESTATEMENT NOTE (note 39, printed pp.139-140). The FY2025 accounts restate FY2024 and the 1 January "
    "2024 opening position for a Lease Hire depreciation system error corrected retrospectively under IAS 8. This "
    "workbook keeps FY2024 and FY2023 on their ORIGINAL as-reported basis - the basis each year's own edition "
    "published - and records the restatement separately rather than overwriting them. The restated amounts the "
    "bank prints are: at 31/12/2024, property plant and equipment 679,541 -> 689,260 (+9,719), deferred tax asset "
    "31,036 -> 28,606 (-2,430), total assets 7,299,251 -> 7,306,540 (+7,289), retained earnings 436,990 -> 444,279 "
    "(+7,289), total equity 723,469 -> 730,758 (+7,289), depreciation (104,189) -> (100,075) (+4,114), tax expense "
    "(10,922) -> (11,951) (-1,029), profit for the year 26,593 -> 29,678 (+3,085); and at 01/01/2024 (this "
    "workbook's FY2023 closing position), property plant and equipment 575,015 -> 580,620 (+5,605), deferred tax "
    "asset 18,541 -> 17,140 (-1,401), retained earnings 409,935 -> 414,139 (+4,204), total equity 696,139 -> "
    "700,343 (+4,204) and total liabilities and shareholder equity 6,932,488 -> 6,936,692 (+4,204). Both sets are "
    "the bank's own figures and neither has been moved towards the other.\n"
    "A PRINTED ROW THAT DOES NOT SAY WHAT IT LABELS, REPORTED NOT CORRECTED: in the 01/01/2024 half of note 39 "
    "(printed p.139) the row labelled 'Total Assets' prints 6,236,349 -> 6,240,553. 6,236,349 is the Group's total "
    "LIABILITIES at 01/01/2024 (the FY2025 balance sheet's own 01/01/2024 column prints total liabilities at that "
    "figure, unrestated); the Group's as-reported total assets at that date was 6,932,488, which is what the same "
    "table's final row prints. The equivalent 31/12/2024 table on p.140 does not have this problem. Nothing has "
    "been adjusted - the bank's table is reproduced as printed and the inconsistency is recorded here.\n\n"
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
    f"FY2025: {AR25_CITE}, printed pp.50-51 (PDF pp.50-51, zero folio offset), 'COMPANY AND CONSOLIDATED "
    f"STATEMENT OF CASH FLOWS', Group 2025 column. The statement prints FOUR columns - Company 2025, Company "
    f"2024, Group 2025 and Group 2024 (Restated*) - and only the Group 2025 column is transcribed here.\n"
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
    "subtotals below tie exactly to the as-reported figures with no plug required.\n\n"
    "FY2025 PRESENTATION NOTES.\n"
    "(i) THE DEPRECIATION LINE IS NOW TWO PRINTED LINES AND IS NOT SUMMED HERE. Through FY2024 the bank "
    "printed one combined add-back. On printed p.50 the FY2025 statement prints 'Depreciation (Restated*)' "
    "(note 17) at 135,111 and 'Amortisation' (note 22) at 380 as two separate lines, so this sheet carries "
    "two rows: the long-standing 'Depreciation and amortisation' row holds the printed DEPRECIATION figure "
    "alone for FY2025, and a new 'Amortisation' row holds the 380. Their sum, 135,491, is printed NOWHERE in "
    "the filing and is deliberately not shown. FY2019-FY2024 keep the single combined figure each of those "
    "editions printed. For context on why the FY2024 combined 104,189 is not simply the FY2025 edition's "
    "restated 100,075 plus 268: the restatement cut FY2024 depreciation by 4,114, and the FY2024 edition's "
    "single line was depreciation only, its 268 of amortisation sitting inside operating expenses (whose "
    "FY2024 figure, 70,151, is unchanged).\n"
    "(ii) A NEW FINANCING LINE, AND A BLANK THAT IS NOT A DASH. 'Increase in subordinated loan' 29,000 is "
    "printed on p.51 between 'Issuing of ordinary share capital' and 'Property lease rent paid', and is "
    "reproduced in that position on its own row rather than folded into the existing 'Proceeds from "
    "subordinated debt' row, which is a DIFFERENT printed label used only in FY2020 and FY2019. Its 2024 "
    "cells are GENUINELY BLANK - nothing printed at all, in either the Company or the Group column - whereas "
    "every row around it prints an explicit dash in its 2024 cells. That distinction was confirmed on both a "
    "300 dpi and a 400 dpi rendering, so FY2024 is left EMPTY on this row, not set to zero. Corroborated at "
    "note 26 (printed p.97): 'During 2025 a third tranche of GBP29m with a maturity date of June 2037 was "
    "entered into at a rate of Compounded Daily SONIA plus 2.71%', taking subordinated debt from GBP100m to "
    "GBP129m.\n"
    "(iii) THREE PRINTED DASHES in the Group 2025 column are carried as 0, the bank saying nil: 'Loan to "
    "subsidiary', 'Purchasing of investment securities' and 'Debt securities issued/(redeemed)'. The "
    "statement also prints a 'Loan from subsidiary' line, but it is dashed in both Group columns and is a "
    "Company-level item, so no row is added for it.\n"
    "(iv) NO PLUG ROW IS NEEDED FOR FY2025. The printed Group 2025 column foots exactly as printed: "
    "operating adds to (15,017), less 34,707 of tax paid gives (49,724); investing (337,782)+(10)+0+125,000 = "
    "(212,792); financing 0+45,000+29,000-874-171 = 72,955; net (189,561); and 959,888-189,561 = 770,327, "
    "which agrees with Cash and cash at central banks on the FY2025 balance sheet. The 'Other operating items "
    "included in reported subtotal' and 'Other financing items included in reported subtotal' rows are "
    "therefore left blank for FY2025.\n"
    "(v) AN EDITION DIFFERENCE IN THE 2024 COLUMN THAT IS NOT A RESTATEMENT, RECORDED NOT APPLIED. The FY2025 "
    "edition prints 'Impairment of financial assets' for 2024 as 16, where this sheet carries the FY2024 "
    "edition's own 57; and with 16 in place, the FY2025 edition's 2024 operating column foots to 192,018 with "
    "no residual, so it prints no equivalent of this sheet's FY2024 plug of 227. Note 39 does NOT list this "
    "line among the restated items, so it is an edition difference rather than part of the prior-period "
    "error. FY2024 is left exactly as the FY2024 edition published it (57, with the 227 plug), per the rule "
    "that a prior year keeps its own edition's as-reported figures. Both readings are recorded here and "
    "neither has been moved towards the other.\n"
    "(vi) THE RESTATED 2024 COLUMN, FOR THE RECORD. The FY2025 edition restates 2024 profit before taxation "
    "to 41,629 (this sheet keeps 37,515) and splits 2024 depreciation as 100,075 + 268 (this sheet keeps the "
    "combined 104,189). Every other 2024 figure in that column matches this sheet digit for digit: derivative "
    "financial instruments 18,732, profit on disposal of investment securities (6,008), provision for "
    "liabilities 73,644, other non-cash (462), loans and advances (245,366), NBV to inventory 125,434, "
    "inventory (28,631), other assets (70,864), other liabilities 2,516, pension (2,468), customer deposits "
    "183,943, bank deposits (440), cash generated by operations 192,018, income taxes paid (31,905), net "
    "operating 160,113, purchase of PP&E (334,148), intangible (980), purchasing of investment securities "
    "(244,257), proceeds 232,036, net investing (347,349), debt securities 100,000, property lease rent "
    "(1,188), interest on property lease (198), net financing 98,614, net decrease (88,622), opening "
    "1,048,510 and closing 959,888."
)

bw = BankWorkbook(bank_name="RCI Bank UK Limited", years=YEARS, header_color="174A5B")

rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": -82909, "FY2024": 37515, "FY2023": 63631, "FY2022": 131197, "FY2021": 127547, "FY2020": 71623, "FY2019": 75988}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 135111, "FY2024": 104189, "FY2023": 92713, "FY2022": 52443, "FY2021": 35811, "FY2020": 28245, "FY2019": 23686}),
    # FY2025 SPLITS THIS LINE IN TWO. The row above carries the printed "Depreciation (Restated*)" figure
    # ALONE for FY2025 (note 17); "Amortisation" (note 22) is printed as its own line and gets its own row
    # below. The two are NOT summed - 135,111 + 380 appears nowhere in the filing. See the source note.
    ("DATA", "Amortisation", {"FY2025": 380}),
    ("DATA", "Net book value of property, plant and equipment disposed", {"FY2021": 36583, "FY2020": 45774}),
    ("DATA", "Gain on sale of property, plant and equipment", {"FY2019": -251}),
    ("DATA", "Impairment of financial assets", {"FY2025": 29, "FY2024": 57, "FY2023": 57, "FY2022": 37, "FY2021": 65, "FY2020": -151, "FY2019": -2115}),
    ("DATA", "Loss/(gain) on fair value adjustment - derivatives", {"FY2023": 30339, "FY2021": -11969, "FY2020": 55, "FY2019": 3353}),
    ("DATA", "Derivative financial instruments", {"FY2025": 19269, "FY2024": 18732, "FY2022": -47914, "FY2020": 228, "FY2019": 3841}),
    ("DATA", "Interest income", {"FY2022": 2018, "FY2021": -23, "FY2020": -1458}),
    ("DATA", "Interest expenses", {"FY2023": 7864, "FY2022": -2051, "FY2021": 1732, "FY2020": 1737, "FY2019": 1438}),
    ("DATA", "Profit on disposal of investment securities", {"FY2025": -2945, "FY2024": -6008, "FY2023": -4940}),
    ("DATA", "Provision for liabilities", {"FY2025": 145597, "FY2024": 73644}),
    ("DATA", "Other non-cash or non-operating items", {"FY2025": -888, "FY2024": -462, "FY2023": 100}),
    ("DATA", "Loans and advances to customers", {"FY2025": -273647, "FY2024": -245366, "FY2023": -635081, "FY2022": -890629, "FY2021": 72609, "FY2020": 412363, "FY2019": 134813}),
    ("DATA", "NBV of vehicles transferred to inventory", {"FY2025": 147176, "FY2024": 125434, "FY2023": 83828, "FY2022": 74920}),
    ("DATA", "Inventory", {"FY2025": -17931, "FY2024": -28631, "FY2023": -8468, "FY2022": -6497, "FY2021": 12434, "FY2020": 14535, "FY2019": -19210}),
    ("DATA", "Other assets", {"FY2025": -4322, "FY2024": -70864, "FY2023": -30614, "FY2022": -18531, "FY2021": -18531, "FY2020": -20422, "FY2019": -79904}),
    ("DATA", "Other liabilities", {"FY2025": 45653, "FY2024": 2516, "FY2023": 5379, "FY2022": 73787, "FY2021": -25651, "FY2020": -4527, "FY2019": 69191}),
    ("DATA", "Residual value provisions for HP & PCP", {"FY2019": -1457}),
    ("DATA", "Pension contributions paid and amounts recognised in income statement", {"FY2025": 42, "FY2024": -2468, "FY2023": -2366, "FY2022": -128, "FY2021": -104, "FY2020": -103, "FY2019": -47}),
    ("DATA", "Customer deposits", {"FY2025": 288975, "FY2024": 183943, "FY2023": 654141, "FY2022": 1211022, "FY2021": -219850, "FY2020": 195717, "FY2019": 110055}),
    ("DATA", "Bank deposits", {"FY2025": -414607, "FY2024": -440, "FY2023": -200051, "FY2022": -89121, "FY2021": 704439, "FY2020": -37451, "FY2019": 187533}),
    ("DATA", "Loan to subsidiary", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Other operating items included in reported subtotal", {"FY2024": 227, "FY2021": -2594, "FY2020": -47952}),
    ("TOTAL", "Cash generated by operations", {"FY2025": -15017, "FY2024": 192018, "FY2023": 56532, "FY2022": 490553, "FY2021": 712498, "FY2020": 658213, "FY2019": 506914}),
    ("DATA", "Income taxes paid", {"FY2025": -34707, "FY2024": -31905, "FY2023": -17777, "FY2022": -18403, "FY2021": -23266, "FY2020": -15308, "FY2019": -5000}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": -49724, "FY2024": 160113, "FY2023": 38755, "FY2022": 472150, "FY2021": 689232, "FY2020": 642905, "FY2019": 501914}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -337782, "FY2024": -334148, "FY2023": -331888, "FY2022": -265940, "FY2021": -132014, "FY2020": -122580, "FY2019": -64655}),
    ("DATA", "Intangible asset", {"FY2025": -10, "FY2024": -980, "FY2023": -1000}),
    ("DATA", "Purchasing of investment securities", {"FY2025": 0, "FY2024": -244257, "FY2023": -231803, "FY2022": -761812, "FY2021": -430074, "FY2020": -1437759, "FY2019": -2085873}),
    ("DATA", "Proceeds from investment securities", {"FY2025": 125000, "FY2024": 232036, "FY2023": 290000, "FY2022": 1024803, "FY2021": 10000, "FY2020": 1988828, "FY2019": 1539635}),
    ("DATA", "Profit on disposal of investment securities", {"FY2022": 2051}),
    ("DATA", "Investment in associate", {"FY2023": -15980}),
    ("DATA", "Non-controlling interest subscription", {"FY2023": 225}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2021": 0, "FY2020": 49409, "FY2019": 54227}),
    ("DATA", "Interest income", {"FY2021": 23, "FY2020": -1458, "FY2019": -3374}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2025": -212792, "FY2024": -347349, "FY2023": -290446, "FY2022": -898, "FY2021": -552065, "FY2020": 476440, "FY2019": -560040}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Proceeds from subordinated debt", {"FY2020": 40000, "FY2019": 40000}),
    ("DATA", "Debt securities issued/(redeemed)", {"FY2025": 0, "FY2024": 100000, "FY2023": 100000, "FY2021": -400000, "FY2020": -200000, "FY2019": -200000}),
    ("DATA", "Issuing of ordinary share capital", {"FY2025": 45000, "FY2019": 184000}),
    # NEW FY2025 LINE, printed between "Issuing of ordinary share capital" and "Property lease rent paid"
    # on folio 51 and reproduced in that position. Its 2024 cells are GENUINELY BLANK in the source - the
    # rows around it print an explicit dash - so FY2024 is left empty here rather than set to zero.
    ("DATA", "Increase in subordinated loan", {"FY2025": 29000}),
    ("DATA", "Dividends paid", {"FY2021": -86862, "FY2020": -51400}),
    ("DATA", "Property lease rent paid", {"FY2025": -874, "FY2024": -1188, "FY2023": -672, "FY2022": -654, "FY2021": -935}),
    ("DATA", "Interest on property lease", {"FY2025": -171, "FY2024": -198, "FY2023": -221, "FY2022": -242}),
    ("DATA", "Other financing items included in reported subtotal", {"FY2022": -7133, "FY2020": 60000}),
    ("TOTAL", "Net cash (used in)/generated from financing activities", {"FY2025": 72955, "FY2024": 98614, "FY2023": 99107, "FY2022": -8029, "FY2021": -487797, "FY2020": -151400, "FY2019": 24000}),
    ("TOTAL", "Net increase/(decrease) in cash and cash at central banks", {"FY2025": -189561, "FY2024": -88622, "FY2023": -152584, "FY2022": 463223, "FY2021": -350630, "FY2020": 967945, "FY2019": -34126}),
    ("DATA", "Cash and cash at central banks at 1 January", {"FY2025": 959888, "FY2024": 1048510, "FY2023": 1201094, "FY2022": 737871, "FY2021": 1088501, "FY2020": 120556, "FY2019": 0}),
    ("DATA", "Cash on transfer of Branch/acquisition of Subsidiary", {"FY2019": 154682}),
    ("TOTAL", "Cash and cash at central banks at 31 December", {"FY2025": 770327, "FY2024": 959888, "FY2023": 1048510, "FY2022": 1201094, "FY2021": 737871, "FY2020": 1088501, "FY2019": 120556}),
]

BS_SOURCES = (
    "Sources - RCI Bank UK Limited Group consolidated balance sheet, £'000 (Group column):\n"
    f"FY2025: {AR25_CITE}, printed p.47 (PDF p.47, zero folio offset), 'COMPANY AND CONSOLIDATED BALANCE SHEET', "
    f"Group 2025 column. That page prints FIVE columns - Company 2025, Company 2024, Group 2025, Group 2024 "
    f"(Restated*) and Group 01/01/2024 (Restated*), the last being the IAS 8 opening-position column the "
    f"restatement requires. Only the Group 2025 column is transcribed here; the Group 2024 and 01/01/2024 columns "
    f"are RESTATED and are recorded in the restatement note rather than written over this workbook's as-reported "
    f"FY2024 and FY2023 columns.\n"
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
    "gross loans less ECL allowance only (no RV deduction), reconciling exactly to Note 13 of the FY2019 accounts.\n\n"
    "FY2025 PRESENTATION NOTES. (i) Three Group 2025 lines print an explicit DASH, not a blank: Investment "
    "securities, Current tax liabilities and Retirement benefit liability. A dash is the bank saying nil, so each "
    "is carried as 0 here, the same treatment the FY2020 Investment securities dash already gets above. The "
    "Investment securities nil is corroborated at note 15 (printed p.88): 'During the year the company disposed "
    "of GBP123.7m of Treasury Bills resulting in the balance held at 31 December 2025 being GBPnil (2024: "
    "GBP123.7m)'. (ii) 'Current tax asset' is live again at 18,567 after being dashed in both the 2024 and "
    "01/01/2024 columns. (iii) The printed row label for share capital is 'Issued capital' and for the final row "
    "'TOTAL LIABILITIES AND SHAREHOLDERS' EQUITY'; this workbook's long-standing labels are kept so the series "
    "reads continuously. (iv) The FY2019-only 'Residual value provisions for HP & PCP' liability line is not "
    "printed in FY2025 and is left blank, not zero. (v) Every FY2025 Group line maps to a row that already "
    "existed; no new balance sheet row was needed. The Group column foots exactly as printed with no plug.\n"
    "FY2025 vs the prior-year columns - see the restatement note above. The FY2025 edition's Group 2024 column "
    "prints property plant and equipment 689,260, deferred tax asset 28,606, total assets 7,306,540, retained "
    "earnings 444,279, total equity 730,758 and total liabilities and equity 7,306,540, all restated. The FY2024 "
    "column on this sheet deliberately keeps the as-reported 679,541 / 31,036 / 7,299,251 / 436,990 / 723,469 / "
    "7,299,251 that the FY2024 edition published. Likewise the FY2025 edition's 01/01/2024 column restates this "
    "workbook's FY2023 property plant and equipment to 580,620, deferred tax asset to 17,140, retained earnings "
    "to 414,139, total equity to 700,343 and the balance sheet total to 6,936,692, while FY2023 here keeps "
    "575,015 / 18,541 / 409,935 / 696,139 / 6,932,488. Every other line in that 01/01/2024 column is identical to "
    "this workbook's FY2023 figures. The two bases are recorded, never reconciled."
)

BS_ROWS = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash at central banks", {"FY2025": 770327, "FY2024": 959888, "FY2023": 1048510, "FY2022": 1201094, "FY2021": 737871, "FY2020": 1088501, "FY2019": 120556}),
    ("DATA", "Derivative financial instruments", {"FY2025": 2991, "FY2024": 11829, "FY2023": 37622, "FY2022": 55475, "FY2021": 10254, "FY2020": 1388, "FY2019": 35}),
    ("DATA", "Investment securities - UK Treasury Bills at FVOCI", {"FY2025": 0, "FY2024": 123749, "FY2023": 105575, "FY2022": 157926, "FY2021": 419939, "FY2020": 0, "FY2019": 548818}),
    ("DATA", "Inventory", {"FY2025": 64822, "FY2024": 46891, "FY2023": 18260, "FY2022": 9792, "FY2021": 3295, "FY2020": 15729, "FY2019": 30264}),
    ("DATA", "Loans and advances to customers", {"FY2025": 5444325, "FY2024": 5170678, "FY2023": 4925312, "FY2022": 4290231, "FY2021": 3414627, "FY2020": 3487236, "FY2019": 3916076}),
    ("DATA", "Property, plant and equipment", {"FY2025": 744754, "FY2024": 679541, "FY2023": 575015, "FY2022": 419670, "FY2021": 266068, "FY2020": 206448, "FY2019": 157891}),
    ("DATA", "Current tax asset", {"FY2025": 18567, "FY2022": 0, "FY2021": 1273}),
    ("DATA", "Deferred tax asset", {"FY2025": 59396, "FY2024": 31036, "FY2023": 18541, "FY2022": 7203, "FY2021": 4748, "FY2020": 3967, "FY2019": 2621}),
    ("DATA", "Other assets", {"FY2025": 261938, "FY2024": 257616, "FY2023": 186752, "FY2022": 156138, "FY2021": 137607, "FY2020": 119076, "FY2019": 237961}),
    ("DATA", "Investment in associate", {"FY2025": 16583, "FY2024": 16311, "FY2023": 15901}),
    ("DATA", "Intangible assets", {"FY2025": 1342, "FY2024": 1712, "FY2023": 1000}),
    ("TOTAL", "Total assets", {"FY2025": 7385045, "FY2024": 7299251, "FY2023": 6932488, "FY2022": 6297529, "FY2021": 4995682, "FY2020": 4922345, "FY2019": 5014222}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from customers", {"FY2025": 5267541, "FY2024": 4978566, "FY2023": 4794623, "FY2022": 4140482, "FY2021": 2929460, "FY2020": 3149310, "FY2019": 2953593}),
    ("DATA", "Deposits from banks", {"FY2025": 150302, "FY2024": 564909, "FY2023": 565349, "FY2022": 765400, "FY2021": 854521, "FY2020": 150082, "FY2019": 187533}),
    ("DATA", "Derivative financial instruments", {"FY2025": 16331, "FY2024": 5900, "FY2023": 12961, "FY2022": 475, "FY2021": 3168, "FY2020": 8865, "FY2019": 7229}),
    ("DATA", "Debt securities issued", {"FY2025": 700000, "FY2024": 700000, "FY2023": 600000, "FY2022": 500000, "FY2021": 400000, "FY2020": 800000, "FY2019": 900000}),
    ("DATA", "Current tax liabilities", {"FY2025": 0, "FY2024": 5723, "FY2023": 13994, "FY2022": 6544, "FY2020": 452, "FY2019": 5076}),
    ("DATA", "Residual value provisions for HP & PCP", {"FY2019": 63707}),
    ("DATA", "Other liabilities", {"FY2025": 319969, "FY2024": 246255, "FY2023": 245125, "FY2022": 232934, "FY2021": 158024, "FY2020": 182878, "FY2019": 277745}),
    ("DATA", "Provision for liabilities", {"FY2025": 219241, "FY2024": 73644}),
    ("DATA", "Retirement benefit liability", {"FY2025": 0, "FY2024": 785, "FY2023": 4297, "FY2022": 4827, "FY2021": 9172, "FY2020": 14121, "FY2019": 10886}),
    ("TOTAL", "Total liabilities", {"FY2025": 6673384, "FY2024": 6575782, "FY2023": 6236349, "FY2022": 5650662, "FY2021": 4354345, "FY2020": 4305708, "FY2019": 4405769}),
    ("SECTION", "Equity", {}),
    ("DATA", "Issued/ordinary share capital", {"FY2025": 335400, "FY2024": 290400, "FY2023": 290400, "FY2022": 290400, "FY2021": 290400, "FY2020": 290400, "FY2019": 290400}),
    ("DATA", "Retained earnings", {"FY2025": 381750, "FY2024": 436990, "FY2023": 409935, "FY2022": 360048, "FY2021": 358442, "FY2020": 338171, "FY2019": 328034}),
    ("DATA", "Non-controlling interests", {"FY2025": -1225, "FY2024": -337, "FY2023": 125}),
    ("DATA", "Other reserves", {"FY2025": -4264, "FY2024": -3584, "FY2023": -4321, "FY2022": -3581, "FY2021": -7505, "FY2020": -11934, "FY2019": -9981}),
    ("TOTAL", "Total equity", {"FY2025": 711661, "FY2024": 723469, "FY2023": 696139, "FY2022": 646867, "FY2021": 641337, "FY2020": 616637, "FY2019": 608453}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 7385045, "FY2024": 7299251, "FY2023": 6932488, "FY2022": 6297529, "FY2021": 4995682, "FY2020": 4922345, "FY2019": 5014222}),
]

bw.add_balance_sheet_sheet(
    title="RCI Bank UK Limited - Group Balance Sheet",
    subtitle="Company and Consolidated Statement of Financial Position, Group column, £'000; FY2019-FY2025 (FY2019 is a 10-month Group period - see source note). See source note.",
    rows=BS_ROWS, sources_text=BS_SOURCES, first_col_width=58, source_height=200, unit_suffix=" (£'000)",
)

PL_SOURCES = (
    "Sources - RCI Bank UK Limited Group consolidated statement of profit or loss, £'000 (Group column):\n"
    f"FY2025: {AR25_CITE}, printed p.45 (PDF p.45, zero folio offset), 'CONSOLIDATED STATEMENT OF PROFIT OR "
    f"LOSS', Group 2025 column; the other-comprehensive-income lines from printed p.46, 'CONSOLIDATED "
    f"STATEMENT OF OTHER COMPREHENSIVE INCOME', Group 2025 column. Unlike the balance sheet, BOTH these "
    f"statements are GROUP ONLY - two columns, 2025 and 2024 (Restated*), with no Company column at all. The "
    f"2024 column is restated and is NOT written over this workbook's as-reported FY2024.\n"
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
    "as-reported FY2019 structure, not a workbook estimate.\n\n"
    "FY2025 PRESENTATION NOTES. (i) FY2025 IS A LOSS YEAR AND THE TAX LINE IS A CREDIT. The printed labels "
    "change accordingly - '(Loss)Profit before tax' (sic, the bank omits the slash), 'Tax credit/(expense)' "
    "and '(Loss)/Profit after tax for the financial year'. This workbook's long-standing row labels ('Profit "
    "before tax', 'Tax expense', 'Profit after tax for the financial year') are kept so the seven-year series "
    "reads continuously; the FY2025 cells carry the printed signs, so Tax expense is POSITIVE 19,492 in FY2025 "
    "because the bank printed a tax credit, not an expense. Three further printed labels differ cosmetically "
    "from this sheet's: 'Change in provision for changes in residual value on HP & PCP vehicles', 'Change in "
    "provision for expected credit loss on investment securities' (singular 'loss') and 'Loss on derivatives - "
    "fair value adjustment'. Each maps one-for-one to the existing row.\n"
    "(ii) THE 'Attributable to:' BLOCKS ARE NEW AND ARE REPRODUCED BECAUSE THE BANK PRINTS THEM. FY2025 is the "
    "first year this statement splits the result between the owners of the parent and the non-controlling "
    "interest on the face of the P&L. Both printed blocks are reproduced in their printed position and "
    "wording - one on p.45 beneath '(Loss)/Profit after tax for the financial year' ((62,529) owners, (888) "
    "non-controlling, (63,417) total) and one on p.46 beneath 'Total Comprehensive (Loss)/Income for the year' "
    "((63,209) owners, (888) non-controlling, (64,097) total). The bank prints the closing total of each block "
    "with NO row label at all; the labels used for those two rows here say so explicitly rather than inventing "
    "a caption. These rows carry FY2025 ONLY. The FY2025 edition does print a 2024 column for both blocks "
    "(30,140 / (462) / 29,678 and 30,877 / (462) / 30,415), but those are RESTATED figures and are therefore "
    "not placed in this workbook's as-reported FY2024 column; FY2024's own as-reported split (27,055 to the "
    "owners, (462) to the non-controlling interest) is on the Statement of Changes in Equity sheet, from the "
    "FY2024 edition. The earlier years are blank here because no earlier edition printed the block.\n"
    "(iii) FY2025 FOOTS EXACTLY AS PRINTED, NO PLUG: 148,302+15,026+173,503+190,376 = 527,207; then "
    "527,207-216,829-135,111-81,285-150,000-2,268-17,626+29-10,609+2,945+638 = (82,909); (82,909)+19,492 = "
    "(63,417); (63,417)+(680) = (64,097).\n"
    "(iv) THE RESTATEMENT, RECORDED NOT APPLIED - see also the entity note above. The FY2025 edition's 2024 "
    "column prints depreciation (100,075) not (104,189), profit before tax 41,629 not 37,515, tax (11,951) not "
    "(10,922), profit after tax 29,678 not 26,593 and total comprehensive income 30,415 not 27,330. This "
    "sheet's FY2024 column deliberately keeps the figures the FY2024 edition itself published. Every other "
    "2024 line in the FY2025 edition agrees with this sheet digit for digit (interest income 437,390, interest "
    "expense (313,697), net interest income 123,693, fee income 12,118, fee expense (931), net fee 11,187, "
    "operating lease rentals 141,203, revenue on sale of inventories 115,479, total income 391,562, cost of "
    "sales (115,943), operating expenses (70,151), change in provision for liabilities (73,644), residual "
    "value 12,209, ECL on loans (1,301), ECL on investment securities 16, derivatives (7,561), profit on "
    "disposal 6,008, equity-method income 509, OCI 737). The two bases are recorded, never reconciled.\n"
    "(v) A DISAGREEMENT BETWEEN THE BANK'S OWN TWO STATEMENTS, REPRODUCED NOT RECONCILED. The Group statement "
    "of changes in equity on printed p.49 shows a 2025 row labelled 'Total comprehensive income' totalling "
    "(18,209), because that row also carries the 45,000 share issue in its ordinary-share-capital column. A "
    "share issue is not comprehensive income, and this statement gives total comprehensive loss as (64,097) on "
    "p.46. Both figures are the bank's own, printed four pages apart, and differ by exactly the 45,000 share "
    "issue plus the (888) non-controlling split. Neither has been moved towards the other; see the Statement "
    "of Changes in Equity sheet, where the row is reproduced as printed."
)

PL_ROWS = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 446475, "FY2024": 437390, "FY2023": 354682, "FY2022": 198217, "FY2021": 136838, "FY2020": 179280, "FY2019": 170847}),
    ("DATA", "Interest expense", {"FY2025": -298173, "FY2024": -313697, "FY2023": -243245, "FY2022": -95917, "FY2021": -43321, "FY2020": -64873, "FY2019": -60746}),
    ("TOTAL", "Net interest income", {"FY2025": 148302, "FY2024": 123693, "FY2023": 111437, "FY2022": 102300, "FY2021": 93517, "FY2020": 114407, "FY2019": 110101}),
    ("DATA", "Fee and commission income", {"FY2025": 15678, "FY2024": 12118, "FY2023": 12651, "FY2022": 9211, "FY2021": 9764, "FY2020": 7287, "FY2019": 6261}),
    ("DATA", "Fee and commission expense", {"FY2025": -652, "FY2024": -931, "FY2023": -689, "FY2022": -119, "FY2021": -870, "FY2020": -535, "FY2019": -1558}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 15026, "FY2024": 11187, "FY2023": 11962, "FY2022": 9092, "FY2021": 8894, "FY2020": 6752, "FY2019": 4703}),
    ("DATA", "Operating lease rentals", {"FY2025": 173503, "FY2024": 141203, "FY2023": 105791, "FY2022": 71833, "FY2021": 50490, "FY2020": 43027}),
    ("DATA", "Revenue on sale of inventories", {"FY2025": 190376, "FY2024": 115479, "FY2023": 70967, "FY2022": 71702, "FY2021": 114906}),
    ("DATA", "Other profits/(losses) from sale of Operating Lease vehicles", {"FY2020": 3987}),
    ("DATA", "Other profits/(losses) from sale of HP & PCP vehicles", {"FY2020": 28761, "FY2019": -2670}),
    ("DATA", "Other revenue (operating lease rentals and sale of assets, as reported)", {"FY2019": 87716}),
    ("TOTAL", "Total income", {"FY2025": 527207, "FY2024": 391562, "FY2023": 300157, "FY2022": 254927, "FY2021": 267807, "FY2020": 164186, "FY2019": 202520}),
    ("SECTION", "Costs and provisions", {}),
    ("DATA", "Cost of sales", {"FY2025": -216829, "FY2024": -115943, "FY2023": -59187, "FY2022": -47242, "FY2021": -83972}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": -135111, "FY2024": -104189, "FY2023": -92713, "FY2022": -52443, "FY2021": -35811, "FY2020": -28245, "FY2019": -23686}),
    ("DATA", "Operating expenses", {"FY2025": -81285, "FY2024": -70151, "FY2023": -59749, "FY2022": -43281, "FY2021": -44355, "FY2020": -55162, "FY2019": -100395}),
    ("DATA", "Change in provision for liabilities", {"FY2025": -150000, "FY2024": -73644}),
    ("DATA", "Change in provision for residual value on HP & PCP vehicles", {"FY2025": -2268, "FY2024": 12209, "FY2023": 21368, "FY2022": -10579, "FY2021": -3305, "FY2020": -18291, "FY2019": 1457}),
    ("DATA", "Change in provision for expected credit losses on loans and advances to customers", {"FY2025": -17626, "FY2024": -1301, "FY2023": -9075, "FY2022": -11912, "FY2021": 15279, "FY2020": -23709, "FY2019": 2266}),
    ("DATA", "Change in provision for expected credit losses on investment securities", {"FY2025": 29, "FY2024": 16, "FY2023": 57, "FY2022": -37, "FY2021": -65, "FY2020": 151, "FY2019": -151}),
    ("DATA", "(Loss)/profit on derivatives - fair value adjustments", {"FY2025": -10609, "FY2024": -7561, "FY2023": -41989, "FY2022": 39713, "FY2021": 11969, "FY2020": -55, "FY2019": -3353}),
    ("DATA", "Profit on disposal of investment securities", {"FY2025": 2945, "FY2024": 6008, "FY2023": 4940, "FY2022": 2051}),
    ("DATA", "Income from equity method investments", {"FY2025": 638, "FY2024": 509, "FY2023": -178}),
    ("TOTAL", "Profit before tax", {"FY2025": -82909, "FY2024": 37515, "FY2023": 63631, "FY2022": 131197, "FY2021": 127547, "FY2020": 71623, "FY2019": 75988}),
    ("DATA", "Tax expense", {"FY2025": 19492, "FY2024": -10922, "FY2023": -13844, "FY2022": -22458, "FY2021": -20414, "FY2020": -10086, "FY2019": -14421}),
    ("TOTAL", "Profit after tax for the financial year", {"FY2025": -63417, "FY2024": 26593, "FY2023": 49787, "FY2022": 108739, "FY2021": 107133, "FY2020": 61537, "FY2019": 61567}),
    ("SECTION", "Attributable to: (of profit after tax - printed block, p.45)", {}),
    ("DATA", "(Loss)/Profit attributable to the owners of the parent company", {"FY2025": -62529}),
    ("DATA", "Non-controlling interests", {"FY2025": -888}),
    ("TOTAL", "(Loss)/Profit after tax for the financial year (attributable total - printed unlabelled)", {"FY2025": -63417}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income/(loss), net of tax", {"FY2025": -680, "FY2024": 737, "FY2023": -740, "FY2022": 3924, "FY2021": 4429, "FY2020": -1953, "FY2019": -3893}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2025": -64097, "FY2024": 27330, "FY2023": 49047, "FY2022": 112663, "FY2021": 111562, "FY2020": 59584, "FY2019": 57674}),
    ("SECTION", "Attributable to: (of total comprehensive income - printed block, p.46)", {}),
    ("DATA", "Total comprehensive (loss)/income attributable to the owners of the parent company", {"FY2025": -63209}),
    ("DATA", "Non-controlling interests ", {"FY2025": -888}),
    ("TOTAL", "Total comprehensive (loss)/income for the year (attributable total - printed unlabelled)", {"FY2025": -64097}),
]

bw.add_income_statement_sheet(
    title="RCI Bank UK Limited - Group Profit & Loss",
    subtitle="Consolidated Statement of Profit or Loss (and Other Comprehensive Income), Group column, £'000; FY2019-FY2025 (FY2019 is a 10-month Group period - see source note). See source note.",
    rows=PL_ROWS, sources_text=PL_SOURCES, first_col_width=68, source_height=210, unit_suffix=" (£'000)",
)

EQUITY_SOURCES = (
    "Sources - RCI Bank UK Limited Group consolidated statement of changes in equity, £'000 (Group column):\n"
    f"FY2025 (and the restatement bridge): {AR25_CITE}, printed p.49 (PDF p.49, zero folio offset), 'COMPANY "
    f"AND CONSOLIDATED STATEMENT OF CHANGES IN EQUITY', the GROUP table. That filing prints TWO separate "
    f"tables under the same heading - the Company table on printed p.48 and the Group table on printed p.49. "
    f"Only the Group table is used, consistent with the rest of this workbook. The restatement amounts are "
    f"corroborated at note 39, printed pp.139-140.\n"
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
    "plug.\n\n"
    "THE FY2024/FY2025 RESTATEMENT BRIDGE - BOTH POSITIONS CARRIED, NEITHER MOVED. This is the one place in "
    "the workbook where the two bases meet on the same sheet, so it is spelled out in full.\n"
    "  - 'Balance at 31 December 2024' = 290,400 / (3,584) / 436,990 / (337) / 723,469. This is the "
    "AS-PREVIOUSLY-REPORTED close, taken from the FY2024 edition's own Group statement of changes in equity "
    f"(printed p.45 of that report - {AR24_URL}). It is unchanged.\n"
    "  - 'Balance at 31 December 2024 and 1 January 2025 (as restated)' = 290,400 / (3,584) / 444,279 / (337) "
    "/ 730,758. This is the FY2025 EDITION's opening position, printed verbatim on p.49 of that report under "
    "the label 'Balance at 31 December 2024 and 1 January 2025(Restated)'.\n"
    "  - Between them sits the bank's own adjustment, +7,289 to retained earnings. That figure is printed at "
    "note 39 (p.140) as the cumulative impact of the Lease Hire depreciation prior-period error on retained "
    "earnings and total equity at 31 December 2024. It is NOT computed here.\n"
    "  - The bank itself prints its restatement row one year earlier, at 1 January 2024, as 'Prior year "
    "adjustment overstating depreciation' +4,204 (p.49). The two printed adjustments differ because +4,204 is "
    "the opening-balance effect and +7,289 the closing-balance effect, the difference being the +3,085 by "
    "which restated FY2024 profit (29,678) exceeds as-reported FY2024 profit (26,593). All four numbers are "
    "the bank's own; none is derived here. The bridge is placed at 31 December 2024 rather than at 1 January "
    "2024 because that is where this workbook's as-reported series ends and the FY2025 edition's series "
    "begins. The FY2019-FY2024 rows above are therefore untouched and remain on each year's own edition.\n\n"
    "A PRINTED ROW THAT IS NOT WHAT ITS LABEL SAYS, REPRODUCED NOT RECONCILED. The FY2025 row labelled "
    "'Total comprehensive income' on p.49 reads 45,000 / (680) / (62,529) / - / (18,209). It includes the "
    "45,000 share issue in its ordinary-share-capital column and in its total. A share issue is a transaction "
    "with the owners, not comprehensive income, and the same filing's own Consolidated Statement of Other "
    "Comprehensive Income (p.46) gives total comprehensive loss for 2025 as (64,097), being (680) of other "
    "comprehensive loss plus the (63,417) loss after tax. The two figures are both the bank's, printed three "
    "pages apart, and differ by exactly the 45,000 share issue plus the (888) non-controlling split. The row "
    "is reproduced here exactly as printed, with the label flagging it, and (64,097) is what the Profit & Loss "
    "sheet and the Overview carry. Neither figure has been moved towards the other. The Company table on p.48 "
    "does the same thing (45,000 / (1,300) / 34,393 / 78,093), so it is the bank's presentation, not a "
    "one-off slip.\n\n"
    "FY2025 ROLL-FORWARD, CHECKED AGAINST THE PRINTED FIGURES ONLY: 290,400+45,000 = 335,400; "
    "(3,584)+620+22-1,322 = (4,264); 444,279-62,529 = 381,750; (337)-888 = (1,225); 730,758-18,209-888 = "
    "711,661, and that closing total agrees with Total equity on the FY2025 balance sheet (p.47). No dividend "
    "row appears in 2025 - note 38 (p.139) states 'No dividends proposed for 2025 (2024: nil)'.\n\n"
    "DASH CONVENTION ON THIS SHEET. In the FY2025 Group table every cell that is not a figure is a printed "
    "DASH, not a blank - the bank populates all five columns on every row. This sheet's long-standing "
    "convention, applied to all seven years, renders those dashes as empty cells, so the convention is kept "
    "for FY2025 rather than split mid-sheet. Nothing is lost: a reader should take every empty cell in the "
    "FY2025 block as a printed dash, i.e. the bank saying nil.\n\n"
    "ONE PRINTED TYPOGRAPHICAL ODDITY, NOT REPRODUCED: the p.49 row for the FVOCI fair-value movement reads "
    "'Net change in in fair value of debt instrument at FVOCI' (the word 'in' is printed twice). The label is "
    "given here once, matching the identical 2024 row on the same table; the duplication is a typesetting "
    "artefact in the source, not a different line item."
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
    # --- THE RESTATEMENT BRIDGE (FY2025 edition, note 39 + the Group SOCIE on printed p.49). The row
    # above is the AS-PREVIOUSLY-REPORTED close and is deliberately left exactly as the FY2024 edition
    # published it. The FY2025 roll-forward opens from the RESTATED 730,758, so the two positions are
    # bridged by the bank's own printed adjustment rather than by moving either figure. See the source note.
    ("DATA", "Prior year adjustment overstating depreciation (cumulative restatement at 31 December 2024, note 39)", (None, None, 7289, None, 7289)),
    ("TOTAL", "Balance at 31 December 2024 and 1 January 2025 (as restated)", (290400, -3584, 444279, -337, 730758)),
    # --- FY2025 movements, reproduced in the printed order and wording of the Group table on p.49.
    ("DATA", "Loss for the year", (None, None, -62529, None, -62529)),
    ("DATA", "Issued Share Capital", (45000, None, None, None, 45000)),
    ("DATA", "Other comprehensive income", (None, 620, None, None, 620)),
    ("DATA", "Net changes in allowance for expected credit losses of debt instruments at FVOCI", (None, 22, None, None, 22)),
    ("DATA", "Net change in fair value of debt instrument at FVOCI", (None, -1322, None, None, -1322)),
    ("TOTAL", "Total comprehensive income (as printed - includes the 45,000 share issue; see source note)", (45000, -680, -62529, None, -18209)),
    ("DATA", "Loss attributable to minority interest", (None, None, None, -888, -888)),
    ("TOTAL", "Balance at 31 December 2025", (335400, -4264, 381750, -1225, 711661)),
]

bw.add_equity_changes_sheet(
    title="RCI Bank UK Limited - Group Statement of Changes in Equity",
    subtitle="Group column, £'000; chronological, 1 January 2019 - 31 December 2025. See source note.",
    headers=EQUITY_HEADERS, rows=EQUITY_ROWS, sources_text=EQUITY_SOURCES, first_col_width=52, source_height=200,
)

bw.add_cash_flow_sheet(
    title="RCI Bank UK Limited - Group Cash Flow Statement",
    subtitle="Group/consolidated basis, £'000; FY2019-FY2025 (FY2019 is a 10-month Group period - see source note). See source note.",
    rows=rows, sources_text=CASH_SOURCES, first_col_width=68, source_height=210, unit_suffix=" (£'000)",
)

AQ_SOURCES = (
    "Sources - RCI Bank UK Limited Group loans and advances to customers, £'000 (Group column, note 'Loans and "
    "advances to customers'):\n"
    f"FY2025: {AR25_CITE}, note 14 'Loans and advances to customers', printed pp.78-83 (PDF pp.78-83, zero "
    f"folio offset). Product split and residual value provision from printed p.78; IFRS 9 stage split from "
    f"printed p.80. The note opens (p.78): 'The Company does not have loans and advances to customers and "
    f"therefore there is no analysis to be disclosed. The following tables provide a summary of the Group "
    f"position as at 31 December 2025 together with additional analysis, and the 2024 comparatives' - so this "
    f"note is Group-only, which is the basis this sheet already uses.\n"
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
    "in FY2019 - see the Balance Sheet source note for where the GBP63,707k appears instead).\n\n"
    "FY2025 NOTES. (i) No Finance Lease line is printed in FY2025 (it was discontinued after FY2021), so that "
    "row stays blank, not zero. (ii) The loan book is NOT affected by the note 39 restatement - that error "
    "was in Lease Hire depreciation, which sits in property, plant and equipment. The FY2025 edition's 2024 "
    "comparatives in this note match this sheet EXACTLY: gross HP & PCP 4,166,131, Wholesale 1,102,294, total "
    "5,268,425, stages (11,318)/(4,547)/(19,576) totalling (35,441), residual value provision (62,306) and "
    "net 5,170,678. The 2025 ECL roll-forward's opening balance at 1 January 2025 is likewise (35,441). "
    "(iii) FY2025 foots exactly from printed figures with no plug: 4,178,081+1,371,448 = 5,549,529; the stage "
    "split (12,397)+(8,501)+(19,731) = (40,629), which equals the same page's product split of that allowance "
    "(HP & PCP (38,891) + Wholesale (1,738)); and 5,549,529-40,629-64,575 = 5,444,325, agreeing with Loans "
    "and advances to customers on the FY2025 balance sheet. (iv) A READING TRAP RECORDED: OCR of printed p.80 "
    "renders the Stage 3 loss allowance as (19,734). The figure is (19,731) - read off both a 300 dpi and a "
    "400 dpi rendering of the page, and the only value consistent with the printed total (40,629) and with "
    "the printed product split (19,497 + 234). The whole of this sheet's FY2025 column was taken from the "
    "page images, never from OCR text. (v) The derived ratio rows are this workbook's own, computed to the "
    "same precision as the earlier columns from printed inputs only: 40,629/5,549,529 = 0.73% and "
    "19,731/40,629 = 48.6%. Nothing on this sheet was back-solved."
)

AQ_ROWS = [
    ("SECTION", "Gross loans and advances to customers, by product", {}),
    ("DATA", "HP & PCP", {"FY2025": 4178081, "FY2024": 4166131, "FY2023": 4007471, "FY2022": 3513916, "FY2021": 3079780, "FY2020": 2910212, "FY2019": 2961330}),
    ("DATA", "Finance Lease", {"FY2021": 15291, "FY2020": 11799, "FY2019": 5994}),
    ("DATA", "Wholesale", {"FY2025": 1371448, "FY2024": 1102294, "FY2023": 1033829, "FY2022": 911100, "FY2021": 437250, "FY2020": 700687, "FY2019": 985887}),
    ("TOTAL", "Gross loans and advances to customers", {"FY2025": 5549529, "FY2024": 5268425, "FY2023": 5041300, "FY2022": 4425016, "FY2021": 3532321, "FY2020": 3622698, "FY2019": 3953211}),
    ("SECTION", "Expected credit loss (ECL) allowance, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": -12397, "FY2024": -11318, "FY2023": -15813, "FY2022": -19177, "FY2021": -10376, "FY2020": -19264, "FY2019": -11621}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": -8501, "FY2024": -4547, "FY2023": -7921, "FY2022": -4898, "FY2021": -3893, "FY2020": -14889, "FY2019": -8671}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": -19731, "FY2024": -19576, "FY2023": -17738, "FY2022": -14827, "FY2021": -18121, "FY2020": -19310, "FY2019": -16843}),
    ("TOTAL", "Total ECL allowance", {"FY2025": -40629, "FY2024": -35441, "FY2023": -41472, "FY2022": -38902, "FY2021": -32390, "FY2020": -53463, "FY2019": -37135}),
    ("DATA", "Residual value provision for HP & PCP", {"FY2025": -64575, "FY2024": -62306, "FY2023": -74516, "FY2022": -95883, "FY2021": -85304, "FY2020": -81999}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 5444325, "FY2024": 5170678, "FY2023": 4925312, "FY2022": 4290231, "FY2021": 3414627, "FY2020": 3487236, "FY2019": 3916076}),
    ("SECTION", "Derived asset-quality ratios", {}),
    ("DATA", "ECL coverage ratio (Total ECL allowance / Gross loans)", {"FY2025": "0.73%", "FY2024": "0.67%", "FY2023": "0.82%", "FY2022": "0.88%", "FY2021": "0.92%", "FY2020": "1.48%", "FY2019": "0.94%"}),
    ("DATA", "Stage 3 ECL allowance as % of total ECL allowance", {"FY2025": "48.6%", "FY2024": "55.2%", "FY2023": "42.8%", "FY2022": "38.1%", "FY2021": "55.9%", "FY2020": "36.1%", "FY2019": "45.4%"}),
]

bw.add_asset_quality_sheet(
    title="RCI Bank UK Limited - Group Asset Quality",
    subtitle="Loans and advances to customers, Group column, £'000; FY2019-FY2025 (FY2019 is a 10-month Group period - see source note). See source note.",
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
    f"FY2025 (ANNUAL-REPORT BASIS ONLY - there is no FY2025 Pillar 3 disclosure): {AR25_CITE}. Capital RATIOS "
    f"from the Strategic Report's 'Capital and Liquidity' section, printed p.8; absolute regulatory CAPITAL "
    f"amounts from note 33 'Risk and risk management - Equity Capital Management and Regulatory Capital', "
    f"printed p.126, Group 2025 column. See the FY2025 BASIS NOTE below before comparing any FY2025 cell with "
    f"FY2024 or FY2023.\n"
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
    "FY2025 BASIS NOTE - AN ANNUAL-REPORT YEAR IN A PILLAR 3 SERIES, AND THE BREAKS THAT COME WITH IT.\n"
    "RCI Bank UK had published no FY2025 Pillar 3 disclosure when this workbook was built, so every FY2025 "
    "figure on these sheets comes from the statutory accounts instead. That is a DIFFERENT BASIS from the "
    "FY2024 and FY2023 cells, which are UK KM1. The two are not interchangeable and have not been blended.\n"
    "  (a) CAPITAL AMOUNTS. Note 33 (printed p.126) gives Group 2025 CET1 and Tier 1 capital of GBP678,502k "
    "and total capital of GBP814,731k (subordinated loans 129,000 + credit risk adjustment 7,229 = Tier 2 "
    "136,229). Those sit on their OWN labelled rows on the capital-amount sheets, not appended to the KM1 "
    "row, because the annual-report table is struck on the restated accounts AND includes a proportional "
    "consolidation of SVGH that the KM1 did not: the note itself says 'The Retained earnings differs to the "
    "balance sheet due to the minority shareholding in SVGH acquired in 2024. UK Prudential Regulation "
    "Authority (PRA) required RCI Bank UK Group to proportionally consolidate SVGH for prudential regulatory "
    "capital calculation purpose.' How large that basis gap is can be measured on the bank's own 2024 "
    "figures: the SAME note 33 table prints 2024 CET1/Tier 1 as 714,538 and total capital as 817,377, where "
    "the FY2024 KM1 printed GBP707m and GBP809m. Both are the bank's own; neither has been moved towards the "
    "other, and the 2024 cells on these sheets remain the KM1 figures. Note also that note 33's accumulated "
    "other comprehensive income of (4,885) differs from the balance sheet's Other reserves of (4,264) - a "
    "regulatory adjustment, as printed.\n"
    "  (b) CAPITAL RATIOS. Printed p.8: 'As at 31 December 2025, the Common Equity Tier 1 (CET1) ratio was "
    "11.84% (2024:13.46%). The total capital ratio was 14.22% (2024:15.42%), including GBP129m subordinated "
    "debt.' Here the annual report and the KM1 AGREE for 2024 (13.46% and 15.42% are exactly the KM1 "
    "figures), so the FY2025 ratios continue the series on a consistent footing and are placed on the main "
    "row, the same treatment FY2022-FY2019 already get.\n"
    "  (c) NO TIER 1 RATIO IS PRINTED FOR FY2025, SO THE CELL IS BLANK. Note 33 shows CET1 capital and Tier 1 "
    "capital as a single identical line ('CET1 and Tier 1 Capital' 678,502), so Tier 1 almost certainly "
    "equals CET1 again - but the bank prints no Tier 1 RATIO anywhere in the FY2025 accounts, and writing "
    "11.84% into that cell would be an inference, not a disclosure. It is left empty.\n"
    "  (d) NO RWA, NO LEVERAGE RATIO, NO MREL EXISTS FOR FY2025. The FY2025 accounts define both ratios as "
    "capital divided by Total Risk Weighted Exposures but never print the denominator, and contain no "
    "leverage-ratio, total-exposure-measure, MREL or eligible-liabilities figure of any kind. Those FY2025 "
    "cells are therefore EMPTY and are a real, chaseable gap at the newest end, not a sourced negative: on "
    "this bank's own past cadence the FY2025 Pillar 3 should appear around December 2026. GBP678,502k "
    "divided by 11.84% would produce an RWA-shaped number and is NOT used - a back-solved figure is not a "
    "disclosure.\n"
    "  (e) A TRAP IN THIS DOCUMENT, EXPLICITLY REJECTED. The only occurrences of the word 'Pillar' in the "
    "whole 140-page FY2025 filing are in note 10 (tax, printed p.74) and refer to the OECD's 'Pillar Two' "
    "global minimum tax - 'The UK has enacted legislation implementing the OECD Pillar Two model rules', "
    "'Renault UK Ltd has registered with HMRC for Pillar Two'. That is international tax law and has nothing "
    "whatever to do with Basel Pillar 2 or Pillar 3. It must never be mined for capital data.\n\n"
    + P3_NONEXISTENCE_NOTE
)

SUFFIX = (
    " FY2022-FY2020 ARE A PERMANENT SOURCED NEGATIVE, not an open gap: RCI Bank UK's FY2023 Pillar 3 states it is the 'first iteration of the document' and the FY2024 edition states it is the 'second iteration', so no Pillar 3 disclosure was ever produced for any year before FY2023 - see the sourced-negative section of the source note below. Do not re-chase these cells."
)

AR_BASIS = (
    " FY2025 IS ON A DIFFERENT BASIS AND IS ON ITS OWN ROW: no FY2025 Pillar 3 disclosure exists, so the FY2025 figure is the annual report's note 33 (printed p.126, Group 2025 column), which is struck on the restated accounts and includes the PRA-required proportional consolidation of SVGH. The size of that basis gap is visible in the bank's own 2024 figures: note 33 prints 2024 CET1/Tier 1 as 714,538 and total capital as 817,377, against the FY2024 KM1's GBP707m and GBP809m. The KM1 row is NOT continued into FY2025 and the FY2024/FY2023 cells are unchanged. See the FY2025 BASIS NOTE in the source note below."
)

def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, P3_SOURCES, note=note, first_col_width=52, source_height=170)


KM1_SOURCES = (
    "Sources - RCI Bank UK Limited / Mobilize Financial Services UK, 'Table 2: UK KM1 - Key metrics template', "
    "as published in the entity's own Pillar III Disclosures. The bank prints this table in £'million, and this "
    "sheet keeps that unit - the rest of the workbook is in £'000, so the two are the same figures on different "
    "scales, not different figures:\n"
    f"FY2024: Pillar III Disclosures FY2024, printed p.24 (two columns, 31st December 2024 and 31st December "
    f"2023) - {P3_24_URL}\n"
    f"FY2023: Pillar III Disclosures FY2023, printed p.22 (a SINGLE column, 31st December 2023) - {P3_23_URL}\n"
    "The FY2023 column here is taken from the FY2023 edition, its own year's edition. The FY2024 edition's "
    "31st December 2023 comparative reproduces it value for value - CET1 669, Tier 1 669, total capital 774, "
    "RWAs 4,842, ratios 13.81/13.81/15.99, UK 7a 1.86, UK 7c 0.46, UK 7d 9.86, buffers 2.5/2.0/4.5, UK 11a 14.36, "
    "row 12 3.95, leverage 6,148 and 10.9%, LCR 1,035/718/251/467/236%, NSFR 5,622/4,312/130% - an independent "
    "confirmation of the whole column at no extra sourcing cost.\n\n"
    "FY2022, FY2021, FY2020 AND FY2019 ARE BLANK, AND BLANK MEANS NEVER PUBLISHED IN THIS TEMPLATE, ON ANY BASIS, "
    "IN ANY EDITION. Two things have to hold for that, and both do. (i) No earlier Pillar 3 disclosure exists: the "
    "FY2023 edition describes itself as the 'first iteration of the document' and the FY2024 edition as the "
    "'second iteration', and a Wayback CDX sweep of the whole rcibank.co.uk domain returns only those two Pillar 3 "
    "documents. (ii) No LATER edition prints a comparative reaching those years: the FY2023 edition's KM1 has one "
    "column only, and the FY2024 edition's has two, the earlier of which is 31st December 2023. So there is no "
    "comparative column anywhere to fill FY2022 or earlier from. The capital ratios those years' ANNUAL REPORTS "
    "disclose are on the single-metric sheets; they are a different disclosure, not this template, and are not "
    "mapped onto template row numbers here.\n\n"
    "Row UK 7b (Additional AT1 SREP requirements) is not printed in either edition and so does not appear on this "
    "sheet. Rows 1 and 2 are identical in both years, as are rows 5 and 6, which is consistent with the bank "
    "holding no AT1 capital.\n\n"
    "LATEST-EDITION CHECK 2026-09-17: the bank's own publications index at "
    f"{FACTS_URL} was read directly. It lists exactly two Pillar III disclosures, FY2023 and FY2024 (the FY2024 "
    "file sits under a 2025-12 upload path), and no FY2025 edition has been published. The FY2024 edition is "
    "therefore the newest, and this workbook already runs to FY2024.\n\n"
    "LATEST-EDITION RE-CHECK 2026-09-18, ON BOTH AXES, because an FY2024 baseline is the kind that goes stale "
    "silently. (i) Pillar 3: the publications index above was re-read in full and still links exactly two Pillar "
    "III disclosures. Beware the caption - the newer link reads '2024/2025', which is the bank's publication-year "
    "styling and NOT an FY2025 report: the file is named FY 2024 and its KM1 columns are 31st December 2024 and "
    "31st December 2023. (ii) Statutory accounts: Companies House for company 11429127 shows the newest accounts "
    "filing to be 'Group of companies' accounts made up to 31 December 2024', filed 07 October 2025, and the "
    "company profile states 'Next accounts made up to 31 December 2025 due by 30 September 2026'. So no FY2025 "
    "document of either kind exists yet and the FY2025 accounts are not yet overdue. FY2024 is this bank's "
    "genuine latest edition, not a stale baseline. On the bank's own past cadence (FY2024 accounts filed October "
    "2025, FY2024 Pillar 3 uploaded December 2025) the FY2025 pair should appear around October and December "
    "2026.\n\n"
    "LATEST-EDITION RE-CHECK 2026-09-19 (GA-020) - STILL NONE. (i) Companies House filing history for 11429127, "
    "read UNFILTERED on page 1: newest rows SH01 (2 Jul 2026), CS01 (26 Jun 2026), TM01 (27 May 2026); the newest "
    "AA is still the FY2024 group accounts filed 07 Oct 2025, and the profile still reads 'due by 30 September "
    "2026'. (ii) The facts-and-figures index (HTTP 200) still links exactly two Pillar III disclosures, FY2023 "
    "and FY2024; direct probes of 'Pillar III Disclosures FY 2025 - External.pdf' under the 2026-06 to 2026-09 "
    "upload paths all return a genuine 404, against a 200/application/pdf/%PDF control on the FY2024 file. "
    "(iii) Wayback CDX for rcibank.co.uk from 2026 onward: 57 PDF captures, the only Pillar III among them the "
    "FY2024 edition. Look again after 30 September 2026 (accounts) and around December 2026 (Pillar III).\n\n"
    "A TRAP ON THAT SAME INDEX PAGE, EXPLICITLY REJECTED: its headline statistics ('Basel III Core Tier 1 "
    "solvency ratio 16.05%', 'All figures correct at year end 2025') are RCI Banque / Mobilize Financial Services "
    "GROUP figures for the French parent, not RCI Bank UK Limited. They look exactly like the FY2025 data this "
    "workbook lacks and must never be used to fill it.\n\n"
    "WHY ROWS 1 AND 2 ARE EQUAL WHILE ROW 3 BREAKS HIGHER - CONFIRMED FROM THE SAME DOCUMENT 2026-09-18 so it "
    "need not be re-opened. The FY2024 edition's own UK CC1 table prints row 45 'Tier 1 capital (T1 = CET1 + "
    "AT1)' with no AT1 instrument row above it, so the bank has no Additional Tier 1 in issue and CET1 equals "
    "Tier 1 exactly. Total capital breaks higher because of Tier 2: CC1 row 46 gives Tier 2 capital instruments "
    "of GBP100m (the subordinated debt), row 50 adds GBP3m of credit risk adjustments, row 58 totals Tier 2 at "
    "GBP103m and row 59 gives total capital of GBP809m. The entire KM1 block above was re-read against the "
    "printed table the same day and agrees digit for digit, row set included.\n\n"
    "A ROUNDING DIFFERENCE BETWEEN THE BANK'S OWN TWO TABLES, RECORDED NOT RECONCILED: the FY2024 CC1 prints CET1 "
    "capital (row 29) and Tier 1 capital (row 45) as GBP706m, while KM1 rows 1 and 2 print GBP707m for the same "
    "date and the same entity. Both are as published; neither has been moved towards the other.\n\n"
    "YEARS NOT SHOWN AS COLUMNS ON THIS SHEET (2026-09-18). FY2022, FY2021, FY2020 and FY2019 previously carried "
    "empty columns under printed year headers and are now omitted from this sheet entirely. Nothing is lost by "
    "it: the bank published no Pillar 3 for those years and no later edition prints a comparative reaching them, "
    "as the sourced-negative section above establishes. Those years remain in full on every other sheet in this "
    "workbook, and the capital RATIOS they do disclose are on the single-metric sheets.\n\n"
    "LATEST-EDITION RE-CHECK 2026-10-08 - THE STATUTORY AXIS HAS MOVED, THE PILLAR 3 AXIS HAS NOT, SO THE "
    "FY2025 COLUMN ON THIS SHEET IS DELIBERATELY EMPTY. RCI Bank UK filed its FY2025 Annual Report and Financial "
    "Statements at Companies House on 29 September 2026 (A08 barcode AFBMZRSA, #114), and that filing has "
    "been transcribed into every other sheet of this workbook. It contains NO UK KM1 template, and no Pillar "
    "3 disclosure of any kind: all 140 pages were swept and there is no KM1, no UK OV1, no CC1, no RWA "
    "amount, no leverage ratio, no total exposure measure and no MREL figure. A KM1 sheet may be filled ONLY "
    "from the bank's own published KM1 template, so the capital ratios and amounts the FY2025 accounts DO "
    "disclose (CET1 11.84%, total capital 14.22%, LCR 185%, NSFR 130% on printed p.8; CET1/Tier 1 capital "
    "678,502 and total capital 814,731 at note 33, printed p.126) are on the single-metric sheets with their "
    "basis stated, and are NOT mapped onto template row numbers here. The empty FY2025 column is KEPT rather "
    "than trimmed, and that is the point: an empty column at the NEWEST end is a real, chaseable gap and must "
    "stay visible, whereas the FY2022-FY2019 columns described above are trimmed because no edition will "
    "ever fill them. On the bank's own cadence the FY2025 Pillar III should appear around December 2026, and "
    "this column is where it goes.\n\n"
    "A TRAP IN THE FY2025 ACCOUNTS, EXPLICITLY REJECTED: the only occurrences of 'Pillar' in that document "
    "are in note 10 (tax, printed p.74) and refer to the OECD's 'Pillar Two' global minimum tax. That is "
    "international tax law, not Basel Pillar 2 or Pillar 3, and must never be mined for capital data.\n\n" + ENTITY_NOTE
)

# RCI Bank UK has published exactly two Pillar 3 disclosures, FY2023 and FY2024,
# and neither carries a comparative reaching further back, so FY2022-FY2019 would
# otherwise be four year headers over four empty columns. Those trailing empty
# columns are dropped by the shared library from the row data itself, deliberately
# NOT by a hardcoded year list here: a hardcoded list silently swallows a new
# column the day someone adds a year to the rows below and forgets to widen it.
bw.add_km1_sheet(
    title="RCI Bank UK Limited — KM1 Key Metrics",
    subtitle="UK KM1 - Key metrics template, as published in RCI Bank UK Limited / Mobilize Financial Services UK "
             "Pillar III Disclosures. Reproduced in the bank's own row order, row numbering, labels and precision, "
             "and in the bank's own unit of £'million. FY2023 and FY2024 are each that year's own edition; no "
             "Pillar 3 disclosure exists for FY2022 or earlier and no later edition carries a comparative for "
             "those years, so FY2022-FY2019 carry no column on this sheet - see the source note.",
    rows=[
        ("SECTION", "Available own funds (amounts)", {}),
        ("DATA", "1 Common Equity Tier 1 (CET1) capital (£'million)", {"FY2024": 707, "FY2023": 669}),
        ("DATA", "2 Tier 1 capital (£'million)", {"FY2024": 707, "FY2023": 669}),
        ("DATA", "3 Total capital (£'million)", {"FY2024": 809, "FY2023": 774}),
        ("SECTION", "Risk-weighted exposure (amounts)", {}),
        ("DATA", "4 Total risk-weighted exposure amount (£'million)", {"FY2024": 5247, "FY2023": 4842}),
        ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "5 Common Equity Tier 1 ratio (%)", {"FY2024": "13.46%", "FY2023": "13.81%"}),
        ("DATA", "6 Tier 1 ratio (%)", {"FY2024": "13.46%", "FY2023": "13.81%"}),
        ("DATA", "7 Total capital ratio (%)", {"FY2024": "15.42%", "FY2023": "15.99%"}),
        ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "UK 7a Additional CET1 SREP requirements (%)", {"FY2024": "1.84%", "FY2023": "1.86%"}),
        ("DATA", "UK 7c Additional T2 SREP requirements (%)", {"FY2024": "0.46%", "FY2023": "0.46%"}),
        ("DATA", "UK 7d Total SREP own funds requirements (%)", {"FY2024": "9.84%", "FY2023": "9.86%"}),
        ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "8 Capital conservation buffer (%)", {"FY2024": "2.5%", "FY2023": "2.5%"}),
        ("DATA", "9 Institution specific countercyclical capital buffer (%)", {"FY2024": "2.0%", "FY2023": "2.0%"}),
        ("DATA", "11 Combined buffer requirement (%)", {"FY2024": "4.5%", "FY2023": "4.5%"}),
        ("DATA", "UK 11a Overall capital requirements (%)", {"FY2024": "14.34%", "FY2023": "14.36%"}),
        ("DATA", "12 CET1 available after meeting the total SREP own funds requirements (%)", {"FY2024": "3.62%", "FY2023": "3.95%"}),
        ("SECTION", "Leverage ratio", {}),
        ("DATA", "13 Total exposure measure excluding claims on central banks (£'million)", {"FY2024": 6642, "FY2023": 6148}),
        ("DATA", "14 Leverage ratio excluding claims on central banks (%)", {"FY2024": "10.6%", "FY2023": "10.9%"}),
        ("SECTION", "Liquidity Coverage Ratio", {}),
        ("DATA", "15 Total high-quality liquid assets (HQLA) (Weighted value -average) (£'million)", {"FY2024": 899, "FY2023": 1035}),
        ("DATA", "UK 16a Cash outflows - Total weighted value (£'million)", {"FY2024": 659, "FY2023": 718}),
        ("DATA", "UK 16b Cash inflows - Total weighted value (£'million)", {"FY2024": 293, "FY2023": 251}),
        ("DATA", "16 Total net cash outflows (adjusted value) (£'million)", {"FY2024": 365, "FY2023": 467}),
        ("DATA", "17 Liquidity coverage ratio (%)", {"FY2024": "287%", "FY2023": "236%"}),
        ("SECTION", "Net Stable Funding Ratio", {}),
        ("DATA", "18 Total available stable funding (£'million)", {"FY2024": 6115, "FY2023": 5622}),
        ("DATA", "19 Total required stable funding (£'million)", {"FY2024": 4863, "FY2023": 4312}),
        ("DATA", "20 NSFR ratio (%)", {"FY2024": "126%", "FY2023": "130%"}),
    ],
    sources_text=KM1_SOURCES,
    first_col_width=76,
    source_height=380,
)

metric("CET1 Capital", "£'000, Group basis - two reporting bases, see note",
       [("Common Equity Tier 1 (CET1) capital (Pillar 3 UK KM1 basis)", {"FY2024": 707000, "FY2023": 669000}),
        ("Common Equity Tier 1 (CET1) capital (annual report note 33 basis)", {"FY2025": 678502})],
       "Absolute CET1 capital is disclosed in the UK KM1 table only for FY2024-FY2023; the FY2022-FY2019 annual reports disclose ratios but not the absolute capital amount."+AR_BASIS+SUFFIX)
# CET1 ratio, Pillar 3 UK KM1 basis where a KM1 exists (FY2024/FY2023), annual report
# thereafter. FY2024 CORRECTED 2026-09-15 from 13.69% to 13.46%: see CET1_RATIO_NOTE.
CET1_RATIO = {"FY2025": "11.84%", "FY2024": "13.46%", "FY2023": "13.81%", "FY2022": "13.98%", "FY2021": "15.16%", "FY2020": "15.94%", "FY2019": "14.59%"}
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
metric("Tier 1 Capital", "£'000, Group basis - two reporting bases, see note",
       [("Tier 1 capital (Pillar 3 UK KM1 basis)", {"FY2024": 707000, "FY2023": 669000}),
        ("Tier 1 capital (annual report note 33 basis)", {"FY2025": 678502})],
       "Absolute Tier 1 capital is disclosed in the UK KM1 table only for FY2024-FY2023; the FY2022-FY2019 annual reports do not disclose the amount. The FY2025 note 33 table prints CET1 and Tier 1 capital as a SINGLE combined line ('CET1 and Tier 1 Capital' 678,502), i.e. the bank again holds no Additional Tier 1."+AR_BASIS+SUFFIX)
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2024": "13.46%", "FY2023": "13.81%", "FY2022": "13.98%", "FY2021": "15.16%", "FY2020": "15.94%", "FY2019": "14.59%"})], "FY2024 and FY2023 are from the dedicated UK KM1 disclosure (rows 6 and 5 give an identical Tier 1 and CET1 ratio in both years, and rows 1 and 2 give identical CET1 and Tier 1 capital amounts, so AT1 is nil). The FY2024 annual-report narrative instead gives CET1 13.69% and total capital 15.66%, a different reporting basis/rounding vintage; the KM1 value is used here AND on the CET1 Ratio sheet as of the 2026-09-15 correction, so the two sheets are now mutually consistent - see the CET1 Ratio sheet's note for the full explanation and for the superseded annual-report value, which is preserved there on its own row. FY2022-FY2019 assume Tier 1 = CET1 (no AT1 capital is mentioned in any of these annual reports, and no Pillar 3 disclosure exists for those years - see the source note's sourced-negative section). FY2025 IS DELIBERATELY BLANK AND IS A REAL GAP, NOT A SOURCED NEGATIVE. No FY2025 Pillar 3 exists yet, and the FY2025 annual report prints a CET1 ratio (11.84%) and a total capital ratio (14.22%) on p.8 but NO Tier 1 ratio. Its note 33 (p.126) does show CET1 and Tier 1 capital as one identical line (678,502), so Tier 1 very probably equals CET1 again - but that is an inference, not a printed figure, so the cell is left empty rather than filled with 11.84%. Expect the FY2025 Pillar 3, and with it a Tier 1 ratio, around December 2026 on this bank's past cadence.")
metric("Total Capital", "£'000, Group basis - two reporting bases, see note",
       [("Total capital (Pillar 3 UK KM1 basis)", {"FY2024": 809000, "FY2023": 774000}),
        ("Total capital (annual report note 33 basis)", {"FY2025": 814731})],
       "Absolute total capital is disclosed in the UK KM1 table only for FY2024-FY2023; the FY2022-FY2019 annual reports do not disclose the amount. FY2025 total capital of 814,731 is CET1/Tier 1 of 678,502 plus Tier 2 of 136,229, itself subordinated loans of 129,000 plus a credit risk adjustment of 7,229 - all four printed at note 33 (p.126)."+AR_BASIS+SUFFIX)
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "14.22%", "FY2024": "15.42%", "FY2023": "15.99%", "FY2022": "16.34%", "FY2021": "16.31%", "FY2020": "17.16%", "FY2019": "15.71%"})])
metric("Total RWAs", "£'000, UK KM1 / Group basis", [("Total risk-weighted exposure amount", {"FY2024": 5247000, "FY2023": 4842000, "FY2022": 4246000})], "FY2024-FY2023 are from the UK KM1 table. FY2022 is the comparative column of the FY2023 disclosure's UK OV1 table (printed p.21, row 29 'Total' = GBP4,246m), cross-checked against the same report's introduction page, which prints 'Risk Weighted Assets (RWA) ... (2022: GBP4,246m)'. The FY2021-FY2019 annual reports disclose capital ratios but not RWA amounts, and no Pillar 3 disclosure exists for those years - see the RWA Breakdown source note. FY2025 IS BLANK AND IS A REAL, CHASEABLE GAP AT THE NEWEST END. The FY2025 statutory accounts were filed on 29 September 2026 and were read in full for this build; they define both capital ratios as capital divided by Total Risk Weighted Exposures but never print the denominator, and no FY2025 Pillar 3 disclosure had been published. Dividing the note 33 CET1 capital of GBP678,502k by the p.8 CET1 ratio of 11.84% would yield an RWA-shaped number; that would be a back-solve, not a disclosure, and has NOT been done. Look again around December 2026.")

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
    "exactly to the Total RWAs metric sheet.\n\n"
    "FY2025: AN EMPTY COLUMN, DELIBERATELY KEPT - A REAL GAP AT THE NEWEST END, NOT A SOURCED NEGATIVE (2026-10-08). The "
    "FY2025 statutory accounts were filed on 29 September 2026 and have been transcribed into the rest of "
    "this workbook, but they contain no UK OV1 table and no RWA amount at all - they define the capital "
    "ratios as capital over Total Risk Weighted Exposures without ever printing the denominator. No FY2025 "
    "Pillar 3 disclosure had been published when this workbook was built. The FY2025 category-level "
    "breakdown therefore does not yet exist to be transcribed, and should be chased again around December "
    "2026, which is when the FY2024 edition appeared. Nothing here is back-solved from a ratio."
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

metric("Leverage Ratio", "£'000 / %", [("Total exposure measure excluding claims on central banks", {"FY2024": 6642000, "FY2023": 6148000}), ("Leverage ratio excluding claims on central banks (%)", {"FY2024": "10.6%", "FY2023": "10.9%", "FY2022": "11.10%"})], "FY2024-FY2023 are from the dedicated UK KM1 disclosure. FY2022 is disclosed as a prior-year comparative on the introduction page of the FY2023 Pillar 3 report ('UK Leverage Ratio 10.9% (2022: 11.10%)'); the FY2023 report gives no FY2022 total exposure measure, so that row is left blank for FY2022 rather than back-solved. The FY2021-FY2019 annual reports disclose no leverage ratio in any form, and no Pillar 3 disclosure exists for those years. FY2025 IS BLANK AND IS A REAL, CHASEABLE GAP AT THE NEWEST END: the FY2025 statutory accounts (filed 29 September 2026) were read in full and contain no leverage ratio, no total exposure measure and no UK leverage disclosure of any kind, and no FY2025 Pillar 3 had been published. Look again around December 2026.")
metric("LCR", "£'000 / %", [("Total high-quality liquid assets (HQLA), weighted value - average", {"FY2024": 899000, "FY2023": 1035000}), ("Total net cash outflows (adjusted value)", {"FY2024": 365000, "FY2023": 467000}), ("Liquidity Coverage Ratio (%)", {"FY2025": "185%", "FY2024": "287%", "FY2023": "236%", "FY2022": "354%", "FY2021": "158%", "FY2020": "551%", "FY2019": "221%"})], "FY2024-FY2023 amounts and ratios are UK KM1. The FY2022-FY2019 headline ratios are from the statutory annual-report Capital and Liquidity sections. BASIS NOTE: the FY2023 Pillar 3 report's introduction page prints the FY2022 LCR as 352%, two points below the 354% the FY2022 annual report states. The annual-report value is retained here for continuity with FY2021-FY2019, which have no Pillar 3 equivalent at all. The gap is rounding/restatement scale rather than a basis break (contrast the KM1 12-month-average vs point-in-time divergences seen at other banks, which run to tens or hundreds of points), so the series is not split into two rows. FY2025 (185%) IS THE ANNUAL-REPORT BASIS, like FY2022-FY2019: no FY2025 Pillar 3 exists, so there is no KM1 12-month-average figure for that year, and the FY2025 HQLA and net-cash-outflow amount cells are left blank rather than estimated. A GENUINE BASIS BREAK TO BE AWARE OF WHEN READING THE SERIES, RECORDED NOT RECONCILED: the FY2025 annual report (printed p.8) gives the 2024 LCR as 369%, where the FY2024 KM1 - and this sheet's FY2024 cell - gives 287%. That is a 82-point gap and is the classic KM1-vs-annual-report divergence: KM1 row 17 is a 12-month average of weighted values while the annual-report narrative is a point-in-time figure at 31 December. Both are the bank's own. The FY2024 cell keeps the KM1 figure (it is a Pillar 3 metric sheet), the FY2025 cell is necessarily annual-report basis, and neither has been moved towards the other.")
metric("NSFR", "£'000 / %", [("Total available stable funding", {"FY2024": 6115000, "FY2023": 5622000}), ("Total required stable funding", {"FY2024": 4863000, "FY2023": 4312000}), ("NSFR ratio (%)", {"FY2025": "130%", "FY2024": "126%", "FY2023": "130%", "FY2022": "138%", "FY2021": "109%", "FY2020": "138%", "FY2019": "122%"})], "FY2024-FY2023 amounts and ratios are UK KM1. The FY2022-FY2019 headline ratios are from the statutory annual-report Capital and Liquidity sections. FY2025 (130%) IS THE ANNUAL-REPORT BASIS, like FY2022-FY2019: no FY2025 Pillar 3 exists, so the FY2025 available- and required-stable-funding amount cells are left blank rather than estimated. A SMALLER BASIS BREAK, RECORDED NOT RECONCILED: the FY2025 annual report (printed p.8) gives the 2024 NSFR as 127.4%, where the FY2024 KM1 - and this sheet's FY2024 cell - gives 126%. Both are the bank's own; the FY2024 cell keeps the KM1 figure and neither has been moved. Note also that 130% is both the FY2025 annual-report figure and, coincidentally, the FY2023 KM1 figure already on this sheet; they are not related.")
_RCI_MREL = {
    "FY2025": "Not published - FY2025 annual report (Companies House, filed 29/09/2026) read in full off the page images 2026-10-08: no MREL, eligible-liabilities or KM2 figure anywhere in its 140 pages; no FY2025 Pillar 3 had been published",
    **{y: f"Not published – {y} Pillar 3 and {y} annual report (Companies House) read 2026-09-19: no MREL, eligible-liabilities or KM2 figure" for y in ["FY2024", "FY2023"]},
    **{y: f"Not published – {y} annual report (Companies House, OCR) has no MREL figure; no {y} Pillar 3 exists (Wayback CDX of rcibank.co.uk holds only FY2023/FY2024 editions)" for y in ["FY2022", "FY2021", "FY2020", "FY2019"]},
}
metric("MREL Ratio", None, [("MREL ratio", {y: _RCI_MREL.get(y, "Not publicly disclosed") for y in YEARS})], "No quantitative MREL ratio was found in the RCI Bank UK annual reports, the RCI Bank UK Pillar 3 disclosures reviewed, or the official facts-and-figures page. GA-020 (2026-09-19): FY2019-FY2024 annual reports (Companies House scans, OCR) and the FY2023/FY2024 Pillar 3 reports were re-read, with 0 MREL, eligible-liabilities or KM2 hits against 22-72 'capital' hits per document. A full Wayback CDX crawl of rcibank.co.uk (6,188 URLs) shows no Pillar 3 edition before FY2023. FY2025 (2026-10-08): the FY2025 statutory accounts, filed at Companies House on 29 September 2026, were read in full from 300 dpi page images for this build - the filing is a pure scan with no text layer. They contain no MREL, eligible-liabilities, KM2 or resolution-capital figure. The only occurrences of the word 'Pillar' in the whole document are in note 10 (tax, p.74) and refer to the OECD's Pillar Two global minimum tax, which is unrelated to Basel Pillar 3 and is explicitly rejected as a source here.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 7385045, "FY2024": 7299251, "FY2023": 6932488, "FY2022": 6297529, "FY2021": 4995682, "FY2020": 4922345, "FY2019": 5014222}),
        ("Loans and advances to customers", {"FY2025": 5444325, "FY2024": 5170678, "FY2023": 4925312, "FY2022": 4290231, "FY2021": 3414627, "FY2020": 3487236, "FY2019": 3916076}),
        ("Deposits from customers", {"FY2025": 5267541, "FY2024": 4978566, "FY2023": 4794623, "FY2022": 4140482, "FY2021": 2929460, "FY2020": 3149310, "FY2019": 2953593}),
        ("Total equity", {"FY2025": 711661, "FY2024": 723469, "FY2023": 696139, "FY2022": 646867, "FY2021": 641337, "FY2020": 616637, "FY2019": 608453}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {"FY2025": 527207, "FY2024": 391562, "FY2023": 300157, "FY2022": 254927, "FY2021": 267807, "FY2020": 164186, "FY2019": 202520}),
        ("Total operating expense (cost of sales + operating costs)", {"FY2025": -298114, "FY2024": -290283, "FY2023": -211649, "FY2022": -142966, "FY2021": -164138, "FY2020": -83407, "FY2019": -124081}),
        ("Profit after tax for the financial year", {"FY2025": -63417, "FY2024": 26593, "FY2023": 49787, "FY2022": 108739, "FY2021": 107133, "FY2020": 61537, "FY2019": 61567}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Total comprehensive income for the year", {"FY2025": -64097, "FY2024": 27330, "FY2023": 49047, "FY2022": 112663, "FY2021": 111562, "FY2020": 59584, "FY2019": 57674}),
        ("Dividend paid", {"FY2022": -107133, "FY2021": -86862, "FY2020": -51400}),
        ("Total equity (closing)", {"FY2025": 711661, "FY2024": 723469, "FY2023": 696139, "FY2022": 646867, "FY2021": 641337, "FY2020": 616637, "FY2019": 608453}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": -49724, "FY2024": 160113, "FY2023": 38755, "FY2022": 472150, "FY2021": 689232, "FY2020": 642905, "FY2019": 501914}),
        ("Net cash generated from/(used in) investing activities", {"FY2025": -212792, "FY2024": -347349, "FY2023": -290446, "FY2022": -898, "FY2021": -552065, "FY2020": 476440, "FY2019": -560040}),
        ("Net cash (used in)/generated from financing activities", {"FY2025": 72955, "FY2024": 98614, "FY2023": 99107, "FY2022": -8029, "FY2021": -487797, "FY2020": -151400, "FY2019": 24000}),
        ("Cash and cash at central banks at 31 December", {"FY2025": 770327, "FY2024": 959888, "FY2023": 1048510, "FY2022": 1201094, "FY2021": 737871, "FY2020": 1088501, "FY2019": 120556}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", {"FY2025": "14.22%", "FY2024": "15.42%", "FY2023": "15.99%", "FY2022": "16.34%", "FY2021": "16.31%", "FY2020": "17.16%", "FY2019": "15.71%"}),
        ("LCR", {"FY2025": "185%", "FY2024": "287%", "FY2023": "236%", "FY2022": "354%", "FY2021": "158%", "FY2020": "551%", "FY2019": "221%"}),
        ("NSFR", {"FY2025": "130%", "FY2024": "126%", "FY2023": "130%", "FY2022": "138%", "FY2021": "109%", "FY2020": "138%", "FY2019": "122%"}),
    ],
    note="Cash flows are RCI Bank UK Group consolidated figures. Dedicated UK KM1 Pillar 3 amounts are available for FY2024-FY2023; earlier years use explicitly disclosed annual-report ratios. FY2025 IS A LOSS YEAR and its ratios are annual-report basis (no FY2025 Pillar 3 exists yet) - see the single-metric sheets' notes for the basis breaks that follow from that. The FY2025 loss is driven by a single GBP150m charge to the provision for liabilities for the FCA motor-finance commission redress scheme (note 27); without it profit before tax would have been positive. FY2024 and FY2023 are shown on their ORIGINAL as-reported basis: the FY2025 accounts restate both for a Lease Hire depreciation error (note 39), and this workbook records that restatement in the sheet notes and on the Statement of Changes in Equity rather than overwriting the published figures - see the Balance Sheet and Statement of Changes in Equity source notes. Total comprehensive income for FY2025 is shown as the (64,097) printed on the Consolidated Statement of Other Comprehensive Income (p.46), which is the same basis as every earlier year here; the Statement of Changes in Equity prints a differently-constructed (18,209) on the same filing and both are reproduced on that sheet. Total operating expense for FY2025 is cost of sales 216,829 + operating expenses 81,285, the same two printed lines the earlier years use. FY2019 is a 10-month Group period (6 March-31 December 2019) and FY2018 is excluded - RCI Bank UK Limited was dormant that whole year (2-page nil dormant-company filing) - see the Cash Flow Statement source note for both. Blank cells mean not disclosed, not zero.",
)

bw.save("/Users/armaan/code/katalysis/banks/RCI BANK UK FINANCIALS.xlsx")
