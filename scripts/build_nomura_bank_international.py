import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Nomura Bank International plc (company 01981122, FRN 204419), confirmed against
# Banks List 2608.xlsx and Companies House.  The Bank is a standalone UK legal
# entity with no material subsidiaries and reports in USD.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR25_URL = "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Annual-Report-310325.pdf"
AR24_URL = "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Annual-Report-310324.pdf"
AR23_URL = "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Annual-Report-310323.pdf"
AR22_URL = "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Annual-Report-310322.pdf"
AR21_URL = "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Annual-Report-310321.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Nomura Bank International plc (company 01981122, FRN 204419) is the legal entity in the supplied "
    "Banks List 2608.xlsx. Companies House confirms the active public company, incorporated 22 January 1986, with "
    "the same registered name and annual accounts made up to 31 March. The Bank is a wholly owned subsidiary of "
    "Nomura Europe Holdings plc, has no material subsidiaries, and presents its own financial statements in USD."
)

def ar_sources():
    return (
        ENTITY_NOTE + "\n\n"
        "Sources — Nomura Bank International plc Annual Reports and Financial Statements, Statement of Cash Flows "
        "and Note 15 UK Regulatory Capital:\n"
        f"FY2025: Annual Report for year ended 31 March 2025, pp.34 and 79 — {AR25_URL}\n"
        f"FY2024: Annual Report for year ended 31 March 2024, pp.38 and 85 — {AR24_URL}\n"
        f"FY2023: Annual Report for year ended 31 March 2023, pp.37 and 85 — {AR23_URL}\n"
        f"FY2022: Annual Report for year ended 31 March 2022, Statement of Cash Flows and Note 15; the FY2023 "
        f"report's comparative column is also cross-checkable, pp.37 and 85 — {AR22_URL} / {AR23_URL}\n"
        f"FY2021: Annual Report for year ended 31 March 2021, pp.27 and 80 — {AR21_URL}\n"
        "The official reports are scanned PDFs; figures were transcribed from the cited pages and cross-checked "
        "against the following year's comparative column where available. All amounts are $'000."
    )

def p3_sources(extra=""):
    return ar_sources() + ("\n\n" + extra if extra else "")

def statement_sources():
    return (
        ENTITY_NOTE + "\n\n"
        "Sources — Nomura Bank International plc Annual Reports and Financial Statements, "
        "Income Statement / Statement of Comprehensive Income / Statement of Financial Position / "
        "Statement of Changes in Equity:\n"
        f"FY2025: Annual Report for year ended 31 March 2025, pp.30-33 — {AR25_URL}\n"
        f"FY2024: Annual Report for year ended 31 March 2024, pp.34-37, cross-checked against AR2025's "
        f"comparative column — {AR24_URL} / {AR25_URL}\n"
        f"FY2023: Annual Report for year ended 31 March 2023, pp.33-36, cross-checked against AR2024's "
        f"comparative column — {AR23_URL} / {AR24_URL}\n"
        f"FY2022: Annual Report for year ended 31 March 2022, pp.33-36, cross-checked against AR2023's "
        f"comparative column — {AR22_URL} / {AR23_URL}\n"
        f"FY2021: Annual Report for year ended 31 March 2021, pp.24-27, cross-checked against AR2022's "
        f"comparative column — {AR21_URL} / {AR22_URL}\n"
        "All 5 years' Balance Sheet/P&L/Equity figures were independently cross-checked against the "
        "following year's comparative column and tie exactly - zero plug rows were needed. All amounts "
        "are $'000.\n"
        "PRESENTATION NOTE: the FY2025 report relabels the P&L's 'Dealing Loss' line (used FY2021-FY2024) "
        "as 'Gains and losses from financial instruments at fair value through profit or loss' - the same "
        "underlying line, shown here under each year's own contemporaneous label. The Balance Sheet's cash "
        "line is labelled 'Loans and advances to banks' FY2021-FY2023 and 'Cash and cash equivalents' "
        "FY2024-FY2025 - same underlying line, shown as originally labelled each year. 'Customer Accounts' "
        "(FY2021-FY2022) and 'Customer Deposits' (FY2025) are genuinely distinct - the account fell to nil "
        "and was undisclosed as a line in FY2023-FY2024, then a new deposit appeared in FY2025. "
        "'Right-of-use assets' and 'Deferred tax asset/liability' are genuinely absent in some years "
        "(nil or below the entity's own disclosure threshold), not omitted in error. The FY2025 Balance "
        "Sheet (p.33) shows Retained earnings $34,894k / Own credit reserve $(27,133)k while the FY2025 "
        "Statement of Changes in Equity (p.32) shows $34,895k / $(27,134)k for the same closing balances - "
        "a genuine $1k rounding inconsistency between the Bank's own two primary statements (Total Equity "
        "is identical, $262,761k, on both). Each sheet here reproduces its own source statement's figures "
        "exactly rather than silently reconciling the $1k gap."
    )

