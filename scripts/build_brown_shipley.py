import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Brown Shipley & Co. Limited (Companies House 00398426, FRN 124548), a UK
# subsidiary of Quintet Private Bank (Luxembourg), calendar fiscal year-end.
# FY2025 accounts were filed with Companies House on 26 Aug 2026 but are still
# "being processed" (no document available yet) as of this build - workbook
# therefore covers FY2021-FY2024 (4 years), not the usual 5.
YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/00398426/filing-history"
AR2024_URL = f"{CH_BASE}/MzQ3ODk2Mjk5OWFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = f"{CH_BASE}/MzQzMTg2OTM1MGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = f"{CH_BASE}/MzM5MTEwMDM3NGFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = f"{CH_BASE}/MzM0NzY3MjI5MmFkaXF6a2N4/document?format=pdf&download=0"

# Brown Shipley's OWN standalone Pillar 3 Disclosures report - found 2026-09-15
# by the maximum-effort disclosure sweep. It is not linked from any current
# page of brownshipley.com (its "Important information > Annual report" page
# lists only the TCFD report, the Quintet/PlusPlus group annual report and
# sundry policy PDFs), which is why earlier passes concluded no such document
# existed. The PDF is live and directly fetchable on the Bank's own domain.
P3_2024_URL = "https://brownshipley.com/media/o4tl2pod/pillar-3-disclosure-2024-final-draft_cleanv2.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Brown Shipley & Co. Limited (Companies House 00398426, FRN 124548) is a UK-authorised private "
    "bank, a subsidiary of Quintet Private Bank (Europe) S.A. (Luxembourg). It files full statutory accounts "
    "(income statement, statement of comprehensive income, statement of financial position, statement of changes "
    "in equity, cash flow statement, notes 1-37) under UK-adopted international accounting standards - no FRS 101/"
    "102 cash-flow exemption applies. Companies House filing history shows accounts to 31 December 2025 were "
    "filed 26 Aug 2026 but remained 'being processed' with no document available as of this build; this workbook "
    "therefore covers FY2021-FY2024 (4 years of cash flow and Pillar 3 data), not the usual 5. All Companies "
    "House-filed accounts documents for this entity are image-only PDFs (no text layer) - figures were "
    "transcribed via page-image review of each year's own filing. The Statement of Financial Position confirms "
    "Additional Tier 1 Equity Capital of £10,000k alongside CET1-eligible equity (called-up share capital + "
    "retained earnings) in every year shown - i.e. Brown Shipley's capital structure includes AT1 instruments, so "
    "unlike some smaller banks in this series CET1 capital/ratio cannot be assumed equal to Tier 1 capital. "
    "CORRECTION (2026-09-06 correctness audit, HD-065): an earlier version of this script wrongly stated that "
    "Brown Shipley's own statutory accounts do not disclose a Pillar 3-style capital template at all. In fact "
    "each year's own accounts include a 'Capital' note (Note 35 in the FY2022-FY2024 accounts; Note 36 in the "
    "FY2021 accounts, which numbers its notes one higher throughout) titled 'Unaudited Regulatory Capital at 31 "
    "December', disclosing Total Common Equity Tier One Capital, Additional Tier 1 Capital, Total Tier One "
    "Capital, Risk Exposure Amount (= Total RWAs), a Pillar 1 capital-requirement breakdown by Credit Risk and "
    "Operational Risk, and CET1/Tier 1 Capital ratios - re-verified against each year's own primary source and "
    "now populated on the CET1 Capital, Tier 1 Capital, Tier 1 Ratio, Total RWAs and RWA Breakdown sheets "
    "accordingly. What the statutory accounts alone do not disclose in any year 2021-2024 (confirmed by reading "
    "each year's own Note 35/36 'Capital' and Note 36/37 'Financial Risk Management' sections in full, not "
    "assumed): Total Capital/Total Capital Ratio, Leverage Ratio, NSFR and MREL Ratio. SECOND CORRECTION "
    "(2026-09-15, maximum-effort disclosure sweep): the earlier statement here that 'no standalone Pillar 3 "
    "disclosure document was found on Brown Shipley's own website' was wrong. Brown Shipley does publish its own "
    "entity-level Pillar 3 report, hosted on its own domain, and the 2024 edition is live and directly "
    "fetchable; it is simply unlinked from every current page of that site (the 'Important information > Annual "
    "report' page lists only the TCFD report, the Quintet/PlusPlus group annual report and policy PDFs), so site "
    "navigation alone will never reach it. That report supplies Total Capital, Total Capital Ratio, Leverage "
    "Ratio and NSFR - see those sheets. Only MREL Ratio is now 'Not publicly disclosed' in every year, and "
    "Leverage Ratio/NSFR remain blank for FY2022 and FY2021 (no Pillar 3 report of those years exists)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Brown Shipley & Co. Limited's own Cash Flow Statement, transcribed from each "
    "year's own Companies House filing (not a later year's comparative column, per this project's convention):\n"
    f"FY2024: Annual Report 2024 (filed 28 Aug 2025), p.42 (Cash Flow Statement) - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023 (filed 19 Aug 2024), p.39 (Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022 (filed 01 Sep 2023), p.38 (Cash Flow Statement) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021 (filed 04 Aug 2022), p.36 (Cash Flow Statement) - {AR2021_URL}\n"
    "Cross-checked against each figure's appearance as the following year's comparative column - all figures "
    "matched exactly except for cosmetic line-caption relabelling (e.g. FY2022's own report captions one line "
    "'Gain on deferred consideration - NWB' where FY2023's report captions the identical FY2022 comparative "
    "figure, (965), as 'Loss on deferred consideration - NWB'; and 'Proceeds on sale of Court of Protection "
    "business' in FY2022's own report vs. 'Gain on sale of Court of Protection business' for the same £567k in "
    "FY2023's report). No FY2020 comparative is shown (outside this workbook's FY2021-FY2024 window).\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Brown Shipley & Co. Limited's own Strategic Report 'Regulatory measures' KPI disclosure "
        "(narrative percentages only), transcribed from each year's own Companies House filing:\n"
        f"FY2024: Annual Report 2024, p.6 (Strategic Report, 'Regulatory measures') - {AR2024_URL}\n"
        f"FY2023: Annual Report 2023, p.6 (Strategic Report, 'Regulatory measures') - {AR2023_URL}\n"
        f"FY2022: Annual Report 2022, p.6 (Strategic Report, 'Regulatory measures' (c)) - {AR2022_URL}\n"
        f"FY2021: Annual Report 2021, p.6 (Strategic Report, 'Regulatory measures' (c)) - {AR2021_URL}\n"
        "Cross-checked against each figure's appearance as a prior-year comparative in the following year's own "
        "report - all matched exactly (e.g. FY2021 CET1 19.6%/LCR 253% as stated in both the FY2021 report itself "
        "and as the FY2021 comparative in FY2022's report), except FY2023 CET1: FY2023's own report states 22.3%, "
        "while FY2024's report states the FY2023 comparative as 22.2% (a 0.1pp discrepancy in the Bank's own "
        "filings) - FY2023's own report's 22.3% is used here, per this project's convention of preferring each "
        "year's own report over a later comparative. UPDATE (2026-09-06 correctness audit, HD-065): this same "
        "0.1pp discrepancy is also visible WITHIN FY2023's own report alone - its Strategic Report states CET1 "
        "22.3% (p.6) while its own Note 35 'Capital' table (p.70, see capital_note_sources()) states CET1 22.2% "
        "for the same FY2023 year-end - i.e. it is an internal inconsistency in the Bank's own FY2023 filing "
        "between two disclosures, not merely a between-year comparative drift. The Strategic Report's 22.3% "
        "continues to be used here for consistency with every other year's figure being sourced from the "
        "Strategic Report KPI line.\n\n"
        + ENTITY_NOTE
    )


