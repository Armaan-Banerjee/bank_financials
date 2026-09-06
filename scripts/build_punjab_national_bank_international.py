import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# NOTE (HD-048, 2026-09-05): this window is intentionally shifted one year later than this
# project's usual FY2021-FY2025 default because FY2022-FY2026 were "the five latest available
# years" at build time (WF-020, 2026-08-28) - PNBIL's FY2026 accounts and Pillar 3 disclosure
# were already published when that ticket ran. FY2014-FY2020 are prepended here per HD-048's
# FY2014 historical-depth cap; FY2021 was subsequently recovered from the Bank's own filings.
YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022",
         "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]
YEAR_LABEL = {y: y for y in YEARS}

BASE = "https://www.pnbint.com/PNBIL/pdf/Financial_Reports/"
AR_URL = {
    "FY2026": BASE + "PNBIL-Annual-Report-2026.pdf",
    "FY2025": BASE + "PNBIL%20Annual%20Report%202025.pdf",
    "FY2024": BASE + "Annual_Report_31-03-2024.pdf",
    "FY2023": BASE + "PNBIL_Annual_Report_2023.pdf",
    "FY2022": BASE + "AnnualReport20220331.pdf",
    "FY2021": BASE + "Annual%20report%20%2031-03-21.pdf",
    "FY2020": BASE + "Annual%20Report%2031-03-20_latest.pdf",
    "FY2019": BASE + "Annual%20Report%2031-03-19.pdf",
    "FY2018": BASE + "Annual%20Report%2031-03-18.pdf",
    "FY2017": BASE + "SIGNED%20ANNUAL%20REPORT-1617.pdf",
    "FY2016": BASE + "Annual%20Report%2031-03-16.pdf",
    "FY2015": BASE + "Annual%20Report%2031.03.2015.pdf",
    "FY2014": BASE + "Annualreport31-03-2014.pdf",
}
P3_URL = {
    "FY2026": BASE + "Basel-III-Pillar-3-Disclosure-31-03-2026.pdf",
    "FY2025": BASE + "Basel%20III%20Pillar%203%20Disclosures%2031-03-2025.pdf",
    "FY2024": BASE + "Basel_III_Pillar_3_Disclosures%2031-03-2024.pdf",
    "FY2023": BASE + "PNBIL%20Pillar%20III%20Disclosures%20Publish%20Version.pdf",
    "FY2022": BASE + "Basel%20III%20Pillar%203%20Disclosures%20%2031-03-2022.pdf",
    "FY2021": BASE + "Basel%20III%20Pillar%203%20Disclosures%20%2031-03-2021.pdf",
    "FY2020": BASE + "Pillar_3_Disclosure_%2031st_March_2020.pdf",
    "FY2019": BASE + "PILLAR%20III%20-%2031.03.2019%20-%20FINAL.pdf",
    "FY2018": BASE + "PILLAR%203%20Disclosures-%2031.03.18.pdf",
    "FY2017": BASE + "Pillar%203%20Disclosures%2031%2003%202017_FINAL.pdf",
    "FY2016": BASE + "Pillar%20III%20disclosures%2031%2003%202016_Revised.pdf",
    "FY2015": BASE + "Pillar%20III%20disclosures%2031%2003%202015.pdf",
    "FY2014": BASE + "Pillar%20III%20disclosures%2031%2003%202014.pdf",
}

# Rates are £1 = US$X from the Bank of England XUDLUSS series.  Flow rates are
# averages over each 1 April-31 March financial year; stocks use the final
# available business-day spot rate at 31 March.  FY2022 opening cash uses the
# 31 March 2021 spot rate because it is shown as a comparative in the FY2022
# accounts.
#
# HD-048 (2026-09-05/06) FX NOTE: FY2013-FY2020 spot/average rates were pulled from the Bank of
# England XUDLUSS series via its CSV export endpoint (bankofengland.co.uk/boeapps/database/
# _iadb-fromshowcolumns.asp), the same underlying series as the FY2021-FY2026 rates above -
# these were transcribed by hand from the BoE's interactive database rather than fetched
# programmatically at build time, but FY2014-FY2020's figures were pulled via the same CSV
# export mechanism for this ticket, so both blocks are the same series. Averages are the simple
# mean of all daily XUDLUSS observations from 1 April to 31 March; spot is the last available
# observation on or before 31 March.
FX_SPOT = {"FY2026": 1.3188, "FY2025": 1.2910, "FY2024": 1.2632,
           "FY2023": 1.2364, "FY2022": 1.3162, "FY2021": 1.3796,
           "FY2020": 1.2403, "FY2019": 1.3030, "FY2018": 1.4033,
           "FY2017": 1.2507, "FY2016": 1.4378, "FY2015": 1.4847,
           "FY2014": 1.6673, "FY2013": 1.5181}
FX_AVG = {"FY2026": 1.3404, "FY2025": 1.2763, "FY2024": 1.2568,
          "FY2023": 1.2045, "FY2022": 1.3662, "FY2021": 1.3193,
          "FY2020": 1.2708, "FY2019": 1.3130, "FY2018": 1.3273,
          "FY2017": 1.3067, "FY2016": 1.5082, "FY2015": 1.6125,
          "FY2014": 1.5900}
PREVIOUS_SPOT = {"FY2022": "FY2021", "FY2021": "FY2020", "FY2023": "FY2022", "FY2024": "FY2023",
                 "FY2025": "FY2024", "FY2026": "FY2025",
                 "FY2020": "FY2019", "FY2019": "FY2018", "FY2018": "FY2017",
                 "FY2017": "FY2016", "FY2016": "FY2015", "FY2015": "FY2014",
                 "FY2014": "FY2013"}


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
    "translation line reconciles the use of different flow and stock rates; it is not a Bank-reported cash-flow line.\n\n"
    "HD-048 (2026-09-05/06) FY2014-FY2020 extension: same BoE XUDLUSS series, same average/spot convention. Rates "
    "(£1 = $X) were FY2014 1.5900 average/1.6673 spot, FY2015 1.6125/1.4847, FY2016 1.5082/1.4378, FY2017 "
    "1.3067/1.2507, FY2018 1.3273/1.4033, FY2019 1.3130/1.3030, FY2020 1.2708/1.2403. The FY2014 opening balance "
    "uses the 31 March 2013 spot rate of 1.5181. FY2021 uses the Bank of England XUDLUSS spot/average rates "
    "1.3796/1.3193 and is now included from the Bank's own 2021 filings."
)

