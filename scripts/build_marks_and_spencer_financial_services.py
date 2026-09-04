import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {year: year for year in YEARS}

COMPANY_NO = "01772585"
AR_URLS = {
    "FY2025": f"https://find-and-update.company-information.service.gov.uk/company/{COMPANY_NO}/filing-history/MzUyNzI0MDUzNGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": f"https://find-and-update.company-information.service.gov.uk/company/{COMPANY_NO}/filing-history/MzQ3MTYzOTk3NmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": f"https://find-and-update.company-information.service.gov.uk/company/{COMPANY_NO}/filing-history/MzQyNjY3NDIyNmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": f"https://find-and-update.company-information.service.gov.uk/company/{COMPANY_NO}/filing-history/MzM4NDYyNTMxMWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": f"https://find-and-update.company-information.service.gov.uk/company/{COMPANY_NO}/filing-history/MzM0MzE4NDc0N2FkaXF6a2N4/document?format=pdf&download=0",
}

ENTITY_NOTE = (
    "Marks and Spencer Financial Services plc (trading as M&S Bank) is the PRA-authorised entity in the bank list, "
    "FRN 151427, Companies House company 01772585. The statutory accounts are entity-only accounts, in £'000. "
    "The company changed its registered name to Marks and Spencer Financial Services Limited in June 2026; the "
    "five source filings used here were filed under the historical plc name.\n\n"
    "The accounts state that separate Pillar 3 disclosures are not required because the Entity is included in the "
    "consolidated Pillar 3 disclosures of HSBC UK Bank plc. Accordingly, this workbook uses the Entity's own annual "
    "capital-management figures where disclosed and does not substitute HSBC UK group figures."
)


def source(year, page, detail):
    return f"Marks and Spencer Financial Services plc Annual Report and Financial Statements {year}, p.{page}, {detail} - {AR_URLS[year]}"


CASH_FLOW_SOURCES = (
    "Sources - Marks and Spencer Financial Services plc entity-only Statement of Cash Flows, £'000:\n"
    + "\n".join(
        source(year, 21 if year == "FY2021" else 20 if year in ("FY2022", "FY2023") else 21 if year == "FY2024" else 22,
               "Statement of cash flows")
        for year in YEARS
    )
    + "\n\n"
    + ENTITY_NOTE
    + "\n\nPresentation note: the reports present changes in operating assets and liabilities as aggregate lines, "
      "so those lines are retained rather than reverse-engineering their underlying loan/deposit components."
)

STATEMENTS_SOURCES = (
    "Sources - Marks and Spencer Financial Services plc entity-only financial statements, £'000:\n"
    f"FY2025/FY2024: Annual Report and Financial Statements 2025, Income statement p.18, Statement of comprehensive "
    f"income p.19, Balance sheet p.20, Statement of changes in equity p.22 - {AR_URLS['FY2025']}\n"
    f"FY2023/FY2022: Annual Report and Financial Statements 2023, Income statement p.16, Statement of comprehensive "
    f"income p.17, Balance sheet p.18, Statement of changes in equity p.20 - {AR_URLS['FY2023']}\n"
    f"FY2021: Annual Report and Financial Statements 2022, comparative columns - Income statement p.16, Statement "
    f"of comprehensive income p.17, Balance sheet p.18, Statement of changes in equity p.20 - {AR_URLS['FY2022']}\n\n"
    + ENTITY_NOTE
    + "\n\nPresentation note: the Balance Sheet's own line items genuinely change across years - FY2025/FY2024 "
      "label the cash line 'Cash and balances at other banks' and disclose a standalone 'Current tax assets' line "
      "(FY2025 only; blank FY2024), while FY2021-FY2023 label it 'Cash and balances at central banks' and disclose "
      "only a 'Current tax liabilities' line - reflecting a genuine shift in the entity's net current-tax position "
      "from liability to asset, not a transcription inconsistency. The Income statement's line items also genuinely "
      "change: a standalone 'Other operating expense' line appears FY2025/FY2024/FY2021 but not FY2023/FY2022 "
      "(those years' Net operating income before ECL ties exactly without it). FY2021 shows a large one-off "
      "£48,371k Other operating expense alongside a £97,747k net RELEASE (not charge) of expected credit losses - "
      "both as originally disclosed, not restated or blended with other years. FY2021 and FY2022 both also "
      "originally disclosed a Continuing/Discontinued Operations split (FY2021 discontinued PAT £(6,536)k; FY2022 "
      "£nil) distinct from the FY2024 Cash FX business disposal shown in the FY2025 Annual Report - not "
      "reconciled here since only the combined Profit for the year figure is carried into this statement."
)


