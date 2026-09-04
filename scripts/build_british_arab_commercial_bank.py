import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR_URL = {
    "FY2025": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2025_WEB-Final.pdf",
    "FY2024": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2024_WEB-Final.pdf",
    "FY2023": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2023_WEB-06.pdf",
    "FY2022": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2022_WEB-1proof-10.pdf",
    "FY2021": "https://files.bacb.co.uk/production/files/BACB_AnnualReportYE2021-1.pdf",
}
P3_URL = {
    "FY2025": "https://files.bacb.co.uk/production/files/BACB_Pillar3_YE2025web-03.pdf",
    "FY2024": "https://files.bacb.co.uk/production/files/BACB_Pillar3_YE2024web-05.pdf",
    "FY2023": "https://files.bacb.co.uk/production/files/BACB_Pillar3YE2023-03-002.pdf",
    "FY2022": "https://files.bacb.co.uk/production/files/BACB_Pillar3YE2022-1.pdf",
    "FY2021": "https://files.bacb.co.uk/production/files/BACB_Pillar3-2021_v3.pdf",
}

ENTITY_NOTE = (
    "British Arab Commercial Bank PLC (\"BACB\"), company 01047302 (incorporated 1972 as UBAF Limited, "
    "renamed British Arab Commercial Bank Limited 1996, re-registered as a public company 2009), FRN 204564. "
    "Owned by a consortium: Libyan Foreign Bank 85.95% (wholly owned by the Central Bank of Libya), Banque "
    "Exterieure d'Algerie 7.025%, Banque Centrale Populaire (Morocco) 7.025%. Single UK entity, no "
    "subsidiaries/associates, no prudential consolidation. Does NOT take the FRS 101/102 cash-flow exemption - "
    "full Statement of Cash Flow every year. GBP throughout, no FX conversion needed. Companies House status: "
    "Active, no going-concern issues found in any of the 5 Annual Reports (unqualified audits throughout).\n\n"
    "RESTATEMENTS: this bank's own cash flow comparatives shift modestly between report vintages (e.g. FY2021's "
    "\"Net cash gained from operating activities\" is 189,594 in the 2021 report's own figures vs 189,407 in "
    "2022's comparative; FY2024's is 227,828 in 2024's own report vs 227,636 in 2025's comparative) - each "
    "year's column here uses that year's own originally-published report, per project convention, not a later "
    "report's restated comparative."
)

CASH_FLOW_SOURCES = (
    "Sources - British Arab Commercial Bank PLC's own Statement of Cash Flow, each year from that year's own "
    "Annual Report (not a later report's restated comparative):\n"
    f"FY2025: Annual Report YE2025, pp.65-66 - {AR_URL['FY2025']}\n"
    f"FY2024: Annual Report YE2024, pp.59-60 - {AR_URL['FY2024']}\n"
    f"FY2023: Annual Report YE2023, p.60 - {AR_URL['FY2023']}\n"
    f"FY2022: Annual Report YE2022, p.56 - {AR_URL['FY2022']}\n"
    f"FY2021: Annual Report YE2021, p.48 - {AR_URL['FY2021']}\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - British Arab Commercial Bank PLC Pillar 3 Disclosures, UK KM1 Key Metrics template:\n"
        f"FY2025: 2025 Pillar 3 Disclosures, p.6 (own year) - {P3_URL['FY2025']}\n"
        f"FY2024: 2024 Pillar 3 Disclosures, p.6 (own year) - {P3_URL['FY2024']}\n"
        f"FY2023: 2023 Pillar 3 Disclosures, p.6 (own year) - {P3_URL['FY2023']}\n"
        f"FY2022: 2022 Pillar 3 Disclosures, p.7 (own year) - {P3_URL['FY2022']}\n"
        f"FY2021: sourced from the 2022 Pillar 3 Disclosures' own FY2021 comparative column, p.7 - "
        f"{P3_URL['FY2022']} (the 2021 Pillar 3 document predates the modern UK KM1 template and has no "
        "equivalent single table - same approach as Aldermore/BLME/Bank of Ireland UK elsewhere in this project).\n"
        + (extra + "\n" if extra else "")
    )


