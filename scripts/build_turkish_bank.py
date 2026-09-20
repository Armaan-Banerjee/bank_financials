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

PILLAR3_REFERENCE_DATE_NOTE = (
    "REFERENCE DATE OF THE SOLE PILLAR 3 DOCUMENT - RESOLVED 2026-09-15 FROM THE DOCUMENT'S OWN CONTENT. This "
    "needed settling because the file's circumstances are misleading in three separate ways at once: it is "
    "labelled '2024' on the Bank's index page, it sits at a WordPress upload path dated FEBRUARY 2026 "
    "(/wp-content/uploads/2026/02/), and a search-engine snippet describes it as board-approved in 2025. None of "
    "those is the reporting date, and this project has previously been caught by a document whose cover date did "
    "not match its contents, so the PDF was downloaded and read rather than inferred from any of them.\n"
    "  THE DOCUMENT SAYS 31 DECEMBER 2024, in three independent places, and nothing in it points at any other "
    "date. (i) Cover page, verbatim: 'Turkish Bank (UK) Limited / PILLAR 3 DISCLOSURE / As of 31 December 2024 "
    "(the \"Reference Date\")'. (ii) Section 1 Introduction, verbatim: 'The P3D is aligned with the board of "
    "directors' (the \"Board\") latest strategic plan (the \"Strategic Plan\") and is based on the Bank's "
    "financial situation as of 31 December 2024 (the \"Reference Date\").' (iii) Section 2.1 Basis of Disclosure, "
    "verbatim: 'This document sets out the P3D of the Bank as of 31 December 2024 and has been prepared in "
    "accordance with the requirements of the BOE Prudential Regulation Authority Rulebook - Disclosure (CRR)...'. "
    "Its Appendix 1 Key Metrics table is likewise columned '31 Dec 24' and '31 Dec 23'. The document therefore "
    "maps to FY2024 in this workbook, with FY2023 as its comparative - which is how it is used.\n"
    "  WHY THE '2025' SNIPPET EXISTS, and it is not evidence of a 2025 reference date: section 2.3 Verification "
    "reads, verbatim and including the unfilled placeholder, 'The Pillar 3 disclosures were reviewed and approved "
    "by the Bank's Board of Directors on xx 2025.' The literal characters 'xx' were left in the published PDF - "
    "the day and month were never filled in before release. That sentence is about the date of BOARD APPROVAL, "
    "not the reporting reference date, and a report approved during 2025 for a 31 December 2024 reference date is "
    "entirely ordinary (if slow). Combined with the February 2026 upload, the picture is a small bank publishing "
    "its FY2024 Pillar 3 roughly 14 months after year-end with an unfinished approval line, NOT a mislabelled "
    "FY2025 document. Do not re-map this file to FY2025 on the strength of its upload path or that snippet.\n"
    "  COLUMN-HEADER DEFECT, recorded so it is not mistaken for a basis difference: the Appendix 1 comparative "
    "column is headed 'T-4 - Prior Year' where the UK KM1 template calls for T-1. The date printed immediately "
    "beneath it is '31 Dec 23', one year before the current column's '31 Dec 24', and its figures reconcile to "
    "the FY2023 Annual Report, so 'T-4' is a template-editing slip in the source and the column is the FY2023 "
    "comparative. Transcribed as FY2023 accordingly.\n"
    "  Section 2.2 also states, verbatim: 'The Pillar 3 Disclosures are prepared annually based upon the financial "
    "information prepared for the financial statements to the 31 December of each year and are available on the "
    "Bank's website'. The Bank thus asserts an ANNUAL cadence, yet only this one edition has ever appeared - which "
    "is why the other years' absence is recorded below as a publication failure rather than as any form of "
    "exemption. Section 3 confirms the basis used throughout this workbook: 'Its accounting and disclosures are on "
    "a solo basis. The Bank does not have any subsidiary undertakings and therefore does not fall within "
    "regulatory consolidation group.'\n"
)

