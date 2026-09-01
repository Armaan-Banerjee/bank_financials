import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/11379025/filing-history/MzUxNzk5NTMwNmFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/11379025/filing-history/MzQyMjE2MDUwOWFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/11379025/filing-history/MzM1Mjk5ODYxMGFkaXF6a2N4/document?format=pdf&download=0"

P3_2024_URL = "https://www.triodos.co.uk/binaries/content/assets/tbuk/press-and-media-page/triodos-bank-uk-2024-pillar-3.pdf"
P3_2023_URL = "https://www.triodos.co.uk/binaries/content/assets/tbuk/press-and-media-page/triodos-bank-uk-2023-pillar-3-report.pdf"
P3_2022_URL = "https://www.triodos.co.uk/binaries/content/assets/tbuk/press-and-media-page/triodos-bank-uk-2022-pillar-3-report.pdf"
P3_2021_URL = "https://www.triodos.co.uk/downloads/triodos-bank-uk-2021-pillar-3-report?id=9efebf75e4f1"

ENTITY_NOTE = (
    "ENTITY NOTE: Triodos Bank UK Limited (TBUK, company number 11379025, FRN 817008) is a wholly owned "
    "subsidiary of Triodos Bank N.V. (the Netherlands), established in 2019 to continue Triodos Bank's UK "
    "operations (previously run as a UK branch of Triodos Bank N.V. since 1995) via a Part VII transfer. Although "
    "TBUK's own accounts are exempt under s.401 of the Companies Act 2006 from preparing CONSOLIDATED financial "
    "statements (it and its subsidiary undertaking are fully consolidated into Triodos Bank N.V.'s own group "
    "accounts), TBUK's own entity-level accounts DO include a full Statement of Cash Flows every year - unlike "
    "several other single-parent foreign subsidiary banks in this series (e.g. ICICI Bank UK, United Trust Bank), "
    "TBUK does not take the FRS 101/102 cash-flow-statement disclosure exemption. All figures below are TBUK's own "
    "entity-level (Company) results, in £, not Triodos Bank N.V. group figures. Companies House filings for all 5 "
    "years were fully scanned/image-only PDFs with no text layer; all figures were extracted via OCR (tesseract) "
    "and cross-verified visually against the rendered page images."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Triodos Bank UK Limited's own entity-level (Company) Statement of Cash Flows, £'000:\n"
    f"FY2025: Triodos Bank UK Limited Annual Report 2025 (Companies House filing, made up to 31 Dec 2025), p.57-58 "
    f"(Statement of cash flows for the year ended 31 December 2025) - {AR2025_URL}\n"
    f"FY2024: as reported in the FY2025 Annual Report's own FY2024 comparative column, same pages/source as above.\n"
    f"FY2023: Triodos Bank UK Limited Annual Report 2023 (Companies House filing, made up to 31 Dec 2023), p.76-77 "
    f"(Cash flow statement for the year ended 31 December 2023) - {AR2023_URL}\n"
    f"FY2022: as reported in the FY2023 Annual Report's own FY2022 comparative column, same pages/source as above.\n"
    f"FY2021: Triodos Bank UK Limited Annual Report 2021 (Companies House filing, made up to 31 Dec 2021), p.30-31 "
    f"(Cash flow statement for the year ended 31 December 2021) - {AR2021_URL}\n"
    "PRESENTATION NOTE: 'Cash flow from operating activities' is a two-level subtotal in every year's own "
    "statement - a 'Cash flow from business operations' subtotal (profit before tax + non-cash adjustments), "
    "followed by 'Changes in net operating assets' line items, with the final 'Cash flow from operating "
    "activities' total equal to the BUSINESS OPERATIONS SUBTOTAL PLUS the changes lines, not just the changes "
    "lines alone. verify_workbook.py's generic block-check will report a false-positive mismatch on this specific "
    "total for exactly this reason (it only sums the DATA rows since the immediately preceding TOTAL/SECTION) - "
    "this is expected and not a data error; every subtotal and total independently ties to source and was hand-"
    "verified. Some line items were relabelled or moved sections between report vintages (wording/sign-convention "
    "only, e.g. 'Increase in Expected Credit Losses' (FY2021) vs '(Decrease)/Increase in ECL on financial "
    "instruments' (FY2023) vs 'Decrease in ECL on financial instruments' (FY2025)) - unified onto a single row "
    "where the underlying line item is genuinely the same measure. One GENUINE structural change: 'increase in "
    "interest receivable on debt securities' moved from the INVESTING section (FY2021-FY2023 statements) to the "
    "OPERATING section (FY2024-FY2025 statements) - kept as two separate rows in their respective sections, "
    "exactly as each year's own statement presented it. Blank cells indicate that year's statement did not "
    "disclose/include that specific line at all; a printed '-' in the source was transcribed as 0 (an explicit "
    "nil disclosure, not a gap).\n\n"
    + ENTITY_NOTE
)


