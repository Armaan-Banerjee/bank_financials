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

STATEMENTS_ENTITY_NOTE = (
    ENTITY_NOTE
    + "\n\nEach year's own originally-published figures are used for the Balance Sheet, Profit & Loss and "
    "Statement of Changes in Equity below (not later restated comparatives) - the same convention already "
    "applied to the Cash Flow Statement. FY2025's own report explicitly restates FY2024 (e.g. Total assets "
    "£5,098,500k own-report vs £5,083,343k restated comparative shown in the FY2025 report) - FY2024's own "
    "Annual Report is used instead. FY2021 figures are the FY2021 comparative column within FY2022's own "
    "Annual Report (Companies House, scanned) - the FY2021 Annual Report itself was not independently "
    "re-checked, same pattern as the Cash Flow Statement's FY2021 sourcing.\n"
    "PRESENTATION NOTE: 'Current tax asset(s)' and 'Deferred tax liabilities' only appear as their own "
    "Balance Sheet lines from FY2025 onward (per that year's own restatement note); earlier years fold these "
    "into Other assets/Other liabilities - left blank rather than guessed for FY2021-FY2024. 'Assets "
    "classified as held for sale' appears only FY2022-FY2023. Subordinated loan(s) were fully repaid during "
    "FY2022 (nil at 31 Dec 2022) and re-issued during FY2023 (£14,847k) - a genuine, disclosed movement, not "
    "a data gap."
)

