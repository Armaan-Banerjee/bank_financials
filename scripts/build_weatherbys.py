import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
COMPANY = "Weatherbys Bank Limited"
COMPANY_NO = "02943300"
FRN = "204571"
LEI = "549300OF84KDPIFN4M17"

AR_URLS = {
    "FY2025": "https://www.weatherbys.bank/weatherbys-banking-group-annual-report-2025/",
    "FY2024": "https://www.weatherbys.bank/app/uploads/2025/04/Weatherbys-Banking-Group-Annual-Report-2024.pdf",
    "FY2023": "https://www.weatherbys.bank/app/uploads/2024/05/Weatherbys-Banking-Group-Annual-Report-2023.pdf",
    "FY2022": "https://www.weatherbys.bank/app/uploads/2023/05/Weatherbys-Banking-Group-Annual_Report-2022.pdf",
}
P3_URLS = {
    "FY2024": "https://www.weatherbys.bank/app/uploads/2025/04/Weatherbys-Bank-Pillar-3-Disclosures-2024.pdf",
    "FY2023": "https://weatherbys.bank/app/uploads/2024/05/Weatherbys-Bank-Pillar-3-Dislcosures-2023.pdf",
    "FY2022": "https://weatherbys.bank/app/uploads/2023/05/Weatherbys-Bank-Pillar-3-Dislcosures-2022.pdf",
    "FY2021": "https://www.weatherbys.bank/app/uploads/2022/05/Pillar-3-2021-v2.0-Weatherbys-Bank.pdf",
}
CH_URL = f"https://find-and-update.company-information.service.gov.uk/company/{COMPANY_NO}"
PRA_URL = "https://www.bankofengland.co.uk/prudential-regulation/authorisations/which-firms-does-the-pra-regulate"

ENTITY_NOTE = (
    f"Entity verification: {COMPANY}, Companies House {COMPANY_NO}, FRN {FRN}, LEI {LEI}; "
    "the supplied Banks List 2608.xlsx, the Weatherbys corporate-information page, the PRA register, "
    "and Companies House identify the same legal bank. The workbook uses Weatherbys Banking Group's "
    "consolidated cash-flow statement because that is the audited cash-flow presentation in the annual "
    "reports. The official Pillar 3 disclosures are consolidated Group/Solo disclosures: the documents "
    "state that the solo-consolidated group includes Weatherbys Bank Limited and its subsidiaries and that "
    "there are no differences between accounting and prudential consolidation for the Group. Group figures "
    "are therefore used only where the source explicitly labels them Group and Solo; unrelated wider-group "
    "figures are not substituted. Amounts are GBP'000 unless stated otherwise."
)

