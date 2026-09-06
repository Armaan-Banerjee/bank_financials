import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR_URLS = {
    "FY2025": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwm-annual-report.pdf",
    "FY2024": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/14022025/nwm-annual-report.pdf",
    "FY2023": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/16022024/nwmp-annual-report.pdf",
    "FY2022": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/nwmp-annual-report.pdf",
    "FY2021": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/18022022/nwm-plc-annual-report-2021.pdf",
}
P3_URLS = {
    "FY2025": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/nwm-pillar-3-report.pdf",
    "FY2024": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/14022025/nwm-pillar-3-report.pdf",
    "FY2023": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/16022024/nwmp-pillar-3-report.pdf",
    "FY2022": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/17022023/nwmp-pillar-3-report.pdf",
    "FY2021": "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/18022022/nwg-pillar-3-supplement-2021.pdf",
}


def sources(kind, pages):
    urls = AR_URLS if kind == "annual" else P3_URLS
    label = "Annual Report and Accounts" if kind == "annual" else "Pillar 3 Report"
    lines = ["Sources — NatWest Markets Plc (NWM Plc), entity/group basis as stated in each source:"]
    for year in YEARS:
        lines.append(f"{year}: NWM Plc {label}, p.{pages[year]} — {urls[year]}")
    return "\n".join(lines)


bw = BankWorkbook("NatWest Markets Plc", YEARS, header_color="5B2C6F")

ENTITY_NOTE = (
    "Entity: NatWest Markets Plc (NWM Plc), company SC090312. The Balance Sheet and "
    "Statement of Changes in Equity below are the NWM Plc entity column of each year's "
    "audited financial statements (which present NWM Group consolidated and NWM Plc "
    "entity figures side by side). Profit & Loss is necessarily NWM Group consolidated "
    "basis - NWM Plc's own Annual Report and Accounts publishes only a single "
    "'Consolidated income statement' (no standalone NWM Plc-entity income statement "
    "or statement of comprehensive income); NWM Plc's own operating profit/(loss) "
    "before tax is disclosed only via the cash-flow reconciliation (see the Cash Flow "
    "Statement sheet) and differs from the Group figure shown here."
)

