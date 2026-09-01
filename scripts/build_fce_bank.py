import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

# Companies House filing history, company 00772784 (FCE Bank Plc)
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzUxMTcwMTU1NGFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzQ2MTUzNDU1OGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzQxNTY0NTE3NGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_AMENDED_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzM5ODE1MjYzNmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzMzMzk0NjU4NWFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "FCE Bank Plc (company 00772784) is the UK-regulated captive auto-finance bank for Ford "
    "Motor Company's European operations (vehicle financing/leasing across Ford's European "
    "markets, not just the UK). Does NOT take the FRS 101/102 cash-flow exemption - full "
    "Group-basis Statement of Cash Flows every year. All 5 Companies House filings are fully "
    "scanned/image-only (0 text blocks/page); every figure was transcribed via page rendering.\n"
    "FY2022's accounts were AMENDED (30 Oct 2023, replacing the original 24 Mar 2023 filing) - "
    "the amended FY2022 figures were used as the operative record for that year, since this is "
    "the entity's own correction to its own year's accounts (not a later year's restatement). "
    "Confirmed the amended FY2022 figures are internally consistent with how FY2023's own report "
    "later carries them forward as its FY2022 comparative - no discrepancy found.\n"
    "FY2024's cash and cash equivalents at end of year include a genuine, disclosed "
    "'Cash and cash equivalents in respect of discontinued operations' adjustment of £(873)m "
    "(Group basis) - a real disposal/discontinuation event that year, not a data error; kept as "
    "the entity's own disclosed reconciling item, not silently absorbed elsewhere.\n"
    "FY2021's own Statement of Cash Flows classifies 'Net cash inflow/(outflow) on derivative "
    "financial instruments', 'Increase in restricted cash', and 'Decrease in restricted cash' "
    "under Financing activities (Group: £44m/£(97)m/£463m respectively, p.49); FY2022 onward "
    "reclassify these same three items under Investing activities instead. Confirmed via direct "
    "page image (p.49) - each year's own reported section placement is used, not forced into a "
    "single consistent classification across the 5 years."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are FCE Bank Plc's own consolidated (Group) Statement of Cash Flows, "
    "each year's own originally-published figures (not a later year's restated comparative):\n"
    f"FY2025: Annual Report 2025, p.53 (Statements of Cash Flows) - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.58 (Statements of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, p.55 (Statements of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022 (AMENDED filing, 30 Oct 2023), p.53 (Statements of Cash Flows) - {AR2022_AMENDED_URL}\n"
    f"FY2021: Annual Report 2021, p.49 (Statements of Cash Flow) - {AR2021_URL}\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - FCE Bank Plc Pillar 3 / capital basis, Group/Consolidated:\n"
        f"FY2021-FY2025 Tier 1 Capital, Tier 2 Capital and Total Capital Ratio: Annual Report 2025, "
        f"p.5 ('Business Performance' - 'Total Capital' chart, values to the nearest £0.1bn) - {AR2025_URL}\n"
        "FY2021 CET1/Tier 1 Capital (exact, £2,684m) and Leverage Ratio (16.95%): Annual Report 2021, "
        f"'Pillar 3 Disclosures' Table 2 (p.135) and Table 19 (p.155) - {AR2021_URL}\n"
        "CET1 = Tier 1 Capital every year (confirmed via the FY2021 Pillar 3 Own Funds reconciliation - "
        "no Additional Tier 1 instruments held).\n"
        "FY2022-FY2025 CET1/Tier 1 Capital and CET1/Tier 1 Ratio are CALCULATED, not directly disclosed: "
        "the Annual Report only publishes the rounded (nearest £0.1bn) Tier 1/Tier 2 chart and the "
        "Total Capital Ratio %; no standalone Pillar 3 document or CET1/Tier 1 Ratio % is published for "
        "these years (the dedicated 'Pillar 3 Disclosures' chapter present in the FY2021 report was "
        "dropped from FY2022 onward). Total RWAs is likewise calculated (Total Capital / Total Capital "
        "Ratio) for every year, since no year discloses RWA directly.\n"
        "Leverage Ratio, LCR, NSFR, MREL Ratio: not located for FY2022-FY2025 - no Pillar 3 chapter "
        "exists in those reports to check, and none of these appear in the Business Performance/Business "
        "Environment narrative sections reviewed.\n"
        + extra
    )


