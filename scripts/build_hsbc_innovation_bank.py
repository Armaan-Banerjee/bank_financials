import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]  # most recent first
YEAR_LABEL = {
    "FY2025": "FY2025",
    "FY2024": "FY2024",
    "FY2023": "FY2023",
    "FY2022": "FY2022",
    "FY2021": "FY2021*",
    "FY2020": "FY2020*",
}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/12546585/filing-history"
AR2024_URL = AR2025_URL
AR2023_URL = AR2025_URL
AR2022_URL = AR2025_URL
AR2021_URL = AR2025_URL
AR2025_DOC_URL = "https://find-and-update.company-information.service.gov.uk/company/12546585/filing-history/MzUyNjUwMTE0MmFkaXF6a2N4/document?format=pdf&download=0"
AR2024_DOC_URL = "https://find-and-update.company-information.service.gov.uk/company/12546585/filing-history/MzQ4MDA1NzM0MWFkaXF6a2N4/document?format=pdf&download=0"
AR2023_DOC_URL = "https://find-and-update.company-information.service.gov.uk/company/12546585/filing-history/MzQyMTMzNzQ4OGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_DOC_URL = "https://find-and-update.company-information.service.gov.uk/company/12546585/filing-history/MzM5NzEzNzM5MWFkaXF6a2N4/document?format=pdf&download=0"
P3_2022_URL = "https://www.hsbcinnovationbanking.com/-/media/hinv/pdf/regulations/pillar-3-report-2022.pdf"

ENTITY_NOTE = (
    "\nENTITY HISTORY: HSBC Innovation Bank Limited (company 12546585) was incorporated on 3 April 2020 as "
    "SVBUK Limited, a dormant shell company seeking UK bank authorisation. Its very first accounting period "
    "was shortened by an AA01 filing from a 30 April 2021 year-end to 31 December 2020 (filed 28 Oct 2020), "
    "and its FY2020 accounts (filed 26 Jul 2021, 2 pages, Companies House document "
    "MzMwODc2NzM1M2FkaXF6a2N4) were filed as 'Dormant Accounts' under the section 480 Companies Act 2006 "
    "dormant-company exemption: the entire balance sheet is GBP1 cash at bank held against 1 Ordinary Share "
    "of GBP1, with no P&L, no cash flow statement, and no banking activity of any kind - confirmed by reading "
    "the filed document itself, not inferred from the filing description alone. FY2020 is therefore left "
    "blank throughout this workbook, the same treatment already applied to FY2021 below and for the same "
    "reason (a pre-authorisation shell with nothing bankable to show), just one year further back and even "
    "more literally dormant (GBP1 nominal capital vs FY2021's genuine, if small, GBP477k operating loss). It "
    "had no banking operations in FY2021 (loss of GBP477k, funded by a loan from Silicon Valley Bank's UK "
    "Branch purely to pay non-executive director fees) and, being a small company under FRS 101's Reduced "
    "Disclosure Framework that year, published no cash flow statement or Pillar 3 disclosure at all - FY2021 "
    "is left blank here rather than guessed. The actual banking business (Silicon Valley Bank UK Branch) was "
    "transferred into "
    "this entity via a court-based Part VII transfer on 31 July 2022, at which point it began operating and "
    "reporting as a real bank (renamed Silicon Valley Bank UK Limited in July 2022). On 10-13 March 2023, "
    "the entity's former US parent (SVB Financial Group) collapsed after a bank run, triggering a severe "
    "liquidity stress event at this UK entity despite its balance sheet being legally standalone from SVB "
    "US; the Bank of England used its Special Resolution Regime powers on 13 March 2023 to sell the entity "
    "to HSBC UK Bank plc for GBP1 and separately cancelled GBP322m of AT1 debt previously issued to SVB US. "
    "The entity was renamed HSBC Innovation Bank Limited in June 2023 and has since been integrated into the "
    "HSBC UK Domestic Liquidity Sub-group (DoLSub)."
)