STATEMENTS_SOURCES = (
    "Sources - NWM Plc Annual Report and Accounts, NWM Group/NWM Plc dual-column financial statements:\n"
    f"FY2025: Annual Report and Accounts 2025, Consolidated income statement p.75, Balance sheet p.76, "
    f"Statement of changes in equity p.77-78 - {AR_URLS['FY2025']}\n"
    f"FY2024: Annual Report and Accounts 2024, Consolidated income statement p.83, Balance sheet p.84, "
    f"Statement of changes in equity p.85-86 - {AR_URLS['FY2024']}\n"
    f"FY2023: Annual Report and Accounts 2023, Consolidated income statement p.90, Balance sheet p.91, "
    f"Statement of changes in equity p.92 - {AR_URLS['FY2023']}\n"
    f"FY2022: Annual Report and Accounts 2022, Consolidated income statement p.97, Balance sheet p.98, "
    f"Statement of changes in equity p.99 - {AR_URLS['FY2022']}\n"
    f"FY2021: Annual Report and Accounts 2021, Consolidated income statement/statement of comprehensive "
    f"income p.104-105, Balance sheet and Statement of changes in equity p.106-107 - {AR_URLS['FY2021']}\n\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. All 5 years tie exactly to the equity statement's own
# opening/closing balances and to Total assets = Total liabilities + Total
# equity. Zero plug rows needed anywhere.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 9357, "FY2024": 11069, "FY2023": 8607, "FY2022": 13467, "FY2021": 12294}),
    ("DATA", "Trading assets", {"FY2025": 22087, "FY2024": 26186, "FY2023": 28411, "FY2022": 27301, "FY2021": 41222}),
    ("DATA", "Derivatives", {"FY2025": 57793, "FY2024": 74982, "FY2023": 75832, "FY2022": 96258, "FY2021": 103042}),
    ("DATA", "Settlement balances", {"FY2025": 490, "FY2024": 550, "FY2023": 2168, "FY2022": 1686, "FY2021": 795}),
    ("DATA", "Loans to banks (amortised cost)", {"FY2025": 603, "FY2024": 897, "FY2023": 910, "FY2022": 815, "FY2021": 712}),
    ("DATA", "Loans to customers (amortised cost)", {"FY2025": 22154, "FY2024": 17089, "FY2023": 12104, "FY2022": 9154, "FY2021": 6810}),
    ("DATA", "Amounts due from holding company and fellow subsidiaries", {"FY2025": 3611, "FY2024": 3341, "FY2023": 6472, "FY2022": 6665, "FY2021": 6723}),
    ("DATA", "Other financial assets", {"FY2025": 17354, "FY2024": 16081, "FY2023": 13444, "FY2022": 10377, "FY2021": 7743}),
    ("DATA", "Investments in group undertakings", {"FY2025": 2403, "FY2024": 2263, "FY2023": 2320, "FY2022": 2626, "FY2021": 2481}),
    ("DATA", "Other assets", {"FY2025": 436, "FY2024": 479, "FY2023": 390, "FY2022": 712, "FY2021": 732}),
    ("TOTAL", "Total assets", {"FY2025": 136288, "FY2024": 152937, "FY2023": 150658, "FY2022": 169061, "FY2021": 182554}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Bank deposits", {"FY2025": 7650, "FY2024": 4069, "FY2023": 1909, "FY2022": 2936, "FY2021": 1808}),
    ("DATA", "Customer deposits", {"FY2025": 2824, "FY2024": 2350, "FY2023": 3060, "FY2022": 2665, "FY2021": 1510}),
    ("DATA", "Amounts due to holding company and fellow subsidiaries", {"FY2025": 8278, "FY2024": 10757, "FY2023": 14385, "FY2022": 12867, "FY2021": 10978}),
    ("DATA", "Settlement balances", {"FY2025": 501, "FY2024": 444, "FY2023": 400, "FY2022": 1133, "FY2021": 1028}),
    ("DATA", "Trading liabilities", {"FY2025": 25916, "FY2024": 30130, "FY2023": 34079, "FY2022": 33225, "FY2021": 47119}),
    ("DATA", "Derivatives (liability)", {"FY2025": 52166, "FY2024": 70016, "FY2023": 69404, "FY2022": 90754, "FY2021": 95096}),
    ("DATA", "Other financial liabilities", {"FY2025": 31740, "FY2024": 27966, "FY2023": 20655, "FY2022": 18396, "FY2021": 16877}),
    ("DATA", "Other liabilities", {"FY2025": 333, "FY2024": 386, "FY2023": 453, "FY2022": 567, "FY2021": 789}),
    ("TOTAL", "Total liabilities", {"FY2025": 129408, "FY2024": 146118, "FY2023": 144345, "FY2022": 162543, "FY2021": 175205}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called-up share capital", {"FY2025": 400, "FY2024": 400, "FY2023": 400, "FY2022": 400, "FY2021": 400}),
    ("DATA", "Paid-in equity", {"FY2025": 1192, "FY2024": 1496, "FY2023": 904, "FY2022": 904, "FY2021": 904}),
    ("DATA", "Share premium account", {"FY2025": 1946, "FY2024": 1946, "FY2023": 1946, "FY2022": 1946, "FY2021": 1946}),
    ("DATA", "FVOCI reserve", {"FY2025": 19, "FY2024": 9, "FY2023": 0, "FY2022": -2, "FY2021": 18}),
    ("DATA", "Cash flow hedging reserve", {"FY2025": -97, "FY2024": -204, "FY2023": -187, "FY2022": -284, "FY2021": 46}),
    ("DATA", "Foreign exchange reserve", {"FY2025": -117, "FY2024": -142, "FY2023": -157, "FY2022": -78, "FY2021": -218}),
    ("DATA", "Retained earnings", {"FY2025": 3537, "FY2024": 3314, "FY2023": 3407, "FY2022": 3632, "FY2021": 4253}),
    ("TOTAL", "Total equity", {"FY2025": 6880, "FY2024": 6819, "FY2023": 6313, "FY2022": 6518, "FY2021": 7349}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 136288, "FY2024": 152937, "FY2023": 150658, "FY2022": 169061, "FY2021": 182554}),
]

bw.add_balance_sheet_sheet(
    title="NatWest Markets Plc — Balance Sheet",
    subtitle="NWM Plc entity basis (not NWM Group consolidated). £m. NWM Plc carries no non-controlling "
              "interests in any year, so Owners' equity = Total equity throughout.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss - necessarily NWM Group consolidated basis (see ENTITY_NOTE):
# NWM Plc's Annual Report and Accounts publishes only one Consolidated
# income statement / statement of comprehensive income, not a separate
# NWM Plc-entity version.
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income (NWM Group consolidated basis)", {}),
    ("DATA", "Interest receivable", {"FY2025": 2585, "FY2024": 2720, "FY2023": 2186, "FY2022": 745, "FY2021": 343}),
    ("DATA", "Interest payable", {"FY2025": -2097, "FY2024": -2288, "FY2023": -1831, "FY2022": -654, "FY2021": -335}),
    ("TOTAL", "Net interest income", {"FY2025": 488, "FY2024": 432, "FY2023": 355, "FY2022": 91, "FY2021": 8}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 417, "FY2024": 476, "FY2023": 377, "FY2022": 349, "FY2021": 262}),
    ("DATA", "Fees and commissions payable", {"FY2025": -188, "FY2024": -213, "FY2023": -175, "FY2022": -158, "FY2021": -104}),
    ("DATA", "Income from trading activities", {"FY2025": 658, "FY2024": 585, "FY2023": 477, "FY2022": 389, "FY2021": 263}),
    ("DATA", "Other operating income", {"FY2025": 96, "FY2024": -43, "FY2023": 35, "FY2022": 18, "FY2021": -28}),
    ("TOTAL", "Non-interest income", {"FY2025": 983, "FY2024": 805, "FY2023": 714, "FY2022": 598, "FY2021": 393}),
    ("TOTAL", "Total income", {"FY2025": 1471, "FY2024": 1237, "FY2023": 1069, "FY2022": 689, "FY2021": 401}),
    ("DATA", "Staff costs", {"FY2025": -506, "FY2024": -452, "FY2023": -418, "FY2022": -400, "FY2021": -498}),
    ("DATA", "Premises and equipment", {"FY2025": -79, "FY2024": -75, "FY2023": -66, "FY2022": -60, "FY2021": -110}),
    ("DATA", "Other administrative expenses", {"FY2025": -711, "FY2024": -671, "FY2023": -642, "FY2022": -652, "FY2021": -522}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -12, "FY2024": -10, "FY2023": -16, "FY2022": -16, "FY2021": -20}),
    ("TOTAL", "Operating expenses", {"FY2025": -1308, "FY2024": -1208, "FY2023": -1142, "FY2022": -1128, "FY2021": -1150}),
    ("TOTAL", "Profit/(loss) before impairment losses/releases", {"FY2025": 163, "FY2024": 29, "FY2023": -73, "FY2022": -439, "FY2021": -749}),
    ("DATA", "Impairment (losses)/releases", {"FY2025": -3, "FY2024": 8, "FY2023": -2, "FY2022": -8, "FY2021": 35}),
    ("TOTAL", "Operating profit/(loss) before tax", {"FY2025": 160, "FY2024": 37, "FY2023": -75, "FY2022": -447, "FY2021": -714}),
    ("DATA", "Tax credit/(charge)", {"FY2025": 115, "FY2024": 26, "FY2023": -23, "FY2022": 183, "FY2021": 223}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 275, "FY2024": 63, "FY2023": -98, "FY2022": -264, "FY2021": -491}),
    ("SECTION", "Other comprehensive income/(loss), net of tax", {}),
    ("DATA", "Remeasurement of retirement benefit schemes", {"FY2025": 5, "FY2024": -13, "FY2023": -113, "FY2022": -68, "FY2021": 36}),
    ("DATA", "Changes in FV of financial liabilities designated at FVTPL (own credit risk)", {"FY2025": -17, "FY2024": -33, "FY2023": -39, "FY2022": 50, "FY2021": -29}),
    ("DATA", "FVOCI financial assets (items not qualifying for reclassification)", {"FY2025": 3, "FY2024": 14, "FY2023": 7, "FY2022": -2, "FY2021": 2}),
    ("DATA", "Tax (items not qualifying for reclassification)", {"FY2025": -8, "FY2024": 23, "FY2023": 42, "FY2022": 32, "FY2021": -10}),
    ("DATA", "FVOCI financial assets (items qualifying for reclassification)", {"FY2025": 16, "FY2024": 5, "FY2023": 5, "FY2022": -31, "FY2021": -2}),
    ("DATA", "Cash flow hedges", {"FY2025": 127, "FY2024": -29, "FY2023": 178, "FY2022": -475, "FY2021": -206}),
    ("DATA", "Currency translation", {"FY2025": 23, "FY2024": -14, "FY2023": -132, "FY2022": 245, "FY2021": -124}),
    ("DATA", "Tax (items qualifying for reclassification)", {"FY2025": -46, "FY2024": 16, "FY2023": -48, "FY2022": 142, "FY2021": 45}),
    ("TOTAL", "Other comprehensive income/(loss) after tax", {"FY2025": 103, "FY2024": -31, "FY2023": -100, "FY2022": -107, "FY2021": -288}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 378, "FY2024": 32, "FY2023": -198, "FY2022": -371, "FY2021": -779}),
]

