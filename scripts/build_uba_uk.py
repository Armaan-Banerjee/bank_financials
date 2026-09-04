import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023"}

# ---------------------------------------------------------------
# FX conversion (United Bank for Africa (UK) Limited reports in USD; converting
# to £ per this project's established FX methodology - see build_smbc.py /
# build_zenith.py precedent). Same calendar years as Zenith Bank UK, so the
# same Bank of England GBP/USD spot/average rates apply (£1 = $X, via
# poundsterlinglive.com's published BoE archive).
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2020": 1.3661,  # 31 Dec 2020 - only used for FY2021's opening cash balance
    "FY2021": 1.3521,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
}
FX_AVG = {
    "FY2021": 1.3752,
    "FY2022": 1.2362,
    "FY2023": 1.2439,
    "FY2024": 1.2782,
}


def flow(usd_000s):
    """Flow (cash flow statement line item) figures, £'000, at that year's
    average rate. UBA UK's own source already prints figures in US$'000, so
    (unlike build_zenith.py, whose source printed whole dollars) there's no
    extra /1000 here - dividing US$'000 by the rate gives £'000 directly."""
    return {y: round(v / FX_AVG[y], 1) for y, v in usd_000s.items()}


def stock(usd_000s):
    """Point-in-time (balance/capital) figures, £'000, at that year's period-end spot rate."""
    return {y: round(v / FX_SPOT[y], 1) for y, v in usd_000s.items()}


def opening_cash(usd_000s):
    """Opening cash balance, £'000 - uses the PRIOR year's period-end spot rate (it's the
    same balance as that prior year's closing figure, so must convert identically)."""
    return {y: round(v / FX_SPOT[PREV_YEAR[y]], 1) for y, v in usd_000s.items()}

# ---------------------------------------------------------------
# Source documents
# ---------------------------------------------------------------
AR2024_URL = "https://www.ubauk.com/wp-content/uploads/sites/29/2025/07/UBA-UK-2024-AR-1.pdf"
AR2022_URL = "https://www.ubauk.com/wp-content/uploads/sites/29/2023/09/UBA-UK-FIN-A-Ann-Rpt-and-Accts-31-Dec-2022.pdf"

P3_2024_URL = "https://www.ubauk.com/wp-content/uploads/sites/29/2026/05/UBA-UK-Pillar-3-Disclosures-31-Dec-2024.pdf"
P3_2022_URL = "https://www.ubauk.com/wp-content/uploads/sites/29/2023/08/UBA-UK-Pillar-3-Disclosures-31-Dec-2022_final-clean-trotter-comments.1-1.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: United Bank for Africa (UK) Limited (Companies House 03104974, FRN 695048) is a UK subsidiary of "
    "United Bank for Africa Plc (Nigeria). Unlike several other foreign-subsidiary banks in this workbook series "
    "(ICICI Bank UK, Philippine National Bank Europe, Citibank UK, State Bank of India UK), it prepares full IFRS "
    "financial statements with a genuine Statement of Cash Flows every year - no FRS 101/102 cash-flow exemption "
    "applies. The Bank's Own Funds consist entirely of Common Equity Tier 1 (CET1) capital (no AT1 or Tier 2 "
    "instruments), so CET1 capital = Tier 1 capital = Total capital in every year shown. No FY2025 Annual Report or "
    "Pillar 3 disclosure has been published yet (as of this workbook's build date), so this workbook covers "
    "FY2021-FY2024 only (4 years) rather than the usual 5."
)

FX_NOTE = (
    "FX CONVERSION NOTE: United Bank for Africa (UK) Limited reports in US Dollars (its functional currency, per "
    "its own foreign currency risk note - 'Revenues, assets and liabilities are primarily in the functional "
    "currency US dollar'). This workbook converts every $ amount to £ for consistency with the rest of this "
    "series, following the same methodology established for SMBC Bank International plc and Zenith Bank (UK) "
    "Limited: point-in-time/balance figures (capital, RWA, leverage exposure, HQLA, cash balances) use the Bank "
    "of England GBP/USD SPOT rate as at that fiscal year-end (31 December); flow figures (every cash flow "
    "statement line item) use the AVERAGE of Bank of England rates over that calendar year - both via "
    "poundsterlinglive.com's published Bank of England archive, and identical to the rates used for Zenith Bank "
    "UK since both banks share the same 31 December fiscal year-end. Rates used (£1 = $X): 31 Dec 2020 spot "
    "1.3661 (FY2021 opening cash only); FY2021 spot 1.3521 / average 1.3752; FY2022 spot 1.2097 / average "
    "1.2362; FY2023 spot 1.2732 / average 1.2439; FY2024 spot 1.2515 / average 1.2782. All % ratios (CET1/Tier "
    "1/Total Capital/Leverage/LCR/NSFR ratios) are shown EXACTLY as reported in USD and were NOT converted - a "
    "ratio is dimensionless and currency-invariant. Because stocks and flows are converted at different rates, "
    "the cash flow statement includes an explicit 'Effect of GBP/USD translation' reconciling line so opening + "
    "all flows + this line = closing exactly in £ terms - this line is purely an artefact of £ translation and "
    "has no bearing on the Bank's underlying USD results. This conversion was not explicitly requested for this "
    "bank (unlike SMBC) - applied for consistency with the rest of the series, following the same call already "
    "confirmed for Zenith Bank UK; flag if £'000 rather than the Bank's native US$'000 presentation is not what's "
    "wanted here."
)

