import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwb-annual-report.pdf"
AR2024_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/14022025/nwb-annual-report.pdf"
AR2023_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/16022024/nwb-plc-annual-report.pdf"
AR2022_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/nwb-plc-annual-report.pdf"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00929027/filing-history/MzMzODcyODkwNGFkaXF6a2N4/document?format=pdf&download=0"
P3_2025_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwb-pillar-3-report.pdf"
P3_2024_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/14022025/nwb-pillar-3-report.pdf"
P3_2023_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/16022024/nwb-plc-pillar-3-report.pdf"
P3_2022_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/nwb-plc-pillar-3-report.pdf"
P3_2025_Q3_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/11112025/11112025-nwb-pillar-3-report.pdf"
P3_2024_Q3_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/12112024/nwb-plc-pillar-3-q3-2024.pdf"
P3_2023_Q3_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13-11-2023/natwest-bank-plc-pillar-3-q3-2023.pdf"
P3_2022_Q3_URL = "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/nwb-plc-pillar-3-report.pdf"
CH_COMPANY_URL = "https://find-and-update.company-information.service.gov.uk/company/00929027"

ENTITY_NOTE = (
    "ENTITY NOTE: This workbook covers National Westminster Bank Public Limited Company (NWB Plc), company "
    "number 00929027, FRN 121878 and LEI 213800IBT39XQ9C4CP71. It is the PRA-authorised legal entity named in "
    "the project bank list, not NatWest Group plc, NatWest Holdings Limited, RBS plc or NatWest Markets Plc. "
    "NWB Plc is a member of the UK Domestic Liquidity Sub-Group (UK DoLSub) with RBS plc and Coutts & Company; "
    "LCR and NSFR are therefore shown on the UK DoLSub basis where the entity reports that basis, rather than as "
    "NWB Plc solo figures. Companies House confirms company 00929027 and the filed 2021 accounts used below."
)


def ar_sources():
    return (
        "Sources - NWB Plc own annual accounts, £m:\n"
        f"FY2025: NWB Group Annual Report and Accounts 2025, p.96 (cash flow statement) - {AR2025_URL}\n"
        f"FY2024: NWB Group Annual Report and Accounts 2024, p.102 (cash flow statement) - {AR2024_URL}\n"
        f"FY2023: NWB Group Annual Report and Accounts 2023, p.103 (cash flow statement) - {AR2023_URL}\n"
        f"FY2022: NWB Group Annual Report and Accounts 2022, p.104 (cash flow statement) - {AR2022_URL}\n"
        f"FY2021: NWB Group Annual Report and Accounts 2022, p.104 (FY2021 comparative column; independently filed at Companies House) - {AR2022_URL}; {AR2021_URL}\n\n"
        + ENTITY_NOTE
    )


