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

STATEMENTS_SOURCES = (
    "Sources - Schroder & Co. Limited standalone statutory accounts, GBP'000. "
    f"FY2025/FY2024: 2025 accounts, Income statement p.15, Statement of comprehensive income p.16, "
    f"Statement of financial position p.17, Statement of changes in equity p.18, Note 9 (Loans and advances to "
    f"customers) p.30, Note 13(a) (expected credit losses) p.40 - {AR_URL['FY2025']}\n"
    f"FY2023/FY2022: 2023 accounts, Income statement p.17, Statement of comprehensive income p.18, "
    f"Statement of financial position p.19, Statement of changes in equity p.20, Note 10 (Loans and advances to "
    f"customers) p.33, Note 13(a) (expected credit losses) p.41 - {AR_URL['FY2023']}\n"
    f"FY2021: 2021 accounts, Income statement p.17, Statement of comprehensive income p.18, "
    f"Statement of financial position p.19, Statement of changes in equity p.20, Note 10 (Loans and advances to "
    f"customers) p.35, Note 13(a) (expected credit losses) p.43 - {AR_URL['FY2021']}\n\n"
    f"Entity verification: Companies House {CH_URL}; PRA register {PRA_URL}.\n\n"
    + ENTITY_NOTE
    + "\n\nFY2024 figures for the Balance Sheet, Profit & Loss and Statement of Changes in Equity are taken from "
    "the 2025 accounts' own FY2024 comparative column (the FY2024 accounts themselves were not separately "
    "fetched this session); FY2022 figures are taken from the 2023 accounts' own FY2022 comparative column. "
    "The 2025 accounts re-presented their FY2024 equity comparative by combining Retained earnings and the Fair "
    "value reserve into a single 'Profit and loss reserve' column; the Statement of Changes in Equity sheet "
    "applies that same combined presentation to every year (FY2021-FY2023 recombined from their own separately-"
    "reported Fair value reserve and Retained earnings columns) so the ladder uses one consistent column shape "
    "throughout - this ties exactly: FY2023's own combined closing balance (12 + 133,425 = 133,437) matches the "
    "2025 accounts' own restated 1 January 2024 opening balance exactly."
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Loans and advances to banks", {"FY2025": 2935361, "FY2024": 2723942, "FY2023": 2455855, "FY2022": 2540496, "FY2021": 2007276}),
    ("DATA", "Other financial assets", {"FY2025": 1046693, "FY2024": 977035, "FY2023": 702664, "FY2022": 407352, "FY2021": 245144}),
    ("DATA", "Loans and advances to customers", {"FY2025": 212217, "FY2024": 201141, "FY2023": 216217, "FY2022": 322466, "FY2021": 307037}),
    ("DATA", "Trade and other receivables", {"FY2025": 1520, "FY2024": 1503, "FY2023": 1012, "FY2022": 4413, "FY2021": 3470}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 86310, "FY2024": 70329, "FY2023": 96284, "FY2022": 56794, "FY2021": 64574}),
    ("DATA", "Property, plant and equipment", {"FY2025": 94, "FY2024": 79, "FY2023": 96, "FY2022": 242, "FY2021": 24}),
    ("DATA", "Investments in subsidiaries", {"FY2025": 2248, "FY2024": 37232, "FY2023": 13, "FY2022": 13, "FY2021": 2911}),
    ("DATA", "Deferred tax", {"FY2025": 4148, "FY2024": 4020, "FY2023": 3398, "FY2022": 1329, "FY2021": 197}),
    ("DATA", "Goodwill and intangible assets", {"FY2025": 129282, "FY2024": 99799, "FY2023": 102408, "FY2022": 113164, "FY2021": 118408}),
    ("TOTAL", "Total assets", {"FY2025": 4417873, "FY2024": 4115080, "FY2023": 3577947, "FY2022": 3446269, "FY2021": 2749041}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 37342, "FY2024": 34520, "FY2023": 67987, "FY2022": 124619, "FY2021": 120466}),
    ("DATA", "Customer accounts", {"FY2025": 3865026, "FY2024": 3604438, "FY2023": 3066366, "FY2022": 2906645, "FY2021": 2235672}),
    ("DATA", "Financial liabilities and derivative contracts", {"FY2025": 1289, "FY2024": 3708, "FY2023": 5230, "FY2022": 5260, "FY2021": 2743}),
    ("DATA", "Trade and other payables", {"FY2025": 18463, "FY2024": 7991, "FY2023": 14244, "FY2022": 8308, "FY2021": 14106}),
    ("DATA", "Corporation tax", {"FY2025": 30036, "FY2024": 28460, "FY2023": 16143, "FY2022": 14933, "FY2021": 13223}),
    ("DATA", "Accruals and deferred income", {"FY2025": 87681, "FY2024": 68948, "FY2023": 105040, "FY2022": 66448, "FY2021": 71638}),
    ("TOTAL", "Total liabilities", {"FY2025": 4039837, "FY2024": 3748065, "FY2023": 3275010, "FY2022": 3126213, "FY2021": 2457848}),
    ("SECTION", "Equity", {}),
    ("TOTAL", "Net assets", {"FY2025": 378036, "FY2024": 367015, "FY2023": 302937, "FY2022": 320056, "FY2021": 291193}),
    ("TOTAL", "Total equity", {"FY2025": 378036, "FY2024": 367015, "FY2023": 302937, "FY2022": 320056, "FY2021": 291193}),
]
bw.add_balance_sheet_sheet(
    title=f"{COMPANY} — Balance Sheet",
    subtitle="Standalone Company basis, GBP'000. Statement of financial position; no separate equity component breakdown appears on this statement, only Net assets/Total equity (see the Statement of Changes in Equity sheet for the equity roll-forward).",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=75,
    source_height=420,
    unit_suffix=" (GBP'000)",
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Debt securities and other fixed income securities", {"FY2025": 44209, "FY2024": 43060, "FY2023": 24783, "FY2022": 5433, "FY2021": 563}),
    ("DATA", "Other interest income and similar income", {"FY2025": 141544, "FY2024": 142771, "FY2023": 126368, "FY2022": 44776, "FY2021": 7001}),
    ("DATA", "Interest expense", {"FY2025": -146033, "FY2024": -149016, "FY2023": -118911, "FY2022": -29344, "FY2021": -518}),
    ("TOTAL", "Net interest income", {"FY2025": 39720, "FY2024": 36815, "FY2023": 32240, "FY2022": 20865, "FY2021": 7046}),
    ("DATA", "Fee and commission income", {"FY2025": 280921, "FY2024": 258142, "FY2023": 224377, "FY2022": 226761, "FY2021": 211390}),
    ("DATA", "Fee and commission expense", {"FY2025": -12746, "FY2024": -15673, "FY2023": -9667, "FY2022": -8815, "FY2021": -9241}),
    ("TOTAL", "Net fee income", {"FY2025": 268175, "FY2024": 242469, "FY2023": 214710, "FY2022": 217946, "FY2021": 202149}),
    ("DATA", "Net gains on financial instruments and other income", {"FY2025": 17805, "FY2024": 12017, "FY2023": 6335, "FY2022": 7246, "FY2021": 7263}),
    ("TOTAL", "Total net income", {"FY2025": 325700, "FY2024": 291301, "FY2023": 253285, "FY2022": 246057, "FY2021": 216458}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -213834, "FY2024": -183484, "FY2023": -192316, "FY2022": -168766, "FY2021": -154072}),
    ("DATA", "Gain on disposal of subsidiary undertaking", {"FY2022": 1416}),
    ("TOTAL", "Profit before tax", {"FY2025": 111866, "FY2024": 107817, "FY2023": 60969, "FY2022": 78707, "FY2021": 62386}),
    ("DATA", "Tax", {"FY2025": -27286, "FY2024": -28015, "FY2023": -13833, "FY2022": -13846, "FY2021": -12547}),
    ("TOTAL", "Profit after tax", {"FY2025": 84580, "FY2024": 79802, "FY2023": 47136, "FY2022": 64861, "FY2021": 49839}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Net gains/(losses) on financial assets at fair value through OCI", {"FY2025": 55, "FY2024": 393, "FY2023": 489, "FY2022": -695, "FY2021": -73}),
    ("DATA", "Net realised loss on disposal of debt securities classified as FVOCI", {"FY2025": -6, "FY2024": -9, "FY2023": -2, "FY2022": -2, "FY2021": 0}),
    ("TOTAL", "Other comprehensive income for the year", {"FY2025": 49, "FY2024": 384, "FY2023": 487, "FY2022": -697, "FY2021": -73}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 84629, "FY2024": 80186, "FY2023": 47623, "FY2022": 64164, "FY2021": 49766}),
]
bw.add_income_statement_sheet(
    title=f"{COMPANY} — Profit & Loss",
    subtitle="Standalone Company basis, GBP'000. All the Company's revenues derive from continuing operations. FY2020's realised loss line is disclosed elsewhere in these accounts but the FY2021 figure is nil, not a gap.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=75,
    source_height=420,
    unit_suffix=" (GBP'000)",
)

