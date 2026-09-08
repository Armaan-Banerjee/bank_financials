import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/11379025/filing-history/MzUxNzk5NTMwNmFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/11379025/filing-history/MzQyMjE2MDUwOWFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/11379025/filing-history/MzM1Mjk5ODYxMGFkaXF6a2N4/document?format=pdf&download=0"
AR2020_URL = "https://find-and-update.company-information.service.gov.uk/company/11379025/filing-history/MzMwNzg5OTQzMGFkaXF6a2N4/document?format=pdf&download=0"
AR2019_URL = "https://find-and-update.company-information.service.gov.uk/company/11379025/filing-history/MzI3NjE4MDIwNWFkaXF6a2N4/document?format=pdf&download=0"
AA02_2018_URL = "https://find-and-update.company-information.service.gov.uk/company/11379025/filing-history/MzIyNDA2MDg2NWFkaXF6a2N4/document?format=pdf&download=0"

P3_2024_URL = "https://www.triodos.co.uk/binaries/content/assets/tbuk/press-and-media-page/triodos-bank-uk-2024-pillar-3.pdf"
P3_2023_URL = "https://www.triodos.co.uk/binaries/content/assets/tbuk/press-and-media-page/triodos-bank-uk-2023-pillar-3-report.pdf"
P3_2022_URL = "https://www.triodos.co.uk/binaries/content/assets/tbuk/press-and-media-page/triodos-bank-uk-2022-pillar-3-report.pdf"
P3_2021_URL = "https://www.triodos.co.uk/downloads/triodos-bank-uk-2021-pillar-3-report?id=9efebf75e4f1"
P3_2020_URL = "https://www.triodos.co.uk/binaries/content/assets/tbuk/press-and-media-page/triodos-bank-uk-2020-pillar-3-report.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Triodos Bank UK Limited (TBUK, company number 11379025, FRN 817008) is a wholly owned "
    "subsidiary of Triodos Bank N.V. (the Netherlands), established in 2019 to continue Triodos Bank's UK "
    "operations (previously run as a UK branch of Triodos Bank N.V. since 1995) via a Part VII transfer. Although "
    "TBUK's own accounts are exempt under s.401 of the Companies Act 2006 from preparing CONSOLIDATED financial "
    "statements (it and its subsidiary undertaking are fully consolidated into Triodos Bank N.V.'s own group "
    "accounts), TBUK's own entity-level accounts DO include a full Statement of Cash Flows every year - unlike "
    "several other single-parent foreign subsidiary banks in this series (e.g. ICICI Bank UK, United Trust Bank), "
    "TBUK does not take the FRS 101/102 cash-flow-statement disclosure exemption. All figures below are TBUK's own "
    "entity-level (Company) results, in £, not Triodos Bank N.V. group figures. Companies House filings for all 7 "
    "years covered (FY2019-FY2025) were fully scanned/image-only PDFs with no text layer; all figures were "
    "extracted via direct visual reading of the rendered page images (no OCR text layer available), cross-checked "
    "line-by-line against each statement's own subtotals.\n\n"
    "FY2018 IS DELIBERATELY EXCLUDED (not a self-skipped year within the workbook's column range - it is simply "
    "outside it): TBUK was incorporated 23 May 2018 but did not begin trading until the Part VII transfer of "
    "Triodos Bank N.V.'s UK branch business on 1 May 2019 (see below). TBUK's only Companies House filing for "
    "FY2018 is a 3-page 'Dormant company accounts' (AA02) filing made up to 31 December 2018, showing net assets "
    "of £1,000 (1,000 £1 ordinary subscriber shares, cash at bank £1,000) and no P&L, cash flow, or capital "
    "disclosure of any kind - " + AA02_2018_URL + " . There is no substantive FY2018 financial data to transcribe "
    "for any sheet in this workbook (Balance Sheet, P&L, Cash Flow, Asset Quality, or any Pillar 3 metric); this is "
    "a genuine non-existence of the business, not an access gap, so FY2018 is left out of this workbook's YEARS "
    "range entirely rather than added as an all-blank column. The Statement of Changes in Equity sheet's opening "
    "balance still reflects this dormant £1k starting position, since that sheet is a chronological roll-forward.\n\n"
    "FY2019 covers only EIGHT MONTHS of actual trading (1 May 2019 - 31 December 2019), not a full 12-month period, "
    "even though it is presented as a full financial year: on 1 May 2019 the operations and all assets/liabilities "
    "of the UK branch of Triodos Bank N.V. were transferred to TBUK via a Part VII transfer (Financial Services and "
    "Markets Act 2000), and TBUK's own Annual Report 2019 explicitly states 'the figures presented ... represent "
    "eight months of trading.' FY2019's P&L, cash flow, and equity-movement figures are therefore not directly "
    "comparable on a run-rate basis to any other year in this workbook, which are all full 12-month periods (FY2020 "
    "onward). This is flagged on every sheet FY2019 appears on, not silently normalised to a pro-rated annual figure."
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
    f"FY2020: Triodos Bank UK Limited Annual Report 2020 (Companies House filing, made up to 31 Dec 2020), p.36 "
    f"(Cash flow statement for the year ended 31 December 2020) - {AR2020_URL}\n"
    f"FY2019: Triodos Bank UK Limited Annual Report 2019 (Companies House filing, made up to 31 Dec 2019), p.30 "
    f"(Cash flow statement for the year ended 31 December 2019 - covers 8 months of trading, see ENTITY_NOTE) - "
    f"{AR2019_URL}\n"
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
    "FY2019-SPECIFIC ONE-OFF ITEMS: 'Transfer of business from Triodos Bank N.V.' (£156,471k investing inflow) and "
    "'Increase in equity' (£171,999k financing inflow, the share capital issued in exchange for the Part VII "
    "transfer) are one-off items unique to FY2019 (the year of the transfer itself) and do not recur in any other "
    "year. FY2019's own 'Net impairment loss on financial instruments' (£64k) and 'Decrease in provisions' "
    "(£(237)k) reconciling items are shown as FY2019's own statement presented them; TBUK's own FY2020 Annual "
    "Report separately restates its FY2019 comparative column for several of these reconciling items to different "
    "values (e.g. depreciation £548k vs £527k, ECL movement £(62)k vs £64k, provisions movement £(126)k vs "
    "£(237)k) - a genuine restatement between report vintages, not a transcription error. This sheet uses each "
    "year's OWN annual report as the primary source for that year (consistent with this project's general practice "
    "for every bank), not a later year's restated comparative column, so these FY2020-report restatements are not "
    "reflected in the FY2019 column here.\n\n"
    "GENUINE SOURCE FOOTING GAP (FY2019 only): AR2019's own 'Cash flow from business operations' subtotal is "
    "stated as £4,789k, but its own listed adjustment lines above it sum to £4,802k (a £13k gap) - both the "
    "individual line items and the £4,789k subtotal are transcribed here exactly as AR2019's own statement prints "
    "them, not force-footed to agree. All other years in this workbook (FY2020-FY2025) foot exactly.\n\n"
    + ENTITY_NOTE
)


