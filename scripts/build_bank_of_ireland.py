import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, all 12mo to 31 Dec

AR2025_URL = "https://www.bankofirelanduk.com/app/uploads/annual-report_2025_boi-uk.pdf"
AR2024_URL = "https://investorrelations.bankofireland.com/app/uploads/Annual-Report-UK-2024-web-version.pdf"
AR2023_URL = "https://investorrelations.bankofireland.com/app/uploads/BOI-UKPLC-2023-Annual-Report.pdf"
AR2022_URL = "https://www.bankofirelanduk.com/app/uploads/BOI-UK-Annual-Report-2022.pdf"
AR2021_URL = "https://www.bankofirelanduk.com/app/uploads/2017/04/Annual-Report-UK-2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank of Ireland (UK) Plc (Companies House 07022885, FRN 512956) is a wholly owned subsidiary of "
    "Bank of Ireland Group plc (Ireland). Figures throughout are the CONSOLIDATED GROUP basis (not the standalone "
    "parent-only 'Bank' accounts, which separately take the FRS 101/IAS 7 cash-flow-statement exemption available "
    "to a qualifying entity - the consolidated Group accounts do not take that exemption and contain a full "
    "Consolidated cash flow statement every year). Bank of Ireland (UK) Plc stopped publishing a standalone Pillar "
    "3 disclosure document after the 2020 financial year; from FY2021 onward, its capital/leverage/liquidity/MREL "
    "ratios are instead disclosed directly within the Annual Report's Risk Management Report ('2.2 Funding and "
    "liquidity risk' and '3 Capital management' sections), which is what is cited below. Those sections give a full "
    "capital composition table (CET1/Tier 1/Total capital/RWA/leverage exposure) and headline LCR/NSFR/MREL ratios, "
    "but - unlike a formal Pillar 3 KM1 template - do not publish the underlying £m components behind the LCR "
    "(HQLA, net cash outflows) or NSFR (available/required stable funding) ratios, or a numeric MREL resources "
    "breakdown; only the headline percentages are available for FY2021-FY2025."
)

BASIS_NOTE = (
    "RATIO BASIS NOTE: CET1 ratio and Leverage ratio are quoted exactly as stated in each year's Annual Report, on "
    "the 'fully loaded' basis (i.e. excluding IFRS 9 transitional relief, which fully phased out at 31 December "
    "2024) throughout, for comparability across years. FY2024 and FY2025 Total Capital ratios are also explicitly "
    "stated on a fully loaded basis in the source; for FY2021-FY2023 only a 'regulatory' (IFRS 9 transitional) "
    "basis Total Capital ratio was stated as a headline figure, so the fully loaded Total Capital ratios shown for "
    "those years are calculated here as disclosed fully-loaded Total capital / disclosed RWA (both audited "
    "figures from the same capital composition table) rather than quoted verbatim - cross-checked and consistent "
    "with the FY2024/FY2025 years where both the calculated and stated fully-loaded figures are available. Tier 1 "
    "ratio is not quoted as a percentage in any year's Annual Report (only Tier 1 capital £m and RWA £m); it is "
    "calculated the same way (Tier 1 capital / RWA) for all 5 years."
)

REGULATORY_NOTE = (
    "REGULATORY NOTE: On 19 February 2026 the Payment Systems Regulator (not the PRA) fined Bank of Ireland (UK) "
    "Plc £3.78m for a 14-month delay implementing Confirmation of Payee send functionality (compliant from January "
    "2025). This relates to payment-systems conduct, not capital/liquidity adequacy, and has no bearing on the "
    "figures in this workbook."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank of Ireland (UK) Plc consolidated Group cash flow statement, £m:\n"
    f"FY2025: Bank of Ireland (UK) Annual Report 2025, p.80 (Consolidated cash flow statement) - {AR2025_URL}\n"
    f"FY2024: Bank of Ireland (UK) Annual Report 2024, p.85 (Consolidated cash flow statement) - {AR2024_URL}\n"
    f"FY2023: Bank of Ireland (UK) plc Annual Report 2023, p.79 (Consolidated cash flow statement) - {AR2023_URL}\n"
    f"FY2022: Bank of Ireland (UK) plc Annual Report 2022, p.81 (Consolidated cash flow statement) - {AR2022_URL}\n"
    f"FY2021: Bank of Ireland (UK) plc Annual Report 2021, p.87 (Consolidated cash flow statement) - {AR2021_URL}\n"
    "Note: each year's own report was used for its own column (all cross-checked against the following year's "
    "comparative column, which matched exactly in every case). Operating-activity adjustment line items vary "
    "slightly year to year (e.g. 'Net change in fair value changes due to interest rate risk of the hedged items "
    "in portfolio hedges' appears only in FY2023/FY2024); blank cells indicate that year's report did not include "
    "that specific line. Section totals and cash/cash equivalents figures are consistent and comparable across all "
    "5 years.\n\n"
    + ENTITY_NOTE + "\n\n" + REGULATORY_NOTE
)


def p3_sources(page):
    urls = {"FY2025": AR2025_URL, "FY2024": AR2024_URL, "FY2023": AR2023_URL, "FY2022": AR2022_URL, "FY2021": AR2021_URL}
    names = {
        "FY2025": "Bank of Ireland (UK) Annual Report 2025",
        "FY2024": "Bank of Ireland (UK) Annual Report 2024",
        "FY2023": "Bank of Ireland (UK) plc Annual Report 2023",
        "FY2022": "Bank of Ireland (UK) plc Annual Report 2022",
        "FY2021": "Bank of Ireland (UK) plc Annual Report 2021",
    }
    lines = ["Sources - Bank of Ireland (UK) Plc consolidated Group basis, from the Risk Management Report / "
             "Financial Review ('2.2 Funding and liquidity risk' / '3 Capital management' sections):"]
    for y in YEARS:
        lines.append(f"{y}: {names[y]}, p.{page[y]} - {urls[y]}")
    return "\n".join(lines) + "\n\n" + BASIS_NOTE


