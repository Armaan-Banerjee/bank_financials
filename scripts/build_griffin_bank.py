import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Griffin Bank Limited (FRN 970920) is a very young UK challenger bank -
# renamed from Griffin Financial Technology Limited on 12 April 2023, held
# only an Authorisation-with-Restrictions (AWR/mobilisation) banking licence
# until 29 February 2024, and changed its fiscal year-end from 30 June to
# 30 September during the process (making its first published period a
# 15-month period rather than 12). Only 3 Annual Reports have ever been
# published (periods ended 30 Sep 2023, 2024, 2025) - there is no FY2021/
# FY2022 history for this entity as a bank at all, so only 3 years are
# included here rather than padding to 5.
YEARS = ["FY2025", "FY2024", "FY2023"]  # most recent first
YEAR_LABEL = {
    "FY2025": "FY2025",
    "FY2024": "FY2024",
    "FY2023": "FY2023 (15mo)",
}

AR2023_URL = "https://cms.griffin.com/griffin-assets/Griffin_Bank_Ltd_2023_Annual_Report_and_Financial_Statements_9c92dd2876.pdf"
AR2024_URL = "https://cms.griffin.com/griffin-assets/Griffin_Bank_Ltd_Annual_Report_2024_b98c8d4c38.pdf"
AR2025_URL = "https://cms.griffin.com/griffin-assets/Griffin_Bank_Ltd_Annual_Report_2025_edeb37eca7.pdf"
P3_2023_URL = "https://cms.griffin.com/griffin-assets/Griffin_Bank_Ltd_Pillar_3_30_Sept_2023_df3ca44acc.pdf"

ENTITY_NOTE = (
    "Griffin Bank Limited (Companies House 10842931) was renamed from Griffin Financial Technology "
    "Limited on 12 April 2023 and held only an Authorisation-with-Restrictions (mobilisation) banking "
    "licence until it obtained a full unrestricted licence on 29 February 2024. During the mobilisation "
    "period the Company also changed its financial year-end from 30 June to 30 September, so its first "
    "published period (FY2023) is a 15-month period from 1 July 2022 to 30 September 2023, not a "
    "standard 12-month year - both figures are as originally reported, not annualised. FY2023's cash "
    "flow statement is itself labelled 'Unaudited' in the source Annual Report. Only 3 Annual Reports "
    "have ever been published for this entity (FY2023/FY2024/FY2025) - no FY2021/FY2022 data exists."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Griffin Bank Limited's own Statement of Cash Flows:\n"
    "FY2025: Annual Report and Financial Statements 2025, p.53-54 (Statement of cash flows) - " + AR2025_URL + "\n"
    "FY2024: Annual Report and Financial Statements 2024, p.61 (Statement of cash flows; cross-checked "
    "against its own restated comparative in the 2025 Annual Report, p.53-54 - figures match exactly, "
    "no restatement) - " + AR2024_URL + "\n"
    "FY2023 (15mo): Annual Report and Financial Statements 2023, p.47 (Statement of cash flows, "
    "unaudited, 15 months ended 30 September 2023) - " + AR2023_URL + "\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Griffin Bank Limited Pillar 3 basis:\n"
        "FY2023: 2023 Pillar 3 Report (30 September 2023), p.21 (4.1 Disclosure of key metrics - KM1) - "
        + P3_2023_URL + "\n"
        "FY2024/FY2025: no Pillar 3 disclosure document has been published for either period - only the "
        "2023 Pillar 3 Report exists on the Bank's own site (checked https://griffin.com/reports, which "
        "lists exactly 6 documents across FY2023-FY2025 and only one Pillar 3 report). Not a data-access "
        "gap - confirmed genuinely unpublished, not guessed. The Bank's own FY2023 KM1 table notes it "
        "does not provide comparative information for the prior (pre-authorisation) period either, since "
        "it was first authorised as a bank (with restrictions) only in 2023.\n"
        + ENTITY_NOTE
    )


STATEMENTS_SOURCES = (
    "Sources - all figures are Griffin Bank Limited's own primary financial statements:\n"
    "FY2025: Annual Report and Financial Statements 2025, p.51 (Statement of Financial Position), "
    "p.50 (Statement of comprehensive income), p.52 (Statement of changes in equity) - " + AR2025_URL + "\n"
    "FY2024: Annual Report and Financial Statements 2024, p.59 (Statement of financial position), "
    "p.58 (Statement of comprehensive income), p.60-61 (Statement of changes in equity) - " + AR2024_URL + "\n"
    "FY2023 (15mo, unaudited): Annual Report and Financial Statements 2023, p.45 (Statement of "
    "financial position), p.44 (Statement of comprehensive income), p.46 (Statement of changes in "
    "equity) - " + AR2023_URL + "\n"
    "All 3 documents are text-native (no scanned/image-only pages) - transcribed directly from "
    "extracted text, cross-checked against each later report's own comparative column where "
    "available (all agree exactly, no restatements found).\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(bank_name="Griffin Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="3480C7")