STATEMENTS_SOURCES = (
    "Sources - Cynergy Bank Plc's own Consolidated statement of financial position, statement of profit or "
    "loss / income statement, statement of comprehensive income, and statement of changes in equity, "
    "transcribed from each year's own report (not a later year's restated comparative):\n"
    f"FY2025 (& FY2024 restated comparative used only for the equity roll-forward's opening-balance cross-"
    f"check, not as FY2024's own figures): Cynergy Bank plc Annual Report & Accounts 2025, p.52-53 - "
    f"{AR2025_URL}\n"
    f"FY2024 (own, & FY2023 comparative cross-checked): Cynergy Bank plc Annual Report & Accounts 2024, "
    f"p.83-86 - {AR2024_URL}\n"
    f"FY2023 (own, & FY2022 comparative cross-checked): Cynergy Bank Limited Annual Report & Accounts 2023, "
    f"p.89-93 - {AR2023_URL}\n"
    f"FY2022 (own) & FY2021 (comparative): Cynergy Bank Limited Annual Report & Accounts 2022 (Companies "
    f"House filing, scanned), p.91-93 - {AR2022_CH_URL}\n\n"
    + STATEMENTS_ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Cynergy Bank Plc's own Credit Risk note (IFRS 9 staging, Consolidated Loans + Overdrafts "
    "gross carrying amount and ECL reconciliation tables combined):\n"
    f"FY2025 (& FY2024 own-report comparative used for cross-check only): Annual Report & Accounts 2025, "
    f"Note 15/Credit risk section, p.65-67 - {AR2025_URL}\n"
    f"FY2024 (own) & FY2023 (own-report comparative, cross-checked against AR2023's own FY2023 figures): "
    f"Annual Report & Accounts 2024, p.113-118 - {AR2024_URL}\n"
    f"FY2022 (own, via AR2023's own comparative column) & the FY2021 closing balance (via AR2023's own "
    f"'At 1 January 2022' opening-balance row, which is FY2021's own closing balance): Annual Report & "
    f"Accounts 2023, p.123-126 - {AR2023_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nFY2021's stage split is the FY2021 closing balance recovered from FY2022's own reconciliation "
    "table 'At 1 January' row (the FY2021 Annual Report's own credit risk note was not independently "
    "re-checked) - same 'sourced from the following year's own comparative' pattern used elsewhere in this "
    "project. Ratios (Stage 3/Total gross exposure, Total ECL/Total gross exposure coverage, Stage 3 "
    "coverage) are calculated from the gross carrying amount and ECL figures above, not separately "
    "disclosed."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with central banks",
     {"FY2025": 575031, "FY2024": 1014572, "FY2023": 697790, "FY2022": 553007, "FY2021": 324982}),
    ("DATA", "Placements with banks",
     {"FY2025": 36872, "FY2024": 44279, "FY2023": 63156, "FY2022": 102320, "FY2021": 54529}),
    ("DATA", "Loans and advances to customers",
     {"FY2025": 3745133, "FY2024": 3653477, "FY2023": 3564297, "FY2022": 3254230, "FY2021": 2949578}),
    ("DATA", "Investment in securities",
     {"FY2025": 1080929, "FY2024": 252914, "FY2023": 127547, "FY2022": 113377, "FY2021": 137782}),
    ("DATA", "Derivative assets",
     {"FY2025": 1843, "FY2024": 6404, "FY2023": 4512, "FY2022": 12404, "FY2021": 54}),
    ("DATA", "Intangible assets",
     {"FY2025": 78293, "FY2024": 63455, "FY2023": 49303, "FY2022": 27469, "FY2021": 26513}),
    ("DATA", "Right-of-use assets",
     {"FY2025": 9918, "FY2024": 11060, "FY2023": 11553, "FY2022": 11891, "FY2021": 220}),
    ("DATA", "Property and equipment",
     {"FY2025": 3080, "FY2024": 7934, "FY2023": 3861, "FY2022": 914, "FY2021": 12875}),
    ("DATA", "Assets classified as held for sale",
     {"FY2023": 7070, "FY2022": 7070}),
    ("DATA", "Other assets",
     {"FY2025": 58369, "FY2024": 44405, "FY2023": 82142, "FY2022": 42031, "FY2021": 11501}),
    ("DATA", "Current tax assets",
     {"FY2025": 7854}),
    ("TOTAL", "Total assets",
     {"FY2025": 5597322, "FY2024": 5098500, "FY2023": 4611231, "FY2022": 4124713, "FY2021": 3518034}),

    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits",
     {"FY2025": 4910863, "FY2024": 4492026, "FY2023": 3758037, "FY2022": 3336442, "FY2021": 2832564}),
    ("DATA", "Bank deposits",
     {"FY2025": 85131, "FY2024": 80924, "FY2023": 359667, "FY2022": 390170, "FY2021": 400125}),
    ("DATA", "Subordinated loan(s)",
     {"FY2025": 49805, "FY2024": 14881, "FY2023": 14847, "FY2022": 0, "FY2021": 29868}),
    ("DATA", "Lease liabilities",
     {"FY2025": 10690, "FY2024": 11895, "FY2023": 12873, "FY2022": 12065, "FY2021": 278}),
    ("DATA", "Provision for customer redress",
     {"FY2022": 716, "FY2021": 261}),
    ("DATA", "Deferred tax liabilities",
     {"FY2025": 11526}),
    ("DATA", "Derivative liabilities",
     {"FY2025": 14563, "FY2024": 11478, "FY2023": 32374, "FY2022": 3838, "FY2021": 429}),
    ("DATA", "Other liabilities",
     {"FY2025": 88515, "FY2024": 99440, "FY2023": 83883, "FY2022": 72036, "FY2021": 33793}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 5171093, "FY2024": 4710644, "FY2023": 4261681, "FY2022": 3815267, "FY2021": 3297318}),

    ("SECTION", "Equity", {}),
    ("DATA", "Share capital",
     {"FY2025": 202000, "FY2024": 202000, "FY2023": 202000, "FY2022": 202000, "FY2021": 155000}),
    ("DATA", "Property revaluation reserve",
     {"FY2024": 505, "FY2023": 2433, "FY2022": 3148, "FY2021": 1674}),
    ("DATA", "Accumulated profits",
     {"FY2025": 222240, "FY2024": 184557, "FY2023": 145003, "FY2022": 104490, "FY2021": 64191}),
    ("TOTAL", "Equity attributable to owners of the company",
     {"FY2025": 424240, "FY2024": 387062, "FY2023": 349436, "FY2022": 309638, "FY2021": 220865}),
    ("DATA", "Non-controlling interest",
     {"FY2025": 1989, "FY2024": 794, "FY2023": 114, "FY2022": -192, "FY2021": -149}),
    ("TOTAL", "Total equity",
     {"FY2025": 426229, "FY2024": 387856, "FY2023": 349550, "FY2022": 309446, "FY2021": 220716}),
    ("TOTAL", "Total liabilities and equity",
     {"FY2025": 5597322, "FY2024": 5098500, "FY2023": 4611231, "FY2022": 4124713, "FY2021": 3518034}),
]

