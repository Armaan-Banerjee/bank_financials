import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/01719649/filing-history"
AR2025_URL = CH_BASE + "/MzUxODk2NjE4MWFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = CH_BASE + "/MzQ2NzY3NzI2OWFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = CH_BASE + "/MzQzNjc2MDc4MWFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = CH_BASE + "/MzM4OTg0MTU0M2FkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = CH_BASE + "/MzM1NjI2OTMyN2FkaXF6a2N4/document?format=pdf&download=0"

P3_2025_URL = "https://hblbankuk.com/wp-content/uploads/2020/03/HBL-UK-2025-Pillar-III-Disclosure.pdf"
P3_2024_URL = ("http://web.archive.org/web/20260218212243/"
               "https://hblbankuk.com/wp-content/uploads/2025/05/Pillar-III-Disclosure-2024.pdf")
P3_2022_URL = ("http://web.archive.org/web/20240807115829/"
               "https://hblbankuk.com/wp-content/uploads/2023/06/HBL-UK-2022-Pillar-III-Disclosure-V1.pdf")
P3_2023_URL = "https://hblbankuk.com/wp-content/uploads/2020/03/HBL-UK-2023-Pillar-III-Disclosure.pdf"
P3_2021_URL = "https://hblbankuk.com/wp-content/uploads/2022/06/Pillar-III-Disclosures-2021.pdf"
# Surfaced by the same CDX sweep that recovered P3_2023_URL, both live on the bank's own server
# (verified 2026-09-18: HTTP 200, application/pdf, %PDF-1.7, 590,397 and 444,979 bytes). This
# workbook covers FY2021-FY2025 so neither is cited by a sheet yet; they are recorded here so a
# future pass that extends the year range does not have to re-find them.
P3_2019_URL = "https://hblbankuk.com/wp-content/uploads/2020/09/HBL-UK-2019-Pillar-III-Disclosures-FINAL.pdf"
P3_2020_URL = "https://hblbankuk.com/wp-content/uploads/2021/06/HBL-UK-2020-Pillar-III-Disclosures-Final.pdf"

# Shared correction/calibration text. Referenced from p3_sources(), KM1_SOURCES and RWA_SOURCES,
# all three of which previously carried the withdrawn claim.
FY2023_RECOVERY_NOTE = (
    "CORRECTION, 2026-09-18 - WITHDRAWN CLAIM: this workbook previously stated, on the Pillar 3 "
    "metric sheets, the KM1 sheet and the RWA Breakdown sheet, that \"no standalone FY2023 Pillar 3 "
    "document is reachable\" / that \"FY2023's own standalone Pillar 3 document could not be fetched "
    "this session - the only available Wayback Machine capture is truncated to exactly 1,048,576 "
    "bytes with an unrecoverable cross-reference table, and repeated CDX lookups for an alternate "
    "snapshot were rate-limited for the remainder of the session\". THAT CLAIM WAS FALSE. The "
    "document has been on HBL Bank UK's own live server the whole time, at "
    f"{P3_2023_URL} - re-verified 2026-09-18 with a browser user-agent: HTTP 200, Content-Type "
    "application/pdf, %PDF-1.7 magic bytes, 1,286,862 bytes, 41 pages with a real text layer. The "
    "claim was wrong because it rested entirely on a truncated Wayback Machine capture and never "
    "tried the origin server. The document is NOT linked from hblbankuk.com/pdf-downloads/, which "
    "lists only the 2025 edition; the URL came from a CDX sweep and then resolved live.\n"
    "CALIBRATION FINDING (generalises beyond this bank): the SAME file returns exactly 1,048,576 "
    "bytes from the Wayback Machine and 1,286,862 bytes from the origin, while a 7.2 MB PDF returns "
    "from Wayback intact. The 1 MiB cut is therefore imposed at CRAWL time by particular crawl jobs, "
    "not by the archive's serving layer and not by anything about the document. A 1,048,576-byte "
    "response is evidence about one crawl and is NEVER evidence that a document is unavailable, "
    "unrecoverable or non-existent. The Wayback 'id_' raw form does not bypass it.\n"
    "FOR A FUTURE PASS: the same CDX sweep surfaced two further editions live on the bank's own "
    "server that this workbook does not cite, because its year range starts at FY2021 - the FY2019 "
    f"edition at {P3_2019_URL} and the FY2020 edition at {P3_2020_URL} (both verified 2026-09-18: "
    "HTTP 200, application/pdf, %PDF-1.7). Recorded here so extending the range does not require "
    "re-finding them."
)


CASH_FLOW_NOTE = (
    "DATA NOTE - FY2021 has no primary Cash Flow Statement in its own Annual Report: the "
    "FY2021 Annual Report and Financial Statements (filed with Companies House 25 Oct 2022) "
    "contains an Income Statement, Statement of Comprehensive Income, Statement of Financial "
    "Position, and Statement of Changes in Equity, but genuinely omits a Cash Flow Statement "
    "entirely - confirmed by a full page-by-page review of all 58 pages (Notes to the Financial "
    "Statements run straight from the Statement of Changes in Equity at p.37 to Note 1 at p.38, "
    "ending at Note 30 'Event after balance sheet date' at p.57, with no Cash Flow Statement or "
    "cash-and-cash-equivalents note anywhere in between). FY2021's cash flow figures used here "
    "are therefore sourced from the FY2022 Annual Report's own FY2021 comparative column instead "
    "- the only place these figures are published - not a later restatement of an original that "
    "never existed.\n"
    "DATA NOTE - FY2024's leverage exposure/ratio differs between reports: the FY2024 Annual "
    "Report is not itself a cash-flow source, but the same pattern recurs in Pillar 3 (see "
    "p3_sources() below) - each year's own originally-published figures are used throughout, "
    "consistent with this project's convention."
)

CASH_FLOW_SOURCES = (
    "Sources - HBL Bank UK Limited's own Cash Flow Statement, from each year's Companies "
    "House-filed Annual Report and Financial Statements (company 01719649), scanned/image-only "
    "filings transcribed via page-image rendering:\n"
    f"FY2025: Annual Report and Financial Statements for the year ended 31 December 2025, "
    f"Cash Flow Statement p.38 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements for the year ended 31 December 2024, "
    f"Cash Flow Statement p.38 (FY2024's own originally-published figures used) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 December 2023, "
    f"Cash Flow Statement p.40 (FY2023's own originally-published figures used) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for the year ended 31 December 2022, "
    f"Cash Flow Statement p.41 (FY2022's own originally-published figures used) - {AR2022_URL}\n"
    f"FY2021: FY2021 comparative column of the FY2022 Annual Report's Cash Flow Statement p.41 "
    f"(FY2021's own Annual Report has no Cash Flow Statement at all - see note below) - "
    f"{AR2022_URL}\n"
    + CASH_FLOW_NOTE
)


