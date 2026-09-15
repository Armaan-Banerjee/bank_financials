import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Cash flow statement only exists for FY2021-FY2023 - see CASH_FLOW_EXEMPTION_NOTE
# below. Pillar 3 / capital disclosures (from the Annual Report's own "Capital
# management and liquidity" section - AIB UK does not publish a separate KM1-style
# Pillar 3 document) cover all 5 years.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/NI018800/filing-history"
AR2025_URL = "https://www.aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/annualreport/2025/aib-group-uk-plc-annual-financial-report-2025.pdf"
AR2024_URL = "https://www.aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/annualreport/2024/aib-group-uk-plc-annual-financial-report-2024.pdf"
AR2023_URL = "https://aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/annualreport/2023/aib-group-uk-plc-annual-financial-report-2023.pdf"
AR2022_URL = "https://aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/annualreport/2022/AIB-Group-UK-p.l.c-Annual-Financial-Report-2022.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: 'AIB Group (UK) p.l.c.' (FRN 122088, Companies House NI018800, registered in Northern Ireland) is "
    "a UK subsidiary of Allied Irish Banks, p.l.c. / AIB Group plc (Irish parent, Dublin-registered, no. 594283) - "
    "it is a DIFFERENT legal entity from 'AIB Group plc' itself, which publishes its own much larger, Ireland-wide "
    "consolidated Pillar 3 Disclosures on aib.ie. Early research surfaced AIB Group plc's Irish-group Pillar 3 PDFs "
    "first (they dominate web search results) - these were discarded as the wrong entity. All figures in this "
    "workbook are AIB Group (UK) p.l.c.'s own Annual Financial Report, not the wider AIB Group plc's disclosures. "
    "Confirmed via Companies House filing history and the FRN in Banks List 2608.xlsx."
)

CASH_FLOW_EXEMPTION_NOTE = (
    "CASH FLOW EXEMPTION NOTE: only FY2021-FY2023 have a Statement of Cash Flows. The FY2024 and FY2025 Annual "
    "Financial Reports both state, under '1.2 Basis of preparation': 'the Company has applied the exemptions "
    "available under FRS 101 in respect of the following disclosures: a statement of cash flows and related notes "
    "(IAS 1 Presentation of Financial Statements and IAS 7 Statement of Cash Flows)...' - confirmed directly in "
    "both PDFs' own text (not OCR'd; both are text-native filings). The FY2021-FY2023 reports instead presented "
    "consolidated 'AIB UK Group' financial statements (no FRS 101 exemptions), which is why a full cash flow "
    "statement exists for those three years but not the two most recent ones - the same 'exemption kicks in "
    "partway through the window' pattern seen with Tandem Bank Limited elsewhere in this project, though here it's "
    "a switch from group to solo (FRS 101) reporting that triggers it, not a straightforward late adoption."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are the 'AIB UK Group' (consolidated) column of AIB Group (UK) p.l.c.'s own Statement "
    "of Cash Flows, £m (not the 'AIB UK' solo column shown alongside it, and not AIB Group plc's Irish-group "
    "figures):\n"
    f"FY2023: FY2023 Annual Financial Report, p.73 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: FY2022 Annual Financial Report, p.71 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: sourced from the FY2022 Annual Financial Report's own FY2021 comparative column, p.71 (a standalone "
    f"FY2021 Annual Financial Report PDF could not be fetched - aibgb.co.uk returned HTTP 403 on the only URL "
    f"found for it, and no working aib.ie-hosted equivalent was located) - {AR2022_URL}\n"
    "FY2022 figures were independently cross-checked against their appearance as the FY2023 report's own FY2022 "
    "comparative column and matched exactly.\n\n"
    + ENTITY_NOTE + "\n\n" + CASH_FLOW_EXEMPTION_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - all figures from AIB Group (UK) p.l.c.'s own Annual Financial Report, 'Capital management and "
        "liquidity' section (AIB UK does not publish a separate standalone Pillar 3/KM1 disclosure document - "
        "capital and liquidity metrics are disclosed within the Annual Financial Report itself):\n"
        f"FY2025: FY2025 Annual Financial Report, p.5 - {AR2025_URL}\n"
        f"FY2024: FY2024 Annual Financial Report, p.11 - {AR2024_URL}\n"
        f"FY2023: FY2023 Annual Financial Report, p.17-18 - {AR2023_URL}\n"
        f"FY2022: FY2022 Annual Financial Report, p.19-20 - {AR2022_URL}\n"
        f"FY2021: sourced from the FY2022 Annual Financial Report's own FY2021 comparative figures, p.19-20 (see "
        f"cash flow source note on why a standalone FY2021 report wasn't used) - {AR2022_URL}\n"
        "Figures shown are on a TRANSITIONAL basis (AIB UK's own headline reported ratio each year) - fully loaded "
        "(post-IFRS 9 transitional relief) figures are also disclosed but not used here, consistent with how this "
        "project treats IFRS 9 transitional relief for other banks.\n"
        + (extra + "\n" if extra else "")
        + "\n" + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="AIB Group (UK) p.l.c.", years=YEARS, year_label=YEAR_LABEL, header_color="8C1D40")

