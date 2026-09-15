import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = [
    "FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
    "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014",
    "FY2013", "FY2012", "FY2011", "FY2010", "FY2009", "FY2008",
]
Y_CORE = YEARS[:YEARS.index('FY2014') + 1]  # HD-072/075/079: FY2014-floor default for Pillar 3/Asset Quality/RWA Breakdown/Overview


P3_URLS = {
    "FY2026": "https://www.icicibank.co.uk/content/dam/icicibank-revamp/uk/doc/basel-pillar-3-disclosures-FY2026.pdf",
    "FY2025": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/basel-pillar-3-disclosures-FY2024-25.pdf",
    "FY2024": "https://www.icicibank.co.uk/content/dam/icicibank/india/managed-assets/docs/pdf/basel-pillar-3-disclosures-FY2023-24.pdf",
    "FY2023": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/icici-bank-uk-plc-pillar-3-disclosures-FY2022-23.pdf",
    "FY2022": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/ICICI-Bank-UK-Plc-Pillar3-disclosures-FY2021-22.pdf",
    "FY2021": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/ICICI-Bank-UK-Plc-Pillar3-disclosures-FY2020-21.pdf",
    "FY2020": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/ICICI_Bank_UK_Pillar3_disclosures_FY2019-20.pdf",
    "FY2019": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/ICICI_Bank_UK_Pillar3_disclosures_FY2018-19.pdf",
    "FY2018": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/basel3-disclosures-FY17-18.pdf",
    "FY2017": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/basel3-disclosures-FY16-17.pdf",
    "FY2016": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/basel3-disclosures-FY15-16.pdf",
    "FY2015": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/basel3-disclosures-FY14-15.pdf",
    "FY2014": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/disclosures2013-14.pdf",
}

# Basel II era. Kept separate from P3_URLS because these are a DIFFERENT REGIME, not just
# older editions of the same template: BIPRU 11 / Basel II, not CRR / Basel III. Each of the
# six was downloaded, opened and read in full on 2026-09-15; see BASEL2_NOTE below for what
# they do and do not contain. Dated from the COVER PAGE of each document, never the filename -
# `basel2_disclosures_March31_11.pdf` is the year ended March 31, 2012, not 2011.
P3_BASEL2_URLS = {
    "FY2013": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/disclosures2012-13.pdf",
    "FY2012": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/basel2_disclosures_March31_11.pdf",
    "FY2011": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/basel2_disclosures_FY10_11.pdf",
    "FY2010": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/basel2_disclosures_FY09_10.pdf",
    "FY2009": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/Basel_II_p3_Disclosure_Statement.pdf",
    "FY2008": "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/basel2_disclosures_FY2008.pdf",
}

# Credit-risk Pillar 1 CAPITAL REQUIREMENT totals (USD million) printed in the Basel II
# editions. Recorded here for traceability only - deliberately NOT converted into an RWA
# figure for any sheet, because unlike the FY2014-FY2020 Basel III editions these documents
# disclose no operational-risk and no market-risk capital requirement, so there is no printed
# total to convert. See BASEL2_NOTE.
BASEL2_CREDIT_RISK_PILLAR1_REQUIREMENT = {
    "FY2013": 241.69, "FY2012": 260.31, "FY2011": 402.24,
    "FY2010": 459.49, "FY2009": 426.62, "FY2008": 335.02,
}

BASEL2_NOTE = (
    "FY2008-FY2013 - BASEL II ERA, KEY METRICS NOT DISCLOSED (enumerated, not merely unfound). "
    "The Bank published an annual Pillar 3 disclosure for every one of these years and all six "
    "were downloaded, cover-date-verified and read in full on 2026-09-15. They are short "
    "(10 pages each) BIPRU Chapter 11 / Basel II documents, a different regulatory regime from "
    "the CRR / Basel III disclosures used for FY2014 onward, and they contain NO capital "
    "resources table, NO Tier 1 / Tier 2 / total capital figure, NO capital ratio, NO total "
    "risk-weighted assets, NO leverage ratio, NO LCR and NO NSFR. Their only capital content is "
    "a table captioned 'the Bank's Pillar 1 capital requirement by each of the standardised "
    "credit risk exposure classes' - credit risk ONLY, with no operational-risk or market-risk "
    "capital requirement anywhere in the document. Those printed credit-risk Pillar 1 capital "
    "requirement totals are, in USD million: "
    + ", ".join(f"{y} {BASEL2_CREDIT_RISK_PILLAR1_REQUIREMENT[y]:.2f}" for y in
                ("FY2013", "FY2012", "FY2011", "FY2010", "FY2009", "FY2008"))
    + ". They are recorded here for traceability and are deliberately NOT converted to an RWA "
    "figure: the FY2014-FY2020 'capital requirement / 8%' conversion used elsewhere in this "
    "workbook starts from a printed TOTAL Pillar 1 requirement covering all three risk types, "
    "which these documents do not provide, so the same conversion here would silently understate "
    "RWA by the missing operational-risk and market-risk components. No key-metric cell is "
    "therefore filled for FY2008-FY2013, and none can be from Pillar 3. Documents (dated from "
    "each cover page, NOT from the filename - "
    "`basel2_disclosures_March31_11.pdf` is the year ended March 31, 2012, not 2011): "
    + "; ".join(f"{y} - {P3_BASEL2_URLS[y]}" for y in
                ("FY2013", "FY2012", "FY2011", "FY2010", "FY2009", "FY2008"))
    + ". Entity confirmed on each: every one opens \"ICICI Bank UK PLC ('the Bank') ... a wholly "
    "owned subsidiary of ICICI Bank Limited\", states \"The disclosures have been prepared for "
    "ICICI Bank UK PLC\", and expressly distinguishes itself from \"the consolidated Basel II - "
    "Pillar 3 Disclosures made by ICICI Bank Limited ('the Parent Bank')\" - no parent-group "
    "figure is present in any of them."
)

AR2026_URL = "https://www.icicibank.co.uk/content/dam/icicibank-revamp/uk/doc/financial-report-FY2026.pdf"
AR2025_URL = "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/financial-report-uk-FY2025.pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MzQzNDA3NTE5MmFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MzM5Mjc5MzA4M2FkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MzM0NjUxNzQwNmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MzMwMTQ3NjY0OGFkaXF6a2N4/document?format=pdf&download=0"
AR2020_URL = "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/financial-report-19-20.pdf"
AR2019_URL = "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/financial-report-18-19.pdf"
AR2018_URL = "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/financial-report-17-18.pdf"
AR2017_URL = "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/financial-report-16-17.pdf"
AR2016_URL = "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/financial-report-15-16.pdf"
AR2015_URL = "https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/financial-report-14-15.pdf"
AR2014_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MzEwMDE3NDY1OGFkaXF6a2N4/document?format=pdf&download=0"
AR2013_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MzA3ODM0MTM2NGFkaXF6a2N4/document?format=pdf&download=0"
AR2012_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MzA1NzY0MjQxOGFkaXF6a2N4/document?format=pdf&download=0"
AR2011_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MzAzNjcwNDYwOGFkaXF6a2N4/document?format=pdf&download=0"
AR2010_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MzAyMTI3MzU1MGFkaXF6a2N4/document?format=pdf&download=0"
AR2009_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MjAzNTc0MTU4N2FkaXF6a2N4/document?format=pdf&download=0"
AR2008_URL = "https://find-and-update.company-information.service.gov.uk/company/04663024/filing-history/MjAwNzk0MTQ0MGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: ICICI Bank UK Plc (Companies House 04663024, FRN 223268, LEI "
    "2138002XB6T14IGKGU43) is the UK-incorporated PRA-authorised bank entity. "
    "Companies House confirms it is an active public limited company, incorporated "
    "11 February 2003, with accounts filed at Companies House through 31 March 2025; the FY2026 (year ended 31 March 2026) Annual Report and Pillar 3 disclosure are published on the Bank's own website and were used for FY2026, ahead of that year's Companies House filing. The official Basel "
    "disclosures identify the reporting entity as ICICI Bank UK PLC and present the "
    "UK KM1 data on a standalone Bank basis in USD millions. No parent-group figures "
    "have been substituted."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: ICICI Bank UK Plc applies the FRS 101 reduced-"
    "disclosure framework and does not prepare a separate Statement of Cash Flows. "
    "This is therefore a Pillar-3-only workbook; the Cash Flow Statement sheet is "
    "retained to document the exemption rather than substituting parent-group cash flows. "
    f"Official supporting source: ICICI Bank UK PLC Strategic report, Directors' report "
    f"and financial statements for the year ended 31 March 2025, cash-flow exemptions "
    f"section (c) - {AR2025_URL}. "
    f"For FY2008-FY2015 the Bank's own Annual Report instead cites the equivalent exemption "
    f"under FRS 1 (the pre-FRS 101/102 UK GAAP standard then in force) - same substantive "
    f"exemption, different accounting-standard citation; confirmed in the FY2015 Annual Report's "
    f"own 'Cash flow exemptions' note (d) - {AR2015_URL} - and independently confirmed in the "
    f"FY2008 Annual Report's own note 3(b) 'Cash flow statement', which cites 'the exemption "
    f"available within FRS 1 (revised), \"Cash Flow Statements\"' in identical substance - "
    f"{AR2008_URL}. The intervening years (FY2009-FY2013) were not individually checked for this "
    f"specific note's wording during HD-075 (only their primary statements were transcribed) - "
    f"no basis-shift is expected given both endpoints of the range cite FRS 1, but this is flagged "
    f"rather than assumed."
)


STATEMENTS_ENTITY_NOTE = (
    "STATEMENTS ENTITY NOTE: the Bank's Balance Sheet, Profit & Loss, Statement of Changes "
    "in Equity, Asset Quality, and RWA Breakdown sheets are presented in USD (the Bank's own "
    "and sole primary reporting currency in every source document reviewed - each Annual "
    "Report and Pillar 3 disclosure gives only an unaudited INR 'convenience translation' "
    "alongside the USD primary figures; no GBP figures are published anywhere by this Bank). "
    "Kept in USD throughout (not converted to £) for consistency with the workbook's own "
    "pre-existing Pillar 3 metric sheets, which are also USD million. "
    + ENTITY_NOTE
)

