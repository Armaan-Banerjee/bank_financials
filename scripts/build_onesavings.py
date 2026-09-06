import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]
YEAR_LABEL = {y: y for y in YEARS}

AR_2025_URL = "https://find-and-update.company-information.service.gov.uk/company/07312896/filing-history/MzUyMDIyOTcwM2FkaXF6a2N4/document?download=0&format=pdf"
AR_2024_URL = "https://find-and-update.company-information.service.gov.uk/company/07312896/filing-history/MzQ2NTMxODAwN2FkaXF6a2N4/document?download=0&format=pdf"
AR_2023_URL = "https://find-and-update.company-information.service.gov.uk/company/07312896/filing-history/MzQxOTAwNzg1NWFkaXF6a2N4/document?download=0&format=pdf"
AR_2022_URL = "https://www.onesavingsbank.com/media/w3ffou5b/osbg-ara-2022.pdf"
AR_2021_URL = "https://www.onesavingsbank.com/media/5n1lklrr/onesavings-bank-plc-2021-accounts.pdf"
AR_2019_URL = "https://www.osb.co.uk/media/utofi4fl/11-osb-2019-annual-report-and-accounts.pdf"

P3_2025_URL = "https://www.onesavingsbank.com/media/hbymiii2/q4-2025-osbg-pillar-3-disclosure.pdf"
P3_2024_URL = "https://www.onesavingsbank.com/media/143pzceq/q4-2024-osbg-pillar-3-disclosure.pdf"
P3_2023_URL = "https://www.onesavingsbank.com/media/kn3nulae/q4-2023-osb-pillar-3-disclosures.pdf"
P3_2022_URL = "https://www.onesavingsbank.com/media/cqepdkda/osb-group-pillar-3-disclosures-2022.pdf"
P3_2021_URL = "https://www.onesavingsbank.com/media/iuvfpajb/osb-group-pillar-3-disclosures-2021.pdf"
P3_2020_URL = "https://www.osb.co.uk/media/xmiprmgq/download-pillar-3-disclosure-document-2020.pdf"
P3_2019_URL = "https://www.osb.co.uk/media/nwwagqwf/download-pillar-3-disclosure-document-2019.pdf"

ENTITY_NOTE = (
    "ENTITY AND BASIS NOTE: OneSavings Bank plc (Companies House 07312896, FRN 530504) is the PRA-authorised "
    "bank in scope. Cash Flow Statement figures are the Bank's Company-only column, £m, from its own statutory "
    "annual accounts. The Pillar 3 disclosures are published by OSB Group plc on a consolidated Group basis and "
    "include the Group's banking entities OneSavings Bank plc and Charter Court Financial Services Limited, plus "
    "their relevant subsidiaries; OSB does not publish a five-year OSB-bank-only Pillar 3 series. The bases are "
    "therefore intentionally different and must not be treated as a single-entity time series. The 2019 "
    "Companies House filings were scanned/image-only and were OCR'd; figures were cross-checked against the "
    "official OSB reports and the printed opening/closing cash reconciliation."
)

CASH_FLOW_SOURCES = (
    "Sources — OneSavings Bank plc (Company-only basis), Statement of Cash Flows, £m:\n"
    f"FY2025 & FY2024: OneSavings Bank plc Annual Report and Financial Statements for the year ended 31 December "
    f"2025, p.91 (Company column; FY2024 comparative) — {AR_2025_URL}\n"
    f"FY2024 & FY2023: OneSavings Bank plc Annual Report and Financial Statements for the year ended 31 December "
    f"2024, p.91 (Company column; FY2023 comparative) — {AR_2024_URL}\n"
    f"FY2023 & FY2022: OneSavings Bank plc Annual Report and Financial Statements for the year ended 31 December "
    f"2023, p.89 (Company column; FY2022 comparative) — {AR_2023_URL}\n"
    f"FY2021: OneSavings Bank plc Annual Report and Financial Statements for the year ended 31 December 2021, "
    f"p.98 (Company column) — {AR_2021_URL}\n"
    f"FY2020 & FY2019: OneSavings Bank plc Annual Report and Accounts for the year ended 31 December 2020, "
    f"p.98 (Company columns; FY2019 comparative) — https://www.onesavingsbank.com/media/03kpilxl/onesavings-bank-plc-2020-accounts.pdf; "
    f"FY2019 cross-check: 2019 Annual Report and Accounts, p.166 (Company column) — {AR_2019_URL}\n\n" + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources — OSB Group plc consolidated Pillar 3 basis (includes OneSavings Bank plc and CCFSL):\n"
        f"FY2025: Pillar 3 Disclosures 31 December 2025, p.7 (UK KM1; MREL UK KM2 on p.8; liquidity templates "
        f"on pp.31 and 34) — {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures 31 December 2024, p.9 (UK KM1; MREL UK KM2 on p.10; liquidity templates "
        f"on pp.49 and 52) — {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 31 December 2023, p.9 (UK KM1; liquidity templates on pp.46 and 49) — "
        f"{P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures 31 December 2022, pp.8-9 (UK KM1 and liquidity templates) — {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures for year ended 31 December 2021, p.8 (Table 4: Key metrics) and p.62 "
        f"(Table 47: LIQ1) — {P3_2021_URL}\n"
        f"FY2020: Pillar 3 Disclosures for year ended 31 December 2020, Table 1 — {P3_2020_URL}\n"
        f"FY2019: Pillar 3 Disclosures for year ended 31 December 2019, Table 1 p.7 — {P3_2019_URL}\n\n" + ENTITY_NOTE
    )