bw = BankWorkbook(bank_name="British Arab Commercial Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="0E7C9E")

STATEMENTS_NOTE = (
    "Each year's Balance Sheet/P&L/Equity column uses that year's own originally-published Annual Report, not a "
    "later report's restated comparative (same convention as the Cash Flow Statement - see its own note). This "
    "surfaces several genuine, small restatements between vintages, all left as originally reported and flagged "
    "here rather than silently blended:\n"
    "- FY2023's own report (AR2023) states Profit for the year GBP27,875k / Total comprehensive income GBP30,511k; "
    "the FY2024 report's FY2023 comparative restates these to GBP29,044k / GBP30,527k (AR2024 Note 2 states this "
    "reclassification affected both the 2023 SOCI and SOFP - not detailed further in that report).\n"
    "- FY2023's own report's closing equity is Retained earnings GBP120,650k / Fair value reserve -GBP1,921k; the "
    "FY2024 report's own 1 January 2024 opening balance is GBP121,819k / -GBP3,090k for the same two lines (Total "
    "equity and Other reserves total unaffected - a GBP1,169k reclass between the two reserve lines only). Shown "
    "here as an explicit 'Reclassification between reserves (per FY2024 report)' row at FY2024's opening.\n"
    "- A smaller, similar GBP42k reclass between Retained earnings and Fair value reserve exists between FY2021's "
    "own closing balance and FY2022's own opening balance (Total equity unaffected); shown the same way.\n"
    "- FY2021's own report's Net operating income (GBP53,466k) and Other operating income (GBP1,519k) differ "
    "immaterially (GBP21k) from the FY2022 report's own FY2021 comparative (GBP53,487k / GBP1,540k); FY2021's own "
    "figures are used here.\n"
    "- FY2021's own report's Total assets (GBP2,782,543k, incl. Net pension asset GBP5,480k and Deferred tax "
    "liabilities GBP539k) differs from the FY2022 report's own FY2021 comparative (GBP2,782,004k) by the same "
    "amount - FY2021's own figures are used here.\n"
    "- Within FY2023's own equity statement, an 'Other Fair Value adjustments' GBP16k line pushes the equity "
    "statement's own Total comprehensive income for FY2023 (GBP30,527k) GBP16k above the P&L's own Total "
    "comprehensive income for FY2023 (GBP30,511k) - a small internal inconsistency present in the Bank's own "
    "audited report, not introduced here.\n\n"
    "Presentation changes: FY2025/FY2024's P&L splits interest income/expense into 'calculated under the "
    "effective interest method' vs 'other method'; FY2023/FY2022/FY2021 report single combined interest income/"
    "expense lines. FY2021's P&L has no 'Revaluation of property, plant & equipment' OCI line (adopted from "
    "FY2022). Balance sheet: 'Deferred tax assets' appears as its own line only FY2023 (nil) and FY2022 "
    "(GBP3,561k); 'Corporation tax receivable/payable' and 'Deferred tax liabilities' lines appear inconsistently "
    "across years depending on the sign of that year's balance - left blank where a report has no equivalent line "
    "that year, not assumed zero."
)

STATEMENTS_SOURCES = (
    "Sources - British Arab Commercial Bank PLC's own Statement of Comprehensive Income / Statement of Financial "
    "Position / Statement of Changes in Equity, each year from that year's own Annual Report:\n"
    f"FY2025: Annual Report YE2025, pp.62-64 - {AR_URL['FY2025']}\n"
    f"FY2024: Annual Report YE2024, pp.56-58 - {AR_URL['FY2024']}\n"
    f"FY2023: Annual Report YE2023, pp.57-59 - {AR_URL['FY2023']}\n"
    f"FY2022: Annual Report YE2022, pp.2.2-2.4 - {AR_URL['FY2022']}\n"
    f"FY2021: Annual Report YE2021, pp.2.2-2.4 - {AR_URL['FY2021']}\n\n"
    + STATEMENTS_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Statement of Financial Position)
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash, notes and coins", {"FY2025": 0, "FY2024": 1, "FY2023": 1, "FY2022": 0, "FY2021": 218}),
    ("DATA", "Derivatives", {"FY2025": 2008, "FY2024": 1770, "FY2023": 661, "FY2022": 1344, "FY2021": 616}),
    ("DATA", "Reverse repurchase agreements",
     {"FY2025": 25147, "FY2024": 210601, "FY2023": 86937, "FY2022": 236927, "FY2021": 215824}),
    ("DATA", "Loans and advances to banks",
     {"FY2025": 1570302, "FY2024": 1271347, "FY2023": 855620, "FY2022": 755184, "FY2021": 588843}),
    ("DATA", "Loans and advances to customers",
     {"FY2025": 353562, "FY2024": 387260, "FY2023": 388567, "FY2022": 463780, "FY2021": 484536}),
    ("DATA", "Financial investments",
     {"FY2025": 1317406, "FY2024": 1427440, "FY2023": 1621748, "FY2022": 1695000, "FY2021": 1456288}),
    ("DATA", "Prepayments, accrued income and other debtors",
     {"FY2025": 14721, "FY2024": 8497, "FY2023": 10424, "FY2022": 3014, "FY2021": 3437}),
    ("DATA", "Corporation tax receivable", {"FY2023": 947, "FY2022": 223}),
    ("DATA", "Deferred tax assets", {"FY2023": 0, "FY2022": 3561}),
    ("DATA", "Property, plant and equipment",
     {"FY2025": 30946, "FY2024": 31014, "FY2023": 29839, "FY2022": 27271, "FY2021": 19719}),
    ("DATA", "Intangible assets",
     {"FY2025": 2305, "FY2024": 2937, "FY2023": 4566, "FY2022": 6222, "FY2021": 7582}),
    ("DATA", "Net pension asset",
     {"FY2025": 2353, "FY2024": 2599, "FY2023": 2617, "FY2022": 2219, "FY2021": 5480}),
    ("TOTAL", "Total assets",
     {"FY2025": 3318750, "FY2024": 3343466, "FY2023": 3001927, "FY2022": 3194745, "FY2021": 2782543}),

    ("SECTION", "Liabilities", {}),
    ("DATA", "Derivatives", {"FY2025": 728, "FY2024": 1056, "FY2023": 46, "FY2022": 507, "FY2021": 1268}),
    ("DATA", "Deposits from banks",
     {"FY2025": 2110653, "FY2024": 2218623, "FY2023": 1960559, "FY2022": 2144470, "FY2021": 1876756}),
    ("DATA", "Other deposits",
     {"FY2025": 828120, "FY2024": 758949, "FY2023": 699119, "FY2022": 737763, "FY2021": 604750}),
    ("DATA", "Other liabilities, accruals and deferred income",
     {"FY2025": 29930, "FY2024": 29369, "FY2023": 33274, "FY2022": 27080, "FY2021": 17530}),
    ("DATA", "Corporation tax payable", {"FY2025": 327, "FY2024": 810, "FY2021": 900}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 1646, "FY2024": 2821, "FY2023": 1797, "FY2021": 539}),
    ("DATA", "Subordinated liabilities",
     {"FY2025": 69006, "FY2024": 74226, "FY2023": 74554, "FY2022": 77659, "FY2021": 70514}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 3040410, "FY2024": 3085854, "FY2023": 2769349, "FY2022": 2987479, "FY2021": 2572257}),

    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital",
     {"FY2025": 108069, "FY2024": 107097, "FY2023": 106377, "FY2022": 105592, "FY2021": 104357}),
    ("DATA", "Capital redemption reserve",
     {"FY2025": 4104, "FY2024": 4104, "FY2023": 4104, "FY2022": 4104, "FY2021": 4104}),
    ("DATA", "Other reserves",
     {"FY2025": 166167, "FY2024": 146411, "FY2023": 122097, "FY2022": 97570, "FY2021": 101825}),
    ("TOTAL", "Total equity",
     {"FY2025": 278340, "FY2024": 257612, "FY2023": 232578, "FY2022": 207266, "FY2021": 210286}),
    ("TOTAL", "Total liabilities and equity",
     {"FY2025": 3318750, "FY2024": 3343466, "FY2023": 3001927, "FY2022": 3194745, "FY2021": 2782543}),
]