bw = BankWorkbook(bank_name="Bank of Ireland (UK) Plc", years=YEARS, header_color="00594F")

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
BALANCE_SHEET_SOURCES = (
    "Sources - Bank of Ireland (UK) Plc consolidated Group Balance sheet, £m, each year from its own primary "
    "report:\n"
    f"FY2025: Annual Report 2025, p.77 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.82 - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, p.28 (printed) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, p.26 (printed) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, p.85 - {AR2021_URL}\n"
    "Note: 'Fair value changes due to interest rate risk of hedged items in portfolio hedges' is shown as its own "
    "line FY2022-FY2025 (a voluntary presentation change adopted in the FY2022 report); FY2021's own report embeds "
    "it within Loans and advances to customers / Customer accounts instead - FY2021's own gross loan and customer-"
    "account figures are ~£71m/£1m lower than the FY2022 report's restated FY2021 comparative column as a result. "
    "Each year's own figures are used here (not restated comparatives) per project convention; both totals still "
    "reconcile internally. Current tax assets/Assets classified as held for sale are blank where not separately "
    "disclosed that year.\n\n" + ENTITY_NOTE
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 2306, "FY2024": 2069, "FY2023": 2213, "FY2022": 2239, "FY2021": 3456}),
    ("DATA", "Items in the course of collection from other banks", {"FY2025": 96, "FY2024": 67, "FY2023": 71, "FY2022": 79, "FY2021": 101}),
    ("DATA", "Derivative financial instruments", {"FY2025": 70, "FY2024": 179, "FY2023": 283, "FY2022": 379, "FY2021": 88}),
    ("DATA", "Loans and advances to banks", {"FY2025": 1157, "FY2024": 1171, "FY2023": 1248, "FY2022": 1461, "FY2021": 1574}),
    ("DATA", "Debt securities at amortised cost", {"FY2025": 881, "FY2024": 476, "FY2023": 489, "FY2022": 528, "FY2021": 798}),
    ("DATA", "Fair value changes due to interest rate risk of hedged items in portfolio hedges", {"FY2025": 41, "FY2024": -58, "FY2023": -100, "FY2022": -276}),
    ("DATA", "Loans and advances to customers", {"FY2025": 14704, "FY2024": 14191, "FY2023": 14148, "FY2022": 14018, "FY2021": 16325}),
    ("DATA", "Interest in joint venture", {"FY2025": 60, "FY2024": 61, "FY2023": 67, "FY2022": 71, "FY2021": 47}),
    ("DATA", "Intangible assets and goodwill", {"FY2025": 24, "FY2024": 25, "FY2023": 26, "FY2022": 28, "FY2021": 32}),
    ("DATA", "Property, plant and equipment", {"FY2025": 272, "FY2024": 244, "FY2023": 215, "FY2022": 174, "FY2021": 143}),
    ("DATA", "Other assets", {"FY2025": 102, "FY2024": 74, "FY2023": 65, "FY2022": 52, "FY2021": 42}),
    ("DATA", "Current tax assets", {"FY2025": 67, "FY2024": 23, "FY2021": 8}),
    ("DATA", "Deferred tax assets", {"FY2025": 71, "FY2024": 75, "FY2023": 96, "FY2022": 108, "FY2021": 77}),
    ("DATA", "Retirement benefit asset", {"FY2025": 14, "FY2024": 14, "FY2023": 11, "FY2022": 10, "FY2021": 13}),
    ("DATA", "Assets classified as held for sale", {"FY2021": 1}),
    ("TOTAL", "Total assets", {"FY2025": 19865, "FY2024": 18611, "FY2023": 18832, "FY2022": 18871, "FY2021": 22705}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 2687, "FY2024": 2422, "FY2023": 3237, "FY2022": 3107, "FY2021": 3399}),
    ("DATA", "Customer accounts", {"FY2025": 12765, "FY2024": 12223, "FY2023": 11815, "FY2022": 12222, "FY2021": 15753}),
    ("DATA", "Fair value changes due to interest rate risk of hedged items in portfolio hedges", {"FY2025": -23, "FY2024": -87, "FY2023": -44, "FY2022": -130}),
    ("DATA", "Items in the course of transmission to other banks", {"FY2025": 127, "FY2024": 63, "FY2023": 86, "FY2022": 63, "FY2021": 62}),
    ("DATA", "Derivative financial instruments", {"FY2025": 223, "FY2024": 293, "FY2023": 326, "FY2022": 328, "FY2021": 65}),
    ("DATA", "Debt securities in issue", {"FY2025": 743, "FY2024": 514, "FY2023": 549, "FY2022": 379, "FY2021": 448}),
    ("DATA", "Current tax liabilities", {"FY2025": 0, "FY2024": 16, "FY2023": 6, "FY2022": 4, "FY2021": 2}),
    ("DATA", "Other liabilities", {"FY2025": 971, "FY2024": 1023, "FY2023": 1001, "FY2022": 1037, "FY2021": 1010}),
    ("DATA", "Lease liabilities", {"FY2025": 14, "FY2024": 14, "FY2023": 16, "FY2022": 12, "FY2021": 15}),
    ("DATA", "Provisions", {"FY2025": 377, "FY2024": 159, "FY2023": 8, "FY2022": 9, "FY2021": 14}),
    ("DATA", "Loss allowance provision on loan commitments and financial guarantees", {"FY2025": 6, "FY2024": 4, "FY2023": 3, "FY2022": 5, "FY2021": 4}),
    ("DATA", "Subordinated liabilities", {"FY2025": 190, "FY2024": 190, "FY2023": 190, "FY2022": 190, "FY2021": 190}),
    ("TOTAL", "Total liabilities", {"FY2025": 18080, "FY2024": 16834, "FY2023": 17193, "FY2022": 17226, "FY2021": 20962}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 122, "FY2024": 122, "FY2023": 122, "FY2022": 122, "FY2021": 122}),
    ("DATA", "Retained earnings", {"FY2025": 1162, "FY2024": 1171, "FY2023": 1049, "FY2022": 1049, "FY2021": 1083}),
    ("DATA", "Other reserves", {"FY2025": 351, "FY2024": 334, "FY2023": 318, "FY2022": 324, "FY2021": 388}),
    ("DATA", "Other equity instruments", {"FY2025": 150, "FY2024": 150, "FY2023": 150, "FY2022": 150, "FY2021": 150}),
    ("TOTAL", "Total equity attributable to owners of the Bank", {"FY2025": 1785, "FY2024": 1777, "FY2023": 1639, "FY2022": 1645, "FY2021": 1743}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 19865, "FY2024": 18611, "FY2023": 18832, "FY2022": 18871, "FY2021": 22705}),
]

