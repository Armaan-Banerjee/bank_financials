import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Calendar year-end (31 December), full 5 years FY2021-FY2025.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.charitybank.org/wp-content/uploads/2026/06/Charity-Bank-2025-Annual-Report-signed.pdf"
AR2024_URL = "https://www.charitybank.org/wp-content/uploads/2025/06/Charity-Bank-2024-Annual-Report-signed.pdf"
AR2023_URL = "https://www.charitybank.org/wp-content/uploads/2024/10/Charity-Bank-Annual-Accounts-2023.pdf"
AR2022_CH_URL = ("https://find-and-update.company-information.service.gov.uk/company/04330018/filing-history/"
                  "MzM4MjU0NDA3NWFkaXF6a2N4/document?format=pdf&download=0")
AR2021_CH_URL = ("https://find-and-update.company-information.service.gov.uk/company/04330018/filing-history/"
                  "MzM0MTk3OTg0MGFkaXF6a2N4/document?format=pdf&download=0")

P3_2023_URL = ("https://web.archive.org/web/20250809165738/https://www.charitybank.org/wp-content/uploads/2024/10/"
               "PILLAR-3-disclosures-2023.pdf")
P3_2022_URL = ("https://web.archive.org/web/20250805161700/https://www.charitybank.org/wp-content/uploads/2024/10/"
               "PILLAR-3-disclosures-2022-FINAL.pdf")
P3_2021_URL = ("https://web.archive.org/web/20250726224104/https://www.charitybank.org/wp-content/uploads/2024/10/"
               "PILLAR-3-disclosures-2021-Final.pdf")

ENTITY_NOTE = (
    "ENTITY NOTE: The Charity Bank Limited (Companies House 04330018, FRN 207701) matches Banks List 2608.xlsx "
    "exactly - a wholly UK-owned, standalone entity with no parent-subsidiary complications. Charity Bank "
    "publishes a full Statement of Cash Flows every year (no FRS 101/102 exemption). Its FY2021 and FY2022 "
    "Companies House filings are fully scanned/image-only PDFs (no text layer) - OCR'd with tesseract and every "
    "figure visually cross-checked against a rendered page image at 400dpi (one apparently ambiguous OCR read, "
    "'depreciation of property and equipment' for FY2021, was confirmed as 59 by direct visual inspection, not "
    "the alternative misreading). All 5 years' own primary figures were cross-checked against their appearance "
    "as the following year's comparative column and match exactly - no source-document arithmetic errors found."
)

PILLAR3_NOTE = (
    "PILLAR 3 NOTE: Charity Bank published an annual standalone Pillar 3 disclosure document every year through "
    "the FY2023 edition (retrieved via the Wayback Machine - the current live site no longer links to any Pillar "
    "3 document, only Annual Reports). No FY2024 or FY2025 edition has been published anywhere as of the "
    "research date. Charity Bank's own FY2023 Annual Report (p.35) states it 'was accepted into the Small "
    f"Domestic Deposit Taker (SDDT) regime in January 2024' ({AR2023_URL}) - noted as context for when the "
    "standalone Pillar 3 disclosures stopped, though no document explicitly states SDDT status as the reason "
    "Pillar 3 publication ceased, so this is not asserted as a confirmed causal link. For FY2024 and FY2025, "
    "capital amounts (Tier 1/Tier 2/Total capital, £), RWAs, leverage exposure, and CET1/Total Capital/Leverage "
    "ratios were instead sourced from the 'Capital risk' section of each year's own Annual Report (Strategic "
    "Report and Note 28) - the Annual Reports do not disclose LCR, NSFR, or MREL at all, so those sheets are "
    "blank for FY2024-FY2025 (not a transcription gap - genuinely not published anywhere)."
)