RECONCILIATION_NOTE = (
    "RECONCILIATION NOTE: the FY2022 Annual Report's Statement of Cash Flows shows the FY2022 closing balance as "
    "US$31,392k, but a supplementary 'cash and cash equivalent reconciliation' note in that same report nets this "
    "down to US$31,354k (deducting a US$38k expected credit loss allowance) - and it is this US$31,354k figure "
    "that the FY2023 Annual Report actually carries forward as its own FY2023 opening balance. Both figures are "
    "used exactly as each report presents them (FY2022's own closing balance from its primary statement; FY2023's "
    "own opening balance from its primary statement) rather than forcing them to match, so there is a small "
    "(~£31k) presentational discontinuity between the FY2022 closing and FY2023 opening £ balances shown here - "
    "not a data error, the underlying US$38k difference is fully explained by the source reconciliation note."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are United Bank for Africa (UK) Limited's own Statement of Cash Flows (converted from "
    "USD to £, see FX conversion note below):\n"
    f"FY2024 & FY2023: Annual Report and Accounts 2024, p.50 (Statements of Cash Flows) - {AR2024_URL}\n"
    f"FY2022 & FY2021: Annual Report and Accounts 2022, p.39 (Statement of Cash Flows) - {AR2022_URL}\n"
    "Note: presentation differs between report vintages - FY2024/FY2023 separately disclose 'Change in due from "
    "banks', a combined FVTPL subscription/redemption line, and split FVOCI/amortised-cost gain-on-derecognition "
    "lines; FY2022/FY2021 instead show a single combined 'Loss on disposal of investments at FVOCI' line and "
    "separate FVTPL/amortised-cost purchase and proceeds lines. Each year's own as-reported line items and labels "
    "are preserved rather than forced into a common shape; blank cells indicate that year's report did not "
    "disclose that specific split.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + RECONCILIATION_NOTE
)


