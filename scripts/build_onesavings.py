import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR_2025_URL = "https://find-and-update.company-information.service.gov.uk/company/07312896/filing-history/MzUyMDIyOTcwM2FkaXF6a2N4/document?download=0&format=pdf"
AR_2024_URL = "https://find-and-update.company-information.service.gov.uk/company/07312896/filing-history/MzQ2NTMxODAwN2FkaXF6a2N4/document?download=0&format=pdf"
AR_2023_URL = "https://find-and-update.company-information.service.gov.uk/company/07312896/filing-history/MzQxOTAwNzg1NWFkaXF6a2N4/document?download=0&format=pdf"
AR_2022_URL = "https://www.onesavingsbank.com/media/w3ffou5b/osbg-ara-2022.pdf"
AR_2021_URL = "https://www.onesavingsbank.com/media/5n1lklrr/onesavings-bank-plc-2021-accounts.pdf"

P3_2025_URL = "https://www.onesavingsbank.com/media/hbymiii2/q4-2025-osbg-pillar-3-disclosure.pdf"
P3_2024_URL = "https://www.onesavingsbank.com/media/143pzceq/q4-2024-osbg-pillar-3-disclosure.pdf"
P3_2023_URL = "https://www.onesavingsbank.com/media/kn3nulae/q4-2023-osb-pillar-3-disclosures.pdf"
P3_2022_URL = "https://www.onesavingsbank.com/media/cqepdkda/osb-group-pillar-3-disclosures-2022.pdf"
P3_2021_URL = "https://www.onesavingsbank.com/media/iuvfpajb/osb-group-pillar-3-disclosures-2021.pdf"

ENTITY_NOTE = (
    "ENTITY AND BASIS NOTE: OneSavings Bank plc (Companies House 07312896, FRN 530504) is the PRA-authorised "
    "bank in scope. Cash Flow Statement figures are the Bank's Company-only column, £m, from its own statutory "
    "annual accounts. The Pillar 3 disclosures are published by OSB Group plc on a consolidated Group basis and "
    "include the Group's banking entities OneSavings Bank plc and Charter Court Financial Services Limited, plus "
    "their relevant subsidiaries; OSB does not publish a five-year OSB-bank-only Pillar 3 series. The bases are "
    "therefore intentionally different and must not be treated as a single-entity time series. The 2023-2025 "
    "Companies House filings were scanned/image-only and were OCR'd; figures were cross-checked against the "
    "official OSB reports and the printed opening/closing cash reconciliation."
)

CASH_FLOW_SOURCES = (
    "Sources — OneSavings Bank plc (Company-only basis), Statement of Cash Flows, £m:\n"
    f"FY2025 & FY2024: OneSavings Bank plc Annual Report and Financial Statements for the year ended 31 December "
    f"2025, p.91 (Company column; FY2024 comparative) — {AR_2025_URL}\n"
    f"FY2024 & FY2023: OneSavings Bank plc Annual Report and Financial Statements for the year ended 31 December "
    f"2024, p.91 (Company column; FY2023 comparative) — {AR_2024_URL}\n"
    f"FY2023 & FY2022: OneSavings Bank plc Annual Report and Financial Statements for the year ended 31 December "
    f"2023, p.89 (Company column; FY2022 comparative) — {AR_2023_URL}\n"
    f"FY2021: OneSavings Bank plc Annual Report and Financial Statements for the year ended 31 December 2021, "
    f"p.98 (Company column) — {AR_2021_URL}\n\n" + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources — OSB Group plc consolidated Pillar 3 basis (includes OneSavings Bank plc and CCFSL):\n"
        f"FY2025: Pillar 3 Disclosures 31 December 2025, p.7 (UK KM1; MREL UK KM2 on p.8; liquidity templates "
        f"on pp.31 and 34) — {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures 31 December 2024, p.9 (UK KM1; MREL UK KM2 on p.10; liquidity templates "
        f"on pp.49 and 52) — {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 31 December 2023, p.9 (UK KM1; liquidity templates on pp.46 and 49) — "
        f"{P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures 31 December 2022, pp.8-9 (UK KM1 and liquidity templates) — {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures for year ended 31 December 2021, p.8 (Table 4: Key metrics) and p.62 "
        f"(Table 47: LIQ1) — {P3_2021_URL}\n\n" + ENTITY_NOTE
    )