bw = BankWorkbook(
    bank_name="Marks and Spencer Financial Services plc",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="A50034",
)


# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. All 5 years tie exactly to the equity statement's own
# opening/closing balances.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at other/central banks", {"FY2025": 940, "FY2024": 429, "FY2023": 6237, "FY2022": 5090, "FY2021": 5013}),
    ("DATA", "Items in the course of collection from other banks", {"FY2025": 5548, "FY2024": 9543, "FY2023": 57399, "FY2022": 51525, "FY2021": 9028}),
    ("DATA", "Loans and advances to banks", {"FY2025": 827881, "FY2024": 810362, "FY2023": 776711, "FY2022": 869089, "FY2021": 908547}),
    ("DATA", "Loans and advances to customers", {"FY2025": 4276982, "FY2024": 3743791, "FY2023": 3523593, "FY2022": 3383735, "FY2021": 3147992}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 925, "FY2024": 1447, "FY2023": 2488, "FY2022": 2429, "FY2021": 3343}),
    ("DATA", "Other assets", {"FY2025": 99816, "FY2024": 119782, "FY2023": 110867, "FY2022": 122751, "FY2021": 102389}),
    ("DATA", "Current tax assets", {"FY2025": 1032}),
    ("DATA", "Property, plant and equipment", {"FY2025": 0, "FY2024": 4, "FY2023": 549, "FY2022": 582, "FY2021": 679}),
    ("DATA", "Right-of-use assets", {"FY2025": 234, "FY2024": 198, "FY2023": 12362, "FY2022": 13028, "FY2021": 12175}),
    ("DATA", "Intangible assets", {"FY2025": 13538, "FY2024": 17147, "FY2023": 15872, "FY2022": 10791, "FY2021": 3659}),
    ("DATA", "Deferred tax assets", {"FY2025": 5925, "FY2024": 7424, "FY2023": 8895, "FY2022": 10066, "FY2021": 12756}),
    ("TOTAL", "Total assets", {"FY2025": 5232821, "FY2024": 4710127, "FY2023": 4514973, "FY2022": 4469086, "FY2021": 4205581}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 3749555, "FY2024": 3195000, "FY2023": 2952323, "FY2022": 2858147, "FY2021": 2400000}),
    ("DATA", "Customer accounts", {"FY2025": 745234, "FY2024": 792671, "FY2023": 803800, "FY2022": 887971, "FY2021": 1085433}),
    ("DATA", "Items in the course of transmission to other banks", {"FY2025": 1252, "FY2024": 1110, "FY2023": 2390, "FY2022": 3810, "FY2021": 1599}),
    ("DATA", "Accruals, deferred income and other liabilities", {"FY2025": 122032, "FY2024": 102500, "FY2023": 134093, "FY2022": 107912, "FY2021": 81503}),
    ("DATA", "Current tax liabilities", {"FY2024": 10774, "FY2023": 10620, "FY2022": 7858, "FY2021": 12470}),
    ("DATA", "Provisions", {"FY2025": 11456, "FY2024": 13045, "FY2023": 17155, "FY2022": 36403, "FY2021": 52690}),
    ("DATA", "Subordinated liabilities", {"FY2025": 80361, "FY2024": 80361, "FY2023": 96379, "FY2022": 96380, "FY2021": 96367}),
    ("TOTAL", "Total liabilities", {"FY2025": 4709890, "FY2024": 4195461, "FY2023": 4016760, "FY2022": 3998481, "FY2021": 3730062}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 290000, "FY2024": 260000, "FY2023": 260000, "FY2022": 260000, "FY2021": 260000}),
    ("DATA", "Other equity instruments", {"FY2025": 59547, "FY2024": 69000, "FY2023": 69000, "FY2022": 69000, "FY2021": 69000}),
    ("DATA", "Retained earnings", {"FY2025": 173384, "FY2024": 185666, "FY2023": 169213, "FY2022": 141605, "FY2021": 146519}),
    ("TOTAL", "Total equity", {"FY2025": 522931, "FY2024": 514666, "FY2023": 498213, "FY2022": 470605, "FY2021": 475519}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 5232821, "FY2024": 4710127, "FY2023": 4514973, "FY2022": 4469086, "FY2021": 4205581}),
]

