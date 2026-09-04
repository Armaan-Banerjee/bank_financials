import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

# Companies House annual accounts filings (company 00383032). All 4 filings
# used are fully scanned (image-only) - every figure below was read visually
# from the rendered page image and cross-checked against the adjoining year's
# own comparative column.
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00383032/filing-history/MzUxODk5NjMzM2FkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/00383032/filing-history/MzQ2NDYzNjU4OGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00383032/filing-history/MzQyMDI4MDMwNWFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00383032/filing-history/MzMzODQ2NDUzMWFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "Entity: Cater Allen Limited (FRN 178737, company 00383032), a UK private bank, wholly "
    "owned by Santander Private Banking UK Limited, itself a wholly-owned subsidiary of "
    "Santander UK plc (ultimate UK parent: Santander UK Group Holdings plc; ultimate parent: "
    "Banco Santander SA). Reports in GBP; no FX conversion needed.\n\n"
    "GENUINELY NEW PATTERN - exemption newly adopted in the FINAL year of this workbook's "
    "window, not from the start: FY2021-FY2024 all have a full, audited Statement of Cash "
    "Flows (confirmed directly from each year's own filing - the FY2024 filing, approved 24 "
    "April 2025, includes a complete Cash Flow Statement for both FY2024 and its FY2023 "
    "comparative). Only the FY2025 filing (approved 23 April 2026) newly invokes the FRS 101 "
    "exemption for IAS 7 'Statement of cash flows' - its Basis of Preparation note states the "
    "financial statements 'are presented with the benefit of the disclosure exemptions "
    "permitted by FRS 101 with regards to: IAS 7, Statement of cash flows... standards not yet "
    "effective', and no cash flow statement (for FY2025 OR its FY2024 comparative) appears "
    "anywhere in that filing. This is a mirror-image of Tandem Bank/AIB Group UK/Atom Bank's "
    "'exemption kicks in partway through the window' pattern - here it only blocks the LAST "
    "year rather than the earlier years, so FY2021-FY2024 are built as a normal full cash flow "
    "statement and only FY2025 is left blank with this note.\n\n"
    "PRESENTATION FORMAT NOTE: FY2021's own filing discloses only a single aggregate operating "
    "cash flow figure (no trading-activities/working-capital breakdown, no investing/financing "
    "sections) - this is the source's own presentation for that year, not a gap. FY2022-FY2024 "
    "(sourced from the FY2023 and FY2024 filings, whose comparative/current columns cross-"
    "check exactly) use a fuller breakdown. Blank cells on the more granular rows for FY2021 "
    "reflect this genuine presentation difference; the year's one available total is placed on "
    "the 'Net cash (used in)/generated from operating activities' row.\n\n"
    "Full opening-to-closing chain cross-checked and ties exactly across all 4 years with cash "
    "flow data: FY2021 closing (5,128,808) = FY2022 opening; FY2022 closing (5,671,848) = "
    "FY2023 opening; FY2023 closing (5,383,852) = FY2024 opening; FY2024 closing = 5,540,507, "
    "matching the FY2024 Balance Sheet's own 'Loans and advances to banks' figure exactly."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Cater Allen Limited's own Cash Flow Statement, GBP'000:\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.14 (Cash Flow Statement) and p.35 "
    f"(Note 24, reconciliation) - {AR2021_URL}\n"
    f"FY2022 (restated comparative, used as primary column per project convention): Annual "
    f"Report and Financial Statements 2023, p.26 (Cash Flow Statement, 2022 restated column) - {AR2023_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.26 (Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.27 (Cash Flow Statement) - {AR2024_URL}\n"
    f"FY2025: Not applicable - FRS 101 cash-flow exemption newly taken this year. Annual Report "
    f"and Financial Statements 2025, p.29 (Note 1, Basis of preparation) - {AR2025_URL}\n\n"
    + ENTITY_NOTE
)

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2024": 168882, "FY2023": 169529, "FY2022": 67307}),
    ("DATA", "Effect of foreign exchange rates on loans and advances to banks",
     {"FY2024": -81, "FY2023": 3545, "FY2022": -10493}),
    ("DATA", "Amortisation of intangible assets", {"FY2024": 2771, "FY2023": 2905, "FY2022": 2905}),
    ("DATA", "Impairment reversal", {"FY2022": -35}),
    ("TOTAL", "Net cash flow from trading activities", {"FY2024": 171572, "FY2023": 175979, "FY2022": 59684}),
    ("DATA", "Decrease in loans and advances to customers", {"FY2022": 35}),
    ("DATA", "Decrease/(increase) in other assets", {"FY2024": 3044, "FY2023": -2207, "FY2022": -10406}),
    ("DATA", "Increase/(decrease) in customer accounts", {"FY2024": 135483, "FY2023": -348801, "FY2022": 782202}),
    ("DATA", "Increase/(decrease) in deposits by banks", {"FY2024": 2820, "FY2023": 2577, "FY2022": -1348}),
    ("DATA", "Increase in amounts due to other group companies", {"FY2024": 1736, "FY2023": 2073, "FY2022": 4061}),
    ("DATA", "(Decrease)/increase in other liabilities", {"FY2024": -9420, "FY2023": 4491, "FY2022": 8942}),
    ("DATA", "Settlement to Santander UK plc in respect of Corporation Tax",
     {"FY2024": -47048, "FY2023": -18170, "FY2022": -10623}),
    ("TOTAL", "Net cash (used in)/generated from operating activities",
     {"FY2024": 258187, "FY2023": -184058, "FY2022": 832547, "FY2021": -200379}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Intangible asset work in progress", {"FY2023": -393}),
    ("TOTAL", "Cash used in investing activities", {"FY2024": 0, "FY2023": -393, "FY2022": 0}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividend paid", {"FY2024": -100000, "FY2023": -100000, "FY2022": -300000}),
    ("TOTAL", "Cash used in financing activities", {"FY2024": -100000, "FY2023": -100000, "FY2022": -300000}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents",
     {"FY2024": 158187, "FY2023": -284451, "FY2022": 532547, "FY2021": -200379}),
    ("DATA", "Effect of foreign exchange rates", {"FY2024": -1532, "FY2023": -3545, "FY2022": 10493}),
    ("DATA", "Opening cash and cash equivalents",
     {"FY2024": 5383852, "FY2023": 5671848, "FY2022": 5128808, "FY2021": 5329187}),
    ("TOTAL", "Closing cash and cash equivalents",
     {"FY2024": 5540507, "FY2023": 5383852, "FY2022": 5671848, "FY2021": 5128808}),
]

bw = BankWorkbook(bank_name="Cater Allen Limited", years=YEARS, year_label=None, header_color="1A5276")

# ---------------------------------------------------------------
# Balance Sheet / Profit & Loss / Statement of Changes in Equity
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - Cater Allen Limited's own Balance Sheet / Statement of Comprehensive Income / "
    "Statement of Changes in Equity, GBP'000, all scanned/image-only Companies House filings "
    "visually transcribed:\n"
    f"FY2025: Annual Report and Financial Statements 2025, p.27 (Statement of Comprehensive "
    f"Income, Statement of Changes in Equity) and p.28 (Balance Sheet) - {AR2025_URL}\n"
    f"FY2024 (own report, not the FY2025 filing's restated comparative - see PRESENTATION NOTE "
    f"below): Annual Report and Financial Statements 2024, p.25 (Statement of Comprehensive "
    f"Income, Statement of Changes in Equity) and p.26 (Balance Sheet) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2024, p.25 (2023 comparative column) and "
    f"p.26 (2023 comparative column) - {AR2024_URL}\n"
    f"FY2022 (restated comparative, used as primary column per project convention - matches the "
    f"existing Cash Flow Statement's own treatment of this year): Annual Report and Financial "
    f"Statements 2023, p.24 (Statement of Comprehensive Income, Statement of Changes in Equity, "
    f"2022 restated column) and p.25 (Balance Sheet, 2022 restated column) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.12 (Statement of Comprehensive "
    f"Income, Statement of Changes in Equity) and p.13 (Balance Sheet) - {AR2021_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: FY2025's own Statement of Comprehensive Income combines amortisation of "
    "intangible assets into a single 'Operating expenses' line, whereas FY2021-FY2024 each show "
    "'Operating expenses' and 'Amortisation of intangible assets' as two separate lines - both "
    "reproduced as each source presents them, not forced onto one basis. FY2021's own income "
    "statement additionally shows a one-off 'Other operating result' line (£479k) with no "
    "equivalent in any later year - shown as reported, not reclassified. The FY2025 Balance "
    "Sheet separately discloses 'Cash, and other balances at central banks' (£39,583k) for the "
    "first time; FY2021-FY2024 fold this into 'Loans and advances to banks' with no separate "
    "line - the FY2024 comparative column in the FY2025 filing is marked '(Restated)' for this "
    "split, but FY2024's own total assets/equity are unchanged either way, so this workbook uses "
    "FY2024's own (unrestated, undivided) presentation per project convention, leaving the "
    "'Cash, and other balances at central banks' cell blank for FY2021-FY2024. The Company holds "
    "no customer loans in any year (see Asset Quality sheet)."
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash, and other balances at central banks", {"FY2025": 39583}),
    ("DATA", "Loans and advances to banks",
     {"FY2025": 5297136, "FY2024": 5540507, "FY2023": 5383852, "FY2022": 5671848, "FY2021": 5128808}),
    ("DATA", "Loans and advances to customers",
     {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Other assets", {"FY2025": 7920, "FY2024": 9737, "FY2023": 12783, "FY2022": 10576, "FY2021": 170}),
    ("DATA", "Goodwill", {"FY2025": 30000, "FY2024": 30000, "FY2023": 30000, "FY2022": 30000, "FY2021": 30000}),
    ("DATA", "Intangible assets", {"FY2025": 155, "FY2024": 286, "FY2023": 3057, "FY2022": 5569, "FY2021": 8474}),
    ("DATA", "Deferred tax", {"FY2025": 8, "FY2024": 10, "FY2023": 12, "FY2022": 15, "FY2021": 22}),
    ("DATA", "Property, plant and equipment", {"FY2025": 6, "FY2024": 6, "FY2023": 6, "FY2022": 6, "FY2021": 6}),
    ("TOTAL", "Total assets",
     {"FY2025": 5374808, "FY2024": 5580546, "FY2023": 5429710, "FY2022": 5718014, "FY2021": 5167480}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 6652, "FY2024": 5902, "FY2023": 3082, "FY2022": 505, "FY2021": 2783}),
    ("DATA", "Customer accounts",
     {"FY2025": 4964597, "FY2024": 5112126, "FY2023": 4978130, "FY2022": 5326931, "FY2021": 4544224}),
    ("DATA", "Amounts due to group companies",
     {"FY2025": 14660, "FY2024": 10168, "FY2023": 8432, "FY2022": 6359, "FY2021": 1873}),
    ("DATA", "Other liabilities", {"FY2025": 20076, "FY2024": 7816, "FY2023": 17363, "FY2022": 12873, "FY2021": 3932}),
    ("DATA", "Current tax", {"FY2025": 34040, "FY2024": 47285, "FY2023": 47042, "FY2022": 18170, "FY2021": 10623}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 5040025, "FY2024": 5183297, "FY2023": 5054049, "FY2022": 5364838, "FY2021": 4563435}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 100000, "FY2024": 100000, "FY2023": 100000, "FY2022": 100000, "FY2021": 100000}),
    ("DATA", "Share premium", {"FY2025": 2950, "FY2024": 2950, "FY2023": 2950, "FY2022": 2950, "FY2021": 2950}),
    ("DATA", "Retained earnings",
     {"FY2025": 231833, "FY2024": 294299, "FY2023": 272711, "FY2022": 250226, "FY2021": 501095}),
    ("TOTAL", "Total equity",
     {"FY2025": 334783, "FY2024": 397249, "FY2023": 375661, "FY2022": 353176, "FY2021": 604045}),
    ("TOTAL", "Total liabilities and equity",
     {"FY2025": 5374808, "FY2024": 5580546, "FY2023": 5429710, "FY2022": 5718014, "FY2021": 5167480}),
]

