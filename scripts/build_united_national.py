import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Fiscal year-end 31 December. Only 4 years sourced (FY2022-FY2025) - see
# ENTITY_NOTE; no FY2021 was pursued given diminishing returns on a small bank.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzUxODk3MTQ2NWFkaXF6a2N4/document?format=pdf"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzQyNTcyMzI0MGFkaXF6a2N4/document?format=pdf"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzM3ODQxMzg4MWFkaXF6a2N4/document?format=pdf"
P3_2023_URL = "https://www.ubluk.com/media/lupbssja/annual-report-unb-2023-pillar3-final-approved.pdf"
P3_2022_URL = "https://web.archive.org/web/20230923163742if_/https://www.ubluk.com/media/1368/ubl-2022-pillar-3-final-published.pdf"
P3_2024_URL = "https://www.ubluk.com/media/vsvfbmui/pillar260825.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: United National Bank Limited (Companies House 04146820) was formed in 2001 from the merger of the "
    "UK branches of two Pakistani banks, United Bank Limited ('UBL') and National Bank of Pakistan ('NBP'), who had "
    "operated in the UK since the 1960s - historically 55% UBL / 45% NBP owned, trading as 'UBL UK'. In July 2024, "
    "following regulatory approval, Bestway Group Financial Services Limited (a wholly-owned subsidiary of Bestway "
    "Group, a UK diversified conglomerate) acquired 95.1% of the Company's shares from UBL and NBP - the Company is "
    "now majority UK-owned rather than a foreign subsidiary in the usual sense, though UBL/NBP retain a residual "
    "stake and a preference-share arrangement (see Notes). All financial statements are prepared under FRS 102 in "
    "Pound Sterling (the Company's functional currency) - no cash-flow-statement exemption is taken.\n\n"
    "DATA AVAILABILITY NOTE: 4 years (FY2022-FY2025) sourced from three Companies House annual report filings "
    "(FY2025/FY2024 from the 2025 filing, FY2023 from the 2023 filing, and FY2022's own originally-published figures "
    "from the FY2022 filing itself rather than the FY2023 filing's restated comparative - all fully scanned/"
    "image-only PDFs, transcribed directly from the source page images). No FY2021 was pursued. Pillar 3: the "
    "pre-Bestway entity ('UBL UK') published 'Pillar 3 and Remuneration Code Disclosures' on its own site "
    "(ubluk.com) for every year FY2016-FY2024; the live site no longer links to most of these (only the current "
    "year's edition is navigable from ubluk.com/resources), but every year's PDF is still reachable at its original "
    "URL or via the Wayback Machine once located via a CDX search - FY2022, FY2023 and FY2024 editions were all "
    "recovered this way. No FY2025 edition exists yet as of this build (2026-09) - the FY2025 Annual Report itself "
    "was signed 23 April 2026, so a Pillar 3 disclosure for that year, if produced, would likely not be published "
    "until later in 2026; this is a genuine access gap (document may not yet exist), not a confirmed non-disclosure."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are United National Bank Limited's own Statement of Cash Flows, exact £ as reported "
    "(not rounded to £'000/£m):\n"
    f"FY2025 & FY2024: Annual report and financial statements 2025, p.26 (Statement of cash flows) - {AR2025_URL}\n"
    f"FY2023 & FY2022 (as restated): Annual report and financial statements 2023, p.32 (Statement of cash flows) - "
    f"{AR2023_URL}\n"
    "FY2023's own closing balance (£9,725,415) matches the FY2025 report's own FY2024 opening balance exactly, "
    "confirming consistency across the two source documents. FY2022 is labelled '(as restated)' in the FY2023 "
    "report; its own originally-published cash flow figures were not sourced separately here (unlike the new "
    "Balance Sheet / Profit & Loss / Statement of Changes in Equity / Asset Quality sheets added in this build, "
    "which do use FY2022's own originally-published figures throughout - see those sheets' own source notes for "
    "the ~£2.26m net-loans restatement this creates between FY2022's own Balance Sheet and the FY2023 report's "
    "restated FY2022 comparative).\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - United National Bank Limited (trading as 'UBL UK' at the time) Pillar 3 basis:\n"
        f"FY2023: UBL UK Pillar 3 and Remuneration Code Disclosures at 31 December 2023, various pages (Table LRSum/"
        f"LRCom p.47-48; Appendix VI Own funds disclosure p.61-63) - {P3_2023_URL}\n"
        f"FY2022: UBL UK Pillar 3 and Remuneration Code Disclosures at 31 December 2022, p.27 (Pillar 1 capital "
        f"requirements), p.48-49 (Leverage Ratio), p.22-23 (Own Funds) - {P3_2022_URL} (recovered via Wayback "
        f"Machine; the live ubluk.com URL for this document now 301-redirects to the site's generic resources page).\n"
        f"FY2024: UBL UK Pillar 3 and Remuneration Code Disclosures at 31 December 2024, p.26 (Pillar 1 capital "
        f"requirements), p.46-47 (Leverage Ratio), p.22 (Own Funds) - {P3_2024_URL} (also recovered via Wayback "
        f"Machine CDX search - not linked from the live site's own resources page, but the direct URL still "
        f"resolves).\n"
        f"FY2025: no Pillar 3 document exists yet as of this build - see entity note on the Cash Flow Statement "
        f"sheet.\n"
        f"CET1/Tier 1/Total Capital ratios for FY2022 and FY2024 are computed here (capital ÷ Total RWAs, both "
        f"directly from the sources above) since neither document states the ratio as text, unlike FY2023's "
        f"document, which states its ratios directly.\n"
        f"Tier 1 capital and Total capital £ amounts for all 4 years cross-check exactly against each year's own "
        f"audited Annual Report 'Capital resources' note (see Cash Flow Statement sheet source note for URLs)."
    )


