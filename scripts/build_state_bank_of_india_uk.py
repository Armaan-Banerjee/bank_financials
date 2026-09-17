import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]
YEAR_LABEL = {y: y for y in YEARS}

P3 = {
    "FY2025": "https://sbiuk.statebank/documents/274771/0/PILLAR+3+DISCLOSURE+FINAL310325_241225_Clean.pdf/276091ea-d916-6dca-edea-e443f2360cc9?t=1767022122544",
    "FY2024": "https://sbiuk.statebank/documents/274771/0/Pillar+3+Disclosures+March+24.pdf/91bf9318-a453-5bc7-f2ae-434bdbe0371c?t=1730125188784",
    "FY2023": "https://sbiuk.statebank/documents/274771/0/Disclosure+Statement+Basel+3+FY+22+23.pdf/f068336d-c894-0e35-49b6-a3bb372791ae?t=1699459644582",
    "FY2022": "https://sbiuk.statebank/documents/274771/0/SBI+UK+Limited+Pillar+3+Disclosures_2022_Final.pdf/f3ecb40e-bb6a-2a6b-52b6-44c00b93dc8b?t=1671208953569",
    "FY2021": "https://sbiuk.statebank/documents/274771/0/SBI+UK+Limited+Pillar+3_2021_FINAL.pdf/cea4191a-a7ee-17ef-df42-ee5d2d21f73f?t=1635936666779",
    "FY2020": "https://sbiuk.statebank/documents/274771/1346149/SBI+UK+Limited+Pillar+3+Disclosures+March+2020.pdf",
    "FY2019": "https://sbiuk.statebank/documents/274771/1346149/SBI+UK+Limited+Pillar+3+Disclosures_31+Mar+2019.pdf",
}
PAGES = {"FY2025": "6-7", "FY2024": "7-8", "FY2023": "7-8", "FY2022": "7-8", "FY2021": "4", "FY2020": "20-21", "FY2019": "20-21"}
# Asset Quality (credit risk exposure by degree of risk of financial loss) and RWA Breakdown (UK
# OV1 / Pillar 1 RWA table) sit on different pages than the KM1 metrics table in the older, longer
# FY2019/FY2020 Pillar 3 documents (the FY2021-2025 documents are short enough that all three
# tables share the same page range, hence PAGES is reused for those years).
AQ_PAGES = dict(PAGES)
AQ_PAGES.update({"FY2020": "25-26", "FY2019": "25"})
RWA_PAGES = dict(PAGES)
RWA_PAGES.update({"FY2020": "17-18", "FY2019": "18-19"})
FS2026 = "https://find-and-update.company-information.service.gov.uk/company/10436460/filing-history/MzU0MjU0NTEyMWFkaXF6a2N4/document?format=pdf&download=0"
FS2025 = "https://sbiuk.statebank/documents/274771/0/SBIUK%2B-%2BAnnual%2BReport%2B2025%2Bapproved.pdf/4d165f25-8596-0935-9c39-80cf4c7202b8?t=1767022144810"
FS2024 = "http://sbiuk.statebank/documents/274771/0/SBIUK+Ltd+-+Annual+Report+++2024.pdf/80699e7d-ba2e-8cc6-6726-f8bc7058261f?t=1730125796286"
FS2023 = "https://sbiuk.statebank/documents/274771/0/Annual+Financial+22+23.pdf/77b485b2-332e-c7b0-63bf-30991ce5238b?t=1699459677034"
FS2022 = "https://sbiuk.statebank/documents/274771/0/SBIUK+Annual+Financial+Statement+2022.pdf/e333fa11-f77e-d3ab-b179-010d91c38b92?t=1671208995591"
FS2021 = "https://sbiuk.statebank/documents/274771/0/SBI+UK+Annual+Report+-+Final.pdf/d188a204-db49-de8e-9662-5fece3c6f364?t=1635936642226"
FS2020 = "https://sbiuk.statebank/documents/274771/1346149/SBIUK+Annual+Report+March+2020.pdf"
FS2019 = "https://sbiuk.statebank/documents/274771/1346149/Annual+Statement+2019.PDF"

ENTITY_NOTE = (
    "ENTITY NOTE: State Bank of India (UK) Limited (Companies House 10436460, FRN 757156, LEI "
    "213800LOV39TJH6YQY23) is the UK legal entity named in the Banks List 2608.xlsx and the PRA register. "
    "It is a wholly owned subsidiary of State Bank of India and has no subsidiaries. The Pillar 3 figures below "
    "are SBI UK standalone/entity figures; parent State Bank of India figures have not been substituted."
)
EXEMPTION_NOTE = (
    "FRS 102 CASH-FLOW EXEMPTION: SBI UK’s annual accounts explicitly state that it takes the FRS 102 disclosure "
    "exemption from preparation of a cash flow statement because it is a qualifying entity and its ultimate parent, "
    "State Bank of India, includes the bank’s cash flows in consolidated financial statements. This wording is in "
    f"the FY2025 accounts, accounting policies (p.29) - {FS2025}, and the corresponding FY2024, FY2023, FY2022, "
    f"FY2021, FY2020 (p.31) and FY2019 (p.29) accounts. No entity cash-flow statement is therefore presented. "
    f"This is a PILLAR-3-ONLY workbook."
)
HISTORICAL_FLOOR_NOTE = (
    "HISTORICAL FLOOR (HD-024): SBI UK (Companies House 10436460) was incorporated 19 October 2016 as "
    "'SBIUK Operations Limited', renamed 'State Bank of India (UK) Limited' 7 September 2017. Its FIRST "
    "accounting period ran 19 October 2016 - 31 March 2018 (18 months, first accounts filed at Companies "
    "House 24 July 2018) and is EXCLUDED from this workbook: the entity was pre-operational for almost "
    "all of it (Statement of Financial Position as at 31 March 2018 shows only £225,339k of deposits with "
    "banks and £175,329k of shareholders' funds - no loans and advances to customers, no customer deposits, "
    "no derivatives, per Annual Statement 2019's FY2018 comparative column, p.27), it is not a standard "
    "12-month year, and no Pillar 3 disclosure was published for it (SBI UK's own Pillar 3 archive begins "
    "with the FY2019 document). FY2019 (year ended 31 March 2019, its first full trading year and first "
    "Pillar 3 disclosure) is therefore the real, source-confirmed floor - not FY2016 as HD-024's stated "
    "'confirmed floor FY2016 (source: HD-001)' assumed; SBI UK is not one of HD-001's 4 actual deep-dive "
    "banks and that figure was an unverified GLEIF entity-creation-year guess. FY2019 and FY2020 are added "
    "in this rebuild; FY2018 is self-skipped as documented above."
)


P3_PENDING_NOTE = (
    "FY2026 PILLAR 3 NOT YET PUBLISHED: SBI UK's FY2026 (year ended 31 March 2026) statutory "
    "accounts were filed at Companies House on 9 September 2026 and are the source for this "
    "workbook's FY2026 Balance Sheet, Profit & Loss and Statement of Changes in Equity. Its FY2026 "
    "Pillar 3 disclosure had not been published as of 15 September 2026 - the Bank publishes each "
    "year's Pillar 3 document several months after the accounts (FY2025's went up 29 December 2025, "
    "FY2024's 28 October 2024), and no FY2026 document appears on sbiuk.statebank or in the Internet "
    "Archive. FY2026 is therefore blank on the Asset Quality and RWA Breakdown sheets and on the "
    "Total RWAs metric, and the FY2026 capital/leverage/NSFR figures that ARE shown come from the "
    "Annual Report's own disclosures rather than from a KM1 table - see each sheet's own note."
)


def sources():
    return (
        "Sources - State Bank of India (UK) Limited standalone UK KM1 / Key Metrics disclosures, £m and %:\n"
        + "\n".join(f"{y}: SBI UK Pillar 3 disclosure, pp. {PAGES[y]} - {P3[y]}" for y in YEARS if y in P3)
        + "\nFY2026: no Pillar 3 disclosure published yet - see note below."
        + "\n\n"
        + P3_PENDING_NOTE + "\n\n"
        + ENTITY_NOTE
    )