# ---------------------------------------------------------------
# Balance Sheet - built first per the equity reconciliation ladder, so
# each year's own Total equity figure is an independent check value for
# the Statement of Changes in Equity sheet below.
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 7326998, "FY2024": 2364540, "FY2023": 270150}),
    ("DATA", "Debt securities", {"FY2025": 106511170, "FY2024": 12709240, "FY2023": 8551308}),
    ("DATA", "Trade and other receivables", {"FY2025": 1380080, "FY2024": 1430220, "FY2023": 1085821}),
    ("DATA", "Intangible assets", {"FY2025": 4194662, "FY2024": 2073199, "FY2023": 197614}),
    ("DATA", "Property, plant and equipment", {"FY2025": 138510, "FY2024": 148461, "FY2023": 126821}),
    ("TOTAL", "Total assets", {"FY2025": 119551420, "FY2024": 18725660, "FY2023": 10231714}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2025": 101783429, "FY2024": 2070144}),
    ("DATA", "Trade and other payables", {"FY2025": 1121665, "FY2024": 1372107, "FY2023": 776298}),
    ("DATA", "Contract liabilities", {"FY2025": 138627, "FY2024": 108984, "FY2023": 115000}),
    ("DATA", "Borrowings", {"FY2025": 0, "FY2024": 0, "FY2023": 579173}),
    ("TOTAL", "Total liabilities", {"FY2025": 103043721, "FY2024": 3551235, "FY2023": 1470471}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 23, "FY2024": 16, "FY2023": 13}),
    ("DATA", "Share premium account", {"FY2025": 60901935, "FY2024": 49559702, "FY2023": 30877722}),
    ("DATA", "Employee share option reserve", {"FY2025": 3701831, "FY2024": 1653057, "FY2023": 1039179}),
    ("DATA", "Warrant reserve", {"FY2025": 101283, "FY2024": 101283, "FY2023": 101283}),
    ("DATA", "Accumulated losses", {"FY2025": -48197373, "FY2024": -36139633, "FY2023": -23256954}),
    ("TOTAL", "Total equity", {"FY2025": 16507699, "FY2024": 15174425, "FY2023": 8761243}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 119551420, "FY2024": 18725660, "FY2023": 10231714}),
]

bw.add_balance_sheet_sheet(
    title="Griffin Bank Limited — Balance Sheet",
    subtitle="Bank-only (no group); FY2023 covers a 15-month period ended 30 September 2023 and is "
              "labelled unaudited in the source. £.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nPRESENTATION NOTE: Customer deposits first appear as a Balance Sheet line in FY2024 - the Bank "
        "held no customer deposits at all as at 30 September 2023, its first full period as an authorised "
        "bank (confirmed by that year's own Balance Sheet having no such line) - genuinely nil, not a gap."
    ),
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Revenue", {}),
    ("DATA", "Net interest income", {"FY2025": 787929, "FY2024": 661153, "FY2023": 207121}),
    ("DATA", "Net fees and commissions", {"FY2025": 1137886, "FY2024": 83480, "FY2023": 84335}),
    ("TOTAL", "Total net revenue", {"FY2025": 1925815, "FY2024": 744633, "FY2023": 291456}),
    ("SECTION", "Operating costs", {}),
    ("DATA", "Administrative expenses", {"FY2025": -13467508, "FY2024": -13477876, "FY2023": -12906136}),
    ("DATA", "Other expenses", {"FY2025": -516456, "FY2024": -156686, "FY2023": -104904}),
    ("TOTAL", "Total operating costs", {"FY2025": -13983964, "FY2024": -13634562, "FY2023": -13011040}),
    ("TOTAL", "Loss before tax", {"FY2025": -12058149, "FY2024": -12889929, "FY2023": -12719584}),
    ("DATA", "Tax", {"FY2025": 0, "FY2024": 0, "FY2023": 0}),
    ("TOTAL", "Loss for the year/period after taxation", {"FY2025": -12058149, "FY2024": -12889929, "FY2023": -12719584}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other gains and losses", {"FY2025": 409, "FY2024": 7250, "FY2023": -1108}),
    ("TOTAL", "Total comprehensive income/(loss) for the year/period", {"FY2025": -12057740, "FY2024": -12882679, "FY2023": -12720692}),
]

