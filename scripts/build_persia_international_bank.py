import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzQ3OTMzNTI0NWFkaXF6a2N4/document?download=0&format=pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzQzMzA4NzcwMWFkaXF6a2N4/document?download=0&format=pdf"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzM4OTExNTc1NmFkaXF6a2N4/document?download=0&format=pdf"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzM1NTU5ODQzNmFkaXF6a2N4/document?download=0&format=pdf"
PILLAR3_2021_URL = "https://www.persiabank.co.uk/Pillar%203%202021%20v3.pdf"

# HD-021 (extend to FY2015) source documents: Companies House full-accounts filings
# (scanned, no text layer - transcribed from page images) plus Wayback Machine snapshots
# of the Bank's own standalone Pillar 3 disclosures for FY2016/FY2018/FY2020 (its own
# site refused live TLS connections this session, same as the FY2021 Pillar 3 document
# above). No standalone Pillar 3 document was locatable for FY2017 or FY2019; those two
# years' regulatory-capital figures are instead the FY2017/FY2019 comparative columns
# printed inside the FY2018/FY2020 Pillar 3 documents respectively.
AR2020_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzI4MjYzOTE2OGFkaXF6a2N4/document?download=0&format=pdf"
AR2019_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzI0MDMwNDExNmFkaXF6a2N4/document?download=0&format=pdf"
AR2018_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzIxMjI1ODQ3MmFkaXF6a2N4/document?download=0&format=pdf"
AR2017_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzE4MTE5NDQwMWFkaXF6a2N4/document?download=0&format=pdf"
AR2016_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzE1NjI0NzM2OWFkaXF6a2N4/document?download=0&format=pdf"
AR2015_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzEyNzM3Mjc4NWFkaXF6a2N4/document?download=0&format=pdf"
PILLAR3_2020_URL = (
    "http://web.archive.org/web/20220125010012if_/http://www.persiabank.co.uk/Pillar%203%202020%20v7.pdf"
)
PILLAR3_2018_URL = (
    "http://web.archive.org/web/20180902131909if_/http://www.persiabank.co.uk/"
    "Pillar%203%20Disclosure%20as%20at%2031_03_2018%20(final).pdf"
)
PILLAR3_2016_URL = (
    "http://web.archive.org/web/20161024202355if_/http://www.persiabank.co.uk/"
    "Pillar%203%20Disclosure%20as%20at%2031%20March%202016.pdf"
)

# The Bank reports in EUR and discloses its own EUR/GBP rates in the accounting
# policies.  Rates are EUR per GBP, so EUR / rate = GBP.  FY2015 and FY2016's own
# accounts disclose only an average rate for the year, not a year-end/closing rate -
# so stock (balance-sheet-type) figures for those two years cannot be converted to GBP
# and are left in EUR '000 (see stock_v/stock below, which pass EUR through unchanged
# when no year-end rate is available for that year).
AVG_RATE = {
    "FY2025": 0.8390, "FY2024": 0.8630, "FY2023": 0.8525, "FY2022": 0.8525, "FY2021": 0.8925,
    "FY2020": 0.8852, "FY2019": 0.8823, "FY2018": 0.8827, "FY2017": 0.8400, "FY2016": 0.7390, "FY2015": 0.7819,
}
YEAR_END_RATE = {
    "FY2025": 0.8350, "FY2024": 0.8550, "FY2023": 0.8800, "FY2022": 0.8475, "FY2021": 0.8525,
    "FY2020": 0.8900, "FY2019": 0.8600, "FY2018": 0.8750, "FY2017": 0.8575,
    # FY2016 and FY2015: no year-end/closing EUR/GBP rate is disclosed in either year's
    # own accounts (only an average rate) - deliberately omitted, not a transcription gap.
}

ENTITY_NOTE = (
    "ENTITY AND REPORTING BASIS: Persia International Bank Plc (company 04218020, FRN 208020) is an active UK "
    "PRA/FCA-regulated bank incorporated 16 May 2001, with registered office at 6 Lothbury, London EC2R 7HH. "
    "Companies House shows full accounts filed through the year ended 31 March 2025; the Bank is owned 60% by Bank "
    "Mellat and 40% by Bank Tejarat. These are the Company's own entity-level financial statements, prepared under "
    "UK-adopted IFRS on a going-concern basis, in EUR (the functional and presentation currency). The Bank's reports "
    "say that OFAC sanctions re-imposed in November 2018 and continuing difficulty obtaining UK clearing and "
    "correspondent-bank relationships restrict normal banking activity; Iranian exposures continue to receive a 150% "
    "risk weight because Iran is excluded from the relevant UK/EU equivalence list. The reports nevertheless state "
    "that the Bank expects to continue as a going concern. The FY2022 report's auditor highlighted material uncertainty "
    "over going concern, while later reports continued on a going-concern basis. "
    "HD-021 EXTENSION: EU/UN sanctions on the Bank (imposed 27 July 2010, annulled by the EU General Court in "
    "September 2013, re-imposed November 2013) were lifted 16 January 2016, and the FY2017 report states the PRA "
    "authorised the Bank to resume normal business on 7 November 2016 - so FY2015/FY2016 predate that resumption "
    "and describe a materially more restricted, wind-down-mode bank than FY2017 onward. BASEL II/III CAVEAT: the "
    "FY2015 accounts and the Bank's FY2015 Pillar 3 disclosure predate the UK's CRD IV Pillar 3 rollout for a firm "
    "of this size and disclose only Tier 1 / Tier 2 / Total Capital (no CET1 concept, no Leverage Ratio, no LCR); "
    "CET1, Leverage Ratio and (from FY2018) LCR are all genuinely disclosed from the Bank's FY2016 Pillar 3 "
    "disclosure onward. FY2015's own Pillar 3 disclosure separately states a Total Capital figure (EUR 151,979,000) "
    "that is EUR 518,000 lower than the FY2015 statutory accounts' own capital-management note (EUR 152,497,000, "
    "which ties to the Balance Sheet); the Pillar 3 figure appears to reuse the FY2014 year-end retained-earnings "
    "figure by mistake. This workbook uses each year's own statutory accounts' capital-management note as the "
    "authoritative Tier 1/Tier 2/Total Capital figure (consistent with every other bank in this project), and uses "
    "Pillar 3 disclosures only for figures the statutory accounts do not state at all (RWA, CET1/Total capital "
    "ratios, Leverage Ratio, LCR)."
)

FX_NOTE = (
    "FX METHODOLOGY: the Bank's accounting policies disclose EUR/GBP rates (EUR per GBP). Flow figures are divided "
    "by the year's disclosed average rate; balance figures are divided by the year's disclosed year-end rate. The "
    "cash-flow sheet includes the Bank's own exchange-difference line and a programmatic GBP translation line where "
    "the use of average rates for flows and year-end rates for balances creates a residual. FY2021 opening cash is "
    "left blank because the source does not provide a FY2020 year-end rate in the reviewed five-year source set. "
    "HD-021 EXTENSION (FY2015-FY2020): FY2017-FY2020 are converted to GBP the same way, using each year's own "
    "disclosed average/year-end rate. FY2015 and FY2016's own accounts disclose only an average EUR/GBP rate for "
    "the year, not a year-end rate - so every balance-sheet-type (stock) figure for FY2015 and FY2016 in this "
    "workbook (Balance Sheet, Asset Quality, Pillar 3 capital/RWA sheets, and equity closing balances) is shown in "
    "EUR '000, unconverted, not GBP; flow figures (P&L, cash flow, in-year equity movements) for FY2015/FY2016 are "
    "still converted to GBP using that year's own disclosed average rate. This is a genuine source limitation, not "
    "a transcription gap - see stock_v()/stock() below, which pass EUR values through unchanged for any year "
    "missing from YEAR_END_RATE."
)

CASH_FLOW_SOURCES = (
    "Sources - Persia International Bank Plc's own entity-level Statements of Cash Flows, converted from EUR to GBP "
    "using the Bank's disclosed rates (see FX note):\n"
    f"FY2025: Annual Report and Financial Statements for year ended 31 March 2025, p.39 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements for year ended 31 March 2024, p.32 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements for year ended 31 March 2023, p.31 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for year ended 31 March 2022, p.30 - {AR2022_URL}\n"
    "FY2021: FY2022 Annual Report's comparative column, p.30 - " + AR2022_URL + "\n"
    f"FY2020: Annual Report and Financial Statements for year ended 31 March 2020, p.29 (scanned Companies House "
    f"filing, transcribed from the page image) - {AR2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements for year ended 31 March 2019, p.25 (scanned filing) - {AR2019_URL}\n"
    f"FY2018: Annual Report and Financial Statements for year ended 31 March 2018, p.18 (scanned filing) - {AR2018_URL}\n"
    f"FY2017: Annual Report and Financial Statements for year ended 31 March 2017, p.16 (scanned filing) - {AR2017_URL}\n"
    f"FY2016: Annual Report and Financial Statements for year ended 31 March 2016, p.16 (scanned filing) - {AR2016_URL}\n"
    f"FY2015: Annual Report and Financial Statements for year ended 31 March 2015, p.15 (scanned filing) - {AR2015_URL}\n\n"
    + ENTITY_NOTE + "\n" + FX_NOTE + "\n\n"
    "FY2020 CASH RECONCILIATION NOTE: the FY2020 Annual Report's own Statement of Cash Flows states \"Cash and cash "
    "equivalents at the end of the year\" as EUR 174,469k, but its own supporting reconciliation table two lines "
    "below (cash at central banks EUR 27,443k + loans/advances to banks with maturity <3 months EUR 151,026k) sums "
    "to EUR 178,469k - a genuine EUR 4,000k internal inconsistency in the Bank's own document, not a transcription "
    "error here. This workbook uses EUR 178,469k (the reconciliation-table figure, which also ties to opening cash "
    "plus the year's own operating/investing/financing/FX movements) for FY2020 closing cash."
)


