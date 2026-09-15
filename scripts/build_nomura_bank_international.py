import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Nomura Bank International plc (company 01981122, FRN 204419), confirmed against
# Banks List 2608.xlsx and Companies House.  The Bank is a standalone UK legal
# entity with no material subsidiaries and reports in USD.

YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR26_URL = "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Annual-Report-310326.pdf"
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
        f"FY2026: Annual Report for year ended 31 March 2026, Statement of Cash Flows printed p.37 and Note 15 "
        f"'Capital Management Policy' UK Regulatory Capital table printed p.84 — {AR26_URL}\n"
        f"FY2025: Annual Report for year ended 31 March 2025, pp.34 and 79 — {AR25_URL}\n"
        f"FY2024: Annual Report for year ended 31 March 2024, pp.38 and 85 — {AR24_URL}\n"
        f"FY2023: Annual Report for year ended 31 March 2023, pp.37 and 85 — {AR23_URL}\n"
        f"FY2022: Annual Report for year ended 31 March 2022, Statement of Cash Flows and Note 15; the FY2023 "
        f"report's comparative column is also cross-checkable, pp.37 and 85 — {AR22_URL} / {AR23_URL}\n"
        f"FY2021: Annual Report for year ended 31 March 2021, pp.27 and 80 — {AR21_URL}\n"
        "The official reports are scanned PDFs; figures were transcribed from the cited pages and cross-checked "
        "against the following year's comparative column where available. All amounts are $'000.\n"
        "FY2026 ADDED 2026-09-15 from the Bank's own Annual Report for the year ended 31 March 2026 (Note 15 "
        "'Capital Management Policy', UK Regulatory Capital table, printed p.84): Tier 1 capital $281,438k and "
        "Total capital resources $281,438k. That table's own 31 March 2025 comparative column states $281,414k "
        "for both lines, matching this workbook's pre-existing FY2025 figures exactly - no restatement. The same "
        "table confirms the disclosure's shape across every year: it reports only 'Tier 1 capital' and 'Total "
        "capital resources' (the Bank states it does not maintain Tier 2 capital), with no CET1 line, no capital "
        "ratio and no RWA figure - which is why those sheets are blank from FY2022 onward once the parent's "
        "Pillar 3 stopped disclosing NBI. Note the report flags Tier 1 capital as not subject to audit."
    )

def p3_sources(extra=""):
    return ar_sources() + ("\n\n" + extra if extra else "")