CASH_FLOW_SOURCES = (
    "Sources - Punjab National Bank (International) Limited entity-level Statement of Cash Flows (native unit $'000):\n"
    "FY2026: Annual Report and Accounts 2026, printed p.50 - " + AR_URL["FY2026"] + "\n"
    "FY2025: Annual Report and Accounts 2025, printed p.49 - " + AR_URL["FY2025"] + "\n"
    "FY2024: Annual Report and Accounts 2024, printed p.44 - " + AR_URL["FY2024"] + "\n"
    "FY2023: Annual Report and Accounts 2023, printed p.39 - " + AR_URL["FY2023"] + "\n"
    "FY2022: Annual Report and Accounts 2022, printed p.36 - " + AR_URL["FY2022"] + "\n"
    "FY2021: Annual Report and Accounts 2021, printed pp.24-28 - " + AR_URL["FY2021"] + "\n"
    "FY2020: Annual Report and Accounts 2020, printed p.29 - " + AR_URL["FY2020"] + "\n"
    "FY2019: Annual Report and Accounts 2019, printed p.32 - " + AR_URL["FY2019"] + "\n"
    "FY2018: Annual Report and Accounts 2018, printed p.33 - " + AR_URL["FY2018"] + "\n"
    "FY2017: Annual Report and Accounts 2018's own FY2017 comparative column, printed p.33 - " + AR_URL["FY2018"]
    + " (FY2017's own report is a scanned/photocopied PDF - AR2018's native-text comparative was used for higher "
    "transcription confidence; cross-checked against FY2017's own OCR'd report at " + AR_URL["FY2017"] + ")\n"
    "FY2016: Annual Report and Accounts 2016, printed p.25 - " + AR_URL["FY2016"] + " (OCR'd from a scanned PDF)\n"
    "FY2015: Annual Report and Accounts 2016's own FY2015 comparative column, printed p.25 - " + AR_URL["FY2016"]
    + " (OCR'd from a scanned PDF; cross-checked against FY2015's own report at " + AR_URL["FY2015"] + ")\n"
    "FY2014: Annual Report and Accounts 2014, printed p.21 - " + AR_URL["FY2014"] + " (OCR'd from a scanned PDF; "
    "the Statement of Financial Position on the same page range was additionally verified against a 250dpi page "
    "render, see BS_DISCREPANCY_NOTE-style verification below)\n\n"
    + ENTITY_NOTE + "\n" + FX_NOTE + "\n\n"
    "HD-048 EXCHANGE-EFFECTS NOTE: the Bank's own Statement of Cash Flows discloses a separate 'unrealised "
    "(gain)/loss on exchange rate difference' reconciling line (after the net change in cash, before the closing "
    "balance) only in the FY2017 and FY2018 reports; FY2014-FY2016, FY2019 and FY2020 close exactly from opening + "
    "net change with no such line disclosed that year - a genuine year-to-year presentation difference, not a gap "
    "in this transcription."
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
            f"FY2020: {P3_URL['FY2020']}, printed p.2 (2020 KM1 table, with FY2019 comparative)",
            f"FY2019: {P3_URL['FY2019']}, printed p.2 (2019 KM1 table, with FY2018 comparative)",
            f"FY2018: {P3_URL['FY2018']}, printed pp.11-12/16 (own-basis capital/leverage/liquidity tables; FY2017 comparative also sourced here)",
            f"FY2017: {P3_URL['FY2017']}, printed pp.7/12-13 (own-year capital resources, leverage, LCR/NSFR tables)",
            f"FY2016: {P3_URL['FY2016']}, printed pp.1/4-6 (own-year capital resources, Pillar I RWA, leverage, LCR, NSFR tables; OCR'd from a scanned PDF)",
            f"FY2015: {P3_URL['FY2015']}, printed pp.1/5-6 (own-year capital resources, Pillar I RWA, leverage, NSFR tables; OCR'd from a scanned PDF; LCR not disclosed - see LCR_NOTE)",
            f"FY2014: {P3_URL['FY2014']}, printed pp.1/5-6 (own-year capital resources, Pillar I RWA, leverage, NSFR tables; OCR'd from a scanned PDF; LCR not disclosed - see LCR_NOTE)",
        ])
        + "\n\n" + ENTITY_NOTE + "\n\n"
        "HD-048 METHODOLOGY NOTE (FY2014-FY2020): FY2020-FY2018 use the UK KM1/CA1-style tables broadly comparable "
        "to the modern KM1 template. FY2017-FY2014 predate the KM1 template - their 'Capital Resources' table uses "
        "the CRD IV transitional Core Tier I / Additional Tier I / Tier II structure; where the Bank held no "
        "Additional Tier 1 capital that year (FY2014, FY2015), CET1 capital equals Tier 1 capital exactly and the "
        "CET1 ratio is taken as equal to the disclosed Tier 1 ratio. 'Total Capital to Risk Adequacy Ratio (CRAR)' "
        "is this era's name for the Total capital ratio."
    )


# Native cash-flow figures, $'000.  Each report's own current-year column is
# used; later reports' comparative columns were checked for continuity.
OPERATING = {
    "FY2026": 63882, "FY2025": 3518, "FY2024": -29200,
    "FY2023": 7735, "FY2022": -20687,
    "FY2021": 102557,
    "FY2020": -21456, "FY2019": 31802, "FY2018": -334192, "FY2017": 158164,
    "FY2016": 81196, "FY2015": -55376, "FY2014": 5386,
}
INVESTING = {
    "FY2026": -28192, "FY2025": -7088, "FY2024": 22199,
    "FY2023": -9217, "FY2022": -48112,
    "FY2021": -9878,
    "FY2020": 455, "FY2019": -2387, "FY2018": -40085, "FY2017": -8449,
    "FY2016": 103, "FY2015": 1945, "FY2014": 1949,
}
FINANCING = {
    "FY2026": -15391, "FY2025": -15689, "FY2024": -5568,
    "FY2023": -4493, "FY2022": -3305,
    "FY2021": -3490,
    "FY2020": -4222, "FY2019": -3432, "FY2018": 17072, "FY2017": 100000,
    "FY2016": 8864, "FY2015": 8918, "FY2014": 53889,
}
NET_CHANGE = {
    "FY2026": 23169, "FY2025": -17279, "FY2024": -10789,
    "FY2023": -5975, "FY2022": -72104,
    "FY2021": 89190,
    "FY2020": -25223, "FY2019": 25985, "FY2018": -357205, "FY2017": 249715,
    "FY2016": 90163, "FY2015": -44513, "FY2014": 61224,
}
EXCHANGE = {"FY2026": 2870, "FY2025": 1980, "FY2024": 1780,
            "FY2023": 998, "FY2022": 582,
            # Disclosed by the Bank only in FY2017/FY2018 - see the HD-048 EXCHANGE-EFFECTS NOTE
            # in CASH_FLOW_SOURCES; other years reconcile exactly opening + net change = closing
            # with no separate line disclosed, so the key is left absent per this project's
            # "missing years are blank dict keys, not zeros" convention.
            "FY2018": -1437, "FY2017": 90}
OPENING_USD = {"FY2026": 116753, "FY2025": 134032, "FY2024": 144821,
               "FY2023": 149798, "FY2022": 221320,
               "FY2021": 132130,
               "FY2020": 157353, "FY2019": 131368, "FY2018": 490010,
               "FY2017": 240205, "FY2016": 150042, "FY2015": 194555,
               "FY2014": 133331}
CLOSING_USD = {"FY2026": 139922, "FY2025": 116753, "FY2024": 134032,
               "FY2023": 144821, "FY2022": 149798,
               "FY2021": 221320,
               "FY2020": 132130, "FY2019": 157353, "FY2018": 131368,
               "FY2017": 490010, "FY2016": 240205, "FY2015": 150042,
               "FY2014": 194555}