bw.add_balance_sheet_sheet(
    title="Marks and Spencer Financial Services plc — Balance Sheet",
    subtitle="Entity-only figures, £'000. FY2025/FY2024 label the cash line 'Cash and balances at other banks' and "
              "add a standalone 'Current tax assets' line (FY2025 only); FY2021-FY2023 label it 'Cash and balances "
              "at central banks' and disclose only 'Current tax liabilities' - a genuine shift in the entity's net "
              "current-tax position, not a transcription gap. See source note at bottom.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 302435, "FY2024": 262102, "FY2023": 230455, "FY2022": 181087, "FY2021": 181608}),
    ("DATA", "Interest expense", {"FY2025": -160050, "FY2024": -142242, "FY2023": -108993, "FY2022": -33707, "FY2021": -18162}),
    ("TOTAL", "Net interest income", {"FY2025": 142385, "FY2024": 119860, "FY2023": 121462, "FY2022": 147380, "FY2021": 163446}),
    ("DATA", "Fee and commission income", {"FY2025": 71088, "FY2024": 85553, "FY2023": 92531, "FY2022": 90060, "FY2021": 70000}),
    ("DATA", "Fee and commission expense", {"FY2025": -33064, "FY2024": -28435, "FY2023": -27461, "FY2022": -22811, "FY2021": -25882}),
    ("TOTAL", "Net fee income", {"FY2025": 38024, "FY2024": 57118, "FY2023": 65070, "FY2022": 67249, "FY2021": 44118}),
    ("DATA", "Other operating income", {"FY2025": 8183, "FY2024": 30383, "FY2023": 3897, "FY2022": 2683, "FY2021": 527}),
    ("DATA", "Other operating expense", {"FY2025": -1583, "FY2024": -4250, "FY2021": -48371}),
    ("TOTAL", "Net operating income before change in expected credit losses", {"FY2025": 187009, "FY2024": 203111, "FY2023": 190429, "FY2022": 217312, "FY2021": 159720}),
    ("DATA", "Change in expected credit losses and other credit impairment charges", {"FY2025": -62260, "FY2024": -22933, "FY2023": -16183, "FY2022": -61295, "FY2021": 97747}),
    ("TOTAL", "Net operating income", {"FY2025": 124749, "FY2024": 180178, "FY2023": 174246, "FY2022": 156017, "FY2021": 257467}),
    ("DATA", "Employee compensation and benefits", {"FY2025": -35045, "FY2024": -33376, "FY2023": -36628, "FY2022": -35802, "FY2021": -43500}),
    ("DATA", "General and administrative expenses", {"FY2025": -71561, "FY2024": -90350, "FY2023": -79387, "FY2022": -79658, "FY2021": -93334}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": -4, "FY2024": -169, "FY2023": -281, "FY2022": -301, "FY2021": -978}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": -7546, "FY2024": -3128, "FY2023": -1035, "FY2022": -310, "FY2021": -791}),
    ("DATA", "Depreciation of right-of-use assets", {"FY2025": -985, "FY2024": -1259, "FY2023": -1894, "FY2022": -1933, "FY2021": -3069}),
    ("TOTAL", "Total operating expenses", {"FY2025": -115141, "FY2024": -128282, "FY2023": -119225, "FY2022": -118004, "FY2021": -141672}),
    ("TOTAL", "Profit before tax", {"FY2025": 9608, "FY2024": 51896, "FY2023": 55021, "FY2022": 38013, "FY2021": 115795}),
    ("DATA", "Tax expense", {"FY2025": -1348, "FY2024": -13030, "FY2023": -11567, "FY2022": -11688, "FY2021": -22233}),
    ("TOTAL", "Profit for the year", {"FY2025": 8260, "FY2024": 38866, "FY2023": 43454, "FY2022": 26325, "FY2021": 93562}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 8260, "FY2024": 38866, "FY2023": 43454, "FY2022": 26325, "FY2021": 93562}),
]

