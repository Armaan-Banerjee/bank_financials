import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, all 12mo to 31 Dec

AR2025_URL = "https://www.bankofirelanduk.com/app/uploads/annual-report_2025_boi-uk.pdf"
AR2024_URL = "https://investorrelations.bankofireland.com/app/uploads/Annual-Report-UK-2024-web-version.pdf"
AR2023_URL = "https://investorrelations.bankofireland.com/app/uploads/BOI-UKPLC-2023-Annual-Report.pdf"
AR2022_URL = "https://www.bankofirelanduk.com/app/uploads/BOI-UK-Annual-Report-2022.pdf"
AR2021_URL = "https://www.bankofirelanduk.com/app/uploads/2017/04/Annual-Report-UK-2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank of Ireland (UK) Plc (Companies House 07022885, FRN 512956) is a wholly owned subsidiary of "
    "Bank of Ireland Group plc (Ireland). Figures throughout are the CONSOLIDATED GROUP basis (not the standalone "
    "parent-only 'Bank' accounts, which separately take the FRS 101/IAS 7 cash-flow-statement exemption available "
    "to a qualifying entity - the consolidated Group accounts do not take that exemption and contain a full "
    "Consolidated cash flow statement every year). Bank of Ireland (UK) Plc stopped publishing a standalone Pillar "
    "3 disclosure document after the 2020 financial year; from FY2021 onward, its capital/leverage/liquidity/MREL "
    "ratios are instead disclosed directly within the Annual Report's Risk Management Report ('2.2 Funding and "
    "liquidity risk' and '3 Capital management' sections), which is what is cited below. Those sections give a full "
    "capital composition table (CET1/Tier 1/Total capital/RWA/leverage exposure) and headline LCR/NSFR/MREL ratios, "
    "but - unlike a formal Pillar 3 KM1 template - do not publish the underlying £m components behind the LCR "
    "(HQLA, net cash outflows) or NSFR (available/required stable funding) ratios, or a numeric MREL resources "
    "breakdown; only the headline percentages are available for FY2021-FY2025."
)

BASIS_NOTE = (
    "RATIO BASIS NOTE: CET1 ratio and Leverage ratio are quoted exactly as stated in each year's Annual Report, on "
    "the 'fully loaded' basis (i.e. excluding IFRS 9 transitional relief, which fully phased out at 31 December "
    "2024) throughout, for comparability across years. FY2024 and FY2025 Total Capital ratios are also explicitly "
    "stated on a fully loaded basis in the source; for FY2021-FY2023 only a 'regulatory' (IFRS 9 transitional) "
    "basis Total Capital ratio was stated as a headline figure, so the fully loaded Total Capital ratios shown for "
    "those years are calculated here as disclosed fully-loaded Total capital / disclosed RWA (both audited "
    "figures from the same capital composition table) rather than quoted verbatim - cross-checked and consistent "
    "with the FY2024/FY2025 years where both the calculated and stated fully-loaded figures are available. Tier 1 "
    "ratio is not quoted as a percentage in any year's Annual Report (only Tier 1 capital £m and RWA £m); it is "
    "calculated the same way (Tier 1 capital / RWA) for all 5 years."
)

REGULATORY_NOTE = (
    "REGULATORY NOTE: On 19 February 2026 the Payment Systems Regulator (not the PRA) fined Bank of Ireland (UK) "
    "Plc £3.78m for a 14-month delay implementing Confirmation of Payee send functionality (compliant from January "
    "2025). This relates to payment-systems conduct, not capital/liquidity adequacy, and has no bearing on the "
    "figures in this workbook."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank of Ireland (UK) Plc consolidated Group cash flow statement, £m:\n"
    f"FY2025: Bank of Ireland (UK) Annual Report 2025, p.80 (Consolidated cash flow statement) - {AR2025_URL}\n"
    f"FY2024: Bank of Ireland (UK) Annual Report 2024, p.85 (Consolidated cash flow statement) - {AR2024_URL}\n"
    f"FY2023: Bank of Ireland (UK) plc Annual Report 2023, p.79 (Consolidated cash flow statement) - {AR2023_URL}\n"
    f"FY2022: Bank of Ireland (UK) plc Annual Report 2022, p.81 (Consolidated cash flow statement) - {AR2022_URL}\n"
    f"FY2021: Bank of Ireland (UK) plc Annual Report 2021, p.87 (Consolidated cash flow statement) - {AR2021_URL}\n"
    "Note: each year's own report was used for its own column (all cross-checked against the following year's "
    "comparative column, which matched exactly in every case). Operating-activity adjustment line items vary "
    "slightly year to year (e.g. 'Net change in fair value changes due to interest rate risk of the hedged items "
    "in portfolio hedges' appears only in FY2023/FY2024); blank cells indicate that year's report did not include "
    "that specific line. Section totals and cash/cash equivalents figures are consistent and comparable across all "
    "5 years.\n\n"
    + ENTITY_NOTE + "\n\n" + REGULATORY_NOTE
)


