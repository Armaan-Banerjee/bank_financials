import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzQ3OTMzNTI0NWFkaXF6a2N4/document?download=0&format=pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzQzMzA4NzcwMWFkaXF6a2N4/document?download=0&format=pdf"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzM4OTExNTc1NmFkaXF6a2N4/document?download=0&format=pdf"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzM1NTU5ODQzNmFkaXF6a2N4/document?download=0&format=pdf"
PILLAR3_2021_URL = "https://www.persiabank.co.uk/Pillar%203%202021%20v3.pdf"

# The Bank reports in EUR and discloses its own EUR/GBP rates in the accounting
# policies.  Rates are EUR per GBP, so EUR / rate = GBP.
AVG_RATE = {"FY2025": 0.8390, "FY2024": 0.8630, "FY2023": 0.8525, "FY2022": 0.8525, "FY2021": 0.8925}
YEAR_END_RATE = {"FY2025": 0.8350, "FY2024": 0.8550, "FY2023": 0.8800, "FY2022": 0.8475, "FY2021": 0.8525}

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
    "over going concern, while later reports continued on a going-concern basis."
)

FX_NOTE = (
    "FX METHODOLOGY: the Bank's accounting policies disclose EUR/GBP rates (EUR per GBP). Flow figures are divided "
    "by the year's disclosed average rate; balance figures are divided by the year's disclosed year-end rate. The "
    "cash-flow sheet includes the Bank's own exchange-difference line and a programmatic GBP translation line where "
    "the use of average rates for flows and year-end rates for balances creates a residual. FY2021 opening cash is "
    "left blank because the source does not provide a FY2020 year-end rate in the reviewed five-year source set."
)

CASH_FLOW_SOURCES = (
    "Sources - Persia International Bank Plc's own entity-level Statements of Cash Flows, converted from EUR to GBP "
    "using the Bank's disclosed rates (see FX note):\n"
    f"FY2025: Annual Report and Financial Statements for year ended 31 March 2025, p.39 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements for year ended 31 March 2024, p.32 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements for year ended 31 March 2023, p.31 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for year ended 31 March 2022, p.30 - {AR2022_URL}\n"
    "FY2021: FY2022 Annual Report's comparative column, p.30 - " + AR2022_URL + "\n\n" + ENTITY_NOTE + "\n" + FX_NOTE
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
    return {y: round(v / AVG_RATE[y], 1) for y, v in values.items()}


def stock(values):
    return {y: round(v / YEAR_END_RATE[y], 1) for y, v in values.items()}


bw = BankWorkbook(bank_name="Persia International Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="6B3E75")


def stock_v(v, y):
    return round(v / YEAR_END_RATE[y], 1)


def flow_v(v, y):
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
    f"this is the latest filing that still contains a full FY2021 column) - {AR2022_URL}\n\n"
    + ENTITY_NOTE + "\n" + FX_NOTE + "\n\n"
    "RESTATEMENT: the Annual Report and Financial Statements 2024's own Note 33 restates the Bank's FY2022/FY2023 "
    "figures (e.g. FY2023 closing retained earnings restated from EUR (17,439k) to EUR (18,414k), a genuine "
    "EUR 975k downward adjustment; FY2023 loans and advances to customers also restated from EUR 24,653k net to "
    "EUR 28,105k net, reclassifying interest receivable into that line). Each year's Balance Sheet/P&L/Equity "
    "column here uses that year's own originally-reported figures (not the later restated comparative), "
    "consistent with every other bank in this project; the restatement is instead shown as its own explicit "
    "bridging row in the Statement of Changes in Equity, between FY2023's originally-reported closing balance "
    "and FY2024's own restated opening balance, per the Bank's own Note 33."
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
    ("DATA", "Cash and cash equivalent", {"FY2025": 77114, "FY2024": 75472, "FY2023": 51929, "FY2022": 103084, "FY2021": 25484}),
    ("DATA", "Loans and advances to banks", {"FY2025": 45768, "FY2024": 48056, "FY2023": 122438, "FY2022": 67577, "FY2021": 151008}),
    ("DATA", "Loans and advances to customers", {"FY2025": 27178, "FY2024": 49438, "FY2023": 24653, "FY2022": 32356, "FY2021": 36278}),
    ("DATA", "Property, plant and equipment", {"FY2025": 2855, "FY2024": 3193, "FY2023": 4510, "FY2022": 3432, "FY2021": 3318}),
    ("DATA", "Intangible assets (FY2023 report shows this line as nil/dash)", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 89, "FY2021": 268}),
    ("DATA", "Other assets", {"FY2025": 2577, "FY2024": 1984, "FY2023": 1305, "FY2022": 2698, "FY2021": 1397}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 134, "FY2024": 147, "FY2023": 3971, "FY2022": 652, "FY2021": 723}),
    ("TOTAL", "Total assets", {"FY2025": 155626, "FY2024": 178290, "FY2023": 208806, "FY2022": 209888, "FY2021": 218476}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 37468, "FY2024": 41447, "FY2023": 68704, "FY2022": 69319, "FY2021": 78551}),
    ("DATA", "Deposits from customers", {"FY2025": 4597, "FY2024": 5603, "FY2023": 5608, "FY2022": 6313, "FY2021": 6270}),
    ("DATA", "Other liabilities", {"FY2025": 3137, "FY2024": 3547, "FY2023": 1933, "FY2022": 2498, "FY2021": 3011}),
    ("TOTAL", "Total liabilities", {"FY2025": 45202, "FY2024": 50597, "FY2023": 76245, "FY2022": 78130, "FY2021": 87832}),
    ("SECTION", "Shareholders' equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 150000, "FY2024": 150000, "FY2023": 150000, "FY2022": 150000, "FY2021": 150000}),
    ("DATA", "Retained earnings", {"FY2025": -39576, "FY2024": -22307, "FY2023": -17439, "FY2022": -18242, "FY2021": -19356}),
    ("TOTAL", "Total shareholders' equity", {"FY2025": 110424, "FY2024": 127693, "FY2023": 132561, "FY2022": 131758, "FY2021": 130644}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 155626, "FY2024": 178290, "FY2023": 208806, "FY2022": 209888, "FY2021": 218476}),
]
bs_rows = [(kind, label, {y: stock_v(v, y) for y, v in values.items()}) for kind, label, values in bs_rows_eur]

