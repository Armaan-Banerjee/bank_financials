import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Cash flow statement only exists for FY2021-FY2022 (calendar year-end) - see
# ENTITY_NOTE / CASH_FLOW_EXEMPTION_NOTE below. Pillar 3 covers all 5 years.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history"

P3_2025_URL = "https://cdn.prod.website-files.com/62b1c54534b6a11713c35c02/6a1da906ea626c65de0ea1b6_TML_Pillar%203%202025%20Final.pdf"
P3_2024_URL = "https://cdn.prod.website-files.com/62b1c54534b6a11713c35c02/680f52c61791aa8addbecd66_TML_Pillar%203%202024%20Final.pdf"
P3_2023_URL = "https://cdn.prod.website-files.com/62b1c54534b6a11713c35c02/66a0e99ad693a6e63fe72544_TML_Pillar%203%202023%20Final.pdf"
P3_2021_URL = "https://assets.website-files.com/62a364a1705cce548303c9aa/6337028c7519c4c08e1b5d54_TML_Pillar%203%202021.12.31_Board.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: 'Tandem Bank Limited' (company number 00955491, FRN 204479) is the PRA-authorised entity built "
    "here. It is NOT the same company as 'Tandem Money Limited' (company number 08628614) - a related, similarly-"
    "named entity that briefly used the name 'Tandem Bank Limited' itself from Dec 2015-May 2017 before becoming "
    "Tandem Money Limited (TML), the non-bank holding company that today sits above Tandem Bank Limited (TBL) in "
    "the group structure. Company 00955491 was previously 'Harrods Bank Limited' (renamed 12 Jan 2018) - Tandem "
    "acquired Harrods Bank's banking licence in 2017 to become a PRA-authorised deposit-taker quickly; it traces "
    "further back to 'Harrods Trust Limited' and, before that, 'Harrods (Knightsbridge) Limited' (incorporated "
    "1969), which is why Companies House shows an incorporation date decades before Tandem's own 2013 founding. "
    "Confirmed via Companies House (previous-names history) and cross-checked against the FRN in Banks List 2608.xlsx."
)

CASH_FLOW_EXEMPTION_NOTE = (
    "CASH FLOW EXEMPTION NOTE: only FY2021 and FY2022 have a Statement of Cash Flows. From the FY2023 Annual Report "
    "onward (confirmed directly in the FY2023, FY2024, and FY2025 Annual Reports - all three fully scanned/image-"
    "only Companies House filings, OCR'd with tesseract and cross-verified against rendered page images), Tandem "
    "Bank Limited's accounting policies note states: 'The Bank is a qualifying entity as defined in FRS 102 and has "
    "therefore adopted the disclosure exemptions of FRS 102 Section 7 and paragraph 3.17(d) to not disclose a cash "
    "flow statement' - the same FRS 101/102 'qualifying entity' exemption that has blocked several other banks in "
    "this project (PNBE, ICICI, United Trust Bank, Union Bancaire Privée UK) entirely. Unlike those banks, Tandem "
    "took the exemption only recently (from FY2023) rather than throughout its history, so FY2021-FY2022 do have "
    "genuine, fully reconciling cash flow statements - both built here from the Bank's own Companies House filings "
    "(also fully scanned, OCR'd and cross-verified) rather than skipping the bank outright. FY2023-FY2025 are left "
    "blank on the Cash Flow Statement sheet rather than guessed."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Tandem Bank Limited's own (Company-only, not Group) Statement of Cash Flows, £'000:\n"
    f"FY2022: Tandem Bank Limited Annual Report and Accounts for the year ended 31 December 2022, p.45 (Statement "
    f"of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: Tandem Bank Limited Annual Report and Accounts for the year ended 31 December 2021, p.48 (Statement "
    f"of Cash Flows) - {AR2021_URL}\n"
    "Both years' figures were independently cross-checked against their appearance as the following year's "
    "comparative column (FY2021 as reported in the FY2022 Annual Report) and matched exactly.\n\n"
    + ENTITY_NOTE + "\n\n" + CASH_FLOW_EXEMPTION_NOTE
)


