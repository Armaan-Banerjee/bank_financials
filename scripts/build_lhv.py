import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# LHV Bank Limited was granted its (unrestricted) PRA banking licence on
# 3 May 2023 - its first Annual Report covers FY2023, so only 3 years of
# history exist (mirrors why Bank of London only had 4 - too young for 5).
YEARS = ["FY2025", "FY2024", "FY2023"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://framerusercontent.com/assets/ZBWKLmRUPe8T4hKrOicG3V2KYeE.pdf"
AR2024_URL = "https://framerusercontent.com/assets/srilZFyKHEx1zeu697l5ZFVMXoU.pdf"
AR2023_URL = "https://framerusercontent.com/assets/6Jp4ZWQKQVS1wXUDoBneovYKzIo.pdf"
P3_2025_URL = "https://framerusercontent.com/assets/xqUVp5XxVe8i90y3LAxlQmmQg.pdf"
P3_2024_URL = "https://framerusercontent.com/assets/OJpwHIE7Kzeo65KeJdj7ZrJGUk.pdf"
P3_2023_URL = "https://framerusercontent.com/assets/5YzVUZr8JQg4njsGLzu4ZBXBs8.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: LHV Bank Limited (Companies House 13180211, FRN 993767) is a UK bank owned by AS LHV Group "
    "(Estonia), incorporated 4 February 2021 and granted an unrestricted PRA banking licence on 3 May 2023 - its "
    "first Annual Report and Pillar 3 disclosure cover FY2023, so only 3 years of history exist (too young for 5). "
    "As at 31 December 2025 it is classified as an 'other institution' (not Small and Non-Complex, not Large) under "
    "Article 433 of the PRA Rulebook's Disclosure Part, requiring a reduced annual-only Pillar 3 disclosure with no "
    "KM2/MREL template - consistent with no MREL figures appearing in any year's Pillar 3 report."
)

