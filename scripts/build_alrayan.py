import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Full 5 years of cash flow AND Pillar 3 coverage for FY2021-FY2024; FY2025 Pillar 3
# not yet published (accounts filed but the Pillar 3 disclosure typically lags ~9
# months - none found as of this build). No FRS 101/102 cash-flow exemption at all.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/04483430"
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04483430/filing-history/MzUxNTE1ODIyNGFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://www.alrayanbank.co.uk/sites/default/files/media/file-uploads/2025-04/04a_-_arb_financial_statements_fy_31-12-2024_-_signed_ey.cleaned.pdf"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04483430/filing-history/MzM4MzEwOTk0N2FkaXF6a2N4/document?format=pdf&download=0"
P3_2021_URL = "https://www.alrayanbank.co.uk/sites/default/files/media/file-uploads/2022-10/inv-rep-2021-pillar-3.pdf"
P3_2023_URL = "https://www.alrayanbank.co.uk/sites/default/files/media/file-uploads/2024-08/pb7703_al_rayan_pillar_3_disclosures_2023_v2.pdf"
P3_2024_URL = "https://www.alrayanbank.co.uk/sites/default/files/media/file-uploads/2025-09/alrayan_pillar_3_disclosures_2024_web_-_010925.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Alrayan Bank Limited (FRN 229148, Companies House 04483430, matches Banks List 2608.xlsx "
    "exactly) is a UK Sharia-compliant bank, wholly owned by AlRayan Bank (Q.P.S.C.) of Qatar. Its own Annual "
    "Report/Pillar 3 documents style it 'Al Rayan Bank PLC' but Companies House confirms its current registered "
    "name is 'ALRAYAN BANK LIMITED' - same company number throughout, not an entity change, just inconsistent "
    "branding between the statutory filing and the bank's own PDFs."
)

