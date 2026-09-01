import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Only 4 years available: FY2025 (y/e 31 Dec 2025) accounts are not yet filed
# at Companies House as of this build (2026-08-28) - next annual filing due by
# ~30 Sep 2026 (9-month UK deadline).
YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2024_URL = ("https://find-and-update.company-information.service.gov.uk/company/02321802/"
              "filing-history/MzQ2ODA5NDQ2MGFkaXF6a2N4/document?format=pdf&download=0")
AR2023_URL = ("https://find-and-update.company-information.service.gov.uk/company/02321802/"
              "filing-history/MzQyMTAwMDI4OGFkaXF6a2N4/document?format=pdf&download=0")
AR2022_URL = ("https://find-and-update.company-information.service.gov.uk/company/02321802/"
              "filing-history/MzM4ODQ3NjMwOWFkaXF6a2N4/document?format=pdf&download=0")
AR2021_URL = ("https://find-and-update.company-information.service.gov.uk/company/02321802/"
              "filing-history/MzMzODA1ODgyNmFkaXF6a2N4/document?format=pdf&download=0")

ENTITY_NOTE = (
    "EFG Private Bank Limited (company 02321802, FRN 144036), a UK subsidiary of EFG "
    "International AG (Switzerland, listed on the SIX Swiss Exchange). Each year's Cash Flow "
    "Statement figures are that year's own originally-published statement, not a later report's "
    "restated comparative - a genuine restatement exists between FY2021's own filing and its "
    "appearance as the FY2022 report's comparative (e.g. FY2021 operating activities £586,667k "
    "own filing vs £571,317k restated comparative), and again between FY2022's own filing and "
    "its appearance as the FY2023 report's comparative (£547,141k vs £542,301k). FY2023's own "
    "filing figures match exactly what the FY2024 report shows as its own comparative, so no "
    "restatement issue there."
)

CASH_FLOW_SOURCES = (
    "Sources - EFG Private Bank Limited's own Cash Flow Statement, each year's own originally-"
    "published filing (not a later report's restated comparative):\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.24-25 (Cash Flow Statement) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.24-25 (Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.22 (Cash Flow Statement) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.22 (Cash Flow Statement) - {AR2021_URL}\n"
    + ENTITY_NOTE
)


def p3_sources(page="83"):
    return (
        "Sources - EFG Private Bank Limited's own accounts, Note 34 (Capital management), unless "
        "noted otherwise:\n"
        f"FY2024: Annual Report and Financial Statements 2024, p.{page} - {AR2024_URL}\n"
        f"FY2023: Annual Report and Financial Statements 2023, p.80 - {AR2023_URL}\n"
        f"FY2022: Annual Report and Financial Statements 2022, p.60-61 - {AR2022_URL}\n"
        "FY2021: as stated in the FY2022 Annual Report's own FY2021 comparative column, p.60-61 "
        f"- {AR2022_URL}\n"
        "No standalone Pillar 3 document was locatable for this entity (efginternational.com "
        "blocks automated fetches; no UK-specific regulatory disclosures page found) - all figures "
        "sourced from the statutory accounts' own Capital management note.\n"
        "IMPORTANT DISCLOSURE-FORMAT NOTE: FY2021 and FY2022's own Annual Reports disclose a full "
        "capital table (CET1 Capital, Total Capital, Total RWAs, CET1 Ratio, Total Capital Ratio). "
        "FY2023 and FY2024's own Annual Reports disclose ONLY Common equity tier 1 capital (£m) - "
        "no ratio, no RWA, no Total Capital figure at all, confirmed by reading the full Capital "
        "management note in both reports. This is a genuine reduction in disclosure depth between "
        "report vintages, not a gap in this research. Liquidity risk (Note 29) is purely "
        "qualitative/contractual-maturity-table based in every year reviewed - no LCR/NSFR "
        "percentage is stated anywhere. No Leverage Ratio or MREL figure was found in any year."
    )