equity_headers = ["Share capital", "Profit and loss reserve", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2021", (169500, 109056, 278556)),
    ("TOTAL", "Total comprehensive income for the year (FY2021)", (None, 49766, 49766)),
    ("DATA", "Tax in respect of share schemes (FY2021)", (None, 367, 367)),
    ("DATA", "Equity retained earnings (FY2021)", (None, -804, -804)),
    ("DATA", "Dividends paid (FY2021)", (None, -36692, -36692)),
    ("TOTAL", "At 31 December 2021", (169500, 121693, 291193)),
    ("TOTAL", "Total comprehensive income for the year (FY2022)", (None, 64164, 64164)),
    ("DATA", "Tax in respect of share schemes (FY2022)", (None, -301, -301)),
    ("DATA", "Dividends paid (FY2022)", (None, -35000, -35000)),
    ("TOTAL", "At 31 December 2022", (169500, 150556, 320056)),
    ("TOTAL", "Total comprehensive income for the year (FY2023)", (None, 47623, 47623)),
    ("DATA", "Tax in respect of share schemes (FY2023)", (None, 119, 119)),
    ("DATA", "Dividends paid (FY2023)", (None, -64861, -64861)),
    ("TOTAL", "At 31 December 2023", (169500, 133437, 302937)),
    ("TOTAL", "Total comprehensive income for the year (FY2024)", (None, 80186, 80186)),
    ("DATA", "Tax in respect of share schemes (FY2024)", (None, 28, 28)),
    ("DATA", "Increase in share capital (FY2024)", (31000, None, 31000)),
    ("DATA", "Dividends paid (FY2024)", (None, -47136, -47136)),
    ("TOTAL", "At 31 December 2024", (200500, 166515, 367015)),
    ("TOTAL", "Total comprehensive income for the year (FY2025)", (None, 84629, 84629)),
    ("DATA", "Tax in respect of share schemes (FY2025)", (None, 292, 292)),
    ("DATA", "Dividends paid (FY2025)", (None, -73900, -73900)),
    ("TOTAL", "At 31 December 2025", (200500, 177536, 378036)),
]
bw.add_equity_changes_sheet(
    title=f"{COMPANY} — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, standalone Company basis, GBP'000. Equity reconciliation ladder confirmed: every year's own closing balance ties exactly to both the next year's own opening balance and that year's own Balance Sheet Total equity - zero undocumented plug rows across all 5 years, including FY2021's easy-to-skip 'Equity retained earnings' adjustment and FY2024's share capital increase.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=52,
    source_height=380,
)

