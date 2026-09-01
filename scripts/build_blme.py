import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Full 5 years of cash flow AND Pillar 3 coverage, FY2021-FY2025. No FRS 101/102
# cash-flow exemption. Bank-solo ("BLME plc") basis throughout for both statements -
# BLME also publishes wider "BLME Holdings" group accounts but the PRA entity here
# is the plc, and its Pillar 3 KM1 tables are already at the plc level.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/05897786"
FS2025_URL = "https://www.blme.com/media/z0jd2sah/blme-plc-financial-statements-31-december-2025.pdf"
FS2024_URL = "https://www.blme.com/media/rneds5db/blme-plc-financial-statements-31-december-2024.pdf"
FS2023_URL = "https://www.blme.com/media/2j5fy4tv/blme-plc-financial-statements-31-december-2023.pdf"
FS2022_URL = "https://www.blme.com/media/2014/blme-plc-financial-statements-31-december-2022.pdf"
FS2021_URL = "https://www.blme.com/media/1964/blme-plc-fin-stats-31-december-2021-for-website.pdf"
P32025_URL = "https://www.blme.com/media/jf2dbyrm/2025-pillar-iii-disclosure.pdf"
P32024_URL = "https://www.blme.com/media/mhantsoh/2024-pillar-iii-disclosure.pdf"
P32023_URL = "https://www.blme.com/media/fluobg0d/2023-pillar-iii-disclosure.pdf"
P32022_URL = "https://www.blme.com/media/2017/2022-pillar-iii-disclosure.pdf"
P32021_URL = "https://www.blme.com/media/1997/2021-pillar-iii-disclosure.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank of London and The Middle East plc (FRN 464292, Companies House 05897786, matches "
    "Banks List 2608.xlsx exactly) is a UK-incorporated Sharia-compliant wholesale/private bank, majority-owned "
    "by Boubyan Bank (Kuwait). It publishes both wider 'BLME Holdings' group accounts and standalone 'BLME plc' "
    "(Bank-solo) accounts on its own site - this workbook uses the plc/solo figures throughout for both the cash "
    "flow statement and Pillar 3, matching the PRA-regulated entity. Terminology uses 'profit'/'financing' rather "
    "than 'interest'/'loans' (Sharia-compliant banking), consistent with ALRAYAN Bank elsewhere in this project."
)

