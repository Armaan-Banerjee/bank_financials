import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: Julian Hodge Bank Limited (company 00743437, FRN 204439)
# takes the FRS 101 cash-flow-statement disclosure exemption in every one of its FY2021-FY2025
# Annual Reports - explicitly stated each year in Note 1 (Basis of preparation): "the Bank has
# applied the exemptions available under FRS 101 in respect of the following disclosures: A Cash
# Flow Statement and related notes; ..." No Statement of Cash Flows exists in any year's accounts.
# Pillar 3 / capital disclosures are rich for FY2021-FY2023 (full UK KM1-format Key Regulatory
# Metrics tables, standalone Pillar 3 documents), but FY2024-FY2025 have no standalone Pillar 3
# document published - only a brief unaudited "Capital risk management" note inside each year's
# own Annual Report giving CET1/RWA/ratios (no Leverage/LCR/NSFR for those two years). Follows the
# BNY Mellon International / ABC International Bank precedent: standard 13-sheet structure, but
# the Cash Flow Statement sheet documents the exemption instead of line items, and the Overview
# sheet omits the cash-flow chart.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, fiscal year-end 30 September
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://hodgebank.co.uk/wp-content/uploads/2026/02/Hodge-AR-28.01.26.pdf"
AR2024_URL = "https://hodgebank.co.uk/wp-content/uploads/2025/02/Hodge-annual-report-21.02.25.pdf"
AR2023_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Annual-report-Jan-25.01.24.pdf"
AR2022_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-Annual-Report-April-04.04.23-optimised.pdf"
AR2021_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-Annual-Report-2020_2021.pdf"
P3_2023_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-pillar-3-11.03.24.pdf"
P3_2022_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-pillar-3-19.06.23.pdf"
P3_2021_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-Pillar-3-Document-2020_2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Julian Hodge Bank Limited (company 00743437, FRN 204439, incorporated 1962) is a "
    "privately-owned Cardiff-based bank; immediate parent Hodge Limited, ultimate parent The Carlyle Trust "
    "(Jersey) Limited. Fiscal year-end is 30 September. All 5 years text-native PDFs, no OCR required."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: every Annual Report FY2021-FY2025 states in Note 1 (Basis of preparation) that "
    "the Bank \"has applied the exemptions available under FRS 101 in respect of the following disclosures: A Cash "
    "Flow Statement and related notes; ...\" - e.g. Julian Hodge Bank Limited Annual Report 2025, Note 1.1, p.42 - "
    f"{AR2025_URL}. No Statement of Cash Flows exists in any of the entity's published accounts for any year in "
    "this window - a standing structural feature, not a one-off or data gap. Per the project's established policy "
    "for this exemption (see The Bank of New York Mellon (International) Limited / ABC International Bank plc), "
    "this workbook is built as a PILLAR-3-ONLY variant: all 11 Pillar 3 metric sheets are populated below, but no "
    "cash flow figures exist to show. See the Overview sheet for the equivalent treatment there."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

BASIS_NOTE = (
    "FY2021-FY2023: full UK KM1-format 'Key Regulatory Metrics' table from each year's own standalone Pillar 3 "
    "Disclosures document. FY2024-FY2025: no standalone Pillar 3 document was located on the bank's site (financial "
    "information page lists a Pillar 3 disclosure link for FY2018-FY2023 only) - CET1/RWA/ratio figures instead "
    "come from each year's own Annual Report 'Capital risk management (unaudited)' note, which does not include "
    "Leverage Ratio, LCR, or NSFR - those 3 metrics are genuinely unavailable for FY2024/FY2025 this session, not "
    "assumed absent."
)


