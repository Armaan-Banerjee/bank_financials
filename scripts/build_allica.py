import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]  # most recent first

AR2025_URL = "https://www.allica.bank/hubfs/pdf/allica-bank_annual-report-2025.pdf"
AR2023_URL = "https://www.allica.bank/hubfs/Allica-Bank_Annual-report_2023.pdf"
AR2022_URL = "https://www.allica.bank/hubfs/pdf/web/investor-relations/Allica_Bank-Annual_Report-2022.pdf"
AR2020_URL = ("https://find-and-update.company-information.service.gov.uk/company/07706156/filing-history/"
              "MzMxMTI2MDM1MWFkaXF6a2N4/document?format=pdf — Allica Bank Limited consolidated financial "
              "statements for the year ended 31 December 2020, filed with Companies House (registered "
              "number 07706156) 27 August 2021")

P3_2025_URL = "https://www.allica.bank/hubfs/pdf/Pillar-3-Report-2025_Allica.pdf"
P3_2024_URL = "https://www.allica.bank/hubfs/pdf/Pillar-3-Report-2024_Allica.pdf"
P3_2023_URL = "https://www.allica.bank/hubfs/Allica%20Bank%20Limited_Pillar%203%20Report%20_Year-ended%2031%20December%202023.pdf"
P3_2022_URL = "https://www.allica.bank/hubfs/pdf/web/investor-relations/Allica_Bank_Pillar_3_disclosure_2022.pdf"
P3_2020_URL = "https://www.allica.bank/hubfs/pdf/web/investor-relations/Allica_Bank_Pillar_3_disclosure_2020.pdf"

HISTORICAL_DEPTH_NOTE = (
    "HISTORICAL DEPTH NOTE (HD-056, 2026-09): FY2020 added as the earliest comparable full-year column. "
    "FY2019 and FY2018 were deliberately NOT added despite Allica's confirmed entity-existence floor being "
    "FY2018 (Companies House no. 07706156, incorporated 2011). Verified directly against the primary filings: "
    "(1) the FY2018 accounts (year ended 31 July 2018, filed under the pre-Allica name 'Civilised Bank "
    "Limited') show nil turnover and no banking assets/liabilities at all — the company had returned its "
    "banking licence to the PRA in May 2018 and was a pre-launch shell; (2) there is no standalone calendar-"
    "year FY2019 set of accounts at all — the next filing after July 2018 is a 17-month period ended 31 "
    "December 2019, during which the company (renamed 'Allica Bank Limited' from 10 September 2019) was "
    "granted its banking licence on 5 September 2019 but had made no loans and taken no deposits by the "
    "period end ('little operating activity ... no customers on the loan book as at 31 December 2019' — "
    "Directors' Report). A standalone Pillar 3 disclosure for this 17-month period does exist (LCR 18,883%, "
    "Leverage ratio 91%) and confirms the pre-launch nature of the balance sheet rather than filling a real "
    "gap. Including either period as an ordinary FY column would misrepresent a pre-operational shell/startup "
    "balance sheet as comparable 'bank financials' and would distort every flow-statement sheet (a 17-month "
    "cumulative P&L/cash flow sitting in a column next to 12-month columns). The one exception is the "
    "Statement of Changes in Equity sheet, which is a chronological (not year-column) roll-forward of the "
    "same continuous legal entity — that sheet has been extended back to the FY2018 floor (1 August 2017) "
    "since it is not distorted by the irregular period lengths."
)

CASH_FLOW_SOURCES = (
    "Sources — all figures are Allica Bank Limited consolidated (Group) cash flow statement, £m:\n"
    f"FY2025 & FY2024: Allica Bank Limited Annual Report & Accounts 2025, p.92-93 (Statement of cash flows) — {AR2025_URL}\n"
    f"FY2023 & FY2022: Allica Bank Limited Annual Report and Accounts 2023, p.76-77 & Note 32 p.130-131 (Statements of "
    f"cash flows / Note 32: Cash flow information) — {AR2023_URL}\n"
    f"FY2021: Allica Bank Limited Annual Report and Accounts 2022, p.85 & Note 32 p.139 (Statements of cash flows / "
    f"Note 32: Cash flow information) — {AR2022_URL}\n"
    f"FY2020: Allica Bank Limited Consolidated Financial Statements for the year ended 31 December 2020, p.25 "
    f"(Statement of cash flows) & Note 30 p.54-55 (Cash flow information) — {AR2020_URL}\n"
    "Note: Allica changed cash flow statement presentation across report vintages. FY2021-FY2023 reports show a Note 32 "
    "reconciliation (profit before tax + non-cash adjustments + working capital changes = 'Cash generated from "
    "operations') and then add actual cash 'Interest income received'/'Interest expense paid' on the face of the "
    "primary statement to reach 'Net cash from operating activities'. FY2024-FY2025 reports show the full "
    "reconciliation (including accrued-interest reversal lines) directly on the face of the statement with no "
    "separate interest-received/paid lines, reaching 'Net cash from operating activities' via 'Tax paid' alone. Blank "
    "cells indicate a line not separately disclosed that year under the applicable presentation; the operating/"
    "investing/financing/net-change/cash-at-year-end TOTAL rows are all consistent and comparable across all years "
    "(independently cross-checked by hand against each year's underlying line items). FY2024-FY2025 also newly "
    "disclose 'Acquisition of a subsidiary, net of cash acquired' and a foreign-exchange translation line, both nil/"
    "absent in FY2020-FY2023 (Allica had no foreign operations in that earlier period). FY2020's Note 30 reconciliation "
    "bundles several small non-cash items (interest on lease liability, net FX differences) into this sheet's 'Other "
    "non-cash items' row rather than the finer split used from FY2021 onward; 'Interest income received (cash)' / "
    "'Interest expense paid (cash)' for FY2020 are the primary statement's combined 'Interest received'/'Interest "
    "paid' lines. See HISTORICAL_DEPTH_NOTE below this block in the script for why FY2019/FY2018 are not included."
)

def p3_sources(extra_note=None):
    text = (
        "Sources — Allica Bank Limited consolidated (Group) basis, UK KM1 Key Metrics table, £'000:\n"
        f"FY2025: Allica Bank Limited Pillar 3 Report 2025, p.2 — {P3_2025_URL}\n"
        f"FY2024: Allica Bank Limited Pillar 3 Report 2024, p.2 — {P3_2024_URL}\n"
        f"FY2023: Allica Bank Limited Pillar 3 Report 2023, p.2-3 — {P3_2023_URL}\n"
        f"FY2022: Allica Bank Limited Pillar 3 Report, year ended 31 December 2022, p.2 — {P3_2022_URL}\n"
        f"FY2021: comparative column of the FY2022 Pillar 3 Report above, p.2 (restated onto the post-1 Jan 2022 "
        "leverage exposure basis per PRA PS21/21).\n"
        f"FY2020: Allica Bank Limited Pillar 3 disclosure, year ended 31 December 2020, p.11 (Common Equity "
        f"Tier 1 capital, RWA, ratios) — {P3_2020_URL}"
    )
    if extra_note:
        text += "\n" + extra_note
    return text

bw = BankWorkbook(bank_name="Allica Bank Limited", years=YEARS, header_color="C1440E")

