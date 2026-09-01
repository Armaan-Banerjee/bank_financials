import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwb-annual-report.pdf"
AR2024_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/14022025/nwb-annual-report.pdf"
AR2023_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/16022024/nwb-plc-annual-report.pdf"
AR2022_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/nwb-plc-annual-report.pdf"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00929027/filing-history/MzMzODcyODkwNGFkaXF6a2N4/document?format=pdf&download=0"
P3_2025_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwb-pillar-3-report.pdf"
P3_2024_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/14022025/nwb-pillar-3-report.pdf"
P3_2023_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/16022024/nwb-plc-pillar-3-report.pdf"
P3_2022_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/nwb-plc-pillar-3-report.pdf"
P3_2025_Q3_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/11112025/11112025-nwb-pillar-3-report.pdf"
P3_2024_Q3_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/12112024/nwb-plc-pillar-3-q3-2024.pdf"
P3_2023_Q3_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13-11-2023/natwest-bank-plc-pillar-3-q3-2023.pdf"
P3_2022_Q3_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/nwb-plc-pillar-3-report.pdf"
CH_COMPANY_URL = "https://find-and-update.company-information.service.gov.uk/company/00929027"

ENTITY_NOTE = (
    "ENTITY NOTE: This workbook covers National Westminster Bank Public Limited Company (NWB Plc), company "
    "number 00929027, FRN 121878 and LEI 213800IBT39XQ9C4CP71. It is the PRA-authorised legal entity named in "
    "the project bank list, not NatWest Group plc, NatWest Holdings Limited, RBS plc or NatWest Markets Plc. "
    "NWB Plc is a member of the UK Domestic Liquidity Sub-Group (UK DoLSub) with RBS plc and Coutts & Company; "
    "LCR and NSFR are therefore shown on the UK DoLSub basis where the entity reports that basis, rather than as "
    "NWB Plc solo figures. Companies House confirms company 00929027 and the filed 2021 accounts used below."
)


def ar_sources():
    return (
        "Sources - NWB Plc own annual accounts, £m:\n"
        f"FY2025: NWB Group Annual Report and Accounts 2025, p.96 (cash flow statement) - {AR2025_URL}\n"
        f"FY2024: NWB Group Annual Report and Accounts 2024, p.102 (cash flow statement) - {AR2024_URL}\n"
        f"FY2023: NWB Group Annual Report and Accounts 2023, p.103 (cash flow statement) - {AR2023_URL}\n"
        f"FY2022: NWB Group Annual Report and Accounts 2022, p.104 (cash flow statement) - {AR2022_URL}\n"
        f"FY2021: NWB Group Annual Report and Accounts 2022, p.104 (FY2021 comparative column; independently filed at Companies House) - {AR2022_URL}; {AR2021_URL}\n\n"
        + ENTITY_NOTE
    )