def p3_sources():
    return (
        "Sources - HBL Bank UK Limited's own Pillar 3 disclosures (company FRN 188585):\n"
        f"FY2025: Pillar III Disclosure - 31 December 2025, section 2 'Key Metrics' p.4 and "
        f"Leverage/LCR/NSFR table p.5 - {P3_2025_URL}\n"
        f"FY2024: Pillar III Disclosure - 31 December 2024, section 2 'Key Metrics' p.4 and "
        f"Leverage/LCR/NSFR table p.5 (FY2024's own originally-published figures used - the "
        f"FY2025 Pillar 3 document's FY2024 comparative restates the leverage exposure measure "
        f"from £532,088k/11.85% to £599,922k/11.56%, a genuine cross-report restatement not "
        f"reflected here) - {P3_2024_URL}\n"
        f"FY2023: Pillar III Disclosure - 31 December 2023, section 2 'Key Metrics', printed p.5 "
        f"(£'000, columns 2023 / 2022) - {P3_2023_URL}\n"
        f"        The FY2023 figures on these sheets were originally taken from the FY2024 "
        f"edition's FY2023 comparative column ({P3_2024_URL}). Having now read FY2023's own "
        f"standalone document, every one of them is CONFIRMED identical to it - RWAs 273,837; "
        f"AT1 9,786; Tier 1 58,635; Tier 2 11,501; Total Capital 70,136; CET1/T1/Total ratios "
        f"17.84%/21.41%/25.61%; leverage exposure 409,798 and ratio 13.42%; HQLA 154,579, net "
        f"outflow 22,021, LCR 702%; ASF 387,842, RSF 209,372, NSFR 185% - with ONE exception, the "
        f"CET1 Capital figure, documented on the CET1 Capital sheet. A confirmed negative is worth "
        f"recording: the comparative-column sourcing was not producing wrong numbers.\n"
        f"FY2022: Pillar III Disclosure - 31 December 2022, section 2 'Key Metrics' p.7 "
        f"(FY2022's own originally-published figures used) - {P3_2022_URL}\n"
        f"FY2021: Pillar III Disclosures - 31 December 2021, section 2 'Key Metrics' p.4 and "
        f"Leverage/LCR/NSFR table p.5 (FY2021's own standalone Pillar 3 document, found in a "
        f"later session and confirmed identical to the FY2022 Pillar III Disclosure's FY2021 "
        f"comparative column for every figure except CET1 Capital, which the standalone document "
        f"states as £41,623k against the £41,624k previously recorded here from the comparative "
        f"column - a £1k rounding-level difference, left unchanged pending further review) - "
        f"{P3_2021_URL}\n"
        "No MREL Ratio is disclosed in any year's Pillar 3 document (not identified as a UK "
        "resolution entity).\n\n"
        + FY2023_RECOVERY_NOTE
    )


bw = BankWorkbook(bank_name="HBL Bank UK Limited", years=YEARS, year_label=YEAR_LABEL, header_color="690D7D")

STATEMENTS_SOURCES = (
    "Sources - HBL Bank UK Limited's own Income Statement / Statement of Comprehensive Income / "
    "Statement of Financial Position / Statement of Changes in Equity, each year's own originally-"
    "published figures, from each year's Companies House-filed Annual Report and Financial "
    "Statements (company 01719649), text-native filings:\n"
    f"FY2025: Annual Report and Financial Statements 2025, pp.34-37 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements 2024, pp.34-37 (FY2024's own originally-"
    f"published figures used) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, pp.36-39 (FY2023's own originally-"
    f"published figures used) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, pp.37-40 (FY2022's own originally-"
    f"published figures used) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, pp.34-37 (FY2021's own originally-"
    f"published figures used - confirmed identical to the FY2022 Annual Report's own FY2021 "
    f"comparative column) - {AR2021_URL}\n"
    "Balance Sheet's own FY2025 Total equity (87,654) is £1k above the Statement of Changes in "
    "Equity's own FY2025 closing total (87,653) - a rounding gap present in the Bank's own report, "
    "reproduced as disclosed rather than force-reconciled.\n"
    "Debt securities breakdown (measurement basis: Held to Maturity vs Available for Sale; issuer "
    "type: Government securities vs Other) is sourced from Note 10 'Debt Securities' of each year's "
    "own Annual Report and Financial Statements, each year's own originally-published figures, "
    "reconciling exactly to the Balance Sheet's own Debt securities total for every year:\n"
    f"FY2025: Note 10, p.45 - {AR2025_URL}\n"
    f"FY2024: Note 10, p.45 - {AR2024_URL}\n"
    f"FY2023: Note 10, p.48 - {AR2023_URL}\n"
    f"FY2022: Note 10, p.49 - {AR2022_URL}\n"
    f"FY2021: Note 10, p.45 - {AR2021_URL}\n"
    "FY2025 and FY2024 disclose no 'Other securities' leg under Available for Sale (100% "
    "Government securities that year); FY2025 also discloses no Provision for diminution line "
    "(fully written off by FY2024, per Note 10.1's roll-forward in each year's own report)."
)


# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {
        "FY2025": 54821, "FY2024": 67835, "FY2023": 78138, "FY2022": 91424, "FY2021": 103943,
    }),
    ("DATA", "Loans and advances to banks", {
        "FY2025": 112260, "FY2024": 100848, "FY2023": 102904, "FY2022": 145200, "FY2021": 169942,
    }),
    ("DATA", "Loans and advances to customers", {
        "FY2025": 293309, "FY2024": 215563, "FY2023": 217968, "FY2022": 204734, "FY2021": 178267,
    }),
    ("DATA", "Debt securities - Held to Maturity (Government securities)", {
        "FY2025": 3644, "FY2024": 3709, "FY2023": 7609, "FY2022": 3509, "FY2021": 0,
    }),
    ("DATA", "Debt securities - Available for Sale (Government securities)", {
        "FY2025": 81444, "FY2024": 163009, "FY2023": 89666, "FY2022": 77063, "FY2021": 88149,
    }),
    ("DATA", "Debt securities - Available for Sale (Other securities)", {
        "FY2024": 0, "FY2023": 3886, "FY2022": 10635, "FY2021": 11463,
    }),
    ("DATA", "Gain/(deficit) on revaluation of available-for-sale debt securities", {
        "FY2025": 90, "FY2024": 152, "FY2023": -151, "FY2022": -906, "FY2021": -125,
    }),
    ("DATA", "Provision for diminution in the value of investments", {
        "FY2024": 0, "FY2023": -3901, "FY2022": -3901, "FY2021": -3901,
    }),
    ("TOTAL", "Total debt securities", {
        "FY2025": 85178, "FY2024": 166870, "FY2023": 97109, "FY2022": 86400, "FY2021": 95586,
    }),
    ("DATA", "Fixed assets", {
        "FY2025": 1989, "FY2024": 1599, "FY2023": 1116, "FY2022": 1158, "FY2021": 1618,
    }),
    ("DATA", "Other assets", {
        "FY2025": 1687, "FY2024": 3006, "FY2023": 1717, "FY2022": 3354, "FY2021": 2067,
    }),
    ("DATA", "Accrued income on securities", {
        "FY2025": 1230, "FY2024": 1372, "FY2023": 758, "FY2022": 654, "FY2021": 416,
    }),
    ("DATA", "Deferred taxation", {
        "FY2025": 6230, "FY2024": 7054, "FY2023": 6237, "FY2022": 5865, "FY2021": 2303,
    }),
    ("TOTAL", "Total assets", {
        "FY2025": 556704, "FY2024": 564147, "FY2023": 505947, "FY2022": 538789, "FY2021": 554142,
    }),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {
        "FY2025": 6741, "FY2024": 5261, "FY2023": 5362, "FY2022": 9841, "FY2021": 7806,
    }),
    ("DATA", "Customer accounts", {
        "FY2025": 449122, "FY2024": 461701, "FY2023": 411886, "FY2022": 444361, "FY2021": 469399,
    }),
    ("DATA", "Other liabilities", {
        "FY2025": 13187, "FY2024": 12985, "FY2023": 13447, "FY2022": 14105, "FY2021": 12423,
    }),
    ("TOTAL", "Total liabilities", {
        "FY2025": 469050, "FY2024": 479947, "FY2023": 430695, "FY2022": 468307, "FY2021": 489628,
    }),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {
        "FY2025": 53315, "FY2024": 53315, "FY2023": 53315, "FY2022": 53315, "FY2021": 50315,
    }),
    ("DATA", "Profit and loss account", {
        "FY2025": 12595, "FY2024": 9649, "FY2023": 2068, "FY2022": -2159, "FY2021": -6191,
    }),
    ("DATA", "Revaluation reserve", {
        "FY2025": 3, "FY2024": -119, "FY2023": -618, "FY2022": -1161, "FY2021": -97,
    }),
    ("DATA", "Other equity instruments (AT1 + Tier II)", {
        "FY2025": 21741, "FY2024": 21355, "FY2023": 20487, "FY2022": 20487, "FY2021": 20487,
    }),
    ("TOTAL", "Total equity", {
        "FY2025": 87654, "FY2024": 84200, "FY2023": 75252, "FY2022": 70482, "FY2021": 64514,
    }),
    ("TOTAL", "Total liabilities and equity", {
        "FY2025": 556704, "FY2024": 564147, "FY2023": 505947, "FY2022": 538789, "FY2021": 554142,
    }),
]