bw.add_balance_sheet_sheet(
    title="Bank of Ireland (UK) Plc — Consolidated Statement of Financial Position",
    subtitle="Consolidated Group basis, £m. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=78,
    source_height=180,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
INCOME_STATEMENT_SOURCES = (
    "Sources - Bank of Ireland (UK) Plc consolidated Group Income statement / Statement of other comprehensive "
    "income, £m, each year from its own primary report:\n"
    f"FY2025: Annual Report 2025, p.75-76 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.80-81 - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, p.76 (printed) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, p.78 (printed) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, p.84 - {AR2021_URL}\n"
    "Note: minor one-off gains (profit on disposal of PP&E/business activities/financial assets) are combined into "
    "a single 'Other gains, net' row since none is consistently disclosed as its own line every year; blank/0 cells "
    "reflect that year's own disclosure (0 = explicitly nil in the source, blank = line not applicable that year). "
    "All totals reconcile exactly to (Loss)/profit before taxation and Total comprehensive income.\n\n" + ENTITY_NOTE
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income calculated using the effective interest method", {"FY2025": 684, "FY2024": 796, "FY2023": 792, "FY2022": 580, "FY2021": 532}),
    ("DATA", "Other interest income", {"FY2025": 215, "FY2024": 177, "FY2023": 131, "FY2022": 83, "FY2021": 78}),
    ("TOTAL", "Total interest income", {"FY2025": 899, "FY2024": 973, "FY2023": 923, "FY2022": 663, "FY2021": 610}),
    ("DATA", "Interest expense", {"FY2025": -442, "FY2024": -481, "FY2023": -340, "FY2022": -108, "FY2021": -99}),
    ("TOTAL", "Net interest income", {"FY2025": 457, "FY2024": 492, "FY2023": 583, "FY2022": 555, "FY2021": 511}),
    ("DATA", "Net leasing income", {"FY2025": 24, "FY2024": 19, "FY2023": 26, "FY2022": 22, "FY2021": 14}),
    ("DATA", "Other leasing income", {"FY2025": 104, "FY2024": 92, "FY2023": 80, "FY2022": 60, "FY2021": 55}),
    ("DATA", "Other leasing expense", {"FY2025": -80, "FY2024": -73, "FY2023": -54, "FY2022": -38, "FY2021": -41}),
    ("DATA", "Fee and commission income", {"FY2025": 31, "FY2024": 32, "FY2023": 35, "FY2022": 37, "FY2021": 57}),
    ("DATA", "Fee and commission expense", {"FY2025": -50, "FY2024": -67, "FY2023": -91, "FY2022": -88, "FY2021": -50}),
    ("DATA", "Net trading income", {"FY2025": 14, "FY2024": 20, "FY2023": 15, "FY2022": 7, "FY2021": 3}),
    ("DATA", "Other operating income", {"FY2025": 0, "FY2024": 2, "FY2023": 3, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Total operating income", {"FY2025": 476, "FY2024": 498, "FY2023": 571, "FY2022": 533, "FY2021": 535}),
    ("SECTION", "Expenses and impairment", {}),
    ("DATA", "Operating expenses", {"FY2025": -485, "FY2024": -382, "FY2023": -222, "FY2022": -247, "FY2021": -272}),
    ("TOTAL", "Operating profit/(loss) before impairment charges on financial assets", {"FY2025": -9, "FY2024": 116, "FY2023": 349, "FY2022": 286, "FY2021": 263}),
    ("DATA", "Net impairment (losses)/gains on financial instruments", {"FY2025": -25, "FY2024": 8, "FY2023": -43, "FY2022": -64, "FY2021": 54}),
    ("TOTAL", "Operating profit/(loss)", {"FY2025": -34, "FY2024": 124, "FY2023": 306, "FY2022": 222, "FY2021": 317}),
    ("DATA", "Share of profit/(loss) after tax of joint venture", {"FY2025": 22, "FY2024": 24, "FY2023": 25, "FY2022": 28, "FY2021": -2}),
    ("DATA", "Other gains, net (disposal of PP&E/business activities/financial assets)", {"FY2025": 0, "FY2024": 33, "FY2023": 0, "FY2022": 1, "FY2021": 95}),
    ("TOTAL", "Profit/(loss) before taxation", {"FY2025": -12, "FY2024": 181, "FY2023": 331, "FY2022": 251, "FY2021": 410}),
    ("DATA", "Taxation credit/(charge)", {"FY2025": 11, "FY2024": -48, "FY2023": -72, "FY2022": -23, "FY2021": -12}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": -1, "FY2024": 133, "FY2023": 259, "FY2022": 228, "FY2021": 398}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Net change in cash flow hedge reserve, net of tax", {"FY2025": 17, "FY2024": 17, "FY2023": -5, "FY2022": -63, "FY2021": -35}),
    ("DATA", "Net actuarial gain/(loss) on defined benefit schemes", {"FY2025": 0, "FY2024": 1, "FY2023": 0, "FY2022": -3, "FY2021": 2}),
    ("DATA", "Net change in revaluation reserve, net of tax", {"FY2025": 0, "FY2024": -1, "FY2023": -1, "FY2022": -1, "FY2021": 1}),
    ("TOTAL", "Other comprehensive income/(expense) for the year, net of tax", {"FY2025": 17, "FY2024": 17, "FY2023": -6, "FY2022": -67, "FY2021": -32}),
    ("TOTAL", "Total comprehensive income/(loss) for the year, net of tax", {"FY2025": 16, "FY2024": 150, "FY2023": 253, "FY2022": 161, "FY2021": 366}),
]

bw.add_income_statement_sheet(
    title="Bank of Ireland (UK) Plc — Consolidated Statement of Comprehensive Income",
    subtitle="Consolidated Group basis, £m. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=78,
    source_height=180,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_CHANGES_SOURCES = (
    "Sources - Bank of Ireland (UK) Plc consolidated Group Statement of changes in equity, £m, each year from its "
    "own primary report (own-year 'Balance at 31 December' column used for that year's closing balances):\n"
    f"FY2021: Annual Report 2021, p.86 - {AR2021_URL}\n"
    f"FY2022: Annual Report 2022, p.80 (printed) - {AR2022_URL}\n"
    f"FY2023: Annual Report 2023, p.78 (printed) - {AR2023_URL}\n"
    f"FY2024: Annual Report 2024, p.83 - {AR2024_URL}\n"
    f"FY2025: Annual Report 2025, p.78 - {AR2025_URL}\n"
    "Note: Revaluation reserve, Cash flow hedge reserve, Capital contribution and Capital redemption reserve fund "
    "are reported as 'Other reserves' sub-components in the source; Capital contribution never moves across all 5 "
    "years shown (£266m throughout) so no separate movement row is needed for it. Each year's opening balance ties "
    "exactly to the prior year's own closing balance.\n\n" + ENTITY_NOTE
)

EQUITY_HEADERS = ["Share capital", "Retained earnings", "Other equity instruments", "Revaluation reserve",
                   "Cash flow hedge reserve", "Capital contribution", "Capital redemption reserve fund", "Total equity"]

equity_changes_rows = [
    ("TOTAL", "Balance at 1 January 2021", (197, 957, 300, 2, 21, 266, 58, 1801)),
    ("DATA", "Profit for the year", (None, 398, None, None, None, None, None, 398)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -25, None, None, None, None, None, -25)),
    ("DATA", "Share repurchase", (-75, -250, None, None, None, None, 75, -250)),
    ("DATA", "Remeasurement of the net defined benefit pension asset", (None, 3, None, None, None, None, None, 3)),
    ("DATA", "Repayment of other equity instruments", (None, None, -300, None, None, None, None, -300)),
    ("DATA", "Issuance of other equity instruments", (None, None, 150, None, None, None, None, 150)),
    ("DATA", "Revaluation of property", (None, None, None, 1, None, None, None, 1)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, -35, None, None, -35)),
    ("TOTAL", "Balance at 31 December 2021", (122, 1083, 150, 3, -14, 266, 133, 1743)),
    ("DATA", "Profit for the year", (None, 228, None, None, None, None, None, 228)),
    ("DATA", "Dividend on ordinary shares", (None, -250, None, None, None, None, None, -250)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -9, None, None, None, None, None, -9)),
    ("DATA", "Remeasurement of the net defined benefit pension asset", (None, -3, None, None, None, None, None, -3)),
    ("DATA", "Revaluation of property", (None, None, None, -1, None, None, None, -1)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, -63, None, None, -63)),
    ("TOTAL", "Balance at 31 December 2022", (122, 1049, 150, 2, -77, 266, 133, 1645)),
    ("DATA", "Profit for the year", (None, 259, None, None, None, None, None, 259)),
    ("DATA", "Dividend on ordinary shares", (None, -250, None, None, None, None, None, -250)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -9, None, None, None, None, None, -9)),
    ("DATA", "Revaluation of property", (None, None, None, -1, None, None, None, -1)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, -5, None, None, -5)),
    ("TOTAL", "Balance at 31 December 2023", (122, 1049, 150, 1, -82, 266, 133, 1639)),
    ("DATA", "Profit for the year", (None, 133, None, None, None, None, None, 133)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -9, None, None, None, None, None, -9)),
    ("DATA", "Remeasurement of the net defined benefit pension asset", (None, 1, None, None, None, None, None, 1)),
    ("DATA", "Other movements", (None, -3, None, None, None, None, None, -3)),
    ("DATA", "Revaluation of property", (None, None, None, -1, None, None, None, -1)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, 17, None, None, 17)),
    ("TOTAL", "Balance at 31 December 2024", (122, 1171, 150, 0, -65, 266, 133, 1777)),
    ("DATA", "(Loss) for the year", (None, -1, None, None, None, None, None, -1)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -9, None, None, None, None, None, -9)),
    ("DATA", "Other movements", (None, 1, None, None, None, None, None, 1)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, 17, None, None, 17)),
    ("TOTAL", "Balance at 31 December 2025", (122, 1162, 150, 0, -48, 266, 133, 1785)),
]