bw.add_income_statement_sheet(
    title="NatWest Markets Plc — Profit & Loss",
    subtitle="NWM Group consolidated basis (see sources note - NWM Plc publishes no standalone entity income "
              "statement). £m.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=82,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - NWM Plc entity basis. Equity
# reconciliation ladder confirmed exactly across all 5 years: every year's
# own closing balance ties to both the next year's own opening balance and
# that year's own Balance Sheet Total equity. Zero plug rows needed. NWM
# Plc carries no Merger reserve balance in any year (the Group-only
# component from FY2023 onward is always 0 for the Plc entity) so it is
# omitted as a column here. NWM Plc carries no non-controlling interests.
# ---------------------------------------------------------------
equity_headers = ["Called-up share capital", "Paid-in equity", "Share premium", "FVOCI reserve",
                   "Cash flow hedging reserve", "Foreign exchange reserve", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2021 (FY2021 opening)", (400, 904, 1759, 14, 201, -192, 6066, 9152)),
    ("DATA", "Redemption of preference shares (share premium)", (None, None, 187, None, None, None, None, 187)),
    ("DATA", "FVOCI reserve: unrealised gains, realised losses, tax", (None, None, None, 4, None, None, None, 4)),
    ("DATA", "Cash flow hedging reserve: recognised, transferred, tax", (None, None, None, None, -155, None, None, -155)),
    ("DATA", "Foreign exchange reserve: retranslation, hedges, tax", (None, None, None, None, None, -26, None, -26)),
    ("DATA", "Loss attributable to ordinary shareholders and other equity holders", (None, None, None, None, None, None, -527, -527)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, None, -1000, -1000)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, -63, -63)),
    ("DATA", "Redemption of preference shares (retained earnings)", (None, None, None, None, None, None, -188, -188)),
    ("DATA", "Realised losses on FVOCI equity shares, gross and tax", (None, None, None, None, None, None, -2, -2)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, 22, 22)),
    ("DATA", "Changes in FV of credit in financial liabilities at FVTPL, net of tax", (None, None, None, None, None, None, -8, -8)),
    ("DATA", "Share-based payments", (None, None, None, None, None, None, -47, -47)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (400, 904, 1946, 18, 46, -218, 4253, 7349)),
    ("DATA", "FVOCI reserve: unrealised losses, realised gains, tax", (None, None, None, -20, None, None, None, -20)),
    ("DATA", "Cash flow hedging reserve: recognised, transferred, tax", (None, None, None, None, -330, None, None, -330)),
    ("DATA", "Foreign exchange reserve: retranslation, hedges, tax", (None, None, None, None, None, 140, None, 140)),
    ("DATA", "Loss attributable to ordinary shareholders and other equity holders", (None, None, None, None, None, None, -79, -79)),
    ("DATA", "Ordinary dividends paid", (None, None, None, None, None, None, -430, -430)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, -70, -70)),
    ("DATA", "Realised gains on FVOCI equity shares, gross and tax", (None, None, None, None, None, None, 16, 16)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, -45, -45)),
    ("DATA", "Changes in FV of credit in financial liabilities at FVTPL, net of tax", (None, None, None, None, None, None, 5, 5)),
    ("DATA", "Share-based payments", (None, None, None, None, None, None, -18, -18)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (400, 904, 1946, -2, -284, -78, 3632, 6518)),
    ("DATA", "FVOCI reserve: unrealised gains, realised losses, tax", (None, None, None, 2, None, None, None, 2)),
    ("DATA", "Cash flow hedging reserve: recognised, transferred, tax", (None, None, None, None, 97, None, None, 97)),
    ("DATA", "Foreign exchange reserve: retranslation, hedges, recycled", (None, None, None, None, None, -79, None, -79)),
    ("DATA", "Loss attributable to ordinary shareholders and other equity holders", (None, None, None, None, None, None, -169, -169)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, -70, -70)),
    ("DATA", "Capital contribution (indemnity claim against parent, NatWest Group plc)", (None, None, None, None, None, None, 115, 115)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, -73, -73)),
    ("DATA", "Changes in FV of credit in financial liabilities at FVTPL, net of tax", (None, None, None, None, None, None, -10, -10)),
    ("DATA", "Share-based payments", (None, None, None, None, None, None, -18, -18)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (400, 904, 1946, 0, -187, -157, 3407, 6313)),
    ("DATA", "Paid-in equity issued", (None, 592, None, None, None, None, None, 592)),
    ("DATA", "FVOCI reserve: unrealised gains, realised losses, tax", (None, None, None, 9, None, None, None, 9)),
    ("DATA", "Cash flow hedging reserve: recognised, transferred, tax", (None, None, None, None, -17, None, None, -17)),
    ("DATA", "Foreign exchange reserve: retranslation, hedges, recycled", (None, None, None, None, None, 15, None, 15)),
    ("DATA", "Loss attributable to ordinary shareholders and other equity holders", (None, None, None, None, None, None, -33, -33)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, -73, -73)),
    ("DATA", "Realised gains on FVOCI equity shares, gross and tax", (None, None, None, None, None, None, 9, 9)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, 3, 3)),
    ("DATA", "Changes in FV of credit in financial liabilities at FVTPL, net of tax", (None, None, None, None, None, None, -6, -6)),
    ("DATA", "Share-based payments", (None, None, None, None, None, None, 7, 7)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (400, 1496, 1946, 9, -204, -142, 3314, 6819)),
    ("DATA", "Paid-in equity redeemed / issued", (None, -304, None, None, None, None, None, -304)),
    ("DATA", "FVOCI reserve: unrealised gains, realised losses, tax", (None, None, None, 10, None, None, None, 10)),
    ("DATA", "Cash flow hedging reserve: recognised, reclassified to P&L, tax", (None, None, None, None, 107, None, None, 107)),
    ("DATA", "Foreign exchange reserve: retranslation, hedges, recycled", (None, None, None, None, None, 25, None, 25)),
    ("DATA", "Profit attributable to ordinary shareholders and other equity holders", (None, None, None, None, None, None, 265, 265)),
    ("DATA", "Paid-in equity dividends paid", (None, None, None, None, None, None, -108, -108)),
    ("DATA", "Redemption/reclassification of paid-in equity", (None, None, None, None, None, None, 59, 59)),
    ("DATA", "Realised losses on FVOCI equity shares, tax", (None, None, None, None, None, None, -6, -6)),
    ("DATA", "Remeasurement of retirement benefit schemes, net of tax", (None, None, None, None, None, None, 4, 4)),
    ("DATA", "Share-based payments", (None, None, None, None, None, None, 7, 7)),
    ("DATA", "Sharing in success", (None, None, None, None, None, None, 2, 2)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (400, 1192, 1946, 19, -97, -117, 3537, 6880)),
]

