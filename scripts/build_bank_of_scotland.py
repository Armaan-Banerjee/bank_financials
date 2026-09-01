import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, all 12mo to 31 Dec
YEAR_LABEL = {y: y for y in YEARS}

# All 5 years sourced directly from Bank of Scotland plc's own Companies House
# full accounts filings (each year's own originally-filed document, not a
# later comparative) - the bank's own investor-relations site (lloydsbankinggroup.com)
# blocked automated fetches throughout this build.
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/SC327000/filing-history/MzUxMDk3MTM2NGFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/SC327000/filing-history/MzQ2MDQ2MzkxNmFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/SC327000/filing-history/MzQxNzI4ODY0NmFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/SC327000/filing-history/MzM3NTQ1ODI2M2FkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/SC327000/filing-history/MzMzNTAwMTQxNWFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank of Scotland plc (Companies House SC327000, FRN 169628) is a major UK high-street bank, "
    "wholly owned by Lloyds Banking Group plc - not to be confused with the separate PRA-authorised entity "
    "'Lloyds Bank plc' (FRN 119278), also part of the same group but not yet attempted in this project. All 5 "
    "Companies House filings for this entity are fully scanned/image-only (no text layer at all) despite being a "
    "major bank - every figure below was located by rendering pages and reading them visually, not OCR'd or "
    "text-searched. The bank's own website (lloydsbankinggroup.com) returned a Cloudflare block (error 1007) on "
    "every automated fetch attempt, so no alternative text-native source was available. Every Annual Report "
    "presents both 'The Group' (consolidated, including subsidiaries) and 'The Bank' (Bank of Scotland plc "
    "unconsolidated) columns for both the cash flow statement and, separately, an explicit unconsolidated capital "
    "position for 'the Bank' in the Strategic Report - THE BANK (unconsolidated) basis is used throughout this "
    "workbook for consistency between the cash flow and capital/Pillar 3 sheets."
)

