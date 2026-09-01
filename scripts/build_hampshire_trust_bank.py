import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzUyMTMxMjk3OWFkaXF6a2N4/document?format=pdf&download=0"
AR2025_WEBSITE_URL = "https://www.htb.co.uk/htbcontent/uploads/2026/04/HTB_Annual_Report_2025.pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzQ2NTc0NTU3N2FkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzQyNDU2MzAzMmFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzM4ODU3ODUzOWFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzM0MjI1MzEyMmFkaXF6a2N4/document?format=pdf&download=0"

P3_2025_URL = "https://www.htb.co.uk/htbcontent/uploads/2026/04/HTB_Pillar_3_Disclosures_2025.pdf"
P3_2024_URL = "https://www.htb.co.uk/htbcontent/uploads/2025/07/HTB_Pillar_3_Disclosures_2024.pdf"
P3_2023_URL = "https://www.htb.co.uk/htbcontent/uploads/2024/06/HTB_Pillar_3_Disclosures_2023.pdf"
P3_2022_URL = "https://www.htb.co.uk/htbcontent/uploads/2023/08/Hampshire-Trust-Bank-HTB-2022-Pillar-3-Disclosures.pdf"
P3_2021_URL = "https://www.htb.co.uk/htbcontent/uploads/2022/07/Hampshire-Trust-Bank-HTB-2021-Pillar-3-Disclosures.pdf"

ENTITY_NOTE = (
    "All Cash Flow Statement figures use the Bank (parent-entity, non-consolidated) column, matching the "
    "entity-level basis of the Pillar 3 disclosures below. HTB's FY2021 Annual Report predates any Group "
    "consolidation (its first subsidiary was acquired during FY2022, see the Investing Activities section), "
    "so FY2021 presents a single unified Company statement rather than separate Group/Bank columns - that "
    "single column is used here. The FY2025 Companies House filing (the source used for every other year) is "
    "missing page 64 of its own PDF (the Statement of Cash Flows' operating-activities page - printed page "
    "numbers jump 63 to 65 with no page 64 present in the scan); the operating-activities detail for FY2025 "
    "was instead sourced from the identical statement in HTB's own website copy of the same Annual Report, "
    "which is text-native and paginates differently. Every other line item and every other year comes from "
    "the Companies House filings."
)

CASH_FLOW_SOURCES = (
    "Sources - Hampshire Trust Bank Plc's own Consolidated and Bank Statement of Cash Flows (Bank column):\n"
    f"FY2025: Group Annual Report and Accounts 2025 (Companies House, filed 13 May 2026), p.64-65 - {AR2025_URL}\n"
    f"  (operating-activities section from HTB's own website copy of the same report, p.32 - {AR2025_WEBSITE_URL})\n"
    f"FY2024: Annual Report and Accounts for the year ended 31 December 2024 (Companies House, filed 13 May 2025), p.74-75 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts for the year ended 31 December 2023 (Companies House, filed 11 Jun 2024), p.74-75 (FY2023 comparative column) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts for the year ended 31 December 2022 (Companies House, filed 07 Aug 2023), p.61-62 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Accounts for the year ended 31 December 2021 (Companies House, filed 14 Jun 2022), p.54, Statement of Cash flows - {AR2021_URL}\n"
    + ENTITY_NOTE
)


def p3_sources(km1_page="10-11"):
    return (
        "Sources - Hampshire Trust Bank Plc Pillar 3 Disclosures, 'Key Metrics' (KM1) table, Bank column "
        "(Group column used only for LCR/NSFR, which HTB discloses only at consolidated/Group level - 'Liquidity "
        "is managed on a consolidated basis hence only Group metrics are reported'; FY2021's Pillar 3 report "
        "predates the Group/Bank split entirely and shows a single value used for every metric that year):\n"
        f"FY2025: Pillar 3 Disclosures | 31 December 2025, p.{km1_page} - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures | 31 December 2024, p.9-10 - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures | 31 December 2023, p.10-11 - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures | 31 December 2022, p.10-11 - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures | 31 December 2021, Key Metrics table - {P3_2021_URL}\n"
        "MREL is not mentioned anywhere in any year's Pillar 3 disclosure - not publicly disclosed."
    )