bw = BankWorkbook("OneSavings Bank plc", YEARS, YEAR_LABEL, header_color="1F4E78")

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. Company-only basis throughout, matching the existing Cash
# Flow Statement's basis. All 5 years tie exactly (Total assets = Total
# liabilities + Total equity; Total equity ties to the equity statement's
# own opening/closing balances - zero plug rows needed anywhere).
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources — OneSavings Bank plc (Company-only basis for Balance Sheet and Statement of Changes in "
    "Equity; OSB Group consolidated basis for Profit & Loss - Company takes the section 408 Companies Act "
    "2006 exemption from presenting its own income statement), £m:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements for the year ended 31 December 2025, "
    f"Statement of Comprehensive Income (Group) p.87, Statement of Financial Position p.88, Statement of "
    f"Changes in Equity (Group) p.89 and (Company) p.90 — {AR_2025_URL}\n"
    f"FY2023 & FY2022: Annual Report and Financial Statements for the year ended 31 December 2023, "
    f"Statement of Comprehensive Income (Group) p.85, Statement of Financial Position p.86, Statement of "
    f"Changes in Equity (Group) p.87 and (Company) p.88 — {AR_2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements for the year ended 31 December 2021, Statement of "
    f"Comprehensive Income (Group) p.94, Statement of Financial Position p.95, Statement of Changes in "
    f"Equity (Group) p.96 and (Company) p.97 — {AR_2021_URL}\n"
    f"FY2020: OneSavings Bank plc Annual Report and Financial Statements for the year ended 31 December 2020, Company comparative columns — https://www.onesavingsbank.com/media/03kpilxl/onesavings-bank-plc-2020-accounts.pdf\n"
    f"FY2019: OneSavings Bank plc Annual Report and Accounts for the year ended 31 December 2019, Statements pp.163-165 — {AR_2019_URL}\n\n" + ENTITY_NOTE
)

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash in hand", {"FY2025": 0.4, "FY2024": 0.3, "FY2023": 0.4, "FY2022": 0.4, "FY2021": 0.5}),
    ("DATA", "Loans and advances to credit institutions", {"FY2025": 1424.8, "FY2024": 1129.4, "FY2023": 1002.7, "FY2022": 1506.1, "FY2021": 1405.0}),
    ("DATA", "Investment securities", {"FY2025": 633.2, "FY2024": 528.7, "FY2023": 396.2, "FY2022": 211.4, "FY2021": 16.2}),
    ("DATA", "Loans and advances to customers", {"FY2025": 12656.1, "FY2024": 11958.8, "FY2023": 11432.2, "FY2022": 10531.9, "FY2021": 9476.4}),
    ("DATA", "Fair value adjustments on hedged assets", {"FY2025": 56.1, "FY2024": -68.7, "FY2023": -11.6, "FY2022": -200.8, "FY2021": 1.3}),
    ("DATA", "Derivative assets", {"FY2025": 60.9, "FY2024": 157.0, "FY2023": 180.8, "FY2022": 234.0, "FY2021": 50.5}),
    ("DATA", "Other assets", {"FY2025": 18.5, "FY2024": 15.2, "FY2023": 19.4, "FY2022": 13.1, "FY2021": 8.3}),
    ("DATA", "Current taxation asset", {"FY2024": 3.9, "FY2022": 2.6}),
    ("DATA", "Deferred taxation asset", {"FY2025": 7.3, "FY2024": 5.0, "FY2023": 3.8, "FY2022": 4.1, "FY2021": 4.9}),
    ("DATA", "Deemed loan assets", {"FY2025": 29.1, "FY2022": 31.2}),
    ("DATA", "Non-current assets held for sale", {"FY2025": 1.5}),
    ("DATA", "Property, plant and equipment", {"FY2025": 21.8, "FY2024": 26.3, "FY2023": 22.6, "FY2022": 20.9, "FY2021": 17.3}),
    ("DATA", "Intangible assets", {"FY2025": 66.9, "FY2024": 48.3, "FY2023": 23.8, "FY2022": 6.5, "FY2021": 7.7}),
    ("DATA", "Investments in subsidiaries and intercompany loans", {"FY2025": 4585.1, "FY2024": 4025.3, "FY2023": 3667.7, "FY2022": 3242.5, "FY2021": 3096.4}),
    ("TOTAL", "Total assets", {"FY2025": 19561.7, "FY2024": 17829.5, "FY2023": 16738.0, "FY2022": 15603.9, "FY2021": 14084.5}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Amounts owed to credit institutions", {"FY2025": 1036.5, "FY2024": 1623.5, "FY2023": 2018.3, "FY2022": 2568.5, "FY2021": 2420.7}),
    ("DATA", "Amounts owed to retail depositors", {"FY2025": 14088.3, "FY2024": 13525.4, "FY2023": 12246.5, "FY2022": 11132.2, "FY2021": 9739.4}),
    ("DATA", "Fair value adjustments on hedged liabilities", {"FY2025": 12.2, "FY2024": -2.2, "FY2023": 11.8, "FY2022": -33.7, "FY2021": -8.8}),
    ("DATA", "Amounts owed to other customers", {"FY2025": 20.0, "FY2023": 0.5, "FY2022": 0.5, "FY2021": 5.7}),
    ("DATA", "Derivative liabilities", {"FY2025": 103.4, "FY2024": 54.4, "FY2023": 123.8, "FY2022": 63.8, "FY2021": 8.7}),
    ("DATA", "Lease liabilities", {"FY2025": 2.1, "FY2024": 2.7, "FY2023": 3.4, "FY2022": 3.6, "FY2021": 3.9}),
    ("DATA", "Other liabilities", {"FY2025": 34.7, "FY2024": 28.5, "FY2023": 25.8, "FY2022": 23.9, "FY2021": 17.3}),
    ("DATA", "Provisions", {"FY2025": 2.6, "FY2024": 3.8, "FY2023": 0.4, "FY2022": 0.1, "FY2021": 1.9}),
    ("DATA", "Current taxation liability", {"FY2025": 7.6, "FY2023": 10.9, "FY2021": 2.7}),
    ("DATA", "Deferred taxation liability", {"FY2025": 18.4, "FY2024": 13.1}),
    ("DATA", "Deemed loan liabilities", {"FY2024": 3.6, "FY2023": 25.3, "FY2021": 142.8}),
    ("DATA", "Intercompany loans", {"FY2025": 1432.4, "FY2024": 28.6, "FY2023": 24.7, "FY2022": 33.3, "FY2021": 33.2}),
    ("DATA", "Senior notes", {"FY2025": 548.4, "FY2024": 466.0, "FY2023": 226.6}),
    ("DATA", "Subordinated liabilities", {"FY2025": 156.4, "FY2024": 156.4, "FY2023": 156.4, "FY2022": 63.8, "FY2021": 10.3}),
    ("DATA", "Perpetual subordinated bonds", {"FY2023": 15.2, "FY2022": 15.2, "FY2021": 15.2}),
    ("TOTAL", "Total liabilities", {"FY2025": 17463.0, "FY2024": 15903.8, "FY2023": 14889.6, "FY2022": 13807.4, "FY2021": 12393.0}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 4.5, "FY2024": 4.5, "FY2023": 4.5, "FY2022": 4.5, "FY2021": 4.5}),
    ("DATA", "Other equity instruments (AT1)", {"FY2025": 100.2, "FY2024": 90.0, "FY2023": 90.0, "FY2022": 90.0}),
    ("DATA", "Retained earnings", {"FY2025": 1975.7, "FY2024": 1817.4, "FY2023": 1741.6, "FY2022": 1690.9, "FY2021": 1587.6}),
    ("DATA", "Other reserves", {"FY2025": 18.3, "FY2024": 13.8, "FY2023": 12.3, "FY2022": 11.1, "FY2021": 99.4}),
    ("TOTAL", "Total equity", {"FY2025": 2098.7, "FY2024": 1925.7, "FY2023": 1848.4, "FY2022": 1796.5, "FY2021": 1691.5}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 19561.7, "FY2024": 17829.5, "FY2023": 16738.0, "FY2022": 15603.9, "FY2021": 14084.5}),
]