CASH_FLOW_NOTE = (
    "CASH FLOW NOTE - genuine definitional break, not an error: the FY2022 Annual Report restates the FY2021 "
    "comparative cash-and-cash-equivalents balances (Bank: opening £2,208m / closing £2,165m) far above FY2021's "
    "own originally-published figures (Bank: opening £847m / closing £854m) - a ~2.6x jump most likely reflecting "
    "a broadened definition of 'cash and cash equivalents' (e.g. additional short-term interbank placements folded "
    "in) rather than a transcription issue, alongside a much smaller (£50m) revision to the FY2021 operating-"
    "activities total (£6,414m originally vs. £6,364m restated). Per this project's convention, each column below "
    "uses that year's own originally-published figures, so the FY2021 and FY2022 columns are NOT on a directly "
    "comparable cash-equivalents basis at the opening/closing balance level - the activity subtotals (operating/"
    "investing/financing) are only mildly affected. An 'Effect of exchange rate changes on cash and cash "
    "equivalents' line appears in FY2021 and FY2022 only (small, non-zero) and was dropped from the statement "
    "entirely from FY2023 onward - presentation change, not a gap."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank of Scotland plc's own unconsolidated ('The Bank') cash flow statement, £m, "
    "from each year's own Companies House full accounts filing:\n"
    f"FY2025: Bank of Scotland plc Annual Report and Accounts 2025, p.26 (Cash flow statements) - {AR2025_URL}\n"
    f"FY2024: Bank of Scotland plc Annual Report and Accounts 2024, p.28 (Cash flow statements) - {AR2024_URL}\n"
    f"FY2023: Bank of Scotland plc Annual Report and Accounts 2023, p.29 (Cash flow statements) - {AR2023_URL}\n"
    f"FY2022: Bank of Scotland plc Annual Report and Accounts 2022, p.29 (Cash flow statements) - {AR2022_URL}\n"
    f"FY2021: Bank of Scotland plc Annual Report and Accounts 2021, p.27 (Cash flow statements) - {AR2021_URL}\n"
    "Each year cross-checked against its own report only (not blended with later comparatives) - see the Cash "
    "Flow Note below.\n\n"
    + CASH_FLOW_NOTE + "\n\n" + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Bank of Scotland plc's own unconsolidated ('The Bank') capital position, as stated in the "
        "'Capital position' section of the Strategic Report of each year's own Companies House full accounts "
        "filing (no standalone Pillar 3 document is published for this entity - see the Entity Note):\n"
        f"FY2025: Annual Report and Accounts 2025, p.2 - {AR2025_URL}\n"
        f"FY2024: Annual Report and Accounts 2024, p.2 - {AR2024_URL}\n"
        f"FY2023: Annual Report and Accounts 2023, p.2 - {AR2023_URL}\n"
        f"FY2022: Annual Report and Accounts 2022, p.2 - {AR2022_URL}\n"
        f"FY2021: Annual Report and Accounts 2021, p.2 - {AR2021_URL}\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Bank of Scotland plc", years=YEARS, year_label=YEAR_LABEL, header_color="003865")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 1896, "FY2024": 1015, "FY2023": 901, "FY2022": 1213, "FY2021": 2305}),
    ("DATA", "Change in operating assets", {"FY2025": -9007, "FY2024": -5430, "FY2023": -481, "FY2022": -6488, "FY2021": 2094}),
    ("DATA", "Change in operating liabilities", {"FY2025": 8052, "FY2024": 7275, "FY2023": 1135, "FY2022": 3169, "FY2021": 2275}),
    ("DATA", "Non-cash and other items", {"FY2025": -454, "FY2024": -346, "FY2023": -1434, "FY2022": 478, "FY2021": 251}),
    ("DATA", "Tax paid", {"FY2025": -296, "FY2024": -1364, "FY2023": -556, "FY2022": -208, "FY2021": -511}),
    ("DATA", "Tax refunded", {"FY2025": 942, "FY2024": 970}),
    ("TOTAL", "Net cash provided by/(used in) operating activities", {"FY2025": 1133, "FY2024": 2120, "FY2023": -435, "FY2022": -1836, "FY2021": 6414}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Dividends received from subsidiaries", {"FY2025": 406, "FY2024": 184, "FY2023": 719, "FY2022": 126, "FY2021": 49}),
    ("DATA", "Purchase of financial assets", {"FY2021": -107}),
    ("DATA", "Proceeds from sale and maturity of financial assets", {"FY2022": 1955, "FY2021": 399}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -172, "FY2024": -194, "FY2023": -219, "FY2022": -158, "FY2021": -171}),
    ("DATA", "Purchase of other intangible assets", {"FY2025": -114, "FY2024": -76}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 10, "FY2024": 36, "FY2023": 13, "FY2021": 41}),
    ("DATA", "Proceeds from goodwill and other intangible assets", {"FY2024": 1}),
    ("DATA", "Additional capital injections to subsidiaries", {"FY2025": -37}),
    ("TOTAL", "Net cash (used in)/provided by investing activities", {"FY2025": 93, "FY2024": -49, "FY2023": 513, "FY2022": 1923, "FY2021": 211}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid to ordinary shareholders", {"FY2025": -980, "FY2024": -1050, "FY2021": -1200}),
    ("DATA", "Distributions on other equity instruments", {"FY2025": -237, "FY2024": -206, "FY2023": -186, "FY2022": -122, "FY2021": -109}),
    ("DATA", "Interest paid on subordinated liabilities", {"FY2025": -96, "FY2024": -108, "FY2023": -105, "FY2022": -58, "FY2021": -94}),
    ("DATA", "Proceeds from issue of subordinated liabilities", {"FY2021": 500}),
    ("DATA", "Proceeds from issue of other equity instruments", {"FY2024": 1250, "FY2023": 350}),
    ("DATA", "Repayment of subordinated liabilities", {"FY2023": -63, "FY2022": -44, "FY2021": -5714}),
    ("DATA", "Repurchases and redemptions of other equity instruments", {"FY2024": -1200}),
    ("TOTAL", "Net cash used in/(provided by) financing activities", {"FY2025": -1313, "FY2024": -1314, "FY2023": -4, "FY2022": -224, "FY2021": -6617}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents", {"FY2022": -1, "FY2021": -1}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2025": -87, "FY2024": 757, "FY2023": 74, "FY2022": -138, "FY2021": 7}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 2858, "FY2024": 2101, "FY2023": 2027, "FY2022": 2165, "FY2021": 847}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 2771, "FY2024": 2858, "FY2023": 2101, "FY2022": 2027, "FY2021": 854}),
]

bw.add_cash_flow_sheet(
    title="Bank of Scotland plc — Cash Flow Statement",
    subtitle="Unconsolidated ('The Bank') basis, £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 / capital metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Unconsolidated ('The Bank') basis, {unit}" if unit else "Unconsolidated ('The Bank') basis",
                         rows_data, p3_sources(), note=note, first_col_width=48, source_height=180)