CASH_FLOW_SOURCES = (
    "Sources - Al Rayan Bank's own Statement of Cash Flows, £'000s, all years:\n"
    f"FY2025: FY2025 Annual Report and Financial Statements (Companies House filing, made up to 31 Dec 2025, "
    f"filed 16 Apr 2026), p.41 - {AR2025_URL}\n"
    f"FY2024: FY2024 Annual Report and Financial Statements, p.42 - {AR2024_URL}\n"
    f"FY2023: sourced from the FY2024 Annual Report's own FY2023 comparative column, p.42 - {AR2024_URL}\n"
    f"FY2022: FY2022 Annual Report and Financial Statements (Companies House filing, made up to 31 Dec 2022, "
    f"filed 23 Jun 2023), p.38 - {AR2022_URL}\n"
    f"FY2021 (restated): sourced from the FY2022 Annual Report's own FY2021 comparative column, p.38 - "
    f"{AR2022_URL}. The FY2022 report's own footnote explains the FY2021 restatement: the Bank of England cash "
    f"ratio deposit was removed from 'Cash and cash equivalents' and MasterCard balances were added, following "
    f"updated IFRS Interpretations Committee guidance - the originally-reported FY2021 figures (from a standalone "
    f"FY2021 Annual Report) were not used, this restated version was, consistent with project convention of using "
    f"a year's most contemporary/authoritative appearance.\n"
    "FY2025's Statement of Cash Flows introduces new line-item names not used in earlier years (e.g. 'Structured "
    "real estate' replacing 'Commercial property finance', a new 'Securities purchased under reverse repurchase "
    "agreements' line, 'Encumbered non-cash balances' replacing 'Treasury placements') - these are shown as "
    "separate rows below rather than force-merged into the old line items, consistent with how this project "
    "handles other banks' presentation changes; every year's own reported section TOTALs are unaffected and the "
    "full chain reconciles exactly across all 5 years except one immaterial £1k FY2021 rounding gap in the source "
    "document itself (opening 383,234 + net change -138,791 + FX -354 = 244,089 vs the printed closing balance of "
    "244,090), kept as printed not force-corrected.\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Alrayan Bank Limited's own Pillar 3 Disclosures, £m capital amounts / % ratios, all years:\n"
        f"FY2024: Pillar 3 Disclosures - 31 December 2024, Annex I KM1 table, p.38 - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures - 31 December 2023, Annex I KM1 table, p.33 - {P3_2023_URL}\n"
        f"FY2022: sourced from the FY2023 Pillar 3 Disclosures' own FY2022 comparative column, Annex I KM1 table, "
        f"p.33 - {P3_2023_URL}\n"
        f"FY2021: Pillar 3 Disclosures - 31 December 2021, Table 1/2/3 (this edition pre-dates the bank's adoption "
        f"of the standardised KM1 Annex template, so FY2021 figures come from the Executive Summary tables "
        f"instead), p.5 - {P3_2021_URL}\n"
        "FY2025: no Pillar 3 Disclosures document has been published yet as of this build (FY2025 accounts were "
        "only filed 16 Apr 2026; this bank's Pillar 3 editions have historically lagged the Annual Report by "
        "roughly 9 months) - left blank rather than guessed.\n"
        "This bank's own Pillar 3 documents show small internal discrepancies between their Executive Summary "
        "narrative tables and their formal KM1 Annex tables in a couple of instances (e.g. FY2023 NSFR: 160% "
        "exec summary vs 157% KM1 annex; FY2022 Leverage Ratio: 6.8% exec summary vs 6.7% KM1 annex) - this "
        "workbook uses the KM1 Annex figures throughout for consistency with the standard regulatory template and "
        "with every other bank in this project.\n"
        + (extra + "\n" if extra else "")
        + "\n" + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Alrayan Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="4361EE")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 23587, "FY2024": 23469, "FY2023": 30608, "FY2022": 20797, "FY2021": 9627}),
    ("DATA", "Depreciation", {"FY2025": 1407, "FY2024": 1844, "FY2023": 1338, "FY2022": 1843, "FY2021": 2968}),
    ("DATA", "Amortisation", {"FY2025": 1064, "FY2024": 1361, "FY2023": 1230, "FY2022": 1991, "FY2021": 1516}),
    ("DATA", "Loss/(gain) on disposal of investment securities", {"FY2023": 3766, "FY2022": -51, "FY2021": -25}),
    ("DATA", "Cost of subordinated funding", {"FY2025": 1118, "FY2024": 2000, "FY2023": 2000}),
    ("DATA", "Impairment / expected credit loss charge on financial assets",
     {"FY2025": 3798, "FY2024": 2936, "FY2023": 1428, "FY2022": 183, "FY2021": -464}),
    ("DATA", "Other non-cash items", {"FY2025": 191, "FY2024": 943, "FY2023": 340, "FY2022": 292, "FY2021": 565}),
    ("TOTAL", "Net cash generated before changes in operating assets and liabilities",
     {"FY2025": 31165, "FY2024": 32553, "FY2023": 40710, "FY2022": 25055, "FY2021": 14187}),
    ("DATA", "Treasury placements", {"FY2024": 3330, "FY2023": -350, "FY2022": 120, "FY2021": -1318}),
    ("DATA", "Encumbered non-cash balances", {"FY2025": -1054}),
    ("DATA", "Home purchase plans", {"FY2025": 45000, "FY2024": 61204, "FY2023": 106281, "FY2022": 92488, "FY2021": 1971}),
    ("DATA", "Commercial property finance", {"FY2024": -278317, "FY2023": -111420, "FY2022": -120113, "FY2021": -112138}),
    ("DATA", "Structured real estate", {"FY2025": -417886}),
    ("DATA", "Securities purchased under reverse repurchase agreements", {"FY2025": -74193}),
    ("DATA", "Other assets", {"FY2025": -2105, "FY2024": 925, "FY2023": -138, "FY2022": 2191, "FY2021": -1514}),
    ("DATA", "Derivative financial instruments", {"FY2025": 1143, "FY2024": 3254, "FY2023": -4188, "FY2022": 275, "FY2021": 5137}),
    ("DATA", "Deposits from banks and financial institutions",
     {"FY2025": 156470, "FY2024": -46485, "FY2023": -34466, "FY2022": 46741, "FY2021": 61095}),
    ("DATA", "Deposits from customers", {"FY2025": 64775, "FY2024": 263683, "FY2023": 105052, "FY2022": 84485, "FY2021": -5338}),
    ("DATA", "Other liabilities", {"FY2025": -22811, "FY2024": 22284, "FY2023": -3379, "FY2022": 2767, "FY2021": 3871}),
    ("DATA", "Taxation paid", {"FY2025": -4547, "FY2024": -4688, "FY2023": -6300, "FY2022": -3140, "FY2021": -1945}),
    ("TOTAL", "Net cash generated from/(used in) operating activities",
     {"FY2025": -224043, "FY2024": 57743, "FY2023": 91802, "FY2022": 130869, "FY2021": -35992}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of investment securities", {"FY2025": -302813, "FY2024": -200801, "FY2023": -226418}),
    ("DATA", "Sales/maturities of investment securities", {"FY2025": 205903, "FY2024": 209476, "FY2023": 189530}),
    ("DATA", "Net sales of investment securities", {"FY2022": 7253, "FY2021": 46245}),
    ("DATA", "Purchase of property and equipment", {"FY2025": -354, "FY2024": -1826, "FY2023": -1828, "FY2022": -29430, "FY2021": -40}),
    ("DATA", "Investment in intangible assets", {"FY2025": -1163, "FY2024": -1167, "FY2023": -1321, "FY2022": -966, "FY2021": -548}),
    ("TOTAL", "Net cash generated from/(used in) investing activities",
     {"FY2025": -98427, "FY2024": 5682, "FY2023": -40037, "FY2022": -23143, "FY2021": 45657}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Redemption of sukuk funding", {"FY2021": -146944}),
    ("DATA", "Financing from banks", {"FY2025": 95247, "FY2024": 80776}),
    ("DATA", "Payment of principal in respect of leases", {"FY2025": -435, "FY2024": -325, "FY2023": -1260, "FY2022": -1019, "FY2021": -1318}),
    ("DATA", "Payment of financing in respect of leases", {"FY2025": -25, "FY2024": -27, "FY2023": -33, "FY2022": -116, "FY2021": -194}),
    ("DATA", "Payment of Additional Tier 1 Financing profit", {"FY2025": -377, "FY2024": -282, "FY2023": -281, "FY2022": -843}),
    ("DATA", "Payment of subordinated funding / profit on subordinated funding", {"FY2025": -23618, "FY2024": -2000, "FY2023": -2000}),
    ("TOTAL", "Net cash generated from/(used in) financing activities",
     {"FY2025": 70792, "FY2024": 78142, "FY2023": -3574, "FY2022": -1978, "FY2021": -148456}),
    ("TOTAL", "Net change in cash and cash equivalents",
     {"FY2025": -251678, "FY2024": 141567, "FY2023": 48191, "FY2022": 105748, "FY2021": -138791}),
    ("DATA", "Foreign exchange gain/(loss)", {"FY2025": 4, "FY2024": -274, "FY2023": -266, "FY2022": -10, "FY2021": -354}),
    ("DATA", "Opening cash and cash equivalents", {"FY2025": 539046, "FY2024": 397753, "FY2023": 349828, "FY2022": 244090, "FY2021": 383234}),
    ("TOTAL", "Closing cash and cash equivalents",
     {"FY2025": 287372, "FY2024": 539046, "FY2023": 397753, "FY2022": 349828, "FY2021": 244090}),
]

bw.add_cash_flow_sheet(
    title="Alrayan Bank Limited — Statement of Cash Flows",
    subtitle="Bank entity-level basis, £'000s. Full 5 years, no cash-flow exemption.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else "", rows_data, sources_text,
                         note=note, first_col_width=52, source_height=200)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2024": 208.2, "FY2023": 183.9, "FY2022": 152.7, "FY2021": 142.4})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2024": "15.95%", "FY2023": "17.36%", "FY2022": "14.93%", "FY2021": "15.1%"})],
    p3_sources("FY2021 is from the pre-KM1 Executive Summary table (rounded to 1dp in the source); FY2022-FY2024 "
               "are from the formal KM1 Annex template (2dp)."),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2024": 211.2, "FY2023": 186.9, "FY2022": 155.7, "FY2021": 145.4})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2024": "16.15%", "FY2023": "17.65%", "FY2022": "15.23%", "FY2021": "15.4%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2024": 224.9, "FY2023": 205.5, "FY2022": 178.4, "FY2021": 170.4})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2024": "17.19%", "FY2023": "19.41%", "FY2022": "17.45%", "FY2021": "18.1%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets", {"FY2024": 1307.8, "FY2023": 1059.1, "FY2022": 1022.3, "FY2021": 943.9})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2024": "7.7%", "FY2023": "7.8%", "FY2022": "6.7%", "FY2021": "6.4%"})],
    p3_sources(),
    note="FY2022-FY2024 are on the 'excluding claims on central banks' KM1 basis; FY2021 (6.4%) is on the older "
         "CRR/LRSum basis, from before the PRA's leverage-framework methodology change (PRA PS21/21) - not "
         "directly comparable, same industry-wide basis break documented for several other banks in this project.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (12-month average, KM1 basis)",
      {"FY2024": "523%", "FY2023": "641%", "FY2022": "442%", "FY2021": "316%"})],
    p3_sources(),
    note="This bank's Pillar 3 documents disclose TWO different LCR figures each year: a spot/point-in-time "
         "figure in the Executive Summary (FY2021 635%, FY2022 458%, FY2023 786%, FY2024 746% - none of these "
         "used here) and a 12-month AVERAGE figure in the formal KM1/Annex template (used here, for consistency "
         "with every other bank in this project and the standard regulatory template). FY2021's average figure "
         "comes from a dedicated 'Analysis of the Bank's average liquidity coverage ratio' table rather than a "
         "KM1 template (that edition pre-dates the bank's KM1 adoption).",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {"FY2024": "161%", "FY2023": "157%", "FY2022": "155%", "FY2021": "146%"})],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "MREL is not mentioned anywhere in the FY2023 or FY2024 Pillar 3 Disclosures (searched "
                      "directly, no hits) - consistent with a bank of this size not being its own resolution "
                      "entity under the Bank of England's MREL framework.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities",
         {"FY2025": -224043, "FY2024": 57743, "FY2023": 91802, "FY2022": 130869, "FY2021": -35992}),
        ("Net cash from/(used in) investing activities",
         {"FY2025": -98427, "FY2024": 5682, "FY2023": -40037, "FY2022": -23143, "FY2021": 45657}),
        ("Net cash from/(used in) financing activities",
         {"FY2025": 70792, "FY2024": 78142, "FY2023": -3574, "FY2022": -1978, "FY2021": -148456}),
        ("Closing cash and cash equivalents",
         {"FY2025": 287372, "FY2024": 539046, "FY2023": 397753, "FY2022": 349828, "FY2021": 244090}),
    ],
    cash_flow_unit="£'000s",
    ratios=[
        ("CET1 Ratio", {"FY2024": "15.95%", "FY2023": "17.36%", "FY2022": "14.93%", "FY2021": "15.1%"}),
        ("Tier 1 Ratio", {"FY2024": "16.15%", "FY2023": "17.65%", "FY2022": "15.23%", "FY2021": "15.4%"}),
        ("Total Capital Ratio", {"FY2024": "17.19%", "FY2023": "19.41%", "FY2022": "17.45%", "FY2021": "18.1%"}),
        ("Leverage Ratio", {"FY2024": "7.7%", "FY2023": "7.8%", "FY2022": "6.7%", "FY2021": "6.4%"}),
        ("LCR", {"FY2024": "523%", "FY2023": "641%", "FY2022": "442%", "FY2021": "316%"}),
        ("NSFR", {"FY2024": "161%", "FY2023": "157%", "FY2022": "155%", "FY2021": "146%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Pillar 3 ratios are blank for FY2025 (no disclosure published "
         "yet). LCR uses the 12-month average/KM1 basis throughout, not the spot figures also disclosed in this "
         "bank's own Executive Summary tables - see the LCR sheet's note.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ALRAYAN BANK FINANCIALS.xlsx")