opening = {
    y: round(OPENING_USD[y] / FX_SPOT[PREVIOUS_SPOT[y]], 1) for y in YEARS
}
closing = stock(CLOSING_USD)
_exchange_flow = flow(EXCHANGE)
translation = {
    y: round(closing[y] - opening[y] - flow(NET_CHANGE)[y] - _exchange_flow.get(y, 0), 1)
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
    "FY2022: Annual Report and Accounts 2022, printed pp.33-35 - " + AR_URL["FY2022"] + "\n"
    "FY2020: Annual Report and Accounts 2020, printed pp.26-28 - " + AR_URL["FY2020"] + "\n"
    "FY2019: Annual Report and Accounts 2019, printed pp.29-31 - " + AR_URL["FY2019"] + "\n"
    "FY2018: Annual Report and Accounts 2018, printed pp.29-31 - " + AR_URL["FY2018"] + "\n"
    "FY2017: Annual Report and Accounts 2018's own FY2017 comparative columns, printed pp.29-32 - " + AR_URL["FY2018"]
    + " (native-text PDF; used in preference to FY2017's own scanned/OCR'd report at " + AR_URL["FY2017"] + " for "
    "higher transcription confidence, cross-checked against it)\n"
    "FY2016: Annual Report and Accounts 2016, printed pp.20-25 - " + AR_URL["FY2016"] + " (OCR'd from a scanned "
    "PDF; each total independently verified by summing the disclosed line items)\n"
    "FY2015: Annual Report and Accounts 2015, printed pp.18-21 - " + AR_URL["FY2015"] + " (OCR'd from a scanned "
    "PDF; some liability/equity lines not shown on the FY2015 report's own face were taken from Annual Report and "
    "Accounts 2016's FY2015 comparative column and verified to sum exactly to FY2015's own disclosed Total "
    "liabilities of $1,690,610k)\n"
    "FY2014: Annual Report and Accounts 2014, printed p.17 - " + AR_URL["FY2014"] + " (OCR'd from a scanned PDF; "
    "the Statement of Financial Position was additionally verified against a 250dpi rendered page image "
    "line-by-line because of poor OCR quality on this particular scan)\n\n"
    + ENTITY_NOTE + "\n" + FX_NOTE + "\n\n"
    "GBP CONVERSION NOTE (Balance Sheet/Equity balances, Profit & Loss/Equity movements): balance-date figures "
    "(Balance Sheet lines, equity opening/closing balances) use the 31 March spot rate of that balance date; "
    "period figures (Profit & Loss lines, equity movement rows) use the financial year's average rate. Because "
    "these are two different rates, a computed 'GBP translation adjustment' row is shown on the equity sheet for "
    "each year to keep the GBP columns arithmetically closed - it is not a Bank-reported line.\n\n"
    "HD-048 IAS 39-TO-IFRS 9 CLASSIFICATION BRIDGE NOTE: FY2014-FY2018 predate the Bank's IFRS 9 adoption (first "
    "applied FY2019 - see the Statement of Changes in Equity's 'IFRS 9 adoption' transition row). Those years' "
    "IAS 39 categories are mapped onto this sheet's IFRS 9-era row labels by nearest economic equivalent: "
    "'Investment securities - held for trading' is shown as 'Financial assets at fair value through profit or "
    "loss'; 'Investment securities - available for sale' is shown as 'Financial assets at fair value through "
    "other comprehensive income'; 'Investment securities - held to maturity' is shown as 'Investment securities "
    "at amortised cost'. Right of use lease assets/Lease liability are blank pre-FY2020 because IFRS 16 was not "
    "yet adopted. 'Deferred tax liabilities' and 'Current tax assets' are additional line items only disclosed "
    "in some FY2014-FY2016 years and are shown as their own rows, blank elsewhere."
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
    "Cash and balances with banks": {"FY2026": 139922, "FY2025": 116753, "FY2024": 134032, "FY2023": 144821, "FY2022": 149798, "FY2021": 221320,
                                      "FY2020": 132130, "FY2019": 157353, "FY2018": 131368, "FY2017": 490010,
                                      "FY2016": 240205, "FY2015": 150042, "FY2014": 194555},
    "Financial assets at fair value through profit or loss": {"FY2026": 1014, "FY2025": 964, "FY2024": 3029, "FY2023": 0, "FY2022": 10001, "FY2021": 10071,
                                      "FY2020": 33585, "FY2019": 24232, "FY2018": 32588, "FY2017": 59968,
                                      "FY2016": 49727, "FY2015": 81667, "FY2014": 62113},
    "Derivative financial instruments (asset)": {"FY2026": 2925, "FY2025": 156, "FY2024": 14, "FY2023": 7, "FY2022": 1064, "FY2021": 1871,
                                      "FY2020": 3014, "FY2019": 2532, "FY2018": 11932, "FY2017": 4319,
                                      "FY2016": 5994, "FY2015": 3626, "FY2014": 1973},
    "Loans and advances to banks": {"FY2026": 1453, "FY2025": 1352, "FY2024": 10496, "FY2023": 836, "FY2022": 700, "FY2021": 30478,
                                      "FY2020": 125044, "FY2019": 155671, "FY2018": 335509, "FY2017": 205154,
                                      "FY2016": 310453, "FY2015": 338882, "FY2014": 299720},
    "Loans and advances to customers": {"FY2026": 1131159, "FY2025": 903981, "FY2024": 772119, "FY2023": 748698, "FY2022": 791237, "FY2021": 690599,
                                      "FY2020": 566366, "FY2019": 602733, "FY2018": 568317, "FY2017": 605202,
                                      "FY2016": 1071990, "FY2015": 1196008, "FY2014": 1170545},
    "Investment securities at amortised cost": {"FY2026": 63199, "FY2025": 75947, "FY2024": 65117, "FY2023": 108096, "FY2022": 89114, "FY2021": 58332,
                                      "FY2020": 49467, "FY2019": 50648, "FY2018": 48624, "FY2017": 8936,
                                      "FY2016": 1171, "FY2015": 1568, "FY2014": 4839},
    "Financial assets at amortised cost (subtotal, as disclosed FY2024-FY2026)": {"FY2026": 1195811, "FY2025": 981280, "FY2024": 847732},
    "Financial assets at fair value through other comprehensive income": {"FY2026": 110830, "FY2025": 71606, "FY2024": 72866, "FY2023": 55263, "FY2022": 54753, "FY2021": 39311,
                                      "FY2020": 35651, "FY2019": 42588, "FY2018": 46547, "FY2017": 53936,
                                      "FY2016": 122080, "FY2015": 120760, "FY2014": 166328},
    "Right of use lease assets": {"FY2026": 4394, "FY2025": 2946, "FY2024": 3685, "FY2023": 4395, "FY2022": 3073, "FY2021": 4066, "FY2020": 4383},
    "Property, plant and equipment": {"FY2026": 1034, "FY2025": 237, "FY2024": 287, "FY2023": 311, "FY2022": 391, "FY2021": 493,
                                      "FY2020": 460, "FY2019": 534, "FY2018": 694, "FY2017": 962,
                                      "FY2016": 1526, "FY2015": 2071, "FY2014": 1472},
    "Intangible assets": {"FY2026": 485, "FY2025": 126, "FY2024": 180, "FY2023": 230, "FY2022": 589, "FY2021": 962,
                                      "FY2020": 539, "FY2019": 362, "FY2018": 504, "FY2017": 556,
                                      "FY2016": 170, "FY2015": 136, "FY2014": 168},
    "Deferred tax assets": {"FY2026": 24463, "FY2025": 24441, "FY2024": 24862, "FY2023": 24990, "FY2022": 25155, "FY2021": 24657,
                                      "FY2020": 25023, "FY2019": 24301, "FY2018": 25310, "FY2017": 25802,
                                      "FY2016": 3836, "FY2014": 20},
    "Current tax assets": {"FY2016": 3891},
    "Prepayments and other receivables": {"FY2026": 1575, "FY2025": 1117, "FY2024": 591, "FY2023": 533, "FY2022": 384, "FY2021": 587,
                                      "FY2020": 469, "FY2019": 636, "FY2018": 627, "FY2017": 524,
                                      "FY2016": 696, "FY2015": 3977, "FY2014": 925},
}
BS_TOTAL_ASSETS = {"FY2026": 1482453, "FY2025": 1199626, "FY2024": 1087278, "FY2023": 1088180, "FY2022": 1126259, "FY2021": 1082747,
                    "FY2020": 976131, "FY2019": 1061590, "FY2018": 1202020, "FY2017": 1455369,
                    "FY2016": 1811739, "FY2015": 1898737, "FY2014": 1902658}