def statement_sources():
    return (
        ENTITY_NOTE + "\n\n"
        "Sources — Nomura Bank International plc Annual Reports and Financial Statements, "
        "Income Statement / Statement of Comprehensive Income / Statement of Financial Position / "
        "Statement of Changes in Equity:\n"
        f"FY2026: Annual Report for year ended 31 March 2026, printed pp.33-36 (Income Statement p.33, "
        f"Statement of Comprehensive Income p.34, Statement of Changes in Equity p.35, Statement of Financial "
        f"Position p.36) — {AR26_URL}\n"
        f"FY2025: Annual Report for year ended 31 March 2025, pp.30-33 — {AR25_URL}\n"
        f"FY2024: Annual Report for year ended 31 March 2024, pp.34-37, cross-checked against AR2025's "
        f"comparative column — {AR24_URL} / {AR25_URL}\n"
        f"FY2023: Annual Report for year ended 31 March 2023, pp.33-36, cross-checked against AR2024's "
        f"comparative column — {AR23_URL} / {AR24_URL}\n"
        f"FY2022: Annual Report for year ended 31 March 2022, pp.33-36, cross-checked against AR2023's "
        f"comparative column — {AR22_URL} / {AR23_URL}\n"
        f"FY2021: Annual Report for year ended 31 March 2021, pp.24-27, cross-checked against AR2022's "
        f"comparative column — {AR21_URL} / {AR22_URL}\n"
        "All years' Balance Sheet/P&L/Equity figures were independently cross-checked against the "
        "following year's comparative column and tie exactly - zero plug rows were needed. All amounts "
        "are $'000.\n"
        "FY2026 ADDED 2026-09-15: every FY2026 statement was verified to foot internally (Total Assets "
        "$9,284,526k = Total Liabilities $9,112,270k + Total Equity $172,256k; the equity roll-forward from "
        "the 1 April 2025 opening balance ties to the 31 March 2026 closing balance on all three components) "
        "and the AR2026 comparative column reproduces this workbook's existing FY2025 figures exactly, so no "
        "prior year was restated. Two FY2026 presentational points: the Statement of Cash Flows no longer "
        "carries a 'Depreciation' or 'Payment of principal portion of lease liabilities' line (both were nil "
        "in FY2025), and the working-capital line 'Net change in customer accounts' is relabelled 'Net changes "
        "in customer deposits' - the same underlying line, kept on the existing row. FY2026 also shows a large "
        "own-credit movement: Other comprehensive loss of $(91,870)k drives Total Equity down from $262,761k "
        "to $172,256k despite a $9,865k profit, which is a real disclosed movement, not a transcription error.\n"
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
        "exactly rather than silently reconciling the $1k gap.\n"
        "INVESTMENT COMPOSITION NOTE: 'Financial investments' is the Bank's sole investment-securities-type "
        "Balance Sheet line; it is not split by issuer type (no UK government/gilt vs corporate/supranational "
        "breakdown is disclosed - the balance is too small, $11k-$20k, to warrant one) but Note 8 'Financial "
        "Instruments' (Analysis of the Company's financial assets and financial liabilities by IFRS 9 "
        "classification) shows the entire balance sits 100% in the 'Mandatorily at fair value through profit "
        "or loss' column in every one of the 5 years checked, none at amortised cost: FY2025 $13k (AR2025 "
        "Note 8, p.49), FY2024 $11k (AR2025 Note 8 comparative, p.50), FY2023 $11k (AR2023 Note 9, p.54), "
        "FY2022 $20k (AR2023 Note 9 comparative, p.55), FY2021 $20k (AR2021 Note 9, p.48). Since the whole "
        "balance is one measurement basis in every year, and no issuer-type split is disclosed, the row is "
        "relabelled in place rather than split into sub-rows."
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
    "Profit before taxation": {"FY2026": 13177, "FY2025": 12493, "FY2024": 9544, "FY2023": 8701, "FY2022": 19189, "FY2021": 13873},
    "Depreciation": {"FY2025": 0, "FY2024": 17, "FY2023": 80, "FY2022": 105, "FY2021": 113},
    "Net gain/loss including FX gain/loss on bonds and medium term notes": {"FY2026": 177065, "FY2025": 56668, "FY2024": 95274},
    "Interest and FX gain/loss on commercial papers": {"FY2026": 51562, "FY2025": 30018, "FY2024": 21359},
    "Provisions": {"FY2026": 1353, "FY2025": -38, "FY2024": 34},
    "Net change in derivative assets": {"FY2026": -181274, "FY2025": -142070, "FY2024": -140794, "FY2023": 291082, "FY2022": 1032728, "FY2021": 421444},
    "Net change in loans and advances to affiliates": {"FY2026": -1472975, "FY2025": -1305745, "FY2024": -422254, "FY2023": -607748, "FY2022": -1012313, "FY2021": -857200},
    "Net change in securities purchased under agreements to resell": {"FY2026": 83529, "FY2025": 154611, "FY2024": 21196, "FY2023": 364450, "FY2022": 685731, "FY2021": 891295},
    "Net change in loans and advances to others": {"FY2026": 304, "FY2025": 294, "FY2024": 318, "FY2023": -2045, "FY2022": 1163, "FY2021": 64842},
    "Net changes in prepayments and accrued income": {"FY2026": 10657, "FY2025": -7833, "FY2024": -35111, "FY2023": -17528, "FY2022": 791, "FY2021": -1791},
    "Net change in other assets": {"FY2026": -3364, "FY2025": 2380, "FY2024": -5633, "FY2023": 4747, "FY2022": 2330, "FY2021": 17160},
    "Net change in financial investments": {"FY2026": -1, "FY2025": -2, "FY2024": 0, "FY2023": 9, "FY2022": 0, "FY2021": -2},
    "Net change in customer accounts": {"FY2026": 40000, "FY2025": 10000, "FY2024": -761, "FY2023": 0, "FY2022": -166, "FY2021": 10},
    "Net change in derivative liabilities": {"FY2026": -7184, "FY2025": 117342, "FY2024": 64879, "FY2023": 152843, "FY2022": -726077, "FY2021": -480143},
    "Net change in accruals and deferred income": {"FY2026": 17500, "FY2025": 5453, "FY2024": -24204, "FY2023": 40180, "FY2022": -1286, "FY2021": 3734},
    "Net change in borrowings from affiliates": {"FY2026": 97368, "FY2025": 7122, "FY2024": -2879, "FY2023": -153177, "FY2022": -54912, "FY2021": 1757},
    "Net change in borrowings from others": {"FY2023": 151, "FY2022": -8118, "FY2021": -29299},
    "Net change in commercial papers issued": {"FY2023": -19080, "FY2022": -53485, "FY2021": -1255},
    "Net change in securities sold under agreements to repurchase": {"FY2021": -425000},
    "Net change in bonds and medium-term notes": {"FY2023": -405274, "FY2022": -492696, "FY2021": 12330},
    "Net change in other liabilities": {"FY2026": 916, "FY2025": 28, "FY2024": -11, "FY2023": -679, "FY2022": 596, "FY2021": -43},
    "Income tax and group relief paid": {"FY2026": -2546, "FY2025": -1684, "FY2024": -6553, "FY2023": 0, "FY2022": 0, "FY2021": -3287},
    "Net cash flow from operating activities": {"FY2026": -1173913, "FY2025": -1060963, "FY2024": -425579, "FY2023": -343288, "FY2022": -606420, "FY2021": -371462},
    "Proceeds from issuance of bonds and commercial papers": {"FY2026": 4228662, "FY2025": 2784772, "FY2024": 2939680, "FY2023": 3368550, "FY2022": 3257272, "FY2021": 3408164},
    "Repayments of bonds and commercial papers": {"FY2026": -3046844, "FY2025": -1722843, "FY2024": -2516103, "FY2023": -3008861, "FY2022": -2642274, "FY2021": -3038749},
    "Dividends paid": {"FY2026": -8500, "FY2025": 0, "FY2024": -5000, "FY2023": -10000, "FY2022": -10000, "FY2021": -12000},
    "Payment of principal portion of lease liabilities": {"FY2025": 0, "FY2024": -18, "FY2023": -82, "FY2022": -114, "FY2021": -113},
    "Net cash flows from financing activities": {"FY2026": 1173318, "FY2025": 1061929, "FY2024": 418559, "FY2023": 349607, "FY2022": 604884, "FY2021": 357302},
    "Net increase/(decrease) in cash and cash equivalents": {"FY2026": -595, "FY2025": 966, "FY2024": -7020, "FY2023": 6319, "FY2022": -1536, "FY2021": -14160},
    "Cash and cash equivalents at the beginning of the year": {"FY2026": 1727, "FY2025": 761, "FY2024": 7781, "FY2023": 1462, "FY2022": 2998, "FY2021": 17158},
    "Cash and cash equivalents at the end of the year": {"FY2026": 1132, "FY2025": 1727, "FY2024": 761, "FY2023": 7781, "FY2022": 1462, "FY2021": 2998},
    "Interest paid": {"FY2026": -5105, "FY2025": -5305, "FY2024": -5334, "FY2023": -7193, "FY2022": -5543, "FY2021": -5978},
    "Interest received": {"FY2026": 350157, "FY2025": 323619, "FY2024": 258954, "FY2023": 95480, "FY2022": 27216, "FY2021": 31357},
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
    "Cash and cash equivalents": {"FY2026": 1132, "FY2025": 1727, "FY2024": 761, "FY2023": 7781, "FY2022": 1462, "FY2021": 2998},
    "Derivative financial instruments (asset)": {"FY2026": 613989, "FY2025": 432715, "FY2024": 290645, "FY2023": 149851, "FY2022": 440933, "FY2021": 1473660},
    "Loans and advances to affiliates": {"FY2026": 6428499, "FY2025": 4956351, "FY2024": 3650595, "FY2023": 3228350, "FY2022": 2620602, "FY2021": 1608289},
    "Securities purchased under agreements to resell": {"FY2026": 2175544, "FY2025": 2259073, "FY2024": 2413684, "FY2023": 2434880, "FY2022": 2799330, "FY2021": 3485060},
    "Loans and advances to others": {"FY2026": 1546, "FY2025": 1850, "FY2024": 2144, "FY2023": 2462, "FY2022": 417, "FY2021": 1580},
    "Prepayments and accrued income": {"FY2026": 54187, "FY2025": 64844, "FY2024": 57011, "FY2023": 21899, "FY2022": 4371, "FY2021": 5161},
    "Other assets": {"FY2026": 7016, "FY2025": 3652, "FY2024": 6032, "FY2023": 399, "FY2022": 5146, "FY2021": 7476},
    "Right-of-use assets": {"FY2024": 0, "FY2023": 316, "FY2022": 396, "FY2021": 91},
    "Financial investments (mandatorily at fair value through profit or loss)": {"FY2026": 14, "FY2025": 13, "FY2024": 11, "FY2023": 11, "FY2022": 20, "FY2021": 20},
    "Deferred tax asset": {"FY2026": 2599, "FY2025": 2286, "FY2024": 1920, "FY2022": 1256, "FY2021": 24615},
    "Total Assets": {"FY2026": 9284526, "FY2025": 7722511, "FY2024": 6422803, "FY2023": 5845949, "FY2022": 5873933, "FY2021": 6608950},
    "Customer accounts/deposits": {"FY2026": 50000, "FY2025": 10000, "FY2022": 0, "FY2021": 166},
    "Derivative financial instruments (liability)": {"FY2026": 1051395, "FY2025": 1058579, "FY2024": 941237, "FY2023": 876358, "FY2022": 723515, "FY2021": 1449591},
    "Accruals and deferred income": {"FY2026": 55479, "FY2025": 37979, "FY2024": 32526, "FY2023": 56730, "FY2022": 16550, "FY2021": 17834},
    "Borrowings from affiliates": {"FY2026": 222856, "FY2025": 125488, "FY2024": 118366, "FY2023": 121244, "FY2022": 274421, "FY2021": 329333},
    "Borrowings from others": {"FY2024": 0, "FY2023": 761, "FY2022": 610, "FY2021": 8728},
    "Commercial papers issued": {"FY2026": 505372, "FY2025": 682741, "FY2024": 815131, "FY2023": 789011, "FY2022": 794070, "FY2021": 798480},
    "Bonds and medium-term notes": {"FY2026": 7219566, "FY2025": 5539325, "FY2024": 4258572, "FY2023": 3578986, "FY2022": 3793645, "FY2021": 3834998},
    "Group relief payable": {"FY2026": 6088, "FY2025": 5564, "FY2024": 4231, "FY2023": 7478, "FY2022": 5793},
    "Corporate tax liability": {"FY2024": 0, "FY2023": 787, "FY2022": 837, "FY2021": 1487},
    "Other liabilities": {"FY2026": 1514, "FY2025": 74, "FY2024": 72, "FY2023": 364, "FY2022": 1075, "FY2021": 114},
    "Deferred tax liability": {"FY2024": 0, "FY2023": 27062},
    "Total Liabilities": {"FY2026": 9112270, "FY2025": 7459750, "FY2024": 6170135, "FY2023": 5458781, "FY2022": 5610516, "FY2021": 6440731},
    "Called up share capital": {"FY2026": 255000, "FY2025": 255000, "FY2024": 255000, "FY2023": 255000, "FY2022": 255000, "FY2021": 255000},
    "Retained earnings": {"FY2026": 27726, "FY2025": 34894, "FY2024": 26080, "FY2023": 30560, "FY2022": 33222, "FY2021": 21879},
    "Own credit reserve": {"FY2026": -110470, "FY2025": -27133, "FY2024": -28412, "FY2023": 101608, "FY2022": -24805, "FY2021": -108660},
    "Total Equity": {"FY2026": 172256, "FY2025": 262761, "FY2024": 252668, "FY2023": 387168, "FY2022": 263417, "FY2021": 168219},
    "Total Liabilities and Equity": {"FY2026": 9284526, "FY2025": 7722511, "FY2024": 6422803, "FY2023": 5845949, "FY2022": 5873933, "FY2021": 6608950},
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
    ("DATA", "Financial investments (mandatorily at fair value through profit or loss)", BS["Financial investments (mandatorily at fair value through profit or loss)"]),
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
    "Interest income calculated using effective interest method": {"FY2026": 251525, "FY2025": 220848, "FY2024": 180718, "FY2023": 64139, "FY2022": 12320, "FY2021": 17163},
    "Other interest and similar income": {"FY2026": 87187, "FY2025": 110413, "FY2024": 112645, "FY2023": 49998, "FY2022": 12771, "FY2021": 16026},
    "Interest expense calculated using effective interest method": {"FY2026": -16406, "FY2025": -27677, "FY2024": -29736, "FY2023": -7783, "FY2022": -823, "FY2021": -566},
    "Other interest and similar expenses": {"FY2026": -3339, "FY2025": -4455, "FY2024": -4323, "FY2022": -4473, "FY2021": -5948},
    "Net interest income": {"FY2026": 318967, "FY2025": 299129, "FY2024": 259304, "FY2023": 106354, "FY2022": 19795, "FY2021": 26675},
    "Fee and commission income": {"FY2026": 34649, "FY2025": 20044, "FY2024": 11994, "FY2023": 43462, "FY2022": 41653, "FY2021": 52332},
    "Fee and commission expense": {"FY2026": -1598, "FY2025": -1514, "FY2024": -1455, "FY2023": -1326, "FY2022": -1342, "FY2021": -2939},
    "Gains and losses from financial instruments at fair value through profit or loss": {"FY2026": -328872, "FY2025": -296169, "FY2024": -251873, "FY2023": -104219, "FY2022": -28708, "FY2021": -47561},
    "Total operating income": {"FY2026": 23146, "FY2025": 21490, "FY2024": 17970, "FY2023": 44271, "FY2022": 31398, "FY2021": 28507},
    "General and administrative expenses": {"FY2026": -8616, "FY2025": -9035, "FY2024": -8391, "FY2023": -35479, "FY2022": -11655, "FY2021": -14680},
    "Credit impairment release/(charge)": {"FY2026": -1353, "FY2025": 38, "FY2024": -34, "FY2023": -91, "FY2022": -554, "FY2021": 46},
    "Profit before tax": {"FY2026": 13177, "FY2025": 12493, "FY2024": 9545, "FY2023": 8701, "FY2022": 19189, "FY2021": 13873},
    "Tax charge on profit on ordinary activities": {"FY2026": -3312, "FY2025": -3123, "FY2024": -2370, "FY2023": -1653, "FY2022": -3647, "FY2021": -2525},
    "Profit for the year": {"FY2026": 9865, "FY2025": 9370, "FY2024": 7175, "FY2023": 7048, "FY2022": 15542, "FY2021": 11348},
    "Fair value changes on financial liabilities at FVTPL attributable to own credit risk (net of tax)": {"FY2026": -91870, "FY2025": 723, "FY2024": -136675, "FY2023": 126703, "FY2022": 89656, "FY2021": -172938},
    "Total comprehensive income/(loss) for the year": {"FY2026": -82005, "FY2025": 10093, "FY2024": -129500, "FY2023": 133751, "FY2022": 105198, "FY2021": -161590},
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
    # Retagged TOTAL (was DATA) 2026-09-07: this is the Bank's sole,
    # complete operating-expense line (no personnel/other-opex split
    # disclosed), so it IS the genuine opex total, not a sub-component of a
    # larger opex section - needed so cost-to-income analysis can find it.
    ("TOTAL", "General and administrative expenses", IS["General and administrative expenses"]),
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
    ("DATA", "Dividends paid during the year", (None, -8500, None, -8500)),
    ("DATA", "Transferred from own credit reserve to retained earnings", (None, -8534, 8534, 0)),
    ("DATA", "Profit for the year", (None, 9865, None, 9865)),
    ("DATA", "Other comprehensive loss (net of tax)", (None, None, -91870, -91870)),
    ("TOTAL", "At 31 March 2026", (255000, 27726, -110470, 172256)),
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

def metric(name, unit, rows_data, note=None, extra_source=""):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(extra_source), note=note,
                        first_col_width=52, source_height=180)

