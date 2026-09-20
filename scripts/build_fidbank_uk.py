import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

# ---------------------------------------------------------------
# FX conversion (FidBank UK reports in USD; converting to £ per this
# project's established FX methodology - see build_zenith.py precedent).
# Unlike other banks in this series, rates are NOT sourced from the Bank of
# England independently - FidBank UK's own Annual Report discloses its own
# Dollar/Sterling exchange rate (year-end and average) for each year in its
# 5-year Financial Highlights table, so those entity-disclosed rates are used
# directly (£1 = $X), avoiding any independent-source mismatch.
# ---------------------------------------------------------------
FX_SPOT = {  # "Year End" rate, £1 = $X
    "FY2025": 1.35,
    "FY2024": 1.25,
    "FY2023": 1.27,
    "FY2022": 1.20,
    "FY2021": 1.35,  # from the FY2025 AR's own 5-year Financial Highlights table (p.6) -
                      # needed only to convert FY2022's opening balance (= FY2021's closing
                      # balance) at the correct spot rate; no FY2021 cash flow statement exists.
}
FX_AVG = {  # "Average" rate, £1 = $X
    "FY2025": 1.32,
    "FY2024": 1.28,
    "FY2023": 1.25,
    "FY2022": 1.23,
}
PREV_YEAR = {"FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024", "FY2022": "FY2021"}


def flow(usd):
    """Flow (cash flow statement line item) figures, £'000, at that year's average rate."""
    return {y: round(v / FX_AVG[y], 1) for y, v in usd.items() if y in FX_AVG}


def stock(usd):
    """Point-in-time (balance) figures, £'000, at that year's period-end spot rate."""
    return {y: round(v / FX_SPOT[y], 1) for y, v in usd.items() if y in FX_SPOT}


def opening_cash(usd):
    """Opening cash balance, £'000 - uses the PRIOR year's period-end spot rate."""
    return {y: round(v / FX_SPOT[PREV_YEAR[y]], 1) for y, v in usd.items() if y in PREV_YEAR}


# ---------------------------------------------------------------
# Source documents (all via Companies House - FidBank UK's own site has no
# investor-relations/regulatory-disclosures section; only 3 Annual Report
# filings exist at Companies House at all, none earlier - see ENTITY_NOTE)
# ---------------------------------------------------------------
CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/04661188/filing-history"
AR2025_URL = f"{CH_BASE}/MzUzMzg1ODU2NWFkaXF6a2N4/document?format=pdf&download=0"  # filed 25 Jul 2026, covers FY2025+FY2024
AR2023_URL = f"{CH_BASE}/MzQxOTU1NjA5M2FkaXF6a2N4/document?format=pdf&download=0"  # filed 26 Apr 2024, covers FY2023+FY2022
P3_2024_URL = "https://fidbank.co.uk/assets/Uploads/NewFolder/FidBank-UK-Pillar-3-Disclosure-2024.pdf"
P3_2023_URL = "https://fidbank.co.uk/assets/Uploads/NewFolder/FidBank-UK-Pillar-3-Disclosure-2023.pdf"
P3_2022_URL = "https://fidbank.co.uk/assets/Uploads/NewFolder/FBUK-Pillar-3-Disclosure-2022.pdf"
P3_2021_URL = "https://fidbank.co.uk/assets/Uploads/NewFolder/FBUK-Pillar-3-Disclosure-2021.pdf"

ENTITY_NOTE = (
    "FidBank UK Limited (company 04661188, FRN 400712) is a wholly-owned subsidiary of Fidelity Bank Plc, "
    "Nigeria (listed on the Nigerian Stock Exchange). The company has changed name twice: incorporated 2003 "
    "as \"Union Bank UK PLC\", later became \"Fidelity Bank UK Limited\", then renamed \"FidBank UK Limited\" "
    "on 13/14 March 2024 (per Companies House and the FY2023 Annual Report's own Subsequent Events note). "
    "Only 3 Annual Report filings exist at Companies House at all (FY2023, FY2024, FY2025) - no earlier "
    "filings were found, consistent with this being a young/thin filer at Companies House even though the "
    "company itself is over 20 years old; FY2021's cash flow could not be sourced from any document and is "
    "left blank rather than estimated (the FY2025 Annual Report's own 5-year \"Financial Highlights\" table "
    "gives only headline P&L/balance-sheet figures for FY2021, not a line-item cash flow statement).\n\n"
    "PRESENTATION CHANGE: the FY2023 Annual Report's cash flow statement (covering FY2023/FY2022) and the "
    "FY2025 Annual Report's cash flow statement (covering FY2025/FY2024) use different line-item structures "
    "and different terminology for the closing cash balance (\"Cash and cash equivalents\" in the FY2023 "
    "vintage vs. \"Cash and cash equivalents (including bank placements)\" in the FY2025 vintage) - each "
    "year's own line items and labels are preserved as printed rather than forced into a common format, per "
    "project convention.\n\n"
    "UNEXPLAINED CASH-BRIDGE GAP: FY2023's own statement shows closing cash and cash equivalents of "
    "US$7,127k. The FY2025 Annual Report's own comparative shows the FY2024 column's OPENING balance as "
    "US$115,901k - a US$108,774k gap between the two filings' figures for what should be the same balance "
    "sheet date (31 Dec 2023). This is plausibly explained by the broadened \"(including bank placements)\" "
    "definition introduced in the newer presentation, but this could not be confirmed from the source "
    "documents available - left unreconciled and flagged here rather than forced to match, per project "
    "convention (compare Arab Bank Europe's/Bank of China UK's similar unreconciled gaps elsewhere in this "
    "project).\n\n"
    "SOURCE-LABEL NOTE: the FY2025 Annual Report's cash flow statement labels BOTH columns' opening-balance "
    "row \"at 31 December 2024\" - this is a source-document label copy-paste artifact (the FY2024 column's "
    "opening balance is actually as at 31 December 2023); the VALUES are used exactly as printed, only the "
    "shared row label is affected.\n\n"
    "FX METHODOLOGY NOTE, FY2023/FY2022: the opening cash balance for these two years is converted at the "
    "correct PRIOR-year spot rate (FY2022's opening uses FY2021's own year-end $/£ rate of 1.35, sourced from "
    "the FY2025 Annual Report's 5-year Financial Highlights table, p.6 - no FY2021 cash flow statement exists "
    "for this entity, but its exchange rate is separately disclosed there). Because the FY2023 Annual Report's "
    "own USD figures tie exactly with no FX line (single-currency presentation), converting opening/flow/"
    "closing at three different correct rates (prior-year spot / this year's average / this year's spot) "
    "necessarily creates a translation gap in GBP terms - a genuine 'Exchange difference / effect of GBP-USD "
    "translation' line for FY2023/FY2022 is computed programmatically from the actual converted figures (see "
    "_FY2023_FY2022_TRANSLATION_PLUG in the build script) and shown alongside FY2025/FY2024's real disclosed "
    "exchange-difference line, per this project's established FX conversion methodology."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are FidBank UK Limited's own Statement of Cash Flows (Bank-only, GBP figures "
    "converted from the source's own USD figures at FidBank UK's own disclosed Dollar/Sterling exchange "
    "rates - see FX methodology note below):\n"
    f"FY2025, FY2024: Annual Report and Financial Statements for the year ended 31 December 2025, p.37 "
    f"(Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2023, FY2022: Annual Report & Financial Statements for the year ended 31 December 2023, p.26 "
    f"(Statement of Cash Flows) - {AR2023_URL}\n"
    "FY2021: not available - no source document with line-item cash flow detail was found (see entity note).\n\n"
    "FX conversion methodology: this project converts flow (cash flow statement) figures at each year's "
    "average GBP/USD rate and point-in-time (balance) figures at that year's period-end spot rate. FidBank "
    "UK's own Annual Report discloses its own Dollar/Sterling exchange rates (year-end and average) directly "
    "in its 5-year Financial Highlights table each year - those entity-disclosed rates are used here rather "
    "than an independently-sourced Bank of England rate, since they are explicitly stated as the rates the "
    "entity itself used to prepare its accounts. Ratios are never converted (dimensionless, currency-"
    "invariant).\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - FidBank UK Limited Pillar 3/capital basis:\n"
        f"FY2025, FY2024: Annual Report and Financial Statements for the year ended 31 December 2025 - "
        f"\"Financial Highlights\" (p.6) and \"Performance Metrics\" (p.7) - {AR2025_URL}\n"
        f"FY2023, FY2022, FY2021: Annual Report and Financial Statements for the year ended 31 December "
        f"2025's own 5-year \"Financial Highlights\" comparative table (p.6), cross-checked against the "
        f"FY2023 Annual Report's own 5-year Financial Highlights table (p.3), which independently confirms "
        f"the same FY2023/FY2022/FY2021 figures - {AR2025_URL} ; {AR2023_URL}\n\n"
        f"Pillar 3 sources: FY2024 p.9 - {P3_2024_URL}; FY2023 p.9 - {P3_2023_URL}; "
        f"FY2022 pp.6,10 - {P3_2022_URL}; FY2021 pp.6,10 - {P3_2021_URL}.\n\n"
        "Primary-source correction (HD-064): FidBank UK's own Reporting Archive publishes standalone, "
        "entity-level Pillar 3 disclosures for FY2021-FY2024. The FY2023/FY2024 UK KM1 tables disclose "
        "CET1, Tier 1, total capital, RWA, capital ratios, leverage, LCR and NSFR; FY2021/FY2022's older "
        "disclosures give the capital base and RWA components. These replace the prior incorrect blanket "
        "claim that no Pillar 3 document existed. MREL remains not disclosed.\n\n"
        "FY2025 PILLAR 3 STATUS (re-verified 15 September 2026): no FY2025 Pillar 3 disclosure has been "
        "published. Four filename permutations under the Bank's own /assets/Uploads/ paths return a genuine "
        "404 while the FY2024 file at the same path still serves a 775KB PDF, so the site is live and the "
        "FY2025 document simply is not there; a Wayback CDX sweep of the whole fidbank.co.uk domain filtered "
        "on 'pillar' returns exactly three documents, the newest being the FY2024 edition (archived 17 January "
        "2026). FidBank publishes its Pillar 3 roughly 12-13 months after year-end, so the FY2025 edition "
        "would be expected around January 2027.\n"
        "Consequently CET1 Ratio, Tier 1 Ratio, Total RWAs, Leverage Ratio and NSFR are all BLANK for FY2025 "
        "and are NOT derived. The FY2025 Annual Report (a scanned, image-only filing with no text layer - "
        "Creator 'go-tiff2pdf' - read here by rendering all 69 pages at 250 dpi and OCRing, with every figure "
        "used re-checked visually at 450 dpi) discloses the capital AMOUNT (Total Tier 1 = Total Regulatory "
        "Capital = US$55,665k, Note 30, p.64) and the LCR (178%, Performance Metrics, p.7), but gives NO "
        "risk-weighted-asset amount, NO leverage ratio and NO NSFR anywhere in the document ('stable funding' "
        "returns zero hits). Total RWAs is specifically NOT back-solved from capital / the 21.99% ratio: the "
        "ratio is rounded to 2dp and the document contradicts itself on its value (see the Total Capital Ratio "
        "sheet), so any implied RWA would be both imprecise and basis-ambiguous.\n"
        "COMPARATIVE DISCREPANCY, recorded not resolved: the FY2025 Annual Report's capital table shows a "
        "FY2024 comparative of US$55,005k, whereas this workbook carries US$55,029k for FY2024 sourced from "
        "the FY2024 Pillar 3 disclosure itself. The US$24k difference is unexplained in the document. Per this "
        "project's convention of preferring each year's own report, the FY2024 figure is left at 55,029 from "
        "its own Pillar 3; the AR's differing comparative is flagged here rather than silently overwritten.\n"
        + extra
    )


