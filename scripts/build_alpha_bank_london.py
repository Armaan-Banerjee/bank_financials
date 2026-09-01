import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/00185070/filing-history"
AR25_URL = "https://find-and-update.company-information.service.gov.uk/company/00185070/filing-history/MzUyMzkyMTM5MGFkaXF6a2N4/document?format=pdf&download=0"
AR24_URL = "https://find-and-update.company-information.service.gov.uk/company/00185070/filing-history/MzQ2NDAyMTQ4MGFkaXF6a2N4/document?format=pdf&download=0"
AR22_URL = "https://find-and-update.company-information.service.gov.uk/company/00185070/filing-history/MzM3OTU0ODM0NWFkaXF6a2N4/document?format=pdf&download=0"

CASH_FLOW_SOURCES = (
    "Sources — Alpha Bank London Limited (FRN 135327, company 00185070) own Statement of Cash Flows, £000's:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 31 December 2025, p.25-26 (Statement of Cash Flows) — {AR25_URL}\n"
    f"FY2023 & FY2024 (cross-checked): Annual Report and Financial Statements 31 December 2024, p.26-27 (Statement of Cash Flows) — {AR24_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements 31 December 2022, p.22-23 (Statement of Cash Flows) — {AR22_URL}\n"
    "Filed accounts at Companies House are fully scanned/image-only (no text layer) for all 5 years — figures "
    "transcribed via OCR (tesseract) then manually cross-checked against a rendered page image. All figures GBP "
    "throughout (no FX conversion needed).\n"
    "PRESENTATION NOTE: the source restructures this statement across the 5 years. FY2021-FY2024 report an "
    "'adjustments' block (incl. accrued interest income/expense removed from profit) feeding an unlabelled interim "
    "subtotal, then separate blocks for changes in operating assets and operating liabilities, then a block adding "
    "back actual CASH interest received/paid, then tax paid, before the final 'Net cash flows used in operating "
    "activities' total. FY2025 drops both the interim subtotal and the separate cash-interest block entirely (cash "
    "interest is folded directly into the asset/liability movement figures) — cells left blank for FY2025 where "
    "FY2021-FY2024 show a value are genuinely not broken out that year, not a data gap. Section TOTALs (assets "
    "change, liabilities change, investing, financing, and the final operating/net-change/closing-balance figures) "
    "are fully consistent and comparable across all 5 years — verified by hand line-by-line; see "
    "scripts/verify_workbook.py's own docstring re: its known limitation on multi-block tail reconciliation, which "
    "applies here (it will only cleanly auto-check the asset-change and liability-change blocks).\n"
    "Two immaterial (£1k) accrued-vs-cash timing differences exist between the operating-adjustments block's accrued "
    "interest figures and the financing section's actual cash-paid interest figures for FY2023 (£669k accrued vs "
    "£668k paid) and FY2021 (£161k accrued vs £162k paid) — normal accrual/cash timing, not an error, both used "
    "exactly as each section states them.\n"
    "FY2023 investing-activities section: component lines sum to £16,147k but the source's own printed total reads "
    "£16,148k — an immaterial £1k rounding artifact in the original filing, kept as printed (not force-corrected)."
)

def p3_sources():
    return (
        "Sources — Alpha Bank London Limited's own Annual Report (no standalone Pillar 3 document is published; "
        "the Bank is below the threshold requiring one, disclosing capital/liquidity KPIs and a capital breakdown "
        "note within the Annual Report itself):\n"
        f"FY2025 & FY2024: Annual Report 2025, p.6 (Key Performance Indicators) and p.67 Note 34.7 (Capital "
        f"management, Regulatory analysis) — {AR25_URL}\n"
        f"FY2024 & FY2023: Annual Report 2024, p.6 (Key Performance Indicators) and p.68 Note 34.7 (Capital "
        f"management, Regulatory analysis) — {AR24_URL}\n"
        f"FY2022 & FY2021: Annual Report 2022, p.65 Note 34.6 (Capital management, Regulatory analysis) — {AR22_URL}\n"
        f"Companies House filing history — {CH_URL}\n"
        "DATA QUALITY NOTE: the FY2024 Annual Report's own Key Performance Indicators table (p.6) shows a "
        "'Total regulatory capital' line of £68.4m (FY2024) / £66.0m (FY2023) that does NOT match the same report's "
        "own Note 34.7 'Total regulatory capital' figure of £77,015k / £67,916k for the identical years. Comparing "
        "the KPI-table figures against Total Equity (share capital + retained earnings + FVTOCI reserve, i.e. "
        "Tier 1 before the intangible-assets deduction) shows they match almost exactly — the FY2025 Annual Report "
        "itself confirms this by renaming that same KPI line to 'Total equity' and dropping the 'Total regulatory "
        "capital' label entirely. This is treated as a labelling fix made in the FY2025 report rather than an "
        "arithmetic error: Note 34.7's fully itemised, internally-consistent regulatory-capital build-up (used "
        "throughout this workbook) is the correct regulatory figure in every year."
    )