bw.add_balance_sheet_sheet(
    title="British Arab Commercial Bank PLC — Statement of Financial Position",
    subtitle="Bank entity basis (single UK entity, no subsidiaries/associates). GBP throughout, no FX conversion.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=460,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Statement of Comprehensive Income)
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income (or: calculated under effective interest method)",
     {"FY2025": 130031, "FY2024": 144622, "FY2023": 168035, "FY2022": 71950, "FY2021": 33156}),
    ("DATA", "Interest income calculated using other method", {"FY2025": 34805, "FY2024": 38274}),
    ("DATA", "Interest expense and similar charges (or: calculated under effective interest method)",
     {"FY2025": -101087, "FY2024": -112061, "FY2023": -103747, "FY2022": -38301, "FY2021": -12248}),
    ("DATA", "Interest expense calculated using other method", {"FY2025": -325, "FY2024": -192}),
    ("TOTAL", "Net interest income",
     {"FY2025": 63424, "FY2024": 70643, "FY2023": 64288, "FY2022": 33649, "FY2021": 20908}),
    ("DATA", "Fee and commission income",
     {"FY2025": 25974, "FY2024": 26821, "FY2023": 24098, "FY2022": 21653, "FY2021": 17502}),
    ("DATA", "Fee and commission expense",
     {"FY2025": -7360, "FY2024": -6431, "FY2023": -6977, "FY2022": -4035, "FY2021": -1599}),
    ("TOTAL", "Net fee and commission income",
     {"FY2025": 18614, "FY2024": 20390, "FY2023": 17121, "FY2022": 17618, "FY2021": 15903}),
    ("DATA", "Net trading (and other) income",
     {"FY2025": 9424, "FY2024": 6549, "FY2023": 5546, "FY2022": 6522, "FY2021": 3393}),
    ("DATA", "Other operating income/(expense)",
     {"FY2025": 1301, "FY2024": 1068, "FY2023": 901, "FY2022": -356, "FY2021": 1519}),
    ("TOTAL", "Operating income before allowance for credit losses",
     {"FY2025": 92763, "FY2024": 98650, "FY2023": 87856, "FY2022": 57433, "FY2021": 41723}),
    ("DATA", "Allowance for credit losses",
     {"FY2025": -2313, "FY2024": -3992, "FY2023": -479, "FY2022": -3306, "FY2021": -1245}),
    ("DATA", "Reversal of allowances booked in previous periods",
     {"FY2025": 5554, "FY2024": 5633, "FY2023": 2623, "FY2022": 1825, "FY2021": 12441}),
    ("DATA", "Recoveries of amounts written off in previous periods",
     {"FY2024": 0, "FY2023": 1, "FY2022": 4, "FY2021": 547}),
    ("TOTAL", "Net reversals/(allowances) for credit losses",
     {"FY2025": 3241, "FY2024": 1641, "FY2023": 2145, "FY2022": -1477, "FY2021": 11743}),
    ("TOTAL", "Net operating income",
     {"FY2025": 96004, "FY2024": 100291, "FY2023": 90001, "FY2022": 55956, "FY2021": 53466}),
    ("DATA", "Administrative expenses",
     {"FY2025": -64363, "FY2024": -62082, "FY2023": -53594, "FY2022": -42031, "FY2021": -38763}),
    ("TOTAL", "Profit before income tax",
     {"FY2025": 31641, "FY2024": 38209, "FY2023": 36407, "FY2022": 13925, "FY2021": 14703}),
    ("DATA", "Income tax credit/(charge)",
     {"FY2025": -7514, "FY2024": -9454, "FY2023": -8532, "FY2022": 1175, "FY2021": -1668}),
    ("TOTAL", "Profit for the year",
     {"FY2025": 24127, "FY2024": 28755, "FY2023": 27875, "FY2022": 15100, "FY2021": 13035}),

    ("SECTION", "Other comprehensive income/(expense), net of tax", {}),
    ("DATA", "Remeasurement of defined benefit liability",
     {"FY2025": -219, "FY2024": -1558, "FY2023": -1257, "FY2022": -4161, "FY2021": 3231}),
    ("DATA", "Revaluation gain/(loss) on equity investments designated at FVOCI",
     {"FY2025": -244, "FY2024": 61, "FY2023": -1048, "FY2022": -376, "FY2021": -138}),
    ("DATA", "Disposal of equity investment designated at FVOCI", {"FY2024": -161}),
    ("DATA", "Revaluation gain/(loss) on property, plant & equipment",
     {"FY2025": 871, "FY2024": 778, "FY2023": -3359, "FY2022": 7851}),
    ("DATA", "Related tax (items not reclassified to P&L)",
     {"FY2025": 1379, "FY2024": -420, "FY2023": 1109, "FY2022": -1153, "FY2021": -588}),
    ("DATA", "Change in fair value for debt securities designated at FVOCI",
     {"FY2025": 786, "FY2024": 2662, "FY2023": 9036, "FY2022": -14178, "FY2021": -3924}),
    ("DATA", "Other Fair value adjustments", {"FY2023": 16}),
    ("DATA", "Credit loss on debt securities at FVOCI transferred to P&L",
     {"FY2025": -128, "FY2024": -18, "FY2023": -79, "FY2022": -57, "FY2021": -218}),
    ("DATA", "FV gains on debt securities at FVOCI transferred to income upon derecognition",
     {"FY2025": 775, "FY2024": 508, "FY2023": 397, "FY2022": -646, "FY2021": 1130}),
    ("DATA", "Related tax (items that may be reclassified to P&L)",
     {"FY2025": -391, "FY2024": -793, "FY2023": -2163, "FY2022": 3349, "FY2021": 551}),
    ("TOTAL", "Other comprehensive income/(expense) for the year, net of tax",
     {"FY2025": 2829, "FY2024": 1059, "FY2023": 2636, "FY2022": -9371, "FY2021": 44}),
    ("TOTAL", "Total comprehensive income for the year",
     {"FY2025": 26956, "FY2024": 29814, "FY2023": 30511, "FY2022": 5729, "FY2021": 13079}),
]

