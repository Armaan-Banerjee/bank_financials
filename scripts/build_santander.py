import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]  # most recent first

AR2025_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/SantanderUKplc2025AnnualReport.pdf"
AR2023_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/santander_uk_plc_annual_report_2023.pdf"
AR2020_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/santander_uk_plc_2020_annual_report.pdf"

ACRMD2025_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/2025SantanderUKACRMD.pdf"
ACRMD2023_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/santander_uk_acrmd_2023.pdf"
ACRMD2022_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/santander_uk_additional_capital_and_risk_management_disclosures_2022.pdf"
ACRMD2021_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/2021_additional_capital_risk_management_disclosures.pdf"
ACRMD2020_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/santander_uk_acrmd_2020_0.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Santander UK Plc (FRN 106054, company number 02294747) is the PRA-authorised ring-fenced bank "
    "(RFB) - not to be confused with 'Santander Financial Services plc' (FRN 146003, a separate, smaller PRA-"
    "authorised entity) or with its own intermediate holding company 'Santander UK Group Holdings plc' (the "
    "resolution entity, which publishes its own separate Annual Report/Pillar 3). This workbook uses Santander UK "
    "Plc's own consolidated ('RFB Group') basis throughout, consistent with how this workbook series always prefers "
    "the ring-fenced/regulated banking entity's own consolidation level over a wider holding company - matching "
    "Barclays' use of 'Barclays Bank UK Group' rather than 'Barclays PLC'."
)

FY2020_EXTENSION_NOTE = (
    "FY2020 EXTENSION NOTE: FY2020 was added by re-verifying directly against Santander UK plc's own primary "
    "source documents (its FY2020 Annual Report and 31 December 2020 ACRMD), not assumed from the historical-"
    "depth ticket's nominal 'confirmed floor FY2020' signal alone. FY2020's Balance Sheet and Statement of Changes "
    "in Equity both tie exactly into the FY2021 column already in this workbook (e.g. FY2020's own closing Total "
    "equity of 15,936 is the exact same figure already used as this workbook's FY2021 opening balance) - no "
    "restatement at that boundary. FY2020's own cash-equivalents reconciliation, by contrast, does NOT tie exactly "
    "to the FY2021 column's opening balance - see the Cash Flow Statement sheet's own source note for the £1,115m "
    "gap, consistent with the same cash-equivalents composition restatement pattern already documented at the "
    "FY2023/FY2024 boundary. FY2020's own Cash Flow Statement is "
    "presented differently to every later year - starting from 'Profit after tax' plus a separate 'Corporation "
    "tax charge' non-cash addback, rather than starting from 'Profit before tax' directly - so the 'Profit "
    "before tax' cell shown for FY2020 here is the two figures recombined (471 + 134 = 605), which ties exactly "
    "to the Income Statement's own independently-disclosed FY2020 Profit before tax of 605; not an estimated "
    "plug. FY2020's cash flow statement also does not itemise 'Reverse repurchase agreements' / 'Repurchase "
    "agreements' as their own net-change lines (left blank for FY2020 only), does not itemise lease principal "
    "repayments as its own financing-activities line (embedded within 'Other liabilities' instead, per the "
    "source document's own footnote), and presents 'Other cash equivalents' as a single £5,186m line rather than "
    "split by instrument type (shown under 'loans and advances to banks - non-trading' for lack of a more precise "
    "label, with the reverse-repo sub-row blank for FY2020 only) - the within-year reconciliation (beginning + "
    "change + FX = end) still ties exactly for FY2020 itself; see above re: the cross-year gap into FY2021. FY2020 "
    "also still carries a small non-controlling interest (£162m, disposed of during "
    "2021 per the existing FY2021 note) and a 'Dividends paid on non-controlling interests' cash flow line "
    "(£15m), both genuinely absent from FY2021 onward."
)

TSB_ACQUISITION_NOTE = (
    "TSB ACQUISITION NOTE: On 21 July 2025 Banco Santander agreed to acquire TSB Banking Group plc (parent of TSB "
    "Bank plc, also covered elsewhere in this workbook series) from Sabadell for c.£2.65bn, with completion expected "
    "in early 2026 and a subsequent merger of TSB into the Santander UK group. The FY2025 ACRMD's 'Key Movements' "
    "commentary explicitly cites 'a no-dividend decision for 2025, in anticipation of the acquisition of TSB' as a "
    "driver of Santander UK's improved FY2025 capital ratios. This acquisition was still pending as at the FY2025 "
    "reporting date and is not reflected in any of the historical figures below; it may be worth revisiting both "
    "workbooks once the transaction completes and TSB Bank plc's own reporting entity status changes."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Santander UK Plc consolidated cash flow statement, £m:\n"
    f"FY2025 & FY2024: Santander UK plc Annual Report 2025, p.126 (Consolidated Cash Flow Statement) - {AR2025_URL}\n"
    f"FY2023, FY2022 & FY2021: Santander UK plc Annual Report 2023, p.120 (Consolidated Cash Flow Statement) - "
    f"{AR2023_URL}\n"
    f"FY2020: Santander UK plc Annual Report 2020, p.176 (Consolidated Cash Flow Statement) - {AR2020_URL}\n"
    "Note: Santander UK redefined the composition of 'cash and cash equivalents' between these report vintages - "
    "the FY2023 annual report (used for the FY2023/FY2022/FY2021 columns here) includes 'Reverse repurchase "
    "agreements' as a component of cash equivalents, while the FY2025 annual report's presentation (used for the "
    "FY2025/FY2024 columns) does not. Each column above uses that year's own report's original presentation rather "
    "than a later restated comparative, so FY2023's closing cash balance (42,502) will not tie directly to the "
    "FY2024 column's opening balance as shown in the FY2025 report (36,781) - the £5,721m difference is exactly the "
    "FY2023 reverse-repo balance reclassified out of cash equivalents. The same pattern recurs at the FY2020/FY2021 "
    "boundary: FY2020's own closing cash balance as originally reported in the FY2020 Annual Report (45,582, using "
    "that report's single undifferentiated 'Other cash equivalents' line) does not tie directly to the FY2021 "
    "column's opening balance as shown in the FY2023 report (46,697) - a £1,115m gap consistent with the same kind "
    "of cash-equivalents composition restatement, though the FY2023 report does not itemise FY2020's restated "
    "composition closely enough to attribute the gap to a specific instrument. Operating/investing/financing "
    "subtotals and the change-in-cash reconciliation are internally consistent within each year shown.\n\n"
    + ENTITY_NOTE + "\n\n" + TSB_ACQUISITION_NOTE + "\n\n" + FY2020_EXTENSION_NOTE
)


def p3_sources(page_25="47-48", page_23="47-48", page_21="42", page_20="42"):
    return (
        "Sources - Santander UK Plc's own consolidated ('RFB Group') basis, from the Additional Capital and Risk "
        "Management Disclosures (ACRMD, Santander UK's Pillar 3 equivalent document):\n"
        f"FY2025 & FY2024: Santander UK Group Holdings plc and Santander UK plc - Additional Capital and Risk "
        f"Management Disclosures, 31 December 2025, p.{page_25} (Key metrics (KM1), RFB Group) - {ACRMD2025_URL}\n"
        f"FY2023 & FY2022: Santander UK Group Holdings plc and Santander UK plc - Additional Capital and Risk "
        f"Management Disclosures, 31 December 2023, p.{page_23} (Key metrics (KM1), RFB Group) - {ACRMD2023_URL}\n"
        f"FY2021: Santander UK Group Holdings plc and Santander UK plc - Additional Capital and Risk Management "
        f"Disclosures, 31 December 2021, p.{page_21} (Key metrics (KM1), RFB Group) - {ACRMD2021_URL}\n"
        f"FY2020: Santander UK plc - Additional Capital and Risk Management Disclosures, 31 December 2020, "
        f"p.{page_20} (Key metrics, Part 2: Santander UK plc Group) - {ACRMD2020_URL}"
    )


