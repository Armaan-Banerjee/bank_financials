import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2021_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Co-Annual-Report-2021.pdf"
AR2022_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Co-2022-Annual-Report-and-Financial-Statements.pdf"
AR2023_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Co-Annual-Report-and-Financial-Statements-2023.pdf"
AR2024_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Bank-Annual-Report-and-Financial-Statements-2024.pdf"
AR2025_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden_Bank_Annual_Report_2025_2026-06-09-100801_cggc.pdf"

P3_2021_URL = "https://hampdenandco.com/content/hampden/content/Hampden-Co-plc-2021-Pillar-3-Disclosures-FINAL.pdf"
P3_2022_URL = "https://hampdenandco.com/content/hampden/content/Hampden-Co-2022-Pillar-3-Disclosures.pdf"
P3_2023_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Co-plc-2023-Pillar-3-Disclosures.pdf"

ENTITY_NOTE = (
    "Hampden & Co Plc (Companies House SC386922, FRN 606934) is a small Edinburgh-based private/relationship "
    "banking group; it began trading as 'Hampden Bank' during 2025/2026 but the legal entity name and company "
    "number are unchanged - confirmed via the entity's own 'about us' page. The cash flow statement's presentation "
    "structure genuinely changes mid-series: FY2021-FY2022 present operating activities as a single reconciliation "
    "block; FY2023 onward split it into a 'Cash generated from operations' subtotal followed by a separate "
    "'Changes in operating assets and liabilities' block and a final operating subtotal (with 'Tax paid' appearing "
    "as its own line from FY2024). Each year is kept on its own as-disclosed structure rather than forced into a "
    "single row set. All comparative-year figures cross-checked against each year's own originally-published "
    "report - no restatements found anywhere in the 5-year window."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Hampden & Co Plc's own Statement of Cash Flows, as filed with Companies House:\n"
    f"FY2025: Hampden Bank Annual Report and Financial Statements 2025, p.49 (Statement of cash flows) - {AR2025_URL}\n"
    f"FY2024: Hampden Bank Annual Report and Financial Statements 2024, p.51 (Statement of cash flows) - {AR2024_URL}\n"
    f"FY2023: Hampden & Co Plc Annual Report and Financial Statements 2023, p.44 (Statement of cash flows) - {AR2023_URL}\n"
    f"FY2022: Hampden & Co Plc Annual Report and Financial Statements 2022, p.45 (Statement of cash flows) - {AR2022_URL}\n"
    f"FY2021: Hampden & Co Plc Annual Report and Financial Statements 2021, p.56 (Statement of cash flows) - {AR2021_URL}\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Hampden & Co Plc Pillar 3 Disclosures (Article 447/UK KM1 Key Metrics table unless noted):\n"
        f"FY2023/FY2022: Pillar 3 Disclosures for the year ended 31 December 2023, p.5-6 (UK KM1 Key metrics table) - {P3_2023_URL}\n"
        f"FY2021: Pillar 3 Disclosures for the year ended 31 December 2021 (pre-KM1 format), p.15 'Table 4: Capital resources' "
        f"and p.18 leverage ratio and p.26 'Table 15: Liquidity coverage ratio' - {P3_2021_URL}\n"
        "FY2024/FY2025: no standalone Pillar 3 document was found published for either year (last located Pillar 3 disclosure "
        "covers FY2023) - Total Capital Ratio only is sourced from each year's own Annual Report Key Performance Indicators "
        f"table instead (FY2024 AR p.7, FY2025 AR p.11) - {AR2024_URL} / {AR2025_URL}. All other metrics are not publicly "
        "disclosed for FY2024/FY2025."
    )


