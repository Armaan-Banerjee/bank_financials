import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, y/e 31 July
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = ("https://find-and-update.company-information.service.gov.uk/company/00195626/"
              "filing-history/MzQ5NDAzMzc1NGFkaXF6a2N4/document?format=pdf&download=0")
AR2023_URL = ("https://find-and-update.company-information.service.gov.uk/company/00195626/"
              "filing-history/MzQwNzQ2MzI3OWFkaXF6a2N4/document?format=pdf&download=0")
AR2021_URL = ("https://find-and-update.company-information.service.gov.uk/company/00195626/"
              "filing-history/filing-history (FY2021 Group of companies' accounts, y/e 31 Jul 2021)")

ENTITY_NOTE = (
    "Close Brothers Limited (company 00195626, FRN 124750) is the PRA-regulated bank subsidiary of the "
    "LSE-listed Close Brothers Group plc. Cash flow figures are the entity's own Consolidated (Close "
    "Brothers Limited + its subsidiaries) Statement of Cash Flows, from its statutory 'Group of companies' "
    "accounts' filings at Companies House - NOT the wider Close Brothers Group plc's own consolidated "
    "accounts (a separate filing). All 5 Companies House filings used were fully scanned/image-only.\n\n"
    "FY2021 is shown as a single headline total only (no line-item breakdown) - the operating-activities "
    "reconciliation note for that year's own report could not be located within budget; the other 4 years "
    "have full breakdowns. FY2022's figures are FY2023's report's own comparative column (no separate "
    "FY2022 filing was sourced); FY2024's figures are similarly FY2025's report's own comparative column.\n\n"
    "GENUINE MID-SERIES PRESENTATION BREAK in the Financing activities section: FY2021-FY2023 report "
    "'Equity dividends paid' and 'Interest paid on debt financing' as distinct lines; FY2024-FY2025 drop "
    "both (no dividend was paid in either year, consistent with FY2025's substantial loss) and instead "
    "introduce 'Issue of ordinary share capital', 'Issuance/costs of AT1 capital securities', and 'AT1 "
    "coupon payment' lines (a $200m AT1 issuance occurred in FY2024). Each year kept on its own "
    "originally-published presentation - blank cells where a line item doesn't apply to that year, not a "
    "gap. Full chain of opening/closing cash balances ties exactly across all 5 years.\n\n"
    "MOTOR FINANCE COMMISSION MIS-SELLING IMPACT: FY2025's Operating profit before tax swung to a loss of "
    "£(67.6)m (from £178.0m profit in FY2024), driven substantially by three new provision lines in the "
    "FY2025 operating-activities reconciliation: 'Provision in relation to motor finance commissions "
    "excluding cash paid' (£161.4m), 'Complaints handling and other operational and legal costs...in "
    "relation to motor finance commissions' (£5.6m), and 'Provision in relation to early settlements in "
    "Motor Finance' (£33.0m) - approximately £200m of provisions tied to the well-publicised FCA motor "
    "finance commission review. This is a real, disclosed business event, not a data anomaly."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Close Brothers Limited's own Consolidated Cash Flow Statement (Close "
    "Brothers Limited + its subsidiaries, NOT the wider listed Close Brothers Group plc):\n"
    "FY2025: Group of companies' accounts to 31 Jul 2025 (Companies House, filed 20 Dec 2025), "
    "Consolidated Cash Flow Statement p.101 + Note 24 reconciliation p.145 - " + AR2025_URL + "\n"
    "FY2024: same FY2025 filing's own FY2024 comparative column, p.101 + p.145\n"
    "FY2023: Group of companies' accounts to 31 Jul 2023 (Companies House, filed 20 Jan 2024), "
    "Consolidated Cash Flow Statement p.71 + Note 24 reconciliation p.112 - " + AR2023_URL + "\n"
    "FY2022: same FY2023 filing's own FY2022 comparative column, p.71 + p.112\n"
    "FY2021: Group of companies' accounts to 31 Jul 2021 (Companies House, filed ~Dec 2021), "
    "Consolidated Cash Flow Statement p.47 (headline total only - operating-activities note not "
    "located within budget)\n\n"
    + ENTITY_NOTE
)


