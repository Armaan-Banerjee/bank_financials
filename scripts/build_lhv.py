import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# LHV Bank Limited was granted its (unrestricted) PRA banking licence on
# 3 May 2023 - its first Annual Report covers FY2023, so only 3 years of
# history exist (mirrors why Bank of London only had 4 - too young for 5).
YEARS = ["FY2025", "FY2024", "FY2023"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://framerusercontent.com/assets/ZBWKLmRUPe8T4hKrOicG3V2KYeE.pdf"
AR2024_URL = "https://framerusercontent.com/assets/srilZFyKHEx1zeu697l5ZFVMXoU.pdf"
AR2023_URL = "https://framerusercontent.com/assets/6Jp4ZWQKQVS1wXUDoBneovYKzIo.pdf"
P3_2025_URL = "https://framerusercontent.com/assets/xqUVp5XxVe8i90y3LAxlQmmQg.pdf"
P3_2024_URL = "https://framerusercontent.com/assets/OJpwHIE7Kzeo65KeJdj7ZrJGUk.pdf"
P3_2023_URL = "https://framerusercontent.com/assets/5YzVUZr8JQg4njsGLzu4ZBXBs8.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: LHV Bank Limited (Companies House 13180211, FRN 993767) is a UK bank owned by AS LHV Group "
    "(Estonia), incorporated 4 February 2021 and granted an unrestricted PRA banking licence on 3 May 2023 - its "
    "first Annual Report and Pillar 3 disclosure cover FY2023, so only 3 years of history exist (too young for 5). "
    "As at 31 December 2025 it is classified as an 'other institution' (not Small and Non-Complex, not Large) under "
    "Article 433 of the PRA Rulebook's Disclosure Part, requiring a reduced annual-only Pillar 3 disclosure with no "
    "KM2/MREL template - consistent with no MREL figures appearing in any year's Pillar 3 report."
)

DATA_ERROR_NOTE = (
    "DATA ERROR NOTE: LHV Bank Limited's own FY2024 Annual Report (p.55) prints 'Net Increase in cash and cash "
    "equivalents' for FY2024 as (199,190,949) - this does not reconcile with that same report's own opening "
    "(242,124,881) and closing (362,299,484) balances, nor with the sum of its own three activity subtotals "
    "(101,379,183 - 1,059,316 + 19,854,736 = 120,174,603). This workbook uses the correct, reconciling figure "
    "(120,174,603, i.e. £120,175k), which independently matches both the opening/closing balance difference and "
    "the FY2025 Annual Report's own restated FY2024 comparative (£120,175k, p.67) - not the erroneous figure as "
    "printed in the FY2024 report itself."
)