INTERIM_SOURCES = {
    "Sep-2025": "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Interim-Report-Sep2025.pdf",
    "Sep-2024": "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Interims-September-2024-Accounts-Branded.pdf",
    "Sep-2023": "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Interim-Report-Sep2023.pdf",
    "Sep-2022": "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Interim-Report-Sep2022.pdf",
    "Sep-2021": "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Interim-Report-Sep2021.pdf",
}

# Standalone interim financial-statement metrics, $'000.  These are deliberately
# kept separate from Pillar 3 metrics: the 2022–2025 NBI interim reports do not
# contain a standalone KM1 table.  Values are transcribed from the cited pages.
INTERIM_VALUES = {
    "Sep-2025": {"Profit before tax": 6697, "Profit for the period": 5023, "Total assets": 9206874, "Total equity": 126721},
    "Sep-2024": {"Profit before tax": 6377, "Profit for the period": 4783, "Total assets": 7151199, "Total equity": 271396},
    "Sep-2023": {"Profit before tax": 4228, "Profit for the period": 3187, "Total assets": 6422803, "Total equity": 296505},
    "Sep-2022": {"Profit before tax": 4341, "Profit for the period": 3516, "Total assets": 5427698, "Total equity": 356030},
    "Sep-2021": {"Profit before tax": 9579, "Profit for the period": 7759, "Total assets": 6349266, "Total equity": 171698},
}

INTERIM_PAGE_REFS = {
    "Sep-2025": {"Profit before tax": "p.11", "Profit for the period": "p.11", "Total assets": "p.10", "Total equity": "p.10"},
    "Sep-2024": {"Profit before tax": "p.9", "Profit for the period": "p.9", "Total assets": "p.12", "Total equity": "p.12"},
    "Sep-2023": {"Profit before tax": "p.11", "Profit for the period": "p.11", "Total assets": "p.14", "Total equity": "p.14"},
    "Sep-2022": {"Profit before tax": "p.11", "Profit for the period": "p.11", "Total assets": "p.14", "Total equity": "p.14"},
    "Sep-2021": {"Profit before tax": "p.12", "Profit for the period": "p.12", "Total assets": "p.15", "Total equity": "p.15"},
}

