import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: DB UK Bank Limited (company 00315841, FRN 140848) is a UK
# private-banking/wealth-management subsidiary of Deutsche Bank AG (via Deutsche
# Holdings Limited -> DB Investments (GB) Limited -> Deutsche Bank AG). It takes the
# FRS 101 "Cashflow Statement and related notes (IAS 7)" disclosure exemption every
# year - confirmed as a standing feature across three filing vintages 4 years apart
# (FY2021, FY2023, FY2025 Annual Reports all list the same exemption in their
# "Basis of preparation" note, and none of their Contents pages lists a cash flow
# statement). Follows the BNY Mellon International / ABC International Bank /
# Bank Mandiri Europe precedent: 13-sheet structure, Cash Flow Statement sheet
# documents the exemption instead of line items, Overview sheet omits the cash-flow
# chart.
#
# No dedicated Pillar 3 document exists and no standalone Pillar 3 page was found on
# db.com. The ONLY capital/liquidity figures found anywhere in the Annual Reports
# are: a single generic "regulatory capital ratio" (unaudited) mentioned once in the
# Going Concern paragraph of Note 1 (no CET1/Tier 1/Total Capital breakdown, no RWA,
# no £ capital amount - just the one ratio, for the report's own year only, never a
# prior-year comparative), and a Liquidity Risk KPI table (note 27/29 "Risk Report")
# giving LCR and NSFR for the current and one comparative year. All figures reported
# in GBP (the Company's functional currency) - no FX conversion needed.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

FY2025_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/00315841/filing-history/MzUxOTM5NDA3NGFkaXF6a2N4/document?format=pdf&download=0"
FY2023_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/00315841/filing-history/MzQyMDM4NDU3MmFkaXF6a2N4/document?format=pdf&download=0"
FY2021_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/00315841/filing-history/MzMzODM1NTI4NGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: DB UK Bank Limited (company 00315841, FRN 140848, incorporated 30 June 1936) is a wholly-owned "
    "subsidiary of Deutsche Holdings Limited (\"DHL\"), itself wholly owned by DB Investments (GB) Limited "
    "(\"DBIGB\"), whose parent is Deutsche Bank Aktiengesellschaft (\"DB AG\", Germany). The Company provides "
    "Wealth Management services to High and Ultra High Net Worth clients as part of Deutsche Bank's Private Bank. "
    "All figures below are on the Company's own entity-level basis - it has no subsidiaries of its own."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: the FY2025 Annual Report's Note 1 \"Basis of preparation\" states the Company has "
    "applied the FRS 101 exemptions available in respect of, among others, \"A Cashflow Statement and related notes "
    "(the requirements of IAS 7 Statement of Cash Flows and the requirements of paragraphs 10(d) and 111 of IAS 1)\" "
    f"- DB UK Bank Limited Annual Report 2025, p.29 - {FY2025_AR_URL}. The identical exemption (worded slightly more "
    f"briefly, \"A Cashflow Statement and related notes\") appears in the FY2023 Annual Report (p.29 - "
    f"{FY2023_AR_URL}) and the FY2021 Annual Report (p.26 - {FY2021_AR_URL}), confirming this is a standing "
    "structural feature across the entity's history (checked 4 years apart), not a one-off. None of the three "
    "filings' own Contents pages lists a cash flow statement. Per the project's established policy for this "
    "exemption (see The Bank of New York Mellon (International) Limited / ABC International Bank plc / Bank "
    "Mandiri (Europe) Limited), this workbook is built as a PILLAR-3-ONLY variant: the capital/liquidity metrics "
    "that are disclosed are populated below, but no cash flow figures exist to show."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

NOT_DISCLOSED_NOTE = (
    "No dedicated Pillar 3 document is published by this entity, and no separate regulatory-disclosures page for "
    "DB UK Bank Limited was found on db.com. The only capital/liquidity figures found anywhere in the FY2021, "
    "FY2023 and FY2025 Annual Reports (the three filings checked) are a single generic \"regulatory capital ratio\" "
    "(see Total Capital Ratio sheet) and LCR/NSFR (see those sheets) - this metric is not disclosed in any form in "
    "any of the three filings checked."
)