bw = BankWorkbook(bank_name="Hampden & Co Plc", years=YEARS, year_label=YEAR_LABEL, header_color="32ADB6")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {
        "FY2025": 6953, "FY2024": 8181, "FY2023": 9143, "FY2022": 2045, "FY2021": -2970,
    }),
    ("DATA", "Net losses/(gains) from derivatives and hedge accounting", {
        "FY2025": 111, "FY2024": 203, "FY2023": 303, "FY2022": -820,
    }),
    ("DATA", "Depreciation and amortisation", {
        "FY2025": 2672, "FY2024": 1258, "FY2023": 1038, "FY2022": 945, "FY2021": 1176,
    }),
    ("DATA", "Equity settled share-based payments", {
        "FY2025": 145, "FY2024": 176, "FY2023": 186, "FY2022": 840, "FY2021": 1042,
    }),
    ("DATA", "Dividend equivalent on share options", {
        "FY2025": -182, "FY2024": -91,
    }),
    ("DATA", "Cancellation of share options", {
        "FY2023": -688,
    }),
    ("DATA", "Impairment (credit)/charge for the year", {
        "FY2025": -107, "FY2024": 12, "FY2023": 103, "FY2022": 29, "FY2021": -5,
    }),
    ("DATA", "(Increase) in prepayments and accrued income", {
        "FY2021": -185,
    }),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {
        "FY2021": 353,
    }),
    ("DATA", "(Increase) in loans and advances to clients and banks", {
        "FY2021": -132311,
    }),
    ("DATA", "Increase in deposits by clients and banks", {
        "FY2021": 194668,
    }),
    ("DATA", "Decrease in other assets", {
        "FY2021": 3,
    }),
    ("DATA", "(Decrease)/increase in other liabilities and provisions", {
        "FY2021": -22,
    }),
    ("DATA", "Elimination of foreign exchange differences", {
        "FY2022": 8, "FY2021": -9,
    }),
    ("TOTAL", "Cash generated from/(used in) operations", {
        "FY2025": 9592, "FY2024": 9739, "FY2023": 10085,
    }),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Increase/(decrease) in prepayments and accrued income", {
        "FY2025": -1271, "FY2024": -441, "FY2023": 421, "FY2022": -205,
    }),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {
        "FY2025": -942, "FY2024": 25, "FY2023": 6, "FY2022": 1560,
    }),
    ("DATA", "Decrease/(increase) in loans and advances to clients and banks", {
        "FY2025": 34430, "FY2024": -57243, "FY2023": -93474, "FY2022": -43506,
    }),
    ("DATA", "Increase in deposits from clients/by clients and banks", {
        "FY2025": 133690, "FY2024": 134544, "FY2023": 67050, "FY2022": 90941,
    }),
    ("DATA", "(Increase)/decrease in other assets", {
        "FY2025": -49, "FY2024": 5, "FY2023": 1859, "FY2022": -2160,
    }),
    ("DATA", "(Decrease)/increase in other liabilities and provisions", {
        "FY2025": -285, "FY2024": 117, "FY2023": -56, "FY2022": 405,
    }),
    ("TOTAL", "Cash generated from/(used in) operating activities", {
        "FY2025": 175165, "FY2024": 86746, "FY2023": -14109,
    }),
    ("DATA", "Tax paid/(income tax received)", {
        "FY2025": -131, "FY2024": -870, "FY2021": 0,
    }),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2025": 175034, "FY2024": 85876, "FY2023": -14109, "FY2022": 50082, "FY2021": 61740,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities", {
        "FY2025": -853557, "FY2024": -414862, "FY2023": -67066,
    }),
    ("DATA", "Sales and maturities of debt securities", {
        "FY2025": 715908, "FY2024": 257177,
    }),
    ("DATA", "Purchase of property, plant and equipment", {
        "FY2025": -1848, "FY2024": -902, "FY2023": -77, "FY2022": -86,
    }),
    ("DATA", "Purchases/development of intangible assets", {
        "FY2025": -2736, "FY2024": -5995, "FY2023": -2184, "FY2022": -891, "FY2021": -1145,
    }),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": -142233, "FY2024": -164582, "FY2023": -69327, "FY2022": -977, "FY2021": -1145,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of lease liabilities", {
        "FY2025": -74, "FY2024": -500, "FY2023": -427, "FY2022": -378, "FY2021": -445,
    }),
    ("DATA", "Proceeds from issue of shares", {
        "FY2023": 2059, "FY2022": 8000, "FY2021": 8000,
    }),
    ("DATA", "Direct costs of share issuance", {
        "FY2023": -92, "FY2022": -154, "FY2021": -109,
    }),
    ("DATA", "Equity dividends paid", {
        "FY2025": -3024, "FY2024": -1512,
    }),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2025": -3098, "FY2024": -2012, "FY2023": 1540, "FY2022": 7468, "FY2021": 7446,
    }),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {
        "FY2025": 29703, "FY2024": -80718, "FY2023": -81896, "FY2022": 56573, "FY2021": 68041,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 125315, "FY2024": 207363, "FY2023": 294851, "FY2022": 228768, "FY2021": 160960,
    }),
    ("DATA", "Effects of foreign exchange rate changes on cash and cash equivalents", {
        "FY2025": -667, "FY2024": -1330, "FY2023": -5592, "FY2022": 9510, "FY2021": -233,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 154351, "FY2024": 125315, "FY2023": 207363, "FY2022": 294851, "FY2021": 228768,
    }),
]