STATEMENTS_SOURCES = (
    "Sources - all figures are United Bank for Africa (UK) Limited's own primary financial statements (converted "
    "from USD to £, see FX conversion note below):\n"
    f"FY2024 & FY2023: Annual Report and Accounts 2024, p.47 (Statement of Profit or Loss and Other Comprehensive "
    f"Income), p.48 (Statement of Financial Position) - {AR2024_URL}\n"
    f"FY2022 & FY2021: Annual Report and Accounts 2022, p.36 (Statement of Comprehensive Income), p.37 (Statement "
    f"of Financial Position) - {AR2022_URL}\n\n"
    "Presentation differs between report vintages: FY2024/FY2023 split interest income into 'calculated using the "
    "effective interest method' and 'other interest and similar income' lines and separately disclose 'Due from "
    "banks', a Deferred tax asset, and a Current tax asset; FY2022/FY2021 show a single 'Interest receivable and "
    "similar income' line, no 'Due from banks' split, and a Deferred TAX LIABILITY instead (FY2021 only, £nil "
    "FY2022) rather than an asset. Each year's own as-reported line items and labels are preserved rather than "
    "forced into a common shape; blank cells indicate that year's report did not disclose that specific split.\n\n"
    "OCI DISCREPANCY NOTE: FY2024's Statement of Profit or Loss and OCI shows 4 separate OCI detail lines summing "
    "to the stated 'Total items that may be reclassified to profit or loss' ($1,086k + $740k + $618k + $349k = "
    "$2,793k) - but the Statement of Changes in Equity's own FY2024 roll-forward shows a DIFFERENT 3-line OCI "
    "component split ($1,435k fair value change + $740k reclassification + $618k ECL allowance change = the same "
    "$2,793k total). Both statements' totals agree exactly ($2,793k / £2,185.1k), but their component breakdowns "
    "do not reconcile line-for-line - an unresolved labelling inconsistency in the source document itself, "
    "reproduced here exactly as each statement presents it rather than silently reconciled or picked one over "
    "the other.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

EQUITY_SOURCES = (
    "Sources - United Bank for Africa (UK) Limited's own Statement of Changes in Equity, presented in the Bank's "
    "native US$'000 (NOT converted to £, unlike every other sheet in this workbook):\n"
    f"FY2024 & FY2023: Annual Report and Accounts 2024, p.49 (Statement of Changes in Equity) - {AR2024_URL}\n"
    f"FY2022 & FY2021: Annual Report and Accounts 2022, p.38 (Statement of Changes in Equity) - {AR2022_URL}\n\n"
    "WHY NOT CONVERTED: unlike the Balance Sheet (a point-in-time snapshot, convertible at that date's spot rate) "
    "and the Profit & Loss (a single year's flow, convertible at that year's average rate), this sheet is a "
    "multi-year chronological ROLL-FORWARD chaining 4 years of opening/movement/closing balances together. "
    "Converting each balance at its own date's spot rate while converting each movement at that year's average "
    "rate would introduce a distinct, unexplained 'FX translation' gap into every reserve column at every year "
    "boundary (verified: gaps of several hundred to several thousand £'000 per column per year, driven entirely "
    "by USD/GBP rate movement, not by any real accounting entry) - materially different from the Cash Flow "
    "Statement sheet's single-line, whole-statement translation plug, and not cleanly representable as one "
    "reconciling row across 5 equity-component columns. Rather than fabricate a misleadingly precise-looking £ "
    "conversion that would obscure this, the ladder is shown in the Bank's own native USD, exactly as reported, "
    "on every row. Convert any individual balance to £ using this sheet's own year-end spot rate (see FX "
    "conversion note on the Cash Flow Statement sheet) if needed for cross-reference.\n\n"
    "RECONCILIATION NOTE: FY2022, FY2023, and FY2024 all tie exactly to that year's own Balance Sheet Total "
    "equity and to the next year's opening balance. FY2021's closing balance as shown in this equity statement "
    "($39,492k total; Accumulated losses $(19,931)k; Fair value + Hedging reserve $(1,024)k combined) differs "
    "from the FY2021 Balance Sheet's own independently-stated figures (Accumulated losses $(19,930)k; Other "
    "reserves $(1,025)k) by exactly $1k in each of two lines (Total equity itself, $39,492k, matches exactly) - "
    "a genuine $1k rounding artefact between the two primary statements in the FY2022 Annual Report, reproduced "
    "exactly as each statement states rather than forced to tie.\n\n"
    + ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - United Bank for Africa (UK) Limited's own credit risk / ECL disclosures (converted from USD to £ "
    "where a $ amount; see FX conversion note on the Cash Flow Statement sheet):\n"
    f"FY2024 & FY2023: Annual Report and Accounts 2024, p.59 (ECL scenario/stage summary table), p.85-86 "
    f"(maximum exposure to credit risk by stage and credit rating) - {AR2024_URL}\n"
    f"FY2022 & FY2021: Annual Report and Accounts 2022, p.44 (ECL scenario note), p.54 (Ghana Stage 3 exposure "
    f"note) - {AR2022_URL}\n\n"
    "GRANULARITY NOTE: UBA UK is a wholesale/treasury bank with an essentially nil customer loan book (£0-2.6m "
    "across all 4 years) - its real credit risk sits in interbank placements and investment securities, so this "
    "sheet is built from the Bank's own IFRS 9 stage-tagged ECL disclosure across ALL financial assets subject to "
    "ECL (cash, due from banks, loans and advances to banks/customers, debt instruments, investment securities at "
    "FVOCI, financial commitments), not a conventional retail/commercial loan book split. FY2024/FY2023 disclose "
    "a full stage-by-stage gross exposure and ECL allowance table (summed across all asset classes here); "
    "FY2022/FY2021's Annual Report describes the same 3-stage ECL methodology only QUALITATIVELY, with no "
    "consolidated numeric stage-tagged table anywhere in the document (confirmed via full review of the credit "
    "risk note and all ECL-related notes) - a genuine confirmed non-disclosure at this granularity, not an access "
    "gap. FY2022's one disclosed Stage 3 item (a Ghanaian sovereign Eurobond, $5m nominal / $4m carrying amount, "
    "following a Fitch default downgrade) and FY2021's explicit 'Stage 3: Nil' are shown as the only stage-level "
    "data points available for those two years.\n\n"
    + ENTITY_NOTE
)


def p3_sources(page_24="10", page_22="9"):
    return (
        "Sources - United Bank for Africa (UK) Limited Pillar 3 Disclosures (Key Metrics table), converted from "
        "USD to £ where a $ amount (see FX conversion note on the Cash Flow Statement sheet; % ratios are "
        "unconverted):\n"
        f"FY2024 & FY2023: Pillar 3 Disclosures - 31 Dec 2024, p.{page_24} (Section 4, Key Metrics) - {P3_2024_URL}\n"
        f"FY2022 & FY2021: Pillar 3 Disclosures - 31 Dec 2022, p.{page_22} (Section 4, Key Metrics) - {P3_2022_URL}"
    )


bw = BankWorkbook(bank_name="United Bank for Africa (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="805B10")

# ---------------------------------------------------------------
# Sheet: Balance Sheet (£'000, converted via stock() - a point-in-time snapshot per year)
# ---------------------------------------------------------------
bs_rows_usd = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2024": 102328, "FY2023": 91250, "FY2022": 31354, "FY2021": 55425}),
    ("DATA", "Due from banks", {"FY2024": 86235}),
    ("DATA", "Loans and advances to banks", {"FY2024": 88969, "FY2023": 363448, "FY2022": 418231, "FY2021": 326606}),
    ("DATA", "Loans and advances to customers", {"FY2024": 0, "FY2023": 2561}),
    ("DATA", "Investment securities", {"FY2024": 181213, "FY2023": 147377, "FY2022": 140253, "FY2021": 133829}),
    ("DATA", "Property, plant and equipment", {"FY2024": 1740, "FY2023": 1600, "FY2022": 1831, "FY2021": 2399}),
    ("DATA", "Intangible assets", {"FY2024": 1425, "FY2023": 1616, "FY2022": 1916, "FY2021": 2066}),
    ("DATA", "Current tax asset", {"FY2024": 264}),
    ("DATA", "Other assets", {"FY2024": 5872, "FY2023": 3805, "FY2022": 2253, "FY2021": 2212}),
    ("DATA", "Deferred tax asset", {"FY2024": 1656}),
    ("TOTAL", "Total assets", {"FY2024": 469702, "FY2023": 611657, "FY2022": 595838, "FY2021": 522537}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2024": 373403, "FY2023": 493214, "FY2022": 539010, "FY2021": 476448}),
    ("DATA", "Deposits from customers", {"FY2024": 9836, "FY2023": 37380, "FY2022": 4815, "FY2021": 17}),
    ("DATA", "Deferred tax liability", {"FY2021": 67}),
    ("DATA", "Corporation tax liability", {"FY2023": 176, "FY2022": 669}),
    ("DATA", "Other liabilities", {"FY2024": 7154, "FY2023": 5820, "FY2022": 4941, "FY2021": 6513}),
    ("TOTAL", "Total liabilities", {"FY2024": 390393, "FY2023": 536590, "FY2022": 549435, "FY2021": 483045}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2024": 72246, "FY2023": 72246, "FY2022": 60246, "FY2021": 60246}),
    ("DATA", "Share premium account", {"FY2024": 201, "FY2023": 201, "FY2022": 201, "FY2021": 201}),
    ("DATA", "Retained earnings/(Accumulated losses)", {"FY2024": 7292, "FY2023": 5843, "FY2022": -8480, "FY2021": -19930}),
    ("DATA", "Other reserves", {"FY2024": -430, "FY2023": -3223, "FY2022": -5564, "FY2021": -1025}),
    ("TOTAL", "Total equity", {"FY2024": 79309, "FY2023": 75067, "FY2022": 46403, "FY2021": 39492}),
    ("TOTAL", "Total liabilities and equity", {"FY2024": 469702, "FY2023": 611657, "FY2022": 595838, "FY2021": 522537}),
]
bs_rows = [(kind, label, ({} if kind == "SECTION" else stock(usd))) for kind, label, usd in bs_rows_usd]

bw.add_balance_sheet_sheet(
    title="United Bank for Africa (UK) Limited — Statement of Financial Position",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=420,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (£'000, converted via flow() - a single year's flow per column)
# ---------------------------------------------------------------
is_rows_usd = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income calculated using the effective interest method", {"FY2024": 43575, "FY2023": 48839}),
    ("DATA", "Other interest and similar income", {"FY2024": 1627, "FY2023": 1403}),
    ("DATA", "Interest receivable and similar income", {"FY2022": 41116, "FY2021": 16513}),
    ("DATA", "Interest expense", {"FY2024": -19477, "FY2023": -21553, "FY2022": -16927, "FY2021": -9045}),
    ("TOTAL", "Net interest income", {"FY2024": 25725, "FY2023": 28689, "FY2022": 24189, "FY2021": 7468}),
    ("DATA", "Fee and commission income", {"FY2024": 405, "FY2023": 558, "FY2022": 1763, "FY2021": 1624}),
    ("DATA", "Provision for expected credit losses", {"FY2024": -33, "FY2023": -246, "FY2022": -3894, "FY2021": -1288}),
    ("DATA", "Net gains/(losses) on derecognition of debt instruments at amortised cost", {"FY2024": 1047, "FY2023": -124}),
    ("DATA", "Net gains on derecognition of debt instruments at FVOCI", {"FY2024": 204, "FY2023": 12}),
    ("DATA", "Loss on disposal of investments at FVOCI", {"FY2022": -343, "FY2021": -18}),
    ("DATA", "Other income", {"FY2024": 732, "FY2023": 2281, "FY2022": 676, "FY2021": 1114}),
    ("TOTAL", "Operating income", {"FY2024": 28080, "FY2023": 31170, "FY2022": 22391, "FY2021": 8900}),
    ("DATA", "Staff costs", {"FY2024": -9432, "FY2023": -7728, "FY2022": -7106, "FY2021": -5680}),
    ("DATA", "Administrative expenses", {"FY2024": -4894, "FY2023": -3875, "FY2022": -2894, "FY2021": -2008}),
    ("DATA", "Other operating (expenses)/income", {"FY2024": -55, "FY2023": -889, "FY2022": 418, "FY2021": -1494}),
    ("DATA", "Depreciation and amortisation", {"FY2024": -780, "FY2023": -783, "FY2022": -756, "FY2021": -765}),
    ("TOTAL", "Profit/(loss) before taxation", {"FY2024": 12919, "FY2023": 17895, "FY2022": 12053, "FY2021": -1047}),
    ("DATA", "Income tax (expense)/credit", {"FY2024": -1470, "FY2023": -3572, "FY2022": -602, "FY2021": 0}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2024": 11449, "FY2023": 14323, "FY2022": 11451, "FY2021": -1047}),
    ("SECTION", "Other comprehensive income/(expense)", {}),
    ("DATA", "Items that may be reclassified to profit or loss (as printed - see OCI discrepancy note)", {"FY2024": 1086, "FY2023": 2341}),
    ("DATA", "Net change in fair value of investment securities at FVOCI", {"FY2024": 740}),
    ("DATA", "Net change in allowances for expected credit losses of investment securities at FVOCI", {"FY2024": 618}),
    ("DATA", "Income tax related to the above", {"FY2024": 349}),
    ("DATA", "Hedging derivative unrealised gain/(loss)", {"FY2022": 0, "FY2021": 172}),
    ("DATA", "Net loss on financial assets measured at FVOCI", {"FY2022": -4540, "FY2021": -841}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2024": 14242, "FY2023": 16664, "FY2022": 6911, "FY2021": -1716}),
]
is_rows = [(kind, label, ({} if kind == "SECTION" else flow(usd))) for kind, label, usd in is_rows_usd]

bw.add_income_statement_sheet(
    title="United Bank for Africa (UK) Limited — Statement of Profit or Loss and Other Comprehensive Income",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=is_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=78,
    source_height=420,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity (US$'000, NOT converted - see EQUITY_SOURCES note)
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Share premium account", "Fair value & hedging reserve", "Retained earnings/(Accumulated losses)", "Total equity"]

equity_rows = [
    ("TOTAL", "Balance as at 1 January 2021", (60246, 201, -355, -18884, 41208)),
    ("DATA", "Loss for the year", (None, None, None, -1047, -1047)),
    ("DATA", "Other comprehensive expense (hedging + FVOCI)", (None, None, -669, None, -669)),
    ("TOTAL", "Balance at 31 December 2021 / 1 January 2022", (60246, 201, -1024, -19931, 39492)),
    ("DATA", "Profit for the year", (None, None, None, 11451, 11451)),
    ("DATA", "Other comprehensive expense (FVOCI)", (None, None, -4540, None, -4540)),
    ("TOTAL", "Balance at 31 December 2022 / 1 January 2023", (60246, 201, -5564, -8480, 46403)),
    ("DATA", "Issuance of share capital", (12000, None, None, None, 12000)),
    ("DATA", "Profit for the year", (None, None, None, 14323, 14323)),
    ("DATA", "Net change in fair value of financial instruments at FVOCI", (None, None, 2341, None, 2341)),
    ("TOTAL", "Balance at 31 December 2023 / 1 January 2024", (72246, 201, -3223, 5843, 75067)),
    ("DATA", "Profit for the year", (None, None, None, 11449, 11449)),
    ("DATA", "Total items that may be reclassified to profit or loss (OCI, net)", (None, None, 2793, None, 2793)),
    ("DATA", "Dividends", (None, None, None, -10000, -10000)),
    ("TOTAL", "Balance at 31 December 2024", (72246, 201, -430, 7292, 79309)),
]

bw.add_equity_changes_sheet(
    title="United Bank for Africa (UK) Limited — Statement of Changes in Equity",
    subtitle="US$'000 (NOT converted to £ - see source note at bottom for why).",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=52,
    source_height=460,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD '000, then converted via flow()/stock()/opening_cash())
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2024": 12919, "FY2023": 17895, "FY2022": 12053, "FY2021": -1047}),
    ("DATA", "Depreciation and amortisation", {"FY2024": 780, "FY2023": 783, "FY2022": 756, "FY2021": 765}),
    ("DATA", "Net gain/(loss) on derecognition of debt instruments measured at amortised cost", {"FY2024": -1047, "FY2023": 124}),
    ("DATA", "Net gain/(loss) on derecognition of debt instruments measured at FVOCI", {"FY2024": -204, "FY2023": -12}),
    ("DATA", "Loss on disposal of investments at FVOCI", {"FY2022": 343, "FY2021": 18}),
    ("DATA", "Other non-cash items included in profit before tax", {"FY2024": 93, "FY2023": -1366}),
    ("DATA", "Increase in other non-cash movements", {"FY2022": 4583, "FY2021": -201}),
    ("DATA", "Change in due from banks", {"FY2024": -86309}),
    ("DATA", "Change in loans and advances to banks", {"FY2024": 274189, "FY2023": 56239, "FY2022": -92501, "FY2021": -249404}),
    ("DATA", "Change in loans and advances to customers", {"FY2024": 2561, "FY2023": -2561}),
    ("DATA", "Change in other assets", {"FY2024": -2122, "FY2023": -1552, "FY2022": 737, "FY2021": -1228}),
    ("DATA", "Change in deposit from banks", {"FY2024": -119812, "FY2023": -45796, "FY2022": 62562, "FY2021": 287902}),
    ("DATA", "Change in deposit from customers", {"FY2024": -27544, "FY2023": 32565, "FY2022": 4798, "FY2021": -13452}),
    ("DATA", "Change/increase in other liabilities", {"FY2024": 1841, "FY2023": 973, "FY2022": -1251, "FY2021": 3115}),
    ("DATA", "Tax paid", {"FY2024": -3217, "FY2023": -4064}),
    ("TOTAL", "Net cash flows from/(used in) operating activities", {"FY2024": 52128, "FY2023": 53228, "FY2022": -7920, "FY2021": 26468}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2024": -546, "FY2023": -67}),
    ("DATA", "Purchase and sale of property, plant and equipment (net)", {"FY2022": -24}),
    ("DATA", "Purchase of intangible assets", {"FY2024": -207, "FY2023": -95, "FY2022": -229, "FY2021": -122}),
    ("DATA", "Payments for investment securities at FVOCI", {"FY2024": -75117, "FY2023": -9857, "FY2022": -4988, "FY2021": -86474}),
    ("DATA", "Net payment for subscription/redemption of investment securities at FVTPL", {"FY2024": -5961, "FY2023": -15621}),
    ("DATA", "Payments for investment securities at FVTPL", {"FY2022": -27044, "FY2021": -12502}),
    ("DATA", "Payments for investment securities at amortised cost", {"FY2022": -13533, "FY2021": -33135}),
    ("DATA", "Proceeds from sale of investment securities at FVOCI", {"FY2024": 32328, "FY2023": 17627, "FY2022": 17438, "FY2021": 73743}),
    ("DATA", "Proceeds from sale of investment securities at amortised cost", {"FY2024": 18662, "FY2023": 2038}),
    ("DATA", "Proceeds from sale of investment securities at FVTPL", {"FY2022": 12502, "FY2021": 2000}),
    ("DATA", "Proceeds from maturity of investment securities at amortised cost", {"FY2021": 41008}),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {"FY2024": -30841, "FY2023": -5975, "FY2022": -15878, "FY2021": -15482}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payments of lease liabilities", {"FY2024": -255, "FY2023": -235, "FY2022": -235, "FY2021": -283}),
    ("DATA", "Payments of interest on leases", {"FY2024": -9, "FY2023": -11}),
    ("DATA", "Dividend paid", {"FY2024": -10000}),
    ("DATA", "Proceeds from issuance of share capital", {"FY2023": 12000}),
    ("TOTAL", "Net cash flow (used in)/from financing activities", {"FY2024": -10264, "FY2023": 11754, "FY2022": -235, "FY2021": -283}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2024": 11023, "FY2023": 59007, "FY2022": -24033, "FY2021": 10703}),
    ("DATA", "Net foreign exchange difference", {"FY2024": 55, "FY2023": 889}),
    ("DATA", "Cash and cash equivalents at beginning of period", {"FY2024": 91250, "FY2023": 31354, "FY2022": 55425, "FY2021": 44722}),
    ("TOTAL", "Cash and cash equivalents at end of period", {"FY2024": 102328, "FY2023": 91250, "FY2022": 31392, "FY2021": 55425}),
]

# £ translation plug (see FX_NOTE): stocks (opening/closing) and flows (everything
# else) are converted at different rates, so the £ statement needs an explicit
# reconciling line to tie exactly. Computed as closing(£) - opening(£) - net
# change(£) - reported FX-effect line(£), per year (verified independently).
TRANSLATION_PLUG_GBP = {"FY2024": 1427.6, "FY2023": -2400.8, "FY2022": 4399.5, "FY2021": 471.9}

# convert: SECTION rows pass through unchanged; opening-cash row uses opening_cash();
# everything else (DATA/TOTAL) uses flow() - all cash flow statement figures are
# period flows/movements except the opening balance, which is a point-in-time carry-forward.
rows = []
for kind, label, usd in rows_usd:
    if kind == "SECTION":
        rows.append((kind, label, {}))
    elif label == "Cash and cash equivalents at beginning of period":
        rows.append((kind, label, opening_cash(usd)))
    elif label == "Cash and cash equivalents at end of period":
        # point-in-time balance, like the opening row - spot rate, not average
        rows.append((kind, label, stock(usd)))
    else:
        rows.append((kind, label, flow(usd)))
    if label == "Net foreign exchange difference":
        rows.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", TRANSLATION_PLUG_GBP))

bw.add_cash_flow_sheet(
    title="United Bank for Africa (UK) Limited — Statement of Cash Flows",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality (£'000, stock() for balances / flow() for the P&L ECL charge)
# ---------------------------------------------------------------
aq_rows = [
    ("SECTION", "Credit quality (IFRS 9 ECL by stage, all financial assets subject to ECL)", {}),
    ("DATA", "Total gross exposure subject to ECL", stock({"FY2024": 437778, "FY2023": 585061})),
    ("DATA", "Stage 1 ECL allowance", stock({"FY2024": 1774, "FY2023": 2805})),
    ("DATA", "Stage 2 ECL allowance", stock({"FY2024": 517, "FY2023": 956})),
    ("DATA", "Stage 3 ECL allowance", stock({"FY2024": 0, "FY2023": 2366})),
    ("DATA", "POCI ECL allowance", stock({"FY2024": 96, "FY2023": 0})),
    ("TOTAL", "Total ECL allowance", stock({"FY2024": 2387, "FY2023": 6127})),
    ("DATA", "ECL charge for the year (P&L)", flow({"FY2024": -33, "FY2023": -246, "FY2022": -3894, "FY2021": -1288})),
    ("DATA", "Stage 3 / non-performing gross exposure", stock({"FY2024": 0, "FY2023": 4418, "FY2022": 4000, "FY2021": 0})),
    ("DATA", "Coverage ratio (Total ECL allowance / total gross exposure)", {"FY2024": "0.55%", "FY2023": "1.05%"}),
    ("DATA", "Memo: Ghana sovereign Eurobond nominal value (FY2022 Stage 3 exposure)", stock({"FY2022": 5000})),
]

bw.add_asset_quality_sheet(
    title="United Bank for Africa (UK) Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="£'000, converted from USD - see source note at bottom. UBA UK is a wholesale/treasury bank with an essentially nil customer loan book; figures cover all financial assets subject to IFRS 9 ECL.",
    rows=aq_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=380,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=48, source_height=120)


CET1_TIER1_TOTAL_USD = {"FY2024": 78168.563, "FY2023": 60900.368, "FY2022": 36513.246, "FY2021": 38317.917}
RWA_USD = {"FY2024": 159390.258, "FY2023": 127932.133, "FY2022": 137833.765, "FY2021": 93272.286}
LEVERAGE_EXPOSURE_USD = {"FY2024": 483630.135, "FY2023": 626525.876, "FY2022": 613889.918, "FY2021": 573663.805}
HQLA_USD = {"FY2024": 110851.365, "FY2023": 100502.936, "FY2022": 91179.217, "FY2021": 92773.320}
NET_CASH_OUTFLOWS_USD = {"FY2024": 31422.835, "FY2023": 43919.581, "FY2022": 40678.515, "FY2021": 25667.620}
NSFR_ASF_USD = {"FY2024": 122954.356, "FY2023": 138256.344, "FY2022": 167040.341, "FY2021": 152043.116}
NSFR_RSF_USD = {"FY2024": 67305.335, "FY2023": 90321.851, "FY2022": 92117.147, "FY2021": 102891.413}

metric("CET1 Capital", "£'000 (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", stock(CET1_TIER1_TOTAL_USD))], p3_sources())
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {"FY2024": "49.04%", "FY2023": "47.60%", "FY2022": "23.27%", "FY2021": "33.56%"})], p3_sources())
metric("Tier 1 Capital", "£'000 (conv. from USD)", [("Tier 1 capital", stock(CET1_TIER1_TOTAL_USD))], p3_sources(),
       note="Equal to CET1 capital in every year - the Bank holds no Additional Tier 1 (AT1) instruments.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2024": "49.04%", "FY2023": "47.60%", "FY2022": "23.27%", "FY2021": "33.56%"})], p3_sources())
metric("Total Capital", "£'000 (conv. from USD)", [("Total capital", stock(CET1_TIER1_TOTAL_USD))], p3_sources(),
       note="Equal to CET1/Tier 1 capital in every year - the Bank holds no AT1 or Tier 2 instruments.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2024": "49.04%", "FY2023": "47.60%", "FY2022": "23.27%", "FY2021": "33.56%"})], p3_sources())