CASH_FLOW_SOURCES = (
    "Sources - HSBC Innovation Bank Limited's own Statement of Cash Flows, from each year's own Companies "
    "House-filed Annual Report and Accounts (find-and-update.company-information.service.gov.uk, company "
    "12546585):\n"
    "FY2025: Annual Report and Accounts 2025, p.26 (Statement of Cash Flows), filed 23 Jun 2026.\n"
    "FY2024: Annual Report and Accounts 2024, p.26 (Statement of Cash Flows), filed 08 Sep 2025 - matches "
    "FY2025 AR's FY2024 comparative exactly, no restatement.\n"
    "FY2023: Annual Report and Accounts 2023, p.37 (Statement of Cash Flows), filed 16 May 2024 - matches "
    "FY2024 AR's FY2023 comparative exactly, no restatement.\n"
    "FY2022: Annual Report and Accounts 2022 (filed as 'HSBC Innovation Bank Limited', formerly Silicon "
    "Valley Bank UK Limited), p.41 (Statement of Cash Flows), filed 19 Oct 2023 - matches FY2023 AR's FY2022 "
    "comparative exactly, no restatement. Includes GBP3,946,893k 'Cash transferred on business acquisition' "
    "reflecting the 31 Jul 2022 Part VII transfer of Silicon Valley Bank UK Branch's business into this "
    "entity.\n"
    "FY2021: not applicable - see entity-history note below. SVBUK Limited's own FY2021 accounts ('Accounts "
    "for a small company', filed 7 Sep 2022) applied FRS 101's Reduced Disclosure Framework and published no "
    "cash flow statement; the entity was a pre-authorisation dormant/near-dormant shell that year with no "
    "banking operations.\n"
    "FY2020: not applicable - see entity-history note below. SVBUK Limited's own FY2020 accounts (filed as "
    "'Dormant Accounts' under s480 CA2006, 26 Jul 2021) show a GBP1 balance sheet only, no P&L, and no cash "
    "flow statement at all - a genuinely dormant shell for its entire first (shortened) accounting period.\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - HSBC Innovation Bank Limited Pillar 3 / capital disclosure basis:\n"
        "FY2020-FY2021: not applicable - the entity was a dormant/pre-authorisation shell with no regulated "
        "banking operations and so no Pillar 3 disclosure obligation in either year (see entity-history "
        "note).\n"
        f"FY2022: standalone Pillar 3 Report 2022, p.4-5 (Key Metrics; Capital & Risk Weighted-Assets), "
        f"{P3_2022_URL} - the only year this entity has published a standalone Pillar 3 report (confirmed "
        "via the bank's own regulatory-disclosures page and a Wayback Machine CDX search finding no other "
        "year archived).\n"
        "FY2023-FY2025: no standalone Pillar 3 report has been published for this entity in any of these "
        "years (site enumeration + Wayback CDX search both confirm this - a genuine non-disclosure, not an "
        "access blocker). Figures instead sourced from each year's own Annual Report and Accounts, 'Report "
        "of the Directors: Capital resources' and 'Capital and leverage ratios' tables (audited/unaudited "
        "respectively) - FY2025 AR p.10, FY2024 AR p.10, FY2023 AR p.17-18 - each year's own "
        "originally-published figures used, not later restated comparatives (see note below on the FY2023 "
        "RWA restatement). LCR and NSFR are not shown in these tables for FY2023-FY2025: since the March "
        "2023 HSBC acquisition, the entity's liquidity is managed and disclosed only at the wider HSBC UK "
        "Domestic Liquidity Sub-group (DoLSub) level via HSBC UK's own ILAAP, not published at this solo "
        "entity level (same pattern as RBS plc/Coutts & Company and Bank of Scotland plc elsewhere in this "
        "project). MREL is likewise not disclosed at this subsidiary level in any year.\n"
        "RESTATEMENT NOTE: FY2023's own Annual Report reported RWA of GBP8,430,014k and CET1/Tier1/Total "
        "Capital ratios of 16.1%/16.1%/16.9% and a 13.2% leverage ratio. The FY2024 Annual Report's own "
        "footnote states December 2023 RWA was later restated down by GBP539m to GBP7,890,931m 'following an "
        "internal review of the capital held against undrawn loan commitments', which also raised the "
        "restated CET1/Tier1 ratios to 17.2%, Total Capital ratio to 18.1%, and leverage ratio to 13.9%. "
        "Per this project's convention, FY2023's own originally-published figures are used here throughout; "
        "the restatement is noted for reference only.\n"
        + extra
    )


