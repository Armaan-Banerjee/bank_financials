import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://redwoodbank.co.uk/media/howpdnen/2025-annual-report-and-accounts_redwood-bank-signed-150426.pdf"
AR2024_URL = "https://redwoodbank.co.uk/media/0h5hp3ku/2024-redwood-bank-annual-report-and-accounts.pdf"
AR2023_URL = "https://redwoodbank.co.uk/media/zrjnifqm/redwood-year-end-annual-report-and-accounts-2023-1.pdf"
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/09872265/filing-history"
CH2022_URL = "https://find-and-update.company-information.service.gov.uk/company/09872265/filing-history/MzM4NjEzNjAwN2FkaXF6a2N4/document?download=0&format=pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Redwood Bank Limited (company 09872265, FRN 755924) is the exact legal entity in the bank list. "
    "It is a UK-authorised bank and a wholly owned subsidiary of Redwood Financial Partners Limited. The annual "
    "reports present the Bank on a Company-only basis; no Group cash-flow statement has been substituted. The "
    "company was previously named Acorn Financial Partners Limited, but the name change occurred before the years "
    "covered and does not create an entity ambiguity."
)

CASH_FLOW_SOURCES = (
    "Sources - Redwood Bank Limited Company-only statement of cash flows, £:\n"
    f"FY2025: Redwood Bank Annual Report and Accounts 2025, p.50 - {AR2025_URL}\n"
    f"FY2024: Redwood Bank Annual Report and Accounts 2024, p.47 - {AR2024_URL}\n"
    f"FY2023: Redwood Bank Annual Report and Accounts 2023, p.59 - {AR2023_URL}\n"
    f"FY2022: Redwood Bank Limited full accounts made up to 31 December 2022 filed at Companies House, p.33 "
    f"(comparative column) - {CH2022_URL}\n"
    f"FY2021: Redwood Bank Limited full accounts made up to 31 December 2022 filed at Companies House, p.33 "
    f"(comparative column for 2021), with the 2021 account used as a cross-check, p.28 - {CH2022_URL}\n\n"
    "The FY2022 and FY2021 columns use later-year comparative columns where available, following the project rule "
    "to inspect comparatives before seeking separate documents. The FY2021 comparative presents a small internal "
    "reclassification of TFSME interest and financing cash: its operating subtotal is £15,466,786 and financing "
    "subtotal £28,300,000, while the standalone 2021 report prints £15,456,792 and £28,309,994. Both produce the "
    "same reported net cash increase of £23,972,927 and the same closing cash of £105,308,945; the later comparative "
    "is used consistently here.\n\n" + ENTITY_NOTE
)

P3_SOURCES = (
    "Sources - Redwood Bank Limited regulatory capital and liquidity KPIs:\n"
    f"FY2025/FY2024: Redwood Bank Annual Report and Accounts 2025, pp.17 and 26, own-funds table p.26 - {AR2025_URL}\n"
    f"FY2024/FY2023: Redwood Bank Annual Report and Accounts 2024, pp.16 and 68 - {AR2024_URL}\n"
    f"FY2023/FY2022: Redwood Bank Annual Report and Accounts 2023, pp.22 and 81, own-funds table pp.81-82 - {AR2023_URL}\n"
    f"FY2021: Redwood Bank Limited full accounts made up to 31 December 2022 filed at Companies House, pp.6 and 60 "
    f"(comparative column), cross-checked against the 2021 accounts pp.6 and 53 - {CH2022_URL}\n\n"
    "Redwood's public reports do not provide separate entity-level numeric disclosures for Total RWAs, leverage "
    "ratio, NSFR, or MREL. Those fields remain explicitly undisclosed rather than being derived from other ratios."
)

