import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2021_URL = "https://www.vanquis.com/wp-content/uploads/2025/05/Vanquis_Bank_Ltd_31_12_2021_Signed.pdf"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/02558509/filing-history/MzQxNzkzNTkxNWFkaXF6a2N4/document?format=pdf&download=0"
AR2025_URL = "https://www.vanquis.com/wp-content/uploads/2026/03/VBL-stats-2025-FINAL-Fully-Signed.pdf"

# HD-050 (2026-09-05): Companies House filing-history PDFs (scanned images,
# OCR'd via tesseract - no text layer) for the FY2014-FY2020 extension,
# capped at FY2014 project-wide even though this bank's own archive goes
# back further (HD-004 found signal to FY2010).
CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/02558509/filing-history"
AR2014_URL = f"{CH_BASE}/MzEzMzA5NjUxM2FkaXF6a2N4/document?format=pdf&download=0"
AR2015_URL = f"{CH_BASE}/MzE0NTU0NTQ4OWFkaXF6a2N4/document?format=pdf&download=0"
AR2016_URL = f"{CH_BASE}/MzE3Mjg3NDA2OGFkaXF6a2N4/document?format=pdf&download=0"
AR2017_URL = f"{CH_BASE}/MzIwMzQ0MjQ5MGFkaXF6a2N4/document?format=pdf&download=0"
AR2018_URL = f"{CH_BASE}/MzIzMTgyMDcyOGFkaXF6a2N4/document?format=pdf&download=0"
AR2019_URL = f"{CH_BASE}/MzI1OTkzNjY4M2FkaXF6a2N4/document?format=pdf&download=0"
AR2020_URL = f"{CH_BASE}/MzMxMjg4NDQzM2FkaXF6a2N4/document?format=pdf&download=0"

P3_2021_URL = "https://www.vanquis.com/wp-content/uploads/2025/05/Provident_Financial_plc_Pillar_3_Disclosures_2021.pdf"
P3_2023_URL = "https://www.vanquis.com/wp-content/uploads/2025/05/04-04-24_Pillar-3-Disclosures-2023.pdf"
P3_2024_URL = "https://www.vanquis.com/wp-content/uploads/2025/05/Vanquis_Banking_Group_plc_Pillar_3_Disclosures_2024.pdf"
P3_2025_URL = "https://www.vanquis.com/wp-content/uploads/2026/02/DEC25_VANQ_Pillar-3-Disclosure_Annual_FINAL.pdf"

# Provident Financial plc (Vanquis Bank's then-parent, renamed Vanquis Banking
# Group plc in 2021 - same continuous listed entity) Pillar 3 Disclosures,
# FY2014-FY2020 - primary site (providentfinancial.com) now redirects to
# vanquis.com with these documents unreachable live; cited via Wayback.
P3_2014_URL = "https://web.archive.org/web/20220703025345/https://www.providentfinancial.com/application/files/9516/1437/2735/2015-pillar-iii-disclosures-april-2015.pdf"
P3_2015_URL = "https://web.archive.org/web/20220703055435/https://www.providentfinancial.com/application/files/2416/1454/4505/pf-plc-2016-pillar-3-disclosures.pdf"
P3_2017_URL = "https://web.archive.org/web/20220703024108/https://www.providentfinancial.com/application/files/7916/1454/6790/pfg_pillar_3_report-2017.pdf"
P3_2018_URL = "https://web.archive.org/web/20220703030203/https://www.providentfinancial.com/application/files/4516/1454/6864/22746_pfg_pillar_3_report_2018-2.pdf"
P3_2019_URL = "https://web.archive.org/web/20220703022837/https://www.providentfinancial.com/application/files/6516/1415/8644/provident-financial-plc-pillar-3-disclosures-2019.pdf"
P3_2020_URL = "https://web.archive.org/web/20220703030607/https://www.providentfinancial.com/application/files/3716/2049/4304/Provident_Financial_plc_Pillar_3_Disclosures_2020.pdf"
# FY2016's own standalone Pillar 3 document exists in the Wayback index but
# its single capture is truncated mid-file (server confirmed: "wayback
# content truncated by length", captured 1,048,576 of 1,322,229 bytes) - a
# genuine, unrecoverable access gap, not a search failure. FY2016 Pillar 3
# figures below are sourced instead from the FY2017 Pillar 3 document's own
# FY2016 comparative column (P3_2017_URL) - self-skipped at the document
# level, not the year level, since the underlying FY2016 figures ARE
# available (just via a different document).

ENTITY_NOTE = (
    "ENTITY NOTE: Vanquis Bank Limited (company number 02558509, FRN 221156) is the PRA-authorised entity and the "
    "principal banking subsidiary of the listed Vanquis Banking Group plc (renamed from Provident Financial plc in "
    "2021 - the Bank's own name has not changed). The Cash Flow Statement sheet is on Vanquis Bank Limited's own "
    "entity-level (Company) basis. Pillar 3 disclosures, however, are published ONLY at the wider Vanquis Banking "
    "Group plc consolidated level - the Group's Pillar 3 Disclosure Policy states explicitly that disclosures 'cover "
    "the Group as a whole' with no separate Bank-only breakout (unlike some other banks in this workbook series, "
    "e.g. Clydesdale, where a dedicated Bank-level Pillar 3 appendix exists). On 31 December 2024 the Group's two "
    "principal trading entities were Vanquis Bank Limited (the Bank) and Moneybarn No.1 Limited (a non-bank vehicle "
    "finance lender) - so every Pillar 3 sheet in this workbook is on a basis that includes Moneybarn as well as the "
    "Bank, and is NOT directly comparable to the Bank-only Cash Flow Statement sheet. This is a structural limitation "
    "of what Vanquis publicly discloses, not a choice made in compiling this workbook."
)

HISTORICAL_NOTE = (
    "HISTORICAL NOTE (FY2014-FY2020, added under HD-050): sourced from Vanquis Bank Limited's own Companies House "
    "filing history (scanned Annual Report and Financial Statements PDFs, no text layer - transcribed via OCR then "
    "cross-checked against each year's own comparative column) and from Provident Financial plc's own Pillar 3 "
    "Disclosures (Provident Financial plc is the same continuous listed entity later renamed Vanquis Banking Group "
    "plc in 2021 - see entity note above). Extension capped at FY2014 project-wide per the historical-depth map's "
    "2026-09-05 decision, even though this bank's own archive goes back further (HD-004 found signal to FY2010)."
)

DISCONTINUED_NOTE = (
    "The Company sold its Personal Loans portfolio in March 2025, presented as a discontinued operation under IFRS "
    f"5 in the FY2025 Annual Report - this is the main driver of FY2025's much lower operating cash flow (£19.6m) "
    f"and investing outflow (net purchases of investment securities) versus FY2024 (Annual Report and Financial "
    f"Statements, year ended 31 December 2025, Note 2) - {AR2025_URL}."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Vanquis Bank Limited's own (Company) Statement of Cash Flows, £m:\n"
    f"FY2025 & FY2024: Vanquis Bank Limited Annual Report and Financial Statements, year ended 31 December 2025, "
    f"p.32 (Statement of Cash Flows; FY2024 restated - see Note 30) - {AR2025_URL}\n"
    f"FY2023 & FY2022: Vanquis Bank Limited Annual Report and Financial Statements, year ended 31 December 2023 "
    f"(Companies House filing, 18 Apr 2024), p.34 (Statement of Cash Flows; FY2022 reclassified between borrowings "
    f"proceeds/repayments - see note 1 on that statement) - {AR2023_URL}\n"
    f"FY2021: Vanquis Bank Limited Annual Report and Financial Statements, year ended 31 December 2021, p.59 "
    f"(Statement of Cash Flows) - {AR2021_URL}\n"
    f"FY2020 & FY2019: Annual Report and Financial Statements, year ended 31 December 2020, p.56 (Statement of "
    f"Cash Flows) - {AR2020_URL}\n"
    f"FY2018 & FY2017: Annual Report and Financial Statements, year ended 31 December 2018, p.18 (Statement of "
    f"Cash Flows) - {AR2018_URL}\n"
    f"FY2016 & FY2015: Annual Report and Financial Statements, year ended 31 December 2016, p.10 (Statement of "
    f"Cash Flows) - {AR2016_URL}\n"
    f"FY2014: Annual Report and Financial Statements, year ended 31 December 2014, p.11 (Statement of Cash "
    f"Flows) - {AR2014_URL}\n"
    "Note: presentation changed between report vintages - FY2021-FY2023 show 'Funding costs paid'/'Tax paid' as "
    "separate operating-activities lines and no loan-to-related-party financing lines; FY2024-FY2025 show 'Tax "
    "received'/no separate funding-costs line, and add 'Financing of loan to related party'/'Repayment of loan to "
    "related party' lines - each year's own as-reported presentation is preserved rather than forced into a common "
    "shape. Section totals and cash/cash equivalents figures are consistent and comparable across all 5 years "
    "(each year's opening balance matches the prior year's closing balance exactly). Note: FY2023's financing-"
    "activities line items sum to £809.2m against a printed 'Net cash generated from financing activities' total of "
    "£809.1m - an immaterial £0.1m artefact of each line being independently rounded to one decimal place in the "
    "source document itself (not a transcription error here); the printed total (£809.1m, used above) is the "
    "figure consistent with the overall net-change-in-cash reconciliation. FY2014-FY2020: 'Drawdown of loan from "
    "parent undertaking'/'Repayment of loan from parent undertaking' (FY2014-FY2017) and 'Proceeds from/repayment "
    "of borrowings' are each year's own as-reported financing-activity lines; FY2018-FY2020's own comparative "
    "columns for the immediately preceding year occasionally restate the prior year's own borrowings split (e.g. "
    "FY2018's own FY2017 comparative shows Proceeds from borrowings £455.2m/Repayment £104.1m vs FY2017's own "
    "report showing £472.5m/£121.9m) - each year's OWN as-originally-published figure is used for that year's "
    "column, per this project's usual convention, not the later restated comparative.\n\n"
    + ENTITY_NOTE + "\n\n" + DISCONTINUED_NOTE + "\n\n" + HISTORICAL_NOTE
)


def p3_sources(doc_label, doc_url, page_km1_1, page_km1_2=None):
    lines = [
        "Sources - Vanquis Banking Group plc (consolidated, includes Vanquis Bank Limited and Moneybarn No.1 "
        "Limited - see entity note on the Cash Flow Statement sheet) Pillar 3 basis:",
        f"{doc_label}: Vanquis Banking Group plc Pillar 3 Disclosures, p.{page_km1_1} - {doc_url}",
    ]
    if page_km1_2:
        lines.append(f"(liquidity metrics on p.{page_km1_2} of the same document)")
    return "\n".join(lines)


def p3_sources_pfg(doc_label, doc_url, page):
    """FY2014-FY2020 Pillar 3 sources - Provident Financial plc (same continuous
    listed entity later renamed Vanquis Banking Group plc; see HISTORICAL_NOTE)."""
    return (
        "Sources - Provident Financial plc (consolidated - see historical note on the Cash Flow Statement sheet) "
        f"Pillar 3 basis:\n{doc_label}: Provident Financial plc Pillar 3 Disclosures, p.{page} - {doc_url}"
    )


