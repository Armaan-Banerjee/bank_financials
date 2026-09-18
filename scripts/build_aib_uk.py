import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Cash flow statement only exists for FY2021-FY2023 - see CASH_FLOW_EXEMPTION_NOTE
# below. Pillar 3 / capital disclosures (from the Annual Report's own "Capital
# management and liquidity" section - AIB UK does not publish a separate KM1-style
# Pillar 3 document) cover all 5 years.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/NI018800/filing-history"
AR2025_URL = "https://www.aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/annualreport/2025/aib-group-uk-plc-annual-financial-report-2025.pdf"
AR2024_URL = "https://www.aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/annualreport/2024/aib-group-uk-plc-annual-financial-report-2024.pdf"
AR2023_URL = "https://aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/annualreport/2023/aib-group-uk-plc-annual-financial-report-2023.pdf"
AR2022_URL = "https://aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/annualreport/2022/AIB-Group-UK-p.l.c-Annual-Financial-Report-2022.pdf"
# FY2021 Annual Financial Report - see ACCESS_ROUTE_NOTE below. NOT on aib.ie and NOT
# reachable on the bank's own aibgb.co.uk (HTTP 403); Companies House serves it.
AR2021_URL = ("https://find-and-update.company-information.service.gov.uk/company/NI018800/filing-history/"
              "MzMzMjQ0MDUyOWFkaXF6a2N4/document?format=pdf&download=0")

ACCESS_ROUTE_NOTE = (
    "ACCESS ROUTE NOTE (FY2021 - CORRECTS AN EARLIER 'COULD NOT BE FETCHED' CLAIM, 2026-09-16): an earlier pass of "
    "this script recorded that the standalone FY2021 Annual Financial Report 'could not be fetched' because the only "
    "URL found for it (on the bank's own aibgb.co.uk) returned HTTP 403, and fell back on the FY2022 edition's FY2021 "
    "comparative column for every FY2021 figure. That claim is WRONG and is corrected here: the document IS publicly "
    "available, via COMPANIES HOUSE rather than either of AIB's own websites. Working route - Companies House filing "
    "history for company NI018800, filing filed 11 March 2022, document id 'MzMzMjQ0MDUyOWFkaXF6a2N4':\n"
    f"  {AR2021_URL}\n"
    "Verified on retrieval: %PDF magic bytes, 9,246,343 bytes, 168 pages, cover reads 'AIB Group (UK) p.l.c. Annual "
    "Financial Report for the year ended 31 December 2021, Company number: NI018800'; signed by Robert Mulhall "
    "(Managing Director) and Janet McConkey (CFO) on 2 March 2022. Do NOT retry aibgb.co.uk for this document - it "
    "403s, and aib.ie's investor-relations document tree only goes back to the FY2022 edition. Use Companies House.\n"
    "TRANSCRIPTION METHOD: unlike AIB UK's FY2022-FY2025 PDFs (which are text-native), the Companies House FY2021 "
    "filing is a SCANNED image with no text layer (pdftotext -layout returns 168 bytes for 168 pages). Figures were "
    "obtained by rendering each page (pdftoppm -png -r 200 -gray) and OCR'ing (tesseract --psm 6), then VISUALLY "
    "verifying every digit used here against the rendered page image. That visual check mattered: OCR misread the "
    "Criticised watch total on printed p.118 as 187 (the Stage 2 column) when the Total column reads 242, and "
    "flattened several two-block table rows. No figure below rests on unverified OCR.\n"
    "OTHER 403-DRIVEN FALLBACKS IN THIS SCRIPT: none. FY2021 was the only year sourced via a 403 fallback - "
    "FY2022-FY2025 each have a working aib.ie-hosted PDF of that year's own Annual Financial Report, already cited "
    "below. The remaining next-year-comparative citations in this script (e.g. FY2024 balance-sheet figures read "
    "from the FY2025 report) are deliberate cross-checks against a document that WAS fetched, not access failures."
)

ENTITY_NOTE = (
    "ENTITY NOTE: 'AIB Group (UK) p.l.c.' (FRN 122088, Companies House NI018800, registered in Northern Ireland) is "
    "a UK subsidiary of Allied Irish Banks, p.l.c. / AIB Group plc (Irish parent, Dublin-registered, no. 594283) - "
    "it is a DIFFERENT legal entity from 'AIB Group plc' itself, which publishes its own much larger, Ireland-wide "
    "consolidated Pillar 3 Disclosures on aib.ie. Early research surfaced AIB Group plc's Irish-group Pillar 3 PDFs "
    "first (they dominate web search results) - these were discarded as the wrong entity. All figures in this "
    "workbook are AIB Group (UK) p.l.c.'s own Annual Financial Report, not the wider AIB Group plc's disclosures. "
    "Confirmed via Companies House filing history and the FRN in Banks List 2608.xlsx."
)

CASH_FLOW_EXEMPTION_NOTE = (
    "CASH FLOW EXEMPTION NOTE: only FY2021-FY2023 have a Statement of Cash Flows. The FY2024 and FY2025 Annual "
    "Financial Reports both state, under '1.2 Basis of preparation': 'the Company has applied the exemptions "
    "available under FRS 101 in respect of the following disclosures: a statement of cash flows and related notes "
    "(IAS 1 Presentation of Financial Statements and IAS 7 Statement of Cash Flows)...' - confirmed directly in "
    "both PDFs' own text (not OCR'd; both are text-native filings). The FY2021-FY2023 reports instead presented "
    "consolidated 'AIB UK Group' financial statements (no FRS 101 exemptions), which is why a full cash flow "
    "statement exists for those three years but not the two most recent ones - the same 'exemption kicks in "
    "partway through the window' pattern seen with Tandem Bank Limited elsewhere in this project, though here it's "
    "a switch from group to solo (FRS 101) reporting that triggers it, not a straightforward late adoption."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are the 'AIB UK Group' (consolidated) column of AIB Group (UK) p.l.c.'s own Statement "
    "of Cash Flows, £m (not the 'AIB UK' solo column shown alongside it, and not AIB Group plc's Irish-group "
    "figures):\n"
    f"FY2023: FY2023 Annual Financial Report, p.73 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: FY2022 Annual Financial Report, p.71 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: FY2021 Annual Financial Report, printed p.70 (Statement of cash flows, 'AIB UK Group' column), "
    f"retrieved from Companies House - {AR2021_URL}\n"
    "FY2022 figures were independently cross-checked against their appearance as the FY2023 report's own FY2022 "
    "comparative column and matched exactly.\n\n"
    "FY2021 VALIDATION GATE (2026-09-16) - PRIMARY vs. THE FY2022 COMPARATIVE COLUMN PREVIOUSLY RELIED ON: every "
    "FY2021 cash-flow figure in this sheet was re-read from the FY2021 report's OWN statement of cash flows and "
    "REPRODUCES the FY2022 edition's FY2021 comparative column EXACTLY - profit before taxation 89, non-cash items "
    "27, 116, (73), 679, (32), 109, 2, (50), 637, 753, taxation paid (3), 750, additions to PP&E (7), additions to "
    "intangibles (4), (11), repayment of secondary non-preferential debt (45), repayment of lease liabilities (3), "
    "(48), change in cash 691, opening 4,662, closing 5,353. This is a meaningful confirmation, not a formality: "
    "the figures were previously one edition removed from their source and are now primary-sourced.\n"
    "ONE PRESENTATIONAL DIFFERENCE, documented rather than merged: the FY2021 report shows a separate 'Net decrease "
    "in items in course of collection' line of £1m and a NIL 'Net decrease in other assets' line, whereas the FY2022 "
    "edition carries a single 'Change in other assets' of £1m for FY2021 (i.e. it folded items in course of "
    "collection into other assets, matching the same folding it applied on the balance sheet - see the Balance Sheet "
    "sheet's note). Both presentations are shown below on separate labelled rows; no figure was overwritten. The "
    "FY2021 report also prints a 'Dividends received from subsidiary undertakings' line that is NIL on the AIB UK "
    "Group (consolidated) basis used here (£3m on the AIB UK solo basis, which this workbook does not use for "
    "FY2021-FY2023).\n\n"
    + ENTITY_NOTE + "\n\n" + CASH_FLOW_EXEMPTION_NOTE + "\n\n" + ACCESS_ROUTE_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - all figures from AIB Group (UK) p.l.c.'s own Annual Financial Report, 'Capital management and "
        "liquidity' section (AIB UK does not publish a separate standalone Pillar 3/KM1 disclosure document - "
        "capital and liquidity metrics are disclosed within the Annual Financial Report itself):\n"
        f"FY2025: FY2025 Annual Financial Report, p.5 - {AR2025_URL}\n"
        f"FY2024: FY2024 Annual Financial Report, p.11 - {AR2024_URL}\n"
        f"FY2023: FY2023 Annual Financial Report, p.17-18 - {AR2023_URL}\n"
        f"FY2022: FY2022 Annual Financial Report, p.19-20 - {AR2022_URL}\n"
        f"FY2021: FY2021 Annual Financial Report, printed p.20-21 ('Capital management and liquidity'), retrieved "
        f"from Companies House - {AR2021_URL}\n"
        "Figures shown are on a TRANSITIONAL basis (AIB UK's own headline reported ratio each year) - fully loaded "
        "(post-IFRS 9 transitional relief) figures are also disclosed but not used here, consistent with how this "
        "project treats IFRS 9 transitional relief for other banks. For FY2021 the primary states both: CET1 "
        "£1,508m transitional / £1,442m fully loaded, capital ratio 22.81% transitional / 22.01% fully loaded, RWA "
        "£6,611m transitional / £6,554m fully loaded (FY2021 Annual Financial Report, p.20).\n"
        "FY2021 VALIDATION GATE (2026-09-16): the FY2021 figures here were previously taken from the FY2022 "
        "edition's comparatives. They have now been re-read from the FY2021 Annual Financial Report itself and "
        "AGREE with what was already in the workbook - CET1 £1,508m (the FY2022 report's own capital-movement table "
        "opens at the identical 'CET1 at 31 December 2021 1,508 / 1,442'), Total RWA £6,611m (likewise the FY2022 "
        "RWA table's opening line, 6,611 / 6,554) and LCR 169% (the FY2022 report's 'LCR was 176% (2021: 169%)' "
        "reproduces the FY2021 report's own 'As at 31 December 2021 AIB UK Group's LCR was 169% (2020: 178%)'). No "
        "capital or liquidity figure required correction; the citations are upgraded from the following year's "
        "comparative column to the primary document.\n"
        "WHAT THE FY2021 PRIMARY DOES *NOT* CONTAIN (checked by full-text search of the OCR'd 168-page filing, so "
        "these absences are evidenced rather than assumed, and should not be re-chased): no leverage ratio anywhere; "
        "no NSFR and no mention of stable funding (the NSFR became a binding UK requirement only from 1 January "
        "2022, per the FY2022 report's own 'Net Stable Funding Ratio' note, so FY2021's 156% exists only as a "
        "retrospectively-supplied comparative in the FY2022 report); no 'Total capital' or 'Tier 1 capital' figure "
        "of any kind - the FY2021 capital table discloses CET1 only, the word 'total capital' appearing solely in "
        "the recital of the 8% CRR minimum; and no absolute category-level RWA split (the FY2021 report gives only a "
        "FY2020-to-FY2021 movement, the mirror image of the FY2022 report's own presentation - see RWA Breakdown).\n"
        "ADDITIONAL FY2021 DETAIL FROM THE PRIMARY: AIB UK Group's agreed Pillar 1 + Pillar 2a requirement for 2021 "
        "was 9.95% of RWA (FY2021 Annual Financial Report, p.20; corroborated by the FY2022 report, which states "
        "9.86% 'for 2022, a reduction from 9.95% in 2021'). Loan to deposit ratio 62% at 31 December 2021 (2020: "
        "69%); customer balances were 79% of total liabilities and shareholders' equity (2020: 82%). The FY2021 "
        "CET1 ratio of 22.8% includes COVID-19 relief add-backs; excluding them it is 22.0% (p.3 footnote).\n"
        + (extra + "\n" if extra else "")
        + "\n" + ENTITY_NOTE + "\n\n" + ACCESS_ROUTE_NOTE
    )