STATEMENTS_SOURCES = (
    "Sources - Redwood Bank Limited Company-only Balance Sheet / Profit & Loss / Statement of Changes in Equity, £:\n"
    f"FY2025/FY2024: Redwood Bank Annual Report and Accounts 2025, pp.47-49 - {AR2025_URL}\n"
    f"FY2024/FY2023: Redwood Bank Annual Report and Accounts 2024, pp.44-45 - {AR2024_URL}\n"
    f"FY2023/FY2022: Redwood Bank Annual Report and Accounts 2023, pp.56-58 - {AR2023_URL}\n"
    f"FY2021: Redwood Bank Limited full accounts made up to 31 December 2022 filed at Companies House, pp.29-31 "
    f"(2021 comparative column) - {CH2022_URL}\n\n"
    "RESTATEMENT NOTE: the FY2025 report presents a RESTATED FY2024 comparative Balance Sheet (Total assets "
    "£635,583,084) that differs from AR2024's own originally-published FY2024 figure (Total assets £635,400,816, "
    "a difference of £182,268), splitting 'Cash and balances at central banks' into a separate 'Loans and advances "
    "to banks' line and adding a 'Derivative assets'/'Fair value adjustments on hedged assets' split not present "
    "in the original AR2024 presentation. Following the project convention of using each year's own "
    "originally-published figure rather than a later restatement, the FY2024 column below reproduces AR2024's own "
    "figures, not AR2025's restated comparative.\n\n"
    "PRESENTATION NOTE: FY2025 splits 'Other assets and prepayments' into two lines ('Other assets' and "
    "'Prepayments and accrued income') and 'Other liabilities and accruals' into two lines ('Other liabilities' "
    "and 'Accruals and deferred income'); FY2024-FY2021 disclose each as a single combined line - both are shown "
    "as separate rows, populated only for the years that split them. 'Loans and advances to banks' and 'Fair "
    "value adjustments on hedged assets'/'Derivative assets' are new lines from FY2025 (FY2024's own figures fold "
    "these into other lines); blank for FY2023-FY2021. The Available-for-sale reserve was fully utilised by "
    "FY2023 year-end and the FY2024/FY2025 statements of changes in equity no longer carry the column - blank "
    "(nil) from FY2024 onward. P&L: FY2024-FY2025 disclose 'Fair value gains/(losses) on financial instruments' "
    "and a 'Total income' subtotal as separate lines; FY2021-FY2023 do not - net interest income flows directly "
    "into administrative expenses in those years' own statements, so 'Total income' is blank for FY2021-FY2023.\n\n"
    + ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Redwood Bank Limited mortgage portfolio arrears/impairment and loan loss provisions, £:\n"
    f"FY2025/FY2024: Redwood Bank Annual Report and Accounts 2025, pp.63-64 and 73-74 - {AR2025_URL}\n"
    f"FY2024/FY2023: Redwood Bank Annual Report and Accounts 2024, pp.60-61 and 70 - {AR2024_URL}\n"
    f"FY2023/FY2022: Redwood Bank Annual Report and Accounts 2023, pp.75 and 84 - {AR2023_URL}\n"
    f"FY2021: Redwood Bank Limited full accounts made up to 31 December 2022 filed at Companies House, pp.50 and "
    f"63 (2021 comparative column) - {CH2022_URL}\n\n"
    "The Bank lends only against fixed UK property (max 75% LTV) to SME/commercial and residential property "
    "investors; there is no IFRS 9 stage 1/2/3 disclosure (FRS 102 basis, not IFRS) - the Bank's own 'impaired / "
    "past due but not impaired / forborne' categorisation is used instead. 'Total impaired' combines 'past due and "
    "impaired' and 'not past due and impaired' where both are disclosed (FY2023 only; other years show impaired "
    "loans as entirely past due). Forborne totals are 'not past due and forborne' plus 'past due and forborne' "
    "where both exist; FY2022 and FY2021 forbearance was £nil. Gross loans and advances to customers (before "
    "deferred fee income and loan loss provisions) and derived NPL/coverage ratios are calculated from the same "
    "notes, not separately disclosed by the Bank.\n\n" + ENTITY_NOTE
)