# ---------------------------------------------------------------
# Entity-basis note for the statement sheets below: FY2021-FY2023 figures
# are the "AIB UK Group" consolidated column of each year's own Annual
# Financial Report; FY2024-FY2025 figures are AIB Group (UK) p.l.c.'s own
# (solo/Company) column, since group-level consolidated statements ceased
# once the FRS 101 exemptions took effect (see CASH_FLOW_EXEMPTION_NOTE).
# This mirrors the CASH_FLOW_SOURCES convention already used above.
# ---------------------------------------------------------------
STATEMENT_ENTITY_NOTE = (
    "STATEMENT BASIS NOTE: FY2021-FY2023 figures are the 'AIB UK Group' (consolidated) column of that year's own "
    "Annual Financial Report; FY2024-FY2025 figures are AIB Group (UK) p.l.c.'s own single (solo/Company) column, "
    "since a separate consolidated 'AIB UK Group' basis ceased being reported once the FRS 101 exemptions took "
    "effect (see CASH_FLOW_EXEMPTION_NOTE above). This produces a real, small entity-basis break in the Statement "
    "of Changes in Equity between the FY2023 Group closing balance (£1,853m) and the FY2024 solo opening balance "
    "(£1,852m) - a genuine £1m difference in AIB UK's own disclosures, not a transcription error - flagged rather "
    "than silently reconciled, the same treatment used for a similar cross-statement inconsistency found in "
    "Monzo's pilot workbook."
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
BALANCE_SHEET_SOURCES = (
    "Sources - Statement of financial position, £m:\n"
    f"FY2025: FY2025 Annual Financial Report, p.33 - {AR2025_URL}\n"
    f"FY2024: FY2025 Annual Financial Report, p.33 (FY2024 comparative column; also independently cross-checked "
    f"against FY2024 Annual Financial Report's own p.96 statement, which matches exactly) - {AR2025_URL}\n"
    f"FY2023: FY2023 Annual Financial Report, p.70 ('AIB UK Group' column) - {AR2023_URL}\n"
    f"FY2022: FY2023 Annual Financial Report, p.70 (FY2022 comparative, 'AIB UK Group' column; matches FY2022 "
    f"Annual Financial Report's own p.70 statement) - {AR2023_URL}\n"
    f"FY2021: FY2022 Annual Financial Report, p.70 (FY2021 comparative, 'AIB UK Group' column) - {AR2022_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + STATEMENT_ENTITY_NOTE
    + "\n\nCORRECTION (HD-066 correctness audit): 'Investment securities' FY2024 (£54m) was previously missing "
      "entirely from this sheet - confirmed via the FY2024 Annual Financial Report's own p.52 Statement of "
      "financial position and the FY2025 Annual Financial Report's own p.33 FY2024 comparative column (both agree: "
      "£54m) - this £54m gap exactly reconciled the previous Total assets tie-out for FY2024. Also added the "
      "explicitly-disclosed nil ('—') FY2025 Investment securities and FY2024 Investments in group undertakings "
      "values (both £0m, not blank) for consistency with how every other year on this row is shown."
    + "\n\nINVESTMENT SECURITIES NOTE-LEVEL BREAKDOWN (checked for all 5 years against each year's own annual "
      "report note, not just the balance sheet page): the 'Investment securities' note discloses only a single "
      "line item, 'Equity shares (unlisted) - measured at FVTPL', which reconciles exactly to 'Total investment "
      "securities' in every year - there is no further split by measurement basis or issuer type to break out, and "
      "no UK government/gilts/treasury exposure sits in this line (that would be unlisted equity shares, not debt "
      "securities). Row relabelled in place (not split into sub-rows) since there is nothing to sum against. "
      "Sourced from: FY2025 Annual Financial Report, note 21 'Investment securities', p.81 (FY2025: £0m; FY2024: "
      f"£54m) - {AR2025_URL}; FY2024 Annual Financial Report, note 20 'Investment securities', p.103 (FY2024: £54m; "
      f"FY2023: £73m) - {AR2024_URL}; FY2023 Annual Financial Report, note 21 'Investment securities' (FY2023: "
      f"£73m; FY2022: £50m) - {AR2023_URL}; FY2022 Annual Financial Report, note 22 'Investment securities', p.129 "
      f"(FY2022: £50m; FY2021: £40m, 'AIB UK Group & AIB UK' basis) - {AR2022_URL}."
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 3056, "FY2024": 3961, "FY2023": 3229, "FY2022": 3924, "FY2021": 5306}),
    ("DATA", "Derivative financial instruments", {"FY2025": 27, "FY2024": 46, "FY2023": 186, "FY2022": 220, "FY2021": 91}),
    ("DATA", "Loans and advances to banks", {"FY2025": 696, "FY2024": 714, "FY2023": 502, "FY2022": 555, "FY2021": 637}),
    ("DATA", "Loans and advances to customers", {"FY2025": 5291, "FY2024": 4708, "FY2023": 5647, "FY2022": 5718, "FY2021": 6198}),
    ("DATA", "Securities financing", {"FY2025": 921}),
    ("DATA", "Investment securities - Equity shares (unlisted), measured at FVTPL", {"FY2025": 0, "FY2024": 54, "FY2023": 73, "FY2022": 50, "FY2021": 40}),
    ("DATA", "Investments in group undertakings", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Intangible assets", {"FY2025": 15, "FY2024": 14, "FY2023": 13, "FY2022": 15, "FY2021": 21}),
    ("DATA", "Property, plant and equipment", {"FY2025": 30, "FY2024": 31, "FY2023": 33, "FY2022": 27, "FY2021": 31}),
    ("DATA", "Other assets", {"FY2025": 22, "FY2024": 22, "FY2023": 13, "FY2022": 55, "FY2021": 17}),
    ("DATA", "Current taxation", {"FY2025": 0, "FY2024": 16, "FY2023": 8, "FY2022": 6, "FY2021": 28}),
    ("DATA", "Deferred tax assets", {"FY2025": 226, "FY2024": 208, "FY2023": 207, "FY2022": 241, "FY2021": 148}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 8, "FY2024": 5, "FY2023": 4, "FY2022": 7, "FY2021": 10}),
    ("DATA", "Retirement benefit assets", {"FY2025": 12, "FY2024": 41, "FY2023": 54, "FY2022": 57, "FY2021": 161}),
    ("TOTAL", "Total assets", {"FY2025": 10304, "FY2024": 9820, "FY2023": 9969, "FY2022": 10875, "FY2021": 12688}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 230, "FY2024": 109, "FY2023": 354, "FY2022": 390, "FY2021": 434}),
    ("DATA", "Customer deposits", {"FY2025": 7588, "FY2024": 7317, "FY2023": 7118, "FY2022": 8204, "FY2021": 10088}),
    ("DATA", "Derivative financial instruments", {"FY2025": 176, "FY2024": 262, "FY2023": 376, "FY2022": 506, "FY2021": 128}),
    ("DATA", "Lease liabilities", {"FY2025": 12, "FY2024": 13, "FY2023": 14, "FY2022": 8, "FY2021": 17}),
    ("DATA", "Current taxation", {"FY2025": 10, "FY2024": 0, "FY2023": 10, "FY2022": 0}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 1, "FY2024": 1, "FY2023": 2, "FY2022": 2, "FY2021": 13}),
    ("DATA", "Other liabilities", {"FY2025": 61, "FY2024": 59, "FY2023": 78, "FY2022": 80, "FY2021": 174}),
    ("DATA", "Accruals and deferred income", {"FY2025": 12, "FY2024": 13, "FY2023": 12, "FY2022": 11, "FY2021": 8}),
    ("DATA", "Provisions for liabilities and commitments", {"FY2025": 12, "FY2024": 12, "FY2023": 11, "FY2022": 20, "FY2021": 34}),
    ("DATA", "Tier 2 subordinated liabilities / other capital instruments", {"FY2025": 141, "FY2024": 141, "FY2023": 141}),
    ("TOTAL", "Total liabilities", {"FY2025": 8243, "FY2024": 7927, "FY2023": 8116, "FY2022": 9221, "FY2021": 10896}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 457, "FY2024": 457, "FY2023": 457, "FY2022": 2384, "FY2021": 2384}),
    ("DATA", "Reserves", {"FY2025": 1494, "FY2024": 1326, "FY2023": 1286, "FY2022": -730, "FY2021": -592}),
    ("TOTAL", "Total shareholders' equity", {"FY2025": 1951, "FY2024": 1783, "FY2023": 1743, "FY2022": 1654, "FY2021": 1792}),
    ("DATA", "Other equity interests (AT1)", {"FY2025": 110, "FY2024": 110, "FY2023": 110}),
    ("TOTAL", "Total equity", {"FY2025": 2061, "FY2024": 1893, "FY2023": 1853, "FY2022": 1654, "FY2021": 1792}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 10304, "FY2024": 9820, "FY2023": 9969, "FY2022": 10875, "FY2021": 12688}),
]

