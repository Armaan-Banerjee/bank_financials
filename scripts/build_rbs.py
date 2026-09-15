import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/rbs-annual-report.pdf"
AR2024_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/14022025/rbs-plc-annual-report.pdf"
AR2023_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/16022024/rbs-plc-annual-report.pdf"
AR2022_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/rbs-plc-annual-report.pdf"
AR2021_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/18022022/rbs-plc-annual-report-2021.pdf"

# UK DoLSub liquidity (LCR/NSFR) is disclosed by NatWest Holdings Group, not by
# RBS plc - see liquidity_sources() and the LCR sheet note.
NWH_AR2025_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwh-annual-report.pdf"
NWH_AR2024_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/14022025/nwh-annual-report.pdf"

P3_2025_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/rbs-pillar-3-report.pdf"
P3_2024_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/14022025/rbs-plc-pillar-3-report.pdf"
P3_2023_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/16022024/rbs-plc-pillar-3-report.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: The Royal Bank of Scotland Public Limited Company ('RBS plc', company number SC083026, FRN "
    "114724, LEI 549300WHU4EIHRP28H10) is a large, PRA-authorised subsidiary of NatWest Group plc (formerly The "
    "Royal Bank of Scotland Group plc). IMPORTANT LINEAGE NOTE: company SC083026 was originally incorporated on 9 "
    "May 1983 as 'Adam & Company Public Limited Company' (a private banking subsidiary) and was renamed 'The Royal "
    "Bank of Scotland Public Limited Company' on 29 April 2018, as part of the ring-fencing reforms that split "
    "NatWest Group's retail/commercial banking (ring-fenced) from investment banking (non-ring-fenced) activities. "
    "The pre-2018 entity that historically traded as 'The Royal Bank of Scotland plc' (the 1727-founded bank, "
    "formerly the whole group's principal operating subsidiary) was itself renamed 'NatWest Markets Plc' at the "
    "same time and continues today as NatWest Group's investment banking subsidiary - it is NOT the entity covered "
    "by this workbook. This workbook covers the entity that currently and continuously holds the exact name 'The "
    "Royal Bank of Scotland Public Limited Company' (confirmed via Companies House and the FCA/PRA Financial "
    "Services Register, and matching the FRN and LEI listed in this project's source bank list) - i.e. the "
    "ring-fenced retail/commercial banking entity operating under the RBS brand in Scotland and Northern Ireland, "
    "not the original historic RBS legal entity. Flagged here prominently given the scale of the institution and "
    "the potential for this lineage to be confused with NatWest Markets Plc.\n\n"
    "RBS plc is a member of the 'UK DoLSub' (UK Domestic Liquidity Sub-Group) alongside National Westminster Bank "
    "Plc and Coutts & Company; under a PRA waiver, liquidity (LCR/NSFR) is managed and disclosed at this sub-group "
    "level rather than at the individual RBS plc entity level - the LCR/NSFR figures on those sheets are UK DoLSub "
    "figures, consistently across every year in this workbook, not RBS plc solo. From FY2024 onward, RBS plc's own "
    "Annual Report and Pillar 3 Report no longer state a numeric UK DoLSub LCR/NSFR at all (that disclosure moved "
    "entirely to NatWest Holdings Group's own reports) - so FY2024/FY2025 are not a gap in RBS plc's own reporting. "
    "The UK DoLSub is a liquidity sub-group of which RBS plc is a constituent, NOT the NatWest Holdings Group or "
    "NatWest Group consolidated entity; taking the UK DoLSub figure from a NatWest Holdings Group document "
    "therefore continues the same sub-group measure this workbook has always used, and is not a substitution of a "
    "parent-group figure into an entity-level sheet. FY2024 UK DoLSub spot LCR/NSFR are recorded on that basis. "
    "FY2025 spot is genuinely unpublished - NatWest Holdings Group dropped the Spot column from FY2025 and now "
    "reports these metrics on an average basis only - so the FY2025 figures appear on the separate average-basis "
    "row instead. See the LCR sheet note for the spot-vs-average distinction, which is material (11 points apart "
    "for FY2023)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are RBS plc's own Cash flow statement, £m:\n"
    f"FY2025: RBS plc Annual Report and Accounts 2025, p.85 (Cash flow statement) - {AR2025_URL}\n"
    f"FY2024: RBS plc Annual Report and Accounts 2024, p.89 (Cash flow statement) - {AR2024_URL}\n"
    f"FY2023: RBS plc Annual Report and Accounts 2023, p.90 (Cash flow statement) - {AR2023_URL}\n"
    f"FY2022: RBS plc Annual Report and Accounts 2022, p.98 (Cash flow statement) - {AR2022_URL}\n"
    f"FY2021: RBS plc Annual Report and Accounts 2022, p.98 (FY2021 comparative column of the same statement; "
    f"independently cross-checked against RBS plc Annual Report and Accounts 2021, p.91, own-year statement, which "
    f"gives an identical operating-activities total of £15,792m) - {AR2022_URL}\n"
    "Presentation note: FY2021-FY2022 annual reports itemise cash flows from operating activities in full detail "
    "(individual adjustments, changes in each operating asset/liability class); FY2023-FY2025 reports condense "
    "these into two note-referenced lines ('Non-cash and other items' and 'Changes in operating assets and "
    "liabilities', detailed in Note 21/22 rather than the face statement). Each year's own as-published presentation "
    "is preserved below rather than forced into a common format. The full opening-to-closing cash chain reconciles "
    "exactly across all 5 years (FY2021 opening £46,426m through FY2025 closing £48,316m).\n\n"
    + ENTITY_NOTE
)