bw.add_balance_sheet_sheet(
    title="Cater Allen Limited — Balance Sheet",
    subtitle="Entity basis, £'000. No customer loans in any year - see Asset Quality sheet. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=80,
    source_height=340,
    unit_suffix=" (£'000)",
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income",
     {"FY2025": 236408, "FY2024": 291425, "FY2023": 259964, "FY2022": 102326, "FY2021": 57544}),
    ("DATA", "Interest expense and similar charges",
     {"FY2025": -87134, "FY2024": -94933, "FY2023": -66912, "FY2022": -14546, "FY2021": -3162}),
    ("TOTAL", "Net interest income",
     {"FY2025": 149274, "FY2024": 196492, "FY2023": 193052, "FY2022": 87780, "FY2021": 54382}),
    ("DATA", "Fee and commission income", {"FY2025": 2487, "FY2024": 3036, "FY2023": 2666, "FY2022": 3348, "FY2021": 3147}),
    ("DATA", "Fee and commission expense",
     {"FY2025": -4949, "FY2024": -4369, "FY2023": -2530, "FY2022": -1811, "FY2021": -2113}),
    ("TOTAL", "Net fee and commission income/(expense)",
     {"FY2025": -2462, "FY2024": -1333, "FY2023": 136, "FY2022": 1537, "FY2021": 1034}),
    ("DATA", "Other operating result", {"FY2021": 479}),
    ("TOTAL", "Total income",
     {"FY2025": 146812, "FY2024": 195159, "FY2023": 193188, "FY2022": 89317, "FY2021": 55895}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Operating expenses",
     {"FY2025": -25236, "FY2024": -23506, "FY2023": -20754, "FY2022": -19105, "FY2021": -13632}),
    ("DATA", "Amortisation of intangible assets", {"FY2024": -2771, "FY2023": -2905, "FY2022": -2905, "FY2021": -2905}),
    ("TOTAL", "Profit before tax",
     {"FY2025": 121576, "FY2024": 168882, "FY2023": 169529, "FY2022": 67307, "FY2021": 39358}),
    ("DATA", "Tax on profit",
     {"FY2025": -34042, "FY2024": -47294, "FY2023": -47044, "FY2022": -18176, "FY2021": -10623}),
    ("TOTAL", "Profit for the year after tax",
     {"FY2025": 87534, "FY2024": 121588, "FY2023": 122485, "FY2022": 49131, "FY2021": 28735}),
    ("TOTAL", "Total comprehensive income for the year, net of tax",
     {"FY2025": 87534, "FY2024": 121588, "FY2023": 122485, "FY2022": 49131, "FY2021": 28735}),
]