# Source statement-of-cash-flows rows. Values are $'000 and are transcribed from
# each year's own report, using the next report's comparative column as a check.
CF = {
    "Profit before taxation": {"FY2025": 12493, "FY2024": 9544, "FY2023": 8701, "FY2022": 19189, "FY2021": 13873},
    "Depreciation": {"FY2025": 0, "FY2024": 17, "FY2023": 80, "FY2022": 105, "FY2021": 113},
    "Net gain/loss including FX gain/loss on bonds and medium term notes": {"FY2025": 56668, "FY2024": 95274},
    "Interest and FX gain/loss on commercial papers": {"FY2025": 30018, "FY2024": 21359},
    "Provisions": {"FY2025": -38, "FY2024": 34},
    "Net change in derivative assets": {"FY2025": -142070, "FY2024": -140794, "FY2023": 291082, "FY2022": 1032728, "FY2021": 421444},
    "Net change in loans and advances to affiliates": {"FY2025": -1305745, "FY2024": -422254, "FY2023": -607748, "FY2022": -1012313, "FY2021": -857200},
    "Net change in securities purchased under agreements to resell": {"FY2025": 154611, "FY2024": 21196, "FY2023": 364450, "FY2022": 685731, "FY2021": 891295},
    "Net change in loans and advances to others": {"FY2025": 294, "FY2024": 318, "FY2023": -2045, "FY2022": 1163, "FY2021": 64842},
    "Net changes in prepayments and accrued income": {"FY2025": -7833, "FY2024": -35111, "FY2023": -17528, "FY2022": 791, "FY2021": -1791},
    "Net change in other assets": {"FY2025": 2380, "FY2024": -5633, "FY2023": 4747, "FY2022": 2330, "FY2021": 17160},
    "Net change in financial investments": {"FY2025": -2, "FY2024": 0, "FY2023": 9, "FY2022": 0, "FY2021": -2},
    "Net change in customer accounts": {"FY2025": 10000, "FY2024": -761, "FY2023": 0, "FY2022": -166, "FY2021": 10},
    "Net change in derivative liabilities": {"FY2025": 117342, "FY2024": 64879, "FY2023": 152843, "FY2022": -726077, "FY2021": -480143},
    "Net change in accruals and deferred income": {"FY2025": 5453, "FY2024": -24204, "FY2023": 40180, "FY2022": -1286, "FY2021": 3734},
    "Net change in borrowings from affiliates": {"FY2025": 7122, "FY2024": -2879, "FY2023": -153177, "FY2022": -54912, "FY2021": 1757},
    "Net change in borrowings from others": {"FY2023": 151, "FY2022": -8118, "FY2021": -29299},
    "Net change in commercial papers issued": {"FY2023": -19080, "FY2022": -53485, "FY2021": -1255},
    "Net change in securities sold under agreements to repurchase": {"FY2021": -425000},
    "Net change in bonds and medium-term notes": {"FY2023": -405274, "FY2022": -492696, "FY2021": 12330},
    "Net change in other liabilities": {"FY2025": 28, "FY2024": -11, "FY2023": -679, "FY2022": 596, "FY2021": -43},
    "Income tax and group relief paid": {"FY2025": -1684, "FY2024": -6553, "FY2023": 0, "FY2022": 0, "FY2021": -3287},
    "Net cash flow from operating activities": {"FY2025": -1060963, "FY2024": -425579, "FY2023": -343288, "FY2022": -606420, "FY2021": -371462},
    "Proceeds from issuance of bonds and commercial papers": {"FY2025": 2784772, "FY2024": 2939680, "FY2023": 3368550, "FY2022": 3257272, "FY2021": 3408164},
    "Repayments of bonds and commercial papers": {"FY2025": -1722843, "FY2024": -2516103, "FY2023": -3008861, "FY2022": -2642274, "FY2021": -3038749},
    "Dividends paid": {"FY2025": 0, "FY2024": -5000, "FY2023": -10000, "FY2022": -10000, "FY2021": -12000},
    "Payment of principal portion of lease liabilities": {"FY2025": 0, "FY2024": -18, "FY2023": -82, "FY2022": -114, "FY2021": -113},
    "Net cash flows from financing activities": {"FY2025": 1061929, "FY2024": 418559, "FY2023": 349607, "FY2022": 604884, "FY2021": 357302},
    "Net increase/(decrease) in cash and cash equivalents": {"FY2025": 966, "FY2024": -7020, "FY2023": 6319, "FY2022": -1536, "FY2021": -14160},
    "Cash and cash equivalents at the beginning of the year": {"FY2025": 761, "FY2024": 7781, "FY2023": 1462, "FY2022": 2998, "FY2021": 17158},
    "Cash and cash equivalents at the end of the year": {"FY2025": 1727, "FY2024": 761, "FY2023": 7781, "FY2022": 1462, "FY2021": 2998},
    "Interest paid": {"FY2025": -5305, "FY2024": -5334, "FY2023": -7193, "FY2022": -5543, "FY2021": -5978},
    "Interest received": {"FY2025": 323619, "FY2024": 258954, "FY2023": 95480, "FY2022": 27216, "FY2021": 31357},
}

ROWS = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before taxation", CF["Profit before taxation"]),
    ("DATA", "Depreciation", CF["Depreciation"]),
    ("DATA", "Net gain/loss including FX gain/loss on bonds and medium term notes", CF["Net gain/loss including FX gain/loss on bonds and medium term notes"]),
    ("DATA", "Interest and FX gain/loss on commercial papers", CF["Interest and FX gain/loss on commercial papers"]),
    ("DATA", "Provisions", CF["Provisions"]),
]
for label in list(CF)[5:21]:
    ROWS.append(("DATA", label, CF[label]))
ROWS += [
    ("DATA", "Income tax and group relief paid", CF["Income tax and group relief paid"]),
    ("TOTAL", "Net cash flow from operating activities", CF["Net cash flow from operating activities"]),
    ("SECTION", "Cash flows from financing activities", {}),
]
for label in ["Proceeds from issuance of bonds and commercial papers", "Repayments of bonds and commercial papers", "Dividends paid", "Payment of principal portion of lease liabilities"]:
    ROWS.append(("DATA", label, CF[label]))
ROWS += [
    ("TOTAL", "Net cash flows from financing activities", CF["Net cash flows from financing activities"]),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", CF["Net increase/(decrease) in cash and cash equivalents"]),
    ("DATA", "Cash and cash equivalents at the beginning of the year", CF["Cash and cash equivalents at the beginning of the year"]),
    ("TOTAL", "Cash and cash equivalents at the end of the year", CF["Cash and cash equivalents at the end of the year"]),
    ("DATA", "Interest paid", CF["Interest paid"]),
    ("DATA", "Interest received", CF["Interest received"]),
]