bw = BankWorkbook(bank_name="Vanquis Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="0B4F6C")

STATEMENTS_ENTITY_NOTE = (
    "Balance Sheet, Profit & Loss, Statement of Changes in Equity and Asset Quality are all on Vanquis Bank "
    "Limited's own entity-level (Company) basis, £m - the same basis as the existing Cash Flow Statement sheet "
    "(see that sheet's entity note for the wider Pillar 3 basis mismatch, which does not affect these 4 sheets)."
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: the Company's income statement structure changed materially over this period. FY2022-"
    "FY2025 show a gross 'Interest income'/'Interest expense'/'Net interest income' split; FY2021's own Annual "
    "Report instead shows a single net 'Income' line, 'Funding costs', and 'Net interest margin' (the FY2021 "
    "value used on the Net interest income row, 379.5, is that year's own Net interest margin - functionally "
    "equivalent but not a like-for-like gross split) - Interest income/expense are left blank for FY2021 as this "
    "split was not published that year. FY2021's own 'Income' (405.4) and 'Funding costs' (25.9) lines are shown "
    "on their own rows since they don't map cleanly onto later years' structure. FY2023/FY2022's income "
    "statements also disclose Exceptional items and an 'Adjusted profit before tax' as a memo add-back below the "
    "primary statement (already embedded within Operating costs, not a separate deduction) - not reproduced as "
    "its own row for consistency with FY2024/FY2025, which don't disclose that split at all. From FY2024 onward "
    "the Company splits 'continuing'/'discontinued operations' (following the March 2025 sale of the Personal "
    "Loans portfolio, presented retrospectively in FY2024's own comparative) - FY2023/FY2022/FY2021 predate this "
    "split and show one unified profit figure. 'Profit for the year' and 'Total comprehensive income for the "
    "year' are the two rows populated and exactly comparable across all 5 years."
)

bw.add_balance_sheet_sheet(
    title="Vanquis Bank Limited — Balance Sheet",
    subtitle="Vanquis Bank Limited (Company) basis, £m.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and cash equivalents", {"FY2025": 745.8, "FY2024": 945.0, "FY2023": 680.1, "FY2022": 413.0, "FY2021": 413.4, "FY2020": 833.6, "FY2019": 325.2, "FY2018": 373.6, "FY2017": 231.5, "FY2016": 172.7, "FY2015": 137.7, "FY2014": 128.4}),
        ("DATA", "Investment securities", {"FY2025": 254.6, "FY2024": 0}),
        ("DATA", "Amounts receivable from customers", {"FY2025": 2003.2, "FY2024": 1419.2, "FY2023": 1382.9, "FY2022": 1257.9, "FY2021": 1091.5, "FY2020": 1094.3, "FY2019": 1461.5, "FY2018": 1473.8, "FY2017": 1554.7, "FY2016": 1424.7, "FY2015": 1252.0, "FY2014": 1109.4}),
        ("DATA", "Trade and other receivables", {"FY2025": 121.2, "FY2024": 83.5, "FY2023": 67.4, "FY2022": 40.3, "FY2021": 30.5, "FY2020": 19.7, "FY2019": 7.8, "FY2018": 13.5, "FY2017": 12.7, "FY2016": 10.4, "FY2015": 8.2, "FY2014": 7.2}),
        ("DATA", "Loan to related party / ultimate parent undertaking", {"FY2025": 359.2, "FY2024": 379.7, "FY2023": 398.4, "FY2022": 69.3, "FY2021": 69.3, "FY2020": 69.3}),
        ("DATA", "Investments", {"FY2025": 2.4, "FY2024": 2.3, "FY2023": 5.4, "FY2022": 10.7, "FY2021": 9.1, "FY2020": 9.2, "FY2019": 16.6, "FY2018": 47.8, "FY2017": 45.8}),
        ("DATA", "Property, plant and equipment", {"FY2025": 7.2, "FY2024": 5.4, "FY2023": 4.9, "FY2022": 4.8, "FY2021": 5.0, "FY2020": 6.4, "FY2019": 6.3, "FY2018": 5.1, "FY2017": 5.7, "FY2016": 6.4, "FY2015": 5.6, "FY2014": 6.7}),
        ("DATA", "Right-of-use assets", {"FY2025": 12.1, "FY2024": 9.0, "FY2023": 10.4, "FY2022": 18.0, "FY2021": 30.6, "FY2020": 35.7, "FY2019": 40.7}),
        ("DATA", "Intangible assets", {"FY2025": 55.4, "FY2024": 49.5, "FY2023": 38.4, "FY2022": 34.5, "FY2021": 24.5, "FY2020": 14.4, "FY2019": 5.5, "FY2018": 4.4, "FY2017": 4.0, "FY2016": 1.7, "FY2015": 1.9, "FY2014": 0.5}),
        ("DATA", "Derivative financial instruments (asset)", {"FY2025": 4.4, "FY2024": 0.2, "FY2023": 1.2, "FY2022": 0}),
        ("DATA", "Current tax assets", {"FY2025": 0, "FY2024": 3.8, "FY2023": 8.3, "FY2022": 3.4, "FY2021": 1.4}),
        ("DATA", "Deferred tax assets", {"FY2025": 8.5, "FY2024": 9.8, "FY2023": 12.1, "FY2022": 15.5, "FY2021": 25.0, "FY2020": 23.8, "FY2019": 25.8, "FY2018": 40.4, "FY2017": 0.7, "FY2016": 4.8, "FY2015": 1.8, "FY2014": 3.2}),
        ("TOTAL", "Total assets", {"FY2025": 3574.0, "FY2024": 2907.4, "FY2023": 2609.5, "FY2022": 1867.4, "FY2021": 1700.3, "FY2020": 2106.4, "FY2019": 1889.4, "FY2018": 1958.6, "FY2017": 1855.1, "FY2016": 1628.7, "FY2015": 1424.7, "FY2014": 1257.3}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Trade and other payables", {"FY2025": 76.7, "FY2024": 82.6, "FY2023": 61.6, "FY2022": 175.1, "FY2021": 81.3, "FY2020": 49.8, "FY2019": 59.2, "FY2018": 72.8, "FY2017": 54.4, "FY2016": 42.2, "FY2015": 33.7, "FY2014": 29.4}),
        ("DATA", "Current tax liabilities", {"FY2025": 8.1, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 1.0, "FY2019": 34.7, "FY2018": 33.0, "FY2017": 48.4, "FY2016": 32.9, "FY2015": 21.9, "FY2014": 16.2}),
        ("DATA", "Provisions", {"FY2025": 3.0, "FY2024": 9.1, "FY2023": 2.7, "FY2022": 2.2, "FY2021": 5.3, "FY2020": 2.6, "FY2019": 11.6, "FY2018": 45.7, "FY2017": 96.7}),
        ("DATA", "Lease liabilities", {"FY2025": 21.2, "FY2024": 21.1, "FY2023": 25.3, "FY2022": 30.8, "FY2021": 37.6, "FY2020": 42.7, "FY2019": 47.6}),
        ("DATA", "Retail deposits", {"FY2025": 3019.9, "FY2024": 2428.1, "FY2023": 1950.5, "FY2022": 1100.6, "FY2021": 1018.6, "FY2020": 1683.2, "FY2019": 1345.2, "FY2018": 1431.7, "FY2017": 1291.8}),
        ("DATA", "Bank and other borrowings (pre-retail-deposit funding)", {"FY2017": 74.5, "FY2016": 1173.9, "FY2015": 1014.0, "FY2014": 927.1}),
        ("DATA", "Derivative financial instruments (liability)", {"FY2025": 7.1, "FY2024": 0.6, "FY2023": 1.0, "FY2022": 0}),
        ("DATA", "Central bank facilities", {"FY2025": 0, "FY2024": 4.2}),
        ("DATA", "Collateralised loan", {"FY2023": 174.7, "FY2022": 173.7, "FY2021": 172.2}),
        ("TOTAL", "Total liabilities", {"FY2025": 3136.0, "FY2024": 2545.7, "FY2023": 2215.8, "FY2022": 1482.4, "FY2021": 1315.0, "FY2020": 1779.3, "FY2019": 1498.3, "FY2018": 1583.2, "FY2017": 1565.8, "FY2016": 1249.0, "FY2015": 1069.6, "FY2014": 972.7}),
        ("SECTION", "Equity", {}),
        ("DATA", "Share capital", {"FY2025": 124.2, "FY2024": 124.2, "FY2023": 124.2, "FY2022": 124.2, "FY2021": 124.2, "FY2020": 124.2, "FY2019": 124.2, "FY2018": 124.2, "FY2017": 74.2, "FY2016": 74.2, "FY2015": 74.2, "FY2014": 74.2}),
        ("DATA", "Share based payment reserve", {"FY2025": 1.7, "FY2024": 1.6, "FY2023": 1.8, "FY2022": 2.3, "FY2021": 1.9, "FY2020": 2.0, "FY2019": 1.8, "FY2018": 1.8, "FY2017": 2.5, "FY2016": 6.1, "FY2015": 7.0, "FY2014": 6.0}),
        ("DATA", "Fair value / available-for-sale reserve", {"FY2020": 3.9, "FY2019": 6.7, "FY2018": 3.4, "FY2017": 1.7, "FY2016": 0.3, "FY2015": 12.7}),
        ("DATA", "Retained earnings", {"FY2025": 252.2, "FY2024": 235.9, "FY2023": 267.7, "FY2022": 258.5, "FY2021": 259.2, "FY2020": 197.0, "FY2019": 258.4, "FY2018": 246.0, "FY2017": 210.9, "FY2016": 299.1, "FY2015": 261.2, "FY2014": 204.4}),
        ("DATA", "Other equity instruments", {"FY2025": 59.9, "FY2024": 0}),
        ("TOTAL", "Total equity", {"FY2025": 438.0, "FY2024": 361.7, "FY2023": 393.7, "FY2022": 385.0, "FY2021": 385.3, "FY2020": 327.1, "FY2019": 391.1, "FY2018": 375.4, "FY2017": 289.3, "FY2016": 379.7, "FY2015": 355.1, "FY2014": 284.6}),
        ("TOTAL", "Total liabilities and equity", {"FY2025": 3574.0, "FY2024": 2907.4, "FY2023": 2609.5, "FY2022": 1867.4, "FY2021": 1700.3, "FY2020": 2106.4, "FY2019": 1889.4, "FY2018": 1958.6, "FY2017": 1855.1, "FY2016": 1628.7, "FY2015": 1424.7, "FY2014": 1257.3}),
    ],
    sources_text=(
        "Sources - Vanquis Bank Limited's own (Company) Statement of Financial Position (Balance Sheet, FY2014-"
        "FY2020; Statement of Financial Position, FY2021 onward), £m:\n"
        f"FY2025 & FY2024: Annual Report and Financial Statements, year ended 31 December 2025, p.30 - {AR2025_URL}\n"
        f"FY2023 & FY2022: Annual Report and Financial Statements, year ended 31 December 2023 (Companies House "
        f"filing, 18 Apr 2024), p.31 - {AR2023_URL}\n"
        f"FY2021: Annual Report and Financial Statements, year ended 31 December 2021, p.57 - {AR2021_URL}\n"
        f"FY2020 & FY2019: Annual Report and Financial Statements, year ended 31 December 2020, p.55 - {AR2020_URL}\n"
        f"FY2018 & FY2017: Annual Report and Financial Statements, year ended 31 December 2018, p.16 - {AR2018_URL}\n"
        f"FY2016 & FY2015: Annual Report and Financial Statements, year ended 31 December 2016, p.8 - {AR2016_URL}\n"
        f"FY2014: Annual Report and Financial Statements, year ended 31 December 2014, p.9 - {AR2014_URL}\n"
        "Note: 'Loan to related party' (FY2023-FY2025) was labelled 'Loan to ultimate parent undertaking' in "
        "FY2021-FY2022's own reports - same line, relabelled. 'Investment securities', 'Central bank facilities' "
        "and 'Other equity instruments' are new lines that only start appearing from FY2024/FY2025 (shown as 0 "
        "where the line exists that year at a nil balance, left blank where the line simply didn't exist yet). "
        "'Collateralised loan' (£172.2m-£174.7m, FY2021-FY2023) is not shown as a separate line in FY2024/FY2025's "
        "own Balance Sheet - not reproduced as a blank continuing line since it is genuinely absent from those "
        "years' own statements. Total assets = Total liabilities + Total equity exactly for all 12 years.\n\n"
        "FY2014-FY2020 additions (HD-050): 'Investments' before FY2021 is the Company's available-for-sale (FY2016-"
        "FY2017)/fair-value-through-OCI (FY2018-FY2020) investment securities holding - same balance-sheet role as "
        "the later 'Investments'/'Investment securities' lines, presentational continuity documented rather than a "
        "like-for-like restatement. 'Bank and other borrowings (pre-retail-deposit funding)' is a genuinely distinct "
        "funding line, not a renamed 'Retail deposits': Vanquis Bank funded itself through parent/wholesale "
        "borrowings until retail deposit-taking began during FY2017 (both lines appear on FY2017's own Balance "
        "Sheet simultaneously, £74.5m residual borrowings alongside £1,291.8m retail deposits); the borrowings line "
        "is genuinely absent from FY2018 onward (fully repaid - see Cash Flow Statement sheet). 'Fair value / "
        "available-for-sale reserve' is a real separate equity component from FY2015 (when the Company first held "
        "an available-for-sale investment) - FY2014's own Statement of Changes in Shareholders' Equity carries no "
        "such reserve column at all (the one immaterial FY2014 OCI item, foreign-exchange translation, was folded "
        "directly into Retained earnings that year), consistent with the equity roll-forward on the next sheet. "
        "'Provisions' (£2.6m-£96.7m, FY2017-FY2020) and 'Lease liabilities' (FY2019-FY2020, following IFRS 16 "
        "adoption - see equity roll-forward) are genuinely new lines, not renamed continuations of an earlier line. "
        "FY2017's own Balance Sheet folds a small non-current 'amounts receivable from customers' instalment-loan "
        "portion (£14.5m) into the single combined receivables figure used here, matching how FY2020 onward "
        "presents just one combined line (no current/non-current split).\n\n"
        + STATEMENTS_ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£m)",
)