def p3_sources():
    return (
        "Sources - NWB Plc UK KM1 key metrics, PRA transitional basis:\n"
        f"FY2025: NWB Plc Pillar 3 Report 2025, p.7 - {P3_2025_URL}\n"
        f"FY2024: NWB Plc Pillar 3 Report 2024, p.7 - {P3_2024_URL}\n"
        f"FY2023: NWB Plc Pillar 3 Report 2023, p.7 - {P3_2023_URL}\n"
        f"FY2022 and FY2021: NWB Plc Pillar 3 Report 2022, p.7 (FY2021 comparative column) - {P3_2022_URL}\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook("National Westminster Bank Public Limited Company", YEARS, YEAR_LABEL, header_color="005A8D")

# The 2023-2025 reports use condensed cash-flow presentation; 2022 provides the detailed 2022/2021 comparative.
cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Operating profit before tax", {"FY2025": 5591, "FY2024": 4680, "FY2023": 4705, "FY2022": 4687, "FY2021": 3542}),
    ("DATA", "Non-cash and other items", {"FY2025": -62, "FY2024": 1424, "FY2023": 396}),
    ("DATA", "Impairment losses/(releases)", {"FY2022": 389, "FY2021": -732}),
    ("DATA", "Depreciation and amortisation", {"FY2022": 598, "FY2021": 594}),
    ("DATA", "Net impairment charges of investments in Group undertakings", {"FY2022": 336, "FY2021": 61}),
    ("DATA", "Change in fair value on financial assets", {"FY2022": 1177, "FY2021": 1595}),
    ("DATA", "Change in fair value on financial liabilities and subordinated liabilities", {"FY2022": -924, "FY2021": -418}),
    ("DATA", "Elimination of foreign exchange differences", {"FY2022": -3, "FY2021": 1118}),
    ("DATA", "Other non-cash items", {"FY2022": -215, "FY2021": 58}),
    ("DATA", "Income receivable on other financial assets", {"FY2022": -303, "FY2021": -412}),
    ("DATA", "Dividends receivable from subsidiaries", {"FY2022": -1010, "FY2021": -424}),
    ("DATA", "Interest payable on MRELs and subordinated liabilities", {"FY2022": 358, "FY2021": 310}),
    ("DATA", "Charges and releases on provisions", {"FY2022": 122, "FY2021": 388}),
    ("DATA", "Defined benefit pension schemes", {"FY2022": 132, "FY2021": 146}),
    ("TOTAL", "Net cash flows from trading activities", {"FY2022": 5443, "FY2021": 6038}),
    ("DATA", "Changes in operating assets and liabilities", {"FY2025": 9514, "FY2024": -7007, "FY2023": -8999, "FY2022": -45374, "FY2021": 31327}),
    ("DATA", "Income taxes paid", {"FY2025": -1515, "FY2024": -993, "FY2023": -484, "FY2022": -998, "FY2021": -791}),
    ("TOTAL", "Net cash flows from operating activities", {"FY2025": 13528, "FY2024": -1896, "FY2023": -4382, "FY2022": -40929, "FY2021": 36574}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Sale and maturity of other financial assets", {"FY2025": 31898, "FY2024": 33860, "FY2023": 17887, "FY2022": 25339, "FY2021": 9884}),
    ("DATA", "Purchase of other financial assets", {"FY2025": -44449, "FY2024": -41551, "FY2023": -34249, "FY2022": -13022, "FY2021": -2811}),
    ("DATA", "Income received on other financial assets", {"FY2025": 1404, "FY2024": 768, "FY2023": 435, "FY2022": 371, "FY2021": 412}),
    ("DATA", "Net movement in business interests and intangible assets", {"FY2025": -401, "FY2024": -2861, "FY2023": -1188, "FY2022": -719, "FY2021": -3093}),
    ("DATA", "Dividends received from subsidiaries", {"FY2025": 487, "FY2024": 553, "FY2023": 617, "FY2022": 1010, "FY2021": 424}),
    ("DATA", "Sale of property, plant and equipment", {"FY2025": 36, "FY2024": 101, "FY2023": 34, "FY2022": 82, "FY2021": 17}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -237, "FY2024": -252, "FY2023": -544, "FY2022": -316, "FY2021": -617}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": -11262, "FY2024": -9382, "FY2023": -17008, "FY2022": 12745, "FY2021": 4216}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of paid-in equity", {"FY2025": 1741, "FY2024": 799, "FY2022": 500, "FY2021": 941}),
    ("DATA", "Redemption of paid-in equity", {"FY2025": -1911, "FY2022": -388, "FY2021": -934}),
    ("DATA", "Issue of subordinated liabilities", {"FY2025": 830, "FY2024": 600, "FY2023": 1263}),
    ("DATA", "Redemption of subordinated liabilities", {"FY2025": -500, "FY2024": -579, "FY2023": -539}),
    ("DATA", "Interest paid on subordinated liabilities", {"FY2025": -174, "FY2024": -159, "FY2023": -120}),
    ("DATA", "Movement in subordinated liabilities", {"FY2022": -199, "FY2021": -1267}),
    ("DATA", "Movement in MRELs", {"FY2022": 509, "FY2021": 1515}),
    ("DATA", "Issue of MRELs", {"FY2025": 1544, "FY2024": 927, "FY2023": 441}),
    ("DATA", "Maturity and redemption of MRELs", {"FY2025": 0, "FY2024": -930, "FY2023": -107}),
    ("DATA", "Interest paid on MRELs", {"FY2025": -227, "FY2024": -215, "FY2023": -261}),
    ("DATA", "Dividends paid", {"FY2025": -3221, "FY2024": -2710, "FY2023": -1880, "FY2022": -3413, "FY2021": -1709}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": -1918, "FY2024": -2267, "FY2023": -1203, "FY2022": -2991, "FY2021": -1454}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2025": 141, "FY2024": -259, "FY2023": -397, "FY2022": 1101, "FY2021": -984}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 489, "FY2024": -13804, "FY2023": -22990, "FY2022": -30074, "FY2021": 38352}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 38678, "FY2024": 52482, "FY2023": 75472, "FY2022": 105546, "FY2021": 67194}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 39167, "FY2024": 38678, "FY2023": 52482, "FY2022": 75472, "FY2021": 105546}),
]
bw.add_cash_flow_sheet("National Westminster Bank Plc — Cash Flow Statement", "NWB Plc entity-level basis, £m. " + ENTITY_NOTE, cash_rows, ar_sources(), first_col_width=80, source_height=240, unit_suffix=" (£m)")


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, p3_sources(), note=note, first_col_width=55, source_height=150)