bw = BankWorkbook(bank_name="AIB Group (UK) p.l.c.", years=YEARS, year_label=YEAR_LABEL, header_color="8C1D40")

# ---------------------------------------------------------------
# Entity-basis note for the statement sheets below: FY2021-FY2023 figures
# are the "AIB UK Group" consolidated column of each year's own Annual
# Financial Report; FY2024-FY2025 figures are AIB Group (UK) p.l.c.'s own
# (solo/Company) column, since group-level consolidated statements ceased
# once the FRS 101 exemptions took effect (see CASH_FLOW_EXEMPTION_NOTE).
# This mirrors the CASH_FLOW_SOURCES convention already used above.
# ---------------------------------------------------------------
STATEMENT_ENTITY_NOTE = (
    "STATEMENT BASIS NOTE: FY2021-FY2023 figures are the 'AIB UK Group' (consolidated) column of that year's own "
    "Annual Financial Report; FY2024-FY2025 figures are AIB Group (UK) p.l.c.'s own single (solo/Company) column, "
    "since a separate consolidated 'AIB UK Group' basis ceased being reported once the FRS 101 exemptions took "
    "effect (see CASH_FLOW_EXEMPTION_NOTE above). This produces a real, small entity-basis break in the Statement "
    "of Changes in Equity between the FY2023 Group closing balance (£1,853m) and the FY2024 solo opening balance "
    "(£1,852m) - a genuine £1m difference in AIB UK's own disclosures, not a transcription error - flagged rather "
    "than silently reconciled, the same treatment used for a similar cross-statement inconsistency found in "
    "Monzo's pilot workbook."
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
BALANCE_SHEET_SOURCES = (
    "Sources - Statement of financial position, £m:\n"
    f"FY2025: FY2025 Annual Financial Report, p.33 - {AR2025_URL}\n"
    f"FY2024: FY2025 Annual Financial Report, p.33 (FY2024 comparative column; also independently cross-checked "
    f"against FY2024 Annual Financial Report's own p.96 statement, which matches exactly) - {AR2025_URL}\n"
    f"FY2023: FY2023 Annual Financial Report, p.70 ('AIB UK Group' column) - {AR2023_URL}\n"
    f"FY2022: FY2023 Annual Financial Report, p.70 (FY2022 comparative, 'AIB UK Group' column; matches FY2022 "
    f"Annual Financial Report's own p.70 statement) - {AR2023_URL}\n"
    f"FY2021 (as presented in the FY2022 edition - the column used for the main rows above): FY2022 Annual "
    f"Financial Report, p.70 (FY2021 comparative, 'AIB UK Group' column) - {AR2022_URL}\n"
    f"FY2021 (as originally reported - the separately labelled memorandum rows at the foot of this sheet): FY2021 "
    f"Annual Financial Report, printed p.68 (Statement of financial position, 'AIB UK Group' column), retrieved "
    f"from Companies House - {AR2021_URL}\n\n"
    "FY2021 VALIDATION GATE (2026-09-16) - PRIMARY vs. THE FY2022 COMPARATIVE COLUMN: the FY2021 Annual Financial "
    "Report was retrieved from Companies House (see ACCESS ROUTE NOTE) and its own statement of financial position "
    "re-read. Every FY2021 figure on this sheet REPRODUCES, including all three totals - cash and balances at "
    "central banks 5,306, derivative financial instruments 91 (asset) / 128 (liability), loans and advances to "
    "banks 637, loans and advances to customers 6,198, investment securities 40, investments in group undertakings "
    "nil on the Group basis, intangibles 21, PP&E 31, current taxation 28, deferred tax assets 148, prepayments and "
    "accrued income 10, retirement benefit assets 161, TOTAL ASSETS 12,688; deposits by banks 434, customer "
    "accounts 10,088, lease liabilities 17, deferred tax liabilities 13, other liabilities 174, accruals and "
    "deferred income 8, provisions 34, TOTAL LIABILITIES 10,896; share capital 2,384, TOTAL SHAREHOLDERS' EQUITY "
    "1,792, TOTAL LIABILITIES AND EQUITY 12,688. Nothing required correction.\n"
    "TWO PRESENTATIONAL DIFFERENCES, recorded on separate labelled rows rather than merged (the FY2022 edition "
    "aggregates where the FY2021 edition split, and every total is unaffected):\n"
    "  (1) The FY2021 report prints 'Items in course of collection' as its own asset line at £3m and 'Other assets' "
    "at £14m; the FY2022 edition drops the separate line and shows 'Other assets' at £17m for FY2021 (= 14 + 3). "
    "The main row above carries £17m, so that FY2021 is on the same footing as FY2022-FY2025; the £14m/£3m split is "
    "in the memorandum rows. The same folding shows up on the Cash Flow Statement sheet - see its note.\n"
    "  (2) The FY2021 report splits shareholders' equity into 'Reserves' (22) and 'Retained earnings' (570); the "
    "FY2022 edition presents a single 'Reserves' line of (592) for FY2021 (= -22 + -570). Main row carries (592); "
    "the split is in the memorandum rows. Note the FY2021 report's £(570) retained-earnings figure ties exactly to "
    "the 'Revenue reserves' closing balance on the Statement of Changes in Equity sheet.\n"
    "Also newly evidenced from the primary: 'Secondary non-preferential debt' - a line the FY2022 edition omits "
    "entirely for FY2021 - stood at NIL at 31 December 2021 (£45m at 31 December 2020), the £45m having been repaid "
    "during the year. That is an explicit disclosed nil, not an unknown, and it is what makes Total Capital = CET1 "
    "for FY2021 (see the Tier 1 Capital and Total Capital sheets).\n\n"
    + ENTITY_NOTE + "\n\n" + STATEMENT_ENTITY_NOTE + "\n\n" + ACCESS_ROUTE_NOTE
    + "\n\nCORRECTION (HD-066 correctness audit): 'Investment securities' FY2024 (£54m) was previously missing "
      "entirely from this sheet - confirmed via the FY2024 Annual Financial Report's own p.52 Statement of "
      "financial position and the FY2025 Annual Financial Report's own p.33 FY2024 comparative column (both agree: "
      "£54m) - this £54m gap exactly reconciled the previous Total assets tie-out for FY2024. Also added the "
      "explicitly-disclosed nil ('—') FY2025 Investment securities and FY2024 Investments in group undertakings "
      "values (both £0m, not blank) for consistency with how every other year on this row is shown."
    + "\n\nINVESTMENT SECURITIES NOTE-LEVEL BREAKDOWN (checked for all 5 years against each year's own annual "
      "report note, not just the balance sheet page): the 'Investment securities' note discloses only a single "
      "line item, 'Equity shares (unlisted) - measured at FVTPL', which reconciles exactly to 'Total investment "
      "securities' in every year - there is no further split by measurement basis or issuer type to break out, and "
      "no UK government/gilts/treasury exposure sits in this line (that would be unlisted equity shares, not debt "
      "securities). Row relabelled in place (not split into sub-rows) since there is nothing to sum against. "
      "Sourced from: FY2025 Annual Financial Report, note 21 'Investment securities', p.81 (FY2025: £0m; FY2024: "
      f"£54m) - {AR2025_URL}; FY2024 Annual Financial Report, note 20 'Investment securities', p.103 (FY2024: £54m; "
      f"FY2023: £73m) - {AR2024_URL}; FY2023 Annual Financial Report, note 21 'Investment securities' (FY2023: "
      f"£73m; FY2022: £50m) - {AR2023_URL}; FY2022 Annual Financial Report, note 22 'Investment securities', p.129 "
      f"(FY2022: £50m; FY2021: £40m, 'AIB UK Group & AIB UK' basis) - {AR2022_URL}."
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 3056, "FY2024": 3961, "FY2023": 3229, "FY2022": 3924, "FY2021": 5306}),
    ("DATA", "Derivative financial instruments", {"FY2025": 27, "FY2024": 46, "FY2023": 186, "FY2022": 220, "FY2021": 91}),
    ("DATA", "Loans and advances to banks", {"FY2025": 696, "FY2024": 714, "FY2023": 502, "FY2022": 555, "FY2021": 637}),
    ("DATA", "Loans and advances to customers", {"FY2025": 5291, "FY2024": 4708, "FY2023": 5647, "FY2022": 5718, "FY2021": 6198}),
    ("DATA", "Securities financing", {"FY2025": 921}),
    ("DATA", "Investment securities - Equity shares (unlisted), measured at FVTPL", {"FY2025": 0, "FY2024": 54, "FY2023": 73, "FY2022": 50, "FY2021": 40}),
    ("DATA", "Investments in group undertakings", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Intangible assets", {"FY2025": 15, "FY2024": 14, "FY2023": 13, "FY2022": 15, "FY2021": 21}),
    ("DATA", "Property, plant and equipment", {"FY2025": 30, "FY2024": 31, "FY2023": 33, "FY2022": 27, "FY2021": 31}),
    ("DATA", "Other assets", {"FY2025": 22, "FY2024": 22, "FY2023": 13, "FY2022": 55, "FY2021": 17}),
    ("DATA", "Current taxation", {"FY2025": 0, "FY2024": 16, "FY2023": 8, "FY2022": 6, "FY2021": 28}),
    ("DATA", "Deferred tax assets", {"FY2025": 226, "FY2024": 208, "FY2023": 207, "FY2022": 241, "FY2021": 148}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 8, "FY2024": 5, "FY2023": 4, "FY2022": 7, "FY2021": 10}),
    ("DATA", "Retirement benefit assets", {"FY2025": 12, "FY2024": 41, "FY2023": 54, "FY2022": 57, "FY2021": 161}),
    ("TOTAL", "Total assets", {"FY2025": 10304, "FY2024": 9820, "FY2023": 9969, "FY2022": 10875, "FY2021": 12688}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 230, "FY2024": 109, "FY2023": 354, "FY2022": 390, "FY2021": 434}),
    ("DATA", "Customer deposits", {"FY2025": 7588, "FY2024": 7317, "FY2023": 7118, "FY2022": 8204, "FY2021": 10088}),
    ("DATA", "Derivative financial instruments", {"FY2025": 176, "FY2024": 262, "FY2023": 376, "FY2022": 506, "FY2021": 128}),
    ("DATA", "Lease liabilities", {"FY2025": 12, "FY2024": 13, "FY2023": 14, "FY2022": 8, "FY2021": 17}),
    ("DATA", "Current taxation", {"FY2025": 10, "FY2024": 0, "FY2023": 10, "FY2022": 0}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 1, "FY2024": 1, "FY2023": 2, "FY2022": 2, "FY2021": 13}),
    ("DATA", "Other liabilities", {"FY2025": 61, "FY2024": 59, "FY2023": 78, "FY2022": 80, "FY2021": 174}),
    ("DATA", "Accruals and deferred income", {"FY2025": 12, "FY2024": 13, "FY2023": 12, "FY2022": 11, "FY2021": 8}),
    ("DATA", "Provisions for liabilities and commitments", {"FY2025": 12, "FY2024": 12, "FY2023": 11, "FY2022": 20, "FY2021": 34}),
    ("DATA", "Tier 2 subordinated liabilities / other capital instruments", {"FY2025": 141, "FY2024": 141, "FY2023": 141}),
    ("TOTAL", "Total liabilities", {"FY2025": 8243, "FY2024": 7927, "FY2023": 8116, "FY2022": 9221, "FY2021": 10896}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 457, "FY2024": 457, "FY2023": 457, "FY2022": 2384, "FY2021": 2384}),
    ("DATA", "Reserves", {"FY2025": 1494, "FY2024": 1326, "FY2023": 1286, "FY2022": -730, "FY2021": -592}),
    ("TOTAL", "Total shareholders' equity", {"FY2025": 1951, "FY2024": 1783, "FY2023": 1743, "FY2022": 1654, "FY2021": 1792}),
    ("DATA", "Other equity interests (AT1)", {"FY2025": 110, "FY2024": 110, "FY2023": 110}),
    ("TOTAL", "Total equity", {"FY2025": 2061, "FY2024": 1893, "FY2023": 1853, "FY2022": 1654, "FY2021": 1792}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 10304, "FY2024": 9820, "FY2023": 9969, "FY2022": 10875, "FY2021": 12688}),
    ("SECTION", "Memorandum — FY2021 as originally reported (see validation-gate note below)", {}),
    ("DATA", "Items in course of collection (FY2021 as originally reported; folded into 'Other assets' by the FY2022 edition)", {"FY2021": 3}),
    ("DATA", "Other assets, excluding items in course of collection (FY2021 as originally reported)", {"FY2021": 14}),
    ("DATA", "Reserves, excluding retained earnings (FY2021 as originally reported)", {"FY2021": -22}),
    ("DATA", "Retained earnings (FY2021 as originally reported; combined into 'Reserves' by the FY2022 edition)", {"FY2021": -570}),
    ("DATA", "Secondary non-preferential debt (FY2021 as originally reported — explicitly nil, repaid in the year)", {"FY2021": 0}),
]

