import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://ccbank.co.uk/wp-content/uploads/2026/04/Cambridge__Counties-Bank_Annual-Report_2025.pdf"
AR2024_URL = "https://ccbank.co.uk/wp-content/uploads/2025/05/86395_CCB-2024-Annual-Report-web.pdf"
AR2022_URL = "https://ccbank.co.uk/wp-content/uploads/2023/06/CCB_Annual-Report_2022.pdf"

P3_2024_URL = "https://ccbank.co.uk/wp-content/uploads/2025/05/Pillar-3-report-CCB-2024.docx"
P3_2023_URL = "https://ccbank.co.uk/wp-content/uploads/2024/05/Pillar-3-report-2023-Cambridge-Counties-Bank.docx"
P3_2022_URL = "https://ccbank.co.uk/wp-content/uploads/2023/05/Pillar-3-Disclosure2022.pdf"
P3_2021_URL = "https://ccbank.co.uk/wp-content/uploads/2022/06/CCB_Pillar-3-2021.pdf"

# --- HD-020 additions: FY2015-FY2020 ---
# Statutory financial statements (Balance Sheet/P&L/Statement of Changes in Equity/Cash Flow Statement/
# Asset Quality note) for FY2015-FY2020 are no longer published on ccbank.co.uk - the bank's own site
# still lists PDF links under old URLs, but those particular files are Wayback-archived truncated mid-file
# at exactly 1,048,576 bytes by the crawl that captured them (confirmed via the CDX API and a direct
# byte-count check on the response headers, not just assumed truncated). All six years' statutory accounts
# are instead sourced from Companies House's filing history for company 07972522, which holds the
# complete, non-truncated "Full accounts" PDF filed for each year end (each filing carries both its own
# year and the prior year's comparative column, so three filings - FY2016, FY2018 and FY2020 - cover all
# six years FY2015-FY2020). These Companies House filings are scanned/image-only PDFs (no extractable
# text layer) - figures below were read directly off the rendered page images, not OCR'd or text-scraped.
CH_FILING_HISTORY_URL = "https://find-and-update.company-information.service.gov.uk/company/07972522/filing-history"
CH2016_NOTE = "Companies House filing history (company 07972522), 'Full accounts made up to 31 December 2016', filed 07 Mar 2017 (60 pages) - also carries FY2015 comparative"

# Pillar 3 Disclosures for FY2015-FY2020 remain live on ccbank.co.uk.
P3_2020_URL = "https://ccbank.co.uk/wp-content/uploads/2021/07/CCB-Pillar-3-2020.pdf"
P3_2019_URL = "https://ccbank.co.uk/wp-content/uploads/2021/05/CCB-Pillar-3-2019.pdf"
P3_2018_URL = "https://ccbank.co.uk/wp-content/uploads/2021/05/CCB-Pillar-3-2018.pdf"
P3_2017_URL = "https://ccbank.co.uk/wp-content/uploads/2021/05/CCB-Pillar-3-2017.pdf"
P3_2016_URL = "https://ccbank.co.uk/wp-content/uploads/2021/05/CCB-Pillar-3-Disclosures-2016.pdf"
P3_2015_URL = "https://ccbank.co.uk/wp-content/uploads/2021/05/CCB-Pillar-3-Disclosures-2015.pdf"

CET1_ERA_NOTE = (
    "CET1 CAVEAT: the UK/EU CRD IV framework (with its CET1/Tier 1/Total Capital three-way split) took "
    "effect from 1 January 2014, so the CET1 concept already applies throughout this workbook's full "
    "FY2015-FY2025 window - there is no Basel II/CET1-less era to flag for this bank. The one genuine "
    "terminology/methodology shift in the window is IAS 39 to IFRS 9, adopted by the Bank on 1 January "
    "2018: FY2015-FY2017's loan loss allowance is a single collective/individual-assessment figure with "
    "no IFRS 9 stage split, while FY2018 onward is analysed by Stage 1/2/3 - see the Asset Quality "
    "sheet's own note."
)

ENTITY_NOTE = (
    "ENTITY NOTE: Cambridge & Counties Bank Limited (company 07972522, FRN 579415), a UK SME/commercial-property "
    "lender jointly owned by Trinity Hall (a Cambridge University college) and Cambridgeshire County Council as "
    "Administering Authority of the Cambridgeshire Local Government Pension Fund. The Bank has no subsidiaries, so "
    "all figures below are the Bank's own entity-level (not consolidated) results - there is no Group/solo basis "
    "question for this bank. No FRS cash-flow exemption is taken - a full Statement of Cash Flows is published "
    "every year. Cash flow figures for FY2021-FY2025 are internally consistent to the pound across every source "
    "document checked (each year cross-verified against its appearance as the following year's comparative "
    "column). The 2023 and 2024 Pillar 3 disclosures are published as .docx files (not PDF) with the Key Metrics "
    "table embedded as an image rather than as text/a real table - extracted by rendering the embedded image.\n"
    "SDDT EXEMPTION - REASON FOR THE FY2025 PILLAR 3 GAP, established 2026-09-15 (cross-bank SDDT pass). The "
    "FY2025 Pillar 3 blanks are an EVIDENCED STRUCTURAL EXEMPTION, not a 'not published YET' timing gap, and "
    "no FY2025 Pillar 3 document should be expected to appear later: Cambridge & Counties Bank is a Small "
    "Domestic Deposit Taker (SDDT), and becoming one removes the Pillar 3 disclosure obligation outright. "
    "Evidence - the PRA's own firm-level register, the Bank of England consolidated list of waivers and "
    "modifications granted to PRA-authorised firms (downloaded 2026-09-15, "
    "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
    "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv), row: FRN 579415, 'Cambridge & "
    "Counties Bank Limited', 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT "
    "Regime - General Application Part', rule 'SDDT Regime - General Application', sub rule 'Ru 3.1', waiver "
    "ref 'A00009927P.pdf', start date '20/02/2025', no end date. What Rule 3.1 does to Pillar 3 is stated by "
    "a peer holding the identical register row - Cynergy Bank plc Annual Report & Accounts 2024, p.71: 'The "
    "Bank applied for the Modification by Consent to become an SDDT and received approval on 17 January 2025. "
    "As a result, we are not required to publish Pillar 3 disclosures as at 31 December 2024 and will submit "
    "only a simplified retail deposit ratio instead of a full Net Stable Funding Ratio (NSFR) going forward.' "
    "(Cynergy's own register row is Rule 3.1 starting '17/01/2025', matching its stated approval date to the "
    "day - which is what ties the register row to the firm-stated effect.)\n"
    "DATE FIT: the Bank's accounting reference date is 31 DECEMBER, confirmed at Companies House (company "
    "07972522, an unbroken run of accounts to 31 December from 2016 to 2025). The modification took effect 20 "
    "February 2025, before the 31 December 2025 year-end, so it covers FY2025 - the year in which every Pillar "
    "3 metric is blank because no Pillar 3 document exists. It covers FY2024 and earlier NOT AT ALL, and none "
    "of those years needs it: FY2015-FY2024 each have their own published Pillar 3 document, cited above. Do "
    "not read the SDDT exemption back onto FY2024 or earlier.\n"
    "WHAT IT DOES NOT EXPLAIN - FY2021. There is one further outstanding gap year in this workbook and the "
    "SDDT modification has NOTHING to do with it. FY2021 ended 31 December 2021, more than three years before "
    "the 20 February 2025 start date, and the Bank published a full Pillar 3 report for FY2021 which this "
    "workbook draws on throughout. The only FY2021 blank is the NSFR, and it already has its own separate and "
    "entirely sufficient cause: the UK NSFR requirement took effect only for periods beginning after 1 January "
    "2022, so no FY2021 figure was ever required and the FY2021 Pillar 3 report carries no NSFR section at "
    "all. That explanation stands unchanged - it is not an SDDT matter, and a future pass must not relabel it "
    "as one.\n"
    "The Bank's own Annual Reports corroborate the SDDT move but stop short of stating the disclosure "
    "consequence. Both were downloaded and text-extracted in full (readable text layers) and searched: AR2025 "
    "p.36 records the Board 'reviewing and approving our application to operate under the SDDT framework', "
    "p.6 that 'the new Small Domestic Deposit Takers (SDDT) regime will yield further benefits in terms of "
    "capital levels and reporting requirements', and p.28 that the Bank is 'actively preparing for the full "
    "implementation of the Strong & Simple SDDT' framework; AR2024 mentions SDDT only as forthcoming "
    "regulatory change (pp.5, 12, 20, 25). AR2025 p.25 says 'We are currently planning for the implementation "
    "of the SDDT capital framework in 2027' - that is the separate, later simplified CAPITAL regime, NOT the "
    "disclosure exemption, which the register shows already in force from February 2025; the two must not be "
    "conflated. Neither Annual Report discusses Pillar 3 disclosure obligations at all. No Simplified Retail "
    "Deposit Ratio value is disclosed, so nothing replaces the NSFR series."
)

RWA_RESTATEMENT_NOTE = (
    "RWA CAVEAT: FY2022's own Pillar 3 report states Total RWA of £787,621k. FY2023's Pillar 3 report's own "
    "'31-Dec-22' comparative column instead shows £728,379k for the same date - a figure that exactly matches "
    "what FY2022's own report separately states as FY2021's RWA, suggesting the FY2023 report's comparative "
    "column was populated in error (a copy of the prior-prior year) rather than reflecting a genuine restatement. "
    "FY2022's own originally-published figure (£787,621k) is used here, per this project's standing convention of "
    "using each year's own originally-published figures - flagged prominently since the coincidence is unusual "
    "enough to be worth checking against the primary source again if precision matters. FY2015's own Pillar 3 "
    "document reports credit risk on an exposure basis, not RWA, with no explicit 'Total RWA' line - the figure "
    "used here (£284,853k) is instead FY2016's own document's FY2015 comparative OV1 table (the earliest year an "
    "OV1-shaped RWA figure exists, same source as the RWA Breakdown sheet's FY2015 row). FY2015's own document's "
    "implied RWA from its Pillar 1 capital requirement (£21,828k / 8%) works out to ≈£272,850k - about £12k lower, "
    "presumably a methodology difference since the OV1 template wasn't in use yet in 2015."
)