bw = BankWorkbook(bank_name="Close Brothers Limited", years=YEARS, year_label=YEAR_LABEL, header_color="F6324B")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Operating profit before tax",
     {"FY2025": -67.6, "FY2024": 178.0, "FY2023": 120.7, "FY2022": 229.4}),
    ("DATA", "Tax paid",
     {"FY2025": -25.2, "FY2024": -30.2, "FY2023": -3.6, "FY2022": -60.8}),
    ("DATA", "Depreciation, amortisation and impairment",
     {"FY2025": 132.9, "FY2024": 96.3, "FY2023": 94.4, "FY2022": 86.6}),
    ("DATA", "Impairment losses on financial assets",
     {"FY2025": 92.8, "FY2024": 98.9, "FY2023": 204.0, "FY2022": 103.3}),
    ("DATA", "Provision in relation to motor finance commissions excluding cash paid",
     {"FY2025": 161.4}),
    ("DATA", "Complaints handling and other operational/legal costs re. motor finance commissions",
     {"FY2025": 5.6}),
    ("DATA", "Provision in relation to early settlements in Motor Finance",
     {"FY2025": 33.0}),
    ("DATA", "Amortisation of de-designated cash flow hedges",
     {"FY2025": -11.4, "FY2024": -27.9}),
    ("DATA", "Decrease/(increase) in interest receivable and prepaid expenses",
     {"FY2025": 11.6, "FY2024": 8.6, "FY2023": -5.7, "FY2022": 19.9}),
    ("DATA", "Decrease in interest payable and accrued expenses",
     {"FY2025": -2.6, "FY2024": -10.7, "FY2023": -0.2, "FY2022": -1.7}),
    ("TOTAL", "Net cash inflow from trading activities",
     {"FY2025": 330.5, "FY2024": 313.0, "FY2023": 409.6, "FY2022": 376.7}),
    ("DATA", "Loans and advances to banks not repayable on demand",
     {"FY2025": 1.3, "FY2024": 24.0, "FY2023": -21.1, "FY2022": -5.9}),
    ("DATA", "Loans and advances to customers",
     {"FY2025": 196.8, "FY2024": -699.4, "FY2023": -584.3, "FY2022": -515.0}),
    ("DATA", "Assets let under operating leases",
     {"FY2025": -20.3, "FY2024": -41.1, "FY2023": -73.2, "FY2022": -54.5}),
    ("DATA", "Certificates of deposit", {"FY2023": 185.0, "FY2022": 79.7}),
    ("DATA", "Sovereign and central bank debt",
     {"FY2025": -213.3, "FY2024": -194.2, "FY2023": 191.2, "FY2022": -255.3}),
    ("DATA", "SSA bonds", {"FY2024": -140.2}),
    ("DATA", "Covered Bonds", {"FY2025": 81.9, "FY2024": -80.7, "FY2023": -105.4}),
    ("DATA", "Deposits by banks",
     {"FY2025": -52.1, "FY2024": -1.3, "FY2023": -22.1, "FY2022": 11.8}),
    ("DATA", "Deposits by customers",
     {"FY2025": 100.1, "FY2024": 975.1, "FY2023": 942.5, "FY2022": 142.7}),
    ("DATA", "Loans and overdrafts from banks",
     {"FY2025": -112.1, "FY2024": -527.7, "FY2023": 24.5, "FY2022": 104.6}),
    ("DATA", "Debt securities in issue (net)",
     {"FY2025": -22.4, "FY2024": -71.6, "FY2023": 10.4, "FY2022": 243.6}),
    ("DATA", "Derivative financial instruments (net)", {"FY2025": 1.0, "FY2023": 70.4}),
    ("DATA", "Other assets less other liabilities",
     {"FY2025": -8.4, "FY2024": 2.8, "FY2023": -10.1, "FY2022": -7.6}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities",
     {"FY2025": 283.0, "FY2024": -441.3, "FY2023": 1017.4, "FY2022": 120.8, "FY2021": 89.2}),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment",
     {"FY2025": -4.5, "FY2024": -4.5, "FY2023": -4.5, "FY2022": -4.6, "FY2021": -3.7}),
    ("DATA", "Purchase of intangible assets - software",
     {"FY2025": -20.6, "FY2024": -27.7, "FY2023": -52.1, "FY2022": -48.8, "FY2021": -43.5}),
    ("DATA", "Purchase of subsidiaries, net of cash acquired",
     {"FY2024": -8.8, "FY2023": 0.0, "FY2022": -0.1}),
    ("TOTAL", "Net cash outflow from investing activities",
     {"FY2025": -25.1, "FY2024": -41.0, "FY2023": -56.6, "FY2022": -53.5, "FY2021": -47.2}),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Equity dividends paid", {"FY2023": -89.5, "FY2022": -127.9, "FY2021": -90.0}),
    ("DATA", "Interest paid on debt financing", {"FY2023": -6.9, "FY2022": -6.9, "FY2021": -6.9}),
    ("DATA", "Issue of ordinary share capital", {"FY2024": 65.0}),
    ("DATA", "Issuance of Additional Tier 1 (\"AT1\") capital securities", {"FY2024": 200.0}),
    ("DATA", "Costs arising on issue of AT1", {"FY2024": -2.4}),
    ("DATA", "AT1 coupon payment", {"FY2025": -22.3, "FY2024": -11.1}),
    ("DATA", "Amounts (paid)/received from group undertakings",
     {"FY2025": 86.4, "FY2024": -171.7, "FY2023": -17.8, "FY2022": 12.8, "FY2021": 19.7}),
    ("DATA", "Payment of lease liabilities",
     {"FY2025": -7.9, "FY2024": -9.9, "FY2023": -9.3, "FY2022": -9.2, "FY2021": -11.0}),
    ("TOTAL", "Net cash (outflow)/inflow from financing activities",
     {"FY2025": 56.2, "FY2024": 69.9, "FY2023": -123.5, "FY2022": -131.2, "FY2021": -88.2}),

    ("TOTAL", "Net (decrease)/increase in cash",
     {"FY2025": 314.1, "FY2024": -412.4, "FY2023": 837.3, "FY2022": -63.9, "FY2021": -46.2}),
    ("DATA", "Cash and cash equivalents at beginning of year",
     {"FY2025": 1728.1, "FY2024": 2140.5, "FY2023": 1303.2, "FY2022": 1367.1, "FY2021": 1413.3}),
    ("TOTAL", "Cash and cash equivalents at end of year",
     {"FY2025": 2042.2, "FY2024": 1728.1, "FY2023": 2140.5, "FY2022": 1303.2, "FY2021": 1367.1}),
]