LEVERAGE_BASIS_NOTE = (
    "LEVERAGE RATIO BASIS NOTE: the FY2021 Pillar 3 disclosure's own leverage ratio calculation (Tier 1 capital "
    "÷ [total balance sheet assets + addbacks - intangibles + 10% of off-balance-sheet commitments]) does not "
    "show an explicit deduction for claims on central banks, whereas the FY2022-FY2025 figures are explicitly "
    "computed on a 'total exposure measure excluding claims on central banks' basis (per the UK KM1 Pillar 3 "
    "template / each Annual Report's own definition). FY2021 (7.72%) is therefore likely not on a directly "
    "comparable basis to FY2022 onward (8.39%-10.39%) - shown exactly as each year's own source states it, not "
    "blended or recalculated."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are The Charity Bank Limited's own Cash Flow Statement, £'000:\n"
    f"FY2025: Charity Bank 2025 Annual Report, p.54 (Cash Flow Statement) - {AR2025_URL}\n"
    f"FY2024: Charity Bank 2024 Annual Report, p.52 (Cash Flow Statement) - {AR2024_URL}\n"
    f"FY2023: Charity Bank Annual Report 2023, p.54 (Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2022: The Charity Bank Limited Annual Report for the year ended 31 December 2022 (Companies House filing, "
    f"17 Jun 2023), p.42 (Cash Flow Statement) - scanned/image-only, OCR'd and visually cross-checked - {AR2022_CH_URL}\n"
    f"FY2021: The Charity Bank Limited Annual Report for the year ended 31 December 2021 (Companies House filing), "
    f"p.38 (Cash Flow Statement) - scanned/image-only, OCR'd and visually cross-checked - {AR2021_CH_URL}\n"
    "All 5 years' own primary figures cross-checked and tie exactly against their appearance as the following "
    "year's comparative column (e.g. FY2021's own £2,878k operating-adjustments subtotal matches the FY2022 "
    "report's own FY2021 comparative exactly).\n\n"
    + ENTITY_NOTE
)


def p3_sources(page_2025="93 (Note 28) / 32 (Strategic Report)", page_2024="91 (Note 28) / 34 (Strategic Report)",
               page_2023="14 (Template UK KM1)", page_2022="14-15 (Template UK KM1, FY2022 column)",
               page_2021="15 (Own Funds / Key CRD IV Ratios)"):
    return (
        "Sources - The Charity Bank Limited entity-level Pillar 3 / regulatory capital basis:\n"
        f"FY2025: Charity Bank 2025 Annual Report, p.{page_2025} - {AR2025_URL}\n"
        f"FY2024: Charity Bank 2024 Annual Report, p.{page_2024} - {AR2024_URL}\n"
        f"FY2023: Charity Bank Pillar 3 Disclosures 2023, p.{page_2023} - {P3_2023_URL}\n"
        f"FY2022: Charity Bank Pillar 3 Disclosures 2022, p.{page_2022} - {P3_2022_URL}\n"
        f"FY2021: Charity Bank Pillar 3 Disclosures 2021, p.{page_2021} - {P3_2021_URL}\n\n"
        + PILLAR3_NOTE
    )


