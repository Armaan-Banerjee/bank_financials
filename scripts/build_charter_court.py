import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

BASE = "https://find-and-update.company-information.service.gov.uk/company/06749498/filing-history"
AR2025_URL = BASE + "/MzUxNjgzMTY2OWFkaXF6a2N4/document?format=pdf&download=0"  # filed 23 Apr 2026, covers FY2025/FY2024
AR2024_URL = BASE + "/MzQ2MzY3MjYwMmFkaXF6a2N4/document?format=pdf&download=0"  # filed 23 Apr 2025, covers FY2024/FY2023
AR2023_URL = BASE + "/MzQxOTgyMzYzMWFkaXF6a2N4/document?format=pdf&download=0"  # filed 30 Apr 2024, covers FY2023/FY2022
AR2022_URL = BASE + "/MzM3NjA1NDU0NWFkaXF6a2N4/document?format=pdf&download=0"  # filed 18 Apr 2023, covers FY2022/FY2021
AR2021_URL = BASE + "/MzMzNTQwMDY5MWFkaXF6a2N4/document?format=pdf&download=0"  # filed 07 Apr 2022, covers FY2021/FY2020

ENTITY_NOTE = (
    "Charter Court Financial Services Limited (company 06749498) trades under the Charter "
    "Savings Bank, Precise Mortgages and Exact Mortgage Experts brands - a UK specialist "
    "mortgage lender. Its parent was CCFSG Holdings Limited (formerly Charter Court Financial "
    "Services Group PLC, merged with OneSavings Bank plc in 2019) until 22 September 2025, when "
    "the Company was transferred directly to OneSavings Bank plc; the ultimate parent throughout "
    "is OSB GROUP PLC. All 5 Companies House filings used were fully scanned/image-only, "
    "transcribed via page rendering. Each year's own originally-published Statement of Cash "
    "Flows is used as that year's column (not a later restated comparative) - the full chain "
    "ties exactly (each year's closing balance = the next year's opening balance) across all 5 "
    "years. FY2022's own Annual Report discloses a voluntary restatement of its FY2021 "
    "comparative (reclassifying £73.3m of cash collateral/margin on interest rate swaps from "
    "financing to operating activities, plus a presentation gross-up of fair-value-hedge and "
    "derivative movements) - FY2021's own originally-published figures are used here regardless, "
    "per this project's convention, so this workbook's FY2021 column will not tie to the "
    "restated FY2021 comparative shown in the FY2022 report."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Charter Court Financial Services Limited's own Statement of Cash "
    "Flows, from each year's own originally-filed Companies House accounts (not a later "
    "restated comparative):\n"
    f"FY2025: Full accounts made up to 31 Dec 2025, p.69 (Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2024: Full accounts made up to 31 Dec 2024, p.68 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Full accounts made up to 31 Dec 2023, p.56 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Full accounts made up to 31 Dec 2022, p.50 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: Full accounts made up to 31 Dec 2021, p.51 (Statement of Cash Flows) - {AR2021_URL}\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Charter Court Financial Services Limited's own Strategic Report narrative "
        "(no standalone Pillar 3 document or KM1 template found at this entity level; the "
        "Directors' Report explicitly refers readers to \"the OSBG annual report and accounts\" "
        "for further capital/risk detail):\n"
        f"FY2025/FY2024: Full accounts to 31 Dec 2025, p.44 (KPIs table, CET1 only) - {AR2025_URL}\n"
        f"FY2023/FY2022: Full accounts to 31 Dec 2023, p.19 (Solvency Risk narrative) - {AR2023_URL}\n"
        + ("\n" + extra if extra else "")
    )


