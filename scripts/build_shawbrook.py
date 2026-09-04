import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

Y=["FY2025","FY2024","FY2023","FY2022","FY2021"]
AR={"FY2025":"https://www.shawbrook.co.uk/media/vkkpos4a/shawbrook-bank-limited-2025-annual-report-accounts.pdf","FY2024":"https://www.shawbrook.co.uk/media/jhujcnzh/shawbrook-bank-limited-2024-annual-report-accounts.pdf","FY2023":"https://www.shawbrook.co.uk/media/iflapcxl/shawbrook-bank-ltd-annual-report-and-accounts-2023.pdf","FY2022":"https://www.shawbrook.co.uk/media/wttf0kdt/2022-shawbrook-bank-limited-annual-report-and-accounts.pdf","FY2021":"https://www.shawbrook.co.uk/media/ft4eulfp/shawbrook-bank-ara-2021.pdf"}
P3={"FY2025":"https://www.shawbrook.co.uk/media/w5chxn4q/shawbrook-pillar-3-disclosures-2025.pdf","FY2024":"https://www.shawbrook.co.uk/media/rzpdavyj/shawbrook-2024-pillar-3-disclosures.pdf","FY2023":"https://www.shawbrook.co.uk/media/wrpglj2h/shawbrook-pillar-3-disclosures-2023.pdf","FY2022":"https://www.shawbrook.co.uk/media/pljhf2fo/2022-shawbrook-pillar-3-disclosures.pdf","FY2021":"https://www.shawbrook.co.uk/media/hlbpmnjm/pillar-3-2021.pdf"}
def d(vals): return dict(zip(Y,vals))
note=("Shawbrook Bank Limited (Companies House 00388466; FRN 204574; LEI 213800XSHRKUIZK86B68) is the matched legal entity. "
"Cash flows use the Company column, £m, from the Bank's consolidated-and-company accounts. Bank-specific Pillar 3 metrics are used for FY2021-FY2024. "
"The FY2025 Pillar 3 publication is Group-only after the listing and is not substituted for Bank data. FY2022 RWA/capital comparatives use the restatement in the 2023 Pillar 3 disclosure; FY2021 and FY2022 leverage bases differ.")
cf="Sources - Shawbrook Bank Limited Company cash flows (£m):\n"+"\n".join(f"{y}: Annual Report and Accounts cash-flow statement, p.{({'FY2021':106,'FY2022':98,'FY2023':111,'FY2024':107,'FY2025':114}[y])}, {AR[y]}" for y in Y)+"\n\n"+note
b=BankWorkbook(bank_name="Shawbrook Bank Limited",years=Y,header_color="FE1270")

# ---------------------------------------------------------------
# Statement sources shared by Balance Sheet / P&L / Statement of Changes in
# Equity. Balance Sheet and Equity use the Company column (consistent with
# the existing Company-basis Cash Flow Statement); P&L is necessarily
# Group/Consolidated basis - the Company takes the s.408 Companies Act 2006
# exemption and does not publish a standalone income statement, only a
# single disclosed after-tax profit figure each year (documented below).
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - Shawbrook Bank Limited:\n"
    f"FY2025: Annual Report and Accounts 2025, Consolidated and Company statement of financial position p.111, "
    f"Company statement of changes in equity p.113, Consolidated statement of profit and loss and other "
    f"comprehensive income (Group basis) p.110 - {AR['FY2025']}\n"
    f"FY2024: Annual Report and Accounts 2024, Consolidated and Company statement of financial position p.104, "
    f"Company statement of changes in equity p.106, Consolidated statement of profit and loss and other "
    f"comprehensive income (Group basis) p.103 - {AR['FY2024']}\n"
    f"FY2023: Annual Report and Accounts 2023, Consolidated and Company statement of financial position p.108, "
    f"Company statement of changes in equity p.110, Consolidated statement of profit and loss p.106 and "
    f"Consolidated statement of comprehensive income p.107 (Group basis) - {AR['FY2023']}\n"
    f"FY2022: Annual Report and Accounts 2022, Consolidated and Company statement of financial position p.95, "
    f"Company statement of changes in equity p.97, Consolidated statement of profit and loss p.93 and "
    f"Consolidated statement of comprehensive income p.94 (Group basis) - {AR['FY2022']}\n"
    f"FY2021: Annual Report and Accounts 2021, Consolidated and Company statement of financial position p.104, "
    f"Company statement of changes in equity p.105, Consolidated statement of profit and loss and other "
    f"comprehensive income (Group basis) p.103 - {AR['FY2021']}\n\n" + note +
    "\n\nPRESENTATION NOTE: the Company has taken the exemption in s.408 Companies Act 2006 not to present its "
    "own individual income statement, so the P&L sheet is necessarily Group/Consolidated basis (the only fully "
    "disclosed income statement each year), while the Balance Sheet and Statement of Changes in Equity sheets "
    "use the Company column to stay consistent with the existing Company-basis Cash Flow Statement. Each year's "
    "Balance Sheet report also separately discloses the Company's own after-tax profit figure in a footnote "
    "(FY2025: £189.2m; FY2024: £203.2m; FY2023: £246.4m; FY2022: £213.0m; FY2021: £153.5m) - these Company "
    "profit figures do NOT equal the Group P&L's 'Profit after tax' shown on the P&L sheet (FY2025: £194.9m; "
    "FY2024: £219.8m; FY2023: £212.6m; FY2022: £179.7m; FY2021: £149.5m), a genuine Group-vs-Company difference, "
    "not an error - the Statement of Changes in Equity sheet's 'Profit for the year' rows correctly use the "
    "Company's own profit figures, ticking exactly to Company Total equity."
)

