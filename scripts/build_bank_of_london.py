import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022"]  # most recent first - no clean FY2021 (pre-launch stub periods only)

AR25_URL = "https://find-and-update.company-information.service.gov.uk/company/12844788/filing-history/MzUzODUxMzE5M2FkaXF6a2N4/document?format=pdf&download=0"
AR24_URL = "https://find-and-update.company-information.service.gov.uk/company/12844788/filing-history/MzUwMDM4NjMxMWFkaXF6a2N4/document?format=pdf&download=0"
AR23_URL = "https://find-and-update.company-information.service.gov.uk/company/12844788/filing-history/MzQ2NTkxNTY0NWFkaXF6a2N4/document?format=pdf&download=0"
PRA_NOTICE_URL = "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-action/2026/final-notice-bol-and-oplyse-holdings-limited.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: The Bank of London Group Limited is the entity on the PRA register (company number 12844788) - "
    "no holding-company substitution needed. The company is young: incorporated August 2020, authorised by the PRA "
    "7 October 2021, and only exited 'mobilisation' (the restricted post-authorisation set-up phase) on 3 February "
    "2023. There is no clean 5- or 4-year run of ordinary 12-month accounts stretching back further than shown here "
    "- earlier filings cover irregular stub/mobilisation periods (period to 31 August 2021, then a transition period "
    "to 31 December 2021) that aren't meaningfully comparable, so this workbook covers FY2022-FY2025 (4 years) "
    "rather than 5. FY2022's own annual report took an FRS 101 exemption from presenting a cash flow statement; "
    "FY2022 figures here are the restated prior-year comparative column published in the FY2023 annual report "
    "instead (same audited figures, just sourced from the following year's report)."
)

REGULATORY_NOTE = (
    "REGULATORY NOTE - IMPORTANT: On 23 March 2026 the PRA issued a Final Notice imposing a GBP2 million financial "
    "penalty (reduced from GBP12 million on financial hardship grounds) on The Bank of London Group Limited and its "
    "parent, Oplyse Holdings Limited (formerly The Bank of London Group Holdings Limited), for breaches including "
    "PRA Fundamental Rules 1 (integrity), 3 (prudent conduct), 4 (adequate financial resources) and 7 (open and "
    "cooperative dealing with the regulator), plus Large Exposures and capital-reporting rules, during the "
    "'Relevant Period' of 7 October 2021 to 22 May 2024. The PRA found the Firm repeatedly recognised capital as "
    "CET1-qualifying when it had not in fact been received, that a then senior manager falsified documents to "
    "mislead the PRA about the Firm's true capital position, that the Firm claimed to hold the GBP21.5m capital "
    "required to exit mobilisation on 3 February 2023 when it did not (the cash arrived 28 February 2023), and that "
    "an undocumented intercompany receivable from the Firm to the Parent breached large exposure limits. "
    "PRACTICAL IMPLICATION FOR THIS WORKBOOK: capital-related figures for FY2022, FY2023 and part of FY2024 "
    "(pre-22 May 2024) relate to a period the regulator has since confirmed involved inaccurate capital reporting - "
    "treat any capital metric from that window with caution. Ownership and most senior management have since "
    "changed, with new capital injected and remediation under way. Source: PRA Final Notice, 23 March 2026 - "
    f"{PRA_NOTICE_URL}"
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are The Bank of London Group Limited, £'000. See entity note above re: 4-year window "
    "and FY2022 sourcing.\n"
    f"FY2025: Annual Report and Financial Statements, year ended 31 December 2025, p.28 (Statement of Cash Flows) "
    f"- {AR25_URL}\n"
    f"FY2024: Annual Report and Financial Statements, year ended 31 December 2024, p.27 (Statement of Cash Flows) "
    f"- {AR24_URL}\n"
    f"FY2023: Annual Report and Financial Statements, year ended 31 December 2023, p.30 (Statement of Cash Flows) "
    f"- {AR23_URL}\n"
    f"FY2022: Annual Report and Financial Statements, year ended 31 December 2023, p.30 (restated prior-year "
    f"comparative column - FY2022's own annual report took the FRS 101 cash-flow-statement exemption) - {AR23_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + REGULATORY_NOTE + "\n\n"
    "PRESENTATION NOTE: The operating-activities line items were relabelled/restructured slightly each year as the "
    "business grew (e.g. FY2025 introduced a 'Cash payments to utilise provisions' line and renamed the pre-interest "
    "subtotal). Blank cells indicate that year's report did not disclose that specific split. Section totals and "
    "cash and cash equivalents reconcile exactly across all 4 years."
)