# The statutory reports disclose Tier 1 capital and total capital resources, but
# not a separate CET1 figure. No standalone ratios or liquidity metrics were
# numerically disclosed in the five entity-level reports.
NEH_P3_URL = "https://www.nomuranow.com/portal/site/login/en-gb/resources/upload/nomura-europe-holdings-plc-annual-pillar-3-disclosures-310321.pdf"
NEH_P3_22_URL = "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/nomura-europe-holdings-plc-annual-pillar-3-disclosures-310322.pdf"
NEH_P3_23_URL = "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/nomura-europe-holdings-plc-annual-pillar-3-disclosures-310323.pdf"
NEH_P3_24_URL = "https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/nomura-europe-holdings-plc-annual-pillar-3-disclosures-310324.pdf"

NEH_SOURCE = (
    "NBI entity-level own funds and ratios - Nomura Europe Holdings Plc, Annual Pillar 3 Disclosures "
    "31 March 2021, table CC1 'Composition of Regulatory Capital', NBI column - printed p.7 (PDF p.11 of 76) - "
    + NEH_P3_URL +
    "\nPAGE CITATION CORRECTED 2026-09-15: an earlier revision of this file cited that table as 'p.16'. The document's "
    "own contents page lists 'CC1: Composition of Regulatory Capital .... 7', and the table itself sits on PDF page 11 "
    "under the 'Own Funds Disclosures' section header, so printed p.7 / PDF p.11 is the correct reference. The figures "
    "themselves were unaffected and are unchanged."
)
NEH_NOTE = (
    '\n\nRE-VERIFIED 2026-09-12 (independent disclosure audit) - PARTIAL RECOVERY AND A STRUCTURAL EXPLANATION. Nomura Bank International plc does not publish its own Pillar 3 document, but it IS named as a material subsidiary in its parent\'s: "Nomura Europe Holdings Plc - Annual Pillar 3 Disclosures, 31 March 2021" (https://www.nomuranow.com/portal/site/login/en-gb/resources/upload/nomura-europe-holdings-plc-annual-pillar-3-disclosures-310321.pdf) carries a dedicated NBI column in its CC1 "Composition of Regulatory Capital" table (p.16), giving NBI\'s OWN entity-level own funds and ratios - these are used on the relevant sheets and are NOT group figures.\nWHY MOST METRICS REMAIN BLANK - the same document states it explicitly (Scope of Application, p.1): "NBI is a United Kingdom (\'UK\') regulated bank but its Risk Weighted Assets (\'RWA\') are immaterial to the Group. Therefore NBI disclosures have been made for article 437 (Own Funds) with no other disclosures relevant to significant subsidiary requirements." So NBI\'s RWA amount, RWA category breakdown, leverage ratio, LCR, NSFR and MREL are genuinely not disclosed anywhere, by design, rather than being an access gap.\nFY2025-FY2022 - RESOLVED 2026-09-15, AND IT IS STRUCTURAL, NOT AN ACCESS GAP. A previous revision of this note recorded FY2022-FY2025 as an unresolved ACCESS LIMITATION, reasoning that the nomuranow.com portal returns HTTP 403 unauthenticated and that later editions \"very likely exist and would extend FY2022-FY2025\". Those later editions have since been obtained directly (browser session against the Nomura portal) and read in full. The reasoning was wrong: the editions do exist, but they deliberately STOP disclosing NBI. \"Nomura Europe Holdings plc - Annual Pillar 3 Disclosures, 31st March 2022\" states in its own Scope of Application (printed p.5, PDF p.6): \"NBI and NFPE were previously considered \'significant subsidiaries\' and previously disclosed. However, along with the other regulated subsidiaries, they are not considered to be large subsidiaries as at 31st March 2022 and are therefore not disclosed in this document.\" Consistent with that, the 31 March 2022 edition\'s own CC1 template is titled \"Composition of regulatory own funds for the Group and NIP\" (printed p.12, PDF p.13) and carries only Group and NIP columns - the NBI column present in the 31 March 2021 edition is gone. NBI therefore has no disclosed CET1 amount, CET1 ratio, Tier 1 ratio or Total Capital ratio for FY2022 onward from any source: the parent ceased disclosing it, and NBI\'s own Annual Report capital note (Note 15 \'UK Regulatory Capital\') discloses only Tier 1 capital and Total capital resources - no CET1 figure, no ratio and no RWA in any year. These blanks are a genuine end of disclosure, not a document that remains to be found.'
    "\nINDEPENDENTLY RE-VERIFIED 2026-09-15 (second reader, documents re-downloaded and re-read rather than taken on trust), "
    "and EXTENDED THROUGH FY2024, which the earlier pass had left open:\n"
    "- 31 March 2022 edition (91 pages, " + NEH_P3_22_URL + "), Scope of Application, PDF p.6: \"NBI and NFPE were previously "
    "considered 'significant subsidiaries' and previously disclosed. However, along with the other regulated subsidiaries, they "
    "are not considered to be large subsidiaries as at 31st March 2022 and are therefore not disclosed in this document.\" Its "
    "own capital template is headed \"CC1 - Composition of regulatory own funds for the Group and NIP\" (PDF p.13) and has Group "
    "and NIP columns only.\n"
    "- 31 March 2024 edition (120 pages, " + NEH_P3_24_URL + "), same section, PDF p.6: \"Other regulated subsidiaries included "
    "in the Group are Nomura Bank International Plc ('NBI'), Nomura Financial Products Europe GmbH ('NFPE'), Nomura Bank "
    "Luxembourg S.A. ('NBL'), Banque Nomura France S.A. ('BNF'), Nomura Alternative Investment Management France S.A.S ('NAIM') "
    "and Nomura Bank Switzerland Ltd ('NBS'). They are not considered to be large subsidiaries as at 31st March 2024 and are "
    "therefore not disclosed in this document.\" Its CC1 is likewise headed \"...for the Group and NIP\" (PDF p.16). The "
    "31 March 2023 edition (" + NEH_P3_23_URL + ") carries the equivalent wording for 31st March 2023.\n"
    "- The FY2025 and FY2026 editions are not published at the expected addresses at all: "
    "nomura-europe-holdings-plc-annual-pillar-3-disclosures-310325.pdf and -310326.pdf both return HTTP 404 under BOTH the "
    "/portal/site/public/ and /portal/site/login/ path prefixes (all four combinations tested 2026-09-15). So for FY2025 and "
    "FY2026 there is not even a group document to exclude NBI from.\n"
    "NET EFFECT: the NEHS significant-subsidiary route yields NBI figures for FY2021 and for FY2021 only. FY2022 through FY2024 "
    "are a SOURCED structural negative (the group report exists, names NBI, and says in terms that it is not disclosing it); "
    "FY2025 and FY2026 are an enumerated negative (no group report at those addresses). Neither is an access problem, and "
    "neither should be re-chased."
)

