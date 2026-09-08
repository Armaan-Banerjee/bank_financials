import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.turkishbank.co.uk/wp-content/uploads/2026/04/Financial-Statements-TBUK-signed.pdf"
AR2024_URL = "https://www.turkishbank.co.uk/wp-content/uploads/2025/04/FINANCIAL-STATEMENTS-31122024-FINAL_SIGNED.pdf"
AR2023_URL = "https://www.turkishbank.co.uk/wp-content/uploads/2024/07/FY23TBUK-Financial-Statements-Signed.pdf"
AR2022_URL = "https://www.turkishbank.co.uk/wp-content/uploads/2023/05/FY22TBUK-Financial-Statements-Signed-for-AGM-signed.pdf"
AR2021_URL = "https://www.turkishbank.co.uk/wp-content/uploads/2022/07/21TBUK-Financial-Statements-reported-to-AGM-signed.pdf"
P3_2024_URL = "https://www.turkishbank.co.uk/wp-content/uploads/2026/02/PILLAR-3-DISCLOSURE.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Turkish Bank (UK) Limited (company number 02643004, FRN 204566), a UK-incorporated PRA-authorised "
    "bank majority-owned by Turkish Bank A.S. (Turkey/Northern Cyprus). Entity-level (unconsolidated) basis "
    "throughout - the Bank has no subsidiaries of its own. FY2021 and FY2025 Annual Reports were only available as "
    "fully scanned/image-only PDFs on the Bank's own site (no text layer) - both were OCR'd (tesseract) and every "
    "figure used below was cross-verified against the rendered page image, not trusted from OCR text alone."
)

PILLAR3_NOTE = (
    "PILLAR 3 COVERAGE NOTE: only one Pillar 3 Disclosure document is published on the Bank's site, covering "
    "31 Dec 2024 with a 31 Dec 2023 comparative (its 'Appendix 1: Key Metrics' UK KM1 template). No earlier Pillar 3 "
    "edition could be found (site search or Wayback Machine) and no FY2025 edition has been published yet - "
    "consistent with this being a very small bank that appears to have only recently begun formal Pillar 3 "
    "disclosure. FY2021/FY2022/FY2025 capital ratios (CET1/Tier 1/Total Capital/Leverage/LCR/NSFR) and the £ capital "
    "amounts behind them are therefore genuinely not publicly available and are left blank rather than estimated. "
    "Each Annual Report's own Note 37/38 'Capital risk management' does give a 'Total regulatory capital' figure for "
    "every year (FY2021-FY2025), but that figure is NOT on the same basis as CET1/Tier 1/Total Capital: it is an "
    "audited figure that includes fair value and revaluation reserve movements which the Bank's own notes state "
    "'would have [been] excluded... at the time of submission' of its actual regulatory return (confirmed by "
    "comparing the FY2024 AR's Total regulatory capital of £29,678k against the Pillar 3 KM1's CET1/Tier1/Total "
    "Capital of £28,884k for the same date). To avoid mixing bases under a single ratio/capital label, that broader "
    "AR figure is not substituted in here - see the Cash Flow Statement source note for where it can be found "
    "instead. Total RWAs is the one metric confirmed on a consistent, comparable basis across all 5 years (the "
    "Annual Reports' own RWA breakdown ties exactly to the Pillar 3 KM1 RWA figure for the years both exist)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Turkish Bank (UK) Limited's own Statement of Cash Flows, £'000:\n"
    f"FY2025: Annual Report and Financial Statements for the year ended 31 December 2025, p.21 (Statement of Cash "
    f"Flows) - {AR2025_URL} (scanned filing, OCR'd and visually cross-verified)\n"
    f"FY2024: Annual Report and Financial Statements for the year ended 31 December 2024, p.22 (Statement of Cash "
    f"Flows) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.22 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.23 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.23 (Statement of Cash Flows) - {AR2021_URL} (scanned "
    f"filing, OCR'd and visually cross-verified)\n"
    "Note: each year's column uses that year's own Annual Report's own as-originally-reported comparative rather "
    "than a later report's restated comparative (e.g. the FY2023 report restated some FY2022 line items following a "
    "reclassification of accrued interest, and the FY2025 report similarly restated FY2024 - in both cases the "
    "originally-reported figures from that year's own report are used here, consistent with this project's usual "
    "convention). All 5 years reconcile exactly: opening cash equivalents in each year matches the prior year's own "
    "closing figure, and every activity subtotal sums correctly from its own line items. The FY2025 Statement's "
    "'Net decrease in cash and cash equivalents' row is labelled 'decrease' in the source but the figure itself is "
    "positive (+£1,217k, an increase) - the number is used as printed (it reconciles exactly with opening/closing "
    "balances); only the label appears to be a leftover from the prior year's (negative) presentation. FY2021's "
    "'profit and non-cash adjustments' subtotal is printed as £(3,466)k but the seven line items above it as printed "
    "sum to £(3,464)k - an immaterial £2k gap in the source itself; the printed subtotal is used as shown (not "
    "force-corrected) since it is what the statement's own downstream totals are built from, and the gap is too "
    "small to matter to any of this bank's other figures.\n\n"
    + ENTITY_NOTE + "\n\n"
    "Note 37/38 'Capital risk management' in each Annual Report separately discloses 'Total regulatory capital' "
    "(FY2021: £24,681k: FY2022: £26,022k; FY2023: £29,196k; FY2024: £29,678k; FY2025: £27,379k) and 'Total risk "
    "weighted assets' (used for the Total RWAs sheet) - see PILLAR3_NOTE on the Pillar 3 sheets for why the capital "
    "figure is not used as CET1/Tier1/Total Capital. Minor (<£100k) differences exist between a year's figure as "
    "originally reported and as shown as the following year's comparative (e.g. FY2022 retained earnings: £8,102k "
    "in the FY2022 report vs £8,019k in the FY2023 report's comparative) - not explained in either report; each "
    "year's own report's own figure is used for its own column."
)