bw = BankWorkbook(bank_name="The Bank of London Group Limited", years=YEARS, header_color="0A2540")

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
BALANCE_SHEET_SOURCES = (
    "Sources - all figures are The Bank of London Group Limited, £'000. See entity note below re: 4-year "
    "window.\n"
    f"FY2025/FY2024: Annual Report and Financial Statements, year ended 31 December 2025, p.26 (Statement of "
    f"Financial Position) - {AR25_URL}\n"
    f"FY2023: Annual Report and Financial Statements, year ended 31 December 2023, p.28 (Statement of Financial "
    f"Position) - {AR23_URL}\n"
    f"FY2022: Annual Report and Financial Statements, year ended 31 December 2023, p.28 (2022 Restated "
    f"comparative column) - {AR23_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + REGULATORY_NOTE + "\n\n"
    "PRESENTATION NOTE: FY2023's own annual report restated its 1 January 2022 and 31 December 2022 balances - "
    "see note 18, 'Prior year adjustments' - reclassifying most of the originally-stated Total equity into a "
    "structure closer to what's shown here; the FY2022 column uses that restated figure (the only version FY2023's "
    "own report carries forward), consistent with the equity ladder on the Statement of Changes in Equity sheet. "
    "Right-of-use-assets and Lease Liability only appear from FY2025 (the Bank took on its first lease that year). "
    "Provisions only appear from FY2024. Total assets = Total liabilities + Total equity exactly in every year."
)

bw.add_balance_sheet_sheet(
    title="The Bank of London Group Limited — Balance Sheet",
    subtitle="Statement of Financial Position, £'000. FY2022-FY2025 (4 years - no clean earlier history). See source note at bottom.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and cash equivalents", {"FY2025": 326874, "FY2024": 829694, "FY2023": 223159, "FY2022": 16412}),
        ("DATA", "Receivables and other assets", {"FY2025": 19074, "FY2024": 18198, "FY2023": 18420, "FY2022": 3539}),
        ("DATA", "Property, plant and equipment", {"FY2025": 16, "FY2024": 52, "FY2023": 87, "FY2022": 93}),
        ("DATA", "Right-of-use assets", {"FY2025": 40}),
        ("TOTAL", "Total assets", {"FY2025": 346004, "FY2024": 847944, "FY2023": 241666, "FY2022": 20044}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Customer deposits", {"FY2025": 301129, "FY2024": 807019, "FY2023": 212531, "FY2022": 1}),
        ("DATA", "Other payables", {"FY2025": 21182, "FY2024": 18488, "FY2023": 2449, "FY2022": 1934}),
        ("DATA", "Provisions", {"FY2025": 382, "FY2024": 294}),
        ("DATA", "Lease liability", {"FY2025": 94}),
        ("TOTAL", "Total liabilities", {"FY2025": 322787, "FY2024": 825801, "FY2023": 214980, "FY2022": 1935}),
        ("SECTION", "Equity", {}),
        ("DATA", "Share capital", {"FY2025": 468, "FY2024": 345, "FY2023": 250, "FY2022": 148}),
        ("DATA", "Share premium", {"FY2025": 95072, "FY2024": 70695, "FY2023": 51790, "FY2022": 31392}),
        ("DATA", "Share-based payment reserve", {"FY2025": 981, "FY2024": 1632, "FY2023": 1205, "FY2022": 714}),
        ("DATA", "Retained earnings", {"FY2025": -73304, "FY2024": -50529, "FY2023": -26559, "FY2022": -14145}),
        ("TOTAL", "Total equity", {"FY2025": 23217, "FY2024": 22143, "FY2023": 26686, "FY2022": 18109}),
        ("TOTAL", "Total liabilities and equity", {"FY2025": 346004, "FY2024": 847944, "FY2023": 241666, "FY2022": 20044}),
    ],
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=48,
    source_height=230,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