bw.add_income_statement_sheet(
    title="Vanquis Bank Limited — Profit & Loss",
    subtitle="Vanquis Bank Limited (Company) basis, £m. See presentation note at bottom re: structure changes across years.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest income", {"FY2025": 460.8, "FY2024": 434.8, "FY2023": 411.4, "FY2022": 354.7}),
        ("DATA", "Interest expense", {"FY2025": -121.1, "FY2024": -105.0, "FY2023": -69.8, "FY2022": -24.5}),
        ("TOTAL", "Net interest income", {"FY2025": 339.7, "FY2024": 329.8, "FY2023": 341.6, "FY2022": 330.2, "FY2021": 379.5, "FY2020": 453.7, "FY2019": 556.0, "FY2018": 622.7, "FY2017": 607.4, "FY2016": 545.6, "FY2015": 501.3, "FY2014": 431.7}),
        ("DATA", "Income (FY2021 net presentation, pre-funding-costs)", {"FY2021": 405.4}),
        ("DATA", "Funding costs (FY2021 presentation)", {"FY2021": -25.9}),
        ("DATA", "Revenue / Income (FY2014-FY2020 presentation, gross - not split into interest/fee income)", {"FY2020": 489.2, "FY2019": 590.4, "FY2018": 658.8, "FY2017": 644.0, "FY2016": 589.4, "FY2015": 542.1, "FY2014": 471.2}),
        ("DATA", "Finance costs (FY2014-FY2020 presentation)", {"FY2020": -35.5, "FY2019": -34.4, "FY2018": -36.1, "FY2017": -36.6, "FY2016": -43.8, "FY2015": -40.8, "FY2014": -39.5}),
        ("DATA", "Fee and commission income", {"FY2025": 36.7, "FY2024": 36.8, "FY2023": 44.2, "FY2022": 47.0}),
        ("DATA", "Fee and commission expense", {"FY2025": -2.4, "FY2024": -1.7, "FY2023": -1.7, "FY2022": -2.8}),
        ("TOTAL", "Net fee and commission income", {"FY2025": 34.3, "FY2024": 35.1, "FY2023": 42.5, "FY2022": 44.2}),
        ("DATA", "Other income", {"FY2025": 0.3, "FY2024": 1.4, "FY2023": 1.3, "FY2022": 1.0}),
        ("TOTAL", "Total income", {"FY2025": 374.3, "FY2024": 366.3, "FY2023": 385.4, "FY2022": 375.4, "FY2020": 453.7, "FY2019": 556.0, "FY2018": 622.7, "FY2017": 607.4, "FY2016": 545.6, "FY2015": 501.3, "FY2014": 431.7}),
        ("SECTION", "Costs", {}),
        ("DATA", "Impairment charges", {"FY2025": -139.2, "FY2024": -124.7, "FY2023": -150.9, "FY2022": -25.3, "FY2021": -5.9, "FY2020": -239.9, "FY2019": -198.9, "FY2018": -241.6, "FY2017": -171.9, "FY2016": -162.6, "FY2015": -149.9, "FY2014": -149.1}),
        ("TOTAL", "Risk-adjusted income", {"FY2025": 235.1, "FY2024": 241.6, "FY2023": 234.5, "FY2022": 350.1, "FY2021": 373.6, "FY2020": 213.8, "FY2019": 357.1, "FY2018": 381.1, "FY2017": 435.5, "FY2016": 383.0, "FY2015": 351.4, "FY2014": 282.6}),
        ("DATA", "Operating costs", {"FY2025": -190.6, "FY2024": -236.6, "FY2023": -223.4, "FY2022": -219.7, "FY2021": -195.6, "FY2020": -171.4, "FY2019": -179.5, "FY2018": -190.4, "FY2017": -222.7, "FY2016": -175.2, "FY2015": -162.3, "FY2014": -138.9}),
        ("DATA", "Exceptional items", {"FY2020": 8.3, "FY2019": 12.4, "FY2017": -172.1, "FY2016": 20.2}),
        ("TOTAL", "Statutory profit before taxation", {"FY2025": 44.5, "FY2024": 5.0, "FY2023": 11.1, "FY2022": 130.4, "FY2021": 178.0, "FY2020": 50.7, "FY2019": 190.0, "FY2018": 190.7, "FY2017": 40.7, "FY2016": 228.0, "FY2015": 189.1, "FY2014": 143.7}),
        ("DATA", "Tax (charge)/credit", {"FY2025": -9.5, "FY2024": 1.2, "FY2023": -3.5, "FY2022": -36.6, "FY2021": -32.0, "FY2020": -8.1, "FY2019": -51.4, "FY2018": -44.8, "FY2017": -64.7, "FY2016": -60.2, "FY2015": -36.5, "FY2014": -30.3}),
        ("TOTAL", "Statutory profit after tax from continuing operations", {"FY2025": 35.0, "FY2024": 6.2}),
        ("DATA", "Profit after taxation from discontinued operations", {"FY2025": 0.7, "FY2024": 1.3}),
        ("TOTAL", "Profit for the year", {"FY2025": 35.7, "FY2024": 7.5, "FY2023": 7.6, "FY2022": 93.8, "FY2021": 146.0, "FY2020": 42.6, "FY2019": 138.6, "FY2018": 145.9, "FY2017": -24.0, "FY2016": 167.8, "FY2015": 152.6, "FY2014": 113.4}),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Fair value movements transferred to income statement", {"FY2021": -5.3}),
        ("DATA", "Fair value movements on investments / available-for-sale assets", {"FY2020": 3.8, "FY2019": 4.4, "FY2018": 2.2, "FY2017": 1.9, "FY2016": 3.1, "FY2015": 17.5}),
        ("DATA", "Gain on available-for-sale investment recycled to the income statement", {"FY2016": -20.2}),
        ("DATA", "Exchange differences on translation of foreign operations", {"FY2014": 0.1}),
        ("DATA", "Tax on items taken directly to other comprehensive income", {"FY2021": 1.4, "FY2020": -1.0, "FY2019": -1.2, "FY2018": -0.5, "FY2017": -0.5, "FY2016": 4.7, "FY2015": -3.5}),
        ("DATA", "Impact of change in UK tax rate", {"FY2020": -0.2, "FY2019": 0.1, "FY2015": -1.3}),
        ("DATA", "Deferred tax credit on disposal of investment", {"FY2020": 2.0}),
        ("DATA", "Current tax charge on disposal of investment", {"FY2020": -2.0}),
        ("TOTAL", "Other comprehensive (expense)/income for the year", {"FY2021": -3.9, "FY2020": 2.6, "FY2019": 3.3, "FY2018": 1.7, "FY2017": 1.4, "FY2016": -12.4, "FY2015": 12.7, "FY2014": 0.1}),
        ("TOTAL", "Total comprehensive income for the year", {"FY2025": 35.7, "FY2024": 7.5, "FY2023": 7.6, "FY2022": 93.8, "FY2021": 142.1, "FY2020": 45.2, "FY2019": 141.9, "FY2018": 147.6, "FY2017": -22.6, "FY2016": 155.4, "FY2015": 165.3, "FY2014": 113.5}),
    ],
    sources_text=(
        "Sources - Vanquis Bank Limited's own (Company) Income Statement, £m:\n"
        f"FY2025 & FY2024: Annual Report and Financial Statements, year ended 31 December 2025, p.29 (Income "
        f"Statement; there is no other comprehensive income for either year) - {AR2025_URL}\n"
        f"FY2023 & FY2022: Annual Report and Financial Statements, year ended 31 December 2023 (Companies House "
        f"filing, 18 Apr 2024), p.30 (Income Statement; there is no other comprehensive income for either year) - "
        f"{AR2023_URL}\n"
        f"FY2021: Annual Report and Financial Statements, year ended 31 December 2021, p.56 (Income Statement "
        f"and Statement of Comprehensive Income) - {AR2021_URL}\n"
        f"FY2020 & FY2019: Annual Report and Financial Statements, year ended 31 December 2020, p.54 (Income "
        f"Statement and Statement of Comprehensive Income) - {AR2020_URL}\n"
        f"FY2018 & FY2017: Annual Report and Financial Statements, year ended 31 December 2018, p.16 (Income "
        f"Statement and Statement of Comprehensive Income) - {AR2018_URL}\n"
        f"FY2016 & FY2015: Annual Report and Financial Statements, year ended 31 December 2016, p.8 (Income "
        f"Statement and Statement of Comprehensive Income) - {AR2016_URL}\n"
        f"FY2014: Annual Report and Financial Statements, year ended 31 December 2014, p.9 (Income Statement "
        f"and Statement of Comprehensive Income) - {AR2014_URL}\n\n"
        "FY2014-FY2020 presentation note (HD-050): none of these years split Revenue into interest/fee income - "
        "each year discloses a single blended 'Revenue' (FY2014-FY2019) or 'Income' (FY2020) line and a separate "
        "'Finance costs' line, so 'Net interest income'/'Total income' above are computed as Revenue less Finance "
        "costs (same treatment already used for FY2021's own 'Income' presentation). FY2014-FY2016's own income "
        "statements do not separately disclose Impairment charges as a line item (it is bundled inside that year's "
        "own 'Operating costs' figure alongside genuine non-credit operating expenses); the Impairment charges "
        "figure shown for those 3 years is instead the 'Charge for the year' from that year's own impairment "
        "allowance-account note (Note 11), and 'Operating costs' is the residual (that year's own disclosed Total "
        "costs, less Finance costs, less this note-sourced impairment charge) - both figures tie exactly to each "
        "year's own disclosed 'Profit before taxation'. FY2017 onward discloses Impairment charges as its own face "
        "line item directly (no derivation needed). 'Exceptional items' is a genuine separate disclosed line in "
        "FY2016 (£20.2m gain, an AFS investment recycled to the income statement), FY2017 (£172.1m loss, driving "
        "that year's near-breakeven result), and FY2019 (£12.4m gain) - blank/not applicable in FY2014, FY2015 and "
        "FY2018, which had none. FY2020's own report nets its £8.3m exceptional gain directly into the 'Administrative "
        "and operational costs' line on the face (£163.1m as printed) rather than disclosing it as a separate "
        "additive line as other years do (confirmed by the FY2020 report's own dual subtotals: 'profit before tax "
        "and exceptional items' £42.4m + exceptional items £8.3m = 'profit before tax' £50.7m) - the Operating "
        "costs row for FY2020 above is therefore shown gross of that exceptional item (£171.4m = £163.1m + £8.3m) "
        "with Exceptional items broken back out as its own row, for consistency with every other year's presentation "
        "rather than silently blending FY2020 into a different shape; this also explains why FY2020's own report's "
        "restated FY2019 comparative for that cost line (£167.1m) differs from FY2019's own originally-published "
        "figure (£179.5m, used here) by exactly FY2019's own £12.4m exceptional item. FY2018's Profit for the year "
        "(£145.9m) is that year's own originally-published figure; FY2019's own Annual Report later restated the "
        "FY2018 comparative to £150.9m/£151.7m (a change in accounting policy - direct customer-acquisition costs "
        "reclassified from an expense to a capitalised, amortised asset) - each year's own as-originally-published "
        "figure is used for that year's column, per this project's usual convention, not the later restated "
        "comparative.\n\n"
        + PRESENTATION_NOTE + "\n\n" + STATEMENTS_ENTITY_NOTE
    ),
    first_col_width=68,
    source_height=340,
    unit_suffix=" (£m)",
)

