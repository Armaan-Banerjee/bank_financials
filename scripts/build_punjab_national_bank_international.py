import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022"]
YEAR_LABEL = {y: y for y in YEARS}

BASE = "https://www.pnbint.com/PNBIL/pdf/Financial_Reports/"
AR_URL = {
    "FY2026": BASE + "PNBIL-Annual-Report-2026.pdf",
    "FY2025": BASE + "PNBIL%20Annual%20Report%202025.pdf",
    "FY2024": BASE + "Annual_Report_31-03-2024.pdf",
    "FY2023": BASE + "PNBIL_Annual_Report_2023.pdf",
    "FY2022": BASE + "AnnualReport20220331.pdf",
}
P3_URL = {
    "FY2026": BASE + "Basel-III-Pillar-3-Disclosure-31-03-2026.pdf",
    "FY2025": BASE + "Basel%20III%20Pillar%203%20Disclosures%2031-03-2025.pdf",
    "FY2024": BASE + "Basel_III_Pillar_3_Disclosures%2031-03-2024.pdf",
    "FY2023": BASE + "PNBIL%20Pillar%20III%20Disclosures%20Publish%20Version.pdf",
    "FY2022": BASE + "Basel%20III%20Pillar%203%20Disclosures%20%2031-03-2022.pdf",
}

# Rates are £1 = US$X from the Bank of England XUDLUSS series.  Flow rates are
# averages over each 1 April-31 March financial year; stocks use the final
# available business-day spot rate at 31 March.  FY2022 opening cash uses the
# 31 March 2021 spot rate because it is shown as a comparative in the FY2022
# accounts.
FX_SPOT = {"FY2026": 1.3188, "FY2025": 1.2910, "FY2024": 1.2632,
           "FY2023": 1.2364, "FY2022": 1.3162, "FY2021": 1.3796}
FX_AVG = {"FY2026": 1.3404, "FY2025": 1.2763, "FY2024": 1.2568,
          "FY2023": 1.2045, "FY2022": 1.3662}
PREVIOUS_SPOT = {"FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023",
                 "FY2025": "FY2024", "FY2026": "FY2025"}


def flow(values):
    return {y: round(v / FX_AVG[y], 1) for y, v in values.items()}


def stock(values):
    return {y: round(v / FX_SPOT[y], 1) for y, v in values.items()}


ENTITY_NOTE = (
    "Punjab National Bank (International) Limited (Companies House company 05781326, FRN 459701) is an active UK "
    "private limited bank, incorporated in England and Wales and wholly owned by Punjab National Bank, India. The "
    "FY2026 annual report confirms the registered office at 1 Moorgate, London EC2R 6JH, no branches outside the UK, "
    "and UK-adopted International Accounting Standards. The financial statements are entity-level and presented in "
    "US Dollars because that is the Bank's functional currency. The Bank's own Pillar 3 disclosures are solo-basis; "
    "PNB India consolidates the group separately. The Bank has a genuine Statement of Cash Flows in every report used."
)

FX_NOTE = (
    "USD-to-GBP conversion: cash-flow flows use the Bank of England XUDLUSS average rate for the 1 April-31 March "
    "financial year, while cash balances and Pillar 3 dollar amounts use the final available Bank of England spot "
    "rate at 31 March. Rates (£1 = $X) were FY2022 1.3662 average/1.3162 spot, FY2023 1.2045/1.2364, FY2024 "
    "1.2568/1.2632, FY2025 1.2763/1.2910, and FY2026 1.3404/1.3188. The FY2022 opening balance uses the 31 March "
    "2021 spot rate of 1.3796. Ratios remain exactly as reported because they are dimensionless. A computed GBP "
    "translation line reconciles the use of different flow and stock rates; it is not a Bank-reported cash-flow line."
)

CASH_FLOW_SOURCES = (
    "Sources - Punjab National Bank (International) Limited entity-level Statement of Cash Flows (native unit $'000):\n"
    "FY2026: Annual Report and Accounts 2026, printed p.50 - " + AR_URL["FY2026"] + "\n"
    "FY2025: Annual Report and Accounts 2025, printed p.49 - " + AR_URL["FY2025"] + "\n"
    "FY2024: Annual Report and Accounts 2024, printed p.44 - " + AR_URL["FY2024"] + "\n"
    "FY2023: Annual Report and Accounts 2023, printed p.39 - " + AR_URL["FY2023"] + "\n"
    "FY2022: Annual Report and Accounts 2022, printed p.36; FY2021 comparative is not needed for this five-year window - " + AR_URL["FY2022"] + "\n\n"
    + ENTITY_NOTE + "\n" + FX_NOTE
)


def p3_sources():
    return (
        "Sources - Punjab National Bank (International) Limited solo-basis Pillar 3 UK KM1 key metrics table, "
        "native unit $ million:\n"
        + "\n".join([
            f"FY2026: {P3_URL['FY2026']}, printed p.6 (2026 KM1)",
            f"FY2025: {P3_URL['FY2025']}, printed p.6 (2025 KM1)",
            f"FY2024: {P3_URL['FY2024']}, printed p.6 (2024 KM1)",
            f"FY2023: {P3_URL['FY2023']}, printed p.6 (2023 KM1)",
            f"FY2022: {P3_URL['FY2023']}, printed p.6 (2022 comparative in 2023 KM1); the 2022 report's headline ratios are also confirmed at printed p.5 via {P3_URL['FY2022']}",
        ])
        + "\n\n" + ENTITY_NOTE
    )


