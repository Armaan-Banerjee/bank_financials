import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

# All 5 years sourced from Companies House filings (fully scanned/image-only,
# 0 text blocks per page) - the bank's registered site (www.kingdombank.co.uk)
# is an unrelated expired/parked domain; the real site is www.kingdom.bank.
CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/04346834/filing-history"
FY2025_URL = f"{CH_BASE}/MzUzMjA2MDkzOWFkaXF6a2N4/document?format=pdf&download=0"
FY2024_URL = f"{CH_BASE}/MzQ3Mjc3MDk4N2FkaXF6a2N4/document?format=pdf&download=0"
FY2023_URL = f"{CH_BASE}/MzQyNzk5NjY3OGFkaXF6a2N4/document?format=pdf&download=0"
FY2022_URL = f"{CH_BASE}/MzM3Nzc1Mzk0NWFkaXF6a2N4/document?format=pdf&download=0"
FY2021_URL = f"{CH_BASE}/MzM0MzYxNTEyM2FkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "Entity: Kingdom Bank Limited, company 04346834 (formerly Kingdom Banking Limited), FRN 400972 - "
    "confirmed via Banks List 2608.xlsx and Companies House, no identity ambiguity. A small specialist "
    "bank providing mortgages, savings and insurance broking to UK churches, Christian charities and "
    "individuals in Christian ministry; parent/ultimate controlling party is Lamb's Passage Holding "
    "Limited (LPHL), whose investor group includes Stewardship Services (UKET) Limited. Solo/Bank basis "
    "throughout - no group consolidation applies. All 5 years' filings on Companies House are fully "
    "scanned/image-only (0 extractable text on every page); the bank's registered-looking domain "
    "www.kingdombank.co.uk is an unrelated expired/parked domain (a GoDaddy-style parking page) - its "
    "real site is www.kingdom.bank, which hosts only the FY2025 Annual Report and no standalone Pillar 3 "
    "disclosures."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Kingdom Bank Limited's own Statement of cash flows, £'000, Bank/solo basis "
    "(Companies House filings, all fully scanned):\n"
    f"FY2025 (own) & FY2024 (comparative, cross-checked against FY2024's own report): Annual Report & "
    "Accounts 2025, p.38 (Statement of cash flows) - " + FY2025_URL + "\n"
    f"FY2024 (own): Annual Report & Accounts 2024 - " + FY2024_URL + "\n"
    f"FY2023 (own) & FY2022 (comparative): Annual Report & Accounts 2023, p.39 (Statement of cash flows) - " + FY2023_URL + "\n"
    f"FY2022 (own): Annual Report & Accounts 2022 - " + FY2022_URL + "\n"
    f"FY2021 (own) & FY2020 comparative (not used): Annual Report & Accounts 2021, p.33 (Statement of cash "
    "flows) - " + FY2021_URL + "\n"
    + ENTITY_NOTE + "\n"
    "Every year-end closing balance ties exactly to the following year's opening balance across all 5 years "
    "(FY2021 closing £20,030k = FY2022 opening; FY2022 closing £24,861k = FY2023 opening; FY2023 closing "
    "£35,058k = FY2024 opening; FY2024 closing £39,791k = FY2025 opening) - no restatements found."
)


def p3_sources():
    return (
        "Sources - Kingdom Bank Limited, Bank/solo basis, £'000 (from each year's own audited Statement of "
        "financial position and Strategic Report):\n"
        f"FY2025 & FY2024: Annual Report & Accounts 2025, p.10 (Capital) and p.36 (Statement of financial "
        "position) - " + FY2025_URL + "\n"
        f"FY2023 & FY2022: Annual Report & Accounts 2023, p.10 (Capital) and p.37 (Statement of financial "
        "position) - " + FY2023_URL + "\n"
        f"FY2021: Annual Report & Accounts 2021, p.31 (Statement of financial position) - " + FY2021_URL + "\n"
        + "No standalone Pillar 3/KM1 disclosure document was found on the bank's own site (www.kingdom.bank) "
        "or via Companies House - each Annual Report's 'Capital' section states only that 'the Bank's "
        "regulatory capital consists of shareholders' funds (\"Core Equity Tier 1\") and subordinated "
        "liabilities (\"Tier 2\")' with £m totals, and no year discloses Total RWAs or any capital/liquidity "
        "ratio (%) figure. This is consistent with the PRA's Small Domestic Deposit Taker (SDDT) thin-"
        "disclosure pattern already seen at Cynergy Bank Plc/DF Capital Bank Limited in this project."
    )


NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed. Kingdom Bank's Annual Reports state only narrative £m totals for shareholders' "
    "funds (CET1) and subordinated liabilities (Tier 2) in the 'Capital' section of the Strategic Report - "
    "no Total RWAs or any capital/liquidity ratio (%) figure is given in any of the 5 years reviewed, and no "
    "standalone Pillar 3 document exists on the bank's own site or via Companies House. See the CET1 "
    "Capital/Total Capital sheets' source note for the SDDT-regime context that plausibly explains this."
)

TIER1_NOTE = (
    "Kingdom Bank's own Annual Reports state regulatory capital consists only of shareholders' funds "
    "(\"Core Equity Tier 1\") and subordinated liabilities (\"Tier 2\") - no Additional Tier 1 instruments "
    "are in issue in any year reviewed, so Tier 1 Capital equals CET1 Capital exactly. See the CET1 Capital "
    "sheet for the same figures and source."
)