def p3_sources():
    return (
        "Sources - Persia International Bank Plc entity-level capital disclosures:\n"
        f"FY2025/FY2024: Annual Report and Financial Statements 2025, Note 25 (Capital management), p.77 - {AR2025_URL}\n"
        f"FY2023/FY2022: Annual Report and Financial Statements 2023, Note 26 (Capital management), p.62 - {AR2023_URL}\n"
        f"FY2021: Annual Report and Financial Statements 2022, Note 26 (Capital management), p.58 - {AR2022_URL}\n"
        f"FY2021 Pillar 3: Persia International Bank Pillar 3 Disclosure 2021, pp.16-20 and 26 - {PILLAR3_2021_URL}\n"
        "The Bank states in the FY2023-FY2025 annual reports that Pillar 3 disclosures are made separately and can "
        "be made available on request; no public 2022-2025 Pillar 3 document was locatable. The 2021 Pillar 3 document "
        "is unaudited and provides the only directly disclosed FY2021 RWA, LCR and leverage values used here."
    )


def flow(values):
    return {y: round(v / AVG_RATE[y], 1) if y in AVG_RATE else v for y, v in values.items()}


def stock(values):
    return {y: round(v / YEAR_END_RATE[y], 1) if y in YEAR_END_RATE else v for y, v in values.items()}


bw = BankWorkbook(bank_name="Persia International Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="6B3E75")


def stock_v(v, y):
    if y not in YEAR_END_RATE:
        return v
    return round(v / YEAR_END_RATE[y], 1)


def flow_v(v, y):
    if y not in AVG_RATE:
        return v
    return round(v / AVG_RATE[y], 1)


STATEMENTS_SOURCES = (
    "Sources - Persia International Bank Plc's own entity-level Statement of Comprehensive Income / Statement of "
    "Financial Position / Statement of Changes in Equity / Note 12 (Impairment) / Notes 14-16 (Cash, Loans to "
    "banks, Loans to customers), converted from EUR to GBP using the Bank's disclosed rates (see FX note):\n"
    f"FY2025: Annual Report and Financial Statements 2025, Statement of Comprehensive Income p.36, Statement of "
    f"Financial Position p.37, Statement of Changes in Equity p.38, Note 12 p.69, Notes 14-16 p.71, Credit loss "
    f"exposure/Capital management (Note 25) p.77 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements 2024, Statement of Comprehensive Income p.29, Statement of "
    f"Financial Position p.30, Statement of Changes in Equity p.31, Note 12 p.57, Notes 14-16 p.59 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, Statement of Comprehensive Income p.28, Statement of "
    f"Financial Position p.29, Statement of Changes in Equity p.30, Note 12 p.54, Notes 14-16 p.56 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, Statement of Comprehensive Income p.27, Statement of "
    f"Financial Position p.28, Statement of Changes in Equity p.29, Note 12 p.51, Notes 14-16 p.53 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2022's own comparative column (same pages as FY2022 above, "
    f"this is the latest filing that still contains a full FY2021 column) - {AR2022_URL}\n"
    f"FY2020: Annual Report and Financial Statements for year ended 31 March 2020, Statement of Comprehensive "
    f"Income p.26, Statement of Financial Position p.27, Note 28.4 (Capital management) p.62, Note 28.2 (stage-level "
    f"credit exposure) p.61 (scanned Companies House filing) - {AR2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements for year ended 31 March 2019, Statement of Comprehensive "
    f"Income p.22, Statement of Financial Position p.23, Note 28.4 (Capital management) p.58, Note 28 (stage-level "
    f"credit exposure) p.57 (scanned filing) - {AR2019_URL}\n"
    f"FY2018: Annual Report and Financial Statements for year ended 31 March 2018, Statement of Comprehensive "
    f"Income p.15, Statement of Financial Position p.16, capital management note p.31, loan-portfolio note p.30 "
    f"(scanned filing) - {AR2018_URL}\n"
    f"FY2017: Annual Report and Financial Statements for year ended 31 March 2017, Statement of Comprehensive "
    f"Income p.13, Statement of Financial Position p.14, capital management note p.28, loan-portfolio note p.27 "
    f"(scanned filing) - {AR2017_URL}\n"
    f"FY2016: Annual Report and Financial Statements for year ended 31 March 2016, Statement of Comprehensive "
    f"Income p.13, Statement of Financial Position p.14, capital management note p.27, loan-portfolio note p.26 "
    f"(scanned filing) - {AR2016_URL}\n"
    f"FY2015: Annual Report and Financial Statements for year ended 31 March 2015, Statement of Comprehensive "
    f"Income p.12, Statement of Financial Position p.13, capital management note p.31, loan-portfolio note p.30 "
    f"(scanned filing, includes an embedded Pillar 3 disclosure at pp.35-52) - {AR2015_URL}\n\n"
    + ENTITY_NOTE + "\n" + FX_NOTE + "\n\n"
    "RESTATEMENT: the Annual Report and Financial Statements 2024's own Note 33 restates the Bank's FY2022/FY2023 "
    "figures (e.g. FY2023 closing retained earnings restated from EUR (17,439k) to EUR (18,414k), a genuine "
    "EUR 975k downward adjustment; FY2023 loans and advances to customers also restated from EUR 24,653k net to "
    "EUR 28,105k net, reclassifying interest receivable into that line). Each year's Balance Sheet/P&L/Equity "
    "column here uses that year's own originally-reported figures (not the later restated comparative), "
    "consistent with every other bank in this project; the restatement is instead shown as its own explicit "
    "bridging row in the Statement of Changes in Equity, between FY2023's originally-reported closing balance "
    "and FY2024's own restated opening balance, per the Bank's own Note 33.\n\n"
    "DEBT SECURITIES BREAKDOWN: Note 12 (Debt securities) of both the FY2015 (p.23 of the scanned Companies House "
    "filing) and FY2016 (p.23 of the scanned Companies House filing) Annual Reports states the entire Debt securities "
    "balance is one unlisted Sukuk (Islamic) bond, classified as \"Available for sale securities - other debt "
    "securities\" and \"Issued by other than public bodies\" - i.e. 100% one measurement-basis bucket "
    "(available-for-sale/mark-to-market, no amortised-cost or FVTPL component) and 100% one issuer-type bucket "
    "(not UK government/gilts/sovereign - a non-public-body, corporate-type issuer) in both years, so no sub-row "
    "split is added; the Balance Sheet row is instead relabelled in place to state both classifications. FY2015's "
    "note carries a 90.56% impairment provision against this bond; FY2016's note raises that provision to 100% (an "
    "additional EUR 416k impairment, matching the P&L's 'Impairment charge for available-for-sale financial assets' "
    "row), which is why the FY2016 balance is nil."
)

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder confirmed: every year's own
# closing Total equity ties exactly to both the next year's own opening
# balance and that year's own Statement of Changes in Equity closing row,
# using each year's own originally-reported figures (see RESTATEMENT note
# above for the one genuine bridging item, FY2023->FY2024).
# ---------------------------------------------------------------
bs_rows_eur = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalent", {"FY2025": 77114, "FY2024": 75472, "FY2023": 51929, "FY2022": 103084, "FY2021": 25484,
        "FY2020": 27443, "FY2019": 28882, "FY2018": 30018, "FY2017": 83613, "FY2016": 151493, "FY2015": 147831}),
    ("DATA", "Loans and advances to banks", {"FY2025": 45768, "FY2024": 48056, "FY2023": 122438, "FY2022": 67577, "FY2021": 151008,
        "FY2020": 151026, "FY2019": 117079, "FY2018": 130981, "FY2017": 78708, "FY2016": 14732, "FY2015": 10336}),
    ("DATA", "Loans and advances to customers", {"FY2025": 27178, "FY2024": 49438, "FY2023": 24653, "FY2022": 32356, "FY2021": 36278,
        "FY2020": 34366, "FY2019": 13853, "FY2018": 15512, "FY2017": 28316, "FY2016": 44775, "FY2015": 50022}),
    ("DATA", "Debt securities - other debt securities, available-for-sale, issued by other than public bodies (unlisted Sukuk/Islamic Bonds; FY2015/FY2016 own reports only; no equivalent line FY2017 onward)", {"FY2016": 0, "FY2015": 435}),
    ("DATA", "Property, plant and equipment", {"FY2025": 2855, "FY2024": 3193, "FY2023": 4510, "FY2022": 3432, "FY2021": 3318,
        "FY2020": 4195, "FY2019": 4357, "FY2018": 4199, "FY2017": 4479, "FY2016": 4353, "FY2015": 4456}),
    ("DATA", "Intangible assets (FY2023 report shows this line as nil/dash; FY2015-FY2017 own reports have no separate line)", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 89, "FY2021": 268,
        "FY2020": 446, "FY2019": 625, "FY2018": 803}),
    ("DATA", "Other assets", {"FY2025": 2577, "FY2024": 1984, "FY2023": 1305, "FY2022": 2698, "FY2021": 1397,
        "FY2020": 1557, "FY2019": 901, "FY2018": 1285, "FY2017": 1070, "FY2016": 6074, "FY2015": 11021}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 134, "FY2024": 147, "FY2023": 3971, "FY2022": 652, "FY2021": 723,
        "FY2020": 961, "FY2019": 840, "FY2018": 1331, "FY2017": 1364, "FY2016": 748, "FY2015": 783}),
    ("DATA", "Current tax (FY2015-FY2019 own reports only; FY2020's own report shows this line as nil/dash)", {"FY2019": 192, "FY2018": 189, "FY2017": 193, "FY2016": 209, "FY2015": 129}),
    ("TOTAL", "Total assets", {"FY2025": 155626, "FY2024": 178290, "FY2023": 208806, "FY2022": 209888, "FY2021": 218476,
        "FY2020": 219994, "FY2019": 166729, "FY2018": 184318, "FY2017": 197743, "FY2016": 222384, "FY2015": 225013}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 37468, "FY2024": 41447, "FY2023": 68704, "FY2022": 69319, "FY2021": 78551,
        "FY2020": 83609, "FY2019": 23545, "FY2018": 33881, "FY2017": 43334, "FY2016": 65074, "FY2015": 66801}),
    ("DATA", "Deposits from customers", {"FY2025": 4597, "FY2024": 5603, "FY2023": 5608, "FY2022": 6313, "FY2021": 6270,
        "FY2020": 6299, "FY2019": 6670, "FY2018": 2880, "FY2017": 1534, "FY2016": 2687, "FY2015": 2732}),
    ("DATA", "Other liabilities / Provisions and accruals (FY2015-FY2018 own reports label this 'Provisions and accruals'; FY2019-FY2020 own reports use 'Other liabilities')", {"FY2025": 3137, "FY2024": 3547, "FY2023": 1933, "FY2022": 2498, "FY2021": 3011,
        "FY2020": 2405, "FY2019": 2415, "FY2018": 2755, "FY2017": 2524, "FY2016": 2624, "FY2015": 2983}),
    ("DATA", "Subordinated debt liabilities (FY2015-FY2020 own reports only; converted/extinguished by FY2021 - see the Statement of Changes in Equity's FY2021 share-capital-issued row)", {"FY2020": 46500, "FY2019": 46500, "FY2018": 46500, "FY2017": 46500, "FY2016": 46500, "FY2015": 46500}),
    ("TOTAL", "Total liabilities", {"FY2025": 45202, "FY2024": 50597, "FY2023": 76245, "FY2022": 78130, "FY2021": 87832,
        "FY2020": 138813, "FY2019": 79130, "FY2018": 86016, "FY2017": 93892, "FY2016": 116885, "FY2015": 119016}),
    ("SECTION", "Shareholders' equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 150000, "FY2024": 150000, "FY2023": 150000, "FY2022": 150000, "FY2021": 150000,
        "FY2020": 100000, "FY2019": 100000, "FY2018": 100000, "FY2017": 100000, "FY2016": 100000, "FY2015": 100000}),
    ("DATA", "Retained earnings", {"FY2025": -39576, "FY2024": -22307, "FY2023": -17439, "FY2022": -18242, "FY2021": -19356,
        "FY2020": -18819, "FY2019": -12401, "FY2018": -1698, "FY2017": 3851, "FY2016": 5499, "FY2015": 5997}),
    ("TOTAL", "Total shareholders' equity", {"FY2025": 110424, "FY2024": 127693, "FY2023": 132561, "FY2022": 131758, "FY2021": 130644,
        "FY2020": 81181, "FY2019": 87599, "FY2018": 98302, "FY2017": 103851, "FY2016": 105499, "FY2015": 105997}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 155626, "FY2024": 178290, "FY2023": 208806, "FY2022": 209888, "FY2021": 218476,
        "FY2020": 219994, "FY2019": 166729, "FY2018": 184318, "FY2017": 197743, "FY2016": 222384, "FY2015": 225013}),
]
bs_rows = [(kind, label, {y: stock_v(v, y) for y, v in values.items()}) for kind, label, values in bs_rows_eur]