bw = BankWorkbook("Redwood Bank Limited", YEARS, YEAR_LABEL, header_color="8B3A3A")

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 85516188, "FY2024": 115416225, "FY2023": 109250259, "FY2022": 84018745, "FY2021": 105308945}),
    ("DATA", "Treasury bills and gilts", {"FY2025": 20013691, "FY2024": 25011813, "FY2023": 73494617, "FY2022": 49958358, "FY2021": 49938351}),
    ("DATA", "Loans and advances to banks", {"FY2025": 8841755}),
    ("DATA", "Loans and advances to customers", {"FY2025": 490444848, "FY2024": 492244170, "FY2023": 413983306, "FY2022": 403371972, "FY2021": 369798691}),
    ("DATA", "Fair value adjustments on hedged assets", {"FY2025": 1302543}),
    ("DATA", "Derivative assets", {"FY2025": 0}),
    ("DATA", "Other assets and prepayments", {"FY2024": 1231228, "FY2023": 1037196, "FY2022": 853781, "FY2021": 652247}),
    ("DATA", "Other assets", {"FY2025": 1483513}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 1088724}),
    ("DATA", "Tangible fixed assets", {"FY2025": 104511, "FY2024": 151269, "FY2023": 174182, "FY2022": 166207, "FY2021": 182226}),
    ("DATA", "Intangible fixed assets", {"FY2025": 1132393, "FY2024": 1011135, "FY2023": 783820, "FY2022": 448996, "FY2021": 182069}),
    ("DATA", "Deferred tax assets", {"FY2025": 115182, "FY2024": 307517, "FY2023": 331990, "FY2022": 1442426, "FY2021": 1910683}),
    ("TOTAL", "Total assets", {"FY2025": 610043348, "FY2024": 635400816, "FY2023": 599055370, "FY2022": 540260485, "FY2021": 527973212}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Amounts due to banks", {"FY2024": 18726182, "FY2023": 38067988, "FY2022": 37862456, "FY2021": 37611747}),
    ("DATA", "Customer deposits", {"FY2025": 546762522, "FY2024": 552995571, "FY2023": 499967473, "FY2022": 447173300, "FY2021": 438038613}),
    ("DATA", "Derivative liabilities", {"FY2025": 1224574}),
    ("DATA", "Other liabilities and accruals", {"FY2024": 4994868, "FY2023": 4245490, "FY2022": 2898770, "FY2021": 1826748}),
    ("DATA", "Other liabilities", {"FY2025": 603027}),
    ("DATA", "Accruals and deferred income", {"FY2025": 2470155}),
    ("DATA", "Tax liabilities", {"FY2024": 303938, "FY2023": 222250}),
    ("DATA", "Subordinated debt", {"FY2025": 9000000, "FY2024": 9000000, "FY2023": 9000000, "FY2022": 9000000, "FY2021": 9000000}),
    ("TOTAL", "Total liabilities", {"FY2025": 560060278, "FY2024": 586020559, "FY2023": 551503201, "FY2022": 496934526, "FY2021": 486477108}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 111, "FY2024": 111, "FY2023": 111, "FY2022": 111, "FY2021": 111}),
    ("DATA", "Share premium reserve", {"FY2025": 47922405, "FY2024": 47922405, "FY2023": 47922405, "FY2022": 47922405, "FY2021": 47922405}),
    ("DATA", "Available-for-sale reserve", {"FY2023": 0, "FY2022": -21961, "FY2021": -54202}),
    ("DATA", "Retained earnings", {"FY2025": 2060554, "FY2024": 1457741, "FY2023": -370347, "FY2022": -4574596, "FY2021": -6372210}),
    ("TOTAL", "Total equity", {"FY2025": 49983070, "FY2024": 49380257, "FY2023": 47552169, "FY2022": 43325959, "FY2021": 41496104}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 610043348, "FY2024": 635400816, "FY2023": 599055370, "FY2022": 540260485, "FY2021": 527973212}),
]

bw.add_balance_sheet_sheet(
    title="Redwood Bank Limited — Balance Sheet",
    subtitle="Company-only basis, £. FY2021 uses the comparative column in the FY2022 Companies House filing; see source note.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=320,
    unit_suffix=" (£)",
)

pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 45241843, "FY2024": 49521006, "FY2023": 46123616, "FY2022": 28087329, "FY2021": 19924820}),
    ("DATA", "Interest payable", {"FY2025": -22521076, "FY2024": -23269459, "FY2023": -17294646, "FY2022": -7219223, "FY2021": -4789284}),
    ("TOTAL", "Net interest income", {"FY2025": 22720767, "FY2024": 26251547, "FY2023": 28828970, "FY2022": 20868106, "FY2021": 15135536}),
    ("DATA", "Fair value gains/(losses) on financial instruments", {"FY2025": 80899, "FY2024": -8932}),
    ("TOTAL", "Total income", {"FY2025": 22801666, "FY2024": 26242615}),
    ("DATA", "Administrative expenses", {"FY2025": -21265984, "FY2024": -21675255, "FY2023": -20509671, "FY2022": -16105258, "FY2021": -12922871}),
    ("TOTAL", "Operating profit before impairment charge", {"FY2025": 1535682, "FY2024": 4567360, "FY2023": 8319299, "FY2022": 4762848, "FY2021": 2212665}),
    ("DATA", "Impairment charge on loans and advances to customers", {"FY2025": -756168, "FY2024": -1869546, "FY2023": -2782364, "FY2022": -2496977, "FY2021": -38873}),
    ("TOTAL", "Profit before tax", {"FY2025": 779514, "FY2024": 2697814, "FY2023": 5536935, "FY2022": 2265871, "FY2021": 2173792}),
    ("DATA", "Tax (charge)/credit", {"FY2025": -176701, "FY2024": -869726, "FY2023": -1332686, "FY2022": -468257, "FY2021": 1910683}),
    ("TOTAL", "Profit for the year", {"FY2025": 602813, "FY2024": 1828088, "FY2023": 4204249, "FY2022": 1797614, "FY2021": 4084475}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Movement in available-for-sale investments", {"FY2023": 21961, "FY2022": 32241, "FY2021": -69078}),
    ("TOTAL", "Total comprehensive income", {"FY2025": 602813, "FY2024": 1828088, "FY2023": 4226210, "FY2022": 1829855, "FY2021": 4015397}),
]

bw.add_income_statement_sheet(
    title="Redwood Bank Limited — Profit & Loss",
    subtitle="Company-only basis, £. FY2021 uses the comparative column in the FY2022 Companies House filing; see source note.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=320,
    unit_suffix=" (£)",
)

equity_headers = ["Share capital", "Share premium", "Available-for-sale reserve", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2021", (111, 38022405, 14876, -10456685, 27580707)),
    ("DATA", "Profit for the year", (None, None, None, 4084475, 4084475)),
    ("DATA", "Other comprehensive loss for the year", (None, None, -69078, None, -69078)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, -69078, 4084475, 4015397)),
    ("DATA", "Issue of share capital", (None, 9900000, None, None, 9900000)),
    ("TOTAL", "Total transactions with owners, recognised directly in equity", (None, 9900000, None, None, 9900000)),
    ("TOTAL", "At 31 December 2021", (111, 47922405, -54202, -6372210, 41496104)),
    ("TOTAL", "At 1 January 2022", (111, 47922405, -54202, -6372210, 41496104)),
    ("DATA", "Profit for the year", (None, None, None, 1797614, 1797614)),
    ("DATA", "Other comprehensive income for the year", (None, None, 32241, None, 32241)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 32241, 1797614, 1829855)),
    ("TOTAL", "At 31 December 2022", (111, 47922405, -21961, -4574596, 43325959)),
    ("TOTAL", "At 1 January 2023", (111, 47922405, -21961, -4574596, 43325959)),
    ("DATA", "Profit for the year", (None, None, None, 4204249, 4204249)),
    ("DATA", "Other comprehensive income for the year", (None, None, 21961, None, 21961)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 21961, 4204249, 4226210)),
    ("TOTAL", "At 31 December 2023", (111, 47922405, None, -370347, 47552169)),
    ("TOTAL", "At 1 January 2024", (111, 47922405, None, -370347, 47552169)),
    ("DATA", "Profit for the year", (None, None, None, 1828088, 1828088)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, 1828088, 1828088)),
    ("TOTAL", "At 31 December 2024", (111, 47922405, None, 1457741, 49380257)),
    ("TOTAL", "At 1 January 2025", (111, 47922405, None, 1457741, 49380257)),
    ("DATA", "Profit for the year", (None, None, None, 602813, 602813)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, 602813, 602813)),
    ("TOTAL", "At 31 December 2025", (111, 47922405, None, 2060554, 49983070)),
]