bw.add_balance_sheet_sheet(
    title="AIB Group (UK) p.l.c. — Statement of Financial Position",
    subtitle="£m. Main rows: FY2022-edition basis for FY2021. See the memorandum rows and source note for the FY2021 presentational splits, plus the Group (FY2021-FY2023) vs solo (FY2024-FY2025) entity-basis switch.",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=88,
    source_height=940,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
INCOME_STATEMENT_SOURCES = (
    "Sources - (Consolidated) income statement, £m:\n"
    f"FY2025: FY2025 Annual Financial Report, p.31 - {AR2025_URL}\n"
    f"FY2024: FY2025 Annual Financial Report, p.31 (FY2024 comparative column; matches FY2024 Annual Financial "
    f"Report's own p.50 statement) - {AR2025_URL}\n"
    f"FY2023: FY2023 Annual Financial Report, p.68 ('AIB UK Group'/consolidated column - NOT the 'AIB UK' solo "
    f"column shown alongside it in that report, nor the solo-basis FY2023 comparative later reused in the FY2024 "
    f"report) - {AR2023_URL}\n"
    f"FY2022: FY2023 Annual Financial Report, p.68 (FY2022 comparative, 'AIB UK Group' column; matches FY2022 "
    f"Annual Financial Report's own p.68 statement) - {AR2023_URL}\n"
    f"FY2021 (as presented in the FY2022 edition - the column used for the main rows above, for consistency of "
    f"presentation with FY2022 onward): FY2022 Annual Financial Report, p.68 (FY2021 comparative, 'AIB UK Group' "
    f"column) - {AR2022_URL}\n"
    f"FY2021 (as originally reported - the separately labelled memorandum rows at the foot of this sheet): FY2021 "
    f"Annual Financial Report, printed p.66 (Consolidated income statement), retrieved from Companies House - "
    f"{AR2021_URL}\n\n"
    "FY2021 VALIDATION GATE (2026-09-16) - PRIMARY vs. THE FY2022 COMPARATIVE COLUMN, DIVERGENCE FOUND, NOTHING "
    "OVERWRITTEN: the FY2021 Annual Financial Report was retrieved from Companies House (see ACCESS ROUTE NOTE) and "
    "its own income statement re-read. Most of the column reproduces exactly - interest income 218, interest "
    "expense (20), net interest income 198, fee and commission income 45 and expense (4), net trading and other "
    "financial income 7, net gain on other financial assets at FVTPL 6, net loss on derecognition (8), operating "
    "expenses (141), impairment and amortisation of intangibles (8), impairment and depreciation of PP&E (11), "
    "total operating expenses (160), net credit impairment writeback 8, profit before taxation 89, income tax "
    "credit 81, and profit for the year 170. But SIX lines do NOT reproduce, because the FY2022 edition "
    "RECLASSIFIED a £3m loss on disposal of property that the FY2021 edition had reported BELOW operating profit:\n"
    "  Other operating income:                     FY2021 edition NIL   -> FY2022 edition (3)\n"
    "  Other income / Total other income:          FY2021 edition 46    -> FY2022 edition 43\n"
    "  Total operating income:                     FY2021 edition 244   -> FY2022 edition 241\n"
    "  Operating profit before impairment losses:  FY2021 edition 84    -> FY2022 edition 81\n"
    "  Operating profit before taxation:           FY2021 edition 92    -> line no longer presented\n"
    "  Loss on disposal of property:               FY2021 edition (3)   -> line no longer presented\n"
    "This is a genuine restatement BETWEEN EDITIONS, not a transcription error in either direction: both documents "
    "have been read and both were confirmed to print what is shown above (the FY2022 report's FY2021 comparative "
    "column literally reads 'Other operating income/(expense) ... (3)', 'Other income ... 43', 'Total operating "
    "income ... 241', 'Operating profit before impairment losses ... 81' with no disposal line beneath it). Profit "
    "before taxation (89) and profit for the year (170) are IDENTICAL on both bases - the reclassification moves "
    "£3m across the operating-profit subtotal without changing the bottom line. Per this project's validation gate, "
    "the two presentations are recorded on separate labelled rows and neither was overwritten: the main rows keep "
    "the FY2022-edition basis so that the FY2021 column is comparable with FY2022-FY2025 alongside it, and the "
    "'(as originally reported...)' memorandum rows at the foot of the sheet carry the FY2021 edition's own "
    "presentation. Anyone comparing this workbook against the FY2021 Annual Financial Report directly should read "
    "the memorandum rows.\n\n"
    + ENTITY_NOTE + "\n\n" + STATEMENT_ENTITY_NOTE + "\n\n" + ACCESS_ROUTE_NOTE
    + "\n\nDISCREPANCY FLAGGED: the FY2024 Annual Financial Report's own FY2023 comparative column (p.50) shows "
      "Profit for the year £275m / Total operating income £449m - these are the 'AIB UK' SOLO figures, not the "
      "£269m/£443m 'AIB UK Group' consolidated figures FY2023's own report used (matching the same Group-vs-solo "
      "entity switch as the balance sheet note above). This sheet uses FY2023's own report's Group-basis figures "
      "throughout for consistency with FY2021-FY2022. Separately, the FY2022 Annual Financial Report's narrative "
      "text states FY2021 profit as '£172m', but both the FY2021 income statement and statement of comprehensive "
      "income tables in the same report show the AIB UK Group figure as £170m (£172m is the AIB UK solo figure) - "
      "£170m (Group) is used here for consistency."
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 434, "FY2024": 470, "FY2023": 459, "FY2022": 280, "FY2021": 218}),
    ("DATA", "Interest and similar expense", {"FY2025": -136, "FY2024": -128, "FY2023": -81, "FY2022": -27, "FY2021": -20}),
    ("TOTAL", "Net interest income", {"FY2025": 298, "FY2024": 342, "FY2023": 378, "FY2022": 253, "FY2021": 198}),
    ("DATA", "Fee and commission income", {"FY2025": 38, "FY2024": 41, "FY2023": 42, "FY2022": 48, "FY2021": 45}),
    ("DATA", "Fee and commission expense", {"FY2025": -2, "FY2024": -4, "FY2023": -4, "FY2022": -4, "FY2021": -4}),
    ("DATA", "Net trading and other financial income/(expense)", {"FY2025": -1, "FY2024": 2, "FY2023": 2, "FY2022": 8, "FY2021": 7}),
    ("DATA", "Net gain/(loss) on other financial assets measured at FVTPL", {"FY2025": 0, "FY2024": -19, "FY2023": 23, "FY2022": 10, "FY2021": 6}),
    ("DATA", "Net gain/(loss) on derecognition of financial assets at amortised cost", {"FY2025": 0, "FY2024": 18, "FY2023": 1, "FY2022": -16, "FY2021": -8}),
    ("DATA", "Other operating income/(expense)", {"FY2025": 51, "FY2024": 12, "FY2023": 1, "FY2022": 2, "FY2021": -3}),
    ("TOTAL", "Total other income", {"FY2025": 86, "FY2024": 50, "FY2023": 65, "FY2022": 48, "FY2021": 43}),
    ("TOTAL", "Total operating income", {"FY2025": 384, "FY2024": 392, "FY2023": 443, "FY2022": 301, "FY2021": 241}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Operating expenses", {"FY2025": -125, "FY2024": -121, "FY2023": -117, "FY2022": -109, "FY2021": -141}),
    ("DATA", "Impairment and amortisation of intangible assets", {"FY2025": -5, "FY2024": -6, "FY2023": -6, "FY2022": -8, "FY2021": -8}),
    ("DATA", "Impairment and depreciation of property, plant and equipment", {"FY2025": -4, "FY2024": -4, "FY2023": -4, "FY2022": -5, "FY2021": -11}),
    ("TOTAL", "Total operating expenses", {"FY2025": -134, "FY2024": -131, "FY2023": -127, "FY2022": -122, "FY2021": -160}),
    ("TOTAL", "Operating profit before impairment losses", {"FY2025": 250, "FY2024": 261, "FY2023": 316, "FY2022": 179, "FY2021": 81}),
    ("DATA", "Net credit impairment charge/(writeback)", {"FY2025": -1, "FY2024": -21, "FY2023": 21, "FY2022": -41, "FY2021": 8}),
    ("DATA", "Impairment of investments in group undertakings", {"FY2025": 0, "FY2024": -1}),
    ("TOTAL", "Profit before taxation", {"FY2025": 249, "FY2024": 239, "FY2023": 337, "FY2022": 138, "FY2021": 89}),
    ("DATA", "Income tax charge/(credit)", {"FY2025": -12, "FY2024": -51, "FY2023": -68, "FY2022": -23, "FY2021": 81}),
    ("TOTAL", "Profit for the year", {"FY2025": 237, "FY2024": 188, "FY2023": 269, "FY2022": 115, "FY2021": 170}),
    ("SECTION", "Memorandum — FY2021 as originally reported (see validation-gate note below)", {}),
    ("DATA", "Other operating income (FY2021 as originally reported)", {"FY2021": 0}),
    ("DATA", "Other income (FY2021 as originally reported)", {"FY2021": 46}),
    ("DATA", "Total operating income (FY2021 as originally reported)", {"FY2021": 244}),
    ("DATA", "Operating profit before impairment losses and provisions (FY2021 as originally reported)", {"FY2021": 84}),
    ("DATA", "Operating profit before taxation (FY2021 as originally reported)", {"FY2021": 92}),
    ("DATA", "Loss on disposal of property, shown below operating profit (FY2021 as originally reported)", {"FY2021": -3}),
    ("DATA", "Profit before taxation (FY2021 as originally reported — unchanged by the reclassification)", {"FY2021": 89}),
    ("DATA", "Profit for the year (FY2021 as originally reported — unchanged by the reclassification)", {"FY2021": 170}),
]