bw = BankWorkbook(bank_name="Alpha Bank London Limited", years=YEARS, header_color="1D3557")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "(Loss)/profit before tax", {"FY2025": -1066, "FY2024": 3163, "FY2023": 8267, "FY2022": 4160, "FY2021": 1868}),
    ("DATA", "Interest income on investment securities", {"FY2025": -1367, "FY2024": -2894, "FY2023": -4042, "FY2022": -630, "FY2021": 248}),
    ("DATA", "Interest income on loans and advances to customers (accrued)", {"FY2024": -29603, "FY2023": -25319, "FY2022": -16874, "FY2021": -12771}),
    ("DATA", "Interest expense on due to banks (accrued)", {"FY2024": 0, "FY2023": 624, "FY2022": 2316, "FY2021": 1484}),
    ("DATA", "Interest expense on due to customers (accrued)", {"FY2024": 7547, "FY2023": 7383, "FY2022": 355, "FY2021": 144}),
    ("DATA", "Interest expense on debt securities in issue and other borrowed funds", {"FY2025": 690, "FY2024": 726, "FY2023": 669, "FY2022": 340, "FY2021": 207}),
    ("DATA", "Interest expense on lease liabilities", {"FY2025": 54, "FY2024": 139, "FY2023": 185, "FY2022": 138, "FY2021": 161}),
    ("DATA", "Gain/(loss) on forward revaluation of FX transactions", {"FY2025": -374, "FY2024": -60, "FY2023": 67, "FY2022": 340, "FY2021": 98}),
    ("DATA", "Gain on foreign exchange", {"FY2025": 49, "FY2024": -100, "FY2023": -96, "FY2022": -120, "FY2021": -143}),
    ("DATA", "(Loss)/gain from derecognition of investment securities", {"FY2025": -1, "FY2024": 28, "FY2023": 152, "FY2022": -206, "FY2021": 94}),
    ("DATA", "Movement in ECL allowance on investment securities", {"FY2025": 0, "FY2024": -5, "FY2023": -3, "FY2022": 3, "FY2021": -13}),
    ("DATA", "Movement in ECL allowance on loans and advances to customers", {"FY2025": 2, "FY2024": -1, "FY2023": -168, "FY2022": -254, "FY2021": -92}),
    ("DATA", "Movement in ECL allowance on undrawn commitments", {"FY2025": 1, "FY2024": -1}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 1230, "FY2024": 992, "FY2023": 1044, "FY2022": 1039, "FY2021": 1028}),
    ("DATA", "Provision", {"FY2023": 1, "FY2022": 0, "FY2021": 6}),
    ("TOTAL", "Cash flows before changes in operating assets/liabilities (as reported; not broken out FY2025)", {"FY2024": -20069, "FY2023": -11236, "FY2022": -9393, "FY2021": -7681}),

    ("SECTION", "Net increase/(decrease) in assets relating to operating activities", {}),
    ("DATA", "Derivative financial instruments", {"FY2025": 2605, "FY2024": -2523, "FY2023": 2916, "FY2022": -3261, "FY2021": 452}),
    ("DATA", "Investment securities", {"FY2025": 447, "FY2024": 8164, "FY2023": 1729, "FY2022": -5211, "FY2021": -3265}),
    ("DATA", "Loans and advances to customers", {"FY2025": -57033, "FY2024": -67368, "FY2023": -4461, "FY2022": 32615, "FY2021": -20115}),
    ("DATA", "Other assets", {"FY2025": -1364, "FY2024": -1057, "FY2023": 203, "FY2022": 213, "FY2021": 61}),
    ("TOTAL", "Total change in operating assets", {"FY2025": -55345, "FY2024": -62784, "FY2023": 387, "FY2022": 24356, "FY2021": -22867}),

    ("SECTION", "Net increase/(decrease) in liabilities relating to operating activities", {}),
    ("DATA", "Derivative financial instruments", {"FY2025": -106, "FY2024": -825, "FY2023": -119, "FY2022": -659, "FY2021": 523}),
    ("DATA", "Due to banks", {"FY2025": 5337, "FY2024": 1761, "FY2023": -6187, "FY2022": -23806, "FY2021": 27128}),
    ("DATA", "Due to customers", {"FY2025": 57757, "FY2024": 26848, "FY2023": -10414, "FY2022": -43423, "FY2021": -91738}),
    ("DATA", "Other borrowed funds", {"FY2025": 0, "FY2024": -2, "FY2023": 3, "FY2022": 2, "FY2021": 1}),
    ("DATA", "Other liabilities", {"FY2025": 517, "FY2024": 2481, "FY2023": 250, "FY2022": -1075, "FY2021": 1209}),
    ("TOTAL", "Total change in operating liabilities", {"FY2025": 63505, "FY2024": 30263, "FY2023": -16467, "FY2022": -68961, "FY2021": -62877}),

    ("SECTION", "Cash interest received/(paid) reconciliation (as reported; not broken out FY2025)", {}),
    ("DATA", "Interest income on loans and advances to customers (cash received)", {"FY2024": 29603, "FY2023": 25319, "FY2022": 16874, "FY2021": 12771}),
    ("DATA", "Interest expense on due to banks (cash paid)", {"FY2024": 0, "FY2023": -624, "FY2022": -2316, "FY2021": -1484}),
    ("DATA", "Interest expense on due to customers (cash paid)", {"FY2024": -7547, "FY2023": -7383, "FY2022": -355, "FY2021": -144}),
    ("TOTAL", "Total cash interest reconciliation", {"FY2024": 22056, "FY2023": 17312, "FY2022": 14203, "FY2021": 11143}),

    ("DATA", "Income tax paid", {"FY2025": -182, "FY2024": -836, "FY2023": -2022, "FY2022": -805, "FY2021": -482}),
    ("TOTAL", "Net cash flows used in operating activities", {"FY2025": 7196, "FY2024": -31370, "FY2023": -12026, "FY2022": -40650, "FY2021": -82764}),

    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisition of investment securities", {"FY2025": -102879, "FY2024": -32554, "FY2023": -44562, "FY2022": -97105, "FY2021": -62157}),
    ("DATA", "Disposal/maturity of investment securities", {"FY2025": 104753, "FY2024": 60257, "FY2023": 56786, "FY2022": 95910, "FY2021": 129499}),
    ("DATA", "Interest income/(expense) on investment securities", {"FY2025": 1367, "FY2024": 2894, "FY2023": 4042, "FY2022": 630, "FY2021": -248}),
    ("DATA", "Acquisition of fixed assets (including intangibles)", {"FY2025": -1916, "FY2024": -1398, "FY2023": -119, "FY2022": -9, "FY2021": -189}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": 1325, "FY2024": 29199, "FY2023": 16148, "FY2022": -574, "FY2021": 66905}),

    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of lease liabilities", {"FY2025": -858, "FY2024": -815, "FY2023": -800, "FY2022": -775, "FY2021": -725}),
    ("DATA", "Interest paid on other borrowed funds", {"FY2025": -690, "FY2024": -726, "FY2023": -668, "FY2022": -340, "FY2021": -207}),
    ("DATA", "Interest paid on lease liabilities", {"FY2025": -54, "FY2024": -139, "FY2023": -185, "FY2022": -138, "FY2021": -162}),
    ("TOTAL", "Net cash flows used in financing activities", {"FY2025": -1602, "FY2024": -1680, "FY2023": -1653, "FY2022": -1253, "FY2021": -1094}),

    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 6919, "FY2024": -3851, "FY2023": 2469, "FY2022": -42477, "FY2021": -16953}),
    ("DATA", "Cash and cash equivalents at beginning of the year", {"FY2025": 36967, "FY2024": 40658, "FY2023": 38160, "FY2022": 80857, "FY2021": 97765}),
    ("DATA", "Net effect of foreign exchange fluctuations", {"FY2025": 325, "FY2024": 160, "FY2023": 29, "FY2022": -220, "FY2021": 45}),
    ("TOTAL", "Cash and cash equivalents at end of the year", {"FY2025": 44211, "FY2024": 36967, "FY2023": 40658, "FY2022": 38160, "FY2021": 80857}),
]

