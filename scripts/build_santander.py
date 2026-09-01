import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR2025_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/SantanderUKplc2025AnnualReport.pdf"
AR2023_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/santander_uk_plc_annual_report_2023.pdf"

ACRMD2025_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/2025SantanderUKACRMD.pdf"
ACRMD2023_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/santander_uk_acrmd_2023.pdf"
ACRMD2021_URL = "https://www.santander.co.uk/assets/s3fs-public/documents/2021_additional_capital_risk_management_disclosures.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Santander UK Plc (FRN 106054, company number 02294747) is the PRA-authorised ring-fenced bank "
    "(RFB) - not to be confused with 'Santander Financial Services plc' (FRN 146003, a separate, smaller PRA-"
    "authorised entity) or with its own intermediate holding company 'Santander UK Group Holdings plc' (the "
    "resolution entity, which publishes its own separate Annual Report/Pillar 3). This workbook uses Santander UK "
    "Plc's own consolidated ('RFB Group') basis throughout, consistent with how this workbook series always prefers "
    "the ring-fenced/regulated banking entity's own consolidation level over a wider holding company - matching "
    "Barclays' use of 'Barclays Bank UK Group' rather than 'Barclays PLC'."
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
    "Note: Santander UK redefined the composition of 'cash and cash equivalents' between these report vintages - "
    "the FY2023 annual report (used for the FY2023/FY2022/FY2021 columns here) includes 'Reverse repurchase "
    "agreements' as a component of cash equivalents, while the FY2025 annual report's presentation (used for the "
    "FY2025/FY2024 columns) does not. Each column above uses that year's own report's original presentation rather "
    "than a later restated comparative, so FY2023's closing cash balance (42,502) will not tie directly to the "
    "FY2024 column's opening balance as shown in the FY2025 report (36,781) - the £5,721m difference is exactly the "
    "FY2023 reverse-repo balance reclassified out of cash equivalents. Operating/investing/financing subtotals and "
    "the change-in-cash reconciliation are internally consistent within each year shown.\n\n"
    + ENTITY_NOTE + "\n\n" + TSB_ACQUISITION_NOTE
)


def p3_sources(page_25="47-48", page_23="47-48", page_21="42"):
    return (
        "Sources - Santander UK Plc's own consolidated ('RFB Group') basis, from the Additional Capital and Risk "
        "Management Disclosures (ACRMD, Santander UK's Pillar 3 equivalent document):\n"
        f"FY2025 & FY2024: Santander UK Group Holdings plc and Santander UK plc - Additional Capital and Risk "
        f"Management Disclosures, 31 December 2025, p.{page_25} (Key metrics (KM1), RFB Group) - {ACRMD2025_URL}\n"
        f"FY2023 & FY2022: Santander UK Group Holdings plc and Santander UK plc - Additional Capital and Risk "
        f"Management Disclosures, 31 December 2023, p.{page_23} (Key metrics (KM1), RFB Group) - {ACRMD2023_URL}\n"
        f"FY2021: Santander UK Group Holdings plc and Santander UK plc - Additional Capital and Risk Management "
        f"Disclosures, 31 December 2021, p.{page_21} (Key metrics (KM1), RFB Group) - {ACRMD2021_URL}"
    )


