import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

CH2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00819519/filing-history/MzUyMzkzMjQ5NmFkaXF6a2N4/document?format=pdf&download=0"
CH2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00819519/filing-history/MzQyMzk5NjI0NGFkaXF6a2N4/document?format=pdf&download=0"
CH2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00819519/filing-history/MzM0MTEwODM3MmFkaXF6a2N4/document?format=pdf&download=0"

P3_2024_URL = "https://www.arbuthnotlatham.co.uk/sites/default/files/documents/abg-pillar-3-disclosures-december-24.pdf"
P3_2023_URL = "https://www.arbuthnotlatham.co.uk/sites/default/files/documents/ABG_Pillar_3_Disclosures_2023_Final.pdf"
P3_2022_URL = "https://www.arbuthnotlatham.co.uk/sites/default/files/documents/ABG_Pillar_3_Disclosures_2022_Final.pdf"
P3_2021_URL = "https://www.arbuthnotlatham.co.uk/sites/default/files/documents/ABG_Pillar_3_Disclosures_2021_Annual.pdf"

ENTITY_NOTE = (
    "Entity note: Arbuthnot Latham & Co., Limited (company 00819519, FRN 143336) is the PRA-authorised Bank "
    "itself, not the wider LSE-listed ultimate holding company Arbuthnot Banking Group PLC. The Bank files its "
    "own 'Group of companies' accounts' at Companies House (Arbuthnot Latham & Co., Limited and its own "
    "subsidiaries - Wealth Management, Asset Finance, Asset Based Lending and Commercial Vehicle Finance), which "
    "is the basis used for the cash flow statement here. The Bank's Annual Report also states its own 'Group Key "
    "Metrics' (e.g. FY2024 Tier 1 capital ratio 13.3%, Total capital ratio 15.4%, LCR 179%), which differ "
    "slightly from the formal Pillar 3 disclosures published under the Arbuthnot Banking Group PLC name (FY2024 "
    "CET1/Tier 1 ratio 13.15%, Total capital ratio 15.28%, LCR 175%) - the Pillar 3 sheets in this workbook use "
    "the formal ABG PLC Pillar 3 (Article 447 CRR) disclosures, since that is the entity's actual published "
    "Pillar 3 document; the small basis difference vs. the Bank's own Annual Report figures is not explained in "
    "either source and is flagged here rather than silently blended."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Arbuthnot Latham & Co., Limited's own Consolidated Statement of Cash Flows "
    "(the Bank + its own subsidiaries), £'000, as filed at Companies House:\n"
    f"FY2025 & FY2024: accounts made up to 31 December 2025, p.41 (Consolidated Statement of Cash Flows) - {CH2025_URL}\n"
    f"FY2023 & FY2022: accounts made up to 31 December 2023, p.42 (Consolidated Statement of Cash Flows) - {CH2023_URL}\n"
    f"FY2021 (& FY2020 comparative, not used): accounts made up to 31 December 2021, p.48 (Consolidated Statement "
    f"of Cash Flows) - {CH2021_URL}\n"
    "Presentation note: FY2021's own report builds the operating-profit-before-changes subtotal from actual cash "
    "interest/fee/payment flows (Interest received, Interest paid, Fees and commissions received, Other income, "
    "Cash payments to employees and suppliers, Taxation paid); FY2022 onward builds the same subtotal indirectly "
    "from Profit before tax plus non-cash adjustments (Depreciation, Impairment, Net interest expense, FX "
    "elimination on debt securities, Other non-cash items, Tax paid/expense). Both bases reconcile to a "
    "consistent, comparable 'Cash flows from operating profit before changes in operating assets and liabilities' "
    "subtotal each year - blank cells simply mean that year's report used the other presentation. FY2025's "
    "investing-activities total has an immaterial £1k rounding gap vs. the sum of its own printed line items, "
    "kept as printed rather than force-corrected. Every other section total and the full opening/closing cash "
    "chain reconciles exactly year-to-year across all 3 source documents.\n"
    + ENTITY_NOTE
)