DATA_ERROR_NOTE = (
    "DATA ERROR NOTE: LHV Bank Limited's own FY2024 Annual Report (p.55) prints 'Net Increase in cash and cash "
    "equivalents' for FY2024 as (199,190,949) - this does not reconcile with that same report's own opening "
    "(242,124,881) and closing (362,299,484) balances, nor with the sum of its own three activity subtotals "
    "(101,379,183 - 1,059,316 + 19,854,736 = 120,174,603). This workbook uses the correct, reconciling figure "
    "(120,174,603, i.e. £120,175k), which independently matches both the opening/closing balance difference and "
    "the FY2025 Annual Report's own restated FY2024 comparative (£120,175k, p.67) - not the erroneous figure as "
    "printed in the FY2024 report itself."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are LHV Bank Limited's own Statement of Cash Flows, £'000 (FY2023/FY2024 as originally "
    "reported in whole £, divided by 1,000 here for unit consistency with FY2025's own £'000 presentation):\n"
    f"FY2025: LHV Bank Limited Annual Report 2025, p.67 (Statement of cash flows) - {AR2025_URL}\n"
    f"FY2024: LHV Bank Limited Annual Report and Financial Statements 2024, p.55 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: LHV Bank Limited Annual Report and Financial Statements 2023, p.31 (Statement of Cash Flows) - {AR2023_URL}\n"
    "Note: FY2025's report uses a simplified presentation ('Non-cash items' and 'Changes in operating assets and "
    "liabilities' as single combined lines); FY2023/FY2024 break these out into more granular line items instead - "
    "each year's own line items/labels are preserved as reported, blank where a year didn't disclose that split. "
    "FY2023's own report did not print a combined 'Net cash from operating activities' total (only three "
    "un-combined subsection subtotals) - the total shown here for FY2023 is computed as the sum of its own "
    "operating-activity line items, and is confirmed exactly by its appearance as FY2024's report's own FY2023 "
    "comparative (224,565,739).\n\n"
    + ENTITY_NOTE + "\n\n" + DATA_ERROR_NOTE
)


def p3_sources():
    return (
        "Sources - LHV Bank Limited's own Pillar 3 disclosures (solo basis), £'000:\n"
        f"FY2025: LHV Bank Limited Pillar 3 Disclosures 2025, p.6-7 (3.1.2 Template UK KM1 - Key metrics) - {P3_2025_URL}\n"
        f"FY2024: LHV Bank Limited Pillar 3 Disclosures 2024, p.11 (Key metrics) - {P3_2024_URL}\n"
        f"FY2023: LHV Bank Limited Pillar 3 Disclosures 2023, p.12 (Key metrics) - {P3_2023_URL}\n"
        "Each year's figures are confirmed by their exact appearance as the following year's comparative column, "
        "where shown."
    )


bw = BankWorkbook(bank_name="LHV Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="5C2751")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit for the year before taxation", {"FY2025": 6766, "FY2024": 4044.276, "FY2023": 4779.563}),
    ("DATA", "Non-cash items (combined, as reported)", {"FY2025": 4064}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2024": 1091.16, "FY2023": 1596.396}),
    ("DATA", "Share based payments", {"FY2024": 638.961, "FY2023": 334.11}),
    ("DATA", "Foreign exchange translation differences", {"FY2024": 101.96}),
    ("DATA", "Credit impairment losses/(gains)", {"FY2024": 411.671, "FY2023": 149.876}),
    ("DATA", "Increase/(decrease) in other assets/other liabilities (combined, as reported)", {"FY2023": 2716.589}),
    ("DATA", "Changes in operating assets and liabilities (combined, as reported)", {"FY2025": 147815}),
    ("DATA", "(Increase)/decrease in operating assets", {"FY2024": -3353.822}),
    ("DATA", "(Increase)/decrease in operating liabilities", {"FY2024": -1200.156}),
    ("DATA", "Tax paid", {"FY2025": -1125, "FY2024": -278.181}),
    ("DATA", "Net loans and advances to customers", {"FY2024": -219442.236, "FY2023": -49482.095}),
    ("DATA", "Net deposits from customers", {"FY2024": 376838.55, "FY2023": 206998.301}),
    ("DATA", "Facilities/amounts received from/(to) group companies", {"FY2024": -57472.999, "FY2023": 57472.999}),
    ("TOTAL", "Net cash generated from operating activities", {"FY2025": 157520, "FY2024": 101379.183, "FY2023": 224565.739}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2023": -1079.751}),
    ("DATA", "Acquisition of property, plant & equipment and intangibles (combined, as reported)", {"FY2024": -1059.316}),
    ("DATA", "Purchase and development of intangible assets", {"FY2025": -325}),
    ("DATA", "Banking Services business transfer", {"FY2023": -1724.857}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {"FY2025": -325, "FY2024": -1059.316, "FY2023": -2804.607}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue and allotment of share capital / shares issued", {"FY2025": 30000, "FY2024": 20900, "FY2023": 10000}),
    ("DATA", "Proceeds from issuance of subordinated liabilities", {"FY2025": 10000}),
    ("DATA", "Payment of lease liabilities", {"FY2025": -1010, "FY2024": -1045.264, "FY2023": -1287.675}),
    ("TOTAL", "Net cash generated from financing activities", {"FY2025": 38990, "FY2024": 19854.736, "FY2023": 8712.325}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 196185, "FY2024": 120174.603, "FY2023": 230473.456}),
    ("DATA", "Cash and cash equivalents at start of year", {"FY2025": 362299, "FY2024": 242124.881, "FY2023": 11651.425}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 558485, "FY2024": 362299.484, "FY2023": 242124.881}),
]

bw.add_cash_flow_sheet(
    title="LHV Bank Limited — Statement of Cash Flows",
    subtitle="Solo basis, £'000 unless stated. See source note at bottom (incl. a known FY2024 report error).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Solo basis, {unit}" if unit else "Solo basis",
                         rows_data, p3_sources(), note=note, first_col_width=46, source_height=120)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 103888, "FY2024": 68399, "FY2023": 44532})],
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common equity Tier 1 capital ratio", {"FY2025": "18.5%", "FY2024": "24.1%", "FY2023": "31.7%"})],
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 103888, "FY2024": 68399, "FY2023": 44532})],
    note="Equal to CET1 capital in every year shown - LHV Bank has no Additional Tier 1 (AT1) instruments.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 capital ratio", {"FY2025": "18.5%", "FY2024": "24.1%", "FY2023": "31.7%"})],
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 113921, "FY2024": 68399, "FY2023": 44532})],
    note="Exceeds Tier 1 capital from FY2025 onward following issuance of £10,000k of subordinated (Tier 2) "
         "liabilities during the year (see Cash Flow Statement sheet) - equal to CET1/Tier 1 capital in FY2023 "
         "and FY2024, before that issuance.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "20.3%", "FY2024": "24.1%", "FY2023": "31.7%"})],
)