# ---------------------------------------------------------------
# Balance Sheet (Consolidated and Company statement of financial position) -
# Company column throughout. Total assets = Total liabilities + Total
# equity for every year; Total equity ties exactly to the Statement of
# Changes in Equity sheet's own opening/closing balances - zero plug rows.
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", d([1924.5, 2244.7, 2188.1, 2037.1, 1693.8])),
    ("DATA", "Loans and advances to banks", d([200.2, 248.8, 337.5, 199.9, 49.0])),
    ("DATA", "Loans and advances to customers", d([17801.1, 15129.4, 13157.9, 10472.8, 8278.9])),
    ("DATA", "Investment securities", d([2164.8, 1449.3, 816.3, 716.8, 614.8])),
    ("DATA", "Derivative financial assets", d([64.1, 151.8, 182.1, 271.6, 21.5])),
    ("DATA", "Current tax receivable", d([12.3, 17.9, None, None, 4.2])),
    ("DATA", "Property, plant and equipment", d([54.0, 64.3, 38.9, 47.8, 47.8])),
    ("DATA", "Intangible assets", d([60.9, 56.2, 51.6, 45.6, 44.3])),
    ("DATA", "Deferred tax assets", d([None, None, 5.4, 11.3, 9.2])),
    ("DATA", "Assets held for sale", d([None, None, None, None, 299.7])),
    ("DATA", "Other assets", d([55.6, 55.0, 50.4, 35.5, 17.5])),
    ("DATA", "Deemed loan due from structured entities", d([52.8, 131.0, 214.1, 93.4, None])),
    ("DATA", "Investment in subsidiaries", d([145.4, 80.6, 58.6, 13.9, 13.9])),
    ("TOTAL", "Total assets", d([22535.7, 19629.0, 17100.9, 13945.7, 11094.6])),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Amounts due to banks", d([1430.6, 1372.1, 1397.6, 1498.7, 1200.7])),
    ("DATA", "Customer deposits", d([18353.5, 15804.0, 13562.7, 10914.5, 8358.6])),
    ("DATA", "Provisions", d([8.3, 11.5, 15.9, 6.0, 14.2])),
    ("DATA", "Derivative financial liabilities", d([93.2, 117.1, 184.5, 90.5, 7.9])),
    ("DATA", "Current tax liabilities", d([None, None, 0.2, 3.6, None])),
    ("DATA", "Lease liabilities", d([24.4, 25.0, 5.2, 7.1, 9.4])),
    ("DATA", "Deferred tax liabilities", d([14.5, 7.1, None, None, None])),
    ("DATA", "Other liabilities", d([188.3, 122.4, 85.4, 58.5, 60.7])),
    ("DATA", "Subordinated debt liability", d([171.5, 171.2, 188.8, 97.4, 97.5])),
    ("DATA", "Deemed loan due to structured entities", d([375.7, 388.5, 269.2, 133.0, 402.8])),
    ("TOTAL", "Total liabilities", d([20660.0, 18018.9, 15709.5, 12809.3, 10151.8])),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", d([225.5, 175.5, 175.5, 175.5, 175.5])),
    ("DATA", "Share premium account", d([81.0, 81.0, 81.0, 81.0, 81.0])),
    ("DATA", "Capital securities", d([125.0, 125.0, 125.0, 125.0, 125.0])),
    ("DATA", "Merger reserve", d([1.6, 1.6, 1.6, 1.6, 1.6])),
    ("DATA", "Capital contribution reserve", d([39.7, 39.7, 39.0, 24.0, 23.9])),
    ("DATA", "Cash flow hedging reserve", d([1.3, 0.1, 0.1, None, None])),
    ("DATA", "Fair value through other comprehensive income reserve", d([43.8, 29.6, -0.3, -10.7, None])),
    ("DATA", "Retained earnings", d([1357.8, 1157.6, 969.5, 740.0, 535.8])),
    ("TOTAL", "Total equity", d([1875.7, 1610.1, 1391.4, 1136.4, 942.8])),
    ("TOTAL", "Total liabilities and equity", d([22535.7, 19629.0, 17100.9, 13945.7, 11094.6])),
]