def p3_sources(pages="7-14"):
    return (
        "Sources - Triodos Bank UK Limited (TBUK) entity-level Pillar 3 disclosures:\n"
        f"FY2024: Triodos Bank UK Limited 2024 Pillar 3 Report, p.{pages} - {P3_2024_URL}\n"
        f"FY2023: Triodos Bank UK Limited 2023 Pillar 3 Report - {P3_2023_URL}\n"
        f"FY2022: Triodos Bank UK Limited 2022 Pillar 3 Report - {P3_2022_URL}\n"
        f"FY2021: Triodos Bank UK Limited 2021 Pillar 3 Report - {P3_2021_URL}\n"
        f"FY2020: Triodos Bank UK Limited 2020 Pillar 3 Report - {P3_2020_URL}\n"
        "FY2019: no standalone Pillar 3 report was published for FY2019 - confirmed by checking both the same "
        "binaries/ URL pattern used for the 2020-2024 editions and the /downloads/ URL pattern used for the 2021 "
        "edition; neither resolves for a 2019 edition (both return HTTP 404). This is consistent with FY2019 being "
        "TBUK's first (partial, 8-month) trading period - TBUK's Pillar 3 disclosure appears to have started with "
        "FY2020, its first full 12-month year. Where FY2019 Pillar 3-style figures appear on this sheet, they are "
        "instead the FY2020 Pillar 3 Report's own audited FY2019 comparative column (that report states its own "
        "current-year CET1 capital figure 'agrees to equity and reserves in the Annual Report', i.e. this "
        "comparative column is itself an audited regulatory figure, not a narrative estimate) - see the sheet's own "
        "note for which figures this applies to.\n"
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
    f"changes in equity p.29 - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020 - Statement of comprehensive income p.33, Balance sheet p.34, Statement of "
    f"changes in equity p.35 - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019 - Statement of comprehensive income p.27, Balance sheet p.28, Statement of "
    f"changes in equity p.29 (covers 8 months of trading, see ENTITY_NOTE) - {AR2019_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nGENUINE SOURCE DISCREPANCY (not a transcription error, not forced to tie): TBUK's own AR2025 does "
    "not internally reconcile to the pound for FY2025. The Statement of comprehensive income states 'Profit "
    "and total comprehensive income' of £13,928k; the Statement of changes in equity separately states "
    "'Total profit and comprehensive income' of £13,930k for the same year (a £2k gap). Correspondingly, the "
    "Statement of changes in equity's own closing Retained earnings/Total equity for 31 December 2025 "
    "(£36,563k / £208,618k) does not exactly match the Statement of financial position's own Retained "
    "earnings/Total equity as at the same date (£36,567k / £208,622k) - a £4k gap. Both figures are "
    "reproduced here exactly as each statement states them; this sheet does not silently pick one or plug "
    "the difference. No such gap exists in FY2020-FY2024 - those years tie to the pound across "
    "all three statements as each YEAR'S OWN report states them.\n\n"
    "SEPARATE GENUINE RESTATEMENT (FY2019 only, not the same issue as above): TBUK's own FY2020 Annual Report "
    "restates several of its FY2019 comparative balance-sheet/P&L figures to different values than AR2019's own "
    "audited FY2019 figures - e.g. Total assets £1,378,463k (AR2020 comparative) vs £1,378,369k (AR2019 own, a "
    "£94k gap), Loans and advances to customers £975,151k vs £975,025k (£126k gap), Provisions £488k vs £377k "
    "(£111k gap), Profit for the year £3,656k vs £3,663k (£7k gap), Total equity £175,711k vs £175,718k (£7k "
    "gap). This sheet uses each year's OWN annual report as the primary source for that year (AR2019 for the "
    "FY2019 column here), not a later year's restated comparative - consistent with this project's general "
    "practice. Separately, AR2019 is not even internally consistent with itself: its own Statement of financial "
    "position states Loans and advances to customers of £975,025k, while its own credit-quality note (Note 26) "
    "sums to £975,151k for the same balance - a £126k gap WITHIN the single AR2019 document, reproduced here "
    "exactly as each of AR2019's own statements/notes state it (Balance Sheet sheet uses the £975,025k "
    "Statement-of-financial-position figure; the Asset Quality sheet uses the £975,151k credit-quality-note "
    "figure), not silently reconciled."
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
    ("DATA", "Cash and cash equivalents", {"FY2025": 269090, "FY2024": 298593, "FY2023": 282378, "FY2022": 359906, "FY2021": 374820, "FY2020": 375679, "FY2019": 236613}),
    ("DATA", "On demand deposits with credit institutions", {"FY2025": 18184, "FY2024": 10684}),
    ("DATA", "Loans and advances to credit institutions", {"FY2023": 31575, "FY2022": 34611, "FY2021": 42177, "FY2020": 22705, "FY2019": 27455}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1098334, "FY2024": 1088413, "FY2023": 1111377, "FY2022": 1121305, "FY2021": 1132132, "FY2020": 1070386, "FY2019": 975025}),
    ("DATA", "Total debt securities", {"FY2025": 643064, "FY2024": 551669, "FY2023": 456689, "FY2022": 345801, "FY2021": 269035, "FY2020": 153005, "FY2019": 115269}),
    ("DATA", "Government securities (issued by public bodies)", {"FY2025": 296183, "FY2024": 167494, "FY2023": 171574, "FY2022": 154662, "FY2021": 124958, "FY2020": 62207, "FY2019": 71259}),
    ("DATA", "Debt securities issued by other issuers", {"FY2025": 346887, "FY2024": 384178, "FY2023": 285118, "FY2022": 191142, "FY2021": 144081, "FY2020": 90808, "FY2019": 44016}),
    ("DATA", "Expected credit loss on debt securities", {"FY2025": -7, "FY2024": -3, "FY2023": -3, "FY2022": -3, "FY2021": -4, "FY2020": -10, "FY2019": -7}),
    ("DATA", "Intangible fixed assets", {"FY2025": 1183, "FY2024": 1371, "FY2023": 927, "FY2022": 1162, "FY2021": 1183, "FY2020": 1312, "FY2019": 1548}),
    ("DATA", "Property, plant and equipment", {"FY2025": 10497, "FY2024": 11032, "FY2023": 11230, "FY2022": 11624, "FY2021": 11957, "FY2020": 12327, "FY2019": 12456}),
    ("DATA", "Right of use assets", {"FY2025": 733, "FY2024": 766, "FY2023": 912, "FY2022": 1049, "FY2021": 1180, "FY2020": 1322, "FY2019": 977}),
    ("DATA", "Deferred tax asset", {"FY2025": 325, "FY2024": 254, "FY2023": 288, "FY2022": 235, "FY2021": 238, "FY2020": 161, "FY2019": 170}),
    ("DATA", "Current tax asset", {"FY2023": 640}),
    ("DATA", "Other assets", {"FY2025": 1718, "FY2024": 1547, "FY2023": 1799, "FY2022": 1139, "FY2021": 1742, "FY2020": 2473, "FY2019": 8855}),
    ("TOTAL", "Total assets", {"FY2025": 2043128, "FY2024": 1964329, "FY2023": 1897815, "FY2022": 1876832, "FY2021": 1834464, "FY2020": 1639370, "FY2019": 1378369}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from credit institutions", {"FY2025": 9760, "FY2024": 12743, "FY2023": 18008, "FY2022": 24692, "FY2021": 27899, "FY2020": 34142, "FY2019": 36256}),
    ("DATA", "Customer accounts", {"FY2025": 1817763, "FY2024": 1736002, "FY2023": 1664051, "FY2022": 1641905, "FY2021": 1607602, "FY2020": 1412742, "FY2019": 1155946}),
    ("DATA", "Debt issued", {"FY2024": 5736, "FY2023": 5736, "FY2022": 5733, "FY2021": 5736, "FY2020": 5703}),
    ("DATA", "Lease liabilities", {"FY2025": 764, "FY2024": 803, "FY2023": 950, "FY2022": 1080, "FY2021": 1205, "FY2020": 1332, "FY2019": 974}),
    ("DATA", "Current tax", {"FY2025": 2205, "FY2024": 477, "FY2022": 317, "FY2021": 382, "FY2020": 218, "FY2019": 596}),
    ("DATA", "Other liabilities", {"FY2025": 3470, "FY2024": 7305, "FY2023": 12730, "FY2022": 6674, "FY2021": 3886, "FY2020": 3219, "FY2019": 8502}),
    ("DATA", "Provisions", {"FY2025": 544, "FY2024": 1075, "FY2023": 255, "FY2022": 334, "FY2021": 861, "FY2020": 662, "FY2019": 377}),
    ("TOTAL", "Total liabilities", {"FY2025": 1834506, "FY2024": 1764141, "FY2023": 1701730, "FY2022": 1680735, "FY2021": 1647571, "FY2020": 1458018, "FY2019": 1202652}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 172000, "FY2024": 172000, "FY2023": 172000, "FY2022": 172000, "FY2021": 172000, "FY2020": 172000, "FY2019": 172000}),
    ("DATA", "Merger reserve", {"FY2025": 55, "FY2024": 55, "FY2023": 55, "FY2022": 55, "FY2021": 55, "FY2020": 55, "FY2019": 55}),
    ("DATA", "Retained earnings", {"FY2025": 36567, "FY2024": 28133, "FY2023": 24030, "FY2022": 24042, "FY2021": 14838, "FY2020": 9297, "FY2019": 3663}),
    ("TOTAL", "Total equity", {"FY2025": 208622, "FY2024": 200188, "FY2023": 196085, "FY2022": 196097, "FY2021": 186893, "FY2020": 181352, "FY2019": 175718}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 2043128, "FY2024": 1964329, "FY2023": 1897815, "FY2022": 1876832, "FY2021": 1834464, "FY2020": 1639370, "FY2019": 1378369}),
]