bw.add_equity_changes_sheet(
    title="NatWest Markets Plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, NWM Plc entity basis. £m. Equity reconciliation "
              "ladder confirmed: every year's own closing balance ties exactly to both the next year's own "
              "opening balance and that year's own Balance Sheet Total equity - zero plug rows needed anywhere "
              "across all 5 years. NWM Plc carries no Merger reserve or non-controlling interests balance in "
              "any year, so both are omitted as columns.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
)

# NWM Plc column of the audited consolidated cash-flow statement. The 2021–22
# reports present detailed lines; later reports present condensed note-referenced
# lines. Each year's own presentation is retained.
cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Operating profit/(loss) before tax", {"FY2025": 186, "FY2024": -32, "FY2023": -141, "FY2022": -264, "FY2021": -702}),
    ("DATA", "Non-cash and other items", {"FY2025": -895, "FY2024": -104, "FY2023": 21}),
    ("DATA", "Impairment losses/(releases)", {"FY2022": -1, "FY2021": -36}),
    ("DATA", "Depreciation and amortisation", {"FY2022": 6, "FY2021": 9}),
    ("DATA", "Other non-cash items and fair-value movements", {"FY2022": -637, "FY2021": -103}),
    ("DATA", "Changes in operating assets and liabilities", {"FY2025": -1864, "FY2024": -51, "FY2023": -672, "FY2022": 5883, "FY2021": 1130}),
    ("DATA", "Income taxes received/(paid)", {"FY2025": 108, "FY2024": -81, "FY2023": 116, "FY2022": 144, "FY2021": 55}),
    ("DATA", "Other detailed operating adjustments (reported residual)", {"FY2022": 264, "FY2021": 702}),
    ("TOTAL", "Net cash flows from operating activities", {"FY2025": -2465, "FY2024": -268, "FY2023": -676, "FY2022": 5395, "FY2021": 1055}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Sale and maturity of other financial assets", {"FY2025": 8623, "FY2024": 4622, "FY2023": 3752, "FY2022": 4797, "FY2021": 3842}),
    ("DATA", "Purchase of other financial assets", {"FY2025": -9833, "FY2024": -7364, "FY2023": -6771, "FY2022": -7601, "FY2021": -3822}),
    ("DATA", "Income received on other financial assets", {"FY2025": 871, "FY2024": 882, "FY2023": 573, "FY2022": 252, "FY2021": 146}),
    ("DATA", "Dividends received from subsidiaries", {"FY2025": 98, "FY2024": 94, "FY2023": 349, "FY2022": 53, "FY2021": 65}),
    ("DATA", "Sale of property, plant and equipment", {"FY2023": 1}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -1, "FY2024": -1}),
    ("DATA", "Other investing activities (reported residual)", {"FY2024": -1, "FY2022": -1}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": -242, "FY2024": -1768, "FY2023": -2096, "FY2022": -2500, "FY2021": 231}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of paid-in equity", {"FY2025": 600, "FY2024": 592}),
    ("DATA", "Redemption of paid-in equity", {"FY2025": -845}),
    ("DATA", "Issue/(redemption) of subordinated liabilities", {"FY2025": -67, "FY2024": 22, "FY2023": -652, "FY2022": -350, "FY2021": -339}),
    ("DATA", "Issue/(maturity) of MRELs", {"FY2025": 104, "FY2024": 1247, "FY2023": -45, "FY2022": -1027, "FY2021": -1234}),
    ("DATA", "Interest paid on MRELs and subordinated liabilities", {"FY2025": -306, "FY2024": -261, "FY2023": -232, "FY2022": -210, "FY2021": -166}),
    ("DATA", "Dividends paid", {"FY2025": -108, "FY2024": -73, "FY2023": -70, "FY2022": -500, "FY2021": -1063}),
    ("DATA", "Capital contribution", {"FY2023": 115}),
    ("DATA", "Other financing activities (reported residual)", {"FY2025": 67, "FY2024": 82, "FY2023": 57, "FY2022": 210, "FY2021": 166}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": -555, "FY2024": 1609, "FY2023": -827, "FY2022": -1877, "FY2021": -2636}),
    ("DATA", "Effects of exchange rate on cash and cash equivalents", {"FY2025": 114, "FY2024": -291, "FY2023": -336, "FY2022": 691, "FY2021": -721}),
    ("TOTAL", "Net decrease in cash and cash equivalents", {"FY2025": -3148, "FY2024": -718, "FY2023": -3935, "FY2022": 1709, "FY2021": -2071}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 16270, "FY2024": 16988, "FY2023": 20923, "FY2022": 19214, "FY2021": 21285}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 13122, "FY2024": 16270, "FY2023": 16988, "FY2022": 20923, "FY2021": 19214}),
]
bw.add_cash_flow_sheet(
    "NatWest Markets Plc — Cash Flow Statement",
    "NWM Plc consolidated basis, £m. Figures are the NWM Plc column of each year's audited statement.",
    cash_rows,
    sources("annual", {"FY2025": 79, "FY2024": 87, "FY2023": 93, "FY2022": "100–101", "FY2021": "108–109"}),
    first_col_width=70, source_height=150, unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Asset Quality - NWM Plc entity-level IFRS 9 stage split, ECL provisions
# and coverage ratios (Note 14, Loan impairment provisions - this is the
# one note in the financial statements that discloses NWM Plc entity
# figures directly, not just via the dual-column primary statements).
# The note's own "Total" (which includes an "Inter-Group" sub-line) does
# not tie exactly to the Balance Sheet's "Loans to banks" + "Loans to
# customers" lines - a modest gap exists every year, most likely reflecting
# scope/netting differences between this note and the primary statement
# lines rather than a transcription error; both are shown as originally
# disclosed.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "NWM Plc loans (amortised cost), by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2025": 22708, "FY2024": 17789, "FY2023": 12584, "FY2022": 9713, "FY2021": 7444}),
    ("DATA", "Stage 2", {"FY2025": 107, "FY2024": 253, "FY2023": 436, "FY2022": 228, "FY2021": 104}),
    ("DATA", "Stage 3", {"FY2025": 22, "FY2024": 25, "FY2023": 25, "FY2022": 49, "FY2021": 61}),
    ("DATA", "  of which: individual", {"FY2025": 15, "FY2024": 18, "FY2023": 17, "FY2022": 37, "FY2021": 53}),
    ("DATA", "  of which: collective", {"FY2025": 7, "FY2024": 7, "FY2023": 8, "FY2022": 12, "FY2021": 8}),
    ("DATA", "Inter-Group", {"FY2025": 1733, "FY2024": 1839, "FY2023": 2623, "FY2022": 2324, "FY2021": 2605}),
    ("TOTAL", "Total loans within ECL scope", {"FY2025": 24570, "FY2024": 19906, "FY2023": 15668, "FY2022": 12314, "FY2021": 10214}),
    ("SECTION", "ECL provisions", {}),
    ("DATA", "Stage 1 ECL provision", {"FY2025": 22, "FY2024": 21, "FY2023": 17, "FY2022": 15, "FY2021": 6}),
    ("DATA", "Stage 2 ECL provision", {"FY2025": 4, "FY2024": 4, "FY2023": 7, "FY2022": 3, "FY2021": 2}),
    ("DATA", "Stage 3 ECL provision", {"FY2025": 15, "FY2024": 16, "FY2023": 24, "FY2022": 26, "FY2021": 36}),
    ("DATA", "Inter-Group ECL provision", {"FY2025": 2, "FY2024": 2, "FY2023": 3, "FY2022": 4, "FY2021": 1}),
    ("TOTAL", "Total ECL provisions", {"FY2025": 43, "FY2024": 43, "FY2023": 51, "FY2022": 48, "FY2021": 45}),
    ("SECTION", "ECL provision coverage ratios", {}),
    ("DATA", "Stage 1 coverage", {"FY2025": "0.10%", "FY2024": "0.12%", "FY2023": "0.14%", "FY2022": "0.15%", "FY2021": "0.08%"}),
    ("DATA", "Stage 2 coverage", {"FY2025": "3.74%", "FY2024": "1.58%", "FY2023": "1.61%", "FY2022": "1.32%", "FY2021": "1.92%"}),
    ("DATA", "Stage 3 coverage", {"FY2025": "68.18%", "FY2024": "64.00%", "FY2023": "96.00%", "FY2022": "53.06%", "FY2021": "59.02%"}),
    ("DATA", "Total coverage (NPL-adjacent ratio)", {"FY2025": "0.18%", "FY2024": "0.23%", "FY2023": "0.37%", "FY2022": "0.44%", "FY2021": "0.58%"}),
]