b.add_balance_sheet_sheet(
    title="Shawbrook Bank Limited — Balance Sheet",
    subtitle="Company/entity basis, £m; FY2021-FY2025 calendar year-ends. Total assets = Total liabilities + "
              "Total equity for every year; Total equity ties exactly to the Statement of Changes in Equity "
              "sheet's own opening/closing balances - zero plug rows.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss (Consolidated statement of profit and loss and other
# comprehensive income) - Group/Consolidated basis (see PRESENTATION NOTE
# above). FY2021 uses the Bank's own FY2021 Annual Report figures (not the
# FY2022 Annual Report's restated comparative, which reclassifies ~£28.5m
# between the two interest-income lines below with no effect on Net
# interest income or any other total).
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income calculated using the effective interest rate method", d([1284.6, 1199.3, 946.0, 588.1, 456.3])),
    ("DATA", "Other interest and similar income", d([137.3, 187.7, 197.8, 36.2, -12.6])),
    ("DATA", "Interest expense and similar charges", d([-774.9, -795.9, -567.1, -164.4, -88.9])),
    ("TOTAL", "Net interest income", d([647.0, 591.1, 576.7, 459.9, 354.8])),
    ("DATA", "Operating lease rental income", d([7.3, 8.7, 9.6, 10.1, 10.4])),
    ("DATA", "Depreciation on operating leases", d([-6.2, -7.4, -8.2, -8.7, -8.6])),
    ("DATA", "Net other operating lease income/(expense)", d([0.1, 0.1, 0.1, 0.3, None])),
    ("TOTAL", "Net operating lease income", d([1.2, 1.4, 1.5, 1.7, 1.8])),
    ("DATA", "Fee and commission income", d([17.3, 16.2, 16.9, 14.1, 11.5])),
    ("DATA", "Fee and commission expense", d([-19.6, -17.0, -13.3, -8.8, -7.3])),
    ("TOTAL", "Net fee and commission income/(expense)", d([-2.3, -0.8, 3.6, 5.3, 4.2])),
    ("DATA", "Net gains on derecognition of financial assets measured at amortised cost", d([None, None, None, 7.7, 21.7])),
    ("DATA", "Net gains on structured asset sales", d([34.8, 14.1, None, None, None])),
    ("DATA", "Net (losses)/gains on derivative financial instruments and hedge accounting", d([-2.2, 1.9, 5.1, -0.8, 3.1])),
    ("DATA", "Net gains on loans and advances measured at FVTPL", d([0.3, None, None, None, None])),
    ("DATA", "Net other operating income/(expense)", d([2.5, 1.4, -0.9, 2.4, 0.4])),
    ("TOTAL", "Net operating income", d([681.3, 609.1, 586.0, 476.2, 386.0])),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Administrative expenses", d([-325.9, -252.2, -225.6, -189.3, -164.2])),
    ("DATA", "Impairment losses on financial assets", d([-83.0, -67.2, -60.1, -47.7, -31.4])),
    ("DATA", "Provisions", d([-0.8, 5.3, -13.1, -0.8, 7.0])),
    ("TOTAL", "Total operating expenses", d([-409.7, -314.1, -298.8, -237.8, -188.6])),
    ("TOTAL", "Profit before tax", d([271.6, 295.0, 287.2, 238.4, 197.4])),
    ("DATA", "Tax", d([-76.7, -75.2, -74.6, -58.7, -47.9])),
    ("TOTAL", "Profit after tax, attributable to owners", d([194.9, 219.8, 212.6, 179.7, 149.5])),
    ("SECTION", "Other comprehensive income, net of tax (items that may be reclassified subsequently to the statement of profit and loss)", {}),
    ("DATA", "Cash flow hedging reserve - net (losses)/gains from effective portion of changes in fair value", d([-4.4, 17.6, -23.1, 38.4, None])),
    ("DATA", "Cash flow hedging reserve - reclassifications to statement of profit and loss", d([-6.6, -6.2, -6.8, -2.2, None])),
    ("DATA", "Cash flow hedging reserve - related tax", d([3.0, -3.2, 8.0, -9.8, None])),
    ("TOTAL", "Movement in cash flow hedging reserve", d([-8.0, 8.2, -21.9, 26.4, None])),
    ("DATA", "FVOCI reserve - net gains/(losses) from changes in fair value", d([18.3, 35.6, 9.9, -17.1, None])),
    ("DATA", "FVOCI reserve - change in loss allowance", d([1.4, 5.3, 4.3, 2.4, None])),
    ("DATA", "FVOCI reserve - related tax", d([-5.5, -11.0, -3.8, 4.0, None])),
    ("TOTAL", "Movement in fair value through other comprehensive income reserve", d([14.2, 29.9, 10.4, -10.7, None])),
    ("TOTAL", "Other comprehensive income/(expense), net of tax", d([6.2, 38.1, -11.5, 15.7, None])),
    ("TOTAL", "Total comprehensive income, attributable to owners", d([201.1, 257.9, 201.1, 195.4, 149.5])),
]