bw = BankWorkbook(bank_name="EFG Private Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="4223DA")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operations", {}),
    ("DATA", "Profit before tax",
     {"FY2024": 26187, "FY2023": 40142, "FY2022": 34871, "FY2021": 99029}),
    ("DATA", "Depreciation of fixed assets",
     {"FY2024": 4248, "FY2023": 3323, "FY2022": 4499, "FY2021": 4752}),
    ("DATA", "Amortisation of intangibles",
     {"FY2024": 245, "FY2023": 551, "FY2022": 535, "FY2021": 434}),
    ("DATA", "Amortisation of IFRS 2 reserve through profit and loss",
     {"FY2024": 9630, "FY2023": 6052, "FY2022": 4214, "FY2021": 4030}),
    ("DATA", "Loss allowance provision",
     {"FY2024": 1690, "FY2023": 555, "FY2022": -210, "FY2021": 37}),
    ("DATA", "Loss/(gain) on sale of subsidiary as investment activity",
     {"FY2022": 0, "FY2021": -68900}),
    ("DATA", "Gains less losses on disposal of financial assets",
     {"FY2024": 0, "FY2023": -217, "FY2022": -147, "FY2021": -60}),
    ("DATA", "Dividend paid by subsidiary included in investment income",
     {"FY2022": 0, "FY2021": -30000}),
    ("DATA", "Lease interest per IFRS16",
     {"FY2024": 581, "FY2023": 435, "FY2022": 448, "FY2021": 156}),
    ("DATA", "Change in interest accrual",
     {"FY2024": -9430, "FY2023": -4920}),
    ("DATA", "Effect of foreign exchange",
     {"FY2024": -5429, "FY2023": 51485, "FY2022": -61770}),
    ("DATA", "Release of tax related provision", {"FY2024": -1991}),
    ("DATA", "(Increase)/decrease in derivative financial instruments",
     {"FY2024": -8951, "FY2023": 42583, "FY2022": -57077, "FY2021": -15336}),
    ("DATA", "(Increase)/decrease in loans and advances to customers",
     {"FY2024": -492079, "FY2023": 59123, "FY2022": -202340, "FY2021": -590609}),
    ("DATA", "Decrease/(increase) in other assets",
     {"FY2024": 15349, "FY2023": -21479, "FY2022": -2019, "FY2021": 28685}),
    ("DATA", "Increase/(decrease) in due to other banks",
     {"FY2024": 462830, "FY2023": -63755, "FY2022": 219568, "FY2021": 11595}),
    ("DATA", "Increase/(decrease) in due to customers",
     {"FY2024": 327090, "FY2023": -46670, "FY2022": 609713, "FY2021": 1137564}),
    ("DATA", "(Decrease)/increase in other liabilities and provisions",
     {"FY2024": -30373, "FY2023": 35466, "FY2022": 5925, "FY2021": 12154}),
    ("DATA", "Payments to tax authorities", {"FY2024": -9774, "FY2023": -5025}),
    ("DATA", "Corporation tax paid", {"FY2022": -2617, "FY2021": -1183}),
    ("DATA", "Payments to parent for participation in share scheme",
     {"FY2024": -9465, "FY2023": -7833, "FY2022": -6452, "FY2021": -5681}),
    ("TOTAL", "Net cash flows from operating activities",
     {"FY2024": 280358, "FY2023": 89816, "FY2022": 547141, "FY2021": 586667}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "(Purchase) of investment securities",
     {"FY2024": -1817999, "FY2023": -1574973, "FY2022": -1177277, "FY2021": -453370}),
    ("DATA", "Proceeds from maturities/sale of investment securities",
     {"FY2024": 1630203, "FY2023": 973586, "FY2022": 587790, "FY2021": 340452}),
    ("DATA", "(Purchase) of capital in subsidiaries", {"FY2021": -1275}),
    ("DATA", "Proceeds from disposal of subsidiary", {"FY2021": 78900}),
    ("DATA", "(Purchase) of property plant & equipment",
     {"FY2024": -2864, "FY2023": -819, "FY2022": -5793, "FY2021": -176}),
    ("DATA", "(Purchase) of intangible assets",
     {"FY2024": -2414, "FY2023": -1946, "FY2022": -1850, "FY2021": -973}),
    ("DATA", "Proceeds from dividends", {"FY2021": 30000}),
    ("TOTAL", "Net cash flows used in investing activities",
     {"FY2024": -193074, "FY2023": -604152, "FY2022": -597130, "FY2021": -6442}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Payment of AT1 interest",
     {"FY2024": -7174, "FY2023": -7154, "FY2022": -5394, "FY2021": -5389}),
    ("DATA", "Payment of dividends",
     {"FY2024": 0, "FY2023": -12676, "FY2022": 0, "FY2021": -89000}),
    ("DATA", "Lease interest repaid",
     {"FY2024": -421, "FY2023": -36, "FY2022": -448, "FY2021": None}),
    ("DATA", "Lease disposal", {"FY2024": -267}),
    ("DATA", "Lease principal repaid",
     {"FY2024": -2202, "FY2023": -644, "FY2022": -1905, "FY2021": -3028}),
    ("TOTAL", "Net cash flows from financing activities",
     {"FY2024": -10064, "FY2023": -20510, "FY2022": -7747, "FY2021": -97417}),
    ("TOTAL", "Net cash outflows/(inflows)",
     {"FY2024": 77220, "FY2023": -534846, "FY2022": -57736, "FY2021": 482808}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents",
     {"FY2024": -326, "FY2023": 794, "FY2022": -3042, "FY2021": -12197}),
    ("TOTAL", "Net change in cash and cash equivalents",
     {"FY2024": 76894, "FY2023": -534052, "FY2022": -60778, "FY2021": 470611}),
    ("DATA", "Cash and cash equivalents at the beginning of period",
     {"FY2024": 769571, "FY2023": 1303623, "FY2022": 1369241, "FY2021": 898630}),
    ("TOTAL", "Cash and cash equivalents at the end of period",
     {"FY2024": 846465, "FY2023": 769571, "FY2022": 1308463, "FY2021": 1369241}),
]