bw = BankWorkbook(bank_name="FCE Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="881D78")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (Group/Consolidated basis)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Cash from/(used in) operating activities",
     {"FY2025": 554, "FY2024": -1420, "FY2023": -1661, "FY2022": -1431, "FY2021": 2574}),
    ("DATA", "Interest paid",
     {"FY2025": -475, "FY2024": -672, "FY2023": -542, "FY2022": -177, "FY2021": -184}),
    ("DATA", "Interest received",
     {"FY2025": 926, "FY2024": 1160, "FY2023": 1071, "FY2022": 442, "FY2021": 836}),
    ("DATA", "Other operating income received",
     {"FY2025": 0, "FY2024": 48, "FY2023": 72, "FY2022": 26, "FY2021": 109}),
    ("DATA", "Income taxes paid",
     {"FY2025": -39, "FY2024": -51, "FY2023": -73, "FY2022": -133, "FY2021": -43}),
    ("TOTAL", "Net cash generated from/(used in) operating activities",
     {"FY2025": 966, "FY2024": -935, "FY2023": -1133, "FY2022": -1273, "FY2021": 3292}),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property and equipment",
     {"FY2025": -2, "FY2024": 0, "FY2023": -6, "FY2022": -6, "FY2021": -1}),
    ("DATA", "Proceeds from sale of property and equipment",
     {"FY2021": 6}),
    ("DATA", "Investment in internally and externally generated software",
     {"FY2025": -13, "FY2024": -19, "FY2023": -21, "FY2022": -15, "FY2021": -11}),
    ("DATA", "Net cash movement in sale of subsidiaries",
     {"FY2023": 0, "FY2022": -13}),
    ("DATA", "Net cash (outflow)/inflow on derivative financial instruments",
     {"FY2025": 2, "FY2024": 109, "FY2023": 165, "FY2022": 29}),
    ("DATA", "Increase in restricted cash",
     {"FY2025": -65, "FY2024": -61, "FY2023": -61, "FY2022": -73}),
    ("DATA", "Decrease in restricted cash",
     {"FY2025": 61, "FY2024": 84, "FY2023": 62, "FY2022": 63}),
    ("DATA", "Dividend from subsidiaries",
     {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Net cash (used in)/generated from investing activities",
     {"FY2025": -17, "FY2024": 113, "FY2023": 139, "FY2022": -15, "FY2021": -6}),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from the issue of debt securities and from loans provided by banks and other financial institutions",
     {"FY2025": 1001, "FY2024": 1642, "FY2023": 1311, "FY2022": 4482, "FY2021": 2972}),
    ("DATA", "Repayments of debt securities and of loans provided by banks and other financial institutions",
     {"FY2025": -797, "FY2024": -1790, "FY2023": -2022, "FY2022": -3861, "FY2021": -6212}),
    ("DATA", "Proceeds of funds provided by parent and related undertakings",
     {"FY2025": 211, "FY2024": 214, "FY2023": 698, "FY2022": 568, "FY2021": 398}),
    ("DATA", "Repayment of funds provided by parent and related undertakings",
     {"FY2025": -557, "FY2024": -485, "FY2023": -548, "FY2022": -480, "FY2021": -2614}),
    ("DATA", "Net (decrease)/increase in short-term borrowings",
     {"FY2025": -61, "FY2024": 343, "FY2023": -289, "FY2022": -168, "FY2021": 472}),
    ("DATA", "Net (decrease)/increase in deposits",
     {"FY2025": -408, "FY2024": 517, "FY2023": 1891, "FY2022": 2005, "FY2021": 1427}),
    ("DATA", "Net cash inflow/(outflow) on derivative financial instruments (FY2021 only - "
             "classified under Investing in later years' presentation, see ENTITY_NOTE)",
     {"FY2021": 44}),
    ("DATA", "Increase in restricted cash (FY2021 only - classified under Investing in later "
             "years' presentation)",
     {"FY2021": -97}),
    ("DATA", "Decrease in restricted cash (FY2021 only - classified under Investing in later "
             "years' presentation)",
     {"FY2021": 463}),
    ("DATA", "Dividend paid",
     {"FY2025": -500, "FY2024": 0, "FY2023": 0, "FY2022": -600, "FY2021": -300}),
    ("TOTAL", "Net cash (used in)/generated from financing activities",
     {"FY2025": -1111, "FY2024": 441, "FY2023": 1041, "FY2022": 1946, "FY2021": -3447}),

    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents",
     {"FY2025": -162, "FY2024": -381, "FY2023": 47, "FY2022": 658, "FY2021": -161}),
    ("DATA", "Cash and cash equivalents at beginning of year",
     {"FY2025": 1253, "FY2024": 2557, "FY2023": 2536, "FY2022": 1822, "FY2021": 2048}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents",
     {"FY2025": 20, "FY2024": -50, "FY2023": -26, "FY2022": 56, "FY2021": -65}),
    ("DATA", "Cash and cash equivalents in respect of discontinued operations",
     {"FY2024": -873}),
    ("TOTAL", "Cash and cash equivalents at end of year",
     {"FY2025": 1111, "FY2024": 1253, "FY2023": 2557, "FY2022": 2536, "FY2021": 1822}),
]

bw.add_cash_flow_sheet(
    title="FCE Bank Plc — Consolidated Statement of Cash Flows",
    subtitle="Group/Consolidated basis, £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=210,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=210)


CALC_NOTE = (
    "CALCULATED, not directly disclosed for FY2022-FY2025 (only the rounded nearest-£0.1bn chart "
    "value is published) - see the sheet's own source note for the exact FY2021 figure and full "
    "methodology."
)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital (= Tier 1 Capital, no AT1 instruments held)",
      {"FY2025": 1600, "FY2024": 1800, "FY2023": 2400, "FY2022": 2100, "FY2021": 2684})],
    note=CALC_NOTE,
)

