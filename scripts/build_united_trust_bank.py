import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# PILLAR-3-ONLY WORKBOOK
# United Trust Bank Limited (company 00549690, FRN 204463) is the regulated
# operating bank within UTB Partners Plc.  The available Pillar 3 disclosures
# are prepared on the consolidated UTB Partners group basis, not as a solo UTB
# series.  The statutory accounts omit a cash-flow statement; consequently the
# workbook records the limitation and presents the available regulatory data.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

P3 = {
    "FY2025": "https://www.utbank.co.uk/wp-content/uploads/2026/03/UTB-Partners-Pillar-3-Disclosure-2025.pdf",
    "FY2024": "https://www.utbank.co.uk/wp-content/uploads/2025/03/UTB-Partners-Pillar-3-Disclosure-2024.pdf",
    "FY2023": "https://www.utbank.co.uk/wp-content/uploads/2024/03/UTB-Partners-Pillar-3-Disclosure-2023.pdf",
    "FY2022": "https://www.utbank.co.uk/wp-content/uploads/2023/03/UTB-Partners-Pillar-3-Disclosure-2022-.pdf",
    "FY2021": "https://rebrand-dev.utbank.co.uk/wp-content/uploads/2022/03/UTB-Partners-Pillar-3-Disclosure-2021-FINAL1-.pdf",
}
ACCOUNTS_2024 = "https://www.utbank.co.uk/wp-content/uploads/2025/03/UTB-Report-and-Accounts-2024.pdf"
CH = "https://find-and-update.company-information.service.gov.uk/company/00549690/filing-history"

ENTITY_NOTE = (
    "ENTITY AND BASIS: United Trust Bank Limited (company 00549690, FCA/PRA FRN 204463) is the regulated,"
    " material operating bank and wholly-owned subsidiary of UTB Partners Plc. The Pillar 3 reports used here"
    " constitute consolidated disclosures of UTB Partners Plc; UTB Partners is a financial holding company and"
    " the group is supervised on a consolidated basis. SOS Intelligence is immaterial and excluded from regulatory"
    " consolidation. Accordingly, all figures in this workbook are explicitly labelled CONSOLIDATED UTB PARTNERS"
    " BASIS and must not be read as standalone United Trust Bank Limited figures."
)

EXEMPTION_NOTE = (
    "CASH-FLOW LIMITATION: United Trust Bank Limited's published 2024 Report and Accounts contains the"
    " Income Statement, Statement of Comprehensive Income, Statement of Financial Position and Statement of"
    " Changes in Equity, but no Statement of Cash Flows; the Companies House filing history likewise describes"
    " the accounts as full accounts. The available accounts and source material do not provide a cash-flow"
    " statement suitable for this workbook. The Cash Flow Statement sheet therefore records this limitation"
    " rather than inferring or fabricating cash-flow values."
)


def sources():
    return (
        "Sources - consolidated UTB Partners Plc basis, £'000 unless stated:\n"
        "FY2025: UTB Partners Pillar 3 Disclosure 2025, Table KM1, pp.6-7 - " + P3["FY2025"] + "\n"
        "FY2024: UTB Partners Pillar 3 Disclosure 2024, Table KM1, pp.6-7 - " + P3["FY2024"] + "\n"
        "FY2023: UTB Partners Pillar 3 Disclosure 2023, Appendix 1 Table KM1, pp.44-45 - " + P3["FY2023"] + "\n"
        "FY2022: UTB Partners Pillar 3 Disclosure 2022, Appendix 1 Table KM1, p.43 - " + P3["FY2022"] + "\n"
        "FY2021: UTB Partners Pillar 3 Disclosure 2022 comparative column and 2021 disclosure, Appendix 1 /"
        " own-funds and leverage templates - " + P3["FY2021"] + "\n"
        "Accounts cross-check: United Trust Bank Report and Accounts 2024, pp.47-50 - " + ACCOUNTS_2024 + "\n"
        "Companies House entity and filing history (company 00549690) - " + CH + "\n\n" + ENTITY_NOTE
    )


bw = BankWorkbook(
    bank_name="United Trust Bank Limited (consolidated UTB Partners basis)",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="1B4965",
)

