import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {
    "FY2025": "FY2025",
    "FY2024": "FY2024",
    "FY2023": "FY2023",
    "FY2022": "FY2022",
    "FY2021": "FY2021*",
}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/12546585/filing-history"
AR2024_URL = AR2025_URL
AR2023_URL = AR2025_URL
AR2022_URL = AR2025_URL
AR2021_URL = AR2025_URL
P3_2022_URL = "https://www.hsbcinnovationbanking.com/-/media/hinv/pdf/regulations/pillar-3-report-2022.pdf"

ENTITY_NOTE = (
    "\nENTITY HISTORY: HSBC Innovation Bank Limited (company 12546585) was incorporated in April 2020 as "
    "SVBUK Limited, a dormant shell company seeking UK bank authorisation. It had no banking operations in "
    "FY2021 (loss of GBP477k, funded by a loan from Silicon Valley Bank's UK Branch purely to pay "
    "non-executive director fees) and, being a small company under FRS 101's Reduced Disclosure Framework "
    "that year, published no cash flow statement or Pillar 3 disclosure at all - FY2021 is left blank here "
    "rather than guessed. The actual banking business (Silicon Valley Bank UK Branch) was transferred into "
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
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - HSBC Innovation Bank Limited Pillar 3 / capital disclosure basis:\n"
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
    subtitle="As reported in each year's own Companies House-filed Annual Report and Accounts. FY2021 is "
              "blank - the entity was a dormant, pre-authorisation shell that year with no banking "
              "operations and no cash flow statement published under its FRS 101 exemption (see source note).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=210,
    unit_suffix=" (£'000)",
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
    note="Only disclosed for FY2022 (the only year with a standalone Pillar 3 report) - not publicly "
         "disclosed at this entity level FY2023-FY2025 (see source note).",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (adjusted value)", {"FY2022": "203%"})],
    p3_sources(
        extra="FY2022's 203% is a 2-quarter (not 4-quarter) average, for the same reason as LCR above - per "
              "the Pillar 3 report's own footnote."
    ),
    note="Only disclosed for FY2022 (the only year with a standalone Pillar 3 report) - not publicly "
         "disclosed at this entity level FY2023-FY2025 (see source note).",
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
         "collapse of former US parent SVB Financial Group. FY2021 is blank throughout (dormant "
         "pre-authorisation shell, no banking operations, FRS 101 exemption). LCR/NSFR only disclosed for "
         "FY2022; MREL not disclosed at this entity level in any year - see individual sheets for detail.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HSBC INNOVATION BANK FINANCIALS.xlsx")
print("Saved.")