ENTITY_NOTE = (
    "Entity note: all figures on this and the Balance Sheet/Profit & Loss/Statement of Changes in Equity sheets "
    "are Allica Bank Limited Group (consolidated), £m. FY2025 & FY2024 sourced from Allica Bank Limited Annual "
    f"Report & Accounts 2025 (£m as reported) — {AR2025_URL}; FY2023 & FY2022 sourced from Allica Bank Limited "
    f"Annual Report and Accounts 2023 (£'000 as reported, converted to £m for consistency with other years) — "
    f"{AR2023_URL}; FY2021 sourced from the FY2021 comparative column of Allica Bank Limited Annual Report and "
    f"Accounts 2022 (£'000 as reported, converted to £m) — {AR2022_URL} — no separate FY2021 Annual Report was "
    "located, matching the existing Cash Flow Statement sheet's own FY2021 sourcing convention. FY2020 sourced "
    f"from Allica Bank Limited's own Consolidated Financial Statements for the year ended 31 December 2020 "
    f"(£'000 as reported, converted to £m), filed with Companies House — {AR2020_URL}. A disclosed nil "
    "('–' in the source table) is written as 0; a blank cell means that year's report did not disclose that "
    "specific line at all."
)

BALANCE_SHEET_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: 'Amounts due from subsidiaries' (Company-only) and 'Investments in subsidiaries' "
    "(Company-only) are excluded here since this sheet is Group/consolidated basis only. 'Investments' and "
    "'Deferred tax asset' are both explicitly disclosed as nil ('–') for FY2021, not omitted from that year's "
    "statement. 'Goodwill' only appears as its own line from FY2024 onward (Allica's first acquisition); "
    "FY2020-2023 have no goodwill line. 'Cash collateral' (a liability) only appears FY2021-2023; not present "
    "in the FY2024-2025 statements (nil/not applicable by then). FY2020's own statement of financial position "
    "does not disclose an 'Investments', 'Deferred tax asset', 'Deposits from banks', 'Cash collateral' or "
    "'Subordinated liabilities/external borrowings' line at all (left blank, not zero) and captions two rows "
    "slightly differently ('Due from Banks' -> 'Loans and advances to banks'; 'Customer deposits' -> 'Deposits "
    "from customers') — mapped onto the same rows as later years for comparability; figures are as disclosed. "
    "See HISTORICAL_DEPTH_NOTE in this script for why FY2019/FY2018 are not included as columns here."
)

BALANCE_SHEET_SOURCES = (
    "Sources — Allica Bank Limited consolidated (Group) Statement of Financial Position, £m:\n"
    f"FY2025 & FY2024: Annual Report & Accounts 2025, p.87-88 (Statements of financial position) — {AR2025_URL}\n"
    f"FY2023 & FY2022: Annual Report and Accounts 2023, p.72-73 (Statements of financial position) — {AR2023_URL}\n"
    f"FY2021: Annual Report and Accounts 2022, p.79-80 (Statements of financial position, FY2021 comparative "
    f"column) — {AR2022_URL}\n"
    f"FY2020: Consolidated Financial Statements for the year ended 31 December 2020, p.23 (Statement of "
    f"financial position) — {AR2020_URL}\n\n" + ENTITY_NOTE + "\n\n" + BALANCE_SHEET_PRESENTATION_NOTE + "\n\n"
    "DEBT SECURITIES BREAKDOWN: checked for a measurement-basis / issuer-type split (as in Close Brothers' "
    "workbook) and found none available to sub-divide — the 'Debt securities' line is relabelled in place "
    "rather than split into sub-rows. Every year's accounts state debt securities are held to meet liquidity "
    "requirements and classified in full as Fair Value Through Other Comprehensive Income ('FVOCI') — see "
    "Annual Report & Accounts 2025 Note 2 'Material accounting policies', p.99, Annual Report and Accounts 2023 "
    "Note 2 'Basis of preparation and material accounting policies', and Annual Report and Accounts 2022 Note 2 "
    "'Basis of preparation and significant accounting policies' (all materially identical wording, all years). "
    "Issuer type: FY2025 & FY2024 Note 10 'Debt securities', p.118, discloses only one "
    "combined line, 'Issued by governments and supranational bodies' (£1,154.0m / £301.4m) — not split further "
    "into UK sovereign vs supranational/other. FY2023, FY2022 and FY2021 reports carry no equivalent numbered "
    "note for debt securities at all (the Statement of financial position line itself has no note reference in "
    "those vintages) and disclose only the same FVOCI classification plus a fair-value-hierarchy note describing "
    "the balance as 'Bonds and Treasury Bills' valued from quoted market prices, with no issuer-type split. "
    "Relabelled to 'Debt securities - Government and supranational bonds, at FVOCI' for all years to reflect "
    "this."
)

bw.add_balance_sheet_sheet(
    title="Allica Bank Limited — Consolidated Statement of Financial Position",
    subtitle="Allica Bank Limited Group (consolidated basis), £m",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances at central banks", {"FY2025": 1104.3, "FY2024": 1378.0, "FY2023": 718.805, "FY2022": 230.150, "FY2021": 295.291, "FY2020": 92.925}),
        ("DATA", "Loans and advances to banks", {"FY2025": 183.8, "FY2024": 124.6, "FY2023": 87.763, "FY2022": 64.093, "FY2021": 17.290, "FY2020": 10.338}),
        ("DATA", "Debt securities - Government and supranational bonds, at FVOCI", {"FY2025": 1154.0, "FY2024": 301.4, "FY2023": 115.774, "FY2022": 65.552, "FY2021": 40.406}),
        ("DATA", "Derivative financial instruments", {"FY2025": 9.1, "FY2024": 23.5, "FY2023": 19.570, "FY2022": 27.846, "FY2021": 0.058, "FY2020": 0.004}),
        ("DATA", "Loans and advances to customers", {"FY2025": 3742.0, "FY2024": 3048.8, "FY2023": 1976.826, "FY2022": 1348.166, "FY2021": 566.040, "FY2020": 45.040}),
        ("DATA", "Investments", {"FY2025": 1.0, "FY2024": 1.0, "FY2023": 1.000, "FY2022": 1.000, "FY2021": 0}),
        ("DATA", "Other assets", {"FY2025": 13.9, "FY2024": 10.4, "FY2023": 6.212, "FY2022": 8.659, "FY2021": 22.549, "FY2020": 1.791}),
        ("DATA", "Tangible fixed assets", {"FY2025": 1.3, "FY2024": 1.2, "FY2023": 0.805, "FY2022": 0.616, "FY2021": 0.249, "FY2020": 0.214}),
        ("DATA", "Right-of-use assets", {"FY2025": 3.2, "FY2024": 0.3, "FY2023": 0.836, "FY2022": 1.333, "FY2021": 0.146, "FY2020": 0.339}),
        ("DATA", "Intangible assets", {"FY2025": 30.0, "FY2024": 25.4, "FY2023": 18.426, "FY2022": 12.857, "FY2021": 8.178, "FY2020": 14.092}),
        ("DATA", "Goodwill", {"FY2025": 16.4, "FY2024": 8.6}),
        ("DATA", "Deferred tax asset", {"FY2025": 9.9, "FY2024": 11.3, "FY2023": 12.902, "FY2022": 2.198, "FY2021": 0}),
        ("TOTAL", "Total assets", {"FY2025": 6268.9, "FY2024": 4934.5, "FY2023": 2958.919, "FY2022": 1762.470, "FY2021": 950.207, "FY2020": 164.743}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits from banks", {"FY2025": 0.3, "FY2024": 16.8}),
        ("DATA", "Cash collateral", {"FY2023": 3.485, "FY2022": 23.514, "FY2021": 0}),
        ("DATA", "Deposits from customers", {"FY2025": 5719.9, "FY2024": 4428.1, "FY2023": 2633.247, "FY2022": 1507.433, "FY2021": 845.769, "FY2020": 104.299}),
        ("DATA", "Other liabilities", {"FY2025": 27.4, "FY2024": 19.3, "FY2023": 10.523, "FY2022": 9.023, "FY2021": 5.887, "FY2020": 3.523}),
        ("DATA", "Derivative financial instruments", {"FY2025": 22.4, "FY2024": 8.1, "FY2023": 22.518, "FY2022": 3.915, "FY2021": 0.988, "FY2020": 0.024}),
        ("DATA", "Provisions", {"FY2023": 1.617, "FY2022": 0.490, "FY2021": 0.066, "FY2020": 0.088}),
        ("DATA", "Subordinated liabilities / external borrowings", {"FY2025": 71.7, "FY2024": 85.1, "FY2023": 7.500, "FY2022": 7.500, "FY2021": 7.500}),
        ("DATA", "Leases", {"FY2025": 3.2, "FY2024": 0.4, "FY2023": 0.887, "FY2022": 1.324, "FY2021": 0.114, "FY2020": 0.321}),
        ("TOTAL", "Total liabilities", {"FY2025": 5844.9, "FY2024": 4557.8, "FY2023": 2679.777, "FY2022": 1553.199, "FY2021": 860.324, "FY2020": 108.255}),
        ("SECTION", "Equity", {}),
        ("DATA", "Share capital", {"FY2025": 3.7, "FY2024": 3.4, "FY2023": 2.873, "FY2022": 2.501, "FY2021": 1.417, "FY2020": 1.003}),
        ("DATA", "Share premium", {"FY2025": 323.0, "FY2024": 280.9, "FY2023": 301.158, "FY2022": 266.332, "FY2021": 160.708, "FY2020": 120.321}),
        ("DATA", "Perpetual notes (including convertible)", {"FY2025": 44.9, "FY2024": 44.9, "FY2023": 45.127, "FY2022": 9.886, "FY2021": 17.500}),
        ("DATA", "Other components of equity", {"FY2025": -4.2, "FY2024": 11.3, "FY2023": -2.937, "FY2022": 16.781, "FY2021": 2.110, "FY2020": -0.022}),
        ("DATA", "Retained earnings/(accumulated losses)", {"FY2025": 56.6, "FY2024": 36.2, "FY2023": -67.079, "FY2022": -86.229, "FY2021": -91.852, "FY2020": -64.814}),
        ("TOTAL", "Total equity", {"FY2025": 424.0, "FY2024": 376.7, "FY2023": 279.142, "FY2022": 209.271, "FY2021": 89.883, "FY2020": 56.488}),
        ("TOTAL", "Total liabilities and equity", {"FY2025": 6268.9, "FY2024": 4934.5, "FY2023": 2958.919, "FY2022": 1762.470, "FY2021": 950.207, "FY2020": 164.743}),
    ],
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=58,
    source_height=170,
    unit_suffix=" (£m)",
)

