import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, all 12mo to 31 Dec

AR2025_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/annual/pdfs/hsbc-uk-bank-plc/260225-annual-report-and-accounts-2025.pdf"
AR2024_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/annual/pdfs/hsbc-uk-bank-plc/250219-annual-report-and-accounts-2024.pdf"
AR2023_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/annual/pdfs/hsbc-uk-bank-plc/240221-annual-report-and-accounts-2023.pdf"
AR2022_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/annual/pdfs/hsbc-uk-bank-plc/230221-annual-report-and-accounts-2022.pdf"
AR2021_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2021/annual/pdfs/hsbc-uk-bank-plc/220222-annual-report-and-accounts-2021.pdf"

P32025_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/annual/pdfs/hsbc-uk-bank-plc/260225-pillar-3-disclosures-at-31-december-2025.pdf"
P32024_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/annual/pdfs/hsbc-uk-bank-plc/250219-pillar-3-disclosures-at-31-december-2024.pdf"
P32023_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/annual/pdfs/hsbc-uk-bank-plc/240221-pillar-3-disclosures-at-31-december-2023.pdf"
P32022_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/annual/pdfs/hsbc-uk-bank-plc/230221-pillar-3-disclosures-at-31-december-2022.pdf"
P32021_URL = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2021/annual/pdfs/hsbc-uk-bank-plc/220222-pillar-3-disclosures-at-31-december-2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: HSBC UK Bank plc (Companies House 09928412, FRN 765112) is the ring-fenced retail/SME "
    "banking entity created in 2018 under UK ring-fencing reform - confirmed distinct from HSBC Bank plc "
    "(FRN 114216, the legacy non-ring-fenced entity, built separately in WF-012) and HSBC Innovation Bank "
    "Limited (FRN 543146, the former Silicon Valley Bank UK, also built in WF-012). All figures below are "
    "HSBC UK Bank plc's own entity-level Consolidated statements, sourced directly from HSBC UK Bank plc's "
    "own Annual Report and Accounts and Pillar 3 Disclosures on hsbc.com's investor-relations subsidiaries "
    "reporting archive."
)

CASH_FLOW_NOTE = (
    "CASH FLOW NOTE: figures are £m. Presentation granularity changed across report vintages: FY2025/FY2024 "
    "and FY2023/FY2022 both itemise 'Purchase of property, plant and equipment' / 'Proceeds from sale of "
    "property, plant and equipment' as separate lines, while FY2021's own report combines them into a single "
    "'Net cash flows from the purchase and sale of property, plant and equipment' line; similarly FY2025/2024 "
    "itemise 'Purchase of intangible assets' / 'Proceeds from sale of intangible assets' separately, FY2023/"
    "2022 report only a net purchase line, and FY2021 combines both into 'Net investment in intangible "
    "assets'. FY2023/FY2022 include two SVB UK-acquisition-specific lines (HSBC UK Bank plc acquired Silicon "
    "Valley Bank UK in March 2023) not present in other years. FY2025 introduces two new financing lines "
    "('Issue of ordinary share capital and other equity instruments', 'Repayment of other equity instruments "
    "to non-controlling interests') not present in earlier years. Blank cells indicate that year's own report "
    "did not disclose that specific line; section totals (net cash from operating/investing/financing "
    "activities, cash and cash equivalents) are consistent and comparable across all 5 years."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are HSBC UK Bank plc's own Consolidated statement of cash flows, £m, from each "
    "year's own Annual Report and Accounts:\n"
    f"FY2025 & FY2024: HSBC UK Bank plc Annual Report and Accounts 2025, p.79 (Consolidated statement of cash flows) - {AR2025_URL}\n"
    f"FY2023 & FY2022: HSBC UK Bank plc Annual Report and Accounts 2023, p.81 (Consolidated statement of cash flows) - {AR2023_URL}\n"
    f"FY2021: HSBC UK Bank plc Annual Report and Accounts 2021, p.75 (Consolidated statement of cash flows) - {AR2021_URL}\n\n"
    + CASH_FLOW_NOTE + "\n\n" + ENTITY_NOTE
)