bw = BankWorkbook("OneSavings Bank plc", YEARS, YEAR_LABEL, header_color="1F4E78")

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": 415.6, "FY2024": 345.9, "FY2023": 446.9, "FY2022": 387.3, "FY2021": 314.5}),
    ("DATA", "Adjustments for non-cash and other items", {"FY2025": 131.2, "FY2024": 126.3, "FY2023": 153.1, "FY2022": 68.6, "FY2021": 12.2}),
    ("DATA", "Changes in operating assets and liabilities", {"FY2025": 563.7, "FY2024": 521.6, "FY2023": -402.4, "FY2022": 276.6, "FY2021": -817.4}),
    ("SECTION", "Net operating cash flow reconciliation", {}),
    ("DATA", "Cash generated in operating activities", {"FY2025": 1110.5, "FY2024": 993.8, "FY2023": 197.6, "FY2022": 732.5, "FY2021": -490.7}),
    ("DATA", "Provisions paid", {"FY2025": -3.3}),
    ("DATA", "Net tax paid", {"FY2025": -10.8, "FY2024": -52.3, "FY2023": -46.3, "FY2022": -54.0, "FY2021": -53.2}),
    ("TOTAL", "Net cash generated from operating activities", {"FY2025": 1096.4, "FY2024": 941.5, "FY2023": 151.3, "FY2022": 678.5, "FY2021": -543.9}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Maturity and sales of investment securities", {"FY2025": 303.7, "FY2024": 428.9, "FY2023": 317.5, "FY2022": 451.0, "FY2021": 215.4}),
    ("DATA", "Purchases of investment securities", {"FY2025": -405.7, "FY2024": -559.8, "FY2023": -592.0, "FY2022": -556.4, "FY2021": -216.6}),
    ("DATA", "Interest received on investment securities", {"FY2025": 22.7, "FY2024": 23.5, "FY2023": 16.3, "FY2022": 3.0, "FY2021": 0.2}),
    ("DATA", "Sales of financial instruments", {"FY2021": 0.3}),
    ("DATA", "Investments in subsidiaries", {"FY2023": 0, "FY2022": -3.2}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 1.1, "FY2021": 2.0}),
    ("DATA", "Purchases of property, plant and equipment and intangible assets", {"FY2025": -29.6, "FY2024": -34.0, "FY2023": -24.4, "FY2022": -7.2, "FY2021": -5.0}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": -107.8, "FY2024": -141.4, "FY2023": -282.6, "FY2022": -112.8, "FY2021": -3.7}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Financing received", {"FY2025": 1377.2, "FY2024": 527.0, "FY2023": 578.7, "FY2022": 120.0, "FY2021": 3163.6}),
    ("DATA", "Financing repaid", {"FY2025": -1805.9, "FY2024": -764.2, "FY2023": -597.2, "FY2022": -304.1, "FY2021": -2589.1}),
    ("DATA", "Interest paid on financing", {"FY2025": -110.9, "FY2024": -145.4, "FY2023": -107.7, "FY2022": -25.5, "FY2021": -6.6}),
    ("DATA", "Dividends paid", {"FY2025": -219.0, "FY2024": -218.7, "FY2023": -335.0, "FY2022": -233.1, "FY2021": -86.7}),
    ("DATA", "Coupon paid on AT1 securities", {"FY2024": -5.4, "FY2023": -5.4, "FY2022": -5.4, "FY2021": -4.7}),
    ("DATA", "Net swap interest paid on subordinated liabilities and senior notes", {"FY2024": -2.7}),
    ("DATA", "Net swap interest paid on structural hedge", {"FY2024": -2.1}),
    ("DATA", "Redemption of AT1 securities", {"FY2025": -80.0, "FY2021": -63.5}),
    ("DATA", "Issuance of AT1 securities", {"FY2025": 89.4, "FY2021": 90.0}),
    ("DATA", "Repayments of principal portion of lease liabilities", {"FY2024": -0.5, "FY2023": -0.7, "FY2022": -0.8, "FY2021": -0.7}),
    ("DATA", "Other financing activities", {"FY2025": -10.0}),
    ("DATA", "Proceeds from issuance of shares under employee SAYE scheme", {"FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": -759.2, "FY2024": -612.0, "FY2023": -467.3, "FY2022": -448.9, "FY2021": 502.3}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": 229.4, "FY2024": 188.1, "FY2023": -598.6, "FY2022": 116.8, "FY2021": -45.3}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 1038.6, "FY2024": 850.5, "FY2023": 1449.1, "FY2022": 1332.3, "FY2021": 1377.6}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 1268.0, "FY2024": 1038.6, "FY2023": 850.5, "FY2022": 1449.1, "FY2021": 1332.3}),
]

bw.add_cash_flow_sheet("OneSavings Bank plc — Statement of Cash Flows", "Company-only basis, £m. Pillar 3 sheets are OSB Group consolidated; see source note.", rows, CASH_FLOW_SOURCES, first_col_width=72, source_height=260, unit_suffix=" (£m)")


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"OSB Group consolidated basis, {unit}" if unit else "OSB Group consolidated basis", rows_data, p3_sources(), note=note, first_col_width=50, source_height=190)


metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1975.8, "FY2024": 1946.4, "FY2023": 1905.7, "FY2022": 1920.7, "FY2021": 1781.7})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "15.8%", "FY2024": "16.3%", "FY2023": "16.1%", "FY2022": "18.3%", "FY2021": "19.6%"})])
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 2142.9, "FY2024": 2096.4, "FY2023": 2055.7, "FY2022": 2070.7, "FY2021": 1931.7})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "17.1%", "FY2024": "17.6%", "FY2023": "17.4%", "FY2022": "19.7%", "FY2021": "21.2%"})])
metric("Total Capital", "£m", [("Total capital", {"FY2025": 2392.9, "FY2024": 2346.4, "FY2023": 2305.7, "FY2022": 2070.7, "FY2021": 1931.7})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "19.1%", "FY2024": "19.7%", "FY2023": "19.5%", "FY2022": "19.7%", "FY2021": "21.2%"})])
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", {"FY2025": 12541.7, "FY2024": 11915.7, "FY2023": 11845.6, "FY2022": 10494.7, "FY2021": 9101.6})])
metric("Leverage Ratio", "£m / %", [("Total exposure measure excluding claims on central banks", {"FY2025": 28956.3, "FY2024": 27322.9, "FY2023": 27438.8, "FY2022": 24725.4}), ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "7.4%", "FY2024": "7.7%", "FY2023": "7.5%", "FY2022": "8.4%", "FY2021": "7.9%"})], "FY2021 uses the pre-UK-KM1 disclosure's Group leverage ratio and does not provide a comparable exposure-measure amount; the 2022 report notes a like-for-like FY2021 exposure measure of £21,742.2m and ratio of 8.9%, but the workbook preserves the FY2021 as-reported 7.9% ratio rather than mixing bases.")
metric("LCR", "£m / %", [("Total high-quality liquid assets (HQLA), weighted value average", {"FY2025": 3181.5, "FY2024": 3351.8, "FY2023": 3078.0, "FY2022": 2907.1}), ("Total net cash outflows (adjusted value)", {"FY2025": 1898.6, "FY2024": 1794.3, "FY2023": 1565.6, "FY2022": 1491.5}), ("Liquidity Coverage Ratio (%)", {"FY2025": "169.5%", "FY2024": "188.0%", "FY2023": "197.1%", "FY2022": "197.0%", "FY2021": "195.5%"})], "FY2021's pre-UK-KM1 disclosure provides only the Group LCR percentage in Table 4; HQLA and adjusted net-outflow amounts are not disclosed on a directly comparable annual basis. FY2022 onward uses the 12-month average template (the 2022 disclosure restates prior LCR methodology).")
metric("NSFR", "£m / %", [("Total available stable funding", {"FY2025": 26596.3, "FY2024": 27138.8, "FY2023": 26087.0}), ("Total required stable funding", {"FY2025": 18911.8, "FY2024": 20051.6, "FY2023": 19638.6}), ("NSFR ratio (%)", {"FY2025": "140.6%", "FY2024": "135.4%", "FY2023": "132.8%"})], "FY2022's Pillar 3 report states that NSFR disclosures were not due until 1 January 2023; FY2021 likewise has no NSFR disclosure. The FY2023 table does not provide a 31 Dec 2022 comparative, so those cells remain blank.")
metric("MREL Ratio", None, [("MREL resources as a percentage of total risk-weighted assets", {"FY2025": "24.7%", "FY2024": "25.6%"})], "Numeric MREL ratio is disclosed in UK KM2 for FY2025 and FY2024 only. FY2023's Pillar 3 report discusses the 18% requirement but does not provide a year-end MREL-resource ratio; FY2022 and FY2021 do not provide a comparable numeric MREL ratio. Those years are left blank rather than inferred.")

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated from operating activities", {"FY2025": 1096.4, "FY2024": 941.5, "FY2023": 151.3, "FY2022": 678.5, "FY2021": -543.9}),
        ("Net cash from investing activities", {"FY2025": -107.8, "FY2024": -141.4, "FY2023": -282.6, "FY2022": -112.8, "FY2021": -3.7}),
        ("Net cash from financing activities", {"FY2025": -759.2, "FY2024": -612.0, "FY2023": -467.3, "FY2022": -448.9, "FY2021": 502.3}),
        ("Cash and cash equivalents at end of year", {"FY2025": 1268.0, "FY2024": 1038.6, "FY2023": 850.5, "FY2022": 1449.1, "FY2021": 1332.3}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.8%", "FY2024": "16.3%", "FY2023": "16.1%", "FY2022": "18.3%", "FY2021": "19.6%"}),
        ("Tier 1 Ratio", {"FY2025": "17.1%", "FY2024": "17.6%", "FY2023": "17.4%", "FY2022": "19.7%", "FY2021": "21.2%"}),
        ("Total Capital Ratio", {"FY2025": "19.1%", "FY2024": "19.7%", "FY2023": "19.5%", "FY2022": "19.7%", "FY2021": "21.2%"}),
        ("Leverage Ratio", {"FY2025": "7.4%", "FY2024": "7.7%", "FY2023": "7.5%", "FY2022": "8.4%", "FY2021": "7.9%"}),
        ("LCR", {"FY2025": "169.5%", "FY2024": "188.0%", "FY2023": "197.1%", "FY2022": "197.0%", "FY2021": "195.5%"}),
        ("NSFR", {"FY2025": "140.6%", "FY2024": "135.4%", "FY2023": "132.8%"}),
    ],
    note="Cash flows are OneSavings Bank plc Company-only; Pillar 3 metrics are OSB Group consolidated. See the basis note on each sheet.",
)

bw.save("/Users/armaan/code/katalysis/banks/ONESAVINGS FINANCIALS.xlsx")
