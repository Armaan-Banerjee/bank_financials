import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}

# ---------------------------------------------------------------
# FX conversion (Zenith Bank UK reports in USD; converting to £ per this
# project's established FX methodology - see build_smbc.py precedent).
# Rates are Bank of England GBP/USD spot/average via poundsterlinglive.com's
# published archive, £1 = $X.
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2020": 1.3661,  # 31 Dec 2020 - only used for FY2021's opening cash balance
    "FY2021": 1.3521,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
    "FY2025": 1.3448,  # 31 Dec 2025
}
FX_AVG = {
    "FY2021": 1.3752,
    "FY2022": 1.2362,
    "FY2023": 1.2439,
    "FY2024": 1.2782,
    "FY2025": 1.3193,
}


def flow(usd):
    """Flow (cash flow statement line item) figures, £'000, at that year's average rate."""
    return {y: round(v / FX_AVG[y] / 1000, 1) for y, v in usd.items()}


def stock(usd):
    """Point-in-time (balance/capital) figures, £'000, at that year's period-end spot rate."""
    return {y: round(v / FX_SPOT[y] / 1000, 1) for y, v in usd.items()}


def opening_cash(usd):
    """Opening cash balance, £'000 - uses the PRIOR year's period-end spot rate (it's the
    same balance as that prior year's closing figure, so must convert identically)."""
    return {y: round(v / FX_SPOT[PREV_YEAR[y]] / 1000, 1) for y, v in usd.items()}


def pct(usd_strings):
    """Ratios are NOT converted - dimensionless and currency-invariant."""
    return usd_strings

# ---------------------------------------------------------------
# Source documents
# ---------------------------------------------------------------
BASE = "https://www.zenith-bank.co.uk/media"
AR2024_URL = f"{BASE}/2273/2024-annual-report-and-financial-statements.pdf"
AR2023_URL = f"{BASE}/2253/2023-annual-report-and-financial-statements.pdf"
AR2022_URL = f"{BASE}/2237/2022-annual-report-and-financial-statements.pdf"
AR2021_URL = f"{BASE}/2205/2021-annual-report-and-financial-statements.pdf"

P3_2025_URL = f"{BASE}/2290/pillar-3-zbuk-31dec25.pdf"
P3_2024_URL = f"{BASE}/2274/31dec24-pillar-3-zbuk.pdf"
P3_2023_URL = f"{BASE}/2260/pillar-3-31dec23-final.pdf"
P3_2022_URL = f"{BASE}/2238/zbuk-31dec22-pillar-3-disclosures.pdf"
P3_2021_URL = f"{BASE}/2228/31dec21-pillar-3.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Zenith Bank (UK) Limited (FRN 451720) is a UK subsidiary of Zenith Bank Plc (Nigeria). Unlike "
    "several other foreign-subsidiary banks in this workbook series (ICICI Bank UK, Philippine National Bank "
    "Europe, Citibank UK, State Bank of India UK), it prepares full financial statements under UK-adopted "
    "International Accounting Standards (not FRS 101/102 reduced disclosure), including a genuine Statement of "
    "Cash Flows every year - no cash-flow exemption applies. The Bank's own capital structure is CET1-only (no "
    "AT1 or Tier 2 instruments), so CET1 capital = Tier 1 capital = Total capital in every year shown."
)

FX_NOTE = (
    "FX CONVERSION NOTE: Zenith Bank (UK) Limited reports in US Dollars. This workbook converts every $ amount to "
    "£ for consistency with the rest of this series, following the same methodology established for SMBC Bank "
    "International plc: point-in-time/balance figures (capital, RWA, leverage exposure, HQLA, cash balances) use "
    "the Bank of England GBP/USD SPOT rate as at that fiscal year-end (31 December); flow figures (every cash "
    "flow statement line item) use the AVERAGE of Bank of England rates over that calendar year - both via "
    "poundsterlinglive.com's published Bank of England archive. Rates used (£1 = $X): 31 Dec 2020 spot 1.3661 "
    "(FY2021 opening cash only); FY2021 spot 1.3521 / average 1.3752; FY2022 spot 1.2097 / average 1.2362; "
    "FY2023 spot 1.2732 / average 1.2439; FY2024 spot 1.2515 / average 1.2782; FY2025 spot 1.3448 / average "
    "1.3193. All % ratios (CET1/Tier 1/Total Capital/Leverage/LCR/NSFR ratios) are shown EXACTLY as reported in "
    "USD and were NOT converted - a ratio is dimensionless and currency-invariant. Because stocks and flows are "
    "converted at different rates, the cash flow statement includes an explicit 'Effect of GBP/USD translation' "
    "reconciling line so opening + all flows + this line = closing exactly in £ terms - this line is purely an "
    "artefact of £ translation and has no bearing on the Bank's underlying USD results. This conversion was not "
    "explicitly requested for this bank (unlike SMBC) - applied for consistency with the rest of the series; "
    "flag if £'000 rather than the Bank's native US$'000 presentation is not what's wanted here."
)