PILLAR3_NOTE = (
    PILLAR3_REFERENCE_DATE_NOTE +
    "PILLAR 3 COVERAGE NOTE: only one Pillar 3 Disclosure document is published on the Bank's site, covering "
    "31 Dec 2024 with a 31 Dec 2023 comparative (its 'Appendix 1: Key Metrics' UK KM1 template). No earlier Pillar 3 "
    "edition could be found (site search or Wayback Machine) and no FY2025 edition has been published yet - "
    "consistent with this being a very small bank that appears to have only recently begun formal Pillar 3 "
    "disclosure. FY2021/FY2022/FY2025 capital RATIOS (CET1/Tier 1/Total Capital/Leverage/LCR/NSFR) are therefore "
    "genuinely not publicly available and are left blank rather than estimated; for the capital AMOUNTS those years "
    "do have an Annual Report figure, carried as a separate memo row (see below). "
    "Each Annual Report's own Note 37/38 'Capital risk management' does give a 'Total regulatory capital' figure for "
    "every year (FY2021-FY2025), but that figure is NOT on the same basis as CET1/Tier 1/Total Capital: it is an "
    "audited figure that includes fair value and revaluation reserve movements which the Bank's own notes state "
    "'would have [been] excluded... at the time of submission' of its actual regulatory return (confirmed by "
    "comparing the FY2024 AR's Total regulatory capital of £29,678k against the Pillar 3 KM1's CET1/Tier1/Total "
    "Capital of £28,884k for the same date). To avoid mixing bases under a single ratio/capital label, that broader "
    "AR figure is never substituted into the CET1/Tier 1/Total Capital rows themselves; as of 2026-09-15 it is "
    "instead carried on the three capital-amount sheets as a separate, explicitly-labelled 'Memo: Total regulatory "
    "capital (Annual Report basis)' row covering all five years, so the figure is available to a reader without "
    "ever being mistaken for CET1. The capital RATIO sheets are deliberately left untouched: the Annual Reports "
    "disclose a capital surplus over buffers but no capital ratio, and dividing the memo capital figure by Total "
    "RWAs would manufacture a ratio that appears in no source. Total RWAs is the one metric confirmed on a "
    "consistent, comparable basis across all 5 years (the "
    "Annual Reports' own RWA breakdown ties exactly to the Pillar 3 KM1 RWA figure for the years both exist).\n"
    "RE-VERIFIED 2026-09-12 (independent check, not a re-reading of the above): a Wayback Machine CDX scan of the "
    "whole turkishbank.co.uk domain filtered for 'pillar' returns exactly ONE archived document ever - the same "
    "FY2024 PILLAR-3-DISCLOSURE.pdf already cited here (capture 2026-03-07) - confirming no earlier or later "
    "edition has been published and then withdrawn. The FY2025 Annual Report (published April 2026) still carries "
    "no Pillar 3 edition alongside it. The FY2022 Annual Report was re-downloaded and re-read directly this "
    "session: its Note 'Capital risk management' (p.62) gives Total regulatory capital of GBP26,022k (FY2022) and "
    "GBP24,681k (FY2021) on that same broader audited basis, immediately followed by the Bank's own caveat that "
    "the actual capital returns 'would have excluded these items at the time of submission' - so those two years "
    "remain correctly excluded from the CET1/Tier 1/Total Capital ROWS for the basis reason above, not for lack "
    "of a findable figure. CORRECTION 2026-09-15: the GBP26,022k quoted in the preceding sentence is the FY2022 "
    "Annual Report's own printed total, but it is internally inconsistent with that same document's audited "
    "Statement of Changes in Equity and is superseded by the FY2023 Annual Report's GBP25,939k - the memo row on "
    "the capital sheets uses GBP25,939k, and the capital sheets' source note sets out the full reconciliation.\n"
    "RE-VERIFIED AGAIN 2026-09-15, this time against the Bank's own live publications page rather than the archive: "
    "https://www.turkishbank.co.uk/reports/ was fetched and every PDF link on it enumerated. It lists 19 Annual "
    "Reports (FY2007 through FY2025, the newest being the April-2026 Financial-Statements-TBUK-signed.pdf already "
    "cited in this workbook) and exactly ONE Pillar 3 item, labelled 'Pillar 3 Disclosure 2024' and pointing at the "
    "same /2026/02/PILLAR-3-DISCLOSURE.pdf already cited here. Direct probes of the WordPress upload paths a later "
    "edition would land in (/2026/04/, /2026/06/, /2026/08/ and /2027/02/ PILLAR-3-DISCLOSURE.pdf) all return HTTP "
    "404. So as at this date the FY2024 edition is still the Bank's newest Pillar 3 disclosure, published roughly "
    "14 months after its year-end; on that cadence an FY2025 edition would not be expected before early 2027. No "
    "FY2025 figure on a Pillar 3 basis therefore exists for the 9 metric sheets other than Total RWAs - Total RWAs "
    "is the one FY2025 Pillar 3 metric this workbook can fill on a comparable basis, and it comes from the FY2025 "
    "Annual Report's own Note 37 risk-weighted assets table rather than from any Pillar 3 document. The three "
    "capital-amount sheets additionally show FY2025 on the memo row described above, drawn from the same Note 37."
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


def capital_sources():
    """p3_sources() plus the Annual Report Note 37/38 capital-table citations.

    Used only on the three capital-amount sheets, which carry the AR 'Total
    regulatory capital' memo row in addition to the Pillar 3 KM1 row.
    """
    return (
        "Sources - Turkish Bank (UK) Limited, entity-level basis:\n"
        f"CET1/Tier 1/Total Capital row, FY2024/FY2023: Pillar 3 Disclosure (published Feb 2026), p.31 (Appendix 1: "
        f"Key Metrics - UK KM1 template, columns '31 Dec 24' / '31 Dec 23') - {P3_2024_URL}\n"
        f"Memo row, FY2025/FY2024 (GBP27,379k/GBP29,678k): Annual Report and Financial Statements for the year ended "
        f"31 December 2025, p.61 (Note 37 Capital risk management (unaudited), 'The Bank's regulatory capital "
        f"position was as follows') - {AR2025_URL} (scanned filing, OCR'd and visually cross-verified against the "
        f"rendered page image)\n"
        f"Memo row, FY2023 (GBP29,196k) and FY2022 (GBP25,939k): Annual Report and Financial Statements 2023, p.61 "
        f"(Note 37 Capital risk management) - {AR2023_URL}\n"
        f"Memo row, FY2021 (GBP24,681k): Annual Report and Financial Statements 2021, p.62 (Note 38 Capital risk "
        f"management) - {AR2021_URL} (scanned filing, OCR'd and visually cross-verified), corroborated by the "
        f"FY2021 comparative column of the FY2022 Annual Report, p.62 - {AR2022_URL}\n\n"
        "FY2022 FIGURE - WHICH EDITION IS RIGHT: the FY2022 Annual Report's own capital note (p.62) prints Total "
        "regulatory capital of GBP26,022k, built on retained earnings of GBP8,102k. That contradicts the SAME "
        "document's audited Statement of Changes in Equity (p.24), which closes retained earnings at 31 December "
        "2022 at GBP8,019k. The FY2023 Annual Report's comparative column uses GBP8,019k and restates the total to "
        "GBP25,939k, and its SOCIE opening balance also shows GBP8,019k. The other four components are identical in "
        "both editions, so the GBP83k difference is a retained-earnings error in the FY2022 note rather than a "
        "restatement (the FY2023 Annual Report's only flagged restatement is a loans/other-liabilities "
        "reclassification which it states had 'no impact... to the result for the period or net assets'). The "
        "audited-SOCIE-consistent GBP25,939k is used here.\n\n"
        + AR_CAPITAL_BASIS_NOTE + "\n\n"
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


# ---------------------------------------------------------------
# FY2021 / FY2022 / FY2025 ratio gap - converted 2026-09-15 from a blank cell
# (indistinguishable from an unresearched gap) to an explicit, enumerated
# negative. See RATIO_GAP_NEGATIVE for the evidence; these are written into
# the ratio/liquidity sheets by RATIO_GAP_DEFAULTS below.
# ---------------------------------------------------------------
RATIO_GAP_YEARS = ["FY2025", "FY2022", "FY2021"]
NOT_DISCLOSED = "Not publicly disclosed"

RATIO_GAP_NEGATIVE = (
    "FY2021 / FY2022 / FY2025 RATIOS - ENUMERATED AND ABSENT, NOT MERELY 'NOT FOUND' (established 2026-09-15; "
    "these cells previously stood blank, which is indistinguishable from an unresearched gap and had caused this "
    "bank to be re-chased). Two independent enumerations, each of a document set rather than a guessed URL:\n"
    "  (1) NO PILLAR 3 EDITION EXISTS FOR ANY OF THE THREE YEARS. https://www.turkishbank.co.uk/reports/ was "
    "fetched on 2026-09-15 and every PDF href in the raw HTML extracted and de-duplicated. Exactly ONE Pillar 3 "
    "item is present on the whole page - /wp-content/uploads/2026/02/PILLAR-3-DISCLOSURE.pdf, the FY2024 edition "
    "already cited in this workbook - alongside the Annual Reports. There is no FY2021, FY2022 or FY2025 Pillar 3 "
    "document to transcribe from. This agrees with the earlier Wayback CDX domain scan recorded above, which "
    "returned that same single file as the only 'pillar' object ever archived on the domain.\n"
    "  (2) THE ANNUAL REPORTS COVERING THOSE YEARS PUBLISH NO RATIO AT ALL. Each was opened and read, not merely "
    "searched for a filename:\n"
    "      FY2021 and FY2022 - the FY2022 Annual Report (" + AR2022_URL + ") is text-native (237,194 extracted "
    "characters, so no scanned-image false negative) and carries both years in one document. Full-text searching "
    "it for 'capital ratio', 'Tier 1', 'CET1', 'leverage ratio', 'liquidity coverage' and 'net stable' returns "
    "ZERO occurrences of any of them. Its Note 38 'Capital risk management' (p.62) is the only regulatory-capital "
    "disclosure in the document, and it prints a components table (Share capital 12,000 / 12,000; Retained "
    "earnings 8,102 / 6,879; Fair value reserve 198 / 293; Revaluation reserve 6,826 / 6,354; Less intangible "
    "assets (1,104) / (845)) totalling 'Total regulatory capital 26,022 / 24,681' - an AMOUNT and no ratio, no "
    "RWA-relative percentage, no leverage measure, followed immediately by the Bank's own caveat: 'Note the "
    "figures above include changes in fair value and revaluation reserves, as it has been audited. The actual "
    "capital returns submitted would have excluded these items at the time of submission.'\n"
    "      FY2025 - the FY2025 Annual Report (" + AR2025_URL + ") is a 66-page scanned Acrobat Sign filing with no "
    "text layer, so it was rendered to page images at 200dpi and OCR'd, and the capital note read from the "
    "rendered image directly. Note 37 'Capital risk management (unaudited)' is the only regulatory-capital "
    "disclosure in it. It prints the same shape of components table ending 'Total regulatory capital 27,379 / "
    "29,678', then a single further line 'Capital surplus taking into account buffers 13,307 / 15,240', then the "
    "risk-weighted-assets breakdown (Credit risk 85,636 / 96,508; Operational risk 17,787 / 14,332; FX risk 50 / "
    "280; Credit valuation adjustment - / 115; Total risk weighted assets 103,473 / 111,235). There is no capital "
    "ratio, no leverage ratio, no LCR and no NSFR anywhere in the note. Note that a capital SURPLUS over buffers "
    "is not a ratio and must not be converted into one.\n"
    "  WHY THE GAP IS NOT CLOSED BY ARITHMETIC: for every one of these three years this workbook holds both a "
    "capital amount (the Annual Report memo figure) and Total RWAs, so a CET1-style ratio could be produced by "
    "division. It deliberately is NOT. That would be back-solving a figure that appears in no source, and it "
    "would additionally be basis-mixing: the Annual Report capital figure is struck on the broader audited basis "
    "described in AR_CAPITAL_BASIS_NOTE and runs GBP794k-GBP1,097k above the Pillar 3 KM1 CET1 figure on the two "
    "dates where both bases are observable, so any quotient would be materially overstated and would sit in a "
    "column alongside genuinely-disclosed FY2023/FY2024 ratios as though comparable.\n"
    "  THIS IS NOT AN EXEMPTION. Nothing found in this pass suggests Turkish Bank (UK) Limited is relieved of the "
    "Pillar 3 duty for these years - and the Bank's own section 2.2 asserts it prepares the disclosures annually. "
    "The FY2024 document does record a narrower relief at section 2.1, quoted verbatim so it is not mistaken for "
    "a broader one: 'The level of disclosure on remuneration matters is subject to the proportionality rules set "
    "out in PRA PS16/23 \"Remuneration: Enhancing proportionality for small firms\". In accordance with the "
    "regulations published by the PRA in December 2023, the Bank meets the small CRR firms' criteria and for "
    "non-listed institutions and is therefore exempted from remuneration disclosures.' That is an exemption from "
    "REMUNERATION disclosures only; it does not touch the key-metrics templates and does not explain these gaps. "
    "So FY2021/FY2022 are a historical publication failure, and FY2025 is most likely simply not published yet - "
    "on the FY2024 edition's own ~14-month lag an FY2025 edition would not be expected before early 2027, which "
    "makes FY2025 (unlike FY2021/FY2022) worth one re-check then, and only then.\n"
    "  RE-ENUMERATED 2026-09-19 BY A SECOND, INDEPENDENT ROUTE, AND THE FY2025 CELL NOW SAYS SO INSTEAD OF "
    "STANDING BLANK. The reports page was re-fetched (HTTP 200, text/html, 160,913 bytes) and still carries "
    "exactly ONE Pillar 3 href among twenty PDFs. More usefully, turkishbank.co.uk runs WordPress, so the "
    "media library itself was enumerated through the REST API - /wp-json/wp/v2/media?per_page=100&search="
    "pillar (HTTP 200, application/json) - which lists UPLOADS whether or not any page links them, and so "
    "answers a question the page cannot. It returns exactly ONE item: PILLAR-3-DISCLOSURE.pdf, uploaded "
    "2026-02-13. That upload date is the real find. It pins the FY2024 edition's lag at thirteen and a half "
    "months after its 31 December 2024 reporting date, which puts an FY2025 edition around February 2027 - "
    "so FY2025 is NOT-YET-DUE rather than withheld, and the cell says that rather than implying a refusal. "
    "No SDDT row exists for this bank in the PRA waivers register (checked on both required columns, "
    "2026-09-19), so there is no exemption in play either - consistent with the Bank's own section 2.2."
)

# GA-020 (2026-09-19): the three gap years now say WHICH outcome they are,
# on the evidence in RATIO_GAP_NEGATIVE. FY2021 was additionally checked
# against its OWN Annual Report (a 64-page scan, OCR'd 2026-09-19 at 150dpi):
# no 'Tier 1', 'CET1', 'capital ratio', 'leverage ratio', 'coverage ratio',
# 'stable funding', 'LCR', 'NSFR' or 'MREL' anywhere; the capital note is
# narrative plus amounts.
GAP_TEXT = {
    "FY2025": ("Not published yet – only Pillar 3 is the FY2024 ed., uploaded 13 Feb 2026 (~14m lag), so FY2025 due "
               "c. Feb 2027; FY2025 AR Note 37 prints no ratio"),
    "FY2022": ("Not published – no FY2022 Pillar 3 (reports page, WP media API, Wayback CDX enumerated); FY2022 AR "
               "Note 38 p.62 gives a capital amount only, no ratio"),
    "FY2021": ("Not published – no FY2021 Pillar 3 (reports page, WP media API, Wayback CDX enumerated); FY2021 and "
               "FY2022 ARs give a capital amount only, no ratio"),
}
NSFR_FY2021 = ("Not applicable – UK NSFR requirement took effect 1 Jan 2022 (PRA PS17/21); in any case no FY2021 "
               "Pillar 3 exists and the FY2021/FY2022 ARs print no NSFR")
RATIO_GAP_DEFAULTS = dict(GAP_TEXT)


def ratio_sources():
    """p3_sources() plus the enumerated negative for the three gap years.

    Used on the ratio and liquidity sheets - the ones whose FY2021/FY2022/FY2025
    cells are an evidenced absence rather than an unresearched blank.
    """
    return p3_sources() + "\n\n" + RATIO_GAP_NEGATIVE


def ratio_row(label, values):
    """A ratio row with the three gap years pre-filled as an explicit negative."""
    return (label, {**RATIO_GAP_DEFAULTS, **values})


# Secondary, DIFFERENTLY-BASED series carried alongside the Pillar 3 rows on the
# three capital-amount sheets. This is the Annual Reports' own Note 37/38 "Total
# regulatory capital", available for all 5 years but on the broader audited basis
# described in AR_CAPITAL_BASIS_NOTE - it is NOT interchangeable with the KM1
# CET1/Tier 1/Total Capital figures, so it is kept on its own clearly-labelled
# row rather than used to fill the blanks in the row above it.
AR_TOTAL_REG_CAPITAL = {"FY2025": 27379, "FY2024": 29678, "FY2023": 29196, "FY2022": 25939, "FY2021": 24681}

AR_CAPITAL_ROW_LABEL = "Memo: Total regulatory capital (Annual Report basis - see note)"

AR_CAPITAL_BASIS_NOTE = (
    "The second row is a DIFFERENT BASIS and must not be read as a continuation of the first. It is the Annual "
    "Reports' own Note 37/38 'Capital risk management' Total regulatory capital, which is available for all five "
    "years but is struck on a broader basis than the Pillar 3 KM1 figure: for FY2021-FY2024 the Bank's own caveat "
    "under the table states the figures 'include changes in fair value and revaluation reserves, as it has been "
    "audited. The actual capital returns submitted would have excluded these items at the time of submission' "
    "(in the FY2025 Annual Report the whole of Note 37 is instead headed 'unaudited'). The gap is material and not "
    "a constant: for the two dates where both bases exist, the AR figure exceeds the KM1 figure by GBP794k at "
    "FY2024 (29,678 vs 28,884) and GBP1,097k at FY2023 (29,196 vs 28,099). It is carried here because it is the "
    "only capital amount the Bank publishes for FY2021, FY2022 and FY2025, and because every year's table foots "
    "exactly from its disclosed components - but it is a memo figure, not a CET1/Tier 1/Total Capital substitute."
)


def ar_capital_row():
    return (AR_CAPITAL_ROW_LABEL, dict(AR_TOTAL_REG_CAPITAL))

# ---------------------------------------------------------------
# KM1 Key Metrics - the Bank's own "Appendix 1: Key Metrics" UK KM1
# template, reproduced whole. Called BEFORE the first add_metric_sheet() so
# the sheet lands immediately after Asset Quality and before CET1 Capital.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital (£'000)", {"FY2024": 28884, "FY2023": 28099}),
    ("DATA", "2  Tier 1 capital (£'000)", {"FY2024": 28884, "FY2023": 28099}),
    ("DATA", "3  Total capital (£'000)", {"FY2024": 28884, "FY2023": 28099}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4  Total risk-weighted exposure amount (£'000)", {"FY2024": 111235, "FY2023": 99516}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    # FY2025 carries a recorded absence rather than a blank (2026-09-19). Row 5
    # is chosen because the CET1 Ratio sheet already holds a text cell for
    # FY2025, so no verifier comparison exists here to lose.
    ("DATA", "5  Common Equity Tier 1 ratio (%)",
     {"FY2025": "Not published yet - only edition is FY2024, uploaded Feb 2026; ~14m lag",
      "FY2024": "25.97%", "FY2023": "28.24%"}),
    ("DATA", "6  Tier 1 ratio (%)", {"FY2024": "25.97%", "FY2023": "28.24%"}),
    ("DATA", "7  Total Capital ratio (%)", {"FY2024": "25.97%", "FY2023": "28.24%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirement (%)", {}),
    ("DATA", "UK 7b  Additional AT1 SREP requirements (%)", {}),
    ("DATA", "UK 7c  Additional T2 SREP requirements (%)", {}),
    ("DATA", "UK 7d  Total SREP own funds requirements (%)", {"FY2024": "1.49%", "FY2023": "1.49%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8  Capital conservation buffer (%)", {"FY2024": "2.50%", "FY2023": "2.50%"}),
    ("DATA", "UK 8a  Conservation buffer due to macro-prudential or systemic risk identified at the level of a Member State (%)", {}),
    ("DATA", "9  Institution specific countercyclical buffer (%)", {"FY2024": "0.99%", "FY2023": "1.65%"}),
    ("DATA", "UK 9a  Systemic risk buffer (%)", {}),
    ("DATA", "10  Global Systemically Important Institution buffer (%)", {}),
    ("DATA", "UK 10a  Other Systemically Important Institution buffer", {}),
    ("DATA", "11  Combined buffer requirement (%)", {"FY2024": "3.49%", "FY2023": "4.15%"}),
    ("DATA", "UK 11a  Overall capital requirements (%)", {}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%)", {}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13  Total exposure measure (£'000)", {"FY2024": 181556, "FY2023": 185406}),
    ("DATA", "14  Leverage ratio", {"FY2024": "15.9%", "FY2023": "15.2%"}),
    ("SECTION", "Additional leverage ratio disclosure requirements", {}),
    ("DATA", "14a  Fully loaded ECL accounting model leverage ratio excluding claims on central banks (%)", {}),
    ("DATA", "1b  Leverage ratio including claims on central banks (%)", {"FY2024": "15.9%", "FY2023": "15.2%"}),
    ("DATA", "14c  Average leverage ratio excluding claims on central banks (%)", {}),
    ("DATA", "14d  Average leverage ratio including claims on central banks (%)", {}),
    ("DATA", "14e  Countercyclical leverage ratio buffer (%)", {}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (£'000)", {"FY2024": 30533, "FY2023": 45106}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value (£'000)", {"FY2024": 20131, "FY2023": 24411}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value (£'000)", {"FY2024": 15098, "FY2023": 18309}),
    ("DATA", "16  Total net cash outflows (adjusted value) (£'000)", {"FY2024": 5033, "FY2023": 6103}),
    ("DATA", "17  Liquidity coverage ratio (%)", {"FY2024": "606%", "FY2023": "739%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18  Total available stable funding (£'000)", {"FY2024": 158883, "FY2023": 147611}),
    ("DATA", "19  Total required stable funding (£'000)", {"FY2024": 81335, "FY2023": 76650}),
    ("DATA", "20  NSFR ratio", {"FY2024": "195.34%", "FY2023": "192.58%"}),
]

KM1_SOURCES = (
    "Sources - Turkish Bank (UK) Limited, entity-level (unconsolidated) basis, the Bank's own 'Appendix 1: Key "
    "Metrics' UK KM1 template:\n"
    f"FY2024: Pillar 3 Disclosure, reference date 31 December 2024 (published Feb 2026), p.31 (section 9 "
    f"Appendix, 'Appendix 1: Key Metrics'), column headed 'T - Current Year / 31 Dec 24' - {P3_2024_URL}\n"
    f"FY2023: the same table's 'Prior Year / 31 Dec 23' COMPARATIVE column, p.31 of the same document "
    f"- {P3_2024_URL}\n"
    "\n"
    "LATEST-EDITION CHECK, 2026-09-18: the Bank's own reports index (turkishbank.co.uk/reports/) was fetched "
    "directly as static HTML and every PDF href extracted - not Wayback, not the URLs already cited here. It "
    "carries exactly ONE Pillar 3 item, the file cited above, alongside the Annual Reports back to 2007. The "
    "newest Annual Report listed is the one already used here for FY2025. The document behind that single "
    "Pillar 3 URL was re-downloaded on 2026-09-18 and its cover still reads 'As of 31 December 2024 (the "
    "\"Reference Date\")', so it has not been silently replaced with a later edition since it was first read. "
    "Checked, none newer.\n"
    "STRENGTHENED THE SAME DAY by an enumeration that does not depend on the index page linking anything. The "
    "site is WordPress, so its whole media library was listed through the REST API - "
    "/wp-json/wp/v2/media?per_page=100&mime_type=application/pdf&orderby=date&order=desc, HTTP 200, "
    "application/json, 662,958 bytes - which returned ALL 77 PDFs the Bank has ever uploaded, including any "
    "that are unlinked or withdrawn from navigation. Exactly ONE of the 77 is a Pillar 3 document: "
    ".../2026/02/PILLAR-3-DISCLOSURE.pdf, uploaded 13 February 2026, the FY2024 edition already cited. The "
    "newest upload of any kind is dated 24 July 2026. So the FY2025 Pillar 3 is absent from the media library "
    "itself, not merely unlinked from the reports page - which is the difference between 'we could not find "
    "the link' and 'the file was never published'.\n"
    "\n"
    "WHY FY2023 IS A COMPARATIVE COLUMN AND WHY THE OTHER THREE YEARS ARE EMPTY. The Bank publishes a single "
    "Pillar 3 Disclosure and it is the only edition that has ever existed on its site or in the Internet "
    "Archive: a Wayback CDX domain sweep of turkishbank.co.uk filtered on '(pillar|disclos)' on 2026-09-18 "
    "returned exactly one capture, of this same file. There is therefore no FY2023 edition of its own to "
    "prefer over this comparative, and no FY2021, FY2022 or FY2025 edition at all - those three columns are "
    "empty because no key-metrics template exists for them on any basis, not because one was not found. See "
    "the Pillar 3 coverage note on the metric sheets for the full enumerated negative, including the Annual "
    "Reports' own capital tables, which are a different and broader basis and are deliberately not used to "
    "back-fill this template.\n"
    "\n"
    "BLANK CELLS ARE THE BANK'S OWN BLANKS. Fourteen template rows are printed with a row number and a label "
    "and NO figure in either column - UK 7a, UK 7b, UK 7c, UK 8a, UK 9a, 10, UK 10a, UK 11a, 12, 14a, 14c, "
    "14d and 14e. They are reproduced here as printed rows with empty cells rather than dropped, because a "
    "dropped row is indistinguishable from a row that was never found. The document prints no dash, no "
    "'n/a' and no zero in any of them: the cells are genuinely empty, confirmed in both the layout-preserving "
    "and the raw text extraction of p.31.\n"
    "\n"
    "THREE SOURCE DEFECTS, REPRODUCED AS PUBLISHED AND NOT CORRECTED.\n"
    "1. The comparative column is headed 'T-4 - Prior Year' above the date '31 Dec 23'. The prior year of a "
    "31 December 2024 reference date is T-1, and the date printed underneath is unambiguous, so the '-4' is a "
    "typo in the column header rather than a four-year-old column. The FY2023 figures are consistent with "
    "31 December 2023 throughout - the Annual Report's own Note 38 risk-weighted assets total for that date "
    "is the 99,516 this table prints on row 4.\n"
    "2. Row 14b is numbered '1b'. The row sits between 14a and 14c, is captioned 'Leverage ratio including "
    "claims on central banks (%)', and carries the same 15.9%/15.2% as row 14 - the UK template's 14b. The "
    "number is printed as '1b' and is shown that way here.\n"
    "3. Rows UK 7a, UK 7b and UK 7c are blank while row UK 7d prints a total SREP own funds requirement of "
    "1.49%, so the components of a figure the Bank does disclose are withheld. Nothing is derived to fill "
    "them.\n"
    "\n"
    "UNITS AND PRESENTATION. The table's column header reads £'000 and the amount rows additionally carry a "
    "'£' inside each cell ('£28,884'); the unit is carried in the row label here and the currency symbol is "
    "not repeated per cell. The Bank prints its capital ratios to two decimal places, its leverage ratio to "
    "one, its LCR to none and its NSFR to two - that mixture is the Bank's own and is kept.\n"
    "\n"
    "ENTITY. Turkish Bank (UK) Limited on an entity-level, unconsolidated basis - the Bank has no "
    "subsidiaries and the document prints one entity's columns only. See the ENTITY NOTE on the Cash Flow "
    "Statement sheet."
)

bw.add_km1_sheet(
    title="Turkish Bank (UK) Limited — KM1 Key Metrics",
    subtitle="The Bank's own 'Appendix 1: Key Metrics' UK KM1 template, reproduced whole in its own row order, "
             "row numbers, labels and precision. Amounts in £'000, ratios as printed. FY2024 is the sole Pillar "
             "3 edition's own reference date and FY2023 is that same table's comparative column; FY2025, FY2022 "
             "and FY2021 carry no column because no key-metrics template exists for them in any document.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=70,
    source_height=300,
)




metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2024": 28884, "FY2023": 28099}),
     ar_capital_row()],
    capital_sources(),
    note="TWO BASES - do not read down the column. Row 1 is CET1 as reported in the Pillar 3 KM1 template, which "
         "exists only for FY2023/FY2024. Row 2 is the Annual Reports' broader 'Total regulatory capital', the only "
         "capital amount published for FY2021/FY2022/FY2025; it runs GBP794k-GBP1,097k above CET1 where both are "
         "known. See the source note for the full basis reconciliation.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [ratio_row("Common Equity Tier 1 (CET1) ratio", {"FY2024": "25.97%", "FY2023": "28.24%"})],
    ratio_sources(),
    note="Only FY2023/FY2024 are publicly disclosed, and only because the Bank's single Pillar 3 edition covers "
         "those two dates. FY2021/FY2022/FY2025 read 'Not publicly disclosed' as an ENUMERATED negative, not an "
         "unchecked gap: no Pillar 3 edition exists for any of them, and the Annual Reports covering them were "
         "read in full and publish no capital ratio at all. Not back-solved from the capital and RWA figures this "
         "workbook does hold - see the source note for why that would be both a fabrication and a basis mix.",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2024": 28884, "FY2023": 28099}),
     ar_capital_row()],
    capital_sources(),
    note="CET1 = Tier 1 = Total Capital in both disclosed years (no AT1 or Tier 2 instruments), and the Annual "
         "Reports confirm capital resources 'consist of Share Capital, retained earnings, and other reserves' in "
         "every year, so the memo row is likewise all-CET1 in composition. TWO BASES - do not read down the column; "
         "see the source note.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [ratio_row("Tier 1 ratio", {"FY2024": "25.97%", "FY2023": "28.24%"})],
    ratio_sources(),
    note="Equal to the CET1 ratio in both disclosed years - the Bank holds no AT1 instruments. "
         "FY2021/FY2022/FY2025 read 'Not publicly disclosed' as an enumerated negative; see the source note.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2024": 28884, "FY2023": 28099}),
     ar_capital_row()],
    capital_sources(),
    note="CET1 = Tier 1 = Total Capital in both disclosed years (no AT1 or Tier 2 instruments), and the Annual "
         "Reports confirm capital resources 'consist of Share Capital, retained earnings, and other reserves' in "
         "every year, so the memo row is likewise all-CET1 in composition. TWO BASES - do not read down the column; "
         "see the source note.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [ratio_row("Total Capital ratio", {"FY2024": "25.97%", "FY2023": "28.24%"})],
    ratio_sources(),
    note="Equal to the CET1 and Tier 1 ratios in both disclosed years - the Bank holds no AT1 or Tier 2 "
         "instruments. FY2021/FY2022/FY2025 read 'Not publicly disclosed' as an enumerated negative; see the "
         "source note.",
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
        ratio_row("Total exposure measure", {"FY2024": 181556, "FY2023": 185406}),
        ratio_row("Leverage ratio (including claims on central banks) (%)", {"FY2024": "15.9%", "FY2023": "15.2%"}),
    ],
    ratio_sources(),
    note="The Bank reports on KM1 row 1b, 'Leverage ratio including claims on central banks', and leaves rows 14a "
         "and 14c-14e (the excluding-central-banks and average variants) blank in its own template, so only the "
         "including-central-banks basis exists for this bank - do not compare it like-for-like with another "
         "bank's excluding-central-banks figure. FY2021/FY2022/FY2025 read 'Not publicly disclosed' as an "
         "enumerated negative: no Pillar 3 edition covers them and neither Annual Report discloses any leverage "
         "measure or total exposure measure. See the source note.",
)

