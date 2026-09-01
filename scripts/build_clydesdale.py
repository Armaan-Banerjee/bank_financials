import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Fiscal year-end changed from 30 September to 31 March via an 18-month PRA-
# approved transition period (1 Oct 2023 - 31 Mar 2025); there is no separate
# "FY2024". See FY2025_TRANSITION_NOTE below.
YEARS = ["FY2026", "FY2025", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {
    "FY2026": "FY2026",
    "FY2025": "FY2025 (18mo)",
    "FY2023": "FY2023",
    "FY2022": "FY2022",
    "FY2021": "FY2021",
}

AR2026_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2026-signed.pdf"
AR2025_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2025-signed.pdf"
AR2023_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cbplc-2023-ar-cfs.pdf"
AR2022_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cbplc-2022-ar-cfs.pdf"
AR2021_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2021.pdf"

P3_2026_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-2026-pillar-3-report.pdf"
P3_2025_URL = "https://www.virginmoneyukplc.com/downloads/pdf/vmukplc-2025-pillar-3-report.pdf"
P3_2023_URL = "https://www.virginmoneyukplc.com/downloads/pdf/vmukplc-2023-pillar-3-report.pdf"
P3_2022_URL = "https://www.virginmoneyukplc.com/downloads/pdf/vmukplc-2022-pillar-3-report.pdf"
P3_2021_URL = "https://www.virginmoneyukplc.com/downloads/pdf/vm-pillar-3-2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Clydesdale Bank PLC (company number SC001111) is the PRA-authorised entity (FRN 121873) and the "
    "main operating banking subsidiary of Virgin Money UK PLC. On 28 July 2026 the company re-registered from a "
    "public limited company to a private limited company and is now named 'Clydesdale Bank Limited' - this workbook "
    "uses 'Clydesdale Bank PLC' throughout since that was its name for the entirety of the period covered (FY2021-"
    "FY2026). The fiscal year-end changed from 30 September to 31 March via a PRA-approved 18-month transition "
    "period (1 October 2023 - 31 March 2025, shown as 'FY2025 (18mo)' below); there is no separate FY2024 - that "
    "period is entirely contained within the 18-month column. Cash flow and Pillar 3 figures are on the 'CB Group "
    "Consolidated' / 'CB Solo-Consolidated Group' basis (Clydesdale Bank PLC's own consolidation perimeter) rather "
    "than the wider Virgin Money UK PLC group, consistent with the ring-fenced-entity basis used elsewhere in this "
    "workbook series; most annual Pillar 3 reports through FY2025 are published under the 'Virgin Money UK PLC' "
    "title but contain a dedicated CB Group Consolidated appendix, which is what is cited here."
)

NATIONWIDE_NOTE = (
    "NATIONWIDE ACQUISITION NOTE: Nationwide Building Society completed its acquisition of Virgin Money UK PLC "
    "(Clydesdale Bank PLC's parent) on 1 October 2024. On 14 November 2025 the Bank's Directors publicly announced "
    "a decision to move substantially all of the Bank's business to Nationwide by way of a Part VII banking business "
    "transfer; the High Court approved the transfer on 23 February 2026 and on 2 April 2026 the majority of the "
    "Bank's assets and liabilities transferred to Nationwide. At 31 March 2026 the transferred assets/liabilities "
    "were classified as a disposal group 'held for distribution' and the related financial performance presented as "
    f"a discontinued operation (FY2026 Annual Report and Accounts, p.60) - {AR2026_URL}."
)