bw.add_income_statement_sheet(
    title="British Arab Commercial Bank PLC — Statement of Comprehensive Income",
    subtitle="Bank entity basis (single UK entity, no subsidiaries/associates). GBP throughout, no FX conversion.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=460,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity (chronological, oldest to newest)
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "Balance at 1 January 2021", (104357, 4104, 83713, 0, 5033, 197207)),
    ("DATA", "Profit for the year (FY2021)", (None, None, 13035, None, None, 13035)),
    ("DATA", "Other comprehensive income (FY2021)", (None, None, 2505, None, -2461, 44)),
    ("TOTAL", "Balance at 31 December 2021 (per FY2021's own report)", (104357, 4104, 99253, 0, 2572, 210286)),
    ("DATA", "Reclassification between reserves (per FY2022 report's own opening balance)",
     (None, None, 42, None, -42, 0)),
    ("TOTAL", "Balance at 1 January 2022 (per FY2022's own report)", (104357, 4104, 99295, 0, 2530, 210286)),
    ("DATA", "Profit for the year (FY2022)", (None, None, 15100, None, None, 15100)),
    ("DATA", "Reclassification between FV reserve and retained earnings", (None, None, 126, None, -110, 16)),
    ("DATA", "Other comprehensive (expense)/income (FY2022)", (None, None, -3727, 5888, -11532, -9371)),
    ("DATA", "Issue of share capital (FY2022)", (1235, None, None, None, None, 1235)),
    ("DATA", "Dividend paid (FY2022)", (None, None, -10000, None, None, -10000)),
    ("TOTAL", "Balance at 31 December 2022", (105592, 4104, 100794, 5888, -9112, 207266)),
    ("DATA", "Profit for the year (FY2023)", (None, None, 27875, None, None, 27875)),
    ("DATA", "Other Fair Value adjustments (FY2023)", (None, None, 16, None, None, 16)),
    ("DATA", "Other comprehensive (expense)/income (FY2023)", (None, None, -2035, -2520, 7191, 2636)),
    ("DATA", "Issue of share capital (FY2023)", (785, None, None, None, None, 785)),
    ("DATA", "Dividend paid (FY2023)", (None, None, -6000, None, None, -6000)),
    ("TOTAL", "Balance at 31 December 2023 (per FY2023's own report)", (106377, 4104, 120650, 3368, -1921, 232578)),
    ("DATA", "Reclassification between reserves (per FY2024 report's own opening balance)",
     (None, None, 1169, None, -1169, 0)),
    ("TOTAL", "Balance at 1 January 2024 (per FY2024's own report)", (106377, 4104, 121819, 3368, -3090, 232578)),
    ("DATA", "Profit for the year (FY2024)", (None, None, 28755, None, None, 28755)),
    ("DATA", "Other comprehensive (expense)/income (FY2024)", (None, None, -1883, 583, 2359, 1059)),
    ("DATA", "Issue of share capital (FY2024)", (720, None, None, None, None, 720)),
    ("DATA", "Dividend paid (FY2024)", (None, None, -5500, None, None, -5500)),
    ("TOTAL", "Balance at 31 December 2024", (107097, 4104, 143191, 3951, -731, 257612)),
    ("DATA", "Profit for the year (FY2025)", (None, None, 24127, None, None, 24127)),
    ("DATA", "Other comprehensive (expense)/income (FY2025)", (None, None, -402, 2189, 1042, 2829)),
    ("DATA", "Issue of share capital (FY2025)", (972, None, None, None, None, 972)),
    ("DATA", "Dividend paid (FY2025)", (None, None, -7200, None, None, -7200)),
    ("TOTAL", "Balance at 31 December 2025", (108069, 4104, 159716, 6140, 311, 278340)),
]