INCOME_STATEMENT_SOURCES = (
    "Sources - all figures are The Bank of London Group Limited, £'000. See entity note below re: 4-year "
    "window.\n"
    f"FY2025/FY2024: Annual Report and Financial Statements, year ended 31 December 2025, p.25 (Statement of "
    f"Profit or Loss and other comprehensive income) - {AR25_URL}\n"
    f"FY2023: Annual Report and Financial Statements, year ended 31 December 2023, p.27 (Statement of Profit or "
    f"Loss and other comprehensive income) - {AR23_URL}\n"
    f"FY2022: Annual Report and Financial Statements, year ended 31 December 2023, p.27 (2022 Restated "
    f"comparative column) - {AR23_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + REGULATORY_NOTE + "\n\n"
    "PRESENTATION NOTE: FY2025/FY2024's own report labels the top line 'Interest revenue'; FY2023/FY2022's own "
    "report labels the same line 'Interest income' - same line, relabelled, not a data difference. Taxation is "
    "nil in every year shown (the Bank has never recognised a deferred tax asset against its accumulated losses - "
    "see the CET1 Ratio sheet's regulatory note). Total comprehensive loss for the year = Loss for the year "
    "exactly in every year (no OCI items disclosed in any year)."
)

bw.add_income_statement_sheet(
    title="The Bank of London Group Limited — Profit & Loss",
    subtitle="Statement of Profit or Loss and other comprehensive income, £'000. FY2022-FY2025 (4 years). See source note at bottom.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest income", {"FY2025": 24290, "FY2024": 24027, "FY2023": 3502, "FY2022": 227}),
        ("DATA", "Interest expense", {"FY2025": -20149, "FY2024": -21279, "FY2023": -2308, "FY2022": -1}),
        ("TOTAL", "Net interest income", {"FY2025": 4141, "FY2024": 2748, "FY2023": 1194, "FY2022": 226}),
        ("DATA", "Fee and commission income", {"FY2025": 3088, "FY2024": 1510, "FY2023": 216, "FY2022": 0}),
        ("DATA", "Fee and commission expense", {"FY2025": -466, "FY2024": -431, "FY2023": -198, "FY2022": -376}),
        ("TOTAL", "Net fee and commission income/(expense)", {"FY2025": 2622, "FY2024": 1079, "FY2023": 18, "FY2022": -376}),
        ("DATA", "Credit loss expense on financial assets", {"FY2025": -42, "FY2024": -136, "FY2023": -395, "FY2022": -93}),
        ("DATA", "Other operating expense", {"FY2025": -7, "FY2024": -2, "FY2023": -1, "FY2022": -5}),
        ("TOTAL", "Net operating income/(expense)", {"FY2025": 6714, "FY2024": 3689, "FY2023": 816, "FY2022": -248}),
        ("DATA", "Administrative expenses", {"FY2025": -30217, "FY2024": -27659, "FY2023": -13230, "FY2022": -12575}),
        ("TOTAL", "Loss before taxation", {"FY2025": -23503, "FY2024": -23970, "FY2023": -12414, "FY2022": -12823}),
        ("DATA", "Taxation", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0}),
        ("TOTAL", "Loss for the year", {"FY2025": -23503, "FY2024": -23970, "FY2023": -12414, "FY2022": -12823}),
        ("TOTAL", "Total comprehensive loss for the year", {"FY2025": -23503, "FY2024": -23970, "FY2023": -12414, "FY2022": -12823}),
    ],
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=48,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_CHANGES_SOURCES = (
    "Sources - all figures are The Bank of London Group Limited, £'000.\n"
    f"FY2025/FY2024: Annual Report and Financial Statements, year ended 31 December 2025, p.27 (Statement of "
    f"Changes in Equity) - {AR25_URL}\n"
    f"FY2023/FY2022 (incl. the 1 January 2022 restatement): Annual Report and Financial Statements, year ended "
    f"31 December 2023, p.29 (Statement of Changes in Equity) - {AR23_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + REGULATORY_NOTE + "\n\n"
    "PRESENTATION NOTE: FY2023's own report restated the 1 January 2022 opening balance (originally Share capital "
    "GBP103k, Share premium GBP22,437k, Total equity GBP21,218k) down to Retained earnings of GBP(1,322)k only - "
    "see note 18, 'Prior year adjustments', in that report; the underlying reason for the restatement isn't "
    "detailed further in the extracted pages. Every closing balance below ties exactly to that year's own Balance "
    "Sheet Total equity and to the next year's opening balance - zero undocumented plug rows."
)