bw.add_equity_changes_sheet(
    title="Bank of Ireland (UK) Plc — Consolidated Statement of Changes in Equity",
    subtitle="Consolidated Group basis, £m; chronological, oldest to newest. See source note at bottom.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    source_height=200,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before taxation", {"FY2025": -12, "FY2024": 181, "FY2023": 331, "FY2022": 251, "FY2021": 410}),
    ("DATA", "Interest expense on subordinated liabilities and other capital instruments", {"FY2025": 28, "FY2024": 31, "FY2023": 34, "FY2022": 14, "FY2021": 17}),
    ("DATA", "Interest expense on lease liabilities", {"FY2025": 1, "FY2024": 1, "FY2023": 1, "FY2022": 1}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 48, "FY2024": 46, "FY2023": 34, "FY2022": 27, "FY2021": 31}),
    ("DATA", "Net impairment losses/(gains) on financial instruments", {"FY2025": 25, "FY2024": -8, "FY2023": 43, "FY2022": 64, "FY2021": -54}),
    ("DATA", "Profit on sale of financial assets", {"FY2024": -33}),
    ("DATA", "(Gain)/loss on disposal of financial assets", {"FY2021": -94}),
    ("DATA", "(Gain)/loss on disposal of business activities", {"FY2021": -1}),
    ("DATA", "(Gain)/loss on sale of property, plant, equipment", {"FY2022": -1}),
    ("DATA", "Share of results of joint venture", {"FY2025": -22, "FY2024": -24, "FY2023": -25, "FY2022": -28, "FY2021": 2}),
    ("DATA", "Net change in prepayments and interest receivable", {"FY2025": -5, "FY2024": 9, "FY2022": -4, "FY2021": 10}),
    ("DATA", "Net change in accruals and interest payable", {"FY2025": -9, "FY2024": 8, "FY2023": 94, "FY2022": 36, "FY2021": -28}),
    ("DATA", "Charge for provisions", {"FY2025": 236, "FY2024": 148, "FY2023": 3, "FY2022": 2, "FY2021": 13}),
    ("DATA", "Other non-cash items", {"FY2025": -18, "FY2024": -98, "FY2023": -127, "FY2022": -45, "FY2021": 7}),
    ("TOTAL", "Cash flows from operating activities before changes in operating assets and liabilities", {"FY2025": 272, "FY2024": 261, "FY2023": 388, "FY2022": 317, "FY2021": 313}),
    ("DATA", "Net change in items in the course of collection to/from banks", {"FY2025": 35, "FY2024": -19, "FY2023": 31, "FY2022": 24, "FY2021": 5}),
    ("DATA", "Net change in derivative financial instruments", {"FY2025": 26, "FY2024": 97, "FY2023": 97, "FY2022": 30, "FY2021": -9}),
    ("DATA", "Net change in loans and advances to banks", {"FY2025": 32, "FY2024": -51, "FY2023": -45, "FY2021": 4}),
    ("DATA", "Net change in fair value changes due to interest rate risk of hedged items in portfolio hedges", {"FY2023": -146}),
    ("DATA", "Net change in loans and advances to customers", {"FY2025": -536, "FY2024": -671, "FY2023": 101, "FY2022": 2316, "FY2021": 2051}),
    ("DATA", "Net change in deposits from banks", {"FY2025": 265, "FY2024": -815, "FY2023": 130, "FY2022": -292, "FY2021": -803}),
    ("DATA", "Net change in customer accounts", {"FY2025": 542, "FY2024": 408, "FY2023": -537, "FY2022": -3532, "FY2021": -2495}),
    ("DATA", "Net change in debt securities in issue", {"FY2025": 229, "FY2024": -35, "FY2023": 170, "FY2022": -69, "FY2021": -63}),
    ("DATA", "Net change in provisions", {"FY2025": -18, "FY2024": -8, "FY2023": -4, "FY2022": -7, "FY2021": -14}),
    ("DATA", "Net change in retirement benefit obligation", {"FY2025": -1, "FY2024": -1, "FY2022": -1, "FY2021": -1}),
    ("DATA", "Net change in other assets and other liabilities", {"FY2025": -65, "FY2024": -7, "FY2023": -143, "FY2022": -14, "FY2021": -90}),
    ("TOTAL", "Net cash flow from operating assets and liabilities", {"FY2025": 509, "FY2024": -1102, "FY2023": -346, "FY2022": -1545, "FY2021": -1415}),
    ("TOTAL", "Net cash flow from operating activities before taxation", {"FY2025": 781, "FY2024": -841, "FY2023": 42, "FY2022": -1228, "FY2021": -1102}),
    ("DATA", "Taxation paid", {"FY2025": -51, "FY2024": -47, "FY2023": -56, "FY2022": -21, "FY2021": -53}),
    ("TOTAL", "Net cash flow from operating activities", {"FY2025": 730, "FY2024": -888, "FY2023": -14, "FY2022": -1249, "FY2021": -1155}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Proceeds from sale of financial assets", {"FY2024": 680, "FY2021": 2942}),
    ("DATA", "Disposal of business activities", {}),
    ("DATA", "Additions to debt securities at amortised cost", {"FY2025": -461, "FY2024": -77, "FY2023": -145, "FY2022": -26, "FY2021": -252}),
    ("DATA", "Disposal/redemption of debt securities at amortised cost", {"FY2025": 69, "FY2024": 90, "FY2023": 196, "FY2022": 266, "FY2021": 359}),
    ("DATA", "Dividends received from joint venture", {"FY2025": 23, "FY2024": 30, "FY2023": 29, "FY2022": 3}),
    ("DATA", "Additions to intangible assets", {}),
    ("DATA", "Additions to property, plant and equipment", {"FY2025": -105, "FY2024": -97, "FY2023": -82, "FY2022": -70, "FY2021": -54}),
    ("DATA", "Disposal of property, plant and equipment", {"FY2025": 37, "FY2024": 33, "FY2023": 29, "FY2022": 23, "FY2021": 18}),
    ("TOTAL", "Cash flows from investing activities", {"FY2025": -437, "FY2024": 659, "FY2023": 27, "FY2022": 196, "FY2021": 3013}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Share repurchase", {"FY2021": -250}),
    ("DATA", "Dividend paid on ordinary shares", {"FY2023": -250, "FY2022": -250}),
    ("DATA", "Proceeds from issue of AT1", {"FY2021": 150}),
    ("DATA", "Redemption of AT1", {"FY2021": -300}),
    ("DATA", "Additional tier 1 coupon paid", {"FY2025": -9, "FY2024": -9, "FY2023": -9, "FY2022": -9, "FY2021": -25}),
    ("DATA", "Redemption of subordinated liabilities", {"FY2022": -90, "FY2021": -200}),
    ("DATA", "Proceeds from issue of subordinated liabilities", {"FY2022": 90, "FY2021": 100}),
    ("DATA", "Interest paid on subordinated liabilities", {"FY2025": -28, "FY2024": -31, "FY2023": -34, "FY2022": -14, "FY2021": -17}),
    ("DATA", "Payment of lease liability", {"FY2025": -1, "FY2024": -3, "FY2023": -4, "FY2022": -4, "FY2021": -4}),
    ("TOTAL", "Cash flows from financing activities", {"FY2025": -38, "FY2024": -43, "FY2023": -297, "FY2022": -277, "FY2021": -546}),
    ("TOTAL", "Net change in cash and cash equivalents", {"FY2025": 255, "FY2024": -272, "FY2023": -284, "FY2022": -1330, "FY2021": 1312}),
    ("DATA", "Opening cash and cash equivalents", {"FY2025": 3115, "FY2024": 3387, "FY2023": 3671, "FY2022": 5001, "FY2021": 3689}),
    ("TOTAL", "Closing cash and cash equivalents", {"FY2025": 3370, "FY2024": 3115, "FY2023": 3387, "FY2022": 3671, "FY2021": 5001}),
]

bw.add_cash_flow_sheet(
    title="Bank of Ireland (UK) Plc — Consolidated Cash Flow Statement",
    subtitle="Consolidated Group basis, £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - Bank of Ireland (UK) Plc consolidated Group basis, loans and advances to customers at amortised "
    "cost, £m, each year from its own primary report's IFRS 9 stage/product note (own-year gross carrying amount "
    "and impairment loss allowance tables):\n"
    f"FY2025: Annual Report 2025, p.111-113 (Note 19) - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.111-113 (Note 19, prior-period comparative) - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, p.114-115 (Note 18, printed) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, p.120-121 (Note 20, printed) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, p.128-130 (Note 20) - {AR2021_URL}\n"
    "Note: by-product split (Residential mortgages / Non-property SME and corporate / Commercial property and "
    "construction / Consumer) is disclosed at Group level for FY2022-FY2025 only; FY2021's Group-level table shows "
    "only stage totals (a by-product split exists but only at Bank/solo level for FY2021, not reused here for a "
    "Group-basis sheet) - by-product cells are blank for FY2021, the stage-level rows are complete for all 5 years. "
    "FY2021's gross carrying amount (£16,503m) is ~£71m lower than the FY2022 report's restated FY2021 comparative "
    "(£16,574m) - see the Balance Sheet sheet's note on the same reclassification; each year's own figures are used "
    "here. Net loans (gross minus impairment loss allowance) tie exactly to the Balance Sheet's Loans and advances "
    "to customers line for every year. Ratios are calculated here (not separately disclosed as ratios in the "
    "source).\n\n" + ENTITY_NOTE
)

asset_quality_rows = [
    ("SECTION", "Gross carrying amount by product", {}),
    ("DATA", "Residential mortgages", {"FY2025": 10750, "FY2024": 10639, "FY2023": 9811, "FY2022": 9742}),
    ("DATA", "Non-property SME and corporate", {"FY2025": 1157, "FY2024": 1278, "FY2023": 1306, "FY2022": 1355}),
    ("DATA", "Commercial property and construction", {"FY2025": 207, "FY2024": 203, "FY2023": 216, "FY2022": 274}),
    ("DATA", "Consumer", {"FY2025": 2684, "FY2024": 2159, "FY2023": 2966, "FY2022": 2831}),
    ("SECTION", "Gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 - 12 month ECL (not credit-impaired)", {"FY2025": 13409, "FY2024": 13113, "FY2023": 12501, "FY2022": 12615, "FY2021": 14769}),
    ("DATA", "Stage 2 - Lifetime ECL (not credit-impaired)", {"FY2025": 1210, "FY2024": 901, "FY2023": 1502, "FY2022": 1288, "FY2021": 1208}),
    ("DATA", "Stage 3 - Lifetime ECL (credit-impaired)", {"FY2025": 179, "FY2024": 265, "FY2023": 296, "FY2022": 299, "FY2021": 526}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 14798, "FY2024": 14279, "FY2023": 14299, "FY2022": 14202, "FY2021": 16503}),
    ("SECTION", "Impairment loss allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1 - 12 month ECL (not credit-impaired)", {"FY2025": 22, "FY2024": 17, "FY2023": 40, "FY2022": 40, "FY2021": 47}),
    ("DATA", "Stage 2 - Lifetime ECL (not credit-impaired)", {"FY2025": 30, "FY2024": 23, "FY2023": 66, "FY2022": 44, "FY2021": 46}),
    ("DATA", "Stage 3 - Lifetime ECL (credit-impaired)", {"FY2025": 42, "FY2024": 48, "FY2023": 45, "FY2022": 100, "FY2021": 85}),
    ("TOTAL", "Total impairment loss allowance", {"FY2025": 94, "FY2024": 88, "FY2023": 151, "FY2022": 184, "FY2021": 178}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 14704, "FY2024": 14191, "FY2023": 14148, "FY2022": 14018, "FY2021": 16325}),
    ("SECTION", "Ratios (calculated)", {}),
    ("DATA", "ECL coverage ratio (total allowance / total gross carrying amount)", {"FY2025": "0.64%", "FY2024": "0.62%", "FY2023": "1.06%", "FY2022": "1.30%", "FY2021": "1.08%"}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross carrying amount)", {"FY2025": "1.21%", "FY2024": "1.86%", "FY2023": "2.07%", "FY2022": "2.11%", "FY2021": "3.19%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross)", {"FY2025": "23.46%", "FY2024": "18.11%", "FY2023": "15.20%", "FY2022": "33.44%", "FY2021": "16.16%"}),
]