RESTATEMENT_NOTE = (
    "RESTATEMENT NOTE: FY2023's own Annual Report cash flow figures (used for FY2023's column here) differ "
    "slightly from the 'restated' FY2023 comparative shown in the FY2024 Annual Report (e.g. operating activities "
    "$(344,220,013) as originally reported vs $(346,336,139) restated) - both report the same $276,069,567 "
    "closing balance, so the restatement is a reclassification between line items, not a change to overall cash "
    "movement. FY2023's own as-originally-reported figures are used throughout, consistent with this project's "
    "convention of preferring each year's own report over a later restated comparative."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Zenith Bank (UK) Limited's own Statement of Cash Flows (converted from USD to £, "
    "see FX conversion note below):\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.44-45 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.36 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.34 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.32 (Statement of Cash Flows) - {AR2021_URL}\n"
    "FY2025 cash flow is blank: no FY2025 Annual Report has been published yet (only the FY2025 Pillar 3 "
    "disclosure is out so far) - Pillar 3 sheets are fully populated for FY2025.\n"
    "Note: FY2021's own report presents operating cash flow more simply than later years - net interest is not "
    "separately reversed out of profit and re-added on a cash basis (no 'Interest income'/'Interest expense' "
    "adjustment lines, no 'Interest income received'/'Interest expense paid' cash lines); FY2022 onward introduced "
    "this more granular presentation. Blank cells for FY2021 on those rows reflect this, not missing data.\n"
    "Activity-total rows may be off by up to £0.2k from summing the visible line items above them, since each £ "
    "line is independently rounded to 1 decimal place before summing; the full statement ties exactly end-to-end "
    "via the net change, opening balance, exchange-rate-effect and translation-effect lines (verified to the "
    "penny in £'000 terms for all 4 populated years).\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + RESTATEMENT_NOTE
)


def p3_sources():
    return (
        "Sources - Zenith Bank (UK) Limited Pillar 3 Disclosures (UK KM1 - Key Metrics), converted from USD to £ "
        "where a $ amount (see FX conversion note on the Cash Flow Statement sheet; % ratios are unconverted):\n"
        f"FY2025: Pillar 3 Disclosures as at 31 Dec 2025, p.16 (Section 10, Key Metrics) - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures as at 31 Dec 2024, p.17 (Section 9, Key Metrics) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures as at 31 Dec 2023, p.17 (Section 9, Key Metrics) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures as at 31 Dec 2022, p.24 (Section 10, Key Metrics) - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures as at 31 Dec 2021, p.23 (Section 10, Key Metrics) - {P3_2021_URL}"
    )