bw.add_income_statement_sheet(
    title="AIB Group (UK) p.l.c. — Income Statement",
    subtitle="£m. Main rows: FY2022-edition basis for FY2021. See the memorandum rows and source note for the FY2021 inter-edition reclassification, plus the Group (FY2021-FY2023) vs solo (FY2024-FY2025) entity-basis switch.",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=76,
    source_height=900,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_CHANGES_SOURCES = (
    "Sources - Statement of changes in equity, £m ('AIB UK Group' consolidated column FY2021-FY2023, solo/Company "
    "column FY2024-FY2025):\n"
    f"FY2021 movements + 1 Jan 2021 opening balance: FY2021 Annual Financial Report, printed p.69 ('AIB UK Group' "
    f"block), retrieved from Companies House - {AR2021_URL}\n"
    f"  (previously cited to the FY2022 Annual Financial Report's FY2021 comparative block, p.71 - {AR2022_URL} - "
    f"which reproduces the primary line for line; see the validation-gate note below)\n"
    f"FY2022 movements: FY2022 Annual Financial Report, p.71 - {AR2022_URL}\n"
    f"FY2023 movements: FY2023 Annual Financial Report, p.71 ('AIB UK Group' block) - {AR2023_URL}\n"
    f"FY2024 movements + 1 Jan 2024 opening balance: FY2025 Annual Financial Report, p.35 (FY2024 statement) - {AR2025_URL}\n"
    f"FY2025 movements: FY2025 Annual Financial Report, p.34 - {AR2025_URL}\n\n"
    + "FY2021 VALIDATION GATE (2026-09-16): the FY2021 rows here were previously read off the FY2022 edition's "
      "FY2021 comparative block. The FY2021 Annual Financial Report has now been retrieved from Companies House "
      "(see ACCESS ROUTE NOTE) and its own 'AIB UK Group' roll-forward re-read: it REPRODUCES every figure exactly "
      "- At 1 January 2021 share capital 2,384 / other reserves 2 / cash flow hedging reserve 33 / retained "
      "earnings (745) / total equity 1,674; profit for the year 170; other comprehensive income net of tax (57) on "
      "the hedging reserve and 5 on retained earnings, total (52); total comprehensive income (57) / 175 / 118; At "
      "31 December 2021 2,384 / 2 / (24) / (570) / 1,792. This is a clean confirmation with no divergence, and the "
      "citation is upgraded from the following year's comparative block to the primary document. (The FY2021 report "
      "labels the last movement column 'Retained earnings' where FY2022 onward calls it 'Revenue reserves' - the "
      "same column, renamed, and (570) ties to the FY2021 balance sheet's own retained-earnings line.)\n\n"
    + ENTITY_NOTE + "\n\n" + STATEMENT_ENTITY_NOTE + "\n\n" + ACCESS_ROUTE_NOTE
    + "\n\nJUDGEMENT CALL: FY2021-FY2022 reports disclose only a single combined 'Other reserves' column (not split "
      "into Capital redemption / Revaluation reserves as FY2023 onward does) - since AIB UK's Capital redemption "
      "reserve was only created by the November 2023 share buyback, the FY2021-FY2022 'Other reserves' figures are "
      "mapped to the 'Revaluation reserves' column here (Capital redemption reserves left blank for those years). "
      "CONFIRMED 2026-09-16 against the FY2021 primary, which settles this rather than leaving it a judgement: the "
      "FY2021 Annual Financial Report's note 35 (printed p.144) breaks out the combined 'Other reserves' column and "
      "names its sole component in terms - 'Revaluation reserves at beginning and end of year ... AIB UK Group "
      "2021: 2, 2020: 2' - so the £2m mapped into the Revaluation reserves column above IS a revaluation reserve, "
      "not an unclassified residual."
)

EQUITY_HEADERS = ["Share capital", "Capital redemption reserves", "Revaluation reserves",
                   "Cash flow hedging reserve", "Revenue reserves", "Other equity interests (AT1)", "Total equity"]

equity_changes_rows = [
    ("TOTAL", "Balance at 1 January 2021", (2384, None, 2, 33, -745, None, 1674)),
    ("DATA", "Profit for the year", (None, None, None, None, 170, None, 170)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, None, -57, 5, None, -52)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, -57, 175, None, 118)),
    ("TOTAL", "Balance at 31 December 2021", (2384, None, 2, -24, -570, None, 1792)),
    ("DATA", "Profit for the year", (None, None, None, None, 115, None, 115)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, None, -185, -68, None, -253)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, -185, 47, None, -138)),
    ("DATA", "Other movements", (None, None, -1, None, 1, None, 0)),
    ("TOTAL", "Balance at 31 December 2022", (2384, None, 1, -209, -522, None, 1654)),
    ("DATA", "Profit for the year", (None, None, None, None, 269, None, 269)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, None, 73, -2, None, 71)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, 73, 267, None, 340)),
    ("DATA", "Capital reduction", (-1788, None, None, None, 1788, None, 0)),
    ("DATA", "Buyback of ordinary shares", (-139, 139, None, None, -250, None, -250)),
    ("DATA", "Issue of Additional Tier 1 securities", (None, None, None, None, None, 110, 110)),
    ("DATA", "Other movements", (None, None, None, None, -1, None, -1)),
    ("TOTAL", "Balance at 31 December 2023 (AIB UK Group basis)", (457, 139, 1, -136, 1282, 110, 1853)),
    ("TOTAL", "Balance at 1 January 2024 (AIB UK solo basis - entity switch, see note)", (457, 139, 1, -136, 1281, 110, 1852)),
    ("DATA", "Profit for the year", (None, None, None, None, 188, None, 188)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, None, -20, -9, None, -29)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, -20, 179, None, 159)),
    ("DATA", "Dividends paid on ordinary shares", (None, None, None, None, -107, None, -107)),
    ("DATA", "Distributions paid on other equity interests", (None, None, None, None, -11, None, -11)),
    ("TOTAL", "Balance at 31 December 2024", (457, 139, 1, -156, 1342, 110, 1893)),
    ("DATA", "Profit for the year", (None, None, None, None, 237, None, 237)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, None, 49, -19, None, 30)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, 49, 218, None, 267)),
    ("DATA", "Dividends paid on ordinary shares", (None, None, None, None, -88, None, -88)),
    ("DATA", "Distributions paid on other equity interests", (None, None, None, None, -11, None, -11)),
    ("DATA", "Other movements", (None, None, -1, None, 1, None, 0)),
    ("TOTAL", "Balance at 31 December 2025", (457, 139, 0, -107, 1462, 110, 2061)),
]