bw.add_equity_changes_sheet(
    title="Vanquis Bank Limited — Statement of Changes in Equity",
    subtitle="Vanquis Bank Limited (Company) basis, £m, chronological (oldest to newest).",
    headers=["Share capital", "Share-based payment reserve", "Fair value reserve", "Retained earnings", "Other equity instruments", "Total equity"],
    rows=[
        ("TOTAL", "At 1 January 2014 / At 31 December 2013", (74.2, 5.4, None, 131.1, None, 210.7)),
        ("DATA", "Profit for the year", (None, None, None, 113.4, None, 113.4)),
        ("DATA", "Exchange differences on translation of foreign operations", (None, None, None, 0.1, None, 0.1)),
        ("TOTAL", "Total comprehensive income for the year (FY2014)", (None, None, None, 113.5, None, 113.5)),
        ("DATA", "Share-based payment charge", (None, 2.9, None, None, None, 2.9)),
        ("DATA", "Transfer of share-based payment reserve", (None, -2.3, None, 2.3, None, 0)),
        ("DATA", "Dividends", (None, None, None, -42.5, None, -42.5)),
        ("TOTAL", "At 31 December 2014 / At 1 January 2015", (74.2, 6.0, None, 204.4, None, 284.6)),
        ("DATA", "Profit for the year", (None, None, None, 152.6, None, 152.6)),
        ("DATA", "Fair value movements on available-for-sale assets", (None, None, 17.5, None, None, 17.5)),
        ("DATA", "Tax on items taken directly to other comprehensive income", (None, None, -3.5, None, None, -3.5)),
        ("DATA", "Impact of change in UK tax rate", (None, None, -1.3, None, None, -1.3)),
        ("TOTAL", "Total comprehensive income for the year (FY2015)", (None, None, 12.7, 152.6, None, 165.3)),
        ("DATA", "Share-based payment charge", (None, 3.6, None, None, None, 3.6)),
        ("DATA", "Transfer of share-based payment reserve", (None, -2.5, None, 2.5, None, 0)),
        ("DATA", "Dividends", (None, None, None, -98.3, None, -98.3)),
        ("TOTAL", "At 31 December 2015 / At 1 January 2016", (74.2, 7.0, 12.7, 261.2, None, 355.1)),
        ("DATA", "Profit for the year", (None, None, None, 167.8, None, 167.8)),
        ("DATA", "Fair value movements on available-for-sale assets", (None, None, 3.1, None, None, 3.1)),
        ("DATA", "Gain on available-for-sale investment recycled to the income statement", (None, None, -20.2, None, None, -20.2)),
        ("DATA", "Tax on items taken directly to other comprehensive income", (None, None, 4.7, None, None, 4.7)),
        ("TOTAL", "Total comprehensive income for the year (FY2016)", (None, None, -12.4, 167.8, None, 155.4)),
        ("DATA", "Share-based payment charge", (None, 3.2, None, None, None, 3.2)),
        ("DATA", "Transfer of share-based payment reserve", (None, -4.1, None, 4.1, None, 0)),
        ("DATA", "Dividends", (None, None, None, -134.0, None, -134.0)),
        ("TOTAL", "At 31 December 2016 / At 1 January 2017", (74.2, 6.1, 0.3, 299.1, None, 379.7)),
        ("DATA", "(Loss) for the year", (None, None, None, -24.0, None, -24.0)),
        ("DATA", "Fair value movements on available-for-sale assets", (None, None, 1.9, None, None, 1.9)),
        ("DATA", "Tax on items taken directly to other comprehensive income", (None, None, -0.5, None, None, -0.5)),
        ("TOTAL", "Total comprehensive income for the year (FY2017)", (None, None, 1.4, -24.0, None, -22.6)),
        ("DATA", "Share-based payment charge", (None, -0.6, None, None, None, -0.6)),
        ("DATA", "Transfer of share-based payment reserve", (None, -3.0, None, 3.0, None, 0)),
        ("DATA", "Dividends", (None, None, None, -67.3, None, -67.3)),
        ("TOTAL", "At 31 December 2017 / At 1 January 2018", (74.2, 2.5, 1.7, 210.9, None, 289.3)),
        ("DATA", "Impact of adoption of IFRS 9 'Financial instruments'", (None, None, None, -111.4, None, -111.4)),
        ("DATA", "Profit for the year", (None, None, None, 145.9, None, 145.9)),
        ("DATA", "Fair value movements on investments", (None, None, 2.2, None, None, 2.2)),
        ("DATA", "Tax on items taken directly to other comprehensive income", (None, None, -0.5, None, None, -0.5)),
        ("TOTAL", "Total comprehensive income for the year (FY2018)", (None, None, 1.7, 145.9, None, 147.6)),
        ("DATA", "Issue of share capital", (50.0, None, None, None, None, 50.0)),
        ("DATA", "Transfer of share-based payment reserve", (None, -0.7, None, 0.7, None, 0)),
        ("TOTAL", "At 31 December 2018 (as originally reported in FY2018's own accounts)", (124.2, 1.8, 3.4, 246.0, None, 375.4)),
        ("DATA", "Restatement of FY2018 comparative in FY2019's own accounts (prior year adjustment for directly attributable acquisition costs, net of other basis differences)", (None, None, None, 16.0, None, 16.0)),
        ("TOTAL", "At 1 January 2019 (per FY2019's own restated comparative)", (124.2, 1.8, 3.4, 262.0, None, 391.4)),
        ("DATA", "Impact of adoption of IFRS 16 'Leases'", (None, None, None, -2.6, None, -2.6)),
        ("DATA", "Profit for the year", (None, None, None, 138.6, None, 138.6)),
        ("DATA", "Fair value movements on investments", (None, None, 4.4, None, None, 4.4)),
        ("DATA", "Tax on items taken directly to other comprehensive income", (None, None, -1.1, None, None, -1.1)),
        ("TOTAL", "Total comprehensive income for the year (FY2019)", (None, None, 3.3, 138.6, None, 141.9)),
        ("DATA", "Share-based payment charge", (None, 0.2, None, None, None, 0.2)),
        ("DATA", "Transfer of share-based payment reserve", (None, -0.2, None, 0.2, None, 0)),
        ("DATA", "Dividends", (None, None, None, -139.8, None, -139.8)),
        ("TOTAL", "At 31 December 2019 / At 1 January 2020", (124.2, 1.8, 6.7, 258.4, None, 391.1)),
        ("DATA", "Profit for the year", (None, None, None, 42.6, None, 42.6)),
        ("DATA", "Fair value movements on investments", (None, None, 3.8, None, None, 3.8)),
        ("DATA", "Tax on items taken directly to other comprehensive income", (None, None, -1.2, None, None, -1.2)),
        ("TOTAL", "Total comprehensive income for the year (FY2020)", (None, None, 2.6, 42.6, None, 45.2)),
        ("DATA", "Share-based payment charge", (None, 0.8, None, None, None, 0.8)),
        ("DATA", "Transfer of cumulative gain on disposal of investment", (None, None, -7.4, 7.4, None, 0)),
        ("DATA", "Transfer of tax on disposal of investment", (None, None, 2.0, -2.0, None, 0)),
        ("DATA", "Transfer of share-based payment reserve", (None, -0.6, None, 0.6, None, 0)),
        ("DATA", "Dividends", (None, None, None, -110.0, None, -110.0)),
        ("TOTAL", "At 31 December 2020 / At 1 January 2021", (124.2, 2.0, 3.9, 197.0, None, 327.1)),
        ("DATA", "Profit for the year", (None, None, None, 146.0, None, 146.0)),
        ("DATA", "Fair value movements transferred to income statement", (None, None, -5.3, None, None, -5.3)),
        ("DATA", "Tax on items taken directly to other comprehensive income", (None, None, 1.4, None, None, 1.4)),
        ("TOTAL", "Total comprehensive income for the year (FY2021)", (None, None, -3.9, 146.0, None, 142.1)),
        ("DATA", "Share-based payment charge", (None, 1.1, None, None, None, 1.1)),
        ("DATA", "Transfer of share-based payment reserve", (None, -1.2, None, 1.2, None, 0)),
        ("DATA", "Dividends", (None, None, None, -85.0, None, -85.0)),
        ("TOTAL", "At 31 December 2021 / At 1 January 2022", (124.2, 1.9, 0, 259.2, None, 385.3)),
        ("DATA", "Profit for the year", (None, None, None, 93.8, None, 93.8)),
        ("TOTAL", "Total comprehensive income for the year (FY2022)", (None, None, None, 93.8, None, 93.8)),
        ("DATA", "Share-based payment charge", (None, 1.0, None, None, None, 1.0)),
        ("DATA", "Transfer of share-based payment reserve", (None, -0.6, None, 0.6, None, 0)),
        ("DATA", "Dividends", (None, None, None, -95.1, None, -95.1)),
        ("TOTAL", "At 31 December 2022 / At 1 January 2023", (124.2, 2.3, None, 258.5, None, 385.0)),
        ("DATA", "Profit for the year", (None, None, None, 7.6, None, 7.6)),
        ("TOTAL", "Total comprehensive income for the year (FY2023)", (None, None, None, 7.6, None, 7.6)),
        ("DATA", "Share-based payment charge", (None, 1.1, None, None, None, 1.1)),
        ("DATA", "Transfer of share-based payment reserve", (None, -1.6, None, 1.6, None, 0)),
        ("TOTAL", "At 31 December 2023 / At 1 January 2024", (124.2, 1.8, None, 267.7, None, 393.7)),
        ("DATA", "Profit for the year", (None, None, None, 7.5, None, 7.5)),
        ("TOTAL", "Total comprehensive income for the year (FY2024)", (None, None, None, 7.5, None, 7.5)),
        ("DATA", "Share-based payment charge", (None, 0.5, None, None, None, 0.5)),
        ("DATA", "Transfer of share-based payment reserve", (None, -0.7, None, 0.7, None, 0)),
        ("DATA", "Dividends", (None, None, None, -40.0, None, -40.0)),
        ("TOTAL", "At 31 December 2024 / At 1 January 2025", (124.2, 1.6, None, 235.9, None, 361.7)),
        ("DATA", "Profit for the year", (None, None, None, 35.7, None, 35.7)),
        ("TOTAL", "Total comprehensive income for the year (FY2025)", (None, None, None, 35.7, None, 35.7)),
        ("DATA", "Share-based payment charge", (None, 0.7, None, None, None, 0.7)),
        ("DATA", "Transfer of share-based payment reserve", (None, -0.6, None, 0.6, None, 0)),
        ("DATA", "Issuance of other equity instruments", (None, None, None, None, 59.9, 59.9)),
        ("DATA", "Dividends", (None, None, None, -20.0, None, -20.0)),
        ("TOTAL", "At 31 December 2025", (124.2, 1.7, None, 252.2, 59.9, 438.0)),
    ],
    sources_text=(
        "Sources - Vanquis Bank Limited's own (Company) Statement of Changes in Shareholder's Equity, £m:\n"
        f"FY2021 opening & FY2021 movements: Annual Report and Financial Statements, year ended 31 December "
        f"2021, p.58 - {AR2021_URL}\n"
        f"FY2022 & FY2023 movements: Annual Report and Financial Statements, year ended 31 December 2023 "
        f"(Companies House filing, 18 Apr 2024), p.32 - {AR2023_URL}\n"
        f"FY2024 & FY2025 movements: Annual Report and Financial Statements, year ended 31 December 2025, p.31 - "
        f"{AR2025_URL}\n"
        "Note: the Fair value reserve fully unwound during FY2021 (£3.9m to £0.0m) and does not appear as a "
        "column in any later report - shown as None (not applicable) from FY2022 onward rather than a fabricated "
        "zero row. 'Other equity instruments' (£59.9m AT1 issuance) is unique to FY2025. Zero undocumented plug "
        "rows: every movement category is individually sourced (including easy-to-skip items - the FY2021 fair "
        "value/tax-on-OCI movements and the FY2025 AT1 issuance) and each closing balance ties exactly to both "
        "the next period's opening balance and to that year's own Balance Sheet Total equity.\n\n"
        + STATEMENTS_ENTITY_NOTE
    ),
    source_height=220,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Cash (used in)/generated from operations", {"FY2025": 15.5, "FY2024": 460.8, "FY2023": -494.1, "FY2022": 75.2, "FY2021": 212.9, "FY2020": 354.9, "FY2019": 210.5, "FY2018": 100.9, "FY2017": 58.2, "FY2016": 91.1, "FY2015": 97.3, "FY2014": -46.4}),
    ("DATA", "Funding costs paid", {"FY2023": -33.8, "FY2022": -10.9, "FY2021": -25.9, "FY2020": -35.5, "FY2019": -34.0, "FY2018": -36.1, "FY2017": -36.4, "FY2016": -43.4, "FY2015": -43.2, "FY2014": -40.4}),
    ("DATA", "Tax paid", {"FY2023": -6.1, "FY2022": -13.4, "FY2021": -6.1, "FY2020": -25.5, "FY2019": -22.5, "FY2018": -25.4, "FY2017": -45.7, "FY2016": -47.5, "FY2015": -30.1, "FY2014": -28.0}),
    ("DATA", "Tax received", {"FY2025": 4.1, "FY2024": 8.2}),
    ("TOTAL", "Net cash (used in)/generated from operating activities", {"FY2025": 19.6, "FY2024": 469.0, "FY2023": -534.0, "FY2022": 50.9, "FY2021": 180.9, "FY2020": 293.9, "FY2019": 154.0, "FY2018": 39.4, "FY2017": -23.9, "FY2016": 0.2, "FY2015": 24.0, "FY2014": -114.8}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property and equipment", {"FY2025": -1.4, "FY2024": -1.2, "FY2023": -1.9, "FY2022": -2.5, "FY2021": -0.7, "FY2020": -5.0, "FY2019": -2.7, "FY2018": -0.6, "FY2017": -1.3, "FY2016": -2.4, "FY2015": -1.2, "FY2014": -5.6}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -14.6, "FY2024": -11.6, "FY2023": -12.5, "FY2022": -19.2, "FY2021": -16.9, "FY2020": -14.1, "FY2019": -4.4, "FY2018": -3.1, "FY2017": -5.2, "FY2016": -0.9, "FY2015": -2.1, "FY2014": -0.5}),
    ("DATA", "Purchase of investment securities", {"FY2025": -291.8, "FY2018": -36.4, "FY2017": -35.9}),
    ("DATA", "Proceeds from maturity of investment securities", {"FY2025": 40.0}),
    ("DATA", "Proceeds from sale of investments", {"FY2024": 4.3, "FY2023": 6.4, "FY2019": 35.8, "FY2018": 36.7}),
    ("DATA", "Proceeds from disposal of available-for-sale investment", {"FY2020": 7.4, "FY2016": 12.2}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -267.8, "FY2024": -8.5, "FY2023": -8.0, "FY2022": -21.7, "FY2021": -17.6, "FY2020": -11.7, "FY2019": 28.7, "FY2018": -3.4, "FY2017": -42.4, "FY2016": 8.9, "FY2015": -3.3, "FY2014": -6.1}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payment/capital elements of lease liabilities", {"FY2025": -6.8, "FY2024": -5.5, "FY2023": -6.0, "FY2022": -6.1, "FY2021": -6.1, "FY2020": -6.0, "FY2019": -4.8}),
    ("DATA", "Financing of loan to related party", {"FY2025": -163.0, "FY2024": -140.0}),
    ("DATA", "Repayment of loan to related party", {"FY2025": 183.9, "FY2024": 158.9}),
    ("DATA", "Drawdown of loan from parent", {"FY2014": 54.7}),
    ("DATA", "Repayment of loan from parent", {"FY2018": -74.5, "FY2017": -158.2, "FY2016": -50.3, "FY2015": -63.8}),
    ("DATA", "Proceeds from issue of share capital", {"FY2018": 50.0}),
    ("DATA", "Proceeds from borrowings", {"FY2024": 5.0, "FY2023": 1100.0, "FY2022": 330.0, "FY2021": 295.8, "FY2020": 680.8, "FY2019": 125.1, "FY2018": 352.2, "FY2017": 472.5, "FY2016": 331.8, "FY2015": 239.1, "FY2014": 217.3}),
    ("DATA", "Repayment of borrowings", {"FY2025": -5.0, "FY2024": -174.0, "FY2023": -284.8, "FY2022": -258.4, "FY2021": -788.2, "FY2020": -338.6, "FY2019": -211.6, "FY2018": -221.6, "FY2017": -121.9, "FY2016": -121.6, "FY2015": -88.4, "FY2014": -72.1}),
    ("DATA", "Proceeds of issuance of other equity instruments", {"FY2025": 59.9}),
    ("DATA", "Dividends paid to company shareholder", {"FY2025": -20.0, "FY2024": -40.0, "FY2022": -95.1, "FY2021": -85.0, "FY2020": -110.0, "FY2019": -139.8, "FY2017": -67.3, "FY2016": -134.0, "FY2015": -98.3, "FY2014": -42.5}),
    ("TOTAL", "Net cash generated/(used in) financing activities", {"FY2025": 49.0, "FY2024": -195.6, "FY2023": 809.1, "FY2022": -29.6, "FY2021": -583.5, "FY2020": 226.2, "FY2019": -231.1, "FY2018": 106.1, "FY2017": 125.1, "FY2016": 25.9, "FY2015": -11.4, "FY2014": 157.4}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -199.2, "FY2024": 264.9, "FY2023": 267.1, "FY2022": -0.4, "FY2021": -420.2, "FY2020": 508.4, "FY2019": -48.4, "FY2018": 142.1, "FY2017": 58.8, "FY2016": 35.0, "FY2015": 9.3, "FY2014": 36.5}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 945.0, "FY2024": 680.1, "FY2023": 413.0, "FY2022": 413.4, "FY2021": 833.6, "FY2020": 325.2, "FY2019": 373.6, "FY2018": 231.5, "FY2017": 172.7, "FY2016": 137.7, "FY2015": 128.4, "FY2014": 91.9}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 745.8, "FY2024": 945.0, "FY2023": 680.1, "FY2022": 413.0, "FY2021": 413.4, "FY2020": 833.6, "FY2019": 325.2, "FY2018": 373.6, "FY2017": 231.5, "FY2016": 172.7, "FY2015": 137.7, "FY2014": 128.4}),
]