bw = BankWorkbook(bank_name="Zenith Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="2A3E5C")

# ---------------------------------------------------------------
# Statement sources (Balance Sheet / P&L / Equity all come from the same
# Annual Reports already used for the Cash Flow Statement)
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - all figures are Zenith Bank (UK) Limited's own primary statements (converted from USD to £, see FX "
    "conversion note below):\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.42-43 (Statement of Profit or Loss and OCI), p.41 "
    f"(Statement of Financial Position) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.35 (Statement of Profit or Loss and OCI), p.34 "
    f"(Statement of Financial Position) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.33 (Statement of Profit or Loss and OCI), p.32 "
    f"(Statement of Financial Position) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.31 (Statement of Profit or Loss and OCI), p.30 "
    f"(Statement of Financial Position) - {AR2021_URL}\n"
    "FY2025 is blank: no FY2025 Annual Report has been published yet (only the FY2025 Pillar 3 disclosure is out "
    "so far) - Pillar 3 sheets are fully populated for FY2025.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

EQUITY_SOURCES = (
    "Sources - Zenith Bank (UK) Limited's own Statement of Changes in Equity (converted from USD to £, see FX "
    "conversion note below):\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.45 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.37 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.35 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.33 - {AR2021_URL}\n"
    "Opening balance (1 Jan 2021) is converted using the 31 Dec 2020 GBP/USD spot rate (1.3661) since it is the "
    "same balance as FY2020's closing position. Profit/OCI/dividend movements use each year's average rate; "
    "balances (opening/closing) use that date's spot rate - consistent with the rest of this workbook's FX "
    "methodology (see FX conversion note). Every year ties exactly: each closing balance matches both the next "
    "year's opening balance and that year's own Balance Sheet Total equity figure, to the penny in USD before "
    "conversion. Zero plug rows.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Zenith Bank (UK) Limited's own IFRS 9 credit risk / ECL notes (converted from USD to £, see FX "
    "conversion note below):\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.66-68 (Credit risk note, ECL by stage) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.58-60 (Credit risk note, ECL by stage) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.56-58 (Credit risk note, ECL by stage) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.54-56 (Credit risk note, ECL by stage) - {AR2021_URL}\n"
    "FY2025 is blank: no FY2025 Annual Report has been published yet.\n"
    "IFRS 9 STAGING NOTE: the Bank discloses the ECL ALLOWANCE by stage for loans and advances to customers in "
    "every year shown, but does NOT separately disclose the GROSS CARRYING AMOUNT by stage for this specific line "
    "(only the allowance split) - so a gross-exposure-based NPL ratio cannot be honestly derived from what's "
    "disclosed and is not shown here. Stage 3 (credit-impaired/default) ECL allowance is exactly nil for loans and "
    "advances to customers in every year FY2021-FY2024 - a genuine finding (no identified defaulted customer "
    "exposures in the disclosed period), not an omission.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bs_rows_usd = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2024": 480233340, "FY2023": 276069567, "FY2022": 629660723, "FY2021": 882609330}),
    ("DATA", "Derivative financial assets", {"FY2024": 1517779, "FY2023": 2410504, "FY2022": 2217579, "FY2021": 5109817}),
    ("DATA", "Loans and advances to banks", {"FY2024": 112643670, "FY2023": 153876803, "FY2022": 170490516, "FY2021": 154001591}),
    ("DATA", "Loans and advances to customers", {"FY2024": 443603255, "FY2023": 353457523, "FY2022": 315202777, "FY2021": 353514574}),
    ("DATA", "Securities measured at fair value through profit or loss", {"FY2024": 4295068, "FY2023": 5106226, "FY2022": 2568446, "FY2021": 10529212}),
    ("DATA", "Securities measured at fair value through OCI", {"FY2024": 1373024636, "FY2023": 1662513466, "FY2022": 1808390552, "FY2021": 1280759668}),
    ("DATA", "Securities measured at amortised cost", {"FY2024": 213536320, "FY2023": 197839485, "FY2022": 194149391, "FY2021": 186251678}),
    ("DATA", "Right-of-use assets", {"FY2024": 8693058, "FY2023": 1217453}),
    ("DATA", "Property and equipment", {"FY2024": 168467, "FY2023": 353650, "FY2022": 2585683, "FY2021": 3690371}),
    ("DATA", "Intangible assets", {"FY2024": 2446032, "FY2023": 771955, "FY2022": 993670, "FY2021": 1045877}),
    ("DATA", "Current tax assets", {"FY2024": 519490, "FY2023": 569334}),
    ("DATA", "Deferred tax assets", {"FY2024": 1024013, "FY2023": 2958195, "FY2022": 7028290, "FY2021": 1135311}),
    ("DATA", "Other assets", {"FY2024": 7348853, "FY2023": 2940642, "FY2022": 1675207, "FY2021": 1811204}),
    ("TOTAL", "Total assets", {"FY2024": 2649053981, "FY2023": 2660084803, "FY2022": 3134962834, "FY2021": 2880458633}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Derivative financial liabilities", {"FY2024": 3094465, "FY2023": 529436, "FY2022": 455372, "FY2021": 3737253}),
    ("DATA", "Deposits from banks", {"FY2024": 1285833708, "FY2023": 1283720090, "FY2022": 1971527508, "FY2021": 1891966488}),
    ("DATA", "Deposits from customers", {"FY2024": 871249258, "FY2023": 985581621, "FY2022": 778495366, "FY2021": 652949933}),
    ("DATA", "Repurchase agreements and other similar secured borrowing", {"FY2024": 88965017, "FY2023": 45992015, "FY2022": 76385080, "FY2021": 45573102}),
    ("DATA", "Current tax liabilities", {"FY2024": 2070141, "FY2023": 0, "FY2022": 1223535, "FY2021": 1038468}),
    ("DATA", "Impairment allowance on committed/off-balance-sheet facilities", {"FY2024": 625420, "FY2023": 0, "FY2022": 712297, "FY2021": 792249}),
    ("DATA", "Lease obligation", {"FY2024": 8819920, "FY2023": 1055479, "FY2022": 1852896, "FY2021": 2957523}),
    ("DATA", "Other liabilities", {"FY2024": 6073358, "FY2023": 7184781, "FY2022": 16905766, "FY2021": 7110089}),
    ("DATA", "Provision", {"FY2024": 169398}),
    ("TOTAL", "Total liabilities", {"FY2024": 2266900685, "FY2023": 2324063422, "FY2022": 2847557820, "FY2021": 2606125105}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share Capital", {"FY2024": 136701620, "FY2023": 136701620, "FY2022": 136701620, "FY2021": 136701620}),
    ("DATA", "FVOCI Reserves", {"FY2024": -598009, "FY2023": -4506575, "FY2022": -15885531, "FY2021": 543670}),
    ("DATA", "Retained earnings", {"FY2024": 246049685, "FY2023": 203826336, "FY2022": 166588925, "FY2021": 137088238}),
    ("TOTAL", "Total equity", {"FY2024": 382153296, "FY2023": 336021381, "FY2022": 287405014, "FY2021": 274333528}),
    ("TOTAL", "Total liabilities and equity", {"FY2024": 2649053981, "FY2023": 2660084803, "FY2022": 3134962834, "FY2021": 2880458633}),
]
bw.add_balance_sheet_sheet(
    title="Zenith Bank (UK) Limited — Statement of Financial Position",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used. FY2025 blank (no FY2025 Annual Report yet).",
    rows=[(k, l, stock(v) if k != "SECTION" else {}) for k, l, v in bs_rows_usd],
    sources_text=STATEMENTS_SOURCES
        + "\n\nPRESENTATION NOTE: 'Right-of-use assets' and 'Current tax assets' are shown as separate balance "
          "sheet lines only from FY2023 onward - FY2021/FY2022's own balance sheets do not present a right-of-use "
          "asset line at all (embedded within 'Property and equipment') and show no current tax asset line "
          "(the Bank held a current tax LIABILITY, not asset, in those years). FY2023 explicitly discloses both "
          "'Current tax liabilities' and 'Impairment allowance on committed but undrawn facilities' as nil (US$0), "
          "shown as 0 here (a confirmed disclosed nil, not a gap). All 4 years tie exactly: Total assets = Total "
          "liabilities + Total equity, to the penny in USD before conversion - zero plug rows.",
    first_col_width=64,
    source_height=320,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
pl_rows_usd = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2024": 150477684, "FY2023": 148015884, "FY2022": 78988040, "FY2021": 43357525}),
    ("DATA", "Interest expense", {"FY2024": -70136461, "FY2023": -51787199, "FY2022": -14995830, "FY2021": -5116838}),
    ("TOTAL", "Net interest income", {"FY2024": 80341223, "FY2023": 96228685, "FY2022": 63992210, "FY2021": 38240687}),
    ("DATA", "Fee and commission income", {"FY2024": 9673145, "FY2023": 10403918, "FY2022": 10543909, "FY2021": 8876199}),
    ("DATA", "Trading income", {"FY2024": 3955862}),
    ("DATA", "Trading and other income", {"FY2023": 2490366, "FY2022": 5262139, "FY2021": 1121346}),
    ("DATA", "Net gains/(losses) on disposal of securities measured at FVOCI", {"FY2024": -210586, "FY2023": -1656333}),
    ("DATA", "Net loss on derecognition of financial instruments", {"FY2024": -7486009}),
    ("DATA", "Fair value movement on financial derivatives (net)", {"FY2024": -3457754, "FY2023": 150805, "FY2022": -6904275}),
    ("DATA", "Exchange differences", {"FY2024": 2466208, "FY2023": -1415863, "FY2022": 4359385}),
    ("DATA", "Revaluation loss", {"FY2021": -4304574}),
    ("TOTAL", "Operating income", {"FY2024": 85282089, "FY2023": 106201578, "FY2022": 77253368, "FY2021": 43933658}),
    ("DATA", "Personnel expenses", {"FY2024": -23746944, "FY2023": -22411476, "FY2022": -17086793, "FY2021": -17001905}),
    ("DATA", "Depreciation and amortisation", {"FY2024": -1684109, "FY2023": -1624921, "FY2022": -1674804, "FY2021": -1777063}),
    ("DATA", "Other expenses", {"FY2024": -11821300, "FY2023": -8600456, "FY2022": -7959047, "FY2021": -7826210}),
    ("TOTAL", "Operating expenses", {"FY2024": -37252353, "FY2023": -32636853, "FY2022": -26720644, "FY2021": -26605178}),
    ("TOTAL", "Operating profit before impairment provision and taxation", {"FY2024": 48029736, "FY2023": 73564725, "FY2022": 50532724, "FY2021": 17328480}),
    ("DATA", "Net impairment credit/(charge) on financial assets", {"FY2024": 8225131, "FY2023": -771074, "FY2022": -5269233, "FY2021": -3692274}),
    ("TOTAL", "Profit before tax", {"FY2024": 56254867, "FY2023": 72793651, "FY2022": 45263491, "FY2021": 13636206}),
    ("DATA", "Income tax expense", {"FY2024": -14031518, "FY2023": -17956240, "FY2022": -10062804, "FY2021": -2232071}),
    ("TOTAL", "Profit for the year", {"FY2024": 42223349, "FY2023": 54837411, "FY2022": 35200687, "FY2021": 11404135}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Net change in fair value of debt instruments at FVOCI", {"FY2024": 5614429, "FY2023": 13774075, "FY2022": -22511501, "FY2021": -3808346}),
    ("DATA", "Net change in fair value of debt instruments reclassified to profit or loss", {"FY2024": 210586, "FY2023": 1656333, "FY2022": -50484, "FY2021": -598380}),
    ("DATA", "Expected credit loss reversals/(gains) recognised in income statement", {"FY2024": -460195, "FY2023": -193850}),
    ("DATA", "Income tax on items reclassified subsequently to profit or loss", {"FY2024": -1456254, "FY2023": -3857602, "FY2022": 6132784, "FY2021": 718575}),
    ("TOTAL", "Other comprehensive income for the year (net of tax)", {"FY2024": 3908566, "FY2023": 11378956, "FY2022": -16429201, "FY2021": -3688151}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2024": 46131915, "FY2023": 66216367, "FY2022": 18771486, "FY2021": 7715984}),
]
bw.add_income_statement_sheet(
    title="Zenith Bank (UK) Limited — Statement of Profit or Loss and Other Comprehensive Income",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used. FY2025 blank (no FY2025 Annual Report yet).",
    rows=[(k, l, flow(v) if k != "SECTION" else {}) for k, l, v in pl_rows_usd],
    sources_text=STATEMENTS_SOURCES
        + "\n\nPRESENTATION NOTE: row labels are held constant across years for comparability where the underlying "
          "concept is the same, even though the Bank's own report relabels/regroups some lines year to year - e.g. "
          "FY2022/FY2023's own reports label the pre-impairment subtotal 'Net operating income' rather than "
          "'Operating profit before impairment provision and taxation' (FY2021/FY2024's label, used here "
          "throughout); 'Trading income' (FY2024) replaces 'Trading and other income' (FY2021-FY2023) as a "
          "relabelling, not a scope change; FY2021's FV-movement/exchange-difference/FVOCI-disposal lines are "
          "combined into a single 'Revaluation loss' line in that year's report (not split as in later years, and "
          "NOT split to match AR2022's restated FY2021 comparative - FY2021's own report figure is used). "
          "'Net gains/(losses) on disposal of securities measured at FVOCI' and 'Expected credit loss "
          "reversals/(gains) recognised in income statement' are new lines first disclosed in FY2023's own report "
          "(present for FY2023 and FY2024 only; blank, not zero, for FY2021/FY2022 since those years' own reports "
          "genuinely do not disclose them as separate items - each is a carve-out of a few tens of thousands of "
          "dollars from a pre-existing broader line, with zero effect on any subtotal). "
          "RESTATEMENT NOTE: FY2023's own P&L (used for FY2023's column here, net interest income $96,228,685) "
          "differs from the FY2024 Annual Report's restated FY2023 comparative (interest income revised down to "
          "$147,456,638, net interest income $95,669,439) - FY2023's own report figure is used, consistent with "
          "this project's convention and the same restatement already documented on the Cash Flow Statement sheet. "
          "All totals tie exactly to the penny in USD before conversion for all 4 years shown - zero plug rows.",
    first_col_width=68,
    source_height=380,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity (chronological, oldest to newest)
# ---------------------------------------------------------------
EQ_HEADERS = ["Share Capital", "FVOCI Reserves", "Retained Earnings", "Total Equity"]


def eq_stock(usd_tuple, year):
    return tuple(round(v / FX_SPOT[year] / 1000, 1) for v in usd_tuple)


def eq_flow(usd_tuple, year):
    return tuple(round(v / FX_AVG[year] / 1000, 1) for v in usd_tuple)


EQ_ROWS = [
    ("TOTAL", "Balance as at 1 January 2021", eq_stock((136701620, 4231821, 134639777, 275573218), "FY2020")),
    ("DATA", "Profit for the year (FY2021)", eq_flow((0, 0, 11404135, 11404135), "FY2021")),
    ("DATA", "Other comprehensive income (FY2021)", eq_flow((0, -3688151, 0, -3688151), "FY2021")),
    ("DATA", "Dividends paid to shareholders (FY2021)", eq_flow((0, 0, -8955674, -8955674), "FY2021")),
    ("TOTAL", "Balance as at 31 December 2021", eq_stock((136701620, 543670, 137088238, 274333528), "FY2021")),
    ("DATA", "Profit for the year (FY2022)", eq_flow((0, 0, 35200687, 35200687), "FY2022")),
    ("DATA", "Other comprehensive income (FY2022)", eq_flow((0, -16429201, 0, -16429201), "FY2022")),
    ("DATA", "Dividends paid to shareholders (FY2022)", eq_flow((0, 0, -5700000, -5700000), "FY2022")),
    ("TOTAL", "Balance as at 31 December 2022", eq_stock((136701620, -15885531, 166588925, 287405014), "FY2022")),
    ("DATA", "Profit for the year (FY2023)", eq_flow((0, 0, 54837411, 54837411), "FY2023")),
    ("DATA", "Other comprehensive income (FY2023)", eq_flow((0, 11378956, 0, 11378956), "FY2023")),
    ("DATA", "Dividends paid to shareholders (FY2023)", eq_flow((0, 0, -17600000, -17600000), "FY2023")),
    ("TOTAL", "Balance as at 31 December 2023", eq_stock((136701620, -4506575, 203826336, 336021381), "FY2023")),
    ("DATA", "Profit for the year (FY2024)", eq_flow((0, 0, 42223349, 42223349), "FY2024")),
    ("DATA", "Other comprehensive income (FY2024)", eq_flow((0, 3908566, 0, 3908566), "FY2024")),
    ("DATA", "Dividends paid to shareholders (FY2024)", eq_flow((0, 0, 0, 0), "FY2024")),
    ("TOTAL", "Balance as at 31 December 2024", eq_stock((136701620, -598009, 246049685, 382153296), "FY2024")),
]
bw.add_equity_changes_sheet(
    title="Zenith Bank (UK) Limited — Statement of Changes in Equity",
    subtitle="£'000, converted from USD - chronological 1 January 2021 through 31 December 2024. No FY2025 movement shown (no FY2025 Annual Report yet).",
    headers=EQ_HEADERS,
    rows=EQ_ROWS,
    sources_text=EQUITY_SOURCES,
    first_col_width=52,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD, then converted via flow()/stock()/opening_cash())
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit for the year", {"FY2024": 42223349, "FY2023": 54837411, "FY2022": 35200687, "FY2021": 11404135}),
    ("DATA", "Impairment provision charge/(reversal)", {"FY2024": -8225131, "FY2023": 771074, "FY2022": 5269233, "FY2021": 3692274}),
    ("DATA", "Depreciation of property and equipment", {"FY2024": 1184560, "FY2023": 1074768, "FY2022": 1131020, "FY2021": 1114950}),
    ("DATA", "Amortisation of intangible assets", {"FY2024": 499549, "FY2023": 550153, "FY2022": 543784, "FY2021": 662113}),
    ("DATA", "Interest expense on Right-of-use lease obligations", {"FY2024": 346769, "FY2023": 18326, "FY2021": 49200}),
    ("DATA", "Recoveries of bad debts written off", {"FY2022": -69063}),
    ("DATA", "Current income tax expense", {"FY2024": 13553590, "FY2023": 17745025, "FY2022": 9439732, "FY2021": 2232071}),
    ("DATA", "Deferred income tax expense", {"FY2024": 477928, "FY2023": 211215, "FY2022": 239806}),
    ("DATA", "Foreign currency translation gain - Right-of-use assets", {"FY2021": -211646}),
    ("DATA", "Foreign currency translation gain/(loss) - Lease obligation", {"FY2023": 110592, "FY2022": -317849, "FY2021": -307066}),
    ("DATA", "Foreign currency translation gain - Deferred tax assets", {"FY2022": 45}),
    ("DATA", "Foreign currency translation (gain)/loss - Corporation tax liability", {"FY2023": -123381, "FY2022": -43758, "FY2021": -2756}),
    ("DATA", "Deferred tax asset write-off (legacy)", {"FY2023": 1278}),
    ("DATA", "Impairment on equity investments", {"FY2021": 66644}),
    ("DATA", "Interest income", {"FY2024": -150477684, "FY2023": -148015884, "FY2022": -78988040}),
    ("DATA", "Interest expense", {"FY2024": 69789692, "FY2023": 51768873, "FY2022": 14995830}),
    ("DATA", "Fair value movement on securities measured at FVTPL", {"FY2024": 69201}),
    ("DATA", "Fair value movement on derivative contracts", {"FY2024": 3457754}),
    ("DATA", "Unrealised foreign exchange (gains)/losses", {"FY2024": -2466206}),
    ("DATA", "Loss on derecognition of assets", {"FY2024": 7486009}),
    ("DATA", "Decrease/(Increase) in loans and advances to banks", {"FY2024": 37241172, "FY2023": 17720794, "FY2022": -16995457, "FY2021": 29588441}),
    ("DATA", "(Increase)/Decrease in loans and advances to customers", {"FY2024": -92041493, "FY2023": -37968440, "FY2022": 39931143, "FY2021": -196507247}),
    ("DATA", "(Increase)/Decrease in securities measured at fair value through profit or loss", {"FY2024": -120096, "FY2023": -1751539, "FY2022": 6591830, "FY2021": 525737}),
    ("DATA", "Decrease/(Increase) in securities measured at FVOCI", {"FY2024": 314536239, "FY2023": 155867577, "FY2022": -568931339, "FY2021": -313837082}),
    ("DATA", "(Increase)/Decrease in other assets", {"FY2024": -4408211, "FY2023": -1265435, "FY2022": 135997, "FY2021": -577710}),
    ("DATA", "(Decrease)/Increase in deposits from banks", {"FY2024": -7577015, "FY2023": -688088465, "FY2022": 79243126, "FY2021": 600568191}),
    ("DATA", "(Decrease)/Increase in deposits from customers", {"FY2024": -104968633, "FY2023": 200100437, "FY2022": 123837261, "FY2021": -74898564}),
    ("DATA", "Increase/(Decrease) in repurchase agreements and other similar secured borrowing", {"FY2024": 43001229, "FY2023": -30579358, "FY2022": 30379006, "FY2021": 45573102}),
    ("DATA", "(Increase)/Decrease in derivative financial instruments (net)", {"FY2023": -118861, "FY2022": -389643, "FY2021": 5839211}),
    ("DATA", "Increase/(Decrease) in other liabilities", {"FY2024": 4871782, "FY2023": -9720985, "FY2022": 9795677, "FY2021": 2836076}),
    ("DATA", "Interest income received", {"FY2024": 104041078, "FY2023": 136365040, "FY2022": 86951488}),
    ("DATA", "Interest expense paid", {"FY2024": -53649527, "FY2023": -44315715, "FY2022": -12499405}),
    ("DATA", "Income tax paid", {"FY2024": -11483449, "FY2023": -19414513, "FY2022": -9210907, "FY2021": -1768909}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2024": 207362455, "FY2023": -344220013, "FY2022": -243759796, "FY2021": 116041165}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of securities measured at amortised cost", {"FY2024": -81087234, "FY2023": -26729752, "FY2022": -47624983, "FY2021": -42913212}),
    ("DATA", "Proceeds from redemption of securities measured at amortised cost", {"FY2024": 69818444, "FY2023": 21071506, "FY2022": 27641163, "FY2021": 32279901}),
    ("DATA", "Interest income received (investing)", {"FY2024": 14053675, "FY2023": 15202064, "FY2022": 17837082}),
    ("DATA", "Acquisition of property and equipment", {"FY2024": -62128, "FY2023": -60188, "FY2022": -26331, "FY2021": -34354}),
    ("DATA", "Additions to Right-of-use assets", {"FY2021": -46639}),
    ("DATA", "Acquisition of intangible assets", {"FY2024": -2173626, "FY2023": -328438, "FY2022": -491577, "FY2021": -312642}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2024": 549131, "FY2023": 9155192, "FY2022": -2664646, "FY2021": -11026946}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of lease liability/obligation", {"FY2024": -672177, "FY2023": -926335, "FY2022": -824165, "FY2021": -1084238}),
    ("DATA", "Addition of new lease obligation", {"FY2021": 46639}),
    ("DATA", "Dividends paid to shareholders", {"FY2023": -17600000, "FY2022": -5700000, "FY2021": -8955674}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {"FY2024": -672177, "FY2023": -18526335, "FY2022": -6524165, "FY2021": -9993273}),
    ("TOTAL", "Net (decrease)/increase of cash and cash equivalents", {"FY2024": 207239409, "FY2023": -353591156, "FY2022": -252948607, "FY2021": 95020946}),
    ("DATA", "Cash and cash equivalents as at 1 January", {"FY2024": 276069567, "FY2023": 629660723, "FY2022": 882609330, "FY2021": 787588384}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents (as reported, USD)", {"FY2024": -3075636}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2024": 480233340, "FY2023": 276069567, "FY2022": 629660723, "FY2021": 882609330}),
]

# convert: SECTION rows pass through unchanged; opening-cash uses opening_cash()
# (prior year's spot rate); closing cash uses stock() (this year's spot rate) since
# it's a point-in-time balance, NOT a flow; everything else (DATA/TOTAL) uses flow().
_usd_by_label = {label: usd for _, label, usd in rows_usd}
rows = []
for kind, label, usd in rows_usd:
    if kind == "SECTION":
        rows.append((kind, label, {}))
    elif label == "Cash and cash equivalents as at 1 January":
        rows.append((kind, label, opening_cash(usd)))
    elif label == "Cash and cash equivalents at 31 December":
        rows.append((kind, label, stock(usd)))
    else:
        rows.append((kind, label, flow(usd)))
    if label == "Effect of exchange rate changes on cash and cash equivalents (as reported, USD)":
        # £ translation plug (see FX_NOTE): stocks (opening/closing) and flows
        # (everything else) are converted at different rates, so the £ statement
        # needs an explicit reconciling line to tie exactly. Computed programmatically
        # as closing(£) - opening(£) - net change(£) - reported FX-effect(£), per year,
        # rather than hardcoded, so it can never drift out of sync with the rates above.
        opening_gbp = opening_cash(_usd_by_label["Cash and cash equivalents as at 1 January"])
        closing_gbp = stock(_usd_by_label["Cash and cash equivalents at 31 December"])
        net_change_gbp = flow(_usd_by_label["Net (decrease)/increase of cash and cash equivalents"])
        fx_gbp = flow(usd)
        plug = {
            y: round(closing_gbp[y] - opening_gbp[y] - net_change_gbp[y] - fx_gbp.get(y, 0), 1)
            for y in closing_gbp
        }
        rows.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", plug))

bw.add_cash_flow_sheet(
    title="Zenith Bank (UK) Limited — Statement of Cash Flows",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used. FY2025 blank (no FY2025 Annual Report yet).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=320,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality (placed after Cash Flow Statement, before Pillar 3 sheets)
# ---------------------------------------------------------------
aq_rows_usd = [
    ("SECTION", "Loans and advances to customers", {}),
    ("DATA", "Gross exposure", {"FY2024": 446909206, "FY2023": 359647626, "FY2022": 320279907, "FY2021": 359441063}),
    ("DATA", "IFRS 9 impairment allowance", {"FY2024": -3305951, "FY2023": -6190103, "FY2022": -5077130, "FY2021": -5926489}),
    ("TOTAL", "Net loans and advances to customers", {"FY2024": 443603255, "FY2023": 353457523, "FY2022": 315202777, "FY2021": 353514574}),
    ("SECTION", "IFRS 9 ECL allowance by stage (Loans and advances to customers)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2024": 2871738, "FY2023": 5808582, "FY2022": 4303234, "FY2021": 5236789}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2024": 434213, "FY2023": 381521, "FY2022": 773896, "FY2021": 689700}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired/default)", {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Total ECL allowance", {"FY2024": 3305951, "FY2023": 6190103, "FY2022": 5077130, "FY2021": 5926489}),
]
aq_rows = [(k, l, stock(v)) if k != "SECTION" else (k, l, {}) for k, l, v in aq_rows_usd]
aq_rows.insert(4, ("DATA", "Impairment as % of gross exposure", {"FY2024": "0.7%", "FY2023": "1.7%", "FY2022": "1.6%", "FY2021": "1.6%"}))

bw.add_asset_quality_sheet(
    title="Zenith Bank (UK) Limited — Asset Quality",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used. FY2025 blank (no FY2025 Annual Report yet).",
    rows=aq_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=280,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=48, source_height=120)


CET1_TIER1_TOTAL_USD = {"FY2025": 431376, "FY2024": 378325, "FY2023": 338086, "FY2022": 290721, "FY2021": 281088}
RWA_USD = {"FY2025": 1843312, "FY2024": 1475750, "FY2023": 1167888, "FY2022": 1125146, "FY2021": 1352803}

metric("CET1 Capital", "£'000 (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", stock(CET1_TIER1_TOTAL_USD))], p3_sources())
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%"})], p3_sources())
metric("Tier 1 Capital", "£'000 (conv. from USD)", [("Tier 1 capital", stock(CET1_TIER1_TOTAL_USD))], p3_sources(),
       note="Equal to CET1 capital in every year - the Bank holds no Additional Tier 1 (AT1) instruments.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%"})], p3_sources())