LEVERAGE_NOTE = (
    "LEVERAGE CAVEAT: FY2021's own Pillar 3 report states a leverage ratio total exposure measure of £1,298,463k "
    "(ratio 12.90%). FY2022's report's FY2021 comparative instead shows £1,298,284k (ratio 12.83%) - a small "
    "(£179k / 0.07pp) discrepancy, plausibly a minor restatement or rounding difference rather than an error. "
    "FY2021's own originally-published figures are used here, per project convention. A larger version of the same "
    "pattern recurs at FY2017: FY2017's own document (narrative table and regulatory LRSum/LRCom appendix, "
    "internally consistent) states £1,024,505k / 7.39%, while FY2018's own document's FY2017 comparative column "
    "instead shows £923,402k / 8.20% - a ~£100m difference, not just rounding. FY2017's own originally-published "
    "figures are used here, same convention."
)

LCR_NOTE = (
    "LCR CAVEAT: the formal Pillar 3/KM1 template figures (used for FY2021-FY2024 below) are themselves labelled "
    "'Average of 12 months'. The FY2025 Annual Report's own narrative separately states the Bank's FY2024 LCR as "
    "521%, materially different from the FY2024 Pillar 3 KM1 table's 605% for the same year - two different "
    "figures for what should be the same average-basis metric, not reconciled anywhere in the source documents. "
    "The formal Pillar 3 KM1 figures are used throughout FY2021-FY2024 for internal consistency across this "
    "workbook series; FY2025 (no standalone Pillar 3 document published, and none will be - the Bank is an SDDT and is exempt from the Pillar 3 disclosure obligation, see ENTITY NOTE) falls back to the Annual Report's "
    "own narrative figure of 587%, on a basis that may not be directly comparable to the KM1 years - flagged. "
    "FY2018's own Pillar 3 document similarly shows two different LCR figures on the same page: a point-in-time "
    "'31/12/2018' ratio of 331%, and a separate 'Q4 2018' quarterly table (HQLA £334.6m / Net Cash Outflows "
    "£105.8m / LCR 321.1%). The Q4 quarterly-average table (321.1%) is used here for consistency with the "
    "KM1-style average-basis figures used in FY2019 onward. FY2015-FY2017 have no LCR table in either year's own "
    "Pillar 3 document (confirmed by checking each doc's Liquidity section) - genuinely undisclosed, not a gap."
)

CASH_FLOW_SOURCES = (
    "Sources - Cambridge & Counties Bank Limited's own Statement of Cash Flows (Bank-only basis, no subsidiaries):\n"
    f"FY2025: Annual Report 2025, p.58 (own year) - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.82 (own year); cross-checked against Annual Report 2025's FY2024 comparative "
    f"column, p.58 (exact match) - {AR2024_URL}\n"
    f"FY2023: Annual Report 2024, p.82 (FY2023 comparative column) - {AR2024_URL}\n"
    f"FY2022: Annual Report 2022 (accounts to 31 Dec 2022), p.86 (own year) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2022, p.86 (FY2021 comparative column) - {AR2022_URL}\n"
    f"FY2020: Companies House filing history (company 07972522), 'Full accounts made up to 31 December 2020', "
    f"filed 25 Jun 2021 (108 pages), 'Statement of Cash Flow' p.65 (own year) - {CH_FILING_HISTORY_URL}\n"
    f"FY2019: same FY2020 filing, p.65 (FY2019 comparative column) - {CH_FILING_HISTORY_URL}\n"
    f"FY2018: Companies House filing history (company 07972522), 'Full accounts made up to 31 December 2018', "
    f"filed 18 May 2019 (87 pages), 'Statement of Cash Flow' p.44 (own year) - {CH_FILING_HISTORY_URL}\n"
    f"FY2017: same FY2018 filing, p.44 (FY2017 comparative column) - {CH_FILING_HISTORY_URL}\n"
    f"FY2016: {CH2016_NOTE}, 'Statement of Cash Flow' p.29 (own year) - {CH_FILING_HISTORY_URL}\n"
    f"FY2015: same filing as FY2016, p.29 (FY2015 comparative column) - {CH_FILING_HISTORY_URL}\n"
    "LABEL NOTE: both the FY2024 and FY2025 Annual Reports mislabel the financing-activities subtotal row as "
    "'Net cash (used in) investing activities' (should read 'financing') - a recurring caption typo in the Bank's "
    "own template across at least two years; the figure is correctly placed under the Financing Activities section "
    "here regardless of the source's mislabelled caption.\n"
    "PRESENTATION NOTE: FY2021-FY2024 show two running subtotals within operating activities (adjustments-for "
    "subtotal, then a working-capital-changes subtotal) before the final operating total; FY2025's presentation "
    "drops both intermediate subtotals and lists all line items in one unbroken block - both years' totals "
    "reconcile exactly against their own line items either way; FY2025's missing subtotal cells are a genuine "
    "presentation change, not a gap. FY2015-FY2020 (all sourced pre-FY2021) present operating activities as a "
    "single unbroken block like FY2025, with no intermediate subtotals either - consistent with this being the "
    "Bank's older template, later expanded to two subtotals for FY2021-FY2024 and then simplified back for FY2025.\n"
    "DATA QUALITY NOTE: Annual Report 2024's own printed working-capital-changes subtotal for FY2024 reads "
    "£(21,140)k, but this does not match the sum of its own seven component line items, which total £(22,140)k - "
    "a £1,000k discrepancy. £(22,140)k is used here instead, since it is the figure that reconciles exactly to "
    "the report's own final 'Net cash generated from operating activities' total of £13,542k (£35,682k + "
    "£(22,140)k = £13,542k, matching exactly; £35,682k + £(21,140)k = £14,542k, which does not match the printed "
    "final total). The FY2023 comparative column in the same table is internally consistent and required no "
    "correction.\n"
    "DATA QUALITY NOTE (FY2016/FY2015): the FY2016 Companies House filing's own printed 'Net cash from investing "
    "activities' and 'Net cash from financing activities' subtotal rows (68,823 and 69,648 for FY2016; (68,200) "
    "and (60,435) for FY2015) do not sum from their own component line items and instead appear to duplicate "
    "cumulative running totals. The figures used here (FY2016: 13,774 investing / 825 financing; FY2015: 4,799 "
    "investing / 7,765 financing) are recomputed directly from the filing's own component lines and reconcile "
    "exactly to the filing's own (internally consistent) 'Net increase/(decrease) in cash and cash equivalents' "
    "totals (FY2016: 69,648; FY2015: (60,435)) and to the unbroken opening/closing cash chain running from "
    "FY2015 through FY2025.\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Cambridge & Counties Bank Limited Pillar 3 Disclosures (entity-level, no subsidiaries):\n"
        f"FY2025: Annual Report 2025 Strategic Report 'Capital'/'Loans and liquid assets' sections, p.22-23 (no "
        f"standalone Pillar 3 document published, and none will be - the Bank is an SDDT and is exempt from the Pillar 3 disclosure obligation, see ENTITY NOTE) - {AR2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures 2024, Table 1: Key metrics (own year, 31-Dec-24 column) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 2023, Table 1: Key metrics (own year, 31-Dec-23 column) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures 2022, Table 1: Key metrics, p.18 (own year, 31-Dec-22 column) - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures 2021, 'Own funds disclosure' table p.38 and 'Table LRCom' p.40 (own year, "
        f"2021 column) - {P3_2021_URL}\n"
        f"FY2020: Pillar 3 Disclosures 2020, 'Own funds disclosure' template and 'Overview of RWA (OV1)' (own "
        f"year, 2020 column) - {P3_2020_URL}\n"
        f"FY2019: Pillar 3 Disclosures 2019, 'Own funds disclosure' template and 'Overview of RWA (OV1)' (own "
        f"year, 2019 column) - {P3_2019_URL}\n"
        f"FY2018: Pillar 3 Disclosures 2018, p.32 'Own funds disclosure' template and p.36 'Overview of RWA "
        f"(OV1)' (own year, 2018 column) - {P3_2018_URL}\n"
        f"FY2017: Pillar 3 Disclosures 2017, own-year narrative capital/RWA figures and p.13 Leverage Ratio "
        f"table (own year); cross-checked against Pillar 3 Disclosures 2018's FY2017 comparative column, "
        f"p.32/p.36 (CET1/Tier1/Total Capital/RWA all match; Leverage Ratio table does not - see caveat) "
        f"- {P3_2017_URL}\n"
        f"FY2016: Pillar 3 Disclosures 2016, own-year narrative capital/RWA figures, 'Own Funds' table and "
        f"'Table LRCom' p.26 Leverage Ratio (own year); also carries FY2015 comparative for CET1/Tier1/Total "
        f"Capital/RWA ratios and amounts (cross-checked against Pillar 3 Disclosures 2015's own FY2015 figures "
        f"- exact match) - {P3_2016_URL}\n"
        f"FY2015: Pillar 3 Disclosures 2015, p.15 capital resources table (own year) and p.18 Leverage Ratio "
        f"'Q4 2015' table (own year, using the quarterly-average Tier 1 capital basis - see caveat) "
        f"- {P3_2015_URL}\n"
        + CET1_ERA_NOTE + "\n"
        + (extra + "\n" if extra else "")
    )