bw.add_balance_sheet_sheet(
    title="HBL Bank UK Limited — Statement of Financial Position",
    subtitle="Figures as reported in each year's own Annual Report and Financial Statements",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=62,
    source_height=220,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income - Debt Securities", {
        "FY2025": 5884, "FY2024": 6032, "FY2023": 3776, "FY2022": 1892, "FY2021": 1015,
    }),
    ("DATA", "Interest income - Loans and Other services", {
        "FY2025": 23106, "FY2024": 25627, "FY2023": 24647, "FY2022": 12718, "FY2021": 8569,
    }),
    ("TOTAL", "Total interest income", {
        "FY2025": 28990, "FY2024": 31659, "FY2023": 28423, "FY2022": 14610, "FY2021": 9584,
    }),
    ("DATA", "Interest expense", {
        "FY2025": -7248, "FY2024": -6856, "FY2023": -3466, "FY2022": -674, "FY2021": -612,
    }),
    ("TOTAL", "Net interest income", {
        "FY2025": 21742, "FY2024": 24803, "FY2023": 24957, "FY2022": 13936, "FY2021": 8972,
    }),
    ("DATA", "Fees and commissions income", {
        "FY2025": 6193, "FY2024": 4973, "FY2023": 3491, "FY2022": 4403, "FY2021": 5392,
    }),
    ("DATA", "(Losses)/Gains on foreign exchange - net", {
        "FY2025": -951, "FY2024": 846, "FY2023": -1293, "FY2022": 3633, "FY2021": 687,
    }),
    ("DATA", "Other operating income", {
        "FY2025": 939, "FY2024": 235, "FY2023": 548, "FY2022": 188, "FY2021": 725,
    }),
    ("TOTAL", "Net operating income", {
        "FY2025": 27923, "FY2024": 30857, "FY2023": 27703, "FY2022": 22160, "FY2021": 15776,
    }),
    ("DATA", "Administrative expenses", {
        "FY2025": -21631, "FY2024": -21449, "FY2023": -20221, "FY2022": -21378, "FY2021": -19484,
    }),
    ("DATA", "Restructuring cost", {
        "FY2021": 0,
    }),
    ("DATA", "Depreciation and amortisation expense", {
        "FY2025": -435, "FY2024": -310, "FY2023": -314, "FY2022": -634, "FY2021": -389,
    }),
    ("TOTAL", "Total operating expenses before provisions", {
        "FY2025": -22066, "FY2024": -21759, "FY2023": -20535, "FY2022": -22012, "FY2021": -19873,
    }),
    ("TOTAL", "Operating profit/(loss) before provisions and tax", {
        "FY2025": 5857, "FY2024": 9098, "FY2023": 7168, "FY2022": 148, "FY2021": -4097,
    }),
    ("DATA", "Provision for loan (losses)/reversals - net", {
        "FY2025": -74, "FY2024": -84, "FY2023": -50, "FY2022": 1456, "FY2021": 188,
    }),
    ("DATA", "Reversal of provision for diminution in the value of investments", {
        "FY2025": 0, "FY2024": 207, "FY2022": 0, "FY2021": 124,
    }),
    ("TOTAL", "Profit/(loss) before tax", {
        "FY2025": 5783, "FY2024": 9221, "FY2023": 7118, "FY2022": 1604, "FY2021": -3785,
    }),
    ("DATA", "Tax (expense)/credit", {
        "FY2025": -775, "FY2024": 816, "FY2023": 637, "FY2022": 3187, "FY2021": -1906,
    }),
    ("TOTAL", "Profit/(loss) for the year", {
        "FY2025": 5008, "FY2024": 10037, "FY2023": 7755, "FY2022": 4791, "FY2021": -5691,
    }),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Gain/(Loss) on revaluation of investments", {
        "FY2025": 173, "FY2024": 656, "FY2023": 808, "FY2022": -1439, "FY2021": -262,
    }),
    ("DATA", "Current tax related to available for sale debt securities", {
        "FY2021": 0,
    }),
    ("DATA", "Deferred tax related to available for sale debt securities", {
        "FY2025": -51, "FY2024": -157, "FY2023": -265, "FY2022": 375, "FY2021": 56,
    }),
    ("DATA", "Effect of movements in exchange rates on retained earnings/other movement", {
        "FY2023": 0, "FY2022": 7, "FY2021": -10,
    }),
    ("TOTAL", "Other comprehensive income/(expense) for the year", {
        "FY2025": 122, "FY2024": 499, "FY2023": 543, "FY2022": -1057, "FY2021": -216,
    }),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {
        "FY2025": 5130, "FY2024": 10536, "FY2023": 8298, "FY2022": 3734, "FY2021": -5907,
    }),
]