bw.add_equity_changes_sheet(
    title="The Bank of London Group Limited — Statement of Changes in Equity",
    subtitle="£'000, chronological (oldest to newest). See source note at bottom.",
    headers=["Share capital", "Share premium", "Total share capital", "Share-based payment reserve", "Retained earnings", "Total equity"],
    rows=[
        ("DATA", "Balance as at 1 January 2022 (as originally stated)", (103, 22437, 22540, None, -1322, 21218)),
        ("DATA", "Prior year adjustment (net of tax)", (-103, -22437, -22540, None, 0, -22540)),
        ("TOTAL", "Balance as at 1 January 2022 (restated)", (0, 0, 0, None, -1322, -1322)),
        ("DATA", "Loss for the year (FY2022)", (None, None, None, None, -12823, -12823)),
        ("DATA", "Issue of shares (FY2022)", (148, 31392, 31540, None, None, 31540)),
        ("DATA", "Share-based payment reserve (FY2022)", (None, None, None, 714, None, 714)),
        ("TOTAL", "Balance as at 31 December 2022 (restated)", (148, 31392, 31540, 714, -14145, 18109)),
        ("DATA", "Loss for the year (FY2023)", (None, None, None, None, -12414, -12414)),
        ("DATA", "Issue of shares (FY2023)", (102, 20398, 20500, None, None, 20500)),
        ("DATA", "Share-based payment reserve (FY2023)", (None, None, None, 491, None, 491)),
        ("TOTAL", "Balance as at 31 December 2023", (250, 51790, 52040, 1205, -26559, 26686)),
        ("DATA", "Loss for the year (FY2024)", (None, None, None, None, -23970, -23970)),
        ("DATA", "Issue of shares (FY2024)", (95, 18905, 19000, None, None, 19000)),
        ("DATA", "Share-based payment reserve (FY2024)", (None, None, None, 427, None, 427)),
        ("TOTAL", "Balance as at 31 December 2024", (345, 70695, 71040, 1632, -50529, 22143)),
        ("DATA", "Loss for the year (FY2025)", (None, None, None, None, -23503, -23503)),
        ("DATA", "Issue of shares (FY2025)", (123, 24377, 24500, None, None, 24500)),
        ("DATA", "Share-based payment reserve (FY2025)", (None, None, None, 77, None, 77)),
        ("DATA", "Recycling share-based payment reserve (FY2025)", (None, None, None, -728, 728, 0)),
        ("TOTAL", "Balance as at 31 December 2025", (468, 95072, 95540, 981, -73304, 23217)),
    ],
    sources_text=EQUITY_CHANGES_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Cash generated from/(used in) operations", {"FY2024": 585593, "FY2023": 185085, "FY2022": -15245}),
    ("DATA", "Net cash (used in)/from operating activities (pre-interest)", {"FY2025": -532314}),
    ("DATA", "Interest received from central bank", {"FY2025": 25200, "FY2024": 23209, "FY2023": 3502, "FY2022": 227}),
    ("DATA", "Interest paid on customer deposits", {"FY2025": -20149, "FY2024": -21250, "FY2023": -2308, "FY2022": -1}),
    ("DATA", "Cash payments to utilise provisions", {"FY2025": -56}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": -527319, "FY2024": 587552, "FY2023": 186279, "FY2022": -15019}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -1, "FY2024": -17, "FY2023": -32, "FY2022": -109}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -1, "FY2024": -17, "FY2023": -32, "FY2022": -109}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Proceeds on share issue", {"FY2025": 24500, "FY2024": 19000, "FY2023": 20500, "FY2022": 31540}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": 24500, "FY2024": 19000, "FY2023": 20500, "FY2022": 31540}),
    ("TOTAL", "Total cash and cash equivalents movement for the year", {"FY2025": -502820, "FY2024": 606535, "FY2023": 206747, "FY2022": 16412}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 829694, "FY2024": 223159, "FY2023": 16412, "FY2022": 0}),
    ("TOTAL", "Total cash and cash equivalents at end of the year", {"FY2025": 326874, "FY2024": 829694, "FY2023": 223159, "FY2022": 16412}),
]