# Native cash-flow figures, $'000.  Each report's own current-year column is
# used; later reports' comparative columns were checked for continuity.
OPERATING = {
    "FY2026": 63882, "FY2025": 3518, "FY2024": -29200,
    "FY2023": 7735, "FY2022": -20687,
}
INVESTING = {
    "FY2026": -28192, "FY2025": -7088, "FY2024": 22199,
    "FY2023": -9217, "FY2022": -48112,
}
FINANCING = {
    "FY2026": -15391, "FY2025": -15689, "FY2024": -5568,
    "FY2023": -4493, "FY2022": -3305,
}
NET_CHANGE = {
    "FY2026": 23169, "FY2025": -17279, "FY2024": -10789,
    "FY2023": -5975, "FY2022": -72104,
}
EXCHANGE = {"FY2026": 2870, "FY2025": 1980, "FY2024": 1780,
            "FY2023": 998, "FY2022": 582}
OPENING_USD = {"FY2026": 116753, "FY2025": 134032, "FY2024": 144821,
               "FY2023": 149798, "FY2022": 221320}
CLOSING_USD = {"FY2026": 139922, "FY2025": 116753, "FY2024": 134032,
               "FY2023": 144821, "FY2022": 149798}

opening = {
    y: round(OPENING_USD[y] / FX_SPOT[PREVIOUS_SPOT[y]], 1) for y in YEARS
}
closing = stock(CLOSING_USD)
translation = {
    y: round(closing[y] - opening[y] - flow(NET_CHANGE)[y] - flow(EXCHANGE)[y], 1)
    for y in YEARS
}

rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash (used in)/generated from operating activities", flow(OPERATING)),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", flow(INVESTING)),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash used in financing activities", flow(FINANCING)),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", flow(NET_CHANGE)),
    ("DATA", "Effects of exchange rate on cash and cash equivalents (Bank's own line)", flow(EXCHANGE)),
    ("DATA", "Effect of GBP/USD translation (this workbook's conversion line)", translation),
    ("DATA", "Cash and cash equivalents at beginning of year", opening),
    ("TOTAL", "Cash and cash equivalents at end of year", closing),
]

bw = BankWorkbook(bank_name="Punjab National Bank (International) Limited", years=YEARS,
                  year_label=YEAR_LABEL, header_color="5C2751")

STATEMENTS_SOURCES = (
    "Sources - Punjab National Bank (International) Limited entity-level Balance Sheet / Profit & Loss / "
    "Statement of Changes in Equity (native unit $'000):\n"
    "FY2026: Annual Report and Accounts 2026, Statement of Financial Position/Comprehensive Income/Changes in "
    "Equity, printed pp.47-49 - " + AR_URL["FY2026"] + "\n"
    "FY2025: Annual Report and Accounts 2025, printed pp.46-48 - " + AR_URL["FY2025"] + "\n"
    "FY2024: Annual Report and Accounts 2024, printed pp.41-43 - " + AR_URL["FY2024"] + "\n"
    "FY2023: Annual Report and Accounts 2023, printed pp.36-38 - " + AR_URL["FY2023"] + "\n"
    "FY2022: Annual Report and Accounts 2022, printed pp.33-35 - " + AR_URL["FY2022"] + "\n\n"
    + ENTITY_NOTE + "\n" + FX_NOTE + "\n\n"
    "GBP CONVERSION NOTE (Balance Sheet/Equity balances, Profit & Loss/Equity movements): balance-date figures "
    "(Balance Sheet lines, equity opening/closing balances) use the 31 March spot rate of that balance date; "
    "period figures (Profit & Loss lines, equity movement rows) use the financial year's average rate. Because "
    "these are two different rates, a computed 'GBP translation adjustment' row is shown on the equity sheet for "
    "each year to keep the GBP columns arithmetically closed - it is not a Bank-reported line."
)

# FY2022's own Balance Sheet (Annual Report and Accounts 2022, p.34) shows Total assets $1,126,259k and Loans
# and advances to customers $791,237k; the FOLLOWING year's report (AR2023, p.37) later gives a different FY2022
# comparative ($1,123,130k / $788,108k respectively) with no explanatory note found in AR2023. Each year's own
# originally-published figure is used for that year's column, per this project's standing convention - the
# discrepancy is flagged here rather than silently reconciled.
BS_DISCREPANCY_NOTE = (
    "DATA QUALITY FLAG: FY2022's Balance Sheet uses the Bank's own FY2022 Annual Report figures (Total assets "
    "$1,126,259k, Loans and advances to customers $791,237k). AR2023's own FY2022 comparative column later shows "
    "different figures ($1,123,130k / $788,108k) with no explanatory note found - a genuine cross-report "
    "inconsistency in the Bank's own disclosures, not a transcription error here; each year's own originally-"
    "published figure is used per this project's convention. Separately, FY2024's Deferred tax assets ($24,862k, "
    "AR2024's own figure) differs by exactly $233k from AR2025's own FY2024 comparative ($24,629k) - this is the "
    "same restatement AR2025 itself discloses affecting the fair value reserve (see Note 28/Note 35, also visible "
    "on the Statement of Changes in Equity sheet's bridging row)."
)

