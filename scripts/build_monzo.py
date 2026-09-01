import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {
    "FY2025": "FY2025 (MBHG)",
    "FY2024": "FY2024 (MBHG)*",
    "FY2023": "FY2023 (MBL)",
    "FY2022": "FY2022 (MBL)",
    "FY2021": "FY2021 (MBL)",
}

AR25_URL = "https://monzo.com/annual-report/2025/Monzo%20Bank%20Group%20FY2025%20Annual%20Report.pdf"
AR24_URL = "https://monzo.com/docs/monzo-annual-report-2024.pdf"
AR23_URL = "https://monzo.com/docs/monzo-annual-report-2023.pdf"
AR22_URL = "https://monzo.com/static/docs/monzo-annual-report-2022.pdf"

P3_25_URL = "https://monzo.com/annual-report/2025/monzo-pillar-3-2025.pdf"
P3_24_URL = "https://monzo.com/docs/monzo-pillar-3-2024.pdf"
P3_23_URL = "https://monzo.com/docs/monzo-pillar-3-2023.pdf"
P3_22_URL = "https://monzo.com/static/docs/monzo-pillar-3-2022.pdf"
P3_21_URL = "https://monzo.com/static/docs/monzo-pillar-3-2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: FY2025 and FY2024 (marked MBHG) are Monzo Bank Holding Group Limited, the new parent company "
    "formed April 2023 - a broader consolidation scope than Monzo Bank Limited (MBL), which includes MBL plus "
    "(from FY2025) additional EU/US subsidiaries. FY2021-FY2023 (marked MBL) are Monzo Bank Limited, the entity on "
    "the PRA register. Monzo Bank Limited continued filing its own standalone accounts through FY2025, but that "
    "filing was only available as a scanned, non-text Companies House filing and could not be extracted; MBHG's "
    "figures were used for FY2024/25 instead as the only cleanly-extractable source, per user direction. "
    "Also note: Monzo changed its financial year end from 28 February to 31 March starting FY2024, making FY2024 "
    "a 13-month period (1 March 2023 - 31 March 2024) rather than 12 months - it is not directly run-rate "
    "comparable to the other four years."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Monzo Group (consolidated) cash flow statement, £'000. See entity note above for "
    "MBL vs MBHG scope by year.\n"
    f"FY2025: Monzo Annual Report and Accounts 2025, p.119 (Consolidated statement of cash flows) - {AR25_URL}\n"
    f"FY2024: Monzo Bank Holding Group Limited Annual Report and Group Financial Statements 2024, p.98 "
    f"(Consolidated statement of cash flows, 13-month period ended 31 March 2024) - {AR24_URL}\n"
    f"FY2023: Monzo Bank Limited Annual Report and Accounts 2023, p.100-101 (Statement of cash flows, year ended "
    f"28 February 2023) - {AR23_URL}\n"
    f"FY2022: Monzo Bank Limited Group Annual Report 2022, p.111-112 (Statement of cash flows, year ended "
    f"28 February 2022) - {AR22_URL}\n"
    f"FY2021: Monzo Bank Limited Group Annual Report 2022, p.110-111 (Statement of cash flows, FY2021 restated "
    f"comparative, year ended 28 February 2021) - {AR22_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: Monzo's cash flow statement format changed materially between the MBL years (FY2021-23) "
    "and the MBHG years (FY2024-25) - e.g. separate lease/subordinated-debt/treasury interest lines were combined "
    "into a single 'Net interest' line, and 'Impairment and charge-offs' became its own line. Blank cells indicate "
    "that year's report did not disclose that specific split. Section totals (net cash from operating/investing/"
    "financing, cash and cash equivalents) are consistent and comparable across all 5 years regardless of this."
)

def p3_sources(page_25="20", page_24="29", page_23="30", page_22="32-33", page_21="12-13,20,32-33",
               table_25="Appendix 1: Key metrics - KM1 (Group)", table_24="Appendix 1: Key metrics - KM1 (Group)",
               table_23="Appendix 1: Key metrics - KM1", table_22="Appendix 1: Key metrics - KM1",
               table_21="Table E/F/K and Appendix 4 IFRS9 transitional impact"):
    return (
        "Sources (see entity note on Cash Flow Statement sheet: FY2025/24 = Monzo Bank Holding Group Limited "
        "consolidated (Group); FY2023-21 = Monzo Bank Limited, solo/Group basis as disclosed):\n"
        f"FY2025: Monzo Bank Holding Group Limited Pillar 3 Disclosures 2025, p.{page_25} ({table_25}) - {P3_25_URL}\n"
        f"FY2024: Monzo Bank Holding Group Limited Pillar 3 Disclosures 2024, p.{page_24} ({table_24}) - {P3_24_URL}\n"
        f"FY2023: Monzo Bank Limited Pillar 3 Disclosures 2023, p.{page_23} ({table_23}) - {P3_23_URL}\n"
        f"FY2022: Monzo Bank Limited Pillar 3 Disclosures 2022, p.{page_22} ({table_22}) - {P3_22_URL}\n"
        f"FY2021: Monzo Bank Limited Pillar 3 Disclosures 2021, p.{page_21} ({table_21}) - {P3_21_URL}"
    )