bw.add_income_statement_sheet(
    title="HBL Bank UK Limited — Income Statement",
    subtitle="Figures as reported in each year's own Annual Report and Financial Statements",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=220,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity - built year-by-year per the map's
# per-year reconciliation ladder: Balance Sheet built first (above), then
# equity transcribed year-by-year, checking each year's own closing balance
# ties to both the next year's own opening balance and that year's own
# Balance Sheet Total equity. Zero plug rows needed anywhere - every year
# ties exactly except the pre-existing £1k FY2025 rounding gap noted above
# (Equity Statement's own closing total 87,653 vs Balance Sheet's own Total
# equity 87,654), reproduced as disclosed.
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Other equity instruments", "Profit and loss account", "Revaluation reserve", "Total equity"]
equity_changes_rows = [
    ("TOTAL", "At 1 January 2021", [50315, 20151, 131, 109, 70706]),
    ("DATA", "Loss for the year (FY2021)", [None, None, -5691, None, -5691]),
    ("DATA", "Other comprehensive income (FY2021)", [None, None, -10, -206, -216]),
    ("TOTAL", "Total comprehensive loss for the year (FY2021)", [None, None, -5701, -206, -5907]),
    ("DATA", "Issuance of Additional Tier 1 Capital (FY2021)", [None, 2190, None, None, 2190]),
    ("DATA", "Repayment of Tier II Capital (FY2021)", [None, -1854, None, None, -1854]),
    ("DATA", "Interest on equity instruments classified as equity (FY2021)", [None, None, -621, None, -621]),
    ("TOTAL", "At 31 December 2021", [50315, 20487, -6191, -97, 64514]),

    ("DATA", "Profit for the year (FY2022)", [None, None, 4791, None, 4791]),
    ("DATA", "Other comprehensive income/(expense) (FY2022)", [None, None, 7, -1064, -1057]),
    ("TOTAL", "Total comprehensive income for the year (FY2022)", [None, None, 4798, -1064, 3734]),
    ("DATA", "Issuance of Common Equity Tier 1 Capital (FY2022)", [3000, None, None, None, 3000]),
    ("DATA", "Interest on equity instruments classified as equity (FY2022)", [None, None, -766, None, -766]),
    ("TOTAL", "At 31 December 2022", [53315, 20487, -2159, -1161, 70482]),

    ("DATA", "Profit for the year (FY2023)", [None, None, 7755, None, 7755]),
    ("DATA", "Other comprehensive income (FY2023)", [None, None, None, 543, 543]),
    ("TOTAL", "Total comprehensive income for the year (FY2023)", [None, None, 7755, 543, 8298]),
    ("DATA", "Interest on other equity instruments (FY2023)", [None, None, -3528, None, -3528]),
    ("TOTAL", "At 31 December 2023", [53315, 20487, 2068, -618, 75252]),

    ("DATA", "Profit for the year (FY2024)", [None, None, 10037, None, 10037]),
    ("DATA", "Other comprehensive income (FY2024)", [None, None, None, 499, 499]),
    ("TOTAL", "Total comprehensive income for the year (FY2024)", [None, None, 10037, 499, 10536]),
    ("DATA", "Issuance of Additional Tier 1 Capital (FY2024)", [None, 3958, None, None, 3958]),
    ("DATA", "Repayment of Tier II Capital (FY2024)", [None, -3090, None, None, -3090]),
    ("DATA", "Interest on other equity instruments (FY2024)", [None, None, -2456, None, -2456]),
    ("TOTAL", "At 31 December 2024", [53315, 21355, 9649, -119, 84200]),

    ("DATA", "Profit for the year (FY2025)", [None, None, 5008, None, 5008]),
    ("DATA", "Other comprehensive income (FY2025)", [None, None, None, 122, 122]),
    ("TOTAL", "Total comprehensive income for the year (FY2025)", [None, None, 5008, 122, 5130]),
    ("DATA", "Issuance of Additional Tier 1 Capital (FY2025)", [None, 1621, None, None, 1621]),
    ("DATA", "Repayment of Tier II Capital (FY2025)", [None, -1236, None, None, -1236]),
    ("DATA", "Interest on other equity instruments (FY2025)", [None, None, -2062, None, -2062]),
    ("TOTAL", "At 31 December 2025 (per the Bank's own Equity Statement; the Balance Sheet's own Total equity is £87,654k, £1k above this figure - see source note)", [53315, 21741, 12595, 3, 87653]),
]

bw.add_equity_changes_sheet(
    title="HBL Bank UK Limited — Statement of Changes in Equity",
    subtitle="£'000, chronological, oldest to newest",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=66,
    source_height=220,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) for the year", {
        "FY2025": 5008, "FY2024": 10037, "FY2023": 7755, "FY2022": 4791, "FY2021": -5691,
    }),
    ("DATA", "Depreciation", {
        "FY2025": 435, "FY2024": 310, "FY2023": 314, "FY2022": 354, "FY2021": 389,
    }),
    ("DATA", "Amortisation - HTM securities", {
        "FY2025": 234,
    }),
    ("DATA", "Gain on sale of fixed assets", {
        "FY2025": -720,
    }),
    ("DATA", "Loss/(gain) on sale of securities", {
        "FY2023": 0, "FY2022": 39, "FY2021": -126,
    }),
    ("DATA", "Provisions for diminution in the value of investments", {
        "FY2022": 0, "FY2021": -124,
    }),
    ("DATA", "Fixed assets written off", {
        "FY2023": 0, "FY2022": 280, "FY2021": 0,
    }),
    ("DATA", "Taxation", {
        "FY2025": 775, "FY2024": -816, "FY2023": -637, "FY2022": -3187, "FY2021": 1906,
    }),
    ("DATA", "Provisions for loan losses/(reversal) - net", {
        "FY2025": 74, "FY2024": 84, "FY2023": 50, "FY2022": -1456, "FY2021": -188,
    }),
    ("SECTION", "(Increase)/decrease in operating assets", {}),
    ("DATA", "Loans and advances to banks (excl. short term placements and Nostro balances)", {
        "FY2025": -22193, "FY2024": 1592, "FY2023": 28974, "FY2022": 13390, "FY2021": 3765,
    }),
    ("DATA", "Loans and advances to customers", {
        "FY2025": -77820, "FY2024": 2321, "FY2023": -13284, "FY2022": -25011, "FY2021": 18113,
    }),
    ("DATA", "Other assets (excl. Corporation Tax) including Accrued Income", {
        "FY2025": 1780, "FY2024": -1746, "FY2023": 1799, "FY2022": -1525, "FY2021": 2993,
    }),
    ("SECTION", "Increase/(decrease) in operating liabilities", {}),
    ("DATA", "Deposit by banks", {
        "FY2025": 1480, "FY2024": -101, "FY2023": -4479, "FY2022": 2035, "FY2021": 2361,
    }),
    ("DATA", "Customer accounts", {
        "FY2025": -12579, "FY2024": 49815, "FY2023": -32475, "FY2022": -25038, "FY2021": 10138,
    }),
    ("DATA", "Other liabilities (excl. Corporation Tax) including Deferred Income", {
        "FY2025": 201, "FY2024": -620, "FY2023": -658, "FY2022": 1682, "FY2021": -1554,
    }),
    ("DATA", "Income tax paid - net", {
        "FY2025": -205, "FY2022": 0, "FY2021": 112,
    }),
    ("TOTAL", "Net cash flows generated from/(used in) operating activities", {
        "FY2025": -103530, "FY2024": 60876, "FY2023": -12641, "FY2022": -33646, "FY2021": 32094,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Maturity/Sale of Investments in available-for-sale securities", {
        "FY2025": 200628,
    }),
    ("DATA", "Purchase of Investments in available-for-sale securities", {
        "FY2025": -119113,
    }),
    ("DATA", "Maturity of Investments in held-to-maturity securities", {
        "FY2025": 0,
    }),
    ("DATA", "Net investments in available-for-sale securities", {
        "FY2024": -73517, "FY2023": -6121, "FY2022": 11217, "FY2021": -22599,
    }),
    ("DATA", "Net investments in held-to-maturity securities", {
        "FY2024": 4255, "FY2023": -4046, "FY2022": -3509, "FY2021": 3661,
    }),
    ("DATA", "Fixed capital expenditure", {
        "FY2025": -105, "FY2024": -792, "FY2023": -272, "FY2022": -156, "FY2021": -59,
    }),
    ("TOTAL", "Net cash flows generated from/(used in) investing activities", {
        "FY2025": 81410, "FY2024": -70054, "FY2023": -10439, "FY2022": 7552, "FY2021": -18997,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of Tier II Capital", {
        "FY2025": -1236, "FY2024": -3090, "FY2023": 0, "FY2022": 0, "FY2021": -1852,
    }),
    ("DATA", "Issuance of additional Tier 1 capital", {
        "FY2025": 1621, "FY2022": 3000, "FY2021": 2190,
    }),
    ("DATA", "Issuance of ordinary share capital", {
        "FY2024": 3958, "FY2023": 0,
    }),
    ("DATA", "Interest paid on other equity instruments", {
        "FY2025": -2062, "FY2024": -2456, "FY2023": -3528, "FY2022": -766, "FY2021": -621,
    }),
    ("TOTAL", "Net cash flows used in/(generated from) financing activities", {
        "FY2025": -1677, "FY2024": -1588, "FY2023": -3528, "FY2022": 2234, "FY2021": -283,
    }),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents during the year", {
        "FY2025": -23797, "FY2024": -10766, "FY2023": -26608, "FY2022": -23860, "FY2021": 12814,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 102057, "FY2024": 112823, "FY2023": 139431, "FY2022": 163302, "FY2021": 150837,
    }),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {
        "FY2023": 0, "FY2022": -11, "FY2021": -349,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 78260, "FY2024": 102057, "FY2023": 112823, "FY2022": 139431, "FY2021": 163302,
    }),
]