FY2026_CASH_FLOW_GAP_NOTE = (
    "FY2026 cash flow is blank: the FY2026 Annual Report and Accounts moved to the FRS 101 Reduced Disclosure "
    f"Framework and explicitly took the IAS 7 'Statement of Cash Flows' disclosure exemption (p.60) - {AR2026_URL} "
    "- available to it as a qualifying subsidiary whose ultimate parent (Nationwide Building Society) publishes "
    "consolidated financial statements. No cash flow statement of any kind appears in the FY2026 accounts. See the "
    "Nationwide acquisition note above for context (the exemption coincides with the Part VII transfer of "
    "substantially all of the Bank's business)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Clydesdale Bank PLC (CB) Group consolidated cash flow statement, £m:\n"
    f"FY2025 (18mo, 1 Oct 2023 - 31 Mar 2025): Clydesdale Bank PLC 2025 Annual Report and Accounts, p.113 "
    f"(Statement of cash flows) - {AR2025_URL}\n"
    f"FY2023: Clydesdale Bank PLC 2023 Annual report & consolidated financial statements, p.116 (Statement of cash "
    f"flows) - {AR2023_URL}\n"
    f"FY2022: Clydesdale Bank PLC 2022 Annual Report and consolidated financial statements, p.119 (Statement of "
    f"cash flows) - {AR2022_URL}\n"
    f"FY2021: Clydesdale Bank PLC 2021 Annual report & consolidated financial statements, p.119 (Statement of cash "
    f"flows) - {AR2021_URL}\n"
    "Note: the FY2025 (18mo) statement's comparative period (FY2023) is presented on a basis restated to align "
    "Group accounting policies/presentation with Nationwide, and combines some line items (e.g. interest received/"
    "paid, changes in operating assets and liabilities) that FY2021-FY2023 report split out individually; FY2023's "
    "own column above uses that year's own as-originally-reported presentation, not the restated comparative. Blank "
    "cells indicate that year's report did not disclose that specific split; where a coarser combined figure was "
    "reported instead, it appears on its own row. Section totals and cash/cash equivalents figures are consistent "
    "and comparable across all 4 populated years.\n\n"
    + ENTITY_NOTE + "\n\n" + NATIONWIDE_NOTE + "\n\n" + FY2026_CASH_FLOW_GAP_NOTE
)


def p3_sources(source_label_25="21.1.2 UK KM1 - Key metrics (Appendix 1: CB Solo-Consolidated Group)", page_25="140",
               source_label_23="21.1.2 UK KM1 - Key metrics (Appendix 1: CB Group Consolidated)", page_23="123",
               source_label_22="21.1.2 UK KM1 - Key metrics (Appendix 1: CB Group Consolidated)", page_22="103",
               source_label_21="Table 57/59 (Appendix 1: Disclosures for CB Group consolidated)", page_21="77, 79"):
    return (
        "Sources - Clydesdale Bank PLC (CB) Group/Solo-Consolidated basis:\n"
        f"FY2026: Clydesdale Bank PLC 2026 Pillar 3 Report, p.5-6 (2.1 UK KM1 - Key metrics) - {P3_2026_URL}\n"
        f"FY2025 (18mo): Virgin Money UK PLC 2025 Pillar 3 Report, p.{page_25} ({source_label_25}) - {P3_2025_URL}\n"
        f"FY2023: Virgin Money UK PLC 2023 Pillar 3 Report, p.{page_23} ({source_label_23}) - {P3_2023_URL}\n"
        f"FY2022: Virgin Money UK PLC 2022 Pillar 3 Report, p.{page_22} ({source_label_22}) - {P3_2022_URL}\n"
        f"FY2021: Virgin Money UK PLC 2021 Pillar 3 Report, p.{page_21} ({source_label_21}) - {P3_2021_URL}"
    )


