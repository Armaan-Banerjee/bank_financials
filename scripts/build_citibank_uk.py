import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# CUKL, company 11283101, FRN 124579.  The company applies the FRS 101
# IAS 7 exemption, so no statutory cash-flow statement is available (see
# EXEMPTION_NOTE). Statement-of-financial-position/income-statement/equity
# data is available for FY2019-FY2024 (full statutory accounts, 3 source
# documents each covering 2 years); Pillar 3 (capital/RWA/liquidity) data
# is available for FY2019-FY2023 (standalone CUKL Pillar 3 reports located
# for FY2019 and FY2020 during the HD-056 extend-to-FY2018 pass). No
# standalone CUKL Pillar 3 report exists for FY2024 - Citi's own naming
# scheme predicts b3p3d241231_uk.pdf and that URL returns 'asset does not
# exist' while the FY2023 equivalent still serves, so it is a genuine
# non-publication. FY2024 is therefore populated for the 3 statement sheets
# + Asset Quality, plus Total Capital / Total Capital Ratio / Leverage Ratio
# taken from section 4 of the FY2024 audited accounts (validated against the
# FY2023 Pillar 3 figures via that table's own comparative column - see
# P3_SOURCES); the remaining Pillar 3 sheets stay blank for FY2024. FY2025 is omitted entirely: statutory
# accounts not yet filed as at this build and no Pillar 3 document located.
#
# FY2018 is deliberately NOT included, despite HD-056 naming FY2018 as
# CUKL's "confirmed floor": CUKL (formerly Citi Marble Arch Limited) was
# incorporated 29 March 2018 and filed DORMANT COMPANY ACCOUNTS for FY2018
# (Companies House, filed 27 Sep 2019) showing net assets of GBP 1 and no
# income statement - it held no PRA/FCA authorisation (granted 17 May 2019)
# and had transacted no business of any kind. This was verified by reading
# the actual FY2018 filing, not assumed from the earlier scan's domain
# signal. There is therefore no genuine FY2018 figure to transcribe for
# any line on any sheet; FY2019 (the year the retail business was actually
# transferred in and CUKL began trading, per its own FY2019/FY2020 accounts)
# is the true earliest year with real financial substance, and is the new
# floor added by this pass. See CH_2018_DORMANT_URL below.
YEARS = ["FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]
YEAR_LABEL = {y: y for y in YEARS}

P3_2021_URL = "https://www.citigroup.com/rcs/citigpa/akpublic/storage/public/b3p3d211231_uk.pdf"
P3_2023_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/b3p3d231231_uk.pdf"
P3_2020_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/b3p3d201231_uk.pdf"
P3_2019_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/b3p3d191231_uk.pdf"
FS_2024_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/citibank-uk-limited-annual-fs-2024.pdf"
CH_2022_URL = "https://find-and-update.company-information.service.gov.uk/company/11283101/filing-history/MzM3OTI1NDA3NWFkaXF6a2N4/document?format=pdf&download=0"
CH_2020_URL = "https://find-and-update.company-information.service.gov.uk/company/11283101/filing-history/MzMwODEyNzk0NGFkaXF6a2N4/document?format=pdf&download=0"
CH_2019_URL = "https://find-and-update.company-information.service.gov.uk/company/11283101/filing-history/MzI3NDY5NDc2MWFkaXF6a2N4/document?format=pdf&download=0"
CH_2018_DORMANT_URL = "https://find-and-update.company-information.service.gov.uk/company/11283101/filing-history/MzI0NTI2MzExOWFkaXF6a2N4/document?format=pdf&download=0"
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/11283101/filing-history"
REG_URL = "https://www.citigroup.com/global/investors/other-regulatory-filings"

STATEMENTS_SOURCES = (
    "Sources - Citibank UK Limited's own audited Annual Report and Financial Statements, transcribed from each "
    "year's own filing (not a later year's comparative column):\n"
    f"FY2024: Annual Financial Statements 2024, Income Statement/Statement of Comprehensive Income p.22, Statement "
    f"of Financial Position p.23, Statement of Changes in Equity p.24 (text-native PDF) - {FS_2024_URL}\n"
    f"FY2023: FY2023 comparative column in the same FY2024 document above (same pages) - {FS_2024_URL}\n"
    f"FY2022: Annual Report and Financial Statements for the year ended 31 December 2022 (Companies House filing, "
    f"scanned/image-only, visually transcribed), Income Statement/Statement of Comprehensive Income p.23, Statement "
    f"of Financial Position p.24, Statement of Changes in Equity p.25 - {CH_2022_URL}\n"
    f"FY2021: FY2021 comparative column in the same FY2022 Companies House filing above (same pages, including the "
    f"1 January 2021 opening equity balance) - {CH_2022_URL}\n"
    f"FY2020: Annual Report and Financial Statements for the year ended 31 December 2020 (Companies House filing, "
    f"text-native), Income Statement p.22, Statement of Comprehensive Income p.23, Statement of Financial Position "
    f"p.24, Statement of Changes in Equity p.25 - {CH_2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements for the year ended 31 December 2019 (Companies House filing, "
    f"text-native, CUKL's own first full-year filing after commencing trading - see ENTITY NOTE below), Income "
    f"Statement p.18, Statement of Comprehensive Income p.19, Statement of Financial Position p.20, Statement of "
    f"Changes in Equity p.21 (opening balance at 1 January 2019 is nil across every equity component, reflecting "
    f"CUKL's dormant FY2018) - {CH_2019_URL}\n"
    + "ENTITY NOTE: Citibank UK Limited (CUKL), Companies House company 11283101 and FRN 124579, is the UK legal "
    "entity covered here - not Citibank N.A. London Branch or Citibank Europe plc. CUKL's Total liabilities line "
    "on its own Statement of Financial Position combines actual liabilities with Reserves and the Profit and loss "
    "account (i.e. equity is presented within the same total as liabilities, not as a separate 'Total liabilities "
    "and equity' line) - reproduced here as the Bank's own statutory format presents it; Total assets still ties "
    "exactly to this combined Total liabilities figure every year."
)

ENTITY_NOTE = (
    "ENTITY NOTE: Citibank UK Limited (CUKL), Companies House company 11283101 and FRN 124579, is the UK legal "
    "entity covered here. CUKL's official Pillar 3 disclosures state that it has no subsidiaries and that the "
    "disclosures are prepared on a stand-alone basis. This is not Citibank N.A. London Branch or Citibank Europe plc. "
    "CUKL (formerly Citi Marble Arch Limited) was incorporated 29 March 2018 and was a dormant shell with GBP 1 net "
    "assets throughout FY2018 (Companies House dormant company accounts, filed 27 Sep 2019) - "
    f"{CH_2018_DORMANT_URL}. It was authorised by the PRA/FCA on 17 May 2019, and the Global Consumer Bank retail "
    "business (previously serviced out of Citibank Europe Plc UK branch and Citibank N.A. London Branch) was "
    "transferred to CUKL on 16 September 2019, per CUKL's own FY2019 and FY2020 accounts. FY2019 is therefore the "
    "earliest year with any real financial substance; FY2018 is not populated on any sheet in this workbook."
)

P3_SOURCES = (
    "Sources - official Citibank UK Limited standalone Pillar 3 disclosures, UK KM1 and related tables:\n"
    f"FY2024: no standalone CUKL Pillar 3 report exists for year-end 31 December 2024. The document would sit "
    f"at the same path as every prior year under Citi's own naming scheme (b3p3d<YYMMDD>_uk.pdf, i.e. "
    f"b3p3d241231_uk.pdf), and that URL returns 'asset does not exist' while the equivalent FY2023 URL still "
    f"serves its PDF - so this is a genuine non-publication, not a broken link or a naming change. The three "
    f"FY2024 figures that ARE populated below instead come from section 4 of CUKL's own audited financial "
    f"statements for the year ended 31 December 2024: '4.3. Regulatory Capital (unaudited)' (Regulatory "
    f"capital and Total capital ratio) and '4. Financial Highlights' (Leverage Ratio) - {FS_2024_URL}. Those "
    f"tables are on the same basis as the Pillar 3 KM1 they replace: their own FY2023 comparative column "
    f"(Regulatory capital GBP521,953k = GBP522.0m, Total capital ratio 90.8%, Leverage Ratio 16.71%) matches "
    f"this workbook's FY2023 Pillar 3 Total capital, Total capital ratio and Leverage ratio exactly. Note the "
    f"accounts' surrounding narrative loosely describes that line as comprising 'CET1 capital'; numerically it "
    f"is unambiguously the TOTAL capital line (FY2023 CET1 was GBP418.0m, Tier 1 GBP470.0m, Total GBP522.0m), "
    f"so it is recorded on the Total Capital sheet and NOT on the CET1 or Tier 1 sheets. CUKL redeemed its "
    f"GBP52m of Additional Tier 1 capital on 5 December 2024, so the FY2024 CET1/Tier 1/Total split cannot be "
    f"inferred from the FY2023 split either; those sheets stay blank. The accounts disclose no RWA total, no "
    f"leverage exposure measure, no LCR and no NSFR, so those stay blank rather than being back-solved from "
    f"the ratio.\n"
    f"FY2023: CUKL Pillar 3 Disclosures December 2023, pp. 3-5 and 8 - {P3_2023_URL}\n"
    f"FY2022: FY2022 comparative column in the CUKL Pillar 3 Disclosures December 2023, p. 5 - {P3_2023_URL}\n"
    f"FY2021: CUKL Pillar 3 Disclosures December 2021, pp. 6 and 15 - {P3_2021_URL}\n"
    f"FY2020: CUKL Pillar 3 Disclosures December 2020, Table 1 (KM1) p.5 - {P3_2020_URL}\n"
    f"FY2019: CUKL Pillar 3 Disclosures December 2019 (CUKL's first Pillar 3 disclosure, no comparatives - see "
    f"note below), Table 1 (KM1) p.5 - {P3_2019_URL}\n"
    f"Regulatory filing index: {REG_URL}\n"
    + ENTITY_NOTE + "\n\n"
    "MREL NOTE: the FY2019 report states MREL was introduced as an internal CUKL requirement effective 1 January "
    "2020 and that the Bank of England set it equal to CUKL's minimum capital requirement; no MREL-eligible debt "
    "had been issued as at FY2019 or FY2020, consistent with later years - no numeric MREL ratio is disclosed for "
    "any year."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: CUKL's 2024 audited financial statements state that the Company has taken the "
    "FRS 101 exemption from the requirements of IAS 7 Statement of cash flows (note 1, p. 25). The same reduced-"
    "disclosure basis is consistent with the standalone Pillar 3 reports. The 2024 accounts also state that capital "
    f"management is explained in CUKL's Basel Pillar 3 disclosures. Source: {FS_2024_URL}. Companies House filing "
    f"history for company 11283101 confirms the 2024 accounts were filed on 30 May 2025: {CH_URL}."
)

ASSET_QUALITY_SOURCES = (
    "Sources - Citibank UK Limited's own Note 12 (Risk management / Credit Risk):\n"
    f"FY2024/FY2023: Annual Financial Statements 2024, Note 12.2 Credit Risk, 'Expected credit loss' tables "
    f"(loans and advances to customers) p.58 - {FS_2024_URL}\n"
    f"FY2022/FY2021: Annual Report and Financial Statements for the year ended 31 December 2022, Note 12.2 Credit "
    f"Risk, 'Risk Ratings' classifiably-managed exposure table (by Obligor Risk Rating stage) p.58 - {CH_2022_URL}\n"
    f"FY2020: Annual Report and Financial Statements for the year ended 31 December 2020, Note 12.2 Credit Risk, "
    f"'Loans and advances to customers' IFRS 9 stage-by-stage exposure/ECL movement table (b), p.60 - {CH_2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements for the year ended 31 December 2019 (CUKL's own filing, not "
    f"the FY2020 filing's comparative column), Note 13.2 Credit Risk, 'Loans and advances to customers' IFRS 9 "
    f"stage-by-stage exposure/ECL movement table (b), p.50 - {CH_2019_URL}\n"
    + ENTITY_NOTE + "\n\n"
    "DISCLOSURE BASIS NOTE: CUKL's loan book is negligible relative to its balance sheet (a wholesale/treasury "
    "bank whose main assets are cash at central banks, treasury bills, and interbank placements) and its own ECL "
    "allowances on every asset class are correspondingly tiny (well under £0.1m in every year shown). FY2024/FY2023 "
    "use the Bank's own IFRS 9 stage-by-stage ECL movement table for 'Loans and advances to customers' (note "
    "12.2(b)). FY2022/FY2021 instead use the Bank's own 'Risk Ratings' classifiably-managed exposure table, which "
    "only breaks out the CRE (commercial real estate) loan component of the customer loan book by stage - the "
    "remainder of FY2022/FY2021's customer loans (Margin and Securities Backed Finance, a delinquency-managed "
    "retail product per the Bank's own note) is not broken out by IFRS 9 stage in either source document, so the "
    "'Loans and advances to customers, net' row for FY2022/FY2021 is the Balance Sheet's own total (not just the "
    "CRE component) while the stage split beneath it covers CRE only - documented, not blended or backfilled.\n\n"
    "FY2020/FY2019 use a THIRD basis: like FY2024/FY2023, their own Note 12.2/13.2 'Loans and advances to "
    "customers' IFRS 9 stage-by-stage table covers the FULL customer loan book (not just CRE) and reconciles "
    "exactly to the Balance Sheet's net figure every year (e.g. FY2020: 355,233 gross - 1,485 ECL = 353,748 net; "
    "FY2019: 579,400 gross - 551 ECL = 578,849 net). The narrower CRE-only stage split is specific to the "
    "FY2021/FY2022 Companies House filing's own note structure, not a general pattern across all years."
)

RWA_SOURCES = (
    "Sources - official Citibank UK Limited standalone Pillar 3 disclosures, Table 'Overview of risk weighted "
    "exposure amounts (UK OV1)':\n"
    f"FY2023/FY2022: CUKL Pillar 3 Disclosures December 2023, Table 5 (UK OV1), p.10 - {P3_2023_URL}\n"
    f"FY2021: CUKL Pillar 3 Disclosures December 2021, Table 4 (OV1), p.13 - {P3_2021_URL}\n"
    f"FY2020: CUKL Pillar 3 Disclosures December 2020, Table 6 (OV1), p.14 - {P3_2020_URL}\n"
    f"FY2019: CUKL Pillar 3 Disclosures December 2019, Table 6 (OV1), p.10 - {P3_2019_URL}\n"
    f"Regulatory filing index: {REG_URL}\n"
    + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: the FY2021 table's category labels differ slightly from FY2022/FY2023's (CCR is broken "
    "into mark-to-market/SFT sub-components in FY2021 vs a single CCR line in FY2022/FY2023; FY2021 has no "
    "'amounts below the thresholds for deduction' line, FY2022/FY2023 do) - both years' own category totals are "
    "reproduced as each report presents them, summing exactly to that year's own disclosed Total RWA (which ties "
    "to the existing Total RWAs sheet). FY2024 is blank: no standalone CUKL Pillar 3 report for FY2024 was located. "
    "FY2019/FY2020 also have no 'amounts below the thresholds for deduction' line (like FY2021), and both years' "
    "own OV1 tables report Market risk as nil ('-') under the de minimis guidance in CRR article 351 (CUKL's own "
    "FY2020 report states this explicitly) - reproduced here as 0.0, not blended with any other category."
)

bw = BankWorkbook(
    bank_name="Citibank UK Limited",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="1F3B57",
)

bw.add_balance_sheet_sheet(
    title="Citibank UK Limited — Consolidated Statement of Financial Position",
    subtitle="Company (entity-level) basis, £'000. See sources for the combined Total liabilities/equity presentation.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances at central banks", {"FY2024": 484139, "FY2023": 680797, "FY2022": 1526980, "FY2021": 1176483, "FY2020": 523979, "FY2019": 410731}),
        ("DATA", "Derivative financial instruments", {"FY2024": 2592, "FY2023": 43848, "FY2022": 201825, "FY2021": 324553, "FY2020": 135163, "FY2019": 31272}),
        ("DATA", "Treasury bills and other eligible bills", {"FY2024": 0, "FY2023": 1651630, "FY2022": 2623200, "FY2021": 2309712, "FY2020": 2113702, "FY2019": 1625349}),
        ("DATA", "Loans and advances to banks", {"FY2024": 191422, "FY2023": 173568, "FY2022": 170277, "FY2021": 1287129, "FY2020": 624621, "FY2019": 1852319}),
        ("DATA", "Loans and advances to customers", {"FY2024": 160, "FY2023": 40801, "FY2022": 70599, "FY2021": 265672, "FY2020": 353748, "FY2019": 578849}),
        ("DATA", "Debt securities", {"FY2024": 0, "FY2023": 865731, "FY2022": 1823106, "FY2021": 1756683, "FY2020": 1769954, "FY2019": 280016}),
        ("DATA", "Intangible fixed assets", {"FY2024": 24, "FY2023": 2936, "FY2022": 4467, "FY2021": 6687, "FY2020": 7339, "FY2019": 7615}),
        ("DATA", "Other assets", {"FY2024": 4174, "FY2023": 37418, "FY2022": 65125, "FY2021": 65217, "FY2020": 97394, "FY2019": 24491}),
        ("DATA", "Prepayment and accrued income", {"FY2024": 2118, "FY2023": 2488, "FY2022": 1661, "FY2021": 2148}),
        ("TOTAL", "Total assets", {"FY2024": 684629, "FY2023": 3499217, "FY2022": 6487240, "FY2021": 7194284, "FY2020": 5625900, "FY2019": 4810642}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits by banks", {"FY2024": 84, "FY2023": 9400, "FY2022": 32184, "FY2021": 8316, "FY2020": 18965, "FY2019": 5799}),
        ("DATA", "Customer accounts", {"FY2024": 140207, "FY2023": 2790344, "FY2022": 5672994, "FY2021": 6372454, "FY2020": 4983443, "FY2019": 4345627}),
        ("DATA", "Derivative financial instruments", {"FY2024": 3015, "FY2023": 43411, "FY2022": 203089, "FY2021": 320789, "FY2020": 139610, "FY2019": 31510}),
        ("DATA", "Other liabilities", {"FY2024": 8843, "FY2023": 15330, "FY2022": 19456, "FY2021": 56809, "FY2020": 21551, "FY2019": 8758}),
        ("DATA", "Accruals and deferred income", {"FY2024": 3687, "FY2023": 4877, "FY2022": 7840, "FY2021": 4868, "FY2020": 5733, "FY2019": 4090}),
        ("DATA", "Provisions for liabilities", {"FY2024": 10833, "FY2023": 10254, "FY2022": 10436, "FY2021": 850, "FY2020": 176, "FY2019": 113}),
        ("DATA", "Subordinated liabilities", {"FY2024": 0, "FY2023": 52382, "FY2022": 52237, "FY2021": 52072, "FY2020": 52092, "FY2019": 52121}),
        ("SECTION", "Equity", {}),
        ("DATA", "Called up share capital", {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0}),
        ("DATA", "Reserves", {"FY2024": 510934, "FY2023": 505184, "FY2022": 434300, "FY2021": 341987, "FY2020": 375755, "FY2019": 356341}),
        ("DATA", "Profit and loss account", {"FY2024": 7026, "FY2023": 68035, "FY2022": 54704, "FY2021": 36139, "FY2020": 28575, "FY2019": 6283}),
        ("TOTAL", "Total liabilities (incl. equity - see sources)", {"FY2024": 684629, "FY2023": 3499217, "FY2022": 6487240, "FY2021": 7194284, "FY2020": 5625900, "FY2019": 4810642}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=56,
    source_height=180,
    unit_suffix=" (£'000)",
)

bw.add_income_statement_sheet(
    title="Citibank UK Limited — Income Statement",
    subtitle="Company (entity-level) basis, £'000.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest receivable", {"FY2024": 65131, "FY2023": 160605, "FY2022": 98603, "FY2021": 42733, "FY2020": 37549, "FY2019": 17376}),
        ("DATA", "Interest payable", {"FY2024": -20935, "FY2023": -43107, "FY2022": -11677, "FY2021": -1816, "FY2020": -5318, "FY2019": -3705}),
        ("DATA", "Fees and commissions receivable", {"FY2024": 24476, "FY2023": 38466, "FY2022": 48022, "FY2021": 34505, "FY2020": 31551, "FY2019": 9380}),
        ("DATA", "Fees and commissions payable", {"FY2024": -3389, "FY2023": -4333, "FY2022": -4516, "FY2021": -5050, "FY2020": -3088, "FY2019": -578}),
        ("DATA", "Dealing profits/(loss)", {"FY2024": -70424, "FY2023": -35246, "FY2022": -606, "FY2021": 3743, "FY2020": 26886, "FY2019": 942}),
        ("DATA", "Other operating income", {"FY2024": 1093, "FY2023": 1559, "FY2022": 825, "FY2021": 530, "FY2020": 40, "FY2019": 0}),
        ("DATA", "Administrative expenses", {"FY2024": -77701, "FY2023": -95512, "FY2022": -98726, "FY2021": -61763, "FY2020": -50367, "FY2019": -12136}),
        ("DATA", "Depreciation and amortization", {"FY2024": -2913, "FY2023": -1530, "FY2022": -2187, "FY2021": -2346, "FY2020": -1979, "FY2019": -846}),
        ("DATA", "Other operating charges", {"FY2024": -7, "FY2023": -15, "FY2022": -292, "FY2021": -103, "FY2020": -377, "FY2019": -44}),
        ("DATA", "Impairment on financial assets / Provisions", {"FY2024": 53, "FY2023": 110, "FY2022": 416, "FY2021": 1309, "FY2020": -1216, "FY2019": -878}),
        ("TOTAL", "Profit/(loss) on ordinary activities before tax", {"FY2024": -84616, "FY2023": 20997, "FY2022": 29862, "FY2021": 11742, "FY2020": 33681, "FY2019": 9511}),
        ("DATA", "Tax on profit on ordinary activities", {"FY2024": 27444, "FY2023": -1016, "FY2022": -8047, "FY2021": -928, "FY2020": -8139, "FY2019": -2425}),
        ("TOTAL", "Profit/(loss) for the financial year", {"FY2024": -57172, "FY2023": 19981, "FY2022": 21815, "FY2021": 10814, "FY2020": 25542, "FY2019": 7086}),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", {"FY2024": 12450, "FY2023": 66975, "FY2022": -147555, "FY2021": -44921, "FY2020": 53343, "FY2019": -9664}),
        ("DATA", "Debt instruments at FVOCI - reclassified to profit or loss", {"FY2024": 70082, "FY2023": 26902, "FY2022": 0, "FY2021": -3980, "FY2020": -27034, "FY2019": 0}),
        ("DATA", "Related tax", {"FY2024": -24102, "FY2023": -26320, "FY2022": 39779, "FY2021": 15139, "FY2020": -6910, "FY2019": 2416}),
        ("TOTAL", "Other comprehensive income/(loss) for the year, net of tax", {"FY2024": 58430, "FY2023": 67557, "FY2022": -107776, "FY2021": -33762, "FY2020": 19399, "FY2019": -7248}),
        ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2024": 1258, "FY2023": 87538, "FY2022": -85961, "FY2021": -22948, "FY2020": 44941, "FY2019": -162}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=56,
    source_height=180,
    unit_suffix=" (£'000)",
)

bw.add_equity_changes_sheet(
    title="Citibank UK Limited — Statement of Changes in Equity",
    subtitle="Company (entity-level) basis, £'000. Read chronologically oldest-to-newest.",
    headers=["Called up share capital", "Other reserve", "Fair value reserve", "Equity reserve", "Profit and loss account", "Total"],
    rows=[
        ("TOTAL", "At 1 January 2019 (CUKL dormant throughout FY2018 - see ENTITY NOTE)", (0, 0, 0, 0, 0, 0)),
        ("DATA", "Profit for the financial year (FY2019)", (None, None, None, None, 7086, 7086)),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", (None, None, -9664, None, None, -9664)),
        ("DATA", "Tax on other comprehensive loss", (None, None, 2416, None, None, 2416)),
        ("DATA", "Capital contribution", (None, 318647, None, None, None, 318647)),
        ("DATA", "Equity decrease resulting from common control transaction", (None, -7058, None, None, None, -7058)),
        ("DATA", "Additional Tier 1 Capital", (None, 52000, None, None, None, 52000)),
        ("DATA", "Dividends on Additional Tier 1 Capital", (None, None, None, None, -803, -803)),
        ("TOTAL", "At 31 December 2019", (0, 363589, -7248, 0, 6283, 362624)),
        ("DATA", "Profit for the financial year (FY2020)", (None, None, None, None, 25542, 25542)),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", (None, None, 53343, None, None, 53343)),
        ("DATA", "Debt instruments at FVOCI - reclassified to profit or loss", (None, None, -27034, None, None, -27034)),
        ("DATA", "Tax on other comprehensive income", (None, None, -6910, None, None, -6910)),
        ("DATA", "Dividends on Additional Tier 1 Capital", (None, None, None, None, -3250, -3250)),
        ("DATA", "Equity settled share-based payment", (None, None, None, 21, None, 21)),
        ("DATA", "Tax on equity", (None, None, None, -6, None, -6)),
        ("TOTAL", "At 31 December 2020", (0, 363589, 12151, 15, 28575, 404330)),
        ("DATA", "Profit for the financial year (FY2021)", (None, None, None, None, 10814, 10814)),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", (None, None, -44921, None, None, -44921)),
        ("DATA", "Debt instruments at FVOCI - reclassified to profit or loss", (None, None, -3980, None, None, -3980)),
        ("DATA", "Tax on other comprehensive loss", (None, None, 15139, None, None, 15139)),
        ("DATA", "Capital contribution", (None, 22991, None, None, None, 22991)),
        ("DATA", "Equity decrease resulting from common control transaction", (None, -22991, None, None, None, -22991)),
        ("DATA", "Dividends on Additional Tier 1 Capital", (None, None, None, None, -3250, -3250)),
        ("DATA", "Equity settled share-based payment, net of tax", (None, None, None, -6, None, -6)),
        ("TOTAL", "At 31 December 2021", (0, 363589, -21611, 9, 36139, 378126)),
        ("DATA", "Profit for the financial year (FY2022)", (None, None, None, None, 21815, 21815)),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", (None, None, -147555, None, None, -147555)),
        ("DATA", "Tax on other comprehensive loss", (None, None, 39779, None, None, 39779)),
        ("DATA", "Capital contribution", (None, 200000, None, None, None, 200000)),
        ("DATA", "Dividends on Additional Tier 1 Capital", (None, None, None, None, -3250, -3250)),
        ("DATA", "Equity settled share-based payment", (None, None, None, 89, None, 89)),
        ("TOTAL", "At 31 December 2022", (0, 563589, -129387, 98, 54704, 489004)),
        ("DATA", "Profit for the financial year (FY2023)", (None, None, None, None, 19981, 19981)),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", (None, None, 66975, None, None, 66975)),
        ("DATA", "Debt instruments at FVOCI - reclassified to profit or loss", (None, None, 26902, None, None, 26902)),
        ("DATA", "Tax on other comprehensive loss", (None, None, -26320, None, None, -26320)),
        ("DATA", "Adjustment (reclassification within reserves - see sources)", (None, None, 3400, None, -3400, 0)),
        ("DATA", "Dividends on Additional Tier 1 Capital", (None, None, None, None, -3250, -3250)),
        ("DATA", "Equity settled share-based payment", (None, None, None, -73, None, -73)),
        ("TOTAL", "At 31 December 2023", (0, 563589, -58430, 25, 68035, 573219)),
        ("DATA", "Profit/(loss) for the financial year (FY2024)", (None, None, None, None, -57172, -57172)),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", (None, None, 12450, None, None, 12450)),
        ("DATA", "Debt instruments at FVOCI - reclassified to profit or loss", (None, None, 70082, None, None, 70082)),
        ("DATA", "Tax on other comprehensive income", (None, None, -24102, None, None, -24102)),
        ("DATA", "Dividends on Additional Tier 1 Capital", (None, None, None, None, -3837, -3837)),
        ("DATA", "Additional Tier 1 Capital redemption", (None, -52000, None, None, None, -52000)),
        ("DATA", "Equity settled share-based payment", (None, None, None, -680, None, -680)),
        ("TOTAL", "At 31 December 2024", (0, 511589, 0, -655, 7026, 517960)),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=56,
    source_height=180,
)

bw.add_cash_flow_sheet(
    title="Citibank UK Limited — Cash Flow Statement",
    subtitle="Not applicable — CUKL applies the FRS 101 IAS 7 cash-flow disclosure exemption.",
    rows=[
        ("SECTION", "No Statement of Cash Flows is published for the covered entity", {}),
        ("DATA", "Pillar-3-only scope used because the statutory cash-flow statement is exempted and unavailable.", {}),
    ],
    sources_text=ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE,
    first_col_width=90,
    source_height=230,
    unit_suffix="",
)


bw.add_asset_quality_sheet(
    title="Citibank UK Limited — Asset Quality",
    subtitle="Company (entity-level) basis, £'000. See sources - stage-split basis differs FY2024/23/20/19 vs FY2022/21.",
    rows=[
        ("SECTION", "Loan book", {}),
        ("DATA", "Loans and advances to customers, net", {"FY2024": 160, "FY2023": 40801, "FY2022": 70599, "FY2021": 265672, "FY2020": 353748, "FY2019": 578849}),
        ("SECTION", "Stage split (FY2024/23/20/19: full customer loan book; FY2022/21: CRE component only - see sources)", {}),
        ("DATA", "Stage 1 gross exposure", {"FY2024": 162, "FY2023": 40742, "FY2021": 161246, "FY2020": 240290, "FY2019": 579400}),
        ("DATA", "Stage 2 gross exposure", {"FY2023": 53, "FY2020": 114930}),
        ("DATA", "Stage 3 gross exposure", {"FY2023": 17, "FY2020": 13}),
        ("DATA", "Stage 1 ECL allowance", {"FY2024": -2, "FY2023": -11, "FY2020": -150, "FY2019": -551}),
        ("DATA", "Stage 2 ECL allowance", {"FY2020": -1322}),
        ("DATA", "Stage 3 ECL allowance", {"FY2020": -13}),
        ("TOTAL", "Total ECL allowance, closing balance", {"FY2024": -2, "FY2023": -11, "FY2022": 0, "FY2021": 0, "FY2020": -1485, "FY2019": -551}),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=56, source_height=145)


metric("CET1 Capital", "£m", [
    ("Common Equity Tier 1 (CET1) capital", {"FY2023": 418.0, "FY2022": 417.0, "FY2021": 304.2, "FY2020": 316.7, "FY2019": 291.8}),
])
metric("CET1 Ratio", "% of RWA", [
    ("Common Equity Tier 1 (CET1) ratio", {"FY2023": "72.7%", "FY2022": "59.1%", "FY2021": "37.8%", "FY2020": "32.9%", "FY2019": "33.4%"}),
])
metric("Tier 1 Capital", "£m", [
    ("Tier 1 capital", {"FY2023": 470.0, "FY2022": 469.0, "FY2021": 356.2, "FY2020": 368.7, "FY2019": 343.8}),
])
metric("Tier 1 Ratio", "% of RWA", [
    ("Tier 1 ratio", {"FY2023": "81.8%", "FY2022": "66.4%", "FY2021": "44.2%", "FY2020": "38.3%", "FY2019": "39.4%"}),
])
metric("Total Capital", "£m", [
    ("Total capital", {"FY2024": 514.5, "FY2023": 522.0, "FY2022": 521.0, "FY2021": 408.2, "FY2020": 420.7, "FY2019": 395.8}),
])
metric("Total Capital Ratio", "% of RWA", [
    ("Total capital ratio", {"FY2024": "138.6%", "FY2023": "90.8%", "FY2022": "73.8%", "FY2021": "50.7%", "FY2020": "43.7%", "FY2019": "45.3%"}),
])
metric("Total RWAs", "£m", [
    ("Total risk-weighted exposure amount", {"FY2023": 574.7, "FY2022": 706.1, "FY2021": 805.3, "FY2020": 961.6, "FY2019": 873.2}),
])
bw.add_rwa_breakdown_sheet(
    title="Citibank UK Limited — RWA Breakdown",
    subtitle="UK OV1 template, £m.",
    rows=[
        ("DATA", "Credit risk (excluding CCR)", {"FY2023": 264.1, "FY2022": 193.6, "FY2021": 419.2, "FY2020": 543.6, "FY2019": 668.2}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2023": 0.9, "FY2022": 3.4, "FY2021": 15.2, "FY2020": 39.4, "FY2019": 8.3}),
        ("DATA", "Securitisation exposures in the non-trading/banking book", {"FY2023": 124.0, "FY2022": 261.5, "FY2021": 245.9, "FY2020": 246.7, "FY2019": 28.0}),
        ("DATA", "Market risk (position, FX and commodities)", {"FY2023": 43.2, "FY2022": 106.3, "FY2021": 14.1, "FY2020": 0.0, "FY2019": 0.0}),
        ("DATA", "Operational risk", {"FY2023": 142.4, "FY2022": 141.3, "FY2021": 110.9, "FY2020": 132.0, "FY2019": 168.7}),
        ("DATA", "Amounts below the thresholds for deduction (250% risk weight)", {"FY2023": 107.2, "FY2022": 27.9}),
        ("TOTAL", "Total RWAs", {"FY2023": 574.7, "FY2022": 706.1, "FY2021": 805.3, "FY2020": 961.6, "FY2019": 873.2}),
    ],
    sources_text=RWA_SOURCES,
    first_col_width=68,
    unit_suffix=" (£m)",
)
metric("Leverage Ratio", "£m / %", [
    ("Total exposure measure", {"FY2023": 2812.0, "FY2022": 4733.0, "FY2021": 6818.1, "FY2020": 5424.1, "FY2019": 4773.6}),
    ("Leverage ratio", {"FY2024": "76.67%", "FY2023": "16.7%", "FY2022": "9.9%", "FY2021": "5.2%", "FY2020": "6.8%", "FY2019": "7.2%"}),
], note="FY2019-FY2021 are reported on the pre-2022 Basel III basis; FY2022-FY2023 use the UK KM1 leverage measure excluding claims on central banks. FY2024 has no Pillar 3 report; its 76.67% is the Leverage Ratio printed in the FY2024 audited accounts' own '4. Financial Highlights' table, whose FY2023 comparative (16.71%) matches the FY2023 Pillar 3 figure here. That table gives the ratio only - no total exposure measure - so the exposure row is blank for FY2024 rather than back-solved.")
metric("LCR", "£m / %", [
    ("Total HQLA (weighted value / average)", {"FY2023": 2988.6, "FY2022": 4476.6, "FY2021": 4219.7, "FY2020": 3069.7, "FY2019": 3474.2}),
    ("Total net cash outflows (adjusted value)", {"FY2023": 357.5, "FY2022": 687.1, "FY2021": 639.8, "FY2020": 434.5, "FY2019": 436.6}),
    ("Liquidity coverage ratio", {"FY2023": "836.0%", "FY2022": "654.5%", "FY2021": "659%", "FY2020": "707%", "FY2019": "795.8%"}),
], note="FY2019-FY2021 are based on daily averages; FY2022-FY2023 use the revised UK KM1 weighted-average presentation.")
metric("NSFR", "£m / %", [
    ("Total available stable funding", {"FY2023": 4091.4, "FY2022": 6249.1}),
    ("Total required stable funding", {"FY2023": 1018.8, "FY2022": 1839.5}),
    ("NSFR ratio", {"FY2023": "401.6%", "FY2022": "342.2%"}),
], note="NSFR was implemented in the UK reporting framework from 2022; no FY2021/FY2020/FY2019 NSFR figure is populated - CUKL's own FY2019 and FY2020 Pillar 3 reports both confirm NSFR was not yet a binding requirement.")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    P3_SOURCES,
    per_note={"MREL Ratio": "The 2021 report states that no MREL eligible debt had been issued. The 2023 report states that the BoE set CUKL's MREL requirement equal to its minimum capital requirement and that no MREL eligible debt had been issued as at 31 December 2023; no numeric MREL ratio is disclosed. The 2019 report states MREL was introduced as an internal CUKL requirement effective 1 January 2020, equal to CUKL's minimum capital requirement, and that no MREL eligible debt had been issued - consistent with FY2020 and all later years."},
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2023": "72.7%", "FY2022": "59.1%", "FY2021": "37.8%", "FY2020": "32.9%", "FY2019": "33.4%"}),
        ("Tier 1 Ratio", {"FY2023": "81.8%", "FY2022": "66.4%", "FY2021": "44.2%", "FY2020": "38.3%", "FY2019": "39.4%"}),
        ("Total Capital Ratio", {"FY2023": "90.8%", "FY2022": "73.8%", "FY2021": "50.7%", "FY2020": "43.7%", "FY2019": "45.3%"}),
        ("Leverage Ratio", {"FY2023": "16.7%", "FY2022": "9.9%", "FY2021": "5.2%", "FY2020": "6.8%", "FY2019": "7.2%"}),
        ("LCR", {"FY2023": "836.0%", "FY2022": "654.5%", "FY2021": "659%", "FY2020": "707%", "FY2019": "795.8%"}),
        ("NSFR", {"FY2023": "401.6%", "FY2022": "342.2%"}),
    ],
    balance_sheet_totals=[
        ("Total assets", {"FY2024": 684629, "FY2023": 3499217, "FY2022": 6487240, "FY2021": 7194284, "FY2020": 5625900, "FY2019": 4810642}),
        ("Loans and advances to customers", {"FY2024": 160, "FY2023": 40801, "FY2022": 70599, "FY2021": 265672, "FY2020": 353748, "FY2019": 578849}),
        ("Customer accounts", {"FY2024": 140207, "FY2023": 2790344, "FY2022": 5672994, "FY2021": 6372454, "FY2020": 4983443, "FY2019": 4345627}),
        ("Total equity", {"FY2024": 517960, "FY2023": 573219, "FY2022": 489004, "FY2021": 378126, "FY2020": 404330, "FY2019": 362624}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Interest receivable", {"FY2024": 65131, "FY2023": 160605, "FY2022": 98603, "FY2021": 42733, "FY2020": 37549, "FY2019": 17376}),
        ("Administrative expenses", {"FY2024": -77701, "FY2023": -95512, "FY2022": -98726, "FY2021": -61763, "FY2020": -50367, "FY2019": -12136}),
        ("Profit/(loss) for the financial year", {"FY2024": -57172, "FY2023": 19981, "FY2022": 21815, "FY2021": 10814, "FY2020": 25542, "FY2019": 7086}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2024": 573219, "FY2023": 489004, "FY2022": 378126, "FY2021": 404330, "FY2020": 362624, "FY2019": 0}),
        ("Total comprehensive income/(loss) for the year", {"FY2024": 1258, "FY2023": 87538, "FY2022": -85961, "FY2021": -22948, "FY2020": 44941, "FY2019": -162}),
        ("Other equity movements, net", {"FY2024": -56517, "FY2023": -3323, "FY2022": 196839, "FY2021": -3256, "FY2020": -3235, "FY2019": 362786}),
        ("Closing equity", {"FY2024": 517960, "FY2023": 573219, "FY2022": 489004, "FY2021": 378126, "FY2020": 404330, "FY2019": 362624}),
    ],
    equity_changes_unit="£'000",
    note="Statement sheets (Balance Sheet/P&L/Equity/Asset Quality) cover FY2019-FY2024 (full statutory accounts). Pillar 3 ratios/RWA sheets cover FY2019-FY2023: no official standalone CUKL Pillar 3 report was located for FY2024, and Companies House shows FY2025 accounts are not yet filed as at this build. FY2018 is deliberately excluded from every sheet: CUKL was a dormant shell throughout FY2018 (GBP 1 net assets, no PRA/FCA authorisation, no trading) per its own Companies House dormant-company filing - see ENTITY NOTE in the source cells. See source notes for the FRS 101 IAS 7 cash-flow exemption and full source coverage.",
)

bw.save("/Users/armaan/code/katalysis/banks/CITIBANK UK FINANCIALS.xlsx")
