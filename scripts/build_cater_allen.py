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

# Santander publishes Cater Allen's FY2022-FY2024 reports on its own site as
# full text-layer PDFs. These are the same documents as the Companies House
# filings above but machine-readable, so every FY2022-FY2024 figure in this
# script has now been re-verified against extracted text rather than a page
# image. Cite these in preference; the Companies House URLs remain the only
# route to FY2021 and FY2025, which Santander does not host.
SANT2022_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/2022_cater_allen_limited_annual_report.pdf"
SANT2023_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/cater_allen_limited.pdf"
SANT2024_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/Cater%20Allen%20Limited%202024%20-%20Signed.pdf"

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
    "PRESENTATION FORMAT NOTE: FY2021's face Cash Flow Statement (p.14) itself shows only a "
    "single aggregate operating total, but the full working-capital breakdown behind that total "
    "IS disclosed in Note 24 'Cashflow statement' (p.35) - a prior text-only pass on this "
    "workbook had cited p.35 as a source but, unable to read the scanned page image, incorrectly "
    "left the breakdown rows blank and claimed no breakdown existed. A visual re-check of p.35 "
    "found the full reconciliation and it has now been transcribed below; every FY2021 line "
    "reconciles exactly (trading activities 41,774 + working-capital changes -242,153 = "
    "-200,379, matching the face statement's total precisely). FY2021 has no investing or "
    "financing activities section - that part of the presentation difference vs FY2022-FY2024 "
    "is genuine, confirmed on both p.14 and p.35.\n\n"
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
    f"FY2025: NEVER PUBLISHED (not 'unreached') - no Statement of Cash Flows exists in the FY2025 "
    f"filing, for FY2025 or for its FY2024 comparative, because the FRS 101 exemption from IAS 7 "
    f"was newly taken this year. Evidence: Annual Report and Financial Statements 2025, printed "
    f"p.29 = PDF p.30, Note 1 'Accounting policies', sub-heading 'Basis of preparation', which "
    f"reads verbatim: \"These financial statements are presented with the benefit of the "
    f"disclosure exemptions permitted by FRS 101 with regards to: IAS 7, 'Statement of cash "
    f"flows' and paragraphs 10(d) (statement of cash flows), and 111 (statement of cash flows "
    f"information)\". The same note states the cause: \"during the year, the Company has undergone "
    f"transition from reporting under UK-adopted International Accounting Standards to FRS 101\" - "
    f"i.e. the exemption only became available on that transition, which is why FY2021-FY2024 are "
    f"full cash flow statements and FY2025 is not. Retrieval and search method (this filing is "
    f"image-only - 43 characters of text layer across 43 pages, so every keyword search against "
    f"the PDF text returns nothing regardless of content): fetched with curl -L (HTTP 200, "
    f"Content-Type application/pdf, %PDF-1.1 magic bytes, 2,050,119 bytes), rendered with "
    f"pdftoppm -r 200 -png and OCR'd with tesseract; richness control on the OCR text returned "
    f"1,893 hits for 'the'. Searched terms: 'cash flow', 'statement of cash flows', 'IAS 7', "
    f"'FRS 101', 'exemption'. 'cash flow' hits 8 of 43 pages and every hit is discursive "
    f"(contractual-maturity table p.11; going-concern and auditors' report p.23; IFRS 9 "
    f"business-model policy pp.32-33; cash-generating-unit impairment projections pp.34, 39, 40). "
    f"The only primary-statement headings in the document are Balance Sheet and Statement of "
    f"Changes in Equity. - {AR2025_URL}\n\n"
    + ENTITY_NOTE
)