bw = BankWorkbook(bank_name="Hampshire Trust Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="DD741F")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (Bank / entity-level column)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax for the year", {
        "FY2025": 78521, "FY2024": 72461, "FY2023": 80407, "FY2022": 64521, "FY2021": 27346,
    }),
    ("DATA", "Depreciation and amortisation", {
        "FY2025": 6963, "FY2024": 5800, "FY2023": 4936, "FY2022": 4411, "FY2021": 3936,
    }),
    ("DATA", "Loss on disposal of fixed assets", {
        "FY2023": 503,
    }),
    ("DATA", "Impairment loss on investment in subsidiaries", {
        "FY2025": 26500, "FY2024": 11219,
    }),
    ("DATA", "Foreign exchange gains/(losses)", {
        "FY2025": -29, "FY2022": -2, "FY2021": 9,
    }),
    ("DATA", "Gain on securitisation", {
        "FY2024": -10414,
    }),
    ("DATA", "Increase in impairment of loans and advances", {
        "FY2025": 10147, "FY2024": 8939, "FY2023": 7183, "FY2022": 11995, "FY2021": 6362,
    }),
    ("DATA", "Increase/(decrease) in provisions", {
        "FY2025": 1831, "FY2024": 1364, "FY2023": 6036, "FY2022": 3215, "FY2021": -4206,
    }),
    ("DATA", "Equity-settled share-based payment transactions", {
        "FY2025": 718, "FY2024": -204, "FY2023": 1399, "FY2022": 240, "FY2021": 676,
    }),
    ("DATA", "Bond premium/discount amortisation", {
        "FY2025": 157, "FY2024": -1943, "FY2023": -4943, "FY2022": -335, "FY2021": 1275,
    }),
    ("DATA", "Decrease/(increase) in fair value of derivative assets", {
        "FY2025": 30481, "FY2024": 18609, "FY2023": 41007, "FY2022": -76695, "FY2021": -28408,
    }),
    ("DATA", "Increase/(decrease) in fair value of loans and advances designated as hedged items", {
        "FY2025": -32163, "FY2024": -19784, "FY2023": -39698, "FY2022": 73530, "FY2021": 25595,
    }),
    ("DATA", "Decrease/(increase) in fair value of loans and advances held at FVTPL", {
        "FY2025": 188, "FY2024": -53, "FY2023": 1436, "FY2022": -6981, "FY2021": -749,
    }),
    ("DATA", "Repayment of the interest accrued on lease liabilities", {
        "FY2025": 228, "FY2024": 258, "FY2023": 142, "FY2022": 70, "FY2021": -129,
    }),
    ("DATA", "Dividends received", {
        "FY2025": -26500, "FY2024": -11000, "FY2023": -27500, "FY2022": -20000,
    }),
    ("DATA", "Other acquisition costs recognised through equity", {
        "FY2022": -392,
    }),
    ("DATA", "Corporation tax paid", {
        "FY2025": -21655, "FY2024": -18086, "FY2023": -15835, "FY2022": -14257, "FY2021": -3709,
    }),
    ("DATA", "Corporation tax received", {
        "FY2025": 1166,
    }),
    ("DATA", "(Increase) in loans and advances to customers", {
        "FY2025": -1121847, "FY2024": -717726, "FY2023": -675670, "FY2022": -625569, "FY2021": -419379,
    }),
    ("DATA", "(Increase)/decrease in other assets", {
        "FY2025": 61605, "FY2024": 6841, "FY2023": -169564, "FY2022": -94775, "FY2021": -508,
    }),
    ("DATA", "(Decrease)/increase in central bank facilities", {
        "FY2025": -5000, "FY2024": -5000, "FY2023": 5000, "FY2021": 115000,
    }),
    ("DATA", "(Increase)/decrease in collateral held with banks", {
        "FY2025": -30078, "FY2024": -25256, "FY2023": -33646, "FY2022": 73421, "FY2021": 27594,
    }),
    ("DATA", "Increase in customer deposits", {
        "FY2025": 702733, "FY2024": 1324101, "FY2023": 765355, "FY2022": 798748, "FY2021": 512682,
    }),
    ("DATA", "Increase/(decrease) in subordinated and other liabilities", {
        "FY2025": -12373, "FY2024": -20701, "FY2023": 6564, "FY2022": 68205, "FY2021": 3637,
    }),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2025": -328407, "FY2024": 619425, "FY2023": -46888, "FY2022": 259350, "FY2021": 267024,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of subsidiary, net of cash acquired", {
        "FY2022": -32000,
    }),
    ("DATA", "Dividends received from subsidiary undertakings", {
        "FY2025": 26500, "FY2024": 11000, "FY2023": 27500, "FY2022": 20000,
    }),
    ("DATA", "Purchase of property, plant and equipment", {
        "FY2025": -300, "FY2024": -298, "FY2023": -4742, "FY2022": -543, "FY2021": -231,
    }),
    ("DATA", "Disposal of property, plant and equipment", {
        "FY2024": 51,
    }),
    ("DATA", "Purchase of intangible assets", {
        "FY2025": -4612, "FY2024": -6814, "FY2023": -5424, "FY2022": -4777, "FY2021": -3355,
    }),
    ("DATA", "Disposal of intangible assets", {
        "FY2025": 477, "FY2024": 67,
    }),
    ("DATA", "Purchase of right of use asset", {
        "FY2023": -3982,
    }),
    ("DATA", "Disposal of right of use asset", {
        "FY2024": -113,
    }),
    ("DATA", "Purchase of investment securities", {
        "FY2025": -500773, "FY2024": -135668, "FY2023": -415054, "FY2022": -424657, "FY2021": -178144,
    }),
    ("DATA", "Settlement/sale of investment securities", {
        "FY2025": 28148, "FY2024": 162520, "FY2023": 439744, "FY2022": 402000,
    }),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": -450560, "FY2024": 30745, "FY2023": 38042, "FY2022": -39977, "FY2021": -181730,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayments of the principal portion of finance lease liabilities", {
        "FY2025": -737, "FY2024": -710, "FY2023": -797, "FY2022": -1318, "FY2021": -1183,
    }),
    ("DATA", "Inception of finance lease liability", {
        "FY2023": 3982,
    }),
    ("DATA", "Coupon paid to other equity instrument holders", {
        "FY2025": -1518, "FY2024": -1517, "FY2023": -1507, "FY2022": -1404,
    }),
    ("DATA", "Proceeds from the issuance of subordinated debt", {
        "FY2025": 55000, "FY2023": 25000,
    }),
    ("DATA", "Repayment of subordinated debt", {
        "FY2025": -30000,
    }),
    ("DATA", "Proceeds from securitisation", {
        "FY2024": 310558,
    }),
    ("DATA", "Proceeds from the issue of share capital", {
        "FY2021": 13540,
    }),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2025": 22745, "FY2024": 308331, "FY2023": 26678, "FY2022": -2722, "FY2021": 12357,
    }),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2025": -756222, "FY2024": 958501, "FY2023": 17832, "FY2022": 216651, "FY2021": 97651,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 1435307, "FY2024": 476806, "FY2023": 458974, "FY2022": 242323, "FY2021": 144672,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 679085, "FY2024": 1435307, "FY2023": 476806, "FY2022": 458974, "FY2021": 242323,
    }),
]