DATA_ERROR_NOTE_2 = (
    "DATA ERROR NOTE 2 (2026-09-07): LHV Bank Limited's own FY2025 Annual Report (p.66, Statement of comprehensive "
    "income) prints 'Total operating income' for FY2025 as £2k - this is the sum of only the last three income "
    "lines (Other operating income 248, Changes in fair value of financial instruments at FVTPL (183), Foreign "
    "exchange translation differences (63) = 2), omitting Net interest income (23,515) and Net fee and commission "
    "income (24,058) entirely, even though both sit directly above it in the same statement with no other "
    "subtotal in between. This does not reconcile with the same statement's own next line down: 'Net operating "
    "income' (Total operating income less Operating expenses) is printed as 8,133, which only reconciles against "
    "a Total operating income of approximately 47,575 (23,515 + 24,058 + 248 - 183 - 63 = 47,575; less Operating "
    "expenses of 39,443 = 8,132, matching the printed 8,133 to rounding) - not the printed 2. This workbook uses "
    "the reconciling figure (47,575) for 'Total operating income', not the source's own apparent misprint."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are LHV Bank Limited's own Statement of Cash Flows, £'000 (FY2023/FY2024 as originally "
    "reported in whole £, divided by 1,000 here for unit consistency with FY2025's own £'000 presentation):\n"
    f"FY2025: LHV Bank Limited Annual Report 2025, p.67 (Statement of cash flows) - {AR2025_URL}\n"
    f"FY2024: LHV Bank Limited Annual Report and Financial Statements 2024, p.55 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: LHV Bank Limited Annual Report and Financial Statements 2023, p.31 (Statement of Cash Flows) - {AR2023_URL}\n"
    "Note: FY2025's report uses a simplified presentation ('Non-cash items' and 'Changes in operating assets and "
    "liabilities' as single combined lines); FY2023/FY2024 break these out into more granular line items instead - "
    "each year's own line items/labels are preserved as reported, blank where a year didn't disclose that split. "
    "FY2023's own report did not print a combined 'Net cash from operating activities' total (only three "
    "un-combined subsection subtotals) - the total shown here for FY2023 is computed as the sum of its own "
    "operating-activity line items, and is confirmed exactly by its appearance as FY2024's report's own FY2023 "
    "comparative (224,565,739).\n\n"
    + ENTITY_NOTE + "\n\n" + DATA_ERROR_NOTE
)


def p3_sources():
    return (
        "Sources - LHV Bank Limited's own Pillar 3 disclosures (solo basis), £'000:\n"
        f"FY2025: LHV Bank Limited Pillar 3 Disclosures 2025, p.6-7 (3.1.2 Template UK KM1 - Key metrics) - {P3_2025_URL}\n"
        f"FY2024: LHV Bank Limited Pillar 3 Disclosures 2024, p.11 (Key metrics) - {P3_2024_URL}\n"
        f"FY2023: LHV Bank Limited Pillar 3 Disclosures 2023, p.12 (Key metrics) - {P3_2023_URL}\n"
        "Each year's figures are confirmed by their exact appearance as the following year's comparative column, "
        "where shown."
    )


bw = BankWorkbook(bank_name="LHV Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="5C2751")

STATEMENTS_SOURCES = (
    "Sources - LHV Bank Limited Annual Reports, solo basis, £'000 (FY2023/FY2024 as originally reported in whole "
    "£, divided by 1,000 here for unit consistency with FY2025's own £'000 presentation):\n"
    f"FY2025: Annual Report 2025, Statement of financial position/Statement of comprehensive income/Statement of "
    f"change in equity, p.65-66, Note 14 'Loans and advances to customers' p.86, Note 34.1.12-34.1.14 'Credit "
    f"performance'/'Movement in total exposures' p.107-108 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements 2024, Statement of Financial Position/Statement of "
    f"Comprehensive Income/Statement of Change in Equity, p.52-54, Note 12 'Loans and advances to customers' "
    f"p.78-79 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, Statement of Comprehensive Income/Statement of "
    f"Financial Position/Statement of Changes in Equity, p.28-30 - {AR2023_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: FY2025's Statement of comprehensive income \"has been re-represented using a new format\" "
    "(the Bank's own words) - its structure (Total operating income before Operating expenses, then Net operating "
    "income, then Change in ECL allowance as its own line) genuinely differs from FY2023/FY2024's structure (Net "
    "operating income shown AFTER Credit impairment charge, BEFORE Operating expenses). Each year's own "
    "contemporaneous report's structure is preserved as published rather than forced into one template; FY2024's "
    "own report (not AR2025's later re-represented comparative) is used for FY2024's own figures, per project "
    "convention - the two are numerically identical (AR2025's FY2024 comparative column ties to AR2024's own "
    "figures to the last £'000) so this is a presentation-only choice, not a data conflict.\n\n"
    "Balance Sheet line items also differ across years: FY2025 splits out Derivative financial instruments, "
    "Prepayments and accrued income, Amounts due from/to other group undertakings, and Right-of-use assets "
    "separately; FY2023/FY2024 combine most of these into 'Other assets'/'Other liabilities' or fold right-of-use "
    "assets into Property, plant and equipment - blank cells indicate that year's report did not disclose that "
    "specific split, not that the balance was zero. FY2023/FY2024 disclose 'Overdraft from fellow subsidiary' as "
    "its own line (repaid during FY2024); no equivalent exists in FY2025. FY2023/FY2024 disclose a separate "
    "'Merger reserve' component of equity (arising on the LHV Pank branch business transfer, Aug 2023); FY2025's "
    "own equity statement combines this into a single 'Other reserves' line instead - see the Statement of Changes "
    "in Equity sheet's own note for how this is reconciled.\n\n"
    + DATA_ERROR_NOTE_2
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 558485, "FY2024": 362299, "FY2023": 242125}),
    ("DATA", "Derivative financial instruments (asset)", {"FY2025": 481}),
    ("DATA", "Loans and advances to customers", {"FY2025": 682579, "FY2024": 288799, "FY2023": 69009}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 2022}),
    ("DATA", "Other assets", {"FY2025": 2558, "FY2024": 6052, "FY2023": 2731}),
    ("DATA", "Amounts due from other group undertakings", {"FY2025": 1778}),
    ("DATA", "Right-of-use assets", {"FY2025": 1285}),
    ("DATA", "Property, plant and equipment", {"FY2025": 870, "FY2024": 3435, "FY2023": 5437}),
    ("DATA", "Intangible assets", {"FY2025": 1193, "FY2024": 1041}),
    ("DATA", "Deferred tax assets", {"FY2025": 418, "FY2024": 806, "FY2023": 1710}),
    ("TOTAL", "Total assets", {"FY2025": 1251669, "FY2024": 662432, "FY2023": 321011}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Derivative financial instruments (liability)", {"FY2025": 446}),
    ("DATA", "Amounts due to banks", {"FY2025": 9090}),
    ("DATA", "Deposits by/from customers", {"FY2025": 1114522, "FY2024": 584520, "FY2023": 206998}),
    ("DATA", "Overdraft from fellow subsidiary", {"FY2023": 57473}),
    ("DATA", "Amounts due to other group undertakings", {"FY2025": 12}),
    ("DATA", "Subordinated liabilities", {"FY2025": 10033}),
    ("DATA", "Provisions", {"FY2025": 358, "FY2024": 267, "FY2023": 188}),
    ("DATA", "Other liabilities", {"FY2025": 8876, "FY2024": 3939, "FY2023": 5651}),
    ("DATA", "Lease liabilities", {"FY2025": 1454, "FY2024": 2367, "FY2023": 4004}),
    ("TOTAL", "Total liabilities", {"FY2025": 1144791, "FY2024": 591093, "FY2023": 274314}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called-up share capital", {"FY2025": 105000, "FY2024": 75000, "FY2023": 54100}),
    ("DATA", "Other reserves", {"FY2025": -346, "FY2024": -612, "FY2023": -1270}),
    ("DATA", "Accumulated profits/(losses)", {"FY2025": 2224, "FY2024": -3049, "FY2023": -6133}),
    ("TOTAL", "Total equity", {"FY2025": 106878, "FY2024": 71339, "FY2023": 46697}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 1251669, "FY2024": 662432, "FY2023": 321011}),
]

