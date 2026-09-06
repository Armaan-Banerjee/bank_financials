import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR25_URL = "https://static.ifastgb.com/investor-relations/iFAST%20Global%20Bank%20Ltd.%20Annual%20Report%202025.pdf"
AR24_URL = "https://static.ifastgb.com/investor-relations/iFAST%20Global%20Bank%20Ltd.%20Annual%20Report%202024.pdf"
AR23_URL = "https://www.ifastgb.com/assets/static-file/investor-relations/iFAST%20Global%20Bank%20Ltd.%20Annual%20Report%202023.pdf"
AR21_URL = "https://www.ifastgb.com/assets/static-file/investor-relations/iFAST%20Global%20Bank%20Ltd.%20Annual%20Report%202021.pdf"

P3_25_URL = "https://static.ifastgb.com/investor-relations/iFAST%20Global%20Bank%20Limited%20Pillar%203%20Disclosures%202025.pdf"
P3_23_URL = "https://www.ifastgb.com/assets/static-file/investor-relations/iFAST%20Global%20Bank%20Limited%20Pillar%203%20Disclosures%202023.pdf"
P3_21_URL = "https://www.ifastgb.com/assets/static-file/investor-relations/iFAST%20Global%20Bank%20Limited%20Pillar%203%20Disclosures%202021.pdf"

CASH_FLOW_SOURCES = (
    "Sources — iFAST Global Bank Limited (company no. 04797759, formerly BFC Bank Limited until "
    "31 March 2022) standalone Statement of cash flows, £'000:\n"
    f"FY2025 & FY2024: iFAST Global Bank Ltd. Annual Report 2025, p.36 (Statement of cash flows) — {AR25_URL}\n"
    f"FY2022: iFAST Global Bank Ltd. Annual Report 2023, p.36 (Statement of cash flows, FY2022 comparative "
    f"column, as originally reported) — {AR23_URL}\n"
    f"FY2023: iFAST Global Bank Ltd. Annual Report 2023, p.36 (Statement of cash flows, as originally reported) "
    f"— {AR23_URL}\n"
    f"FY2021: iFAST Global Bank Ltd. Annual Report 2021, p.32 (Statement of cash flows) — {AR21_URL}\n"
    "Note: FY2023 cash and cash equivalents were subsequently restated in the FY2024 Annual Report "
    f"({AR24_URL}) — originally reported closing balance £181,658k, restated to £205,582k — due to Money "
    "Market Funds being reclassified from 'Debt instruments at FVPL' to cash and cash equivalents. This "
    "workbook uses the FY2023 figures as originally reported in the FY2023 Annual Report, so the FY2023 "
    "closing balance shown here will not tie to the FY2024 column's opening balance; this is a genuine "
    "disclosed restatement, not a transcription error. Line-item granularity also changes across vintages "
    "(e.g. FY2025/FY2024 itemise 'Increase in loans to customers' and 'Profit on sale of bonds' separately; "
    "FY2023/FY2022 itemise 'Purchase of assets at fair value through profit and loss'; FY2021 itemises "
    "'Interest received'/'Interest paid' separately) — section totals are consistent and comparable across "
    "all 5 years."
)

def p3_sources(part_label_25="Table 1: UK KM1 - Key Metrics template", page_25="16",
               part_label_23="Table 1: UK KM1- Key Metrics template", page_23="12",
               part_label_21="Own funds table / Leverage Ratio Common Disclosure table", page_21="25 / 23"):
    return (
        "Sources — iFAST Global Bank Limited (formerly BFC Bank Limited) solo basis:\n"
        f"FY2025 & FY2024: iFAST Global Bank Limited Pillar 3 Disclosures 2025, p.{page_25} ({part_label_25}) — {P3_25_URL}\n"
        f"FY2023 & FY2022: iFAST Global Bank Limited Pillar 3 Disclosures 2023, p.{page_23} ({part_label_23}) — {P3_23_URL}\n"
        f"FY2021: BFC Bank Limited Pillar 3 Disclosures 2021, p.{page_21} ({part_label_21}) — {P3_21_URL}"
    )

bw = BankWorkbook(bank_name="iFAST Global Bank Limited", years=YEARS, header_color="0091D5")

