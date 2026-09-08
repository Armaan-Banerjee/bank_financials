import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2021"]
YEAR_LABEL = {
    "FY2025": "FY2025",
    "FY2024": "FY2024",
    "FY2023": "FY2023 (15m)",
    "FY2021": "FY2021",
}

AR2025_URL = "https://streambank.co.uk/pdf/March-2025-Annual-Report-2025.pdf"
AR2024_URL = "https://streambank.co.uk/pdf/StreamBank-Plc-FY24-Live-PwC-Signed.pdf"
AR2023_URL = "https://streambank.co.uk/pdf/StreamBank-Plc-Financial-Statements-31-March-2023-Signed.pdf"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/11995458/filing-history/MzM0MzQ4NDk4M2FkaXF6a2N4/document?download=0&format=pdf"
P3_2025_URL = "https://streambank.co.uk/pdf/March-2025-Pillar-3-Disclosures.pdf"
P3_2024_URL = "https://streambank.co.uk/pdf/FY24-Pillar-3-StreamBank-PLC.pdf"

ENTITY_NOTE = (
    "ENTITY / PERIOD NOTE: StreamBank PLC (FRN 954876, Companies House no. 11995458, "
    "LEI 213800KDQFY4NBXFKP66) is the exact PRA-authorised entity covered. It was "
    "previously named Activtrades Loans PLC until 19 July 2022. The accounting period "
    "was extended from 31 December 2022 to 31 March 2023, so the FY2023 figures cover "
    "15 months (1 January 2022 to 31 March 2023); no separate FY2022 annual period is "
    "invented. StreamBank has no subsidiaries."
)

STATEMENTS_SOURCES = (
    "Sources - StreamBank PLC standalone/entity basis; all figures £'000:\n"
    f"FY2025: StreamBank Plc Annual report and financial statements 2025, p.37 (Income Statement), p.38 (Statement of Comprehensive Income), p.39 (Statement of Financial Position), p.40 (Statement of Changes in Equity) - {AR2025_URL}\n"
    f"FY2024: StreamBank Plc Annual report and financial statements 2024, p.37 (Income Statement), p.39 (Statement of Financial Position) - {AR2024_URL}\n"
    f"FY2023 (15 months) and FY2021: StreamBank Plc Annual report and accounts 2023, p.36 (Income Statement), p.37 (Statement of Other Comprehensive Income), p.38 (Statement of Financial Position), p.39 (Statement of Changes in Equity) - {AR2023_URL}\n\n"
    + ENTITY_NOTE
)

CASH_FLOW_SOURCES = (
    "Sources - StreamBank PLC standalone/entity basis; all figures £'000:\n"
    f"FY2025 and FY2024: StreamBank Plc Annual report and financial statements 2025, p.41 (cash flow statement) - {AR2025_URL}\n"
    f"FY2023 (15 months) and FY2021: StreamBank Plc Annual report and accounts 2023, p.40 (cash flow statement and 2021 comparative) - {AR2023_URL}\n"
    f"FY2021 filing copy: Companies House full accounts made up to 31 December 2021 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - StreamBank PLC standalone regulatory basis:\n"
        f"FY2025 and FY2024: StreamBank Pillar 3 Disclosures 2025, p.10 (UKB KM1 key metrics), p.28 (leverage), pp.31-32 (LCR/NSFR) - {P3_2025_URL}\n"
        f"FY2024: StreamBank Pillar 3 Disclosures 2024, p.9 (UKB KM1 key metrics), pp.23-24 (leverage), pp.26-27 (LCR/NSFR) - {P3_2024_URL}\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(
    bank_name="StreamBank PLC",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="0B4F6C",
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 38692.5, "FY2024": 32730.1}),
    ("DATA", "Cash and balances with other banks / credit institutions", {"FY2025": 7956.8, "FY2024": 8342.1, "FY2023": 14534.8, "FY2021": 100.1}),
    ("DATA", "Debt instruments at fair value through OCI", {"FY2025": 4190.0, "FY2024": 4092.2, "FY2023": 2985.5}),
    ("DATA", "Loans and advances to customers", {"FY2025": 156706.3, "FY2024": 137242.0, "FY2023": 31221.0}),
    ("DATA", "Intangible assets", {"FY2025": 139.0, "FY2024": 193.8, "FY2023": 249.8, "FY2021": 222.8}),
    ("DATA", "Property, plant & equipment", {"FY2025": 71.3, "FY2024": 76.1, "FY2023": 64.1}),
    ("DATA", "Deferred tax assets", {"FY2025": 1683.3, "FY2024": 2017.1, "FY2023": 1017.3, "FY2021": 125.0}),
    ("DATA", "Other assets", {"FY2025": 944.2, "FY2024": 557.9, "FY2023": 642.2}),
    ("TOTAL", "Total assets", {"FY2025": 210383.4, "FY2024": 185251.3, "FY2023": 50714.7, "FY2021": 447.9}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from customers", {"FY2025": 173512.6, "FY2024": 149625.7, "FY2023": 16632.2}),
    ("DATA", "Other liabilities", {"FY2025": 1661.3, "FY2024": 1398.4, "FY2023": 644.7, "FY2021": 800.5}),
    ("TOTAL", "Total liabilities", {"FY2025": 175173.9, "FY2024": 151024.1, "FY2023": 17276.9, "FY2021": 800.5}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 40600.0, "FY2024": 40600.0, "FY2023": 37500.0, "FY2021": 50.0}),
    ("DATA", "Accumulated losses", {"FY2025": -5390.5, "FY2024": -6372.8, "FY2023": -4062.2, "FY2021": -402.6}),
    ("TOTAL", "Total equity", {"FY2025": 35209.5, "FY2024": 34227.2, "FY2023": 33437.8, "FY2021": -352.6}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 210383.4, "FY2024": 185251.3, "FY2023": 50714.7, "FY2021": 447.9}),
]