# Balance Sheet (Statement of Financial Position), $'000. Transcribed from each
# year's own report and cross-checked against the following year's comparative
# column - all 5 years tie exactly, zero plug rows.
BS = {
    "Cash and cash equivalents": {"FY2025": 1727, "FY2024": 761, "FY2023": 7781, "FY2022": 1462, "FY2021": 2998},
    "Derivative financial instruments (asset)": {"FY2025": 432715, "FY2024": 290645, "FY2023": 149851, "FY2022": 440933, "FY2021": 1473660},
    "Loans and advances to affiliates": {"FY2025": 4956351, "FY2024": 3650595, "FY2023": 3228350, "FY2022": 2620602, "FY2021": 1608289},
    "Securities purchased under agreements to resell": {"FY2025": 2259073, "FY2024": 2413684, "FY2023": 2434880, "FY2022": 2799330, "FY2021": 3485060},
    "Loans and advances to others": {"FY2025": 1850, "FY2024": 2144, "FY2023": 2462, "FY2022": 417, "FY2021": 1580},
    "Prepayments and accrued income": {"FY2025": 64844, "FY2024": 57011, "FY2023": 21899, "FY2022": 4371, "FY2021": 5161},
    "Other assets": {"FY2025": 3652, "FY2024": 6032, "FY2023": 399, "FY2022": 5146, "FY2021": 7476},
    "Right-of-use assets": {"FY2024": 0, "FY2023": 316, "FY2022": 396, "FY2021": 91},
    "Financial investments": {"FY2025": 13, "FY2024": 11, "FY2023": 11, "FY2022": 20, "FY2021": 20},
    "Deferred tax asset": {"FY2025": 2286, "FY2024": 1920, "FY2022": 1256, "FY2021": 24615},
    "Total Assets": {"FY2025": 7722511, "FY2024": 6422803, "FY2023": 5845949, "FY2022": 5873933, "FY2021": 6608950},
    "Customer accounts/deposits": {"FY2025": 10000, "FY2022": 0, "FY2021": 166},
    "Derivative financial instruments (liability)": {"FY2025": 1058579, "FY2024": 941237, "FY2023": 876358, "FY2022": 723515, "FY2021": 1449591},
    "Accruals and deferred income": {"FY2025": 37979, "FY2024": 32526, "FY2023": 56730, "FY2022": 16550, "FY2021": 17834},
    "Borrowings from affiliates": {"FY2025": 125488, "FY2024": 118366, "FY2023": 121244, "FY2022": 274421, "FY2021": 329333},
    "Borrowings from others": {"FY2024": 0, "FY2023": 761, "FY2022": 610, "FY2021": 8728},
    "Commercial papers issued": {"FY2025": 682741, "FY2024": 815131, "FY2023": 789011, "FY2022": 794070, "FY2021": 798480},
    "Bonds and medium-term notes": {"FY2025": 5539325, "FY2024": 4258572, "FY2023": 3578986, "FY2022": 3793645, "FY2021": 3834998},
    "Group relief payable": {"FY2025": 5564, "FY2024": 4231, "FY2023": 7478, "FY2022": 5793},
    "Corporate tax liability": {"FY2024": 0, "FY2023": 787, "FY2022": 837, "FY2021": 1487},
    "Other liabilities": {"FY2025": 74, "FY2024": 72, "FY2023": 364, "FY2022": 1075, "FY2021": 114},
    "Deferred tax liability": {"FY2024": 0, "FY2023": 27062},
    "Total Liabilities": {"FY2025": 7459750, "FY2024": 6170135, "FY2023": 5458781, "FY2022": 5610516, "FY2021": 6440731},
    "Called up share capital": {"FY2025": 255000, "FY2024": 255000, "FY2023": 255000, "FY2022": 255000, "FY2021": 255000},
    "Retained earnings": {"FY2025": 34894, "FY2024": 26080, "FY2023": 30560, "FY2022": 33222, "FY2021": 21879},
    "Own credit reserve": {"FY2025": -27133, "FY2024": -28412, "FY2023": 101608, "FY2022": -24805, "FY2021": -108660},
    "Total Equity": {"FY2025": 262761, "FY2024": 252668, "FY2023": 387168, "FY2022": 263417, "FY2021": 168219},
    "Total Liabilities and Equity": {"FY2025": 7722511, "FY2024": 6422803, "FY2023": 5845949, "FY2022": 5873933, "FY2021": 6608950},
}