metric("Total Capital", "£'000 (conv. from USD)", [("Total capital", stock(CET1_TIER1_TOTAL_USD))], p3_sources(),
       note="Equal to CET1/Tier 1 capital in every year - the Bank holds no AT1 or Tier 2 instruments.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%"})], p3_sources())
metric("Total RWAs", "£'000 (conv. from USD)", [("Total risk-weighted exposure amount", stock(RWA_USD))], p3_sources(),
       note="FY2023's figure (own report, £m equivalent of $1,167,888k) differs from the FY2024 report's restated FY2023 "
            "comparative ($1,203,364k) - a Basic Indicator Approach operational-risk methodology update. FY2023's own "
            "report figure is used, consistent with this project's convention of preferring each year's own report.")

rwa_rows_usd = [
    ("DATA", "Credit Risk (excluding CCR)", {"FY2025": 1646471, "FY2024": 1205520, "FY2023": 1003271, "FY2022": 939921, "FY2021": 1242586}),
    ("DATA", "Counterparty Credit Risk (CCR)", {"FY2025": 6886, "FY2024": 98068, "FY2023": 54106, "FY2022": 79324}),
    ("DATA", "of which: Credit Valuation Adjustment (CVA)", {"FY2025": 1085, "FY2024": 1392, "FY2023": 1301, "FY2022": 1025, "FY2021": 4500}),
    ("DATA", "Settlement Risk", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Market Risk (FX and commodities)", {"FY2025": 5073, "FY2024": 4202, "FY2023": 3869, "FY2022": 11250, "FY2021": 7485}),
    ("DATA", "Operational Risk", {"FY2025": 184881, "FY2024": 167960, "FY2023": 106641, "FY2022": 94651, "FY2021": 98232}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 1843312, "FY2024": 1475750, "FY2023": 1167888, "FY2022": 1125146, "FY2021": 1352803}),
    ("DATA", "Memo: amounts below thresholds for deduction (already included within Credit Risk above)", {"FY2025": 0, "FY2024": 1024}),
]
bw.add_rwa_breakdown_sheet(
    title="Zenith Bank (UK) Limited — RWA Breakdown (UK OV1)",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=[(k, l, stock(v)) for k, l, v in rwa_rows_usd],
    sources_text=p3_sources()
        + "\n\nUK OV1 template (Overview of risk weighted exposure amounts). Each year's own Pillar 3 report is "
          "used. FY2024's own report splits Credit Risk (excl. CCR) $1,205,520k / CCR $98,068k, while the FY2025 "
          "report's restated FY2024 comparative shows a different split ($1,280,947k / $22,641k) - same total "
          "($1,475,750k) either way; a reclassification between the two lines, not a change to overall RWAs. "
          "FY2021's own report pre-dates the UK OV1 template's current form: it combines most Counterparty Credit "
          "Risk into the 'Credit Risk' line (footnoted in the source as immaterial, <1% of Credit Risk) while "
          "still separately disclosing CVA - so FY2021's CCR row is blank (not zero) and its Credit Risk row "
          "includes that CCR. FY2023's total ($1,167,888k) is $1k off the sum of its own visible rows due to "
          "source-side rounding of each row to the nearest $1k - not a plug. Settlement Risk is nil (explicitly "
          "disclosed, immaterial) in every year. The 'amounts below thresholds for deduction' memo line (FY2024 "
          "only, $1,024k) is explicitly excluded from the Total per the source's own footnote (already counted "
          "within Credit Risk) - not additive.",
    first_col_width=64,
    source_height=320,
    unit_suffix=" (£'000, conv. from USD)",
)