bw.add_cash_flow_sheet(
    title="EFG Private Bank Limited — Cash Flow Statement",
    subtitle="Company basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=170)


NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed for this entity. No standalone Pillar 3 document was locatable, and "
    "this metric does not appear in the statutory accounts' Capital management or Liquidity risk "
    "notes for this year (confirmed by reading both notes directly, not assumed)."
)

metric(
    "CET1 Capital", "£m",
    [("Common equity tier 1 capital",
      {"FY2024": 237.2, "FY2023": 205.8, "FY2022": 165.6, "FY2021": 195.2})],
    p3_sources(),
    note="FY2022/FY2021 stated as \"(audited)\" in the source; FY2024/FY2023 not marked audited/unaudited.",
)

metric(
    "CET1 Ratio", "%",
    [("Common equity tier 1 capital ratio", {"FY2022": "10.9%", "FY2021": "14.8%"})],
    p3_sources(),
    note=NOT_DISCLOSED_NOTE,
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital (= CET1 capital; no AT1 instruments disclosed any year)",
      {"FY2024": 237.2, "FY2023": 205.8, "FY2022": 165.6, "FY2021": 195.2})],
    p3_sources(),
    note="Tier 1 = CET1 throughout - no Additional Tier 1 instruments are mentioned anywhere in "
         "the source across any of the 4 years (the AT1 INTEREST paid in the Cash Flow Statement "
         "relates to a different capital instrument class disclosed elsewhere in the accounts as "
         "part of \"other equity\", not counted as regulatory Tier 1/AT1 capital in Note 34).",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio (= CET1 ratio; no AT1 instruments disclosed any year)",
      {"FY2022": "10.9%", "FY2021": "14.8%"})],
    p3_sources(),
    note=NOT_DISCLOSED_NOTE,
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2022": 232.3, "FY2021": 261.8})],
    p3_sources(),
    note=NOT_DISCLOSED_NOTE + " FY2022/FY2021 values are from the source's own table (Tier 1 + Tier 2; "
         "Tier 2 comprises unrealised FVOCI gains per the source's own definition, not separately "
         "itemised).",
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {"FY2022": "15.2%", "FY2021": "19.9%"})],
    p3_sources(),
    note=NOT_DISCLOSED_NOTE,
)

metric(
    "Total RWAs", "£m",
    [("Total risk weighted assets", {"FY2022": 1523.7, "FY2021": 1317.8})],
    p3_sources(),
    note=NOT_DISCLOSED_NOTE + " FY2022/FY2021 as directly stated in the source (not calculated).",
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flows from operating activities",
         {"FY2024": 280358, "FY2023": 89816, "FY2022": 547141, "FY2021": 586667}),
        ("Net cash flows used in investing activities",
         {"FY2024": -193074, "FY2023": -604152, "FY2022": -597130, "FY2021": -6442}),
        ("Net cash flows from financing activities",
         {"FY2024": -10064, "FY2023": -20510, "FY2022": -7747, "FY2021": -97417}),
        ("Cash and cash equivalents at end of period",
         {"FY2024": 846465, "FY2023": 769571, "FY2022": 1308463, "FY2021": 1369241}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2022": "10.9%", "FY2021": "14.8%"}),
        ("Total Capital Ratio", {"FY2022": "15.2%", "FY2021": "19.9%"}),
    ],
    note="FY2023/FY2024's own Annual Reports disclose only CET1 Capital (£m) - no ratio, no RWA, "
         "no Total Capital - so no ratios plot for those two years; see the CET1 Capital sheet and "
         "the Pillar 3 source note for the full disclosure-format explanation. Figures are "
         "duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/EFG PRIVATE BANK FINANCIALS.xlsx")
