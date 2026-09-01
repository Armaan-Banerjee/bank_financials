import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
COMPANY = "Schroder & Co. Limited"
COMPANY_NO = "02280926"

AR_URL = {
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/02280926/filing-history/MzUxODQzNTIxOWFkaXF6a2N4/document?download=0&format=pdf",
    "FY2024": "https://find-and-update.company-information.service.gov.uk/company/02280926/filing-history/MzQ2MjI2NjAwNmFkaXF6a2N4/document?download=0&format=pdf",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/02280926/filing-history/MzQxNzc4NDk4OGFkaXF6a2N4/document?download=0&format=pdf",
    "FY2022": "https://find-and-update.company-information.service.gov.uk/company/02280926/filing-history/MzM3NDc5MjQzOGFkaXF6a2N4/document?download=0&format=pdf",
    "FY2021": "https://find-and-update.company-information.service.gov.uk/company/02280926/filing-history/MzMzNTY5MDAyOGFkaXF6a2N4/document?download=0&format=pdf",
}
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/02280926"
PRA_URL = "https://www.bankofengland.co.uk/prudential-regulation/authorisations/which-firms-does-the-pra-regulate"

ENTITY_NOTE = (
    f"{COMPANY} (Companies House company {COMPANY_NO}, FRN 144206, LEI XZYM01I1402576QWNU05) is the UK legal entity in the supplied Banks List 2608.xlsx. "
    "Companies House identifies the company by this name and shows accounts made up to 31 December 2025; the Bank of England PRA register lists the same legal name and FRN. "
    "The accounts are standalone Company financial statements in GBP'000. Schroder & Co. Limited is part of the wider Schroders group, but group figures are not substituted. "
    "All five Companies House accounts are image-only scans; they were OCR-processed with ocrmypdf/tesseract and the cash-flow pages were checked against rendered pages."
)

CASH_SOURCES = (
    "Sources - Schroder & Co. Limited standalone statutory cash flow statements, GBP'000. "
    f"FY2025/FY2024: 2025 accounts, p.19 - {AR_URL['FY2025']}\n"
    f"FY2024/FY2023: 2024 accounts, p.20 - {AR_URL['FY2024']}\n"
    f"FY2023/FY2022: 2023 accounts, p.21 - {AR_URL['FY2023']}\n"
    f"FY2022/FY2021: 2022 accounts, p.19 - {AR_URL['FY2022']}\n"
    f"FY2021: 2021 accounts, p.21 - {AR_URL['FY2021']}\n\n"
    f"Entity verification: Companies House {CH_URL}; PRA register {PRA_URL}.\n\n"
    + ENTITY_NOTE
    + "\n\nThe 2025 accounts separately report an exchange-rate effect of -£13,679k after the net increase in cash; it is retained as a separate tail line. The 2023 accounts contain a £1k inconsistency between the detailed reconciliation and the reported operating-cash subtotal; the reported statement subtotal is retained and the £1k source difference is shown explicitly."
)

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 111866, "FY2024": 107817, "FY2023": 60969, "FY2022": 78707, "FY2021": 62386}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": 6424, "FY2024": 17, "FY2023": 18, "FY2022": 24, "FY2021": 9}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 0, "FY2024": 4278, "FY2023": 9565, "FY2022": 8562, "FY2021": 9013}),
    ("DATA", "Impairment of software", {"FY2023": 3352}),
    ("DATA", "Impairment of investment in subsidiary", {"FY2025": 4628}),
    ("DATA", "Other non-cash movements", {"FY2025": -4804}),
    ("DATA", "Interest income", {"FY2025": -15288}),
    ("DATA", "Dividend income", {"FY2025": -6000}),
    ("DATA", "Research and development tax credits", {"FY2023": 0, "FY2022": -275}),
    ("DATA", "Net profit/(loss) on financial instruments", {"FY2021": -4}),
    ("DATA", "Net (increase)/decrease in loans and advances to customers", {"FY2025": -11077, "FY2024": 15076, "FY2023": 106249, "FY2022": -15429, "FY2021": -102247}),
    ("DATA", "Net (increase)/decrease in positive replacement values of derivatives", {"FY2024": 954, "FY2023": 1301, "FY2022": -4650, "FY2021": 8386}),
    ("DATA", "Net (increase)/decrease in trade and other receivables", {"FY2025": -16, "FY2024": -491, "FY2023": 3401, "FY2022": -943, "FY2021": -2225}),
    ("DATA", "Net (increase)/decrease in prepayments and accrued income", {"FY2025": -15981, "FY2024": 25955, "FY2023": -39490, "FY2022": 7780, "FY2021": -13259}),
    ("DATA", "Net (decrease)/increase in deposits from banks", {"FY2025": 2822, "FY2024": -33467, "FY2023": -56632, "FY2022": 4153, "FY2021": 54233}),
    ("DATA", "Net increase in amounts due to customers/customer accounts", {"FY2025": 283348, "FY2024": 538072, "FY2023": 159721, "FY2022": 670973, "FY2021": 165264}),
    ("DATA", "Net (increase)/decrease in interbank deposits over three months", {"FY2025": -35343, "FY2024": 199051, "FY2023": -267818, "FY2022": -67289, "FY2021": 22981}),
    ("DATA", "Net decrease/(increase) in replacement values of derivatives", {"FY2025": 798, "FY2024": -1523, "FY2023": -30, "FY2022": 2517, "FY2021": -8572}),
    ("DATA", "Net increase/(decrease) in trade and other payables", {"FY2025": 10471, "FY2024": -6253, "FY2023": 5937, "FY2022": -5799, "FY2021": 6964}),
    ("DATA", "Net increase/(decrease) in accruals and deferred income", {"FY2025": 19332, "FY2024": -40059, "FY2023": 38592, "FY2022": -5190, "FY2021": 19883}),
    ("DATA", "Source reconciliation difference", {"FY2025": -1}),
    ("DATA", "Income taxes paid", {"FY2025": -28511, "FY2024": -16292, "FY2023": -14573, "FY2022": -13294, "FY2021": -12071}),
    ("TOTAL", "Net cash generated from operating activities", {"FY2025": 322668, "FY2024": 793135, "FY2023": 10562, "FY2022": 659847, "FY2021": 210741}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of business", {"FY2021": 148}),
    ("DATA", "Purchase of software", {"FY2025": -2123, "FY2024": -1669, "FY2023": -2161, "FY2022": -3318, "FY2021": -3553}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -32, "FY2024": 0, "FY2023": -3, "FY2022": -242, "FY2021": -21}),
    ("DATA", "Disposal of property, plant and equipment", {"FY2023": 131}),
    ("DATA", "Net purchase of debt and other fixed income securities", {"FY2025": -62518, "FY2024": -274941, "FY2023": -296126, "FY2022": -158254, "FY2021": -36538}),
    ("DATA", "Dividends received", {"FY2025": 6000, "FY2022": 2898}),
    ("DATA", "Acquisition of subsidiary", {"FY2024": -33251}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -58673, "FY2024": -309861, "FY2023": -298159, "FY2022": -158916, "FY2021": -39964}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Increase in share capital", {"FY2024": 31000}),
    ("DATA", "Tax paid in respect of share schemes", {"FY2021": -1}),
    ("DATA", "Dividends paid", {"FY2025": -73900, "FY2024": -47136, "FY2023": -64861, "FY2022": -35000, "FY2021": -36692}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": -73900, "FY2024": -16136, "FY2023": -64861, "FY2022": -35000, "FY2021": -36693}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 190095, "FY2024": 467138, "FY2023": -352458, "FY2022": 465931, "FY2021": 134084}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 2577524, "FY2024": 2110386, "FY2023": 2462844, "FY2022": 1996913, "FY2021": 1862829}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents", {"FY2025": -13679}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 2753940, "FY2024": 2577524, "FY2023": 2110386, "FY2022": 2462844, "FY2021": 1996913}),
]