bw.add_cash_flow_sheet(
    title="United Trust Bank Limited — Cash Flow Statement",
    subtitle="Not available in the published statutory accounts; this is a Pillar-3-only workbook.",
    rows=[
        ("SECTION", "No Statement of Cash Flows available for the covered entity", {}),
        ("DATA", "See the source note below. No cash-flow values are inferred.", {}),
    ],
    sources_text=ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE + "\n\n" + sources(),
    first_col_width=90,
    source_height=270,
    unit_suffix="",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(
        name, unit, rows_data, sources(), note=note, first_col_width=54, source_height=235
    )


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {
    "FY2025": 390450, "FY2024": 330662, "FY2023": 268495,
    "FY2022": 209850, "FY2021": 170785,
})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {
    "FY2025": "14.01%", "FY2024": "13.04%", "FY2023": "11.79%",
    "FY2022": "12.07%", "FY2021": "12.74%",
})])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {
    "FY2025": 453206, "FY2024": 344803, "FY2023": 283710,
    "FY2022": 226701, "FY2021": 187636,
})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {
    "FY2025": "16.27%", "FY2024": "13.60%", "FY2023": "12.46%",
    "FY2022": "13.04%", "FY2021": "14.00%",
})])
metric("Total Capital", "£'000", [("Total capital", {
    "FY2025": 482806, "FY2024": 400094, "FY2023": 340213,
    "FY2022": 257803, "FY2021": 218186,
})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {
    "FY2025": "17.33%", "FY2024": "15.78%", "FY2023": "14.94%",
    "FY2022": "14.83%", "FY2021": "16.28%",
})])
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", {
    "FY2025": 2785964, "FY2024": 2535096, "FY2023": 2277864,
    "FY2022": 1738779, "FY2021": 1340432,
})], note=(
    "Each year's own published figure is preserved. The 2024 report's OV1 table shows 2,535,339 for 2024 "
    "versus the KM1 figure 2,535,096; the KM1 value is used for consistency with the capital ratios."
))
metric("Leverage Ratio", "£'000 / %", [
    ("Total exposure measure excluding claims on central banks", {
        "FY2025": 4500670, "FY2024": 3979115, "FY2023": 3502424,
        "FY2022": 2878801, "FY2021": 2318303,
    }),
    ("Leverage ratio excluding claims on central banks", {
        "FY2025": "10.1%", "FY2024": "8.7%", "FY2023": "8.1%",
        "FY2022": "7.9%", "FY2021": "8.1%",
    }),
])
metric("LCR", "£'000 / %", [
    ("Total high-quality liquid assets (HQLA), weighted value - average", {
        "FY2025": 384058, "FY2024": 322714, "FY2023": 257050,
        "FY2022": 252352,
    }),
    ("Total net cash outflows, adjusted value", {
        "FY2025": 113223, "FY2024": 40033, "FY2023": 32258,
        "FY2022": 19185,
    }),
    ("Liquidity coverage ratio", {
        "FY2025": "398.42%", "FY2024": "806.12%", "FY2023": "796.86%",
        "FY2022": "1315.36%", "FY2021": "1013.36%",
    }),
], note=(
    "The FY2021 disclosure does not provide a KM1 LCR table; only the headline ratio is available in the FY2022 "
    "comparative column. The FY2022 and FY2023 reports contain materially different comparative LCR figures; "
    "this series preserves each year's own as-reported value."
))
metric("NSFR", "£'000 / %", [
    ("Total available stable funding", {
        "FY2025": 3590720, "FY2024": 3376614, "FY2023": 3057724,
        "FY2022": 2555002,
    }),
    ("Total required stable funding", {
        "FY2025": 2570256, "FY2024": 2367394, "FY2023": 2057282,
        "FY2022": 1648317,
    }),
    ("NSFR ratio", {
        "FY2025": "139.71%", "FY2024": "142.63%", "FY2023": "148.63%",
        "FY2022": "155.01%",
    }),
], note="No 2021 NSFR headline or component values were located in the 2021 disclosure or the 2022 comparative column.")
metric("MREL Ratio", "£'000 / %", [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], note=(
    "No MREL ratio or numeric MREL requirement was located in the five UTB Partners Pillar 3 reports reviewed."
))

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "14.01%", "FY2024": "13.04%", "FY2023": "11.79%", "FY2022": "12.07%", "FY2021": "12.74%"}),
        ("Tier 1 Ratio", {"FY2025": "16.27%", "FY2024": "13.60%", "FY2023": "12.46%", "FY2022": "13.04%", "FY2021": "14.00%"}),
        ("Total Capital Ratio", {"FY2025": "17.33%", "FY2024": "15.78%", "FY2023": "14.94%", "FY2022": "14.83%", "FY2021": "16.28%"}),
        ("Leverage Ratio", {"FY2025": "10.1%", "FY2024": "8.7%", "FY2023": "8.1%", "FY2022": "7.9%", "FY2021": "8.1%"}),
        ("LCR", {"FY2025": "398.42%", "FY2024": "806.12%", "FY2023": "796.86%", "FY2022": "1315.36%", "FY2021": "1013.36%"}),
        ("NSFR", {"FY2025": "139.71%", "FY2024": "142.63%", "FY2023": "148.63%", "FY2022": "155.01%"}),
    ],
    note=(
        "PILLAR-3-ONLY: statutory cash-flow data is not available in the entity accounts. All regulatory metrics "
        "are consolidated UTB Partners basis, not standalone UTB Limited. FY2021 LCR is headline-only and FY2021 "
        "NSFR is unavailable; MREL is not publicly disclosed."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/UNITED TRUST BANK FINANCIALS.xlsx")