# FY2020 is the Company comparative in the 2021 accounts; FY2019 is the
# Bank column in the 2019 accounts.  Keep the statutory Company basis explicit.
_bs_history = {
    "Cash in hand": (0.5, 0.4), "Loans and advances to credit institutions": (1518.1, 1340.0),
    "Investment securities": (15.0, 58.9), "Loans and advances to customers": (8531.7, 7208.2),
    "Fair value adjustments on hedged assets": (127.4, 19.8), "Derivative assets": (4.7, 11.7),
    "Other assets": (5.7, 5.5), "Deferred taxation asset": (3.1, 1.6),
    "Property, plant and equipment": (20.5, 15.6), "Intangible assets": (7.0, 7.1),
    "Investments in subsidiaries and intercompany loans": (3137.3, 3629.4),
    "Total assets": (13374.8, 13469.9), "Amounts owed to credit institutions": (1900.5, 1671.1),
    "Amounts owed to retail depositors": (9705.3, 9435.7), "Fair value adjustments on hedged liabilities": (3.1, -0.1),
    "Amounts owed to other customers": (5.8, 8.9), "Derivative liabilities": (93.8, 54.3),
    "Lease liabilities": (3.9, 4.3), "Other liabilities": (13.8, 17.1), "Provisions": (1.6, 1.6),
    "Deemed loan liabilities": (66.2, 240.2), "Intercompany loans": (37.9, 643.9),
    "Subordinated liabilities": (10.5, 10.6), "Perpetual subordinated bonds": (37.6, 37.6),
    "Total liabilities": (11880.0, 12141.6), "Share capital": (4.5, 4.5),
    "Retained earnings": (1423.7, 407.0), "Other reserves": (66.6, 52.6),
    "Total equity": (1494.8, 1328.3), "Total liabilities and equity": (13374.8, 13469.9),
}
for _row in bs_rows:
    if _row[1] in _bs_history:
        _row[2]["FY2020"], _row[2]["FY2019"] = _bs_history[_row[1]]