def capital_note_sources():
    return (
        "Sources - Brown Shipley & Co. Limited's own 'Capital' note (Note 35 in the FY2022-FY2024 accounts, Note "
        "36 in the FY2021 accounts - that year's notes are numbered one higher throughout), 'Unaudited Regulatory "
        "Capital at 31 December' table, transcribed from each year's own Companies House filing:\n"
        f"FY2024: Annual Report 2024, p.73 (Note 35, 'Capital') - {AR2024_URL}\n"
        f"FY2023: Annual Report 2023, pp.69-70 (Note 35, 'Capital') - {AR2023_URL}\n"
        f"FY2022: Annual Report 2022, pp.69-70 (Note 35, 'Capital') - {AR2022_URL}\n"
        f"FY2021: Annual Report 2021, pp.69-70 (Note 36, 'Capital') - {AR2021_URL}\n"
        "Cross-checked against each figure's appearance as the following year's comparative column - all matched "
        "exactly (e.g. FY2021's own Total CET1 Capital £67,645k/Total Tier 1 Capital £77,645k/Risk Exposure "
        "Amount £344,361k/CET1 ratio 19.6%/Tier 1 ratio 22.6% all tie to FY2022's own report's FY2021 comparative "
        "column). Discovered by this correctness audit (2026-09-06, HD-065): a prior version of this script "
        "wrongly marked CET1 Capital, Tier 1 Capital, Tier 1 Ratio and Total RWAs 'Not publicly disclosed' - this "
        "note discloses all four, plus a Pillar 1 capital-requirement breakdown by Credit Risk and Operational "
        "Risk (used on the RWA Breakdown sheet - see that sheet's own note on how RWA-by-category is derived from "
        "the disclosed capital-requirement figures). This note itself discloses no Tier 2 capital instrument in "
        "any year, and none appears elsewhere in any year's accounts; the Bank's own Pillar 3 Disclosures 2024 "
        "(Template UK KM1 rows 2-3) states Total capital = Tier 1 capital, confirming Tier 2 = nil, which is "
        "what now allows the Total Capital and Total Capital Ratio sheets to be populated - see those sheets for "
        "the full derivation.\n\n"
        + ENTITY_NOTE
    )


PILLAR3_DOC_NOTE = (
    "PILLAR 3 DOCUMENT NOTE: 'Brown Shipley & Co. Limited - Pillar 3 Disclosures 2024' (38pp, prepared on a "
    "consolidated basis for the Brown Shipley group, which the report itself states is the same reporting "
    "perimeter as the Company because 'all its subsidiaries were dormant in the year') is the Bank's own "
    "entity-level Pillar 3 report - NOT a Quintet group document. It carries the full UK templates KM1 (key "
    "metrics), OV1, LR1/LR2/LR3 (leverage), LIQ1 (LCR) and LIQ2 (NSFR). Only the 2024 edition is retrievable: no "
    "2021, 2022 or 2023 edition appears anywhere on brownshipley.com or in that domain's full Wayback Machine URL "
    "index (7,140 archived URLs checked on 2026-09-15; 'pillar-3-disclosure-2024-final-draft_cleanv2.pdf' is the "
    "only Pillar 3 document of any year), nor on quintet.com (11,645 archived URLs checked - that domain holds "
    "only Quintet GROUP Pillar 3 reports, which are consolidated Luxembourg-group disclosures and are therefore "
    "not usable here; Quintet's own 2021 group Pillar 3 mentions Brown Shipley exactly once, and only in respect "
    "of large-exposure limits, with no Brown Shipley own-funds table). INTERNAL INCONSISTENCY IN THE SOURCE: the "
    "2024 report states its LCR and NSFR twice with different values - template UK KM1 (and the report's own "
    "front 'Key Prudential Risk Ratios' summary, s.1.1) give LCR 236% and NSFR 162%, while the narrative "
    "ss.11.3-11.4 and templates UK LIQ1/LIQ2 give LCR 216% and NSFR 157% off different underlying totals (KM1 "
    "row 19 total RSF 514,666 vs LIQ2 row 33 total RSF 547,524). This workbook uses the KM1 values throughout, "
    "both because KM1 is the headline prescribed key-metrics template the report's own summary table reproduces, "
    "and because the LCR already carried here for every year comes from the Strategic Report KPI line, which "
    "agrees with KM1 (236% for FY2024). The same report's KM1 row 14 prints 'Leverage ratio 0.00%', an obvious "
    "template-population error in the Bank's own file (its row 13 exposure measure is also printed in £ rather "
    "than the £000 the template declares, and its LIQ2 row 7 prints '#VALUE!'); the leverage figures used here "
    "are instead taken from template UK LR2 row 25 and s.6.1's narrative, which agree with each other and with "
    "the front summary table."
)