STATEMENTS_SOURCES = (
    "Sources - Turkish Bank (UK) Limited's own Statement of Financial Position, Statement of Profit or Loss and "
    "Statement of Changes in Equity, entity-level (unconsolidated) basis, £'000:\n"
    f"FY2025: Annual Report and Financial Statements for the year ended 31 December 2025, p.19 (Statement of "
    f"Profit or Loss and Other Comprehensive Income), p.20 (Statement of Financial Position), p.22 (Statement of "
    f"Changes in Equity) - {AR2025_URL} (scanned filing, OCR'd and visually cross-verified)\n"
    f"FY2024: Annual Report and Financial Statements for the year ended 31 December 2024, p.20 (Statement of "
    f"Profit or Loss...), p.21 (Statement of Financial Position), p.23 (Statement of Changes in Equity) - "
    f"{AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.20 (Statement of Profit or Loss...), p.21 (Statement "
    f"of Financial Position), p.23 (Statement of Changes in Equity) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.21 (Statement of Profit or Loss...), p.22 (Statement "
    f"of Financial Position), p.24 (Statement of Changes in Equity) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.21 (Statement of Profit or Loss...), p.22 (Statement "
    f"of Financial Position), p.24 (Statement of Changes in Equity) - {AR2021_URL} (scanned filing, OCR'd and "
    f"visually cross-verified)\n"
    "Note: each year's column uses that year's own Annual Report's own as-originally-reported figures rather than "
    "a later report's restated comparative - the same convention as the existing Cash Flow Statement sheet. "
    "AR2023 restated FY2022's Balance Sheet (reclassification of accrued interest) and AR2025 similarly restated "
    "FY2024's Balance Sheet (see each report's own Note 39) - the restated figures are not used here; FY2022 and "
    "FY2024 both use their own report's originally-published figures, and both still tie exactly (Total assets = "
    "Total liabilities + Total equity) on that basis. The restatements only reclassify line items between "
    "categories (e.g. accrued interest between 'Other assets'/'Other liabilities' and the posts they relate to) - "
    "Total assets/Total liabilities/Total equity are unaffected by the restatement, only the individual line-item "
    "split.\n\n"
    "INVESTMENT SECURITIES COMPOSITION: 'Investment securities' is 100% one bucket in every year shown - each "
    "year's own Note 19 'Investment securities' discloses it as entirely Preference Shares in Visa Inc./Visa "
    "Europe, an equity investment (arising from the 2016 Visa Europe/Visa Inc. reorganisation) held at fair value "
    "through other comprehensive income (FVOCI), with a same-note 'Origin of investment securities' analysis "
    "showing 100% USA issuer origin every year - not a debt security and not UK/government-issued, so there is no "
    "amortised-cost-vs-FVOCI or UK-government-vs-other split to make; the row is relabelled in place rather than "
    "broken into sub-rows. FY2025/FY2024 (GBP2,224k/GBP2,133k): Annual Report and Financial Statements for the "
    f"year ended 31 December 2025, Note 19, p.46 (table) - {AR2025_URL} (scanned filing, OCR'd). FY2023/FY2022 "
    f"(GBP1,631k/GBP1,380k): Annual Report and Financial Statements 2023, Note 19, p.44 - {AR2023_URL}. FY2022/"
    f"FY2021 (GBP1,380k/GBP1,132k): Annual Report and Financial Statements 2022, Note 19, p.45 - {AR2022_URL}. "
    f"FY2021 (GBP1,132k): Annual Report and Financial Statements 2021, Note 19, p.45 - {AR2021_URL} (scanned "
    "filing, OCR'd).\n\n"
    + ENTITY_NOTE
)