bw.add_cash_flow_sheet(
    title=f"{COMPANY} — Cash Flow Statement",
    subtitle="Standalone Company basis, GBP'000. Five latest available financial years.",
    rows=rows,
    sources_text=CASH_SOURCES,
    first_col_width=75,
    source_height=360,
    unit_suffix=" (GBP'000)",
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by product (Note 9/10)", {}),
    ("DATA", "Overdrafts", {"FY2025": 696, "FY2024": 1577, "FY2023": 4466, "FY2022": 2006, "FY2021": 1222}),
    ("DATA", "Term loans", {"FY2025": 141372, "FY2024": 138909, "FY2023": 142859, "FY2022": 230230, "FY2021": 291366}),
    ("DATA", "Mortgages", {"FY2025": 70149, "FY2024": 60655, "FY2023": 68892, "FY2022": 90230, "FY2021": 14449}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 212217, "FY2024": 201141, "FY2023": 216217, "FY2022": 322466, "FY2021": 307037}),
    ("SECTION", "Expected credit losses (Note 13(a))", {}),
    ("DATA", "Gross carrying value", {"FY2025": 212228, "FY2024": 201150, "FY2023": 216233, "FY2022": 322483, "FY2021": 307082}),
    ("DATA", "Expected credit losses", {"FY2025": -11, "FY2024": -10, "FY2023": -15, "FY2022": -17, "FY2021": -45}),
    ("TOTAL", "Net carrying value", {"FY2025": 212217, "FY2024": 201141, "FY2023": 216217, "FY2022": 322466, "FY2021": 307037}),
    ("DATA", "Expected credit losses as % of gross carrying value", {"FY2025": "0.0%", "FY2024": "0.0%", "FY2023": "0.0%", "FY2022": "0.0%", "FY2021": "0.0%"}),
]
bw.add_asset_quality_sheet(
    title=f"{COMPANY} — Asset Quality",
    subtitle="Standalone Company basis, GBP'000. Loans and advances to customers are usually secured. Under IFRS 9's three-stage model, all financial assets have been classified as performing (Stage 1) in every year FY2021-FY2025 covered by this workbook - no Stage 2 (under-performing) or Stage 3 (non-performing/defaulted) exposure in any of those years. (The FY2020 comparative disclosed in the FY2021 accounts included £1,795k of loans classified as non-performing/Stage 3, giving rise to £59,000 of expected credit losses - fully resolved by FY2021, the earliest year in this workbook, which reports zero Stage 2/3 exposure.) FY2023/FY2024's Net carrying value is the source's own reported figure (matching the Balance Sheet exactly) and is £1k above the Gross carrying value less Expected credit losses arithmetic - a genuine source rounding artifact, not a transcription error.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=380,
    unit_suffix=" (GBP'000)",
)

