import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Fiscal year-end 31 December. Only 4 years sourced (FY2022-FY2025) - see
# ENTITY_NOTE; no FY2021 was pursued given diminishing returns on a small bank.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzUxODk3MTQ2NWFkaXF6a2N4/document?format=pdf"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzQyNTcyMzI0MGFkaXF6a2N4/document?format=pdf"
P3_2023_URL = "https://www.ubluk.com/media/lupbssja/annual-report-unb-2023-pillar3-final-approved.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: United National Bank Limited (Companies House 04146820) was formed in 2001 from the merger of the "
    "UK branches of two Pakistani banks, United Bank Limited ('UBL') and National Bank of Pakistan ('NBP'), who had "
    "operated in the UK since the 1960s - historically 55% UBL / 45% NBP owned, trading as 'UBL UK'. In July 2024, "
    "following regulatory approval, Bestway Group Financial Services Limited (a wholly-owned subsidiary of Bestway "
    "Group, a UK diversified conglomerate) acquired 95.1% of the Company's shares from UBL and NBP - the Company is "
    "now majority UK-owned rather than a foreign subsidiary in the usual sense, though UBL/NBP retain a residual "
    "stake and a preference-share arrangement (see Notes). All financial statements are prepared under FRS 102 in "
    "Pound Sterling (the Company's functional currency) - no cash-flow-statement exemption is taken.\n\n"
    "DATA AVAILABILITY NOTE: only 4 years (FY2022-FY2025) were sourced from the last two Companies House annual "
    "report filings (both fully scanned/image-only PDFs, transcribed via OCR - tesseract - and cross-checked "
    "against each other's comparative columns, which matched exactly). No FY2021 was pursued. Pillar 3: the "
    "pre-Bestway entity ('UBL UK') published 'unaudited Pillar III and Remuneration Code Disclosures' on its own "
    "site (ubluk.com) - a text-based FY2023 edition was found and used, but the FY2022 edition's URL returned the "
    "website's navigation shell rather than the actual PDF (not retried further given time constraints), and no "
    "FY2024/FY2025 edition was found - the FY2025 Annual Report's own 'Capital management and adequacy' section no "
    "longer references a separate Pillar 3 document at all (unlike the FY2023 Annual Report, which explicitly "
    "pointed to ubluk.com), suggesting standalone Pillar 3 disclosure may have lapsed post-Bestway acquisition - "
    "this is an inference, not confirmed. Consequently Pillar 3 ratios/RWA/leverage are only solidly available for "
    "FY2023 (plus a narrative-only FY2022 leverage ratio); FY2024/FY2025 ratios and RWA, and LCR/NSFR/MREL for "
    "every year, are 'Not disclosed' rather than guessed."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are United National Bank Limited's own Statement of Cash Flows, exact £ as reported "
    "(not rounded to £'000/£m):\n"
    f"FY2025 & FY2024: Annual report and financial statements 2025, p.26 (Statement of cash flows) - {AR2025_URL}\n"
    f"FY2023 & FY2022 (as restated): Annual report and financial statements 2023, p.32 (Statement of cash flows) - "
    f"{AR2023_URL}\n"
    "FY2023's own closing balance (£9,725,415) matches the FY2025 report's own FY2024 opening balance exactly, "
    "confirming consistency across the two source documents. FY2022 is labelled '(as restated)' in the FY2023 "
    "report - its original as-first-reported FY2022 figures were not sourced separately.\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - United National Bank Limited (trading as 'UBL UK' at the time) Pillar 3 basis:\n"
        f"FY2023: UBL UK Pillar 3 and Remuneration Code Disclosures at 31 December 2023, various pages (Table LRSum/"
        f"LRCom p.47-48; Appendix VI Own funds disclosure p.61-63) - {P3_2023_URL}\n"
        f"FY2022 leverage ratio only: quoted as the prior-year comparator within the FY2023 Pillar 3 document above "
        f"(narrative text, no supporting table found).\n"
        f"Tier 1 capital and Total capital £ amounts for all 4 years are instead sourced from each year's own "
        f"audited Annual Report (see Cash Flow Statement sheet source note for URLs), 'Capital management and "
        f"adequacy' / 'Capital resources' section."
    )


