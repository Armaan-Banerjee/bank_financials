import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Fiscal year-end changed from 30 September to 31 March via an 18-month PRA-
# approved transition period (1 Oct 2023 - 31 Mar 2025); there is no separate
# "FY2024". See FY2025_TRANSITION_NOTE below.
YEARS = ["FY2026", "FY2025", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {
    "FY2026": "FY2026",
    "FY2025": "FY2025 (18mo)",
    "FY2023": "FY2023",
    "FY2022": "FY2022",
    "FY2021": "FY2021",
}

AR2026_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2026-signed.pdf"
AR2025_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2025-signed.pdf"
AR2023_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cbplc-2023-ar-cfs.pdf"
AR2022_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cbplc-2022-ar-cfs.pdf"
AR2021_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-ara-2021.pdf"

P3_2026_URL = "https://www.virginmoneyukplc.com/downloads/pdf/cb-2026-pillar-3-report.pdf"
P3_2025_URL = "https://www.virginmoneyukplc.com/downloads/pdf/vmukplc-2025-pillar-3-report.pdf"
P3_2023_URL = "https://www.virginmoneyukplc.com/downloads/pdf/vmukplc-2023-pillar-3-report.pdf"
P3_2022_URL = "https://www.virginmoneyukplc.com/downloads/pdf/vmukplc-2022-pillar-3-report.pdf"
P3_2021_URL = "https://www.virginmoneyukplc.com/downloads/pdf/vm-pillar-3-2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Clydesdale Bank PLC (company number SC001111) is the PRA-authorised entity (FRN 121873) and the "
    "main operating banking subsidiary of Virgin Money UK PLC. On 28 July 2026 the company re-registered from a "
    "public limited company to a private limited company and is now named 'Clydesdale Bank Limited' - this workbook "
    "uses 'Clydesdale Bank PLC' throughout since that was its name for the entirety of the period covered (FY2021-"
    "FY2026). The fiscal year-end changed from 30 September to 31 March via a PRA-approved 18-month transition "
    "period (1 October 2023 - 31 March 2025, shown as 'FY2025 (18mo)' below); there is no separate FY2024 - that "
    "period is entirely contained within the 18-month column. Cash flow and Pillar 3 figures are on the 'CB Group "
    "Consolidated' / 'CB Solo-Consolidated Group' basis (Clydesdale Bank PLC's own consolidation perimeter) rather "
    "than the wider Virgin Money UK PLC group, consistent with the ring-fenced-entity basis used elsewhere in this "
    "workbook series; most annual Pillar 3 reports through FY2025 are published under the 'Virgin Money UK PLC' "
    "title but contain a dedicated CB Group Consolidated appendix, which is what is cited here."
)

NATIONWIDE_NOTE = (
    "NATIONWIDE ACQUISITION NOTE: Nationwide Building Society completed its acquisition of Virgin Money UK PLC "
    "(Clydesdale Bank PLC's parent) on 1 October 2024. On 14 November 2025 the Bank's Directors publicly announced "
    "a decision to move substantially all of the Bank's business to Nationwide by way of a Part VII banking business "
    "transfer; the High Court approved the transfer on 23 February 2026 and on 2 April 2026 the majority of the "
    "Bank's assets and liabilities transferred to Nationwide. At 31 March 2026 the transferred assets/liabilities "
    "were classified as a disposal group 'held for distribution' and the related financial performance presented as "
    f"a discontinued operation (FY2026 Annual Report and Accounts, p.60) - {AR2026_URL}."
)

FY2026_CASH_FLOW_GAP_NOTE = (
    "FY2026 cash flow is blank: the FY2026 Annual Report and Accounts moved to the FRS 101 Reduced Disclosure "
    f"Framework and explicitly took the IAS 7 'Statement of Cash Flows' disclosure exemption (p.60) - {AR2026_URL} "
    "- available to it as a qualifying subsidiary whose ultimate parent (Nationwide Building Society) publishes "
    "consolidated financial statements. No cash flow statement of any kind appears in the FY2026 accounts. See the "
    "Nationwide acquisition note above for context (the exemption coincides with the Part VII transfer of "
    "substantially all of the Bank's business)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Clydesdale Bank PLC (CB) Group consolidated cash flow statement, £m:\n"
    f"FY2025 (18mo, 1 Oct 2023 - 31 Mar 2025): Clydesdale Bank PLC 2025 Annual Report and Accounts, p.113 "
    f"(Statement of cash flows) - {AR2025_URL}\n"
    f"FY2023: Clydesdale Bank PLC 2023 Annual report & consolidated financial statements, p.116 (Statement of cash "
    f"flows) - {AR2023_URL}\n"
    f"FY2022: Clydesdale Bank PLC 2022 Annual Report and consolidated financial statements, p.119 (Statement of "
    f"cash flows) - {AR2022_URL}\n"
    f"FY2021: Clydesdale Bank PLC 2021 Annual report & consolidated financial statements, p.119 (Statement of cash "
    f"flows) - {AR2021_URL}\n"
    "Note: the FY2025 (18mo) statement's comparative period (FY2023) is presented on a basis restated to align "
    "Group accounting policies/presentation with Nationwide, and combines some line items (e.g. interest received/"
    "paid, changes in operating assets and liabilities) that FY2021-FY2023 report split out individually; FY2023's "
    "own column above uses that year's own as-originally-reported presentation, not the restated comparative. Blank "
    "cells indicate that year's report did not disclose that specific split; where a coarser combined figure was "
    "reported instead, it appears on its own row. Section totals and cash/cash equivalents figures are consistent "
    "and comparable across all 4 populated years.\n\n"
    + ENTITY_NOTE + "\n\n" + NATIONWIDE_NOTE + "\n\n" + FY2026_CASH_FLOW_GAP_NOTE
)


