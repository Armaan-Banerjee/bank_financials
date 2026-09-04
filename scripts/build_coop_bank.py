import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Calendar year-end (31 December). Most recent published Annual Report and Pillar 3
# disclosures are for FY2024 (signed 6 March 2025) - no FY2025 Annual Report and
# Accounts had yet been published as of the source-gathering date (2026-08-26),
# only summary H1/H2 2025 Pillar 3 KM1 disclosures (no cash flow statement, and
# no capital-amount breakdown, only headline ratios in the trading update) - not
# usable for this workbook's format, so FY2025 is left out entirely rather than
# filled in from an incompatible source. 5 years used: FY2024-FY2020.
YEARS = ["FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2024_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2024-annual-report-and-accounts.pdf"
AR2022_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2022-annual-report-and-accounts.pdf"
AR2020_URL = "https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/2020-annual-report-and-accounts.pdf"

P3_2024_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2024-pillar-3-disclosures.pdf"
P3_2022_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2022-pillar-3-disclosures.pdf"
P3_2020_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2020-pillar-3-disclosures.pdf"
P3_2025_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2025-h2-pillar-3-disclosures.pdf"
P3_2025_H1_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2025-h1-pillar-3-disclosures.pdf"

ENTITY_NOTE = (
    "ENTITY/OWNERSHIP NOTE: The Co-operative Bank p.l.c. (company number 00990937, FRN 121885) is the PRA-"
    "authorised entity. It is a wholly-owned subsidiary of The Co-operative Bank Finance p.l.c., itself wholly-"
    "owned by The Co-operative Bank Holdings p.l.c. (the listed holding company; named 'The Co-operative Bank "
    "Holdings Limited' in the FY2020-FY2022 Annual Reports, re-registered as a p.l.c. by FY2023). Coventry "
    "Building Society completed its acquisition of The Co-operative Bank Holdings p.l.c. on 1 January 2025 - "
    "outside the FY2020-FY2024 period covered by this workbook, so it has no bearing on any figure shown here. "
    "Coventry and Co-operative Bank have proposed a Part VII transfer of the Bank's business (including 'smile') "
    "into Coventry Building Society, targeted for 1 January 2027 - not yet effective as of the most recent "
    "published accounts, watch for a cash-flow-statement exemption or entity change in future years similar to "
    "Clydesdale Bank PLC's Nationwide Part VII transfer in this same workbook series. "
    "This workbook uses The Co-operative Bank p.l.c.'s own entity-level ('Bank Company-only') figures throughout "
    "- both cash flow and Pillar 3 - not the wider consolidated Group (The Co-operative Bank Holdings p.l.c. and "
    "its subsidiaries), consistent with the PRA-authorised-entity basis used elsewhere in this workbook series."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are The Co-operative Bank p.l.c.'s own Bank Company-only Statement of Cashflows, £m:\n"
    f"FY2024: The Co-operative Bank p.l.c. 2024 Annual Report and Accounts, p.222 (Statement of Cashflows, Bank "
    f"Company-only) - {AR2024_URL}\n"
    f"FY2023: The Co-operative Bank p.l.c. 2024 Annual Report and Accounts, p.222 (FY2023 comparative column, "
    f"same statement) - {AR2024_URL}\n"
    f"FY2022: The Co-operative Bank p.l.c. 2022 Annual Report and Accounts, p.245 (Statement of Cashflows, Bank "
    f"Company-only) - {AR2022_URL}\n"
    f"FY2021: The Co-operative Bank p.l.c. 2022 Annual Report and Accounts, p.245 (FY2021 comparative column, "
    f"same statement) - {AR2022_URL}\n"
    f"FY2020: The Co-operative Bank p.l.c. 2020 Annual Report and Accounts, p.215 (Statement of Cashflows, Bank "
    f"Company-only) - {AR2020_URL}\n"
    "All 5 years cross-checked and tie exactly across adjacent reports (e.g. FY2020 closing cash and cash "
    "equivalents of £4,221.1m matches the FY2022 report's own FY2021 opening balance).\n\n"
    + ENTITY_NOTE
)


def p3_sources(page_2024="139-140", page_2022_23="101-102"):
    return (
        "Sources - The Co-operative Bank p.l.c. individual-entity Pillar 3 basis (Appendix 1, 'KM1 - Key Metrics "
        "(Individual)' / 'KM2 - Key Metrics MREL (Individual)'):\n"
        f"FY2024: The Co-operative Bank 2024 Pillar 3 Disclosures, p.{page_2024} - {P3_2024_URL}\n"
        f"FY2023: The Co-operative Bank 2024 Pillar 3 Disclosures, p.{page_2024} (FY2023 comparative column, same "
        f"tables) - {P3_2024_URL}\n"
        f"FY2022: The Co-operative Bank 2022 Pillar 3 Disclosures, p.{page_2022_23} - {P3_2022_URL}\n"
        f"FY2021: The Co-operative Bank 2022 Pillar 3 Disclosures, p.{page_2022_23} (31 Dec 21 column, same "
        f"tables) - {P3_2022_URL}\n"
        f"FY2020: The Co-operative Bank 2022 Pillar 3 Disclosures, p.{page_2022_23} (31 Dec 20 column, same "
        f"tables - the KM1/KM2 templates report the current period plus 4 prior half-year-end points) - "
        f"{P3_2022_URL}"
    )


bw = BankWorkbook(bank_name="The Co-operative Bank p.l.c.", years=YEARS, year_label=YEAR_LABEL, header_color="1E5631")

STATEMENTS_SOURCES = (
    "Sources - The Co-operative Bank p.l.c.'s own Bank Company-only Balance Sheet / Statement of Changes in "
    "Equity, £m, transcribed from each year's own report (not a later year's comparative column):\n"
    f"FY2024: 2024 Annual Report and Accounts, p.220-221 (Balance Sheet), p.224 (Statement of Changes in Equity), "
    f"p.226 (Note 2, Net profit attributable to equity shareholders - Section 408 Companies Act 2006 exemption) "
    f"- {AR2024_URL}\n"
    f"FY2023: 2024 Annual Report and Accounts, p.220-221/224/226 (FY2023 comparative columns, same statements) - "
    f"{AR2024_URL}\n"
    f"FY2022: 2022 Annual Report and Accounts, p.242-243/246/248 (Balance Sheet, Statement of Changes in Equity, "
    f"Note 2) - {AR2022_URL}\n"
    f"FY2021: 2022 Annual Report and Accounts, p.242-243/246/248 (FY2021 comparative columns, same statements) - "
    f"{AR2022_URL}\n"
    f"FY2020: 2020 Annual Report and Accounts, p.212-213/216/217 (Balance Sheet, Statement of Changes in Equity, "
    f"Note 2) - {AR2020_URL}\n\n"
    "The Bank Company (individual entity) takes advantage of the Section 408 Companies Act 2006 exemption not to "
    "present its own income statement - each year's Annual Report discloses only the Bank Company's bottom-line "
    "net profit/(loss) figure (Note 2) plus, separately, its Other Comprehensive Income broken into reserve "
    "movements within the Statement of Changes in Equity itself; the Profit & Loss sheet reconstructs a P&L from "
    "these two disclosed pieces rather than fabricating a full income statement - all rows tie exactly to the "
    "equity roll-forward's own 'Total comprehensive income/(expense) for the year' figures.\n\n"
    "PRESENTATION NOTE: the Balance Sheet's equity section shows 'Other reserves' as a single aggregate line from "
    "FY2021 onward (FVOCI + cash flow hedging + capital redemption + defined benefit pension reserves combined); "
    "FY2020's own Balance Sheet still itemises 'Share premium account' separately (£2,416.9m) - a genuine one-off "
    "'Reserve reorganisation' movement during FY2021 (disclosed in the FY2022 Annual Report's own equity note) "
    "wrote the share premium account and capital redemption reserve down to £nil and transferred the combined "
    "£2,826.9m into retained earnings, a net-zero movement on Total equity; both entries are reproduced explicitly "
    "in the Statement of Changes in Equity sheet, not silently dropped. 'Equity shares' and 'Prepayments' appear as "
    "their own Balance Sheet lines FY2020-FY2022 only, folded into 'Other assets' from FY2023 onward per the "
    "Bank's own presentation. Deferred tax is presented as an asset FY2021-FY2024 but as a liability in FY2020 - "
    "both reproduced on their own side of the Balance Sheet as originally disclosed, not netted. 'Fair value "
    "adjustments for hedged risk' appears as separate Balance Sheet lines (both asset- and liability-side) only "
    "FY2020-FY2022 - embedded within the Loans and advances to customers note instead from FY2023 onward.\n\n"
    + ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - The Co-operative Bank p.l.c.'s own Note 26/27 'Analysis of Credit Risk Exposure' (Bank "
    "Company-only basis), £m:\n"
    f"FY2024/FY2023: 2024 Annual Report and Accounts, p.242-243 (Note 26) - {AR2024_URL}\n"
    f"FY2022/FY2021: 2022 Annual Report and Accounts, p.264-265 (Note 27) - {AR2022_URL}\n"
    f"FY2020: 2022 Annual Report and Accounts, p.265 (Note 27's own 'At 1 January 2021' comparative row, i.e. "
    f"FY2020's closing position) - {AR2022_URL}\n\n"
    "Figures are 'Gross customer exposure'/'Allowance for losses' by IFRS 9 stage for Loans and advances to "
    "customers - this is broader than the Balance Sheet's own 'Loans and advances to customers' line, since it "
    "includes off-balance-sheet credit commitments and excludes FVTPL-measured balances (each year's own note "
    "states the reconciling items); reproduced as disclosed, not force-reconciled to the narrower Balance Sheet "
    "figure. All balances other than Loans and advances to customers are confirmed Stage 1 in every year and did "
    "not transfer during the year (per each note's own statement), so are not separately broken out here.\n\n"
    + ENTITY_NOTE
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - The Co-operative Bank p.l.c. individual-entity Pillar 3 basis, UK OV1 'Overview of risk weighted "
    "exposures (Individual)' template (Appendix 1), £m:\n"
    f"FY2024/FY2023: 2024 Pillar 3 Disclosures, p.139 - {P3_2024_URL}\n"
    f"FY2022/FY2021: 2022 Pillar 3 Disclosures, p.101 - {P3_2022_URL}\n"
    f"FY2020: 2020 Pillar 3 Disclosures, p.55 (Table 40, 'Pillar 1 capital requirements', individual basis, "
    f"Appendix 2) - {P3_2020_URL}\n\n"
    "All 4 category-broken-out years tie exactly to the existing Total RWAs sheet's own figures. FY2020's own "
    "Pillar 3 document predates the UK OV1 template and uses an older CRR exposure-class format (IRB approach vs "
    "Standardised approach, not Credit risk/CCR/Securitisation/Market risk/Operational risk) - only Operational "
    "risk (£512.6m) and the Total (£4,668.4m, ties exactly) map cleanly onto the later years' category structure; "
    "Credit risk/CCR/Securitisation are left blank for FY2020 rather than force-mapped from a materially different "
    "categorisation (FY2020's 'Total credit risk' of £4,155.8m combines what later years split into 3 separate "
    "rows, and does not separately break out securitisation).\n\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
bw.add_balance_sheet_sheet(
    title="The Co-operative Bank p.l.c. — Balance Sheet (Bank Company-only)",
    subtitle="Bank Company-only basis (not the wider consolidated Group), £m",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances at central banks", {
            "FY2024": 2586.0, "FY2023": 2708.3, "FY2022": 5270.4, "FY2021": 5696.9, "FY2020": 3877.8,
        }),
        ("DATA", "Loans and advances to banks", {
            "FY2024": 173.1, "FY2023": 193.7, "FY2022": 312.5, "FY2021": 124.7, "FY2020": 431.6,
        }),
        ("DATA", "Loans and advances to customers", {
            "FY2024": 20370.8, "FY2023": 20147.5, "FY2022": 20919.1, "FY2021": 20998.3, "FY2020": 18676.7,
        }),
        ("DATA", "Fair value adjustments for hedged risk (assets)", {
            "FY2022": -430.7, "FY2021": -90.5, "FY2020": 134.1,
        }),
        ("DATA", "Investment securities", {
            "FY2024": 1637.3, "FY2023": 2509.4, "FY2022": 1826.0, "FY2021": 2149.8, "FY2020": 2158.6,
        }),
        ("DATA", "Derivative financial instruments", {
            "FY2024": 216.6, "FY2023": 301.0, "FY2022": 488.4, "FY2021": 241.2, "FY2020": 178.8,
        }),
        ("DATA", "Property, plant and equipment classified as held-for-sale", {"FY2020": 0.3}),
        ("DATA", "Equity shares", {"FY2022": 11.1, "FY2021": 22.8, "FY2020": 22.1}),
        ("DATA", "Investments in subsidiaries/group undertakings", {
            "FY2024": 22.8, "FY2023": 14.9, "FY2022": 15.0, "FY2021": 14.7, "FY2020": 43.3,
        }),
        ("DATA", "Investment properties", {"FY2020": 1.9}),
        ("DATA", "Other assets", {
            "FY2024": 51.0, "FY2023": 47.9, "FY2022": 14.1, "FY2021": 12.7, "FY2020": 99.6,
        }),
        ("DATA", "Prepayments", {"FY2022": 21.4, "FY2021": 20.3, "FY2020": 13.2}),
        ("DATA", "Amounts owed by Co-operative Bank undertakings", {
            "FY2024": 552.1, "FY2023": 70.6, "FY2022": 65.1, "FY2021": 33.2, "FY2020": 1336.1,
        }),
        ("DATA", "Current tax assets", {"FY2024": 6.7, "FY2023": 4.3, "FY2022": 1.8}),
        ("DATA", "Property, plant and equipment", {
            "FY2024": 24.9, "FY2023": 23.6, "FY2022": 22.8, "FY2021": 24.3, "FY2020": 35.2,
        }),
        ("DATA", "Intangible assets", {
            "FY2024": 109.8, "FY2023": 114.0, "FY2022": 90.0, "FY2021": 68.5, "FY2020": 63.4,
        }),
        ("DATA", "Right-of-use assets", {
            "FY2024": 26.8, "FY2023": 31.4, "FY2022": 33.0, "FY2021": 46.9, "FY2020": 53.7,
        }),
        ("DATA", "Deferred tax assets", {
            "FY2024": 243.0, "FY2023": 233.9, "FY2022": 167.5, "FY2021": 36.8,
        }),
        ("DATA", "Net retirement benefit asset", {
            "FY2024": 32.0, "FY2023": 148.5, "FY2022": 159.7, "FY2021": 841.1, "FY2020": 651.8,
        }),
        ("TOTAL", "Total assets", {
            "FY2024": 26052.9, "FY2023": 26549.0, "FY2022": 28987.2, "FY2021": 30241.7, "FY2020": 27778.2,
        }),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits by banks", {
            "FY2024": 2717.2, "FY2023": 4288.9, "FY2022": 5683.4, "FY2021": 5527.6, "FY2020": 2066.4,
        }),
        ("DATA", "Customer accounts", {
            "FY2024": 19974.2, "FY2023": 19215.8, "FY2022": 20107.9, "FY2021": 21136.4, "FY2020": 20366.3,
        }),
        ("DATA", "Fair value adjustment for hedged risk (liabilities)", {"FY2022": -34.6, "FY2021": -7.5}),
        ("DATA", "Debt securities in issue", {"FY2024": 499.3, "FY2020": 485.7}),
        ("DATA", "Derivative financial instruments", {
            "FY2024": 47.6, "FY2023": 110.3, "FY2022": 103.5, "FY2021": 148.2, "FY2020": 316.2,
        }),
        ("DATA", "Amounts owed to Co-operative Bank undertakings / parent undertakings / Finance Company", {
            "FY2024": 897.3, "FY2023": 937.6, "FY2022": 646.9, "FY2021": 402.1, "FY2020": 408.2,
        }),
        ("DATA", "Other liabilities", {
            "FY2024": 55.3, "FY2023": 44.1, "FY2022": 42.3, "FY2021": 38.0, "FY2020": 32.9,
        }),
        ("DATA", "Accruals and deferred income", {
            "FY2024": 46.6, "FY2023": 22.7, "FY2022": 32.4, "FY2021": 36.8, "FY2020": 34.8,
        }),
        ("DATA", "Provisions", {
            "FY2024": 10.1, "FY2023": 31.7, "FY2022": 33.1, "FY2021": 33.8, "FY2020": 46.0,
        }),
        ("DATA", "Lease liabilities", {
            "FY2024": 26.2, "FY2023": 30.1, "FY2022": 31.0, "FY2021": 44.1, "FY2020": 53.6,
        }),
        ("DATA", "Deferred tax liabilities", {"FY2020": 38.2}),
        ("DATA", "Net retirement benefit liability", {
            "FY2024": 5.2, "FY2023": 5.9, "FY2022": 5.9, "FY2021": 8.1, "FY2020": 8.8,
        }),
        ("TOTAL", "Total liabilities", {
            "FY2024": 24780.0, "FY2023": 25117.3, "FY2022": 27692.9, "FY2021": 28494.7, "FY2020": 26326.9,
        }),
        ("SECTION", "Equity", {}),
        ("DATA", "Ordinary share capital", {
            "FY2024": 25.6, "FY2023": 25.6, "FY2022": 25.6, "FY2021": 25.6, "FY2020": 25.6,
        }),
        ("DATA", "Share premium account", {"FY2020": 2416.9}),
        ("DATA", "Retained earnings", {
            "FY2024": 1328.6, "FY2023": 1398.2, "FY2022": 1241.1, "FY2021": 1218.8, "FY2020": -1823.6,
        }),
        ("DATA", "Other reserves", {
            "FY2024": -81.3, "FY2023": 7.9, "FY2022": 27.6, "FY2021": 502.6, "FY2020": 832.4,
        }),
        ("TOTAL", "Total equity", {
            "FY2024": 1272.9, "FY2023": 1431.7, "FY2022": 1294.3, "FY2021": 1747.0, "FY2020": 1451.3,
        }),
        ("TOTAL", "Total liabilities and equity", {
            "FY2024": 26052.9, "FY2023": 26549.0, "FY2022": 28987.2, "FY2021": 30241.7, "FY2020": 27778.2,
        }),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
