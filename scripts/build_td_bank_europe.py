import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

CH_FILINGS = "https://find-and-update.company-information.service.gov.uk/company/02734652/filing-history"
REGULATORY_PAGE = "https://www.tdsecurities.com/ca/en/legal"
P3_URL = {
    "FY2025": "https://www.tdsecurities.com/tds/document/Pillar-3-Disclosure-Oct-2025",
    "FY2024": "https://www.tdsecurities.com/tds/document/Pillar-3-Disclosure-Oct-2024",
    "FY2023": "https://www.tdsecurities.com/tds/document/Pillar-3-Disclosure-2023",
    "FY2022": "https://www.tdsecurities.com/tds/document/Pillar-3-Disclosure-2022",
    "FY2021": "https://www.tdsecurities.com/tds/document/Pillar-3-Disclosure-2022",
}

ENTITY_NOTE = (
    "TD Bank Europe Limited (TDBEL; Companies House company 02734652; FRN 165556) is the UK PRA/FCA-authorised "
    "banking entity covered by this workbook. Companies House filings show accounts through 31 October 2025. "
    "The 2023, 2024 and 2025 Pillar 3 reports state that TDBEL is the sole/single operating regulated UK subsidiary "
    "and present the current disclosure basis as solo. The TD regulatory page states that prior-year disclosures were "
    "included in Toronto-Dominion Investments B.V.'s Pillar 3 report at UK-consolidation level; this is a basis break, "
    "not a claim that the FY2021 comparative is directly comparable to the later solo series."
)


def p3_sources():
    return (
        "Sources - TD Bank Europe Limited annual Pillar 3 disclosures (amounts in CAD millions; ratios as reported):\n"
        "FY2025: TD Bank Europe Limited Pillar 3 Disclosure, year ended 31 October 2025, Appendix 1 Table 21 "
        "pp.34-35 and capital tables pp.13-14 - " + P3_URL["FY2025"] + "\n"
        "FY2024: TD Bank Europe Limited Pillar 3 Disclosure, year ended 31 October 2024, Appendix 1 Table 21 "
        "p.34 and capital tables p.13 - " + P3_URL["FY2024"] + "\n"
        "FY2023: TD Bank Europe Limited Pillar 3 Disclosure, year ended 31 October 2023, Appendix 1 Table 21 "
        "p.35 and capital tables p.13 - " + P3_URL["FY2023"] + "\n"
        "FY2022: TD Bank Europe Limited Pillar 3 Disclosure, year ended 31 October 2022, Appendix 1 Table 21 "
        "p.35 and capital tables p.13 - " + P3_URL["FY2022"] + "\n"
        "FY2021: 2021 comparative column in the 2022 TD Bank Europe Limited Pillar 3 Disclosure, Appendix 1 Table 21 "
        "p.35 and capital tables p.13 - " + P3_URL["FY2021"] + "\n"
        "Regulatory source index and basis-transition statement: " + REGULATORY_PAGE + "\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(
    bank_name="TD Bank Europe Limited",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="2A3E5C",
)

AR_URL = {
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/02734652/filing-history/MzUwNjUzNTQxMmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": "https://find-and-update.company-information.service.gov.uk/company/02734652/filing-history/MzQ1NjMyMzYxNmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/02734652/filing-history/MzQxMTU5MjQ4MmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": "https://find-and-update.company-information.service.gov.uk/company/02734652/filing-history/MzMzMzc5NzAzMWFkaXF6a2N4/document?format=pdf&download=0",
}

AR_SOURCES_NOTE = (
    "Sources - TD Bank Europe Limited Annual Report and Financial Statements (Companies House full accounts filings; "
    "amounts in CAD'000, entity/Company basis, year ended 31 October):\n"
    "FY2025/FY2024: Full accounts made up to 31 October 2025 (filed 24 Feb 2026), Statement of comprehensive income "
    "p.28, Statement of changes in equity p.30, Balance sheet p.31 - " + AR_URL["FY2025"] + "\n"
    "FY2023/FY2022: Full accounts made up to 31 October 2023 (filed 19 Feb 2024), Statement of comprehensive income "
    "p.31, Statement of changes in equity p.32, Balance sheet p.33 - " + AR_URL["FY2023"] + "\n"
    "FY2021 (FY2020 comparative not used): Full accounts made up to 31 October 2021 (filed 23 Mar 2022), Statement "
    "of comprehensive income p.25, Statement of changes in equity p.26, Balance sheet p.27 - " + AR_URL["FY2021"] + "\n"
    "All 3 filings are scanned/image-only (no extractable text layer); transcribed by direct page render.\n"
    + ENTITY_NOTE
)