EQUITY_SOURCES = (
    STATEMENTS_SOURCES
    + "\n\nSOURCE INCONSISTENCY, reproduced as disclosed, not silently corrected: AR2024's own Statement of "
      "Financial Position (p.21) shows FY2024's closing OCI reserve as £749k and Revaluation reserve as £6,096k, "
      "but that same report's own Statement of Changes in Equity (p.23) shows the FY2024 closing balance for "
      "those same two components as £763k and £6,082k respectively - a £14k difference in opposite directions "
      "within the same document. Both pairs sum to the same Total equity (£30,499k), so the Total row here ties "
      "exactly to the Balance Sheet either way; the equity ladder below uses the Statement of Changes in Equity's "
      "own figures (763/6,082) since this is the equity sheet, and the £14k split difference is flagged here "
      "rather than picked silently. Separately, FY2021's own Statement of Changes in Equity (AR2021, p.24) prints "
      "a 'Total comprehensive income' row of £284k for FY2021, one £1k short of the £285k that its own three "
      "component figures for that row (-£23k OCI, +£337k revaluation OCI, -£29k retained earnings) actually sum "
      "to, and one £1k short of the £285k 'Total comprehensive income' the same year's own Statement of Profit or "
      "Loss (p.21) reports - an immaterial rounding artifact in the equity statement's own printed total, used as "
      "shown (not force-corrected)."
)

ASSET_QUALITY_SOURCES = (
    "Sources - Turkish Bank (UK) Limited, entity-level basis, £'000 unless stated:\n"
    f"FY2025/FY2024: Annual Report and Financial Statements for the year ended 31 December 2025, p.41-42 (Note 17 "
    f"Loans and advances to customers) and p.43 (Note 18 Provision for impairment losses) - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.42-44 (Notes 17-18) - {AR2023_URL}\n"
    f"FY2022/FY2021: Annual Report and Financial Statements 2022, p.43-45 (Notes 17-18) - {AR2022_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nThe 'Entity-wide loss allowance by IFRS 9 stage' block reconciles Note 18's opening-to-closing loss "
      "allowance table, which covers the Bank's ENTIRE portfolio (cash and cash equivalents, loans to banks, "
      "loans to customers and off-balance-sheet commitments combined) - not customer loans alone - and is kept "
      "separate from the customer-loan-specific Specific/Collective ECL split above it (Note 17), which is the "
      "figure that ties to the Balance Sheet's own 'Loans and advances to customers' line. Non-performing loan "
      "and gross-loan figures are only disclosed for customer loans (no by-stage gross-carrying-amount split is "
      "published, only the ECL allowance roll-forward), so the NPL ratio and ECL coverage ratio below are both "
      "calculated against total gross customer loans, not a Stage-3-specific denominator."
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Turkish Bank (UK) Limited, entity-level basis, £'000, each from that year's own Annual Report's "
    "'Capital risk management' note (marked unaudited by the Bank itself):\n"
    f"FY2025/FY2024: Annual Report and Financial Statements for the year ended 31 December 2025, p.61 (Note 37 "
    f"Capital risk management, risk weighted assets table) - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.63 (Note 38 Capital risk management, risk weighted "
    f"assets table) - {AR2023_URL}\n"
    f"FY2022/FY2021: Annual Report and Financial Statements 2022, p.64 (Note 38 Capital risk management, risk "
    f"weighted assets table) - {AR2022_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nUnlike the other Pillar 3 sheets in this workbook (CET1/Tier 1/Total Capital/Leverage/LCR/NSFR, only "
      "publicly disclosed for FY2023/FY2024 per PILLAR3_NOTE on those sheets), each Annual Report's own Capital "
      "risk management note independently discloses a full risk-category RWA breakdown for that report's own two "
      "years - giving genuine 5-year coverage here, broader than the standalone Pillar 3 Disclosure document (which "
      "only covers FY2023/FY2024 and has no category-level RWA table at all, only the KM1 total). All 5 years' "
      "category rows sum exactly to that year's own Total risk weighted assets, matching the existing Total RWAs "
      "metric sheet. FY2021's own comparative table (published in the FY2022 Annual Report) shows only 3 "
      "categories (Credit/Operational/FX risk), summing exactly to that year's Total RWAs with no separate Credit "
      "Valuation Adjustment line - left blank rather than assumed nil, since it isn't clear whether CVA risk was "
      "assessed separately that year or wasn't yet a distinct Pillar 1 component for the Bank."
)


def p3_sources():
    return (
        "Sources - Turkish Bank (UK) Limited, entity-level basis:\n"
        f"FY2024/FY2023: Pillar 3 Disclosure (published Feb 2026), p.31 (Appendix 1: Key Metrics - UK KM1 template, "
        f"columns '31 Dec 24' / '31 Dec 23') - {P3_2024_URL}\n"
        f"Total RWAs only, FY2022/FY2021: Annual Report and Financial Statements 2022, p.63 (Note 38 Capital risk "
        f"management, risk-weighted assets table) - {AR2022_URL}\n"
        f"Total RWAs only, FY2025: Annual Report and Financial Statements for the year ended 31 December 2025, p.61 "
        f"(Note 37 Capital risk management, risk-weighted assets table) - {AR2025_URL}\n\n"
        + PILLAR3_NOTE
    )


