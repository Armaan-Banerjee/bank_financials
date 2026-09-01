import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR2025_URL = "https://www.oxbury.com/media/e3xppqoe/2025-company-accounts.pdf"
AR2024_URL = "https://www.oxbury.com/media/03rk55or/oxbury-2024-accounts-1pg.pdf"
AR2023_URL = "https://www.oxbury.com/media/dxeb3xqx/oxbury-bank-annual-accounts-31122023.pdf"
AR2022_URL = "https://www.oxbury.com/media/brmf2riv/annual-report-2022.pdf"
AR2021_URL = "https://www.oxbury.com/media/g5xibgrw/annual-report-2021.pdf"
P3_2023_URL = "https://www.oxbury.com/media/xttezclr/oxbury-bank-plc-pillar-3-2023-final.pdf"

ENTITY_NOTE = (
    "ENTITY / BASIS NOTE: Oxbury Bank Plc (FRN 834822; Companies House no. 11383418) is the PRA-authorised "
    "bank and the entity covered by this workbook. The annual reports present both Group and Company columns. "
    "This workbook uses the Company/entity-level cash-flow figures throughout. The Group includes Oxbury Bank Plc "
    "and its wholly owned subsidiary Oxbury Earth Ltd (and, from FY2025, Oxbury Earth LLC); Group figures are not "
    "substituted for the Bank's own figures. The FY2025 report describes a new wider holding structure, but the "
    "legal bank entity remains Oxbury Bank Plc."
)

CASH_FLOW_SOURCES = (
    "Sources - Oxbury Bank Plc Company/entity basis; all figures £'000:\n"
    f"FY2025 and restated FY2024: Oxbury Bank Plc Annual Report and Accounts 2025, pp.40-41, Company columns - {AR2025_URL}\n"
    f"FY2023: Oxbury Bank Plc Annual Report and Accounts 2024, pp.40-41, Company columns - {AR2024_URL}\n"
    f"FY2022: Oxbury Bank Plc Annual Report and Accounts 2023, pp.40-41, Company columns; the report marks the affected comparative figures with an asterisk and explains the restatement in Note 31 - {AR2023_URL}\n"
    f"FY2021: Oxbury Bank Plc Annual Report and Accounts 2022, p.39, Company columns - {AR2022_URL}\n"
    f"The FY2021 source report also reproduces the FY2021 statement in the 2021 Annual Report, p.35 - {AR2021_URL}\n\n"
    "The FY2025 financing subtotal is £1k above the sum of the displayed rounded component lines; the explicit "
    "£1k rounding adjustment preserves the report's stated subtotal.\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Oxbury Bank Plc regulatory/entity basis:\n"
        f"FY2023 and FY2022: Oxbury Bank Plc Pillar 3 Disclosures December 2023, pp.11-12 (capital resources, "
        f"RWA, capital ratios), pp.17-18 (leverage), pp.36-40 (LCR and NSFR) - {P3_2023_URL}\n"
        f"FY2025 and FY2024: Oxbury Bank Plc Annual Report and Accounts 2025, p.6 (Company Key Performance "
        f"Indicators, unaudited capital/liquidity measures) - {AR2025_URL}\n"
        f"FY2021: Oxbury Bank Plc Annual Report and Accounts 2021, p.6 (Company Key Performance Indicators, "
        f"unaudited CET1/Total Capital, leverage and LCR measures) - {AR2021_URL}\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(
    bank_name="Oxbury Bank Plc",
    years=YEARS,
    header_color="2F5597",
)