# WHY CET1 IS LEFT BLANK FOR FY2022-FY2026 EVEN THOUGH TIER 1 IS KNOWN.
# This is the single most tempting bad inference available on this bank, so the
# refusal is written down rather than left implicit.
CET1_DERIVATION_REFUSAL = (
    "DERIVATION DELIBERATELY REFUSED for FY2022-FY2026 - read this before 'filling' these cells. It is tempting to set CET1 "
    "capital equal to the disclosed Tier 1 capital, because the Bank's own capital note states that 'The Bank does not currently "
    "maintain Tier 2 capital'. That statement does exactly one thing: it establishes that Total capital resources equals Tier 1 "
    "capital, which is why the Total Capital sheet legitimately carries the same figures. It does NOT establish that CET1 equals "
    "Tier 1. Tier 1 capital is CET1 plus Additional Tier 1, and the absence of Tier 2 says nothing at all about the presence or "
    "absence of AT1. No Nomura Bank International document states that the Bank holds no AT1 instrument, and no document discloses "
    "a CET1 figure for these years. Writing CET1 = Tier 1 would therefore be an assumption dressed as a transcription, and it "
    "would be wrong in exactly the way this project's first rule forbids.\n"
    "Note that the one year where both figures ARE independently disclosed shows they genuinely differ for this entity: at "
    "31 March 2021 the parent's CC1 table gives NBI CET1 of $267m while the Bank's own capital note gives Tier 1 capital of "
    "$276,772k - a $9.8m gap arising from prudential filters and deductions applied in the regulatory return but not in the "
    "accounts-based note. That is direct evidence that the two measures are not interchangeable for this bank, quite apart from "
    "the AT1 point.\n"
    "The blank cell is the correct and informative answer here. It says the figure was never published; a filled cell would say "
    "something that no document says."
)