metric(
    "LCR", "£'000 / %",
    [
        ratio_row("Total high-quality liquid assets (HQLA)", {"FY2024": 30533, "FY2023": 45106}),
        ratio_row("Total net cash outflows (adjusted value)", {"FY2024": 5033, "FY2023": 6103}),
        ratio_row("Liquidity Coverage Ratio (%)", {"FY2024": "606%", "FY2023": "739%"}),
    ],
    ratio_sources(),
    note="FY2021/FY2022/FY2025 read 'Not publicly disclosed' as an enumerated negative - no Pillar 3 edition "
         "covers them and neither Annual Report gives a numeric LCR. See the source note.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": GAP_TEXT["FY2025"], "FY2024": 158883, "FY2023": 147611,
                                            "FY2022": GAP_TEXT["FY2022"], "FY2021": NSFR_FY2021}),
        ("Total required stable funding", {"FY2025": GAP_TEXT["FY2025"], "FY2024": 81335, "FY2023": 76650,
                                           "FY2022": GAP_TEXT["FY2022"], "FY2021": NSFR_FY2021}),
        ("NSFR ratio (%)", {"FY2025": GAP_TEXT["FY2025"], "FY2024": "195.34%", "FY2023": "192.58%",
                            "FY2022": GAP_TEXT["FY2022"], "FY2021": NSFR_FY2021}),
    ],
    ratio_sources() + (
        "\n\nNSFR FY2021 - STRUCTURAL, A DIFFERENT FINDING FROM THE OTHER GAP YEARS AND DELIBERATELY LABELLED "
        "DIFFERENTLY. The UK Net Stable Funding Ratio requirement took effect only on 1 January 2022 under PRA "
        "PS17/21. A 31 December 2021 reference date therefore precedes the requirement entirely: there was no NSFR "
        "for this bank to disclose, so the cell reads 'Not applicable' rather than 'Not publicly disclosed'. "
        "FY2022 is inside the requirement (the Bank's year-end is 31 December, so 31 December 2022 is the first "
        "in-scope reference date) but no Pillar 3 edition was published for it, so that cell keeps the ordinary "
        "'Not publicly disclosed'. Conflating the two would misrepresent a regulatory boundary as a publication "
        "failure."
    ),
    note="FY2024/FY2023 are the only disclosed years, from the Bank's single Pillar 3 edition. FY2025 and FY2022 "
         "read 'Not publicly disclosed' as an enumerated negative (no Pillar 3 edition, and no NSFR in the Annual "
         "Reports). FY2021 reads 'Not applicable' instead, for the different reason that the UK NSFR requirement "
         "did not exist at that reference date - see the source note.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    sources_text=p3_sources(),
    per_note={"MREL Ratio": (
        "Not publicly disclosed for any year - no numeric or qualitative MREL disclosure was found in either the "
        "Pillar 3 Disclosure or any Annual Report. Consistent with a very small bank likely below the threshold at "
        "which the Bank of England sets an MREL requirement above minimum capital requirements (no explicit "
        "exemption is stated, it is simply absent). GA-020 RE-CHECK 2026-09-19: zero occurrences of 'MREL' or "
        "'loss-absorbing' in the FY2024 Pillar 3 (text-native; its one 'resolution' hit is governance wording), the "
        "text-native FY2022, FY2023 and FY2024 Annual Reports, or the OCR text of the scanned FY2021 and FY2025 "
        "Annual Reports."
    )},
    statements={"MREL Ratio": ("Not published – no MREL figure or mention in the only Pillar 3 (FY2024 ed.) or in "
                               "ARs FY2021-FY2025 (full text / OCR searched 2026-09-19)")},
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
        ratio_row("CET1 Ratio", {"FY2024": "25.97%", "FY2023": "28.24%"}),
        ratio_row("Tier 1 Ratio", {"FY2024": "25.97%", "FY2023": "28.24%"}),
        ratio_row("Total Capital Ratio", {"FY2024": "25.97%", "FY2023": "28.24%"}),
        ratio_row("Leverage Ratio", {"FY2024": "15.9%", "FY2023": "15.2%"}),
        ratio_row("LCR", {"FY2024": "606%", "FY2023": "739%"}),
        ("NSFR", {"FY2025": GAP_TEXT["FY2025"], "FY2024": "195.34%", "FY2023": "192.58%",
                  "FY2022": GAP_TEXT["FY2022"], "FY2021": NSFR_FY2021}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Pillar 3 ratios are only publicly disclosed for FY2023/FY2024 "
         "- the Bank has published exactly one Pillar 3 edition to date, and that edition's own reference date is "
         "31 December 2024 (confirmed 2026-09-15 from its cover page, Introduction and section 2.1, despite its "
         "February 2026 upload path and an unfilled 'approved ... on xx 2025' line in its section 2.3). "
         "FY2021/FY2022/FY2025 now read 'Not publicly disclosed' rather than sitting blank: that is an ENUMERATED "
         "negative established 2026-09-15, not an unchecked gap. The Bank's reports index was fetched and every "
         "PDF link extracted (exactly one Pillar 3 item, the FY2024 edition), and the Annual Reports covering "
         "those three years were opened and read - the FY2022 report (text-native, covering FY2022 and FY2021) "
         "contains no occurrence of 'capital ratio', 'Tier 1', 'CET1', 'leverage ratio', 'liquidity coverage' or "
         "'net stable' anywhere, and the FY2025 report's Note 37 (read from the rendered page image, the filing "
         "being a scan) prints only capital amounts, a capital surplus over buffers and an RWA breakdown, with no "
         "ratio of any kind. These ratios are NOT computed from the capital and RWA figures this workbook holds "
         "for those years: that would be back-solving, and the available capital figure is on the broader Annual "
         "Report basis rather than the Pillar 3 basis. NSFR FY2021 reads 'Not applicable' instead, because the UK "
         "NSFR requirement began only on 1 January 2022 (PRA PS17/21) - a regulatory boundary, not a publication "
         "failure. See the Pillar 3 sheets' own source notes for the full evidence.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/TURKISH BANK UK FINANCIALS.xlsx")