bw = BankWorkbook(bank_name="HSBC Innovation Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="B42892")

STATEMENTS_SOURCES = (
    "Sources - HSBC Innovation Bank Limited's own Balance Sheet / Income Statement / Statement of "
    "Changes in Equity, from each year's own Companies House-filed Annual Report and Accounts "
    "(find-and-update.company-information.service.gov.uk, company 12546585):\n"
    f"FY2025: Annual Report and Accounts 2025, pp.24-27, filed 23 Jun 2026 - {AR2025_DOC_URL}\n"
    f"FY2024: Annual Report and Accounts 2024, pp.24-27 (as originally published; ties exactly to FY2025 "
    f"AR's FY2024 comparative), filed 08 Sep 2025 - {AR2024_DOC_URL}\n"
    f"FY2023: Annual Report and Accounts 2023, pp.35-38, filed 16 May 2024 - {AR2023_DOC_URL}\n"
    f"FY2022: Annual Report and Accounts 2022 (filed as 'HSBC Innovation Bank Limited', formerly Silicon "
    f"Valley Bank UK Limited), pp.39-42 (as originally published; ties exactly to FY2023 AR's FY2022 "
    f"comparative), filed 19 Oct 2023 - {AR2022_DOC_URL}\n"
    "FY2021: not applicable - see entity-history note below.\n"
    "FY2020: not applicable - see entity-history note below (dormant shell, GBP1 balance sheet only, no "
    "P&L or Statement of Changes in Equity movements).\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTE: the Balance Sheet's own line-item structure genuinely changed over this "
    "period, reflecting HSBC's integration of the entity's treasury function. FY2022-FY2023 show separate "
    "'Cash and balances at central banks' and 'Financial investments' lines (both nil by FY2023's own "
    "year-end, following the March 2023 liquidity event's forced asset disposals - see the Income "
    "Statement's GBP205,005k 'Net loss arising from derecognition of financial assets' for FY2023); from "
    "FY2024 onward neither line appears at all - short-term liquidity appears to route entirely through "
    "'Loans and advances to banks' instead, not a disclosed reclassification, so left as two genuinely "
    "distinct presentations rather than force-merged. Tax assets/liabilities similarly flip between "
    "'Current'/'Deferred' and asset/liability sides year to year exactly as each year's own report shows."
    "\n\nFINANCIAL INVESTMENTS BREAKDOWN NOTE: Annual Report and Accounts 2022, Note 18 'Financial "
    "investments' (p.74) tables 'Financial investments by type' and 'Governments and other public bodies "
    "by country of issuance' - " + AR2022_DOC_URL + " - disclose FY2022's GBP3,458,278k Financial "
    "investments balance (net of ECL) by issuer: Governments and other public bodies GBP3,091.1m (89%, "
    "of which United Kingdom GBP547m/18%, United States GBP2,499m/81%, France GBP45m/1%), Agencies "
    "GBP367.2m (11%), Corporate and other issuers nil (0%). Note 2(e)/(f) (p.47-49) confirms the entity "
    "'does not currently classify any financial assets as measured at fair value through other "
    "comprehensive income' and that financial investments are measured entirely at amortised cost - "
    "there is no FVOCI/FVTPL/available-for-sale leg to split out. The 'UK government and public bodies' "
    "sub-row above uses Note 18's own disclosed GBP547m UK net-exposure figure exactly as reported; the "
    "'other issuers' sub-row is the residual (total less the UK figure) so the two sub-rows reconcile "
    "EXACTLY to the GBP3,458,278k balance sheet total (Note 18's own more granular by-type/by-country "
    "tables only sum to GBP3,458.2m-3,458.3m depending on which sub-table's roundings are combined, a "
    "sub-GBP100k/~0.002% rounding artefact of the source disclosing in whole/one-decimal GBPm rather than "
    "GBP'000 - not reproduced here since the residual construction avoids it entirely). FY2023's balance "
    "is nil (see PRESENTATION NOTE above) so no breakdown applies that year; FY2024 onward the line no "
    "longer exists on the Balance Sheet at all."
)


def statement(kind_rows, sheet_fn, title, subtitle, sheet_name, first_col_width=60, source_height=260):
    sheet_fn(
        title=title,
        subtitle=subtitle,
        rows=kind_rows,
        sources_text=STATEMENTS_SOURCES,
        sheet_name=sheet_name,
        first_col_width=first_col_width,
        source_height=source_height,
        unit_suffix=" (£'000)",
    )


# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2023": 0, "FY2022": 2064343}),
    ("TOTAL", "Financial investments total (amortised cost)", {"FY2023": 0, "FY2022": 3458278}),
    ("DATA", "Financial investments - UK government and public bodies (gilts/treasury), amortised cost", {"FY2022": 547000}),
    ("DATA", "Financial investments - other issuers (overseas government/agencies/corporate), amortised cost", {"FY2022": 2911278}),
    ("DATA", "Derivatives", {"FY2025": 3883, "FY2024": 3426, "FY2023": 2720, "FY2022": 124999}),
    ("DATA", "Loans and advances to banks", {"FY2025": 3553416, "FY2024": 2820579, "FY2023": 2510251, "FY2022": 928181}),
    ("DATA", "Loans and advances to clients", {"FY2025": 6922886, "FY2024": 6615509, "FY2023": 6283807, "FY2022": 5747242}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 109049, "FY2024": 183261, "FY2023": 131863, "FY2022": 166756}),
    ("DATA", "Intangible assets", {"FY2025": 16856, "FY2024": 12570, "FY2023": 0, "FY2022": 11080}),
    ("DATA", "Current tax assets", {"FY2023": 0, "FY2022": 461}),
    ("DATA", "Deferred tax assets", {"FY2025": 2962, "FY2024": 0, "FY2023": 2057}),
    ("TOTAL", "Total assets", {"FY2025": 10609052, "FY2024": 9635345, "FY2023": 8930698, "FY2022": 12501340}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 2567540, "FY2024": 2236913}),
    ("DATA", "Client accounts", {"FY2025": 5937852, "FY2024": 5067197, "FY2023": 4719304, "FY2022": 10446692}),
    ("DATA", "Repurchase agreements - non-trading", {"FY2022": 403736}),
    ("DATA", "Derivatives (liabilities)", {"FY2022": 96415}),
    ("DATA", "Accruals, deferred income and other liabilities", {"FY2025": 129630, "FY2024": 369669, "FY2023": 187473, "FY2022": 140504}),
    ("DATA", "Provisions", {"FY2025": 8929, "FY2024": 18403, "FY2023": 4142, "FY2022": 3680}),
    ("DATA", "Current tax liabilities", {"FY2025": 74210, "FY2024": 107599, "FY2023": 38066}),
    ("DATA", "Deferred tax liabilities", {"FY2024": 250, "FY2022": 2329}),
    ("DATA", "Subordinated liabilities", {"FY2025": 295668, "FY2024": 298472, "FY2023": 74354, "FY2022": 33000}),
    ("TOTAL", "Total liabilities", {"FY2025": 9013829, "FY2024": 8098503, "FY2023": 7574237, "FY2022": 11126356}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 978000, "FY2024": 978000, "FY2023": 978000, "FY2022": 978000}),
    ("DATA", "Other equity instruments", {"FY2025": 229680, "FY2024": 229680, "FY2023": 0, "FY2022": 322000}),
    ("DATA", "Other reserves", {"FY2025": 13278, "FY2024": 13278, "FY2023": 13278, "FY2022": 14456}),
    ("DATA", "Retained earnings", {"FY2025": 374265, "FY2024": 315884, "FY2023": 365183, "FY2022": 60528}),
    ("TOTAL", "Total equity", {"FY2025": 1595223, "FY2024": 1536842, "FY2023": 1356461, "FY2022": 1374984}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 10609052, "FY2024": 9635345, "FY2023": 8930698, "FY2022": 12501340}),
]

