import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR_2025 = "https://www.mcafundingforchurches.co.uk/media/4bcl2vk5/mca-ar-2025.pdf"
AR_2024 = "https://www.mcafundingforchurches.co.uk/media/keybconk/annual-report-2024.pdf"
AR_2022 = "https://www.mcafundingforchurches.co.uk/sitefiles/resources/pdf/annualreport2022.pdf"
P3_2023 = "https://www.mcafundingforchurches.co.uk/media/ngqlqg5o/pillar-3-disclosures-2023.pdf"
P3_2022 = "https://www.mcafundingforchurches.co.uk/siteFiles/resources/pdf/Pillar3disclosures2022.pdf"

ENTITY = (
    "ENTITY NOTE: Methodist Chapel Aid Limited (Companies House 00030546, FRN 204508, "
    "LEI 213800GD7EDYBP4LH202) matches Banks List 2608.xlsx and Companies House. It is a "
    "UK-incorporated PRA/FCA-authorised bank operating on a standalone company basis. The "
    "2025 reporting period covers nine months ended 30 September 2025 after the accounting "
    "reference date changed from 31 December. The Company states that its Pillar 3 policy is "
    "annual. No defensible entity-level interim Pillar 3 series was located, so this is a "
    "13-sheet annual workbook. FY2024 and FY2025 absolute regulatory capital metrics were "
    "not separately disclosed in the located sources and are left blank rather than inferred "
    "from statutory net assets. MREL was not disclosed."
)


def cash_sources():
    return (
        "Sources - Methodist Chapel Aid Limited entity-level Statement of Cash Flows, £:\n"
        f"FY2025 (9 months ended 30 September 2025): MCA Annual report and accounts 2025, pp. 38-39 - {AR_2025}\n"
        f"FY2024: MCA Annual report and accounts 2024, pp. 36-39 - {AR_2024}\n"
        f"FY2023: MCA Annual report and accounts 2024 comparative, p. 39 - {AR_2024}\n"
        f"FY2022: MCA Annual report and accounts 2022, p. 38 - {AR_2022}\n"
        f"FY2021: MCA Annual report and accounts 2022 comparative, p. 38 - {AR_2022}\n\n"
        + ENTITY
    )


def p3_sources():
    return (
        "Sources - Methodist Chapel Aid Limited entity-level Pillar 3 / regulatory capital disclosures, £'000 unless stated:\n"
        f"FY2023: Pillar 3 Disclosures for year ended 31 December 2023, Key Metrics table, p. 3 - {P3_2023}\n"
        f"FY2022 and FY2021: Pillar 3 Disclosures for year ended 31 December 2022, Key Metrics table, p. 3 - {P3_2022}\n"
        "FY2024/FY2025: no separate absolute Key Metrics table was located; values left blank.\n\n"
        + ENTITY
    )


bw = BankWorkbook("Methodist Chapel Aid Limited", YEARS, header_color="6B4E71")

cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash generated/(used) from operating activities", {"FY2025": 230314, "FY2024": 429322, "FY2023": -3050504, "FY2022": -2346030, "FY2021": 714322}),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash generated/(used) from investing activities", {"FY2025": -249591, "FY2024": 661933, "FY2023": -364592, "FY2022": -261027, "FY2021": 519122}),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash generated/(used) in financing activities", {"FY2025": -1353, "FY2024": -1317, "FY2023": -1233, "FY2022": -1113, "FY2021": -1068}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -20630, "FY2024": 1089938, "FY2023": -3416329, "FY2022": -2608170, "FY2021": 1232376}),
    ("DATA", "Cash and cash equivalents at the beginning of year/period", {"FY2025": 10187072, "FY2024": 9097134, "FY2023": 12513463, "FY2022": 15121633, "FY2021": 13889257}),
    ("TOTAL", "Cash and cash equivalents at the end of year/period", {"FY2025": 10166442, "FY2024": 10187072, "FY2023": 9097134, "FY2022": 12513463, "FY2021": 15121633}),
]
bw.add_cash_flow_sheet(
    "Methodist Chapel Aid Limited — Cash Flow Statement",
    "Entity-level basis, £",
    cash_rows,
    cash_sources(),
    first_col_width=65,
    source_height=190,
    unit_suffix=" (£)",
)


