import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Full 5 years of cash flow AND Pillar 3 coverage FY2021-FY2025. No FRS 101/102
# cash-flow exemption at all - clean, active, well-documented UK subsidiary of
# Bank of Beirut SAL (Lebanon), unaffected in its own filings by the parent
# jurisdiction's banking crisis (confirmed active Companies House status,
# unqualified audit opinions, no going-concern language in any of the 5 reports).
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/04406777"
AR2025_URL = "https://www.bankofbeirut.co.uk/Content/uploads/AnnualReport/Annual_Report_and_Financial_Statements_2025_-_for_publishing.pdf"
AR2024_URL = "https://www.bankofbeirut.co.uk/Content/Uploads/AnnualReport/Annual%20Report%20and%20Financial%20Statements%202024%20-%20Final%20-%20for%20publishing250506021233950~.pdf"
AR2023_URL = "https://www.bankofbeirut.co.uk/Content/Uploads/AnnualReport/Annual%20Report%20and%20Financial%20Statements%202023%20-%20for%20publishing240429124230700~.pdf"
AR2021_URL = "https://www.bankofbeirut.co.uk/Content/uploads/AnnualReport/Bank_of_beirut_UK_Annual_Report_-_2021_.pdf"
P3_2025_URL = "https://www.bankofbeirut.co.uk/Content/uploads/PillarDisclosure/Bank_of_Beirut_UK_Ltd_-_Pillar_III_Disclosures_-_31_December_2025.pdf"
P3_2024_URL = "https://www.bankofbeirut.co.uk/Content/uploads/Announcement/bob-disclosures3-2024.pdf"
P3_2023_URL = "https://www.bankofbeirut.co.uk/Content/uploads/Announcement/Bank_of_Beirut_UK_Ltd_-_Pillar_III_Disclosures_-_31_December_2023.pdf"
P3_2022_URL = "https://www.bankofbeirut.co.uk/Content/uploads/Announcement/Bank_of_Beirut_UK_Ltd_-_Pillar_III_Disclosures_-_31DEC2022_-_Final.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank of Beirut (UK) Ltd (FRN 219523, Companies House 04406777, matches Banks List 2608.xlsx "
    "exactly) is a UK-incorporated subsidiary of Bank of Beirut SAL (Lebanon). Despite Lebanon's severe banking-"
    "sector crisis since 2019, this UK entity remains Active at Companies House with unqualified audit opinions "
    "and no going-concern qualification in any of the 5 Annual Reports reviewed (FY2021-FY2025) - the parent's "
    "distress has not visibly affected this subsidiary's own filings or capital position. Reports in GBP "
    "throughout, no FX conversion needed."
)