BS_ROWS = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", BS["Cash and cash equivalents"]),
    ("DATA", "Derivative financial instruments (asset)", BS["Derivative financial instruments (asset)"]),
    ("DATA", "Loans and advances to affiliates", BS["Loans and advances to affiliates"]),
    ("DATA", "Securities purchased under agreements to resell", BS["Securities purchased under agreements to resell"]),
    ("DATA", "Loans and advances to others", BS["Loans and advances to others"]),
    ("DATA", "Prepayments and accrued income", BS["Prepayments and accrued income"]),
    ("DATA", "Other assets", BS["Other assets"]),
    ("DATA", "Right-of-use assets", BS["Right-of-use assets"]),
    ("DATA", "Financial investments", BS["Financial investments"]),
    ("DATA", "Deferred tax asset", BS["Deferred tax asset"]),
    ("TOTAL", "Total Assets", BS["Total Assets"]),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts/deposits", BS["Customer accounts/deposits"]),
    ("DATA", "Derivative financial instruments (liability)", BS["Derivative financial instruments (liability)"]),
    ("DATA", "Accruals and deferred income", BS["Accruals and deferred income"]),
    ("DATA", "Borrowings from affiliates", BS["Borrowings from affiliates"]),
    ("DATA", "Borrowings from others", BS["Borrowings from others"]),
    ("DATA", "Commercial papers issued", BS["Commercial papers issued"]),
    ("DATA", "Bonds and medium-term notes", BS["Bonds and medium-term notes"]),
    ("DATA", "Group relief payable", BS["Group relief payable"]),
    ("DATA", "Corporate tax liability", BS["Corporate tax liability"]),
    ("DATA", "Other liabilities", BS["Other liabilities"]),
    ("DATA", "Deferred tax liability", BS["Deferred tax liability"]),
    ("TOTAL", "Total Liabilities", BS["Total Liabilities"]),
    ("SECTION", "Shareholders' funds", {}),
    ("DATA", "Called up share capital", BS["Called up share capital"]),
    ("DATA", "Retained earnings", BS["Retained earnings"]),
    ("DATA", "Own credit reserve", BS["Own credit reserve"]),
    ("TOTAL", "Total Equity", BS["Total Equity"]),
    ("TOTAL", "Total Liabilities and Equity", BS["Total Liabilities and Equity"]),
]

# Income Statement + Statement of Comprehensive Income, $'000. FY2023-FY2021's
# OCI is only disclosed within the Statement of Changes in Equity (no separate
# comprehensive-income statement those years) - reused from there.
IS = {
    "Interest income calculated using effective interest method": {"FY2025": 220848, "FY2024": 180718, "FY2023": 64139, "FY2022": 12320, "FY2021": 17163},
    "Other interest and similar income": {"FY2025": 110413, "FY2024": 112645, "FY2023": 49998, "FY2022": 12771, "FY2021": 16026},
    "Interest expense calculated using effective interest method": {"FY2025": -27677, "FY2024": -29736, "FY2023": -7783, "FY2022": -823, "FY2021": -566},
    "Other interest and similar expenses": {"FY2025": -4455, "FY2024": -4323, "FY2022": -4473, "FY2021": -5948},
    "Net interest income": {"FY2025": 299129, "FY2024": 259304, "FY2023": 106354, "FY2022": 19795, "FY2021": 26675},
    "Fee and commission income": {"FY2025": 20044, "FY2024": 11994, "FY2023": 43462, "FY2022": 41653, "FY2021": 52332},
    "Fee and commission expense": {"FY2025": -1514, "FY2024": -1455, "FY2023": -1326, "FY2022": -1342, "FY2021": -2939},
    "Gains and losses from financial instruments at fair value through profit or loss": {"FY2025": -296169, "FY2024": -251873, "FY2023": -104219, "FY2022": -28708, "FY2021": -47561},
    "Total operating income": {"FY2025": 21490, "FY2024": 17970, "FY2023": 44271, "FY2022": 31398, "FY2021": 28507},
    "General and administrative expenses": {"FY2025": -9035, "FY2024": -8391, "FY2023": -35479, "FY2022": -11655, "FY2021": -14680},
    "Credit impairment release/(charge)": {"FY2025": 38, "FY2024": -34, "FY2023": -91, "FY2022": -554, "FY2021": 46},
    "Profit before tax": {"FY2025": 12493, "FY2024": 9545, "FY2023": 8701, "FY2022": 19189, "FY2021": 13873},
    "Tax charge on profit on ordinary activities": {"FY2025": -3123, "FY2024": -2370, "FY2023": -1653, "FY2022": -3647, "FY2021": -2525},
    "Profit for the year": {"FY2025": 9370, "FY2024": 7175, "FY2023": 7048, "FY2022": 15542, "FY2021": 11348},
    "Fair value changes on financial liabilities at FVTPL attributable to own credit risk (net of tax)": {"FY2025": 723, "FY2024": -136675, "FY2023": 126703, "FY2022": 89656, "FY2021": -172938},
    "Total comprehensive income/(loss) for the year": {"FY2025": 10093, "FY2024": -129500, "FY2023": 133751, "FY2022": 105198, "FY2021": -161590},
}