bw = BankWorkbook(bank_name="Santander UK Plc", years=YEARS, header_color="EC0000")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 1482, "FY2024": 1349, "FY2023": 2100, "FY2022": 1874, "FY2021": 1888}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 322, "FY2024": 300, "FY2023": 290, "FY2022": 296, "FY2021": 501}),
    ("DATA", "Loss from disposal of mortgage portfolio", {"FY2024": 31}),
    ("DATA", "Provisions for other liabilities and charges", {"FY2025": 597, "FY2024": 689, "FY2023": 335, "FY2022": 419, "FY2021": 381}),
    ("DATA", "Impairment losses", {"FY2025": 207, "FY2024": 94, "FY2023": 195, "FY2022": 284, "FY2021": -228}),
    ("DATA", "Other non-cash items", {"FY2025": -4, "FY2024": 65, "FY2023": -749, "FY2022": 1497, "FY2021": -147}),
    ("DATA", "Pension charge for defined benefit pension schemes", {"FY2025": 8, "FY2024": 13, "FY2023": 13, "FY2022": 28, "FY2021": 38}),
    ("SECTION", "Net change in operating assets and liabilities", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 140, "FY2024": 731, "FY2023": -88, "FY2022": 275, "FY2021": -659}),
    ("DATA", "Derivative assets", {"FY2025": 334, "FY2024": 228, "FY2023": 975, "FY2022": -726, "FY2021": 1725}),
    ("DATA", "Other financial assets at fair value through profit or loss", {"FY2025": 72, "FY2024": 130, "FY2023": 40, "FY2022": 877, "FY2021": 1007}),
    ("DATA", "Loans and advances to banks and customers", {"FY2025": -3403, "FY2024": 8065, "FY2023": 12112, "FY2022": -9966, "FY2021": -971}),
    ("DATA", "Reverse repurchase agreements - non-trading", {"FY2025": -7340, "FY2024": 2130, "FY2023": -3224, "FY2022": 6818, "FY2021": 7024}),
    ("DATA", "Other assets", {"FY2025": -70, "FY2024": 118, "FY2023": -141, "FY2022": -574, "FY2021": 324}),
    ("DATA", "Deposits by banks and customers", {"FY2025": -1130, "FY2024": -16059, "FY2023": -13504, "FY2022": -3128, "FY2021": 10735}),
    ("DATA", "Repurchase agreements - non-trading", {"FY2025": 412, "FY2024": 206, "FY2023": 704, "FY2022": -4145, "FY2021": -7550}),
    ("DATA", "Derivative liabilities", {"FY2025": -15, "FY2024": -116, "FY2023": -133, "FY2022": 174, "FY2021": -807}),
    ("DATA", "Other financial liabilities at fair value through profit or loss", {"FY2025": 241, "FY2024": 179, "FY2023": 102, "FY2022": -973, "FY2021": -1109}),
    ("DATA", "Debt securities in issue", {"FY2025": 38, "FY2024": 212, "FY2023": 962, "FY2022": 3120, "FY2021": -329}),
    ("DATA", "Other liabilities", {"FY2025": -299, "FY2024": -1403, "FY2023": -67, "FY2022": -98, "FY2021": -603}),
    ("DATA", "Corporation taxes paid", {"FY2025": -46, "FY2024": -240, "FY2023": -537, "FY2022": -405, "FY2021": -427}),
    ("DATA", "Effects of exchange rate differences", {"FY2025": -344, "FY2024": -53, "FY2023": -518, "FY2022": 1383, "FY2021": -542}),
    ("TOTAL", "Net cash flows from operating activities", {"FY2025": -8798, "FY2024": -3331, "FY2023": -1133, "FY2022": -2970, "FY2021": 10251}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment and intangible assets", {"FY2025": -407, "FY2024": -528, "FY2023": -385, "FY2022": -496, "FY2021": -613}),
    ("DATA", "Proceeds from sale of property, plant and equipment and intangible assets", {"FY2025": 161, "FY2024": 148, "FY2023": 175, "FY2022": 159, "FY2021": 437}),
    ("DATA", "Purchase of financial assets at amortised cost and financial assets at FVOCI", {"FY2025": -1981, "FY2024": -10343, "FY2023": -10899, "FY2022": -2884, "FY2021": -1256}),
    ("DATA", "Proceeds from sale and redemption of financial assets at amortised cost and financial assets at FVOCI", {"FY2025": 5184, "FY2024": 6183, "FY2023": 8362, "FY2022": 3023, "FY2021": 4509}),
    ("TOTAL", "Net cash flows from investing activities", {"FY2025": 2957, "FY2024": -4540, "FY2023": -2747, "FY2022": -198, "FY2021": 3077}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Issue of other equity instruments", {"FY2025": 500, "FY2024": 400, "FY2022": 750, "FY2021": 210}),
    ("DATA", "Issue of debt securities and subordinated notes", {"FY2025": 9833, "FY2024": 8425, "FY2023": 5276, "FY2022": 4794, "FY2021": 2878}),
    ("DATA", "Issuance costs of debt securities and subordinated notes", {"FY2025": -24, "FY2024": -28, "FY2023": -18, "FY2022": -16, "FY2021": -6}),
    ("DATA", "Repayment of debt securities and subordinated notes", {"FY2025": -4219, "FY2024": -6539, "FY2023": -3539, "FY2022": -3076, "FY2021": -11914}),
    ("DATA", "Disposal of non-controlling interests", {"FY2021": -181}),
    ("DATA", "Repurchase of other equity instruments", {"FY2025": -500, "FY2024": -500, "FY2022": -985, "FY2021": -210}),
    ("DATA", "Dividends paid on ordinary shares", {"FY2025": -26, "FY2024": -1311, "FY2023": -1530, "FY2022": -1014, "FY2021": -1358}),
    ("DATA", "Dividends paid on preference shares and other equity instruments", {"FY2025": -132, "FY2024": -129, "FY2023": -123, "FY2022": -150, "FY2021": -147}),
    ("DATA", "Principal elements of lease payments", {"FY2025": -22, "FY2024": -33, "FY2023": -47, "FY2022": -26, "FY2021": -25}),
    ("TOTAL", "Net cash flows from financing activities", {"FY2025": 5410, "FY2024": 285, "FY2023": 19, "FY2022": 277, "FY2021": -10753}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2025": -431, "FY2024": -7586, "FY2023": -3861, "FY2022": -2891, "FY2021": 2575}),
    ("DATA", "Cash and cash equivalents at beginning of the year", {"FY2025": 29181, "FY2024": 36781, "FY2023": 46484, "FY2022": 49254, "FY2021": 46697}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2025": -12, "FY2024": -14, "FY2023": -121, "FY2022": 121, "FY2021": -18}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 28738, "FY2024": 29181, "FY2023": 42502, "FY2022": 46484, "FY2021": 49254}),
    ("SECTION", "Cash and cash equivalents at the end of the year comprise", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 29376, "FY2024": 29881, "FY2023": 38214, "FY2022": 44190, "FY2021": 48139}),
    ("DATA", "Less: restricted balances", {"FY2025": -1440, "FY2024": -1580, "FY2023": -2311, "FY2022": -2223, "FY2021": -2498}),
    ("DATA", "Other cash equivalents: loans and advances to banks - non-trading", {"FY2025": 802, "FY2024": 880, "FY2023": 878, "FY2022": 904, "FY2021": 1074}),
    ("DATA", "Other cash equivalents: reverse repurchase agreements", {"FY2023": 5721, "FY2022": 3613, "FY2021": 2539}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 28738, "FY2024": 29181, "FY2023": 42502, "FY2022": 46484, "FY2021": 49254}),
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
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"RFB Group consolidated basis, {unit}" if unit else "RFB Group consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=110)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 10601, "FY2024": 9791, "FY2023": 10443, "FY2022": 10799, "FY2021": 10820})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "15.8%", "FY2024": "14.9%", "FY2023": "15.39%", "FY2022": "15.41%", "FY2021": "16.1%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 12461, "FY2024": 11651, "FY2023": 12399, "FY2022": 12755, "FY2021": 12939})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "18.5%", "FY2024": "17.8%", "FY2023": "18.28%", "FY2022": "18.20%", "FY2021": "19.2%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 14315, "FY2024": 13744, "FY2023": 14571, "FY2022": 14303, "FY2021": 14755})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "21.3%", "FY2024": "21.0%", "FY2023": "21.48%", "FY2022": "20.41%", "FY2021": "21.9%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 67231, "FY2024": 65528, "FY2023": 67839, "FY2022": 70089, "FY2021": 67148})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 247722, "FY2024": 238445, "FY2023": 242900, "FY2022": 244000, "FY2021": 242100}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "5.0%", "FY2024": "4.9%", "FY2023": "5.1%", "FY2022": "5.2%", "FY2021": "5.3%"}),
        ("Leverage ratio including claims on central banks (%)", {"FY2025": "4.5%", "FY2024": "4.3%", "FY2023": "4.4%", "FY2022": "4.4%", "FY2021": "4.3%"}),
    ],
    p3_sources(),
    note="FY2021's exposure measure/ratio ('UK1' basis, excluding claims on central banks per FPC recommendation) "
         "and the 'UK CRR' basis (including them, 293,800/4.3%) come from a differently-labelled table than "
         "FY2022 onward (which use the standardised 'UK KM1' template naming) - shown here on a consistent "
         "excluding/including basis for comparability.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 46888, "FY2024": 43681, "FY2023": 47824, "FY2022": 46160, "FY2021": 51266}),
        ("Total net cash outflows, adjusted value", {"FY2025": 28951, "FY2024": 28323, "FY2023": 29985, "FY2022": 29448, "FY2021": 30439}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "162%", "FY2024": "154%", "FY2023": "159.49%", "FY2022": "156.75%", "FY2021": "168.4%"}),
    ],
    p3_sources(),
    note="LCR is a 12-month simple average of month-end observations.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2025": 211913, "FY2024": 208000, "FY2023": 218975, "FY2022": 233408}),
        ("Total required stable funding", {"FY2025": 156768, "FY2024": 151457, "FY2023": 158693, "FY2022": 170615}),
        ("NSFR ratio (%)", {"FY2025": "135%", "FY2024": "137%", "FY2023": "137.99%", "FY2022": "136.80%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note="NSFR was not a UK Pillar 3 disclosure requirement as at FY2021 (the UK NSFR regime took effect from 1 "
         "January 2022), so no FY2021 figures are available.",
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
    cash_flow_totals=[
        ("Net cash flows from operating activities", {"FY2025": -8798, "FY2024": -3331, "FY2023": -1133, "FY2022": -2970, "FY2021": 10251}),
        ("Net cash flows from investing activities", {"FY2025": 2957, "FY2024": -4540, "FY2023": -2747, "FY2022": -198, "FY2021": 3077}),
        ("Net cash flows from financing activities", {"FY2025": 5410, "FY2024": 285, "FY2023": 19, "FY2022": 277, "FY2021": -10753}),
        ("Cash and cash equivalents at end of year", {"FY2025": 28738, "FY2024": 29181, "FY2023": 42502, "FY2022": 46484, "FY2021": 49254}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.8%", "FY2024": "14.9%", "FY2023": "15.39%", "FY2022": "15.41%", "FY2021": "16.1%"}),
        ("Tier 1 Ratio", {"FY2025": "18.5%", "FY2024": "17.8%", "FY2023": "18.28%", "FY2022": "18.20%", "FY2021": "19.2%"}),
        ("Total Capital Ratio", {"FY2025": "21.3%", "FY2024": "21.0%", "FY2023": "21.48%", "FY2022": "20.41%", "FY2021": "21.9%"}),
        ("Leverage Ratio", {"FY2025": "5.0%", "FY2024": "4.9%", "FY2023": "5.1%", "FY2022": "5.2%", "FY2021": "5.3%"}),
        ("LCR", {"FY2025": "162%", "FY2024": "154%", "FY2023": "159.49%", "FY2022": "156.75%", "FY2021": "168.4%"}),
        ("NSFR", {"FY2025": "135%", "FY2024": "137%", "FY2023": "137.99%", "FY2022": "136.80%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. See the Cash Flow Statement sheet's note re: Santander's "
         "pending acquisition of TSB Bank plc (announced 21 July 2025, not yet completed as at the FY2025 "
         "reporting date) - a bank also covered elsewhere in this workbook series.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/SANTANDER FINANCIALS.xlsx")