bw.add_cash_flow_sheet(
    title="Vanquis Bank Limited — Cash Flow Statement",
    subtitle="Vanquis Bank Limited (Company) basis, £m. See source note at bottom re: basis mismatch with Pillar 3 sheets.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=260,
    unit_suffix=" (£m)",
)

bw.add_asset_quality_sheet(
    title="Vanquis Bank Limited — Asset Quality",
    subtitle="Vanquis Bank Limited (Company) basis, £m. IFRS 9 stage split shown on Credit Cards (largest, most consistently disclosed product) except FY2021 (whole book).",
    rows=[
        ("SECTION", "Gross receivables by product", {}),
        ("DATA", "Credit Cards (gross)", {"FY2025": 1553.8, "FY2024": 1309.9, "FY2023": 1476.4, "FY2022": 1452.0}),
        ("DATA", "Personal Loans (gross)", {"FY2023": 117.5, "FY2022": 85.5}),
        ("DATA", "Second Charge Mortgages (gross)", {"FY2025": 619.4, "FY2024": 225.5, "FY2023": 2.8}),
        ("DATA", "Whole book (gross, FY2021 - not split by product that year)", {"FY2021": 1451.0, "FY2020": 1568.5, "FY2019": 1903.1, "FY2018": 1976.5, "FY2017": 1843.6, "FY2016": 1686.1, "FY2015": 1476.5, "FY2014": 1288.0}),
        ("TOTAL", "Gross amounts receivable from customers (continuing operations)", {"FY2025": 2173.2, "FY2024": 1535.4, "FY2023": 1596.7, "FY2022": 1537.5, "FY2021": 1451.0, "FY2020": 1568.5, "FY2019": 1903.1, "FY2018": 1976.5, "FY2017": 1843.6, "FY2016": 1686.1, "FY2015": 1476.5, "FY2014": 1288.0}),
        ("SECTION", "Allowance account by product", {}),
        ("DATA", "Credit Cards allowance", {"FY2025": -169.5, "FY2024": -160.0, "FY2023": -198.7, "FY2022": -270.4}),
        ("DATA", "Personal Loans allowance", {"FY2023": -15.1, "FY2022": -9.2}),
        ("DATA", "Second Charge Mortgages allowance", {"FY2025": -0.9, "FY2024": -0.2}),
        ("DATA", "Whole book allowance (FY2021 - not split by product that year)", {"FY2021": -359.5, "FY2020": -474.2, "FY2019": -441.6, "FY2018": -502.7, "FY2017": -288.9, "FY2016": -261.4, "FY2015": -224.5, "FY2014": -178.6}),
        ("TOTAL", "Allowance account (continuing operations)", {"FY2025": -170.4, "FY2024": -160.2, "FY2023": -213.8, "FY2022": -279.6, "FY2021": -359.5, "FY2020": -474.2, "FY2019": -441.6, "FY2018": -502.7, "FY2017": -288.9, "FY2016": -261.4, "FY2015": -224.5, "FY2014": -178.6}),
        ("TOTAL", "Net amounts receivable from customers (continuing operations)", {"FY2025": 2002.8, "FY2024": 1375.2, "FY2023": 1382.9, "FY2022": 1257.9, "FY2021": 1091.5, "FY2020": 1094.3, "FY2019": 1461.5, "FY2018": 1473.8, "FY2017": 1554.7, "FY2016": 1424.7, "FY2015": 1252.0, "FY2014": 1109.4}),
        ("DATA", "Fair value adjustment for portfolio hedged risk (Second Charge Mortgages)", {"FY2025": 0.4}),
        ("DATA", "Discontinued operations (Personal Loans, sold March 2025)", {"FY2024": 44.0}),
        ("TOTAL", "Reported amounts receivable from customers (per Balance Sheet)", {"FY2025": 2003.2, "FY2024": 1419.2, "FY2023": 1382.9, "FY2022": 1257.9, "FY2021": 1091.5, "FY2020": 1094.3, "FY2019": 1461.5, "FY2018": 1473.8, "FY2017": 1554.7, "FY2016": 1424.7, "FY2015": 1252.0, "FY2014": 1109.4}),
        ("SECTION", "Credit quality by IFRS 9 stage (FY2018 onward only - IFRS 9 adopted 1 Jan 2018)", {}),
        ("DATA", "Stage 1 (gross)", {"FY2025": 1351.5, "FY2024": 1136.6, "FY2023": 1200.8, "FY2022": 1116.6, "FY2021": 913.7, "FY2020": 1044.5, "FY2019": 1368.0, "FY2018": 1288.4}),
        ("DATA", "Stage 2 (gross)", {"FY2025": 139.1, "FY2024": 99.8, "FY2023": 161.4, "FY2022": 148.7, "FY2021": 342.8, "FY2020": 188.4, "FY2019": 171.5, "FY2018": 172.8}),
        ("DATA", "Stage 3 / non-performing (gross)", {"FY2025": 63.2, "FY2024": 73.5, "FY2023": 114.2, "FY2022": 186.7, "FY2021": 194.5, "FY2020": 335.6, "FY2019": 363.6, "FY2018": 515.3}),
        ("TOTAL", "Total gross (Credit Cards; FY2021 whole book)", {"FY2025": 1553.8, "FY2024": 1309.9, "FY2023": 1476.4, "FY2022": 1452.0, "FY2021": 1451.0, "FY2020": 1568.5, "FY2019": 1903.1, "FY2018": 1976.5}),
        ("DATA", "Stage 3 as % of gross - NPL ratio (derived)", {"FY2025": "4.07%", "FY2024": "5.61%", "FY2023": "7.74%", "FY2022": "12.86%", "FY2021": "13.40%", "FY2020": "21.40%", "FY2019": "19.11%", "FY2018": "26.07%"}),
        ("DATA", "Coverage ratio - allowance / gross (derived)", {"FY2025": "10.91%", "FY2024": "12.21%", "FY2023": "13.46%", "FY2022": "18.62%", "FY2021": "24.78%", "FY2020": "30.23%", "FY2019": "23.20%", "FY2018": "25.43%", "FY2017": "15.67%", "FY2016": "15.50%", "FY2015": "15.21%", "FY2014": "13.87%"}),
        ("SECTION", "Credit quality, IAS 39 basis (FY2014-FY2017, pre-IFRS 9 - not stage-split; net carrying value)", {}),
        ("DATA", "Neither past due nor impaired (net carrying value, IAS 39 basis)", {"FY2017": 1456.3, "FY2016": 1338.8, "FY2015": 1168.5, "FY2014": 1016.5}),
        ("DATA", "Impaired (net carrying value, IAS 39 basis)", {"FY2017": 98.4, "FY2016": 85.9, "FY2015": 83.5, "FY2014": 92.9}),
        ("DATA", "Impaired as % of total net receivables - NPL ratio, net basis (derived; not comparable with the gross-basis ratio used FY2018 onward)", {"FY2017": "6.33%", "FY2016": "6.03%", "FY2015": "6.67%", "FY2014": "8.38%"}),
    ],
    sources_text=(
        "Sources - Vanquis Bank Limited's own (Company) Note 'Amounts receivable from customers', £m:\n"
        f"FY2025 & FY2024: Annual Report and Financial Statements, year ended 31 December 2025, note 12, p.56-60 "
        f"- {AR2025_URL}\n"
        f"FY2023 & FY2022: Annual Report and Financial Statements, year ended 31 December 2023 (Companies House "
        f"filing, 18 Apr 2024), note 11, p.53-58 - {AR2023_URL}\n"
        f"FY2021: Annual Report and Financial Statements, year ended 31 December 2021, note 10, p.79-80 - "
        f"{AR2021_URL}\n"
        f"FY2020 & FY2019: Annual Report and Financial Statements, year ended 31 December 2020 (Companies House "
        f"filing), amounts receivable from customers note - {AR2020_URL}\n"
        f"FY2018 & FY2017: Annual Report and Financial Statements, year ended 31 December 2018 (Companies House "
        f"filing), amounts receivable from customers note (includes FY2018's own IFRS 9 stage split and FY2017's "
        f"IAS 39 comparative) - {AR2018_URL}\n"
        f"FY2016 & FY2015: Annual Report and Financial Statements, year ended 31 December 2016 (Companies House "
        f"filing), amounts receivable from customers note - {AR2016_URL}\n"
        f"FY2014: Annual Report and Financial Statements, year ended 31 December 2014 (Companies House filing), "
        f"amounts receivable from customers note - {AR2014_URL}\n"
        "Note: FY2021's own note discloses only a combined (whole-book) gross/allowance/stage split, not broken "
        "out by product - Credit Cards/Personal Loans product-level figures only start from FY2022's report. "
        "Personal Loans was sold in March 2025 (presented as a discontinued operation in the FY2025 Annual "
        "Report) and is not stage-split in FY2024/FY2025's own disclosures (shown only as a lump-sum discontinued "
        "figure). The IFRS 9 stage split shown here is Credit Cards only for FY2022-FY2025 (the largest, most "
        "consistently disclosed product across all years) rather than the whole book - NOT a like-for-like basis "
        "with FY2021's whole-book split, documented rather than blended. NPL and coverage ratios are derived here "
        "(Stage 3 gross / Total gross; Allowance / Total gross) - not printed as ratios in the source documents.\n\n"
        "FY2014-FY2020 (this build's historical-depth extension, capped at FY2014 per project decision): the "
        "whole book was never split by product in Vanquis Bank Limited's own disclosures before FY2022, so all of "
        "FY2014-FY2020 sit on the 'Whole book' rows, consistent with FY2021's own treatment. IFRS 9 was adopted "
        "1 January 2018 (no restatement of FY2017 or earlier) - FY2018/FY2019/FY2020 carry a real Stage 1/2/3 "
        "gross split from the Company's own note; FY2014-FY2017 instead use the IAS 39-basis 'neither past due "
        "nor impaired' / 'impaired' net-carrying-value split their own notes disclosed pre-IFRS 9. The FY2014-"
        "FY2017 NPL ratio is therefore computed on a NET basis (impaired net / total net receivables) and is NOT "
        "comparable with the gross-basis Stage 3 ratio used from FY2018 onward - shown as a separate row rather "
        "than blended into one series. The coverage ratio (allowance / gross) uses a consistent definition across "
        "every year FY2014-FY2025 and is directly comparable throughout.\n\n"
        + STATEMENTS_ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=240,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Vanquis Banking Group consolidated basis, {unit}" if unit else "Vanquis Banking Group consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=120)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 341.3, "FY2024": 344.3, "FY2023": 409.0, "FY2022": 478.8, "FY2021": 506.5, "FY2020": 674.8, "FY2019": 697.2, "FY2018": 621.9, "FY2017": 308.1, "FY2016": 454.6, "FY2015": 386.0, "FY2014": 330.0})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22 (Appendix 1 - Own funds disclosures)", P3_2021_URL, "28") + "\n"
    + p3_sources_pfg("FY2020: Pillar 3 Disclosures 2020", P3_2020_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2019: Pillar 3 Disclosures 2019", P3_2019_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2018: Pillar 3 Disclosures 2018", P3_2018_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2017: Pillar 3 Disclosures 2017", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2016 (sourced from FY2017's own comparative column - FY2016's own document is truncated in the Wayback archive, see HISTORICAL_NOTE)", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2015: Pillar 3 Disclosures 2015", P3_2015_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2014: Pillar 3 Disclosures 2014", P3_2014_URL, "n/a"),
    note="FY2014-FY2020: Provident Financial plc (Vanquis Bank's then-parent, the same continuous listed entity "
         "later renamed Vanquis Banking Group plc in 2021) had no Additional Tier 1 or Tier 2 capital in any of "
         "these years - CET1 = Tier 1 = Total capital exactly, unlike FY2021 onward which does carry Tier 2 "
         "capital. " + HISTORICAL_NOTE,
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "16.5%", "FY2024": "18.8%", "FY2023": "20.5%", "FY2022": "26.4%", "FY2021": "29.1%", "FY2020": "34.2%", "FY2019": "31.1%", "FY2018": "28.2%", "FY2017": "14.5%", "FY2016": "21.7%", "FY2015": "21.5%", "FY2014": "20.0%"})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28") + "\n"
    + p3_sources_pfg("FY2020: Pillar 3 Disclosures 2020", P3_2020_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2019: Pillar 3 Disclosures 2019", P3_2019_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2018: Pillar 3 Disclosures 2018 (verified/transitional basis; a 'fully loaded' alternate of 20.7% and an 'accrued basis' alternate of 29.7% are also disclosed)", P3_2018_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2017: Pillar 3 Disclosures 2017", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2016 (sourced from FY2017's own comparative column)", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2015: Pillar 3 Disclosures 2015", P3_2015_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2014: Pillar 3 Disclosures 2014", P3_2014_URL, "n/a"),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 400.0, "FY2024": 344.3, "FY2023": 409.0, "FY2022": 478.8, "FY2021": 506.5, "FY2020": 674.8, "FY2019": 697.2, "FY2018": 621.9, "FY2017": 308.1, "FY2016": 454.6, "FY2015": 386.0, "FY2014": 330.0})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28") + "\n"
    + p3_sources_pfg("FY2020: Pillar 3 Disclosures 2020", P3_2020_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2019: Pillar 3 Disclosures 2019", P3_2019_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2018: Pillar 3 Disclosures 2018", P3_2018_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2017: Pillar 3 Disclosures 2017", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2016 (sourced from FY2017's own comparative column)", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2015: Pillar 3 Disclosures 2015", P3_2015_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2014: Pillar 3 Disclosures 2014", P3_2014_URL, "n/a"),
    note="FY2025 is the first year Tier 1 capital exceeds CET1 - the Group issued £59.9m of other (AT1) equity "
         "instruments during 2025 (see Cash Flow Statement sheet, financing activities). All other years shown, "
         "including all of FY2014-FY2020, have no Additional Tier 1 capital, so Tier 1 = CET1 exactly.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "19.3%", "FY2024": "18.8%", "FY2023": "20.5%", "FY2022": "26.4%", "FY2021": "29.1%", "FY2020": "34.2%", "FY2019": "31.1%", "FY2018": "28.2%", "FY2017": "14.5%", "FY2016": "21.7%", "FY2015": "21.5%", "FY2014": "20.0%"})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28") + "\n"
    + p3_sources_pfg("FY2020: Pillar 3 Disclosures 2020", P3_2020_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2019: Pillar 3 Disclosures 2019", P3_2019_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2018: Pillar 3 Disclosures 2018", P3_2018_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2017: Pillar 3 Disclosures 2017", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2016 (sourced from FY2017's own comparative column)", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2015: Pillar 3 Disclosures 2015", P3_2015_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2014: Pillar 3 Disclosures 2014", P3_2014_URL, "n/a"),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 541.5, "FY2024": 544.3, "FY2023": 609.0, "FY2022": 678.8, "FY2021": 706.5, "FY2020": 674.8, "FY2019": 697.2, "FY2018": 621.9, "FY2017": 308.1, "FY2016": 454.6, "FY2015": 386.0, "FY2014": 330.0})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28") + "\n"
    + p3_sources_pfg("FY2020: Pillar 3 Disclosures 2020", P3_2020_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2019: Pillar 3 Disclosures 2019", P3_2019_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2018: Pillar 3 Disclosures 2018", P3_2018_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2017: Pillar 3 Disclosures 2017", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2016 (sourced from FY2017's own comparative column)", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2015: Pillar 3 Disclosures 2015", P3_2015_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2014: Pillar 3 Disclosures 2014", P3_2014_URL, "n/a"),
    note="DATA QUALITY NOTE: the FY2024 Pillar 3 Disclosures document's own comparative column for 31 Dec 2023 "
         "prints a 'Total capital' amount (£393.4m) that is inconsistent with that same document's own 31 Dec 2023 "
         "Total capital RATIO (30.0%) and RWA (£1,975.6m) - 30.0% x 1,975.6 implies Total capital of ~£592.7m, not "
         "£393.4m (and £393.4m simply repeats that column's CET1 figure, i.e. as if Tier 2 capital were zero, which "
         "contradicts row UK 7c showing a non-zero Additional T2 SREP requirement). The figures used here for FY2023 "
         "instead come from the FY2023 Pillar 3 Disclosures document's OWN as-originally-reported 31 Dec 2023 "
         "column (£609.0m), which is internally consistent (609.0 / 1,990.6 = 30.6%, matching its own stated ratio "
         "exactly) - this is also why FY2023's RWA here (£1,990.6m) differs slightly from the restated £1,975.6m "
         "shown as a comparative in the FY2024 document (a legitimate restatement, per that document's own footnote, "
         "for a Vehicle Finance Stage 3 ECL review - unrelated to the Total capital error). Separately: FY2014-"
         "FY2020 all have zero Additional Tier 1/Tier 2 capital, so Total capital = CET1 = Tier 1 exactly in those "
         "years - a genuinely different capital structure from FY2021 onward, not a data gap.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "26.1%", "FY2024": "29.7%", "FY2023": "30.6%", "FY2022": "37.5%", "FY2021": "40.6%", "FY2020": "34.2%", "FY2019": "31.1%", "FY2018": "28.2%", "FY2017": "14.5%", "FY2016": "21.7%", "FY2015": "21.5%", "FY2014": "20.0%"})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28") + "\n"
    + p3_sources_pfg("FY2020: Pillar 3 Disclosures 2020", P3_2020_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2019: Pillar 3 Disclosures 2019", P3_2019_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2018: Pillar 3 Disclosures 2018", P3_2018_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2017: Pillar 3 Disclosures 2017", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2016 (sourced from FY2017's own comparative column)", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2015: Pillar 3 Disclosures 2015", P3_2015_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2014: Pillar 3 Disclosures 2014", P3_2014_URL, "n/a"),
    note="See the Total Capital sheet's DATA QUALITY NOTE - this ratio row is unaffected (it is directly stated in "
         "each document, not derived from the erroneous amount), but is included here for context.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 2073.2, "FY2024": 1834.8, "FY2023": 1990.6, "FY2022": 1810.8, "FY2021": 1740.6, "FY2020": 1973.5, "FY2019": 2244.3, "FY2018": 2209.2, "FY2017": 2118.0, "FY2016": 2091.8, "FY2015": 1796.0, "FY2014": 1649.3})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28") + "\n"
    + p3_sources_pfg("FY2020: Pillar 3 Disclosures 2020", P3_2020_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2019: Pillar 3 Disclosures 2019", P3_2019_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2018: Pillar 3 Disclosures 2018", P3_2018_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2017: Pillar 3 Disclosures 2017", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2016 (sourced from FY2017's own comparative column)", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2015: Pillar 3 Disclosures 2015", P3_2015_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2014: Pillar 3 Disclosures 2014", P3_2014_URL, "n/a"),
    note="FY2023 (£1,990.6m) is as originally reported in the FY2023 Pillar 3 Disclosures; the FY2024 document later "
         "restated the 31 Dec 2023 comparative to £1,975.6m following a Vehicle Finance Stage 3 ECL methodology "
         "review - both figures are genuine, just on slightly different bases (see Total Capital sheet note).",
)

