import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# J.P. Morgan Securities plc ("JPMS plc", company 02711006, FRN 155240) is
# JPMorgan Chase & Co.'s principal UK operating subsidiary for Markets and
# Banking (investment banking advisory, equity/debt securities, derivatives,
# clearing). Its FY2025 Annual Report confirms it applies the FRS 101
# exemption from IAS 7 "Cash flow statement and related notes" (Note 2, Basis
# of preparation) ONLY - its largest and smallest parent groups (J.P. Morgan
# Capital Holdings Limited and ultimately JPMorgan Chase & Co.) publish
# consolidated cash flow statements instead, so the Cash Flow Statement sheet
# below remains "not applicable" per the project's established policy for
# this exemption (see The Bank of New York Mellon (International) Limited /
# ABC International Bank plc / Bank Mandiri (Europe) Limited / DB UK Bank
# Limited). The full Balance Sheet/P&L/Statement of Changes in Equity/Asset
# Quality ARE published and are built below (ST-024).
#
# Reports in USD ('000s) - the Company's functional currency (equity capital is
# held in USD per its own FX-risk-to-capital-ratio note). Point-in-time capital/RWA
# figures converted to GBP at each year-end's Bank of England GBP/USD spot rate,
# using the same rate table established for Zenith Bank (UK) Limited/other FX
# banks in this project; %-ratios are dimensionless and left unconverted.
#
# The official JPMorgan archive was recoverable in this revisit and exposes
# standalone JPMS plc annual Pillar 3 disclosures for FY2021-FY2025. These
# reports support the historical capital, RWA, leverage and LCR series directly;
# NSFR is supported from FY2022 onward. No standalone numeric MREL ratio is
# reported in the recovered disclosures, so that sheet remains explicitly
# unavailable rather than being inferred from subordinated capital instruments.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/02711006/filing-history/MzUxOTQxNzUzOGFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/02711006/filing-history/MzQ2NDE1MTk5OGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/02711006/filing-history/MzQyMDg4NTQwMWFkaXF6a2N4/document?format=pdf&download=0"
P3_ARCHIVE_URL = "https://jpmorganchaseco.gcs-web.com/financial-information/basel-pillar-3-us-lcr-disclosures"

# STATEMENTS COVERAGE NOTE: Companies House's public filing history for this
# entity (company 02711006) genuinely only begins 26 January 2024 - no
# earlier Annual Report of any kind is publicly filed, confirmed by paging
# through the entity's full filing history (~250 filings, overwhelmingly
# MR01 charge registrations). Only 3 Full Accounts filings exist: made up to
# 31 December 2023 (filed 13 May 2024, AR2023_URL), 31 December 2024 (filed
# 28 April 2025, AR2024_URL), and 31 December 2025 (filed 10 May 2026,
# AR2025_URL). FY2022's Balance Sheet/P&L/Equity figures ARE available - as
# AR2023's own comparative column, checked in full detail (not just a
# closing total) - but FY2021's are genuinely not: AR2023's equity statement
# opens at "1 January 2022" with no earlier detail. FY2021's Pillar 3
# capital/RWA/leverage/LCR figures remain available via the standalone
# Pillar 3 archive (see P3_2021_URL below) and are unaffected by this gap.

FX_SPOT = {  # Bank of England GBP/USD spot rate, 31 December each year (USD per £1)
    "FY2021": 1.3521,
    "FY2022": 1.2097,
    "FY2023": 1.2732,
    "FY2024": 1.2515,
    "FY2025": 1.3448,
}


def stock(usd):
    """Point-in-time (capital/RWA) USD '000s -> GBP '000s at that year-end's spot rate."""
    return {y: round(v / FX_SPOT[y]) for y, v in usd.items()}