metric("CET1 Capital", "$'000", [("Common Equity Tier 1 capital", {"FY2021": 267000})],
       note="FY2021 recovered 2026-09-12 from the parent's Pillar 3 CC1 table, NBI's own column (reported "
            "in $m, shown here as $'000: $267m). NOTE A GENUINE BASIS DIFFERENCE, not a transcription "
            "error: the Annual Report's own Note 15 states Tier 1 capital of $276,772k for the same date, "
            "$9.8m higher, because the regulatory CC1 figure applies prudential filters and deductions "
            "(prudent valuation, deferred tax, own-credit adjustment) that the accounts-based note does "
            "not. Both are reproduced as their own source states them rather than reconciled. FY2025-"
            "FY2022 are blank because the parent's Pillar 3 stopped disclosing NBI from its 31 March 2022 "
            "edition onward, and NBI's own Annual Report never discloses a CET1 figure - a genuine end of "
            "disclosure, confirmed 2026-09-15 against the later editions themselves. See the source note.\n\n"
            + CET1_DERIVATION_REFUSAL,
       extra_source=NEH_SOURCE)
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", {"FY2021": "279.68%"})],
       note="FY2021 as directly disclosed in the parent's Pillar 3 CC1 table, NBI column. The very high "
            "ratio is consistent with that document's own statement that NBI's risk-weighted assets are "
            "immaterial to the Group. FY2025-FY2022 blank because the parent ceased disclosing NBI from "
            "its 31 March 2022 Pillar 3 edition onward (confirmed 2026-09-15 by reading those editions) "
            "and no ratio appears in NBI's own accounts - see source note.",
       extra_source=NEH_SOURCE)