STATEMENTS_SOURCES = (
    "Sources - ICICI Bank UK Plc's own Annual Reports (own website unless noted; Companies House "
    "filings for FY2024/23/22/21/14, text-native except FY2014 which is a scanned/non-text filing "
    "read page-by-page):\n"
    f"FY2026: Strategic report, Directors' report and financial statements, year ended 31 March "
    f"2026, Profit and loss account p.32 / Statement of other comprehensive income p.33 / Balance "
    f"sheet p.34 / Statement of change in equity p.36 / Note 19 'Potential credit risk on financial "
    f"instruments' p.61 - {AR2026_URL}. Published on the Bank's own website; the Companies House "
    f"filing history for 04663024 still shows 31 March 2025 as the latest accounts filed, so this "
    f"is the Bank's own published source rather than a Companies House copy. Added 2026-09-15. "
    f"Every FY2026 statement was verified to foot internally (Total assets USD 2,908,251k = Total "
    f"Liabilities USD 2,550,469k + Total Equity USD 357,782k; the equity roll-forward from the "
    f"1 April 2025 opening balance ties to the 31 March 2026 closing balance on all four "
    f"components) and every FY2025 comparative printed in the FY2026 report reproduces this "
    f"workbook's existing FY2025 figures exactly, so no prior year was restated. Two presentational "
    f"points carried over unchanged from FY2025: 'Debt Securities' and 'Equity shares' are printed "
    f"as two separate Balance Sheet lines and are combined here into the single 'Investment "
    f"securities other than Government/Treasury securities' row (FY2026 473,773 + 3,804 = 477,577), "
    f"and 'Intangible fixed assets' and 'Tangible fixed assets' are likewise combined into "
    f"'Tangible & intangible fixed assets' (FY2026 1,189 + 2,145 = 3,334) - both matching how the "
    f"earlier years in this sheet are already presented. FY2026's 'Impairment on loans and "
    f"advances' is a net credit of USD 534k (a release, not a charge), which is a real disclosed "
    f"figure, not a sign error.\n"
    f"FY2025/FY2024: Annual Report and Accounts, year ended 31 March 2025, Profit and loss "
    f"account/Statement of other comprehensive income/Balance sheet/Statement of change in "
    f"equity, pp.36-39 - {AR2025_URL}\n"
    f"FY2023 (own): Annual Report and Accounts, year ended 31 March 2023, pp.38-41 - {AR2023_URL}\n"
    f"FY2022 (own): Annual Report and Accounts, year ended 31 March 2022, pp.39-42 - {AR2022_URL}\n"
    f"FY2021 (own): Annual Report and Accounts, year ended 31 March 2021, pp.35-38 - {AR2021_URL}\n"
    f"FY2020 (own): Strategic report, Directors' report and financial statements, year ended 31 "
    f"March 2020, Profit and loss account/Statement of other comprehensive income/Balance "
    f"sheet/Statement of change in equity/Note 19, pp.30-33, 51-52 - {AR2020_URL}\n"
    f"FY2019 (own): Strategic report, Directors' report and financial statements, year ended 31 "
    f"March 2019, pp.29-32, 55 - {AR2019_URL}\n"
    f"FY2018 (own): Strategic report, Directors' report and financial statements, year ended 31 "
    f"March 2018, pp.25-28, 51 - {AR2018_URL}\n"
    f"FY2017 (own): Strategic Report, Directors' Report and Financial Statements, year ended 31 "
    f"March 2017, pp.19-22, 44 - {AR2017_URL}\n"
    f"FY2016 (own): Strategic Report, Directors' Report and Financial Statements, year ended 31 "
    f"March 2016, pp.16-19, 40 - {AR2016_URL}\n"
    f"FY2015 (own): Strategic Report, Directors' Report and Financial Statements, year ended 31 "
    f"March 2015, pp.14-19, 36-39 - {AR2015_URL}\n"
    f"FY2014 (own): Strategic report, Directors' report and financial statements, year ended 31 "
    f"March 2014 (Companies House filing, scanned/non-text - read directly page by page), pp.16-19 "
    f"- {AR2014_URL}. Cross-checked against the identical FY2014 comparative column reproduced "
    f"text-natively in the FY2015 Annual Report ({AR2015_URL}) - every figure ties exactly.\n"
    f"FY2013 (own, Companies House filing MzA3ODM0MTM2NGFkaXF6a2N4, scanned/non-text - read directly "
    f"page by page): Directors' report and financial statements, year ended March 31, 2013, Profit "
    f"and loss account/Balance sheet/Statement of total recognised gains and losses/Reconciliation "
    f"of movements in shareholders' funds, pp.12-15 - {AR2013_URL}. Cross-checked against the "
    f"identical FY2013 comparative column reproduced in the FY2014 Companies House filing "
    f"({AR2014_URL}) via the opening 1 April 2013 balance on the Statement of Changes in Equity "
    f"sheet - ties exactly.\n"
    f"FY2012 (own, Companies House filing MzA1NzY0MjQxOGFkaXF6a2N4, scanned/non-text): Directors' "
    f"report and financial statements, year ended March 31, 2012, pp.10-13 - {AR2012_URL}. "
    f"Cross-checked against the FY2012 comparative column in the FY2013 filing above - ties exactly "
    f"except the FY2013 filing's comparative reclassifies USD 67,183k out of 'Loans and advances to "
    f"banks' into a new 'Balances at central banks' line for FY2012 (a restatement, not a real "
    f"change - FY2012's own originally-published Total assets of 4,084,322 is unaffected either "
    f"way); this workbook uses FY2012's own originally-published, unreclassified figures "
    f"throughout, per this project's standard convention.\n"
    f"FY2011 (own, Companies House filing MzAzNjcwNDYwOGFkaXF6a2N4, scanned/non-text): Directors' "
    f"report and financial statements, year ended March 31, 2011, pp.9-12 - {AR2011_URL}. "
    f"Cross-checked against the FY2011 comparative column in the FY2012 filing above - ties exactly.\n"
    f"FY2010 (own, Companies House filing MzAyMTI3MzU1MGFkaXF6a2N4, scanned/non-text): Directors "
    f"report and financial statements, year ended March 31, 2010, pp.9-12 - {AR2010_URL}. "
    f"Cross-checked against the FY2010 comparative column in the FY2011 filing above - ties exactly.\n"
    f"FY2009 (own, Companies House filing MjAzNTc0MTU4N2FkaXF6a2N4, scanned/non-text): Directors' "
    f"report and financial statements, year ended March 31, 2009, pp.10-13 - {AR2009_URL}. "
    f"Cross-checked against the FY2009 comparative column in the FY2010 filing above - ties exactly.\n"
    f"FY2008 (own, Companies House filing MjAwNzk0MTQ0MGFkaXF6a2N4, scanned/non-text): Directors' "
    f"report and financial statements, year ended 31 March 2008, Profit and loss account/Balance "
    f"sheet/Statement of total recognised gains and losses/Reconciliation of movements in "
    f"shareholders' funds, pp.9-12 - {AR2008_URL}. Cross-checked against the FY2008 comparative "
    f"column in the FY2009 filing above - ties exactly (both give Total assets 8,829,049).\n"
    "HD-046 (2026-09-05): extended FY2014-FY2020 back from the prior FY2021-FY2025 window, capped "
    "at FY2014 by explicit project-wide decision (real archive on icicibank.co.uk goes back to "
    "FY2008, see HD-046.md) - see wayfinder/historical-depth/tickets/HD-046.md.\n"
    "HD-075 (2026-09-06): extended the four statutory statements (Balance Sheet, Profit & Loss, "
    "Statement of Changes in Equity, Cash Flow Statement) only, further back to FY2008 - the real "
    "statutory floor identified by HD-004/HD-046 - by reading all six Companies House filings for "
    "FY2008-FY2013 directly (all scanned/non-text, read page by page). Pillar 3, Asset Quality and "
    "RWA Breakdown remain capped at FY2014 - out of scope for HD-075. See "
    "wayfinder/historical-depth/tickets/HD-075.md.\n"
    "PRESENTATION NOTES: each year's own originally-published figures are used throughout "
    "(not later restated comparatives), except for the Statement of Changes in Equity where a "
    "genuine, Bank-disclosed prior period adjustment is shown explicitly (see that sheet's own "
    "note). Line items renamed/regrouped across years without changing the underlying figure "
    "are shown on a consistent row (e.g. FY2021-2023's 'Cash and cash equivalents' = FY2024-25's "
    "'Cash and Balances at Central Banks' = FY2014-2017's 'Cash' + 'Balances at central banks' "
    "summed, since FY2014-2017 disclosed these as two separate lines; FY2021-2024's single "
    "'Investment securities other than Government/Treasury securities' line = FY2025's 'Debt "
    "Securities' + 'Equity shares' combined, since FY2025 was the only year to break these out "
    "separately). P&L uses 'Total revenue' (FY2021-2023) and 'Net Income' (FY2024-2025) "
    "interchangeably for the same subtotal concept (sum of net interest income plus fee/FX/"
    "trading income including profit/(loss) on sale of financial assets) - shown on one row; "
    "FY2018-FY2020's own 'Total revenue' subtotal is built the same way. FY2014-FY2017's own "
    "headline subtotal is instead 'Operating income', which EXCLUDES 'Profit/(Loss) on sale of "
    "debt securities' (that line sits structurally below impairments in those years' own P&L, "
    "immediately before pre-tax profit) - so the 'Total revenue / Net Income' TOTAL row for "
    "FY2014-FY2017 equals that year's own 'Operating income' figure, not a recomputed sum "
    "including the sale-of-debt-securities line shown elsewhere on this sheet; shown explicitly "
    "rather than force-reconciled to match later years' structure. Balance Sheet: FY2025 has no "
    "separate 'Bonds and medium term notes' line (present FY2021-2024, nil in FY2024) - left "
    "blank for FY2025, not force-merged into another line; FY2025 has no separate 'Deposits by "
    "banks' comparator issue (FY2024 explicitly nil, shown as 0). 'Bonds and medium term notes' "
    "and 'Subordinated debt' were disclosed as a single combined 'Debt securities and "
    "subordinated liabilities' line in both the FY2014 and FY2015 Annual Reports (neither report "
    "splits FY2014 into the two components); the FY2015 figure is split here using the FY2016 "
    "Annual Report's own FY2015 comparative column (250,530/233,402, ties exactly to the combined "
    "483,932 both FY2014 and FY2015 ARs report), but no equivalent split exists anywhere for "
    "FY2014, so FY2014's combined total is shown on its own dedicated row instead, with both "
    "'Bonds and medium term notes' and 'Subordinated debt' left blank for FY2014 rather than "
    "guessed. The same 'Debt securities and subordinated liabilities' combined row is used for "
    "FY2008-FY2013 too (none of those years' own Annual Reports, nor any later year's comparative "
    "column, ever splits them) - see the dedicated combined row below the split rows. Similarly, "
    "'Investment in Treasury Bills / Government Securities' and 'Investment Securities other than "
    "Government/Treasury securities' are shown combined on a single 'Investment securities' row "
    "for FY2008-FY2010 (no split exists in any source reviewed); FY2011 IS split, using the FY2012 "
    "Annual Report's own FY2011 comparative column (517,435/1,057,938, ties exactly to the combined "
    "1,575,373 both the FY2011 and FY2012 ARs report for that year), even though FY2011's own "
    "Annual Report itself only shows the combined figure. HD-075 (2026-09-06) wrinkle: 'Issued "
    "share capital' meant only Ordinary/Equity share capital throughout the pre-existing FY2014-"
    "FY2025 window (Preference share capital having already been redeemed by FY2014); for the newly-"
    "added FY2008-FY2012 the Bank's Balance Sheet discloses Ordinary/Equity and Preference/Non-"
    "equity share capital as two separate lines throughout (labelled 'Ordinary'/'Preference' from "
    "FY2012, 'Equity'/'Non-equity' FY2008-FY2011 - same substance), so a new 'Preference share "
    "capital' row is added, carrying 50,000 for FY2008-FY2012 and explicit nil for FY2013 (the year "
    "of redemption - see Statement of Changes in Equity), blank thereafter. The Profit & Loss sheet "
    "gains a new 'Gains on buy back of bonds' row, disclosed as its own P&L line FY2009-FY2012 "
    "(87,357/6,415/150/0) but not present at all in the FY2008 P&L or any FY2013 onward P&L - left "
    "blank for FY2008 and FY2013 onward rather than assumed nil (FY2012's own 'Financial 2013' "
    "column implies the line still existed conceptually but was FY2013-onward folded back into "
    "profit/(loss) on sale of debt securities per that year's own Directors' report highlights "
    "table). FY2008's P&L does not separately disclose 'Foreign exchange revaluation gains' - that "
    "year's own statement instead shows a single combined 'Dealing (losses)/profits' line (-27,313), "
    "which the FY2009 Annual Report's own FY2008 comparative column later reclassifies into "
    "'Foreign exchange revaluation gains' (23,353) plus 'Income/(Expense) on financial instruments "
    "at fair value through profit and loss' (-50,666) - a restatement, not a real change (both net "
    "to -27,313). Per this workbook's standing convention of using each year's own originally-"
    "published figures, FY2008's combined -27,313 is shown on the 'Income/(loss) on financial "
    "instruments at fair value through P&L' row, with 'Foreign exchange revaluation gains' left "
    "blank for FY2008 only rather than force-split. FY2008's Balance Sheet has no directly-"
    "disclosed 'Total Liabilities' subtotal separate from Total Equity (that year's own statement "
    "prints one combined bottom-line figure covering both) - the FY2008 Total Liabilities row shown "
    "here (8,363,027) is therefore computed as the sum of that year's own disclosed liability line "
    "items, not copied from an explicit source subtotal; it ties exactly (Total Liabilities + Total "
    "Equity = Total assets = 8,829,049). Tangible/intangible fixed assets: shown as one combined line for FY2014 (5,751, no "
    "separate intangible disclosed that year), FY2015 (4,774, ditto), FY2019 and FY2020 (both "
    "years' own 'Tangible and Intangible fixed assets' combined line); shown as two components "
    "summed for FY2016-FY2018, where the Bank disclosed them as separate lines. 'Derivative "
    "financial instruments' first appears as its own Balance Sheet line from FY2018 onward - for "
    "FY2014-FY2017 it was not broken out on the face of the Balance Sheet (only within the credit-"
    "risk note's 'Other assets'/'Other liabilities' sub-analysis) and is left blank rather than "
    "estimated. A 'Capital redemption reserve' row (once $50.0m, cancelled into Retained earnings "
    "during FY2015 - see the Statement of Changes in Equity) applied only to FY2014 (50,000) and "
    "FY2015 (explicitly nil); no such reserve existed FY2016 onward."
    "\n\n" + STATEMENTS_ENTITY_NOTE
)