bw = BankWorkbook(bank_name="Cambridge & Counties Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="390062")

STATEMENTS_SOURCES = (
    "Sources - Cambridge & Counties Bank Limited's own Income Statement / Balance Sheet / Statement of Changes "
    "in Equity (Bank-only basis, no subsidiaries):\n"
    f"FY2025: Annual Report 2025, pp.55-57 (own year) - {AR2025_URL}\n"
    f"FY2024: Annual Report 2025, pp.55-57 (FY2024 comparative column); cross-checked against Annual Report "
    f"2024's own FY2024 figures, p.80-81 (exact match) - {AR2025_URL}\n"
    f"FY2023: Annual Report 2024, pp.80-81 (FY2023 comparative column) - {AR2024_URL}\n"
    f"FY2022: Annual Report 2022 (accounts to 31 Dec 2022), pp.85-86 (own year) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2022, pp.85-86 (FY2021 comparative column) - {AR2022_URL}\n"
    f"FY2020: Companies House filing history (company 07972522), 'Full accounts made up to 31 December 2020', "
    f"filed 25 Jun 2021 (108 pages), 'Statement of Profit or Loss and Other Comprehensive Income' p.62 and "
    f"'Statement of Financial Position' p.63 (own year) - {CH_FILING_HISTORY_URL}\n"
    f"FY2019: same FY2020 filing, p.62/p.63 (FY2019 comparative column) - {CH_FILING_HISTORY_URL}\n"
    f"FY2018: Companies House filing history (company 07972522), 'Full accounts made up to 31 December 2018', "
    f"filed 18 May 2019 (87 pages), 'Statement of Profit or Loss and Other Comprehensive Income' p.41 and "
    f"'Statement of Financial Position' p.42 (own year) - {CH_FILING_HISTORY_URL}\n"
    f"FY2017: same FY2018 filing, p.41/p.42 (FY2017 comparative column) - {CH_FILING_HISTORY_URL}\n"
    f"FY2016: {CH2016_NOTE}, 'Income Statement' p.26 and 'Statement of Financial Position' p.27 (own year) "
    f"- {CH_FILING_HISTORY_URL}\n"
    f"FY2015: same filing as FY2016, p.26/p.27 (FY2015 comparative column) - {CH_FILING_HISTORY_URL}\n"
    "Statement of Changes in Equity for FY2015-FY2020: same filings as above, p.28 (2016 filing) / p.43 (2018 "
    "filing) / p.64 (2020 filing) - each shows both its own year and the immediately preceding year in full, so "
    "every year FY2015-FY2020 is independently disclosed at least once, several cross-checked twice.\n"
    "EQUITY STRUCTURE NOTE: a 'Preference shares' column is carried on the Statement of Changes in Equity only "
    "for FY2015 (issued and then fully redeemed within that year, ending at nil) - the Bank held no preference "
    "shares before or after FY2015, so the column is blank in every other year. The 1 January 2018 restatement "
    "row reflects the £3,013k adjustment made on IFRS 9's first adoption (transition method applied means the "
    "FY2017 comparative itself is not restated - see the CET1 CAVEAT on the Pillar 3 metric sheets for the "
    "related IAS 39/IFRS 9 impairment-methodology shift).\n"
    "DEBT SECURITIES MEASUREMENT BASIS: Note 17 'Debt securities' (Annual Report 2025 p.35 own text, Annual "
    "Report 2024 p.30, Annual Report 2022 p.100-101) states in every year's own accounting policy wording that "
    "the Bank's debt securities 'are initially recognised at fair value and subsequently measured at fair value "
    "through other comprehensive income' - a Held to Collect and Sell business model, with no amortised-cost "
    "leg disclosed in any year. The 'Fair value through other comprehensive income reserve' equity line above "
    "carries a non-zero balance back to FY2015, corroborating the same FVOCI (or its pre-IFRS 9 IAS 39 "
    "available-for-sale equivalent) treatment for the full FY2015-FY2025 run. Note 17 also breaks the FY2021/"
    "FY2022 balance down by named instrument (European Investment Bank bond + International Bank for "
    "Reconstruction and Development bond, both supranational, not sovereign) - Annual Report 2022 p.100 - but "
    "no government/sovereign leg is disclosed in any year, so no issuer-type split is added.\n"
    + ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Cambridge & Counties Bank Limited's own Note 15 (Loans and advances to customers) and Note 16 "
    "(Allowance for impairment losses):\n"
    f"FY2025/FY2024: Annual Report 2025, p.66-67 - {AR2025_URL}\n"
    f"FY2023: Annual Report 2024, Note 16 (Allowance for impairment losses), p.47's 'Gross loan balances by "
    f"Stage 2023' table, 'Closing Balance at 31 December 2023' row - {AR2024_URL}\n"
    f"FY2022/FY2021: Annual Report 2022, pp.48-49 - {AR2022_URL}\n"
    f"FY2020/FY2019: Companies House filing history (company 07972522), 'Full accounts made up to 31 December "
    f"2020', filed 25 Jun 2021, Note 15 p.72 and Note 16 p.73 (IFRS 9 Stage 1/2/3 split, both years shown) "
    f"- {CH_FILING_HISTORY_URL}\n"
    f"FY2018/FY2017: Companies House filing history (company 07972522), 'Full accounts made up to 31 December "
    f"2018', filed 18 May 2019, Note 15/16 p.53 (IFRS 9 Stage 1/2/3 split for FY2018's own year; FY2017's own "
    f"comparative column is a single pre-IFRS9 allowance figure, no stage split) - {CH_FILING_HISTORY_URL}\n"
    f"FY2016/FY2015: {CH2016_NOTE}, Note 15 p.35 (single pre-IFRS9 allowance figure, no stage split for either "
    f"year) - {CH_FILING_HISTORY_URL}\n"
    "Gross/net loan figures per the Balance Sheet above; the loan loss provision is disclosed by full IFRS 9 "
    "stage (Stage 1/2/3) from FY2018 onward - shown as negative (a deduction from gross loans). FY2015-FY2017 "
    "predate the Bank's 1 January 2018 IFRS 9 adoption and disclose only a single collective/individual-"
    "assessment allowance total, with no stage breakdown - those years' Stage 1/2/3 cells are left blank rather "
    "than estimated, and only the Total loan loss provision row is populated for them. The loan loss provision "
    "credit/(charge) for the year is the P&L's own 'Impairment release/(losses) on loans and advances to "
    "customers' line throughout. FY2020/FY2019 gross loans and advances (£840,831k / £769,684k) are not printed "
    "directly as a combined figure in the FY2020 filing's Note 15 (which shows the two years' net receivables "
    "only) - they are derived as net loans plus the matching year's Note 16 total IFRS 9 provision (£828,380k + "
    "£12,451k; £761,503k + £8,181k respectively), both of which reconcile exactly against the Balance Sheet's own "
    "net figure. FY2016/FY2015's pre-IFRS9 provision splits into 'Individual provisions' and 'Collective "
    "provisions' sub-totals per the Bank's own Note 16 roll-forward table; FY2017's own comparative column in "
    "the FY2018 filing shows only the combined total (£3,584k), not the individual/collective split.\n"
    + ENTITY_NOTE
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Cambridge & Counties Bank Limited's own Pillar 3 Disclosures, 'Overview of RWA (OV1)' table:\n"
    f"FY2024: Pillar 3 Disclosures 2024 (own year, 31-Dec-24 column) - {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosures 2023 (own year, 31-Dec-23 column) - {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosures 2022, p.19 (own year, 31-Dec-22 column) - {P3_2022_URL}\n"
    f"FY2021: Pillar 3 Disclosures 2022, p.19 (31-Dec-21 comparative column) - {P3_2022_URL}\n"
    f"FY2020: Pillar 3 Disclosures 2020, 'Overview of RWA (OV1)' (own year, 2020 column) - {P3_2020_URL}\n"
    f"FY2019: Pillar 3 Disclosures 2019, 'Overview of RWA (OV1)' (own year, 2019 column) - {P3_2019_URL}\n"
    f"FY2018: Pillar 3 Disclosures 2018, p.36 'Overview of RWA (OV1)' (own year, 2018 column) - {P3_2018_URL}\n"
    f"FY2017: Pillar 3 Disclosures 2017, 'Overview of RWA (OV1)' (own year, 2017 column) - {P3_2017_URL}\n"
    f"FY2016: Pillar 3 Disclosures 2016, 'Overview of RWA (OV1)' (own year, 2016 column; also carries FY2015 "
    f"comparative) - {P3_2016_URL}\n"
    "FY2025: not publicly disclosed - no standalone Pillar 3 document has been published, and none will be - the Bank is an SDDT and is exempt from the Pillar 3 disclosure obligation, see ENTITY NOTE (same "
    "gap as the other Pillar 3 metric sheets this year).\n"
    "FY2015: the OV1 template was not yet in use in the Bank's own FY2015 Pillar 3 Disclosures (it reports "
    "credit risk on an exposure-value basis, not risk-weighted-asset basis, with no risk-category RWA "
    "breakdown) - FY2015's row below is instead the OV1-format figures from Pillar 3 Disclosures 2016's own "
    "FY2015 comparative column, the earliest year for which an OV1-shaped breakdown by risk category exists.\n"
    "COMPOSITION NOTE: whether the printed 'Total' row on the OV1 table equals the sum of the numbered risk-"
    "category rows above it, or that sum plus the memo 'Amounts below the thresholds for deduction' row, varies "
    "by year in the Bank's own published tables (FY2015-FY2017 exclude the thresholds row from the total; "
    "FY2018-FY2024 include it) - each year's Total row below is transcribed exactly as printed in its own "
    "source document regardless of which composition it reflects.\n"
    "Table 2 in the 2023/2024 Pillar 3 Disclosures is a .docx-embedded image (not text/a real table) - extracted "
    "by rendering the embedded image. All years' Total row ties exactly to the Total RWAs sheet's own figure "
    "for that year, except FY2017 (561,630 here vs 561,633 on the Total RWAs sheet - a £3k difference between "
    "two tables in the same underlying disclosure family; both are transcribed as printed, see the Total RWAs "
    "sheet's own note) and FY2019 (619,342 here, the OV1 table's own printed total, vs 619,343 on the Total RWAs "
    "sheet, from the Own Funds template's 'Total risk weighted assets' line - the same £1-3k intra-document "
    "rounding pattern as FY2017, both transcribed exactly as printed in their own source table).\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 282554, "FY2024": 292850, "FY2023": 302473, "FY2022": 286680, "FY2021": 240158, "FY2020": 190962, "FY2019": 228972, "FY2018": 232286, "FY2017": 164295, "FY2016": 127905, "FY2015": 62121}),
    ("DATA", "Loans and advances to banks", {"FY2025": 11034, "FY2024": 12139, "FY2023": 10420, "FY2022": 13931, "FY2021": 12293, "FY2020": 9687, "FY2019": 7695, "FY2018": 14384, "FY2017": 20091, "FY2016": 14754, "FY2015": 10740}),
    ("DATA", "Debt securities (fair value through other comprehensive income)", {"FY2025": 151065, "FY2024": 65137, "FY2023": 47409, "FY2022": 30412, "FY2021": 37137, "FY2020": 38044, "FY2019": 0, "FY2018": 13350, "FY2017": 3107, "FY2016": 13249, "FY2015": 27229}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1446075, "FY2024": 1204444, "FY2023": 1083278, "FY2022": 1037710, "FY2021": 977834, "FY2020": 828380, "FY2019": 761503, "FY2018": 769016, "FY2017": 689954, "FY2016": 588352, "FY2015": 416263}),
    ("DATA", "Derivative financial assets", {"FY2025": 0, "FY2024": 149, "FY2023": 0, "FY2020": 9, "FY2019": 0, "FY2016": 0, "FY2015": 15}),
    ("DATA", "Other assets and prepayments", {"FY2025": 1534, "FY2024": 1443, "FY2023": 2526, "FY2022": 2573, "FY2021": 2091, "FY2020": 1431, "FY2019": 1224, "FY2018": 940, "FY2017": 868, "FY2016": 449, "FY2015": 365}),
    ("DATA", "Property, plant and equipment", {"FY2025": 1398, "FY2024": 1700, "FY2023": 2026, "FY2022": 2366, "FY2021": 2587, "FY2020": 2934, "FY2019": 3154, "FY2018": 386, "FY2017": 144, "FY2016": 329, "FY2015": 274}),
    ("DATA", "Intangible assets", {"FY2025": 3089, "FY2024": 2277, "FY2023": 1869, "FY2022": 1774, "FY2021": 1589, "FY2020": 1567, "FY2019": 791, "FY2018": 846, "FY2017": 520, "FY2016": 509, "FY2015": 681}),
    ("DATA", "Current tax asset", {"FY2025": 1276, "FY2024": 689, "FY2023": 0, "FY2022": 0, "FY2021": 407, "FY2020": 522, "FY2019": 0}),
    ("DATA", "Deferred tax asset", {"FY2025": 608, "FY2024": 907, "FY2023": 721, "FY2022": 1099, "FY2021": 775, "FY2020": 725, "FY2019": 729, "FY2018": 880, "FY2017": 253, "FY2016": 220, "FY2015": 261}),
    ("TOTAL", "Total assets", {"FY2025": 1898633, "FY2024": 1581735, "FY2023": 1450722, "FY2022": 1376545, "FY2021": 1274871, "FY2020": 1074261, "FY2019": 1004068, "FY2018": 1032088, "FY2017": 879232, "FY2016": 745767, "FY2015": 517949}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customers' accounts", {"FY2025": 1633601, "FY2024": 1271824, "FY2023": 1155224, "FY2022": 1103256, "FY2021": 1025520, "FY2020": 917215, "FY2019": 854449, "FY2018": 901398, "FY2017": 798176, "FY2016": 684672, "FY2015": 471564}),
    ("DATA", "Central Bank facilities", {"FY2025": 0, "FY2024": 55000, "FY2023": 65000, "FY2022": 78000, "FY2021": 78000}),
    ("DATA", "Subordinated debt liability", {"FY2025": 4840, "FY2024": 4800, "FY2023": 4751, "FY2016": 0, "FY2015": 2086}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 3087, "FY2024": 0, "FY2023": 652, "FY2022": 1010, "FY2021": 254, "FY2020": 0, "FY2019": 31, "FY2018": 94, "FY2017": 121, "FY2016": 183, "FY2015": 29}),
    ("DATA", "Provisions", {"FY2025": 0, "FY2024": 750, "FY2018": 8, "FY2017": 134}),
    ("DATA", "Other liabilities and accruals", {"FY2025": 8462, "FY2024": 9277, "FY2023": 9628, "FY2022": 9107, "FY2021": 7280, "FY2020": 6911, "FY2019": 5840, "FY2018": 2710, "FY2017": 2194, "FY2016": 3668, "FY2015": 2982}),
    ("DATA", "Current tax liability", {"FY2025": 0, "FY2024": 0, "FY2023": 689, "FY2022": 326, "FY2021": 0, "FY2020": 0, "FY2019": 1595, "FY2018": 2698, "FY2017": 2364}),
    ("TOTAL", "Total liabilities", {"FY2025": 1649990, "FY2024": 1341651, "FY2023": 1235944, "FY2022": 1191699, "FY2021": 1111054, "FY2020": 924126, "FY2019": 861915, "FY2018": 906908, "FY2017": 802989, "FY2016": 688523, "FY2015": 476661}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 44955, "FY2024": 44955, "FY2023": 44955, "FY2022": 44955, "FY2021": 44955, "FY2020": 44955, "FY2019": 44955, "FY2018": 44955, "FY2017": 23955, "FY2016": 23955, "FY2015": 22955}),
    ("DATA", "Contingent convertible loan notes", {"FY2025": 22900, "FY2024": 22900, "FY2023": 22900, "FY2022": 22900, "FY2021": 22900, "FY2020": 22900, "FY2019": 22900, "FY2018": 22900, "FY2017": 12900, "FY2016": 12900, "FY2015": 11900}),
    ("DATA", "Fair value through other comprehensive income reserve", {"FY2025": 77, "FY2024": -274, "FY2023": -376, "FY2022": -1209, "FY2021": -475, "FY2020": 26, "FY2019": 2, "FY2018": 73, "FY2017": 36, "FY2016": 106, "FY2015": 11}),
    ("DATA", "Retained earnings", {"FY2025": 180711, "FY2024": 172503, "FY2023": 147299, "FY2022": 118200, "FY2021": 96437, "FY2020": 82254, "FY2019": 74296, "FY2018": 57252, "FY2017": 39352, "FY2016": 20283, "FY2015": 6422}),
    ("TOTAL", "Total equity", {"FY2025": 248643, "FY2024": 240084, "FY2023": 214778, "FY2022": 184846, "FY2021": 163817, "FY2020": 150135, "FY2019": 142153, "FY2018": 125180, "FY2017": 76243, "FY2016": 57244, "FY2015": 41288}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 1898633, "FY2024": 1581735, "FY2023": 1450722, "FY2022": 1376545, "FY2021": 1274871, "FY2020": 1074261, "FY2019": 1004068, "FY2018": 1032088, "FY2017": 879232, "FY2016": 745767, "FY2015": 517949}),
]