def pillar3_report_sources(extra=""):
    return (
        "Sources - Brown Shipley & Co. Limited's own standalone Pillar 3 Disclosures report:\n"
        f"FY2024: Pillar 3 Disclosures 2024, Appendix 15.1 (Template UK KM1 - Key metrics template), p.31, "
        f"cross-checked against s.1.1 'Key Prudential Risk Ratios' (p.4) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 2024, s.1.1 'Key Prudential Risk Ratios' prior-year comparative column "
        f"(p.4), cross-checked against Template UK LR2 row 25's own 2023 comparative (p.32) - {P3_2024_URL}\n"
        "FY2022 and FY2021: no Brown Shipley Pillar 3 report for those years could be retrieved (see Pillar 3 "
        "document note below), and the Bank's own statutory accounts for those years disclose neither metric - "
        "left blank rather than filled from a group-level source.\n"
        + (extra + "\n" if extra else "")
        + "\n" + PILLAR3_DOC_NOTE + "\n\n" + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Brown Shipley & Co. Limited", years=YEARS, year_label=YEAR_LABEL, header_color="5C4033")

# ---------------------------------------------------------------
# ST- rollout (batch ST-014): Balance Sheet, P&L, Statement of Changes in
# Equity, Asset Quality, RWA Breakdown. Sourced from the same 4 Companies
# House filings already cited above (AR20XX_URL) - each year's OWN
# originally-published report is used (project convention), not a later
# comparative column. This matters here: the FY2023 Annual Report
# "re-presents" its own FY2022 comparative column (Other receivables
# £8,615k vs FY2022's own report's £8,569k, a +£46k presentation
# reclassification that also nudges Total assets/Other liabilities by the
# same £46k) - this workbook uses each year's own originally-published
# figures throughout (matching the Cash Flow Statement sheet's existing
# convention), not the later re-presented version. FY2021's own report
# and its FY2022 comparative appearance both tie exactly (no restatement
# that year).
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - Brown Shipley & Co. Limited's own Income Statement / Statement of Financial Position / Statement "
    "of Changes in Equity, transcribed from each year's own Companies House filing (not a later year's "
    "comparative column):\n"
    f"FY2024: Annual Report 2024, pp.38,40-41 - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, pp.35,37-38 - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, pp.34,36-37 - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, pp.32,34-35 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: the FY2023 Annual Report's own FY2022 comparative column re-presents Other receivables "
    "as £8,615k (vs £8,569k in FY2022's own originally-published report) with matching +£46k nudges to Total "
    "assets (£1,507,146k re-presented vs £1,507,100k as originally published) and Other liabilities - a genuine "
    "but immaterial presentation reclassification disclosed by the Bank itself, not a restatement of profit or "
    "equity. This workbook uses each year's own originally-published figures throughout (project convention), so "
    "FY2022's column here shows £8,569k/£1,507,100k, not the later re-presented £8,615k/£1,507,146k. Separately: "
    "the FY2024 Statement of Changes in Equity's own 'Balance at end of year' total reads £132,954k, £1k more "
    "than its own four column figures actually sum to (£81,824k + £10,000k + £41,129k = £132,953k, matching the "
    "Balance Sheet's own Total Equity figure) - an immaterial £1k rounding artifact in the Bank's own source "
    "table, shown here as £132,953k for cross-sheet consistency. The Defined Benefit Pension Scheme surplus/"
    "deficit swaps sides of the Balance Sheet across the 4 years - an asset (£1,922k/£441k/£187k) FY2022-24, a "
    "liability ('Pensions', £4,423k) FY2021 - both shown as reported, not netted together. 'Current tax' and "
    "'Deferred tax' appear as separate Balance Sheet asset lines only in some years (both FY2021; Deferred tax "
    "only FY2022; neither disclosed as a distinct asset line FY2023-24) - blank cells where a year's own report "
    "doesn't show that specific line."
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2024": 292700, "FY2023": 528997, "FY2022": 456835, "FY2021": 236409}),
    ("DATA", "Loans and advances to banks", {"FY2024": 290450, "FY2023": 276949, "FY2022": 222163, "FY2021": 86610}),
    ("DATA", "Loans and advances to customers", {"FY2024": 483277, "FY2023": 554649, "FY2022": 646794, "FY2021": 565574}),
    ("DATA", "Derivative financial instruments - held for trading", {"FY2024": 3785, "FY2023": 4148, "FY2022": 5795, "FY2021": 1952}),
    ("DATA", "Investments - non-trading at fair value through profit or loss", {"FY2024": 764, "FY2023": 405, "FY2022": 359, "FY2021": 698}),
    ("DATA", "Debt securities at amortised cost", {"FY2024": 105293, "FY2023": 111833, "FY2022": 117333, "FY2021": 188307}),
    ("DATA", "Other receivables", {"FY2024": 8062, "FY2023": 11639, "FY2022": 8569, "FY2021": 12597}),
    ("DATA", "Property and equipment", {"FY2024": 9248, "FY2023": 11612, "FY2022": 14021, "FY2021": 14917}),
    ("DATA", "Goodwill and other intangible assets", {"FY2024": 22250, "FY2023": 28205, "FY2022": 34538, "FY2021": 42818}),
    ("DATA", "Investment in subsidiaries", {"FY2024": 293, "FY2023": 293, "FY2022": 293, "FY2021": 293}),
    ("DATA", "Current tax asset", {"FY2021": 385}),
    ("DATA", "Deferred tax asset", {"FY2022": 213, "FY2021": 1717}),
    ("DATA", "Defined Benefit Pension Scheme (asset)", {"FY2024": 1922, "FY2023": 441, "FY2022": 187}),
    ("TOTAL", "Total assets", {"FY2024": 1218044, "FY2023": 1529171, "FY2022": 1507100, "FY2021": 1152277}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2024": 7138, "FY2023": 9131, "FY2022": 13740, "FY2021": 4713}),
    ("DATA", "Deposits from customers", {"FY2024": 1046365, "FY2023": 1353609, "FY2022": 1321391, "FY2021": 971736}),
    ("DATA", "Derivative financial instruments - held for trading", {"FY2024": 11, "FY2023": 1417, "FY2022": 1846, "FY2021": 207}),
    ("DATA", "Other liabilities", {"FY2024": 29447, "FY2023": 34773, "FY2022": 36539, "FY2021": 37230}),
    ("DATA", "Defined Benefit Pension Scheme (liability)", {"FY2021": 4423}),
    ("DATA", "Provisions", {"FY2024": 371, "FY2023": 143, "FY2022": 2719, "FY2021": 6893}),
    ("DATA", "Current tax liability", {"FY2024": 1757, "FY2023": 929, "FY2022": 184}),
    ("DATA", "Deferred tax liability", {"FY2024": 2, "FY2023": 30}),
    ("TOTAL", "Total liabilities", {"FY2024": 1085091, "FY2023": 1400032, "FY2022": 1376419, "FY2021": 1025202}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2024": 81824, "FY2023": 81824, "FY2022": 81824, "FY2021": 81824}),
    ("DATA", "Additional Tier 1 Equity Capital", {"FY2024": 10000, "FY2023": 10000, "FY2022": 10000, "FY2021": 10000}),
    ("DATA", "Retained earnings", {"FY2024": 41129, "FY2023": 37315, "FY2022": 38857, "FY2021": 35251}),
    ("TOTAL", "Total equity", {"FY2024": 132953, "FY2023": 129139, "FY2022": 130681, "FY2021": 127075}),
    ("TOTAL", "Total liabilities and equity", {"FY2024": 1218044, "FY2023": 1529171, "FY2022": 1507100, "FY2021": 1152277}),
]

bw.add_balance_sheet_sheet(
    title="Brown Shipley & Co. Limited — Statement of Financial Position",
    subtitle="Company (entity-level) basis, £'000. FY2025 not yet available - see source note.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=68,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2024": 83170, "FY2023": 90709, "FY2022": 33998, "FY2021": 13124}),
    ("DATA", "Interest and similar expense", {"FY2024": -58552, "FY2023": -63253, "FY2022": -16047, "FY2021": -3827}),
    ("TOTAL", "Net interest income", {"FY2024": 24618, "FY2023": 27456, "FY2022": 17951, "FY2021": 9297}),
    ("DATA", "Fee and commission income", {"FY2024": 58352, "FY2023": 60023, "FY2022": 59780, "FY2021": 64976}),
    ("DATA", "Fee and commission expense", {"FY2024": -3494, "FY2023": -3136, "FY2022": -2120, "FY2021": -1824}),
    ("TOTAL", "Net fee and commission income", {"FY2024": 54858, "FY2023": 56887, "FY2022": 57660, "FY2021": 63152}),
    ("DATA", "Dividend income", {"FY2024": 7, "FY2023": 7, "FY2022": 8, "FY2021": 8}),
    ("DATA", "Net gains from financial instruments at fair value through profit or loss", {"FY2024": 4620, "FY2023": 3356, "FY2022": 7718, "FY2021": 3559}),
    ("DATA", "Net losses from financial instruments not measured at fair value through profit or loss", {"FY2021": 0}),
    ("DATA", "Other operating income", {"FY2024": 11318, "FY2023": 8017, "FY2022": 9688, "FY2021": 14866}),
    ("TOTAL", "Net operating income", {"FY2024": 95421, "FY2023": 95723, "FY2022": 93025, "FY2021": 90882}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Staff expenses", {"FY2024": -44065, "FY2023": -53830, "FY2022": -53667, "FY2021": -52755}),
    ("DATA", "General administrative expenses", {"FY2024": -33199, "FY2023": -31153, "FY2022": -27501, "FY2021": -23574}),
    ("DATA", "Depreciation of property and equipment", {"FY2024": -3563, "FY2023": -3392, "FY2022": -3123, "FY2021": -2695}),
    ("DATA", "Amortisation of intangible assets", {"FY2024": -3177, "FY2023": -3501, "FY2022": -3805, "FY2021": -3939}),
    ("DATA", "Net (increase)/decrease in provisions", {"FY2024": -361, "FY2023": 850, "FY2022": 0, "FY2021": -2516}),
    ("TOTAL", "Total operating expenses", {"FY2024": -84365, "FY2023": -91026, "FY2022": -88096, "FY2021": -85479}),
    ("DATA", "Impairment of assets", {"FY2024": -3253, "FY2023": -3474, "FY2022": -2594, "FY2021": -96}),
    ("TOTAL", "Profit before tax", {"FY2024": 7803, "FY2023": 1223, "FY2022": 2335, "FY2021": 5307}),
    ("DATA", "Income tax (charge)/credit", {"FY2024": -3719, "FY2023": -1835, "FY2022": -1224, "FY2021": -2399}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2024": 4084, "FY2023": -612, "FY2022": 1111, "FY2021": 2908}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Actuarial gain/(loss) on Defined Benefit Pension Scheme", {"FY2024": 1154, "FY2023": -63, "FY2022": 4391, "FY2021": 2131}),
    ("DATA", "Deferred tax (debit)/credit on pension scheme", {"FY2024": -288, "FY2023": 16, "FY2022": -1245, "FY2021": -75}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2024": 4950, "FY2023": -659, "FY2022": 4257, "FY2021": 4964}),
]

bw.add_income_statement_sheet(
    title="Brown Shipley & Co. Limited — Income Statement",
    subtitle="Company (entity-level) basis, £'000. FY2025 not yet available - see source note.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=78,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological)
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "At 1 January 2021", (81824, 10000, 30922, 122746)),
    ("DATA", "Additional Tier 1 Equity Capital coupon paid to parent (FY2021)", (None, None, -635, -635)),
    ("DATA", "Total comprehensive income for the year (FY2021)", (None, None, 4964, 4964)),
    ("TOTAL", "At 31 December 2021", (81824, 10000, 35251, 127075)),
    ("DATA", "Additional Tier 1 Equity Capital coupon paid to parent (FY2022)", (None, None, -651, -651)),
    ("DATA", "Total comprehensive income for the year (FY2022)", (None, None, 4257, 4257)),
    ("TOTAL", "At 31 December 2022", (81824, 10000, 38857, 130681)),
    ("DATA", "Additional Tier 1 Equity Capital coupon paid to parent (FY2023)", (None, None, -883, -883)),
    ("DATA", "Total comprehensive loss for the year (FY2023)", (None, None, -659, -659)),
    ("TOTAL", "At 31 December 2023", (81824, 10000, 37315, 129139)),
    ("DATA", "Additional Tier 1 Equity Capital coupon paid to parent (FY2024)", (None, None, -1136, -1136)),
    ("DATA", "Total comprehensive income for the year (FY2024)", (None, None, 4950, 4950)),
    ("TOTAL", "At 31 December 2024", (81824, 10000, 41129, 132953)),
]

bw.add_equity_changes_sheet(
    title="Brown Shipley & Co. Limited — Statement of Changes in Equity",
    subtitle="Company (entity-level) basis, £'000. Chronological roll-forward, oldest to newest.",
    headers=["Called up share capital", "Additional Tier 1 Equity Capital", "Retained earnings", "Total"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=58,
    source_height=380,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Net profit before tax on continuing activities", {"FY2024": 7803, "FY2023": 1223, "FY2022": 2335, "FY2021": 5307}),
    ("DATA", "Changes in operating assets", {"FY2024": 99240, "FY2023": -12578, "FY2022": -67317, "FY2021": -149872}),
    ("DATA", "Changes in operating liabilities", {"FY2024": -317156, "FY2023": 30240, "FY2022": 349131, "FY2021": 164590}),
    ("DATA", "Dividend receivable", {"FY2024": -7, "FY2023": -7, "FY2022": -8, "FY2021": -8}),
    ("DATA", "Loss/(gain) on sale of prior year acquisitions", {"FY2022": 97, "FY2021": 5}),
    ("DATA", "Profit on sale of the pensions activities", {"FY2022": -400, "FY2021": -3600}),
    ("DATA", "Loss/(gain) on deferred consideration - NWB", {"FY2024": 0, "FY2023": 1442, "FY2022": -965, "FY2021": -3003}),
    ("DATA", "Net gains from financial instruments at fair value", {"FY2024": -4620, "FY2023": -3356, "FY2022": -6993, "FY2021": -3559}),
    ("DATA", "Impairment", {"FY2024": 3253, "FY2023": 3474, "FY2022": 2594, "FY2021": 96}),
    ("DATA", "Income taxes paid", {"FY2024": -3206, "FY2023": -829, "FY2022": -393, "FY2021": -1631}),
    ("DATA", "Depreciation of property and equipment", {"FY2024": 3563, "FY2023": 3392, "FY2022": 3123, "FY2021": 2695}),
    ("DATA", "Amortisation of intangible assets", {"FY2024": 3177, "FY2023": 3501, "FY2022": 3805, "FY2021": 3939}),
    ("DATA", "Loss on disposal of property and equipment", {"FY2024": 8, "FY2023": 4, "FY2022": 8, "FY2021": 70}),
    ("DATA", "(Profit)/loss on deferred consideration - TRP", {"FY2021": -3}),
    ("DATA", "Gain on sale of non-core Affluent client book", {"FY2024": -3318}),
    ("DATA", "Proceeds on sale of Court of Protection business / pensions administration activities", {"FY2024": 802, "FY2023": 567, "FY2022": 800, "FY2021": 3200}),
    ("DATA", "Proceeds on sale of a portfolio of assets", {"FY2023": 632, "FY2022": 600}),
    ("DATA", "Changes in provisions", {"FY2024": 229, "FY2023": -2576, "FY2022": -4174, "FY2021": 1582}),
    ("DATA", "Changes in Defined Benefit Pension Scheme surplus/(deficit)", {"FY2024": -327, "FY2023": -317, "FY2022": -219, "FY2021": -1431}),
    ("TOTAL", "Net cash (used in)/from operating activities", {"FY2024": -210559, "FY2023": 24812, "FY2022": 282024, "FY2021": 18377}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Dividend received", {"FY2024": 7, "FY2023": 7, "FY2022": 8, "FY2021": 8}),
    ("DATA", "Proceeds on sale of equity investments", {"FY2022": 725}),
    ("DATA", "Deferred consideration paid on prior year acquisitions", {"FY2023": -3200, "FY2022": -106, "FY2021": -3265}),
    ("DATA", "Proceeds on sale of non-core Affluent client book", {"FY2024": 2416}),
    ("DATA", "Purchase of property and equipment (excludes leased assets)", {"FY2024": -89, "FY2023": -916, "FY2022": -1402, "FY2021": -1405}),
    ("DATA", "Purchase of intangible assets", {"FY2024": -2, "FY2023": -16, "FY2022": 0, "FY2021": -4}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2024": 2332, "FY2023": -4125, "FY2022": -775, "FY2021": -4666}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Coupon paid to shareholder of Additional Tier 1 equity capital", {"FY2024": -1136, "FY2023": -883, "FY2022": -651, "FY2021": -635}),
    ("DATA", "Repayment of principal portion of lease liabilities", {"FY2024": -2359, "FY2023": -2194, "FY2022": -2040, "FY2021": -1857}),
    ("TOTAL", "Net cash used in financing activities", {"FY2024": -3495, "FY2023": -3077, "FY2022": -2691, "FY2021": -2492}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2024": -211722, "FY2023": 17610, "FY2022": 278558, "FY2021": 11219}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2024": 586631, "FY2023": 569021, "FY2022": 290463, "FY2021": 279244}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2024": 374909, "FY2023": 586631, "FY2022": 569021, "FY2021": 290463}),
    ("SECTION", "Components of cash and cash equivalents", {}),
    ("DATA", "Cash and balances at central banks", {"FY2024": 292700, "FY2023": 528997, "FY2022": 456835, "FY2021": 236409}),
    ("DATA", "Loans and advances to banks repayable on demand and less than 3 months", {"FY2024": 89347, "FY2023": 66766, "FY2022": 125926, "FY2021": 58767}),
    ("DATA", "Deposits from banks repayable on demand and less than 3 months", {"FY2024": -7138, "FY2023": -9132, "FY2022": -13740, "FY2021": -4713}),
    ("TOTAL", "Total components of cash and cash equivalents", {"FY2024": 374909, "FY2023": 586631, "FY2022": 569021, "FY2021": 290463}),
]

bw.add_cash_flow_sheet(
    title="Brown Shipley & Co. Limited — Cash Flow Statement",
    subtitle="£'000. Company (entity-level) basis. FY2025 not yet available - see source note.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality: Loans and advances to customers by purpose, and ECL
# allowance by IFRS 9 stage - from the Bank's own Note 14 "Loans and
# advances to customers" (each year's own report). Only the ECL
# ALLOWANCE is disclosed by stage; gross exposure by stage is not
# disclosed (only a partial "Stage 2 transfers" reconciliation, not a
# full gross-by-stage table) - confirmed by reading the note in full, not
# assumed. Stage 3/NPL exposure ratios therefore cannot be derived here;
# only an overall ECL coverage ratio (total allowance / total gross
# loans) is shown.
# ---------------------------------------------------------------
AQ_ON_DEMAND = {"FY2024": 171242, "FY2023": 192821, "FY2022": 179111, "FY2021": 132746}
AQ_PERSONAL = {"FY2024": 2252, "FY2023": 845, "FY2022": 1126, "FY2021": 427}
AQ_PROPERTY = {"FY2024": 279254, "FY2023": 320684, "FY2022": 378183, "FY2021": 311293}
AQ_LOMBARD = {"FY2024": 800, "FY2023": 13043, "FY2022": 26716, "FY2021": 24868}
AQ_OTHER_TERM = {"FY2024": 31295, "FY2023": 27801, "FY2022": 61728, "FY2021": 96302}
AQ_GROSS_TOTAL = {y: AQ_ON_DEMAND[y] + AQ_PERSONAL[y] + AQ_PROPERTY[y] + AQ_LOMBARD[y] + AQ_OTHER_TERM[y] for y in YEARS}

AQ_ECL_S1 = {"FY2024": 49, "FY2023": 117, "FY2022": 55, "FY2021": 51}
AQ_ECL_S2 = {"FY2024": 102, "FY2023": 7, "FY2022": 4, "FY2021": 0}
AQ_ECL_S3 = {"FY2024": 1415, "FY2023": 421, "FY2022": 13, "FY2021": 11}
AQ_ECL_TOTAL = {y: AQ_ECL_S1[y] + AQ_ECL_S2[y] + AQ_ECL_S3[y] for y in YEARS}

AQ_NET_TOTAL = {"FY2024": 483277, "FY2023": 554649, "FY2022": 646794, "FY2021": 565574}
AQ_COVERAGE = {y: f"{AQ_ECL_TOTAL[y] / AQ_GROSS_TOTAL[y] * 100:.3f}%" for y in YEARS}
AQ_STAGE3_SHARE_OF_ECL = {y: f"{AQ_ECL_S3[y] / AQ_ECL_TOTAL[y] * 100:.1f}%" for y in YEARS}

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, gross, by purpose", {}),
    ("DATA", "On demand and short notice facilities", AQ_ON_DEMAND),
    ("DATA", "Credit for personal consumption", AQ_PERSONAL),
    ("DATA", "Lending for property purchase or transformation", AQ_PROPERTY),
    ("DATA", "Loans secured on investment portfolios (Lombard loans)", AQ_LOMBARD),
    ("DATA", "Other term loans", AQ_OTHER_TERM),
    ("TOTAL", "Total gross loans and advances to customers", AQ_GROSS_TOTAL),
    ("SECTION", "Expected credit loss (ECL) allowance, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 allowance", {y: -v for y, v in AQ_ECL_S1.items()}),
    ("DATA", "Stage 2 allowance", {y: -v for y, v in AQ_ECL_S2.items()}),
    ("DATA", "Stage 3 allowance", {y: -v for y, v in AQ_ECL_S3.items()}),
    ("TOTAL", "Total ECL allowance", {y: -v for y, v in AQ_ECL_TOTAL.items()}),
    ("TOTAL", "Net loans and advances to customers", AQ_NET_TOTAL),
    ("SECTION", "Ratios", {}),
    ("DATA", "Overall ECL coverage ratio (total allowance / total gross loans)", AQ_COVERAGE),
    ("DATA", "Stage 3 allowance as % of total ECL allowance", AQ_STAGE3_SHARE_OF_ECL),
]

bw.add_asset_quality_sheet(
    title="Brown Shipley & Co. Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Loans and advances to customers, £'000. Company (entity-level) basis.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Brown Shipley & Co. Limited's own Note 14 'Loans and advances to customers' (gross by "
        "purpose, ECL allowance by IFRS 9 stage), transcribed from each year's own Companies House filing:\n"
        f"FY2024: Annual Report 2024, p.57 - {AR2024_URL}\n"
        f"FY2023: Annual Report 2023 (comparative column cross-checked against FY2024's own note) - {AR2023_URL}\n"
        f"FY2022: Annual Report 2022, p.53 - {AR2022_URL}\n"
        f"FY2021: Annual Report 2021 (comparative column cross-checked against FY2022's own note) - {AR2021_URL}\n\n"
        "Note: only the ECL ALLOWANCE is disclosed by IFRS 9 stage - the Bank's own note analyses gross exposure "
        "by loan purpose (shown above) and separately discloses a partial 'Stage 2 transfers' reconciliation, but "
        "never a full gross-exposure-by-stage table for all three stages - confirmed by reading the note in full, "
        "not assumed. Stage 3/NPL exposure ratios (Stage 3 gross / total gross) therefore cannot be derived here; "
        "only the ratios shown above (overall ECL coverage, and Stage 3's share of the total allowance) are "
        "calculable from what's disclosed. The FY2022 gross total (£646,864k) is £2k above the Bank's own "
        "disclosed net-of-ECL figure plus ECL allowance (£646,792k) - an immaterial rounding gap already present "
        "in the Bank's own source tables, not a transcription error (cross-checked against the Balance Sheet's "
        "own Loans and advances to customers figure of £646,794k, which the Note 14 net total matches exactly).\n\n"
        + ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=150)


CET1_RATIO = {"FY2024": "21.6%", "FY2023": "22.3%", "FY2022": "20.3%", "FY2021": "19.6%"}
LCR_RATIO = {"FY2024": "236%", "FY2023": "274%", "FY2022": "218%", "FY2021": "253%"}

# Disclosed via each year's own "Capital" note (Note 35, Note 36 for FY2021) - see
# capital_note_sources(). Found by the 2026-09-06 correctness audit (HD-065); a
# prior version of this script wrongly marked these "Not publicly disclosed".
CET1_CAPITAL = {"FY2024": 94885, "FY2023": 90201, "FY2022": 84594, "FY2021": 67645}
TIER1_CAPITAL = {"FY2024": 104885, "FY2023": 100201, "FY2022": 94594, "FY2021": 77645}
TIER1_RATIO = {"FY2024": "23.9%", "FY2023": "24.7%", "FY2022": "22.7%", "FY2021": "22.6%"}
TOTAL_RWAS = {"FY2024": 439621, "FY2023": 405524, "FY2022": 417077, "FY2021": 344361}

# Total Capital / Total Capital Ratio - opened 2026-09-15 by the maximum-effort
# disclosure sweep, which located Brown Shipley's own Pillar 3 Disclosures 2024
# (P3_2024_URL). Its Template UK KM1 prints row 2 "Tier 1 capital" and row 3
# "Total capital" as the SAME figure (105, in £m - that template's own rows are
# in £m despite its £000 header, since its row 4 RWA 439,621 is in £000 and ties
# exactly to the FY2024 accounts' Risk Exposure Amount), and row 6 "Tier 1 ratio"
# and row 7 "Total capital ratio" as the same 23.86%. That is the Bank stating
# for itself that it holds no Tier 2 capital - the exact confirmation the earlier
# version of this script said was missing, and which it (correctly) declined to
# assume. FY2021-FY2023 are therefore derived, not assumed: each year's own
# "Capital" note table runs share capital -> reserves -> deductions -> Total CET1
# -> Additional Tier 1 -> Total Tier One Capital and then stops, with no Tier 2
# row and no "total regulatory capital" row, and no year's Statement of Financial
# Position carries a subordinated-liabilities line. With Tier 2 evidenced as nil
# on the same capital structure (£81,824k permanent share capital + reserves +
# an unchanged £10,000k AT1) in all four years, Total Capital = Total Tier 1
# Capital and Total Capital Ratio = Tier 1 Capital ratio throughout.
TOTAL_CAPITAL = {"FY2024": 104885, "FY2023": 100201, "FY2022": 94594, "FY2021": 77645}
TOTAL_CAPITAL_RATIO = {"FY2024": "23.86%", "FY2023": "24.7%", "FY2022": "22.7%", "FY2021": "22.6%"}

# Leverage Ratio and NSFR - FY2024 and FY2023 only, from the Pillar 3 2024
# report (the Bank's statutory accounts disclose neither in any year, which is
# why FY2022 and FY2021 stay blank).
LEVERAGE_RATIO = {"FY2024": "11.23%", "FY2023": "9.96%"}
NSFR_RATIO = {"FY2024": "162%", "FY2023": "181%"}

# Pillar 1 CAPITAL REQUIREMENT by risk type, as literally disclosed (not RWA itself -
# see the RWA Breakdown sheet's own note for how RWA-by-category is derived from these).
RWA_CREDIT_RISK_CAPREQ = {"FY2024": 24024, "FY2023": 21885, "FY2022": 23868, "FY2021": 18347}
RWA_OPERATIONAL_RISK_CAPREQ = {"FY2024": 11145, "FY2023": 10557, "FY2022": 9498, "FY2021": 9202}
RWA_CREDIT_RISK = {y: round(RWA_CREDIT_RISK_CAPREQ[y] * 12.5) for y in YEARS}
RWA_OPERATIONAL_RISK = {y: round(RWA_OPERATIONAL_RISK_CAPREQ[y] * 12.5) for y in YEARS}

NOT_DISCLOSED_NOTE = (
    "Brown Shipley's own statutory accounts do not disclose this metric in any year 2021-2024 (see Entity note "
    "on the Cash Flow Statement sheet)."
)

metric(
    "CET1 Capital", "£'000",
    [("Total Common Equity Tier 1 (CET1) Capital", CET1_CAPITAL)],
    capital_note_sources(),
)

metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CET1_RATIO)], p3_sources())