bw.add_income_statement_sheet(
    title="Cater Allen Limited — Profit & Loss",
    subtitle="Entity basis, £'000. No OCI in any year - profit for the year equals total comprehensive income "
              "every year (per the Company's own disclosure). See source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=80,
    source_height=340,
    unit_suffix=" (£'000)",
)

equity_headers = ["Share capital", "Share premium", "Retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "At 1 January 2021", (100000, 2950, 472360, 575310)),
    ("DATA", "Profit and total comprehensive income for the year", (None, None, 28735, 28735)),
    ("TOTAL", "At 31 December 2021", (100000, 2950, 501095, 604045)),
    ("DATA", "Dividend paid", (None, None, -300000, -300000)),
    ("DATA", "Profit and total comprehensive income for the year", (None, None, 49131, 49131)),
    ("TOTAL", "At 31 December 2022", (100000, 2950, 250226, 353176)),
    ("DATA", "Dividend paid", (None, None, -100000, -100000)),
    ("DATA", "Profit and total comprehensive income for the year", (None, None, 122485, 122485)),
    ("TOTAL", "At 31 December 2023", (100000, 2950, 272711, 375661)),
    ("DATA", "Dividend paid", (None, None, -100000, -100000)),
    ("DATA", "Profit and total comprehensive income for the year", (None, None, 121588, 121588)),
    ("TOTAL", "At 31 December 2024", (100000, 2950, 294299, 397249)),
    ("DATA", "Dividend paid", (None, None, -150000, -150000)),
    ("DATA", "Profit and total comprehensive income for the year", (None, None, 87534, 87534)),
    ("TOTAL", "At 31 December 2025", (100000, 2950, 231833, 334783)),
]