TIER1_AR_NOTE = (
    "All six years come from the Bank's OWN annual reports - entity basis throughout, no parent figure substituted - in the "
    "'UK Regulatory Capital' table inside the Capital Management Policy note (note 16 in the FY2022 and FY2023 reports, "
    "renumbered note 15 from FY2024). Every figure was re-read from the source PDFs on 2026-09-15 and the full chain of "
    "prior-year comparatives reconciles with no restatement anywhere: AR2022 (PDF p.89) gives 287,698 with a 31 March 2021 "
    "comparative of 276,772; AR2023 (PDF p.86) gives 280,841 with 287,698; AR2024 (PDF p.86) gives 281,296 with 280,841; "
    "AR2025 (PDF p.80) gives 281,414 with 281,296; AR2026 (PDF p.85) gives 281,438 with 281,414. Each edition's comparative "
    "reproduces the previous edition's own published figure exactly, so the validation gate passes across all five links.\n"
    "AUDIT CAVEAT, as the Bank itself flags it: the FY2026 report footnotes this table 'Tier 1 capital is not subject to audit'. "
    "The figure is transcribed as published, with that caveat attached rather than silently dropped.\n"
    "BASIS CAVEAT: this is an accounts-based capital note, not a Pillar 3 CC1 return. Where both exist for the same date - "
    "31 March 2021 - they differ: the parent's CC1 gives NBI CET1 of $267m against this note's Tier 1 of $276,772k, because the "
    "regulatory return applies prudential filters (prudent valuation, deferred tax, own-credit adjustment) that the accounts-based "
    "note does not. The two are shown on their own sheets on their own bases and are not reconciled to each other."
)