def p3_sources(extra=""):
    return (
        "Sources - Julian Hodge Bank Limited:\n"
        f"FY2023: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2023, Table \"3 Key Regulatory "
        f"Metrics\", p.9 - {P3_2023_URL}\n"
        f"FY2022: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2022, Table \"3 Key Regulatory "
        f"Metrics\", p.12 - {P3_2022_URL}\n"
        f"FY2021: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2021, Table \"Key Metrics\", p.16 - "
        f"{P3_2021_URL}\n"
        f"FY2024: Julian Hodge Bank Limited Annual Report 2024, Note 32 'Capital risk management (unaudited)', "
        f"p.73 - {AR2024_URL}\n"
        f"FY2025: Julian Hodge Bank Limited Annual Report 2025, Note 34 'Capital risk management (unaudited)', "
        f"p.76 - {AR2025_URL}\n"
        + (extra + "\n" if extra else "") + BASIS_NOTE
    )


bw = BankWorkbook(bank_name="Julian Hodge Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="8B4513")

STATEMENTS_SOURCES = (
    "Sources - Julian Hodge Bank Limited Annual Reports:\n"
    f"FY2025: Annual Report 2025, Balance Sheet/Income Statement/Statement of Changes in Equity, p.40-41, "
    f"Note 12 'Loans and advances to customers'/Note 13 'Impairment provisions', p.49-50 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, Balance Sheet/Income Statement/Statement of Changes in Equity, p.40-42, "
    f"Note 12/13, p.48-49 - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, Balance Sheet/Income Statement/Statement of Changes in Equity, p.40-42, "
    f"Note 13/14, p.49-50 - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, Balance Sheet/Income Statement/Statement of Changes in Equity, p.37-39, "
    f"Note 13/14, p.46-47 - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, Balance Sheet/Income Statement/Statement of Other Comprehensive Income/"
    f"Statement of Changes in Equity, p.62-65 (printed pages 67-70) - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances held at central banks", {"FY2025": 69.5, "FY2024": 151.3, "FY2023": 93.7, "FY2022": 118.1, "FY2021": 412.2}),
    ("DATA", "Loans and advances to credit institutions", {"FY2025": 7.9, "FY2024": 4.5, "FY2023": 11.2, "FY2022": 0.2, "FY2021": 45.9}),
    ("DATA", "Derivative financial instruments (asset)", {"FY2025": 16.8, "FY2024": 27.9, "FY2023": 58.5, "FY2022": 75.8}),
    ("DATA", "Government bonds", {"FY2025": 27.9, "FY2024": 27.7, "FY2023": 61.7, "FY2022": 111.2, "FY2021": 29.8}),
    ("DATA", "Debt securities", {"FY2025": 135.8, "FY2024": 70.7, "FY2023": 82.0, "FY2022": 116.2, "FY2021": 42.3}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1839.7, "FY2024": 1699.3, "FY2023": 1488.5, "FY2022": 1404.6, "FY2021": 1061.5}),
    ("DATA", "Intangible assets", {"FY2025": 14.5, "FY2024": 15.1, "FY2023": 12.7, "FY2022": 9.7, "FY2021": 7.4}),
    ("DATA", "Property and equipment", {"FY2025": 0.6, "FY2024": 1.0, "FY2023": 1.2, "FY2022": 1.5, "FY2021": 1.6}),
    ("DATA", "Investment properties", {"FY2025": 0.2, "FY2024": 1.5, "FY2023": 2.6, "FY2022": 9.2, "FY2021": 94.6}),
    ("DATA", "Deferred tax assets", {"FY2025": 2.2, "FY2024": 3.7, "FY2023": 5.6, "FY2022": 6.3, "FY2021": 11.5}),
    ("DATA", "Other assets", {"FY2025": 6.6, "FY2024": 5.9, "FY2023": 5.4, "FY2022": 8.0, "FY2021": 6.6}),
    ("DATA", "Pension asset", {"FY2025": 0.9, "FY2024": 0.2}),
    ("TOTAL", "Total assets", {"FY2025": 2122.6, "FY2024": 2008.8, "FY2023": 1823.1, "FY2022": 1860.8, "FY2021": 1713.4}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 67.0, "FY2024": 167.7, "FY2023": 240.7, "FY2022": 221.0, "FY2021": 145.0}),
    ("DATA", "Deposits from customers", {"FY2025": 1860.3, "FY2024": 1639.4, "FY2023": 1368.1, "FY2022": 1425.0, "FY2021": 1381.0}),
    ("DATA", "Derivative financial instruments (liability)", {"FY2025": 5.1, "FY2024": 5.6, "FY2023": 9.7, "FY2022": 11.4, "FY2021": 14.7}),
    ("DATA", "Other liabilities", {"FY2025": 10.4, "FY2024": 12.9, "FY2023": 16.5, "FY2022": 13.9, "FY2021": 9.9}),
    ("DATA", "Pension liabilities", {"FY2023": 4.3, "FY2022": 4.5, "FY2021": 14.2}),
    ("TOTAL", "Total liabilities", {"FY2025": 1942.8, "FY2024": 1825.6, "FY2023": 1639.3, "FY2022": 1675.8, "FY2021": 1564.8}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 130.0, "FY2024": 130.0, "FY2023": 130.0, "FY2022": 130.0, "FY2021": 105.0}),
    ("DATA", "Other reserves (retained earnings + pension reserve)", {"FY2025": 49.8, "FY2024": 53.2, "FY2023": 53.8, "FY2022": 55.0, "FY2021": 43.6}),
    ("TOTAL", "Total equity", {"FY2025": 179.8, "FY2024": 183.2, "FY2023": 183.8, "FY2022": 185.0, "FY2021": 148.6}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 2122.6, "FY2024": 2008.8, "FY2023": 1823.1, "FY2022": 1860.8, "FY2021": 1713.4}),
]

