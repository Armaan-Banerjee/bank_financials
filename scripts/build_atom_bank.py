import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Cash flow statement only exists for FY2021-FY2022 (31 March year-end) - see
# CASH_FLOW_EXEMPTION_NOTE below. Pillar 3 covers all 5 years.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_FILING_HISTORY_URL = "https://find-and-update.company-information.service.gov.uk/company/08632552/filing-history"

P3_FY21_URL = "https://www.atombank.co.uk/~/docs/pillar-3-disclosures-20-21.pdf"
P3_FY22_URL = "https://www.atombank.co.uk/~/docs/pillar-3-disclosures-21-22.pdf"
P3_FY23_URL = "https://www.atombank.co.uk/~/docs/pillar-3-disclosures-22-23.pdf"
P3_FY24_URL = "https://www.atombank.co.uk/~/docs/atom-holdco-limited-pillar-3.pdf"
P3_FY25_URL = "https://www.atombank.co.uk/~/docs/pillar-3-disclosures-24-25.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Atom Bank Plc (company 08632552, FRN 661960, matches Banks List 2608.xlsx exactly) is the "
    "PRA-authorised entity built here. During FY2023, a new non-trading holding company - Atom Holdco Limited "
    "(later re-registered Atom Holdco plc ahead of its 2025 IPO-track listing) - was inserted above Atom Bank "
    "Plc in the group structure. From that point, Atom Bank Plc became a wholly-owned subsidiary whose results "
    "are consolidated into Atom Holdco's own published financial statements, and Pillar 3 disclosures moved from "
    "being published at Bank level to being published at Holdco (Group) level, with a separate Bank-solo column "
    "shown alongside Group in the KM1 template from FY2023 onward. All Pillar 3 figures in this workbook use the "
    "Bank column (or, for FY2021-FY2022, the single pre-restructuring figure that IS the Bank, per each report's "
    "own note: 'the comparatives reflect the previous structure where Atom bank plc was the sole regulated "
    "entity') - so there is no cash-flow-vs-Pillar-3 basis mismatch here, unlike several other banks in this "
    "project."
)