bw.add_equity_changes_sheet(
    title="British Arab Commercial Bank PLC — Statement of Changes in Equity",
    subtitle="Bank entity basis, £'000. Chronological roll-forward, oldest to newest. GBP throughout, no FX conversion.",
    headers=["Share capital", "Capital redemption reserve", "Retained earnings", "Revaluation reserve",
             "Fair Value reserve", "Total equity"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
    source_height=460,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before taxation",
     {"FY2025": 31641, "FY2024": 38209, "FY2023": 36407, "FY2022": 13925, "FY2021": 14703}),
    ("DATA", "Allowance for credit losses",
     {"FY2025": 2313, "FY2024": 3992, "FY2023": 479, "FY2022": 3306, "FY2021": 1245}),
    ("DATA", "Recoveries of allowance for credit losses",
     {"FY2025": -5554, "FY2024": -5633, "FY2023": -2623, "FY2022": -1825, "FY2021": -12441}),
    ("DATA", "Depreciation and amortisation",
     {"FY2025": 3229, "FY2024": 3214, "FY2023": 2904, "FY2022": 2753, "FY2021": 2544}),
    ("DATA", "(Loss)/gain on sale or impairment of property, plant and equipment",
     {"FY2025": -6, "FY2024": 3, "FY2023": 518, "FY2022": 28, "FY2021": 9}),
    ("DATA", "Other non-cash items included in net profit",
     {"FY2025": -1275, "FY2024": -34, "FY2023": 115, "FY2022": 366, "FY2021": -3}),
    ("TOTAL", "Non-cash items included in net profit",
     {"FY2025": -1293, "FY2024": 1542, "FY2023": 1393, "FY2022": 4628, "FY2021": -8646}),
    ("DATA", "Reverse repurchase agreements",
     {"FY2024": 0, "FY2023": 149990, "FY2022": -21103, "FY2021": -36757}),
    ("DATA", "Loans, advances other than cash or cash equivalents",
     {"FY2025": -221607, "FY2024": -243014, "FY2023": -268285, "FY2022": -68881, "FY2021": -13840}),
    ("DATA", "Debt securities other than cash equivalents",
     {"FY2025": 250302, "FY2024": 164699, "FY2023": -108164, "FY2022": -221117, "FY2021": 7009}),
    ("DATA", "Derivatives",
     {"FY2025": -571, "FY2024": -1109, "FY2023": 683, "FY2022": -728, "FY2021": 465}),
    ("DATA", "Other debtors and prepayments",
     {"FY2025": -7064, "FY2024": 387, "FY2023": -9064, "FY2022": -1161, "FY2021": 1497}),
    ("TOTAL", "Change in operating assets",
     {"FY2025": 21060, "FY2024": -79037, "FY2023": -234840, "FY2022": -312990, "FY2021": -41626}),
    ("DATA", "Customer accounts and deposits by banks",
     {"FY2025": 78001, "FY2024": 277676, "FY2023": -94670, "FY2022": 165574, "FY2021": 238429}),
    ("DATA", "Other liabilities",
     {"FY2025": 2884, "FY2024": -2695, "FY2023": 10519, "FY2022": 9288, "FY2021": -12192}),
    ("TOTAL", "Change in operating liabilities",
     {"FY2025": 80885, "FY2024": 274981, "FY2023": -84151, "FY2022": 174862, "FY2021": 226237}),
    ("DATA", "Income tax paid",
     {"FY2025": -8155, "FY2024": -7867, "FY2023": -5220, "FY2022": -1169, "FY2021": -1074}),
    ("TOTAL", "Net cash generated from/(used in) operating activities",
     {"FY2025": 124138, "FY2024": 227828, "FY2023": -286411, "FY2022": -120744, "FY2021": 189594}),

    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment",
     {"FY2025": -409, "FY2024": -1590, "FY2023": -7683, "FY2022": -552, "FY2021": -274}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2022": 42}),
    ("DATA", "Proceeds on sale of equity investments", {"FY2024": 1162}),
    ("DATA", "Purchase of intangible assets",
     {"FY2025": -1128, "FY2024": -392, "FY2023": -841, "FY2022": -853, "FY2021": -540}),
    ("DATA", "Proceeds from sale of intangible assets", {"FY2022": 269}),
    ("TOTAL", "Net cash used in investing activities",
     {"FY2025": -1537, "FY2024": -820, "FY2023": -8524, "FY2022": -1094, "FY2021": -814}),

    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Dividend paid", {"FY2025": -6228, "FY2024": -4780, "FY2023": -5215, "FY2022": -8765}),
    ("DATA", "Lease payments for Right of Use assets (principal)",
     {"FY2025": -249, "FY2024": -83, "FY2023": -202, "FY2022": -6, "FY2021": -191}),
    ("DATA", "Interest on lease payments", {"FY2024": -192}),
    ("DATA", "Subordinated debt issued", {"FY2024": 28185}),
    ("DATA", "Subordinated debt redeemed", {"FY2024": -28185}),
    ("TOTAL", "Net cash used in financing activities",
     {"FY2025": -6477, "FY2024": -5055, "FY2023": -5417, "FY2022": -8771, "FY2021": -191}),

    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents",
     {"FY2025": 116124, "FY2024": 221953, "FY2023": -300352, "FY2022": -130609, "FY2021": 188589}),
    ("DATA", "Cash and cash equivalents at the beginning of the year",
     {"FY2025": 604467, "FY2024": 372940, "FY2023": 700795, "FY2022": 766720, "FY2021": 586617}),
    ("DATA", "Effect of exchange rate change on cash and cash equivalents",
     {"FY2025": -2014, "FY2024": 9574, "FY2023": -27503, "FY2022": 64684, "FY2021": -8486}),
    ("TOTAL", "Cash and cash equivalents at the end of the year",
     {"FY2025": 718577, "FY2024": 604467, "FY2023": 372940, "FY2022": 700795, "FY2021": 766720}),

    ("SECTION", "Cash and cash equivalents comprise", {}),
    ("DATA", "Cash, notes and coin",
     {"FY2025": 0, "FY2024": 1, "FY2023": 1, "FY2022": 0, "FY2021": 218}),
    ("DATA", "Loans and advances to banks of original maturity three months or less",
     {"FY2025": 409309, "FY2024": 488558, "FY2023": 216705, "FY2022": 391580, "FY2021": 376162}),
    ("DATA", "Debt securities/certificates of deposit of three months original maturity or less",
     {"FY2025": 309268, "FY2024": 115908, "FY2023": 156234, "FY2022": 309215, "FY2021": 390340}),
    ("TOTAL", "Cash and cash equivalents",
     {"FY2025": 718577, "FY2024": 604467, "FY2023": 372940, "FY2022": 700795, "FY2021": 766720}),
]

