import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

# Site (Contentful CDN) hosts text-native copies of the last 3 Annual Reports;
# FY2022/FY2021 only exist as scanned Companies House filings.
AR2025_URL = "https://assets.ctfassets.net/xzmqg68ot16t/1aUkuB7BcAd8Pj5Kq0RNqh/101ced4af6be2d55cd37fad3542829b2/Cynergy_Bank_-_Annual_Report_2025.pdf"
AR2024_URL = "https://assets.ctfassets.net/xzmqg68ot16t/2AeSbXsBP7fwKhngGTLWxb/ca86e60128ab83d41842b85ae74aa326/Annual_Report_2024.pdf"
AR2023_URL = "https://assets.ctfassets.net/xzmqg68ot16t/2oPLoaeUJ2c4kRJcNMSyMp/54230fc39821a0d6ede6f81f1c7528ce/Cynergy_Bank_Limited_-_Annual_Report_2023.pdf"
AR2022_CH_URL = "https://find-and-update.company-information.service.gov.uk/company/04728421/filing-history/MzM3OTM0NzA5MmFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "Entity: Cynergy Bank Plc, company 04728421 (formerly Bank of Cyprus UK Limited / Bank of Cyprus "
    "Advances Limited before a 2018 rebrand/ownership change to a consortium led by Cynergy Capital Ltd) - "
    "same company number throughout, no entity-identity ambiguity. Consolidated basis throughout (the Bank "
    "plus subsidiaries Cynergy Business Finance Limited and, in earlier years, Cynergy Connect Technologies "
    "Ltd, which never traded and was dissolved during 2023).\n"
    "Each year's own originally-published figures are used (not later restated comparatives) - FY2025's own "
    "Annual Report explicitly restates its FY2024 comparative column (see its own footnote: 'Comparatives "
    "have been re-presented to conform with the current year's presentation... presentational only and have "
    "no impact on the reported cash and cash equivalents') and the FY2025 report's own Alternative "
    "Performance Measures note gives a full reconciliation of the reclassifications; FY2024's own column here "
    "uses FY2024's own Annual Report instead. Similarly FY2022's own Annual Report (Companies House, scanned) "
    "presents cash and cash equivalents movements without a separate 'effects of exchange rate' line "
    "(opening + net change ties to closing exactly on its own); a later report's FY2022 comparative adds a "
    "separate £760k FX line by reclassifying it out of the opening balance - FY2022's own original figures "
    "are used here, not that later restatement.\n"
    "FY2021 figures are the FY2021 comparative column within FY2022's own Annual Report (the FY2021 Annual "
    "Report itself is only available as a further scanned Companies House filing and was not independently "
    "re-checked) - this is the standard 'sourced from the following year's own comparative' pattern used "
    "elsewhere in this project when a year's own standalone report isn't the primary source.\n"
    "Line items vary in granularity across report vintages (e.g. 'purchase' and 'redemption' of asset-backed "
    "securities are reported as one combined net line in FY2022/FY2021's presentation but split into two "
    "lines from FY2023 onward) - blank cells indicate that year's report did not disclose that specific "
    "split; a combined figure appears on its own row where reported that way. Section TOTALs are consistent "
    "and comparable across all 5 years regardless of this granularity."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Cynergy Bank Plc's own Consolidated statement of cash flows, £'000:\n"
    f"FY2025 (& FY2024 restated comparative, not used - see note): Cynergy Bank plc Annual Report & Accounts 2025, p.54 (Consolidated and company statement of cash flows) - {AR2025_URL}\n"
    f"FY2024 (own, & FY2023 comparative cross-checked): Cynergy Bank plc Annual Report & Accounts 2024, p.87-88 (Consolidated and company statement of cash flows) - {AR2024_URL}\n"
    f"FY2023 (own, & FY2022 comparative cross-checked): Cynergy Bank Limited Annual Report & Accounts 2023, p.93-94 (Consolidated and company statement of cash flows) - {AR2023_URL}\n"
    f"FY2022 (own) & FY2021 (comparative): Cynergy Bank Limited Annual Report & Accounts 2022 (Companies House filing, scanned), p.95-96 (Consolidated and Company statement of cash flows) - {AR2022_CH_URL}\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Cynergy Bank Plc Consolidated basis:\n"
        f"FY2024 & FY2023: Cynergy Bank plc Annual Report & Accounts 2024, p.146 (Note 32, Capital resources) - {AR2024_URL}\n"
        "FY2025, FY2022, FY2021: no quantitative capital or liquidity figures were found in the corresponding "
        "Annual Report - only qualitative narrative in the 'Capital, liquidity and funding risk' section of "
        "each report's Risk report (e.g. 'we held surplus regulatory capital', 'the liquidity coverage ratio "
        "has exceeded the regulatory requirements'), with no £ or % figures stated. No standalone Pillar 3 "
        "document was found on Cynergy Bank's own site (its investor/company-performance page lists only the "
        "3 Annual Reports above, no separate regulatory disclosures page) - Cynergy Bank operates under the "
        "PRA's Small Domestic Deposit Taker (SDDT) regime, which the FY2025 report's own risk section states "
        "'simplifies certain capital requirements', plausibly explaining the absence of a formal KM1-style "
        "disclosure in any year reviewed."
    )