bw.add_balance_sheet_sheet(
    title="AIB Group (UK) p.l.c. — Statement of Financial Position",
    subtitle="£m. See source note at bottom for the Group (FY2021-FY2023) vs solo (FY2024-FY2025) entity-basis switch.",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=64,
    source_height=210,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
INCOME_STATEMENT_SOURCES = (
    "Sources - (Consolidated) income statement, £m:\n"
    f"FY2025: FY2025 Annual Financial Report, p.31 - {AR2025_URL}\n"
    f"FY2024: FY2025 Annual Financial Report, p.31 (FY2024 comparative column; matches FY2024 Annual Financial "
    f"Report's own p.50 statement) - {AR2025_URL}\n"
    f"FY2023: FY2023 Annual Financial Report, p.68 ('AIB UK Group'/consolidated column - NOT the 'AIB UK' solo "
    f"column shown alongside it in that report, nor the solo-basis FY2023 comparative later reused in the FY2024 "
    f"report) - {AR2023_URL}\n"
    f"FY2022: FY2023 Annual Financial Report, p.68 (FY2022 comparative, 'AIB UK Group' column; matches FY2022 "
    f"Annual Financial Report's own p.68 statement) - {AR2023_URL}\n"
    f"FY2021: FY2022 Annual Financial Report, p.68 (FY2021 comparative, 'AIB UK Group' column) - {AR2022_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + STATEMENT_ENTITY_NOTE
    + "\n\nDISCREPANCY FLAGGED: the FY2024 Annual Financial Report's own FY2023 comparative column (p.50) shows "
      "Profit for the year £275m / Total operating income £449m - these are the 'AIB UK' SOLO figures, not the "
      "£269m/£443m 'AIB UK Group' consolidated figures FY2023's own report used (matching the same Group-vs-solo "
      "entity switch as the balance sheet note above). This sheet uses FY2023's own report's Group-basis figures "
      "throughout for consistency with FY2021-FY2022. Separately, the FY2022 Annual Financial Report's narrative "
      "text states FY2021 profit as '£172m', but both the FY2021 income statement and statement of comprehensive "
      "income tables in the same report show the AIB UK Group figure as £170m (£172m is the AIB UK solo figure) - "
      "£170m (Group) is used here for consistency."
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 434, "FY2024": 470, "FY2023": 459, "FY2022": 280, "FY2021": 218}),
    ("DATA", "Interest and similar expense", {"FY2025": -136, "FY2024": -128, "FY2023": -81, "FY2022": -27, "FY2021": -20}),
    ("TOTAL", "Net interest income", {"FY2025": 298, "FY2024": 342, "FY2023": 378, "FY2022": 253, "FY2021": 198}),
    ("DATA", "Fee and commission income", {"FY2025": 38, "FY2024": 41, "FY2023": 42, "FY2022": 48, "FY2021": 45}),
    ("DATA", "Fee and commission expense", {"FY2025": -2, "FY2024": -4, "FY2023": -4, "FY2022": -4, "FY2021": -4}),
    ("DATA", "Net trading and other financial income/(expense)", {"FY2025": -1, "FY2024": 2, "FY2023": 2, "FY2022": 8, "FY2021": 7}),
    ("DATA", "Net gain/(loss) on other financial assets measured at FVTPL", {"FY2025": 0, "FY2024": -19, "FY2023": 23, "FY2022": 10, "FY2021": 6}),
    ("DATA", "Net gain/(loss) on derecognition of financial assets at amortised cost", {"FY2025": 0, "FY2024": 18, "FY2023": 1, "FY2022": -16, "FY2021": -8}),
    ("DATA", "Other operating income/(expense)", {"FY2025": 51, "FY2024": 12, "FY2023": 1, "FY2022": 2, "FY2021": -3}),
    ("TOTAL", "Total other income", {"FY2025": 86, "FY2024": 50, "FY2023": 65, "FY2022": 48, "FY2021": 43}),
    ("TOTAL", "Total operating income", {"FY2025": 384, "FY2024": 392, "FY2023": 443, "FY2022": 301, "FY2021": 241}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Operating expenses", {"FY2025": -125, "FY2024": -121, "FY2023": -117, "FY2022": -109, "FY2021": -141}),
    ("DATA", "Impairment and amortisation of intangible assets", {"FY2025": -5, "FY2024": -6, "FY2023": -6, "FY2022": -8, "FY2021": -8}),
    ("DATA", "Impairment and depreciation of property, plant and equipment", {"FY2025": -4, "FY2024": -4, "FY2023": -4, "FY2022": -5, "FY2021": -11}),
    ("TOTAL", "Total operating expenses", {"FY2025": -134, "FY2024": -131, "FY2023": -127, "FY2022": -122, "FY2021": -160}),
    ("TOTAL", "Operating profit before impairment losses", {"FY2025": 250, "FY2024": 261, "FY2023": 316, "FY2022": 179, "FY2021": 81}),
    ("DATA", "Net credit impairment charge/(writeback)", {"FY2025": -1, "FY2024": -21, "FY2023": 21, "FY2022": -41, "FY2021": 8}),
    ("DATA", "Impairment of investments in group undertakings", {"FY2025": 0, "FY2024": -1}),
    ("TOTAL", "Profit before taxation", {"FY2025": 249, "FY2024": 239, "FY2023": 337, "FY2022": 138, "FY2021": 89}),
    ("DATA", "Income tax charge/(credit)", {"FY2025": -12, "FY2024": -51, "FY2023": -68, "FY2022": -23, "FY2021": 81}),
    ("TOTAL", "Profit for the year", {"FY2025": 237, "FY2024": 188, "FY2023": 269, "FY2022": 115, "FY2021": 170}),
]