BS_LIABILITIES = {
    "Deposits from banks": {"FY2026": 50355, "FY2025": 2311, "FY2024": 3292, "FY2023": 1967, "FY2022": 1106, "FY2021": 865,
                                      "FY2020": 16126, "FY2019": 56464, "FY2018": 54342, "FY2017": 73692,
                                      "FY2016": 176964, "FY2015": 135260, "FY2014": 280764},
    "Deposits from customers": {"FY2026": 1184925, "FY2025": 916442, "FY2024": 811182, "FY2023": 816636, "FY2022": 858073, "FY2021": 819493,
                                      "FY2020": 685120, "FY2019": 731971, "FY2018": 876208, "FY2017": 1134852,
                                      "FY2016": 1358109, "FY2015": 1454943, "FY2014": 1361155},
    "Derivative financial instruments (liability)": {"FY2026": 16, "FY2025": 1471, "FY2024": 159, "FY2023": 155, "FY2022": 295, "FY2021": 25,
                                      "FY2020": 1458, "FY2019": 1262, "FY2018": 1295, "FY2017": 455,
                                      "FY2016": 14944, "FY2015": 21668, "FY2014": 202},
    "Current tax liability": {"FY2023": 0, "FY2022": 0,
                                      "FY2019": 316, "FY2016": 0, "FY2015": 2387, "FY2014": -254},
    "Deferred tax liabilities": {"FY2016": 57, "FY2015": 90},
    "Repurchase agreement - non trading": {"FY2026": 0, "FY2025": 20868},
    "Lease liability": {"FY2026": 4603, "FY2025": 3173, "FY2024": 3870, "FY2023": 4522, "FY2022": 3205, "FY2021": 4181, "FY2020": 4443},
    "Other liabilities": {"FY2026": 2182, "FY2025": 3092, "FY2024": 2639, "FY2023": 1572, "FY2022": 5314, "FY2021": 4095,
                                      "FY2020": 3399, "FY2019": 4708, "FY2018": 6553, "FY2017": 4513,
                                      "FY2016": 8034, "FY2015": 11262, "FY2014": 11460},
    "Subordinated bonds and other borrowed funds": {"FY2026": 30997, "FY2025": 41108, "FY2024": 51252, "FY2023": 50000, "FY2022": 50000,
                                      "FY2020": 50000, "FY2019": 50000, "FY2018": 50000, "FY2017": 50000,
                                      "FY2016": 75000, "FY2015": 65000, "FY2014": 55000},
}
BS_TOTAL_LIABILITIES = {"FY2026": 1273078, "FY2025": 988465, "FY2024": 872394, "FY2023": 874852, "FY2022": 917993, "FY2021": 878659,
                         "FY2020": 760546, "FY2019": 844721, "FY2018": 988398, "FY2017": 1263512,
                         "FY2016": 1633108, "FY2015": 1690610, "FY2014": 1708327}

BS_EQUITY_NATIVE = {
    "Share capital": {"FY2026": 319631, "FY2025": 319631, "FY2024": 319631, "FY2023": 319631, "FY2022": 319631, "FY2021": 319631,
                                      "FY2020": 319631, "FY2019": 319631, "FY2018": 319631, "FY2017": 299631,
                                      "FY2016": 174631, "FY2015": 174631, "FY2014": 174631},
    "Fair value reserve": {"FY2026": -123, "FY2025": 279, "FY2024": -807, "FY2023": -986, "FY2022": -1293, "FY2021": 68,
                                      "FY2020": -1256, "FY2019": -608, "FY2018": -1157, "FY2017": -34,
                                      "FY2016": 390, "FY2015": 1751, "FY2014": -5006},
    "Retained earnings": {"FY2026": -110133, "FY2025": -108749, "FY2024": -103940, "FY2023": -105317, "FY2022": -110072, "FY2021": -115611,
                                      "FY2020": -102790, "FY2019": -102154, "FY2018": -104852, "FY2017": -107740,
                                      "FY2016": 3610, "FY2015": 31745, "FY2014": 24706},
}
BS_TOTAL_EQUITY_NATIVE = {"FY2026": 209375, "FY2025": 211161, "FY2024": 214884, "FY2023": 213328, "FY2022": 208266, "FY2021": 204088,
                           "FY2020": 215585, "FY2019": 216869, "FY2018": 213622, "FY2017": 191857,
                           "FY2016": 178631, "FY2015": 208127, "FY2014": 194331}


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
PL_PROFIT = {"FY2026": 2937, "FY2025": 750, "FY2024": 6211, "FY2023": 8333, "FY2022": 7906, "FY2021": -10234,
             "FY2020": 2726, "FY2019": 8318, "FY2018": 5893, "FY2017": -111328,
             "FY2016": -27225, "FY2015": 8121, "FY2014": 6990}
PL_OCI_OLD = {  # FY2021-FY2024 presentation
    "FVOCI gains/(losses) arising during the year": {"FY2024": 248, "FY2023": -79, "FY2022": -2066, "FY2021": 1534},
    "Tax credit/(charge) relating to change in fair value": {"FY2024": -62, "FY2023": -9, "FY2022": 496, "FY2021": -281},
    "Reclassification adjustment transferred to P&L": {"FY2024": -7, "FY2023": 395, "FY2022": 209, "FY2021": 71},
}
PL_OCI_NEW = {  # FY2025-FY2026 presentation
    "Fair value gains/(losses) transferred to income statement on disposal": {"FY2026": -613, "FY2025": 258},
    "Fair value gains on Investment Securities - FVOCI": {"FY2026": 77, "FY2025": 268},
    "Income tax on other comprehensive income items": {"FY2026": 134, "FY2025": -130},
}
# HD-048: FY2014-FY2020 presentation - IAS 39 available-for-sale gains/losses (pre-IFRS 9 adoption in FY2019;
# the FY2019/FY2020 columns still use "Investment securities - FVTOCI" wording after the IFRS 9 relabelling but
# the OCI mechanics are unchanged from the AFS era, so all seven years are shown on this one basis).
PL_OCI_AFS = {
    "Net change in fair value on AFS/FVTOCI investments (gross)": {
        "FY2020": -794, "FY2019": 513, "FY2018": -1122, "FY2017": -679,
        "FY2016": -1612, "FY2015": 5818, "FY2014": -6280},
    "Tax (charge)/credit relating to fair value change": {
        "FY2020": 134, "FY2019": -66, "FY2018": 237, "FY2017": -77,
        "FY2016": 322, "FY2015": -1222, "FY2014": 1444},
    "Reclassification adjustment transferred to profit and loss": {
        "FY2020": 12, "FY2019": 102, "FY2018": -238, "FY2017": 332,
        "FY2016": -71, "FY2015": 2161, "FY2014": -295},
}
PL_OCI_TOTAL = {"FY2026": -402, "FY2025": 396, "FY2024": 179, "FY2023": 307, "FY2022": -1361, "FY2021": 1324,
                "FY2020": -648, "FY2019": 549, "FY2018": -1123, "FY2017": -424,
                "FY2016": -1361, "FY2015": 6757, "FY2014": -5131}
PL_TOTAL_COMPREHENSIVE = {"FY2026": 2535, "FY2025": 1146, "FY2024": 6390, "FY2023": 8640, "FY2022": 6545, "FY2021": -8910,
                           "FY2020": 2078, "FY2019": 8867, "FY2018": 4770, "FY2017": -111752,
                           "FY2016": -28586, "FY2015": 14878, "FY2014": 1859}

income_statement_rows = (
    [("SECTION", "Income", {}), ("TOTAL", "Profit after tax for the year", flow(PL_PROFIT))]
    + [("SECTION", "Other comprehensive income - FY2022-FY2024 presentation", {})]
    + [("DATA", label, flow(values)) for label, values in PL_OCI_OLD.items()]
    + [("SECTION", "Other comprehensive income - FY2025-FY2026 presentation", {})]
    + [("DATA", label, flow(values)) for label, values in PL_OCI_NEW.items()]
    + [("SECTION", "Other comprehensive income - FY2014-FY2020 presentation (IAS 39 available-for-sale)", {})]
    + [("DATA", label, flow(values)) for label, values in PL_OCI_AFS.items()]
    + [("TOTAL", "Other comprehensive income for the year, net of tax", flow(PL_OCI_TOTAL))]
    + [("TOTAL", "Total comprehensive income for the year, net of tax", flow(PL_TOTAL_COMPREHENSIVE))]
)