def p3_sources(source_label_25="21.1.2 UK KM1 - Key metrics (Appendix 1: CB Solo-Consolidated Group)", page_25="140",
               source_label_23="21.1.2 UK KM1 - Key metrics (Appendix 1: CB Group Consolidated)", page_23="123",
               source_label_22="21.1.2 UK KM1 - Key metrics (Appendix 1: CB Group Consolidated)", page_22="103",
               source_label_21="Table 57/59 (Appendix 1: Disclosures for CB Group consolidated)", page_21="77, 79"):
    return (
        "Sources - Clydesdale Bank PLC (CB) Group/Solo-Consolidated basis:\n"
        f"FY2026: Clydesdale Bank PLC 2026 Pillar 3 Report, p.5-6 (2.1 UK KM1 - Key metrics) - {P3_2026_URL}\n"
        f"FY2025 (18mo): Virgin Money UK PLC 2025 Pillar 3 Report, p.{page_25} ({source_label_25}) - {P3_2025_URL}\n"
        f"FY2023: Virgin Money UK PLC 2023 Pillar 3 Report, p.{page_23} ({source_label_23}) - {P3_2023_URL}\n"
        f"FY2022: Virgin Money UK PLC 2022 Pillar 3 Report, p.{page_22} ({source_label_22}) - {P3_2022_URL}\n"
        f"FY2021: Virgin Money UK PLC 2021 Pillar 3 Report, p.{page_21} ({source_label_21}) - {P3_2021_URL}"
    )