metric(
    "Tier 1 Capital", "£'000",
    [("Total Tier 1 Capital (CET1 + Additional Tier 1)", TIER1_CAPITAL)],
    capital_note_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 Capital ratio", TIER1_RATIO)],
    capital_note_sources(),
)

TOTAL_CAPITAL_SOURCES = (
    "Sources - FY2024 as disclosed by Brown Shipley & Co. Limited's own Pillar 3 report; FY2021-FY2023 derived "
    "from the Bank's own 'Capital' note on the Tier 2 = nil finding that same Pillar 3 report establishes:\n"
    f"FY2024: Pillar 3 Disclosures 2024, Appendix 15.1, Template UK KM1 rows 2-3 and 6-7 (p.31) - Tier 1 capital "
    f"and Total capital are printed as the same amount, and Tier 1 ratio and Total capital ratio as the same "
    f"23.86% - {P3_2024_URL}\n"
    f"FY2023: Annual Report 2023, p.71 (Note 35, 'Capital', 'Unaudited Regulatory Capital at 31 December'): "
    f"Total Tier One Capital £100,201k, Tier 1 Capital ratio 24.7%, no Tier 2 row - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022 (Note 35, 'Capital'): Total Tier One Capital £94,594k, Tier 1 Capital ratio "
    f"22.7%, no Tier 2 row - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, p.71 (Note 36, 'Capital'): Total Tier One Capital £77,645k, Tier 1 Capital "
    f"ratio 22.6%, no Tier 2 row - {AR2021_URL}\n"
    "DERIVATION NOTE for FY2021-FY2023: these are derived, not assumed. Total Capital = CET1 + Additional Tier 1 "
    "+ Tier 2. The Bank's own FY2024 Pillar 3 KM1 states Total capital = Tier 1 capital (and Total capital ratio "
    "= Tier 1 ratio), i.e. Tier 2 = nil on this capital structure. That structure is unchanged across the whole "
    "window - permanent share capital £81,824k in every year, an unchanged £10,000k Additional Tier 1 instrument "
    "in every year, and no subordinated-liabilities line anywhere on any year's Statement of Financial Position - "
    "and each year's own 'Capital' note table ends at 'Total Tier One Capital' with no Tier 2 row and no separate "
    "'total regulatory capital' row. A prior version of this script marked all four years 'Not publicly "
    "disclosed' precisely because the Bank had not itself stated the Tier 2 = nil identity; the FY2024 Pillar 3 "
    "report, located on 2026-09-15, is that statement.\n\n"
    + PILLAR3_DOC_NOTE + "\n\n" + ENTITY_NOTE
)