bw.add_asset_quality_sheet(
    title="Bank of Ireland (UK) Plc — Asset Quality / Credit Risk Disclosures",
    subtitle="Consolidated Group basis, loans and advances to customers at amortised cost, £m. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    source_height=220,
)

# ---------------------------------------------------------------
# Pillar 3 / capital metric sheets
# ---------------------------------------------------------------
CAP_PAGE = {"FY2025": "55", "FY2024": "57-58", "FY2023": "54-55", "FY2022": "55-56", "FY2021": "60"}
LIQ_PAGE = {"FY2025": "48", "FY2024": "49-50", "FY2023": "45-46", "FY2022": "45-46", "FY2021": "51-52"}


def metric(name, unit, rows_data, page, note=None):
    bw.add_metric_sheet(name, f"Consolidated Group basis, {unit}" if unit else "Consolidated Group basis",
                         rows_data, p3_sources(page), note=note, first_col_width=44, source_height=140)


metric(
    "CET1 Capital", "£m",
    [("Common equity tier 1 capital", {"FY2025": 1601, "FY2024": 1548, "FY2023": 1412, "FY2022": 1394, "FY2021": 1497})],
    CAP_PAGE,
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio (fully loaded)", {"FY2025": "19.6%", "FY2024": "19.9%", "FY2023": "17.8%", "FY2022": "18.2%", "FY2021": "17.2%"})],
    CAP_PAGE,
)