bw.add_balance_sheet_sheet(
    title="StreamBank Plc — Balance Sheet",
    subtitle="Standalone entity basis, £'000; FY2023 covers the 15-month transition period ended 31 March 2023; no separate FY2022 period was published",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nPRESENTATION NOTE: FY2025/FY2024's own report labels the cash line 'Cash balances held with "
        "other banks'; FY2023/FY2021's own report labels the equivalent line 'Loans and advances to credit "
        "institutions'. Both are combined here under one label as they cover the same underlying balance "
        "(repayable-on-demand deposits with UK banks). FY2021 had not yet begun lending or taking deposits "
        "(confirmed by that year's own Balance Sheet showing no Loans and advances to customers or Deposits "
        "from customers line at all) - blank cells for FY2021 are genuinely nil, not a data gap."
    ),
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£'000)",
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2025": 19996.4, "FY2024": 8950.3, "FY2023": 2039.8}),
    ("DATA", "Interest payable and similar charges", {"FY2025": -8737.1, "FY2024": -3608.2, "FY2023": -290.0}),
    ("TOTAL", "Net interest income", {"FY2025": 11259.3, "FY2024": 5342.1, "FY2023": 1749.8}),
    ("DATA", "Other operating income/(expense)", {"FY2025": 121.3, "FY2024": -96.6, "FY2023": 99.0}),
    ("TOTAL", "Net operating income", {"FY2025": 11380.6, "FY2024": 5245.5, "FY2023": 1848.8}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -5243.6, "FY2024": -4701.2, "FY2023": -3754.5}),
    ("DATA", "Other operating expenses", {"FY2025": -3141.0, "FY2024": -2670.9, "FY2023": -1980.4, "FY2021": -527.6}),
    ("DATA", "Impairment losses on loans and advances to customers", {"FY2025": -1678.4, "FY2024": -1201.9, "FY2023": -600.8}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -100.3, "FY2024": -89.6, "FY2023": -50.4}),
    # Not itself a printed AR subtotal - the sum of Staff costs + Other
    # operating expenses + Depreciation and amortisation above. Excludes
    # Impairment losses on loans and advances per standard cost-to-income
    # convention (operating costs only, not credit risk).
    ("TOTAL", "Total operating expenses (sum of Staff costs + Other operating expenses + Depreciation and amortisation - excludes impairment losses on loans and advances)",
     {"FY2025": -8484.9, "FY2024": -7461.7, "FY2023": -5785.3, "FY2021": -527.6}),
    ("TOTAL", "Profit/(Loss) before taxation", {"FY2025": 1217.3, "FY2024": -3418.1, "FY2023": -4537.4, "FY2021": -527.6}),
    ("DATA", "Tax (charge)/credit", {"FY2025": -309.0, "FY2024": 1023.1, "FY2023": 892.3, "FY2021": 125.0}),
    ("TOTAL", "Profit/(Loss) for the year", {"FY2025": 908.3, "FY2024": -2395.0, "FY2023": -3645.1, "FY2021": -402.6}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Fair value adjustment through OCI", {"FY2025": 98.8, "FY2024": 107.7, "FY2023": -14.5}),
    ("DATA", "Deferred tax thereon", {"FY2025": -24.8, "FY2024": -23.3}),
    ("TOTAL", "Total other comprehensive income", {"FY2025": 74.0, "FY2024": 84.4, "FY2023": -14.5}),
    ("TOTAL", "Total comprehensive income/(expense) for the year", {"FY2025": 982.3, "FY2024": -2310.6, "FY2023": -3659.6, "FY2021": -402.6}),
]