bw.add_equity_changes_sheet(
    title="AIB Group (UK) p.l.c. — Statement of Changes in Equity",
    subtitle="£m, chronological (oldest to newest). See source note at bottom for the Group-to-solo entity-basis break between FY2023 and FY2024.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=58,
    source_height=680,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    # GA-018 (2026-09-18): FY2025 and FY2024 previously left every cell on this
    # sheet EMPTY, which a reader cannot distinguish from "nobody has looked
    # yet". The absence is evidenced, dated and quoted (see
    # CASH_FLOW_EXEMPTION_NOTE), so it is now STATED in the cells rather than
    # implied by their emptiness. Same treatment as the Leverage Ratio sheet
    # and the NOT_DISCLOSED_BY_YEAR pattern used in
    # scripts/build_nomura_bank_international.py.
    ("SECTION", "FY2025 and FY2024 — no Statement of Cash Flows was published for either year", {}),
    ("DATA", "Statement of Cash Flows for the year",
     {"FY2025": "Not published — FRS 101 cash-flow exemption taken",
      "FY2024": "Not published — FRS 101 cash-flow exemption taken"}),
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before taxation for the year", {"FY2023": 337, "FY2022": 138, "FY2021": 89}),
    ("DATA", "Non-cash items", {"FY2023": -29, "FY2022": 67, "FY2021": 27}),
    ("TOTAL", "Net cash inflow from operating activities before changes in operating assets and liabilities",
     {"FY2023": 308, "FY2022": 205, "FY2021": 116}),
    ("DATA", "Change in loans and advances to banks", {"FY2023": -72, "FY2022": 142, "FY2021": -73}),
    ("DATA", "Change in loans and advances to customers", {"FY2023": 88, "FY2022": 419, "FY2021": 679}),
    ("DATA", "Change in deposits by banks", {"FY2023": -16, "FY2022": -18, "FY2021": -32}),
    ("DATA", "Change in customer accounts", {"FY2023": -1086, "FY2022": -1884, "FY2021": 109}),
    ("DATA", "Change in derivative financial instruments", {"FY2023": 3, "FY2022": -3, "FY2021": 2}),
    ("DATA", "Change in notes in circulation", {"FY2023": -6, "FY2022": -44, "FY2021": -50}),
    ("DATA", "Change in other assets", {"FY2023": 42, "FY2022": -37, "FY2021": 1}),
    ("DATA", "Change in other liabilities", {"FY2023": -1, "FY2022": -64, "FY2021": 1}),
    ("TOTAL", "Net cash (outflow)/inflow from operating assets and liabilities",
     {"FY2023": -1048, "FY2022": -1489, "FY2021": 637}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities before taxation",
     {"FY2023": -740, "FY2022": -1284, "FY2021": 753}),
    ("DATA", "Taxation (paid)/refund", {"FY2023": -54, "FY2022": 2, "FY2021": -3}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities", {"FY2023": -794, "FY2022": -1282, "FY2021": 750}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Additions to property, plant and equipment", {"FY2023": 0, "FY2022": -4, "FY2021": -7}),
    ("DATA", "Proceeds from disposals of property, plant and equipment", {"FY2023": 1, "FY2022": 1, "FY2021": 0}),
    ("DATA", "Additions to intangible assets", {"FY2023": -4, "FY2022": -2, "FY2021": -4}),
    ("TOTAL", "Net cash outflow from investing activities", {"FY2023": -3, "FY2022": -5, "FY2021": -11}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Buyback of ordinary shares", {"FY2023": -250}),
    ("DATA", "Proceeds on issues of debt securities", {"FY2023": 140}),
    ("DATA", "Net proceeds on issue of additional Tier 1 securities", {"FY2023": 110}),
    ("DATA", "Repayment of secondary non-preferential debt", {"FY2022": 0, "FY2021": -45}),
    ("DATA", "Repayment of lease liabilities", {"FY2023": -3, "FY2022": -9, "FY2021": -3}),
    ("TOTAL", "Net cash outflow from financing activities", {"FY2023": -3, "FY2022": -9, "FY2021": -48}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2023": -800, "FY2022": -1296, "FY2021": 691}),
    ("DATA", "Opening cash and cash equivalents", {"FY2023": 4057, "FY2022": 5353, "FY2021": 4662}),
    ("TOTAL", "Closing cash and cash equivalents", {"FY2023": 3257, "FY2022": 4057, "FY2021": 5353}),
    ("SECTION", "Memorandum — FY2021 as originally reported (see validation-gate note below)", {}),
    ("DATA", "Net decrease in items in course of collection (FY2021 as originally reported; folded into 'Change in other assets' by the FY2022 edition)", {"FY2021": 1}),
    ("DATA", "Net decrease in other assets, excluding items in course of collection (FY2021 as originally reported)", {"FY2021": 0}),
    ("DATA", "Dividends received from subsidiary undertakings (FY2021 as originally reported — nil on the AIB UK Group basis used here)", {"FY2021": 0}),
]

bw.add_cash_flow_sheet(
    title="AIB Group (UK) p.l.c. — Statement of Cash Flows",
    subtitle="AIB UK Group (consolidated) basis, £m. FY2024-FY2025 blank - see source note at bottom (FRS 101 cash-flow exemption). FY2021 is now primary-sourced; see the memorandum rows.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=96,
    source_height=600,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - loans and advances to customers, by internal credit grading and IFRS 9 stage (at amortised cost), £m:\n"
    f"FY2025 and FY2024: FY2025 Annual Financial Report, p.73 (Note 20(f), 'Credit profile of the loan portfolio') "
    f"and p.79 (Note 20(h), ECL allowance movements) - {AR2025_URL}\n"
    f"FY2023 and FY2022: FY2023 Annual Financial Report, p.120 (Note 21(f)) - {AR2023_URL}\n"
    f"FY2021: FY2021 Annual Financial Report, printed p.118 ('Credit profile of the loan portfolio', the internal "
    f"credit grading profile by ECL staging at 31 December 2021), retrieved from Companies House - {AR2021_URL}\n"
    f"  (previously cited to the FY2022 Annual Financial Report's FY2021 comparative, p.120 - {AR2022_URL})\n\n"
    "FY2021 VALIDATION GATE (2026-09-16): re-read from the FY2021 primary, every FY2021 figure on this sheet "
    "REPRODUCES - Total strong/satisfactory 5,210 (Stage 1 4,736 / Stage 2 474 / Stage 3 nil), Criticised watch "
    "242, Criticised recovery 435, Total criticised 677 (Stage 1 55 / Stage 2 622), Non-performing 512, Gross "
    "carrying amount 6,399 (Stage 1 4,791 / Stage 2 1,096 / Stage 3 512), ECL allowance (201) (Stage 1 (28) / "
    "Stage 2 (80) / Stage 3 (93)), carrying amount 6,198. OCR CAUTION FOR ANY FUTURE PASS: on this scanned page "
    "tesseract read the Criticised watch row as 187 - that is the Stage 2 cell; the Total column reads 242, "
    "confirmed visually against the rendered page image (and 242 + 435 = 677, the printed Total criticised). "
    "Do not transcribe 187 into the Criticised watch row.\n"
    "The FY2021 primary also CONFIRMS the Strong/Satisfactory finding already recorded below: its own credit "
    "profile table shows a single combined 'Total strong/satisfactory' line with no Strong vs. Satisfactory split "
    "for either 2021 or 2020. So the blank FY2021 Strong and Satisfactory cells are now evidenced against the "
    "FY2021 report itself, not merely inferred from the FY2022 report's presentation - AIB UK had genuinely not "
    "begun publishing that split. Those two cells should not be re-chased.\n\n"
    + ENTITY_NOTE + "\n\n" + ACCESS_ROUTE_NOTE
    + "\n\nPRESENTATION NOTE: AIB UK does not disclose loans and advances to customers by product (e.g. mortgages "
      "vs. term loans vs. overdrafts) at a group total level - only a credit-quality/stage breakdown and a "
      "sector-concentration breakdown (not reproduced here as a distinct line item set). 'Non-performing' = Stage 3 "
      "throughout. Coverage/NPL ratios below are CALCULATED from the gross carrying amount and ECL allowance "
      "figures above (AIB UK does not itself publish these ratios as named percentages, aside from the "
      "£0.3bn/4.4%-of-gross-loans NPL figure narrated in the FY2023 Financial review, which matches the calculated "
      "FY2023 Stage 3/NPL ratio here exactly).\n\n"
      "CORRECTION (HD-066 correctness audit): FY2023 and FY2022 Strong/Satisfactory were previously wrongly left "
      "blank on the assumption only the combined 'Total strong/satisfactory' figure was disclosed for those years. "
      "The FY2023 Annual Financial Report's own Note 21(f) (p.120) in fact splits both years: FY2023 Strong £4,233m "
      "/ Satisfactory £998m (sums to the Total strong/satisfactory £5,231m already shown), FY2022 Strong £3,959m / "
      "Satisfactory £1,092m (sums to £5,051m) - both now added. FY2021 genuinely has no such split anywhere - the "
      "FY2022 Annual Financial Report's own Note 21(f) (p.119, covering FY2022/FY2021) shows only the combined "
      "'Total strong/satisfactory' line for both years, i.e. AIB UK had not yet started publishing the split as of "
      "that report - FY2021 Strong/Satisfactory cells remain blank accordingly."
)

asset_quality_rows = [
    ("SECTION", "Gross carrying amount, by credit quality", {}),
    ("DATA", "Strong", {"FY2025": 3038, "FY2024": 2746, "FY2023": 4233, "FY2022": 3959}),
    ("DATA", "Satisfactory", {"FY2025": 2093, "FY2024": 1711, "FY2023": 998, "FY2022": 1092}),
    ("TOTAL", "Total strong/satisfactory", {"FY2025": 5131, "FY2024": 4457, "FY2023": 5231, "FY2022": 5051, "FY2021": 5210}),
    ("DATA", "Criticised watch", {"FY2025": 65, "FY2024": 51, "FY2023": 147, "FY2022": 174, "FY2021": 242}),
    ("DATA", "Criticised recovery", {"FY2025": 75, "FY2024": 111, "FY2023": 149, "FY2022": 361, "FY2021": 435}),
    ("TOTAL", "Total criticised", {"FY2025": 140, "FY2024": 162, "FY2023": 296, "FY2022": 535, "FY2021": 677}),
    ("DATA", "Non-performing (Stage 3)", {"FY2025": 95, "FY2024": 210, "FY2023": 253, "FY2022": 329, "FY2021": 512}),
    ("TOTAL", "Gross carrying amount", {"FY2025": 5366, "FY2024": 4829, "FY2023": 5780, "FY2022": 5915, "FY2021": 6399}),
    ("SECTION", "Gross carrying amount, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 4951, "FY2024": 4127, "FY2023": 4879, "FY2022": 4614, "FY2021": 4791}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": 320, "FY2024": 492, "FY2023": 648, "FY2022": 972, "FY2021": 1096}),
    ("DATA", "Stage 3 (non-performing)", {"FY2025": 95, "FY2024": 210, "FY2023": 253, "FY2022": 329, "FY2021": 512}),
    ("TOTAL", "Gross carrying amount (by stage)", {"FY2025": 5366, "FY2024": 4829, "FY2023": 5780, "FY2022": 5915, "FY2021": 6399}),
    ("SECTION", "ECL allowance, by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2025": -32, "FY2024": -22, "FY2023": -39, "FY2022": -33, "FY2021": -28}),
    ("DATA", "Stage 2", {"FY2025": -18, "FY2024": -21, "FY2023": -41, "FY2022": -82, "FY2021": -80}),
    ("DATA", "Stage 3", {"FY2025": -25, "FY2024": -78, "FY2023": -53, "FY2022": -82, "FY2021": -93}),
    ("TOTAL", "Total ECL allowance", {"FY2025": -75, "FY2024": -121, "FY2023": -133, "FY2022": -197, "FY2021": -201}),
    ("TOTAL", "Loans and advances to customers, net carrying amount", {"FY2025": 5291, "FY2024": 4708, "FY2023": 5647, "FY2022": 5718, "FY2021": 6198}),
    ("SECTION", "Asset quality ratios (calculated)", {}),
    ("DATA", "ECL coverage ratio (Total ECL allowance / Gross carrying amount)", {"FY2025": "1.40%", "FY2024": "2.51%", "FY2023": "2.30%", "FY2022": "3.33%", "FY2021": "3.14%"}),
    ("DATA", "Stage 3 (NPL) ratio (Stage 3 gross / Gross carrying amount)", {"FY2025": "1.77%", "FY2024": "4.35%", "FY2023": "4.38%", "FY2022": "5.56%", "FY2021": "8.00%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", {"FY2025": "26.32%", "FY2024": "37.14%", "FY2023": "20.95%", "FY2022": "24.92%", "FY2021": "18.16%"}),
]

bw.add_asset_quality_sheet(
    title="AIB Group (UK) p.l.c. — Asset Quality / Credit Risk Disclosures",
    subtitle="Loans and advances to customers at amortised cost, £m. See entity note on the Cash Flow Statement sheet.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=62,
    source_height=760,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else "", rows_data, sources_text,
                         note=note, first_col_width=52, source_height=860, note_height=320)


# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics (KM1-003)
# ---------------------------------------------------------------
# AIB Group (UK) p.l.c. PUBLISHES NO KM1. This sheet exists to say so with its
# evidence attached, because "we could not reach it" and "it is not published"
# are different findings and only one of them is safe to record (map rule 9).
#
# WHAT WAS POSITIVELY CHECKED, 2026-09-16:
#  * The FY2025 and FY2024 Annual Financial Reports were fetched from aib.ie
#    (HTTP 200, application/pdf, %PDF verified), are text-native, and extract
#    to 646,006 and 658,542 characters respectively. Full-text searched
#    case-insensitively, both contain ZERO occurrences of "KM1" and ZERO of
#    "Pillar 3". Every occurrence of "pillar" is one of three other things:
#    the Pillar 1 / Pillar 2a capital requirement (11.21% for 2025, 9.77% for
#    2024), the bank's "strategic pillars" narrative, or the OECD Pillar Two
#    global minimum top-up tax. The FY2024 report's own glossary defines
#    "Pillar 1" and "Pillar 2a" and does not define Pillar 3 at all.
#  * aib.ie's investor-relations tree was READ, not guessed: /investorrelations
#    (90 links), /investorrelations/financial-information (86) and
#    .../results-centre (92) all returned HTTP 200, and not one link on any of
#    them matches pillar, regulat or disclos. The only PDFs offered are a
#    whistleblowing policy, a financial calendar, a dividend-payments note,
#    terms of business and a code of conduct.
#
# WHAT IS *NOT* EXCLUDED, AND MUST NOT BE WRITTEN DOWN AS IF IT WERE:
#    aibgb.co.uk, www.aibgb.co.uk and aibni.co.uk each returned HTTP 403 with a
#    ~365-byte body on 2026-09-16 (an edge deny, not even a challenge page).
#    web.archive.org returned "Temporarily Offline" throughout, so the archive
#    route could not be tried at all. If a standalone AIB UK Pillar 3 document
#    exists anywhere, that blocked host is where it would live. This is the
#    same shape of evidence that produced a false "publishes no Pillar 3"
#    claim for Bank of Scotland, so the claim below is deliberately bounded.
#
# THE IRISH PARENT'S KM1 IS A DIFFERENT ENTITY AND IS NOT WIRED IN. AIB Group
# plc publishes Ireland-wide consolidated Pillar 3 disclosures containing a
# full KM1, and those documents dominate any search for "AIB Pillar 3" - an
# earlier pass of this script surfaced them first and correctly discarded them.
# A parent's consolidated KM1 can never stand in for a UK subsidiary's own.
km1_rows = [
    ("DATA", "UK KM1 - Key metrics template: not published by this entity",
     {y: "Not applicable" for y in YEARS}),
]

KM1_SOURCES = (
    "AIB Group (UK) p.l.c. does not publish a UK KM1 key-metrics template, and does not publish a standalone "
    "Pillar 3 disclosure document at all. Its capital and liquidity metrics are disclosed inside the Annual "
    "Financial Report, in the 'Capital management and liquidity' section, and those figures are carried on the "
    "eleven single-metric Pillar 3 sheets in this workbook under their own citations. Nothing on this sheet is "
    "back-filled from the statutory accounts: the accounts are a different basis and do not contain the "
    "template's rows.\n"
    "\n"
    "POSITIVE EVIDENCE FOR THAT STATEMENT, checked 2026-09-16 (not inferred from a failed fetch):\n"
    f"1. FY2025 Annual Financial Report ({AR2025_URL}) and FY2024 Annual Financial Report ({AR2024_URL}) were "
    "both retrieved (HTTP 200, application/pdf, %PDF magic bytes verified), are text-native, and extract to "
    "646,006 and 658,542 characters. Searched case-insensitively, each contains ZERO occurrences of 'KM1' and "
    "ZERO of 'Pillar 3'. Every 'pillar' in either document is the Pillar 1 / Pillar 2a capital requirement, the "
    "bank's 'strategic pillars' narrative, or the OECD Pillar Two top-up tax. The FY2024 report's glossary "
    "defines Pillar 1 and Pillar 2a and contains no Pillar 3 entry.\n"
    "2. aib.ie's investor-relations tree was read by following its own links rather than by guessing paths: "
    "/investorrelations, /investorrelations/financial-information and "
    "/investorrelations/financial-information/results-centre all returned HTTP 200 (90, 86 and 92 links "
    "respectively), and none of those links matches 'pillar', 'regulat' or 'disclos'. The only PDFs published "
    "there are a whistleblowing policy, a financial calendar, a dividend-payments note, terms of business and a "
    "code of conduct.\n"
    "\n"
    "WHAT THIS CHECK DOES NOT COVER - stated plainly so it is not mistaken for a complete search. On "
    "2026-09-16 aibgb.co.uk, www.aibgb.co.uk and aibni.co.uk each returned HTTP 403 with a ~365-byte body, and "
    "web.archive.org was 'Temporarily Offline' for the whole session, so neither the bank's own UK-facing site "
    "nor the archive could be examined. A blocked host is not an empty one. If a standalone AIB UK Pillar 3 "
    "document exists, that host is the likeliest place for it, and this sheet should be re-tested when either "
    "route becomes reachable. (The same class of evidence - a Cloudflare block recorded as a fact about the "
    "bank - produced a false 'publishes no Pillar 3' statement for Bank of Scotland elsewhere in this corpus.)\n"
    "\n"
    "THE IRISH PARENT'S PILLAR 3 IS DELIBERATELY NOT USED. AIB Group plc (Dublin, company 594283) publishes "
    "Ireland-wide consolidated Pillar 3 disclosures that do contain a full KM1, and they dominate search "
    "results for 'AIB Pillar 3'. AIB Group (UK) p.l.c. (FRN 122088, Companies House NI018800) is a different "
    "legal entity, roughly an order of magnitude smaller. Substituting the parent's consolidated template for "
    "the subsidiary's own would put the wrong bank's figures in this workbook, so it is excluded on entity "
    "grounds and not merely on convenience.\n"
    "\n"
    "ENTITY-BASIS NOTE carried over from the rest of this workbook: FY2021-FY2023 figures are the 'AIB UK "
    "Group' (consolidated) column of each year's own Annual Financial Report, while FY2024-FY2025 are AIB Group "
    "(UK) p.l.c.'s single (solo/Company) column, because a separate consolidated basis ceased being reported "
    "once the FRS 101 exemptions took effect. Had a KM1 existed, its columns would have had to straddle that "
    "same break.\n"
    "\n"
    "LATEST-EDITION CHECK: aib.ie's document tree was read 2026-09-16 as described above. The newest AIB Group "
    "(UK) p.l.c. Annual Financial Report is FY2025 (year ended 31 December 2025), already cited by this script. "
    "None newer. The bank's own aibgb.co.uk site could not be checked (403)."
)

bw.add_km1_sheet(
    title="AIB Group (UK) p.l.c. - KM1 Key Metrics",
    subtitle="Not applicable: AIB Group (UK) p.l.c. publishes no UK KM1 key-metrics template and no standalone "
             "Pillar 3 document. Its capital and liquidity metrics appear inside the Annual Financial Report "
             "and are carried on the eleven single-metric sheets. See the note below for what was positively "
             "checked, what remains unchecked because the bank's own UK site is blocked, and why the Irish "
             "parent's Pillar 3 KM1 is not used here.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=64,
    source_height=300,
    years=YEARS,
)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital, transitional", {"FY2025": 1614, "FY2024": 1533, "FY2023": 1407, "FY2022": 1531, "FY2021": 1508})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio, transitional", {"FY2025": "26.8%", "FY2024": "27.7%", "FY2023": "21.44%", "FY2022": "24.11%", "FY2021": "22.81%"})],
    p3_sources("PROVENANCE UPGRADE (2026-09-16): FY2021's 22.81% was previously flagged in this script as CALCULATED "
               "(CET1 / RWA), because the FY2022 Annual Financial Report never states the FY2021 percentage - that "
               "remains true of the FY2022 report (it says only 'Transitional CET1 of 24.11% increased in the year', "
               "and its highlights page carries the 2022 ratio alone). But the FY2021 Annual Financial Report states "
               "it DIRECTLY: 'Capital ratio at 31 December 2021 ... 22.81% [transitional] / 22.01% [fully loaded]' "
               "(p.20), with the narrative on p.21 repeating 'Transitional CET1 of 22.81%' and 'a fully loaded "
               "capital ratio of 22.01%', and the highlights page (p.3) showing 22.8%. The derived figure happened "
               "to be right, but it is no longer derived: this row is now transcribed from the primary throughout, "
               "and the CALCULATED caveat is withdrawn."),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 1724, "FY2024": 1643, "FY2023": 1517, "FY2022": 1531, "FY2021": 1508})],
    p3_sources(),
    note="Tier 1 Capital = CET1 Capital for FY2021-FY2022 (no Additional Tier 1 instruments outstanding yet). AIB "
         "UK issued £110m of AT1 as part of a November 2023 capital restructure; Tier 1 Capital from FY2023 onward "
         "is CALCULATED as CET1 + AT1 (£110m every year FY2023-FY2025) - AIB UK's own disclosures give CET1 and "
         "Total Capital explicitly but never break out a separate 'Tier 1' capital or ratio line. The FY2021 = CET1 "
         "equivalence is now confirmed against the FY2021 Annual Financial Report itself (Companies House copy, "
         "2026-09-16): its statement of financial position at 31 December 2021 shows shareholders' equity as share "
         "capital, reserves and retained earnings only, with no 'other equity interests'/AT1 line and no "
         "subordinated liabilities (the only such instrument, £45m of secondary non-preferential debt, stood at nil "
         "at 31 December 2021 having been repaid during the year - see the FY2021 cash flow's 'Repayment of "
         "secondary non-preferential debt (45)').",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio (calculated: Tier 1 Capital ÷ RWA)", {"FY2025": "28.64%", "FY2024": "29.66%", "FY2023": "23.11%", "FY2022": "24.11%", "FY2021": "22.81%"})],
    p3_sources("Entirely CALCULATED (Tier 1 Capital ÷ Total RWA) - AIB UK does not disclose a Tier 1 ratio as a "
               "distinct line anywhere in its Annual Financial Reports. Re-confirmed for FY2021 on 2026-09-16 "
               "against the FY2021 Annual Financial Report itself (Companies House copy, full-text searched): its "
               "capital section discloses CET1 and the CET1/capital ratio only, with no Tier 1 capital and no "
               "Tier 1 ratio line - so FY2021 stays calculated too."),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 1865, "FY2024": 1783, "FY2023": 1657, "FY2022": 1531, "FY2021": 1508})],
    p3_sources("FY2021's £1,508m is Total Capital = CET1, not a separately disclosed 'Total capital' figure: the "
               "FY2021 Annual Financial Report (read directly from the Companies House copy, 2026-09-16) never "
               "states a Total Capital amount - its capital table runs to 'CET1 at 31 December 2021 1,508' and "
               "stops - and the same report's balance sheet confirms there was no AT1 and no Tier 2 outstanding at "
               "that date (see the Tier 1 Capital sheet's note), so the two are equal by construction rather than "
               "by back-solving."),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio, transitional", {"FY2025": "31.0%", "FY2024": "32.3%", "FY2023": "25.24%", "FY2022": "24.11%", "FY2021": "22.81%"})],
    p3_sources("FY2021-FY2022 Total Capital Ratio = CET1 Ratio (no AT1/Tier 2 outstanding, so Total Capital = CET1 "
               "those two years)."),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets, transitional", {"FY2025": 6020, "FY2024": 5540, "FY2023": 6564, "FY2022": 6352, "FY2021": 6611})],
    p3_sources(),
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - RWA breakdown by risk category, transitional basis, £m:\n"
    f"FY2025: FY2025 Annual Financial Report, p.5 - {AR2025_URL}\n"
    f"FY2024: FY2024 Annual Financial Report, p.11 - {AR2024_URL}\n"
    f"FY2023: FY2023 Annual Financial Report, p.18 - {AR2023_URL}\n"
    f"FY2022: FY2023 Annual Financial Report, p.18 (FY2022 comparative - the FY2022 Annual Financial Report itself "
    f"discloses only the FY2021-to-FY2022 category-level RWA movement/waterfall, not FY2022's own absolute "
    f"category split, so the next year's report is used instead; the resulting FY2022 Total (£6,352m) still ties "
    f"to the Total RWAs sheet) - {AR2023_URL}\n"
    f"FY2021: not available at category level - and, as of 2026-09-16, this is now an EVIDENCED absence rather than "
    f"an assumed one. The FY2021 Annual Financial Report itself was retrieved from Companies House and read "
    f"directly (see ACCESS ROUTE NOTE), and its RWA table on printed p.20 has exactly the same movement shape as "
    f"every other year's: it opens 'At 31 December 2020 7,353 [transitional] / 7,266 [fully loaded]', shows the "
    f"year's movements by category (Credit risk (734)/(704), Operational risk (8)/(8)) and closes 'At 31 December "
    f"2021 6,611 / 6,554'. That yields FY2021's absolute TOTAL RWA, which is already on the Total RWAs sheet and "
    f"in the Total row below, but no absolute FY2021 credit-risk/operational-risk/CVA split - a movement is not a "
    f"split and must not be back-solved from one. So the FY2021 category cells stay blank across all five now-read "
    f"Annual Financial Reports (FY2021's own, plus FY2022-FY2025) - {AR2021_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + ACCESS_ROUTE_NOTE
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk", {"FY2025": 5258, "FY2024": 4802, "FY2023": 5920, "FY2022": 5835}),
    ("DATA", "Operational risk", {"FY2025": 762, "FY2024": 737, "FY2023": 644, "FY2022": 516}),
    ("DATA", "CVA", {"FY2025": 0, "FY2024": 1, "FY2023": 0, "FY2022": 1}),
    ("TOTAL", "Total RWA", {"FY2025": 6020, "FY2024": 5540, "FY2023": 6564, "FY2022": 6352, "FY2021": 6611}),
]

