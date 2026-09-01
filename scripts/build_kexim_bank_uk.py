import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: KEXIM Bank (UK) Limited (company 02693038, FRN 204490,
# formerly KEXIM International (U.K.) Limited) is the wholly-owned UK subsidiary of
# the Export-Import Bank of Korea ("KEXIM", the sole shareholder). It takes the FRS
# 101 "presentation of a cash flow statement" disclosure exemption every year -
# confirmed explicitly in Note 2 "Significant accounting policies" of the FY2025
# Annual Report ("As permitted by FRS 101, the Bank has taken advantage of the
# disclosure exemptions available under that standard in relation to ... presentation
# of a cash flow statement ...", with "a statement of cash flows for the period"
# listed as the first bulleted exemption applied). No Contents/statement list in any
# of the 5 filings includes a cash flow statement. Follows the BNY Mellon
# International / ABC International Bank / Bank Mandiri Europe / DB UK Bank
# precedent: 13-sheet Pillar-3-only structure.
#
# No dedicated Pillar 3 document exists for this entity and no reachable bank-owned
# website was found this session (see WEBSITE_NOTE below) - the ONLY capital metric
# disclosed anywhere in the 5 Annual Reports checked is a single combined "Common
# Equity Tier 1 and total capital adequacy ratio" percentage, stated once per report
# in the Strategic Report's "Review of the business" section, with a prior-year
# comparative given each time (independently cross-checked and consistent across all
# 5 consecutive report-pairs - no restatements). No £ CET1/Tier1/Total Capital
# amount, no RWA figure, no Tier 1-vs-CET1 breakdown, no Leverage Ratio, LCR, NSFR or
# MREL Ratio is disclosed anywhere in the Strategic Report, Directors' Report, Risk
# Management notes, or the Notes to the Financial Statements (including Note 27
# "Parent and subsidiary relationships", which only refers the reader to the parent
# Export-Import Bank of Korea's own group accounts, and Note 28, which is an
# unrelated Capital Requirements (Country-by-Country Reporting) Regulations 2013
# disclosure, not a Pillar 3/capital-adequacy note). All 5 Companies House filings
# are fully scanned (image-only, 0 extractable text layer) - transcribed via
# targeted page-image reads, not full-document OCR.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

FY2025_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzUzMDYxMTU0N2FkaXF6a2N4/document?format=pdf&download=0"
FY2024_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzQ2ODk1NTg1M2FkaXF6a2N4/document?format=pdf&download=0"
FY2023_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzQyMzUxMTIzMWFkaXF6a2N4/document?format=pdf&download=0"
FY2022_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzM4NTcxODk4NWFkaXF6a2N4/document?format=pdf&download=0"
FY2021_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzM0NjA0OTUyMGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: KEXIM Bank (UK) Limited (company 02693038, FRN 204490, incorporated 3 March 1992 as KEXIM "
    "International (U.K.) Limited) is a wholly-owned subsidiary of the Export-Import Bank of Korea (\"the Parent "
    "Bank\"), which is itself 100% owned by the Korean government and is registered in South Korea. The Bank's "
    "principal activity is wholesale banking - providing credit facilities to corporates with a Korean linkage. "
    "All figures below are on the Bank's own entity-level basis, reported in pound Sterling throughout (no FX "
    "conversion needed) - it has no subsidiaries of its own."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: the FY2025 Annual Report's Note 2 \"Significant accounting policies - Basis of "
    "accounting\" states the financial statements are prepared in accordance with FRS 101 'Reduced Disclosure "
    "Framework' and that the Bank has taken advantage of the available disclosure exemptions, the first bulleted "
    f"item being \"a statement of cash flows for the period\" - KEXIM Bank (UK) Limited Annual Report 2025, p.31 - "
    f"{FY2025_AR_URL}. No cash flow statement appears in any of the 5 filings checked (FY2021-FY2025), consistent "
    "with a standing structural feature of this entity's accounts, not a one-off. Per the project's established "
    "policy for this exemption (see The Bank of New York Mellon (International) Limited / ABC International Bank "
    "plc / Bank Mandiri (Europe) Limited / DB UK Bank Limited), this workbook is built as a PILLAR-3-ONLY variant: "
    "the capital metric that is disclosed is populated below, but no cash flow figures exist to show."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

WEBSITE_NOTE = (
    "ACCESS NOTE: the domain keximbank.co.uk (as listed in some directories) resolves to an unrelated Fasthosts "
    "domain-parking page, not the Bank's own site. Two other plausible domains (keximuk.com, kexim.co.uk) either "
    "did not resolve or refused connections this session, and the Wayback Machine returned persistent HTTP 429 "
    "rate-limit responses throughout this session (a known ongoing Internet Archive-side issue also seen on "
    "other tickets in this project - not bank-specific). No standalone Pillar 3 document could therefore be "
    "located this session; worth a revisit with fresh Wayback/WebSearch budget."
)

NOT_DISCLOSED_NOTE = (
    "No dedicated Pillar 3 document is published by this entity that could be located this session (see the "
    "access note on the Cash Flow Statement sheet), and no separate quantitative capital note exists in any of "
    "the 5 Annual Reports checked (FY2021-FY2025) beyond the single combined ratio disclosed on the CET1 Ratio "
    "and Total Capital Ratio sheets - this metric is not disclosed in any form in any of the 5 filings checked, "
    "including Note 27 (which only refers to the Parent Bank's own group accounts) and Note 28 (an unrelated "
    "Country-by-Country Reporting disclosure)."
)


def p3_sources(extra=""):
    return (
        "Sources - KEXIM Bank (UK) Limited, all figures GBP (no FX conversion needed), from each year's own "
        "Companies House full-accounts filing, Strategic Report, 'Review of the business' section:\n"
        f"FY2025: Annual Report 2025, p.3 (\"The Bank's Common Equity Tier 1 and total capital adequacy ratios "
        f"decreased to 20.5% at the end of 2025 (2024: 20.9%)\") - {FY2025_AR_URL}\n"
        f"FY2024: Annual Report 2024, p.3 (\"...has decreased to 20.9% at the end of 2024 (2023: 22.8%)\") - "
        f"{FY2024_AR_URL} (independently cross-checked against the FY2025 report's own FY2024 comparative above - "
        "consistent, no restatement)\n"
        f"FY2023: Annual Report 2023, p.3 (\"...has increased slightly to 22.8% at the end of 2023 (2022: "
        f"22.5%)\") - {FY2023_AR_URL} (cross-checked against the FY2024 report's comparative - consistent)\n"
        f"FY2022: Annual Report 2022, p.3 (\"...has reduced to 22.5% at the end of 2022 (2021: 30%)\") - "
        f"{FY2022_AR_URL} (cross-checked against the FY2023 report's comparative - consistent)\n"
        f"FY2021: Annual Report 2021, p.3 (\"...ratios improved from 13.5% and 18.0% respectively at the end of "
        f"2019, to both being 36.4% at the end of 2020 and 30.0% following the partial deployment of this capital "
        f"by the end of 2021\") - {FY2021_AR_URL} (cross-checked against the FY2022 report's comparative - "
        "consistent). All 5 filings are fully scanned (image-only); figures transcribed via targeted page-image "
        "reads of the Strategic Report's 'Review of the business' section (p.3 in every filing).\n"
        + (extra + "\n" if extra else "")
    )


bw = BankWorkbook(bank_name="KEXIM Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="7A1F2B")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the notes below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="KEXIM Bank (UK) Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source notes below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES + "\n\n" + WEBSITE_NOTE,
    first_col_width=90,
    source_height=340,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=190)


CAPITAL_RATIO = {"FY2025": "20.5%", "FY2024": "20.9%", "FY2023": "22.8%", "FY2022": "22.5%", "FY2021": "30.0%"}

RATIO_NOTE = (
    "The source discloses this as a single combined \"Common Equity Tier 1 and total capital adequacy ratio\" "
    "(the same percentage for both measures, explicitly stated as one figure covering both in every one of the 5 "
    "reports checked) - populated identically on both the CET1 Ratio and Total Capital Ratio sheets rather than "
    "assumed for only one. No £ CET1/Total Capital amount and no RWA figure is disclosed anywhere, so the "
    "underlying capital amount cannot be calculated. Tier 1 Ratio is not separately disclosed (no AT1/Tier 2 "
    "instruments are mentioned in any report, but the source never explicitly confirms Tier 1 = CET1 = Total "
    "Capital, so Tier 1 Ratio is left not-disclosed rather than assumed equal)."
)

bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital"], p3_sources(), per_note={"CET1 Capital": NOT_DISCLOSED_NOTE},
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 ratio", CAPITAL_RATIO)],
    p3_sources(),
    note=RATIO_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["Tier 1 Capital", "Tier 1 Ratio", "Total Capital"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Tier 1 Capital", "Tier 1 Ratio", "Total Capital"]},
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital adequacy ratio", CAPITAL_RATIO)],
    p3_sources(),
    note=RATIO_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Total RWAs", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 / Total Capital Ratio", CAPITAL_RATIO),
    ],
    note="This is a PILLAR-3-ONLY workbook: KEXIM Bank (UK) Limited takes the FRS 101 cash-flow-statement "
         "exemption every year (see the Cash Flow Statement sheet), so no cash flow summary or chart is shown "
         "here - only the capital ratio trend chart below. No dedicated Pillar 3 document could be located for "
         "this entity this session (see the Cash Flow Statement sheet's access note); the only capital metric "
         "disclosed anywhere is a single combined CET1/Total Capital adequacy ratio, stated once per year in each "
         "Annual Report's Strategic Report - all 5 years fully cross-checked and consistent, no restatements.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/KEXIM BANK UK FINANCIALS.xlsx")
