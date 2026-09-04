import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/11379025/filing-history/MzUxNzk5NTMwNmFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/11379025/filing-history/MzQyMjE2MDUwOWFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/11379025/filing-history/MzM1Mjk5ODYxMGFkaXF6a2N4/document?format=pdf&download=0"

P3_2024_URL = "https://www.triodos.co.uk/binaries/content/assets/tbuk/press-and-media-page/triodos-bank-uk-2024-pillar-3.pdf"
P3_2023_URL = "https://www.triodos.co.uk/binaries/content/assets/tbuk/press-and-media-page/triodos-bank-uk-2023-pillar-3-report.pdf"
P3_2022_URL = "https://www.triodos.co.uk/binaries/content/assets/tbuk/press-and-media-page/triodos-bank-uk-2022-pillar-3-report.pdf"
P3_2021_URL = "https://www.triodos.co.uk/downloads/triodos-bank-uk-2021-pillar-3-report?id=9efebf75e4f1"

ENTITY_NOTE = (
    "ENTITY NOTE: Triodos Bank UK Limited (TBUK, company number 11379025, FRN 817008) is a wholly owned "
    "subsidiary of Triodos Bank N.V. (the Netherlands), established in 2019 to continue Triodos Bank's UK "
    "operations (previously run as a UK branch of Triodos Bank N.V. since 1995) via a Part VII transfer. Although "
    "TBUK's own accounts are exempt under s.401 of the Companies Act 2006 from preparing CONSOLIDATED financial "
    "statements (it and its subsidiary undertaking are fully consolidated into Triodos Bank N.V.'s own group "
    "accounts), TBUK's own entity-level accounts DO include a full Statement of Cash Flows every year - unlike "
    "several other single-parent foreign subsidiary banks in this series (e.g. ICICI Bank UK, United Trust Bank), "
    "TBUK does not take the FRS 101/102 cash-flow-statement disclosure exemption. All figures below are TBUK's own "
    "entity-level (Company) results, in £, not Triodos Bank N.V. group figures. Companies House filings for all 5 "
    "years were fully scanned/image-only PDFs with no text layer; all figures were extracted via OCR (tesseract) "
    "and cross-verified visually against the rendered page images."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Triodos Bank UK Limited's own entity-level (Company) Statement of Cash Flows, £'000:\n"
    f"FY2025: Triodos Bank UK Limited Annual Report 2025 (Companies House filing, made up to 31 Dec 2025), p.57-58 "
    f"(Statement of cash flows for the year ended 31 December 2025) - {AR2025_URL}\n"
    f"FY2024: as reported in the FY2025 Annual Report's own FY2024 comparative column, same pages/source as above.\n"
    f"FY2023: Triodos Bank UK Limited Annual Report 2023 (Companies House filing, made up to 31 Dec 2023), p.76-77 "
    f"(Cash flow statement for the year ended 31 December 2023) - {AR2023_URL}\n"
    f"FY2022: as reported in the FY2023 Annual Report's own FY2022 comparative column, same pages/source as above.\n"
    f"FY2021: Triodos Bank UK Limited Annual Report 2021 (Companies House filing, made up to 31 Dec 2021), p.30-31 "
    f"(Cash flow statement for the year ended 31 December 2021) - {AR2021_URL}\n"
    "PRESENTATION NOTE: 'Cash flow from operating activities' is a two-level subtotal in every year's own "
    "statement - a 'Cash flow from business operations' subtotal (profit before tax + non-cash adjustments), "
    "followed by 'Changes in net operating assets' line items, with the final 'Cash flow from operating "
    "activities' total equal to the BUSINESS OPERATIONS SUBTOTAL PLUS the changes lines, not just the changes "
    "lines alone. verify_workbook.py's generic block-check will report a false-positive mismatch on this specific "
    "total for exactly this reason (it only sums the DATA rows since the immediately preceding TOTAL/SECTION) - "
    "this is expected and not a data error; every subtotal and total independently ties to source and was hand-"
    "verified. Some line items were relabelled or moved sections between report vintages (wording/sign-convention "
    "only, e.g. 'Increase in Expected Credit Losses' (FY2021) vs '(Decrease)/Increase in ECL on financial "
    "instruments' (FY2023) vs 'Decrease in ECL on financial instruments' (FY2025)) - unified onto a single row "
    "where the underlying line item is genuinely the same measure. One GENUINE structural change: 'increase in "
    "interest receivable on debt securities' moved from the INVESTING section (FY2021-FY2023 statements) to the "
    "OPERATING section (FY2024-FY2025 statements) - kept as two separate rows in their respective sections, "
    "exactly as each year's own statement presented it. Blank cells indicate that year's statement did not "
    "disclose/include that specific line at all; a printed '-' in the source was transcribed as 0 (an explicit "
    "nil disclosure, not a gap).\n\n"
    + ENTITY_NOTE
)