bw.add_rwa_breakdown_sheet(
    title="Vanquis Bank Limited — RWA Breakdown",
    subtitle="Vanquis Banking Group plc consolidated basis, £m (see entity note - same basis mismatch as the other Pillar 3 sheets).",
    rows=[
        ("DATA", "Credit risk (excluding CCR)", {"FY2025": 1931.5, "FY2024": 1696.8, "FY2023": 1848.8, "FY2022": 1656.5, "FY2021": 1595.0, "FY2020": 1793.1, "FY2019": 2057.6, "FY2018": 2023.9, "FY2017": 1946.7, "FY2016": 1933.7, "FY2015": 1661.7, "FY2014": 1523.6}),
        ("DATA", "Counterparty credit risk (CCR, incl. CVA)", {"FY2025": 3.0, "FY2024": 3.8, "FY2023": 10.6, "FY2022": 23.0, "FY2021": 4.1, "FY2016": 0.1, "FY2015": 0.1, "FY2014": 0.7}),
        ("DATA", "Securitisation exposures", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
        ("DATA", "Market risk", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 21.1, "FY2019": 16.6, "FY2018": 14.0, "FY2017": 9.9, "FY2016": 9.7, "FY2015": 0, "FY2014": 0}),
        ("DATA", "Operational risk", {"FY2025": 138.7, "FY2024": 134.2, "FY2023": 131.2, "FY2022": 131.3, "FY2021": 141.5, "FY2020": 159.3, "FY2019": 170.1, "FY2018": 171.3, "FY2017": 161.4, "FY2016": 148.3, "FY2015": 134.2, "FY2014": 125.0}),
        ("DATA", "Amounts below thresholds for deduction (memo, not summed into Total)", {"FY2025": 40.2, "FY2024": 46.5, "FY2023": 49.8, "FY2022": 29.4}),
        ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 2073.2, "FY2024": 1834.8, "FY2023": 1990.6, "FY2022": 1810.8, "FY2021": 1740.6, "FY2020": 1973.5, "FY2019": 2244.3, "FY2018": 2209.2, "FY2017": 2118.0, "FY2016": 2091.8, "FY2015": 1796.0, "FY2014": 1649.3}),
    ],
    sources_text=(
        "Sources - Vanquis Banking Group plc (consolidated) Pillar 3 UK OV1 disclosure, £m:\n"
        f"FY2025 & FY2024: Pillar 3 Disclosures 31 Dec 2025, UK OV1 table, p.8 - {P3_2025_URL}\n"
        f"FY2023 & FY2022: Pillar 3 Disclosures 2023, UK OV1 table (section 2.1), p.4 - {P3_2023_URL}\n"
        f"FY2021: Provident Financial plc Pillar 3 Disclosures 2021, Table 8 (5.3 Pillar 1 minimum requirement), "
        f"p.10 - {P3_2021_URL}\n"
        f"FY2020: Provident Financial plc Pillar 3 Disclosures 2020 - {P3_2020_URL}\n"
        f"FY2019: Provident Financial plc Pillar 3 Disclosures 2019 - {P3_2019_URL}\n"
        f"FY2018: Provident Financial plc Pillar 3 Disclosures 2018 - {P3_2018_URL}\n"
        f"FY2017: Provident Financial plc Pillar 3 Disclosures 2017 - {P3_2017_URL}\n"
        f"FY2016 (sourced from FY2017's own comparative column): Provident Financial plc Pillar 3 Disclosures "
        f"2017 - {P3_2017_URL}\n"
        f"FY2015: Provident Financial plc Pillar 3 Disclosures 2015 - {P3_2015_URL}\n"
        f"FY2014: Provident Financial plc Pillar 3 Disclosures 2014 - {P3_2014_URL}\n"
        "Note: FY2021 predates the UK OV1 template (introduced from FY2022) - Provident Financial plc's own "
        "older CRR-era Table 8 groups risk categories slightly differently ('Credit risk (excluding CCR)', "
        "'Counterparty credit risk (CCR)', 'Operational risk', 'Market risk') but sums to the same Total RWEA "
        "(£1,740.6m) already on file on the Total RWAs sheet; no 'amounts below thresholds' memo line exists in "
        "that year's table. FY2025's/FY2024's/FY2023's/FY2022's category rows sum exactly to Total RWAs; the "
        "'amounts below thresholds for deduction' row is an informational memo per the source template's own "
        "footnote and is correctly excluded from the sum. FY2014-FY2020 use the same older CRR-era Table 8 shape "
        "as FY2021 - FY2014/FY2015 disclose no separate market-risk RWA (rounds to nil) and instead fold a small "
        "residual CCR/CVA/rounding amount into an 'Other risks' memo line, shown here on the CCR row; FY2016 "
        "onward disclose a genuine non-zero market risk RWA. No securitised assets in any year FY2014-FY2020 "
        "(stated explicitly in the FY2017 document, applied uniformly). Every year's category rows sum exactly to "
        "that year's Total RWAs.\n\n"
        + ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=220,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure", {"FY2025": 3299.2, "FY2024": 2482.6, "FY2023": 2489.5, "FY2022": 2284.8, "FY2021": 2798.0, "FY2020": 3236.7, "FY2019": 3063.3, "FY2018": 3063.0, "FY2017": 2841.4, "FY2016": 2715.9, "FY2015": 2335.0, "FY2014": 2127.2}),
        ("Leverage ratio (%)", {"FY2025": "12.1%", "FY2024": "13.9%", "FY2023": "16.4%", "FY2022": "21.0%", "FY2021": "18.1%", "FY2020": "20.8%", "FY2019": "22.8%", "FY2018": "20.3%", "FY2017": "10.8%", "FY2016": "16.7%", "FY2015": "16.5%", "FY2014": "15.5%"}),
    ],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 6 (Leverage ratio)", P3_2021_URL, "9") + "\n"
    + p3_sources_pfg("FY2020: Pillar 3 Disclosures 2020", P3_2020_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2019: Pillar 3 Disclosures 2019", P3_2019_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2018: Pillar 3 Disclosures 2018", P3_2018_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2017: Pillar 3 Disclosures 2017", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2016 (sourced from FY2017's own comparative column)", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2015: Pillar 3 Disclosures 2015", P3_2015_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2014: Pillar 3 Disclosures 2014", P3_2014_URL, "n/a"),
    note="FY2022 onward use the UK KM1 template's 'leverage ratio excluding claims on central banks' basis. FY2021 "
         "predates that template and is calculated per CRR Article 429 instead (Table 6 of the 2021 Pillar 3 "
         "report) - a different, not directly comparable methodology, shown on its own basis rather than blended. "
         "FY2014-FY2020 use the same CRR Article 429 basis as FY2021 (consistent methodology across all of them). "
         "FY2015's leverage ratio has an alternate 16.9% basis also disclosed (including Q4 profits) - 16.5% "
         "(excluding Q4 profits) is used here as the primary, consistent figure.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA) / liquidity buffer", {"FY2025": 930.0, "FY2024": 802.0, "FY2023": 512.0, "FY2022": 383.2, "FY2021": 439, "FY2020": 842, "FY2019": 396, "FY2018": 453.6, "FY2017": 213.3}),
        ("Total net cash outflows (adjusted value)", {"FY2025": 249.4, "FY2024": 116.4, "FY2023": 74.7, "FY2022": 48.0, "FY2021": 21, "FY2020": 64, "FY2019": 96, "FY2018": 106.7, "FY2017": 92.8}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "391.6%", "FY2024": "1,001.2%", "FY2023": "847.1%", "FY2022": "986.2%", "FY2021": "2,073%", "FY2020": "1,756%", "FY2019": "578%", "FY2018": "490%", "FY2017": "242%", "FY2016": "207%", "FY2015": "Not required", "FY2014": "Not required"}),
    ],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5", "6") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4", "5") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 20 (10.2.1 Liquidity coverage ratio)", P3_2021_URL, "24") + "\n"
    + p3_sources_pfg("FY2020: Pillar 3 Disclosures 2020", P3_2020_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2019: Pillar 3 Disclosures 2019 (spot/point-in-time alternate of 224% also disclosed)", P3_2019_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2018: Pillar 3 Disclosures 2018 (spot/point-in-time alternate of 688% also disclosed)", P3_2018_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2017: Pillar 3 Disclosures 2017 (spot/point-in-time alternate of 189% also disclosed)", P3_2017_URL, "n/a") + "\n"
    + p3_sources_pfg("FY2016 (sourced from FY2017's own comparative column - ratio only, buffer/outflow sub-figures genuinely unavailable, a document-level self-skip)", P3_2017_URL, "n/a"),
    note="FY2022 onward use the UK KM1 template (12-month rolling average of month-end positions). FY2021 predates "
         "that template - its figures are the 31 December 2021 quarter's own values (£439m liquidity buffer, £21m "
         "net cash outflows, 2,073% LCR) from the pre-onshoring quarterly disclosure format, not a 12-month "
         "average. FY2017-FY2020 use the same 12-month-rolling-average methodology as FY2022 onward (not the "
         "FY2021 quarterly-spot exception). The LCR regime only came into force in the UK from 1 October 2015, so "
         "FY2014 and FY2015 have no LCR disclosure at all ('Not required'). FY2016's buffer/outflow sub-figures "
         "could not be sourced (see HISTORICAL_NOTE on the FY2016 Wayback truncation) - only the ratio itself "
         "survives via FY2017's own comparative column, a self-skip of those two sub-figures specifically.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2023": 2611.7, "FY2022": 2198.0}),
        ("Total required stable funding", {"FY2023": 1828.1, "FY2022": 1565.7}),
        ("NSFR ratio (%)", {"FY2025": "Not required", "FY2024": "Not required", "FY2023": "142.8%", "FY2022": "140.4%", "FY2021": "Not required", "FY2020": "Not required", "FY2019": "Not required", "FY2018": "Not required", "FY2017": "Not required", "FY2016": "Not required", "FY2015": "Not required", "FY2014": "Not required"}),
    ],
    p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4", "5") + "\n"
    + p3_sources("FY2024/FY2025 and FY2021 basis note", P3_2024_URL, "6"),
    note="Not required for FY2021 and earlier (NSFR only became binding in the UK from 1 January 2022) - this "
         "applies uniformly across FY2014-FY2021, consistent with the pre-existing FY2021 treatment. Not required "
         "from the 30 June 2024 reporting date onward: in March 2024 the Group was confirmed as a Small Domestic "
         "Deposit Taker consolidation entity, exempting it from NSFR reporting - so no FY2024 or FY2025 figures "
         "exist either, despite falling in the middle of the window where NSFR was otherwise required.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not applicable" for y in YEARS})],
    p3_sources("All years: Pillar 3 Disclosures 2021-2025 (no MREL section in any edition)", P3_2025_URL, "n/a"),
    note="No MREL disclosure of any kind (numeric or qualitative) appears in any Pillar 3 Disclosures document "
         "reviewed, FY2014-FY2025 - consistent with Vanquis Banking Group (and its Provident Financial plc "
         "predecessor entity) not being a resolution entity subject to a standalone MREL requirement in any of "
         "these years.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 3574.0, "FY2024": 2907.4, "FY2023": 2609.5, "FY2022": 1867.4, "FY2021": 1700.3, "FY2020": 2106.4, "FY2019": 1889.4, "FY2018": 1958.6, "FY2017": 1855.1, "FY2016": 1628.7, "FY2015": 1424.7, "FY2014": 1257.3}),
        ("Amounts receivable from customers", {"FY2025": 2003.2, "FY2024": 1419.2, "FY2023": 1382.9, "FY2022": 1257.9, "FY2021": 1091.5, "FY2020": 1094.3, "FY2019": 1461.5, "FY2018": 1473.8, "FY2017": 1554.7, "FY2016": 1424.7, "FY2015": 1252.0, "FY2014": 1109.4}),
        ("Retail deposits", {"FY2025": 3019.9, "FY2024": 2428.1, "FY2023": 1950.5, "FY2022": 1100.6, "FY2021": 1018.6, "FY2020": 1683.2, "FY2019": 1345.2, "FY2018": 1431.7, "FY2017": 1291.8}),
        ("Total equity", {"FY2025": 438.0, "FY2024": 361.7, "FY2023": 393.7, "FY2022": 385.0, "FY2021": 385.3, "FY2020": 327.1, "FY2019": 391.1, "FY2018": 375.4, "FY2017": 289.3, "FY2016": 379.7, "FY2015": 355.1, "FY2014": 284.6}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 374.3, "FY2024": 366.3, "FY2023": 385.4, "FY2022": 375.4, "FY2020": 453.7, "FY2019": 556.0, "FY2018": 622.7, "FY2017": 607.4, "FY2016": 545.6, "FY2015": 501.3, "FY2014": 431.7}),
        ("Impairment charges", {"FY2025": -139.2, "FY2024": -124.7, "FY2023": -150.9, "FY2022": -25.3, "FY2021": -5.9, "FY2020": -239.9, "FY2019": -198.9, "FY2018": -241.6, "FY2017": -171.9, "FY2016": -162.6, "FY2015": -149.9, "FY2014": -149.1}),
        ("Operating costs", {"FY2025": -190.6, "FY2024": -236.6, "FY2023": -223.4, "FY2022": -219.7, "FY2021": -195.6, "FY2020": -171.4, "FY2019": -179.5, "FY2018": -190.4, "FY2017": -222.7, "FY2016": -175.2, "FY2015": -162.3, "FY2014": -138.9}),
        ("Profit for the year", {"FY2025": 35.7, "FY2024": 7.5, "FY2023": 7.6, "FY2022": 93.8, "FY2021": 146.0, "FY2020": 42.6, "FY2019": 138.6, "FY2018": 145.9, "FY2017": -24.0, "FY2016": 167.8, "FY2015": 152.6, "FY2014": 113.4}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 361.7, "FY2024": 393.7, "FY2023": 385.0, "FY2022": 385.3, "FY2021": 327.1, "FY2020": 391.1, "FY2019": 391.4, "FY2018": 289.3, "FY2017": 379.7, "FY2016": 355.1, "FY2015": 284.6, "FY2014": 210.7}),
        ("Total comprehensive income for the year", {"FY2025": 35.7, "FY2024": 7.5, "FY2023": 7.6, "FY2022": 93.8, "FY2021": 142.1, "FY2020": 45.2, "FY2019": 141.9, "FY2018": 147.6, "FY2017": -22.6, "FY2016": 155.4, "FY2015": 165.3, "FY2014": 113.5}),
        ("Other equity movements, net", {"FY2025": 40.6, "FY2024": -39.5, "FY2023": 1.1, "FY2022": -94.1, "FY2021": -83.9, "FY2020": -109.2, "FY2019": -142.2, "FY2018": -61.5, "FY2017": -67.8, "FY2016": -130.8, "FY2015": -94.8, "FY2014": -39.6}),
        ("Closing equity", {"FY2025": 438.0, "FY2024": 361.7, "FY2023": 393.7, "FY2022": 385.0, "FY2021": 385.3, "FY2020": 327.1, "FY2019": 391.1, "FY2018": 375.4, "FY2017": 289.3, "FY2016": 379.7, "FY2015": 355.1, "FY2014": 284.6}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 19.6, "FY2024": 469.0, "FY2023": -534.0, "FY2022": 50.9, "FY2021": 180.9, "FY2020": 293.9, "FY2019": 154.0, "FY2018": 39.4, "FY2017": -23.9, "FY2016": 0.2, "FY2015": 24.0, "FY2014": -114.8}),
        ("Net cash from/(used in) investing activities", {"FY2025": -267.8, "FY2024": -8.5, "FY2023": -8.0, "FY2022": -21.7, "FY2021": -17.6, "FY2020": -11.7, "FY2019": 28.7, "FY2018": -3.4, "FY2017": -42.4, "FY2016": 8.9, "FY2015": -3.3, "FY2014": -6.1}),
        ("Net cash from/(used in) financing activities", {"FY2025": 49.0, "FY2024": -195.6, "FY2023": 809.1, "FY2022": -29.6, "FY2021": -583.5, "FY2020": 226.2, "FY2019": -231.1, "FY2018": 106.1, "FY2017": 125.1, "FY2016": 25.9, "FY2015": -11.4, "FY2014": 157.4}),
        ("Cash and cash equivalents at end of year", {"FY2025": 745.8, "FY2024": 945.0, "FY2023": 680.1, "FY2022": 413.0, "FY2021": 413.4, "FY2020": 833.6, "FY2019": 325.2, "FY2018": 373.6, "FY2017": 231.5, "FY2016": 172.7, "FY2015": 137.7, "FY2014": 128.4}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.5%", "FY2024": "18.8%", "FY2023": "20.5%", "FY2022": "26.4%", "FY2021": "29.1%", "FY2020": "34.2%", "FY2019": "31.1%", "FY2018": "28.2%", "FY2017": "14.5%", "FY2016": "21.7%", "FY2015": "21.5%", "FY2014": "20.0%"}),
        ("Tier 1 Ratio", {"FY2025": "19.3%", "FY2024": "18.8%", "FY2023": "20.5%", "FY2022": "26.4%", "FY2021": "29.1%", "FY2020": "34.2%", "FY2019": "31.1%", "FY2018": "28.2%", "FY2017": "14.5%", "FY2016": "21.7%", "FY2015": "21.5%", "FY2014": "20.0%"}),
        ("Total Capital Ratio", {"FY2025": "26.1%", "FY2024": "29.7%", "FY2023": "30.6%", "FY2022": "37.5%", "FY2021": "40.6%", "FY2020": "34.2%", "FY2019": "31.1%", "FY2018": "28.2%", "FY2017": "14.5%", "FY2016": "21.7%", "FY2015": "21.5%", "FY2014": "20.0%"}),
        ("Leverage Ratio", {"FY2025": "12.1%", "FY2024": "13.9%", "FY2023": "16.4%", "FY2022": "21.0%", "FY2021": "18.1%", "FY2020": "20.8%", "FY2019": "22.8%", "FY2018": "20.3%", "FY2017": "10.8%", "FY2016": "16.7%", "FY2015": "16.5%", "FY2014": "15.5%"}),
        ("LCR", {"FY2025": "391.6%", "FY2024": "1,001.2%", "FY2023": "847.1%", "FY2022": "986.2%", "FY2021": "2,073%", "FY2020": "1,756%", "FY2019": "578%", "FY2018": "490%", "FY2017": "242%", "FY2016": "207%", "FY2015": "Not required", "FY2014": "Not required"}),
        ("NSFR", {"FY2023": "142.8%", "FY2022": "140.4%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. IMPORTANT: the Cash Flow Summary above is Vanquis Bank "
         "Limited's own entity-level (Company) basis, but the Pillar 3 Key Metrics below are Vanquis Banking Group "
         "plc consolidated basis (Bank + Moneybarn No.1 Limited pre-2021 / Provident Financial plc pre-2021) - "
         "Vanquis does not publish a Bank-only Pillar 3 breakdown. See the Cash Flow Statement sheet's entity note "
         "for detail. FY2014-FY2020 is this build's historical-depth extension, capped at FY2014 per project "
         "decision - see HISTORICAL_NOTE on the Cash Flow Statement sheet for the OCR/Companies House sourcing "
         "methodology used for these years.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/VANQUIS FINANCIALS.xlsx")