bw.add_cash_flow_sheet(
    title="Hampshire Trust Bank Plc — Bank Statement of Cash Flows",
    subtitle="Bank (parent-entity) column; FY2021 predates Group consolidation and uses the single Company "
              "statement — see source note",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=74,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=130)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2025": 397694, "FY2024": 300589, "FY2023": 243719, "FY2022": 180193, "FY2021": 174913,
    })],
    p3_sources(),
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2025": "13.5%", "FY2024": "13.6%", "FY2023": "13.3%", "FY2022": "13.8%", "FY2021": "18.9%",
    })],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {
        "FY2025": 414725, "FY2024": 317619, "FY2023": 260749, "FY2022": 197223, "FY2021": 174913,
    })],
    p3_sources(),
    note="No Additional Tier 1 instruments are disclosed for FY2021 — Tier 1 capital equals CET1 capital that year.",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2025": "14.1%", "FY2024": "14.4%", "FY2023": "14.2%", "FY2022": "15.1%", "FY2021": "18.9%",
    })],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {
        "FY2025": 494725, "FY2024": 362750, "FY2023": 311890, "FY2022": 227223, "FY2021": 204913,
    })],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2025": "16.8%", "FY2024": "16.4%", "FY2023": "17.0%", "FY2022": "17.4%", "FY2021": "22.2%",
    })],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {
        "FY2025": 2949233, "FY2024": 2207947, "FY2023": 1830864, "FY2022": 1310125, "FY2021": 922921,
    })],
    p3_sources(),
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {
        "FY2025": "7.5%", "FY2024": "8.1%", "FY2023": "7.5%", "FY2022": "9.2%", "FY2021": "8.0%",
    })],
    p3_sources(),
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio", {
        "FY2025": "346.9%", "FY2024": "391.1%", "FY2023": "388.6%", "FY2022": "386.9%", "FY2021": "314.8%",
    })],
    p3_sources(),
    note="Disclosed only at consolidated Group level from FY2022 onward ('Liquidity is managed on a "
         "consolidated basis hence only Group metrics are reported') — no separate Bank-solo LCR exists to "
         "report for those years. FY2021 predates the Group/Bank split; its single reported value is used.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {
        "FY2025": "158.9%", "FY2024": "163.3%", "FY2023": "147.7%", "FY2022": "152.5%", "FY2021": "120.5%",
    })],
    p3_sources(),
    note="Disclosed only at consolidated Group level from FY2022 onward, same basis as LCR above. FY2021 "
         "predates the Group/Bank split; its single reported value is used.",
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources())

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": -328407, "FY2024": 619425, "FY2023": -46888, "FY2022": 259350, "FY2021": 267024,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": -450560, "FY2024": 30745, "FY2023": 38042, "FY2022": -39977, "FY2021": -181730,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": 22745, "FY2024": 308331, "FY2023": 26678, "FY2022": -2722, "FY2021": 12357,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 679085, "FY2024": 1435307, "FY2023": 476806, "FY2022": 458974, "FY2021": 242323,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {
            "FY2025": "13.5%", "FY2024": "13.6%", "FY2023": "13.3%", "FY2022": "13.8%", "FY2021": "18.9%",
        }),
        ("Tier 1 Ratio", {
            "FY2025": "14.1%", "FY2024": "14.4%", "FY2023": "14.2%", "FY2022": "15.1%", "FY2021": "18.9%",
        }),
        ("Total Capital Ratio", {
            "FY2025": "16.8%", "FY2024": "16.4%", "FY2023": "17.0%", "FY2022": "17.4%", "FY2021": "22.2%",
        }),
        ("Leverage Ratio", {
            "FY2025": "7.5%", "FY2024": "8.1%", "FY2023": "7.5%", "FY2022": "9.2%", "FY2021": "8.0%",
        }),
        ("LCR", {
            "FY2025": "346.9%", "FY2024": "391.1%", "FY2023": "388.6%", "FY2022": "386.9%", "FY2021": "314.8%",
        }),
        ("NSFR", {
            "FY2025": "158.9%", "FY2024": "163.3%", "FY2023": "147.7%", "FY2022": "152.5%", "FY2021": "120.5%",
        }),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. All Cash Flow figures are the Bank (entity-level) "
         "column; LCR/NSFR are Group-level from FY2022 onward (see the LCR/NSFR sheets' notes).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HAMPSHIRE TRUST BANK FINANCIALS.xlsx")