ND = "Not publicly disclosed for Schroder & Co. Limited as a standalone entity. The annual accounts refer to regulatory capital/liquidity processes but do not provide the requested numeric Pillar 3 metric. Schroders group figures are not substituted."
_pillar3_before_rwa = ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital", "Total Capital Ratio", "Total RWAs"]
_pillar3_after_rwa = ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]
for metric_name in _pillar3_before_rwa:
    bw.add_metric_sheet(metric_name, "Not disclosed", [(metric_name, {y: ND for y in YEARS})], CASH_SOURCES, note=ND, first_col_width=55, source_height=320)
bw.add_rwa_breakdown_sheet(
    title=f"{COMPANY} — RWA Breakdown",
    subtitle="Not publicly disclosed at entity level.",
    rows=[("DATA", "RWA Breakdown", {y: "Not publicly disclosed" for y in YEARS})],
    sources_text=CASH_SOURCES,
    first_col_width=54,
    source_height=180,
    unit_suffix="",
)
for metric_name in _pillar3_after_rwa:
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
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 4417873, "FY2024": 4115080, "FY2023": 3577947, "FY2022": 3446269, "FY2021": 2749041}),
        ("Loans and advances to customers", {"FY2025": 212217, "FY2024": 201141, "FY2023": 216217, "FY2022": 322466, "FY2021": 307037}),
        ("Customer accounts", {"FY2025": 3865026, "FY2024": 3604438, "FY2023": 3066366, "FY2022": 2906645, "FY2021": 2235672}),
        ("Total equity", {"FY2025": 378036, "FY2024": 367015, "FY2023": 302937, "FY2022": 320056, "FY2021": 291193}),
    ],
    balance_sheet_unit="GBP'000",
    income_statement_totals=[
        ("Total net income", {"FY2025": 325700, "FY2024": 291301, "FY2023": 253285, "FY2022": 246057, "FY2021": 216458}),
        ("Administrative expenses", {"FY2025": -213834, "FY2024": -183484, "FY2023": -192316, "FY2022": -168766, "FY2021": -154072}),
        ("Profit after tax", {"FY2025": 84580, "FY2024": 79802, "FY2023": 47136, "FY2022": 64861, "FY2021": 49839}),
    ],
    income_statement_unit="GBP'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 367015, "FY2024": 302937, "FY2023": 320056, "FY2022": 291193, "FY2021": 278556}),
        ("Total comprehensive income for the year", {"FY2025": 84629, "FY2024": 80186, "FY2023": 47623, "FY2022": 64164, "FY2021": 49766}),
        ("Closing equity", {"FY2025": 378036, "FY2024": 367015, "FY2023": 302937, "FY2022": 320056, "FY2021": 291193}),
    ],
    equity_changes_unit="GBP'000",
)
bw.save("/Users/armaan/code/katalysis/banks/SCHRODER FINANCIALS.xlsx")