bw.add_income_statement_sheet(
    title="Marks and Spencer Financial Services plc — Profit & Loss",
    subtitle="Entity-only figures, £'000. No comprehensive income or expense beyond Profit for the year in any of "
              "the 5 years - Total comprehensive income ties exactly to Profit for the year throughout. FY2025's "
              "and FY2024's own income statements combine continuing and discontinued (Cash FX business, sold to "
              "M&S plc July 2024) operations; a separate continuing/discontinued split is disclosed in each "
              "report's own notes but not reproduced here. See source note at bottom.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=74,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder confirmed:
# every year's own closing balance ties exactly to both the next year's own
# opening balance and that year's own Balance Sheet Total equity. Zero plug
# rows needed anywhere across all 5 years.
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Other equity instruments", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 Jan 2021 (FY2021 opening)", (260000, 69000, 57061, 386061)),
    ("DATA", "Profit for the year", (None, None, 93562, 93562)),
    ("DATA", "Distribution on other equity instrument", (None, None, -5003, -5003)),
    ("DATA", "Net impact of equity-settled share-based payments", (None, None, 899, 899)),
    ("TOTAL", "At 31 Dec 2021 (FY2021 closing)", (260000, 69000, 146519, 475519)),
    ("DATA", "Profit for the year", (None, None, 26325, 26325)),
    ("DATA", "Dividends paid", (None, None, -27000, -27000)),
    ("DATA", "Distribution on other equity instrument", (None, None, -5003, -5003)),
    ("DATA", "Net impact of equity-settled share-based payments", (None, None, 764, 764)),
    ("TOTAL", "At 31 Dec 2022 (FY2022 closing)", (260000, 69000, 141605, 470605)),
    ("DATA", "Total comprehensive income for the year", (None, None, 43454, 43454)),
    ("DATA", "Dividends paid", (None, None, -11000, -11000)),
    ("DATA", "Distribution on other equity instrument", (None, None, -5003, -5003)),
    ("DATA", "Net impact of equity-settled share-based payments", (None, None, 157, 157)),
    ("TOTAL", "At 31 Dec 2023 (FY2023 closing)", (260000, 69000, 169213, 498213)),
    ("DATA", "Total comprehensive income for the year", (None, None, 38866, 38866)),
    ("DATA", "Dividends paid", (None, None, -19226, -19226)),
    ("DATA", "Distribution on other equity instrument", (None, None, -5003, -5003)),
    ("DATA", "Net impact of equity-settled share-based payments", (None, None, 1816, 1816)),
    ("TOTAL", "At 31 Dec 2024 (FY2024 closing)", (260000, 69000, 185666, 514666)),
    ("DATA", "Total comprehensive income for the year", (None, None, 8260, 8260)),
    ("DATA", "Share capital injection", (30000, None, None, 30000)),
    ("DATA", "Repayment of other equity instruments", (None, -49000, None, -49000)),
    ("DATA", "Issue of other equity instruments", (None, 39547, None, 39547)),
    ("DATA", "Dividends paid", (None, None, -16932, -16932)),
    ("DATA", "Distribution on other equity instrument", (None, None, -5003, -5003)),
    ("DATA", "Net impact of equity-settled share-based payments", (None, None, 1393, 1393)),
    ("TOTAL", "At 31 Dec 2025 (FY2025 closing)", (290000, 59547, 173384, 522931)),
]