def p3_sources():
    lines = [
        "Sources - ICICI Bank UK Plc's own Basel Pillar 3 disclosures (standalone Bank basis, USD "
        "million). Every year FY2008-FY2026 now cites that year's OWN edition, read directly; no "
        "year relies on a later edition's comparative column. Two different templates are in play "
        "and are labelled row by row where they differ - the UK KM1 Key Metrics template (FY2022 "
        "onward) and the pre-KM1 CRR/Basel III disclosure (FY2014-FY2021):"
    ]
    for year in YEARS:
        if year in P3_URLS:
            if year >= "FY2022":
                lines.append(
                    f"{year}: official ICICI Bank UK Pillar 3 disclosure, UK KM1 Key Metrics "
                    f"template, pp.7-8 - {P3_URLS[year]}"
                )
            else:
                lines.append(
                    f"{year}: official ICICI Bank UK Pillar 3 disclosure (pre-KM1 CRR/Basel III "
                    f"format: section 3 'Capital resources' / Annexure I transitional own funds "
                    f"template, section 10 'Leverage ratio' CRR LRSum+LRCom tables, and the "
                    f"liquidity-risk section's LCR narrative) - {P3_URLS[year]}"
                )
        else:
            lines.append(
                f"{year}: Basel II edition - published and read, but discloses no key metric. "
                f"See the Basel II note below. {P3_BASEL2_URLS[year]}"
            )
    lines.append(
        "FY2021 SOURCE UPGRADE (2026-09-15): FY2021 previously relied on the 31 March 2021 "
        "comparative column of the FY2022 edition. Its own FY2021 edition has since been located "
        "and read, and it reproduces every figure already carried here exactly - CET1 493.9, "
        "Tier 1 493.9, Total capital 586.7, Total RWA 2,075.1, CET1/Tier 1 ratio 23.80%, total "
        "capital ratio 28.27% (Annexure I transitional own funds template rows 59-63 and LRCom "
        "row 20). The same document's 31 March 2020 comparatives (440.9 / 547.2 / 2,941.4 / "
        "14.99% / 18.60%) likewise reproduce this workbook's FY2020 figures exactly. No "
        "restatement in either direction. The upgrade additionally supplies FY2021's leverage "
        "and LCR figures, which the FY2022 KM1 had left blank - see those sheets' own basis notes."
    )
    lines.append(BASEL2_NOTE)
    lines.append(ENTITY_NOTE)
    return "\n".join(lines)


bw = BankWorkbook(bank_name="ICICI Bank UK Plc", years=Y_CORE, year_label={y: y for y in YEARS}, header_color="2A5D67")

BS_ROWS = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents / Cash and Balances at Central Banks", {"FY2026": 339580, "FY2025": 403868, "FY2024": 219629, "FY2023": 352907, "FY2022": 336706, "FY2021": 733560, "FY2020": 289988, "FY2019": 273101, "FY2018": 500246, "FY2017": 282287, "FY2016": 500618, "FY2015": 449752, "FY2014": 1009055, "FY2013": 583792, "FY2012": 1255, "FY2011": 1057, "FY2010": 1060, "FY2009": 3108, "FY2008": 3150}),
    ("DATA", "Investment in Treasury Bills / Government Securities", {"FY2026": 410126, "FY2025": 140589, "FY2024": 146509, "FY2023": 206357, "FY2022": 154441, "FY2021": 125760, "FY2020": 263617, "FY2019": 297509, "FY2018": 192094, "FY2017": 74127, "FY2016": 129352, "FY2015": 84951, "FY2014": 126967, "FY2013": 101988, "FY2012": 693723, "FY2011": 517435}),
    ("DATA", "Loans and advances to banks", {"FY2026": 342659, "FY2025": 339561, "FY2024": 355557, "FY2023": 190371, "FY2022": 141379, "FY2021": 52372, "FY2020": 168105, "FY2019": 144881, "FY2018": 137553, "FY2017": 106641, "FY2016": 283149, "FY2015": 184146, "FY2014": 79079, "FY2013": 78657, "FY2012": 301503, "FY2011": 875384, "FY2010": 1429224, "FY2009": 984601, "FY2008": 2225539}),
    ("DATA", "Loans and advances to customers", {"FY2026": 1303357, "FY2025": 964471, "FY2024": 888857, "FY2023": 899505, "FY2022": 1182895, "FY2021": 1522138, "FY2020": 2074527, "FY2019": 2423180, "FY2018": 2365651, "FY2017": 2332132, "FY2016": 2962535, "FY2015": 2878811, "FY2014": 2749136, "FY2013": 2282972, "FY2012": 2387707, "FY2011": 3594595, "FY2010": 3635269, "FY2009": 3146865, "FY2008": 1963202}),
    ("DATA", "Investment securities other than Government/Treasury securities (FY2026 and FY2025: Debt Securities + Equity shares combined)", {"FY2026": 477577, "FY2025": 535052, "FY2024": 551784, "FY2023": 431819, "FY2022": 366804, "FY2021": 412986, "FY2020": 607599, "FY2019": 608610, "FY2018": 612801, "FY2017": 609179, "FY2016": 614061, "FY2015": 412979, "FY2014": 371918, "FY2013": 423667, "FY2012": 479531, "FY2011": 1057938}),
    ("DATA", "Investment securities (FY2008-FY2010 only - combined, not split into Treasury Bills/other; see source note)", {"FY2010": 2000397, "FY2009": 2927000, "FY2008": 4365047}),
    ("DATA", "Derivative financial instruments", {"FY2026": 16802, "FY2025": 22995, "FY2024": 23710, "FY2023": 48189, "FY2022": 20096, "FY2021": 49181, "FY2020": 33964, "FY2019": 29259, "FY2018": 24295}),
    ("DATA", "Tangible & intangible fixed assets", {"FY2026": 3334, "FY2025": 2447, "FY2024": 2350, "FY2023": 2348, "FY2022": 2690, "FY2021": 3549, "FY2020": 4107, "FY2019": 2302, "FY2018": 2776, "FY2017": 3469, "FY2016": 4184, "FY2015": 4774, "FY2014": 5751, "FY2013": 7172, "FY2012": 8487, "FY2011": 9760, "FY2010": 11666, "FY2009": 13076, "FY2008": 7677}),
    ("DATA", "Other assets", {"FY2026": 13670, "FY2025": 11331, "FY2024": 13339, "FY2023": 9221, "FY2022": 27383, "FY2021": 46158, "FY2020": 82985, "FY2019": 43270, "FY2018": 30380, "FY2017": 55076, "FY2016": 53236, "FY2015": 79037, "FY2014": 109065, "FY2013": 93402, "FY2012": 182211, "FY2011": 337406, "FY2010": 285930, "FY2009": 162985, "FY2008": 177925}),
    ("DATA", "Prepayments and accrued income", {"FY2026": 1146, "FY2025": 1299, "FY2024": 1525, "FY2023": 1343, "FY2022": 9579, "FY2021": 11050, "FY2020": 15792, "FY2019": 18048, "FY2018": 18544, "FY2017": 16855, "FY2016": 56122, "FY2015": 35356, "FY2014": 20183, "FY2013": 15656, "FY2012": 29905, "FY2011": 48445, "FY2010": 55319, "FY2009": 83073, "FY2008": 86509}),
    ("TOTAL", "Total assets", {"FY2026": 2908251, "FY2025": 2421613, "FY2024": 2203260, "FY2023": 2142060, "FY2022": 2241973, "FY2021": 2956754, "FY2020": 3540684, "FY2019": 3840160, "FY2018": 3884340, "FY2017": 3479766, "FY2016": 4603257, "FY2015": 4129806, "FY2014": 4471154, "FY2013": 3587306, "FY2012": 4084322, "FY2011": 6442020, "FY2010": 7418865, "FY2009": 7320708, "FY2008": 8829049}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2026": 167161, "FY2025": 27169, "FY2024": 0, "FY2023": 32456, "FY2022": 28850, "FY2021": 65315, "FY2020": 285939, "FY2019": 559541, "FY2018": 916438, "FY2017": 602425, "FY2016": 591280, "FY2015": 365417, "FY2014": 461141, "FY2013": 288768, "FY2012": 318651, "FY2011": 355627, "FY2010": 782806, "FY2009": 813326, "FY2008": 1413152}),
    ("DATA", "Customer accounts", {"FY2026": 2263521, "FY2025": 1901625, "FY2024": 1668596, "FY2023": 1617438, "FY2022": 1541957, "FY2021": 1957458, "FY2020": 2042228, "FY2019": 2140798, "FY2018": 1748820, "FY2017": 1648588, "FY2016": 2466866, "FY2015": 2284686, "FY2014": 2533259, "FY2013": 1799281, "FY2012": 2411464, "FY2011": 4210158, "FY2010": 4552107, "FY2009": 4622767, "FY2008": 5180328}),
    ("DATA", "Bonds and medium term notes", {"FY2024": 0, "FY2023": 25122, "FY2022": 146358, "FY2021": 197852, "FY2020": 295301, "FY2019": 238632, "FY2018": 359781, "FY2017": 344197, "FY2016": 511453, "FY2015": 250530}),
    ("DATA", "Debt securities and subordinated liabilities (FY2008-FY2014 only - combined; none of these years' own Annual Reports, nor any later year's comparative column, ever splits this into Bonds/Subordinated debt, see source note)", {"FY2014": 426643, "FY2013": 528070, "FY2012": 372621, "FY2011": 838492, "FY2010": 1112408, "FY2009": 1168120, "FY2008": 1341251}),
    ("DATA", "Derivative financial instruments", {"FY2026": 15516, "FY2025": 16587, "FY2024": 19191, "FY2023": 28483, "FY2022": 18208, "FY2021": 40360, "FY2020": 73225, "FY2019": 19918, "FY2018": 17572}),
    ("DATA", "Other liabilities", {"FY2026": 16953, "FY2025": 28627, "FY2024": 24163, "FY2023": 37868, "FY2022": 15546, "FY2021": 19620, "FY2020": 18843, "FY2019": 32265, "FY2018": 13066, "FY2017": 26297, "FY2016": 76075, "FY2015": 126762, "FY2014": 73041, "FY2013": 106591, "FY2012": 222742, "FY2011": 262727, "FY2010": 245458, "FY2009": 287430, "FY2008": 403240}),
    ("DATA", "Accruals and deferred income", {"FY2026": 12955, "FY2025": 11671, "FY2024": 11078, "FY2023": 9734, "FY2022": 13680, "FY2021": 14139, "FY2020": 20724, "FY2019": 24064, "FY2018": 21045, "FY2017": 19096, "FY2016": 24431, "FY2015": 29546, "FY2014": 31477, "FY2013": 34464, "FY2012": 49204, "FY2011": 91654, "FY2010": 99483, "FY2009": 19233, "FY2008": 25056}),
    ("DATA", "Subordinated debt", {"FY2026": 50661, "FY2025": 50568, "FY2024": 50028, "FY2023": 72616, "FY2022": 72954, "FY2021": 76116, "FY2020": 219854, "FY2019": 223348, "FY2018": 149880, "FY2017": 176149, "FY2016": 234242, "FY2015": 233402}),
    ("DATA", "Repurchase Agreements", {"FY2026": 23702, "FY2025": 33425, "FY2024": 92735, "FY2023": 0, "FY2022": 88548, "FY2021": 79153, "FY2020": 131238, "FY2019": 147263, "FY2018": 150986, "FY2017": 129784, "FY2016": 153383, "FY2015": 294035, "FY2014": 316544}),
    ("TOTAL", "Total Liabilities", {"FY2026": 2550469, "FY2025": 2069672, "FY2024": 1865791, "FY2023": 1823717, "FY2022": 1926101, "FY2021": 2450013, "FY2020": 3087352, "FY2019": 3385829, "FY2018": 3377588, "FY2017": 2946536, "FY2016": 4057730, "FY2015": 3584378, "FY2014": 3842105, "FY2013": 2965134, "FY2012": 3374682, "FY2011": 5758658, "FY2010": 6792262, "FY2009": 6910876, "FY2008": 8363027}),
    ("SECTION", "Shareholders' funds", {}),
    ("DATA", "Issued share capital", {"FY2026": 220095, "FY2025": 220095, "FY2024": 220095, "FY2023": 220095, "FY2022": 220095, "FY2021": 420095, "FY2020": 420095, "FY2019": 420095, "FY2018": 420095, "FY2017": 420095, "FY2016": 420095, "FY2015": 420095, "FY2014": 495095, "FY2013": 495095, "FY2012": 545095, "FY2011": 545095, "FY2010": 545095, "FY2009": 545095, "FY2008": 445095}),
    ("DATA", "Preference share capital (Non-equity/Preference share capital; redeemed during FY2013 - see Statement of Changes in Equity)", {"FY2013": 0, "FY2012": 50000, "FY2011": 50000, "FY2010": 50000, "FY2009": 50000, "FY2008": 50000}),
    ("DATA", "Capital contribution", {"FY2026": 12208, "FY2025": 12208, "FY2024": 12208, "FY2023": 12208, "FY2022": 12194, "FY2021": 12108, "FY2020": 11634, "FY2019": 10703, "FY2018": 10168, "FY2017": 9121, "FY2016": 7332, "FY2015": 5912, "FY2014": 5256, "FY2013": 4148, "FY2012": 3151, "FY2011": 2131, "FY2010": 1467, "FY2009": 851}),
    ("DATA", "Capital redemption reserve (cancelled into Retained earnings during FY2015 - see Statement of Changes in Equity)", {"FY2015": 0, "FY2014": 50000, "FY2013": 50000}),
    ("DATA", "Retained earnings", {"FY2026": 126683, "FY2025": 117423, "FY2024": 103595, "FY2023": 86086, "FY2022": 83076, "FY2021": 72175, "FY2020": 57383, "FY2019": 34133, "FY2018": 87002, "FY2017": 112550, "FY2016": 128632, "FY2015": 128089, "FY2014": 89760, "FY2013": 89536, "FY2012": 149278, "FY2011": 148013, "FY2010": 115582, "FY2009": 78589, "FY2008": 71753}),
    ("DATA", "Available for sale reserve", {"FY2026": -1204, "FY2025": 2215, "FY2024": 1571, "FY2023": -46, "FY2022": 507, "FY2021": 2363, "FY2020": -35780, "FY2019": -10600, "FY2018": -10513, "FY2017": -8536, "FY2016": -10532, "FY2015": -8668, "FY2014": -11062, "FY2013": -16607, "FY2012": -37884, "FY2011": -61877, "FY2010": -85541, "FY2009": -264703, "FY2008": -100826}),
    ("TOTAL", "Total Equity", {"FY2026": 357782, "FY2025": 351941, "FY2024": 337469, "FY2023": 318343, "FY2022": 315872, "FY2021": 506741, "FY2020": 453332, "FY2019": 454331, "FY2018": 506752, "FY2017": 533230, "FY2016": 545527, "FY2015": 545428, "FY2014": 629049, "FY2013": 622172, "FY2012": 709640, "FY2011": 683362, "FY2010": 626603, "FY2009": 409832, "FY2008": 466022}),
    ("TOTAL", "Total Equity and Liabilities", {"FY2026": 2908251, "FY2025": 2421613, "FY2024": 2203260, "FY2023": 2142060, "FY2022": 2241973, "FY2021": 2956754, "FY2020": 3540684, "FY2019": 3840160, "FY2018": 3884340, "FY2017": 3479766, "FY2016": 4603257, "FY2015": 4129806, "FY2014": 4471154, "FY2013": 3587306, "FY2012": 4084322, "FY2011": 6442020, "FY2010": 7418865, "FY2009": 7320708, "FY2008": 8829049}),
]