bw.add_income_statement_sheet(
    title="The Co-operative Bank p.l.c. — Profit & Loss (Bank Company-only)",
    subtitle="Bank Company-only basis; bottom-line profit plus OCI detail only (see source note), £m",
    rows=[
        ("TOTAL", "Profit/(loss) for the year", {
            "FY2024": 25.4, "FY2023": 157.1, "FY2022": 22.3, "FY2021": 215.5, "FY2020": -87.4,
        }),
        ("SECTION", "Other comprehensive income/(expense), net of tax", {}),
        ("DATA", "Fair value through OCI (FVOCI) reserve movement", {
            "FY2024": -0.3, "FY2023": -2.7, "FY2022": -8.2, "FY2021": -1.9, "FY2020": 0.7,
        }),
        ("DATA", "Cash flow hedging reserve movement", {
            "FY2024": -4.4, "FY2023": -5.2, "FY2022": -4.1, "FY2021": -7.8, "FY2020": 5.8,
        }),
        ("DATA", "Defined benefit pension reserve movement", {
            "FY2024": -84.5, "FY2023": -11.8, "FY2022": -462.7, "FY2021": 89.9, "FY2020": -48.3,
        }),
        ("TOTAL", "Other comprehensive income/(expense) for the year, net of tax", {
            "FY2024": -89.2, "FY2023": -19.7, "FY2022": -475.0, "FY2021": 80.2, "FY2020": -41.8,
        }),
        ("TOTAL", "Total comprehensive income/(expense) for the year, net of tax", {
            "FY2024": -63.8, "FY2023": 137.4, "FY2022": -452.7, "FY2021": 295.7, "FY2020": -129.2,
        }),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity
# ---------------------------------------------------------------
bw.add_equity_changes_sheet(
    title="The Co-operative Bank p.l.c. — Statement of Changes in Equity (Bank Company-only)",
    subtitle="Bank Company-only basis, £m, chronological",
    headers=[
        "Share capital", "Share premium", "FVOCI reserve", "Cash flow hedging reserve",
        "Capital redemption reserve", "Defined benefit pension reserve", "Retained earnings", "Total equity",
    ],
    rows=[
        ("TOTAL", "At 1 January 2020", (25.6, 2416.9, 4.1, 16.7, 410.0, 443.4, -1736.2, 1580.5)),
        ("DATA", "Total comprehensive income/(expense) for the year (FY2020)",
         (None, None, 0.7, 5.8, None, -48.3, -87.4, -129.2)),
        ("TOTAL", "At 31 December 2020", (25.6, 2416.9, 4.8, 22.5, 410.0, 395.1, -1823.6, 1451.3)),
        ("DATA", "Total comprehensive income for the year (FY2021)",
         (None, None, -1.9, -7.8, None, 89.9, 215.5, 295.7)),
        ("DATA", "Reserve reorganisation (FY2021)",
         (None, -2416.9, None, None, -410.0, None, 2826.9, 0.0)),
        ("TOTAL", "At 31 December 2021", (25.6, 0.0, 2.9, 14.7, 0.0, 485.0, 1218.8, 1747.0)),
        ("DATA", "Total comprehensive (expense)/income for the year (FY2022)",
         (None, None, -8.2, -4.1, None, -462.7, 22.3, -452.7)),
        ("TOTAL", "At 31 December 2022", (25.6, 0.0, -5.3, 10.6, 0.0, 22.3, 1241.1, 1294.3)),
        ("DATA", "Total comprehensive income for the year (FY2023)",
         (None, None, -2.7, -5.2, None, -11.8, 157.1, 137.4)),
        ("TOTAL", "At 31 December 2023", (25.6, 0.0, -8.0, 5.4, 0.0, 10.5, 1398.2, 1431.7)),
        ("DATA", "Total comprehensive (expense)/income for the year (FY2024)",
         (None, None, -0.3, -4.4, None, -84.5, 25.4, -63.8)),
        ("DATA", "Dividends paid (FY2024)", (None, None, None, None, None, None, -95.0, -95.0)),
        ("TOTAL", "At 31 December 2024", (25.6, 0.0, -8.3, 1.0, 0.0, -74.0, 1328.6, 1272.9)),
    ],
    sources_text=STATEMENTS_SOURCES,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {
        "FY2024": 50.9, "FY2023": 105.6, "FY2022": 132.9, "FY2021": 49.4, "FY2020": -95.1,
    }),
    ("DATA", "Pension scheme adjustments", {
        "FY2024": -0.9, "FY2023": -3.4, "FY2022": -12.7, "FY2021": -5.6, "FY2020": -9.3,
    }),
    ("DATA", "Net credit impairment (gains)/losses", {
        "FY2024": -5.0, "FY2023": 0.6, "FY2022": 6.4, "FY2021": 1.1, "FY2020": 21.6,
    }),
    ("DATA", "Depreciation, amortisation and impairment", {
        "FY2024": 35.3, "FY2023": 34.8, "FY2022": 35.3, "FY2021": 36.6, "FY2020": 40.2,
    }),
    ("DATA", "Impairment of investment in subsidiaries", {
        "FY2024": 21.0, "FY2023": 0.1, "FY2022": -0.3, "FY2021": 28.6, "FY2020": -0.3,
    }),
    ("DATA", "Other non-cash movements (incl. exchange rate movements)", {
        "FY2024": 53.2, "FY2023": 54.9, "FY2022": 134.4, "FY2021": 121.4, "FY2020": 77.1,
    }),
    ("DATA", "Increase/(decrease) in deposits by banks", {
        "FY2024": -1571.7, "FY2023": -1394.5, "FY2022": 155.8, "FY2021": 3461.2, "FY2020": 922.7,
    }),
    ("DATA", "(Increase) in prepayments", {
        "FY2024": -11.6, "FY2023": -2.7, "FY2022": -1.1, "FY2021": -7.1, "FY2020": 8.4,
    }),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {
        "FY2024": 23.9, "FY2023": -9.7, "FY2022": -4.4, "FY2021": 2.0, "FY2020": -23.6,
    }),
    ("DATA", "Increase/(decrease) in customer accounts", {
        "FY2024": 759.5, "FY2023": -873.9, "FY2022": -1028.7, "FY2021": 769.2, "FY2020": 1367.9,
    }),
    ("DATA", "(Decrease) in debt securities in issue", {
        "FY2022": 0.0, "FY2021": -485.7, "FY2020": -121.9,
    }),
    ("DATA", "Decrease/(increase) in loans and advances to banks", {
        "FY2024": 25.7, "FY2023": -18.7, "FY2022": -19.9, "FY2021": -23.8, "FY2020": -16.9,
    }),
    ("DATA", "(Increase)/decrease in loans and advances to customers", {
        "FY2024": -210.7, "FY2023": 578.5, "FY2022": 31.5, "FY2021": -2358.6, "FY2020": -912.2,
    }),
    ("DATA", "Increase/(decrease) in amounts owed by Co-operative Bank undertakings", {
        "FY2024": -481.5, "FY2023": -5.5, "FY2022": -31.9, "FY2021": 1302.9, "FY2020": 132.9,
    }),
    ("DATA", "Increase/(decrease) in amounts owed to Co-operative Bank undertakings", {
        "FY2024": 70.8, "FY2023": -564.5, "FY2022": -86.0, "FY2021": -1342.7, "FY2020": -755.7,
    }),
    ("DATA", "Net movement of other assets and other liabilities", {
        "FY2024": 1.6, "FY2023": -64.5, "FY2022": -3.8, "FY2021": 49.3, "FY2020": -154.6,
    }),
    ("DATA", "Income tax paid", {
        "FY2024": -4.0, "FY2023": -2.7, "FY2022": -6.8, "FY2021": 0.0,
    }),
    ("TOTAL", "Net cash flows from/(used in) operating activities", {
        "FY2024": -1243.5, "FY2023": -2165.6, "FY2022": -699.3, "FY2021": 1598.2, "FY2020": 481.2,
    }),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase and construction of tangible and intangible assets", {
        "FY2024": -27.6, "FY2023": -55.0, "FY2022": -48.0, "FY2021": -28.9, "FY2020": -16.8,
    }),
    ("DATA", "Purchase of investment securities", {
        "FY2024": -1096.4, "FY2023": -1544.9, "FY2022": -471.6, "FY2021": -886.5, "FY2020": -969.6,
    }),
    ("DATA", "Proceeds from sale of property, plant and equipment", {
        "FY2022": 0.4, "FY2021": 1.9, "FY2020": 2.6,
    }),
    ("DATA", "Proceeds from sale of shares and other interests", {
        "FY2024": 13.6, "FY2023": 0.2, "FY2022": 20.4, "FY2021": 2.0, "FY2020": 38.6,
    }),
    ("DATA", "Proceeds from sale and maturity of investment securities", {
        "FY2024": 1972.6, "FY2023": 899.0, "FY2022": 750.8, "FY2021": 849.9, "FY2020": 2088.4,
    }),
    ("DATA", "Purchase of equity shares", {
        "FY2022": -0.8, "FY2021": -0.5,
    }),
    ("DATA", "Proceeds from sale of investment properties", {
        "FY2024": 0.2, "FY2023": 0.3, "FY2020": 0.0,
    }),
    ("DATA", "Dividends received", {
        "FY2024": 0.2, "FY2023": 6.8, "FY2022": 0.2, "FY2021": 0.3, "FY2020": 0.3,
    }),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {
        "FY2024": 862.6, "FY2023": -693.6, "FY2022": 251.4, "FY2021": -61.8, "FY2020": 1143.5,
    }),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issuance of Tier 2 notes / senior unsecured debt / MREL", {
        "FY2024": 199.1, "FY2023": 397.9, "FY2022": 248.4, "FY2020": 197.7,
    }),
    ("DATA", "Redemption of Tier 2 notes and senior unsecured debt", {
        "FY2024": -236.5, "FY2023": -163.5,
    }),
    ("DATA", "Proceeds from issuance of covered bonds", {
        "FY2024": 498.5, "FY2023": 0.0,
    }),
    ("DATA", "Interest paid on Tier 2 notes, senior unsecured debt and covered bonds", {
        "FY2024": -88.2, "FY2023": -62.7, "FY2022": -44.5, "FY2021": -37.0, "FY2020": -19.0,
    }),
    ("DATA", "Lease liability principal payments", {
        "FY2024": -5.6, "FY2023": -6.6, "FY2022": -14.6, "FY2021": -11.0, "FY2020": -10.0,
    }),
    ("DATA", "Dividends paid", {
        "FY2024": -95.0, "FY2023": 0.0,
    }),
    ("TOTAL", "Net cash flows from/(used in) financing activities", {
        "FY2024": 272.3, "FY2023": 165.1, "FY2022": 189.3, "FY2021": -48.0, "FY2020": 168.7,
    }),

    ("DATA", "Effect of exchange rate changes on cash and cash equivalents", {
        "FY2024": -8.6, "FY2023": -5.5,
    }),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2024": -117.2, "FY2023": -2699.6, "FY2022": -258.6, "FY2021": 1488.4, "FY2020": 1793.4,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2024": 2751.3, "FY2023": 5450.9, "FY2022": 5709.5, "FY2021": 4221.1, "FY2020": 2427.7,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2024": 2634.1, "FY2023": 2751.3, "FY2022": 5450.9, "FY2021": 5709.5, "FY2020": 4221.1,
    }),
    ("DATA", "Comprising: Cash and balances with central banks", {
        "FY2024": 2586.0, "FY2023": 2631.7, "FY2022": 5183.8, "FY2021": 5609.8, "FY2020": 3802.5,
    }),
    ("DATA", "Comprising: Loans and advances to banks", {
        "FY2024": 48.1, "FY2023": 119.6, "FY2022": 267.1, "FY2021": 99.7, "FY2020": 418.6,
    }),
]