metric("Tier 1 Capital", "$'000", [("Tier 1 capital", {"FY2026": 281438, "FY2025": 281414, "FY2024": 281296, "FY2023": 280841, "FY2022": 287698, "FY2021": 276772})], note=TIER1_AR_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 capital ratio", {"FY2021": "279.68%"})],
       note="FY2021 equals the CET1 ratio: the parent's Pillar 3 CC1 table states in its own footnote 6 "
            "that \"Tier 1 capital ratio is equal to the Common Equity Tier 1 ratio\", and NBI holds no "
            "Additional Tier 1 instrument. FY2025-FY2022 blank because the parent ceased disclosing NBI "
            "from its 31 March 2022 Pillar 3 edition onward (confirmed 2026-09-15 by reading those "
            "editions) and no ratio appears in NBI's own accounts - see source note.",
       extra_source=NEH_SOURCE)
metric("Total Capital", "$'000", [("Total capital resources", {"FY2026": 281438, "FY2025": 281414, "FY2024": 281296, "FY2023": 280841, "FY2022": 287698, "FY2021": 276772})], note=(
    "These are NOT derived from the Tier 1 sheet. Each year's 'UK Regulatory Capital' table prints 'Tier 1 capital' and "
    "'Total capital resources' as two separate, separately stated lines, and both are transcribed from the table as published; "
    "they happen to be equal because, as the same note says in its own words, 'The Bank does not currently maintain Tier 2 "
    "capital'. That statement supports this equality and nothing further - in particular it does NOT license setting CET1 equal "
    "to Tier 1, since it says nothing about Additional Tier 1; see the CET1 Capital sheet's note.\n\n" + TIER1_AR_NOTE))