bw.add_rwa_breakdown_sheet(
    title="AIB Group (UK) p.l.c. — RWA Breakdown",
    subtitle="Transitional basis, £m. FY2021 category-level split not disclosed - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=52,
    source_height=600,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2025": "Not published — outside UK LREQ scope from 1 January 2022",
                         "FY2024": "Not published — outside UK LREQ scope from 1 January 2022",
                         "FY2023": "Not published — outside UK LREQ scope from 1 January 2022",
                         "FY2022": "Not published — outside UK LREQ scope from 1 January 2022",
                         "FY2021": "11.26%"})],
    p3_sources(),
    note="GA-018 (2026-09-18): FY2022-FY2025 now STATE the absence in the cell instead of leaving it empty. "
         "Nothing about the finding changed - the evidence below was already here - but an empty cell and an "
         "evidenced absence had been made to look identical, and only one of them is safe to read as a finding. "
         "The absence was re-confirmed first-hand on 2026-09-18 by full-text search of all four FY2022-FY2025 "
         "Annual Financial Reports: the phrase 'leverage ratio' occurs ZERO times in the FY2023, FY2024 and "
         "FY2025 reports, and in FY2022 only inside the 'Regulatory changes' note quoted below. The word "
         "'leverage' does occur in all four (1, 3, 4 and 3 times respectively) and every occurrence was read "
         "individually - all are unrelated prose ('leverages AIB Group's cyber capabilities', 'Leverage "
         "features', 'deleveraged through a portfolio sale'). Richness control on the same extractions, so the "
         "zeroes are facts about the documents and not about the search: 'capital' and 'ratio' return healthy "
         "counts in every edition and the reports' capital sections were read directly.\n"
         "Only FY2021 is disclosed - a one-off figure mentioned in the FY2022 Annual Financial Report's "
         "'Regulatory changes' note ('...significantly increased the Bank's leverage ratio from 11.26% in "
         "December 2021 to 20.22% in March 2022' following a PRA leverage-framework methodology change, PRA "
         "Policy Statement 21/21). No FY2022-FY2025 year-end leverage ratio figure appears anywhere in any of the "
         "five Annual Financial Reports - AIB UK's 'Capital management and liquidity' section covers CET1/Total "
         "Capital/RWA/LCR/NSFR every year but never a leverage ratio outside that single FY2021 mention.\n"
         "IMPORTANT PROVENANCE POINT (2026-09-16): the FY2021 figure is NOT in the FY2021 Annual Financial Report. "
         "That report was retrieved from Companies House and read directly (see ACCESS ROUTE NOTE), and the word "
         "'leverage' appears in it only in unrelated credit-risk prose ('leverage lending portfolio', 'highly "
         "leveraged exposures') - there is no leverage ratio figure, no leverage exposure measure, and no glossary "
         "entry for it. So this row's sole source remains the FY2022 Annual Financial Report's backward-looking "
         "narrative sentence, even now that the FY2021 primary is in hand. Recorded explicitly so a future pass "
         "does not re-open the FY2021 report expecting to find it.\n"
         "The FY2022 break is STRUCTURAL, not an unsourced document. PS21/21 (October 2021, effective "
         "1 January 2022) set the scope of the UK leverage ratio requirement at firms with UK retail deposits "
         ">= GBP 50bn or non-UK assets >= GBP 10bn (PS21/21 paras 1.6, 2.4 and 5.8). AIB Group (UK) p.l.c. is far "
         "below both - GBP 10.3bn TOTAL assets and GBP 7.6bn customer deposits at FY2025 - so it ceased to be an "
         "'LREQ firm' from 1 January 2022, exactly when the disclosure stops. PS21/21 Table 4 (para 5.79) confirms "
         "the 'additional' leverage disclosures (averaged metrics, buffers, distance to requirement) apply on an "
         "LREQ basis only. Consistent with this, AIB UK publishes no Pillar 3 document at all: the string "
         "'Pillar 3' does not appear anywhere in the FY2025 Annual Financial Report, and every capital/liquidity "
         "figure in this workbook is taken from the Annual Report's own narrative capital section. "
         "PS21/21 - https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/policy-statement/2021/october/ps2121.pdf",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {"FY2025": "216%", "FY2024": "282%", "FY2023": "216%", "FY2022": "176%", "FY2021": "169%"})],
    p3_sources("BASIS: every year on this row is a POINT-IN-TIME year-end LCR taken from the Annual Financial "
               "Report's own liquidity narrative - not a 12-month average. FY2021's wording, read directly from the "
               "primary on 2026-09-16, is explicit about that: 'As at 31 December 2021 AIB UK Group's LCR was 169% "
               "(2020: 178%)' (FY2021 Annual Financial Report, p.21). AIB UK publishes no Pillar 3 KM1 table, so "
               "there is no 12-month-average series to confuse this with, and none should be merged into this row "
               "if one later surfaces."),
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {"FY2025": "157%", "FY2024": "172%", "FY2023": "139%", "FY2022": "145%", "FY2021": "156%"})],
    p3_sources("FY2021 SOURCING (2026-09-16): FY2021's 156% is the one metric on this workbook's Pillar 3 sheets "
               "that could NOT be upgraded to the FY2021 primary, and the reason is structural rather than an "
               "access problem. The FY2021 Annual Financial Report (Companies House copy, full-text searched) "
               "contains no NSFR figure and no mention of stable funding at all - its liquidity section covers the "
               "LCR only. The FY2022 report explains why: 'Following the UK implementation of CRR II / CRD V, the "
               "NSFR became a binding requirement under UK law from 1 January 2022', and it is that report which "
               "first supplies a FY2021 comparative ('NSFR was 145% (2021: 156%)'). FY2021's 156% is therefore a "
               "retrospectively-disclosed comparative by construction, correctly cited to the FY2022 report, and "
               "re-opening the FY2021 report for it would be wasted effort."),
)