statement(
    balance_sheet_rows, bw.add_balance_sheet_sheet,
    title="HSBC Innovation Bank Limited — Statement of Financial Position",
    subtitle="As reported in each year's own Companies House-filed Annual Report and Accounts. FY2020-FY2021 "
              "are blank - the entity was a dormant, pre-authorisation shell in both years with no banking "
              "operations (FY2020: GBP1 dormant-company balance sheet only). Cash/Financial investments "
              "lines disappear from FY2024 onward - see source note.",
    sheet_name="Balance Sheet",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 583393, "FY2024": 621440, "FY2023": 552498, "FY2022": 179842}),
    ("DATA", "Interest expense", {"FY2025": -181021, "FY2024": -216580, "FY2023": -176474, "FY2022": -48629}),
    ("TOTAL", "Net interest income", {"FY2025": 402372, "FY2024": 404860, "FY2023": 376024, "FY2022": 131213}),
    ("DATA", "Fee income", {"FY2025": 51779, "FY2024": 46257, "FY2023": 50014, "FY2022": 27556}),
    ("DATA", "Fee expense", {"FY2025": -496, "FY2024": -852, "FY2023": -1302, "FY2022": -576}),
    ("TOTAL", "Net fee income", {"FY2025": 51283, "FY2024": 45405, "FY2023": 48712, "FY2022": 26980}),
    ("DATA", "Net loss arising from derecognition of financial assets measured at amortised cost", {"FY2023": -205005}),
    ("DATA", "Net income/(expense) from financial instruments held for trading or managed on a fair value basis", {"FY2025": 2491, "FY2024": 477, "FY2023": 2141, "FY2022": -2717}),
    ("DATA", "Other operating income", {"FY2025": 847, "FY2024": 929, "FY2023": 30121}),
    ("TOTAL", "Net operating income before change in expected credit losses and other credit impairment charges", {"FY2025": 456993, "FY2024": 451671, "FY2023": 251993, "FY2022": 155476}),
    ("DATA", "Change in expected credit losses and other credit impairment releases/(charges)", {"FY2025": 772, "FY2024": -39186, "FY2023": -22215, "FY2022": -8207}),
    ("TOTAL", "Net operating income", {"FY2025": 457765, "FY2024": 412485, "FY2023": 229778, "FY2022": 147269}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Employee compensation and benefits", {"FY2025": -141365, "FY2024": -123253, "FY2023": -109914, "FY2022": -36846}),
    ("DATA", "General and administrative expenses", {"FY2025": -27802, "FY2024": -66465, "FY2023": -69063, "FY2022": -20523}),
    ("DATA", "Depreciation and impairment of property, plant and equipment and right-of-use assets", {"FY2025": -2562, "FY2024": -2468, "FY2023": -2564, "FY2022": -1199}),
    ("DATA", "Amortisation and impairment of intangible assets", {"FY2025": -2816, "FY2024": -356, "FY2023": -11404, "FY2022": -629}),
    ("TOTAL", "Total operating expenses", {"FY2025": -174545, "FY2024": -192542, "FY2023": -192945, "FY2022": -59197}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": 283220, "FY2024": 219943, "FY2023": 36833, "FY2022": 88072}),
    ("DATA", "Tax (expense)/credit", {"FY2025": -67795, "FY2024": -71918, "FY2023": -54178, "FY2022": -27067}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 215425, "FY2024": 148025, "FY2023": -17345, "FY2022": 61005}),
]

