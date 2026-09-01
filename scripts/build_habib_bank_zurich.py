import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/08864609/filing-history"
AR2025_URL = CH_BASE + "/MzUyNTkxNzE0NGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = CH_BASE + "/MzQxOTMzMTc3MGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = CH_BASE + "/MzM4MjUzMDg5N2FkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = CH_BASE + "/MzM0MjYxMTQxOWFkaXF6a2N4/document?format=pdf&download=0"

RESTATEMENT_NOTE = (
    "DATA NOTE - FY2022/FY2023 opening-vs-closing cash gap (£14,806k): the FY2022 Annual "
    "Report's own originally-published cash flow statement (p.54) shows FY2022 closing cash "
    "of £96,506k, driven by a 'Due to banks' operating-liability movement of £22,119k and "
    "'Accruals, deferred income and other liabilities' of £4,453k. The FY2023 Annual Report's "
    "FY2022 comparative (p.58) restates these to £36,925k and £3,429k respectively (a £14,806k "
    "net reclassification, with a matching £1,024k offset between 'Accruals' and 'Loans and "
    "advances to customers'), producing a restated FY2022 closing cash of £111,312k that "
    "reconciles onto FY2023's own opening balance. Per this project's convention, each year "
    "keeps its own originally-published figures (FY2022 = FY2022 AR's figures throughout) "
    "rather than a later restated comparative, so the FY2022-to-FY2023 opening/closing bridge "
    "does not tie by £14,806k - this is a traced, disclosed reclassification, not an error."
)

CASH_FLOW_SOURCES = (
    "Sources - Habib Bank Zurich Plc's own Cash Flow Statement, from each year's Companies "
    "House-filed Annual Report and Financial Statements (company 08864609):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements for the year ended 31 December 2025, "
    f"Cash Flow Statement, p.59 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 December 2023, "
    f"Cash Flow Statement, p.58 (FY2023's own originally-published figures used; not the FY2022 "
    f"comparative shown here - see note below) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for the year ended 31 December 2022, "
    f"Cash Flow Statement, p.54 (FY2022's own originally-published figures used) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements for the year ended 31 December 2021, "
    f"Cash Flow Statement, p.52 - {AR2021_URL}\n"
    + RESTATEMENT_NOTE
)


def p3_sources():
    return (
        "Sources - Habib Bank Zurich Plc does not publish a standalone Pillar 3 disclosure "
        "(no such document was locatable on the Bank's own site, via Wayback Machine, or via "
        "web search this session); figures are the Bank's own regulatory-capital and liquidity "
        "disclosures from its statutory Annual Report and Financial Statements (company "
        "08864609), Notes to the Financial Statements:\n"
        f"FY2025 & FY2024: Note 31.25 'Capital Management and Risk' p.106 (CET1/Tier 1/Total "
        f"Capital) and Note 31.21 'Liquidity Risk Management' p.104 (LCR, average-for-period "
        f"basis) of the FY2025 Annual Report - {AR2025_URL}\n"
        f"FY2023 & FY2022: Note 31.25 p.106 and Note 31.21 p.104 of the FY2023 Annual Report "
        f"- {AR2023_URL}\n"
        f"FY2021: Note 31.25 p.107 and Note 31.21 p.103 of the FY2021 Annual Report "
        f"- {AR2021_URL}\n"
        "No Additional Tier 1 capital is disclosed in any year (Tier 1 = CET1 throughout, per "
        "the Bank's own 'Common equity Tier 1 (CET1) capital' labelling in the FY2023 Annual "
        "Report's capital note). No RWA figure is disclosed in any year, so CET1/Tier 1/Total "
        "Capital Ratios, Leverage Ratio and NSFR cannot be computed from the statutory accounts; "
        "MREL is not disclosed (Habib Bank Zurich Plc is not identified as a UK resolution "
        "entity in these accounts)."
    )