def p3_sources():
    return (
        "Sources - NWB Plc UK KM1 key metrics, PRA transitional basis:\n"
        f"FY2025: NWB Plc Pillar 3 Report 2025, p.7 - {P3_2025_URL}\n"
        f"FY2024: NWB Plc Pillar 3 Report 2024, p.7 - {P3_2024_URL}\n"
        f"FY2023: NWB Plc Pillar 3 Report 2023, p.7 - {P3_2023_URL}\n"
        f"FY2022 and FY2021: NWB Plc Pillar 3 Report 2022, p.7 (FY2021 comparative column) - {P3_2022_URL}\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook("National Westminster Bank Public Limited Company", YEARS, YEAR_LABEL, header_color="005A8D")

STATEMENTS_SOURCES = (
    "Sources - NWB Plc own annual accounts, £m:\n"
    f"FY2025/FY2024: NWB Group Annual Report and Accounts 2025, Balance sheet p.93, Statement of changes in equity p.94 - {AR2025_URL}\n"
    f"FY2023/FY2022: NWB Group Annual Report and Accounts 2023, Balance sheet p.100, Statement of changes in equity p.101 - {AR2023_URL}\n"
    f"FY2021 (and FY2022 cross-check): NWB Group Annual Report and Accounts 2022, Balance sheet p.101, Statement of changes in equity p.102 - {AR2022_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    "BASIS NOTE - Profit & Loss: as permitted by s.408(3) Companies Act 2006, NWB Plc has not presented a standalone "
    "income statement or statement of comprehensive income in any of the 5 reviewed Annual Reports - only the NWB Group "
    "consolidated income statement is published. The Profit & Loss sheet is therefore shown on NWB Group basis (not "
    "NWB Plc entity-level like the Balance Sheet and Statement of Changes in Equity). NWB Plc's own profit for the year "
    "(disclosed only as a single headline figure via a Balance Sheet footnote) is close to but not identical to the "
    "Group figure each year (e.g. FY2025: NWB Plc £4,227m vs NWB Group £4,198m) - the difference reflects dividend "
    "income and other items that differ between the solo and consolidated bases.\n\n"
    "BASIS NOTE - Balance Sheet and Statement of Changes in Equity: both are shown on the NWB Plc entity-level column "
    "of each report's Group/Plc comparative tables, consistent with the Cash Flow Statement and Pillar 3 sheets. "
    "NWB Plc's own Total equity carries no non-controlling interests (NCI only arises at NWB Group level)."
)

# ---------------------------------------------------------------
# Balance Sheet (NWB Plc entity-level column of each report's own
# NWB Group / NWB Plc comparative table). Total assets = Total liabilities +
# Total equity exactly in every year - zero plug rows.
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 29911, "FY2024": 35083, "FY2023": 48238, "FY2022": 73062, "FY2021": 101210}),
    ("DATA", "Derivatives", {"FY2025": 1106, "FY2024": 2892, "FY2023": 3213, "FY2022": 4430, "FY2021": 2547}),
    ("DATA", "Loans to banks - amortised cost", {"FY2025": 4261, "FY2024": 3148, "FY2023": 3043, "FY2022": 2870, "FY2021": 3638}),
    ("DATA", "Loans to customers - amortised cost", {"FY2025": 310121, "FY2024": 297548, "FY2023": 284314, "FY2022": 267401, "FY2021": 255443}),
    ("DATA", "Amounts due from holding companies and fellow subsidiaries", {"FY2025": 38965, "FY2024": 36383, "FY2023": 33499, "FY2022": 32133, "FY2021": 27122}),
    ("DATA", "Securities subject to repurchase agreements", {"FY2025": 15004, "FY2024": 8984, "FY2023": 6469, "FY2022": 2140, "FY2021": 10813}),
    ("DATA", "Other financial assets excluding securities subject to repurchase agreements", {"FY2025": 37152, "FY2024": 29814, "FY2023": 24623, "FY2022": 12040, "FY2021": 17836}),
    ("TOTAL", "Other financial assets", {"FY2025": 52156, "FY2024": 38798, "FY2023": 31092, "FY2022": 14180, "FY2021": 28649}),
    ("DATA", "Investment in group undertakings", {"FY2025": 2477, "FY2024": 2520, "FY2023": 2615, "FY2022": 2030, "FY2021": 2319}),
    ("DATA", "Other assets", {"FY2025": 5652, "FY2024": 5503, "FY2023": 5735, "FY2022": 5641, "FY2021": 5183}),
    ("TOTAL", "Total assets", {"FY2025": 444649, "FY2024": 421875, "FY2023": 411749, "FY2022": 401747, "FY2021": 426111}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Bank deposits", {"FY2025": 33016, "FY2024": 24778, "FY2023": 18052, "FY2022": 16059, "FY2021": 22829}),
    ("DATA", "Customer deposits", {"FY2025": 282427, "FY2024": 275972, "FY2023": 276202, "FY2022": 281558, "FY2021": 292470}),
    ("DATA", "Amounts due to holding companies and fellow subsidiaries", {"FY2025": 98661, "FY2024": 90925, "FY2023": 84174, "FY2022": 75037, "FY2021": 76722}),
    ("DATA", "Derivatives", {"FY2025": 780, "FY2024": 1323, "FY2023": 2014, "FY2022": 2582, "FY2021": 4336}),
    ("DATA", "Other financial liabilities", {"FY2025": 3670, "FY2024": 3824, "FY2023": 8147, "FY2022": 4525, "FY2021": 6384}),
    ("DATA", "Subordinated liabilities", {"FY2025": 119, "FY2024": 119, "FY2023": 119, "FY2022": 191, "FY2021": 205}),
    ("DATA", "Notes in circulation", {"FY2025": 1049, "FY2024": 935, "FY2023": 806, "FY2022": 809, "FY2021": 904}),
    ("DATA", "Other liabilities", {"FY2025": 2242, "FY2024": 2390, "FY2023": 2534, "FY2022": 2743, "FY2021": 3095}),
    ("TOTAL", "Total liabilities", {"FY2025": 421964, "FY2024": 400266, "FY2023": 392048, "FY2022": 383504, "FY2021": 406945}),
    ("SECTION", "Equity", {}),
    ("TOTAL", "Total equity (owners' equity - no NCI at NWB Plc solo level)", {"FY2025": 22685, "FY2024": 21609, "FY2023": 19701, "FY2022": 18243, "FY2021": 19166}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 444649, "FY2024": 421875, "FY2023": 411749, "FY2022": 401747, "FY2021": 426111}),
]
bw.add_balance_sheet_sheet(
    title="National Westminster Bank Plc — Balance Sheet",
    subtitle="NWB Plc entity-level basis (the Plc column of each report's Group/Plc comparative table), £m.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss - NWB Group basis (NWB Plc takes the s.408(3) Companies Act
# 2006 exemption and publishes no standalone income statement - see
# BASIS NOTE in STATEMENTS_SOURCES).
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 19148, "FY2024": 18100, "FY2023": 14764, "FY2022": 9159, "FY2021": 6721}),
    ("DATA", "Interest payable", {"FY2025": -9497, "FY2024": -9892, "FY2023": -6741, "FY2022": -1627, "FY2021": -719}),
    ("TOTAL", "Net interest income", {"FY2025": 9651, "FY2024": 8208, "FY2023": 8023, "FY2022": 7532, "FY2021": 6002}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 2419, "FY2024": 2276, "FY2023": 2177, "FY2022": 2119, "FY2021": 1862}),
    ("DATA", "Fees and commissions payable", {"FY2025": -597, "FY2024": -542, "FY2023": -508, "FY2022": -493, "FY2021": -380}),
    ("DATA", "Other operating income", {"FY2025": 2147, "FY2024": 2031, "FY2023": 2394, "FY2022": 2585, "FY2021": 1785}),
    ("TOTAL", "Non-interest income", {"FY2025": 3969, "FY2024": 3765, "FY2023": 4063, "FY2022": 4211, "FY2021": 3267}),
    ("TOTAL", "Total income", {"FY2025": 13620, "FY2024": 11973, "FY2023": 12086, "FY2022": 11743, "FY2021": 9269}),
    ("DATA", "Staff costs", {"FY2025": -3392, "FY2024": -3301, "FY2023": -3109, "FY2022": -2896, "FY2021": -2815}),
    ("DATA", "Premises and equipment", {"FY2025": -1183, "FY2024": -1099, "FY2023": -1039, "FY2022": -994, "FY2021": -948}),
    ("DATA", "Other administrative expenses", {"FY2025": -1588, "FY2024": -1576, "FY2023": -1768, "FY2022": -1630, "FY2021": -1660}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -1078, "FY2024": -987, "FY2023": -877, "FY2022": -768, "FY2021": -776}),
    ("TOTAL", "Operating expenses", {"FY2025": -7241, "FY2024": -6963, "FY2023": -6793, "FY2022": -6288, "FY2021": -6199}),
    ("TOTAL", "Profit before impairment losses/(releases)", {"FY2025": 6379, "FY2024": 5010, "FY2023": 5293, "FY2022": 5455, "FY2021": 3070}),
    ("DATA", "Impairment losses/(releases)", {"FY2025": -653, "FY2024": -347, "FY2023": -504, "FY2022": -341, "FY2021": 813}),
    ("TOTAL", "Operating profit before tax", {"FY2025": 5726, "FY2024": 4663, "FY2023": 4789, "FY2022": 5114, "FY2021": 3883}),
    ("DATA", "Tax charge", {"FY2025": -1528, "FY2024": -1238, "FY2023": -1280, "FY2022": -1425, "FY2021": -976}),
    ("TOTAL", "Profit for the year", {"FY2025": 4198, "FY2024": 3425, "FY2023": 3509, "FY2022": 3689, "FY2021": 2907}),
    ("SECTION", "Other comprehensive income, net of tax", {}),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", {"FY2025": 0, "FY2024": -111, "FY2023": -107, "FY2022": -410, "FY2021": -373}),
    ("DATA", "FVOCI financial assets", {"FY2025": 115, "FY2024": -28, "FY2023": 43, "FY2022": -392, "FY2021": -96}),
    ("DATA", "Cash flow hedges", {"FY2025": 73, "FY2024": 405, "FY2023": -290, "FY2022": -542, "FY2021": 180}),
    ("DATA", "Currency translation", {"FY2025": 6, "FY2024": -18, "FY2023": -17, "FY2022": -2, "FY2021": -22}),
    ("DATA", "Tax on items that qualify for reclassification", {"FY2025": -54, "FY2024": -107, "FY2023": 73, "FY2022": 276, "FY2021": -40}),
    ("TOTAL", "Other comprehensive income/(loss) after tax", {"FY2025": 140, "FY2024": 141, "FY2023": -298, "FY2022": -1070, "FY2021": -351}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 4338, "FY2024": 3566, "FY2023": 3211, "FY2022": 2619, "FY2021": 2556}),
]
bw.add_income_statement_sheet(
    title="National Westminster Bank Plc — Profit & Loss",
    subtitle="NWB Group basis (Consolidated income statement / statement of comprehensive income) - NWB Plc "
              "publishes no standalone income statement, see BASIS NOTE in the source citation. £m.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - NWB Plc entity-level column, chronological
# roll-forward. Equity reconciliation ladder confirmed: every year's own
# closing balance ties exactly to both the next year's own opening balance
# and that year's own Balance Sheet Total equity - zero plug rows needed
# anywhere across all 5 years. Ladder's mandated scan caught the "easy to
# skip" reserve-transfer items (merger reserve amortisation, capital
# redemption reserve movements from preference share redemptions) that
# net to zero on Total equity but move real balances between components.
# ---------------------------------------------------------------
equity_headers = [
    "Called-up share capital", "Paid-in equity", "Share premium account", "Merger reserve",
    "FVOCI reserve", "Cash flow hedging reserve", "Foreign exchange reserve",
    "Capital redemption reserve", "Retained earnings", "Total equity",
]
equity_rows = [
    ("TOTAL", "At 1 January 2021 (FY2021 opening)", (1678, 2370, 2225, -140, 279, -133, -13, 796, 11402, 18464)),
    ("DATA", "Paid-in equity redeemed", (None, -934, None, None, None, None, None, None, None, -934)),
    ("DATA", "Paid-in equity issued", (None, 941, None, None, None, None, None, None, None, 941)),
    ("DATA", "Merger reserve amortisation (transfer to/from retained earnings)", (None, None, None, 51, None, None, None, None, -51, 0)),
    ("DATA", "FVOCI reserve - unrealised gains", (None, None, None, None, 28, None, None, None, None, 28)),
    ("DATA", "FVOCI reserve - realised gains", (None, None, None, None, -122, None, None, None, None, -122)),
    ("DATA", "FVOCI reserve - tax", (None, None, None, None, 8, None, None, None, None, 8)),
    ("DATA", "Cash flow hedging reserve - amount recognised in equity", (None, None, None, None, None, 100, None, None, None, 100)),
    ("DATA", "Cash flow hedging reserve - amount transferred to earnings", (None, None, None, None, None, 79, None, None, None, 79)),
    ("DATA", "Cash flow hedging reserve - tax", (None, None, None, None, None, -48, None, None, None, -48)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, None, None, -18, None, None, -18)),
    ("DATA", "Foreign exchange reserve - FX gains on hedges of net assets", (None, None, None, None, None, None, 15, None, None, 15)),
    ("DATA", "Capital redemption reserve - redemption of preference shares (transfer from retained earnings)", (None, None, None, None, None, None, None, 24, -24, 0)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 2752, 2752)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, None, None, None, -1600, -1600)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, None, None, -109, -109)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, -386, -386)),
    ("DATA", "Redemption/reclassification of paid-in equity, net of tax", (None, None, None, None, None, None, None, None, -18, -18)),
    ("DATA", "Share-based payments, net of tax", (None, None, None, None, None, None, None, None, 4, 4)),
    ("DATA", "Employee share schemes", (None, None, None, None, None, None, None, None, 10, 10)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (1678, 2377, 2225, -89, 193, -2, -16, 820, 11980, 19166)),
    ("DATA", "Paid-in equity redeemed", (None, -359, None, None, None, None, None, None, None, -359)),
    ("DATA", "Paid-in equity issued", (None, 500, None, None, None, None, None, None, None, 500)),
    ("DATA", "Merger reserve amortisation (transfer to/from retained earnings)", (None, None, None, 87, None, None, None, None, -87, 0)),
    ("DATA", "FVOCI reserve - unrealised losses", (None, None, None, None, -486, None, None, None, None, -486)),
    ("DATA", "FVOCI reserve - realised losses", (None, None, None, None, 93, None, None, None, None, 93)),
    ("DATA", "FVOCI reserve - tax", (None, None, None, None, 124, None, None, None, None, 124)),
    ("DATA", "Cash flow hedging reserve - amount recognised in equity", (None, None, None, None, None, -288, None, None, None, -288)),
    ("DATA", "Cash flow hedging reserve - amount transferred to earnings", (None, None, None, None, None, -255, None, None, None, -255)),
    ("DATA", "Cash flow hedging reserve - tax", (None, None, None, None, None, 152, None, None, None, 152)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, None, None, 31, None, None, 31)),
    ("DATA", "Foreign exchange reserve - FX losses on hedges of net assets", (None, None, None, None, None, None, -33, None, None, -33)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 3457, 3457)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, None, None, None, -3293, -3293)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, None, None, -120, -120)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, -419, -419)),
    ("DATA", "Redemption/reclassification of paid-in equity, net of tax", (None, None, None, None, None, None, None, None, -35, -35)),
    ("DATA", "Share-based payments, net of tax", (None, None, None, None, None, None, None, None, 2, 2)),
    ("DATA", "Employee share schemes", (None, None, None, None, None, None, None, None, 6, 6)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (1678, 2518, 2225, -2, -76, -393, -18, 820, 11491, 18243)),
    ("DATA", "Merger reserve amortisation (transfer to/from retained earnings)", (None, None, None, 2, None, None, None, None, -2, 0)),
    ("DATA", "FVOCI reserve - unrealised losses", (None, None, None, None, -11, None, None, None, None, -11)),
    ("DATA", "FVOCI reserve - realised losses", (None, None, None, None, 43, None, None, None, None, 43)),
    ("DATA", "FVOCI reserve - tax", (None, None, None, None, -8, None, None, None, None, -8)),
    ("DATA", "Cash flow hedging reserve - amount recognised in equity", (None, None, None, None, None, -180, None, None, None, -180)),
    ("DATA", "Cash flow hedging reserve - amount transferred to earnings", (None, None, None, None, None, -109, None, None, None, -109)),
    ("DATA", "Cash flow hedging reserve - tax", (None, None, None, None, None, 81, None, None, None, 81)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, None, None, -12, None, None, -12)),
    ("DATA", "Foreign exchange reserve - FX gains on hedges of net assets", (None, None, None, None, None, None, 12, None, None, 12)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 3625, 3625)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, None, None, None, -1738, -1738)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, None, None, -142, -142)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, -100, -100)),
    ("DATA", "Share-based payments, net of tax", (None, None, None, None, None, None, None, None, -3, -3)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (1678, 2518, 2225, 0, -52, -601, -18, 820, 13131, 19701)),
    ("DATA", "Paid-in equity issued", (None, 799, None, None, None, None, None, None, None, 799)),
    ("DATA", "FVOCI reserve - unrealised gains/(losses)", (None, None, None, None, -52, None, None, None, None, -52)),
    ("DATA", "FVOCI reserve - realised losses", (None, None, None, None, 32, None, None, None, None, 32)),
    ("DATA", "FVOCI reserve - tax", (None, None, None, None, 6, None, None, None, None, 6)),
    ("DATA", "Cash flow hedging reserve - amounts recognised in equity", (None, None, None, None, None, 125, None, None, None, 125)),
    ("DATA", "Cash flow hedging reserve - reclassification of OCI to profit or loss", (None, None, None, None, None, 283, None, None, None, 283)),
    ("DATA", "Cash flow hedging reserve - tax", (None, None, None, None, None, -114, None, None, None, -114)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, None, None, -28, None, None, -28)),
    ("DATA", "Foreign exchange reserve - FX losses on hedges of net assets", (None, None, None, None, None, None, 16, None, None, 16)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 3613, 3613)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, None, None, None, -2516, -2516)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, None, None, -194, -194)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, -100, -100)),
    ("DATA", "Employee share schemes, net of tax", (None, None, None, None, None, None, None, None, 22, 22)),
    ("DATA", "Share-based remuneration, net of tax", (None, None, None, None, None, None, None, None, 16, 16)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (1678, 3317, 2225, 0, -66, -307, -30, 820, 13972, 21609)),
    ("DATA", "Paid-in equity redeemed", (None, -1877, None, None, None, None, None, None, None, -1877)),
    ("DATA", "Paid-in equity issued", (None, 1741, None, None, None, None, None, None, None, 1741)),
    ("DATA", "FVOCI reserve - unrealised gains", (None, None, None, None, 111, None, None, None, None, 111)),
    ("DATA", "FVOCI reserve - realised losses", (None, None, None, None, 7, None, None, None, None, 7)),
    ("DATA", "FVOCI reserve - tax", (None, None, None, None, -34, None, None, None, None, -34)),
    ("DATA", "Cash flow hedging reserve - amounts recognised in equity", (None, None, None, None, None, -33, None, None, None, -33)),
    ("DATA", "Cash flow hedging reserve - reclassification of OCI to profit or loss", (None, None, None, None, None, 105, None, None, None, 105)),
    ("DATA", "Cash flow hedging reserve - tax", (None, None, None, None, None, -20, None, None, None, -20)),
    ("DATA", "Foreign exchange reserve - retranslation of net assets", (None, None, None, None, None, None, 30, None, None, 30)),
    ("DATA", "Foreign exchange reserve - FX losses on hedges of net assets", (None, None, None, None, None, None, -17, None, None, -17)),
    ("DATA", "Foreign exchange reserve - recycled to profit or loss on disposal of businesses", (None, None, None, None, None, None, -2, None, None, -2)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 4227, 4227)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, None, None, None, -2988, -2988)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, None, None, -233, -233)),
    ("DATA", "Redemption/reclassification of paid-in equity", (None, None, None, None, None, None, None, None, -34, -34)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, None, None, 2, 2)),
    ("DATA", "Employee share schemes, net of tax", (None, None, None, None, None, None, None, None, 19, 19)),
    ("DATA", "Share-based remuneration, net of tax", (None, None, None, None, None, None, None, None, 23, 23)),
    ("DATA", "Sharing in success", (None, None, None, None, None, None, None, None, 49, 49)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (1678, 3181, 2225, 0, 18, -255, -19, 820, 15037, 22685)),
]
bw.add_equity_changes_sheet(
    title="National Westminster Bank Plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, NWB Plc entity-level basis. £m. Equity reconciliation "
              "ladder confirmed: every year's own closing balance ties exactly to both the next year's own opening "
              "balance and that year's own Balance Sheet Total equity - zero plug rows needed anywhere across all "
              "5 years.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
)