cash_flow_rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit and adjustments before net changes in operating assets and liabilities", {"FY2025": -26222, "FY2024": -17894, "FY2023": -12067, "FY2022": -9138, "FY2021": -6468}),
    ("DATA", "Net changes in operating assets and liabilities (aggregate of source line items)", {"FY2025": 280132, "FY2024": 898886, "FY2023": 382363, "FY2022": 73038, "FY2021": 27493}),
    ("TOTAL", "Cash flows generated from/(used in) operating activities", {"FY2025": 253910, "FY2024": 880992, "FY2023": 370296, "FY2022": 63900, "FY2021": 21025}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of tangible assets", {"FY2025": -72, "FY2024": -119, "FY2023": -188, "FY2022": -72, "FY2021": -64}),
    ("DATA", "Disposal/(purchase) of gilts", {"FY2021": 50}),
    ("DATA", "Investment in subsidiary", {"FY2022": -2466}),
    ("DATA", "Addition in intangible assets and trademarks", {"FY2025": -1911, "FY2024": -1643, "FY2023": -2281, "FY2022": -1638, "FY2021": -1524}),
    ("DATA", "Purchase of investment securities", {"FY2025": -820188}),
    ("DATA", "Sale of investment securities", {"FY2025": 447232}),
    ("TOTAL", "Net cash flows used in investing activities", {"FY2025": -374939, "FY2024": -1762, "FY2023": -2469, "FY2022": -4176, "FY2021": -1538}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of share capital", {"FY2025": 43129, "FY2024": 68951, "FY2023": 24262, "FY2022": 28167, "FY2021": 12019}),
    ("DATA", "Costs directly related to issue of share capital", {"FY2025": -282, "FY2024": -275, "FY2023": -226, "FY2022": -153, "FY2021": -70}),
    ("DATA", "Increase in subordinated debt", {"FY2025": 16250, "FY2024": 2500, "FY2023": 7500, "FY2022": 7500, "FY2021": 0}),
    ("DATA", "Interest paid on subordinated debt", {"FY2025": -2301, "FY2024": -1873, "FY2023": -1151, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Interest paid on lease payments", {"FY2025": -55, "FY2024": -71, "FY2023": -43, "FY2022": -37, "FY2021": 0}),
    ("DATA", "Payments in relation to leases", {"FY2025": -252, "FY2024": -109, "FY2023": -148, "FY2022": -115, "FY2021": -93}),
    ("DATA", "Rounding adjustment to FY2025 reported financing subtotal", {"FY2025": 1}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": 56490, "FY2024": 69123, "FY2023": 30194, "FY2022": 35362, "FY2021": 11856}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents in the year", {"FY2025": -64539, "FY2024": 948353, "FY2023": 398021, "FY2022": 95086, "FY2021": 31343}),
    ("DATA", "Cash and cash equivalents at start of year", {"FY2025": 1492018, "FY2024": 543665, "FY2023": 145644, "FY2022": 50558, "FY2021": 19215}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 1427479, "FY2024": 1492018, "FY2023": 543665, "FY2022": 145644, "FY2021": 50558}),
]

bw.add_cash_flow_sheet(
    title="Oxbury Bank Plc — Statement of Cash Flows",
    subtitle="Company/entity-level basis, £'000; FY2024 is the restated comparative presented in the FY2025 report",
    rows=cash_flow_rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=220,
    unit_suffix=" (£'000)",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=180)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {"FY2023": 68026, "FY2022": 45557})], "Not publicly disclosed for FY2025, FY2024 and FY2021 in the sources reviewed; FY2023 and FY2022 are from the dedicated Pillar 3 capital-resources table.")