bw.add_equity_changes_sheet(
    title="Cater Allen Limited — Statement of Changes in Equity",
    subtitle="Entity basis, £'000, chronological (oldest to newest). See source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=340,
)

bw.add_cash_flow_sheet(
    title="Cater Allen Limited — Cash Flow Statement",
    subtitle="Entity basis, £'000. FY2025 not applicable — FRS 101 cash-flow exemption newly taken. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=320,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    STATEMENTS_SOURCES + "\n\n"
    "ASSET QUALITY NOTE: Cater Allen Limited holds no loans and advances to customers in any "
    "year (see Balance Sheet - 'Loans and advances to customers' is nil every year 2021-2025). "
    "Its financial assets are entirely intercompany placements with, and cash held in accounts "
    "operated by, Santander UK plc. Per the Company's own Note 1 'Impairment of financial "
    "assets' (confirmed identically worded in the FY2025, FY2024 and FY2023 filings), expected "
    "credit losses are assessed on these balances using Santander UK plc's own net asset value "
    "and credit ratings, and 'because of these and given the intercompany nature, any "
    "probability of default and loss given default is deemed to be nil and thus no ECL is "
    "recognised over these balances' - with no write-offs in any year reviewed. This is a "
    "genuine structural feature of a deposit-taking bank with no lending book, not a disclosure "
    "gap."
)