bw = BankWorkbook(bank_name="Kingdom Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="7A1F2B")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Net cash (used in)/generated from operating activities excluding tax", {"FY2025": -1079, "FY2024": -481, "FY2023": 10255, "FY2022": 3157, "FY2021": -630}),
    ("DATA", "Taxation paid", {"FY2025": -55, "FY2024": -102, "FY2023": -11, "FY2022": -25}),
    ("TOTAL", "Net cash (used in)/generated from operating activities", {"FY2025": -1134, "FY2024": -583, "FY2023": 10244, "FY2022": 3132, "FY2021": -630}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of intangible assets", {"FY2025": 0, "FY2024": 0, "FY2023": -23, "FY2022": -16, "FY2021": -47}),
    ("DATA", "Purchase of tangible assets", {"FY2025": -43, "FY2024": -41, "FY2023": -24, "FY2022": -24, "FY2021": -197}),
    ("DATA", "Sale of investment property", {"FY2021": 2013}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {"FY2025": -43, "FY2024": -41, "FY2023": -47, "FY2022": -40, "FY2021": 1769}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of subordinated liabilities", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -61, "FY2021": -670}),
    ("DATA", "Share allotment", {"FY2025": 1170, "FY2024": 5400, "FY2023": 0, "FY2022": 1800, "FY2021": 0}),
    ("DATA", "Dividends paid", {"FY2025": -70, "FY2024": -43}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {"FY2025": 1100, "FY2024": 5357, "FY2023": 0, "FY2022": 1739, "FY2021": -670}),
    ("TOTAL", "Net movement in cash and cash equivalents", {"FY2025": -77, "FY2024": 4733, "FY2023": 10197, "FY2022": 4831, "FY2021": 469}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 39791, "FY2024": 35058, "FY2023": 24861, "FY2022": 20030, "FY2021": 19561}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 39714, "FY2024": 39791, "FY2023": 35058, "FY2022": 24861, "FY2021": 20030}),
]

bw.add_cash_flow_sheet(
    title="Kingdom Bank Limited — Statement of Cash Flows",
    subtitle="Bank/solo basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=200,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Bank/solo basis, {unit}" if unit else "Bank/solo basis",
                         rows_data, p3_sources(), note=note, first_col_width=52, source_height=190)


CET1_VALUES = {"FY2025": 15808, "FY2024": 15512, "FY2023": 9876, "FY2022": 9353, "FY2021": 7451}
TIER2_VALUES = {"FY2025": 700, "FY2024": 700, "FY2023": 700, "FY2022": 700, "FY2021": 761}
TOTAL_CAPITAL_VALUES = {y: CET1_VALUES[y] + TIER2_VALUES[y] for y in YEARS}

metric(
    "CET1 Capital", "£'000",
    [("Shareholders' funds (Core Equity Tier 1)", CET1_VALUES)],
)

bw.add_not_disclosed_metric_sheets(
    ["CET1 Ratio"], p3_sources(), per_note={"CET1 Ratio": NOT_DISCLOSED_NOTE},
)

metric(
    "Tier 1 Capital", "£'000",
    [("Shareholders' funds (Core Equity Tier 1)", CET1_VALUES)],
    note=TIER1_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["Tier 1 Ratio"], p3_sources(), per_note={"Tier 1 Ratio": NOT_DISCLOSED_NOTE},
)

metric(
    "Total Capital", "£'000",
    [
        ("Shareholders' funds (Core Equity Tier 1)", CET1_VALUES),
        ("Subordinated liabilities (Tier 2)", TIER2_VALUES),
        ("Total regulatory capital (CET1 + Tier 2)", TOTAL_CAPITAL_VALUES),
    ],
)

bw.add_not_disclosed_metric_sheets(
    ["Total Capital Ratio", "Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in
              ["Total Capital Ratio", "Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flow from/(used in) operating activities", {"FY2025": -1134, "FY2024": -583, "FY2023": 10244, "FY2022": 3132, "FY2021": -630}),
        ("Net cash flow from/(used in) investing activities", {"FY2025": -43, "FY2024": -41, "FY2023": -47, "FY2022": -40, "FY2021": 1769}),
        ("Net cash flow from/(used in) financing activities", {"FY2025": 1100, "FY2024": 5357, "FY2023": 0, "FY2022": 1739, "FY2021": -670}),
        ("Cash and cash equivalents at end of year", {"FY2025": 39714, "FY2024": 39791, "FY2023": 35058, "FY2022": 24861, "FY2021": 20030}),
    ],
    cash_flow_unit="£'000",
    ratios=[],
    note="No Pillar 3 ratio-type metrics (CET1/Tier 1/Total Capital Ratio, Leverage Ratio, LCR, NSFR, MREL "
         "Ratio) or Total RWAs are disclosed by Kingdom Bank in any of the 5 years reviewed, so no ratios "
         "chart is shown here - see each individual Pillar 3 sheet. CET1 Capital, Tier 1 Capital and Total "
         "Capital (£'000) are disclosed for all 5 years on their own sheets. Cash flow figures are duplicated "
         "from the Cash Flow Statement sheet for at-a-glance trend viewing.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/KINGDOM BANK FINANCIALS.xlsx")