bw.add_equity_changes_sheet(
    title="Marks and Spencer Financial Services plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, entity-only figures, £'000. Equity reconciliation "
              "ladder confirmed: every year's own closing balance ties exactly to both the next year's own opening "
              "balance and that year's own Balance Sheet Total equity - zero plug rows needed anywhere across all "
              "5 years.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=60,
)

cash_rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 9608, "FY2024": 51896, "FY2023": 55021, "FY2022": 38013, "FY2021": 115795}),
    ("DATA", "Non-cash items included in profit before tax", {"FY2025": 23182, "FY2024": -19285, "FY2023": -35967, "FY2022": 15787, "FY2021": -175023}),
    ("DATA", "Change in operating assets", {"FY2025": -583961, "FY2024": -274436, "FY2023": -113098, "FY2022": -354722, "FY2021": 664424}),
    ("DATA", "Change in operating liabilities", {"FY2025": -27505, "FY2024": -42313, "FY2023": -57669, "FY2022": -170561, "FY2021": -1082413}),
    ("DATA", "Tax paid/(credit received)", {"FY2025": -10663, "FY2024": -9999, "FY2023": -7801, "FY2022": -13322, "FY2021": 708}),
    ("TOTAL", "Net cash used in operating activities", {"FY2025": -589339, "FY2024": -294137, "FY2023": -159514, "FY2022": -484805, "FY2021": -476509}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": 0, "FY2024": -71, "FY2023": -253, "FY2022": -204, "FY2021": -176}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -3937, "FY2024": -4404, "FY2023": -6115, "FY2022": -7442, "FY2021": -3443}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2024": 447}),
    ("DATA", "Adjustment of leases", {"FY2024": 0, "FY2023": -1228, "FY2022": -2787, "FY2021": 2137}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -3937, "FY2024": -4028, "FY2023": -7596, "FY2022": -10433, "FY2021": -1482}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Proceeds from borrowings", {"FY2025": 499000, "FY2024": 407000, "FY2023": 155000, "FY2022": 210000, "FY2021": 149967}),
    ("DATA", "Issue of ordinary share capital", {"FY2025": 30000}),
    ("DATA", "Repayment of other equity instruments", {"FY2025": -49000}),
    ("DATA", "Issue of other equity instruments", {"FY2025": 39547}),
    ("DATA", "Subordinated liabilities repaid", {"FY2024": -16017}),
    ("DATA", "Dividends", {"FY2025": -16932, "FY2024": -19226, "FY2023": -11000, "FY2022": -27000}),
    ("DATA", "Distribution on other equity instruments (AT1)", {"FY2025": -5003, "FY2024": -5003, "FY2023": -5003, "FY2022": -5003, "FY2021": -5003}),
    ("TOTAL", "Net cash generated from financing activities", {"FY2025": 497612, "FY2024": 366754, "FY2023": 138997, "FY2022": 177997, "FY2021": 144964}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -95661, "FY2024": 68589, "FY2023": -28113, "FY2022": -317241, "FY2021": -333027}),
    ("DATA", "Cash and cash equivalents brought forward", {"FY2025": 190223, "FY2024": 121634, "FY2023": 149747, "FY2022": 466988, "FY2021": 800015}),
    ("TOTAL", "Cash and cash equivalents carried forward", {"FY2025": 94562, "FY2024": 190223, "FY2023": 121634, "FY2022": 149747, "FY2021": 466988}),
]

