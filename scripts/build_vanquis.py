import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2021_URL = "https://www.vanquis.com/wp-content/uploads/2025/05/Vanquis_Bank_Ltd_31_12_2021_Signed.pdf"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/02558509/filing-history/MzQxNzkzNTkxNWFkaXF6a2N4/document?format=pdf&download=0"
AR2025_URL = "https://www.vanquis.com/wp-content/uploads/2026/03/VBL-stats-2025-FINAL-Fully-Signed.pdf"

P3_2021_URL = "https://www.vanquis.com/wp-content/uploads/2025/05/Provident_Financial_plc_Pillar_3_Disclosures_2021.pdf"
P3_2023_URL = "https://www.vanquis.com/wp-content/uploads/2025/05/04-04-24_Pillar-3-Disclosures-2023.pdf"
P3_2024_URL = "https://www.vanquis.com/wp-content/uploads/2025/05/Vanquis_Banking_Group_plc_Pillar_3_Disclosures_2024.pdf"
P3_2025_URL = "https://www.vanquis.com/wp-content/uploads/2026/02/DEC25_VANQ_Pillar-3-Disclosure_Annual_FINAL.pdf"

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
    "Note: presentation changed between report vintages - FY2021-FY2023 show 'Funding costs paid'/'Tax paid' as "
    "separate operating-activities lines and no loan-to-related-party financing lines; FY2024-FY2025 show 'Tax "
    "received'/no separate funding-costs line, and add 'Financing of loan to related party'/'Repayment of loan to "
    "related party' lines - each year's own as-reported presentation is preserved rather than forced into a common "
    "shape. Section totals and cash/cash equivalents figures are consistent and comparable across all 5 years "
    "(each year's opening balance matches the prior year's closing balance exactly). Note: FY2023's financing-"
    "activities line items sum to £809.2m against a printed 'Net cash generated from financing activities' total of "
    "£809.1m - an immaterial £0.1m artefact of each line being independently rounded to one decimal place in the "
    "source document itself (not a transcription error here); the printed total (£809.1m, used above) is the "
    "figure consistent with the overall net-change-in-cash reconciliation.\n\n"
    + ENTITY_NOTE + "\n\n" + DISCONTINUED_NOTE
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