bw.add_income_statement_sheet(
    title="AIB Group (UK) p.l.c. — Income Statement",
    subtitle="£m. See source note at bottom for the Group (FY2021-FY2023) vs solo (FY2024-FY2025) entity-basis switch and a flagged discrepancy.",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_CHANGES_SOURCES = (
    "Sources - Statement of changes in equity, £m ('AIB UK Group' consolidated column FY2021-FY2023, solo/Company "
    "column FY2024-FY2025):\n"
    f"FY2021 movements + 1 Jan 2021 opening balance: FY2022 Annual Financial Report, p.71 (FY2021 comparative) - {AR2022_URL}\n"
    f"FY2022 movements: FY2022 Annual Financial Report, p.71 - {AR2022_URL}\n"
    f"FY2023 movements: FY2023 Annual Financial Report, p.71 ('AIB UK Group' block) - {AR2023_URL}\n"
    f"FY2024 movements + 1 Jan 2024 opening balance: FY2025 Annual Financial Report, p.35 (FY2024 statement) - {AR2025_URL}\n"
    f"FY2025 movements: FY2025 Annual Financial Report, p.34 - {AR2025_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + STATEMENT_ENTITY_NOTE
    + "\n\nJUDGEMENT CALL: FY2021-FY2022 reports disclose only a single combined 'Other reserves' column (not split "
      "into Capital redemption / Revaluation reserves as FY2023 onward does) - since AIB UK's Capital redemption "
      "reserve was only created by the November 2023 share buyback, the FY2021-FY2022 'Other reserves' figures are "
      "mapped to the 'Revaluation reserves' column here (Capital redemption reserves left blank for those years)."
)

EQUITY_HEADERS = ["Share capital", "Capital redemption reserves", "Revaluation reserves",
                   "Cash flow hedging reserve", "Revenue reserves", "Other equity interests (AT1)", "Total equity"]

equity_changes_rows = [
    ("TOTAL", "Balance at 1 January 2021", (2384, None, 2, 33, -745, None, 1674)),
    ("DATA", "Profit for the year", (None, None, None, None, 170, None, 170)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, None, -57, 5, None, -52)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, -57, 175, None, 118)),
    ("TOTAL", "Balance at 31 December 2021", (2384, None, 2, -24, -570, None, 1792)),
    ("DATA", "Profit for the year", (None, None, None, None, 115, None, 115)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, None, -185, -68, None, -253)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, -185, 47, None, -138)),
    ("DATA", "Other movements", (None, None, -1, None, 1, None, 0)),
    ("TOTAL", "Balance at 31 December 2022", (2384, None, 1, -209, -522, None, 1654)),
    ("DATA", "Profit for the year", (None, None, None, None, 269, None, 269)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, None, 73, -2, None, 71)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, 73, 267, None, 340)),
    ("DATA", "Capital reduction", (-1788, None, None, None, 1788, None, 0)),
    ("DATA", "Buyback of ordinary shares", (-139, 139, None, None, -250, None, -250)),
    ("DATA", "Issue of Additional Tier 1 securities", (None, None, None, None, None, 110, 110)),
    ("DATA", "Other movements", (None, None, None, None, -1, None, -1)),
    ("TOTAL", "Balance at 31 December 2023 (AIB UK Group basis)", (457, 139, 1, -136, 1282, 110, 1853)),
    ("TOTAL", "Balance at 1 January 2024 (AIB UK solo basis - entity switch, see note)", (457, 139, 1, -136, 1281, 110, 1852)),
    ("DATA", "Profit for the year", (None, None, None, None, 188, None, 188)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, None, -20, -9, None, -29)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, -20, 179, None, 159)),
    ("DATA", "Dividends paid on ordinary shares", (None, None, None, None, -107, None, -107)),
    ("DATA", "Distributions paid on other equity interests", (None, None, None, None, -11, None, -11)),
    ("TOTAL", "Balance at 31 December 2024", (457, 139, 1, -156, 1342, 110, 1893)),
    ("DATA", "Profit for the year", (None, None, None, None, 237, None, 237)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, None, 49, -19, None, 30)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, 49, 218, None, 267)),
    ("DATA", "Dividends paid on ordinary shares", (None, None, None, None, -88, None, -88)),
    ("DATA", "Distributions paid on other equity interests", (None, None, None, None, -11, None, -11)),
    ("DATA", "Other movements", (None, None, -1, None, 1, None, 0)),
    ("TOTAL", "Balance at 31 December 2025", (457, 139, 0, -107, 1462, 110, 2061)),
]