bw.add_balance_sheet_sheet(
    title="ICICI Bank UK Plc — Statement of Financial Position",
    subtitle="Bank (standalone), USD'000, each year's own originally-published figures. See source note at bottom.",
    rows=BS_ROWS,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=220,
    unit_suffix=" (USD'000)",
    years=YEARS,
)

PL_ROWS = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income and similar income", {"FY2026": 121087, "FY2025": 124272, "FY2024": 123959, "FY2023": 76554, "FY2022": 54766, "FY2021": 82846, "FY2020": 123971, "FY2019": 130009, "FY2018": 115269, "FY2017": 118410, "FY2016": 141059, "FY2015": 134664, "FY2014": 130932, "FY2013": 141925, "FY2012": 196182, "FY2011": 257674, "FY2010": 286754, "FY2009": 447061, "FY2008": 414259}),
    ("DATA", "Interest expense", {"FY2026": -53845, "FY2025": -58391, "FY2024": -57300, "FY2023": -23910, "FY2022": -14268, "FY2021": -31939, "FY2020": -59708, "FY2019": -59487, "FY2018": -48364, "FY2017": -52884, "FY2016": -69571, "FY2015": -70012, "FY2014": -75700, "FY2013": -91033, "FY2012": -137742, "FY2011": -182846, "FY2010": -239637, "FY2009": -377893, "FY2008": -364419}),
    ("TOTAL", "Net interest income", {"FY2026": 67242, "FY2025": 65881, "FY2024": 66659, "FY2023": 52644, "FY2022": 40498, "FY2021": 50907, "FY2020": 64263, "FY2019": 70522, "FY2018": 66905, "FY2017": 65526, "FY2016": 71488, "FY2015": 64652, "FY2014": 55232, "FY2013": 50892, "FY2012": 58440, "FY2011": 74828, "FY2010": 47117, "FY2009": 69168, "FY2008": 49840}),
    ("DATA", "Fees and commissions receivable", {"FY2026": 10818, "FY2025": 8656, "FY2024": 7399, "FY2023": 6785, "FY2022": 7352, "FY2021": 6461, "FY2020": 8475, "FY2019": 8042, "FY2018": 8135, "FY2017": 9217, "FY2016": 17285, "FY2015": 20812, "FY2014": 27030, "FY2013": 19041, "FY2012": 16514, "FY2011": 23578, "FY2010": 40541, "FY2009": 31046, "FY2008": 81023}),
    ("DATA", "Foreign exchange revaluation gains", {"FY2026": 10585, "FY2025": 8918, "FY2024": 8389, "FY2023": 6343, "FY2022": 5786, "FY2021": 6376, "FY2020": 6969, "FY2019": 5363, "FY2018": 6907, "FY2017": 4572, "FY2016": 4820, "FY2015": 6689, "FY2014": 7999, "FY2013": 9435, "FY2012": 9277, "FY2011": 2828, "FY2010": 7456, "FY2009": 1712}),
    ("DATA", "Income/(loss) on financial instruments at fair value through P&L (FY2008: combined with Foreign exchange revaluation gains as a single 'Dealing (losses)/profits' line - see source note)", {"FY2026": 192, "FY2025": 1238, "FY2024": -17, "FY2023": 1095, "FY2022": 461, "FY2021": -157, "FY2020": -749, "FY2019": 126, "FY2018": -2282, "FY2017": -1090, "FY2016": -6638, "FY2015": 12023, "FY2014": -1291, "FY2013": 4508, "FY2012": -694, "FY2011": 3240, "FY2010": 9460, "FY2009": -667, "FY2008": -27313}),
    ("DATA", "Profit/(loss) on sale of financial assets", {"FY2026": 692, "FY2025": 2601, "FY2024": 3221, "FY2023": -7094, "FY2022": 66, "FY2021": -1336, "FY2020": -23, "FY2019": -4773, "FY2018": 2960, "FY2017": 4619, "FY2016": 11984, "FY2015": 8299, "FY2014": 2974, "FY2013": -1192, "FY2012": -5205, "FY2011": 6390, "FY2010": 8932, "FY2009": -12476, "FY2008": 23}),
    ("DATA", "Gains on buy back of bonds (disclosed as its own P&L line FY2009-FY2012 only; not present in the FY2008 P&L or any FY2013-onward P&L - see source note)", {"FY2012": 0, "FY2011": 150, "FY2010": 6415, "FY2009": 87357}),
    ("DATA", "Other operating income", {"FY2026": 771, "FY2025": 28, "FY2024": 40, "FY2023": 279, "FY2022": 294, "FY2021": 326, "FY2020": 375, "FY2019": 562, "FY2018": 599, "FY2017": 665, "FY2016": 682, "FY2015": 451, "FY2014": 1185, "FY2013": 697, "FY2012": 848, "FY2011": 2285, "FY2010": 2225, "FY2009": 1508, "FY2008": 6186}),
    ("TOTAL", "Total revenue / Net Income (FY2014-FY2017: that year's own 'Operating income' subtotal, which EXCLUDES the profit/(loss)-on-sale-of-financial-assets row above - see source note)", {"FY2026": 90300, "FY2025": 87322, "FY2024": 85691, "FY2023": 60052, "FY2022": 54457, "FY2021": 62577, "FY2020": 79310, "FY2019": 79842, "FY2018": 83224, "FY2017": 78890, "FY2016": 87637, "FY2015": 104627, "FY2014": 90155, "FY2013": 84573, "FY2012": 84385, "FY2011": 106909, "FY2010": 113214, "FY2009": 190124, "FY2008": 109736}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2026": -57704, "FY2025": -51266, "FY2024": -46758, "FY2023": -37348, "FY2022": -38960, "FY2021": -35531, "FY2020": -37402, "FY2019": -33314, "FY2018": -34135, "FY2017": -33050, "FY2016": -33142, "FY2015": -37259, "FY2014": -35318, "FY2013": -35523, "FY2012": -37630, "FY2011": -42153, "FY2010": -46814, "FY2009": -58413, "FY2008": -45704}),
    ("DATA", "Depreciation", {"FY2026": -1043, "FY2025": -786, "FY2024": -709, "FY2023": -956, "FY2022": -1229, "FY2021": -1157, "FY2020": -994, "FY2019": -796, "FY2018": -782, "FY2017": -867, "FY2016": -1026, "FY2015": -1414, "FY2014": -1472, "FY2013": -1476, "FY2012": -1540, "FY2011": -2338, "FY2010": -2490, "FY2009": -1610, "FY2008": -1301}),
    # Not a line the source statement itself prints - the Bank's own P&L
    # goes straight from these two expense lines to the impairment lines,
    # with no combined opex subtotal. This row is simply their sum
    # (Administrative expenses + Depreciation, excluding the two impairment
    # lines below, consistent with this project's convention of keeping
    # credit-loss/impairment charges out of "operating expenses" - ties
    # exactly to Total revenue - Profit on ordinary activities before tax
    # net of the two impairment lines in every year, e.g. FY2025
    # 87322-51266-786-27-3207=32036), added 2026-09-07 so cost-to-income
    # analysis has a "Total operating expenses" numerator to work from.
    ("TOTAL", "Total operating expenses (sum of Administrative expenses + Depreciation above - not itself a printed subtotal)", {
        "FY2026": -58747, "FY2025": -52052, "FY2024": -47467, "FY2023": -38304, "FY2022": -40189, "FY2021": -36688,
        "FY2020": -38396, "FY2019": -34110, "FY2018": -34917, "FY2017": -33917, "FY2016": -34168,
        "FY2015": -38673, "FY2014": -36790, "FY2013": -36999, "FY2012": -39170, "FY2011": -44491,
        "FY2010": -49304, "FY2009": -60023, "FY2008": -47005,
    }),
    ("DATA", "Impairment on investment securities", {"FY2026": -4, "FY2025": -27, "FY2024": -23, "FY2023": -79, "FY2022": -20, "FY2021": 49, "FY2020": -3432, "FY2019": -992, "FY2018": 0, "FY2017": 0, "FY2016": -5917, "FY2015": -13538, "FY2014": -5632, "FY2013": -7015, "FY2012": -8916, "FY2011": 1112, "FY2010": 0, "FY2009": -91434}),
    ("DATA", "Impairment on loans and advances", {"FY2026": 534, "FY2025": -3207, "FY2024": -7145, "FY2023": -5867, "FY2022": -2906, "FY2021": -8414, "FY2020": -8902, "FY2019": -104401, "FY2018": -78710, "FY2017": -68181, "FY2016": -53525, "FY2015": -37945, "FY2014": -14590, "FY2013": -20209, "FY2012": 4356, "FY2011": -18868, "FY2010": -20549, "FY2009": -16111, "FY2008": -6026}),
    ("TOTAL", "Profit on ordinary activities before tax", {"FY2026": 32083, "FY2025": 32036, "FY2024": 31056, "FY2023": 15802, "FY2022": 11342, "FY2021": 17524, "FY2020": 28580, "FY2019": -59661, "FY2018": -30404, "FY2017": -18589, "FY2016": 6011, "FY2015": 22770, "FY2014": 36117, "FY2013": 19158, "FY2012": 35450, "FY2011": 51052, "FY2010": 52293, "FY2009": 10080, "FY2008": 56728}),
    ("DATA", "Taxation on ordinary activities", {"FY2026": -6823, "FY2025": -5208, "FY2024": -2279, "FY2023": -2792, "FY2022": -441, "FY2021": -2732, "FY2020": -5331, "FY2019": 6792, "FY2018": 4856, "FY2017": 2507, "FY2016": -5468, "FY2015": -4441, "FY2014": -10893, "FY2013": -4775, "FY2012": -10060, "FY2011": -14496, "FY2010": -15300, "FY2009": -3244, "FY2008": -18316}),
    ("TOTAL", "Profit for the year", {"FY2026": 25260, "FY2025": 26828, "FY2024": 28777, "FY2023": 13010, "FY2022": 10901, "FY2021": 14792, "FY2020": 23249, "FY2019": -52869, "FY2018": -25548, "FY2017": -16082, "FY2016": 543, "FY2015": 18329, "FY2014": 25224, "FY2013": 14383, "FY2012": 25390, "FY2011": 36556, "FY2010": 36993, "FY2009": 6836, "FY2008": 38412}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Movement in valuation of available for sale debt securities, net of tax (FY2020 also includes a new cash flow hedge component - see source note)", {"FY2026": -3419, "FY2025": 644, "FY2024": 1617, "FY2023": -553, "FY2022": -1856, "FY2021": 38143, "FY2020": -25180, "FY2019": -87, "FY2018": -1977, "FY2017": 1996, "FY2016": -1864, "FY2015": 2394, "FY2014": 5545, "FY2013": 21277, "FY2012": 23993, "FY2011": 23664, "FY2010": 179162, "FY2009": -163877, "FY2008": -100454}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2026": 21841, "FY2025": 27472, "FY2024": 30394, "FY2023": 12457, "FY2022": 9045, "FY2021": 52935, "FY2020": -1931, "FY2019": -52956, "FY2018": -27525, "FY2017": -14086, "FY2016": -1321, "FY2015": 20723, "FY2014": 30769, "FY2013": 35660, "FY2012": 49383, "FY2011": 60220, "FY2010": 216155, "FY2009": -157041, "FY2008": -62042}),
]

