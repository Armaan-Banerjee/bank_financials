import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 Dec)
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.datocms-assets.com/23873/1773841899-zopa_bank_ar25_web.pdf"
AR2024_URL = "https://www.datocms-assets.com/23873/1747055131-zopa-bank-2024-annual-report-signed-web-based.pdf"
AR2023_URL = "https://www.datocms-assets.com/23873/1713257733-zopa-group-2023-annual-report-signed_web-version.pdf"
AR2022_URL = "https://www.datocms-assets.com/23873/1694796852-zopa-bank-annual-report-2022-web.pdf"
AR2021_URL = "https://www.datocms-assets.com/23873/1658745948-zopa-bank-annual-report-2021.pdf"

P3_2025_URL = "https://www.datocms-assets.com/23873/1773842098-12-25-pillar-3-disclosures.pdf"
P3_2024_URL = "https://www.datocms-assets.com/23873/1745405670-2024-zopa-bank-pillar-3-disclosures.pdf"
P3_2023_URL = "https://www.datocms-assets.com/23873/1715596314-2023-pillar-3-disclosures-final.pdf"
P3_2022_URL = "https://www.datocms-assets.com/23873/1696603046-2022-pillar-3-disclosures-final_051023.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Zopa Bank Limited (FRN 800542, Companies House 10627575) is the PRA-authorised entity. It sits "
    "beneath a group holding company (Zopa Group Limited, later re-registered Zopa Group PLC) whose own separate "
    "consolidated accounts and Pillar 3 disclosures also exist - this workbook uses Zopa Bank Limited's own "
    "entity-level figures throughout (its own 'Statement of cash flows' in its own Annual Report and Accounts, "
    "and the dedicated 'Section 4: Disclosures for Zopa Bank Limited' within each year's Pillar 3 report, not the "
    "wider Group-level Section 3), consistent with the ring-fenced/individual-entity basis used elsewhere in this "
    "workbook series. Pillar 3 capital figures differ slightly from the Bank's own Annual Report & Accounts because "
    "they include audited profit and the full amount of Tier 2 capital (stated explicitly in each Pillar 3 report)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Zopa Bank Limited's own Statement of cash flows, £'000:\n"
    f"FY2025 & FY2024: Zopa Bank Limited Annual Report and Accounts 2025, p.101 (Statement of cash flows) - {AR2025_URL}\n"
    f"FY2023: Zopa Bank Limited Annual Report and Accounts 2023, p.114 (Statement of cash flows) - {AR2023_URL} "
    f"(cross-checked against its comparative appearance in the 2024 Annual Report, p.111 - {AR2024_URL} - matched exactly)\n"
    f"FY2022: Zopa Bank Limited Annual Report and Accounts 2022, p.95 (Statement of cash flows) - {AR2022_URL} "
    f"(cross-checked against its comparative appearance in the 2023 Annual Report, p.114 - matched exactly)\n"
    f"FY2021: Zopa Bank Limited Annual Report and Accounts 2021, p.69 (Statement of cash flows) - {AR2021_URL} "
    f"(cross-checked against its comparative appearance in the 2022 Annual Report, p.95 - matched exactly)\n"
    "Note: the 2021 Annual Report states 'the statement of cash flows has been represented' vs. its own prior-year "
    "presentation (details in that report's note 1.9) - not a concern for the FY2021-FY2025 figures shown here, "
    "which are all on a mutually consistent, cross-checked basis.\n\n"
    + ENTITY_NOTE
)


def p3_sources(page="14-15"):
    return (
        "Sources - Zopa Bank Limited basis (Section 4: 'Disclosures for Zopa Bank Limited', within each year's "
        "'Zopa Group' Pillar 3 Disclosures document):\n"
        f"FY2025 & FY2024: Pillar 3 Disclosures, year ended 31 December 2025, p.14-15 (Table 5: UK KM1 - Key "
        f"metrics table) - {P3_2025_URL}\n"
        f"FY2023: Pillar 3 Disclosures, year ended 31 December 2023, p.14-15 (Table 5: UK KM1) - {P3_2023_URL} "
        f"(cross-checked against its comparative in the 2024 report, p.14 - {P3_2024_URL} - matched exactly)\n"
        f"FY2022: Pillar 3 Disclosures, year ended 31 December 2022, p.13-14 (Table 5: UK KM1) - {P3_2022_URL} "
        f"(cross-checked against its comparative in the 2023 report, p.14 - matched exactly)\n"
        f"FY2021: as the comparative ('Dec-21') column in the Pillar 3 Disclosures, year ended 31 December 2022, "
        f"p.13-14 (Table 5: UK KM1) - {P3_2022_URL} (Zopa's FY2021 Pillar 3 document is titled/structured as a "
        "Group-only disclosure with no equivalent Bank-specific KM1 section, so the FY2022 report's own comparative "
        "column is used as the citable Bank-level source for FY2021 instead)"
    )