def p3_sources(page="5"):
    return (
        "Sources - HSBC UK Bank plc's own entity-level Pillar 3 Disclosures, Table 1 'Key metrics "
        "(KM1/IFRS9-FL)', each year's own originally-published figures at 31 December:\n"
        f"FY2025: HSBC UK Bank plc Pillar 3 Disclosures at 31 December 2025, p.5 - {P32025_URL}\n"
        f"FY2024: HSBC UK Bank plc Pillar 3 Disclosures at 31 December 2024, p.5 - {P32024_URL}\n"
        f"FY2023: HSBC UK Bank plc Pillar 3 Disclosures at 31 December 2023, p.5 - {P32023_URL}\n"
        f"FY2022: HSBC UK Bank plc Pillar 3 Disclosures at 31 December 2022, p.5 - {P32022_URL}\n"
        f"FY2021: HSBC UK Bank plc Pillar 3 Disclosures at 31 December 2021, p.4 - {P32021_URL}\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="HSBC UK Bank plc", years=YEARS, header_color="DB0011")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 5619, "FY2024": 5647, "FY2023": 6679, "FY2022": 3638, "FY2021": 3480}),
    ("DATA", "Depreciation, amortisation and impairment", {"FY2025": 495, "FY2024": 447, "FY2023": 435, "FY2022": 482, "FY2021": 421}),
    ("DATA", "Net gain from investing activities", {"FY2025": -20, "FY2024": -38, "FY2023": 79, "FY2022": -37, "FY2021": -101}),
    ("DATA", "Provisional gain on acquisition of SVB UK", {"FY2023": -1307}),
    ("DATA", "Change in expected credit losses gross of recoveries and other credit impairment charges", {"FY2025": 616, "FY2024": 386, "FY2023": 472, "FY2022": 575, "FY2021": -911}),
    ("DATA", "Provisions including pensions", {"FY2025": -181, "FY2024": -198, "FY2023": -233, "FY2022": -78, "FY2021": 123}),
    ("DATA", "Share-based payment expense", {"FY2025": 30, "FY2024": 28, "FY2023": 19, "FY2022": 17, "FY2021": 16}),
    ("DATA", "Other non-cash items included in profit before tax", {"FY2025": -249, "FY2024": -249, "FY2023": -149, "FY2022": -204, "FY2021": -30}),
    ("DATA", "Elimination of exchange differences", {"FY2025": 143, "FY2024": 142, "FY2023": 332, "FY2022": 1032, "FY2021": -33}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Change in net trading securities and derivatives", {"FY2025": 1208, "FY2024": -626, "FY2023": 1615, "FY2022": -2174, "FY2021": -97}),
    ("DATA", "Change in loans and advances to banks and customers", {"FY2025": -14483, "FY2024": -5073, "FY2023": -2773, "FY2022": -9182, "FY2021": -3717}),
    ("DATA", "Change in reverse repurchase agreements - non-trading", {"FY2025": -4764, "FY2024": -1952, "FY2023": -264, "FY2022": 894, "FY2021": -5503}),
    ("DATA", "Change in financial assets mandatorily measured at fair value", {"FY2025": -1, "FY2024": -39, "FY2023": -27, "FY2022": -29, "FY2021": -53}),
    ("DATA", "Change in other assets", {"FY2025": -730, "FY2024": -748, "FY2023": 114, "FY2022": -2219, "FY2021": 728}),
    ("DATA", "Change in deposits by banks and customer accounts", {"FY2025": 4956, "FY2024": 12322, "FY2023": -20028, "FY2022": -1234, "FY2021": 33169}),
    ("DATA", "Change in repurchase agreements - non-trading", {"FY2025": 5856, "FY2024": -4231, "FY2023": -5086, "FY2022": -1104, "FY2021": 4288}),
    ("DATA", "Change in debt securities in issue", {"FY2025": 975, "FY2024": 56, "FY2023": 689, "FY2022": 399, "FY2021": 34}),
    ("DATA", "Change in other liabilities", {"FY2025": -113, "FY2024": -900, "FY2023": 605, "FY2022": 1052, "FY2021": -1233}),
    ("DATA", "Contributions paid to defined benefit plans", {"FY2025": 0, "FY2024": -1, "FY2023": -17, "FY2022": -21, "FY2021": -195}),
    ("DATA", "Tax paid", {"FY2025": -1632, "FY2024": -1209, "FY2023": -1182, "FY2022": -1499, "FY2021": 53}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": -2275, "FY2024": 3764, "FY2023": -20027, "FY2022": -9692, "FY2021": 30439}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of financial investments", {"FY2025": -26063, "FY2024": -33396, "FY2023": -17640, "FY2022": -10386, "FY2021": -12468}),
    ("DATA", "Proceeds from the sale and maturity of financial investments", {"FY2025": 22519, "FY2024": 22617, "FY2023": 10222, "FY2022": 8571, "FY2021": 17000}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 0, "FY2024": 27, "FY2023": 67, "FY2022": 39}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -73, "FY2024": -71, "FY2023": -45, "FY2022": -80}),
    ("DATA", "Net cash flows from the purchase and sale of property, plant and equipment", {"FY2021": -53}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -438, "FY2024": -363, "FY2023": -325, "FY2022": -382}),
    ("DATA", "Proceeds from sale of intangible assets", {"FY2025": 10, "FY2024": 1}),
    ("DATA", "Net investment in intangible assets", {"FY2021": -347}),
    ("DATA", "Net cash flow on acquisition of subsidiaries, businesses and joint venture", {"FY2025": 1, "FY2024": 0}),
    ("DATA", "Net cash flow from acquisition of SVB UK", {"FY2023": 1023}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": -4044, "FY2024": -11185, "FY2023": -6698, "FY2022": -2238, "FY2021": 4132}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of ordinary share capital and other equity instruments", {"FY2025": 495, "FY2024": 0}),
    ("DATA", "Subordinated loan capital issued", {"FY2025": 3194, "FY2024": 3259, "FY2023": 2250, "FY2021": 4978}),
    ("DATA", "Subordinated loan capital repaid", {"FY2025": -2414, "FY2024": -2194, "FY2021": -2079}),
    ("DATA", "Dividends paid to shareholders of the parent company and non-controlling interests", {"FY2025": -3028, "FY2024": -3569, "FY2023": -2416, "FY2022": -1934, "FY2021": -752}),
    ("DATA", "Repayment of other equity instruments to non-controlling interests", {"FY2025": -40, "FY2024": 0}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": -1793, "FY2024": -2504, "FY2023": -166, "FY2022": -1934, "FY2021": 2147}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -8112, "FY2024": -9925, "FY2023": -26891, "FY2022": -13864, "FY2021": 36718}),
    ("DATA", "Cash and cash equivalents at 1 Jan", {"FY2025": 63366, "FY2024": 73381, "FY2023": 100319, "FY2022": 114134, "FY2021": 77422}),
    ("DATA", "Exchange differences in respect of cash and cash equivalents", {"FY2025": 45, "FY2024": -90, "FY2023": -47, "FY2022": 49, "FY2021": -6}),
    ("TOTAL", "Cash and cash equivalents at 31 Dec", {"FY2025": 55299, "FY2024": 63366, "FY2023": 73381, "FY2022": 100319, "FY2021": 114134}),
]

