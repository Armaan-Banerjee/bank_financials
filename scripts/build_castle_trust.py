import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, y/e 30 September

CH_FY2025_URL = "https://find-and-update.company-information.service.gov.uk/company/07454474/filing-history/MzUwMDY5OTYyMGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2024_URL = "https://find-and-update.company-information.service.gov.uk/company/07454474/filing-history/MzQ1MzY3NTE2MGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2023_URL = "https://find-and-update.company-information.service.gov.uk/company/07454474/filing-history/MzQxNTc2MDk1NGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2022_URL = "https://find-and-update.company-information.service.gov.uk/company/07454474/filing-history/MzM2MzAyNjk5NGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2021_URL = "https://find-and-update.company-information.service.gov.uk/company/07454474/filing-history/MzMzNDg3NzA5MWFkaXF6a2N4/document?format=pdf&download=0"

P3_2025_URL = "https://www.castletrust.co.uk/wp-content/uploads/fy-30_sept-2025-ctb-pillar-3-disclosures.pdf"
P3_2024_URL = "https://www.castletrust.co.uk/wp-content/uploads/fy-30_sept-2024-ctb-pillar-3-disclosures.pdf"
P3_2023_URL = "https://www.castletrust.co.uk/wp-content/uploads/fy-30-sept-2023-ctb-pillar-3-disclosures.pdf"
P3_2022_URL = "https://www.castletrust.co.uk/wp-content/uploads/fy-30-sept-2022-ctb-pillar-3-disclosures.pdf"
P3_2021_URL = "https://www.castletrust.co.uk/wp-content/uploads/fy-30-sept-2021-ctb-pillar-3-disclosures.pdf"

ENTITY_NOTE = (
    "Castle Trust Capital plc (company 07454474, FRN 541910, trading as 'Castle Trust Bank') is a "
    "wholly-owned subsidiary of Castle Trust Holdings Limited ('CTH', company 12161224) and has availed "
    "itself of the exemption under s.400 Companies Act 2006 to not prepare group accounts - its own "
    "statutory accounts (sourced here) are solo/Company-only, not consolidated, and are a genuinely "
    "different document from CTH's own consolidated 'Annual report and financial statements' (also "
    "published on the bank's website) which cover the wider Group. Cash flow figures on this sheet are "
    "Castle Trust Capital plc solo, matching the Pillar 3 sheets' 'Bank' (not 'Group') columns - kept "
    "consistent throughout to avoid a cash-flow-vs-Pillar-3 basis mismatch. All 5 Companies House filings "
    "for this entity are fully scanned/image-only; figures were transcribed via page rendering and "
    "cross-checked against each year's own report where it appears again as the following year's "
    "comparative column.\n"
    "One genuine cross-vintage discrepancy found, not silently resolved: the FY2022 Annual Report's own "
    "note states 'Certain items in operating activities have been reclassified in the prior year "
    "comparatives for presentational purposes. The changes had no impact on the net cashflows from "
    "operating activities' - but its FY2021 comparative operating-activities total is stated as "
    "£(57,981)k, which does NOT match FY2021's own originally-published total of £(62,617)k (a £4,636k "
    "difference), despite the note's claim of no impact. FY2021's own originally-published figure is used "
    "in the FY2021 column here, per project convention; the discrepancy itself is flagged here rather than "
    "silently reconciled either way. All other tail-chain closing/opening balances tie exactly year to "
    "year with no gap."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Castle Trust Capital plc's own Company-only (solo) Statement of Cash Flows, £'000:\n"
    f"FY2025 (& FY2024 comparative): Castle Trust Capital plc Annual financial statements, y/e 30 Sept 2025, p.59 - {CH_FY2025_URL}\n"
    f"FY2024 (& FY2023 comparative): Castle Trust Capital plc Annual financial statements, y/e 30 Sept 2024, p.58 - {CH_FY2024_URL}\n"
    f"FY2023 (& FY2022 comparative): Castle Trust Capital plc Annual financial statements, y/e 30 Sept 2023, p.55 - {CH_FY2023_URL}\n"
    f"FY2022 (& FY2021 comparative): Castle Trust Capital plc Annual financial statements, y/e 30 Sept 2022, p.48 - {CH_FY2022_URL}\n"
    f"FY2021 (& FY2020 comparative): Castle Trust Capital plc Annual financial statements, y/e 30 Sept 2021, p.41 - {CH_FY2021_URL}\n"
    + ENTITY_NOTE
)


