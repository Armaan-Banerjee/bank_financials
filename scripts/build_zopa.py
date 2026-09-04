import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 Dec)
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.datocms-assets.com/23873/1773841899-zopa_bank_ar25_web.pdf"
AR2024_URL = "https://www.datocms-assets.com/23873/1747055131-zopa-bank-2024-annual-report-signed-web-based.pdf"
AR2023_URL = "https://www.datocms-assets.com/23873/1713257733-zopa-group-2023-annual-report-signed_web-version.pdf"
AR2022_URL = "https://www.datocms-assets.com/23873/1694796852-zopa-bank-annual-report-2022-web.pdf"
AR2021_URL = "https://www.datocms-assets.com/23873/1658745948-zopa-bank-annual-report-2021.pdf"

P3_2025_URL = "https://www.datocms-assets.com/23873/1773842098-12-25-pillar-3-disclosures.pdf"
P3_2024_URL = "https://www.datocms-assets.com/23873/1745405670-2024-zopa-bank-pillar-3-disclosures.pdf"
P3_2023_URL = "https://www.datocms-assets.com/23873/1715596314-2023-pillar-3-disclosures-final.pdf"
P3_2022_URL = "https://www.datocms-assets.com/23873/1696603046-2022-pillar-3-disclosures-final_051023.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Zopa Bank Limited (FRN 800542, Companies House 10627575) is the PRA-authorised entity. It sits "
    "beneath a group holding company (Zopa Group Limited, later re-registered Zopa Group PLC) whose own separate "
    "consolidated accounts and Pillar 3 disclosures also exist - this workbook uses Zopa Bank Limited's own "
    "entity-level figures throughout (its own 'Statement of cash flows' in its own Annual Report and Accounts, "
    "and the dedicated 'Section 4: Disclosures for Zopa Bank Limited' within each year's Pillar 3 report, not the "
    "wider Group-level Section 3), consistent with the ring-fenced/individual-entity basis used elsewhere in this "
    "workbook series. Pillar 3 capital figures differ slightly from the Bank's own Annual Report & Accounts because "
    "they include audited profit and the full amount of Tier 2 capital (stated explicitly in each Pillar 3 report)."
)

STATEMENTS_SOURCES = (
    "Sources - Zopa Bank Limited's own entity-level financial statements, £'000:\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025 - Statement of comprehensive income p.98, Statement of "
    f"financial position p.99, Statement of changes in equity p.100 - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Accounts 2023 - Statement of comprehensive income p.111, Statement of "
    f"financial position p.112, Statement of changes in equity p.113 - {AR2023_URL}\n"
    f"FY2021: Annual Report and Accounts 2021 - Statement of comprehensive income p.66, Statement of financial "
    f"position p.67, Statement of changes in equity p.68 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTE: line-item structure and labels differ by report vintage (e.g. 'Total operating "
    "income' block only appears from FY2024 onward; the equity statement gained separate 'Share premium' and "
    "'Other equity instruments' columns only in FY2025, when the Bank issued AT1 instruments and restructured its "
    "share capital via a capital reduction - both columns are blank/nil for FY2021-FY2024, not a gap). Every "
    "year's own Profit/(loss) before tax ties exactly to the pre-existing Cash Flow Statement sheet's own opening "
    "reconciliation line. Blank cells indicate that year's own statement did not disclose/include that specific "
    "line at all; a printed em-dash in the source was transcribed as 0 (an explicit nil, not a gap)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Zopa Bank Limited's own Statement of cash flows, £'000:\n"
    f"FY2025 & FY2024: Zopa Bank Limited Annual Report and Accounts 2025, p.101 (Statement of cash flows) - {AR2025_URL}\n"
    f"FY2023: Zopa Bank Limited Annual Report and Accounts 2023, p.114 (Statement of cash flows) - {AR2023_URL} "
    f"(cross-checked against its comparative appearance in the 2024 Annual Report, p.111 - {AR2024_URL} - matched exactly)\n"
    f"FY2022: Zopa Bank Limited Annual Report and Accounts 2022, p.95 (Statement of cash flows) - {AR2022_URL} "
    f"(cross-checked against its comparative appearance in the 2023 Annual Report, p.114 - matched exactly)\n"
    f"FY2021: Zopa Bank Limited Annual Report and Accounts 2021, p.69 (Statement of cash flows) - {AR2021_URL} "
    f"(cross-checked against its comparative appearance in the 2022 Annual Report, p.95 - matched exactly)\n"
    "Note: the 2021 Annual Report states 'the statement of cash flows has been represented' vs. its own prior-year "
    "presentation (details in that report's note 1.9) - not a concern for the FY2021-FY2025 figures shown here, "
    "which are all on a mutually consistent, cross-checked basis.\n\n"
    + ENTITY_NOTE
)