bw.add_cash_flow_sheet(
    title="British Arab Commercial Bank PLC — Statement of Cash Flow",
    subtitle="Bank entity basis (single UK entity, no subsidiaries/associates). GBP throughout, no FX conversion.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality: Loans and advances to customers by IFRS 9 stage, from the
# Bank's own "Credit quality analysis" note each year (own report). FY2024
# and FY2022's own reports present credit quality only via a combined
# grade-based table across all financial assets (no customer-loan-specific
# stage split that year) - confirmed by reading each report in full, left
# blank rather than assumed or backfilled from a different year's document.
# ---------------------------------------------------------------
AQ_S1 = {"FY2025": 270253, "FY2023": 254360, "FY2021": 417375}
AQ_S2 = {"FY2025": 36036, "FY2023": 102165, "FY2021": 69314}
AQ_S3 = {"FY2025": 49098, "FY2023": 43879, "FY2021": 11038}
AQ_GROSS_TOTAL = {"FY2025": 355387, "FY2023": 400404, "FY2021": 497727}
AQ_ALLOW_S1 = {"FY2025": -266, "FY2023": -229, "FY2021": -632}
AQ_ALLOW_S2 = {"FY2025": -628, "FY2023": -2442, "FY2021": -4388}
AQ_ALLOW_S3 = {"FY2025": -931, "FY2023": -9166, "FY2021": -8171}
AQ_ALLOW_TOTAL = {"FY2025": -1825, "FY2023": -11837, "FY2021": -13191}
AQ_CARRYING = {"FY2025": 353562, "FY2024": 387260, "FY2023": 388567, "FY2022": 463780, "FY2021": 484536}
AQ_STAGE3_RATIO = {y: f"{AQ_S3[y] / AQ_GROSS_TOTAL[y] * 100:.2f}%" for y in AQ_S3}
AQ_STAGE3_COVERAGE = {y: f"{-AQ_ALLOW_S3[y] / AQ_S3[y] * 100:.2f}%" for y in AQ_S3}
AQ_OVERALL_COVERAGE = {y: f"{-AQ_ALLOW_TOTAL[y] / AQ_GROSS_TOTAL[y] * 100:.2f}%" for y in AQ_S3}

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by IFRS 9 stage (gross exposure)", {}),
    ("DATA", "Stage 1 (12-month ECL)", AQ_S1),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", AQ_S2),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired / default)", AQ_S3),
    ("TOTAL", "Total gross exposure", AQ_GROSS_TOTAL),
    ("SECTION", "Loss allowance, by stage", {}),
    ("DATA", "Stage 1 allowance", AQ_ALLOW_S1),
    ("DATA", "Stage 2 allowance", AQ_ALLOW_S2),
    ("DATA", "Stage 3 allowance", AQ_ALLOW_S3),
    ("TOTAL", "Total loss allowance", AQ_ALLOW_TOTAL),
    ("TOTAL", "Carrying amount (= Balance Sheet's Loans and advances to customers)", AQ_CARRYING),
    ("SECTION", "Ratios (FY2024/FY2022 not computable - see note)", {}),
    ("DATA", "Stage 3 exposure ratio (Stage 3 / total gross exposure)", AQ_STAGE3_RATIO),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 exposure)", AQ_STAGE3_COVERAGE),
    ("DATA", "Overall coverage ratio (total allowance / total gross exposure)", AQ_OVERALL_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="British Arab Commercial Bank PLC — Asset Quality / Credit Risk Disclosures",
    subtitle="Loans and advances to customers by IFRS 9 stage, £'000. Bank entity basis.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - British Arab Commercial Bank PLC's own 'Credit quality analysis' note (Loans and advances to "
        "customers only, £'000), each year from that year's own Annual Report:\n"
        f"FY2025: Annual Report YE2025, p.95 - {AR_URL['FY2025']}\n"
        f"FY2023: Annual Report YE2023, p.83 - {AR_URL['FY2023']}\n"
        f"FY2021: Annual Report YE2021, p.72 - {AR_URL['FY2021']}\n\n"
        "FY2024 and FY2022's own Annual Reports (checked in full) present credit quality only via a single "
        "grade-based table spanning all financial assets combined (cash, loans, debt securities, derivatives) - "
        "no customer-loan-specific Stage 1/2/3 split that year, unlike FY2025/FY2023/FY2021's own reports. "
        "Genuine finding: the Stage 3 exposure ratio rose sharply (2.22% FY2021 -> 13.82% FY2025) while the Stage "
        "3 coverage ratio fell sharply (74.03% FY2021 -> 1.90% FY2025) - consistent with the Bank's own disclosed "
        "credit-grade migration and write-off activity, not a data error."
    ),
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