bw = BankWorkbook(bank_name="Monzo", years=YEARS, year_label=YEAR_LABEL, header_color="B8322A")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(Loss) for the year", {"FY2025": 94568, "FY2024": 8709, "FY2023": -116341, "FY2022": -119020, "FY2021": -131077}),
    ("DATA", "Impairment and charge-offs", {"FY2025": 152595, "FY2024": 176868}),
    ("DATA", "Depreciation & impairment expense", {"FY2025": 4623, "FY2024": 7288, "FY2023": 7601, "FY2022": 8311, "FY2021": 9010}),
    ("DATA", "Share-based payments", {"FY2025": 83468, "FY2024": 37469, "FY2023": 29100, "FY2022": 23254, "FY2021": 26547}),
    ("DATA", "Loss on disposals and write-offs", {"FY2023": 510, "FY2022": 495, "FY2021": 274}),
    ("DATA", "(Decrease)/increase in provisions", {"FY2025": 3281, "FY2024": -9830, "FY2023": 8787, "FY2022": -290, "FY2021": 8098}),
    ("DATA", "Loss on warrants", {"FY2023": 23, "FY2022": 502}),
    ("DATA", "Net interest expense on leases", {"FY2023": 1191, "FY2022": 1690, "FY2021": 1450}),
    ("DATA", "Interest expense on subordinated debt", {"FY2023": 2031, "FY2022": 1958}),
    ("DATA", "Interest on collateral", {"FY2023": 403}),
    ("DATA", "Interest on treasury investments", {"FY2023": -29392, "FY2022": -2381, "FY2021": -183}),
    ("DATA", "Net interest (combined, MBHG presentation)", {"FY2025": -68155, "FY2024": -75798}),
    ("DATA", "Taxation", {"FY2025": -34090}),
    ("DATA", "Other non-cash items", {"FY2025": -7494, "FY2024": -1049}),
    ("DATA", "Movement in loans and advances to customers", {"FY2025": -564849, "FY2024": -713349, "FY2023": -418650, "FY2022": -147936, "FY2021": 36766}),
    ("DATA", "Movement in customer deposits", {"FY2025": 5401749, "FY2024": 5251674, "FY2023": 1505297, "FY2022": 1316604, "FY2021": 1731529}),
    ("DATA", "Movement in other assets (excluding RDEC claim)", {"FY2023": -36597, "FY2022": 30628, "FY2021": -20379}),
    ("DATA", "Movement in RDEC claim receivable", {"FY2023": -1698, "FY2022": -186, "FY2021": 2662}),
    ("DATA", "Movement in other assets (combined, MBHG presentation)", {"FY2025": 312246, "FY2024": -299495}),
    ("DATA", "Movement in current tax asset/liability", {"FY2024": -7090}),
    ("DATA", "Net tax paid", {"FY2025": -6019}),
    ("DATA", "Movement in collateral held with third parties", {"FY2025": -1075, "FY2024": -63, "FY2023": -169, "FY2022": -19978, "FY2021": -40672}),
    ("DATA", "Movement in other liabilities (excl. leases/provisions, MBL) / other liabilities (MBHG)", {"FY2025": -454084, "FY2024": 644962, "FY2023": 46717, "FY2022": -77125, "FY2021": 71024}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": 4916764, "FY2024": 5020296, "FY2023": 998813, "FY2022": 1016526, "FY2021": 1695049}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of treasury investments", {"FY2023": -1495059, "FY2022": -1310560, "FY2021": -420977}),
    ("DATA", "Interest received on treasury investments", {"FY2023": 14892, "FY2022": 5048, "FY2021": 1359}),
    ("DATA", "Proceeds from sale and maturity of treasury investments", {"FY2023": 457517, "FY2022": 9000, "FY2021": 142112}),
    ("DATA", "Net movement in treasury investments (combined, MBHG presentation)", {"FY2025": -1676621, "FY2024": -829471}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -213, "FY2024": -1060, "FY2023": -3453, "FY2022": -4383, "FY2021": -8290}),
    ("DATA", "Proceeds on disposal of property, plant and equipment", {"FY2021": 75}),
    ("DATA", "Movement in sublease receivables", {"FY2025": 171, "FY2024": 1010}),
    ("DATA", "Other cash flows from investing activities", {"FY2021": -38}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -1676663, "FY2024": -829521, "FY2023": -1026103, "FY2022": -1300895, "FY2021": -285759}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Net proceeds from issuance of ordinary shares", {"FY2025": 162362, "FY2024": 339440, "FY2023": 300, "FY2022": 436008, "FY2021": 197548}),
    ("DATA", "Payment of interest portion of lease liabilities", {"FY2023": -1988, "FY2022": -385, "FY2021": -388}),
    ("DATA", "Payment of principal portion of lease liabilities", {"FY2023": -3075, "FY2022": -7136, "FY2021": -2654}),
    ("DATA", "Payment of lease liabilities (combined, MBHG presentation)", {"FY2025": -4955, "FY2024": -7008}),
    ("DATA", "Issuance of subordinated debt and warrant liability", {"FY2022": 14812}),
    ("DATA", "Interest paid on subordinated debt liability", {"FY2023": -1801, "FY2022": -1765}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": 157407, "FY2024": 332432, "FY2023": -6564, "FY2022": 441534, "FY2021": 194506}),
    ("DATA", "Effect of exchange rates on cash and cash equivalents", {"FY2025": -45, "FY2024": -149, "FY2023": 556, "FY2022": -150}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 3397463, "FY2024": 4523058, "FY2023": -33298, "FY2022": 157172, "FY2021": 1603646}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 7624300, "FY2024": 3101242, "FY2023": 3134540, "FY2022": 2977368, "FY2021": 1373722}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 11021763, "FY2024": 7624300, "FY2023": 3101242, "FY2022": 3134540, "FY2021": 2977368}),
]