metric("Total RWAs", "£'000 (conv. from USD)", [("Total risk-weighted exposure amount", stock(RWA_USD))], p3_sources())

bw.add_rwa_breakdown_sheet(
    title="United Bank for Africa (UK) Limited — RWA Breakdown",
    subtitle="Not publicly disclosed.",
    rows=[("DATA", "RWA Breakdown", {y: "Not publicly disclosed" for y in YEARS})],
    sources_text=p3_sources() + "\n\nNo UK OV1 (or equivalent RWA-by-category) template was found in either "
                 "Pillar 3 Disclosures document - only a single Total RWA figure is disclosed in each year's Key "
                 "Metrics table (see Total RWAs sheet), with no risk-category breakdown (credit risk, market risk, "
                 "operational risk, etc.) anywhere in either document. Confirmed via full review of both Pillar 3 "
                 "reports, not an access gap.",
    first_col_width=54,
    source_height=140,
    unit_suffix="",
)

metric(
    "Leverage Ratio", "£'000 / % (conv. from USD)",
    [
        ("Total exposure measure excluding claims on central banks", stock(LEVERAGE_EXPOSURE_USD)),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2024": "16.16%", "FY2023": "9.72%", "FY2022": "6%", "FY2021": "7%"}),
    ],
    p3_sources(),
    note="FY2022/FY2021 leverage ratios are printed to whole-percent precision only in the source document "
         "(6% and 7%), unlike FY2024/FY2023's two-decimal precision - transcribed exactly as shown, not rounded "
         "further or given false precision.",
)