bw.add_balance_sheet_sheet(
    title="Cambridge & Counties Bank Limited — Balance Sheet",
    subtitle="Bank-only basis (no subsidiaries), £'000. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income calculated using the effective interest rate", {"FY2025": 130181, "FY2024": 128313, "FY2023": 116023, "FY2022": 75977, "FY2021": 55335, "FY2020": 50897, "FY2019": 57045, "FY2018": 57514, "FY2017": 48198, "FY2016": 35261, "FY2015": 24253}),
    ("DATA", "Interest expense", {"FY2025": -59341, "FY2024": -54838, "FY2023": -40172, "FY2022": -16753, "FY2021": -10408, "FY2020": -12785, "FY2019": -14137, "FY2018": -13089, "FY2017": -9767, "FY2016": -8579, "FY2015": -6727}),
    ("TOTAL", "Net interest income", {"FY2025": 70840, "FY2024": 73475, "FY2023": 75851, "FY2022": 59224, "FY2021": 44927, "FY2020": 38112, "FY2019": 42908, "FY2018": 44425, "FY2017": 38431, "FY2016": 26682, "FY2015": 17526}),
    ("DATA", "Other income", {"FY2025": 376, "FY2024": 126, "FY2023": 553, "FY2022": 28, "FY2021": 23, "FY2020": 30, "FY2019": 50, "FY2018": 310, "FY2017": 528, "FY2016": 1997, "FY2015": 1016}),
    ("TOTAL", "Total operating income", {"FY2025": 71216, "FY2024": 73601, "FY2023": 76404, "FY2022": 59252, "FY2021": 44950, "FY2020": 38142, "FY2019": 42958, "FY2018": 44735, "FY2017": 38959, "FY2016": 28679, "FY2015": 18542}),
    ("SECTION", "Expenses", {}),
    ("TOTAL", "Administrative expenses", {"FY2025": -32390, "FY2024": -31772, "FY2023": -27287, "FY2022": -25034, "FY2021": -21965, "FY2020": -20236, "FY2019": -17763, "FY2018": -14584, "FY2017": -11826, "FY2016": -8873, "FY2015": -7668}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -1122, "FY2024": -1077, "FY2023": -944, "FY2022": -906, "FY2021": -971, "FY2020": -932, "FY2019": -1093, "FY2018": -509, "FY2017": -490, "FY2016": -326, "FY2015": -264}),
    ("TOTAL", "Operating profit before impairment losses", {"FY2025": 37704, "FY2024": 40752, "FY2023": 48173, "FY2022": 33312, "FY2021": 22014, "FY2020": 16974, "FY2019": 24102, "FY2018": 29642, "FY2017": 26643, "FY2016": 19480, "FY2015": 10610}),
    ("DATA", "Impairment release/(losses) on loans and advances to customers", {"FY2025": 1967, "FY2024": -4932, "FY2023": -7263, "FY2022": -4773, "FY2021": -3524, "FY2020": -5813, "FY2019": -1566, "FY2018": -1716, "FY2017": -2237, "FY2016": -1361, "FY2015": -439}),
    ("TOTAL", "Profit before tax", {"FY2025": 39671, "FY2024": 35820, "FY2023": 40910, "FY2022": 28539, "FY2021": 18490, "FY2020": 11161, "FY2019": 22536, "FY2018": 27926, "FY2017": 24406, "FY2016": 18119, "FY2015": 10171}),
    ("DATA", "Taxation charge", {"FY2025": -9179, "FY2024": -8157, "FY2023": -9620, "FY2022": -5337, "FY2021": -3024, "FY2020": -1763, "FY2019": -4035, "FY2018": -5518, "FY2017": -4712, "FY2016": -3434, "FY2015": -2085}),
    ("TOTAL", "Profit after tax", {"FY2025": 30492, "FY2024": 27663, "FY2023": 31290, "FY2022": 23202, "FY2021": 15466, "FY2020": 9398, "FY2019": 18501, "FY2018": 22408, "FY2017": 19694, "FY2016": 14685, "FY2015": 8086}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Fair value movements taken to reserves", {"FY2025": 455, "FY2024": 150, "FY2023": 1111, "FY2022": -1233, "FY2021": -411, "FY2020": 29, "FY2019": -86, "FY2018": 48, "FY2017": -75, "FY2016": 94, "FY2015": -29}),
    ("DATA", "Taxation", {"FY2025": -104, "FY2024": -48, "FY2023": -278, "FY2022": 499, "FY2021": -90, "FY2020": -5, "FY2019": 15, "FY2018": -11, "FY2017": 5, "FY2016": 1, "FY2015": 1}),
    ("TOTAL", "Total other comprehensive income/(expense), net of tax", {"FY2025": 351, "FY2024": 102, "FY2023": 833, "FY2022": -734, "FY2021": -501, "FY2020": 24, "FY2019": -71, "FY2018": 37, "FY2017": -70, "FY2016": 95, "FY2015": -28}),
    ("TOTAL", "Total comprehensive income attributable to owners of the Bank", {"FY2025": 30843, "FY2024": 27765, "FY2023": 32123, "FY2022": 22468, "FY2021": 14965, "FY2020": 9422, "FY2019": 18430, "FY2018": 22445, "FY2017": 19624, "FY2016": 14780, "FY2015": 8058}),
]

