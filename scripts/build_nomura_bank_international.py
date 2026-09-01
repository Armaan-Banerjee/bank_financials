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
        "and Note 16 UK Regulatory Capital:\n"
        f"FY2025: Annual Report for year ended 31 March 2025, pp.34 and 79 — {AR25_URL}\n"
        f"FY2024: Annual Report for year ended 31 March 2024, pp.38 and 85 — {AR24_URL}\n"
        f"FY2023: Annual Report for year ended 31 March 2023, pp.37 and 85 — {AR23_URL}\n"
        f"FY2022: Annual Report for year ended 31 March 2022, Statement of Cash Flows and Note 16; the FY2023 "
        f"report's comparative column is also cross-checkable, pp.37 and 85 — {AR22_URL} / {AR23_URL}\n"
        f"FY2021: Annual Report for year ended 31 March 2021, pp.27 and 80 — {AR21_URL}\n"
        "The official reports are scanned PDFs; figures were transcribed from the cited pages and cross-checked "
        "against the following year's comparative column where available. All amounts are $'000."
    )

def p3_sources(extra=""):
    return ar_sources() + ("\n\n" + extra if extra else "")

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

bw = BankWorkbook(bank_name="Nomura Bank International plc", years=YEARS, header_color="6B2D5C")
bw.add_cash_flow_sheet(
    title="Nomura Bank International plc — Statement of Cash Flows",
    subtitle="Standalone Bank basis, $'000",
    rows=ROWS,
    sources_text=ar_sources(),
    first_col_width=78,
    source_height=220,
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
    ["Total Capital Ratio", "Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
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
    cash_flow_totals=[
        ("Net cash flow from operating activities", CF["Net cash flow from operating activities"]),
        ("Net cash flows from financing activities", CF["Net cash flows from financing activities"]),
        ("Cash and cash equivalents at end of year", CF["Cash and cash equivalents at the end of the year"]),
    ],
    cash_flow_unit="$'000",
    ratios=[],
    note="Nomura Bank International plc's entity-level annual reports disclose Tier 1 capital and total capital resources but do not numerically disclose the standard capital, leverage, liquidity, or MREL ratios. See the corresponding metric sheets for explicit non-disclosure notes.",
)

bw.save("/Users/armaan/code/katalysis/banks/NOMURA BANK INTERNATIONAL FINANCIALS.xlsx")