metric(
    "Total Capital", "£'000",
    [("Total Capital (CET1 + Additional Tier 1; Tier 2 = nil)", TOTAL_CAPITAL)],
    TOTAL_CAPITAL_SOURCES,
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total Capital ratio", TOTAL_CAPITAL_RATIO)],
    TOTAL_CAPITAL_SOURCES,
)

metric(
    "Total RWAs", "£'000",
    [("Total Risk Exposure Amount (RWAs)", TOTAL_RWAS)],
    capital_note_sources(),
)

bw.add_rwa_breakdown_sheet(
    title="Brown Shipley & Co. Limited — RWA Breakdown",
    subtitle="£'000. Company (entity-level) basis. RWA by category derived - see note below.",
    rows=[
        ("SECTION", "RWA by risk category (derived)", {}),
        ("DATA", "Credit Risk", RWA_CREDIT_RISK),
        ("DATA", "Operational Risk", RWA_OPERATIONAL_RISK),
        ("TOTAL", "Total RWAs (as disclosed - Risk Exposure Amount)", TOTAL_RWAS),
    ],
    sources_text=capital_note_sources() + "\n\nDERIVATION NOTE: the Bank's own 'Capital' note discloses a Pillar "
                 "1 CAPITAL REQUIREMENT by risk type (Credit Risk, Operational Risk), not RWA by category "
                 "directly. Under the standardised approach the Pillar 1 capital requirement is exactly 8% of "
                 "RWA (confirmed here: each year's own disclosed 'Pillar 1 Capital Requirement' divided by its "
                 "own disclosed 'Risk Exposure Amount' equals 8.0000% in every year 2021-2024), so RWA by "
                 "category above is each risk type's own disclosed capital requirement multiplied by 12.5 (i.e. "
                 "divided by 8%). This grosses back up to the Bank's own disclosed Total RWAs (Risk Exposure "
                 "Amount) within immaterial rounding (largest gap: £8.5k on a ~£440m total, FY2024) in every "
                 "year - cross-checked, not assumed.",
    first_col_width=54,
    source_height=260,
)