PRESENTATION_NOTE = (
    "Presentation changes across years, not errors: (1) \"Loans and advances to customers\" appears as its own "
    "Balance Sheet line FY2021-FY2023 (CAD22,977k at FY2023) but disappears entirely from the FY2024/FY2025 Balance "
    "Sheet - this ties to the FY2024 Pillar 3 report's own statement that TDBEL's corporate lending business was run "
    "off in May 2024, and to Note 4's interest-income line for this product falling to CAD776k in FY2024 and nil in "
    "FY2025. (2) FY2021's Balance Sheet carries a Deferred tax ASSET (CAD69,577k); FY2023/FY2022 instead carry only a "
    "Deferred tax LIABILITY; FY2025/FY2024 carry both a (near-nil) Deferred tax asset line and a separate Deferred "
    "tax liability line - each year's own presentation is reproduced as printed, not netted or reclassified. "
    "(3) \"Repurchase agreements\" and \"Current tax liabilities\"/\"Current tax assets\" only appear as separate lines "
    "in the years the Bank actually reports a non-nil balance; left blank in years the line isn't part of that year's "
    "own statement structure. (4) The FY2023 report's Statement of comprehensive income has no \"before ECL and "
    "taxation\" subtotal line (unlike FY2025/FY2024); the underlying Credit loss (expense)/recovery and Profit before "
    "taxation figures are unaffected."
)

# TDBEL's accounts use the applicable small-company/FRS exemption and do not
# publish a Statement of Cash Flows. Keep the standard sheet so the omission is
# explicit and the workbook retains the project's normal 13-sheet structure.
CASH_FLOW_SOURCES = (
    "No Statement of Cash Flows is included because TD Bank Europe Limited's published accounts take the applicable "
    "cash-flow-statement exemption. This workbook is therefore Pillar-3-only for quantitative purposes. Entity and "
    "filing identity: " + CH_FILINGS + "\n" + ENTITY_NOTE
)


def statement(kind_label, name, rows, first_col_width=58):
    fn = {
        "balance_sheet": bw.add_balance_sheet_sheet,
        "income_statement": bw.add_income_statement_sheet,
    }[kind_label]
    fn(
        title=f"TD Bank Europe Limited — {name}",
        subtitle="Entity/Company basis, CAD'000 unless noted - see the equity ladder/asset quality units in each sheet's own subtitle.",
        rows=rows,
        sources_text=AR_SOURCES_NOTE + "\n\n" + PRESENTATION_NOTE,
        first_col_width=first_col_width,
        source_height=280,
        unit_suffix=" (CAD'000)",
    )