metric(
    "LCR", "£'000 / % (conv. from USD)",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", stock(HQLA_USD)),
        ("Total net cash outflows, adjusted value", stock(NET_CASH_OUTFLOWS_USD)),
        ("Liquidity Coverage Ratio (%)", {"FY2024": "352.77%", "FY2023": "228.83%", "FY2022": "224.15%", "FY2021": "361.44%"}),
    ],
    p3_sources(),
)

metric(
    "NSFR", "£'000 / % (conv. from USD)",
    [
        ("Total available stable funding", stock(NSFR_ASF_USD)),
        ("Total required stable funding", stock(NSFR_RSF_USD)),
        ("NSFR ratio (%)", {"FY2024": "182.68%", "FY2023": "153.07%", "FY2022": "181.33%", "FY2021": "147.77%"}),
    ],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "No MREL disclosure (numeric or qualitative) or UK KM2 template found anywhere in any "
                             "year's Pillar 3 report - not explicitly stated as an exemption, but consistent with "
                             "the Bank's small size relative to typical MREL-in-scope thresholds."})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
cf_totals_usd = {
    "Net cash flows from/(used in) operating activities": {"FY2024": 52128, "FY2023": 53228, "FY2022": -7920, "FY2021": 26468},
    "Net cash flows from/(used in) investing activities": {"FY2024": -30841, "FY2023": -5975, "FY2022": -15878, "FY2021": -15482},
    "Net cash flow (used in)/from financing activities": {"FY2024": -10264, "FY2023": 11754, "FY2022": -235, "FY2021": -283},
}
cf_close_usd = {"FY2024": 102328, "FY2023": 91250, "FY2022": 31392, "FY2021": 55425}