bw = BankWorkbook(bank_name="Clydesdale Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="6D0E23")

BASIS_NOTE = (
    "BASIS NOTE: Balance Sheet/P&L figures for FY2021-FY2025 are CB Group consolidated (matching the Cash Flow "
    "Statement's own basis); each year's own originally-published figures are used, not a later restated "
    "comparative (e.g. FY2023's own 2023 Annual Report column, not the restated FY2023 comparative shown in the "
    "FY2025 report). FY2026 is a genuine entity-basis change: following the Part VII transfer of substantially all "
    "of the Bank's business to Nationwide, the FY2026 Annual Report states the Bank 'has not prepared consolidated "
    "financial statements' (relying on the Section 400 Companies Act / IFRS 10.4 exemption, since results are now "
    f"included in Nationwide's own consolidated accounts) - {AR2026_URL}. FY2026's Balance Sheet/P&L/RWA figures "
    "are therefore Bank (Company)-solo, not Group consolidated - the last comparable Group figure is FY2025."
)

STATEMENTS_SOURCES = (
    "Sources - Clydesdale Bank PLC (CB) Group consolidated Balance Sheet / Income Statement / Statement of "
    "Comprehensive Income, £m, except FY2026 which is Bank (Company)-solo (see basis note below):\n"
    f"FY2026: Clydesdale Bank PLC 2026 Annual Report and Accounts, p.57-58 (Statement of comprehensive income, "
    f"Balance sheet) - {AR2026_URL}\n"
    f"FY2025 (18mo): Clydesdale Bank PLC 2025 Annual Report and Accounts, p.108-111 (Consolidated income "
    f"statement, Consolidated statement of comprehensive income, Balance sheets, Statements of changes in equity) "
    f"- {AR2025_URL}\n"
    f"FY2023: Clydesdale Bank PLC 2023 Annual report & consolidated financial statements, p.111-114 (Consolidated "
    f"income statement, Consolidated statement of comprehensive income, Balance sheets, Statements of changes in "
    f"equity) - {AR2023_URL}\n"
    f"FY2022: Clydesdale Bank PLC 2022 Annual Report and consolidated financial statements, p.114-117 (same "
    f"statement set) - {AR2022_URL}\n"
    f"FY2021: Clydesdale Bank PLC 2021 Annual report & consolidated financial statements, p.114-118 (same "
    f"statement set) - {AR2021_URL}\n\n"
    "PRESENTATION NOTE: the income statement's line-item structure changed between vintages - FY2021-FY2023 report "
    "'Gains less losses on financial instruments at fair value' + 'Other operating income' netted into a single "
    "'Non-interest income' subtotal with no separate Fee and commission income/expense lines; FY2025-FY2026 "
    "introduce explicit Fee and commission income/expense and Gains/(losses) from derivatives and hedge accounting "
    "lines instead. Both are shown as reported, not forced onto one basis. FY2026's Statement of comprehensive "
    "income splits Continuing/Discontinued operations (following the Part VII transfer); this workbook uses the "
    "combined Total column throughout, consistent with earlier years which do not split operations. FY2026's "
    "Other comprehensive income is shown only as a single total (not split into reclassifiable/non-reclassifiable "
    "sub-totals as in other years) since the FY2026 accounts do not disclose that split. A genuine cross-statement "
    "inconsistency: the FY2025 Annual Report's own P&L discloses FY2025's Total comprehensive loss as £(343)m, "
    "while its own Statement of changes in equity (Group basis) shows the same period's total comprehensive "
    "movement summing to £(331)m (a £12m difference not explained in the source document) - both figures are "
    "reproduced as disclosed on their respective sheets (P&L and Statement of Changes in Equity), not reconciled.\n\n"
    + BASIS_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Loans and advances to customers (amortised cost)", {"FY2026": 69060, "FY2025": 71072, "FY2023": 72191, "FY2022": 71749, "FY2021": 71874}),
    ("DATA", "Fair value adjustment for portfolio hedged risk", {"FY2026": -185, "FY2025": -116}),
    ("DATA", "Cash and balances with central banks", {"FY2026": 16158, "FY2025": 10882, "FY2023": 11282, "FY2022": 12221, "FY2021": 9711}),
    ("DATA", "Due from other banks and similar institutions", {"FY2026": 528, "FY2025": 364, "FY2023": 661, "FY2022": 656, "FY2021": 800}),
    ("DATA", "Financial assets at FVOCI", {"FY2026": 3835, "FY2025": 6197, "FY2023": 6184, "FY2022": 5064, "FY2021": 4352}),
    ("DATA", "Loans and advances to customers, at FVTPL", {"FY2026": 37, "FY2025": 47, "FY2023": 59, "FY2022": 70, "FY2021": 133}),
    ("DATA", "Derivative financial assets", {"FY2026": 13, "FY2025": 48, "FY2023": 135, "FY2022": 342, "FY2021": 140}),
    ("DATA", "Other financial assets at FVTPL", {"FY2026": 2, "FY2025": 1, "FY2023": 2, "FY2022": 2, "FY2021": 16}),
    ("DATA", "Due from related entities", {"FY2026": 614, "FY2025": 3, "FY2023": 0, "FY2022": 4, "FY2021": 4}),
    ("DATA", "Intangible assets and goodwill", {"FY2026": 0, "FY2025": 127, "FY2023": 173, "FY2022": 267, "FY2021": 373}),
    ("DATA", "Property, plant and equipment", {"FY2026": 32, "FY2025": 181, "FY2022": 211, "FY2021": 250}),
    ("DATA", "Accrued income and prepaid expenses", {"FY2026": 83, "FY2025": 100}),
    ("DATA", "Investments in controlled entities and associates", {"FY2022": 0, "FY2021": 0}),
    ("DATA", "Current tax assets", {"FY2026": 21, "FY2025": 129, "FY2022": 0, "FY2021": 10}),
    ("DATA", "Deferred tax assets", {"FY2026": 406, "FY2025": 403, "FY2023": 296, "FY2022": 256, "FY2021": 497}),
    ("DATA", "Defined benefit pension assets", {"FY2026": 366, "FY2025": 357, "FY2023": 512, "FY2022": 1000, "FY2021": 847}),
    ("DATA", "Other assets", {"FY2026": 50, "FY2025": 81, "FY2023": 389, "FY2022": 168, "FY2021": 209}),
    ("TOTAL", "Total assets", {"FY2026": 91020, "FY2025": 89876, "FY2023": 91884, "FY2022": 92010, "FY2021": 89216}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2026": 72711, "FY2025": 70383, "FY2023": 66827, "FY2022": 65434, "FY2021": 66971}),
    ("DATA", "Debt securities in issue", {"FY2026": 3749, "FY2025": 6557, "FY2023": 6155, "FY2022": 5347, "FY2021": 4241}),
    ("DATA", "Due to other banks and similar institutions", {"FY2026": 975, "FY2025": 934, "FY2023": 6920, "FY2022": 8486, "FY2021": 5918}),
    ("DATA", "Derivative financial liabilities", {"FY2026": 33, "FY2025": 132, "FY2023": 290, "FY2022": 327, "FY2021": 209}),
    ("DATA", "Due to related entities", {"FY2026": 6224, "FY2025": 4304, "FY2023": 3605, "FY2022": 3210, "FY2021": 3450}),
    ("DATA", "Current tax liabilities", {"FY2022": 7}),
    ("DATA", "Deferred tax liabilities", {"FY2026": 91, "FY2025": 89, "FY2023": 179, "FY2022": 350, "FY2021": 296}),
    ("DATA", "Provisions for liabilities and charges", {"FY2026": 44, "FY2025": 39, "FY2023": 69, "FY2022": 50, "FY2021": 104}),
    ("DATA", "Accruals and deferred income", {"FY2026": 165, "FY2025": 163}),
    ("DATA", "Other liabilities", {"FY2026": 1446, "FY2025": 1666, "FY2023": 2150, "FY2022": 2388, "FY2021": 2445}),
    ("TOTAL", "Total liabilities", {"FY2026": 85438, "FY2025": 84267, "FY2023": 86195, "FY2022": 85599, "FY2021": 83634}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital and share premium", {"FY2026": 2328, "FY2025": 2043, "FY2023": 2792, "FY2022": 2792, "FY2021": 2792}),
    ("DATA", "Other equity instruments", {"FY2026": 698, "FY2025": 693, "FY2023": 594, "FY2022": 662, "FY2021": 672}),
    ("DATA", "Other reserves", {"FY2026": 44, "FY2025": 145, "FY2023": 503, "FY2022": 743, "FY2021": 44}),
    ("DATA", "Retained earnings", {"FY2026": 2512, "FY2025": 2728, "FY2023": 1800, "FY2022": 2214, "FY2021": 2074}),
    ("TOTAL", "Total equity", {"FY2026": 5582, "FY2025": 5609, "FY2023": 5689, "FY2022": 6411, "FY2021": 5582}),
    ("TOTAL", "Total liabilities and equity", {"FY2026": 91020, "FY2025": 89876, "FY2023": 91884, "FY2022": 92010, "FY2021": 89216}),
]

bw.add_balance_sheet_sheet(
    title="Clydesdale Bank PLC — Balance Sheet",
    subtitle="CB Group consolidated basis, £m (FY2026 Bank-solo - see basis note at bottom).",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2026": 4305, "FY2025": 7042, "FY2023": 3830, "FY2022": 2215, "FY2021": 1906}),
    ("DATA", "Other similar interest", {"FY2025": 5, "FY2023": 3, "FY2022": 2, "FY2021": 4}),
    ("DATA", "Interest expense and similar charges", {"FY2026": -2594, "FY2025": -4512, "FY2023": -2147, "FY2022": -641, "FY2021": -550}),
    ("TOTAL", "Net interest income", {"FY2026": 1711, "FY2025": 2535, "FY2023": 1686, "FY2022": 1576, "FY2021": 1360}),
    ("DATA", "Fee and commission income", {"FY2026": 195, "FY2025": 288}),
    ("DATA", "Fee and commission expense", {"FY2026": -92, "FY2025": -119}),
    ("DATA", "Gains less losses on financial instruments at fair value", {"FY2023": -17, "FY2022": -22, "FY2021": -9}),
    ("DATA", "Gains/(losses) from derivatives and hedge accounting", {"FY2026": 5, "FY2025": -9}),
    ("DATA", "Other operating income", {"FY2026": 14, "FY2025": 46, "FY2023": 157, "FY2022": 157, "FY2021": 136}),
    ("TOTAL", "Total income", {"FY2026": 1833, "FY2025": 2741, "FY2023": 1826, "FY2022": 1711, "FY2021": 1487}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Operating and administrative expenses", {"FY2026": -1462, "FY2025": -2126, "FY2023": -1173, "FY2022": -1069, "FY2021": -1202}),
    ("TOTAL", "Operating profit before impairment losses", {"FY2026": 371, "FY2025": 615, "FY2023": 653, "FY2022": 642, "FY2021": 285}),
    ("DATA", "Impairment losses/(credit) on credit exposures", {"FY2026": -180, "FY2025": -429, "FY2023": -309, "FY2022": -52, "FY2021": 131}),
    ("TOTAL", "Profit on ordinary activities before tax", {"FY2026": 191, "FY2025": 186, "FY2023": 344, "FY2022": 590, "FY2021": 416}),
    ("DATA", "Tax (expense)/credit", {"FY2026": -41, "FY2025": -36, "FY2023": -95, "FY2022": -70, "FY2021": 116}),
    ("TOTAL", "Profit for the period/year", {"FY2026": 150, "FY2025": 150, "FY2023": 249, "FY2022": 520, "FY2021": 532}),
    ("SECTION", "Other comprehensive income/(expense)", {}),
    ("DATA", "Items that may be reclassified to the income statement, net of tax", {"FY2025": -358, "FY2023": -240, "FY2022": 699, "FY2021": 113}),
    ("DATA", "Items that will not be reclassified to the income statement, net of tax", {"FY2025": -135, "FY2023": -355, "FY2022": 78, "FY2021": 29}),
    ("TOTAL", "Other comprehensive income/(losses), net of tax", {"FY2026": -113, "FY2025": -493, "FY2023": -595, "FY2022": 777, "FY2021": 142}),
    ("TOTAL", "Total comprehensive income/(losses) for the period/year, net of tax", {"FY2026": 37, "FY2025": -343, "FY2023": -346, "FY2022": 1297, "FY2021": 674}),
]

bw.add_income_statement_sheet(
    title="Clydesdale Bank PLC — Profit & Loss",
    subtitle="CB Group consolidated basis, £m (FY2026 Bank-solo - see basis note at bottom).",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital and share premium", "Other equity instruments", "FVOCI reserve", "Other hedging reserve", "Cash flow hedge reserve", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "As at 1 October 2020 (=30 Sep 2020)", (2792, 672, 11, None, -80, 1595, 4990)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 532, 532)),
    ("DATA", "Other comprehensive income, net of tax", (None, None, 23, None, 90, 29, 142)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, -59, -59)),
    ("DATA", "Dividends paid to ordinary shareholders", (None, None, None, None, None, -20, -20)),
    ("DATA", "Settlement of Virgin Money Holdings (UK) Limited share awards", (None, None, None, None, None, -3, -3)),
    ("TOTAL", "At 30 September 2021", (2792, 672, 34, None, 10, 2074, 5582)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 520, 520)),
    ("DATA", "Other comprehensive income, net of tax", (None, None, 10, None, 689, 78, 777)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, -60, -60)),
    ("DATA", "Dividends paid to ordinary shareholders", (None, None, None, None, None, -367, -367)),
    ("DATA", "Settlement of Virgin Money Holdings (UK) Limited share awards", (None, None, None, None, None, -3, -3)),
    ("DATA", "AT1 issuance", (None, 346, None, None, None, None, 346)),
    ("DATA", "AT1 redemption", (None, -356, None, None, None, -28, -384)),
    ("TOTAL", "At 30 September 2022", (2792, 662, 44, None, 699, 2214, 6411)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 249, 249)),
    ("DATA", "Other comprehensive losses, net of tax", (None, None, -37, None, -203, -355, -595)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, -54, -54)),
    ("DATA", "Dividends paid to ordinary shareholders", (None, None, None, None, None, -248, -248)),
    ("DATA", "Settlement of Virgin Money Holdings (UK) Limited share awards", (None, None, None, None, None, -2, -2)),
    ("DATA", "AT1 redemption", (None, -68, None, None, None, -4, -72)),
    ("TOTAL", "At 30 September 2023 (as originally reported)", (2792, 594, 7, None, 496, 1800, 5689)),
    ("DATA", "Restatement to align Group accounting policies with Nationwide, net (per FY2025 Annual Report note 1.7)", (None, None, None, None, None, -355, -355)),
    ("TOTAL", "At 1 October 2023 (restated, per FY2025 Annual Report)", (2792, 594, 7, None, 496, 1445, 5334)),
    ("DATA", "Profit for the period", (None, None, None, None, None, 150, 150)),
    ("DATA", "Other comprehensive losses, net of tax", (None, None, -29, -3, -326, -135, -493)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, -100, -100)),
    ("DATA", "Dividends paid to ordinary shareholders", (None, None, None, None, None, -177, -177)),
    ("DATA", "Ordinary shares issued", (800, None, None, None, None, None, 800)),
    ("DATA", "Release of share premium to retained earnings", (-1549, None, None, None, None, 1549, 0)),
    ("DATA", "Impact of share schemes moving from equity settled to cash settled", (None, None, None, None, None, -1, -1)),
    ("DATA", "AT1 issuance", (None, 346, None, None, None, None, 346)),
    ("DATA", "AT1 redemption", (None, -247, None, None, None, -3, -250)),
    ("TOTAL", "At 31 March 2025 (Group basis)", (2043, 693, -22, -3, 170, 2728, 5609)),
    ("DATA", "Entity basis change: Group to Bank (Company)-solo consolidation, net (per FY2026 Annual Report, s.400/IFRS 10.4 exemption)", (None, None, None, 2, None, -28, -26)),
    ("TOTAL", "At 31 March 2025 (restated to Bank-solo basis)", (2043, 693, -22, -1, 170, 2700, 5583)),
    ("DATA", "Profit for the period", (None, None, None, None, None, 150, 150)),
    ("DATA", "Other comprehensive income/(losses), net of tax", (None, None, 5, 1, -109, -10, -113)),
    ("DATA", "AT1 distributions paid", (None, None, None, None, None, -77, -77)),
    ("DATA", "Ordinary shares issued", (285, None, None, None, None, None, 285)),
    ("DATA", "AT1 issuance", (None, 520, None, None, None, None, 520)),
    ("DATA", "AT1 redemption", (None, -515, None, None, None, -43, -558)),
    ("DATA", "Impairment of disposal group assets", (None, None, None, None, None, -208, -208)),
    ("TOTAL", "At 31 March 2026", (2328, 698, -17, 0, 61, 2512, 5582)),
]