metric(
    "Tier 1 Capital", "£m",
    [("Total tier 1 capital", {"FY2025": 1751, "FY2024": 1698, "FY2023": 1562, "FY2022": 1544, "FY2021": 1647})],
    CAP_PAGE,
    note="Tier 1 ratio (see Tier 1 Ratio sheet) is calculated from this figure - see the Ratio Basis Note on the "
         "Cash Flow Statement sheet.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio (fully loaded; calculated as Tier 1 capital / RWA)", {"FY2025": "21.4%", "FY2024": "21.9%", "FY2023": "19.7%", "FY2022": "20.1%", "FY2021": "19.0%"})],
    CAP_PAGE,
    note="Not stated as a percentage in any year's Annual Report (only Tier 1 capital £m and RWA £m are disclosed); "
         "calculated here as Tier 1 capital / Total risk weighted assets - see the Ratio Basis Note on the Cash "
         "Flow Statement sheet.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 1941, "FY2024": 1888, "FY2023": 1752, "FY2022": 1734, "FY2021": 1837})],
    CAP_PAGE,
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio (fully loaded)", {"FY2025": "23.7%", "FY2024": "24.3%", "FY2023": "22.1%", "FY2022": "22.5%", "FY2021": "21.2%"})],
    CAP_PAGE,
    note="Explicitly stated on a fully loaded basis for FY2024/FY2025 only; FY2021-FY2023 are calculated as Total "
         "capital / RWA (both disclosed fully-loaded figures) since only a regulatory-basis ratio was stated as a "
         "headline figure those years - see the Ratio Basis Note on the Cash Flow Statement sheet.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk weighted assets", {"FY2025": 8180, "FY2024": 7767, "FY2023": 7939, "FY2022": 7699, "FY2021": 8686})],
    CAP_PAGE,
)