bw.add_income_statement_sheet(
    title="StreamBank Plc — Profit & Loss",
    subtitle="Standalone entity basis, £'000; FY2023 covers the 15-month transition period ended 31 March 2023; results relate entirely to continuing operations",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nFY2021 predates the start of lending/deposit-taking operations - no interest income/expense, "
        "impairment, or OCI was disclosed for that year (confirmed by that year's own Income Statement and "
        "Statement of Other Comprehensive Income, both showing '-' for those lines); FY2021's sole cost was "
        "Other Operating expenses."
    ),
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological) - built using the per-year
# reconciliation ladder: Balance Sheet built first (above), then each
# year's closing balance checked against both the next year's own opening
# balance and that year's own Balance Sheet Total equity. Ties exactly at
# every boundary - zero plug rows needed.
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "As at 1 January 2021", (50.0, 0.0, 50.0)),
    ("DATA", "Loss for the financial year (FY2021)", (None, -527.6, -527.6)),
    ("DATA", "Other comprehensive income (FY2021)", (None, 125.0, 125.0)),
    ("TOTAL", "As at 31 December 2021", (50.0, -402.6, -352.6)),
    ("DATA", "Loss for the financial period (FY2023, 15mo)", (None, -3645.1, -3645.1)),
    ("DATA", "Fair value adjustment through OCI (FY2023)", (None, -14.5, -14.5)),
    ("DATA", "Increase in share capital (FY2023)", (37450.0, None, 37450.0)),
    ("TOTAL", "As at 31 March 2023", (37500.0, -4062.2, 33437.8)),
    ("DATA", "Loss for the financial year (FY2024)", (None, -2395.0, -2395.0)),
    ("DATA", "Other comprehensive income (FY2024)", (None, 84.4, 84.4)),
    ("DATA", "Increase in share capital (FY2024)", (3100.0, None, 3100.0)),
    ("TOTAL", "As at 31 March 2024", (40600.0, -6372.8, 34227.2)),
    ("DATA", "Profit for the financial year (FY2025)", (None, 908.3, 908.3)),
    ("DATA", "Other comprehensive income (FY2025)", (None, 74.0, 74.0)),
    ("DATA", "Increase in share capital (FY2025)", (0.0, None, 0.0)),
    ("TOTAL", "As at 31 March 2025", (40600.0, -5390.5, 35209.5)),
]

bw.add_equity_changes_sheet(
    title="StreamBank Plc — Statement of Changes in Equity",
    subtitle="Standalone entity basis, £'000; FY2023 row covers the 15-month transition period ended 31 "
              "March 2023. Ties exactly to the Balance Sheet's own Total equity at every year-end - no plug "
              "rows needed.",
    headers=["Called up share capital", "Accumulated losses", "Total"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nSOURCE ANOMALY, reproduced as disclosed, not silently corrected: the FY2021 row of StreamBank's "
        "own Statement of Changes in Equity (AR2023, p.39) labels a +£125.0k movement 'Other comprehensive "
        "income', but that figure exactly matches the FY2021 tax credit reported in the Income Statement "
        "(p.36), while the same year's own Statement of Other Comprehensive Income (p.37) shows nil OCI for "
        "FY2021. The 'Loss for the financial year' row used here (£527.6k) is therefore the FY2021 loss "
        "before tax, not the £402.6k loss after tax - the two figures net to the correct £402.6k movement "
        "and tie exactly to the Balance Sheet's own FY2021 Total equity, so the underlying numbers are not "
        "in question, only the source's own row labelling for that one year."
    ),
    first_col_width=76,
    source_height=260,
)

