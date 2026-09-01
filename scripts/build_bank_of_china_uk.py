import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR2021_URL = "https://pic.bankofchina.com/bocappd/uk/202303/P020230331590070165221.pdf"
AR2022_URL = "https://pic.bankofchina.com/bocappd/uk/202403/P020240315379765805794.pdf"
AR2023_URL = "https://pic.bankofchina.com/bocappd/uk/202405/P020240508355110735895.pdf"
AR2024_URL = "https://pic.bankofchina.com/bocappd/uk/202507/P020250718380377744220.pdf"
AR2025_URL = "https://pic.bankofchina.com/bocappd/uk/202605/P020260506389809417235.pdf"

P3_2021_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202303/P020230315381669571541.pdf"
P3_2022_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202310/P020231026347190320350.pdf"
P3_2023_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202410/P020241008402737321677.pdf"
P3_2024_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202507/P020250718380587744231.pdf"
P3_2025_URL = "https://pic.bankofchina.com/bocappd/uk/202607/P020260716391457618567.pdf"

ENTITY_NOTE = (
    "Entity note: Bank of China (UK) Limited (company 06193060, FRN 467410) is a wholly-owned UK subsidiary of "
    "Bank of China Limited (state-owned). It does not take the FRS 101/102 cash-flow-statement exemption - a full "
    "Statement of Cash Flows is published every year. All figures are the Bank's own solo entity basis throughout."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank of China (UK) Limited's own Statement of Cash Flows, £'000, as published on "
    "the Bank's own site (each year's own originally-published report, not a later restated comparative):\n"
    f"FY2025: Annual Report and Financial Statements for the year ended 31 December 2025, p.51-52 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements for the year ended 31 December 2024, p.52-53 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 December 2023, p.52-53 - {AR2023_URL}\n"
    f"FY2022: Financial Statements for the year ended 31 December 2022, p.40 - {AR2022_URL}\n"
    f"FY2021: Financial Statements for the year ended 31 December 2021, p.37 - {AR2021_URL}\n"
    "Restatement note: FY2023's own report marks its FY2022 comparative column 'Restated' and shows different "
    "figures (e.g. operating activities -£17,138k, closing cash £687,013k) to FY2022's own originally-published "
    "report (operating activities +£22,570k, closing cash £657,656k). This workbook uses each year's own "
    "originally-published figures as the primary column (project convention), which creates a genuine, disclosed "
    "£29,357k gap between FY2022's own closing balance and FY2023's own opening balance - flagged here rather "
    "than silently blended or force-reconciled. The underlying cause of the restatement is not explained in "
    "either source.\n"
    "Presentation notes: FY2021-FY2023 include small 'Exchange rate movements on plant and equipment/on equity' "
    "lines not present in FY2024/FY2025's statements. FY2022 alone shows a one-off Tier 2-to-AT1 capital "
    "replacement (subordinated debt of £60,000k repaid, an equal Additional Tier 1 instrument issued, both under "
    "financing activities). FY2025's own report split 'Change in financial assets at amortised cost/fair value' "
    "into two lines (the government-bond component shown separately) and separated lease-liability cash flows "
    "into principal and interest portions for the first time - both are FY2025-only presentational changes with "
    "no net impact on any section total. FY2025's own supplementary 'cash and cash equivalents comprise' note "
    "totals £1,073,245k (£157k less than the statement's own £1,073,402k closing balance), a gap matching the "
    "same page's separately-shown expected-credit-loss allowance of £157k - the statement's own total is used as "
    "the primary closing-balance figure here. FY2022's own report does not break out a separate 'Interest paid "
    "on Additional Tier 1 instrument' line (the AT1 instrument was only issued in June 2022); FY2023's restated "
    "FY2022 comparative does show one (£1,759k), consistent with the broader FY2022 restatement noted above - "
    "not included here since it wasn't part of FY2022's own originally-published statement.\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Bank of China (UK) Limited Pillar 3 disclosures (UK KM1 Key Metrics template from FY2022 "
        "onward; FY2021's own document is narrative/ratio-only and predates the KM1 template), £'000 unless "
        "stated:\n"
        f"FY2025 & FY2024 comparative: Pillar 3 Disclosure 31 December 2025, p.15 (UK KM1) - {P3_2025_URL}\n"
        f"FY2024 (own year) & FY2023 comparative: Pillar 3 Disclosures 31 December 2024, p.16 (UK KM1) - {P3_2024_URL}\n"
        f"FY2023 (own year) & FY2022 comparative: Pillar 3 disclosures 31 December 2023, p.14 (UK KM1) - {P3_2023_URL}\n"
        f"FY2022 (own year) & FY2021 comparative: Pillar 3 Disclosures 2022, p.14 (UK KM1) - {P3_2022_URL}\n"
        f"FY2021 (own year, narrative/ratio-only - no KM1 template yet): Pillar 3 Disclosures 2021, p.12-14, 24 - {P3_2021_URL}\n"
        "FY2021 note: the Bank's own FY2021 Pillar 3 document states CET1/Total Capital as rounded £275m/£335m "
        "and gives no £-breakdown for leverage exposure, LCR HQLA/outflow, or NSFR (NSFR was not yet a formal "
        "disclosure). The precise FY2021 figures used on those sheets (CET1/Tier 1 £275,164k, Total Capital "
        "£335,164k, leverage exposure £2,431,869k, LCR HQLA £527,697k/outflow £294,774k, NSFR £1,438,026k/"
        "£950,742k) are taken from the FY2022 Pillar 3 document's FY2021 comparative column instead, since it is "
        "the more complete disclosure - all overlapping ratios (CET1 24.6%, Total Capital 29.9%, Leverage 11.3%, "
        "LCR 179.0%) match the FY2021 document's own narrative figures exactly.\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Bank of China (UK) Limited", years=YEARS, header_color="B22222")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before income tax", {"FY2025": 90368, "FY2024": 107644, "FY2023": 138195, "FY2022": 91147, "FY2021": 39266}),
    ("DATA", "Depreciation and amortisation of plant and equipment and intangible assets", {"FY2025": 2031, "FY2024": 1644, "FY2023": 1624, "FY2022": 1733, "FY2021": 2039}),
    ("DATA", "Net (credit)/loss for expected credit losses", {"FY2025": -297, "FY2024": -3958, "FY2023": -11237, "FY2022": -11526, "FY2021": 23665}),
    ("DATA", "Exchange rate movements on plant and equipment", {"FY2021": -1}),
    ("DATA", "Exchange rate movements on equity", {"FY2023": -1, "FY2022": 12, "FY2021": 135}),
    ("DATA", "Net fair value (gain)/loss on financial instruments", {"FY2025": -1895, "FY2024": -1310, "FY2023": -7446, "FY2022": 10358, "FY2021": 2656}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Change in derivative financial instruments assets", {"FY2025": 2163, "FY2024": 839, "FY2023": 2196, "FY2022": -7691, "FY2021": -8}),
    ("DATA", "Change in loans and advances to banks", {"FY2022": 39708, "FY2021": 41381}),
    ("DATA", "Change in loans and advances to customers", {"FY2025": 130992, "FY2024": 53197, "FY2023": 142977, "FY2022": 83721, "FY2021": -79736}),
    ("DATA", "Change in financial assets at amortised cost/fair value", {"FY2025": -39251, "FY2024": 16787, "FY2023": 20515, "FY2022": -6213, "FY2021": 10167}),
    ("DATA", "Change in financial assets at amortised cost - Government bonds", {"FY2025": 2147}),
    ("DATA", "Change in other assets", {"FY2025": -18315, "FY2024": -7665, "FY2023": 221384, "FY2022": -264099, "FY2021": -9099}),
    ("DATA", "Change in derivative financial instruments liabilities", {"FY2025": 287, "FY2024": 1, "FY2023": -10, "FY2022": -5267, "FY2021": -3484}),
    ("DATA", "Change in deposits from banks", {"FY2025": 18705, "FY2024": 123666, "FY2023": -169797, "FY2022": 143133, "FY2021": 176876}),
    ("DATA", "Change in deposits from customers", {"FY2025": -50713, "FY2024": 132461, "FY2023": -68081, "FY2022": -42374, "FY2021": 117876}),
    ("DATA", "Change in other liabilities and provisions", {"FY2025": -2001, "FY2024": 7855, "FY2023": -4681, "FY2022": 8883, "FY2021": 1456}),
    ("DATA", "Income taxes paid", {"FY2025": -22969, "FY2024": -26070, "FY2023": -32346, "FY2022": -18955, "FY2021": -18895}),
    ("TOTAL", "Net cash generated from operating activities", {"FY2025": 111252, "FY2024": 405091, "FY2023": 233292, "FY2022": 22570, "FY2021": 304294}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisition of government bonds", {"FY2025": -78477, "FY2024": -36107, "FY2023": -74108, "FY2022": -44264}),
    ("DATA", "Proceeds from government bonds", {"FY2025": 78289, "FY2024": 11775}),
    ("DATA", "Acquisition of property, plant and equipment", {"FY2025": -2120, "FY2024": -1086, "FY2023": -745, "FY2022": -3086, "FY2021": -1349}),
    ("DATA", "Acquisition of intangible assets", {"FY2025": -412, "FY2024": -435, "FY2023": -83, "FY2022": -183, "FY2021": -86}),
    ("DATA", "Proceeds from disposal of property, plant and equipment", {"FY2025": 97, "FY2024": 27, "FY2023": 40, "FY2022": 22, "FY2021": 272}),
    ("DATA", "Proceeds from disposal of intangible assets", {"FY2021": 16}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -2623, "FY2024": -25826, "FY2023": -74896, "FY2022": -47511, "FY2021": -1147}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of subordinated debt", {"FY2022": -60000}),
    ("DATA", "Issuance of Additional Tier 1 instrument", {"FY2022": 60000}),
    ("DATA", "Dividend paid", {"FY2025": -78700, "FY2024": -98100, "FY2023": -66800, "FY2022": -33459, "FY2021": -67000}),
    ("DATA", "Interest paid on Additional Tier 1 instrument", {"FY2025": -4962, "FY2024": -5362, "FY2023": -5015}),
    ("DATA", "Repayment of principal portion of lease liabilities", {"FY2025": -722, "FY2024": -491, "FY2023": -47, "FY2022": -77, "FY2021": -1393}),
    ("DATA", "Repayment of interest portion of lease liabilities", {"FY2025": 298}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": -84086, "FY2024": -103953, "FY2023": -71862, "FY2022": -33536, "FY2021": -68393}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 24543, "FY2024": 275312, "FY2023": 86534, "FY2022": -58477, "FY2021": 234754}),
    ("DATA", "Cash and cash equivalents at beginning of period", {"FY2025": 1048859, "FY2024": 773547, "FY2023": 687013, "FY2022": 716133, "FY2021": 481379}),
    ("TOTAL", "Cash and cash equivalents at end of period", {"FY2025": 1073402, "FY2024": 1048859, "FY2023": 773547, "FY2022": 657656, "FY2021": 716133}),
]

bw.add_cash_flow_sheet(
    title="Bank of China (UK) Limited — Statement of Cash Flows",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=46, source_height=170)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 274521, "FY2024": 274294, "FY2023": 275056, "FY2022": 275000, "FY2021": 275164})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "27.2%", "FY2024": "24.8%", "FY2023": "26.8%", "FY2022": "23.4%", "FY2021": "24.6%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 334521, "FY2024": 334294, "FY2023": 335056, "FY2022": 335000, "FY2021": 275164})],
    p3_sources(),
    note="Equal to CET1 capital at FY2021 (no AT1 instruments in issue that year). A £60m Additional Tier 1 "
         "instrument was issued in June 2022, replacing an equal amount of Tier 2 subordinated debt.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "24.6%"})],
    p3_sources(),
    note="FY2021 not separately stated as a percentage in the source; numerically equal to the stated CET1 ratio "
         "since Tier 1 capital equalled CET1 capital exactly that year (no AT1 in issue).",
)