ENTITY_NOTE = (
    "ENTITY NOTE: J.P. Morgan Securities plc (\"JPMS plc\", company 02711006, FRN 155240, incorporated 30 April "
    "1992) is a public limited company, an indirect subsidiary of JPMorgan Chase Bank, N.A. and a principal "
    "operating subsidiary of JPMorgan Chase & Co. (\"the Firm\") in the UK, engaged in international investment "
    "banking activity across Markets (client-facing and trading entity for the majority of Markets EMEA ex EU) and "
    "Banking (primary M&A advisory entity). It also operates a branch in Zurich. FY2025: $831bn total assets, $50bn "
    "total equity, $9,542,478k net operating income - Annual Report 2025, Strategic Report p.2. All monetary "
    "figures below are the Company's own entity-level (not the wider JPMorgan Chase Group's consolidated) "
    "disclosure, reported in USD, converted to GBP at each year-end's spot rate (see FX_SPOT table) for point-in-"
    "time capital/RWA figures; %-ratios are shown exactly as reported (dimensionless, not converted)."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: the FY2025 Annual Report's Note 2 \"Basis of preparation\" states these financial "
    "statements are prepared under FRS 101 'Reduced Disclosure Framework' and lists the IFRS exemptions applied, "
    "including \"Cash flow statement and related notes, IAS 7 'Cash flow statements'\" - Annual Report 2025, Note "
    f"2, p.61 - {AR2025_URL}. The Annual Report's own Contents page (p.i) does not list a Statement of Cash Flows "
    "anywhere among its financial statements (Income statement p.57, Statement of comprehensive income p.58, "
    "Balance sheet p.59, Statement of changes in equity p.60, Notes p.61-112 - no cash flow statement). Note 1 "
    "confirms the Company's results are consolidated into both J.P. Morgan Capital Holdings Limited's accounts "
    "(smallest group) and JPMorgan Chase & Co.'s accounts (largest group), both of which publish their own "
    "consolidated cash flow statements. Per the project's established policy for this exemption, this workbook is "
    "built as a PILLAR-3-ONLY variant: no cash flow figures exist to show, while the recovered capital and liquidity "
    "metrics are populated below."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

ACCESS_GAP_NOTE = (
    "SOURCE COVERAGE NOTE: the official JPMorgan archive exposes standalone annual JPMS plc Pillar 3 disclosures "
    "for FY2021, FY2022, FY2023, FY2024 and FY2025. The FY2021 report uses the older Key Metrics format and does "
    "not provide an NSFR series; the FY2022 report provides FY2022 NSFR but not a FY2021 NSFR comparative. The "
    "recovered reports describe the MREL framework and capital instruments issued in support of the Firm's MREL "
    "strategy, but do not provide a JPMS plc numeric MREL ratio or requirement.\n\n"
    "MANUAL-RETRIEVAL VERIFICATION (2026-09-15): JPMorgan's IR host (jpmorganchaseco.gcs-web.com) returns HTTP "
    "403 to automated requests, so the FY2021 and FY2022 reports were retrieved by hand and re-read in full. "
    "Every FY2021 and FY2022 figure on these sheets was re-confirmed against the primary documents and matched "
    "exactly, with no basis break and nothing added or altered. Specifically: FY2021 was previously cited from "
    "the FY2022 report's Q4 2021 comparative column, and is now independently confirmed against the FY2021 "
    "report's OWN tables - Table 1 'Key Metrics' p.6 (Tier 1 $41,911mm, Total Own Funds $53,911mm, RWA "
    "$226,258mm, Tier 1 ratio 18.52%, Total capital ratio 23.83%, Leverage exposure $729,749mm / 5.74%, LCR "
    "216%) and Table 47 'EU LIQ1' p.34 (liquidity buffer $71,625mm, total net cash outflows $33,228mm). "
    "The two FY2021 gaps are confirmed genuine, not access failures: (a) NSFR - the FY2021 report contains zero "
    "occurrences of 'NSFR'/'Net Stable Funding' anywhere, and the FY2022 report states \"The NSFR ratio and the "
    "amount of available and required stable funding are disclosed for the first time in this 2022 annual Pillar "
    "3\", with its KM1 Q4 2021 NSFR cells (rows 18-20) left blank; (b) the LCR cash-inflow/cash-outflow "
    "components - FY2021's Table 47 reports only liquidity buffer and total net cash outflows, and the FY2022 "
    "KM1's Q4 2021 column likewise leaves rows UK 16a/16b blank. MREL remains narrative-only in both documents "
    "(framework discussion plus a glossary entry; no numeric ratio), re-confirmed by full-text search."
)

P3_2021_URL = "https://jpmorganchaseco.gcs-web.com/static-files/41a50bf4-81db-4063-8e55-8703a0fc500f"
P3_2022_URL = "https://jpmorganchaseco.gcs-web.com/static-files/d761ba10-ab1b-4309-8a4d-24cb70fd6cc1"
P3_2023_URL = "https://jpmorganchaseco.gcs-web.com/static-files/3645e9a4-c721-404e-a901-70fa73fac642"
P3_2024_URL = "https://jpmorganchaseco.gcs-web.com/static-files/a170e6df-d951-42fc-9897-2aa04d681885"
P3_2025_URL = "https://jpmorganchaseco.gcs-web.com/static-files/a51475c0-d908-423e-b8de-6410d277a867"


def p3_sources():
    return (
        "Sources - J.P. Morgan Securities plc, all $'000 figures converted to £'000 at the Bank of England GBP/USD "
        f"spot rate as at each year-end (FY2021: 1.3521, FY2022: 1.2097, FY2023: 1.2732, FY2024: 1.2515, FY2025: 1.3448):\n"
        f"FY2025: Annual Pillar 3 Disclosure 2025, UK KM1 Table 1 - {P3_2025_URL}\n"
        f"FY2024: Annual Pillar 3 Disclosure 2024, UK KM1 Table 1 - {P3_2024_URL}\n"
        f"FY2023: Annual Pillar 3 Disclosure 2023, UK KM1 Table 1 - {P3_2023_URL}\n"
        f"FY2022: Annual Pillar 3 Disclosure 2022, UK KM1 Table 4 - {P3_2022_URL}\n"
        f"FY2021: Annual Pillar 3 Disclosure 2021, Key Metrics Table 1 and LCR Table 47 - {P3_2021_URL}\n"
        f"FY2025/FY2024 capital precision cross-check: Annual Report 2025, Strategic Report, \"Capital risk\" table, p.10 - {AR2025_URL}\n\n"
        + ACCESS_GAP_NOTE
    )


def statements_sources():
    return (
        "Sources - J.P. Morgan Securities plc's own entity-level financial statements, in the Company's own "
        "reporting currency (US$'000, NOT converted to £ - unlike the Pillar 3 sheets' point-in-time capital/RWA "
        "figures, which are GBP-converted per this script's established convention; kept in USD here for direct, "
        "unconverted comparability with the primary statements as filed):\n"
        f"FY2025/FY2024: Annual Report 2025, Income statement p.57, Statement of comprehensive income p.58, "
        f"Balance sheet p.59, Statement of changes in equity p.60, Notes 15-16 p.79-80 - {AR2025_URL}\n"
        f"FY2023/FY2022: Annual Report 2023 (accounts made up to 31 December 2023), Income statement p.68, "
        f"Statement of comprehensive income p.69, Balance sheet p.70, Statement of changes in equity p.71, "
        f"Notes 15-16 p.90 - {AR2023_URL}\n"
        f"FY2024's own originally-published figures (Annual Report 2024, made up to 31 December 2024) were "
        f"cross-checked against AR2025's FY2024 comparative column and found identical (both show Profit for "
        f"the financial year $2,596,449k) - {AR2024_URL}\n\n"
        + STATEMENTS_COVERAGE_NOTE
    )


STATEMENTS_COVERAGE_NOTE = (
    "STATEMENTS COVERAGE NOTE: Companies House's public filing history for this entity genuinely only begins "
    "26 January 2024 (confirmed by paging through the full ~250-filing history) - only 3 Full Accounts filings "
    "exist (FY2023, FY2024, FY2025). FY2022's Balance Sheet/P&L/Equity figures ARE available, as AR2023's own "
    "comparative column (checked in full detail, not just a closing total), but FY2021's are genuinely not - "
    "AR2023's equity statement opens at \"1 January 2022\" with no earlier detail, so FY2021's Balance Sheet, "
    "P&L, Statement of Changes in Equity and Asset Quality are blank (not zero, not guessed) below. FY2021's "
    "Pillar 3 capital/RWA/leverage/LCR figures remain available via the standalone Pillar 3 archive (see the "
    "Pillar 3 sheets) and are unaffected by this gap."
)

bw = BankWorkbook(bank_name="J.P. Morgan Securities plc", years=YEARS, year_label=YEAR_LABEL, header_color="C104D3")

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 1440217, "FY2024": 3100890, "FY2023": 9069418, "FY2022": 11743695}),
    ("DATA", "Loans and advances to banks", {"FY2025": 7579349, "FY2024": 9456743, "FY2023": 4418798, "FY2022": 5260582}),
    ("DATA", "Loans and advances to customers", {"FY2025": 257277, "FY2024": 92593, "FY2023": 300256, "FY2022": 518663}),
    ("DATA", "Securities purchased under agreements to resell", {"FY2025": 235021525, "FY2024": 215556422, "FY2023": 181266110, "FY2022": 178125963}),
    ("DATA", "Securities borrowed", {"FY2025": 70821133, "FY2024": 48189827, "FY2023": 51259430, "FY2022": 50891145}),
    ("DATA", "Financial assets at fair value through profit or loss", {"FY2025": 378354083, "FY2024": 326845417, "FY2023": 326699107, "FY2022": 343441285}),
    ("DATA", "Debtors", {"FY2025": 132996016, "FY2024": 90926839, "FY2023": 92547261, "FY2022": 110736501}),
    ("DATA", "Other assets", {"FY2025": 4410838, "FY2024": 3424164, "FY2023": 2986428, "FY2022": 2525721}),
    ("DATA", "Investments in JPMorgan Chase undertakings", {"FY2023": 28, "FY2022": 872}),
    ("DATA", "Tangible assets", {"FY2025": 3109, "FY2024": 3133, "FY2023": 2894, "FY2022": 3027}),
    ("TOTAL", "Total assets", {"FY2025": 830883547, "FY2024": 697596028, "FY2023": 668549730, "FY2022": 703247454}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Securities sold under agreements to repurchase", {"FY2025": 125001077, "FY2024": 94404028, "FY2023": 65301124, "FY2022": 72184220}),
    ("DATA", "Securities loaned", {"FY2025": 30887772, "FY2024": 15284668, "FY2023": 13080624, "FY2022": 13573027}),
    ("DATA", "Financial liabilities at fair value through profit or loss", {"FY2025": 256717599, "FY2024": 233190651, "FY2023": 237519957, "FY2022": 273608227}),
    ("DATA", "Financial liabilities designated at fair value through profit or loss", {"FY2025": 54303069, "FY2024": 38744425, "FY2023": 25485640, "FY2022": 22156522}),
    ("DATA", "Trade creditors", {"FY2025": 85370421, "FY2024": 51353155, "FY2023": 60941932, "FY2022": 57028087}),
    ("DATA", "Deposits from JPMorganChase undertakings", {"FY2025": 189371965, "FY2024": 178311538, "FY2023": 180934577, "FY2022": 174404967}),
    ("DATA", "Other liabilities", {"FY2025": 28446802, "FY2024": 27089411, "FY2023": 27891296, "FY2022": 31803394}),
    ("DATA", "Subordinated liabilities with JPMorganChase undertakings", {"FY2025": 11000000, "FY2024": 11000000, "FY2023": 11000000, "FY2022": 12000000}),
    ("TOTAL", "Total liabilities", {"FY2025": 781098705, "FY2024": 649377876, "FY2023": 622155150, "FY2022": 656758444}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called-up share capital", {"FY2025": 12443530, "FY2024": 12443530, "FY2023": 12443530, "FY2022": 12443530}),
    ("DATA", "Share premium account", {"FY2025": 9950724, "FY2024": 9950724, "FY2023": 9950724, "FY2022": 9950724}),
    ("DATA", "Other equity instruments", {"FY2025": 10000000, "FY2024": 10000000, "FY2023": 10000000, "FY2022": 5000000}),
    ("DATA", "Capital redemption reserve", {"FY2025": 4996040, "FY2024": 4996040, "FY2023": 4996040, "FY2022": 4996040}),
    ("DATA", "Other reserves", {"FY2025": 324555, "FY2024": 331859, "FY2023": 211755, "FY2022": 1689478}),
    ("DATA", "Retained earnings", {"FY2025": 12069993, "FY2024": 10495999, "FY2023": 8792531, "FY2022": 12409238}),
    ("TOTAL", "Total equity", {"FY2025": 49784842, "FY2024": 48218152, "FY2023": 46394580, "FY2022": 46489010}),
    ("TOTAL", "Total liabilities and equity funds", {"FY2025": 830883547, "FY2024": 697596028, "FY2023": 668549730, "FY2022": 703247454}),
]

bw.add_balance_sheet_sheet(
    title="J.P. Morgan Securities plc — Balance Sheet",
    subtitle="Entity-level basis, US$'000 (not GBP-converted - see source note). FY2021 blank: no Annual Report of any kind is publicly filed for that year - see source note.",
    rows=balance_sheet_rows,
    sources_text=statements_sources(),
    first_col_width=76,
    source_height=340,
    unit_suffix=" ($'000)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 21080660, "FY2024": 20129417, "FY2023": 16278933, "FY2022": 7143359}),
    ("DATA", "Interest expense and similar expense", {"FY2025": -20960587, "FY2024": -21947988, "FY2023": -18122826, "FY2022": -7162970}),
    ("TOTAL", "Net interest income/(expense)", {"FY2025": 120073, "FY2024": -1818571, "FY2023": -1843893, "FY2022": -19611}),
    ("DATA", "Fee and commission income", {"FY2025": 3714964, "FY2024": 3406538, "FY2023": 2867099, "FY2022": 2843343}),
    ("DATA", "Fee and commission expense", {"FY2025": -1373587, "FY2024": -1316427, "FY2023": -1252046, "FY2022": -1618349}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 2341377, "FY2024": 2090111, "FY2023": 1615053, "FY2022": 1224994}),
    ("DATA", "Trading profit", {"FY2025": 7093839, "FY2024": 8863313, "FY2023": 8795451, "FY2022": 6655165}),
    ("DATA", "Dividend income", {"FY2023": 17}),
    ("DATA", "Expected credit loss (charge)/release", {"FY2025": -12811, "FY2024": 9219, "FY2023": -6318, "FY2022": 6279}),
    ("TOTAL", "Net operating income", {"FY2025": 9542478, "FY2024": 9144072, "FY2023": 8560310, "FY2022": 7866827}),
    ("DATA", "Administrative expenses", {"FY2025": -6270069, "FY2024": -5184705, "FY2023": -4992840, "FY2022": -4669692}),
    ("DATA", "Other impairment", {"FY2024": -6, "FY2022": -177}),
    ("DATA", "Other expenses", {"FY2024": -122500}),
    # Not a line the source statement itself prints - the Company's own
    # income statement has no combined opex subtotal, going straight from
    # these three expense lines to Profit before taxation. This row is
    # simply their sum (ties exactly to Net operating income - Profit before
    # taxation in every year: e.g. FY2025 9542478-6270069=3272409), added
    # 2026-09-07 so cost-to-income analysis has a "Total operating expenses"
    # numerator to work from.
    ("TOTAL", "Total operating expenses (sum of the expense lines above - not itself a printed subtotal)", {
        "FY2025": -6270069, "FY2024": -5307211, "FY2023": -4992840, "FY2022": -4669869,
    }),
    ("TOTAL", "Profit before taxation", {"FY2025": 3272409, "FY2024": 3836861, "FY2023": 3567470, "FY2022": 3196958}),
    ("DATA", "Tax on profit", {"FY2025": -928331, "FY2024": -1240412, "FY2023": -989297, "FY2022": -750277}),
    ("TOTAL", "Profit for the financial year", {"FY2025": 2344078, "FY2024": 2596449, "FY2023": 2578173, "FY2022": 2446681}),
    ("SECTION", "Other comprehensive income/(expense)", {}),
    ("DATA", "Actuarial (loss)/gain on pension schemes", {"FY2025": -6768, "FY2024": 16182, "FY2023": -5336, "FY2022": 96384}),
    ("DATA", "Tax effect of movement in pension reserve", {"FY2025": 1896, "FY2024": -8038, "FY2023": 3117, "FY2022": -29389}),
    ("DATA", "Movement attributed to own credit risk on financial liabilities designated at FVTPL", {"FY2025": -51815, "FY2024": 43910, "FY2023": -9755, "FY2022": 36565}),
    ("DATA", "Fair value movement on loans at FVOCI", {"FY2025": -2923, "FY2024": 2365, "FY2023": -5883, "FY2022": -3347}),
    ("DATA", "Movement in ECL on loans at FVOCI", {"FY2025": 3406, "FY2024": -6755, "FY2023": -8826, "FY2022": -646}),
    ("DATA", "Tax effect on loans at FVOCI", {"FY2025": -167, "FY2024": -1313, "FY2023": 651, "FY2022": 2106}),
    ("TOTAL", "Total other comprehensive (expense)/income", {"FY2025": -56371, "FY2024": 46351, "FY2023": -26032, "FY2022": 101673}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 2287707, "FY2024": 2642800, "FY2023": 2552141, "FY2022": 2548354}),
]