bw.add_income_statement_sheet(
    title="Punjab National Bank (International) Limited — Profit & Loss",
    subtitle="Entity-level Statement of Comprehensive Income, £'000 converted from the Bank's native US$'000 "
             "presentation. OCI's underlying line-item structure changed between FY2024 and FY2025, and again "
             "predates IFRS 9 for FY2014-FY2020 - each era shown on its own contemporaneous basis; only Profit "
             "after tax and the two Total rows are directly comparable across all 13 years.",
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
# HD-048 (2026-09-05/06): FY2014-FY2020 prepended, oldest first. Equity ladder confirmed exactly in native
# USD terms across all seven years by summing each year's own disclosed movements against its own disclosed
# opening/closing balances (see the Session/Progress notes accompanying this build for the reconciliation).
# FY2014
equity_rows.append(("TOTAL", "Balance at 1 April 2013 (FY2014 opening)", eq_stock(124631, 125, 18827, 143583, "FY2013")))
equity_rows.append(("DATA", "Profit for the year", eq_flow(None, None, 6990, 6990, "FY2014")))
equity_rows.append(("DATA", "Net change in fair value of AFS investments", eq_flow(None, -4836, None, -4836, "FY2014")))
equity_rows.append(("DATA", "Net amount transferred to profit and loss", eq_flow(None, -295, None, -295, "FY2014")))
equity_rows.append(("DATA", "Issue of share capital", eq_flow(50000, None, None, 50000, "FY2014")))
equity_rows.append(("DATA", "Dividend on perpetual Tier II capital", eq_flow(None, None, -1111, -1111, "FY2014")))
equity_rows.append(("DATA", "GBP translation adjustment (this workbook's conversion line)", (None, None, None, None)))
equity_rows.append(("TOTAL", "Balance at 31 March 2014 (FY2014 closing)", eq_stock(174631, -5006, 24706, 194331, "FY2014")))
# FY2015
equity_rows.append(("DATA", "Profit for the year", eq_flow(None, None, 8121, 8121, "FY2015")))
equity_rows.append(("DATA", "Net change in fair value of AFS investments", eq_flow(None, 4596, None, 4596, "FY2015")))
equity_rows.append(("DATA", "Net amount transferred to profit and loss", eq_flow(None, 2161, None, 2161, "FY2015")))
equity_rows.append(("DATA", "Dividend on perpetual Tier II capital", eq_flow(None, None, -1082, -1082, "FY2015")))
equity_rows.append(("DATA", "GBP translation adjustment (this workbook's conversion line)", (None, None, None, None)))
equity_rows.append(("TOTAL", "Balance at 31 March 2015 (FY2015 closing)", eq_stock(174631, 1751, 31745, 208127, "FY2015")))
# FY2016
equity_rows.append(("DATA", "Loss for the year", eq_flow(None, None, -27225, -27225, "FY2016")))
equity_rows.append(("DATA", "Net change in fair value of AFS investments", eq_flow(None, -1290, None, -1290, "FY2016")))
equity_rows.append(("DATA", "Net amount transferred to profit and loss", eq_flow(None, -71, None, -71, "FY2016")))
equity_rows.append(("DATA", "Dividend on perpetual Tier II capital", eq_flow(None, None, -1137, -1137, "FY2016")))
equity_rows.append(("DATA", "Deferred tax benefit", eq_flow(None, None, 227, 227, "FY2016")))
equity_rows.append(("DATA", "GBP translation adjustment (this workbook's conversion line)", (None, None, None, None)))
equity_rows.append(("TOTAL", "Balance at 31 March 2016 (FY2016 closing)", eq_stock(174631, 390, 3610, 178631, "FY2016")))
# FY2017
equity_rows.append(("DATA", "Loss for the year", eq_flow(None, None, -111328, -111328, "FY2017")))
equity_rows.append(("DATA", "Net change in fair value of AFS investments", eq_flow(None, -424, None, -424, "FY2017")))
equity_rows.append(("DATA", "Tax credit arising on AFS reserve movement (Bank's own footnoted item, posted to retained earnings)",
                     eq_flow(None, None, -22, -22, "FY2017")))
equity_rows.append(("DATA", "Issue of share capital", eq_flow(125000, None, None, 125000, "FY2017")))
equity_rows.append(("DATA", "GBP translation adjustment (this workbook's conversion line)", (None, None, None, None)))
equity_rows.append(("TOTAL", "Balance at 31 March 2017 (FY2017 closing)", eq_stock(299631, -34, -107740, 191857, "FY2017")))
# FY2018 (with a genuine, Bank-disclosed prior period adjustment at the start of the year)
equity_rows.append(("DATA", "Prior period adjustment (tax credit arising on AFS reserve movement)",
                     eq_flow(None, None, -77, -77, "FY2017")))
equity_rows.append(("TOTAL", "Balance at 1 April 2017, as restated (FY2018 opening)", eq_stock(299631, -34, -107817, 191780, "FY2017")))
equity_rows.append(("DATA", "Profit for the year", eq_flow(None, None, 5893, 5893, "FY2018")))
equity_rows.append(("DATA", "Net change in fair value of AFS investments", eq_flow(None, -885, None, -885, "FY2018")))
equity_rows.append(("DATA", "Net amount transferred to profit and loss", eq_flow(None, -238, None, -238, "FY2018")))
equity_rows.append(("DATA", "Issue of share capital", eq_flow(20000, None, None, 20000, "FY2018")))
equity_rows.append(("DATA", "Dividend on perpetual additional Tier I capital", eq_flow(None, None, -2928, -2928, "FY2018")))
equity_rows.append(("DATA", "GBP translation adjustment (this workbook's conversion line)", (None, None, None, None)))
equity_rows.append(("TOTAL", "Balance at 31 March 2018 (FY2018 closing)", eq_stock(319631, -1157, -104852, 213622, "FY2018")))
# FY2019 (IFRS 9 first adopted at 1 April 2018 - see the ENTITY_NOTE-adjacent commentary elsewhere in this file)
equity_rows.append(("DATA", "IFRS 9 adoption (retained earnings transition adjustment)",
                     eq_flow(None, None, -2584, -2584, "FY2018")))
equity_rows.append(("TOTAL", "Balance at 1 April 2018, as adjusted for IFRS 9 adoption (FY2019 opening)", eq_stock(319631, -1157, -107436, 211038, "FY2018")))
equity_rows.append(("DATA", "Profit for the year", eq_flow(None, None, 8318, 8318, "FY2019")))
equity_rows.append(("DATA", "Net change in fair value of Investment securities - FVTOCI", eq_flow(None, 447, None, 447, "FY2019")))
equity_rows.append(("DATA", "Net amount transferred to profit and loss", eq_flow(None, 102, None, 102, "FY2019")))
equity_rows.append(("DATA", "Dividend on perpetual additional Tier I capital", eq_flow(None, None, -3432, -3432, "FY2019")))
equity_rows.append(("DATA", "IFRS 9 deferred tax transitional adjustment", eq_flow(None, None, 396, 396, "FY2019")))
equity_rows.append(("DATA", "GBP translation adjustment (this workbook's conversion line)", (None, None, None, None)))
equity_rows.append(("TOTAL", "Balance at 31 March 2019 (FY2019 closing)", eq_stock(319631, -608, -102154, 216869, "FY2019")))
# FY2020
equity_rows.append(("DATA", "Profit for the year", eq_flow(None, None, 2726, 2726, "FY2020")))
equity_rows.append(("DATA", "Net change in fair value of Investment securities - FVTOCI", eq_flow(None, -660, None, -660, "FY2020")))
equity_rows.append(("DATA", "Net amount transferred to Profit & Loss", eq_flow(None, 12, None, 12, "FY2020")))
equity_rows.append(("DATA", "Dividend on additional Tier 1 capital", eq_flow(None, None, -3362, -3362, "FY2020")))
equity_rows.append(("DATA", "GBP translation adjustment (this workbook's conversion line)", (None, None, None, None)))
equity_rows.append(("TOTAL", "Balance at 31 March 2020 (FY2020 closing)", eq_stock(319631, -1256, -102790, 215585, "FY2020")))
# FY2021 (recovered from the Bank's own annual report, printed p.27).
equity_rows.append(("DATA", "Loss for the year", eq_flow(None, None, -10234, -10234, "FY2021")))
equity_rows.append(("DATA", "Net change in fair value of Investment securities - FVOCI", eq_flow(None, 1253, None, 1253, "FY2021")))
equity_rows.append(("DATA", "Net amount transferred to Profit & Loss", eq_flow(None, 71, None, 71, "FY2021")))
equity_rows.append(("DATA", "Dividend on additional Tier 1 capital", eq_flow(None, None, -2587, -2587, "FY2021")))
equity_rows.append(("DATA", "GBP translation adjustment (this workbook's conversion line)", (None, None, None, None)))
equity_rows.append(("TOTAL", "Balance at 31 March 2021 (FY2021 closing)", eq_stock(319631, 68, -115611, 204088, "FY2021")))
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
# HD-048 (2026-09-05/06): rewritten to scan for TOTAL-row boundaries generically (rather than hardcoded index
# tuples) because prepending FY2014-FY2020 - some with extra prior-period-adjustment/IFRS 9 transition rows
# between TOTAL rows - would otherwise require re-deriving every index by hand. Each run of DATA rows between
# two consecutive TOTAL rows is summed; the LAST DATA row in that run (the GBP translation placeholder, by
# construction above) is overwritten with whatever value keeps the block arithmetically closed.
_total_indices = [i for i, row in enumerate(equity_rows) if row[0] == "TOTAL"]
for opening_idx, closing_idx in zip(_total_indices, _total_indices[1:]):
    # Only overwrite when the last row before the closing TOTAL is actually the GBP translation
    # placeholder - some blocks (the FY2018 prior-period restatement, the FY2019 IFRS 9 transition) are a
    # single real bridging DATA row with no placeholder, and must be left exactly as transcribed.
    if "GBP translation adjustment" not in equity_rows[closing_idx - 1][1]:
        continue
    _eq_opening = equity_rows[opening_idx][2]
    _eq_closing = equity_rows[closing_idx][2]
    movement_sum = [0.0, 0.0, 0.0, 0.0]
    for i in range(opening_idx + 1, closing_idx):
        for ci, v in enumerate(equity_rows[i][2]):
            if v is not None:
                movement_sum[ci] += v
    translation = tuple(
        round(_eq_closing[ci] - _eq_opening[ci] - movement_sum[ci], 1) if _eq_closing[ci] is not None and _eq_opening[ci] is not None else None
        for ci in range(4)
    )
    equity_rows[closing_idx - 1] = ("DATA", equity_rows[closing_idx - 1][1], translation)

bw.add_equity_changes_sheet(
    title="Punjab National Bank (International) Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, entity-level, £'000 converted from the Bank's native "
              "US$'000 presentation. Equity ladder confirmed exactly in native USD terms across all 13 years - the "
              "bridging rows (FY2018's prior period adjustment, FY2019's IFRS 9 transition, and AR2025's own Note "
              "28/Note 35 restatement) are genuine, Bank-disclosed items, not errors. FY2021 is intentionally "
              "absent (see this file's YEARS comment), so the 1 April 2021 opening balance does not equal the "
              "FY2020 closing balance shown above it. GBP translation-adjustment rows arise only from converting "
              "a USD ladder using two different point-in-time/average rates - see the Balance Sheet sheet's GBP "
              "conversion note.",
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
    "Stage 1": {"FY2026": 1093759, "FY2025": 883431, "FY2024": 718452, "FY2023": 786625, "FY2022": 723702,
                "FY2020": 546951, "FY2019": 680867},
    "Stage 2": {"FY2026": 62543, "FY2025": 39431, "FY2024": 34493, "FY2023": 362, "FY2022": 40577,
                "FY2020": 57217, "FY2019": 86509},
    "Stage 3": {"FY2026": 95862, "FY2025": 129209, "FY2024": 255526, "FY2023": 284217, "FY2022": 308877,
                "FY2020": 371763, "FY2019": 406259},
}
AQ_GROSS_TOTAL = {"FY2026": 1252164, "FY2025": 1051071, "FY2024": 1008471, "FY2023": 1071204, "FY2022": 1073156,
                   "FY2020": 975931, "FY2019": 1173635}
AQ_IMPAIR = {
    "Stage 1": {"FY2026": 667, "FY2025": 521, "FY2024": 506, "FY2023": 3068, "FY2022": 1747,
                "FY2020": 2085, "FY2019": 3130},
    "Stage 2": {"FY2026": 20, "FY2025": 10, "FY2024": 2, "FY2023": 1, "FY2022": 147,
                "FY2020": 501, "FY2019": 962},
    "Stage 3": {"FY2026": 55666, "FY2025": 70262, "FY2024": 160233, "FY2023": 176961, "FY2022": 193340,
                "FY2020": 240273, "FY2019": 262067},
}
AQ_IMPAIR_TOTAL = {"FY2026": 56353, "FY2025": 70793, "FY2024": 160741, "FY2023": 180030, "FY2022": 195234,
                    "FY2020": 242859, "FY2019": 266159}
AQ_NET = {
    "Stage 1": {"FY2026": 1093092, "FY2025": 882911, "FY2024": 717947, "FY2023": 783557, "FY2022": 721955,
                "FY2020": 544866, "FY2019": 677737},
    "Stage 2": {"FY2026": 62523, "FY2025": 39422, "FY2024": 34491, "FY2023": 361, "FY2022": 40430,
                "FY2020": 56716, "FY2019": 85546},
    "Stage 3": {"FY2026": 40196, "FY2025": 58947, "FY2024": 95293, "FY2023": 107256, "FY2022": 115537,
                "FY2020": 131490, "FY2019": 144192},
}
AQ_NET_TOTAL = {"FY2026": 1195811, "FY2025": 981280, "FY2024": 847731, "FY2023": 891174, "FY2022": 877922,
                "FY2020": 733072, "FY2019": 907475}
AQ_NPL_RATIO = {y: f"{AQ_GROSS['Stage 3'][y] / AQ_GROSS_TOTAL[y] * 100:.2f}%" for y in AQ_GROSS_TOTAL}
AQ_COVERAGE_RATIO = {y: f"{AQ_IMPAIR_TOTAL[y] / AQ_GROSS_TOTAL[y] * 100:.2f}%" for y in AQ_GROSS_TOTAL}

# HD-048 (2026-09-05/06): FY2014-FY2018 predate IFRS 9 (first adopted FY2019 - see the Statement of Changes in
# Equity's transition row) and disclose an IAS 39 incurred-loss impairment model instead of an IFRS 9 stage
# split. This section covers Loans and advances to customers only (the Bank's own disclosure for this era does
# not extend the same combined-with-banks-and-amortised-cost-securities scope used by the IFRS 9 Stage table
# above), so the two sections are not directly comparable in scope, only in broad direction.
AQ_AFS_GROSS_LOANS = {"FY2018": 839762, "FY2017": 871680, "FY2016": 1186240, "FY2015": 1238412, "FY2014": 1205208}
AQ_AFS_SPECIFIC = {"FY2018": 267880, "FY2017": 258560, "FY2016": 108620, "FY2015": 35504, "FY2014": 31155}
AQ_AFS_COLLECTIVE = {"FY2018": 3560, "FY2017": 4720, "FY2016": 5630, "FY2015": 6900, "FY2014": 3508}
AQ_AFS_TOTAL_IMPAIR = {"FY2018": 271445, "FY2017": 266478, "FY2016": 114250, "FY2015": 42404, "FY2014": 34663}
AQ_AFS_NET_LOANS = {"FY2018": 568317, "FY2017": 605202, "FY2016": 1071990, "FY2015": 1196008, "FY2014": 1170545}
AQ_AFS_GROSS_IMPAIRED = {"FY2018": 318470, "FY2017": 299390, "FY2016": 144990, "FY2015": 82530, "FY2014": 66793}
AQ_AFS_NPL_RATIO = {y: f"{AQ_AFS_GROSS_IMPAIRED[y] / AQ_AFS_GROSS_LOANS[y] * 100:.2f}%" for y in AQ_AFS_GROSS_LOANS}
AQ_AFS_COVERAGE_RATIO = {y: f"{AQ_AFS_TOTAL_IMPAIR[y] / AQ_AFS_GROSS_LOANS[y] * 100:.2f}%" for y in AQ_AFS_GROSS_LOANS}

asset_quality_rows = (
    [("SECTION", "Gross carrying amount, by IFRS 9 stage (loans, banks, and investment securities at amortised cost) - FY2019-FY2026", {})]
    + [("DATA", f"Stage {s.split()[-1]} gross carrying amount", stock(AQ_GROSS[s])) for s in ["Stage 1", "Stage 2", "Stage 3"]]
    + [("TOTAL", "Total gross carrying amount", stock(AQ_GROSS_TOTAL))]
    + [("SECTION", "Impairment allowance, by IFRS 9 stage - FY2019-FY2026", {})]
    + [("DATA", f"Stage {s.split()[-1]} impairment allowance", stock(AQ_IMPAIR[s])) for s in ["Stage 1", "Stage 2", "Stage 3"]]
    + [("TOTAL", "Total impairment allowance", stock(AQ_IMPAIR_TOTAL))]
    + [("SECTION", "Net carrying amount, by IFRS 9 stage - FY2019-FY2026", {})]
    + [("DATA", f"Stage {s.split()[-1]} net carrying amount", stock(AQ_NET[s])) for s in ["Stage 1", "Stage 2", "Stage 3"]]
    + [("TOTAL", "Total net carrying amount", stock(AQ_NET_TOTAL))]
    + [("SECTION", "Asset quality ratios (derived) - FY2019-FY2026", {})]
    + [("DATA", "Stage 3 as % of total gross carrying amount (NPL ratio)", AQ_NPL_RATIO)]
    + [("DATA", "Total impairment allowance as % of total gross carrying amount (coverage)", AQ_COVERAGE_RATIO)]
    + [("SECTION", "IAS 39 incurred-loss impairment model, Loans and advances to customers only - FY2014-FY2018", {})]
    + [("DATA", "Gross loans and advances to customers", stock(AQ_AFS_GROSS_LOANS))]
    + [("DATA", "Specific impairment provision", stock(AQ_AFS_SPECIFIC))]
    + [("DATA", "Collective impairment provision", stock(AQ_AFS_COLLECTIVE))]
    + [("TOTAL", "Total impairment provision", stock(AQ_AFS_TOTAL_IMPAIR))]
    + [("TOTAL", "Net loans and advances to customers", stock(AQ_AFS_NET_LOANS))]
    + [("DATA", "Gross impaired loans and advances (Bank's own headline non-performing figure)", stock(AQ_AFS_GROSS_IMPAIRED))]
    + [("DATA", "Gross impaired advances as % of gross loans and advances to customers (NPL ratio)", AQ_AFS_NPL_RATIO)]
    + [("DATA", "Total impairment provision as % of gross loans and advances to customers (coverage)", AQ_AFS_COVERAGE_RATIO)]
)

bw.add_asset_quality_sheet(
    title="Punjab National Bank (International) Limited — Asset Quality",
    subtitle="Entity-level. IFRS 9 stage 1/2/3 split (FY2019-FY2026) for Loans and advances to banks/customers "
             "and Investment securities at amortised cost combined (the Bank's own 'loans & advances at "
             "amortised cost by product' note table); IAS 39 incurred-loss model (FY2014-FY2018, Loans and "
             "advances to customers only - see the section note below). £'000 converted from the Bank's native "
             "US$'000 presentation.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nFY2026: Note 19, printed p.80 - " + AR_URL["FY2026"] + "; FY2025: Note 19, printed p.77 - "
        + AR_URL["FY2025"] + " (FY2024 comparative also sourced here); FY2023: Note 19, printed p.67 - "
        + AR_URL["FY2023"] + " (FY2022 comparative also sourced here); FY2020: Note 25, printed pp.60-61 - "
        + AR_URL["FY2020"] + " (FY2019 comparative also sourced here, printed p.61).\n\n"
        "A large, steadily-declining Stage 3/impaired-loan book is genuinely disclosed every year (34.34% of gross "
        "loans in FY2017, rising to 37.92% in FY2018, then 28.79% by FY2022, down to 7.66% by FY2026) - not a "
        "transcription artefact; the Bank's own Annual Reports discuss legacy non-performing exposures, mostly "
        "originated before FY2016, being worked down over this period. FY2014-FY2018 figures are sourced from "
        "each year's own Balance Sheet/Loans and advances to customers note - FY2014: p.17/Note 13, "
        + AR_URL["FY2014"] + "; FY2015: Note 13, " + AR_URL["FY2015"] + "; FY2016: Note 13, " + AR_URL["FY2016"]
        + "; FY2017/FY2018: Note 21, " + AR_URL["FY2018"] + " (native-text PDF, FY2017 comparative sourced here "
        "for higher transcription confidence). FY2014-FY2016 sources are OCR'd from scanned PDFs; each year's own "
        "gross/provisions/net figures were cross-checked to sum exactly (net = gross - impairment) and, where "
        "shown, to the following year's own comparative column."
    ),
    first_col_width=88,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)