bw = BankWorkbook(bank_name="Turkish Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="9C3D54")

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 44666, "FY2024": 43449, "FY2023": 71933, "FY2022": 93264, "FY2021": 59279}),
    ("DATA", "Loans and advances to banks", {"FY2025": 49346, "FY2024": 50170, "FY2023": 31369, "FY2022": 15493, "FY2021": 39954}),
    ("DATA", "Loans and advances to customers", {"FY2025": 73278, "FY2024": 76518, "FY2023": 69249, "FY2022": 75754, "FY2021": 78062}),
    ("DATA", "Investment securities (Visa Inc./Visa Europe preference shares, FVOCI equity)", {"FY2025": 2224, "FY2024": 2133, "FY2023": 1631, "FY2022": 1380, "FY2021": 1132}),
    ("DATA", "Swap derivative assets", {"FY2024": 15, "FY2022": 182}),
    ("DATA", "Other assets", {"FY2025": 1298, "FY2024": 2192, "FY2023": 1830, "FY2022": 1307, "FY2021": 2909}),
    ("DATA", "Current tax assets", {"FY2025": 90, "FY2024": 163}),
    ("DATA", "Deferred tax assets", {"FY2025": 236, "FY2022": 86, "FY2021": 349}),
    ("DATA", "Property and equipment", {"FY2025": 7485, "FY2024": 6903, "FY2023": 8043, "FY2022": 7984, "FY2021": 7619}),
    ("DATA", "Intangible assets", {"FY2025": 1108, "FY2024": 819, "FY2023": 984, "FY2022": 1104, "FY2021": 845}),
    ("TOTAL", "Total assets", {"FY2025": 179731, "FY2024": 182362, "FY2023": 185039, "FY2022": 196554, "FY2021": 190149}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 6187, "FY2024": 6725, "FY2023": 10894, "FY2022": 13047, "FY2021": 15378}),
    ("DATA", "Deposits from customers", {"FY2025": 142952, "FY2024": 142973, "FY2023": 141429, "FY2022": 154342, "FY2021": 147702}),
    ("DATA", "Current tax liabilities", {"FY2023": 180}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 515, "FY2024": 462, "FY2023": 480, "FY2022": 483, "FY2021": 338}),
    ("DATA", "Swap derivative liabilities", {"FY2023": 40}),
    ("DATA", "Lease liabilities", {"FY2025": 29, "FY2024": 44, "FY2023": 81, "FY2022": 84, "FY2021": 187}),
    ("DATA", "Other liabilities", {"FY2025": 1254, "FY2024": 1659, "FY2023": 1755, "FY2022": 1555, "FY2021": 1018}),
    ("TOTAL", "Total liabilities", {"FY2025": 150937, "FY2024": 151863, "FY2023": 154859, "FY2022": 169511, "FY2021": 164623}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 12000, "FY2024": 12000, "FY2023": 12000, "FY2022": 12000, "FY2021": 12000}),
    ("DATA", "Retained earnings", {"FY2025": 11078, "FY2024": 11654, "FY2023": 10859, "FY2022": 8019, "FY2021": 6879}),
    ("DATA", "OCI reserve", {"FY2025": 832, "FY2024": 749, "FY2023": 387, "FY2022": 198, "FY2021": 293}),
    ("DATA", "Revaluation reserve", {"FY2025": 4884, "FY2024": 6096, "FY2023": 6934, "FY2022": 6826, "FY2021": 6354}),
    ("TOTAL", "Total equity", {"FY2025": 28794, "FY2024": 30499, "FY2023": 30180, "FY2022": 27043, "FY2021": 25526}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 179731, "FY2024": 182362, "FY2023": 185039, "FY2022": 196554, "FY2021": 190149}),
]