bw.add_income_statement_sheet(
    title="J.P. Morgan Securities plc — Profit & Loss",
    subtitle="Entity-level basis, US$'000 (not GBP-converted - see source note). FY2021 blank - see source note.",
    rows=income_statement_rows,
    sources_text=statements_sources(),
    first_col_width=82,
    source_height=340,
    unit_suffix=" ($'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - built via the per-year reconciliation
# ladder: Balance Sheet built first (above), then equity transcribed
# year-by-year. Ties exactly at every boundary (opening = prior year's own
# closing = prior year's own Balance Sheet Total equity) for all 4
# available years - zero plug rows needed anywhere.
# ---------------------------------------------------------------
EQUITY_HEADERS = [
    "Called-up share capital", "Share premium account", "Other equity instruments",
    "Capital redemption reserve", "Capital contribution reserve", "Pension reserve",
    "Other reserves", "Retained earnings", "Total equity",
]

equity_rows = [
    ("TOTAL", "Balance as at 1 January 2022", (12443530, 9950724, None, 4996040, 1588615, 6874, 27448, 17462557, 46475788)),
    ("DATA", "Profit for the financial year", (None, None, None, None, None, None, None, 2446681, 2446681)),
    ("DATA", "Gain related to own credit risk on financial liabilities designated at FVTPL", (None, None, None, None, None, None, 36565, None, 36565)),
    ("DATA", "Movement in fair value of loans at FVOCI", (None, None, None, None, None, None, -3347, None, -3347)),
    ("DATA", "Movement in ECL on loans at FVOCI", (None, None, None, None, None, None, -646, None, -646)),
    ("DATA", "Actuarial gain on pension schemes", (None, None, None, None, None, 96384, None, None, 96384)),
    ("DATA", "Tax effect on loans at FVOCI", (None, None, None, None, None, None, 2106, None, 2106)),
    ("DATA", "Tax effect on movement in pension reserve", (None, None, None, None, None, -29389, None, None, -29389)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, None, None, 66995, 34678, 2446681, 2548354)),
    ("DATA", "Additional Tier 1 notes issuance during the year", (None, None, 5000000, None, None, None, None, None, 5000000)),
    ("DATA", "Group share-based payment costs", (None, None, None, None, None, None, 316328, None, 316328)),
    ("DATA", "Group share-based payment costs recharged", (None, None, None, None, None, None, -316328, None, -316328)),
    ("DATA", "Tax effect on share-based payments", (None, None, None, None, None, None, -41920, None, -41920)),
    ("DATA", "Dividends paid", (None, None, None, None, None, None, None, -7500000, -7500000)),
    ("DATA", "Movement in other reserves", (None, None, None, None, None, None, 6788, None, 6788)),
    ("TOTAL", "Balance as at 31 December 2022 (ties to Balance Sheet's own FY2022 Total equity)", (12443530, 9950724, 5000000, 4996040, 1588615, 73869, 26994, 12409238, 46489010)),
    ("DATA", "Profit for the financial year", (None, None, None, None, None, None, None, 2578173, 2578173)),
    ("DATA", "Loss related to own credit risk on financial liabilities designated at FVTPL", (None, None, None, None, None, None, -9755, None, -9755)),
    ("DATA", "Movement in fair value of loans at FVOCI", (None, None, None, None, None, None, -5883, None, -5883)),
    ("DATA", "Movement in ECL on loans at FVOCI", (None, None, None, None, None, None, -8826, None, -8826)),
    ("DATA", "Actuarial (loss)/gain on pension schemes", (None, None, None, None, None, -5336, None, None, -5336)),
    ("DATA", "Tax effect on loans at FVOCI", (None, None, None, None, None, None, 651, None, 651)),
    ("DATA", "Tax effect on movement in pension reserve", (None, None, None, None, None, 3117, None, None, 3117)),
    ("TOTAL", "Total comprehensive income/(expense) for the year", (None, None, None, None, None, -2219, -23813, 2578173, 2552141)),
    ("DATA", "Additional Tier 1 notes issuance during the year", (None, None, 5000000, None, None, None, None, None, 5000000)),
    ("DATA", "Additional Tier 1 interest", (None, None, None, None, None, None, None, -783495, -783495)),
    ("DATA", "Group share-based payment costs", (None, None, None, None, None, None, 335076, None, 335076)),
    ("DATA", "Group share-based payment costs recharged", (None, None, None, None, None, None, -335076, None, -335076)),
    ("DATA", "Tax effect on share-based payments", (None, None, None, None, None, None, 45938, None, 45938)),
    ("DATA", "Dividends paid", (None, None, None, None, -1588615, None, None, -5411385, -7000000)),
    ("DATA", "Movement in other reserves", (None, None, None, None, None, None, 90986, None, 90986)),
    ("TOTAL", "Balance as at 31 December 2023 (ties to Balance Sheet's own FY2023 Total equity)", (12443530, 9950724, 10000000, 4996040, None, 71650, 140105, 8792531, 46394580)),
    ("DATA", "Profit for the financial year", (None, None, None, None, None, None, None, 2596449, 2596449)),
    ("DATA", "Gain related to own credit risk on financial liabilities designated at FVTPL", (None, None, None, None, None, None, 43910, None, 43910)),
    ("DATA", "Movement in fair value of loans at FVOCI", (None, None, None, None, None, None, 2365, None, 2365)),
    ("DATA", "Movement in ECL on loans at FVOCI", (None, None, None, None, None, None, -6755, None, -6755)),
    ("DATA", "Actuarial gain on pension schemes", (None, None, None, None, None, 16182, None, None, 16182)),
    ("DATA", "Tax effect on loans at FVOCI", (None, None, None, None, None, None, -1313, None, -1313)),
    ("DATA", "Tax effect on movement in pension reserve", (None, None, None, None, None, -8038, None, None, -8038)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, None, None, 8144, 38207, 2596449, 2642800)),
    ("DATA", "Additional Tier 1 interest", (None, None, None, None, None, None, None, -914609, -914609)),
    ("DATA", "Group share-based payment costs", (None, None, None, None, None, None, 356679, None, 356679)),
    ("DATA", "Group share-based payment costs recharged", (None, None, None, None, None, None, -356679, None, -356679)),
    ("DATA", "Tax effect on share-based payments", (None, None, None, None, None, None, 74208, 21628, 95836)),
    ("DATA", "Movement in other reserves", (None, None, None, None, None, None, -455, None, -455)),
    ("TOTAL", "Balance as at 31 December 2024 (ties to Balance Sheet's own FY2024 Total equity)", (12443530, 9950724, 10000000, 4996040, None, 79794, 252065, 10495999, 48218152)),
    ("DATA", "Profit for the financial year", (None, None, None, None, None, None, None, 2344078, 2344078)),
    ("DATA", "Loss related to own credit risk on financial liabilities designated at FVTPL", (None, None, None, None, None, None, -51815, None, -51815)),
    ("DATA", "Movement in fair value of loans at FVOCI", (None, None, None, None, None, None, -2923, None, -2923)),
    ("DATA", "Movement in ECL on loans at FVOCI", (None, None, None, None, None, None, 3406, None, 3406)),
    ("DATA", "Actuarial loss on pension schemes", (None, None, None, None, None, -6768, None, None, -6768)),
    ("DATA", "Tax effect on loans at FVOCI", (None, None, None, None, None, None, -167, None, -167)),
    ("DATA", "Tax effect on movement in pension reserve", (None, None, None, None, None, 1896, None, None, 1896)),
    ("TOTAL", "Total comprehensive income/(expense) for the year", (None, None, None, None, None, -4872, -51499, 2344078, 2287707)),
    ("DATA", "Additional Tier 1 interest", (None, None, None, None, None, None, None, -819887, -819887)),
    ("DATA", "Group share-based payment costs", (None, None, None, None, None, None, 294100, None, 294100)),
    ("DATA", "Group share-based payment costs recharged", (None, None, None, None, None, None, -294100, None, -294100)),
    ("DATA", "Tax effect on share-based payments", (None, None, None, None, None, None, 48039, 49803, 97842)),
    ("DATA", "Movement in other reserves", (None, None, None, None, None, None, 1028, None, 1028)),
    ("TOTAL", "Balance as at 31 December 2025 (ties to Balance Sheet's own FY2025 Total equity)", (12443530, 9950724, 10000000, 4996040, None, 74922, 249633, 12069993, 49784842)),
]