def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, p3_sources(), note=note,
                        first_col_width=54, source_height=180)


CAPITAL_NOTE = ("Directly disclosed in the annual Pillar 3 UK KM1 table (FY2018-FY2026) or its pre-KM1 'Capital "
                 "Resources'/CA1-style equivalent (FY2014-FY2017 - see p3_sources()'s HD-048 methodology note); "
                 "figures are converted from $m to £m at the corresponding 31 March spot rate.")
RWA_NOTE = ("Directly disclosed total risk-weighted exposure amount in the annual Pillar 3 UK KM1 table "
            "(FY2018-FY2026) or its pre-KM1 'Capital Resources' table equivalent (FY2014-FY2017); converted from "
            "$m to £m at the corresponding 31 March spot rate.")
LCR_NOTE = (
    "The Bank's own report-year headline LCR is used. FY2025's report shows 201% for FY2025, while its FY2024 "
    "comparative shows 528%; the FY2024 report itself reported 647% for FY2024. This workbook preserves each year's "
    "own as-reported figure rather than replacing it with a later comparative restatement. FY2014 and FY2015 are "
    "left blank because the EU's LCR delegated act was not adopted until October 2014 and PNBIL's own Pillar 3 "
    "disclosures do not report an LCR figure for either year - a genuine regulatory-timing gap, not a missed "
    "disclosure."
)

