import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Cash flow statement only exists for FY2021-FY2023 - see CASH_FLOW_EXEMPTION_NOTE
# below. Pillar 3 / capital disclosures (from the Annual Report's own "Capital
# management and liquidity" section - AIB UK does not publish a separate KM1-style
# Pillar 3 document) cover all 5 years.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/NI018800/filing-history"
AR2025_URL = "https://www.aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/annualreport/2025/aib-group-uk-plc-annual-financial-report-2025.pdf"
AR2024_URL = "https://www.aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/annualreport/2024/aib-group-uk-plc-annual-financial-report-2024.pdf"
AR2023_URL = "https://aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/annualreport/2023/aib-group-uk-plc-annual-financial-report-2023.pdf"
AR2022_URL = "https://aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/annualreport/2022/AIB-Group-UK-p.l.c-Annual-Financial-Report-2022.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: 'AIB Group (UK) p.l.c.' (FRN 122088, Companies House NI018800, registered in Northern Ireland) is "
    "a UK subsidiary of Allied Irish Banks, p.l.c. / AIB Group plc (Irish parent, Dublin-registered, no. 594283) - "
    "it is a DIFFERENT legal entity from 'AIB Group plc' itself, which publishes its own much larger, Ireland-wide "
    "consolidated Pillar 3 Disclosures on aib.ie. Early research surfaced AIB Group plc's Irish-group Pillar 3 PDFs "
    "first (they dominate web search results) - these were discarded as the wrong entity. All figures in this "
    "workbook are AIB Group (UK) p.l.c.'s own Annual Financial Report, not the wider AIB Group plc's disclosures. "
    "Confirmed via Companies House filing history and the FRN in Banks List 2608.xlsx."
)