bw = BankWorkbook(bank_name=COMPANY, years=YEARS, year_label=None, header_color="1F4E79")
bw.add_cash_flow_sheet(
    title=f"{COMPANY} — Cash Flow Statement",
    subtitle="Standalone Company basis, GBP'000. Five latest available financial years.",
    rows=rows,
    sources_text=CASH_SOURCES,
    first_col_width=75,
    source_height=360,
    unit_suffix=" (GBP'000)",
)

ND = "Not publicly disclosed for Schroder & Co. Limited as a standalone entity. The annual accounts refer to regulatory capital/liquidity processes but do not provide the requested numeric Pillar 3 metric. Schroders group figures are not substituted."
for metric_name in ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital", "Total Capital Ratio", "Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]:
    bw.add_metric_sheet(metric_name, "Not disclosed", [(metric_name, {y: ND for y in YEARS})], CASH_SOURCES, note=ND, first_col_width=55, source_height=320)

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated from operating activities", {"FY2025": 322668, "FY2024": 793135, "FY2023": 10562, "FY2022": 659847, "FY2021": 210741}),
        ("Net cash used in investing activities", {"FY2025": -58673, "FY2024": -309861, "FY2023": -298159, "FY2022": -158916, "FY2021": -39964}),
        ("Net cash used in financing activities", {"FY2025": -73900, "FY2024": -16136, "FY2023": -64861, "FY2022": -35000, "FY2021": -36693}),
        ("Cash and cash equivalents at end of year", {"FY2025": 2753940, "FY2024": 2577524, "FY2023": 2110386, "FY2022": 2462844, "FY2021": 1996913}),
    ],
    cash_flow_unit="GBP'000",
    ratios=[("CET1 Ratio", {y: "Not publicly disclosed" for y in YEARS})],
    note="All regulatory metric sheets are intentionally marked not publicly disclosed at entity level; see their source notes.",
)
bw.save("/Users/armaan/code/katalysis/banks/SCHRODER FINANCIALS.xlsx")