BS_ASSETS = {
    "Cash and balances with banks": {"FY2026": 139922, "FY2025": 116753, "FY2024": 134032, "FY2023": 144821, "FY2022": 149798},
    "Financial assets at fair value through profit or loss": {"FY2026": 1014, "FY2025": 964, "FY2024": 3029, "FY2023": 0, "FY2022": 10001},
    "Derivative financial instruments (asset)": {"FY2026": 2925, "FY2025": 156, "FY2024": 14, "FY2023": 7, "FY2022": 1064},
    "Loans and advances to banks": {"FY2026": 1453, "FY2025": 1352, "FY2024": 10496, "FY2023": 836, "FY2022": 700},
    "Loans and advances to customers": {"FY2026": 1131159, "FY2025": 903981, "FY2024": 772119, "FY2023": 748698, "FY2022": 791237},
    "Investment securities at amortised cost": {"FY2026": 63199, "FY2025": 75947, "FY2024": 65117, "FY2023": 108096, "FY2022": 89114},
    "Financial assets at amortised cost (subtotal, as disclosed FY2024-FY2026)": {"FY2026": 1195811, "FY2025": 981280, "FY2024": 847732},
    "Financial assets at fair value through other comprehensive income": {"FY2026": 110830, "FY2025": 71606, "FY2024": 72866, "FY2023": 55263, "FY2022": 54753},
    "Right of use lease assets": {"FY2026": 4394, "FY2025": 2946, "FY2024": 3685, "FY2023": 4395, "FY2022": 3073},
    "Property, plant and equipment": {"FY2026": 1034, "FY2025": 237, "FY2024": 287, "FY2023": 311, "FY2022": 391},
    "Intangible assets": {"FY2026": 485, "FY2025": 126, "FY2024": 180, "FY2023": 230, "FY2022": 589},
    "Deferred tax assets": {"FY2026": 24463, "FY2025": 24441, "FY2024": 24862, "FY2023": 24990, "FY2022": 25155},
    "Prepayments and other receivables": {"FY2026": 1575, "FY2025": 1117, "FY2024": 591, "FY2023": 533, "FY2022": 384},
}
BS_TOTAL_ASSETS = {"FY2026": 1482453, "FY2025": 1199626, "FY2024": 1087278, "FY2023": 1088180, "FY2022": 1126259}

BS_LIABILITIES = {
    "Deposits from banks": {"FY2026": 50355, "FY2025": 2311, "FY2024": 3292, "FY2023": 1967, "FY2022": 1106},
    "Deposits from customers": {"FY2026": 1184925, "FY2025": 916442, "FY2024": 811182, "FY2023": 816636, "FY2022": 858073},
    "Derivative financial instruments (liability)": {"FY2026": 16, "FY2025": 1471, "FY2024": 159, "FY2023": 155, "FY2022": 295},
    "Current tax liability": {"FY2023": 0, "FY2022": 0},
    "Repurchase agreement - non trading": {"FY2026": 0, "FY2025": 20868},
    "Lease liability": {"FY2026": 4603, "FY2025": 3173, "FY2024": 3870, "FY2023": 4522, "FY2022": 3205},
    "Other liabilities": {"FY2026": 2182, "FY2025": 3092, "FY2024": 2639, "FY2023": 1572, "FY2022": 5314},
    "Subordinated bonds and other borrowed funds": {"FY2026": 30997, "FY2025": 41108, "FY2024": 51252, "FY2023": 50000, "FY2022": 50000},
}
BS_TOTAL_LIABILITIES = {"FY2026": 1273078, "FY2025": 988465, "FY2024": 872394, "FY2023": 874852, "FY2022": 917993}

BS_EQUITY_NATIVE = {
    "Share capital": {"FY2026": 319631, "FY2025": 319631, "FY2024": 319631, "FY2023": 319631, "FY2022": 319631},
    "Fair value reserve": {"FY2026": -123, "FY2025": 279, "FY2024": -807, "FY2023": -986, "FY2022": -1293},
    "Retained earnings": {"FY2026": -110133, "FY2025": -108749, "FY2024": -103940, "FY2023": -105317, "FY2022": -110072},
}
BS_TOTAL_EQUITY_NATIVE = {"FY2026": 209375, "FY2025": 211161, "FY2024": 214884, "FY2023": 213328, "FY2022": 208266}


def stock_rows(native_dict):
    return {label: stock(values) for label, values in native_dict.items()}


balance_sheet_rows = (
    [("SECTION", "Assets", {})]
    + [("DATA", label, stock(values)) for label, values in BS_ASSETS.items()]
    + [("TOTAL", "Total assets", stock(BS_TOTAL_ASSETS))]
    + [("SECTION", "Liabilities", {})]
    + [("DATA", label, stock(values)) for label, values in BS_LIABILITIES.items()]
    + [("TOTAL", "Total liabilities", stock(BS_TOTAL_LIABILITIES))]
    + [("SECTION", "Equity", {})]
    + [("DATA", label, stock(values)) for label, values in BS_EQUITY_NATIVE.items()]
    + [("TOTAL", "Total equity", stock(BS_TOTAL_EQUITY_NATIVE))]
    + [("TOTAL", "Total liabilities and equity", stock({y: BS_TOTAL_LIABILITIES[y] + BS_TOTAL_EQUITY_NATIVE[y] for y in YEARS}))]
)