bw.add_income_statement_sheet(
    title="Griffin Bank Limited — Profit & Loss",
    subtitle="Bank-only (no group); FY2023 covers a 15-month period ended 30 September 2023 and is "
              "labelled unaudited in the source. All results are from continuing operations. £.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nTax was £nil in all 3 periods (no tax charge or credit disclosed - confirmed by reading each "
        "year's own P&L in full)."
    ),
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological) - built using the per-year
# reconciliation ladder: Balance Sheet built first (above), then each
# year's closing balance checked against both the next year's own opening
# balance and that year's own Balance Sheet Total equity. Ties exactly at
# every boundary - zero plug rows needed.
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "Balance at 1 July 2022", (10, 20122137, None, None, -10536262, 9585885)),
    ("DATA", "Loss for the period (FY2023, 15mo)", (None, None, None, None, -12719584, -12719584)),
    ("DATA", "Other comprehensive loss for the period (FY2023)", (None, None, None, None, -1108, -1108)),
    ("DATA", "Net issue of share capital (FY2023)", (3, 10755585, None, None, None, 10755588)),
    ("DATA", "Issue of employee share options (FY2023)", (None, None, 1039179, None, None, 1039179)),
    ("DATA", "Net issue/(release) of warrants (FY2023)", (None, None, None, 101283, None, 101283)),
    ("TOTAL", "Balance at 30 September 2023", (13, 30877722, 1039179, 101283, -23256954, 8761243)),
    ("DATA", "Loss for the year (FY2024)", (None, None, None, None, -12889929, -12889929)),
    ("DATA", "Other comprehensive income for the year (FY2024)", (None, None, None, None, 7250, 7250)),
    ("DATA", "Net issue of share capital (FY2024)", (3, 18681980, None, None, None, 18681983)),
    ("DATA", "Issue of employee share options (FY2024)", (None, None, 613878, None, None, 613878)),
    ("TOTAL", "Balance at 30 September 2024", (16, 49559702, 1653057, 101283, -36139633, 15174425)),
    ("DATA", "Loss for the year (FY2025)", (None, None, None, None, -12058149, -12058149)),
    ("DATA", "Other comprehensive income for the year (FY2025)", (None, None, None, None, 409, 409)),
    ("DATA", "Net issue of share capital (FY2025)", (7, 11342233, None, None, None, 11342240)),
    ("DATA", "Issue of employee share options (FY2025)", (None, None, 2048774, None, None, 2048774)),
    ("TOTAL", "Balance at 30 September 2025", (23, 60901935, 3701831, 101283, -48197373, 16507699)),
]