bw.add_balance_sheet_sheet(
    title="LHV Bank Limited — Balance Sheet",
    subtitle="Solo basis, £'000 unless stated. Only 3 years shown - see Cash Flow Statement sheet's ENTITY NOTE.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 58374, "FY2024": 29616, "FY2023": 29628}),
    ("DATA", "Interest expense", {"FY2025": -34859, "FY2024": -17219, "FY2023": -4576}),
    ("TOTAL", "Net interest income", {"FY2025": 23515, "FY2024": 12397, "FY2023": 25052}),
    ("DATA", "Fee and commission income", {"FY2025": 26285, "FY2024": 26840, "FY2023": 6962}),
    ("DATA", "Fee and commission expense", {"FY2025": -2227, "FY2024": -1902, "FY2023": -202}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 24058}),
    ("DATA", "Other operating income", {"FY2025": 248, "FY2024": 420, "FY2023": 227}),
    ("DATA", "Changes in fair value of financial instruments measured at FVTPL", {"FY2025": -183}),
    ("DATA", "Foreign exchange translation differences", {"FY2025": -63, "FY2024": -102, "FY2023": -62}),
    ("TOTAL", "Total operating income",
     # DATA_ERROR_NOTE_2: the FY2025 AR's own printed figure here is 2 -
     # this workbook uses the reconciling figure instead, see source note.
     {"FY2025": 47575}),
    ("TOTAL", "Net operating income (FY2023/FY2024's own subtotal, BEFORE operating expenses - structured "
              "differently from FY2025's own subtotals above/below)", {"FY2024": 37241, "FY2023": 31978}),
    ("DATA", "Personnel expenses", {"FY2024": -18715, "FY2023": -12886}),
    ("DATA", "Depreciation and amortisation", {"FY2024": -1091, "FY2023": -1596}),
    ("DATA", "Other operating expenses", {"FY2024": -13391, "FY2023": -12566}),
    ("TOTAL", "Operating expenses", {"FY2025": -39443, "FY2024": -33197, "FY2023": -27198}),
    ("TOTAL", "Net operating income (FY2025's own subtotal, AFTER operating expenses)", {"FY2025": 8133}),
    ("DATA", "Change in expected credit loss allowance", {"FY2025": -1367, "FY2024": -412, "FY2023": -150}),
    ("TOTAL", "Profit before tax", {"FY2025": 6766, "FY2024": 4044, "FY2023": 4780}),
    ("DATA", "Taxation (charge)/credit", {"FY2025": -2004, "FY2024": -961, "FY2023": 1657}),
    ("TOTAL", "Profit after tax", {"FY2025": 4761, "FY2024": 3084, "FY2023": 6437}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 4761, "FY2024": 3084, "FY2023": 6437}),
]