def p3_sources(page="14-15"):
    return (
        "Sources - Zopa Bank Limited basis (Section 4: 'Disclosures for Zopa Bank Limited', within each year's "
        "'Zopa Group' Pillar 3 Disclosures document):\n"
        f"FY2025 & FY2024: Pillar 3 Disclosures, year ended 31 December 2025, p.14-15 (Table 5: UK KM1 - Key "
        f"metrics table) - {P3_2025_URL}\n"
        f"FY2023: Pillar 3 Disclosures, year ended 31 December 2023, p.14-15 (Table 5: UK KM1) - {P3_2023_URL} "
        f"(cross-checked against its comparative in the 2024 report, p.14 - {P3_2024_URL} - matched exactly)\n"
        f"FY2022: Pillar 3 Disclosures, year ended 31 December 2022, p.13-14 (Table 5: UK KM1) - {P3_2022_URL} "
        f"(cross-checked against its comparative in the 2023 report, p.14 - matched exactly)\n"
        f"FY2021: as the comparative ('Dec-21') column in the Pillar 3 Disclosures, year ended 31 December 2022, "
        f"p.13-14 (Table 5: UK KM1) - {P3_2022_URL} (Zopa's FY2021 Pillar 3 document is titled/structured as a "
        "Group-only disclosure with no equivalent Bank-specific KM1 section, so the FY2022 report's own comparative "
        "column is used as the citable Bank-level source for FY2021 instead)"
    )


bw = BankWorkbook(bank_name="Zopa Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="1B4332")

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Statement of financial position). Total assets =
# Total liabilities + Total equity for every year. Ties exactly to the
# Statement of Changes in Equity sheet's own closing balances every year.
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents / balances - Central bank(s)", {"FY2025": 2225694, "FY2024": 2761315, "FY2023": 1336105, "FY2022": 1397062, "FY2021": 191148}),
    ("DATA", "Cash and cash equivalents / balances - Other bank(s)", {"FY2025": 82231, "FY2024": 58428, "FY2023": 66063, "FY2022": 21429, "FY2021": 30366}),
    ("DATA", "Debt securities (cash-like)", {"FY2025": 30572, "FY2024": 0, "FY2023": 13988, "FY2022": 13386, "FY2021": 16244}),
    ("DATA", "Amounts due from other Group undertakings", {"FY2025": 39724, "FY2024": 642, "FY2023": 1431, "FY2022": 0, "FY2021": 1808}),
    ("DATA", "Derivative financial instruments", {"FY2025": 141, "FY2024": 5946, "FY2023": 7974, "FY2022": 8346, "FY2021": 11}),
    ("DATA", "Loans and advances to customers", {"FY2025": 3506654, "FY2024": 2865635, "FY2023": 2478213, "FY2022": 1937964, "FY2021": 1173013}),
    ("DATA", "Investment securities (held at FVOCI)", {"FY2025": 1253125, "FY2024": 455157, "FY2023": 80710, "FY2022": 0}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 8578, "FY2024": 6445, "FY2023": 4891, "FY2022": 5007, "FY2021": 2489}),
    ("DATA", "Other assets", {"FY2025": 22470, "FY2024": 22259, "FY2023": 13814, "FY2022": 28358, "FY2021": 1960}),
    ("DATA", "Property, plant and equipment", {"FY2025": 1676, "FY2024": 1150, "FY2023": 1307, "FY2022": 788, "FY2021": 1054}),
    ("DATA", "Right-of-use assets", {"FY2025": 17109, "FY2024": 2137, "FY2023": 4135, "FY2022": 1559, "FY2021": 3526}),
    ("DATA", "Intangible assets", {"FY2025": 43949, "FY2024": 32360, "FY2023": 16055, "FY2022": 9435, "FY2021": 9352}),
    ("DATA", "Deferred tax assets", {"FY2025": 11788, "FY2024": 17573, "FY2023": 24401, "FY2022": 0}),
    ("TOTAL", "Total assets", {"FY2025": 7243711, "FY2024": 6229047, "FY2023": 4049087, "FY2022": 3423334, "FY2021": 1430971}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Derivative financial instruments", {"FY2025": 6020, "FY2024": 1087, "FY2023": 3388, "FY2022": 757, "FY2021": 0}),
    ("DATA", "Amounts due to banks", {"FY2025": 50783, "FY2024": 157227, "FY2023": 159239, "FY2022": 180074, "FY2021": 175193}),
    ("DATA", "Deposits by customers", {"FY2025": 6393598, "FY2024": 5455740, "FY2023": 3357724, "FY2022": 2922845, "FY2021": 968000}),
    ("DATA", "Amounts due to other Group undertakings", {"FY2025": 34361, "FY2024": 4, "FY2023": 615, "FY2022": 106, "FY2021": 17000}),
    ("DATA", "Subordinated liabilities", {"FY2025": 76086, "FY2024": 76086, "FY2023": 78817, "FY2022": 0}),
    ("DATA", "Accruals", {"FY2025": 17498, "FY2024": 16747, "FY2023": 12483, "FY2022": 10449, "FY2021": 8887}),
    ("DATA", "Provisions", {"FY2025": 10521, "FY2024": 3110, "FY2023": 2131, "FY2022": 1370, "FY2021": 1372}),
    ("DATA", "Other liabilities", {"FY2025": 15313, "FY2024": 20016, "FY2023": 27237, "FY2022": 7087, "FY2021": 5113}),
    ("DATA", "Lease liabilities", {"FY2025": 16314, "FY2024": 1739, "FY2023": 3038, "FY2022": 1039, "FY2021": 3151}),
    ("TOTAL", "Total liabilities", {"FY2025": 6620494, "FY2024": 5731756, "FY2023": 3644672, "FY2022": 3123727, "FY2021": 1178716}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called-up share capital", {"FY2025": 68542, "FY2024": 554819, "FY2023": 486319, "FY2022": 421319, "FY2021": 349319}),
    ("DATA", "Share premium", {"FY2025": 6146, "FY2024": 0}),
    ("DATA", "Other equity instruments", {"FY2025": 78298, "FY2024": 0}),
    ("DATA", "Other reserves", {"FY2025": 21826, "FY2024": 9428, "FY2023": 6829, "FY2022": 5902, "FY2021": 6180}),
    ("DATA", "Retained earnings/(accumulated losses)", {"FY2025": 448405, "FY2024": -66956, "FY2023": -88733, "FY2022": -127614, "FY2021": -103244}),
    ("TOTAL", "Total equity", {"FY2025": 623217, "FY2024": 497291, "FY2023": 404415, "FY2022": 299607, "FY2021": 252255}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 7243711, "FY2024": 6229047, "FY2023": 4049087, "FY2022": 3423334, "FY2021": 1430971}),
]