CAPITAL_RATIO_NOTE = (
    "CAUTION: this is FidBank UK's own headline \"Capital Ratio\" (Shareholders' Funds ÷ Risk Weighted "
    "Assets, per the source's own stated formula), NOT necessarily a standard regulatory Total Capital Ratio "
    "(CET1+AT1+T2 ÷ RWA) since the numerator is an accounting equity figure, not a confirmed regulatory-"
    "capital figure. Used as the best available proxy since no other capital ratio breakdown is disclosed. "
    "FY2025's Performance Metrics infographic (p.7) separately states this same ratio as 21.64%, a minor "
    "internal inconsistency with the Strategic Report 'Key Performance Indicators' section (p.12), which "
    "gives 21.99% twice. The 21.99% figure is used here, because it appears in the formal KPI section "
    "rather than in a summary infographic; 21.64% is recorded rather than discarded, and the inconsistency "
    "is the bank's own. Both readings were confirmed visually at 450 dpi, not by OCR alone.\n\n"
    "STALE-NOTE CORRECTION (2026-09-18). This paragraph previously said the ratio used here was 21.46%, "
    "'the Financial Highlights table's own' figure. That was wrong twice over: 21.46% appears NOWHERE in "
    "the FY2025 Annual Report - it was a transcription error, corrected on 15 September 2026 - and the "
    "script has carried 21.99% ever since. The note was simply not updated with the figure, so a reader "
    "checking the sheet against its own note would have found them disagreeing, with the note citing a "
    "figure that does not exist in the source. A correction that changes a value must also change every "
    "note that names it; the sheet and its note are one disclosure, not two."
)

NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed - the metric does not appear in FidBank UK Limited's four standalone Pillar 3 "
    "disclosures (FY2021-FY2024, published on the Bank's own Reporting Archive and cited in full on the "
    "capital sheets), nor in any of the 3 Annual Report filings reviewed (FY2023, FY2024, FY2025 - the only "
    "filings that exist at Companies House for this entity). The FY2023/FY2024 UK KM1 tables disclose CET1, "
    "Tier 1, total capital, RWA, capital ratios, leverage, LCR and NSFR, and carry no MREL row.\n\n"
    "CORRECTION, 18 September 2026 (KM1-032): this note previously opened 'no standalone Pillar 3 document "
    "exists for this entity'. That was false and had already been retracted elsewhere in this same build - "
    "the HD-064 primary-source correction on the capital sheets establishes that FidBank publishes "
    "entity-level Pillar 3 disclosures for FY2021-FY2024 - but the superseded sentence was left standing "
    "here, so one stale string kept asserting on this sheet what the rest of the workbook had disproved. "
    "The absence being recorded is MREL's, not the document's. See the Cash Flow Statement sheet's entity note."
)


STATEMENTS_SOURCES = (
    "Sources - FidBank UK Limited's own Statement of Financial Position / Statement of Comprehensive "
    "Income / Statement of Changes in Equity (Bank-only, GBP figures converted from the source's own USD "
    "figures - see FX methodology note in the Cash Flow Statement sheet's source citation):\n"
    f"FY2025, FY2024: Annual Report and Financial Statements for the year ended 31 December 2025, "
    f"pp.34-36 - {AR2025_URL}\n"
    f"FY2023, FY2022: Annual Report & Financial Statements for the year ended 31 December 2023, "
    f"pp.23-25 - {AR2023_URL}\n"
    "FY2021: only the equity roll-forward's opening balance is available (as the FY2023 Annual Report's "
    "own comparative 'Balance as at 1 January 2022' row) - no FY2021 balance sheet or income statement "
    "exists in any filing reviewed (see the Cash Flow Statement sheet's entity note for why).\n\n"
    "FX conversion: point-in-time (balance) figures at that year's period-end spot rate; flow (income "
    "statement) figures at that year's average rate - both entity-disclosed, same methodology as the Cash "
    "Flow Statement sheet.\n\n"
    "PRESENTATION CHANGE, FY2025: Short-term investments, Derivative Financial Assets/Liabilities, and "
    "Financial assets valued at Amortised Cost are new lines that first appear in FY2025 (nil/absent in "
    "prior years' own statements) - left blank for FY2024-FY2022 rather than assumed nil, except where "
    "the FY2025 Annual Report's own FY2024 comparative column explicitly shows '-' (shown as 0).\n\n"
    "MINOR DISCLOSED INCONSISTENCY, FY2024/FY2025 BOUNDARY: the FY2025 Annual Report's own equity "
    "statement states the 1 January 2025 opening balance as Retained losses $(29,740)k / Total equity "
    "$55,372k, which differs by $1k from the FY2024 Annual Report's own 31 December 2024 closing balance "
    "of $(29,741)k / $55,371k - a source-document rounding artifact. The equity sheet below uses each "
    "year's own closing balance as the following year's opening (continuous roll-forward) rather than "
    "FY2025's own restated opening figure, per project convention (reproduce as disclosed, not force-"
    "reconciled) - the $1k gap is absorbed into that year's FX translation effect row alongside the "
    "genuine FX translation effect, since both are immaterial at this entity's scale.\n\n"
    + ENTITY_NOTE
)