metric(
    "Leverage Ratio", "%",
    [("UK leverage ratio (excluding claims on central banks)", LEVERAGE_RATIO)],
    pillar3_report_sources(
        "FY2024 11.23% and FY2023 9.96% are template UK LR2 row 25 ('Leverage ratio excluding claims on central "
        "banks'), which agrees with s.6.1's narrative ('Brown Shipley's leverage ratio stands at 11.23% as at 31 "
        "December 2024') and with the front summary table's rounded 11.2%/10.0%. The same report also discloses "
        "row UK-25c 'Leverage ratio including claims on central banks' at 8.55% (2023: 6.53%); the excluding-"
        "central-banks measure is the UK's binding definition and is the one used here. The Bank's statutory "
        "accounts disclose no leverage ratio in any year - each year's own 'Capital' note and 'Financial Risk "
        "Management' note were read in full and neither mentions one."),
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", LCR_RATIO)],
    p3_sources(),
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", NSFR_RATIO)],
    pillar3_report_sources(
        "FY2024 162% and FY2023 181% are the report's own front summary table (s.1.1) figures, which agree with "
        "template UK KM1 row 20 (162%) and with KM1's own rows 18-19 (available stable funding 832,003 / required "
        "stable funding 514,666 = 161.7%). See the inconsistency paragraph below on the 157% that the same "
        "report's narrative s.11.4 and template UK LIQ2 row 34 print instead. The Bank's statutory accounts "
        "disclose no NSFR in any year - each year's own 'Capital' and 'Financial Risk Management'/'Liquidity "
        "risk' notes were read in full and LCR is the only liquidity metric given. FY2021 additionally predates "
        "the UK NSFR requirement, which became binding on 1 January 2022 (PRA PS17/21)."),
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    capital_note_sources(),
    per_note={
        "MREL Ratio": NOT_DISCLOSED_NOTE + " Confirmed by reading each year's own 'Capital' note in full, and "
                      "the FY2024 Pillar 3 report in full - no MREL requirement or ratio is mentioned in either.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2024": 1218044, "FY2023": 1529171, "FY2022": 1507100, "FY2021": 1152277}),
        ("Loans and advances to customers", {"FY2024": 483277, "FY2023": 554649, "FY2022": 646794, "FY2021": 565574}),
        ("Deposits from customers", {"FY2024": 1046365, "FY2023": 1353609, "FY2022": 1321391, "FY2021": 971736}),
        ("Total equity", {"FY2024": 132953, "FY2023": 129139, "FY2022": 130681, "FY2021": 127075}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", {"FY2024": 95421, "FY2023": 95723, "FY2022": 93025, "FY2021": 90882}),
        ("Total operating expenses", {"FY2024": -84365, "FY2023": -91026, "FY2022": -88096, "FY2021": -85479}),
        ("Profit/(loss) for the year", {"FY2024": 4084, "FY2023": -612, "FY2022": 1111, "FY2021": 2908}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2024": 129139, "FY2023": 130681, "FY2022": 127075, "FY2021": 122746}),
        ("Total comprehensive income/(loss) for the year", {"FY2024": 4950, "FY2023": -659, "FY2022": 4257, "FY2021": 4964}),
        ("AT1 coupon paid, net", {"FY2024": -1136, "FY2023": -883, "FY2022": -651, "FY2021": -635}),
        ("Closing equity", {"FY2024": 132953, "FY2023": 129139, "FY2022": 130681, "FY2021": 127075}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash (used in)/from operating activities", {"FY2024": -210559, "FY2023": 24812, "FY2022": 282024, "FY2021": 18377}),
        ("Net cash from/(used in) investing activities", {"FY2024": 2332, "FY2023": -4125, "FY2022": -775, "FY2021": -4666}),
        ("Net cash used in financing activities", {"FY2024": -3495, "FY2023": -3077, "FY2022": -2691, "FY2021": -2492}),
        ("Cash and cash equivalents at end of year", {"FY2024": 374909, "FY2023": 586631, "FY2022": 569021, "FY2021": 290463}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Tier 1 Ratio", TIER1_RATIO),
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR_RATIO),
        ("NSFR", NSFR_RATIO),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. This workbook covers FY2021-FY2024 (4 years, not the "
         "usual 5) since Brown Shipley's FY2025 accounts were still 'being processed' at Companies House as of "
         "this build. CET1 Ratio, Tier 1 Ratio, CET1 Capital, Tier 1 Capital, Total RWAs and LCR are all "
         "disclosed by Brown Shipley's own statutory accounts (the CET1/Tier 1 figures via each year's own "
         "'Capital' note, re-confirmed by the 2026-09-06 correctness audit, HD-065). UPDATE (2026-09-15 "
         "maximum-effort disclosure sweep): Brown Shipley's own standalone 'Pillar 3 Disclosures 2024' report "
         "was located on the Bank's own domain - it is not linked from any current page of that site, which is "
         "why earlier passes concluded it did not exist. It supplies Total Capital and Total Capital Ratio for "
         "FY2024 directly (and establishes Tier 2 = nil, from which FY2021-FY2023 follow), plus Leverage Ratio "
         "and NSFR for FY2024 and FY2023. Leverage Ratio and NSFR remain blank for FY2022 and FY2021 - no Pillar "
         "3 report of those years exists on either brownshipley.com or quintet.com, and the statutory accounts "
         "disclose neither metric. MREL Ratio is not disclosed by this entity in any year. See each metric "
         "sheet for detail.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BROWN SHIPLEY FINANCIALS.xlsx")