bw.add_balance_sheet_sheet(
    title="Turkish Bank (UK) Limited — Statement of Financial Position",
    subtitle="Entity-level basis, £'000",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=60,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 10531, "FY2024": 12623, "FY2023": 12411, "FY2022": 6417, "FY2021": 4405}),
    ("DATA", "Interest expense", {"FY2025": -2862, "FY2024": -2960, "FY2023": -2572, "FY2022": -651, "FY2021": -393}),
    ("TOTAL", "Net interest income", {"FY2025": 7669, "FY2024": 9663, "FY2023": 9839, "FY2022": 5766, "FY2021": 4012}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 580, "FY2024": 651, "FY2023": 663, "FY2022": 1135, "FY2021": 813}),
    ("DATA", "Fees and commissions payable", {"FY2025": -173, "FY2024": -158, "FY2023": -146, "FY2022": -157, "FY2021": -136}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 407, "FY2024": 493, "FY2023": 517, "FY2022": 978, "FY2021": 677}),
    ("DATA", "Net trading income", {"FY2025": 201, "FY2024": 266, "FY2023": 409, "FY2022": 146, "FY2021": 144}),
    ("DATA", "Other operating income", {"FY2025": 321, "FY2022": 383, "FY2021": 61}),
    ("TOTAL", "Total operating income", {"FY2025": 8598, "FY2024": 10422, "FY2023": 10765, "FY2022": 7273, "FY2021": 4895}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "ECL release/(charge) on financial instruments", {"FY2025": 1, "FY2024": -35, "FY2023": 60, "FY2022": -128, "FY2021": 153}),
    ("DATA", "Personnel expenses", {"FY2025": -5303, "FY2024": -5010, "FY2023": -3625, "FY2022": -2893, "FY2021": -2290}),
    ("DATA", "Premise expenses", {"FY2025": -647, "FY2024": -517, "FY2023": -564, "FY2022": -439, "FY2021": -357}),
    ("DATA", "Administrative expenses", {"FY2025": -3088, "FY2024": -3359, "FY2023": -2463, "FY2022": -1710, "FY2021": -1853}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -502, "FY2024": -455, "FY2023": -449, "FY2022": -526, "FY2021": -537}),
    ("DATA", "Other expenses", {"FY2025": -1, "FY2024": -26, "FY2023": -2, "FY2022": -105}),
    ("TOTAL", "Total operating expenses", {"FY2025": -9540, "FY2024": -9402, "FY2023": -7043, "FY2022": -5801, "FY2021": -4884}),
    ("DATA", "Finance cost", {"FY2024": -1, "FY2023": -1, "FY2022": -2, "FY2021": -2}),
    ("TOTAL", "(Loss)/Profit before taxation", {"FY2025": -942, "FY2024": 1019, "FY2023": 3721, "FY2022": 1470, "FY2021": 9}),
    ("DATA", "Income tax credit/(expense)", {"FY2025": 366, "FY2024": -224, "FY2023": -881, "FY2022": -330, "FY2021": -38}),
    ("TOTAL", "(Loss)/Profit after taxation", {"FY2025": -576, "FY2024": 795, "FY2023": 2840, "FY2022": 1140, "FY2021": -29}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Equity investments at FVOCI - net change in fair value", {"FY2025": 91, "FY2024": 501, "FY2023": 252, "FY2022": -129, "FY2021": 1}),
    ("DATA", "Deferred tax on fair value of equity investments", {"FY2025": -22, "FY2024": -125, "FY2023": -63, "FY2022": 34, "FY2021": -24}),
    ("DATA", "Revaluation of properties", {"FY2025": -1198, "FY2024": -961, "FY2023": 94, "FY2022": 583, "FY2021": 349}),
    ("DATA", "Deferred tax on property revaluation", {"FY2024": 109, "FY2023": 14, "FY2022": -111, "FY2021": -12}),
    ("TOTAL", "Total other comprehensive income/(expense)", {"FY2025": -1129, "FY2024": -476, "FY2023": 297, "FY2022": 377, "FY2021": 314}),
    ("TOTAL", "Total comprehensive income/(expense) for the year", {"FY2025": -1705, "FY2024": 319, "FY2023": 3137, "FY2022": 1517, "FY2021": 285}),
]

bw.add_income_statement_sheet(
    title="Turkish Bank (UK) Limited — Statement of Profit or Loss and Other Comprehensive Income",
    subtitle="Entity-level basis, £'000",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "OCI reserve", "Revaluation reserve", "Retained earnings", "Total"]
equity_changes_rows = [
    ("TOTAL", "At 1 January 2021", (12000, 316, 6017, 6908, 25241)),
    ("DATA", "Loss for the year", (None, None, None, -29, -29)),
    ("DATA", "Other comprehensive income/(expense)", (None, -23, 337, None, 314)),
    ("TOTAL", "Total comprehensive income/(expense) for the year", (None, -23, 337, -29, 284)),
    ("TOTAL", "At 31 December 2021", (12000, 293, 6354, 6879, 25526)),
    ("DATA", "Profit for the year", (None, None, None, 1140, 1140)),
    ("DATA", "Other comprehensive income/(expense)", (None, -95, 472, None, 377)),
    ("TOTAL", "Total comprehensive income/(expense) for the year", (None, -95, 472, 1140, 1517)),
    ("TOTAL", "At 31 December 2022", (12000, 198, 6826, 8019, 27043)),
    ("DATA", "Profit for the year", (None, None, None, 2840, 2840)),
    ("DATA", "Other comprehensive income/(expense)", (None, 189, 108, None, 297)),
    ("TOTAL", "Total comprehensive income/(expense) for the year", (None, 189, 108, 2840, 3137)),
    ("TOTAL", "At 31 December 2023", (12000, 387, 6934, 10859, 30180)),
    ("DATA", "Profit for the year", (None, None, None, 795, 795)),
    ("DATA", "Other comprehensive income/(expense)", (None, 376, -852, None, -476)),
    ("TOTAL", "Total comprehensive income/(expense) for the year", (None, 376, -852, 795, 319)),
    ("TOTAL", "At 31 December 2024", (12000, 763, 6082, 11654, 30499)),
    ("DATA", "Loss for the year", (None, None, None, -576, -576)),
    ("DATA", "Other comprehensive income/(expense)", (None, 69, -1198, None, -1129)),
    ("TOTAL", "Total comprehensive income/(expense) for the year", (None, 69, -1198, -576, -1705)),
    ("TOTAL", "At 31 December 2025", (12000, 832, 4884, 11078, 28794)),
]