rows = [
    # GAP-FILL (2026-09-18): the FY2025 column previously held NO cell at all, so a
    # reader (and audit_gaps.py) could not tell "the exemption was taken" from
    # "nobody has looked yet" - even though the finding was already complete and
    # quoted in ENTITY_NOTE/CASH_FLOW_SOURCES. The exemption now appears IN the
    # column, in one labelled row, the same treatment already applied to Atom Bank
    # and AIB Group (UK). No column is suppressed.
    #
    # RE-PROVEN 2026-09-18 from the FY2025 filing's OWN basis-of-preparation note
    # (printed p.29 = PDF p.30, Note 1 'Accounting policies', 'Basis of
    # preparation'). The filing is image-only - 43 characters of text layer across
    # 43 pages - so it was rendered at 200dpi and OCR'd before the wording could be
    # read at all. Verbatim: "These financial statements are presented with the
    # benefit of the disclosure exemptions permitted by FRS 101 with regards to:
    # IAS 7, 'Statement of cash flows' and paragraphs 10(d) (statement of cash
    # flows), and 111 (statement of cash flows information)".
    #
    # WHY IT IS NEW IN THE FINAL YEAR - the same note gives the mechanism, which
    # was not previously recorded here: "during the year, the Company has undergone
    # transition from reporting under UK-adopted International Accounting Standards
    # to FRS 101". The exemption did not become available until that transition, so
    # FY2021-FY2024 are genuinely full cash flow statements and only FY2025 is not.
    #
    # All 43 OCR'd pages were searched for "cash flow": 8 pages hit and every hit is
    # discursive (contractual-maturity table p.11, going-concern and audit report
    # p.23, IFRS 9 business-model policy pp.32-33, CGU impairment projections
    # pp.34/39/40). The only primary-statement headings in the filing are Balance
    # Sheet and Statement of Changes in Equity. There is no Statement of Cash Flows
    # for FY2025 nor for its FY2024 comparative.
    ("SECTION", "FY2025 — no Cash Flow Statement is published; the FRS 101 exemption from IAS 7 was newly taken this year (see note below)", {}),
    ("DATA", "Statement of Cash Flows for the year",
     {"FY2025": "Not published - FRS reduced-disclosure cash-flow exemption taken on transition (see note)"}),
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2024": 168882, "FY2023": 169529, "FY2022": 67307, "FY2021": 39358}),
    ("DATA", "Effect of foreign exchange rates on loans and advances to banks",
     {"FY2024": -81, "FY2023": 3545, "FY2022": -10493}),
    ("DATA", "Amortisation of intangible assets", {"FY2024": 2771, "FY2023": 2905, "FY2022": 2905, "FY2021": 2905}),
    ("DATA", "Impairment reversal", {"FY2022": -35, "FY2021": -10}),
    ("DATA", "Finance write-backs", {"FY2021": -479}),
    ("TOTAL", "Net cash flow from trading activities", {"FY2024": 171572, "FY2023": 175979, "FY2022": 59684, "FY2021": 41774}),
    ("DATA", "Increase in items in course of transmission by other banks", {"FY2021": 1907}),
    ("DATA", "Decrease in loans and advances to customers", {"FY2022": 35, "FY2021": 10}),
    ("DATA", "Decrease/(increase) in other assets", {"FY2024": 3044, "FY2023": -2207, "FY2022": -10406, "FY2021": -76}),
    ("DATA", "Decrease in derivative financial liabilities", {"FY2021": -10}),
    ("DATA", "Decrease in financial assets at fair value through profit or loss", {"FY2021": 2572}),
    ("DATA", "Increase/(decrease) in customer accounts", {"FY2024": 135483, "FY2023": -348801, "FY2022": 782202, "FY2021": -232334}),
    ("DATA", "Increase/(decrease) in deposits by banks", {"FY2024": 2820, "FY2023": 2577, "FY2022": -1348, "FY2021": -2347}),
    ("DATA", "Increase/(decrease) in amounts due to other group companies", {"FY2024": 1736, "FY2023": 2073, "FY2022": 4061, "FY2021": -1140}),
    ("DATA", "(Decrease)/increase in other liabilities", {"FY2024": -9420, "FY2023": 4491, "FY2022": 8942, "FY2021": 475}),
    ("DATA", "Settlement to Santander UK plc in respect of Corporation Tax",
     {"FY2024": -47048, "FY2023": -18170, "FY2022": -10623, "FY2021": -11210}),
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
CET1_CAPITAL = {"FY2025": 217373, "FY2024": 246095, "FY2023": 220848, "FY2022": 268414, "FY2021": 537042}
CET1_RATIO = {"FY2025": "78.20%", "FY2024": "98.74%", "FY2023": "122.8%", "FY2022": "246.5%"}
# WITHDRAWN 2026-09-16 on the user's decision. These four values were never
# disclosed by the bank: each was Total Capital Resources DIVIDED BY that year's
# CET1 ratio. They are retained here, unused, ONLY as the record of what was
# removed and of the arithmetic that produced them - do NOT re-wire them into
# the Total RWAs sheet, which now reads "Not publicly disclosed".
#   FY2025 217,373/0.7820 = 277,971    FY2024 246,095/0.9874 = 249,235
#   FY2023 220,848/1.2280 = 179,844    FY2022 268,414/2.4650 = 108,890
RWA_CALC_WITHDRAWN = {"FY2025": 277971, "FY2024": 249235, "FY2023": 179844, "FY2022": 108890}  # noqa: F841
# GA-020 (2026-09-19): bare statements reclassified on the evidence already cited in this
# script (FY2021-FY2025 Annual Reports; Santander UK ACRMD FY2023-FY2025; BoE waivers
# register row for FRN 178737), re-checked against the text-layer FY2022-FY2024 reports:
# 'leverage' and 'MREL' occur only as "continues to be in excess of ... minimum leverage
# requirements and ... MREL" and "subject to ... leverage rules" at RFB sub-group level;
# liquidity is managed through the RFB Domestic Liquidity Sub-Group (FY2024 AR, Liquidity risk).
RWA_NOT_DISCLOSED = {y: ("Not published – no RWA amount in Cater Allen ARs FY2021–FY2025 (Capital adequacy table is a "
                         "Tier 1 build-up only); Santander UK ACRMD FY2023–25 carries no Cater Allen figure.") for y in YEARS}
GA020_ST = {
    "Leverage Ratio": ("Not published – Cater Allen ARs FY2021–FY2025 print no leverage ratio, only that it is 'in excess "
                       "of ... minimum leverage requirements' (leverage rules apply at Santander UK RFB sub-group level)."),
    "LCR": dict({y: ("Not applicable – liquidity requirements met at RFB Domestic Liquidity Sub-group level (BoE waivers "
                     "register, FRN 178737, 'DoLSub Permission', Ru 2.2, from 01/01/2022; AR Liquidity risk section).")
                 for y in ["FY2025", "FY2024", "FY2023", "FY2022"]},
                FY2021="Not published – no LCR figure in the FY2021 or FY2022 Annual Report (liquidity described narratively only)."),
    "NSFR": dict({y: ("Not applicable – liquidity requirements met at RFB Domestic Liquidity Sub-group level (BoE waivers "
                      "register, FRN 178737, 'DoLSub Permission', Ru 2.2, from 01/01/2022; AR Liquidity risk section).")
                  for y in ["FY2025", "FY2024", "FY2023", "FY2022"]},
                 FY2021="Not published – no NSFR figure in the FY2021 or FY2022 Annual Report (liquidity described narratively only)."),
    "MREL Ratio": ("Not published – no MREL figure in Cater Allen ARs FY2021–FY2025 (FY2023/24 say only it is 'in excess "
                   "of ... MREL') or in Santander UK's ACRMD FY2023–25."),
}

NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed. Cater Allen's Annual Report discloses only CET1 capital ratio and "
    "Total Tier 1 Capital/Total Capital Resources (identical, since no AT1/Tier 2 instruments "
    "exist) via its Strategic Report KPI table and Capital risk note - no Leverage Ratio, LCR, "
    "NSFR, or MREL figures are disclosed at this entity level in any of the 5 years reviewed. "
    "FY2021's CET1 ratio and RWA are not disclosed (only the absolute capital figure is); CET1 "
    "ratios are available FY2022 onward only, because the ratio first entered the KPI table in "
    "the FY2023 Annual Report and that report's comparative column reaches back only to FY2022 "
    "- see the Total RWAs and CET1 Ratio source notes for the full proof of absence. "
    "No standalone Pillar 3 document exists; liquidity/capital management is described only "
    "narratively (managed centrally with Santander UK plc as part of the RFB Domestic "
    "Liquidity Sub-Group and the RFB Sub-Group Capital Support Deed).\n\n"
    "RE-VERIFIED 2026-09-12: independently re-downloaded and OCR'd the live FY2025 Annual Report "
    "(scanned, no text layer) and re-read the Risk Review's 'Capital' section (p.12) in full - "
    "confirmed it still discloses only the Tier 1 capital build-up table (Total Tier 1 Capital, "
    "Deductions, Total Capital Resources), with no risk-weighted-assets figure anywhere on that "
    "page or in the surrounding Capital risk narrative. No standalone Pillar 3 document found on "
    "the bank's own site or in the Wayback archive. The non-disclosure is confirmed current."
)