# The 2023-2025 reports use condensed cash-flow presentation; 2022 provides the detailed 2022/2021 comparative.
cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Operating profit before tax", {"FY2025": 5591, "FY2024": 4680, "FY2023": 4705, "FY2022": 4687, "FY2021": 3542}),
    ("DATA", "Non-cash and other items", {"FY2025": -62, "FY2024": 1424, "FY2023": 396}),
    ("DATA", "Impairment losses/(releases)", {"FY2022": 389, "FY2021": -732}),
    ("DATA", "Depreciation and amortisation", {"FY2022": 598, "FY2021": 594}),
    ("DATA", "Net impairment charges of investments in Group undertakings", {"FY2022": 336, "FY2021": 61}),
    ("DATA", "Change in fair value on financial assets", {"FY2022": 1177, "FY2021": 1595}),
    ("DATA", "Change in fair value on financial liabilities and subordinated liabilities", {"FY2022": -924, "FY2021": -418}),
    ("DATA", "Elimination of foreign exchange differences", {"FY2022": -3, "FY2021": 1118}),
    ("DATA", "Other non-cash items", {"FY2022": -215, "FY2021": 58}),
    ("DATA", "Income receivable on other financial assets", {"FY2022": -303, "FY2021": -412}),
    ("DATA", "Dividends receivable from subsidiaries", {"FY2022": -1010, "FY2021": -424}),
    ("DATA", "Interest payable on MRELs and subordinated liabilities", {"FY2022": 358, "FY2021": 310}),
    ("DATA", "Charges and releases on provisions", {"FY2022": 122, "FY2021": 388}),
    ("DATA", "Defined benefit pension schemes", {"FY2022": 132, "FY2021": 146}),
    ("TOTAL", "Net cash flows from trading activities", {"FY2022": 5443, "FY2021": 6038}),
    ("DATA", "Changes in operating assets and liabilities", {"FY2025": 9514, "FY2024": -7007, "FY2023": -8999, "FY2022": -45374, "FY2021": 31327}),
    ("DATA", "Income taxes paid", {"FY2025": -1515, "FY2024": -993, "FY2023": -484, "FY2022": -998, "FY2021": -791}),
    ("TOTAL", "Net cash flows from operating activities", {"FY2025": 13528, "FY2024": -1896, "FY2023": -4382, "FY2022": -40929, "FY2021": 36574}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Sale and maturity of other financial assets", {"FY2025": 31898, "FY2024": 33860, "FY2023": 17887, "FY2022": 25339, "FY2021": 9884}),
    ("DATA", "Purchase of other financial assets", {"FY2025": -44449, "FY2024": -41551, "FY2023": -34249, "FY2022": -13022, "FY2021": -2811}),
    ("DATA", "Income received on other financial assets", {"FY2025": 1404, "FY2024": 768, "FY2023": 435, "FY2022": 371, "FY2021": 412}),
    ("DATA", "Net movement in business interests and intangible assets", {"FY2025": -401, "FY2024": -2861, "FY2023": -1188, "FY2022": -719, "FY2021": -3093}),
    ("DATA", "Dividends received from subsidiaries", {"FY2025": 487, "FY2024": 553, "FY2023": 617, "FY2022": 1010, "FY2021": 424}),
    ("DATA", "Sale of property, plant and equipment", {"FY2025": 36, "FY2024": 101, "FY2023": 34, "FY2022": 82, "FY2021": 17}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -237, "FY2024": -252, "FY2023": -544, "FY2022": -316, "FY2021": -617}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": -11262, "FY2024": -9382, "FY2023": -17008, "FY2022": 12745, "FY2021": 4216}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of paid-in equity", {"FY2025": 1741, "FY2024": 799, "FY2022": 500, "FY2021": 941}),
    ("DATA", "Redemption of paid-in equity", {"FY2025": -1911, "FY2022": -388, "FY2021": -934}),
    ("DATA", "Issue of subordinated liabilities", {"FY2025": 830, "FY2024": 600, "FY2023": 1263}),
    ("DATA", "Redemption of subordinated liabilities", {"FY2025": -500, "FY2024": -579, "FY2023": -539}),
    ("DATA", "Interest paid on subordinated liabilities", {"FY2025": -174, "FY2024": -159, "FY2023": -120}),
    ("DATA", "Movement in subordinated liabilities", {"FY2022": -199, "FY2021": -1267}),
    ("DATA", "Movement in MRELs", {"FY2022": 509, "FY2021": 1515}),
    ("DATA", "Issue of MRELs", {"FY2025": 1544, "FY2024": 927, "FY2023": 441}),
    ("DATA", "Maturity and redemption of MRELs", {"FY2025": 0, "FY2024": -930, "FY2023": -107}),
    ("DATA", "Interest paid on MRELs", {"FY2025": -227, "FY2024": -215, "FY2023": -261}),
    ("DATA", "Dividends paid", {"FY2025": -3221, "FY2024": -2710, "FY2023": -1880, "FY2022": -3413, "FY2021": -1709}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": -1918, "FY2024": -2267, "FY2023": -1203, "FY2022": -2991, "FY2021": -1454}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2025": 141, "FY2024": -259, "FY2023": -397, "FY2022": 1101, "FY2021": -984}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 489, "FY2024": -13804, "FY2023": -22990, "FY2022": -30074, "FY2021": 38352}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 38678, "FY2024": 52482, "FY2023": 75472, "FY2022": 105546, "FY2021": 67194}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 39167, "FY2024": 38678, "FY2023": 52482, "FY2022": 75472, "FY2021": 105546}),
]
bw.add_cash_flow_sheet("National Westminster Bank Plc — Cash Flow Statement", "NWB Plc entity-level basis, £m. " + ENTITY_NOTE, cash_rows, ar_sources(), first_col_width=80, source_height=240, unit_suffix=" (£m)")