bw.add_equity_changes_sheet(
    title="J.P. Morgan Securities plc — Statement of Changes in Equity",
    subtitle="Entity-level basis, US$'000 (not GBP-converted). Chronological roll-forward, 1 January 2022 to 31 December 2025 - the earliest opening balance publicly available (see source note). Reconciliation ladder confirmed: every closing balance ties exactly to both the next year's own opening balance and that year's own Balance Sheet Total equity - zero plug rows needed anywhere. \"Capital contribution reserve\" was fully applied against dividends in FY2023 and doesn't reappear from FY2024 onward, matching the Company's own later statements dropping that column.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=statements_sources(),
    first_col_width=64,
    source_height=260,
    col_width=15,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement (not applicable - FRS 101 exemption)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Not applicable", {}),
    ("DATA", "J.P. Morgan Securities plc takes the FRS 101 exemption from preparing a Statement of Cash Flows "
             "(IAS 7) every year covered by this workbook - see source note below.", {}),
]

bw.add_cash_flow_sheet(
    title="J.P. Morgan Securities plc — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=260,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to banks", {}),
    ("DATA", "Loans and advances to banks (amortised cost)", {"FY2025": 7579349, "FY2024": 9456743, "FY2023": 4418798, "FY2022": 5260582}),
    ("SECTION", "Loans and advances to customers", {}),
    ("DATA", "Amortised cost", {"FY2025": 33890, "FY2024": 80178, "FY2023": 220463, "FY2022": 262313}),
    ("DATA", "FVOCI", {"FY2025": 224877, "FY2024": 15638, "FY2023": 83853, "FY2022": 265089}),
    ("TOTAL", "Gross loans and advances to customers", {"FY2025": 258767, "FY2024": 95816, "FY2023": 304316, "FY2022": 527402}),
    ("DATA", "Expected credit loss impairment (amortised cost)", {"FY2025": -1490, "FY2024": -3223, "FY2023": -4060, "FY2022": -8739}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 257277, "FY2024": 92593, "FY2023": 300256, "FY2022": 518663}),
    ("DATA", "ECL coverage ratio (amortised-cost loans and advances to customers)", {
        "FY2025": "4.40%", "FY2024": "4.02%", "FY2023": "1.84%", "FY2022": "3.33%",
    }),
    ("SECTION", "Income statement movement (memo)", {}),
    ("DATA", "Expected credit loss (charge)/release for the year", {"FY2025": -12811, "FY2024": 9219, "FY2023": -6318, "FY2022": 6279}),
]