metric("CET1 Ratio", "%", [("Common Equity Tier 1 (CET1) ratio", {"FY2023": "15.94%", "FY2022": "16.16%", "FY2021": "23%"})], "FY2021 is reported as ‘CET1 / Total Capital Ratio’ in the annual-report KPI table; FY2024-FY2025 CET1-specific ratios were not disclosed in the sources reviewed.")
metric("Tier 1 Capital", "£'000", [("Total Tier 1 capital", {"FY2023": 68026, "FY2022": 45557})], "Not publicly disclosed for FY2025, FY2024 and FY2021 in the sources reviewed.")
metric("Tier 1 Ratio", "%", [("Tier 1 capital ratio", {"FY2023": "15.94%", "FY2022": "16.16%", "FY2021": "23%"})], "FY2021 annual-report KPI is labelled CET1 / Total Capital Ratio and is used as the only disclosed capital-ratio measure for that year.")
metric("Total Capital", "£'000", [("Total regulatory capital", {"FY2023": 82214, "FY2022": 53057})], "Not publicly disclosed for FY2025, FY2024 and FY2021 in the sources reviewed.")
metric("Total Capital Ratio", "%", [("Total capital ratio", {"FY2025": "18.8%", "FY2024": "22.5%", "FY2023": "19.27%", "FY2022": "18.81%", "FY2021": "23%"})], "FY2025 and FY2024 are the annual-report Company Key Performance Indicators; FY2023-FY2022 are dedicated Pillar 3 ratios; FY2021 annual-report KPI is labelled CET1 / Total Capital Ratio.")
metric("Total RWAs", "£'000", [("Total risk-weighted assets", {"FY2023": 426705, "FY2022": 282001})], "Not publicly disclosed for FY2025, FY2024 and FY2021 in the sources reviewed.")
metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", {"FY2025": "9.2%", "FY2024": "12.7%", "FY2023": "10.69%", "FY2022": "12.17%", "FY2021": "15%"})], "FY2025-FY2024 are annual-report KPI measures; FY2023-FY2022 are Pillar 3 ratios excluding claims on central banks; FY2021 is the annual-report KPI.")
metric("LCR", "%", [("Liquidity Coverage Ratio", {"FY2025": "296%", "FY2024": "460%", "FY2023": "545.2%", "FY2022": "2,132%", "FY2021": "1,090%"})], "FY2025-FY2024 are annual-report KPI measures; FY2023-FY2022 are the Pillar 3 LCR ratios (the annual report also shows a year-end 614%/2,819% measure on a different basis); FY2021 is the annual-report KPI.")
metric("NSFR", "%", [("Net Stable Funding Ratio", {"FY2023": "201.1%", "FY2022": "149.1%"})], "Not publicly disclosed for FY2025, FY2024 and FY2021 in the sources reviewed.")
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No quantitative MREL ratio was found in the annual reports or the dedicated FY2023 Pillar 3 disclosure reviewed.")

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 253910, "FY2024": 880992, "FY2023": 370296, "FY2022": 63900, "FY2021": 21025}),
        ("Net cash used in investing activities", {"FY2025": -374939, "FY2024": -1762, "FY2023": -2469, "FY2022": -4176, "FY2021": -1538}),
        ("Net cash from financing activities", {"FY2025": 56490, "FY2024": 69123, "FY2023": 30194, "FY2022": 35362, "FY2021": 11856}),
        ("Cash and cash equivalents at end of year", {"FY2025": 1427479, "FY2024": 1492018, "FY2023": 543665, "FY2022": 145644, "FY2021": 50558}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2023": "15.94%", "FY2022": "16.16%", "FY2021": "23%"}),
        ("Tier 1 Ratio", {"FY2023": "15.94%", "FY2022": "16.16%", "FY2021": "23%"}),
        ("Total Capital Ratio", {"FY2025": "18.8%", "FY2024": "22.5%", "FY2023": "19.27%", "FY2022": "18.81%", "FY2021": "23%"}),
        ("Leverage Ratio", {"FY2025": "9.2%", "FY2024": "12.7%", "FY2023": "10.69%", "FY2022": "12.17%", "FY2021": "15%"}),
        ("LCR", {"FY2025": "296%", "FY2024": "460%", "FY2023": "545.2%", "FY2022": "2,132%", "FY2021": "1,090%"}),
        ("NSFR", {"FY2023": "201.1%", "FY2022": "149.1%"}),
    ],
    note="Five latest financial years are covered (FY2021-FY2025). Cash flows use Oxbury Bank Plc Company columns. Dedicated Pillar 3 quantitative disclosures were located for FY2022-FY2023; FY2024-FY2025 capital/liquidity KPI ratios come from the annual reports, and FY2021 KPI ratios from the FY2021 annual report. Blank cells represent metrics not disclosed for that year, not zero.",
)

bw.save("/Users/armaan/code/katalysis/banks/OXBURY FINANCIALS.xlsx")