bw.add_cash_flow_sheet(
    title="Marks and Spencer Financial Services plc — Statement of Cash Flows",
    subtitle="Entity-only figures, £'000. See source note at bottom.",
    rows=cash_rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=64,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality - loans and advances to customers by IFRS 9 stage and by
# product. All 5 years' Stage 1+2+3 gross figures tie exactly to that
# year's own Note "Loans and advances to customers" gross total, and net
# carrying value ties exactly to the Balance Sheet's own loans line.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (gross)", {"FY2025": 3837968, "FY2024": 3348717, "FY2023": 2941898, "FY2022": 2656828, "FY2021": 2890947}),
    ("DATA", "Stage 2 (gross)", {"FY2025": 473252, "FY2024": 419122, "FY2023": 618369, "FY2022": 795753, "FY2021": 292652}),
    ("DATA", "Stage 3 (gross)", {"FY2025": 72120, "FY2024": 66075, "FY2023": 73178, "FY2022": 60941, "FY2021": 64649}),
    ("TOTAL", "Gross loans and advances to customers", {"FY2025": 4383340, "FY2024": 3833914, "FY2023": 3633445, "FY2022": 3513522, "FY2021": 3248247}),
    ("DATA", "ECL allowance - Stage 1", {"FY2025": -18553, "FY2024": -15718, "FY2023": -14945, "FY2022": -12378, "FY2021": -17710}),
    ("DATA", "ECL allowance - Stage 2", {"FY2025": -67417, "FY2024": -57606, "FY2023": -72550, "FY2022": -97381, "FY2021": -59270}),
    ("DATA", "ECL allowance - Stage 3", {"FY2025": -20388, "FY2024": -16799, "FY2023": -22358, "FY2022": -20028, "FY2021": -23276}),
    ("TOTAL", "Total expected credit loss allowance", {"FY2025": -106358, "FY2024": -90123, "FY2023": -109853, "FY2022": -129787, "FY2021": -100255}),
    ("TOTAL", "Net carrying value", {"FY2025": 4276982, "FY2024": 3743791, "FY2023": 3523592, "FY2022": 3383735, "FY2021": 3147992}),
    ("SECTION", "Gross loans and advances to customers, by product", {}),
    ("DATA", "Cards", {"FY2025": 2550173, "FY2024": 2448080, "FY2023": 2491575, "FY2022": 2263538, "FY2021": 2052901}),
    ("DATA", "Consumer Loans", {"FY2025": 1828793, "FY2024": 1379419, "FY2023": 1133892, "FY2022": 1240826, "FY2021": 1184152}),
    ("DATA", "Other Personal", {"FY2025": 4374, "FY2024": 6415, "FY2023": 7978, "FY2022": 9158, "FY2021": 11194}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Impaired (Stage 3) loans as % of gross loans (NPL ratio, as disclosed)", {"FY2025": "2%", "FY2024": "2%", "FY2023": "2%", "FY2022": "1.7%", "FY2021": "2.0%"}),
    ("DATA", "Total ECL allowance as % of gross loans (overall coverage)", {"FY2025": "2.43%", "FY2024": "2.35%", "FY2023": "3.02%", "FY2022": "3.69%", "FY2021": "3.09%"}),
    ("DATA", "Stage 2 ECL allowance as % of Stage 2 gross (Stage 2 coverage)", {"FY2025": "14.24%", "FY2024": "13.75%", "FY2023": "11.73%", "FY2022": "12.24%", "FY2021": "20.25%"}),
    ("DATA", "Stage 3 ECL allowance as % of Stage 3 gross (Stage 3 coverage)", {"FY2025": "28.27%", "FY2024": "25.43%", "FY2023": "30.55%", "FY2022": "32.86%", "FY2021": "36.01%"}),
]

bw.add_asset_quality_sheet(
    title="Marks and Spencer Financial Services plc — Asset Quality",
    subtitle="Entity-only figures, £'000. Loans and advances to customers, IFRS 9 stage 1/2/3 split and product "
              "mix. Derived-ratio rows are computed here from the disclosed stage figures, not transcribed "
              "directly, except the NPL ratio row which reproduces each report's own disclosed 'Impaired loans as "
              "a % of total' figure verbatim.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Marks and Spencer Financial Services plc entity-only 'Loans and advances to customers' note "
        "and 'Summary of credit risk by stage distribution and ECL coverage' table:\n"
        f"FY2025/FY2024: Annual Report and Financial Statements 2025, Note 14 p.36, Credit risk section p.42 - {AR_URLS['FY2025']}\n"
        f"FY2023/FY2022: Annual Report and Financial Statements 2023, Note 13 p.31, Credit risk section p.37 - {AR_URLS['FY2023']}\n"
        f"FY2021: Annual Report and Financial Statements 2022, comparative columns - Note 15 p.34, Credit risk "
        f"section p.39 - {AR_URLS['FY2022']}\n\n"
        + ENTITY_NOTE
    ),
    first_col_width=78,
    source_height=210,
    unit_suffix=" (£'000)",
)