AR2022_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/santander_uk_plc_annual_report_2022.pdf"

ACRMD2024_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/ACRMD%20FINAL_Dec%2024.pdf"

STATEMENTS_SOURCES = (
    "Sources - Santander UK Plc consolidated ('RFB Group') basis, £m:\n"
    f"FY2025: Santander UK plc Annual Report 2025, p.123 (Consolidated Income Statement), p.124 (Consolidated "
    f"Statement of Comprehensive Income), p.125 (Consolidated Balance Sheet), p.127 (Consolidated Statement of "
    f"Changes in Equity) - {AR2025_URL}\n"
    f"FY2024: Santander UK plc Annual Report 2025, p.123-127 (FY2024 comparative column of the same statements) - "
    f"{AR2025_URL}\n"
    f"FY2023: Santander UK plc Annual Report 2023, p.117 (Consolidated Income Statement), p.118 (Consolidated "
    f"Statement of Comprehensive Income), p.119 (Consolidated Balance Sheet), p.121 (Consolidated Statement of "
    f"Changes in Equity) - {AR2023_URL}\n"
    f"FY2022: Santander UK plc Annual Report 2023, p.117-121 (FY2022 comparative column), independently "
    f"cross-checked against Santander UK plc Annual Report 2022's own FY2022 Balance Sheet (p.131, Total assets "
    f"285,213 / Total liabilities 270,806 / Total equity 14,407), which agrees exactly - {AR2023_URL}\n"
    f"FY2021: Santander UK plc Annual Report 2022, p.129 (Consolidated Income Statement), p.132 (Consolidated "
    f"Balance Sheet), p.121-122 comparative in the FY2023 report's Statement of Changes in Equity (opening/closing "
    f"equity ties exactly to both years' own Balance Sheet Total equity: 16,102) - {AR2022_URL}\n"
    "Presentation note: FY2021 includes a small discontinued-operations profit of £31m and non-controlling "
    "interests of £19m (disposed of during 2021, per the Statement of Changes in Equity's 'Disposal of "
    "non-controlling interests' movement) - neither recurs from FY2022 onward. FY2025's Statement of Changes in "
    "Equity introduces a new 'Cost of hedging reserve' column (nil in prior years) and drops the "
    "'Non-controlling interests' column (nil since FY2022). Each year's own as-published structure is preserved "
    "rather than forced into a common format.\n\n"
    + ENTITY_NOTE + "\n\n" + TSB_ACQUISITION_NOTE
)

bw = BankWorkbook(bank_name="Santander UK Plc", years=YEARS, header_color="EC0000")

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. Zero undocumented plug rows - Total assets = Total
# liabilities + Total equity for every year.
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 29376, "FY2024": 29881, "FY2023": 38214, "FY2022": 44190, "FY2021": 48139, "FY2020": 41250}),
    ("DATA", "Derivative financial instruments", {"FY2025": 870, "FY2024": 1204, "FY2023": 1432, "FY2022": 2407, "FY2021": 1681, "FY2020": 3406}),
    ("DATA", "Other financial assets at FVTPL", {"FY2025": 64, "FY2024": 136, "FY2023": 262, "FY2022": 129, "FY2021": 185, "FY2020": 208}),
    ("DATA", "Loans and advances to banks", {"FY2025": 1048, "FY2024": 1032, "FY2023": 1080, "FY2022": 992, "FY2021": 1169, "FY2020": 1682}),
    ("DATA", "Loans and advances to customers", {"FY2025": 202609, "FY2024": 199408, "FY2023": 207435, "FY2022": 219716, "FY2021": 210094, "FY2020": 208750}),
    ("DATA", "Reverse repurchase agreements - non-trading", {"FY2025": 17678, "FY2024": 10338, "FY2023": 12468, "FY2022": 7348, "FY2021": 12683, "FY2020": 19599}),
    ("DATA", "Other financial assets at amortised cost", {"FY2025": 3987, "FY2024": 3408, "FY2023": 152, "FY2022": 156, "FY2021": 506, "FY2020": 1163}),
    ("DATA", "Macro hedge of interest rate risk", {"FY2025": -80, "FY2024": -738, "FY2023": -632, "FY2022": -2657, "FY2021": 77}),
    ("DATA", "Financial assets at FVOCI", {"FY2025": 5216, "FY2024": 9040, "FY2023": 8481, "FY2022": 6024, "FY2021": 5851, "FY2020": 8950}),
    ("DATA", "Interests in other entities", {"FY2025": 293, "FY2024": 289, "FY2023": 245, "FY2022": 252, "FY2021": 201, "FY2020": 172}),
    ("DATA", "Intangible assets", {"FY2025": 1511, "FY2024": 1539, "FY2023": 1548, "FY2022": 1550, "FY2021": 1545, "FY2020": 1646}),
    ("DATA", "Property, plant and equipment", {"FY2025": 1511, "FY2024": 1563, "FY2023": 1494, "FY2022": 1513, "FY2021": 1548, "FY2020": 1734}),
    ("DATA", "Current tax assets", {"FY2025": 355, "FY2024": 506, "FY2023": 490, "FY2022": 478, "FY2021": 347, "FY2020": 264}),
    ("DATA", "Retirement benefit assets", {"FY2025": 524, "FY2024": 439, "FY2023": 723, "FY2022": 1050, "FY2021": 1572, "FY2020": 495}),
    ("DATA", "Other assets", {"FY2025": 1857, "FY2024": 1887, "FY2023": 2043, "FY2022": 2016, "FY2021": 1500, "FY2020": 3013}),
    ("DATA", "Assets held for sale", {"FY2025": 18, "FY2024": 12, "FY2023": 13, "FY2022": 49}),
    ("TOTAL", "Total assets", {"FY2025": 266837, "FY2024": 259944, "FY2023": 275448, "FY2022": 285213, "FY2021": 287098, "FY2020": 292332}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 6628, "FY2024": 13993, "FY2023": 20332, "FY2022": 28525, "FY2021": 33855, "FY2020": 20958}),
    ("DATA", "Deposits by customers", {"FY2025": 187300, "FY2024": 180967, "FY2023": 190850, "FY2022": 195568, "FY2021": 192926, "FY2020": 195135}),
    ("DATA", "Repurchase agreements - non-trading", {"FY2025": 9029, "FY2024": 8617, "FY2023": 8411, "FY2022": 7982, "FY2021": 11718, "FY2020": 15848}),
    ("DATA", "Derivative financial instruments", {"FY2025": 687, "FY2024": 702, "FY2023": 818, "FY2022": 951, "FY2021": 777, "FY2020": 1584}),
    ("DATA", "Other financial liabilities at FVTPL", {"FY2025": 1250, "FY2024": 1055, "FY2023": 899, "FY2022": 803, "FY2021": 803, "FY2020": 1434}),
    ("DATA", "Debt securities in issue", {"FY2025": 41388, "FY2024": 35673, "FY2023": 33910, "FY2022": 31531, "FY2021": 25520, "FY2020": 35566}),
    ("DATA", "Macro hedge of interest rate risk", {"FY2025": 60, "FY2024": 47, "FY2023": 86, "FY2022": 95, "FY2021": 122}),
    ("DATA", "Other liabilities", {"FY2025": 2173, "FY2024": 1852, "FY2023": 2479, "FY2022": 2581, "FY2021": 2067, "FY2020": 2337}),
    ("DATA", "Provisions", {"FY2025": 683, "FY2024": 611, "FY2023": 402, "FY2022": 378, "FY2021": 364, "FY2020": 464}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 437, "FY2024": 246, "FY2023": 186, "FY2022": 35, "FY2021": 579, "FY2020": 111}),
    ("DATA", "Retirement benefit obligations", {"FY2025": 22, "FY2024": 23, "FY2023": 66, "FY2022": 25, "FY2021": 37, "FY2020": 403}),
    ("DATA", "Subordinated liabilities", {"FY2025": 2032, "FY2024": 2385, "FY2023": 2386, "FY2022": 2332, "FY2021": 2228, "FY2020": 2556}),
    ("TOTAL", "Total liabilities", {"FY2025": 251689, "FY2024": 246171, "FY2023": 260825, "FY2022": 270806, "FY2021": 270996, "FY2020": 276396}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 3105, "FY2024": 3105, "FY2023": 3105, "FY2022": 3105, "FY2021": 3105, "FY2020": 3105}),
    ("DATA", "Share premium", {"FY2025": 1119, "FY2024": 5620, "FY2023": 5620, "FY2022": 5620, "FY2021": 5620, "FY2020": 5620}),
    ("DATA", "Other equity instruments", {"FY2025": 1860, "FY2024": 1860, "FY2023": 1956, "FY2022": 1956, "FY2021": 2191, "FY2020": 2191}),
    ("DATA", "Other reserves", {"FY2025": 186, "FY2024": -333, "FY2023": -353, "FY2022": -1122, "FY2021": 133, "FY2020": 510}),
    ("DATA", "Retained earnings", {"FY2025": 8878, "FY2024": 3521, "FY2023": 4295, "FY2022": 4848, "FY2021": 5053, "FY2020": 4348}),
    ("DATA", "Non-controlling interests", {"FY2020": 162}),
    ("TOTAL", "Total equity", {"FY2025": 15148, "FY2024": 13773, "FY2023": 14623, "FY2022": 14407, "FY2021": 16102, "FY2020": 15936}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 266837, "FY2024": 259944, "FY2023": 275448, "FY2022": 285213, "FY2021": 287098, "FY2020": 292332}),
]