BS_ROWS = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 163611, "FY2024": 960678, "FY2023": 135911, "FY2022": 84054, "FY2021": 1009106}),
    ("DATA", "Debt securities at amortised cost, net of allowance for credit losses", {"FY2025": 23455915, "FY2024": 21297771, "FY2023": 21193385, "FY2022": 19221927, "FY2021": 16375260}),
    ("DATA", "Loans and advances to banks", {"FY2025": 512755, "FY2024": 1310183, "FY2023": 319740, "FY2022": 285427, "FY2021": 293637}),
    ("DATA", "Loans and advances to customers, net of allowance for credit losses", {"FY2023": 22977, "FY2022": 70648, "FY2021": 176208}),
    ("DATA", "Derivative financial instruments", {"FY2025": 0, "FY2024": 159, "FY2023": 137226, "FY2022": 1698556, "FY2021": 1151448}),
    ("DATA", "Tangible fixed assets", {"FY2025": 4, "FY2024": 14, "FY2023": 55, "FY2022": 113, "FY2021": 172}),
    ("DATA", "Current tax assets", {"FY2025": 0, "FY2024": 1507, "FY2023": 883, "FY2021": 3793}),
    ("DATA", "Deferred tax assets", {"FY2025": 0, "FY2024": 23, "FY2021": 69577}),
    ("DATA", "Other assets", {"FY2025": 395, "FY2024": 455, "FY2023": 2733, "FY2022": 1484, "FY2021": 3589}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 170855, "FY2024": 131043, "FY2023": 89659, "FY2022": 48916, "FY2021": 36570}),
    ("TOTAL", "Total assets", {"FY2025": 24303535, "FY2024": 23701833, "FY2023": 21902569, "FY2022": 21411125, "FY2021": 19119360}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 450776, "FY2024": 1238909, "FY2023": 340060, "FY2022": 186223, "FY2021": 237439}),
    ("DATA", "Other deposits", {"FY2025": 21016787, "FY2024": 20690780, "FY2023": 20161902, "FY2022": 19925444, "FY2021": 17969614}),
    ("DATA", "Derivative financial instruments", {"FY2025": 1102192, "FY2024": 197974, "FY2023": 1272, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Repurchase agreements", {"FY2025": 0, "FY2024": 26174}),
    ("DATA", "Current tax liabilities", {"FY2025": 6717, "FY2024": 258, "FY2023": 0, "FY2022": 5905}),
    ("DATA", "Deferred tax liability", {"FY2025": 52864, "FY2024": 67245, "FY2023": 9704, "FY2022": 23971}),
    ("DATA", "Other liabilities", {"FY2025": 247494, "FY2024": 72366, "FY2023": 202123, "FY2022": 94903, "FY2021": 45606}),
    ("TOTAL", "Total liabilities", {"FY2025": 22876830, "FY2024": 22293706, "FY2023": 20715061, "FY2022": 20236446, "FY2021": 18252659}),
    ("SECTION", "Shareholder's equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 629878, "FY2024": 629878, "FY2023": 629878, "FY2022": 629878, "FY2021": 629878}),
    ("DATA", "Retained earnings", {"FY2025": 638244, "FY2024": 576600, "FY2023": 528656, "FY2022": 472619, "FY2021": 419884}),
    ("DATA", "FVTOCI reserve", {"FY2025": 598, "FY2024": 370, "FY2023": 548, "FY2022": 508, "FY2021": 532}),
    ("DATA", "Cash flow hedging reserve", {"FY2025": 157985, "FY2024": 201279, "FY2023": 28426, "FY2022": 71674, "FY2021": -183593}),
    ("TOTAL", "Total shareholder's equity", {"FY2025": 1426705, "FY2024": 1408127, "FY2023": 1187508, "FY2022": 1174679, "FY2021": 866701}),
    ("TOTAL", "Total liabilities and shareholder's equity", {"FY2025": 24303535, "FY2024": 23701833, "FY2023": 21902569, "FY2022": 21411125, "FY2021": 19119360}),
]
statement("balance_sheet", "Balance Sheet", BS_ROWS)

IS_ROWS = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income using the effective interest rate method", {"FY2025": 668472, "FY2024": 552834, "FY2023": 370139, "FY2022": 194043, "FY2021": 95526}),
    ("DATA", "Interest expense using the effective interest rate method", {"FY2025": -579863, "FY2024": -477486, "FY2023": -300155, "FY2022": -138703, "FY2021": -64462}),
    ("TOTAL", "Net interest income", {"FY2025": 88609, "FY2024": 75348, "FY2023": 69984, "FY2022": 55340, "FY2021": 31064}),
    ("DATA", "Fee & commission income", {"FY2025": 222, "FY2024": 1151, "FY2023": 23812, "FY2022": 30577, "FY2021": 41313}),
    ("TOTAL", "Net fee & commission income", {"FY2025": 222, "FY2024": 1151, "FY2023": 23812, "FY2022": 30577, "FY2021": 41313}),
    ("DATA", "Foreign exchange gain/(loss)", {"FY2025": -566, "FY2024": -1072, "FY2023": -303, "FY2022": 2191, "FY2021": 122}),
    ("DATA", "Income/(loss) on financial assets at fair value", {"FY2025": 2666, "FY2024": -218, "FY2023": 205, "FY2022": -889, "FY2021": 374}),
    ("DATA", "Other operating income", {"FY2025": 0, "FY2024": 396, "FY2023": 11, "FY2022": 11, "FY2021": 288}),
    ("DATA", "Personnel expenses", {"FY2025": 1265, "FY2024": -5342, "FY2023": -10029, "FY2022": -7063, "FY2021": -5869}),
    ("DATA", "Other expenses", {"FY2025": -9551, "FY2024": -8470, "FY2023": -13966, "FY2022": -8584, "FY2021": -5419}),
    ("DATA", "Credit loss (expense)/recovery", {"FY2025": -25, "FY2024": -31, "FY2023": 745, "FY2022": 706, "FY2021": -753}),
    ("TOTAL", "Profit on ordinary activities before taxation", {"FY2025": 82620, "FY2024": 61762, "FY2023": 70459, "FY2022": 72289, "FY2021": 61120}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": -20976, "FY2024": -13818, "FY2023": -14422, "FY2022": -19554, "FY2021": -16841}),
    ("TOTAL", "Profit for the financial year", {"FY2025": 61644, "FY2024": 47944, "FY2023": 56037, "FY2022": 52735, "FY2021": 44279}),
    ("SECTION", "Other comprehensive income (OCI)", {}),
    ("DATA", "Net gain/(loss) on derivatives designated as cash flow hedges", {"FY2025": -43294, "FY2024": 172853, "FY2023": -43248, "FY2022": 255267, "FY2021": -180323}),
    ("DATA", "Financial assets at fair value through OCI - realised gain/(loss)", {"FY2025": 228, "FY2024": -178, "FY2023": 40, "FY2022": -24, "FY2021": 101}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 18578, "FY2024": 220619, "FY2023": 12829, "FY2022": 307978, "FY2021": -135943}),
]
statement("income_statement", "Profit & Loss", IS_ROWS)

EQ_HEADERS = ["Called up share capital", "Retained earnings", "FVTOCI reserve", "Cash flow hedging reserve", "Total shareholder's equity"]
EQ_ROWS = [
    ("TOTAL", "Balance as at 1 November 2020", (629878, 375605, 431, -3270, 1002644)),
    ("DATA", "Profit for the financial year (FY2021)", (None, 44279, None, None, 44279)),
    ("DATA", "Losses on derivatives designated as cash flow hedges", (None, None, None, -180323, -180323)),
    ("DATA", "Financial assets at fair value through OCI - realised gain", (None, None, 101, None, 101)),
    ("TOTAL", "At 31 October 2021", (629878, 419884, 532, -183593, 866701)),
    ("DATA", "Profit for the financial year (FY2022)", (None, 52735, None, None, 52735)),
    ("DATA", "Gains on derivatives designated as cash flow hedges", (None, None, None, 255267, 255267)),
    ("DATA", "Financial assets at fair value through OCI - realised loss", (None, None, -24, None, -24)),
    ("TOTAL", "At 31 October 2022", (629878, 472619, 508, 71674, 1174679)),
    ("DATA", "Profit for the financial year (FY2023)", (None, 56037, None, None, 56037)),
    ("DATA", "Losses on derivatives designated as cash flow hedges", (None, None, None, -43248, -43248)),
    ("DATA", "Financial assets at fair value through OCI - realised loss", (None, None, 40, None, 40)),
    ("TOTAL", "At 31 October 2023", (629878, 528656, 548, 28426, 1187508)),
    ("DATA", "Profit for the financial year (FY2024)", (None, 47944, None, None, 47944)),
    ("DATA", "Gains on derivatives designated as cash flow hedges", (None, None, None, 172853, 172853)),
    ("DATA", "Financial assets at fair value through OCI - realised loss", (None, None, -178, None, -178)),
    ("TOTAL", "At 31 October 2024", (629878, 576600, 370, 201279, 1408127)),
    ("DATA", "Profit for the financial year (FY2025)", (None, 61644, None, None, 61644)),
    ("DATA", "Losses on derivatives designated as cash flow hedges", (None, None, None, -43294, -43294)),
    ("DATA", "Financial assets at fair value through OCI - realised gain", (None, None, 228, None, 228)),
    ("TOTAL", "At 31 October 2025", (629878, 638244, 598, 157985, 1426705)),
]
bw.add_equity_changes_sheet(
    title="TD Bank Europe Limited — Statement of Changes in Equity",
    subtitle="Entity/Company basis, CAD'000. Chronological roll-forward, 1 November 2020 to 31 October 2025 - "
    "zero undocumented plug rows; called up share capital unchanged (CAD629,878k) throughout the window.",
    headers=EQ_HEADERS,
    rows=EQ_ROWS,
    sources_text=AR_SOURCES_NOTE + "\n\n" + PRESENTATION_NOTE,
    source_height=280,
)

bw.add_cash_flow_sheet(
    title="TD Bank Europe Limited — Cash Flow Statement",
    subtitle="Pillar-3-only build: no cash-flow statement published under the entity's applicable exemption.",
    rows=[("SECTION", "No Statement of Cash Flows is published by this entity", {})],
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=190,
    unit_suffix=" (not disclosed)",
)

AQ_NOTE = (
    "TDBEL is a treasury/wholesale bank, not a retail or commercial lender: its credit exposure is overwhelmingly "
    "cash at central banks, interbank placements with its ultimate parent, and a large government/other debt "
    "securities book, plus (FY2021-FY2023 only) a small, now wound-down corporate lending book. As at each of "
    "31 October 2021-2025, ALL disclosed credit exposure (cash, loans and advances to banks, loans and advances to "
    "customers where applicable, and debt securities at amortised cost) was classified Stage 1 (performing) for IFRS "
    "9 expected credit loss purposes - a genuine finding confirmed by reading each year's own notes, not an omission. "
    "The FY2021 report's own FY2020 comparative did carry a Stage 2 balance (CAD472,886) within loans and advances to "
    "customers, outside this workbook's FY2021-FY2025 window. Cash and loans and advances to banks carry a CAD Nil "
    "ECL allowance in every year (confirmed explicitly in each year's own note)."
)
AQ_ROWS = [
    ("SECTION", "Credit-risk-bearing balance sheet exposure by category", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 163611, "FY2024": 960678, "FY2023": 135911, "FY2022": 84054, "FY2021": 1009106}),
    ("DATA", "Loans and advances to banks", {"FY2025": 512755, "FY2024": 1310183, "FY2023": 319740, "FY2022": 285427, "FY2021": 293637}),
    ("DATA", "Loans and advances to customers, net of allowance for credit losses", {"FY2023": 22977, "FY2022": 70648, "FY2021": 176208}),
    ("DATA", "Debt securities at amortised cost, net of allowance for credit losses", {"FY2025": 23455915, "FY2024": 21297771, "FY2023": 21193385, "FY2022": 19221927, "FY2021": 16375260}),
    ("TOTAL", "Total in-scope credit exposure (excludes derivatives, fixed assets, tax and other non-credit assets)", {"FY2025": 24132281, "FY2024": 23568532, "FY2023": 21672399, "FY2022": 21122036, "FY2021": 18754617}),
    ("SECTION", "Expected credit loss (ECL) allowance by category - all Stage 1 throughout", {}),
    ("DATA", "Cash and balances at central banks - ECL allowance", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Loans and advances to banks - ECL allowance", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Loans and advances to customers - ECL allowance", {"FY2023": 21, "FY2022": 12, "FY2021": 68}),
    ("DATA", "Debt securities at amortised cost - ECL allowance (provision for credit losses)", {"FY2025": 314, "FY2024": 289, "FY2023": 170, "FY2022": 36, "FY2021": 112}),
    ("SECTION", "Credit quality", {}),
    ("DATA", "Stage 1 (performing) share of in-scope credit exposure", {"FY2025": "100%", "FY2024": "100%", "FY2023": "100%", "FY2022": "100%", "FY2021": "100%"}),
]
bw.add_asset_quality_sheet(
    title="TD Bank Europe Limited — Asset Quality",
    subtitle="Entity/Company basis, CAD'000 unless noted. " + AQ_NOTE,
    rows=AQ_ROWS,
    sources_text=AR_SOURCES_NOTE + "\n\n" + AQ_NOTE,
    first_col_width=72,
    source_height=340,
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows,
        p3_sources(),
        note=note,
        first_col_width=60,
        source_height=250,
    )