bw = BankWorkbook(bank_name="Cynergy Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="46C505")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 51564, "FY2024": 52632, "FY2023": 55157, "FY2022": 50489, "FY2021": 30400}),
    ("DATA", "Credit impairment charges/(reversals) on financial assets", {"FY2025": -91, "FY2024": 2082, "FY2023": 4445, "FY2022": 9100, "FY2021": 5396}),
    ("DATA", "Depreciation of property, equipment and right-of-use assets", {"FY2025": 2028, "FY2024": 2197, "FY2023": 1730, "FY2022": 378, "FY2021": 1018}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 9891, "FY2024": 7264, "FY2023": 4636, "FY2022": 3876, "FY2021": 2429}),
    ("DATA", "Write-off/impairment of fixed and intangible assets", {"FY2025": 597, "FY2024": 305, "FY2023": 706, "FY2022": 1215}),
    ("DATA", "Gain on disposal of property", {"FY2022": -9230}),
    ("DATA", "Deferred gain on disposal of property", {"FY2023": -276, "FY2022": -277}),
    ("DATA", "Other gains", {"FY2025": -404, "FY2024": -1000}),
    ("DATA", "Net gains on derecognition of financial assets", {"FY2025": -3578}),
    ("DATA", "Lease interest", {"FY2025": 877, "FY2024": 946, "FY2023": 937, "FY2022": 81, "FY2021": 29}),
    ("DATA", "Interest expense on subordinated loan(s)", {"FY2025": 4218, "FY2024": 1851, "FY2023": 783, "FY2022": 2328, "FY2021": 2400}),
    ("DATA", "Interest income on asset-backed securities (accrual adjustment)", {"FY2025": -21020, "FY2024": -11703, "FY2023": -5667, "FY2022": -2570, "FY2021": -76}),
    ("DATA", "Amortisation of issuance costs relating to subordinated loan(s)", {"FY2025": -76, "FY2024": 34, "FY2023": 21, "FY2021": 125}),
    ("DATA", "Interest paid on lease liabilities (accrual adjustment)", {"FY2025": -839}),
    ("DATA", "Tax paid", {"FY2025": -13475, "FY2024": -6580, "FY2023": -17052, "FY2022": -9937, "FY2021": -6409}),
    ("DATA", "Foreign exchange losses/(gains)", {"FY2025": 677, "FY2024": -711, "FY2023": -42, "FY2022": 977, "FY2021": 68}),
    ("DATA", "Fair value (gains)/losses on derivative/hedging instruments", {"FY2025": -544, "FY2024": 204, "FY2023": -2111, "FY2022": -3983}),
    ("SECTION", "Changes in operating assets", {}),
    ("DATA", "Mandatory deposits with central bank", {"FY2025": 0, "FY2024": 9348, "FY2023": -549, "FY2022": -1576, "FY2021": -1491}),
    ("DATA", "Loans and advances to customers", {"FY2025": -545166, "FY2024": -90320, "FY2023": -313908, "FY2022": -313752, "FY2021": -341012}),
    ("DATA", "Other assets", {"FY2025": -11434, "FY2024": 38737, "FY2023": -41284, "FY2022": -23449, "FY2021": -225}),
    ("DATA", "Derivative assets", {"FY2025": 4299, "FY2024": -2096, "FY2023": 10003, "FY2022": -12350, "FY2021": -23}),
    ("DATA", "Accrued income and prepaid expenses", {"FY2022": -4072, "FY2021": -6391}),
    ("DATA", "Proceeds from sale of financial assets", {"FY2025": 76687}),
    ("SECTION", "Changes in operating liabilities", {}),
    ("DATA", "Customer and bank deposits", {"FY2025": 423044, "FY2024": 455246, "FY2023": 391092, "FY2022": 493923, "FY2021": 540317}),
    ("DATA", "Derivative liabilities", {"FY2025": 3085, "FY2024": -20896, "FY2023": 28536, "FY2022": 3409, "FY2021": -344}),
    ("DATA", "Other liabilities", {"FY2025": 2517, "FY2024": 8019, "FY2023": 13796, "FY2022": 4916, "FY2021": -213}),
    ("DATA", "Accrued expenses", {"FY2022": 1290, "FY2021": 8305}),
    ("TOTAL", "Net cash flow generated from/(used in) operating activities", {"FY2025": -17143, "FY2024": 445559, "FY2023": 130953, "FY2022": 190786, "FY2021": 234303}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property and equipment", {"FY2025": -204, "FY2024": -398, "FY2023": -3343, "FY2022": -877, "FY2021": -72}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -25325, "FY2024": -21721, "FY2023": -27176, "FY2022": -6048, "FY2021": -9230}),
    ("DATA", "Purchase of asset-backed/debt securities", {"FY2025": -484349, "FY2024": -149500, "FY2023": -76396}),
    ("DATA", "Redemption of asset-backed/debt securities", {"FY2025": 26952, "FY2024": 35836, "FY2023": 67893}),
    ("DATA", "Redemption/(purchase) of asset-backed securities (combined, as reported)", {"FY2022": 26975, "FY2021": -137782}),
    ("DATA", "Interest received on asset-backed securities", {"FY2025": 17692}),
    ("DATA", "Proceeds from sale of property", {"FY2025": 5904, "FY2022": 16370}),
    ("TOTAL", "Net cash flow generated from/(used in) investing activities", {"FY2025": -459330, "FY2024": -135783, "FY2023": -39022, "FY2022": 36420, "FY2021": -147084}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issuance of new share capital", {"FY2022": 47000}),
    ("DATA", "Proceeds from issuance of subordinated loan(s)", {"FY2025": 35000, "FY2023": 14826}),
    ("DATA", "Capital repayment from finance lease obligations", {"FY2025": -1487, "FY2024": -2292, "FY2023": -1125, "FY2022": 34, "FY2021": -238}),
    ("DATA", "Interest paid on subordinated loan(s)", {"FY2025": -4032}),
    ("TOTAL", "Net cash flow generated from/(used in) financing activities", {"FY2025": 29481, "FY2024": -2292, "FY2023": 13701, "FY2022": 47034, "FY2021": -238}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents for the year", {"FY2025": -446992, "FY2024": 307484, "FY2023": 105632, "FY2022": 274240, "FY2021": 86981}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 1058851, "FY2024": 751598, "FY2023": 646528, "FY2022": 372288, "FY2021": 285307}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2025": 44, "FY2024": -231, "FY2023": -562}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 611903, "FY2024": 1058851, "FY2023": 751598, "FY2022": 646528, "FY2021": 372288}),
]