bw.add_balance_sheet_sheet(
    title="Zopa Bank Limited — Balance Sheet",
    subtitle="Zopa Bank Limited (entity-level), £'000. Total assets = Total liabilities + Total equity for every "
              "year. Ties exactly to the Statement of Changes in Equity sheet's own closing Total equity every "
              "year. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Statement of comprehensive income). Every year's
# own Profit/(loss) before tax ties exactly to the Cash Flow Statement
# sheet's own opening reconciliation line.
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 598989, "FY2024": 503794, "FY2023": 349917, "FY2022": 200049, "FY2021": 61146}),
    ("DATA", "Interest expense", {"FY2025": -239341, "FY2024": -224454, "FY2023": -136957, "FY2022": -33937, "FY2021": -5466}),
    ("TOTAL", "Net interest income", {"FY2025": 359648, "FY2024": 279340, "FY2023": 212960, "FY2022": 166112, "FY2021": 55680}),
    ("DATA", "Fee and commission income", {"FY2025": 15232, "FY2024": 14347, "FY2023": 13020, "FY2022": 8133, "FY2021": 2432}),
    ("DATA", "Fee and commission expense", {"FY2025": -16633, "FY2024": -14033, "FY2023": -10684, "FY2022": -9040, "FY2021": -3275}),
    ("TOTAL", "Net fee and commission income/(expense)", {"FY2025": -1401, "FY2024": 314, "FY2023": 2336, "FY2022": -907, "FY2021": -843}),
    ("DATA", "Other operating income", {"FY2025": 266, "FY2024": 2478, "FY2023": 1261, "FY2022": 279, "FY2021": 12807}),
    ("DATA", "Net gains/(losses) on derecognition of financial assets at amortised cost", {"FY2025": 212, "FY2024": 10095, "FY2023": 2984, "FY2022": -21049, "FY2021": -2234}),
    ("DATA", "Net losses on disposal of property, plant and equipment", {"FY2021": 0}),
    ("DATA", "Changes in fair value of financial instruments measured at FVTPL", {"FY2025": 827, "FY2024": 5561, "FY2023": 2889, "FY2022": 6089, "FY2021": -182}),
    ("TOTAL", "Total operating income", {"FY2025": 359552, "FY2024": 297788, "FY2023": 222430, "FY2022": 150524, "FY2021": 65228}),
    ("SECTION", "Operating expenses and impairment", {}),
    ("DATA", "Operating expenses", {"FY2025": -136999, "FY2024": -107992, "FY2023": -83266, "FY2022": -75578, "FY2021": -57640}),
    ("TOTAL", "Net operating income/(loss)", {"FY2025": 222553, "FY2024": 189796, "FY2023": 139164, "FY2022": 74946, "FY2021": 7588}),
    ("DATA", "Change in expected credit losses and other credit impairment charges", {"FY2025": -167501, "FY2024": -156229, "FY2023": -122817, "FY2022": -100609, "FY2021": -41812}),
    ("DATA", "Change in provisions for other liabilities and charges", {"FY2025": -10200, "FY2024": -2017, "FY2023": -530, "FY2022": -325, "FY2021": 0}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": 44852, "FY2024": 31550, "FY2023": 15817, "FY2022": -25988, "FY2021": -34224}),
    ("DATA", "Taxation", {"FY2025": -11472, "FY2024": -9773, "FY2023": 23064, "FY2022": 0, "FY2021": 1}),
    ("TOTAL", "Profit/(loss) after tax", {"FY2025": 33380, "FY2024": 21777, "FY2023": 38881, "FY2022": -25988, "FY2021": -34223}),
    ("SECTION", "Other comprehensive income/(loss)", {}),
    ("DATA", "Changes in fair value of investment securities held at FVOCI", {"FY2025": 187, "FY2024": -46, "FY2023": -49}),
    ("TOTAL", "Total other comprehensive income/(loss)", {"FY2025": 187, "FY2024": -46, "FY2023": -49}),
    ("TOTAL", "Total comprehensive income/(loss)", {"FY2025": 33567, "FY2024": 21731, "FY2023": 38832, "FY2022": -25988, "FY2021": -34223}),
]