CASH_FLOW_EXEMPTION_NOTE = (
    "CASH FLOW EXEMPTION NOTE: only FY2021 and FY2022 have a Statement of Cash Flows (called 'Cash flow "
    "statements' in the source, Bank column used throughout). Both Companies House filings for those years are "
    "fully scanned/image-only (0 text blocks/page), OCR'd with tesseract and cross-verified against rendered page "
    "images. From the FY2023 Annual Report onward (confirmed directly in the FY2023 and FY2025 filings - also "
    "fully scanned, OCR'd), Atom Bank Plc's accounting policies note states: 'The Bank is exempt by virtue of "
    "s400 of the Companies Act 2006 from the requirement to prepare group financial statements... The Bank is a "
    "qualifying entity as defined by Financial Reporting Standard 101... and therefore has adopted the reduced "
    "disclosure framework of FRS 101', explicitly listing 'IAS 7 Statement of cash flows' among the disclosures "
    "exempted - the same FRS 101 'qualifying entity' exemption seen elsewhere in this project (ABC International "
    "Bank, BNY Mellon, United Trust Bank, ICICI, PNBE), but here - like Tandem Bank and AIB Group (UK) - taken "
    "only from a specific year onward rather than throughout the entity's whole history. FY2023-FY2025 are left "
    "blank on the Cash Flow Statement sheet rather than guessed."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Atom Bank Plc's own Bank-column 'Cash flow statements', £'000, from its Companies "
    "House full accounts filings (Group of companies' accounts, which for FY2021/FY2022 present Group and Bank "
    "columns side by side):\n"
    f"FY2022: full accounts made up to 31 March 2022, filed 7 Sep 2022, p.65 (Cash flow statement, Bank column) - "
    f"{CH_FILING_HISTORY_URL}\n"
    f"FY2021: group of companies' accounts made up to 31 March 2021, filed 28 Sep 2021, p.48 (Cash flow "
    f"statements, Bank column) - {CH_FILING_HISTORY_URL}\n"
    "FY2021's own closing 'Cash and balances at central banks' (£316,827k) differs from FY2022's own opening "
    "figure for the same balance (£316,826k) by £1k - an immaterial rounding difference in the source documents "
    "themselves, kept as printed in each year's own report rather than force-corrected.\n\n"
    + ENTITY_NOTE + "\n\n" + CASH_FLOW_EXEMPTION_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Atom Bank Plc (Bank-solo basis; Group basis where Bank=Group pre-restructuring, see ENTITY "
        "NOTE), Table UK KM1 - Key metrics, as at 31 March each year:\n"
        f"FY2025: Atom Holdco plc Pillar 3 Disclosures 2025, p.13 (4. Key metrics) - {P3_FY25_URL}\n"
        f"FY2024: comparative column within the FY2025 Pillar 3 Disclosures above (no separate FY2024 edition "
        f"fetched directly) - {P3_FY25_URL}\n"
        f"FY2023: Atom Holdco Limited Pillar 3 Disclosures 2023, p.12-13 (5. Key metrics) - {P3_FY23_URL}\n"
        f"FY2022: Atom Bank Plc Pillar 3 Disclosures 2021/22, p.17 (5. Key Metrics) - {P3_FY22_URL}\n"
        f"FY2021: Atom Bank Plc Pillar 3 Disclosures 2020/21, p.11 (3. Summary analysis) - {P3_FY21_URL}, "
        f"cross-checked against its identical appearance as the FY2021 comparative column in the FY2022 Pillar 3 "
        f"Disclosures above (both matched exactly).\n"
        "FY2024/FY2025 figures were originally disclosed in £m and are shown here converted to £'000 (x1,000) "
        "for consistency with FY2021-FY2023's own £'000 presentation - ratios are unaffected by this unit change."
        + extra
    )


bw = BankWorkbook(bank_name="Atom Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="146C94")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Loss for the year", {"FY2022": -11927, "FY2021": -62379}),
    ("DATA", "Depreciation and amortisation", {"FY2022": 10531, "FY2021": 10442}),
    ("DATA", "Deferred tax asset recognised", {"FY2022": -5353}),
    ("DATA", "Impairment of intangible assets", {"FY2021": 0}),
    ("DATA", "Share option scheme reserves", {"FY2022": 4585, "FY2021": 2497}),
    ("DATA", "Other non cash movements", {"FY2022": -345, "FY2021": 1307}),
    ("DATA", "Loans and advances to customers", {"FY2022": -745215, "FY2021": 331967}),
    ("DATA", "Customer deposits", {"FY2022": 1075377, "FY2021": 289607}),
    ("DATA", "Borrowing(s) from central banks", {"FY2022": 297656, "FY2021": 22612}),
    ("DATA", "Deemed loan", {"FY2022": 233156, "FY2021": -122391}),
    ("DATA", "Debt securities in issue", {"FY2022": 0, "FY2021": 0}),
    ("DATA", "Debt instruments/securities held at amortised cost", {"FY2022": 354400, "FY2021": -426192}),
    ("DATA", "Repurchase agreements", {"FY2021": 0}),
    ("DATA", "Other assets", {"FY2022": -20768, "FY2021": -4443}),
    ("DATA", "Other liabilities and provisions", {"FY2022": 20413, "FY2021": 1828}),
    ("DATA", "Derivatives held for hedging purposes", {"FY2022": -36277, "FY2021": -14013}),
    ("TOTAL", "Net Cash Inflow/(Outflow) in Operating Activities", {"FY2022": 1176233, "FY2021": 30842}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of intangible assets", {"FY2022": -9707, "FY2021": -8641}),
    ("DATA", "Acquisition of property, plant and equipment", {"FY2022": -267, "FY2021": -271}),
    ("DATA", "Net (acquisition)/maturity of debt securities at FVOCI", {"FY2022": -146282, "FY2021": 25681}),
    ("TOTAL", "Net Cash (Outflow)/Inflow from Investing Activities", {"FY2022": -156256, "FY2021": 16769}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issuance of shares, net of expenses", {"FY2022": 117443, "FY2021": 0}),
    ("DATA", "Purchase of treasury shares", {"FY2021": 0}),
    ("DATA", "Payment of principal portion of lease liabilities", {"FY2022": -650, "FY2021": -699}),
    ("TOTAL", "Net Cash Inflow/(Outflow) from Financing Activities", {"FY2022": 116793, "FY2021": -699}),
    ("TOTAL", "Net Increase in Cash and Balances at Central Banks", {"FY2022": 1136770, "FY2021": 46912}),
    ("DATA", "Cash and balances at central banks at beginning of year", {"FY2022": 316826, "FY2021": 269915}),
    ("TOTAL", "Cash and Balances at Central Banks at the End of the Year", {"FY2022": 1453596, "FY2021": 316827}),
]

bw.add_cash_flow_sheet(
    title="Atom Bank Plc — Statement of Cash Flows",
    subtitle="Bank (solo) basis, £'000. FY2023-FY2025 blank - see source note at bottom (FRS 101 cash-flow exemption).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=74,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Bank basis, {unit}" if unit else "Bank basis",
                         rows_data, sources_text, note=note, first_col_width=52, source_height=180)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 356400, "FY2024": 347300, "FY2023": 241213, "FY2022": 217158, "FY2021": 114012})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWEA",
    [("Common Equity Tier 1 ratio (%)", {"FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%", "FY2021": "15.3%"})],
    p3_sources(),
    note="Reported on a transitional (IFRS 9 relief) basis throughout, per project convention. The FY2025 Pillar 3 "
         "Disclosures state that without IFRS 9 transitional relief, FY2025's CET1 ratio would be 14.8% (Bank: "
         "14.8%) rather than the 15.0% shown - not substituted in, noted here for reference only.",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 356400, "FY2024": 347300, "FY2023": 241213, "FY2022": 217158, "FY2021": 114012})],
    p3_sources(),
    note="Tier 1 Capital = CET1 Capital every year - Atom has never held Additional Tier 1 (AT1) instruments (KM1 "
         "template shows an identical row 1/row 2 every year).",
)