bw.add_cash_flow_sheet(
    title="HSBC UK Bank plc — Consolidated Cash Flow Statement",
    subtitle="HSBC UK Bank plc consolidated, £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=82,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=170)


metric(
    "CET1 Capital", "£m",
    [("Common equity tier 1 (CET1) capital", {"FY2025": 15509, "FY2024": 15059, "FY2023": 14224, "FY2022": 12519, "FY2021": 12813})],
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2025": "13.2%", "FY2024": "13.6%", "FY2023": "14.0%", "FY2022": "13.5%", "FY2021": "15.3%"})],
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 18218, "FY2024": 17307, "FY2023": 16479, "FY2022": 14771, "FY2021": 15067})],
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "15.5%", "FY2024": "15.7%", "FY2023": "16.2%", "FY2022": "16.0%", "FY2021": "18.0%"})],
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 21888, "FY2024": 20500, "FY2023": 19772, "FY2022": 17847, "FY2021": 18067})],
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "18.6%", "FY2024": "18.6%", "FY2023": "19.5%", "FY2022": "19.3%", "FY2021": "21.6%"})],
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets", {"FY2025": 117463, "FY2024": 110423, "FY2023": 101478, "FY2022": 92413, "FY2021": 83723})],
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2025": "5.6%", "FY2024": "5.8%", "FY2023": "6.1%", "FY2022": "5.9%", "FY2021": "4.2%"})],
    note="A genuine basis change: FY2022-FY2025 are disclosed 'excluding claims on central banks' under the "
         "CRR II end-point basis (the new PRA disclosure template effective 1 January 2022), while FY2021's "
         "own report pre-dates that template and discloses a single leverage ratio (total exposure £358,237m, "
         "ratio 4.2%) that includes claims on central banks - a narrower/different exposure measure. FY2021 "
         "is left on its own originally-disclosed basis rather than forced onto the newer definition.",
)

