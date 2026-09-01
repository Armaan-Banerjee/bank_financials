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
    "entirely to the NatWest Holdings Group Annual Report, a different reporting entity not covered by this "
    "project) - FY2024/FY2025 LCR/NSFR are therefore blank, not a gap in RBS plc's own reporting."
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
# Sheet 1: Cash Flow Statement
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
    [("Liquidity Coverage Ratio (%) - UK DoLSub level", {"FY2023": "138%", "FY2022": "131%", "FY2021": "169%"})],
    p3_sources(),
    note="UK DoLSub (RBS plc + National Westminster Bank Plc + Coutts & Company) sub-group figure throughout, per "
         "the PRA waiver described in the entity note - RBS plc solo LCR is not disclosed at all in any year. No "
         "£m HQLA/net-outflow breakdown is given in RBS plc's own Annual Report or Pillar 3 Report (only the "
         "headline %). FY2024 and FY2025: not disclosed in any RBS plc document - moved entirely to the NatWest "
         "Holdings Group Annual Report (a separate reporting entity, out of scope for this project).",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (%) - UK DoLSub level", {"FY2023": "126%", "FY2022": "137%", "FY2021": "151%"})],
    p3_sources(),
    note="Same UK DoLSub sub-group basis and same FY2024/FY2025 disclosure gap as the LCR sheet - see that sheet's "
         "note.",
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
        ("LCR (UK DoLSub)", {"FY2023": "138%", "FY2022": "131%", "FY2021": "169%"}),
        ("NSFR (UK DoLSub)", {"FY2023": "126%", "FY2022": "137%", "FY2021": "151%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. See the Cash Flow Statement sheet's ENTITY NOTE for an "
         "important entity-lineage flag (this is NOT the historic 1727 'Royal Bank of Scotland plc' entity, which "
         "is now named NatWest Markets Plc) and for the UK DoLSub liquidity-disclosure basis.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/RBS FINANCIALS.xlsx")