# ---------------------------------------------------------------
# Asset Quality - NWB Plc entity-level loan exposure/ECL by IFRS 9 stage
# (Note 13 "Loan impairment provisions" of each Annual Report). All 5 years
# fully disclosed at NWB Plc level - no access gaps.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans - amortised cost (and FVOCI from FY2025), by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2025": 287175, "FY2024": 268368, "FY2023": 258188, "FY2022": 236809, "FY2021": 236255}),
    ("DATA", "Stage 2", {"FY2025": 27117, "FY2024": 31101, "FY2023": 28008, "FY2022": 32765, "FY2021": 22492}),
    ("DATA", "Stage 3", {"FY2025": 3212, "FY2024": 4112, "FY2023": 4003, "FY2022": 3383, "FY2021": 2548}),
    ("DATA", "Inter-group (classified Stage 1)", {"FY2025": 37823, "FY2024": 34942, "FY2023": 32200, "FY2022": 30633, "FY2021": 25362}),
    ("TOTAL", "Total loans - amortised cost (and FVOCI from FY2025)", {"FY2025": 355327, "FY2024": 338523, "FY2023": 322400, "FY2022": 303590, "FY2021": 286657}),
    ("SECTION", "ECL provisions, by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2025": 483, "FY2024": 442, "FY2023": 521, "FY2022": 459, "FY2021": 207}),
    ("DATA", "Stage 2", {"FY2025": 633, "FY2024": 624, "FY2023": 746, "FY2022": 765, "FY2021": 1026}),
    ("DATA", "Stage 3", {"FY2025": 1645, "FY2024": 1482, "FY2023": 1416, "FY2022": 1170, "FY2021": 1037}),
    ("DATA", "Inter-group", {"FY2025": 30, "FY2024": 39, "FY2023": 41, "FY2022": 48, "FY2021": 8}),
    ("TOTAL", "Total ECL provisions", {"FY2025": 2791, "FY2024": 2587, "FY2023": 2724, "FY2022": 2442, "FY2021": 2278}),
    ("SECTION", "ECL provision coverage (ECL provisions / loans - amortised cost and FVOCI)", {}),
    ("DATA", "Stage 1 coverage", {"FY2025": "0.17%", "FY2024": "0.16%", "FY2023": "0.20%", "FY2022": "0.19%", "FY2021": "0.09%"}),
    ("DATA", "Stage 2 coverage", {"FY2025": "2.33%", "FY2024": "2.01%", "FY2023": "2.70%", "FY2022": "2.33%", "FY2021": "4.56%"}),
    ("DATA", "Stage 3 coverage (NPL coverage)", {"FY2025": "51.21%", "FY2024": "36.04%", "FY2023": "35.40%", "FY2022": "34.58%", "FY2021": "40.70%"}),
    ("DATA", "Total coverage", {"FY2025": "0.87%", "FY2024": "0.84%", "FY2023": "0.92%", "FY2022": "0.88%", "FY2021": "0.87%"}),
    ("SECTION", "Impairment (releases)/losses - ECL (release)/charge for the year", {}),
    ("DATA", "Stage 1", {"FY2025": -135, "FY2024": -335, "FY2023": -302, "FY2022": -256, "FY2021": -945}),
    ("DATA", "Stage 2", {"FY2025": 354, "FY2024": 316, "FY2023": 516, "FY2022": 373, "FY2021": 48}),
    ("DATA", "Stage 3", {"FY2025": 399, "FY2024": 356, "FY2023": 276, "FY2022": 234, "FY2021": 183}),
    ("DATA", "Third party", {"FY2025": 618, "FY2024": 337, "FY2023": 490, "FY2022": 351, "FY2021": -714}),
    ("DATA", "Inter-group", {"FY2025": -9, "FY2024": -3, "FY2023": -7, "FY2022": 40, "FY2021": -18}),
    ("TOTAL", "Total ECL (release)/charge", {"FY2025": 609, "FY2024": 334, "FY2023": 483, "FY2022": 391, "FY2021": -732}),
    ("DATA", "Amounts written-off", {"FY2025": 454, "FY2024": 536, "FY2023": 218, "FY2022": 272, "FY2021": 352}),
]
bw.add_asset_quality_sheet(
    title="National Westminster Bank Plc — Asset Quality",
    subtitle="NWB Plc entity-level basis, Note 13 'Loan impairment provisions' loan exposure and impairment metrics. £m.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nFY2025/FY2024: Annual Report and Accounts 2025, Note 13 'Loan impairment provisions', p.143. "
        "FY2023/FY2022: Annual Report and Accounts 2023, Note 13, p.148. FY2021 (and FY2022 cross-check): "
        "Annual Report and Accounts 2022, Note 13, p.149. Coverage percentages are as disclosed (rounded by the "
        "source, not recalculated). Inter-group balances (classified Stage 1 per the source's own footnote) are "
        "kept as their own row rather than folded into Stage 1, matching the source table's own structure."
    ),
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£m)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, p3_sources(), note=note, first_col_width=55, source_height=150)