metric(
    "LCR", "%, 12-month average",
    [("Liquidity coverage ratio", {"FY2025": "175%", "FY2024": "190%", "FY2023": "201%", "FY2022": "226%"})],
    note="Not disclosed for FY2021: HSBC UK Bank plc's own FY2021 Pillar 3 Disclosures pre-date the PRA's "
         "entity-level LCR quantitative-disclosure requirement (effective 1 January 2022, per the FY2022 "
         "Pillar 3 Disclosures' own footnote) - the FY2021 report only describes the LCR qualitatively, with "
         "no numeric value given. Confirmed genuinely absent, not an access gap. Reported on a 12-month "
         "rolling average basis (this project's standard convention).",
)

metric(
    "NSFR", "%, average of preceding 4 quarters",
    [("Net stable funding ratio", {"FY2025": "146%", "FY2024": "154%", "FY2023": "158%", "FY2022": "164%"})],
    note="Not disclosed for FY2021 - same reason as the LCR sheet (pre-dates the PRA's entity-level NSFR "
         "quantitative-disclosure requirement, effective 1 January 2022).",
)

# ---------------------------------------------------------------
# Additional interim Pillar 3 disclosures
# ---------------------------------------------------------------
# The standard metric sheets intentionally remain annual (one fixed column per
# year). HSBC UK publishes additional Q1/H1/Q3 disclosures, so these are kept
# in a separate wide matrix with periods across the columns.
INTERIM_PERIODS = [
    ("2025 Q3", "Q3", "2025-09-30"),
    ("2025 H1", "H1", "2025-06-30"),
    ("2025 Q1", "Q1", "2025-03-31"),
    ("2024 Q3", "Q3", "2024-09-30"),
    ("2024 H1", "H1", "2024-06-30"),
    ("2024 Q1", "Q1", "2024-03-31"),
    ("2023 Q3", "Q3", "2023-09-30"),
    ("2023 H1", "H1", "2023-06-30"),
    ("2023 Q1", "Q1", "2023-03-31"),
    ("2022 Q3", "Q3", "2022-09-30"),
    ("2022 H1", "H1", "2022-06-30"),
    ("2022 Q1", "Q1", "2022-03-31"),
    ("2021 H1", "H1", "2021-06-30"),
]

