import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR_URLS = {
    "FY2025": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwm-annual-report.pdf",
    "FY2024": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/14022025/nwm-annual-report.pdf",
    "FY2023": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/16022024/nwmp-annual-report.pdf",
    "FY2022": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/nwmp-annual-report.pdf",
    "FY2021": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/18022022/nwm-plc-annual-report-2021.pdf",
}
P3_URLS = {
    "FY2025": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwm-pillar-3-report.pdf",
    "FY2024": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/14022025/nwm-pillar-3-report.pdf",
    "FY2023": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/16022024/nwmp-pillar-3-report.pdf",
    "FY2022": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/nwmp-pillar-3-report.pdf",
    "FY2021": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/18022022/nwg-pillar-3-supplement-2021.pdf",
}


def sources(kind, pages):
    urls = AR_URLS if kind == "annual" else P3_URLS
    label = "Annual Report and Accounts" if kind == "annual" else "Pillar 3 Report"
    lines = ["Sources — NatWest Markets Plc (NWM Plc), entity/group basis as stated in each source:"]
    for year in YEARS:
        lines.append(f"{year}: NWM Plc {label}, p.{pages[year]} — {urls[year]}")
    return "\n".join(lines)


bw = BankWorkbook("NatWest Markets Plc", YEARS, header_color="5B2C6F")