bw.add_balance_sheet_sheet(
    title="Cynergy Bank Plc — Consolidated Statement of Financial Position",
    subtitle="Consolidated basis, £'000. See source note at bottom (presentation changes documented).",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=86,
    source_height=320,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income calculated using the effective interest method",
     {"FY2025": 328554, "FY2024": 312777, "FY2023": 276395, "FY2022": 167199, "FY2021": 105716}),
    ("DATA", "Other interest and similar income/(expense)",
     {"FY2025": 59793, "FY2024": 57827, "FY2023": 41559, "FY2022": 1610, "FY2021": -187}),
    ("DATA", "Interest expense calculated using the effective interest method",
     {"FY2025": -193820, "FY2024": -191478, "FY2023": -128355, "FY2022": -44103, "FY2021": -18356}),
    ("DATA", "Other interest expense",
     {"FY2025": -61768, "FY2024": -48550, "FY2023": -34811, "FY2022": -1578}),
    ("TOTAL", "Net interest income",
     {"FY2025": 132759, "FY2024": 130576, "FY2023": 154788, "FY2022": 123128, "FY2021": 87173}),
    ("DATA", "Fee and commission income",
     {"FY2025": 3777, "FY2024": 3089, "FY2023": 2606, "FY2022": 1667, "FY2021": 1193}),
    ("DATA", "Foreign exchange (losses)/gains",
     {"FY2025": -677, "FY2024": 712, "FY2023": 42, "FY2022": -1194, "FY2021": 1853}),
    ("DATA", "Fair value adjustment/(loss)/gain on hedging or derivative instruments",
     {"FY2025": 544, "FY2024": -204, "FY2023": 2110, "FY2022": 3983, "FY2021": -2190}),
    ("DATA", "Net gains on derecognition of financial assets",
     {"FY2025": 3578}),
    ("DATA", "Other income",
     {"FY2025": 504, "FY2024": 473}),
    ("TOTAL", "Total operating income",
     {"FY2025": 140485, "FY2024": 134646, "FY2023": 159546, "FY2022": 127584, "FY2021": 88029}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Staff costs",
     {"FY2025": -41616, "FY2024": -42783, "FY2023": -49464, "FY2022": -38334, "FY2021": -28874}),
    ("DATA", "Depreciation, amortisation and impairment/write-offs",
     {"FY2025": -12516, "FY2024": -9766, "FY2023": -7072, "FY2022": -5758, "FY2021": -3447}),
    ("DATA", "Other operating expenses",
     {"FY2025": -35284, "FY2024": -28383, "FY2023": -43684, "FY2022": -33133, "FY2021": -19912}),
    ("TOTAL", "Total operating expenses",
     {"FY2025": -89416, "FY2024": -80932, "FY2023": -100220, "FY2022": -77225, "FY2021": -52233}),
    ("DATA", "Other gains",
     {"FY2025": 404, "FY2024": 1000}),
    ("DATA", "Gain on sale of property",
     {"FY2023": 276, "FY2022": 9230}),
    ("TOTAL", "Profit before credit impairment reversals/(charges)",
     {"FY2025": 51473, "FY2024": 54714, "FY2023": 59602, "FY2022": 59589, "FY2021": 35796}),
    ("DATA", "Credit impairment reversals/(charges) on financial assets",
     {"FY2025": 91, "FY2024": -2082, "FY2023": -4445, "FY2022": -9100, "FY2021": -5396}),
    ("TOTAL", "Profit before tax",
     {"FY2025": 51564, "FY2024": 52632, "FY2023": 55157, "FY2022": 50489, "FY2021": 30400}),
    ("DATA", "Income tax expense",
     {"FY2025": -13624, "FY2024": -12398, "FY2023": -14544, "FY2022": -10233, "FY2021": -5471}),
    ("TOTAL", "Profit for the year",
     {"FY2025": 37940, "FY2024": 40234, "FY2023": 40613, "FY2022": 40256, "FY2021": 24929}),
    ("DATA", "Profit attributable to: Owners of the company",
     {"FY2025": 36745, "FY2024": 39554, "FY2023": 40307, "FY2022": 40299, "FY2021": 25078}),
    ("DATA", "Profit/(loss) attributable to: Non-controlling interest",
     {"FY2025": 1195, "FY2024": 680, "FY2023": 306, "FY2022": -43, "FY2021": -149}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Revaluation gain/(loss) on property",
     {"FY2024": -2571, "FY2022": 1474}),
    ("DATA", "Income tax relating to property revaluation",
     {"FY2024": 643, "FY2023": -509}),
    ("TOTAL", "Other comprehensive income/(expense) for the year, net of tax",
     {"FY2025": 0, "FY2024": -1928, "FY2023": -509, "FY2022": 1474, "FY2021": 0}),
    ("TOTAL", "Total comprehensive income for the year",
     {"FY2025": 37940, "FY2024": 38306, "FY2023": 40104, "FY2022": 41730, "FY2021": 24929}),
]