bw.add_asset_quality_sheet(
    title="J.P. Morgan Securities plc — Asset Quality",
    subtitle="Entity-level basis, US$'000. No IFRS 9 Stage 1/2/3 split is disclosed - the Company's loan book is a small wholesale corporate/institutional book alongside a much larger securities-financing/trading balance sheet, and Note 16 shows only a gross/impairment/net split by measurement basis, not by stage (confirmed by reading the note in full). FY2021 blank - see source note.",
    rows=asset_quality_rows,
    sources_text=statements_sources() + (
        "\n\nNote 16 'Loans and advances to customers' (referenced above) covers the Company's wholesale loan "
        "portfolio only - large corporates and institutional clients - and is a small fraction of the balance "
        "sheet dominated by securities financing and trading positions. ECL coverage ratio is a derived figure "
        "(ECL impairment / amortised-cost gross loans), not directly disclosed, computed for a cleaner asset-"
        "quality signal since FVOCI loans don't carry a separate on-balance-sheet impairment line."
    ),
    first_col_width=76,
    source_height=340,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=140)


CET1_USD = {
    "FY2025": 37434585,
    "FY2024": 36053977,
    "FY2023": 34321000,
    "FY2022": 39571000,
    "FY2021": 41911000,
}
TIER1_USD = {
    "FY2025": 47434585,
    "FY2024": 46053977,
    "FY2023": 44321000,
    "FY2022": 44571000,
    "FY2021": 41911000,
}
TOTAL_CAP_USD = {
    "FY2025": 55987951,
    "FY2024": 55806030,
    "FY2023": 55230000,
    "FY2022": 56571000,
    "FY2021": 53911000,
}
RWA_USD = {
    "FY2025": 227965642,
    "FY2024": 195273360,
    "FY2023": 187226000,
    "FY2022": 166720000,
    "FY2021": 226258000,
}