bw.add_equity_changes_sheet(
    title="AIB Group (UK) p.l.c. — Statement of Changes in Equity",
    subtitle="£m, chronological (oldest to newest). See source note at bottom for the Group-to-solo entity-basis break between FY2023 and FY2024.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=58,
    source_height=230,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before taxation for the year", {"FY2023": 337, "FY2022": 138, "FY2021": 89}),
    ("DATA", "Non-cash items", {"FY2023": -29, "FY2022": 67, "FY2021": 27}),
    ("TOTAL", "Net cash inflow from operating activities before changes in operating assets and liabilities",
     {"FY2023": 308, "FY2022": 205, "FY2021": 116}),
    ("DATA", "Change in loans and advances to banks", {"FY2023": -72, "FY2022": 142, "FY2021": -73}),
    ("DATA", "Change in loans and advances to customers", {"FY2023": 88, "FY2022": 419, "FY2021": 679}),
    ("DATA", "Change in deposits by banks", {"FY2023": -16, "FY2022": -18, "FY2021": -32}),
    ("DATA", "Change in customer accounts", {"FY2023": -1086, "FY2022": -1884, "FY2021": 109}),
    ("DATA", "Change in derivative financial instruments", {"FY2023": 3, "FY2022": -3, "FY2021": 2}),
    ("DATA", "Change in notes in circulation", {"FY2023": -6, "FY2022": -44, "FY2021": -50}),
    ("DATA", "Change in other assets", {"FY2023": 42, "FY2022": -37, "FY2021": 1}),
    ("DATA", "Change in other liabilities", {"FY2023": -1, "FY2022": -64, "FY2021": 1}),
    ("TOTAL", "Net cash (outflow)/inflow from operating assets and liabilities",
     {"FY2023": -1048, "FY2022": -1489, "FY2021": 637}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities before taxation",
     {"FY2023": -740, "FY2022": -1284, "FY2021": 753}),
    ("DATA", "Taxation (paid)/refund", {"FY2023": -54, "FY2022": 2, "FY2021": -3}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities", {"FY2023": -794, "FY2022": -1282, "FY2021": 750}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Additions to property, plant and equipment", {"FY2023": 0, "FY2022": -4, "FY2021": -7}),
    ("DATA", "Proceeds from disposals of property, plant and equipment", {"FY2023": 1, "FY2022": 1, "FY2021": 0}),
    ("DATA", "Additions to intangible assets", {"FY2023": -4, "FY2022": -2, "FY2021": -4}),
    ("TOTAL", "Net cash outflow from investing activities", {"FY2023": -3, "FY2022": -5, "FY2021": -11}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Buyback of ordinary shares", {"FY2023": -250}),
    ("DATA", "Proceeds on issues of debt securities", {"FY2023": 140}),
    ("DATA", "Net proceeds on issue of additional Tier 1 securities", {"FY2023": 110}),
    ("DATA", "Repayment of secondary non-preferential debt", {"FY2022": 0, "FY2021": -45}),
    ("DATA", "Repayment of lease liabilities", {"FY2023": -3, "FY2022": -9, "FY2021": -3}),
    ("TOTAL", "Net cash outflow from financing activities", {"FY2023": -3, "FY2022": -9, "FY2021": -48}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2023": -800, "FY2022": -1296, "FY2021": 691}),
    ("DATA", "Opening cash and cash equivalents", {"FY2023": 4057, "FY2022": 5353, "FY2021": 4662}),
    ("TOTAL", "Closing cash and cash equivalents", {"FY2023": 3257, "FY2022": 4057, "FY2021": 5353}),
]

bw.add_cash_flow_sheet(
    title="AIB Group (UK) p.l.c. — Statement of Cash Flows",
    subtitle="AIB UK Group (consolidated) basis, £m. FY2024-FY2025 blank - see source note at bottom (FRS 101 cash-flow exemption).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - loans and advances to customers, by internal credit grading and IFRS 9 stage (at amortised cost), £m:\n"
    f"FY2025 and FY2024: FY2025 Annual Financial Report, p.73 (Note 20(f), 'Credit profile of the loan portfolio') "
    f"and p.79 (Note 20(h), ECL allowance movements) - {AR2025_URL}\n"
    f"FY2023 and FY2022: FY2023 Annual Financial Report, p.120 (Note 21(f)) - {AR2023_URL}\n"
    f"FY2021: FY2022 Annual Financial Report, p.120 (Note 21(f), FY2021 comparative) - {AR2022_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTE: AIB UK does not disclose loans and advances to customers by product (e.g. mortgages "
      "vs. term loans vs. overdrafts) at a group total level - only a credit-quality/stage breakdown and a "
      "sector-concentration breakdown (not reproduced here as a distinct line item set). 'Non-performing' = Stage 3 "
      "throughout. Coverage/NPL ratios below are CALCULATED from the gross carrying amount and ECL allowance "
      "figures above (AIB UK does not itself publish these ratios as named percentages, aside from the "
      "£0.3bn/4.4%-of-gross-loans NPL figure narrated in the FY2023 Financial review, which matches the calculated "
      "FY2023 Stage 3/NPL ratio here exactly).\n\n"
      "CORRECTION (HD-066 correctness audit): FY2023 and FY2022 Strong/Satisfactory were previously wrongly left "
      "blank on the assumption only the combined 'Total strong/satisfactory' figure was disclosed for those years. "
      "The FY2023 Annual Financial Report's own Note 21(f) (p.120) in fact splits both years: FY2023 Strong £4,233m "
      "/ Satisfactory £998m (sums to the Total strong/satisfactory £5,231m already shown), FY2022 Strong £3,959m / "
      "Satisfactory £1,092m (sums to £5,051m) - both now added. FY2021 genuinely has no such split anywhere - the "
      "FY2022 Annual Financial Report's own Note 21(f) (p.119, covering FY2022/FY2021) shows only the combined "
      "'Total strong/satisfactory' line for both years, i.e. AIB UK had not yet started publishing the split as of "
      "that report - FY2021 Strong/Satisfactory cells remain blank accordingly."
)

asset_quality_rows = [
    ("SECTION", "Gross carrying amount, by credit quality", {}),
    ("DATA", "Strong", {"FY2025": 3038, "FY2024": 2746, "FY2023": 4233, "FY2022": 3959}),
    ("DATA", "Satisfactory", {"FY2025": 2093, "FY2024": 1711, "FY2023": 998, "FY2022": 1092}),
    ("TOTAL", "Total strong/satisfactory", {"FY2025": 5131, "FY2024": 4457, "FY2023": 5231, "FY2022": 5051, "FY2021": 5210}),
    ("DATA", "Criticised watch", {"FY2025": 65, "FY2024": 51, "FY2023": 147, "FY2022": 174, "FY2021": 242}),
    ("DATA", "Criticised recovery", {"FY2025": 75, "FY2024": 111, "FY2023": 149, "FY2022": 361, "FY2021": 435}),
    ("TOTAL", "Total criticised", {"FY2025": 140, "FY2024": 162, "FY2023": 296, "FY2022": 535, "FY2021": 677}),
    ("DATA", "Non-performing (Stage 3)", {"FY2025": 95, "FY2024": 210, "FY2023": 253, "FY2022": 329, "FY2021": 512}),
    ("TOTAL", "Gross carrying amount", {"FY2025": 5366, "FY2024": 4829, "FY2023": 5780, "FY2022": 5915, "FY2021": 6399}),
    ("SECTION", "Gross carrying amount, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 4951, "FY2024": 4127, "FY2023": 4879, "FY2022": 4614, "FY2021": 4791}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": 320, "FY2024": 492, "FY2023": 648, "FY2022": 972, "FY2021": 1096}),
    ("DATA", "Stage 3 (non-performing)", {"FY2025": 95, "FY2024": 210, "FY2023": 253, "FY2022": 329, "FY2021": 512}),
    ("TOTAL", "Gross carrying amount (by stage)", {"FY2025": 5366, "FY2024": 4829, "FY2023": 5780, "FY2022": 5915, "FY2021": 6399}),
    ("SECTION", "ECL allowance, by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2025": -32, "FY2024": -22, "FY2023": -39, "FY2022": -33, "FY2021": -28}),
    ("DATA", "Stage 2", {"FY2025": -18, "FY2024": -21, "FY2023": -41, "FY2022": -82, "FY2021": -80}),
    ("DATA", "Stage 3", {"FY2025": -25, "FY2024": -78, "FY2023": -53, "FY2022": -82, "FY2021": -93}),
    ("TOTAL", "Total ECL allowance", {"FY2025": -75, "FY2024": -121, "FY2023": -133, "FY2022": -197, "FY2021": -201}),
    ("TOTAL", "Loans and advances to customers, net carrying amount", {"FY2025": 5291, "FY2024": 4708, "FY2023": 5647, "FY2022": 5718, "FY2021": 6198}),
    ("SECTION", "Asset quality ratios (calculated)", {}),
    ("DATA", "ECL coverage ratio (Total ECL allowance / Gross carrying amount)", {"FY2025": "1.40%", "FY2024": "2.51%", "FY2023": "2.30%", "FY2022": "3.33%", "FY2021": "3.14%"}),
    ("DATA", "Stage 3 (NPL) ratio (Stage 3 gross / Gross carrying amount)", {"FY2025": "1.77%", "FY2024": "4.35%", "FY2023": "4.38%", "FY2022": "5.56%", "FY2021": "8.00%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", {"FY2025": "26.32%", "FY2024": "37.14%", "FY2023": "20.95%", "FY2022": "24.92%", "FY2021": "18.16%"}),
]

bw.add_asset_quality_sheet(
    title="AIB Group (UK) p.l.c. — Asset Quality / Credit Risk Disclosures",
    subtitle="Loans and advances to customers at amortised cost, £m. See entity note on the Cash Flow Statement sheet.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=62,
    source_height=220,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else "", rows_data, sources_text,
                         note=note, first_col_width=52, source_height=190)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital, transitional", {"FY2025": 1614, "FY2024": 1533, "FY2023": 1407, "FY2022": 1531, "FY2021": 1508})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio, transitional", {"FY2025": "26.8%", "FY2024": "27.7%", "FY2023": "21.44%", "FY2022": "24.11%", "FY2021": "22.81%"})],
    p3_sources("FY2021's CET1 ratio (22.81%) is CALCULATED (CET1 ÷ RWA) - the FY2022 report only states the ratio "
               "increased from an unstated FY2021 base, it never gives the FY2021 % directly."),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 1724, "FY2024": 1643, "FY2023": 1517, "FY2022": 1531, "FY2021": 1508})],
    p3_sources(),
    note="Tier 1 Capital = CET1 Capital for FY2021-FY2022 (no Additional Tier 1 instruments outstanding yet). AIB "
         "UK issued £110m of AT1 as part of a November 2023 capital restructure; Tier 1 Capital from FY2023 onward "
         "is CALCULATED as CET1 + AT1 (£110m every year FY2023-FY2025) - AIB UK's own disclosures give CET1 and "
         "Total Capital explicitly but never break out a separate 'Tier 1' capital or ratio line.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio (calculated: Tier 1 Capital ÷ RWA)", {"FY2025": "28.64%", "FY2024": "29.66%", "FY2023": "23.11%", "FY2022": "24.11%", "FY2021": "22.81%"})],
    p3_sources("Entirely CALCULATED (Tier 1 Capital ÷ Total RWA) - AIB UK does not disclose a Tier 1 ratio as a "
               "distinct line anywhere in its Annual Financial Reports."),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 1865, "FY2024": 1783, "FY2023": 1657, "FY2022": 1531, "FY2021": 1508})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio, transitional", {"FY2025": "31.0%", "FY2024": "32.3%", "FY2023": "25.24%", "FY2022": "24.11%", "FY2021": "22.81%"})],
    p3_sources("FY2021-FY2022 Total Capital Ratio = CET1 Ratio (no AT1/Tier 2 outstanding, so Total Capital = CET1 "
               "those two years)."),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets, transitional", {"FY2025": 6020, "FY2024": 5540, "FY2023": 6564, "FY2022": 6352, "FY2021": 6611})],
    p3_sources(),
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - RWA breakdown by risk category, transitional basis, £m:\n"
    f"FY2025: FY2025 Annual Financial Report, p.5 - {AR2025_URL}\n"
    f"FY2024: FY2024 Annual Financial Report, p.11 - {AR2024_URL}\n"
    f"FY2023: FY2023 Annual Financial Report, p.18 - {AR2023_URL}\n"
    f"FY2022: FY2023 Annual Financial Report, p.18 (FY2022 comparative - the FY2022 Annual Financial Report itself "
    f"discloses only the FY2021-to-FY2022 category-level RWA movement/waterfall, not FY2022's own absolute "
    f"category split, so the next year's report is used instead; the resulting FY2022 Total (£6,352m) still ties "
    f"to the Total RWAs sheet) - {AR2023_URL}\n"
    f"FY2021: not available at category level in any of the four fetched Annual Financial Reports - only the "
    f"aggregate Total RWA (£6,611m, per the Total RWAs sheet) and the FY2021-to-FY2022 movement are disclosed "
    f"(FY2022 Annual Financial Report, p.19) - {AR2022_URL}\n\n"
    + ENTITY_NOTE
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk", {"FY2025": 5258, "FY2024": 4802, "FY2023": 5920, "FY2022": 5835}),
    ("DATA", "Operational risk", {"FY2025": 762, "FY2024": 737, "FY2023": 644, "FY2022": 516}),
    ("DATA", "CVA", {"FY2025": 0, "FY2024": 1, "FY2023": 0, "FY2022": 1}),
    ("TOTAL", "Total RWA", {"FY2025": 6020, "FY2024": 5540, "FY2023": 6564, "FY2022": 6352, "FY2021": 6611}),
]