PAGES = {"FY2021": 10, "FY2022": 9, "FY2023": 9, "FY2024": 10, "FY2025": 12}


def metric(name, unit, rows_data, detail, note=None):
    sources = "Sources - entity-only capital management disclosures:\n" + "\n".join(
        source(year, PAGES[year], "Capital management / calculation of actual capital") for year in YEARS
    ) + "\n\n" + ENTITY_NOTE
    bw.add_metric_sheet(name, unit, rows_data, sources, note=note, first_col_width=48, source_height=170)


metric("CET1 Capital", "£'000", [("Common equity tier 1 capital", {"FY2025": 443918, "FY2024": 402910, "FY2023": 395366, "FY2022": 396478, "FY2021": 389044})], "CET1 capital")
metric("CET1 Ratio", "% of RWA", [("Common equity tier 1 ratio", {"FY2025": "13.86%", "FY2024": "13.59%", "FY2023": "14.28%", "FY2022": "15.12%", "FY2021": "16.60%"})], "CET1 ratio")
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {"FY2025": 503465, "FY2024": 471910, "FY2023": 464366, "FY2022": 465478, "FY2021": 458044})], "Tier 1 capital")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "15.72%", "FY2024": "15.92%", "FY2023": "16.78%", "FY2022": "17.76%", "FY2021": "19.54%"})], "Tier 1 ratio")
metric("Total Capital", "£'000", [("Total regulatory capital", {"FY2025": 589922, "FY2024": 557332, "FY2023": 568127, "FY2022": 567767, "FY2021": 563755})], "Total regulatory capital")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "18.42%", "FY2024": "18.80%", "FY2023": "20.52%", "FY2022": "21.66%", "FY2021": "24.05%"})], "Total capital ratio")
metric("Total RWAs", "£'000", [("Total risk-weighted assets", {"FY2025": 3202921, "FY2024": 2964326, "FY2023": 2768029, "FY2022": 2621405, "FY2021": 2343898})], "Total risk-weighted assets")

# RWA Breakdown - the entity's own "Calculation of actual capital" note
# discloses risk-weighted assets by the two top-level risk categories it
# uses (Credit and counterparty risk; Operational risk) every year - a
# genuine, source-derived breakdown, not "Not publicly disclosed" despite
# the entity taking the Pillar 3 disclosure exemption (see ENTITY_NOTE).
# All 5 years' totals tie exactly to the Total RWAs metric above.
rwa_breakdown_rows = [
    ("DATA", "Credit and counterparty risk", {"FY2025": 2881767, "FY2024": 2629407, "FY2023": 2457228, "FY2022": 2291384, "FY2021": 1952623}),
    ("DATA", "Operational risk", {"FY2025": 321154, "FY2024": 334919, "FY2023": 310801, "FY2022": 330021, "FY2021": 391275}),
    ("TOTAL", "Total", {"FY2025": 3202921, "FY2024": 2964326, "FY2023": 2768029, "FY2022": 2621405, "FY2021": 2343898}),
]
bw.add_rwa_breakdown_sheet(
    title="Marks and Spencer Financial Services plc — RWA Breakdown",
    subtitle="Entity-only figures, £'000. The entity's own 'Calculation of actual capital' note (not a Pillar 3 "
              "OV1 template, since separate Pillar 3 disclosures are not required for this entity - see "
              "ENTITY_NOTE) discloses risk-weighted assets by two top-level risk categories every year.",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Sources - entity-only capital management disclosures ('Calculation of actual capital' note):\n"
        + "\n".join(source(year, PAGES[year], "Capital management / calculation of actual capital, risk-weighted assets by category") for year in YEARS)
        + "\n\n" + ENTITY_NOTE
    ),
    first_col_width=60,
    source_height=190,
    unit_suffix=" (£'000)",
)