bw.add_cash_flow_sheet(
    title="Alpha Bank London Limited — Cash Flow Statement",
    subtitle="Entity-level basis, £000's, FY2021-FY2025",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Entity-level basis, {unit}" if unit else "Entity-level basis",
                         rows_data, sources_text, note=note, first_col_width=46, source_height=110)

metric(
    "CET1 Capital", "£000's",
    [("Common Equity Tier 1 (CET1) capital = Total Tier 1 capital (no AT1 instruments)",
      {"FY2025": 64528, "FY2024": 67015, "FY2023": 65916, "FY2022": 59465, "FY2021": 56254})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {y: "Not separately disclosed" for y in YEARS})],
    p3_sources(),
    note="The source discloses only a single combined 'Capital adequacy ratio' (see Total Capital Ratio sheet), "
         "not separately-stated CET1/Tier 1/Total Capital ratios. Since Tier 2 capital (subordinated debt) is a "
         "material part of total regulatory capital in every year, a CET1-only ratio would differ measurably from "
         "the disclosed combined ratio — left blank rather than assume which capital measure the disclosed ratio "
         "uses.",
)

metric(
    "Tier 1 Capital", "£000's",
    [("Tier 1 capital (share capital, retained earnings, FVTOCI reserve, less intangible assets)",
      {"FY2025": 64528, "FY2024": 67015, "FY2023": 65916, "FY2022": 59465, "FY2021": 56254})],
    p3_sources(),
    note="No AT1 instruments in any year — Tier 1 = CET1.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {y: "Not separately disclosed" for y in YEARS})],
    p3_sources(),
    note="Same basis issue as the CET1 Ratio sheet — only a single combined 'Capital adequacy ratio' is disclosed.",
)