def p3_sources(pages="7-14"):
    return (
        "Sources - Triodos Bank UK Limited (TBUK) entity-level Pillar 3 disclosures:\n"
        f"FY2024: Triodos Bank UK Limited 2024 Pillar 3 Report, p.{pages} - {P3_2024_URL}\n"
        f"FY2023: Triodos Bank UK Limited 2023 Pillar 3 Report - {P3_2023_URL}\n"
        f"FY2022: Triodos Bank UK Limited 2022 Pillar 3 Report - {P3_2022_URL}\n"
        f"FY2021: Triodos Bank UK Limited 2021 Pillar 3 Report - {P3_2021_URL}\n"
        "FY2025: no standalone Pillar 3 report has been published yet as of this workbook's build date (2026-08-26) "
        "- the FY2025 Annual Report was only filed 28 Apr 2026 and TBUK's Pillar 3 report has historically followed "
        "several months after its Annual Report (e.g. the FY2024 edition above was published well after the "
        "FY2024 Annual Report). Where marked '(derived)' below, a FY2025 figure was calculated from Annual Report "
        "disclosures rather than transcribed from a Pillar 3 table, since no such table exists yet - see the "
        "sheet's own note.\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Triodos Bank UK Limited", years=YEARS, year_label=YEAR_LABEL, header_color="5A3E85")

# ---------------------------------------------------------------
# Statement sources shared by Balance Sheet / P&L / Statement of Changes in
# Equity. Balance Sheet: FY2025-FY2024 from AR2025 (p.55), FY2023-FY2022
# from AR2023 (p.73), FY2021 from AR2021 (p.28). P&L: FY2025-FY2024 from
# AR2025 (p.54), FY2023-FY2022 from AR2023 (p.72), FY2021 from AR2021
# (p.27). Statement of Changes in Equity: FY2024-FY2025 from AR2025 (p.56),
# FY2022-FY2023 from AR2023 (p.75), FY2021 from AR2021 (p.29). All figures
# TBUK entity-level (Company) basis, £'000, same OCR-extraction basis as
# ENTITY_NOTE describes for the rest of this workbook.
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - Triodos Bank UK Limited, entity-level (Company) financial statements, £'000:\n"
    f"FY2025/FY2024: Annual Report 2025 - Statement of comprehensive income p.54, Statement of financial "
    f"position p.55, Statement of changes in equity p.56 - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report 2023 - Statement of comprehensive income p.72, Balance sheet p.73, "
    f"Statement of changes in equity p.75 - {AR2023_URL}\n"
    f"FY2021: Annual Report 2021 - Statement of Comprehensive Income p.27, Balance sheet p.28, Statement of "
    f"changes in equity p.29 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nGENUINE SOURCE DISCREPANCY (not a transcription error, not forced to tie): TBUK's own AR2025 does "
    "not internally reconcile to the pound for FY2025. The Statement of comprehensive income states 'Profit "
    "and total comprehensive income' of £13,928k; the Statement of changes in equity separately states "
    "'Total profit and comprehensive income' of £13,930k for the same year (a £2k gap). Correspondingly, the "
    "Statement of changes in equity's own closing Retained earnings/Total equity for 31 December 2025 "
    "(£36,563k / £208,618k) does not exactly match the Statement of financial position's own Retained "
    "earnings/Total equity as at the same date (£36,567k / £208,622k) - a £4k gap. Both figures are "
    "reproduced here exactly as each statement states them; this sheet does not silently pick one or plug "
    "the difference. No such gap exists in FY2021-FY2024 - all four of those years tie to the pound across "
    "all three statements."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Statement of financial position). Total assets =
# Total liabilities + Total equity for every year. Total equity ties
# exactly to the Statement of Changes in Equity sheet's own closing
# balances for FY2021-FY2024; FY2025 has the £4k genuine source gap noted
# above (Balance Sheet's own Total equity, not the equity sheet's, is used
# as this workbook's primary FY2025 equity figure, consistent with the
# convention of preferring the balance sheet's own total elsewhere in this
# project).
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 269090, "FY2024": 298593, "FY2023": 282378, "FY2022": 359906, "FY2021": 374820}),
    ("DATA", "On demand deposits with credit institutions", {"FY2025": 18184, "FY2024": 10684}),
    ("DATA", "Loans and advances to credit institutions", {"FY2023": 31575, "FY2022": 34611, "FY2021": 42177}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1098334, "FY2024": 1088413, "FY2023": 1111377, "FY2022": 1121305, "FY2021": 1132132}),
    ("DATA", "Debt securities", {"FY2025": 643064, "FY2024": 551669, "FY2023": 456689, "FY2022": 345801, "FY2021": 269035}),
    ("DATA", "Intangible fixed assets", {"FY2025": 1183, "FY2024": 1371, "FY2023": 927, "FY2022": 1162, "FY2021": 1183}),
    ("DATA", "Property, plant and equipment", {"FY2025": 10497, "FY2024": 11032, "FY2023": 11230, "FY2022": 11624, "FY2021": 11957}),
    ("DATA", "Right of use assets", {"FY2025": 733, "FY2024": 766, "FY2023": 912, "FY2022": 1049, "FY2021": 1180}),
    ("DATA", "Deferred tax asset", {"FY2025": 325, "FY2024": 254, "FY2023": 288, "FY2022": 235, "FY2021": 238}),
    ("DATA", "Current tax asset", {"FY2023": 640}),
    ("DATA", "Other assets", {"FY2025": 1718, "FY2024": 1547, "FY2023": 1799, "FY2022": 1139, "FY2021": 1742}),
    ("TOTAL", "Total assets", {"FY2025": 2043128, "FY2024": 1964329, "FY2023": 1897815, "FY2022": 1876832, "FY2021": 1834464}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from credit institutions", {"FY2025": 9760, "FY2024": 12743, "FY2023": 18008, "FY2022": 24692, "FY2021": 27899}),
    ("DATA", "Customer accounts", {"FY2025": 1817763, "FY2024": 1736002, "FY2023": 1664051, "FY2022": 1641905, "FY2021": 1607602}),
    ("DATA", "Debt issued", {"FY2024": 5736, "FY2023": 5736, "FY2022": 5733, "FY2021": 5736}),
    ("DATA", "Lease liabilities", {"FY2025": 764, "FY2024": 803, "FY2023": 950, "FY2022": 1080, "FY2021": 1205}),
    ("DATA", "Current tax", {"FY2025": 2205, "FY2024": 477, "FY2022": 317, "FY2021": 382}),
    ("DATA", "Other liabilities", {"FY2025": 3470, "FY2024": 7305, "FY2023": 12730, "FY2022": 6674, "FY2021": 3886}),
    ("DATA", "Provisions", {"FY2025": 544, "FY2024": 1075, "FY2023": 255, "FY2022": 334, "FY2021": 861}),
    ("TOTAL", "Total liabilities", {"FY2025": 1834506, "FY2024": 1764141, "FY2023": 1701730, "FY2022": 1680735, "FY2021": 1647571}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 172000, "FY2024": 172000, "FY2023": 172000, "FY2022": 172000, "FY2021": 172000}),
    ("DATA", "Merger reserve", {"FY2025": 55, "FY2024": 55, "FY2023": 55, "FY2022": 55, "FY2021": 55}),
    ("DATA", "Retained earnings", {"FY2025": 36567, "FY2024": 28133, "FY2023": 24030, "FY2022": 24042, "FY2021": 14838}),
    ("TOTAL", "Total equity", {"FY2025": 208622, "FY2024": 200188, "FY2023": 196085, "FY2022": 196097, "FY2021": 186893}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 2043128, "FY2024": 1964329, "FY2023": 1897815, "FY2022": 1876832, "FY2021": 1834464}),
]