b.add_income_statement_sheet(
    title="Shawbrook Bank Limited — Profit & Loss",
    subtitle="Group/Consolidated basis, £m; FY2021-FY2025 calendar year-ends. Necessarily Group basis - the "
              "Company takes the s.408 Companies Act 2006 exemption and does not publish its own income "
              "statement (see source note for the Company's own disclosed after-tax profit each year, which "
              "differs from Group 'Profit after tax' shown here). FY2021 has no disclosed OCI items at all - "
              "'Profit after tax' equals 'Total comprehensive income' exactly, per that year's own Annual Report.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=86,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - Company basis, chronological. Equity
# reconciliation ladder: built year-by-year, each closing balance ties
# exactly to that year's own Balance Sheet Total equity above and to the
# next year's opening balance - zero undocumented plug rows across all 5
# years, including easy-to-skip categories (cash flow hedging reserve,
# FVOCI reserve, capital securities issue/settlement, capital
# contributions, share-based payments, a FY2025 ordinary share issue).
# ---------------------------------------------------------------
EQUITY_HEADERS = [
    "Share capital", "Share premium account", "Capital securities", "Merger reserve",
    "Capital contribution reserve", "Cash flow hedging reserve", "FVOCI reserve",
    "Retained earnings", "Total equity",
]

equity_rows = [
    ("TOTAL", "Balance at 1 January 2021", (175.5, 81.0, 125.0, 1.6, 17.7, None, None, 392.1, 792.9)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 153.5, 153.5)),
    ("DATA", "Equity-settled share-based payments", (None, None, None, None, 0.6, None, None, None, 0.6)),
    ("DATA", "Coupon paid on capital securities", (None, None, None, None, None, None, None, -9.8, -9.8)),
    ("DATA", "Capital contribution", (None, None, None, None, 5.6, None, None, None, 5.6)),
    ("TOTAL", "Balance at 31 December 2021 / 1 January 2022", (175.5, 81.0, 125.0, 1.6, 23.9, None, None, 535.8, 942.8)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 213.0, 213.0)),
    ("DATA", "Movement in fair value through other comprehensive income reserve", (None, None, None, None, None, None, -10.7, None, -10.7)),
    ("DATA", "Equity-settled share-based payments", (None, None, None, None, 0.1, None, None, None, 0.1)),
    ("DATA", "Issue of capital securities", (None, None, 124.0, None, None, None, None, None, 124.0)),
    ("DATA", "Settlement of capital securities", (None, None, -124.0, None, None, None, None, None, -124.0)),
    ("DATA", "Coupon paid on capital securities", (None, None, None, None, None, None, None, -8.8, -8.8)),
    ("TOTAL", "Balance at 31 December 2022 / 1 January 2023", (175.5, 81.0, 125.0, 1.6, 24.0, None, -10.7, 740.0, 1136.4)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 246.4, 246.4)),
    ("DATA", "Movement in cash flow hedging reserve", (None, None, None, None, None, 0.1, None, None, 0.1)),
    ("DATA", "Movement in fair value through other comprehensive income reserve", (None, None, None, None, None, None, 10.4, None, 10.4)),
    ("DATA", "Equity-settled share-based payments", (None, None, None, None, 0.7, None, None, None, 0.7)),
    ("DATA", "Coupon paid on capital securities", (None, None, None, None, None, None, None, -16.9, -16.9)),
    ("DATA", "Capital contribution", (None, None, None, None, 14.3, None, None, None, 14.3)),
    ("TOTAL", "Balance at 31 December 2023 / 1 January 2024", (175.5, 81.0, 125.0, 1.6, 39.0, 0.1, -0.3, 969.5, 1391.4)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 203.2, 203.2)),
    ("DATA", "Movement in fair value through other comprehensive income reserve", (None, None, None, None, None, None, 29.9, None, 29.9)),
    ("DATA", "Equity-settled share-based payments", (None, None, None, None, 0.7, None, None, None, 0.7)),
    ("DATA", "Coupon paid on capital securities", (None, None, None, None, None, None, None, -15.1, -15.1)),
    ("TOTAL", "Balance at 31 December 2024 / 1 January 2025", (175.5, 81.0, 125.0, 1.6, 39.7, 0.1, 29.6, 1157.6, 1610.1)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 189.2, 189.2)),
    ("DATA", "Movement in cash flow hedging reserve", (None, None, None, None, None, 1.2, None, None, 1.2)),
    ("DATA", "Movement in fair value through other comprehensive income reserve", (None, None, None, None, None, None, 14.2, None, 14.2)),
    ("DATA", "Issue of ordinary shares", (50.0, None, None, None, None, None, None, None, 50.0)),
    ("DATA", "Equity-settled share-based payments", (None, None, None, None, None, None, None, 26.1, 26.1)),
    ("DATA", "Coupon paid on capital securities", (None, None, None, None, None, None, None, -15.1, -15.1)),
    ("TOTAL", "Balance at 31 December 2025", (225.5, 81.0, 125.0, 1.6, 39.7, 1.3, 43.8, 1357.8, 1875.7)),
]