statement(
    income_statement_rows, bw.add_income_statement_sheet,
    title="HSBC Innovation Bank Limited — Income Statement",
    subtitle="As reported in each year's own Companies House-filed Annual Report and Accounts. FY2020-FY2021 "
              "are blank (dormant shell, no banking operations - FY2020 had no P&L at all, filed as Dormant "
              "Accounts). There is no difference between profit/(loss) after tax and total comprehensive "
              "income/(expense) in any year - no OCI is disclosed.",
    sheet_name="Profit & Loss",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Called up share capital", "Other equity instruments", "Other reserves", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "Balance as at incorporation (3 Apr 2020)", (0, 0, 0, 0, 0)),
    ("DATA", "Movement in the period (GBP1 nominal share capital issued; dormant, s480 CA2006 exemption)", (0, None, None, None, 0)),
    ("TOTAL", "Balance as at 31 Dec 2020 / 1 Jan 2021", (0, 0, 0, 0, 0)),
    ("DATA", "Loss for the year", (None, None, None, -477, -477)),
    ("TOTAL", "Balance as at 31 Dec 2021", (0, 0, 0, -477, -477)),
    ("DATA", "Issue of share capital", (978000, None, None, None, 978000)),
    ("DATA", "Capital securities issued", (None, 322000, None, None, 322000)),
    ("DATA", "Share-based compensation", (None, None, 1178, None, 1178)),
    ("DATA", "Business transfer reserve (US GAAP->IFRS adjustment on Part VII transfer)", (None, None, 13278, None, 13278)),
    ("DATA", "Profit for the year", (None, None, None, 61005, 61005)),
    ("TOTAL", "Balance as at 31 Dec 2022", (978000, 322000, 14456, 60528, 1374984)),
    ("DATA", "Extinguish of capital securities (BoE cancellation of AT1 debt, 13 Mar 2023)", (None, -322000, None, 322000, 0)),
    ("DATA", "Derecognition of share-based compensation", (None, None, -1178, None, -1178)),
    ("DATA", "Loss for the year", (None, None, None, -17345, -17345)),
    ("TOTAL", "Balance as at 31 Dec 2023", (978000, 0, 13278, 365183, 1356461)),
    ("DATA", "Profit for the year", (None, None, None, 148025, 148025)),
    ("DATA", "Capital securities issued during the year", (None, 229680, None, None, 229680)),
    ("DATA", "Other movements (share-based payment arrangements)", (None, None, None, 676, 676)),
    ("DATA", "Dividends paid", (None, None, None, -198000, -198000)),
    ("TOTAL", "Balance as at 31 Dec 2024", (978000, 229680, 13278, 315884, 1536842)),
    ("DATA", "Profit for the year", (None, None, None, 215425, 215425)),
    ("DATA", "Capital securities issued during the year", (None, 0, None, None, 0)),
    ("DATA", "Other movements (share-based payment arrangements)", (None, None, None, -879, -879)),
    ("DATA", "Dividends paid", (None, None, None, -156165, -156165)),
    ("TOTAL", "Balance as at 31 Dec 2025", (978000, 229680, 13278, 374265, 1595223)),
]

bw.add_equity_changes_sheet(
    title="HSBC Innovation Bank Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest. Equity reconciliation ladder confirmed: each "
             "year's own closing balance ties exactly to the next year's own opening balance and to that "
             "year's own Balance Sheet Total equity - zero plug rows needed anywhere in this bank's history.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) for the year", {"FY2025": 215425, "FY2024": 148025, "FY2023": -17345, "FY2022": 61005}),
    ("SECTION", "Adjustments for non-cash items", {}),
    ("DATA", "Depreciation/amortisation on fixed and intangible assets", {"FY2025": 5378, "FY2024": 2824, "FY2023": 2597, "FY2022": 1828}),
    ("DATA", "Unwind of premium on financial assets", {"FY2024": 0, "FY2023": -10915, "FY2022": -14922}),
    ("DATA", "Change in expected credit loss", {"FY2025": -772, "FY2024": 39186, "FY2023": 19897, "FY2022": 7556}),
    ("DATA", "Share-based payment expense/(release)", {"FY2025": 6119, "FY2024": 6858, "FY2023": -1178, "FY2022": 1178}),
    ("DATA", "Net loss arising from derecognition of financial assets", {"FY2024": 0, "FY2023": 205005, "FY2022": 0}),
    ("DATA", "Cancellation of subordinated debt", {"FY2024": 0, "FY2023": -33000, "FY2022": 0}),
    ("DATA", "Intangibles write-off", {"FY2024": 0, "FY2023": 11404, "FY2022": 0}),
    ("DATA", "Other non-cash items included in profit/(loss)", {"FY2025": -12647, "FY2024": 13963, "FY2023": -196, "FY2022": -19365}),
    ("DATA", "Elimination of exchange differences", {"FY2025": 978, "FY2024": 1550, "FY2023": -587, "FY2022": 904}),
    ("TOTAL", "Adjustments for non-cash items (subtotal)", {"FY2025": -944, "FY2024": 64381, "FY2023": 193027, "FY2022": -22821}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Net derivatives held for risk management", {"FY2024": 0, "FY2023": 65794, "FY2022": -655}),
    ("DATA", "Financial assets designated at fair value", {"FY2024": 0, "FY2023": 153, "FY2022": -69}),
    ("DATA", "Loans and advances to clients", {"FY2025": -307653, "FY2024": -343256, "FY2023": -557202, "FY2022": -536659}),
    ("DATA", "Other assets", {"FY2025": 77728, "FY2024": -62554, "FY2023": 20747, "FY2022": -24239}),
    ("DATA", "Deposits by banks", {"FY2025": 330627, "FY2024": -313985, "FY2023": 2550898}),
    ("DATA", "Client accounts", {"FY2025": 870655, "FY2024": 347893, "FY2023": -5727067, "FY2022": -480866}),
    ("DATA", "Repurchase agreements - non-trading", {"FY2024": 0, "FY2023": -403736, "FY2022": 403736}),
    ("DATA", "Other liabilities", {"FY2025": -284216, "FY2024": 251304, "FY2023": 81983, "FY2022": 107687}),
    ("DATA", "Fixed rate deposits with parent", {"FY2025": -55000, "FY2024": -619000, "FY2023": -1281000}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": 846622, "FY2024": -527192, "FY2023": -5073749, "FY2022": -492881}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Cash transferred on business acquisition", {"FY2022": 3946893}),
    ("DATA", "Consideration paid on business acquisition", {"FY2022": -232244}),
    ("DATA", "Sale of financial investments", {"FY2024": 0, "FY2023": 3171249}),
    ("DATA", "Purchase of financial investments", {"FY2024": 0, "FY2023": -15737, "FY2022": -1612481}),
    ("DATA", "Proceeds from maturity of treasury investments", {"FY2024": 0, "FY2023": 80932, "FY2022": 52525}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -1086}),
    ("DATA", "Net investment in intangible assets", {"FY2025": -7103, "FY2024": -12926, "FY2023": -324, "FY2022": -2333}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -8189, "FY2024": -12926, "FY2023": 3236120, "FY2022": 2152360}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Issuance of other equity instruments", {"FY2024": 229680}),
    ("DATA", "Proceeds of issuance of subordinated debt", {"FY2024": 224118, "FY2023": 74354, "FY2022": 33000}),
    ("DATA", "Dividends paid to shareholders of the parent company", {"FY2025": -156165, "FY2024": -198000}),
    ("DATA", "Capital contribution from parent", {"FY2022": 1300000}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": -156165, "FY2024": 255798, "FY2023": 74354, "FY2022": 1333000}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 682268, "FY2024": -284320, "FY2023": -1763275, "FY2022": 2992479}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 943912, "FY2024": 1229251, "FY2023": 2992524, "FY2022": 45}),
    ("DATA", "Effect of exchange rate fluctuations on cash and cash equivalents held", {"FY2025": -4430, "FY2024": -1019, "FY2023": 2, "FY2022": 0}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 1621750, "FY2024": 943912, "FY2023": 1229251, "FY2022": 2992524}),
]