bw.add_equity_changes_sheet(
    title="Griffin Bank Limited — Statement of Changes in Equity",
    subtitle="Bank-only (no group); FY2023 opening/period figures cover the 15 months ended 30 September "
              "2023 and are labelled unaudited in the source. £. Ties exactly to the Balance Sheet's own "
              "Total equity at every year-end - no plug rows needed.",
    headers=["Share capital", "Share premium account", "Employee share option reserve", "Warrant reserve", "Accumulated losses", "Total equity"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Loss for the year/period after taxation", {
        "FY2025": -12058149, "FY2024": -12889929, "FY2023": -12719584,
    }),
    ("DATA", "Finance income", {"FY2025": -787929, "FY2024": -661153, "FY2023": -207121}),
    ("DATA", "Fair value on warrants expense", {"FY2025": 0, "FY2024": 0, "FY2023": 101283}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": 89059, "FY2024": 87363, "FY2023": 82107}),
    ("DATA", "Loss on disposal of property, plant and equipment", {"FY2023": 0}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 427397, "FY2024": 69323, "FY2023": 22797}),
    ("DATA", "Share-based payment expense", {"FY2025": 2048775, "FY2024": 613878, "FY2023": 1039179}),
    ("TOTAL", "Operating cash flows before movements in working capital", {
        "FY2025": -10280847, "FY2024": -12780518, "FY2023": -11681339,
    }),
    ("DATA", "Change/(increase) in trade and other receivables", {"FY2025": 50140, "FY2024": -344399, "FY2023": -337582}),
    ("DATA", "Change/(increase) in customer deposits", {"FY2025": 99713285, "FY2024": 2070144}),
    ("DATA", "Change/(increase) in trade and other payables", {"FY2025": -250442, "FY2024": 595809, "FY2023": -160031}),
    ("DATA", "Change in contract liabilities", {"FY2025": 29643, "FY2024": -6016, "FY2023": 115000}),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2025": 89261779, "FY2024": -10464980, "FY2023": -12063952,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Interest received", {"FY2025": 2385325, "FY2024": 670900, "FY2023": 370741}),
    ("DATA", "Purchases of debt securities", {"FY2025": -297626768, "FY2024": -37188716, "FY2023": -14891308}),
    ("DATA", "Proceeds on disposal of debt securities", {"FY2025": 209748720, "FY2024": 33030785, "FY2023": 6340000}),
    ("DATA", "Purchases of Treasury bills", {"FY2025": -20713633}),
    ("DATA", "Proceeds on disposal and maturity of Treasury bills", {"FY2025": 14789751}),
    ("DATA", "Purchases of supranational bonds", {"FY2025": -3122866}),
    ("DATA", "Proceeds on disposal and maturity of supranational bonds", {"FY2025": 3122866}),
    ("DATA", "Proceeds on disposal of property, plant and equipment", {"FY2025": 5011, "FY2024": 1107}),
    ("DATA", "Purchases of property, plant and equipment", {"FY2025": -84119, "FY2024": -110110, "FY2023": -144868}),
    ("DATA", "Capitalisation of intangible assets / purchases of patents and trademarks", {
        "FY2025": -2548860, "FY2024": -1944908, "FY2023": -202536,
    }),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": -94044573, "FY2024": -5540942, "FY2023": -8527971,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Interest paid", {"FY2025": -1597396, "FY2024": -9747, "FY2023": -163620}),
    ("DATA", "Repayments of loans and borrowings", {"FY2024": -579173, "FY2023": -777435}),
    ("DATA", "Transaction costs related to issuing shares", {"FY2025": -213963, "FY2024": -454668, "FY2023": -411555}),
    ("DATA", "Proceeds on issue of shares", {"FY2025": 11556203, "FY2024": 19136651, "FY2023": 11167143}),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2025": 9744844, "FY2024": 18093063, "FY2023": 9814533,
    }),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {
        "FY2025": 4962049, "FY2024": 2087140, "FY2023": -10777390,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year/period", {
        "FY2025": 2364540, "FY2024": 270150, "FY2023": 11048648,
    }),
    ("DATA", "Effect of foreign exchange rate changes", {"FY2025": 409, "FY2024": 7250, "FY2023": -1108}),
    ("TOTAL", "Cash and cash equivalents at the end of the year/period", {
        "FY2025": 7326998, "FY2024": 2364540, "FY2023": 270150,
    }),
]

bw.add_cash_flow_sheet(
    title="Griffin Bank Limited — Statement of Cash Flows",
    subtitle="Bank-only (no group); FY2023 covers a 15-month period ended 30 September 2023 and is "
              "labelled unaudited in the source; see the source note below",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=170,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Asset Quality: the Bank has no customer lending at all in any of the 3
# published years - confirmed explicitly in its own Financial risk
# management note ("As the Bank has no customer lending at this stage, the
# main credit risk to which the Bank is exposed is counterparty risk
# associated with its placements at banks and its investments" - AR2025
# p.93, Note 28 Financial risk management, Credit risk) and by all 3
# years' own Balance Sheets having no "Loans and advances to customers"
# line at all - genuinely nil, not a data gap.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("DATA", "Not publicly disclosed - the Bank has no customer lending in any of the 3 published years "
             "(confirmed explicitly in its own Note 28 'Financial risk management, Credit risk' and by the "
             "absence of any loan line on the Balance Sheet) - see source note.", {}),
]

bw.add_asset_quality_sheet(
    title="Griffin Bank Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="No customer lending exists at all in FY2023-FY2025 - see source note.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Griffin Bank Limited's own Note 28 'Financial risk management' (Annual Report and "
        "Financial Statements 2025, p.93, Credit risk section) - " + AR2025_URL + " - states: \"As the "
        "Bank has no customer lending at this stage, the main credit risk to which the Bank is exposed is "
        "counterparty risk associated with its placements at banks and its investments.\" Confirmed against "
        "all 3 years' own Balance Sheets (FY2023-FY2025), none of which show a Loans and advances to "
        "customers line at all - the Bank's only interest-bearing assets are cash/bank placements and debt "
        "securities/Treasury bills/supranational bonds (see Balance Sheet sheet).\n\n" + ENTITY_NOTE
    ),
    first_col_width=90,
    source_height=200,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=130)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2023": 8564})],
    p3_sources(),
)
metric(
    "CET1 Ratio", "%",
    [("CET1 ratio", {"FY2023": "456%"})],
    p3_sources(),
    note="An extreme ratio reflecting the Bank's genuine early-mobilisation position (capital raised "
         "ahead of loan-book/RWA growth, per the Bank's own FY2023 Pillar 3 report), not a transcription "
         "error - the KM1 table's own RWA figure (£1,879k) against £8,564k of CET1 capital is internally "
         "consistent.",
)
metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2023": 8564})],
    p3_sources(),
    note="No Additional Tier 1 instruments - Tier 1 capital equals CET1 capital in the source.",
)
metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {"FY2023": "456%"})],
    p3_sources(),
)
metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2023": 8564})],
    p3_sources(),
    note="No Tier 2 instruments - Total capital equals CET1/Tier 1 capital in the source.",
)
metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {"FY2023": "456%"})],
    p3_sources(),
)
metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2023": 1879})],
    p3_sources(),
)