bw.add_balance_sheet_sheet(
    title="Santander UK Plc — Balance Sheet",
    subtitle="Santander UK Plc Group (consolidated 'RFB Group' basis), £m. Total assets = Total liabilities + "
              "Total equity for every year; Total equity ties exactly to the Statement of Changes in Equity "
              "sheet's own opening/closing balances - zero plug rows. FY2020 carries its own small "
              "'Non-controlling interests' equity line (blank thereafter, disposed of during 2021) and does not "
              "disclose a separate 'Macro hedge of interest rate risk' or 'Assets held for sale' line (both left "
              "blank for FY2020 only, per its own report's older balance sheet presentation).",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss (Consolidated Income Statement + Statement of Comprehensive
# Income)
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 11541, "FY2024": 12439, "FY2023": 11617, "FY2022": 6708, "FY2021": 4762, "FY2020": 5105}),
    ("DATA", "Interest expense and similar charges", {"FY2025": -7161, "FY2024": -8127, "FY2023": -6959, "FY2022": -2283, "FY2021": -813, "FY2020": -1662}),
    ("TOTAL", "Net interest income", {"FY2025": 4380, "FY2024": 4312, "FY2023": 4658, "FY2022": 4425, "FY2021": 3949, "FY2020": 3443}),
    ("DATA", "Fee and commission income", {"FY2025": 752, "FY2024": 733, "FY2023": 804, "FY2022": 839, "FY2021": 697, "FY2020": 756}),
    ("DATA", "Fee and commission expense", {"FY2025": -419, "FY2024": -481, "FY2023": -501, "FY2022": -509, "FY2021": -411, "FY2020": -371}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 333, "FY2024": 252, "FY2023": 303, "FY2022": 330, "FY2021": 286, "FY2020": 385}),
    ("DATA", "Other operating income", {"FY2025": 16, "FY2024": 93, "FY2023": 135, "FY2022": 201, "FY2021": 264, "FY2020": 147}),
    ("TOTAL", "Total operating income", {"FY2025": 4729, "FY2024": 4657, "FY2023": 5096, "FY2022": 4956, "FY2021": 4499, "FY2020": 3975}),
    ("SECTION", "Impairment, provisions and expenses", {}),
    ("DATA", "Operating expenses before credit impairment charges, provisions and charges", {"FY2025": -2457, "FY2024": -2548, "FY2023": -2456, "FY2022": -2343, "FY2021": -2510, "FY2020": -2452}),
    ("DATA", "Credit impairment charges/(write-backs)", {"FY2025": -193, "FY2024": -71, "FY2023": -205, "FY2022": -320, "FY2021": 233, "FY2020": -645}),
    ("DATA", "Provisions for other liabilities and charges", {"FY2025": -597, "FY2024": -689, "FY2023": -335, "FY2022": -419, "FY2021": -377, "FY2020": -273}),
    ("TOTAL", "Total credit impairment charges, provisions and charges", {"FY2025": -790, "FY2024": -760, "FY2023": -540, "FY2022": -739, "FY2021": -144, "FY2020": -918}),
    ("TOTAL", "Profit from continuing operations before tax", {"FY2025": 1482, "FY2024": 1349, "FY2023": 2100, "FY2022": 1874, "FY2021": 1845, "FY2020": 605}),
    ("DATA", "Tax on profit", {"FY2025": -396, "FY2024": -378, "FY2023": -559, "FY2022": -480, "FY2021": -492, "FY2020": -134}),
    ("TOTAL", "Profit from continuing operations after tax", {"FY2025": 1086, "FY2024": 971, "FY2023": 1541, "FY2022": 1394, "FY2021": 1353, "FY2020": 471}),
    ("DATA", "Profit from discontinued operations after tax", {"FY2021": 31}),
    ("TOTAL", "Profit after tax", {"FY2025": 1086, "FY2024": 971, "FY2023": 1541, "FY2022": 1394, "FY2021": 1384, "FY2020": 471}),
    ("DATA", "Attributable to: equity holders of the parent", {"FY2025": 1086, "FY2024": 971, "FY2023": 1541, "FY2022": 1394, "FY2021": 1365, "FY2020": 452}),
    ("DATA", "Attributable to: non-controlling interests", {"FY2021": 19, "FY2020": 19}),
    ("SECTION", "Other comprehensive income, net of tax", {}),
    ("DATA", "Movement in fair value reserve (debt instruments)", {"FY2025": 11, "FY2024": -11, "FY2023": -11, "FY2022": -20, "FY2021": -3, "FY2020": 5}),
    ("DATA", "Cash flow hedges", {"FY2025": 529, "FY2024": 31, "FY2023": 780, "FY2022": -1235, "FY2021": -374, "FY2020": 110}),
    ("DATA", "Cost of hedging", {"FY2025": -20}),
    ("DATA", "Pension remeasurement", {"FY2025": -72, "FY2024": -289, "FY2023": -431, "FY2022": -455, "FY2021": 845, "FY2020": -372}),
    ("DATA", "Own credit adjustment", {"FY2025": -1, "FY2024": -12, "FY2023": -11, "FY2022": 20, "FY2020": -3}),
    ("DATA", "Currency translation on foreign operations", {"FY2025": -1}),
    ("TOTAL", "Total other comprehensive income/(expense), net of tax", {"FY2025": 446, "FY2024": -281, "FY2023": 327, "FY2022": -1690, "FY2021": 468, "FY2020": -260}),
    ("TOTAL", "Total comprehensive income/(expense)", {"FY2025": 1532, "FY2024": 690, "FY2023": 1868, "FY2022": -296, "FY2021": 1852, "FY2020": 211}),
]