bw.add_cash_flow_sheet(
    title="Cynergy Bank Plc — Consolidated and Company Statement of Cash Flows",
    subtitle="Consolidated basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=80,
    source_height=260,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
NOT_DISCLOSED_NOTE = (
    "Not publicly disclosed. Cynergy Bank's Annual Reports discuss capital/liquidity/funding risk only "
    "qualitatively (e.g. 'we held surplus regulatory capital', 'the liquidity coverage ratio has exceeded "
    "the regulatory requirements') with no £ or % figures stated in any year reviewed for this metric, and "
    "no standalone Pillar 3 document was found on the bank's own site. See the Cash Flow Statement sheet's "
    "source note for the SDDT-regime context that plausibly explains this."
)

TIER1_NOTE = (
    "Cynergy Bank's own Annual Report labels this line 'Total eligible Tier 1 capital (CET1)' - i.e. it "
    "states Tier 1 capital and CET1 capital are identical (no Additional Tier 1 instruments in issue) - see "
    "the CET1 Capital sheet for the same figures and source."
)

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"Consolidated basis, {unit}" if unit else "Consolidated basis",
                         rows_data, p3_sources(), note=note, first_col_width=52, source_height=170)


metric(
    "CET1 Capital", "£'000",
    [("Total eligible Tier 1 capital (CET1)", {"FY2024": 321877, "FY2023": 306251})],
)