metric("CET1 Capital", "£m", [("Common equity tier 1 (CET1) capital", {"FY2025": 14968, "FY2024": 14181, "FY2023": 14082, "FY2022": 12713, "FY2021": 13924})])
metric("CET1 Ratio", "% of RWA", [("Common equity tier 1 (CET1) ratio", {"FY2025": "11.2%", "FY2024": "11.4%", "FY2023": "11.6%", "FY2022": "11.3%", "FY2021": "16.1%"})])
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 17910, "FY2024": 17258, "FY2023": 16360, "FY2022": 14956, "FY2021": 16039})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "13.4%", "FY2024": "13.9%", "FY2023": "13.4%", "FY2022": "13.3%", "FY2021": "18.6%"})])
metric("Total Capital", "£m", [("Total capital", {"FY2025": 21701, "FY2024": 20629, "FY2023": 19798, "FY2022": 17877, "FY2021": 18945})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "16.2%", "FY2024": "16.6%", "FY2023": "16.3%", "FY2022": "15.9%", "FY2021": "22.0%"})])
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", {"FY2025": 133749, "FY2024": 124522, "FY2023": 121740, "FY2022": 112428, "FY2021": 86217})])
metric("Leverage Ratio", "£m / %", [("Leverage exposure measure", {"FY2025": 424554, "FY2024": 390032, "FY2023": 359897, "FY2022": 341308, "FY2021": 426681}), ("Leverage ratio", {"FY2025": "4.2%", "FY2024": "4.4%", "FY2023": "4.5%", "FY2022": "4.4%", "FY2021": "3.8%"})], note="FY2021 is shown on the prior CRR methodology as reported in NWB Plc Annual Report 2022, p.64; the report also gives 4.8% on the later UK methodology. FY2022 onward uses the current PRA basis and is not directly comparable with the FY2021 headline.")
metric("LCR", "%", [("Liquidity Coverage Ratio - UK DoLSub", {"FY2025": "151%", "FY2024": "147%", "FY2023": "138%", "FY2022": "131%", "FY2021": "169%"})], note="UK DoLSub basis: NWB Plc, RBS plc and Coutts & Company. The 2025 figure is the December value from the NWB Pillar 3 report; the 2024 and 2023 figures are the December values in the corresponding KM1 disclosures. NWB Plc reports liquidity under a PRA waiver at UK DoLSub level rather than solo.")
metric("NSFR", "%", [("Net Stable Funding Ratio - UK DoLSub", {"FY2025": "137%", "FY2024": "136%", "FY2023": "126%", "FY2022": "137%", "FY2021": "151%"})], note="UK DoLSub basis; see LCR note. NSFR is a four-quarter average under the regulatory disclosure framework.")
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], "NWB Plc Pillar 3 Reports 2022-2025 - " + P3_2025_URL, per_note={"MREL Ratio": "No single numeric MREL ratio is presented in the five-year source set used for this annual workbook. MREL instruments and movements are discussed in the annual accounts, but no comparable headline ratio was disclosed in the reviewed NWB Plc UK KM1 material."})