bw.add_asset_quality_sheet(
    title="Cater Allen Limited — Asset Quality",
    subtitle="Entity basis, £'000. No loan book; ECL nil in all years. See source note at bottom.",
    rows=[
        ("DATA", "Loans and advances to customers", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("DATA", "Expected credit loss (ECL) allowance on financial assets at amortised cost",
         {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("DATA", "Write-offs during the year", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=80,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 / capital metric sheets
# ---------------------------------------------------------------
CET1_CAPITAL = {"FY2025": 217373, "FY2024": 246095, "FY2023": 220848, "FY2022": 268414}
CET1_RATIO = {"FY2025": "78.20%", "FY2024": "98.74%", "FY2023": "122.8%", "FY2022": "246.5%"}
RWA_CALC = {"FY2025": 277971, "FY2024": 249235, "FY2023": 179844, "FY2022": 108890}

NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed. Cater Allen's Annual Report discloses only CET1 capital ratio and "
    "Total Tier 1 Capital/Total Capital Resources (identical, since no AT1/Tier 2 instruments "
    "exist) via its Strategic Report KPI table and Capital risk note - no Leverage Ratio, LCR, "
    "NSFR, or MREL figures are disclosed at this entity level in any of the 4 years reviewed. "
    "No standalone Pillar 3 document exists; liquidity/capital management is described only "
    "narratively (managed centrally with Santander UK plc as part of the RFB Domestic "
    "Liquidity Sub-Group and the RFB Sub-Group Capital Support Deed)."
)

CAPITAL_SOURCES = (
    "Sources - Cater Allen Limited's own Annual Report, Strategic Report KPI table and Risk "
    "Review 'Capital risk' section (Capital table), GBP'000 except ratios:\n"
    f"FY2025: Annual Report and Financial Statements 2025, p.2 (KPIs) and p.12 (Capital) - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.2 (KPIs) and p.13 (Capital) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.2 (KPIs) and p.15 (Capital) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2023, p.2 (KPI comparative) and p.15 "
    f"(Capital table 2022 comparative) - {AR2023_URL}\n\n"
    "CET1 Capital = Tier 1 Capital = Total Capital every year - the Company's Tier 1 capital "
    "consists of shareholders' equity, share premium and audited prior-year profits (adjusted "
    "for foreseeable charges/dividends); no AT1 or Tier 2 instruments exist. FY2021 is "
    "genuinely not disclosed - the FY2021 Annual Report's KPI table and financial-statement "
    "notes predate this project's window's capital-ratio disclosure format and contain no "
    "capital-adequacy figures of any kind."
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, CAPITAL_SOURCES, note=note, first_col_width=52, source_height=220)


metric("CET1 Capital", "£'000", [("Total Capital Resources (= CET1 Capital)", CET1_CAPITAL)])
metric("CET1 Ratio", "%", [("CET1 capital ratio", CET1_RATIO)])
metric("Tier 1 Capital", "£'000 (= CET1 Capital; no AT1 instruments)", [("Total Tier 1 Capital Resources", CET1_CAPITAL)])
metric("Tier 1 Ratio", "%", [("CET1 capital ratio (= Tier 1 Ratio; no AT1 instruments)", CET1_RATIO)])
metric("Total Capital", "£'000 (= CET1 Capital; no Tier 2 instruments)", [("Total Capital Resources", CET1_CAPITAL)])
metric("Total Capital Ratio", "%", [("CET1 capital ratio (= Total Capital Ratio; no AT1/Tier 2 instruments)", CET1_RATIO)])
metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets", RWA_CALC)],
    note="CALCULATED, not directly disclosed - derived as Total Capital Resources ÷ CET1 "
         "capital ratio for each year. No RWA figure appears in any source reviewed.",
)

bw.add_rwa_breakdown_sheet(
    title="Cater Allen Limited — RWA Breakdown",
    subtitle="Not publicly disclosed. See source note at bottom.",
    rows=[("DATA", "Not publicly disclosed", {})],
    sources_text=CAPITAL_SOURCES + "\n\n" + NOT_DISCLOSED_NOTE,
    first_col_width=54,
    source_height=280,
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    CAPITAL_SOURCES,
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets",
         {"FY2025": 5374808, "FY2024": 5580546, "FY2023": 5429710, "FY2022": 5718014, "FY2021": 5167480}),
        ("Loans and advances to banks",
         {"FY2025": 5297136, "FY2024": 5540507, "FY2023": 5383852, "FY2022": 5671848, "FY2021": 5128808}),
        ("Customer accounts",
         {"FY2025": 4964597, "FY2024": 5112126, "FY2023": 4978130, "FY2022": 5326931, "FY2021": 4544224}),
        ("Total equity",
         {"FY2025": 334783, "FY2024": 397249, "FY2023": 375661, "FY2022": 353176, "FY2021": 604045}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income",
         {"FY2025": 146812, "FY2024": 195159, "FY2023": 193188, "FY2022": 89317, "FY2021": 55895}),
        ("Operating expenses",
         {"FY2025": -25236, "FY2024": -23506, "FY2023": -20754, "FY2022": -19105, "FY2021": -13632}),
        ("Profit for the year after tax",
         {"FY2025": 87534, "FY2024": 121588, "FY2023": 122485, "FY2022": 49131, "FY2021": 28735}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity",
         {"FY2025": 397249, "FY2024": 375661, "FY2023": 353176, "FY2022": 604045, "FY2021": 575310}),
        ("Total comprehensive income for the year",
         {"FY2025": 87534, "FY2024": 121588, "FY2023": 122485, "FY2022": 49131, "FY2021": 28735}),
        ("Other equity movements, net",
         {"FY2025": -150000, "FY2024": -100000, "FY2023": -100000, "FY2022": -300000}),
        ("Closing equity",
         {"FY2025": 334783, "FY2024": 397249, "FY2023": 375661, "FY2022": 353176, "FY2021": 604045}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash (used in)/generated from operating activities",
         {"FY2024": 258187, "FY2023": -184058, "FY2022": 832547, "FY2021": -200379}),
        ("Cash used in investing activities", {"FY2024": 0, "FY2023": -393, "FY2022": 0}),
        ("Closing cash and cash equivalents",
         {"FY2024": 5540507, "FY2023": 5383852, "FY2022": 5671848, "FY2021": 5128808}),
    ],
    cash_flow_unit=" (£'000)",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", CET1_RATIO),
    ],
)

bw.save("/Users/armaan/code/katalysis/banks/CATER ALLEN FINANCIALS.xlsx")