bw = BankWorkbook(bank_name="United National Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="4A1E4D")

STATEMENTS_SOURCES = (
    "Sources - all figures are United National Bank Limited's own statements, exact £ as reported (not rounded to "
    "£'000/£m):\n"
    f"FY2025 & FY2024: Annual report and financial statements 2025 - p.22 (Statement of profit or loss), p.24 "
    f"(Balance sheet), p.25 (Statement of changes in equity), p.42-43 (Note 9, Loans and advances to customers) - "
    f"{AR2025_URL}\n"
    f"FY2023: Annual report and financial statements 2023 - p.28 (Statement of profit or loss), p.30 (Balance "
    f"sheet), p.31 (Statement of changes in equity), p.47 (Note 9, Loans and advances to customers) - {AR2023_URL}\n"
    f"FY2022 (own originally-published figures, not the FY2023 report's restated comparative): Full accounts made "
    f"up to 31 December 2022 (filed 10 May 2023) - p.27 (Statement of profit or loss), p.29 (Balance sheet), p.30 "
    f"(Statement of changes in equity), p.45 (Note 8, Loans and advances to customers) - {AR2022_URL}\n"
    "DISCREPANCY: FY2022's own net loans figure (£638,315,902, tying to its own Balance Sheet and Note 8) differs "
    "from the FY2023 report's restated FY2022 comparative (£636,057,857) by ~£2.26m - a genuine restatement "
    "between the two filings. This workbook uses FY2022's own originally-published figures throughout, per project "
    "convention, so this Balance Sheet / Profit & Loss / Statement of Changes in Equity / Asset Quality sheet will "
    "not exactly match a later report's restated FY2022 comparative column.\n"
    "DISCREPANCY: the FY2025 Statement of Changes in Equity's own 31 December 2025 closing Total (£117,048,805) "
    "does not exactly match the FY2025 Balance Sheet's own Total equity for the same date (£117,048,800) - both "
    "figures are transcribed exactly as each statement states; this ~£5 gap is a source-document-internal rounding "
    "artefact, not a transcription error, and is not forced to tie.\n\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at banks", {"FY2025": 13278966, "FY2024": 8271317, "FY2023": 9725415, "FY2022": 6703512}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1540326075, "FY2024": 1032354956, "FY2023": 718597663, "FY2022": 638315902}),
    ("DATA", "Loans and advances to banks", {"FY2025": 23388100, "FY2024": 22616365, "FY2023": 13576284, "FY2022": 2000329}),
    ("DATA", "Derivative financial assets", {"FY2025": 245277, "FY2024": 331288, "FY2023": 632792, "FY2022": 3137104}),
    ("DATA", "Debt securities", {"FY2025": 297504303, "FY2024": 178309427, "FY2023": 138342935, "FY2022": 122536714}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 1387861, "FY2024": 1002759, "FY2023": 1140078, "FY2022": 772017}),
    ("DATA", "Other assets", {"FY2025": 6369330, "FY2024": 8673325, "FY2023": 6382510, "FY2022": 1906588}),
    ("DATA", "Investment property", {"FY2025": 2900000, "FY2024": 2960000, "FY2023": 9604343, "FY2022": 9446895}),
    ("DATA", "Tangible fixed assets", {"FY2025": 29230135, "FY2024": 28954170, "FY2023": 21774348, "FY2022": 21122931}),
    ("DATA", "Intangible assets", {"FY2025": 2928124, "FY2024": 153494, "FY2023": 157144, "FY2022": 254630}),
    ("TOTAL", "Total assets", {"FY2025": 1917558171, "FY2024": 1283627101, "FY2023": 919933512, "FY2022": 806196622}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 4578229, "FY2024": 302453, "FY2023": 151115, "FY2022": 213652}),
    ("DATA", "Provision for liabilities", {"FY2025": 9565009, "FY2024": 9788808, "FY2023": 7577361, "FY2022": 4881234}),
    ("DATA", "Other liabilities", {"FY2025": 5808142, "FY2024": 3011086, "FY2023": 3534309, "FY2022": 2711282}),
    ("DATA", "Deferred income", {"FY2022": 2299569}),
    ("DATA", "Deposits by banks and credit unions", {"FY2025": 36695947, "FY2024": 19058682, "FY2023": 19917773, "FY2022": 21387884}),
    ("DATA", "Repurchase agreements", {"FY2023": 19284670}),
    ("DATA", "Customer accounts", {"FY2025": 1743862044, "FY2024": 1146536321, "FY2023": 777311509, "FY2022": 700089790}),
    ("TOTAL", "Total liabilities", {"FY2025": 1800509371, "FY2024": 1178697350, "FY2023": 827776737, "FY2022": 731583411}),
    ("TOTAL", "Net assets", {"FY2025": 117048800, "FY2024": 104929751, "FY2023": 92156775, "FY2022": 74613211}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 45000000, "FY2024": 45000000, "FY2023": 45000000, "FY2022": 45000000}),
    ("DATA", "Property revaluation reserve", {"FY2025": 15764478, "FY2024": 15447589, "FY2023": 13672082, "FY2022": 13326168}),
    ("DATA", "Investment revaluation reserve", {"FY2025": -350290, "FY2024": -1348598, "FY2023": -4894285, "FY2022": -13936218}),
    ("DATA", "Profit and loss account", {"FY2025": 56634612, "FY2024": 45830760, "FY2023": 38378978, "FY2022": 30223261}),
    ("TOTAL", "Total equity", {"FY2025": 117048800, "FY2024": 104929751, "FY2023": 92156775, "FY2022": 74613211}),
]