bw.add_balance_sheet_sheet(
    title="OneSavings Bank plc — Balance Sheet",
    subtitle="Company-only basis, £m (matches the existing Cash Flow Statement's basis, not the OSB Group "
              "consolidated basis used by the Pillar 3 sheets - see basis note below). FY2021's own Balance "
              "Sheet does not yet break out 'Other equity instruments (AT1)' as its own line - that year's "
              "£90.0m of AT1 instruments (per the Statement of Changes in Equity) is bundled into 'Other "
              "reserves' (99.4 = 90.0 AT1 + 9.4 FVOCI/share-based reserves), confirmed by the Total equity tie; "
              "left blank on the AT1 row rather than double-counted. 'Perpetual subordinated bonds' (15.2, "
              "unchanged FY2021-FY2023) is not disclosed as its own line from FY2024 onward - either redeemed "
              "or folded into 'Subordinated liabilities' (which itself stays flat at 156.4 across FY2023-FY2025); "
              "shown as a genuine presentation change, not forced together. All 5 years' Total assets = Total "
              "liabilities + Total equity exactly.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss - OSB Group consolidated basis (the Company takes the s.408
# exemption and publishes no standalone income statement; its own Balance
# Sheet note discloses only a headline Company profit-after-tax figure each
# year - materially different from Group profit since it excludes
# subsidiary results, e.g. FY2023 Company profit after tax was £386.8m vs
# Group profit for the year of £283.6m - not blended into this sheet).
# Every year's own income/expense lines tie exactly to that year's own
# disclosed Total income, Profit before taxation, Profit for the year, and
# Total comprehensive income - zero plug rows needed anywhere.
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2025": 1914.3, "FY2024": 2099.3, "FY2023": 1767.0, "FY2022": 1069.3, "FY2021": 746.8}),
    ("DATA", "Interest payable and similar charges", {"FY2025": -1234.4, "FY2024": -1431.8, "FY2023": -1108.1, "FY2022": -359.4, "FY2021": -159.2}),
    ("TOTAL", "Net interest income", {"FY2025": 679.9, "FY2024": 667.5, "FY2023": 658.9, "FY2022": 709.9, "FY2021": 587.6}),
    ("DATA", "Fair value gains/(losses) on financial instruments", {"FY2025": -20.5, "FY2024": -1.5, "FY2023": -4.4, "FY2022": 58.9, "FY2021": 29.5}),
    ("DATA", "Gain/(loss) on sale of financial assets held at amortised cost", {"FY2025": 3.4, "FY2024": -2.4, "FY2021": 4.0}),
    ("DATA", "Other operating income", {"FY2025": 7.3, "FY2024": 3.6, "FY2023": 3.9, "FY2022": 6.6, "FY2021": 7.9}),
    ("TOTAL", "Total income", {"FY2025": 670.1, "FY2024": 667.2, "FY2023": 658.4, "FY2022": 775.4, "FY2021": 629.0}),
    ("DATA", "Administrative expenses", {"FY2025": -270.3, "FY2024": -258.1, "FY2023": -233.8, "FY2022": -206.5, "FY2021": -166.5}),
    ("DATA", "Increase/(decrease) in provisions", {"FY2025": -2.4, "FY2024": -2.7, "FY2023": -0.4, "FY2022": 1.6, "FY2021": -0.2}),
    ("DATA", "Impairment of financial assets", {"FY2025": -13.0, "FY2024": 11.7, "FY2023": -48.8, "FY2022": -29.8, "FY2021": 4.4}),
    ("DATA", "Impairment of intangible assets", {"FY2021": 3.1}),
    ("DATA", "Integration costs", {"FY2022": -7.9, "FY2021": -5.0}),
    ("DATA", "Exceptional items", {"FY2021": -0.2}),
    ("TOTAL", "Profit before taxation", {"FY2025": 384.4, "FY2024": 418.1, "FY2023": 375.4, "FY2022": 532.8, "FY2021": 464.6}),
    ("DATA", "Taxation", {"FY2025": -97.3, "FY2024": -110.0, "FY2023": -91.8, "FY2022": -121.5, "FY2021": -119.6}),
    ("TOTAL", "Profit for the year", {"FY2025": 287.1, "FY2024": 308.1, "FY2023": 283.6, "FY2022": 411.3, "FY2021": 345.0}),
    ("SECTION", "Other comprehensive (expense)/income", {}),
    ("DATA", "Fair value changes on FVOCI instruments arising in the year", {"FY2025": 1.6, "FY2024": -0.1, "FY2023": -0.2, "FY2022": 0.3, "FY2021": 1.1}),
    ("DATA", "Amounts reclassified to profit or loss for investment securities at FVOCI", {"FY2022": -0.7, "FY2021": -2.0}),
    ("DATA", "Tax on items in other comprehensive (expense)/income", {"FY2025": -0.2, "FY2023": 0.1, "FY2022": 0.1, "FY2021": 0.5}),
    ("DATA", "Revaluation of foreign operations", {"FY2025": -2.1, "FY2023": -0.8, "FY2022": -0.2, "FY2021": -0.1}),
    ("TOTAL", "Other comprehensive expense", {"FY2025": -0.7, "FY2024": -0.1, "FY2023": -0.9, "FY2022": -0.5, "FY2021": -0.5}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 286.4, "FY2024": 308.0, "FY2023": 282.7, "FY2022": 410.8, "FY2021": 344.5}),
]
_pl_history = {
    "Interest receivable and similar income": (711.9, 539.9), "Interest payable and similar charges": (-239.7, -195.2),
    "Net interest income": (472.2, 344.7), "Fair value gains/(losses) on financial instruments": (7.4, -3.3),
    "Gain/(loss) on sale of financial assets held at amortised cost": (20.0, -0.1),
    "Other operating income": (9.0, 3.4), "Total income": (508.6, 343.4),
    "Administrative expenses": (-157.1, -108.7), "Increase/(decrease) in provisions": (-0.1, 0.0),
    "Impairment of financial assets": (-71.0, -15.6), "Integration costs": (-9.8, -5.2),
    "Exceptional items": (-3.3, -15.6), "Profit before taxation": (260.3, 209.1),
    "Taxation": (-64.1, -50.3), "Profit for the year": (196.2, 158.8),
    "Fair value changes on FVOCI instruments arising in the year": (1.0, 0.8),
    "Tax on items in other comprehensive (expense)/income": (-0.5, -0.2),
    "Other comprehensive expense": (0.5, 0.0), "Total comprehensive income for the year": (196.7, 158.8),
}
for _row in pl_rows:
    if _row[1] in _pl_history:
        _row[2]["FY2020"], _row[2]["FY2019"] = _pl_history[_row[1]]