bw.add_balance_sheet_sheet(
    title="Julian Hodge Bank Limited — Balance Sheet",
    subtitle="Entity-level (Company-only, FRS 101). £m.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest revenue calculated using the EIR method", {"FY2025": 122.9, "FY2024": 92.1, "FY2023": 67.3, "FY2022": 50.5, "FY2021": 39.6}),
    ("DATA", "Interest expense calculated using the EIR method", {"FY2025": -81.1, "FY2024": -52.4, "FY2023": -27.9, "FY2022": -21.1, "FY2021": -22.0}),
    ("TOTAL", "Net interest income", {"FY2025": 41.8, "FY2024": 39.7, "FY2023": 39.4, "FY2022": 29.4, "FY2021": 17.6}),
    ("DATA", "Fees and commission income", {"FY2025": 1.0, "FY2024": 2.9, "FY2023": 2.5, "FY2022": 2.6, "FY2021": 2.5}),
    ("DATA", "Fees and commission expense", {"FY2025": -3.6, "FY2024": -1.2, "FY2023": -0.1, "FY2022": -0.1}),
    ("TOTAL", "Net fee and commission income/(expense)", {"FY2025": -2.6, "FY2024": 1.7, "FY2023": 2.4, "FY2022": 2.5, "FY2021": 2.5}),
    ("DATA", "Investment income", {"FY2025": 0.6, "FY2024": 0.5, "FY2023": 4.6, "FY2022": 6.7, "FY2021": 6.0}),
    ("DATA", "Other operating income", {"FY2023": 0.2, "FY2021": 0.1}),
    ("DATA", "Bad debt recovery", {"FY2022": 0.4}),
    ("TOTAL", "Net operating income", {"FY2025": 39.8, "FY2024": 41.9, "FY2023": 46.6, "FY2022": 38.6, "FY2021": 26.2}),
    ("DATA", "Administrative expenses", {"FY2025": -33.7, "FY2024": -36.4, "FY2023": -35.3, "FY2022": -34.2, "FY2021": -25.9}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -3.1, "FY2024": -2.9, "FY2023": -2.9, "FY2022": -2.5, "FY2021": -2.4}),
    ("DATA", "Impairment (losses)/gains on loans and advances to customers", {"FY2025": -6.5, "FY2024": -2.2, "FY2023": -1.6}),
    ("TOTAL", "Operating profit/(loss) (FY2021-FY2024 subtotal; see Net operating (loss)/income for FY2025's own equivalent line)",
     {"FY2024": 0.4, "FY2023": 6.8, "FY2022": 2.3, "FY2021": -2.1}),
    ("TOTAL", "Net operating (loss)/income (FY2025's own subtotal, structured differently from FY2021-FY2024's 'Operating profit')",
     {"FY2025": -3.5}),
    ("DATA", "(Loss)/gain arising from the derecognition of financial assets managed at amortised cost", {"FY2024": -1.0, "FY2021": 0.0}),
    ("DATA", "Other fair value gains/(losses)", {"FY2025": -2.3, "FY2024": -1.5, "FY2023": -7.0, "FY2022": 4.3, "FY2021": 11.3}),
    ("DATA", "Loss on disposal of loans and advances to customers held at fair value", {"FY2021": -5.5}),
    ("TOTAL", "Profit/(loss) before taxation", {"FY2025": -5.8, "FY2024": -2.1, "FY2023": -0.2, "FY2022": 6.6, "FY2021": 3.7}),
    ("DATA", "Tax credit/(charge) on profit/(loss) before taxation", {"FY2025": 1.9, "FY2024": 0.4, "FY2022": -1.8, "FY2021": 2.1}),
    ("TOTAL", "Profit/(loss) for the financial year", {"FY2025": -3.9, "FY2024": -1.7, "FY2023": -0.2, "FY2022": 4.8, "FY2021": 5.8}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Re-measurement of defined benefit pension plan", {"FY2025": 0.7, "FY2024": 1.7, "FY2023": -1.7, "FY2022": 9.0, "FY2021": 2.6}),
    ("DATA", "Deferred tax on pension plan re-measurement", {"FY2025": -0.2, "FY2024": -0.4, "FY2023": 0.4, "FY2022": -2.2, "FY2021": -0.4}),
    ("DATA", "Movement of pension scheme reimbursement asset/(liability)", {"FY2024": -0.3, "FY2023": 0.4, "FY2022": -0.2, "FY2021": -1.0}),
    ("DATA", "Deferred tax on pension reimbursement movement", {"FY2024": 0.1, "FY2023": -0.1, "FY2021": 0.6}),
    ("TOTAL", "Total other comprehensive income/(loss)", {"FY2025": 0.5, "FY2024": 1.1, "FY2023": -1.0, "FY2022": 6.6, "FY2021": 1.8}),
    ("TOTAL", "Total comprehensive (loss)/income for the year", {"FY2025": -3.4, "FY2024": -0.6, "FY2023": -1.2, "FY2022": 11.4, "FY2021": 7.6}),
]

