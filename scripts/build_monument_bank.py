import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]

# Companies House filings for Monument Bank Limited (company 10921940).
AR25_URL = "https://find-and-update.company-information.service.gov.uk/company/10921940/filing-history/MzQ3Njc0NjA3MmFkaXF6a2N4/document?download=0&format=pdf"
AR24_URL = "https://find-and-update.company-information.service.gov.uk/company/10921940/filing-history/MzQzNjUxODg2NmFkaXF6a2N4/document?download=0&format=pdf"
AR23_URL = "https://find-and-update.company-information.service.gov.uk/company/10921940/filing-history/MzM5NDQyODAwN2FkaXF6a2N4/document?download=0&format=pdf"
AR22_URL = "https://find-and-update.company-information.service.gov.uk/company/10921940/filing-history/MzM1Mjc4MTU2M2FkaXF6a2N4/document?download=0&format=pdf"
AR20_URL = "https://find-and-update.company-information.service.gov.uk/company/10921940/filing-history/MzMxNjk5NzI2OGFkaXF6a2N4/document?download=0&format=pdf"

# Standalone Pillar 3 disclosures, published by the Bank itself. Found 2026-09-15.
# The FY2022 and FY2023 files are still linked from https://www.monument.co/annual-reports
# and share an identical display name, differing only by Webflow CDN hash - the year was
# confirmed from each document's own cover page and running footer, not from the filename.
# The FY2021 document sits on Monument's older Contentful CDN and is no longer linked from
# the live page; the URL was recovered from the Wayback capture of the annual-reports page
# dated 2023-06-09 and re-verified live on 2026-09-15 (HTTP 200, byte-identical).
P3_23_URL = "https://cdn.prod.website-files.com/6435124ea79f72c265f72807/66f410fafb215ace68a82827_Monument%20Bank%20Pillar%203%20Report.pdf"
P3_22_URL = "https://cdn.prod.website-files.com/6435124ea79f72c265f72807/65168a20ee9b129fb0cb9fe3_Monument%20Bank%20Pillar%203%20Report.pdf"
P3_21_URL = "https://assets.ctfassets.net/056oa4qkl0n4/3IhfDT5SeXi0hEaeG4qX3P/066a72110553dbd149a1e9e27c095ffb/2021_Pillar_3_Disclosures_document.pdf"

# Monument also publishes its own annual reports at https://www.monument.co/annual-reports.
# These are the same accounts as the Companies House filings but, unlike the scanned CH
# copies, the FY2020, FY2023 and FY2024 web copies carry a real text layer.
WEB_AR24_URL = "https://cdn.prod.website-files.com/6435124ea79f72c265f72807/68948defbf0375a1d85d11f9_Monument%20Bank%202024.pdf"
WEB_AR23_URL = "https://cdn.prod.website-files.com/6435124ea79f72c265f72807/66f6d2535d967ffe1afc3061_Monument%20Bank%20FY23.pdf"
WEB_AR20_URL = "https://cdn.prod.website-files.com/6435124ea79f72c265f72807/6489c5a09d3686a31e3ae73d_Monument_Bank_Limited_2020_Annual_Report.pdf"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Monument Bank Limited (Companies House 10921940; FRN 849724; "
    "LEI 213800OLF8OE1I3HVY91) is the matched legal entity in Banks List 2608.xlsx. "
    "Cash flows are the Company/standalone figures in £'000. The latest available filing "
    "is the report for the year ended 31 December 2024; FY2025 is blank because no FY2025 "
    "accounts were available in the Companies House filing history reviewed. The accounts "
    "are scanned filings and were OCR-processed and cross-checked against rendered pages "
    "(the FY2020 filing was re-OCR'd with layout-preserving column extraction to resolve "
    "a multi-column table). Blank cells mean not publicly disclosed, not zero.\n\n"
    "HISTORICAL FLOOR NOTE: the entity (Companies House 10921940) was incorporated on "
    "18 August 2017 as 'Monument Principal Capital Ltd.', renamed 'Monument Corporation "
    "Ltd.' on 26 January 2018, and only renamed 'Monument Bank Limited' on 9 November 2020 "
    "after receiving its PRA/FCA Banking Licence on 6 October 2020 (entering the "
    "'Authorisation with Restriction' mobilisation phase). Two micro-entity accounts were "
    "filed for the pre-bank shell company - for the period to 31 August 2018 (Companies "
    "House filing 13 Apr 2019) and the shortened period to 31 December 2018 (filing 3 Jul "
    "2019), plus a further micro-entity filing for FY2019 (filing 27 Apr 2020) - all three "
    "were independently retrieved, OCR'd and read in full: none discloses any banking "
    "business (no loans, no deposits, no P&L is even filed under the micro-entity "
    "exemption - only a bare shell-company balance sheet: total shareholders' funds of "
    "£52,101 at 31 Aug 2018, £5,042,885 at 31 Dec 2018, £5,578,186 at 31 Dec 2019, all "
    "cash/debtors/share-capital with no line item this workbook's shape could populate). "
    "FY2017-FY2019 are therefore self-skipped in full as a genuine non-disclosure of any "
    "bank-relevant figures, not a convenience skip - the ticket's claimed 'FY2017 floor' "
    "(from HD-001's generic entity-incorporation-year filter) does not hold for this bank, "
    "the same pattern already found for Griffin Bank Ltd in this batch. FY2020 is the real "
    "floor: the first full, audited annual report (45 pages, filed 15 Oct 2021), covering "
    "the Bank's first year in the mobilisation/pre-revenue phase post-licence. FY2020's own "
    "Asset Quality is genuinely blank (no loans and advances to customers existed yet - the "
    "Bank had not begun lending); among the Pillar 3 metrics that year the Total Capital Ratio "
    "(359%), CET1 capital, Tier 1 capital and Total capital (all £23,895,804) are disclosed - "
    "the first via FY2020's own Strategic Report, the capital amounts via the FY2021 report's "
    "2020 comparative column (see the Pillar 3 sheets' 2026-09-12 re-verification note)."
)

CASH_SOURCES = (
    "Sources - Monument Bank Limited Company/standalone cash flows, £'000:\n"
    f"FY2024 & FY2023: Financial Statements for the year ended 31 December 2024, pp.74-75 (Company columns) - {AR25_URL}\n"
    f"FY2023 & FY2022: Financial Statements for the year ended 31 December 2023, p.35 (Company figures; FY2022 comparative) - {AR24_URL}\n"
    f"FY2022 & FY2021: Financial Statements for the year ended 31 December 2022, p.29 - {AR23_URL}\n"
    f"FY2021: Financial Statements for the year ended 31 December 2021, p.25 - {AR22_URL}\n"
    f"FY2020: Financial Statements for the year ended 31 December 2020, Statement of Cash Flows, "
    f"p.30 - {AR20_URL}\n\n"
    + ENTITY_NOTE
)