BALANCE_SHEET_SOURCES = (
    STATEMENTS_SOURCES
    + "\n\nDEBT SECURITIES BREAKDOWN (issuer type, each year's own Note 12/13 'Debt Securities'): 'Government "
    "securities (issued by public bodies)' = that note's own 'Issued by public bodies' line (UK central "
    "government plus, in most years, regional government/public sector entities - not broken out separately "
    "here); 'Debt securities issued by other issuers' = that note's own 'Issued by other issuers' line (credit "
    "institutions, corporate debt securities, multilateral development banks - see the note's own maturity-"
    "analysis sub-table for the issuer-type detail within this leg); 'Expected credit loss on debt securities' "
    "= that note's own ECL line. The three sum exactly to 'Total debt securities' for FY2020-FY2024; FY2025 and FY2019 each have "
    "a genuine £1k internal rounding gap within their own source note (FY2025: Note 12's own three lines sum "
    "to £643,063k against its own stated 'Balance sheet value as at 31 December' of £643,064k; FY2019: Note "
    "13's own three lines sum to £115,268k against its own stated total of £115,269k) - both years reproduced "
    "exactly as each note states its own lines and its own total, not plugged. Per AR2025's own 'Financial "
    "instruments' accounting policy (p.61): 'All of the Bank's financial instruments are measured at amortised "
    "cost less impairment allowance where applicable' - i.e. there is no FVOCI/FVTPL/trading leg to split out "
    "for this book in any year; 100% of debt securities are held at amortised cost. Note pages: FY2025/FY2024 "
    f"Note 12, AR2025 p.74 - {AR2025_URL}; FY2023/FY2022 Note 12, AR2023 p.95 - {AR2023_URL}; FY2021/FY2020 "
    f"Note 12, AR2021 p.50 - {AR2021_URL}; FY2019 Note 13, AR2019 p.48 - {AR2019_URL}."
)