# ---------------------------------------------------------------
# KM1 Key Metrics - the Bank's own published UK KM1 template, reproduced whole.
# Called BEFORE the first add_metric_sheet() so the sheet lands at index 6,
# immediately after Asset Quality and immediately before CET1 Capital.
#
# STAYS IN US$'mm AS PUBLISHED. The 11 single-metric sheets above/below are
# GBP-converted at each year-end's spot rate (see FX_SPOT); this sheet is a
# reproduction of a prescribed disclosure and is not converted, re-rounded or
# reordered. verify_workbook.py detects the currency break from the row labels
# and skips the amount rows rather than reporting them as disagreements; the
# six ratio rows are currency-free and ARE cross-checked.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital ($'mm)",
     {"FY2025": 37435, "FY2024": 36054, "FY2023": 34321, "FY2022": 39571, "FY2021": 41911}),
    ("DATA", "2    Tier 1 capital ($'mm)",
     {"FY2025": 47435, "FY2024": 46054, "FY2023": 44321, "FY2022": 44571, "FY2021": 41911}),
    ("DATA", "3    Total capital ($'mm)",
     {"FY2025": 55988, "FY2024": 55806, "FY2023": 55230, "FY2022": 56571, "FY2021": 53911}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4    Total risk-weighted exposure amount ($'mm)",
     {"FY2025": 227966, "FY2024": 195273, "FY2023": 187226, "FY2022": 166720, "FY2021": 226258}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2025": "16.42%", "FY2024": "18.46%", "FY2023": "18.33%", "FY2022": "23.73%", "FY2021": "18.52%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "20.81%", "FY2024": "23.58%", "FY2023": "23.67%", "FY2022": "26.73%", "FY2021": "18.52%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "24.56%", "FY2024": "28.58%", "FY2023": "29.50%", "FY2022": "33.93%", "FY2021": "23.83%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2025": "1.52%", "FY2024": "1.52%", "FY2023": "1.46%", "FY2022": "1.49%", "FY2021": "1.41%"}),
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)",
     {"FY2025": "0.51%", "FY2024": "0.51%", "FY2023": "0.49%", "FY2022": "0.50%", "FY2021": "0.47%"}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)",
     {"FY2025": "0.67%", "FY2024": "0.68%", "FY2023": "0.65%", "FY2022": "0.66%", "FY2021": "0.63%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2025": "10.70%", "FY2024": "10.70%", "FY2023": "10.59%", "FY2022": "10.64%", "FY2021": "10.51%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2025": "0.62%", "FY2024": "0.59%", "FY2023": "0.50%", "FY2022": "0.19%", "FY2021": "0.04%"}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2025": "3.12%", "FY2024": "3.09%", "FY2023": "3.00%", "FY2022": "2.69%", "FY2021": "2.54%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2025": "13.82%", "FY2024": "13.79%", "FY2023": "13.59%", "FY2022": "13.33%", "FY2021": "13.05%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "10.40%", "FY2024": "12.44%", "FY2023": "8.98%", "FY2022": "14.39%", "FY2021": "12.52%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks ($'mm)",
     {"FY2025": 757150, "FY2024": 607589, "FY2023": 572319, "FY2022": 580992, "FY2021": 729749}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "6.26%", "FY2024": "7.58%", "FY2023": "7.74%", "FY2022": "7.67%", "FY2021": "5.74%"}),
    ("SECTION", "Additional leverage ratio disclosure requirements", {}),
    ("DATA", "14a    Fully loaded ECL accounting model leverage ratio excluding claims on central banks (%)",
     {"FY2025": "6.26%", "FY2024": "7.58%"}),
    ("DATA", "14b    Leverage ratio including claims on central banks (%)",
     {"FY2025": "6.25%", "FY2024": "7.54%"}),
    ("DATA", "14c    Average leverage ratio excluding claims on central banks (%)",
     {"FY2025": "5.82%", "FY2024": "6.61%"}),
    ("DATA", "14d    Average leverage ratio including claims on central banks (%)",
     {"FY2025": "5.79%", "FY2024": "6.58%"}),
    ("DATA", "14e    Countercyclical leverage ratio buffer (%)",
     {"FY2025": "0.20%", "FY2024": "0.20%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value -average) ($'mm)",
     {"FY2025": 124463, "FY2024": 101202, "FY2023": 78544, "FY2022": 76119, "FY2021": 71625}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value ($'mm)",
     {"FY2025": 171627, "FY2024": 143440, "FY2023": 136030, "FY2022": 145955}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value ($'mm)",
     {"FY2025": 97895, "FY2024": 89342, "FY2023": 106007, "FY2022": 121958}),
    ("DATA", "16    Total net cash outflows (adjusted value) ($'mm)",
     {"FY2025": 73732, "FY2024": 54098, "FY2023": 35384, "FY2022": 36489, "FY2021": 33228}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2025": "174.25%", "FY2024": "192.75%", "FY2023": "222.82%", "FY2022": "208.50%", "FY2021": "216.00%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18    Total available stable funding ($'mm)",
     {"FY2025": 222212, "FY2024": 205106, "FY2023": 171918, "FY2022": 171384}),
    ("DATA", "19    Total required stable funding ($'mm)",
     {"FY2025": 187812, "FY2024": 175883, "FY2023": 147370, "FY2022": 142084}),
    ("DATA", "20    NSFR ratio (%)",
     {"FY2025": "118.55%", "FY2024": "117.56%", "FY2023": "116.64%", "FY2022": "121.09%"}),
]

KM1_SOURCES = (
    "Sources - J.P. Morgan Securities plc's own published UK KM1 key-metrics template, reproduced as printed, "
    "in US$'mm. ONE document covers the whole series: JPMorgan publishes a single annual UK Pillar 3 report "
    "(\"Annual Pillar 3 Disclosure\" / \"Main Disclosure ... Large Subsidiaries\"), and from FY2024 that report "
    "carries TWO separate KM1 tables - Table 1 for JPMS plc in $'mm and Table 2 for J.P. Morgan Europe Limited "
    "in GBP. Only Table 1 is used here; Table 2 belongs to the separate JP MORGAN EUROPE workbook. Each column "
    "below comes from the edition in which that year is the reporting year, except FY2021 - see RULE 28 NOTE.\n"
    f"FY2025: Annual Pillar 3 Disclosure 2025, Table 1 \"UK KM1 - Key metrics template for JPMS plc\", printed "
    f"Page 8, Q4 2025 column - {P3_2025_URL}\n"
    f"FY2024: Annual Pillar 3 Disclosure 2024, Table 1 \"UK KM1 - Key metrics template for JPMS plc\", printed "
    f"Page 8, Q4 2024 column - {P3_2024_URL}\n"
    f"FY2023: Annual Pillar 3 Disclosure 2023, Table 1 \"UK KM1 - Key metrics template\", printed Page 7, "
    f"Q4 2023 column (that edition covers JPMS plc alone, so its KM1 carries no entity suffix) - {P3_2023_URL}\n"
    f"FY2022: Annual Pillar 3 Disclosure 2022, Table 4 \"UK KM1 - Key metrics template\", printed Page 14, "
    f"Q4 2022 column - {P3_2022_URL}\n"
    f"FY2021: Annual Pillar 3 Disclosure 2022, Table 4, printed Page 14, Q4 2021 COMPARATIVE column - "
    f"{P3_2022_URL}. See RULE 28 NOTE below.\n"
    "Printed folios verified 2026-09-17 against each page's own running header (\"Annual Pillar 3 Disclosure "
    "<year> ... Page N\", read at full page width) AND against that edition's own List of Tables; the two agree "
    "in every edition and the offset from the PDF sheet index is zero throughout.\n\n"
    "RULE 28 NOTE - WHY FY2021 COMES FROM THE FY2022 EDITION. The FY2021 edition publishes no UK KM1 at all. "
    "What it prints instead, as \"Table 1: Key Metrics\" on printed Page 6, is a different and much shorter "
    "table: eleven rows, unnumbered, covering TWO entities side by side (JPMS plc and J.P. Morgan Markets "
    "Limited), with no CET1 capital row, no CET1 ratio row, no SREP block, no combined-buffer block, no overall "
    "capital requirement, no CET1-available-after-SREP row, no HQLA/cash-outflow/cash-inflow build-up and no "
    "NSFR rows at all - and with a \"Tier 2 Capital\" row the UK template does not have. It is therefore not an "
    "unnumbered version of the template but a different table, and the template is simply not used that year "
    "(the UK template post-dates that edition). Because no FY2021 KM1 exists in its own edition, and the FY2022 "
    "edition does print a full Q4 2021 comparative in the template, this workbook takes FY2021 from that "
    "comparative rather than leaving the column blank. Cross-check: every figure the FY2021 edition's own table "
    "DOES publish reappears unchanged in the FY2022 comparative - Tier 1 capital 41,911, total own funds 53,911, "
    "RWA 226,258, Tier 1 ratio 18.52%, total capital ratio 23.83%, leverage exposure 729,749, leverage ratio "
    "5.74%, LCR 216% - so the comparative restates nothing; it adds the template rows FY2021 never printed. "
    "Rows UK 16a, UK 16b, 18, 19 and 20 are blank in that comparative and are left blank here.\n\n"
    "ROW-SET DRIFT, REPRODUCED NOT NORMALISED. The \"Additional leverage ratio disclosure requirements\" block "
    "(rows 14a-14e) appears ONLY in the FY2024 and FY2025 editions. The FY2022 and FY2023 editions go straight "
    "from row 14 to the Liquidity Coverage Ratio section. The FY2024 edition's Q4 2023 COMPARATIVE does print "
    "14a-14e (7.74 / 7.62 / 7.61 / 7.53 / 0.20), but FY2023's own edition did not, so those five cells are left "
    "BLANK for FY2023 rather than back-filled: each year comes from its own edition wherever its own edition "
    "prints the table. Rows UK 8a, UK 9a, 10 and UK 10a are not shown at all because JPMS plc has never printed "
    "them in any edition; a row the bank did not print is not invented here.\n\n"
    "NO RESTATEMENT FOUND. Every row that appears in two editions for the same date was compared across those "
    "editions and is identical: the FY2024 edition's Q4 2023 comparative matches the FY2023 edition's own Q4 "
    "2023 column digit for digit, the FY2023 edition's Q4 2022 comparative matches the FY2022 edition's own Q4 "
    "2022 column, and the FY2025 edition's Q4 2024 comparative matches the FY2024 edition's own Q4 2024 column.\n\n"
    "CURRENCY - DELIBERATE DIVERGENCE FROM THE METRIC SHEETS. This sheet is in US$'mm exactly as published. The "
    "CET1 Capital / Tier 1 Capital / Total Capital / Total RWAs / Leverage Ratio / LCR / NSFR sheets in this "
    "same workbook are GBP-converted at each year-end's Bank of England spot rate (FY2021 1.3521, FY2022 "
    "1.2097, FY2023 1.2732, FY2024 1.2515, FY2025 1.3448), per this script's established convention. The "
    "amounts on this sheet will therefore NOT equal the amounts on those sheets; the ratios will, since ratios "
    "are currency-free. Nothing is converted here - KM1 reproduces a prescribed disclosure.\n\n"
    "LEVEL OF APPLICATION (verified in the documents, 2026-09-17). JPMS plc is a large subsidiary of J.P. "
    "Morgan Capital Holdings Limited (\"JPMCHL\") under Rule 2.3 of Chapter 2 of the Disclosure (CRR) part of "
    "the UK PRA Rulebook, and this report is the disclosure it makes in that capacity. JPMCHL, the UK "
    "consolidated parent, files its own separate UK Pillar 3 whose KM1 is the JPMCHL GROUP's, not this "
    "entity's, and is not used here. JPMorgan Chase & Co.'s US Basel disclosures and J.P. Morgan SE's German "
    "disclosures are different entities again and are likewise not substituted.\n\n"
    "ACCESS (rule 9 - a fact about our reach, not about the bank). jpmorganchaseco.gcs-web.com returns an "
    "Akamai HTTP 403 to automated requests, including with a full browser User-Agent, Referer and Sec-Fetch "
    "headers. The FY2023 edition used above was retrieved from the Internet Archive on 2026-09-17 "
    "(web.archive.org/web/2024id_/ the FY2023 static-file URL; HTTP 200, application/pdf, 705,988 bytes, %PDF "
    "magic bytes and a complete %%EOF), and the FY2024 and FY2025 editions the same way; the FY2021 and FY2022 "
    "editions were retrieved by hand in an earlier session. The disclosures page itself was read on 2026-09-17 "
    "through a reader proxy and its newest annual item is \"Main Disclosure 2025 - Large Subsidiaries\", i.e. "
    "the FY2025 edition already cited above. The block is never recorded as a non-publication.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="J.P. Morgan Securities plc — KM1 Key Metrics",
    subtitle="The Bank's own published \"UK KM1 - Key metrics template\" (Table 1 from FY2024, Table 4 in FY2022), "
             "reproduced in its own row order, row numbers, labels and printed precision. AMOUNTS ARE IN US$'mm "
             "AS PUBLISHED — this sheet is NOT GBP-converted, unlike the single-metric Pillar 3 sheets that "
             "follow it. Rows 14a–14e exist only in the FY2024 and FY2025 editions. FY2021 is the FY2022 edition's "
             "own Q4 2021 comparative column, because the FY2021 edition publishes a different, shorter "
             "key-metrics table and not the template — see the source note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=82,
    source_height=760,
)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", stock(CET1_USD))],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2025": "16.4%", "FY2024": "18.5%", "FY2023": "18.33%",
        "FY2022": "23.73%", "FY2021": "18.52%",
    })],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Total Tier 1 capital (CET1 and Additional Tier 1)", stock(TIER1_USD))],
    p3_sources(),
    note="The source disclosures show no AT1 in FY2021, $5,000,000k in FY2022, and $10,000,000k from FY2023 onward; "
         "the Tier 1 series includes those directly reported AT1 instruments.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 capital ratio", {
        "FY2025": "20.8%", "FY2024": "23.6%", "FY2023": "23.67%",
        "FY2022": "26.73%", "FY2021": "18.52%",
    })],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital (CET1, Additional Tier 1 and Tier 2)", stock(TOTAL_CAP_USD))],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {
        "FY2025": "24.6%", "FY2024": "28.6%", "FY2023": "29.50%",
        "FY2022": "33.93%", "FY2021": "23.83%",
    })],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total Risk Weighted Assets (RWA)", stock(RWA_USD))],
    p3_sources(),
    note="Comprises Credit RWAs, Market RWAs and Operational RWAs - Annual Report 2025 p.10 gives the full "
         "breakdown (not reproduced here; this sheet shows the total only, consistent with other banks in this "
         "project's Total RWAs sheet).",
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 15177000, "FY2024": 9286000, "FY2023": 10053000, "FY2022": 10641000, "FY2021": 13496000}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 122375000, "FY2024": 109870000, "FY2023": 98418000, "FY2022": 81647000, "FY2021": 121546000}),
    ("DATA", "Settlement risk", {"FY2025": 1138000, "FY2024": 396000, "FY2023": 531000, "FY2022": 652000, "FY2021": 809000}),
    ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {"FY2025": 54000, "FY2024": 228000, "FY2023": 251000, "FY2022": 241000}),
    ("DATA", "Market risk (position, FX and commodities)", {"FY2025": 72187000, "FY2024": 59510000, "FY2023": 63153000, "FY2022": 59086000, "FY2021": 75691000}),
    ("DATA", "Operational risk", {"FY2025": 17035000, "FY2024": 15983000, "FY2023": 14820000, "FY2022": 14453000, "FY2021": 14102000}),
    ("DATA", "Amounts below the thresholds for deduction (FY2021 own separate additive line only - see source note)", {"FY2021": 614000}),
    ("TOTAL", "Total risk-weighted exposure amount", RWA_USD),
]