bw = BankWorkbook(bank_name="Clydesdale Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="6D0E23")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit on ordinary activities before tax", {"FY2025": 186, "FY2023": 344, "FY2022": 590, "FY2021": 416}),
    ("DATA", "Non-cash or non-operating items included in profit before tax", {"FY2025": 368, "FY2023": -1203, "FY2022": -1306, "FY2021": -1221}),
    ("DATA", "Changes in operating assets", {"FY2023": -551, "FY2022": 1213, "FY2021": 819}),
    ("DATA", "Changes in operating liabilities", {"FY2023": 284, "FY2022": -240, "FY2021": -1026}),
    ("DATA", "Changes in operating assets and liabilities (combined, as reported)", {"FY2025": -1738}),
    ("DATA", "Payments for short-term and low value leases", {"FY2023": -3, "FY2022": -2, "FY2021": -1}),
    ("DATA", "Interest received (operating)", {"FY2023": 3300, "FY2022": 2112, "FY2021": 2088}),
    ("DATA", "Interest paid (operating)", {"FY2023": -1173, "FY2022": -378, "FY2021": -461}),
    ("DATA", "Tax paid including group relief", {"FY2025": -37, "FY2023": -50, "FY2022": -59, "FY2021": -32}),
    ("TOTAL", "Net cash provided by/(used in) operating activities", {"FY2025": -1221, "FY2023": 948, "FY2022": 1930, "FY2021": 582}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Interest received (investing)", {"FY2023": 232, "FY2022": 47, "FY2021": 19}),
    ("DATA", "Proceeds from maturity of financial instruments at FVOCI", {"FY2022": 479, "FY2021": 1079}),
    ("DATA", "Proceeds from sale of financial assets at FVOCI", {"FY2022": 194}),
    ("DATA", "Proceeds from sale and maturity of financial instruments at FVOCI (combined, as reported)", {"FY2025": 2266, "FY2023": 1868}),
    ("DATA", "Purchase of financial assets at FVOCI", {"FY2025": -2198, "FY2023": -2950, "FY2022": -2019, "FY2021": -521}),
    ("DATA", "Purchase of shares in UTM previously held in Virgin Money Holdings (UK) Limited", {"FY2022": -4, "FY2021": -12}),
    ("DATA", "Acquisition of controlled entities", {"FY2025": -20}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 3, "FY2023": 1, "FY2022": 1, "FY2021": 6}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -15, "FY2023": -9, "FY2022": -13, "FY2021": -26}),
    ("DATA", "Purchase and development of intangible assets", {"FY2025": -6, "FY2023": -11, "FY2022": -53, "FY2021": -80}),
    ("TOTAL", "Net cash provided by/(used in) investing activities", {"FY2025": 30, "FY2023": -869, "FY2022": -1368, "FY2021": 465}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Interest paid (financing)", {"FY2023": -743, "FY2022": -246, "FY2021": -158}),
    ("DATA", "Repayment of principal portion of lease liabilities", {"FY2025": -40, "FY2023": -24, "FY2022": -26, "FY2021": -28}),
    ("DATA", "Redemption and principal repayment on RMBS and covered bonds", {"FY2023": -1012, "FY2022": -1264, "FY2021": -1543}),
    ("DATA", "Issuance of RMBS and covered bonds", {"FY2023": 1826, "FY2022": 2480}),
    ("DATA", "Issuance of AT1 securities", {"FY2025": 347, "FY2022": 347}),
    ("DATA", "Redemption of AT1 securities", {"FY2025": -250, "FY2023": -72, "FY2022": -384}),
    ("DATA", "Redemption and principal repayment on medium-term notes", {"FY2021": 0}),
    ("DATA", "Amounts drawn down under the TFSME", {"FY2022": 2550, "FY2021": 3350}),
    ("DATA", "Amounts repaid under the TFSME", {"FY2023": -1000}),
    ("DATA", "Amounts repaid under the TFS", {"FY2022": -1244, "FY2021": -2864}),
    ("DATA", "Net (increase)/decrease in amounts due from related entities", {"FY2025": -55, "FY2023": 7, "FY2022": 1, "FY2021": 9}),
    ("DATA", "Net increase/(decrease) in amounts due to related entities", {"FY2025": 373, "FY2023": 297, "FY2022": 9, "FY2021": 705}),
    ("DATA", "AT1 distributions", {"FY2025": -66, "FY2023": -54, "FY2022": -60, "FY2021": -59}),
    ("DATA", "Ordinary dividends paid", {"FY2025": -211, "FY2023": -248, "FY2022": -367, "FY2021": -20}),
    ("DATA", "Proceeds from ordinary shares issued", {"FY2025": 800}),
    ("TOTAL", "Net cash provided by/(used in) financing activities", {"FY2025": 898, "FY2023": -1023, "FY2022": 1796, "FY2021": -608}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -293, "FY2023": -944, "FY2022": 2358, "FY2021": 439}),
    ("DATA", "Cash and cash equivalents at the beginning of the period/year", {"FY2025": 10589, "FY2023": 12611, "FY2022": 10253, "FY2021": 9814}),
    ("TOTAL", "Cash and cash equivalents at the end of the period/year", {"FY2025": 10296, "FY2023": 11667, "FY2022": 12611, "FY2021": 10253}),
]