def liquidity_sources():
    """Citations for the LCR/NSFR sheets.

    These differ from p3_sources() because UK DoLSub liquidity is not disclosed
    in RBS plc's own Pillar 3 Report at all - its UK KM1 rows 15-20 are blank in
    every year, footnoted to the sub-group waiver, with UK LIQ1/LIQB/LIQ2 marked
    'Refer to the NatWest Holdings Group Pillar 3 report'.
    """
    return (
        "Sources - UK DoLSub sub-group basis (RBS plc + National Westminster Bank Plc + Coutts & Company):\n"
        "SPOT (point-in-time at 31 December) row:\n"
        f"  FY2024: NatWest Holdings Group Annual Report and Accounts 2024, 'Liquidity key metrics' table (Risk and "
        f"capital management - Capital, liquidity and funding risk), UK DoLSub 'Spot' column - LCR 142%, NSFR 129% "
        f"- {NWH_AR2024_URL}\n"
        f"  FY2023: RBS plc Annual Report and Accounts 2023, p.57 ('Liquidity key metrics', UK DoLSub) - LCR 138%, "
        f"NSFR 126%. Independently corroborated by the NatWest Holdings Group Annual Report and Accounts 2024, whose "
        f"2023 UK DoLSub 'Spot' column gives the identical 138%/126% (and whose 2023 'Average' column gives a "
        f"materially different 127%/129%, which is what establishes that this workbook's pre-FY2024 series is the "
        f"spot measure) - {AR2023_URL}\n"
        f"  FY2022: RBS plc Annual Report and Accounts 2023, p.57 (2022 comparative block of the same 'Liquidity key "
        f"metrics' table) - {AR2023_URL}\n"
        f"  FY2021: RBS plc Annual Report and Accounts 2021 ('Liquidity key metrics', UK DoLSub) - {AR2021_URL}\n"
        "AVERAGE row:\n"
        f"  FY2025: NatWest Holdings Group Annual Report and Accounts 2025, 'Liquidity key metrics' table, UK DoLSub "
        f"column - LCR 135% (average of the preceding 12 months), NSFR 129% (average of the preceding four "
        f"quarters). This table is stated 'on an average basis' and no longer carries a Spot column - "
        f"{NWH_AR2025_URL}\n"
        f"  FY2024/FY2023: NatWest Holdings Group Annual Report and Accounts 2024, 'Liquidity key metrics' table, UK "
        f"DoLSub 'Average' columns - {NWH_AR2024_URL}\n"
        "Cross-check: the NatWest Holdings Group Pillar 3 Report 2025's UK LIQ1 (Quantitative information of LCR) "
        "and UK LIQ2 (Net Stable Funding Ratio) tables, UK DoLSub sections, independently give a 31 December 2025 "
        "12-month-average LCR of 135% and an NSFR of 129% (ASF GBP353,089m / RSF GBP273,869m = 128.9%), matching the "
        "average row above - "
        "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwh-pillar-3-report.pdf\n"
        "Checked 15 September 2026: RBS plc's own Annual Report and Accounts 2025 replaces the former 'Liquidity key "
        "metrics' figures with the 100% minimum-requirement table only, stating that disclosures relating to these "
        "metrics 'are completed at UK DoLSub level and published in the NatWest Holdings Group 2025 Annual Report "
        "and Accounts'.\n\n"
        + ENTITY_NOTE
    )


def p3_sources(cap_source="AR own-report 'Capital, RWAs and leverage' table (Risk and capital management section)"):
    return (
        "Sources - RBS plc entity-level basis (PRA transitional basis):\n"
        f"FY2025: RBS plc Pillar 3 Report 2025, p.6 (UK KM1: Key metrics) - {P3_2025_URL}\n"
        f"FY2024: RBS plc Pillar 3 Report 2024, p.7 (UK KM1: Key metrics) - {P3_2024_URL}\n"
        f"FY2023: RBS plc Pillar 3 Report 2023, p.7 (UK KM1: Key metrics) - {P3_2023_URL}\n"
        f"FY2022: RBS plc Annual Report and Accounts 2023, p.57 ('{cap_source}', FY2022 comparative column - RBS "
        f"plc's own FY2022 Annual Report p.61/p.124 gives the CET1 capital, CET1 ratio, RWA and leverage figures "
        f"directly but not a single consolidated Tier 1%/Total%/Total capital table; the FY2023 report's own "
        f"comparative column supplies those, and was independently cross-checked against the matching column in "
        f"RBS plc Pillar 3 Report 2023's UK KM1 table, which agrees exactly) - {AR2023_URL}\n"
        f"FY2021: RBS plc Annual Report and Accounts 2021, p.61 ('{cap_source}') - {AR2021_URL}\n"
        "No standalone RBS plc Pillar 3 Report exists for FY2021/FY2022 (RBS plc's large-subsidiary Pillar 3 "
        "disclosures were embedded within the wider NatWest Holdings Group Pillar 3 Report those years); RBS plc "
        "began publishing its own standalone Pillar 3 Report from FY2023 onward. Ratios prior to FY2025 include an "
        "IFRS 9 transitional adjustment for ECL provisions (ceased 1 January 2025) - see each source document's own "
        "footnotes for the equivalent fully-loaded figures."
    )


bw = BankWorkbook(bank_name="The Royal Bank of Scotland Public Limited Company", years=YEARS, year_label=YEAR_LABEL,
                   header_color="264653")