def p3_sources(pages="7-14"):
    return (
        "Sources - Triodos Bank UK Limited (TBUK) entity-level Pillar 3 disclosures:\n"
        f"FY2024: Triodos Bank UK Limited 2024 Pillar 3 Report, p.{pages} - {P3_2024_URL}\n"
        f"FY2023: Triodos Bank UK Limited 2023 Pillar 3 Report - {P3_2023_URL}\n"
        f"FY2022: Triodos Bank UK Limited 2022 Pillar 3 Report - {P3_2022_URL}\n"
        f"FY2021: Triodos Bank UK Limited 2021 Pillar 3 Report - {P3_2021_URL}\n"
        "FY2025: no standalone Pillar 3 report has been published yet as of this workbook's build date (2026-08-26) "
        "- the FY2025 Annual Report was only filed 28 Apr 2026 and TBUK's Pillar 3 report has historically followed "
        "several months after its Annual Report (e.g. the FY2024 edition above was published well after the "
        "FY2024 Annual Report). Where marked '(derived)' below, a FY2025 figure was calculated from Annual Report "
        "disclosures rather than transcribed from a Pillar 3 table, since no such table exists yet - see the "
        "sheet's own note.\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Triodos Bank UK Limited", years=YEARS, year_label=YEAR_LABEL, header_color="5A3E85")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 18175, "FY2024": 6970, "FY2023": 2915, "FY2022": 10201, "FY2021": 8478}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 388, "FY2024": 1082, "FY2023": 1045, "FY2022": 1022, "FY2021": 980}),
    ("DATA", "Loss on fixed asset disposal", {"FY2023": 20, "FY2022": 5, "FY2021": 0}),
    ("DATA", "Debt securities premium and discount amortisation", {"FY2025": -5116, "FY2024": -4528, "FY2023": -1710, "FY2022": 82, "FY2021": 1509}),
    ("DATA", "Increase in interest receivable on debt securities", {"FY2025": -2225, "FY2024": -2163}),
    ("DATA", "Increase/(Decrease) in ECL on financial instruments", {"FY2025": -1246, "FY2024": -3590, "FY2023": -787, "FY2022": 4262, "FY2021": 2268}),
    ("DATA", "Write off of financial instruments", {"FY2025": 1539, "FY2024": 7229, "FY2023": 12308, "FY2022": 0}),
    ("DATA", "Increase/(Decrease) in provisions", {"FY2025": -531, "FY2024": 820, "FY2023": -80, "FY2022": -527, "FY2021": 199}),
    ("DATA", "Interest on lease liabilities", {"FY2025": 16, "FY2024": 29, "FY2023": 39, "FY2022": 36, "FY2021": 28}),
    ("DATA", "Tax expense", {"FY2025": -4247, "FY2024": -1467, "FY2023": -127, "FY2022": -997, "FY2021": -637}),
    ("TOTAL", "Cash flow from business operations", {"FY2025": 6753, "FY2024": 4382, "FY2023": 13623, "FY2022": 14084, "FY2021": 12825}),
    ("DATA", "Increase/(Decrease) in loans and advances to customers", {"FY2025": -10208, "FY2024": 19325, "FY2023": -1593, "FY2022": 6563, "FY2021": -64020}),
    ("DATA", "Increase/(Decrease) in deferred tax asset", {"FY2025": -70, "FY2024": 34, "FY2023": -53, "FY2022": 3, "FY2021": -77}),
    ("DATA", "Increase/(Decrease) in other assets", {"FY2025": -171, "FY2024": 252, "FY2023": -660, "FY2022": 604, "FY2021": 730}),
    ("DATA", "(Decrease) in deposits from credit institutions", {"FY2025": -2983, "FY2024": -5265, "FY2023": -6684, "FY2022": -3207, "FY2021": -6243}),
    ("DATA", "Increase in deposits from customers", {"FY2025": 81761, "FY2024": 71951, "FY2023": 22145, "FY2022": 34303, "FY2021": 194863}),
    ("DATA", "Increase/(Decrease) in current tax liability", {"FY2025": 1728, "FY2024": 1117, "FY2023": -957, "FY2022": -66, "FY2021": 164}),
    ("DATA", "Increase/(Decrease) in other liabilities", {"FY2025": -3834, "FY2024": -5425, "FY2023": 6056, "FY2022": 2788, "FY2021": 667}),
    ("TOTAL", "Cash flow from operating activities (= business operations subtotal + changes above)", {"FY2025": 72976, "FY2024": 86371, "FY2023": 31877, "FY2022": 55072, "FY2021": 138909}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Investment in intangible assets", {"FY2025": -132, "FY2024": -701, "FY2023": -5, "FY2022": -200, "FY2021": -85}),
    ("DATA", "Investment in property and equipment", {"FY2025": 502, "FY2024": -481, "FY2023": -294, "FY2022": -342, "FY2021": -254}),
    ("DATA", "(Increase)/decrease in interest receivable on debt securities", {"FY2023": -1777, "FY2022": 249, "FY2021": 49}),
    ("DATA", "Investment in debt securities", {"FY2025": -240343, "FY2024": -183290, "FY2023": -162400, "FY2022": -106096, "FY2021": -138211}),
    ("DATA", "Sale of debt securities", {"FY2023": 0, "FY2022": 0, "FY2021": 5128}),
    ("DATA", "Maturity of debt securities", {"FY2025": 156285, "FY2024": 95000, "FY2023": 55000, "FY2022": 29000, "FY2021": 15500}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -83688, "FY2024": -89472, "FY2023": -109476, "FY2022": -77389, "FY2021": -117873}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid", {"FY2025": -5500, "FY2024": -1400, "FY2023": -2800, "FY2022": 0, "FY2021": -2300}),
    ("DATA", "Payment of lease liabilities", {"FY2025": -55, "FY2024": -175, "FY2023": -168, "FY2022": -160, "FY2021": -156}),
    ("DATA", "Increase/(Decrease) in debt issued and borrowed funds", {"FY2025": -5736, "FY2024": 0, "FY2023": 3, "FY2022": -4, "FY2021": 33}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": -11291, "FY2024": -1575, "FY2023": -2965, "FY2022": -164, "FY2021": -2423}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -22003, "FY2024": -4676, "FY2023": -80564, "FY2022": -22481, "FY2021": 18613}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 309277, "FY2024": 313953, "FY2023": 394517, "FY2022": 416998, "FY2021": 398385}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 287274, "FY2024": 309277, "FY2023": 313953, "FY2022": 394517, "FY2021": 416998}),
    ("SECTION", "Represented by (memo breakdown, not additional totals)", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 269090, "FY2024": 298593, "FY2023": 282378, "FY2022": 359906, "FY2021": 374820}),
    ("DATA", "On demand deposits with credit institutions", {"FY2025": 18184, "FY2024": 10684, "FY2023": 30472, "FY2022": 33412, "FY2021": 40979}),
    ("DATA", "Other loans and advances to credit institutions", {"FY2023": 1103, "FY2022": 1199, "FY2021": 1199}),
]