bw = BankWorkbook(bank_name="The Charity Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="285943")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {
        "FY2025": 3724, "FY2024": 6590, "FY2023": 8990, "FY2022": 2716, "FY2021": 944,
    }),
    ("DATA", "Interest expense", {
        "FY2025": 13398, "FY2024": 12537, "FY2023": 8026, "FY2022": 2822, "FY2021": 1602,
    }),
    ("DATA", "Depreciation of property and equipment", {
        "FY2025": 102, "FY2024": 45, "FY2023": 56, "FY2022": 61, "FY2021": 59,
    }),
    ("DATA", "Amortisation of intangible assets", {
        "FY2025": 151, "FY2024": 154, "FY2023": 163, "FY2022": 164, "FY2021": 166,
    }),
    ("DATA", "Depreciation of right-of-use asset", {
        "FY2025": 143, "FY2024": 192, "FY2023": 193, "FY2022": 199, "FY2021": 198,
    }),
    ("DATA", "Movement in impairment", {
        "FY2025": -106, "FY2024": -227, "FY2023": -367, "FY2022": 1057, "FY2021": -91,
    }),
    ("DATA", "Corporation tax paid", {
        "FY2025": -1206, "FY2024": -2274,
    }),
    ("TOTAL", "Adjustments to reconcile net profit to cash flow generated from operating activities", {
        "FY2025": 16206, "FY2024": 17017, "FY2023": 17061, "FY2022": 7019, "FY2021": 2878,
    }),

    ("SECTION", "Net increase in assets relating to operating activities", {}),
    ("DATA", "Loans and advances to customers", {
        "FY2025": -32043, "FY2024": -45526, "FY2023": -11550, "FY2022": -35715, "FY2021": -31665,
    }),
    ("DATA", "Financial assets", {
        "FY2025": -18309, "FY2024": 1811, "FY2023": 2113, "FY2022": 6103, "FY2021": 4723,
    }),
    ("DATA", "Other assets", {
        "FY2025": 78, "FY2024": 93, "FY2023": -139, "FY2022": -145, "FY2021": 526,
    }),
    ("DATA", "Movement in prepayments", {
        "FY2025": -193, "FY2024": -170, "FY2023": -46, "FY2022": -105, "FY2021": 12,
    }),
    ("TOTAL", "Net increase in assets relating to operating activities", {
        "FY2025": -50467, "FY2024": -43792, "FY2023": -9622, "FY2022": -29862, "FY2021": -26404,
    }),

    ("SECTION", "Net increase in liabilities relating to operating activities", {}),
    ("DATA", "Due to customers", {
        "FY2025": 34566, "FY2024": 44212, "FY2023": 29128, "FY2022": 41264, "FY2021": 31312,
    }),
    ("DATA", "Interest paid", {
        "FY2025": -13201, "FY2024": -12422, "FY2023": -7961, "FY2022": -2744, "FY2021": -1531,
    }),
    ("DATA", "Deferred income", {
        "FY2025": -105, "FY2024": 4, "FY2023": 21, "FY2022": -58, "FY2021": -45,
    }),
    ("DATA", "Movement in accruals and accrued interest", {
        "FY2025": -425, "FY2024": 377, "FY2023": 37, "FY2022": -24, "FY2021": 118,
    }),
    ("DATA", "Other liabilities", {
        "FY2025": -84, "FY2024": 1001, "FY2023": -1903, "FY2022": 358, "FY2021": 1586,
    }),
    ("TOTAL", "Net increase in liabilities relating to operating activities", {
        "FY2025": 20751, "FY2024": 33172, "FY2023": 19322, "FY2022": 38796, "FY2021": 31440,
    }),

    ("TOTAL", "Net cash (outflow)/inflow from operating activities", {
        "FY2025": -13510, "FY2024": 6397, "FY2023": 26761, "FY2022": 15953, "FY2021": 7914,
    }),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of fixed assets", {
        "FY2025": -47, "FY2024": -236, "FY2023": -34, "FY2022": -14, "FY2021": -66,
    }),
    ("DATA", "Proceeds from sale of fixed assets", {
        "FY2022": 0, "FY2021": 1,
    }),
    ("TOTAL", "Net cash outflow from investing activities", {
        "FY2025": -47, "FY2024": -236, "FY2023": -34, "FY2022": -14, "FY2021": -65,
    }),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Principal elements of lease payment", {
        "FY2025": -119, "FY2024": -167, "FY2023": -152, "FY2022": -147, "FY2021": -164,
    }),
    ("DATA", "Proceeds from issue of share capital", {
        "FY2025": 0, "FY2024": 400, "FY2023": 1712, "FY2022": 550, "FY2021": 4900,
    }),
    ("DATA", "Proceeds from issue of subordinated loan stock", {
        "FY2025": 200, "FY2024": 1170, "FY2023": 0, "FY2022": 1000, "FY2021": 1310,
    }),
    ("DATA", "Interest on subordinated loan stock", {
        "FY2025": -188, "FY2024": -80, "FY2023": -65, "FY2022": -78, "FY2021": -71,
    }),
    ("DATA", "Dividends paid to shareholders", {
        "FY2025": -988, "FY2024": -1552,
    }),
    ("TOTAL", "Net cash (outflow)/inflow from financing activities", {
        "FY2025": -1095, "FY2024": -229, "FY2023": 1495, "FY2022": 1325, "FY2021": 5975,
    }),

    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2025": -14652, "FY2024": 5932, "FY2023": 28222, "FY2022": 17264, "FY2021": 13824,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 97352, "FY2024": 91420, "FY2023": 63198, "FY2022": 45934, "FY2021": 32110,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 82700, "FY2024": 97352, "FY2023": 91420, "FY2022": 63198, "FY2021": 45934,
    }),
]