# ---------------------------------------------------------------
# Statement sources - RBS plc entity-level basis, £m, own-report figures for
# each year (each year's own Annual Report Financial statements section),
# independently cross-checked against the following/preceding year's report's
# comparative column - all ties exactly across all 5 years for Balance Sheet
# Total assets/Total liabilities/Total equity, Profit for the year, and Total
# comprehensive income. Zero undocumented plug rows anywhere.
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - RBS plc entity-level basis, £m:\n"
    f"FY2025: RBS plc Annual Report and Accounts 2025, p.82 (Income statement / Statement of comprehensive income), "
    f"p.83 (Balance sheet), p.84 (Statement of changes in equity) - {AR2025_URL}\n"
    f"FY2024: RBS plc Annual Report and Accounts 2024, p.86 (Income statement / Statement of comprehensive income), "
    f"p.87 (Balance sheet), p.88 (Statement of changes in equity) - {AR2024_URL}\n"
    f"FY2023: RBS plc Annual Report and Accounts 2023, p.87 (Income statement / Statement of comprehensive income), "
    f"p.88 (Balance sheet), p.89 (Statement of changes in equity) - {AR2023_URL}\n"
    f"FY2022: RBS plc Annual Report and Accounts 2022, p.95 (Income statement / Statement of comprehensive income), "
    f"p.96 (Balance sheet), p.97 (Statement of changes in equity) - {AR2022_URL}\n"
    f"FY2021: RBS plc Annual Report and Accounts 2021, p.88 (Income statement / Statement of comprehensive income), "
    f"p.89 (Balance sheet), p.90 (Statement of changes in equity) - independently cross-checked against RBS plc "
    f"Annual Report and Accounts 2022's FY2021 comparative column, which agrees exactly on every line - {AR2021_URL}\n"
    "Presentation note: FY2025's Statement of changes in equity no longer discloses a separate FVOCI reserve line "
    "(nil since FY2024 year-end, folded away); FY2025's income statement drops the 'Items that do not qualify for "
    "reclassification' sub-heading used in FY2023-FY2024 (that sub-total was nil or near-nil in every year it "
    "appeared). Each year's own as-published structure is preserved rather than forced into a common format.\n\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below.
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 25590, "FY2024": 26630, "FY2023": 23984, "FY2022": 34323, "FY2021": 38014}),
    ("DATA", "Derivatives", {"FY2025": 535, "FY2024": 465, "FY2023": 623, "FY2022": 498, "FY2021": 220}),
    ("DATA", "Loans to banks - amortised cost", {"FY2025": 420, "FY2024": 484, "FY2023": 1059, "FY2022": 1071, "FY2021": 1147}),
    ("DATA", "Loans to customers - amortised cost", {"FY2025": 33531, "FY2024": 33524, "FY2023": 34805, "FY2022": 37667, "FY2021": 42035}),
    ("DATA", "Amounts due from holding companies and fellow subsidiaries", {"FY2025": 34340, "FY2024": 28060, "FY2023": 28497, "FY2022": 21722, "FY2021": 23941}),
    ("DATA", "Other assets", {"FY2025": 946, "FY2024": 1313, "FY2023": 1421, "FY2022": 1382, "FY2021": 738}),
    ("TOTAL", "Total assets", {"FY2025": 95362, "FY2024": 90476, "FY2023": 90389, "FY2022": 96663, "FY2021": 106095}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Bank deposits", {"FY2025": 861, "FY2024": 921, "FY2023": 1027, "FY2022": 986, "FY2021": 1117}),
    ("DATA", "Customer deposits", {"FY2025": 78399, "FY2024": 78069, "FY2023": 77504, "FY2022": 83306, "FY2021": 92144}),
    ("DATA", "Amounts due to holding companies and fellow subsidiaries", {"FY2025": 8760, "FY2024": 3755, "FY2023": 3577, "FY2022": 3910, "FY2021": 5216}),
    ("DATA", "Derivatives", {"FY2025": 599, "FY2024": 1411, "FY2023": 1932, "FY2022": 2683, "FY2021": 827}),
    ("DATA", "Notes in circulation", {"FY2025": 2115, "FY2024": 2381, "FY2023": 2430, "FY2022": 2409, "FY2021": 2144}),
    ("DATA", "Other liabilities", {"FY2025": 970, "FY2024": 690, "FY2023": 816, "FY2022": 708, "FY2021": 900}),
    ("TOTAL", "Total liabilities", {"FY2025": 91704, "FY2024": 87227, "FY2023": 87286, "FY2022": 94002, "FY2021": 102348}),
    ("SECTION", "Equity", {}),
    ("TOTAL", "Total equity", {"FY2025": 3658, "FY2024": 3249, "FY2023": 3103, "FY2022": 2661, "FY2021": 3747}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 95362, "FY2024": 90476, "FY2023": 90389, "FY2022": 96663, "FY2021": 106095}),
]

bw.add_balance_sheet_sheet(
    title="The Royal Bank of Scotland Public Limited Company — Balance Sheet",
    subtitle="RBS plc entity-level basis, £m. Total assets = Total liabilities + Total equity for every year; "
              "Total equity ties exactly to the Statement of Changes in Equity sheet's own opening/closing "
              "balances - zero plug rows.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=230,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss (Income statement + Statement of comprehensive income)
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 3462, "FY2024": 3539, "FY2023": 3324, "FY2022": 2036, "FY2021": 1449}),
    ("DATA", "Interest payable", {"FY2025": -1391, "FY2024": -1591, "FY2023": -1231, "FY2022": -254, "FY2021": -107}),
    ("TOTAL", "Net interest income", {"FY2025": 2071, "FY2024": 1948, "FY2023": 2093, "FY2022": 1782, "FY2021": 1342}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 441, "FY2024": 442, "FY2023": 440, "FY2022": 455, "FY2021": 413}),
    ("DATA", "Fees and commissions payable", {"FY2025": -105, "FY2024": -88, "FY2023": -93, "FY2022": -107, "FY2021": -135}),
    ("DATA", "Other operating income", {"FY2025": 103, "FY2024": -25, "FY2023": 93, "FY2022": -59, "FY2021": 155}),
    ("TOTAL", "Non-interest income", {"FY2025": 439, "FY2024": 329, "FY2023": 440, "FY2022": 289, "FY2021": 433}),
    ("TOTAL", "Total income", {"FY2025": 2510, "FY2024": 2277, "FY2023": 2533, "FY2022": 2071, "FY2021": 1775}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -51, "FY2024": -51, "FY2023": -54, "FY2022": -58, "FY2021": -120}),
    ("DATA", "Premises and equipment", {"FY2025": -2, "FY2024": -1, "FY2023": 1, "FY2022": 1, "FY2021": -32}),
    ("DATA", "Other administrative expenses", {"FY2025": -746, "FY2024": -800, "FY2023": -835, "FY2022": -814, "FY2021": -838}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -11, "FY2024": -19, "FY2023": -13, "FY2022": -21, "FY2021": -124}),
    ("TOTAL", "Operating expenses", {"FY2025": -810, "FY2024": -871, "FY2023": -901, "FY2022": -892, "FY2021": -1114}),
    ("TOTAL", "Profit before impairment losses", {"FY2025": 1700, "FY2024": 1406, "FY2023": 1632, "FY2022": 1179, "FY2021": 661}),
    ("DATA", "Impairment losses/(releases)", {"FY2025": -29, "FY2024": -17, "FY2023": -44, "FY2022": -20, "FY2021": 360}),
    ("TOTAL", "Operating profit before tax", {"FY2025": 1671, "FY2024": 1389, "FY2023": 1588, "FY2022": 1159, "FY2021": 1021}),
    ("DATA", "Tax (charge)/credit", {"FY2025": -416, "FY2024": -209, "FY2023": -189, "FY2022": 17, "FY2021": -245}),
    ("TOTAL", "Profit for the year", {"FY2025": 1255, "FY2024": 1180, "FY2023": 1399, "FY2022": 1176, "FY2021": 776}),
    ("DATA", "Attributable to ordinary shareholders", {"FY2025": 1221, "FY2024": 1146, "FY2023": 1352, "FY2022": 1122, "FY2021": 722}),
    ("DATA", "Attributable to paid-in equity holders", {"FY2025": 34, "FY2024": 34, "FY2023": 47, "FY2022": 54, "FY2021": 54}),
    ("SECTION", "Other comprehensive income, net of tax", {}),
    ("DATA", "Items not qualifying for reclassification - tax", {"FY2024": 0, "FY2023": -1}),
    ("DATA", "FVOCI financial assets", {"FY2024": 0, "FY2023": -1, "FY2022": 0, "FY2021": 1}),
    ("DATA", "Cash flow hedges", {"FY2025": 631, "FY2024": 277, "FY2023": 1030, "FY2022": -1803, "FY2021": -766}),
    ("DATA", "Currency translation", {"FY2025": 0, "FY2024": 1, "FY2023": -1, "FY2022": 2, "FY2021": -2}),
    ("DATA", "Tax on items qualifying for reclassification", {"FY2025": -177, "FY2024": -78, "FY2023": -288, "FY2022": 492, "FY2021": 222}),
    ("TOTAL", "Other comprehensive income/(loss) after tax", {"FY2025": 454, "FY2024": 200, "FY2023": 739, "FY2022": -1309, "FY2021": -545}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 1709, "FY2024": 1380, "FY2023": 2138, "FY2022": -133, "FY2021": 231}),
]