def metric(name, unit, label, data, note=None):
    bw.add_metric_sheet(name, unit, [(label, data)], p3_sources(), note=note, first_col_width=50, source_height=190)


metric("CET1 Capital", "£'000", "CET1 capital", {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919}, "FY2024 and FY2025 absolute regulatory capital was not separately disclosed in the located sources.")
metric("CET1 Ratio", "%", "CET1 ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%"}, "FY2024 and FY2025 ratio not separately disclosed in the located sources.")
metric("Tier 1 Capital", "£'000", "Tier 1 capital", {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919}, "All disclosed Tier 1 capital was CET1; FY2024 and FY2025 were not separately disclosed.")
metric("Tier 1 Ratio", "%", "Tier 1 ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%"}, "FY2024 and FY2025 ratio not separately disclosed in the located sources.")
metric("Total Capital", "£'000", "Total capital", {"FY2023": 13354, "FY2022": 12952, "FY2021": 13919}, "All disclosed total capital was CET1; FY2024 and FY2025 were not separately disclosed.")
metric("Total Capital Ratio", "%", "Total capital ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%"}, "FY2024 and FY2025 ratio not separately disclosed in the located sources.")
metric("Total RWAs", "£'000", "Total risk-weighted exposure amount", {"FY2023": 25253, "FY2022": 24052, "FY2021": 26369}, "FY2024 and FY2025 absolute RWA was not separately disclosed in the located sources.")
metric("Leverage Ratio", "%", "Leverage ratio", {"FY2023": "35.4%", "FY2022": "33.49%", "FY2021": "33.05%"}, "The Company states that the smaller-bank leverage requirement does not apply; reported ratios are included as disclosed. FY2024 and FY2025 were not separately disclosed.")
metric("LCR", "%", "Average liquidity coverage ratio", {"FY2023": "835%", "FY2022": "833%", "FY2021": "603%"}, "FY2023 is the average based on quarterly end-of-month positions; FY2024 and FY2025 were not separately disclosed.")
metric("NSFR", "%", "Average net stable funding ratio", {"FY2023": "182%", "FY2022": "192%", "FY2021": "184%"}, "FY2023 is the average based on quarterly end-of-month positions; FY2024 and FY2025 were not separately disclosed.")
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": "No MREL ratio was disclosed in the located Methodist Chapel Aid Pillar 3 documents."})

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated/(used) from operating activities", {"FY2025": 230314, "FY2024": 429322, "FY2023": -3050504, "FY2022": -2346030, "FY2021": 714322}),
        ("Net cash generated/(used) from investing activities", {"FY2025": -249591, "FY2024": 661933, "FY2023": -364592, "FY2022": -261027, "FY2021": 519122}),
        ("Net cash generated/(used) in financing activities", {"FY2025": -1353, "FY2024": -1317, "FY2023": -1233, "FY2022": -1113, "FY2021": -1068}),
        ("Cash and cash equivalents at end of year/period", {"FY2025": 10166442, "FY2024": 10187072, "FY2023": 9097134, "FY2022": 12513463, "FY2021": 15121633}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%"}),
        ("Total Capital Ratio", {"FY2023": "52.88%", "FY2022": "53.85%", "FY2021": "52.79%"}),
        ("Leverage Ratio", {"FY2023": "35.4%", "FY2022": "33.49%", "FY2021": "33.05%"}),
        ("LCR", {"FY2023": "835%", "FY2022": "833%", "FY2021": "603%"}),
    ],
    note=ENTITY,
)

bw.save("/Users/armaan/code/katalysis/banks/METHODIST CHAPEL AID FINANCIALS.xlsx")
print("Saved.")