bw.add_income_statement_sheet(
    title="Cambridge & Counties Bank Limited — Profit & Loss",
    subtitle="Bank-only basis (no subsidiaries), £'000. All profit for the year arises from continuing "
              "operations. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Contingent convertible loan notes", "Preference shares", "FVOCI reserve", "Retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "At 1 January 2015", (18455, None, 7500, 39, -1040, 24954)),
    ("DATA", "Profit for the year", (None, None, None, None, 8086, 8086)),
    ("DATA", "Other comprehensive expense", (None, None, None, -28, None, -28)),
    ("DATA", "Total comprehensive income for the period (FY2015)", (None, None, None, -28, 8086, 8058)),
    ("DATA", "Issue of shares", (4500, 11900, 4400, None, None, 20800)),
    ("DATA", "Redemption of shares", (None, None, -11900, None, None, -11900)),
    ("DATA", "Convertible loan note interest", (None, None, None, None, -165, -165)),
    ("DATA", "Dividends", (None, None, None, None, -459, -459)),
    ("TOTAL", "At 31 December 2015", (22955, 11900, 0, 11, 6422, 41288)),
    ("DATA", "Profit for the year", (None, None, None, None, 14685, 14685)),
    ("DATA", "Other comprehensive income", (None, None, None, 95, None, 95)),
    ("DATA", "Total comprehensive income for the period (FY2016)", (None, None, None, 95, 14685, 14780)),
    ("DATA", "Issue of shares", (1000, 1000, None, None, None, 2000)),
    ("DATA", "Convertible loan note interest", (None, None, None, None, -824, -824)),
    ("TOTAL", "At 31 December 2016", (23955, 12900, 0, 106, 20283, 57244)),
    ("DATA", "Profit for the year", (None, None, None, None, 19694, 19694)),
    ("DATA", "Other comprehensive expense", (None, None, None, -70, None, -70)),
    ("DATA", "Total comprehensive income for the period (FY2017)", (None, None, None, -70, 19694, 19624)),
    ("DATA", "Convertible loan note interest", (None, None, None, None, -625, -625)),
    ("TOTAL", "At 31 December 2017", (23955, 12900, 0, 36, 39352, 76243)),
    ("TOTAL", "At 1 January 2018 (as restated for IFRS 9 transition)", (23955, 12900, None, 36, 36339, 73230)),
    ("DATA", "Profit for the year", (None, None, None, None, 22408, 22408)),
    ("DATA", "Other comprehensive income", (None, None, None, 37, None, 37)),
    ("DATA", "Total comprehensive income for the period (FY2018)", (None, None, None, 37, 22408, 22445)),
    ("DATA", "Dividends paid on ordinary shares", (None, None, None, None, -1000, -1000)),
    ("DATA", "Issue of shares", (21000, 10000, None, None, None, 31000)),
    ("DATA", "Convertible loan note interest (net of tax)", (None, None, None, None, -495, -495)),
    ("TOTAL", "At 31 December 2018", (44955, 22900, 0, 73, 57252, 125180)),
    ("DATA", "Profit for the year", (None, None, None, None, 18501, 18501)),
    ("DATA", "Other comprehensive expense", (None, None, None, -71, None, -71)),
    ("DATA", "Total comprehensive income for the period (FY2019)", (None, None, None, -71, 18501, 18430)),
    ("DATA", "Convertible loan note interest (net of tax)", (None, None, None, None, -1457, -1457)),
    ("TOTAL", "At 31 December 2019", (44955, 22900, 0, 2, 74296, 142153)),
    ("DATA", "Profit for the year", (None, None, None, None, 9398, 9398)),
    ("DATA", "Other comprehensive income", (None, None, None, 24, None, 24)),
    ("DATA", "Total comprehensive income for the period (FY2020)", (None, None, None, 24, 9398, 9422)),
    ("DATA", "Convertible loan note interest", (None, None, None, None, -1440, -1440)),
    ("TOTAL", "At 31 December 2020", (44955, 22900, 0, 26, 82254, 150135)),
    ("DATA", "Profit for the year", (None, None, None, None, 15466, 15466)),
    ("DATA", "Other comprehensive expense", (None, None, None, -501, None, -501)),
    ("DATA", "Total comprehensive income for the period (FY2021)", (None, None, None, -501, 15466, 14965)),
    ("DATA", "Convertible loan note interest", (None, None, None, None, -1283, -1283)),
    ("TOTAL", "At 31 December 2021", (44955, 22900, None, -475, 96437, 163817)),
    ("DATA", "Total comprehensive income for the period (FY2022)", (None, None, None, -734, 23202, 22468)),
    ("DATA", "Convertible loan note interest", (None, None, None, None, -1439, -1439)),
    ("TOTAL", "At 31 December 2022", (44955, 22900, None, -1209, 118200, 184846)),
    ("DATA", "Total comprehensive income for the period (FY2023)", (None, None, None, 833, 31290, 32123)),
    ("DATA", "Convertible loan note interest", (None, None, None, None, -2191, -2191)),
    ("TOTAL", "At 31 December 2023", (44955, 22900, None, -376, 147299, 214778)),
    ("DATA", "Total comprehensive income for the period (FY2024)", (None, None, None, 102, 27663, 27765)),
    ("DATA", "Convertible loan note interest", (None, None, None, None, -2459, -2459)),
    ("TOTAL", "At 31 December 2024", (44955, 22900, None, -274, 172503, 240084)),
    ("DATA", "Total comprehensive income for the period (FY2025)", (None, None, None, 351, 30492, 30843)),
    ("DATA", "Dividend paid", (None, None, None, None, -20000, -20000)),
    ("DATA", "Convertible loan note interest", (None, None, None, None, -2284, -2284)),
    ("TOTAL", "At 31 December 2025", (44955, 22900, None, 77, 180711, 248643)),
]

bw.add_equity_changes_sheet(
    title="Cambridge & Counties Bank Limited — Statement of Changes in Equity",
    subtitle="Bank-only basis (no subsidiaries), £'000, chronological (oldest to newest). All totals reconcile "
              "exactly, no plug rows needed (real audited data). See source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit after tax", {"FY2025": 30492, "FY2024": 27663, "FY2023": 31290, "FY2022": 23202, "FY2021": 15466, "FY2020": 9398, "FY2019": 18501, "FY2018": 22408, "FY2017": 19694}),
    ("DATA", "Profit before tax (FY2015-FY2016 cash flow presentation starts from PBT, not PAT)", {"FY2016": 18119, "FY2015": 10171}),
    ("DATA", "Subordinated debt liability interest and fee accrual", {"FY2025": 40, "FY2024": 196, "FY2023": 147}),
    ("DATA", "Non-cash item on adoption of IFRS 16", {"FY2020": -193, "FY2019": -2429}),
    ("DATA", "Depreciation, amortisation and (loss)/gain on disposals", {"FY2025": 1122, "FY2024": 1077, "FY2023": 944, "FY2022": 906, "FY2021": 971, "FY2020": 932, "FY2019": 1093, "FY2018": 509, "FY2017": 490, "FY2016": 326, "FY2015": 264}),
    ("DATA", "(Decrease)/increase in allowance for impairment losses", {"FY2025": -9644, "FY2024": -1654, "FY2023": 5849}),
    ("DATA", "Taxation charge", {"FY2025": 9179, "FY2024": 8157, "FY2023": 9620, "FY2022": 5337, "FY2021": 3024, "FY2020": 1763, "FY2019": 4035, "FY2018": 5518, "FY2017": 4712}),
    ("DATA", "Other non-cash items", {"FY2025": 597, "FY2024": 243, "FY2023": -112}),
    ("TOTAL", "Cash flows from operating activities before changes in working capital", {"FY2024": 35682, "FY2023": 47738, "FY2022": 29445, "FY2021": 19461, "FY2020": 11900, "FY2019": 21200, "FY2018": 28435, "FY2017": 24896, "FY2016": 18445, "FY2015": 10435}),
    ("SECTION", "Net increase/(decrease) in other assets/liabilities", {}),
    ("DATA", "Net (increase)/decrease in loans and advances to customers", {"FY2025": -228708, "FY2024": -119661, "FY2023": -51418, "FY2022": -59876, "FY2021": -149454, "FY2020": -66877, "FY2019": 7513, "FY2018": -82692, "FY2017": -101602, "FY2016": -173450, "FY2015": -166039}),
    ("DATA", "Net increase/(decrease) in customers' accounts", {"FY2025": 361462, "FY2024": 116329, "FY2023": 51968, "FY2022": 77736, "FY2021": 108305, "FY2020": 62766, "FY2019": -46949, "FY2018": 103222, "FY2017": 113504, "FY2016": 213108, "FY2015": 83365}),
    ("DATA", "Net (decrease)/increase in central bank facilities", {"FY2025": -55000, "FY2024": -10000, "FY2023": -13000, "FY2022": 0, "FY2021": 78000}),
    ("DATA", "Net (increase)/decrease in derivatives", {"FY2025": -57, "FY2024": -475, "FY2023": -358, "FY2022": 756, "FY2021": 262, "FY2020": -40, "FY2019": -63, "FY2018": -27, "FY2017": -62, "FY2016": -169, "FY2015": 32}),
    ("DATA", "Net (decrease)/increase in value of debt securities", {"FY2022": 336, "FY2021": 591, "FY2020": 518, "FY2019": -86, "FY2018": 6, "FY2017": 66, "FY2016": -162, "FY2015": 80}),
    ("DATA", "Net (decrease)/increase in other liabilities and provisions", {"FY2025": -1565, "FY2024": 399, "FY2023": 520, "FY2022": 1827, "FY2021": 371, "FY2020": 1071, "FY2019": 3122, "FY2018": 585, "FY2017": 222, "FY2016": 63, "FY2015": 610}),
    ("DATA", "Net (increase)/decrease in other assets and prepayments", {"FY2025": -91, "FY2024": 1083, "FY2023": 46, "FY2022": -482, "FY2021": -661, "FY2020": -207, "FY2019": -285, "FY2018": -72, "FY2017": -419, "FY2016": -84, "FY2015": 54}),
    ("DATA", "Accrued interest on cash balances", {"FY2016": 14, "FY2015": 21}),
    ("DATA", "Income tax paid", {"FY2025": -9572, "FY2024": -9815, "FY2023": -9154, "FY2022": -4428, "FY2021": -3050, "FY2020": -3881, "FY2019": -4972, "FY2018": -5102, "FY2017": -3788, "FY2016": -2716, "FY2015": -1557}),
    ("TOTAL", "Net increase/(decrease) in operating assets and liabilities", {"FY2024": -22140, "FY2023": -21396, "FY2022": 15869, "FY2021": 34364, "FY2020": -6650, "FY2019": -41720, "FY2018": 15920, "FY2017": 7921, "FY2016": 36604, "FY2015": -83434}),
    ("TOTAL", "Net cash generated from operating activities", {"FY2025": 98255, "FY2024": 13542, "FY2023": 26342, "FY2022": 45314, "FY2021": 53825, "FY2020": 5250, "FY2019": -20520, "FY2018": 44355, "FY2017": 32817, "FY2016": 55049, "FY2015": -72999}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Proceeds from debt securities sales/maturity", {"FY2025": 21594, "FY2024": 6609, "FY2023": 20000, "FY2022": 10000, "FY2021": 7000, "FY2019": 23244, "FY2017": 10000, "FY2016": 17097, "FY2015": 5198}),
    ("DATA", "Acquisition of debt securities", {"FY2025": -107335, "FY2024": -24437, "FY2023": -35774, "FY2022": -4845, "FY2021": -7094, "FY2020": -38533, "FY2019": -9894, "FY2018": -10199, "FY2016": -3106}),
    ("DATA", "Acquisition of property, plant & equipment and intangible assets", {"FY2025": -1631, "FY2024": -1159, "FY2023": -700, "FY2022": -870, "FY2021": -646, "FY2020": -1295, "FY2019": -1376, "FY2018": -1077, "FY2017": -315, "FY2016": -217, "FY2015": -399}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {"FY2025": -87372, "FY2024": -18987, "FY2023": -16474, "FY2022": 4285, "FY2021": -740, "FY2020": -39828, "FY2019": 11974, "FY2018": -11276, "FY2017": 9685, "FY2016": 13774, "FY2015": 4799}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividend paid", {"FY2025": -20000, "FY2018": -1000, "FY2016": -390, "FY2015": -1135}),
    ("DATA", "Issue of subordinated debt liability", {"FY2024": 0, "FY2023": 4604}),
    ("DATA", "Proceeds from the issue of share capital", {"FY2018": 21000, "FY2016": 2000, "FY2015": 8900}),
    ("DATA", "Proceeds from the issue of contingent convertible loan notes", {"FY2018": 10000}),
    ("DATA", "Convertible loan note interest paid", {"FY2025": -2284, "FY2024": -2459, "FY2023": -2191, "FY2022": -1439, "FY2021": -1283, "FY2020": -1440, "FY2019": -1457, "FY2018": -795, "FY2017": -775, "FY2016": -785}),
    ("TOTAL", "Net cash (used in)/generated from financing activities", {"FY2025": -22284, "FY2024": -2459, "FY2023": 2413, "FY2022": -1439, "FY2021": -1283, "FY2020": -1440, "FY2019": -1457, "FY2018": 29205, "FY2017": -775, "FY2016": 825, "FY2015": 7765}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -11401, "FY2024": -7904, "FY2023": 12282, "FY2022": 48160, "FY2021": 51802, "FY2020": -36018, "FY2019": -10003, "FY2018": 62284, "FY2017": 41727, "FY2016": 69648, "FY2015": -60435}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 304989, "FY2024": 312893, "FY2023": 300611, "FY2022": 252451, "FY2021": 200649, "FY2020": 236667, "FY2019": 246670, "FY2018": 184386, "FY2017": 142659, "FY2016": 73011, "FY2015": 133446}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 293588, "FY2024": 304989, "FY2023": 312893, "FY2022": 300611, "FY2021": 252451, "FY2020": 200649, "FY2019": 236667, "FY2018": 246670, "FY2017": 184386, "FY2016": 142659, "FY2015": 73011}),
]