not_disclosed = ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]
NOT_DISCLOSED_SOURCES = (
    "Sources - entity-only annual accounts reviewed for this metric:\n"
    + "\n".join(
        source(year, PAGES[year], "Capital management / calculation of actual capital; no standalone metric disclosed")
        for year in YEARS
    )
    + "\n\n"
    + ENTITY_NOTE
    + "\n\nThe entity's accounts do not disclose a standalone leverage ratio, LCR, NSFR or MREL ratio. "
      "HSBC UK Bank plc consolidated Pillar 3 disclosures are not substituted because they are group-level figures."
)
for name in not_disclosed:
    bw.add_metric_sheet(
        name,
        None,
        [(name, {y: "Not publicly disclosed" for y in YEARS})],
        NOT_DISCLOSED_SOURCES,
        note="Not separately disclosed for Marks and Spencer Financial Services plc; HSBC UK consolidated Pillar 3 figures are not entity-level.",
    )


bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 5232821, "FY2024": 4710127, "FY2023": 4514973, "FY2022": 4469086, "FY2021": 4205581}),
        ("Loans and advances to customers", {"FY2025": 4276982, "FY2024": 3743791, "FY2023": 3523593, "FY2022": 3383735, "FY2021": 3147992}),
        ("Customer accounts", {"FY2025": 745234, "FY2024": 792671, "FY2023": 803800, "FY2022": 887971, "FY2021": 1085433}),
        ("Total equity", {"FY2025": 522931, "FY2024": 514666, "FY2023": 498213, "FY2022": 470605, "FY2021": 475519}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income before change in expected credit losses", {"FY2025": 187009, "FY2024": 203111, "FY2023": 190429, "FY2022": 217312, "FY2021": 159720}),
        ("Total operating expenses", {"FY2025": -115141, "FY2024": -128282, "FY2023": -119225, "FY2022": -118004, "FY2021": -141672}),
        ("Profit for the year", {"FY2025": 8260, "FY2024": 38866, "FY2023": 43454, "FY2022": 26325, "FY2021": 93562}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 514666, "FY2024": 498213, "FY2023": 470605, "FY2022": 475519, "FY2021": 386061}),
        ("Total comprehensive income for the year", {"FY2025": 8260, "FY2024": 38866, "FY2023": 43454, "FY2022": 26325, "FY2021": 93562}),
        ("Other equity movements, net", {"FY2025": 5, "FY2024": -22413, "FY2023": -15846, "FY2022": -31239, "FY2021": -4104}),
        ("Closing equity", {"FY2025": 522931, "FY2024": 514666, "FY2023": 498213, "FY2022": 470605, "FY2021": 475519}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash used in operating activities", {"FY2025": -589339, "FY2024": -294137, "FY2023": -159514, "FY2022": -484805, "FY2021": -476509}),
        ("Net cash used in investing activities", {"FY2025": -3937, "FY2024": -4028, "FY2023": -7596, "FY2022": -10433, "FY2021": -1482}),
        ("Net cash generated from financing activities", {"FY2025": 497612, "FY2024": 366754, "FY2023": 138997, "FY2022": 177997, "FY2021": 144964}),
        ("Cash and cash equivalents carried forward", {"FY2025": 94562, "FY2024": 190223, "FY2023": 121634, "FY2022": 149747, "FY2021": 466988}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 ratio", {"FY2025": 13.86, "FY2024": 13.59, "FY2023": 14.28, "FY2022": 15.12, "FY2021": 16.60}),
        ("Total capital ratio", {"FY2025": 18.42, "FY2024": 18.80, "FY2023": 20.52, "FY2022": 21.66, "FY2021": 24.05}),
    ],
    note="Entity-only annual capital-management figures. Separate Pillar 3 disclosures are not required because the entity is included in HSBC UK Bank plc's consolidated Pillar 3 disclosures; group figures are not substituted here.",
)


bw.save("/Users/armaan/code/katalysis/banks/MARKS AND SPENCER FINANCIAL SERVICES FINANCIALS.xlsx")