RWA_BREAKDOWN_SOURCES = (
    p3_sources(CAP_PAGE) + "\n\nNote: no formal Pillar 3 KM1/OV1-style template has been published at this UK-"
    "entity level since FY2020 (see the Cash Flow Statement sheet's entity note) - the Annual Report's Capital "
    "management section discloses only the aggregate Total risk weighted assets figure, not a category breakdown "
    "(credit risk / counterparty credit risk / market risk / operational risk). Checked directly against all 5 "
    "years' Capital management sections - genuinely not publicly disclosed at category level, not merely omitted "
    "here. The Total row ties exactly to the Total RWAs sheet for every year."
)

rwa_breakdown_rows = [
    ("DATA", "Category breakdown (credit risk / market risk / operational risk)", {"FY2025": "Not publicly disclosed"}),
    ("TOTAL", "Total risk weighted assets", {"FY2025": 8180, "FY2024": 7767, "FY2023": 7939, "FY2022": 7699, "FY2021": 8686}),
]

bw.add_rwa_breakdown_sheet(
    title="Bank of Ireland (UK) Plc — RWA Breakdown",
    subtitle="Consolidated Group basis, £m. Category breakdown not publicly disclosed - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total leverage ratio exposures", {"FY2025": 19437, "FY2024": 17664, "FY2023": 16678, "FY2022": 16948, "FY2021": 22879}),
        ("Leverage ratio (fully loaded)", {"FY2025": "9.0%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "9.1%", "FY2021": "7.2%"}),
    ],
    CAP_PAGE,
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {"FY2025": "161%", "FY2024": "154%", "FY2023": "168%", "FY2022": "178%", "FY2021": "268%"})],
    LIQ_PAGE,
    note="Only the headline LCR percentage is disclosed in the Annual Report's Funding and liquidity risk section; "
         "the underlying £m components (HQLA, net cash outflows) are not published for FY2021-FY2025, since a "
         "formal Pillar 3 KM1-style template has not been published at this UK-entity level since FY2020.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {"FY2025": "135%", "FY2024": "130%", "FY2023": "135%", "FY2022": "135%", "FY2021": "139%"})],
    LIQ_PAGE,
    note="Only the headline NSFR percentage is disclosed; the underlying £m components (available/required stable "
         "funding) are not published for FY2021-FY2025 - see the LCR sheet's note.",
)