bw.add_not_disclosed_metric_sheets(
    ["CET1 Ratio"], p3_sources(), per_note={"CET1 Ratio": NOT_DISCLOSED_NOTE},
)

metric(
    "Tier 1 Capital", "£'000",
    [("Total eligible Tier 1 capital (CET1)", {"FY2024": 321877, "FY2023": 306251})],
    note=TIER1_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["Tier 1 Ratio"], p3_sources(), per_note={"Tier 1 Ratio": NOT_DISCLOSED_NOTE},
)

metric(
    "Total Capital", "£'000",
    [("Total eligible regulatory capital (CET1 + Tier 2 subordinated debt)", {"FY2024": 336877, "FY2023": 321251})],
)

bw.add_not_disclosed_metric_sheets(
    ["Total Capital Ratio", "Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in
              ["Total Capital Ratio", "Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flow from/(used in) operating activities", {"FY2025": -17143, "FY2024": 445559, "FY2023": 130953, "FY2022": 190786, "FY2021": 234303}),
        ("Net cash flow from/(used in) investing activities", {"FY2025": -459330, "FY2024": -135783, "FY2023": -39022, "FY2022": 36420, "FY2021": -147084}),
        ("Net cash flow from/(used in) financing activities", {"FY2025": 29481, "FY2024": -2292, "FY2023": 13701, "FY2022": 47034, "FY2021": -238}),
        ("Cash and cash equivalents at end of year", {"FY2025": 611903, "FY2024": 1058851, "FY2023": 751598, "FY2022": 646528, "FY2021": 372288}),
    ],
    cash_flow_unit="£'000",
    ratios=[],
    note="No Pillar 3 ratio-type metrics (CET1/Tier 1/Total Capital Ratio, Leverage Ratio, LCR, NSFR, MREL "
         "Ratio) are disclosed by Cynergy Bank in any year reviewed, so no ratios chart is shown here - see "
         "each individual Pillar 3 sheet. CET1 Capital, Tier 1 Capital and Total Capital (£'000) are "
         "disclosed for FY2023-FY2024 only, on their own sheets. Cash flow figures are duplicated from the "
         "Cash Flow Statement sheet for at-a-glance trend viewing.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CYNERGY BANK FINANCIALS.xlsx")