INCOME_STATEMENT_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: FY2024-2025 present a single 'Operating expenses' line on the face of the statement "
    "(sub-breakdown moved to a note); FY2020-2023 break this into Administrative expenses / Depreciation and "
    "amortisation / Staff costs, each shown here and rolling up to the same 'Total operating expenses' TOTAL "
    "row. FY2022's OCI detail is taken from Allica's own FY2022 Annual Report (Annual Report and Accounts 2022) "
    "rather than the FY2023 report's restated comparative column, per this workbook's per-year-primary-source "
    "convention — the FY2023 report's FY2022 comparative omits the 'Net change in fair value of financial "
    "instruments during the year' line that FY2022's own report discloses; both are otherwise consistent. "
    "FY2020 is Allica's first full year of banking operations and its Statement of profit or loss discloses no "
    "separate fee/commission or fair-value-gain lines at all that year (net interest income of £204k IS the "
    "reported 'Net interest and other operating income' / total operating income figure, with no other income "
    "items — those lines only start being separately disclosed from FY2021); left blank rather than zero for "
    "FY2020. See HISTORICAL_DEPTH_NOTE in this script for why FY2019/FY2018 are not included as columns here."
)

INCOME_STATEMENT_SOURCES = (
    "Sources — Allica Bank Limited consolidated (Group) Statement of Profit or Loss and Other Comprehensive "
    "Income, £m:\n"
    f"FY2025 & FY2024: Annual Report & Accounts 2025, p.85-86 — {AR2025_URL}\n"
    f"FY2023: Annual Report and Accounts 2023, p.70-71 — {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts 2022, p.75-76 (own-year figures) — {AR2022_URL}\n"
    f"FY2021: Annual Report and Accounts 2022, p.75-76 (FY2021 comparative column) — {AR2022_URL}\n"
    f"FY2020: Consolidated Financial Statements for the year ended 31 December 2020, p.22 (Statement of profit "
    f"or loss and other comprehensive income) — {AR2020_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + INCOME_STATEMENT_PRESENTATION_NOTE
)

bw.add_income_statement_sheet(
    title="Allica Bank Limited — Consolidated Statement of Profit or Loss and Other Comprehensive Income",
    subtitle="Allica Bank Limited Group (consolidated basis), £m",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest income", {"FY2025": 404.2, "FY2024": 320.3, "FY2023": 177.843, "FY2022": 72.252, "FY2021": 11.494, "FY2020": 0.739}),
        ("DATA", "Interest expense", {"FY2025": -245.2, "FY2024": -206.3, "FY2023": -97.813, "FY2022": -23.341, "FY2021": -3.670, "FY2020": -0.535}),
        ("TOTAL", "Net interest income", {"FY2025": 159.0, "FY2024": 114.0, "FY2023": 80.030, "FY2022": 48.911, "FY2021": 7.824, "FY2020": 0.204}),
        ("DATA", "Net fair value gains/(losses) on financial instruments", {"FY2025": 6.5, "FY2024": 11.8, "FY2023": 6.905, "FY2022": 0.067, "FY2021": -0.155}),
        ("DATA", "Fee and commission income", {"FY2025": 7.5, "FY2024": 3.7, "FY2023": 2.838, "FY2022": 0.587, "FY2021": 0.159}),
        ("DATA", "Fee and commission expense", {"FY2025": -14.4, "FY2024": -9.1, "FY2023": -2.965, "FY2022": -1.253, "FY2021": -0.002}),
        ("TOTAL", "Net fee and commission income/(expense)", {"FY2025": -6.9, "FY2024": -5.4, "FY2023": -0.127, "FY2022": -0.666, "FY2021": 0.157}),
        ("TOTAL", "Total operating income", {"FY2025": 158.6, "FY2024": 120.4, "FY2023": 86.808, "FY2022": 48.312, "FY2021": 7.826, "FY2020": 0.204}),
        ("SECTION", "Expenses", {}),
        ("DATA", "Operating expenses", {"FY2025": -108.4, "FY2024": -80.3}),
        ("DATA", "Administrative expenses", {"FY2023": -18.016, "FY2022": -14.266, "FY2021": -7.890, "FY2020": -8.001}),
        ("DATA", "Depreciation and amortisation", {"FY2023": -5.394, "FY2022": -3.337, "FY2021": -9.445, "FY2020": -2.098}),
        ("DATA", "Staff costs", {"FY2023": -33.028, "FY2022": -23.823, "FY2021": -14.472, "FY2020": -11.751}),
        ("TOTAL", "Total operating expenses", {"FY2025": -108.4, "FY2024": -80.3, "FY2023": -56.438, "FY2022": -41.426, "FY2021": -31.807, "FY2020": -21.850}),
        ("DATA", "Impairment losses", {"FY2025": -13.3, "FY2024": -10.2, "FY2023": -14.279, "FY2022": -8.473, "FY2021": -1.077, "FY2020": -0.068}),
        ("TOTAL", "Profit/(loss) before tax", {"FY2025": 36.9, "FY2024": 29.9, "FY2023": 16.091, "FY2022": -1.587, "FY2021": -25.058, "FY2020": -21.714}),
        ("DATA", "Taxation charge/credit", {"FY2025": -9.6, "FY2024": -0.1, "FY2023": 3.059, "FY2022": 7.210, "FY2021": 0, "FY2020": 0}),
        ("TOTAL", "Profit/(loss) after tax for the year", {"FY2025": 27.3, "FY2024": 29.8, "FY2023": 19.150, "FY2022": 5.623, "FY2021": -25.058, "FY2020": -21.714}),
        ("SECTION", "Other comprehensive income/(loss)", {}),
        ("DATA", "Fair value gains/(losses) on debt securities", {"FY2025": 0.2, "FY2024": -0.2, "FY2023": 0.837, "FY2022": -0.764, "FY2021": -0.004, "FY2020": 0.002}),
        ("DATA", "Net change in fair value of financial instruments", {"FY2022": 0, "FY2021": 0.020, "FY2020": -0.020}),
        ("DATA", "Exchange differences on translation of foreign operations", {"FY2025": -0.1, "FY2024": 0}),
        ("DATA", "Cash flow hedges: gains/(losses) arising during the year", {"FY2025": -14.3, "FY2024": 31.8, "FY2023": -20.264, "FY2022": 20.431, "FY2021": 0}),
        ("DATA", "Cash flow hedges: amounts recycled to profit or loss", {"FY2025": -6.5, "FY2024": -11.8, "FY2023": -6.759, "FY2022": -0.084, "FY2021": 0.023}),
        ("DATA", "Tax credit/(expense)", {"FY2025": 5.2, "FY2024": -5.0, "FY2023": 6.756, "FY2022": -5.087, "FY2021": 0}),
        ("TOTAL", "Other comprehensive income/(loss) for the year, net of tax", {"FY2025": -15.5, "FY2024": 14.8, "FY2023": -19.430, "FY2022": 14.496, "FY2021": 0.039, "FY2020": -0.018}),
        ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 11.8, "FY2024": 44.6, "FY2023": -0.280, "FY2022": 20.119, "FY2021": -25.019, "FY2020": -21.732}),
    ],
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=58,
    source_height=170,
    unit_suffix=" (£m)",
)

