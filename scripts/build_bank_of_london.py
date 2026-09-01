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