bw.add_income_statement_sheet(
    title="Santander UK Plc — Profit & Loss",
    subtitle="Santander UK Plc Group (consolidated 'RFB Group' basis), £m. 'Total comprehensive income/(expense)' "
              "ties exactly to Profit after tax + Total other comprehensive income for every year. FY2021 includes "
              "a small discontinued-operations profit and non-controlling interest, both nil from FY2022 onward; "
              "FY2020 also carries a small non-controlling interest (disposed of during 2021) but no "
              "discontinued-operations line.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=74,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - equity reconciliation ladder steps 2-3:
# built year-by-year, confirmed against next year's opening AND that year's
# own Balance Sheet Total equity above. All 5 years tie exactly. Zero
# undocumented plug rows (verified against every OCI/dividend/instrument
# movement disclosed in each year's own equity note, including the FY2021
# non-controlling-interest disposal and FY2025's capital reduction).
# ---------------------------------------------------------------
EQUITY_HEADERS = [
    "Share capital", "Share premium", "Other equity instruments", "Fair value reserve",
    "Cash flow hedging reserve", "Cost of hedging reserve", "Currency translation reserve",
    "Retained earnings", "Non-controlling interests", "Total equity",
]

equity_rows = [
    ("TOTAL", "Balance at 1 January 2020", (3105, 5620, 2191, 23, 371, None, 1, 4546, 160, 16017)),
    ("DATA", "Profit after tax", (None, None, None, None, None, None, None, 452, 19, 471)),
    ("DATA", "Fair value reserve movements (debt instruments)", (None, None, None, 5, None, None, None, None, None, 5)),
    ("DATA", "Cash flow hedges", (None, None, None, None, 110, None, None, None, None, 110)),
    ("DATA", "Pension remeasurement", (None, None, None, None, None, None, None, -370, -2, -372)),
    ("DATA", "Own credit adjustment", (None, None, None, None, None, None, None, -3, None, -3)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -129, None, -129)),
    ("DATA", "Dividends on preference shares and other equity instruments", (None, None, None, None, None, None, None, -148, None, -148)),
    ("DATA", "Dividends on non-controlling interests", (None, None, None, None, None, None, None, None, -15, -15)),
    ("TOTAL", "Balance at 31 December 2020 / 1 January 2021", (3105, 5620, 2191, 28, 481, None, 1, 4348, 162, 15936)),
    ("DATA", "Profit after tax", (None, None, None, None, None, None, None, 1365, 19, 1384)),
    ("DATA", "Fair value reserve movements (debt instruments)", (None, None, None, -3, None, None, None, None, None, -3)),
    ("DATA", "Cash flow hedges", (None, None, None, None, -374, None, None, None, None, -374)),
    ("DATA", "Pension remeasurement", (None, None, None, None, None, None, None, 845, None, 845)),
    ("DATA", "Issue of other equity instruments", (None, None, 210, None, None, None, None, None, None, 210)),
    ("DATA", "Repurchase of other equity instruments", (None, None, -210, None, None, None, None, None, None, -210)),
    ("DATA", "Disposal of non-controlling interests", (None, None, None, None, None, None, None, None, -181, -181)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -1358, None, -1358)),
    ("DATA", "Dividends on preference shares and other equity instruments", (None, None, None, None, None, None, None, -147, None, -147)),
    ("TOTAL", "Balance at 31 December 2021 / 1 January 2022", (3105, 5620, 2191, 25, 107, None, 1, 5053, 0, 16102)),
    ("DATA", "Profit after tax", (None, None, None, None, None, None, None, 1394, None, 1394)),
    ("DATA", "Fair value reserve movements (debt instruments)", (None, None, None, -20, None, None, None, None, None, -20)),
    ("DATA", "Cash flow hedges", (None, None, None, None, -1235, None, None, None, None, -1235)),
    ("DATA", "Pension remeasurement", (None, None, None, None, None, None, None, -455, None, -455)),
    ("DATA", "Own credit adjustment", (None, None, None, None, None, None, None, 20, None, 20)),
    ("DATA", "Issue of other equity instruments", (None, None, 750, None, None, None, None, None, None, 750)),
    ("DATA", "Repurchase of other equity instruments", (None, None, -985, None, None, None, None, None, None, -985)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -1014, None, -1014)),
    ("DATA", "Dividends on preference shares and other equity instruments", (None, None, None, None, None, None, None, -150, None, -150)),
    ("TOTAL", "Balance at 31 December 2022 / 1 January 2023", (3105, 5620, 1956, 5, -1128, None, 1, 4848, 0, 14407)),
    ("DATA", "Profit after tax", (None, None, None, None, None, None, None, 1541, None, 1541)),
    ("DATA", "Fair value reserve movements (debt instruments)", (None, None, None, -11, None, None, None, None, None, -11)),
    ("DATA", "Cash flow hedges", (None, None, None, None, 780, None, None, None, None, 780)),
    ("DATA", "Pension remeasurement", (None, None, None, None, None, None, None, -431, None, -431)),
    ("DATA", "Own credit adjustment", (None, None, None, None, None, None, None, -11, None, -11)),
    ("DATA", "Other", (None, None, None, None, None, None, None, 1, None, 1)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -1530, None, -1530)),
    ("DATA", "Dividends on preference shares and other equity instruments", (None, None, None, None, None, None, None, -123, None, -123)),
    ("TOTAL", "Balance at 31 December 2023 / 1 January 2024", (3105, 5620, 1956, -6, -348, None, 1, 4295, 0, 14623)),
    ("DATA", "Profit after tax", (None, None, None, None, None, None, None, 971, None, 971)),
    ("DATA", "Fair value reserve movements (debt instruments)", (None, None, None, -11, None, None, None, None, None, -11)),
    ("DATA", "Cash flow hedges", (None, None, None, None, 31, None, None, None, None, 31)),
    ("DATA", "Pension remeasurement", (None, None, None, None, None, None, None, -289, None, -289)),
    ("DATA", "Own credit adjustment", (None, None, None, None, None, None, None, -12, None, -12)),
    ("DATA", "Issue of other equity instruments", (None, None, 400, None, None, None, None, None, None, 400)),
    ("DATA", "Repurchase of other equity instruments", (None, None, -496, None, None, None, None, -4, None, -500)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -1311, None, -1311)),
    ("DATA", "Dividends on preference shares and other equity instruments", (None, None, None, None, None, None, None, -129, None, -129)),
    ("TOTAL", "Balance at 31 December 2024 / 1 January 2025", (3105, 5620, 1860, -17, -317, None, 1, 3521, 0, 13773)),
    ("DATA", "Profit after tax", (None, None, None, None, None, None, None, 1086, None, 1086)),
    ("DATA", "Fair value reserve movements (debt instruments)", (None, None, None, 11, None, None, None, None, None, 11)),
    ("DATA", "Cash flow hedges", (None, None, None, None, 529, None, None, None, None, 529)),
    ("DATA", "Cost of hedging", (None, None, None, None, None, -20, None, None, None, -20)),
    ("DATA", "Pension remeasurement", (None, None, None, None, None, None, None, -72, None, -72)),
    ("DATA", "Own credit adjustment", (None, None, None, None, None, None, None, -1, None, -1)),
    ("DATA", "Currency translation on foreign operations", (None, None, None, None, None, None, -1, None, None, -1)),
    ("DATA", "Capital reduction", (None, -4501, None, None, None, None, None, 4501, None, 0)),
    ("DATA", "Issue of other equity instruments", (None, None, 500, None, None, None, None, None, None, 500)),
    ("DATA", "Repurchase of other equity instruments", (None, None, -500, None, None, None, None, None, None, -500)),
    ("DATA", "Other", (None, None, None, None, None, None, None, 1, None, 1)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -26, None, -26)),
    ("DATA", "Dividends on preference shares and other equity instruments", (None, None, None, None, None, None, None, -132, None, -132)),
    ("TOTAL", "Balance at 31 December 2025", (3105, 1119, 1860, -6, 212, -20, 0, 8878, 0, 15148)),
]