def p3_sources(page="6"):
    return (
        "Sources - Castle Trust Bank Pillar 3 Disclosures, 'Key Metrics for the Bank' table (Castle Trust "
        "Capital plc solo basis, not the wider CTH Group):\n"
        f"FY2025: Pillar 3 Disclosures FY ended 30 Sept 2025, p.{page} - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures FY ended 30 Sept 2024, p.{page} - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures FY ended 30 Sept 2023, p.{page} - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures FY ended 30 Sept 2022, p.{page} - {P3_2022_URL}\n"
        "FY2021: Pillar 3 Disclosures FY ended 30 Sept 2021 (pre-KM1 template - 'Appendix 4. Bank "
        f"Disclosures'), p.40-43 - {P3_2021_URL}"
    )


NOT_DISCLOSED_NOTE = "Not found in any of the 5 Pillar 3 Disclosures documents reviewed - no MREL figure or exemption statement given at any point."


bw = BankWorkbook(bank_name="Castle Trust Capital plc", years=YEARS, header_color="6A4C93")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (Company/solo basis)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 1203, "FY2024": 544, "FY2023": 10147, "FY2022": 4460, "FY2021": -2265}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 2754, "FY2024": 2464, "FY2023": 2219, "FY2022": 2040, "FY2021": 1617}),
    ("DATA", "Loss on disposal of property, plant and equipment", {"FY2025": 63}),
    ("DATA", "Write off of intangible assets", {"FY2024": 80}),
    ("DATA", "Loss on disposal of intangibles and property, plant and equipment", {"FY2022": 78, "FY2021": 78}),
    ("DATA", "Dividends received", {"FY2022": -18001, "FY2021": -18001}),
    ("DATA", "Impairment charge/(reversal) on investments in subsidiaries", {"FY2022": 18001, "FY2021": 18001}),
    ("DATA", "Share based payment expense", {"FY2025": 0, "FY2024": 1, "FY2023": 93, "FY2022": 36, "FY2021": 16}),
    ("DATA", "Net interest income", {"FY2025": -33009, "FY2024": -26408, "FY2023": -29626, "FY2022": -25436}),
    ("DATA", "Interest income - MILA", {"FY2021": -4687}),
    ("DATA", "Interest on lease liabilities", {"FY2021": 52}),
    ("DATA", "Impairment losses", {"FY2025": 8911, "FY2024": 4715, "FY2023": 3298, "FY2022": 1530, "FY2021": 1892}),
    ("DATA", "Other income on R&D tax credits", {"FY2025": -255, "FY2024": -417}),
    ("DATA", "R&D tax credits released against tax charge", {"FY2023": -120, "FY2022": -220}),
    ("DATA", "Tax charge transferred from subsidiary", {"FY2024": 0, "FY2023": -225}),
    ("DATA", "Fair value losses/(gains) on loans to customers at fair value", {"FY2025": 0, "FY2024": 319, "FY2023": 278, "FY2022": 427, "FY2021": 1032}),
    ("DATA", "Fair value (gains)/losses on amounts due to customers at fair value", {"FY2025": -4, "FY2024": 51, "FY2023": -41, "FY2022": 112, "FY2021": 158}),
    ("DATA", "Net unrealised (gain)/loss on derivative(s) assets", {"FY2025": 1753, "FY2024": 2406, "FY2023": -1225, "FY2022": -3219}),
    ("TOTAL", "Cash flows from operating activities before changes in operating assets and liabilities", {"FY2025": -18584, "FY2024": -16245, "FY2023": -15202}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "(Increase)/decrease in trade and other receivables (excluding corporation tax receivable)", {"FY2025": -258, "FY2024": 12, "FY2023": 253, "FY2022": -186, "FY2021": 201}),
    ("DATA", "Increase/(decrease) in loans to customers at amortised cost", {"FY2025": -390164, "FY2024": -107177, "FY2023": -79742, "FY2022": -47624, "FY2021": 48663}),
    ("DATA", "Increase in amounts due to customers at amortised cost (and related hedged asset)", {"FY2025": 546293, "FY2024": 139599, "FY2023": 108862, "FY2022": 168780}),
    ("DATA", "Increase in amounts due to customers at amortised cost / Borrower Loan Agreement", {"FY2021": -93538}),
    ("DATA", "Increase/(decrease) in prepayments (and related hedge liability)", {"FY2025": -177, "FY2024": -350, "FY2023": -81, "FY2022": -14, "FY2021": 466}),
    ("DATA", "Increase/(decrease) in trade and other payables (excl. corporation tax payable and lease liability)", {"FY2025": 6547, "FY2024": 1281, "FY2023": -3074, "FY2022": 772, "FY2021": -16013}),
    ("DATA", "Decrease/(increase) in loans to customers at fair value", {"FY2025": 0, "FY2024": 3764, "FY2023": -267, "FY2022": -47, "FY2021": 0}),
    ("DATA", "Decrease in amounts due to customers at fair value", {"FY2025": -71, "FY2024": -754, "FY2023": -561, "FY2022": -21}),
    ("DATA", "Increase/(decrease) in derivative financial instruments/assets", {"FY2025": -1523, "FY2024": -2605, "FY2023": 1671, "FY2022": 96}),
    ("DATA", "Increase in amounts due to customers at fair value / group companies (inter-company swap)", {"FY2021": -289}),
    ("DATA", "Increase in amounts due from credit institutions", {"FY2025": -2799, "FY2024": -8354, "FY2023": -1930}),
    ("DATA", "Increase/(decrease) in amounts due to credit institutions", {"FY2025": 119, "FY2024": -1326, "FY2023": -1160, "FY2022": 4100}),
    ("DATA", "Tax refunds", {"FY2025": 0, "FY2024": 118}),
    ("DATA", "Tax paid", {"FY2025": -1188, "FY2022": -26}),
    ("DATA", "Tax refunded/(paid)", {"FY2023": -13}),
    ("DATA", "Interest received", {"FY2025": 60879, "FY2024": 46245, "FY2023": 30986, "FY2022": 20746}),
    ("DATA", "Interest paid (excluding interest on lease liabilities and MILA loan)", {"FY2025": -64410}),
    ("DATA", "Interest paid on lease liabilities", {"FY2025": -59}),
    ("DATA", "Interest paid (including interest on lease liabilities and MILA loan)", {"FY2024": -48308, "FY2023": -26760, "FY2022": -10649}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 134605, "FY2024": 5222, "FY2023": 12982, "FY2022": 113687, "FY2021": -62617}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -1781, "FY2024": -2237, "FY2023": -2352, "FY2022": -1862, "FY2021": -1027}),
    ("DATA", "Purchase of debt instruments", {"FY2025": -19838, "FY2024": -53000}),
    ("DATA", "Proceeds from sale of debt instruments", {"FY2025": 63347, "FY2024": 29685, "FY2022": 14999}),
    ("DATA", "(Purchase)/sale of debt instruments (net, as reported)", {"FY2023": -35495}),
    ("DATA", "Sale/(purchase) of debt instruments (net, as reported)", {"FY2021": 96919}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -97, "FY2024": -123, "FY2023": -11, "FY2022": -493, "FY2021": -73}),
    ("DATA", "Disposals of property, plant and equipment", {"FY2025": 0, "FY2024": 22}),
    ("DATA", "Purchase of leased asset on transfer", {"FY2021": -17}),
    ("DATA", "Proceeds from maturities of fixed deposits", {"FY2021": 0}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2025": 41631, "FY2024": -25653, "FY2023": -37858, "FY2022": 12644, "FY2021": 95802}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Principal receipts of intercompany loans", {"FY2025": 127105, "FY2024": 35952}),
    ("DATA", "Principal repayment of intercompany loans", {"FY2025": -101088, "FY2024": -5199, "FY2023": -18021}),
    ("DATA", "Principal repayment of MILA loan", {"FY2022": -36770}),
    ("DATA", "Proceeds from issue of share capital", {"FY2021": 0}),
    ("DATA", "Interest received on MILA", {"FY2021": 4687}),
    ("DATA", "Principal (repayment)/receipt of MILA", {"FY2021": -14813}),
    ("DATA", "Lease payments of principal", {"FY2025": -411, "FY2024": -561, "FY2023": -517, "FY2022": -399, "FY2021": -293}),
    ("DATA", "Lease interest paid", {"FY2021": -52}),
    ("DATA", "Receipts from issuance of subordinated liability", {"FY2025": 8000, "FY2024": 7000}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {"FY2025": 33606, "FY2024": 37192, "FY2023": -18538, "FY2022": -37169, "FY2021": -10471}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 209842, "FY2024": 16761, "FY2023": -43414, "FY2022": 89162, "FY2021": 22714}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 117053, "FY2024": 100292, "FY2023": 143706, "FY2022": 54544, "FY2021": 31830}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 326895, "FY2024": 117053, "FY2023": 100292, "FY2022": 143706, "FY2021": 54544}),
]