metric(
    "Total Capital", "£'000",
    [("Total regulatory capital", {"FY2025": 334521, "FY2024": 334294, "FY2023": 335056, "FY2022": 335000, "FY2021": 335164})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "29.9%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets (RWA)", {"FY2025": 1008110, "FY2024": 1106898, "FY2023": 1024452, "FY2022": 1176625, "FY2021": 1119380})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total Basel III leverage ratio exposure measure", {"FY2025": 1373968, "FY2024": 1462346, "FY2023": 1473437, "FY2022": 1814024, "FY2021": 2431869}),
        ("Basel III leverage ratio (%)", {"FY2025": "24.4%", "FY2024": "22.9%", "FY2023": "22.7%", "FY2022": "18.5%", "FY2021": "11.3%"}),
    ],
    p3_sources(),
    note="FY2021's 11.3% is on an older/broader exposure-measure basis (pre-dates the KM1 'excluding claims on "
         "central banks' framework used from FY2022 onward) - not directly comparable to later years, kept on "
         "its own row per project convention.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA)", {"FY2025": 1007375, "FY2024": 1014087, "FY2023": 677646, "FY2022": 545654, "FY2021": 527697}),
        ("Total net cash outflow", {"FY2025": 310866, "FY2024": 272240, "FY2023": 174967, "FY2022": 299877, "FY2021": 294774}),
        ("LCR ratio (%)", {"FY2025": "324.1%", "FY2024": "372.5%", "FY2023": "387.3%", "FY2022": "182.0%", "FY2021": "179.0%"}),
    ],
    p3_sources(),
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 1389486, "FY2024": 1630136, "FY2023": 1289845, "FY2022": 1463448, "FY2021": 1438026}),
        ("Total required stable funding", {"FY2025": 714820, "FY2024": 752941, "FY2023": 959234, "FY2022": 1209361, "FY2021": 950742}),
        ("NSFR ratio (%)", {"FY2025": "194.4%", "FY2024": "216.5%", "FY2023": "134.5%", "FY2022": "121.0%", "FY2021": "151.3%"}),
    ],
    p3_sources(),
    note="FY2021's own Pillar 3 document does not disclose an NSFR figure at all (the UK NSFR regime's formal KM1 "
         "disclosure only started from FY2022) - the FY2021 figures here are taken from the FY2022 Pillar 3 "
         "document's FY2021 comparative column instead, the only source where they appear.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL disclosure found in any of the 5 available Pillar 3 documents (FY2021-FY2025).",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated from operating activities", {"FY2025": 111252, "FY2024": 405091, "FY2023": 233292, "FY2022": 22570, "FY2021": 304294}),
        ("Net cash from/(used in) investing activities", {"FY2025": -2623, "FY2024": -25826, "FY2023": -74896, "FY2022": -47511, "FY2021": -1147}),
        ("Net cash used in financing activities", {"FY2025": -84086, "FY2024": -103953, "FY2023": -71862, "FY2022": -33536, "FY2021": -68393}),
        ("Cash and cash equivalents at end of period", {"FY2025": 1073402, "FY2024": 1048859, "FY2023": 773547, "FY2022": 657656, "FY2021": 716133}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "27.2%", "FY2024": "24.8%", "FY2023": "26.8%", "FY2022": "23.4%", "FY2021": "24.6%"}),
        ("Tier 1 Ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "24.6%"}),
        ("Total Capital Ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "29.9%"}),
        ("Leverage Ratio", {"FY2025": "24.4%", "FY2024": "22.9%", "FY2023": "22.7%", "FY2022": "18.5%", "FY2021": "11.3%"}),
        ("LCR", {"FY2025": "324.1%", "FY2024": "372.5%", "FY2023": "387.3%", "FY2022": "182.0%", "FY2021": "179.0%"}),
        ("NSFR", {"FY2025": "194.4%", "FY2024": "216.5%", "FY2023": "134.5%", "FY2022": "121.0%", "FY2021": "151.3%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. See the Cash Flow Statement sheet's source note for "
         "a disclosed restatement gap between FY2022's and FY2023's own reports.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF CHINA UK FINANCIALS.xlsx")
