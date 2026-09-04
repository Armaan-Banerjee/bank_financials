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


BALANCE_SHEET_SOURCES = (
    "Sources - Afin Bank Limited audited annual report and financial statements for the year ended 31 December 2024:\n"
    f"FY2024: Statement of financial position, printed p. 34 - {AR_2024_URL}\n"
    + ENTITY_NOTE
    + "\nPRESENTATION NOTE: The source statement also shows FY2023 comparatives on its face, but this workbook is "
    "intentionally FY2024-only for consistency with the Cash Flow Statement and Pillar 3 sheets, whose primary "
    "source (the 2024 Pillar 3 report) explicitly states no prior-period comparatives are provided."
)

INCOME_STATEMENT_SOURCES = (
    "Sources - Afin Bank Limited audited annual report and financial statements for the year ended 31 December 2024:\n"
    f"FY2024: Statement of comprehensive income, printed p. 33 - {AR_2024_URL}\n"
    + ENTITY_NOTE
    + "\nPRESENTATION NOTE: The source statement also shows FY2023 comparatives on its face, but this workbook is "
    "intentionally FY2024-only for consistency with the Cash Flow Statement and Pillar 3 sheets."
)

EQUITY_CHANGES_SOURCES = (
    "Sources - Afin Bank Limited audited annual report and financial statements for the year ended 31 December 2024:\n"
    f"Statement of changes in equity, printed p. 35, covering 1 January 2023 to 31 December 2024 - {AR_2024_URL}\n"
    + ENTITY_NOTE
    + "\nThis is the one sheet in the workbook that includes FY2023 movements, since the equity roll-forward is "
    "chronological (not year-columned) and both years' movements are disclosed on the statement's face."
)

ASSET_QUALITY_SOURCES = (
    "Sources - Afin Bank Limited 2024 Annual Report and Pillar 3 Disclosures:\n"
    f"{AR_2024_URL}\n{P3_2024_URL}\n" + ENTITY_NOTE
    + "\nNOT DISCLOSED: Afin Bank's balance sheet has no lending product line (assets are Cash, Treasury assets, "
    "Receivables, Prepayments, PP&E and intangibles only) and neither the 2024 Annual Report nor the 2024 Pillar 3 "
    "disclosure (a small non-complex institution under CRR Article 433b) contains a loan book / IFRS 9 stage / "
    "credit risk exposure breakdown."
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Afin Bank Limited standalone Pillar 3 Disclosures for the year ended 31 December 2024:\n"
    f"UK KM1 Key Metrics, printed pp. 4-5 - {P3_2024_URL}\n" + ENTITY_NOTE
    + "\nNOT DISCLOSED: as a small non-complex institution under CRR Article 433b, Afin Bank's 2024 Pillar 3 "
    "disclosure contains only the single aggregate Total RWA figure in UK KM1 (see the Total RWAs sheet) - no "
    "UK OV1 exposure-class breakdown is published."
)

bw.add_balance_sheet_sheet(
    title="Afin Bank Limited — Consolidated Statement of Financial Position",
    subtitle="Afin Bank Limited audited statement of financial position; amounts in £.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and cash equivalents", {"FY2024": 3155921}),
        ("DATA", "Treasury assets", {"FY2024": 9767797}),
        ("DATA", "Receivables", {"FY2024": 450628}),
        ("DATA", "Prepayments", {"FY2024": 372022}),
        ("DATA", "Property, plant and equipment", {"FY2024": 57172}),
        ("DATA", "Right-of-use assets", {"FY2024": 967204}),
        ("DATA", "Intangible assets", {"FY2024": 2657199}),
        ("TOTAL", "Total assets", {"FY2024": 17427943}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Trade and other payables", {"FY2024": 1102894}),
        ("DATA", "Lease liabilities", {"FY2024": 965184}),
        ("TOTAL", "Total liabilities", {"FY2024": 2068078}),
        ("TOTAL", "Net assets", {"FY2024": 15359865}),
        ("SECTION", "Equity", {}),
        ("DATA", "Called up share capital", {"FY2024": 23614036}),
        ("DATA", "Revaluation reserve", {"FY2024": 67382}),
        ("DATA", "Share based payment reserve", {"FY2024": 267626}),
        ("DATA", "Retained earnings", {"FY2024": -8589179}),
        ("TOTAL", "Total equity", {"FY2024": 15359865}),
    ],
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=48,
    source_height=150,
    unit_suffix=" (£)",
)