bw.add_income_statement_sheet(
    title="Zopa Bank Limited — Profit & Loss",
    subtitle="Zopa Bank Limited (entity-level), £'000. All profits/losses are from continuing operations. "
              "FY2022/FY2021 disclose no other comprehensive income items at all (confirmed via the source "
              "statement's own text, not a gap) - Total comprehensive income equals Profit/(loss) after tax "
              "exactly in those two years. Every year's Profit/(loss) before tax ties exactly to the Cash Flow "
              "Statement sheet's own opening reconciliation line.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity - chronological, ties exactly to
# the Balance Sheet sheet's own Total equity every year and chains
# correctly across all 5 boundaries. Zero undocumented plug rows - every
# movement category (including the easy-to-skip FY2022 "Transfer of
# capital contribution reserve" and FY2025's capital reduction/AT1
# issuance) is captured. Every year's own "Shares issued" figure ties
# exactly to the Cash Flow Statement sheet's own "Shares issued" line.
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Called-up share capital", "Share premium", "Other equity instruments", "Other reserves", "Retained earnings/(accumulated losses)", "Total equity"]

equity_rows = [
    ("TOTAL", "Balance at 1 January 2021", (192319, None, None, 4324, -69021, 127622)),
    ("DATA", "Total comprehensive loss", (None, None, None, None, -34223, -34223)),
    ("DATA", "Shares issued", (157000, None, None, None, None, 157000)),
    ("DATA", "Net share option movements", (None, None, None, 1856, None, 1856)),
    ("TOTAL", "Balance at 31 December 2021 / 1 January 2022", (349319, None, None, 6180, -103244, 252255)),
    ("DATA", "Total comprehensive loss", (None, None, None, None, -25988, -25988)),
    ("DATA", "Shares issued", (72000, None, None, None, None, 72000)),
    ("DATA", "Net share option movements", (None, None, None, 1340, None, 1340)),
    ("DATA", "Transfer of capital contribution reserve", (None, None, None, -1618, 1618, 0)),
    ("TOTAL", "Balance at 31 December 2022 / 1 January 2023", (421319, None, None, 5902, -127614, 299607)),
    ("DATA", "Profit for the year", (None, None, None, None, 38881, 38881)),
    ("DATA", "Other comprehensive loss relating to investment securities held at FVOCI", (None, None, None, -49, None, -49)),
    ("TOTAL", "Total comprehensive income", (None, None, None, -49, 38881, 38832)),
    ("DATA", "Shares issued", (65000, None, None, None, None, 65000)),
    ("DATA", "Net share option movements", (None, None, None, 976, None, 976)),
    ("TOTAL", "Balance at 31 December 2023 / 1 January 2024", (486319, None, None, 6829, -88733, 404415)),
    ("DATA", "Profit for the year", (None, None, None, None, 21777, 21777)),
    ("DATA", "Other comprehensive loss relating to investment securities", (None, None, None, -46, None, -46)),
    ("TOTAL", "Total comprehensive income", (None, None, None, -46, 21777, 21731)),
    ("DATA", "Shares issued", (68500, None, None, None, None, 68500)),
    ("DATA", "Net share option movements", (None, None, None, 2645, None, 2645)),
    ("TOTAL", "Balance at 31 December 2024 / 1 January 2025", (554819, 0, 0, 9428, -66956, 497291)),
    ("DATA", "Profit for the year", (None, None, None, None, 33380, 33380)),
    ("DATA", "Other comprehensive income relating to investment securities", (None, None, None, 187, None, 187)),
    ("TOTAL", "Total comprehensive income", (None, None, None, 187, 33380, 33567)),
    ("DATA", "Shares issued", (854, 6146, None, None, None, 7000)),
    ("DATA", "Capital reduction", (-487131, None, None, None, 487131, 0)),
    ("DATA", "Issue of other equity instruments", (None, None, 78298, None, None, 78298)),
    ("DATA", "Coupons paid on other equity instruments", (None, None, None, None, -5150, -5150)),
    ("DATA", "Net share option movements", (None, None, None, 12211, None, 12211)),
    ("TOTAL", "Balance at 31 December 2025", (68542, 6146, 78298, 21826, 448405, 623217)),
]

bw.add_equity_changes_sheet(
    title="Zopa Bank Limited — Statement of Changes in Equity",
    subtitle="Zopa Bank Limited (entity-level), £'000, chronological (oldest to newest). Zero undocumented plug "
              "rows across all 5 years - ties exactly to the Balance Sheet sheet's own Total equity every year "
              "and chains correctly across all 5 boundaries. 'Share premium' and 'Other equity instruments' "
              "columns only exist from FY2025 (blank/nil in earlier years, not a gap - see source note). Every "
              "year's own 'Shares issued' figure ties exactly to the Cash Flow Statement sheet's own line.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=54,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit/(loss) before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 44852, "FY2024": 31550, "FY2023": 15817, "FY2022": -25988, "FY2021": -34224}),
    ("DATA", "Non-cash items", {"FY2025": 108122, "FY2024": 67370, "FY2023": 66198, "FY2022": 92460, "FY2021": 50828}),
    ("DATA", "Changes in operating assets and liabilities", {"FY2025": 216056, "FY2024": 1640591, "FY2023": -133115, "FY2022": 1082800, "FY2021": -192441}),
    ("DATA", "Current tax expense", {"FY2025": -5687, "FY2024": -3439, "FY2023": -1337}),
    ("DATA", "Tax received", {"FY2021": 0}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 363343, "FY2024": 1736072, "FY2023": -52437, "FY2022": 1149272, "FY2021": -175837}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of investment securities", {"FY2025": -948990, "FY2024": -431925, "FY2023": -80367}),
    ("DATA", "Investment securities matured during the year", {"FY2025": 154254, "FY2024": 67356}),
    ("DATA", "Disposal of property, plant and equipment", {"FY2021": 0}),
    ("DATA", "Purchase of non-current assets from related party", {"FY2021": 0}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -1486, "FY2024": -659, "FY2023": -1167, "FY2022": -610, "FY2021": -519}),
    ("DATA", "Purchase and development of intangible assets", {"FY2025": -21194, "FY2024": -23775, "FY2023": -10779, "FY2022": -3948, "FY2021": -2036}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -817416, "FY2024": -389003, "FY2023": -92313, "FY2022": -4558, "FY2021": -2555}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Shares issued", {"FY2025": 7000, "FY2024": 68500, "FY2023": 65000, "FY2022": 72000, "FY2021": 157000}),
    ("DATA", "Issuance of other equity instruments", {"FY2025": 80000}),
    ("DATA", "Transaction costs on issuance of other equity instruments", {"FY2025": -1702}),
    ("DATA", "Coupon payment on other equity instruments", {"FY2025": -5150}),
    ("DATA", "Proceeds from issuance of subordinated liabilities", {"FY2023": 75000}),
    ("DATA", "Repayment of TFSME borrowings", {"FY2025": -150000}),
    ("DATA", "Proceeds from ILTR borrowings", {"FY2025": 50000}),
    ("DATA", "Change in TFSME and ILTR borrowings", {"FY2023": -19316, "FY2022": -3791}),
    ("DATA", "Change in amounts due to banks", {"FY2021": 175182}),
    ("DATA", "Change in non-trading amounts due to and from other Group undertakings", {"FY2025": -5393, "FY2024": 4, "FY2023": -74, "FY2022": -16507, "FY2021": 15144}),
    ("DATA", "Cash payments/principal elements on lease liabilities", {"FY2025": -1928, "FY2024": -1822, "FY2023": -1745, "FY2022": -2297, "FY2021": -632}),
    ("TOTAL", "Net cash (used in)/generated from financing activities", {"FY2025": -27173, "FY2024": 66682, "FY2023": 118865, "FY2022": 49405, "FY2021": 346694}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -481246, "FY2024": 1413751, "FY2023": -25885, "FY2022": 1194119, "FY2021": 168302}),
    ("DATA", "Cash and cash equivalents at start of year", {"FY2025": 2819743, "FY2024": 1405992, "FY2023": 1431877, "FY2022": 237758, "FY2021": 69456}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 2338497, "FY2024": 2819743, "FY2023": 1405992, "FY2022": 1431877, "FY2021": 237758}),
]