bw.add_balance_sheet_sheet(
    title="United National Bank Limited — Balance Sheet",
    subtitle="Company basis, exact £ (not £'000/£m) - see source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Interest income", {}),
    ("DATA", "Interest receivable from debt securities", {"FY2025": 12639358, "FY2024": 8810361, "FY2023": 6781043, "FY2022": 3402074}),
    ("DATA", "Interest receivable from group undertakings", {"FY2025": 129941, "FY2024": 366363, "FY2023": 471110, "FY2022": 85430}),
    ("DATA", "Other interest receivable and similar income", {"FY2025": 89261113, "FY2024": 54771776, "FY2023": 36417814, "FY2022": 26604318}),
    ("TOTAL", "Total interest receivable", {"FY2025": 102030412, "FY2024": 63948500, "FY2023": 43669967, "FY2022": 30091822}),
    ("SECTION", "Interest expense", {}),
    ("DATA", "Interest payable to group undertakings", {"FY2025": -36039, "FY2024": -53937, "FY2023": -291812, "FY2022": -108360}),
    ("DATA", "Interest payable", {"FY2025": -70542609, "FY2024": -39858637, "FY2023": -22302031, "FY2022": -11235244}),
    ("TOTAL", "Total interest payable", {"FY2025": -70578648, "FY2024": -39912574, "FY2023": -22593843, "FY2022": -11343604}),
    ("TOTAL", "Net interest income", {"FY2025": 31451764, "FY2024": 24035926, "FY2023": 21076124, "FY2022": 18748218}),
    ("SECTION", "Non-interest income", {}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 465923, "FY2024": 574808, "FY2023": 531356, "FY2022": 463844}),
    ("DATA", "Profit from foreign exchange", {"FY2025": 380059, "FY2024": 270867, "FY2023": 623278, "FY2022": 720867}),
    ("DATA", "Fair value loss on investment properties", {"FY2025": -60000, "FY2024": -1692678}),
    ("DATA", "Profit/(loss) on realised debt securities", {"FY2025": 255520, "FY2024": -759855, "FY2023": 139910, "FY2022": 344705}),
    ("DATA", "Other operating income", {"FY2025": 90942, "FY2024": 776648, "FY2023": 366513, "FY2022": 139404}),
    ("DATA", "Profit on disposal of fixed assets", {"FY2024": 46958, "FY2022": 372270}),
    ("DATA", "Fair value gains/(losses) on derivatives", {"FY2025": -36260, "FY2024": -8502, "FY2023": -206509, "FY2022": 3635562}),
    ("TOTAL", "Total income", {"FY2025": 32547948, "FY2024": 23244172, "FY2023": 22530672, "FY2022": 24424870}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -16827131, "FY2024": -14816212, "FY2023": -12549595, "FY2022": -12752766}),
    ("DATA", "Remeasurement of financial liability", {"FY2025": -291571, "FY2024": -2561700, "FY2023": -2650000}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -297373, "FY2024": -344925, "FY2023": -597021, "FY2022": -755530}),
    ("DATA", "Impairment (losses)/recoveries", {"FY2025": -555015, "FY2024": -277396, "FY2023": 177172, "FY2022": -5620263}),
    ("TOTAL", "Profit before tax on ordinary activities", {"FY2025": 14576858, "FY2024": 5243939, "FY2023": 6911228, "FY2022": 5296311}),
    ("DATA", "Income tax (expense)/credit", {"FY2025": -3731753, "FY2024": 1894527, "FY2023": 1689239, "FY2022": -754543}),
    ("TOTAL", "Profit for the year", {"FY2025": 10845105, "FY2024": 7138466, "FY2023": 8600467, "FY2022": 4541768}),
]