b.add_equity_changes_sheet(
    title="Shawbrook Bank Limited — Statement of Changes in Equity",
    subtitle="Company/entity basis, £m, chronological (oldest to newest). Each year's closing Total equity ties "
              "exactly to that year's own Balance Sheet Total equity and to the next year's opening balance - "
              "zero undocumented plug rows across all 5 years. 'Profit for the year' rows use the Company's own "
              "disclosed profit figure (see the Profit & Loss sheet's source note for why this differs from "
              "Group 'Profit after tax').",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=50,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
r=[("SECTION","Cash flows from operating activities",{}),
("DATA","Profit before tax",d([252.7,271.6,333.8,284.6,203.8])),
("DATA","Adjustments for non-cash items and other adjustments",d([182.2,52.4,63.2,67.4,2.6])),
("DATA","(Increase)/decrease in operating assets",d([-2597.8,-1906.0,-2632.5,-2234.4,-1526.5])),
("DATA","Increase in operating liabilities",d([2590.0,2209.7,2775.8,2627.5,1449.6])),
("DATA","Tax (paid)/recovered",d([-56.5,-85.1,-88.5,-61.9,-48.4])),
("TOTAL","Net cash generated from operating activities",d([370.6,542.6,451.8,683.2,81.1])),
("SECTION","Cash flows from investing activities",{}),
("DATA","Purchase of investment securities",d([-1254.0,-691.3,-308.4,-204.8,-231.9])),
("DATA","Disposals and maturities of investment securities",d([441.1,60.7,194.8,92.9,37.7])),
("DATA","Purchase of property, plant and equipment",d([-0.3,-2.3,-0.7,-0.4,-0.7])),
("DATA","Purchase and development of intangible assets",d([-17.2,-13.3,-13.4,-9.1,-7.1])),
("DATA","Investment in right-of-use asset",d([0,-6.9,0,0,0])),
("DATA","Purchase of subsidiary",d([-64.8,-22.0,-44.7,0,-5.5])),
("TOTAL","Net cash (used by)/generated from investing activities",d([-895.2,-675.1,-172.4,-121.4,-207.5])),
("SECTION","Cash flows from financing activities",{}),
("DATA","Increase/(decrease) in amounts due to banks",d([58.5,-25.5,-101.1,298.0,385.2])),
("DATA","Issue of debt securities",d([0,0,0,0,0])),
("DATA","Repurchase and redemption of debt securities",d([0,0,0,0,0])),
("DATA","Costs arising on issue of debt securities",d([0,0,0,0,0])),
("DATA","Payment of principal portion of lease liabilities",d([-0.6,-1.5,-1.9,-2.1,-1.8])),
("DATA","Issue of subordinated debt",d([75.0,0,90.0,0,0])),
("DATA","Redemption of subordinated debt",d([-76.5,-20.0,0,0,0])),
("DATA","Costs arising on issue of subordinated debt",d([-0.9,0,-1.0,0,0])),
("DATA","Net proceeds from issue of share capital",d([50.0,0,0,0,0])),
("DATA","Decrease/(increase) in deemed loan due from structured entities",d([78.2,83.1,-120.7,0,0])),
("DATA","(Decrease)/increase in deemed loan due to structured entities",d([-12.8,119.3,136.2,-269.8,134.6])),
("DATA","Increase in deemed loan due from structured entities",d([0,0,0,-93.4,0])),
("DATA","Capital contribution",d([0,0,14.3,0,0])),
("DATA","Coupon paid to holders of capital securities",d([-15.1,-15.1,-16.9,-8.8,-9.8])),
("TOTAL","Net cash (used by)/generated from financing activities",d([155.8,140.3,-1.1,-76.1,508.2])),
("TOTAL","Net (decrease)/increase in cash and cash equivalents",d([-368.8,7.8,278.3,485.7,381.8])),
("DATA","Cash and cash equivalents as at 1 January",d([2493.5,2485.7,2207.4,1721.7,1339.9])),
("TOTAL","Cash and cash equivalents as at 31 December",d([2124.7,2493.5,2485.7,2207.4,1721.7]))]
b.add_cash_flow_sheet(title="Shawbrook Bank Limited — Company Cash Flow Statement",subtitle="Company/entity basis, £m; FY2021-FY2025 calendar year-ends.",rows=r,sources_text=cf,first_col_width=70,source_height=230,unit_suffix=" (£m)")

# ---------------------------------------------------------------
# Asset Quality - loans and advances to customers AT AMORTISED COST ONLY
# (a narrower, but the only comparable, basis across all 5 years - a wider
# "Total loans and advances to customers" table including FVOCI-measured
# loans only appears in the FY2023-FY2025 Annual Reports; using the
# amortised-cost table throughout keeps years on a consistent footing).
# Each year's own Annual Report figures used (not later restated
# comparatives). Note this narrower total does NOT tie to the Balance
# Sheet's "Loans and advances to customers" line (which is Total loans
# across all measurement categories including FVOCI) - a genuine,
# documented cross-statement scope difference, not forced to tie.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers at amortised cost, by IFRS 9 stage (£m)", {}),
    ("DATA", "Gross loans - Stage 1", d([12235.5, 10276.9, 9281.0, 8279.5, 7315.7])),
    ("DATA", "Gross loans - Stage 2", d([1064.7, 1023.3, 997.5, 897.3, 831.2])),
    ("DATA", "Gross loans - Stage 3", d([474.7, 506.8, 352.1, 287.9, 221.6])),
    ("DATA", "Gross loans - POCI (purchased or originated credit-impaired)", d([40.3, None, None, None, None])),
    ("TOTAL", "Gross carrying amount", d([13815.2, 11807.0, 10630.6, 9464.7, 8368.5])),
    ("DATA", "Loss allowance - Stage 1", d([-59.8, -48.0, -47.3, -43.2, -25.8])),
    ("DATA", "Loss allowance - Stage 2", d([-31.5, -33.4, -29.0, -22.6, -15.2])),
    ("DATA", "Loss allowance - Stage 3", d([-93.3, -78.0, -53.9, -46.0, -35.0])),
    ("DATA", "Loss allowance - POCI", d([-4.8, None, None, None, None])),
    ("TOTAL", "Loss allowance", d([-189.4, -159.4, -130.2, -111.8, -76.0])),
    ("TOTAL", "Net carrying amount", d([13625.8, 11647.6, 10500.4, 9352.9, 8292.5])),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross loans)", d(["3.44%", "4.29%", "3.31%", "3.04%", "2.65%"])),
    ("DATA", "Stage 3 coverage ratio (Stage 3 loss allowance / Stage 3 gross)", d(["19.65%", "15.39%", "15.31%", "15.98%", "15.79%"])),
]