bw.add_balance_sheet_sheet(
    title="Persia International Bank Plc — Balance Sheet",
    subtitle="Entity-level basis, £'000 converted from EUR (see FX note; FY2015/FY2016 figures are EUR '000, unconverted - "
              "no year-end EUR/GBP rate is disclosed for those two years). Each year shown on its own originally-reported basis - "
              "see the RESTATEMENT note for a genuine FY2022/FY2023 restatement disclosed in the Annual Report and Financial "
              "Statements 2024's own Note 33, bridged explicitly in the Statement of Changes in Equity rather than blended here. "
              "'Deposits from banks'/'Deposits from customers' are labelled 'Due to other banks'/'Customer accounts' in the "
              "Bank's own FY2015-FY2020 reports.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=100,
    source_height=340,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# Profit & Loss - each year's own reported structure preserved as-is
# (genuine structural differences across years, not blended): FY2021/
# FY2022's own reports show Net operating income before Administrative
# expenses/Depreciation/impairment reversal; FY2023's own report moves the
# net impairment charge/reversal into that same subtotal instead; FY2024/
# FY2025's own reports use a "Credit impairment" line within Net operating
# income and drop the standalone "Reversal of impairment" line entirely.
# ---------------------------------------------------------------
pl_rows_eur = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 7044, "FY2024": 7890, "FY2023": 6767, "FY2022": 3644, "FY2021": 3965,
        "FY2020": 2406, "FY2019": 1524, "FY2018": 2696, "FY2017": 4245, "FY2016": 5540, "FY2015": 5142}),
    ("DATA", "Interest and similar expenses", {"FY2025": -357, "FY2024": -297, "FY2023": -198, "FY2022": -456, "FY2021": -302,
        "FY2020": -368, "FY2019": -12, "FY2018": -35, "FY2017": -33, "FY2016": -45, "FY2015": -44}),
    ("TOTAL", "Net Interest Income", {"FY2025": 6687, "FY2024": 7593, "FY2023": 6569, "FY2022": 3188, "FY2021": 3663,
        "FY2020": 2038, "FY2019": 1512, "FY2018": 2661, "FY2017": 4212, "FY2016": 5495, "FY2015": 5098}),
    ("DATA", "Loan impairment (charge)/credit (FY2015-FY2018 own reports only, shown mid-statement; FY2019 onward split out below as its own late-statement line)", {"FY2018": 0, "FY2017": 1353, "FY2016": -251, "FY2015": -238}),
    ("DATA", "Impairment charge for available-for-sale financial assets (FY2016 own report only)", {"FY2016": -416}),
    ("TOTAL", "Net interest income after loan impairments (FY2015-FY2018 own reports only - those years' own statements carry this subtotal; FY2019 onward do not)", {"FY2018": 2661, "FY2017": 5565, "FY2016": 4828, "FY2015": 4860}),
    ("DATA", "Fees and commission income", {"FY2025": 75, "FY2024": 340, "FY2023": 444, "FY2022": 175, "FY2021": 184,
        "FY2020": 1565, "FY2019": 122, "FY2018": 54, "FY2017": 20, "FY2016": 31, "FY2015": 38}),
    ("DATA", "Fees and commission expense", {"FY2025": -14, "FY2024": -47, "FY2023": -109, "FY2022": -81, "FY2021": -22,
        "FY2020": -15, "FY2019": -216, "FY2018": -219, "FY2017": -156, "FY2016": -21, "FY2015": -15}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 61, "FY2024": 293, "FY2023": 335, "FY2022": 94, "FY2021": 162,
        "FY2020": 1550, "FY2019": -94}),
    ("DATA", "Other operating (expense)/income", {"FY2025": -315, "FY2024": -1347, "FY2023": 686, "FY2022": 1611, "FY2021": 842,
        "FY2020": 3, "FY2019": 150, "FY2018": 245, "FY2017": 212, "FY2016": 214, "FY2015": 46}),
    ("TOTAL", "Net fee, commission and other operating income (FY2015-FY2018 own reports only - those years' own statements sum fees and other operating income into one subtotal)", {"FY2018": 80, "FY2017": 76, "FY2016": 224, "FY2015": 69}),
    ("TOTAL", "Net operating income (FY2019/FY2020 own reports only - those years' own statements carry this subtotal, before administrative expenses)", {"FY2020": 3591, "FY2019": 1568}),
    ("DATA", "Credit impairment / Net impairment (charge)/reversal (FY2025/FY2024's own report labels this 'Credit impairment'; FY2023's own report labels it 'Net impairment (charge)/reversal')", {"FY2025": -16719, "FY2024": -3137, "FY2023": -1374}),
    ("TOTAL", "Net operating (loss)/income", {"FY2025": -10286, "FY2024": 3402, "FY2023": 6216, "FY2022": 4893, "FY2021": 4667}),
    ("DATA", "Administrative expenses", {"FY2025": -6643, "FY2024": -6964, "FY2023": -6332, "FY2022": -5261, "FY2021": -5263,
        "FY2020": -5087, "FY2019": -7131, "FY2018": -7914, "FY2017": -7035, "FY2016": -5568, "FY2015": -4220}),
    ("DATA", "Depreciation", {"FY2025": -340, "FY2024": -331, "FY2023": -185, "FY2022": -252, "FY2021": -313,
        "FY2020": -388, "FY2019": -462, "FY2018": -376, "FY2017": -254, "FY2016": -191, "FY2015": -96}),
    ("TOTAL", "Total operating expenses (FY2019/FY2020 own reports only)", {"FY2020": -5475, "FY2019": -7593}),
    ("DATA", "Net impairment (loss)/credit (FY2019/FY2020 own reports only - those years' own statements show this as a single late-statement line rather than a mid-statement loan-impairment charge)", {"FY2020": -4534, "FY2019": 186}),
    ("DATA", "Impairment of property (FY2021 only, per that year's own report)", {"FY2021": -542}),
    ("DATA", "Reversal of impairment / Net impairment reversal (FY2021-FY2023's own reports only; FY2024/FY2025's own reports fold this into 'Credit impairment' above instead)", {"FY2023": 1104, "FY2022": 1734, "FY2021": 914}),
    ("TOTAL", "Total operating expenses", {"FY2025": -6983, "FY2024": -7295, "FY2023": -5413, "FY2022": -3779, "FY2021": -5204}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": -17269, "FY2024": -3893, "FY2023": 803, "FY2022": 1114, "FY2021": -537,
        "FY2020": -6418, "FY2019": -5839, "FY2018": -5549, "FY2017": -1648, "FY2016": -707, "FY2015": 613}),
    ("DATA", "Tax on profit", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0,
        "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 209, "FY2015": -95}),
    ("TOTAL", "Profit/(loss) for the year attributable to equity holders", {"FY2025": -17269, "FY2024": -3893, "FY2023": 803, "FY2022": 1114, "FY2021": -537,
        "FY2020": -6418, "FY2019": -5839, "FY2018": -5549, "FY2017": -1648, "FY2016": -498, "FY2015": 518}),
    ("TOTAL", "Total comprehensive income/(expense) for the year attributable to equity holders", {"FY2025": -17269, "FY2024": -3893, "FY2023": 803, "FY2022": 1114, "FY2021": -537,
        "FY2020": -6418, "FY2019": -5839, "FY2018": -5549, "FY2017": -1648, "FY2016": -498, "FY2015": 518}),
]
pl_rows = [(kind, label, {y: flow_v(v, y) for y, v in values.items()}) for kind, label, values in pl_rows_eur]