bw.add_income_statement_sheet(
    title="United National Bank Limited — Profit & Loss",
    subtitle="Company basis, exact £ (not £'000/£m) - see source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Profit and Loss Account", "Investment revaluation reserve", "Property Revaluation reserve", "Total"]
equity_rows = [
    ("TOTAL", "Balance at 1 January 2022", (45000000, 25297603, -3862585, 13646702, 80081720)),
    ("DATA", "Profit for the year", (None, 4541768, None, None, 4541768)),
    ("DATA", "Actuarial gain recognised relating to the pension scheme", (None, 889850, None, None, 889850)),
    ("DATA", "Fair value loss on available for sale debt securities", (None, None, -10073633, None, -10073633)),
    ("DATA", "Gain on revaluation of freehold property", (None, None, None, 98316, 98316)),
    ("DATA", "Deferred tax relating to revaluation of freehold property", (None, None, None, 90190, 90190)),
    ("DATA", "Release of revaluation reserve on disposal of property", (None, 499440, None, -499440, 0)),
    ("DATA", "Dividend paid and declared", (None, -1015000, None, None, -1015000)),
    ("TOTAL", "Total", (45000000, 30213661, -13936218, 13335768, 74613211)),
    ("DATA", "Transfer of depreciation on revaluation surplus", (None, 9600, None, -9600, 0)),
    ("TOTAL", "Balance as at 31 December 2022", (45000000, 30223261, -13936218, 13326168, 74613211)),
    ("TOTAL", "Balance as at 1 January 2023", (45000000, 30223261, -13936218, 13326168, 74613211)),
    ("DATA", "Profit for the year", (None, 8600467, None, None, 8600467)),
    ("DATA", "Actuarial loss recognised relating to the pension scheme", (None, -454350, None, None, -454350)),
    ("DATA", "Fair value gain on available for sale debt securities", (None, None, 7410504, None, 7410504)),
    ("DATA", "Deferred tax related to available for sale debt securities", (None, None, 1631429, None, 1631429)),
    ("DATA", "Gain on revaluation of freehold property", (None, None, None, 440867, 440867)),
    ("DATA", "Deferred tax relating to revaluation of freehold property", (None, None, None, -85353, -85353)),
    ("TOTAL", "Total", (45000000, 38369378, -4894285, 13681682, 92156775)),
    ("DATA", "Transfer of depreciation on revaluation surplus", (None, 9600, None, -9600, 0)),
    ("TOTAL", "Balance as at 31 December 2023", (45000000, 38378978, -4894285, 13672082, 92156775)),
    ("TOTAL", "Balance as at 1 January 2024", (45000000, 38378978, -4894285, 13672082, 92156775)),
    ("DATA", "Profit for the year", (None, 7138466, None, None, 7138466)),
    ("DATA", "Actuarial gain recognised relating to the pension scheme", (None, 185250, None, None, 185250)),
    ("DATA", "Fair value movement on available for sale debt securities", (None, None, 4727584, None, 4727584)),
    ("DATA", "Deferred tax related to available for sale debt securities", (None, None, -1181897, None, -1181897)),
    ("DATA", "Gain on revaluation of freehold property", (None, None, None, 2514243, 2514243)),
    ("DATA", "Deferred tax relating to revaluation of freehold property", (None, None, None, -610670, -610670)),
    ("DATA", "Transfer of depreciation on disposal of property", (None, 118466, None, -118466, 0)),
    ("TOTAL", "Total", (45000000, 45821160, -1348598, 15457189, 104929751)),
    ("DATA", "Transfer of depreciation on revaluation surplus", (None, 9600, None, -9600, 0)),
    ("TOTAL", "Balance as at 31 December 2024", (45000000, 45830760, -1348598, 15447589, 104929751)),
    ("TOTAL", "Balance as at 1 January 2025", (45000000, 45830760, -1348598, 15447589, 104929751)),
    ("DATA", "Profit for the year", (None, 10845105, None, None, 10845105)),
    ("DATA", "Actuarial (loss) recognised relating to the pension scheme", (None, -41250, None, None, -41250)),
    ("DATA", "Fair value gain on available for sale debt securities", (None, None, 1331077, None, 1331077)),
    ("DATA", "Deferred tax related to available for sale debt securities", (None, None, -332769, None, -332769)),
    ("DATA", "Gain on revaluation of freehold property", (None, None, None, 394391, 394391)),
    ("DATA", "Deferred tax relating to revaluation of freehold property", (None, None, None, -77500, -77500)),
    ("TOTAL", "Balance as at 31 December 2025", (45000000, 56634615, -350290, 15764480, 117048805)),
]