b.add_asset_quality_sheet(
    title="Shawbrook Bank Limited — Asset Quality",
    subtitle="Group basis, £m. Loans and advances to customers at amortised cost only (the one basis disclosed "
              "consistently across all 5 years) - see source note for why this doesn't tie exactly to the "
              "Balance Sheet's broader 'Loans and advances to customers' line. FY2021-FY2024 include POCI loans "
              "within the Stage 3 total (each year's own report's footnote gives the POCI split; FY2025 is the "
              "first year POCI is broken out as its own row).",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Shawbrook Bank Limited, 'loans and advances to customers at amortised cost' stage analysis:\n"
        f"FY2025: Annual Report and Accounts 2025, p.54 - {AR['FY2025']}\n"
        f"FY2024: Annual Report and Accounts 2024, p.52 - {AR['FY2024']}\n"
        f"FY2023: Annual Report and Accounts 2023, p.52 (independently cross-checked against the FY2023 "
        f"comparative column in Annual Report and Accounts 2024, p.52, which agrees exactly) - {AR['FY2023']}\n"
        f"FY2022: Annual Report and Accounts 2022, p.49 (independently cross-checked against the FY2022 "
        f"restated comparative in Annual Report and Accounts 2023, p.52, which agrees on Total figures) - "
        f"{AR['FY2022']}\n"
        f"FY2021: Annual Report and Accounts 2021, p.56-57 (independently cross-checked against the FY2021 "
        f"comparative column in Annual Report and Accounts 2022, p.48, which agrees exactly) - {AR['FY2021']}\n\n"
        + note
    ),
    first_col_width=64,
    source_height=240,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