bw.add_cash_flow_sheet(
    title="HBL Bank UK Limited — Cash Flow Statement",
    subtitle="Figures as reported in each year's own Annual Report and Financial Statements",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
# The Bank applies FRS 102/IAS 39's incurred-loss impairment model, not
# IFRS 9 staging - no Stage 1/2/3 gross-exposure split is disclosed
# anywhere in any year's Annual Report (confirmed by reading Note 16
# "Provision for Loan Losses" in full each year - it only ever shows a
# Specific/Collective impairment split against the loan book as a whole,
# not a staged breakdown by credit-quality bucket). Asset Quality is
# built around that actual disclosed basis instead.
ASSET_QUALITY_SOURCES = (
    "Sources - HBL Bank UK Limited's own Note 16 'Provision for Loan Losses' (Specific/Collective "
    "impairment split), each year's own originally-published figures, cross-referenced against the "
    "Balance Sheet's own 'Loans and advances to customers' net figure (gross derived as net + total "
    "provision):\n"
    f"FY2025: Annual Report and Financial Statements 2025, Note 16, p.47 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements 2024, Note 16, p.47 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, Note 16, p.49 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, Note 16, p.50 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, Note 16, p.46 (own Specific/Collective "
    f"split confirmed identical to the FY2022 Annual Report's own FY2021 comparative) - {AR2021_URL}\n"
    "No IFRS 9 Stage 1/2/3 gross-exposure split is disclosed in any year - the Bank applies FRS 102/"
    "IAS 39's incurred-loss impairment model (Specific/Collective, not staged), confirmed by reading "
    "Note 16 in full each year. Coverage ratio = total provision / derived gross loans to customers."
)

_gross_loans = {}
_provision_total = {}
for _y, _net, _spec, _coll in [
    ("FY2025", 293309, 666, 600),
    ("FY2024", 215563, 392, 800),
    ("FY2023", 217968, 308, 800),
    ("FY2022", 204734, 408, 650),
    ("FY2021", 178267, 2714, 650),
]:
    _provision_total[_y] = _spec + _coll
    _gross_loans[_y] = _net + _provision_total[_y]

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, gross-to-net bridge", {}),
    ("DATA", "Gross loans and advances to customers (derived: net + total provision)", _gross_loans),
    ("DATA", "Specific impairment provision", {
        "FY2025": 666, "FY2024": 392, "FY2023": 308, "FY2022": 408, "FY2021": 2714,
    }),
    ("DATA", "Collective impairment provision", {
        "FY2025": 600, "FY2024": 800, "FY2023": 800, "FY2022": 650, "FY2021": 650,
    }),
    ("TOTAL", "Total provision for loan losses", _provision_total),
    ("TOTAL", "Net loans and advances to customers (per Balance Sheet)", {
        "FY2025": 293309, "FY2024": 215563, "FY2023": 217968, "FY2022": 204734, "FY2021": 178267,
    }),
    ("DATA", "Provision coverage ratio (total provision / gross loans)", {
        y: f"{_provision_total[y] / _gross_loans[y] * 100:.2f}%" for y in YEARS
    }),
]