bw.add_equity_changes_sheet(
    title="United National Bank Limited — Statement of Changes in Equity",
    subtitle="Company basis, exact £ (not £'000/£m), chronological (oldest to newest) - see source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax on ordinary activities for the year", {"FY2025": 14576858, "FY2024": 5243939, "FY2023": 6911228, "FY2022": 5296311}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 297373, "FY2024": 344925, "FY2023": 597021, "FY2022": 755530}),
    ("DATA", "Remeasurement of financial liability", {"FY2025": 291571, "FY2024": 2561700, "FY2023": 2650000}),
    ("DATA", "Net (reversal)/charge in respect of defined benefit pension scheme", {"FY2025": 36000, "FY2024": 35000, "FY2023": -54000, "FY2022": 3000}),
    ("DATA", "Impairment charge/(recoveries) on loans and advances and other items", {"FY2025": 555015, "FY2024": 277396, "FY2023": -133448, "FY2022": -190335}),
    ("DATA", "Impairment (recoveries)/charge on available for sale investments", {"FY2023": -43724, "FY2022": 5081559}),
    ("DATA", "Non-cash movements relating to AFS debt securities", {"FY2025": 1798841, "FY2024": 518237, "FY2023": -38664, "FY2022": 472140}),
    ("DATA", "Fair value (gain)/loss on investment properties", {"FY2025": 60000, "FY2024": 1692678, "FY2023": -157448}),
    ("DATA", "Fair value losses on derivatives", {"FY2025": 36260, "FY2024": 8502}),
    ("DATA", "Disposal of fixed assets - non cash", {"FY2024": -46958, "FY2022": -950000}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents (within adjustments)", {"FY2025": 78789, "FY2024": 203350, "FY2023": -1040191, "FY2022": 1310294}),
    ("DATA", "Change in loans to banks", {"FY2025": -771732, "FY2024": -9040080, "FY2023": -11575956, "FY2022": 253159}),
    ("DATA", "Change in loans and advances", {"FY2025": -508526134, "FY2024": -314034689, "FY2023": -82406357, "FY2022": -129900329}),
    ("DATA", "Change in other operating assets", {"FY2025": 1574513, "FY2024": -4401232, "FY2023": -2726540, "FY2022": -1703767}),
    ("DATA", "Change in deposits from banks and customers", {"FY2025": 614962983, "FY2024": 368365721, "FY2023": 75751608, "FY2022": 145891909}),
    ("DATA", "Change in other operating liabilities", {"FY2025": 4362320, "FY2024": 3532520, "FY2023": 4913759, "FY2022": -5203335}),
    ("DATA", "Corporate income tax paid", {"FY2025": -1630000, "FY2024": -1440000, "FY2023": -907009, "FY2022": -563132}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": 127702657, "FY2024": 53821009, "FY2023": -8259721, "FY2022": 20553004}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of tangible fixed and intangible assets", {"FY2025": -2953578, "FY2024": -246091, "FY2023": -710084, "FY2022": -216696}),
    ("DATA", "Proceeds from disposal of fixed assets", {"FY2024": 237859, "FY2022": 950000}),
    ("DATA", "Purchase of debt securities", {"FY2025": -1051570428, "FY2024": -750228210, "FY2023": -595299208, "FY2022": -572112956}),
    ("DATA", "Sale and maturity of debt securities", {"FY2025": 931907787, "FY2024": 714471065, "FY2023": 586985878, "FY2022": 526168675}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -122616219, "FY2024": -35765377, "FY2023": -9023414, "FY2022": -45210977}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of obligations under finance lease", {"FY2024": -21710, "FY2023": -19823, "FY2022": -8263}),
    ("DATA", "Proceeds from/(repayment of) repurchase agreements", {"FY2024": -19284670, "FY2023": 19284670}),
    ("DATA", "Dividends paid", {"FY2022": -1015000}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2024": -19306380, "FY2023": 19264847, "FY2022": -1023263}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 5086438, "FY2024": -1250748, "FY2023": 1981712, "FY2022": -25681236}),
    ("DATA", "Cash and cash equivalents at the beginning of the financial year", {"FY2025": 8271317, "FY2024": 9725415, "FY2023": 6703512, "FY2022": 33695042}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents (tail)", {"FY2025": -78789, "FY2024": -203350, "FY2023": 1040191, "FY2022": -1310294}),
    ("TOTAL", "Cash and cash equivalents at the end of the financial year", {"FY2025": 13278966, "FY2024": 8271317, "FY2023": 9725415, "FY2022": 6703512}),
]

bw.add_cash_flow_sheet(
    title="United National Bank Limited — Cash Flow Statement",
    subtitle="Company basis, exact £ (not £'000/£m) - see source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=260,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers by impairment status (FRS 102 basis - not IFRS 9 stage 1/2/3)", {}),
    ("DATA", "Impaired loans", {"FY2025": 8563357, "FY2024": 7627387, "FY2023": 14038077, "FY2022": 8027926}),
    ("DATA", "Non-impaired loans", {"FY2025": 1533904725, "FY2024": 1028820429, "FY2023": 707202735, "FY2022": 631590077}),
    ("TOTAL", "Gross loans and advances to customers", {"FY2025": 1542468082, "FY2024": 1036447816, "FY2023": 721240812, "FY2022": 639618003}),
    ("DATA", "Unamortised portion of loan fees", {"FY2025": -5320210, "FY2024": -3331731, "FY2023": -2198275}),
    ("DATA", "Collective provision", {"FY2025": -1261608, "FY2024": -706593, "FY2023": -444874, "FY2022": -368530}),
    ("DATA", "Specific impairment allowance on impaired loans", {"FY2022": -933571}),
    ("DATA", "Fair value of hedged risk", {"FY2025": 4439811, "FY2024": -54536}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 1540326075, "FY2024": 1032354956, "FY2023": 718597663, "FY2022": 638315902}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "Impaired loans as % of gross loans", {"FY2025": "0.56%", "FY2024": "0.74%", "FY2023": "1.95%", "FY2022": "1.26%"}),
    ("DATA", "Total provisions as % of gross loans", {"FY2025": "0.08%", "FY2024": "0.07%", "FY2023": "0.06%", "FY2022": "2.04%"}),
]