# NWM Plc column of the audited consolidated cash-flow statement. The 2021–22
# reports present detailed lines; later reports present condensed note-referenced
# lines. Each year's own presentation is retained.
cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Operating profit/(loss) before tax", {"FY2025": 186, "FY2024": -32, "FY2023": -141, "FY2022": -264, "FY2021": -702}),
    ("DATA", "Non-cash and other items", {"FY2025": -895, "FY2024": -104, "FY2023": 21}),
    ("DATA", "Impairment losses/(releases)", {"FY2022": -1, "FY2021": -36}),
    ("DATA", "Depreciation and amortisation", {"FY2022": 6, "FY2021": 9}),
    ("DATA", "Other non-cash items and fair-value movements", {"FY2022": -637, "FY2021": -103}),
    ("DATA", "Changes in operating assets and liabilities", {"FY2025": -1864, "FY2024": -51, "FY2023": -672, "FY2022": 5883, "FY2021": 1130}),
    ("DATA", "Income taxes received/(paid)", {"FY2025": 108, "FY2024": -81, "FY2023": 116, "FY2022": 144, "FY2021": 55}),
    ("DATA", "Other detailed operating adjustments (reported residual)", {"FY2022": 264, "FY2021": 702}),
    ("TOTAL", "Net cash flows from operating activities", {"FY2025": -2465, "FY2024": -268, "FY2023": -676, "FY2022": 5395, "FY2021": 1055}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Sale and maturity of other financial assets", {"FY2025": 8623, "FY2024": 4622, "FY2023": 3752, "FY2022": 4797, "FY2021": 3842}),
    ("DATA", "Purchase of other financial assets", {"FY2025": -9833, "FY2024": -7364, "FY2023": -6771, "FY2022": -7601, "FY2021": -3822}),
    ("DATA", "Income received on other financial assets", {"FY2025": 871, "FY2024": 882, "FY2023": 573, "FY2022": 252, "FY2021": 146}),
    ("DATA", "Dividends received from subsidiaries", {"FY2025": 98, "FY2024": 94, "FY2023": 349, "FY2022": 53, "FY2021": 65}),
    ("DATA", "Sale of property, plant and equipment", {"FY2023": 1}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -1, "FY2024": -1}),
    ("DATA", "Other investing activities (reported residual)", {"FY2024": -1, "FY2022": -1}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": -242, "FY2024": -1768, "FY2023": -2096, "FY2022": -2500, "FY2021": 231}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of paid-in equity", {"FY2025": 600, "FY2024": 592}),
    ("DATA", "Redemption of paid-in equity", {"FY2025": -845}),
    ("DATA", "Issue/(redemption) of subordinated liabilities", {"FY2025": -67, "FY2024": 22, "FY2023": -652, "FY2022": -350, "FY2021": -339}),
    ("DATA", "Issue/(maturity) of MRELs", {"FY2025": 104, "FY2024": 1247, "FY2023": -45, "FY2022": -1027, "FY2021": -1234}),
    ("DATA", "Interest paid on MRELs and subordinated liabilities", {"FY2025": -306, "FY2024": -261, "FY2023": -232, "FY2022": -210, "FY2021": -166}),
    ("DATA", "Dividends paid", {"FY2025": -108, "FY2024": -73, "FY2023": -70, "FY2022": -500, "FY2021": -1063}),
    ("DATA", "Capital contribution", {"FY2023": 115}),
    ("DATA", "Other financing activities (reported residual)", {"FY2025": 67, "FY2024": 82, "FY2023": 57, "FY2022": 210, "FY2021": 166}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": -555, "FY2024": 1609, "FY2023": -827, "FY2022": -1877, "FY2021": -2636}),
    ("DATA", "Effects of exchange rate on cash and cash equivalents", {"FY2025": 114, "FY2024": -291, "FY2023": -336, "FY2022": 691, "FY2021": -721}),
    ("TOTAL", "Net decrease in cash and cash equivalents", {"FY2025": -3148, "FY2024": -718, "FY2023": -3935, "FY2022": 1709, "FY2021": -2071}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 16270, "FY2024": 16988, "FY2023": 20923, "FY2022": 19214, "FY2021": 21285}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 13122, "FY2024": 16270, "FY2023": 16988, "FY2022": 20923, "FY2021": 19214}),
]
bw.add_cash_flow_sheet(
    "NatWest Markets Plc — Cash Flow Statement",
    "NWM Plc consolidated basis, £m. Figures are the NWM Plc column of each year's audited statement.",
    cash_rows,
    sources("annual", {"FY2025": 79, "FY2024": 87, "FY2023": 93, "FY2022": "100–101", "FY2021": "108–109"}),
    first_col_width=70, source_height=150, unit_suffix=" (£m)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, sources("p3", {"FY2025": 7, "FY2024": 7, "FY2023": 6, "FY2022": 8, "FY2021": 16}), note=note, first_col_width=55, source_height=125)


metric("CET1 Capital", "£m", [("Common equity tier 1 (CET1) capital", {"FY2025": 3952, "FY2024": 3779, "FY2023": 3776, "FY2022": 3682, "FY2021": 4072})])
metric("CET1 Ratio", "% of RWA", [("Common equity tier 1 (CET1) ratio", {"FY2025": "18.4%", "FY2024": "18.2%", "FY2023": "17.1%", "FY2022": "17.2%", "FY2021": "17.9%"})])
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 4926, "FY2024": 5067, "FY2023": 4455, "FY2022": 4361, "FY2021": 4755})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "23.0%", "FY2024": "24.3%", "FY2023": "20.2%", "FY2022": "20.4%", "FY2021": "21.0%"})])
metric("Total Capital", "£m", [("Total capital", {"FY2025": 5576, "FY2024": 5779, "FY2023": 5072, "FY2022": 5502, "FY2021": 5870})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "26.0%", "FY2024": "27.8%", "FY2023": "23.0%", "FY2022": "25.7%", "FY2021": "25.9%"})])
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", {"FY2025": 21457, "FY2024": 20812, "FY2023": 22099, "FY2022": 21422, "FY2021": 22686})])
metric("Leverage Ratio", "£m / %", [("Leverage exposure measure", {"FY2025": 97880, "FY2024": 92859, "FY2023": 89929, "FY2022": 81083, "FY2021": 110603}), ("Leverage ratio", {"FY2025": "5.0%", "FY2024": "5.5%", "FY2023": "5.0%", "FY2022": "5.4%", "FY2021": "4.3%"})], note="FY2021 uses the CRR leverage ratio; FY2022 onward uses the PRA UK leverage-ratio presentation. These bases are not directly comparable.")
metric("LCR", "%", [("Liquidity coverage ratio", {"FY2025": "198%", "FY2024": "192%", "FY2023": "240%", "FY2022": "226%"})], note="NWM Plc's standalone headline LCR is not included in the 2021 large-subsidiary supplement; FY2021 is left blank rather than substituted with a NatWest Group figure.")
metric("NSFR", "%", [("Net stable funding ratio", {"FY2025": "121%", "FY2024": "120%", "FY2023": "127%", "FY2022": "133%"})], note="NWM Plc's standalone NSFR is not included in the 2021 large-subsidiary supplement; FY2021 is left blank rather than substituted with a NatWest Group figure.")
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], sources_text="NWM Plc Pillar 3 Reports 2021–2025 — " + P3_URLS["FY2025"], per_note={"MREL Ratio": "The reviewed NWM Plc reports disclose MREL instruments and liabilities but do not provide a numeric MREL ratio in the project's target metric format."})


