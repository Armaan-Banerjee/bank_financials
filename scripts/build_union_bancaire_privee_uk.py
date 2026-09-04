import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {year: year for year in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history"
P3_ARCHIVE_URL = "https://www.ubp.com/en/legal-aspects/union-bancaire-privee-uk-limited/pillar-3-disclosure"
P3_2024_URL = "https://www.ubp.com/files/live/sites/ubp/files/documents/legal/ubp-uk/SGKH_2024-P3-disclosures.pdf"
P3_2023_URL = "https://www.ubp.com/files/live/sites/ubp/files/documents/legal/ubp-uk/UBP_2023_P3_disclosures.pdf"
P3_2022_URL = "https://www.ubp.com/files/live/sites/ubp/files/documents/legal/ubp-uk/UBP_2022_P3_disclosures.pdf"

AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzQ4Mjg5Njk3OWFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzQyNTQxNTkxNWFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzM5NTQ1NTI3NGFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzM1MzcxNDM1MGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Union Bancaire Privée (UK) Limited (Companies House "
    "00964058; FRN 119250) was formerly SG Kleinwort Hambros Bank Limited. "
    "The 2022-2024 Pillar 3 reports retain the SGKH name because they cover "
    "pre-acquisition periods. All figures use the reports' UK Consolidation "
    "Group basis, incorporating SGKH Bank Ltd, its branches, and the trust "
    "entity; they are not bank-solo figures. The reports state that the "
    "published financial statements use FRS 101 and differ from the prudential "
    "scope of consolidation."
)

P3_SOURCES = (
    "Sources - UK Consolidation Group Pillar 3 disclosures, amounts converted "
    "from £'000 to £m; ratios retained as reported:\n"
    f"FY2024: SGKH Pillar 3 Disclosure 31 December 2024, UK KM1 p.10 (FY2024 "
    f"current and FY2023 comparative) - {P3_2024_URL}\n"
    f"FY2023: SGKH Pillar 3 Disclosure 31 December 2023, UK KM1 p.10 (FY2023 "
    f"current and FY2022 comparative) - {P3_2023_URL}\n"
    f"FY2022: SGKH Pillar 3 Disclosure 31 December 2022, UK KM1 p.10 (FY2022 "
    f"current and FY2021 comparative) - {P3_2022_URL}\n"
    f"Official UBP UK disclosure archive - {P3_ARCHIVE_URL}\n"
    "FY2025: no defensible UK Consolidation Group Pillar 3 disclosure found; "
    "left blank rather than substituted. Amounts are shown in £m for "
    "consistency with this project.\n"
    + ENTITY_NOTE
)

CASH_FLOW_SOURCES = (
    "CASH-FLOW EXEMPTION: the SGKH disclosures explain that the published "
    "financial statements use FRS 101 Reduced Disclosure Framework and do not "
    "consolidate the relevant subsidiaries, while prudential reporting uses "
    "the UK Consolidation Group scope. No standalone cash-flow statement is "
    "used in this Pillar-3-only workbook; no group or other-entity cash flows "
    f"are substituted. Companies House filing history: {CH_URL}\n"
    f"SGKH 2024 Pillar 3 disclosure, scope/basis discussion - {P3_2024_URL}\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(
    bank_name="Union Bancaire Privée (UK) Limited",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="355C7D",
)

STATEMENTS_SOURCES = (
    "Sources - Union Bancaire Privée (UK) Limited (formerly SG Kleinwort Hambros Bank Limited) "
    "statutory Companies House accounts, Company-only basis, £'000. Each year's own column was "
    "checked against the adjacent report's comparative column where available.\n"
    f"FY2024/FY2023 comparative: Full accounts made up to 31 December 2024 - {AR2024_URL}\n"
    f"FY2023/FY2022 comparative: Full accounts made up to 31 December 2023 - {AR2023_URL}\n"
    f"FY2022/FY2021 comparative: Full accounts made up to 31 December 2022 - {AR2022_URL} "
    "(this filing's own copy of the financial statements is truncated after Note 12 - Companies "
    "House bundled it with the SGKH Pillar 3 Disclosures document, which starts mid-filing; Note 14's "
    "credit-quality table for FY2022 is therefore sourced from the FY2023 filing's own FY2022 "
    "comparative column instead, not from this filing.)\n"
    f"FY2021/FY2020 comparative: Full accounts made up to 31 December 2021 - {AR2021_URL}\n\n"
    "FY2025 is blank throughout the Balance Sheet, Profit & Loss, Statement of Changes in Equity and "
    "Asset Quality sheets: no FY2025 statutory accounts have been filed at Companies House as of this "
    "workbook's build date (the FY2024 filing is the most recent).\n\n"
    + ENTITY_NOTE
    + "\n\nSTATEMENT STRUCTURE NOTE: the FY2024/FY2023 Statement of Profit and Loss uses a "
    "Revenue/Cost-of-Revenue-style presentation (Total operating income before administrative "
    "expenses) while FY2022/FY2021 present the same P&L with slightly different line labels "
    "(e.g. 'Interest income calculated using effective interest method' vs 'Interest income', "
    "'Gain on financial instruments at fair value' vs 'Loss on financial instruments at fair value' - "
    "sign follows the source, not relabelled). 'Gains on sales of investments' and an explicit "
    "'Undistributable reserves' Balance Sheet line only appear in some years; blank cells reflect a "
    "line genuinely absent from that year's own statement, not a gap."
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2024": 459161, "FY2023": 502104, "FY2022": 564799, "FY2021": 144684}),
    ("DATA", "Derivative assets", {"FY2024": 7409, "FY2023": 6993, "FY2022": 6360, "FY2021": 4817}),
    ("DATA", "Loans and advances to banks", {"FY2024": 143664, "FY2023": 124270, "FY2022": 181081, "FY2021": 28831}),
    ("DATA", "Loans and advances to customers", {"FY2024": 1667863, "FY2023": 1923638, "FY2022": 2355390, "FY2021": 1248614}),
    ("DATA", "Revaluation differences on portfolios hedged against interest rate risk", {"FY2024": -249, "FY2023": 634}),
    ("DATA", "Debt and investment securities", {"FY2024": 2410283, "FY2023": 1902435, "FY2022": 2036353, "FY2021": 761764}),
    ("DATA", "Shares in group undertakings", {"FY2024": 22114, "FY2023": 22415, "FY2022": 95040, "FY2021": 231352}),
    ("DATA", "Intangible assets", {"FY2024": 1908, "FY2023": 3067, "FY2022": 5023, "FY2021": 3469}),
    ("DATA", "Tangible assets", {"FY2024": 7923, "FY2023": 6180, "FY2022": 9284, "FY2021": 1205}),
    ("DATA", "Current income tax assets", {"FY2024": 2617, "FY2023": 0, "FY2022": 0, "FY2021": 887}),
    ("DATA", "Deferred income tax assets", {"FY2024": 11717, "FY2023": 12847, "FY2022": 10247, "FY2021": 2570}),
    ("DATA", "Pension asset", {"FY2024": 2934, "FY2023": 169, "FY2022": 521, "FY2021": 0}),
    ("DATA", "Trade and other receivables", {"FY2024": 28064, "FY2023": 25347, "FY2022": 27503, "FY2021": 20270}),
    ("TOTAL", "Total assets", {"FY2024": 4765408, "FY2023": 4530099, "FY2022": 5291601, "FY2021": 2448463}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2024": 61031, "FY2023": 68185, "FY2022": 87141, "FY2021": 1116}),
    ("DATA", "Customers' accounts", {"FY2024": 4329605, "FY2023": 3970768, "FY2022": 4654279, "FY2021": 1934968}),
    ("DATA", "Revaluation differences on portfolios hedged against interest rate risk", {"FY2024": -481, "FY2023": 2908}),
    ("DATA", "Derivative liabilities", {"FY2024": 5864, "FY2023": 6365, "FY2022": 5242, "FY2021": 5024}),
    ("DATA", "Current income tax liabilities", {"FY2024": 392, "FY2023": 2712, "FY2022": 89, "FY2021": 0}),
    ("DATA", "Deferred income tax liabilities", {"FY2024": 492, "FY2023": 69, "FY2022": 183, "FY2021": 0}),
    ("DATA", "Other liabilities", {"FY2024": 70263, "FY2023": 72669, "FY2022": 66326, "FY2021": 35454}),
    ("DATA", "Provisions for liabilities", {"FY2024": 1021, "FY2023": 1026, "FY2022": 1079, "FY2021": 8391}),
    ("TOTAL", "Total liabilities", {"FY2024": 4468187, "FY2023": 4124702, "FY2022": 4814339, "FY2021": 1984953}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2024": 265750, "FY2023": 328266, "FY2022": 328266, "FY2021": 328266}),
    ("DATA", "Share premium", {"FY2024": 0, "FY2023": 45500, "FY2022": 45500, "FY2021": 45500}),
    ("DATA", "Share-based payment reserves", {"FY2024": 5214, "FY2023": 5082, "FY2022": 4735, "FY2021": 2542}),
    ("DATA", "Undistributable reserves", {"FY2022": 42500, "FY2021": 42500}),
    ("DATA", "OCI reserves", {"FY2024": -13632, "FY2023": -19227, "FY2022": -30856, "FY2021": 3083}),
    ("DATA", "Retained earnings", {"FY2024": 39889, "FY2023": 45776, "FY2022": 87117, "FY2021": 41619}),
    ("TOTAL", "Equity attributable to owners of the Company", {"FY2024": 297221, "FY2023": 405397, "FY2022": 477262, "FY2021": 463510}),
    ("TOTAL", "Total liabilities and equity", {"FY2024": 4765408, "FY2023": 4530099, "FY2022": 5291601, "FY2021": 2448463}),
]
bw.add_balance_sheet_sheet(
    title="Union Bancaire Privée (UK) Limited — Balance Sheet",
    subtitle="Statement of Financial Position, Company-only basis, £'000. Blank cells indicate a line not presented that year; 0 indicates a line disclosed as nil.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=82,
    source_height=340,
    unit_suffix=" (£'000)",
)

income_statement_rows = [
    ("SECTION", "Interest", {}),
    ("DATA", "Interest income", {"FY2024": 238931, "FY2023": 227011, "FY2022": 78433, "FY2021": 29774}),
    ("DATA", "Interest expense", {"FY2024": -149685, "FY2023": -113785, "FY2022": -20695, "FY2021": -4372}),
    ("TOTAL", "Net interest income", {"FY2024": 89246, "FY2023": 113226, "FY2022": 57738, "FY2021": 25402}),
    ("SECTION", "Fees and commissions", {}),
    ("DATA", "Fee and commission income", {"FY2024": 53735, "FY2023": 53948, "FY2022": 45677, "FY2021": 42430}),
    ("DATA", "Fee and commission expense", {"FY2024": -1252, "FY2023": -1745, "FY2022": -988, "FY2021": -1054}),
    ("TOTAL", "Net fee and commission income", {"FY2024": 52483, "FY2023": 52203, "FY2022": 44689, "FY2021": 41376}),
    ("SECTION", "Other operating income", {}),
    ("DATA", "Gain/(loss) on financial instruments at fair value", {"FY2024": -11818, "FY2023": -1138, "FY2022": 6746, "FY2021": 4083}),
    ("DATA", "Other income/(expense)", {"FY2024": 88, "FY2023": 358, "FY2022": 1, "FY2021": 399}),
    ("DATA", "Gains on sales of investments", {"FY2024": 393, "FY2023": 0}),
    ("DATA", "Dividend income", {"FY2024": 12, "FY2023": 2383, "FY2022": 0, "FY2021": 25000}),
    ("TOTAL", "Total operating income", {"FY2024": 130404, "FY2023": 167032, "FY2022": 109174, "FY2021": 96260}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Administrative expenses", {"FY2024": -122303, "FY2023": -120040, "FY2022": -84000, "FY2021": -57258}),
    ("DATA", "Amortisation", {"FY2024": -1219, "FY2023": -1896, "FY2022": -1430, "FY2021": -1649}),
    ("DATA", "Depreciation", {"FY2024": -2335, "FY2023": -2369, "FY2022": -719, "FY2021": -248}),
    ("DATA", "(Increase)/decrease in expected credit loss provisions", {"FY2024": 5014, "FY2023": -2320, "FY2022": -639, "FY2021": -4288}),
    ("DATA", "Other provisions", {"FY2024": -352, "FY2023": -673, "FY2022": -1233, "FY2021": -1158}),
    ("TOTAL", "Total operating expenses", {"FY2024": -121195, "FY2023": -127298, "FY2022": -88021, "FY2021": -64601}),
    ("TOTAL", "Profit before income tax", {"FY2024": 9209, "FY2023": 39734, "FY2022": 21153, "FY2021": 31659}),
    ("DATA", "Income tax (expense)/credit", {"FY2024": -555, "FY2023": -4495, "FY2022": -3389, "FY2021": -1208}),
    ("TOTAL", "Profit for the year", {"FY2024": 8654, "FY2023": 35239, "FY2022": 17764, "FY2021": 30451}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income for the year, net of tax", {"FY2024": 5151, "FY2023": 12549, "FY2022": -14588, "FY2021": -4587}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2024": 13805, "FY2023": 47788, "FY2022": 3176, "FY2021": 25864}),
]
bw.add_income_statement_sheet(
    title="Union Bancaire Privée (UK) Limited — Profit & Loss",
    subtitle="Statement of Profit and Loss / Statement of Comprehensive Income, Company-only basis, £'000. All results derived from continuing operations, entirely attributable to owners of the Company.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=82,
    source_height=340,
    unit_suffix=" (£'000)",
)

equity_headers = ["Share capital", "Share premium", "Share-based payment reserve", "Undistributable reserves", "OCI reserves", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2021", (328266, 45500, 2502, 42500, 7670, 11168, 437606)),
    ("DATA", "Total comprehensive income/(expense) (FY2021)", (None, None, None, None, -4587, 30451, 25864)),
    ("DATA", "Equity settled payments (FY2021)", (None, None, 40, None, None, None, 40)),
    ("TOTAL", "At 31 December 2021", (328266, 45500, 2542, 42500, 3083, 41619, 463510)),
    ("DATA", "Total comprehensive income/(expense) (FY2022)", (None, None, None, None, -14588, 17764, 3176)),
    ("DATA", "Transfer of net assets from SGKHCIL (Note 30, FY2022)", (None, None, 1913, None, -18670, 22529, 5772)),
    ("DATA", "Transfer of net assets from SGKHGL (Note 30, FY2022)", (None, None, None, None, -681, 5205, 4524)),
    ("DATA", "Equity settled payments (FY2022)", (None, None, 280, None, None, None, 280)),
    ("TOTAL", "At 31 December 2022", (328266, 45500, 4735, 42500, -30856, 87117, 477262)),
    ("DATA", "Total comprehensive income/(expense) (FY2023)", (None, None, None, None, 12549, 35239, 47788)),
    ("DATA", "Transfer of undistributable reserves to retained earnings (Note 24, FY2023)", (None, None, None, -42500, None, 42500, 0)),
    ("DATA", "Transfer from reserves (FY2023)", (None, None, None, None, -920, 920, 0)),
    ("DATA", "Equity settled payments (FY2023)", (None, None, 347, None, None, None, 347)),
    ("DATA", "Dividends paid (FY2023)", (None, None, None, None, None, -120000, -120000)),
    ("TOTAL", "At 31 December 2023", (328266, 45500, 5082, 0, -19227, 45776, 405397)),
    ("DATA", "Total comprehensive income/(expense) (FY2024)", (None, None, None, None, 5151, 8654, 13805)),
    ("DATA", "Transfer from reserves (FY2024)", (None, None, None, None, 444, -444, 0)),
    ("DATA", "Equity settled payments (FY2024)", (None, None, 132, None, None, None, 132)),
    ("DATA", "Capital repayment (FY2024)", (-62516, -27484, None, None, None, None, -90000)),
    ("DATA", "Cancellation of share premium (FY2024)", (None, -18016, None, None, None, 18016, 0)),
    ("DATA", "Dividends paid (FY2024)", (None, None, None, None, None, -32113, -32113)),
    ("TOTAL", "At 31 December 2024", (265750, 0, 5214, 0, -13632, 39889, 297221)),
]
bw.add_equity_changes_sheet(
    title="Union Bancaire Privée (UK) Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, Company-only basis, £'000. Equity reconciliation ladder "
              "confirmed: every year's own closing balance ties exactly to both the next year's own opening balance "
              "and that year's own Balance Sheet Total equity - zero undocumented plug rows across all 4 years, "
              "including the FY2022 acquisition-related transfers of net assets from SGKHCIL/SGKHGL and FY2024's "
              "capital repayment and share premium cancellation. FY2025 is not yet disclosed (no FY2025 statutory "
              "accounts filed).",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=54,
    source_height=300,
)

bw.add_cash_flow_sheet(
    title="Union Bancaire Privée (UK) Limited — Statement of Cash Flows",
    subtitle="Not applicable: the Company's own FRS 101 Reduced Disclosure Framework accounts do not include a Statement of Cash Flows in any year covered (a permitted FRS 101 exemption, distinct from the separate Pillar 3/statutory consolidation-scope mismatch noted below).",
    rows=[
        ("SECTION", "FRS 101 exemption", {}),
        ("DATA", "Standalone cash-flow statement", {year: "Not presented" for year in YEARS}),
    ],
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=82,
    source_height=250,
    unit_suffix="",
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by product (gross)", {}),
    ("DATA", "Retail mortgages", {"FY2024": 1162158, "FY2023": 1409121, "FY2022": 1690736, "FY2021": 865254}),
    ("DATA", "Other loans", {"FY2024": 518784, "FY2023": 532693, "FY2022": 684771, "FY2021": 392952}),
    ("TOTAL", "Total gross loans and advances to customers", {"FY2024": 1680942, "FY2023": 1941814, "FY2022": 2375507, "FY2021": 1258206}),
    ("DATA", "Expected credit loss", {"FY2024": -13079, "FY2023": -18176, "FY2022": -20117, "FY2021": -9592}),
    ("TOTAL", "Net loans and advances to customers", {"FY2024": 1667863, "FY2023": 1923638, "FY2022": 2355390, "FY2021": 1248614}),
    ("SECTION", "Credit quality by IFRS 9 stage, net of ECL", {}),
    ("DATA", "Stage 1 (performing)", {"FY2024": 1524977, "FY2023": 1710531, "FY2022": 2132521, "FY2021": 1138843}),
    ("DATA", "Stage 2 (underperforming)", {"FY2024": 55231, "FY2023": 100344, "FY2022": 132207, "FY2021": 39609}),
    ("DATA", "Stage 3 (non-performing)", {"FY2024": 87655, "FY2023": 112763, "FY2022": 90662, "FY2021": 70162}),
    ("TOTAL", "Total, net of ECL", {"FY2024": 1667863, "FY2023": 1923638, "FY2022": 2355390, "FY2021": 1248614}),
    ("SECTION", "Gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing), gross", {"FY2024": 1526322, "FY2023": 1712678, "FY2022": 2135104, "FY2021": 1141352}),
    ("DATA", "Stage 2 (underperforming), gross", {"FY2024": 57078, "FY2023": 102584, "FY2022": 134462, "FY2021": 39936}),
    ("DATA", "Stage 3 (non-performing), gross", {"FY2024": 97542, "FY2023": 126552, "FY2022": 105941, "FY2021": 76918}),
    ("TOTAL", "Total gross carrying amount", {"FY2024": 1680942, "FY2023": 1941814, "FY2022": 2375507, "FY2021": 1258206}),
    ("SECTION", "Loan book by security type, net of ECL", {}),
    ("DATA", "Lombard", {"FY2024": 323533, "FY2023": 339135, "FY2022": 504694, "FY2021": 283206}),
    ("DATA", "Real estate", {"FY2024": 1265966, "FY2023": 1546376, "FY2022": 1799430, "FY2021": 944242}),
    ("DATA", "Asset-backed", {"FY2024": 6086, "FY2023": 14554, "FY2022": 23401, "FY2021": 2860}),
    ("DATA", "Unsecured", {"FY2024": 72278, "FY2023": 23573, "FY2022": 27865, "FY2021": 18306}),
    ("TOTAL", "Total, net of ECL (by security type)", {"FY2024": 1667863, "FY2023": 1923638, "FY2022": 2355390, "FY2021": 1248614}),
    ("SECTION", "Derived ratios (as reported)", {}),
    ("DATA", "Non-performing loan ratio (Stage 3 gross / total gross)", {"FY2024": "5.80%", "FY2023": "6.52%", "FY2022": "4.46%", "FY2021": "6.11%"}),
    ("DATA", "Total coverage ratio (total ECL / total gross)", {"FY2024": "0.78%", "FY2023": "0.94%", "FY2022": "0.79%", "FY2021": "0.76%"}),
    ("DATA", "Stage 3 coverage ratio", {"FY2024": "10.14%", "FY2023": "10.90%", "FY2022": "14.41%", "FY2021": "8.78%"}),
]
bw.add_asset_quality_sheet(
    title="Union Bancaire Privée (UK) Limited — Asset Quality",
    subtitle="Loans and advances to customers by product, IFRS 9 stage and security type (Note 14), Company-only basis, £'000. Zero undocumented plug rows: every block ties exactly to the Balance Sheet's Loans and advances to customers line and to each other across all 4 years.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nNote 14 (Loans and advances to customers) page references - FY2024/FY2023: AR2024 p.56-57; "
        "FY2023/FY2022: AR2023 p.55-56 (FY2022's own credit-quality table is not in the AR2022 Companies "
        "House filing, which is truncated after Note 12 - see the note above); FY2021/FY2020: AR2021 p.49-50. "
        "Coverage/NPL ratios derived from each year's own reported gross-by-stage and ECL-by-stage tables; "
        "the total coverage ratio and Stage 3 coverage ratio are reproduced exactly as reported."
    ),
    first_col_width=90,
    source_height=320,
    unit_suffix=" (£'000)",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        P3_SOURCES,
        note=note,
        first_col_width=65,
        source_height=240,
    )


CAPITAL = {"FY2024": 291.256, "FY2023": 356.795, "FY2022": 426.529, "FY2021": 461.392}
RWA = {"FY2024": 1373.096, "FY2023": 1450.014, "FY2022": 1830.761, "FY2021": 1951.543}
CAPITAL_RATIO = {"FY2024": "21.2%", "FY2023": "24.6%", "FY2022": "23.3%", "FY2021": "23.6%"}
LEVERAGE_EXPOSURE = {"FY2024": 4407.957, "FY2023": 4161.978, "FY2022": 4707.494, "FY2021": 5203.049}
LEVERAGE = {"FY2024": "6.6%", "FY2023": "8.6%", "FY2022": "9.1%", "FY2021": "8.9%"}
HQLA = {"FY2024": 2565.121, "FY2023": 2191.986, "FY2022": 2372.431, "FY2021": 2319.358}
LCR_OUTFLOWS = {"FY2024": 1167.142, "FY2023": 971.156, "FY2022": 1029.869, "FY2021": 1079.986}
LCR_INflows = {"FY2024": 135.972, "FY2023": 103.495, "FY2022": 208.111, "FY2021": 301.570}
LCR_NET = {"FY2024": 1031.169, "FY2023": 867.661, "FY2022": 821.759, "FY2021": 778.416}
LCR = {"FY2024": "248.8%", "FY2023": "252.6%", "FY2022": "288.7%", "FY2021": "298.0%"}
ASF = {"FY2024": 3202.089, "FY2023": 3140.112, "FY2022": 3765.621, "FY2021": 3792.308}
RSF = {"FY2024": 1265.791, "FY2023": 1441.162, "FY2022": 1698.754, "FY2021": 2108.413}
NSFR = {"FY2024": "253.0%", "FY2023": "217.9%", "FY2022": "221.7%", "FY2021": "179.9%"}

GAP_NOTE = (
    "FY2025 is blank because the official UBP UK archive currently provides "
    "SGKH UK Consolidation Group disclosures through 31 December 2024 only. "
    "FY2021-FY2024 are populated from the 2022-2024 reports. Amounts are "
    "converted from £'000 to £m; ratios remain as reported."
)

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", CAPITAL)], GAP_NOTE)
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", CAPITAL_RATIO)], GAP_NOTE)
metric("Tier 1 Capital", "£m", [("Tier 1 capital", CAPITAL)], "Tier 1 capital equals CET1 capital in every populated year; the UK KM1 tables report the same amount.\n" + GAP_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CAPITAL_RATIO)], GAP_NOTE)
metric("Total Capital", "£m", [("Total capital", CAPITAL)], "Total capital equals CET1 and Tier 1 capital in every populated year in the UK KM1 tables.\n" + GAP_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", CAPITAL_RATIO)], GAP_NOTE)
metric("Total RWAs", "£m", [("Total risk-weighted exposure amounts", RWA)], GAP_NOTE)

RWA_CREDIT = {"FY2024": 1088.247, "FY2023": 1209.992, "FY2022": 1556.662, "FY2021": 1663.351}
RWA_CCR = {"FY2024": 38.962, "FY2023": 32.907, "FY2022": 34.661, "FY2021": 21.756}
RWA_SETTLEMENT = {"FY2024": 0.000, "FY2023": 0.092, "FY2022": 0.004, "FY2021": 0.042}
RWA_MARKET = {"FY2024": 1.174, "FY2023": 1.336, "FY2022": 1.158, "FY2021": 0.881}
RWA_OPERATIONAL = {"FY2024": 244.713, "FY2023": 205.688, "FY2022": 238.276, "FY2021": 265.514}
RWA_THRESHOLD_MEMO = {"FY2024": 30.604, "FY2023": 31.439, "FY2022": 35.922, "FY2021": 12.243}
rwa_breakdown_rows = [
    ("SECTION", "UK OV1 - Overview of Risk-Weighted Exposure Amounts", {}),
    ("DATA", "Credit Risk (excluding CCR)", RWA_CREDIT),
    ("DATA", "Counterparty Credit Risk (CCR)", RWA_CCR),
    ("DATA", "Settlement Risk", RWA_SETTLEMENT),
    ("DATA", "Position, foreign exchange and commodities risks (Market Risk)", RWA_MARKET),
    ("DATA", "Operational risk", RWA_OPERATIONAL),
    ("TOTAL", "Total risk-weighted exposure amounts", RWA),
    ("DATA", "Memo: amounts below thresholds for deduction (250% risk weight, excluded from Total)", RWA_THRESHOLD_MEMO),
]
bw.add_rwa_breakdown_sheet(
    title="Union Bancaire Privée (UK) Limited — RWA Breakdown",
    subtitle="UK Consolidation Group basis, £m. Category rows sum exactly to Total RWAs (the 'amounts below thresholds for deduction' row is a memo/for-information line excluded from the additive total, per the source template's own footnote).",
    rows=rwa_breakdown_rows,
    sources_text=P3_SOURCES + (
        "\n\nUK OV1 category breakdown: FY2024/FY2023 - SGKH Pillar 3 Disclosure 31 December 2024, "
        f"Table UK OV1 p.9 - {P3_2024_URL}\nFY2022/FY2021 - SGKH Pillar 3 Disclosure 31 December 2022, "
        f"Table UK OV1 p.9 - {P3_2022_URL}. FY2021's Counterparty Credit Risk (CCR) figure is transcribed "
        "as £21.756m: the source document prints '21,7561' (a trailing-digit typo confirmed by the column "
        "summing to the reported Total RWAs of £1,951.543m only when read as 21,756)."
    ),
    first_col_width=76,
    source_height=300,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio",
    "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", LEVERAGE_EXPOSURE),
        ("Leverage ratio excluding claims on central banks", LEVERAGE),
    ],
    "SGKH states that it is outside the binding LREQ framework but continues to monitor leverage. The reported ratio uses the excluding-central-bank-claims basis.\n" + GAP_NOTE,
)
metric(
    "LCR",
    "£m / %",
    [
        ("Total HQLA, weighted value average", HQLA),
        ("Cash outflows, total weighted value", LCR_OUTFLOWS),
        ("Cash inflows, total weighted value", LCR_INflows),
        ("Total net cash outflows, adjusted value", LCR_NET),
        ("Liquidity Coverage Ratio", LCR),
    ],
    "LCR is presented on the reports' weighted-average basis. FY2021 component values are taken from the FY2022 report's comparative column.\n" + GAP_NOTE,
)
metric(
    "NSFR",
    "£m / %",
    [
        ("Total available stable funding", ASF),
        ("Total required stable funding", RSF),
        ("NSFR ratio", NSFR),
    ],
    "NSFR is presented on the reports' four-quarter average basis. FY2021 component values are taken from the FY2022 report's comparative column.\n" + GAP_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    P3_SOURCES,
    per_note={
        "MREL Ratio": "No numeric MREL ratio was found in the 2022-2024 UK Consolidation Group disclosures reviewed. FY2025 is also outside the located disclosure coverage.",
    },
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Tier 1 Ratio", CAPITAL_RATIO),
        ("Total Capital Ratio", CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note=(
        "Balance Sheet/P&L/Equity/Asset Quality are on the Company-only statutory basis (FY2021-FY2024); "
        "Pillar 3 ratios are on the UK Consolidation Group basis (FY2021-FY2024) - two different scopes, "
        "per the Company's own disclosures (see the entity/basis note on each sheet). FY2025 is blank "
        "throughout because no FY2025 statutory accounts or UK Consolidation Group Pillar 3 disclosure had "
        "been filed/located as of this workbook's build date. Cash flow is not substituted because the "
        "published accounts use the FRS 101 reduced disclosure framework, which exempts the Company from "
        "presenting a Statement of Cash Flows."
    ),
    balance_sheet_totals=[
        ("Total assets", {"FY2024": 4765408, "FY2023": 4530099, "FY2022": 5291601, "FY2021": 2448463}),
        ("Loans and advances to customers", {"FY2024": 1667863, "FY2023": 1923638, "FY2022": 2355390, "FY2021": 1248614}),
        ("Customers' accounts", {"FY2024": 4329605, "FY2023": 3970768, "FY2022": 4654279, "FY2021": 1934968}),
        ("Total equity", {"FY2024": 297221, "FY2023": 405397, "FY2022": 477262, "FY2021": 463510}),
    ],
    balance_sheet_unit=" (£'000)",
    income_statement_totals=[
        ("Total operating income", {"FY2024": 130404, "FY2023": 167032, "FY2022": 109174, "FY2021": 96260}),
        ("Total operating expenses", {"FY2024": -121195, "FY2023": -127298, "FY2022": -88021, "FY2021": -64601}),
        ("Profit for the year", {"FY2024": 8654, "FY2023": 35239, "FY2022": 17764, "FY2021": 30451}),
    ],
    income_statement_unit=" (£'000)",
    equity_changes_totals=[
        ("Opening equity", {"FY2024": 405397, "FY2023": 477262, "FY2022": 463510, "FY2021": 437606}),
        ("Total comprehensive income/(expense) for the year", {"FY2024": 13805, "FY2023": 47788, "FY2022": 3176, "FY2021": 25864}),
        ("Closing equity", {"FY2024": 297221, "FY2023": 405397, "FY2022": 477262, "FY2021": 463510}),
    ],
    equity_changes_unit=" (£'000)",
)

bw.save("/Users/armaan/code/katalysis/banks/UNION BANCAIRE PRIVEE UK FINANCIALS.xlsx")
print("Saved.")