# Equivalent to bw.add_not_disclosed_metric_sheets(["MREL Ratio"], ...) - spelled out as a
# direct add_metric_sheet call purely so the note cell can be given a taller note_height,
# which add_not_disclosed_metric_sheets does not forward. Row content is identical.
bw.add_metric_sheet(
    "MREL Ratio",
    None,
    [("MREL Ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    first_col_width=52,
    source_height=860,
    note_height=320,
    note=(
        "No MREL RATIO is disclosed for any year: AIB UK's own capital section discusses only the CRR "
                      "minimum capital requirement (8% Total Capital / 4.5% Tier 1) plus its PRA-set Pillar 1 and "
                      "Pillar 2a add-on, and never states an MREL requirement as a percentage of RWA or of leverage "
                      "exposure, nor an MREL resource amount. This row therefore stays 'Not publicly disclosed' - "
                      "nothing here may be derived from the capital figures on the other sheets.\n"
                      "CORRECTION (2026-09-16): an earlier pass of this script recorded that 'MREL is not mentioned "
                      "anywhere in any of AIB Group (UK) p.l.c.'s five Annual Financial Reports (FY2021-FY2025)'. "
                      "That was written without the FY2021 report, which had not then been fetched, and it is WRONG "
                      "for FY2021. The FY2021 Annual Financial Report (Companies House copy - see ACCESS ROUTE "
                      "NOTE) mentions MREL twice: in the glossary ('MREL - Minimum Requirement for Eligible "
                      "Liabilities', p.165) and, substantively, in note 34 'Secondary non-preferential debt' "
                      "(printed p.144), which states: 'On 31 December 2020, AIB plc issued a GBP45m secondary "
                      "non-preferential loan to AIB UK FOR THE PURPOSES OF MEETING AIB UK MREL REQUIREMENTS. The "
                      "loan bore interest on the outstanding nominal amount at a rate of SONIA plus a margin of "
                      "130bps, payable half-yearly in arrears.' and 'AIB UK exercised the option to repay the "
                      "secondary non-preferential debt on 31 December 2021.' The note shows the instrument at "
                      "GBP45m at 31 December 2020 and NIL at 31 December 2021.\n"
                      "WHAT THAT DOES AND DOES NOT ESTABLISH: it establishes that AIB UK had an MREL requirement of "
                      "its own during FY2020-FY2021, met with internal (downstreamed) MREL from the Irish parent, "
                      "and that the instrument was repaid at the very end of FY2021 - which is consistent with, and "
                      "dates, the disappearance of the requirement from AIB UK's disclosures thereafter. It does "
                      "NOT give a ratio, a requirement level, or an eligible-liabilities total for any year, so no "
                      "cell on this sheet can be filled. The 'no hits' finding remains true for the FY2022 report "
                      "(re-verified 2026-09-16 by full-text search of the FY2022 PDF: zero occurrences of 'MREL' or "
                      "'eligible liabilities') and, per the earlier pass, for FY2023-FY2025. Note the ordering: "
                      "AIB UK stopped disclosing a leverage ratio from 1 January 2022 and repaid its MREL "
                      "instrument on 31 December 2021 - two independent disclosures thinning out at the same "
                      "moment, both consistent with the PS21/21 scope change described on the Leverage Ratio sheet."
    ),
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 10304, "FY2024": 9820, "FY2023": 9969, "FY2022": 10875, "FY2021": 12688}),
        ("Loans and advances to customers", {"FY2025": 5291, "FY2024": 4708, "FY2023": 5647, "FY2022": 5718, "FY2021": 6198}),
        ("Customer deposits", {"FY2025": 7588, "FY2024": 7317, "FY2023": 7118, "FY2022": 8204, "FY2021": 10088}),
        ("Total equity", {"FY2025": 2061, "FY2024": 1893, "FY2023": 1853, "FY2022": 1654, "FY2021": 1792}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 384, "FY2024": 392, "FY2023": 443, "FY2022": 301, "FY2021": 241}),
        ("Total operating expense", {"FY2025": -134, "FY2024": -131, "FY2023": -127, "FY2022": -122, "FY2021": -160}),
        ("Profit for the year", {"FY2025": 237, "FY2024": 188, "FY2023": 269, "FY2022": 115, "FY2021": 170}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1893, "FY2024": 1852, "FY2023": 1654, "FY2022": 1792, "FY2021": 1674}),
        ("Total comprehensive income for the year", {"FY2025": 267, "FY2024": 159, "FY2023": 340, "FY2022": -138, "FY2021": 118}),
        ("Other equity movements, net", {"FY2025": -99, "FY2024": -118, "FY2023": -141, "FY2022": 0, "FY2021": 0}),
        ("Closing equity", {"FY2025": 2061, "FY2024": 1893, "FY2023": 1853, "FY2022": 1654, "FY2021": 1792}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2023": -794, "FY2022": -1282, "FY2021": 750}),
        ("Net cash from/(used in) investing activities", {"FY2023": -3, "FY2022": -5, "FY2021": -11}),
        ("Net cash from/(used in) financing activities", {"FY2023": -3, "FY2022": -9, "FY2021": -48}),
        ("Closing cash and cash equivalents", {"FY2023": 3257, "FY2022": 4057, "FY2021": 5353}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "26.8%", "FY2024": "27.7%", "FY2023": "21.44%", "FY2022": "24.11%", "FY2021": "22.81%"}),
        ("Tier 1 Ratio", {"FY2025": "28.64%", "FY2024": "29.66%", "FY2023": "23.11%", "FY2022": "24.11%", "FY2021": "22.81%"}),
        ("Total Capital Ratio", {"FY2025": "31.0%", "FY2024": "32.3%", "FY2023": "25.24%", "FY2022": "24.11%", "FY2021": "22.81%"}),
        ("Leverage Ratio", {"FY2021": "11.26%"}),
        ("LCR", {"FY2025": "216%", "FY2024": "282%", "FY2023": "216%", "FY2022": "176%", "FY2021": "169%"}),
        ("NSFR", {"FY2025": "157%", "FY2024": "172%", "FY2023": "139%", "FY2022": "145%", "FY2021": "156%"}),
    ],
    note="FY2021 SOURCING (2026-09-16): FY2021 no longer depends on the FY2022 edition's comparative column. The "
         "FY2021 Annual Financial Report was retrieved from COMPANIES HOUSE (company NI018800 - it is not on "
         "aib.ie, and the bank's own aibgb.co.uk returns HTTP 403; see the ACCESS ROUTE NOTE carried on every "
         "detail sheet) and read directly. Every FY2021 figure ON THIS OVERVIEW reproduces from the primary "
         "unchanged EXCEPT 'Total operating income' (£241m here, the FY2022-edition basis; the FY2021 edition "
         "reported £244m before a £3m loss on disposal of property was reclassified into operating income by the "
         "next edition - profit for the year is £170m on both bases). That divergence is documented on separate "
         "labelled memorandum rows on the Profit & Loss sheet; this Overview is a COPY of the detail sheets and "
         "deliberately carries only the FY2022-edition basis so the FY2021 column stays comparable with "
         "FY2022-FY2025 beside it. Read the Profit & Loss sheet before quoting FY2021 income figures against the "
         "FY2021 Annual Financial Report itself.\n"
         "Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Cash flow is blank for FY2024-FY2025 (FRS 101 exemption took "
         "effect from FY2024 - see Cash Flow Statement sheet note); Leverage Ratio is populated for FY2021 only "
         "(never disclosed again in later years). Balance Sheet/P&L/Equity blocks are Group basis FY2021-FY2023 and "
         "solo (Company) basis FY2024-FY2025 - see the Statement of Changes in Equity sheet's note on the resulting "
         "£1m entity-basis break in the equity bridge between those years. All figures are AIB Group (UK) p.l.c. "
         "itself, NOT AIB Group plc (the Irish parent) - see entity note on every sheet.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/AIB GROUP UK FINANCIALS.xlsx")