bw.add_cash_flow_sheet(
    title="Cambridge & Counties Bank Limited — Statement of Cash Flows",
    subtitle="Bank-only basis (no subsidiaries), £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loan book", {}),
    ("DATA", "Gross loans and advances", {"FY2025": 1454424, "FY2024": 1225716, "FY2023": 1106055, "FY2022": 1054638, "FY2021": 992600, "FY2020": 840831, "FY2019": 769684, "FY2018": 777084, "FY2017": 693538, "FY2016": 590860, "FY2015": 417410}),
    ("DATA", "Loans and advances to customers, net", {"FY2025": 1446075, "FY2024": 1204444, "FY2023": 1083278, "FY2022": 1037710, "FY2021": 977834, "FY2020": 828380, "FY2019": 761503, "FY2018": 769016, "FY2017": 689954, "FY2016": 588352, "FY2015": 416263}),
    ("SECTION", "Loan loss provision, by IFRS 9 stage (FY2018-FY2025; IFRS 9 adopted 1 Jan 2018)", {}),
    ("DATA", "Stage 1: subject to 12-month ECL", {"FY2025": -3559, "FY2024": -2645, "FY2023": -3288, "FY2022": -3082, "FY2021": -2836, "FY2020": -3332, "FY2019": -3423, "FY2018": -2326}),
    ("DATA", "Stage 2: subject to lifetime ECL", {"FY2025": -3366, "FY2024": -8208, "FY2023": -8907, "FY2022": -8283, "FY2021": -5954, "FY2020": -4867, "FY2019": -1303, "FY2018": -2171}),
    ("DATA", "Stage 3: subject to lifetime ECL", {"FY2025": -4554, "FY2024": -10270, "FY2023": -10582, "FY2022": -5563, "FY2021": -5976, "FY2020": -4252, "FY2019": -3455, "FY2018": -3571}),
    ("TOTAL", "Total loan loss provision (IFRS 9 basis, FY2018-FY2025)", {"FY2025": -11479, "FY2024": -21123, "FY2023": -22777, "FY2022": -16928, "FY2021": -14766, "FY2020": -12451, "FY2019": -8181, "FY2018": -8068}),
    ("SECTION", "Loan loss provision, pre-IFRS 9 (FY2015-FY2017, single collective/individual total)", {}),
    ("DATA", "Individual provisions", {"FY2016": -1016, "FY2015": -100}),
    ("DATA", "Collective provisions", {"FY2016": -1492, "FY2015": -1047}),
    ("TOTAL", "Total loan loss provision (pre-IFRS 9 basis)", {"FY2017": -3584, "FY2016": -2508, "FY2015": -1147}),
    ("DATA", "Loan loss provision credit/(charge) for the year", {"FY2025": 1967, "FY2024": -4932, "FY2023": -7263, "FY2022": -4773, "FY2021": -3524, "FY2020": -5813, "FY2019": -1566, "FY2018": -1716, "FY2017": -2237, "FY2016": -1361, "FY2015": -439}),
]

bw.add_asset_quality_sheet(
    title="Cambridge & Counties Bank Limited — Asset Quality",
    subtitle="Bank-only basis (no subsidiaries), £'000. Full IFRS 9 stage split disclosed every year from "
              "FY2018 (adoption date) onward, including FY2023's gross loan figure (found on a follow-up pass; "
              "ties exactly to net + provision); FY2015-FY2017 predate IFRS 9 and disclose a single "
              "individual/collective provision total instead (see Note 16 CAVEAT below). See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=88,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=180)


CET1_CAPITAL = {"FY2025": 218496, "FY2024": 213247, "FY2023": 190817, "FY2022": 163071, "FY2021": 144655, "FY2020": 130263, "FY2019": 119471, "FY2018": 104339, "FY2017": 62823, "FY2016": 43835, "FY2015": 28707}
TIER1_CAPITAL = {"FY2025": 242394, "FY2024": 236147, "FY2023": 213717, "FY2022": 185972, "FY2021": 167555, "FY2020": 153163, "FY2019": 142371, "FY2018": 127239, "FY2017": 75723, "FY2016": 56735, "FY2015": 40607}
TOTAL_CAPITAL = {"FY2025": 246946, "FY2024": 241147, "FY2023": 218717, "FY2022": 185972, "FY2021": 167555, "FY2020": 153163, "FY2019": 142371, "FY2018": 127239, "FY2017": 77518, "FY2016": 58227, "FY2015": 42054}
TOTAL_RWA = {"FY2025": 1138000, "FY2024": 980319, "FY2023": 841556, "FY2022": 787621, "FY2021": 728379, "FY2020": 629727, "FY2019": 619343, "FY2018": 621368, "FY2017": 561633, "FY2016": 428605, "FY2015": 284853}

CET1_RATIO = {"FY2025": "19.2%", "FY2024": "21.75%", "FY2023": "22.67%", "FY2022": "20.70%", "FY2021": "19.86%", "FY2020": "20.69%", "FY2019": "19.29%", "FY2018": "16.79%", "FY2017": "11.19%", "FY2016": "10.60%", "FY2015": "10.5%"}
TIER1_RATIO = {"FY2025": "21.3%", "FY2024": "24.09%", "FY2023": "25.40%", "FY2022": "23.61%", "FY2021": "23.00%", "FY2020": "24.32%", "FY2019": "22.99%", "FY2018": "20.48%", "FY2017": "13.48%", "FY2016": "13.72%", "FY2015": "14.8%"}
TOTAL_CAPITAL_RATIO = {"FY2025": "21.7%", "FY2024": "24.60%", "FY2023": "25.99%", "FY2022": "23.61%", "FY2021": "23.00%", "FY2020": "24.32%", "FY2019": "22.99%", "FY2018": "20.48%", "FY2017": "13.80%", "FY2016": "14.08%", "FY2015": "15.4%"}

CALC_NOTE_2025 = (
    "FY2025: no standalone Pillar 3 document has been published, and none will be - the Bank is an SDDT and is exempt from the Pillar 3 disclosure obligation, see ENTITY NOTE - CALCULATED from the Annual Report 2025's own "
    "disclosed RWA (£1,138m) and ratio (see Overview/Strategic Report), not directly disclosed as a £ figure "
    "anywhere in the source. FY2021-FY2024 are directly disclosed, not calculated."
)

KM1_YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]