bw.add_balance_sheet_sheet(
    title="Triodos Bank UK Limited — Balance Sheet",
    subtitle="TBUK entity-level (Company) basis, £'000. Total assets = Total liabilities + Total equity for "
              "every year (off by £1k for FY2019, immaterial rounding). FY2025 Total equity has a genuine £4k "
              "gap against the Statement of Changes in Equity sheet's own closing figure; FY2019's own figures "
              "here differ from later years' restated FY2019 comparatives - see source note for both, not plugs. "
              "Debt securities are broken down below by issuer type (government/public bodies vs other issuers, "
              "net of expected credit loss) per each year's own Note 12/13 - see source note; all debt "
              "securities are held at amortised cost (no fair-value-through-P&L/OCI leg disclosed, see source "
              "note).",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=68,
    source_height=420,
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
    ("DATA", "Interest income", {"FY2025": 98092, "FY2024": 98818, "FY2023": 88278, "FY2022": 53932, "FY2021": 39075, "FY2020": 37933, "FY2019": 24844}),
    ("DATA", "Interest expense", {"FY2025": -39517, "FY2024": -43573, "FY2023": -34637, "FY2022": -8528, "FY2021": -2900, "FY2020": -5613, "FY2019": -5590}),
    ("TOTAL", "Net interest income", {"FY2025": 58575, "FY2024": 55245, "FY2023": 53641, "FY2022": 45404, "FY2021": 36175, "FY2020": 32320, "FY2019": 19254}),
    ("DATA", "Fee and commission income", {"FY2025": 4561, "FY2024": 4077, "FY2023": 4348, "FY2022": 4387, "FY2021": 4221, "FY2020": 3172, "FY2019": 1922}),
    ("DATA", "Fee and commission expense", {"FY2025": -1449, "FY2024": -2031, "FY2023": -2295, "FY2022": -1985, "FY2021": -1520, "FY2020": -932, "FY2019": -503}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 3112, "FY2024": 2046, "FY2023": 2053, "FY2022": 2402, "FY2021": 2701, "FY2020": 2240, "FY2019": 1419}),
    ("DATA", "Other operating income/(expense)", {"FY2025": -84, "FY2024": 47, "FY2023": -49, "FY2022": 54, "FY2021": 232, "FY2020": -8, "FY2019": 127}),
    ("TOTAL", "Total income", {"FY2025": 61603, "FY2024": 57338, "FY2023": 55645, "FY2022": 47860, "FY2021": 39108, "FY2020": 34552, "FY2019": 20800}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Personnel expenses", {"FY2025": -21508, "FY2024": -21310, "FY2023": -18185, "FY2022": -14704, "FY2021": -12087, "FY2020": -10384, "FY2019": -6603}),
    ("DATA", "Other administrative expenses", {"FY2025": -21626, "FY2024": -25393, "FY2023": -23177, "FY2022": -18093, "FY2021": -16384, "FY2020": -15165, "FY2019": -9829}),
    ("TOTAL", "Operating expenses", {"FY2025": -43134, "FY2024": -46703, "FY2023": -41362, "FY2022": -32797, "FY2021": -28471, "FY2020": -25549, "FY2019": -16432}),
    ("DATA", "Impairment loss on financial instruments", {"FY2025": -294, "FY2024": -3665, "FY2023": -11368, "FY2022": -4862, "FY2021": -2159, "FY2020": -2972, "FY2019": -87}),
    ("TOTAL", "Profit on ordinary activities before tax", {"FY2025": 18175, "FY2024": 6970, "FY2023": 2915, "FY2022": 10201, "FY2021": 8478, "FY2020": 6031, "FY2019": 4281}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": -4247, "FY2024": -1467, "FY2023": -127, "FY2022": -997, "FY2021": -637, "FY2020": -390, "FY2019": -618}),
    ("TOTAL", "Profit and total comprehensive income for the year", {"FY2025": 13928, "FY2024": 5503, "FY2023": 2788, "FY2022": 9204, "FY2021": 7841, "FY2020": 5641, "FY2019": 3663}),
]

bw.add_income_statement_sheet(
    title="Triodos Bank UK Limited — Profit & Loss",
    subtitle="TBUK entity-level (Company) basis, £'000. All profits are from continuing activities and TBUK "
              "discloses no other comprehensive income in any year - Profit for the year equals Total "
              "comprehensive income for the year exactly, every year. FY2025's own P&L bottom line (£13,928k) "
              "has a genuine £2k gap against the Statement of Changes in Equity sheet's own FY2025 movement "
              "figure (£13,930k) - see source note, not a transcription error. FY2019 covers only 8 months of "
              "trading (1 May-31 Dec 2019, see source note) - not comparable run-rate to other years. AR2019's "
              "own line was labelled 'Co-worker expenses'; unified onto this workbook's 'Personnel expenses' "
              "row as the same underlying measure used in later years.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity - chronological, ties to the
# Balance Sheet sheet's own Total equity every year (FY2020-FY2024 exactly;
# FY2025 has the documented £4k gap - see STATEMENTS_SOURCES). Starts at
# incorporation (23 May 2018, TBUK's only pre-trading equity event - see
# ENTITY_NOTE on why FY2018 has no column of its own elsewhere in this
# workbook). One documented restatement gap at the FY2019/FY2020 boundary
# (AR2020's own opening balance for FY2020 does not equal AR2019's own
# closing balance for FY2019 - a genuine £7k gap, see the labelled
# adjustment row below, not a plug). Otherwise zero undocumented plug rows
# - only 'Profit for the year', 'Prior year dividend paid', and (FY2019
# only) the one-off Part VII transfer items ever move equity; no treasury
# shares, share-based payments, or FX reserve movements appear anywhere in
# this note.
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Called up share capital", "Merger reserve", "Retained earnings", "Total"]

equity_rows = [
    ("DATA", "Issue of share capital on incorporation (23 May 2018)", (1, None, None, 1)),
    ("TOTAL", "Balance at 31 December 2018 (dormant, pre-trading)", (1, None, None, 1)),
    ("DATA", "Issue of share capital (Part VII transfer)", (171999, None, None, 171999)),
    ("DATA", "Impact of Part VII transfer (merger reserve)", (None, 55, None, 55)),
    ("DATA", "Profit and total comprehensive income for the year/period", (None, None, 3663, 3663)),
    ("TOTAL", "Balance at 31 December 2019 (per AR2019)", (172000, 55, 3663, 175718)),
    ("DATA", "Restatement adjustment (AR2020's restated FY2019 comparative vs AR2019's own figures - genuine £7k gap, not a plug - see STATEMENTS_SOURCES)", (None, None, -7, -7)),
    ("TOTAL", "Balance at 1 January 2020 (per AR2020, restated)", (172000, 55, 3656, 175711)),
    ("DATA", "Total profit and comprehensive income for the year", (None, None, 5641, 5641)),
    ("TOTAL", "Balance at 31 December 2020 / 1 January 2021", (172000, 55, 9297, 181352)),
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
    subtitle="TBUK entity-level (Company) basis, £'000, chronological (oldest to newest), starting from "
              "incorporation. FY2019's own closing balance (£175,718k, per AR2019) does not equal FY2020's own "
              "opening balance (£175,711k, per AR2020) - a genuine documented £7k restatement gap between "
              "report vintages, shown as its own labelled row, not silently plugged. FY2021-FY2024 closing "
              "balances otherwise tie exactly to the Balance Sheet sheet's own Total equity; FY2025's closing "
              "balance here (£208,618k) has a genuine £4k gap against the Balance Sheet's own stated FY2025 "
              "Total equity (£208,622k) - see source note, reproduced exactly as this statement states it, not "
              "silently reconciled.",
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
    ("DATA", "Profit before tax", {"FY2025": 18175, "FY2024": 6970, "FY2023": 2915, "FY2022": 10201, "FY2021": 8478, "FY2020": 6031, "FY2019": 4281}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 388, "FY2024": 1082, "FY2023": 1045, "FY2022": 1022, "FY2021": 980, "FY2020": 895, "FY2019": 527}),
    ("DATA", "(Gain)/Loss on fixed asset disposal", {"FY2023": 20, "FY2022": 5, "FY2021": 0, "FY2020": 6}),
    ("DATA", "Debt securities premium and discount amortisation", {"FY2025": -5116, "FY2024": -4528, "FY2023": -1710, "FY2022": 82, "FY2021": 1509, "FY2020": 1182, "FY2019": 772}),
    ("DATA", "Increase in interest receivable on debt securities", {"FY2025": -2225, "FY2024": -2163}),
    ("DATA", "Increase/(Decrease) in ECL on financial instruments", {"FY2025": -1246, "FY2024": -3590, "FY2023": -787, "FY2022": 4262, "FY2021": 2268, "FY2020": 1721}),
    ("DATA", "Net impairment loss on financial instruments (FY2019's own distinct label - see source note)", {"FY2019": 64}),
    ("DATA", "Write off of financial instruments", {"FY2025": 1539, "FY2024": 7229, "FY2023": 12308, "FY2022": 0}),
    ("DATA", "Increase/(Decrease) in provisions", {"FY2025": -531, "FY2024": 820, "FY2023": -80, "FY2022": -527, "FY2021": 199, "FY2020": 174, "FY2019": -237}),
    ("DATA", "Interest on lease liabilities", {"FY2025": 16, "FY2024": 29, "FY2023": 39, "FY2022": 36, "FY2021": 28, "FY2020": 39, "FY2019": 13}),
    ("DATA", "Tax expense", {"FY2025": -4247, "FY2024": -1467, "FY2023": -127, "FY2022": -997, "FY2021": -637, "FY2020": -390, "FY2019": -618}),
    ("TOTAL", "Cash flow from business operations", {"FY2025": 6753, "FY2024": 4382, "FY2023": 13623, "FY2022": 14084, "FY2021": 12825, "FY2020": 9658, "FY2019": 4789}),
    ("DATA", "Increase/(Decrease) in loans and advances to customers", {"FY2025": -10208, "FY2024": 19325, "FY2023": -1593, "FY2022": 6563, "FY2021": -64020, "FY2020": -96953, "FY2019": -101865}),
    ("DATA", "Increase/(Decrease) in deferred tax asset", {"FY2025": -70, "FY2024": 34, "FY2023": -53, "FY2022": 3, "FY2021": -77, "FY2020": 10, "FY2019": 37}),
    ("DATA", "Increase/(Decrease) in other assets", {"FY2025": -171, "FY2024": 252, "FY2023": -660, "FY2022": 604, "FY2021": 730, "FY2020": 6383, "FY2019": -4924}),
    ("DATA", "Increase/(Decrease) in deposits from credit institutions", {"FY2025": -2983, "FY2024": -5265, "FY2023": -6684, "FY2022": -3207, "FY2021": -6243, "FY2020": -2114, "FY2019": 3056}),
    ("DATA", "Increase in deposits from customers", {"FY2025": 81761, "FY2024": 71951, "FY2023": 22145, "FY2022": 34303, "FY2021": 194863, "FY2020": 256795, "FY2019": 53008}),
    ("DATA", "Decrease in lease liabilities", {"FY2019": -25}),
    ("DATA", "Increase/(Decrease) in current tax liability", {"FY2025": 1728, "FY2024": 1117, "FY2023": -957, "FY2022": -66, "FY2021": 164, "FY2020": -381, "FY2019": 49}),
    ("DATA", "Increase/(Decrease) in other liabilities", {"FY2025": -3834, "FY2024": -5425, "FY2023": 6056, "FY2022": 2788, "FY2021": 667, "FY2020": -5283, "FY2019": 1521}),
    ("TOTAL", "Cash flow from operating activities (= business operations subtotal + changes above)", {"FY2025": 72976, "FY2024": 86371, "FY2023": 31877, "FY2022": 55072, "FY2021": 138909, "FY2020": 168115, "FY2019": -49128}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Transfer of business from Triodos Bank N.V. (one-off, Part VII transfer - see source note)", {"FY2019": 156471}),
    ("DATA", "Investment in intangible assets", {"FY2025": -132, "FY2024": -701, "FY2023": -5, "FY2022": -200, "FY2021": -85, "FY2020": 28, "FY2019": -33}),
    ("DATA", "Investment in property and equipment", {"FY2025": 502, "FY2024": -481, "FY2023": -294, "FY2022": -342, "FY2021": -254, "FY2020": -471, "FY2019": -129}),
    ("DATA", "(Increase)/decrease in interest receivable on debt securities", {"FY2023": -1777, "FY2022": 249, "FY2021": 49, "FY2020": -841}),
    ("DATA", "Investment in debt securities", {"FY2025": -240343, "FY2024": -183290, "FY2023": -162400, "FY2022": -106096, "FY2021": -138211, "FY2020": -61980, "FY2019": -24672}),
    ("DATA", "Sale of debt securities", {"FY2023": 0, "FY2022": 0, "FY2021": 5128}),
    ("DATA", "Maturity of debt securities", {"FY2025": 156285, "FY2024": 95000, "FY2023": 55000, "FY2022": 29000, "FY2021": 15500, "FY2020": 23900, "FY2019": 4800}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -83688, "FY2024": -89472, "FY2023": -109476, "FY2022": -77389, "FY2021": -117873, "FY2020": -39364, "FY2019": 136437}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid", {"FY2025": -5500, "FY2024": -1400, "FY2023": -2800, "FY2022": 0, "FY2021": -2300}),
    ("DATA", "Payment of lease liabilities", {"FY2025": -55, "FY2024": -175, "FY2023": -168, "FY2022": -160, "FY2021": -156, "FY2020": -140, "FY2019": -26}),
    ("DATA", "Increase in equity (share capital issued for Part VII transfer, one-off - see source note)", {"FY2019": 171999}),
    ("DATA", "Increase/(Decrease) in debt issued and borrowed funds", {"FY2025": -5736, "FY2024": 0, "FY2023": 3, "FY2022": -4, "FY2021": 33, "FY2020": 5703}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": -11291, "FY2024": -1575, "FY2023": -2965, "FY2022": -164, "FY2021": -2423, "FY2020": 5563, "FY2019": 171973}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -22003, "FY2024": -4676, "FY2023": -80564, "FY2022": -22481, "FY2021": 18613, "FY2020": 134314, "FY2019": 264070}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 309277, "FY2024": 313953, "FY2023": 394517, "FY2022": 416998, "FY2021": 398385, "FY2020": 264071, "FY2019": 1}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 287274, "FY2024": 309277, "FY2023": 313953, "FY2022": 394517, "FY2021": 416998, "FY2020": 398385, "FY2019": 264071}),
    ("SECTION", "Represented by (memo breakdown, not additional totals)", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 269090, "FY2024": 298593, "FY2023": 282378, "FY2022": 359906, "FY2021": 374820, "FY2020": 375679, "FY2019": 236613}),
    ("DATA", "On demand deposits with credit institutions", {"FY2025": 18184, "FY2024": 10684, "FY2023": 30472, "FY2022": 33412, "FY2021": 40979, "FY2020": 21405, "FY2019": 27057}),
    ("DATA", "Other loans and advances to credit institutions", {"FY2023": 1103, "FY2022": 1199, "FY2021": 1199, "FY2020": 1301, "FY2019": 401}),
]

bw.add_cash_flow_sheet(
    title="Triodos Bank UK Limited — Cash Flow Statement",
    subtitle="TBUK entity-level (Company) basis, £'000. See source note for the two-level operating subtotal, "
              "FY2019's one-off Part VII transfer items, and the FY2019/FY2020-vintage restatements.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=300,
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
    f"by-stage credit-quality table exists in this earlier report vintage), p.45-46 - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020, Note 27A(i) Credit quality analysis (Stage 1/2/3, by internal risk rating), "
    f"p.65 - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019, Note 26A(i) Credit quality analysis (Stage 1/2/3 + POCI, corporate and retail "
    f"customers shown separately), p.57 (covers 8 months of trading, see ENTITY_NOTE) - {AR2019_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nCONFIRMED NON-DISCLOSURE (not an access gap): AR2021's own notes were reviewed in full (Note 22 "
    "Provisions p.55-57, through Note 23 Called up share capital, Note 24 Related party transactions) and "
    "contain no separate stage/rating-based credit quality note - that disclosure format was introduced in a "
    "later report vintage. FY2021's Stage 1/2/3 and NPL/coverage ratio rows are therefore left blank rather "
    "than guessed.\n\n"
    "FY2019 STRUCTURAL DIFFERENCE: AR2019's own credit-quality note splits 'Loans and advances to corporate "
    "customers' and 'Loans and advances to retail customers' into separate Stage 1/2/3/POCI tables (POCI = "
    "purchased or originated credit-impaired - a category that does not appear in any later year's report). The "
    "Stage 1/2/3/POCI rows below are the corporate+retail COMBINED total (matching the FY2020-FY2025 sheets' "
    "single 'loans and advances to customers' scope). GENUINE INTERNAL AR2019 INCONSISTENCY: this note's own "
    "combined carrying-amount total (£975,151k = £975,037k corporate + £114k retail) does not equal AR2019's own "
    "Statement of financial position figure for the same balance (£975,025k, a £126k gap) - both are reproduced "
    "exactly as AR2019's own statement/note state them (see STATEMENTS_SOURCES), not reconciled."
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 1069935, "FY2024": 1061389, "FY2023": 1090721, "FY2022": 1104291, "FY2020": 879180, "FY2019": 937556}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 22764, "FY2024": 22323, "FY2023": 15718, "FY2022": 12724, "FY2020": 153348, "FY2019": 16220}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 15827, "FY2024": 14663, "FY2023": 13977, "FY2022": 12045, "FY2020": 41823, "FY2019": 18329}),
    ("DATA", "POCI - purchased or originated credit-impaired (FY2019 only, see source note)", {"FY2019": 5294}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 1108526, "FY2024": 1098375, "FY2023": 1120416, "FY2022": 1129060, "FY2020": 1074351, "FY2019": 977399}),
    ("SECTION", "ECL allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1 allowance", {"FY2025": 1657, "FY2024": 1584, "FY2023": 1653, "FY2022": 1602, "FY2020": 1220, "FY2019": 563}),
    ("DATA", "Stage 2 allowance", {"FY2025": 979, "FY2024": 963, "FY2023": 663, "FY2022": 557, "FY2020": 1520, "FY2019": 188}),
    ("DATA", "Stage 3 allowance", {"FY2025": 7556, "FY2024": 7415, "FY2023": 6723, "FY2022": 5596, "FY2020": 1225, "FY2019": 863}),
    ("DATA", "POCI allowance (FY2019 only)", {"FY2019": 635}),
    ("TOTAL", "Total ECL allowance", {"FY2025": 10192, "FY2024": 9962, "FY2023": 9039, "FY2022": 7755, "FY2020": 3965, "FY2019": 2249}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 1098334, "FY2024": 1088413, "FY2023": 1111377, "FY2022": 1121305, "FY2020": 1070386, "FY2019": 975151}),
    ("SECTION", "FY2021 product-level split (no by-stage table disclosed that year - see source note)", {}),
    ("DATA", "Corporate loans", {"FY2021": 1108956}),
    ("DATA", "Current accounts", {"FY2021": 23176}),
    ("TOTAL", "Total loans and advances to customers (gross, FY2021)", {"FY2021": 1132132}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross)", {"FY2025": "1.43%", "FY2024": "1.33%", "FY2023": "1.25%", "FY2022": "1.07%", "FY2020": "3.89%", "FY2019": "1.88%"}),
    ("DATA", "Coverage ratio (Total ECL allowance / Total gross)", {"FY2025": "0.92%", "FY2024": "0.91%", "FY2023": "0.81%", "FY2022": "0.69%", "FY2020": "0.37%", "FY2019": "0.23%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross)", {"FY2025": "47.74%", "FY2024": "50.57%", "FY2023": "48.10%", "FY2022": "46.46%", "FY2020": "2.93%", "FY2019": "4.71%"}),
]