CASH_FLOW_SOURCES = (
    "Sources - BLME plc's own Statement of Cash Flows, £'000s, all years, each from that year's own "
    "originally-published Financial Statements (not a later restated comparative):\n"
    f"FY2025: BLME plc Financial Statements 31 December 2025, p.31-32 - {FS2025_URL}\n"
    f"FY2024: BLME plc Financial Statements 31 December 2024, p.31 - {FS2024_URL}\n"
    f"FY2023: BLME plc Financial Statements 31 December 2023, p.32 - {FS2023_URL}\n"
    f"FY2022: BLME plc Financial Statements 31 December 2022, p.32 - {FS2022_URL}\n"
    f"FY2021: BLME plc Financial Statements 31 December 2021, p.30 - {FS2021_URL}\n"
    "The FY2025 report restates FY2024's comparative (a prior period adjustment of -£9,035k to retained earnings "
    "at 1 Jan 2024, per its own Note 2.3), and the FY2024 report itself already restated FY2023's comparative "
    "(-£3,964k, per its own Note 2b) - both are genuine disclosed restatements, but every column in this sheet "
    "uses each year's own originally-published figures (project convention), not a later restated version.\n"
    "Presentation changed twice across the 5 years: FY2021-FY2023 include a separate 'Due from customers' line "
    "in operating assets (dropped from FY2024 onward), and FY2025 combines the 'operating assets' and 'operating "
    "liabilities' movements into a single unlabelled subtotal rather than the two separate ones FY2021-FY2024 "
    "printed - shown as blank cells where a line doesn't apply that year, not gaps. All TOTAL rows reconcile "
    "exactly to source for every year.\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - BLME plc's own Pillar III Disclosures, £m capital amounts / % ratios, all years:\n"
        f"FY2025: Pillar III Disclosure - 31 December 2025, Key metrics table, p.4 - {P32025_URL}\n"
        f"FY2024: Pillar III Disclosure - 31 December 2024, Key metrics table, p.4 - {P32024_URL}\n"
        f"FY2023: Pillar III Disclosure - 31 December 2023, Key metrics table, p.4 - {P32023_URL}\n"
        f"FY2022: Pillar III Disclosure - 31 December 2022, Key metrics table, p.4 - {P32022_URL}\n"
        f"FY2021: sourced from the FY2022 Pillar III Disclosure's own FY2021 comparative column, Key metrics "
        f"table, p.4 - {P32022_URL} (the FY2021 edition itself, {P32021_URL}, pre-dates BLME's adoption of the "
        f"standardised KM1 template - it uses the older CRR own-funds/appendix format instead, so the FY2022 "
        f"report's comparative column is used for consistency with every other year in this workbook).\n"
        + (extra + "\n" if extra else "")
        + "\n" + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Bank of London and The Middle East plc", years=YEARS, year_label=YEAR_LABEL,
                   header_color="5D3FD3")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 1603, "FY2024": 7739, "FY2023": 7837, "FY2022": -9037, "FY2021": -7176}),
    ("DATA", "Exchange differences", {"FY2025": -21, "FY2024": -3, "FY2023": -5, "FY2022": -10, "FY2021": -12}),
    ("DATA", "Fair value (gain)/loss on investment securities", {"FY2022": 195, "FY2021": -8}),
    ("DATA", "Share of profit of equity-accounted investees, net of tax", {"FY2025": -658, "FY2024": -2921, "FY2023": -81, "FY2022": -97, "FY2021": -100}),
    ("DATA", "Credit impairment losses / provision for impairment", {"FY2025": 3938, "FY2024": 2897, "FY2023": 2879, "FY2022": 13398, "FY2021": 12451}),
    ("DATA", "Impairment of investment in subsidiary", {"FY2025": -1185}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 748, "FY2024": 343, "FY2023": 235, "FY2022": 60, "FY2021": 29}),
    ("DATA", "Movements relating to profit rate swaps", {"FY2022": -112}),
    ("DATA", "IFRS 16 - depreciation and finance charges/additions", {"FY2025": 494, "FY2024": 630, "FY2023": 775, "FY2022": 2797, "FY2021": 878}),
    ("DATA", "Accretion of finance charge on lease liabilities", {"FY2025": 65}),
    ("DATA", "Amortisation of investment securities", {"FY2025": -195, "FY2024": 365, "FY2023": 152, "FY2022": 239, "FY2021": 257}),
    ("DATA", "Net change in fair value of investment in equity/debt at FVOCI", {"FY2025": 280}),
    ("TOTAL", "Net cash generated before changes in operating assets and liabilities",
     {"FY2025": 5069, "FY2024": 9050, "FY2023": 11792, "FY2022": 7433, "FY2021": 6319}),
    ("DATA", "Due from financial institutions", {"FY2025": 127437, "FY2024": 145520, "FY2023": 152940, "FY2022": 26243, "FY2021": -138243}),
    ("DATA", "Due from customers", {"FY2022": 24950, "FY2021": 9594}),
    ("DATA", "Financing arrangements", {"FY2025": -69536, "FY2024": -143580, "FY2023": -97301, "FY2022": -126771, "FY2021": 13336}),
    ("DATA", "Finance lease receivables", {"FY2025": 1262, "FY2024": -1367, "FY2023": 32645, "FY2022": 7214, "FY2021": 159360}),
    ("DATA", "Other assets", {"FY2025": 7645, "FY2024": -10275, "FY2023": 10797, "FY2022": -5460, "FY2021": -4206}),
    ("DATA", "Due to financial institutions", {"FY2025": 15709, "FY2024": 26815, "FY2023": -42286, "FY2022": -226876, "FY2021": 83757}),
    ("DATA", "Due to customers", {"FY2025": -64011, "FY2024": 13193, "FY2023": -75983, "FY2022": 290262, "FY2021": -263860}),
    ("DATA", "Other liabilities", {"FY2025": 1403, "FY2024": -649, "FY2023": 294, "FY2022": 1930, "FY2021": -9295}),
    ("DATA", "Income taxes/corporation tax paid", {"FY2025": -7, "FY2023": -260, "FY2022": -2062, "FY2021": -2847}),
    ("TOTAL", "Net cash generated from/(used in) operating activities",
     {"FY2025": 24971, "FY2024": 38707, "FY2023": -7362, "FY2022": -3137, "FY2021": -146085}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase/(disposal) of property and equipment", {"FY2025": 23, "FY2024": -123, "FY2023": -791, "FY2022": -876, "FY2021": -15}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -452, "FY2024": -1031, "FY2023": -893, "FY2022": -714}),
    ("DATA", "Purchase of investment securities", {"FY2025": -7598, "FY2024": -34858, "FY2023": -15629, "FY2022": -4873}),
    ("DATA", "Sale of investment securities", {"FY2025": 19615, "FY2024": 8006, "FY2023": 1741, "FY2022": 33130, "FY2021": 30483}),
    ("DATA", "Sale of subsidiary to a fellow subsidiary", {"FY2023": 298}),
    ("DATA", "Purchase of interest in assets held for sale", {"FY2023": -35763}),
    ("DATA", "Sale of interest in assets held for sale", {"FY2024": 1800, "FY2023": 6000, "FY2021": 485}),
    ("DATA", "Purchase of interest in joint venture", {"FY2023": -6440}),
    ("DATA", "Dividend(s) received from joint venture(s)", {"FY2025": 2170, "FY2024": 2284, "FY2023": 325, "FY2022": 100, "FY2021": 100}),
    ("DATA", "Sale of equity instrument at FVOCI", {"FY2025": 620}),
    ("DATA", "Sale of interest in joint venture", {"FY2025": 1650}),
    ("TOTAL", "Net cash generated from/(used in) investing activities",
     {"FY2025": 16028, "FY2024": -23922, "FY2023": -51152, "FY2022": 26767, "FY2021": 31053}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payment of principal portion of lease liabilities", {"FY2025": -512, "FY2024": -589, "FY2023": -719, "FY2022": -1123, "FY2021": -1086}),
    ("DATA", "Payment of finance charge on lease liabilities", {"FY2025": -65}),
    ("TOTAL", "Net cash generated from/(used in) financing activities",
     {"FY2025": -577, "FY2024": -589, "FY2023": -719, "FY2022": -1123, "FY2021": -1086}),
    ("TOTAL", "Net change in cash and cash equivalents",
     {"FY2025": 40422, "FY2024": 14196, "FY2023": -59233, "FY2022": 22507, "FY2021": -116118}),
    ("DATA", "Exchange differences in respect of cash and cash equivalents", {"FY2025": -33, "FY2024": -65, "FY2023": -21, "FY2022": 679, "FY2021": -3292}),
    ("DATA", "Cash and cash equivalents at the beginning of the period", {"FY2025": 90139, "FY2024": 76008, "FY2023": 135262, "FY2022": 112076, "FY2021": 231486}),
    ("TOTAL", "Cash and cash equivalents at the end of the period",
     {"FY2025": 130528, "FY2024": 90139, "FY2023": 76008, "FY2022": 135262, "FY2021": 112076}),
]

bw.add_cash_flow_sheet(
    title="Bank of London and The Middle East plc — Statement of Cash Flows",
    subtitle="BLME plc, Bank-solo basis, £'000s. Full 5 years, no cash-flow exemption.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=80,
    source_height=280,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else "", rows_data, sources_text,
                         note=note, first_col_width=52, source_height=200)


metric("CET1 Capital", "£m",
       [("Common Equity Tier 1 (CET1) capital", {"FY2025": 225.806, "FY2024": 227.639, "FY2023": 226.478, "FY2022": 227.212, "FY2021": 238.839})],
       p3_sources())

metric("CET1 Ratio", "% of RWA",
       [("CET1 ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"})],
       p3_sources())