P3_SOURCES = (
    "Sources - Monument Bank Limited annual regulatory KPIs and risk disclosures:\n"
    f"FY2024 & FY2023: Financial Statements for the year ended 31 December 2024, pp.11-12 and 74 - {AR25_URL}\n"
    f"FY2023 & FY2022: Financial Statements for the year ended 31 December 2023, pp.8-9 and 60-61 - {AR24_URL}\n"
    f"FY2022 & FY2021: Financial Statements for the year ended 31 December 2022, pp.10 and 51 - {AR23_URL}\n"
    f"FY2021: Financial Statements for the year ended 31 December 2021, pp.9 and 41 - {AR22_URL}\n"
    f"FY2020: Financial Statements for the year ended 31 December 2020, Strategic Report - "
    f"Financial Review, p.9 - {AR20_URL}\n\n"
    "STANDALONE PILLAR 3 DOCUMENTS - PRIMARY SOURCE FOR FY2021-FY2023, found 2026-09-15:\n"
    f"FY2023: Monument Bank Pillar 3 Disclosures for the year ended 31 December 2023, "
    f"section 11 'Key Metrics' (full UK KM1 table), p.28, and section 6.1 'Pillar 1 Capital "
    f"requirements', p.24 - {P3_23_URL}\n"
    f"FY2022: Monument Bank Pillar 3 Disclosures for the Year Ended 31 December 2022, "
    f"section 11 'Key Metrics', p.28, and section 6.1, p.23 - {P3_22_URL}\n"
    f"FY2021: Monument Bank Pillar 3 Disclosures for the year ended 31 December 2021, "
    f"section 11 'Key Metrics', pp.30-31, and section 6.1, p.25 - {P3_21_URL}\n\n"
    "CORRECTION 2026-09-15. This note previously asserted that 'Monument has never published a "
    "standalone Pillar 3 document in any year: every Pillar 3 figure here is transcribed from an "
    "Annual Report.' That was wrong. Three standalone Pillar 3 documents exist, each carrying a "
    "complete UK KM1 table (items 1-20), and all three were retrieved, year-verified from their "
    "own cover pages and transcribed in this pass. They are the reason FY2021 and FY2022 are no "
    "longer blank for Tier 1 Ratio, Total RWAs, Leverage Ratio and NSFR, and the reason the "
    "FY2021 and FY2020 Total Capital Ratio figures were withdrawn (see that sheet's note). The "
    "earlier claim was reached by searching Companies House only; Monument publishes its Pillar 3 "
    "documents on its own website (https://www.monument.co/annual-reports), never at Companies "
    "House, so a Companies-House-only search returns a false negative for this bank.\n\n"
    "CHAIN VALIDATION. The three documents form an unbroken chain: each one's prior-year column "
    "reproduces the next one's current-year column exactly, for every KM1 item. The FY2023 "
    "document's 2022 column matches the FY2022 document's 2022 column (CET1 21,299,969; RWA "
    "48,417,473; ratios 43.99%; leverage 12.00%; LCR 10,128%; NSFR 242.85%), and the FY2022 "
    "document's 2021 column matches the FY2021 document (CET1 32,643,538; RWA 29,951,235; ratios "
    "108.99%; leverage 90.48%; LCR 2,861,111,111%; NSFR 153.40%). In every year the section 6.1 "
    "risk-category components also sum exactly to the KM1 item-4 Total RWA. Capital amounts agree "
    "with the Annual Reports' 'Regulatory capital' tables to the pound in all three years.\n\n"
    "BASIS SPLIT. FY2021-FY2023 Pillar 3 metrics are taken from the Pillar 3 documents where the "
    "two sources differ; FY2024 and FY2020 have no Pillar 3 document and remain on the Annual "
    "Report. Where an Annual Report comparative differs from the Pillar 3, both figures are "
    "recorded on the affected sheet rather than one silently replacing the other - see the Total "
    "RWAs, NSFR and RWA Breakdown sheets.\n\n"
    "The reports do not provide a complete UK KM1 table for every year. Only explicitly disclosed "
    "entity-level values are populated; unavailable capital components and ratios remain blank.\n\n"
    "RE-VERIFIED 2026-09-12 (disclosure audit): all five annual reports (FY2020-FY2024) were "
    "re-downloaded from Companies House and OCR'd in full - they are scanned filings with no text "
    "layer, so an earlier text-only pass would have found nothing in them. This pass overturned two "
    "previous claims. (1) 'No standalone Tier 1 capital amount was separately disclosed' was wrong: "
    "every report from FY2020 onward carries a 'Regulatory capital' table (Note 20/21) whose bottom "
    "line reads 'Total Tier 1 capital', giving FY2024 56,324 / FY2023 28,035.733 / FY2022 21,299.969 "
    "/ FY2021 32,643.538 / FY2020 23,895.804 (£'000). (2) 'FY2020 only discloses a Total Capital "
    "Ratio' was also wrong: the FY2021 report's 2020 comparative column supplies FY2020's CET1 and "
    "Tier 1 capital as well. Each figure was cross-checked against the disclosed ratios, which it "
    "reproduces exactly (see the CET1 Ratio sheet's note). Tier 1 Ratio and MREL Ratio remain "
    "genuinely undisclosed in every year.\n\n"
    "SDDT STATUS, established 2026-09-15 (cross-bank SDDT pass) - recorded so that no future session "
    "wastes effort hunting for a Monument Pillar 3 document that will never exist. Monument Bank is a "
    "Small Domestic Deposit Taker (SDDT), and becoming one removes the Pillar 3 disclosure obligation "
    "outright. Evidence - the PRA's own firm-level register, the Bank of England consolidated list of "
    "waivers and modifications granted to PRA-authorised firms (downloaded 2026-09-15, "
    "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
    "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv), row: FRN 849724, 'MONUMENT "
    "BANK LIMITED', 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT Regime - "
    "General Application Part', rule 'SDDT Regime - General Application', sub rule 'Ru 3.1', waiver ref "
    "'A00009546.pdf', start date '15/01/2025', no end date. What Rule 3.1 does to Pillar 3 is stated by a "
    "peer holding the identical register row - Cynergy Bank plc Annual Report & Accounts 2024, p.71: 'The "
    "Bank applied for the Modification by Consent to become an SDDT and received approval on 17 January "
    "2025. As a result, we are not required to publish Pillar 3 disclosures as at 31 December 2024 and will "
    "submit only a simplified retail deposit ratio instead of a full Net Stable Funding Ratio (NSFR) going "
    "forward.' (Cynergy's own row is Rule 3.1 starting '17/01/2025' - two days after Monument's - matching "
    "its stated approval date to the day, which is what ties the register row to the firm-stated effect.)\n"
    "SCOPE - WHAT THIS DOES AND DOES NOT EXPLAIN (revised 2026-09-15). It changes NO cell in this workbook, "
    "but it does explain the shape of the Pillar 3 record. Monument published a standalone Pillar 3 document "
    "for FY2021, FY2022 and FY2023 (all three are cited above and are the primary source for those years), "
    "and then stopped: the SDDT modification took effect 15 January 2025, which removed the obligation to "
    "publish Pillar 3 disclosures as at 31 December 2024, and Monument's own annual-reports page lists no "
    "FY2024 Pillar 3 document - only the FY2022 and FY2023 ones. So the FY2024 column is on an Annual Report "
    "basis because no FY2024 Pillar 3 exists or will exist, and that IS an SDDT consequence. What SDDT does "
    "not explain is FY2020, which predates both the SDDT regime and Monument's first Pillar 3 - the Bank was "
    "in its post-licence mobilisation phase and simply published less. Do not read SDDT back onto FY2023 or "
    "earlier: those years have full KM1 tables. The FY2025 column is blank "
    "for an entirely separate and unrelated reason - no FY2025 accounts had been filed at Companies House "
    "when this workbook was built (a filing-lag gap, which will close when the FY2025 accounts appear); it "
    "is NOT an SDDT exemption. What the SDDT status does establish is forward-looking: no Monument Pillar 3 "
    "disclosure will ever be published for FY2025 or later, so the Annual Report will remain the only "
    "source for these metrics.\n"
    "The Bank does not state its SDDT status in its own words. The FY2023 and FY2024 Annual Reports are "
    "fully scanned, image-only Companies House filings with no text layer (pdftotext extracted 0 characters "
    "from each), so both were OCR'd page-by-page at 200dpi with tesseract before being searched - a plain "
    "text search would have returned a false negative here. The FY2023 report mentions SDDT not at all; the "
    "FY2024 report mentions it twice, in both cases only as regulatory-watching context: 'We continue to "
    "monitor the developments of Basel 3.1 and the Small Domestic Deposit Takers (SDDT) regime and their "
    "potential impact' (p.12, Capital and liquidity) and 'The Board continues to monitor the developments of "
    "Basel 3.1 and Small Domestic Deposit Takers (SDDT) regime' (p.23, Capital risk). Neither states an "
    "opt-in, an approval date, or any Pillar 3 consequence - the PRA register is what evidences those. No "
    "Simplified Retail Deposit Ratio value is disclosed either.\n"
    "ADDENDUM 2026-09-15: the scanning problem is a property of the Companies House copies, not of the "
    "reports. Monument hosts its own PDFs of the same accounts, and the FY2020, FY2023 and FY2024 web "
    f"copies carry real text layers - FY2024 {WEB_AR24_URL}, FY2023 {WEB_AR23_URL}, FY2020 {WEB_AR20_URL} "
    "(the FY2022 web copy is scanned like the Companies House one). Future passes on this bank should "
    "prefer the web copies; the OCR round-trip is avoidable for three of the five years. Both sets were "
    "compared for this pass and agree on every figure in this workbook."
)

bw = BankWorkbook(bank_name="Monument Bank Limited", years=YEARS, header_color="5B2C6F")