bw.add_asset_quality_sheet(
    title="United National Bank Limited — Asset Quality",
    subtitle="Company basis, exact £ (not £'000/£m) - see source note at bottom.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nACCOUNTING BASIS NOTE: the Company reports under FRS 102 (not IFRS 9), so its own loan-book disclosure "
        "categorises loans as 'Impaired'/'Non-Impaired' with 'Specific'/'Collective' provisions, rather than the "
        "IFRS 9 stage-1/2/3 staging used by most other banks in this project - this sheet reproduces the Company's "
        "own categories rather than forcing an IFRS 9 shape onto FRS 102 data. FY2022's collective provision "
        "(£368,530) plus specific impairment allowance (£933,571) together give total provisions of £1,302,101 "
        "against gross loans of £639,618,003 (2.04%) - materially higher than other years because FY2022 carried a "
        "specific impairment allowance against impaired loans (later years show £Nil specific allowance, impaired "
        "loans covered entirely by collective provision and/or expected recovery)."
    ),
    first_col_width=68,
    source_height=340,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Company basis, {unit}" if unit else "Company basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=150)


metric(
    "CET1 Capital", "£",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 108644570, "FY2024": 97948100, "FY2023": 88559510, "FY2022": 73598731})],
    p3_sources(),
    note="Equal to Tier 1 capital in every year - the Company has no Additional Tier 1 (AT1) instruments. FY2023's "
         "figure is confirmed to the nearest £'000 by the Pillar 3 document's own Appendix VI (£88,559k).",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2023": "21.46%", "FY2022": "19.08%", "FY2024": "19.86%", "FY2025": "Not disclosed"})],
    p3_sources(),
    note="FY2023 is directly stated in that year's Pillar 3 document (equal to its stated Tier 1 ratio, since "
         "CET1=Tier 1 capital exactly that year). FY2022 and FY2024 are computed here (CET1 capital ÷ Total RWAs, "
         "both from that year's own Pillar 3 document - see Total RWAs sheet) since neither document states the "
         "ratio as text. FY2025: no Pillar 3 document exists yet - genuine access gap, not confirmed non-disclosure.",
)

