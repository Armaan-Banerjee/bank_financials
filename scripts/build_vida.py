import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Entity was named "Belmont Green Finance Limited" (trading as Vida/Vida
# Homeloans) through FY2023, renamed "Vida Bank Limited" on receiving its PRA
# banking licence 19 Nov 2024. FY2022 cash flow is a genuine gap - see
# ENTITY_NOTE. Pillar 3 only exists from FY2024 (first year as a bank).
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.vidabank.co.uk/media/pkmnxlqg/annual-report-and-accounts-2025-company.pdf"
AR2024_URL = "https://www.vidabank.co.uk/media/emghy4z2/annual-report-and-accounts-2024-company.pdf"
AR2023_URL = "https://www.vidabank.co.uk/media/zhoj0swe/annual-report-and-accounts-2023.pdf"
AR2021_URL = "https://www.vidabank.co.uk/media/p3wau0ms/annual-report-and-accounts-2021.pdf"

P3_2025_URL = "https://www.vidabank.co.uk/media/od2lpxc0/vghl-pillar-3-report-2025-final.pdf"
P3_2024_URL = "https://www.vidabank.co.uk/media/mucbqgwi/vghl-pillar-3-report-2024-final.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: the company (FRN 738741, Companies House 09837692) was named 'Belmont Green Finance Limited' "
    "(trading as Vida / Vida Homeloans) through its FY2023 Annual Report, and was renamed 'Vida Bank Limited' after "
    "receiving its PRA banking licence on 19 November 2024. This workbook uses 'Vida Bank Limited' throughout since "
    "that is its current name. Pre-authorisation (FY2021-FY2023), the business was funded mainly through mortgage "
    "securitisation (numerous 'Tower Bridge Funding' special-purpose vehicles) rather than retail deposits; the "
    "FY2023 Annual Report's own commentary describes the business as still 'preparing for the banking licence'. "
    "Cash flow figures below are on the Company's own (non-consolidated/solo) basis in every populated year - this "
    "is the only basis for which a full three-part cash flow statement (operating/investing/financing) could be "
    "found in every report; the Consolidated (Group) statement of financial position was reported each year, but "
    "the FY2022 and FY2023 Annual Reports' own primary financial statements do not include a full Group cash flow "
    "statement, only a partial 'Net cash flow from operating activities' reconciliation note (Note 25) on the Group "
    "basis - see FY2022_GAP_NOTE below."
)

FY2022_GAP_NOTE = (
    "FY2022 is blank on this sheet: neither the FY2022 nor FY2023 Annual Report presents a full three-part Company "
    f"cash flow statement for FY2022 (checked both directly - {AR2023_URL} - and via the FY2023 report's own prior-"
    "year comparative column, which is likewise not present.) The FY2023 Annual Report's Note 25 gives only a "
    "partial Group-basis operating reconciliation ending at 'Net cash flows from operating activities: £68,297k' "
    "for FY2022 - not on the same (Company) basis as every other populated year here and with no investing/"
    "financing breakdown at all, so it is not shown rather than presented as a misleadingly partial column."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Vida Bank Limited's own Company (non-consolidated) cash flow statement, £'000:\n"
    f"FY2025: Vida Bank Limited Annual Report and Accounts 2025 (Company), p.55 (Statement of Cash Flows) - "
    f"{AR2025_URL}\n"
    f"FY2024: Vida Bank Limited Annual Report and Accounts 2024 (Company), p.73 (Statement of Cash Flows) - "
    f"{AR2024_URL}\n"
    f"FY2023: taken from Vida Bank Limited's FY2024 Annual Report's own FY2023 comparative column (p.73, same "
    f"document as above) - Belmont Green Finance Limited's own FY2023 Annual Report does not present a comparable "
    f"Company-basis statement (see ENTITY_NOTE/FY2022_GAP_NOTE).\n"
    f"FY2021: Belmont Green Finance Limited (Vida) Annual Report and Accounts 2021, p.150 (Company Statement of "
    f"Cash Flows) - {AR2021_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + FY2022_GAP_NOTE
)


def p3_sources():
    return (
        "Sources - Vida Group Holdings Limited/plc Pillar 3 disclosures (Table 3.1 KM1 - Key Metrics; the smallest "
        "regulatory group Vida Bank Limited is consolidated into - no Vida-Bank-Limited-only Pillar 3 disclosure is "
        "separately published):\n"
        f"FY2025: Vida Group Holdings plc Pillar 3 Disclosures 2025, p.5 (3.1 Key Metrics / Table KM1) - {P3_2025_URL}\n"
        f"FY2024: Vida Group Holdings Limited Pillar 3 Disclosures 2024, p.5 (3.1 Key Metrics / Table KM1) - {P3_2024_URL}\n"
        "No Pillar 3 disclosure exists for FY2021-FY2023: Pillar 3 only applies once PRA-authorised as a deposit-"
        "taker, which happened 19 November 2024 (see ENTITY_NOTE on the Cash Flow Statement sheet)."
    )