bw.add_cash_flow_sheet(
    title="The Bank of London Group Limited — Cash Flow Statement",
    subtitle="£'000. FY2022-FY2025 (4 years - no clean earlier history; company launched Nov 2021). See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=56,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - all figures are The Bank of London Group Limited, £'000.\n"
    f"FY2025/FY2024: Annual Report and Financial Statements, year ended 31 December 2025, p.42 (note 9, "
    f"'Receivables and other assets') - {AR25_URL}\n"
    f"FY2023/FY2022: Annual Report and Financial Statements, year ended 31 December 2023, p.43 (note 9, "
    f"'Receivables and other assets') - {AR23_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + REGULATORY_NOTE + "\n\n"
    "SCOPE NOTE - IMPORTANT: The Bank of London Group Limited is a payments/clearing-focused bank with "
    "essentially no customer lending book (see the REGULATORY NOTE and the Balance Sheet sheet - there is no "
    "'Loans and advances to customers' line at all). The only IFRS 9 expected-credit-loss (ECL) disclosure the "
    "Bank publishes covers the ECL-bearing components of 'Receivables and other assets' (trade receivables and "
    "intercompany amounts owed by group undertakings) - this sheet is built from that note rather than a "
    "loan-book stage split, since no such split exists for this bank. These net figures don't sum to the full "
    "Balance Sheet 'Receivables and other assets' line, which also includes non-ECL items (accrued income, lease "
    "deposits, prepayments) - documented, not a tie error. Movement-in-provisions figures independently cross-"
    "checked: FY2025's report states the FY2023 closing provision balance (GBP488k) as its own '1 January 2024' "
    "opening figure, matching FY2023's report exactly."
)