metric("CET1 Capital", "£m", [("Common equity tier 1 (CET1) capital", {"FY2025": 14968, "FY2024": 14181, "FY2023": 14082, "FY2022": 12713, "FY2021": 13924})])
metric("CET1 Ratio", "% of RWA", [("Common equity tier 1 (CET1) ratio", {"FY2025": "11.2%", "FY2024": "11.4%", "FY2023": "11.6%", "FY2022": "11.3%", "FY2021": "16.1%"})])
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 17910, "FY2024": 17258, "FY2023": 16360, "FY2022": 14956, "FY2021": 16039})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "13.4%", "FY2024": "13.9%", "FY2023": "13.4%", "FY2022": "13.3%", "FY2021": "18.6%"})])
metric("Total Capital", "£m", [("Total capital", {"FY2025": 21701, "FY2024": 20629, "FY2023": 19798, "FY2022": 17877, "FY2021": 18945})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "16.2%", "FY2024": "16.6%", "FY2023": "16.3%", "FY2022": "15.9%", "FY2021": "22.0%"})])
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", {"FY2025": 133749, "FY2024": 124522, "FY2023": 121740, "FY2022": 112428, "FY2021": 86217})])

# RWA Breakdown - Pillar 3 UK OV1 template, placed right after Total RWAs per
# the locked sheet order. FY2025-FY2022 all tie exactly to the Total RWAs
# figures above. FY2021's breakdown was located this session (ST-028
# follow-up): NWB Plc did not publish its own standalone Pillar 3 report for
# FY2021 (that only started with the FY2022 report cycle) - instead its OV1
# table for FY2021 appears as a large-subsidiary column inside the NatWest
# Holdings Group Pillar 3 Report 2021 (NWH Group, NWB Plc, RBS plc, UBIDAC
# and Coutts & Co side by side), p.25. Found via Wayback Machine CDX search
# against investors.natwestgroup.com/results-center/18022022/ after the live
# site's search/index no longer surfaces it - archived copy:
# https://web.archive.org/web/20220218072522/https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/18022022/nwh-pillar-3-supplement-fy-2021.pdf
#
# Note a methodology/template difference versus FY2022 onward: in this
# FY2021 table the "Amounts below the thresholds for deduction" memo row is
# NOT already embedded in the Credit risk row (unlike FY2022-FY2025) - it is
# additive to reach the Total. Row-for-row figures below are exactly as
# reported; the FY2021 Total (86,217) ties precisely to the existing Total
# RWAs figure for FY2021 used elsewhere in this workbook, confirming the
# reconciliation: 66,419 + 574 + 1,054 + 53 + 12,874 + 5,243 = 86,217.
NWH_P3_2021_URL = "https://web.archive.org/web/20220218072522/https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/18022022/nwh-pillar-3-supplement-fy-2021.pdf"
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2025": 110314, "FY2024": 106185, "FY2023": 105860, "FY2022": 98731, "FY2021": 66419}),
    ("DATA", "Counterparty credit risk", {"FY2025": 600, "FY2024": 606, "FY2023": 713, "FY2022": 497, "FY2021": 574}),
    ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {"FY2025": 4050, "FY2024": 1737, "FY2023": 836, "FY2022": 182, "FY2021": 1054}),
    ("DATA", "Position, foreign exchange and commodities risk (market risk)", {"FY2025": 23, "FY2024": 71, "FY2023": 12, "FY2022": 26, "FY2021": 53}),
    ("DATA", "Operational risk", {"FY2025": 18762, "FY2024": 15923, "FY2023": 14319, "FY2022": 12992, "FY2021": 12874}),
    ("DATA", "Memo: Amounts below the thresholds for deduction (subject to 250% risk-weight; FY2022-FY2025 non-additive/already in Credit risk above, FY2021 additive to Total - see code comment above)", {"FY2025": 4703, "FY2024": 4711, "FY2023": 4743, "FY2022": 4561, "FY2021": 5243}),
    ("TOTAL", "Total", {"FY2025": 133749, "FY2024": 124522, "FY2023": 121740, "FY2022": 112428, "FY2021": 86217}),
]
bw.add_rwa_breakdown_sheet(
    title="National Westminster Bank Plc — RWA Breakdown",
    subtitle="NWB Plc entity-level basis, Pillar 3 UK OV1 template (top-level risk-type categories). £m.",
    rows=rwa_breakdown_rows,
    sources_text=(
        f"Sources - NWB Plc UK OV1 tables:\n"
        f"FY2025: NWB Plc Pillar 3 Report 2025, p.8 - {P3_2025_URL}\n"
        f"FY2024: NWB Plc Pillar 3 Report 2024, p.9 - {P3_2024_URL}\n"
        f"FY2023: NWB Plc Pillar 3 Report 2023, p.9 - {P3_2023_URL}\n"
        f"FY2022: NWB Plc Pillar 3 Report 2022, p.8 - {P3_2022_URL}\n"
        f"FY2021: NWH Group Pillar 3 Report 2021, OV1 table (NWB Plc large-subsidiary column), p.25 - {NWH_P3_2021_URL}\n\n"
        + ENTITY_NOTE + "\n\n"
        "Settlement risk (row 15 of the UK OV1 template) is nil across all 5 available years and is omitted as a "
        "row here rather than shown as an all-zero line. The 'Amounts below the thresholds for deduction' memo "
        "row is shown for information only: for FY2022-FY2025 it is already included within Credit risk above "
        "and is NOT additive to the Total (per those reports' own template footnote); for FY2021 the NWH Group "
        "Pillar 3 Report 2021's OV1 table presents it as a distinct, ADDITIVE line - Credit risk excludes it, and "
        "it must be added to reach the Total. This reflects a genuine definitional difference between the FY2021 "
        "and FY2022 OV1 disclosures, not a transcription inconsistency; the FY2021 row values are exactly as "
        "reported and the Total (86,217) ties to the Total RWAs figure used elsewhere in this workbook."
    ),
    first_col_width=90,
    source_height=220,
    unit_suffix=" (£m)",
)