INVESTMENT_SECURITIES_NOTE = (
    "INVESTMENT SECURITIES BREAKDOWN: the 'Investment securities - ...' sub-rows below the renamed 'Total "
    "Investment securities' line are transcribed from Note 3.9 'Investment securities' of each year's own "
    "Notes to the Financial Statements (Note 3.11 in the FY2019 Annual Statement, which uses different note "
    "numbering), which splits the balance both by measurement basis (Available for Sale, i.e. mark-to-"
    "market / Held to Maturity, i.e. amortised cost) and by issuer type (Government Issued vs Other public "
    "sector securities & corporates):\n"
    f"FY2026: Note 3.9, p.56 - {FS2026} (FY2026 has no Held-to-Maturity Government Issued balance, so "
    f"that row is blank; the Held to Maturity 'Other public sector securities & corporates' figure of "
    f"93,278 is shown net of the (89) fair-value adjustment of hedged bonds, the same convention used "
    f"for every earlier year. The sub-rows sum exactly to the 364,408 headline: 28,296 + 245,875 - "
    f"3,041 + 93,278.)\n"
    f"FY2025/FY2024: Note 3.9, p.52 - {FS2025}\n"
    f"FY2023/FY2022: Note 3.9, p.51 - {FS2023}\n"
    f"FY2021: Note 3.9, p.47 - {FS2021}\n"
    f"FY2020: Note 3.9, p.47 - {FS2020} (used in preference to the FY2021 report's own FY2020 comparative "
    "column, which nets a 'Depreciation in Mark to market' line into the Available for Sale carrying "
    f"amounts differently but sums to the same totals - each year's own originally-published figures are "
    "used, per project convention)\n"
    f"FY2019: Note 3.11, p.43 - {FS2019} (cross-checked against the FY2020 report's own FY2019 comparative "
    "column, Note 3.9, p.47, which shows the identical figures)\n\n"
    "Each year's sub-rows sum exactly to that year's headline 'Total Investment securities' line. The "
    "Available for Sale 'Loss due to market rate movement' line (a mark-to-market adjustment) is disclosed "
    "as a single blended figure covering both issuer types, not split between Government Issued and Other "
    "public sector securities & corporates, so it is shown as its own row rather than force-allocated - a "
    "presentation choice of the source note, not a gap. Held to Maturity issuer-type rows are net of the "
    "'fair value adjustment of hedged bonds' shown in the source table, so they already equal the source's "
    "own 'Total' column per issuer type. FY2020 alone also carries a 'Collective provision' deduction line "
    "(-£490k, a portfolio-level impairment allowance) not present in any other year; FY2019 and FY2020 do "
    "not disclose a separate 'Loss due to market rate movement' line (their own report presents Available "
    "for Sale carrying amounts net of any revaluation, with no separate adjustment line that year) - blank "
    "cells reflect the note's own year-by-year composition, not a gap. No Government Issued Held to "
    "Maturity holdings are disclosed for FY2025/FY2024/FY2023 (explicit nil/dash in the source note, shown "
    "as 0)."
)

STATEMENTS_SOURCES = (
    "Sources - State Bank of India (UK) Limited Annual Report and Financial Statements, £'000:\n"
    f"FY2026: Annual Report and Financial Statements for the year ended 31 March 2026 (Companies House filing, full accounts made up to 31 March 2026, filed 9 September 2026; scanned/image-only PDF with no text layer - read by OCR at 250 dpi), Income statement p.34 / Statement of comprehensive income p.35 / Statement of financial position p.36 / Statement of changes in equity p.37 - {FS2026}. Added 2026-09-15. Every FY2026 statement was verified to foot internally (Total assets GBP 2,079,942k = Total liabilities GBP 1,800,967k + Total equity GBP 278,975k; Net interest income, Operating income, Total operating expenses, Profit before tax and Profit after tax each recompute exactly from their own component lines) and every FY2025 comparative printed in the FY2026 accounts reproduces this workbook's existing FY2025 figures exactly, so no prior year was restated. The FY2026 balance sheet prints Tangible and Intangible fixed assets as two lines (3,682 + 235); they are combined here into the single 'Fixed assets (tangible & intangible)' row of 3,917, matching how every earlier year in this sheet is already presented. The 'Borrowings from banks' line does not appear at all in the FY2026 balance sheet and is left blank rather than set to zero.\n"
    f"FY2025/FY2024: Annual Report 2025, Income statement/Statement of comprehensive income/Statement of "
    f"financial position/Statement of changes in equity, pp. 33-36 - {FS2025}\n"
    f"FY2023/FY2022: Annual Report 2023, same statements, pp. 31-34 - {FS2023}\n"
    f"FY2021: Annual Report 2021 (also carries the FY2020 comparative and the FY2021 opening-equity bridge "
    f"used to build the FY2022 opening row below), same statements, pp. 25-28 - {FS2021}\n"
    f"FY2020: Annual Report (year ended 31 March 2020) (also carries the FY2019 comparative), same "
    f"statements, pp. 25-27 - {FS2020}\n"
    f"FY2019: Annual Statement 2019 (SBI UK's first full 12-month trading year; also carries the FY2018 "
    f"18-month first-period comparative used only for HISTORICAL_FLOOR_NOTE evidence, not as a workbook "
    f"column - see source note at bottom), same statements, pp. 25-28 - {FS2019}\n"
    "All 7 years independently cross-checked against the adjacent report's own comparative column (FY2024 "
    "vs FY2025's comparative; FY2022 vs FY2023's comparative; FY2019 vs FY2020's comparative) - exact "
    "match in every case bar one £1k rounding artifact noted below.\n\n"
    + ENTITY_NOTE
    + "\n\n" + HISTORICAL_FLOOR_NOTE
    + "\n\nPRESENTATION NOTES: (1) FY2025's Other assets (4,877) and Balance Sheet total tie exactly, but "
    "FY2024's own originally-published Other assets figure (5,269, from the FY2024 report) is £1k higher "
    "than the comparative FY2025's report shows for FY2024 (5,268) - FY2024's own originally-published "
    "figure is used here, per project convention, producing a £1k rounding gap against FY2024's reported "
    "Total assets of 1,842,936 that is not reproduced in the line items (1,842,937) - a source rounding "
    "artifact, not an error in this workbook. (2) FY2025 splits Fixed assets into Tangible (3,638) and "
    "Intangible (232) for the first time; all other years disclose only a single combined Fixed assets "
    "line - a single combined 'Fixed assets (tangible & intangible)' row is used throughout for "
    "comparability (FY2025: 3,870 = 3,638 + 232). (3) FY2021's Balance Sheet splits retained earnings "
    "into 'Retained earnings' (11,468) and 'Profit and loss account for the year' (7,423); these are "
    "combined into a single Retained earnings row (18,891) matching later years' presentation - this "
    "combined figure is confirmed by the FY2023 report's own equity statement, which shows the FY2021 "
    "closing Profit and loss balance as 18,891. (4) Income statement line-item wording shifts over time: "
    "FY2022-FY2025 report 'Net gains from derivative financial instruments' (FY2025/FY2024 relabelled "
    "'Net gains from Forex and derivative financial instruments') plus a separate 'Gain/(Loss) on sale of "
    "investments' line; FY2021, FY2020 and FY2019's reports instead split this into 'Net income/(expense) "
    "on foreign exchange' and 'Net gain/(loss) on realised financial instruments', with no separate "
    "sale-of-investments line - these three years' rows are shown separately and left blank for other "
    "years, documented rather than forced into the later years' line labels. (5) FY2020's Income statement "
    "carries a one-off 'Loss on Sale of Loans' line (£4,528k) with no FY2019 equivalent (reported as nil); "
    "shown in the existing 'Profit/(loss) on sale of loans' row with FY2019 recorded as 0, matching the "
    "source's own dash."
)

BALANCE_SHEET_SOURCES = STATEMENTS_SOURCES + "\n\n" + INVESTMENT_SECURITIES_NOTE

EQUITY_SOURCES = (
    "Sources - State Bank of India (UK) Limited Statement of Changes in Equity, £'000, chronological "
    "(oldest to newest):\n"
    f"FY2019 movements (opening 1 April 2018 through 31 March 2019): Annual Statement 2019, p.28 - {FS2019}\n"
    f"FY2020 movements: Annual Report (year ended 31 March 2020), p.27 - {FS2020}\n"
    f"FY2021 movements: Annual Report 2021, p.28 - {FS2021}\n"
    f"FY2022/FY2023 movements: Annual Report 2023, p.34 - {FS2023}\n"
    f"FY2024/FY2025 movements: Annual Report 2025, p.36 - {FS2025}\n"
    f"FY2026 movements: Annual Report 2026, p.37 - {FS2026} (the FY2026 statement's own 31 March 2025 "
    f"opening row, 225,000 / 53,177 / (717) / 52,460 / 277,460, ties exactly to the FY2025 closing row "
    f"already in this sheet)\n"
    "Every closing balance ties exactly to the next year's own opening balance and to that year's own "
    "Balance Sheet Total equity - confirmed via a sixth independent source (the FY2023 report's own SOCE "
    "restates the FY2021 closing balance as its own 1 April 2021 opening row: 225,000 / 18,891 / (74) / "
    "18,817 / 243,817, an exact match to the figure derived from the FY2021 report's own 4-column SOCE; "
    "and the FY2020 report's own SOCE restates the FY2019 closing balance as its own 1 April 2019 opening "
    "row: 175,000 / 8,113 / 24 / 183,137, an exact match to the figure derived from the FY2019 report's own "
    "SOCE). Zero undocumented plug rows across all 7 years.\n\n"
    + ENTITY_NOTE
    + "\n\n" + HISTORICAL_FLOOR_NOTE
    + "\n\nPRESENTATION NOTE: FY2023/FY2024/FY2025 reports use a 5-column SOCE (Share capital / Profit "
    "and loss / Other comprehensive income / Total comprehensive income / Total equity); FY2021, FY2020 "
    "and FY2019's own reports use a simpler 4-column SOCE (Share capital / Retained earnings / Investment "
    "revaluation reserve / Total equity) with no separate 'Total comprehensive income' column and a single "
    "combined AFS-revaluation movement line (not split into a gross revaluation line and a deferred-tax "
    "line, as the later years' reports do). The FY2019-FY2021 movement rows below are shown exactly as "
    "each year's own report presents them, with a derived Total comprehensive income figure (Profit + OCI "
    "movement) added for structural consistency with later years - not a re-presentation of any figure. "
    "The chain below starts at 'As at 1 April 2018' (the opening balance of FY2019, the confirmed floor "
    "year); it deliberately does not extend back through the excluded 18-month FY2018 first period (see "
    "HISTORICAL_FLOOR_NOTE)."
)