IS_ROWS = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income calculated using effective interest method", IS["Interest income calculated using effective interest method"]),
    ("DATA", "Other interest and similar income", IS["Other interest and similar income"]),
    ("DATA", "Interest expense calculated using effective interest method", IS["Interest expense calculated using effective interest method"]),
    ("DATA", "Other interest and similar expenses", IS["Other interest and similar expenses"]),
    ("TOTAL", "Net interest income", IS["Net interest income"]),
    ("DATA", "Fee and commission income", IS["Fee and commission income"]),
    ("DATA", "Fee and commission expense", IS["Fee and commission expense"]),
    ("DATA", "Gains and losses from financial instruments at fair value through profit or loss", IS["Gains and losses from financial instruments at fair value through profit or loss"]),
    ("TOTAL", "Total operating income", IS["Total operating income"]),
    ("DATA", "General and administrative expenses", IS["General and administrative expenses"]),
    ("DATA", "Credit impairment release/(charge)", IS["Credit impairment release/(charge)"]),
    ("TOTAL", "Profit before tax", IS["Profit before tax"]),
    ("DATA", "Tax charge on profit on ordinary activities", IS["Tax charge on profit on ordinary activities"]),
    ("TOTAL", "Profit for the year", IS["Profit for the year"]),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Fair value changes on financial liabilities at FVTPL attributable to own credit risk (net of tax)", IS["Fair value changes on financial liabilities at FVTPL attributable to own credit risk (net of tax)"]),
    ("TOTAL", "Total comprehensive income/(loss) for the year", IS["Total comprehensive income/(loss) for the year"]),
]

# Statement of Changes in Equity - chronological roll-forward, oldest to newest.
# Confirmed exactly against both the Balance Sheet's own Total Equity each year
# and the next year's own opening balance - zero plug rows.
EQ_HEADERS = ["Called-up Share Capital", "Retained Earnings", "Own Credit Reserve", "Total"]
EQ_ROWS = [
    ("TOTAL", "As at 1 April 2020", (255000, 23137, 63672, 341809)),
    ("DATA", "Dividends paid during the year", (None, -12000, None, -12000)),
    ("DATA", "Transferred from own credit reserve to retained earnings", (None, -606, 606, 0)),
    ("DATA", "Profit for the year", (None, 11348, None, 11348)),
    ("DATA", "Other comprehensive loss (net of tax)", (None, None, -172938, -172938)),
    ("TOTAL", "At 31 March 2021", (255000, 21879, -108660, 168219)),
    ("DATA", "Dividends paid during the year", (None, -10000, None, -10000)),
    ("DATA", "Transferred from own credit reserve to retained earnings", (None, 5801, -5801, 0)),
    ("DATA", "Profit for the year", (None, 15542, None, 15542)),
    ("DATA", "Other comprehensive income (net of tax)", (None, None, 89656, 89656)),
    ("TOTAL", "At 31 March 2022", (255000, 33222, -24805, 263417)),
    ("DATA", "Dividends paid during the year", (None, -10000, None, -10000)),
    ("DATA", "Transferred from own credit reserve to retained earnings", (None, 290, -290, 0)),
    ("DATA", "Profit for the year", (None, 7048, None, 7048)),
    ("DATA", "Other comprehensive income (net of tax)", (None, None, 126703, 126703)),
    ("TOTAL", "At 31 March 2023", (255000, 30560, 101608, 387168)),
    ("DATA", "Dividends paid during the year", (None, -5000, None, -5000)),
    ("DATA", "Transferred from own credit reserve to retained earnings", (None, -6655, 6655, 0)),
    ("DATA", "Profit for the year", (None, 7175, None, 7175)),
    ("DATA", "Other comprehensive loss (net of tax)", (None, None, -136675, -136675)),
    ("TOTAL", "At 31 March 2024", (255000, 26080, -28412, 252668)),
    ("DATA", "Transferred from own credit reserve to retained earnings", (None, -555, 555, 0)),
    ("DATA", "Profit for the year", (None, 9370, None, 9370)),
    ("DATA", "Other comprehensive income (net of tax)", (None, None, 723, 723)),
    ("TOTAL", "At 31 March 2025 (Equity statement's own figures - see source note on the $1k rounding gap vs the Balance Sheet)", (255000, 34895, -27134, 262761)),
]