# NWB Plc publishes quarterly UK KM1 disclosures.  The Q3 reports include the
# current quarter plus the preceding Q1/Q2 comparatives, allowing a complete
# March-to-September quarterly series without mixing in NatWest Group data.
INTERIM_PERIODS = [
    ("31 March 2022", "Q1 2022", P3_2022_Q3_URL, "p.7"),
    ("30 June 2022", "H1 2022", P3_2022_Q3_URL, "p.7"),
    ("30 September 2022", "Q3 2022", P3_2022_Q3_URL, "p.7"),
    ("31 March 2023", "Q1 2023", P3_2023_Q3_URL, "p.6"),
    ("30 June 2023", "H1 2023", P3_2023_Q3_URL, "p.6"),
    ("30 September 2023", "Q3 2023", P3_2023_Q3_URL, "p.6"),
    ("31 March 2024", "Q1 2024", P3_2024_Q3_URL, "p.6"),
    ("30 June 2024", "H1 2024", P3_2024_Q3_URL, "p.6"),
    ("30 September 2024", "Q3 2024", P3_2024_Q3_URL, "p.6"),
    ("31 March 2025", "Q1 2025", P3_2025_Q3_URL, "p.6"),
    ("30 June 2025", "H1 2025", P3_2025_Q3_URL, "p.6"),
    ("30 September 2025", "Q3 2025", P3_2025_Q3_URL, "p.6"),
]

INTERIM_VALUES = {
    "31 March 2022": [13802, 15917, 18709, 103987, "13.3%", "15.3%", "18.0%", 338123, "4.7%"],
    "30 June 2022": [12335, 14591, 17503, 106211, "11.6%", "13.7%", "16.5%", 340086, "4.3%"],
    "30 September 2022": [12437, 14680, 17719, 107157, "11.6%", "13.7%", "16.5%", 343343, "4.3%"],
    "31 March 2023": [13640, 15883, 19343, 116122, "11.7%", "13.7%", "16.7%", 349719, "4.5%"],
    "30 June 2023": [13609, 15852, 19235, 116811, "11.7%", "13.6%", "16.5%", 363052, "4.4%"],
    "30 September 2023": [14320, 16563, 20011, 117745, "12.2%", "14.1%", "17.0%", 362422, "4.6%"],
    "31 March 2024": [14823, 17101, 20497, 124523, "11.9%", "13.7%", "16.5%", 358649, "4.8%"],
    "30 June 2024": [13813, 16890, 20273, 120780, "11.4%", "14.0%", "16.8%", 366912, "4.6%"],
    "30 September 2024": [14722, 17799, 21172, 122340, "12.0%", "14.5%", "17.3%", 381762, "4.7%"],
    "31 March 2025": [15271, 18848, 23064, 127480, "12.0%", "14.8%", "18.1%", 397065, "4.7%"],
    "30 June 2025": [14828, 18346, 22104, 130712, "11.3%", "14.0%", "16.9%", 411371, "4.5%"],
    "30 September 2025": [16128, 20147, 23937, 130496, "12.4%", "15.4%", "18.3%", 413717, "4.9%"],
}