bw.add_income_statement_sheet(
    title="ICICI Bank UK Plc — Profit and Loss Account",
    subtitle="Bank (standalone), USD'000, each year's own originally-published figures. See source note at bottom.",
    rows=PL_ROWS,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=220,
    unit_suffix=" (USD'000)",
    years=YEARS,
)

EQUITY_HEADERS = ["Issued share capital", "Retained earnings", "Capital redemption reserve", "Available for sale reserve", "Capital contribution", "Total equity"]
EQUITY_ROWS = [
    ("TOTAL", "Balance as at 1 April 2007 (FY2008's own opening; 'Issued share capital' here combines Ordinary/Equity + Preference/Non-equity share capital throughout FY2008-FY2012, matching the Bank's own Reconciliation of movements in shareholders' funds table - see subtitle note)", (185095, 37466, None, -372, None, 222189)),
    ("DATA", "Ordinary shares issued during the year, FY2008", (310000, None, None, None, None, 310000)),
    ("DATA", "Unrealised loss on available for sale securities, FY2008", (None, None, None, -142763, None, -142763)),
    ("DATA", "Tax impact on available for sale reserve, FY2008", (None, None, None, 42309, None, 42309)),
    ("DATA", "Profit for the year, FY2008", (None, 38412, None, None, None, 38412)),
    ("DATA", "Preference dividend paid, FY2008", (None, -4125, None, None, None, -4125)),
    ("TOTAL", "Balance as at 31 March 2008 / 1 April 2008", (495095, 71753, None, -100826, None, 466022)),
    ("DATA", "Ordinary shares issued during the year, FY2009", (100000, None, None, None, None, 100000)),
    ("DATA", "Capital contribution (share-based payments), FY2009", (None, None, None, None, 851, 851)),
    ("DATA", "Unrealised loss on available for sale securities, FY2009", (None, None, None, -208291, None, -208291)),
    ("DATA", "Tax impact on available for sale reserve, FY2009", (None, None, None, 44414, None, 44414)),
    ("DATA", "Profit for the year, FY2009", (None, 6836, None, None, None, 6836)),
    ("TOTAL", "Balance as at 31 March 2009 / 1 April 2009", (595095, 78589, None, -264703, 851, 409832)),
    ("DATA", "Capital contribution (share-based payments), FY2010", (None, None, None, None, 616, 616)),
    ("DATA", "Unrealised gain on available for sale securities, FY2010", (None, None, None, 232412, None, 232412)),
    ("DATA", "Tax impact on available for sale reserve, FY2010", (None, None, None, -53250, None, -53250)),
    ("DATA", "Profit for the year, FY2010", (None, 36993, None, None, None, 36993)),
    ("TOTAL", "Balance as at 31 March 2010 / 1 April 2010", (595095, 115582, None, -85541, 1467, 626603)),
    ("DATA", "Capital contribution (share-based payments), FY2011", (None, None, None, None, 664, 664)),
    ("DATA", "Unrealised gain on available for sale securities, FY2011", (None, None, None, 32867, None, 32867)),
    ("DATA", "Tax impact on available for sale reserve, FY2011", (None, None, None, -9203, None, -9203)),
    ("DATA", "Profit for the year, FY2011", (None, 36556, None, None, None, 36556)),
    ("DATA", "Preference dividend paid, FY2011", (None, -4125, None, None, None, -4125)),
    ("TOTAL", "Balance as at 31 March 2011 / 1 April 2011", (595095, 148013, None, -61877, 2131, 683362)),
    ("DATA", "Capital contribution (share-based payments), FY2012", (None, None, None, None, 1020, 1020)),
    ("DATA", "Unrealised gain on available for sale securities, FY2012", (None, None, None, 30020, None, 30020)),
    ("DATA", "Tax impact on available for sale reserve, FY2012", (None, None, None, -6027, None, -6027)),
    ("DATA", "Profit for the year, FY2012", (None, 25390, None, None, None, 25390)),
    ("DATA", "Preference dividend paid, FY2012", (None, -4125, None, None, None, -4125)),
    ("DATA", "Equity dividend paid, FY2012", (None, -20000, None, None, None, -20000)),
    ("TOTAL", "Balance as at 31 March 2012 / 1 April 2012", (595095, 149278, None, -37884, 3151, 709640)),
    ("DATA", "Capital contribution (share-based payments), FY2013", (None, None, None, None, 997, 997)),
    ("DATA", "Redemption of Preference share capital, FY2013", (-50000, -50000, 50000, None, None, -50000)),
    ("DATA", "Reduction in Equity share capital, FY2013", (-50000, None, None, None, None, -50000)),
    ("DATA", "Unrealised gain on available for sale securities, FY2013", (None, None, None, 27996, None, 27996)),
    ("DATA", "Tax impact on available for sale reserve, FY2013", (None, None, None, -6719, None, -6719)),
    ("DATA", "Profit for the year, FY2013", (None, 14383, None, None, None, 14383)),
    ("DATA", "Preference dividend paid, FY2013", (None, -4125, None, None, None, -4125)),
    ("DATA", "Equity dividend paid, FY2013", (None, -20000, None, None, None, -20000)),
    ("TOTAL", "Balance as at 31 March 2013 / 1 April 2013 (FY2014's own opening; from here on 'Issued share capital' is Ordinary shares only, since Preference share capital was redeemed to nil during FY2013 - see the two DATA rows above)", (495095, 89536, 50000, -16607, 4148, 622172)),
    ("DATA", "Capital contribution (share-based payments), FY2014", (None, None, None, None, 1108, 1108)),
    ("DATA", "Unrealised gain on available for sale securities, FY2014", (None, None, None, 7201, None, 7201)),
    ("DATA", "Tax impact on available for sale reserve, FY2014", (None, None, None, -1656, None, -1656)),
    ("DATA", "Profit for the year, FY2014", (None, 25224, None, None, None, 25224)),
    ("DATA", "Equity dividend paid, FY2014", (None, -25000, None, None, None, -25000)),
    ("TOTAL", "Balance as at 31 March 2014 / 1 April 2014", (495095, 89760, 50000, -11062, 5256, 629049)),
    ("DATA", "Reduction in equity share capital, FY2015", (-75000, None, None, None, None, -75000)),
    ("DATA", "Cancellation of capital redemption reserve, FY2015 (moved to Retained earnings, no effect on Total equity)", (None, 50000, -50000, None, None, 0)),
    ("DATA", "Capital contribution (share-based payments), FY2015", (None, None, None, None, 656, 656)),
    ("DATA", "Unrealised gain on available for sale securities, FY2015", (None, None, None, 6585, None, 6585)),
    ("DATA", "Tax impact on available for sale reserve, FY2015", (None, None, None, -4191, None, -4191)),
    ("DATA", "Profit for the year, FY2015", (None, 18329, None, None, None, 18329)),
    ("DATA", "Equity dividend paid, FY2015", (None, -30000, None, None, None, -30000)),
    ("TOTAL", "Balance as at 31 March 2015 / 1 April 2015 (Capital redemption reserve now nil, cancelled - see above)", (420095, 128089, 0, -8668, 5912, 545428)),
    ("DATA", "Capital contribution (share-based payments), FY2016", (None, None, None, None, 1420, 1420)),
    ("DATA", "Other comprehensive income, FY2016", (None, None, None, -1864, None, -1864)),
    ("DATA", "Profit for the year, FY2016", (None, 543, None, None, None, 543)),
    ("TOTAL", "Balance as at 31 March 2016 / 1 April 2016", (420095, 128632, 0, -10532, 7332, 545527)),
    ("DATA", "Capital contribution (share-based payments), FY2017", (None, None, None, None, 1789, 1789)),
    ("DATA", "Other comprehensive income, FY2017", (None, None, None, 1996, None, 1996)),
    ("DATA", "(Loss) for the year, FY2017", (None, -16082, None, None, None, -16082)),
    ("TOTAL", "Balance as at 31 March 2017 / 1 April 2017", (420095, 112550, 0, -8536, 9121, 533230)),
    ("DATA", "Capital contribution (share-based payments), FY2018", (None, None, None, None, 1047, 1047)),
    ("DATA", "Other comprehensive income, FY2018", (None, None, None, -1977, None, -1977)),
    ("DATA", "(Loss) for the year, FY2018", (None, -25548, None, None, None, -25548)),
    ("TOTAL", "Balance as at 31 March 2018 / 1 April 2018", (420095, 87002, 0, -10513, 10168, 506752)),
    ("DATA", "Capital contribution (share-based payments), FY2019", (None, None, None, None, 535, 535)),
    ("DATA", "Other comprehensive income, FY2019", (None, None, None, -87, None, -87)),
    ("DATA", "(Loss) for the year, FY2019", (None, -52869, None, None, None, -52869)),
    ("TOTAL", "Balance as at 31 March 2019 / 1 April 2019", (420095, 34133, 0, -10600, 10703, 454331)),
    ("DATA", "Capital contribution (share-based payments), FY2020", (None, None, None, None, 931, 931)),
    ("DATA", "Profit for the year, FY2020 (per the Bank's own Statement of Changes in Equity; the P&L account's own figure is 23,249, a $1k rounding difference between the two source statements)", (None, 23250, None, None, None, 23250)),
    ("DATA", "Movement in other comprehensive income (fair value + cash flow hedge, net of tax), FY2020", (None, None, None, -25180, None, -25180)),
    ("TOTAL", "Balance as at 1 April 2020 (FY2021's own opening)", (420095, 57383, 0, -35780, 11634, 453332)),
    ("DATA", "Capital contribution (share-based payments), FY2021", (None, None, None, None, 474, 474)),
    ("DATA", "Profit for the year, FY2021", (None, 14792, None, None, None, 14792)),
    ("DATA", "Movement in valuation of AFS debt securities, net of tax, FY2021", (None, None, None, 38143, None, 38143)),
    ("TOTAL", "Balance as at 31 March 2021 / 1 April 2021", (420095, 72175, 0, 2363, 12108, 506741)),
    ("DATA", "Capital contribution (share-based payments), FY2022", (None, None, None, None, 86, 86)),
    ("DATA", "Profit for the year, FY2022", (None, 10901, None, None, None, 10901)),
    ("DATA", "Movement in valuation of AFS debt securities, net of tax, FY2022", (None, None, None, -1856, None, -1856)),
    ("DATA", "Capital reduction, FY2022", (-200000, None, None, None, None, -200000)),
    ("TOTAL", "Balance as at 31 March 2022 / 1 April 2022", (220095, 83076, 0, 507, 12194, 315872)),
    ("DATA", "Capital contribution (share-based payments), FY2023", (None, None, None, None, 14, 14)),
    ("DATA", "Profit for the year, FY2023", (None, 13010, None, None, None, 13010)),
    ("DATA", "Movement in valuation of AFS debt securities, net of tax, FY2023", (None, None, None, -553, None, -553)),
    ("DATA", "Dividends paid, FY2023", (None, -10000, None, None, None, -10000)),
    ("TOTAL", "Balance as at 31 March 2023 (as originally reported in the FY2023 Annual Report)", (220095, 86086, 0, -46, 12208, 318343)),
    ("DATA", "Prior period adjustment (disclosed only in the FY2024 Annual Report, restating the 1 April 2022 opening retained earnings - see source note)", (None, -1268, None, None, None, -1268)),
    ("TOTAL", "Restated balance as at 1 April 2023 (per the FY2024 Annual Report)", (220095, 84818, 0, -46, 12208, 317075)),
    ("DATA", "Profit for the year, FY2024", (None, 28777, None, None, None, 28777)),
    ("DATA", "Movement in valuation of AFS debt securities, net of tax, FY2024", (None, None, None, 1617, None, 1617)),
    ("DATA", "Dividends paid, FY2024", (None, -10000, None, None, None, -10000)),
    ("TOTAL", "Balance as at 31 March 2024 / 1 April 2024", (220095, 103595, 0, 1571, 12208, 337469)),
    ("DATA", "Profit for the year, FY2025", (None, 26828, None, None, None, 26828)),
    ("DATA", "Movement in valuation of AFS debt securities, net of tax, FY2025", (None, None, None, 644, None, 644)),
    ("DATA", "Dividends paid, FY2025", (None, -13000, None, None, None, -13000)),
    ("TOTAL", "Closing shareholders' funds as at 31 March 2025 / 1 April 2025", (220095, 117423, 0, 2215, 12208, 351941)),
    ("DATA", "Profit for the year, FY2026", (None, 25260, None, None, None, 25260)),
    ("DATA", "Movement in valuation of AFS debt securities, net of tax, FY2026", (None, None, None, -3419, None, -3419)),
    ("DATA", "Dividends paid, FY2026", (None, -16000, None, None, None, -16000)),
    ("TOTAL", "Closing shareholders' funds as at 31 March 2026", (220095, 126683, 0, -1204, 12208, 357782)),
]