CET1 = {"FY2026": 138.2, "FY2025": 140.8, "FY2024": 144.1, "FY2023": 143.1, "FY2022": 137.9, "FY2021": 134.4,
        "FY2020": 146.1, "FY2019": 150.4, "FY2018": 142.8, "FY2017": 120.5,
        "FY2016": 149.625, "FY2015": 182.989, "FY2014": 169.143}
TIER1 = {"FY2026": 183.2, "FY2025": 185.8, "FY2024": 189.1, "FY2023": 188.1, "FY2022": 182.9, "FY2021": 179.4,
         "FY2020": 191.1, "FY2019": 195.4, "FY2018": 187.8, "FY2017": 165.5,
         "FY2016": 174.625, "FY2015": 182.989, "FY2014": 169.143}
TOTAL_CAPITAL = {"FY2026": 210.9, "FY2025": 216.1, "FY2024": 223.1, "FY2023": 226.4, "FY2022": 213.9, "FY2021": 206.6,
                  "FY2020": 225.7, "FY2019": 236.3, "FY2018": 237.2, "FY2017": 219.8,
                  "FY2016": 245.233, "FY2015": 274.878, "FY2014": 252.637}
RWA = {"FY2026": 894.9, "FY2025": 697.1, "FY2024": 701.0, "FY2023": 730.1, "FY2022": 802.6, "FY2021": 784.6,
       "FY2020": 755.9, "FY2019": 797.6, "FY2018": 906.2, "FY2017": 1013.0,
       "FY2016": 1635.853, "FY2015": 1764.265, "FY2014": 1654.759}
CET1_RATIO = {"FY2026": "15.4%", "FY2025": "20.2%", "FY2024": "20.6%", "FY2023": "19.6%", "FY2022": "17.2%", "FY2021": "17.1%",
              "FY2020": "19.3%", "FY2019": "18.9%", "FY2018": "15.8%", "FY2017": "11.90%",
              "FY2016": "9.15%", "FY2015": "10.37%", "FY2014": "10.22%"}
TIER1_RATIO = {"FY2026": "20.5%", "FY2025": "26.7%", "FY2024": "27.0%", "FY2023": "25.8%", "FY2022": "22.8%", "FY2021": "22.9%",
               "FY2020": "25.3%", "FY2019": "24.5%", "FY2018": "20.7%", "FY2017": "16.3%",
               "FY2016": "10.67%", "FY2015": "10.37%", "FY2014": "10.22%"}