metric(
    "CET1 Ratio", "%",
    [("CET1 Ratio (= Tier 1 Ratio, calculated as CET1 Capital / Total RWAs)",
      {"FY2025": "16.59%", "FY2024": "17.61%", "FY2023": "17.16%", "FY2022": "16.65%", "FY2021": "23.58%"})],
    note=CALC_NOTE + " FY2021 also independently cross-checked against the exact Pillar 3 Own Funds table.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital (= CET1, no AT1 instruments held)",
      {"FY2025": 1600, "FY2024": 1800, "FY2023": 2400, "FY2022": 2100, "FY2021": 2684})],
    note=CALC_NOTE,
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 Ratio (= CET1 Ratio, no AT1 instruments held)",
      {"FY2025": "16.59%", "FY2024": "17.61%", "FY2023": "17.16%", "FY2022": "16.65%", "FY2021": "23.58%"})],
    note=CALC_NOTE,
)

metric(
    "Total Capital", "£m",
    [("Total Capital (Tier 1 + Tier 2)",
      {"FY2025": 1800, "FY2024": 2000, "FY2023": 2700, "FY2022": 2400, "FY2021": 2994})],
    note="FY2022-FY2025 summed from the Annual Report's own rounded (nearest £0.1bn) Tier 1/Tier 2 "
         "chart. FY2021 exact from the Pillar 3 Own Funds tables (£2,684m CET1 + £310m Tier 2).",
)

metric(
    "Total Capital Ratio", "%",
    [("Total Capital / Total Risk-Weighted Exposure Amounts",
      {"FY2025": "18.66%", "FY2024": "19.57%", "FY2023": "19.30%", "FY2022": "19.03%", "FY2021": "26.20%"})],
    note="Directly disclosed every year in the Annual Report's own 'Business Performance' - 'Total "
         "Capital' chart, the only capital ratio consistently published across all 5 years.",
)

metric(
    "Total RWAs", "£m",
    [("Total Risk-Weighted Exposure Amounts",
      {"FY2025": 9646, "FY2024": 10220, "FY2023": 13990, "FY2022": 12612, "FY2021": 11450})],
    note="CALCULATED (Total Capital / Total Capital Ratio) - not directly disclosed in any year "
         "reviewed. Not independently cross-checked against a directly-disclosed RWA figure since "
         "none was found.",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage Ratio", {"FY2021": "16.95%"})],
    note="Only directly disclosed for FY2021, from the dedicated 'Pillar 3 Disclosures' chapter "
         "present in that year's Annual Report (Table 19, p.155) - this chapter was dropped from "
         "FY2022 onward, and no leverage ratio was found anywhere in the FY2022-FY2025 reports. "
         "Not calculated for those years since no leverage exposure measure is disclosed either.",
)

bw.add_not_disclosed_metric_sheets(
    ["LCR"],
    p3_sources(),
    per_note={
        "LCR": "Not publicly disclosed - no LCR reference found in any of the 5 Annual Reports "
               "reviewed, including the FY2021 Pillar 3 Disclosures chapter's own index of every "
               "CRR disclosure article it covers (no liquidity-ratio article listed at all). "
               "Plausibly reflects FCE Bank's captive auto-finance/wholesale-funded business model.",
    },
)

bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={
        "NSFR": "Not publicly disclosed - no NSFR reference found in any of the 5 Annual Reports "
                "reviewed, including the FY2021 Pillar 3 Disclosures chapter's own index of every "
                "CRR disclosure article it covers (no liquidity-ratio article listed at all).",
        "MREL Ratio": "Not publicly disclosed - no MREL reference found in any of the 5 Annual "
                      "Reports reviewed.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities",
         {"FY2025": 966, "FY2024": -935, "FY2023": -1133, "FY2022": -1273, "FY2021": 3292}),
        ("Net cash (used in)/generated from investing activities",
         {"FY2025": -17, "FY2024": 113, "FY2023": 139, "FY2022": -15, "FY2021": -6}),
        ("Net cash (used in)/generated from financing activities",
         {"FY2025": -1111, "FY2024": 441, "FY2023": 1041, "FY2022": 1946, "FY2021": -3447}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 1111, "FY2024": 1253, "FY2023": 2557, "FY2022": 2536, "FY2021": 1822}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.59%", "FY2024": "17.61%", "FY2023": "17.16%", "FY2022": "16.65%", "FY2021": "23.58%"}),
        ("Total Capital Ratio", {"FY2025": "18.66%", "FY2024": "19.57%", "FY2023": "19.30%", "FY2022": "19.03%", "FY2021": "26.20%"}),
        ("Leverage Ratio", {"FY2021": "16.95%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. CET1/Tier 1 Ratio and Total RWAs are calculated "
         "for FY2022-FY2025 (only the rounded Tier 1/Tier 2/Total Capital Ratio chart is published for "
         "those years) - see the individual metric sheets for the full methodology.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/FCE BANK FINANCIALS.xlsx")