EQUITY_CHANGES_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: chronological roll-forward, £m, 1 August 2017 (Allica's confirmed FY2018 historical "
    "floor, per HD-056) to 31 December 2025 (oldest to newest, unlike the rest of the workbook's most-recent-"
    "first year columns). This sheet is the one exception to HISTORICAL_DEPTH_NOTE's FY2019/FY2018 exclusion: "
    "because it is a chronological roll-forward of one continuous legal entity (Companies House no. 07706156) "
    "rather than a set of side-by-side year columns, the irregular period lengths that make FY2019/FY2018 non-"
    "comparable on the other sheets do not distort this one — each row is self-labelled with its own exact "
    "date range. 'Balance at 1 August 2017' through 'Balance at 31 July 2018' reflect the company's pre-Allica "
    "name and trading identity, 'Civilised Bank Limited' (FRS 102 basis, £ as reported, converted to £m); it "
    "returned its banking licence to the PRA in May 2018 and had nil turnover throughout. 'Balance at 31 July "
    "2018' to 'Balance at 31 December 2019' is a single 17-month period (the accounting reference date changed "
    "from 31 July to 31 December during it) under the renamed 'Allica Bank Limited' (IFRS basis from this "
    "point on); the company was granted its banking licence on 5 September 2019 but had made no loans and "
    "taken no deposits by the period end. 'Perpetual notes (including convertible)' only appears from the 31 "
    "December 2021 balance onward (first issued during FY2021)."
)

EQUITY_CHANGES_SOURCES = (
    "Sources — Allica Bank Limited consolidated (Group) Statement of Changes in Equity, £m:\n"
    f"1 Aug 2017 – 31 Jul 2018 roll-forward (as 'Civilised Bank Limited'): Civilised Bank Limited Strategic "
    f"Report, Report of the Directors and Financial Statements for the Year Ended 31 July 2018, p.11 (Statement "
    f"of Changes in Equity), filed with Companies House (registered number 07706156) 2 May 2019 — "
    f"https://find-and-update.company-information.service.gov.uk/company/07706156/filing-history/"
    f"MzIzMzI4ODY2MWFkaXF6a2N4/document?format=pdf\n"
    f"31 Jul 2018 – 31 Dec 2019 roll-forward (17-month period, as 'Allica Bank Limited (Formerly Civilised "
    f"Bank Limited)'): Financial Statements For The Period Ended 31 December 2019, p.19 (Statement of Changes "
    f"in Equity), filed with Companies House 31 December 2020 — "
    f"https://find-and-update.company-information.service.gov.uk/company/07706156/filing-history/"
    f"MzI4Njg3NjY0M2FkaXF6a2N4/document?format=pdf\n"
    f"1 Jan 2020 – 31 Dec 2020 roll-forward: Allica Bank Limited Consolidated Financial Statements for the "
    f"year ended 31 December 2020, p.24 (Statement of changes in equity) — {AR2020_URL}\n"
    f"1 Jan 2021 – 31 Dec 2022 roll-forward: Annual Report and Accounts 2022, p.82 — {AR2022_URL}\n"
    f"1 Jan 2022 – 31 Dec 2023 roll-forward: Annual Report and Accounts 2023, p.74 — {AR2023_URL}\n"
    f"1 Jan 2024 – 31 Dec 2025 roll-forward: Annual Report & Accounts 2025, p.89 — {AR2025_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + EQUITY_CHANGES_PRESENTATION_NOTE
)

EQUITY_HEADERS = ["Share capital", "Share premium", "Other components of equity", "Perpetual notes (incl. convertible)", "Retained earnings/(accumulated losses)", "Total equity"]

