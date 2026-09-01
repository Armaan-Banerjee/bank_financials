import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = ("https://find-and-update.company-information.service.gov.uk/company/01074897/"
              "filing-history/MzUzNzM1MjkyOGFkaXF6a2N4/document?format=pdf&download=0")
AR2024_URL = ("https://find-and-update.company-information.service.gov.uk/company/01074897/"
              "filing-history/MzQ4Mzc3NzE0NWFkaXF6a2N4/document?format=pdf&download=0")
AR2023_URL = ("https://find-and-update.company-information.service.gov.uk/company/01074897/"
              "filing-history/MzQ0MDMxMDc4MGFkaXF6a2N4/document?format=pdf&download=0")
AR2022_URL = ("https://find-and-update.company-information.service.gov.uk/company/01074897/"
              "filing-history/MzQyNDMxMDM1M2FkaXF6a2N4/document?format=pdf&download=0")
AR2021_URL = ("https://find-and-update.company-information.service.gov.uk/company/01074897/"
              "filing-history/MzM2MTYzNTYxM2FkaXF6a2N4/document?format=pdf&download=0")

ENTITY_NOTE = (
    "Havin Bank Limited (Companies House 01074897, formerly Havana International Bank Limited) "
    "is a UK-incorporated bank whose majority and ultimate controlling shareholder is Banco "
    "Central de Cuba (95.6%), with Banco Popular de Ahorro and Banco de Credito y Comercio "
    "(2.2% each) also Cuban state banks. All 5 Companies House filings used are scanned/"
    "image-only (0 extractable text) - transcribed via page-image rendering. PRESENTATION "
    "NOTE: cash and cash equivalents were redefined starting with the FY2022 Annual Report to "
    "include loans and advances to banks with a maturity up to 3 months (previously excluded); "
    "FY2022's own report states this restates FY2021's closing balance from GBP43,634,527 to "
    "GBP98,668,182 for comparability, but each year here is shown on its own originally-"
    "published basis per this project's convention, so FY2021's closing balance does NOT tie "
    "to FY2022's opening balance - this is a genuine, documented source-driven discontinuity, "
    "not a transcription error. A second presentational point: 'Interest paid' sits under "
    "Financing activities in every year's own original presentation (FY2021-FY2024); the "
    "FY2025 Annual Report reclassified it into the Operating activities note for FY2025 only "
    "(explicitly stated to have no impact on net cash movement), so FY2025's own Financing "
    "section only shows Dividends paid. FY2021's own Statement of Cash Flows title differs "
    "slightly across years but is the Bank's own primary statement throughout. FY2025's own "
    "Note 25 discloses two 2026 US Executive Orders (14380, 14404) expanding sanctions "
    "pressure on Cuba, flagged as a post balance sheet event potentially affecting the Bank's "
    "future business - not reflected in these historical figures."
)

CASH_FLOW_SOURCES = (
    "Sources - Havin Bank Limited's own Statement of Cash Flows (face of statement, each "
    "year's own primary presentation, not a later restated comparative) from its Companies "
    "House-filed Annual Report and Financial Statements:\n"
    f"FY2025: Annual Report FY2025, p.22 - {AR2025_URL}\n"
    f"FY2024: Annual Report FY2024, p.21 - {AR2024_URL}\n"
    f"FY2023: Annual Report FY2024, p.21 (FY2023 comparative column; FY2023's own report was "
    f"not independently re-verified for this line since the FY2024 comparative is consistent "
    f"with the FY2022 report's own FY2022 closing balance) - {AR2024_URL}\n"
    f"FY2022: Annual Report FY2022, p.27 - {AR2022_URL}\n"
    f"FY2021: Annual Report FY2021, p.21 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Havin Bank Limited's own statutory accounts (no standalone Pillar 3 "
        "document exists for this entity - the Bank's website, hib.uk.com, is entirely "
        "client-side JavaScript-rendered with no server-side content reachable by automated "
        "tools, and Wayback Machine was unavailable this session; a Pillar 3 report may exist "
        "that simply couldn't be located this session, so this is a documented access gap, "
        "not a confirmed non-disclosure):\n"
        f"FY2025/FY2024: Annual Report FY2025, Note 23 'Capital', p.43 - {AR2025_URL}\n"
        f"FY2023/FY2022: Annual Report FY2023, Note 23 'Capital', p.47 - {AR2023_URL}\n"
        f"FY2021: Annual Report FY2021, Note 22 'Capital', p.42-43 (this year's disclosure "
        f"gives only Total Tier One Capital - no Deductions from Capital/Total Regulatory "
        f"Capital breakdown was published for FY2021, a thinner format than later years) - "
        f"{AR2021_URL}\n\n"
        "No Risk Weighted Assets figure, and no CET1/Tier 1/Total Capital Ratio, Leverage "
        "Ratio, LCR, NSFR, or MREL figure is disclosed anywhere in the statutory accounts for "
        "any year (only an unaudited 'Capital surplus over regulatory minimum' % from FY2022 "
        "onward, which is a different metric to a standard CRR capital ratio and is not used "
        "here). CET1 = Tier 1 = Total Capital throughout, since no Additional Tier 1 or Tier 2 "
        "instruments are disclosed in any year."
    )