bw.add_cash_flow_sheet(
    title="Zopa Bank Limited — Cash Flow Statement",
    subtitle="Zopa Bank Limited (entity-level), £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality. Credit performance of loans and advances to
# customers by IFRS 9 stage (on-balance sheet only), Note 15/37.1.11-12
# (FY2025-FY2022) and the FY2021 rating-distribution tier table (Note
# 34.1.10, aggregated across tiers - same underlying data, no by-stage
# summary table exists that early). Ties exactly to the Balance Sheet's
# own Loans and advances to customers line for FY2025/FY2024 (after
# adding back the fair value hedge adjustment) and FY2021 (no hedge
# adjustment existed that year); FY2023/FY2022 have a small (~£1.8k-
# £2.3k, <0.1%) genuine gap against the Balance Sheet - documented, not
# forced to tie.
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - Zopa Bank Limited entity-level credit quality disclosures (on-balance sheet loans and advances to "
    "customers only), £'000:\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025, Note 37.1.11 'Credit performance' and Note 37.1.12 'Credit "
    f"quality', p.158 - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Accounts 2023, Note 37.1.11 'Credit performance' and Note 37.1.12 'Credit "
    f"quality', p.167 - {AR2023_URL}\n"
    f"FY2021: Annual Report and Accounts 2021, Note 34.1.10 'Rating distribution' (Zopa risk ratings tier table), "
    f"p.107-108 - aggregated across all 4 Tier bands to a single Stage 1/2/3 figure, since no consolidated by-"
    f"stage summary table exists in this earlier report vintage - {AR2021_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nGENUINE, IMMATERIAL DISCREPANCY (not forced to tie): FY2023's on-balance sheet net figure "
    "(£2,475,917k) is £2,296k below the Balance Sheet's own Loans and advances to customers line (£2,478,213k); "
    "FY2022's (£1,939,768k) is £1,804k above the Balance Sheet's own figure (£1,937,964k). Both gaps are under "
    "0.1% of the balance and are reproduced exactly as each note states them, not plugged. FY2025/FY2024 tie "
    "exactly once the Balance Sheet's own fair value hedge adjustment (+£4,037k / -£714k, see Balance Sheet "
    "sheet note 14) is added back; FY2021 ties exactly with no adjustment needed."
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, gross carrying amount by IFRS 9 stage (on-balance sheet)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 3337595, "FY2024": 2728099, "FY2023": 2336414, "FY2022": 1794856, "FY2021": 1151567}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 252301, "FY2024": 228781, "FY2023": 214897, "FY2022": 216507, "FY2021": 55351}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 181656, "FY2024": 110477, "FY2023": 97665, "FY2022": 65747, "FY2021": 14802}),
    ("DATA", "POCI (purchased or originated credit-impaired)", {"FY2025": 0, "FY2024": 450, "FY2023": 1305, "FY2022": 3743, "FY2021": 4725}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 3771552, "FY2024": 3067807, "FY2023": 2650281, "FY2022": 2080853, "FY2021": 1226445}),
    ("SECTION", "ECL allowance by IFRS 9 stage (on-balance sheet)", {}),
    ("DATA", "Stage 1 allowance", {"FY2025": 75836, "FY2024": 58414, "FY2023": 44313, "FY2022": 38924, "FY2021": 27069}),
    ("DATA", "Stage 2 allowance", {"FY2025": 71644, "FY2024": 67210, "FY2023": 60155, "FY2022": 53373, "FY2021": 15713}),
    ("DATA", "Stage 3 allowance", {"FY2025": 121455, "FY2024": 75822, "FY2023": 69847, "FY2022": 48454, "FY2021": 10650}),
    ("DATA", "POCI allowance", {"FY2024": 12, "FY2023": 49, "FY2022": 334}),
    ("TOTAL", "Total ECL allowance", {"FY2025": 268935, "FY2024": 201458, "FY2023": 174364, "FY2022": 141085, "FY2021": 53432}),
    ("TOTAL", "Net loans and advances to customers (on-balance sheet)", {"FY2025": 3502617, "FY2024": 2866349, "FY2023": 2475917, "FY2022": 1939768, "FY2021": 1173013}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross)", {"FY2025": "4.82%", "FY2024": "3.60%", "FY2023": "3.69%", "FY2022": "3.16%", "FY2021": "1.21%"}),
    ("DATA", "Coverage ratio (Total ECL allowance / Total gross)", {"FY2025": "7.13%", "FY2024": "6.57%", "FY2023": "6.58%", "FY2022": "6.78%", "FY2021": "4.36%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross)", {"FY2025": "66.86%", "FY2024": "68.63%", "FY2023": "71.52%", "FY2022": "73.70%", "FY2021": "71.95%"}),
]