bw.add_cash_flow_sheet(
    title="HSBC Innovation Bank Limited — Statement of Cash Flows",
    subtitle="As reported in each year's own Companies House-filed Annual Report and Accounts. FY2020-FY2021 "
              "are blank - the entity was a dormant, pre-authorisation shell in both years with no banking "
              "operations and no cash flow statement published (FY2021's FRS 101 exemption; FY2020's s480 "
              "dormant-company exemption - see source note).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to clients at amortised cost, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 - gross carrying amount", {"FY2025": 6847800, "FY2024": 6581600, "FY2023": 5567500, "FY2022": 5241600}),
    ("DATA", "Stage 2 - gross carrying amount", {"FY2025": 94200, "FY2024": 44700, "FY2023": 719100, "FY2022": 525100}),
    ("DATA", "Stage 3 - gross carrying amount", {"FY2025": 13700, "FY2024": 54400, "FY2023": 39800, "FY2022": 2700}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 6955700, "FY2024": 6680700, "FY2023": 6326400, "FY2022": 5769400}),
    ("DATA", "Stage 1 - allowance for ECL", {"FY2025": -19000, "FY2024": -19600, "FY2023": -23700, "FY2022": -15800}),
    ("DATA", "Stage 2 - allowance for ECL", {"FY2025": -4800, "FY2024": -1600, "FY2023": -11700, "FY2022": -6300}),
    ("DATA", "Stage 3 - allowance for ECL", {"FY2025": -8900, "FY2024": -43900, "FY2023": -7200, "FY2022": -100}),
    ("TOTAL", "Total allowance for ECL", {"FY2025": -32700, "FY2024": -65100, "FY2023": -42600, "FY2022": -22200}),
    ("DATA", "Stage 1 ECL coverage", {"FY2025": "0.3%", "FY2024": "0.3%", "FY2023": "0.4%", "FY2022": "0.3%"}),
    ("DATA", "Stage 2 ECL coverage", {"FY2025": "5.1%", "FY2024": "3.6%", "FY2023": "1.6%", "FY2022": "1.2%"}),
    ("DATA", "Stage 3 ECL coverage", {"FY2025": "65.0%", "FY2024": "80.7%", "FY2023": "18.1%", "FY2022": "3.7%"}),
    ("DATA", "Total ECL coverage", {"FY2025": "0.5%", "FY2024": "1.0%", "FY2023": "0.7%", "FY2022": "0.4%"}),
]