ps="Sources - Bank-specific Pillar 3: FY2021 Appendix 4 pp.54-58; FY2022 Bank tables 17 and KM1 pp.18-21; FY2023 Bank tables 14-15 pp.19-22; FY2024 Bank tables 11-12 pp.16-19.\n"+"\n".join(f"{y}: {P3[y]}" for y in Y)+"\nBlank cells mean not publicly disclosed/not applicable; FY2025 Group-only data is not used as a Bank proxy."
def m(name,unit,data,n=None): b.add_metric_sheet(name,unit,[(name,data)],ps,note=n,first_col_width=54,source_height=180)
m("CET1 Capital","£m",d([None,1297.0,1122.7,951.5,775.7]))
m("CET1 Ratio","%",d([None,"13.0%","12.9%","12.7%","12.6%"]))
m("Tier 1 Capital","£m",d([None,1422.0,1247.7,1076.5,900.7]))
m("Tier 1 Ratio","%",d([None,"14.3%","14.3%","14.6%","14.7%"]))
m("Total Capital","£m",d([None,1586.2,1431.7,1171.5,995.7]))
m("Total Capital Ratio","%",d([None,"15.9%","16.4%","15.9%","16.2%"]))
m("Total RWAs","£m",d([None,9952.2,8707.3,7466.4,6134.0]))

# ---------------------------------------------------------------
# RWA Breakdown - Pillar 3 UK OV1 (FY2022-FY2024)/EU OV1 (FY2021) template,
# Bank-specific (consistent with the existing Bank-specific Pillar 3
# metrics above). FY2022 uses the restated figures published in the FY2023
# Pillar 3 disclosure (see note - RWAs increased £80.6m from £7,385.8m to
# £7,466.4m on a CVA/CCR adjustment for structured-entity interest rate
# swaps). FY2025 is blank - the only available FY2025 Pillar 3 publication
# is Group-only (post-listing) and is not substituted for Bank data, per
# the existing convention on this workbook's other Pillar 3 sheets. All 4
# populated years sum exactly to Total RWAs above.
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (Pillar 3 UK OV1 template FY2022-FY2024; EU OV1 template FY2021)", {}),
    ("DATA", "Credit risk (excluding CCR)", d([None, 8925.4, 7942.9, 6768.0, 5582.3])),
    ("DATA", "Counterparty credit risk (CCR) - credit valuation adjustment", d([None, 4.2, 2.7, 65.1, 1.0])),
    ("DATA", "Securitisation exposures in the non-trading book (after the cap)", d([None, 117.3, 46.2, 31.8, 20.9])),
    ("DATA", "Operational risk", d([None, 905.3, 715.5, 601.5, 529.8])),
    ("TOTAL", "Total RWAs", d([None, 9952.2, 8707.3, 7466.4, 6134.0])),
]