CASH_SOURCES = (
    "Sources - Weatherbys Banking Group consolidated statement of cash flows, GBP'000: "
    f"FY2025/FY2024: Annual Report and Financial Accounts 2025, p.64 - {AR_URLS['FY2025']}; "
    f"FY2024/FY2023: Annual Report & Accounts 2024, p.45 - {AR_URLS['FY2024']}; "
    f"FY2023/FY2022: Annual Report & Accounts 2023, p.50 - {AR_URLS['FY2023']}; "
    f"FY2022/FY2021: Annual Report & Accounts 2022, p.46 - {AR_URLS['FY2022']}.\n\n"
    + ENTITY_NOTE
    + " The 2024 statement labels the financing section's subtotal as investing activities, but its placement and figures are the financing cash flows; the source presentation is retained with a corrected descriptive label."
)

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit for the financial year before exceptional items", {"FY2025": 19244, "FY2024": 18270, "FY2023": 24735, "FY2022": 11909, "FY2021": 5206}),
    ("DATA", "Depreciation, impairment and amortisation of fixed assets", {"FY2025": 7065, "FY2024": 4506, "FY2023": 2758, "FY2022": 2786, "FY2021": 2402}),
    ("DATA", "Amortisation of debt securities", {"FY2025": -1870, "FY2024": -1138, "FY2023": 413, "FY2022": 443, "FY2021": 133}),
    ("DATA", "Taxation expense", {"FY2025": 3830, "FY2024": 6306, "FY2023": 8348, "FY2022": 3504, "FY2021": 1596}),
    ("DATA", "Increase in prepayments and accrued income", {"FY2025": -1508, "FY2024": -4032, "FY2023": -4930, "FY2022": -6282, "FY2021": -1055}),
    ("DATA", "Decrease/(increase) in trade and other debtors", {"FY2025": -678, "FY2024": 38, "FY2023": -201, "FY2022": -364, "FY2021": 20}),
    ("DATA", "Change in fair value of financial instruments", {"FY2025": 6430, "FY2024": -1624, "FY2023": 7216, "FY2022": -8619, "FY2021": -3069}),
    ("DATA", "Movement in margin call", {"FY2025": -6550}),
    ("DATA", "Loss/(gain) on investments", {"FY2025": 20, "FY2024": 71, "FY2023": -17, "FY2022": 104, "FY2021": 3}),
    ("DATA", "Loss/(gain) on disposal of subsidiary/tangible fixed assets", {"FY2025": -10235}),
    ("DATA", "Change in trade and other creditors", {"FY2025": 2299, "FY2024": -2982, "FY2023": 11753, "FY2022": 2607, "FY2021": -496}),
    ("DATA", "Net decrease/(increase) in provisions", {"FY2025": -64, "FY2024": -1366, "FY2023": 5968, "FY2022": 2623, "FY2021": 1123}),
    ("DATA", "Increase/(decrease) in provision for bad and doubtful debts", {"FY2025": 1074, "FY2024": 46, "FY2023": 184, "FY2022": -25, "FY2021": -518}),
    ("DATA", "Net increase/(decrease) in deposits from customers", {"FY2025": 193121, "FY2024": 203231, "FY2023": -16626, "FY2022": 116590, "FY2021": 315834}),
    ("DATA", "Net increase in loans and advances to customers", {"FY2025": -138623, "FY2024": -38018, "FY2023": -46309, "FY2022": -30957, "FY2021": -65508}),
    ("TOTAL", "Cash from operations", {"FY2025": 73555, "FY2024": 183308, "FY2023": -6708, "FY2022": 94319, "FY2021": 255671}),
    ("DATA", "Taxation paid", {"FY2025": -4301, "FY2024": -5721, "FY2023": -5421, "FY2022": -2320, "FY2021": -678}),
    ("TOTAL", "Net cash generated/(used) from operating activities", {"FY2025": 69254, "FY2024": 177587, "FY2023": -12129, "FY2022": 91999, "FY2021": 254993}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Sale of subsidiary undertaking", {"FY2025": 10552}),
    ("DATA", "Income from joint venture", {"FY2025": 400}),
    ("DATA", "Investment in joint venture", {"FY2023": -60, "FY2022": -280, "FY2021": -12}),
    ("DATA", "Purchase of investment securities", {"FY2025": -361092, "FY2024": -173844, "FY2023": -66857, "FY2022": -136837, "FY2021": -22148}),
    ("DATA", "Sale and maturities of investment securities", {"FY2025": 190722, "FY2024": 72330, "FY2023": 127951, "FY2022": 46415, "FY2021": 38649}),
    ("DATA", "Purchase of tangible fixed assets", {"FY2025": -4139, "FY2024": -2103, "FY2021": -3939}),
    ("DATA", "Purchase of intangible fixed assets", {"FY2025": -13123, "FY2024": -6502}),
    ("DATA", "Purchase of intangible/tangible fixed assets", {"FY2023": -7251, "FY2022": -6456}),
    ("TOTAL", "Net cash (used)/generated from investing activities", {"FY2025": -176680, "FY2024": -110119, "FY2023": 53783, "FY2022": -97158, "FY2021": 12550}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of contingent convertible securities", {"FY2023": 3000}),
    ("DATA", "Equity dividends paid", {"FY2025": -11100, "FY2024": -5000, "FY2023": -5000, "FY2022": -2000, "FY2021": -1250}),
    ("TOTAL", "Net cash (used)/generated from financing activities", {"FY2025": -11100, "FY2024": -5000, "FY2023": -2000, "FY2022": -2000, "FY2021": -1250}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -118526, "FY2024": 62468, "FY2023": 39654, "FY2022": -7159, "FY2021": 266293}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 687343, "FY2024": 624875, "FY2023": 585221, "FY2022": 592380, "FY2021": 326087}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 568817, "FY2024": 687343, "FY2023": 624875, "FY2022": 585221, "FY2021": 592380}),
]

bw = BankWorkbook(bank_name=COMPANY, years=YEARS, year_label=None, header_color="7030A0")
bw.add_cash_flow_sheet(
    title=f"{COMPANY} — Cash Flow Statement",
    subtitle="Weatherbys Banking Group consolidated basis, GBP'000. Five latest available financial years.",
    rows=rows,
    sources_text=CASH_SOURCES,
    first_col_width=78,
    source_height=360,
    unit_suffix=" (GBP'000)",
)

