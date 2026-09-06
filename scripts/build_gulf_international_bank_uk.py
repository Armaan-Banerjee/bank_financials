import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024",
             "FY2020": "FY2019"}

# ---------------------------------------------------------------
# FX conversion (GIB UK reports in USD; converting to £ per this project's
# established FX methodology - same public Bank of England GBP/USD spot/
# average rates already used for Zenith Bank UK / Union Bank of India UK /
# Credit Suisse International, reused here rather than re-derived).
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2019": 1.3210,  # 31 Dec 2019 - only used for FY2020's opening cash balance
    "FY2020": 1.3661,  # 31 Dec 2020
    "FY2021": 1.3521,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
}
FX_AVG = {
    "FY2020": 1.2825,
    "FY2021": 1.3752,
    "FY2022": 1.2362,
    "FY2023": 1.2439,
    "FY2024": 1.2782,
}


def flow(usd):
    """Flow (cash flow statement line item) figures, £'000, at that year's average rate."""
    return {y: round(v / FX_AVG[y] / 1000, 1) for y, v in usd.items() if y in FX_AVG}


def stock(usd):
    """Point-in-time (balance/capital) figures, £'000, at that year's period-end spot rate."""
    return {y: round(v / FX_SPOT[y] / 1000, 1) for y, v in usd.items() if y in FX_SPOT}


def opening_cash(usd):
    """Opening cash balance, £'000 - uses the PRIOR year's period-end spot rate (it's the
    same balance as that prior year's closing figure, so must convert identically)."""
    return {y: round(v / FX_SPOT[PREV_YEAR[y]] / 1000, 1) for y, v in usd.items() if PREV_YEAR.get(y) in FX_SPOT}


# ---------------------------------------------------------------
# Source documents
# ---------------------------------------------------------------
CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/01223938/filing-history"
AR2024_URL = f"{CH_BASE}/MzQ2MTE4ODYxN2FkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = f"{CH_BASE}/MzQxNzM5ODc0MWFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = f"{CH_BASE}/MzM3NTI0MDA2MmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = f"{CH_BASE}/MzM1NTYyODEwMGFkaXF6a2N4/document?format=pdf&download=0"
# HD-062 (2026-09-06) FY2020 extension: "Full accounts made up to 31 December
# 2020", filed 10 Sep 2021, re-verified directly against Companies House's own
# filing-history page 2 for this company (the FY2021 filing above only goes
# back to page 1) rather than assumed from the ticket's nominal floor.
AR2020_URL = f"{CH_BASE}/MzMxMzAyNDY0OGFkaXF6a2N4/document?format=pdf&download=0"

P3_2024_URL = "https://gib-am.files.svdcdn.com/production/documents/2024-GIBUK-Pillar-3-disclosures-Board-approved.pdf"
P3_2023_URL = "https://gib-am.files.svdcdn.com/production/documents/Fund-sustainability-related-documents/2023-GIBUK-Pillar-3-disclosures.pdf"
P3_2022_URL = "https://web.archive.org/web/20240223164517/https://gibam.com/assets/2022-GIBUK-Pillar-3-disclosures_VF.pdf"
# Note: the 20230927145657 snapshot originally cited here is truncated by the
# Wayback Machine's own crawler at 1,048,576 bytes (confirmed: it fails to
# open as a valid PDF at all) - the 20240223164517 snapshot above is a full,
# valid capture of the same document and was used for this workbook's RWA
# Breakdown sheet.
P3_2021_URL = "https://web.archive.org/web/20230329132856/https://gibam.com/assets/2021-GIBUK-Pillar-3_Final.pdf"
# HD-062 (2026-09-06): found via a Wayback CDX domain scan of gibam.com/assets/*
# (the naive "2020-GIBUK-Pillar-3_Final.pdf" direct URL is not itself archived
# stand-alone at gibam.com any more) - this snapshot is a full, valid capture
# confirmed by rendering all 38 pages as images (the PDF's own text layer is
# present but its custom font's cmap renders numbers/table text as mangled
# unicode glyphs when copy-pasted, so every figure below was read visually
# from the rendered page image, not machine-extracted).
P3_2020_URL = "https://web.archive.org/web/20220518000354/https://gibam.com/assets/2020-GIBUK-Pillar-3_Final.pdf"
# HD-062 (2026-09-06) IMPORTANT DATA-QUALITY NOTE: the only surviving Wayback
# capture of this document (there is no other successful, non-404 snapshot in
# the CDX index for this URL) is itself truncated by the Wayback Machine's own
# playback service at exactly 1,048,576 bytes (2^20) - confirmed by direct
# re-download (byte-for-byte identical across the plain/if_/id_ URL variants,
# always ending mid-stream with no %%EOF) - the SAME failure mode already
# documented above for the FY2022 snapshot, just previously unconfirmed for
# this one. A prior (killed) session's claim that this snapshot was "a full,
# valid capture ... confirmed by rendering all 38 pages" was NOT correct and
# has been corrected here. The truncated file was repaired with `qpdf
# --qdf --replace-input` (rebuilds the cross-reference table from the
# recoverable object stream, discarding only the unrecoverable tail past the
# 1MB cutoff), after which `pdftotext -layout` extracted clean, legible text
# for capital resources/adequacy, leverage, and liquidity (LCR) - contrary to
# the prior session's claim of a mangled custom-font cmap, the text layer for
# most of the document is fine; only one small section (the capital-buffer
# summary table under 4.6, not used for any figure in this workbook) renders
# as garbled non-Latin glyphs, isolated to that one table.
ENTITY_NOTE = (
    "ENTITY NOTE: Gulf International Bank (UK) Limited (\"GIB UK\", FRN 124772, company 01223938) is a wholly "
    "owned subsidiary of Gulf International Bank B.S.C. (Bahrain, sovereign-backed by several Gulf Cooperation "
    "Council states), trading as \"GIB Asset Management\" (GIB AM) for its investment-management business, with a "
    "branch in New York. It prepares standalone (non-consolidated) financial statements under UK-adopted "
    "international accounting standards, exempt from producing group accounts under Companies Act 2006 s.401 and "
    "IFRS 10 (its parent's consolidated accounts are filed in Bahrain). No cash-flow exemption applies - a full "
    "Statement of Cash Flow is presented every year. FY2025 accounts had not yet been filed with Companies House "
    "and no FY2025 Pillar 3 disclosure had been published as at the time of this workbook's research (accounts "
    "for this entity have historically been filed 3-4 months after the 31 December year-end, so this is normal "
    "lag, not a gap).\n\n"
    "HD-062 (2026-09-06) FY2020 EXTENSION: FY2020 accounts and Pillar 3 disclosure both genuinely exist and were "
    "obtained and read in full (re-verified directly against Companies House and a Wayback CDX domain scan of "
    "gibam.com rather than assumed from the ticket's nominal 'confirmed floor FY2020' signal) - no self-skip was "
    "needed for this bank. FY2020's Pillar 3 Disclosures document (a Basel II-era 38-page document, titled "
    "'Basel II Pillar 3 Disclosures', predating the UK KM1/OV1 template rollout later years use) DOES disclose an "
    "LCR (section 5.3 'Liquidity and Funding Risk', reported as 'Liquidity Coverage ratio' with a 'Liquidity "
    "Buffer' and 'Total Net cash outflows' - functionally equivalent to later years' HQLA/net-cash-outflow KM1 "
    "fields, see the LCR sheet's own basis note for the two ratio variants disclosed). It genuinely has NO NSFR "
    "or MREL section anywhere in its own table of contents or body text (only a passing mention of the upcoming "
    "regulatory 'binding NSFR measure of 100%' requirement, not GIB UK's own NSFR ratio) - confirmed by reading "
    "the full document, not assumed from a missing keyword - so those two metric sheets are genuinely blank for "
    "FY2020 specifically, distinct from later years where a value exists (FY2021 onward). It also predates the "
    "UK OV1 RWA-breakdown template used from FY2021 onward: no separate counterparty-credit-risk (CCR) or CVA "
    "line is disclosed for FY2020, so the RWA Breakdown sheet's CCR/CVA rows are genuinely blank that year - see "
    "that sheet's own source note for how the credit/market/operational RWA figures were derived instead."
)