STATEMENTS_SOURCES = (
    "Sources - Monument Bank Limited Company/standalone Balance Sheet, Profit & Loss, "
    "Statement of Changes in Equity, and Asset Quality, £'000:\n"
    f"FY2024 & FY2023: Financial Statements for the year ended 31 December 2024, "
    "Statement of financial position/Statement of total comprehensive income/Statement of "
    f"changes in equity, pp.52-55, and Note 16 Loans and advances to customers, p.68 - {AR25_URL}\n"
    f"FY2023 & FY2022: Financial Statements for the year ended 31 December 2023, "
    "Statement of financial position/Statement of total comprehensive income/Statement of "
    f"changes in equity, pp.32-34, and Note 15 Loans and advances to customers, p.51 - {AR24_URL}\n"
    f"FY2022: Financial Statements for the year ended 31 December 2022, Statement of "
    "financial position/Statement of total comprehensive income, pp.27-28 (own-year figures - "
    f"confirmed identical to the FY2023 report's FY2022 comparative, no restatement) - {AR23_URL}\n"
    f"FY2021: Financial Statements for the year ended 31 December 2021, Statement of "
    "financial position/Statement of total comprehensive income/Statement of changes in "
    f"equity, pp.23-26, and Note 13 Loans and advances to customers, pp.37-38 - {AR22_URL}\n"
    f"FY2020: Financial Statements for the year ended 31 December 2020, Statement of "
    "Financial Position p.28, Income Statement p.26, Statement of Comprehensive Income p.27, "
    f"Statement of Changes in Equity p.29 - {AR20_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nBASIS NOTE: all 4 statement sheets are shown on the same Company/standalone basis "
    "as the Cash Flow Statement. Whole-£ source figures for FY2022, FY2021 and FY2020 have "
    "been converted to £'000 (division by 1,000, decimals retained) - FY2024/FY2023 are "
    "already reported in £'000 by the source document.\n\n"
    "PRESENTATION NOTE: FY2021's Balance Sheet used a different line structure to later years "
    "- a single combined 'Cash and balances with banks' line (no separate 'Loans and advances "
    "to credit institutions' split), no Treasury bills/Debt securities/Derivative financial "
    "instruments lines (the Bank had none that year), and no Available-for-sale reserve line "
    "(introduced only once AFS investments were held, from FY2023). These are left blank for "
    "FY2021 rather than estimated, per this project's standing 'blank cells mean not "
    "disclosed, not zero' convention - except where the source explicitly states nil ('-'), "
    "which is shown as 0. FY2020's Balance Sheet is simpler still: 'Cash and balances at "
    "central banks / with banks' is Cash at Bank, 'Other assets' is Debtors, and 'Other "
    "liabilities and accruals' is Creditors falling due within one year - the Bank had no "
    "loan book, no customer deposits, no derivatives and no treasury/debt securities that "
    "year (pre-launch mobilisation phase), so those lines are blank, not zero.\n\n"
    "EQUITY LADDER: confirmed exactly across all 5 years - each year's own closing balance "
    "ties to both the next year's own opening balance and that year's own Balance Sheet Total "
    "equity, with zero plug rows. All equity movements (share issuances, shares to be issued, "
    "employee share scheme charge, available-for-sale reserve movements) are genuinely "
    "disclosed line items, not derived.\n\n"
    "ASSET QUALITY NOTE: this Bank applies FRS 102 in conjunction with IAS 39's incurred-loss "
    "impairment model (not IFRS 9), so no Stage 1/2/3 split is disclosed in any year - Asset "
    "Quality is built instead from the Bank's own individual/collective impairment provision "
    "note, which is the finest granularity disclosed. FY2020 is blank on this one sheet only "
    "(self-skipped at the year level, not the whole sheet/bank): the Bank had not begun "
    "lending as of 31 December 2020 (pre-revenue mobilisation phase following its 6 October "
    "2020 Banking Licence), so no loan book or impairment provision existed to disclose that "
    "year - confirmed by the FY2020 Statement of Financial Position, which has no loans and "
    "advances to customers line at all.\n\n"
    "RWA BREAKDOWN NOTE: no breakdown of Total RWAs by risk category (credit/market/"
    "operational risk) was found in any of the 4 filings' risk management or capital "
    "sections reviewed - only the aggregate Total Tier 1 capital and (via the Total Capital "
    "Ratio) an implied Total RWAs figure are disclosed. Confirmed as a genuine non-disclosure, "
    "not an access gap - all 4 filings were fully read through their risk management notes."
)

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks / with banks", {"FY2024": 3685561, "FY2023": 354658, "FY2022": 60337.153, "FY2021": 23888.337, "FY2020": 25112.989}),
    ("DATA", "Loans and advances to credit institutions", {"FY2024": 39419, "FY2023": 22557, "FY2022": 5336.605}),
    ("DATA", "Treasury bills", {"FY2023": 130102, "FY2021": 10300.000}),
    ("DATA", "Debt securities", {"FY2024": 1227659, "FY2023": 384491, "FY2022": 10542.496}),
    ("DATA", "Derivative financial instruments", {"FY2024": 1460, "FY2023": 2423, "FY2022": 3648.550}),
    ("DATA", "Loans and advances to customers", {"FY2024": 173839, "FY2023": 139689, "FY2022": 93371.115, "FY2021": 759.085}),
    ("DATA", "Other assets", {"FY2024": 2576, "FY2023": 2522, "FY2022": 1102.443, "FY2021": 989.827, "FY2020": 301.406}),
    ("DATA", "Tangible fixed assets", {"FY2024": 261, "FY2023": 164, "FY2022": 160.952, "FY2021": 140.030, "FY2020": 28.978}),
    ("DATA", "Intangible fixed assets", {"FY2024": 12153, "FY2023": 11184, "FY2022": 10560.587, "FY2021": 9479.735, "FY2020": 1301.285}),
    ("TOTAL", "Total assets", {"FY2024": 5142928, "FY2023": 1047790, "FY2022": 185059.901, "FY2021": 45557.014, "FY2020": 26744.658}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2024": 5069724, "FY2023": 990502, "FY2022": 147657.857, "FY2021": 2093.036}),
    ("DATA", "Derivative financial instruments", {"FY2024": 573, "FY2023": 2178, "FY2022": 1072.413}),
    ("DATA", "Other liabilities and accruals", {"FY2024": 2882, "FY2023": 1417, "FY2022": 1673.075, "FY2021": 1340.705, "FY2020": 1547.569}),
    ("TOTAL", "Total liabilities", {"FY2024": 5073179, "FY2023": 994097, "FY2022": 150403.345, "FY2021": 3433.741, "FY2020": 1547.569}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2024": 39, "FY2023": 32, "FY2022": 27.256, "FY2021": 25.730, "FY2020": 16.354}),
    ("DATA", "Share premium reserve", {"FY2024": 129928, "FY2023": 87459, "FY2022": 61434.408, "FY2021": 58982.976, "FY2020": 18397.070}),
    ("DATA", "Shares to be issued", {"FY2024": 48, "FY2023": 13980, "FY2022": 2796.000, "FY2021": 724.816, "FY2020": 15034.157}),
    ("DATA", "Available-for-sale reserve", {"FY2024": -216, "FY2023": 575, "FY2022": 0}),
    ("DATA", "Accumulated losses", {"FY2024": -60050, "FY2023": -48353, "FY2022": -29601.108, "FY2021": -17610.249, "FY2020": -8250.492}),
    ("TOTAL", "Total equity", {"FY2024": 69749, "FY2023": 53693, "FY2022": 34656.556, "FY2021": 42123.273, "FY2020": 25197.089}),
    ("TOTAL", "Total liabilities and equity", {"FY2024": 5142928, "FY2023": 1047790, "FY2022": 185059.901, "FY2021": 45557.014, "FY2020": 26744.658}),
]

bw.add_balance_sheet_sheet(
    title="Monument Bank Limited - Balance Sheet",
    subtitle="Company/standalone basis, £'000; 31 December year-end.",
    rows=bs_rows, sources_text=STATEMENTS_SOURCES, first_col_width=68, source_height=340, unit_suffix=" (£'000)",
)

pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2024": 148993, "FY2023": 20705, "FY2022": 2128.074, "FY2021": 0.730, "FY2020": 8.260}),
    ("DATA", "Interest payable and similar charges", {"FY2024": -136868, "FY2023": -17400, "FY2022": -1784.745, "FY2021": -1.102}),
    ("TOTAL", "Net interest income/(expense)", {"FY2024": 12125, "FY2023": 3305, "FY2022": 343.329, "FY2021": -0.372, "FY2020": 8.260}),
    ("DATA", "Net fee income", {"FY2024": 14}),
    ("DATA", "Net gains/(losses) from derivative financial instruments", {"FY2024": 1726, "FY2023": -2331, "FY2022": 3464.937}),
    ("DATA", "Other operating expense", {"FY2024": -185, "FY2023": -49}),
    ("TOTAL", "Total net income/(expense)", {"FY2024": 13680, "FY2023": 925, "FY2022": 3808.266, "FY2021": -0.372, "FY2020": 8.260}),
    ("DATA", "Administrative expenses", {"FY2024": -26926, "FY2023": -20895, "FY2022": -18474.978, "FY2021": -9970.282, "FY2020": -5743.261}),
    ("DATA", "Impairment charge on loans and advances to customers", {"FY2024": -79, "FY2023": -83, "FY2022": -101.980, "FY2021": -2.664}),
    ("TOTAL", "Operating loss before taxation", {"FY2024": -13325, "FY2023": -20053, "FY2022": -14768.692, "FY2021": -9973.318, "FY2020": -5735.001}),
    ("DATA", "Taxation credit/(expense)", {"FY2024": 239, "FY2023": 693, "FY2022": 2059.137, "FY2021": 0, "FY2020": 0}),
    ("TOTAL", "Loss for the financial year", {"FY2024": -13086, "FY2023": -19360, "FY2022": -12709.555, "FY2021": -9973.318, "FY2020": -5735.001}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Fair value movements taken to reserves", {"FY2024": -813, "FY2023": 553}),
    ("DATA", "Amount transferred to income statement", {"FY2024": 21, "FY2023": 23}),
    ("TOTAL", "Other comprehensive income for the year", {"FY2024": -792, "FY2023": 576, "FY2022": 0, "FY2021": 0, "FY2020": 0}),
    ("TOTAL", "Total comprehensive loss for the year", {"FY2024": -13878, "FY2023": -18784, "FY2022": -12709.555, "FY2021": -9973.318, "FY2020": -5735.001}),
]

bw.add_income_statement_sheet(
    title="Monument Bank Limited - Profit & Loss",
    subtitle="Company/standalone basis, £'000. FY2023 Company Net fee income/Total net income "
              "figures are identical to Group (no fee income that year); FY2021 predates "
              "derivative and fee income lines; FY2020 is pre-revenue (mobilisation phase, "
              "no interest payable/fee/impairment lines existed yet).",
    rows=pl_rows, sources_text=STATEMENTS_SOURCES, first_col_width=76, source_height=340, unit_suffix=" (£'000)",
)

equity_headers = ["Called up share capital", "Share premium", "Shares to be issued", "Available-for-sale reserve", "Accumulated losses", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2020 (FY2020 opening)", (13.099, 6928.158, 1499.595, 0, -2862.666, 5578.186)),
    ("DATA", "Loss for the year", (None, None, None, None, -5735.001, -5735.001)),
    ("DATA", "Employee share scheme charge", (None, None, None, None, 347.175, 347.175)),
    ("DATA", "Issue of share capital", (3.255, 11468.912, -1499.595, None, None, 9972.572)),
    ("DATA", "Shares to be issued", (None, None, 15034.157, None, None, 15034.157)),
    ("TOTAL", "At 31 December 2020 (FY2020 closing / FY2021 opening)", (16.354, 18397.070, 15034.157, 0, -8250.492, 25197.089)),
    ("DATA", "Loss for the year", (None, None, None, None, -9973.318, -9973.318)),
    ("DATA", "Employee share scheme charge", (None, None, None, None, 613.561, 613.561)),
    ("DATA", "Issue of share capital", (9.376, 40585.906, -15034.157, None, None, 25561.125)),
    ("DATA", "Shares to be issued", (None, None, 724.816, None, None, 724.816)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (25.730, 58982.976, 724.816, 0, -17610.249, 42123.273)),
    ("DATA", "Loss for the year", (None, None, None, None, -12709.555, -12709.555)),
    ("DATA", "Employee share scheme charge", (None, None, None, None, 718.696, 718.696)),
    ("DATA", "Issue of share capital", (1.526, 2451.432, -724.816, None, None, 1728.142)),
    ("DATA", "Shares to be issued", (None, None, 2796.000, None, None, 2796.000)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (27.256, 61434.408, 2796.000, 0, -29601.108, 34656.556)),
    ("DATA", "Loss for the year", (None, None, None, None, -19359.604, -19359.604)),
    ("DATA", "Movement in available-for-sale reserve", (None, None, None, 575.232, None, 575.232)),
    ("DATA", "Employee share scheme charge", (None, None, None, None, 608.050, 608.050)),
    ("DATA", "Issue of share capital", (4.809, 26024.340, -2796.000, None, None, 23233.149)),
    ("DATA", "Shares to be issued", (None, None, 13980.144, None, None, 13980.144)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (32.065, 87458.748, 13980.144, 575.232, -48352.662, 53693.527)),
    ("DATA", "Loss for the year", (None, None, None, None, -13086, -13086)),
    ("DATA", "Movement in available-for-sale reserve", (None, None, None, -791, None, -791)),
    ("DATA", "Employee share scheme charge", (None, None, None, None, 1389, 1389)),
    ("DATA", "Issue of share capital", (7, 42469, -13980, None, None, 28496)),
    ("DATA", "Shares to be issued", (None, None, 48, None, None, 48)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (39, 129928, 48, -216, -60050, 69749)),
]

bw.add_equity_changes_sheet(
    title="Monument Bank Limited - Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, Company/standalone basis, £'000. "
              "Equity reconciliation ladder confirmed exactly across all 5 years - each year's "
              "own closing balance ties to both the next year's own opening balance and that "
              "year's own Balance Sheet Total equity, with zero plug rows.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=46,
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, Company basis", {}),
    ("DATA", "Gross loans and advances", {"FY2024": 174105, "FY2023": 139876, "FY2022": 93475.759, "FY2021": 761.749}),
    ("DATA", "Less: allowance for impairment on loans and advances", {"FY2024": -266, "FY2023": -187, "FY2022": -104.644, "FY2021": -2.664}),
    ("TOTAL", "Net loans and advances to customers", {"FY2024": 173839, "FY2023": 139689, "FY2022": 93371.115, "FY2021": 759.085}),
    ("SECTION", "Impairment provision (IAS 39 incurred-loss model - no IFRS 9 stage split disclosed)", {}),
    ("DATA", "Individual impairment provision", {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Collective impairment provision", {"FY2024": 266, "FY2023": 187, "FY2022": 104.644, "FY2021": 2.664}),
    ("TOTAL", "Total impairment provision", {"FY2024": 266, "FY2023": 187, "FY2022": 104.644, "FY2021": 2.664}),
    ("DATA", "Impairment charge/(release) recognised in the income statement", {"FY2024": 79, "FY2023": 82.581, "FY2022": 101.980, "FY2021": 2.664}),
    ("DATA", "Coverage ratio (impairment provision / gross loans and advances)", {"FY2024": "0.15%", "FY2023": "0.13%", "FY2022": "0.11%", "FY2021": "0.35%"}),
]

rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Loss for the financial year", {"FY2024": -13086, "FY2023": -19360, "FY2022": -12709.555, "FY2021": -9973.318, "FY2020": -5735.001}),
    ("DATA", "Amortisation charges", {"FY2024": 3538, "FY2023": 2793.918, "FY2022": 2175.212, "FY2021": 128.659}),
    ("DATA", "Depreciation charges", {"FY2024": 95, "FY2023": 69.739, "FY2022": 57.660, "FY2021": 28.517, "FY2020": 11.655}),
    ("DATA", "Finance income", {"FY2020": -8.419}),
    ("DATA", "Impairment charge on loans and advances to customers", {"FY2024": 79, "FY2023": 82.581, "FY2022": 101.980, "FY2021": 2.664}),
    ("DATA", "Employee share scheme charge", {"FY2024": 1389, "FY2023": 608.050, "FY2022": 718.696, "FY2021": 613.561, "FY2020": 347.175}),
    ("DATA", "Increase in loans and advances to customers", {"FY2024": -34229, "FY2023": -46400.642, "FY2022": -92714.010, "FY2021": -761.749}),
    ("DATA", "Increase in customer deposits", {"FY2024": 4079222, "FY2023": 842843.947, "FY2022": 145564.821, "FY2021": 2093.036}),
    ("DATA", "Increase in other assets", {"FY2024": -54, "FY2023": -1418.529, "FY2022": -112.616, "FY2021": -688.421, "FY2020": -182.842}),
    ("DATA", "Increase/(decrease) in other liabilities", {"FY2024": 1465, "FY2023": -256.431, "FY2022": 332.370, "FY2021": -206.864, "FY2020": 1488.636}),
    ("DATA", "Decrease/(increase) in derivative financial instruments", {"FY2024": -642, "FY2023": 2331.057, "FY2022": -2576.137}),
    ("DATA", "Decrease/(increase) in treasury bills", {"FY2024": 130102, "FY2023": -130101.590}),
    ("DATA", "Increase in debt securities", {"FY2024": -843959, "FY2023": -373373.722}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2024": 3323920, "FY2023": 277818.774, "FY2022": 40838.421, "FY2021": -8763.915, "FY2020": -4078.796}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Expenditure on internally generated intangible assets", {"FY2024": -4507, "FY2023": -3417.546, "FY2022": -3256.064, "FY2021": -8307.109, "FY2020": -1301.285}),
    ("DATA", "Purchase of tangible fixed assets", {"FY2024": -192, "FY2023": -72.485, "FY2022": -78.582, "FY2021": -139.569, "FY2020": -28.620}),
    ("DATA", "Purchase of financial investments", {"FY2022": -242.496, "FY2021": -10300}),
    ("DATA", "Interest received", {"FY2020": 8.419}),
    ("TOTAL", "Net cash used in investing activities", {"FY2024": -4699, "FY2023": -3490.041, "FY2022": -3577.142, "FY2021": -18746.678, "FY2020": -1321.486}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Share issuance", {"FY2024": 31183, "FY2023": 23233.150, "FY2022": 1728.142, "FY2021": 25561.125, "FY2020": 9972.572}),
    ("DATA", "Cost of share issuance", {"FY2024": -2687, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0}),
    ("DATA", "Cash inflows from shares to be issued", {"FY2024": 48, "FY2023": 13980.144, "FY2022": 2796, "FY2021": 724.816, "FY2020": 15034.157}),
    ("TOTAL", "Net cash from financing activities", {"FY2024": 28544, "FY2023": 37213.294, "FY2022": 4524.142, "FY2021": 26285.941, "FY2020": 25006.730}),
    ("TOTAL", "Increase/(decrease) in cash and cash equivalents", {"FY2024": 3347765, "FY2023": 311542.027, "FY2022": 41785.421, "FY2021": -1224.652, "FY2020": 19606.448}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2024": 377215, "FY2023": 65673.758, "FY2022": 23888.337, "FY2021": 25112.989, "FY2020": 5506.541}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2024": 3724980, "FY2023": 377215.785, "FY2022": 65673.758, "FY2021": 23888.337, "FY2020": 25112.989}),
]

bw.add_cash_flow_sheet(
    title="Monument Bank Limited - Company Cash Flow Statement",
    subtitle="Company/standalone basis, £'000; 31 December year-end. FY2025 not yet filed. "
              "FY2020 is the Bank's first full annual report, filed post-Banking Licence "
              "(6 Oct 2020) in its pre-revenue mobilisation phase - 'Finance income' and "
              "'Interest received' are that year's own reconciling items (interest accrued "
              "vs. received), not used in later years' presentation.",
    rows=rows, sources_text=CASH_SOURCES, first_col_width=68, source_height=240,
    unit_suffix=" (£'000)",
)

bw.add_asset_quality_sheet(
    title="Monument Bank Limited - Asset Quality",
    subtitle="Company basis, £'000. This Bank applies FRS 102/IAS 39's incurred-loss model, "
              "not IFRS 9 - no Stage 1/2/3 split is disclosed in any year (see source note).",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# KM1 Key Metrics - Monument's own published key-metrics template,
# reproduced whole, in the bank's own row order, row numbers, labels and
# precision. Each year comes from the edition in which it is the REPORTING
# year, never from a later edition's comparative column:
#   FY2023 <- the FY2023 Pillar 3 (p.28), FY2022 <- the FY2022 Pillar 3
#   (p.28), FY2021 <- the FY2021 Pillar 3 (pp.30-31).
# Amounts are printed in SINGLE POUNDS in all three editions (the column
# header is a bare "£"), not £'000 - the unit is carried on each amount row
# rather than on a divider.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available capital", {}),
    ("DATA", "1 Common Equity Tier 1 (CET1) (£, single pounds as printed)", {"FY2023": 28035733, "FY2022": 21299969, "FY2021": 32643538}),
    ("DATA", "1a Fully loaded ECL accounting model CET1 (£, single pounds as printed)", {"FY2023": 28035733, "FY2022": 21299969, "FY2021": 32643538}),
    ("DATA", "2 Tier 1 (£, single pounds as printed)", {"FY2023": 28035733, "FY2022": 21299969, "FY2021": 32643538}),
    ("DATA", "2a Fully loaded ECL accounting model Tier 1 (£, single pounds as printed)", {"FY2023": 28035733, "FY2022": 21299969, "FY2021": 32643538}),
    ("DATA", "3 Total capital (£, single pounds as printed)", {"FY2023": 28035733, "FY2022": 21299969, "FY2021": 32643538}),
    ("DATA", "3a Fully loaded ECL accounting model total capital (£, single pounds as printed)", {"FY2023": 28035733, "FY2022": 21299969, "FY2021": 32643538}),
    ("SECTION", "Risk-weighted assets", {}),
    ("DATA", "4 Total risk-weighted assets (RWA) (£, single pounds as printed)", {"FY2023": 126732992, "FY2022": 48417473, "FY2021": 29951235}),
    ("SECTION", "Risk-based capital ratios as a percentage of RWA", {}),
    ("DATA", "5 Common Equity Tier 1 ratio (%)", {"FY2023": "22.12%", "FY2022": "43.99%", "FY2021": "108.99%"}),
    ("DATA", "5a Fully loaded ECL accounting model Common Equity Tier 1 (%)", {"FY2023": "22.12%", "FY2022": "43.99%", "FY2021": "108.99%"}),
    ("DATA", "6 Tier 1 ratio (%)", {"FY2023": "22.12%", "FY2022": "43.99%", "FY2021": "108.99%"}),
    ("DATA", "6a Fully loaded ECL accounting model Tier 1 ratio (%)", {"FY2023": "22.12%", "FY2022": "43.99%", "FY2021": "108.99%"}),
    ("DATA", "7 Total capital ratio (%)", {"FY2023": "22.12%", "FY2022": "43.99%", "FY2021": "108.99%"}),
    ("DATA", "7a Fully loaded ECL accounting model total capital ratio (%)", {"FY2023": "22.12%", "FY2022": "43.99%", "FY2021": "108.99%"}),
    ("SECTION", "Additional CET1 buffer requirements as a percentage of RWA", {}),
    ("DATA", "8 Capital conservation buffer requirement (2.5% from 2019) (%)", {"FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "9 Countercyclical buffer requirement (%)", {"FY2023": "2.00%", "FY2022": "0%", "FY2021": "0%"}),
    ("DATA", "10 Bank specific buffer requirement (%)", {"FY2023": "0.00%", "FY2022": "0.28%"}),
    ("DATA", "10 Bank G-SIB and/or D-SIB additional requirements (%)", {"FY2021": "0%"}),
    ("DATA", "11 Total of bank CET1 specific buffer requirements (%)", {"FY2023": "4.50%", "FY2022": "2.78%", "FY2021": "2.50%"}),
    ("DATA", "12 CET1 available after meeting the bank's minimum capital requirements (%)", {"FY2023": "18.32%", "FY2022": "35.99%", "FY2021": "100.99%"}),
    ("SECTION", "Basel III leverage ratio", {}),
    ("DATA", "13 Total Basel III leverage ratio exposure measure (£, single pounds as printed)", {"FY2023": 1040727012, "FY2022": 177552754, "FY2021": 36077278}),
    ("DATA", "14 Basel III leverage ratio (%) (row 2 / row 13)", {"FY2023": "4.08%", "FY2022": "12.00%", "FY2021": "90.48%"}),
    ("DATA", "14a Fully loaded ECL accounting model Basel III leverage ratio (%)", {"FY2023": "4.08%", "FY2022": "12.00%", "FY2021": "90.48%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15 Total high-quality liquid assets (HQLA) (£, single pounds as printed)", {"FY2023": 489275319, "FY2022": 70879649, "FY2021": 10300000}),
    ("DATA", "16 Total net cash outflow (£, single pounds as printed)", {"FY2023": 44771829, "FY2022": 699861, "FY2021": 0.36}),
    ("DATA", "17 LCR (%)", {"FY2023": "1,093%", "FY2022": "10,128%", "FY2021": "2,861,111,111.11%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18 Total available stable funding (£, single pounds as printed)", {"FY2023": 914948708, "FY2022": 160835001, "FY2021": 34625872}),
    ("DATA", "19 Total required stable funding (£, single pounds as printed)", {"FY2023": 385273385, "FY2022": 66227130, "FY2021": 22572338}),
    ("DATA", "20 NSFR (%)", {"FY2023": "237.48%", "FY2022": "242.85%", "FY2021": "153.40%"}),
]

bw.add_km1_sheet(
    title="Monument Bank Limited - KM1 Key Metrics",
    subtitle="Monument's own published key-metrics template (section 11 'Key Metrics' of each Pillar 3 "
             "document), reproduced whole in the bank's own row order, row numbers, labels and precision. "
             "AMOUNTS ARE IN SINGLE POUNDS, as printed - the source column header is a bare '£', not "
             "£'000 - so each amount row carries that unit in its own label; ratio rows are percentages. "
             "Only FY2023, FY2022 and FY2021 are populated, and each comes from the edition in which that "
             "year is the reporting year, never from a later edition's comparative column. FY2024, FY2025 "
             "and FY2020 are blank because no KM1 column for those dates exists in any edition anywhere "
             "(see the source note).",
    rows=km1_rows,
    sources_text=P3_SOURCES + "\n\n" + (
        "KM1 SHEET SOURCES - one edition per column, per this project's own-year sourcing rule:\n"
        f"FY2023: Monument Bank Pillar 3 Disclosures for the year ended 31 December 2023, section 11 "
        f"'Key Metrics', p.28 - {P3_23_URL}\n"
        f"FY2022: Monument Bank Pillar 3 Disclosures for the Year Ended 31 December 2022, section 11 "
        f"'Key Metrics', p.28 - {P3_22_URL}\n"
        f"FY2021: Monument Bank Pillar 3 Disclosures for the year ended 31 December 2021, section 11 "
        f"'Key Metrics', pp.30-31 (the table breaks across two pages: rows 1-12 on p.30, rows 13-20 on "
        f"p.31) - {P3_21_URL}\n\n"
        "WHY FY2024, FY2025 AND FY2020 ARE BLANK - three different reasons, none of them a sourcing gap.\n"
        "FY2024 and FY2025: Monument became a Small Domestic Deposit Taker on 15 January 2025 (PRA "
        "register, Rule 3.1 of the SDDT Regime - General Application Part; see the SDDT note above), which "
        "removed the obligation to publish Pillar 3 disclosures as at 31 December 2024. No FY2024 or FY2025 "
        "Pillar 3 document exists or will exist, Monument's own annual-reports page lists none, and no "
        "later edition prints a comparative column for either date - so there is no published KM1 column "
        "for those years on any basis.\n"
        "FY2020: predates Monument's first Pillar 3 document entirely (the Bank was in its post-licence "
        "mobilisation phase), and the FY2021 edition is a SINGLE-COLUMN table carrying 2021 only, so it "
        "prints no 2020 comparative either. Nothing has been back-filled from the annual reports, which "
        "are a different basis.\n\n"
        "TWO ROWS NUMBERED 10, DELIBERATELY NOT MERGED. The FY2023 and FY2022 editions print row 10 as "
        "'Bank specific buffer requirement'; the FY2021 edition prints row 10 as 'Bank G-SIB and/or D-SIB "
        "additional requirements (%)'. Same row number, different captions and different metrics, so they "
        "are kept as two rows rather than combined into one series.\n\n"
        "PRECISION IS THE BANK'S OWN. Row 17's FY2021 value is printed as 2,861,111,111.11% in the FY2021 "
        "edition and as 2,861,111,111% in the FY2022 edition's comparative column; this sheet carries the "
        "FY2021 edition's own two-decimal figure, and the LCR metric sheet carries the whole-number form. "
        "Neither is adjusted to match the other. The extreme value is genuine and is explained on the "
        "Leverage Ratio and LCR sheets: the Bank held a full capital base against an almost empty balance "
        "sheet, with a total net cash outflow of £0.36.\n\n"
        "KNOWN DISAGREEMENTS WITH THE SINGLE-METRIC SHEETS, all pre-existing and all documented rather "
        "than reconciled. This sheet reproduces the Pillar 3 documents; the Total RWAs, CET1 Ratio and "
        "NSFR sheets carry the FY2024 annual report's restated FY2023 figures so that FY2023 sits on the "
        "same basis as FY2024 beside it. So for FY2023 this sheet shows RWA 126,732,992 against the Total "
        "RWAs sheet's 126,528 (£'000), CET1 ratio 22.12% against 22%, and NSFR 237.48% against 228%. Each "
        "pair is two correctly-transcribed figures from two different documents - see those sheets' own "
        "notes, which carry the same divergence in the other direction."
    ),
    first_col_width=72,
    source_height=300,
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=56, source_height=180)

def vals(data):
    return {y: data.get(y) for y in YEARS}

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", vals({"FY2024": 56324, "FY2023": 28035.733, "FY2022": 21299.969, "FY2021": 32643.538, "FY2020": 23895.804}))], "FY2020 is the 2020 comparative column of the FY2021 report's own 'Regulatory capital' table (Note 20) and its Strategic Report KPI table, which labels the same figure 'Common Equity Tier 1 (CET1) capital'.")
metric("CET1 Ratio", "%", [("Common Equity Tier 1 (CET1) ratio", vals({"FY2024": "20%", "FY2023": "22%", "FY2022": "43.99%", "FY2021": "108.99%"}))], "FY2024 is the FY2024 annual report's regulatory metrics table ('CET 1 %', p.9). FY2023 is the same table's 2023 comparative; the FY2023 Pillar 3 states the same ratio to two decimals as 22.12% (KM1 item 5), the small difference coming from the FY2024 report's restated FY2023 RWA denominator - see the Total RWAs sheet. FY2022 and FY2021 are KM1 item 5 of the FY2022 and FY2021 Pillar 3 documents, added 2026-09-15; the previous note's claim that 'earlier ratios were not separately disclosed' was a Companies-House-only search artefact. Both Pillar 3 ratios reproduce exactly from that year's own disclosed capital and RWA: 21,299,969/48,417,473 = 43.99% and 32,643,538/29,951,235 = 108.99%.")
metric("Tier 1 Capital", "£'000", [("Total Tier 1 capital", vals({"FY2024": 56324, "FY2023": 28035.733, "FY2022": 21299.969, "FY2021": 32643.538, "FY2020": 23895.804}))], "Directly disclosed: every annual report from FY2020 onward carries a 'Regulatory capital' table whose bottom line is labelled 'Total Tier 1 capital'. The amounts equal the CET1 Capital sheet's figures because the table builds Tier 1 solely from ordinary share capital and share premium (plus, from FY2023, the AFS reserve less PruVal adjustment) less accumulated losses and intangible-asset deductions - no Additional Tier 1 instrument is disclosed in any year.")
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", vals({"FY2023": "22.12%", "FY2022": "43.99%", "FY2021": "108.99%"}))], "Added 2026-09-15, overturning the previous 'no standalone Tier 1 ratio was separately disclosed in the reports reviewed' - that was true of the annual reports but the standalone Pillar 3 documents carry the ratio explicitly as KM1 item 6, 'Tier 1 ratio (%)', for all three years they cover. The figures equal the CET1 ratios because Monument's capital base is entirely CET1 in every year (no Additional Tier 1 and no Tier 2 instrument is disclosed anywhere), which the Pillar 3 KM1 tables show directly by printing identical values for items 5, 6 and 7 - this is the disclosed position, not a derivation. FY2024 and FY2020 remain blank: neither year has a Pillar 3 document and neither annual report states a Tier 1 ratio.")
metric("Total Capital", "£'000", [("Total capital", vals({"FY2024": 56324, "FY2023": 28035.733, "FY2022": 21299.969, "FY2021": 32643.538, "FY2020": 23895.804}))], "Shown equal to Total Tier 1 capital on the strength of the reports' own explicit statement, repeated verbatim each year, that the capital base consists entirely of Tier 1 - e.g. 'As at 31 December 2024, our capital base was made up of £56.3 million of Tier 1 capital (2023: £28.0 million)'. No Tier 2 row appears in any year's 'Regulatory capital' table and no Tier 2 instrument is disclosed anywhere in the reports, although the Bank's stated capital policy permits Tier 2 up to 25% of total capital. This is the disclosed composition, not a derived figure.")
metric("Total Capital Ratio", "%", [("Total capital ratio", vals({"FY2023": "22.12%", "FY2022": "43.99%", "FY2021": "108.99%"}))], "CORRECTED 2026-09-15 - this sheet previously read FY2022 44%, FY2021 529%, FY2020 359%. The FY2021 and FY2020 values were not CRR total capital ratios at all and have been withdrawn. Monument's annual reports use the abbreviation 'TCR' for two different things in different years, and the two earlier reports use it in the PRA sense of Total Capital Requirement. The FY2020 report states 'As at 31st December 2020, our Total Capital Ratio (TCR) was 359% (2019 453%)' and the FY2021 report's KPI table prints 'Total capital ratio (TCR) 529% 359%' - these are capital-resources-to-capital-requirement cover ratios, not capital as a percentage of RWA. The FY2021 Pillar 3, KM1 item 7, gives the actual CRR total capital ratio for FY2021 as 108.99%, which reproduces exactly from that document's own figures (32,643,538 total capital / 29,951,235 total RWA) and is what now sits in the FY2021 cell. From the FY2022 report onward 'TCR' reverts to the CRR meaning: the FY2023 report's '22% (2022: 44%)' agrees with KM1 item 7 of the FY2023 and FY2022 Pillar 3 documents (22.12% and 43.99%), and those two-decimal Pillar 3 values are used here. FY2020 is now blank: Monument published no Pillar 3 for FY2020, the FY2020 report discloses no RWA figure at all, and the only ratio it gives is the cover ratio - so no CRR total capital ratio exists for that year and none may be computed. FY2024 is blank for the same reason on the other end: no FY2024 Pillar 3 (SDDT) and the FY2024 report states only the CET1 ratio.")
metric("Total RWAs", "£'000", [("Total risk-weighted assets", vals({"FY2024": 281756, "FY2023": 126528, "FY2022": 48417.473, "FY2021": 29951.235}))], "FY2024 and FY2023 are the FY2024 report's regulatory metrics table (p.9). FY2022 and FY2021 are KM1 item 4 of the FY2022 and FY2021 Pillar 3 documents, added 2026-09-15 - the previous note's 'earlier totals were not separately disclosed' was wrong, they are disclosed, just not at Companies House. TWO-SOURCE DIVERGENCE ON FY2023, recorded rather than resolved: the FY2023 Pillar 3 states Total RWA of 126,732.992 (£'000), while the FY2024 annual report's 2023 comparative states 126,528 - a difference of 205, or 0.16%. The cell holds the annual report figure so that it stays on the same basis as FY2024 beside it, and because the Pillar 3 components behind 126,732.992 differ from the annual report's by risk category as well as in total (see the RWA Breakdown sheet, which carries both splits side by side in separate blocks rather than mixing them in one row). The divergence is a restatement in the later document, not a transcription error: both figures were read from their own source and both reconcile internally to their own components. Neither has been adjusted.")

rwa_breakdown_rows = [
    ("SECTION", "Annual report basis - 'Balance sheet and regulatory metrics' table (Company, as disclosed)", {}),
    ("DATA", "Counterparty and credit risk weighted assets (RWA)", {"FY2024": 270331, "FY2023": 112159}),
    ("DATA", "Operational RWA", {"FY2024": 9755, "FY2023": 11500}),
    ("DATA", "Credit valuation adjustment RWA", {"FY2024": 1670, "FY2023": 2869}),
    ("TOTAL", "Total RWAs (annual report basis)", {"FY2024": 281756, "FY2023": 126528}),
    ("SECTION", "Pillar 3 basis - section 6.1 'Pillar 1 Capital requirements', standardised approach exposure classes", {}),
    ("DATA", "Central governments or central banks", {"FY2021": 0}),
    ("DATA", "Regional governments or local authorities", {"FY2021": 0}),
    ("DATA", "Public sector entities", {"FY2021": 0}),
    ("DATA", "Multilateral development banks", {"FY2021": 0}),
    ("DATA", "International organisations", {"FY2021": 0}),
    ("DATA", "Institutions", {"FY2023": 5453.118, "FY2022": 957.321, "FY2021": 3322.447}),
    ("DATA", "Corporates", {"FY2023": 0, "FY2022": 0, "FY2021": 1455.220}),
    ("DATA", "Retail", {"FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Secured by mortgages on immovable property", {"FY2023": 51992.602, "FY2022": 32877.923, "FY2021": 265.680}),
    ("DATA", "Exposures in default", {"FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Items associated with particular high risk", {"FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Covered bonds", {"FY2023": 2946.049, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Securitisations", {"FY2023": 47763.684, "FY2022": 0}),
    ("DATA", "Claims on institutions and corporates with a short-term credit assessment", {"FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Collective investment undertakings (CIU)", {"FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Equity", {"FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Other items", {"FY2023": 4273.789, "FY2022": 3083.899, "FY2021": 1129.857}),
    ("TOTAL", "Total credit risk RWA", {"FY2023": 112429.242, "FY2022": 36919.143, "FY2021": 6173.204}),
    ("DATA", "Credit valuation adjustment", {"FY2023": 1785.000, "FY2022": 0}),
    ("DATA", "Operational risk - basic indicator approach", {"FY2023": 12518.750, "FY2022": 11498.330, "FY2021": 23778.032}),
    ("TOTAL", "Total Pillar 1 risk-weighted assets (Pillar 3 basis)", {"FY2023": 126732.992, "FY2022": 48417.473, "FY2021": 29951.235}),
]

bw.add_rwa_breakdown_sheet(
    title="Monument Bank Limited - RWA Breakdown",
    subtitle="Company basis, £'000. Two blocks, deliberately kept separate because they are two "
              "different disclosures on two different bases, and the years they cover overlap. "
              "The first block is the three-way risk-type split (counterparty & credit / "
              "operational / credit valuation adjustment) from the FY2024 annual report's own "
              "regulatory metrics table, covering FY2024 and FY2023. The second block is the "
              "full standardised-approach exposure-class breakdown from section 6.1 of the "
              "FY2023, FY2022 and FY2021 Pillar 3 documents, added 2026-09-15. Each block sums "
              "exactly to its own total in every year it covers, and no market risk RWA line "
              "appears in either - so both are complete breakdowns, not partial ones. The two "
              "blocks disagree about FY2023 and that disagreement is shown rather than "
              "reconciled away: see the source note. FY2020 has no breakdown on either basis.",
    rows=rwa_breakdown_rows,
    sources_text=P3_SOURCES + "\n\n" + (
        "RWA BREAKDOWN SOURCES:\n"
        f"FY2024 & FY2023 (Company basis, matching the Total RWAs sheet's own FY2024/FY2023 "
        "figures exactly: 270,331 + 9,755 + 1,670 = 281,756 for FY2024; 112,159 + 11,500 + "
        "2,869 = 126,528 for FY2023): Financial Statements for the year ended 31 December "
        "2024, Strategic Report, 'Balance sheet and regulatory metrics' table, p.9 - "
        f"{AR25_URL}\n\n"
        "PILLAR 3 BLOCK - exposure-class breakdown, section 6.1 'Pillar 1 Capital "
        "requirements' (the Risk Weighted Assets column; the adjacent Capital Requirements "
        "column is 8% of it and is not reproduced here). Figures are printed in whole pounds "
        "in the source and are shown here in £'000:\n"
        f"FY2023 (and its FY2022 comparative), p.24 - {P3_23_URL}\n"
        f"FY2022 (and its FY2021 comparative), p.23 - {P3_22_URL}\n"
        f"FY2021, p.25 - {P3_21_URL}\n"
        "Each year reconciles to KM1 item 4 in the same document: FY2023 112,429,242 + "
        "1,785,000 + 12,518,750 = 126,732,992; FY2022 36,919,143 + 11,498,330 = 48,417,473; "
        "FY2021 6,173,204 + 23,778,032 = 29,951,236 against a printed total of 29,951,235 "
        "(a £1 rounding in the source, reproduced as printed, not adjusted).\n"
        "A zero in this block means the source prints a dash for that exposure class in that "
        "year, i.e. a disclosed nil. A blank means the row does not appear in that year's "
        "table at all: the FY2021 table has no Securitisations line and no Credit Valuation "
        "Adjustment line, and the FY2022 table has no Securitisations line - the FY2022 "
        "figures for those two rows come from the FY2023 document's 2022 comparative column, "
        "where both are printed as nil. Conversely the five sovereign-type classes at the top "
        "of the block are printed only in the FY2021 table, all nil; the FY2022 and FY2023 "
        "tables drop them. No value in this block has been inferred from a total.\n\n"
        "WHY THE TWO BLOCKS DISAGREE ABOUT FY2023. The FY2024 annual report restates FY2023, "
        "and its restated split does not match the FY2023 Pillar 3's. Total RWA: 126,528 "
        "(annual report) against 126,732.992 (Pillar 3), 0.16% apart. The components move "
        "more than the total does - credit 112,159 against 112,429.242, operational 11,500 "
        "against 12,518.750, CVA 2,869 against 1,785.000 - so this is not a rounding "
        "difference but a genuine restatement, with the largest single move being CVA. Both "
        "figures were read from their own primary source and each reconciles internally to "
        "its own total. Neither has been adjusted, averaged or dropped, and the two are not "
        "mixed within any row. The Total RWAs sheet carries the annual report figure for "
        "FY2023 so that it sits on the same basis as FY2024 next to it; this sheet shows both.\n\n"
        "CORRECTION 2026-09-15: this note previously stated that 'no breakdown of Total RWAs "
        "by risk category was found for FY2022 or earlier' and called it 'a genuine "
        "non-disclosure for FY2022 and earlier, not an access gap'. Both claims were wrong. "
        "The breakdown is disclosed for FY2021, FY2022 and FY2023, in more detail than the "
        "annual report's three-way split, in standalone Pillar 3 documents published on "
        "Monument's own website rather than filed at Companies House. The earlier pass read "
        "the Companies House filings exhaustively, which is why it found nothing - the "
        "documents it needed were never going to be there."
    ),
    first_col_width=54,
    source_height=220,
)

metric("Leverage Ratio", "%", [("Leverage ratio", vals({"FY2024": "3.9%", "FY2023": "4.1%", "FY2022": "12.00%", "FY2021": "90.48%"}))], "FY2024 and FY2023 are the FY2024 report's regulatory metrics table (p.9). FY2022 and FY2021 are KM1 item 14, 'Basel III leverage ratio (%) (row 2 / row 13)', of the FY2022 and FY2021 Pillar 3 documents, added 2026-09-15. Same definition throughout - Tier 1 capital over the Basel III total leverage exposure measure - and the FY2023 Pillar 3 states 4.08% against the annual report's 4.1%, i.e. the same figure at a different rounding, which is what confirms the two sources share a basis here. The very high FY2021 ratio is as printed: the Bank had a £36.1m exposure measure against £32.6m of Tier 1 capital, having received its banking licence on 4 November 2021 and taken its first deposit on 6 December 2021, so it was carrying a full capital base against almost no balance sheet. FY2020 is blank - no leverage ratio is stated in that year's report and there is no FY2020 Pillar 3.")
metric("LCR", "%", [("Liquidity coverage ratio", vals({"FY2024": "589%", "FY2023": "1,093%", "FY2022": "10,128%", "FY2021": "2,861,111,111%"}))], "FY2021’s unusually high percentage is reproduced exactly as printed in the 2021 accounts; it is not normalised or inferred.")
metric("NSFR", "%", [("Net stable funding ratio", vals({"FY2024": "560%", "FY2023": "228%", "FY2022": "242.85%", "FY2021": "153.40%"}))], "FY2024 and FY2023 are the FY2024 report's regulatory metrics table (p.9). FY2022 and FY2021 are KM1 item 20 of the FY2022 and FY2021 Pillar 3 documents, added 2026-09-15, each supported in the same table by its own available and required stable funding amounts (FY2022 160,835,001/66,227,130; FY2021 34,625,872/22,572,338), which reproduce the printed ratios. FY2021 predates the UK NSFR requirement, which came into force on 1 January 2022 under PRA PS17/21 - Monument disclosed the ratio voluntarily a year early, so this is a real disclosure rather than the structural blank that FY2021 NSFR usually is across this workbook set. TWO-SOURCE DIVERGENCE ON FY2023, recorded rather than resolved: the FY2023 Pillar 3 states 237.48% where the FY2024 annual report's 2023 comparative states 228%, a gap of 9.5 percentage points that is too large to be rounding. Neither document states which convention it uses, so the divergence cannot be attributed with confidence - point-in-time against four-quarter-average is the usual cause of a gap this shape, and the later document restates FY2023 RWA too (see the Total RWAs sheet), so a restatement is equally possible. The cell holds the annual report figure to stay on the same basis as FY2024 beside it; the Pillar 3 figure is recorded here and neither is adjusted.")
metric("MREL Ratio", None, [("MREL ratio", vals({y: "Not applicable" for y in ["FY2023", "FY2022", "FY2021"]}))], "CHANGED 2026-09-15 from blank to an explicit 'Not applicable' for the three years Monument published a Pillar 3 document, because those documents answer the question directly rather than leaving it open. Section 10 of each, 'Minimum Requirement for Own Funds and Eligible Liabilities', states that Monument falls under a Modified Insolvency process - the Bank of England applies this where a firm provides fewer than roughly 40,000 to 80,000 transactional accounts and its failure would not disrupt the wider financial system - and that 'under [which] minimum requirement for own funds and eligible liabilities (MREL) is set at the same level as regulatory capital requirements and so the Bank will meet its MREL by meeting existing regulatory capital requirements as described in Section 6 Capital Requirements.' Monument therefore has no MREL requirement distinct from its capital requirement and no separate MREL ratio exists to disclose. This is a structural non-applicability, not a sourcing gap: the earlier note, 'no quantitative MREL ratio was located in the official annual reports reviewed', was accurate about the annual reports but left the reader unable to tell an unresearched blank from a real absence. FY2024, FY2025 and FY2020 are left blank rather than marked not applicable, because no document covering those years makes the statement - although nothing suggests Monument's resolution strategy has changed.")

def row_values(label):
    return next(values for kind, name, values in rows if name == label)

def bs_value(label):
    return next(values for kind, name, values in bs_rows if name == label)

def pl_value(label):
    return next(values for kind, name, values in pl_rows if name == label)

equity_summary = {
    "FY2020": {"Opening equity": 5578.186, "Total comprehensive loss for the year": -5735.001, "Other equity movements, net": 25353.904, "Closing equity": 25197.089},
    "FY2021": {"Opening equity": 25197.089, "Total comprehensive loss for the year": -9973.318, "Other equity movements, net": 26899.502, "Closing equity": 42123.273},
    "FY2022": {"Opening equity": 42123.273, "Total comprehensive loss for the year": -12709.555, "Other equity movements, net": 5242.838, "Closing equity": 34656.556},
    "FY2023": {"Opening equity": 34656.556, "Total comprehensive loss for the year": -18784.372, "Other equity movements, net": 37821.343, "Closing equity": 53693.527},
    "FY2024": {"Opening equity": 53693.527, "Total comprehensive loss for the year": -13878, "Other equity movements, net": 29933.473, "Closing equity": 69749},
}

bw.add_overview_sheet(
    cash_flow_totals=[(label, row_values(label)) for label in [
        "Net cash from/(used in) operating activities",
        "Net cash used in investing activities",
        "Net cash from financing activities",
        "Cash and cash equivalents at end of year",
    ]],
    cash_flow_unit="£'000",
    balance_sheet_totals=[(label, bs_value(label)) for label in [
        "Total assets",
        "Loans and advances to customers",
        "Customer deposits",
        "Total equity",
    ]],
    balance_sheet_unit="£'000",
    income_statement_totals=[(label, pl_value(label)) for label in [
        "Total net income/(expense)",
        "Administrative expenses",
        "Operating loss before taxation",
        "Loss for the financial year",
    ]],
    income_statement_unit="£'000",
    equity_changes_totals=[
        (label, {y: equity_summary[y].get(label) for y in YEARS if y in equity_summary})
        for label in ["Opening equity", "Total comprehensive loss for the year", "Other equity movements, net", "Closing equity"]
    ],
    equity_changes_unit="£'000",
    ratios=[
        ("CET1 Ratio", vals({"FY2024": "20%", "FY2023": "22%", "FY2022": "43.99%", "FY2021": "108.99%"})),
        ("Total Capital Ratio", vals({"FY2023": "22.12%", "FY2022": "43.99%", "FY2021": "108.99%"})),
        ("Leverage Ratio", vals({"FY2024": "3.9%", "FY2023": "4.1%", "FY2022": "12.00%", "FY2021": "90.48%"})),
        ("LCR", vals({"FY2024": "589%", "FY2023": "1,093%", "FY2022": "10,128%", "FY2021": "2,861,111,111%"})),
        ("NSFR", vals({"FY2024": "560%", "FY2023": "228%", "FY2022": "242.85%", "FY2021": "153.40%"})),
    ],
    note="Monument Bank Limited standalone/Company basis. FY2025 is blank because the latest available Companies House accounts cover 31 December 2024. FY2020 is the Bank's real historical floor (first full annual report, post-Banking Licence, pre-revenue) - FY2017-FY2019 are self-skipped in full because the entity was a pre-authorisation shell company with no bank-relevant disclosure (see Balance Sheet sheet's source note). Pillar 3 sheets contain only explicitly disclosed annual regulatory values; blank cells mean not disclosed. FY2021-FY2023 ratios are from Monument's own standalone Pillar 3 documents (found 2026-09-15), FY2024 from the annual report - the two sources diverge on FY2023 NSFR and Total RWAs and both figures are kept, on the relevant detail sheets. The FY2021 and FY2020 Total Capital Ratio figures previously shown here (529% and 359%) were capital-cover ratios, not CRR ratios, and have been withdrawn or replaced - see the Total Capital Ratio sheet.",
)

bw.save("/Users/armaan/code/katalysis/banks/MONUMENT BANK FINANCIALS.xlsx")