CET1 = {"FY2025": 266352, "FY2024": 245034, "FY2023": 223772, "FY2022": 197516, "FY2021": 199873}
TOTAL_CAPITAL = {"FY2025": 334756, "FY2024": 318553, "FY2023": 276133, "FY2022": 267579, "FY2021": 270130}
RWA = {"FY2025": 1924184, "FY2024": 1571106, "FY2023": 1240666, "FY2022": 1231445, "FY2021": 1085219}
CET1_RATIO = {"FY2025": "13.8%", "FY2024": "15.6%", "FY2023": "18.0%", "FY2022": "16.0%", "FY2021": "18.4%"}
TCR = {"FY2025": "17.4%", "FY2024": "20.3%", "FY2023": "22.3%", "FY2022": "21.7%", "FY2021": "24.9%"}
LEVERAGE_RATIO = {"FY2025": "7.2%", "FY2024": "6.6%", "FY2023": "6.8%", "FY2022": "5.7%", "FY2021": "6.7%"}
LCR = {"FY2025": "234%", "FY2024": "327%", "FY2023": "271%", "FY2022": "254%", "FY2021": "276%"}
NSFR = {"FY2025": "166%", "FY2024": "160%", "FY2023": "151%", "FY2022": "130%"}

RWA_RESTATEMENT_NOTE = (
    "FY2022's Total RWA/CET1/Tier1/Total Capital ratios shown here are as originally published in the 2022 "
    "Pillar 3 Disclosures (RWA 1,231,445). The 2023 Pillar 3 Disclosures' own FY2022 comparative column restates "
    "this to 1,224,488 (footnoted 'amended for consistency of presentation') with correspondingly adjusted ratios "
    "(16.1% CET1/Tier1, 21.9% Total Capital) - the originally-published figure is used here, per project convention."
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CET1)], p3_sources())
metric("CET1 Ratio", "%", [("CET1 ratio", CET1_RATIO)], p3_sources(), note=RWA_RESTATEMENT_NOTE)
metric("Tier 1 Capital", "£'000 (= CET1 capital; no AT1 instruments)", [("Tier 1 capital", CET1)], p3_sources())
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CET1_RATIO)], p3_sources())
metric("Total Capital", "£'000", [("Total capital", TOTAL_CAPITAL)], p3_sources())
metric("Total Capital Ratio", "%", [("Total capital ratio", TCR)], p3_sources(), note=RWA_RESTATEMENT_NOTE)
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", RWA)], p3_sources(),
       note="See CET1 Ratio sheet for the FY2022 restatement note.")