RWA_BREAKDOWN_SOURCES = (
    "Sources - J.P. Morgan Securities plc's own entity-level UK OV1 'Overview of RWAs' table, US$'000 (NOT "
    "GBP-converted, consistent with the Balance Sheet/P&L/Equity sheets above), each year's own originally-"
    "published figures:\n"
    f"FY2025: Annual Pillar 3 Disclosure 2025, Table 8, p.20 (Q4 2025 column) - {P3_2025_URL}\n"
    f"FY2024: Annual Pillar 3 Disclosure 2024, Table 8, p.20 (Q4 2024 column) - {P3_2024_URL}\n"
    f"FY2023: Annual Pillar 3 Disclosure 2023, Table 8, p.20 (Q4 2023 comparative column, cross-checked against "
    f"the FY2023 report's own Q4 2023 column) - {P3_2023_URL}\n"
    f"FY2022: Annual Pillar 3 Disclosure 2022, Table 5, p.15 (Q4 2022 column) - {P3_2022_URL}\n"
    f"FY2021: Annual Pillar 3 Disclosure 2022, Table 5, p.15 (Q4 2021 comparative column) - {P3_2022_URL}\n\n"
    "All 5 years' Total row ties to the pre-existing Total RWAs sheet's own RWA_USD figures exactly (FY2023/"
    "FY2022) or within rounding of the source document's own $'mm precision (FY2025/FY2024, off by ~$0.4m on "
    "~$228bn; FY2021, off by ~$0.5bn on ~$226bn against the sum of the 6 headline categories alone). FY2021's "
    "own OV1 table (Annual Pillar 3 Disclosure 2022's comparative column) includes 'Amounts below the "
    "thresholds for deduction' as an additive line item that year (per that vintage's footnote: 'blank cells in "
    "2021 represent changes on account of CRR2 implementation') - included here for FY2021 only, since without "
    "it FY2021's components underrun the disclosed Total by exactly that amount ($614m); FY2022-FY2025's own "
    "tables do not include this line additively (their 6 headline categories alone already tie to the disclosed "
    "Total). FY2021's Securitisation exposures line is blank - that year's own footnote states SFT exposure "
    "value is folded into CCR instead of shown separately, so it is not a missing figure. Both P3_ARCHIVE_URL "
    "and the individual P3_2021-2025_URL documents required a browser-like User-Agent/Referer to fetch this "
    "session (intermittent Akamai edge blocking on the plain default request, not a permanent access "
    "restriction) - the ST-024 fork's original 'access gap' was a transient fetch failure, not a genuine "
    "non-disclosure.\n\n"
    "MANUAL-RETRIEVAL VERIFICATION (2026-09-15): the FY2021 and FY2022 reports were retrieved by hand (the IR "
    "host now returns a hard HTTP 403 to automated requests) and both OV1 tables re-read in full. FY2021 is now "
    "independently confirmed against its OWN report - 'Table 7: EU OV1 - Overview of RWAs for JPMS plc', p.12-13 "
    "of the Annual Pillar 3 Disclosure 2021 - rather than only the FY2022 comparative: Credit risk (excl CCR) "
    "13,496 + CCR 121,546 + Settlement risk 809 + Market risk 75,691 + Operational risk 14,102 + Amounts below "
    "thresholds 614 = 226,258, footing exactly to the disclosed Total. FY2022 re-confirmed against 'Table 5: UK "
    "OV1', p.15 of the Annual Pillar 3 Disclosure 2022: 10,641 + 81,647 + 652 + 241 + 59,086 + 14,453 = 166,720, "
    "also exact. This re-verifies the additive-line treatment above from both directions: FY2022's own table "
    "does print an 'Amounts below the thresholds for deduction' figure ($604m, row 24), but adding it would "
    "OVERSHOOT that year's disclosed Total by exactly $604m, whereas omitting FY2021's $614m would UNDERRUN "
    "FY2021's Total by exactly that amount - so the asymmetric treatment is the source documents' own, not an "
    "inconsistency here. Every row above matched exactly; nothing was added or altered."
)