bw.add_income_statement_sheet(
    title="Julian Hodge Bank Limited — Profit & Loss",
    subtitle="Entity-level (Company-only, FRS 101). £m. Structure genuinely changes FY2025 (Net operating (loss)/income "
              "subtotal replaces the FY2021-FY2024 'Operating profit' subtotal) - both shown on their own basis, not forced "
              "into one template. Each year's own originally-published figures used throughout; note AR2025's own FY2024 "
              "comparative column is separately labelled 'Restated' (Note 33 interest revenue/expense reclassification) - "
              "that restated column is NOT used here, FY2024's own contemporaneous report is used instead, per project convention.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=90,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder confirmed:
# every year's own closing balance ties exactly to both the next year's own
# opening balance and that year's own Balance Sheet Total equity. Zero plug
# rows needed anywhere across all 5 years.
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Retained earnings", "Pension reserve", "Total"]
equity_rows = [
    ("TOTAL", "Opening balance at 1 October 2020 (FY2021 opening)", (105.0, 50.4, -14.4, 141.0)),
    ("DATA", "Profit for the financial year", (None, 5.5, 0.3, 5.8)),
    ("DATA", "Other comprehensive income", (None, None, 1.8, 1.8)),
    ("TOTAL", "At 30 September 2021 (FY2021 closing)", (105.0, 54.3, -10.7, 148.6)),
    ("DATA", "Issue of share capital", (25.0, None, None, 25.0)),
    ("DATA", "Profit for the financial year", (None, 5.2, -0.4, 4.8)),
    ("DATA", "Other comprehensive income", (None, None, 6.6, 6.6)),
    ("DATA", "Pension additional contribution", (None, -1.2, 1.2, None)),
    ("TOTAL", "At 30 September 2022 (FY2022 closing)", (130.0, 58.3, -3.3, 185.0)),
    ("DATA", "Loss for the financial year", (None, 0.1, -0.3, -0.2)),
    ("DATA", "Other comprehensive loss", (None, None, -1.0, -1.0)),
    ("DATA", "Pension additional contribution", (None, -1.8, 1.8, None)),
    ("TOTAL", "At 30 September 2023 (FY2023 closing)", (130.0, 56.6, -2.8, 183.8)),
    ("DATA", "Loss for the financial year", (None, -1.5, -0.2, -1.7)),
    ("DATA", "Other comprehensive income", (None, None, 1.1, 1.1)),
    ("DATA", "Pension additional contribution", (None, -3.0, 3.0, None)),
    ("TOTAL", "At 30 September 2024 (FY2024 closing)", (130.0, 52.1, 1.1, 183.2)),
    ("DATA", "Loss for the financial year", (None, -3.9, None, -3.9)),
    ("DATA", "Other comprehensive income", (None, None, 0.5, 0.5)),
    ("TOTAL", "At 30 September 2025 (FY2025 closing)", (130.0, 48.2, 1.6, 179.8)),
]

bw.add_equity_changes_sheet(
    title="Julian Hodge Bank Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest. Equity reconciliation ladder confirmed: every year's own "
              "closing balance ties exactly to both the next year's own opening balance and that year's own Balance Sheet "
              "Total equity - zero plug rows needed anywhere across all 5 years. £m.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

# ---------------------------------------------------------------
# Asset Quality - Note 12/13's own IFRS 9 Stage 1/2/3/PMA provision
# roll-forward (portfolio-wide, all loans and advances to customers at
# amortised cost combined - no gross-exposure-by-stage table exists at
# portfolio level, only per-product segment tables for Commercial/PBTL/
# Motor separately, which don't sum to the full book since Retail's own
# stage split isn't separately disclosed).
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers at amortised cost", {}),
    ("DATA", "Gross balances", {"FY2025": 1811.1, "FY2024": 1671.4, "FY2023": 1483.1, "FY2022": 1403.6, "FY2021": 989.9}),
    ("DATA", "Net loan fee deferral", {"FY2025": 13.0, "FY2024": 8.5, "FY2023": 2.9, "FY2022": 3.7, "FY2021": 1.9}),
    ("DATA", "Provision for impairment", {"FY2025": -13.8, "FY2024": -7.7, "FY2023": -6.0, "FY2022": -8.6, "FY2021": -8.4}),
    ("TOTAL", "Net balance (amortised cost)", {"FY2025": 1810.3, "FY2024": 1672.2, "FY2023": 1480.0, "FY2022": 1398.7, "FY2021": 983.4}),
    ("DATA", "Impairment provision coverage (%)", {
        "FY2025": "0.76%", "FY2024": "0.46%", "FY2023": "0.40%", "FY2022": "0.61%", "FY2021": "0.85%",
    }),
    ("SECTION", "Impairment provision, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 3.6, "FY2024": 2.4, "FY2023": 1.3, "FY2022": 1.7, "FY2021": 1.3}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 1.7, "FY2024": 1.2, "FY2023": 3.1, "FY2022": 1.3, "FY2021": 2.0}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 8.3, "FY2024": 4.2, "FY2023": 1.2, "FY2022": 4.8, "FY2021": 5.1}),
    ("DATA", "Post Model Adjustment", {"FY2025": 0.2, "FY2024": -0.1, "FY2023": 0.4, "FY2022": 0.8}),
    ("TOTAL", "Total provision for impairment", {"FY2025": 13.8, "FY2024": 7.7, "FY2023": 6.0, "FY2022": 8.6, "FY2021": 8.4}),
    ("SECTION", "Loans and advances by product, at amortised cost (before hedge FV adjustment / retirement mortgages FVTPL)", {}),
    ("DATA", "Retail", {"FY2025": 1371.8, "FY2024": 1315.9, "FY2023": 1234.9, "FY2022": 1140.0, "FY2021": 679.0}),
    ("DATA", "Commercial (real estate)", {"FY2025": 218.1, "FY2024": 189.7, "FY2023": 170.4, "FY2022": 182.2, "FY2021": 233.9}),
    ("DATA", "Portfolio Buy-to-Let", {"FY2025": 37.3, "FY2024": 70.3, "FY2023": 74.7, "FY2022": 76.5, "FY2021": 70.5}),
    ("DATA", "Motor receivables", {"FY2025": 183.1, "FY2024": 96.3}),
    ("DATA", "Amounts owed from parent and fellow subsidiaries", {"FY2021": 0.4}),
]

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="Julian Hodge Bank Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=260,
    unit_suffix="",
)

bw.add_asset_quality_sheet(
    title="Julian Hodge Bank Limited — Asset Quality",
    subtitle="Portfolio-wide IFRS 9 Stage 1/2/3 impairment provision roll-forward (Note 13/14). £m.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nDATA QUALITY FLAG: AR2025's own Note 13 table prints its 2025-year closing row as \"At 30 September 2024\" "
        "and its 2024-year closing row as \"At 30 September 2023\" - both appear to be an off-by-one-year label carried "
        "over from an earlier template (each closing row's own figures follow arithmetically from that block's own "
        "opening row and match the FOLLOWING year's contemporaneous report exactly), so the closing rows are treated "
        "here as FY2025 and FY2024 respectively, not as literally labelled. No gross-exposure-by-IFRS-9-stage table "
        "exists at portfolio level in any year - only the impairment PROVISION is broken out by stage portfolio-wide; "
        "gross exposure by stage is only disclosed for the Commercial/PBTL/Motor segments separately (not for Retail, "
        "the largest segment), so a full gross-by-stage table is not reconstructable without assuming Retail's split."
    ),
    first_col_width=76,
    source_height=380,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 162.8, "FY2024": 166.2, "FY2023": 172.9, "FY2022": 177, "FY2021": 143.8})],
    p3_sources(),
    note="FY2021's own report (P3 2021) shows CET1 = 143.8; the following year's Pillar 3 document (P3 2022) "
         "restates the FY2021 comparative to 144 (rounding to whole £m from that document's own precision) - "
         "each year's own originally-published figure is used per this project's convention.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 162.8, "FY2024": 166.2, "FY2023": 172.9, "FY2022": 177, "FY2021": 143.8})],
    p3_sources(),
    note="Tier 1 = CET1 every year (no AT1 instruments in issue - 'Hold all its capital in the form of Common "
         "Equity Tier 1 and Tier 2 capital', and Tier 2 = nil every year per the Pillar 3 documents). FY2024/FY2025 "
         "not separately labelled 'Tier 1' in the Annual Report's brief capital note but equal to CET1 by the same "
         "pattern confirmed directly in FY2021-FY2023.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%"})],
    p3_sources(),
    note="Equal to CET1 ratio every year - see Tier 1 Capital sheet note.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 162.8, "FY2024": 166.2, "FY2023": 172.9, "FY2022": 177, "FY2021": 143.8})],
    p3_sources(),
    note="Equal to CET1/Tier 1 every year - the Bank holds no Tier 2 capital in any year covered.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets / exposure amount", {"FY2025": 930.2, "FY2024": 841.1, "FY2023": 704.7, "FY2022": 705, "FY2021": 711.0})],
    p3_sources(),
    note="FY2021's own report (P3 2021) shows RWA = 711.0; the FY2022 Pillar 3 document's FY2021 comparative "
         "restates this to 711 (rounding only, immaterial) - each year's own originally-published figure is used.",
)