cash_flow_rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Cash generated from operations", {"FY2025": 5616.8, "FY2024": 24482.0, "FY2023": 9419.8, "FY2021": 272.8}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": 5616.8, "FY2024": 24482.0, "FY2023": 9419.8, "FY2021": 272.8}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of debt instruments", {"FY2024": -1000.0, "FY2023": -3000.0}),
    ("DATA", "Disposal of debt instruments", {"FY2025": 1.0, "FY2024": 1.0}),
    ("DATA", "Additions of intangible fixed assets", {"FY2025": -1.2}),
    ("DATA", "Purchase of intangible fixed assets", {"FY2023": -57.0, "FY2021": -222.7}),
    ("DATA", "Additions of tangible fixed assets", {"FY2025": -39.5, "FY2024": -45.6, "FY2023": -84.6}),
    ("DATA", "Purchase of loans and advances to customers", {"FY2023": -8343.5}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": -39.7, "FY2024": -1044.6, "FY2023": -11485.1, "FY2021": -222.7}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Share issuance", {"FY2024": 3100.0, "FY2023": 16500.0, "FY2021": 37.5}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": 0.0, "FY2024": 3100.0, "FY2023": 16500.0, "FY2021": 37.5}),
    ("TOTAL", "Net movement in cash and cash equivalents", {"FY2025": 5577.1, "FY2024": 26537.4, "FY2023": 14434.7, "FY2021": 87.6}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 41072.2, "FY2024": 14534.8, "FY2023": 100.1, "FY2021": 12.5}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 46649.3, "FY2024": 41072.2, "FY2023": 14534.8, "FY2021": 100.1}),
]

bw.add_cash_flow_sheet(
    title="StreamBank PLC — Statement of Cash Flows",
    subtitle="Standalone entity basis, £'000; FY2023 covers the 15-month transition period ended 31 March 2023; no separate FY2022 period was published",
    rows=cash_flow_rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=220,
    unit_suffix=" (£'000)",
)


asset_quality_rows = [
    ("SECTION", "Loan book", {}),
    ("DATA", "Gross loans and advances to customers", {"FY2025": 160288.5, "FY2024": 139145.8, "FY2023": 31821.8}),
    ("DATA", "Less: ECL allowance", {"FY2025": -3582.2, "FY2024": -1903.8, "FY2023": -600.8}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 156706.3, "FY2024": 137242.0, "FY2023": 31221.0}),
    ("SECTION", "ECL allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 307.0, "FY2024": 233.0, "FY2023": 47.7}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 107.0, "FY2024": 3.6, "FY2023": 0.6}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 3168.2, "FY2024": 1667.2, "FY2023": 552.5}),
    ("SECTION", "Derived ratio", {}),
    ("DATA", "ECL coverage ratio (total ECL / gross loans)", {"FY2025": "2.24%", "FY2024": "1.37%", "FY2023": "1.89%"}),
]