bw.add_cash_flow_sheet(
    title="The Co-operative Bank p.l.c. — Statement of Cashflows (Bank Company-only)",
    subtitle="Bank Company-only basis (not the wider consolidated Group), £m",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=170,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
bw.add_asset_quality_sheet(
    title="The Co-operative Bank p.l.c. — Asset Quality (Bank Company-only)",
    subtitle="Bank Company-only basis, £m; Loans and advances to customers by IFRS 9 stage",
    rows=[
        ("SECTION", "Gross customer exposure by IFRS 9 stage", {}),
        ("DATA", "Stage 1", {
            "FY2024": 20306.9, "FY2023": 19199.2, "FY2022": 18933.0, "FY2021": 21826.2, "FY2020": 19180.3,
        }),
        ("DATA", "Stage 2", {
            "FY2024": 1415.9, "FY2023": 2421.1, "FY2022": 3692.0, "FY2021": 922.9, "FY2020": 1718.1,
        }),
        ("DATA", "Stage 3", {
            "FY2024": 114.9, "FY2023": 98.3, "FY2022": 80.3, "FY2021": 67.4, "FY2020": 63.5,
        }),
        ("DATA", "POCI (purchased or originated credit-impaired)", {
            "FY2024": 47.5, "FY2023": 55.5, "FY2022": 65.1, "FY2021": 77.3, "FY2020": 93.1,
        }),
        ("TOTAL", "Total gross customer exposure subject to ECL calculation", {
            "FY2024": 21885.2, "FY2023": 21774.1, "FY2022": 22770.4, "FY2021": 22893.8, "FY2020": 21055.0,
        }),
        ("SECTION", "Allowance for losses by IFRS 9 stage", {}),
        ("DATA", "Stage 1 allowance", {
            "FY2024": -8.4, "FY2023": -8.8, "FY2022": -11.3, "FY2021": -19.1, "FY2020": -19.1,
        }),
        ("DATA", "Stage 2 allowance", {
            "FY2024": -13.0, "FY2023": -20.7, "FY2022": -6.8, "FY2021": -13.0, "FY2020": -13.0,
        }),
        ("DATA", "Stage 3 allowance", {
            "FY2024": -7.7, "FY2023": -7.5, "FY2022": -6.9, "FY2021": -7.5, "FY2020": -7.5,
        }),
        ("DATA", "POCI allowance", {
            "FY2024": -0.2, "FY2023": -0.4, "FY2022": -0.3, "FY2021": -1.1, "FY2020": -1.1,
        }),
        ("TOTAL", "Total allowance for losses", {
            "FY2024": -29.3, "FY2023": -37.4, "FY2022": -40.4, "FY2021": -37.5, "FY2020": -40.7,
        }),
        ("SECTION", "Derived ratios", {}),
        ("DATA", "Stage 3 (NPL) ratio, % of gross exposure subject to ECL calculation", {
            "FY2024": "0.53%", "FY2023": "0.45%", "FY2022": "0.35%", "FY2021": "0.29%", "FY2020": "0.30%",
        }),
        ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross exposure)", {
            "FY2024": "6.70%", "FY2023": "7.63%", "FY2022": "8.59%", "FY2021": "11.13%", "FY2020": "11.81%",
        }),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=170,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=110)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2024": 923.5, "FY2023": 995.4, "FY2022": 947.3, "FY2021": 901.5, "FY2020": 874.9,
    })],
    p3_sources(),
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2024": "18.7%", "FY2023": "20.6%", "FY2022": "19.7%", "FY2021": "20.5%", "FY2020": "18.7%",
    })],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {
        "FY2024": 923.5, "FY2023": 995.4, "FY2022": 947.3, "FY2021": 901.5, "FY2020": 874.9,
    })],
    p3_sources(),
    note="Tier 1 capital equals CET1 capital in every year shown - the Bank holds no Additional Tier 1 (AT1) "
         "instruments at the individual entity level in this period.",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2024": "18.7%", "FY2023": "20.6%", "FY2022": "19.7%", "FY2021": "20.5%", "FY2020": "18.7%",
    })],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {
        "FY2024": 1123.9, "FY2023": 1231.8, "FY2022": 1141.5, "FY2021": 1103.7, "FY2020": 1084.9,
    })],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2024": "22.7%", "FY2023": "25.5%", "FY2022": "23.7%", "FY2021": "25.1%", "FY2020": "23.2%",
    })],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {
        "FY2024": 4950.8, "FY2023": 4830.6, "FY2022": 4806.7, "FY2021": 4399.8, "FY2020": 4668.4,
    })],
    p3_sources(),
)