# ---------------------------------------------------------------
# RWA Breakdown - FY2023/FY2022/FY2021 sourced from each year's own
# standalone Pillar 3 document's "Risk Type Breakdown" (UK OV1-style)
# table; FY2025/FY2024 have no standalone Pillar 3 document (see
# BASIS_NOTE) so no category-level split exists, only the aggregate
# Total RWAs figure already shown on that sheet.
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2023": 629.2, "FY2022": 644, "FY2021": 639.9}),
    ("DATA", "Counterparty credit risk (CCR) - includes CVA memo below for FY2023/FY2022 (this year's own template "
             "shows CVA as a memo item within CCR, not a separately additive line); FY2021's own template shows CVA "
             "as its own separately additive line instead (see next row)",
     {"FY2023": 2.7, "FY2022": 1, "FY2021": 4.6}),
    ("DATA", "Of which: Credit valuation adjustment (CVA) - memo only for FY2023/FY2022, already included in CCR above, not separately additive",
     {"FY2023": 0.2, "FY2022": 0}),
    ("DATA", "Credit valuation adjustment (CVA) - shown as its own separately additive risk type in FY2021's own Pillar 3 template only",
     {"FY2021": 0.8}),
    ("DATA", "Operational risk", {"FY2023": 58.9, "FY2022": 44, "FY2021": 36.5}),
    ("DATA", "Amounts below the threshold for deduction (250% risk weight)", {"FY2023": 13.9, "FY2022": 16, "FY2021": 29.2}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2023": 704.7, "FY2022": 705, "FY2021": 711.0}),
]