bw.add_asset_quality_sheet(
    title="Triodos Bank UK Limited — Asset Quality",
    subtitle="TBUK entity-level (Company) basis, £'000. FY2020, FY2022-FY2024 tie exactly to Balance Sheet net "
              "loans and advances to customers; FY2025 has a £1k rounding gap. FY2019 uses AR2019's own "
              "credit-quality note total (£975,151k), which itself differs from AR2019's own Balance Sheet "
              "figure (£975,025k) by a genuine £126k internal gap - see source note. FY2021 uses the coarser "
              "product-level split only - no by-stage table exists in that year's report (confirmed "
              "non-disclosure, see source note).",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=72,
    source_height=320,
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
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 193448, "FY2024": 193259, "FY2023": 192544, "FY2022": 185772, "FY2021": 177905, "FY2020": 174426, "FY2019": 170452})],
    p3_sources(),
    note="FY2025 is from the Annual Report's own 'Total capital resources' note (Note 26/27, audited) since no "
         "FY2025 Pillar 3 report has been published yet - not derived, directly stated. FY2020 is directly stated "
         "in TBUK's own FY2020 Pillar 3 Report (Table 3); FY2019 has no standalone Pillar 3 report (see p3_sources "
         "note) so is taken from that same FY2020 Pillar 3 Report's own audited FY2019 comparative column, which "
         "the report itself states 'agrees to equity and reserves in the Annual Report' - an audited regulatory "
         "figure, not a narrative estimate. FY2019's own Annual Report separately confirms a CET1 ratio of 20.3% "
         "(matching this £170,452k capital figure against FY2019's own £840,575k RWA figure - see Total RWAs "
         "sheet), giving independent cross-verification.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "21.3%", "FY2024": "22.1%", "FY2023": "22.36%", "FY2022": "21.57%", "FY2021": "21.2%", "FY2020": "22.6%", "FY2019": "20.3%"})],
    p3_sources(),
    note="FY2025 is from the Annual Report narrative (p.15), stated as 21.3% (2024: 22.1%); FY2024's figure there "
         "(22.1%) rounds slightly differently from the FY2024 Pillar 3 Report's own Table 9 figure (22.06%) - both "
         "are as-stated in their respective source documents, not reconciled to more decimal places. FY2020 is "
         "from TBUK's own FY2020 Pillar 3 Report (Table 4); FY2019 is that same report's own audited FY2019 "
         "comparative column, independently corroborated by AR2019's own narrative statement ('Triodos Bank UK "
         "ended the year with a CET1 ratio of 20.3%').",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 193448, "FY2024": 193259, "FY2023": 192544, "FY2022": 185772, "FY2021": 177905, "FY2020": 174426, "FY2019": 170452})],
    p3_sources(),
    note="TBUK has no Additional Tier 1 (AT1) instruments in any year - Tier 1 capital equals CET1 capital exactly, "
         "every year, per the Annual Report's own 'Total capital resources' table (e.g. FY2025/FY2024: 'CET1 and "
         "Total Tier 1 capital resources' is a single stated line). FY2020/FY2019 sourced the same way as CET1 "
         "Capital above.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "21.3%", "FY2024": "22.1%", "FY2023": "22.36%", "FY2022": "21.57%", "FY2021": "21.2%", "FY2020": "22.6%", "FY2019": "20.3%"})],
    p3_sources(),
    note="Numerically identical to the CET1 ratio every year, since Tier 1 capital = CET1 capital (no AT1 "
         "instruments) - not a separate disclosure.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 193448, "FY2024": 198954, "FY2023": 198239, "FY2022": 191467, "FY2021": 183600, "FY2020": 180121, "FY2019": 170452})],
    p3_sources(),
    note="Total capital = CET1 + Tier 2 (subordinated debt, £5.7m issued Dec 2020). The Tier 2 note was fully "
         "repaid in 2025, so FY2025 Total capital equals CET1 exactly for the first time in this series. FY2019 "
         "also equals CET1 exactly, but for the opposite reason - the Tier 2 subordinated debt was not issued "
         "until 23 December 2020, so FY2019 (and FY2020's own opening position) simply predates it.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "21.3%", "FY2024": "22.7%", "FY2023": "23.02%", "FY2022": "22.20%", "FY2021": "21.8%", "FY2020": "23.4%", "FY2019": "20.3%"})],
    p3_sources(),
    note="FY2025/FY2024 from the Annual Report narrative (p.15); FY2024's Pillar 3 Report states this ratio as "
         "22.71% (Table 7) - a minor rounding difference from the Annual Report's 22.7%, both as-stated. FY2020 "
         "is from TBUK's own FY2020 Pillar 3 Report (Table 4); FY2019 (that report's own comparative column) "
         "equals its CET1 ratio exactly since TBUK had no Tier 2 capital yet that year (see Total Capital note).",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets (credit + operational + market + counterparty credit risk)",
      {"FY2025": 908207, "FY2024": 876076, "FY2023": 861016, "FY2022": 861273, "FY2021": 840391, "FY2020": 770444, "FY2019": 840575})],
    p3_sources(),
    note="FY2025 is CALCULATED (Total capital £193,448k / Total capital ratio 21.3% = ~£908.2m), not directly "
         "stated, since no FY2025 Pillar 3 report exists yet to give the audited RWA breakdown - simple arithmetic "
         "on two audited/stated figures, not an estimate, flagged per this project's convention (see Bank of "
         "Ireland UK workbook for the same approach). FY2024-FY2020 are Total RWA figures directly stated in each "
         "year's own Pillar 3 Report (Credit + Operational risk RWA; Market risk and Counterparty Credit risk RWA "
         "are nil every year). FY2019 is that same FY2020 Pillar 3 Report's own audited FY2019 comparative column "
         "(Table 4/6) - no standalone FY2019 Pillar 3 report exists (see p3_sources note). FY2019's £840,575k is "
         "coincidentally close to but distinct from FY2021's £840,391k - not a duplication error, both years' own "
         "figures independently confirmed from their respective source tables.",
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Triodos Bank UK Limited (TBUK) entity-level Pillar 3 RWA breakdown (UK OV1-style table):\n"
    f"FY2024: Triodos Bank UK Limited 2024 Pillar 3 Report, 'TBUK RWAs and Capital Ratios' table - {P3_2024_URL}\n"
    f"FY2023: Triodos Bank UK Limited 2023 Pillar 3 Report, 'TBUK RWAs and Capital Ratios' table - {P3_2023_URL}\n"
    f"FY2022: Triodos Bank UK Limited 2022 Pillar 3 Report, 'TBUK RWAs and Capital Ratios' table - {P3_2022_URL}\n"
    f"FY2021: Triodos Bank UK Limited 2021 Pillar 3 Report, Table 7 (Overview of RWAs by exposure class) - "
    f"{P3_2021_URL}\n"
    f"FY2020: Triodos Bank UK Limited 2020 Pillar 3 Report, Table 6 (Overview of RWAs, template EU OV1) - "
    f"{P3_2020_URL}\n"
    f"FY2019: that same FY2020 Pillar 3 Report's own audited FY2019 comparative column (Table 6) - no standalone "
    f"FY2019 Pillar 3 report exists (see p3_sources note) - {P3_2020_URL}\n"
    "FY2025: no standalone Pillar 3 report has been published yet as of this workbook's build date - blank, "
    "consistent with every other Pillar 3 sheet in this workbook.\n"
    "PRESENTATION NOTE: FY2019-FY2021's own Pillar 3 Reports all combine Credit risk and Counterparty Credit risk "
    "into a single exposure-class table (no separate CCR line existed as a distinct category in these earlier "
    "report vintages; the split first appears in the FY2022 Pillar 3 Report) - kept as a single combined row "
    "exactly as each of those years' own reports presented it, not split. FY2019/FY2020 also carry an 'Amounts "
    "below thresholds for deduction' line (subject to 250% risk weight) that does not appear as its own row in "
    "FY2021-FY2024's tables - shown here exactly as FY2019/FY2020's own tables presented it, not merged into "
    "another category. All years' category sums tie exactly to the pre-existing Total RWAs figures on the Total "
    "RWAs sheet.\n\n"
    + ENTITY_NOTE
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk RWA", {"FY2024": 806870, "FY2023": 799630, "FY2022": 799316}),
    ("DATA", "Credit and Counterparty Credit risk RWA (combined, FY2019-FY2021 basis)", {"FY2021": 780882, "FY2020": 709757, "FY2019": 782823}),
    ("DATA", "Counterparty Credit risk RWA", {"FY2024": 0, "FY2023": 0, "FY2022": 0}),
    ("DATA", "Market risk RWA", {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0}),
    ("DATA", "Operational risk RWA", {"FY2024": 69206, "FY2023": 61386, "FY2022": 61957, "FY2021": 59509, "FY2020": 59395, "FY2019": 54922}),
    ("DATA", "Amounts below thresholds for deduction (250% risk weight)", {"FY2020": 1291, "FY2019": 2830}),
    ("TOTAL", "Total RWAs", {"FY2024": 876076, "FY2023": 861016, "FY2022": 861273, "FY2021": 840391, "FY2020": 770444, "FY2019": 840575}),
]