bw.add_equity_changes_sheet(
    title="ICICI Bank UK Plc — Statement of Changes in Equity",
    subtitle=(
        "USD'000, chronological, oldest to newest. Equity reconciliation ladder confirmed: each year's "
        "own closing balance ties exactly to both the next year's own opening balance and that year's own "
        "Balance Sheet Total equity, EXCEPT the FY2023 close, which is bridged by an explicit Prior period "
        "adjustment row - the FY2024 Annual Report discloses a $1,268k restatement to the 1 April 2022 "
        "opening retained earnings (not explained further in that filing) that cascades through to a "
        "different 1 April 2023 opening figure ($317,075k) than the FY2023 Annual Report's own originally-"
        "published 31 March 2023 closing figure ($318,343k). Both figures are genuine, Bank-disclosed "
        "numbers from their respective reports - shown explicitly, not force-reconciled. A Capital "
        "redemption reserve of $50,000k existed at the FY2014 opening (1 April 2013) and was "
        "cancelled into Retained earnings during FY2015 (nil from 31 March 2015 onward) - carried "
        "as its own column throughout for a clean reconciliation even though it is blank/zero after "
        "FY2015. HD-075 (2026-09-06) extended the ladder back from FY2013's opening to FY2008's "
        "opening (1 April 2007), the real statutory floor. For FY2008-FY2012, the 'Issued share "
        "capital' column combines Ordinary/Equity share capital AND Preference/Non-equity share "
        "capital into a single figure, exactly matching how the Bank's own Reconciliation of "
        "movements in shareholders' funds table presents it in every one of those years' Annual "
        "Reports (the Balance Sheet sheet, by contrast, shows them as two separate line items, "
        "matching THAT statement's own presentation - the two sheets are individually accurate to "
        "their own source table, not to each other's convention). Preference share capital ($50,000k "
        "throughout FY2008-FY2012) was redeemed to nil during FY2013 (see the 'Redemption of "
        "Preference share capital, FY2013' row), which is also when the Capital redemption reserve "
        "column first appears - both events happen in the same year, are unrelated to each other, "
        "and are shown as separate rows. Every closing balance from FY2008 to FY2013 ties exactly to "
        "the next year's own opening balance and to that year's own Balance Sheet Total Equity "
        "(single Issued-share-capital-combined total in both cases)."
    ),
    headers=EQUITY_HEADERS,
    rows=EQUITY_ROWS,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=220,
)

bw.add_cash_flow_sheet(
    title="ICICI Bank UK Plc — Cash Flow Statement",
    subtitle="Not applicable — FRS 101 cash-flow-statement exemption applies for the periods covered.",
    rows=[("SECTION", "Not applicable", {}), ("DATA", EXEMPTION_NOTE, {})],
    sources_text=EXEMPTION_NOTE + "\n\n" + ENTITY_NOTE,
    first_col_width=105,
    source_height=180,
    unit_suffix="",
    years=YEARS,
)


AQ_ROWS = [
    ("SECTION", "Loans and advances to customers, by credit risk category", {}),
    ("DATA", "Neither past due nor impaired", {"FY2026": 1304137, "FY2025": 965499, "FY2024": 837804, "FY2023": 864553, "FY2022": 1098791, "FY2021": 1465451, "FY2020": 1994801, "FY2019": 2364063, "FY2018": 2177902, "FY2017": 2113728, "FY2016": 2767417, "FY2015": 2665869, "FY2014": 2476441}),
    ("DATA", "Past due not impaired", {"FY2026": 0, "FY2025": 0, "FY2024": 43847, "FY2023": 3833, "FY2022": 69855, "FY2021": 40536, "FY2020": 18490, "FY2019": 8398, "FY2018": 6004, "FY2017": 3787, "FY2016": 74939, "FY2015": 101160, "FY2014": 123112}),
    ("DATA", "Impaired", {"FY2026": 2724, "FY2025": 8035, "FY2024": 13901, "FY2023": 75966, "FY2022": 54999, "FY2021": 55208, "FY2020": 221391, "FY2019": 216248, "FY2018": 328109, "FY2017": 312046, "FY2016": 202805, "FY2015": 172804, "FY2014": 210750}),
    ("DATA", "Impairment & collective allowances", {"FY2026": -3504, "FY2025": -9063, "FY2024": -6695, "FY2023": -44847, "FY2022": -40750, "FY2021": -39057, "FY2020": -160155, "FY2019": -165529, "FY2018": -146364, "FY2017": -97429, "FY2016": -82626, "FY2015": -61022, "FY2014": -61167}),
    ("TOTAL", "Total loans and advances to customers (net)", {"FY2026": 1303357, "FY2025": 964471, "FY2024": 888857, "FY2023": 899505, "FY2022": 1182895, "FY2021": 1522138, "FY2020": 2074527, "FY2019": 2423180, "FY2018": 2365651, "FY2017": 2332132, "FY2016": 2962535, "FY2015": 2878811, "FY2014": 2749136}),
    ("DATA", "Impaired ratio (Impaired / gross loans)", {"FY2026": "0.21%", "FY2025": "0.83%", "FY2024": "1.55%", "FY2023": "8.04%", "FY2022": "4.49%", "FY2021": "3.54%", "FY2020": "9.91%", "FY2019": "8.36%", "FY2018": "13.06%", "FY2017": "12.85%", "FY2016": "6.66%", "FY2015": "5.88%", "FY2014": "7.50%"}),
    ("DATA", "Coverage ratio (Impairment & collective allowances / Impaired)", {"FY2026": "128.63%", "FY2025": "112.79%", "FY2024": "48.16%", "FY2023": "59.03%", "FY2022": "74.09%", "FY2021": "70.75%", "FY2020": "72.34%", "FY2019": "76.55%", "FY2018": "44.61%", "FY2017": "31.22%", "FY2016": "40.75%", "FY2015": "35.31%", "FY2014": "29.02%"}),
]

bw.add_asset_quality_sheet(
    title="ICICI Bank UK Plc — Asset Quality",
    subtitle=(
        "Bank (standalone), USD'000. No IFRS 9 Stage 1/2/3 split disclosed - the Bank's own Note 19 "
        "'Potential credit risk on financial instruments' breaks the loan book into 'Neither past due nor "
        "impaired' / 'Past due not impaired' / 'Impaired' instead, confirmed by reading each year's own "
        "note in full. FY2026's and FY2025's 'Past due not impaired' are explicitly disclosed as NIL, not blank/missing (the FY2026 note states 'Past due not impaired is NIL as on 31st March 2026'). "
        "FY2016 uses that year's own originally-published figures, not the (higher Impaired / lower Past "
        "due) figures the FY2017 Annual Report's comparative column later reclassified them into - the net "
        "total and impairment allowance are identical either way. See source note at bottom."
    ),
    rows=AQ_ROWS,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=75,
    source_height=220,
    unit_suffix=" (USD'000)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(
        name, unit, rows, p3_sources(), note=note, first_col_width=58, source_height=155
    )