def p3_sources(page_25="4", page_24="4", page_23="3", page_21="21"):
    return (
        "Sources - Tandem Money Limited (TML) Group consolidated basis (comprising TML, its wholly-owned "
        "subsidiary Tandem Bank Limited (TBL), and Allium Lending Group Limited) - NOT Tandem Bank Limited solo:\n"
        f"FY2025: TML Pillar 3 Disclosures, 31 December 2025, p.{page_25} (2. Key Metrics - UK KM1) - {P3_2025_URL}\n"
        f"FY2024: TML Pillar 3 Disclosures, 31 December 2024, p.{page_24} (2. Key Metrics - UK KM1) - {P3_2024_URL}\n"
        f"FY2023: TML Pillar 3 Disclosures, 31 December 2023, p.{page_23} (2. Key Metrics - UK KM1) - {P3_2023_URL}\n"
        "FY2022: no standalone Pillar 3 edition was found published or archived for 31 December 2022 (not on "
        "Tandem's newsroom page, not found via web search or Wayback Machine) - sourced instead from the FY2023 "
        f"Pillar 3 Disclosures' own '31 Dec '22' comparative column, p.{page_23} - {P3_2023_URL}\n"
        f"FY2021: TML Pillar 3 Disclosures, 31 December 2021, p.{page_21} (4. Capital Disclosures) and p.32-41 "
        f"(8. Leverage / Appendix 3: Liquidity Coverage Ratio) - {P3_2021_URL}\n"
        "PILLAR 3 BASIS NOTE: this is a genuine cash-flow-vs-Pillar-3 basis mismatch (Bank-only cash flow vs. "
        "Group-level Pillar 3), the same pattern seen with Vanquis Bank Limited elsewhere in this project - Tandem "
        "does not publish a Bank-only Pillar 3 breakout."
    )


bw = BankWorkbook(bank_name="Tandem Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="7C4A03")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Loss on operating activities before tax", {"FY2022": -6933, "FY2021": -18030}),
    ("DATA", "Non-cash items included in loss on operating activities before tax", {"FY2022": 11707, "FY2021": 2173}),
    ("DATA", "Change in operating assets and liabilities", {"FY2022": 304576, "FY2021": 217383}),
    ("TOTAL", "Net Cash Generated from Operating Activities", {"FY2022": 309350, "FY2021": 201526}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "(Purchase)/sale of debt securities", {"FY2022": -61572, "FY2021": -2075}),
    ("TOTAL", "Net Cash Used in Investing Activities", {"FY2022": -61572, "FY2021": -2075}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issuance of ordinary shares", {"FY2022": 76464, "FY2021": 12309}),
    ("TOTAL", "Net Cash Generated from Financing Activities", {"FY2022": 76464, "FY2021": 12309}),
    ("TOTAL", "Net Increase in Cash and Cash Equivalents", {"FY2022": 324242, "FY2021": 211760}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2022": 376688, "FY2021": 164928}),
    ("TOTAL", "Cash and Cash Equivalents at the end of the Year", {"FY2022": 700930, "FY2021": 376688}),
]

bw.add_cash_flow_sheet(
    title="Tandem Bank Limited — Statement of Cash Flows",
    subtitle="Bank (Company-only) basis, £'000. FY2023-FY2025 blank - see source note at bottom (FRS 102 cash-flow exemption).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"TML Group basis, {unit}" if unit else "TML Group basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=170)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 168224, "FY2024": 165574, "FY2023": 150158, "FY2022": 119883, "FY2021": 39742})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWEA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "15.53%", "FY2024": "17.40%", "FY2023": "16.1%", "FY2022": "15.2%", "FY2021": "14.2%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 168224, "FY2024": 165574, "FY2023": 150158, "FY2022": 119883, "FY2021": 39742})],
    p3_sources(),
    note="Tier 1 Capital = CET1 Capital every year through FY2022 (no AT1 instruments); AT1 capital was first "
         "issued in FY2023 but is included within Total Capital, not Tier 1, per the Group's own KM1 template "
         "(rows 1 and 2 are identical every year) - Total Capital is the row where AT1/T2 shows up as a difference.",
)