bw.add_equity_changes_sheet(
    title="Redwood Bank Limited — Statement of Changes in Equity",
    subtitle="Company-only basis, £, chronological. Zero undocumented plug rows across all 5 years - every movement is profit for the year, an "
              "available-for-sale reserve fair value movement, or the FY2021 share issue.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=52,
    source_height=320,
)

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit for the year", {"FY2025": 602813, "FY2024": 1828088, "FY2023": 4204249, "FY2022": 1797614, "FY2021": 4084475}),
    ("DATA", "Amortisation of intangibles", {"FY2025": 359914, "FY2024": 336289, "FY2023": 216413, "FY2022": 133808, "FY2021": 85194}),
    ("DATA", "Depreciation of tangible assets", {"FY2025": 91501, "FY2024": 92566, "FY2023": 96581, "FY2022": 104682, "FY2021": 98689}),
    ("DATA", "Write off of fixed/intangible assets", {"FY2021": 0}),
    ("DATA", "Impairment charge on loans and advances to customers", {"FY2025": 756168, "FY2024": 1869546, "FY2023": 2782364, "FY2022": 2496977, "FY2021": 38873}),
    ("DATA", "Net increase in loans to banks", {"FY2025": -1870000}),
    ("DATA", "Net decrease/(increase) in loans to customers", {"FY2025": 1043154, "FY2024": -80130410}),
    ("DATA", "Net increase in customer deposits", {"FY2024": 53028098, "FY2023": 52794173, "FY2022": 9134687, "FY2021": 58428886}),
    ("DATA", "(Decrease)/increase in customer deposits", {"FY2025": -6233049}),
    ("DATA", "Increase in other liabilities", {"FY2024": 749378, "FY2023": 1346720, "FY2022": 1072022, "FY2021": 770530}),
    ("DATA", "(Decrease)/increase in other liabilities", {"FY2025": -1322763}),
    ("DATA", "Increase in other assets", {"FY2024": -194032, "FY2023": -183415, "FY2022": -201534, "FY2021": -112205}),
    ("DATA", "Increase in other assets", {"FY2025": -1390656}),
    ("DATA", "Net increase in loans to customers", {"FY2023": -13393698, "FY2022": -36070258, "FY2021": -45957889}),
    ("DATA", "Increase in accruals and deferred income", {"FY2025": -781191}),
    ("DATA", "Decrease/(increase) in payments and accrued income", {"FY2025": 49647}),
    ("DATA", "Increase in interest payable on TFSME", {"FY2023": 205532, "FY2022": 250709, "FY2021": 9994}),
    ("DATA", "(Decrease)/increase in interest payable on TFSME", {"FY2025": -226182, "FY2024": -241806}),
    ("DATA", "Redemption of TFSME", {"FY2025": -18500000, "FY2024": -19100000}),
    ("DATA", "Net increase in derivatives and hedged items", {"FY2025": -50510, "FY2024": -27459}),
    ("DATA", "Finance cost for subordinated debt", {"FY2025": 585000, "FY2024": 586603, "FY2023": 585000, "FY2022": 585000, "FY2021": 583397}),
    ("DATA", "Fair value change of treasury bills and gilts", {"FY2024": 0, "FY2023": 21961, "FY2022": 32241, "FY2021": -69078}),
    ("DATA", "Income tax", {"FY2025": -111603, "FY2024": 106161, "FY2023": 1332686, "FY2022": 468257, "FY2021": -1910683}),
    ("DATA", "Interest paid for subordinated debt", {"FY2025": -585000, "FY2024": -586603, "FY2023": -585000, "FY2022": -585000, "FY2021": -583397}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": -27582757, "FY2024": -41683581, "FY2023": 49423566, "FY2022": -20780795, "FY2021": 15466786}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchases of tangible fixed assets", {"FY2025": -44743, "FY2024": -69653, "FY2023": -104556, "FY2022": -88663, "FY2021": -22261}),
    ("DATA", "Purchases of intangible assets", {"FY2025": -481172, "FY2024": -563604, "FY2023": -551237, "FY2022": -400735, "FY2021": -87059}),
    ("DATA", "Acquisition of treasury bills and gilts", {"FY2024": -5053587, "FY2023": -44402384, "FY2022": -9165232, "FY2021": -19884208}),
    ("DATA", "Acquisition of gilts", {"FY2025": 0}),
    ("DATA", "Proceeds on sale/maturity of treasury bills and gilts", {"FY2025": 4998122, "FY2024": 53536391, "FY2023": 20866125, "FY2022": 9145225, "FY2021": 199669}),
    ("TOTAL", "Net cash generated/(used in) investing activities", {"FY2025": 4472207, "FY2024": 47849547, "FY2023": -24192052, "FY2022": -509405, "FY2021": -19793859}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds of issue of ordinary shares", {"FY2021": 9900000}),
    ("DATA", "Proceeds of TFSME", {"FY2021": 18400000}),
    ("TOTAL", "Net cash from financing activities", {"FY2021": 28300000}),
    ("TOTAL", "Net cash (decrease)/increase in cash and cash equivalents", {"FY2025": -23110550, "FY2024": 6165966, "FY2023": 25231514, "FY2022": -21290200, "FY2021": 23972927}),
    ("DATA", "Cash and cash equivalents at the beginning of year", {"FY2025": 113293493, "FY2024": 109250259, "FY2023": 84018745, "FY2022": 105308945, "FY2021": 81336018}),
    ("TOTAL", "Cash and cash equivalents at the end of year", {"FY2025": 90182943, "FY2024": 115416225, "FY2023": 109250259, "FY2022": 84018745, "FY2021": 105308945}),
]