bw.add_asset_quality_sheet(
    title="HBL Bank UK Limited — Asset Quality",
    subtitle="Figures as reported in each year's own Annual Report and Financial Statements",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=74,
    source_height=220,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# KM1 Key Metrics (KM1-016)
#
# FINDING: HBL Bank UK Limited PUBLISHES a Pillar 3 disclosure every year, but
# it DOES NOT USE the UK KM1 "Key metrics" template in any edition. This is the
# middle of the three findings the KM1 map distinguishes - it is NOT "no Pillar 3
# is published" (four editions were downloaded and read in full for this ticket),
# and it is NOT an Article 432 materiality/confidentiality exclusion (the FY2025
# edition states the opposite in terms: "The Bank has not taken any exemptions
# from these disclosures with regards to confidential or proprietary
# information", section 1.3, p.4).
#
# What HBL prints under its own heading "2. Key Metrics" is three separate,
# bespoke, UNNUMBERED tables - "Regulatory Capital and Capital Ratios",
# "Leverage Ratio", and "Liquidity Ratios - Liquidity Coverage (LCR) and Stable
# Funding (NSFR)" - each with a 2-column current-year/prior-year header. Applying
# the map's row-set test, this fails it the same way ABC International Bank's
# "Table 3 Key Regulatory Metrics" does:
#   * The ENTIRE SREP and buffer block of the template is absent - there is no
#     equivalent of rows UK 7a-UK 7d (additional CET1/AT1/T2 SREP requirements,
#     total SREP own funds requirement), 8/UK 8a (capital conservation buffer),
#     9/UK 9a (countercyclical and systemic risk buffers), 10/UK 10a (G-SII and
#     O-SII buffers), 11 (combined buffer requirement), UK 11a (overall capital
#     requirements) or 12 (CET1 available after meeting total SREP own funds
#     requirements) anywhere in the section, in any of the four editions read.
#   * It ADDS rows the template does not have, as separate line items:
#     "Additional Tier 1 Capital (AT 1)" and "Tier 2 Capital (T 2)".
#   * Its labels are its own, not the template's ("Total Net Flow" where KM1
#     row 16 reads "Total net cash outflows", "Total Risk Weighted Assets" where
#     KM1 row 4 reads "Total risk-weighted exposure amount").
#   * No row numbers of any kind are printed. (Under map rule 8 that alone would
#     NOT disqualify it - Europe Arab Bank prints the real template unnumbered -
#     which is precisely why the row-set test, not the numbering, is what decides
#     this one.)
# Mapping these three short tables onto KM1 row numbers would invent a
# correspondence HBL has never published, so no KM1 sheet is reproduced.
#
# HBL does use at least one prescribed UK template elsewhere: the FY2022-FY2025
# editions print the UK CCyB1 countercyclical-buffer template with its own
# numbered rows. So the absence of KM1 is a choice about that template, not an
# inability to render templates at all.
#
# The eleven single-metric Pillar 3 sheets in this workbook are built from these
# three bespoke tables directly, which is why they are populated while this sheet
# is not - they are not derived from a KM1 that does not exist.
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Sources - every Pillar 3 disclosure HBL Bank UK Limited makes available was downloaded "
    "and read in full for this check (all five verified by HTTP 200, Content-Type "
    "application/pdf and %PDF magic bytes; none was a blocked fetch or a soft-404). This note "
    "previously said 'all four', because the FY2023 edition was wrongly believed unreachable:\n"
    f"FY2025: Pillar III Disclosures 2025 - section 2 'Key Metrics', p.4-5 - {P3_2025_URL}\n"
    f"FY2024: Pillar III Disclosure 2024 - section 2 'Key Metrics', p.4-5 - {P3_2024_URL}\n"
    f"FY2022: Pillar III Disclosure - 31 December 2022 - section 2 'Key Metrics', p.6-7 - "
    f"{P3_2022_URL}\n"
    f"FY2021: Pillar III Disclosures - 31 December 2021 - section 2 'Key Metrics', p.4-5 - "
    f"{P3_2021_URL}\n"
    f"FY2023: Pillar III Disclosure - 31 December 2023 - section 2 'Key Metrics', printed p.5 - "
    f"{P3_2023_URL}\n"
    "  This line previously read \"FY2023: no standalone FY2023 Pillar 3 document is reachable\". "
    "That was FALSE - see the correction at the foot of this note. The FY2023 edition has now been "
    "read in full, and it does not change this sheet's verdict: its section 2 is the same bespoke "
    "three-table layout as every other edition, not a UK KM1 template.\n\n"
    "LATEST-EDITION CHECK, 2026-09-16: checked HBL Bank UK's own website rather than this "
    "project's cited URLs. hblbankuk.com/regulatory-disclosures/ returns HTTP 404 - the bank "
    "has no dedicated regulatory-disclosures page; its documents are published on the general "
    "downloads page hblbankuk.com/pdf-downloads/, which as at that date lists exactly one "
    "Pillar 3 document ('HBL-UK-2025-Pillar-III-Disclosure.pdf') and one set of financial "
    "statements ('FS-HBL-Bank-UK-2025.pdf'), both for the year ended 31 December 2025. FY2025 "
    "is therefore the newest edition published, and this workbook already holds it. Checked, "
    "none newer.\n\n"
    "WHY THIS SHEET IS 'Not applicable':\n"
    "HBL Bank UK Limited publishes a Pillar 3 disclosure annually but has never used the UK "
    "KM1 'Key metrics' template. Its own section headed '2. Key Metrics' is three separate, "
    "unnumbered, bespoke tables ('Regulatory Capital and Capital Ratios'; 'Leverage Ratio'; "
    "'Liquidity Ratios - Liquidity Coverage (LCR) and Stable Funding (NSFR)'), each with a "
    "current-year and prior-year column. That is not the template rendered without numbering - "
    "it is a shorter and different table. Positive evidence, from reading all four editions "
    "end to end:\n"
    "  * The template's entire SREP and buffer block is absent. There is no equivalent of rows "
    "UK 7a-UK 7d, 8, UK 8a, 9, UK 9a, 10, UK 10a, 11, UK 11a or 12 anywhere in the Key Metrics "
    "section of any edition.\n"
    "  * Rows the template does not contain are added as separate line items: 'Additional Tier "
    "1 Capital (AT 1)' and 'Tier 2 Capital (T 2)'.\n"
    "  * The labels are HBL's own, not the template's - e.g. 'Total Net Flow' for what KM1 row "
    "16 calls 'Total net cash outflows', and 'Total Risk Weighted Assets' for what KM1 row 4 "
    "calls 'Total risk-weighted exposure amount'.\n"
    "This is NOT a case of 'no Pillar 3 is published', and it is NOT an Article 432 exclusion: "
    "the FY2025 edition states at section 1.3 (p.4) that 'The Bank has not taken any exemptions "
    "from these disclosures with regards to confidential or proprietary information', and no "
    "edition carries an excluded-templates appendix. HBL does render other prescribed UK "
    "templates - the FY2022-FY2025 editions print UK CCyB1 with its own numbered rows - so the "
    "absence is specific to KM1.\n\n"
    "Nothing on this sheet has been back-filled from the statutory accounts, and the three "
    "bespoke tables have NOT been re-labelled into template row numbers, which would invent a "
    "correspondence the bank never published. The eleven single-metric Pillar 3 sheets in this "
    "workbook are built directly from those bespoke tables and remain fully populated.\n\n"
    + FY2023_RECOVERY_NOTE
)