bw.add_cash_flow_sheet(
    title="Clydesdale Bank PLC — Consolidated Cash Flow Statement",
    subtitle="Clydesdale Bank (CB) Group (consolidated basis), £m unless stated. FY2026 blank - see source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"CB consolidated basis, {unit}" if unit else "CB consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=110)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2026": 4248, "FY2025": 3900, "FY2023": 3685, "FY2022": 3606, "FY2021": 3603})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2026": "14.3%", "FY2025": "14.2%", "FY2023": "14.6%", "FY2022": "14.9%", "FY2021": "14.9%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2026": 4946, "FY2025": 4593, "FY2023": 4279, "FY2022": 4268, "FY2021": 4275})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2026": "16.6%", "FY2025": "16.7%", "FY2023": "17.0%", "FY2022": "17.7%", "FY2021": "17.7%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2026": 5747, "FY2025": 5347, "FY2023": 5301, "FY2022": 5288, "FY2021": 5294})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2026": "19.3%", "FY2025": "19.4%", "FY2023": "21.1%", "FY2022": "21.9%", "FY2021": "21.9%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2026": 29742, "FY2025": 27555, "FY2023": 25172, "FY2022": 24128, "FY2021": 24194})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2026": 78792, "FY2025": 83120, "FY2023": 86545, "FY2022": 83758, "FY2021": 84293}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2026": "6.3%", "FY2025": "5.5%", "FY2023": "4.9%", "FY2022": "5.1%", "FY2021": "5.1%"}),
        ("Leverage ratio including claims on central banks (%)", {"FY2026": "5.3%", "FY2025": "5.0%", "FY2023": "4.5%", "FY2022": "4.5%"}),
    ],
    p3_sources(),
    note="FY2021's Pillar 3 report disclosed a single 'Leverage ratio' (5.1%) without an excluding/including claims "
         "on central banks split (that distinction was introduced in later reports), shown here on the 'excluding' "
         "row for comparability. FY2022's exposure measure (83,758) reflects a PS22/21-driven restatement to "
         "exclude Bounce Back Loan Scheme (BBLS) balances; FY2021's figure (84,293) is as originally reported and "
         "was not restated on the same basis, so the FY2021-to-FY2022 leverage exposure movement is not fully "
         "like-for-like.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2026": 16246, "FY2025": 14868, "FY2023": 13798, "FY2022": 11503}),
        ("Total net cash outflows, adjusted value", {"FY2026": 9912, "FY2025": 9414, "FY2023": 9424, "FY2022": 8222}),
        ("Liquidity Coverage Ratio (%)", {"FY2026": "164%", "FY2025": "158%", "FY2023": "146%", "FY2022": "140%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="LCR is a 12-month simple average of month-end observations. Not disclosed for FY2021 at the CB Group "
         "Consolidated level in the 2021 Pillar 3 report's dedicated CB appendix (only narrative/glossary mentions "
         "of LCR appear elsewhere in that report).",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2026": 78219, "FY2025": 77427, "FY2023": 79295}),
        ("Total required stable funding", {"FY2026": 54560, "FY2025": 54375, "FY2023": 58450}),
        ("NSFR ratio (%)", {"FY2026": "143%", "FY2025": "142%", "FY2023": "136%", "FY2022": "Not disclosed", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="Per PRA guidance, NSFR disclosures were not required until reporting reference dates after 1 January "
         "2023 (per the FY2023 Pillar 3 report), so no FY2022 or FY2021 figures exist.",
)

metric(
    "MREL Ratio", "£m / %",
    [
        ("Total capital resources", {"FY2026": 5747, "FY2025": 5347, "FY2023": 5301, "FY2022": 5288}),
        ("Eligible senior unsecured securities", {"FY2026": 3520, "FY2025": 3004, "FY2023": 2707, "FY2022": 2423}),
        ("Total MREL resources", {"FY2026": 9267, "FY2025": 8351, "FY2023": 8008, "FY2022": 7711}),
        ("MREL resources (% of total risk-weighted assets)", {"FY2026": "31.2%", "FY2025": "30.3%", "FY2023": "31.8%", "FY2022": "32.0%", "FY2021": "Not disclosed"}),
        ("MREL resources (% of UK leverage exposure measure)", {"FY2026": "11.8%", "FY2025": "10.0%", "FY2023": "9.3%", "FY2022": "9.2%"}),
    ],
    p3_sources(),
    note="'Eligible senior unsecured securities' were issued by Clydesdale Bank PLC through FY2023, but by Virgin "
         "Money UK PLC from the FY2025 (18mo) report onward - shown as reported each year, not adjusted for this "
         "change. FY2021's Pillar 3 report contains only qualitative MREL narrative (no numeric MREL disclosure of "
         "any kind), consistent with the UK KM2 MREL template not yet being in use for CB Group Consolidated that "
         "year.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -1221, "FY2023": 948, "FY2022": 1930, "FY2021": 582}),
        ("Net cash from/(used in) investing activities", {"FY2025": 30, "FY2023": -869, "FY2022": -1368, "FY2021": 465}),
        ("Net cash from/(used in) financing activities", {"FY2025": 898, "FY2023": -1023, "FY2022": 1796, "FY2021": -608}),
        ("Cash and cash equivalents at end of period/year", {"FY2025": 10296, "FY2023": 11667, "FY2022": 12611, "FY2021": 10253}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2026": "14.3%", "FY2025": "14.2%", "FY2023": "14.6%", "FY2022": "14.9%", "FY2021": "14.9%"}),
        ("Tier 1 Ratio", {"FY2026": "16.6%", "FY2025": "16.7%", "FY2023": "17.0%", "FY2022": "17.7%", "FY2021": "17.7%"}),
        ("Total Capital Ratio", {"FY2026": "19.3%", "FY2025": "19.4%", "FY2023": "21.1%", "FY2022": "21.9%", "FY2021": "21.9%"}),
        ("Leverage Ratio", {"FY2026": "6.3%", "FY2025": "5.5%", "FY2023": "4.9%", "FY2022": "5.1%", "FY2021": "5.1%"}),
        ("LCR", {"FY2026": "164%", "FY2025": "158%", "FY2023": "146%", "FY2022": "140%"}),
        ("NSFR", {"FY2026": "143%", "FY2025": "142%", "FY2023": "136%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. FY2026 cash flow is blank because the FY2026 Annual Report "
         "took the FRS 101/IAS 7 cash-flow-statement exemption (see Cash Flow Statement sheet note) following the "
         "Part VII transfer of substantially all of the Bank's business to Nationwide on 2 April 2026; Pillar 3 "
         "disclosures were unaffected and continue for FY2026.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CLYDESDALE FINANCIALS.xlsx")
