import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# CUKL, company 11283101, FRN 124579.  The company applies the FRS 101
# IAS 7 exemption, so no statutory cash-flow statement is available (see
# EXEMPTION_NOTE). Statement-of-financial-position/income-statement/equity
# data is available for FY2021-FY2024 (full statutory accounts, 2 source
# documents each covering 2 years); Pillar 3 (capital/RWA/liquidity) data
# is only available for FY2021-FY2023 (no standalone CUKL Pillar 3 report
# was located for FY2024) - FY2024 is therefore populated for the 3
# statement sheets + Asset Quality but left blank on every Pillar 3 sheet.
# FY2025 is omitted entirely: statutory accounts not yet filed as at this
# build and no Pillar 3 document located.
YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

P3_2021_URL = "https://www.citigroup.com/rcs/citigpa/akpublic/storage/public/b3p3d211231_uk.pdf"
P3_2023_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/b3p3d231231_uk.pdf"
FS_2024_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/citibank-uk-limited-annual-fs-2024.pdf"
CH_2022_URL = "https://find-and-update.company-information.service.gov.uk/company/11283101/filing-history/MzM3OTI1NDA3NWFkaXF6a2N4/document?format=pdf&download=0"
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
    "disclosures are prepared on a stand-alone basis. This is not Citibank N.A. London Branch or Citibank Europe plc."
)

P3_SOURCES = (
    "Sources - official Citibank UK Limited standalone Pillar 3 disclosures, UK KM1 and related tables:\n"
    f"FY2023: CUKL Pillar 3 Disclosures December 2023, pp. 3-5 and 8 - {P3_2023_URL}\n"
    f"FY2022: FY2022 comparative column in the CUKL Pillar 3 Disclosures December 2023, p. 5 - {P3_2023_URL}\n"
    f"FY2021: CUKL Pillar 3 Disclosures December 2021, pp. 6 and 15 - {P3_2021_URL}\n"
    f"Regulatory filing index: {REG_URL}\n"
    + ENTITY_NOTE
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
    "CRE component) while the stage split beneath it covers CRE only - documented, not blended or backfilled."
)

