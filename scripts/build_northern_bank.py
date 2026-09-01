import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR_URLS = {
    "FY2025": "https://danskebank.co.uk/-/media/danske-bank/uk/about-us/corporate-governance/annual-reports/northern-bank-annual-report-accounts-2025.pdf?hash=FAA2D970352C7AB5893C6D09B997681A&rev=a79a533060b745c682e1796ed929cab5",
    "FY2024": "https://danskebank.co.uk/-/media/danske-bank/uk/about-us/corporate-governance/annual-reports/northern-bank-annual-report-og-accounts-2024.pdf?hash=C989E05EAE7993B66B70ADF26AB11BF7&rev=1a1acede77ae425a8222ac3395302b9d",
    "FY2023": "https://danskebank.co.uk/-/media/danske-bank/uk/about-us/corporate-governance/annual-reports/northern-bank-annual-report-og-accounts-2023.pdf?hash=7CEA5F947D848F4BD9C1E97211AFF9CE&rev=4202add3decb471fbed08666ff6e307b",
    "FY2022": "https://danskebank.co.uk/-/media/danske-bank/uk/about-us/corporate-governance/annual-reports/northern-bank-annual-report-og-accounts-2022.pdf?rev=9aa72868afb1433d9e9df8f0959d630f",
    "FY2021": "https://danskebank.co.uk/-/media/danske-bank/uk/about-us/corporate-governance/annual-reports/northern-bank---annual-report-og-accounts-2021.pdf?rev=6bfedd29bb0d488ea30ffce998073674",
}

ENTITY_NOTE = (
    "ENTITY NOTE: Northern Bank Limited (Companies House R0000568, FRN 122261, "
    "LEI 549300KUB2XKWLPMXV81) is the exact legal entity in Banks List 2608.xlsx. "
    "It trades as Danske Bank in Northern Ireland but remains Northern Bank Limited, "
    "an autonomous subsidiary of Danske Bank Group. All figures are the Bank's own "
    "entity-level disclosures, not Danske Bank A/S group figures. The annual reports "
    "state that the Bank monitors capital monthly and quarterly and publishes these "
    "annual capital and liquidity metrics; no separate interim Pillar 3 sheet is "
    "included in this standard annual WF-018 build."
)


def sources(section, pages):
    lines = [f"Sources - Northern Bank Limited entity-level {section}:"]
    for year in YEARS:
        lines.append(f"{year}: Northern Bank Limited Annual Report and Financial Statements {year[2:]}, p.{pages[year]} - {AR_URLS[year]}")
    return "\n".join(lines) + "\n\n" + ENTITY_NOTE


bw = BankWorkbook(
    bank_name="Northern Bank Limited (trading as Danske Bank)",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="1D3557",
)