bw.add_equity_changes_sheet(
    title="Clydesdale Bank PLC — Statement of Changes in Equity",
    subtitle="CB Group consolidated basis through 31 Mar 2025; Bank-solo basis from 31 Mar 2025 restated onward - see basis note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=340,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit on ordinary activities before tax", {"FY2025": 186, "FY2023": 344, "FY2022": 590, "FY2021": 416}),
    ("DATA", "Non-cash or non-operating items included in profit before tax", {"FY2025": 368, "FY2023": -1203, "FY2022": -1306, "FY2021": -1221}),
    ("DATA", "Changes in operating assets", {"FY2023": -551, "FY2022": 1213, "FY2021": 819}),
    ("DATA", "Changes in operating liabilities", {"FY2023": 284, "FY2022": -240, "FY2021": -1026}),
    ("DATA", "Changes in operating assets and liabilities (combined, as reported)", {"FY2025": -1738}),
    ("DATA", "Payments for short-term and low value leases", {"FY2023": -3, "FY2022": -2, "FY2021": -1}),
    ("DATA", "Interest received (operating)", {"FY2023": 3300, "FY2022": 2112, "FY2021": 2088}),
    ("DATA", "Interest paid (operating)", {"FY2023": -1173, "FY2022": -378, "FY2021": -461}),
    ("DATA", "Tax paid including group relief", {"FY2025": -37, "FY2023": -50, "FY2022": -59, "FY2021": -32}),
    ("TOTAL", "Net cash provided by/(used in) operating activities", {"FY2025": -1221, "FY2023": 948, "FY2022": 1930, "FY2021": 582}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Interest received (investing)", {"FY2023": 232, "FY2022": 47, "FY2021": 19}),
    ("DATA", "Proceeds from maturity of financial instruments at FVOCI", {"FY2022": 479, "FY2021": 1079}),
    ("DATA", "Proceeds from sale of financial assets at FVOCI", {"FY2022": 194}),
    ("DATA", "Proceeds from sale and maturity of financial instruments at FVOCI (combined, as reported)", {"FY2025": 2266, "FY2023": 1868}),
    ("DATA", "Purchase of financial assets at FVOCI", {"FY2025": -2198, "FY2023": -2950, "FY2022": -2019, "FY2021": -521}),
    ("DATA", "Purchase of shares in UTM previously held in Virgin Money Holdings (UK) Limited", {"FY2022": -4, "FY2021": -12}),
    ("DATA", "Acquisition of controlled entities", {"FY2025": -20}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 3, "FY2023": 1, "FY2022": 1, "FY2021": 6}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -15, "FY2023": -9, "FY2022": -13, "FY2021": -26}),
    ("DATA", "Purchase and development of intangible assets", {"FY2025": -6, "FY2023": -11, "FY2022": -53, "FY2021": -80}),
    ("TOTAL", "Net cash provided by/(used in) investing activities", {"FY2025": 30, "FY2023": -869, "FY2022": -1368, "FY2021": 465}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Interest paid (financing)", {"FY2023": -743, "FY2022": -246, "FY2021": -158}),
    ("DATA", "Repayment of principal portion of lease liabilities", {"FY2025": -40, "FY2023": -24, "FY2022": -26, "FY2021": -28}),
    ("DATA", "Redemption and principal repayment on RMBS and covered bonds", {"FY2023": -1012, "FY2022": -1264, "FY2021": -1543}),
    ("DATA", "Issuance of RMBS and covered bonds", {"FY2023": 1826, "FY2022": 2480}),
    ("DATA", "Issuance of AT1 securities", {"FY2025": 347, "FY2022": 347}),
    ("DATA", "Redemption of AT1 securities", {"FY2025": -250, "FY2023": -72, "FY2022": -384}),
    ("DATA", "Redemption and principal repayment on medium-term notes", {"FY2021": 0}),
    ("DATA", "Amounts drawn down under the TFSME", {"FY2022": 2550, "FY2021": 3350}),
    ("DATA", "Amounts repaid under the TFSME", {"FY2023": -1000}),
    ("DATA", "Amounts repaid under the TFS", {"FY2022": -1244, "FY2021": -2864}),
    ("DATA", "Net (increase)/decrease in amounts due from related entities", {"FY2025": -55, "FY2023": 7, "FY2022": 1, "FY2021": 9}),
    ("DATA", "Net increase/(decrease) in amounts due to related entities", {"FY2025": 373, "FY2023": 297, "FY2022": 9, "FY2021": 705}),
    ("DATA", "AT1 distributions", {"FY2025": -66, "FY2023": -54, "FY2022": -60, "FY2021": -59}),
    ("DATA", "Ordinary dividends paid", {"FY2025": -211, "FY2023": -248, "FY2022": -367, "FY2021": -20}),
    ("DATA", "Proceeds from ordinary shares issued", {"FY2025": 800}),
    ("TOTAL", "Net cash provided by/(used in) financing activities", {"FY2025": 898, "FY2023": -1023, "FY2022": 1796, "FY2021": -608}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -293, "FY2023": -944, "FY2022": 2358, "FY2021": 439}),
    ("DATA", "Cash and cash equivalents at the beginning of the period/year", {"FY2025": 10589, "FY2023": 12611, "FY2022": 10253, "FY2021": 9814}),
    ("TOTAL", "Cash and cash equivalents at the end of the period/year", {"FY2025": 10296, "FY2023": 11667, "FY2022": 12611, "FY2021": 10253}),
]