bw = BankWorkbook(bank_name="Habib Bank Zurich Plc", years=YEARS, year_label=YEAR_LABEL, header_color="CF0DF5")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {
        "FY2025": 13390, "FY2024": 14975, "FY2023": 13287, "FY2022": 6379, "FY2021": 3849,
    }),
    ("DATA", "(Reversals)/impairment losses on loans and advances at amortised cost", {
        "FY2025": -937, "FY2024": -1183, "FY2023": -866, "FY2022": 684, "FY2021": -68,
    }),
    ("DATA", "(Gain)/loss on sale of financial assets at FVOCI", {
        "FY2025": -508, "FY2022": 92, "FY2021": -114,
    }),
    ("DATA", "Depreciation", {
        "FY2025": 1475, "FY2024": 1341, "FY2023": 1510, "FY2022": 1119, "FY2021": 933,
    }),
    ("DATA", "Gain on sale of property and equipment", {
        "FY2021": -1,
    }),
    ("TOTAL", "Profit before tax adjusted for non-cash items", {
        "FY2025": 13420, "FY2024": 15133, "FY2023": 13931, "FY2022": 8274, "FY2021": 4599,
    }),
    ("SECTION", "Net (increase)/decrease in operating assets", {}),
    ("DATA", "Loans and advances to banks at amortised cost", {
        "FY2025": -31608, "FY2024": -9363, "FY2023": 29645, "FY2022": -55923, "FY2021": 11053,
    }),
    ("DATA", "Loans and advances to customers at amortised cost", {
        "FY2025": -117191, "FY2024": -49138, "FY2023": -30221, "FY2022": -87685, "FY2021": -58584,
    }),
    ("DATA", "Derivative financial instruments for risk management", {
        "FY2025": -516, "FY2024": -125, "FY2023": 91, "FY2022": 112, "FY2021": 312,
    }),
    ("DATA", "Other assets", {
        "FY2025": 1037, "FY2024": -1011, "FY2023": -1651, "FY2022": 1128, "FY2021": -966,
    }),
    ("TOTAL", "Net (increase)/decrease in operating assets", {
        "FY2025": -148278, "FY2024": -59637, "FY2023": -2136, "FY2022": -142368, "FY2021": -48185,
    }),
    ("SECTION", "Net increase/(decrease) in operating liabilities", {}),
    ("DATA", "Due to banks at amortised cost", {
        "FY2025": 77915, "FY2024": -15357, "FY2023": -4420, "FY2022": 22119, "FY2021": 67056,
    }),
    ("DATA", "Due to customers at amortised cost", {
        "FY2025": 119800, "FY2024": 137112, "FY2023": 116334, "FY2022": 97548, "FY2021": 48364,
    }),
    ("DATA", "Derivative financial instruments for risk management", {
        "FY2025": -23, "FY2024": 145, "FY2023": -187, "FY2022": -285, "FY2021": 156,
    }),
    ("DATA", "Accruals, deferred income and other liabilities", {
        "FY2025": -2295, "FY2024": 3204, "FY2023": 2710, "FY2022": 4453, "FY2021": 351,
    }),
    ("DATA", "Tax paid", {
        "FY2025": -4395, "FY2024": -3029, "FY2023": -931, "FY2022": -824, "FY2021": -306,
    }),
    ("TOTAL", "Net increase/(decrease) in operating liabilities", {
        "FY2025": 191002, "FY2024": 122075, "FY2023": 113506, "FY2022": 123011, "FY2021": 115621,
    }),
    ("TOTAL", "Net cash flow from operating activities", {
        "FY2025": 56144, "FY2024": 77571, "FY2023": 125301, "FY2022": -11083, "FY2021": 72035,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property and equipment", {
        "FY2025": -313, "FY2024": -193, "FY2023": -1437, "FY2022": -8990, "FY2021": -652,
    }),
    ("DATA", "Proceeds on sale of property and equipment", {
        "FY2022": 0, "FY2021": 1,
    }),
    ("DATA", "Intangible assets under development", {
        "FY2025": -808,
    }),
    ("DATA", "Purchase of financial investments", {
        "FY2025": -101174, "FY2024": -133828, "FY2023": -91617, "FY2022": -19234, "FY2021": -114123,
    }),
    ("DATA", "Proceeds on sale/maturity of financial investments", {
        "FY2025": 111192, "FY2024": 69499, "FY2023": 73406, "FY2022": 49525, "FY2021": 42421,
    }),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": 8897, "FY2024": -64522, "FY2023": -19648, "FY2022": 21301, "FY2021": -72353,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Capital issuance", {
        "FY2024": 10000, "FY2021": 10000,
    }),
    ("DATA", "Dividend paid", {
        "FY2025": -5543, "FY2024": -4142, "FY2022": -1476,
    }),
    ("DATA", "Leases paid", {
        "FY2025": -630, "FY2024": -461, "FY2023": -424, "FY2022": -434, "FY2021": -432,
    }),
    ("DATA", "Interest paid/(charges) on subordinated liabilities", {
        "FY2025": -31, "FY2024": -1408, "FY2023": -1199, "FY2022": -491, "FY2021": 29,
    }),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2025": -6204, "FY2024": 3989, "FY2023": -1623, "FY2022": -2401, "FY2021": 9597,
    }),
    ("TOTAL", "Net increase in cash and cash equivalents", {
        "FY2025": 58837, "FY2024": 17038, "FY2023": 104030, "FY2022": 7817, "FY2021": 9279,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 232380, "FY2024": 215342, "FY2023": 111312, "FY2022": 88689, "FY2021": 79410,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 291217, "FY2024": 232380, "FY2023": 215342, "FY2022": 96506, "FY2021": 88689,
    }),
]