bw.add_asset_quality_sheet(
    title="Zopa Bank Limited — Asset Quality",
    subtitle="Zopa Bank Limited (entity-level), £'000, on-balance sheet loans and advances to customers only. "
              "Ties exactly to Balance Sheet net loans for FY2025/FY2024 (after the fair value hedge adjustment) "
              "and FY2021; FY2023/FY2022 have a small (<0.1%) genuine gap - see source note, not a plug.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Zopa Bank Limited basis, {unit}" if unit else "Zopa Bank Limited basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=120)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 489, "FY2024": 448, "FY2023": 364, "FY2022": 290, "FY2021": 243})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "14.54%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 567, "FY2024": 448, "FY2023": 364, "FY2022": 290, "FY2021": 243})],
    p3_sources(),
    note="Tier 1 = CET1 in every year except FY2025, where the Bank issued £80m of other (AT1) equity instruments "
         "during the year (see Cash Flow Statement sheet), taking Tier 1 above CET1 for the first time.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "16.87%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 642, "FY2024": 523, "FY2023": 439, "FY2022": 290, "FY2021": 243})],
    p3_sources(),
    note="Total capital includes Tier 2 capital (subordinated debt) from FY2023 onward - £75m issued, of which "
         "£63m/£72m/£73m was eligible as at FY2023/FY2024/FY2025 respectively (stated in each year's Pillar 3 "
         "report). No Tier 2 capital existed in FY2021-FY2022, so Total Capital = Tier 1 in those years.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "19.10%", "FY2024": "19.57%", "FY2023": "19.90%", "FY2022": "17.44%", "FY2021": "22.92%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 3364, "FY2024": 2670, "FY2023": 2205, "FY2022": 1663, "FY2021": 1060})],
    p3_sources(),
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Zopa Bank Limited basis, Table 4: UK OV1 - Overview of risk weighted exposure amounts (within "
    "each year's 'Section 4: Disclosures for Zopa Bank Limited'), £m:\n"
    f"FY2025 & FY2024: Pillar 3 Disclosures, year ended 31 December 2025, p.14 - {P3_2025_URL}\n"
    f"FY2023: Pillar 3 Disclosures, year ended 31 December 2023, p.14 - {P3_2023_URL} (cross-checked against its "
    f"comparative in the 2024 report - matched exactly)\n"
    f"FY2022: Pillar 3 Disclosures, year ended 31 December 2022, p.13 - {P3_2022_URL} (cross-checked against its "
    f"comparative in the 2023 report - matched exactly)\n"
    f"FY2021: as the comparative ('2021') column in the Pillar 3 Disclosures, year ended 31 December 2022, p.13 - "
    f"{P3_2022_URL} (same access-gap basis as the FY2021 Total RWAs figure elsewhere in this workbook - no "
    "standalone FY2021 OV1 table exists, so the FY2022 report's own comparative column is used)\n"
    "Category sums round to the Total RWAs figure each year (a <£1m rounding gap in FY2024 only, both figures "
    "reproduced exactly as the source states them).\n\n"
    + ENTITY_NOTE
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk RWA (excluding CCR)", {"FY2025": 2804, "FY2024": 2249, "FY2023": 1921, "FY2022": 1502, "FY2021": 898}),
    ("DATA", "Counterparty Credit Risk RWA", {"FY2025": 0.6, "FY2024": 1, "FY2023": 0.5, "FY2022": 0.3, "FY2021": 0}),
    ("DATA", "Securitisation exposures RWA (non-trading book, after the cap)", {"FY2025": 23, "FY2024": 0}),
    ("DATA", "Operational risk RWA", {"FY2025": 537, "FY2024": 421, "FY2023": 283, "FY2022": 161, "FY2021": 162}),
    ("TOTAL", "Total RWAs", {"FY2025": 3364, "FY2024": 2670, "FY2023": 2205, "FY2022": 1663, "FY2021": 1060}),
]