bw = BankWorkbook(bank_name="Vanquis Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="0B4F6C")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Cash (used in)/generated from operations", {"FY2025": 15.5, "FY2024": 460.8, "FY2023": -494.1, "FY2022": 75.2, "FY2021": 212.9}),
    ("DATA", "Funding costs paid", {"FY2023": -33.8, "FY2022": -10.9, "FY2021": -25.9}),
    ("DATA", "Tax paid", {"FY2023": -6.1, "FY2022": -13.4, "FY2021": -6.1}),
    ("DATA", "Tax received", {"FY2025": 4.1, "FY2024": 8.2}),
    ("TOTAL", "Net cash (used in)/generated from operating activities", {"FY2025": 19.6, "FY2024": 469.0, "FY2023": -534.0, "FY2022": 50.9, "FY2021": 180.9}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property and equipment", {"FY2025": -1.4, "FY2024": -1.2, "FY2023": -1.9, "FY2022": -2.5, "FY2021": -0.7}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -14.6, "FY2024": -11.6, "FY2023": -12.5, "FY2022": -19.2, "FY2021": -16.9}),
    ("DATA", "Purchase of investment securities", {"FY2025": -291.8}),
    ("DATA", "Proceeds from maturity of investment securities", {"FY2025": 40.0}),
    ("DATA", "Proceeds from sale of investments", {"FY2024": 4.3, "FY2023": 6.4}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -267.8, "FY2024": -8.5, "FY2023": -8.0, "FY2022": -21.7, "FY2021": -17.6}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payment/capital elements of lease liabilities", {"FY2025": -6.8, "FY2024": -5.5, "FY2023": -6.0, "FY2022": -6.1, "FY2021": -6.1}),
    ("DATA", "Financing of loan to related party", {"FY2025": -163.0, "FY2024": -140.0}),
    ("DATA", "Repayment of loan to related party", {"FY2025": 183.9, "FY2024": 158.9}),
    ("DATA", "Proceeds from borrowings", {"FY2024": 5.0, "FY2023": 1100.0, "FY2022": 330.0, "FY2021": 295.8}),
    ("DATA", "Repayment of borrowings", {"FY2025": -5.0, "FY2024": -174.0, "FY2023": -284.8, "FY2022": -258.4, "FY2021": -788.2}),
    ("DATA", "Proceeds of issuance of other equity instruments", {"FY2025": 59.9}),
    ("DATA", "Dividends paid to company shareholder", {"FY2025": -20.0, "FY2024": -40.0, "FY2022": -95.1, "FY2021": -85.0}),
    ("TOTAL", "Net cash generated/(used in) financing activities", {"FY2025": 49.0, "FY2024": -195.6, "FY2023": 809.1, "FY2022": -29.6, "FY2021": -583.5}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -199.2, "FY2024": 264.9, "FY2023": 267.1, "FY2022": -0.4, "FY2021": -420.2}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 945.0, "FY2024": 680.1, "FY2023": 413.0, "FY2022": 413.4, "FY2021": 833.6}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 745.8, "FY2024": 945.0, "FY2023": 680.1, "FY2022": 413.0, "FY2021": 413.4}),
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

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Vanquis Banking Group consolidated basis, {unit}" if unit else "Vanquis Banking Group consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=120)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 341.3, "FY2024": 344.3, "FY2023": 409.0, "FY2022": 478.8, "FY2021": 506.5})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22 (Appendix 1 - Own funds disclosures)", P3_2021_URL, "28"),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "16.5%", "FY2024": "18.8%", "FY2023": "20.5%", "FY2022": "26.4%", "FY2021": "29.1%"})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28"),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 400.0, "FY2024": 344.3, "FY2023": 409.0, "FY2022": 478.8, "FY2021": 506.5})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28"),
    note="FY2025 is the first year Tier 1 capital exceeds CET1 - the Group issued £59.9m of other (AT1) equity "
         "instruments during 2025 (see Cash Flow Statement sheet, financing activities). All other years shown have "
         "no Additional Tier 1 capital, so Tier 1 = CET1 exactly.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "19.3%", "FY2024": "18.8%", "FY2023": "20.5%", "FY2022": "26.4%", "FY2021": "29.1%"})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28"),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 541.5, "FY2024": 544.3, "FY2023": 609.0, "FY2022": 678.8, "FY2021": 706.5})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28"),
    note="DATA QUALITY NOTE: the FY2024 Pillar 3 Disclosures document's own comparative column for 31 Dec 2023 "
         "prints a 'Total capital' amount (£393.4m) that is inconsistent with that same document's own 31 Dec 2023 "
         "Total capital RATIO (30.0%) and RWA (£1,975.6m) - 30.0% x 1,975.6 implies Total capital of ~£592.7m, not "
         "£393.4m (and £393.4m simply repeats that column's CET1 figure, i.e. as if Tier 2 capital were zero, which "
         "contradicts row UK 7c showing a non-zero Additional T2 SREP requirement). The figures used here for FY2023 "
         "instead come from the FY2023 Pillar 3 Disclosures document's OWN as-originally-reported 31 Dec 2023 "
         "column (£609.0m), which is internally consistent (609.0 / 1,990.6 = 30.6%, matching its own stated ratio "
         "exactly) - this is also why FY2023's RWA here (£1,990.6m) differs slightly from the restated £1,975.6m "
         "shown as a comparative in the FY2024 document (a legitimate restatement, per that document's own footnote, "
         "for a Vehicle Finance Stage 3 ECL review - unrelated to the Total capital error).",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "26.1%", "FY2024": "29.7%", "FY2023": "30.6%", "FY2022": "37.5%", "FY2021": "40.6%"})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28"),
    note="See the Total Capital sheet's DATA QUALITY NOTE - this ratio row is unaffected (it is directly stated in "
         "each document, not derived from the erroneous amount), but is included here for context.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 2073.2, "FY2024": 1834.8, "FY2023": 1990.6, "FY2022": 1810.8, "FY2021": 1740.6})],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 22", P3_2021_URL, "28"),
    note="FY2023 (£1,990.6m) is as originally reported in the FY2023 Pillar 3 Disclosures; the FY2024 document later "
         "restated the 31 Dec 2023 comparative to £1,975.6m following a Vehicle Finance Stage 3 ECL methodology "
         "review - both figures are genuine, just on slightly different bases (see Total Capital sheet note).",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure", {"FY2025": 3299.2, "FY2024": 2482.6, "FY2023": 2489.5, "FY2022": 2284.8, "FY2021": 2798.0}),
        ("Leverage ratio (%)", {"FY2025": "12.1%", "FY2024": "13.9%", "FY2023": "16.4%", "FY2022": "21.0%", "FY2021": "18.1%"}),
    ],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 6 (Leverage ratio)", P3_2021_URL, "9"),
    note="FY2022 onward use the UK KM1 template's 'leverage ratio excluding claims on central banks' basis. FY2021 "
         "predates that template and is calculated per CRR Article 429 instead (Table 6 of the 2021 Pillar 3 "
         "report) - a different, not directly comparable methodology, shown on its own basis rather than blended.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA) / liquidity buffer", {"FY2025": 930.0, "FY2024": 802.0, "FY2023": 512.0, "FY2022": 383.2, "FY2021": 439}),
        ("Total net cash outflows (adjusted value)", {"FY2025": 249.4, "FY2024": 116.4, "FY2023": 74.7, "FY2022": 48.0, "FY2021": 21}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "391.6%", "FY2024": "1,001.2%", "FY2023": "847.1%", "FY2022": "986.2%", "FY2021": "2,073%"}),
    ],
    p3_sources("FY2025: Pillar 3 Disclosures 31 Dec 2025", P3_2025_URL, "7") + "\n"
    + p3_sources("FY2024: Pillar 3 Disclosures 2024", P3_2024_URL, "5", "6") + "\n"
    + p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4", "5") + "\n"
    + p3_sources("FY2021: Pillar 3 Disclosures 2021, Table 20 (10.2.1 Liquidity coverage ratio)", P3_2021_URL, "24"),
    note="FY2022 onward use the UK KM1 template (12-month rolling average of month-end positions). FY2021 predates "
         "that template - its figures are the 31 December 2021 quarter's own values (£439m liquidity buffer, £21m "
         "net cash outflows, 2,073% LCR) from the pre-onshoring quarterly disclosure format, not a 12-month average.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2023": 2611.7, "FY2022": 2198.0}),
        ("Total required stable funding", {"FY2023": 1828.1, "FY2022": 1565.7}),
        ("NSFR ratio (%)", {"FY2025": "Not required", "FY2024": "Not required", "FY2023": "142.8%", "FY2022": "140.4%", "FY2021": "Not required"}),
    ],
    p3_sources("FY2023 & FY2022: Pillar 3 Disclosures 2023", P3_2023_URL, "4", "5") + "\n"
    + p3_sources("FY2024/FY2025 and FY2021 basis note", P3_2024_URL, "6"),
    note="Not required for FY2021 (NSFR only became binding in the UK from 1 January 2022). Not required from the "
         "30 June 2024 reporting date onward: in March 2024 the Group was confirmed as a Small Domestic Deposit "
         "Taker consolidation entity, exempting it from NSFR reporting - so no FY2024 or FY2025 figures exist "
         "either, despite falling in the middle of the window where NSFR was otherwise required.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not applicable" for y in YEARS})],
    p3_sources("All years: Pillar 3 Disclosures 2021-2025 (no MREL section in any edition)", P3_2025_URL, "n/a"),
    note="No MREL disclosure of any kind (numeric or qualitative) appears in any Pillar 3 Disclosures document "
         "reviewed, FY2021-FY2025 - consistent with Vanquis Banking Group not being a resolution entity subject to "
         "a standalone MREL requirement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 19.6, "FY2024": 469.0, "FY2023": -534.0, "FY2022": 50.9, "FY2021": 180.9}),
        ("Net cash from/(used in) investing activities", {"FY2025": -267.8, "FY2024": -8.5, "FY2023": -8.0, "FY2022": -21.7, "FY2021": -17.6}),
        ("Net cash from/(used in) financing activities", {"FY2025": 49.0, "FY2024": -195.6, "FY2023": 809.1, "FY2022": -29.6, "FY2021": -583.5}),
        ("Cash and cash equivalents at end of year", {"FY2025": 745.8, "FY2024": 945.0, "FY2023": 680.1, "FY2022": 413.0, "FY2021": 413.4}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.5%", "FY2024": "18.8%", "FY2023": "20.5%", "FY2022": "26.4%", "FY2021": "29.1%"}),
        ("Tier 1 Ratio", {"FY2025": "19.3%", "FY2024": "18.8%", "FY2023": "20.5%", "FY2022": "26.4%", "FY2021": "29.1%"}),
        ("Total Capital Ratio", {"FY2025": "26.1%", "FY2024": "29.7%", "FY2023": "30.6%", "FY2022": "37.5%", "FY2021": "40.6%"}),
        ("Leverage Ratio", {"FY2025": "12.1%", "FY2024": "13.9%", "FY2023": "16.4%", "FY2022": "21.0%", "FY2021": "18.1%"}),
        ("LCR", {"FY2025": "391.6%", "FY2024": "1,001.2%", "FY2023": "847.1%", "FY2022": "986.2%", "FY2021": "2,073%"}),
        ("NSFR", {"FY2023": "142.8%", "FY2022": "140.4%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. IMPORTANT: the Cash Flow Summary above is Vanquis Bank "
         "Limited's own entity-level (Company) basis, but the Pillar 3 Key Metrics below are Vanquis Banking Group "
         "plc consolidated basis (Bank + Moneybarn No.1 Limited) - Vanquis does not publish a Bank-only Pillar 3 "
         "breakdown. See the Cash Flow Statement sheet's entity note for detail.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/VANQUIS FINANCIALS.xlsx")