# All amounts are as reported in CAD MM. The 2021 values are the comparative
# column in the FY2022 report and are separately identified in the note below.
CET1 = {"FY2025": 1269, "FY2024": 1206, "FY2023": 1159, "FY2022": 1103, "FY2021": 1050}
RWA = {"FY2025": 801, "FY2024": 805, "FY2023": 1635, "FY2022": 1261, "FY2021": 1096}
CET1_RATIO = {"FY2025": "158%", "FY2024": "150%", "FY2023": "71%", "FY2022": "87%", "FY2021": "96%"}
LEVERAGE_EXPOSURE = {"FY2025": 25214, "FY2024": 23692, "FY2023": 23004, "FY2022": 23408, "FY2021": 20484}
LEVERAGE_RATIO = {"FY2025": "5.0%", "FY2024": "5.1%", "FY2023": "5.0%", "FY2022": "4.7%", "FY2021": "5.1%"}
LCR = {"FY2025": "4039%", "FY2024": "3170%", "FY2023": "2575%", "FY2022": "29989%", "FY2021": "18136%"}
NSFR = {"FY2025": "5467%", "FY2024": "5240%", "FY2023": "6804%", "FY2022": "8307%", "FY2021": "800%"}

TRANSITION_NOTE = (
    "FY2021 is taken from the 2021 comparative column in the FY2022 TDBEL Pillar 3 report. The TD regulatory page "
    "states that prior-year disclosures were previously included in the Toronto-Dominion Investments B.V. report at "
    "UK-consolidation level, while later reports are solo TDBEL. Treat FY2021 as a transition/comparative year and "
    "do not interpret the full series as basis-homogeneous."
)