bw.add_cash_flow_sheet(
    title="Habib Bank Zurich Plc — Cash Flow Statement",
    subtitle="Figures as reported in each year's own Annual Report and Financial Statements",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=140)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2025": 124587, "FY2024": 119896, "FY2023": 103077, "FY2022": 90525, "FY2021": 86301,
    })],
    p3_sources(),
    note="No Additional Tier 1 capital is disclosed in any year, so CET1 = Tier 1 capital throughout.",
)
bw.add_not_disclosed_metric_sheets(["CET1 Ratio"], p3_sources(),
    per_note={"CET1 Ratio": "No RWA figure is disclosed in any year's statutory accounts, so this ratio cannot be computed."})

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {
        "FY2025": 124587, "FY2024": 119896, "FY2023": 103077, "FY2022": 90525, "FY2021": 86301,
    })],
    p3_sources(),
    note="Equal to CET1 capital - no Additional Tier 1 instruments are disclosed in any year.",
)
bw.add_not_disclosed_metric_sheets(["Tier 1 Ratio"], p3_sources(),
    per_note={"Tier 1 Ratio": "No RWA figure is disclosed in any year's statutory accounts, so this ratio cannot be computed."})

metric(
    "Total Capital", "£'000",
    [("Own funds (Tier 1 + Tier 2 capital)", {
        "FY2025": 144852, "FY2024": 140192, "FY2023": 123417, "FY2022": 111377, "FY2021": 106687,
    })],
    p3_sources(),
    note="Tier 2 capital comprises qualifying subordinated liabilities (plus, in FY2023/FY2022, a small IFRS 9 "
         "ECL regulatory-capital adjustment disclosed by the Bank).",
)
bw.add_not_disclosed_metric_sheets(
    ["Total Capital Ratio", "Total RWAs", "Leverage Ratio"], p3_sources(),
    per_note={
        "Total Capital Ratio": "No RWA figure is disclosed in any year's statutory accounts, so this ratio cannot be computed.",
        "Total RWAs": "Not disclosed in any year's statutory accounts.",
        "Leverage Ratio": "No leverage exposure measure is disclosed in any year's statutory accounts.",
    },
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (average for the period)", {
        "FY2025": "232%", "FY2024": "287%", "FY2023": "196%", "FY2022": "205%", "FY2021": "159%",
    })],
    p3_sources(),
    note="The Bank discloses LCR on 4 bases each year (as at 31 December, average/maximum/minimum for the "
         "period); the average-for-the-period figure is used for consistency with this project's convention "
         "elsewhere. As-at-31-December figures are higher every year (e.g. FY2025 180%, FY2024 243%).",
)
bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"], p3_sources(),
    per_note={
        "NSFR": "Not disclosed in any year's statutory accounts.",
        "MREL Ratio": "Not disclosed - Habib Bank Zurich Plc is not identified as a UK resolution entity in these accounts.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": 56144, "FY2024": 77571, "FY2023": 125301, "FY2022": -11083, "FY2021": 72035,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": 8897, "FY2024": -64522, "FY2023": -19648, "FY2022": 21301, "FY2021": -72353,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": -6204, "FY2024": 3989, "FY2023": -1623, "FY2022": -2401, "FY2021": 9597,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 291217, "FY2024": 232380, "FY2023": 215342, "FY2022": 96506, "FY2021": 88689,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("LCR (average, %)", {
            "FY2025": 232, "FY2024": 287, "FY2023": 196, "FY2022": 205, "FY2021": 159,
        }),
    ],
    note="Only LCR is charted here - CET1/Tier 1/Total Capital Ratio, Leverage Ratio, NSFR and MREL Ratio are "
         "not disclosed in this entity's statutory accounts (no standalone Pillar 3 document exists and no RWA "
         "figure is published); see the individual Pillar 3 metric sheets. Figures are duplicated from the "
         "detail sheets for at-a-glance trend viewing; see each sheet's own source citation for the underlying "
         "document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HABIB BANK ZURICH FINANCIALS.xlsx")