bw.add_rwa_breakdown_sheet(
    title="The Co-operative Bank p.l.c. — RWA Breakdown (Bank Company-only, Individual Pillar 3 basis)",
    subtitle="UK OV1 'Overview of risk weighted exposures (Individual)', £m",
    rows=[
        ("DATA", "Credit risk (excluding CCR)", {
            "FY2024": 4143.6, "FY2023": 4132.3, "FY2022": 4178.2, "FY2021": 3743.6,
        }),
        ("DATA", "Counterparty credit risk (CCR)", {
            "FY2024": 18.2, "FY2023": 31.5, "FY2022": 37.6, "FY2021": 61.8,
        }),
        ("DATA", "Securitisation exposures in the non-trading book", {
            "FY2024": 82.3, "FY2023": 100.5, "FY2022": 95.8, "FY2021": 102.9,
        }),
        ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {
            "FY2024": 0.0, "FY2023": 0.0, "FY2022": 0.0, "FY2021": 0.0,
        }),
        ("DATA", "Operational risk", {
            "FY2024": 706.7, "FY2023": 566.3, "FY2022": 495.1, "FY2021": 491.5, "FY2020": 512.6,
        }),
        ("DATA", "Amounts below the thresholds for deduction (for information)", {
            "FY2024": 136.1, "FY2023": 205.1, "FY2022": 236.1, "FY2021": 232.6,
        }),
        ("TOTAL", "Total", {
            "FY2024": 4950.8, "FY2023": 4830.6, "FY2022": 4806.7, "FY2021": 4399.8, "FY2020": 4668.4,
        }),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=64,
    source_height=210,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio (excluding claims on central banks)", {
        "FY2024": "4.0%", "FY2023": "4.2%", "FY2022": "4.0%", "FY2021": "3.7%", "FY2020": "3.8%",
    })],
    p3_sources(),
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {
        "FY2024": "193.4%", "FY2023": "215.4%", "FY2022": "270.4%", "FY2021": "207.6%", "FY2020": "188.2%",
    })],
    p3_sources(),
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {
        "FY2024": "133.3%", "FY2023": "132.1%",
    })],
    p3_sources(),
    note="Blank FY2020-FY2022: under PS22/21 ('Implementation of Basel Standards'), UK NSFR disclosure was not "
         "required until reporting periods starting after 1 January 2024 - the Bank's own Pillar 3 templates "
         "leave these rows blank for those years, not a data gap.",
)