bw.add_equity_changes_sheet(
    title="Turkish Bank (UK) Limited — Statement of Changes in Equity",
    subtitle="Entity-level basis, £'000, chronological",
    headers=equity_headers,
    rows=equity_changes_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=50,
    source_height=320,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) after taxation", {"FY2025": -576, "FY2024": 795, "FY2023": 2840, "FY2022": 1140, "FY2021": -29}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": 311, "FY2024": 255, "FY2023": 261, "FY2022": 316, "FY2021": 309}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 192, "FY2024": 200, "FY2023": 188, "FY2022": 210, "FY2021": 228}),
    ("DATA", "Non-cash stock dividends received from Visa", {"FY2022": -383, "FY2021": 0}),
    ("DATA", "Net interest income", {"FY2025": -7669, "FY2024": -9663, "FY2023": -9839, "FY2022": -5766, "FY2021": -4012}),
    ("DATA", "Interest paid on lease liabilities", {"FY2025": 0, "FY2024": 1, "FY2023": 1, "FY2022": 2, "FY2021": 2}),
    ("DATA", "Income tax expense/(credit)", {"FY2025": -366, "FY2024": 224, "FY2023": 881, "FY2022": 330, "FY2021": 38}),
    ("TOTAL", "Subtotal - profit and non-cash adjustments", {"FY2025": -8108, "FY2024": -8188, "FY2023": -5668, "FY2022": -4151, "FY2021": -3466}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Loans and advances to customers", {"FY2025": 3479, "FY2024": -7269, "FY2023": 5951, "FY2022": 2308, "FY2021": 3493}),
    ("DATA", "Loans and advances to banks", {"FY2025": 1871, "FY2024": -18801, "FY2023": -15876, "FY2022": 24461, "FY2021": -25858}),
    ("DATA", "Other assets", {"FY2025": -304, "FY2024": -540, "FY2023": -340, "FY2022": 1420, "FY2021": -1716}),
    ("DATA", "Deposits from banks", {"FY2025": -538, "FY2024": -4169, "FY2023": -2153, "FY2022": -2331, "FY2021": 5621}),
    ("DATA", "Deposits from customers", {"FY2025": -568, "FY2024": 1544, "FY2023": -12913, "FY2022": 6640, "FY2021": 2240}),
    ("DATA", "Other liabilities", {"FY2025": 173, "FY2024": -215, "FY2023": 1221, "FY2022": 112, "FY2021": 11}),
    ("TOTAL", "Subtotal - changes in operating assets and liabilities", {"FY2025": 4113, "FY2024": -29450, "FY2023": -24110, "FY2022": 32610, "FY2021": -16209}),
    ("SECTION", "Interest and tax", {}),
    ("DATA", "Interest received", {"FY2025": 10531, "FY2024": 12623, "FY2023": 12411, "FY2022": 6417, "FY2021": 4405}),
    ("DATA", "Interest paid", {"FY2025": -2862, "FY2024": -2960, "FY2023": -2572, "FY2022": -651, "FY2021": -393}),
    ("DATA", "Income tax recovered/(paid)", {"FY2025": 130, "FY2024": -374, "FY2023": -669}),
    ("TOTAL", "Net cash flows from/(used in) operating activities", {"FY2025": 3804, "FY2024": -28349, "FY2023": -20608, "FY2022": 34225, "FY2021": -15663}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Additions to/acquisition of property and equipment", {"FY2025": -2091, "FY2024": -61, "FY2023": -186, "FY2022": -97, "FY2021": -15}),
    ("DATA", "Additions to/acquisition of intangible assets", {"FY2025": -481, "FY2024": -35, "FY2023": -493, "FY2022": -43, "FY2021": -6}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -2572, "FY2024": -96, "FY2023": -679, "FY2022": -140, "FY2021": -21}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payment for lease liabilities", {"FY2025": -15, "FY2024": -38, "FY2023": -43, "FY2022": -98, "FY2021": -108}),
    ("DATA", "Interest paid on lease liabilities", {"FY2025": 0, "FY2024": -1, "FY2023": -1, "FY2022": -2, "FY2021": -2}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": -15, "FY2024": -39, "FY2023": -44, "FY2022": -100, "FY2021": -110}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 1217, "FY2024": -28484, "FY2023": -21331, "FY2022": 33985, "FY2021": -15794}),
    ("DATA", "Cash and cash equivalents as at 1 January", {"FY2025": 43449, "FY2024": 71933, "FY2023": 93264, "FY2022": 59279, "FY2021": 75073}),
    ("TOTAL", "Cash and cash equivalents as at 31 December", {"FY2025": 44666, "FY2024": 43449, "FY2023": 71933, "FY2022": 93264, "FY2021": 59279}),
]

bw.add_cash_flow_sheet(
    title="Turkish Bank (UK) Limited — Statement of Cash Flows",
    subtitle="Entity-level basis, £'000",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=310,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers by product (gross)", {}),
    ("DATA", "Overdraft", {"FY2025": 4136, "FY2024": 3229, "FY2023": 2548, "FY2022": 4533, "FY2021": 3111}),
    ("DATA", "Fixed term - Retail", {"FY2025": 52037, "FY2024": 51855, "FY2023": 49829, "FY2022": 52387, "FY2021": 55256}),
    ("DATA", "Fixed term - Corporation", {"FY2025": 17628, "FY2024": 22009, "FY2023": 17228, "FY2022": 18931, "FY2021": 19750}),
    ("TOTAL", "Gross loans and advances to customers", {"FY2025": 73801, "FY2024": 77093, "FY2023": 69605, "FY2022": 75851, "FY2021": 78117}),
    ("SECTION", "Impairment (customer loans)", {}),
    ("DATA", "ECL allowance - Specific", {"FY2025": -1, "FY2024": -68, "FY2023": -35, "FY2022": -35, "FY2021": -35}),
    ("DATA", "ECL allowance - Collective", {"FY2025": -52, "FY2024": -40, "FY2023": -60, "FY2022": -62, "FY2021": -20}),
    ("TOTAL", "Total ECL allowance (customer loans)", {"FY2025": -53, "FY2024": -108, "FY2023": -95, "FY2022": -97, "FY2021": -55}),
    ("DATA", "Unamortised portion of loan fees", {"FY2025": -470, "FY2024": -467, "FY2023": -261}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 73278, "FY2024": 76518, "FY2023": 69249, "FY2022": 75754, "FY2021": 78062}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "Non-performing loans (Stage 3, 90+ days past due), £'000", {"FY2025": 35.9, "FY2024": 966.9, "FY2023": 1020.5, "FY2022": 2074.2, "FY2021": 7242.4}),
    ("DATA", "NPL ratio (NPL / gross customer loans)", {"FY2025": "0.05%", "FY2024": "1.25%", "FY2023": "1.47%", "FY2022": "2.73%", "FY2021": "9.27%"}),
    ("DATA", "ECL coverage ratio (customer ECL / gross customer loans)", {"FY2025": "0.07%", "FY2024": "0.14%", "FY2023": "0.14%", "FY2022": "0.13%", "FY2021": "0.07%"}),
    ("SECTION", "Entity-wide loss allowance by IFRS 9 stage (cash, banks, customer loans and commitments combined)", {}),
    ("DATA", "Stage 1", {"FY2025": 123, "FY2024": 111, "FY2023": 93, "FY2022": 165, "FY2021": 40}),
    ("DATA", "Stage 2", {"FY2025": 3, "FY2024": 1, "FY2023": 2, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Stage 3", {"FY2025": 4, "FY2024": 85, "FY2023": 67, "FY2022": 57, "FY2021": 54}),
    ("TOTAL", "Total loss allowance (all asset classes)", {"FY2025": 130, "FY2024": 197, "FY2023": 162, "FY2022": 222, "FY2021": 94}),
]

bw.add_asset_quality_sheet(
    title="Turkish Bank (UK) Limited — Asset Quality",
    subtitle="Entity-level basis, £'000 unless stated",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=58,
    source_height=280,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=140)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2024": 28884, "FY2023": 28099})],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2024": "25.97%", "FY2023": "28.24%"})],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2024": 28884, "FY2023": 28099})],
    p3_sources(),
    note="CET1 = Tier 1 = Total Capital in both disclosed years (no AT1 or Tier 2 instruments). Only FY2023/FY2024 "
         "are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2024": "25.97%", "FY2023": "28.24%"})],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2024": 28884, "FY2023": 28099})],
    p3_sources(),
    note="CET1 = Tier 1 = Total Capital in both disclosed years (no AT1 or Tier 2 instruments). Only FY2023/FY2024 "
         "are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total Capital ratio", {"FY2024": "25.97%", "FY2023": "28.24%"})],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": 103473, "FY2024": 111235, "FY2023": 99516, "FY2022": 92487, "FY2021": 102064})],
    p3_sources(),
    note="The one metric available for all 5 years: each Annual Report's own Note 37/38 RWA breakdown (Credit + "
         "Operational + FX + CVA risk) ties exactly to the Pillar 3 KM1 RWA figure for the years both exist "
         "(FY2023/FY2024), confirming a consistent basis across all years.",
)