def p3_sources(page):
    urls = {"FY2025": AR2025_URL, "FY2024": AR2024_URL, "FY2023": AR2023_URL, "FY2022": AR2022_URL, "FY2021": AR2021_URL}
    names = {
        "FY2025": "Bank of Ireland (UK) Annual Report 2025",
        "FY2024": "Bank of Ireland (UK) Annual Report 2024",
        "FY2023": "Bank of Ireland (UK) plc Annual Report 2023",
        "FY2022": "Bank of Ireland (UK) plc Annual Report 2022",
        "FY2021": "Bank of Ireland (UK) plc Annual Report 2021",
    }
    lines = ["Sources - Bank of Ireland (UK) Plc consolidated Group basis, from the Risk Management Report / "
             "Financial Review ('2.2 Funding and liquidity risk' / '3 Capital management' sections):"]
    for y in YEARS:
        lines.append(f"{y}: {names[y]}, p.{page[y]} - {urls[y]}")
    return "\n".join(lines) + "\n\n" + BASIS_NOTE


bw = BankWorkbook(bank_name="Bank of Ireland (UK) Plc", years=YEARS, header_color="00594F")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before taxation", {"FY2025": -12, "FY2024": 181, "FY2023": 331, "FY2022": 251, "FY2021": 410}),
    ("DATA", "Interest expense on subordinated liabilities and other capital instruments", {"FY2025": 28, "FY2024": 31, "FY2023": 34, "FY2022": 14, "FY2021": 17}),
    ("DATA", "Interest expense on lease liabilities", {"FY2025": 1, "FY2024": 1, "FY2023": 1, "FY2022": 1}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 48, "FY2024": 46, "FY2023": 34, "FY2022": 27, "FY2021": 31}),
    ("DATA", "Net impairment losses/(gains) on financial instruments", {"FY2025": 25, "FY2024": -8, "FY2023": 43, "FY2022": 64, "FY2021": -54}),
    ("DATA", "Profit on sale of financial assets", {"FY2024": -33}),
    ("DATA", "(Gain)/loss on disposal of financial assets", {"FY2021": -94}),
    ("DATA", "(Gain)/loss on disposal of business activities", {"FY2021": -1}),
    ("DATA", "(Gain)/loss on sale of property, plant, equipment", {"FY2022": -1}),
    ("DATA", "Share of results of joint venture", {"FY2025": -22, "FY2024": -24, "FY2023": -25, "FY2022": -28, "FY2021": 2}),
    ("DATA", "Net change in prepayments and interest receivable", {"FY2025": -5, "FY2024": 9, "FY2022": -4, "FY2021": 10}),
    ("DATA", "Net change in accruals and interest payable", {"FY2025": -9, "FY2024": 8, "FY2023": 94, "FY2022": 36, "FY2021": -28}),
    ("DATA", "Charge for provisions", {"FY2025": 236, "FY2024": 148, "FY2023": 3, "FY2022": 2, "FY2021": 13}),
    ("DATA", "Other non-cash items", {"FY2025": -18, "FY2024": -98, "FY2023": -127, "FY2022": -45, "FY2021": 7}),
    ("TOTAL", "Cash flows from operating activities before changes in operating assets and liabilities", {"FY2025": 272, "FY2024": 261, "FY2023": 388, "FY2022": 317, "FY2021": 313}),
    ("DATA", "Net change in items in the course of collection to/from banks", {"FY2025": 35, "FY2024": -19, "FY2023": 31, "FY2022": 24, "FY2021": 5}),
    ("DATA", "Net change in derivative financial instruments", {"FY2025": 26, "FY2024": 97, "FY2023": 97, "FY2022": 30, "FY2021": -9}),
    ("DATA", "Net change in loans and advances to banks", {"FY2025": 32, "FY2024": -51, "FY2023": -45, "FY2021": 4}),
    ("DATA", "Net change in fair value changes due to interest rate risk of hedged items in portfolio hedges", {"FY2023": -146}),
    ("DATA", "Net change in loans and advances to customers", {"FY2025": -536, "FY2024": -671, "FY2023": 101, "FY2022": 2316, "FY2021": 2051}),
    ("DATA", "Net change in deposits from banks", {"FY2025": 265, "FY2024": -815, "FY2023": 130, "FY2022": -292, "FY2021": -803}),
    ("DATA", "Net change in customer accounts", {"FY2025": 542, "FY2024": 408, "FY2023": -537, "FY2022": -3532, "FY2021": -2495}),
    ("DATA", "Net change in debt securities in issue", {"FY2025": 229, "FY2024": -35, "FY2023": 170, "FY2022": -69, "FY2021": -63}),
    ("DATA", "Net change in provisions", {"FY2025": -18, "FY2024": -8, "FY2023": -4, "FY2022": -7, "FY2021": -14}),
    ("DATA", "Net change in retirement benefit obligation", {"FY2025": -1, "FY2024": -1, "FY2022": -1, "FY2021": -1}),
    ("DATA", "Net change in other assets and other liabilities", {"FY2025": -65, "FY2024": -7, "FY2023": -143, "FY2022": -14, "FY2021": -90}),
    ("TOTAL", "Net cash flow from operating assets and liabilities", {"FY2025": 509, "FY2024": -1102, "FY2023": -346, "FY2022": -1545, "FY2021": -1415}),
    ("TOTAL", "Net cash flow from operating activities before taxation", {"FY2025": 781, "FY2024": -841, "FY2023": 42, "FY2022": -1228, "FY2021": -1102}),
    ("DATA", "Taxation paid", {"FY2025": -51, "FY2024": -47, "FY2023": -56, "FY2022": -21, "FY2021": -53}),
    ("TOTAL", "Net cash flow from operating activities", {"FY2025": 730, "FY2024": -888, "FY2023": -14, "FY2022": -1249, "FY2021": -1155}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Proceeds from sale of financial assets", {"FY2024": 680, "FY2021": 2942}),
    ("DATA", "Disposal of business activities", {}),
    ("DATA", "Additions to debt securities at amortised cost", {"FY2025": -461, "FY2024": -77, "FY2023": -145, "FY2022": -26, "FY2021": -252}),
    ("DATA", "Disposal/redemption of debt securities at amortised cost", {"FY2025": 69, "FY2024": 90, "FY2023": 196, "FY2022": 266, "FY2021": 359}),
    ("DATA", "Dividends received from joint venture", {"FY2025": 23, "FY2024": 30, "FY2023": 29, "FY2022": 3}),
    ("DATA", "Additions to intangible assets", {}),
    ("DATA", "Additions to property, plant and equipment", {"FY2025": -105, "FY2024": -97, "FY2023": -82, "FY2022": -70, "FY2021": -54}),
    ("DATA", "Disposal of property, plant and equipment", {"FY2025": 37, "FY2024": 33, "FY2023": 29, "FY2022": 23, "FY2021": 18}),
    ("TOTAL", "Cash flows from investing activities", {"FY2025": -437, "FY2024": 659, "FY2023": 27, "FY2022": 196, "FY2021": 3013}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Share repurchase", {"FY2021": -250}),
    ("DATA", "Dividend paid on ordinary shares", {"FY2023": -250, "FY2022": -250}),
    ("DATA", "Proceeds from issue of AT1", {"FY2021": 150}),
    ("DATA", "Redemption of AT1", {"FY2021": -300}),
    ("DATA", "Additional tier 1 coupon paid", {"FY2025": -9, "FY2024": -9, "FY2023": -9, "FY2022": -9, "FY2021": -25}),
    ("DATA", "Redemption of subordinated liabilities", {"FY2022": -90, "FY2021": -200}),
    ("DATA", "Proceeds from issue of subordinated liabilities", {"FY2022": 90, "FY2021": 100}),
    ("DATA", "Interest paid on subordinated liabilities", {"FY2025": -28, "FY2024": -31, "FY2023": -34, "FY2022": -14, "FY2021": -17}),
    ("DATA", "Payment of lease liability", {"FY2025": -1, "FY2024": -3, "FY2023": -4, "FY2022": -4, "FY2021": -4}),
    ("TOTAL", "Cash flows from financing activities", {"FY2025": -38, "FY2024": -43, "FY2023": -297, "FY2022": -277, "FY2021": -546}),
    ("TOTAL", "Net change in cash and cash equivalents", {"FY2025": 255, "FY2024": -272, "FY2023": -284, "FY2022": -1330, "FY2021": 1312}),
    ("DATA", "Opening cash and cash equivalents", {"FY2025": 3115, "FY2024": 3387, "FY2023": 3671, "FY2022": 5001, "FY2021": 3689}),
    ("TOTAL", "Closing cash and cash equivalents", {"FY2025": 3370, "FY2024": 3115, "FY2023": 3387, "FY2022": 3671, "FY2021": 5001}),
]

bw.add_cash_flow_sheet(
    title="Bank of Ireland (UK) Plc — Consolidated Cash Flow Statement",
    subtitle="Consolidated Group basis, £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 / capital metric sheets
# ---------------------------------------------------------------
CAP_PAGE = {"FY2025": "55", "FY2024": "57-58", "FY2023": "54-55", "FY2022": "55-56", "FY2021": "60"}
LIQ_PAGE = {"FY2025": "48", "FY2024": "49-50", "FY2023": "45-46", "FY2022": "45-46", "FY2021": "51-52"}


def metric(name, unit, rows_data, page, note=None):
    bw.add_metric_sheet(name, f"Consolidated Group basis, {unit}" if unit else "Consolidated Group basis",
                         rows_data, p3_sources(page), note=note, first_col_width=44, source_height=140)


metric(
    "CET1 Capital", "£m",
    [("Common equity tier 1 capital", {"FY2025": 1601, "FY2024": 1548, "FY2023": 1412, "FY2022": 1394, "FY2021": 1497})],
    CAP_PAGE,
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio (fully loaded)", {"FY2025": "19.6%", "FY2024": "19.9%", "FY2023": "17.8%", "FY2022": "18.2%", "FY2021": "17.2%"})],
    CAP_PAGE,
)

metric(
    "Tier 1 Capital", "£m",
    [("Total tier 1 capital", {"FY2025": 1751, "FY2024": 1698, "FY2023": 1562, "FY2022": 1544, "FY2021": 1647})],
    CAP_PAGE,
    note="Tier 1 ratio (see Tier 1 Ratio sheet) is calculated from this figure - see the Ratio Basis Note on the "
         "Cash Flow Statement sheet.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio (fully loaded; calculated as Tier 1 capital / RWA)", {"FY2025": "21.4%", "FY2024": "21.9%", "FY2023": "19.7%", "FY2022": "20.1%", "FY2021": "19.0%"})],
    CAP_PAGE,
    note="Not stated as a percentage in any year's Annual Report (only Tier 1 capital £m and RWA £m are disclosed); "
         "calculated here as Tier 1 capital / Total risk weighted assets - see the Ratio Basis Note on the Cash "
         "Flow Statement sheet.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 1941, "FY2024": 1888, "FY2023": 1752, "FY2022": 1734, "FY2021": 1837})],
    CAP_PAGE,
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio (fully loaded)", {"FY2025": "23.7%", "FY2024": "24.3%", "FY2023": "22.1%", "FY2022": "22.5%", "FY2021": "21.2%"})],
    CAP_PAGE,
    note="Explicitly stated on a fully loaded basis for FY2024/FY2025 only; FY2021-FY2023 are calculated as Total "
         "capital / RWA (both disclosed fully-loaded figures) since only a regulatory-basis ratio was stated as a "
         "headline figure those years - see the Ratio Basis Note on the Cash Flow Statement sheet.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk weighted assets", {"FY2025": 8180, "FY2024": 7767, "FY2023": 7939, "FY2022": 7699, "FY2021": 8686})],
    CAP_PAGE,
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total leverage ratio exposures", {"FY2025": 19437, "FY2024": 17664, "FY2023": 16678, "FY2022": 16948, "FY2021": 22879}),
        ("Leverage ratio (fully loaded)", {"FY2025": "9.0%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "9.1%", "FY2021": "7.2%"}),
    ],
    CAP_PAGE,
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {"FY2025": "161%", "FY2024": "154%", "FY2023": "168%", "FY2022": "178%", "FY2021": "268%"})],
    LIQ_PAGE,
    note="Only the headline LCR percentage is disclosed in the Annual Report's Funding and liquidity risk section; "
         "the underlying £m components (HQLA, net cash outflows) are not published for FY2021-FY2025, since a "
         "formal Pillar 3 KM1-style template has not been published at this UK-entity level since FY2020.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {"FY2025": "135%", "FY2024": "130%", "FY2023": "135%", "FY2022": "135%", "FY2021": "139%"})],
    LIQ_PAGE,
    note="Only the headline NSFR percentage is disclosed; the underlying £m components (available/required stable "
         "funding) are not published for FY2021-FY2025 - see the LCR sheet's note.",
)