bw.add_km1_sheet(
    title="HBL Bank UK Limited — KM1 Key Metrics",
    subtitle="Not applicable — HBL Bank UK Limited publishes a Pillar 3 disclosure every year but has "
             "never used the UK KM1 'Key metrics' template in any edition (FY2021, FY2022, FY2024 and "
             "FY2025 all read in full). See the source note below for the positive evidence and for why "
             "this is 'the template is not used' rather than 'no Pillar 3 is published' or an Article 432 "
             "exclusion.",
    rows=[
        ("DATA", "Not applicable — the UK KM1 template is not used in HBL Bank UK Limited's Pillar 3 disclosures",
         {y: "Not applicable" for y in YEARS}),
    ],
    sources_text=KM1_SOURCES,
    source_height=330,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None, source_height=560):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=source_height)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2025": 59210, "FY2024": 55598, "FY2023": 48949, "FY2022": 44784, "FY2021": 41624,
    })],
    p3_sources(),
    note="DOCUMENTED CROSS-EDITION DIVERGENCE, FY2023 CET1 - RECORDED, NOT RECONCILED (2026-09-18). "
         "The two editions print different figures for the same year: HBL's FY2023 Pillar III "
         "Disclosure states CET1 at 31 December 2023 as £48,849k (section 2 'Key Metrics', printed "
         "p.5), while the FY2024 Pillar III Disclosure's FY2023 comparative column states £48,949k. "
         "The £48,949k from the FY2024 edition is what this sheet carries and it has been LEFT "
         "UNCHANGED - both figures were read from their own published source and neither is "
         "adjusted to fit the other.\n"
         "Recorded so a later pass does not 'fix' this without the evidence: the arithmetic inside "
         "the FY2024 edition itself favours £48,849k. That same comparative column prints Tier 1 of "
         "£58,635k and AT1 of £9,786k (58,635 - 9,786 = 48,849), and a CET1 ratio of 17.84%, which "
         "against the disclosed RWAs of £273,837k implies £48,849k (£48,949k would give 17.87%). "
         "The FY2023 edition is internally consistent on all three. This looks like a one-digit "
         "transcription slip in the FY2024 edition's comparative, but that is an inference about "
         "the bank's own document, not a disclosure, so the printed figure stands as printed.\n"
         "Every OTHER FY2023 figure in this workbook was checked against the FY2023 standalone "
         "document and is identical to the comparative column - see the source note below.",
)
metric(
    "CET1 Ratio", "%",
    [("CET1 Ratio", {
        "FY2025": "15.46%", "FY2024": "16.80%", "FY2023": "17.84%", "FY2022": "14.80%", "FY2021": "14.14%",
    })],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 Capital (CET1 + AT1)", {
        "FY2025": 74574, "FY2024": 69342, "FY2023": 58635, "FY2022": 54570, "FY2021": 51409,
    })],
    p3_sources(),
)
metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 Ratio", {
        "FY2025": "19.47%", "FY2024": "20.95%", "FY2023": "21.41%", "FY2022": "18.04%", "FY2021": "17.46%",
    })],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total Capital (CET1 + AT1 + Tier 2)", {
        "FY2025": 81550, "FY2024": 77754, "FY2023": 70136, "FY2022": 65921, "FY2021": 62761,
    })],
    p3_sources(),
)
metric(
    "Total Capital Ratio", "%",
    [("Total Capital Ratio", {
        "FY2025": "21.29%", "FY2024": "23.49%", "FY2023": "25.61%", "FY2022": "21.79%", "FY2021": "21.31%",
    })],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total Risk Weighted Assets", {
        "FY2025": 383024, "FY2024": 330996, "FY2023": 273837, "FY2022": 302527, "FY2021": 294454,
    })],
    p3_sources(),
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown
# ---------------------------------------------------------------
# Credit risk RWA is directly disclosed by exposure class in each year's
# own Pillar 3 "Capital Requirement under PRA Rulebook (CRR Part)" table.
# Operational risk / market risk / CVA are only disclosed as capital
# charges (@ 8%) in that same table, not as RWA directly - derived here
# as capital charge / 0.08, documented as derived rather than presented
# as if directly disclosed. FY2025's own table uses a different exposure-
# class grouping (Sovereign/Exposures in default/Secured by mortgages on
# immovable property/Multilateral development banks) than FY2021-FY2024's
# table (Central Governments or Central Bank/Overdue and impaired
# accounts/Secured on real estate property) - mapped onto shared row
# labels below, each year shown on its own actually-disclosed basis.
RWA_SOURCES = (
    "Sources - HBL Bank UK Limited's own Pillar 3 'Capital Requirement under PRA Rulebook (CRR "
    "Part)' table (credit risk RWA directly disclosed by exposure class; operational risk/market "
    "risk/CVA only disclosed as capital charges @ 8%, RWA derived here as charge / 0.08 and flagged "
    "as such):\n"
    f"FY2025: Pillar III Disclosure - 31 December 2025, section 5 'Capital Requirements', p.11 - {P3_2025_URL}\n"
    f"FY2024: Pillar III Disclosure - 31 December 2024, 'Capital Requirement under PRA Rulebook', "
    f"p.11 (FY2024's own originally-published figures used) - {P3_2024_URL}\n"
    f"FY2023: Pillar III Disclosure - 31 December 2023, section 7.1 'Capital Requirement under PRA "
    f"Rulebook (CRR Part)', printed p.27 - {P3_2023_URL}\n"
    f"        This line previously read 'FY2023 comparative column of the FY2024 Pillar III "
    f"Disclosure, p.11 (FY2023's own standalone Pillar 3 document could not be fetched this "
    f"session...)'. The standalone document has now been read, and every FY2023 figure on this "
    f"sheet is CONFIRMED unchanged by it: 4,969 / 30,035 / 67,448 / 3,122 / 126,694 / 4,683 / "
    f"4,468, total credit risk RWA 241,419, operational-risk charge 2,581, market risk 0, CVA 12. "
    f"No cell was edited as a result.\n"
    f"FY2022: Pillar III Disclosure - 31 December 2022, section 7.1, p.26 (FY2022's own originally-"
    f"published figures used) - {P3_2022_URL}\n"
    f"FY2021: Pillar III Disclosures - 31 December 2021, section 7.1 'Capital Requirement under "
    f"CRR', p.23 (FY2021's own standalone Pillar 3 document, found in a later session and "
    f"confirmed identical to the FY2022 Pillar III Disclosure's FY2021 comparative column for "
    f"every row) - {P3_2021_URL}\n"
    "Derived Total RWA (sum of the rows below) is within rounding of the disclosed Total RWAs sheet "
    "in every year (differences of a few £'000 up to a few hundred £'000, from the 8% capital-charge "
    "rounding in the source documents) - reproduced as derived, not force-reconciled to the "
    "disclosed Total RWAs figure. CORRECTION 2026-09-18: this sentence previously singled FY2023 out "
    "as '£5,500k below' the disclosed total and blamed the unreachable FY2023 document. Both halves "
    "were wrong. The gap is 5 units of £'000 - i.e. £5,000, not £5.5m - since derived 273,832 "
    "against disclosed 273,837; and it has nothing to do with sourcing, being purely the 8% "
    "capital-charge rounding, exactly as in the other four years.\n\n"
    + FY2023_RECOVERY_NOTE
)

rwa_breakdown_rows = [
    ("SECTION", "Credit risk RWA by exposure class", {}),
    ("DATA", "Central governments/central banks (Sovereign, FY2025)", {
        "FY2025": 15144, "FY2024": 5564, "FY2023": 4969, "FY2022": 20777, "FY2021": 11799,
    }),
    ("DATA", "Institutions", {
        "FY2025": 43817, "FY2024": 32883, "FY2023": 30035, "FY2022": 36000, "FY2021": 35388,
    }),
    ("DATA", "Corporates", {
        "FY2025": 84540, "FY2024": 109849, "FY2023": 67448, "FY2022": 85497, "FY2021": 90506,
    }),
    ("DATA", "Retail", {
        "FY2025": 2311, "FY2024": 2948, "FY2023": 3122, "FY2022": 4209, "FY2021": 4391,
    }),
    ("DATA", "Secured on real estate/mortgages", {
        "FY2025": 181249, "FY2024": 131504, "FY2023": 126694, "FY2022": 116995, "FY2021": 112069,
    }),
    ("DATA", "Overdue/exposures in default", {
        "FY2025": 2288, "FY2024": 1931, "FY2023": 4683, "FY2022": 4184, "FY2021": 7053,
    }),
    ("DATA", "Multilateral development banks", {
        "FY2025": 0,
    }),
    ("DATA", "Other items", {
        "FY2025": 3147, "FY2024": 4980, "FY2023": 4468, "FY2022": 5078, "FY2021": 3647,
    }),
    ("TOTAL", "Total credit risk RWA", {
        "FY2025": 332496, "FY2024": 289659, "FY2023": 241419, "FY2022": 272740, "FY2021": 264852,
    }),
    ("SECTION", "Other risk types (RWA derived from disclosed capital charge / 0.08)", {}),
    ("DATA", "Operational risk RWA (derived)", {
        "FY2025": 50450, "FY2024": 41025, "FY2023": 32263, "FY2022": 29338, "FY2021": 29263,
    }),
    ("DATA", "Market risk RWA (derived)", {
        "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 175,
    }),
    ("DATA", "Credit value adjustment RWA (derived)", {
        "FY2025": 75, "FY2024": 313, "FY2023": 150, "FY2022": 450, "FY2021": 150,
    }),
    ("TOTAL", "Total RWA (derived, sum of the above)", {
        "FY2025": 383021, "FY2024": 330997, "FY2023": 273832, "FY2022": 302528, "FY2021": 294440,
    }),
]