bw.add_balance_sheet_sheet(
    title="Punjab National Bank (International) Limited — Balance Sheet",
    subtitle="Entity-level Statement of Financial Position, £'000 converted from the Bank's native US$'000 "
             "presentation. Blank cells indicate a line not disclosed/not applicable that year.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + BS_DISCREPANCY_NOTE,
    first_col_width=90,
    source_height=380,
    unit_suffix=" (£'000, conv. from USD)",
)

# Profit & Loss (Statement of Comprehensive Income), native $'000. OCI presentation genuinely changed between
# FY2024 (gains arising/tax/reclassification) and FY2025 (disposal transfer/gains/tax) - both shown on their own
# basis rather than forced into one template; only Profit after tax and the two Total rows are comparable across
# every year.
PL_PROFIT = {"FY2026": 2937, "FY2025": 750, "FY2024": 6211, "FY2023": 8333, "FY2022": 7906}
PL_OCI_OLD = {  # FY2022-FY2024 presentation
    "FVOCI gains/(losses) arising during the year": {"FY2024": 248, "FY2023": -79, "FY2022": -2066},
    "Tax credit/(charge) relating to change in fair value": {"FY2024": -62, "FY2023": -9, "FY2022": 496},
    "Reclassification adjustment transferred to P&L": {"FY2024": -7, "FY2023": 395, "FY2022": 209},
}
PL_OCI_NEW = {  # FY2025-FY2026 presentation
    "Fair value gains/(losses) transferred to income statement on disposal": {"FY2026": -613, "FY2025": 258},
    "Fair value gains on Investment Securities - FVOCI": {"FY2026": 77, "FY2025": 268},
    "Income tax on other comprehensive income items": {"FY2026": 134, "FY2025": -130},
}
PL_OCI_TOTAL = {"FY2026": -402, "FY2025": 396, "FY2024": 179, "FY2023": 307, "FY2022": -1361}
PL_TOTAL_COMPREHENSIVE = {"FY2026": 2535, "FY2025": 1146, "FY2024": 6390, "FY2023": 8640, "FY2022": 6545}

income_statement_rows = (
    [("SECTION", "Income", {}), ("TOTAL", "Profit after tax for the year", flow(PL_PROFIT))]
    + [("SECTION", "Other comprehensive income - FY2022-FY2024 presentation", {})]
    + [("DATA", label, flow(values)) for label, values in PL_OCI_OLD.items()]
    + [("SECTION", "Other comprehensive income - FY2025-FY2026 presentation", {})]
    + [("DATA", label, flow(values)) for label, values in PL_OCI_NEW.items()]
    + [("TOTAL", "Other comprehensive income for the year, net of tax", flow(PL_OCI_TOTAL))]
    + [("TOTAL", "Total comprehensive income for the year, net of tax", flow(PL_TOTAL_COMPREHENSIVE))]
)