bw.add_rwa_breakdown_sheet(
    title="Julian Hodge Bank Limited — RWA Breakdown",
    subtitle="FY2023-FY2021 only (see source note - no standalone Pillar 3 document exists for FY2025/FY2024). £m.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(
        "\nFY2025/FY2024: Not publicly disclosed at category level - no standalone Pillar 3 document is published for "
        "these years (see BASIS_NOTE above); only the aggregate Total RWAs figure exists, already shown on the Total "
        "RWAs sheet, sourced from each year's own Annual Report 'Capital risk management' note instead."
    ),
    first_col_width=90,
    source_height=280,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total Basel III/leverage ratio exposure measure (£m)", {"FY2023": 1649.9, "FY2022": 1624, "FY2021": 1732.2}),
        ("Leverage Ratio (%)", {"FY2023": "10.5%", "FY2022": "10.9%", "FY2021": "8.3%"}),
    ],
    p3_sources(),
    note="FY2024/FY2025 not available - no standalone Pillar 3 document exists for those years and the Annual "
         "Report's brief 'Capital risk management' note does not include a leverage ratio. DATA QUALITY FLAG: the "
         "FY2022 Pillar 3 document's own FY2021 comparative column shows a materially different leverage exposure "
         "(£1,320m) and ratio (10.9%) than FY2021's own contemporaneous report (£1,732.2m / 8.3%) - a genuine "
         "cross-vintage restatement in the bank's own documents, not a transcription error. Per this project's "
         "convention, each year's own originally-published figure is used (FY2021 = 8.3%, not the later-restated "
         "10.9%) - worth double-checking if this workbook is relied on for leverage-ratio trend analysis.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total HQLA after haircuts (£m)", {"FY2023": 230.4, "FY2022": 334, "FY2021": 479.5}),
        ("Total net cash outflow, adjusted value (£m)", {"FY2023": 130.2, "FY2022": 133, "FY2021": 137.1}),
        ("Liquidity Coverage Ratio (%)", {"FY2023": "176.9%", "FY2022": "252%", "FY2021": "349.6%"}),
    ],
    p3_sources(),
    note="FY2024/FY2025 not available - see Leverage Ratio sheet note. Year-end (point-in-time) values shown, "
         "per each source document's own basis ('year end value for LCR related metrics').",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2023": 1721.9, "FY2022": 1549, "FY2021": 1551.0}),
        ("Total required stable funding (£m)", {"FY2023": 1144.2, "FY2022": 1085, "FY2021": 922.7}),
        ("Net Stable Funding Ratio (%)", {"FY2023": "150.5%", "FY2022": "143%", "FY2021": "168.1%"}),
    ],
    p3_sources(),
    note="FY2024/FY2025 not available - see Leverage Ratio sheet note.",
)