STATEMENTS_ENTITY_NOTE = (
    "iFAST Global Bank Limited (company no. 04797759, formerly BFC Bank Limited until 31 March 2022) - "
    "solo/entity basis throughout (the Bank has no subsidiaries). No standalone Annual Report exists for "
    "FY2022 (BFC Bank Limited rebranded mid-year); FY2022 figures are iFAST Global Bank Ltd. Annual Report "
    "2023's own FY2022 comparative column, which that report itself labels 'Restated' for the income "
    "statement (income-statement presentation was reorganised, not a numeric restatement - the loss figure "
    "of £(11,868)k for FY2022 is unchanged across every report that shows it). Balance sheet line items "
    "genuinely change across vintages: 'Debt instruments at fair value through profit or loss' only appears "
    "as its own line in FY2023 (absorbed elsewhere once reclassified in FY2024); 'Loans and advances to "
    "customers' and 'Debt instruments held at amortised cost' first appear from FY2022/FY2024 respectively "
    "as the Bank's balance sheet grew roughly 7x following the 2022 iFAST Corporation acquisition; "
    "'Deferred tax' and 'Other equity instruments' (an AT1 Perpetual Note) first appear in FY2025 only."
)


def statements_sources(extra_note=None):
    text = (
        "Sources - all figures are iFAST Global Bank Limited's own Statement of Financial Position / "
        "Statement of Comprehensive Income / Statement of Changes in Equity:\n"
        f"FY2025: iFAST Global Bank Ltd. Annual Report 2025, p.34-35 - {AR25_URL}\n"
        f"FY2024: iFAST Global Bank Ltd. Annual Report 2024, p.32-33 - {AR24_URL}\n"
        f"FY2023: iFAST Global Bank Ltd. Annual Report 2023, p.34-35 - {AR23_URL}\n"
        f"FY2022: iFAST Global Bank Ltd. Annual Report 2023, p.34-35 (FY2022 comparative column, plus the "
        f"Statement of changes in equity's own FY2022 roll-forward detail) - {AR23_URL}\n"
        f"FY2021: iFAST Global Bank Ltd. Annual Report 2021, p.30-31 - {AR21_URL}\n"
        + STATEMENTS_ENTITY_NOTE
    )
    if extra_note:
        text += " " + extra_note
    return text


# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 394036, "FY2024": 330938, "FY2023": 181658, "FY2022": 74856, "FY2021": 53534}),
    ("DATA", "Trade and other receivables", {"FY2025": 23808, "FY2024": 18868, "FY2023": 20732, "FY2022": 13382, "FY2021": 11037}),
    ("DATA", "Debt instruments held at amortised cost", {"FY2025": 539329, "FY2024": 316623, "FY2023": 58172, "FY2022": 29436}),
    ("DATA", "Debt instruments at fair value through profit or loss", {"FY2023": 23924}),
    ("DATA", "Loans and advances to customers", {"FY2025": 80119, "FY2024": 25046}),
    ("DATA", "Other assets", {"FY2025": 9680, "FY2024": 8483, "FY2023": 2501, "FY2022": 777, "FY2021": 993}),
    ("DATA", "Derivative financial assets", {"FY2025": 240, "FY2024": 7, "FY2023": 216, "FY2022": 83, "FY2021": 187}),
    ("DATA", "Property, plant and equipment", {"FY2025": 3056, "FY2024": 365, "FY2023": 659, "FY2022": 951, "FY2021": 2066}),
    ("DATA", "Intangible assets", {"FY2025": 160, "FY2024": 285, "FY2023": 426, "FY2022": 0, "FY2021": 3919}),
    ("DATA", "Deferred tax", {"FY2025": 1580}),
    ("TOTAL", "Total assets", {"FY2025": 1052008, "FY2024": 700615, "FY2023": 288288, "FY2022": 119485, "FY2021": 71736}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Trade and other payables", {"FY2025": 9524, "FY2024": 9713, "FY2023": 9465, "FY2022": 5742, "FY2021": 8811}),
    ("DATA", "Due to customers", {"FY2025": 941013, "FY2024": 609964, "FY2023": 234882, "FY2022": 73627, "FY2021": 42307}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 0, "FY2024": 1, "FY2023": 16, "FY2022": 156, "FY2021": 82}),
    ("DATA", "Other liabilities", {"FY2025": 5594, "FY2024": 3590, "FY2023": 4066, "FY2022": 3233, "FY2021": 3587}),
    ("DATA", "Provisions", {"FY2024": 0, "FY2023": 378, "FY2022": 1646}),
    ("TOTAL", "Total liabilities", {"FY2025": 956131, "FY2024": 623268, "FY2023": 248807, "FY2022": 84404, "FY2021": 54787}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 124700, "FY2024": 124700, "FY2023": 84700, "FY2022": 74700, "FY2021": 40200}),
    ("DATA", "Contingent Capital Note", {"FY2021": 4500}),
    ("DATA", "Share option reserve", {"FY2025": 856, "FY2024": 436, "FY2023": 110}),
    ("DATA", "Other equity instruments (AT1 Perpetual Note)", {"FY2025": 14676}),
    ("DATA", "Retained earnings", {"FY2025": -44355, "FY2024": -47789, "FY2023": -45329, "FY2022": -39619, "FY2021": -27751}),
    ("TOTAL", "Total equity", {"FY2025": 95877, "FY2024": 77347, "FY2023": 39481, "FY2022": 35081, "FY2021": 16949}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 1052008, "FY2024": 700615, "FY2023": 288288, "FY2022": 119485, "FY2021": 71736}),
]