# ---------------------------------------------------------------
# RWA Breakdown: none of the 5 years' Pillar 3 Disclosures contain an
# RWA-by-risk-category table (UK OV1 or equivalent) - each document only
# carries the UK KM1 Key Metrics table and (from FY2025) a UK CC1 own-funds
# composition table, both single-figure/own-funds disclosures, no category
# split - confirmed by reading each document in full.
# ---------------------------------------------------------------
bw.add_rwa_breakdown_sheet(
    title="British Arab Commercial Bank PLC — RWA Breakdown",
    subtitle="Not publicly disclosed at this granularity in any of the 5 years - see note below.",
    rows=[("DATA", "RWA by risk category", {y: "Not publicly disclosed" for y in YEARS})],
    sources_text=p3_sources(
        extra="None of the 5 years' Pillar 3 Disclosures (each checked in full) contain an RWA-by-risk-category "
              "breakdown table - only the single Total risk-weighted exposure amount figure shown on the Total "
              "RWAs sheet."
    ),
    first_col_width=54,
    source_height=190,
)
metric("Leverage Ratio", "%", [("Leverage ratio", LEVERAGE_RATIO)], p3_sources())
metric("LCR", "%", [("Liquidity coverage ratio (12-month average)", LCR)], p3_sources())
metric("NSFR", "%", [("NSFR ratio (4-quarter average)", NSFR)], p3_sources(
    extra="NSFR not applicable/disclosed for FY2021 - the NSFR reporting requirement and KM1 template line were "
          "new from FY2022; the FY2021 comparative column in the 2022 Pillar 3 Disclosures itself states 'N/A'."))

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "Not found in any of the 5 Annual Reports or Pillar 3 Disclosures checked - not "
                             "asserted as an explicit exemption, just absent from every source."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 3318750, "FY2024": 3343466, "FY2023": 3001927, "FY2022": 3194745, "FY2021": 2782543}),
        ("Loans and advances to customers", {"FY2025": 353562, "FY2024": 387260, "FY2023": 388567, "FY2022": 463780, "FY2021": 484536}),
        ("Deposits from banks + other deposits",
         {"FY2025": 2938773, "FY2024": 2977572, "FY2023": 2659678, "FY2022": 2882233, "FY2021": 2481506}),
        ("Total equity", {"FY2025": 278340, "FY2024": 257612, "FY2023": 232578, "FY2022": 207266, "FY2021": 210286}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income before allowance for credit losses",
         {"FY2025": 92763, "FY2024": 98650, "FY2023": 87856, "FY2022": 57433, "FY2021": 41723}),
        ("Administrative expenses",
         {"FY2025": -64363, "FY2024": -62082, "FY2023": -53594, "FY2022": -42031, "FY2021": -38763}),
        ("Profit for the year",
         {"FY2025": 24127, "FY2024": 28755, "FY2023": 27875, "FY2022": 15100, "FY2021": 13035}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Total equity", {"FY2025": 278340, "FY2024": 257612, "FY2023": 232578, "FY2022": 207266, "FY2021": 210286}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities",
         {"FY2025": 124138, "FY2024": 227828, "FY2023": -286411, "FY2022": -120744, "FY2021": 189594}),
        ("Net cash used in investing activities",
         {"FY2025": -1537, "FY2024": -820, "FY2023": -8524, "FY2022": -1094, "FY2021": -814}),
        ("Net cash used in financing activities",
         {"FY2025": -6477, "FY2024": -5055, "FY2023": -5417, "FY2022": -8771, "FY2021": -191}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 718577, "FY2024": 604467, "FY2023": 372940, "FY2022": 700795, "FY2021": 766720}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TCR),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BRITISH ARAB COMMERCIAL BANK FINANCIALS.xlsx")