metric(
    "Leverage Ratio", "£'000 / % (conv. from USD)",
    [
        ("Total exposure measure excluding claims on central banks", stock({"FY2025": 3171798, "FY2024": 2987483, "FY2023": 2872422, "FY2022": 3409175, "FY2021": 3219954})),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "12.08%", "FY2024": "11.25%", "FY2023": "9.76%", "FY2022": "7.32%", "FY2021": "8.36%"}),
    ],
    p3_sources(),
)

metric(
    "LCR", "£'000 / % (conv. from USD)",
    [
        ("Total high-quality liquid assets (HQLA), weighted value", stock({"FY2025": 952538, "FY2024": 1013789, "FY2023": 1147653, "FY2022": 1227530, "FY2021": 932821})),
        ("Total net cash outflows, adjusted value", stock({"FY2025": 352543, "FY2024": 306820, "FY2023": 369648, "FY2022": 374822, "FY2021": 337730})),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "270.19%", "FY2024": "330.42%", "FY2023": "310%", "FY2022": "343%", "FY2021": "276%"}),
    ],
    p3_sources(),
    note="LCR methodology changed across vintages: FY2021 is a point-in-time (year-end) figure as originally "
         "disclosed; FY2022 onward is a 12-month simple average, per each year's own report. FY2022's own report "
         "(374,822k/343%) differs from the FY2023 report's restated FY2022 comparative (348,210k/352%) - FY2022's "
         "own report figure is used, per this project's convention.",
)