bw.add_balance_sheet_sheet(
    title="Triodos Bank UK Limited — Balance Sheet",
    subtitle="TBUK entity-level (Company) basis, £'000. Total assets = Total liabilities + Total equity for "
              "every year. FY2025 Total equity has a genuine £4k gap against the Statement of Changes in "
              "Equity sheet's own closing figure - see source note, not a plug.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=320,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Statement of comprehensive income). FY2025-FY2024
# use the Revenue/Total income structure introduced in AR2025;
# FY2021-FY2023 use the older Net interest/Net fee income structure - kept
# as each year's own report presented it, not force-fit onto one shape.
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 98092, "FY2024": 98818, "FY2023": 88278, "FY2022": 53932, "FY2021": 39075}),
    ("DATA", "Interest expense", {"FY2025": -39517, "FY2024": -43573, "FY2023": -34637, "FY2022": -8528, "FY2021": -2900}),
    ("TOTAL", "Net interest income", {"FY2025": 58575, "FY2024": 55245, "FY2023": 53641, "FY2022": 45404, "FY2021": 36175}),
    ("DATA", "Fee and commission income", {"FY2025": 4561, "FY2024": 4077, "FY2023": 4348, "FY2022": 4387, "FY2021": 4221}),
    ("DATA", "Fee and commission expense", {"FY2025": -1449, "FY2024": -2031, "FY2023": -2295, "FY2022": -1985, "FY2021": -1520}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 3112, "FY2024": 2046, "FY2023": 2053, "FY2022": 2402, "FY2021": 2701}),
    ("DATA", "Other operating income/(expense)", {"FY2025": -84, "FY2024": 47, "FY2023": -49, "FY2022": 54, "FY2021": 232}),
    ("TOTAL", "Total income", {"FY2025": 61603, "FY2024": 57338, "FY2023": 55645, "FY2022": 47860, "FY2021": 39108}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Personnel expenses", {"FY2025": -21508, "FY2024": -21310, "FY2023": -18185, "FY2022": -14704, "FY2021": -12087}),
    ("DATA", "Other administrative expenses", {"FY2025": -21626, "FY2024": -25393, "FY2023": -23177, "FY2022": -18093, "FY2021": -16384}),
    ("TOTAL", "Operating expenses", {"FY2025": -43134, "FY2024": -46703, "FY2023": -41362, "FY2022": -32797, "FY2021": -28471}),
    ("DATA", "Impairment loss on financial instruments", {"FY2025": -294, "FY2024": -3665, "FY2023": -11368, "FY2022": -4862, "FY2021": -2159}),
    ("TOTAL", "Profit on ordinary activities before tax", {"FY2025": 18175, "FY2024": 6970, "FY2023": 2915, "FY2022": 10201, "FY2021": 8478}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": -4247, "FY2024": -1467, "FY2023": -127, "FY2022": -997, "FY2021": -637}),
    ("TOTAL", "Profit and total comprehensive income for the year", {"FY2025": 13928, "FY2024": 5503, "FY2023": 2788, "FY2022": 9204, "FY2021": 7841}),
]

bw.add_income_statement_sheet(
    title="Triodos Bank UK Limited — Profit & Loss",
    subtitle="TBUK entity-level (Company) basis, £'000. All profits are from continuing activities and TBUK "
              "discloses no other comprehensive income in any year - Profit for the year equals Total "
              "comprehensive income for the year exactly, every year. FY2025's own P&L bottom line (£13,928k) "
              "has a genuine £2k gap against the Statement of Changes in Equity sheet's own FY2025 movement "
              "figure (£13,930k) - see source note, not a transcription error.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=320,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity - chronological, ties to the
# Balance Sheet sheet's own Total equity every year (FY2021-FY2024 exactly;
# FY2025 has the documented £4k gap - see STATEMENTS_SOURCES). Zero
# undocumented plug rows - only two movement categories exist in any year
# (profit for the year, prior year dividend paid); no share issuances,
# treasury shares, share-based payments, FX reserve, or restatements
# appear anywhere in the 5-year equity note.
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Called up share capital", "Merger reserve", "Retained earnings", "Total"]

equity_rows = [
    ("TOTAL", "Balance at 1 January 2021", (172000, 55, 9297, 181352)),
    ("DATA", "Profit and total comprehensive income for the year", (None, None, 7841, 7841)),
    ("DATA", "Prior year dividend paid", (None, None, -2300, -2300)),
    ("TOTAL", "Balance at 31 December 2021 / 1 January 2022", (172000, 55, 14838, 186893)),
    ("DATA", "Profit and total comprehensive income for the year", (None, None, 9204, 9204)),
    ("DATA", "Prior year dividend paid", (None, None, 0, 0)),
    ("TOTAL", "Balance at 31 December 2022 / 1 January 2023", (172000, 55, 24042, 196097)),
    ("DATA", "Profit and total comprehensive income for the year", (None, None, 2788, 2788)),
    ("DATA", "Prior year dividend paid", (None, None, -2800, -2800)),
    ("TOTAL", "Balance at 31 December 2023 / 1 January 2024", (172000, 55, 24030, 196085)),
    ("DATA", "Total profit and comprehensive income", (None, None, 5503, 5503)),
    ("DATA", "Prior year dividend paid", (None, None, -1400, -1400)),
    ("TOTAL", "Balance at 31 December 2024 / 1 January 2025", (172000, 55, 28133, 200188)),
    ("DATA", "Total profit and comprehensive income", (None, None, 13930, 13930)),
    ("DATA", "Prior year dividend paid", (None, None, -5500, -5500)),
    ("TOTAL", "Balance at 31 December 2025 (per this statement)", (172000, 55, 36563, 208618)),
]

bw.add_equity_changes_sheet(
    title="Triodos Bank UK Limited — Statement of Changes in Equity",
    subtitle="TBUK entity-level (Company) basis, £'000, chronological (oldest to newest). Zero undocumented "
              "plug rows across all 5 years - only 'Profit for the year' and 'Prior year dividend paid' ever "
              "move equity; no share issuances, treasury shares, share-based payments, FX reserve movements, "
              "or restatements appear anywhere in this note. FY2021-FY2024 closing balances tie exactly to "
              "the Balance Sheet sheet's own Total equity; FY2025's closing balance here (£208,618k) has a "
              "genuine £4k gap against the Balance Sheet's own stated FY2025 Total equity (£208,622k) - see "
              "source note, reproduced exactly as this statement states it, not silently reconciled.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=50,
    source_height=320,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 18175, "FY2024": 6970, "FY2023": 2915, "FY2022": 10201, "FY2021": 8478}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 388, "FY2024": 1082, "FY2023": 1045, "FY2022": 1022, "FY2021": 980}),
    ("DATA", "Loss on fixed asset disposal", {"FY2023": 20, "FY2022": 5, "FY2021": 0}),
    ("DATA", "Debt securities premium and discount amortisation", {"FY2025": -5116, "FY2024": -4528, "FY2023": -1710, "FY2022": 82, "FY2021": 1509}),
    ("DATA", "Increase in interest receivable on debt securities", {"FY2025": -2225, "FY2024": -2163}),
    ("DATA", "Increase/(Decrease) in ECL on financial instruments", {"FY2025": -1246, "FY2024": -3590, "FY2023": -787, "FY2022": 4262, "FY2021": 2268}),
    ("DATA", "Write off of financial instruments", {"FY2025": 1539, "FY2024": 7229, "FY2023": 12308, "FY2022": 0}),
    ("DATA", "Increase/(Decrease) in provisions", {"FY2025": -531, "FY2024": 820, "FY2023": -80, "FY2022": -527, "FY2021": 199}),
    ("DATA", "Interest on lease liabilities", {"FY2025": 16, "FY2024": 29, "FY2023": 39, "FY2022": 36, "FY2021": 28}),
    ("DATA", "Tax expense", {"FY2025": -4247, "FY2024": -1467, "FY2023": -127, "FY2022": -997, "FY2021": -637}),
    ("TOTAL", "Cash flow from business operations", {"FY2025": 6753, "FY2024": 4382, "FY2023": 13623, "FY2022": 14084, "FY2021": 12825}),
    ("DATA", "Increase/(Decrease) in loans and advances to customers", {"FY2025": -10208, "FY2024": 19325, "FY2023": -1593, "FY2022": 6563, "FY2021": -64020}),
    ("DATA", "Increase/(Decrease) in deferred tax asset", {"FY2025": -70, "FY2024": 34, "FY2023": -53, "FY2022": 3, "FY2021": -77}),
    ("DATA", "Increase/(Decrease) in other assets", {"FY2025": -171, "FY2024": 252, "FY2023": -660, "FY2022": 604, "FY2021": 730}),
    ("DATA", "(Decrease) in deposits from credit institutions", {"FY2025": -2983, "FY2024": -5265, "FY2023": -6684, "FY2022": -3207, "FY2021": -6243}),
    ("DATA", "Increase in deposits from customers", {"FY2025": 81761, "FY2024": 71951, "FY2023": 22145, "FY2022": 34303, "FY2021": 194863}),
    ("DATA", "Increase/(Decrease) in current tax liability", {"FY2025": 1728, "FY2024": 1117, "FY2023": -957, "FY2022": -66, "FY2021": 164}),
    ("DATA", "Increase/(Decrease) in other liabilities", {"FY2025": -3834, "FY2024": -5425, "FY2023": 6056, "FY2022": 2788, "FY2021": 667}),
    ("TOTAL", "Cash flow from operating activities (= business operations subtotal + changes above)", {"FY2025": 72976, "FY2024": 86371, "FY2023": 31877, "FY2022": 55072, "FY2021": 138909}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Investment in intangible assets", {"FY2025": -132, "FY2024": -701, "FY2023": -5, "FY2022": -200, "FY2021": -85}),
    ("DATA", "Investment in property and equipment", {"FY2025": 502, "FY2024": -481, "FY2023": -294, "FY2022": -342, "FY2021": -254}),
    ("DATA", "(Increase)/decrease in interest receivable on debt securities", {"FY2023": -1777, "FY2022": 249, "FY2021": 49}),
    ("DATA", "Investment in debt securities", {"FY2025": -240343, "FY2024": -183290, "FY2023": -162400, "FY2022": -106096, "FY2021": -138211}),
    ("DATA", "Sale of debt securities", {"FY2023": 0, "FY2022": 0, "FY2021": 5128}),
    ("DATA", "Maturity of debt securities", {"FY2025": 156285, "FY2024": 95000, "FY2023": 55000, "FY2022": 29000, "FY2021": 15500}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -83688, "FY2024": -89472, "FY2023": -109476, "FY2022": -77389, "FY2021": -117873}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid", {"FY2025": -5500, "FY2024": -1400, "FY2023": -2800, "FY2022": 0, "FY2021": -2300}),
    ("DATA", "Payment of lease liabilities", {"FY2025": -55, "FY2024": -175, "FY2023": -168, "FY2022": -160, "FY2021": -156}),
    ("DATA", "Increase/(Decrease) in debt issued and borrowed funds", {"FY2025": -5736, "FY2024": 0, "FY2023": 3, "FY2022": -4, "FY2021": 33}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": -11291, "FY2024": -1575, "FY2023": -2965, "FY2022": -164, "FY2021": -2423}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -22003, "FY2024": -4676, "FY2023": -80564, "FY2022": -22481, "FY2021": 18613}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 309277, "FY2024": 313953, "FY2023": 394517, "FY2022": 416998, "FY2021": 398385}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 287274, "FY2024": 309277, "FY2023": 313953, "FY2022": 394517, "FY2021": 416998}),
    ("SECTION", "Represented by (memo breakdown, not additional totals)", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 269090, "FY2024": 298593, "FY2023": 282378, "FY2022": 359906, "FY2021": 374820}),
    ("DATA", "On demand deposits with credit institutions", {"FY2025": 18184, "FY2024": 10684, "FY2023": 30472, "FY2022": 33412, "FY2021": 40979}),
    ("DATA", "Other loans and advances to credit institutions", {"FY2023": 1103, "FY2022": 1199, "FY2021": 1199}),
]