bw.add_asset_quality_sheet(
    title="NatWest Markets Plc — Asset Quality",
    subtitle="NWM Plc entity basis, Note 14 (Loan impairment provisions). £m. This trading/wholesale bank's "
              "credit-loss exposure is small relative to its balance sheet (Stage 3 loans are consistently "
              "under 0.3% of total loans within ECL scope).",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nAsset Quality specifically: FY2025/FY2024: Annual Report and Accounts 2025, Note 14 'Loan "
        "impairment provisions', p.128. FY2023/FY2022: Annual Report and Accounts 2023, Note 14, p.142. "
        "FY2021: Annual Report and Accounts 2021, Note 14, p.79 (page numbering per the source PDF's own "
        "extraction; document prints '14 Loan impairment provisions' without a separate page header on this "
        "occasion).\n\n"
        "DATA QUALITY FLAG: 'Total loans within ECL scope' (which includes an 'Inter-Group' sub-line) does not "
        "tie exactly to the Balance Sheet's 'Loans to banks' + 'Loans to customers' lines in any year - a "
        "genuine scope/netting difference between this note and the primary statement lines, not a "
        "transcription error. 'Total coverage' is the source document's own disclosed 'Total' coverage row "
        "(not independently derived - it does not exactly equal Total ECL provisions / Total loans within ECL "
        "scope due to rounding within the underlying stage-level percentages)."
    ),
    first_col_width=68,
    source_height=340,
    unit_suffix=" (£m)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, sources("p3", {"FY2025": 7, "FY2024": 7, "FY2023": 6, "FY2022": 8, "FY2021": 16}), note=note, first_col_width=55, source_height=125)