bw.add_cash_flow_sheet("Redwood Bank Limited — Cash Flow Statement", "Company-only basis, £. FY2021 uses the later FY2022 comparative column; see source note.", rows, CASH_FLOW_SOURCES, first_col_width=68, source_height=300, unit_suffix=" (£)")

asset_quality_rows = [
    ("SECTION", "Loan book quality (mortgage portfolio)", {}),
    ("DATA", "Gross loans and advances to customers (before deferred fees/provisions)", {"FY2025": 496453100, "FY2024": 498343502, "FY2023": 422021987, "FY2022": 410806685, "FY2021": 375065639}),
    ("DATA", "Total impaired loans", {"FY2025": 12772475, "FY2024": 18348860, "FY2023": 23868967, "FY2022": 11956906, "FY2021": 6913006}),
    ("DATA", "Past due but not impaired", {"FY2025": 20604947, "FY2024": 26789634, "FY2023": 21410656, "FY2022": 19429780, "FY2021": 11469228}),
    ("DATA", "Forborne loans", {"FY2025": 5185947, "FY2024": 7471460, "FY2023": 9739221}),
    ("SECTION", "Loan loss provisions", {}),
    ("DATA", "Collective loan provision (closing)", {"FY2025": 659129, "FY2024": 1066643, "FY2023": 1124076, "FY2022": 889925, "FY2021": 1510276}),
    ("DATA", "Individual loan provision (closing)", {"FY2025": 4259401, "FY2024": 3934301, "FY2023": 5522602, "FY2022": 4745925, "FY2021": 1628597}),
    ("TOTAL", "Total loan loss provisions", {"FY2025": 4918530, "FY2024": 5000944, "FY2023": 6646678, "FY2022": 5635850, "FY2021": 3138873}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL ratio (total impaired / gross loans)", {"FY2025": "2.57%", "FY2024": "3.68%", "FY2023": "5.66%", "FY2022": "2.91%", "FY2021": "1.84%"}),
    ("DATA", "Coverage ratio (total loan loss provisions / total impaired loans)", {"FY2025": "38.51%", "FY2024": "27.25%", "FY2023": "27.85%", "FY2022": "47.13%", "FY2021": "45.41%"}),
]

bw.add_asset_quality_sheet(
    title="Redwood Bank Limited — Asset Quality",
    subtitle="Company-only basis, £. FRS 102 basis (no IFRS 9 stage 1/2/3 split); see source note for category definitions. "
              "NPL and coverage ratios are derived, not separately disclosed by the Bank.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£)",
)

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=46, source_height=190)