bw.add_income_statement_sheet(
    title="OneSavings Bank plc — Profit & Loss",
    subtitle="OSB Group consolidated basis, £m (the Company itself takes the section 408 Companies Act 2006 "
              "exemption and publishes no standalone income statement - see basis note below). 'Gain/(loss) on "
              "sale of financial assets held at amortised cost' is only itemised as its own line from FY2024 "
              "onward (folded into the fair value line in FY2022-FY2023's presentation); FY2021's equivalent "
              "'Gain on sale of financial instruments' line is shown on the same row. 'Impairment of intangible "
              "assets' and 'Exceptional items' are unique one-off FY2021 lines. Every year's own components tie "
              "exactly to that year's own disclosed Total income/Profit before tax/Profit for the year/Total "
              "comprehensive income.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=78,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - Company-only basis, matching the Balance
# Sheet above. Per-year reconciliation ladder confirmed: every year's own
# closing balance ties exactly to both the next year's own opening balance
# and that year's own Balance Sheet Total equity. Zero plug rows needed
# anywhere across all 5 years. Ladder's mandated scan of each year's equity
# note caught genuine "easy to skip" categories: AT1 coupon/redemption/
# issuance/transaction-costs every year, and a tax-recognised-in-equity
# line most years.
# ---------------------------------------------------------------
equity_headers = ["Share capital", "FVOCI reserve", "Share-based payment reserve", "Retained earnings",
                   "Other equity instruments (AT1)", "Total"]
equity_rows = [
    ("TOTAL", "At 31 December 2020 (FY2021 opening)", (4.5, -0.1, 6.7, 1423.7, 60.0, 1494.8)),
    ("DATA", "Profit for the year", (None, None, None, 255.1, None, 255.1)),
    ("DATA", "Other comprehensive income", (None, 0.1, None, None, None, 0.1)),
    ("DATA", "Coupon paid on AT1 securities", (None, None, None, -4.7, None, -4.7)),
    ("DATA", "Dividends paid", (None, None, None, -86.7, None, -86.7)),
    ("DATA", "Share-based payments", (None, None, 1.1, 3.7, None, 4.8)),
    ("DATA", "Redemption of AT1 securities", (None, None, None, None, -60.0, -60.0)),
    ("DATA", "Transaction costs on redemption of AT1 securities", (None, None, None, -3.5, None, -3.5)),
    ("DATA", "Issuance of AT1 securities", (None, None, None, None, 90.0, 90.0)),
    ("DATA", "Tax recognised in equity", (None, None, 1.6, None, None, 1.6)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (4.5, 0.0, 9.4, 1587.6, 90.0, 1691.5)),
    ("DATA", "Profit for the year", (None, None, None, 335.9, None, 335.9)),
    ("DATA", "Other comprehensive income", (None, 0.3, None, None, None, 0.3)),
    ("DATA", "Tax on items in other comprehensive income", (None, -0.1, None, None, None, -0.1)),
    ("DATA", "Coupon paid on AT1 securities", (None, None, None, -5.4, None, -5.4)),
    ("DATA", "Dividends paid", (None, None, None, -233.1, None, -233.1)),
    ("DATA", "Share-based payments", (None, None, 1.5, 5.9, None, 7.4)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (4.5, 0.2, 10.9, 1690.9, 90.0, 1796.5)),
    ("DATA", "Profit for the year", (None, None, None, 386.8, None, 386.8)),
    ("DATA", "Other comprehensive expense", (None, -0.2, None, None, None, -0.2)),
    ("DATA", "Tax on items in other comprehensive expense", (None, 0.1, None, None, None, 0.1)),
    ("DATA", "Coupon paid on AT1 securities", (None, None, None, -5.4, None, -5.4)),
    ("DATA", "Dividends paid", (None, None, None, -335.0, None, -335.0)),
    ("DATA", "Share-based payments", (None, None, 0.9, 4.3, None, 5.2)),
    ("DATA", "Tax recognised in equity", (None, None, 0.4, None, None, 0.4)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (4.5, 0.1, 12.2, 1741.6, 90.0, 1848.4)),
    ("DATA", "Profit for the year", (None, None, None, 295.8, None, 295.8)),
    ("DATA", "Other comprehensive expense", (None, -0.1, None, None, None, -0.1)),
    ("DATA", "Coupon paid on AT1 securities", (None, None, None, -5.4, None, -5.4)),
    ("DATA", "Dividends paid", (None, None, None, -218.7, None, -218.7)),
    ("DATA", "Share-based payments", (None, None, 1.4, 4.1, None, 5.5)),
    ("DATA", "Tax recognised in equity", (None, None, 0.2, None, None, 0.2)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (4.5, 0.0, 13.8, 1817.4, 90.0, 1925.7)),
    ("DATA", "Profit for the year", (None, None, None, 381.7, None, 381.7)),
    ("DATA", "Other comprehensive income", (None, 0.8, None, None, None, 0.8)),
    ("DATA", "Tax on items in other comprehensive income", (None, -0.2, None, None, None, -0.2)),
    ("DATA", "Coupon paid on AT1 securities", (None, None, None, -6.1, None, -6.1)),
    ("DATA", "Dividends paid", (None, None, None, -219.0, None, -219.0)),
    ("DATA", "Share-based payments", (None, None, 1.6, 4.1, None, 5.7)),
    ("DATA", "Redemption of AT1 securities", (None, None, None, -0.2, -79.8, -80.0)),
    ("DATA", "Issuance of AT1 securities", (None, None, None, None, 90.0, 90.0)),
    ("DATA", "Transaction costs on issuance of AT1 securities", (None, None, None, -0.6, None, -0.6)),
    ("DATA", "Tax recognised in equity", (None, None, 2.3, None, None, 2.3)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (4.5, 0.6, 17.7, 1975.7, 100.2, 2098.7)),
]

bw.add_equity_changes_sheet(
    title="OneSavings Bank plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, Company-only basis, £m. Equity reconciliation ladder "
              "confirmed: every year's own closing balance ties exactly to both the next year's own opening "
              "balance and that year's own Balance Sheet Total equity - zero plug rows needed anywhere across "
              "all 5 years.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
)

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": 415.6, "FY2024": 345.9, "FY2023": 446.9, "FY2022": 387.3, "FY2021": 314.5}),
    ("DATA", "Adjustments for non-cash and other items", {"FY2025": 131.2, "FY2024": 126.3, "FY2023": 153.1, "FY2022": 68.6, "FY2021": 12.2}),
    ("DATA", "Changes in operating assets and liabilities", {"FY2025": 563.7, "FY2024": 521.6, "FY2023": -402.4, "FY2022": 276.6, "FY2021": -817.4}),
    ("SECTION", "Net operating cash flow reconciliation", {}),
    ("DATA", "Cash generated in operating activities", {"FY2025": 1110.5, "FY2024": 993.8, "FY2023": 197.6, "FY2022": 732.5, "FY2021": -490.7}),
    ("DATA", "Provisions paid", {"FY2025": -3.3}),
    ("DATA", "Net tax paid", {"FY2025": -10.8, "FY2024": -52.3, "FY2023": -46.3, "FY2022": -54.0, "FY2021": -53.2}),
    ("TOTAL", "Net cash generated from operating activities", {"FY2025": 1096.4, "FY2024": 941.5, "FY2023": 151.3, "FY2022": 678.5, "FY2021": -543.9}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Maturity and sales of investment securities", {"FY2025": 303.7, "FY2024": 428.9, "FY2023": 317.5, "FY2022": 451.0, "FY2021": 215.4}),
    ("DATA", "Purchases of investment securities", {"FY2025": -405.7, "FY2024": -559.8, "FY2023": -592.0, "FY2022": -556.4, "FY2021": -216.6}),
    ("DATA", "Interest received on investment securities", {"FY2025": 22.7, "FY2024": 23.5, "FY2023": 16.3, "FY2022": 3.0, "FY2021": 0.2}),
    ("DATA", "Sales of financial instruments", {"FY2021": 0.3}),
    ("DATA", "Investments in subsidiaries", {"FY2023": 0, "FY2022": -3.2}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 1.1, "FY2021": 2.0}),
    ("DATA", "Purchases of property, plant and equipment and intangible assets", {"FY2025": -29.6, "FY2024": -34.0, "FY2023": -24.4, "FY2022": -7.2, "FY2021": -5.0}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": -107.8, "FY2024": -141.4, "FY2023": -282.6, "FY2022": -112.8, "FY2021": -3.7}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Financing received", {"FY2025": 1377.2, "FY2024": 527.0, "FY2023": 578.7, "FY2022": 120.0, "FY2021": 3163.6}),
    ("DATA", "Financing repaid", {"FY2025": -1805.9, "FY2024": -764.2, "FY2023": -597.2, "FY2022": -304.1, "FY2021": -2589.1}),
    ("DATA", "Interest paid on financing", {"FY2025": -110.9, "FY2024": -145.4, "FY2023": -107.7, "FY2022": -25.5, "FY2021": -6.6}),
    ("DATA", "Dividends paid", {"FY2025": -219.0, "FY2024": -218.7, "FY2023": -335.0, "FY2022": -233.1, "FY2021": -86.7}),
    ("DATA", "Coupon paid on AT1 securities", {"FY2024": -5.4, "FY2023": -5.4, "FY2022": -5.4, "FY2021": -4.7}),
    ("DATA", "Net swap interest paid on subordinated liabilities and senior notes", {"FY2024": -2.7}),
    ("DATA", "Net swap interest paid on structural hedge", {"FY2024": -2.1}),
    ("DATA", "Redemption of AT1 securities", {"FY2025": -80.0, "FY2021": -63.5}),
    ("DATA", "Issuance of AT1 securities", {"FY2025": 89.4, "FY2021": 90.0}),
    ("DATA", "Repayments of principal portion of lease liabilities", {"FY2024": -0.5, "FY2023": -0.7, "FY2022": -0.8, "FY2021": -0.7}),
    ("DATA", "Other financing activities", {"FY2025": -10.0}),
    ("DATA", "Proceeds from issuance of shares under employee SAYE scheme", {"FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": -759.2, "FY2024": -612.0, "FY2023": -467.3, "FY2022": -448.9, "FY2021": 502.3}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": 229.4, "FY2024": 188.1, "FY2023": -598.6, "FY2022": 116.8, "FY2021": -45.3}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 1038.6, "FY2024": 850.5, "FY2023": 1449.1, "FY2022": 1332.3, "FY2021": 1377.6}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 1268.0, "FY2024": 1038.6, "FY2023": 850.5, "FY2022": 1449.1, "FY2021": 1332.3}),
]
_cf_history = {
    "Profit before taxation": (197.3, 189.4), "Adjustments for non-cash and other items": (39.2, 26.8),
    "Changes in operating assets and liabilities": (-573.7, -577.4),
    "Cash generated in operating activities": (-337.2, -361.2), "Net tax paid": (-53.6, -32.4),
    "Provisions paid": (0.0, -0.2), "Net cash generated from operating activities": (-390.8, -393.8),
    "Maturity and sales of investment securities": (291.1, 349.0), "Purchases of investment securities": (-205.9, -389.9),
    "Interest received on investment securities": (0.4, 0.0), "Sales of financial instruments": (248.9, 0.0),
    "Purchases of property, plant and equipment and intangible assets": (-4.3, -6.7),
    "Net cash from investing activities": (330.2, -47.6), "Financing received": (1060.2, 602.2),
    "Financing repaid": (-764.7, -275.0), "Interest paid on financing": (-9.8, -2.5),
    "Dividends paid": (0.0, -37.3), "Coupon paid on AT1 securities": (-5.5, -5.5),
    "Repayments of principal portion of lease liabilities": (-0.6, -0.8),
    "Proceeds from issuance of shares under employee SAYE scheme": (2.6, 0.4),
    "Net cash from financing activities": (281.6, 281.1), "Net (decrease)/increase in cash and cash equivalents": (221.0, -160.3),
    "Cash and cash equivalents at the beginning of the year": (1156.6, 1316.9),
    "Cash and cash equivalents at the end of the year": (1377.6, 1156.6),
}
for _row in rows:
    if _row[1] in _cf_history:
        _row[2]["FY2020"], _row[2]["FY2019"] = _cf_history[_row[1]]

bw.add_cash_flow_sheet("OneSavings Bank plc — Statement of Cash Flows", "Company-only basis, £m. Pillar 3 sheets are OSB Group consolidated; see source note.", rows, CASH_FLOW_SOURCES, first_col_width=72, source_height=260, unit_suffix=" (£m)")

# ---------------------------------------------------------------
# Asset Quality - OSB Group consolidated Pillar 3 basis (UK CR1 template's
# "Loans and advances" row), £m, matching the basis of the other Pillar 3
# sheets below rather than the Company-only Balance Sheet above. Every
# year's own gross carrying amount, stage split and accumulated impairment
# figures are transcribed exactly as disclosed in that year's own UK CR1
# table; NPL ratio and coverage ratio are derived from those same figures.
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources — OSB Group plc consolidated Pillar 3 basis, UK CR1 (Performing and non-performing exposures "
    "and related provisions), 'Loans and advances' row only:\n"
    f"FY2025: Pillar 3 Disclosures 31 December 2025, p.38 — {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosures 31 December 2024, p.56 — {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosures 31 December 2023, p.53 — {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosures 31 December 2022, p.44 — {P3_2022_URL}\n"
    f"FY2021: Pillar 3 Disclosures for year ended 31 December 2021, Table 25, p.44 — {P3_2021_URL}\n\n"
    + ENTITY_NOTE
)

aq_rows = [
    ("SECTION", "Loans and advances, gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 21689.5, "FY2024": 20177.2, "FY2023": 21017.9, "FY2022": 19033.2, "FY2021": 20950.7}),
    ("DATA", "Stage 2 (performing)", {"FY2025": 3821.4, "FY2024": 4352.0, "FY2023": 4524.3, "FY2022": 4411.5, "FY2021": 2408.6}),
    ("DATA", "Non-performing (predominantly Stage 3)", {"FY2025": 1061.9, "FY2024": 1009.7, "FY2023": 796.5, "FY2022": 595.4, "FY2021": 564.6}),
    ("TOTAL", "Total loans and advances, gross carrying amount", {"FY2025": 25522.3, "FY2024": 24541.8, "FY2023": 25555.4, "FY2022": 23459.1, "FY2021": 23359.3}),
    ("SECTION", "Accumulated impairment", {}),
    ("DATA", "On performing exposures (Stage 1 + Stage 2)", {"FY2025": -46.0, "FY2024": -53.3, "FY2023": -77.0, "FY2022": -58.4, "FY2021": -39.7}),
    ("DATA", "On non-performing exposures", {"FY2025": -77.0, "FY2024": -73.6, "FY2023": -68.8, "FY2022": -71.6, "FY2021": -61.8}),
    ("TOTAL", "Net carrying amount", {"FY2025": 25399.3, "FY2024": 24414.9, "FY2023": 25409.6, "FY2022": 23329.1, "FY2021": 23257.8}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL ratio (non-performing / total gross carrying amount)", {"FY2025": "4.16%", "FY2024": "4.11%", "FY2023": "3.12%", "FY2022": "2.54%", "FY2021": "2.42%"}),
    ("DATA", "Coverage ratio (accumulated impairment on non-performing / non-performing gross)", {"FY2025": "7.25%", "FY2024": "7.29%", "FY2023": "8.64%", "FY2022": "12.03%", "FY2021": "10.95%"}),
]

bw.add_asset_quality_sheet(
    title="OneSavings Bank plc — Asset Quality",
    subtitle="OSB Group consolidated Pillar 3 basis, £m ('Loans and advances' row of the UK CR1 template only - "
              "excludes cash balances at central banks and debt securities, which the same table shows as 100% "
              "Stage 1/performing every year). NPL and coverage ratios are derived from the disclosed figures, "
              "not separately disclosed by the Group.",
    rows=aq_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=200,
    unit_suffix=" (£m)",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"OSB Group consolidated basis, {unit}" if unit else "OSB Group consolidated basis", rows_data, p3_sources(), note=note, first_col_width=50, source_height=190)


metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1975.8, "FY2024": 1946.4, "FY2023": 1905.7, "FY2022": 1920.7, "FY2021": 1781.7})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "15.8%", "FY2024": "16.3%", "FY2023": "16.1%", "FY2022": "18.3%", "FY2021": "19.6%"})])
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 2142.9, "FY2024": 2096.4, "FY2023": 2055.7, "FY2022": 2070.7, "FY2021": 1931.7})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "17.1%", "FY2024": "17.6%", "FY2023": "17.4%", "FY2022": "19.7%", "FY2021": "21.2%"})])
metric("Total Capital", "£m", [("Total capital", {"FY2025": 2392.9, "FY2024": 2346.4, "FY2023": 2305.7, "FY2022": 2070.7, "FY2021": 1931.7})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "19.1%", "FY2024": "19.7%", "FY2023": "19.5%", "FY2022": "19.7%", "FY2021": "21.2%"})])
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", {"FY2025": 12541.7, "FY2024": 11915.7, "FY2023": 11845.6, "FY2022": 10494.7, "FY2021": 9101.6})])