bw.add_income_statement_sheet(
    title="Punjab National Bank (International) Limited — Profit & Loss",
    subtitle="Entity-level Statement of Comprehensive Income, £'000 converted from the Bank's native US$'000 "
             "presentation. OCI's underlying line-item structure changed between FY2024 and FY2025 - each year "
             "shown on its own contemporaneous basis; only Profit after tax and the two Total rows are directly "
             "comparable across all 5 years.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=92,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# Statement of Changes in Equity - chronological roll-forward. Equity ladder confirmed exactly in native USD
# terms across all 5 years (FY2021 opening through FY2026 closing) except one genuine, Bank-disclosed
# restatement: AR2025's own FY2024 comparative fair value reserve/retained earnings/deferred tax figures differ
# from AR2024's own originally-published FY2024 closing figures (see Note 28/Note 35 in AR2025) - shown as its
# own explicit bridging row rather than silently absorbed into a movement line.
EQUITY_HEADERS = ["Share capital", "Fair value reserve", "Retained earnings", "Total equity"]


def eq_stock(share, fv, re_, total, year_for_rate):
    return (stock({year_for_rate: share})[year_for_rate], stock({year_for_rate: fv})[year_for_rate],
            stock({year_for_rate: re_})[year_for_rate], stock({year_for_rate: total})[year_for_rate])


def eq_flow(share, fv, re_, total, year_for_rate):
    vals = []
    for v in (share, fv, re_, total):
        vals.append(flow({year_for_rate: v})[year_for_rate] if v is not None else None)
    return tuple(vals)


equity_rows = []
# FY2022
equity_rows.append(("TOTAL", "Balance at 1 April 2021 (FY2022 opening)", eq_stock(319631, 68, -115611, 204088, "FY2021")))
equity_rows.append(("DATA", "Profit for the year", eq_flow(None, None, 7906, 7906, "FY2022")))
equity_rows.append(("DATA", "Net change in fair value of Investment Securities - FVOCI", eq_flow(None, -1570, None, -1570, "FY2022")))
equity_rows.append(("DATA", "Net amount transferred to Profit & Loss", eq_flow(None, 209, None, 209, "FY2022")))
equity_rows.append(("DATA", "Dividend on additional Tier 1 capital", eq_flow(None, None, -2367, -2367, "FY2022")))
equity_rows.append(("DATA", "GBP translation adjustment (this workbook's conversion line)", (None, None, None, None)))
equity_rows.append(("TOTAL", "Balance at 31 March 2022 (FY2022 closing)", eq_stock(319631, -1293, -110072, 208266, "FY2022")))
# FY2023
equity_rows.append(("DATA", "Profit for the year", eq_flow(None, None, 8333, 8333, "FY2023")))
equity_rows.append(("DATA", "Net change in fair value of Investment Securities - FVOCI", eq_flow(None, -88, None, -88, "FY2023")))
equity_rows.append(("DATA", "Net amount transferred to Profit & Loss", eq_flow(None, 395, None, 395, "FY2023")))
equity_rows.append(("DATA", "Dividend on additional Tier 1 capital", eq_flow(None, None, -3578, -3578, "FY2023")))
equity_rows.append(("DATA", "GBP translation adjustment (this workbook's conversion line)", (None, None, None, None)))
equity_rows.append(("TOTAL", "Balance at 31 March 2023 (FY2023 closing)", eq_stock(319631, -986, -105317, 213328, "FY2023")))
# FY2024 (AR2024's own figures)
equity_rows.append(("DATA", "Profit for the year", eq_flow(None, None, 6211, 6211, "FY2024")))
equity_rows.append(("DATA", "Net change in fair value of Investment Securities - FVOCI", eq_flow(None, 186, None, 186, "FY2024")))
equity_rows.append(("DATA", "Net amount transferred to Profit & Loss", eq_flow(None, -7, None, -7, "FY2024")))
equity_rows.append(("DATA", "Dividend on additional Tier 1 capital", eq_flow(None, None, -4834, -4834, "FY2024")))
equity_rows.append(("DATA", "GBP translation adjustment (this workbook's conversion line)", (None, None, None, None)))
equity_rows.append(("TOTAL", "Balance at 31 March 2024, as originally published in AR2024 (FY2024 closing)", eq_stock(319631, -807, -103940, 214884, "FY2024")))
# Restatement bridging row (AR2025's own Note 28/35 restatement, disclosed as "not material")
equity_rows.append(("DATA", "Restatement adjustment (AR2025's own Note 28/Note 35 fair value reserve/deferred tax correction, disclosed as not material)",
                     eq_flow(0, 690, -923, -233, "FY2024")))
equity_rows.append(("TOTAL", "Balance at 1 April 2024, as restated in AR2025 (FY2025 opening)", eq_stock(319631, -117, -104863, 214651, "FY2024")))
# FY2025
equity_rows.append(("DATA", "Profit for the year", eq_flow(None, None, 750, 750, "FY2025")))
equity_rows.append(("DATA", "Fair value gains/(losses) transferred to income statement on disposal", eq_flow(None, 258, None, 258, "FY2025")))
equity_rows.append(("DATA", "Fair value gains on Investment Securities - FVOCI (net of tax)", eq_flow(None, 138, None, 138, "FY2025")))
equity_rows.append(("DATA", "Dividend on additional Tier 1 capital", eq_flow(None, None, -4636, -4636, "FY2025")))
equity_rows.append(("DATA", "GBP translation adjustment (this workbook's conversion line)", (None, None, None, None)))
equity_rows.append(("TOTAL", "Balance at 31 March 2025 (FY2025 closing)", eq_stock(319631, 279, -108749, 211161, "FY2025")))
# FY2026
equity_rows.append(("DATA", "Profit for the year", eq_flow(None, None, 2937, 2937, "FY2026")))
equity_rows.append(("DATA", "Fair value gains/(losses) transferred to income statement on disposal", eq_flow(None, -613, None, -613, "FY2026")))
equity_rows.append(("DATA", "Fair value gains on Investment Securities - FVOCI (net of tax)", eq_flow(None, 211, None, 211, "FY2026")))
equity_rows.append(("DATA", "Dividend on additional Tier 1 capital", eq_flow(None, None, -4321, -4321, "FY2026")))
equity_rows.append(("DATA", "GBP translation adjustment (this workbook's conversion line)", (None, None, None, None)))
equity_rows.append(("TOTAL", "Balance at 31 March 2026 (FY2026 closing)", eq_stock(319631, -123, -110133, 209375, "FY2026")))

# Compute each year's translation-adjustment row so the GBP columns close arithmetically (closing - opening -
# sum of that year's own movement rows), same convention as the Cash Flow Statement's translation line.
_year_blocks = [
    (1, 6, "FY2022"), (7, 12, "FY2023"), (13, 18, "FY2024"),
    (21, 26, "FY2025"), (27, 32, "FY2026"),
]
for start, end, yr in _year_blocks:
    _eq_opening = equity_rows[start - 1][2]
    _eq_closing = equity_rows[end][2]
    movement_sum = [0.0, 0.0, 0.0, 0.0]
    for i in range(start, end):
        for ci, v in enumerate(equity_rows[i][2]):
            if v is not None:
                movement_sum[ci] += v
    translation = tuple(
        round(_eq_closing[ci] - _eq_opening[ci] - movement_sum[ci], 1) if _eq_closing[ci] is not None and _eq_opening[ci] is not None else None
        for ci in range(4)
    )
    equity_rows[end - 1] = ("DATA", equity_rows[end - 1][1], translation)

bw.add_equity_changes_sheet(
    title="Punjab National Bank (International) Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, entity-level, £'000 converted from the Bank's native "
              "US$'000 presentation. Equity ladder confirmed exactly in native USD terms across all 5 years - the "
              "one bridging row (AR2025's own Note 28/Note 35 restatement) is a genuine, Bank-disclosed item, not "
              "an error. GBP translation-adjustment rows arise only from converting a USD ladder using two "
              "different point-in-time/average rates - see the Balance Sheet sheet's GBP conversion note.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=100,
    source_height=280,
    col_width=17,
)

bw.add_cash_flow_sheet(
    title="Punjab National Bank (International) Limited — Statement of Cash Flows",
    subtitle="Entity-level basis, £'000 converted from the Bank's native US$'000 presentation",
    rows=rows, sources_text=CASH_FLOW_SOURCES, first_col_width=92, source_height=260,
    unit_suffix=" (£'000, conv. from USD)",
)

# Asset Quality: IFRS 9 Stage 1/2/3 gross/impairment/net exposure, combining Loans and advances to
# banks/customers and Investment securities at amortised cost (the "loans & advances at amortised cost by
# product" note table) - this combined net total ties exactly to the Balance Sheet's own "Financial assets at
# amortised cost" subtotal for FY2025/FY2026 (the only years that show that subtotal on the face of the Balance
# Sheet). FY2022/FY2023 don't tie exactly to their own Balance Sheet loan lines alone because the Bank's own
# footnotes disclose specific reconciling items (a $3,129k unamortised-fees restatement in FY2022; $33,890k of
# short-term bank placements reported as cash equivalents rather than loans in FY2023) - both genuine disclosed
# items, not gaps.
AQ_GROSS = {
    "Stage 1": {"FY2026": 1093759, "FY2025": 883431, "FY2024": 718452, "FY2023": 786625, "FY2022": 723702},
    "Stage 2": {"FY2026": 62543, "FY2025": 39431, "FY2024": 34493, "FY2023": 362, "FY2022": 40577},
    "Stage 3": {"FY2026": 95862, "FY2025": 129209, "FY2024": 255526, "FY2023": 284217, "FY2022": 308877},
}
AQ_GROSS_TOTAL = {"FY2026": 1252164, "FY2025": 1051071, "FY2024": 1008471, "FY2023": 1071204, "FY2022": 1073156}
AQ_IMPAIR = {
    "Stage 1": {"FY2026": 667, "FY2025": 521, "FY2024": 506, "FY2023": 3068, "FY2022": 1747},
    "Stage 2": {"FY2026": 20, "FY2025": 10, "FY2024": 2, "FY2023": 1, "FY2022": 147},
    "Stage 3": {"FY2026": 55666, "FY2025": 70262, "FY2024": 160233, "FY2023": 176961, "FY2022": 193340},
}
AQ_IMPAIR_TOTAL = {"FY2026": 56353, "FY2025": 70793, "FY2024": 160741, "FY2023": 180030, "FY2022": 195234}
AQ_NET = {
    "Stage 1": {"FY2026": 1093092, "FY2025": 882911, "FY2024": 717947, "FY2023": 783557, "FY2022": 721955},
    "Stage 2": {"FY2026": 62523, "FY2025": 39422, "FY2024": 34491, "FY2023": 361, "FY2022": 40430},
    "Stage 3": {"FY2026": 40196, "FY2025": 58947, "FY2024": 95293, "FY2023": 107256, "FY2022": 115537},
}
AQ_NET_TOTAL = {"FY2026": 1195811, "FY2025": 981280, "FY2024": 847731, "FY2023": 891174, "FY2022": 877922}
AQ_NPL_RATIO = {y: f"{AQ_GROSS['Stage 3'][y] / AQ_GROSS_TOTAL[y] * 100:.2f}%" for y in YEARS}
AQ_COVERAGE_RATIO = {y: f"{AQ_IMPAIR_TOTAL[y] / AQ_GROSS_TOTAL[y] * 100:.2f}%" for y in YEARS}

asset_quality_rows = (
    [("SECTION", "Gross carrying amount, by IFRS 9 stage (loans, banks, and investment securities at amortised cost)", {})]
    + [("DATA", f"Stage {s.split()[-1]} gross carrying amount", stock(AQ_GROSS[s])) for s in ["Stage 1", "Stage 2", "Stage 3"]]
    + [("TOTAL", "Total gross carrying amount", stock(AQ_GROSS_TOTAL))]
    + [("SECTION", "Impairment allowance, by IFRS 9 stage", {})]
    + [("DATA", f"Stage {s.split()[-1]} impairment allowance", stock(AQ_IMPAIR[s])) for s in ["Stage 1", "Stage 2", "Stage 3"]]
    + [("TOTAL", "Total impairment allowance", stock(AQ_IMPAIR_TOTAL))]
    + [("SECTION", "Net carrying amount, by IFRS 9 stage", {})]
    + [("DATA", f"Stage {s.split()[-1]} net carrying amount", stock(AQ_NET[s])) for s in ["Stage 1", "Stage 2", "Stage 3"]]
    + [("TOTAL", "Total net carrying amount", stock(AQ_NET_TOTAL))]
    + [("SECTION", "Asset quality ratios (derived)", {})]
    + [("DATA", "Stage 3 as % of total gross carrying amount (NPL ratio)", AQ_NPL_RATIO)]
    + [("DATA", "Total impairment allowance as % of total gross carrying amount (coverage)", AQ_COVERAGE_RATIO)]
)

bw.add_asset_quality_sheet(
    title="Punjab National Bank (International) Limited — Asset Quality",
    subtitle="Entity-level. IFRS 9 stage 1/2/3 split for Loans and advances to banks/customers and Investment "
             "securities at amortised cost combined (the Bank's own 'loans & advances at amortised cost by "
             "product' note table). £'000 converted from the Bank's native US$'000 presentation.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nFY2026: Note 19, printed p.80 - " + AR_URL["FY2026"] + "; FY2025: Note 19, printed p.77 - "
        + AR_URL["FY2025"] + " (FY2024 comparative also sourced here); FY2023: Note 19, printed p.67 - "
        + AR_URL["FY2023"] + " (FY2022 comparative also sourced here).\n\n"
        "A large, steadily-declining Stage 3 book is genuinely disclosed every year (28.79% of gross exposure in "
        "FY2022, down to 7.66% by FY2026) - not a transcription artefact; the Bank's own Annual Reports discuss "
        "legacy non-performing exposures being worked down over this period."
    ),
    first_col_width=88,
    source_height=280,
    unit_suffix=" (£'000, conv. from USD)",
)