INTERIM_VALUES = {
    "CET1 Capital": [
        15626, 15255, 15211, 14966, 14550, 14611, 14818, 14382, 14317,
        12338, 12346, 12244, 13219,
    ],
    "Tier 1 Capital": [
        18334, 17963, 17423, 17220, 16802, 16864, 17072, 16632, 16567,
        14586, 14599, 14490, 15467,
    ],
    "Total Capital": [
        21978, 21632, 20598, 20375, 19990, 20053, 20140, 19671, 19625,
        17721, 17668, 17509, 18454,
    ],
    "Total RWAs": [
        117852, 115402, 112221, 105494, 104352, 102218, 100563, 99098, 99930,
        91917, 90209, 89803, 84555,
    ],
    "CET1 Ratio": [
        "13.3%", "13.2%", "13.6%", "14.2%", "13.9%", "14.3%", "14.7%", "14.5%", "14.3%",
        "13.4%", "13.7%", "13.6%", "15.6%",
    ],
    "Tier 1 Ratio": [
        "15.6%", "15.6%", "15.5%", "16.3%", "16.1%", "16.5%", "17.0%", "16.8%", "16.6%",
        "15.9%", "16.2%", "16.1%", "18.3%",
    ],
    "Total Capital Ratio": [
        "18.6%", "18.7%", "18.4%", "19.3%", "19.2%", "19.6%", "20.0%", "19.9%", "19.6%",
        "19.3%", "19.6%", "19.5%", "21.8%",
    ],
    "Leverage Ratio": [
        "5.7%", "5.7%", "5.8%", "5.8%", "5.9%", "6.1%", "6.4%", "6.3%", "6.3%",
        "5.6%", "5.8%", "5.8%", "4.6%",
    ],
    "LCR": [
        "181%", "186%", "189%", "192%", "193%", "196%", "206%", "213%", "220%",
        "232%", "232%", "230%", None,
    ],
    "NSFR": [
        "148%", "151%", "154%", "155%", "155%", "156%", "160%", "162%", "163%",
        "165%", "166%", "167%", None,
    ],
}

INTERIM_SOURCES = {
    "2025 Q3": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2025", "Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/3q/pdfs/hsbc-uk-bank-plc-ring-fenced-bank/251106-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-september-2025.pdf"),
    "2025 H1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 June 2025", "Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/interim/pdfs/hsbc-uk-bank-plc/250806-pillar-3-disclosures-at-30-june-2025.pdf"),
    "2025 Q1": ("HSBC UK Bank plc Pillar 3 Disclosures at 31 March 2025", "Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/1q/pdfs/hsbc-uk-bank-plc/250507-hbuk-pillar-3-disclosures-at-31-march-2025.pdf"),
    "2024 Q3": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2024", "p.3, Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/3q/pdfs/hsbc-uk-bank-plc-ring-fenced-bank/241105-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-september-2024.pdf"),
    "2024 H1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 June 2024", "p.4, Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/interim/pdfs/hsbc-uk-bank-plc/240806-pillar-3-disclosures-at-30-june-2024.pdf"),
    "2024 Q1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 June 2024", "p.4, Table 1 comparative", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2024/interim/pdfs/hsbc-uk-bank-plc/240806-pillar-3-disclosures-at-30-june-2024.pdf"),
    "2023 Q3": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2023", "p.3, Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/3q/pdfs/hsbc-bank-plc/231106-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-september-2023.pdf"),
    "2023 H1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2023", "p.3, Table 1 comparative", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/3q/pdfs/hsbc-bank-plc/231106-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-september-2023.pdf"),
    "2023 Q1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2023", "p.3, Table 1 comparative", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/3q/pdfs/hsbc-bank-plc/231106-hsbc-uk-bank-plc-pillar-3-disclosures-at-30-september-2023.pdf"),
    "2022 Q3": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2022", "p.3, Table 1", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/3q/pdfs/hsbc-uk-bank-plc/221102-pillar-3-disclosures-at-30-september-2022.pdf"),
    "2022 H1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2022", "p.3, Table 1 comparative", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/3q/pdfs/hsbc-uk-bank-plc/221102-pillar-3-disclosures-at-30-september-2022.pdf"),
    "2022 Q1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2022", "p.3, Table 1 comparative", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/3q/pdfs/hsbc-uk-bank-plc/221102-pillar-3-disclosures-at-30-september-2022.pdf"),
    "2021 H1": ("HSBC UK Bank plc Pillar 3 Disclosures at 30 September 2022", "p.3, Table 1 comparative", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2022/3q/pdfs/hsbc-uk-bank-plc/221102-pillar-3-disclosures-at-30-september-2022.pdf"),
}