bw.add_rwa_breakdown_sheet(
    title="J.P. Morgan Securities plc — RWA Breakdown",
    subtitle="Entity-level basis, US$'000 (not GBP-converted).",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=90,
    source_height=280,
    unit_suffix=" ($'000)",
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Leverage exposure", stock({
            "FY2025": 757149645, "FY2024": 607589034, "FY2023": 572319000,
            "FY2022": 580992000, "FY2021": 729749000,
        })),
        ("Leverage ratio (%)", {
            "FY2025": "6.3%", "FY2024": "7.6%", "FY2023": "7.74%",
            "FY2022": "7.67%", "FY2021": "5.74%",
        }),
    ],
    p3_sources(),
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA) (weighted value - average)", stock({
            "FY2025": 124463000, "FY2024": 101202000, "FY2023": 78544000,
            "FY2022": 76119000, "FY2021": 71625000,
        })),
        ("Cash outflows - total weighted value", stock({
            "FY2025": 171627000, "FY2024": 143440000, "FY2023": 136030000,
            "FY2022": 145955000,
        })),
        ("Cash inflows - total weighted value", stock({
            "FY2025": 97895000, "FY2024": 89342000, "FY2023": 106007000,
            "FY2022": 121958000,
        })),
        ("Total net cash outflows (adjusted value)", stock({
            "FY2025": 73732000, "FY2024": 54098000, "FY2023": 35384000,
            "FY2022": 36489000, "FY2021": 33228000,
        })),
        ("Liquidity coverage ratio", {
            "FY2025": "174.25%", "FY2024": "192.75%", "FY2023": "222.82%",
            "FY2022": "208.50%", "FY2021": "216%",
        }),
    ],
    p3_sources(),
    note="FY2021's older LCR table reports liquidity buffer and total net cash outflows but does not separately report the cash-outflow and cash-inflow components; those two cells are intentionally blank for FY2021.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", stock({
            "FY2025": 222212000, "FY2024": 205106000, "FY2023": 171918000,
            "FY2022": 171384000,
        })),
        ("Total required stable funding", stock({
            "FY2025": 187812000, "FY2024": 175883000, "FY2023": 147370000,
            "FY2022": 142084000,
        })),
        ("NSFR ratio", {
            "FY2025": "118.55%", "FY2024": "117.56%", "FY2023": "116.64%",
            "FY2022": "121.09%",
        }),
    ],
    p3_sources(),
    note="The FY2021 standalone disclosure does not contain an NSFR series; the recovered FY2022 disclosure provides NSFR from FY2022 onward but no FY2021 comparative.",
)

# GA-020 (2026-09-19). FY2021/FY2022: full-text search recorded in ACCESS_GAP_NOTE (manual retrieval
# 2026-09-15). FY2023-FY2025: the IR host still returns HTTP 403 / times out to direct requests, so each
# edition was read on 2026-09-19 as a text render through the r.jina.ai reader proxy ('P3 Annual Solo 2023',
# 42pp; '2024', 51pp; '2025'; 'capital' 70/142/98 hits). Every MREL hit is framework narrative, the glossary,
# or the Tier 2 footnote on the USD subordinated loan issued 'as part of the Firm's strategy to comply with
# MREL'; no ratio or requirement figure. A proxy render is a view, so this negative is recorded as such.
JPMS_MREL_STATEMENT = ("Not published – no JPMS plc MREL ratio in this year's Pillar 3: MREL appears only as "
                       "framework narrative and the Tier 2 MREL-loan footnote (full-text search 2026-09-15/19)")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    statements={"MREL Ratio": JPMS_MREL_STATEMENT},
    per_note={
        "MREL Ratio": "The recovered standalone disclosures describe the MREL framework and identify subordinated instruments issued in support of the Firm's MREL strategy, but no JPMS plc numeric MREL ratio or requirement is reported. No ratio is inferred from the capital instruments. GA-020 re-check 2026-09-19: FY2023-FY2025 editions re-read as text renders (the IR host blocks direct requests) - MREL hits are framework narrative, glossary and the Tier 2 subordinated-loan footnote only.",
    },
)

# ---------------------------------------------------------------
# Overview sheet (no cash-flow chart - FRS 101 exemption - but now has
# Balance Sheet/P&L/Equity blocks like the rest of the project)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 830883547, "FY2024": 697596028, "FY2023": 668549730, "FY2022": 703247454}),
        ("Loans and advances to customers", {"FY2025": 257277, "FY2024": 92593, "FY2023": 300256, "FY2022": 518663}),
        ("Deposits from JPMorganChase undertakings", {"FY2025": 189371965, "FY2024": 178311538, "FY2023": 180934577, "FY2022": 174404967}),
        ("Total equity", {"FY2025": 49784842, "FY2024": 48218152, "FY2023": 46394580, "FY2022": 46489010}),
    ],
    balance_sheet_unit="$'000",
    income_statement_totals=[
        ("Net interest income/(expense)", {"FY2025": 120073, "FY2024": -1818571, "FY2023": -1843893, "FY2022": -19611}),
        ("Trading profit", {"FY2025": 7093839, "FY2024": 8863313, "FY2023": 8795451, "FY2022": 6655165}),
        ("Administrative expenses", {"FY2025": -6270069, "FY2024": -5184705, "FY2023": -4992840, "FY2022": -4669692}),
        ("Profit for the financial year", {"FY2025": 2344078, "FY2024": 2596449, "FY2023": 2578173, "FY2022": 2446681}),
    ],
    income_statement_unit="$'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 48218152, "FY2024": 46394580, "FY2023": 46489010, "FY2022": 46475788}),
        ("Total comprehensive income for the year", {"FY2025": 2287707, "FY2024": 2642800, "FY2023": 2552141, "FY2022": 2548354}),
        ("Other equity movements, net", {"FY2025": -721017, "FY2024": -819228, "FY2023": -2646571, "FY2022": -2535132}),
        ("Closing equity", {"FY2025": 49784842, "FY2024": 48218152, "FY2023": 46394580, "FY2022": 46489010}),
    ],
    equity_changes_unit="$'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.4%", "FY2024": "18.5%", "FY2023": "18.33%", "FY2022": "23.73%", "FY2021": "18.52%"}),
        ("Tier 1 Ratio", {"FY2025": "20.8%", "FY2024": "23.6%", "FY2023": "23.67%", "FY2022": "26.73%", "FY2021": "18.52%"}),
        ("Total Capital Ratio", {"FY2025": "24.6%", "FY2024": "28.6%", "FY2023": "29.50%", "FY2022": "33.93%", "FY2021": "23.83%"}),
        ("Leverage Ratio", {"FY2025": "6.3%", "FY2024": "7.6%", "FY2023": "7.74%", "FY2022": "7.67%", "FY2021": "5.74%"}),
        ("LCR", {"FY2025": "174.25%", "FY2024": "192.75%", "FY2023": "222.82%", "FY2022": "208.50%", "FY2021": "216%"}),
        ("NSFR", {"FY2025": "118.55%", "FY2024": "117.56%", "FY2023": "116.64%", "FY2022": "121.09%"}),
    ],
    note="No cash-flow summary or chart: J.P. Morgan Securities plc takes the FRS 101 cash-flow-statement exemption every year (see the Cash Flow Statement sheet). Balance Sheet/P&L/Equity blocks cover FY2022-FY2025 only (in US$'000, the Company's own reporting currency) - FY2021 predates the entity's public Companies House filing history (see the Balance Sheet sheet's source note). The Pillar 3 ratios below remain GBP-converted per this script's established convention and cover FY2021-FY2025 (NSFR from FY2022) - the recovered archive provides standalone JPMS plc capital, leverage and LCR data for FY2021-FY2025, and no numeric MREL ratio.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/JP MORGAN SECURITIES FINANCIALS.xlsx")