metric("Leverage Ratio", "£m / %", [("Leverage exposure measure", {"FY2025": 424554, "FY2024": 390032, "FY2023": 359897, "FY2022": 341308, "FY2021": 426681}), ("Leverage ratio", {"FY2025": "4.2%", "FY2024": "4.4%", "FY2023": "4.5%", "FY2022": "4.4%", "FY2021": "3.8%"})], note="FY2021 is shown on the prior CRR methodology as reported in NWB Plc Annual Report 2022, p.64; the report also gives 4.8% on the later UK methodology. FY2022 onward uses the current PRA basis and is not directly comparable with the FY2021 headline.")
metric("LCR", "%", [("Liquidity Coverage Ratio - UK DoLSub", {"FY2025": "151%", "FY2024": "147%", "FY2023": "138%", "FY2022": "131%", "FY2021": "169%"})], note="UK DoLSub basis: NWB Plc, RBS plc and Coutts & Company. The 2025 figure is the December value from the NWB Pillar 3 report; the 2024 and 2023 figures are the December values in the corresponding KM1 disclosures. NWB Plc reports liquidity under a PRA waiver at UK DoLSub level rather than solo.")
metric("NSFR", "%", [("Net Stable Funding Ratio - UK DoLSub", {"FY2025": "137%", "FY2024": "136%", "FY2023": "126%", "FY2022": "137%", "FY2021": "151%"})], note="UK DoLSub basis; see LCR note. NSFR is a four-quarter average under the regulatory disclosure framework.")
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], "NWB Plc Pillar 3 Reports 2022-2025 - " + P3_2025_URL, per_note={"MREL Ratio": "No single numeric MREL ratio is presented in the five-year source set used for this annual workbook. MREL instruments and movements are discussed in the annual accounts, but no comparable headline ratio was disclosed in the reviewed NWB Plc UK KM1 material."})