bw.add_income_statement_sheet(
    title="Persia International Bank Plc — Profit & Loss",
    subtitle="Entity-level basis, £'000 converted from EUR (see FX note). Structure genuinely differs year to year - see the "
              "'Credit impairment / Net impairment (charge)/reversal' and 'Reversal of impairment' row notes. FY2021's own "
              "report uniquely shows a standalone 'Impairment of property' charge alongside a separate impairment reversal. "
              "The Bank reports no OCI in any year - Total comprehensive income/(expense) equals Profit/(loss) for the year "
              "in every year. FY2015-FY2020 (EUR '000 shown for FY2015/FY2016, £'000 for FY2017-FY2020 - see FX note) use "
              "three more structures again: FY2015-FY2018's own statements subtotal 'Net interest income after loan "
              "impairments' mid-statement then fold fees/other-operating income into one combined subtotal; FY2019/FY2020's "
              "own statements instead carry a 'Net operating income' subtotal (before administrative expenses) and a "
              "'Net impairment (loss)/credit' as a single late-statement line, closer to FY2021 onward's shape.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=120,
    source_height=340,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - chronological roll-forward. Ladder
# confirmed in EUR terms across all 5 years (100,000+50,000-537=150,000
# share capital / -18,819+0-537=-19,356 retained earnings roll into
# FY2021's own closing balance; each subsequent year's own profit/loss
# rolls cleanly; the one genuine break is the EUR 975k restatement
# disclosed in the Annual Report and Financial Statements 2024's own Note
# 33, shown below as its own explicit row). The very first opening
# balance (1 April 2020) cannot be converted to GBP - the Bank's disclosed
# EUR/GBP rate series in this workbook's source set only starts at
# FY2021 - so that one row is shown in EUR only, per this workbook's
# established FX-gap convention (see the Cash Flow Statement's FY2021
# opening cash note for the same convention applied there).
# ---------------------------------------------------------------
equity_headers = ["Issued share capital", "Retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "At 1 April 2014 (FY2015 opening; EUR '000, unconverted - no FY2014 year-end EUR/GBP rate disclosed)", (100000, 5479, 105479)),
    ("DATA", "Profit for the year (FY2015; EUR '000, unconverted - see FX note)", (None, 518, 518)),
    ("TOTAL", "At 31 March 2015 (FY2015 closing; EUR '000, unconverted)", (100000, 5997, 105997)),
    ("DATA", "Loss for the year (FY2016; EUR '000, unconverted - see FX note)", (None, -498, -498)),
    ("TOTAL", "At 31 March 2016 (FY2016 closing; EUR '000, unconverted)", (100000, 5499, 105499)),
    ("DATA", "Loss for the year", (None, flow_v(-1648, "FY2017"), flow_v(-1648, "FY2017"))),
    ("TOTAL", "At 31 March 2017 (FY2017 closing)", (stock_v(100000, "FY2017"), stock_v(3851, "FY2017"), stock_v(103851, "FY2017"))),
    ("DATA", "Loss for the year", (None, flow_v(-5549, "FY2018"), flow_v(-5549, "FY2018"))),
    ("TOTAL", "At 31 March 2018 (FY2018 closing)", (stock_v(100000, "FY2018"), stock_v(-1698, "FY2018"), stock_v(98302, "FY2018"))),
    ("DATA", "Loss for the year", (None, flow_v(-5839, "FY2019"), flow_v(-5839, "FY2019"))),
    ("TOTAL", "At 31 March 2019 (FY2019 closing)", (stock_v(100000, "FY2019"), stock_v(-12401, "FY2019"), stock_v(87599, "FY2019"))),
    ("DATA", "Loss for the year", (None, flow_v(-6418, "FY2020"), flow_v(-6418, "FY2020"))),
    ("TOTAL", "At 31 March 2020 (FY2020 closing; source EUR 100,000 / (18,819) / 81,181)", (stock_v(100000, "FY2020"), stock_v(-18819, "FY2020"), stock_v(81181, "FY2020"))),
    ("TOTAL", "At 1 April 2020 (FY2021 opening; source EUR 100,000 / (18,819) / 81,181 - GBP conversion not available, no FY2020 year-end rate in the disclosed source set)", (None, None, None)),
    ("DATA", "Ordinary share capital issued", (flow_v(50000, "FY2021"), None, flow_v(50000, "FY2021"))),
    ("DATA", "Loss for the year", (None, flow_v(-537, "FY2021"), flow_v(-537, "FY2021"))),
    ("TOTAL", "At 31 March 2021 (FY2021 closing)", (stock_v(150000, "FY2021"), stock_v(-19356, "FY2021"), stock_v(130644, "FY2021"))),
    ("DATA", "Profit for the year", (None, flow_v(1114, "FY2022"), flow_v(1114, "FY2022"))),
    ("TOTAL", "At 31 March 2022 (FY2022 closing)", (stock_v(150000, "FY2022"), stock_v(-18242, "FY2022"), stock_v(131758, "FY2022"))),
    ("DATA", "Profit for the year", (None, flow_v(803, "FY2023"), flow_v(803, "FY2023"))),
    ("TOTAL", "At 31 March 2023 (FY2023 closing, as originally reported in the Annual Report and Financial Statements 2023)", (stock_v(150000, "FY2023"), stock_v(-17439, "FY2023"), stock_v(132561, "FY2023"))),
    ("DATA", "Prior period restatement (per the Annual Report and Financial Statements 2024's own Note 33 - a genuine EUR 975k downward adjustment to the FY2023 closing balance, not a transcription error)", (None, stock_v(-975, "FY2023"), stock_v(-975, "FY2023"))),
    ("DATA", "Loss for the year", (None, flow_v(-3893, "FY2024"), flow_v(-3893, "FY2024"))),
    ("TOTAL", "At 31 March 2024 (FY2024 closing)", (stock_v(150000, "FY2024"), stock_v(-22307, "FY2024"), stock_v(127693, "FY2024"))),
    ("DATA", "Loss for the year", (None, flow_v(-17269, "FY2025"), flow_v(-17269, "FY2025"))),
    ("TOTAL", "At 31 March 2025 (FY2025 closing)", (stock_v(150000, "FY2025"), stock_v(-39576, "FY2025"), stock_v(110424, "FY2025"))),
]

bw.add_equity_changes_sheet(
    title="Persia International Bank Plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, £'000 converted from EUR (see FX note; FY2015/FY2016 rows are "
              "EUR '000, unconverted - no year-end EUR/GBP rate is disclosed for those two years). Equity reconciliation "
              "ladder confirmed in EUR terms across all 11 years - zero undocumented plug rows. The one genuine bridging row "
              "(a EUR 975k prior period restatement) is disclosed by the Bank itself in Note 33 of the Annual Report and "
              "Financial Statements 2024, not an error found in this workbook. IMPORTANT: each £'000 cell below is an "
              "independent conversion of that row's own EUR figure at its own correct point-in-time rate (year-end rate for "
              "balances, average rate for in-year movements) - the £'000 column does not sum row-to-row the way the EUR "
              "figures do, because the Bank's EUR/GBP rate moves between each conversion point. This is a presentation "
              "artefact of converting a EUR-functional-currency ladder into GBP for this workbook, not a data error; treat "
              "each TOTAL row's £'000 value as independently correct, and see the underlying EUR figures (quoted in the "
              "'At 1 April 2020' row and the RESTATEMENT source note) for the figures that do tie exactly.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=110,
)

# EUR '000, each year's own published cash-flow column.  FY2021 is taken from
# the FY2022 comparative because that is the latest filing that contains it.
OPERATING_EUR = {"FY2025": 1998, "FY2024": -14216, "FY2023": 5116, "FY2022": 3399, "FY2021": -368,
    "FY2020": -27202, "FY2019": -3730, "FY2018": 7679, "FY2017": -3557, "FY2016": 10747, "FY2015": 14582}
INVESTING_EUR = {"FY2025": -2, "FY2024": -72, "FY2023": -46, "FY2022": -44, "FY2021": 0,
    "FY2020": 0, "FY2019": -63, "FY2018": -899, "FY2017": -380, "FY2016": -88, "FY2015": -166}
FINANCING_EUR = {"FY2025": -227, "FY2024": -27477, "FY2023": -1320, "FY2022": -9186, "FY2021": -1609,
    "FY2020": 59710, "FY2019": -11245, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0}
NET_CHANGE_EUR = {"FY2025": 1787, "FY2024": -41765, "FY2023": 3750, "FY2022": -5831, "FY2021": -1977,
    "FY2020": 32508, "FY2019": -15039, "FY2018": -1323, "FY2017": -3904, "FY2016": 10558, "FY2015": 14445}
EXCHANGE_EUR = {"FY2025": -145, "FY2024": 1009, "FY2023": -44, "FY2022": 0, "FY2021": 0,
    "FY2020": 0, "FY2019": 0, "FY2018": 4, "FY2017": 33, "FY2016": -101, "FY2015": 29}
OPENING_EUR = {"FY2025": 75472, "FY2024": 116228, "FY2023": 170661, "FY2022": 176492, "FY2021": 178469,
    "FY2020": 145961, "FY2019": 160999, "FY2018": 162321, "FY2017": 166225, "FY2016": 155667, "FY2015": 141222}
CLOSING_EUR = {"FY2025": 77114, "FY2024": 75472, "FY2023": 174367, "FY2022": 170661, "FY2021": 176492,
    # FY2020: the Bank's own Statement of Cash Flows states EUR 174,469k, but its own
    # supporting reconciliation table (two lines below) sums to EUR 178,469k - a genuine
    # EUR 4,000k inconsistency in the Bank's own document (see CASH_FLOW_SOURCES note).
    # The reconciliation-table figure is used here since it ties to opening + movements.
    "FY2020": 178469, "FY2019": 145961, "FY2018": 160999, "FY2017": 162321, "FY2016": 166225, "FY2015": 155667}

closing_gbp = stock(CLOSING_EUR)
# Opening balances are the prior year's converted closing balances.  This keeps
# the cash-flow chain internally consistent when the Bank's year-end FX rates
# differ between years.  A year is omitted from this chain (opening left blank,
# per the existing FY2021 convention) wherever the *prior* year has no disclosed
# year-end rate to convert from - that break falls at FY2021 (no FY2020 rate in the
# original five-year source set - see FX_NOTE) and at FY2017 (no FY2016 rate).
# FY2016 and FY2015 are both entirely EUR (no year-end rate for either), so their
# own opening/closing figures are self-consistent EUR-to-EUR and chain normally.
opening_gbp = {
    "FY2025": closing_gbp["FY2024"],
    "FY2024": closing_gbp["FY2023"],
    "FY2023": closing_gbp["FY2022"],
    "FY2022": closing_gbp["FY2021"],
    "FY2020": closing_gbp["FY2019"],
    "FY2019": closing_gbp["FY2018"],
    "FY2018": closing_gbp["FY2017"],
    "FY2016": closing_gbp["FY2015"],
    "FY2015": OPENING_EUR["FY2015"],
}
net_change_gbp = flow(NET_CHANGE_EUR)
exchange_gbp = flow(EXCHANGE_EUR)
translation = {
    y: round(closing_gbp[y] - opening_gbp[y] - net_change_gbp[y] - exchange_gbp[y], 1)
    for y in YEARS if y in opening_gbp
}

rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash flow from operating activities", flow(OPERATING_EUR)),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash flow from investing activities", flow(INVESTING_EUR)),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash flow from financing activities", flow(FINANCING_EUR)),
    ("TOTAL", "Net (decrease) / increase in cash and cash equivalents", net_change_gbp),
    ("DATA", "Exchange difference (Bank's own EUR statement line)", exchange_gbp),
    ("DATA", "Effect of GBP/EUR translation (this workbook's conversion line)", translation),
    ("DATA", "Cash and cash equivalents at the beginning of the year", opening_gbp),
    ("TOTAL", "Cash and cash equivalents at the end of the year", closing_gbp),
]