bw.add_income_statement_sheet(
    title="The Royal Bank of Scotland Public Limited Company — Profit & Loss",
    subtitle="RBS plc entity-level basis, £m. 'Total comprehensive income/(loss) for the year' ties exactly to "
              "Profit for the year + Other comprehensive income for every year. FY2025 no longer discloses an "
              "FVOCI reserve/items-not-qualifying line (nil since FY2024 year-end) - see source note.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=230,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - equity reconciliation ladder steps 2-3:
# built year-by-year, confirmed against next year's opening AND that year's
# own Balance Sheet Total equity above (all 5 years tie exactly - see the
# checks embedded in the session notes). Zero undocumented plug rows.
# ---------------------------------------------------------------
EQUITY_HEADERS = [
    "Share capital", "Paid-in equity", "FVOCI reserve", "Cash flow hedging reserve",
    "Foreign exchange reserve", "Retained earnings", "Total equity",
]

equity_rows = [
    ("TOTAL", "Balance at 1 January 2021", (20, 969, -4, 376, 0, 4309, 5670)),
    ("DATA", "Profit attributable to ordinary shareholders and other equity owners", (None, None, None, None, None, 776, 776)),
    ("DATA", "FVOCI reserve movements (unrealised gains, tax)", (None, None, 1, None, None, None, 1)),
    ("DATA", "Cash flow hedging reserve movements (recognised in equity, transferred to earnings, tax)", (None, None, None, -544, None, None, -544)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, -2, None, -2)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, -2100, -2100)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, -54, -54)),
    ("TOTAL", "Balance at 31 December 2021 / 1 January 2022", (20, 969, -3, -168, -2, 2931, 3747)),
    ("DATA", "Redemption of paid-in equity", (None, -499, None, None, None, None, -499)),
    ("DATA", "Issue of paid-in equity", (None, 500, None, None, None, None, 500)),
    ("DATA", "Profit attributable to ordinary shareholders and other equity owners", (None, None, None, None, None, 1176, 1176)),
    ("DATA", "Cash flow hedging reserve movements (recognised in equity, transferred to earnings, tax)", (None, None, None, -1311, None, None, -1311)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, 2, None, 2)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, -850, -850)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, -54, -54)),
    ("DATA", "Redemption of paid-in equity - retained earnings impact (gross, tax)", (None, None, None, None, None, -50, -50)),
    ("TOTAL", "Balance at 31 December 2022 / 1 January 2023", (20, 970, -3, -1479, 0, 3153, 2661)),
    ("DATA", "Redemption of paid-in equity", (None, -470, None, None, None, None, -470)),
    ("DATA", "Profit attributable to ordinary shareholders and other equity owners", (None, None, None, None, None, 1399, 1399)),
    ("DATA", "FVOCI reserve movements (unrealised/realised losses, tax)", (None, None, 3, None, None, None, 3)),
    ("DATA", "Cash flow hedging reserve movements (recognised in equity, transferred to earnings, tax)", (None, None, None, 742, None, None, 742)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, -1, None, -1)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, -1136, -1136)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, -47, -47)),
    ("DATA", "Redemption of paid-in equity - retained earnings impact (gross)", (None, None, None, None, None, -43, -43)),
    ("DATA", "Realised losses in period on FVOCI equity shares (gross)", (None, None, None, None, None, -5, -5)),
    ("TOTAL", "Balance at 31 December 2023 / 1 January 2024", (20, 500, 0, -737, -1, 3321, 3103)),
    ("DATA", "Profit attributable to ordinary shareholders and other equity owners", (None, None, None, None, None, 1180, 1180)),
    ("DATA", "Cash flow hedging reserve movements (recognised in equity, transferred to earnings, tax)", (None, None, None, 199, None, None, 199)),
    ("DATA", "Foreign exchange reserve movements (retranslation, recycled to P&L)", (None, None, None, None, 1, None, 1)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, -1200, -1200)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, -34, -34)),
    ("TOTAL", "Balance at 31 December 2024 / 1 January 2025", (20, 500, 0, -538, 0, 3267, 3249)),
    ("DATA", "Profit attributable to ordinary shareholders and other equity owners", (None, None, None, None, None, 1255, 1255)),
    ("DATA", "Cash flow hedging reserve movements (recognised in equity, reclassified to P&L, tax)", (None, None, None, 454, None, None, 454)),
    ("DATA", "Foreign exchange reserve movements (retranslation, recycled to P&L)", (None, None, None, None, 0, None, 0)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, -1266, -1266)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, -34, -34)),
    ("TOTAL", "Balance at 31 December 2025", (20, 500, 0, -84, 0, 3222, 3658)),
]