equity_changes_rows = [
    ("TOTAL", "Balance at 1 August 2017 (as Civilised Bank Limited)", (0.007, 6.040, 0.633, None, -4.070, 2.609)),
    ("DATA", "Total comprehensive loss for the year (FY2018, as Civilised Bank Limited)", (None, None, None, None, -8.495, -8.495)),
    ("DATA", "Issue of ordinary share capital", (0.089, 5.448, None, None, None, 5.537)),
    ("DATA", "Capital raising costs", (None, -0.127, None, None, None, -0.127)),
    ("TOTAL", "Balance at 31 July 2018 (as Civilised Bank Limited)", (0.096, 11.360, 0.633, None, -12.565, -0.476)),
    ("DATA", "Loss after tax for the period (17-month period ended 31 December 2019, renamed Allica Bank Limited)", (None, None, None, None, -31.168, -31.168)),
    ("DATA", "Other comprehensive loss for the period, net of tax", (None, None, -0.004, None, None, -0.004)),
    ("TOTAL", "Total comprehensive loss for the period (17 months to 31 December 2019)", (None, None, -0.004, None, -31.168, -31.172)),
    ("DATA", "Issue of share capital", (0.642, 73.382, None, None, None, 74.024)),
    ("DATA", "Capital raising costs", (None, -0.698, None, None, None, -0.698)),
    ("DATA", "Reclassification of other reserves", (None, None, -0.633, None, 0.633, 0)),
    ("TOTAL", "Balance at 31 December 2019", (0.738, 84.044, -0.004, None, -43.100, 41.678)),
    ("DATA", "Loss after tax for the year (FY2020)", (None, None, None, None, -21.714, -21.714)),
    ("DATA", "Other comprehensive loss for the year, net of tax (FY2020)", (None, None, -0.018, None, None, -0.018)),
    ("TOTAL", "Total comprehensive loss for the year (FY2020)", (None, None, -0.018, None, -21.714, -21.732)),
    ("DATA", "Issue of share capital", (0.265, 36.277, None, None, None, 36.542)),
    ("TOTAL", "Balance at 31 December 2020", (1.003, 120.321, -0.022, None, -64.814, 56.488)),
    ("DATA", "Loss after tax for the year (FY2021)", (None, None, None, None, -25.058, -25.058)),
    ("DATA", "Other comprehensive income for the year, net of tax (FY2021)", (None, None, 0.039, None, None, 0.039)),
    ("TOTAL", "Total comprehensive income/(loss) for the year (FY2021)", (None, None, 0.039, None, -25.058, -25.019)),
    ("DATA", "Share-based payments", (None, None, 0.113, None, None, 0.113)),
    ("DATA", "Issue of share warrants", (None, None, 1.980, None, -1.980, 0)),
    ("DATA", "Issue of perpetual notes (including convertible)", (None, None, None, 17.500, None, 17.500)),
    ("DATA", "Issue of ordinary share capital", (0.414, 40.387, None, None, None, 40.801)),
    ("TOTAL", "Balance at 31 December 2021", (1.417, 160.708, 2.110, 17.500, -91.852, 89.883)),
    ("DATA", "Profit after tax credit for the year (FY2022)", (None, None, None, None, 5.623, 5.623)),
    ("DATA", "Other comprehensive income for the year, net of tax (FY2022)", (None, None, 14.496, None, None, 14.496)),
    ("TOTAL", "Total comprehensive income for the year (FY2022)", (None, None, 14.496, None, 5.623, 20.119)),
    ("DATA", "Share-based payments", (None, None, 0.288, None, None, 0.288)),
    ("DATA", "Conversion of perpetual notes (including convertible), net", (None, None, None, -7.614, None, -7.614)),
    ("DATA", "Issue of ordinary share capital", (1.084, 105.624, -0.113, None, None, 106.595)),
    ("TOTAL", "Balance at 31 December 2022", (2.501, 266.332, 16.781, 9.886, -86.229, 209.271)),
    ("DATA", "Profit after tax credit for the year (FY2023)", (None, None, None, None, 19.150, 19.150)),
    ("DATA", "Other comprehensive loss for the year, net of tax (FY2023)", (None, None, -19.430, None, None, -19.430)),
    ("TOTAL", "Total comprehensive income/(loss) for the year (FY2023)", (None, None, -19.430, None, 19.150, -0.280)),
    ("DATA", "Share-based payments", (0.007, 0.281, -0.288, None, None, 0)),
    ("DATA", "Employee bonus share issuance", (0.011, 0.405, None, None, None, 0.416)),
    ("DATA", "Issue of ordinary share capital", (0.354, 34.140, None, None, None, 34.494)),
    ("DATA", "Issue of perpetual convertible notes", (None, None, None, 35.241, None, 35.241)),
    ("TOTAL", "Balance at 31 December 2023", (2.873, 301.158, -2.937, 45.127, -67.079, 279.142)),
    ("DATA", "Profit after tax for the year (FY2024)", (None, None, None, None, 29.8, 29.8)),
    ("DATA", "Other comprehensive income for the year, net of tax (FY2024)", (None, None, 14.8, None, None, 14.8)),
    ("TOTAL", "Total comprehensive income for the year (FY2024)", (None, None, 14.8, None, 29.8, 44.6)),
    ("DATA", "Issue of ordinary share capital and employee bonus shares", (0.1, 17.7, None, None, None, 17.8)),
    ("DATA", "Capital reduction", (None, -73.5, None, None, 73.5, 0)),
    ("DATA", "Issue of perpetual convertible notes", (None, None, None, 35.0, None, 35.0)),
    ("DATA", "Share warrants exercised", (None, 0.6, -0.6, None, None, 0)),
    ("DATA", "Conversion of perpetual convertible notes, net", (0.4, 34.9, None, -35.2, None, 0.1)),
    ("TOTAL", "Balance at 31 December 2024", (3.4, 280.9, 11.3, 44.9, 36.2, 376.7)),
    ("DATA", "Profit after tax for the year (FY2025)", (None, None, None, None, 27.3, 27.3)),
    ("DATA", "Other comprehensive loss for the year, net of tax (FY2025)", (None, None, -15.5, None, None, -15.5)),
    ("TOTAL", "Total comprehensive (loss)/income for the year (FY2025)", (None, None, -15.5, None, 27.3, 11.8)),
    ("DATA", "Issue of ordinary share capital", (0.3, 42.1, None, None, None, 42.4)),
    ("DATA", "Coupon paid on capital securities", (None, None, None, None, -6.9, -6.9)),
    ("TOTAL", "Balance at 31 December 2025", (3.7, 323.0, -4.2, 44.9, 56.6, 424.0)),
]