bw.add_asset_quality_sheet(
    title="HSBC Innovation Bank Limited — Asset Quality",
    subtitle="Loans and advances to clients at amortised cost, by IFRS 9 stage - the Bank's Note 15/18/14 "
              "'Credit risk analysis'/'Summary of credit risk by stage distribution' tables. FY2020-FY2021 "
              "are blank (dormant shell, no lending). FY2022's own segmentation (Investor/Balance Sheet/Cash "
              "Flow Dependent etc.) was replaced by a corporate-and-commercial/non-bank-financial-"
              "institutions split from FY2023 onward following HSBC's post-acquisition risk-management "
              "framework change - both genuinely different bases, shown here only at the combined "
              "Stage 1/2/3 total level which is directly comparable across all 4 years.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nAsset Quality sourced from: FY2025/FY2024 - Annual Report and Accounts 2025, p.41 (Note 15, "
        "'Summary of credit risk by stage distribution and ECL coverage by industry sector'); FY2023 - "
        "Annual Report and Accounts 2023, p.57 (Note 14, same table title); FY2022 - Annual Report and "
        "Accounts 2022, p.72 (Note 18, 'Credit exposures by stage and credit rating for loans and advances "
        "to clients') - each year's own originally-published figures, converted from the source's £m to "
        "£'000 for consistency with the rest of this workbook (introduces immaterial rounding of up to "
        "GBP1k against the Balance Sheet's own net loans figure)."
    ),
    first_col_width=54,
    source_height=230,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=170)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1234805, "FY2024": 1156166, "FY2023": 1353741, "FY2022": 1041683})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "13.5%", "FY2024": "14.0%", "FY2023": "16.1%", "FY2022": "13.9%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 1464485, "FY2024": 1385846, "FY2023": 1353741, "FY2022": 1363683})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 capital ratio", {"FY2025": "16.0%", "FY2024": "16.7%", "FY2023": "16.1%", "FY2022": "18.2%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total regulatory capital", {"FY2025": 1768030, "FY2024": 1684318, "FY2023": 1428095, "FY2022": 1396683})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {"FY2025": "19.3%", "FY2024": "20.3%", "FY2023": "16.9%", "FY2022": "18.6%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets (RWA) - Pillar 1", {"FY2025": 9150116, "FY2024": 8276902, "FY2023": 8430014, "FY2022": 7496138})],
    p3_sources(),
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR) - standardised approach", {"FY2022": 6997168}),
    ("DATA", "Counterparty credit risk (CCR) - standardised approach", {"FY2022": 192328}),
    ("DATA", "Counterparty credit risk - credit valuation adjustment (CVA)", {"FY2022": 37929}),
    ("DATA", "Operational risk - basic indicator approach", {"FY2022": 268713}),
    ("TOTAL", "Total RWAs", {"FY2022": 7496138}),
]