b.add_rwa_breakdown_sheet(
    title="Shawbrook Bank Limited — RWA Breakdown",
    subtitle="Bank-specific basis, £m. FY2025 blank - the only available FY2025 Pillar 3 publication is "
              "Group-only (post-listing) and is not substituted for Bank data. FY2022 uses the restated figures "
              "published in the FY2023 Pillar 3 disclosure (RWAs increased £80.6m on a CVA/CCR adjustment - see "
              "source note). The 4 populated years sum exactly to Total RWAs.",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Sources - Shawbrook Bank Limited, UK OV1 / EU OV1: Overview of risk-weighted exposure amounts:\n"
        f"FY2024: Pillar 3 Disclosures 2024, Table 11 (UK OV1), p.16 - {P3['FY2024']}\n"
        f"FY2023: Pillar 3 Disclosures 2023, Table 14 (UK OV1), p.19 - {P3['FY2023']}\n"
        f"FY2022 (restated): Pillar 3 Disclosures 2023, Table 14 (UK OV1, FY2022 restated comparative column), "
        f"p.19 - RWAs restated from £7,385.8m to £7,466.4m to reflect a CVA/CCR adjustment on the Bank's "
        f"structured entities' interest rate swap derivatives (footnote 1) - {P3['FY2023']}\n"
        f"FY2021: Pillar 3 Disclosures 2021, Appendix 4 ('Overview of risk-weighted assets (EU OV1) and minimum "
        f"capital requirements under Pillar 1 for Shawbrook Bank Limited'), p.57 - independently cross-checked "
        f"against Pillar 3 Disclosures 2022, Table 14's FY2021 comparative column, which agrees exactly - "
        f"{P3['FY2021']}\n"
        f"FY2025: not applicable - see subtitle - {P3['FY2025']}\n\n" + note
    ),
    first_col_width=64,
    source_height=220,
    unit_suffix=" (£m)",
)

m("Leverage Ratio","%",d([None,"8.1%","8.2%","8.8%","8.0%"]),"FY2022 uses the UK leverage framework effective 1 January 2022; FY2021 uses the prior basis and comparatives were not restated.")
m("LCR","%",d([None,"265.0%","310.9%","290.3%",None]),"Bank-specific FY2021 LCR was not provided; Group data was not substituted.")
m("NSFR","%",d([None,"134.5%","145.8%",None,None]),"NSFR was not applicable in the FY2022 disclosure and FY2025 Bank data is unavailable.")
m("MREL Ratio","%",d([None,None,None,None,None]),"No Bank-specific quantitative MREL ratio was disclosed.")

b.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", d([22535.7, 19629.0, 17100.9, 13945.7, 11094.6])),
        ("Loans and advances to customers", d([17801.1, 15129.4, 13157.9, 10472.8, 8278.9])),
        ("Customer deposits", d([18353.5, 15804.0, 13562.7, 10914.5, 8358.6])),
        ("Total equity", d([1875.7, 1610.1, 1391.4, 1136.4, 942.8])),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Net operating income", d([681.3, 609.1, 586.0, 476.2, 386.0])),
        ("Total operating expenses", d([-409.7, -314.1, -298.8, -237.8, -188.6])),
        ("Profit after tax, attributable to owners", d([194.9, 219.8, 212.6, 179.7, 149.5])),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", d([1610.1, 1391.4, 1136.4, 942.8, 792.9])),
        ("Profit for the year", d([189.2, 203.2, 246.4, 213.0, 153.5])),
        ("Other equity movements, net", d([76.4, 15.5, 8.6, -19.4, -3.6])),
        ("Closing equity", d([1875.7, 1610.1, 1391.4, 1136.4, 942.8])),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[("Net cash generated from operating activities",d([370.6,542.6,451.8,683.2,81.1])),("Net cash (used by)/generated from investing activities",d([-895.2,-675.1,-172.4,-121.4,-207.5])),("Net cash (used by)/generated from financing activities",d([155.8,140.3,-1.1,-76.1,508.2])),("Cash and cash equivalents as at 31 December",d([2124.7,2493.5,2485.7,2207.4,1721.7]))],
    cash_flow_unit="£m",
    ratios=[("CET1 Ratio",d([None,"13.0%","12.9%","12.7%","12.6%"])),("Tier 1 Ratio",d([None,"14.3%","14.3%","14.6%","14.7%"])),("Total Capital Ratio",d([None,"15.9%","16.4%","15.9%","16.2%"])),("Leverage Ratio",d([None,"8.1%","8.2%","8.8%","8.0%"])),("LCR",d([None,"265.0%","310.9%","290.3%",None])),("NSFR",d([None,"134.5%","145.8%",None,None]))],
    note="Balance Sheet/Statement of Changes in Equity use the Company column; Profit & Loss is necessarily "
         "Group basis (Company takes the s.408 exemption) - see the Profit & Loss sheet's source note. "
         "Company-only cash flows and Bank-specific regulatory metrics; FY2025 Bank regulatory metrics are "
         "blank because the available Pillar 3 document is Group-only.",
)
b.save("/Users/armaan/code/katalysis/banks/SHAWBROOK FINANCIALS.xlsx")
