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
    "Bank had not begun lending), and only the Total Capital Ratio (359%) is disclosed among "
    "the Pillar 3 metrics for that year - both are self-skips at the metric/sheet-cell level "
    "for that one year, not the whole bank."
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
    "The reports do not provide a complete UK KM1 table for every year. Only explicitly disclosed "
    "entity-level values are populated; unavailable capital components and ratios remain blank. "
    "FY2020 only discloses a Total Capital Ratio (359%, per the Strategic Report) - the Bank had "
    "not yet begun regulatory reporting of the other KM1 components at that stage of mobilisation."
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

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=56, source_height=180)

def vals(data):
    return {y: data.get(y) for y in YEARS}

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", vals({"FY2024": 56324, "FY2023": 28035.733, "FY2022": 21299.969, "FY2021": 32643.538}))])
metric("CET1 Ratio", "%", [("Common Equity Tier 1 (CET1) ratio", vals({"FY2024": "20%", "FY2023": "22%"}))], "The annual reports disclose CET1 capital and, from 2023 onward, the CET1 ratio; earlier ratios were not separately disclosed.")
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", vals({}))], "No standalone Tier 1 capital amount was separately disclosed in the reports reviewed.")
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", vals({}))], "No standalone Tier 1 ratio was separately disclosed in the reports reviewed.")
metric("Total Capital", "£'000", [("Total capital", vals({}))], "No standalone total capital amount was separately disclosed in the reports reviewed.")
metric("Total Capital Ratio", "%", [("Total capital ratio", vals({"FY2022": "44%", "FY2021": "529%", "FY2020": "359%"}))], "The 2023 report states 44% for FY2022 and the 2024 report does not repeat a total capital ratio for FY2023/FY2024; FY2021 is reported as 529%; FY2020's Strategic Report states 359%.")
metric("Total RWAs", "£'000", [("Total risk-weighted assets", vals({"FY2024": 281756, "FY2023": 126528}))], "Total RWAs were disclosed in the 2024 report’s regulatory metrics table; earlier totals were not separately disclosed.")

bw.add_rwa_breakdown_sheet(
    title="Monument Bank Limited - RWA Breakdown",
    subtitle="Company basis, £'000. Not publicly disclosed - see source note.",
    rows=[("DATA", "Not publicly disclosed", {})],
    sources_text=P3_SOURCES + "\n\n" + (
        "RWA BREAKDOWN NOTE: no breakdown of Total RWAs by risk category (credit/market/"
        "operational risk) was found in any of the 4 filings' risk management or capital "
        "sections reviewed - only the aggregate Total Tier 1 capital and (via the Total "
        "Capital Ratio) an implied Total RWAs figure are disclosed. Confirmed as a genuine "
        "non-disclosure, not an access gap - all 4 filings were fully read through their "
        "risk management notes (see Note 26 'Risk management'/'Capital risk management' in "
        "the FY2024 report)."
    ),
    first_col_width=54,
    source_height=190,
)

metric("Leverage Ratio", "%", [("Leverage ratio", vals({"FY2024": "3.9%", "FY2023": "4.1%"}))])
metric("LCR", "%", [("Liquidity coverage ratio", vals({"FY2024": "589%", "FY2023": "1,093%", "FY2022": "10,128%", "FY2021": "2,861,111,111%"}))], "FY2021’s unusually high percentage is reproduced exactly as printed in the 2021 accounts; it is not normalised or inferred.")
metric("NSFR", "%", [("Net stable funding ratio", vals({"FY2024": "560%", "FY2023": "228%"}))], "NSFR was disclosed in the FY2024 report’s regulatory metrics table; no earlier standalone figure was located.")
metric("MREL Ratio", None, [("MREL ratio", vals({}))], "No quantitative MREL ratio was located in the official annual reports reviewed.")

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
        ("CET1 Ratio", vals({"FY2024": "20%", "FY2023": "22%"})),
        ("Total Capital Ratio", vals({"FY2022": "44%", "FY2021": "529%", "FY2020": "359%"})),
        ("Leverage Ratio", vals({"FY2024": "3.9%", "FY2023": "4.1%"})),
        ("LCR", vals({"FY2024": "589%", "FY2023": "1,093%", "FY2022": "10,128%", "FY2021": "2,861,111,111%"})),
        ("NSFR", vals({"FY2024": "560%", "FY2023": "228%"})),
    ],
    note="Monument Bank Limited standalone/Company basis. FY2025 is blank because the latest available Companies House accounts cover 31 December 2024. FY2020 is the Bank's real historical floor (first full annual report, post-Banking Licence, pre-revenue) - FY2017-FY2019 are self-skipped in full because the entity was a pre-authorisation shell company with no bank-relevant disclosure (see Balance Sheet sheet's source note). Pillar 3 sheets contain only explicitly disclosed annual regulatory values; blank cells mean not disclosed.",
)

bw.save("/Users/armaan/code/katalysis/banks/MONUMENT BANK FINANCIALS.xlsx")