metric(
    "Total RWAs", "£'000",
    [("Total risk weighted exposure amount", {"FY2025": 561468, "FY2024": 284276, "FY2023": 140702})],
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims made on central banks", {"FY2025": 721124, "FY2024": 317763, "FY2023": 79084}),
        ("Leverage ratio excluding claims made on central banks (%)", {"FY2025": "14.4%", "FY2024": "21.5%", "FY2023": "56.3%"}),
    ],
    note="FY2023's very high ratio (56.3%) reflects the bank's small, deposit/capital-heavy balance sheet shortly "
         "after launch (unrestricted licence granted 3 May 2023), not a transcription error - it fell sharply as "
         "the loan book scaled in FY2024/FY2025.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total HQLA", {"FY2025": 405138, "FY2024": 296989, "FY2023": 137258}),
        ("Total net cash outflows", {"FY2025": 205363, "FY2024": 171530, "FY2023": 103776}),
        ("Liquidity coverage ratio (%)", {"FY2025": "196%", "FY2024": "175%", "FY2023": "133%"}),
    ],
    note="FY2023's LCR/NSFR are averages over 3 May 2023 (authorisation) to 31 December 2023 only, not a full "
         "12-month average like FY2024/FY2025.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available funding", {"FY2025": 802886, "FY2024": 372192, "FY2023": 144797}),
        ("Total required funding", {"FY2025": 441159, "FY2024": 153881, "FY2023": 51410}),
        ("Net stable funding ratio (%)", {"FY2025": "182%", "FY2024": "260%", "FY2023": "278%"}),
    ],
    note="FY2023's NSFR is an average over 3 May 2023 (authorisation) to 31 December 2023 only, not a full "
         "12-month average like FY2024/FY2025.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not applicable" for y in YEARS})],
    note="LHV Bank Limited is classified as an 'other institution' (not Large, not subject to LREQ/G-SII/O-SII "
         "status) under Article 433 of the PRA Rulebook's Disclosure Part as at 31 December 2025, requiring only "
         "reduced annual Pillar 3 disclosure with no UK KM2/MREL template - no MREL figure of any kind appears in "
         "any year's Pillar 3 report.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 157520, "FY2024": 101379.183, "FY2023": 224565.739}),
        ("Net cash from/(used in) investing activities", {"FY2025": -325, "FY2024": -1059.316, "FY2023": -2804.607}),
        ("Net cash from/(used in) financing activities", {"FY2025": 38990, "FY2024": 19854.736, "FY2023": 8712.325}),
        ("Cash and cash equivalents at end of year", {"FY2025": 558485, "FY2024": 362299.484, "FY2023": 242124.881}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "18.5%", "FY2024": "24.1%", "FY2023": "31.7%"}),
        ("Tier 1 Ratio", {"FY2025": "18.5%", "FY2024": "24.1%", "FY2023": "31.7%"}),
        ("Total Capital Ratio", {"FY2025": "20.3%", "FY2024": "24.1%", "FY2023": "31.7%"}),
        ("Leverage Ratio", {"FY2025": "14.4%", "FY2024": "21.5%", "FY2023": "56.3%"}),
        ("LCR", {"FY2025": "196%", "FY2024": "175%", "FY2023": "133%"}),
        ("NSFR", {"FY2025": "182%", "FY2024": "260%", "FY2023": "278%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Only 3 years shown - LHV Bank Limited was granted its PRA "
         "banking licence on 3 May 2023, so no earlier trading history exists. FY2024 cash flow uses a corrected "
         "'Net increase in cash' figure - see the Cash Flow Statement sheet's DATA ERROR NOTE.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/LHV FINANCIALS.xlsx")