bw = BankWorkbook(bank_name="Charter Court Financial Services Limited", years=YEARS, year_label=YEAR_LABEL, header_color="C83584")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": 149.2, "FY2024": 191.2, "FY2023": 105.3, "FY2022": 263.3, "FY2021": 187.4}),
    ("DATA", "Adjustments for non-cash and other items", {"FY2025": 26.6, "FY2024": 93.9, "FY2023": 117.7, "FY2022": -1.1, "FY2021": 127.1}),
    ("DATA", "Changes in operating assets and liabilities", {"FY2025": 581.9, "FY2024": 1103.6, "FY2023": 92.0, "FY2022": -388.0, "FY2021": -254.9}),
    ("TOTAL", "Cash generated from/(used in) operating activities", {"FY2025": 757.7, "FY2024": 1388.7, "FY2023": 315.0, "FY2022": -125.8, "FY2021": 59.6}),
    ("DATA", "Provisions paid", {"FY2025": -0.3}),
    ("DATA", "Net tax paid", {"FY2025": -40.0, "FY2024": -53.3, "FY2023": -35.9, "FY2022": -69.3, "FY2021": -47.1}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 717.4, "FY2024": 1335.4, "FY2023": 279.1, "FY2022": -195.1, "FY2021": 12.5}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Sales of loans and advances to customers", {"FY2021": 0}),
    ("DATA", "Maturity and sales of investment securities", {"FY2025": 256.3, "FY2024": 360.3, "FY2023": 49.5, "FY2022": 215.3, "FY2021": 535.8}),
    ("DATA", "Purchases of investment securities", {"FY2025": -526.9, "FY2024": -251.4, "FY2023": -72.2, "FY2022": -40.2, "FY2021": -452.5}),
    ("DATA", "Interest received on investment securities", {"FY2025": 51.3, "FY2024": 18.3, "FY2023": 11.8, "FY2022": 5.1}),
    ("DATA", "Purchases of property, plant and equipment and intangible assets", {"FY2025": -0.1, "FY2024": -0.2, "FY2023": -0.1, "FY2022": -0.6, "FY2021": -1.8}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": -219.4, "FY2024": 127.0, "FY2023": -11.0, "FY2022": 179.6, "FY2021": 81.5}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Financing received", {"FY2025": 1174.2, "FY2024": 1170.9, "FY2023": 731.3, "FY2022": 309.5, "FY2021": 1899.5}),
    ("DATA", "Financing repaid", {"FY2025": -644.1, "FY2024": -1777.5, "FY2023": -804.9, "FY2022": -2.5, "FY2021": -1667.9}),
    ("DATA", "Interest paid on financing", {"FY2025": -64.3, "FY2024": -127.1, "FY2023": -92.2, "FY2022": -15.4, "FY2021": -1.8}),
    ("DATA", "Coupon paid on AT1 securities", {"FY2024": -3.6, "FY2023": -3.6, "FY2022": -3.6}),
    ("DATA", "Redemption of AT1 securities", {"FY2025": -53.3}),
    ("DATA", "Issuance of AT1 securities", {"FY2025": 59.5, "FY2021": 60.0}),
    ("DATA", "Dividends paid", {"FY2025": -169.4, "FY2024": -134.9, "FY2023": -124.9, "FY2022": -75.2}),
    ("DATA", "Net swap interest paid on subordinated liabilities and senior notes", {"FY2024": -2.3}),
    ("DATA", "Net swap interest paid on structural hedge", {"FY2024": -1.2}),
    ("DATA", "Repayments of principal portion of lease liabilities", {"FY2025": -7.6, "FY2024": -0.9, "FY2023": -1.0, "FY2022": -1.0, "FY2021": -1.0}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": 295.0, "FY2024": -876.6, "FY2023": -295.3, "FY2022": 211.8, "FY2021": 288.8}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 793.0, "FY2024": 585.8, "FY2023": -27.2, "FY2022": 196.3, "FY2021": 382.8}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 2037.8, "FY2024": 1452.0, "FY2023": 1479.2, "FY2022": 1282.9, "FY2021": 900.1}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 2830.8, "FY2024": 2037.8, "FY2023": 1452.0, "FY2022": 1479.2, "FY2021": 1282.9}),
]

bw.add_cash_flow_sheet(
    title="Charter Court Financial Services Limited — Statement of Cash Flows",
    subtitle="Entity (Company) basis, £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed at the Charter Court Financial Services Limited entity level in any "
    "of the 5 Annual Reports reviewed - the Directors' Report explicitly defers to \"the OSBG "
    "annual report and accounts\" for further capital/risk detail, and no standalone Pillar 3 "
    "document or KM1 template for this entity was found."
)