metric(
    "Total Capital", "£000's",
    [("Total regulatory capital (Tier 1 + Tier 2)",
      {"FY2025": 74528, "FY2024": 77015, "FY2023": 67916, "FY2022": 63465, "FY2021": 62254})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Capital adequacy ratio (as disclosed; source does not specify whether the numerator is Total Capital or "
      "Tier 1 only — treated as Total Capital ratio per standard Basel/PRA usage of this exact term)",
      {"FY2025": "20%", "FY2024": "23%", "FY2023": "25%"})],
    p3_sources(),
    note="Not disclosed at all for FY2021/FY2022 — the Annual Report's KPI table for those years lists only "
         "Profit before tax, Total equity, and Return on equity; the Capital adequacy/LCR/Leverage ratio KPI trio "
         "was introduced from the FY2023 report onward.",
)

metric(
    "Total RWAs", "£000's",
    [("Total risk-weighted assets (calculated: Total Capital ÷ Capital adequacy ratio, as reported)",
      {"FY2025": 372640, "FY2024": 334848, "FY2023": 271664})],
    p3_sources(),
    note="Not directly disclosed any year — calculated from the two most literal disclosed figures for the years "
         "the capital adequacy ratio exists (FY2023-FY2025). Not calculable for FY2021/FY2022 since no ratio is "
         "disclosed for those years either.",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2025": "11%", "FY2024": "13%", "FY2023": "13%"})],
    p3_sources(),
    note="Not disclosed for FY2021/FY2022 (same KPI-table introduction timing as the Total Capital Ratio sheet). "
         "No exposure-measure £ figure is disclosed alongside the ratio in any year.",
)

metric(
    "LCR", "%",
    [("Liquidity coverage ratio", {"FY2025": "310%", "FY2024": "323%", "FY2023": "349%"})],
    p3_sources(),
    note="Not disclosed for FY2021/FY2022 (same KPI-table introduction timing as the other ratio sheets).",
)

bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={
        "NSFR": "Not disclosed in any of the 5 years reviewed — no NSFR figure or qualitative statement found in "
                "any Annual Report, including the years the LCR/leverage/capital-adequacy KPI trio was introduced.",
        "MREL Ratio": "Not disclosed in any of the 5 years reviewed, and no explicit exemption statement found "
                      "either — plausibly reflects the Bank's small balance sheet size sitting below the threshold "
                      "requiring a stated MREL requirement, but this is not confirmed by the source.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": 7196, "FY2024": -31370, "FY2023": -12026, "FY2022": -40650, "FY2021": -82764}),
        ("Net cash from investing activities", {"FY2025": 1325, "FY2024": 29199, "FY2023": 16148, "FY2022": -574, "FY2021": 66905}),
        ("Net cash from financing activities", {"FY2025": -1602, "FY2024": -1680, "FY2023": -1653, "FY2022": -1253, "FY2021": -1094}),
        ("Cash and cash equivalents at end of year", {"FY2025": 44211, "FY2024": 36967, "FY2023": 40658, "FY2022": 38160, "FY2021": 80857}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("Total Capital Ratio", {"FY2025": "20%", "FY2024": "23%", "FY2023": "25%"}),
        ("Leverage Ratio", {"FY2025": "11%", "FY2024": "13%", "FY2023": "13%"}),
        ("LCR", {"FY2025": "310%", "FY2024": "323%", "FY2023": "349%"}),
    ],
    note="CET1/Tier 1 ratios not shown here — only a single combined 'Capital adequacy ratio' is disclosed by this "
         "bank (see the Total Capital Ratio sheet's note). No ratios of any kind disclosed for FY2021/FY2022. "
         "Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page.",
)

bw.save("/Users/armaan/code/katalysis/banks/ALPHA BANK LONDON FINANCIALS.xlsx")
print("Saved ALPHA BANK LONDON FINANCIALS.xlsx")