bw.add_equity_changes_sheet(
    title="Santander UK Plc — Statement of Changes in Equity",
    subtitle="Santander UK Plc Group (consolidated 'RFB Group' basis), £m, chronological (oldest to newest). Each "
              "year's closing Total equity ties exactly to that year's own Balance Sheet Total equity and to the "
              "next year's opening balance - zero undocumented plug rows across all 6 years. FY2020's own opening "
              "balance (1 January 2020, Total equity 16,017) ties exactly to the FY2019 comparative disclosed in "
              "the FY2020 Annual Report.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=54,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 1482, "FY2024": 1349, "FY2023": 2100, "FY2022": 1874, "FY2021": 1888, "FY2020": 605}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 322, "FY2024": 300, "FY2023": 290, "FY2022": 296, "FY2021": 501, "FY2020": 562}),
    ("DATA", "Loss from disposal of mortgage portfolio", {"FY2024": 31}),
    ("DATA", "Provisions for other liabilities and charges", {"FY2025": 597, "FY2024": 689, "FY2023": 335, "FY2022": 419, "FY2021": 381, "FY2020": 273}),
    ("DATA", "Impairment losses", {"FY2025": 207, "FY2024": 94, "FY2023": 195, "FY2022": 284, "FY2021": -228, "FY2020": 672}),
    ("DATA", "Other non-cash items", {"FY2025": -4, "FY2024": 65, "FY2023": -749, "FY2022": 1497, "FY2021": -147, "FY2020": -267}),
    ("DATA", "Pension charge for defined benefit pension schemes", {"FY2025": 8, "FY2024": 13, "FY2023": 13, "FY2022": 28, "FY2021": 38, "FY2020": 38}),
    ("SECTION", "Net change in operating assets and liabilities", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 140, "FY2024": 731, "FY2023": -88, "FY2022": 275, "FY2021": -659, "FY2020": -147}),
    ("DATA", "Derivative assets", {"FY2025": 334, "FY2024": 228, "FY2023": 975, "FY2022": -726, "FY2021": 1725, "FY2020": -90}),
    ("DATA", "Other financial assets at fair value through profit or loss", {"FY2025": 72, "FY2024": 130, "FY2023": 40, "FY2022": 877, "FY2021": 1007, "FY2020": 1603}),
    ("DATA", "Loans and advances to banks and customers", {"FY2025": -3403, "FY2024": 8065, "FY2023": 12112, "FY2022": -9966, "FY2021": -971, "FY2020": -2654}),
    ("DATA", "Reverse repurchase agreements - non-trading", {"FY2025": -7340, "FY2024": 2130, "FY2023": -3224, "FY2022": 6818, "FY2021": 7024}),
    ("DATA", "Other assets", {"FY2025": -70, "FY2024": 118, "FY2023": -141, "FY2022": -574, "FY2021": 324, "FY2020": -340}),
    ("DATA", "Deposits by banks and customers", {"FY2025": -1130, "FY2024": -16059, "FY2023": -13504, "FY2022": -3128, "FY2021": 10735, "FY2020": 19977}),
    ("DATA", "Repurchase agreements - non-trading", {"FY2025": 412, "FY2024": 206, "FY2023": 704, "FY2022": -4145, "FY2021": -7550}),
    ("DATA", "Derivative liabilities", {"FY2025": -15, "FY2024": -116, "FY2023": -133, "FY2022": 174, "FY2021": -807, "FY2020": 136}),
    ("DATA", "Other financial liabilities at fair value through profit or loss", {"FY2025": 241, "FY2024": 179, "FY2023": 102, "FY2022": -973, "FY2021": -1109, "FY2020": -1618}),
    ("DATA", "Debt securities in issue", {"FY2025": 38, "FY2024": 212, "FY2023": 962, "FY2022": 3120, "FY2021": -329, "FY2020": 1201}),
    ("DATA", "Other liabilities", {"FY2025": -299, "FY2024": -1403, "FY2023": -67, "FY2022": -98, "FY2021": -603, "FY2020": -966}),
    ("DATA", "Corporation taxes paid", {"FY2025": -46, "FY2024": -240, "FY2023": -537, "FY2022": -405, "FY2021": -427, "FY2020": -159}),
    ("DATA", "Effects of exchange rate differences", {"FY2025": -344, "FY2024": -53, "FY2023": -518, "FY2022": 1383, "FY2021": -542, "FY2020": 410}),
    ("TOTAL", "Net cash flows from operating activities", {"FY2025": -8798, "FY2024": -3331, "FY2023": -1133, "FY2022": -2970, "FY2021": 10251, "FY2020": 19236}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment and intangible assets", {"FY2025": -407, "FY2024": -528, "FY2023": -385, "FY2022": -496, "FY2021": -613, "FY2020": -373}),
    ("DATA", "Proceeds from sale of property, plant and equipment and intangible assets", {"FY2025": 161, "FY2024": 148, "FY2023": 175, "FY2022": 159, "FY2021": 437, "FY2020": 166}),
    ("DATA", "Purchase of financial assets at amortised cost and financial assets at FVOCI", {"FY2025": -1981, "FY2024": -10343, "FY2023": -10899, "FY2022": -2884, "FY2021": -1256, "FY2020": -3015}),
    ("DATA", "Proceeds from sale and redemption of financial assets at amortised cost and financial assets at FVOCI", {"FY2025": 5184, "FY2024": 6183, "FY2023": 8362, "FY2022": 3023, "FY2021": 4509, "FY2020": 9858}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": 2957, "FY2024": -4540, "FY2023": -2747, "FY2022": -198, "FY2021": 3077, "FY2020": 6636}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Issue of other equity instruments", {"FY2025": 500, "FY2024": 400, "FY2022": 750, "FY2021": 210}),
    ("DATA", "Issue of debt securities and subordinated notes", {"FY2025": 9833, "FY2024": 8425, "FY2023": 5276, "FY2022": 4794, "FY2021": 2878, "FY2020": 4190}),
    ("DATA", "Issuance costs of debt securities and subordinated notes", {"FY2025": -24, "FY2024": -28, "FY2023": -18, "FY2022": -16, "FY2021": -6, "FY2020": -13}),
    ("DATA", "Repayment of debt securities and subordinated notes", {"FY2025": -4219, "FY2024": -6539, "FY2023": -3539, "FY2022": -3076, "FY2021": -11914, "FY2020": -12037}),
    ("DATA", "Disposal of non-controlling interests", {"FY2021": -181}),
    ("DATA", "Repurchase of other equity instruments", {"FY2025": -500, "FY2024": -500, "FY2022": -985, "FY2021": -210}),
    ("DATA", "Dividends paid on ordinary shares", {"FY2025": -26, "FY2024": -1311, "FY2023": -1530, "FY2022": -1014, "FY2021": -1358, "FY2020": -129}),
    ("DATA", "Dividends paid on preference shares and other equity instruments", {"FY2025": -132, "FY2024": -129, "FY2023": -123, "FY2022": -150, "FY2021": -147, "FY2020": -148}),
    ("DATA", "Dividends paid on non-controlling interests", {"FY2020": -15}),
    ("DATA", "Principal elements of lease payments", {"FY2025": -22, "FY2024": -33, "FY2023": -47, "FY2022": -26, "FY2021": -25}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": 5410, "FY2024": 285, "FY2023": 19, "FY2022": 277, "FY2021": -10753, "FY2020": -8152}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2025": -431, "FY2024": -7586, "FY2023": -3861, "FY2022": -2891, "FY2021": 2575, "FY2020": 17720}),
    ("DATA", "Cash and cash equivalents at beginning of the year", {"FY2025": 29181, "FY2024": 36781, "FY2023": 46484, "FY2022": 49254, "FY2021": 46697, "FY2020": 27817}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2025": -12, "FY2024": -14, "FY2023": -121, "FY2022": 121, "FY2021": -18, "FY2020": 45}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 28738, "FY2024": 29181, "FY2023": 42502, "FY2022": 46484, "FY2021": 49254, "FY2020": 45582}),
    ("SECTION", "Cash and cash equivalents at the end of the year comprise", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 29376, "FY2024": 29881, "FY2023": 38214, "FY2022": 44190, "FY2021": 48139, "FY2020": 41250}),
    ("DATA", "Less: restricted balances", {"FY2025": -1440, "FY2024": -1580, "FY2023": -2311, "FY2022": -2223, "FY2021": -2498, "FY2020": -854}),
    ("DATA", "Other cash equivalents: loans and advances to banks - non-trading", {"FY2025": 802, "FY2024": 880, "FY2023": 878, "FY2022": 904, "FY2021": 1074, "FY2020": 5186}),
    ("DATA", "Other cash equivalents: reverse repurchase agreements", {"FY2023": 5721, "FY2022": 3613, "FY2021": 2539}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 28738, "FY2024": 29181, "FY2023": 42502, "FY2022": 46484, "FY2021": 49254, "FY2020": 45582}),
]