metric(
    "MREL Ratio", "£m / %",
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL figure (numeric or qualitative) appears in any of the 3 standalone Pillar 3 documents reviewed, "
         "nor in either Annual Report's brief capital note - no reason is stated. Consistent with this small "
         "private bank not being set an independent MREL requirement by the Bank of England, the same pattern "
         "seen at other small UK banks in this project (e.g. Cynergy Bank, DF Capital Bank).",
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 2122.6, "FY2024": 2008.8, "FY2023": 1823.1, "FY2022": 1860.8, "FY2021": 1713.4}),
        ("Loans and advances to customers", {"FY2025": 1839.7, "FY2024": 1699.3, "FY2023": 1488.5, "FY2022": 1404.6, "FY2021": 1061.5}),
        ("Deposits from customers", {"FY2025": 1860.3, "FY2024": 1639.4, "FY2023": 1368.1, "FY2022": 1425.0, "FY2021": 1381.0}),
        ("Total equity", {"FY2025": 179.8, "FY2024": 183.2, "FY2023": 183.8, "FY2022": 185.0, "FY2021": 148.6}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 41.8, "FY2024": 39.7, "FY2023": 39.4, "FY2022": 29.4, "FY2021": 17.6}),
        ("Net operating income", {"FY2025": 39.8, "FY2024": 41.9, "FY2023": 46.6, "FY2022": 38.6, "FY2021": 26.2}),
        ("Profit/(loss) for the financial year", {"FY2025": -3.9, "FY2024": -1.7, "FY2023": -0.2, "FY2022": 4.8, "FY2021": 5.8}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 183.2, "FY2024": 183.8, "FY2023": 185.0, "FY2022": 148.6, "FY2021": 141.0}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": -3.4, "FY2024": -0.6, "FY2023": -1.2, "FY2022": 11.4, "FY2021": 7.6}),
        ("Other equity movements, net", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 25.0, "FY2021": 0}),
        ("Closing equity", {"FY2025": 179.8, "FY2024": 183.2, "FY2023": 183.8, "FY2022": 185.0, "FY2021": 148.6}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%"}),
        ("Tier 1 Ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%"}),
        ("Total Capital Ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%"}),
        ("Leverage Ratio", {"FY2023": "10.5%", "FY2022": "10.9%", "FY2021": "8.3%"}),
        ("LCR", {"FY2023": "176.9%", "FY2022": "252%", "FY2021": "349.6%"}),
        ("NSFR", {"FY2023": "150.5%", "FY2022": "143%", "FY2021": "168.1%"}),
    ],
    note="This entity takes the FRS 101 cash-flow-statement exemption every year (see the Cash Flow Statement "
         "sheet), so no cash flow summary or chart is shown here - Balance Sheet/Profit & Loss/Statement of Changes "
         "in Equity summaries and the Pillar 3 Key Metrics trend chart are shown instead. Leverage/LCR/NSFR are only "
         "available FY2021-FY2023 - see each Pillar 3 sheet's own source citation for detail. The FY2022 'Other "
         "equity movements' figure (£25.0m) is a real £25.0m share capital issuance that year, not a plug.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/JULIAN HODGE BANK FINANCIALS.xlsx")