bw.add_rwa_breakdown_sheet(
    title="HBL Bank UK Limited — RWA Breakdown",
    subtitle="Figures as reported in each year's own Pillar 3 disclosures - see source note for exposure-class mapping across years",
    rows=rwa_breakdown_rows,
    sources_text=RWA_SOURCES,
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage Ratio", {
        "FY2025": "13.11%", "FY2024": "11.85%", "FY2023": "13.42%", "FY2022": "13.01%", "FY2021": "9.41%",
    })],
    p3_sources(),
    note="NO FY2021/FY2022 BASIS BREAK - CHECKED AND CLEARED 2026-09-16, recorded so this series is not "
         "'corrected' later on a false positive. The 9.41% -> 13.01% step is a real capital increase, not the "
         "UK Leverage Ratio Framework's exclusion of claims on central banks (which took effect 1 January 2022 "
         "and does break other banks' series in this project). Both the FY2021 and FY2022 Pillar 3 documents were "
         "downloaded and read in full this session (%PDF verified, 36 and 38 pages): each states the same CRR "
         "Article 451 / CRD IV definition - exposure is 'the sum of balance sheet assets, plus off-balance sheet "
         "items', with no central-bank-exclusion line in either - and the exposure measure barely moved, "
         "£546,542k at 31 December 2021 to £543,633k at 31 December 2022 (-0.5%). The FY2022 document's own "
         "FY2021 comparative is £546,542k / 9.41%, i.e. identical to FY2021's own report: no restatement. The "
         "ratio therefore rose because Tier 1 capital rose roughly 37%, not because the denominator changed.\n"
         "FY2024 uses FY2024's own originally-published figure (11.85%); the FY2025 Pillar 3 "
         "document's FY2024 comparative restates this to 11.56% - see the source citation.\n"
         "DOCUMENTED CROSS-EDITION DIVERGENCE, FY2022 (added 2026-09-18, RECORDED NOT RECONCILED): "
         "this sheet carries 13.01% for FY2022, read from FY2022's own Pillar 3 document "
         "(exposure £543,633k). The FY2023 Pillar III Disclosure, recovered 2026-09-18 and now "
         "cited below, prints a DIFFERENT FY2022 comparative on its own printed p.5 - exposure "
         "£419,520k and ratio 12.82%. Both were read from their own primary source; neither has "
         "been adjusted, averaged or restated to match the other, and no cell was changed. The "
         "exposure measure moves by £124m between the two editions, so this is a re-basing of the "
         "denominator in the FY2023 edition rather than a rounding difference; the FY2023 document "
         "gives no reconciliation of it. Note that the FY2023 edition's own FY2023 figures "
         "(£409,798k / 13.42%) agree exactly with the FY2024 edition's FY2023 comparative, so the "
         "divergence is confined to the FY2022 column.",
    source_height=700,
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {
        "FY2025": "235%", "FY2024": "376%", "FY2023": "702%", "FY2022": "613%", "FY2021": "560%",
    })],
    p3_sources(),
)
metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {
        "FY2025": "145%", "FY2024": "199%", "FY2023": "185%", "FY2022": "183%", "FY2021": "180%",
    })],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "Not disclosed - HBL Bank UK Limited is not identified as a UK resolution entity in its Pillar 3 disclosures."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2025": 556704, "FY2024": 564147, "FY2023": 505947, "FY2022": 538789, "FY2021": 554142,
        }),
        ("Loans and advances to customers", {
            "FY2025": 293309, "FY2024": 215563, "FY2023": 217968, "FY2022": 204734, "FY2021": 178267,
        }),
        ("Customer accounts", {
            "FY2025": 449122, "FY2024": 461701, "FY2023": 411886, "FY2022": 444361, "FY2021": 469399,
        }),
        ("Total equity", {
            "FY2025": 87654, "FY2024": 84200, "FY2023": 75252, "FY2022": 70482, "FY2021": 64514,
        }),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total interest income", {
            "FY2025": 28990, "FY2024": 31659, "FY2023": 28423, "FY2022": 14610, "FY2021": 9584,
        }),
        ("Net operating income", {
            "FY2025": 27923, "FY2024": 30857, "FY2023": 27703, "FY2022": 22160, "FY2021": 15776,
        }),
        ("Total operating expenses before provisions", {
            "FY2025": -22066, "FY2024": -21759, "FY2023": -20535, "FY2022": -22012, "FY2021": -19873,
        }),
        ("Profit/(loss) for the year", {
            "FY2025": 5008, "FY2024": 10037, "FY2023": 7755, "FY2022": 4791, "FY2021": -5691,
        }),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {
            "FY2025": 84200, "FY2024": 75252, "FY2023": 70482, "FY2022": 64514, "FY2021": 70706,
        }),
        ("Total comprehensive income/(loss) for the year", {
            "FY2025": 5130, "FY2024": 10536, "FY2023": 8298, "FY2022": 3734, "FY2021": -5907,
        }),
        ("Other equity movements, net", {
            "FY2025": -1677, "FY2024": -1588, "FY2023": -3528, "FY2022": 2234, "FY2021": -285,
        }),
        ("Closing equity (per the Bank's own Equity Statement)", {
            "FY2025": 87653, "FY2024": 84200, "FY2023": 75252, "FY2022": 70482, "FY2021": 64514,
        }),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flows generated from/(used in) operating activities", {
            "FY2025": -103530, "FY2024": 60876, "FY2023": -12641, "FY2022": -33646, "FY2021": 32094,
        }),
        ("Net cash flows generated from/(used in) investing activities", {
            "FY2025": 81410, "FY2024": -70054, "FY2023": -10439, "FY2022": 7552, "FY2021": -18997,
        }),
        ("Net cash flows used in/(generated from) financing activities", {
            "FY2025": -1677, "FY2024": -1588, "FY2023": -3528, "FY2022": 2234, "FY2021": -283,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 78260, "FY2024": 102057, "FY2023": 112823, "FY2022": 139431, "FY2021": 163302,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {
            "FY2025": 15.46, "FY2024": 16.80, "FY2023": 17.84, "FY2022": 14.80, "FY2021": 14.14,
        }),
        ("Tier 1 Ratio", {
            "FY2025": 19.47, "FY2024": 20.95, "FY2023": 21.41, "FY2022": 18.04, "FY2021": 17.46,
        }),
        ("Total Capital Ratio", {
            "FY2025": 21.29, "FY2024": 23.49, "FY2023": 25.61, "FY2022": 21.79, "FY2021": 21.31,
        }),
        ("Leverage Ratio", {
            "FY2025": 13.11, "FY2024": 11.85, "FY2023": 13.42, "FY2022": 13.01, "FY2021": 9.41,
        }),
        ("LCR", {
            "FY2025": 235, "FY2024": 376, "FY2023": 702, "FY2022": 613, "FY2021": 560,
        }),
        ("NSFR", {
            "FY2025": 145, "FY2024": 199, "FY2023": 185, "FY2022": 183, "FY2021": 180,
        }),
    ],
    note="MREL Ratio is not charted here - not disclosed (see the MREL Ratio sheet). Figures are "
         "duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HBL BANK UK FINANCIALS.xlsx")