ASSET_QUALITY_SOURCES = (
    "Sources - State Bank of India (UK) Limited Pillar 3 credit risk exposures (loans and advances to "
    "customers, maximum exposure by degree of risk of financial loss), £m:\n"
    + "\n".join(f"{y}: SBI UK Pillar 3 disclosure, pp. {AQ_PAGES[y]} - {P3[y]}" for y in YEARS if y in P3)
    + "\nFY2026: no Pillar 3 disclosure published yet - see note below."
    + "\n\nEach year's Total maximum exposure figure reconciles to the source table's own total (FY2022's "
    "reconciles to within £0.01m of its own reported total; FY2019's within £0.06m - a source rounding "
    "artifact, not an error in this workbook). This Total does not tie to the Balance Sheet's narrower "
    "'Loans and advances to customers' line (a net, on-balance-sheet figure), since it also includes "
    "off-balance-sheet unutilised overdraft commitments and pipeline loans - a genuine, documented scope "
    "difference, not forced to tie. Forbearance facility counts/exposures are drawn from each year's own "
    "Pillar 3 forbearance-policy paragraph; FY2019 and FY2020 both explicitly state no loans and advances "
    "had been considered for forbearance (NIL), so both rows are 0 rather than blank. FY2019's collateral "
    "value and Gross loans and advances figures are taken from the FY2020 Pillar 3 document's own FY2019 "
    f"comparative column (p.26 - {P3['FY2020']}), which carries them to the nearest £'000, in preference to "
    "the FY2019 document's own £m-rounded figures, for precision.\n\n"
    + P3_PENDING_NOTE + "\n\n"
    + ENTITY_NOTE
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - State Bank of India (UK) Limited UK OV1 (Overview of risk-weighted exposure amounts), £m:\n"
    + "\n".join(f"{y}: SBI UK Pillar 3 disclosure, pp. {RWA_PAGES[y]} - {P3[y]}" for y in YEARS if y in P3)
    + "\nFY2026: no Pillar 3 disclosure published yet - see note below."
    + "\n\nEach year's category rows sum to that year's own reported Total, except FY2025: 1,216.73 + "
    "7.60 + 95.33 = 1,319.66m against a reported Total of 1,320.25m, a genuine ~£0.59m gap present in the "
    "source document's own UK OV1 table (confirmed by direct visual inspection of the source PDF page, "
    "not a transcription error in this workbook) - the reported Total is used as the TOTAL row, and the "
    "gap is not silently plugged into any category; and FY2020/FY2019, where the category rows sum to "
    "£1,375.1m/£1,339.3m against reported Totals of £1,375.0m/£1,339.4m, a ~£0.1m gap present in the "
    "source document's own Pillar 1 RWA table in both years (same treatment: reported Total used, gap "
    "not plugged).\n\n"
    "FY2019/FY2020 PRESENTATION NOTE: these two years' Pillar 3 documents use an older Pillar 1 RWA "
    "categorisation (Credit Risk [on-balance sheet + off-balance sheet + counterparty-credit-risk-for-"
    "forex-swap + credit valuation adjustment, combined] / Market Risk / Operational Risk) rather than "
    "the UK OV1 format used from FY2021 onward (Credit risk excluding CCR / Counterparty credit risk (CCR) "
    "/ Operational risk), so Counterparty credit risk is not broken out as its own row for FY2019/FY2020 - "
    "it is embedded, and separately disclosed as a sub-line, within their combined Credit Risk figure "
    "(shown in a dedicated row below rather than forced into the 'Credit risk (excluding CCR)' row, which "
    "is left blank for these two years). FY2020's Market Risk is reported as nil (the Bank's open position "
    "was below the 2% of own-funds threshold requiring a capital charge under CRR Article 351)."
    + "\n\n"
    + P3_PENDING_NOTE
)


bw = BankWorkbook("State Bank of India (UK) Limited", YEARS, YEAR_LABEL, header_color="1B4D6B")