bw.add_balance_sheet_sheet(
    title="iFAST Global Bank Limited — Statement of Financial Position",
    subtitle="Solo basis, £'000",
    rows=bs_rows,
    sources_text=statements_sources(),
    first_col_width=68,
    source_height=180,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
is_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 37524, "FY2024": 22104, "FY2023": 6213, "FY2022": 580, "FY2021": 13}),
    ("DATA", "Interest expense", {"FY2025": -26613, "FY2024": -16764, "FY2023": -4512, "FY2022": -459, "FY2021": -463}),
    ("TOTAL", "Net interest income/(expense)", {"FY2025": 10911, "FY2024": 5340, "FY2023": 1701, "FY2022": 121, "FY2021": -450}),
    ("DATA", "Fee and commission income", {"FY2025": 9086, "FY2024": 6787, "FY2023": 4862, "FY2022": 4916, "FY2021": 4832}),
    ("DATA", "Fee and commission expense", {"FY2025": -1215, "FY2024": -1888, "FY2023": -1305, "FY2022": -1260, "FY2021": -1369}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 7871, "FY2024": 4899, "FY2023": 3557, "FY2022": 3656}),
    ("DATA", "Net trading profit on foreign exchange", {"FY2025": 2693, "FY2024": 1803, "FY2023": 2706, "FY2022": 2996, "FY2021": 4479}),
    ("DATA", "Fair value gain/(loss) on derivatives", {"FY2025": 52, "FY2024": -194, "FY2023": 274, "FY2022": -37, "FY2021": -531}),
    ("DATA", "Other operating income", {"FY2025": 8, "FY2024": 2, "FY2023": 0, "FY2022": 17, "FY2021": 88}),
    ("DATA", "Allowance for impairment loss", {"FY2025": -303, "FY2024": -179, "FY2023": -119, "FY2022": -109}),
    ("TOTAL", "Net operating income", {"FY2025": 21232, "FY2024": 11671, "FY2023": 8119, "FY2022": 6644, "FY2021": 7049}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Depreciation", {"FY2025": -397, "FY2024": -313, "FY2023": -312, "FY2022": -349, "FY2021": -363}),
    ("DATA", "Amortisation", {"FY2025": -149, "FY2024": -141, "FY2023": -12, "FY2022": -159, "FY2021": -635}),
    ("DATA", "Other operating expenses", {"FY2025": -18854, "FY2024": -14009, "FY2023": -12780, "FY2022": -14688, "FY2021": -9637}),
    ("DATA", "Net foreign exchange gain/(loss)", {"FY2025": 22, "FY2024": 332, "FY2023": -725, "FY2022": -166, "FY2021": 501}),
    ("TOTAL", "Total operating expenses", {"FY2025": -19378, "FY2024": -14131, "FY2023": -13829, "FY2022": -15632, "FY2021": -10134}),
    ("TOTAL", "Profit/(loss) from continuing operations", {"FY2025": 1854, "FY2024": -2460, "FY2023": -5710, "FY2022": -8718, "FY2021": -3085}),
    ("DATA", "Loss from discontinued operations, net of tax", {"FY2022": -3150}),
    ("TOTAL", "Profit/(loss) before tax for the year", {"FY2025": 1854, "FY2024": -2460, "FY2023": -5710, "FY2022": -11868, "FY2021": -3085}),
    ("DATA", "Tax credit/(expense)", {"FY2025": 1580, "FY2024": 0}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 3434, "FY2024": -2460, "FY2023": -5710, "FY2022": -11868, "FY2021": -3085}),
]