bw = BankWorkbook(bank_name="Havin Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="2858A5")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Cash (outflows)/inflows from operating activities", {
        "FY2025": 3521073, "FY2024": 1528221, "FY2023": -3161495,
        "FY2022": 1121795, "FY2021": -13679377,
    }),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2025": 3521073, "FY2024": 1528221, "FY2023": -3161495,
        "FY2022": 1121795, "FY2021": -13679377,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Interest received", {"FY2021": 1590087}),
    ("DATA", "Payments to acquire intangible assets", {"FY2022": -184990, "FY2023": 0}),
    ("DATA", "Payments to acquire tangible fixed assets", {"FY2025": -68081, "FY2021": -2152}),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": -68081, "FY2023": 0, "FY2022": -184990, "FY2021": 1587935,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Interest paid", {
        "FY2024": -1680946, "FY2023": -1518544, "FY2022": -211750, "FY2021": -106956,
    }),
    ("DATA", "Dividend paid", {"FY2025": -1600000}),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2025": -1600000, "FY2024": -1680946, "FY2023": -1518544,
        "FY2022": -211750, "FY2021": -106956,
    }),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2025": 1852992, "FY2024": -152725, "FY2023": -4680040,
        "FY2022": 725055, "FY2021": -12198398,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 94560472, "FY2024": 94713197, "FY2023": 99393237,
        "FY2022": 98668182, "FY2021": 55832925,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 96413464, "FY2024": 94560472, "FY2023": 94713197,
        "FY2022": 99393237, "FY2021": 43634527,
    }),
]

bw.add_cash_flow_sheet(
    title="Havin Bank Limited — Statement of Cash Flows",
    subtitle="As presented in each year's own primary Statement of Cash Flows (Operating "
             "activities shown as the single reconciled figure the face of each year's own "
             "statement discloses, referencing that year's own supporting note for detail)",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=210,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=140)


CAPITAL_VALUES = {
    "FY2025": 22532098, "FY2024": 23791445, "FY2023": 23105954,
    "FY2022": 22291259, "FY2021": 22508676,
}
CAPITAL_NOTE = ("FY2021 is Total Tier One Capital (Share Capital + Reserves) as no Deductions "
                 "from Capital were separately disclosed that year; FY2022-FY2025 are Total "
                 "Regulatory Capital (Total Tier One Capital less Deductions from Capital). No "
                 "AT1/T2 capital is disclosed in any year, so CET1 = Tier 1 = Total Capital.")

metric("CET1 Capital", "£", [("Common Equity Tier 1 (CET1) capital", dict(CAPITAL_VALUES))],
       p3_sources(), note=CAPITAL_NOTE)
bw.add_not_disclosed_metric_sheets(["CET1 Ratio"], p3_sources())
metric("Tier 1 Capital", "£", [("Tier 1 capital", dict(CAPITAL_VALUES))],
       p3_sources(), note=CAPITAL_NOTE)
bw.add_not_disclosed_metric_sheets(["Tier 1 Ratio"], p3_sources())
metric("Total Capital", "£", [("Total regulatory capital", dict(CAPITAL_VALUES))],
       p3_sources(), note=CAPITAL_NOTE)

bw.add_not_disclosed_metric_sheets(
    ["Total Capital Ratio", "Total RWAs",
     "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": 3521073, "FY2024": 1528221, "FY2023": -3161495,
            "FY2022": 1121795, "FY2021": -13679377,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": -68081, "FY2023": 0, "FY2022": -184990, "FY2021": 1587935,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": -1600000, "FY2024": -1680946, "FY2023": -1518544,
            "FY2022": -211750, "FY2021": -106956,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 96413464, "FY2024": 94560472, "FY2023": 94713197,
            "FY2022": 99393237, "FY2021": 43634527,
        }),
    ],
    cash_flow_unit="£",
    ratios=[],
    note="No Pillar 3 ratios are disclosed for this entity (see the individual metric sheets) "
         "- CET1/Tier 1/Total Capital £ figures are shown on their own sheets instead. Figures "
         "are duplicated from the detail sheets for at-a-glance trend viewing; see each "
         "sheet's own source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HAVIN BANK FINANCIALS.xlsx")