CAPITAL_SOURCES = (
    "Sources - Cater Allen Limited's own Annual Report, Strategic Report KPI table and Risk "
    "Review 'Capital risk' section (Capital table), GBP'000 except ratios:\n"
    f"FY2025: Annual Report and Financial Statements 2025, p.2 (KPIs) and p.12 (Capital) - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.2 (KPIs) and p.13 (Capital) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.2 (KPIs) and p.15 (Capital) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, Risk Review 'Capital adequacy' table "
    f"(Total Capital Resources 268,414) - {SANT2022_URL}; CET1 ratio 246.5% from Annual Report "
    f"and Financial Statements 2023, p.2 (KPI 2022 comparative) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2022, Risk Review 'Capital adequacy' table, "
    f"2021 comparative column (Total Tier 1 Capital 575,515 less Deductions 38,473 = Total "
    f"Capital Resources 537,042) - {SANT2022_URL}; also Annual Report and Financial Statements "
    f"2021, p.27 (Capital adequacy note) - {AR2021_URL}\n\n"
    "TEXT-LAYER RE-VERIFICATION 2026-09-15: FY2022, FY2023 and FY2024 were re-read from "
    "Santander's own text-layer PDFs (see SANT*_URL above) rather than the scanned Companies "
    "House images. Every capital figure in this script reconciles exactly against the extracted "
    "text, and each year's table is corroborated by the following year's comparative column: "
    "FY2021 537,042 and FY2022 268,414 both appear in the FY2022 report; FY2022 268,414 and "
    "FY2023 220,848 both appear in the FY2023 report; FY2023 220,848 and FY2024 246,095 both "
    "appear in the FY2024 report. The CET1 ratios 122.8%/246.5% (FY2023 report KPI table) and "
    "98.74%/122.80% (FY2024 report KPI table) likewise overlap consistently.\n\n"
    "CET1 Capital = Tier 1 Capital = Total Capital every year - this is a disclosed identity, "
    "not an inference: the Capital adequacy table prints 'Total Capital Resources (Tier 1)' and "
    "'Total Capital Resources' as the same number in every year, and the footnote states Tier 1 "
    "capital consists of shareholders' equity, share premium and audited prior-year profits "
    "(adjusted for foreseeable charges/dividends). No AT1 or Tier 2 instruments exist.\n\n"
    "The CET1 ratio is verified as a genuine CRR ratio, not a capital-cover measure: the Capital "
    "risk note states 'The main metrics used to measure capital risk are CET1 capital ratio and "
    "total capital ratio' and describes Pillar 1, Pillar 2A, the ICAAP and the PRA. The very "
    "high values are plausible for this balance sheet - customer loans are nil in every year and "
    "the intercompany placements that make up the asset base are risk-weighted at 0%.\n\n"
    "FY2021 CET1 RATIO - PROVEN ABSENT, not an unresearched gap. The CET1 capital ratio entered "
    "Cater Allen's KPI table only with the FY2023 Annual Report, whose comparative column reaches "
    "back just one year, to FY2022. The FY2022 Annual Report's own KPI table was checked line by "
    "line and contains no CET1 ratio row at all (its KPIs are Total volume of accounts, New "
    "Customer Account Openings, Customer Liabilities, Net Operating Income, Operating expenses "
    "including amortisation, Cost-Income Ratio and Customer Complaints), and its Capital "
    "adequacy table gives absolute capital only, with no ratio and no RWA. There is therefore no "
    "published document in which an FY2021 CET1 ratio for this entity appears. Santander's site "
    "hosts no FY2021 or FY2020 report (both filename patterns return 404), and an unfiltered "
    "Wayback CDX sweep of santander.co.uk returns only the three FY2022-FY2024 PDFs cited above."
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, CAPITAL_SOURCES, note=note, first_col_width=52, source_height=220)