def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, p3_sources(), note=note,
                        first_col_width=54, source_height=180)


CAPITAL_NOTE = "Directly disclosed in the annual Pillar 3 UK KM1 table; figures are converted from $m to £m at the corresponding 31 March spot rate."
RWA_NOTE = "Directly disclosed total risk-weighted exposure amount in the annual Pillar 3 UK KM1 table; converted from $m to £m at the corresponding 31 March spot rate."
LCR_NOTE = (
    "The Bank's own report-year headline LCR is used. FY2025's report shows 201% for FY2025, while its FY2024 "
    "comparative shows 528%; the FY2024 report itself reported 647% for FY2024. This workbook preserves each year's "
    "own as-reported figure rather than replacing it with a later comparative restatement."
)

CET1 = {"FY2026": 138.2, "FY2025": 140.8, "FY2024": 144.1, "FY2023": 143.1, "FY2022": 137.9}
TIER1 = {"FY2026": 183.2, "FY2025": 185.8, "FY2024": 189.1, "FY2023": 188.1, "FY2022": 182.9}
TOTAL_CAPITAL = {"FY2026": 210.9, "FY2025": 216.1, "FY2024": 223.1, "FY2023": 226.4, "FY2022": 213.9}
RWA = {"FY2026": 894.9, "FY2025": 697.1, "FY2024": 701.0, "FY2023": 730.1, "FY2022": 802.6}
CET1_RATIO = {"FY2026": "15.4%", "FY2025": "20.2%", "FY2024": "20.6%", "FY2023": "19.6%", "FY2022": "17.2%"}
TIER1_RATIO = {"FY2026": "20.5%", "FY2025": "26.7%", "FY2024": "27.0%", "FY2023": "25.8%", "FY2022": "22.8%"}
TOTAL_RATIO = {"FY2026": "23.6%", "FY2025": "31.0%", "FY2024": "31.8%", "FY2023": "31.0%", "FY2022": "26.7%"}
LEVERAGE = {"FY2026": "13.6%", "FY2025": "16.7%", "FY2024": "19.1%", "FY2023": "19.9%", "FY2022": "19.3%"}
LCR = {"FY2026": "350%", "FY2025": "201%", "FY2024": "647%", "FY2023": "384%", "FY2022": "405%"}
NSFR = {"FY2026": "118%", "FY2025": "121%", "FY2024": "130%", "FY2023": "135%", "FY2022": "128%"}