bw.add_cash_flow_sheet(
    title="Triodos Bank UK Limited — Cash Flow Statement",
    subtitle="TBUK entity-level (Company) basis, £'000. See source note for the two-level operating subtotal.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality. FY2022-FY2025 use the Stage 1/2/3 credit-quality
# analysis note (loans and advances to customers, gross carrying amount +
# ECL allowance); ties exactly to the Balance Sheet's own Loans and
# advances to customers net figure for FY2022-FY2024 (£1k rounding gap for
# FY2025). FY2021's Annual Report genuinely does not contain a by-stage
# credit-quality table at all (confirmed via full page-by-page review of
# AR2021's notes 22-24, which jump straight from Provisions to Called up
# share capital) - a real, confirmed non-disclosure for that year, not an
# access gap - so FY2021 uses only the coarser product-level split (Note
# 11: Corporate loans / Current accounts) that IS available that year.
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - Triodos Bank UK Limited entity-level (Company) credit quality disclosures, £'000:\n"
    f"FY2025/FY2024: Annual Report 2025, Financial risk management note (credit quality analysis by stage), "
    f"p.79-81 - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report 2023, Financial risk management note (credit quality analysis by stage), "
    f"p.98-100 - {AR2023_URL}\n"
    f"FY2021: Annual Report 2021, Note 11 (Loans and advances to customers - product-level split only; no "
    f"by-stage credit-quality table exists in this earlier report vintage), p.45-46 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nCONFIRMED NON-DISCLOSURE (not an access gap): AR2021's own notes were reviewed in full (Note 22 "
    "Provisions p.55-57, through Note 23 Called up share capital, Note 24 Related party transactions) and "
    "contain no separate stage/rating-based credit quality note - that disclosure format was introduced in a "
    "later report vintage. FY2021's Stage 1/2/3 and NPL/coverage ratio rows are therefore left blank rather "
    "than guessed."
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 1069935, "FY2024": 1061389, "FY2023": 1090721, "FY2022": 1104291}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 22764, "FY2024": 22323, "FY2023": 15718, "FY2022": 12724}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 15827, "FY2024": 14663, "FY2023": 13977, "FY2022": 12045}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 1108526, "FY2024": 1098375, "FY2023": 1120416, "FY2022": 1129060}),
    ("SECTION", "ECL allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1 allowance", {"FY2025": 1657, "FY2024": 1584, "FY2023": 1653, "FY2022": 1602}),
    ("DATA", "Stage 2 allowance", {"FY2025": 979, "FY2024": 963, "FY2023": 663, "FY2022": 557}),
    ("DATA", "Stage 3 allowance", {"FY2025": 7556, "FY2024": 7415, "FY2023": 6723, "FY2022": 5596}),
    ("TOTAL", "Total ECL allowance", {"FY2025": 10192, "FY2024": 9962, "FY2023": 9039, "FY2022": 7755}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 1098334, "FY2024": 1088413, "FY2023": 1111377, "FY2022": 1121305}),
    ("SECTION", "FY2021 product-level split (no by-stage table disclosed that year - see source note)", {}),
    ("DATA", "Corporate loans", {"FY2021": 1108956}),
    ("DATA", "Current accounts", {"FY2021": 23176}),
    ("TOTAL", "Total loans and advances to customers (gross, FY2021)", {"FY2021": 1132132}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross)", {"FY2025": "1.43%", "FY2024": "1.33%", "FY2023": "1.25%", "FY2022": "1.07%"}),
    ("DATA", "Coverage ratio (Total ECL allowance / Total gross)", {"FY2025": "0.92%", "FY2024": "0.91%", "FY2023": "0.81%", "FY2022": "0.69%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross)", {"FY2025": "47.74%", "FY2024": "50.57%", "FY2023": "48.10%", "FY2022": "46.46%"}),
]