bw = BankWorkbook(bank_name="Vida Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="6E2C00")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash flows from/(used in) operating activities", {"FY2025": 1766849, "FY2024": 70662, "FY2023": 65493, "FY2021": -179449}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -92, "FY2024": -57, "FY2023": -24, "FY2021": -190}),
    ("DATA", "Expenditure on software development", {"FY2025": -12, "FY2024": -351, "FY2023": -674, "FY2021": -1567}),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {"FY2025": -104, "FY2024": -408, "FY2023": -698, "FY2021": -1757}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from shares issued", {"FY2021": 8300}),
    ("DATA", "Movement of deemed loans due to Group undertakings", {"FY2025": -904243, "FY2024": 115457, "FY2023": -62096, "FY2021": 169705}),
    ("DATA", "Repayment of loans", {"FY2024": -25000}),
    ("DATA", "Issuance of Tier 2 subordinated liabilities", {"FY2025": 35000}),
    ("DATA", "Repayment of lease liabilities", {"FY2025": -479, "FY2024": -225, "FY2023": -446, "FY2021": -1407}),
    ("DATA", "Movement in debt securities", {"FY2025": -785634, "FY2024": -34135}),
    ("DATA", "Other movements", {"FY2025": 0, "FY2024": -27, "FY2023": -12}),
    ("TOTAL", "Net cash flows (used in)/generated from financing activities", {"FY2025": -1655356, "FY2024": 56070, "FY2023": -62554, "FY2021": 176598}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 111389, "FY2024": 126324, "FY2023": 2241, "FY2021": -4608}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 143485, "FY2024": 17161, "FY2023": 14920, "FY2021": 18108}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 254874, "FY2024": 143485, "FY2023": 17161, "FY2021": 13500}),
]

bw.add_cash_flow_sheet(
    title="Vida Bank Limited — Company Cash Flow Statement",
    subtitle="Company (non-consolidated) basis, £'000. FY2022 blank - see source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Vida Group Holdings basis, {unit}" if unit else "Vida Group Holdings basis",
                         rows_data, p3_sources(), note=note, first_col_width=48, source_height=130)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {"FY2025": 168319, "FY2024": 160316})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "15.2%", "FY2024": "16.2%"})])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {"FY2025": 168319, "FY2024": 160316})],
       note="Equal to CET1 capital in both years - Vida has no Additional Tier 1 (AT1) instruments.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "15.2%", "FY2024": "16.2%"})])
metric("Total Capital", "£'000", [("Total capital", {"FY2025": 202429, "FY2024": 160316})],
       note="FY2025 total capital exceeds Tier 1 capital because the Group issued £35m of qualifying Tier 2 capital "
            "during the year to support planned balance sheet expansion; FY2024 had no Tier 2 capital.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "18.3%", "FY2024": "16.2%"})])
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", {"FY2025": 1105780, "FY2024": 986809})])
metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 3440332, "FY2024": 2331835}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "4.9%", "FY2024": "6.9%"}),
    ],
)
metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 1073005, "FY2024": 167705}),
        ("Total net cash outflows, adjusted value", {"FY2025": 669438, "FY2024": 16046}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "163%", "FY2024": "1,045%"}),
    ],
    note="FY2024's very high LCR (1,045%) reflects a build-up of liquid assets immediately following PRA "
         "authorisation on 19 November 2024, per the Group's own Pillar 3 commentary.",
)
metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 2377496, "FY2024": 2016146}),
        ("Total required stable funding", {"FY2025": 1719626, "FY2024": 1830180}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "138%", "FY2024": "110%"}),
    ],
)
metric("MREL Ratio", None, [("MREL ratio", {y: "Not disclosed" for y in YEARS})],
       note="No MREL disclosure (numeric or qualitative) found in either Pillar 3 report - Vida is a small, "
            "recently-authorised bank and does not appear to be within scope of an MREL-above-minimum-capital "
            "requirement based on its own disclosures.")

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 1766849, "FY2024": 70662, "FY2023": 65493, "FY2021": -179449}),
        ("Net cash from/(used in) investing activities", {"FY2025": -104, "FY2024": -408, "FY2023": -698, "FY2021": -1757}),
        ("Net cash from/(used in) financing activities", {"FY2025": -1655356, "FY2024": 56070, "FY2023": -62554, "FY2021": 176598}),
        ("Cash and cash equivalents at end of year", {"FY2025": 254874, "FY2024": 143485, "FY2023": 17161, "FY2021": 13500}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.2%", "FY2024": "16.2%"}),
        ("Tier 1 Ratio", {"FY2025": "15.2%", "FY2024": "16.2%"}),
        ("Total Capital Ratio", {"FY2025": "18.3%", "FY2024": "16.2%"}),
        ("Leverage Ratio", {"FY2025": "4.9%", "FY2024": "6.9%"}),
        ("LCR", {"FY2025": "163%", "FY2024": "1,045%"}),
        ("NSFR", {"FY2025": "138%", "FY2024": "110%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. FY2022 cash flow and FY2021-FY2023 Pillar 3 are blank - Vida "
         "only became a PRA-authorised bank on 19 November 2024 (no Pillar 3 exists before then), and FY2022's own "
         "Annual Report doesn't present a full cash flow statement on a basis comparable to other years - see the "
         "Cash Flow Statement sheet's source note for details.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/VIDA FINANCIALS.xlsx")