bw.add_cash_flow_sheet(
    title="Monzo — Consolidated (Group) Cash Flow Statement",
    subtitle="£'000 unless stated. FY2025/24 = Monzo Bank Holding Group Limited; FY2023-21 = Monzo Bank Limited. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=62,
    source_height=150,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=46, source_height=150)

metric(
    "CET1 Capital", "£'000, Group/consolidated basis (solo basis for MBL years - Monzo's subsidiaries are excluded from prudential consolidation as below UK CRR Article 19 thresholds)",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1158302, "FY2024": 888274, "FY2023": 532582, "FY2022": 575287, "FY2021": 233604})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "55.92%", "FY2024": "54.94%", "FY2023": "54.40%", "FY2022": "155.1%", "FY2021": "99%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 1158302, "FY2024": 888274, "FY2023": 532582, "FY2022": 575287, "FY2021": 233604})],
    p3_sources(),
    note="Equal to CET1 capital in every year shown - Monzo has not issued any Additional Tier 1 (AT1) instruments.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "55.92%", "FY2024": "54.94%", "FY2023": "54.40%", "FY2022": "155.1%", "FY2021": "99%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 1173723, "FY2024": 903387, "FY2023": 547407, "FY2022": 589880, "FY2021": 233604})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "56.67%", "FY2024": "55.87%", "FY2023": "55.91%", "FY2022": "159.1%", "FY2021": "99%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": 2071182, "FY2024": 1616928, "FY2023": 979042, "FY2022": 370849, "FY2021": 236653})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 7459493, "FY2024": 5550297, "FY2023": 3763096, "FY2021": 796590}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "15.53%", "FY2024": "16.00%", "FY2023": "14.15%", "FY2021": "29.3%"}),
        ("Leverage ratio total exposure measure - 2022 KM1 format, basis not specified in source", {"FY2022": 2238857}),
        ("Leverage ratio (%) - 2022 KM1 format, basis not specified in source", {"FY2022": "25.7%"}),
        ("Total exposure measure including claims on central banks (CRR basis, retired from FY2022)", {"FY2021": 3667694}),
        ("Leverage ratio including claims on central banks (%) (CRR basis, retired from FY2022)", {"FY2021": "6.4%"}),
    ],
    p3_sources(),
    note="Leverage ratio terminology changed across these reports. FY2021 disclosed both a UK ratio (excluding central "
         "bank claims) and a CRR ratio (including them); the CRR ratio was retired PRA-wide from FY2022 onward "
         "('The CRR leverage ratio will no longer apply for UK banks' - FY2022 Pillar 3 report). FY2022's KM1 table "
         "shows a single unlabelled 'Leverage ratio' whose exact basis is not stated in the source document, so it is "
         "kept on its own row rather than assumed to match the 'excluding central banks' series. FY2023 onward "
         "explicitly reintroduced 'excluding claims on central banks' labelling, matching the convention used for "
         "Barclays. Monzo is not currently subject to a binding leverage ratio requirement (below the size threshold).",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets / liquidity buffer (weighted value)", {"FY2025": 13124870, "FY2024": 7651328, "FY2023": 5103316, "FY2022": 4600376, "FY2021": 3212266}),
        ("Total net cash outflows (adjusted value)", {"FY2025": 1133118, "FY2024": 1070436, "FY2023": 671159, "FY2022": 428980, "FY2021": 355375}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "1,178.76%", "FY2024": "724.51%", "FY2023": "760.4%", "FY2022": "1,072.4%", "FY2021": "904%"}),
    ],
    p3_sources(),
    note="FY2021 used a simpler 'Table K: LCR' disclosure (liquidity buffer / net cash outflows) rather than the full "
         "KM1 template used from FY2022 onward; the two are conceptually equivalent to the HQLA/net cash outflow rows "
         "used in later years.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 14543697, "FY2024": 9139028, "FY2023": 6055616, "FY2022": 4703076}),
        ("Total required stable funding", {"FY2025": 1807551, "FY2024": 1345619, "FY2023": 835938, "FY2022": 444598}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "843.98%", "FY2024": "680.81%", "FY2023": "724.4%", "FY2022": "1,057.8%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="NSFR was not disclosed in Monzo's FY2021 Pillar 3 report (no NSFR table or mention present); it first "
         "appears from the FY2022 report onward.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed (ratio)" for y in YEARS})],
    p3_sources(),
    note="Unlike Barclays Bank UK PLC, Monzo IS subject to its own MREL requirement (preferred resolution strategy: "
         "partial transfer) - but no Pillar 3 report in this series discloses a numeric MREL ratio or MREL resources "
         "figure, only the qualitative target. As disclosed: an indicative interim MREL requirement was set from "
         "April 2021 (updated April 2022, then April 2023), with an end-state requirement effective from April 2024/25 "
         "of 1.3x Total Capital Requirement (TCR) - reduced from earlier guidance of 2.0x TCR (per the FY2023 report).",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": 4916764, "FY2024": 5020296, "FY2023": 998813, "FY2022": 1016526, "FY2021": 1695049}),
        ("Net cash from/(used in) investing activities", {"FY2025": -1676663, "FY2024": -829521, "FY2023": -1026103, "FY2022": -1300895, "FY2021": -285759}),
        ("Net cash from/(used in) financing activities", {"FY2025": 157407, "FY2024": 332432, "FY2023": -6564, "FY2022": 441534, "FY2021": 194506}),
        ("Cash and cash equivalents at end of year", {"FY2025": 11021763, "FY2024": 7624300, "FY2023": 3101242, "FY2022": 3134540, "FY2021": 2977368}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "55.92%", "FY2024": "54.94%", "FY2023": "54.40%", "FY2022": "155.1%", "FY2021": "99%"}),
        ("Tier 1 Ratio", {"FY2025": "55.92%", "FY2024": "54.94%", "FY2023": "54.40%", "FY2022": "155.1%", "FY2021": "99%"}),
        ("Total Capital Ratio", {"FY2025": "56.67%", "FY2024": "55.87%", "FY2023": "55.91%", "FY2022": "159.1%", "FY2021": "99%"}),
        ("Leverage Ratio", {"FY2025": "15.53%", "FY2024": "16.00%", "FY2023": "14.15%", "FY2022": "25.7%", "FY2021": "29.3%"}),
        ("LCR", {"FY2025": "1,178.76%", "FY2024": "724.51%", "FY2023": "760.4%", "FY2022": "1,072.4%", "FY2021": "904%"}),
        ("NSFR", {"FY2025": "843.98%", "FY2024": "680.81%", "FY2023": "724.4%", "FY2022": "1,057.8%", "FY2021": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Entity basis switches from Monzo Bank Limited (FY2021-23) to "
         "Monzo Bank Holding Group Limited (FY2024-25); FY2024 is a 13-month transition period from a fiscal-year-end "
         "change. Leverage ratio for FY2022 uses the single unlabelled 'Leverage ratio' KM1 row whose basis is not "
         "stated in the source (see Leverage Ratio sheet).",
)

bw.save("/Users/armaan/code/katalysis/banks/MONZO FINANCIALS.xlsx")