def p3_sources(page_24="6", page_23="6", page_22="6", page_21="31"):
    return (
        "Sources - Arbuthnot Banking Group PLC Pillar 3 disclosures (UK KM1 Key Metrics template; FY2021 uses the "
        "pre-KM1 'Key Regulatory Metrics' template), £'000 unless stated:\n"
        f"FY2024 & FY2023 comparative: Pillar 3 disclosures for the year ended 31 December 2024, p.{page_24} (Template UK KM1) - {P3_2024_URL}\n"
        f"FY2023 (own year) & FY2022 comparative: Pillar 3 disclosures for the year ended 31 December 2023, p.{page_23} (Template UK KM1) - {P3_2023_URL}\n"
        f"FY2022 (own year) & FY2021 comparative: Pillar 3 disclosures for the year ended 31 December 2022, p.{page_22} (Template UK KM1) - {P3_2022_URL}\n"
        f"FY2021 (own year): Pillar 3 disclosures for the year ended 31 December 2021, p.{page_21} (Key Regulatory Metrics) - {P3_2021_URL}\n"
        "FY2025 Pillar 3 disclosures have not been published yet (checked against the site's naming pattern from "
        "prior years; none found) - FY2025 is left blank on every Pillar 3 sheet rather than guessed.\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Arbuthnot Latham & Co., Limited", years=YEARS, header_color="4E3B31")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 24184, "FY2024": 35091, "FY2023": 47117, "FY2022": 20009}),
    ("DATA", "Interest received", {"FY2021": 77319}),
    ("DATA", "Interest paid", {"FY2021": -11752}),
    ("DATA", "Fees and commissions received", {"FY2021": 15579}),
    ("DATA", "Other income", {"FY2021": 4402}),
    ("DATA", "Cash payments to employees and suppliers", {"FY2021": -59153}),
    ("DATA", "Taxation paid", {"FY2021": 0}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 10674, "FY2024": 11691, "FY2023": 9817, "FY2022": 7180}),
    ("DATA", "Impairment loss on loans and advances", {"FY2025": 1576, "FY2024": 4778, "FY2023": 208, "FY2022": 214}),
    ("DATA", "Net interest expense", {"FY2025": 3203, "FY2024": 598, "FY2023": 564, "FY2022": 70}),
    ("DATA", "Elimination of exchange differences on debt securities", {"FY2025": 11337, "FY2024": -3157, "FY2023": 8712, "FY2022": -9524}),
    ("DATA", "Other non-cash or non-operating items included in profit before tax", {"FY2025": 3402, "FY2024": -73, "FY2023": 31, "FY2022": -276}),
    ("DATA", "Tax paid/(expense)", {"FY2025": -6690, "FY2024": -4150, "FY2023": -8433, "FY2022": -2146}),
    ("TOTAL", "Cash flows from operating profit before changes in operating assets and liabilities", {"FY2025": 47686, "FY2024": 44778, "FY2023": 58016, "FY2022": 15527, "FY2021": 26395}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Net decrease/(increase) in derivative financial instruments", {"FY2025": 1572, "FY2024": 212, "FY2023": 3005, "FY2022": -4605, "FY2021": -388}),
    ("DATA", "Net decrease/(increase) in loans and advances to customers", {"FY2025": 132098, "FY2024": -34748, "FY2023": -16886, "FY2022": -165331, "FY2021": -284871}),
    ("DATA", "Net decrease/(increase) in assets held for leasing", {"FY2025": 721, "FY2024": -18474, "FY2023": -95960, "FY2022": -50175}),
    ("DATA", "Net increase/(decrease) in other assets", {"FY2025": 1447, "FY2024": 12828, "FY2023": -4063, "FY2022": 57955, "FY2021": -12558}),
    ("DATA", "Net increase in amounts due to customers", {"FY2025": 441708, "FY2024": 373207, "FY2023": 647721, "FY2022": 255529, "FY2021": 465088}),
    ("DATA", "Net increase/(decrease) in other liabilities", {"FY2025": 5211, "FY2024": -3369, "FY2023": 18490, "FY2022": 4593, "FY2021": 12651}),
    ("TOTAL", "Net cash inflow from operating activities", {"FY2025": 630443, "FY2024": 374434, "FY2023": 610323, "FY2022": 113493, "FY2021": 206317}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisition of financial investments", {"FY2025": -131, "FY2024": -215, "FY2023": -174, "FY2022": -53}),
    ("DATA", "Disposal of financial investments", {"FY2025": 2958, "FY2024": 84, "FY2023": 63, "FY2022": 640, "FY2021": 2400}),
    ("DATA", "Purchase of subsidiary undertakings", {"FY2021": -9998}),
    ("DATA", "Purchase of intangible assets / computer software", {"FY2025": -6425, "FY2024": -4739, "FY2023": -1523, "FY2022": -5837, "FY2021": -5100}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -985, "FY2024": -22808, "FY2023": -4611, "FY2022": -1065, "FY2021": -172915}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2021": 48255}),
    ("DATA", "Disposal of assets held for sale", {"FY2021": 149}),
    ("DATA", "Purchase of debt securities", {"FY2025": -3273055, "FY2024": -1621196, "FY2023": -1582889, "FY2022": -799341, "FY2021": -590492}),
    ("DATA", "Proceeds from redemption of debt securities", {"FY2025": 2428998, "FY2024": 1366350, "FY2023": 1071232, "FY2022": 670164, "FY2021": 635155}),
    ("DATA", "Dividends received", {"FY2025": 18}),
    ("TOTAL", "Net cash outflow from investing activities", {"FY2025": -848623, "FY2024": -282524, "FY2023": -517902, "FY2022": -135492, "FY2021": -92546}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "(Decrease)/increase in borrowings", {"FY2025": -191522, "FY2024": -530, "FY2023": -29489, "FY2022": -4306, "FY2021": 10243}),
    ("DATA", "Dividends paid", {"FY2025": -13347, "FY2024": -16260, "FY2023": -6855, "FY2022": -5850, "FY2021": -5550}),
    ("DATA", "Capital contribution received", {"FY2023": 5000, "FY2021": 25500}),
    ("DATA", "Repayment of lease liabilities", {"FY2025": -763, "FY2024": -2202, "FY2023": -3653, "FY2022": -7458, "FY2021": -2893}),
    ("TOTAL", "Net cash (outflow)/inflow from financing activities", {"FY2025": -205632, "FY2024": -18992, "FY2023": -34997, "FY2022": -17614, "FY2021": 27300}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -423812, "FY2024": 72918, "FY2023": 57424, "FY2022": -39613, "FY2021": 141071}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 978851, "FY2024": 905933, "FY2023": 848509, "FY2022": 888122, "FY2021": 747051}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 555039, "FY2024": 978851, "FY2023": 905933, "FY2022": 848509, "FY2021": 888122}),
]