bw.add_cash_flow_sheet(
    title="Triodos Bank UK Limited — Cash Flow Statement",
    subtitle="TBUK entity-level (Company) basis, £'000. See source note for the two-level operating subtotal.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"TBUK entity-level basis, {unit}" if unit else "TBUK entity-level basis",
                         rows_data, sources_text, note=note, first_col_width=52, source_height=140)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 193448, "FY2024": 193259, "FY2023": 192544, "FY2022": 185772, "FY2021": 177905})],
    p3_sources(),
    note="FY2025 is from the Annual Report's own 'Total capital resources' note (Note 26/27, audited) since no "
         "FY2025 Pillar 3 report has been published yet - not derived, directly stated.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "21.3%", "FY2024": "22.1%", "FY2023": "22.36%", "FY2022": "21.57%", "FY2021": "21.2%"})],
    p3_sources(),
    note="FY2025 is from the Annual Report narrative (p.15), stated as 21.3% (2024: 22.1%); FY2024's figure there "
         "(22.1%) rounds slightly differently from the FY2024 Pillar 3 Report's own Table 9 figure (22.06%) - both "
         "are as-stated in their respective source documents, not reconciled to more decimal places.",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 193448, "FY2024": 193259, "FY2023": 192544, "FY2022": 185772, "FY2021": 177905})],
    p3_sources(),
    note="TBUK has no Additional Tier 1 (AT1) instruments in any year - Tier 1 capital equals CET1 capital exactly, "
         "every year, per the Annual Report's own 'Total capital resources' table (e.g. FY2025/FY2024: 'CET1 and "
         "Total Tier 1 capital resources' is a single stated line).",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "21.3%", "FY2024": "22.1%", "FY2023": "22.36%", "FY2022": "21.57%", "FY2021": "21.2%"})],
    p3_sources(),
    note="Numerically identical to the CET1 ratio every year, since Tier 1 capital = CET1 capital (no AT1 "
         "instruments) - not a separate disclosure.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 193448, "FY2024": 198954, "FY2023": 198239, "FY2022": 191467, "FY2021": 183600})],
    p3_sources(),
    note="Total capital = CET1 + Tier 2 (subordinated debt, £5.7m issued Dec 2020). The Tier 2 note was fully "
         "repaid in 2025, so FY2025 Total capital equals CET1 exactly for the first time in this series.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "21.3%", "FY2024": "22.7%", "FY2023": "23.02%", "FY2022": "22.20%", "FY2021": "21.8%"})],
    p3_sources(),
    note="FY2025/FY2024 from the Annual Report narrative (p.15); FY2024's Pillar 3 Report states this ratio as "
         "22.71% (Table 7) - a minor rounding difference from the Annual Report's 22.7%, both as-stated.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets (credit + operational + market + counterparty credit risk)",
      {"FY2025": 908207, "FY2024": 876076, "FY2023": 861016, "FY2022": 861273, "FY2021": 840391})],
    p3_sources(),
    note="FY2025 is CALCULATED (Total capital £193,448k / Total capital ratio 21.3% = ~£908.2m), not directly "
         "stated, since no FY2025 Pillar 3 report exists yet to give the audited RWA breakdown - simple arithmetic "
         "on two audited/stated figures, not an estimate, flagged per this project's convention (see Bank of "
         "Ireland UK workbook for the same approach). FY2024-FY2021 are Total RWA figures directly stated in each "
         "year's own Pillar 3 Report (Credit + Operational risk RWA; Market risk and Counterparty Credit risk RWA "
         "are nil every year).",
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Tier 1 capital after deductions", {"FY2024": 193258, "FY2023": 192544, "FY2022": 185772, "FY2021": 177905}),
        ("Leverage ratio exposure measure", {"FY2024": 1715067, "FY2023": 1664149, "FY2022": 1583516, "FY2021": 1910203}),
        ("Leverage ratio (%)", {"FY2024": "11.27%", "FY2023": "11.57%", "FY2022": "11.73%", "FY2021": "9.3%"}),
    ],
    p3_sources(),
    note="TBUK is below the £50bn deposit threshold that triggers a binding UK leverage ratio requirement (PRA "
         "expectation only, minimum 3.25%). FY2022 onward uses the 'excluding claims on central banks' exposure "
         "basis (introduced in the 2022 Pillar 3 Report); FY2021's own 2021 Pillar 3 Report used a broader, "
         "non-comparable CRR2 full-exposure basis (9.3%, exposure measure £1,910.2m, including central bank "
         "claims) - shown here exactly as that year's own report stated it, NOT the later report's restated "
         "comparative, consistent with this project's practice of not blending non-comparable methodology "
         "vintages. No FY2025 figure: not disclosed in the Annual Report and no FY2025 Pillar 3 report exists yet.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total HQLA (point-in-time, year-end)", {"FY2024": 826600, "FY2023": 715900, "FY2022": 668900, "FY2021": 628207}),
        ("Total net cash outflows over 30-day stress (point-in-time, year-end)", {"FY2024": 175400, "FY2023": 170100, "FY2022": 151100, "FY2021": 151875}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "446%", "FY2024": "471.1%", "FY2023": "420.8%", "FY2022": "442.7%", "FY2021": "413.6%"}),
    ],
    p3_sources(),
    note="All ratios are the year-end point-in-time LCR (not the 12-month average-by-quarter tables each Pillar 3 "
         "report also separately discloses). FY2025's ratio (446%) is from the Annual Report narrative only (p.15) "
         "- no £ HQLA/outflow breakdown is available since no FY2025 Pillar 3 report exists yet.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Available stable funding", {"FY2024": 1731150, "FY2022": 1637537}),
        ("Required stable funding", {"FY2024": 866978, "FY2022": 903741}),
        ("Net Stable Funding Ratio (%)", {"FY2024": "206%", "FY2023": "188%", "FY2022": "181%"}),
    ],
    p3_sources(),
    note="FY2024 and FY2022 are year-end point-in-time NSFR (FY2024 Pillar 3 Report states '206%' directly in "
         "narrative and gives the underlying £; FY2022's own Pillar 3 Report gives a separate point-in-time "
         "quarter-end table distinct from its 12-month-average table, from which the 31-Dec-22 figure of 181% is "
         "taken). FY2023's Pillar 3 Report only discloses the 12-month-average-by-quarter-end table (no separate "
         "point-in-time statement that year) - 188% shown here is that average-basis 31-Dec-23 quarter figure, "
         "not a strict point-in-time balance, so is not fully comparable to the other years' figures. FY2021: no "
         "NSFR section appears in TBUK's 2021 Pillar 3 Report at all (the metric was not yet part of that year's "
         "disclosure). FY2025: not disclosed - no FY2025 Pillar 3 report exists yet and the Annual Report gives no "
         "NSFR percentage (only confirms the ratio is monitored).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "No MREL figure or qualitative MREL disclosure appears in any of TBUK's Annual Reports or "
                      "Pillar 3 Reports (FY2021-FY2024) - not asserted as an explicit exemption, simply absent "
                      "from every source reviewed, consistent with several other small banks in this project "
                      "series (e.g. Zopa, LHV, Vida).",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Cash flow from operating activities", {"FY2025": 72976, "FY2024": 86371, "FY2023": 31877, "FY2022": 55072, "FY2021": 138909}),
        ("Net cash from/(used in) investing activities", {"FY2025": -83688, "FY2024": -89472, "FY2023": -109476, "FY2022": -77389, "FY2021": -117873}),
        ("Net cash from/(used in) financing activities", {"FY2025": -11291, "FY2024": -1575, "FY2023": -2965, "FY2022": -164, "FY2021": -2423}),
        ("Cash and cash equivalents at end of year", {"FY2025": 287274, "FY2024": 309277, "FY2023": 313953, "FY2022": 394517, "FY2021": 416998}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "21.3%", "FY2024": "22.1%", "FY2023": "22.36%", "FY2022": "21.57%", "FY2021": "21.2%"}),
        ("Tier 1 Ratio", {"FY2025": "21.3%", "FY2024": "22.1%", "FY2023": "22.36%", "FY2022": "21.57%", "FY2021": "21.2%"}),
        ("Total Capital Ratio", {"FY2025": "21.3%", "FY2024": "22.7%", "FY2023": "23.02%", "FY2022": "22.20%", "FY2021": "21.8%"}),
        ("Leverage Ratio", {"FY2024": "11.27%", "FY2023": "11.57%", "FY2022": "11.73%", "FY2021": "9.3%"}),
        ("LCR", {"FY2025": "446%", "FY2024": "471.1%", "FY2023": "420.8%", "FY2022": "442.7%", "FY2021": "413.6%"}),
        ("NSFR", {"FY2024": "206%", "FY2023": "188%", "FY2022": "181%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. No FY2025 Pillar 3 report has been published yet, so Leverage "
         "Ratio and NSFR are blank for FY2025 (Total RWAs on that sheet is a calculated figure for FY2025 - see "
         "its own note). TBUK does not take the FRS 101/102 cash-flow exemption used by several other single-"
         "parent foreign subsidiary banks in this project - a full Statement of Cash Flows exists for all 5 years.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/TRIODOS FINANCIALS.xlsx")