bw.add_cash_flow_sheet(
    title="Clydesdale Bank PLC — Consolidated Cash Flow Statement",
    subtitle="Clydesdale Bank (CB) Group (consolidated basis), £m unless stated. FY2026 blank - see source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - 'Gross loans and advances ECL and coverage' table (audited), Risk report, Total column, £m:\n"
    f"FY2026/FY2025: Clydesdale Bank PLC 2026 Annual Report and Accounts, p.15 - {AR2026_URL}\n"
    f"FY2023/FY2022: Clydesdale Bank PLC 2023 Annual report & consolidated financial statements, p.22 - {AR2023_URL}\n"
    f"FY2021: Clydesdale Bank PLC 2021 Annual report & consolidated financial statements, p.25 - {AR2021_URL}\n\n"
    "Excludes loans designated at FVTPL, balances due from customers on acceptances, accrued interest and "
    "deferred/unamortised fee income - so the Total gross figure here is smaller than the Balance Sheet's "
    "'Loans and advances to customers (amortised cost)' line, which is expected and not reconciled (a source-"
    "table scope difference, not an error). Ratios calculated here from the disclosed stage-level figures: NPL "
    "ratio = Stage 3 gross / Total gross; Stage 3 coverage = Stage 3 ECL / Stage 3 gross; Total coverage = Total "
    "ECL / Total gross - all match the source table's own disclosed coverage percentages exactly.\n\n"
    + BASIS_NOTE
)