metric(
    "CET1 Capital", "£m",
    [("Common equity tier 1 capital", {"FY2025": 11083, "FY2024": 11028, "FY2023": 11966, "FY2022": 11284, "FY2021": 9540})],
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common equity tier 1 capital ratio", {"FY2025": "13.5%", "FY2024": "13.5%", "FY2023": "14.9%", "FY2022": "15.4%", "FY2021": "15.7%"})],
)

metric(
    "Tier 1 Capital", "£m",
    [("Total tier 1 capital", {"FY2025": 13683, "FY2024": 13628, "FY2023": 14516, "FY2022": 13484, "FY2021": 11762})],
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 capital ratio", {"FY2025": "16.6%", "FY2024": "16.7%", "FY2023": "18.1%", "FY2022": "18.5%", "FY2021": "19.3%"})],
)

metric(
    "Total Capital", "£m",
    [("Total capital resources", {"FY2025": 15183, "FY2024": 15402, "FY2023": 16410, "FY2022": 15330, "FY2021": 13259})],
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "18.4%", "FY2024": "18.9%", "FY2023": "20.4%", "FY2022": "21.0%", "FY2021": "21.8%"})],
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets", {"FY2025": 82357, "FY2024": 81493, "FY2023": 80254, "FY2022": 73084, "FY2021": 60807})],
)

metric(
    "Leverage Ratio", "%",
    [("UK leverage ratio", {"FY2025": "4.3%", "FY2024": "4.4%", "FY2023": "4.8%", "FY2022": "4.5%"})],
    note="Not disclosed in FY2021's own Annual Report, nor in FY2022's own Annual Report (the FY2022 capital "
         "table has no leverage-ratio row at all) - the UK leverage ratio template was only introduced to this "
         "entity's own disclosure from the FY2023 Annual Report onward. The FY2022 figure (4.5%) shown here comes "
         "from FY2023's report, which is the first to show it as a prior-year comparative; FY2021 is left blank "
         "since no source (that year's own report or the following year's comparative) ever discloses it.",
)

bw.add_not_disclosed_metric_sheets(
    ["LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={
        "LCR": "Bank of Scotland plc's own Annual Report contains no dedicated risk-management/liquidity "
               "disclosure section and no standalone Pillar 3 document is published for this entity - LCR is "
               "disclosed only at the wider Lloyds Banking Group plc consolidated level, which is out of scope "
               "for this entity-level workbook.",
        "NSFR": "Same as the LCR note - not disclosed at this entity level.",
        "MREL Ratio": "Same as the LCR note - not disclosed at this entity level; MREL is set and disclosed at "
                      "the Lloyds Banking Group plc resolution-group level, not for Bank of Scotland plc solo.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash provided by/(used in) operating activities", {"FY2025": 1133, "FY2024": 2120, "FY2023": -435, "FY2022": -1836, "FY2021": 6414}),
        ("Net cash (used in)/provided by investing activities", {"FY2025": 93, "FY2024": -49, "FY2023": 513, "FY2022": 1923, "FY2021": 211}),
        ("Net cash used in/(provided by) financing activities", {"FY2025": -1313, "FY2024": -1314, "FY2023": -4, "FY2022": -224, "FY2021": -6617}),
        ("Cash and cash equivalents at end of year", {"FY2025": 2771, "FY2024": 2858, "FY2023": 2101, "FY2022": 2027, "FY2021": 854}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "13.5%", "FY2024": "13.5%", "FY2023": "14.9%", "FY2022": "15.4%", "FY2021": "15.7%"}),
        ("Tier 1 Ratio", {"FY2025": "16.6%", "FY2024": "16.7%", "FY2023": "18.1%", "FY2022": "18.5%", "FY2021": "19.3%"}),
        ("Total Capital Ratio", {"FY2025": "18.4%", "FY2024": "18.9%", "FY2023": "20.4%", "FY2022": "21.0%", "FY2021": "21.8%"}),
        ("Leverage Ratio", {"FY2025": "4.3%", "FY2024": "4.4%", "FY2023": "4.8%", "FY2022": "4.5%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. LCR/NSFR/MREL are not shown here (not disclosed at "
         "this entity level - see those sheets). The FY2021-to-FY2022 cash-flow figures are not on a directly "
         "comparable cash-equivalents basis - see the Cash Flow Statement sheet's note.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF SCOTLAND FINANCIALS.xlsx")