bw.add_balance_sheet_sheet(
    title="Persia International Bank Plc — Balance Sheet",
    subtitle="Entity-level basis, £'000 converted from EUR (see FX note). Each year shown on its own originally-reported basis - "
              "see the RESTATEMENT note for a genuine FY2022/FY2023 restatement disclosed in the Annual Report and Financial "
              "Statements 2024's own Note 33, bridged explicitly in the Statement of Changes in Equity rather than blended here.",
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
    ("DATA", "Interest and similar income", {"FY2025": 7044, "FY2024": 7890, "FY2023": 6767, "FY2022": 3644, "FY2021": 3965}),
    ("DATA", "Interest and similar expenses", {"FY2025": -357, "FY2024": -297, "FY2023": -198, "FY2022": -456, "FY2021": -302}),
    ("TOTAL", "Net Interest Income", {"FY2025": 6687, "FY2024": 7593, "FY2023": 6569, "FY2022": 3188, "FY2021": 3663}),
    ("DATA", "Fees and commission income", {"FY2025": 75, "FY2024": 340, "FY2023": 444, "FY2022": 175, "FY2021": 184}),
    ("DATA", "Fees and commission expense", {"FY2025": -14, "FY2024": -47, "FY2023": -109, "FY2022": -81, "FY2021": -22}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 61, "FY2024": 293, "FY2023": 335, "FY2022": 94, "FY2021": 162}),
    ("DATA", "Other operating (expense)/income", {"FY2025": -315, "FY2024": -1347, "FY2023": 686, "FY2022": 1611, "FY2021": 842}),
    ("DATA", "Credit impairment / Net impairment (charge)/reversal (FY2025/FY2024's own report labels this 'Credit impairment'; FY2023's own report labels it 'Net impairment (charge)/reversal')", {"FY2025": -16719, "FY2024": -3137, "FY2023": -1374}),
    ("TOTAL", "Net operating (loss)/income", {"FY2025": -10286, "FY2024": 3402, "FY2023": 6216, "FY2022": 4893, "FY2021": 4667}),
    ("DATA", "Administrative expenses", {"FY2025": -6643, "FY2024": -6964, "FY2023": -6332, "FY2022": -5261, "FY2021": -5263}),
    ("DATA", "Depreciation", {"FY2025": -340, "FY2024": -331, "FY2023": -185, "FY2022": -252, "FY2021": -313}),
    ("DATA", "Impairment of property (FY2021 only, per that year's own report)", {"FY2021": -542}),
    ("DATA", "Reversal of impairment / Net impairment reversal (FY2021-FY2023's own reports only; FY2024/FY2025's own reports fold this into 'Credit impairment' above instead)", {"FY2023": 1104, "FY2022": 1734, "FY2021": 914}),
    ("TOTAL", "Total operating expenses", {"FY2025": -6983, "FY2024": -7295, "FY2023": -5413, "FY2022": -3779, "FY2021": -5204}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": -17269, "FY2024": -3893, "FY2023": 803, "FY2022": 1114, "FY2021": -537}),
    ("DATA", "Tax on profit", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Profit/(loss) for the year attributable to equity holders", {"FY2025": -17269, "FY2024": -3893, "FY2023": 803, "FY2022": 1114, "FY2021": -537}),
    ("TOTAL", "Total comprehensive income/(expense) for the year attributable to equity holders", {"FY2025": -17269, "FY2024": -3893, "FY2023": 803, "FY2022": 1114, "FY2021": -537}),
]
pl_rows = [(kind, label, {y: flow_v(v, y) for y, v in values.items()}) for kind, label, values in pl_rows_eur]

bw.add_income_statement_sheet(
    title="Persia International Bank Plc — Profit & Loss",
    subtitle="Entity-level basis, £'000 converted from EUR (see FX note). Structure genuinely differs year to year - see the "
              "'Credit impairment / Net impairment (charge)/reversal' and 'Reversal of impairment' row notes. FY2021's own "
              "report uniquely shows a standalone 'Impairment of property' charge alongside a separate impairment reversal. "
              "The Bank reports no OCI in any year - Total comprehensive income/(expense) equals Profit/(loss) for the year "
              "in every year.",
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
    subtitle="Chronological roll-forward, oldest to newest, £'000 converted from EUR (see FX note). Equity reconciliation "
              "ladder confirmed in EUR terms across all 5 years - zero undocumented plug rows. The one genuine bridging row "
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
OPERATING_EUR = {"FY2025": 1998, "FY2024": -14216, "FY2023": 5116, "FY2022": 3399, "FY2021": -368}
INVESTING_EUR = {"FY2025": -2, "FY2024": -72, "FY2023": -46, "FY2022": -44, "FY2021": 0}
FINANCING_EUR = {"FY2025": -227, "FY2024": -27477, "FY2023": -1320, "FY2022": -9186, "FY2021": -1609}
NET_CHANGE_EUR = {"FY2025": 1787, "FY2024": -41765, "FY2023": 3750, "FY2022": -5831, "FY2021": -1977}
EXCHANGE_EUR = {"FY2025": -145, "FY2024": 1009, "FY2023": -44, "FY2022": 0, "FY2021": 0}
OPENING_EUR = {"FY2025": 75472, "FY2024": 116228, "FY2023": 170661, "FY2022": 176492, "FY2021": 178469}
CLOSING_EUR = {"FY2025": 77114, "FY2024": 75472, "FY2023": 174367, "FY2022": 170661, "FY2021": 176492}

closing_gbp = stock(CLOSING_EUR)
# Opening balances are the prior year's converted closing balances.  This keeps
# the cash-flow chain internally consistent when the Bank's year-end FX rates
# differ between years.
opening_gbp = {
    "FY2025": closing_gbp["FY2024"],
    "FY2024": closing_gbp["FY2023"],
    "FY2023": closing_gbp["FY2022"],
    "FY2022": closing_gbp["FY2021"],
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
    subtitle="Entity-level basis, £'000 converted from EUR; see source note for sanctions, reporting basis and FX methodology",
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

bw.add_asset_quality_sheet(
    title="Persia International Bank Plc — Asset Quality",
    subtitle="Entity-level basis, £'000 converted from EUR (see FX note). Net loans and advances to customers ties exactly to "
              "the Balance Sheet every year. FY2022's own component split (Commercial/Syndicated) differs from a later "
              "report's FY2022 comparative despite both giving the identical net figure (EUR 32,356k) - a genuine "
              "component-level reclassification, not a data error; this year's own contemporaneous report is used, as "
              "elsewhere in this workbook.",
    rows=aq_rows + aq_ratio_rows_eur + aq_stage_charge + aq_fy25_exposure,
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

metric("CET1 Capital", "£'000 (conv. from EUR)", [("Common Equity Tier 1 capital / disclosed Tier one base", CAPITAL_GBP)], note=CAPITAL_NOTE)
metric("CET1 Ratio", "%", [("CET1 ratio", {"FY2021": "Not publicly disclosed"})], note=NOT_DISCLOSED)
metric("Tier 1 Capital", "£'000 (conv. from EUR)", [("Tier one / total regulatory capital base", CAPITAL_GBP)], note=CAPITAL_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", {"FY2021": "Not publicly disclosed"})], note=NOT_DISCLOSED)
metric("Total Capital", "£'000 (conv. from EUR)", [("Total regulatory capital base", CAPITAL_GBP)], note=CAPITAL_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", {"FY2021": "Not publicly disclosed"})], note=NOT_DISCLOSED)
metric("Total RWAs", "£'000 (conv. from EUR)", [("Pillar 1 risk-weighted assets", RWA_GBP)], note="Only FY2021 is directly disclosed: €318.824m in the 2021 Pillar 3 disclosure, p.18. Later years are not publicly disclosed and are not calculated from capital because no corresponding capital ratio is stated.")

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
    "Credit and counterparty credit risk": {"FY2021": 298566},
    "Market risk": {"FY2021": 15321},
    "Operational risk": {"FY2021": 4937},
}
rwa_breakdown_rows = [
    ("DATA", label, {y: stock_v(v, y) for y, v in values.items()})
    for label, values in RWA_BREAKDOWN_EUR.items()
] + [("TOTAL", "Total Pillar 1 risk-weighted assets", RWA_GBP)]

bw.add_rwa_breakdown_sheet(
    title="Persia International Bank Plc — RWA Breakdown",
    subtitle="FY2021 only (recovered via Wayback Machine snapshot of the Bank's own Pillar 3 Disclosure 2021, p.18, after the "
              "Bank's live site refused every direct TLS connection attempt this session). £'000 converted from EUR (see FX "
              "note). Ties exactly to the Total RWAs sheet. FY2022-FY2025 not publicly disclosed - the Bank's Annual Reports "
              "state Pillar 3 disclosure is available on request, and no public standalone Pillar 3 document for those years "
              "was located.",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Sources - Persia International Bank Plc Pillar 3 Disclosure 2021, p.18 (Pillar 1 capital requirements table), "
        "recovered via Wayback Machine snapshot (captured 10 January 2026) - "
        "http://web.archive.org/web/20260110002617if_/http://www.persiabank.co.uk/Pillar%203%202021%20v3.pdf "
        "(original URL, unreachable this session due to a TLS handshake failure on every attempt: " + PILLAR3_2021_URL + ")\n\n"
        + ENTITY_NOTE + "\n" + FX_NOTE
    ),
    first_col_width=54,
    source_height=220,
    unit_suffix=" (£'000, conv. from EUR)",
)

metric("Leverage Ratio", "%", [("Leverage ratio", {"FY2021": "53.32%"})], note="FY2021 only: directly disclosed in the Bank's 2021 Pillar 3 disclosure, p.26. No public later-year value found.")
metric("LCR", "%", [("Liquidity Coverage Ratio (simple average of 12 monthly reports)", {"FY2021": "221.13%"})], note="FY2021 only: directly disclosed in the Bank's 2021 Pillar 3 disclosure, p.16. No public later-year value found.")
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
        ("Opening equity", {"FY2022": stock_v(130644, "FY2021"), "FY2023": stock_v(131758, "FY2022"), "FY2024": stock_v(132561, "FY2023"), "FY2025": stock_v(127693, "FY2024")}),
        ("Total comprehensive income/(expense) for the year", {"FY2021": flow_v(-537, "FY2021"), "FY2022": flow_v(1114, "FY2022"), "FY2023": flow_v(803, "FY2023"), "FY2024": flow_v(-3893, "FY2024"), "FY2025": flow_v(-17269, "FY2025")}),
        ("Other equity movements, net (FY2021: share capital issuance; FY2024: prior period restatement per Note 33)", {"FY2021": flow_v(50000, "FY2021"), "FY2022": 0, "FY2023": 0, "FY2024": stock_v(-975, "FY2023"), "FY2025": 0}),
        ("Closing equity", {"FY2021": stock_v(130644, "FY2021"), "FY2022": stock_v(131758, "FY2022"), "FY2023": stock_v(132561, "FY2023"), "FY2024": stock_v(127693, "FY2024"), "FY2025": stock_v(110424, "FY2025")}),
    ],
    equity_changes_unit="£'000 (conv. from EUR)",
    cash_flow_totals=[
        ("Net cash flow from operating activities", flow(OPERATING_EUR)),
        ("Net cash flow from investing activities", flow(INVESTING_EUR)),
        ("Cash and cash equivalents at end of year", closing_gbp),
    ],
    cash_flow_unit="£'000 (conv. from EUR)",
    ratios=[("Leverage Ratio", {"FY2021": "53.32%"}), ("LCR", {"FY2021": "221.13%"})],
    note="FY2021 leverage and LCR are the only directly disclosed regulatory liquidity metrics located in the public source set; later years are intentionally blank/not disclosed. FY2021's opening equity is blank because the Bank's disclosed EUR/GBP rate series in this workbook's source set only starts at FY2021 - see the Statement of Changes in Equity sheet for detail.",
)

bw.save("/Users/armaan/code/katalysis/banks/PERSIA INTERNATIONAL BANK FINANCIALS.xlsx")