bw.add_asset_quality_sheet(
    title="StreamBank Plc — Asset Quality / Credit Risk Disclosures",
    subtitle="Standalone entity basis, £'000; FY2023 covers the 15-month transition period ended 31 March "
              "2023. FY2021 predates the start of lending - genuinely nil, not a data gap.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - StreamBank PLC standalone/entity basis, all figures £'000:\n"
        f"FY2025 and FY2024: StreamBank Plc Annual report and financial statements 2025, p.53-54 (Note 12 "
        f"Loans and advances to customers, Note 13 Impairment losses by IFRS 9 stage) - {AR2025_URL}\n"
        f"FY2023: StreamBank Plc Annual report and accounts 2023, p.51-52 (Note 11 Loans and advances to "
        f"customers, Note 12 Impairment losses by IFRS 9 stage) - {AR2023_URL}\n\n"
        + ENTITY_NOTE
        + "\n\nFY2021 had no loans and advances to customers at all (confirmed by that year's own Balance "
          "Sheet and Note 11 comparative column, both showing '-') - the Bank had not yet begun lending. "
          "No gross-balance-by-stage split is disclosed in either source, only the ECL allowance roll-forward "
          "by stage; the ECL coverage ratio is calculated as total ECL allowance divided by gross loans, not "
          "a Stage-3-specific NPL ratio, since Stage 3 gross exposure isn't separately disclosed."
    ),
    first_col_width=64,
    source_height=220,
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=180)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {"FY2025": 35066.3, "FY2024": 32012.2})], "Not publicly disclosed for FY2023 (15m) and FY2021 in the sources reviewed.")
metric("CET1 Ratio", "%", [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "24.8%", "FY2024": "22.2%"})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {"FY2025": 35066.3, "FY2024": 32012.2})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
metric("Tier 1 Ratio", "%", [("Tier 1 capital ratio", {"FY2025": "24.8%", "FY2024": "22.2%"})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
metric("Total Capital", "£'000", [("Total capital", {"FY2025": 35066.3, "FY2024": 32012.2})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
metric("Total Capital Ratio", "%", [("Total capital ratio", {"FY2025": "24.8%", "FY2024": "22.2%"})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
metric("Total RWAs", "£'000", [("Risk-weighted exposure amounts", {"FY2025": 141336.1, "FY2024": 143947.0})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
rwa_breakdown_rows = [
    ("SECTION", "Risk-weighted exposure amounts (UK OV1)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 123094.2, "FY2024": 126646.0}),
    ("DATA", "Operational risk", {"FY2025": 18241.9, "FY2024": 17301.0}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 141336.1, "FY2024": 143947.0}),
]

bw.add_rwa_breakdown_sheet(
    title="StreamBank Plc — RWA Breakdown",
    subtitle="Standalone regulatory basis, £'000; not publicly disclosed for FY2023 (15m) and FY2021 - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\n\nStreamBank's Pillar 3 Disclosures document is only published from FY2024 onward; no standalone "
        "Pillar 3 report covering the FY2023 (15-month) or FY2021 periods was found on the Bank's own site "
        "or via Wayback Machine - a genuine access/non-existence gap, consistent with the pre-existing "
        "Total RWAs and capital ratio sheets, which mark those two periods 'Not publicly disclosed'."
    ),
    first_col_width=54,
    source_height=200,
)

metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", {"FY2025": "20.4%", "FY2024": "21.0%"})], "The Pillar 3 document also reports ratios including central-bank claims of 16.6% (FY2025) and 17.3% (FY2024); this workbook uses the headline ratio excluding those claims. Earlier periods were not disclosed.")
metric("LCR", "%", [("Liquidity Coverage Ratio", {"FY2025": "9081.1%", "FY2024": "54235.0%"})], "Not publicly disclosed for FY2023 (15m) and FY2021. The source rounds the FY2025 table presentation to 9,081% in one location and reports 9,081.1% in UKB KM1; the latter is retained here.")
metric("NSFR", "%", [("Net Stable Funding Ratio", {"FY2025": "171.6%", "FY2024": "223.8%"})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No quantitative MREL ratio was found in the annual reports or Pillar 3 disclosures reviewed. StreamBank states it is assigned to the Modified Insolvency resolution category.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 210383.4, "FY2024": 185251.3, "FY2023": 50714.7, "FY2021": 447.9}),
        ("Loans and advances to customers", {"FY2025": 156706.3, "FY2024": 137242.0, "FY2023": 31221.0}),
        ("Deposits from customers", {"FY2025": 173512.6, "FY2024": 149625.7, "FY2023": 16632.2}),
        ("Total equity", {"FY2025": 35209.5, "FY2024": 34227.2, "FY2023": 33437.8, "FY2021": -352.6}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 11259.3, "FY2024": 5342.1, "FY2023": 1749.8}),
        ("Total operating expense", {"FY2025": -10163.3, "FY2024": -8663.6, "FY2023": -6386.1, "FY2021": -527.6}),
        ("Profit/(Loss) for the year", {"FY2025": 908.3, "FY2024": -2395.0, "FY2023": -3645.1, "FY2021": -402.6}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 34227.2, "FY2024": 33437.8, "FY2023": -352.6, "FY2021": 50.0}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 982.3, "FY2024": -2310.6, "FY2023": -3659.6, "FY2021": -402.6}),
        ("Other equity movements, net", {"FY2025": 0.0, "FY2024": 3100.0, "FY2023": 37450.0, "FY2021": 0.0}),
        ("Closing equity", {"FY2025": 35209.5, "FY2024": 34227.2, "FY2023": 33437.8, "FY2021": -352.6}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": 5616.8, "FY2024": 24482.0, "FY2023": 9419.8, "FY2021": 272.8}),
        ("Net cash from investing activities", {"FY2025": -39.7, "FY2024": -1044.6, "FY2023": -11485.1, "FY2021": -222.7}),
        ("Net cash from financing activities", {"FY2025": 0.0, "FY2024": 3100.0, "FY2023": 16500.0, "FY2021": 37.5}),
        ("Cash and cash equivalents at end of year", {"FY2025": 46649.3, "FY2024": 41072.2, "FY2023": 14534.8, "FY2021": 100.1}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "24.8%", "FY2024": "22.2%"}),
        ("Tier 1 Ratio", {"FY2025": "24.8%", "FY2024": "22.2%"}),
        ("Total Capital Ratio", {"FY2025": "24.8%", "FY2024": "22.2%"}),
        ("Leverage Ratio", {"FY2025": "20.4%", "FY2024": "21.0%"}),
        ("LCR", {"FY2025": "9081.1%", "FY2024": "54235.0%"}),
        ("NSFR", {"FY2025": "171.6%", "FY2024": "223.8%"}),
    ],
    note="Coverage is FY2021, FY2023 (15-month transition period), FY2024 and FY2025. FY2022 is intentionally absent because the accounting period was extended to 31 March 2023. Blank metric cells mean not publicly disclosed, not zero. Sources are entity-level; wider group data was not substituted.",
)

bw.save("/Users/armaan/code/katalysis/banks/STREAMBANK FINANCIALS.xlsx")