bw.add_equity_changes_sheet(
    title="The Royal Bank of Scotland Public Limited Company — Statement of Changes in Equity",
    subtitle="RBS plc entity-level basis, £m, chronological (oldest to newest). Each year's closing Total equity "
              "ties exactly to that year's own Balance Sheet Total equity and to the next year's opening balance - "
              "zero undocumented plug rows across all 5 years.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=50,
    source_height=230,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Operating profit before tax", {"FY2025": 1671, "FY2024": 1389, "FY2023": 1588, "FY2022": 1159, "FY2021": 1021}),
    ("DATA", "Non-cash and other items (Note 21/22)", {"FY2025": 609, "FY2024": 1138, "FY2023": 1255}),
    ("DATA", "Impairment losses/(releases)", {"FY2022": 20, "FY2021": -360}),
    ("DATA", "Depreciation and amortisation", {"FY2022": 21, "FY2021": 124}),
    ("DATA", "Write-down of investment in group undertakings", {"FY2022": 0, "FY2021": 3}),
    ("DATA", "Change in fair value taken to profit or loss on other liabilities and subordinated liabilities", {"FY2022": -110, "FY2021": -67}),
    ("DATA", "Elimination of foreign exchange differences", {"FY2022": -336, "FY2021": 37}),
    ("DATA", "Other non-cash items", {"FY2022": 158, "FY2021": -199}),
    ("DATA", "Dividends receivable from subsidiaries", {"FY2022": -8, "FY2021": -22}),
    ("DATA", "Profit on sale of subsidiaries and associates", {"FY2022": 0, "FY2021": -34}),
    ("DATA", "Loss/(profit) on sale of net assets/liabilities", {"FY2022": 24, "FY2021": -4}),
    ("DATA", "Loss/(profit) on sale of property, plant and equipment", {"FY2022": 1, "FY2021": -5}),
    ("DATA", "Interest payable on MRELs and subordinated liabilities", {"FY2022": 95, "FY2021": 86}),
    ("DATA", "Charges and releases on provisions", {"FY2022": -10, "FY2021": 67}),
    ("DATA", "Defined benefit pension schemes", {"FY2022": 7, "FY2021": 9}),
    ("TOTAL", "Net cash flows from trading activities (subtotal)", {"FY2022": 1021, "FY2021": 656}),
    ("DATA", "Increase in derivative assets", {"FY2022": -2230, "FY2021": -39}),
    ("DATA", "Increase in loans to banks", {"FY2022": -5, "FY2021": -44}),
    ("DATA", "Decrease in loans to customers", {"FY2022": 3750, "FY2021": 6928}),
    ("DATA", "Increase in amounts due from holding companies and fellow subsidiaries", {"FY2022": -2862, "FY2021": -285}),
    ("DATA", "Decrease in other assets", {"FY2022": 88, "FY2021": 34}),
    ("DATA", "Decrease in bank deposits", {"FY2022": -131, "FY2021": -35}),
    ("DATA", "(Decrease)/increase in customer deposits", {"FY2022": -6599, "FY2021": 7516}),
    ("DATA", "(Decrease)/increase in amounts due to holding companies and fellow subsidiaries", {"FY2022": -1073, "FY2021": 741}),
    ("DATA", "Increase in derivative liabilities", {"FY2022": 1856, "FY2021": 39}),
    ("DATA", "Increase in notes in circulation", {"FY2022": 265, "FY2021": 501}),
    ("DATA", "Decrease in other liabilities", {"FY2022": -205, "FY2021": -170}),
    ("TOTAL", "Changes in operating assets and liabilities (subtotal)", {"FY2025": -309, "FY2024": 769, "FY2023": -7837, "FY2022": -7146, "FY2021": 15186}),
    ("DATA", "Income tax paid", {"FY2025": 0, "FY2024": -339, "FY2023": -263, "FY2022": -228, "FY2021": -50}),
    ("TOTAL", "Net cash flows from operating activities", {"FY2025": 1971, "FY2024": 2957, "FY2023": -5257, "FY2022": -6353, "FY2021": 15792}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of other financial assets", {"FY2021": -1}),
    ("DATA", "Sale of property, plant and equipment", {"FY2025": 1, "FY2024": 3, "FY2023": 43, "FY2022": 8, "FY2021": 20}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -1, "FY2024": -5, "FY2023": -18, "FY2022": -21, "FY2021": -5}),
    ("DATA", "Disposal of net assets and liabilities", {"FY2023": 0, "FY2022": 270, "FY2021": 155}),
    ("DATA", "Profit on disposal of net assets and liabilities", {"FY2021": 4}),
    ("DATA", "Disposal of subsidiaries and associates", {"FY2022": 0, "FY2021": 54}),
    ("DATA", "Dividends received from subsidiaries", {"FY2025": 6, "FY2024": 0, "FY2023": 5, "FY2022": 8, "FY2021": 22}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": 6, "FY2024": -2, "FY2023": 30, "FY2022": 265, "FY2021": 249}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of paid-in equity", {"FY2023": 0}),
    ("DATA", "Redemption of paid-in equity", {"FY2024": 0, "FY2023": -513}),
    ("DATA", "Movement in paid-in equity (as reported)", {"FY2022": -40, "FY2021": 0}),
    ("DATA", "Issue of MRELs", {"FY2025": 0, "FY2024": 119}),
    ("DATA", "Redemption of MRELs", {"FY2025": 0, "FY2024": -397}),
    ("DATA", "Movement in MRELs (as reported)", {"FY2023": 991, "FY2022": -16, "FY2021": -16}),
    ("DATA", "Interest paid on MRELs", {"FY2025": -63, "FY2024": -71, "FY2023": -32}),
    ("DATA", "Issue of subordinated liabilities", {"FY2025": 0, "FY2024": 546}),
    ("DATA", "Redemption of subordinated liabilities", {"FY2025": 0, "FY2024": -381, "FY2023": -1059}),
    ("DATA", "Interest paid on subordinated liabilities", {"FY2025": -33, "FY2024": -39, "FY2023": -77}),
    ("DATA", "Movement in subordinated liabilities (as reported)", {"FY2022": -78, "FY2021": -70}),
    ("DATA", "Dividends paid", {"FY2025": -1300, "FY2024": -1234, "FY2023": -1183, "FY2022": -904, "FY2021": -2154}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": -1396, "FY2024": -1457, "FY2023": -1873, "FY2022": -1038, "FY2021": -2240}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2025": -81, "FY2024": -13, "FY2023": -198, "FY2022": 547, "FY2021": -19}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 500, "FY2024": 1485, "FY2023": -7298, "FY2022": -6579, "FY2021": 13782}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 47816, "FY2024": 46331, "FY2023": 53629, "FY2022": 60208, "FY2021": 46426}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 48316, "FY2024": 47816, "FY2023": 46331, "FY2022": 53629, "FY2021": 60208}),
]