bw.add_cash_flow_sheet(
    title="Hampden & Co Plc — Statement of Cash Flows",
    subtitle="Company-only statement, as filed with Companies House",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=130)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2023": 74173, "FY2022": 65731, "FY2021": 55264,
    })],
    p3_sources(),
    note="No Additional Tier 1 or Tier 2 capital any year - CET1 = Tier 1 = Total Capital throughout. "
         "Not disclosed for FY2024/FY2025 (no standalone Pillar 3 document located for either year).",
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
    })],
    p3_sources(),
    note="Not disclosed for FY2024/FY2025 (no standalone Pillar 3 document located for either year); "
         "only the aggregate Total Capital Ratio is given in those years' own Annual Reports.",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {
        "FY2023": 74173, "FY2022": 65731, "FY2021": 55264,
    })],
    p3_sources(),
    note="No AT1 capital any year - Tier 1 = CET1 = Total Capital throughout. Not disclosed for FY2024/FY2025.",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
    })],
    p3_sources(),
    note="Not disclosed for FY2024/FY2025 (no standalone Pillar 3 document located for either year).",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {
        "FY2023": 74173, "FY2022": 65731, "FY2021": 55264,
    })],
    p3_sources(),
    note="Not disclosed in £'000 terms for FY2024/FY2025 - only the ratio (below) is given.",
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2025": "17%", "FY2024": "17%", "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
    })],
    p3_sources(),
    note="FY2024/FY2025 sourced from each year's own Annual Report Key Performance Indicators table (the only "
         "capital metric given there) rather than a standalone Pillar 3 document - none was found published for "
         "either year.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {
        "FY2023": 361317, "FY2022": 316422, "FY2021": 285422,
    })],
    p3_sources(),
    note="Not disclosed for FY2024/FY2025 (no standalone Pillar 3 document located for either year).",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio (excluding claims on central banks, FY2022-FY2023)", {
        "FY2023": "8.36%", "FY2022": "8.72%",
    }),
     ("Leverage ratio (FY2021 basis, as originally disclosed)", {
        "FY2021": "7%",
    })],
    p3_sources(),
    note="FY2021's pre-UK-KM1-format disclosure does not specify whether central-bank claims are excluded - shown "
         "on its own row rather than merged with the later, explicitly-labelled basis. Not disclosed for "
         "FY2024/FY2025.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (12-month average)", {
        "FY2023": "262%", "FY2022": "213%",
    }),
     ("Liquidity Coverage Ratio (point-in-time, FY2021 basis)", {
        "FY2021": "180%",
    })],
    p3_sources(),
    note="FY2021's disclosure predates the UK KM1 format and does not state an averaging basis (later years use "
         "a 12-month average per KM1) - shown on its own row rather than assumed equivalent. Not disclosed for "
         "FY2024/FY2025.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (4-quarter average)", {
        "FY2023": "186%", "FY2022": "186%",
    })],
    p3_sources(),
    note="Not disclosed for FY2021 - the Bank's own FY2021 Pillar 3 report contains no NSFR section at all, "
         "consistent with the UK's NSFR reporting requirement only commencing during 2022 for firms of this size "
         "(the same commencement pattern already seen at Ghana International Bank). Not disclosed for "
         "FY2024/FY2025.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "Not publicly disclosed for any year - no MREL-related content appears in any Pillar 3 "
                       "document reviewed (FY2021-FY2023); Hampden & Co Plc does not appear to be a UK "
                       "resolution entity subject to a standalone MREL requirement.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": 175034, "FY2024": 85876, "FY2023": -14109, "FY2022": 50082, "FY2021": 61740,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": -142233, "FY2024": -164582, "FY2023": -69327, "FY2022": -977, "FY2021": -1145,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": -3098, "FY2024": -2012, "FY2023": 1540, "FY2022": 7468, "FY2021": 7446,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 154351, "FY2024": 125315, "FY2023": 207363, "FY2022": 294851, "FY2021": 228768,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {
            "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
        }),
        ("Tier 1 Ratio", {
            "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
        }),
        ("Total Capital Ratio", {
            "FY2025": "17%", "FY2024": "17%", "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
        }),
        ("LCR", {
            "FY2023": "262%", "FY2022": "213%", "FY2021": "180%",
        }),
        ("NSFR", {
            "FY2023": "186%", "FY2022": "186%",
        }),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. FY2024/FY2025 ratios other than Total Capital Ratio "
         "are blank - no standalone Pillar 3 document was found published for either year.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HAMPDEN & CO FINANCIALS.xlsx")