bw.add_income_statement_sheet(
    title="Cynergy Bank Plc — Consolidated Statement of Comprehensive Income",
    subtitle="Consolidated basis, £'000. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=86,
    source_height=320,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Property revaluation reserve", "Accumulated profits",
                   "Total attributable to owners", "Non-controlling interest", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2021 (via FY2022 report's own comparative)",
     (155000, 1674, 39113, 195787, 0, 195787)),
    ("DATA", "Profit for the year after tax", (None, None, 25078, 25078, -149, 24929)),
    ("TOTAL", "At 31 December 2021", (155000, 1674, 64191, 220865, -149, 220716)),

    ("TOTAL", "At 1 January 2022", (155000, 1674, 64191, 220865, -149, 220716)),
    ("DATA", "Profit/(loss) for the year after tax", (None, None, 40299, 40299, -43, 40256)),
    ("DATA", "Other comprehensive income (revaluation of own properties)", (None, 1474, None, 1474, None, 1474)),
    ("DATA", "Issue of share capital", (47000, None, None, 47000, None, 47000)),
    ("TOTAL", "At 31 December 2022", (202000, 3148, 104490, 309638, -192, 309446)),

    ("TOTAL", "At 1 January 2023", (202000, 3148, 104490, 309638, -192, 309446)),
    ("DATA", "Profit for the year after tax", (None, None, 40307, 40307, 306, 40613)),
    ("DATA", "Other comprehensive income (tax on property revaluation)", (None, -509, None, -509, None, -509)),
    ("DATA", "Transfer from revaluation reserve to retained earnings", (None, -206, 206, None, None, None)),
    ("TOTAL", "At 31 December 2023", (202000, 2433, 145003, 349436, 114, 349550)),

    ("TOTAL", "At 1 January 2024", (202000, 2433, 145003, 349436, 114, 349550)),
    ("DATA", "Profit for the year after tax", (None, None, 39554, 39554, 680, 40234)),
    ("DATA", "Other comprehensive income (revaluation loss on property, net of tax)", (None, -1928, None, -1928, None, -1928)),
    ("TOTAL", "At 31 December 2024", (202000, 505, 184557, 387062, 794, 387856)),

    ("TOTAL", "At 1 January 2025", (202000, 505, 184557, 387062, 794, 387856)),
    ("DATA", "Profit for the year after tax", (None, None, 36745, 36745, 1195, 37940)),
    ("DATA", "Transfer and tax release on disposal of revalued asset", (None, -505, 938, 433, None, 433)),
    ("TOTAL", "At 31 December 2025", (202000, 0, 222240, 424240, 1989, 426229)),
]