metric(
    "MREL Ratio", "%",
    [("MREL ratio", {"FY2025": "26.2%", "FY2024": "26.9%", "FY2023": "24.6%", "FY2022": "26.7%", "FY2021": "24.9%"})],
    CAP_PAGE,
    note="Only the headline MREL ratio percentage is disclosed each year (a 'Key points' bullet in the Capital "
         "management section); no £m MREL resources/requirement breakdown is published. The Bank has been subject "
         "to an internal MREL requirement on a transitional basis since 1 January 2020; the Parent (Bank of "
         "Ireland Group plc), as sole shareholder, is expected to provide any future core MREL resources.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 19865, "FY2024": 18611, "FY2023": 18832, "FY2022": 18871, "FY2021": 22705}),
        ("Loans and advances to customers", {"FY2025": 14704, "FY2024": 14191, "FY2023": 14148, "FY2022": 14018, "FY2021": 16325}),
        ("Customer accounts", {"FY2025": 12765, "FY2024": 12223, "FY2023": 11815, "FY2022": 12222, "FY2021": 15753}),
        ("Total equity", {"FY2025": 1785, "FY2024": 1777, "FY2023": 1639, "FY2022": 1645, "FY2021": 1743}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 476, "FY2024": 498, "FY2023": 571, "FY2022": 533, "FY2021": 535}),
        ("Operating expenses", {"FY2025": -485, "FY2024": -382, "FY2023": -222, "FY2022": -247, "FY2021": -272}),
        ("Profit/(loss) for the year", {"FY2025": -1, "FY2024": 133, "FY2023": 259, "FY2022": 228, "FY2021": 398}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1777, "FY2024": 1639, "FY2023": 1645, "FY2022": 1743, "FY2021": 1801}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 16, "FY2024": 150, "FY2023": 253, "FY2022": 161, "FY2021": 366}),
        ("Other equity movements, net", {"FY2025": -8, "FY2024": -12, "FY2023": -259, "FY2022": -259, "FY2021": -424}),
        ("Closing equity", {"FY2025": 1785, "FY2024": 1777, "FY2023": 1639, "FY2022": 1645, "FY2021": 1743}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash flow from operating activities", {"FY2025": 730, "FY2024": -888, "FY2023": -14, "FY2022": -1249, "FY2021": -1155}),
        ("Cash flows from investing activities", {"FY2025": -437, "FY2024": 659, "FY2023": 27, "FY2022": 196, "FY2021": 3013}),
        ("Cash flows from financing activities", {"FY2025": -38, "FY2024": -43, "FY2023": -297, "FY2022": -277, "FY2021": -546}),
        ("Closing cash and cash equivalents", {"FY2025": 3370, "FY2024": 3115, "FY2023": 3387, "FY2022": 3671, "FY2021": 5001}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "19.6%", "FY2024": "19.9%", "FY2023": "17.8%", "FY2022": "18.2%", "FY2021": "17.2%"}),
        ("Tier 1 Ratio", {"FY2025": "21.4%", "FY2024": "21.9%", "FY2023": "19.7%", "FY2022": "20.1%", "FY2021": "19.0%"}),
        ("Total Capital Ratio", {"FY2025": "23.7%", "FY2024": "24.3%", "FY2023": "22.1%", "FY2022": "22.5%", "FY2021": "21.2%"}),
        ("Leverage Ratio", {"FY2025": "9.0%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "9.1%", "FY2021": "7.2%"}),
        ("LCR", {"FY2025": "161%", "FY2024": "154%", "FY2023": "168%", "FY2022": "178%", "FY2021": "268%"}),
        ("NSFR", {"FY2025": "135%", "FY2024": "130%", "FY2023": "135%", "FY2022": "135%", "FY2021": "139%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Tier 1 Ratio and part of the Total Capital Ratio series are "
         "calculated (capital / RWA), not directly quoted - see the Ratio Basis Note on the Cash Flow Statement "
         "sheet. No standalone Pillar 3 document has been published for this entity since FY2020; all figures here "
         "come from the Annual Report's Risk Management Report instead.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF IRELAND UK FINANCIALS.xlsx")