metric("CET1 Capital", "£", [("Common Equity Tier 1 capital (rounded as reported)", {"FY2025": 48900000, "FY2024": 48400000, "FY2023": 46800000, "FY2022": 41400000, "FY2021": 39400000})], "The annual reports state CET1 capital rounded to £m; these values preserve that stated precision and are not presented as inferred exact amounts.")
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", {"FY2025": "16.6%", "FY2024": "15.1%", "FY2023": "16.0%", "FY2022": "15.4%", "FY2021": "16.9%"})])
metric("Tier 1 Capital", "£", [("Total Tier 1 capital", {"FY2025": 48846803, "FY2024": 48365248, "FY2023": 46764475, "FY2022": 41430663, "FY2021": 39399478})])
metric("Tier 1 Ratio", None, [("Tier 1 ratio", {y: "Not publicly disclosed" for y in YEARS})], "No separate Tier 1 ratio is stated in the public Redwood reports; it is not derived from CET1 or total-capital ratios.")
metric("Total Capital", "£", [("Total regulatory capital / own funds", {"FY2025": 58505932, "FY2024": 58431891, "FY2023": 56888551, "FY2022": 51320588, "FY2021": 49909754})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "19.8%", "FY2024": "18.3%", "FY2023": "19.4%", "FY2022": "19.0%", "FY2021": "21.4%"})])
metric("Total RWAs", None, [("Total risk-weighted assets", {y: "Not publicly disclosed" for y in YEARS})])

bw.add_rwa_breakdown_sheet(
    title="Redwood Bank Limited — RWA Breakdown",
    subtitle="Not publicly disclosed.",
    rows=[("DATA", "RWA breakdown by risk category", {y: "Not publicly disclosed" for y in YEARS})],
    sources_text=P3_SOURCES,
    first_col_width=54,
    source_height=190,
    unit_suffix="",
)

metric("Leverage Ratio", None, [("Leverage ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("LCR", "%", [("Liquidity Coverage Ratio", {"FY2025": "362%", "FY2024": "284%", "FY2023": "481%", "FY2022": "352%", "FY2021": "970%"})])
metric("NSFR", None, [("NSFR", {y: "Not publicly disclosed" for y in YEARS})])
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})])

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 610043348, "FY2024": 635400816, "FY2023": 599055370, "FY2022": 540260485, "FY2021": 527973212}),
        ("Loans and advances to customers", {"FY2025": 490444848, "FY2024": 492244170, "FY2023": 413983306, "FY2022": 403371972, "FY2021": 369798691}),
        ("Customer deposits", {"FY2025": 546762522, "FY2024": 552995571, "FY2023": 499967473, "FY2022": 447173300, "FY2021": 438038613}),
        ("Total equity", {"FY2025": 49983070, "FY2024": 49380257, "FY2023": 47552169, "FY2022": 43325959, "FY2021": 41496104}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 22720767, "FY2024": 26251547, "FY2023": 28828970, "FY2022": 20868106, "FY2021": 15135536}),
        ("Administrative expenses", {"FY2025": -21265984, "FY2024": -21675255, "FY2023": -20509671, "FY2022": -16105258, "FY2021": -12922871}),
        ("Profit for the year", {"FY2025": 602813, "FY2024": 1828088, "FY2023": 4204249, "FY2022": 1797614, "FY2021": 4084475}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Total equity (closing)", {"FY2025": 49983070, "FY2024": 49380257, "FY2023": 47552169, "FY2022": 43325959, "FY2021": 41496104}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -27582757, "FY2024": -41683581, "FY2023": 49423566, "FY2022": -20780795, "FY2021": 15466786}),
        ("Net cash generated/(used in) investing activities", {"FY2025": 4472207, "FY2024": 47849547, "FY2023": -24192052, "FY2022": -509405, "FY2021": -19793859}),
        ("Net cash from financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 28300000}),
        ("Cash and cash equivalents at end of year", {"FY2025": 90182943, "FY2024": 115416225, "FY2023": 109250259, "FY2022": 84018745, "FY2021": 105308945}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.6%", "FY2024": "15.1%", "FY2023": "16.0%", "FY2022": "15.4%", "FY2021": "16.9%"}),
        ("Total Capital Ratio", {"FY2025": "19.8%", "FY2024": "18.3%", "FY2023": "19.4%", "FY2022": "19.0%", "FY2021": "21.4%"}),
        ("LCR", {"FY2025": "362%", "FY2024": "284%", "FY2023": "481%", "FY2022": "352%", "FY2021": "970%"}),
    ],
    note="CET1 capital is rounded to the nearest £m as stated in Redwood's KPI narrative. Undisclosed regulatory metrics remain blank/not publicly disclosed on their detail sheets.",
)

bw.save("/Users/armaan/code/katalysis/banks/REDWOOD BANK FINANCIALS.xlsx")