bw.add_income_statement_sheet(
    title="Afin Bank Limited — Consolidated Statement of Comprehensive Income",
    subtitle="Afin Bank Limited audited statement of comprehensive income; amounts in £.",
    rows=[
        ("SECTION", "Operating expenses", {}),
        ("DATA", "Staff costs", {"FY2024": -3941455}),
        ("DATA", "Depreciation", {"FY2024": -142504}),
        ("DATA", "Amortisation of intangibles", {"FY2024": -23179}),
        ("DATA", "Other operating costs", {"FY2024": -2149595}),
        ("TOTAL", "Total operating expenses", {"FY2024": -6256733}),
        ("TOTAL", "Operating loss", {"FY2024": -6256733}),
        ("DATA", "Finance income", {"FY2024": 75152}),
        ("DATA", "Finance costs", {"FY2024": -11970}),
        ("TOTAL", "Loss before taxation", {"FY2024": -6193551}),
        ("DATA", "Income tax expense", {"FY2024": 0}),
        ("TOTAL", "Loss for the year", {"FY2024": -6193551}),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Treasury asset revaluation", {"FY2024": 67382}),
        ("TOTAL", "Total other comprehensive income for the year", {"FY2024": 67382}),
        ("TOTAL", "Total comprehensive income for the year", {"FY2024": -6126169}),
    ],
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=48,
    source_height=150,
    unit_suffix=" (£)",
)

EQUITY_HEADERS = ["Share capital", "Revaluation reserve", "Share based payment", "Retained earnings", "Total equity"]
bw.add_equity_changes_sheet(
    title="Afin Bank Limited — Statement of Changes in Equity",
    subtitle="Afin Bank Limited audited statement of changes in equity, 1 January 2023 to 31 December 2024; amounts in £.",
    headers=EQUITY_HEADERS,
    rows=[
        ("TOTAL", "Balance at 1 January 2023", (590654, None, None, -626440, -35786)),
        ("DATA", "Total comprehensive income for the year (2023)", (None, None, None, -1769188, -1769188)),
        ("DATA", "Issue of share capital (2023)", (2767153, None, None, None, 2767153)),
        ("TOTAL", "Balance at 31 December 2023", (3357807, 0, 0, -2395628, 962179)),
        ("DATA", "Loss for the year (2024)", (None, None, None, -6193551, -6193551)),
        ("DATA", "Other comprehensive income - Treasury asset revaluation (2024)", (None, 67382, None, None, 67382)),
        ("TOTAL", "Total comprehensive income for the year (2024)", (None, 67382, None, -6193551, -6126169)),
        ("DATA", "Issue of share capital (2024)", (20256229, None, None, None, 20256229)),
        ("DATA", "Share based payment (2024)", (None, None, 267626, None, 267626)),
        ("TOTAL", "Balance at 31 December 2024", (23614036, 67382, 267626, -8589179, 15359865)),
    ],
    sources_text=EQUITY_CHANGES_SOURCES,
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


bw.add_asset_quality_sheet(
    title="Afin Bank Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Afin Bank Limited loan book / credit risk disclosures; amounts in £.",
    rows=[
        ("DATA", "Not publicly disclosed", {"FY2024": "Not publicly disclosed"}),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=58,
    source_height=150,
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
bw.add_rwa_breakdown_sheet(
    title="Afin Bank Limited — RWA Breakdown",
    subtitle="Afin Bank Limited risk-weighted exposure amount breakdown; amounts in £'000.",
    rows=[
        ("DATA", "Not publicly disclosed", {"FY2024": "Not publicly disclosed"}),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=150,
    unit_suffix=" (£'000)",
)
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
    balance_sheet_totals=[
        ("Total assets", {"FY2024": 17427943}),
        ("Trade and other payables", {"FY2024": 1102894}),
        ("Total equity", {"FY2024": 15359865}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Total operating expenses", {"FY2024": -6256733}),
        ("Loss for the year", {"FY2024": -6193551}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {"FY2024": 962179}),
        ("Total comprehensive income", {"FY2024": -6126169}),
        ("Other movements, net", {"FY2024": 20523855}),
        ("Closing equity", {"FY2024": 15359865}),
    ],
    equity_changes_unit="£",
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
        "audited annual accounts. See each detail sheet for the source citation. Asset Quality and RWA Breakdown "
        "are marked not publicly disclosed: Afin has no lending product on its balance sheet yet and, as a small "
        "non-complex institution, its Pillar 3 report has no exposure-class RWA table."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/AFIN BANK FINANCIALS.xlsx")