asset_quality_rows = [
    ("SECTION", "Gross lending assets by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2026": 60522, "FY2025": 61585, "FY2023": 65889, "FY2022": 66385, "FY2021": 61416}),
    ("DATA", "Stage 2", {"FY2026": 8069, "FY2025": 8271, "FY2023": 6326, "FY2022": 5723, "FY2021": 10176}),
    ("DATA", "Stage 3", {"FY2026": 1145, "FY2025": 1351, "FY2023": 1080, "FY2022": 1036, "FY2021": 957}),
    ("TOTAL", "Total gross lending assets", {"FY2026": 69736, "FY2025": 71207, "FY2023": 73295, "FY2022": 73144, "FY2021": 72549}),
    ("SECTION", "Expected credit loss (ECL) allowance by stage", {}),
    ("DATA", "Stage 1", {"FY2026": 139, "FY2025": 119, "FY2023": 89, "FY2022": 85, "FY2021": 111}),
    ("DATA", "Stage 2", {"FY2026": 359, "FY2025": 406, "FY2023": 400, "FY2022": 268, "FY2021": 302}),
    ("DATA", "Stage 3", {"FY2026": 181, "FY2025": 212, "FY2023": 128, "FY2022": 104, "FY2021": 91}),
    ("TOTAL", "Total ECL allowance", {"FY2026": 679, "FY2025": 737, "FY2023": 617, "FY2022": 457, "FY2021": 504}),
    ("TOTAL", "Net lending assets (Total gross - Total ECL)", {"FY2026": 69057, "FY2025": 70470, "FY2023": 72678, "FY2022": 72687, "FY2021": 72045}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "Total coverage ratio (Total ECL / Total gross)", {"FY2026": "0.97%", "FY2025": "1.04%", "FY2023": "0.84%", "FY2022": "0.62%", "FY2021": "0.70%"}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross)", {"FY2026": "1.6%", "FY2025": "1.9%", "FY2023": "1.5%", "FY2022": "1.4%", "FY2021": "1.3%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", {"FY2026": "15.81%", "FY2025": "15.69%", "FY2023": "13.93%", "FY2022": "11.24%", "FY2021": "9.59%"}),
]