CAPITAL_AMOUNTS_NOTE = (
    "Sourced from Note 30(f) 'Capital adequacy' (Annual Report and Financial Statements, various years) - "
    "an analysis of the items comprising the Regulatory Capital base reported to the PRA. This table gives "
    "actual capital AMOUNTS (Total Tier 1 Capital / Total Regulatory Capital), not previously captured in "
    "this workbook, which had only the entity's separately-disclosed headline 'Capital Ratio' (Shareholders' "
    "Funds / RWA). Since Total Regulatory Capital exactly equals Total Tier 1 Capital in every year "
    "disclosed (no AT1 or Tier 2 capital line appears), CET1 Capital, Tier 1 Capital, and Total Capital are "
    "shown here as equal to that same figure - the capital base is entirely ordinary share capital and "
    "reserves less intangibles, with no other capital instruments. RWA itself is never disclosed in any "
    "filing reviewed (see CET1 Ratio/Tier 1 Ratio/Total RWAs/Leverage Ratio sheets), so these ratios cannot "
    "be derived from this table - only the Capital Ratio proxy (Total Capital Ratio sheet) is available. "
    "FY2021: no equivalent table exists (no capital-adequacy note for FY2021 in any filing reviewed)."
)

bw = BankWorkbook(bank_name="FidBank UK Limited", years=YEARS, year_label=YEAR_LABEL, header_color="AD7B7E")

# ---------------------------------------------------------------
# Balance Sheet / P&L / Statement of Changes in Equity data (all USD'000,
# from the Statement of Financial Position / Statement of Comprehensive
# Income / Statement of Changes in Equity, converted to £'000 as above).
# ---------------------------------------------------------------
bw.add_balance_sheet_sheet(
    title="FidBank UK Limited — Statement of Financial Position",
    subtitle="Bank-only basis, £'000 (conv. from USD). FY2021 not available - see source note below.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and cash equivalents", stock({"FY2025": 121756, "FY2024": 99914, "FY2023": 7127, "FY2022": 5431})),
        ("DATA", "Short-term investments", stock({"FY2025": 11074, "FY2024": 0})),
        ("DATA", "Loans and advances to banks", stock({"FY2025": 123763, "FY2024": 65801, "FY2023": 128017, "FY2022": 65437})),
        ("DATA", "Loans and advances to customers", stock({"FY2025": 146830, "FY2024": 55165, "FY2023": 8590, "FY2022": 3564})),
        ("DATA", "Derivative Financial Assets", stock({"FY2025": 423, "FY2024": 0})),
        ("DATA", "Financial assets measured at FVOCI", stock({"FY2025": 33826, "FY2024": 47544, "FY2023": 42025, "FY2022": 18123})),
        ("DATA", "Financial assets valued at Amortised Cost", stock({"FY2025": 8103, "FY2024": 0})),
        ("DATA", "Property and equipment", stock({"FY2025": 38, "FY2024": 59, "FY2023": 56, "FY2022": 44})),
        ("DATA", "Intangible assets", stock({"FY2025": 616, "FY2024": 366, "FY2023": 463, "FY2022": 507})),
        ("DATA", "Right-of-use-assets", stock({"FY2025": 919, "FY2024": 1300, "FY2023": 1673, "FY2022": 2052})),
        ("DATA", "Other assets", stock({"FY2025": 1708, "FY2024": 1226, "FY2023": 939, "FY2022": 850})),
        ("DATA", "Prepayments", stock({"FY2025": 1066, "FY2024": 945, "FY2023": 719, "FY2022": 625})),
        ("TOTAL", "Total Assets", stock({"FY2025": 450122, "FY2024": 272320, "FY2023": 189609, "FY2022": 96633})),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits by banks", stock({"FY2025": 194123, "FY2024": 106195, "FY2023": 78638, "FY2022": 19943})),
        ("DATA", "Customer accounts", stock({"FY2025": 197185, "FY2024": 107700, "FY2023": 50613, "FY2022": 38278})),
        ("DATA", "Derivative Financial Liabilities", stock({"FY2025": 138, "FY2024": 0})),
        ("DATA", "Lease liabilities", stock({"FY2025": 1238, "FY2024": 1605, "FY2023": 2001, "FY2022": 2065})),
        ("DATA", "Other liabilities", stock({"FY2025": 1008, "FY2024": 988, "FY2023": 717, "FY2022": 653})),
        ("DATA", "Accruals and deferred income", stock({"FY2025": 149, "FY2024": 461, "FY2023": 143, "FY2022": 175})),
        ("TOTAL", "Total Liabilities", stock({"FY2025": 393841, "FY2024": 216949, "FY2023": 132112, "FY2022": 61114})),
        ("SECTION", "Equity", {}),
        ("DATA", "Called up share capital", stock({"FY2025": 85090, "FY2024": 85090, "FY2023": 85090, "FY2022": 60090})),
        ("DATA", "FVOCI reserve", stock({"FY2025": 11, "FY2024": 22, "FY2023": -3, "FY2022": -4})),
        ("DATA", "Retained losses", stock({"FY2025": -28820, "FY2024": -29741, "FY2023": -27590, "FY2022": -24567})),
        ("TOTAL", "Total equity", stock({"FY2025": 56281, "FY2024": 55371, "FY2023": 57497, "FY2022": 35519})),
        ("TOTAL", "Total Liabilities and Equity", stock({"FY2025": 450122, "FY2024": 272320, "FY2023": 189609, "FY2022": 96633})),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=380,
    unit_suffix=" (£'000, conv. from USD)",
)