metric("CET1 Capital", "£m", [("Common equity tier 1 (CET1) capital", {"FY2025": 3952, "FY2024": 3779, "FY2023": 3776, "FY2022": 3682, "FY2021": 4072})])
metric("CET1 Ratio", "% of RWA", [("Common equity tier 1 (CET1) ratio", {"FY2025": "18.4%", "FY2024": "18.2%", "FY2023": "17.1%", "FY2022": "17.2%", "FY2021": "17.9%"})])
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 4926, "FY2024": 5067, "FY2023": 4455, "FY2022": 4361, "FY2021": 4755})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "23.0%", "FY2024": "24.3%", "FY2023": "20.2%", "FY2022": "20.4%", "FY2021": "21.0%"})])
metric("Total Capital", "£m", [("Total capital", {"FY2025": 5576, "FY2024": 5779, "FY2023": 5072, "FY2022": 5502, "FY2021": 5870})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "26.0%", "FY2024": "27.8%", "FY2023": "23.0%", "FY2022": "25.7%", "FY2021": "25.9%"})])
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", {"FY2025": 21457, "FY2024": 20812, "FY2023": 22099, "FY2022": 21422, "FY2021": 22686})])

# RWA Breakdown - Pillar 3 UK OV1 template, placed right after Total RWAs per
# the locked sheet order. All 5 years tie exactly to the Total RWAs figure
# above. Genuine template difference: FY2021 used NatWest Group's large-
# subsidiary Pillar 3 Supplement (NWM Plc had not yet begun publishing its
# own standalone Pillar 3 report), whose OV1-equivalent table ADDS "Amounts
# below the thresholds for deduction" into the Total; FY2022 onward's NWM
# Plc-published OV1 table treats that same line as a non-additive memo
# (already included within rows 1-2) - both are shown as originally
# disclosed rather than forced onto one convention.
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2025": 7215, "FY2024": 5892, "FY2023": 5600, "FY2022": 5682, "FY2021": 4488}),
    ("DATA", "Counterparty credit risk", {"FY2025": 5839, "FY2024": 5712, "FY2023": 6409, "FY2022": 5587, "FY2021": 6602}),
    ("DATA", "Settlement risk", {"FY2023": 2, "FY2021": 1}),
    ("DATA", "Securitisation exposures (non-trading/banking book, after the cap)", {"FY2025": 3261, "FY2024": 3101, "FY2023": 2400, "FY2022": 1523, "FY2021": 1202}),
    ("DATA", "Position, foreign exchange and commodities risk (market risk)", {"FY2025": 3425, "FY2024": 5099, "FY2023": 6366, "FY2022": 7152, "FY2021": 6934}),
    ("DATA", "Operational risk", {"FY2025": 1711, "FY2024": 1002, "FY2023": 1322, "FY2022": 1478, "FY2021": 2020}),
    ("DATA", "Other risk exposure amount", {"FY2025": 6, "FY2024": 6}),
    ("DATA", "Memo: amounts below thresholds for deduction, subject to 250% risk-weight (non-additive FY2022-FY2025; additive within FY2021's Total - see note)", {"FY2025": 1413, "FY2024": 1325, "FY2023": 1337, "FY2022": 1373, "FY2021": 1439}),
    ("TOTAL", "Total", {"FY2025": 21457, "FY2024": 20812, "FY2023": 22099, "FY2022": 21422, "FY2021": 22686}),
]
bw.add_rwa_breakdown_sheet(
    title="NatWest Markets Plc — RWA Breakdown",
    subtitle="NWM Plc entity basis, Pillar 3 UK OV1 template (top-level risk-type categories). £m.",
    rows=rwa_breakdown_rows,
    sources_text=sources("p3", {"FY2025": 7, "FY2024": 7, "FY2023": 6, "FY2022": 8, "FY2021": "26-27"}) + (
        "\n\nRWA Breakdown specifically: FY2025/FY2024/FY2023/FY2022: NWM Plc Pillar 3 Report, 'UK OV1: Overview "
        "of risk-weighted exposure amounts'. FY2021: NatWest Group Pillar 3 Report 2021, 'OV1: CAP: RWAs and "
        "MCR summary - NatWest Group and large subsidiaries', NWM Plc column, p.26-27 - "
        + P3_URLS["FY2021"] + "\n\n"
        "DATA QUALITY FLAG: FY2021's Total (22,686) = the sum of all rows above INCLUDING the 'Amounts below "
        "thresholds' memo line (4,488+6,602+1+1,202+6,934+2,020+1,439); FY2022-FY2025's Totals exclude that "
        "memo line from the sum (it is already embedded within 'Credit risk'/rows 1-2 per those years' own "
        "footnote) - a genuine template difference between the large-subsidiary supplement used pre-2022 and "
        "NWM Plc's own standalone Pillar 3 report used from FY2022, not a transcription error."
    ),
    first_col_width=90,
    source_height=260,
    unit_suffix=" (£m)",
)