bw.add_equity_changes_sheet(
    title="Cynergy Bank Plc — Consolidated Statement of Changes in Equity",
    subtitle="Consolidated basis, £'000, chronological (oldest to newest). See source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=320,
)

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
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross carrying amount by IFRS 9 stage (Loans + Overdrafts, Consolidated)", {}),
    ("DATA", "Stage 1 gross carrying amount",
     {"FY2025": 3423245, "FY2024": 3210782, "FY2023": 2968247, "FY2022": 2826161, "FY2021": 2687050}),
    ("DATA", "Stage 2 gross carrying amount",
     {"FY2025": 259276, "FY2024": 372480, "FY2023": 549578, "FY2022": 385150, "FY2021": 232788}),
    ("DATA", "Stage 3 gross carrying amount",
     {"FY2025": 91016, "FY2024": 99046, "FY2023": 73262, "FY2022": 65258, "FY2021": 43661}),
    ("TOTAL", "Total gross carrying amount",
     {"FY2025": 3773537, "FY2024": 3682308, "FY2023": 3591087, "FY2022": 3276569, "FY2021": 2963499}),
    ("SECTION", "Expected credit loss (ECL) allowance by stage", {}),
    ("DATA", "Stage 1 ECL", {"FY2025": 3964, "FY2024": 4403, "FY2023": 5372, "FY2022": 3338, "FY2021": 2124}),
    ("DATA", "Stage 2 ECL", {"FY2025": 2951, "FY2024": 4118, "FY2023": 8485, "FY2022": 5321, "FY2021": 2175}),
    ("DATA", "Stage 3 ECL", {"FY2025": 21489, "FY2024": 20310, "FY2023": 12933, "FY2022": 13680, "FY2021": 9626}),
    ("TOTAL", "Total ECL allowance",
     {"FY2025": 28404, "FY2024": 28831, "FY2023": 26790, "FY2022": 22339, "FY2021": 13925}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 / total gross carrying amount",
     {"FY2025": "2.412%", "FY2024": "2.690%", "FY2023": "2.040%", "FY2022": "1.992%", "FY2021": "1.473%"}),
    ("DATA", "Total ECL / total gross carrying amount (overall coverage)",
     {"FY2025": "0.753%", "FY2024": "0.783%", "FY2023": "0.746%", "FY2022": "0.682%", "FY2021": "0.470%"}),
    ("DATA", "Stage 3 ECL / Stage 3 gross carrying amount (Stage 3 coverage)",
     {"FY2025": "23.61%", "FY2024": "20.51%", "FY2023": "17.65%", "FY2022": "20.96%", "FY2021": "22.05%"}),
]

bw.add_asset_quality_sheet(
    title="Cynergy Bank Plc — Asset Quality",
    subtitle="Consolidated basis, £'000 (ratios as calculated), combining the Loans and Overdrafts credit "
              "risk note tables. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=60,
    source_height=320,
    unit_suffix=" (£'000)",
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
    ["Total Capital Ratio", "Total RWAs"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Total Capital Ratio", "Total RWAs"]},
)

RWA_BREAKDOWN_NOTE = (
    "Not publicly disclosed in any of the 5 years reviewed. See the Total RWAs sheet's own note - no "
    "aggregate RWA figure, let alone a risk-category breakdown, was found in any Annual Report reviewed; "
    "confirmed by reading each report's Risk report and financial statement notes in full, not assumed "
    "absent."
)
bw.add_rwa_breakdown_sheet(
    title="Cynergy Bank Plc — RWA Breakdown",
    subtitle="Not publicly disclosed. See source note at bottom.",
    rows=[("DATA", "Not publicly disclosed", {})],
    sources_text=p3_sources() + "\n\n" + RWA_BREAKDOWN_NOTE,
    first_col_width=54,
    source_height=200,
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 5597322, "FY2024": 5098500, "FY2023": 4611231, "FY2022": 4124713, "FY2021": 3518034}),
        ("Loans and advances to customers", {"FY2025": 3745133, "FY2024": 3653477, "FY2023": 3564297, "FY2022": 3254230, "FY2021": 2949578}),
        ("Customer deposits", {"FY2025": 4910863, "FY2024": 4492026, "FY2023": 3758037, "FY2022": 3336442, "FY2021": 2832564}),
        ("Total equity", {"FY2025": 426229, "FY2024": 387856, "FY2023": 349550, "FY2022": 309446, "FY2021": 220716}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 140485, "FY2024": 134646, "FY2023": 159546, "FY2022": 127584, "FY2021": 88029}),
        ("Total operating expenses", {"FY2025": -89416, "FY2024": -80932, "FY2023": -100220, "FY2022": -77225, "FY2021": -52233}),
        ("Profit for the year", {"FY2025": 37940, "FY2024": 40234, "FY2023": 40613, "FY2022": 40256, "FY2021": 24929}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 387856, "FY2024": 349550, "FY2023": 309446, "FY2022": 220716, "FY2021": 195787}),
        ("Total comprehensive income for the year", {"FY2025": 37940, "FY2024": 38306, "FY2023": 40104, "FY2022": 41730, "FY2021": 24929}),
        ("Other equity movements, net", {"FY2025": 433, "FY2024": 0, "FY2023": 0, "FY2022": 47000, "FY2021": 0}),
        ("Closing equity", {"FY2025": 426229, "FY2024": 387856, "FY2023": 349550, "FY2022": 309446, "FY2021": 220716}),
    ],
    equity_changes_unit="£'000",
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