FX_NOTE = (
    "FX CONVERSION NOTE: GIB UK reports in US Dollars (its functional and presentation currency per its own "
    "accounting policy note). This workbook converts every $ amount to £ for consistency with the rest of this "
    "series, following the same methodology established for Zenith Bank UK/Union Bank of India UK/Credit Suisse "
    "International: point-in-time/balance figures (capital, RWA, leverage exposure, HQLA/stable-funding amounts, "
    "cash balances) use the Bank of England GBP/USD SPOT rate as at that fiscal year-end; flow figures (every "
    "cash flow statement line item) use the AVERAGE of Bank of England rates over that calendar year. Rates used "
    "(£1 = $X, reused from this project's existing FX rate table): 31 Dec 2019 spot 1.3210 (FY2020 opening cash "
    "only); FY2020 spot 1.3661 / average 1.2825; FY2021 spot 1.3521 / average 1.3752; FY2022 spot 1.2097 / "
    "average 1.2362; FY2023 spot 1.2732 / average 1.2439; FY2024 spot 1.2515 / average 1.2782. All % ratios are "
    "shown exactly as reported in USD and "
    "were NOT converted - a ratio is dimensionless and currency-invariant. Because stocks and flows are converted "
    "at different rates, the cash flow statement includes an explicit 'Effect of GBP/USD translation' reconciling "
    "line, computed programmatically so it can never drift out of sync with the rates above, so that opening + "
    "all flows + this line = closing exactly in £ terms - this line is purely an artefact of £ translation and "
    "has no bearing on the Bank's underlying USD results. This conversion was not explicitly requested for this "
    "bank - applied for consistency with the rest of the series; flag if £'000 rather than the Bank's native "
    "US$'000 presentation is not what's wanted here."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Gulf International Bank (UK) Limited's own Statement of Cash Flow (converted from "
    "USD to £, see FX conversion note below), transcribed from scanned/image-only Companies House filings (no "
    "text layer in any of the 5 filings):\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.109 (Statement of Cash Flow) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.71 (Statement of Cash Flow, incl. FY2022 comparative) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.52 (Statement of Cash Flow) - {AR2021_URL}\n"
    f"FY2020: Annual Report and Financial Statements 2020, p.29 (Statement of Cash Flow) - {AR2020_URL}\n"
    "FY2022's own column is sourced from the FY2023 Annual Report's comparative column (p.71 above) rather than "
    "the FY2022 Annual Report directly - both would show the same figures for FY2022 (a bank's own prior-year "
    "comparative is not normally restated absent a disclosed reason, and none is disclosed here); the FY2022 "
    "filing itself is also fully scanned - see AR2022_URL for reference: " + AR2022_URL + ".\n"
    "FY2025 is blank: no FY2025 Annual Report has been filed with Companies House yet.\n"
    "All 5 years' opening-to-closing cash bridges reconcile exactly in USD as originally reported; the £ "
    "conversion is exact by construction (translation-effect line computed programmatically, see FX note). "
    "FY2020/FY2021/FY2023/FY2024's operating-activities line items also sum exactly (in USD) to each year's own "
    "printed subtotal (FY2020: independently re-summed to -$1,602,673k, exactly matching the source's own "
    "printed 'Net cash (used)/from operating activities' subtotal). FY2022's do not: summing FY2022's own line "
    "items above gives $285,026k vs the source's own printed $287,025k subtotal - a $1,999k (~0.7%) gap within "
    "the source document's own comparative column, not traceable to a specific mis-cast line (each line was "
    "independently re-checked against the source image). Flagged rather than forced to reconcile, per this "
    "project's convention for unexplained source-side gaps. FY2020 has no reported 'Net foreign exchange "
    "difference' line at all (unlike FY2022-FY2024) - its own opening-to-closing USD bridge already ties exactly "
    "without one ($6,861,304k - $1,604,216k = $5,257,088k), so that cell is genuinely blank for FY2020 rather "
    "than estimated; the programmatic £ translation-effect line still applies since GBP conversion at differing "
    "spot/average rates still requires a plug even when the USD bridge itself needs none.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)


def p3_sources():
    return (
        "Sources - Gulf International Bank (UK) Limited Pillar 3 Disclosures (UK KM1 - Key Metrics table), "
        "converted from USD to £ where a $ amount (see FX conversion note on the Cash Flow Statement sheet; % "
        "ratios are unconverted):\n"
        f"FY2024: Pillar 3 Disclosures as at 31 December 2024 (Board-approved), p.6 (UK KM1) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures as at 31 December 2023, p.6 (UK KM1) - {P3_2023_URL}\n"
        f"FY2022: sourced from the FY2023 Pillar 3 Disclosures' own T-4/prior-year comparative column (p.6 above), "
        "which matches the FY2022 Pillar 3 Disclosures document exactly where both are legible - "
        f"{P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures as at 31 December 2021, p.6 (Key ratios summary) and p.7 (Liquidity, "
        f"Q4 2021 quarter-end figures) - {P3_2021_URL}\n"
        f"FY2020: 'Basel II Pillar 3 Disclosures as at 31 December 2020', p.15 (section 4.5 'Capital adequacy' - "
        f"Total RWAs/Capital base/Tier 1 capital/Tier 1 ratio/Total Capital ratio table) and p.34 (section 7 "
        f"'Leverage' - reconciliation table) - {P3_2020_URL}. This is the only surviving (non-404) Wayback "
        f"capture of this document and is itself truncated by the Wayback Machine's own playback service at "
        f"exactly 1,048,576 bytes; it was repaired with `qpdf --qdf --replace-input` (rebuilds the cross-"
        f"reference table from the recoverable object streams) before reading - see the Cash Flow sheet's "
        f"ENTITY NOTE for the full data-quality account of this repair.\n"
        "FY2025: not yet published as at the time of this workbook's research."
    )


bw = BankWorkbook(bank_name="Gulf International Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="38AD47")

STATEMENTS_SOURCES = (
    "Sources - Gulf International Bank (UK) Limited's own Statement of Financial Position / Statement of "
    "Income (converted from USD to £, see FX conversion note below), transcribed from Companies House filings "
    "(FY2024/FY2023 text-native; FY2022/FY2021/FY2020 scanned/image-only, no text layer):\n"
    f"FY2024/FY2023: Annual Report and Financial Statements 2024, pp.105-108 (Statement of Financial Position, "
    f"Statement of Income, Statement of Comprehensive Income, Statement of Changes in Equity) - {AR2024_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2023, pp.67-70 (own FY2022 comparative column) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, pp.48-51 - {AR2021_URL}\n"
    f"FY2020: Annual Report and Financial Statements 2020, pp.25-28 (Statement of Financial Position p.25, "
    f"Income Statement p.26, Statement of Comprehensive Income p.27, Statement of Changes in Equity p.28) - "
    f"{AR2020_URL}\n"
    "FY2025 is blank throughout: no FY2025 Annual Report has been filed with Companies House yet.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet (raw USD, then converted via stock())
# ---------------------------------------------------------------
balance_sheet_rows_usd = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2024": 7378636, "FY2023": 14883184, "FY2022": 5325978, "FY2021": 5599337, "FY2020": 5069290}),
    ("DATA", "Placements with banks", {"FY2024": 5666838, "FY2023": 5290351, "FY2022": 3661166, "FY2021": 3805701, "FY2020": 4988056}),
    ("DATA", "Investment in group entities", {"FY2020": 341}),
    ("DATA", "Trading securities", {"FY2024": 141808, "FY2023": 111752, "FY2022": 73490, "FY2021": 56471, "FY2020": 33405}),
    ("DATA", "Derivative financial asset", {"FY2024": 89160, "FY2023": 73778, "FY2022": 69607, "FY2021": 22397, "FY2020": 15196}),
    ("DATA", "Debt securities at amortised cost", {"FY2024": 1015473, "FY2023": 969443, "FY2022": 983131, "FY2021": 1001816, "FY2020": 277194}),
    ("DATA", "Property, plant and equipment", {"FY2024": 2762, "FY2023": 3363, "FY2022": 3915, "FY2021": 5087, "FY2020": 1390}),
    ("DATA", "Right-of-use assets", {"FY2024": 21499, "FY2023": 23857, "FY2022": 25740, "FY2021": 28260, "FY2020": 31706}),
    ("DATA", "Other assets", {"FY2024": 182679, "FY2023": 207336, "FY2022": 115596, "FY2021": 56297, "FY2020": 43583}),
    ("DATA", "Current tax asset", {"FY2022": 918, "FY2021": 1026, "FY2020": 2483}),
    ("TOTAL", "Total assets", {"FY2024": 14498855, "FY2023": 21563064, "FY2022": 10259541, "FY2021": 10576392, "FY2020": 10462644}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2024": 1159003, "FY2023": 76401, "FY2022": 370965, "FY2021": 35438, "FY2020": 180064}),
    ("DATA", "Deposits from customers", {"FY2024": 12755439, "FY2023": 20851700, "FY2022": 9323428, "FY2021": 10022108, "FY2020": 9774293}),
    ("DATA", "Derivative financial liability", {"FY2024": 7739, "FY2023": 50031, "FY2022": 43543, "FY2021": 54878, "FY2020": 65930}),
    ("DATA", "Deferred tax liability", {"FY2024": 6226, "FY2023": 12219, "FY2022": 5032, "FY2021": 1851}),
    ("DATA", "Other liabilities", {"FY2024": 109076, "FY2023": 113887, "FY2022": 97890, "FY2021": 55256, "FY2020": 49761}),
    ("DATA", "Current tax liabilities", {"FY2024": 1546, "FY2023": 775}),
    ("TOTAL", "Total liabilities", {"FY2024": 14039029, "FY2023": 21105013, "FY2022": 9840858, "FY2021": 10169531, "FY2020": 10070048}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2024": 250000, "FY2023": 250000, "FY2022": 250000, "FY2021": 250000, "FY2020": 250000}),
    ("DATA", "Capital contribution", {"FY2024": 2279, "FY2023": 2279, "FY2022": 2279, "FY2021": 2279, "FY2020": 2279}),
    ("DATA", "Cashflow hedge reserve", {"FY2024": 1928}),
    ("DATA", "Pension reserves", {"FY2024": 8724, "FY2023": 32878, "FY2022": 33390, "FY2021": 28678, "FY2020": 7473}),
    ("DATA", "Retained earnings", {"FY2024": 196895, "FY2023": 172894, "FY2022": 133014, "FY2021": 125904, "FY2020": 132844}),
    ("TOTAL", "Total equity", {"FY2024": 459826, "FY2023": 458051, "FY2022": 418683, "FY2021": 406861, "FY2020": 392596}),
    ("TOTAL", "Total liabilities and equity", {"FY2024": 14498855, "FY2023": 21563064, "FY2022": 10259541, "FY2021": 10576392, "FY2020": 10462644}),
]

balance_sheet_rows = [
    (kind, label, {} if kind == "SECTION" else stock(usd))
    for kind, label, usd in balance_sheet_rows_usd
]

bw.add_balance_sheet_sheet(
    title="Gulf International Bank (UK) Limited — Statement of Financial Position",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used. FY2025 blank (no FY2025 Annual Report filed yet).",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (raw USD, then converted via flow())
# ---------------------------------------------------------------
income_statement_rows_usd = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income from financial instruments at amortised cost", {"FY2024": 1030743, "FY2023": 702928, "FY2022": 222570, "FY2021": 27749, "FY2020": 66271}),
    ("DATA", "Other interest income/(expense)", {"FY2024": 30875, "FY2023": 57071, "FY2022": 399, "FY2021": -6645, "FY2020": -12565}),
    ("DATA", "Interest expense from financial instruments at amortised cost", {"FY2024": -987369, "FY2023": -679131, "FY2022": -184447, "FY2021": -9043, "FY2020": -39415}),
    ("TOTAL", "Net interest income", {"FY2024": 74249, "FY2023": 80868, "FY2022": 38522, "FY2021": 12061, "FY2020": 14291}),
    ("DATA", "Net fee and commission income", {"FY2024": 5455, "FY2023": 3415, "FY2022": 2128, "FY2021": 4036, "FY2020": 5188}),
    ("DATA", "Net trading income/(loss)", {"FY2024": 5358, "FY2023": 7376, "FY2022": 4753, "FY2021": 3371, "FY2020": -4106}),
    ("DATA", "Foreign exchange income and revaluation of foreign currencies", {"FY2024": 8150, "FY2023": 15526, "FY2022": 11764, "FY2021": 10845, "FY2020": 10204}),
    ("DATA", "Expected credit loss charge/(release) on financial assets", {"FY2024": 166, "FY2023": -199, "FY2022": -140, "FY2021": -162, "FY2020": -149}),
    ("DATA", "Other operating income/(loss)", {"FY2024": 4133, "FY2023": 2852, "FY2022": 4801, "FY2021": 491, "FY2020": -5803}),
    ("DATA", "Impairment of right-of-use asset", {"FY2021": -1199}),
    ("DATA", "Operating expenses", {"FY2024": -65407, "FY2023": -57344, "FY2022": -52682, "FY2021": -43014, "FY2020": -38820}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2024": 32104, "FY2023": 52494, "FY2022": 9146, "FY2021": -13571, "FY2020": -19195}),
    ("DATA", "Income tax (expense)/credit", {"FY2024": -8103, "FY2023": -12614, "FY2022": -2036, "FY2021": 6631, "FY2020": 2416}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2024": 24001, "FY2023": 39880, "FY2022": 7110, "FY2021": -6940, "FY2020": -16779}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Net movement in cash flow hedge reserve", {"FY2024": 2571}),
    ("DATA", "Tax relating to cash flow hedge reserve", {"FY2024": -643}),
    ("DATA", "Remeasurement of defined benefit pension fund", {"FY2024": -32186, "FY2023": -426, "FY2022": 6016, "FY2021": 28694, "FY2020": 17500}),
    ("DATA", "Tax relating to defined benefit pension", {"FY2024": 8032, "FY2023": -86, "FY2022": -1304, "FY2021": -7489, "FY2020": -2451}),
    ("TOTAL", "Other comprehensive income for the year, net of tax", {"FY2024": -22226, "FY2023": -512, "FY2022": 4712, "FY2021": 21205, "FY2020": 15049}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2024": 1775, "FY2023": 39368, "FY2022": 11822, "FY2021": 14265, "FY2020": -1730}),
]
income_statement_rows = [
    (kind, label, {} if kind == "SECTION" else flow(usd))
    for kind, label, usd in income_statement_rows_usd
]

bw.add_income_statement_sheet(
    title="Gulf International Bank (UK) Limited — Statement of Income",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used. FY2025 blank (no FY2025 Annual Report filed yet).",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity - built year-by-year per the map's
# per-year reconciliation ladder: each TOTAL "At 31 December YYYY" row below
# was checked to tie to (a) its own component's Balance Sheet figure above
# and (b) the following year's own opening row, in USD, before conversion.
# A "FX translation effect on equity, net" plug row (Total column only,
# computed as the balancing figure) makes each year's roll-forward tie
# exactly in GBP too, since opening/movement/closing convert at different
# point-in-time rates (same pattern as this entity's own Cash Flow FX plug).
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Capital contribution", "Pension reserve", "Cashflow hedge reserve", "Retained earnings", "Total equity"]
EQUITY_ROWS_USD = [
    ("TOTAL", "At 1 January 2020", [250000, 2279, -7576, None, 149480, 394183], "spot", "FY2019"),
    ("DATA", "Opening adjustment - GIBUK/GIB AM income reclassification (FY2020)", [None, None, None, None, 143, 143], "avg", "FY2020"),
    ("DATA", "Deferred tax liability on defined benefit pension (FY2020)", [None, None, -2451, None, None, -2451], "avg", "FY2020"),
    ("DATA", "Pension reserves (FY2020)", [None, None, 17500, None, None, 17500], "avg", "FY2020"),
    ("TOTAL", "Total other comprehensive income (FY2020)", [None, None, 15049, None, None, 15049], "avg", "FY2020"),
    ("DATA", "Net loss for the year (FY2020)", [None, None, None, None, -16779, -16779], "avg", "FY2020"),
    ("TOTAL", "Total comprehensive income for the year (FY2020)", [None, None, 15049, None, -16779, -1730], "avg", "FY2020"),
    ("DATA", "FX translation effect on equity, net (FY2020)", [None, None, None, None, None, None], "plug", "FY2020"),
    ("TOTAL", "At 31 December 2020", [250000, 2279, 7473, None, 132844, 392596], "spot", "FY2020"),

    ("DATA", "Deferred tax liability on defined benefit pension (FY2021)", [None, None, -7489, None, None, -7489], "avg", "FY2021"),
    ("DATA", "Pension reserves (FY2021)", [None, None, 28694, None, None, 28694], "avg", "FY2021"),
    ("TOTAL", "Total other comprehensive income (FY2021)", [None, None, 21205, None, None, 21205], "avg", "FY2021"),
    ("DATA", "Net loss for the year (FY2021)", [None, None, None, None, -6940, -6940], "avg", "FY2021"),
    ("TOTAL", "Total comprehensive income for the year (FY2021)", [None, None, 21205, None, -6940, 14265], "avg", "FY2021"),
    ("DATA", "FX translation effect on equity, net (FY2021)", [None, None, None, None, None, None], "plug", "FY2021"),
    ("TOTAL", "At 31 December 2021", [250000, 2279, 28678, None, 125904, 406861], "spot", "FY2021"),

    ("DATA", "Deferred tax liability on defined benefit pension (FY2022)", [None, None, -1304, None, None, -1304], "avg", "FY2022"),
    ("DATA", "Pension reserves (FY2022)", [None, None, 6016, None, None, 6016], "avg", "FY2022"),
    ("TOTAL", "Total other comprehensive income (FY2022)", [None, None, 4712, None, None, 4712], "avg", "FY2022"),
    ("DATA", "Net profit for the year (FY2022)", [None, None, None, None, 7110, 7110], "avg", "FY2022"),
    ("TOTAL", "Total comprehensive income for the year (FY2022)", [None, None, 4712, None, 7110, 11822], "avg", "FY2022"),
    ("DATA", "FX translation effect on equity, net (FY2022)", [None, None, None, None, None, None], "plug", "FY2022"),
    ("TOTAL", "At 31 December 2022", [250000, 2279, 33390, None, 133014, 418683], "spot", "FY2022"),

    ("DATA", "Deferred tax liability on defined benefit pension (FY2023)", [None, None, -86, None, None, -86], "avg", "FY2023"),
    ("DATA", "Pension reserves (FY2023)", [None, None, -426, None, None, -426], "avg", "FY2023"),
    ("TOTAL", "Total other comprehensive income (FY2023)", [None, None, -512, None, None, -512], "avg", "FY2023"),
    ("DATA", "Net profit for the year (FY2023)", [None, None, None, None, 39880, 39880], "avg", "FY2023"),
    ("TOTAL", "Total comprehensive income for the year (FY2023)", [None, None, -512, None, 39880, 39368], "avg", "FY2023"),
    ("DATA", "FX translation effect on equity, net (FY2023)", [None, None, None, None, None, None], "plug", "FY2023"),
    ("TOTAL", "At 31 December 2023", [250000, 2279, 32878, None, 172894, 458051], "spot", "FY2023"),

    ("DATA", "Pension reserves (FY2024)", [None, None, -32186, None, None, -32186], "avg", "FY2024"),
    ("DATA", "Deferred tax liability on defined benefit pension (FY2024)", [None, None, 8032, None, None, 8032], "avg", "FY2024"),
    ("DATA", "Net movement in cash flow hedge reserve (FY2024)", [None, None, None, 2571, None, 2571], "avg", "FY2024"),
    ("DATA", "Tax relating to cash flow hedge reserve (FY2024)", [None, None, None, -643, None, -643], "avg", "FY2024"),
    ("TOTAL", "Total other comprehensive income (FY2024)", [None, None, -24154, 1928, None, -22226], "avg", "FY2024"),
    ("DATA", "Net profit for the year (FY2024)", [None, None, None, None, 24001, 24001], "avg", "FY2024"),
    ("TOTAL", "Total comprehensive income for the year (FY2024)", [None, None, -24154, 1928, 24001, 1775], "avg", "FY2024"),
    ("DATA", "FX translation effect on equity, net (FY2024)", [None, None, None, None, None, None], "plug", "FY2024"),
    ("TOTAL", "At 31 December 2024", [250000, 2279, 8724, 1928, 196895, 459826], "spot", "FY2024"),
]


def _rate(rtype, ry):
    return FX_SPOT[ry] if rtype == "spot" else FX_AVG[ry]


_equity_totals_usd = {}
for _kind, _label, _vals, _rtype, _ry in EQUITY_ROWS_USD:
    if _kind == "TOTAL" and _rtype == "spot":
        _equity_totals_usd[_label] = _vals

EXTRA_MOVEMENT_LABELS = {
    # FY2020's roll-forward includes a one-off retained-earnings reclassification
    # adjustment (see source note) that is not itself part of "Total comprehensive
    # income" - it must be folded into the movement sum below, else the FX plug
    # would silently absorb it as if it were a currency-translation effect.
    "FY2020": ["Opening adjustment - GIBUK/GIB AM income reclassification (FY2020)"],
}

FX_PLUG_GBP = {}
for _ry in ["FY2020", "FY2021", "FY2022", "FY2023", "FY2024"]:
    _prev_year = PREV_YEAR[_ry]
    _open_label = "At 1 January 2020" if _ry == "FY2020" else f"At 31 December {int(_prev_year[2:])}"
    _close_label = f"At 31 December {int(_ry[2:])}"
    _opening_gbp = round(_equity_totals_usd[_open_label][-1] / FX_SPOT[_prev_year] / 1000, 1)
    _closing_gbp = round(_equity_totals_usd[_close_label][-1] / FX_SPOT[_ry] / 1000, 1)
    _movement_gbp = round(
        sum(
            v[-1] for k, l, v, rt, ry in EQUITY_ROWS_USD
            if ry == _ry and rt == "avg"
            and (
                (k == "TOTAL" and l.startswith("Total comprehensive income"))
                or l in EXTRA_MOVEMENT_LABELS.get(_ry, [])
            )
        ) / FX_AVG[_ry] / 1000,
        1,
    )
    FX_PLUG_GBP[_ry] = round(_closing_gbp - _opening_gbp - _movement_gbp, 1)

equity_changes_rows = []
for kind, label, vals, rtype, ry in EQUITY_ROWS_USD:
    if rtype == "plug":
        row_vals = [None] * (len(EQUITY_HEADERS) - 1) + [FX_PLUG_GBP[ry]]
    else:
        rate = _rate(rtype, ry)
        row_vals = [None if v is None else round(v / rate / 1000, 1) for v in vals]
    equity_changes_rows.append((kind, label, row_vals))

EQUITY_SOURCES = (
    STATEMENTS_SOURCES + "\n\n"
    "FX METHODOLOGY FOR THIS SHEET: opening/closing balances converted at that year-end's spot rate, movement "
    "lines at that year's average rate - the same convention used throughout this workbook. Converting stocks "
    "and flows at different rates within one year means the roll-forward doesn't tie exactly in GBP even though "
    "it ties exactly in USD (independently verified against each year's own source table before conversion) - "
    "an explicit 'FX translation effect on equity, net' row (Total column only, computed as the balancing "
    "figure) is included each year, same treatment as this entity's own Cash Flow Statement's 'Effect of "
    "GBP/USD translation' line. Zero plug rows were needed in USD terms - every year's own closing balance ties "
    "exactly to both the next year's own opening balance and that year's Balance Sheet Total equity.\n\n"
    "FY2020 has one additional wrinkle, disclosed in the Annual Report and Financial Statements 2020's own "
    "Statement of Changes in Equity footnote (p.28): a $143k 'Opening adjustment' to retained earnings, "
    "explained as 'in relation to the classification error whereby the 2019 GIBUK income had been classified as "
    "GIB AIM income. This had been corrected at the time of the preparation of prior year GIB AIM financial "
    "statements. Given these financial statements are prepared on a standalone basis, therefore it has been "
    "disclosed as an opening adjustment.' Included in this sheet as its own row (converted at FY2020's average "
    "rate, folded into the FX-plug movement calculation so it isn't mistaken for a currency-translation effect) "
    "- USD ties exactly: $394,183k (1 Jan 2020) + $143k (adjustment) + -$1,730k (total comprehensive loss) = "
    "$392,596k (31 Dec 2020), matching both the Balance Sheet's own Total equity and the FY2021 roll-forward's "
    "own opening balance."
)

bw.add_equity_changes_sheet(
    title="Gulf International Bank (UK) Limited — Statement of Changes in Equity",
    subtitle="£'000, converted from USD - chronological, oldest to newest. See source note for FX methodology.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=56,
    source_height=340,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD, then converted via flow()/stock()/opening_cash())
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2024": 32104, "FY2023": 52494, "FY2022": 9146, "FY2021": -13571, "FY2020": -19195}),
    ("DATA", "Income tax (paid)/received", {"FY2024": -6050, "FY2023": -3870, "FY2022": 0, "FY2021": 2400, "FY2020": -1049}),
    ("DATA", "Depreciation of property and equipment", {"FY2024": 902, "FY2023": 1060, "FY2022": 1211, "FY2021": 1270, "FY2020": 1320}),
    ("DATA", "Depreciation of ROU assets", {"FY2024": 2358, "FY2023": 1883, "FY2022": 2520, "FY2021": 2247, "FY2020": 2121}),
    ("DATA", "Change in accrued interest receivable", {"FY2024": -4050, "FY2023": -90461, "FY2022": -47278, "FY2021": 10789, "FY2020": 8386}),
    ("DATA", "Change in accrued interest payable", {"FY2024": -4230, "FY2023": 7017, "FY2022": 45097, "FY2021": -649, "FY2020": -6604}),
    ("DATA", "Change in other net assets (incl. movements to pension reserve)", {"FY2023": 11798, "FY2022": -68074, "FY2021": -7360, "FY2020": 38153}),
    ("DATA", "Change in other operating assets and liabilities", {"FY2024": -56920}),
    ("DATA", "Change in trading securities", {"FY2024": -30056, "FY2023": -38262, "FY2022": -17018, "FY2021": -23066, "FY2020": -5937}),
    ("DATA", "Change in placements with banks", {"FY2024": -376341, "FY2023": -1629689, "FY2022": 144535, "FY2021": 994557, "FY2020": -226199}),
    ("DATA", "Change in debt securities at amortised cost/investment securities net", {"FY2023": 13993, "FY2022": 18566, "FY2021": -724622, "FY2020": -99922}),
    ("DATA", "Change in debt securities at amortised cost", {"FY2024": -46010}),
    ("DATA", "Change in deposits from banks", {"FY2024": 1179214, "FY2023": -536019, "FY2022": 893757, "FY2021": -144626, "FY2020": -631458}),
    ("DATA", "Change in deposits from customers", {"FY2024": -8096261, "FY2023": 11528272, "FY2022": -698680, "FY2021": 247815, "FY2020": -665755}),
    ("DATA", "Finance costs (lease liability)", {"FY2024": 1058, "FY2023": 1093, "FY2022": 1125}),
    ("DATA", "Finance costs (lease liability) and FX loss on reval of lease liability", {"FY2021": 940, "FY2020": 3466}),
    ("DATA", "Impairment", {"FY2024": -166, "FY2023": 199, "FY2022": 119, "FY2021": 1199}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities", {"FY2024": -7404448, "FY2023": 9319508, "FY2022": 287025, "FY2021": 347323, "FY2020": -1602673}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Net purchase of property and equipment", {"FY2024": -302, "FY2023": -508, "FY2022": -39, "FY2021": -4966, "FY2020": -735}),
    ("TOTAL", "Net cash used in investing activities", {"FY2024": -302, "FY2023": -508, "FY2022": -39, "FY2021": -4966, "FY2020": -735}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Payment of principal portion of lease liabilities", {"FY2024": -3186, "FY2023": -3249, "FY2022": -2115, "FY2021": -108, "FY2020": -808}),
    ("TOTAL", "Net cash used in financing activities", {"FY2024": -3186, "FY2023": -3249, "FY2022": -2115, "FY2021": -108, "FY2020": -808}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2024": -7407936, "FY2023": 9315751, "FY2022": 284871, "FY2021": 342249, "FY2020": -1604216}),
    ("DATA", "Net foreign exchange difference (as reported, USD)", {"FY2024": -96612, "FY2023": 241455, "FY2022": -558230}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2024": 14883184, "FY2023": 5325978, "FY2022": 5599337, "FY2021": 5257088, "FY2020": 6861304}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2024": 7378636, "FY2023": 14883184, "FY2022": 5325978, "FY2021": 5599337, "FY2020": 5257088}),
]

_usd_by_label = {label: usd for _, label, usd in rows_usd}
rows = []
for kind, label, usd in rows_usd:
    if kind == "SECTION":
        rows.append((kind, label, {}))
    elif label == "Cash and cash equivalents at beginning of year":
        rows.append((kind, label, opening_cash(usd)))
    elif label == "Cash and cash equivalents at end of year":
        rows.append((kind, label, stock(usd)))
    else:
        rows.append((kind, label, flow(usd)))
    if label == "Net foreign exchange difference (as reported, USD)":
        # £ translation plug (see FX_NOTE): stocks (opening/closing) and flows
        # (everything else) are converted at different rates, so the £ statement
        # needs an explicit reconciling line to tie exactly. Computed programmatically
        # from the actual converted figures, per year, so it can never drift out of
        # sync with the rates above.
        opening_gbp = opening_cash(_usd_by_label["Cash and cash equivalents at beginning of year"])
        closing_gbp = stock(_usd_by_label["Cash and cash equivalents at end of year"])
        net_change_gbp = flow(_usd_by_label["Net (decrease)/increase in cash and cash equivalents"])
        fx_gbp = flow(usd)
        plug = {
            y: round(closing_gbp[y] - opening_gbp[y] - net_change_gbp[y] - fx_gbp.get(y, 0), 1)
            for y in closing_gbp
        }
        rows.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", plug))

bw.add_cash_flow_sheet(
    title="Gulf International Bank (UK) Limited — Statement of Cash Flow",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used. FY2025 blank (no FY2025 Annual Report filed yet).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality - GIB UK does not lend to customers (its own filings
# confirm no "Loans and advances to customers" line exists anywhere on the
# Balance Sheet); credit risk sits in Placements with banks (Note 4) and
# Debt securities at amortised cost (Note 6), each with their own IFRS 9
# stage/internal-rating table. Every year, both are 100% Stage 1 /
# Investment grade 1-4 - confirmed by reading each note in full, not
# assumed from the aggregate ECL charge being small.
# ---------------------------------------------------------------
asset_quality_rows_usd = [
    ("SECTION", "Placements with banks - gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (Investment grade 1-4)", {"FY2024": 5667335, "FY2023": 5290994, "FY2022": 3661305, "FY2021": 3805820, "FY2020": 4988141}),
    ("DATA", "Stage 2 (Sub-investment grade 5-7)", {}),
    ("DATA", "Stage 3 (Classified 8-10)", {}),
    ("TOTAL", "Total gross placements with banks", {"FY2024": 5667335, "FY2023": 5290994, "FY2022": 3661305, "FY2021": 3805820, "FY2020": 4988141}),
    ("DATA", "Less: allowance for impairment losses", {"FY2024": -497, "FY2023": -643, "FY2022": -139, "FY2021": -119, "FY2020": -85}),
    ("TOTAL", "Net placements with banks", {"FY2024": 5666838, "FY2023": 5290351, "FY2022": 3661166, "FY2021": 3805701, "FY2020": 4988056}),
    ("SECTION", "Debt securities at amortised cost - gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (Investment grade 1-4)", {"FY2024": 1015473, "FY2023": 969443, "FY2022": 983625, "FY2021": 1002191, "FY2020": 277441}),
    ("DATA", "Stage 2 (Sub-investment grade 5-7)", {}),
    ("DATA", "Stage 3 (Classified 8-10)", {}),
    ("TOTAL", "Total gross debt securities at amortised cost", {"FY2024": 1015473, "FY2023": 969443, "FY2022": 983625, "FY2021": 1002191, "FY2020": 277441}),
    ("DATA", "Less: allowance for impairment losses", {"FY2024": -20, "FY2023": -305, "FY2022": -494, "FY2021": -375, "FY2020": -247}),
    ("TOTAL", "Net debt securities at amortised cost", {"FY2024": 1015473, "FY2023": 969443, "FY2022": 983131, "FY2021": 1001816, "FY2020": 277194}),
]
asset_quality_rows = [
    (kind, label, {} if kind == "SECTION" else stock(usd))
    for kind, label, usd in asset_quality_rows_usd
]
# Coverage ratios - genuinely trivial (0.00-0.04%) given every asset is
# Stage 1/Investment grade; computed from the USD figures directly (a
# dimensionless ratio, so FX conversion doesn't change it).
_placements_gross_usd = {"FY2024": 5667335, "FY2023": 5290994, "FY2022": 3661305, "FY2021": 3805820, "FY2020": 4988141}
_placements_ecl_usd = {"FY2024": 497, "FY2023": 643, "FY2022": 139, "FY2021": 119, "FY2020": 85}
_debt_sec_gross_usd = {"FY2024": 1015473, "FY2023": 969443, "FY2022": 983625, "FY2021": 1002191, "FY2020": 277441}
_debt_sec_ecl_usd = {"FY2024": 20, "FY2023": 305, "FY2022": 494, "FY2021": 375, "FY2020": 247}
asset_quality_rows.append((
    "DATA", "Placements with banks - ECL coverage ratio",
    {y: f"{_placements_ecl_usd[y] / _placements_gross_usd[y] * 100:.3f}%" for y in _placements_gross_usd},
))
asset_quality_rows.append((
    "DATA", "Debt securities - ECL coverage ratio",
    {y: f"{_debt_sec_ecl_usd[y] / _debt_sec_gross_usd[y] * 100:.3f}%" for y in _debt_sec_gross_usd},
))

ASSET_QUALITY_SOURCES = (
    "Sources - Gulf International Bank (UK) Limited's own Note 4 (Placements with banks) / Note 6 (Debt "
    "securities at amortised cost) IFRS 9 stage and internal-credit-rating tables, converted from USD to £ (see "
    "FX conversion note on the Cash Flow Statement sheet):\n"
    f"FY2024/FY2023: Annual Report and Financial Statements 2024, pp.124-128 (Notes 4, 4.1, 6, 6.1) - {AR2024_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2023, pp.87-93 (Notes 4, 4.1, 6, 6.1, own FY2022 "
    f"comparative) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, pp.68-70 (Notes 4, 4.1, 6, 6.1) - {AR2021_URL}\n"
    f"FY2020: Annual Report and Financial Statements 2020, pp.46-50 (Notes 4, 4.1 Placements with banks; Note 6, "
    f"6.1 'Financial investments other than those measured at FVTPL' - FY2020's own note numbering/title for "
    f"what later years call 'Debt securities at amortised cost') - {AR2020_URL}\n\n"
    "GIB UK does not lend to customers - confirmed by reading: there is no 'Loans and advances to customers' "
    "line anywhere in the Balance Sheet across all 5 years reviewed. Its credit risk instead sits entirely in "
    "Placements with banks and Debt securities at amortised cost, each disclosed on the Bank's own internal "
    "credit rating scale (Investment grade 1-4 / Sub-investment grade 5-7 / Classified 8-10) cross-referenced "
    "to IFRS 9 stage. Every year, both asset classes are 100% Stage 1 / Investment grade 1-4, with no transfers "
    "to Stage 2 or 3 disclosed in any year - confirmed by reading each note in full, not assumed from the small "
    "ECL charge. ECL coverage ratios are correspondingly minimal (well under 0.1%).\n\n"
    + ENTITY_NOTE
)

bw.add_asset_quality_sheet(
    title="Gulf International Bank (UK) Limited — Asset Quality",
    subtitle="£'000, converted from USD - see source note. GIB UK does not lend to customers; credit risk sits in Placements with banks and Debt securities at amortised cost.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=140)


CAPITAL_USD = {"FY2024": 435465, "FY2023": 411658, "FY2022": 368416, "FY2021": 371866, "FY2020": 393000}
RWA_USD = {"FY2024": 1963743, "FY2023": 1809984, "FY2022": 1557567, "FY2021": 1932234, "FY2020": 1482000}
CAPITAL_RATIO = {"FY2024": "22.18%", "FY2023": "22.74%", "FY2022": "23.65%", "FY2021": "19.22%", "FY2020": "26.48%"}

metric("CET1 Capital", "£'000 (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", stock(CAPITAL_USD))], p3_sources(),
       note="GIB UK's regulatory capital consists entirely of CET1 (fully paid-up ordinary shares, capital contribution, and audited retained earnings/reserves) - no AT1 or Tier 2 instruments in any year. FY2020's Basel II-era Pillar 3 document calls this figure 'Total regulatory capital' (comprising Share Capital $250m + Retained Earnings $143m = $393m, Tier 1 only, no Tier 2) rather than 'CET1' by name, but is the same underlying capital base.")
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CAPITAL_RATIO)], p3_sources())
metric("Tier 1 Capital", "£'000 (conv. from USD)", [("Tier 1 capital", stock(CAPITAL_USD))], p3_sources(),
       note="Equal to CET1 capital in every year - the Bank holds no Additional Tier 1 (AT1) instruments.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CAPITAL_RATIO)], p3_sources())
metric("Total Capital", "£'000 (conv. from USD)", [("Total capital", stock(CAPITAL_USD))], p3_sources(),
       note="Equal to CET1/Tier 1 capital in every year - the Bank holds no AT1 or Tier 2 instruments.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", CAPITAL_RATIO)], p3_sources())
metric("Total RWAs", "£'000 (conv. from USD)", [("Total risk-weighted exposure amount", stock(RWA_USD))], p3_sources())

# ---------------------------------------------------------------
# RWA Breakdown (UK OV1) - fully disclosed all 4 later years. FY2024/FY2023 from
# the Bank's own FY2024 Pillar 3 document (text-native); FY2022 from its
# own FY2023 Pillar 3 document; FY2021 sourced from that same FY2023
# Pillar 3 document's own T-4/prior-year comparative column (matches this
# project's existing convention, e.g. p3_sources() already does this for
# other metrics) rather than the dedicated FY2021 Pillar 3 document, since
# both give identical figures where legible. Each year's own Total ties
# exactly to the Total RWAs sheet above.
#
# FY2020 predates the UK OV1 template entirely - it's a Basel II-style
# disclosure with separate Credit risk / Market risk / Operational risk
# sections (section 4 of that document) and no CCR/CVA breakout at all (the
# document's own credit-risk table folds any counterparty exposure into the
# single Credit risk total). Market risk RWA ($143.75m) is stated directly;
# Operational risk RWA is not stated directly - only its capital requirement
# ($10.3m) is - so it's derived here as capital requirement x 12.5 (the same
# multiplier the document itself uses to turn market risk's capital
# requirement into an RWA figure, per its own section 4.2 methodology
# description). Summing the three derived FY2020 components (1,206.0 +
# 143.75 + 128.75 = 1,478.5) falls short of the document's own separately
# reported Total RWAs of $1,482m by $3.5m (~0.24%) - not traceable to a
# specific line (each component was independently re-checked against the
# source image/text); flagged rather than forced to reconcile, per this
# project's convention for unexplained source-side gaps.
# ---------------------------------------------------------------
rwa_breakdown_rows_usd = [
    ("SECTION", "Credit risk", {}),
    ("DATA", "Credit risk (excluding CCR) - standardised approach", {"FY2024": 1704126, "FY2023": 1588788, "FY2022": 1426851, "FY2021": 1633319, "FY2020": 1206000}),
    ("SECTION", "Counterparty credit risk", {}),
    ("DATA", "Of which credit valuation adjustment (CVA)", {"FY2024": 15040, "FY2023": 20994, "FY2022": 20625, "FY2021": 12553}),
    ("DATA", "Of which other CCR", {"FY2024": 45049, "FY2023": 39716, "FY2022": 21799, "FY2021": 23092}),
    ("TOTAL", "Total counterparty credit risk - CCR", {"FY2024": 60089, "FY2023": 60709, "FY2022": 42424, "FY2021": 35645}),
    ("SECTION", "Market risk", {}),
    ("DATA", "Position, foreign exchange and commodities risks - standardised approach", {"FY2024": 819, "FY2023": 11263, "FY2022": 2332, "FY2021": 166380, "FY2020": 143750}),
    ("SECTION", "Operational risk", {}),
    ("DATA", "Operational risk - standardised approach", {"FY2024": 198710, "FY2023": 149224, "FY2022": 85961, "FY2021": 96890, "FY2020": 128750}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2024": 1963743, "FY2023": 1809984, "FY2022": 1557567, "FY2021": 1932234, "FY2020": 1482000}),
]
rwa_breakdown_rows = [
    (kind, label, {} if kind == "SECTION" else stock(usd))
    for kind, label, usd in rwa_breakdown_rows_usd
]

RWA_BREAKDOWN_SOURCES = (
    "Sources - Gulf International Bank (UK) Limited's own UK OV1 (Pillar 1 capital requirements) table (FY2021 "
    "onward) / Basel II-style capital requirements tables (FY2020 - see note below), converted from USD to £ "
    "(see FX conversion note on the Cash Flow Statement sheet; the underlying $ RWA figures are unconverted "
    "regulatory exposure amounts, converted here at spot rate for consistency with the rest of this workbook):\n"
    f"FY2024/FY2023: Pillar 3 Disclosures as at 31 December 2024 (Board-approved), pp.27-28 (section 6.2, UK "
    f"OV1) - {P3_2024_URL}\n"
    f"FY2022/FY2021: Pillar 3 Disclosures as at 31 December 2022, pp.26-27 (section 6.2, UK OV1) - FY2021 is "
    f"that document's own T-4/prior-year comparative column - {P3_2022_URL}\n"
    f"FY2020: 'Basel II Pillar 3 Disclosures as at 31 December 2020', pp.13-15 (sections 4.1 Credit risk RWA "
    f"table, 4.2 Market risk RWA table, 4.3 Operational risk capital requirement) - {P3_2020_URL}. FY2020 "
    "predates the UK OV1 template and has no CCR/CVA breakout - the Operational risk RWA is derived (capital "
    "requirement x 12.5) rather than stated directly; the 3 derived FY2020 components sum to $3.5m (~0.24%) "
    "short of the document's own separately reported Total RWAs, an unexplained source-side gap flagged rather "
    "than forced to reconcile.\n\n"
    + ENTITY_NOTE
)

bw.add_rwa_breakdown_sheet(
    title="Gulf International Bank (UK) Limited — RWA Breakdown",
    subtitle="£'000, converted from USD - see source note. UK OV1 template.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£'000, conv. from USD)",
)

metric(
    "Leverage Ratio", "£'000 / % (conv. from USD)",
    [
        ("Total exposure measure", stock({
            "FY2024": 8682283, "FY2023": 7795728, "FY2022": 5136739, "FY2021": 10573209, "FY2020": 8524000,
        })),
        ("Leverage ratio (%)", {"FY2024": "5.02%", "FY2023": "5.28%", "FY2022": "7.17%", "FY2021": "3.52%", "FY2020": "4.61%"}),
    ],
    p3_sources(),
    note="Basis change: FY2022 onward reports 'Total exposure measure EXCLUDING claims on central banks' (the "
         "Bank's own FY2021 report states it was 'not, currently, in scope of the UK Leverage Framework' that "
         "introduced this exclusion, effective 1 January 2022); FY2021/FY2020's figures are the single "
         "(unqualified) leverage ratio/exposure measure as originally reported those years, likely on an "
         "including-central-bank-claims basis. Each year's own as-reported figure is used rather than forcing a "
         "common basis. FY2020's own document reconciles this exposure measure directly from Total Assets per "
         "the Financial Statements ($10,463m) less securities-financing-transaction credit risk mitigation "
         "($1,928m) plus derivative add-ons ($25m) and other adjustments (-$35m) = $8,524m.",
)

metric(
    "LCR", "£'000 / % (conv. from USD)",
    [
        ("Total high-quality liquid assets (HQLA / average liquid assets buffer)", stock({
            "FY2024": 8650825, "FY2023": 15980246, "FY2022": 9198733, "FY2021": 6737809, "FY2020": 5860000,
        })),
        ("Total net cash outflows, adjusted value", stock({
            "FY2024": 3021360, "FY2023": 5579776, "FY2022": 2597379, "FY2020": 2019000,
        })),
        ("Liquidity Coverage Ratio (%)", {"FY2024": "286.32%", "FY2023": "286.40%", "FY2022": "354.15%", "FY2021": "480.13%", "FY2020": "290%"}),
    ],
    p3_sources(),
    note="Methodology differs for FY2021: that year's Pillar 3 report discloses LCR as a quarterly (not annual) "
         "average - Q4 2021 is used here as the closest analogue to later years' 12-month-average KM1 figure. "
         "FY2021's own 'Average net flows' figure is not directly comparable to later years' 'Total net cash "
         "outflows (adjusted value)' definition, so that cell is left blank for FY2021 rather than approximated; "
         "the ratio and HQLA-equivalent buffer are shown as reported. FY2020's document uses its own pre-KM1 "
         "terms 'Liquidity Buffer' (used here as the HQLA-equivalent figure) and 'Total Net cash outflows'; its "
         "own headline LCR of 290% is 'excluding PRA Scalar' (its own footnote), with a lower 153% figure "
         "disclosed as the alternative including a 5% PRA Scalar add-on - the as-reported headline (excl. PRA "
         "Scalar) figure is used here for consistency with how later years' single as-reported ratio is shown, "
         "but the alternative basis is flagged since it is not a like-for-like methodology across all years.",
)

metric(
    "NSFR", "£'000 / % (conv. from USD)",
    [
        ("Total available stable funding", stock({
            "FY2024": 5139351, "FY2023": 4607371, "FY2022": 4297495, "FY2021": 10511066,
        })),
        ("Total required stable funding", stock({
            "FY2024": 2225713, "FY2023": 1822687, "FY2022": 1031978, "FY2021": 9455958,
        })),
        ("Net Stable Funding Ratio (%)", {"FY2024": "230.91%", "FY2023": "252.78%", "FY2022": "416.49%", "FY2021": "111.16%"}),
    ],
    p3_sources(),
    note="FY2021 is that year's Q4 (year-end) quarterly figure, as originally disclosed in quarterly form; "
         "FY2022 onward is each year's single annual KM1 figure. FY2020 is genuinely blank: that year's Basel "
         "II-era Pillar 3 document only mentions the upcoming regulatory 'binding NSFR measure of 100%' "
         "requirement (not yet in force that year) in its CRD V/CRR II preview section - it discloses no NSFR "
         "ratio, available stable funding, or required stable funding figure of its own anywhere in the document "
         "- confirmed by reading the full document, not assumed from a missing keyword.",
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "No separate MREL ratio or instruments disclosed in any year, including FY2020 (its "
                             "Basel II-era Pillar 3 document has no MREL section or mention at all - a different, "
                             "and more basic, non-disclosure than later years' explained non-disclosure below). "
                             "The Bank's own FY2021 Pillar 3 report is the first to explain why: following the "
                             "Bank of England's 3 December 2021 Statement of Policy on MREL, 'GIB (UK)'s MREL "
                             "requirement is equal to its CRD V requirement under Pillar 1 and Pillar 2A. "
                             "Consequently, the Bank does not need to hold any MREL compliant instruments in "
                             "addition to those needed to satisfy its CRD V requirement' - i.e. MREL is fully "
                             "satisfied by ordinary capital, with no incremental MREL-specific ratio or "
                             "instrument stock to disclose."})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
cf_totals_usd = {
    "Net cash (outflow)/inflow from operating activities": {"FY2024": -7404448, "FY2023": 9319508, "FY2022": 287025, "FY2021": 347323, "FY2020": -1602673},
    "Net cash used in investing activities": {"FY2024": -302, "FY2023": -508, "FY2022": -39, "FY2021": -4966, "FY2020": -735},
    "Net cash used in financing activities": {"FY2024": -3186, "FY2023": -3249, "FY2022": -2115, "FY2021": -108, "FY2020": -808},
}
cf_close_usd = {"FY2024": 7378636, "FY2023": 14883184, "FY2022": 5325978, "FY2021": 5599337, "FY2020": 5257088}

balance_sheet_totals_usd = {
    "Total assets": {"FY2024": 14498855, "FY2023": 21563064, "FY2022": 10259541, "FY2021": 10576392, "FY2020": 10462644},
    "Placements with banks": {"FY2024": 5666838, "FY2023": 5290351, "FY2022": 3661166, "FY2021": 3805701, "FY2020": 4988056},
    "Deposits from customers": {"FY2024": 12755439, "FY2023": 20851700, "FY2022": 9323428, "FY2021": 10022108, "FY2020": 9774293},
    "Total equity": {"FY2024": 459826, "FY2023": 458051, "FY2022": 418683, "FY2021": 406861, "FY2020": 392596},
}
income_statement_totals_usd = {
    "Net interest income": {"FY2024": 74249, "FY2023": 80868, "FY2022": 38522, "FY2021": 12061, "FY2020": 14291},
    "Operating expenses": {"FY2024": -65407, "FY2023": -57344, "FY2022": -52682, "FY2021": -43014, "FY2020": -38820},
    "Profit/(loss) for the year": {"FY2024": 24001, "FY2023": 39880, "FY2022": 7110, "FY2021": -6940, "FY2020": -16779},
}
equity_changes_totals_usd = {
    "Opening equity": {"FY2024": 458051, "FY2023": 418683, "FY2022": 406861, "FY2021": 392596, "FY2020": 394183},
    "Total comprehensive income/(loss) for the year": {"FY2024": 1775, "FY2023": 39368, "FY2022": 11822, "FY2021": 14265, "FY2020": -1730},
    "Closing equity": {"FY2024": 459826, "FY2023": 458051, "FY2022": 418683, "FY2021": 406861, "FY2020": 392596},
}

bw.add_overview_sheet(
    cash_flow_totals=[(label, flow(vals)) for label, vals in cf_totals_usd.items()]
                      + [("Cash and cash equivalents at end of year", stock(cf_close_usd))],
    cash_flow_unit="£'000",
    balance_sheet_totals=[(label, stock(vals)) for label, vals in balance_sheet_totals_usd.items()],
    balance_sheet_unit="£'000",
    income_statement_totals=[(label, flow(vals)) for label, vals in income_statement_totals_usd.items()],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", opening_cash(equity_changes_totals_usd["Opening equity"])),
        ("Total comprehensive income/(loss) for the year", flow(equity_changes_totals_usd["Total comprehensive income/(loss) for the year"])),
        ("Closing equity", stock(equity_changes_totals_usd["Closing equity"])),
    ],
    equity_changes_unit="£'000",
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Tier 1 Ratio", CAPITAL_RATIO),
        ("Total Capital Ratio", CAPITAL_RATIO),
        ("Leverage Ratio", {"FY2024": "5.02%", "FY2023": "5.28%", "FY2022": "7.17%", "FY2021": "3.52%", "FY2020": "4.61%"}),
        ("LCR", {"FY2024": "286.32%", "FY2023": "286.40%", "FY2022": "354.15%", "FY2021": "480.13%", "FY2020": "290%"}),
        ("NSFR", {"FY2024": "230.91%", "FY2023": "252.78%", "FY2022": "416.49%", "FY2021": "111.16%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation. All £ figures are converted from the Bank's native USD reporting (see Cash Flow Statement "
         "sheet's FX conversion note) - this conversion was not explicitly requested for this bank but applied "
         "for consistency with the rest of the series. FY2025 is blank throughout (no FY2025 Annual Report or "
         "Pillar 3 Disclosure published yet). FY2020's equity roll-forward row alone does not sum to the cent "
         "(Opening $394,183k + Total comprehensive income/(loss) -$1,730k = $392,453k, $143k short of the actual "
         "$392,596k closing balance) because of a one-off $143k retained-earnings reclassification adjustment "
         "disclosed that year (see the Statement of Changes in Equity sheet's own source note) - not an error.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/GULF INTERNATIONAL BANK UK FINANCIALS.xlsx")