CASH_FLOW_SOURCES = (
    "Sources - Bank of Beirut (UK) Ltd's own Cash Flow Statement, converted from £ to £'000s (rounded), all years:\n"
    f"FY2025/FY2024: Annual Report and Financial Statements 2025, p.33 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.34 - {AR2023_URL}\n"
    f"FY2022: sourced from the Annual Report and Financial Statements 2023's own FY2022 comparative column, p.34 - "
    f"{AR2023_URL}\n"
    f"FY2021: Annual Report & Financial Statements 2021, p.31 - {AR2021_URL}\n"
    "GENUINE UNRESOLVED PRESENTATIONAL BREAK: FY2024's own report (Annual Report 2024, p.34/p.33 Balance Sheet) "
    "states 'Cash and balances at banks' at FY2024 year-end as £139,856,747, matching FY2023's own year-end "
    "figure of £97,312,901 as that year's opening balance - fully self-consistent. But the FY2025 report's own "
    "FY2024 comparative restates BOTH the FY2024 balance-sheet cash figure and the cash-flow opening balance to "
    "£276,517,994 - a £136.7m increase. Tracing this: the FY2025 report's FY2024 comparative 'Placements with "
    "banks' balance-sheet line also drops from its FY2024-report-original £139,666,071 to a restated £3,004,824 "
    "in the same amount as the cash increase (£139,666,071 - £3,004,824 = £136,661,247, matching the cash "
    "increase to the pound). This is evidence of a genuine reclassification - most of 'Placements with banks' "
    "moved into 'Cash and balances at banks' from FY2025 onward, with FY2024 restated for comparability - not an "
    "error. Per this project's convention, each column below keeps ITS OWN report's originally-published figures "
    "(FY2024 = £139,857k as originally stated, FY2025's own opening balance = £276,518k as its own report "
    "states) rather than force-blending the two; the reconciling difference is fully explained above, unlike the "
    "unexplained gap left at Arab Bank Europe.\n"
    "One immaterial £1k rounding artifact in the FY2021 report's own tail chain (kept as printed).\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Bank of Beirut (UK) Ltd's own Pillar 3 Disclosures, £m capital amounts / % ratios, all years:\n"
        f"FY2025: Pillar 3 Disclosures - 31 December 2025, s.3.6 Key Metrics (UK KM1 template) - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures - 31 December 2024, s.3.6 Key Metrics (UK KM1 template) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures - 31 December 2023, s.4.2 Key Metrics (UK KM1 template) - {P3_2023_URL}\n"
        f"FY2022: sourced from the FY2023 Pillar 3 Disclosures' own FY2022 KM1 comparative column - {P3_2023_URL}. "
        f"Capital £ figures independently cross-checked against the FY2022 Pillar 3 Disclosures' own 5-year ICAAP "
        f"summary table (s.4.1) - {P3_2022_URL} - and match to the pound (CET1 £103,161,031 both sources); that "
        f"document's TREA is on a different ICAAP basis (£314.6m) vs the KM1/COREP basis used here (£317.6m), a "
        f"~1% difference, KM1 basis used throughout for consistency with FY2023 onward.\n"
        f"FY2021: calculated from the FY2022 Pillar 3 Disclosures' own 5-year ICAAP summary table (s.4.1), which "
        f"predates this bank's adoption of the KM1 template - {P3_2022_URL}. CET1 = Own Funds Capital Resources "
        f"less Eligible Tier II Capital; ratios = £ amount / Total Risk Exposure Amount (Memo line), consistent "
        f"with this project's convention of calculating a ratio from disclosed £ figures where no % is directly "
        f"stated (see Bank of Ireland UK). No Leverage/LCR/NSFR/MREL numeric figures exist in this pre-KM1 "
        f"document (narrative KPI list only, no values) - left blank rather than guessed.\n"
        "No document at any year mentions MREL.\n"
        + (extra + "\n" if extra else "")
        + "\n" + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Bank of Beirut (UK) Ltd", years=YEARS, year_label=YEAR_LABEL, header_color="6B4226")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit for the year", {"FY2025": 7597, "FY2024": 9670, "FY2023": 8899, "FY2022": 3976, "FY2021": 1420}),
    ("DATA", "Taxation", {"FY2025": 2586, "FY2024": 3283, "FY2023": 2838, "FY2022": 980, "FY2021": 737}),
    ("DATA", "Treasury Bills discount and interest", {"FY2025": -233, "FY2024": -277, "FY2023": 594, "FY2022": 0}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 1004, "FY2024": 834, "FY2023": 750, "FY2022": 642, "FY2021": 809}),
    ("DATA", "Impairment reversal/(losses) on financial assets", {"FY2025": -368, "FY2024": -241, "FY2023": 736, "FY2022": 2669, "FY2021": 297}),
    ("DATA", "Finance cost on lease liabilities", {"FY2025": 23, "FY2024": 83, "FY2023": 32, "FY2022": 38, "FY2021": 43}),
    ("DATA", "Interest income", {"FY2025": -22273, "FY2024": -23830}),
    ("DATA", "Interest expense", {"FY2025": 6352, "FY2024": 5875}),
    ("TOTAL", "Operating cash flows before movements in working capital", {"FY2025": -5312, "FY2024": -4603, "FY2023": 13849, "FY2022": 8304, "FY2021": 3306}),
    ("DATA", "Increase/(Decrease) in prepayments and accrued income", {"FY2025": -337, "FY2024": -497, "FY2023": 104, "FY2022": -178, "FY2021": -181}),
    ("DATA", "(Decrease)/Increase in accruals and deferred income", {"FY2025": -347, "FY2024": -170, "FY2023": 303, "FY2022": -31, "FY2021": 263}),
    ("DATA", "Net Increase/(Decrease) in loans and advances to banks and customers", {"FY2025": -24435, "FY2024": -54985, "FY2023": 39905, "FY2022": -27093, "FY2021": 24313}),
    ("DATA", "(Decrease)/Increase in deposits by banks and customer accounts", {"FY2025": 24806, "FY2024": 103729, "FY2023": -29538, "FY2022": -6085, "FY2021": -11002}),
    ("DATA", "(Decrease)/Increase in other liabilities", {"FY2025": -8938, "FY2024": 10394, "FY2023": -69, "FY2022": 299, "FY2021": -1363}),
    ("DATA", "Net (Decrease)/Increase in derivative financial instruments", {"FY2025": -145, "FY2024": 192, "FY2023": -65, "FY2022": 17}),
    ("DATA", "Interest income received", {"FY2025": 23318, "FY2024": 23628}),
    ("DATA", "Interest expense paid", {"FY2025": -6569, "FY2024": -6056}),
    ("DATA", "Corporation tax paid", {"FY2025": -2571, "FY2024": -4710, "FY2023": -1828, "FY2022": -356, "FY2021": -295}),
    ("TOTAL", "Net cash (used in)/generated from operating activities", {"FY2025": -529, "FY2024": 121755, "FY2023": 22662, "FY2022": -25122, "FY2021": 15041}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, equipment and intangible assets", {"FY2025": -3860, "FY2024": -1906, "FY2023": -355, "FY2022": -769, "FY2021": -128}),
    ("DATA", "Proceeds on maturity of treasury bills and other eligible bills", {"FY2025": 340419, "FY2024": 107809, "FY2023": 43930, "FY2022": 39572, "FY2021": 30077}),
    ("DATA", "Purchase of treasury bills and other eligible bills", {"FY2025": -355953, "FY2024": -125744, "FY2023": -49034, "FY2022": -45974, "FY2021": -29631}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {"FY2025": -19394, "FY2024": -19841, "FY2023": -5459, "FY2022": -7171, "FY2021": 318}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Lease payments under Finance Lease", {"FY2025": -156, "FY2024": -136, "FY2023": -148, "FY2022": -141, "FY2021": -148}),
    ("DATA", "Subordinated loan redemption", {"FY2023": -17408}),
    ("DATA", "Dividend paid", {"FY2025": -4835, "FY2024": -4450, "FY2023": -1988, "FY2022": -802}),
    ("TOTAL", "Net cash (used in)/generated from financing activities", {"FY2025": -4991, "FY2024": -4586, "FY2023": -19544, "FY2022": -944, "FY2021": -148}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -24915, "FY2024": 42879, "FY2023": -2340, "FY2022": -33237, "FY2021": 15211}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 276518, "FY2024": 97313, "FY2023": 97866, "FY2022": 134557, "FY2021": 118590}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents", {"FY2025": 3169, "FY2024": -335, "FY2023": 1787, "FY2022": -3454, "FY2021": 755}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 254772, "FY2024": 139857, "FY2023": 97313, "FY2022": 97866, "FY2021": 134557}),
]