def metric(name, unit, rows_data, note=None, extra_source=""):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(extra_source), note=note, first_col_width=44, source_height=150)


# Sheet order matches the project-wide standard: CET1 Capital, CET1 Ratio, Tier 1
# Capital, Tier 1 Ratio, Total Capital, Total Capital Ratio, Total RWAs, Leverage
# Ratio, LCR, NSFR, MREL Ratio - even though this entity only discloses 3 of them.
bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital"], p3_sources(), per_note={"CET1 Capital": NOT_DISCLOSED_NOTE},
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio, under CRD IV", {"FY2025": "16.2%", "FY2024": "17.8%", "FY2023": "15.8%", "FY2022": "18.8%"})],
    note="FY2025/FY2024 from the Annual Report's own KPI table (FY2024 shown as that report's own "
         "comparative). FY2023 from the Strategic Report's own Solvency Risk narrative (FY2022 shown "
         "as that report's own comparative). FY2021 not located within this build's research budget - "
         "left blank rather than guessed, not confirmed absent.",
)

bw.add_not_disclosed_metric_sheets(
    ["Tier 1 Capital", "Tier 1 Ratio"], p3_sources(),
    per_note={"Tier 1 Capital": NOT_DISCLOSED_NOTE, "Tier 1 Ratio": NOT_DISCLOSED_NOTE},
)

bw.add_not_disclosed_metric_sheets(
    ["Total Capital"], p3_sources(), per_note={"Total Capital": NOT_DISCLOSED_NOTE},
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio, under CRD IV", {"FY2023": "19.2%", "FY2022": "20.2%"})],
    note=NOT_DISCLOSED_NOTE + " FY2023/FY2022 are the exception, from the Strategic Report's own "
         "Solvency Risk narrative (FY2022 shown as FY2023's report's own comparative). FY2025/FY2024/"
         "FY2021 not found - the later KPI table format only carries CET1, and FY2021 wasn't located "
         "within this build's research budget.",
)

bw.add_not_disclosed_metric_sheets(
    ["Total RWAs"], p3_sources(), per_note={"Total RWAs": NOT_DISCLOSED_NOTE},
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio, under CRD IV", {"FY2023": "6.9%", "FY2022": "7.9%"})],
    note=NOT_DISCLOSED_NOTE + " FY2023/FY2022 are the exception, from the Strategic Report's own "
         "Solvency Risk narrative (FY2022 shown as FY2023's report's own comparative). FY2025/FY2024/"
         "FY2021 not found within this build's research budget.",
)

bw.add_not_disclosed_metric_sheets(
    ["LCR", "NSFR", "MREL Ratio"], p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 717.4, "FY2024": 1335.4, "FY2023": 279.1, "FY2022": -195.1, "FY2021": 12.5}),
        ("Net cash from investing activities", {"FY2025": -219.4, "FY2024": 127.0, "FY2023": -11.0, "FY2022": 179.6, "FY2021": 81.5}),
        ("Net cash from/(used in) financing activities", {"FY2025": 295.0, "FY2024": -876.6, "FY2023": -295.3, "FY2022": 211.8, "FY2021": 288.8}),
        ("Cash and cash equivalents at end of year", {"FY2025": 2830.8, "FY2024": 2037.8, "FY2023": 1452.0, "FY2022": 1479.2, "FY2021": 1282.9}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.2%", "FY2024": "17.8%", "FY2023": "15.8%", "FY2022": "18.8%"}),
        ("Total Capital Ratio", {"FY2023": "19.2%", "FY2022": "20.2%"}),
        ("Leverage Ratio", {"FY2023": "6.9%", "FY2022": "7.9%"}),
    ],
    note="LCR/NSFR/MREL/Tier 1 metrics omitted from this chart - not disclosed at this entity level "
         "in any year (see the individual sheets). Figures are duplicated from the detail sheets for "
         "at-a-glance trend viewing; see each sheet's own source citation for the underlying "
         "document/page.",
)

bw.save("/Users/armaan/code/katalysis/banks/CHARTER COURT FINANCIAL SERVICES FINANCIALS.xlsx")