metric(
    "MREL Ratio", "%",
    [("MREL ratio", {"FY2025": "26.2%", "FY2024": "26.9%", "FY2023": "24.6%", "FY2022": "26.7%", "FY2021": "24.9%"})],
    CAP_PAGE,
    note="Only the headline MREL ratio percentage is disclosed each year (a 'Key points' bullet in the Capital "
         "management section); no £m MREL resources/requirement breakdown is published. The Bank has been subject "
         "to an internal MREL requirement on a transitional basis since 1 January 2020; the Parent (Bank of "
         "Ireland Group plc), as sole shareholder, is expected to provide any future core MREL resources.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flow from operating activities", {"FY2025": 730, "FY2024": -888, "FY2023": -14, "FY2022": -1249, "FY2021": -1155}),
        ("Cash flows from investing activities", {"FY2025": -437, "FY2024": 659, "FY2023": 27, "FY2022": 196, "FY2021": 3013}),
        ("Cash flows from financing activities", {"FY2025": -38, "FY2024": -43, "FY2023": -297, "FY2022": -277, "FY2021": -546}),
        ("Closing cash and cash equivalents", {"FY2025": 3370, "FY2024": 3115, "FY2023": 3387, "FY2022": 3671, "FY2021": 5001}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "19.6%", "FY2024": "19.9%", "FY2023": "17.8%", "FY2022": "18.2%", "FY2021": "17.2%"}),
        ("Tier 1 Ratio", {"FY2025": "21.4%", "FY2024": "21.9%", "FY2023": "19.7%", "FY2022": "20.1%", "FY2021": "19.0%"}),
        ("Total Capital Ratio", {"FY2025": "23.7%", "FY2024": "24.3%", "FY2023": "22.1%", "FY2022": "22.5%", "FY2021": "21.2%"}),
        ("Leverage Ratio", {"FY2025": "9.0%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "9.1%", "FY2021": "7.2%"}),
        ("LCR", {"FY2025": "161%", "FY2024": "154%", "FY2023": "168%", "FY2022": "178%", "FY2021": "268%"}),
        ("NSFR", {"FY2025": "135%", "FY2024": "130%", "FY2023": "135%", "FY2022": "135%", "FY2021": "139%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Tier 1 Ratio and part of the Total Capital Ratio series are "
         "calculated (capital / RWA), not directly quoted - see the Ratio Basis Note on the Cash Flow Statement "
         "sheet. No standalone Pillar 3 document has been published for this entity since FY2020; all figures here "
         "come from the Annual Report's Risk Management Report instead.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF IRELAND UK FINANCIALS.xlsx")