bw.add_cash_flow_sheet(
    title="Santander UK Plc — Consolidated Cash Flow Statement",
    subtitle="Santander UK Plc Group (consolidated basis), £m. See source note at bottom re: a cash-equivalents definition change.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=190,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Asset Quality - on-balance-sheet loans by IFRS 9 stage. FY2025/FY2024 use
# the Annual Report's 'Credit performance' Total Drawn table (own customer
# loan scope, £197.4bn/£194.5bn); FY2023-FY2021 use the 'Rating
# distribution' Loans and advances to customers table (£207.4bn/£219.7bn/
# £210.1bn) - a slightly different scope from each other and from the
# Balance Sheet's own broader Loans and advances to customers line
# (£202.6bn/£199.4bn/etc, which also includes accrued interest and other
# adjustments) - documented below, not forced to tie.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans by IFRS 9 stage (on-balance sheet, drawn)", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 177700, "FY2024": 171900, "FY2023": 182600, "FY2022": 199600, "FY2021": 191600, "FY2020": 189900}),
    ("DATA", "Stage 2 (underperforming / significant increase in credit risk)", {"FY2025": 17500, "FY2024": 20000, "FY2023": 22200, "FY2022": 17800, "FY2021": 16000, "FY2020": 16600}),
    ("DATA", "Stage 3 (credit-impaired / non-performing)", {"FY2025": 2200, "FY2024": 2600, "FY2023": 2600, "FY2022": 2300, "FY2021": 2500, "FY2020": 2300}),
    ("TOTAL", "Total loans in scope", {"FY2025": 197400, "FY2024": 194500, "FY2023": 207400, "FY2022": 219700, "FY2021": 210100, "FY2020": 208800}),
    ("SECTION", "Expected credit loss (ECL) allowance", {}),
    ("DATA", "Stage 1 ECL allowance", {"FY2023": 100, "FY2022": 100, "FY2021": 100, "FY2020": 200}),
    ("DATA", "Stage 2 ECL allowance", {"FY2023": 400, "FY2022": 500, "FY2021": 400, "FY2020": 500}),
    ("DATA", "Stage 3 ECL allowance", {"FY2023": 400, "FY2022": 300, "FY2021": 400, "FY2020": 600}),
    ("TOTAL", "Total ECL allowance", {"FY2025": 729, "FY2024": 784, "FY2023": 900, "FY2022": 900, "FY2021": 900, "FY2020": 1300}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 / NPL ratio (%)", {"FY2025": "1.18%", "FY2024": "1.42%", "FY2023": "1.25%", "FY2022": "1.05%", "FY2021": "1.19%", "FY2020": "1.45%"}),
    ("DATA", "ECL coverage ratio (Total ECL / Total loans in scope, %)", {"FY2025": "0.37%", "FY2024": "0.40%", "FY2023": "0.43%", "FY2022": "0.41%", "FY2021": "0.43%", "FY2020": "0.62%"}),
    ("DATA", "12-month gross write-offs (£m)", {"FY2025": 248, "FY2024": 230}),
]

bw.add_asset_quality_sheet(
    title="Santander UK Plc — Asset Quality",
    subtitle="Santander UK Plc Group (consolidated 'RFB Group' basis). On-balance-sheet, drawn loans within the "
              "IFRS 9 ECL framework, by stage. FY2025/FY2024 and FY2023-FY2021 use two related but non-identical "
              "disclosure tables (Total Drawn customer loans vs. Loans and advances to customers rating "
              "distribution) - see source note; FY2025/FY2024 don't disclose a Stage 1/2/3 ECL split (only a Total "
              "ECL allowance), so those cells are blank rather than estimated. FY2020's Stage 3/NPL ratio (1.45%) "
              "is the directly-disclosed 'Key metrics' figure (a slightly different denominator, including undrawn "
              "Stage 3 exposures, per the source table's own definition), consistent with how FY2025/FY2024's ratio "
              "is also directly reported rather than derived.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Santander UK Plc consolidated ('RFB Group') basis:\n"
        f"FY2025: Santander UK plc Annual Report 2025, p.67 ('Credit performance (audited)' table, Total Drawn "
        f"row) - {AR2025_URL}\n"
        f"FY2024: Santander UK plc Annual Report 2025, p.67 (FY2024 comparative in the same table) - {AR2025_URL}\n"
        f"FY2023: Santander UK plc Annual Report 2023, p.61 ('Rating distribution (audited)' table, Loans and "
        f"advances to customers row) - {AR2023_URL}\n"
        f"FY2022: Santander UK plc Annual Report 2023, p.62 (FY2022 comparative in the same rating distribution "
        f"table) - {AR2023_URL}\n"
        f"FY2021: Santander UK plc Annual Report 2022, p.65 ('Rating distribution (audited)' table, Loans and "
        f"advances to customers row) - {AR2022_URL}\n"
        f"FY2020: Santander UK plc Annual Report 2020, p.90-91 ('Rating distribution (audited)' table, Loans and "
        f"advances to customers row, and 'Key metrics' Stage 3 ratio) - {AR2020_URL}\n"
        "Presentation note: the FY2025/FY2024 table reports 'Total Drawn' customer loans (£197.4bn/£194.5bn), "
        "narrower than the FY2023-FY2021 table's 'Loans and advances to customers' on-balance-sheet scope "
        "(£207.4bn/£219.7bn/£210.1bn) and narrower still than the Balance Sheet's own broader Loans and advances "
        "to customers line (which includes accrued interest and other adjustments not captured in either credit-"
        "risk table) - each year's own as-disclosed figure is used rather than forced to tie across scopes. Stage "
        "3/NPL ratio and ECL coverage ratio are derived from the figures above (Stage 3 ratio for FY2025/FY2024 is "
        "as directly reported in the source table, which uses a slightly different denominator including undrawn "
        "Stage 3 exposures - see the table's own footnote).\n\n" + ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=250,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"RFB Group consolidated basis, {unit}" if unit else "RFB Group consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=110)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 10601, "FY2024": 9791, "FY2023": 10443, "FY2022": 10799, "FY2021": 10820, "FY2020": 11057})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "15.8%", "FY2024": "14.9%", "FY2023": "15.39%", "FY2022": "15.41%", "FY2021": "16.1%", "FY2020": "15.4%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 12461, "FY2024": 11651, "FY2023": 12399, "FY2022": 12755, "FY2021": 12939, "FY2020": 13338})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "18.5%", "FY2024": "17.8%", "FY2023": "18.28%", "FY2022": "18.20%", "FY2021": "19.2%", "FY2020": "18.6%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 14315, "FY2024": 13744, "FY2023": 14571, "FY2022": 14303, "FY2021": 14755, "FY2020": 15247})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "21.3%", "FY2024": "21.0%", "FY2023": "21.48%", "FY2022": "20.41%", "FY2021": "21.9%", "FY2020": "21.2%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 67231, "FY2024": 65528, "FY2023": 67839, "FY2022": 70089, "FY2021": 67148, "FY2020": 71860})],
    p3_sources(),
)