bw.add_equity_changes_sheet(
    title="Allica Bank Limited — Consolidated Statement of Changes in Equity",
    subtitle="Allica Bank Limited Group (consolidated basis), £m, chronological 1 Aug 2017 - 31 Dec 2025.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=56,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 36.9, "FY2024": 29.9, "FY2023": 16.091, "FY2022": -1.587, "FY2021": -25.058, "FY2020": -21.714}),
    ("DATA", "Depreciation", {"FY2025": 1.5, "FY2024": 1.0, "FY2023": 0.849, "FY2022": 0.491, "FY2021": 0.312, "FY2020": 0.305}),
    ("DATA", "Amortisation", {"FY2025": 9.4, "FY2024": 5.3, "FY2023": 3.606, "FY2022": 2.846, "FY2021": 2.421, "FY2020": 1.777}),
    ("DATA", "Loss on disposal/write-off of fixed assets", {"FY2023": 0.028, "FY2022": 0.059, "FY2021": 0}),
    ("DATA", "Loss on write-off of intangible assets", {"FY2023": 0.939, "FY2022": 0, "FY2021": 6.712, "FY2020": 0.016}),
    ("DATA", "Net fair value (losses)/gains on derivatives", {"FY2025": 0, "FY2024": 0, "FY2023": -0.146, "FY2022": 0.017, "FY2021": 0.147}),
    ("DATA", "Share-based payment charge", {"FY2023": 0, "FY2022": 0.288, "FY2021": 0.113}),
    ("DATA", "Impairment losses", {"FY2025": 13.3, "FY2024": 10.7, "FY2023": 14.279, "FY2022": 8.417, "FY2021": 1.077, "FY2020": 0.068}),
    ("DATA", "Interest income accrued (non-cash reversal)", {"FY2025": -17.2, "FY2024": -14.7, "FY2023": -177.843, "FY2022": -72.252, "FY2021": -11.494, "FY2020": -0.739}),
    ("DATA", "Interest expense accrued (non-cash reversal)", {"FY2025": -9.9, "FY2024": 19.1, "FY2023": 97.813, "FY2022": 23.358, "FY2021": 3.670, "FY2020": 0.516}),
    ("DATA", "Other non-cash items", {"FY2025": 6.6, "FY2024": 0, "FY2020": 0.030}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Net change in balances at central banks", {"FY2025": -0.1, "FY2024": 6.7, "FY2023": -6.106, "FY2022": -2.870, "FY2021": 0}),
    ("DATA", "Net change in loans and advances to banks", {"FY2025": 3.6, "FY2024": 41.7, "FY2023": -16.762, "FY2022": -28.527, "FY2021": 0}),
    ("DATA", "Net change in loans and advances to customers", {"FY2025": -651.3, "FY2024": -1007.9, "FY2023": -618.964, "FY2022": -795.711, "FY2021": -520.942, "FY2020": -45.509}),
    ("DATA", "Net change in deposits from banks", {"FY2025": -16.5, "FY2024": 13.4}),
    ("DATA", "Net change in deposits from customers", {"FY2025": 1301.1, "FY2024": 1778.5, "FY2023": 1101.860, "FY2022": 657.114, "FY2021": 740.017, "FY2020": 103.995}),
    ("DATA", "Net change in cash collateral", {"FY2023": -20.029, "FY2022": 23.514, "FY2021": 0}),
    ("DATA", "Net change in derivatives (balance sheet)", {"FY2022": 0, "FY2021": 0.806}),
    ("DATA", "Net change in trade and other debtors", {"FY2025": -2.5, "FY2024": -2.8, "FY2023": 2.447, "FY2022": 13.890, "FY2021": -20.758, "FY2020": -0.752}),
    ("DATA", "Net change in trade and other creditors", {"FY2025": -1.6, "FY2024": 6.6, "FY2023": 2.034, "FY2022": 2.715, "FY2021": 2.364, "FY2020": 1.433}),
    ("DATA", "Net change in provisions", {"FY2022": 0, "FY2021": -0.024, "FY2020": -0.165}),
    ("DATA", "Interest income received (cash)", {"FY2023": 158.027, "FY2022": 71.813, "FY2021": 10.361, "FY2020": 1.168}),
    ("DATA", "Interest expense paid (cash)", {"FY2023": -76.617, "FY2022": -17.118, "FY2021": -2.217, "FY2020": -0.250}),
    ("DATA", "Tax paid", {"FY2025": -3.7, "FY2024": -3.4, "FY2023": -1.024, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": 669.6, "FY2024": 884.1, "FY2023": 480.482, "FY2022": -113.543, "FY2021": 187.507, "FY2020": 40.179}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities", {"FY2025": -1391.5, "FY2024": -577.0, "FY2023": -49.641, "FY2022": -25.737, "FY2021": -40.410, "FY2020": 0}),
    ("DATA", "Proceeds from sale and maturity of debt securities", {"FY2025": 554.4, "FY2024": 402.2, "FY2020": 29.440}),
    ("DATA", "Purchase of investments", {"FY2023": 0, "FY2022": -1.0, "FY2021": 0}),
    ("DATA", "Acquisition of a subsidiary, net of cash acquired", {"FY2025": 8.0, "FY2024": -6.1}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -0.9, "FY2024": -0.8, "FY2023": -0.568, "FY2022": -0.613, "FY2021": -0.154, "FY2020": -0.125}),
    ("DATA", "Purchase and development of intangible assets", {"FY2025": -11.7, "FY2024": -12.3, "FY2023": -10.114, "FY2022": -7.525, "FY2021": -3.219, "FY2020": -5.390}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -841.7, "FY2024": -194.0, "FY2023": -60.323, "FY2022": -34.875, "FY2021": -43.783, "FY2020": 23.925}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issue of ordinary shares", {"FY2025": 35.0, "FY2024": 17.6, "FY2023": 34.494, "FY2022": 98.981, "FY2021": 40.801, "FY2020": 36.542}),
    ("DATA", "Issue of subordinated debt", {"FY2024": 30.0, "FY2021": 7.5}),
    ("DATA", "Issue of credit-linked notes", {"FY2024": 50.0}),
    ("DATA", "Payment of principal on credit-linked notes", {"FY2025": -46.1, "FY2024": -3.9}),
    ("DATA", "Coupon paid on capital securities", {"FY2025": -6.9}),
    ("DATA", "Issue of perpetual notes (including convertible)", {"FY2024": 35.0, "FY2023": 35.241, "FY2021": 17.5}),
    ("DATA", "Capital repayment of lease liabilities", {"FY2025": -0.8, "FY2024": -0.5, "FY2023": -0.437, "FY2022": -0.298, "FY2021": -0.207, "FY2020": -0.199}),
    ("DATA", "Repayment of external debt", {"FY2025": -19.3, "FY2024": -73.8, "FY2020": 0}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": -38.1, "FY2024": 54.4, "FY2023": 69.298, "FY2022": 98.683, "FY2021": 65.594, "FY2020": 36.343}),
    ("DATA", "Effect of exchange rates on cash and cash equivalents", {"FY2025": -0.1, "FY2024": 0}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -210.3, "FY2024": 744.5, "FY2023": 489.457, "FY2022": -49.735, "FY2021": 209.318, "FY2020": 100.447}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 1496.8, "FY2024": 752.303, "FY2023": 262.846, "FY2022": 312.581, "FY2021": 103.263, "FY2020": 2.816}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 1286.5, "FY2024": 1496.8, "FY2023": 752.303, "FY2022": 262.846, "FY2021": 312.581, "FY2020": 103.263}),
    ("SECTION", "Cash and cash equivalents at end of year comprise", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 1102.7, "FY2024": 1375.8, "FY2023": 709.829, "FY2022": 227.280, "FY2021": 295.291, "FY2020": 92.925}),
    ("DATA", "Loans and advances to banks", {"FY2025": 183.8, "FY2024": 121.0, "FY2023": 42.474, "FY2022": 35.566, "FY2021": 17.290, "FY2020": 10.338}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 1286.5, "FY2024": 1496.8, "FY2023": 752.303, "FY2022": 262.846, "FY2021": 312.581, "FY2020": 103.263}),
]