bw = BankWorkbook(bank_name="Zopa Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="1B4332")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit/(loss) before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 44852, "FY2024": 31550, "FY2023": 15817, "FY2022": -25988, "FY2021": -34224}),
    ("DATA", "Non-cash items", {"FY2025": 108122, "FY2024": 67370, "FY2023": 66198, "FY2022": 92460, "FY2021": 50828}),
    ("DATA", "Changes in operating assets and liabilities", {"FY2025": 216056, "FY2024": 1640591, "FY2023": -133115, "FY2022": 1082800, "FY2021": -192441}),
    ("DATA", "Current tax expense", {"FY2025": -5687, "FY2024": -3439, "FY2023": -1337}),
    ("DATA", "Tax received", {"FY2021": 0}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 363343, "FY2024": 1736072, "FY2023": -52437, "FY2022": 1149272, "FY2021": -175837}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of investment securities", {"FY2025": -948990, "FY2024": -431925, "FY2023": -80367}),
    ("DATA", "Investment securities matured during the year", {"FY2025": 154254, "FY2024": 67356}),
    ("DATA", "Disposal of property, plant and equipment", {"FY2021": 0}),
    ("DATA", "Purchase of non-current assets from related party", {"FY2021": 0}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -1486, "FY2024": -659, "FY2023": -1167, "FY2022": -610, "FY2021": -519}),
    ("DATA", "Purchase and development of intangible assets", {"FY2025": -21194, "FY2024": -23775, "FY2023": -10779, "FY2022": -3948, "FY2021": -2036}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -817416, "FY2024": -389003, "FY2023": -92313, "FY2022": -4558, "FY2021": -2555}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Shares issued", {"FY2025": 7000, "FY2024": 68500, "FY2023": 65000, "FY2022": 72000, "FY2021": 157000}),
    ("DATA", "Issuance of other equity instruments", {"FY2025": 80000}),
    ("DATA", "Transaction costs on issuance of other equity instruments", {"FY2025": -1702}),
    ("DATA", "Coupon payment on other equity instruments", {"FY2025": -5150}),
    ("DATA", "Proceeds from issuance of subordinated liabilities", {"FY2023": 75000}),
    ("DATA", "Repayment of TFSME borrowings", {"FY2025": -150000}),
    ("DATA", "Proceeds from ILTR borrowings", {"FY2025": 50000}),
    ("DATA", "Change in TFSME and ILTR borrowings", {"FY2023": -19316, "FY2022": -3791}),
    ("DATA", "Change in amounts due to banks", {"FY2021": 175182}),
    ("DATA", "Change in non-trading amounts due to and from other Group undertakings", {"FY2025": -5393, "FY2024": 4, "FY2023": -74, "FY2022": -16507, "FY2021": 15144}),
    ("DATA", "Cash payments/principal elements on lease liabilities", {"FY2025": -1928, "FY2024": -1822, "FY2023": -1745, "FY2022": -2297, "FY2021": -632}),
    ("TOTAL", "Net cash (used in)/generated from financing activities", {"FY2025": -27173, "FY2024": 66682, "FY2023": 118865, "FY2022": 49405, "FY2021": 346694}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -481246, "FY2024": 1413751, "FY2023": -25885, "FY2022": 1194119, "FY2021": 168302}),
    ("DATA", "Cash and cash equivalents at start of year", {"FY2025": 2819743, "FY2024": 1405992, "FY2023": 1431877, "FY2022": 237758, "FY2021": 69456}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 2338497, "FY2024": 2819743, "FY2023": 1405992, "FY2022": 1431877, "FY2021": 237758}),
]

