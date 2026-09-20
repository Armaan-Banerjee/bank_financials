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


DEBT_SECURITIES_NOTE = (
    "DEBT SECURITIES BREAKDOWN: the 'Debt securities at amortised cost - ...' sub-rows below the renamed "
    "'Total debt securities at amortised cost, net of allowance for credit losses' line are transcribed from "
    "each year's own Note 13/14 'Debt Securities' of the Notes to the financial statements, which splits the "
    "balance by issuer type (Government securities vs. Other debt securities) and separately states the "
    "Provision for credit losses deducted to reach the net total; the note gives no measurement-basis split "
    "(100% of the balance is at amortised cost - no FVOCI/FVTPL debt securities line exists) and does not "
    "identify which sovereign(s) 'Government securities' refers to:\n"
    "FY2025/FY2024: Note 13, p.48 (image-rendered PDF page; scanned/image-only filing, OCR-transcribed) - "
    + AR_URL["FY2025"] + "\n"
    "FY2023/FY2022: Note 14, p.54 (image-rendered PDF page; scanned/image-only filing, OCR-transcribed) - "
    + AR_URL["FY2023"] + "\n"
    "FY2021: Note 14, p.50 (image-rendered PDF page; scanned/image-only filing, OCR-transcribed) - "
    + AR_URL["FY2021"] + "\n"
    "Each year's three sub-rows sum exactly to that year's headline total, e.g. FY2025: 16,473,157 + 6,983,072 "
    "- 314 = 23,455,915 (verified for all 5 years)."
)


def statement(kind_label, name, rows, first_col_width=58, extra_note=None, source_height=280):
    fn = {
        "balance_sheet": bw.add_balance_sheet_sheet,
        "income_statement": bw.add_income_statement_sheet,
    }[kind_label]
    sources_text = AR_SOURCES_NOTE + "\n\n" + PRESENTATION_NOTE
    if extra_note:
        sources_text += "\n\n" + extra_note
    fn(
        title=f"TD Bank Europe Limited — {name}",
        subtitle="Entity/Company basis, CAD'000 unless noted - see the equity ladder/asset quality units in each sheet's own subtitle.",
        rows=rows,
        sources_text=sources_text,
        first_col_width=first_col_width,
        source_height=source_height,
        unit_suffix=" (CAD'000)",
    )


BS_ROWS = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 163611, "FY2024": 960678, "FY2023": 135911, "FY2022": 84054, "FY2021": 1009106}),
    ("DATA", "Total debt securities at amortised cost, net of allowance for credit losses", {"FY2025": 23455915, "FY2024": 21297771, "FY2023": 21193385, "FY2022": 19221927, "FY2021": 16375260}),
    ("DATA", "Debt securities at amortised cost - Government securities", {"FY2025": 16473157, "FY2024": 14864668, "FY2023": 14979772, "FY2022": 14114679, "FY2021": 12566303}),
    ("DATA", "Debt securities at amortised cost - Other debt securities", {"FY2025": 6983072, "FY2024": 6433392, "FY2023": 6213783, "FY2022": 5107284, "FY2021": 3809069}),
    ("DATA", "Debt securities at amortised cost - Provision for credit losses", {"FY2025": -314, "FY2024": -289, "FY2023": -170, "FY2022": -36, "FY2021": -112}),
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
statement("balance_sheet", "Balance Sheet", BS_ROWS, extra_note=DEBT_SECURITIES_NOTE, source_height=360)

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
    # Not a line the source statement itself prints - the Company's own
    # income statement has no combined income subtotal, going straight from
    # these five income lines to the expense lines. This row is simply their
    # sum (ties exactly to Profit on ordinary activities before taxation net
    # of the expense/credit-loss lines below in every year, e.g. FY2025
    # 88609+222-566+2666+0=90931, and 90931-8286-25=82620), added
    # 2026-09-07 so cost-to-income analysis has a "Total operating income"
    # denominator to work from.
    ("TOTAL", "Total operating income (sum of the five income lines above - not itself a printed subtotal)", {
        "FY2025": 90931, "FY2024": 75605, "FY2023": 93709, "FY2022": 87230, "FY2021": 73161,
    }),
    ("DATA", "Personnel expenses", {"FY2025": 1265, "FY2024": -5342, "FY2023": -10029, "FY2022": -7063, "FY2021": -5869}),
    ("DATA", "Other expenses", {"FY2025": -9551, "FY2024": -8470, "FY2023": -13966, "FY2022": -8584, "FY2021": -5419}),
    # Not a line the source statement itself prints - the Company's own
    # income statement has no combined opex subtotal either. This row is
    # simply their sum (Personnel expenses + Other expenses, excluding
    # Credit loss (expense)/recovery just below, kept out of opex per this
    # project's convention of separating credit-related items from operating
    # costs), added 2026-09-07 so cost-to-income analysis has a "Total
    # operating expenses" numerator to work from.
    ("TOTAL", "Total operating expenses (sum of Personnel expenses + Other expenses above - not itself a printed subtotal)", {
        "FY2025": -8286, "FY2024": -13812, "FY2023": -23995, "FY2022": -15647, "FY2021": -11288,
    }),
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