P3_SOURCES = (
    "Sources - Weatherbys Bank 3 Pillar Disclosures, Group/Solo columns, GBP'000 except ratios: "
    f"FY2024, pp.5-6 and 20-26 - {P3_URLS['FY2024']}; "
    f"FY2023, pp.5-6 and 20-27 - {P3_URLS['FY2023']}; "
    f"FY2022, pp.6-7 and 21-27 - {P3_URLS['FY2022']}; "
    f"FY2021, pp.5-6 and 14, 18-22 - {P3_URLS['FY2021']}.\n\n"
    + ENTITY_NOTE
    + " FY2025 is blank for regulatory metrics because the 2025 annual report does not reproduce the requested Pillar 3 capital/liquidity tables and no 2025 Pillar 3 disclosure was located in the official archive."
)

capital = {
    "FY2024": {"cet1": 84898, "tier1": 87898, "total": 99753, "rwa": 613559, "cet1r": "13.84%", "tier1r": "14.33%", "totalr": "16.26%", "lev": "7.08%", "lcr": "1017%", "nsfr": "266%"},
    "FY2023": {"cet1": 73192, "tier1": 76192, "total": 87815, "rwa": 543090, "cet1r": "13.48%", "tier1r": "14.03%", "totalr": "16.17%", "lev": "7.13%", "lcr": "896%", "nsfr": "254%"},
    "FY2022": {"cet1": 57524, "tier1": 57524, "total": 69108, "rwa": 476472, "cet1r": "12.07%", "tier1r": "12.07%", "totalr": "14.50%", "lev": "5.30%", "lcr": "650%", "nsfr": "259.7%"},
    "FY2021": {"cet1": 50247, "tier1": 50247, "total": 61634, "rwa": 425582, "cet1r": "11.81%", "tier1r": "11.81%", "totalr": "14.48%", "lev": "3.37%", "lcr": "531%", "nsfr": "268.2%"},
}

def series(key):
    return {y: capital[y][key] for y in capital}

def metric(name, unit, label, key):
    bw.add_metric_sheet(name, unit, [(label, series(key))], P3_SOURCES, first_col_width=58, source_height=320)

metric("CET1 Capital", "£'000", "CET1 capital", "cet1")
metric("CET1 Ratio", "%", "CET1 ratio", "cet1r")
metric("Tier 1 Capital", "£'000", "Tier 1 capital", "tier1")
metric("Tier 1 Ratio", "%", "Tier 1 ratio", "tier1r")
metric("Total Capital", "£'000", "Total capital", "total")
metric("Total Capital Ratio", "%", "Total capital ratio", "totalr")
metric("Total RWAs", "£'000", "Total risk weighted assets", "rwa")
metric("Leverage Ratio", "%", "Leverage ratio", "lev")
metric("LCR", "%", "Liquidity coverage ratio", "lcr")
metric("NSFR", "%", "Net stable funding ratio", "nsfr")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], P3_SOURCES,
    per_note={"MREL Ratio": "MREL was not separately disclosed in the Weatherbys 2021-2024 Pillar 3 documents reviewed; FY2025 has no official Pillar 3 document located. This is an explicit non-disclosure, not a zero."},
)

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated/(used) from operating activities", {y: dict((r[1], r[2].get(y)) for r in rows).get("Net cash generated/(used) from operating activities") for y in YEARS}),
        ("Net cash (used)/generated from investing activities", {y: dict((r[1], r[2].get(y)) for r in rows).get("Net cash (used)/generated from investing activities") for y in YEARS}),
        ("Net cash (used)/generated from financing activities", {y: dict((r[1], r[2].get(y)) for r in rows).get("Net cash (used)/generated from financing activities") for y in YEARS}),
        ("Cash and cash equivalents at end of year", {y: dict((r[1], r[2].get(y)) for r in rows).get("Cash and cash equivalents at end of year") for y in YEARS}),
    ],
    cash_flow_unit="GBP'000",
    ratios=[("CET1 Ratio", series("cet1r")), ("Total Capital Ratio", series("totalr"))],
    note="FY2025 Pillar 3 metrics are blank because no 2025 official disclosure was located; FY2021-FY2024 values are the official Weatherbys Group/Solo disclosures.",
)

bw.save("/Users/armaan/code/katalysis/banks/WEATHERBYS FINANCIALS.xlsx")