# ---------------------------------------------------------------
# RWA Breakdown - only FY2023 has a Pillar 3 report at all (see p3_sources'
# note - no Pillar 3 disclosure has been published for FY2024/FY2025).
# Sourced from the FY2023 Pillar 3 Report's own OV1 table.
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2023": 706}),
    ("DATA", "Operational risk", {"FY2023": 1174}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2023": 1879}),
]

bw.add_rwa_breakdown_sheet(
    title="Griffin Bank Limited — RWA Breakdown",
    subtitle="Only FY2023 has a published Pillar 3 report - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\n\nGENUINE £1k ROUNDING GAP, not force-reconciled: the OV1 table's own category figures (Credit "
        "risk £706k + Operational risk £1,174k = £1,880k) sum to £1k more than the same document's own KM1 "
        "table Total risk-weighted exposure amount (£1,879k) - both reproduced as disclosed; the KM1 total "
        "is used on the Total RWAs sheet per project convention."
    ),
    first_col_width=64,
    source_height=200,
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio excluding claims on central banks", {"FY2023": "91%"})],
    p3_sources(),
)
metric(
    "LCR", "%",
    [("Liquidity coverage ratio (average of 8 months reported LCR post-authorisation)", {"FY2023": "2,675%"})],
    p3_sources(),
    note="An extreme ratio for the same genuine early-mobilisation reason as the capital ratios above - "
         "the Bank held far more high-quality liquid assets (£10,387k weighted) than its tiny net cash "
         "outflow (£388k) required this early in its life.",
)
metric(
    "NSFR", "%",
    [("Net stable funding ratio (average of 8 months reported NSFR post-authorisation)", {"FY2023": "1,034%"})],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], sources_text=p3_sources())

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 119551420, "FY2024": 18725660, "FY2023": 10231714}),
        ("Debt securities", {"FY2025": 106511170, "FY2024": 12709240, "FY2023": 8551308}),
        ("Customer deposits", {"FY2025": 101783429, "FY2024": 2070144}),
        ("Total equity", {"FY2025": 16507699, "FY2024": 15174425, "FY2023": 8761243}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Total net revenue", {"FY2025": 1925815, "FY2024": 744633, "FY2023": 291456}),
        ("Total operating costs", {"FY2025": -13983964, "FY2024": -13634562, "FY2023": -13011040}),
        ("Loss for the year/period after taxation", {"FY2025": -12058149, "FY2024": -12889929, "FY2023": -12719584}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 15174425, "FY2024": 8761243, "FY2023": 9585885}),
        ("Loss for the year/period", {"FY2025": -12058149, "FY2024": -12889929, "FY2023": -12719584}),
        ("Other movements, net", {"FY2025": 13391423, "FY2024": 19303111, "FY2023": 11894942}),
        ("Closing equity", {"FY2025": 16507699, "FY2024": 15174425, "FY2023": 8761243}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": 89261779, "FY2024": -10464980, "FY2023": -12063952,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": -94044573, "FY2024": -5540942, "FY2023": -8527971,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": 9744844, "FY2024": 18093063, "FY2023": 9814533,
        }),
        ("Cash and cash equivalents at end of year/period", {
            "FY2025": 7326998, "FY2024": 2364540, "FY2023": 270150,
        }),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2023": "456%"}),
        ("Tier 1 Ratio", {"FY2023": "456%"}),
        ("Total Capital Ratio", {"FY2023": "456%"}),
        ("Leverage Ratio", {"FY2023": "91%"}),
        ("LCR", {"FY2023": "2,675%"}),
        ("NSFR", {"FY2023": "1,034%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Only FY2023 has any Pillar 3 data - no "
         "Pillar 3 report has been published for FY2024 or FY2025 (confirmed, not an access gap). The Bank "
         "has no customer lending at all in any of the 3 published years - Asset Quality is 'Not publicly "
         "disclosed' for this genuine reason (see that sheet's own source note).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/GRIFFIN BANK FINANCIALS.xlsx")