# ---------------------------------------------------------------
# RWA Breakdown - UK OV1 template, OSB Group consolidated Pillar 3 basis,
# £m. FY2021's figures are the Group's own FY2021 comparative column as
# republished in the FY2022 Pillar 3 disclosure (its own FY2021 report's
# OV1 table wasn't reachable this session in the same format - the FY2022
# document's own comparative is used instead of a separate lookup, per the
# existing metric()s' established source pattern). "Amounts below the
# thresholds for deduction" is a memo/information-only line every year -
# confirmed non-additive by cross-checking Credit risk + CCR +
# Securitisation + Operational risk sums to the disclosed Total exactly
# (within rounding) in all 5 years.
# ---------------------------------------------------------------
RWA_BREAKDOWN_SOURCES = (
    "Sources — OSB Group plc consolidated Pillar 3 basis, UK OV1 (Overview of risk weighted exposure amounts):\n"
    f"FY2025: Pillar 3 Disclosures 31 December 2025, p.9 — {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosures 31 December 2024, p.11 — {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosures 31 December 2023, p.11 — {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosures 31 December 2022, p.10-11 — {P3_2022_URL}\n"
    f"FY2021: FY2021 comparative column as republished in the Pillar 3 Disclosures 31 December 2022, p.10-11 "
    f"(the FY2021 disclosure's own UK OV1 table was not reachable in the same format this session) — "
    f"{P3_2022_URL}\n\n" + ENTITY_NOTE
)