metric(
    "MREL Ratio", "%",
    [
        ("Total MREL resources available as a % of RWAs", {
            "FY2024": "36.0%", "FY2023": "39.1%", "FY2022": "33.2%", "FY2021": "29.6%", "FY2020": "27.5%",
        }),
        ("Total MREL resources available as a % of UK leverage exposure", {
            "FY2024": "7.7%", "FY2023": "8.0%", "FY2022": "6.8%", "FY2021": "5.4%", "FY2020": "5.6%",
        }),
    ],
    p3_sources(),
    note="The Bank's own KM2 Pillar 3 template discloses MREL adequacy on both an RWA basis and a UK leverage-"
         "exposure basis; both are shown here (the RWA-basis row is the headline figure used elsewhere in this "
         "workbook series).",
)

# ---------------------------------------------------------------
# Interim / semi-annual Pillar 3 disclosures
# ---------------------------------------------------------------
# The December 2025 report is headed and prepared for The Co-operative Bank
# p.l.c. itself. Its KM1 tables provide the current 31 December 2025 values
# on pp.4-5. The June 2025 report is deliberately represented as a gap: it is
# a Bank Holdings UK Consolidation Group disclosure, not an individual Bank
# plc disclosure, and therefore must not be mixed into this entity-level set.
INTERIM_HEADERS = [
    "Period", "Disclosure type", "Metric", "Value", "Unit", "Basis",
    "Source document", "Page / table",
]