bw.add_cash_flow_sheet(
    title="The Royal Bank of Scotland Public Limited Company — Cash Flow Statement",
    subtitle="RBS plc entity-level basis, £m. See source note for a lineage/entity-identity flag and a FY2021-2022 "
              "vs FY2023-2025 presentation-format change.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=230,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Asset Quality - loan book by IFRS 9 stage, own-report figures each year,
# independently cross-checked against the adjacent report's comparative
# column (identical). Note: this "Total loans - in scope of the IFRS 9 ECL
# framework" figure includes both loans to customers AND loans to banks
# amortised cost, on an in-scope-exposure basis that does not tie exactly to
# the Balance Sheet's "Loans to customers - amortised cost" line (a smaller,
# narrower figure) - a genuine, documented cross-statement presentation
# difference, not forced to tie.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans - amortised cost, in scope of the IFRS 9 ECL framework (£bn, rounded to 1dp as disclosed)", {}),
    ("DATA", "Gross loans - Stage 1", {"FY2025": 28.9, "FY2024": 29.6, "FY2023": 30.6, "FY2022": 30.4, "FY2021": 36.1}),
    ("DATA", "Gross loans - Stage 2", {"FY2025": 4.8, "FY2024": 4.3, "FY2023": 5.0, "FY2022": 8.1, "FY2021": 6.5}),
    ("DATA", "Gross loans - Stage 3 (non-performing)", {"FY2025": 0.9, "FY2024": 0.9, "FY2023": 1.0, "FY2022": 1.0, "FY2021": 1.0}),
    ("TOTAL", "Gross loans - Total loans in scope", {"FY2025": 34.6, "FY2024": 34.8, "FY2023": 36.6, "FY2022": 39.5, "FY2021": 43.6}),
    ("DATA", "ECL provisions - Stage 1", {"FY2025": 0.0, "FY2024": 0.1, "FY2023": 0.1, "FY2022": 0.1, "FY2021": 0.0}),
    ("DATA", "ECL provisions - Stage 2", {"FY2025": 0.1, "FY2024": 0.1, "FY2023": 0.1, "FY2022": 0.2, "FY2021": 0.3}),
    ("DATA", "ECL provisions - Stage 3", {"FY2025": 0.4, "FY2024": 0.4, "FY2023": 0.4, "FY2022": 0.3, "FY2021": 0.4}),
    ("TOTAL", "ECL provisions - Total", {"FY2025": 0.5, "FY2024": 0.6, "FY2023": 0.6, "FY2022": 0.6, "FY2021": 0.7}),
    ("DATA", "Net loans - Stage 1", {"FY2025": 28.9, "FY2024": 29.5, "FY2023": 30.5, "FY2022": 30.3, "FY2021": 36.1}),
    ("DATA", "Net loans - Stage 2", {"FY2025": 4.7, "FY2024": 4.2, "FY2023": 4.9, "FY2022": 7.9, "FY2021": 6.2}),
    ("DATA", "Net loans - Stage 3", {"FY2025": 0.5, "FY2024": 0.5, "FY2023": 0.6, "FY2022": 0.7, "FY2021": 0.6}),
    ("TOTAL", "Net loans - Total loans in scope", {"FY2025": 34.1, "FY2024": 34.2, "FY2023": 36.0, "FY2022": 38.9, "FY2021": 42.9}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross loans)", {"FY2025": "2.60%", "FY2024": "2.59%", "FY2023": "2.73%", "FY2022": "2.53%", "FY2021": "2.29%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", {"FY2025": "44.4%", "FY2024": "44.4%", "FY2023": "40.0%", "FY2022": "30.0%", "FY2021": "40.0%"}),
]

bw.add_asset_quality_sheet(
    title="The Royal Bank of Scotland Public Limited Company — Asset Quality",
    subtitle="RBS plc entity-level basis. Loans within IFRS 9 ECL framework scope, by stage. See source note for "
              "why this doesn't tie exactly to the Balance Sheet's Loans to customers line.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - RBS plc entity-level basis, 'Financial instruments within the scope of the IFRS 9 ECL "
        "framework' table:\n"
        f"FY2025: RBS plc Annual Report and Accounts 2025, p.26 - {AR2025_URL}\n"
        f"FY2024: RBS plc Annual Report and Accounts 2024, p.29 - {AR2024_URL}\n"
        f"FY2023: RBS plc Annual Report and Accounts 2023, p.29 - {AR2023_URL}\n"
        f"FY2022: RBS plc Annual Report and Accounts 2022, p.32 - {AR2022_URL}\n"
        f"FY2021: RBS plc Annual Report and Accounts 2021, p.32 - independently cross-checked against RBS plc "
        f"Annual Report and Accounts 2022's FY2021 comparative column, which agrees exactly - {AR2021_URL}\n"
        "Figures as disclosed at 1 decimal place (£bn); NPL/coverage ratios are derived from those rounded figures "
        "so carry the same rounding limitation.\n\n" + ENTITY_NOTE
    ),
    first_col_width=58,
    source_height=220,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=52, source_height=140)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1905, "FY2024": 1956, "FY2023": 2042, "FY2022": 2149, "FY2021": 2682})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "11.0%", "FY2024": "11.1%", "FY2023": "11.2%", "FY2022": "11.6%", "FY2021": "13.7%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 2405, "FY2024": 2456, "FY2023": 2542, "FY2022": 3119, "FY2021": 3651})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "13.8%", "FY2024": "14.0%", "FY2023": "13.9%", "FY2022": "16.8%", "FY2021": "18.6%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 2955, "FY2024": 3080, "FY2023": 2998, "FY2022": 4715, "FY2021": 5106})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "17.0%", "FY2024": "17.5%", "FY2023": "16.4%", "FY2022": "25.4%", "FY2021": "26.1%"})],
    p3_sources(),
    note="FY2022 to FY2023 shows a large apparent drop (25.4% to 16.4%) alongside Total capital falling from "
         "£4,715m to £2,998m - both figures are as independently stated in each year's own primary source and are "
         "internally consistent with that year's own CET1/Tier1/RWA figures (Tier 2 capital fell sharply, from "
         "£1,596m-equivalent to £456m, i.e. a real reduction in subordinated debt outstanding - RBS plc redeemed "
         "£1,059m of subordinated liabilities in FY2023, see Cash Flow Statement financing activities). Not a data "
         "error.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 17385, "FY2024": 17591, "FY2023": 18228, "FY2022": 18540, "FY2021": 19592})],
    p3_sources(),
)