bw.add_cash_flow_sheet(
    title="Allica Bank Limited — Consolidated Statement of Cash Flows",
    subtitle="Allica Bank Limited Group (consolidated basis), £m unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=170,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
ASSET_QUALITY_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: FY2024-2025 disclose a by-category split (Loans secured on property / Other loans and "
    "advances) alongside IFRS 9 stage in Note 26 'Staging profile of customer lending'; FY2021-2023 disclose "
    "only an internal-risk-rating (Low/Medium/High PD band) x stage breakdown in Note 27, with no by-category "
    "split available at all - left blank for those years rather than estimated. The FY2024/2025 'Gross exposure' "
    "total in Note 26 (£3,802.1m / £3,100.4m) is smaller than Note 11's 'Gross loans and advances to customers' "
    "(£3,781.2m / £3,083.8m is NET after adjustments - Note 26 is in fact the larger, gross-before-fair-value-"
    "hedge-and-EIR-adjustment figure); Note 26 explicitly states its exposures 'exclude adjustments for EIR and "
    "other minor adjustments made to the principal balance' - both figures are transcribed exactly as disclosed, "
    "not reconciled. POCI (purchased or originated credit-impaired) is its own IFRS 9 category, shown separately "
    "from Stage 3 for FY2024-2025 only (not disclosed as a separate line pre-2024). Ratios below use the by-IFRS-9-"
    "stage totals; POCI is included in the gross/ECL totals but excluded from the Stage 3 (NPL) ratio's numerator, "
    "matching Monzo's convention (Stage 3 = credit-impaired, POCI is a distinct IFRS 9 category). FY2020 is Allica's "
    "first year with any loan book at all (first commercial mortgage loan made March 2020) and its accounts contain "
    "no formal by-stage/by-category table — only a narrative disclosure (Note 24) that 'all impairment provisions "
    "are Stage 1 apart from one loan amounting to £495k in stage 3 ... with an immaterial ECL'. The FY2020 Stage 1/"
    "Stage 3 gross split below is therefore derived from that narrative (Total gross exposure 45,080 less the "
    "disclosed £495k Stage 3 loan), not read from a table; FY2020 Stage 2, and the by-stage ECL split, are left "
    "blank as genuinely not disclosed that year (only the £40k Total impairment provision is a directly disclosed "
    "figure)."
)

ASSET_QUALITY_SOURCES = (
    "Sources — Allica Bank Limited consolidated (Group) staging/credit-risk notes, £'000:\n"
    f"FY2025 & FY2024 (by IFRS 9 stage and by category): Annual Report & Accounts 2025, p.139-140 (Note 26, "
    f"'Staging profile of customer lending', Group tables) — {AR2025_URL}\n"
    f"FY2023 (by IFRS 9 stage, by internal risk rating): Annual Report and Accounts 2023, p.115-116 (Note 27) "
    f"— {AR2023_URL}\n"
    f"FY2022 (by IFRS 9 stage, by internal risk rating, own-year figures): Annual Report and Accounts 2022, "
    f"p.124 (Note 27) — {AR2022_URL}\n"
    f"FY2021 (by IFRS 9 stage, own-year closing balance from the year's loss-allowance movement table): Annual "
    f"Report and Accounts 2022, p.124 (Note 27, 'Balance as at 31 December 2021' row) — {AR2022_URL}\n"
    f"FY2020 (total gross/ECL from Note 11; Stage 1/3 split narrative from Note 24 'Diversity and concentration "
    f"of our loan portfolio'): Consolidated Financial Statements for the year ended 31 December 2020, p.40 & "
    f"p.48 — {AR2020_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + ASSET_QUALITY_PRESENTATION_NOTE
)

asset_quality_rows = [
    ("SECTION", "Gross loans and advances to customers, by category", {}),
    ("DATA", "Loans secured on property", {"FY2025": 2875500, "FY2024": 2214200}),
    ("DATA", "Other loans and advances", {"FY2025": 926600, "FY2024": 886200}),
    ("TOTAL", "Total gross exposure (by category)", {"FY2025": 3802100, "FY2024": 3100400}),
    ("SECTION", "Gross loans and advances to customers, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 3308500, "FY2024": 2710100, "FY2023": 1797745, "FY2022": 1277413, "FY2021": 571487, "FY2020": 44585}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": 387100, "FY2024": 308600, "FY2023": 171791, "FY2022": 86511, "FY2021": 4426}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": 100200, "FY2024": 59500, "FY2023": 30093, "FY2022": 9188, "FY2021": 1360, "FY2020": 495}),
    ("DATA", "POCI", {"FY2025": 6300, "FY2024": 22200}),
    ("TOTAL", "Total gross exposure (by stage)", {"FY2025": 3802100, "FY2024": 3100400, "FY2023": 1999629, "FY2022": 1373112, "FY2021": 577273, "FY2020": 45080}),
    ("SECTION", "Expected credit loss (ECL), by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 13100, "FY2024": 13100, "FY2023": 13814, "FY2022": 5667, "FY2021": 918}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": 11400, "FY2024": 6100, "FY2023": 3856, "FY2022": 1815, "FY2021": 45}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": 18100, "FY2024": 13000, "FY2023": 4318, "FY2022": 1495, "FY2021": 21}),
    ("DATA", "POCI", {"FY2025": 0, "FY2024": 800}),
    ("TOTAL", "Total impairment provision (by stage)", {"FY2025": 42600, "FY2024": 33000, "FY2023": 21988, "FY2022": 8977, "FY2021": 984, "FY2020": 40}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "ECL coverage ratio (Total impairment provision / Total gross exposure)", {"FY2025": "1.12%", "FY2024": "1.06%", "FY2023": "1.10%", "FY2022": "0.65%", "FY2021": "0.17%", "FY2020": "0.09%"}),
    ("DATA", "Stage 3 (NPL) ratio (Stage 3 gross exposure / Total gross exposure)", {"FY2025": "2.64%", "FY2024": "1.92%", "FY2023": "1.51%", "FY2022": "0.67%", "FY2021": "0.24%", "FY2020": "1.10%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross exposure)", {"FY2025": "18.06%", "FY2024": "21.85%", "FY2023": "14.35%", "FY2022": "16.28%", "FY2021": "1.54%", "FY2020": "Not disclosed"}),
]

bw.add_asset_quality_sheet(
    title="Allica Bank Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Allica Bank Limited Group (consolidated basis), £'000",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=62,
    source_height=190,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Consolidated (Group) basis, {unit}" if unit else "Consolidated (Group) basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=110)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 325689, "FY2024": 276827, "FY2023": 219055, "FY2022": 170322, "FY2021": 68816, "FY2020": 53152})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "13.4%", "FY2024": "14.5%", "FY2023": "15.7%", "FY2022": "17.1%", "FY2021": "14.1%", "FY2020": "69%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 370566, "FY2024": 321704, "FY2023": 264182, "FY2022": 180208, "FY2021": 86316, "FY2020": 53152})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "15.3%", "FY2024": "16.9%", "FY2023": "18.9%", "FY2022": "18.1%", "FY2021": "17.7%", "FY2020": "69%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 406393, "FY2024": 359031, "FY2023": 271682, "FY2022": 187708, "FY2021": 93816, "FY2020": 53152})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "16.8%", "FY2024": "18.8%", "FY2023": "19.5%", "FY2022": "18.8%", "FY2021": "19.3%", "FY2020": "69%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": 2422216, "FY2024": 1908286, "FY2023": 1396450, "FY2022": 997945, "FY2021": 486558, "FY2020": 77289})],
    p3_sources(),
    note="FY2020's Tier 1 capital and Total capital both equal CET1 capital (£53,152k) — Allica had not yet "
         "issued any Additional Tier 1 or Tier 2 instruments (its first AT1/perpetual notes were issued during "
         "FY2021), so CET1 = Tier 1 = Total capital that year, and the CET1/Tier 1/Total capital ratios are "
         "identical (69%).",
)

RWA_BREAKDOWN_SOURCES = (
    "Sources — Allica Bank Limited consolidated (Group) UK KM1 Key Metrics table (the only Pillar 3 table "
    "Allica publishes — see below):\n"
    f"FY2025: Pillar 3 Report 2025, p.2 — {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Report 2024, p.2 — {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Report 2023, p.2-3 — {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Report, year ended 31 December 2022, p.2 — {P3_2022_URL}\n"
    f"FY2021: comparative column of the FY2022 Pillar 3 Report above.\n"
    f"FY2020: Pillar 3 disclosure, year ended 31 December 2020, p.11 — {P3_2020_URL}\n\n"
    "NOT DISCLOSED (category breakdown): every one of Allica's Pillar 3 reports is a 2-3 page KM1-Key-Metrics-"
    "only disclosure (explicitly published under CRR Article 433b, the small/non-complex institution regime) - "
    "none contains a UK OV1 'Overview of risk weighted exposure amounts' table breaking RWA down by risk "
    "category (credit/market/operational/CVA etc.). Only the single aggregate Total RWA figure exists for every "
    "year (see the Total RWAs sheet, which this sheet's Total row ties out to exactly)."
)