metric(
    "NSFR", "£'000 / % (conv. from USD)",
    [
        ("Total available stable funding", stock({"FY2025": 1316936, "FY2024": 1136904, "FY2023": 1066880, "FY2022": 912816})),
        ("Total required stable funding", stock({"FY2025": 948441, "FY2024": 768308, "FY2023": 744377, "FY2022": 735763})),
        ("Net Stable Funding Ratio (%)", {"FY2025": "138.85%", "FY2024": "147.98%", "FY2023": "143%", "FY2022": "124%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="The UK NSFR was adopted from 1 January 2022 (per the FY2021 and FY2022 Pillar 3 reports), so no FY2021 "
         "figures exist.",
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "No MREL disclosure (numeric or qualitative) or UK KM2 template found in any year's "
                             "Pillar 3 report - not explicitly stated as an exemption, but consistent with the "
                             "Bank's small size relative to typical MREL-in-scope thresholds."})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
cf_totals_usd = {
    "Net cash generated from/(used in) operating activities": {"FY2024": 207362455, "FY2023": -344220013, "FY2022": -243759796, "FY2021": 116041165},
    "Net cash generated from/(used in) investing activities": {"FY2024": 549131, "FY2023": 9155192, "FY2022": -2664646, "FY2021": -11026946},
    "Net cash generated from/(used in) financing activities": {"FY2024": -672177, "FY2023": -18526335, "FY2022": -6524165, "FY2021": -9993273},
}
cf_close_usd = {"FY2024": 480233340, "FY2023": 276069567, "FY2022": 629660723, "FY2021": 882609330}

bw.add_overview_sheet(
    cash_flow_totals=[(label, flow(vals)) for label, vals in cf_totals_usd.items()]
                      + [("Cash and cash equivalents at end of year", stock(cf_close_usd))],
    cash_flow_unit="£'000",
    balance_sheet_totals=[
        ("Total assets", stock({"FY2024": 2649053981, "FY2023": 2660084803, "FY2022": 3134962834, "FY2021": 2880458633})),
        ("Total liabilities", stock({"FY2024": 2266900685, "FY2023": 2324063422, "FY2022": 2847557820, "FY2021": 2606125105})),
        ("Total equity", stock({"FY2024": 382153296, "FY2023": 336021381, "FY2022": 287405014, "FY2021": 274333528})),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", flow({"FY2024": 80341223, "FY2023": 96228685, "FY2022": 63992210, "FY2021": 38240687})),
        ("Operating income", flow({"FY2024": 85282089, "FY2023": 106201578, "FY2022": 77253368, "FY2021": 43933658})),
        ("Profit before tax", flow({"FY2024": 56254867, "FY2023": 72793651, "FY2022": 45263491, "FY2021": 13636206})),
        ("Profit for the year", flow({"FY2024": 42223349, "FY2023": 54837411, "FY2022": 35200687, "FY2021": 11404135})),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Total equity (period end)", stock({"FY2024": 382153296, "FY2023": 336021381, "FY2022": 287405014, "FY2021": 274333528})),
    ],
    equity_changes_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%"}),
        ("Tier 1 Ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%"}),
        ("Total Capital Ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%"}),
        ("Leverage Ratio", {"FY2025": "12.08%", "FY2024": "11.25%", "FY2023": "9.76%", "FY2022": "7.32%", "FY2021": "8.36%"}),
        ("LCR", {"FY2025": "270.19%", "FY2024": "330.42%", "FY2023": "310%", "FY2022": "343%", "FY2021": "276%"}),
        ("NSFR", {"FY2025": "138.85%", "FY2024": "147.98%", "FY2023": "143%", "FY2022": "124%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation. All £ figures are converted from the Bank's native USD reporting (see Cash Flow Statement "
         "sheet's FX conversion note) - this conversion was not explicitly requested for this bank but applied for "
         "consistency with the rest of the series. FY2025 cash flow is blank (no FY2025 Annual Report published "
         "yet); Pillar 3 is fully populated for FY2025.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ZENITH FINANCIALS.xlsx")