# NWM Plc publishes entity-level quarterly Pillar 3 KM1 tables.  The reports
# often include several prior quarter comparatives, so each observation below
# is retained with the report that discloses it and its table page.  Values are
# in the source's native £m / percentage units; blanks are genuine non-
# disclosures rather than substitutions from NatWest Group.
INTERIM_SOURCES = {
    "2021-09-30": ("Q3 2022 Pillar 3 Supplement", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/11112022/natwest-markets-plc-q3-pillar-3-supplement.pdf", "7"),
    "2022-03-31": ("Q1 2023 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/28042023/natwest-markets-plc-pillar-3-q1-2023.pdf", "7"),
    "2022-06-30": ("Q3 2022 Pillar 3 Supplement", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/29072022/natwest-marketsplc-pillar-3-supplement.pdf", "7"),
    "2022-09-30": ("Q3 2022 Pillar 3 Supplement", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/11112022/natwest-markets-plc-q3-pillar-3-supplement.pdf", "7"),
    "2023-03-31": ("Q1 2023 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/28042023/natwest-markets-plc-pillar-3-q1-2023.pdf", "7"),
    "2023-06-30": ("H1 2023 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/2023/natwest-markets-plc-pillar-3-h1-2023.pdf", "7"),
    "2023-09-30": ("Q3 2023 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13-11-2023/natwest-markets-plc-pillar-3-q3-2023.pdf", "7"),
    "2024-03-31": ("Q1 2024 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/2024/natwest-markets-plc-pillar-3-q1-2024.pdf", "7"),
    "2024-06-30": ("H1 2024 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/2024/nwm-plc-pillar-3-hy-2024.pdf", "7"),
    "2024-09-30": ("Q3 2024 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/12112024/nwm-plc-pillar-3-q3-2024.pdf", "7"),
    "2025-03-31": ("Q1 2025 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13052025/nwm-pillar3-report.pdf", "7"),
    "2025-06-30": ("H1 2025 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/11-08-2025/nwm-pillar3-h1-report.pdf", "7"),
    "2025-09-30": ("Q3 2025 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/11112025/11112025-nwm-pillar-3-report.pdf", "7"),
}

INTERIM_VALUES = {
    "2021-09-30": [4553, 5231, 6463, 24582, "19.4%", "22.3%", "27.6%", None, None, "238%", None],
    "2022-03-31": [4005, 4686, 5764, 24063, "16.6%", "19.5%", "24.0%", 100712, "4.7%", "219%", None],
    "2022-06-30": [3837, 4514, 5597, 23456, "16.4%", "19.2%", "23.9%", 102238, "4.4%", "218%", None],
    "2022-09-30": [3714, 4393, 5538, 24873, "14.9%", "17.7%", "22.3%", 99515, "4.4%", "216%", None],
    "2023-03-31": [3676, 4355, 5475, 20173, "18.2%", "21.6%", "27.1%", 77259, "5.6%", "247%", "137%"],
    "2023-06-30": [3542, 4221, 4841, 20159, "17.6%", "20.9%", "24.0%", 78064, "5.4%", "253%", "137%"],
    "2023-09-30": [3523, 4202, 4828, 23392, "15.1%", "18.0%", "20.6%", 85706, "4.9%", "255%", "135%"],
    "2024-03-31": [3901, 4580, 5274, 21506, "18.1%", "21.3%", "24.5%", 91464, "5.0%", "219%", "121%"],
    "2024-06-30": [3840, 4519, 5198, 20542, "18.7%", "22.0%", "25.3%", 86275, "5.2%", "203%", "118%"],
    "2024-09-30": [3720, 4416, 5066, 21476, "17.3%", "20.6%", "23.6%", 96209, "4.6%", "189%", "117%"],
    "2025-03-31": [3743, 5280, 5963, 21705, "17.2%", "24.3%", "27.5%", 97377, "5.4%", "189%", "120%"],
    "2025-06-30": [3627, 5508, 6144, 21243, "17.1%", "25.9%", "28.9%", 98840, "5.6%", "193%", "121%"],
    "2025-09-30": [3801, 4776, 5425, 21678, "17.5%", "22.0%", "25.0%", 106006, "4.5%", "196%", "120%"],
}

INTERIM_METRICS = [
    ("CET1 capital", "£m"), ("Tier 1 capital", "£m"), ("Total capital", "£m"),
    ("Total risk-weighted exposure amount", "£m"), ("CET1 ratio", "%"),
    ("Tier 1 ratio", "%"), ("Total capital ratio", "%"),
    ("Leverage exposure measure excluding claims on central banks", "£m"),
    ("Leverage ratio excluding claims on central banks", "%"),
    ("Liquidity coverage ratio (12-month average)", "%"),
    ("Net stable funding ratio (4-quarter average)", "%"),
]
interim_rows = []
interim_hyperlinks = {}
for period, values in INTERIM_VALUES.items():
    report_name, url, page = INTERIM_SOURCES[period]
    for metric_index, ((metric_name, unit), value) in enumerate(zip(INTERIM_METRICS, values)):
        if value is None:
            continue
        row_index = len(interim_rows)
        interim_rows.append([period, "Quarterly Pillar 3 disclosure", metric_name, value, unit, "NWM Plc consolidated basis", report_name, f"p.{page} — UK KM1 table"])
        # IN-031: the real per-period URL was already sourced into
        # INTERIM_SOURCES above but never threaded through to
        # add_wide_interim_sheet()'s hyperlink_cells - every interim cell's
        # hyperlink silently fell back to the plain `report_name` text
        # instead. Wire it through so citations actually link.
        interim_hyperlinks[(row_index, 6)] = url

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=interim_rows,
    subtitle="NatWest Markets Plc entity-level quarterly KM1 disclosures, 2021–2025",
    note="Official NWM Plc reports provide comparable quarter-end KM1 observations for September 2021 and March/June/September 2022–2025. No standalone March or June 2021 interim KM1 report was located. Leverage and NSFR were not disclosed in the September 2021 comparative; NSFR was introduced in the 2023 disclosures. Values are not substituted from NatWest Group.",
    hyperlink_cells=interim_hyperlinks,
)

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -2465, "FY2024": -268, "FY2023": -676, "FY2022": 5395, "FY2021": 1055}),
        ("Net cash from/(used in) investing activities", {"FY2025": -242, "FY2024": -1768, "FY2023": -2096, "FY2022": -2500, "FY2021": 231}),
        ("Net cash from/(used in) financing activities", {"FY2025": -555, "FY2024": 1609, "FY2023": -827, "FY2022": -1877, "FY2021": -2636}),
        ("Cash and cash equivalents at end of year", {"FY2025": 13122, "FY2024": 16270, "FY2023": 16988, "FY2022": 20923, "FY2021": 19214}),
    ], cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "18.4%", "FY2024": "18.2%", "FY2023": "17.1%", "FY2022": "17.2%", "FY2021": "17.9%"}),
        ("Tier 1 Ratio", {"FY2025": "23.0%", "FY2024": "24.3%", "FY2023": "20.2%", "FY2022": "20.4%", "FY2021": "21.0%"}),
        ("Total Capital Ratio", {"FY2025": "26.0%", "FY2024": "27.8%", "FY2023": "23.0%", "FY2022": "25.7%", "FY2021": "25.9%"}),
        ("Leverage Ratio", {"FY2025": "5.0%", "FY2024": "5.5%", "FY2023": "5.0%", "FY2022": "5.4%", "FY2021": "4.3%"}),
        ("LCR", {"FY2025": "198%", "FY2024": "192%", "FY2023": "240%", "FY2022": "226%"}),
        ("NSFR", {"FY2025": "121%", "FY2024": "120%", "FY2023": "127%", "FY2022": "133%"}),
    ],
    note="This workbook covers NatWest Markets Plc (company SC090312, FRN 121882), formerly The Royal Bank of Scotland Public Limited Company. It is distinct from the current Royal Bank of Scotland plc (company SC083026) workbook. FY2021 LCR/NSFR are blank because the official large-subsidiary supplement did not provide standalone NWM Plc figures.",
)

bw.save("/Users/armaan/code/katalysis/banks/NATWEST MARKETS FINANCIALS.xlsx")