interim_metric_specs = [
    ("Common equity tier 1 (CET1) capital", "£m"),
    ("Tier 1 capital", "£m"),
    ("Total capital", "£m"),
    ("Total risk-weighted exposure amount", "£m"),
    ("Common equity tier 1 (CET1) ratio", "%"),
    ("Tier 1 ratio", "%"),
    ("Total capital ratio", "%"),
    ("Total exposure measure excluding claims on central banks", "£m"),
    ("Leverage ratio excluding claims on central banks", "%"),
]
interim_rows = []
for period, disclosure_type, source_url, page_ref in INTERIM_PERIODS:
    for (metric_name, unit), value in zip(interim_metric_specs, INTERIM_VALUES[period]):
        interim_rows.append([
            period, disclosure_type, metric_name, value, unit,
            "NWB Plc entity-level, PRA transitional/current basis as reported",
            source_url, page_ref,
        ])

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=interim_rows,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(interim_rows)},
    title="National Westminster Bank Plc — Interim Pillar 3",
    subtitle="Quarterly UK KM1 key metrics, March 2022 to September 2025. Capital and leverage figures are NWB Plc entity-level disclosures in £m or percentages.",
    note=(
        "Sources are the official NWB Plc Q3 Pillar 3 reports for 2022-2025, whose UK KM1 tables include the current quarter and prior Q1/Q2 comparatives. "
        "The NWB Plc UK Domestic Liquidity Sub-Group waiver means LCR and NSFR are managed and disclosed at UK DoLSub level rather than entity level; they are therefore not inserted here. "
        "No separate NWB Plc interim UK KM1 report was located for March-June-September 2021 in the reviewed official archive, so those periods are explicitly not represented rather than estimated."
    ),
)

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 13528, "FY2024": -1896, "FY2023": -4382, "FY2022": -40929, "FY2021": 36574}),
        ("Net cash from/(used in) investing activities", {"FY2025": -11262, "FY2024": -9382, "FY2023": -17008, "FY2022": 12745, "FY2021": 4216}),
        ("Net cash from/(used in) financing activities", {"FY2025": -1918, "FY2024": -2267, "FY2023": -1203, "FY2022": -2991, "FY2021": -1454}),
        ("Cash and cash equivalents at end of year", {"FY2025": 39167, "FY2024": 38678, "FY2023": 52482, "FY2022": 75472, "FY2021": 105546}),
    ], cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "11.2%", "FY2024": "11.4%", "FY2023": "11.6%", "FY2022": "11.3%", "FY2021": "16.1%"}),
        ("Tier 1 Ratio", {"FY2025": "13.4%", "FY2024": "13.9%", "FY2023": "13.4%", "FY2022": "13.3%", "FY2021": "18.6%"}),
        ("Total Capital Ratio", {"FY2025": "16.2%", "FY2024": "16.6%", "FY2023": "16.3%", "FY2022": "15.9%", "FY2021": "22.0%"}),
        ("Leverage Ratio", {"FY2025": "4.2%", "FY2024": "4.4%", "FY2023": "4.5%", "FY2022": "4.4%", "FY2021": "3.8%"}),
        ("LCR (UK DoLSub)", {"FY2025": "151%", "FY2024": "147%", "FY2023": "138%", "FY2022": "131%", "FY2021": "169%"}),
        ("NSFR (UK DoLSub)", {"FY2025": "137%", "FY2024": "136%", "FY2023": "126%", "FY2022": "137%", "FY2021": "151%"}),
    ], note="Figures are duplicated from the detail sheets. See source notes for exact documents, pages, entity basis and methodology changes. Additional quarterly NWB Plc disclosures are provided on the Interim Pillar 3 sheet.")

bw.save("/Users/armaan/code/katalysis/banks/NATIONAL WESTMINSTER BANK PLC FINANCIALS.xlsx")