# ---------------------------------------------------------------
# RWA Breakdown - Pillar 3 UK OV1 template (FY2022-FY2025); FY2021 uses the
# older CRR-era 4-category table (no standalone RBS plc Pillar 3 Report
# exists for FY2021 - see ENTITY_NOTE / p3_sources - so FY2021 is sourced
# from the Annual Report's own Capital/RWA table instead). All 5 years tie
# exactly to the Total RWAs metric above.
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (Pillar 3 UK OV1 template; FY2021 uses an older CRR-era 4-category "
                "structure - see source note)", {}),
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2025": 12867, "FY2024": 13757, "FY2023": 14887, "FY2022": 15136, "FY2021": 15634}),
    ("DATA", "Counterparty credit risk", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2025": 459, "FY2024": 195, "FY2023": 63, "FY2022": 0}),
    ("DATA", "Position, foreign exchange and commodities risk (market risk)", {"FY2025": 18, "FY2024": 21, "FY2023": 14, "FY2022": 8, "FY2021": 7}),
    ("DATA", "Operational risk", {"FY2025": 4041, "FY2024": 3618, "FY2023": 3264, "FY2022": 3396, "FY2021": 3951}),
    ("DATA", "Memo: amounts below thresholds for deduction (250% risk-weight; already included in Credit risk above, not additive)", {"FY2025": 88, "FY2024": 100, "FY2023": 95, "FY2022": 98}),
    ("TOTAL", "Total RWAs", {"FY2025": 17385, "FY2024": 17591, "FY2023": 18228, "FY2022": 18540, "FY2021": 19592}),
]

bw.add_rwa_breakdown_sheet(
    title="The Royal Bank of Scotland Public Limited Company — RWA Breakdown",
    subtitle="RBS plc entity-level basis, £m. The 'Memo' row is already included within Credit risk and must NOT "
              "be added when summing to Total RWAs (per the source template's own footnote) - the other 5 category "
              "rows sum exactly to Total RWAs for every year.",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Sources - RBS plc entity-level basis, UK OV1: Overview of risk-weighted exposure amounts:\n"
        f"FY2025: RBS plc Pillar 3 Report 2025, p.7 (UK OV1) - {P3_2025_URL}\n"
        f"FY2024: RBS plc Pillar 3 Report 2024, p.9 (UK OV1) - {P3_2024_URL}\n"
        f"FY2023: RBS plc Pillar 3 Report 2023, p.9 (UK OV1) - {P3_2023_URL}\n"
        f"FY2022: RBS plc Pillar 3 Report 2023, p.9 (UK OV1, FY2022 comparative column) - {P3_2023_URL}\n"
        f"FY2021: RBS plc Annual Report and Accounts 2021, p.61 ('Capital, RWAs and leverage' table - Credit risk/"
        f"Counterparty credit risk/Market risk/Operational risk/Total RWAs only; no standalone RBS plc Pillar 3 "
        f"Report exists for FY2021 - see the entity note) - {AR2021_URL}\n\n" + ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Leverage exposure - including claims on central banks (£m)", {"FY2021": 88670}),
        ("Leverage ratio - including claims on central banks (%)", {"FY2021": "4.1%"}),
        ("Leverage exposure - excluding claims on central banks (£m)", {"FY2025": 42877, "FY2024": 42687, "FY2023": 43770, "FY2022": 48957}),
        ("Leverage ratio - excluding claims on central banks (%)", {"FY2025": "5.6%", "FY2024": "5.8%", "FY2023": "5.8%", "FY2022": "6.4%"}),
    ],
    p3_sources(),
    note="Leverage ratio methodology changed from FY2022: RBS plc's Annual Report/Pillar 3 disclosures switched to "
         "an 'excluding claims on central banks' basis (higher leverage exposure denominator excluded, so a higher "
         "ratio) following the UK's new leverage ratio framework (published 8 October 2021, effective from 2022). "
         "FY2021 is shown as originally reported in the FY2021 Annual Report on the prior 'including claims on "
         "central banks' basis (4.1%, or 4.0% excluding an IFRS 9 transitional add-back) and is NOT directly "
         "comparable to FY2022 onward; a restated FY2021 figure of 7.0% on the newer excluding-central-banks basis "
         "appears only as a comparative in the FY2022 Annual Report's narrative and was not used here, to keep each "
         "year's own-report figure intact. RBS plc is not in scope of the minimum leverage ratio requirement (not "
         "an LREQ firm).",
)

metric(
    "LCR", "%",
    [
        ("Liquidity Coverage Ratio (%) - UK DoLSub, spot at 31 December",
         {"FY2024": "142%", "FY2023": "138%", "FY2022": "131%", "FY2021": "169%"}),
        ("Liquidity Coverage Ratio (%) - UK DoLSub, 12-month average",
         {"FY2025": "135%", "FY2024": "142%", "FY2023": "127%"}),
    ],
    liquidity_sources(),
    note="UK DoLSub (RBS plc + National Westminster Bank Plc + Coutts & Company) sub-group figure throughout, per "
         "the PRA waiver described in the entity note - RBS plc solo LCR is not disclosed at all in any year, and "
         "rows 15-17 of RBS plc's own UK KM1 table are printed blank in every year with the footnote 'Under the UK "
         "DoLSub waiver RBS plc liquidity is managed and disclosed at the sub-group level rather than entity "
         "level'.\n\n"
         "TWO BASES, DELIBERATELY KEPT AS SEPARATE ROWS. The spot row is the point-in-time ratio at 31 December; "
         "the average row is the average of the preceding 12 months. They are NOT interchangeable - for FY2023 the "
         "same sub-group is 138% spot but 127% average, an 11-point gap. FY2021-FY2023 spot figures come from RBS "
         "plc's own Annual Report; FY2024 spot comes from the NatWest Holdings Group Annual Report 2024, which "
         "prints an explicit Spot/Average split per entity and whose FY2023 UK DoLSub spot column reproduces this "
         "workbook's existing 138% exactly (that tie is what identifies the pre-FY2024 series as spot rather than "
         "average).\n\n"
         "FY2025 SPOT IS GENUINELY UNAVAILABLE: from FY2025 the NatWest Holdings Group Annual Report dropped the "
         "Spot column and now states its liquidity key metrics 'on an average basis' only, so no point-in-time "
         "31 December 2025 UK DoLSub LCR is published anywhere. The FY2025 average (135%) is recorded on the "
         "average row rather than being spliced into the spot series. No £m HQLA/net-outflow breakdown appears in "
         "any RBS plc document; the UK LIQ1 £m tables exist only at NatWest Holdings Group level.",
)