KM1_SOURCES = (
    "Sources - UK KM1 'Key metrics' template, Cater Allen Limited (FRN 178737, company 00383032):\n"
    "NOT APPLICABLE AT THIS ENTITY LEVEL. Cater Allen publishes no Pillar 3 document of its own, and its "
    "parent's group disclosure carries no Cater Allen capital block. Established 2026-09-16 (KM1-009) on "
    "affirmative evidence from three independent directions, not on a failed search.\n\n"
    "1. THE ENTITY'S OWN REPORT. Cater Allen Limited's Annual Report and Financial Statements 2024 "
    "(42 pages, text-native) contains ZERO occurrences of 'Pillar 3'. Richness control on the same extraction: "
    "'capital' 76 hits, 'capital ratio' 3, 'leverage' 6, so the zero is a fact about the document rather than "
    "about the extraction (map rule 15). There is no KM1 template, and no table carrying the template's row "
    "set under another name (map rule 8).\n\n"
    "2. THE PARENT'S DISCLOSURE - map rule 18, checked and answered. Santander UK publishes no document titled "
    "'Pillar 3'; its equivalent is the Additional Capital and Risk Management Disclosures (ACRMD). Three "
    "editions were read in full - FY2023, FY2024 and FY2025, each 80 pages, 'capital' richness 258 / 252 / 286. "
    "Each mentions Cater Allen exactly TWICE, and in all three it is the same single sentence, about liquidity "
    "rather than capital: Santander UK plc 'and its subsidiary Cater Allen Limited form the RFB Domestic "
    "Liquidity Sub-group (the RFB DoLSub), which allows the entities to collectively meet' their liquidity "
    "requirements. No Cater Allen CET1, Tier 1, total capital, RWA, leverage, LCR or NSFR figure appears in any "
    "edition. Documents: 2025SantanderUKACRMD.pdf, 'ACRMD FINAL_Dec 24.pdf' and santander_uk_acrmd_2023.pdf, "
    "all under https://assets.santandermedia.com/ , listed from Santander UK's own investor-relations page for "
    "Santander UK Group Holdings plc.\n\n"
    "3. WHICH REGIME THE PARENT FILES UNDER. The ACRMD states its own scope: 'This document contains "
    "disclosures required under UK CRR for the Company as a large subsidiary of an EU parent undertaking' - "
    "i.e. Santander UK Group Holdings plc consolidated, as a large subsidiary of Banco Santander SA. That duty "
    "attaches to the UK holding company, not to each ring-fenced subsidiary beneath it, so no Cater Allen block "
    "is required and none is published. This is the same shape as AIB Group (UK): the parent's regime decides "
    "whether an absence is a finding or a gap, and here it is a finding.\n\n"
    "LIQUIDITY IS SUBSUMED, NOT OMITTED. The DoLSub sentence above is corroborated by the Bank of England "
    "consolidated waivers register (downloaded 2026-09-16), which carries for FRN 178737 a 'DoLSub Permission / "
    "Requirements in relation to liquidity / Ru 2.2' running 01/01/2022-01/02/2027. Cater Allen's LCR and NSFR "
    "are therefore managed and reported at RFB DoLSub level, which explains the absence of KM1 rows 15-20 at "
    "this entity rather than merely recording it.\n\n"
    "SDDT - EXPLICIT NEGATIVE, AND A TRAP WORTH NAMING. Cater Allen holds NO SDDT waiver. The register does "
    "list a row for FRN 178737 whose sub-rule number reads 'Ru 3.1(1), 4.1(1)', but its rule description is "
    "'Requirements to carry out adequate assessment of resolution preparations' - a RESOLUTION rule 3.1, not "
    "Rule 3.1 of the SDDT Regime - General Application Part. Matching on the sub-rule number alone would "
    "manufacture an exemption this firm does not have. Its other rows are ring-fenced-bodies rules 4.1/4.2/4.4/"
    "5.4/6.4/8.1 (01/01/2024-31/12/2026), Core Large Exposures (Ar 113(6), Ar 429a(1)) and an IRB model "
    "permission from 01/05/2026. The absence of a KM1 is not an SDDT exemption.\n\n"
    "ENTITY BASIS. Santander UK Group Holdings plc consolidated figures are deliberately NOT substituted for "
    "Cater Allen Limited. A group consolidated KM1 covers Santander UK plc and every other subsidiary; "
    "presenting it as this entity's own key metrics would be false at the entity level.\n\n"
    "Also recorded: Cater Allen is absent entirely from research/km1_inventory.jsonl - it has no slug among the "
    "114 in that file, so the survey never reached it and no inventory verdict exists for this bank either way."
)