TOTAL_RATIO = {"FY2026": "23.6%", "FY2025": "31.0%", "FY2024": "31.8%", "FY2023": "31.0%", "FY2022": "26.7%", "FY2021": "26.3%",
               "FY2020": "29.9%", "FY2019": "29.6%", "FY2018": "26.2%", "FY2017": "21.7%",
               "FY2016": "14.99%", "FY2015": "15.58%", "FY2014": "15.27%"}
LEVERAGE = {"FY2026": "13.6%", "FY2025": "16.7%", "FY2024": "19.1%", "FY2023": "19.9%", "FY2022": "19.3%", "FY2021": "17.3%",
            "FY2020": "20.4%", "FY2019": "15.1%", "FY2018": "12.94%", "FY2017": "9.7%",
            "FY2016": "8.93%", "FY2015": "8.78%", "FY2014": "7.83%"}
LCR = {"FY2026": "350%", "FY2025": "201%", "FY2024": "647%", "FY2023": "384%", "FY2022": "405%", "FY2021": "748%",
       "FY2020": "403%", "FY2019": "524%", "FY2018": "1027%", "FY2017": "1040%",
       "FY2016": "167.00%"}
NSFR = {"FY2026": "118%", "FY2025": "121%", "FY2024": "130%", "FY2023": "135%", "FY2022": "128%", "FY2021": "146%",
        "FY2020": "126%", "FY2019": "139%", "FY2018": "171%", "FY2017": "180%",
        "FY2016": "119%", "FY2015": "131%", "FY2014": "110%"}

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
RWA_CREDIT = {"FY2026": 813.0, "FY2025": 611.3, "FY2024": 629.0, "FY2023": 666.7, "FY2022": 747.3, "FY2021": 728.7,
              "FY2020": 679.4, "FY2019": 716.1, "FY2018": 774.7, "FY2017": 830.9,
              "FY2016": 1457.986, "FY2015": 1559.581, "FY2014": 1504.345}
RWA_CCR = {"FY2026": 6.4, "FY2025": 14.5, "FY2024": 0.2, "FY2023": 0.3, "FY2022": 1.8, "FY2021": 1.5}
RWA_MARKET = {"FY2026": 8.5, "FY2025": 7.7, "FY2024": 11.6, "FY2023": 11.2, "FY2022": 10.3, "FY2021": 11.0,
              "FY2020": 25.9, "FY2019": 25.3, "FY2018": 64.5, "FY2017": 93.9,
              "FY2016": 83.609, "FY2015": 123.014, "FY2014": 85.615}
RWA_OPERATIONAL = {"FY2026": 66.9, "FY2025": 63.4, "FY2024": 60.0, "FY2023": 51.8, "FY2022": 42.8, "FY2021": 44.9,
                    "FY2020": 50.6, "FY2019": 56.2, "FY2018": 67.0, "FY2017": 88.3,
                    "FY2016": 94.258, "FY2015": 81.669, "FY2014": 64.799}
RWA_BREAKDOWN_TOTAL = {"FY2026": 894.8, "FY2025": 697.1, "FY2024": 701.0, "FY2023": 730.1, "FY2022": 802.6, "FY2021": 784.6,
                        "FY2020": 755.9, "FY2019": 797.6, "FY2018": 906.2, "FY2017": 1013.0,
                        "FY2016": 1635.853, "FY2015": 1764.264, "FY2014": 1654.759}

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", stock(RWA_CREDIT)),
    ("DATA", "Counterparty credit risk (CCR, incl. CVA)", stock(RWA_CCR)),
    ("DATA", "Market risk", stock(RWA_MARKET)),
    ("DATA", "Operational risk", stock(RWA_OPERATIONAL)),
    ("TOTAL", "Total risk-weighted exposure amount", stock(RWA_BREAKDOWN_TOTAL)),
]
bw.add_rwa_breakdown_sheet(
    title="Punjab National Bank (International) Limited — RWA Breakdown",
    subtitle="Entity-level, solo basis. £m converted from the Bank's native US$ million presentation. FY2014-"
             "FY2020's 'Credit risk' row folds counterparty credit risk and CVA into one combined figure (that "
             "era's own Pillar I disclosure does not separate them out) - see the HD-048 note below.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\n\nUK OV1 table: FY2025/FY2024 - " + P3_URL["FY2025"] + ", printed p.45; FY2023/FY2022 - "
        + P3_URL["FY2023"] + ", printed p.44. FY2026 derived from " + P3_URL["FY2026"]
        + ", printed pp.14/27-30/33 (credit risk exposure-class table, CCR table, market risk table, operational "
        "risk table) - the FY2026 Pillar 3 document does not include a UK OV1 template (confirmed by reading the "
        "full document), a genuine structural change from FY2022-FY2025's disclosures.\n\n"
        "HD-048 (2026-09-05/06) FY2014-FY2020: derived from each year's own 'Capital Requirement under Pillar I' "
        "table (own basis, predates the UK OV1 template) - FY2020: " + P3_URL["FY2020"] + ", printed p.9; FY2019: "
        + P3_URL["FY2019"] + ", printed p.9; FY2018: " + P3_URL["FY2018"] + ", printed pp.10/11; FY2017: "
        + P3_URL["FY2017"] + ", printed p.7 (own-year credit risk/market risk/operational risk 'Capital "
        "Requirement' totals); FY2016: " + P3_URL["FY2016"] + ", printed pp.3-4 (OCR'd from a scanned PDF); "
        "FY2015: " + P3_URL["FY2015"] + ", printed pp.2-3 (OCR'd from a scanned PDF); FY2014: " + P3_URL["FY2014"]
        + ", printed pp.2-3 (OCR'd from a scanned PDF). Each year's Credit Risk/Market Risk/Operational Risk "
        "'RWA After SME Benefit' figures sum exactly to that year's own disclosed total RWA."
    ),
    first_col_width=60,
    source_height=320,
    unit_suffix=" (£m, conv. from USD)",
)

metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", LEVERAGE)],
       "FY2014-FY2020 show each year's own quarterly-average 'Leverage Ratio using a fully phased-in definition "
       "of Tier 1' (a full CRR leverage ratio including central bank claims, predating the UK's post-2016 "
       "central-bank-claims-excluded leverage framework used from FY2022 on) - a genuine methodology change "
       "across the two eras, not a like-for-like series; see the metric values for each report's own comparative "
       "column, which sometimes differs from the prior year's own headline figure for this same reason.")
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)], LCR_NOTE)
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)])
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "No MREL ratio or MREL target is disclosed in any FY2014-FY2026 Pillar 3 report or annual report reviewed; left explicitly undisclosed."},
)

EQ_OPENING_NATIVE = {"FY2026": 211161, "FY2025": 214651, "FY2024": 213328, "FY2023": 208266, "FY2022": 204088,
                      "FY2020": 216869, "FY2019": 211038, "FY2018": 191780, "FY2017": 178631,
                      "FY2016": 208127, "FY2015": 194331, "FY2014": 143583}
# HD-048: FY2014-FY2020's "other movements" also include share capital issuances (FY2014 $50,000k, FY2017
# $125,000k, FY2018 $20,000k) and, for FY2016/FY2019, small deferred-tax items alongside the AT1 dividend -
# this row absorbs whatever is needed to close Opening + Total comprehensive income + Other = Closing exactly
# (FY2017's -22 tax reclass to retained earnings, disclosed on the Statement of Changes in Equity sheet, is
# folded in here rather than broken out on this summary sheet).
EQ_OTHER_MOVEMENTS_NATIVE = {"FY2026": -4321, "FY2025": -4636, "FY2024": -4834, "FY2023": -3578, "FY2022": -2367,
                              "FY2020": -3362, "FY2019": -3036, "FY2018": 17072, "FY2017": 124978,
                              "FY2016": -910, "FY2015": -1082, "FY2014": 48889}

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
