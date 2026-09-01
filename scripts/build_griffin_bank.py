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


bw = BankWorkbook(bank_name="Griffin Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="3480C7")

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
         "Pillar 3 report has been published for FY2024 or FY2025 (confirmed, not an access gap).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/GRIFFIN BANK FINANCIALS.xlsx")