bw.add_asset_quality_sheet(
    title="The Bank of London Group Limited — Asset Quality",
    subtitle="Credit risk on Receivables and other assets (no customer loan book - see scope note), £'000. FY2022-FY2025.",
    rows=[
        ("SECTION", "Trade receivables", {}),
        ("DATA", "Trade receivables (gross)", {"FY2025": 182, "FY2024": 197, "FY2023": 49, "FY2022": 38}),
        ("DATA", "ECL provision", {"FY2025": -61, "FY2024": -83, "FY2023": -9, "FY2022": 0}),
        ("TOTAL", "Trade receivables (net)", {"FY2025": 121, "FY2024": 114, "FY2023": 40, "FY2022": 38}),
        ("SECTION", "Amounts owed by group undertakings", {}),
        ("DATA", "Amounts owed by group undertakings (gross)", {"FY2025": 18694, "FY2024": 18263, "FY2023": 18618, "FY2022": 3497}),
        ("DATA", "ECL provision", {"FY2025": -449, "FY2024": -457, "FY2023": -479, "FY2022": -93}),
        ("TOTAL", "Amounts owed by group undertakings (net)", {"FY2025": 18245, "FY2024": 17806, "FY2023": 18139, "FY2022": 3404}),
        ("TOTAL", "Total ECL provision (credit loss allowance)", {"FY2025": -510, "FY2024": -540, "FY2023": -488, "FY2022": -93}),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=54,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
NOT_DISCLOSED_SOURCES = (
    "No standalone Pillar 3 disclosure document is published by The Bank of London Group Limited - checked the "
    "Bank's website (no investor-relations/regulatory-disclosures page exists) and general web search; nothing "
    "found. The only capital metric found anywhere in the public domain is the Common Equity Tier 1 (CET1) ratio "
    "disclosed in a note within the statutory Annual Report - see the CET1 Ratio sheet. No CET1/Tier 1/Total "
    "capital amounts, RWA figure, leverage ratio, LCR, NSFR or MREL data could be found for any year.\n\n"
    + REGULATORY_NOTE
)

bw.add_metric_sheet(
    "CET1 Capital", None,
    [("Common Equity Tier 1 (CET1) capital", {y: "Not publicly disclosed" for y in YEARS})],
    NOT_DISCLOSED_SOURCES,
    note="No absolute CET1 capital amount is disclosed anywhere publicly - only the CET1 ratio (see CET1 Ratio sheet).",
    first_col_width=46, source_height=210,
)

bw.add_metric_sheet(
    "CET1 Ratio", "% (unaudited, as disclosed in the Annual Report's capital note)",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "82.94%", "FY2024": "88.91%"})],
    (
        "FY2025: Annual Report and Financial Statements, year ended 31 December 2025, note 'Capital and Liquidity "
        f"Oversight', p.51 (labelled 'unaudited') - {AR25_URL} (also gives the FY2024 comparator shown here)\n"
        "FY2023/FY2022: not found - no equivalent capital note was located in those years' annual reports, and no "
        "standalone Pillar 3 disclosure exists.\n\n" + REGULATORY_NOTE
    ),
    note="This is the only Pillar 3-style metric found publicly disclosed anywhere for this bank, in any year. The "
         "Annual Report separately states 'Our capital structure comprises Tier 1 instruments only', implying the "
         "Tier 1 ratio and Total Capital ratio would equal this CET1 ratio - but neither is explicitly stated, so "
         "they are not populated as data (see those sheets). The very high ratio (82.94%/88.91%) reflects a small, "
         "cash-heavy balance sheet with minimal risk-weighted lending, typical of a young payments/clearing-focused "
         "bank - not a transcription error.",
    first_col_width=46, source_height=210,
)

bw.add_metric_sheet(
    "Tier 1 Capital", None,
    [("Tier 1 capital", {y: "Not publicly disclosed" for y in YEARS})],
    NOT_DISCLOSED_SOURCES,
    note="Not disclosed as an absolute amount. The Annual Report states the Bank's capital structure 'comprises "
         "Tier 1 instruments only', implying Tier 1 capital = CET1 capital, but neither absolute figure is published.",
    first_col_width=46, source_height=210,
)

bw.add_metric_sheet(
    "Tier 1 Ratio", None,
    [("Tier 1 ratio", {y: "Not publicly disclosed" for y in YEARS})],
    NOT_DISCLOSED_SOURCES,
    note="Not explicitly disclosed. Given the Annual Report states capital is 'Tier 1 instruments only', this would "
         "conceptually equal the CET1 ratio (see CET1 Ratio sheet) - but is not populated here since it isn't "
         "separately stated in the source.",
    first_col_width=46, source_height=210,
)

bw.add_metric_sheet(
    "Total Capital", None,
    [("Total capital", {y: "Not publicly disclosed" for y in YEARS})],
    NOT_DISCLOSED_SOURCES,
    note="Not disclosed as an absolute amount for any year.",
    first_col_width=46, source_height=210,
)

bw.add_metric_sheet(
    "Total Capital Ratio", None,
    [("Total capital ratio", {y: "Not publicly disclosed" for y in YEARS})],
    NOT_DISCLOSED_SOURCES,
    note="Not explicitly disclosed. As with the Tier 1 ratio, this would conceptually equal the CET1 ratio given "
         "the Bank has no AT1 or Tier 2 capital, but is not populated here since it isn't separately stated.",
    first_col_width=46, source_height=210,
)