metric(
    "Tier 1 Ratio", "% of RWEA",
    [("Tier 1 ratio (%)", {"FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%", "FY2021": "15.3%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 406400, "FY2024": 347300, "FY2023": 248418, "FY2022": 225151, "FY2021": 121990})],
    p3_sources(),
    note="Total Capital exceeds Tier 1 Capital from FY2025 onward once Atom's £50m Fixed Rate Reset Callable "
         "Subordinated Tier 2 notes (issued October 2024) entered regulatory capital; FY2021-FY2023 also carry a "
         "smaller Tier 2 balance (British Business Bank instruments, ~£8m in FY2021) but FY2024's KM1 template "
         "shows Total Capital = Tier 1 exactly (no Tier 2 balance that year, per the source table).",
)

metric(
    "Total Capital Ratio", "% of RWEA",
    [("Total capital ratio (%)", {"FY2025": "17.1%", "FY2024": "19.0%", "FY2023": "19.5%", "FY2022": "21.6%", "FY2021": "16.4%"})],
    p3_sources(),
    note="The FY2025 Pillar 3 Disclosures state that without IFRS 9 transitional relief, FY2025's total capital "
         "ratio would be 16.9% (Bank: 16.9%) rather than the 17.1% shown - noted for reference only, not substituted.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": 2379300, "FY2024": 1828000, "FY2023": 1271669, "FY2022": 1043001, "FY2021": 743296})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Leverage ratio total exposure measure", {"FY2025": 7174600, "FY2024": 5064500, "FY2023": 3723901, "FY2022": 3313171, "FY2021": 2914267}),
        ("Leverage ratio (%)", {"FY2025": "5.0%", "FY2024": "6.9%", "FY2023": "6.5%", "FY2022": "6.6%", "FY2021": "3.9%"}),
    ],
    p3_sources(),
    note="Atom states it is 'out of scope of the leverage ratio requirements due to retail deposits falling below "
         "the threshold of £50bn' (FY2025 Pillar 3 Disclosures) - the ratio is voluntarily calculated and "
         "monitored against an internal 3.25% floor rather than a binding regulatory minimum. No 'excluding "
         "claims on central banks' basis break is shown in Atom's own KM1 templates (unlike several other banks "
         "in this project) - one consistent methodology is used throughout FY2021-FY2025.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 2333100, "FY2024": 3849000, "FY2023": 2494398, "FY2022": 971602, "FY2021": 415697}),
        ("Total net cash outflows, adjusted value", {"FY2025": 550400, "FY2024": 534000, "FY2023": 446330, "FY2022": 310483, "FY2021": 185032}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "418.6%", "FY2024": "727.8%", "FY2023": "578.6%", "FY2022": "316.7%", "FY2021": "241.8%"}),
    ],
    p3_sources(),
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 6821300, "FY2024": 6891400, "FY2023": 5557689, "FY2022": 3492177, "FY2021": 2536566}),
        ("Total required stable funding", {"FY2025": 3987700, "FY2024": 3146100, "FY2023": 2615311, "FY2022": 2248265, "FY2021": 2029057}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "171.2%", "FY2024": "221.8%", "FY2023": "211.8%", "FY2022": "154.9%", "FY2021": "125.0%"}),
    ],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "MREL is not mentioned anywhere in any of Atom's 5 Pillar 3 Disclosures (FY2021-FY2025) - "
                       "no numeric ratio and no stated exemption, similar to several other smaller banks in this "
                       "project (e.g. Zopa, Zenith).",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2022": 1176233, "FY2021": 30842}),
        ("Net cash from/(used in) investing activities", {"FY2022": -156256, "FY2021": 16769}),
        ("Net cash from/(used in) financing activities", {"FY2022": 116793, "FY2021": -699}),
        ("Cash and balances at central banks at end of year", {"FY2022": 1453596, "FY2021": 316827}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%", "FY2021": "15.3%"}),
        ("Tier 1 Ratio", {"FY2025": "15.0%", "FY2024": "19.0%", "FY2023": "19.0%", "FY2022": "20.8%", "FY2021": "15.3%"}),
        ("Total Capital Ratio", {"FY2025": "17.1%", "FY2024": "19.0%", "FY2023": "19.5%", "FY2022": "21.6%", "FY2021": "16.4%"}),
        ("Leverage Ratio", {"FY2025": "5.0%", "FY2024": "6.9%", "FY2023": "6.5%", "FY2022": "6.6%", "FY2021": "3.9%"}),
        ("LCR", {"FY2025": "418.6%", "FY2024": "727.8%", "FY2023": "578.6%", "FY2022": "316.7%", "FY2021": "241.8%"}),
        ("NSFR", {"FY2025": "171.2%", "FY2024": "221.8%", "FY2023": "211.8%", "FY2022": "154.9%", "FY2021": "125.0%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Cash flow is blank for FY2023-FY2025 (FRS 101 qualifying-"
         "entity exemption took effect from FY2023, following the insertion of Atom Holdco above Atom Bank Plc - "
         "see Cash Flow Statement sheet note). Unlike several other banks in this project, all ratios here are on "
         "a consistent Bank-solo basis throughout - no cash-flow-vs-Pillar-3 basis mismatch.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ATOM BANK FINANCIALS.xlsx")
print("Saved ATOM BANK FINANCIALS.xlsx")