bw.add_rwa_breakdown_sheet(
    title="Zopa Bank Limited — RWA Breakdown",
    subtitle="Zopa Bank Limited basis, £m. Category sums tie to the Total RWAs sheet's own figures every year "
              "(a <£1m rounding gap in FY2024 only). Securitisation exposures only appear from FY2025.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 4998, "FY2024": 3445, "FY2023": 2699, "FY2022": 2024}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "11.36%", "FY2024": "12.99%", "FY2023": "13.48%", "FY2022": "14.34%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="Not disclosed for FY2021: the Dec-21 comparative column in the 2022 Pillar 3 report shows 'n/a' for both "
         "the leverage exposure measure and ratio, with no explanation given (likely below an applicable "
         "disclosure/reporting threshold at that date).",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 2970, "FY2024": 2347, "FY2023": 1701, "FY2022": 626}),
        ("Total net cash outflows, adjusted value", {"FY2025": 614, "FY2024": 430, "FY2023": 233, "FY2022": 61}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "484%", "FY2024": "546%", "FY2023": "730%", "FY2022": "1,033%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="LCR is a 12-month simple average of month-end observations, which the Pillar 3 report notes 'differs to "
         "the metrics reported in the Bank ARA, which present the position at the year-end date' - the Pillar 3 "
         "(averaged) basis is used here for consistency across years. Not disclosed for FY2021: LCR was a new "
         "disclosure requirement from the FY2022 report onward with no FY2021 comparative provided.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2025": 5761, "FY2024": 4918, "FY2023": 3701}),
        ("Total required stable funding", {"FY2025": 2562, "FY2024": 2162, "FY2023": 1785}),
        ("NSFR ratio (%)", {"FY2025": "225%", "FY2024": "227%", "FY2023": "207%", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
    ],
    p3_sources(),
    note="NSFR disclosure was not applicable/required until 1 January 2023 (PRA PS22/21), so no FY2022 or FY2021 "
         "figures exist.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL disclosure of any kind (numeric or qualitative) was found in Zopa Bank Limited's Pillar 3 "
         "reports for any year reviewed (FY2021-FY2025) - unlike some smaller banks in this workbook series, no "
         "report explicitly states an SNCI/below-threshold exemption reason, it is simply absent from every KM1 "
         "template and surrounding narrative.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 7243711, "FY2024": 6229047, "FY2023": 4049087, "FY2022": 3423334, "FY2021": 1430971}),
        ("Loans and advances to customers", {"FY2025": 3506654, "FY2024": 2865635, "FY2023": 2478213, "FY2022": 1937964, "FY2021": 1173013}),
        ("Deposits by customers", {"FY2025": 6393598, "FY2024": 5455740, "FY2023": 3357724, "FY2022": 2922845, "FY2021": 968000}),
        ("Total equity", {"FY2025": 623217, "FY2024": 497291, "FY2023": 404415, "FY2022": 299607, "FY2021": 252255}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 359552, "FY2024": 297788, "FY2023": 222430, "FY2022": 150524, "FY2021": 65228}),
        ("Profit/(loss) before tax", {"FY2025": 44852, "FY2024": 31550, "FY2023": 15817, "FY2022": -25988, "FY2021": -34224}),
        ("Profit/(loss) after tax", {"FY2025": 33380, "FY2024": 21777, "FY2023": 38881, "FY2022": -25988, "FY2021": -34223}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 497291, "FY2024": 404415, "FY2023": 299607, "FY2022": 252255, "FY2021": 127622}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 33567, "FY2024": 21731, "FY2023": 38832, "FY2022": -25988, "FY2021": -34223}),
        ("Other equity movements, net", {"FY2025": 92359, "FY2024": 71145, "FY2023": 65976, "FY2022": 73340, "FY2021": 158856}),
        ("Closing equity", {"FY2025": 623217, "FY2024": 497291, "FY2023": 404415, "FY2022": 299607, "FY2021": 252255}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 363343, "FY2024": 1736072, "FY2023": -52437, "FY2022": 1149272, "FY2021": -175837}),
        ("Net cash from/(used in) investing activities", {"FY2025": -817416, "FY2024": -389003, "FY2023": -92313, "FY2022": -4558, "FY2021": -2555}),
        ("Net cash from/(used in) financing activities", {"FY2025": -27173, "FY2024": 66682, "FY2023": 118865, "FY2022": 49405, "FY2021": 346694}),
        ("Cash and cash equivalents at end of year", {"FY2025": 2338497, "FY2024": 2819743, "FY2023": 1405992, "FY2022": 1431877, "FY2021": 237758}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "14.54%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%"}),
        ("Tier 1 Ratio", {"FY2025": "16.87%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%"}),
        ("Total Capital Ratio", {"FY2025": "19.10%", "FY2024": "19.57%", "FY2023": "19.90%", "FY2022": "17.44%", "FY2021": "22.92%"}),
        ("Leverage Ratio", {"FY2025": "11.36%", "FY2024": "12.99%", "FY2023": "13.48%", "FY2022": "14.34%"}),
        ("LCR", {"FY2025": "484%", "FY2024": "546%", "FY2023": "730%", "FY2022": "1,033%"}),
        ("NSFR", {"FY2025": "225%", "FY2024": "227%", "FY2023": "207%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. All figures are Zopa Bank Limited's own entity-level basis, "
         "not the wider Zopa Group.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ZOPA FINANCIALS.xlsx")