rwa_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 11382.2, "FY2024": 10631.1, "FY2023": 10605.3, "FY2022": 9496.8, "FY2021": 8298.0}),
    ("DATA", "Counterparty credit risk (CCR, including CVA)", {"FY2025": 44.5, "FY2024": 106.4, "FY2023": 177.2, "FY2022": 5.3, "FY2021": 44.7}),
    ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {"FY2025": 126.4, "FY2024": 137.1, "FY2023": 39.1, "FY2022": 32.9, "FY2021": 31.2}),
    ("DATA", "Operational risk", {"FY2025": 988.6, "FY2024": 1041.2, "FY2023": 1023.9, "FY2022": 959.6, "FY2021": 727.7}),
    ("DATA", "Amounts below the thresholds for deduction (memo, not additive)", {"FY2025": 8.7, "FY2024": 6.0, "FY2023": 3.6, "FY2022": 4.6, "FY2021": 13.2}),
    ("TOTAL", "Total", {"FY2025": 12541.7, "FY2024": 11915.7, "FY2023": 11845.6, "FY2022": 10494.7, "FY2021": 9101.6}),
]

bw.add_rwa_breakdown_sheet(
    title="OneSavings Bank plc — RWA Breakdown",
    subtitle="OSB Group consolidated Pillar 3 basis, £m. 'Amounts below the thresholds for deduction' is "
              "disclosed as a memo/information-only line every year, not included in the Total - confirmed by "
              "Credit risk + CCR + Securitisation + Operational risk summing to the disclosed Total exactly "
              "(within rounding) in all 5 years.",
    rows=rwa_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£m)",
)