bw.add_km1_sheet(
    title="Cater Allen Limited - KM1 Key Metrics",
    subtitle="Not applicable - the Bank publishes no Pillar 3 of its own, and Santander UK's group ACRMD "
             "carries no Cater Allen capital block (liquidity is reported at RFB DoLSub level)",
    rows=[("DATA", "UK KM1 'Key metrics' template", {y: ("Not applicable – no own Pillar 3: disclosure duty sits with Santander "
                                                          "UK Group Holdings (ACRMD scope: 'large subsidiary of an EU parent'); "
                                                          "ACRMD FY2023–25 has no Cater Allen block.") for y in YEARS})],
    sources_text=KM1_SOURCES,
    first_col_width=76,
    source_height=560,
    years=YEARS,
)

metric("CET1 Capital", "£'000", [("Total Capital Resources (= CET1 Capital)", CET1_CAPITAL)])
metric("CET1 Ratio", "%", [("CET1 capital ratio", CET1_RATIO)])
metric("Tier 1 Capital", "£'000 (= CET1 Capital; no AT1 instruments)", [("Total Tier 1 Capital Resources", CET1_CAPITAL)])
metric("Tier 1 Ratio", "%", [("CET1 capital ratio (= Tier 1 Ratio; no AT1 instruments)", CET1_RATIO)])
metric("Total Capital", "£'000 (= CET1 Capital; no Tier 2 instruments)", [("Total Capital Resources", CET1_CAPITAL)])
metric("Total Capital Ratio", "%", [("CET1 capital ratio (= Total Capital Ratio; no AT1/Tier 2 instruments)", CET1_RATIO)])
metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets", RWA_NOT_DISCLOSED)],
    note="NOT PUBLICLY DISCLOSED. Cater Allen Limited does not publish a risk-weighted-assets "
         "figure - aggregate or by risk category - in any source reviewed, for any year. Confirmed "
         "against the text-layer FY2022, FY2023 and FY2024 Annual Reports, whose Capital adequacy "
         "tables carry only the Tier 1 build-up (Total Tier 1 Capital, Deductions, Total Capital "
         "Resources).\n\n"
         "WITHDRAWAL RECORD (2026-09-16). This sheet previously carried four populated values - "
         "FY2025 277,971; FY2024 249,235; FY2023 179,844; FY2022 108,890 - which were NOT disclosed "
         "data. Each was back-solved as Total Capital Resources divided by that year's CET1 ratio "
         "(e.g. FY2025 217,373/0.7820). They were withdrawn on the project owner's decision because "
         "deriving RWAs from capital divided by a ratio breaches this project's rule against "
         "presenting a computed figure as a disclosure - the same pattern already withdrawn from "
         "Bank Mandiri (Europe) and Alpha Bank London on 2026-09-15.\n\n"
         "Two properties of the withdrawn series show why it could not be relied on: it was only as "
         "precise as the rounded ratio it divided by (the FY2023 ratio is published to four "
         "significant figures, 122.8%, giving the implied RWA a roughly +/-0.05% band), and it moved "
         "in the OPPOSITE direction to capital in three of the four years purely as an artefact of "
         "that division. The arithmetic is preserved in this build script as RWA_CALC_WITHDRAWN so "
         "the removal stays auditable.",
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
    statements=GA020_ST,
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