bw.add_income_statement_sheet(
    title="iFAST Global Bank Limited — Statement of Comprehensive Income",
    subtitle="Solo basis, £'000. There was no other comprehensive income in any of the 5 years.",
    rows=is_rows,
    sources_text=statements_sources(
        "FY2025/FY2024 are the only years with a disclosed Tax line (FY2024's is a genuine nil, not a gap) - "
        "FY2023/FY2022/FY2021 show 'Loss before tax and loss for the year' as a single figure with no "
        "separate tax charge disclosed. FY2022 is the only year to separately disclose discontinued "
        "operations (a £3,150k loss); every other year's activities are entirely continuing operations. "
        "'Net fee and commission income' and 'Allowance for impairment loss' are not disclosed as their own "
        "subtotal/line in FY2021 - left blank rather than computed, since that year's own report doesn't "
        "present them that way."
    ),
    first_col_width=68,
    source_height=200,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
eq_headers = ["Share capital", "Contingent Capital Note", "Share option reserve", "Other equity instruments", "Retained earnings", "Total equity"]
eq_rows = [
    ("TOTAL", "At 31 December 2021", (40200, 4500, None, None, -27751, 16949)),
    ("DATA", "Loss for the year", (None, None, None, None, -11868, -11868)),
    ("DATA", "Release of contingent capital note", (None, -4500, None, None, None, -4500)),
    ("DATA", "Share capital issuance", (34500, None, None, None, None, 34500)),
    ("TOTAL", "At 31 December 2022", (74700, 0, None, None, -39619, 35081)),
    ("DATA", "Loss for the year", (None, None, None, None, -5710, -5710)),
    ("DATA", "Share capital issuance", (10000, None, None, None, None, 10000)),
    ("DATA", "Share-based payment", (None, None, 110, None, None, 110)),
    ("TOTAL", "At 31 December 2023", (84700, 0, 110, None, -45329, 39481)),
    ("DATA", "Loss for the year", (None, None, None, None, -2460, -2460)),
    ("DATA", "Share capital issuance", (40000, None, None, None, None, 40000)),
    ("DATA", "Share-based payment", (None, None, 326, None, None, 326)),
    ("TOTAL", "At 31 December 2024", (124700, 0, 436, 0, -47789, 77347)),
    ("DATA", "Profit for the year", (None, None, None, None, 3434, 3434)),
    ("DATA", "Share-based payment", (None, None, 420, None, None, 420)),
    ("DATA", "AT1 issuance", (None, None, None, 15023, None, 15023)),
    ("DATA", "AT1 note interest", (None, None, None, None, -347, -347)),
    ("TOTAL", "At 31 December 2025", (124700, 0, 856, 14676, -44355, 95877)),
]

bw.add_equity_changes_sheet(
    title="iFAST Global Bank Limited — Statement of Changes in Equity",
    subtitle="Solo basis, £'000 — read chronologically, oldest to newest",
    headers=eq_headers,
    rows=eq_rows,
    sources_text=statements_sources(
        "Equity reconciliation ladder: every year's closing balance ties exactly to both the next year's own "
        "reported opening balance and that year's own Balance Sheet Total equity - zero plug rows needed "
        "anywhere in this 5-year window, including through FY2022's 'Release of contingent capital note' "
        "(£4,500k, zeroing that reserve) - an easy-to-miss movement caught by reading the FY2023 Annual "
        "Report's own equity statement in full, which is also the only source disclosing FY2022's own "
        "detailed equity roll-forward (no standalone FY2022 Annual Report exists). One genuine, "
        "not-force-reconciled discrepancy: FY2022's 'Share capital issuance' is £34,500k per the Statement "
        "of Changes in Equity, but the pre-existing Cash Flow Statement's 'Proceeds from the issue of "
        "ordinary shares' for FY2022 is £30,000k - both are the Bank's own disclosed figures from the same "
        "Annual Report, reproduced as reported."
    ),
    first_col_width=44,
    source_height=210,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash outflows generated from operating activities", {}),
    ("DATA", "Profit/(Loss) before tax", {"FY2025": 3434, "FY2024": -2460, "FY2023": -5710, "FY2022": -11868, "FY2021": -3085}),
    ("SECTION", "Adjustment for non-cash items", {}),
    ("DATA", "Depreciation", {"FY2025": 397, "FY2024": 313, "FY2023": 323, "FY2022": 376, "FY2021": 363}),
    ("DATA", "Amortisation", {"FY2025": 149, "FY2024": 141, "FY2023": 12, "FY2022": 159, "FY2021": 635}),
    ("DATA", "Fair value (loss)/gain on derivatives", {"FY2025": -52, "FY2024": 194, "FY2023": -274, "FY2022": 178, "FY2021": 531}),
    ("DATA", "Net foreign exchange (gain)/loss", {"FY2025": -22, "FY2024": -332, "FY2023": 725, "FY2022": 209, "FY2021": -501}),
    ("DATA", "Finance costs on lease", {"FY2025": 14, "FY2024": 4, "FY2023": 8, "FY2022": 6, "FY2021": 174}),
    ("DATA", "Share option reserve", {"FY2025": 420, "FY2024": 326}),
    ("DATA", "Other non-cash items included in profit before tax", {"FY2025": 303, "FY2024": 179, "FY2023": 116, "FY2022": 3869, "FY2021": 7}),
    ("DATA", "Profit on sale of bonds", {"FY2025": -8, "FY2024": -2}),
    ("DATA", "Interest received", {"FY2021": -13}),
    ("DATA", "Interest paid", {"FY2021": 170}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Increase in loans to customers", {"FY2025": -55103, "FY2024": -25046}),
    ("DATA", "Increase in amounts due to customers", {"FY2025": 331049, "FY2024": 375082, "FY2023": 161254, "FY2022": 31320}),
    ("DATA", "Net (increase)/decrease in receivables", {"FY2025": -7962, "FY2024": -3886, "FY2023": -9207, "FY2022": -2025, "FY2021": -2477}),
    ("DATA", "Net (decrease)/increase in payables", {"FY2025": -674, "FY2024": -488, "FY2023": 3716, "FY2022": -1686, "FY2021": -4432}),
    ("DATA", "Purchase of assets at fair value through profit and loss", {"FY2023": -23924}),
    ("DATA", "Purchase of debt instruments at amortised cost", {"FY2023": -55440, "FY2022": -31954}),
    ("DATA", "Proceeds from sale of debt instruments at amortised cost", {"FY2023": 26720, "FY2022": 2108}),
    ("TOTAL", "Net inflows/(outflows) from operating activities", {"FY2025": 271945, "FY2024": 344025, "FY2023": 98319, "FY2022": -9308, "FY2021": -8628}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of debt instruments at amortised cost", {"FY2025": -679033, "FY2024": -381174}),
    ("DATA", "Proceeds from sale of debt instruments at amortised cost", {"FY2025": 456071, "FY2024": 122523}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -728, "FY2024": -19, "FY2023": -52, "FY2022": -268, "FY2021": -125}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -24, "FY2023": -438}),
    ("TOTAL", "Net outflows from investing activities", {"FY2025": -223714, "FY2024": -258670, "FY2023": -490, "FY2022": -268, "FY2021": -125}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Proceeds from the issue of ordinary shares", {"FY2024": 40000, "FY2023": 10000, "FY2022": 30000}),
    ("DATA", "Issue of AT1 Perpetual Note net of fees", {"FY2025": 15023}),
    ("DATA", "Payment of principal portion of lease liabilities", {"FY2025": -178, "FY2024": -331, "FY2023": -302, "FY2021": -730}),
    ("DATA", "Payment of principal and interest portion of lease liabilities", {"FY2022": 1107}),
    ("TOTAL", "Net inflows/(outflows) from financing activities", {"FY2025": 14845, "FY2024": 39669, "FY2023": 9698, "FY2022": 31107, "FY2021": -730}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 63076, "FY2024": 125024, "FY2023": 107527, "FY2022": 21530, "FY2021": -9483}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 330938, "FY2024": 205582, "FY2023": 74856, "FY2022": 53534, "FY2021": 62516}),
    ("DATA", "Effect of exchange rate fluctuations on cash and cash equivalents", {"FY2025": 22, "FY2024": 332, "FY2023": -725, "FY2022": -209, "FY2021": 501}),
    ("TOTAL", "Cash and cash equivalents at end of financial year", {"FY2025": 394036, "FY2024": 330938, "FY2023": 181658, "FY2022": 74856, "FY2021": 53534}),
]