bw.add_balance_sheet_sheet(
    title="State Bank of India (UK) Limited — Balance Sheet",
    subtitle="Entity basis, £'000. See source note at bottom.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances with banks", {"FY2026": 26835, "FY2025": 70262, "FY2024": 90746, "FY2023": 144199, "FY2022": 86381, "FY2021": 113623, "FY2020": 72555, "FY2019": 19472}),
        ("DATA", "Loans and advances to banks", {"FY2026": 19440, "FY2025": 7752, "FY2024": 20607, "FY2023": 79912, "FY2022": 100000, "FY2021": 125000, "FY2020": 195000, "FY2019": 165712}),
        ("DATA", "Loans and advances to customers", {"FY2026": 1655683, "FY2025": 1529812, "FY2024": 1415920, "FY2023": 1403369, "FY2022": 1201300, "FY2021": 1140238, "FY2020": 1101038, "FY2019": 1044412}),
        ("DATA", "Total Investment securities", {"FY2026": 364408, "FY2025": 329255, "FY2024": 292784, "FY2023": 323130, "FY2022": 367831, "FY2021": 339418, "FY2020": 375150, "FY2019": 345303}),
        ("DATA", "Investment securities - Government issued (Available for Sale, mark-to-market)", {"FY2026": 28296, "FY2025": 16231, "FY2024": 32262, "FY2023": 61488, "FY2022": 19622, "FY2021": 3662, "FY2020": 59963, "FY2019": 21948}),
        ("DATA", "Investment securities - Other public sector securities & corporates (Available for Sale, mark-to-market)", {"FY2026": 245875, "FY2025": 203640, "FY2024": 125466, "FY2023": 123224, "FY2022": 86832, "FY2021": 50021, "FY2020": 18425, "FY2019": 0}),
        ("DATA", "Investment securities - Loss due to market rate movement (Available for Sale, mark-to-market adjustment)", {"FY2026": -3041, "FY2025": -958, "FY2024": -3188, "FY2023": -6801, "FY2022": -3862, "FY2021": -92}),
        ("DATA", "Investment securities - Government issued (Held to Maturity, amortised cost)", {"FY2026": 0, "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 20414, "FY2021": 19334, "FY2020": 21459, "FY2019": 7116}),
        ("DATA", "Investment securities - Other public sector securities & corporates (Held to Maturity, amortised cost)", {"FY2026": 93278, "FY2025": 110342, "FY2024": 138244, "FY2023": 145219, "FY2022": 244825, "FY2021": 266493, "FY2020": 275793, "FY2019": 316239}),
        ("DATA", "Investment securities - Collective provision (FY2020 only, see note)", {"FY2020": -490}),
        ("DATA", "Derivative financial instruments", {"FY2026": 2855, "FY2025": 14341, "FY2024": 13186, "FY2023": 12060, "FY2022": 8430, "FY2021": 25114, "FY2020": 0, "FY2019": 7194}),
        ("DATA", "Fixed assets (tangible & intangible)", {"FY2026": 3917, "FY2025": 3870, "FY2024": 4425, "FY2023": 3130, "FY2022": 3463, "FY2021": 2807, "FY2020": 3281, "FY2019": 3846}),
        ("DATA", "Other assets", {"FY2026": 6804, "FY2025": 4877, "FY2024": 5269, "FY2023": 11162, "FY2022": 8600, "FY2021": 9210, "FY2020": 10275, "FY2019": 9340}),
        ("TOTAL", "Total assets", {"FY2026": 2079942, "FY2025": 1960169, "FY2024": 1842936, "FY2023": 1976962, "FY2022": 1776005, "FY2021": 1755410, "FY2020": 1757299, "FY2019": 1595279}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Borrowings from banks", {"FY2025": 0, "FY2024": 16199, "FY2023": 121408, "FY2022": 164120, "FY2021": 128696, "FY2020": 65072, "FY2019": 37137}),
        ("DATA", "Deposit from customers", {"FY2026": 1784374, "FY2025": 1655992, "FY2024": 1530535, "FY2023": 1568185, "FY2022": 1339203, "FY2021": 1360344, "FY2020": 1418658, "FY2019": 1310363}),
        ("DATA", "Derivative financial instruments", {"FY2026": 2453, "FY2025": 654, "FY2024": 538, "FY2023": 0, "FY2022": 6061, "FY2021": 0, "FY2020": 22930, "FY2019": 892}),
        ("DATA", "Other liabilities", {"FY2026": 14140, "FY2025": 26063, "FY2024": 23402, "FY2023": 27217, "FY2022": 17015, "FY2021": 22553, "FY2020": 14950, "FY2019": 13750}),
        ("DATA", "Subordinated debt liabilities (FY2019-FY2020 only; converted to share capital during FY2021, see note)", {"FY2020": 50000, "FY2019": 50000}),
        ("TOTAL", "Total liabilities", {"FY2026": 1800967, "FY2025": 1682709, "FY2024": 1570674, "FY2023": 1716810, "FY2022": 1526399, "FY2021": 1511593, "FY2020": 1571610, "FY2019": 1412142}),
        ("SECTION", "Shareholders' funds", {}),
        ("DATA", "Share capital", {"FY2026": 225000, "FY2025": 225000, "FY2024": 225000, "FY2023": 225000, "FY2022": 225000, "FY2021": 225000, "FY2020": 175000, "FY2019": 175000}),
        ("DATA", "Investment revaluation reserve", {"FY2026": -2280, "FY2025": -717, "FY2024": -2390, "FY2023": -5100, "FY2022": -2896, "FY2021": -74, "FY2020": -779, "FY2019": 24}),
        ("DATA", "Retained earnings", {"FY2026": 56255, "FY2025": 53177, "FY2024": 49652, "FY2023": 40252, "FY2022": 27502, "FY2021": 18891, "FY2020": 11468, "FY2019": 8113}),
        ("TOTAL", "Total equity", {"FY2026": 278975, "FY2025": 277460, "FY2024": 272262, "FY2023": 260152, "FY2022": 249606, "FY2021": 243817, "FY2020": 185689, "FY2019": 183137}),
        ("TOTAL", "Total liabilities and equity", {"FY2026": 2079942, "FY2025": 1960169, "FY2024": 1842936, "FY2023": 1976962, "FY2022": 1776005, "FY2021": 1755410, "FY2020": 1757299, "FY2019": 1595279}),
    ],
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=64,
    source_height=480,
)

bw.add_income_statement_sheet(
    title="State Bank of India (UK) Limited — Profit & Loss",
    subtitle="Entity basis, £'000. See source note at bottom.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest receivable and similar income", {"FY2026": 105641, "FY2025": 101825, "FY2024": 98608, "FY2023": 71035, "FY2022": 43575, "FY2021": 40339, "FY2020": 46232, "FY2019": 51556}),
        ("DATA", "Interest payable and similar charges", {"FY2026": -59967, "FY2025": -56644, "FY2024": -47190, "FY2023": -23899, "FY2022": -8914, "FY2021": -16735, "FY2020": -20114, "FY2019": -26214}),
        ("TOTAL", "Net interest income", {"FY2026": 45674, "FY2025": 45181, "FY2024": 51418, "FY2023": 47136, "FY2022": 34661, "FY2021": 23604, "FY2020": 26118, "FY2019": 25342}),
        ("DATA", "Fees and commissions income", {"FY2026": 1815, "FY2025": 1772, "FY2024": 1486, "FY2023": 1543, "FY2022": 912, "FY2021": 1303, "FY2020": 2258, "FY2019": 1992}),
        ("DATA", "Net gains from Forex and derivative financial instruments", {"FY2026": 1258, "FY2025": 1615, "FY2024": 1607, "FY2023": 1652, "FY2022": 1484}),
        ("DATA", "Net income/(expense) on foreign exchange (FY2019-FY2021 only, see note)", {"FY2021": 991, "FY2020": -218, "FY2019": 60}),
        ("DATA", "Net gain/(loss) on realised financial instruments (FY2019-FY2021 only, see note)", {"FY2021": 537, "FY2020": 687, "FY2019": -192}),
        ("DATA", "Gain/(Loss) on sale of investments", {"FY2026": 715, "FY2025": 10, "FY2024": 51, "FY2023": -1314, "FY2022": 536}),
        ("DATA", "Other operating income", {"FY2026": 4, "FY2025": 7, "FY2024": 37, "FY2023": 28, "FY2022": 30, "FY2021": 195, "FY2020": 20, "FY2019": 7}),
        ("TOTAL", "Operating income", {"FY2026": 49466, "FY2025": 48585, "FY2024": 54599, "FY2023": 49045, "FY2022": 37623, "FY2021": 26630, "FY2020": 28865, "FY2019": 27209}),
        ("SECTION", "Expenses", {}),
        ("DATA", "Administrative expenses", {"FY2026": -27420, "FY2025": -23568, "FY2024": -21916, "FY2023": -21791, "FY2022": -17610, "FY2021": -15515, "FY2020": -15704, "FY2019": -14752}),
        ("DATA", "Depreciation", {"FY2026": -796, "FY2025": -856, "FY2024": -743, "FY2023": -731, "FY2022": -711, "FY2021": -695, "FY2020": -818, "FY2019": -832}),
        ("TOTAL", "Total operating expenses", {"FY2026": -28216, "FY2025": -24424, "FY2024": -22659, "FY2023": -22522, "FY2022": -18321, "FY2021": -16210, "FY2020": -16522, "FY2019": -15584}),
        ("TOTAL", "Operating profit before profit/(loss) on sale of loans, impairment and taxes", {"FY2026": 21250, "FY2025": 24161, "FY2024": 31940, "FY2023": 26523, "FY2022": 19302, "FY2021": 10420, "FY2020": 12343, "FY2019": 11625}),
        ("DATA", "Profit/(loss) on sale of loans", {"FY2026": 0, "FY2025": -158, "FY2024": -194, "FY2023": 9, "FY2022": -44, "FY2021": 129, "FY2020": -4528, "FY2019": 0}),
        ("DATA", "Impairment reversal/(charge) on loans", {"FY2026": 250, "FY2025": 651, "FY2024": 106, "FY2023": -219, "FY2022": -1546, "FY2021": -1352, "FY2020": -3900, "FY2019": -1852}),
        ("TOTAL", "Profit on ordinary activities before tax", {"FY2026": 21500, "FY2025": 24654, "FY2024": 31852, "FY2023": 26313, "FY2022": 17712, "FY2021": 9197, "FY2020": 3915, "FY2019": 9773}),
        ("DATA", "Tax on profit of ordinary activities", {"FY2026": -5422, "FY2025": -6129, "FY2024": -8052, "FY2023": -5125, "FY2022": -3476, "FY2021": -1774, "FY2020": -560, "FY2019": -1989}),
        ("TOTAL", "Profit on ordinary activities after tax", {"FY2026": 16078, "FY2025": 18525, "FY2024": 23800, "FY2023": 21188, "FY2022": 14236, "FY2021": 7423, "FY2020": 3355, "FY2019": 7784}),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Revaluation of available-for-sale investment/debt securities", {"FY2026": -2083, "FY2025": 2230, "FY2024": 3613, "FY2023": -2939, "FY2022": -3770, "FY2021": 870, "FY2020": -992, "FY2019": 29}),
        ("DATA", "Deferred tax adjustment on available-for-sale investment securities", {"FY2026": 520, "FY2025": -557, "FY2024": -903, "FY2023": 735, "FY2022": 948, "FY2021": -165, "FY2020": 189, "FY2019": -5}),
        ("TOTAL", "Total other comprehensive income", {"FY2026": -1563, "FY2025": 1673, "FY2024": 2710, "FY2023": -2204, "FY2022": -2822, "FY2021": 705, "FY2020": -803, "FY2019": 24}),
        ("TOTAL", "Total comprehensive income for the year", {"FY2026": 14515, "FY2025": 20198, "FY2024": 26510, "FY2023": 18984, "FY2022": 11414, "FY2021": 8128, "FY2020": 2552, "FY2019": 7808}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=340,
)

EQUITY_HEADERS = ["Share capital", "Profit and loss", "Other comprehensive income", "Total comprehensive income", "Total equity"]
bw.add_equity_changes_sheet(
    title="State Bank of India (UK) Limited — Statement of Changes in Equity",
    subtitle="Entity basis, £'000, chronological (oldest to newest). See source note at bottom.",
    headers=EQUITY_HEADERS,
    rows=[
        ("TOTAL", "As at 1 April 2018", (175000, 329, 0, None, 175329)),
        ("DATA", "Profit on ordinary activities after tax", (0, 7784, 0, 7784, 7784)),
        ("DATA", "Movement in valuation of available-for-sale debt securities (net of deferred tax)", (0, 0, 24, 24, 24)),
        ("TOTAL", "As at 31 March 2019", (175000, 8113, 24, 7808, 183137)),
        ("DATA", "Profit on ordinary activities after tax", (0, 3355, 0, 3355, 3355)),
        ("DATA", "Movement in valuation of available-for-sale debt securities (net of deferred tax)", (0, 0, -803, -803, -803)),
        ("TOTAL", "As at 31 March 2020", (175000, 11468, -779, 2552, 185689)),
        ("DATA", "Conversion of subordinated debt to equity capital", (50000, 0, 0, 0, 50000)),
        ("DATA", "Profit on ordinary activities after tax", (0, 7423, 0, 7423, 7423)),
        ("DATA", "Movement in valuation of available-for-sale debt securities (net of deferred tax)", (0, 0, 705, 705, 705)),
        ("TOTAL", "As at 31 March 2021", (225000, 18891, -74, 18817, 243817)),
        ("DATA", "Profit on ordinary activities after tax", (0, 14236, 0, 14236, 14236)),
        ("DATA", "Interim dividends paid", (0, -5625, 0, -5625, -5625)),
        ("DATA", "Movement in valuation of available-for-sale debt securities", (0, 0, -3770, -3770, -3770)),
        ("DATA", "Deferred tax", (0, 0, 948, 948, 948)),
        ("TOTAL", "As at 31 March 2022", (225000, 27502, -2896, 24606, 249606)),
        ("DATA", "Profit on ordinary activities after tax", (0, 21188, 0, 21188, 21188)),
        ("DATA", "Interim dividends paid", (0, -8438, 0, -8438, -8438)),
        ("DATA", "Movement in valuation of available-for-sale debt securities", (0, 0, -2939, -2939, -2939)),
        ("DATA", "Deferred tax", (0, 0, 735, 735, 735)),
        ("TOTAL", "As at 31 March 2023", (225000, 40252, -5100, 35152, 260152)),
        ("DATA", "Interim dividends paid", (0, -14400, 0, -14400, -14400)),
        ("DATA", "Profit on ordinary activities after tax", (0, 23800, 0, 23800, 23800)),
        ("DATA", "Movement in valuation of available-for-sale debt securities", (0, 0, 3613, 3613, 3613)),
        ("DATA", "Deferred tax", (0, 0, -903, -903, -903)),
        ("TOTAL", "As at 31 March 2024", (225000, 49652, -2390, 47262, 272262)),
        ("DATA", "Interim dividends paid", (0, -15000, 0, -15000, -15000)),
        ("DATA", "Profit on ordinary activities after tax", (0, 18525, 0, 18525, 18525)),
        ("DATA", "Movement in valuation of available-for-sale debt securities", (0, 0, 2230, 2230, 2230)),
        ("DATA", "Deferred tax", (0, 0, -557, -557, -557)),
        ("TOTAL", "As at 31 March 2025", (225000, 53177, -717, 52460, 277460)),
        ("DATA", "Interim dividends paid", (0, -13000, 0, -13000, -13000)),
        ("DATA", "Profit on ordinary activities after tax", (0, 16078, 0, 16078, 16078)),
        ("DATA", "Movement in valuation of available-for-sale debt securities", (0, 0, -2083, -2083, -2083)),
        ("DATA", "Deferred tax", (0, 0, 520, 520, 520)),
        ("TOTAL", "As at 31 March 2026", (225000, 56255, -2280, 53975, 278975)),
    ],
    sources_text=EQUITY_SOURCES,
    source_height=340,
)

bw.add_cash_flow_sheet(
    title="State Bank of India (UK) Limited — Cash Flow Statement",
    subtitle="Not applicable — the entity takes the FRS 102 cash-flow-statement exemption. See source note below.",
    rows=[
        ("SECTION", "No Statement of Cash Flows is published by this entity", {}),
        ("DATA", "This workbook is the Pillar-3-only variant; the exemption and source evidence are documented below.", {}),
    ],
    sources_text=ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE,
    first_col_width=92,
    source_height=280,
    unit_suffix="",
)

bw.add_asset_quality_sheet(
    title="State Bank of India (UK) Limited — Asset Quality",
    subtitle="Pillar 3 credit risk exposures, £m. Not IFRS 9-staged (FRS 102 entity) — categorised by degree "
              "of risk of financial loss. See source note at bottom.",
    rows=[
        ("SECTION", "Loan book by risk of financial loss (Pillar 3 credit risk exposures)", {}),
        ("DATA", "Neither past due beyond 90 days nor impaired", {"FY2025": 1537.46, "FY2024": 1420.37, "FY2023": 1408.07, "FY2022": 1205.40, "FY2021": 1142.58, "FY2020": 1101.735, "FY2019": 1046.264}),
        ("DATA", "Past due beyond 90 days, but not impaired", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0}),
        ("DATA", "Impaired", {"FY2025": 0, "FY2024": 2.19, "FY2023": 5.32, "FY2022": 5.03, "FY2021": 4.61, "FY2020": 4.565, "FY2019": 0}),
        ("DATA", "Repossessions", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0}),
        ("DATA", "Unutilised overdraft commitments", {"FY2025": 19.93, "FY2024": 34.79, "FY2023": 25.45, "FY2022": 6.52, "FY2021": 8.51, "FY2020": 10.115, "FY2019": 8.253}),
        ("DATA", "Pipeline loans", {"FY2025": 37.89, "FY2024": 10.67, "FY2023": 15.71, "FY2022": 69.29, "FY2021": 86.83, "FY2020": 72.036, "FY2019": 12.927}),
        ("TOTAL", "Total maximum exposure of loans and advances to customers", {"FY2025": 1595.28, "FY2024": 1468.02, "FY2023": 1454.55, "FY2022": 1286.23, "FY2021": 1242.53, "FY2020": 1188.451, "FY2019": 1067.444}),
        ("SECTION", "Collateral", {}),
        ("DATA", "Collateral value", {"FY2025": 1288.58, "FY2024": 1149.26, "FY2023": 1048.50, "FY2022": 770.94, "FY2021": 596.94, "FY2020": 509.338, "FY2019": 417.850}),
        ("DATA", "Gross loans and advances", {"FY2025": 1537.45, "FY2024": 1422.56, "FY2023": 1413.39, "FY2022": 1210.42, "FY2021": 1147.19, "FY2020": 1106.300, "FY2019": 1046.264}),
        ("DATA", "Collateral coverage (% of gross loans and advances)", {"FY2025": "83.81%", "FY2024": "80.79%", "FY2023": "74.18%", "FY2022": "63.69%", "FY2021": "52.03%", "FY2020": "46.04%", "FY2019": "39.94%"}),
        ("SECTION", "Forbearance", {}),
        ("DATA", "Business customers granted forbearance (count)", {"FY2025": 3, "FY2024": 4, "FY2023": 3, "FY2022": 7, "FY2021": 8, "FY2020": 0, "FY2019": 0}),
        ("DATA", "Total forbearance exposure, £m", {"FY2025": 4.60, "FY2024": 6.13, "FY2023": 6.71, "FY2022": 83, "FY2021": 82, "FY2020": 0, "FY2019": 0}),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=66,
    source_height=260,
    unit_suffix=" (£m)",
)