bw.add_cash_flow_sheet(
    title="Arbuthnot Latham & Co., Limited — Consolidated Cash Flow Statement",
    subtitle="Arbuthnot Latham & Co., Limited Group (consolidated basis), £'000",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Arbuthnot Banking Group PLC (Pillar 3) basis, {unit}" if unit else "Arbuthnot Banking Group PLC (Pillar 3) basis",
                         rows_data, sources_text, note=note, first_col_width=46, source_height=140)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2024": 234477, "FY2023": 222291, "FY2022": 175375, "FY2021": 176235})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2024": "13.15%", "FY2023": "12.98%", "FY2022": "11.57%", "FY2021": "12.3%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2024": 234477, "FY2023": 222291, "FY2022": 175375, "FY2021": 176235})],
    p3_sources(),
    note="Equal to CET1 capital every year - no AT1 instruments in issue.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2024": "13.15%", "FY2023": "12.98%", "FY2022": "11.57%", "FY2021": "12.3%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2024": 272459, "FY2023": 260017, "FY2022": 212969, "FY2021": 213007})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2024": "15.28%", "FY2023": "15.18%", "FY2022": "14.05%", "FY2021": "14.9%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2024": 1782645, "FY2023": 1713146, "FY2022": 1516141, "FY2021": 1427724})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2024": 3828489, "FY2023": 3559597, "FY2022": 2923193}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2024": "6.12%", "FY2023": "6.24%", "FY2022": "6.00%"}),
        ("Total Basel III leverage ratio measure (FY2021 basis, includes claims on central banks)", {"FY2021": 3409123}),
        ("Basel III leverage ratio (%) (FY2021 basis)", {"FY2021": "5.2%"}),
    ],
    p3_sources(),
    note="The 'excluding claims on central banks' leverage framework took effect from 1 January 2022 (per the "
         "FY2022 Pillar 3 report itself); FY2021 is shown on its own report's 'Basel III leverage ratio' basis "
         "(includes claims on central banks) as a separate row rather than blended with the later basis.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value", {"FY2024": 1275612, "FY2023": 1046604, "FY2022": 710180, "FY2021": 897493}),
        ("Total net cash outflows, adjusted value", {"FY2024": 730580, "FY2023": 476548, "FY2022": 405819, "FY2021": 487009}),
        ("Liquidity Coverage Ratio (%)", {"FY2024": "175%", "FY2023": "220%", "FY2022": "175%", "FY2021": "184.3%"}),
    ],
    p3_sources(),
    note="FY2021 figures are from the FY2021 report's own 'Key Regulatory Metrics' table (pre-KM1 format). The "
         "FY2022 Pillar 3 report's own Dec-2021 comparative column instead shows HQLA £776,633k, net cash "
         "outflows £354,918k and LCR 219% for the same date - a real discrepancy between the two vintages' own "
         "figures, not resolved in either source. The FY2021 standalone figure is used here as the year's own "
         "original disclosure; the later restated comparative is flagged here rather than silently substituted.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2024": 2995437, "FY2023": 2784678, "FY2022": 2464147, "FY2021": 2389237}),
        ("Total required stable funding", {"FY2024": 2274318, "FY2023": 2043499, "FY2022": 1940538, "FY2021": 1794905}),
        ("NSFR ratio (%)", {"FY2024": "132%", "FY2023": "136%", "FY2022": "127%", "FY2021": "133.1%"}),
    ],
    p3_sources(),
    note="FY2021 is from the FY2021 report's own table; the UK NSFR regime's KM1 disclosure only became a formal "
         "requirement from 1 January 2022, so the FY2022 Pillar 3 report's KM1 template carries no FY2021 "
         "comparative for this line (marked 'NA' in that document) even though FY2021's own report did disclose "
         "a figure.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL disclosure found in any of the 4 available Pillar 3 reports (FY2021-FY2024) - Arbuthnot Banking "
         "Group is not designated as a resolution entity subject to MREL reporting at this level.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash inflow from operating activities", {"FY2025": 630443, "FY2024": 374434, "FY2023": 610323, "FY2022": 113493, "FY2021": 206317}),
        ("Net cash outflow from investing activities", {"FY2025": -848623, "FY2024": -282524, "FY2023": -517902, "FY2022": -135492, "FY2021": -92546}),
        ("Net cash (outflow)/inflow from financing activities", {"FY2025": -205632, "FY2024": -18992, "FY2023": -34997, "FY2022": -17614, "FY2021": 27300}),
        ("Cash and cash equivalents at 31 December", {"FY2025": 555039, "FY2024": 978851, "FY2023": 905933, "FY2022": 848509, "FY2021": 888122}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2024": "13.15%", "FY2023": "12.98%", "FY2022": "11.57%", "FY2021": "12.3%"}),
        ("Tier 1 Ratio", {"FY2024": "13.15%", "FY2023": "12.98%", "FY2022": "11.57%", "FY2021": "12.3%"}),
        ("Total Capital Ratio", {"FY2024": "15.28%", "FY2023": "15.18%", "FY2022": "14.05%", "FY2021": "14.9%"}),
        ("Leverage Ratio", {"FY2024": "6.12%", "FY2023": "6.24%", "FY2022": "6.00%", "FY2021": "5.2%"}),
        ("LCR", {"FY2024": "175%", "FY2023": "220%", "FY2022": "175%", "FY2021": "184.3%"}),
        ("NSFR", {"FY2024": "132%", "FY2023": "136%", "FY2022": "127%", "FY2021": "133.1%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Cash flow is the Bank's own Group basis (Companies "
         "House); Pillar 3 ratios are the Arbuthnot Banking Group PLC published Pillar 3 basis - see the entity "
         "note on the Cash Flow Statement sheet for the small scope difference between the two. FY2025 Pillar 3 "
         "is not yet published.",
)

bw.save("/Users/armaan/code/katalysis/banks/ARBUTHNOT LATHAM FINANCIALS.xlsx")