bw.add_metric_sheet(
    "Total RWAs", None,
    [("Total risk-weighted exposure amount", {y: "Not publicly disclosed" for y in YEARS})],
    NOT_DISCLOSED_SOURCES,
    first_col_width=46, source_height=210,
)

bw.add_rwa_breakdown_sheet(
    title="The Bank of London Group Limited — RWA Breakdown",
    subtitle="Not publicly disclosed - see note below.",
    rows=[("DATA", "Total risk-weighted exposure amount", {y: "Not publicly disclosed" for y in YEARS})],
    sources_text=NOT_DISCLOSED_SOURCES,
    first_col_width=46,
    source_height=210,
)

bw.add_metric_sheet(
    "Leverage Ratio", None,
    [("Leverage ratio", {y: "Not publicly disclosed" for y in YEARS})],
    NOT_DISCLOSED_SOURCES,
    first_col_width=46, source_height=210,
)

bw.add_metric_sheet(
    "LCR", None,
    [("Liquidity Coverage Ratio", {y: "Not publicly disclosed" for y in YEARS})],
    NOT_DISCLOSED_SOURCES,
    first_col_width=46, source_height=210,
)

bw.add_metric_sheet(
    "NSFR", None,
    [("Net Stable Funding Ratio", {y: "Not publicly disclosed" for y in YEARS})],
    NOT_DISCLOSED_SOURCES,
    first_col_width=46, source_height=210,
)

bw.add_metric_sheet(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    NOT_DISCLOSED_SOURCES,
    note="No MREL disclosure of any kind (numeric or qualitative) was found for this bank.",
    first_col_width=46, source_height=210,
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 346004, "FY2024": 847944, "FY2023": 241666, "FY2022": 20044}),
        ("Total liabilities", {"FY2025": 322787, "FY2024": 825801, "FY2023": 214980, "FY2022": 1935}),
        ("Total equity", {"FY2025": 23217, "FY2024": 22143, "FY2023": 26686, "FY2022": 18109}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 4141, "FY2024": 2748, "FY2023": 1194, "FY2022": 226}),
        ("Net operating income/(expense)", {"FY2025": 6714, "FY2024": 3689, "FY2023": 816, "FY2022": -248}),
        ("Loss for the year", {"FY2025": -23503, "FY2024": -23970, "FY2023": -12414, "FY2022": -12823}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Total equity", {"FY2025": 23217, "FY2024": 22143, "FY2023": 26686, "FY2022": 18109}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -527319, "FY2024": 587552, "FY2023": 186279, "FY2022": -15019}),
        ("Net cash used in investing activities", {"FY2025": -1, "FY2024": -17, "FY2023": -32, "FY2022": -109}),
        ("Net cash from financing activities", {"FY2025": 24500, "FY2024": 19000, "FY2023": 20500, "FY2022": 31540}),
        ("Total cash and cash equivalents at end of the year", {"FY2025": 326874, "FY2024": 829694, "FY2023": 223159, "FY2022": 16412}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "82.94%", "FY2024": "88.91%"}),
        ("Tier 1 Ratio", {y: "Not publicly disclosed" for y in YEARS}),
        ("Total Capital Ratio", {y: "Not publicly disclosed" for y in YEARS}),
        ("Leverage Ratio", {y: "Not publicly disclosed" for y in YEARS}),
        ("LCR", {y: "Not publicly disclosed" for y in YEARS}),
        ("NSFR", {y: "Not publicly disclosed" for y in YEARS}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. No standalone Pillar 3 disclosure is published by this bank - "
         "the CET1 ratio (FY2025/FY2024 only) is the only Pillar 3-style metric found anywhere in the public domain "
         "for any year, so the ratios chart below is necessarily sparse. See the REGULATORY NOTE on the Cash Flow "
         "Statement sheet re: a March 2026 PRA Final Notice covering inaccurate capital reporting in part of this "
         "window.",
)

bw.save("/Users/armaan/code/katalysis/banks/THE BANK OF LONDON GROUP FINANCIALS.xlsx")