# ---------------------------------------------------------------
# KM1 Key Metrics - SBI UK's own published UK KM1 template.
#
# The Bank heads the table "UK KM1 - Key Metrics:" and prints it UNNUMBERED,
# in £m, splitting it across three tables on consecutive pages: the capital /
# SREP / buffer / leverage block, then a Liquidity Coverage Ratio table, then
# a Net Stable Funding Ratio table. All three are reproduced here in template
# order, which is the order the Bank prints them in.
#
# FY2025-FY2022 come from their own editions. FY2021 is filled from the
# FY2022 edition's 2021 comparative column - the FY2021 edition prints a short
# bespoke capital table that fails the row-set test. FY2026 is blank because
# no FY2026 Pillar 3 has been published (see P3_PENDING_NOTE); FY2020 and
# FY2019 are blank for the same row-set reason as FY2021, and neither has a
# comparative anywhere to fill from.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) capital (£m)",
     {"FY2025": 277.00, "FY2024": 271.82, "FY2023": 259.67, "FY2022": 249.19, "FY2021": 243.50}),
    ("DATA", "Tier 1 capital (£m)",
     {"FY2025": 277.00, "FY2024": 271.82, "FY2023": 259.67, "FY2022": 249.19, "FY2021": 243.50}),
    ("DATA", "Total capital (£m)",
     {"FY2025": 277.00, "FY2024": 271.82, "FY2023": 259.67, "FY2022": 249.19, "FY2021": 247.76}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "Total risk-weighted exposure amount (£m)",
     {"FY2025": 1320.25, "FY2024": 1213.02, "FY2023": 1227.04, "FY2022": 1276.68, "FY2021": 1357.75}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Common Equity Tier 1 ratio (%)",
     {"FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "17.93%"}),
    ("DATA", "Tier 1 ratio (%)",
     {"FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "17.93%"}),
    ("DATA", "Total capital ratio (%)",
     {"FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "18.25%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Additional CET1 SREP requirements (%)",
     {"FY2025": "1.59%", "FY2024": "1.59%", "FY2023": "3.63%", "FY2022": "3.63%", "FY2021": "3.63%"}),
    ("DATA", "Additional AT1 SREP requirements (%)",
     {"FY2025": "0.53%", "FY2024": "0.53%", "FY2023": "0.73%", "FY2022": "0.73%", "FY2021": "0.73%"}),
    ("DATA", "Additional T2 SREP requirements (%)",
     {"FY2025": "0.71%", "FY2024": "0.71%", "FY2023": "0.97%", "FY2022": "0.97%", "FY2021": "0.97%"}),
    ("DATA", "Total SREP own funds requirements (%)",
     {"FY2025": "10.82%", "FY2024": "10.82%", "FY2023": "13.33%", "FY2022": "13.33%", "FY2021": "13.33%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Capital conservation buffer (%)",
     {"FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "Conservation buffer due to macro-prudential or systemic risk identified at the level of a Member State (%)",
     {"FY2025": "0.00%", "FY2024": "0.00%", "FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
    ("DATA", "Institution specific countercyclical capital buffer (%)",
     {"FY2025": "1.48%", "FY2024": "1.39%", "FY2023": "0.60%", "FY2022": "0.00%", "FY2021": "0.00%"}),
    ("DATA", "Systemic risk buffer (%)",
     {"FY2025": "0.00%", "FY2024": "0.00%", "FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
    ("DATA", "Global Systemically Important Institution buffer (%)",
     {"FY2025": "0.00%", "FY2024": "0.00%", "FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
    ("DATA", "Other Systemically Important Institution buffer",
     {"FY2025": "0.00%", "FY2024": "0.00%", "FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
    ("DATA", "Combined buffer requirement (%)",
     {"FY2025": "3.98%", "FY2024": "3.89%", "FY2023": "3.10%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "Overall capital requirements (%)",
     {"FY2025": "14.80%", "FY2024": "14.71%", "FY2023": "16.43%", "FY2022": "15.83%", "FY2021": "15.83%"}),
    ("DATA", "CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "10.07%", "FY2024": "9.98%", "FY2023": "11.23%", "FY2022": "10.63%", "FY2021": "10.63%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "Total exposure measure excluding claims on central banks (£m)",
     {"FY2025": 1919.23, "FY2024": 1774.80, "FY2023": 1864.49, "FY2022": 1749.04}),
    ("DATA", "Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "14.43%", "FY2024": "15.32%", "FY2023": "13.93%", "FY2022": "14.25%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "Total high-quality liquid assets (HQLA) (Weighted value -average) (£m)",
     {"FY2025": 183.96, "FY2024": 184.64, "FY2023": 188.83, "FY2022": 142.01}),
    ("DATA", "Cash outflows - Total weighted value (£m)",
     {"FY2025": 80.05, "FY2024": 105.33, "FY2023": 135.01, "FY2022": 124.25}),
    ("DATA", "Cash inflows - Total weighted value (£m)",
     {"FY2025": 48.09, "FY2024": 49.57, "FY2023": 43.28, "FY2022": 37.66}),
    ("DATA", "Total net cash outflows (adjusted value) (£m)",
     {"FY2025": 36.64, "FY2024": 55.75, "FY2023": 91.72, "FY2022": 86.59}),
    ("DATA", "Liquidity coverage ratio (%)",
     {"FY2025": "572.38%", "FY2024": "331.15%", "FY2023": "205.87%", "FY2022": "164.00%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "Total available stable funding (£m)",
     {"FY2025": 1782.87, "FY2024": 1687, "FY2023": 1765, "FY2022": 1571.94}),
    ("DATA", "Total required stable funding (£m)",
     {"FY2025": 1311.47, "FY2024": 1200, "FY2023": 1231, "FY2022": 1209.80}),
    ("DATA", "NSFR ratio (%)",
     {"FY2025": "135.94%", "FY2024": "140.48%", "FY2023": "143.36%", "FY2022": "129.93%"}),
]

KM1_SOURCES = (
    "Sources - State Bank of India (UK) Limited's own 'UK KM1 - Key Metrics' template, £m and % as printed. "
    "The Bank splits the template across three consecutive tables (capital/SREP/buffers/leverage, then "
    "Liquidity Coverage Ratio, then Net Stable Funding Ratio):\n"
    f"FY2025: Pillar 3 disclosure for the year ended 31 March 2025, pp. {PAGES['FY2025']} - {P3['FY2025']}\n"
    f"FY2024: Pillar 3 disclosure for the year ended 31 March 2024, pp. {PAGES['FY2024']} - {P3['FY2024']}\n"
    f"FY2023: Pillar 3 disclosure for the year ended 31 March 2023, pp. {PAGES['FY2023']} - {P3['FY2023']}\n"
    f"FY2022: Pillar 3 disclosure for the year ended 31 March 2022, pp. {PAGES['FY2022']} - {P3['FY2022']}\n"
    f"FY2021: the FY2022 disclosure's 2021 comparative column, same pages - {P3['FY2022']}\n\n"
    "LATEST-EDITION CHECK, 2026-09-17: sbiuk.statebank was read directly (root HTTP 200; the "
    "/regulatory-disclosures path returns 404 and the site's own sitemap carries no Pillar 3 links). No FY2026 "
    "Pillar 3 document is published, consistent with the Bank's pattern of publishing each year's disclosure "
    "several months after the accounts (FY2025's went up 29 December 2025, FY2024's 28 October 2024). Checked, "
    "none newer than FY2025.\n\n"
    "WHY FY2026 IS BLANK: no Pillar 3 disclosure exists for the year ended 31 March 2026 yet, so there is no "
    "KM1 table to reproduce. The FY2026 capital and ratio figures that DO appear on the metric sheets come from "
    "the FY2026 Annual Report's own Regulatory Capital resources table, which is not this template and is not "
    "mapped onto it here.\n\n"
    "WHY FY2021 IS FILLED FROM THE FY2022 EDITION, AND WHY FY2020/FY2019 ARE NOT FILLED AT ALL. The FY2021, "
    "FY2020 and FY2019 disclosures pre-date the Bank's adoption of the template: each prints a short bespoke "
    "capital table (capital resources, RWAs and ratios, with headline LCR and NSFR percentages quoted in a "
    "financial-ratios section) and none carries the SREP rows, the buffer block, the overall capital "
    "requirement row or the LCR/NSFR build-ups. On the row-set test that is a different and shorter table, not "
    "an unnumbered template. The FY2022 edition prints a full 2021 comparative column, so FY2021 is filled from "
    "it and labelled as such; no edition anywhere prints a 2020 or 2019 comparative in template form, so those "
    "two years stay blank. What those older tables do disclose is on the individual metric sheets.\n\n"
    "ROWS LEFT BLANK IN THE FILLED FY2021 COLUMN: the FY2022 edition prints its leverage block, its LCR table "
    "and its NSFR table with a 2022 column only - there is no 2021 comparative for those rows anywhere in the "
    "document - so the FY2021 cells are blank rather than carried across from the Bank's older financial-ratios "
    "presentation, which is a different basis. The headline FY2021 LCR (156%) and NSFR (124%) that the FY2021 "
    "edition does quote remain on the LCR and NSFR metric sheets.\n\n"
    "SOURCE DEFECTS, REPRODUCED NOT CORRECTED:\n"
    "- The FY2025 edition's narrative above the table says 'the capital adequacy ratio remained strong at "
    "20.99%, with a Tier 1 capital ratio of 20.99%' while the table itself prints 20.98% in all three ratio "
    "rows. The table's figure is what is reproduced here, and it is what the metric sheets carry.\n"
    "- The FY2022 edition prints '0.00%' against the 'Combined buffer requirement (as a percentage of "
    "risk-weighted exposure amount)' CAPTION row - a section heading that should carry no figures - as well as "
    "the real 2.50% on the 'Combined buffer requirement (%)' row beneath it. The caption is a divider here and "
    "the stray zeroes are not reproduced as data; the row that carries the figure is.\n"
    "- The FY2023 and FY2022 editions print the total RWEA without a thousands separator ('1276.68', "
    "'1357.75'). That is a typographic difference only; the value is unchanged.\n"
    "- The FY2024 and FY2023 editions print the two NSFR amount rows as whole £m ('1,687', '1,200', '1,765', "
    "'1,231') while every other amount carries two decimals. The Bank's own precision is kept.\n"
    "- The Bank's last buffer row is captioned 'Other Systemically Important Institution buffer', without the "
    "'(%)' the other buffer rows carry, in every edition. Reproduced as printed.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="State Bank of India (UK) Limited — KM1 Key Metrics",
    subtitle="The Bank's own published 'UK KM1 - Key Metrics' template, reproduced whole in its own row order, "
             "labels and printed precision. SBI UK prints the template unnumbered and splits it across three "
             "consecutive tables (capital/SREP/buffers/leverage, LCR, NSFR), which are shown here in template "
             "order. Amounts in £m, ratios as printed. FY2025-FY2022 come from their own editions; FY2021 is "
             "the FY2022 edition's comparative column. FY2026 is blank because no FY2026 Pillar 3 has been "
             "published, and FY2020/FY2019 pre-date the Bank's adoption of the template - see the source note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=72,
    source_height=460,
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, sources(), note=note, first_col_width=52, source_height=150)


metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", {"FY2026": 278.47, "FY2025": 277.00, "FY2024": 271.82, "FY2023": 259.67, "FY2022": 249.19, "FY2021": 243.50, "FY2020": 185.5, "FY2019": 183.1})], "FY2026 SOURCE DIFFERS: SBI UK's FY2026 Pillar 3 disclosure is not yet published (see the source note), so the FY2026 figure here is the one printed in the FY2026 Annual Report itself - the 'Regulatory Capital resources' table (p.61) for capital amounts and the financial-ratios summary (p.7) for ratios. That table is the same basis as the Pillar 3 KM1: the Annual Report's FY2025 comparatives (Total Tier 1 capital GBP 276,997k, CET1 and total capital adequacy ratio 21.0%) reproduce this workbook's Pillar 3-sourced FY2025 figures (GBP 277.00m, 20.98%) exactly, differing only in the Annual Report's 1-decimal rounding. The ratios are therefore shown to 1 decimal place for FY2026 and 2 for earlier years - a source-precision difference, not a basis change.")
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", {"FY2026": "19.6%", "FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "17.93%", "FY2020": "13.5%", "FY2019": "13.7%"})], "FY2026 SOURCE DIFFERS: SBI UK's FY2026 Pillar 3 disclosure is not yet published (see the source note), so the FY2026 figure here is the one printed in the FY2026 Annual Report itself - the 'Regulatory Capital resources' table (p.61) for capital amounts and the financial-ratios summary (p.7) for ratios. That table is the same basis as the Pillar 3 KM1: the Annual Report's FY2025 comparatives (Total Tier 1 capital GBP 276,997k, CET1 and total capital adequacy ratio 21.0%) reproduce this workbook's Pillar 3-sourced FY2025 figures (GBP 277.00m, 20.98%) exactly, differing only in the Annual Report's 1-decimal rounding. The ratios are therefore shown to 1 decimal place for FY2026 and 2 for earlier years - a source-precision difference, not a basis change.")
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2026": 278.47, "FY2025": 277.00, "FY2024": 271.82, "FY2023": 259.67, "FY2022": 249.19, "FY2021": 243.50, "FY2020": 185.5, "FY2019": 183.1})], "Tier 1 equals CET1 in every year shown; no AT1 capital is reported. " + "FY2026 SOURCE DIFFERS: SBI UK's FY2026 Pillar 3 disclosure is not yet published (see the source note), so the FY2026 figure here is the one printed in the FY2026 Annual Report itself - the 'Regulatory Capital resources' table (p.61) for capital amounts and the financial-ratios summary (p.7) for ratios. That table is the same basis as the Pillar 3 KM1: the Annual Report's FY2025 comparatives (Total Tier 1 capital GBP 276,997k, CET1 and total capital adequacy ratio 21.0%) reproduce this workbook's Pillar 3-sourced FY2025 figures (GBP 277.00m, 20.98%) exactly, differing only in the Annual Report's 1-decimal rounding. The ratios are therefore shown to 1 decimal place for FY2026 and 2 for earlier years - a source-precision difference, not a basis change.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2026": "19.6%", "FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "17.93%", "FY2020": "13.5%", "FY2019": "13.7%"})], "FY2026 SOURCE DIFFERS: SBI UK's FY2026 Pillar 3 disclosure is not yet published (see the source note), so the FY2026 figure here is the one printed in the FY2026 Annual Report itself - the 'Regulatory Capital resources' table (p.61) for capital amounts and the financial-ratios summary (p.7) for ratios. That table is the same basis as the Pillar 3 KM1: the Annual Report's FY2025 comparatives (Total Tier 1 capital GBP 276,997k, CET1 and total capital adequacy ratio 21.0%) reproduce this workbook's Pillar 3-sourced FY2025 figures (GBP 277.00m, 20.98%) exactly, differing only in the Annual Report's 1-decimal rounding. The ratios are therefore shown to 1 decimal place for FY2026 and 2 for earlier years - a source-precision difference, not a basis change.")
metric("Total Capital", "£m", [("Total capital", {"FY2026": 278.47, "FY2025": 277.00, "FY2024": 271.82, "FY2023": 259.67, "FY2022": 249.19, "FY2021": 247.76, "FY2020": 238.7, "FY2019": 235.0})], "Total capital exceeds CET1/Tier 1 in FY2019-FY2021 because the source reports Tier 2 capital (subordinated debt, £53.2m FY2020/£51.9m FY2019, most of which was converted to CET1 share capital during FY2021, leaving a small residual £4.26m of Tier 2 in FY2021 - see the Statement of Changes in Equity's 'Conversion of subordinated debt to equity capital' row); from FY2022 onward, with no Tier 2 remaining, total capital equals CET1/Tier 1. "
    "FY2026's Total capital is set equal to Tier 1 on the same footing: the FY2026 Annual Report "
    "states a common Tier 1 capital ratio of 19.6% and a total capital adequacy ratio of 19.6%, i.e. "
    "no Tier 2, and its Regulatory Capital resources table (p.61) shows Tier 1 capital only. " + "FY2026 SOURCE DIFFERS: SBI UK's FY2026 Pillar 3 disclosure is not yet published (see the source note), so the FY2026 figure here is the one printed in the FY2026 Annual Report itself - the 'Regulatory Capital resources' table (p.61) for capital amounts and the financial-ratios summary (p.7) for ratios. That table is the same basis as the Pillar 3 KM1: the Annual Report's FY2025 comparatives (Total Tier 1 capital GBP 276,997k, CET1 and total capital adequacy ratio 21.0%) reproduce this workbook's Pillar 3-sourced FY2025 figures (GBP 277.00m, 20.98%) exactly, differing only in the Annual Report's 1-decimal rounding. The ratios are therefore shown to 1 decimal place for FY2026 and 2 for earlier years - a source-precision difference, not a basis change.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2026": "19.6%", "FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "18.25%", "FY2020": "17.4%", "FY2019": "17.5%"})], "FY2026 SOURCE DIFFERS: SBI UK's FY2026 Pillar 3 disclosure is not yet published (see the source note), so the FY2026 figure here is the one printed in the FY2026 Annual Report itself - the 'Regulatory Capital resources' table (p.61) for capital amounts and the financial-ratios summary (p.7) for ratios. That table is the same basis as the Pillar 3 KM1: the Annual Report's FY2025 comparatives (Total Tier 1 capital GBP 276,997k, CET1 and total capital adequacy ratio 21.0%) reproduce this workbook's Pillar 3-sourced FY2025 figures (GBP 277.00m, 20.98%) exactly, differing only in the Annual Report's 1-decimal rounding. The ratios are therefore shown to 1 decimal place for FY2026 and 2 for earlier years - a source-precision difference, not a basis change.")
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", {"FY2025": 1320.25, "FY2024": 1213.02, "FY2023": 1227.04, "FY2022": 1276.68, "FY2021": 1357.75, "FY2020": 1375.0, "FY2019": 1339.4})], "FY2026 is blank: SBI UK's FY2026 Pillar 3 disclosure - the only source that publishes a total risk-weighted exposure amount - is not yet out, and the FY2026 Annual Report discloses capital ratios and capital amounts but no RWA figure. It has deliberately NOT been back-solved from Tier 1 capital divided by the 19.6% ratio: that ratio is rounded to one decimal place, so the implied RWA would be a derived estimate spanning roughly GBP 1,417-1,424m, not a disclosed figure. See the source note.")

bw.add_rwa_breakdown_sheet(
    title="State Bank of India (UK) Limited — RWA Breakdown",
    subtitle="UK OV1 - Overview of risk-weighted exposure amounts, £m. FY2019/FY2020 use an older, differently-"
              "categorised Pillar 1 RWA table - see source note at bottom.",
    rows=[
        ("SECTION", "UK OV1 — Overview of risk-weighted exposure amounts", {}),
        ("DATA", "Credit risk (excluding CCR)", {"FY2025": 1216.73, "FY2024": 1115.26, "FY2023": 1138.84, "FY2022": 1201.92, "FY2021": 1286.62}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 7.60, "FY2024": 9.05, "FY2023": 16.89, "FY2022": 17.00, "FY2021": 18.47}),
        ("DATA", "Credit risk incl. CVA & CCR-for-forex-swap (FY2019-FY2020 Pillar 1 categorisation, see note)", {"FY2020": 1324.7, "FY2019": 1277.2}),
        ("DATA", "Market risk (FY2019-FY2020 only, see note)", {"FY2020": 0, "FY2019": 1.1}),
        ("DATA", "Operational risk", {"FY2025": 95.33, "FY2024": 88.71, "FY2023": 71.30, "FY2022": 57.76, "FY2021": 52.66, "FY2020": 50.4, "FY2019": 61.0}),
        ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 1320.25, "FY2024": 1213.02, "FY2023": 1227.04, "FY2022": 1276.68, "FY2021": 1357.75, "FY2020": 1375.0, "FY2019": 1339.4}),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=200,
    unit_suffix=" (£m)",
)

metric("Leverage Ratio", "£m / %", [
    ("Total exposure measure excluding claims on central banks", {"FY2025": 1919.23, "FY2024": 1774.80, "FY2023": 1864.49, "FY2022": 1749.04}),
    ("Leverage ratio excluding claims on central banks (%)", {"FY2026": "13.4%", "FY2025": "14.43%", "FY2024": "15.32%", "FY2023": "13.93%", "FY2022": "14.25%"}),
    ("Leverage ratio (financial-ratios presentation; basis not specified)", {"FY2021": "13.5%"}),
    ("Total leverage ratio exposure (CRD IV basis, FY2019-FY2020 only, see note)", {"FY2020": 1810.3, "FY2019": 1617.7}),
    ("Leverage ratio (CRD IV basis, FY2019-FY2020 only, see note)", {"FY2020": "10.3%", "FY2019": "11.3%"}),
], "The FY2021 report presents only a headline leverage ratio in its financial-ratios section, on an unspecified basis. FY2019/FY2020 disclose a full CRD IV LRSum/LRCom leverage exposure table (Tier 1 capital / total on- and off-balance-sheet and derivative exposures), a third, older basis that does not exclude central-bank claims - shown in its own pair of rows rather than merged with the FY2021 row or the FY2022+ excluding-central-bank-claims basis. The excluding-central-bank-claims exposure measure and ratio first appear in the FY2022 UK KM1 table; none of FY2019/FY2020/FY2021 are relabelled or inferred onto that basis.")
metric("LCR", "£m / %", [
    ("Total high-quality liquid assets (HQLA), weighted value - average", {"FY2025": 183.96, "FY2024": 184.64, "FY2023": 188.83, "FY2022": 142.01}),
    ("Cash outflows - total weighted value", {"FY2025": 80.05, "FY2024": 105.33, "FY2023": 135.01, "FY2022": 124.25}),
    ("Cash inflows - total weighted value", {"FY2025": 48.09, "FY2024": 49.57, "FY2023": 43.28, "FY2022": 37.66}),
    ("Total net cash outflows (adjusted value)", {"FY2025": 36.64, "FY2024": 55.75, "FY2023": 91.72, "FY2022": 86.59}),
    ("Liquidity coverage ratio (%) - Pillar 3 KM1, 12-month average of weighted values", {"FY2025": "572.38%", "FY2024": "331.15%", "FY2023": "205.87%", "FY2022": "164.00%", "FY2021": "156%", "FY2020": "179%", "FY2019": "292.9%"}),
    ("Liquidity coverage ratio (%) - Annual Report financial-ratios presentation (year-end basis)", {"FY2026": "181%", "FY2025": "319%"}),
], "FY2021/FY2020/FY2019's Pillar 3 reports disclose only the headline LCR ratio in their financial-ratios/Key Metrics presentation; no HQLA/outflow/inflow component amounts were found for these three years, so they remain blank. "
   "FY2026 LCR IS ON A DIFFERENT BASIS AND IS SHOWN ON ITS OWN ROW: SBI UK's FY2026 Pillar 3 disclosure is not yet published, so no FY2026 figure exists on the KM1 12-month-average basis used by the row above. "
   "The FY2026 Annual Report's financial-ratios summary (p.7) does print an LCR of 181% (2025: 319%), but that is a year-end point-in-time figure, not the KM1 average: for FY2025 the same Annual Report basis gives 319% against the Pillar 3 KM1's 572.38%. "
   "The two are therefore kept on separate rows rather than continued as one series, and the FY2025 Annual-Report comparative is shown alongside FY2026 so the size of the basis difference is visible. "
   "For the same reason the Overview sheet's LCR trend row is left blank for FY2026 rather than mixing the two bases in one chart.")
metric("NSFR", "£m / %", [
    ("Total available stable funding", {"FY2025": 1782.87, "FY2024": 1687.00, "FY2023": 1765.00, "FY2022": 1571.94}),
    ("Total required stable funding", {"FY2025": 1311.47, "FY2024": 1200.00, "FY2023": 1231.00, "FY2022": 1209.80}),
    ("NSFR ratio (%)", {"FY2026": "130%", "FY2025": "135.94%", "FY2024": "140.48%", "FY2023": "143.36%", "FY2022": "129.93%", "FY2021": "124%", "FY2020": "120%", "FY2019": "123%"}),
], "FY2021/FY2020/FY2019's Pillar 3 reports disclose only the headline NSFR ratio; no ASF/RSF component amounts were found for these three years, so they remain blank.")
metric("MREL Ratio", "£m / %", [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No numeric MREL ratio was disclosed in the five SBI UK Pillar 3 documents reviewed; it is not inferred from capital or liquidity metrics.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2026": 2079942, "FY2025": 1960169, "FY2024": 1842936, "FY2023": 1976962, "FY2022": 1776005, "FY2021": 1755410, "FY2020": 1757299, "FY2019": 1595279}),
        ("Loans and advances to customers", {"FY2026": 1655683, "FY2025": 1529812, "FY2024": 1415920, "FY2023": 1403369, "FY2022": 1201300, "FY2021": 1140238, "FY2020": 1101038, "FY2019": 1044412}),
        ("Deposit from customers", {"FY2026": 1784374, "FY2025": 1655992, "FY2024": 1530535, "FY2023": 1568185, "FY2022": 1339203, "FY2021": 1360344, "FY2020": 1418658, "FY2019": 1310363}),
        ("Total equity", {"FY2026": 278975, "FY2025": 277460, "FY2024": 272262, "FY2023": 260152, "FY2022": 249606, "FY2021": 243817, "FY2020": 185689, "FY2019": 183137}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income", {"FY2026": 49466, "FY2025": 48585, "FY2024": 54599, "FY2023": 49045, "FY2022": 37623, "FY2021": 26630, "FY2020": 28865, "FY2019": 27209}),
        ("Total operating expenses", {"FY2026": -28216, "FY2025": -24424, "FY2024": -22659, "FY2023": -22522, "FY2022": -18321, "FY2021": -16210, "FY2020": -16522, "FY2019": -15584}),
        ("Profit on ordinary activities after tax", {"FY2026": 16078, "FY2025": 18525, "FY2024": 23800, "FY2023": 21188, "FY2022": 14236, "FY2021": 7423, "FY2020": 3355, "FY2019": 7784}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2026": 277460, "FY2025": 272262, "FY2024": 260152, "FY2023": 249606, "FY2022": 243817, "FY2021": 185689, "FY2020": 183137, "FY2019": 175329}),
        ("Total comprehensive income for the year", {"FY2026": 14515, "FY2025": 20198, "FY2024": 26510, "FY2023": 18984, "FY2022": 11414, "FY2021": 8128, "FY2020": 2552, "FY2019": 7808}),
        ("Other equity movements, net", {"FY2026": -13000, "FY2025": -15000, "FY2024": -14400, "FY2023": -8438, "FY2022": -5625, "FY2021": 50000, "FY2020": 0, "FY2019": 0}),
        ("Closing equity", {"FY2026": 278975, "FY2025": 277460, "FY2024": 272262, "FY2023": 260152, "FY2022": 249606, "FY2021": 243817, "FY2020": 185689, "FY2019": 183137}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2026": "19.6%", "FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "17.93%", "FY2020": "13.5%", "FY2019": "13.7%"}),
        ("Tier 1 Ratio", {"FY2026": "19.6%", "FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "17.93%", "FY2020": "13.5%", "FY2019": "13.7%"}),
        ("Total Capital Ratio", {"FY2026": "19.6%", "FY2025": "20.98%", "FY2024": "22.41%", "FY2023": "21.16%", "FY2022": "19.52%", "FY2021": "18.25%", "FY2020": "17.4%", "FY2019": "17.5%"}),
        ("Leverage Ratio (excl. central bank claims)", {"FY2026": "13.4%", "FY2025": "14.43%", "FY2024": "15.32%", "FY2023": "13.93%", "FY2022": "14.25%"}),
        ("LCR", {"FY2025": "572.38%", "FY2024": "331.15%", "FY2023": "205.87%", "FY2022": "164.00%", "FY2021": "156%", "FY2020": "179%", "FY2019": "292.9%"}),
        ("NSFR", {"FY2026": "130%", "FY2025": "135.94%", "FY2024": "140.48%", "FY2023": "143.36%", "FY2022": "129.93%", "FY2021": "124%", "FY2020": "120%", "FY2019": "123%"}),
    ],
    note="FY2026 ADDED 2026-09-15 from the Companies House filing of the year-ended-31-March-2026 accounts "
         "(filed 9 September 2026). SBI UK's FY2026 Pillar 3 disclosure is NOT yet published, so FY2026 is "
         "blank on Asset Quality, RWA Breakdown and Total RWAs, and the FY2026 capital, leverage and NSFR "
         "figures shown come from the Annual Report's own Regulatory Capital resources table and "
         "financial-ratios summary (a basis the Annual Report's FY2025 comparatives confirm matches the "
         "Pillar 3 KM1, to 1 decimal place). The LCR trend row above is deliberately blank for FY2026: the "
         "Annual Report's LCR is a year-end figure (FY2026 181%) while the Pillar 3 series is a 12-month "
         "average (FY2025 572.38% against the Annual Report's own 319% for the same year), so the two are "
         "not continued as one chart series - see the LCR sheet, which shows both on separate rows. "
         "PILLAR-3-ONLY WORKBOOK: SBI UK takes the FRS 102 cash-flow-statement exemption, so the cash-flow sheet documents the exemption and the Overview contains the Pillar 3 trend chart only. "
         "HISTORICAL DEPTH (HD-024): extended back to FY2019, SBI UK's first full 12-month trading year and "
         "first Pillar 3 disclosure - its true confirmed floor. FY2018 (an 18-month pre-operational first "
         "accounting period from incorporation) is self-skipped; see the Balance Sheet/P&L source note.",
)

bw.save("/Users/armaan/code/katalysis/banks/STATE BANK OF INDIA UK FINANCIALS.xlsx")