bw.add_cash_flow_sheet(
    title="Bank of Beirut (UK) Ltd — Cash Flow Statement",
    subtitle="Entity-level basis, £'000s (converted from source £). Full 5 years, no cash-flow exemption.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=300,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else "", rows_data, sources_text,
                         note=note, first_col_width=52, source_height=220)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 110.6, "FY2024": 109.0, "FY2023": 105.8, "FY2022": 103.2, "FY2021": 104.0})],
    p3_sources(),
    note="FY2021 is calculated (Own Funds less Eligible Tier II Capital from the pre-KM1 ICAAP table) - see source note.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2025": "37.49%", "FY2024": "43.57%", "FY2023": "42.56%", "FY2022": "32.49%", "FY2021": "35.14%"})],
    p3_sources(),
    note="FY2021 is calculated (CET1 £ / Total Risk Exposure Amount £, pre-KM1 ICAAP basis) rather than directly disclosed as a percentage.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 110.6, "FY2024": 109.0, "FY2023": 105.8, "FY2022": 103.2, "FY2021": 104.0})],
    p3_sources(),
    note="Tier 1 = CET1 every year (no AT1 instruments ever issued).",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "37.49%", "FY2024": "43.57%", "FY2023": "42.56%", "FY2022": "32.49%", "FY2021": "35.14%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 123.6, "FY2024": 124.9, "FY2023": 121.5, "FY2022": 133.8, "FY2021": 134.6})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "41.93%", "FY2024": "49.95%", "FY2023": "48.87%", "FY2022": "42.14%", "FY2021": "45.50%"})],
    p3_sources(),
    note="FY2021 is calculated (Total Capital £ / Total Risk Exposure Amount £, pre-KM1 ICAAP basis).",
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 294.9, "FY2024": 250.1, "FY2023": 248.5, "FY2022": 317.6, "FY2021": 295.9})],
    p3_sources(),
    note="FY2022 (£317.6m) is on the KM1/COREP basis; the same year's ICAAP-basis figure in the FY2022 Pillar 3 "
         "document's own 5-year table is £314.6m - a ~1% methodology difference, KM1 used for consistency with "
         "FY2023 onward. FY2021 (£295.9m) is on the older ICAAP basis only (no KM1 equivalent exists for that year).",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio excluding claims on central banks", {"FY2025": "20.42%", "FY2024": "21.19%", "FY2023": "26.38%", "FY2022": "22.88%"})],
    p3_sources(),
    note="Not disclosed for FY2021 - the pre-KM1 Pillar 3 document lists Leverage Ratio as a tracked KPI but "
         "states no numeric value for any year in that edition.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio", {"FY2025": "316.67%", "FY2024": "335.52%", "FY2023": "390.70%", "FY2022": "468.51%"})],
    p3_sources(),
    note="Not disclosed for FY2021 - see Leverage Ratio sheet note (same pre-KM1 document limitation).",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {"FY2025": "310.42%", "FY2024": "325.22%", "FY2023": "371.19%", "FY2022": "417.71%"})],
    p3_sources(),
    note="Not disclosed for FY2021 - see Leverage Ratio sheet note (same pre-KM1 document limitation).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "MREL is not mentioned anywhere in any of the 5 Pillar 3 Disclosures reviewed (searched "
                      "directly, no hits any year) - consistent with a bank of this size not being its own "
                      "resolution entity under the Bank of England's MREL framework.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash (used in)/generated from operating activities", {"FY2025": -529, "FY2024": 121755, "FY2023": 22662, "FY2022": -25122, "FY2021": 15041}),
        ("Net cash (used in)/generated from investing activities", {"FY2025": -19394, "FY2024": -19841, "FY2023": -5459, "FY2022": -7171, "FY2021": 318}),
        ("Net cash (used in)/generated from financing activities", {"FY2025": -4991, "FY2024": -4586, "FY2023": -19544, "FY2022": -944, "FY2021": -148}),
        ("Cash and cash equivalents at end of year", {"FY2025": 254772, "FY2024": 139857, "FY2023": 97313, "FY2022": 97866, "FY2021": 134557}),
    ],
    cash_flow_unit="£'000s",
    ratios=[
        ("CET1 Ratio", {"FY2025": "37.49%", "FY2024": "43.57%", "FY2023": "42.56%", "FY2022": "32.49%", "FY2021": "35.14%"}),
        ("Tier 1 Ratio", {"FY2025": "37.49%", "FY2024": "43.57%", "FY2023": "42.56%", "FY2022": "32.49%", "FY2021": "35.14%"}),
        ("Total Capital Ratio", {"FY2025": "41.93%", "FY2024": "49.95%", "FY2023": "48.87%", "FY2022": "42.14%", "FY2021": "45.50%"}),
        ("Leverage Ratio", {"FY2025": "20.42%", "FY2024": "21.19%", "FY2023": "26.38%", "FY2022": "22.88%"}),
        ("LCR", {"FY2025": "316.67%", "FY2024": "335.52%", "FY2023": "390.70%", "FY2022": "468.51%"}),
        ("NSFR", {"FY2025": "310.42%", "FY2024": "325.22%", "FY2023": "371.19%", "FY2022": "417.71%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Leverage/LCR/NSFR are blank for FY2021 (pre-KM1 "
         "disclosure with no numeric values published that year). Cash flow FY2024-FY2025 has a genuine, fully "
         "explained (not guessed) presentational break - see the Cash Flow Statement sheet's source note.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF BEIRUT UK FINANCIALS.xlsx")
print("Saved.")
