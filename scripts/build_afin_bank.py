import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# SHORT-PERIOD PILLAR-3-ONLY WORKBOOK: Afin Bank Limited's first official
# Pillar 3 disclosure is for 31 December 2024. The report explicitly says
# that prior-period comparatives are not provided, so this workbook uses a
# single FY2024 column rather than inventing a longer history.
YEARS = ["FY2024"]
YEAR_LABEL = {y: y for y in YEARS}

AR_2024_URL = "https://afinbank.com/wp-content/uploads/2025/09/Afin-Bank-Ltd-Year-End-Accounts-FV24-FINAL-SIGNED.pdf"
P3_2024_URL = "https://afinbank.com/wp-content/uploads/2025/09/Afin-Bank-2024-Pillar-3-Disclosures-FINAL.pdf"
CH_OVERVIEW_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556"
CH_FILING_HISTORY_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556/filing-history"
CH_2024_ACCOUNTS_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556/filing-history/MzQ4MjgwOTc2M2FkaXF6a2N4/document?download=0&format=pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Afin Bank Limited (company 13090556, FRN 1004742) is the UK legal entity covered here. "
    "The 2024 Pillar 3 report says the disclosure scope applies to Afin Bank Limited only; it is a majority-owned "
    "subsidiary of WAICA Reinsurance Corporation PLC, but no parent-level figures are substituted. The company was "
    "formerly named All Africa Capital Limited and changed its name after receiving banking authorisation with "
    "restrictions in October 2024."
)

CASH_FLOW_SOURCES = (
    "Sources - Afin Bank Limited audited annual report and financial statements for the year ended 31 December 2024:\n"
    f"FY2024: Statement of cash flows, printed p. 36 - {AR_2024_URL}\n"
    f"Companies House 2024 accounts filing (filed 29 September 2025) - {CH_2024_ACCOUNTS_URL}\n"
    f"Companies House filing history - {CH_FILING_HISTORY_URL}\n"
    + ENTITY_NOTE
)

P3_SOURCES = (
    "Sources - Afin Bank Limited standalone Pillar 3 Disclosures for the year ended 31 December 2024:\n"
    f"FY2024: UK KM1 Key Metrics, printed pp. 4-5, and UK OV1, printed p. 5 - {P3_2024_URL}\n"
    "Afin Bank annual reports and disclosures page - https://afinbank.com/about/annual-reports-and-disclosures/\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(
    bank_name="Afin Bank Limited",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="4A1E4D",
)


bw.add_cash_flow_sheet(
    title="Afin Bank Limited — Cash Flow Statement",
    subtitle="Afin Bank Limited audited standalone statement of cash flows; amounts in £.",
    rows=[
        ("SECTION", "Cash flows from operating activities", {}),
        ("DATA", "Cash absorbed by operations", {"FY2024": -5854403}),
        ("TOTAL", "Net cash outflow from operating activities", {"FY2024": -5854403}),
        ("SECTION", "Investing activities", {}),
        ("DATA", "Purchase of intangible assets", {"FY2024": -2668378}),
        ("DATA", "Purchase of property, plant and equipment", {"FY2024": -52008}),
        ("DATA", "Purchase of investments", {"FY2024": -9700415}),
        ("DATA", "Finance income", {"FY2024": 75152}),
        ("TOTAL", "Net cash used in investing activities", {"FY2024": -12345649}),
        ("SECTION", "Financing activities", {}),
        ("DATA", "Proceeds from issue of shares", {"FY2024": 20523855}),
        ("DATA", "Payment of lease liabilities", {"FY2024": -134783}),
        ("DATA", "Finance cost", {"FY2024": -4777}),
        ("TOTAL", "Net cash generated from financing activities", {"FY2024": 20384295}),
        ("TOTAL", "Net increase in cash and cash equivalents", {"FY2024": 2184243}),
        ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2024": 971678}),
        ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2024": 3155921}),
    ],
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=62,
    source_height=165,
    unit_suffix=" (£)",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        P3_SOURCES,
        note=note,
        first_col_width=56,
        source_height=145,
    )


metric("CET1 Capital", "£'000", [
    ("Common Equity Tier 1 (CET1) capital", {"FY2024": 12922}),
])
metric("CET1 Ratio", "% of RWA", [
    ("Common Equity Tier 1 (CET1) ratio", {"FY2024": "418.5%"}),
])
metric("Tier 1 Capital", "£'000", [
    ("Tier 1 capital", {"FY2024": 12922}),
])
metric("Tier 1 Ratio", "% of RWA", [
    ("Tier 1 ratio", {"FY2024": "418.5%"}),
])
metric("Total Capital", "£'000", [
    ("Total capital", {"FY2024": 12922}),
])
metric("Total Capital Ratio", "% of RWA", [
    ("Total capital ratio", {"FY2024": "418.5%"}),
])
metric("Total RWAs", "£'000", [
    ("Total risk-weighted exposure amount", {"FY2024": 3087}),
])
metric("Leverage Ratio", "£'000 / %", [
    ("Total exposure measure excluding claims on central banks", {"FY2024": 14782}),
    ("Leverage ratio excluding claims on central banks", {"FY2024": "87.4%"}),
])
metric("LCR", "£'000 / %", [
    ("Total high-quality liquid assets (HQLA) (weighted value - average)", {"FY2024": 8909}),
    ("Cash outflows - total weighted value", {"FY2024": 0}),
    ("Cash inflows - total weighted value", {"FY2024": 3971}),
    ("Total net cash outflows (adjusted value)", {"FY2024": 0}),
    ("Liquidity coverage ratio", {"FY2024": "999999%"}),
], note=(
    "Afin states that it had no qualifying cash outflows at 31 December 2024; the source therefore reports the "
    "LCR as 999999%. This is reproduced as reported and is not interpreted as a conventional finite ratio."
))
metric("NSFR", "£'000 / %", [
    ("Total available stable funding", {"FY2024": 21486}),
    ("Total required stable funding", {"FY2024": 4365}),
    ("NSFR ratio", {"FY2024": "492.2%"}),
])
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    P3_SOURCES,
    per_note={
        "MREL Ratio": "No numeric MREL ratio is disclosed in the 2024 Pillar 3 report or the audited annual accounts."
    },
)


bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash outflow from operating activities", {"FY2024": -5854403}),
        ("Net cash used in investing activities", {"FY2024": -12345649}),
        ("Net cash generated from financing activities", {"FY2024": 20384295}),
        ("Cash and cash equivalents at end of year", {"FY2024": 3155921}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2024": "418.5%"}),
        ("Tier 1 Ratio", {"FY2024": "418.5%"}),
        ("Total Capital Ratio", {"FY2024": "418.5%"}),
        ("Leverage Ratio", {"FY2024": "87.4%"}),
        ("LCR", {"FY2024": "999999%"}),
        ("NSFR", {"FY2024": "492.2%"}),
    ],
    note=(
        "SHORT PERIOD: This workbook intentionally covers FY2024 only. Afin's first Pillar 3 report states that it "
        "was authorised as a bank with restrictions in October 2024 and does not provide prior-period comparatives. "
        "The Pillar 3 metrics are standalone Afin Bank Limited disclosures; the cash-flow statement is from the "
        "audited annual accounts. See each detail sheet for the source citation."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/AFIN BANK FINANCIALS.xlsx")