# ---------------------------------------------------------------
# RWA Breakdown - Pillar 3 UK OV1 template (Part 2: Santander UK plc Group /
# RFB Group basis). FY2021 uses an older CRR-era structure with a separate
# CVA line (folded into Counterparty credit risk from FY2022 onward); each
# category row sums exactly to that year's own OV1 Total, which is a small
# rounding difference (£bn precision) from the exact KM1-sourced Total RWAs
# metric above - documented, not forced to tie. FY2022's category split was
# recovered from a December 2022 ACRMD document found via Wayback Machine's
# CDX index (filename santander_uk_additional_capital_and_risk_management_
# disclosures_2022.pdf - not the same naming pattern as the other years'
# ACRMD files, which is why the earlier session missed it) - still live at
# its original URL as of this session. Its Part 2 OV1 table (p.66) sums to
# 69.9bn against its own disclosed 70.1bn Total (a 0.2bn rounding gap the
# document's own footnote attributes to "balances not visible due to
# rounding"), consistent with the same small-rounding pattern seen in the
# other years' columns here.
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (Pillar 3 UK OV1 template; FY2021 and FY2020 use an older CRR-era structure "
                "with a separate CVA line - see source note)", {}),
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2025": 55700, "FY2024": 54700, "FY2023": 57900, "FY2022": 61700, "FY2021": 58500, "FY2020": 62800}),
    ("DATA", "Counterparty credit risk", {"FY2025": 600, "FY2024": 400, "FY2023": 600, "FY2022": 400, "FY2021": 600, "FY2020": 800}),
    ("DATA", "Credit valuation adjustment (CVA)", {"FY2021": 400, "FY2020": 300}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2025": 3100, "FY2024": 2500, "FY2023": 1200, "FY2022": 400, "FY2021": 800, "FY2020": 900}),
    ("DATA", "Position, foreign exchange and commodities risk (market risk)", {"FY2025": 200, "FY2024": 200, "FY2023": 400, "FY2022": 300, "FY2021": 200, "FY2020": 200}),
    ("DATA", "Operational risk", {"FY2025": 7700, "FY2024": 7800, "FY2023": 7700, "FY2022": 7100, "FY2021": 6600, "FY2020": 6800}),
    ("TOTAL", "Total RWAs", {"FY2025": 67300, "FY2024": 65600, "FY2023": 67800, "FY2022": 70100, "FY2021": 67100, "FY2020": 71900}),
]