metric("CET1 Capital", "USD million", [("Common Equity Tier 1 (CET1) capital (FY2014-FY2016: the source labels this 'Core Tier 1', pre-dating the CET1 term)", {"FY2026": 328.4, "FY2025": 322.9, "FY2024": 311.3, "FY2023": 295.4, "FY2022": 293.0, "FY2021": 493.9, "FY2020": 440.9, "FY2019": 442.8, "FY2018": 488.8, "FY2017": 521.3, "FY2016": 537.6, "FY2015": 538.8, "FY2014": 623.8})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio (FY2014-FY2016: the source labels this 'Core Tier 1', pre-dating the CET1 term)", {"FY2026": "17.07%", "FY2025": "19.57%", "FY2024": "20.14%", "FY2023": "21.54%", "FY2022": "17.79%", "FY2021": "23.80%", "FY2020": "14.99%", "FY2019": "12.93%", "FY2018": "13.97%", "FY2017": "15.53%", "FY2016": "13.1%", "FY2015": "14.6%", "FY2014": "16.7%"})], note="FY2017-2018's own '3.1 Capital ratios' summary table also prints a second, differently-labelled 'Tier 1' row (2.83%/2.57%) that is actually the Tier 2 contribution to the total ratio (94.8/94.8 and 89.8/89.8 divided by RWA respectively), not a second CET1/Tier1 figure - confirmed against those same documents' own COREP row 62 ('Tier 1 as a percentage of total risk exposure amount'), which repeats the Core Tier 1 value exactly. The CET1/Tier1 ratio transcribed here is that COREP figure, not the mislabelled summary-table row.")
metric("Tier 1 Capital", "USD million", [("Tier 1 capital", {"FY2026": 328.4, "FY2025": 322.9, "FY2024": 311.3, "FY2023": 295.4, "FY2022": 293.0, "FY2021": 493.9, "FY2020": 440.9, "FY2019": 442.8, "FY2018": 488.8, "FY2017": 521.3, "FY2016": 537.6, "FY2015": 538.8, "FY2014": 623.8})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2026": "17.07%", "FY2025": "19.57%", "FY2024": "20.14%", "FY2023": "21.54%", "FY2022": "17.79%", "FY2021": "23.80%", "FY2020": "14.99%", "FY2019": "12.93%", "FY2018": "13.97%", "FY2017": "15.53%", "FY2016": "13.1%", "FY2015": "14.6%", "FY2014": "16.7%"})], note="See the CET1 Ratio sheet's note on FY2017-2018's mislabelled summary-table row; no Additional Tier 1 capital is disclosed in any year, so Tier 1 = CET1 throughout.")
metric("Total Capital", "USD million", [("Total capital", {"FY2026": 378.4, "FY2025": 372.9, "FY2024": 361.3, "FY2023": 371.9, "FY2022": 378.0, "FY2021": 586.7, "FY2020": 547.2, "FY2019": 576.5, "FY2018": 578.6, "FY2017": 616.1, "FY2016": 684.3, "FY2015": 707.0, "FY2014": 814.4})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2026": "19.67%", "FY2025": "22.60%", "FY2024": "23.37%", "FY2023": "27.12%", "FY2022": "22.96%", "FY2021": "28.27%", "FY2020": "18.60%", "FY2019": "16.84%", "FY2018": "16.54%", "FY2017": "18.36%", "FY2016": "16.7%", "FY2015": "19.2%", "FY2014": "21.8%"})])
metric(
    "Total RWAs",
    "USD million",
    [("Total risk-weighted exposure amount (FY2014-FY2016 are derived, not printed - see note)", {"FY2026": 1923.3, "FY2025": 1649.7, "FY2024": 1546.2, "FY2023": 1371.5, "FY2022": 1646.7, "FY2021": 2075.1, "FY2020": 2941.4, "FY2019": 3424.3, "FY2018": 3498.9, "FY2017": 3356.0, "FY2016": 4093.8, "FY2015": 3685.0, "FY2014": 3737.5})],
    note=(
        "FY2017-FY2026 are each year's own directly-printed total: UK KM1 row 4 'Total "
        "risk-weighted exposure amount' from FY2022 onward, and the transitional own funds "
        "template's row 60 'Total risk-weighted assets' for FY2017-FY2021. FY2021's figure was "
        "re-sourced on 2026-09-15 from the FY2021 edition's own row 60 and reproduces the value "
        "previously carried from the FY2022 comparative exactly.\n"
        "FY2014-FY2016 ARE DERIVED, NOT DISCLOSED. Those three editions print no total RWA "
        "figure anywhere. The values shown are that year's own printed 'Total Capital Resource "
        "requirement under Pillar 1' (FY2014 299.0, FY2015 294.8, FY2016 327.5 USD million) "
        "divided by the CRR Article 92 fixed 8% Pillar 1 minimum - the same mechanical unit "
        "conversion documented on the RWA Breakdown sheet, applied to a printed TOTAL covering "
        "credit, market and operational risk. CORRECTION 2026-09-15: this row previously "
        "described the method as 'implied from Total capital / Total capital ratio'. That "
        "description was wrong - the figures do not reproduce that way (814.4 / 21.8% = 3,735.8, "
        "not 3,737.5) and this workbook does not back-solve RWA from a capital ratio. The "
        "description has been corrected to the method actually used. The values themselves are "
        "unchanged and remain derived rather than transcribed; they are flagged as such here "
        "rather than silently presented as disclosed figures."
    ),
)

RWA_ROWS = [
    ("SECTION", "UK OV1: Overview of risk weighted exposure amounts", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2026": 1747.4, "FY2025": 1487.3, "FY2024": 1397.2, "FY2023": 1221.6, "FY2022": 1491.1, "FY2021": 1865.8, "FY2020": 2788.8, "FY2019": 3271.3, "FY2018": 3345.0, "FY2017": 3186.3, "FY2016": 3918.8, "FY2015": 3522.5, "FY2014": 3528.8}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2026": 15.9, "FY2025": 16.0, "FY2024": 21.5, "FY2023": 34.0, "FY2022": 32.1, "FY2021": 54.4}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2026": 0, "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 12.5}),
    ("DATA", "Position, foreign exchange and commodities risk (Market risk)", {"FY2026": 0, "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 36.3}),
    ("DATA", "Operational risk", {"FY2026": 160.0, "FY2025": 146.4, "FY2024": 127.5, "FY2023": 115.9, "FY2022": 123.5, "FY2021": 142.4, "FY2020": 152.5, "FY2019": 152.5, "FY2018": 153.8, "FY2017": 170.0, "FY2016": 175.0, "FY2015": 162.5, "FY2014": 172.5}),
    ("DATA", "Amounts below thresholds for deduction (subject to 250% risk weight)", {"FY2026": 5.7, "FY2025": 4.6, "FY2024": 15.0, "FY2023": 17.6, "FY2022": 22.0, "FY2021": 21.8}),
    ("TOTAL", "Total RWA", {"FY2026": 1923.3, "FY2025": 1649.7, "FY2024": 1546.2, "FY2023": 1371.5, "FY2022": 1646.7, "FY2021": 2075.1, "FY2020": 2941.4, "FY2019": 3424.3, "FY2018": 3498.9, "FY2017": 3356.0, "FY2016": 4093.8, "FY2015": 3685.0, "FY2014": 3737.5}),
]

bw.add_rwa_breakdown_sheet(
    title="ICICI Bank UK Plc — RWA Breakdown",
    subtitle=(
        "Bank (standalone), USD million. UK OV1 template - source: official Basel III Pillar 3 "
        "Disclosures. FY2014-FY2020 predate this Bank's adoption of the UK OV1 template: those years' "
        "Pillar 3 disclosures only break Pillar 1 minimum capital requirement down by risk type (Credit "
        "risk / Market risk / Operational risk), not RWA directly - the Credit risk, Market risk and "
        "Operational risk rows for FY2014-FY2020 are therefore computed as (that year's own disclosed "
        "capital requirement for the risk type) / 8% (CRR Article 92's fixed Pillar 1 minimum ratio), a "
        "mechanical unit conversion rather than an estimate; Counterparty credit risk, Securitisation and "
        "Amounts-below-thresholds are not broken out at all in those years' disclosures (folded into "
        "Credit risk) and are left blank rather than guessed. For FY2017-FY2020 the Total RWA row uses "
        "that year's own directly-disclosed 'Total risk-weighted assets' COREP figure, which does not "
        "sum exactly to the derived Credit/Market/Operational rows above it (gaps of under 0.6 USD "
        "million, i.e. rounding in the underlying capital-requirement figures) - shown explicitly rather "
        "than force-reconciled. For FY2014-FY2016, where no COREP total is disclosed at all, the Total "
        "RWA row is the same capital-requirement-derived total as used on the Total RWAs metric sheet. "
        "See source note at bottom."
    ),
    rows=RWA_ROWS,
    sources_text=p3_sources(),
    first_col_width=68,
    source_height=200,
    unit_suffix=" (USD million)",
)

# --- Leverage ratio -------------------------------------------------------------------
# TWO BASES, NEVER ONE SERIES. FY2022 onward is the UK KM1 measure, captioned by the Bank
# itself as EXCLUDING claims on central banks. FY2017-FY2021 is the older CRR LRSum/LRCom
# template, whose line 8 / line 21 "Total leverage ratio exposure" is the FULL exposure
# measure with no central-bank exclusion. The Bank flags the break itself: the FY2022
# edition leaves the 31 March 2021 comparative BLANK in KM1 rows 13/14 and says in its own
# note (h) "At March 31, 2021, the Bank's leverage ratio was 15.66% in accordance with the
# regulation applicable as at that date."
LEVERAGE_KM1_EXPOSURE = {"FY2026": 2845.7, "FY2025": 2276.7, "FY2024": 2086.8, "FY2023": 1914.3, "FY2022": 2085.6}
LEVERAGE_KM1_RATIO = {"FY2026": "11.54%", "FY2025": "14.18%", "FY2024": "14.92%", "FY2023": "15.43%", "FY2022": "14.05%"}
LEVERAGE_CRR_EXPOSURE = {"FY2021": 3153.7, "FY2020": 3747.3, "FY2019": 4153.1, "FY2018": 4180.3, "FY2017": 3731.1}
LEVERAGE_CRR_RATIO = {"FY2021": "15.7%", "FY2020": "11.8%", "FY2019": "10.7%", "FY2018": "11.7%", "FY2017": "13.97%"}

metric(
    "Leverage Ratio",
    "USD million / %",
    [
        ("UK KM1 basis (FY2022 onward) - Total exposure measure EXCLUDING claims on central banks", LEVERAGE_KM1_EXPOSURE),
        ("UK KM1 basis (FY2022 onward) - Leverage ratio excluding claims on central banks", LEVERAGE_KM1_RATIO),
        ("CRR LRCom basis (FY2017-FY2021) - Total leverage ratio exposure, INCLUDING claims on central banks", LEVERAGE_CRR_EXPOSURE),
        ("CRR LRCom basis (FY2017-FY2021) - Leverage ratio on that full exposure measure", LEVERAGE_CRR_RATIO),
    ],
    note=(
        "BASIS BREAK AT FY2022 - the two pairs of rows above are NOT one series and must not be "
        "charted or compared as one. FY2022 onward is the UK KM1 template, rows 13 and 14, which "
        "the template itself captions 'Total exposure measure EXCLUDING claims on central banks' "
        "and 'Leverage ratio excluding claims on central banks'. FY2017-FY2021 is the earlier CRR "
        "leverage disclosure template (Table LRSum line 8 / Table LRCom line 21 'Total leverage "
        "ratio exposure', ratio at LRCom line 22), which is the FULL exposure measure with no "
        "central-bank exclusion - a materially larger denominator, so the earlier ratios are "
        "structurally lower than they would be on the later basis. The Bank marks the break "
        "itself: the FY2022 edition leaves the 31 March 2021 comparative blank in KM1 rows 13/14 "
        "and explains in its own note (h) that 'At March 31, 2021, the Bank's leverage ratio was "
        "15.66% in accordance with the regulation applicable as at that date' (the FY2021 edition "
        "itself prints 15.7% - the same figure to its own rounding). FY2021's figures here are "
        "taken from the FY2021 edition's own CRR LRSum/LRCom tables, added 2026-09-15 when that "
        "edition was located; they were previously blank because the FY2022 KM1 does not carry "
        "them. The leverage ratio disclosure requirement did not yet apply to this Bank for "
        "FY2014-FY2016 and no figure appears in those years' Pillar 3 disclosures, so they are "
        "left blank rather than estimated; FY2008-FY2013's Basel II disclosures predate the "
        "leverage ratio concept entirely. Note also that the Bank states it is not itself in "
        "scope of the PRA's 3.25% minimum UK leverage requirement (that applies to LREQ firms "
        "with retail deposits of GBP 50bn or more) but manages to that level as a PRA expectation."
    ),
)

# --- LCR ------------------------------------------------------------------------------
# TWO BASES. Every edition FY2022 onward prints BOTH: KM1 row 17 (a 12-month simple average
# of month-end observations, per each edition's own note) and a narrative point-in-time
# figure "The LCR of the Bank as at March 31, XXXX was ...". They differ materially - FY2022
# is 226.90% average against 245.23% spot. FY2018-FY2021 predate KM1 and have ONLY the spot
# figure, so they belong on the point-in-time row, never on the average row.
LCR_KM1_AVERAGE = {"FY2026": "169.42%", "FY2025": "190.08%", "FY2024": "240.20%", "FY2023": "226.83%", "FY2022": "226.90%"}
LCR_POINT_IN_TIME = {
    "FY2026": "171.83%", "FY2025": "216.84%", "FY2024": "221.17%", "FY2023": "346.1%",
    "FY2022": "245.23%", "FY2021": "329.5%", "FY2020": "183.3%", "FY2019": "225.0%", "FY2018": "203.9%",
}

metric(
    "LCR",
    "%",
    [
        ("UK KM1 row 17 - 12-month average LCR (simple average of month-end observations over the 12 months preceding year end)", LCR_KM1_AVERAGE),
        ("Point-in-time LCR at 31 March, as stated in each year's own disclosure narrative", LCR_POINT_IN_TIME),
    ],
    note=(
        "TWO DIFFERENT MEASURES, SHOWN SEPARATELY - do not merge. Every edition from FY2022 "
        "onward prints both, and they differ materially (FY2022: 226.90% average vs 245.23% "
        "point-in-time; FY2023: 226.83% vs 346.1%). The average row is UK KM1 row 17, which each "
        "edition's own footnote defines as 'computed using the liquidity balances which are "
        "calculated as the simple averages of month end observations over the 12 months preceding "
        "the end of the year'. The point-in-time row is the figure each edition states in prose - "
        "'The LCR of the Bank as at March 31, XXXX was ...' (FY2018-FY2021 in the liquidity-risk "
        "section, FY2022 onward in the KM1 footnote). FY2018-FY2021 have no average figure at all "
        "because the UK KM1 template did not yet apply; they were previously sitting on a single "
        "undifferentiated 'Liquidity coverage ratio' row alongside FY2022+ averages, and were "
        "moved to the point-in-time row on 2026-09-15. FY2021's 329.5% comes from the FY2021 "
        "edition's own liquidity-risk section (the FY2022 edition's footnote independently "
        "confirms it as 329.48%); it was previously blank because the FY2022 KM1 leaves the "
        "31 March 2021 comparative empty in rows 15-17. FY2023's 346.1% is that year's own "
        "edition's figure; the FY2024 edition restates the same date to 346.08% - each year's own "
        "edition is used, per this workbook's standing convention. The Bank has maintained an LCR "
        "since October 1, 2015 per its own disclosures, but published no numeric LCR before "
        "FY2018, so FY2014-FY2017 are blank rather than estimated; FY2008-FY2013's Basel II "
        "disclosures predate the LCR entirely."
    ),
)

# --- NSFR -----------------------------------------------------------------------------
# NSFR became a UK requirement only on 1 January 2022 (PRA), so FY2014-FY2021 are
# structurally Not applicable, not blank - the Bank's own FY2018-FY2021 editions say it
# "tracks its Net Stable Funding ratio (NSFR), though it is yet to be introduced as a
# regulatory requirement in the UK".
# TWO BASES again, and the break is NOT where KM1 starts: FY2022's KM1 figure is itself
# point-in-time. FY2022 note (g): "The NSFR ratio in the above table is computed as at
# March 31, 2022." FY2023 note (h): "the average for the previous year (FY 2022) was not
# computed." Only FY2023 onward is the four-quarter average.
NSFR_NOT_APPLICABLE_YEARS = ["FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]
NSFR_KM1_AVERAGE = {
    "FY2026": "136.53%", "FY2025": "151.03%", "FY2024": "159.20%", "FY2023": "147.72%",
    # Explicit rather than blank: the FY2023 edition states "As the NSFR requirement became
    # applicable from January 1, 2022, the average for the previous year (FY 2022) was not
    # computed." A blank here would read as an unresearched gap.
    "FY2022": "Not computed - first year of the requirement",
}
NSFR_KM1_AVERAGE.update({y: "Not applicable" for y in NSFR_NOT_APPLICABLE_YEARS})
NSFR_POINT_IN_TIME = {"FY2026": "132.18%", "FY2025": "147.50%", "FY2024": "152.71%", "FY2023": "169.72%", "FY2022": "141.69%"}
NSFR_POINT_IN_TIME.update({y: "Not applicable" for y in NSFR_NOT_APPLICABLE_YEARS})

metric(
    "NSFR",
    "%",
    [
        ("UK KM1 row 20 - four-quarter average NSFR (simple average of the latest and three previous quarters)", NSFR_KM1_AVERAGE),
        ("Point-in-time NSFR at 31 March, as stated in each year's own disclosure", NSFR_POINT_IN_TIME),
    ],
    note=(
        "FY2014-FY2021 ARE 'NOT APPLICABLE', NOT MISSING. The PRA introduced the NSFR framework "
        "in the UK with effect from 1 January 2022; before that there was no UK NSFR requirement "
        "and the Bank published no figure. Its own FY2018-FY2021 editions say it 'tracks its Net "
        "Stable Funding ratio (NSFR), though it is yet to be introduced as a regulatory "
        "requirement' in the UK. These years are marked explicitly so the gap is not re-chased. "
        "FY2008-FY2013's Basel II disclosures predate the concept entirely and are outside this "
        "sheet's year range.\n"
        "BASIS BREAK AT FY2023, NOT AT FY2022. FY2022's KM1 figure of 141.69% is NOT an average: "
        "that edition's own note (g) says 'The NSFR ratio in the above table is computed as at "
        "March 31, 2022 in line with this regulation', and the FY2023 edition's note (h) confirms "
        "'As the NSFR requirement became applicable from January 1, 2022, the average for the "
        "previous year (FY 2022) was not computed'. So 141.69% sits on the point-in-time row and "
        "the average row starts at FY2023. From FY2023 each edition's own note defines the KM1 "
        "figure as 'the simple averages of four data sets covering the latest and the three "
        "previous quarters during the year' and separately states the point-in-time figure ('The "
        "NSFR of the Bank as at March 31, XXXX was ...'). The two differ materially - FY2023 "
        "147.72% average vs 169.72% spot, FY2026 136.53% vs 132.18% - and must not be merged. "
        "The point-in-time row was added 2026-09-15."
    ),
)
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": "No MREL ratio appears in the official ICICI Bank UK Basel disclosures reviewed for FY2014–FY2026; no figure has been inferred."})

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    balance_sheet_totals=[
        ("Total assets", {"FY2026": 2908251, "FY2025": 2421613, "FY2024": 2203260, "FY2023": 2142060, "FY2022": 2241973, "FY2021": 2956754, "FY2020": 3540684, "FY2019": 3840160, "FY2018": 3884340, "FY2017": 3479766, "FY2016": 4603257, "FY2015": 4129806, "FY2014": 4471154}),
        ("Loans and advances to customers", {"FY2026": 1303357, "FY2025": 964471, "FY2024": 888857, "FY2023": 899505, "FY2022": 1182895, "FY2021": 1522138, "FY2020": 2074527, "FY2019": 2423180, "FY2018": 2365651, "FY2017": 2332132, "FY2016": 2962535, "FY2015": 2878811, "FY2014": 2749136}),
        ("Customer accounts", {"FY2026": 2263521, "FY2025": 1901625, "FY2024": 1668596, "FY2023": 1617438, "FY2022": 1541957, "FY2021": 1957458, "FY2020": 2042228, "FY2019": 2140798, "FY2018": 1748820, "FY2017": 1648588, "FY2016": 2466866, "FY2015": 2284686, "FY2014": 2533259}),
        ("Total Equity", {"FY2026": 357782, "FY2025": 351941, "FY2024": 337469, "FY2023": 318343, "FY2022": 315872, "FY2021": 506741, "FY2020": 453332, "FY2019": 454331, "FY2018": 506752, "FY2017": 533230, "FY2016": 545527, "FY2015": 545428, "FY2014": 629049}),
    ],
    balance_sheet_unit="USD'000",
    income_statement_totals=[
        ("Total revenue / Net Income", {"FY2026": 90300, "FY2025": 87322, "FY2024": 85691, "FY2023": 60052, "FY2022": 54457, "FY2021": 62577, "FY2020": 79310, "FY2019": 79842, "FY2018": 83224, "FY2017": 78890, "FY2016": 87637, "FY2015": 104627, "FY2014": 90155}),
        ("Administrative expenses", {"FY2026": -57704, "FY2025": -51266, "FY2024": -46758, "FY2023": -37348, "FY2022": -38960, "FY2021": -35531, "FY2020": -37402, "FY2019": -33314, "FY2018": -34135, "FY2017": -33050, "FY2016": -33142, "FY2015": -37259, "FY2014": -35318}),
        ("Profit for the year", {"FY2026": 25260, "FY2025": 26828, "FY2024": 28777, "FY2023": 13010, "FY2022": 10901, "FY2021": 14792, "FY2020": 23249, "FY2019": -52869, "FY2018": -25548, "FY2017": -16082, "FY2016": 543, "FY2015": 18329, "FY2014": 25224}),
    ],
    income_statement_unit="USD'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2026": 351941, "FY2025": 337469, "FY2024": 317075, "FY2023": 315872, "FY2022": 506741, "FY2021": 453332, "FY2020": 454331, "FY2019": 506752, "FY2018": 533230, "FY2017": 545527, "FY2016": 545428, "FY2015": 629049, "FY2014": 622172}),
        ("Total comprehensive income/(loss) for the year", {"FY2026": 21841, "FY2025": 27472, "FY2024": 30394, "FY2023": 12457, "FY2022": 9045, "FY2021": 52935, "FY2020": -1931, "FY2019": -52956, "FY2018": -27525, "FY2017": -14086, "FY2016": -1321, "FY2015": 20723, "FY2014": 30769}),
        ("Closing equity", {"FY2026": 357782, "FY2025": 351941, "FY2024": 337469, "FY2023": 318343, "FY2022": 315872, "FY2021": 506741, "FY2020": 453332, "FY2019": 454331, "FY2018": 506752, "FY2017": 533230, "FY2016": 545527, "FY2015": 545428, "FY2014": 629049}),
    ],
    equity_changes_unit="USD'000",
    ratios=[
        ("CET1 Ratio", {"FY2026": "17.07%", "FY2025": "19.57%", "FY2024": "20.14%", "FY2023": "21.54%", "FY2022": "17.79%", "FY2021": "23.80%", "FY2020": "14.99%", "FY2019": "12.93%", "FY2018": "13.97%", "FY2017": "15.53%", "FY2016": "13.1%", "FY2015": "14.6%", "FY2014": "16.7%"}),
        ("Tier 1 Ratio", {"FY2026": "17.07%", "FY2025": "19.57%", "FY2024": "20.14%", "FY2023": "21.54%", "FY2022": "17.79%", "FY2021": "23.80%", "FY2020": "14.99%", "FY2019": "12.93%", "FY2018": "13.97%", "FY2017": "15.53%", "FY2016": "13.1%", "FY2015": "14.6%", "FY2014": "16.7%"}),
        ("Total Capital Ratio", {"FY2026": "19.67%", "FY2025": "22.60%", "FY2024": "23.37%", "FY2023": "27.12%", "FY2022": "22.96%", "FY2021": "28.27%", "FY2020": "18.60%", "FY2019": "16.84%", "FY2018": "16.54%", "FY2017": "18.36%", "FY2016": "16.7%", "FY2015": "19.2%", "FY2014": "21.8%"}),
        ("Leverage Ratio (UK KM1 basis, excl. central banks - FY2022 onward)", LEVERAGE_KM1_RATIO),
        ("Leverage Ratio (CRR LRCom basis, full exposure incl. central banks - FY2017-FY2021)", LEVERAGE_CRR_RATIO),
        ("LCR (UK KM1 12-month average - FY2022 onward)", LCR_KM1_AVERAGE),
        ("LCR (point-in-time at 31 March)", LCR_POINT_IN_TIME),
        ("NSFR (UK KM1 four-quarter average - FY2023 onward)", NSFR_KM1_AVERAGE),
        ("NSFR (point-in-time at 31 March - FY2022 onward)", NSFR_POINT_IN_TIME),
    ],
    note="ICICI Bank UK Plc's FRS 101 cash-flow exemption means no cash-flow summary or chart is shown (5 blocks total: Balance Sheet, P&L, Equity, and Ratios - no Cash Flow block). All statement figures are Bank-standalone USD, kept in the Bank's own native reporting currency (not converted to £) for consistency with the pre-existing Pillar 3 sheets, which are also USD. FY2026 (year ended 31 March 2026) was added 2026-09-15 from the Bank's own website - its Annual Report and Pillar 3 disclosure are both published there ahead of the Companies House filing, whose latest accounts are still those for 31 March 2025. Extended back to FY2014 (from FY2021) under HD-046, capped at FY2014 by explicit project-wide decision even though the Bank's own archive goes back further (see wayfinder/historical-depth/tickets/HD-046.md). Leverage Ratio and LCR are blank before FY2017/FY2018 respectively (not yet disclosed as a published figure by the Bank) and NSFR is marked 'Not applicable' before FY2022 (the PRA introduced the UK NSFR framework only with effect from 1 January 2022) - neither is force-filled. 2026-09-15: each of Leverage Ratio, LCR and NSFR is now split across TWO rows because each spans a genuine definitional break, and the two rows in each pair must not be read, charted or compared as one series - Leverage breaks at FY2022 (UK KM1 measure excluding central-bank claims, vs the earlier CRR LRCom full exposure measure that includes them), LCR breaks at FY2022 (UK KM1 12-month average vs the point-in-time figure each edition states in prose, which for FY2022 differ by 18pp and for FY2023 by 119pp), and NSFR breaks at FY2023, NOT FY2022 (the FY2022 KM1 figure is itself point-in-time by that edition's own note, since the four-quarter average could not be computed in the requirement's first year). See each metric sheet's own note for the verbatim source wording establishing each break.",
)

bw.save("/Users/armaan/code/katalysis/banks/ICICI BANK UK FINANCIALS.xlsx")