bw.add_cash_flow_sheet(
    title="The Charity Bank Limited — Cash Flow Statement",
    subtitle="Entity-level basis, £'000",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=160,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=48, source_height=140)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2025": 41644, "FY2024": 37540, "FY2023": 30701, "FY2022": 26146, "FY2021": 24522,
    })],
    p3_sources(),
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2025": "17.33%", "FY2024": "16.67%", "FY2023": "16.15%", "FY2022": "15.05%", "FY2021": "16.01%",
    })],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {
        "FY2025": 41644, "FY2024": 37540, "FY2023": 30701, "FY2022": 26146, "FY2021": 24522,
    })],
    p3_sources(),
    note="Tier 1 capital equals CET1 capital in every year shown - Charity Bank has no Additional Tier 1 (AT1) "
         "instruments.",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2025": "17.33%", "FY2024": "16.67%", "FY2023": "16.15%", "FY2022": "15.05%", "FY2021": "16.01%",
    })],
    p3_sources(),
    note="Equal to the CET1 ratio every year shown - no Additional Tier 1 (AT1) instruments.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {
        "FY2025": 47044, "FY2024": 42376, "FY2023": 33541, "FY2022": 29878, "FY2021": 27812,
    })],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2025": "19.58%", "FY2024": "18.82%", "FY2023": "17.65%", "FY2022": "17.19%", "FY2021": "18.15%",
    })],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {
        "FY2025": 240287, "FY2024": 225196, "FY2023": 190056, "FY2022": 173774, "FY2021": 153193,
    })],
    p3_sources(),
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {
        "FY2025": "10.13%", "FY2024": "10.39%", "FY2023": "9.64%", "FY2022": "8.39%", "FY2021": "7.72%",
    })],
    p3_sources(),
    note=LEVERAGE_BASIS_NOTE,
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {
        "FY2023": "206.0%", "FY2022": "182.2%",
    })],
    p3_sources(),
    note="Blank FY2021 (not disclosed in that year's Pillar 3 document) and FY2024-FY2025 (no standalone Pillar 3 "
         "document has been published for either year, and the Annual Reports do not disclose LCR at all - see "
         "the Pillar 3 note on this sheet's source citation).",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {
        "FY2023": "139.7%", "FY2022": "135.6%",
    })],
    p3_sources(),
    note="Blank FY2021 (not disclosed in that year's Pillar 3 document, predates the UK NSFR requirement in any "
         "case - PS22/21) and FY2024-FY2025 (no standalone Pillar 3 document published, Annual Reports don't "
         "disclose NSFR at all).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "Not disclosed in any Pillar 3 document or Annual Report found for any year FY2021-FY2025 "
                      "- no explicit exemption stated, simply absent from every source.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash (outflow)/inflow from operating activities", {
            "FY2025": -13510, "FY2024": 6397, "FY2023": 26761, "FY2022": 15953, "FY2021": 7914,
        }),
        ("Net cash outflow from investing activities", {
            "FY2025": -47, "FY2024": -236, "FY2023": -34, "FY2022": -14, "FY2021": -65,
        }),
        ("Net cash (outflow)/inflow from financing activities", {
            "FY2025": -1095, "FY2024": -229, "FY2023": 1495, "FY2022": 1325, "FY2021": 5975,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 82700, "FY2024": 97352, "FY2023": 91420, "FY2022": 63198, "FY2021": 45934,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {
            "FY2025": 17.33, "FY2024": 16.67, "FY2023": 16.15, "FY2022": 15.05, "FY2021": 16.01,
        }),
        ("Tier 1 Ratio", {
            "FY2025": 17.33, "FY2024": 16.67, "FY2023": 16.15, "FY2022": 15.05, "FY2021": 16.01,
        }),
        ("Total Capital Ratio", {
            "FY2025": 19.58, "FY2024": 18.82, "FY2023": 17.65, "FY2022": 17.19, "FY2021": 18.15,
        }),
        ("Leverage Ratio", {
            "FY2025": 10.13, "FY2024": 10.39, "FY2023": 9.64, "FY2022": 8.39, "FY2021": 7.72,
        }),
        ("LCR", {
            "FY2023": 206.0, "FY2022": 182.2,
        }),
        ("NSFR", {
            "FY2023": 139.7, "FY2022": 135.6,
        }),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. " + ENTITY_NOTE + "\n\n" + PILLAR3_NOTE,
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CHARITY BANK FINANCIALS.xlsx")
print("Saved CHARITY BANK FINANCIALS.xlsx")