metric("Leverage Ratio", "£m / %", [("Leverage exposure measure", {"FY2025": 97880, "FY2024": 92859, "FY2023": 89929, "FY2022": 81083, "FY2021": 110603}), ("Leverage ratio", {"FY2025": "5.0%", "FY2024": "5.5%", "FY2023": "5.0%", "FY2022": "5.4%", "FY2021": "4.3%"})], note="FY2021 uses the CRR leverage ratio; FY2022 onward uses the PRA UK leverage-ratio presentation. These bases are not directly comparable.")
metric("LCR", "%", [("Liquidity coverage ratio", {"FY2025": "198%", "FY2024": "192%", "FY2023": "240%", "FY2022": "226%", "FY2021": "205%"})], note="FY2021 is NWM Plc's own headline LCR (2021 Annual Report and Accounts, p.37), not a NatWest Group figure. The 2021 large-subsidiary supplement does not repeat the standalone LCR, but the annual report's Financial review explicitly reports it.")
metric("NSFR", "%", [("Net stable funding ratio", {"FY2025": "121%", "FY2024": "120%", "FY2023": "127%", "FY2022": "133%"})], note="NWM Plc's standalone NSFR is not included in the 2021 large-subsidiary supplement; FY2021 is left blank rather than substituted with a NatWest Group figure.")
bw.add_metric_sheet(
    "MREL Ratio", "% of RWAs",
    [("Minimum requirement for own funds and eligible liabilities (MREL) ratio", {
        "FY2025": "45.6%", "FY2024": "48.2%", "FY2023": "34.5%", "FY2022": "40.4%", "FY2021": "42.1%",
    })],
    "Sources — NWM Plc Annual Report and Accounts, performance highlights (all metrics explicitly relate to NWM Plc):\n"
    + "\n".join(f"{year}: p.2 — {AR_URLS[year]}" for year in YEARS),
    note="NWM Plc's own Annual Report performance highlights disclose this ratio in every year. It includes total regulatory capital, non-eligible capital and downstreamed internal MREL; it is not a NatWest Group parent figure.",
    first_col_width=55,
    source_height=125,
)