bw.add_overview_sheet(
    cash_flow_totals=[(label, flow(vals)) for label, vals in cf_totals_usd.items()]
                      + [("Cash and cash equivalents at end of period", stock(cf_close_usd))],
    cash_flow_unit="£'000",
    balance_sheet_totals=[
        ("Total assets", stock({"FY2024": 469702, "FY2023": 611657, "FY2022": 595838, "FY2021": 522537})),
        ("Loans and advances to customers", stock({"FY2024": 0, "FY2023": 2561})),
        ("Deposits from customers", stock({"FY2024": 9836, "FY2023": 37380, "FY2022": 4815, "FY2021": 17})),
        ("Total equity", stock({"FY2024": 79309, "FY2023": 75067, "FY2022": 46403, "FY2021": 39492})),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income", flow({"FY2024": 28080, "FY2023": 31170, "FY2022": 22391, "FY2021": 8900})),
        ("Total operating expense", flow({"FY2024": -15161, "FY2023": -13275, "FY2022": -10338, "FY2021": -9947})),
        ("Profit/(loss) for the year", flow({"FY2024": 11449, "FY2023": 14323, "FY2022": 11451, "FY2021": -1047})),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2024": 75067, "FY2023": 46403, "FY2022": 39492, "FY2021": 41208}),
        ("Total comprehensive income/(loss) for the year", {"FY2024": 14242, "FY2023": 16664, "FY2022": 6911, "FY2021": -1716}),
        ("Other equity movements, net (issuances/dividends)", {"FY2024": -10000, "FY2023": 12000, "FY2022": 0, "FY2021": 0}),
        ("Closing equity", {"FY2024": 79309, "FY2023": 75067, "FY2022": 46403, "FY2021": 39492}),
    ],
    equity_changes_unit="US$'000 (native, not converted - see Statement of Changes in Equity source note)",
    ratios=[
        ("CET1 Ratio", {"FY2024": "49.04%", "FY2023": "47.60%", "FY2022": "23.27%", "FY2021": "33.56%"}),
        ("Tier 1 Ratio", {"FY2024": "49.04%", "FY2023": "47.60%", "FY2022": "23.27%", "FY2021": "33.56%"}),
        ("Total Capital Ratio", {"FY2024": "49.04%", "FY2023": "47.60%", "FY2022": "23.27%", "FY2021": "33.56%"}),
        ("Leverage Ratio", {"FY2024": "16.16%", "FY2023": "9.72%", "FY2022": "6%", "FY2021": "7%"}),
        ("LCR", {"FY2024": "352.77%", "FY2023": "228.83%", "FY2022": "224.15%", "FY2021": "361.44%"}),
        ("NSFR", {"FY2024": "182.68%", "FY2023": "153.07%", "FY2022": "181.33%", "FY2021": "147.77%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation. Balance Sheet/Profit & Loss/Cash Flow £ figures are converted from the Bank's native USD "
         "reporting (see Cash Flow Statement sheet's FX conversion note) - this conversion was not explicitly "
         "requested for this bank but applied for consistency with the rest of the series, following the same "
         "call already confirmed for Zenith Bank UK. The Statement of Changes in Equity summary above is shown "
         "in the Bank's native US$'000 (NOT converted), matching that detail sheet - see its own source note for "
         "why. No FY2025 Annual Report or Pillar 3 disclosure has been published yet, so this workbook covers "
         "FY2021-FY2024 (4 years) rather than the usual 5.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/UBA UK FINANCIALS.xlsx")