bw.add_income_statement_sheet(
    title="FidBank UK Limited — Statement of Comprehensive Income",
    subtitle="Bank-only basis, £'000 (conv. from USD). FY2021 not available - see source note below.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest income", flow({"FY2025": 19846, "FY2024": 14679, "FY2023": 8637, "FY2022": 3275})),
        ("DATA", "Interest expense", flow({"FY2025": -8133, "FY2024": -4847, "FY2023": -1413, "FY2022": -432})),
        ("TOTAL", "Net interest income", flow({"FY2025": 11713, "FY2024": 9832, "FY2023": 7224, "FY2022": 2843})),
        ("DATA", "Fees and commission income", flow({"FY2025": 2475, "FY2024": 2028, "FY2023": 1315, "FY2022": 1003})),
        ("DATA", "Dealing and exchange gains", flow({"FY2025": 2254, "FY2024": 275, "FY2023": 261, "FY2022": 125})),
        ("TOTAL", "Total income", flow({"FY2025": 16442, "FY2024": 12135, "FY2023": 8800, "FY2022": 3971})),
        ("DATA", "Administrative expenses", flow({"FY2025": -14688, "FY2024": -12750, "FY2023": -11165, "FY2022": -8495})),
        ("DATA", "Depreciation and amortisation", flow({"FY2025": -544, "FY2024": -537, "FY2023": -572, "FY2022": -563})),
        ("DATA", "Impairment reversal/(charge) on loans and advances", flow({"FY2025": 203, "FY2024": -640, "FY2023": 133, "FY2022": -144})),
        ("DATA", "Other operating expense", flow({"FY2025": -493, "FY2024": -359, "FY2023": -219, "FY2022": -151})),
        ("TOTAL", "Profit/(Loss) before tax", flow({"FY2025": 920, "FY2024": -2151, "FY2023": -3023, "FY2022": -5382})),
        ("DATA", "Tax charge", flow({"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0})),
        ("TOTAL", "Profit/(Loss) for the year after tax", flow({"FY2025": 920, "FY2024": -2151, "FY2023": -3023, "FY2022": -5382})),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Unrealised, net change in fair value of financial assets measured at FVOCI",
         flow({"FY2025": -10, "FY2024": 25, "FY2023": 1, "FY2022": 3})),
        ("TOTAL", "Total comprehensive income/(loss) for the year", flow({"FY2025": 910, "FY2024": -2126, "FY2023": -3022, "FY2022": -5379})),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=380,
    unit_suffix=" (£'000, conv. from USD)",
)

bw.add_equity_changes_sheet(
    title="FidBank UK Limited — Statement of Changes in Equity",
    subtitle="Bank-only basis, £'000 (conv. from USD), chronological. Each year's FX translation effect row "
              "absorbs the pure FX-conversion gap from converting opening/movements/closing at three "
              "different correct rates (prior-year spot / this year's average / this year's spot) - see "
              "Cash Flow Statement sheet's FX methodology note.",
    headers=["Share capital", "FVOCI reserve", "Retained losses", "Total equity"],
    rows=[
        ("DATA", "Balance as at 1 January 2022 (= FY2021 closing)", (44511.1, -5.2, -14211.1, 30294.8)),
        ("DATA", "Change in fair value of assets measured at FVOCI", (None, 2.4, None, 2.4)),
        ("TOTAL", "Loss for the year", (None, None, -4375.6, -4375.6)),
        ("DATA", "FX translation effect on equity, net", (5563.9, -0.5, -1885.8, 3677.6)),
        ("TOTAL", "Balance as at 31 December 2022", (50075.0, -3.3, -20472.5, 29599.2)),
        ("DATA", "Share capital issued", (20000.0, None, None, 20000.0)),
        ("DATA", "Change in fair value of assets measured at FVOCI", (None, 0.8, None, 0.8)),
        ("TOTAL", "Loss for the year", (None, None, -2418.4, -2418.4)),
        ("DATA", "FX translation effect on equity, net", (-3075.0, 0.1, 1166.5, -1908.4)),
        ("TOTAL", "Balance as at 31 December 2023", (67000.0, -2.4, -21724.4, 45273.2)),
        ("DATA", "Change in fair value of assets measured at FVOCI", (None, 19.5, None, 19.5)),
        ("TOTAL", "Loss for the year", (None, None, -1680.5, -1680.5)),
        ("DATA", "FX translation effect on equity, net", (1072.0, 0.5, -387.9, 684.6)),
        ("TOTAL", "Balance as at 31 December 2024", (68072.0, 17.6, -23792.8, 44296.8)),
        ("DATA", "Change in fair value of assets measured at FVOCI", (None, -7.6, None, -7.6)),
        ("TOTAL", "Profit for the year", (None, None, 697.0, 697.0)),
        ("DATA", "FX translation effect on equity, net", (-5042.4, -1.9, 1747.7, -3296.6)),
        ("TOTAL", "Balance as at 31 December 2025", (63029.6, 8.1, -21348.1, 41689.6)),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=52,
    source_height=380,
)

# ---------------------------------------------------------------
# FY2023/FY2022 GBP-translation plug (computed programmatically from the
# actual converted opening/net-change/closing figures, never hardcoded - see
# the Zenith Bank UK fix elsewhere in this project for why this matters).
# The FY2023 Annual Report's own USD statement ties exactly with no FX line
# (single currency, no conversion in the source) - the gap only appears once
# each of opening/flow/closing is converted at ITS OWN correct rate (prior-
# year spot / this year's average / this year's spot respectively), so a
# genuine translation-effect line is needed here even though the FY2023
# vintage's own presentation has no equivalent disclosed line (unlike
# FY2025/FY2024, which use a real disclosed "Exchange difference" figure).
# ---------------------------------------------------------------
_FY2023_FY2022_OPENING_USD = {"FY2023": 5431, "FY2022": 8999}
_FY2023_FY2022_NET_CHANGE_USD = {"FY2023": 1696, "FY2022": -3568}
_FY2023_FY2022_CLOSING_USD = {"FY2023": 7127, "FY2022": 5431}
_FY2023_FY2022_TRANSLATION_PLUG = {
    y: round(
        _FY2023_FY2022_CLOSING_USD[y] / FX_SPOT[y]
        - _FY2023_FY2022_OPENING_USD[y] / FX_SPOT[PREV_YEAR[y]]
        - _FY2023_FY2022_NET_CHANGE_USD[y] / FX_AVG[y],
        1,
    )
    for y in ("FY2023", "FY2022")
}

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    # --- FY2025/FY2024 basis (from the FY2025 Annual Report) ---
    ("DATA", "Profit/(loss) before tax", flow({"FY2025": 920, "FY2024": -2151, "FY2023": -3023, "FY2022": -5382})),
    ("DATA", "Depreciation and amortisation", flow({"FY2025": 164, "FY2024": 156, "FY2023": 193, "FY2022": 185})),
    ("DATA", "Amortisation of rights of use assets", flow({"FY2025": 380, "FY2024": 381, "FY2023": 379, "FY2022": 378})),
    ("DATA", "Adjustment to right of use asset - rent increase", flow({"FY2025": 0, "FY2024": -8})),
    ("DATA", "Amortisation of discounts received/premiums paid", flow({"FY2025": -2245, "FY2024": -2080, "FY2023": -1648, "FY2022": -245})),
    ("DATA", "Net exchange differences", flow({"FY2025": -335, "FY2024": 150})),
    ("DATA", "Profit on sale of amortised cost bonds", flow({"FY2025": -1502, "FY2024": 0})),
    # --- FY2023/FY2022 basis (from the FY2023 Annual Report) ---
    ("DATA", "Loss on disposal of tangible/intangible assets", flow({"FY2025": 0, "FY2024": 0, "FY2023": 1, "FY2022": 1})),
    ("DATA", "Bad debt recovered", flow({"FY2023": 0, "FY2022": 23})),
    ("DATA", "Exchange differences - finance lease liability", flow({"FY2023": 120, "FY2022": -292})),
    ("DATA", "Interest on finance lease liability", flow({"FY2025": 121, "FY2024": 192, "FY2023": 90, "FY2022": 102})),
    ("DATA", "Impairment of loans and advances", flow({"FY2025": 71, "FY2024": 445, "FY2023": -133, "FY2022": 144})),
    ("TOTAL", "Non-cash and other adjustments (subtotal; unlabeled in source)",
     flow({"FY2025": -2426, "FY2024": -2915, "FY2023": -4021, "FY2022": -5086})),
    ("DATA", "Change in loans and advances to banks", flow({"FY2025": -57963, "FY2024": -46794, "FY2023": -62422, "FY2022": 45036})),
    ("DATA", "Change in loans and advances to customers", flow({"FY2025": -91665, "FY2024": -46779, "FY2023": -5052, "FY2022": 12591})),
    ("DATA", "Change in short-term investments", flow({"FY2025": -11074, "FY2024": 0})),
    ("DATA", "Change in other assets", flow({"FY2025": -481, "FY2024": -287, "FY2023": -89, "FY2022": -12})),
    ("DATA", "Change in prepayments", flow({"FY2025": -121, "FY2024": -227, "FY2023": -92, "FY2022": -27})),
    ("DATA", "Change in deposits by banks", flow({"FY2025": 87927, "FY2024": 27557, "FY2023": 58695, "FY2022": -49159})),
    ("DATA", "Change in customer accounts", flow({"FY2025": 89485, "FY2024": 57086, "FY2023": 12335, "FY2022": -19026})),
    ("DATA", "Change in derivatives", flow({"FY2025": -285, "FY2024": 0})),
    ("DATA", "Change in other liabilities", flow({"FY2025": 20, "FY2024": 271, "FY2023": 64, "FY2022": 12})),
    ("DATA", "Change in accruals and deferred income", flow({"FY2025": -312, "FY2024": 318, "FY2023": -32, "FY2022": -47})),
    ("TOTAL", "Cash (used in)/from operations", flow({"FY2025": 13105, "FY2024": -11770, "FY2023": -614, "FY2022": -15718})),
    ("DATA", "Acquisition of financial assets", flow({"FY2025": -117331, "FY2024": -72386, "FY2023": -78132, "FY2022": -40469})),
    ("DATA", "Disposal of financial assets", flow({"FY2025": 126614, "FY2024": 68941, "FY2023": 55879, "FY2022": 52877})),
    ("DATA", "Income tax received", flow({"FY2023": 0, "FY2022": 253})),
    ("TOTAL", "Net cash (used in)/from operating activities", flow({"FY2025": 22388, "FY2024": -15215, "FY2023": -22867, "FY2022": -3057})),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of tangible and intangible assets", flow({"FY2025": -394, "FY2024": -61, "FY2023": -163, "FY2022": -38})),
    ("TOTAL", "Net cash flow used in investing activities", flow({"FY2025": -394, "FY2024": -61, "FY2023": -163, "FY2022": -38})),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Increase in share capital", flow({"FY2025": 0, "FY2024": 0, "FY2023": 25000, "FY2022": 0})),
    ("DATA", "Leasehold property repayments", flow({"FY2025": -606, "FY2024": -564, "FY2023": -274, "FY2022": -473})),
    ("TOTAL", "Net cash generated from/(used in) financing activities", flow({"FY2025": -606, "FY2024": -564, "FY2023": 24726, "FY2022": -473})),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", flow({"FY2025": 21388, "FY2024": -15840, "FY2023": 1696, "FY2022": -3568})),
    ("DATA", "Cash and cash equivalents at the beginning of the year",
     opening_cash({"FY2025": 99914, "FY2024": 115901, "FY2023": 5431, "FY2022": 8999})),
    ("DATA", "Exchange difference in respect of cash and cash equivalents / effect of GBP-USD translation",
     {**flow({"FY2025": 454, "FY2024": -147}), **_FY2023_FY2022_TRANSLATION_PLUG}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", stock({"FY2025": 121756, "FY2024": 99914, "FY2023": 7127, "FY2022": 5431})),
]

bw.add_cash_flow_sheet(
    title="FidBank UK Limited — Statement of Cash Flows",
    subtitle="Bank-only basis, £'000 (conv. from USD). FY2021 not available - see source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Asset Quality sheet - Loans and advances to customers, by product
# (Note 19's own breakdown), gross/impairment/net, plus the Stage 1&2 vs
# Stage 3 impairment split disclosed narratively (not in table form) below
# each year's own Note 19.
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - FidBank UK Limited's own Note 19 'Loans and advances to customers' (gross amount / "
    "impairment allowance / net amount, by product), each Annual Report's own basis:\n"
    f"FY2025, FY2024: Annual Report and Financial Statements for the year ended 31 December 2025, p.53 - "
    f"{AR2025_URL}\n"
    f"FY2023, FY2022: Annual Report & Financial Statements for the year ended 31 December 2023, p.44 - "
    f"{AR2023_URL}\n"
    "FY2021: not available - Note 19 gives no FY2021 comparative in either filing reviewed.\n\n"
    "The Stage 1&2 vs Stage 3 impairment split is disclosed only as narrative text below each year's Note "
    "19 table (not a further breakdown table), e.g. FY2025: 'Of the $0.33m impairment provision, $0.32m "
    "represents the Stage 1 and stage 2 provisions under IFRS 9, while Stage 3 provisions amounted to "
    "$0.01m' - reproduced here as disclosed. 'Sovereign Loans' only appears as its own product line from "
    "FY2024 onward (shown as '-' for FY2024, absent as a line entirely for FY2023/FY2022 - left blank, not "
    "assumed nil, per project convention). Coverage ratio = impairment allowance / gross amount, computed "
    "from the disclosed £'000 figures (converted from USD at each year's period-end spot rate - see Cash "
    "Flow Statement sheet's FX methodology note).\n\n"
    + ENTITY_NOTE
)

bw.add_asset_quality_sheet(
    title="FidBank UK Limited — Asset Quality (Loans and advances to customers)",
    subtitle="Bank-only basis, £'000 (conv. from USD). By product, per Note 19. FY2021 not available.",
    rows=[
        ("SECTION", "Gross amount by product", {}),
        ("DATA", "Commercial loans & advances", stock({"FY2025": 97206, "FY2024": 35991, "FY2023": 8488, "FY2022": 2934})),
        ("DATA", "Personal loans & advances", stock({"FY2025": 295, "FY2024": 263, "FY2023": 132, "FY2022": 52})),
        ("DATA", "Syndicated loans", stock({"FY2025": 24259, "FY2024": 19145, "FY2023": 0, "FY2022": 582})),
        ("DATA", "Sovereign loans", stock({"FY2025": 25397, "FY2024": 0})),
        ("TOTAL", "Gross amount, total", stock({"FY2025": 147157, "FY2024": 55399, "FY2023": 8620, "FY2022": 3568})),
        ("SECTION", "Impairment and net amount", {}),
        ("DATA", "Impairment allowance, total", stock({"FY2025": -327, "FY2024": -234, "FY2023": -30, "FY2022": -4})),
        ("TOTAL", "Net amount, total", stock({"FY2025": 146830, "FY2024": 55165, "FY2023": 8590, "FY2022": 3564})),
        ("DATA", "  of which: Stage 1 and Stage 2 impairment allowance", stock({"FY2025": -320, "FY2024": -180, "FY2023": -29.4, "FY2022": -4.1})),
        ("DATA", "  of which: Stage 3 impairment allowance", stock({"FY2025": -10, "FY2024": -50, "FY2023": 0, "FY2022": 0})),
        ("SECTION", "Derived ratio", {}),
        ("DATA", "Impairment coverage ratio (allowance ÷ gross amount)",
         {"FY2025": "0.22%", "FY2024": "0.42%", "FY2023": "0.35%", "FY2022": "0.11%"}),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=48, source_height=220)


CAPITAL_RATIO = {"FY2025": "21.99%", "FY2024": "43%", "FY2023": "98%", "FY2022": "54%", "FY2021": "40%"}
LCR = {"FY2025": "178%", "FY2024": "243%"}
CAPITAL_AMOUNT = stock({"FY2025": 55665, "FY2024": 55029, "FY2023": 57034, "FY2022": 35045, "FY2021": 40718})
REGULATORY_RWA = stock({"FY2024": 133310, "FY2023": 60485, "FY2022": 65571, "FY2021": 102825})
CET1_RATIO = {"FY2024": "41.28%", "FY2023": "94.29%", "FY2022": "53.45%", "FY2021": "39.60%"}
LEVERAGE_RATIO = {"FY2024": "19.45%", "FY2023": "29.83%", "FY2022": "35.78%"}
P3_LCR = {"FY2024": "243.39%", "FY2023": "233.04%", "FY2022": "379.92%"}
NSFR = {"FY2024": "211.78%", "FY2023": "335.67%", "FY2022": "363.79%"}

# ---------------------------------------------------------------
# FY2025 GAP-FILL, 19 September 2026.
# Seven FY2025 sheet-years here (CET1 Ratio, Tier 1 Ratio, Total RWAs, RWA
# Breakdown, Leverage Ratio, NSFR and KM1) were BLANK. The finding was already
# established and written up at length in p3_sources() below - but a note is
# invisible to the corpus census, which cannot tell an established negative
# from a cell nobody has looked at. The finding now goes IN the year column.
# Nothing below changes a figure; only empty cells gain text.
#
# RE-VERIFIED INDEPENDENTLY THIS SESSION, not inherited from the earlier note:
#  1. NO FY2025 PILLAR 3 EXISTS. FidBank's own site carries no disclosures
#     index at all - regulatory-information.html and media-page.html were both
#     fetched as HTML on 19/09/2026 and link no PDF of any kind - so the Pillar
#     3 files are unlinked uploads under /assets/Uploads/NewFolder/. Probing
#     that path: FidBank-UK-Pillar-3-Disclosure-2025.pdf returns HTTP 404 and
#     FBUK-Pillar-3-Disclosure-2025.pdf returns HTTP 404, while the FY2024 file
#     at the identical path returns HTTP 200 with Content-Type application/pdf -
#     a positive control on the same host in the same sweep, so the 404s are
#     absence and not blocking. A Wayback CDX sweep of the whole fidbank.co.uk
#     domain lists three Pillar 3 PDFs ever archived (2022, 2023, 2024), the
#     newest captured 17/01/2026.
#  2. THE FY2025 ANNUAL REPORT DOES NOT SUPPLY THESE FIGURES. The filing
#     (Companies House, filed 25/07/2026) is an image-only scan - Creator
#     'go-tiff2pdf', 69 pages, pdftotext returns 69 bytes and ZERO hits for
#     ' the ', so a text search of it proves nothing. It was re-rasterised at
#     300 dpi and OCR'd this session; the OCR returns 1,276 hits for ' the ',
#     which is the richness control that makes the following absences the
#     document's rather than the instrument's:
#       - No RWA AMOUNT anywhere. 'risk weighted' appears only in the
#         Performance Metrics formula caption, in the narrative sentence
#         "FBUK's capital over risk weighted assets was 21.99% (2024: 43%)",
#         and in note 30's standard description of how RWAs are determined.
#       - No leverage ratio figure. 'Leverage' appears twice, once in a risk-
#         governance sentence ("The Capital Adequacy Ratio (CAR) and Leverage
#         Ratio is tracked daily") and once in an unrelated business sentence.
#       - No NSFR at all: 'NSFR' and 'stable funding' both return zero hits.
#       - No CET1 line. Note 30's capital table (printed p.64) runs Share
#         Capital 85,090 / P&L Reserve (28,820) / FVOCI 11 / Less Intangibles
#         (616) / Total Tier 1 Capital 55,665 / Total Regulatory Capital 55,665,
#         with a 2024 comparative column - capital AMOUNTS only, no denominator.
#     Nothing here is back-solved: in particular Total RWAs is NOT computed as
#     capital / 21.99%, for the reasons already in CAPITAL_RATIO_NOTE.
#  3. NOT DUE YET EITHER. FidBank publishes its Pillar 3 roughly 12-13 months
#     after year-end (the FY2024 edition was first archived January 2026), so
#     an FY2025 edition would be expected around January 2027 - after this
#     build date. This is a document that does not exist yet, not one that
#     could not be reached.
# ---------------------------------------------------------------
FY2025_NO_P3 = "Not published - no FY2025 Pillar 3 edition; no RWA denominator in AR2025"
FY2025_NO_RWA = "Not disclosed - AR2025 prints no RWA amount; no FY2025 Pillar 3 edition"
FY2025_NO_LEVERAGE = "Not disclosed - no leverage ratio in AR2025; no FY2025 Pillar 3 edition"
FY2025_NO_NSFR = "Not disclosed - 'stable funding' absent from AR2025; no FY2025 Pillar 3 edition"
FY2025_GAPFILL_NOTE = (
    "\n\nFY2025 IS A RECORDED ABSENCE, NOT AN UNCHECKED CELL (written into the column 2026-09-19). "
    "Three things were re-verified this session rather than inherited. (1) No FY2025 Pillar 3 edition "
    "exists: FidBank's site carries no disclosures index at all (regulatory-information.html and "
    "media-page.html both fetched as HTML on 19/09/2026, neither links any PDF), its Pillar 3 files are "
    "unlinked uploads, and two filename permutations for a 2025 edition under that upload path return "
    "HTTP 404 while the FY2024 file at the identical path returns HTTP 200 with Content-Type "
    "application/pdf - a positive control in the same sweep. A Wayback CDX sweep of the whole "
    "fidbank.co.uk domain lists three Pillar 3 PDFs ever, the newest being FY2024 (archived 17/01/2026). "
    "(2) The FY2025 Annual Report does not supply the figure. That filing is an image-only scan (Creator "
    "'go-tiff2pdf'; pdftotext returns 69 bytes and ZERO hits for ' the ' across 69 pages, so a text search "
    "of it indicts the instrument, not the Bank). It was re-rasterised at 300 dpi and OCR'd here, giving "
    "1,276 hits for ' the ' as the richness control; on that OCR there is no RWA amount, no leverage "
    "ratio, no NSFR mention of any kind, and no CET1 line - note 30's capital table (printed p.64) gives "
    "capital AMOUNTS only (Total Tier 1 Capital = Total Regulatory Capital = US$55,665k, 2024: 55,005). "
    "(3) It is not due yet: FidBank publishes its Pillar 3 roughly 12-13 months after year-end, so an "
    "FY2025 edition is expected around January 2027. Nothing is back-solved - Total RWAs is specifically "
    "NOT computed as capital divided by the 21.99% ratio, for the reasons in the Total Capital Ratio "
    "sheet's note.")

# ---------------------------------------------------------------
# KM1 Key Metrics - the Bank's own UK KM1 template, reproduced whole
# ---------------------------------------------------------------
KM1_NOTE = (
    "\n\nKM1 KEY METRICS SHEET - WHAT THIS IS AND HOW IT WAS BUILT\n"
    "This is FidBank UK's own UK KM1 key-metrics template, with the Bank's own row numbers, labels and "
    "precision. The Bank prints its ratio rows as bare numbers under headings that state they are "
    "percentages; they are reproduced as printed, without a percent sign added.\n"
    "\n"
    "THE CURRENCY CAPTION IS DEFECTIVE IN THE SOURCE AND IS RECORDED, NOT SILENTLY FIXED. The FY2023 "
    "edition heads the two columns of this table \"31/12/2023  £000's\" and \"31/12/2022  £000's\". The "
    "FY2024 edition heads the identical digits for 31/12/2023 - CET1 capital 57,034, total risk-weighted "
    "exposure amount 60,485, and every other value in the column - as \"$000's\". The same figures cannot "
    "be simultaneously sterling and dollars, so one caption is simply wrong. THE AMOUNTS ARE US DOLLARS, on "
    "three independent grounds: (a) the digits are byte-identical across the two editions, which could not "
    "happen if the presentation currency had changed between them; (b) every other table in both editions "
    "is captioned (USD'000); and (c) the rest of this workbook treats these as dollars and converts them to "
    "sterling. The rows below are therefore labelled $'000 and NO DIGIT HAS BEEN ALTERED - only the "
    "mislabelled caption is set aside, and it is set aside here in writing rather than quietly.\n"
    "\n"
    "WHY THE AMOUNT ROWS ARE NOT CROSS-CHECKED against this workbook's metric sheets: this sheet is left in "
    "the Bank's own reporting currency (US dollars) while the metric sheets are converted to sterling, so "
    "a cell-for-cell comparison of amounts would compare two different currencies. The ratio rows are "
    "currency-free and ARE cross-checked.\n"
    "\n"
    "FY2022 IS A COMPARATIVE COLUMN, NOT AN OWN EDITION. The FY2022 Pillar 3 edition exists but contains no "
    "key-metrics table of any kind - confirmed by reading its full text layer (about 76,000 characters, so "
    "not an extraction failure) and finding zero occurrences of 'Available own funds', 'Total SREP own "
    "funds', 'Additional CET1 SREP', 'risk-weighted exposure amount', 'Combined buffer requirement', 'Net "
    "Stable Funding', 'Key Metrics' or 'Leverage ratio'. The FY2022 column here is therefore the FY2023 "
    "edition's own 31/12/2022 comparative column, reproduced in that edition's row structure and flagged so "
    "it is never mistaken for a FY2022-edition disclosure.\n"
    "\n"
    "ROW 18 DIVERGES BETWEEN EDITIONS AND THE OWN-EDITION FIGURE IS THE ONE SHOWN. For FY2023, total "
    "available stable funding is printed as 96,213 in the FY2023 edition and as 96,123 in the FY2024 "
    "edition's comparative column - a transposed pair of digits somewhere, but the source does not say "
    "which edition is wrong and it is not this workbook's place to decide. 96,213 is carried here because "
    "each year comes from its own edition. The divergence is recorded rather than reconciled.\n"
    "\n"
    "ROW 12 IS PRINTED WITH NO VALUES in both editions - the row exists in the table and its cells are "
    "empty. It is reproduced as a present-but-blank row, not dropped and not filled with a zero.\n"
    "\n"
    "ROW 10 PRINTS 'N.A.' (the glyph in both the FY2024 and FY2023 editions, in the FY2024, FY2023 and "
    "FY2022 columns) and the cells carry the plain ASCII '-' under KM1 transcription rule 2 (a printed "
    "dash/'n/a' becomes '-', the glyph is recorded here). It is the Bank's own statement that the G-SII "
    "buffer does not apply to it; it is not a blank and it is certainly not a zero. (Changed 2026-09-19, "
    "GA-020: the cells previously carried the literal text 'N.A.'.)\n"
    "\n"
    "THE TOP ROW IS NOT PART OF THE TEMPLATE (added 2026-09-19). It is bracketed, unnumbered and labelled "
    "'[Edition status for this year - not a KM1 template row]'. It carries no figure and is not one of the "
    "Bank's rows; it exists only so the FY2025 column states in the grid what this note states in prose. "
    "The Bank's own rows below it are untouched - same order, same numbers, same labels, same precision.\n"
    "\n"
    "FY2025 AND FY2021 CARRY NO TEMPLATE FIGURES. No FY2025 Pillar 3 edition has been published (the "
    "FY2025 column's top row says so; see also the source note). The FY2021 edition "
    "predates the Bank's adoption of the template and carries no key-metrics table, and no later edition "
    "reaches back to 2021 with a comparative column, so there is nothing to transcribe and nothing is "
    "inferred from the CET1 ratio and RWA figures that the metric sheets carry for that year.\n"
    "\n"
    "ENTITY BASIS. The Bank states in its own Pillar 3 that it is a single entity and that no prudential "
    "consolidation is performed, so these are the UK entity's own figures on the only basis it reports."
)

km1_rows = [
    # Gap-fill 2026-09-19. STATEMENT ROW, NOT A TEMPLATE ROW, placed above the
    # template so the Bank's own KM1 sequence, row numbers, labels and
    # precision are left exactly as printed. It exists because the FY2025
    # column was wholly empty, which the corpus census cannot tell apart from
    # an unexamined gap; the reason was already in the note below but nowhere a
    # reader would meet it in the grid itself.
    ("DATA", "[Edition status for this year - not a KM1 template row]",
     {"FY2025": "Not published - no FY2025 Pillar 3 edition as at 19/09/2026"}),
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital ($'000)",
     {"FY2024": 55029, "FY2023": 57034, "FY2022": 35045}),
    ("DATA", "2  Tier 1 capital ($'000)",
     {"FY2024": 55029, "FY2023": 57034, "FY2022": 35045}),
    ("DATA", "3  Total capital ($'000)",
     {"FY2024": 55029, "FY2023": 57034, "FY2022": 35045}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4  Total risk-weighted exposure amount ($'000)",
     {"FY2024": 133310, "FY2023": 60485, "FY2022": 65571}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)", {"FY2024": 41.28, "FY2023": 94.29, "FY2022": 53.45}),
    ("DATA", "6  Tier 1 ratio (%)", {"FY2024": 41.28, "FY2023": 94.29, "FY2022": 53.45}),
    ("DATA", "7  Total capital ratio (%)", {"FY2024": 41.28, "FY2023": 94.29, "FY2022": 53.45}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirements (%)", {"FY2024": 4.83, "FY2023": 4.41, "FY2022": 4.41}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8  Capital conservation buffer (%)", {"FY2024": 2.5, "FY2023": 2.5, "FY2022": 2.5}),
    ("DATA", "9  Institution specific countercyclical capital buffer (%)",
     {"FY2024": 0.87, "FY2023": 0.44, "FY2022": 0.12}),
    ("DATA", "10  Global Systemically Important Institution buffer (%)",
     {"FY2024": "-", "FY2023": "-", "FY2022": "-"}),
    ("DATA", "11  Combined buffer requirement (%)", {"FY2024": 3.37, "FY2023": 2.94, "FY2022": 2.62}),
    ("DATA", "UK 11a  Overall capital requirements (%)", {"FY2024": 16.20, "FY2023": 15.35, "FY2022": 15.03}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%) [printed with no values]", {}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13  Leverage ratio total exposure measure ($'000)",
     {"FY2024": 282725, "FY2023": 191191, "FY2022": 99083}),
    ("DATA", "14  Leverage ratio (%)", {"FY2024": 19.45, "FY2023": 29.83, "FY2022": 35.78}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (Weighted value -average) ($'000)",
     {"FY2024": 47549, "FY2023": 42026, "FY2022": 18123}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value ($'000)",
     {"FY2024": 78145, "FY2023": 72135, "FY2022": 19081}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value ($'000)",
     {"FY2024": 58609, "FY2023": 54101, "FY2022": 14311}),
    ("DATA", "16  Total net cash outflows (adjusted value) ($'000)",
     {"FY2024": 19536, "FY2023": 18034, "FY2022": 4770}),
    ("DATA", "17  Liquidity coverage ratio (%)", {"FY2024": 243.39, "FY2023": 233.04, "FY2022": 379.92}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18  Total available stable funding ($'000)",
     {"FY2024": 139028, "FY2023": 96213, "FY2022": 69583}),
    ("DATA", "19  Total required stable funding ($'000)",
     {"FY2024": 65648, "FY2023": 28663, "FY2022": 19127}),
    ("DATA", "20  NSFR ratio (%)", {"FY2024": 211.78, "FY2023": 335.67, "FY2022": 363.79}),
]

bw.add_km1_sheet(
    title="FidBank UK Limited — KM1 Key Metrics",
    subtitle="The Bank's own UK KM1 key-metrics template (single entity - no prudential consolidation is "
             "performed), reproduced in its own row order, row numbers, labels and precision. Amounts in "
             "US$'000 as reported; ratios as printed, without a percent sign, which is how the Bank prints "
             "them. FY2024 and FY2023 come from their own editions; FY2022 is the FY2023 edition's "
             "comparative column (the FY2022 edition carries no key-metrics table at all). The FY2023 "
             "edition mislabels this table's currency as £000's - see the note.",
    rows=km1_rows,
    sources_text=p3_sources(
        "KM1 key-metrics table, section 1.4 'Key Metrics', by edition (printed folios, not PDF sheet "
        "indices): FY2024 = 2024 Pillar 3 Disclosures, folio 'Page 9 of 32' ($000's). FY2023 = 2023 Pillar "
        "3 Disclosures, folio 'Page 9 of 31' (captioned £000's, which is a source error - see the note). "
        "FY2022 = the 31/12/2022 comparative column of that same 2023 edition. LATEST-EDITION CHECK "
        "(2026-09-17): the Bank's regulatory-information page was fetched live; the newest Pillar 3 edition "
        "published is the 2024 one, so FY2025 is blank because no edition exists, not because none was "
        "sought."
    ) + KM1_NOTE,
    first_col_width=78,
    source_height=860,
)

metric("CET1 Capital", "£'000 (conv. from USD)", [("CET1 Capital (= Total Regulatory Capital)", CAPITAL_AMOUNT)],
       p3_sources(CAPITAL_AMOUNTS_NOTE), note=CAPITAL_AMOUNTS_NOTE)

metric("CET1 Ratio", "% of RWA", [("CET1 ratio", dict(CET1_RATIO, FY2025=FY2025_NO_P3))], p3_sources(),
       note="FY2024-FY2022 are FidBank UK's own UK KM1 disclosures. FY2021 is calculated from its own disclosed CET1 capital and Pillar 1 RWA components; the Annual Report's 40% headline is rounded."
       + FY2025_GAPFILL_NOTE)

metric("Tier 1 Capital", "£'000 (conv. from USD)", [("Total Tier 1 Capital", CAPITAL_AMOUNT)],
       p3_sources(CAPITAL_AMOUNTS_NOTE), note=CAPITAL_AMOUNTS_NOTE)

metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", dict(CET1_RATIO, FY2025=FY2025_NO_P3))], p3_sources(),
       note="FidBank has no AT1 or Tier 2 in the disclosed periods, so Tier 1 equals CET1."
       + FY2025_GAPFILL_NOTE)

metric("Total Capital", "£'000 (conv. from USD)", [("Total Regulatory Capital", CAPITAL_AMOUNT)],
       p3_sources(CAPITAL_AMOUNTS_NOTE), note=CAPITAL_AMOUNTS_NOTE)

metric("Total Capital Ratio", "%", [("Total capital ratio", {"FY2024": "41.28%", "FY2023": "94.29%", "FY2022": "53.45%", "FY2021": "39.60%"}),
                                         ("Annual Report capital-ratio proxy (Shareholders' Funds ÷ RWA)", CAPITAL_RATIO)],
       p3_sources(), note="The first row is the standard regulatory ratio from FidBank UK's own Pillar 3 disclosures. "
       "The Annual Report's different accounting-equity proxy is retained separately for comparability - the two bases "
       "demonstrably differ (FY2024: 41.28% on the KM1 basis vs 43% on the AR proxy), which is why no FY2025 KM1-basis "
       "ratio is inferred from the AR. "
       "FY2025 PROXY VALUE CORRECTED AND A SOURCE INCONSISTENCY FLAGGED (verified 15 September 2026): this cell "
       "previously read 21.46%, a figure that appears NOWHERE in the FY2025 Annual Report and was a transcription "
       "error. The Annual Report itself states the FY2025 capital ratio TWO DIFFERENT WAYS: the 'Key Performance "
       "Indicators' section (p.12) gives 21.99% twice - 'FBUK's capital over risk weighted assets was 21.99% (2024: "
       "43%)' and 'decreased from 43% in 2024 to 21.99% in 2025' - while the 'Performance Metrics' infographic (p.7) "
       "gives 21.64% for the same measure and year. Both readings were confirmed visually at 450 dpi, not by OCR "
       "alone. This workbook uses the 21.99% figure because it appears in the formal KPI section of the Strategic "
       "Report, is stated twice, and is accompanied by a narrative explanation of the movement, whereas p.7 is a "
       "summary infographic; the 21.64% alternative is recorded here rather than discarded, and the inconsistency is "
       "the Bank's own, not this workbook's.")

metric("Total RWAs", "£'000 (conv. from USD)",
       [("Total risk-weighted exposure amount", dict(REGULATORY_RWA, FY2025=FY2025_NO_RWA))], p3_sources(),
       note="FY2024-FY2022 are directly disclosed in UK KM1. FY2021 is the sum of the source's own Pillar 1 capital requirements divided by 8%; it reconciles to the Annual Report's rounded 40% capital proxy."
       + FY2025_GAPFILL_NOTE)

bw.add_rwa_breakdown_sheet(
    title="FidBank UK Limited — RWA Breakdown",
    subtitle="FidBank UK's own Pillar 3 disclosures; £'000 converted from USD.",
    rows=[
        # Gap-fill 2026-09-19: the FY2025 column held no cell at all, so the
        # census scored it as an untouched gap. Statement row, not a risk
        # category - nothing is computed and no total is affected.
        ("DATA", "[No RWA breakdown published for this year - see note below]",
         {"FY2025": FY2025_NO_RWA}),
        ("DATA", "Credit risk", stock({"FY2023": 46743, "FY2022": 47963, "FY2021": 79725})),
        ("DATA", "Operational risk", stock({"FY2023": 10450, "FY2022": 15525, "FY2021": 21300})),
        ("DATA", "Market risk", stock({"FY2023": 3292, "FY2022": 2075, "FY2021": 1800})),
        ("TOTAL", "Total", REGULATORY_RWA),
    ],
    sources_text=p3_sources("FY2023 components are direct from its own Pillar 3 Table 2. FY2022/FY2021 components are each disclosed Pillar 1 capital requirement ÷ 8%; immaterial rounding differences versus the separately disclosed aggregate are retained in the Total row." + FY2025_GAPFILL_NOTE),
    unit_suffix=" (£'000, conv. from USD)",
)

metric("Leverage Ratio", "%", [("Leverage ratio", dict(LEVERAGE_RATIO, FY2025=FY2025_NO_LEVERAGE))], p3_sources(),
       note="Directly disclosed in FidBank UK's FY2024, FY2023 and FY2022 UK KM1 tables. FY2021 remains blank: its older Pillar 3 disclosure does not provide a leverage ratio."
       + FY2025_GAPFILL_NOTE)

metric("LCR", "%", [("Liquidity Coverage Ratio", {**LCR, **P3_LCR})], p3_sources(),
       note="FY2024-FY2022 values are directly disclosed in FidBank UK's UK KM1 tables; FY2025 remains sourced from its Annual Report. FY2021's older disclosure has no LCR value.")

metric("NSFR", "%", [("Net stable funding ratio", dict(NSFR, FY2025=FY2025_NO_NSFR))], p3_sources(),
       note="Directly disclosed in FidBank UK's FY2024, FY2023 and FY2022 UK KM1 tables. FY2021 remains blank because no entity-level value was located in that year's older disclosure."
       + FY2025_GAPFILL_NOTE)
# GA-020 (2026-09-19): the four Pillar 3 editions were re-downloaded from fidbank.co.uk (%PDF,
# text-native): 0 hits for "MREL", "KM2", "eligible liabilities" and "loss-absorbing" in each,
# against 110-140 "capital" hits. FY2025's Pillar 3 is not out yet (see p3_sources: the Bank
# publishes ~12-13 months after year-end, so ~January 2027).
_FID_MREL = {y: (f"Not published – FidBank UK {y} Pillar 3 disclosure has no MREL figure or KM2 (text "
                 "probe 0 hits, 2026-09-19)") for y in ("FY2024", "FY2023", "FY2022", "FY2021")}
_FID_MREL["FY2025"] = ("Not published yet – FY2025 Pillar 3 expected ~Jan 2027 (FY2024 edition appeared Jan "
                       "2026); FY2025 Annual Report has no MREL figure")
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": NOT_DISCLOSED_NOTE},
                                   statements={"MREL Ratio": _FID_MREL})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total Assets", stock({"FY2025": 450122, "FY2024": 272320, "FY2023": 189609, "FY2022": 96633})),
        ("Loans and advances to customers", stock({"FY2025": 146830, "FY2024": 55165, "FY2023": 8590, "FY2022": 3564})),
        ("Customer accounts", stock({"FY2025": 197185, "FY2024": 107700, "FY2023": 50613, "FY2022": 38278})),
        ("Total equity", stock({"FY2025": 56281, "FY2024": 55371, "FY2023": 57497, "FY2022": 35519})),
    ],
    balance_sheet_unit="£'000 (conv. from USD)",
    income_statement_totals=[
        ("Total income", flow({"FY2025": 16442, "FY2024": 12135, "FY2023": 8800, "FY2022": 3971})),
        ("Administrative expenses", flow({"FY2025": -14688, "FY2024": -12750, "FY2023": -11165, "FY2022": -8495})),
        ("Profit/(Loss) for the year after tax", flow({"FY2025": 920, "FY2024": -2151, "FY2023": -3023, "FY2022": -5382})),
    ],
    income_statement_unit="£'000 (conv. from USD)",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 44296.8, "FY2024": 45273.2, "FY2023": 29599.2, "FY2022": 30294.8}),
        ("Total comprehensive income/(loss) for the year",
         {"FY2025": 689.4, "FY2024": -1661.0, "FY2023": -2417.6, "FY2022": -4373.2}),
        ("Other equity movements, net",
         {"FY2025": -3296.6, "FY2024": 684.6, "FY2023": 18091.6, "FY2022": 3677.6}),
        ("Closing equity", stock({"FY2025": 56281, "FY2024": 55371, "FY2023": 57497, "FY2022": 35519})),
    ],
    equity_changes_unit="£'000 (conv. from USD)",
    cash_flow_totals=[
        ("Net cash (used in)/from operating activities", flow({"FY2025": 22388, "FY2024": -15215, "FY2023": -22867, "FY2022": -3057})),
        ("Net cash flow used in investing activities", flow({"FY2025": -394, "FY2024": -61, "FY2023": -163, "FY2022": -38})),
        ("Net cash generated from/(used in) financing activities", flow({"FY2025": -606, "FY2024": -564, "FY2023": 24726, "FY2022": -473})),
        ("Cash and cash equivalents at end of year", stock({"FY2025": 121756, "FY2024": 99914, "FY2023": 7127, "FY2022": 5431})),
    ],
    cash_flow_unit="£'000 (conv. from USD)",
    ratios=[
        ("Total Capital Ratio", CAPITAL_RATIO),
        ("LCR", LCR),
    ],
    note="FY2021 cash flow/balance sheet/P&L not available (see Cash Flow Statement sheet's source note) - "
         "only FY2021's own closing equity is known (as FY2022's disclosed opening balance), shown on the "
         "Statement of Changes in Equity sheet. Pillar 3 coverage is thin - a headline Capital Ratio (all 5 "
         "years), actual Tier 1/CET1/Total Capital AMOUNTS (FY2025-FY2022, from the capital adequacy note - "
         "a finding not previously captured in this workbook), and LCR (FY2025/FY2024 only) are disclosed; "
         "RWA itself and every ratio derived from it remain Not publicly disclosed. Figures are duplicated "
         "from the detail sheets for at-a-glance trend viewing; see each sheet's own source citation.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/FIDBANK UK FINANCIALS.xlsx")