bw.add_cash_flow_sheet(
    title="Persia International Bank Plc — Statement of Cash Flows",
    subtitle="Entity-level basis, £'000 converted from EUR (FY2015/FY2016 figures are EUR '000, unconverted - no year-end "
              "EUR/GBP rate is disclosed for those two years; FY2017 and FY2021 opening cash are each left blank for the "
              "same reason, one year removed); see source note for sanctions, reporting basis and FX methodology",
    rows=rows, sources_text=CASH_FLOW_SOURCES, first_col_width=86, source_height=330,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# Asset Quality - built from Note 16's own component breakdown of Loans
# and advances to customers (ties exactly to the Balance Sheet net figure
# every year) plus Note 12's IFRS 9 stage split of the annual impairment
# charge/(reversal). FY2022's own component split (Commercial/Syndicated)
# differs from AR2023's later FY2022 comparative despite both giving the
# same net figure (32,356) - a genuine component-level reclassification
# between Syndicated Loans and the ECL allowance, not a data error; this
# year's own AR2022 component split is used, consistent with every other
# year using its own contemporaneous report. A genuine balance-level IFRS
# 9 stage exposure table (gross/allowance/net by stage, not just the
# annual charge) exists only in the Annual Report and Financial
# Statements 2025 (its own new "Credit loss exposure" disclosure, p.77) -
# shown as a FY2025-only supplementary block; no equivalent table was
# found in FY2021-FY2024's reports.
# ---------------------------------------------------------------
aq_rows_eur = [
    ("SECTION", "Loans and advances to customers (Note 16)", {}),
    ("DATA", "Commercial Loan", {"FY2025": 30473, "FY2024": 30221, "FY2023": 4235, "FY2022": 4235, "FY2021": 4235}),
    ("DATA", "Syndicated Loans", {"FY2025": 15334, "FY2024": 24276, "FY2023": 25804, "FY2022": 37408, "FY2021": 41486}),
    ("DATA", "Interest receivable (only disclosed as its own line FY2024-FY2025)", {"FY2025": 5526, "FY2024": 2634}),
    ("TOTAL", "Gross loans and advances to customers", {"FY2025": 51333, "FY2024": 57131, "FY2023": 30039, "FY2022": 41643, "FY2021": 45721}),
    ("DATA", "Less: expected credit loss allowance", {"FY2025": -24155, "FY2024": -7693, "FY2023": -5386, "FY2022": -9287, "FY2021": -9443}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 27178, "FY2024": 49438, "FY2023": 24653, "FY2022": 32356, "FY2021": 36278}),
]
aq_rows = [(kind, label, {y: stock_v(v, y) for y, v in values.items()}) for kind, label, values in aq_rows_eur]