def add_interim_pillar3_sheet():
    interim_rows = []
    basis = "HSBC UK Bank plc consolidated entity-level"
    for metric_name, values in INTERIM_VALUES.items():
        unit = "%" if "Ratio" in metric_name or metric_name in {"Leverage Ratio", "LCR", "NSFR"} else "£m"
        for idx, (period, disclosure_type, as_of) in enumerate(INTERIM_PERIODS):
            document, page, url = INTERIM_SOURCES[period]
            interim_rows.append(
                (period, disclosure_type, metric_name, values[idx], unit, basis, url, page)
            )

    note = (
        "Scope note: 2022–2025 Q1/H1/Q3 observations are taken from HSBC UK Bank plc's own entity-level "
        "Pillar 3 Table 1 disclosures or their comparative columns. The only 2021 interim observation found "
        "was 30 June 2021; LCR and NSFR were not disclosed for that period. MREL was not disclosed in the "
        "entity-level reports. Blank values are source gaps, not calculated estimates. HSBC UK Bank plc is "
        "distinct from HSBC Bank plc and HSBC Group."
    )
    bw.add_wide_interim_sheet(
        "Interim Pillar 3",
        rows=interim_rows,
        hyperlink_cells={(i, 6): row[6] for i, row in enumerate(interim_rows)},
        title="HSBC UK Bank plc — Interim Pillar 3",
        subtitle="Additional entity-level Q1/H1/Q3 observations; annual values remain on the standard metric sheets.",
        note=note,
    )


bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "No MREL figure or mention appears anywhere in any of HSBC UK Bank plc's own Pillar 3 "
                      "Disclosures FY2021-FY2025 - HSBC UK Bank plc is not itself a resolution entity under "
                      "the Bank of England's Single Point of Entry resolution strategy for the HSBC group "
                      "(that role sits with HSBC Holdings plc at the top of the group), so no entity-level "
                      "MREL requirement or ratio applies here - the same pattern as HSBC Bank plc's "
                      "relationship to the wider group (see that workbook).",
    },
)

add_interim_pillar3_sheet()

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": -2275, "FY2024": 3764, "FY2023": -20027, "FY2022": -9692, "FY2021": 30439}),
        ("Net cash from investing activities", {"FY2025": -4044, "FY2024": -11185, "FY2023": -6698, "FY2022": -2238, "FY2021": 4132}),
        ("Net cash from financing activities", {"FY2025": -1793, "FY2024": -2504, "FY2023": -166, "FY2022": -1934, "FY2021": 2147}),
        ("Cash and cash equivalents at 31 Dec", {"FY2025": 55299, "FY2024": 63366, "FY2023": 73381, "FY2022": 100319, "FY2021": 114134}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "13.2%", "FY2024": "13.6%", "FY2023": "14.0%", "FY2022": "13.5%", "FY2021": "15.3%"}),
        ("Tier 1 Ratio", {"FY2025": "15.5%", "FY2024": "15.7%", "FY2023": "16.2%", "FY2022": "16.0%", "FY2021": "18.0%"}),
        ("Total Capital Ratio", {"FY2025": "18.6%", "FY2024": "18.6%", "FY2023": "19.5%", "FY2022": "19.3%", "FY2021": "21.6%"}),
        ("Leverage Ratio", {"FY2025": "5.6%", "FY2024": "5.8%", "FY2023": "6.1%", "FY2022": "5.9%", "FY2021": "4.2%"}),
        ("LCR", {"FY2025": "175%", "FY2024": "190%", "FY2023": "201%", "FY2022": "226%"}),
        ("NSFR", {"FY2025": "146%", "FY2024": "154%", "FY2023": "158%", "FY2022": "164%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. MREL is not shown here (not disclosed at this "
         "entity level - see that sheet). The Leverage Ratio's FY2021 figure is on a different basis than "
         "FY2022-FY2025 - see the Leverage Ratio sheet's note.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HSBC UK BANK PLC FINANCIALS.xlsx")