CASH_FLOW_EXEMPTION_NOTE = (
    "CASH FLOW EXEMPTION NOTE: only FY2021-FY2023 have a Statement of Cash Flows. The FY2024 and FY2025 Annual "
    "Financial Reports both state, under '1.2 Basis of preparation': 'the Company has applied the exemptions "
    "available under FRS 101 in respect of the following disclosures: a statement of cash flows and related notes "
    "(IAS 1 Presentation of Financial Statements and IAS 7 Statement of Cash Flows)...' - confirmed directly in "
    "both PDFs' own text (not OCR'd; both are text-native filings). The FY2021-FY2023 reports instead presented "
    "consolidated 'AIB UK Group' financial statements (no FRS 101 exemptions), which is why a full cash flow "
    "statement exists for those three years but not the two most recent ones - the same 'exemption kicks in "
    "partway through the window' pattern seen with Tandem Bank Limited elsewhere in this project, though here it's "
    "a switch from group to solo (FRS 101) reporting that triggers it, not a straightforward late adoption."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are the 'AIB UK Group' (consolidated) column of AIB Group (UK) p.l.c.'s own Statement "
    "of Cash Flows, £m (not the 'AIB UK' solo column shown alongside it, and not AIB Group plc's Irish-group "
    "figures):\n"
    f"FY2023: FY2023 Annual Financial Report, p.73 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: FY2022 Annual Financial Report, p.71 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: sourced from the FY2022 Annual Financial Report's own FY2021 comparative column, p.71 (a standalone "
    f"FY2021 Annual Financial Report PDF could not be fetched - aibgb.co.uk returned HTTP 403 on the only URL "
    f"found for it, and no working aib.ie-hosted equivalent was located) - {AR2022_URL}\n"
    "FY2022 figures were independently cross-checked against their appearance as the FY2023 report's own FY2022 "
    "comparative column and matched exactly.\n\n"
    + ENTITY_NOTE + "\n\n" + CASH_FLOW_EXEMPTION_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - all figures from AIB Group (UK) p.l.c.'s own Annual Financial Report, 'Capital management and "
        "liquidity' section (AIB UK does not publish a separate standalone Pillar 3/KM1 disclosure document - "
        "capital and liquidity metrics are disclosed within the Annual Financial Report itself):\n"
        f"FY2025: FY2025 Annual Financial Report, p.5 - {AR2025_URL}\n"
        f"FY2024: FY2024 Annual Financial Report, p.11 - {AR2024_URL}\n"
        f"FY2023: FY2023 Annual Financial Report, p.17-18 - {AR2023_URL}\n"
        f"FY2022: FY2022 Annual Financial Report, p.19-20 - {AR2022_URL}\n"
        f"FY2021: sourced from the FY2022 Annual Financial Report's own FY2021 comparative figures, p.19-20 (see "
        f"cash flow source note on why a standalone FY2021 report wasn't used) - {AR2022_URL}\n"
        "Figures shown are on a TRANSITIONAL basis (AIB UK's own headline reported ratio each year) - fully loaded "
        "(post-IFRS 9 transitional relief) figures are also disclosed but not used here, consistent with how this "
        "project treats IFRS 9 transitional relief for other banks.\n"
        + (extra + "\n" if extra else "")
        + "\n" + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="AIB Group (UK) p.l.c.", years=YEARS, year_label=YEAR_LABEL, header_color="8C1D40")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before taxation for the year", {"FY2023": 337, "FY2022": 138, "FY2021": 89}),
    ("DATA", "Non-cash items", {"FY2023": -29, "FY2022": 67, "FY2021": 27}),
    ("TOTAL", "Net cash inflow from operating activities before changes in operating assets and liabilities",
     {"FY2023": 308, "FY2022": 205, "FY2021": 116}),
    ("DATA", "Change in loans and advances to banks", {"FY2023": -72, "FY2022": 142, "FY2021": -73}),
    ("DATA", "Change in loans and advances to customers", {"FY2023": 88, "FY2022": 419, "FY2021": 679}),
    ("DATA", "Change in deposits by banks", {"FY2023": -16, "FY2022": -18, "FY2021": -32}),
    ("DATA", "Change in customer accounts", {"FY2023": -1086, "FY2022": -1884, "FY2021": 109}),
    ("DATA", "Change in derivative financial instruments", {"FY2023": 3, "FY2022": -3, "FY2021": 2}),
    ("DATA", "Change in notes in circulation", {"FY2023": -6, "FY2022": -44, "FY2021": -50}),
    ("DATA", "Change in other assets", {"FY2023": 42, "FY2022": -37, "FY2021": 1}),
    ("DATA", "Change in other liabilities", {"FY2023": -1, "FY2022": -64, "FY2021": 1}),
    ("TOTAL", "Net cash (outflow)/inflow from operating assets and liabilities",
     {"FY2023": -1048, "FY2022": -1489, "FY2021": 637}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities before taxation",
     {"FY2023": -740, "FY2022": -1284, "FY2021": 753}),
    ("DATA", "Taxation (paid)/refund", {"FY2023": -54, "FY2022": 2, "FY2021": -3}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities", {"FY2023": -794, "FY2022": -1282, "FY2021": 750}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Additions to property, plant and equipment", {"FY2023": 0, "FY2022": -4, "FY2021": -7}),
    ("DATA", "Proceeds from disposals of property, plant and equipment", {"FY2023": 1, "FY2022": 1, "FY2021": 0}),
    ("DATA", "Additions to intangible assets", {"FY2023": -4, "FY2022": -2, "FY2021": -4}),
    ("TOTAL", "Net cash outflow from investing activities", {"FY2023": -3, "FY2022": -5, "FY2021": -11}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Buyback of ordinary shares", {"FY2023": -250}),
    ("DATA", "Proceeds on issues of debt securities", {"FY2023": 140}),
    ("DATA", "Net proceeds on issue of additional Tier 1 securities", {"FY2023": 110}),
    ("DATA", "Repayment of secondary non-preferential debt", {"FY2022": 0, "FY2021": -45}),
    ("DATA", "Repayment of lease liabilities", {"FY2023": -3, "FY2022": -9, "FY2021": -3}),
    ("TOTAL", "Net cash outflow from financing activities", {"FY2023": -3, "FY2022": -9, "FY2021": -48}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2023": -800, "FY2022": -1296, "FY2021": 691}),
    ("DATA", "Opening cash and cash equivalents", {"FY2023": 4057, "FY2022": 5353, "FY2021": 4662}),
    ("TOTAL", "Closing cash and cash equivalents", {"FY2023": 3257, "FY2022": 4057, "FY2021": 5353}),
]

bw.add_cash_flow_sheet(
    title="AIB Group (UK) p.l.c. — Statement of Cash Flows",
    subtitle="AIB UK Group (consolidated) basis, £m. FY2024-FY2025 blank - see source note at bottom (FRS 101 cash-flow exemption).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else "", rows_data, sources_text,
                         note=note, first_col_width=52, source_height=190)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital, transitional", {"FY2025": 1614, "FY2024": 1533, "FY2023": 1407, "FY2022": 1531, "FY2021": 1508})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio, transitional", {"FY2025": "26.8%", "FY2024": "27.7%", "FY2023": "21.44%", "FY2022": "24.11%", "FY2021": "22.81%"})],
    p3_sources("FY2021's CET1 ratio (22.81%) is CALCULATED (CET1 ÷ RWA) - the FY2022 report only states the ratio "
               "increased from an unstated FY2021 base, it never gives the FY2021 % directly."),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 1724, "FY2024": 1643, "FY2023": 1517, "FY2022": 1531, "FY2021": 1508})],
    p3_sources(),
    note="Tier 1 Capital = CET1 Capital for FY2021-FY2022 (no Additional Tier 1 instruments outstanding yet). AIB "
         "UK issued £110m of AT1 as part of a November 2023 capital restructure; Tier 1 Capital from FY2023 onward "
         "is CALCULATED as CET1 + AT1 (£110m every year FY2023-FY2025) - AIB UK's own disclosures give CET1 and "
         "Total Capital explicitly but never break out a separate 'Tier 1' capital or ratio line.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio (calculated: Tier 1 Capital ÷ RWA)", {"FY2025": "28.64%", "FY2024": "29.66%", "FY2023": "23.11%", "FY2022": "24.11%", "FY2021": "22.81%"})],
    p3_sources("Entirely CALCULATED (Tier 1 Capital ÷ Total RWA) - AIB UK does not disclose a Tier 1 ratio as a "
               "distinct line anywhere in its Annual Financial Reports."),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 1865, "FY2024": 1783, "FY2023": 1657, "FY2022": 1531, "FY2021": 1508})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio, transitional", {"FY2025": "31.0%", "FY2024": "32.3%", "FY2023": "25.24%", "FY2022": "24.11%", "FY2021": "22.81%"})],
    p3_sources("FY2021-FY2022 Total Capital Ratio = CET1 Ratio (no AT1/Tier 2 outstanding, so Total Capital = CET1 "
               "those two years)."),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets, transitional", {"FY2025": 6020, "FY2024": 5540, "FY2023": 6564, "FY2022": 6352, "FY2021": 6611})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2021": "11.26%"})],
    p3_sources(),
    note="Only FY2021 is disclosed - a one-off figure mentioned in the FY2022 Annual Financial Report's "
         "'Regulatory changes' note ('...significantly increased the Bank's leverage ratio from 11.26% in "
         "December 2021 to 20.22% in March 2022' following a PRA leverage-framework methodology change, PRA "
         "Policy Statement 21/21). No FY2022-FY2025 year-end leverage ratio figure appears anywhere in any of the "
         "five Annual Financial Reports - AIB UK's 'Capital management and liquidity' section covers CET1/Total "
         "Capital/RWA/LCR/NSFR every year but never a leverage ratio outside that single FY2021 mention.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {"FY2025": "216%", "FY2024": "282%", "FY2023": "216%", "FY2022": "176%", "FY2021": "169%"})],
    p3_sources(),
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {"FY2025": "157%", "FY2024": "172%", "FY2023": "139%", "FY2022": "145%", "FY2021": "156%"})],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "MREL is not mentioned anywhere in any of AIB Group (UK) p.l.c.'s five Annual Financial "
                      "Reports (FY2021-FY2025) - searched directly, no hits. AIB UK's own capital section discusses "
                      "only the CRR minimum capital requirement (8% Total Capital / 4.5% Tier 1) plus its "
                      "PRA-set Pillar 1 and Pillar 2a add-on, with no separate resolution/MREL requirement "
                      "disclosed - consistent with AIB UK not being its own resolution entity under the Bank of "
                      "England's MREL framework (resolution planning likely sits at the wider AIB Group level).",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2023": -794, "FY2022": -1282, "FY2021": 750}),
        ("Net cash from/(used in) investing activities", {"FY2023": -3, "FY2022": -5, "FY2021": -11}),
        ("Net cash from/(used in) financing activities", {"FY2023": -3, "FY2022": -9, "FY2021": -48}),
        ("Closing cash and cash equivalents", {"FY2023": 3257, "FY2022": 4057, "FY2021": 5353}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "26.8%", "FY2024": "27.7%", "FY2023": "21.44%", "FY2022": "24.11%", "FY2021": "22.81%"}),
        ("Tier 1 Ratio", {"FY2025": "28.64%", "FY2024": "29.66%", "FY2023": "23.11%", "FY2022": "24.11%", "FY2021": "22.81%"}),
        ("Total Capital Ratio", {"FY2025": "31.0%", "FY2024": "32.3%", "FY2023": "25.24%", "FY2022": "24.11%", "FY2021": "22.81%"}),
        ("Leverage Ratio", {"FY2021": "11.26%"}),
        ("LCR", {"FY2025": "216%", "FY2024": "282%", "FY2023": "216%", "FY2022": "176%", "FY2021": "169%"}),
        ("NSFR", {"FY2025": "157%", "FY2024": "172%", "FY2023": "139%", "FY2022": "145%", "FY2021": "156%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Cash flow is blank for FY2024-FY2025 (FRS 101 exemption took "
         "effect from FY2024 - see Cash Flow Statement sheet note); Leverage Ratio is populated for FY2021 only "
         "(never disclosed again in later years). All figures are AIB Group (UK) p.l.c. itself, NOT AIB Group plc "
         "(the Irish parent) - see entity note on every sheet.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/AIB GROUP UK FINANCIALS.xlsx")