def p3_sources(extra=""):
    return (
        "Sources - DB UK Bank Limited, all figures GBP (no FX conversion needed):\n"
        f"FY2025: Annual Report 2025, Note 1 Going Concern paragraph (regulatory capital ratio, p.29) and Note 27 "
        f"Risk Report (c) Liquidity Risk KPI table (LCR/NSFR, p.65) - {FY2025_AR_URL}\n"
        f"FY2024: Annual Report 2025's own FY2024 comparative column in the same Note 27 Liquidity Risk KPI table "
        f"(p.65) - {FY2025_AR_URL}. No FY2024 capital ratio found (the going-concern note only ever states the "
        "report's own current year, never a prior-year comparative) - left blank, not estimated.\n"
        f"FY2023: Annual Report 2023, Note 1 Going Concern paragraph (regulatory capital ratio, p.29) and Note 29 "
        f"Risk Report (c) Liquidity Risk KPI table (LCR/NSFR, p.65) - {FY2023_AR_URL}\n"
        f"FY2022: Annual Report 2023's own FY2022 comparative column in the same Note 29 Liquidity Risk KPI table "
        f"(p.65) - {FY2023_AR_URL}. No FY2022 capital ratio found (same reason as FY2024) - left blank.\n"
        f"FY2021: Annual Report 2021, Note 1 Going Concern paragraph (regulatory capital ratio and LCR, p.26) - "
        f"{FY2021_AR_URL}. No NSFR for FY2021 - the Company's own FY2023 Annual Report states NSFR only became a "
        "regulatory requirement \"from 1 January 2022\", consistent with no NSFR being mentioned anywhere in the "
        "FY2021 report - left blank, not estimated, not a gap.\n"
        + (extra + "\n" if extra else "")
    )


bw = BankWorkbook(bank_name="DB UK Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="995A1C")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="DB UK Bank Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=300,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


TOTAL_CAPITAL_RATIO = {"FY2025": "536%", "FY2023": "491%", "FY2021": "473%"}
LCR = {"FY2025": "381%", "FY2024": "351%", "FY2023": "437%", "FY2022": "304%", "FY2021": "459%"}
NSFR = {"FY2025": "202%", "FY2024": "140%", "FY2023": "213%", "FY2022": "235%"}

# Sheet order matches the project-wide standard (CET1 Capital/Ratio, Tier 1 Capital/Ratio,
# Total Capital/Ratio, Total RWAs, Leverage Ratio, LCR, NSFR, MREL Ratio) even though this
# entity only discloses Total Capital Ratio/LCR/NSFR.
bw.add_not_disclosed_metric_sheets(
    ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in
              ["CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio", "Total Capital"]},
)

metric(
    "Total Capital Ratio", "% (unaudited)",
    [("Regulatory capital ratio", TOTAL_CAPITAL_RATIO)],
    p3_sources(),
    note="Only a single generic 'regulatory capital ratio' is disclosed, mentioned once in each report's Going "
         "Concern paragraph - no CET1/Tier 1 breakdown exists anywhere, and no £ capital amount or RWA figure is "
         "disclosed either (so Total RWAs cannot be calculated). This ratio is described only as 'well above the "
         "regulatory minimum of 100%' and is explicitly marked unaudited in the source. Placed on Total Capital "
         "Ratio (the broadest measure) rather than assumed equal to CET1/Tier 1, since the source never specifies "
         "which capital tier(s) the ratio uses.",
)

bw.add_not_disclosed_metric_sheets(
    ["Total RWAs", "Leverage Ratio"],
    p3_sources(),
    per_note={m: NOT_DISCLOSED_NOTE for m in ["Total RWAs", "Leverage Ratio"]},
)

metric(
    "LCR", "% (unaudited)",
    [("Liquidity Coverage Ratio", LCR)],
    p3_sources(),
    note="No £ breakdown (HQLA, net cash outflows) is disclosed anywhere - only the ratio itself. Explicitly "
         "marked unaudited in the source (Risk Report note (c) Liquidity Risk is headed '(unaudited)').",
)

metric(
    "NSFR", "% (unaudited)",
    [("Net Stable Funding Ratio", NSFR)],
    p3_sources(),
    note="No £ breakdown (available/required stable funding) is disclosed anywhere - only the ratio itself. "
         "FY2021 genuinely blank: the Company's own FY2023 Annual Report states NSFR only became a regulatory "
         "requirement from 1 January 2022, and no NSFR figure appears anywhere in the FY2021 Annual Report.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": NOT_DISCLOSED_NOTE},
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="This is a PILLAR-3-ONLY workbook: DB UK Bank Limited takes the FRS 101 cash-flow-statement exemption "
         "every year (see the Cash Flow Statement sheet), so no cash flow summary or chart is shown here - only "
         "the capital/liquidity ratio trend chart below. No dedicated Pillar 3 document is published by this "
         "entity; only a single generic 'regulatory capital ratio' (no CET1/Tier 1 breakdown, 3 of 5 years only), "
         "LCR (5 of 5 years) and NSFR (4 of 5 years, not applicable pre-2022) are disclosed, each in a different "
         "part of the Annual Report's own Notes - see each sheet's own source citation.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/DB UK BANK FINANCIALS.xlsx")