# NWB Plc publishes quarterly UK KM1 disclosures.  The Q3 reports include the
# current quarter plus the preceding Q1/Q2 comparatives, allowing a complete
# March-to-September quarterly series without mixing in NatWest Group data.
INTERIM_PERIODS = [
    ("31 March 2022", "Q1 2022", P3_2022_Q3_URL, "p.7"),
    ("30 June 2022", "H1 2022", P3_2022_Q3_URL, "p.7"),
    ("30 September 2022", "Q3 2022", P3_2022_Q3_URL, "p.7"),
    ("31 March 2023", "Q1 2023", P3_2023_Q3_URL, "p.6"),
    ("30 June 2023", "H1 2023", P3_2023_Q3_URL, "p.6"),
    ("30 September 2023", "Q3 2023", P3_2023_Q3_URL, "p.6"),
    ("31 March 2024", "Q1 2024", P3_2024_Q3_URL, "p.6"),
    ("30 June 2024", "H1 2024", P3_2024_Q3_URL, "p.6"),
    ("30 September 2024", "Q3 2024", P3_2024_Q3_URL, "p.6"),
    ("31 March 2025", "Q1 2025", P3_2025_Q3_URL, "p.6"),
    ("30 June 2025", "H1 2025", P3_2025_Q3_URL, "p.6"),
    ("30 September 2025", "Q3 2025", P3_2025_Q3_URL, "p.6"),
]