metric(
    "NSFR", "%",
    [
        ("Net Stable Funding Ratio (%) - UK DoLSub, spot at 31 December",
         {"FY2024": "129%", "FY2023": "126%", "FY2022": "137%", "FY2021": "151%"}),
        ("Net Stable Funding Ratio (%) - UK DoLSub, four-quarter average",
         {"FY2025": "129%", "FY2024": "130%", "FY2023": "129%"}),
    ],
    liquidity_sources(),
    note="Same UK DoLSub sub-group basis, same two-row spot/average split, and same FY2025 spot-disclosure gap as "
         "the LCR sheet - see that sheet's note for the full explanation. The NSFR average is defined by the source "
         "as the average of the preceding four quarters (not twelve months, as for the LCR). The FY2023 UK DoLSub "
         "spot figure of 126% in the NatWest Holdings Group Annual Report 2024 reproduces this workbook's existing "
         "FY2023 value exactly, confirming the pre-FY2024 series is spot. Note the spot and average rows happen to "
         "coincide at 129% for FY2024/FY2025 respectively while measuring different things.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    sources_text="RBS plc's Annual Report and Pillar 3 Report FY2021-FY2025 - " + AR2025_URL,
    per_note={
        "MREL Ratio": "RBS plc's Annual Report and Pillar 3 Report both discuss MREL only qualitatively (as a "
                       "category of gone-concern loss-absorbing instrument, e.g. senior notes) - no numeric MREL "
                       "ratio, MREL resources figure, or UK KM2 template appears in any of the FY2021-FY2025 "
                       "sources reviewed."
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 95362, "FY2024": 90476, "FY2023": 90389, "FY2022": 96663, "FY2021": 106095}),
        ("Loans to customers - amortised cost", {"FY2025": 33531, "FY2024": 33524, "FY2023": 34805, "FY2022": 37667, "FY2021": 42035}),
        ("Customer deposits", {"FY2025": 78399, "FY2024": 78069, "FY2023": 77504, "FY2022": 83306, "FY2021": 92144}),
        ("Total equity", {"FY2025": 3658, "FY2024": 3249, "FY2023": 3103, "FY2022": 2661, "FY2021": 3747}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 2510, "FY2024": 2277, "FY2023": 2533, "FY2022": 2071, "FY2021": 1775}),
        ("Operating expenses", {"FY2025": -810, "FY2024": -871, "FY2023": -901, "FY2022": -892, "FY2021": -1114}),
        ("Profit for the year", {"FY2025": 1255, "FY2024": 1180, "FY2023": 1399, "FY2022": 1176, "FY2021": 776}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 3249, "FY2024": 3103, "FY2023": 2661, "FY2022": 3747, "FY2021": 5670}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 1709, "FY2024": 1380, "FY2023": 2138, "FY2022": -133, "FY2021": 231}),
        ("Other equity movements, net", {"FY2025": -1300, "FY2024": -1234, "FY2023": -1696, "FY2022": -953, "FY2021": -2154}),
        ("Closing equity", {"FY2025": 3658, "FY2024": 3249, "FY2023": 3103, "FY2022": 2661, "FY2021": 3747}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 1971, "FY2024": 2957, "FY2023": -5257, "FY2022": -6353, "FY2021": 15792}),
        ("Net cash from/(used in) investing activities", {"FY2025": 6, "FY2024": -2, "FY2023": 30, "FY2022": 265, "FY2021": 249}),
        ("Net cash from/(used in) financing activities", {"FY2025": -1396, "FY2024": -1457, "FY2023": -1873, "FY2022": -1038, "FY2021": -2240}),
        ("Cash and cash equivalents at end of year", {"FY2025": 48316, "FY2024": 47816, "FY2023": 46331, "FY2022": 53629, "FY2021": 60208}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "11.0%", "FY2024": "11.1%", "FY2023": "11.2%", "FY2022": "11.6%", "FY2021": "13.7%"}),
        ("Tier 1 Ratio", {"FY2025": "13.8%", "FY2024": "14.0%", "FY2023": "13.9%", "FY2022": "16.8%", "FY2021": "18.6%"}),
        ("Total Capital Ratio", {"FY2025": "17.0%", "FY2024": "17.5%", "FY2023": "16.4%", "FY2022": "25.4%", "FY2021": "26.1%"}),
        ("Leverage Ratio (excl. claims on central banks)", {"FY2025": "5.6%", "FY2024": "5.8%", "FY2023": "5.8%", "FY2022": "6.4%"}),
        ("LCR (UK DoLSub, spot)", {"FY2024": "142%", "FY2023": "138%", "FY2022": "131%", "FY2021": "169%"}),
        ("NSFR (UK DoLSub, spot)", {"FY2024": "129%", "FY2023": "126%", "FY2022": "137%", "FY2021": "151%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. See the Cash Flow Statement sheet's ENTITY NOTE for an "
         "important entity-lineage flag (this is NOT the historic 1727 'Royal Bank of Scotland plc' entity, which "
         "is now named NatWest Markets Plc) and for the UK DoLSub liquidity-disclosure basis. The LCR/NSFR rows "
         "here show the SPOT (31 December point-in-time) UK DoLSub series only, so that the trend stays on one "
         "consistent basis; FY2025 spot is not published by any source. The LCR and NSFR sheets additionally carry "
         "an average-basis row covering FY2023-FY2025 - do not read across the two bases, they differ by 11 points "
         "for FY2023.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/RBS FINANCIALS.xlsx")