bw = BankWorkbook(bank_name="United National Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="4A1E4D")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax on ordinary activities for the year", {"FY2025": 14576858, "FY2024": 5243939, "FY2023": 6911228, "FY2022": 5296311}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 297373, "FY2024": 344925, "FY2023": 597021, "FY2022": 755530}),
    ("DATA", "Remeasurement of financial liability", {"FY2025": 291571, "FY2024": 2561700, "FY2023": 2650000}),
    ("DATA", "Net (reversal)/charge in respect of defined benefit pension scheme", {"FY2025": 36000, "FY2024": 35000, "FY2023": -54000, "FY2022": 3000}),
    ("DATA", "Impairment charge/(recoveries) on loans and advances and other items", {"FY2025": 555015, "FY2024": 277396, "FY2023": -133448, "FY2022": -190335}),
    ("DATA", "Impairment (recoveries)/charge on available for sale investments", {"FY2023": -43724, "FY2022": 5081559}),
    ("DATA", "Non-cash movements relating to AFS debt securities", {"FY2025": 1798841, "FY2024": 518237, "FY2023": -38664, "FY2022": 472140}),
    ("DATA", "Fair value (gain)/loss on investment properties", {"FY2025": 60000, "FY2024": 1692678, "FY2023": -157448}),
    ("DATA", "Fair value losses on derivatives", {"FY2025": 36260, "FY2024": 8502}),
    ("DATA", "Disposal of fixed assets - non cash", {"FY2024": -46958, "FY2022": -950000}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents (within adjustments)", {"FY2025": 78789, "FY2024": 203350, "FY2023": -1040191, "FY2022": 1310294}),
    ("DATA", "Change in loans to banks", {"FY2025": -771732, "FY2024": -9040080, "FY2023": -11575956, "FY2022": 253159}),
    ("DATA", "Change in loans and advances", {"FY2025": -508526134, "FY2024": -314034689, "FY2023": -82406357, "FY2022": -129900329}),
    ("DATA", "Change in other operating assets", {"FY2025": 1574513, "FY2024": -4401232, "FY2023": -2726540, "FY2022": -1703767}),
    ("DATA", "Change in deposits from banks and customers", {"FY2025": 614962983, "FY2024": 368365721, "FY2023": 75751608, "FY2022": 145891909}),
    ("DATA", "Change in other operating liabilities", {"FY2025": 4362320, "FY2024": 3532520, "FY2023": 4913759, "FY2022": -5203335}),
    ("DATA", "Corporate income tax paid", {"FY2025": -1630000, "FY2024": -1440000, "FY2023": -907009, "FY2022": -563132}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": 127702657, "FY2024": 53821009, "FY2023": -8259721, "FY2022": 20553004}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of tangible fixed and intangible assets", {"FY2025": -2953578, "FY2024": -246091, "FY2023": -710084, "FY2022": -216696}),
    ("DATA", "Proceeds from disposal of fixed assets", {"FY2024": 237859, "FY2022": 950000}),
    ("DATA", "Purchase of debt securities", {"FY2025": -1051570428, "FY2024": -750228210, "FY2023": -595299208, "FY2022": -572112956}),
    ("DATA", "Sale and maturity of debt securities", {"FY2025": 931907787, "FY2024": 714471065, "FY2023": 586985878, "FY2022": 526168675}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -122616219, "FY2024": -35765377, "FY2023": -9023414, "FY2022": -45210977}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of obligations under finance lease", {"FY2024": -21710, "FY2023": -19823, "FY2022": -8263}),
    ("DATA", "Proceeds from/(repayment of) repurchase agreements", {"FY2024": -19284670, "FY2023": 19284670}),
    ("DATA", "Dividends paid", {"FY2022": -1015000}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2024": -19306380, "FY2023": 19264847, "FY2022": -1023263}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 5086438, "FY2024": -1250748, "FY2023": 1981712, "FY2022": -25681236}),
    ("DATA", "Cash and cash equivalents at the beginning of the financial year", {"FY2025": 8271317, "FY2024": 9725415, "FY2023": 6703512, "FY2022": 33695042}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents (tail)", {"FY2025": -78789, "FY2024": -203350, "FY2023": 1040191, "FY2022": -1310294}),
    ("TOTAL", "Cash and cash equivalents at the end of the financial year", {"FY2025": 13278966, "FY2024": 8271317, "FY2023": 9725415, "FY2022": 6703512}),
]

bw.add_cash_flow_sheet(
    title="United National Bank Limited — Cash Flow Statement",
    subtitle="Company basis, exact £ (not £'000/£m) - see source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=260,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Company basis, {unit}" if unit else "Company basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=150)


metric(
    "CET1 Capital", "£",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 108644570, "FY2024": 97948100, "FY2023": 88559510, "FY2022": 73598731})],
    p3_sources(),
    note="Equal to Tier 1 capital in every year - the Company has no Additional Tier 1 (AT1) instruments. FY2023's "
         "figure is confirmed to the nearest £'000 by the Pillar 3 document's own Appendix VI (£88,559k).",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2023": "21.46%", "FY2022": "Not disclosed", "FY2024": "Not disclosed", "FY2025": "Not disclosed"})],
    p3_sources(),
    note="Only FY2023 is directly evidenced (equal to the Pillar 3 document's stated Tier 1 ratio, since CET1=Tier 1 "
         "capital exactly that year). No Pillar 3 document was found for FY2022, FY2024 or FY2025, and Total RWAs "
         "aren't disclosed for those years either, so the ratio cannot be reliably derived - left as Not disclosed "
         "rather than estimated.",
)