cash_flow = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 250380, "FY2024": 218164, "FY2023": 185960, "FY2022": 103301, "FY2021": 61269}),
    ("TOTAL", "Net cash flow provided by operating activities", {"FY2025": 295380, "FY2024": 441840, "FY2023": -236114, "FY2022": -29212, "FY2021": 929604}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of investments - hold to collect", {"FY2025": -3171759, "FY2024": -958368, "FY2023": -439077, "FY2022": -1113378, "FY2021": -943850}),
    ("DATA", "Maturity of investments - hold to collect", {"FY2025": 3070000, "FY2024": 430500, "FY2023": 343800, "FY2022": 135000, "FY2021": 150000}),
    ("DATA", "Purchase of investments - hold to collect and sell", {"FY2025": -822418, "FY2024": -99541, "FY2023": -316956, "FY2022": -365859, "FY2021": -301761}),
    ("DATA", "Maturity and sale of investments - hold to collect and sell", {"FY2025": 91071, "FY2024": 290568, "FY2023": 462521, "FY2022": 159491, "FY2021": 255005}),
    ("TOTAL", "Net cash flow provided by investing activities", {"FY2025": -838444, "FY2024": -340002, "FY2023": 47639, "FY2022": -1184140, "FY2021": -841417}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid to shareholders", {"FY2025": -150000, "FY2024": -133000, "FY2023": 0, "FY2022": -40000, "FY2021": -75000}),
    ("DATA", "Payments of interest to AT1 capital holders", {"FY2025": -20083, "FY2024": -22011, "FY2023": -19741, "FY2022": -9377, "FY2021": -4970}),
    ("TOTAL", "Net cash flow provided by financing activities", {"FY2025": -201187, "FY2024": -155922, "FY2023": -20740, "FY2022": 79642, "FY2021": -81038}),
    ("TOTAL", "Net change in cash and cash equivalents", {"FY2025": -493871, "FY2024": 164080, "FY2023": -82713, "FY2022": -1043645, "FY2021": 7149}),
    ("DATA", "Cash and cash equivalents, beginning of year", {"FY2025": 3473906, "FY2024": 3309826, "FY2023": 3392539, "FY2022": 4436184, "FY2021": 2962528}),
    ("TOTAL", "Cash and cash equivalents, end of year", {"FY2025": 2980035, "FY2024": 3473906, "FY2023": 3309826, "FY2022": 3392539, "FY2021": 2969677}),
]

bw.add_cash_flow_sheet(
    title="Northern Bank Limited — Cash Flow Statement",
    subtitle="Entity-level annual cash flows, £'000. Trading name: Danske Bank.",
    rows=cash_flow,
    sources_text=sources("cash flow statement", {"FY2025": 91, "FY2024": 91, "FY2023": 66, "FY2022": 119, "FY2021": 107})
    + "\n\nCASH FLOW PRESENTATION NOTE: The workbook retains the principal reported cash-flow lines and reported annual totals. The reports change the presentation and reconciliation detail over time; the generic verifier may therefore flag subtotal arithmetic where omitted underlying adjustments or comparative restatements are not represented in this compact view. The reported net-change-to-opening/closing cash chain is preserved.",
    first_col_width=62,
    source_height=220,
    unit_suffix=" (£'000)",
)


def metric(name, unit, label, values, page_map, note=None):
    bw.add_metric_sheet(name, unit, [(label, values)], sources(name, page_map), note=note, first_col_width=54, source_height=180)


capital_pages = {"FY2025": 61, "FY2024": 84, "FY2023": 87, "FY2022": 53, "FY2021": 65}
liquidity_pages = {"FY2025": 59, "FY2024": 80, "FY2023": 82, "FY2022": 56, "FY2021": 69}

metric("CET1 Capital", "£'000", "Common Equity Tier 1 capital after deductions", {"FY2025": 655970, "FY2024": 636698, "FY2023": 616879, "FY2022": 504118, "FY2021": 496106}, capital_pages)
metric("CET1 Ratio", "% of RWA", "Common Equity Tier 1 ratio", {"FY2025": "14.9%", "FY2024": "16.1%", "FY2023": "15.6%", "FY2022": "13.6%", "FY2021": "14.4%"}, capital_pages)
metric("Tier 1 Capital", "£'000", "Tier 1 capital", {"FY2025": 835421, "FY2024": 797744, "FY2023": 774046, "FY2022": 666724, "FY2021": 561291}, capital_pages)
metric("Tier 1 Ratio", "% of RWA", "Tier 1 ratio", {"FY2025": "19.0%", "FY2024": "20.2%", "FY2023": "19.6%", "FY2022": "18.0%", "FY2021": "16.3%"}, capital_pages)
metric("Total Capital", "£'000", "Total capital after deductions", {"FY2025": 835421, "FY2024": 797744, "FY2023": 774046, "FY2022": 666724, "FY2021": 648203}, capital_pages)
metric("Total Capital Ratio", "% of RWA", "Total capital ratio", {"FY2025": "19.0%", "FY2024": "20.2%", "FY2023": "19.6%", "FY2022": "18.0%", "FY2021": "18.8%"}, capital_pages)
metric("Total RWAs", "£'000", "Total risk-weighted exposure amount", {"FY2025": 4401004, "FY2024": 3949640, "FY2023": 3947673, "FY2022": 3694531, "FY2021": 3455735}, capital_pages)
metric("Leverage Ratio", "%", "Leverage ratio", {"FY2025": "6.4%", "FY2024": "7.2%", "FY2023": "7.4%", "FY2022": "6.7%", "FY2021": "4.2%"}, capital_pages)
metric("LCR", "%", "Liquidity coverage ratio (pillar 1 + 2)", {"FY2025": "287%", "FY2024": "318%", "FY2023": "309%", "FY2022": "290%", "FY2021": "293%"}, liquidity_pages)
metric("NSFR", "%", "Net Stable Funding Ratio", {"FY2025": "200%", "FY2024": "207%", "FY2023": "203%", "FY2022": "217%", "FY2021": "213%"}, liquidity_pages)
metric("MREL Ratio", "%", "MREL ratio", {"FY2025": "127%", "FY2024": "148%", "FY2023": "148%", "FY2022": "146%", "FY2021": "134%"}, {"FY2025": 60, "FY2024": 83, "FY2023": 86, "FY2022": 55, "FY2021": 65}, note="MREL ratios are the Bank's own annual internal-MREL disclosures. The 2021 figure is the 2021 comparative in the 2022 report and is corroborated by the 2021 report's MREL discussion.")

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flow provided by operating activities", {"FY2025": 295380, "FY2024": 441840, "FY2023": -236114, "FY2022": -29212, "FY2021": 929604}),
        ("Net cash flow provided by investing activities", {"FY2025": -838444, "FY2024": -340002, "FY2023": 47639, "FY2022": -1184140, "FY2021": -841417}),
        ("Net cash flow provided by financing activities", {"FY2025": -201187, "FY2024": -155922, "FY2023": -20740, "FY2022": 79642, "FY2021": -81038}),
        ("Cash and cash equivalents, end of year", {"FY2025": 2980035, "FY2024": 3473906, "FY2023": 3309826, "FY2022": 3392539, "FY2021": 2969677}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "14.9%", "FY2024": "16.1%", "FY2023": "15.6%", "FY2022": "13.6%", "FY2021": "14.4%"}),
        ("Tier 1 Ratio", {"FY2025": "19.0%", "FY2024": "20.2%", "FY2023": "19.6%", "FY2022": "18.0%", "FY2021": "16.3%"}),
        ("Total Capital Ratio", {"FY2025": "19.0%", "FY2024": "20.2%", "FY2023": "19.6%", "FY2022": "18.0%", "FY2021": "18.8%"}),
        ("Leverage Ratio", {"FY2025": "6.4%", "FY2024": "7.2%", "FY2023": "7.4%", "FY2022": "6.7%", "FY2021": "4.2%"}),
    ],
    note="All figures are duplicated from the detail sheets for trend viewing. See each detail sheet for the exact annual-report source citation.\n\n" + ENTITY_NOTE,
)

bw.save("/Users/armaan/code/katalysis/banks/NORTHERN BANK FINANCIALS.xlsx")