# Asset Quality: this entity's lending is almost entirely intercompany (Loans
# and advances to affiliates) with a small external book (Loans and advances
# to others); no IFRS 9 stage 1/2/3 split or counterparty-rating table is
# disclosed anywhere in the 5 annual reports - only the accounting policy's
# staging framework (qualitative) and an aggregate P&L impairment line.
AQ_ROWS = [
    ("SECTION", "Credit exposure (Balance Sheet basis)", {}),
    ("DATA", "Loans and advances to affiliates", BS["Loans and advances to affiliates"]),
    ("DATA", "Loans and advances to others", BS["Loans and advances to others"]),
    ("TOTAL", "Total loans and advances", {y: BS["Loans and advances to affiliates"][y] + BS["Loans and advances to others"][y] for y in YEARS}),
    ("SECTION", "Credit impairment (Income Statement basis)", {}),
    ("DATA", "Credit impairment release/(charge) for the year", IS["Credit impairment release/(charge)"]),
    ("SECTION", "IFRS 9 staging", {}),
    ("DATA", "Stage 1 / Stage 2 / Stage 3 split", {y: "Not publicly disclosed" for y in YEARS}),
]

bw = BankWorkbook(bank_name="Nomura Bank International plc", years=YEARS, header_color="6B2D5C")
bw.add_balance_sheet_sheet(
    title="Nomura Bank International plc — Statement of Financial Position",
    subtitle="Standalone Bank basis, $'000",
    rows=BS_ROWS,
    sources_text=statement_sources(),
    first_col_width=62,
    source_height=280,
    unit_suffix=" ($'000)",
)
bw.add_income_statement_sheet(
    title="Nomura Bank International plc — Income Statement and Statement of Comprehensive Income",
    subtitle="Standalone Bank basis, $'000",
    rows=IS_ROWS,
    sources_text=statement_sources(),
    first_col_width=78,
    source_height=280,
    unit_suffix=" ($'000)",
)
bw.add_equity_changes_sheet(
    title="Nomura Bank International plc — Statement of Changes in Equity",
    subtitle="Standalone Bank basis, $'000, chronological (oldest to newest)",
    headers=EQ_HEADERS,
    rows=EQ_ROWS,
    sources_text=statement_sources(),
    first_col_width=98,
    source_height=280,
)
bw.add_cash_flow_sheet(
    title="Nomura Bank International plc — Statement of Cash Flows",
    subtitle="Standalone Bank basis, $'000",
    rows=ROWS,
    sources_text=ar_sources(),
    first_col_width=78,
    source_height=220,
    unit_suffix=" ($'000)",
)
bw.add_asset_quality_sheet(
    title="Nomura Bank International plc — Asset Quality",
    subtitle="Standalone Bank basis, $'000",
    rows=AQ_ROWS,
    sources_text=statement_sources() + (
        "\n\nASSET QUALITY NOTE: the Bank's lending is almost entirely intercompany (Loans and advances to "
        "affiliates); the accounting policy note (p.42) describes a 3-stage IFRS 9 staging framework "
        "qualitatively, but no numeric Stage 1/2/3 split or counterparty-rating table is disclosed anywhere "
        "in the 5 annual reports checked - only the aggregate 'Credit impairment release/(charge)' P&L line."
    ),
    first_col_width=68,
    source_height=200,
    unit_suffix=" ($'000)",
)

def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=52, source_height=180)

# The statutory reports disclose Tier 1 capital and total capital resources, but
# not a separate CET1 figure. No standalone ratios or liquidity metrics were
# numerically disclosed in the five entity-level reports.
bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital", "CET1 Ratio"],
    p3_sources("These metrics were not numerically disclosed in the five entity-level annual reports checked; no values are inferred from group-level Nomura Europe disclosures."),
)
metric("Tier 1 Capital", "$'000", [("Tier 1 capital", {"FY2025": 281414, "FY2024": 281296, "FY2023": 280841, "FY2022": 287698, "FY2021": 276772})])
bw.add_not_disclosed_metric_sheets(
    ["Tier 1 Ratio"],
    p3_sources("These metrics were not numerically disclosed in the five entity-level annual reports checked; no values are inferred from group-level Nomura Europe disclosures."),
)
metric("Total Capital", "$'000", [("Total capital resources", {"FY2025": 281414, "FY2024": 281296, "FY2023": 280841, "FY2022": 287698, "FY2021": 276772})], note="The Bank states that it does not maintain Tier 2 capital; total capital resources therefore equal disclosed Tier 1 capital in each year.")
bw.add_not_disclosed_metric_sheets(
    ["Total Capital Ratio", "Total RWAs"],
    p3_sources("These metrics were not numerically disclosed in the five entity-level annual reports checked; no values are inferred from group-level Nomura Europe disclosures."),
)
bw.add_rwa_breakdown_sheet(
    title="Nomura Bank International plc — RWA Breakdown",
    subtitle="See source note - no RWA figure of any kind is published for this entity.",
    rows=[("DATA", "RWA Breakdown by risk category", {y: "Not publicly disclosed" for y in YEARS})],
    sources_text=p3_sources("Total RWAs itself is not numerically disclosed in the five entity-level annual reports checked (confirmed by reading each report's capital management/regulatory capital note, e.g. Note 15 at AR2025 p.79), so no category-level RWA Breakdown exists to transcribe; no values are inferred from group-level Nomura Europe disclosures."),
    first_col_width=90,
    source_height=220,
)
bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources("These metrics were not numerically disclosed in the five entity-level annual reports checked; no values are inferred from group-level Nomura Europe disclosures."),
)