metric(
    "Tier 1 Capital", "£",
    [("Tier 1 capital", {"FY2025": 108644570, "FY2024": 97948100, "FY2023": 88559510, "FY2022": 73598731})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2023": "21.46%", "FY2022": "Not disclosed", "FY2024": "Not disclosed", "FY2025": "Not disclosed"})],
    p3_sources(),
    note="Directly stated in the FY2023 Pillar 3 document (Table CC1, row 62); other years not disclosed (see CET1 "
         "Ratio sheet note).",
)

metric(
    "Total Capital", "£",
    [("Total capital", {"FY2025": 109906178, "FY2024": 98654693, "FY2023": 89004384, "FY2022": 73967261})],
    p3_sources(),
    note="Tier 1 capital plus a Tier 2 collective provision figure disclosed in each year's own Annual Report.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2023": "21.56%", "FY2022": "Not disclosed", "FY2024": "Not disclosed", "FY2025": "Not disclosed"})],
    p3_sources(),
    note="Directly stated in the FY2023 Pillar 3 document (Table CC1, row 63); other years not disclosed.",
)

metric(
    "Total RWAs", "£",
    [("Total risk-weighted exposure amount", {"FY2023": 412732000, "FY2022": "Not disclosed", "FY2024": "Not disclosed", "FY2025": "Not disclosed"})],
    p3_sources(),
    note="FY2023 only (Pillar 1 Capital Requirement table). No RWA figure was found for any other year.",
)

metric(
    "Leverage Ratio", "£ / %",
    [
        ("Leverage ratio total exposure measure", {"FY2023": 954151000}),
        ("Leverage ratio (%)", {"FY2023": "8.52%", "FY2022": "8.43%", "FY2024": "Not disclosed", "FY2025": "Not disclosed"}),
    ],
    p3_sources(),
    note="FY2022's 8.43% is quoted from the FY2023 Pillar 3 document's own narrative text as the prior-year "
         "comparator - no supporting exposure-measure table for FY2022 was located. FY2024/FY2025 not disclosed "
         "(no Pillar 3 document found for those years - see entity note on the Cash Flow Statement sheet).",
)

bw.add_not_disclosed_metric_sheets(["LCR", "NSFR"], p3_sources())

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed" for y in YEARS})],
    p3_sources(),
    note="No numeric or qualitative MREL disclosure of any kind was found for this bank in any year reviewed.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 127702657, "FY2024": 53821009, "FY2023": -8259721, "FY2022": 20553004}),
        ("Net cash from/(used in) investing activities", {"FY2025": -122616219, "FY2024": -35765377, "FY2023": -9023414, "FY2022": -45210977}),
        ("Net cash from/(used in) financing activities", {"FY2024": -19306380, "FY2023": 19264847, "FY2022": -1023263}),
        ("Cash and cash equivalents at end of year", {"FY2025": 13278966, "FY2024": 8271317, "FY2023": 9725415, "FY2022": 6703512}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2023": "21.46%"}),
        ("Tier 1 Ratio", {"FY2023": "21.46%"}),
        ("Total Capital Ratio", {"FY2023": "21.56%"}),
        ("Leverage Ratio", {"FY2023": "8.52%", "FY2022": "8.43%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Pillar 3 data is sparse - solidly available only for FY2023, "
         "since no standalone Pillar 3 document was found for FY2022 (beyond a narrative leverage-ratio figure), "
         "FY2024, or FY2025 - the FY2025 Annual Report no longer references one at all, following the 2024 change "
         "of majority ownership to Bestway Group (see Cash Flow Statement sheet entity note). LCR/NSFR/MREL: "
         "not disclosed in any year reviewed.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/UNITED NATIONAL FINANCIALS.xlsx")