bw.add_cash_flow_sheet(
    title="Castle Trust Capital plc — Statement of Cash Flows",
    subtitle="Company (solo) basis, £'000. Not the wider Castle Trust Holdings Limited Group. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=88,
    source_height=280,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets (all "Key Metrics for the Bank" - Castle Trust Capital plc solo)
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=50, source_height=170)


CET1_TIER1 = {"FY2025": 84719, "FY2024": 83107, "FY2023": 83177, "FY2022": 75267, "FY2021": 71677}
TOTAL_CAPITAL = {"FY2025": 99719, "FY2024": 90107, "FY2023": 83177, "FY2022": 75267, "FY2021": 71677}
RWA = {"FY2025": 634489, "FY2024": 499532, "FY2023": 413907, "FY2022": 357870, "FY2021": 359249}
CET1_RATIO = {"FY2025": "13.35%", "FY2024": "16.64%", "FY2023": "20.10%", "FY2022": "21.03%", "FY2021": "20.0%"}
TOTAL_CAP_RATIO = {"FY2025": "15.72%", "FY2024": "18.04%", "FY2023": "20.10%", "FY2022": "21.03%", "FY2021": "20.0%"}
LEV_EXPOSURE = {"FY2025": 1173013, "FY2024": 860147, "FY2023": 930371, "FY2022": 821174, "FY2021": 647358}
LEV_RATIO = {"FY2025": "7.22%", "FY2024": "9.66%", "FY2023": "8.94%", "FY2022": "9.17%", "FY2021": "11.1%"}
LCR_RATIO = {"FY2025": "189.07%", "FY2024": "296.84%", "FY2023": "324.90%", "FY2022": "401.68%", "FY2021": "575.71%"}
NSFR_RATIO = {"FY2025": "178.27%", "FY2024": "156.44%", "FY2023": "171.97%", "FY2022": "169.82%"}

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", CET1_TIER1)],
    p3_sources(),
    note="No AT1 instruments in issue in any year to date, so CET1 = Tier 1 capital throughout.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", CET1_RATIO)],
    p3_sources(),
    note="FY2021 sourced from the pre-KM1-template 'Appendix 4. Bank Disclosures' section of the FY2021 "
         "Pillar 3 document (own funds/RWA breakdown, not a KM1 template - this format was only introduced "
         "from 1 Jan 2022).",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", CET1_TIER1)],
    p3_sources(),
    note="= CET1 capital (no AT1 instruments in issue in any year to date).",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", CET1_RATIO)],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital", TOTAL_CAPITAL)],
    p3_sources(),
    note="Total capital exceeds Tier 1 capital from FY2024 onward (Tier 2 instruments: £7.0m FY2024, "
         "£15.0m FY2025) - no Tier 2 in issue FY2021-FY2023, when Total Capital = CET1 = Tier 1.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", TOTAL_CAP_RATIO)],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", RWA)],
    p3_sources(),
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks (£'000)", LEV_EXPOSURE),
        ("Leverage ratio excluding claims on central banks (%)", LEV_RATIO),
    ],
    p3_sources(),
    note="FY2021 figure/basis from the FY2021 Pillar 3 document's own 'Leverage Ratio' appendix table "
         "(pre-KM1 template, same underlying 'excluding claims on central banks' concept).",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value - average (£'000)",
         {"FY2025": 264609, "FY2024": 107626, "FY2023": 91141, "FY2022": 89542}),
        ("Total net cash outflows, adjusted value (£'000)",
         {"FY2025": 139955, "FY2024": 36257, "FY2023": 28052, "FY2022": 22292}),
        ("Liquidity Coverage Ratio (%)", LCR_RATIO),
    ],
    p3_sources(),
    note="FY2021's own Pillar 3 document (pre-KM1 template) discloses no LCR figure for the Bank at all - "
         "the 575.71% shown here is FY2021's comparative column as it appears in the FY2022 Pillar 3 "
         "document's KM1 table (HQLA £77,922k, net cash outflows £13,535k), the earliest source in which "
         "it's disclosed. Flagged, not a same-year original disclosure.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding (£'000)",
         {"FY2025": 1473649, "FY2024": 943517, "FY2023": 810485, "FY2022": 715551}),
        ("Total required stable funding (£'000)",
         {"FY2025": 826660, "FY2024": 603108, "FY2023": 471300, "FY2022": 421346}),
        ("Net Stable Funding Ratio (%)", NSFR_RATIO),
    ],
    p3_sources(),
    note="Not disclosed for FY2021 in any source reviewed (marked 'N/A' even in the FY2022 Pillar 3 "
         "document's FY2021 comparative column) - the UK NSFR regime only took effect from 1 Jan 2022, "
         "partway through this entity's FY2021 (y/e 30 Sept 2021).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(page="n/a"), per_note={"MREL Ratio": NOT_DISCLOSED_NOTE},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities", {"FY2025": 134605, "FY2024": 5222, "FY2023": 12982, "FY2022": 113687, "FY2021": -62617}),
        ("Net cash generated from/(used in) investing activities", {"FY2025": 41631, "FY2024": -25653, "FY2023": -37858, "FY2022": 12644, "FY2021": 95802}),
        ("Net cash generated from/(used in) financing activities", {"FY2025": 33606, "FY2024": 37192, "FY2023": -18538, "FY2022": -37169, "FY2021": -10471}),
        ("Cash and cash equivalents at end of year", {"FY2025": 326895, "FY2024": 117053, "FY2023": 100292, "FY2022": 143706, "FY2021": 54544}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Tier 1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TOTAL_CAP_RATIO),
        ("Leverage Ratio", LEV_RATIO),
        ("LCR", LCR_RATIO),
        ("NSFR", NSFR_RATIO),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. All figures are Castle Trust Capital plc's own "
         "solo ('Bank') basis, not the wider Castle Trust Holdings Limited Group.",
)

bw.save("/Users/armaan/code/katalysis/banks/CASTLE TRUST CAPITAL FINANCIALS.xlsx")