INTERIM_VALUES = {
    "31 March 2022": [13802, 15917, 18709, 103987, "13.3%", "15.3%", "18.0%", 338123, "4.7%"],
    "30 June 2022": [12335, 14591, 17503, 106211, "11.6%", "13.7%", "16.5%", 340086, "4.3%"],
    "30 September 2022": [12437, 14680, 17719, 107157, "11.6%", "13.7%", "16.5%", 343343, "4.3%"],
    "31 March 2023": [13640, 15883, 19343, 116122, "11.7%", "13.7%", "16.7%", 349719, "4.5%"],
    "30 June 2023": [13609, 15852, 19235, 116811, "11.7%", "13.6%", "16.5%", 363052, "4.4%"],
    "30 September 2023": [14320, 16563, 20011, 117745, "12.2%", "14.1%", "17.0%", 362422, "4.6%"],
    "31 March 2024": [14823, 17101, 20497, 124523, "11.9%", "13.7%", "16.5%", 358649, "4.8%"],
    "30 June 2024": [13813, 16890, 20273, 120780, "11.4%", "14.0%", "16.8%", 366912, "4.6%"],
    "30 September 2024": [14722, 17799, 21172, 122340, "12.0%", "14.5%", "17.3%", 381762, "4.7%"],
    "31 March 2025": [15271, 18848, 23064, 127480, "12.0%", "14.8%", "18.1%", 397065, "4.7%"],
    "30 June 2025": [14828, 18346, 22104, 130712, "11.3%", "14.0%", "16.9%", 411371, "4.5%"],
    "30 September 2025": [16128, 20147, 23937, 130496, "12.4%", "15.4%", "18.3%", 413717, "4.9%"],
}

interim_metric_specs = [
    ("Common equity tier 1 (CET1) capital", "£m"),
    ("Tier 1 capital", "£m"),
    ("Total capital", "£m"),
    ("Total risk-weighted exposure amount", "£m"),
    ("Common equity tier 1 (CET1) ratio", "%"),
    ("Tier 1 ratio", "%"),
    ("Total capital ratio", "%"),
    ("Total exposure measure excluding claims on central banks", "£m"),
    ("Leverage ratio excluding claims on central banks", "%"),
]
interim_rows = []
for period, disclosure_type, source_url, page_ref in INTERIM_PERIODS:
    for (metric_name, unit), value in zip(interim_metric_specs, INTERIM_VALUES[period]):
        interim_rows.append([
            period, disclosure_type, metric_name, value, unit,
            "NWB Plc entity-level, PRA transitional/current basis as reported",
            source_url, page_ref,
        ])

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=interim_rows,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(interim_rows)},
    title="National Westminster Bank Plc — Interim Pillar 3",
    subtitle="Quarterly UK KM1 key metrics, March 2022 to September 2025. Capital and leverage figures are NWB Plc entity-level disclosures in £m or percentages.",
    note=(
        "Sources are the official NWB Plc Q3 Pillar 3 reports for 2022-2025, whose UK KM1 tables include the current quarter and prior Q1/Q2 comparatives. "
        "The NWB Plc UK Domestic Liquidity Sub-Group waiver means LCR and NSFR are managed and disclosed at UK DoLSub level rather than entity level; they are therefore not inserted here. "
        "No separate NWB Plc interim UK KM1 report was located for March-June-September 2021 in the reviewed official archive, so those periods are explicitly not represented rather than estimated."
    ),
)

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 444649, "FY2024": 421875, "FY2023": 411749, "FY2022": 401747, "FY2021": 426111}),
        ("Loans to customers - amortised cost", {"FY2025": 310121, "FY2024": 297548, "FY2023": 284314, "FY2022": 267401, "FY2021": 255443}),
        ("Customer deposits", {"FY2025": 282427, "FY2024": 275972, "FY2023": 276202, "FY2022": 281558, "FY2021": 292470}),
        ("Total equity", {"FY2025": 22685, "FY2024": 21609, "FY2023": 19701, "FY2022": 18243, "FY2021": 19166}),
    ], balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 13620, "FY2024": 11973, "FY2023": 12086, "FY2022": 11743, "FY2021": 9269}),
        ("Operating expenses", {"FY2025": -7241, "FY2024": -6963, "FY2023": -6793, "FY2022": -6288, "FY2021": -6199}),
        ("Profit for the year", {"FY2025": 4198, "FY2024": 3425, "FY2023": 3509, "FY2022": 3689, "FY2021": 2907}),
    ], income_statement_unit="£m (NWB Group basis - see BASIS NOTE)",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 21609, "FY2024": 19701, "FY2023": 18243, "FY2022": 19166, "FY2021": 18464}),
        ("Total comprehensive income for the year", {"FY2025": 4338, "FY2024": 3566, "FY2023": 3211, "FY2022": 2619, "FY2021": 2556}),
        ("Other equity movements, net", {"FY2025": -3262, "FY2024": -1658, "FY2023": -1753, "FY2022": -3542, "FY2021": -1854}),
        ("Closing equity", {"FY2025": 22685, "FY2024": 21609, "FY2023": 19701, "FY2022": 18243, "FY2021": 19166}),
    ], equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 13528, "FY2024": -1896, "FY2023": -4382, "FY2022": -40929, "FY2021": 36574}),
        ("Net cash from/(used in) investing activities", {"FY2025": -11262, "FY2024": -9382, "FY2023": -17008, "FY2022": 12745, "FY2021": 4216}),
        ("Net cash from/(used in) financing activities", {"FY2025": -1918, "FY2024": -2267, "FY2023": -1203, "FY2022": -2991, "FY2021": -1454}),
        ("Cash and cash equivalents at end of year", {"FY2025": 39167, "FY2024": 38678, "FY2023": 52482, "FY2022": 75472, "FY2021": 105546}),
    ], cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "11.2%", "FY2024": "11.4%", "FY2023": "11.6%", "FY2022": "11.3%", "FY2021": "16.1%"}),
        ("Tier 1 Ratio", {"FY2025": "13.4%", "FY2024": "13.9%", "FY2023": "13.4%", "FY2022": "13.3%", "FY2021": "18.6%"}),
        ("Total Capital Ratio", {"FY2025": "16.2%", "FY2024": "16.6%", "FY2023": "16.3%", "FY2022": "15.9%", "FY2021": "22.0%"}),
        ("Leverage Ratio", {"FY2025": "4.2%", "FY2024": "4.4%", "FY2023": "4.5%", "FY2022": "4.4%", "FY2021": "3.8%"}),
        ("LCR (UK DoLSub)", {"FY2025": "151%", "FY2024": "147%", "FY2023": "138%", "FY2022": "131%", "FY2021": "169%"}),
        ("NSFR (UK DoLSub)", {"FY2025": "137%", "FY2024": "136%", "FY2023": "126%", "FY2022": "137%", "FY2021": "151%"}),
    ], note="Figures are duplicated from the detail sheets. See source notes for exact documents, pages, entity basis and methodology changes. Additional quarterly NWB Plc disclosures are provided on the Interim Pillar 3 sheet.")

bw.save("/Users/armaan/code/katalysis/banks/NATIONAL WESTMINSTER BANK PLC FINANCIALS.xlsx")