bw.add_rwa_breakdown_sheet(
    title="HSBC Innovation Bank Limited — RWA Breakdown",
    subtitle="FY2022 is the only year this entity has published a standalone Pillar 3 report with a "
              "UK OV1-style RWA-by-category breakdown - confirmed by the bank's own regulatory-disclosures "
              "page and a Wayback Machine CDX search finding no other year archived (see p3_sources note "
              "on the Pillar 3 metric sheets). FY2023-FY2025 are 'Not publicly disclosed' at category "
              "level - only the aggregate Total RWAs figure appears in those years' Annual Reports.",
    rows=rwa_breakdown_rows,
    sources_text=(
        f"Sources - HSBC Innovation Bank Limited Pillar 3 Report 2022, p.6 ('Overview of RWA' table), "
        f"{P3_2022_URL}. FY2023-FY2025: no standalone Pillar 3 report has been published for this entity "
        "in any of these years - only the aggregate Total RWAs figure is disclosed in each year's own "
        "Annual Report 'Capital and leverage ratios' table (see Total RWAs metric sheet). Total ties "
        "exactly to the Total RWAs metric sheet's own FY2022 figure (7,496,138).\n\n"
        "RE-VERIFIED 2026-09-12 (independent fresh check, deeper than the prior claim): (1) pulled a full "
        "listing of every file ever archived under the bank's own "
        "hsbcinnovationbanking.com/-/media/hinv/pdf/regulations/ folder via Wayback CDX (100+ documents "
        "covering terms-and-conditions, summary boxes, policy statements etc.) - 'pillar-3-report-2022.pdf' "
        "is the only Pillar 3 document that has EVER existed at that path; (2) downloaded and fully OCR'd "
        "(scanned/no-text-layer PDFs, all pages, not just a keyword-guessed page range) all 3 of the "
        "FY2023/FY2024/FY2025 Companies House Annual Reports - each contains only a single aggregate "
        "'Risk weighted assets (£'000) - Pillar 1' line (FY2023: 8,430,014; FY2024: 8,276,902, with the "
        "FY2023 comparative separately restated down by £539m per the FY2024 report's own footnote 3; "
        "FY2025: 9,150,116), no category-level split anywhere in any of the three. Confirms this is a "
        "genuine, continuing non-disclosure, not a search miss.\n\n"
        "RE-CONFIRMED 2026-09-15 (third independent check, FY2024 only): downloaded the FY2024 Annual "
        "Report afresh from Companies House (company 12546585, 'Full accounts made up to 31 December "
        "2024', 57pp, scanned go-tiff2pdf with no text layer), rendered all 57 pages at 250 dpi and "
        "OCR'd every one. Exactly ONE page (p.11) mentions risk weighted assets at all, and it carries "
        "only the aggregate 'Risk weighted assets (£'000) - Pillar 1' line - no category split anywhere "
        "in the document. This independently corroborates the 2026-09-12 finding for FY2024. The same "
        "check also CORRECTED a transcription typo in this note: the FY2024 aggregate is 8,276,902 (not "
        "8,276,302 as previously written here); verified by re-rendering p.11 at 450 dpi, since a 9/3 "
        "confusion is a known OCR failure mode. The Total RWAs metric sheet already held the correct "
        "8,276,902, so no data value changed. Note also that p.11 shows the FY2023 comparative as "
        "7,890,931 - the restated figure - against the 8,430,014 as-originally-reported figure carried "
        "on the Total RWAs sheet for FY2023; the £539m restatement is explained in that report's own "
        "footnote 3."
    ),
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2025": "17.6%", "FY2024": "17.9%", "FY2023": "13.2%", "FY2022": "11.7%"})],
    p3_sources(),
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (adjusted value)", {"FY2022": "150%"})],
    p3_sources(
        extra="FY2022's 150% is a 5-month (not 12-month) weighted average, since banking operations only "
              "commenced 1 August 2022, leaving 5 observable month-ends - per the Pillar 3 report's own "
              "footnote, not a like-for-like basis with a full 12-month average."
    ),
    note="Only disclosed for FY2022 (the only year with a standalone Pillar 3 report) - not "
         "applicable FY2020-FY2021 (dormant/pre-authorisation shell, no banking operations) and not "
         "publicly disclosed at this entity level FY2023-FY2025 (see source note).",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (adjusted value)", {"FY2022": "203%"})],
    p3_sources(
        extra="FY2022's 203% is a 2-quarter (not 4-quarter) average, for the same reason as LCR above - per "
              "the Pillar 3 report's own footnote."
    ),
    note="Only disclosed for FY2022 (the only year with a standalone Pillar 3 report) - not "
         "applicable FY2020-FY2021 (dormant/pre-authorisation shell, no banking operations) and not "
         "publicly disclosed at this entity level FY2023-FY2025 (see source note).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "Not publicly disclosed at this entity level in any year - MREL is set at the "
                              "wider HSBC resolution-group level, not for this individual subsidiary."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 10609052, "FY2024": 9635345, "FY2023": 8930698, "FY2022": 12501340}),
        ("Loans and advances to clients", {"FY2025": 6922886, "FY2024": 6615509, "FY2023": 6283807, "FY2022": 5747242}),
        ("Client accounts", {"FY2025": 5937852, "FY2024": 5067197, "FY2023": 4719304, "FY2022": 10446692}),
        ("Total equity", {"FY2025": 1595223, "FY2024": 1536842, "FY2023": 1356461, "FY2022": 1374984}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", {"FY2025": 457765, "FY2024": 412485, "FY2023": 229778, "FY2022": 147269}),
        ("Total operating expenses", {"FY2025": -174545, "FY2024": -192542, "FY2023": -192945, "FY2022": -59197}),
        ("Profit/(loss) for the year", {"FY2025": 215425, "FY2024": 148025, "FY2023": -17345, "FY2022": 61005}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1536842, "FY2024": 1356461, "FY2023": 1374984, "FY2022": -477}),
        ("Profit/(loss) for the year", {"FY2025": 215425, "FY2024": 148025, "FY2023": -17345, "FY2022": 61005}),
        ("Other equity movements, net", {"FY2025": -157044, "FY2024": 32356, "FY2023": -1178, "FY2022": 1314456}),
        ("Closing equity", {"FY2025": 1595223, "FY2024": 1536842, "FY2023": 1356461, "FY2022": 1374984}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 846622, "FY2024": -527192, "FY2023": -5073749, "FY2022": -492881}),
        ("Net cash from/(used in) investing activities", {"FY2025": -8189, "FY2024": -12926, "FY2023": 3236120, "FY2022": 2152360}),
        ("Net cash from/(used in) financing activities", {"FY2025": -156165, "FY2024": 255798, "FY2023": 74354, "FY2022": 1333000}),
        ("Cash and cash equivalents at end of year", {"FY2025": 1621750, "FY2024": 943912, "FY2023": 1229251, "FY2022": 2992524}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "13.5%", "FY2024": "14.0%", "FY2023": "16.1%", "FY2022": "13.9%"}),
        ("Tier 1 Ratio", {"FY2025": "16.0%", "FY2024": "16.7%", "FY2023": "16.1%", "FY2022": "18.2%"}),
        ("Total Capital Ratio", {"FY2025": "19.3%", "FY2024": "20.3%", "FY2023": "16.9%", "FY2022": "18.6%"}),
        ("Leverage Ratio", {"FY2025": "17.6%", "FY2024": "17.9%", "FY2023": "13.2%", "FY2022": "11.7%"}),
    ],
    note="Formerly Silicon Valley Bank UK Limited (formerly SVBUK Limited) - acquired by HSBC UK Bank plc "
         "for GBP1 on 13 March 2023 under the Bank of England's Special Resolution Regime, following the "
         "collapse of former US parent SVB Financial Group. FY2020-FY2021 are blank throughout (dormant "
         "pre-authorisation shell, no banking operations - FY2020 was a s480 dormant-company GBP1 shell, "
         "FY2021 an FRS 101-exempt pre-authorisation shell). LCR/NSFR only disclosed for FY2022; MREL not "
         "disclosed at this entity level in any year - see individual sheets for detail.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HSBC INNOVATION BANK FINANCIALS.xlsx")
print("Saved.")