bw.add_income_statement_sheet(
    title="LHV Bank Limited — Profit & Loss",
    subtitle="Solo basis, £'000 unless stated. FY2023/FY2024's own reports show Credit impairment charge and Net "
              "operating income BEFORE operating expenses; FY2025's re-represented format moves operating expenses "
              "before Net operating income and adds a separate 'Change in ECL allowance' line - each year's own "
              "structure preserved, not forced into one template (see STATEMENTS_SOURCES note).",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=100,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder confirmed:
# every year's own closing balance ties exactly to both the next year's own
# opening balance and that year's own Balance Sheet Total equity, EXCEPT one
# genuine, disclosed reclassification flagged explicitly below (net £nil).
# ---------------------------------------------------------------
equity_headers = ["Called-up share capital", "Other reserves", "Accumulated profits/(losses)", "Total"]
equity_rows = [
    ("TOTAL", "Opening balance at 1 January 2023 (FY2023 opening, = FY2022 closing)", (44100, 121, -12570, 31651)),
    ("DATA", "Profit for the year", (None, None, 6437, 6437)),
    ("DATA", "Issue and allotment of share capital", (10000, None, None, 10000)),
    ("DATA", "Share based payments", (None, 334, None, 334)),
    ("DATA", "Merger reserve arising on LHV Pank branch business transfer (18 Aug 2023)", (None, -1725, None, -1725)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (54100, -1270, -6133, 46697)),
    ("DATA", "Profit for the year", (None, None, 3084, 3084)),
    ("DATA", "Issue and allotment of share capital", (20900, None, None, 20900)),
    ("DATA", "Share based payments", (None, 658, None, 658)),
    ("TOTAL", "At 31 December 2024 per AR2024's own report (FY2024 closing, AR2024's own basis)", (75000, -612, -3049, 71339)),
    ("DATA", "Reclassification between reserve categories per AR2025's own restated FY2024 comparative "
             "(net £nil - see note below, NOT a plug for a genuine error)", (None, -19, 19, None)),
    ("TOTAL", "At 1 January 2025 per AR2025's own comparative (FY2025 opening, AR2025's own basis)", (75000, -631, -3030, 71339)),
    ("DATA", "Total comprehensive income", (None, None, 4761, 4761)),
    ("DATA", "Issue and allotment of share capital", (30000, None, None, 30000)),
    ("DATA", "Net share option movements", (None, 285, 492, 777)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (105000, -346, 2224, 106878)),
]

bw.add_equity_changes_sheet(
    title="LHV Bank Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest. £'000. Equity reconciliation ladder confirmed: every "
              "year's own closing balance ties exactly to the next year's own opening balance and that year's own "
              "Balance Sheet Total equity - Total equity itself is never in doubt at any point (46,697 / 71,339 / "
              "106,878), only the split between the 'Other reserves' and 'Accumulated profits' columns for the "
              "31 Dec 2024 balance differs by £19k between AR2024's own closing figures and AR2025's own restated "
              "comparative (a genuine, disclosed reclassification between reserve categories, not a plug for an "
              "error) - flagged explicitly as its own row rather than silently absorbed into either adjacent row.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

# ---------------------------------------------------------------
# Asset Quality - IFRS 9 stage exposure/ECL for loans and advances to
# customers (on-balance sheet, secured commercial lending). FY2025/FY2024
# stage split from AR2025's own Note 34.1.12-34.1.14 (Credit performance /
# Movement in total exposures); FY2023 stage split (100% Stage 1) from
# AR2024's own Note 12 comparative, confirmed by AR2023's own note that no
# stage escalation had occurred in the Bank's first partial year.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, on-balance sheet gross exposure by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 634582, "FY2024": 286049, "FY2023": 69214}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 42925, "FY2024": 1246}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 6965, "FY2024": 2121}),
    ("TOTAL", "Total gross exposure (on-balance sheet, IFRS 9 stage table basis)", {"FY2025": 684472, "FY2024": 289416, "FY2023": 69214}),
    ("SECTION", "ECL allowance by IFRS 9 stage (on-balance sheet)", {}),
    ("DATA", "Stage 1", {"FY2025": -685, "FY2024": -456, "FY2023": -205}),
    ("DATA", "Stage 2", {"FY2025": -306, "FY2024": -52}),
    ("DATA", "Stage 3", {"FY2025": -902, "FY2024": -109}),
    ("TOTAL", "Total ECL allowance (on-balance sheet)", {"FY2025": -1893, "FY2024": -617, "FY2023": -205}),
    ("SECTION", "Loans and advances to customers, per Note 14/12/loans note (gross secured lending basis)", {}),
    ("DATA", "Gross secured lending", {"FY2025": 684566, "FY2024": 289416, "FY2023": 69214}),
    ("DATA", "Less: allowance for expected credit losses", {"FY2025": -1893, "FY2024": -617, "FY2023": -205}),
    ("DATA", "Fair value adjustment for hedged risk", {"FY2025": -94}),
    ("TOTAL", "Total loans and advances to customers (ties to Balance Sheet)", {"FY2025": 682579, "FY2024": 288799, "FY2023": 69009}),
    ("DATA", "ECL coverage ratio (Total ECL allowance / Gross secured lending)", {
        "FY2025": "0.28%", "FY2024": "0.21%", "FY2023": "0.30%",
    }),
    ("SECTION", "Loans and advances by product (FY2024/FY2023 only - see note)", {}),
    ("DATA", "Commercial Investment Loan", {"FY2024": 219690, "FY2023": 46339}),
    ("DATA", "Commercial Mortgage Loan", {"FY2024": 69726, "FY2023": 22875}),
]

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit for the year before taxation", {"FY2025": 6766, "FY2024": 4044.276, "FY2023": 4779.563}),
    ("DATA", "Non-cash items (combined, as reported)", {"FY2025": 4064}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2024": 1091.16, "FY2023": 1596.396}),
    ("DATA", "Share based payments", {"FY2024": 638.961, "FY2023": 334.11}),
    ("DATA", "Foreign exchange translation differences", {"FY2024": 101.96}),
    ("DATA", "Credit impairment losses/(gains)", {"FY2024": 411.671, "FY2023": 149.876}),
    ("DATA", "Increase/(decrease) in other assets/other liabilities (combined, as reported)", {"FY2023": 2716.589}),
    ("DATA", "Changes in operating assets and liabilities (combined, as reported)", {"FY2025": 147815}),
    ("DATA", "(Increase)/decrease in operating assets", {"FY2024": -3353.822}),
    ("DATA", "(Increase)/decrease in operating liabilities", {"FY2024": -1200.156}),
    ("DATA", "Tax paid", {"FY2025": -1125, "FY2024": -278.181}),
    ("DATA", "Net loans and advances to customers", {"FY2024": -219442.236, "FY2023": -49482.095}),
    ("DATA", "Net deposits from customers", {"FY2024": 376838.55, "FY2023": 206998.301}),
    ("DATA", "Facilities/amounts received from/(to) group companies", {"FY2024": -57472.999, "FY2023": 57472.999}),
    ("TOTAL", "Net cash generated from operating activities", {"FY2025": 157520, "FY2024": 101379.183, "FY2023": 224565.739}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2023": -1079.751}),
    ("DATA", "Acquisition of property, plant & equipment and intangibles (combined, as reported)", {"FY2024": -1059.316}),
    ("DATA", "Purchase and development of intangible assets", {"FY2025": -325}),
    ("DATA", "Banking Services business transfer", {"FY2023": -1724.857}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {"FY2025": -325, "FY2024": -1059.316, "FY2023": -2804.607}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue and allotment of share capital / shares issued", {"FY2025": 30000, "FY2024": 20900, "FY2023": 10000}),
    ("DATA", "Proceeds from issuance of subordinated liabilities", {"FY2025": 10000}),
    ("DATA", "Payment of lease liabilities", {"FY2025": -1010, "FY2024": -1045.264, "FY2023": -1287.675}),
    ("TOTAL", "Net cash generated from financing activities", {"FY2025": 38990, "FY2024": 19854.736, "FY2023": 8712.325}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 196185, "FY2024": 120174.603, "FY2023": 230473.456}),
    ("DATA", "Cash and cash equivalents at start of year", {"FY2025": 362299, "FY2024": 242124.881, "FY2023": 11651.425}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 558485, "FY2024": 362299.484, "FY2023": 242124.881}),
]

bw.add_cash_flow_sheet(
    title="LHV Bank Limited — Statement of Cash Flows",
    subtitle="Solo basis, £'000 unless stated. See source note at bottom (incl. a known FY2024 report error).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=260,
    unit_suffix=" (£'000)",
)

bw.add_asset_quality_sheet(
    title="LHV Bank Limited — Asset Quality",
    subtitle="IFRS 9 stage exposure/ECL for secured commercial lending (on-balance sheet). £'000.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nDATA QUALITY NOTE: FY2024's IFRS 9 stage table (Note 12, AR2024) totals £289,416k, £3k more than "
        "Note 34's own FY2024 (Represented) total in AR2025 (£289,413k) - an immaterial cross-note rounding "
        "difference in the Bank's own disclosures, not a transcription error here; both are shown as sourced. "
        "FY2025's on-balance-sheet IFRS 9 stage total (£684,472k, Note 34) is £94k less than Note 14's own 'Gross "
        "secured lending' figure (£684,566k) - reconciled via the 'Fair value adjustment for hedged risk' line, "
        "which brings the total to the Balance Sheet's own £682,579k. No IFRS 9 stage split or by-product breakdown "
        "is disclosed for FY2025 anywhere in the Annual Report reviewed this session (Note 14 only shows an "
        "aggregate gross/ECL/net figure by product) - genuinely unavailable this session, not assumed absent."
    ),
    first_col_width=90,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Solo basis, {unit}" if unit else "Solo basis",
                         rows_data, p3_sources(), note=note, first_col_width=46, source_height=120)