bw.add_asset_quality_sheet(
    title="Triodos Bank UK Limited — Asset Quality",
    subtitle="TBUK entity-level (Company) basis, £'000. FY2022-FY2024 ties exactly to Balance Sheet net loans "
              "and advances to customers; FY2025 has a £1k rounding gap. FY2021 uses the coarser product-level "
              "split only - no by-stage table exists in that year's report (confirmed non-disclosure, see "
              "source note).",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=72,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"TBUK entity-level basis, {unit}" if unit else "TBUK entity-level basis",
                         rows_data, sources_text, note=note, first_col_width=52, source_height=140)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 193448, "FY2024": 193259, "FY2023": 192544, "FY2022": 185772, "FY2021": 177905})],
    p3_sources(),
    note="FY2025 is from the Annual Report's own 'Total capital resources' note (Note 26/27, audited) since no "
         "FY2025 Pillar 3 report has been published yet - not derived, directly stated.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "21.3%", "FY2024": "22.1%", "FY2023": "22.36%", "FY2022": "21.57%", "FY2021": "21.2%"})],
    p3_sources(),
    note="FY2025 is from the Annual Report narrative (p.15), stated as 21.3% (2024: 22.1%); FY2024's figure there "
         "(22.1%) rounds slightly differently from the FY2024 Pillar 3 Report's own Table 9 figure (22.06%) - both "
         "are as-stated in their respective source documents, not reconciled to more decimal places.",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 193448, "FY2024": 193259, "FY2023": 192544, "FY2022": 185772, "FY2021": 177905})],
    p3_sources(),
    note="TBUK has no Additional Tier 1 (AT1) instruments in any year - Tier 1 capital equals CET1 capital exactly, "
         "every year, per the Annual Report's own 'Total capital resources' table (e.g. FY2025/FY2024: 'CET1 and "
         "Total Tier 1 capital resources' is a single stated line).",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "21.3%", "FY2024": "22.1%", "FY2023": "22.36%", "FY2022": "21.57%", "FY2021": "21.2%"})],
    p3_sources(),
    note="Numerically identical to the CET1 ratio every year, since Tier 1 capital = CET1 capital (no AT1 "
         "instruments) - not a separate disclosure.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 193448, "FY2024": 198954, "FY2023": 198239, "FY2022": 191467, "FY2021": 183600})],
    p3_sources(),
    note="Total capital = CET1 + Tier 2 (subordinated debt, £5.7m issued Dec 2020). The Tier 2 note was fully "
         "repaid in 2025, so FY2025 Total capital equals CET1 exactly for the first time in this series.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "21.3%", "FY2024": "22.7%", "FY2023": "23.02%", "FY2022": "22.20%", "FY2021": "21.8%"})],
    p3_sources(),
    note="FY2025/FY2024 from the Annual Report narrative (p.15); FY2024's Pillar 3 Report states this ratio as "
         "22.71% (Table 7) - a minor rounding difference from the Annual Report's 22.7%, both as-stated.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets (credit + operational + market + counterparty credit risk)",
      {"FY2025": 908207, "FY2024": 876076, "FY2023": 861016, "FY2022": 861273, "FY2021": 840391})],
    p3_sources(),
    note="FY2025 is CALCULATED (Total capital £193,448k / Total capital ratio 21.3% = ~£908.2m), not directly "
         "stated, since no FY2025 Pillar 3 report exists yet to give the audited RWA breakdown - simple arithmetic "
         "on two audited/stated figures, not an estimate, flagged per this project's convention (see Bank of "
         "Ireland UK workbook for the same approach). FY2024-FY2021 are Total RWA figures directly stated in each "
         "year's own Pillar 3 Report (Credit + Operational risk RWA; Market risk and Counterparty Credit risk RWA "
         "are nil every year).",
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Triodos Bank UK Limited (TBUK) entity-level Pillar 3 RWA breakdown (UK OV1-style table):\n"
    f"FY2024: Triodos Bank UK Limited 2024 Pillar 3 Report, 'TBUK RWAs and Capital Ratios' table - {P3_2024_URL}\n"
    f"FY2023: Triodos Bank UK Limited 2023 Pillar 3 Report, 'TBUK RWAs and Capital Ratios' table - {P3_2023_URL}\n"
    f"FY2022: Triodos Bank UK Limited 2022 Pillar 3 Report, 'TBUK RWAs and Capital Ratios' table - {P3_2022_URL}\n"
    f"FY2021: Triodos Bank UK Limited 2021 Pillar 3 Report, Table 7 (Overview of RWAs by exposure class) - "
    f"{P3_2021_URL}\n"
    "FY2025: no standalone Pillar 3 report has been published yet as of this workbook's build date - blank, "
    "consistent with every other Pillar 3 sheet in this workbook.\n"
    "PRESENTATION NOTE: FY2021's own Pillar 3 Report combines Credit risk and Counterparty Credit risk into a "
    "single exposure-class table (no separate CCR line existed as a distinct category that year) - kept as a "
    "single combined row exactly as that year's own report presented it, not split. All years' category sums "
    "tie exactly to the pre-existing Total RWAs figures on the Total RWAs sheet.\n\n"
    + ENTITY_NOTE
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk RWA", {"FY2024": 806870, "FY2023": 799630, "FY2022": 799316}),
    ("DATA", "Credit and Counterparty Credit risk RWA (combined, FY2021 basis)", {"FY2021": 780882}),
    ("DATA", "Counterparty Credit risk RWA", {"FY2024": 0, "FY2023": 0, "FY2022": 0}),
    ("DATA", "Market risk RWA", {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Operational risk RWA", {"FY2024": 69206, "FY2023": 61386, "FY2022": 61957, "FY2021": 59509}),
    ("TOTAL", "Total RWAs", {"FY2024": 876076, "FY2023": 861016, "FY2022": 861273, "FY2021": 840391}),
]

bw.add_rwa_breakdown_sheet(
    title="Triodos Bank UK Limited — RWA Breakdown",
    subtitle="TBUK entity-level basis, £'000. Category sums tie exactly to the Total RWAs sheet's own figures "
              "for every year with a Pillar 3 report. FY2021's Credit and Counterparty Credit risk are combined "
              "as that year's own report presented them (see source note). No FY2025 Pillar 3 report exists "
              "yet, consistent with the rest of this workbook's Pillar 3 sheets.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=68,
    source_height=240,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Tier 1 capital after deductions", {"FY2024": 193258, "FY2023": 192544, "FY2022": 185772, "FY2021": 177905}),
        ("Leverage ratio exposure measure", {"FY2024": 1715067, "FY2023": 1664149, "FY2022": 1583516, "FY2021": 1910203}),
        ("Leverage ratio (%)", {"FY2024": "11.27%", "FY2023": "11.57%", "FY2022": "11.73%", "FY2021": "9.3%"}),
    ],
    p3_sources(),
    note="TBUK is below the £50bn deposit threshold that triggers a binding UK leverage ratio requirement (PRA "
         "expectation only, minimum 3.25%). FY2022 onward uses the 'excluding claims on central banks' exposure "
         "basis (introduced in the 2022 Pillar 3 Report); FY2021's own 2021 Pillar 3 Report used a broader, "
         "non-comparable CRR2 full-exposure basis (9.3%, exposure measure £1,910.2m, including central bank "
         "claims) - shown here exactly as that year's own report stated it, NOT the later report's restated "
         "comparative, consistent with this project's practice of not blending non-comparable methodology "
         "vintages. No FY2025 figure: not disclosed in the Annual Report and no FY2025 Pillar 3 report exists yet.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total HQLA (point-in-time, year-end)", {"FY2024": 826600, "FY2023": 715900, "FY2022": 668900, "FY2021": 628207}),
        ("Total net cash outflows over 30-day stress (point-in-time, year-end)", {"FY2024": 175400, "FY2023": 170100, "FY2022": 151100, "FY2021": 151875}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "446%", "FY2024": "471.1%", "FY2023": "420.8%", "FY2022": "442.7%", "FY2021": "413.6%"}),
    ],
    p3_sources(),
    note="All ratios are the year-end point-in-time LCR (not the 12-month average-by-quarter tables each Pillar 3 "
         "report also separately discloses). FY2025's ratio (446%) is from the Annual Report narrative only (p.15) "
         "- no £ HQLA/outflow breakdown is available since no FY2025 Pillar 3 report exists yet.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Available stable funding", {"FY2024": 1731150, "FY2022": 1637537}),
        ("Required stable funding", {"FY2024": 866978, "FY2022": 903741}),
        ("Net Stable Funding Ratio (%)", {"FY2024": "206%", "FY2023": "188%", "FY2022": "181%"}),
    ],
    p3_sources(),
    note="FY2024 and FY2022 are year-end point-in-time NSFR (FY2024 Pillar 3 Report states '206%' directly in "
         "narrative and gives the underlying £; FY2022's own Pillar 3 Report gives a separate point-in-time "
         "quarter-end table distinct from its 12-month-average table, from which the 31-Dec-22 figure of 181% is "
         "taken). FY2023's Pillar 3 Report only discloses the 12-month-average-by-quarter-end table (no separate "
         "point-in-time statement that year) - 188% shown here is that average-basis 31-Dec-23 quarter figure, "
         "not a strict point-in-time balance, so is not fully comparable to the other years' figures. FY2021: no "
         "NSFR section appears in TBUK's 2021 Pillar 3 Report at all (the metric was not yet part of that year's "
         "disclosure). FY2025: not disclosed - no FY2025 Pillar 3 report exists yet and the Annual Report gives no "
         "NSFR percentage (only confirms the ratio is monitored).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "No MREL figure or qualitative MREL disclosure appears in any of TBUK's Annual Reports or "
                      "Pillar 3 Reports (FY2021-FY2024) - not asserted as an explicit exemption, simply absent "
                      "from every source reviewed, consistent with several other small banks in this project "
                      "series (e.g. Zopa, LHV, Vida).",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 2043128, "FY2024": 1964329, "FY2023": 1897815, "FY2022": 1876832, "FY2021": 1834464}),
        ("Total liabilities", {"FY2025": 1834506, "FY2024": 1764141, "FY2023": 1701730, "FY2022": 1680735, "FY2021": 1647571}),
        ("Total equity", {"FY2025": 208622, "FY2024": 200188, "FY2023": 196085, "FY2022": 196097, "FY2021": 186893}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {"FY2025": 61603, "FY2024": 57338, "FY2023": 55645, "FY2022": 47860, "FY2021": 39108}),
        ("Profit on ordinary activities before tax", {"FY2025": 18175, "FY2024": 6970, "FY2023": 2915, "FY2022": 10201, "FY2021": 8478}),
        ("Profit and total comprehensive income for the year", {"FY2025": 13928, "FY2024": 5503, "FY2023": 2788, "FY2022": 9204, "FY2021": 7841}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 200188, "FY2024": 196085, "FY2023": 196097, "FY2022": 186893, "FY2021": 181352}),
        ("Profit for the year", {"FY2025": 13930, "FY2024": 5503, "FY2023": 2788, "FY2022": 9204, "FY2021": 7841}),
        ("Other equity movements, net", {"FY2025": -5500, "FY2024": -1400, "FY2023": -2800, "FY2022": 0, "FY2021": -2300}),
        ("Closing equity", {"FY2025": 208618, "FY2024": 200188, "FY2023": 196085, "FY2022": 196097, "FY2021": 186893}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Cash flow from operating activities", {"FY2025": 72976, "FY2024": 86371, "FY2023": 31877, "FY2022": 55072, "FY2021": 138909}),
        ("Net cash from/(used in) investing activities", {"FY2025": -83688, "FY2024": -89472, "FY2023": -109476, "FY2022": -77389, "FY2021": -117873}),
        ("Net cash from/(used in) financing activities", {"FY2025": -11291, "FY2024": -1575, "FY2023": -2965, "FY2022": -164, "FY2021": -2423}),
        ("Cash and cash equivalents at end of year", {"FY2025": 287274, "FY2024": 309277, "FY2023": 313953, "FY2022": 394517, "FY2021": 416998}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "21.3%", "FY2024": "22.1%", "FY2023": "22.36%", "FY2022": "21.57%", "FY2021": "21.2%"}),
        ("Tier 1 Ratio", {"FY2025": "21.3%", "FY2024": "22.1%", "FY2023": "22.36%", "FY2022": "21.57%", "FY2021": "21.2%"}),
        ("Total Capital Ratio", {"FY2025": "21.3%", "FY2024": "22.7%", "FY2023": "23.02%", "FY2022": "22.20%", "FY2021": "21.8%"}),
        ("Leverage Ratio", {"FY2024": "11.27%", "FY2023": "11.57%", "FY2022": "11.73%", "FY2021": "9.3%"}),
        ("LCR", {"FY2025": "446%", "FY2024": "471.1%", "FY2023": "420.8%", "FY2022": "442.7%", "FY2021": "413.6%"}),
        ("NSFR", {"FY2024": "206%", "FY2023": "188%", "FY2022": "181%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. No FY2025 Pillar 3 report has been published yet, so Leverage "
         "Ratio and NSFR are blank for FY2025 (Total RWAs on that sheet is a calculated figure for FY2025 - see "
         "its own note). TBUK does not take the FRS 101/102 cash-flow exemption used by several other single-"
         "parent foreign subsidiary banks in this project - a full Statement of Cash Flows exists for all 5 years.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/TRIODOS FINANCIALS.xlsx")