INTERIM_ROWS = [
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Common Equity Tier 1 (CET1) capital", 968, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 1"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Tier 1 capital", 968, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 2"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total capital", 1169, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 3"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total risk-weighted exposure amount", 5112, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 4"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Common Equity Tier 1 (CET1) ratio", "18.9%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 5"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Tier 1 ratio", "18.9%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 6"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total capital ratio", "22.9%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 7"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Leverage ratio total exposure measure", 22035, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 13"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Leverage ratio", "4.4%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 14"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total high-quality liquid assets (HQLA), weighted value average", 3816, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 15"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Cash outflows, total weighted value", 2292, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, UK 16a"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Cash inflows, total weighted value", 154, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, UK 16b"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total net cash outflows, adjusted value", 2138, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 16"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Liquidity coverage ratio (LCR)", "179.8%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 17"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total available stable funding", 21719, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 18"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total required stable funding", 16129, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 19"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Net stable funding ratio (NSFR)", "134.7%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 20"),
    ("31 Dec 2025", "Year-end Pillar 3", "MREL ratio", "Not disclosed", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "No MREL table in report"),
    ("30 Jun 2025", "Half-year Pillar 3 (KM1)", "Entity-level Bank plc KM1 metrics", "Not disclosed", "n/a", "The source is Bank Holdings UK Consolidation Group, not the individual Bank plc entity", P3_2025_H1_URL, "pp.3-4, overview and Table 1"),
]

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=INTERIM_ROWS,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(INTERIM_ROWS)},
    subtitle="Entity-level semi-annual and interim Pillar 3 observations; £m unless stated",
    note=(
        "Coverage note: the 31 December 2025 report is an entity-level disclosure for The Co-operative Bank "
        "p.l.c. The 30 June 2025 report is excluded from the entity metric series because it is prepared for "
        "The Co-operative Bank Holdings p.l.c. UK Consolidation Group. MREL is not disclosed in the December "
        "2025 KM1 report. The December report's LCR is a 12-month average and NSFR is an average of the current "
        "and preceding three quarters."
    ),
)
# Keep the source register directly below the matrix so the generic verifier
# can discover it without treating the helper's spacer rows as end-of-data.
interim_ws = bw.wb["Interim Pillar 3"]
interim_ws.delete_rows(24, 2)
source_register_row = next(
    row for row in range(5, interim_ws.max_row + 1)
    if interim_ws.cell(row=row, column=1).value == "Source register"
)
for offset, source_row in enumerate(INTERIM_ROWS, start=2):
    source_cell = interim_ws.cell(row=source_register_row + offset, column=3)
    source_cell.hyperlink = source_row[6]
    source_cell.style = "Hyperlink"

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Loans and advances to customers", {
            "FY2024": 20370.8, "FY2023": 20147.5, "FY2022": 20919.1, "FY2021": 20998.3, "FY2020": 18676.7,
        }),
        ("Customer accounts", {
            "FY2024": 19974.2, "FY2023": 19215.8, "FY2022": 20107.9, "FY2021": 21136.4, "FY2020": 20366.3,
        }),
        ("Total assets", {
            "FY2024": 26052.9, "FY2023": 26549.0, "FY2022": 28987.2, "FY2021": 30241.7, "FY2020": 27778.2,
        }),
        ("Total equity", {
            "FY2024": 1272.9, "FY2023": 1431.7, "FY2022": 1294.3, "FY2021": 1747.0, "FY2020": 1451.3,
        }),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Profit/(loss) for the year", {
            "FY2024": 25.4, "FY2023": 157.1, "FY2022": 22.3, "FY2021": 215.5, "FY2020": -87.4,
        }),
        ("Other comprehensive income/(expense) for the year, net of tax", {
            "FY2024": -89.2, "FY2023": -19.7, "FY2022": -475.0, "FY2021": 80.2, "FY2020": -41.8,
        }),
        ("Total comprehensive income/(expense) for the year, net of tax", {
            "FY2024": -63.8, "FY2023": 137.4, "FY2022": -452.7, "FY2021": 295.7, "FY2020": -129.2,
        }),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {
            "FY2024": 1431.7, "FY2023": 1294.3, "FY2022": 1747.0, "FY2021": 1451.3, "FY2020": 1580.5,
        }),
        ("Total comprehensive income/(expense) for the year", {
            "FY2024": -63.8, "FY2023": 137.4, "FY2022": -452.7, "FY2021": 295.7, "FY2020": -129.2,
        }),
        ("Other movements, net", {
            "FY2024": -95.0, "FY2023": 0.0, "FY2022": 0.0, "FY2021": 0.0, "FY2020": 0.0,
        }),
        ("Closing equity", {
            "FY2024": 1272.9, "FY2023": 1431.7, "FY2022": 1294.3, "FY2021": 1747.0, "FY2020": 1451.3,
        }),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash flows from/(used in) operating activities", {
            "FY2024": -1243.5, "FY2023": -2165.6, "FY2022": -699.3, "FY2021": 1598.2, "FY2020": 481.2,
        }),
        ("Net cash flows from/(used in) investing activities", {
            "FY2024": 862.6, "FY2023": -693.6, "FY2022": 251.4, "FY2021": -61.8, "FY2020": 1143.5,
        }),
        ("Net cash flows from/(used in) financing activities", {
            "FY2024": 272.3, "FY2023": 165.1, "FY2022": 189.3, "FY2021": -48.0, "FY2020": 168.7,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2024": 2634.1, "FY2023": 2751.3, "FY2022": 5450.9, "FY2021": 5709.5, "FY2020": 4221.1,
        }),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {
            "FY2024": 18.7, "FY2023": 20.6, "FY2022": 19.7, "FY2021": 20.5, "FY2020": 18.7,
        }),
        ("Tier 1 Ratio", {
            "FY2024": 18.7, "FY2023": 20.6, "FY2022": 19.7, "FY2021": 20.5, "FY2020": 18.7,
        }),
        ("Total Capital Ratio", {
            "FY2024": 22.7, "FY2023": 25.5, "FY2022": 23.7, "FY2021": 25.1, "FY2020": 23.2,
        }),
        ("Leverage Ratio", {
            "FY2024": 4.0, "FY2023": 4.2, "FY2022": 4.0, "FY2021": 3.7, "FY2020": 3.8,
        }),
        ("LCR", {
            "FY2024": 193.4, "FY2023": 215.4, "FY2022": 270.4, "FY2021": 207.6, "FY2020": 188.2,
        }),
        ("NSFR", {
            "FY2024": 133.3, "FY2023": 132.1,
        }),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. " + ENTITY_NOTE,
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CO-OPERATIVE BANK FINANCIALS.xlsx")
print("Saved CO-OPERATIVE BANK FINANCIALS.xlsx")
