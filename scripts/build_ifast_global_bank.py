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
        ("Total high-quality liquid assets (HQLA) (£'000)", {"FY2025": 279890, "FY2024": 301040, "FY2023": 180356, "FY2022": 65205, "FY2021": "Not disclosed"}),
        ("Total net cash outflows, adjusted value (£'000)", {"FY2025": 52750, "FY2024": 33002, "FY2023": 24764, "FY2022": 5258, "FY2021": "Not disclosed"}),
        ("Liquidity coverage ratio (%)", {"FY2025": "531%", "FY2024": "912%", "FY2023": "728%", "FY2022": "1240%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="The FY2021 (BFC Bank Limited) Pillar 3 Disclosures document has no LCR/liquidity section at all — only "
         "Leverage, Asset Encumbrance, Own funds, Capital Adequacy and Remuneration are covered — so FY2021 is "
         "genuinely not disclosed, not merely omitted from this workbook.",
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
        ("LCR", {"FY2025": "531%", "FY2024": "912%", "FY2023": "728%", "FY2022": "1240%", "FY2021": "Not disclosed"}),
        ("NSFR", {"FY2025": "190.9%", "FY2024": "257.5%", "FY2023": "345.4%", "FY2022": "416.4%", "FY2021": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. FY2023 cash figures use the originally-reported "
         "(pre-restatement) balances — see the Cash Flow Statement sheet's note. All capital/liquidity ratios "
         "fell sharply from FY2021-2022 to FY2025 as the bank scaled its balance sheet roughly 7x following the "
         "2022 iFAST Corporation acquisition and rebrand from BFC Bank.",
)

bw.save("/Users/armaan/code/katalysis/banks/IFAST GLOBAL BANK LIMITED FINANCIALS.xlsx")