bw.add_cash_flow_sheet(
    title="iFAST Global Bank Limited — Statement of Cash Flows",
    subtitle="iFAST Global Bank Limited (solo basis), £'000 unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=62,
    source_height=130,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
aq_rows = [
    ("SECTION", "Aggregate credit-risk exposure by IFRS 9 stage (cash balances, receivables, debt instruments, "
                "loans and advances to customers, derivatives)", {}),
    ("DATA", "Stage 1 gross exposure", {"FY2025": 896500, "FY2024": 609339, "FY2023": 261048, "FY2022": 111457, "FY2021": 53027}),
    ("DATA", "Stage 2 gross exposure", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Stage 3 gross exposure", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Total gross exposure", {"FY2025": 896500, "FY2024": 609339, "FY2023": 261048, "FY2022": 111457, "FY2021": 53027}),
    ("DATA", "Less: allowance for impairment", {"FY2025": -752, "FY2024": -449, "FY2023": -270, "FY2022": -151, "FY2021": -42}),
    ("TOTAL", "Net exposure", {"FY2025": 895748, "FY2024": 608890, "FY2023": 260778, "FY2022": 111306, "FY2021": 52985}),
    ("DATA", "ECL coverage ratio (allowance / gross exposure)", {"FY2025": "0.08%", "FY2024": "0.07%", "FY2023": "0.10%", "FY2022": "0.14%", "FY2021": "0.08%"}),
]

bw.add_asset_quality_sheet(
    title="iFAST Global Bank Limited — Asset Quality",
    subtitle="Solo basis, £'000. Entire book has sat in Stage 1 throughout FY2021-FY2025 - a genuine feature, "
              "not a gap.",
    rows=aq_rows,
    sources_text=(
        "Sources - iFAST Global Bank Limited's own 'maximum exposure to credit risk by class of financial "
        "asset' table (aggregates cash balances with central banks/due from banks, trade receivables, debt "
        "instruments, loans and advances to customers, and derivative financial instruments; excludes Money "
        "Market Funds, which sit within cash and cash equivalents but outside this note):\n"
        f"FY2025/FY2024: iFAST Global Bank Ltd. Annual Report 2025, p.58-59 (Note 27, Credit risk) — {AR25_URL}\n"
        f"FY2023: iFAST Global Bank Ltd. Annual Report 2023, p.58-59 (Note 29, Credit risk) — {AR23_URL}\n"
        f"FY2022: iFAST Global Bank Ltd. Annual Report 2023, p.59 (Note 29, Credit risk, FY2022 comparative "
        f"column) — {AR23_URL}\n"
        f"FY2021: iFAST Global Bank Ltd. Annual Report 2021, p.51 (Note 25, Credit risk) — {AR21_URL}\n"
        "The Bank's loan book is entirely business-to-business/short-tenor in nature; no Stage 2 or Stage 3 "
        "balance has existed in any of the 5 years covered by this workbook (confirmed by reading each note "
        "in full). Note that 'Loans and advances to customers' only exists as a distinct exposure class from "
        "FY2024 onward (see the Balance Sheet sheet's entity note) - it is already included within the "
        "aggregate figures above for the years in which it exists."
    ),
    first_col_width=64,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Solo basis, {unit}" if unit else "Solo basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=100)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 79319, "FY2024": 76953, "FY2023": 39032, "FY2022": 35017, "FY2021": 8530})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "20.2%", "FY2024": "28.1%", "FY2023": "36.3%", "FY2022": "40.7%", "FY2021": "14%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 93994, "FY2024": 76953, "FY2023": 39032, "FY2022": 35017, "FY2021": 13030})],
    p3_sources(),
    note="FY2021's Pillar 3 disclosure did not use the UK KM1 template; the Tier 1 capital figure is taken from "
         "the Leverage Ratio Common Disclosure table, and equals Total Own Funds as no Tier 2 capital was held.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "23.9%", "FY2024": "28.1%", "FY2023": "36.3%", "FY2022": "40.7%", "FY2021": "22%"})],
    p3_sources(),
    note="FY2021 figure is the 'Capital Adequacy Ratio' from the Own funds table, which equals the Tier 1 ratio "
         "as no Tier 2 capital was held that year.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 93994, "FY2024": 76953, "FY2023": 39032, "FY2022": 35017, "FY2021": 13030})],
    p3_sources(),
    note="FY2021 figure is 'Total Own funds' from the Own funds table (no Tier 2 capital held that year, so "
         "Total capital = Tier 1 capital).",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "23.9%", "FY2024": "28.1%", "FY2023": "36.3%", "FY2022": "40.7%", "FY2021": "22%"})],
    p3_sources(),
    note="FY2021 figure is the 'Capital Adequacy Ratio' from the Own funds table.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": 392607, "FY2024": 273772, "FY2023": 107539, "FY2022": 86029, "FY2021": 58982})],
    p3_sources(),
)