rwa_breakdown_rows = [
    ("SECTION", "Risk-weighted assets by category", {}),
    ("DATA", "Credit risk", {"FY2025": 85636, "FY2024": 96508, "FY2023": 86227, "FY2022": 81562, "FY2021": 90839}),
    ("DATA", "Operational risk", {"FY2025": 17787, "FY2024": 14332, "FY2023": 10869, "FY2022": 9675, "FY2021": 10388}),
    ("DATA", "FX risk", {"FY2025": 50, "FY2024": 280, "FY2023": 1741, "FY2022": 1250, "FY2021": 837}),
    ("DATA", "Credit valuation adjustment", {"FY2025": 0, "FY2024": 115, "FY2023": 679, "FY2022": 0}),
    ("TOTAL", "Total risk-weighted assets", {"FY2025": 103473, "FY2024": 111235, "FY2023": 99516, "FY2022": 92487, "FY2021": 102064}),
]

bw.add_rwa_breakdown_sheet(
    title="Turkish Bank (UK) Limited — RWA Breakdown",
    subtitle="Entity-level basis, £'000",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=280,
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure", {"FY2024": 181556, "FY2023": 185406}),
        ("Leverage ratio (including claims on central banks) (%)", {"FY2024": "15.9%", "FY2023": "15.2%"}),
    ],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA)", {"FY2024": 30533, "FY2023": 45106}),
        ("Total net cash outflows (adjusted value)", {"FY2024": 5033, "FY2023": 6103}),
        ("Liquidity Coverage Ratio (%)", {"FY2024": "606%", "FY2023": "739%"}),
    ],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2024": 158883, "FY2023": 147611}),
        ("Total required stable funding", {"FY2024": 81335, "FY2023": 76650}),
        ("NSFR ratio (%)", {"FY2024": "195.34%", "FY2023": "192.58%"}),
    ],
    p3_sources(),
    note="Only FY2023/FY2024 are publicly disclosed - see PILLAR3_NOTE.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    sources_text=p3_sources(),
    per_note={"MREL Ratio": (
        "Not publicly disclosed for any year - no numeric or qualitative MREL disclosure was found in either the "
        "Pillar 3 Disclosure or any Annual Report. Consistent with a very small bank likely below the threshold at "
        "which the Bank of England sets an MREL requirement above minimum capital requirements (no explicit "
        "exemption is stated, it is simply absent)."
    )},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 179731, "FY2024": 182362, "FY2023": 185039, "FY2022": 196554, "FY2021": 190149}),
        ("Total liabilities", {"FY2025": 150937, "FY2024": 151863, "FY2023": 154859, "FY2022": 169511, "FY2021": 164623}),
        ("Total equity", {"FY2025": 28794, "FY2024": 30499, "FY2023": 30180, "FY2022": 27043, "FY2021": 25526}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 8598, "FY2024": 10422, "FY2023": 10765, "FY2022": 7273, "FY2021": 4895}),
        ("(Loss)/Profit before taxation", {"FY2025": -942, "FY2024": 1019, "FY2023": 3721, "FY2022": 1470, "FY2021": 9}),
        ("(Loss)/Profit after taxation", {"FY2025": -576, "FY2024": 795, "FY2023": 2840, "FY2022": 1140, "FY2021": -29}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Total equity at year end", {"FY2025": 28794, "FY2024": 30499, "FY2023": 30180, "FY2022": 27043, "FY2021": 25526}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 3804, "FY2024": -28349, "FY2023": -20608, "FY2022": 34225, "FY2021": -15663}),
        ("Net cash from/(used in) investing activities", {"FY2025": -2572, "FY2024": -96, "FY2023": -679, "FY2022": -140, "FY2021": -21}),
        ("Net cash from/(used in) financing activities", {"FY2025": -15, "FY2024": -39, "FY2023": -44, "FY2022": -100, "FY2021": -110}),
        ("Cash and cash equivalents at end of year", {"FY2025": 44666, "FY2024": 43449, "FY2023": 71933, "FY2022": 93264, "FY2021": 59279}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2024": "25.97%", "FY2023": "28.24%"}),
        ("Tier 1 Ratio", {"FY2024": "25.97%", "FY2023": "28.24%"}),
        ("Total Capital Ratio", {"FY2024": "25.97%", "FY2023": "28.24%"}),
        ("Leverage Ratio", {"FY2024": "15.9%", "FY2023": "15.2%"}),
        ("LCR", {"FY2024": "606%", "FY2023": "739%"}),
        ("NSFR", {"FY2024": "195.34%", "FY2023": "192.58%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Pillar 3 ratios are only publicly disclosed for FY2023/FY2024 "
         "(the Bank has published only one Pillar 3 edition to date) - see the Pillar 3 sheets' PILLAR3_NOTE for "
         "detail on why FY2021/FY2022/FY2025 are blank rather than estimated.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/TURKISH BANK UK FINANCIALS.xlsx")