metric(
    "Tier 1 Capital", "£",
    [("Tier 1 capital", {"FY2025": 108644570, "FY2024": 97948100, "FY2023": 88559510, "FY2022": 73598731})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2023": "21.46%", "FY2022": "19.08%", "FY2024": "19.86%", "FY2025": "Not disclosed"})],
    p3_sources(),
    note="Equal to the CET1 Ratio in every year - the Company has no Additional Tier 1 (AT1) instruments. FY2023 is "
         "directly stated in that year's Pillar 3 document (Table CC1, row 62); FY2022/FY2024 computed (see CET1 "
         "Ratio sheet note); FY2025 not disclosed (no Pillar 3 document exists yet).",
)

metric(
    "Total Capital", "£",
    [("Total capital", {"FY2025": 109906178, "FY2024": 98654693, "FY2023": 89004384, "FY2022": 73967261})],
    p3_sources(),
    note="Tier 1 capital plus a Tier 2 collective provision figure disclosed in each year's own Annual Report.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2023": "21.56%", "FY2022": "19.18%", "FY2024": "20.00%", "FY2025": "Not disclosed"})],
    p3_sources(),
    note="FY2023 directly stated in that year's Pillar 3 document (Table CC1, row 63). FY2022/FY2024 computed "
         "(Total capital ÷ Total RWAs, both from that year's own Pillar 3 document). FY2025 not disclosed (no "
         "Pillar 3 document exists yet).",
)

metric(
    "Total RWAs", "£",
    [("Total risk-weighted exposure amount", {"FY2023": 412732000, "FY2022": 385707000, "FY2024": 493153000, "FY2025": "Not disclosed"})],
    p3_sources(),
    note="Each year's own Pillar 1 Capital Requirement table (Credit & Counterparty Credit Risk + Market Risk + "
         "CVA Risk + Operational Risk RWAs, summed) - see the RWA Breakdown sheet for the category-level split. "
         "FY2025: no Pillar 3 document exists yet - genuine access gap, not confirmed non-disclosure.",
)

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (Pillar 1 Minimum Capital Requirement)", {}),
    ("DATA", "Credit and Counterparty Credit Risk (Standardised)", {"FY2023": 382394000, "FY2022": 363317000, "FY2024": 456897000}),
    ("DATA", "Market Risk (Position Risk Requirement)", {"FY2023": 1222000, "FY2022": 0, "FY2024": 0}),
    ("DATA", "Credit Valuation Adjustment Risk (Simplified Method)", {"FY2023": 161000, "FY2022": 250000, "FY2024": 311000}),
    ("DATA", "Operational Risk (Basic Indicator Approach)", {"FY2023": 28955000, "FY2022": 22140000, "FY2024": 35945000}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2023": 412732000, "FY2022": 385707000, "FY2024": 493153000, "FY2025": "Not disclosed"}),
]

bw.add_rwa_breakdown_sheet(
    title="United National Bank Limited — RWA Breakdown",
    subtitle="Company basis, exact £ (not £'000/£m) - see source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\n\nEach year's category-level RWAs are its own Pillar 1 Capital Requirement table (same table cited on "
        "the Total RWAs sheet). All 3 years with data sum exactly to that year's Total RWAs. FY2025: no Pillar 3 "
        "document exists yet - genuine access gap, not confirmed non-disclosure."
    ),
    first_col_width=58,
    source_height=180,
    unit_suffix=" (£)",
)

