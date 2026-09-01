import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzQ3OTMzNTI0NWFkaXF6a2N4/document?download=0&format=pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzQzMzA4NzcwMWFkaXF6a2N4/document?download=0&format=pdf"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzM4OTExNTc1NmFkaXF6a2N4/document?download=0&format=pdf"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history/MzM1NTU5ODQzNmFkaXF6a2N4/document?download=0&format=pdf"
PILLAR3_2021_URL = "https://www.persiabank.co.uk/Pillar%203%202021%20v3.pdf"

# The Bank reports in EUR and discloses its own EUR/GBP rates in the accounting
# policies.  Rates are EUR per GBP, so EUR / rate = GBP.
AVG_RATE = {"FY2025": 0.8390, "FY2024": 0.8630, "FY2023": 0.8525, "FY2022": 0.8525, "FY2021": 0.8925}
YEAR_END_RATE = {"FY2025": 0.8350, "FY2024": 0.8550, "FY2023": 0.8800, "FY2022": 0.8475, "FY2021": 0.8525}

ENTITY_NOTE = (
    "ENTITY AND REPORTING BASIS: Persia International Bank Plc (company 04218020, FRN 208020) is an active UK "
    "PRA/FCA-regulated bank incorporated 16 May 2001, with registered office at 6 Lothbury, London EC2R 7HH. "
    "Companies House shows full accounts filed through the year ended 31 March 2025; the Bank is owned 60% by Bank "
    "Mellat and 40% by Bank Tejarat. These are the Company's own entity-level financial statements, prepared under "
    "UK-adopted IFRS on a going-concern basis, in EUR (the functional and presentation currency). The Bank's reports "
    "say that OFAC sanctions re-imposed in November 2018 and continuing difficulty obtaining UK clearing and "
    "correspondent-bank relationships restrict normal banking activity; Iranian exposures continue to receive a 150% "
    "risk weight because Iran is excluded from the relevant UK/EU equivalence list. The reports nevertheless state "
    "that the Bank expects to continue as a going concern. The FY2022 report's auditor highlighted material uncertainty "
    "over going concern, while later reports continued on a going-concern basis."
)

FX_NOTE = (
    "FX METHODOLOGY: the Bank's accounting policies disclose EUR/GBP rates (EUR per GBP). Flow figures are divided "
    "by the year's disclosed average rate; balance figures are divided by the year's disclosed year-end rate. The "
    "cash-flow sheet includes the Bank's own exchange-difference line and a programmatic GBP translation line where "
    "the use of average rates for flows and year-end rates for balances creates a residual. FY2021 opening cash is "
    "left blank because the source does not provide a FY2020 year-end rate in the reviewed five-year source set."
)

CASH_FLOW_SOURCES = (
    "Sources - Persia International Bank Plc's own entity-level Statements of Cash Flows, converted from EUR to GBP "
    "using the Bank's disclosed rates (see FX note):\n"
    f"FY2025: Annual Report and Financial Statements for year ended 31 March 2025, p.39 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements for year ended 31 March 2024, p.32 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements for year ended 31 March 2023, p.31 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for year ended 31 March 2022, p.30 - {AR2022_URL}\n"
    "FY2021: FY2022 Annual Report's comparative column, p.30 - " + AR2022_URL + "\n\n" + ENTITY_NOTE + "\n" + FX_NOTE
)


def p3_sources():
    return (
        "Sources - Persia International Bank Plc entity-level capital disclosures:\n"
        f"FY2025/FY2024: Annual Report and Financial Statements 2025, Note 25 (Capital management), p.77 - {AR2025_URL}\n"
        f"FY2023/FY2022: Annual Report and Financial Statements 2023, Note 26 (Capital management), p.62 - {AR2023_URL}\n"
        f"FY2021: Annual Report and Financial Statements 2022, Note 26 (Capital management), p.58 - {AR2022_URL}\n"
        f"FY2021 Pillar 3: Persia International Bank Pillar 3 Disclosure 2021, pp.16-20 and 26 - {PILLAR3_2021_URL}\n"
        "The Bank states in the FY2023-FY2025 annual reports that Pillar 3 disclosures are made separately and can "
        "be made available on request; no public 2022-2025 Pillar 3 document was locatable. The 2021 Pillar 3 document "
        "is unaudited and provides the only directly disclosed FY2021 RWA, LCR and leverage values used here."
    )


def flow(values):
    return {y: round(v / AVG_RATE[y], 1) for y, v in values.items()}


def stock(values):
    return {y: round(v / YEAR_END_RATE[y], 1) for y, v in values.items()}


