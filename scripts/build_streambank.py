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


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=180)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {"FY2025": 35066.3, "FY2024": 32012.2})], "Not publicly disclosed for FY2023 (15m) and FY2021 in the sources reviewed.")
metric("CET1 Ratio", "%", [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "24.8%", "FY2024": "22.2%"})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {"FY2025": 35066.3, "FY2024": 32012.2})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
metric("Tier 1 Ratio", "%", [("Tier 1 capital ratio", {"FY2025": "24.8%", "FY2024": "22.2%"})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
metric("Total Capital", "£'000", [("Total capital", {"FY2025": 35066.3, "FY2024": 32012.2})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
metric("Total Capital Ratio", "%", [("Total capital ratio", {"FY2025": "24.8%", "FY2024": "22.2%"})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
metric("Total RWAs", "£'000", [("Risk-weighted exposure amounts", {"FY2025": 141336.1, "FY2024": 143947.0})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", {"FY2025": "20.4%", "FY2024": "21.0%"})], "The Pillar 3 document also reports ratios including central-bank claims of 16.6% (FY2025) and 17.3% (FY2024); this workbook uses the headline ratio excluding those claims. Earlier periods were not disclosed.")
metric("LCR", "%", [("Liquidity Coverage Ratio", {"FY2025": "9081.1%", "FY2024": "54235.0%"})], "Not publicly disclosed for FY2023 (15m) and FY2021. The source rounds the FY2025 table presentation to 9,081% in one location and reports 9,081.1% in UKB KM1; the latter is retained here.")
metric("NSFR", "%", [("Net Stable Funding Ratio", {"FY2025": "171.6%", "FY2024": "223.8%"})], "Not publicly disclosed for FY2023 (15m) and FY2021.")
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No quantitative MREL ratio was found in the annual reports or Pillar 3 disclosures reviewed. StreamBank states it is assigned to the Modified Insolvency resolution category.")

bw.add_overview_sheet(
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