metric(
    "Leverage Ratio", "£ / %",
    [
        ("Leverage ratio total exposure measure", {"FY2023": 954151000, "FY2022": 815698000, "FY2024": 1310997000}),
        ("Tier 1 capital used in leverage ratio calculation", {"FY2022": 73599000, "FY2024": 93996000}),
        ("Leverage ratio (%)", {"FY2023": "8.52%", "FY2022": "8.43%", "FY2024": "7.17%", "FY2025": "Not disclosed"}),
    ],
    p3_sources(),
    note="FY2022 and FY2024 now fully evidenced by each year's own Pillar 3 document (Table LRSum/LRCom), not just "
         "the narrative comparator this workbook previously relied on for FY2022. DISCREPANCY: FY2024's Pillar 3 "
         "leverage-ratio Tier 1 capital (£93,996,000, Table LRCom row 20) is ~£3.95m lower than the CET1/Tier 1 "
         "capital figure used elsewhere in this workbook for FY2024 (£97,948,100, per that same document's own "
         "Appendix VI Own Funds disclosure) - both figures are reproduced exactly as each table states, not forced "
         "to tie; the FY2022 document shows no such gap (£73,599,000 vs £73,598,731, a rounding-only difference). "
         "FY2025 not disclosed (no Pillar 3 document exists yet - see entity note on the Cash Flow Statement sheet).",
)

bw.add_not_disclosed_metric_sheets(["LCR", "NSFR"], p3_sources())

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed" for y in YEARS})],
    p3_sources(),
    note="No numeric or qualitative MREL disclosure of any kind was found for this bank in any year reviewed.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1917558171, "FY2024": 1283627101, "FY2023": 919933512, "FY2022": 806196622}),
        ("Loans and advances to customers", {"FY2025": 1540326075, "FY2024": 1032354956, "FY2023": 718597663, "FY2022": 638315902}),
        ("Customer accounts", {"FY2025": 1743862044, "FY2024": 1146536321, "FY2023": 777311509, "FY2022": 700089790}),
        ("Total equity", {"FY2025": 117048800, "FY2024": 104929751, "FY2023": 92156775, "FY2022": 74613211}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 31451764, "FY2024": 24035926, "FY2023": 21076124, "FY2022": 18748218}),
        ("Total income", {"FY2025": 32547948, "FY2024": 23244172, "FY2023": 22530672, "FY2022": 24424870}),
        ("Profit for the year", {"FY2025": 10845105, "FY2024": 7138466, "FY2023": 8600467, "FY2022": 4541768}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 104929751, "FY2024": 92156775, "FY2023": 74613211, "FY2022": 80081720}),
        ("Total comprehensive income for the year", {"FY2025": 12119054, "FY2024": 12772976, "FY2023": 17543564, "FY2022": -4453509}),
        ("Other equity movements, net", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -1015000}),
        ("Closing equity", {"FY2025": 117048805, "FY2024": 104929751, "FY2023": 92156775, "FY2022": 74613211}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 127702657, "FY2024": 53821009, "FY2023": -8259721, "FY2022": 20553004}),
        ("Net cash from/(used in) investing activities", {"FY2025": -122616219, "FY2024": -35765377, "FY2023": -9023414, "FY2022": -45210977}),
        ("Net cash from/(used in) financing activities", {"FY2024": -19306380, "FY2023": 19264847, "FY2022": -1023263}),
        ("Cash and cash equivalents at end of year", {"FY2025": 13278966, "FY2024": 8271317, "FY2023": 9725415, "FY2022": 6703512}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2023": "21.46%", "FY2022": "19.08%", "FY2024": "19.86%"}),
        ("Tier 1 Ratio", {"FY2023": "21.46%", "FY2022": "19.08%", "FY2024": "19.86%"}),
        ("Total Capital Ratio", {"FY2023": "21.56%", "FY2022": "19.18%", "FY2024": "20.00%"}),
        ("Leverage Ratio", {"FY2023": "8.52%", "FY2022": "8.43%", "FY2024": "7.17%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Pillar 3 ratios/RWA are now available for FY2022-FY2024 "
         "(recovered via Wayback Machine after the live ubluk.com site stopped linking most historic editions); "
         "FY2025 remains not disclosed since no Pillar 3 document for that year exists yet (see Cash Flow Statement "
         "sheet entity note). LCR/NSFR/MREL: not disclosed in any year reviewed. Balance Sheet/Profit & Loss/"
         "Statement of Changes in Equity/Asset Quality use FY2022's own originally-published figures, not the "
         "FY2023 report's restated FY2022 comparative - see those sheets' own source notes for the resulting "
         "~£2.26m net-loans discrepancy.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/UNITED NATIONAL FINANCIALS.xlsx")