metric("CET1 Capital", "£m (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", stock(CET1))], CAPITAL_NOTE)
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", CET1_RATIO)])
metric("Tier 1 Capital", "£m (conv. from USD)", [("Tier 1 capital", stock(TIER1))], CAPITAL_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", TIER1_RATIO)])
metric("Total Capital", "£m (conv. from USD)", [("Total capital", stock(TOTAL_CAPITAL))], CAPITAL_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", TOTAL_RATIO)])
metric("Total RWAs", "£m (conv. from USD)", [("Total risk-weighted exposure amount", stock(RWA))], RWA_NOTE)

# RWA Breakdown - UK OV1 template, native $ million. FY2022-FY2025 sourced directly from each year's own
# contemporaneous Pillar 3 disclosure's OV1 table; FY2026's Pillar 3 document dropped the OV1 template entirely
# (a genuine structural change, confirmed by reading the full document) - derived instead from that document's
# own exposure-class credit risk table, standalone CCR/CVA table, market risk table, and operational risk table,
# which sum to $894.8m, $0.1m below the pre-existing Total RWAs sheet's own $894.9m (rounding across the source
# tables' own 1-decimal precision, not a transcription error here).
RWA_CREDIT = {"FY2026": 813.0, "FY2025": 611.3, "FY2024": 629.0, "FY2023": 666.7, "FY2022": 747.3}
RWA_CCR = {"FY2026": 6.4, "FY2025": 14.5, "FY2024": 0.2, "FY2023": 0.3, "FY2022": 1.8}
RWA_MARKET = {"FY2026": 8.5, "FY2025": 7.7, "FY2024": 11.6, "FY2023": 11.2, "FY2022": 10.3}
RWA_OPERATIONAL = {"FY2026": 66.9, "FY2025": 63.4, "FY2024": 60.0, "FY2023": 51.8, "FY2022": 42.8}
RWA_BREAKDOWN_TOTAL = {"FY2026": 894.8, "FY2025": 697.1, "FY2024": 701.0, "FY2023": 730.1, "FY2022": 802.6}

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", stock(RWA_CREDIT)),
    ("DATA", "Counterparty credit risk (CCR, incl. CVA)", stock(RWA_CCR)),
    ("DATA", "Market risk", stock(RWA_MARKET)),
    ("DATA", "Operational risk", stock(RWA_OPERATIONAL)),
    ("TOTAL", "Total risk-weighted exposure amount", stock(RWA_BREAKDOWN_TOTAL)),
]
bw.add_rwa_breakdown_sheet(
    title="Punjab National Bank (International) Limited — RWA Breakdown",
    subtitle="Entity-level, solo basis. £m converted from the Bank's native US$ million presentation.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\n\nUK OV1 table: FY2025/FY2024 - " + P3_URL["FY2025"] + ", printed p.45; FY2023/FY2022 - "
        + P3_URL["FY2023"] + ", printed p.44. FY2026 derived from " + P3_URL["FY2026"]
        + ", printed pp.14/27-30/33 (credit risk exposure-class table, CCR table, market risk table, operational "
        "risk table) - the FY2026 Pillar 3 document does not include a UK OV1 template (confirmed by reading the "
        "full document), a genuine structural change from FY2022-FY2025's disclosures."
    ),
    first_col_width=60,
    source_height=260,
    unit_suffix=" (£m, conv. from USD)",
)

metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", LEVERAGE)])
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)], LCR_NOTE)
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)])
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "No MREL ratio or MREL target is disclosed in the FY2022-FY2026 Pillar 3 reports or annual reports reviewed; left explicitly undisclosed."},
)

EQ_OPENING_NATIVE = {"FY2026": 211161, "FY2025": 214651, "FY2024": 213328, "FY2023": 208266, "FY2022": 204088}
EQ_OTHER_MOVEMENTS_NATIVE = {"FY2026": -4321, "FY2025": -4636, "FY2024": -4834, "FY2023": -3578, "FY2022": -2367}

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", stock(BS_TOTAL_ASSETS)),
        ("Loans and advances to customers", stock(BS_ASSETS["Loans and advances to customers"])),
        ("Deposits from customers", stock(BS_LIABILITIES["Deposits from customers"])),
        ("Total equity", stock(BS_TOTAL_EQUITY_NATIVE)),
    ],
    balance_sheet_unit="£'000 (conv. from USD)",
    income_statement_totals=[
        ("Profit after tax for the year", flow(PL_PROFIT)),
        ("Total comprehensive income for the year, net of tax", flow(PL_TOTAL_COMPREHENSIVE)),
    ],
    income_statement_unit="£'000 (conv. from USD)",
    equity_changes_totals=[
        ("Opening equity", stock(EQ_OPENING_NATIVE)),
        ("Total comprehensive income for the year", flow(PL_TOTAL_COMPREHENSIVE)),
        ("Other equity movements, net (dividends on AT1 capital)", flow(EQ_OTHER_MOVEMENTS_NATIVE)),
        ("Closing equity", stock(BS_TOTAL_EQUITY_NATIVE)),
    ],
    equity_changes_unit="£'000 (conv. from USD)",
    cash_flow_totals=[
        ("Net cash (used in)/generated from operating activities", flow(OPERATING)),
        ("Net cash (used in)/generated from investing activities", flow(INVESTING)),
        ("Net cash used in financing activities", flow(FINANCING)),
        ("Cash and cash equivalents at end of year", closing),
    ],
    cash_flow_unit="£'000 (conv. from USD)",
    ratios=[("CET1 Ratio", CET1_RATIO), ("Tier 1 Ratio", TIER1_RATIO),
            ("Total Capital Ratio", TOTAL_RATIO), ("Leverage Ratio", LEVERAGE),
            ("LCR", LCR), ("NSFR", NSFR)],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing. See each sheet's source citation. Dollar amounts are converted to GBP; ratios remain as reported.",
)

bw.save("/Users/armaan/code/katalysis/banks/PUNJAB NATIONAL BANK INTERNATIONAL FINANCIALS.xlsx")