aq_ratio_rows_eur = [
    ("DATA", "ECL allowance coverage ratio (allowance / gross loans)", {
        "FY2025": "47.06%", "FY2024": "13.47%", "FY2023": "17.93%", "FY2022": "22.30%", "FY2021": "20.66%",
    }),
    ("SECTION", "IFRS 9 stage split of the annual impairment charge/(reversal) (Note 12)", {}),
]
aq_stage_charge_eur = [
    ("DATA", "Stage 1 - Performing - 12 months ECL", {"FY2025": -6, "FY2024": -736, "FY2023": 2652, "FY2022": 5475, "FY2021": 5009}),
    ("DATA", "Stage 2 - Performing - lifetime ECL", {"FY2025": -6293, "FY2024": -2088, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Stage 3 - Non-performing - lifetime ECL", {"FY2025": -10420, "FY2024": -313, "FY2023": -4026, "FY2022": -3741, "FY2021": -4095}),
    ("TOTAL", "Impairment (charge)/reversal for the year", {"FY2025": -16719, "FY2024": -3137, "FY2023": -1374, "FY2022": 1734, "FY2021": 914}),
]
aq_stage_charge = [(kind, label, {y: flow_v(v, y) for y, v in values.items()}) for kind, label, values in aq_stage_charge_eur]

aq_fy25_exposure_eur = [
    ("SECTION", "FY2025-only: IFRS 9 stage-level loan exposure (Credit loss exposure table, Note 25) - no equivalent balance-level stage table found in FY2021-FY2024's reports", {}),
    ("DATA", "Stage 1 gross exposure - loans and advances to customers", {"FY2025": 49}),
    ("DATA", "Stage 2 gross exposure - loans and advances to customers", {"FY2025": 28683}),
    ("DATA", "Stage 3 gross exposure - loans and advances to customers", {"FY2025": 22650}),
    ("DATA", "Stage 1 impairment allowance", {"FY2025": -5}),
    ("DATA", "Stage 2 impairment allowance", {"FY2025": -8382}),
    ("DATA", "Stage 3 impairment allowance", {"FY2025": -14757}),
    ("TOTAL", "Net exposure - loans and advances to customers, per this stage-level table (FY2025 EUR 28,238k gross-less-allowance - EUR 1,060k / ~4% higher than Note 16's EUR 27,178k net figure used above; a genuine inconsistency between two different notes in the same Annual Report, not reconciled here)", {"FY2025": 28238}),
]
aq_fy25_exposure = [(kind, label, {y: stock_v(v, y) for y, v in values.items()}) for kind, label, values in aq_fy25_exposure_eur]

# ---------------------------------------------------------------
# HD-021 extension (FY2015-FY2020) - two more structures again, both from each
# year's own "Total loan portfolio" / stage-exposure note, both tying exactly to
# that year's own Balance Sheet net "Loans and advances to customers" figure:
#   FY2015-FY2018 (IAS 39 incurred-loss basis, pre-IFRS 9): gross performing +
#   gross non-performing, less a single undifferentiated allowance.
#   FY2019/FY2020 (IFRS 9 adopted): a genuine balance-level stage exposure table,
#   the same shape as the FY2025-only block above. FY2020's own source table shows
#   its Stage 1 gross-exposure column combining what would be Stage 1 and Stage 3
#   gross exposure (Stage 3 gross is not separately given even though a Stage 3
#   allowance is disclosed) - transcribed as the Bank's own table presents it,
#   flagged rather than reconciled, consistent with the FY2025 stage-table note above.
# ---------------------------------------------------------------
aq_pre_ifrs9_eur = [
    ("SECTION", "Total loan portfolio (FY2015-FY2018 own reports; IAS 39 incurred-loss basis, pre-IFRS 9 - performing/non-performing split rather than a stage table)", {}),
    ("DATA", "Gross loans and advances to customers - performing", {"FY2018": 407, "FY2017": 6736, "FY2016": 17366, "FY2015": 19857}),
    ("DATA", "Non performing loans", {"FY2018": 19171, "FY2017": 26355, "FY2016": 33264, "FY2015": 35971}),
    ("DATA", "Less: allowance for impairment", {"FY2018": -4066, "FY2017": -4775, "FY2016": -5855, "FY2015": -5806}),
    ("TOTAL", "Net loans and advances to customers", {"FY2018": 15512, "FY2017": 28316, "FY2016": 44775, "FY2015": 50022}),
]
aq_pre_ifrs9 = [(kind, label, {y: stock_v(v, y) for y, v in values.items()}) for kind, label, values in aq_pre_ifrs9_eur]

aq_fy19_20_exposure_eur = [
    ("SECTION", "FY2019/FY2020: IFRS 9 stage-level loan exposure (own reports' Credit risk / Risk management note)", {}),
    ("DATA", "Stage 1 gross exposure - loans and advances to customers (FY2020's own table does not separately break out Stage 3 gross exposure - see note above)", {"FY2020": 45208, "FY2019": 16109}),
    ("DATA", "Stage 3 gross exposure - loans and advances to customers", {"FY2019": 4491}),
    ("DATA", "Stage 1 impairment allowance", {"FY2020": -6265, "FY2019": -2256}),
    ("DATA", "Stage 3 impairment allowance", {"FY2020": -4577, "FY2019": -4491}),
    ("TOTAL", "Net loans and advances to customers", {"FY2020": 34366, "FY2019": 13853}),
]
aq_fy19_20_exposure = [(kind, label, {y: stock_v(v, y) for y, v in values.items()}) for kind, label, values in aq_fy19_20_exposure_eur]

bw.add_asset_quality_sheet(
    title="Persia International Bank Plc — Asset Quality",
    subtitle="Entity-level basis, £'000 converted from EUR (FY2015/FY2016 figures are EUR '000, unconverted - see FX note). "
              "Net loans and advances to customers ties exactly to the Balance Sheet every year. FY2022's own component "
              "split (Commercial/Syndicated) differs from a later report's FY2022 comparative despite both giving the "
              "identical net figure (EUR 32,356k) - a genuine component-level reclassification, not a data error; this "
              "year's own contemporaneous report is used, as elsewhere in this workbook. FY2015-FY2020 (added under "
              "HD-021) use two more structures again - see the section headers below.",
    rows=aq_rows + aq_ratio_rows_eur + aq_stage_charge + aq_fy25_exposure + aq_pre_ifrs9 + aq_fy19_20_exposure,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=110,
    source_height=340,
    unit_suffix=" (£'000, conv. from EUR)",
)

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=50, source_height=240)


CAPITAL_EUR = {"FY2025": 110424, "FY2024": 127693, "FY2023": 132561, "FY2022": 131758, "FY2021": 130644}
CAPITAL_GBP = stock(CAPITAL_EUR)
RWA_GBP = {"FY2021": round(318824 / YEAR_END_RATE["FY2021"], 1)}
NOT_DISCLOSED = (
    "Not publicly disclosed for this entity/year. The Bank says later Pillar 3 disclosures are available on request; "
    "no public 2022-2025 Pillar 3 document was found, and the statutory accounts do not state this metric."
)
CAPITAL_NOTE = (
    "Directly disclosed total regulatory capital base / Tier one capital from the annual-report capital-management "
    "table. The Bank's table does not separately disclose CET1, Additional Tier 1 or Tier 2 amounts for FY2022-FY2025; "
    "the value is therefore repeated as the entity's disclosed Tier one/regulatory capital base, not inferred as a full "
    "Basel capital stack. FY2021's Pillar 3 table reports Own Funds of €130.644m and Tier 2 of zero."
)

# ---------------------------------------------------------------
# HD-021 extension (FY2015-FY2020). Two source layers, used for different rows:
#   - Each year's own STATUTORY capital-management note (in the Annual Report itself)
#     gives Tier 1 = Ordinary share capital + Retained earnings (== Balance Sheet
#     Total shareholders' equity every year) and Tier 2 = the subordinated loan at
#     its full carrying value (EUR 46,500k every year). This workbook uses these
#     statutory figures for the CET1/Tier 1/Total Capital £-value sheets, consistent
#     with using each year's own accounts as the primary source elsewhere.
#   - The Bank's own standalone Pillar 3 disclosures (found for FY2016/FY2018/FY2020,
#     each of which also prints the prior year's figures as a comparative, covering
#     FY2017 and FY2019 too) separately disclose CET1/Total-capital RATIOS and RWA -
#     neither of which the statutory accounts state at all - computed against a
#     CRR-CAPPED Tier 2 (capped at 1/3 of Tier 1 from 1 January 2017) and, for
#     FY2019/FY2020, a CET1 base that nets off that year's own unaudited in-year
#     loss a second time (Pillar 3 FY2020 CET1 EUR 74,763k = statutory equity EUR
#     81,181k less that year's own EUR 6,418k loss again - a CRR prudential filter
#     for not-yet-verified profits/losses, not a transcription error). This workbook
#     uses these Pillar-3-disclosed ratios and RWA figures as-is (they cannot be
#     derived from the statutory £-values above without re-deriving the capping/
#     filter mechanics), so the ratio sheets' own capital base differs from the
#     Total Capital sheet's - flagged here rather than silently reconciled.
# FY2015 predates CRD IV Pillar 3 for a firm this size: only Tier 1/Tier 2/Total
# Capital are disclosed (no CET1, no RWA-by-risk-type split, no Leverage Ratio, no
# LCR) - see ENTITY_NOTE's Basel II/III caveat.
# ---------------------------------------------------------------
TIER1_STATUTORY_EUR = {"FY2020": 81181, "FY2019": 87599, "FY2018": 98302, "FY2017": 103851, "FY2016": 105499, "FY2015": 105997}
TIER2_STATUTORY_EUR = {"FY2020": 46500, "FY2019": 46500, "FY2018": 46500, "FY2017": 46500, "FY2016": 46500, "FY2015": 46500}
TOTAL_CAPITAL_STATUTORY_EUR = {"FY2020": 127681, "FY2019": 134099, "FY2018": 144802, "FY2017": 150351, "FY2016": 151999, "FY2015": 152497}

CET1_TIER1_PILLAR3_EUR = {"FY2020": 74763, "FY2019": 81760, "FY2018": 98302, "FY2017": 103851, "FY2016": 105499}
RWA_CREDIT_EUR = {"FY2020": 262907, "FY2019": 169506, "FY2018": 210723, "FY2017": 243264, "FY2016": 306733}
RWA_MARKET_EUR = {"FY2020": 7355, "FY2019": 6771, "FY2018": 4031, "FY2017": 3604, "FY2016": 3036}
RWA_OPERATIONAL_EUR = {"FY2020": 11212, "FY2019": 7967, "FY2018": 7967, "FY2017": 9514, "FY2016": 9998}
RWA_TOTAL_EUR_EXT = {"FY2020": 281474, "FY2019": 184244, "FY2018": 222721, "FY2017": 256382, "FY2016": 319767, "FY2015": 221221}
CET1_RATIO_EXT = {"FY2020": "28.76%", "FY2019": "50.16%", "FY2018": "44.14%", "FY2017": "40.51%", "FY2016": "32.99%"}
TOTAL_CAPITAL_RATIO_EXT = {
    "FY2020": "38.35%", "FY2019": "66.88%", "FY2018": "58.85%", "FY2017": "54.01%", "FY2016": "47.53%",
    "FY2015": "68.94%",  # FY2015: statutory Total Capital EUR 152,497k / RWA EUR 221,221k (no Pillar 3 ratio table pre-CRD IV)
}
TIER1_RATIO_FY2015 = "47.92%"  # FY2015: statutory Tier 1 EUR 105,997k / RWA EUR 221,221k (Basel II - Tier 1 ratio, no CET1 concept)
LEVERAGE_RATIO_EXT = {"FY2020": "33.77%", "FY2018": "49.27%", "FY2016": "49.99%"}
LCR_EXT = {"FY2020": "181.69%", "FY2018": "539.22%"}

CET1_TIER1_GBP_EXT = stock(CET1_TIER1_PILLAR3_EUR)
TIER1_STATUTORY_GBP = stock(TIER1_STATUTORY_EUR)
TOTAL_CAPITAL_STATUTORY_GBP = stock(TOTAL_CAPITAL_STATUTORY_EUR)
RWA_TOTAL_GBP_EXT = stock(RWA_TOTAL_EUR_EXT)

EXT_CAPITAL_NOTE = (
    "FY2015-FY2020 (added under HD-021): the £-value shown is each year's own STATUTORY capital-management note "
    "(Tier 1 = share capital + retained earnings, tying to the Balance Sheet; FY2016-FY2018 CET1 equals this "
    "statutory Tier 1 exactly). FY2019/FY2020 differ: the Bank's own Pillar 3 disclosure nets off that year's own "
    "in-year loss from CET1 a second time (a CRR prudential filter for unverified profit/loss - see the block "
    "comment above); the Pillar-3-disclosed CET1 figure is shown for FY2019/FY2020 instead of the statutory Tier 1 "
    "figure used for FY2015-FY2018, FY2016-FY2018 and FY2021-FY2025. FY2015 has no CET1 concept at all (pre-CRD IV "
    "Pillar 3 for a firm this size) - its Tier 1 figure appears only on the Tier 1 Capital sheet."
)
EXT_TOTAL_CAPITAL_NOTE = (
    "FY2015-FY2020 (added under HD-021): each year's own statutory capital-management note, Tier 1 (share capital + "
    "retained earnings) plus Tier 2 (the EUR 46,500k subordinated loan at full carrying value, not the CRR-capped "
    "amount used in the Pillar-3-disclosed capital ratios on the Total Capital Ratio sheet)."
)
EXT_RATIO_NOTE = (
    "FY2015-FY2020 (added under HD-021): FY2016-FY2020 are directly disclosed in the Bank's own standalone Pillar 3 "
    "disclosures (found for FY2016/FY2018/FY2020; FY2017/FY2019 are those documents' own comparative columns). "
    "FY2015 predates CRD IV Pillar 3 for a firm this size (no CET1 concept, no ratio table); the FY2015 figure shown "
    "on the Total Capital Ratio / Tier 1 Ratio sheets is this workbook's own calculation from the FY2015 statutory "
    "Total Capital/Tier 1 figures divided by the FY2015 Pillar 3 disclosure's own Total RWA figure (EUR 221,221k, "
    "the 'Breakdown of exposure classes' table's own total - not the same total as its mislabelled Template CR4 "
    "table, see the RWA Breakdown sheet's note)."
)
EXT_RWA_NOTE = (
    "FY2015-FY2020 (added under HD-021): FY2016-FY2020 RWA (credit/market/operational) are directly disclosed in "
    "the Bank's own standalone Pillar 3 disclosures, same sourcing as the ratio sheets. FY2015's own Pillar 3 "
    "disclosure does not break RWA down by credit/market/operational risk type at all - only by exposure class (see "
    "the RWA Breakdown sheet's note) - so only a FY2015 total is shown here, not a risk-type split."
)
EXT_LEVERAGE_LCR_NOTE = (
    "FY2015-FY2020 (added under HD-021): directly disclosed in the Bank's own standalone Pillar 3 disclosures where "
    "found (FY2016/FY2018/FY2020). No leverage ratio is disclosed in the FY2017 or FY2019 Pillar 3 comparative "
    "columns (only the current year's leverage ratio is tabulated in each document), and the EBA's LCR disclosure "
    "guidelines only applied from 31 December 2017 - so FY2015-FY2017 LCR, and FY2015 leverage ratio, are genuinely "
    "not disclosed anywhere located, not a gap in this transcription. FY2019's LCR similarly falls in a gap between "
    "the FY2018 and FY2020 Pillar 3 documents' own quarterly disclosure windows (neither one's table includes a "
    "31 March 2019 quarter)."
)

metric("CET1 Capital", "£'000 (conv. from EUR)", [("Common Equity Tier 1 capital / disclosed Tier one base",
    {**CAPITAL_GBP, **CET1_TIER1_GBP_EXT, "FY2018": TIER1_STATUTORY_GBP["FY2018"], "FY2017": TIER1_STATUTORY_GBP["FY2017"], "FY2016": TIER1_STATUTORY_GBP["FY2016"]})],
    note=CAPITAL_NOTE + "\n\n" + EXT_CAPITAL_NOTE)
metric("CET1 Ratio", "%", [("CET1 ratio", {"FY2021": "Not publicly disclosed", **CET1_RATIO_EXT})], note=NOT_DISCLOSED + "\n\n" + EXT_RATIO_NOTE)
metric("Tier 1 Capital", "£'000 (conv. from EUR)", [("Tier one / total regulatory capital base", {**CAPITAL_GBP, **TIER1_STATUTORY_GBP})], note=CAPITAL_NOTE + "\n\n" + EXT_CAPITAL_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", {"FY2021": "Not publicly disclosed", **CET1_RATIO_EXT, "FY2015": TIER1_RATIO_FY2015})], note=NOT_DISCLOSED + "\n\n" + EXT_RATIO_NOTE)
metric("Total Capital", "£'000 (conv. from EUR)", [("Total regulatory capital base", {**CAPITAL_GBP, **TOTAL_CAPITAL_STATUTORY_GBP})], note=CAPITAL_NOTE + "\n\n" + EXT_TOTAL_CAPITAL_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", {"FY2021": "Not publicly disclosed", **TOTAL_CAPITAL_RATIO_EXT})], note=NOT_DISCLOSED + "\n\n" + EXT_RATIO_NOTE)
metric("Total RWAs", "£'000 (conv. from EUR)", [("Pillar 1 risk-weighted assets", {**RWA_GBP, **RWA_TOTAL_GBP_EXT})],
    note="Only FY2021 is directly disclosed among FY2021-FY2025: €318.824m in the 2021 Pillar 3 disclosure, p.18. FY2022-FY2025 "
         "are not publicly disclosed and are not calculated from capital because no corresponding capital ratio is stated.\n\n" + EXT_RWA_NOTE)

# ---------------------------------------------------------------
# RWA Breakdown - FY2021's own Pillar 3 disclosure (Table, p.18) gives a
# genuine category-level split, recovered this session via a Wayback
# Machine snapshot after the Bank's own site (persiabank.co.uk) refused
# the TLS handshake on every direct attempt. Ties exactly to the existing
# Total RWAs figure (EUR 318,824k). FY2022-FY2025 remain not publicly
# disclosed, consistent with the Total RWAs sheet above - the Bank's own
# later Annual Reports state Pillar 3 disclosure is available on request,
# and no public standalone Pillar 3 document for those years was located.
# ---------------------------------------------------------------
RWA_BREAKDOWN_EUR = {
    "Credit and counterparty credit risk": {"FY2021": 298566, **RWA_CREDIT_EUR},
    "Market risk": {"FY2021": 15321, **RWA_MARKET_EUR},
    "Operational risk": {"FY2021": 4937, **RWA_OPERATIONAL_EUR},
}
rwa_breakdown_rows = [
    ("DATA", label, {y: stock_v(v, y) for y, v in values.items()})
    for label, values in RWA_BREAKDOWN_EUR.items()
] + [("TOTAL", "Total Pillar 1 risk-weighted assets", {**RWA_GBP, **RWA_TOTAL_GBP_EXT})]

bw.add_rwa_breakdown_sheet(
    title="Persia International Bank Plc — RWA Breakdown",
    subtitle="FY2021, plus FY2016-FY2020 added under HD-021 (recovered via Wayback Machine snapshots of the Bank's own "
              "standalone Pillar 3 disclosures, after the Bank's live site refused every direct TLS connection attempt this "
              "session). £'000 converted from EUR (FY2016 figures are EUR '000, unconverted - see FX note). Ties exactly to "
              "the Total RWAs sheet for every year shown. FY2022-FY2025 not publicly disclosed - the Bank's Annual Reports "
              "state Pillar 3 disclosure is available on request, and no public standalone Pillar 3 document for those years "
              "was located. FY2015 is NOT shown on this sheet (see Total RWAs instead): the FY2015 Pillar 3 disclosure "
              "breaks its RWA down by exposure class (Central Government/Bank, Credit institutions, Corporate companies, "
              "Securities, Short term claims on institutions, Others), not by credit/market/operational risk type, so it "
              "does not map onto this sheet's three rows without inventing a category split the source does not provide.",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Sources - Persia International Bank Plc Pillar 3 disclosures, Pillar 1 capital requirements tables:\n"
        "FY2021, p.18, recovered via Wayback Machine snapshot (captured 10 January 2026) - "
        "http://web.archive.org/web/20260110002617if_/http://www.persiabank.co.uk/Pillar%203%202021%20v3.pdf "
        "(original URL, unreachable this session due to a TLS handshake failure on every attempt: " + PILLAR3_2021_URL + ")\n"
        f"FY2020/FY2019: Pillar 3 Disclosure as at 31 March 2020, p.17, recovered via Wayback Machine (captured 25 January "
        f"2022) - {PILLAR3_2020_URL}\n"
        f"FY2018/FY2017: Pillar 3 Disclosure as at 31/03/2018, p.16, recovered via Wayback Machine (captured 2 September "
        f"2018) - {PILLAR3_2018_URL}\n"
        f"FY2016: Pillar 3 Disclosure as at 31 March 2016, p.13, recovered via Wayback Machine (captured 24 October 2016) "
        f"- {PILLAR3_2016_URL}\n\n"
        + ENTITY_NOTE + "\n" + FX_NOTE
    ),
    first_col_width=54,
    source_height=220,
    unit_suffix=" (£'000, conv. from EUR)",
)

metric("Leverage Ratio", "%", [("Leverage ratio", {"FY2021": "53.32%", **LEVERAGE_RATIO_EXT})], note="FY2021, plus FY2016/FY2018/FY2020 added under HD-021: directly disclosed in the Bank's own Pillar 3 disclosures.\n\n" + EXT_LEVERAGE_LCR_NOTE)
metric("LCR", "%", [("Liquidity Coverage Ratio (simple average of 12 monthly reports)", {"FY2021": "221.13%", **LCR_EXT})], note="FY2021, plus FY2018/FY2020 added under HD-021: directly disclosed in the Bank's own Pillar 3 disclosures.\n\n" + EXT_LEVERAGE_LCR_NOTE)
bw.add_not_disclosed_metric_sheets(["NSFR", "MREL Ratio"], p3_sources(), per_note={m: NOT_DISCLOSED for m in ["NSFR", "MREL Ratio"]})

def _row_values(rows, label):
    for kind, lbl, values in rows:
        if lbl == label:
            return values
    raise KeyError(label)


bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", _row_values(bs_rows, "Total assets")),
        ("Loans and advances to customers", _row_values(bs_rows, "Loans and advances to customers")),
        ("Deposits from customers", _row_values(bs_rows, "Deposits from customers")),
        ("Total shareholders' equity", _row_values(bs_rows, "Total shareholders' equity")),
    ],
    balance_sheet_unit="£'000 (conv. from EUR)",
    income_statement_totals=[
        ("Net Interest Income", _row_values(pl_rows, "Net Interest Income")),
        ("Total operating expenses", _row_values(pl_rows, "Total operating expenses")),
        ("Profit/(loss) for the year attributable to equity holders", _row_values(pl_rows, "Profit/(loss) for the year attributable to equity holders")),
    ],
    income_statement_unit="£'000 (conv. from EUR)",
    equity_changes_totals=[
        ("Opening equity", {"FY2022": stock_v(130644, "FY2021"), "FY2023": stock_v(131758, "FY2022"), "FY2024": stock_v(132561, "FY2023"), "FY2025": stock_v(127693, "FY2024"),
            "FY2020": stock_v(87599, "FY2019"), "FY2019": stock_v(98302, "FY2018"), "FY2018": stock_v(103851, "FY2017"), "FY2017": stock_v(105499, "FY2016"),
            "FY2016": stock_v(105997, "FY2015"), "FY2015": 105479}),
        ("Total comprehensive income/(expense) for the year", {"FY2021": flow_v(-537, "FY2021"), "FY2022": flow_v(1114, "FY2022"), "FY2023": flow_v(803, "FY2023"), "FY2024": flow_v(-3893, "FY2024"), "FY2025": flow_v(-17269, "FY2025"),
            "FY2020": flow_v(-6418, "FY2020"), "FY2019": flow_v(-5839, "FY2019"), "FY2018": flow_v(-5549, "FY2018"), "FY2017": flow_v(-1648, "FY2017"), "FY2016": flow_v(-498, "FY2016"), "FY2015": flow_v(518, "FY2015")}),
        ("Other equity movements, net (FY2021: share capital issuance; FY2024: prior period restatement per Note 33)", {"FY2021": flow_v(50000, "FY2021"), "FY2022": 0, "FY2023": 0, "FY2024": stock_v(-975, "FY2023"), "FY2025": 0,
            "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0}),
        ("Closing equity", {"FY2021": stock_v(130644, "FY2021"), "FY2022": stock_v(131758, "FY2022"), "FY2023": stock_v(132561, "FY2023"), "FY2024": stock_v(127693, "FY2024"), "FY2025": stock_v(110424, "FY2025"),
            "FY2020": stock_v(81181, "FY2020"), "FY2019": stock_v(87599, "FY2019"), "FY2018": stock_v(98302, "FY2018"), "FY2017": stock_v(103851, "FY2017"), "FY2016": stock_v(105499, "FY2016"), "FY2015": stock_v(105997, "FY2015")}),
    ],
    equity_changes_unit="£'000 (conv. from EUR)",
    cash_flow_totals=[
        ("Net cash flow from operating activities", flow(OPERATING_EUR)),
        ("Net cash flow from investing activities", flow(INVESTING_EUR)),
        ("Cash and cash equivalents at end of year", closing_gbp),
    ],
    cash_flow_unit="£'000 (conv. from EUR)",
    ratios=[("Leverage Ratio", {"FY2021": "53.32%", **LEVERAGE_RATIO_EXT}), ("LCR", {"FY2021": "221.13%", **LCR_EXT})],
    note="FY2021 leverage and LCR are the only directly disclosed regulatory liquidity metrics located in the public source "
         "set for FY2021-FY2025; later years there are intentionally blank/not disclosed. FY2016/FY2018/FY2020 leverage and "
         "FY2018/FY2020 LCR were added under HD-021 from the Bank's own standalone Pillar 3 disclosures - see the Leverage "
         "Ratio/LCR sheets for the FY2015/FY2017/FY2019 gaps. FY2021's opening equity is blank because the Bank's disclosed "
         "EUR/GBP rate series in this workbook's source set only starts at FY2021 - see the Statement of Changes in Equity "
         "sheet for detail; FY2015's opening equity (EUR 105,479k) and FY2016/FY2017's opening equity are shown unconverted "
         "or independently converted at each year's own rate for the same reason - see that sheet's own methodology note.",
)

bw.save("/Users/armaan/code/katalysis/banks/PERSIA INTERNATIONAL BANK FINANCIALS.xlsx")