metric("Tier 1 Capital", "£m",
       [("Tier 1 capital", {"FY2025": 225.806, "FY2024": 227.639, "FY2023": 226.478, "FY2022": 227.212, "FY2021": 238.839})],
       p3_sources(), note="CET1 = Tier 1 = Total Capital every year - BLME has no Additional Tier 1 or Tier 2 instruments.")

metric("Tier 1 Ratio", "% of RWA",
       [("Tier 1 ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"})],
       p3_sources())

metric("Total Capital", "£m",
       [("Total capital", {"FY2025": 225.806, "FY2024": 227.639, "FY2023": 226.478, "FY2022": 227.212, "FY2021": 238.839})],
       p3_sources())

metric("Total Capital Ratio", "% of RWA",
       [("Total capital ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"})],
       p3_sources())

metric("Total RWAs", "£m",
       [("Total risk-weighted exposure amount", {"FY2025": 1170.428, "FY2024": 1279.034, "FY2023": 1342.418, "FY2022": 1376.389, "FY2021": 1313.776})],
       p3_sources())

metric("Leverage Ratio", "%",
       [("Leverage ratio (excluding claims on central banks)", {"FY2025": "14.95%", "FY2024": "14.98%", "FY2023": "14.88%", "FY2022": "14.00%", "FY2021": "14.92%"})],
       p3_sources(),
       note="No basis break across the 5 years - all figures are on the 'excluding claims on central banks' basis, "
            "unlike several other banks in this project where FY2021 sits on an older methodology.")