metric("Leverage Ratio", "£m / %", [("Total exposure measure excluding claims on central banks", {"FY2025": 28956.3, "FY2024": 27322.9, "FY2023": 27438.8, "FY2022": 24725.4}), ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "7.4%", "FY2024": "7.7%", "FY2023": "7.5%", "FY2022": "8.4%", "FY2021": "7.9%"})], "FY2021 uses the pre-UK-KM1 disclosure's Group leverage ratio and does not provide a comparable exposure-measure amount; the 2022 report notes a like-for-like FY2021 exposure measure of £21,742.2m and ratio of 8.9%, but the workbook preserves the FY2021 as-reported 7.9% ratio rather than mixing bases.")
metric("LCR", "£m / %", [("Total high-quality liquid assets (HQLA), weighted value average", {"FY2025": 3181.5, "FY2024": 3351.8, "FY2023": 3078.0, "FY2022": 2907.1}), ("Total net cash outflows (adjusted value)", {"FY2025": 1898.6, "FY2024": 1794.3, "FY2023": 1565.6, "FY2022": 1491.5}), ("Liquidity Coverage Ratio (%)", {"FY2025": "169.5%", "FY2024": "188.0%", "FY2023": "197.1%", "FY2022": "197.0%", "FY2021": "195.5%"})], "FY2021's pre-UK-KM1 disclosure provides only the Group LCR percentage in Table 4; HQLA and adjusted net-outflow amounts are not disclosed on a directly comparable annual basis. FY2022 onward uses the 12-month average template (the 2022 disclosure restates prior LCR methodology).")
metric("NSFR", "£m / %", [("Total available stable funding", {"FY2025": 26596.3, "FY2024": 27138.8, "FY2023": 26087.0}), ("Total required stable funding", {"FY2025": 18911.8, "FY2024": 20051.6, "FY2023": 19638.6}), ("NSFR ratio (%)", {"FY2025": "140.6%", "FY2024": "135.4%", "FY2023": "132.8%"})], "FY2022's Pillar 3 report states that NSFR disclosures were not due until 1 January 2023; FY2021 likewise has no NSFR disclosure. The FY2023 table does not provide a 31 Dec 2022 comparative, so those cells remain blank.")
metric("MREL Ratio", None, [("MREL resources as a percentage of total risk-weighted assets", {"FY2025": "24.7%", "FY2024": "25.6%"})], "Numeric MREL ratio is disclosed in UK KM2 for FY2025 and FY2024 only. FY2023's Pillar 3 report discusses the 18% requirement but does not provide a year-end MREL-resource ratio; FY2022 and FY2021 do not provide a comparable numeric MREL ratio. Those years are left blank rather than inferred.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 19561.7, "FY2024": 17829.5, "FY2023": 16738.0, "FY2022": 15603.9, "FY2021": 14084.5}),
        ("Loans and advances to customers", {"FY2025": 12656.1, "FY2024": 11958.8, "FY2023": 11432.2, "FY2022": 10531.9, "FY2021": 9476.4}),
        ("Amounts owed to retail depositors", {"FY2025": 14088.3, "FY2024": 13525.4, "FY2023": 12246.5, "FY2022": 11132.2, "FY2021": 9739.4}),
        ("Total equity", {"FY2025": 2098.7, "FY2024": 1925.7, "FY2023": 1848.4, "FY2022": 1796.5, "FY2021": 1691.5}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 670.1, "FY2024": 667.2, "FY2023": 658.4, "FY2022": 775.4, "FY2021": 629.0}),
        ("Administrative expenses", {"FY2025": -270.3, "FY2024": -258.1, "FY2023": -233.8, "FY2022": -206.5, "FY2021": -166.5}),
        ("Profit for the year", {"FY2025": 287.1, "FY2024": 308.1, "FY2023": 283.6, "FY2022": 411.3, "FY2021": 345.0}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1925.7, "FY2024": 1848.4, "FY2023": 1796.5, "FY2022": 1691.5, "FY2021": 1494.8}),
        ("Total comprehensive income for the year", {"FY2025": 286.4, "FY2024": 308.0, "FY2023": 282.7, "FY2022": 410.8, "FY2021": 344.5}),
        ("Other equity movements, net", {"FY2025": -113.4, "FY2024": -230.7, "FY2023": -230.8, "FY2022": -305.8, "FY2021": -147.8}),
        ("Closing equity", {"FY2025": 2098.7, "FY2024": 1925.7, "FY2023": 1848.4, "FY2022": 1796.5, "FY2021": 1691.5}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash generated from operating activities", {"FY2025": 1096.4, "FY2024": 941.5, "FY2023": 151.3, "FY2022": 678.5, "FY2021": -543.9}),
        ("Net cash from investing activities", {"FY2025": -107.8, "FY2024": -141.4, "FY2023": -282.6, "FY2022": -112.8, "FY2021": -3.7}),
        ("Net cash from financing activities", {"FY2025": -759.2, "FY2024": -612.0, "FY2023": -467.3, "FY2022": -448.9, "FY2021": 502.3}),
        ("Cash and cash equivalents at end of year", {"FY2025": 1268.0, "FY2024": 1038.6, "FY2023": 850.5, "FY2022": 1449.1, "FY2021": 1332.3}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.8%", "FY2024": "16.3%", "FY2023": "16.1%", "FY2022": "18.3%", "FY2021": "19.6%"}),
        ("Tier 1 Ratio", {"FY2025": "17.1%", "FY2024": "17.6%", "FY2023": "17.4%", "FY2022": "19.7%", "FY2021": "21.2%"}),
        ("Total Capital Ratio", {"FY2025": "19.1%", "FY2024": "19.7%", "FY2023": "19.5%", "FY2022": "19.7%", "FY2021": "21.2%"}),
        ("Leverage Ratio", {"FY2025": "7.4%", "FY2024": "7.7%", "FY2023": "7.5%", "FY2022": "8.4%", "FY2021": "7.9%"}),
        ("LCR", {"FY2025": "169.5%", "FY2024": "188.0%", "FY2023": "197.1%", "FY2022": "197.0%", "FY2021": "195.5%"}),
        ("NSFR", {"FY2025": "140.6%", "FY2024": "135.4%", "FY2023": "132.8%"}),
    ],
    note="Cash flows are OneSavings Bank plc Company-only; Pillar 3 metrics are OSB Group consolidated. See the basis note on each sheet.",
)

bw.save("/Users/armaan/code/katalysis/banks/ONESAVINGS FINANCIALS.xlsx")