RWA_SOURCES = (
    "Sources - official Citibank UK Limited standalone Pillar 3 disclosures, Table 'Overview of risk weighted "
    "exposure amounts (UK OV1)':\n"
    f"FY2023/FY2022: CUKL Pillar 3 Disclosures December 2023, Table 5 (UK OV1), p.10 - {P3_2023_URL}\n"
    f"FY2021: CUKL Pillar 3 Disclosures December 2021, Table 4 (OV1), p.13 - {P3_2021_URL}\n"
    f"Regulatory filing index: {REG_URL}\n"
    + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: the FY2021 table's category labels differ slightly from FY2022/FY2023's (CCR is broken "
    "into mark-to-market/SFT sub-components in FY2021 vs a single CCR line in FY2022/FY2023; FY2021 has no "
    "'amounts below the thresholds for deduction' line, FY2022/FY2023 do) - both years' own category totals are "
    "reproduced as each report presents them, summing exactly to that year's own disclosed Total RWA (which ties "
    "to the existing Total RWAs sheet). FY2024 is blank: no standalone CUKL Pillar 3 report for FY2024 was located."
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
        ("DATA", "Cash and balances at central banks", {"FY2024": 484139, "FY2023": 680797, "FY2022": 1526980, "FY2021": 1176483}),
        ("DATA", "Derivative financial instruments", {"FY2024": 2592, "FY2023": 43848, "FY2022": 201825, "FY2021": 324553}),
        ("DATA", "Treasury bills and other eligible bills", {"FY2024": 0, "FY2023": 1651630, "FY2022": 2623200, "FY2021": 2309712}),
        ("DATA", "Loans and advances to banks", {"FY2024": 191422, "FY2023": 173568, "FY2022": 170277, "FY2021": 1287129}),
        ("DATA", "Loans and advances to customers", {"FY2024": 160, "FY2023": 40801, "FY2022": 70599, "FY2021": 265672}),
        ("DATA", "Debt securities", {"FY2024": 0, "FY2023": 865731, "FY2022": 1823106, "FY2021": 1756683}),
        ("DATA", "Intangible fixed assets", {"FY2024": 24, "FY2023": 2936, "FY2022": 4467, "FY2021": 6687}),
        ("DATA", "Other assets", {"FY2024": 4174, "FY2023": 37418, "FY2022": 65125, "FY2021": 65217}),
        ("DATA", "Prepayment and accrued income", {"FY2024": 2118, "FY2023": 2488, "FY2022": 1661, "FY2021": 2148}),
        ("TOTAL", "Total assets", {"FY2024": 684629, "FY2023": 3499217, "FY2022": 6487240, "FY2021": 7194284}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits by banks", {"FY2024": 84, "FY2023": 9400, "FY2022": 32184, "FY2021": 8316}),
        ("DATA", "Customer accounts", {"FY2024": 140207, "FY2023": 2790344, "FY2022": 5672994, "FY2021": 6372454}),
        ("DATA", "Derivative financial instruments", {"FY2024": 3015, "FY2023": 43411, "FY2022": 203089, "FY2021": 320789}),
        ("DATA", "Other liabilities", {"FY2024": 8843, "FY2023": 15330, "FY2022": 19456, "FY2021": 56809}),
        ("DATA", "Accruals and deferred income", {"FY2024": 3687, "FY2023": 4877, "FY2022": 7840, "FY2021": 4868}),
        ("DATA", "Provisions for liabilities", {"FY2024": 10833, "FY2023": 10254, "FY2022": 10436, "FY2021": 850}),
        ("DATA", "Subordinated liabilities", {"FY2024": 0, "FY2023": 52382, "FY2022": 52237, "FY2021": 52072}),
        ("SECTION", "Equity", {}),
        ("DATA", "Called up share capital", {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("DATA", "Reserves", {"FY2024": 510934, "FY2023": 505184, "FY2022": 434300, "FY2021": 341987}),
        ("DATA", "Profit and loss account", {"FY2024": 7026, "FY2023": 68035, "FY2022": 54704, "FY2021": 36139}),
        ("TOTAL", "Total liabilities (incl. equity - see sources)", {"FY2024": 684629, "FY2023": 3499217, "FY2022": 6487240, "FY2021": 7194284}),
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
        ("DATA", "Interest receivable", {"FY2024": 65131, "FY2023": 160605, "FY2022": 98603, "FY2021": 42733}),
        ("DATA", "Interest payable", {"FY2024": -20935, "FY2023": -43107, "FY2022": -11677, "FY2021": -1816}),
        ("DATA", "Fees and commissions receivable", {"FY2024": 24476, "FY2023": 38466, "FY2022": 48022, "FY2021": 34505}),
        ("DATA", "Fees and commissions payable", {"FY2024": -3389, "FY2023": -4333, "FY2022": -4516, "FY2021": -5050}),
        ("DATA", "Dealing profits/(loss)", {"FY2024": -70424, "FY2023": -35246, "FY2022": -606, "FY2021": 3743}),
        ("DATA", "Other operating income", {"FY2024": 1093, "FY2023": 1559, "FY2022": 825, "FY2021": 530}),
        ("DATA", "Administrative expenses", {"FY2024": -77701, "FY2023": -95512, "FY2022": -98726, "FY2021": -61763}),
        ("DATA", "Depreciation and amortization", {"FY2024": -2913, "FY2023": -1530, "FY2022": -2187, "FY2021": -2346}),
        ("DATA", "Other operating charges", {"FY2024": -7, "FY2023": -15, "FY2022": -292, "FY2021": -103}),
        ("DATA", "Impairment on financial assets / Provisions", {"FY2024": 53, "FY2023": 110, "FY2022": 416, "FY2021": 1309}),
        ("TOTAL", "Profit/(loss) on ordinary activities before tax", {"FY2024": -84616, "FY2023": 20997, "FY2022": 29862, "FY2021": 11742}),
        ("DATA", "Tax on profit on ordinary activities", {"FY2024": 27444, "FY2023": -1016, "FY2022": -8047, "FY2021": -928}),
        ("TOTAL", "Profit/(loss) for the financial year", {"FY2024": -57172, "FY2023": 19981, "FY2022": 21815, "FY2021": 10814}),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", {"FY2024": 12450, "FY2023": 66975, "FY2022": -147555, "FY2021": -44921}),
        ("DATA", "Debt instruments at FVOCI - reclassified to profit or loss", {"FY2024": 70082, "FY2023": 26902, "FY2022": 0, "FY2021": -3980}),
        ("DATA", "Related tax", {"FY2024": -24102, "FY2023": -26320, "FY2022": 39779, "FY2021": 15139}),
        ("TOTAL", "Other comprehensive income/(loss) for the year, net of tax", {"FY2024": 58430, "FY2023": 67557, "FY2022": -107776, "FY2021": -33762}),
        ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2024": 1258, "FY2023": 87538, "FY2022": -85961, "FY2021": -22948}),
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
        ("TOTAL", "At 1 January 2021", (0, 363589, 12151, 15, 28575, 404330)),
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
    subtitle="Company (entity-level) basis, £'000. See sources - stage-split basis differs FY2024/23 vs FY2022/21.",
    rows=[
        ("SECTION", "Loan book", {}),
        ("DATA", "Loans and advances to customers, net", {"FY2024": 160, "FY2023": 40801, "FY2022": 70599, "FY2021": 265672}),
        ("SECTION", "Stage split (FY2024/23: full customer loan book; FY2022/21: CRE component only - see sources)", {}),
        ("DATA", "Stage 1 gross exposure", {"FY2024": 162, "FY2023": 40742, "FY2021": 161246}),
        ("DATA", "Stage 2 gross exposure", {"FY2023": 53}),
        ("DATA", "Stage 3 gross exposure", {"FY2023": 17}),
        ("DATA", "Stage 1 ECL allowance", {"FY2024": -2, "FY2023": -11}),
        ("DATA", "Stage 2 ECL allowance", {}),
        ("DATA", "Stage 3 ECL allowance", {}),
        ("TOTAL", "Total ECL allowance, closing balance", {"FY2024": -2, "FY2023": -11, "FY2022": 0, "FY2021": 0}),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=56, source_height=145)


metric("CET1 Capital", "£m", [
    ("Common Equity Tier 1 (CET1) capital", {"FY2023": 418.0, "FY2022": 417.0, "FY2021": 304.2}),
])
metric("CET1 Ratio", "% of RWA", [
    ("Common Equity Tier 1 (CET1) ratio", {"FY2023": "72.7%", "FY2022": "59.1%", "FY2021": "37.8%"}),
])
metric("Tier 1 Capital", "£m", [
    ("Tier 1 capital", {"FY2023": 470.0, "FY2022": 469.0, "FY2021": 356.2}),
])
metric("Tier 1 Ratio", "% of RWA", [
    ("Tier 1 ratio", {"FY2023": "81.8%", "FY2022": "66.4%", "FY2021": "44.2%"}),
])
metric("Total Capital", "£m", [
    ("Total capital", {"FY2023": 522.0, "FY2022": 521.0, "FY2021": 408.2}),
])
metric("Total Capital Ratio", "% of RWA", [
    ("Total capital ratio", {"FY2023": "90.8%", "FY2022": "73.8%", "FY2021": "50.7%"}),
])
metric("Total RWAs", "£m", [
    ("Total risk-weighted exposure amount", {"FY2023": 574.7, "FY2022": 706.1, "FY2021": 805.3}),
])
bw.add_rwa_breakdown_sheet(
    title="Citibank UK Limited — RWA Breakdown",
    subtitle="UK OV1 template, £m.",
    rows=[
        ("DATA", "Credit risk (excluding CCR)", {"FY2023": 264.1, "FY2022": 193.6, "FY2021": 419.2}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2023": 0.9, "FY2022": 3.4, "FY2021": 15.2}),
        ("DATA", "Securitisation exposures in the non-trading/banking book", {"FY2023": 124.0, "FY2022": 261.5, "FY2021": 245.9}),
        ("DATA", "Market risk (position, FX and commodities)", {"FY2023": 43.2, "FY2022": 106.3, "FY2021": 14.1}),
        ("DATA", "Operational risk", {"FY2023": 142.4, "FY2022": 141.3, "FY2021": 110.9}),
        ("DATA", "Amounts below the thresholds for deduction (250% risk weight)", {"FY2023": 107.2, "FY2022": 27.9}),
        ("TOTAL", "Total RWAs", {"FY2023": 574.7, "FY2022": 706.1, "FY2021": 805.3}),
    ],
    sources_text=RWA_SOURCES,
    first_col_width=68,
    unit_suffix=" (£m)",
)
metric("Leverage Ratio", "£m / %", [
    ("Total exposure measure", {"FY2023": 2812.0, "FY2022": 4733.0, "FY2021": 6818.1}),
    ("Leverage ratio", {"FY2023": "16.7%", "FY2022": "9.9%", "FY2021": "5.2%"}),
], note="FY2021 is reported on the pre-2022 Basel III basis; FY2022-FY2023 use the UK KM1 leverage measure excluding claims on central banks.")
metric("LCR", "£m / %", [
    ("Total HQLA (weighted value / average)", {"FY2023": 2988.6, "FY2022": 4476.6, "FY2021": 4219.7}),
    ("Total net cash outflows (adjusted value)", {"FY2023": 357.5, "FY2022": 687.1, "FY2021": 639.8}),
    ("Liquidity coverage ratio", {"FY2023": "836.0%", "FY2022": "654.5%", "FY2021": "659%"}),
], note="FY2021 is based on daily averages; FY2022-FY2023 use the revised UK KM1 weighted-average presentation.")
metric("NSFR", "£m / %", [
    ("Total available stable funding", {"FY2023": 4091.4, "FY2022": 6249.1}),
    ("Total required stable funding", {"FY2023": 1018.8, "FY2022": 1839.5}),
    ("NSFR ratio", {"FY2023": "401.6%", "FY2022": "342.2%"}),
], note="NSFR was implemented in the UK reporting framework from 2022; no FY2021 NSFR figure is populated.")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    P3_SOURCES,
    per_note={"MREL Ratio": "The 2021 report states that no MREL eligible debt had been issued. The 2023 report states that the BoE set CUKL's MREL requirement equal to its minimum capital requirement and that no MREL eligible debt had been issued as at 31 December 2023; no numeric MREL ratio is disclosed."},
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2023": "72.7%", "FY2022": "59.1%", "FY2021": "37.8%"}),
        ("Tier 1 Ratio", {"FY2023": "81.8%", "FY2022": "66.4%", "FY2021": "44.2%"}),
        ("Total Capital Ratio", {"FY2023": "90.8%", "FY2022": "73.8%", "FY2021": "50.7%"}),
        ("Leverage Ratio", {"FY2023": "16.7%", "FY2022": "9.9%", "FY2021": "5.2%"}),
        ("LCR", {"FY2023": "836.0%", "FY2022": "654.5%", "FY2021": "659%"}),
        ("NSFR", {"FY2023": "401.6%", "FY2022": "342.2%"}),
    ],
    balance_sheet_totals=[
        ("Total assets", {"FY2024": 684629, "FY2023": 3499217, "FY2022": 6487240, "FY2021": 7194284}),
        ("Loans and advances to customers", {"FY2024": 160, "FY2023": 40801, "FY2022": 70599, "FY2021": 265672}),
        ("Customer accounts", {"FY2024": 140207, "FY2023": 2790344, "FY2022": 5672994, "FY2021": 6372454}),
        ("Total equity", {"FY2024": 517960, "FY2023": 573219, "FY2022": 489004, "FY2021": 378126}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Interest receivable", {"FY2024": 65131, "FY2023": 160605, "FY2022": 98603, "FY2021": 42733}),
        ("Administrative expenses", {"FY2024": -77701, "FY2023": -95512, "FY2022": -98726, "FY2021": -61763}),
        ("Profit/(loss) for the financial year", {"FY2024": -57172, "FY2023": 19981, "FY2022": 21815, "FY2021": 10814}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2024": 573219, "FY2023": 489004, "FY2022": 378126, "FY2021": 404330}),
        ("Total comprehensive income/(loss) for the year", {"FY2024": 1258, "FY2023": 87538, "FY2022": -85961, "FY2021": -22948}),
        ("Other equity movements, net", {"FY2024": -56517, "FY2023": -3323, "FY2022": 196839, "FY2021": -3256}),
        ("Closing equity", {"FY2024": 517960, "FY2023": 573219, "FY2022": 489004, "FY2021": 378126}),
    ],
    equity_changes_unit="£'000",
    note="Statement sheets (Balance Sheet/P&L/Equity/Asset Quality) cover FY2021-FY2024 (full statutory accounts). Pillar 3 ratios/RWA sheets remain FY2021-FY2023 only: no official standalone CUKL Pillar 3 report was located for FY2024, and Companies House shows FY2025 accounts are not yet filed as at this build. See source notes for the FRS 101 IAS 7 cash-flow exemption and full source coverage.",
)

bw.save("/Users/armaan/code/katalysis/banks/CITIBANK UK FINANCIALS.xlsx")