metric("CET1 Capital", "CAD MM", [("Common Equity Tier 1 (CET1) capital", CET1)], TRANSITION_NOTE)
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", CET1_RATIO)], TRANSITION_NOTE)
metric("Tier 1 Capital", "CAD MM", [("Tier 1 capital", CET1)], "TDBEL reports no AT1 capital; Tier 1 equals CET1 in each disclosed year.\n" + TRANSITION_NOTE)
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CET1_RATIO)], TRANSITION_NOTE)
metric("Total Capital", "CAD MM", [("Total capital", CET1)], "TDBEL reports no AT1 or Tier 2 capital; total capital equals CET1 in each disclosed year.\n" + TRANSITION_NOTE)
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", CET1_RATIO)], TRANSITION_NOTE)
metric("Total RWAs", "CAD MM", [("Total risk-weighted exposure amount", RWA)], TRANSITION_NOTE)

RWA_BREAKDOWN_NOTE = (
    "FY2021's category-level RWA split is a genuine access gap, not an omission. Checked directly: Table 4 (Capital "
    "requirements and risk weighted assets) - the actual source table for this sheet - carries no prior-year "
    "comparative column in ANY TDBEL Pillar 3 vintage reviewed. The FY2022 report's Table 4 (p.14) shows only the "
    "FY2022 column; the FY2023 report's Table 4 (p.14) shows only the FY2023 column (not even FY2022). This is "
    "unlike Tables 2, 3, 6 and 7 in the same reports (Capital Ratio, Capital Resources, CCyB Requirement, Leverage "
    "Ratio), which do carry a one-year-prior comparative - so Table 4 specifically has never published a FY2021 "
    "category split, in the FY2022 report or anywhere else. The FY2022 report's Appendix 1 Table 21 (Key Metrics) "
    "and Table 6 (CCyB Requirement) do give the FY2021 Total risk-weighted exposure amount (CAD1,096MM, already on "
    "file in the Total RWAs sheet) as a single comparative figure, but with no category breakdown - consistent with "
    "the entity note that FY2021 was disclosed under a different consolidated entity's Pillar 3 report at the time. "
    "Category rows are correctly left blank for FY2021.\n"
    "\"Large Exposure\" is included as its own category (reported as CAD0MM/nil every year) because the source's own "
    "Table 4 lists it as a fifth RWA component alongside Credit Risk, Market Risk, CVA Risk and Operational Risk.\n"
    "The \"Credit Risk (including CCR)\" category's own sub-breakdown (by exposure class - Institutions, Covered "
    "Bonds, and Corporates until the FY2024 wind-down) changes composition year to year as the corporate lending book "
    "runs off; only the category-level total is shown here for a consistent 5-year row.\n" + TRANSITION_NOTE
)
bw.add_rwa_breakdown_sheet(
    title="TD Bank Europe Limited — RWA Breakdown",
    subtitle="CAD MM, Pillar 3 UK OV1-style category split (Table 4: Capital requirements and risk weighted assets).",
    rows=[
        ("SECTION", "Risk-weighted assets by category", {}),
        ("DATA", "Credit Risk (including counterparty credit risk)", {"FY2025": 262, "FY2024": 286, "FY2023": 427, "FY2022": 705}),
        ("DATA", "Market Risk", {"FY2025": 349, "FY2024": 317, "FY2023": 1012, "FY2022": 386}),
        ("DATA", "CVA Risk", {"FY2025": 30, "FY2024": 42, "FY2023": 38, "FY2022": 42}),
        ("DATA", "Operational Risk", {"FY2025": 160, "FY2024": 160, "FY2023": 158, "FY2022": 128}),
        ("DATA", "Large Exposure", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0}),
        ("TOTAL", "Total risk-weighted exposure amount", RWA),
    ],
    sources_text=p3_sources() + "\n\n" + RWA_BREAKDOWN_NOTE,
    first_col_width=58,
    source_height=310,
    unit_suffix=" (CAD MM)",
)
metric(
    "Leverage Ratio",
    "CAD MM / %",
    [
        ("Total exposure measure excluding claims on central banks", LEVERAGE_EXPOSURE),
        ("Leverage ratio excluding claims on central banks", LEVERAGE_RATIO),
    ],
    TRANSITION_NOTE,
)
metric("LCR", "%", [("Liquidity coverage ratio", LCR)], TRANSITION_NOTE)
metric(
    "NSFR",
    "%",
    [("Net stable funding ratio", NSFR)],
    "The FY2025 report's introductory key-metrics table states 5,820% for FY2025, while Appendix 1 Table 21 states "
    "5,467%; this workbook uses the Appendix 1 value and preserves the discrepancy in this note.\n" + TRANSITION_NOTE,
)
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "No numeric MREL ratio was identified in the reviewed 2021 comparative or FY2022-FY2025 TD Bank Europe Pillar 3 reports."},
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit="CAD MM",
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 24303535, "FY2024": 23701833, "FY2023": 21902569, "FY2022": 21411125, "FY2021": 19119360}),
        ("Debt securities at amortised cost", {"FY2025": 23455915, "FY2024": 21297771, "FY2023": 21193385, "FY2022": 19221927, "FY2021": 16375260}),
        ("Other deposits (customer/wholesale funding)", {"FY2025": 21016787, "FY2024": 20690780, "FY2023": 20161902, "FY2022": 19925444, "FY2021": 17969614}),
        ("Total shareholder's equity", {"FY2025": 1426705, "FY2024": 1408127, "FY2023": 1187508, "FY2022": 1174679, "FY2021": 866701}),
    ],
    balance_sheet_unit="CAD'000",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 88609, "FY2024": 75348, "FY2023": 69984, "FY2022": 55340, "FY2021": 31064}),
        ("Total operating expense", {"FY2025": -8286, "FY2024": -13812, "FY2023": -23995, "FY2022": -15647, "FY2021": -11288}),
        ("Profit for the financial year", {"FY2025": 61644, "FY2024": 47944, "FY2023": 56037, "FY2022": 52735, "FY2021": 44279}),
    ],
    income_statement_unit="CAD'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1408127, "FY2024": 1187508, "FY2023": 1174679, "FY2022": 866701, "FY2021": 1002644}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 18578, "FY2024": 220619, "FY2023": 12829, "FY2022": 307978, "FY2021": -135943}),
        ("Closing equity", {"FY2025": 1426705, "FY2024": 1408127, "FY2023": 1187508, "FY2022": 1174679, "FY2021": 866701}),
    ],
    equity_changes_unit="CAD'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Tier 1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", CET1_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note=(
        "Balance Sheet/Profit & Loss/Statement of Changes in Equity figures are in CAD'000 (Companies House Annual "
        "Report basis); Pillar 3 ratios and the individual Pillar 3/RWA Breakdown sheets are in CAD MM - the two "
        "sources use different reporting units, reproduced as published. No cash-flow totals are shown because the "
        "entity's accounts take the applicable cash-flow-statement exemption. " + TRANSITION_NOTE
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/TD BANK EUROPE FINANCIALS.xlsx")