KM1_SOURCES = (
    "Sources - Cambridge & Counties Bank Limited Pillar 3 Disclosures, 'Table 1: Key metrics' (the UK KM1 "
    "template), Bank-only basis, GBP'000. Each year is transcribed from the edition in which it is the "
    "REPORTING year, never from a later edition's comparative column (map rule 1):\n"
    f"FY2024: Pillar 3 Disclosures 2024, 'Table 1: Key metrics' (31-Dec-24 column) - {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosures 2023, 'Table 1: Key metrics' (31-Dec-23 column) - {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosures 2022, 'Table 1: Key metrics', p.18 (31-Dec-22 column) - {P3_2022_URL}\n\n"
    "THE TABLE IS A BITMAP, NOT TEXT - transcribed visually and twice (map rule 13). None of these tables "
    "extracts as text, and neither the PDF nor the .docx gives any sign of that: the FY2022 PDF is otherwise "
    "fully text-native, and the FY2023/FY2024 documents are .docx files containing ZERO w:tbl elements - not a "
    "single Word table in either - with every table pasted as a picture (10 embedded images in the FY2024 file, "
    "carrying Word's own auto-generated alt-text 'A screenshot of a spreadsheet'). A text-extraction pass over "
    "these documents returns the 'Key metrics' heading and the paragraph beneath it and nothing in between, "
    "which reads exactly like a bank that publishes only a short narrative. It is not. FY2022 was read from two "
    "independent renderings - the page rendered at 150dpi with pdftoppm, and the embedded JPEG extracted at "
    "native resolution with pdfimages - and the two agree digit for digit across all 23 rows and both columns. "
    "FY2023 and FY2024 were read from the native PNGs and cross-checked against the adjacent edition's "
    "comparative column, which agrees on every row except the two source defects recorded below.\n\n"
    "LEVERAGE ROWS KEEP THE BANK'S OWN PRE-2022 CAPTIONS (map rule 5). All three editions print row 13 as "
    "'Leverage ratio total exposure measure' and row 14 as 'Leverage ratio', without the 'excluding claims on "
    "central banks' qualifier that the post-1-January-2022 template uses. The captions are reproduced as "
    "printed and are NOT silently relabelled to the newer wording.\n\n"
    "TWO SOURCE DEFECTS IN THE FY2023 EDITION, recorded and not corrected (map rule 7). Both are in its "
    "COMPARATIVE column and neither affects a cell on this sheet, because every year here comes from its own "
    "edition.\n"
    "  (a) Row 4, 31-Dec-22 comparative: the FY2023 edition prints 728,379, which is the FY2021 figure. "
    "FY2022's own edition prints 787,621. The FY2023 edition contradicts itself here - the same comparative "
    "column prints a CET1 ratio of 20.70%, and 163,071 / 787,621 = 20.70% exactly while 163,071 / 728,379 "
    "would be 22.39%. Three independent sources agree on 787,621: the FY2022 edition's own column, the "
    "FY2024 edition's chain, and this workbook's RWA Breakdown total.\n"
    "  (b) Rows UK 16b and 16, 31-Dec-23 (its OWN year): the FY2023 edition prints cash inflows 21,215 and "
    "total net cash outflows 47,570, which do not tie to each other (81,724 - 21,215 = 60,509) nor to its own "
    "row 17 (296,975 / 47,570 = 624%, but 519% is printed). The FY2024 edition's 31-Dec-23 comparative prints "
    "24,496 and 57,228, which tie both ways: 81,724 - 24,496 = 57,228 and 296,975 / 57,228 = 519%. This sheet "
    "shows 21,215 and 47,570 for FY2023 because that is what the year's own edition published; the figures "
    "that reconcile are the later edition's and are recorded here rather than substituted. FY2022 and FY2024 "
    "are internally consistent on every one of these rows.\n\n"
    "FY2021 AND EARLIER - BLANK, AND NOT FOR WANT OF LOOKING. The FY2021 and FY2020 Pillar 3 documents (70 and "
    "61 pages) carry no KM1 template at all. They use the PRE-2022 EU template set as separate tables: the "
    "own-funds composition template ('Own Funds - Regulatory disclosure template', rows 1/2/3/6/8/10/20c/28/29/"
    "45/59/60/61 per the EBA ITS on Disclosure for Own Funds), leverage as 'Table LRSum' and 'Table LRCom' with "
    "rows 1-8, 17-24 and EU-23/EU-24, and liquidity as a standalone three-row table numbered 21/22/23 "
    "('Liquidity Buffer - HQLA', 'Total Net Cash Outflows', 'Liquidity Coverage Ratio'). Those are LR and LIQ "
    "row numbers, not KM1 rows 13-17, and mapping them onto template row numbers would invent a correspondence "
    "the Bank never published (map rule 8). Checked for hidden bitmaps too, since this bank is a rule-13 case: "
    "pdfimages lists images only on pages 1, 10, 13 and 17 of those files, all small decorative ones (a "
    "2293x248 header band, 187x106 icons), none on the pages where the capital, leverage and liquidity tables "
    "sit (pp.30, 40, 51, 60).\n"
    "FY2021 IS THEREFORE THE FY2022 EDITION'S 31-DEC-21 COMPARATIVE COLUMN, filled under map rule 28: the "
    "FY2021 edition prints no key-metrics table at all, so there is no own-edition table for a later one to "
    "displace and rule 1 has nothing to bite on. This is rule 28's whole-missing-table case, not rule 20's "
    f"dashed-row case. Source for every FY2021 cell here: Pillar 3 Disclosures 2022, 'Table 1: Key metrics', "
    f"p.18, 31-Dec-21 column - {P3_2022_URL} . The three NSFR rows are left EMPTY by the Bank in that "
    "comparative column (the UK NSFR requirement took effect only from 1 January 2022) and stay empty here - "
    "filling a column from a comparative does not license inventing the cells the comparative leaves blank.\n"
    "FY2020 AND EARLIER REMAIN BLANK under rule 28's condition (c): no edition of any year prints a KM1 "
    "comparative reaching back that far, so there is no comparative to fill from.\n"
    "TWO EXPECTED DISAGREEMENTS WITH THE SINGLE-METRIC SHEETS, BOTH FY2021, BOTH GENUINE - predicted before "
    "this sheet was first built rather than explained afterwards. The metric sheets source FY2021 from that "
    "year's OWN pre-2022 templates, while this KM1 column is now the FY2022 edition's comparative, and the two "
    "editions do not agree: (i) row 14 leverage ratio, 12.83% here against 12.90% on the Leverage Ratio sheet "
    "(from the FY2021 edition's own Table LRCom); and (ii) row 17 liquidity coverage ratio, 283% here against "
    "287% on the LCR sheet (from the FY2021 edition's own 21/22/23 LCR table). Row 13's exposure measure "
    "differs too - 1,298,284 here against 1,298,463 there - but by 0.01%, inside the checker's amount "
    "tolerance. Both divergences are cross-edition restatements by the Bank, not transcription errors, and "
    "neither figure is edited to match the other.\n\n"
    "INVENTORY CORRECTION. research/km1_inventory.jsonl records the FY2020 and FY2021 editions as KM1_PRESENT. "
    "Both are FALSE POSITIVES on the evidence above - those editions carry CC1/LRSum/LRCom/LCR, not the key-"
    "metrics template. The same file records the FY2022 edition as NO_KM1_FOUND, which is a false NEGATIVE, "
    "since that edition does carry the full template as a bitmap. It has no row at all for the FY2023 and "
    "FY2024 editions, which are .docx and were never crawled. Recorded here so a later pass does not trust "
    "those verdicts in either direction.\n\n"
    "FY2025 - BLANK, WITH A DATE-FITTED EXPLANATION. No Pillar 3 document has been published for FY2025 and "
    "none will be. Bank of England consolidated waivers register (downloaded 2026-09-16): FRN 579415, "
    "'Cambridge & Counties Bank Limited', 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the "
    "SDDT Regime - General Application Part', sub rule 'Ru 3.1', ref A00009927P.pdf, START DATE 20/02/2025, no "
    "end date. DATE FIT: the Bank's year-end is 31 December, so the opt-in precedes the whole of FY2025 and "
    "explains its absence. It does NOT explain anything earlier - FY2022, FY2023 and FY2024 all postdate "
    "nothing relevant and all carry a full template, and the FY2024 edition was itself published on 14 May "
    "2025, after the opt-in. Only a Rule 3.1 row removes the disclosure obligation; this is the SDDT DISCLOSURE "
    "exemption in force now, not the SDDT CAPITAL regime beginning 1 January 2027.\n\n"
    "LATEST-EDITION CHECK, 16 September 2026: ccbank.co.uk's own media library lists eleven Pillar 3 documents, "
    "the newest being Pillar-3-report-CCB-2024.docx uploaded 14 May 2025. Newest edition published: FY2024, "
    "which this sheet holds. None newer. Also confirmed that Pillar-3-report-CCB-2024.docx and "
    "Pillar-3-report-Cambridge-Counties-Bank-2024.docx, uploaded the same day, are BYTE-IDENTICAL (both md5 "
    "ebe7d0191a3c5cbb4035a11e1213c7e7, both 506,357 bytes) - one document under two URLs, not two editions and "
    "not a second entity basis (map rule 11's inverse case)."
)