bw = BankWorkbook(bank_name="Persia International Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="6B3E75")

# EUR '000, each year's own published cash-flow column.  FY2021 is taken from
# the FY2022 comparative because that is the latest filing that contains it.
OPERATING_EUR = {"FY2025": 1998, "FY2024": -14216, "FY2023": 5116, "FY2022": 3399, "FY2021": -368}
INVESTING_EUR = {"FY2025": -2, "FY2024": -72, "FY2023": -46, "FY2022": -44, "FY2021": 0}
FINANCING_EUR = {"FY2025": -227, "FY2024": -27477, "FY2023": -1320, "FY2022": -9186, "FY2021": -1609}
NET_CHANGE_EUR = {"FY2025": 1787, "FY2024": -41765, "FY2023": 3750, "FY2022": -5831, "FY2021": -1977}
EXCHANGE_EUR = {"FY2025": -145, "FY2024": 1009, "FY2023": -44, "FY2022": 0, "FY2021": 0}
OPENING_EUR = {"FY2025": 75472, "FY2024": 116228, "FY2023": 170661, "FY2022": 176492, "FY2021": 178469}
CLOSING_EUR = {"FY2025": 77114, "FY2024": 75472, "FY2023": 174367, "FY2022": 170661, "FY2021": 176492}

closing_gbp = stock(CLOSING_EUR)
# Opening balances are the prior year's converted closing balances.  This keeps
# the cash-flow chain internally consistent when the Bank's year-end FX rates
# differ between years.
opening_gbp = {
    "FY2025": closing_gbp["FY2024"],
    "FY2024": closing_gbp["FY2023"],
    "FY2023": closing_gbp["FY2022"],
    "FY2022": closing_gbp["FY2021"],
}
net_change_gbp = flow(NET_CHANGE_EUR)
exchange_gbp = flow(EXCHANGE_EUR)
translation = {
    y: round(closing_gbp[y] - opening_gbp[y] - net_change_gbp[y] - exchange_gbp[y], 1)
    for y in YEARS if y in opening_gbp
}

rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash flow from operating activities", flow(OPERATING_EUR)),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash flow from investing activities", flow(INVESTING_EUR)),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash flow from financing activities", flow(FINANCING_EUR)),
    ("TOTAL", "Net (decrease) / increase in cash and cash equivalents", net_change_gbp),
    ("DATA", "Exchange difference (Bank's own EUR statement line)", exchange_gbp),
    ("DATA", "Effect of GBP/EUR translation (this workbook's conversion line)", translation),
    ("DATA", "Cash and cash equivalents at the beginning of the year", opening_gbp),
    ("TOTAL", "Cash and cash equivalents at the end of the year", closing_gbp),
]

bw.add_cash_flow_sheet(
    title="Persia International Bank Plc — Statement of Cash Flows",
    subtitle="Entity-level basis, £'000 converted from EUR; see source note for sanctions, reporting basis and FX methodology",
    rows=rows, sources_text=CASH_FLOW_SOURCES, first_col_width=86, source_height=330,
    unit_suffix=" (£'000, conv. from EUR)",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=50, source_height=240)


CAPITAL_EUR = {"FY2025": 110424, "FY2024": 127693, "FY2023": 132561, "FY2022": 131758, "FY2021": 130644}
CAPITAL_GBP = stock(CAPITAL_EUR)
RWA_GBP = {"FY2021": round(318824 / YEAR_END_RATE["FY2021"], 1)}
NOT_DISCLOSED = (
    "Not publicly disclosed for this entity/year. The Bank says later Pillar 3 disclosures are available on request; "
    "no public 2022-2025 Pillar 3 document was found, and the statutory accounts do not state this metric."
)
CAPITAL_NOTE = (
    "Directly disclosed total regulatory capital base / Tier one capital from the annual-report capital-management "
    "table. The Bank's table does not separately disclose CET1, Additional Tier 1 or Tier 2 amounts for FY2022-FY2025; "
    "the value is therefore repeated as the entity's disclosed Tier one/regulatory capital base, not inferred as a full "
    "Basel capital stack. FY2021's Pillar 3 table reports Own Funds of €130.644m and Tier 2 of zero."
)

metric("CET1 Capital", "£'000 (conv. from EUR)", [("Common Equity Tier 1 capital / disclosed Tier one base", CAPITAL_GBP)], note=CAPITAL_NOTE)
metric("CET1 Ratio", "%", [("CET1 ratio", {"FY2021": "Not publicly disclosed"})], note=NOT_DISCLOSED)
metric("Tier 1 Capital", "£'000 (conv. from EUR)", [("Tier one / total regulatory capital base", CAPITAL_GBP)], note=CAPITAL_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", {"FY2021": "Not publicly disclosed"})], note=NOT_DISCLOSED)
metric("Total Capital", "£'000 (conv. from EUR)", [("Total regulatory capital base", CAPITAL_GBP)], note=CAPITAL_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", {"FY2021": "Not publicly disclosed"})], note=NOT_DISCLOSED)
metric("Total RWAs", "£'000 (conv. from EUR)", [("Pillar 1 risk-weighted assets", RWA_GBP)], note="Only FY2021 is directly disclosed: €318.824m in the 2021 Pillar 3 disclosure, p.18. Later years are not publicly disclosed and are not calculated from capital because no corresponding capital ratio is stated.")
metric("Leverage Ratio", "%", [("Leverage ratio", {"FY2021": "53.32%"})], note="FY2021 only: directly disclosed in the Bank's 2021 Pillar 3 disclosure, p.26. No public later-year value found.")
metric("LCR", "%", [("Liquidity Coverage Ratio (simple average of 12 monthly reports)", {"FY2021": "221.13%"})], note="FY2021 only: directly disclosed in the Bank's 2021 Pillar 3 disclosure, p.16. No public later-year value found.")
bw.add_not_disclosed_metric_sheets(["NSFR", "MREL Ratio"], p3_sources(), per_note={m: NOT_DISCLOSED for m in ["NSFR", "MREL Ratio"]})

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flow from operating activities", flow(OPERATING_EUR)),
        ("Net cash flow from investing activities", flow(INVESTING_EUR)),
        ("Cash and cash equivalents at end of year", closing_gbp),
    ],
    cash_flow_unit="£'000 (conv. from EUR)",
    ratios=[("Leverage Ratio", {"FY2021": "53.32%"}), ("LCR", {"FY2021": "221.13%"})],
    note="FY2021 leverage and LCR are the only directly disclosed regulatory liquidity metrics located in the public source set; later years are intentionally blank/not disclosed.",
)

bw.save("/Users/armaan/code/katalysis/banks/PERSIA INTERNATIONAL BANK FINANCIALS.xlsx")