metric("Total Capital Ratio", "%",
       [("Total capital as a percentage of total risk exposure amounts", {"FY2021": "279.68%"})],
       note="FY2021 as directly disclosed in the parent's Pillar 3 CC1 table, NBI column; equal to the "
            "CET1 ratio because NBI holds no Tier 2 capital (the CC1 table shows a dash on NBI's Tier 2 "
            "row, consistent with the Annual Report's own statement). FY2025-FY2022 blank because the "
            "parent ceased disclosing NBI from its 31 March 2022 Pillar 3 edition onward (confirmed "
            "2026-09-15 by reading those editions) and no ratio appears in NBI's own accounts - see "
            "source note.",
       extra_source=NEH_SOURCE)
bw.add_not_disclosed_metric_sheets(
    ["Total RWAs"],
    p3_sources(
        "TOTAL RWAs: genuinely never disclosed for this entity, in either the Annual Reports or the "
        "parent's Pillar 3 - the latter states NBI's RWAs are immaterial to the Group and so limits NBI's "
        "disclosure to Article 437 (Own Funds) only. An FY2021 figure of roughly $95m is arithmetically "
        "implied by the disclosed CET1 of $267m at the disclosed 279.68% ratio, but that is a "
        "back-solved inference from two rounded inputs, not a disclosed number, so it is deliberately "
        "NOT entered here." + NEH_NOTE),
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
    p3_sources(
        "These four metrics are not numerically disclosed in the five entity-level annual reports, and "
        "are structurally outside the only Pillar 3 disclosure made for this entity: its parent's Pillar "
        "3 limits NBI to Article 437 (Own Funds) disclosures because NBI's RWAs are immaterial to the "
        "Group, which excludes leverage, liquidity and MREL templates. No values are inferred from "
        "group-level Nomura Europe disclosures." + NEH_NOTE),
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
        ("Opening equity", {"FY2026": 262761, "FY2025": 252668, "FY2024": 387168, "FY2023": 263417, "FY2022": 168219, "FY2021": 341809}),
        ("Total comprehensive income/(loss) for the year", IS["Total comprehensive income/(loss) for the year"]),
        ("Other equity movements, net", {"FY2026": -8500, "FY2025": 0, "FY2024": -5000, "FY2023": -10000, "FY2022": -10000, "FY2021": -12000}),
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