bw.add_cash_flow_sheet(
    title="Zopa Bank Limited — Cash Flow Statement",
    subtitle="Zopa Bank Limited (entity-level), £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Zopa Bank Limited basis, {unit}" if unit else "Zopa Bank Limited basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=120)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 489, "FY2024": 448, "FY2023": 364, "FY2022": 290, "FY2021": 243})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "14.54%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 567, "FY2024": 448, "FY2023": 364, "FY2022": 290, "FY2021": 243})],
    p3_sources(),
    note="Tier 1 = CET1 in every year except FY2025, where the Bank issued £80m of other (AT1) equity instruments "
         "during the year (see Cash Flow Statement sheet), taking Tier 1 above CET1 for the first time.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "16.87%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 642, "FY2024": 523, "FY2023": 439, "FY2022": 290, "FY2021": 243})],
    p3_sources(),
    note="Total capital includes Tier 2 capital (subordinated debt) from FY2023 onward - £75m issued, of which "
         "£63m/£72m/£73m was eligible as at FY2023/FY2024/FY2025 respectively (stated in each year's Pillar 3 "
         "report). No Tier 2 capital existed in FY2021-FY2022, so Total Capital = Tier 1 in those years.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "19.10%", "FY2024": "19.57%", "FY2023": "19.90%", "FY2022": "17.44%", "FY2021": "22.92%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 3364, "FY2024": 2670, "FY2023": 2205, "FY2022": 1663, "FY2021": 1060})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 4998, "FY2024": 3445, "FY2023": 2699, "FY2022": 2024}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "11.36%", "FY2024": "12.99%", "FY2023": "13.48%", "FY2022": "14.34%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="Not disclosed for FY2021: the Dec-21 comparative column in the 2022 Pillar 3 report shows 'n/a' for both "
         "the leverage exposure measure and ratio, with no explanation given (likely below an applicable "
         "disclosure/reporting threshold at that date).",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 2970, "FY2024": 2347, "FY2023": 1701, "FY2022": 626}),
        ("Total net cash outflows, adjusted value", {"FY2025": 614, "FY2024": 430, "FY2023": 233, "FY2022": 61}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "484%", "FY2024": "546%", "FY2023": "730%", "FY2022": "1,033%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="LCR is a 12-month simple average of month-end observations, which the Pillar 3 report notes 'differs to "
         "the metrics reported in the Bank ARA, which present the position at the year-end date' - the Pillar 3 "
         "(averaged) basis is used here for consistency across years. Not disclosed for FY2021: LCR was a new "
         "disclosure requirement from the FY2022 report onward with no FY2021 comparative provided.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2025": 5761, "FY2024": 4918, "FY2023": 3701}),
        ("Total required stable funding", {"FY2025": 2562, "FY2024": 2162, "FY2023": 1785}),
        ("NSFR ratio (%)", {"FY2025": "225%", "FY2024": "227%", "FY2023": "207%", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
    ],
    p3_sources(),
    note="NSFR disclosure was not applicable/required until 1 January 2023 (PRA PS22/21), so no FY2022 or FY2021 "
         "figures exist.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL disclosure of any kind (numeric or qualitative) was found in Zopa Bank Limited's Pillar 3 "
         "reports for any year reviewed (FY2021-FY2025) - unlike some smaller banks in this workbook series, no "
         "report explicitly states an SNCI/below-threshold exemption reason, it is simply absent from every KM1 "
         "template and surrounding narrative.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 363343, "FY2024": 1736072, "FY2023": -52437, "FY2022": 1149272, "FY2021": -175837}),
        ("Net cash from/(used in) investing activities", {"FY2025": -817416, "FY2024": -389003, "FY2023": -92313, "FY2022": -4558, "FY2021": -2555}),
        ("Net cash from/(used in) financing activities", {"FY2025": -27173, "FY2024": 66682, "FY2023": 118865, "FY2022": 49405, "FY2021": 346694}),
        ("Cash and cash equivalents at end of year", {"FY2025": 2338497, "FY2024": 2819743, "FY2023": 1405992, "FY2022": 1431877, "FY2021": 237758}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "14.54%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%"}),
        ("Tier 1 Ratio", {"FY2025": "16.87%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%"}),
        ("Total Capital Ratio", {"FY2025": "19.10%", "FY2024": "19.57%", "FY2023": "19.90%", "FY2022": "17.44%", "FY2021": "22.92%"}),
        ("Leverage Ratio", {"FY2025": "11.36%", "FY2024": "12.99%", "FY2023": "13.48%", "FY2022": "14.34%"}),
        ("LCR", {"FY2025": "484%", "FY2024": "546%", "FY2023": "730%", "FY2022": "1,033%"}),
        ("NSFR", {"FY2025": "225%", "FY2024": "227%", "FY2023": "207%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. All figures are Zopa Bank Limited's own entity-level basis, "
         "not the wider Zopa Group.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ZOPA FINANCIALS.xlsx")