# ---------------------------------------------------------------------------
# KM1 Key Metrics - TDBEL's own "Table 21: Key Metrics" in Appendix 11.1 of
# each year's Pillar 3 Disclosure, reproduced whole in TDBEL's own row order,
# labels and printed precision.
#
# THE TABLE IS THE TEMPLATE EVEN THOUGH IT IS NUMBERED NOWHERE AND NEVER SAYS
# "KM1". It carries the template's full row set - available own funds, RWEA,
# capital ratios, the SREP row, the seven buffer rows, leverage, the additional
# leverage-ratio disclosures, the five LCR rows and the three NSFR rows - with
# the template's own section headings. Row numbers are simply not printed, so
# none are invented here; the rows appear in TDBEL's order.
#
# Each column comes from the edition in which that year is the REPORTING year.
# FY2021 is deliberately blank - see KM1_SOURCES.
# ---------------------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds (amounts) (CAD MM)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) capital", {"FY2025": 1269, "FY2024": 1206, "FY2023": 1159, "FY2022": 1103}),
    ("DATA", "Tier 1 capital", {"FY2025": 1269, "FY2024": 1206, "FY2023": 1159, "FY2022": 1103}),
    ("DATA", "Total capital", {"FY2025": 1269, "FY2024": 1206, "FY2023": 1159, "FY2022": 1103}),
    ("SECTION", "Risk-weighted exposure amounts (CAD MM)", {}),
    ("DATA", "Total risk-weighted exposure amount", {"FY2025": 801, "FY2024": 805, "FY2023": 1635, "FY2022": 1261}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Common Equity Tier 1 ratio (%)", {"FY2025": "158%", "FY2024": "150%", "FY2023": "71%", "FY2022": "87%"}),
    ("DATA", "Tier 1 ratio (%)", {"FY2025": "158%", "FY2024": "150%", "FY2023": "71%", "FY2022": "87%"}),
    ("DATA", "Total capital ratio (%)", {"FY2025": "158%", "FY2024": "150%", "FY2023": "71%", "FY2022": "87%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Total SREP own funds requirements (%)", {"FY2025": "16.5%", "FY2024": "16.5%", "FY2023": "13.0%", "FY2022": "13.0%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Capital conservation buffer (%)", {"FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.5%", "FY2022": "2.5%"}),
    # Printed as "-" in every edition and in every column - re-read in all four
    # PDFs on 2026-09-18. The dash is TDBEL saying the requirement does not
    # apply to it, so the cell carries the dash: not a blank, and not a zero.
    ("DATA", "Conservation buffer due to macro-prudential or systemic risk identified at the level of a Member State (%)",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-"}),
    ("DATA", "Institution specific countercyclical capital buffer (%)",
     {"FY2025": "1.21%", "FY2024": "1.15%", "FY2023": "1.58%", "FY2022": "0.04%"}),
    ("DATA", "Systemic risk buffer (%)",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-"}),
    ("DATA", "Global Systemically Important Institution buffer (%)",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-"}),
    ("DATA", "Other Systemically Important Institution buffer",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-"}),
    ("DATA", "Combined buffer requirement (%)", {"FY2025": "3.7%", "FY2024": "3.7%", "FY2023": "4.1%", "FY2022": "2.5%"}),
    ("DATA", "Overall capital requirements (%)", {"FY2025": "20.2%", "FY2024": "20.1%", "FY2023": "17.1%", "FY2022": "23.5%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "Total exposure measure excluding claims on central banks (CAD MM)",
     {"FY2025": 25214, "FY2024": 23692, "FY2023": 23004, "FY2022": 23408}),
    ("DATA", "Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "5.0%", "FY2024": "5.1%", "FY2023": "5.0%", "FY2022": "4.7%"}),
    # Whole block first printed in the FY2023 edition. The FY2022 edition does
    # not contain these rows at all, so FY2022 is BLANK, not zero - and the
    # FY2023 edition's own 2022 comparative prints "-" for all four, which is
    # also a blank rather than a zero.
    ("SECTION", "Additional leverage ratio disclosure requirements (block first printed in the FY2023 edition)", {}),
    ("DATA", "Leverage ratio including claims on central banks (%)", {"FY2025": "5.0%", "FY2024": "5.1%", "FY2023": "5.0%"}),
    ("DATA", "Average leverage ratio excluding claims on central banks (%)", {"FY2025": "5.1%", "FY2024": "5.1%", "FY2023": "5.0%"}),
    ("DATA", "Average leverage ratio including claims on central banks (%)", {"FY2025": "5.1%", "FY2024": "5.1%", "FY2023": "5.0%"}),
    ("DATA", "Countercyclical leverage ratio buffer (%)", {"FY2025": "0.42%", "FY2024": "0.40%", "FY2023": "0.55%"}),
    # First printed in the FY2025 edition, and printed as a ZERO, not a dash -
    # so the zero is kept while the four buffer rows above stay blank.
    ("DATA", "Additional leverage ratio buffer (%) [row first printed in the FY2025 edition]", {"FY2025": "0.0%"}),
    ("SECTION", "Liquidity Coverage Ratio (CAD MM, except the ratio)", {}),
    ("DATA", "Total high-quality liquid assets (HQLA) (Weighted value -average)",
     {"FY2025": 23547, "FY2024": 21755, "FY2023": 20141, "FY2022": 18093}),
    ("DATA", "Cash outflows - Total weighted value", {"FY2025": 1102, "FY2024": 2004, "FY2023": 1135, "FY2022": 241}),
    ("DATA", "Cash inflows - Total weighted value", {"FY2025": 519, "FY2024": 1317, "FY2023": 352, "FY2022": 181}),
    ("DATA", "Total net cash outflows (adjusted value)", {"FY2025": 583, "FY2024": 686, "FY2023": 782, "FY2022": 60}),
    ("DATA", "Liquidity coverage ratio (%)", {"FY2025": "4039%", "FY2024": "3,170%", "FY2023": "2575%", "FY2022": "29989%"}),
    ("SECTION", "Net Stable Funding Ratio (CAD MM, except the ratio)", {}),
    ("DATA", "Total available stable funding", {"FY2025": 22470, "FY2024": 22006, "FY2023": 21441, "FY2022": 21073}),
    ("DATA", "Total required stable funding", {"FY2025": 411, "FY2024": 420, "FY2023": 315, "FY2022": 254}),
    ("DATA", "NSFR ratio (%)", {"FY2025": "5467%", "FY2024": "5,240%", "FY2023": "6804%", "FY2022": "8307%"}),
]

KM1_SOURCES = (
    "Sources - TD Bank Europe Limited's own 'Table 21: Key Metrics', Appendix 11.1 'Key Metrics' of each year's "
    "Pillar 3 Disclosure. Amounts in CAD millions, ratios as printed. TDBEL SOLO basis (the reports state TDBEL "
    "is the only PRA-regulated subsidiary in the UK and that the report is prepared at solo level). Each column "
    "comes from the edition in which that year is the REPORTING year, never a later edition's comparative:\n"
    "FY2025: TDBEL Pillar 3 Disclosure, year ended 31 October 2025, Table 21, printed pp.34-35 - " + P3_URL["FY2025"] + "\n"
    "FY2024: TDBEL Pillar 3 Disclosure, year ended 31 October 2024, Table 21, printed p.34 - " + P3_URL["FY2024"] + "\n"
    "FY2023: TDBEL Pillar 3 Disclosure, year ended 31 October 2023, Table 21, printed pp.35-36 - " + P3_URL["FY2023"] + "\n"
    "FY2022: TDBEL Pillar 3 Disclosure, year ended 31 October 2022, Table 21, printed p.35 - " + P3_URL["FY2022"] + "\n\n"
    "THE TABLE BREAKS ACROSS TWO PAGES IN TWO OF THE FOUR EDITIONS, which a one-page citation would hide. The "
    "FY2023 edition prints everything down to 'Total available stable funding' on p.35 and the last two rows "
    "('Total required stable funding', 'NSFR ratio') alone at the top of p.36; the FY2025 edition breaks in the "
    "same place, with the three NSFR rows on p.35. The FY2024 and FY2022 editions print the table whole. Both "
    "page ranges are cited above.\n\n"
    "THIS IS THE KM1 TEMPLATE EVEN THOUGH TDBEL NEVER WRITES 'KM1' AND PRINTS NO ROW NUMBERS. The test applied "
    "is the row set, not the title or the numbering: the table carries the template's own section headings "
    "('Available own funds (amounts)', 'Risk-weighted exposure amounts', 'Capital ratios (as a percentage of "
    "risk-weighted exposure amount)', 'Additional own funds requirements based on SREP...', 'Combined buffer "
    "requirement...', 'Leverage ratio', 'Additional leverage ratio disclosure requirements', 'Liquidity Coverage "
    "Ratio', 'Net Stable Funding Ratio') and the rows that belong under each. NO ROW NUMBERS ARE INVENTED HERE - "
    "the rows are reproduced unnumbered, exactly as TDBEL prints them.\n"
    "      DO NOT CONFUSE IT WITH TABLE 1. Each edition also prints a 'Table 1: Key regulatory metrics' in "
    "section 1.2.1 with just FOUR rows (CET1 Ratio, Leverage Ratio, LCR, NSFR). That is a summary, not the "
    "template, and the two disagree: the FY2025 Table 1 states an NSFR of 5820% where Table 21 states 5467%. "
    "Table 21 is used here and on the NSFR sheet, and the disagreement is recorded rather than reconciled.\n\n"
    "A DASH IS A DASH, AND IT IS NOT A ZERO. Four buffer rows - 'Conservation buffer due to macro-prudential or "
    "systemic risk...', 'Systemic risk buffer', 'Global Systemically Important Institution buffer' and 'Other "
    "Systemically Important Institution buffer' - are printed as '-' by TDBEL in EVERY edition and in every "
    "column, re-read in all four PDFs on 2026-09-18. Every one of those cells carries a literal '-' above: the "
    "dash is TDBEL stating that no such requirement applies to it, which is a different statement from silence. "
    "A BLANK cell on this sheet means the other thing - that TDBEL printed no such row, or no figure in it, in "
    "the edition for that year. By contrast 'Additional leverage ratio buffer (%)' is printed as '0.0%' in the "
    "FY2025 edition, and a printed zero is a measured zero and stays a number.\n\n"
    "ROW SET DRIFT, AND WHY FY2022 IS BLANK ON FIVE ROWS. The whole 'Additional leverage ratio disclosure "
    "requirements' block appears first in the FY2023 edition; the FY2022 edition does not contain those rows at "
    "all. A row the bank did not print is blank, not zero - and the FY2023 edition's own 2022 comparative prints "
    "'-' for all four of them, so neither route yields a figure. 'Additional leverage ratio buffer (%)' appears "
    "first in the FY2025 edition and is blank in the three earlier columns for the same reason. Nothing is "
    "back-filled.\n\n"
    "A RESTATEMENT FOUND AND NOT USED - THIS IS WHY EACH COLUMN COMES FROM ITS OWN EDITION. 'Overall capital "
    "requirements (%)' for FY2022 is 23.5% in the FY2022 edition (its own reporting year) and 15.5% in the "
    "FY2023 edition's 2022 comparative column. The FY2022 edition's own 23.5% is shown above. Both figures are "
    "TDBEL's; they are not reconciled, and the later one remains visible in the FY2023 document.\n\n"
    "PRECISION AND NUMBER FORMATTING ARE THE BANK'S OWN AND CHANGE BETWEEN EDITIONS. The FY2024 edition prints "
    "the LCR and NSFR with a thousands separator ('3,170%', '5,240%') while the FY2025, FY2023 and FY2022 "
    "editions print them without ('4039%', '2575%', '29989%', '6804%', '8307%'). Buffer rows are printed to two "
    "decimals and ratio rows to one or none. Nothing is re-rounded or reformatted to a common style.\n\n"
    "FY2021 IS BLANK, AND THAT IS AN ACCESS FAILURE ON OUR SIDE - NOT A STATEMENT THAT NOTHING WAS PUBLISHED. "
    "Checked 2026-09-16 on TD's own regulatory page (" + REGULATORY_PAGE + "): it LISTS a 'Pillar 3 Disclosure - "
    "2021' under the 'TD Bank Europe Limited Pillar 3 Disclosure' heading, alongside the 2022-2025 editions, so "
    "an FY2021 TDBEL edition demonstrably exists. Its link is dead: "
    "https://www.tdsecurities.com/tds/document/Pillar-3-Disclosure-2021 returns HTTP 200 with Content-Type "
    "text/html and redirects to https://www.tdsecurities.com/error/404-en.html - a SOFT-404, caught only because "
    "status alone was not trusted. The 2022, 2023, 2024 and 2025 links from the same page all return real "
    "application/pdf bodies with %PDF magic bytes on the same date, so this is link rot on one document, not a "
    "block and not an outage. Wayback was itself offline during this check and could not be used as the "
    "fallback. A full FY2021 KM1 column DOES exist as the FY2022 edition's 2021 comparative and is deliberately "
    "not used here, because every column on this sheet comes from the edition in which that year is the "
    "reporting year. For the record, that comparative prints: CET1 / Tier 1 / Total capital all 1,050; total "
    "RWEA 1,096; all three capital ratios 96%; total SREP own funds requirements 13.0%; capital conservation "
    "buffer 2.5%; institution specific countercyclical capital buffer 0.01%; combined buffer requirement 2.5%; "
    "overall capital requirements 23.5%; total exposure measure excluding claims on central banks 20,484; "
    "leverage ratio excluding claims on central banks 5.1%; HQLA 17,258; cash outflows 381; cash inflows 285; "
    "total net cash outflows 95; LCR 18136%; total available stable funding 18,892; total required stable "
    "funding 2,361; NSFR 800%. Those figures do appear on this workbook's single-metric sheets, captioned there "
    "as a comparative. A FUTURE PASS SHOULD RETRY THE 2021 LINK AND WAYBACK before treating FY2021 as settled.\n\n"
    "PARENT CHECK DONE, AND IT DOES NOT HELP HERE. A subsidiary's figures usually live in the parent's Pillar 3, "
    "so the parent was checked first rather than last. TD's own regulatory page states: 'In prior years, TD Bank "
    "Europe Limited disclosures were included within the Toronto-Dominion Investments B.V. Pillar 3 disclosure "
    "report and completed at the UK consolidation level. The Toronto-Dominion Investments B.V. Pillar 3 report "
    "is FILED WITH THE RESPECTIVE FINANCIAL STATEMENTS. TD Bank Europe Limited is now the sole regulated entity "
    "of TD Securities in the UK, thus the Pillar 3 report is now prepared at the solo level.' So (a) the "
    "parent-document route applies to years BEFORE this workbook's range, not to FY2021-FY2025, which are all "
    "TDBEL-solo editions; and (b) the TDI B.V. report is not published on the web at all - it is filed with that "
    "Dutch entity's financial statements - so there is no parent Pillar 3 to read for a TDBEL column. The "
    "ultimate parent, The Toronto-Dominion Bank, reports on the Canadian OSFI basis, which is a different "
    "framework and not a source for a UK KM1.\n\n"
    "NO SECOND ENTITY BLOCK IN THESE DOCUMENTS. Each edition prints Table 21 once, with two date columns (the "
    "reporting year and its prior-year comparative) and no second entity basis beside it - confirmed by reading "
    "Appendix 11.1 to its end in all four editions. The columns were checked by date as well as by entity: no "
    "edition carries a column dated after its own reporting period.\n\n"
    "CURRENCY: this sheet is in CANADIAN DOLLARS (CAD millions), as TDBEL publishes it, and is not converted. "
    "The single-metric sheets in this workbook are on the same CAD MM basis.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="TD Bank Europe Limited — KM1 Key Metrics",
    subtitle="TDBEL's own 'Table 21: Key Metrics' (Appendix 11.1 of each year's Pillar 3 Disclosure) - the UK "
             "KM1 template, which TDBEL prints unnumbered and never labels 'KM1'. Solo basis, amounts in CAD "
             "millions, ratios as printed. FY2021 is blank because that edition's link on TD's own page is a "
             "dead soft-404 - see the source note; it is an access gap, not a non-disclosure.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=80,
    source_height=320,
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
    statements={"MREL Ratio": {
        **{y: "Not published – no MREL figure or mention in this year's TD Bank Europe Pillar 3 report (text-searched 2026-09-19)"
           for y in ("FY2025", "FY2024", "FY2023", "FY2022")},
        "FY2021": ("Not published – no FY2021 TDBEL Pillar 3 in Wayback CDX of tdsecurities.com/tds/document/ (first "
                   "is 2022); 2022 edition's FY2021 comparative has no MREL"),
    }},
    per_note={"MREL Ratio": "No numeric MREL ratio was identified in the reviewed 2021 comparative or FY2022-FY2025 TD Bank Europe Pillar 3 reports. "
                            "GA-020 (2026-09-19): the four editions (P3_URL) were re-fetched and searched for 'MREL', "
                            "'eligible liabilities' and 'resolution' - zero hits. A Wayback CDX listing of "
                            "tdsecurities.com/tds/document/* (295 URLs) shows 'Pillar-3-Disclosure-2022' as the "
                            "first UK Pillar 3; the '2021-TDS-UK-Disclosure' document there is a remuneration "
                            "disclosure, not a Pillar 3."},
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