interim_rows = []
for period in ["Sep-2025", "Sep-2024", "Sep-2023", "Sep-2022", "Sep-2021"]:
    for metric_name, value in INTERIM_VALUES[period].items():
        page = INTERIM_PAGE_REFS[period][metric_name]
        interim_rows.append((
            period,
            "Interim financial statement",
            metric_name,
            value,
            "$'000",
            "Standalone Bank",
            INTERIM_SOURCES[period],
            page,
        ))

# NBI appeared as a separately disclosed material subsidiary in the official
# September 2021 Nomura Europe Pillar 3 report.  From September 2022 onward the
# Group reports that NBI is not a large subsidiary and is not separately disclosed.
sep21_p3_url = "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/nomura-europe-holdings-plc-semi-annual-pillar-3-disclosures-300921.pdf"
sep21_p3 = [
    ("CET1 Capital", 159, "$m", "p.4, CC1"),
    ("Tier 1 Capital", 267, "$m", "p.4, CC1"),
    ("Total Capital", 267, "$m", "p.4, CC1"),
    ("Tier 1 Ratio", 293.99, "%", "p.4, CC1"),
    ("Total Capital Ratio", 293.99, "%", "p.4, CC1"),
]
for metric_name, value, unit, page in sep21_p3:
    interim_rows.append(("Sep-2021", "Pillar 3 — standalone subsidiary table", metric_name, value, unit, "Standalone Bank", sep21_p3_url, page))

for period in ["Sep-2025", "Sep-2024", "Sep-2023", "Sep-2022"]:
    for metric_name, unit in [("CET1 Capital", "$m"), ("Tier 1 Capital", "$m"), ("Total Capital", "$m"), ("Tier 1 Ratio", "%"), ("Total Capital Ratio", "%")]:
        interim_rows.append((
            period,
            "Pillar 3 — not separately disclosed",
            metric_name,
            "Not disclosed",
            unit,
            "Standalone Bank",
            INTERIM_SOURCES[period],
            "p.4, regulatory disclosure section",
        ))

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=interim_rows,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(interim_rows)},
    title="Nomura Bank International plc — Interim Pillar 3",
    subtitle="September interim disclosures; standalone Bank basis",
    note=(
        "The September 2021 Nomura Europe Holdings plc Pillar 3 report separately disclosed NBI as a material subsidiary. "
        "The 2022–2025 NBI interim reports are entity-level financial statements but do not contain a standalone Pillar 3 KM1 table; "
        "these interim financial-statement metrics are included for completeness, while later standalone Pillar 3 gaps are explicitly recorded."
    ),
)

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total Assets", BS["Total Assets"]),
        ("Loans and advances to affiliates", BS["Loans and advances to affiliates"]),
        ("Total Liabilities", BS["Total Liabilities"]),
        ("Total Equity", BS["Total Equity"]),
    ],
    balance_sheet_unit="$'000",
    income_statement_totals=[
        ("Net interest income", IS["Net interest income"]),
        ("Total operating income", IS["Total operating income"]),
        ("General and administrative expenses", IS["General and administrative expenses"]),
        ("Profit for the year", IS["Profit for the year"]),
    ],
    income_statement_unit="$'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 252668, "FY2024": 387168, "FY2023": 263417, "FY2022": 168219, "FY2021": 341809}),
        ("Total comprehensive income/(loss) for the year", IS["Total comprehensive income/(loss) for the year"]),
        ("Other equity movements, net", {"FY2025": 0, "FY2024": -5000, "FY2023": -10000, "FY2022": -10000, "FY2021": -12000}),
        ("Closing equity", BS["Total Equity"]),
    ],
    equity_changes_unit="$'000",
    cash_flow_totals=[
        ("Net cash flow from operating activities", CF["Net cash flow from operating activities"]),
        ("Net cash flows from financing activities", CF["Net cash flows from financing activities"]),
        ("Cash and cash equivalents at end of year", CF["Cash and cash equivalents at the end of the year"]),
    ],
    cash_flow_unit="$'000",
    ratios=[],
    note="Nomura Bank International plc's entity-level annual reports disclose Tier 1 capital and total capital resources but do not numerically disclose the standard capital, leverage, liquidity, or MREL ratios, and no RWA figure of any kind is published. See the corresponding metric sheets for explicit non-disclosure notes.",
)

bw.save("/Users/armaan/code/katalysis/banks/NOMURA BANK INTERNATIONAL FINANCIALS.xlsx")