# ---------------------------------------------------------------
# KM1 Key Metrics (wayfinder/km1/map.md) - the Bank's own published
# key-metrics template, reproduced whole in its own row order, labels and
# precision. add_km1_sheet() is called BEFORE the first add_metric_sheet()
# so the sheet lands immediately after Asset Quality and immediately before
# CET1 Capital: sheet order follows call order.
#
# ROW-SET TEST (map rule 8). The FY2023 and FY2024 editions head this table
# simply "Key metrics", print no row numbers and never write the token
# "KM1"; the FY2025 edition heads the identical table "3.1.2 Template UK KM1
# - Key metrics template". The row set is the test, and it is the template's:
# own funds, risk-weighted exposure amount, capital ratios, additional own
# funds requirements, the combined buffer block, leverage, and the full LCR
# and NSFR component build-ups. So all three years are the template. The
# Bank's own SREP block is CONDENSED ("Additional requirement" / "Total own
# funds requirements" in place of the template's UK 7a-7d split) and no
# edition prints row numbers at all - both reproduced exactly as published
# rather than mapped onto template row numbers the Bank never printed.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds", {}),
    ("DATA", "Common equity Tier 1 capital (£'000)", {"FY2025": 103888, "FY2024": 68399, "FY2023": 44532}),
    ("DATA", "Tier 1 capital (£'000)", {"FY2025": 103888, "FY2024": 68399, "FY2023": 44532}),
    ("DATA", "Total capital (£'000)", {"FY2025": 113921, "FY2024": 68399, "FY2023": 44532}),
    ("SECTION", "Risk weighted exposure amounts", {}),
    ("DATA", "Total risk weighted exposure amount (£'000)", {"FY2025": 561468, "FY2024": 284276, "FY2023": 140702}),
    ("SECTION", "Capital ratios", {}),
    ("DATA", "Common equity Tier 1 capital ratio (%)", {"FY2025": "18.5%", "FY2024": "24.1%", "FY2023": "31.7%"}),
    ("DATA", "Tier 1 capital ratio (%)", {"FY2025": "18.5%", "FY2024": "24.1%", "FY2023": "31.7%"}),
    ("DATA", "Total capital ratio (%)", {"FY2025": "20.3%", "FY2024": "24.1%", "FY2023": "31.7%"}),
    ("SECTION", "Additional own funds requirements", {}),
    ("DATA", "Additional requirement (%)", {"FY2025": "3.5%", "FY2024": "2.2%", "FY2023": "1.7%"}),
    ("DATA", "Total own funds requirements (%)", {"FY2025": "11.5%", "FY2024": "10.2%", "FY2023": "9.7%"}),
    ("SECTION", "Combined buffer requirement", {}),
    ("DATA", "Capital conservation buffer (%)", {"FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.5%"}),
    ("DATA", "Institution specific countercyclical buffer (%)", {"FY2025": "2.0%", "FY2024": "2.0%", "FY2023": "2.0%"}),
    ("DATA", "Combined buffer requirement (%)", {"FY2025": "4.5%", "FY2024": "4.5%", "FY2023": "4.5%"}),
    ("DATA", "Total capital requirement and combined buffers (%)", {"FY2025": "16.0%", "FY2024": "14.7%", "FY2023": "14.2%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "Total exposure measure excluding claims made on central banks (£'000)",
     {"FY2025": 721124, "FY2024": 317763, "FY2023": 79084}),
    ("DATA", "Leverage ratio excluding claims made on central banks (%)",
     {"FY2025": "14.4%", "FY2024": "21.5%", "FY2023": "56.3%"}),
    ("SECTION", "Liquidity coverage ratio", {}),
    ("DATA", "Total HQLA (£'000)", {"FY2025": 405138, "FY2024": 296989, "FY2023": 137258}),
    ("DATA", "Cash outflows (£'000)", {"FY2025": 224517, "FY2024": 183800, "FY2023": 113127}),
    ("DATA", "Cash inflows (£'000)", {"FY2025": 19154, "FY2024": 12270, "FY2023": 9352}),
    ("DATA", "Total net cash outflows (£'000)", {"FY2025": 205363, "FY2024": 171530, "FY2023": 103776}),
    ("DATA", "Liquidity coverage ratio (%)", {"FY2025": "196%", "FY2024": "175%", "FY2023": "133%"}),
    ("SECTION", "Net stable funding ratio", {}),
    ("DATA", "Total available funding (£'000)", {"FY2025": 802886, "FY2024": 372192, "FY2023": 144797}),
    ("DATA", "Total required funding (£'000)", {"FY2025": 441159, "FY2024": 153881, "FY2023": 51410}),
    ("DATA", "Net stable funding ratio (%)", {"FY2025": "182%", "FY2024": "260%", "FY2023": "278%"}),
]

KM1_SOURCES = (
    "Sources - LHV Bank Limited's own Pillar 3 Disclosures (solo basis), key-metrics template, £'000 and % "
    "exactly as printed. EACH YEAR IS TAKEN FROM THE EDITION IN WHICH IT IS THE REPORTING YEAR, never from a "
    "later edition's comparative column:\n"
    f"FY2025: Pillar 3 Disclosures 31 December 2025, section 3.1.2 'Template UK KM1 - Key metrics template', "
    f"printed p.6-7 (the table breaks across the two pages, splitting after 'Combined buffer requirement'), "
    f"column '31 December 2025' - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosures 2024, 'Key metrics', printed p.11, column '31 December 2024' - {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosures 2023, 'Key metrics', printed p.12, single column '31 December 2023' - "
    f"{P3_2023_URL}\n\n"
    "LATEST-EDITION CHECK (required by the KM1 map), performed 2026-09-17 against the Bank's OWN website rather "
    "than our cited URLs or Wayback: lhv.com/about/reports (the reports page the Pillar 3 document itself names "
    "in its section 1.1) lists exactly six documents - Annual Reports for 2023, 2024 and 2025 and Pillar 3 "
    "Disclosures for 2023, 2024 and 2025 - which are the six already cited in this build script. The newest "
    "edition published is the Pillar 3 Disclosures for 31 December 2025. NONE NEWER EXISTS; this workbook is "
    "not an edition behind.\n\n"
    "IS THIS THE KM1 TEMPLATE? YES, ON THE ROW-SET TEST, AND THE BANK SAYS SO ITSELF IN THE NEWEST EDITION. "
    "The FY2023 and FY2024 editions head the table simply 'Key metrics', print no row numbers, and never write "
    "the token 'KM1' anywhere; a presence test keyed on the token or on row numbering would miss both. The "
    "FY2025 edition prints the identical table under the heading 'Template UK KM1 - Key metrics template' and "
    "states it 'outlines the key metrics referenced in Article 447'. The row set is the template's throughout: "
    "available own funds, risk-weighted exposure amount, capital ratios, additional own funds requirements, the "
    "combined buffer block, leverage ratio and exposure measure, and the full LCR and NSFR component "
    "build-ups.\n\n"
    "WHAT THE BANK DOES NOT PRINT, reproduced as absent rather than filled in:\n"
    "• NO ROW NUMBERS in any edition. The template's own numbering ('1', 'UK 7a', '15') is therefore absent "
    "from this sheet too - mapping the Bank's rows onto template numbers it never printed would invent a "
    "correspondence.\n"
    "• A CONDENSED SREP BLOCK. Where the UK template splits additional own funds requirements into UK 7a-7d "
    "(CET1/AT1/T2/total), LHV prints two rows only - 'Additional requirement' and 'Total own funds "
    "requirements'. Shown as the Bank prints them.\n"
    "• NO ROWS BEFORE FY2023, because no earlier edition exists. LHV Bank Limited was granted its unrestricted "
    "PRA banking licence on 3 May 2023 and FY2023 is its first Pillar 3 disclosure - the blank is the absence "
    "of a reporting period, not an access gap or a row we failed to find.\n\n"
    "BASIS NOTE ON THE LIQUIDITY ROWS. The LCR and NSFR rows are period AVERAGES, not year-end points, and each "
    "edition says so in its own footnote. FY2023's average covers only 3 May 2023 (authorisation) to 31 "
    "December 2023 - 'the period from when the entity became an authorised credit institution subject to "
    "reporting requirements', in the Bank's own words - so it is a partial-period average beside FY2024's and "
    "FY2025's full 12-month averages. That is a genuine basis difference across the row, flagged rather than "
    "smoothed.\n\n"
    "TWO ROWS ARE REPORTED AS DISAGREEMENTS BY verify_workbook.py AND BOTH REPORTS ARE FALSE POSITIVES OF THE "
    "CHECKER'S LABEL MATCHING, NOT ERRORS IN THESE FIGURES. The checker decides which metric sheet a KM1 row "
    "belongs to by longest-prefix match on the row label, and two of LHV's own captions begin with the name "
    "of a different metric:\n"
    "• 'Tier 1 capital ratio (%)' begins with 'Tier 1 capital', so the checker compares this PERCENTAGE "
    "against the Tier 1 Capital sheet's AMOUNT (18.5% against £103,888k, and so on for each year). LHV writes "
    "'Tier 1 capital ratio' where the UK template writes 'Tier 1 ratio'; the figures are right and agree with "
    "the Tier 1 Ratio sheet.\n"
    "• 'Total capital requirement and combined buffers (%)' begins with 'Total capital', so it is compared "
    "against the Total Capital sheet's amount. It is a buffer requirement, not a capital amount, and has no "
    "counterpart metric sheet at all.\n"
    "Neither row has been reworded to satisfy the checker: these are the Bank's own printed captions, and "
    "editing them to suit a matching heuristic would be normalising the source by the back door. Six "
    "disagreements on this sheet are these two rows across three years each; every other cross-checked cell "
    "agrees.\n\n"
    "CROSS-CONFIRMATION. Every FY2023 and FY2024 figure above also appears, identically, as the following "
    "edition's comparative column - an independent confirmation of both columns at no transcription cost. "
    "FY2025's are single-sourced from their own edition, LHV publishing no half-year Pillar 3.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="LHV Bank Limited — KM1 Key Metrics",
    subtitle="The Bank's own published key-metrics template (headed 'Template UK KM1 - Key metrics template' in "
             "the FY2025 edition and simply 'Key metrics', unnumbered, in the FY2023 and FY2024 editions), "
             "reproduced whole in its own row order, labels and printed precision. Solo basis. Amounts in £'000, "
             "ratios as printed. Each year comes from its own edition, never a later comparative. LHV prints no "
             "template row numbers and prints a condensed two-row SREP block - both reproduced as published. No "
             "columns before FY2023: the Bank was authorised on 3 May 2023.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=72,
    source_height=420,
)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 103888, "FY2024": 68399, "FY2023": 44532})],
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common equity Tier 1 capital ratio", {"FY2025": "18.5%", "FY2024": "24.1%", "FY2023": "31.7%"})],
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 103888, "FY2024": 68399, "FY2023": 44532})],
    note="Equal to CET1 capital in every year shown - LHV Bank has no Additional Tier 1 (AT1) instruments.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 capital ratio", {"FY2025": "18.5%", "FY2024": "24.1%", "FY2023": "31.7%"})],
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 113921, "FY2024": 68399, "FY2023": 44532})],
    note="Exceeds Tier 1 capital from FY2025 onward following issuance of £10,000k of subordinated (Tier 2) "
         "liabilities during the year (see Cash Flow Statement sheet) - equal to CET1/Tier 1 capital in FY2023 "
         "and FY2024, before that issuance.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "20.3%", "FY2024": "24.1%", "FY2023": "31.7%"})],
)

