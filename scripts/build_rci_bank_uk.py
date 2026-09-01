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

bw.add_cash_flow_sheet(
    title="RCI Bank UK Limited - Group Cash Flow Statement",
    subtitle="Group/consolidated basis, £'000; five latest available financial years FY2020-FY2024. See source note.",
    rows=rows, sources_text=CASH_SOURCES, first_col_width=68, source_height=210, unit_suffix=" (£'000)",
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
metric("Leverage Ratio", "£'000 / %", [("Total exposure measure excluding claims on central banks", {"FY2024": 6642000, "FY2023": 6148000}), ("Leverage ratio excluding claims on central banks (%)", {"FY2024": "10.6%", "FY2023": "10.9%"})], "No leverage ratio was located in the FY2022-FY2020 annual-report narrative; the dedicated UK KM1 disclosure supplies FY2024-FY2023.")
metric("LCR", "£'000 / %", [("Total high-quality liquid assets (HQLA), weighted value - average", {"FY2024": 899000, "FY2023": 1035000}), ("Total net cash outflows (adjusted value)", {"FY2024": 365000, "FY2023": 467000}), ("Liquidity Coverage Ratio (%)", {"FY2024": "287%", "FY2023": "236%", "FY2022": "354%", "FY2021": "158%", "FY2020": "551%"})], "FY2024-FY2023 amounts and ratios are UK KM1. The FY2022-FY2020 headline ratios are from the statutory annual-report Capital and Liquidity sections.")
metric("NSFR", "£'000 / %", [("Total available stable funding", {"FY2024": 6115000, "FY2023": 5622000}), ("Total required stable funding", {"FY2024": 4863000, "FY2023": 4312000}), ("NSFR ratio (%)", {"FY2024": "126%", "FY2023": "130%", "FY2022": "138%", "FY2021": "109%", "FY2020": "138%"})], "FY2024-FY2023 amounts and ratios are UK KM1. The FY2022-FY2020 headline ratios are from the statutory annual-report Capital and Liquidity sections.")
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No quantitative MREL ratio was found in the RCI Bank UK annual reports, the RCI Bank UK Pillar 3 disclosures reviewed, or the official facts-and-figures page.")

bw.add_overview_sheet(
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