metric("LCR", "%",
       [("Liquidity Coverage Ratio (12-month average)", {"FY2025": "308%", "FY2024": "310%", "FY2023": "288%", "FY2022": "352%", "FY2021": "315%"})],
       p3_sources())

metric("NSFR", "%",
       [("Net Stable Funding Ratio", {"FY2025": "121%", "FY2024": "125%", "FY2023": "144%", "FY2022": "143%"})],
       p3_sources(),
       note="FY2021 shown as N/A in the FY2022 report's own comparative column - UK NSFR requirement not yet in "
            "force for the FY2021 reporting date.")

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "MREL is not mentioned in any of the 5 Pillar III Disclosures reviewed (searched "
                             "directly, no hits any year) - consistent with a bank of this size not being its "
                             "own resolution entity under the Bank of England's MREL framework."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities",
         {"FY2025": 24971, "FY2024": 38707, "FY2023": -7362, "FY2022": -3137, "FY2021": -146085}),
        ("Net cash from/(used in) investing activities",
         {"FY2025": 16028, "FY2024": -23922, "FY2023": -51152, "FY2022": 26767, "FY2021": 31053}),
        ("Net cash from/(used in) financing activities",
         {"FY2025": -577, "FY2024": -589, "FY2023": -719, "FY2022": -1123, "FY2021": -1086}),
        ("Cash and cash equivalents at end of period",
         {"FY2025": 130528, "FY2024": 90139, "FY2023": 76008, "FY2022": 135262, "FY2021": 112076}),
    ],
    cash_flow_unit="£'000s",
    ratios=[
        ("CET1 Ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"}),
        ("Tier 1 Ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"}),
        ("Total Capital Ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"}),
        ("Leverage Ratio", {"FY2025": "14.95%", "FY2024": "14.98%", "FY2023": "14.88%", "FY2022": "14.00%", "FY2021": "14.92%"}),
        ("LCR", {"FY2025": "308%", "FY2024": "310%", "FY2023": "288%", "FY2022": "352%", "FY2021": "315%"}),
        ("NSFR", {"FY2025": "121%", "FY2024": "125%", "FY2023": "144%", "FY2022": "143%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. NSFR blank for FY2021 (not yet in force). BLME plc solo basis "
         "throughout, not the wider BLME Holdings group.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BLME FINANCIALS.xlsx")