metric(
    "Total RWAs", "£'000",
    [("Total risk weighted exposure amount", {"FY2025": 561468, "FY2024": 284276, "FY2023": 140702})],
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk", {"FY2025": 481364, "FY2024": 211654, "FY2023": 61243}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 3110, "FY2024": 0, "FY2023": 0}),
    ("DATA", "Market risk", {"FY2025": 3557}),
    ("DATA", "Operational risk", {"FY2025": 73437, "FY2024": 72622, "FY2023": 79460}),
    ("TOTAL", "Total risk weighted exposure amount", {"FY2025": 561468, "FY2024": 284276, "FY2023": 140702}),
]

bw.add_rwa_breakdown_sheet(
    title="LHV Bank Limited — RWA Breakdown",
    subtitle="Solo basis, standardised approach for credit/market risk, basic indicator approach for operational "
              "risk (Template UK OV1). £'000.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\n\nAll years' figures shown above tie exactly to the Total RWAs sheet. Market Risk and Counterparty "
        "Credit Risk are both nil/not disclosed as separate lines in FY2023/FY2024's own Template UK OV1-equivalent "
        "table (only Credit Risk and Operational Risk lines shown, summing exactly to that year's Total); FY2025's "
        "own table is the first to show non-zero Counterparty Credit Risk (£3,110k) and a new Market Risk line "
        "(£3,557k), reflecting genuine growth/diversification in the Bank's activities, not a change in disclosure "
        "practice."
    ),
    first_col_width=76,
    source_height=200,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims made on central banks", {"FY2025": 721124, "FY2024": 317763, "FY2023": 79084}),
        ("Leverage ratio excluding claims made on central banks (%)", {"FY2025": "14.4%", "FY2024": "21.5%", "FY2023": "56.3%"}),
    ],
    note="FY2023's very high ratio (56.3%) reflects the bank's small, deposit/capital-heavy balance sheet shortly "
         "after launch (unrestricted licence granted 3 May 2023), not a transcription error - it fell sharply as "
         "the loan book scaled in FY2024/FY2025.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total HQLA", {"FY2025": 405138, "FY2024": 296989, "FY2023": 137258}),
        ("Total net cash outflows", {"FY2025": 205363, "FY2024": 171530, "FY2023": 103776}),
        ("Liquidity coverage ratio (%)", {"FY2025": "196%", "FY2024": "175%", "FY2023": "133%"}),
    ],
    note="FY2023's LCR/NSFR are averages over 3 May 2023 (authorisation) to 31 December 2023 only, not a full "
         "12-month average like FY2024/FY2025.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available funding", {"FY2025": 802886, "FY2024": 372192, "FY2023": 144797}),
        ("Total required funding", {"FY2025": 441159, "FY2024": 153881, "FY2023": 51410}),
        ("Net stable funding ratio (%)", {"FY2025": "182%", "FY2024": "260%", "FY2023": "278%"}),
    ],
    note="FY2023's NSFR is an average over 3 May 2023 (authorisation) to 31 December 2023 only, not a full "
         "12-month average like FY2024/FY2025.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not applicable" for y in YEARS})],
    note="LHV Bank Limited is classified as an 'other institution' (not Large, not subject to LREQ/G-SII/O-SII "
         "status) under Article 433 of the PRA Rulebook's Disclosure Part as at 31 December 2025, requiring only "
         "reduced annual Pillar 3 disclosure with no UK KM2/MREL template - no MREL figure of any kind appears in "
         "any year's Pillar 3 report.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1251669, "FY2024": 662432, "FY2023": 321011}),
        ("Loans and advances to customers", {"FY2025": 682579, "FY2024": 288799, "FY2023": 69009}),
        ("Deposits by/from customers", {"FY2025": 1114522, "FY2024": 584520, "FY2023": 206998}),
        ("Total equity", {"FY2025": 106878, "FY2024": 71339, "FY2023": 46697}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 23515, "FY2024": 12397, "FY2023": 25052}),
        ("Profit before tax", {"FY2025": 6766, "FY2024": 4044, "FY2023": 4780}),
        ("Profit after tax", {"FY2025": 4761, "FY2024": 3084, "FY2023": 6437}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 71339, "FY2024": 46697, "FY2023": 31651}),
        ("Total comprehensive income for the year", {"FY2025": 4761, "FY2024": 3084, "FY2023": 6437}),
        ("Other equity movements, net", {"FY2025": 30777, "FY2024": 21558, "FY2023": 8609}),
        ("Closing equity", {"FY2025": 106878, "FY2024": 71339, "FY2023": 46697}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 157520, "FY2024": 101379.183, "FY2023": 224565.739}),
        ("Net cash from/(used in) investing activities", {"FY2025": -325, "FY2024": -1059.316, "FY2023": -2804.607}),
        ("Net cash from/(used in) financing activities", {"FY2025": 38990, "FY2024": 19854.736, "FY2023": 8712.325}),
        ("Cash and cash equivalents at end of year", {"FY2025": 558485, "FY2024": 362299.484, "FY2023": 242124.881}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "18.5%", "FY2024": "24.1%", "FY2023": "31.7%"}),
        ("Tier 1 Ratio", {"FY2025": "18.5%", "FY2024": "24.1%", "FY2023": "31.7%"}),
        ("Total Capital Ratio", {"FY2025": "20.3%", "FY2024": "24.1%", "FY2023": "31.7%"}),
        ("Leverage Ratio", {"FY2025": "14.4%", "FY2024": "21.5%", "FY2023": "56.3%"}),
        ("LCR", {"FY2025": "196%", "FY2024": "175%", "FY2023": "133%"}),
        ("NSFR", {"FY2025": "182%", "FY2024": "260%", "FY2023": "278%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Only 3 years shown - LHV Bank Limited was granted its PRA "
         "banking licence on 3 May 2023, so no earlier trading history exists. FY2024 cash flow uses a corrected "
         "'Net increase in cash' figure - see the Cash Flow Statement sheet's DATA ERROR NOTE.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/LHV FINANCIALS.xlsx")