metric(
    "Tier 1 Ratio", "% of RWEA",
    [("Tier 1 ratio", {"FY2025": "15.53%", "FY2024": "17.40%", "FY2023": "16.1%", "FY2022": "15.2%", "FY2021": "14.2%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 196155, "FY2024": 192343, "FY2023": 175438, "FY2022": 119883, "FY2021": 39742})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWEA",
    [("Total capital ratio", {"FY2025": "18.11%", "FY2024": "20.21%", "FY2023": "18.8%", "FY2022": "15.2%", "FY2021": "14.2%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets (RWEA)", {"FY2025": 1083333, "FY2024": 951607, "FY2023": 931650, "FY2022": 790158, "FY2021": 280843})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 1860727, "FY2024": 1652240, "FY2023": 1458860, "FY2022": 1401205, "FY2021": 859746}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "9.04%", "FY2024": "10.02%", "FY2023": "9.8%", "FY2022": "8.8%", "FY2021": "4.6%"}),
    ],
    p3_sources(),
    note="FY2021's Pillar 3 report predates the 'excluding claims on central banks' UK leverage framework "
         "(introduced Jan 2021 but not yet reflected in TML's own template that year) - its Table LRCom shows a "
         "single 'Total Leverage Ratio Exposures' / 'Leverage Ratio' figure (859,746 / 4.6%), shown here on the "
         "'excluding' row for comparability with later years, though it is not confirmed to be on an identical "
         "basis. The FY2024 Pillar 3 report's own comparative column restates FY2023's exposure measure to "
         "1,529,033 (footnoted 'Restated'); the figure shown here for FY2023 (1,458,860 / 9.8%) is as originally "
         "reported in the FY2023 Pillar 3 Disclosures itself, not the later restated comparative.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 1148813, "FY2024": 1927554, "FY2023": 1786879, "FY2022": 329806}),
        ("Total net cash outflows, adjusted value", {"FY2025": 258152, "FY2024": 359743, "FY2023": 281464, "FY2022": 103147}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "443.40%", "FY2024": "534.75%", "FY2023": "636.0%", "FY2022": "314.1%", "FY2021": "331%"}),
    ],
    p3_sources(),
    note="FY2022-FY2025 LCR is a simple average of monthly liquidity positions during the calendar year (per each "
         "report's own footnote). FY2021 used a different methodology (simple average of month-end observations "
         "over the trailing 12 months up to each quarter-end); the Group's FY2021 report only tabulates quarterly "
         "LCR values (31%: Dec '21 = 331%, Sep '21 = 394%, Jun '21 = 709%, Mar '21 = 1,832%) rather than one "
         "annual figure - the 31 Dec 2021 (year-end) value is shown here for comparability, but the two "
         "methodologies are not identical so a direct FY2021-to-FY2022 LCR comparison should be treated with "
         "caution. No HQLA/cash-outflow £ breakdown was found for FY2021 (only the % ratio was tabulated).",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 2560820, "FY2024": 3156347, "FY2023": 3142854, "FY2022": 1447618}),
        ("Total required stable funding", {"FY2025": 1320668, "FY2024": 1199958, "FY2023": 1156379, "FY2022": 922410}),
        ("NSFR ratio (%)", {"FY2025": "194.30%", "FY2024": "263.10%", "FY2023": "270.6%", "FY2022": "155.5%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="NSFR not disclosed for FY2021 - not yet part of TML's Pillar 3 template that year (consistent with the "
         "UK NSFR requirement not applying to reporting periods that early elsewhere in this project, e.g. Zopa).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "MREL is not disclosed in any of TML's Pillar 3 Disclosures FY2021-FY2025. The Group states "
                       "(FY2023 Pillar 3 Disclosures, Overview) that it qualifies as a 'small, non-complex' "
                       "institution under UK CRR Article 4(145) and follows the reduced Pillar 3 disclosure regime "
                       "of Article 433(b) - consistent with, though not an explicit stated reason for, the absence "
                       "of any MREL figure.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2022": 309350, "FY2021": 201526}),
        ("Net cash from/(used in) investing activities", {"FY2022": -61572, "FY2021": -2075}),
        ("Net cash from/(used in) financing activities", {"FY2022": 76464, "FY2021": 12309}),
        ("Cash and cash equivalents at end of year", {"FY2022": 700930, "FY2021": 376688}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.53%", "FY2024": "17.40%", "FY2023": "16.1%", "FY2022": "15.2%", "FY2021": "14.2%"}),
        ("Tier 1 Ratio", {"FY2025": "15.53%", "FY2024": "17.40%", "FY2023": "16.1%", "FY2022": "15.2%", "FY2021": "14.2%"}),
        ("Total Capital Ratio", {"FY2025": "18.11%", "FY2024": "20.21%", "FY2023": "18.8%", "FY2022": "15.2%", "FY2021": "14.2%"}),
        ("Leverage Ratio", {"FY2025": "9.04%", "FY2024": "10.02%", "FY2023": "9.8%", "FY2022": "8.8%", "FY2021": "4.6%"}),
        ("LCR", {"FY2025": "443.40%", "FY2024": "534.75%", "FY2023": "636.0%", "FY2022": "314.1%", "FY2021": "331%"}),
        ("NSFR", {"FY2025": "194.30%", "FY2024": "263.10%", "FY2023": "270.6%", "FY2022": "155.5%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Cash flow is blank for FY2023-FY2025 (FRS 102 qualifying-"
         "entity exemption took effect from FY2023 - see Cash Flow Statement sheet note) and ratios are on a wider "
         "TML Group basis, not Tandem Bank Limited solo (see each Pillar 3 sheet's source note) - two different, "
         "independently-documented basis differences within this single workbook.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/TANDEM FINANCIALS.xlsx")