bw.add_asset_quality_sheet(
    title="Clydesdale Bank PLC — Asset Quality",
    subtitle="CB Group consolidated basis through FY2025; Bank-solo basis for FY2026, £m (ratios as disclosed). See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"CB consolidated basis, {unit}" if unit else "CB consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=110)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2026": 4248, "FY2025": 3900, "FY2023": 3685, "FY2022": 3606, "FY2021": 3603})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2026": "14.3%", "FY2025": "14.2%", "FY2023": "14.6%", "FY2022": "14.9%", "FY2021": "14.9%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2026": 4946, "FY2025": 4593, "FY2023": 4279, "FY2022": 4268, "FY2021": 4275})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2026": "16.6%", "FY2025": "16.7%", "FY2023": "17.0%", "FY2022": "17.7%", "FY2021": "17.7%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2026": 5747, "FY2025": 5347, "FY2023": 5301, "FY2022": 5288, "FY2021": 5294})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2026": "19.3%", "FY2025": "19.4%", "FY2023": "21.1%", "FY2022": "21.9%", "FY2021": "21.9%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2026": 29742, "FY2025": 27555, "FY2023": 25172, "FY2022": 24128, "FY2021": 24194})],
    p3_sources(),
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - UK OV1: Overview of risk-weighted exposure amounts, CB Group/Solo-Consolidated basis, £m:\n"
    f"FY2026: Clydesdale Bank PLC 2026 Pillar 3 Report, p.9 (2.3 UK OV1) - {P3_2026_URL}\n"
    f"FY2025 (18mo): Virgin Money UK PLC 2025 Pillar 3 Report, p.139 (Appendix 1: CB Solo-Consolidated Group, "
    f"21.1.1 UK OV1) - {P3_2025_URL}\n"
    f"FY2023: Virgin Money UK PLC 2023 Pillar 3 Report, p.122 (Appendix 1: CB Group Consolidated, 21.1.1 UK OV1) "
    f"- {P3_2023_URL}\n"
    f"FY2022: Virgin Money UK PLC 2022 Pillar 3 Report, p.102 (Appendix 1: CB Group Consolidated, 21.1.1 UK OV1) "
    f"- {P3_2022_URL}\n\n"
    "FY2021: not publicly disclosed at category level - the CB appendix in Virgin Money UK PLC's 2021 Pillar 3 "
    "Report only carries Table 57 (capital composition) and Table 58 (capital flow statement), both of which "
    "disclose only the Total RWA figure (£24,194m, already shown on the Total RWAs sheet), not a risk-category "
    "split - confirmed by reading the full appendix (pp.77-79), not assumed. A restated FY2021 comparative split "
    "does exist in the FY2022 Pillar 3 report's own OV1 table (per its PS22/21 restatement footnote) but is not "
    "used here, consistent with this project's convention of using each year's own originally-published figures.\n\n"
    + BASIS_NOTE
)

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2026": 26567, "FY2025": 24361, "FY2023": 21907, "FY2022": 21061}),
    ("DATA", "Of which: standardised approach", {"FY2026": 6186, "FY2025": 6674, "FY2023": 6431, "FY2022": 6120}),
    ("DATA", "Of which: foundation IRB (FIRB) approach", {"FY2026": 7658, "FY2025": 7725, "FY2023": 5994, "FY2022": 5424}),
    ("DATA", "Of which: slotting approach", {"FY2026": 691, "FY2025": 618, "FY2023": 410, "FY2022": 362}),
    ("DATA", "Of which: advanced IRB (AIRB) approach", {"FY2026": 12032, "FY2025": 9344, "FY2023": 9072, "FY2022": 9155}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2026": 48, "FY2025": 103, "FY2023": 424, "FY2022": 443}),
    ("DATA", "Of which: standardised approach", {"FY2026": 35, "FY2025": 80, "FY2023": 141, "FY2022": 180}),
    ("DATA", "Of which: credit valuation adjustment (CVA)", {"FY2026": 8, "FY2025": 19, "FY2023": 278, "FY2022": 258}),
    ("DATA", "Operational risk", {"FY2026": 3127, "FY2025": 3091, "FY2023": 2841, "FY2022": 2624}),
    ("DATA", "Amounts below thresholds for deduction (subject to 250% risk weight)", {"FY2026": 513, "FY2025": 516, "FY2023": 284, "FY2022": 251}),
    ("TOTAL", "Total RWAs", {"FY2026": 29742, "FY2025": 27555, "FY2023": 25172, "FY2022": 24128, "FY2021": 24194}),
]