bw.add_rwa_breakdown_sheet(
    title="AIB Group (UK) p.l.c. — RWA Breakdown",
    subtitle="Transitional basis, £m. FY2021 category-level split not disclosed - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=52,
    source_height=210,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2021": "11.26%"})],
    p3_sources(),
    note="Only FY2021 is disclosed - a one-off figure mentioned in the FY2022 Annual Financial Report's "
         "'Regulatory changes' note ('...significantly increased the Bank's leverage ratio from 11.26% in "
         "December 2021 to 20.22% in March 2022' following a PRA leverage-framework methodology change, PRA "
         "Policy Statement 21/21). No FY2022-FY2025 year-end leverage ratio figure appears anywhere in any of the "
         "five Annual Financial Reports - AIB UK's 'Capital management and liquidity' section covers CET1/Total "
         "Capital/RWA/LCR/NSFR every year but never a leverage ratio outside that single FY2021 mention.\n"
         "The FY2022 break is STRUCTURAL, not an unsourced document. PS21/21 (October 2021, effective "
         "1 January 2022) set the scope of the UK leverage ratio requirement at firms with UK retail deposits "
         ">= GBP 50bn or non-UK assets >= GBP 10bn (PS21/21 paras 1.6, 2.4 and 5.8). AIB Group (UK) p.l.c. is far "
         "below both - GBP 10.3bn TOTAL assets and GBP 7.6bn customer deposits at FY2025 - so it ceased to be an "
         "'LREQ firm' from 1 January 2022, exactly when the disclosure stops. PS21/21 Table 4 (para 5.79) confirms "
         "the 'additional' leverage disclosures (averaged metrics, buffers, distance to requirement) apply on an "
         "LREQ basis only. Consistent with this, AIB UK publishes no Pillar 3 document at all: the string "
         "'Pillar 3' does not appear anywhere in the FY2025 Annual Financial Report, and every capital/liquidity "
         "figure in this workbook is taken from the Annual Report's own narrative capital section. "
         "PS21/21 - https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/policy-statement/2021/october/ps2121.pdf",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {"FY2025": "216%", "FY2024": "282%", "FY2023": "216%", "FY2022": "176%", "FY2021": "169%"})],
    p3_sources(),
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {"FY2025": "157%", "FY2024": "172%", "FY2023": "139%", "FY2022": "145%", "FY2021": "156%"})],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "MREL is not mentioned anywhere in any of AIB Group (UK) p.l.c.'s five Annual Financial "
                      "Reports (FY2021-FY2025) - searched directly, no hits. AIB UK's own capital section discusses "
                      "only the CRR minimum capital requirement (8% Total Capital / 4.5% Tier 1) plus its "
                      "PRA-set Pillar 1 and Pillar 2a add-on, with no separate resolution/MREL requirement "
                      "disclosed - consistent with AIB UK not being its own resolution entity under the Bank of "
                      "England's MREL framework (resolution planning likely sits at the wider AIB Group level).",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 10304, "FY2024": 9820, "FY2023": 9969, "FY2022": 10875, "FY2021": 12688}),
        ("Loans and advances to customers", {"FY2025": 5291, "FY2024": 4708, "FY2023": 5647, "FY2022": 5718, "FY2021": 6198}),
        ("Customer deposits", {"FY2025": 7588, "FY2024": 7317, "FY2023": 7118, "FY2022": 8204, "FY2021": 10088}),
        ("Total equity", {"FY2025": 2061, "FY2024": 1893, "FY2023": 1853, "FY2022": 1654, "FY2021": 1792}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 384, "FY2024": 392, "FY2023": 443, "FY2022": 301, "FY2021": 241}),
        ("Total operating expense", {"FY2025": -134, "FY2024": -131, "FY2023": -127, "FY2022": -122, "FY2021": -160}),
        ("Profit for the year", {"FY2025": 237, "FY2024": 188, "FY2023": 269, "FY2022": 115, "FY2021": 170}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1893, "FY2024": 1852, "FY2023": 1654, "FY2022": 1792, "FY2021": 1674}),
        ("Total comprehensive income for the year", {"FY2025": 267, "FY2024": 159, "FY2023": 340, "FY2022": -138, "FY2021": 118}),
        ("Other equity movements, net", {"FY2025": -99, "FY2024": -118, "FY2023": -141, "FY2022": 0, "FY2021": 0}),
        ("Closing equity", {"FY2025": 2061, "FY2024": 1893, "FY2023": 1853, "FY2022": 1654, "FY2021": 1792}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2023": -794, "FY2022": -1282, "FY2021": 750}),
        ("Net cash from/(used in) investing activities", {"FY2023": -3, "FY2022": -5, "FY2021": -11}),
        ("Net cash from/(used in) financing activities", {"FY2023": -3, "FY2022": -9, "FY2021": -48}),
        ("Closing cash and cash equivalents", {"FY2023": 3257, "FY2022": 4057, "FY2021": 5353}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "26.8%", "FY2024": "27.7%", "FY2023": "21.44%", "FY2022": "24.11%", "FY2021": "22.81%"}),
        ("Tier 1 Ratio", {"FY2025": "28.64%", "FY2024": "29.66%", "FY2023": "23.11%", "FY2022": "24.11%", "FY2021": "22.81%"}),
        ("Total Capital Ratio", {"FY2025": "31.0%", "FY2024": "32.3%", "FY2023": "25.24%", "FY2022": "24.11%", "FY2021": "22.81%"}),
        ("Leverage Ratio", {"FY2021": "11.26%"}),
        ("LCR", {"FY2025": "216%", "FY2024": "282%", "FY2023": "216%", "FY2022": "176%", "FY2021": "169%"}),
        ("NSFR", {"FY2025": "157%", "FY2024": "172%", "FY2023": "139%", "FY2022": "145%", "FY2021": "156%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Cash flow is blank for FY2024-FY2025 (FRS 101 exemption took "
         "effect from FY2024 - see Cash Flow Statement sheet note); Leverage Ratio is populated for FY2021 only "
         "(never disclosed again in later years). Balance Sheet/P&L/Equity blocks are Group basis FY2021-FY2023 and "
         "solo (Company) basis FY2024-FY2025 - see the Statement of Changes in Equity sheet's note on the resulting "
         "£1m entity-basis break in the equity bridge between those years. All figures are AIB Group (UK) p.l.c. "
         "itself, NOT AIB Group plc (the Irish parent) - see entity note on every sheet.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/AIB GROUP UK FINANCIALS.xlsx")