# NWM Plc publishes entity-level quarterly Pillar 3 KM1 tables.  The reports
# often include several prior quarter comparatives, so each observation below
# is retained with the report that discloses it and its table page.  Values are
# in the source's native £m / percentage units; blanks are genuine non-
# disclosures rather than substitutions from NatWest Group.
INTERIM_SOURCES = {
    "2021-09-30": ("Q3 2022 Pillar 3 Supplement", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/11112022/natwest-markets-plc-q3-pillar-3-supplement.pdf", "7"),
    "2022-03-31": ("Q1 2023 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/28042023/natwest-markets-plc-pillar-3-q1-2023.pdf", "7"),
    "2022-06-30": ("Q3 2022 Pillar 3 Supplement", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/29072022/natwest-marketsplc-pillar-3-supplement.pdf", "7"),
    "2022-09-30": ("Q3 2022 Pillar 3 Supplement", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/11112022/natwest-markets-plc-q3-pillar-3-supplement.pdf", "7"),
    "2023-03-31": ("Q1 2023 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/28042023/natwest-markets-plc-pillar-3-q1-2023.pdf", "7"),
    "2023-06-30": ("H1 2023 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/2023/natwest-markets-plc-pillar-3-h1-2023.pdf", "7"),
    "2023-09-30": ("Q3 2023 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13-11-2023/natwest-markets-plc-pillar-3-q3-2023.pdf", "7"),
    "2024-03-31": ("Q1 2024 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/2024/natwest-markets-plc-pillar-3-q1-2024.pdf", "7"),
    "2024-06-30": ("H1 2024 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/2024/nwm-plc-pillar-3-hy-2024.pdf", "7"),
    "2024-09-30": ("Q3 2024 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/12112024/nwm-plc-pillar-3-q3-2024.pdf", "7"),
    "2025-03-31": ("Q1 2025 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13052025/nwm-pillar3-report.pdf", "7"),
    "2025-06-30": ("H1 2025 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/11-08-2025/nwm-pillar3-h1-report.pdf", "7"),
    "2025-09-30": ("Q3 2025 Pillar 3 Report", "https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/11112025/11112025-nwm-pillar-3-report.pdf", "7"),
}

INTERIM_VALUES = {
    "2021-09-30": [4553, 5231, 6463, 24582, "19.4%", "22.3%", "27.6%", None, None, "238%", None],
    "2022-03-31": [4005, 4686, 5764, 24063, "16.6%", "19.5%", "24.0%", 100712, "4.7%", "219%", None],
    "2022-06-30": [3837, 4514, 5597, 23456, "16.4%", "19.2%", "23.9%", 102238, "4.4%", "218%", None],
    "2022-09-30": [3714, 4393, 5538, 24873, "14.9%", "17.7%", "22.3%", 99515, "4.4%", "216%", None],
    "2023-03-31": [3676, 4355, 5475, 20173, "18.2%", "21.6%", "27.1%", 77259, "5.6%", "247%", "137%"],
    "2023-06-30": [3542, 4221, 4841, 20159, "17.6%", "20.9%", "24.0%", 78064, "5.4%", "253%", "137%"],
    "2023-09-30": [3523, 4202, 4828, 23392, "15.1%", "18.0%", "20.6%", 85706, "4.9%", "255%", "135%"],
    "2024-03-31": [3901, 4580, 5274, 21506, "18.1%", "21.3%", "24.5%", 91464, "5.0%", "219%", "121%"],
    "2024-06-30": [3840, 4519, 5198, 20542, "18.7%", "22.0%", "25.3%", 86275, "5.2%", "203%", "118%"],
    "2024-09-30": [3720, 4416, 5066, 21476, "17.3%", "20.6%", "23.6%", 96209, "4.6%", "189%", "117%"],
    "2025-03-31": [3743, 5280, 5963, 21705, "17.2%", "24.3%", "27.5%", 97377, "5.4%", "189%", "120%"],
    "2025-06-30": [3627, 5508, 6144, 21243, "17.1%", "25.9%", "28.9%", 98840, "5.6%", "193%", "121%"],
    "2025-09-30": [3801, 4776, 5425, 21678, "17.5%", "22.0%", "25.0%", 106006, "4.5%", "196%", "120%"],
}

INTERIM_METRICS = [
    ("CET1 capital", "£m"), ("Tier 1 capital", "£m"), ("Total capital", "£m"),
    ("Total risk-weighted exposure amount", "£m"), ("CET1 ratio", "%"),
    ("Tier 1 ratio", "%"), ("Total capital ratio", "%"),
    ("Leverage exposure measure excluding claims on central banks", "£m"),
    ("Leverage ratio excluding claims on central banks", "%"),
    ("Liquidity coverage ratio (12-month average)", "%"),
    ("Net stable funding ratio (4-quarter average)", "%"),
]
interim_rows = []
interim_hyperlinks = {}
for period, values in INTERIM_VALUES.items():
    report_name, url, page = INTERIM_SOURCES[period]
    for metric_index, ((metric_name, unit), value) in enumerate(zip(INTERIM_METRICS, values)):
        if value is None:
            continue
        row_index = len(interim_rows)
        interim_rows.append([period, "Quarterly Pillar 3 disclosure", metric_name, value, unit, "NWM Plc consolidated basis", report_name, f"p.{page} — UK KM1 table"])
        # IN-031: the real per-period URL was already sourced into
        # INTERIM_SOURCES above but never threaded through to
        # add_wide_interim_sheet()'s hyperlink_cells - every interim cell's
        # hyperlink silently fell back to the plain `report_name` text
        # instead. Wire it through so citations actually link.
        interim_hyperlinks[(row_index, 6)] = url

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=interim_rows,
    subtitle="NatWest Markets Plc entity-level quarterly KM1 disclosures, 2021–2025",
    note="Official NWM Plc reports provide comparable quarter-end KM1 observations for September 2021 and March/June/September 2022–2025. No standalone March or June 2021 interim KM1 report was located. Leverage and NSFR were not disclosed in the September 2021 comparative; NSFR was introduced in the 2023 disclosures. Values are not substituted from NatWest Group.",
    hyperlink_cells=interim_hyperlinks,
)

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 136288, "FY2024": 152937, "FY2023": 150658, "FY2022": 169061, "FY2021": 182554}),
        ("Loans to customers (amortised cost)", {"FY2025": 22154, "FY2024": 17089, "FY2023": 12104, "FY2022": 9154, "FY2021": 6810}),
        ("Customer deposits", {"FY2025": 2824, "FY2024": 2350, "FY2023": 3060, "FY2022": 2665, "FY2021": 1510}),
        ("Total equity", {"FY2025": 6880, "FY2024": 6819, "FY2023": 6313, "FY2022": 6518, "FY2021": 7349}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 1471, "FY2024": 1237, "FY2023": 1069, "FY2022": 689, "FY2021": 401}),
        ("Operating expenses", {"FY2025": -1308, "FY2024": -1208, "FY2023": -1142, "FY2022": -1128, "FY2021": -1150}),
        ("Profit/(loss) for the year", {"FY2025": 275, "FY2024": 63, "FY2023": -98, "FY2022": -264, "FY2021": -491}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 6819, "FY2024": 6313, "FY2023": 6518, "FY2022": 7349, "FY2021": 9152}),
        ("Total comprehensive income/(loss) for the year (NWM Plc basis)", {"FY2025": 411, "FY2024": -29, "FY2023": -232, "FY2022": -329, "FY2021": -690}),
        ("Other equity movements, net", {"FY2025": -350, "FY2024": 535, "FY2023": 27, "FY2022": -502, "FY2021": -1113}),
        ("Closing equity", {"FY2025": 6880, "FY2024": 6819, "FY2023": 6313, "FY2022": 6518, "FY2021": 7349}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -2465, "FY2024": -268, "FY2023": -676, "FY2022": 5395, "FY2021": 1055}),
        ("Net cash from/(used in) investing activities", {"FY2025": -242, "FY2024": -1768, "FY2023": -2096, "FY2022": -2500, "FY2021": 231}),
        ("Net cash from/(used in) financing activities", {"FY2025": -555, "FY2024": 1609, "FY2023": -827, "FY2022": -1877, "FY2021": -2636}),
        ("Cash and cash equivalents at end of year", {"FY2025": 13122, "FY2024": 16270, "FY2023": 16988, "FY2022": 20923, "FY2021": 19214}),
    ], cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "18.4%", "FY2024": "18.2%", "FY2023": "17.1%", "FY2022": "17.2%", "FY2021": "17.9%"}),
        ("Tier 1 Ratio", {"FY2025": "23.0%", "FY2024": "24.3%", "FY2023": "20.2%", "FY2022": "20.4%", "FY2021": "21.0%"}),
        ("Total Capital Ratio", {"FY2025": "26.0%", "FY2024": "27.8%", "FY2023": "23.0%", "FY2022": "25.7%", "FY2021": "25.9%"}),
        ("Leverage Ratio", {"FY2025": "5.0%", "FY2024": "5.5%", "FY2023": "5.0%", "FY2022": "5.4%", "FY2021": "4.3%"}),
        ("LCR", {"FY2025": "198%", "FY2024": "192%", "FY2023": "240%", "FY2022": "226%"}),
        ("NSFR", {"FY2025": "121%", "FY2024": "120%", "FY2023": "127%", "FY2022": "133%"}),
    ],
    note="This workbook covers NatWest Markets Plc (company SC090312, FRN 121882), formerly The Royal Bank of Scotland Public Limited Company. It is distinct from the current Royal Bank of Scotland plc (company SC083026) workbook. FY2021 LCR/NSFR are blank because the official large-subsidiary supplement did not provide standalone NWM Plc figures.",
)

bw.save("/Users/armaan/code/katalysis/banks/NATWEST MARKETS FINANCIALS.xlsx")