bw.add_rwa_breakdown_sheet(
    title="Clydesdale Bank PLC — RWA Breakdown",
    subtitle="CB Group/Solo-Consolidated basis, £m. FY2021 category split not publicly disclosed - see source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=280,
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2026": 78792, "FY2025": 83120, "FY2023": 86545, "FY2022": 83758, "FY2021": 84293}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2026": "6.3%", "FY2025": "5.5%", "FY2023": "4.9%", "FY2022": "5.1%", "FY2021": "5.1%"}),
        ("Leverage ratio including claims on central banks (%)", {"FY2026": "5.3%", "FY2025": "5.0%", "FY2023": "4.5%", "FY2022": "4.5%"}),
    ],
    p3_sources(),
    note="FY2021's Pillar 3 report disclosed a single 'Leverage ratio' (5.1%) without an excluding/including claims "
         "on central banks split (that distinction was introduced in later reports), shown here on the 'excluding' "
         "row for comparability. FY2022's exposure measure (83,758) reflects a PS22/21-driven restatement to "
         "exclude Bounce Back Loan Scheme (BBLS) balances; FY2021's figure (84,293) is as originally reported and "
         "was not restated on the same basis, so the FY2021-to-FY2022 leverage exposure movement is not fully "
         "like-for-like.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2026": 16246, "FY2025": 14868, "FY2023": 13798, "FY2022": 11503}),
        ("Total net cash outflows, adjusted value", {"FY2026": 9912, "FY2025": 9414, "FY2023": 9424, "FY2022": 8222}),
        ("Liquidity Coverage Ratio (%)", {"FY2026": "164%", "FY2025": "158%", "FY2023": "146%", "FY2022": "140%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="LCR is a 12-month simple average of month-end observations. Not disclosed for FY2021 at the CB Group "
         "Consolidated level in the 2021 Pillar 3 report's dedicated CB appendix (only narrative/glossary mentions "
         "of LCR appear elsewhere in that report).",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2026": 78219, "FY2025": 77427, "FY2023": 79295}),
        ("Total required stable funding", {"FY2026": 54560, "FY2025": 54375, "FY2023": 58450}),
        ("NSFR ratio (%)", {"FY2026": "143%", "FY2025": "142%", "FY2023": "136%", "FY2022": "Not disclosed", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="Per PRA guidance, NSFR disclosures were not required until reporting reference dates after 1 January "
         "2023 (per the FY2023 Pillar 3 report), so no FY2022 or FY2021 figures exist.",
)

metric(
    "MREL Ratio", "£m / %",
    [
        ("Total capital resources", {"FY2026": 5747, "FY2025": 5347, "FY2023": 5301, "FY2022": 5288}),
        ("Eligible senior unsecured securities", {"FY2026": 3520, "FY2025": 3004, "FY2023": 2707, "FY2022": 2423}),
        ("Total MREL resources", {"FY2026": 9267, "FY2025": 8351, "FY2023": 8008, "FY2022": 7711}),
        ("MREL resources (% of total risk-weighted assets)", {"FY2026": "31.2%", "FY2025": "30.3%", "FY2023": "31.8%", "FY2022": "32.0%", "FY2021": "Not disclosed"}),
        ("MREL resources (% of UK leverage exposure measure)", {"FY2026": "11.8%", "FY2025": "10.0%", "FY2023": "9.3%", "FY2022": "9.2%"}),
    ],
    p3_sources(),
    note="'Eligible senior unsecured securities' were issued by Clydesdale Bank PLC through FY2023, but by Virgin "
         "Money UK PLC from the FY2025 (18mo) report onward - shown as reported each year, not adjusted for this "
         "change. FY2021's Pillar 3 report contains only qualitative MREL narrative (no numeric MREL disclosure of "
         "any kind), consistent with the UK KM2 MREL template not yet being in use for CB Group Consolidated that "
         "year.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2026": 91020, "FY2025": 89876, "FY2023": 91884, "FY2022": 92010, "FY2021": 89216}),
        ("Loans and advances to customers (amortised cost)", {"FY2026": 69060, "FY2025": 71072, "FY2023": 72191, "FY2022": 71749, "FY2021": 71874}),
        ("Customer deposits", {"FY2026": 72711, "FY2025": 70383, "FY2023": 66827, "FY2022": 65434, "FY2021": 66971}),
        ("Total equity", {"FY2026": 5582, "FY2025": 5609, "FY2023": 5689, "FY2022": 6411, "FY2021": 5582}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2026": 1833, "FY2025": 2741, "FY2023": 1826, "FY2022": 1711, "FY2021": 1487}),
        ("Operating and administrative expenses", {"FY2026": -1462, "FY2025": -2126, "FY2023": -1173, "FY2022": -1069, "FY2021": -1202}),
        ("Profit for the period/year", {"FY2026": 150, "FY2025": 150, "FY2023": 249, "FY2022": 520, "FY2021": 532}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2026": 5583, "FY2025": 5334, "FY2023": 6411, "FY2022": 5582, "FY2021": 4990}),
        ("Total comprehensive income/(losses) for the period/year", {"FY2026": 37, "FY2025": -343, "FY2023": -346, "FY2022": 1297, "FY2021": 674}),
        ("Other equity movements, net", {"FY2026": -38, "FY2025": 618, "FY2023": -376, "FY2022": -468, "FY2021": -82}),
        ("Closing equity", {"FY2026": 5582, "FY2025": 5609, "FY2023": 5689, "FY2022": 6411, "FY2021": 5582}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -1221, "FY2023": 948, "FY2022": 1930, "FY2021": 582}),
        ("Net cash from/(used in) investing activities", {"FY2025": 30, "FY2023": -869, "FY2022": -1368, "FY2021": 465}),
        ("Net cash from/(used in) financing activities", {"FY2025": 898, "FY2023": -1023, "FY2022": 1796, "FY2021": -608}),
        ("Cash and cash equivalents at end of period/year", {"FY2025": 10296, "FY2023": 11667, "FY2022": 12611, "FY2021": 10253}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2026": "14.3%", "FY2025": "14.2%", "FY2023": "14.6%", "FY2022": "14.9%", "FY2021": "14.9%"}),
        ("Tier 1 Ratio", {"FY2026": "16.6%", "FY2025": "16.7%", "FY2023": "17.0%", "FY2022": "17.7%", "FY2021": "17.7%"}),
        ("Total Capital Ratio", {"FY2026": "19.3%", "FY2025": "19.4%", "FY2023": "21.1%", "FY2022": "21.9%", "FY2021": "21.9%"}),
        ("Leverage Ratio", {"FY2026": "6.3%", "FY2025": "5.5%", "FY2023": "4.9%", "FY2022": "5.1%", "FY2021": "5.1%"}),
        ("LCR", {"FY2026": "164%", "FY2025": "158%", "FY2023": "146%", "FY2022": "140%"}),
        ("NSFR", {"FY2026": "143%", "FY2025": "142%", "FY2023": "136%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. FY2026 cash flow is blank because the FY2026 Annual Report "
         "took the FRS 101/IAS 7 cash-flow-statement exemption (see Cash Flow Statement sheet note) following the "
         "Part VII transfer of substantially all of the Bank's business to Nationwide on 2 April 2026; Pillar 3 "
         "disclosures were unaffected and continue for FY2026. Balance Sheet/P&L/Equity figures are CB Group "
         "consolidated through FY2025 and Bank (Company)-solo for FY2026 - a genuine entity-basis change since the "
         "FY2026 Annual Report no longer prepares consolidated financial statements (see the Balance Sheet sheet's "
         "basis note); FY2025's equity roll-forward also includes an explicit restatement plug (aligning to "
         "Nationwide's accounting policies) that is not reflected in the FY2023 column, since that column uses "
         "FY2023's own originally-published closing balance.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CLYDESDALE FINANCIALS.xlsx")