bw.add_rwa_breakdown_sheet(
    title="Triodos Bank UK Limited — RWA Breakdown",
    subtitle="TBUK entity-level basis, £'000. Category sums tie exactly to the Total RWAs sheet's own figures "
              "for every year with a Pillar 3 report. FY2019-FY2021's Credit and Counterparty Credit risk are "
              "combined as those years' own reports presented them (see source note); FY2019/FY2020 also carry "
              "an 'Amounts below thresholds for deduction' line not present in later years. No FY2025 Pillar 3 "
              "report exists yet, consistent with the rest of this workbook's Pillar 3 sheets.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Tier 1 capital after deductions", {"FY2024": 193258, "FY2023": 192544, "FY2022": 185772, "FY2021": 177905, "FY2020": 174426, "FY2019": 170452}),
        ("Leverage ratio exposure measure", {"FY2024": 1715067, "FY2023": 1664149, "FY2022": 1583516, "FY2021": 1910203, "FY2020": 1728069, "FY2019": 1460566}),
        ("Leverage ratio (%)", {"FY2024": "11.27%", "FY2023": "11.57%", "FY2022": "11.73%", "FY2021": "9.3%", "FY2020": "10.1%", "FY2019": "11.7%"}),
    ],
    p3_sources(),
    note="TBUK is below the £50bn deposit threshold that triggers a binding UK leverage ratio requirement (PRA "
         "expectation only, minimum 3.25%). FY2022 onward uses the 'excluding claims on central banks' exposure "
         "basis (introduced in the 2022 Pillar 3 Report); FY2019-FY2021 all used a broader, non-comparable CRR2 "
         "full-exposure basis (including central bank claims) - shown here exactly as each of those years' own "
         "reports stated it, NOT a later report's restated comparative, consistent with this project's practice "
         "of not blending non-comparable methodology vintages. FY2020's figures are directly stated in TBUK's own "
         "FY2020 Pillar 3 Report (Table 14/15); FY2019's are that same report's own audited FY2019 comparative "
         "column (no standalone FY2019 Pillar 3 report exists - see p3_sources note). No FY2025 figure: not "
         "disclosed in the Annual Report and no FY2025 Pillar 3 report exists yet.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total HQLA (point-in-time, year-end)", {"FY2024": 826600, "FY2023": 715900, "FY2022": 668900, "FY2021": 628207, "FY2020": 519500}),
        ("Total net cash outflows over 30-day stress (point-in-time, year-end)", {"FY2024": 175400, "FY2023": 170100, "FY2022": 151100, "FY2021": 151875, "FY2020": 125400}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "446%", "FY2024": "471.1%", "FY2023": "420.8%", "FY2022": "442.7%", "FY2021": "413.6%", "FY2020": "414.1%"}),
    ],
    p3_sources(),
    note="All ratios are the year-end point-in-time LCR (not the 12-month average-by-quarter tables each Pillar 3 "
         "report also separately discloses). FY2025's ratio (446%) is from the Annual Report narrative only (p.15) "
         "- no £ HQLA/outflow breakdown is available since no FY2025 Pillar 3 report exists yet. FY2020's figures "
         "are from TBUK's own FY2020 Pillar 3 Report's narrative ('As at 31 December 2020, the Bank's LCR was at "
         "414.1%...calculated as a total HQLA of £519.5m against net outflows of £125.4m'). FY2019: NOT DISCLOSED "
         "- no standalone FY2019 Pillar 3 report exists, the FY2020 Pillar 3 Report's own Table 17 quarterly "
         "series only starts at 31-Mar-2020 (and is itself a 12-month-average basis, not point-in-time - see the "
         "same caveat already noted for other years' average tables), and AR2019's own Liquidity section gives "
         "only a qualitative statement ('significantly in excess of all liquidity targets and requirements') with "
         "no numeric LCR% - genuinely not disclosed anywhere reviewed, not an access gap.",
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
         "not a strict point-in-time balance, so is not fully comparable to the other years' figures. FY2021 and "
         "FY2020: no NSFR section appears in either year's own Pillar 3 Report at all (the metric was not yet "
         "part of that era's disclosure - both reports' full contents pages were reviewed to confirm this). "
         "FY2019: no standalone Pillar 3 report exists for FY2019 at all (see p3_sources note), and AR2019 gives "
         "no NSFR figure either. FY2025: not disclosed - no FY2025 Pillar 3 report exists yet and the Annual "
         "Report gives no NSFR percentage (only confirms the ratio is monitored).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "No MREL figure or qualitative MREL disclosure appears in any of TBUK's Annual Reports or "
                      "Pillar 3 Reports (FY2019-FY2024) - not asserted as an explicit exemption, simply absent "
                      "from every source reviewed, consistent with several other small banks in this project "
                      "series (e.g. Zopa, LHV, Vida).",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 2043128, "FY2024": 1964329, "FY2023": 1897815, "FY2022": 1876832, "FY2021": 1834464, "FY2020": 1639370, "FY2019": 1378369}),
        ("Total liabilities", {"FY2025": 1834506, "FY2024": 1764141, "FY2023": 1701730, "FY2022": 1680735, "FY2021": 1647571, "FY2020": 1458018, "FY2019": 1202652}),
        ("Total equity", {"FY2025": 208622, "FY2024": 200188, "FY2023": 196085, "FY2022": 196097, "FY2021": 186893, "FY2020": 181352, "FY2019": 175718}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {"FY2025": 61603, "FY2024": 57338, "FY2023": 55645, "FY2022": 47860, "FY2021": 39108, "FY2020": 34552, "FY2019": 20800}),
        ("Profit on ordinary activities before tax", {"FY2025": 18175, "FY2024": 6970, "FY2023": 2915, "FY2022": 10201, "FY2021": 8478, "FY2020": 6031, "FY2019": 4281}),
        ("Profit and total comprehensive income for the year", {"FY2025": 13928, "FY2024": 5503, "FY2023": 2788, "FY2022": 9204, "FY2021": 7841, "FY2020": 5641, "FY2019": 3663}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 200188, "FY2024": 196085, "FY2023": 196097, "FY2022": 186893, "FY2021": 181352, "FY2020": 175711, "FY2019": 1}),
        ("Profit for the year", {"FY2025": 13930, "FY2024": 5503, "FY2023": 2788, "FY2022": 9204, "FY2021": 7841, "FY2020": 5641, "FY2019": 3663}),
        ("Other equity movements, net", {"FY2025": -5500, "FY2024": -1400, "FY2023": -2800, "FY2022": 0, "FY2021": -2300, "FY2020": 0, "FY2019": 172054}),
        ("Closing equity", {"FY2025": 208618, "FY2024": 200188, "FY2023": 196085, "FY2022": 196097, "FY2021": 186893, "FY2020": 181352, "FY2019": 175718}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Cash flow from operating activities", {"FY2025": 72976, "FY2024": 86371, "FY2023": 31877, "FY2022": 55072, "FY2021": 138909, "FY2020": 168115, "FY2019": -49128}),
        ("Net cash from/(used in) investing activities", {"FY2025": -83688, "FY2024": -89472, "FY2023": -109476, "FY2022": -77389, "FY2021": -117873, "FY2020": -39364, "FY2019": 136437}),
        ("Net cash from/(used in) financing activities", {"FY2025": -11291, "FY2024": -1575, "FY2023": -2965, "FY2022": -164, "FY2021": -2423, "FY2020": 5563, "FY2019": 171973}),
        ("Cash and cash equivalents at end of year", {"FY2025": 287274, "FY2024": 309277, "FY2023": 313953, "FY2022": 394517, "FY2021": 416998, "FY2020": 398385, "FY2019": 264071}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "21.3%", "FY2024": "22.1%", "FY2023": "22.36%", "FY2022": "21.57%", "FY2021": "21.2%", "FY2020": "22.6%", "FY2019": "20.3%"}),
        ("Tier 1 Ratio", {"FY2025": "21.3%", "FY2024": "22.1%", "FY2023": "22.36%", "FY2022": "21.57%", "FY2021": "21.2%", "FY2020": "22.6%", "FY2019": "20.3%"}),
        ("Total Capital Ratio", {"FY2025": "21.3%", "FY2024": "22.7%", "FY2023": "23.02%", "FY2022": "22.20%", "FY2021": "21.8%", "FY2020": "23.4%", "FY2019": "20.3%"}),
        ("Leverage Ratio", {"FY2024": "11.27%", "FY2023": "11.57%", "FY2022": "11.73%", "FY2021": "9.3%", "FY2020": "10.1%", "FY2019": "11.7%"}),
        ("LCR", {"FY2025": "446%", "FY2024": "471.1%", "FY2023": "420.8%", "FY2022": "442.7%", "FY2021": "413.6%", "FY2020": "414.1%"}),
        ("NSFR", {"FY2024": "206%", "FY2023": "188%", "FY2022": "181%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. No FY2025 Pillar 3 report has been published yet, so Leverage "
         "Ratio and NSFR are blank for FY2025 (Total RWAs on that sheet is a calculated figure for FY2025 - see "
         "its own note). TBUK does not take the FRS 101/102 cash-flow exemption used by several other single-"
         "parent foreign subsidiary banks in this project - a full Statement of Cash Flows exists for all 7 years "
         "(FY2019-FY2025). FY2019 covers only 8 months of trading (see ENTITY_NOTE, and the Cash Flow sheet's own "
         "one-off Part VII transfer items) - not comparable run-rate to other years. FY2019's 'Opening equity' "
         "(£1k) is TBUK's dormant pre-trading balance sheet; its 'Other equity movements' (£172,054k) is the one-"
         "off share capital issued plus merger reserve created by the Part VII transfer, not a recurring item. "
         "FY2020's 'Opening equity' (£175,711k) uses AR2020's own restated FY2019 closing figure, not AR2019's "
         "own closing figure (£175,718k) - a genuine £7k gap, see the Statement of Changes in Equity sheet's own "
         "note. LCR and NSFR are blank for FY2019 - neither was disclosed anywhere reviewed for that year (see "
         "each metric's own sheet note).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/TRIODOS FINANCIALS.xlsx")