rwa_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 338558, "FY2024": 237670, "FY2023": 80249, "FY2022": 47985}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 405, "FY2024": 152, "FY2023": 534, "FY2022": 535}),
    ("DATA", "Of which credit valuation adjustment (CVA)", {"FY2025": 590, "FY2024": 301, "FY2023": 778, "FY2022": 779}),
    ("DATA", "Market risk (position, FX and commodities)", {"FY2025": 36743, "FY2024": 15850, "FY2023": 4524, "FY2022": 1184}),
    ("DATA", "Operational risk", {"FY2025": 16311, "FY2024": 19746, "FY2023": 21454, "FY2022": 35546}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 392607, "FY2024": 273718, "FY2023": 107539, "FY2022": 86029}),
]

bw.add_rwa_breakdown_sheet(
    title="iFAST Global Bank Limited — RWA Breakdown",
    subtitle="Solo basis, £'000. FY2021 not publicly disclosed at category level.",
    rows=rwa_rows,
    sources_text=(
        "Sources - iFAST Global Bank Limited's own Table UK OV1 (Overview of risk weighted exposure amounts):\n"
        f"FY2025/FY2024: iFAST Global Bank Limited Pillar 3 Disclosures 2025, p.21 (Table 4: UK OV1) — {P3_25_URL}\n"
        f"FY2023/FY2022: iFAST Global Bank Limited Pillar 3 Disclosures 2023, p.15 (Table 4: UK OV1) — {P3_23_URL}\n"
        "FY2021: not publicly disclosed at category level — the FY2021 (BFC Bank Limited) Pillar 3 Disclosures "
        "document's Section 6.3 'Pillar 1 capital requirement' promises a category breakdown but the table "
        "itself is absent from the published document (confirmed by reading the full section) - only the "
        f"aggregate Total RWA figure exists that year (see the Total RWAs sheet) — {P3_21_URL}\n"
        "Genuine, not-force-reconciled discrepancy: the FY2025 Pillar 3 document's own FY2024 comparative "
        "differs slightly between its two tables - this OV1 table's FY2024 Total is £273,718k, while the "
        "same document's Table 1 (UK KM1) FY2024 Total is £273,772k (used on the Total RWAs sheet for "
        "consistency with that sheet's other years); both are the Bank's own disclosed figures, reproduced "
        "as reported rather than reconciled."
    ),
    first_col_width=56,
    source_height=200,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks (£'000)", {"FY2025": 868024, "FY2024": 501384, "FY2023": 136351, "FY2022": 74160, "FY2021": 68805}),
        ("Regulatory leverage ratio (%)", {"FY2025": "11.0%", "FY2024": "15.4%", "FY2023": "29.0%", "FY2022": "47.3%", "FY2021": "19%"}),
    ],
    p3_sources(),
    note="FY2021 exposure measure is the 'Leverage ratio total exposure measure' and ratio is the 'Regulatory "
         "Leverage Ratio' from the Leverage Ratio Common Disclosure table (pre-KM1-template disclosure format).",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA) (£'000)", {"FY2025": 279890, "FY2024": 301040, "FY2023": 180356, "FY2022": 65205, "FY2021": 26728}),
        ("Total net cash outflows, adjusted value (£'000)", {"FY2025": 52750, "FY2024": 33002, "FY2023": 24764, "FY2022": 5258, "FY2021": 2411}),
        ("Liquidity coverage ratio (%)", {"FY2025": "531%", "FY2024": "912%", "FY2023": "728%", "FY2022": "1240%", "FY2021": "1109%"}),
    ],
    p3_sources(),
    note="FY2021's (BFC Bank Limited) Pillar 3 Disclosures disclose the liquidity table in the Market Risk section "
         "(p.18): liquidity buffer/HQLA £26,728k, total net cash outflows £2,411k and LCR 1,109%. These are the "
         "Bank's own figures; the report states that BFC Bank refers to the renamed iFAST Global Bank Limited.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding (£'000)", {"FY2025": 835880, "FY2024": 555781, "FY2023": 173025, "FY2022": 92023, "FY2021": "Not disclosed"}),
        ("Total required stable funding (£'000)", {"FY2025": 437854, "FY2024": 215858, "FY2023": 50090, "FY2022": 22101, "FY2021": "Not disclosed"}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "190.9%", "FY2024": "257.5%", "FY2023": "345.4%", "FY2022": "416.4%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="FY2021 is genuinely not disclosed — see the LCR sheet's note; the FY2021 Pillar 3 document predates "
         "this bank's NSFR/LCR disclosure section entirely.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "MREL is not disclosed in any of the 5 years' Pillar 3 documents — iFAST Global "
              "Bank Limited (formerly BFC Bank Limited) is a small bank below the threshold at which the Bank "
              "of England sets an MREL requirement above minimum capital requirements."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1052008, "FY2024": 700615, "FY2023": 288288, "FY2022": 119485, "FY2021": 71736}),
        ("Loans and advances to customers", {"FY2025": 80119, "FY2024": 25046}),
        ("Due to customers", {"FY2025": 941013, "FY2024": 609964, "FY2023": 234882, "FY2022": 73627, "FY2021": 42307}),
        ("Total equity", {"FY2025": 95877, "FY2024": 77347, "FY2023": 39481, "FY2022": 35081, "FY2021": 16949}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income/(expense)", {"FY2025": 10911, "FY2024": 5340, "FY2023": 1701, "FY2022": 121, "FY2021": -450}),
        ("Net operating income", {"FY2025": 21232, "FY2024": 11671, "FY2023": 8119, "FY2022": 6644, "FY2021": 7049}),
        ("Total operating expenses", {"FY2025": -19378, "FY2024": -14131, "FY2023": -13829, "FY2022": -15632, "FY2021": -10134}),
        ("Profit/(loss) for the year", {"FY2025": 3434, "FY2024": -2460, "FY2023": -5710, "FY2022": -11868, "FY2021": -3085}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Total equity", {"FY2025": 95877, "FY2024": 77347, "FY2023": 39481, "FY2022": 35081, "FY2021": 16949}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net inflows/(outflows) from operating activities", {"FY2025": 271945, "FY2024": 344025, "FY2023": 98319, "FY2022": -9308, "FY2021": -8628}),
        ("Net outflows from investing activities", {"FY2025": -223714, "FY2024": -258670, "FY2023": -490, "FY2022": -268, "FY2021": -125}),
        ("Net inflows/(outflows) from financing activities", {"FY2025": 14845, "FY2024": 39669, "FY2023": 9698, "FY2022": 31107, "FY2021": -730}),
        ("Cash and cash equivalents at end of financial year", {"FY2025": 394036, "FY2024": 330938, "FY2023": 181658, "FY2022": 74856, "FY2021": 53534}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "20.2%", "FY2024": "28.1%", "FY2023": "36.3%", "FY2022": "40.7%", "FY2021": "14%"}),
        ("Tier 1 Ratio", {"FY2025": "23.9%", "FY2024": "28.1%", "FY2023": "36.3%", "FY2022": "40.7%", "FY2021": "22%"}),
        ("Total Capital Ratio", {"FY2025": "23.9%", "FY2024": "28.1%", "FY2023": "36.3%", "FY2022": "40.7%", "FY2021": "22%"}),
        ("Leverage Ratio", {"FY2025": "11.0%", "FY2024": "15.4%", "FY2023": "29.0%", "FY2022": "47.3%", "FY2021": "19%"}),
        ("LCR", {"FY2025": "531%", "FY2024": "912%", "FY2023": "728%", "FY2022": "1240%", "FY2021": "1109%"}),
        ("NSFR", {"FY2025": "190.9%", "FY2024": "257.5%", "FY2023": "345.4%", "FY2022": "416.4%", "FY2021": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. FY2023 cash figures use the originally-reported "
         "(pre-restatement) balances — see the Cash Flow Statement sheet's note. All capital/liquidity ratios "
         "fell sharply from FY2021-2022 to FY2025 as the bank scaled its balance sheet roughly 7x following the "
         "2022 iFAST Corporation acquisition and rebrand from BFC Bank.",
)

bw.save("/Users/armaan/code/katalysis/banks/IFAST GLOBAL BANK LIMITED FINANCIALS.xlsx")