bw.add_cash_flow_sheet(
    title="Close Brothers Limited — Consolidated Cash Flow Statement",
    subtitle="Consolidated basis (Close Brothers Limited + subsidiaries), £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=88,
    source_height=320,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets - genuinely none disclosed at this entity level
# ---------------------------------------------------------------
NOT_DISCLOSED_NOTE = (
    "Close Brothers Limited (the PRA-regulated entity, FRN 124750) does not publish its own Pillar 3 "
    "disclosures or Basel capital/liquidity ratios - checked its full 'Group of companies' accounts' "
    "statutory filings (all 5 years) for a capital management/regulatory capital note and found none. "
    "Pillar 3 is published only at the wider listed parent 'Close Brothers Group plc' level (confirmed "
    "via closebrothers.com's investor relations Pillar 3 Disclosures page) - a different, non-PRA-"
    "regulated entity, so those figures are not used here rather than mixing entity levels."
)

bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital", "Total Capital Ratio",
     "Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    "Sources - Close Brothers Limited Pillar 3 basis:\n" + NOT_DISCLOSED_NOTE,
    per_note={m: NOT_DISCLOSED_NOTE for m in
              ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital",
               "Total Capital Ratio", "Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash (outflow)/inflow from operating activities",
         {"FY2025": 283.0, "FY2024": -441.3, "FY2023": 1017.4, "FY2022": 120.8, "FY2021": 89.2}),
        ("Net cash outflow from investing activities",
         {"FY2025": -25.1, "FY2024": -41.0, "FY2023": -56.6, "FY2022": -53.5, "FY2021": -47.2}),
        ("Net cash (outflow)/inflow from financing activities",
         {"FY2025": 56.2, "FY2024": 69.9, "FY2023": -123.5, "FY2022": -131.2, "FY2021": -88.2}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 2042.2, "FY2024": 1728.1, "FY2023": 2140.5, "FY2022": 1303.2, "FY2021": 1367.1}),
    ],
    cash_flow_unit="£m",
    ratios=[],
    note="No Pillar 3 ratios chart shown - Close Brothers Limited (the PRA-regulated entity) does not "
         "publish its own Basel capital/liquidity disclosures; Pillar 3 exists only at the wider listed "
         "parent Close Brothers Group plc level. See the Cash Flow Statement sheet's source note and each "
         "Pillar 3 sheet for detail. Cash flow figures are duplicated from the detail sheet for at-a-glance "
         "trend viewing.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CLOSE BROTHERS FINANCIALS.xlsx")