km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital (£'000)", {"FY2024": 213247, "FY2023": 190817, "FY2022": 163071, "FY2021": 144655}),
    ("DATA", "2  Tier 1 capital (£'000)", {"FY2024": 236147, "FY2023": 213717, "FY2022": 185972, "FY2021": 167555}),
    ("DATA", "3  Total capital (£'000)", {"FY2024": 241147, "FY2023": 218717, "FY2022": 185972, "FY2021": 167555}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4  Total risk-weighted exposure amount (£'000)", {"FY2024": 980319, "FY2023": 841556, "FY2022": 787621, "FY2021": 728379}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)", {"FY2024": "21.75%", "FY2023": "22.67%", "FY2022": "20.70%", "FY2021": "19.86%"}),
    ("DATA", "6  Tier 1 ratio (%)", {"FY2024": "24.09%", "FY2023": "25.40%", "FY2022": "23.61%", "FY2021": "23.00%"}),
    ("DATA", "7  Total capital ratio (%)", {"FY2024": "24.60%", "FY2023": "25.99%", "FY2022": "23.61%", "FY2021": "23.00%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirements (%)", {"FY2024": "5.19%", "FY2023": "5.19%", "FY2022": "5.19%", "FY2021": "3.10%"}),
    ("DATA", "UK 7d  Total SREP own funds requirements (%)", {"FY2024": "13.19%", "FY2023": "13.19%", "FY2022": "13.19%", "FY2021": "11.10%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8  Capital conservation buffer (%)", {"FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "9  Institution specific countercyclical capital buffer (%)", {"FY2024": "2.00%", "FY2023": "2.00%", "FY2022": "1.00%", "FY2021": "0.00%"}),
    ("DATA", "11  Combined buffer requirement (%)", {"FY2024": "4.50%", "FY2023": "4.50%", "FY2022": "3.50%", "FY2021": "2.50%"}),
    ("DATA", "UK 11a  Overall capital requirements (%)", {"FY2024": "17.69%", "FY2023": "17.69%", "FY2022": "16.69%", "FY2021": "13.60%"}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%)", {"FY2024": "8.56%", "FY2023": "9.48%", "FY2022": "7.51%", "FY2021": "7.41%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13  Leverage ratio total exposure measure (£'000)", {"FY2024": 1605041, "FY2023": 1435897, "FY2022": 1335869, "FY2021": 1298284}),
    ("DATA", "14  Leverage ratio (%)", {"FY2024": "14.71%", "FY2023": "14.88%", "FY2022": "13.92%", "FY2021": "12.83%"}),
    ("SECTION", "Liquidity Coverage Ratio (average of 12 months, per the Bank's own footnote)", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (Total Weighted value) (£'000)", {"FY2024": 345604, "FY2023": 296975, "FY2022": 265556, "FY2021": 255526}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value (£'000)", {"FY2024": 78028, "FY2023": 81724, "FY2022": 97431, "FY2021": 99787}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value (£'000)", {"FY2024": 20891, "FY2023": 21215, "FY2022": 13037, "FY2021": 9625}),
    ("DATA", "16  Total net cash outflows (£'000)", {"FY2024": 57137, "FY2023": 47570, "FY2022": 84394, "FY2021": 90162}),
    ("DATA", "17  Liquidity coverage ratio (%)", {"FY2024": "605%", "FY2023": "519%", "FY2022": "315%", "FY2021": "283%"}),
    ("SECTION", "Net Stable Funding Ratio (FY2022 footnoted 'Average of submitted returns post implementation of CRR II'; FY2023-FY2024 'Average of 12 months')", {}),
    ("DATA", "18  Total available stable funding (£'000)", {"FY2024": 1303092, "FY2023": 1190919, "FY2022": 1104235}),
    ("DATA", "19  Total required stable funding (£'000)", {"FY2024": 960390, "FY2023": 873031, "FY2022": 842391}),
    ("DATA", "20  NSFR ratio (%)", {"FY2024": "136%", "FY2023": "136%", "FY2022": "131%"}),
]

bw.add_km1_sheet(
    title="Cambridge & Counties Bank Limited - KM1 Key Metrics",
    subtitle="'Table 1: Key metrics' as published (the UK KM1 template), Bank-only basis, GBP'000. FY2022-"
             "FY2024 are own-edition years; FY2021 is the FY2022 edition's 31-Dec-21 comparative column (map "
             "rule 28). FY2020 and earlier predate the template entirely (those editions use the EU LR/LIQ "
             "set) and no comparative reaches them; no FY2025 Pillar 3 exists (SDDT, PRA Rule 3.1 from "
             "20/02/2025) - see source note",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=84,
    source_height=760,
    years=KM1_YEARS,
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)], p3_sources(), note=CALC_NOTE_2025)
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", CET1_RATIO)], p3_sources())
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", TIER1_CAPITAL)], p3_sources(), note=CALC_NOTE_2025)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", TIER1_RATIO)], p3_sources())
metric(
    "Total Capital", "£'000", [("Total capital", TOTAL_CAPITAL)], p3_sources(),
    note=CALC_NOTE_2025 + " Total Capital = Tier 1 capital alone for FY2021/FY2022 (no Tier 2 instruments held); "
                          "Tier 2 capital (£5m subordinated debt from British Business Bank Investments) was first "
                          "issued during FY2023, explaining the step-up between Tier 1 and Total Capital from that "
                          "year onward.",
)
metric("Total Capital Ratio", "%", [("Total capital ratio", TOTAL_CAPITAL_RATIO)], p3_sources())
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", TOTAL_RWA)], p3_sources(RWA_RESTATEMENT_NOTE))

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2024": 846780, "FY2023": 728547, "FY2022": 690434, "FY2021": 640391, "FY2020": 541056, "FY2019": 529304, "FY2018": 546029, "FY2017": 503743, "FY2016": 390505, "FY2015": 263398}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2024": 2753, "FY2023": 130, "FY2022": 232, "FY2021": 46, "FY2020": 50, "FY2019": 23, "FY2018": 2906, "FY2017": 4024, "FY2016": 3087, "FY2015": 2180}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2024": 0, "FY2023": 0, "FY2022": 7991, "FY2021": 9158, "FY2020": 8161, "FY2019": 9034, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0}),
    ("DATA", "Operational risk", {"FY2024": 130786, "FY2023": 112879, "FY2022": 88964, "FY2021": 78784, "FY2020": 78647, "FY2019": 79158, "FY2018": 70234, "FY2017": 53863, "FY2016": 35013, "FY2015": 19275}),
    ("DATA", "Amounts below the thresholds for deduction", {"FY2024": 2267, "FY2023": 1801, "FY2022": 2749, "FY2021": 1984, "FY2020": 1813, "FY2019": 1823, "FY2018": 2199, "FY2017": 632, "FY2016": 551, "FY2015": 653}),
    ("TOTAL", "Total RWAs", {"FY2024": 980319, "FY2023": 841556, "FY2022": 787621, "FY2021": 728379, "FY2020": 629727, "FY2019": 619342, "FY2018": 621368, "FY2017": 561630, "FY2016": 428605, "FY2015": 284853}),
]

bw.add_rwa_breakdown_sheet(
    title="Cambridge & Counties Bank Limited — RWA Breakdown",
    subtitle="Bank-only basis (no subsidiaries), £'000. FY2025 not publicly disclosed (no standalone Pillar 3 "
              "document published, and none will be - the Bank is an SDDT and is exempt from the Pillar 3 disclosure obligation, see ENTITY NOTE; re-confirmed 2026-09-12 via site check + Wayback CDX, no Pillar 3 URL "
              "of any kind crawled for this domain in 2026). See source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=280,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "£'000 exposure / %",
    [
        ("Leverage ratio total exposure measure", {"FY2024": 1605041, "FY2023": 1435897, "FY2022": 1335869, "FY2021": 1298463, "FY2020": 1097253, "FY2019": 1028001, "FY2018": 1051134, "FY2017": 1024505, "FY2016": 821551, "FY2015": 582770}),
        ("Leverage ratio (%)", {"FY2024": "14.71%", "FY2023": "14.88%", "FY2022": "13.92%", "FY2021": "12.90%", "FY2020": "13.96%", "FY2019": "13.85%", "FY2018": "12.10%", "FY2017": "7.39%", "FY2016": "6.91%", "FY2015": "6.30%"}),
    ],
    p3_sources(LEVERAGE_NOTE),
    note="FY2025 not publicly disclosed (no standalone Pillar 3 document published, and none will be - the Bank is an SDDT and is exempt from the Pillar 3 disclosure obligation, see ENTITY NOTE; and the Annual "
         "Report's own Strategic Report narrative does not state a leverage ratio figure).",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA)", {"FY2024": 345604, "FY2023": 296975, "FY2022": 265556, "FY2021": 275200, "FY2020": 284100, "FY2019": 297100, "FY2018": 334600}),
        ("Total net cash outflows", {"FY2024": 57137, "FY2023": 47570, "FY2022": 84394, "FY2021": 95900, "FY2020": 67800, "FY2019": 64200, "FY2018": 105800}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "587%", "FY2024": "605%", "FY2023": "519%", "FY2022": "315%", "FY2021": "287%", "FY2020": "419.0%", "FY2019": "462.8%", "FY2018": "321.1%"}),
    ],
    p3_sources(LCR_NOTE),
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2024": 1303092, "FY2023": 1190919, "FY2022": 1104235}),
        ("Total required stable funding", {"FY2024": 960390, "FY2023": 873031, "FY2022": 842391}),
        ("Net Stable Funding Ratio (%)", {"FY2024": "136%", "FY2023": "136%", "FY2022": "131%"}),
    ],
    p3_sources(),
    note="FY2021 and FY2025 not publicly disclosed - the UK NSFR requirement only took effect for periods "
         "starting after 1 Jan 2022 (FY2021's Pillar 3 report has no NSFR section at all), and no standalone "
         "Pillar 3 document has been published, and none will be - the Bank is an SDDT and is exempt from the Pillar 3 disclosure obligation, see ENTITY NOTE.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "Not found in any of the 5 years' Annual Reports or Pillar 3 disclosures reviewed - "
                             "no numeric ratio, and no explicit exemption statement either; the Bank's balance "
                             "sheet scale is consistent with sitting below the threshold at which MREL applies."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1898633, "FY2024": 1581735, "FY2023": 1450722, "FY2022": 1376545, "FY2021": 1274871}),
        ("Loans and advances to customers", {"FY2025": 1446075, "FY2024": 1204444, "FY2023": 1083278, "FY2022": 1037710, "FY2021": 977834}),
        ("Customers' accounts", {"FY2025": 1633601, "FY2024": 1271824, "FY2023": 1155224, "FY2022": 1103256, "FY2021": 1025520}),
        ("Total equity", {"FY2025": 248643, "FY2024": 240084, "FY2023": 214778, "FY2022": 184846, "FY2021": 163817}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 71216, "FY2024": 73601, "FY2023": 76404, "FY2022": 59252, "FY2021": 44950}),
        ("Administrative expenses", {"FY2025": -32390, "FY2024": -31772, "FY2023": -27287, "FY2022": -25034, "FY2021": -21965}),
        ("Profit after tax", {"FY2025": 30492, "FY2024": 27663, "FY2023": 31290, "FY2022": 23202, "FY2021": 15466}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 240084, "FY2024": 214778, "FY2023": 184846, "FY2022": 163817}),
        ("Total comprehensive income for the year", {"FY2025": 30843, "FY2024": 27765, "FY2023": 32123, "FY2022": 22468, "FY2021": 14965}),
        ("Other equity movements, net", {"FY2025": -22284, "FY2024": -2459, "FY2023": -2191, "FY2022": -1439, "FY2021": -1283}),
        ("Closing equity", {"FY2025": 248643, "FY2024": 240084, "FY2023": 214778, "FY2022": 184846, "FY2021": 163817}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash generated from operating activities", {"FY2025": 98255, "FY2024": 13542, "FY2023": 26342, "FY2022": 45314, "FY2021": 53825}),
        ("Net cash (used in)/generated from investing activities", {"FY2025": -87372, "FY2024": -18987, "FY2023": -16474, "FY2022": 4285, "FY2021": -740}),
        ("Net cash (used in)/generated from financing activities", {"FY2025": -22284, "FY2024": -2459, "FY2023": 2413, "FY2022": -1439, "FY2021": -1283}),
        ("Cash and cash equivalents at 31 December", {"FY2025": 293588, "FY2024": 304989, "FY2023": 312893, "FY2022": 300611, "FY2021": 252451}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Tier 1 Ratio", TIER1_RATIO),
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
        ("Leverage Ratio", {"FY2024": "14.71%", "FY2023": "14.88%", "FY2022": "13.92%", "FY2021": "12.90%"}),
        ("LCR", {"FY2025": "587%", "FY2024": "605%", "FY2023": "519%", "FY2022": "315%", "FY2021": "287%"}),
        ("NSFR", {"FY2024": "136%", "FY2023": "136%", "FY2022": "131%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. See the RWA and Leverage caveats on the Total RWAs "
         "and Leverage Ratio sheets before treating year-on-year moves in those two series as fully comparable.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CAMBRIDGE AND COUNTIES BANK FINANCIALS.xlsx")