bw.add_rwa_breakdown_sheet(
    title="Santander UK Plc — RWA Breakdown",
    subtitle="Santander UK Plc Group (consolidated 'RFB Group' basis), £m. Category rows sum exactly to each "
              "year's own OV1 Total, a small rounding difference (OV1 is disclosed to £0.1bn precision) from the "
              "exact Total RWAs metric sourced from the KM1 table elsewhere in this workbook - FY2022 has a "
              "slightly larger 0.2bn gap that its own source document attributes to rounding, and FY2020 has a "
              "0.1bn gap from an 'Equity positions under the simple risk weight approach' OV1 line not separately "
              "categorised here (see source note).",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Sources - Santander UK Plc consolidated ('RFB Group') basis, Part 2 of the ACRMD document, UK OV1: "
        "Overview of risk-weighted exposure amounts:\n"
        f"FY2025: Santander UK Group Holdings plc and Santander UK plc ACRMD, 31 December 2025, p.58 (UK OV1, "
        f"Part 2: Santander UK plc Group) - {ACRMD2025_URL}\n"
        f"FY2024: Santander UK Group Holdings plc and Santander UK plc ACRMD, 31 December 2024, p.59 (UK OV1, "
        f"Part 2: Santander UK plc Group) - {ACRMD2024_URL}\n"
        f"FY2023: Santander UK Group Holdings plc and Santander UK plc ACRMD, 31 December 2023, p.59 (UK OV1, "
        f"Part 2: Santander UK plc Group) - {ACRMD2023_URL}\n"
        f"FY2022: Santander UK plc Additional Capital and Risk Management Disclosures, 31 December 2022, p.66 (UK "
        f"OV1, Part 2: December 2022 Additional Capital and Risk Management Disclosures for Santander UK plc "
        f"Group) - {ACRMD2022_URL}. This file uses a different naming convention "
        f"(santander_uk_additional_capital_and_risk_management_disclosures_2022.pdf) than the adjacent years' "
        f"ACRMD files, which is why an earlier session's search missed it; located via the Wayback Machine's CDX "
        f"index of the site's documents folder, and confirmed still live at its original URL as of this session. "
        f"Its own Total RWAs row (70.1bn) reconciles to the KM1-sourced Total risk-weighted exposure amount used "
        f"in the Total RWAs metric sheet elsewhere in this workbook (70,089 -> 70.1bn at OV1's £0.1bn precision).\n"
        f"FY2021: Santander UK Group Holdings plc and Santander UK plc ACRMD, 31 December 2021, p.45 (Overview of "
        f"RWA (OV1), Part 2: Santander UK plc Group) - {ACRMD2021_URL}\n"
        f"FY2020: Santander UK plc ACRMD, 31 December 2020, p.45 (Overview of RWA (OV1), Part 2: December 2020 "
        f"Additional Capital and Risk Management Disclosures for Santander UK plc Group) - {ACRMD2020_URL}. Its "
        f"own Total row (71.9bn) reconciles closely to the KM1-sourced Total risk-weighted exposure amount used in "
        f"the Total RWAs metric sheet elsewhere in this workbook (71,860 -> 71.9bn at OV1's £0.1bn precision); the "
        f"six categories shown here sum to 71.8bn, a 0.1bn gap the source table attributes to a separate 'Equity "
        f"positions under the simple risk weight approach' line (£0.1bn) not large enough to warrant its own row.\n"
        "FY2021 and FY2020's tables use an older CRR-era category structure with Credit Valuation Adjustment (CVA) "
        "reported as its own top-level line rather than folded into Counterparty credit risk (as it is from FY2022 "
        "onward) - shown here as its own row for those two years only, blank otherwise.\n\n" + ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=230,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 247722, "FY2024": 238445, "FY2023": 242900, "FY2022": 244000, "FY2021": 242100, "FY2020": 254600}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "5.0%", "FY2024": "4.9%", "FY2023": "5.1%", "FY2022": "5.2%", "FY2021": "5.3%", "FY2020": "5.1%"}),
        ("Leverage ratio including claims on central banks (%)", {"FY2025": "4.5%", "FY2024": "4.3%", "FY2023": "4.4%", "FY2022": "4.4%", "FY2021": "4.3%", "FY2020": "4.3%"}),
    ],
    p3_sources(),
    note="FY2021 and FY2020's exposure measure/ratio ('UK1' basis, excluding claims on central banks per FPC "
         "recommendation) and the 'UK CRR' basis (including them; FY2021 293,800/4.3%, FY2020 299,900/4.3%) come "
         "from a differently-labelled table than FY2022 onward (which use the standardised 'UK KM1' template "
         "naming) - shown here on a consistent excluding/including basis for comparability.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 46888, "FY2024": 43681, "FY2023": 47824, "FY2022": 46160, "FY2021": 51266, "FY2020": 51232}),
        ("Total net cash outflows, adjusted value", {"FY2025": 28951, "FY2024": 28323, "FY2023": 29985, "FY2022": 29448, "FY2021": 30439, "FY2020": 33766}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "162%", "FY2024": "154%", "FY2023": "159.49%", "FY2022": "156.75%", "FY2021": "168.4%", "FY2020": "151.7%"}),
    ],
    p3_sources(),
    note="LCR is a 12-month simple average of month-end observations.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2025": 211913, "FY2024": 208000, "FY2023": 218975, "FY2022": 233408}),
        ("Total required stable funding", {"FY2025": 156768, "FY2024": 151457, "FY2023": 158693, "FY2022": 170615}),
        ("NSFR ratio (%)", {"FY2025": "135%", "FY2024": "137%", "FY2023": "137.99%", "FY2022": "136.80%", "FY2021": "Not disclosed", "FY2020": "Not disclosed"}),
    ],
    p3_sources(),
    note="NSFR was not a UK Pillar 3 disclosure requirement as at FY2021 or FY2020 (the UK NSFR regime took effect "
         "from 1 January 2022), so no FY2021/FY2020 figures are available.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed at this level" for y in YEARS})],
    p3_sources(),
    note="MREL (Minimum Requirement for own funds and Eligible Liabilities) is disclosed at the resolution-entity "
         "level - 'Santander UK Group Holdings plc' (the intermediate holding company) - not at Santander UK Plc's "
         "own 'RFB Group' level shown throughout the rest of this workbook. As at 31 December 2025, Santander UK "
         "Group Holdings plc's Total Own Funds and Eligible Liabilities were 36.1% of RWA / 9.8% of UK leverage "
         "exposure measure (ACRMD 2025, p.6 (Key metrics - MREL (KM2))).",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 266837, "FY2024": 259944, "FY2023": 275448, "FY2022": 285213, "FY2021": 287098, "FY2020": 292332}),
        ("Loans and advances to customers", {"FY2025": 202609, "FY2024": 199408, "FY2023": 207435, "FY2022": 219716, "FY2021": 210094, "FY2020": 208750}),
        ("Deposits by customers", {"FY2025": 187300, "FY2024": 180967, "FY2023": 190850, "FY2022": 195568, "FY2021": 192926, "FY2020": 195135}),
        ("Total equity", {"FY2025": 15148, "FY2024": 13773, "FY2023": 14623, "FY2022": 14407, "FY2021": 16102, "FY2020": 15936}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 4729, "FY2024": 4657, "FY2023": 5096, "FY2022": 4956, "FY2021": 4499, "FY2020": 3975}),
        ("Operating expenses before impairment, provisions and charges", {"FY2025": -2457, "FY2024": -2548, "FY2023": -2456, "FY2022": -2343, "FY2021": -2510, "FY2020": -2452}),
        ("Profit after tax", {"FY2025": 1086, "FY2024": 971, "FY2023": 1541, "FY2022": 1394, "FY2021": 1384, "FY2020": 471}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 13773, "FY2024": 14623, "FY2023": 14407, "FY2022": 16102, "FY2021": 15936, "FY2020": 16017}),
        ("Total comprehensive income/(expense)", {"FY2025": 1532, "FY2024": 690, "FY2023": 1868, "FY2022": -296, "FY2021": 1852, "FY2020": 211}),
        ("Other equity movements, net", {"FY2025": -157, "FY2024": -1540, "FY2023": -1652, "FY2022": -1399, "FY2021": -1686, "FY2020": -292}),
        ("Closing equity", {"FY2025": 15148, "FY2024": 13773, "FY2023": 14623, "FY2022": 14407, "FY2021": 16102, "FY2020": 15936}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash flows from operating activities", {"FY2025": -8798, "FY2024": -3331, "FY2023": -1133, "FY2022": -2970, "FY2021": 10251, "FY2020": 19236}),
        ("Net cash flows from investing activities", {"FY2025": 2957, "FY2024": -4540, "FY2023": -2747, "FY2022": -198, "FY2021": 3077, "FY2020": 6636}),
        ("Net cash flows from financing activities", {"FY2025": 5410, "FY2024": 285, "FY2023": 19, "FY2022": 277, "FY2021": -10753, "FY2020": -8152}),
        ("Cash and cash equivalents at end of year", {"FY2025": 28738, "FY2024": 29181, "FY2023": 42502, "FY2022": 46484, "FY2021": 49254, "FY2020": 45582}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.8%", "FY2024": "14.9%", "FY2023": "15.39%", "FY2022": "15.41%", "FY2021": "16.1%", "FY2020": "15.4%"}),
        ("Tier 1 Ratio", {"FY2025": "18.5%", "FY2024": "17.8%", "FY2023": "18.28%", "FY2022": "18.20%", "FY2021": "19.2%", "FY2020": "18.6%"}),
        ("Total Capital Ratio", {"FY2025": "21.3%", "FY2024": "21.0%", "FY2023": "21.48%", "FY2022": "20.41%", "FY2021": "21.9%", "FY2020": "21.2%"}),
        ("Leverage Ratio", {"FY2025": "5.0%", "FY2024": "4.9%", "FY2023": "5.1%", "FY2022": "5.2%", "FY2021": "5.3%", "FY2020": "5.1%"}),
        ("LCR", {"FY2025": "162%", "FY2024": "154%", "FY2023": "159.49%", "FY2022": "156.75%", "FY2021": "168.4%", "FY2020": "151.7%"}),
        ("NSFR", {"FY2025": "135%", "FY2024": "137%", "FY2023": "137.99%", "FY2022": "136.80%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. See the Cash Flow Statement sheet's note re: Santander's "
         "pending acquisition of TSB Bank plc (announced 21 July 2025, not yet completed as at the FY2025 "
         "reporting date) - a bank also covered elsewhere in this workbook series.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/SANTANDER FINANCIALS.xlsx")