bw.add_rwa_breakdown_sheet(
    title="Allica Bank Limited — RWA Breakdown",
    subtitle="Allica Bank Limited Group (consolidated basis), £'000",
    rows=[
        ("DATA", "Not publicly disclosed — category breakdown", {y: "Not publicly disclosed" for y in YEARS}),
        ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 2422216, "FY2024": 1908286, "FY2023": 1396450, "FY2022": 997945, "FY2021": 486558, "FY2020": 77289}),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=170,
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks (£'000)", {"FY2025": 5092370, "FY2024": 3421039, "FY2023": 2208236, "FY2022": 1595100, "FY2021": 688827}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "7.3%", "FY2024": "9.4%", "FY2023": "11.4%", "FY2022": "11.3%", "FY2021": "12.5%"}),
        ("Total leverage ratio exposure measure, unrestated basis (£'000)", {"FY2020": 166719}),
        ("Leverage ratio, unrestated basis (%)", {"FY2020": "32%"}),
    ],
    p3_sources(),
    note="Allica has never disclosed a leverage ratio 'including claims on central banks' variant in any of these "
         "years and states in every report that it is not an LREQ firm subject to additional leverage ratio "
         "disclosure requirements. The FY2021 figures shown are already restated onto the post-1-January-2022 "
         "exposure-measure basis (PRA Policy Statement 21/21, excluding certain central bank claims) — the FY2022 "
         "Pillar 3 report explicitly restates its FY2021 comparative on this basis to aid comparison, so unlike "
         "several other banks in this series there is no leverage-ratio methodology break within Allica's own "
         "FY2021-2025 window. FY2020 predates PS21/21 entirely, so its exposure measure and ratio (32%, disclosed "
         "in its own row above) are NOT on the same 'excluding central bank claims' basis as FY2021 onward and "
         "are not directly comparable to the row above it — shown separately rather than blended into the main "
         "row to avoid implying a false trend break.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value, average (£'000)", {"FY2025": 1928875, "FY2024": 1137180, "FY2023": 810081, "FY2022": 386347, "FY2021": 171242}),
        ("Total net cash outflows, adjusted value (£'000)", {"FY2025": 873645, "FY2024": 525922, "FY2023": 280344, "FY2022": 127792, "FY2021": 34252}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "220.8%", "FY2024": "216.2%", "FY2023": "289.0%", "FY2022": "302.3%", "FY2021": "499.9%", "FY2020": "331%"}),
    ],
    p3_sources(),
    note="LCR is calculated as a 12-month average per Allica's own Pillar 3 methodology note. FY2020's Pillar 3 "
         "report discloses only the LCR percentage itself (331%), not the underlying HQLA/net-cash-outflow £'000 "
         "components shown for FY2021 onward — those two component rows are left blank for FY2020, not zero.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding (£'000)", {"FY2025": 3884410, "FY2024": 2937724, "FY2023": 1876364, "FY2022": 1338171}),
        ("Total required stable funding (£'000)", {"FY2025": 2799038, "FY2024": 2195700, "FY2023": 1385603, "FY2022": 897829}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "138.8%", "FY2024": "133.8%", "FY2023": "135.4%", "FY2022": "149.0%", "FY2021": "Not disclosed", "FY2020": "Not disclosed"}),
    ],
    p3_sources(),
    note="NSFR was not a Pillar 3 disclosure requirement until FY2022 (the UK NSFR regime took effect from 1 "
         "January 2022), so no FY2021 or FY2020 figures exist. NSFR is calculated as a 4-quarter average. FY2022 "
         "'Total available stable funding' is reported as £1,338,171k in the FY2022 Pillar 3 report's own "
         "current-year column but as £1,338,711k in the FY2023 Pillar 3 report's prior-year comparative column — "
         "an apparent digit transposition in one of the two source PDFs. This sheet uses the FY2022 report's "
         "own-year figure as authoritative; the £540 discrepancy is immaterial and both reports agree the "
         "resulting NSFR ratio is 149.0%.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL ratio row appears in any of Allica's Pillar 3 reports; each explicitly states Allica Bank Limited "
         "is not an LREQ firm. As a smaller institution below the UK's MREL/bail-in resolution threshold, Allica is "
         "not subject to a separate MREL disclosure requirement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 6268.9, "FY2024": 4934.5, "FY2023": 2958.919, "FY2022": 1762.470, "FY2021": 950.207, "FY2020": 164.743}),
        ("Loans and advances to customers", {"FY2025": 3742.0, "FY2024": 3048.8, "FY2023": 1976.826, "FY2022": 1348.166, "FY2021": 566.040, "FY2020": 45.040}),
        ("Deposits from customers", {"FY2025": 5719.9, "FY2024": 4428.1, "FY2023": 2633.247, "FY2022": 1507.433, "FY2021": 845.769, "FY2020": 104.299}),
        ("Total equity", {"FY2025": 424.0, "FY2024": 376.7, "FY2023": 279.142, "FY2022": 209.271, "FY2021": 89.883, "FY2020": 56.488}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 158.6, "FY2024": 120.4, "FY2023": 86.808, "FY2022": 48.312, "FY2021": 7.826, "FY2020": 0.204}),
        ("Total operating expenses", {"FY2025": -108.4, "FY2024": -80.3, "FY2023": -56.438, "FY2022": -41.426, "FY2021": -31.807, "FY2020": -21.850}),
        ("Profit/(loss) after tax for the year", {"FY2025": 27.3, "FY2024": 29.8, "FY2023": 19.150, "FY2022": 5.623, "FY2021": -25.058, "FY2020": -21.714}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 376.7, "FY2024": 279.142, "FY2023": 209.271, "FY2022": 89.883, "FY2021": 56.488, "FY2020": 41.678}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 11.8, "FY2024": 44.6, "FY2023": -0.280, "FY2022": 20.119, "FY2021": -25.019, "FY2020": -21.732}),
        ("Other equity movements, net", {"FY2025": 35.5, "FY2024": 52.958, "FY2023": 70.151, "FY2022": 99.269, "FY2021": 58.414, "FY2020": 36.542}),
        ("Closing equity", {"FY2025": 424.0, "FY2024": 376.7, "FY2023": 279.142, "FY2022": 209.271, "FY2021": 89.883, "FY2020": 56.488}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 669.6, "FY2024": 884.1, "FY2023": 480.482, "FY2022": -113.543, "FY2021": 187.507, "FY2020": 40.179}),
        ("Net cash from/(used in) investing activities", {"FY2025": -841.7, "FY2024": -194.0, "FY2023": -60.323, "FY2022": -34.875, "FY2021": -43.783, "FY2020": 23.925}),
        ("Net cash from/(used in) financing activities", {"FY2025": -38.1, "FY2024": 54.4, "FY2023": 69.298, "FY2022": 98.683, "FY2021": 65.594, "FY2020": 36.343}),
        ("Cash and cash equivalents at end of year", {"FY2025": 1286.5, "FY2024": 1496.8, "FY2023": 752.303, "FY2022": 262.846, "FY2021": 312.581, "FY2020": 103.263}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "13.4%", "FY2024": "14.5%", "FY2023": "15.7%", "FY2022": "17.1%", "FY2021": "14.1%", "FY2020": "69%"}),
        ("Tier 1 Ratio", {"FY2025": "15.3%", "FY2024": "16.9%", "FY2023": "18.9%", "FY2022": "18.1%", "FY2021": "17.7%", "FY2020": "69%"}),
        ("Total Capital Ratio", {"FY2025": "16.8%", "FY2024": "18.8%", "FY2023": "19.5%", "FY2022": "18.8%", "FY2021": "19.3%", "FY2020": "69%"}),
        ("Leverage Ratio (excl. central banks)", {"FY2025": "7.3%", "FY2024": "9.4%", "FY2023": "11.4%", "FY2022": "11.3%", "FY2021": "12.5%"}),
        ("LCR", {"FY2025": "220.8%", "FY2024": "216.2%", "FY2023": "289.0%", "FY2022": "302.3%", "FY2021": "499.9%", "FY2020": "331%"}),
        ("NSFR", {"FY2025": "138.8%", "FY2024": "133.8%", "FY2023": "135.4%", "FY2022": "149.0%", "FY2021": "Not disclosed", "FY2020": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Allica is a young, fast-growing SME-lending challenger bank "
         "(authorised 2019, first loan made March 2020) — its steadily declining capital/liquidity ratios "
         "alongside rapidly rising absolute capital and RWA figures reflect fast balance-sheet growth diluting "
         "ratios from an initially very well-capitalised base, not deteriorating credit quality. The Leverage "
         "Ratio row omits FY2020 because that year's 32% figure is on a different (pre-PS21/21) exposure-measure "
         "basis to FY2021 onward — see the Leverage Ratio sheet's own note. FY2019 and FY2018 are not included "
         "anywhere in this workbook; see HISTORICAL_DEPTH_NOTE in this script for why.",
)

bw.save("/Users/armaan/code/katalysis/banks/ALLICA FINANCIALS.xlsx")
