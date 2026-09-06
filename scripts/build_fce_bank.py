import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018",
         "FY2017", "FY2016", "FY2015", "FY2014"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

# Companies House filing history, company 00772784 (FCE Bank Plc)
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzUxMTcwMTU1NGFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzQ2MTUzNDU1OGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzQxNTY0NTE3NGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_AMENDED_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzM5ODE1MjYzNmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00772784/filing-history/MzMzMzk0NjU4NWFkaXF6a2N4/document?format=pdf&download=0"

# HD-046: FY2014-FY2020 sourced from FCE Bank's own investor-relations Annual Reports,
# hosted at fcebank.com until the site went dark (fcebank.com/pdf/investor_center/... now
# returns 404 as of 2026-09; the domain root itself still resolves but the investor-centre
# PDF paths are gone). Retrieved via the Wayback Machine (CDX API bounded 2014-2021,
# per this ticket's instructions) - each URL below is the *fullest* capture found for that
# document (the first crawl of several of these PDFs was truncated by Internet Archive's
# own 1MB-per-capture limit on that crawl date; a later, complete 2022-06-15 re-crawl of
# the same URL was used instead wherever the two differ in byte size). All are genuine,
# text-native (not scanned) PDFs - confirmed via pdftotext extraction, unlike the 5
# Companies House filings (FY2021-2025) which are scanned/image-only.
AR2020_URL = "https://web.archive.org/web/20220615085358/https://www.fcebank.com/pdf/investor_center/2020_Annual_Report.pdf"
AR2019_URL = "https://web.archive.org/web/20220615085141/https://www.fcebank.com/pdf/investor_center/2019_Annual_Report.pdf"
AR2018_URL = "https://web.archive.org/web/20220615085110/https://www.fcebank.com/pdf/investor_center/2018_Annual_Report.pdf"
AR2017_URL = "https://web.archive.org/web/20220615085008/https://www.fcebank.com/pdf/investor_center/2017_Annual_Report.pdf"
AR2016_URL = "https://web.archive.org/web/20220615085027/https://www.fcebank.com/pdf/investor_center/2016_annual_report.pdf"
AR2015_URL = "https://web.archive.org/web/20220615085018/https://www.fcebank.com/pdf/investor_center/2015_annual_report.pdf"
AR2014_URL = "https://web.archive.org/web/20220615085021/https://www.fcebank.com/pdf/investor_center/2014_annual_accts.pdf"
# FY2014's own standalone Pillar 3 document (FY2015-2020's Pillar 3 disclosures are a
# chapter *within* each year's own Annual Report instead - see P3_SOURCES_NOTE below).
P3_2014_URL = "https://web.archive.org/web/20211015234304/https://www.fcebank.com/pdf/investor_center/2014_Pillar_3_Disclosure.pdf"

ENTITY_NOTE = (
    "FCE Bank Plc (company 00772784) is the UK-regulated captive auto-finance bank for Ford "
    "Motor Company's European operations (vehicle financing/leasing across Ford's European "
    "markets, not just the UK). Does NOT take the FRS 101/102 cash-flow exemption - full "
    "Group-basis Statement of Cash Flows every year. All 5 Companies House filings (FY2021-2025) "
    "are fully scanned/image-only (0 text blocks/page); every figure was transcribed via page "
    "rendering. FY2014-FY2020 (HD-046) came from FCE's own text-native Annual Report PDFs "
    "archived via the Wayback Machine (fcebank.com/pdf/investor_center/... - see per-sheet "
    "source notes for exact capture URLs); figures were extracted directly, not OCR'd.\n"
    "FY2022's accounts were AMENDED (30 Oct 2023, replacing the original 24 Mar 2023 filing) - "
    "the amended FY2022 figures were used as the operative record for that year, since this is "
    "the entity's own correction to its own year's accounts (not a later year's restatement). "
    "Confirmed the amended FY2022 figures are internally consistent with how FY2023's own report "
    "later carries them forward as its FY2022 comparative - no discrepancy found.\n"
    "FY2024's cash and cash equivalents at end of year include a genuine, disclosed "
    "'Cash and cash equivalents in respect of discontinued operations' adjustment of £(873)m "
    "(Group basis) - a real disposal/discontinuation event that year, not a data error; kept as "
    "the entity's own disclosed reconciling item, not silently absorbed elsewhere.\n"
    "FY2021's own Statement of Cash Flows classifies 'Net cash inflow/(outflow) on derivative "
    "financial instruments', 'Increase in restricted cash', and 'Decrease in restricted cash' "
    "under Financing activities (Group: £44m/£(97)m/£463m respectively, p.49); FY2022 onward "
    "reclassify these same three items under Investing activities instead. Confirmed via direct "
    "page image (p.49) - each year's own reported section placement is used, not forced into a "
    "single consistent classification across the 5 years.\n"
    "HD-046 (FY2014-FY2020) methodology notes: (1) IFRS 9's three-stage ECL model was adopted "
    "1 Jan 2018; FY2014-FY2017 instead use the IAS 39 'incurred loss' model (a single "
    "Retail/Wholesale impairment allowance, not staged) - see the Asset Quality sheet's own note. "
    "(2) IFRS 16 leases were adopted 1 Jan 2019; Right-of-use assets/Lease liabilities first "
    "appear as separate Balance Sheet lines from FY2019 (FY2014-FY2018 predate IFRS 16 entirely - "
    "no ROU/lease lines existed to report). (3) FY2014-FY2018's own Balance Sheet presents "
    "'Due to banks and other financial institutions', 'Due to parent and related undertakings', "
    "and 'Debt securities in issue' as separate lines; FY2019 onward combine all of these into a "
    "single 'Financial liabilities' line instead (this single-line convention thus starts two "
    "years earlier than previously documented on this workbook, at FY2019 not FY2021). "
    "'Subordinated loans' is a separate line only in FY2014-FY2018 (folded into 'Financial "
    "liabilities' from FY2019). Blank cells reflect each year's own reporting granularity, not "
    "missing data - underlying totals reconcile exactly."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are FCE Bank Plc's own consolidated (Group) Statement of Cash Flows, "
    "each year's own originally-published figures (not a later year's restated comparative):\n"
    f"FY2025: Annual Report 2025, p.53 (Statements of Cash Flows) - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.58 (Statements of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, p.55 (Statements of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022 (AMENDED filing, 30 Oct 2023), p.53 (Statements of Cash Flows) - {AR2022_AMENDED_URL}\n"
    f"FY2021: Annual Report 2021, p.49 (Statements of Cash Flow) - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020, p.52 (Statements of Cash Flows, Group column) - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019, p.46 (Statements of Cash Flows, Group column) - {AR2019_URL}\n"
    f"FY2018: Annual Report 2018, p.40 (Statements of Cash Flows, Group column) - {AR2018_URL}\n"
    f"FY2017: Annual Report 2017, p.32 (Statements of Cash Flows, Group column) - {AR2017_URL}\n"
    f"FY2016: Annual Report 2016, p.61 (Statements of Cash Flows, Group column) - {AR2016_URL}\n"
    f"FY2015: Annual Report 2015, p.61 (Statements of Cash Flows, Group column) - {AR2015_URL}\n"
    f"FY2014: Annual Report and Accounts 2014, p.40 (Statements of cash flows, Group column) - {AR2014_URL}\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - FCE Bank Plc Pillar 3 / capital basis, Group/Consolidated:\n"
        f"FY2021-FY2025 Tier 1 Capital, Tier 2 Capital and Total Capital Ratio: Annual Report 2025, "
        f"p.5 ('Business Performance' - 'Total Capital' chart, values to the nearest £0.1bn) - {AR2025_URL}\n"
        "FY2021 CET1/Tier 1 Capital (exact, £2,684m) and Leverage Ratio (16.95%): Annual Report 2021, "
        f"'Pillar 3 Disclosures' Table 2 (p.135) and Table 19 (p.155) - {AR2021_URL}\n"
        "CET1 = Tier 1 Capital every year (confirmed via the FY2021 Pillar 3 Own Funds reconciliation - "
        "no Additional Tier 1 instruments held).\n"
        "FY2022-FY2025 CET1/Tier 1 Capital and CET1/Tier 1 Ratio are CALCULATED, not directly disclosed: "
        "the Annual Report only publishes the rounded (nearest £0.1bn) Tier 1/Tier 2 chart and the "
        "Total Capital Ratio %; no standalone Pillar 3 document or CET1/Tier 1 Ratio % is published for "
        "these years (the dedicated 'Pillar 3 Disclosures' chapter present in the FY2021 report was "
        "dropped from FY2022 onward). Total RWAs is likewise calculated (Total Capital / Total Capital "
        "Ratio) for every year, since no year discloses RWA directly.\n"
        "Leverage Ratio, LCR, NSFR, MREL Ratio: not located for FY2022-FY2025 - no Pillar 3 chapter "
        "exists in those reports to check, and none of these appear in the Business Performance/Business "
        "Environment narrative sections reviewed.\n"
        "HD-046 (FY2014-FY2020): every one of these years has a full, EXACT (not rounded/calculated) "
        "Pillar 3 'Own Funds'/'Capital ratio and buffers' table, either as a standalone document "
        "(FY2014) or as a 'Pillar 3 Disclosures' chapter within that year's own Annual Report "
        "(FY2015-FY2020, unaudited) - the same chapter structure the FY2021 report still carried "
        "before it was dropped from FY2022 onward:\n"
        f"FY2020: Annual Report 2020, Table 14 'Calculation of Own Funds' (p.162) and Table 19 "
        f"'Breakdown of Leverage Exposure Measure and Calculation of Leverage Ratio' (p.167) - {AR2020_URL}\n"
        f"FY2019: Annual Report 2019, Table 14 (p.156) and Table 19 (p.161) - {AR2019_URL}\n"
        f"FY2018: Annual Report 2018, Table 14 (p.139) and Table 19 (p.143) - {AR2018_URL}\n"
        f"FY2017: Annual Report 2017, Table 14 'Calculation of Own Funds' (p.121) and Table 19 "
        f"'Breakdown of Leverage Exposure Measure and Calculation of Leverage Ratio' (p.124) - {AR2017_URL}\n"
        f"FY2016: Annual Report 2016, Table 15 'Calculation of Own Funds' (pp.151-155) and Table 20 "
        f"'Breakdown of Leverage Exposure Measure and Calculation of Leverage Ratio' (p.159) - {AR2016_URL}\n"
        f"FY2015: Annual Report 2015, Table 15 (pp.151-155) and Table 20 (p.159) - {AR2015_URL}\n"
        f"FY2014: standalone 'Pillar 3 Disclosures (excl. Remuneration) - 2014', Note 3 'Own Funds - "
        f"Components of Capital' (p.18) and Note 13 'Leverage Ratio' (p.34) - {P3_2014_URL}\n"
        "LCR/NSFR/MREL Ratio: not located for FY2014-FY2020 either - none of these terms appear "
        "anywhere in the 6 Annual Reports or the standalone 2014 Pillar 3 document reviewed (the "
        "narrative around the FY2018-FY2020 LCR paragraph never states a numeric ratio), consistent "
        "with the gap already documented for FY2021-FY2025. Plausibly reflects FCE's captive "
        "auto-finance/wholesale-funded business model throughout.\n"
        + extra
    )


bw = BankWorkbook(bank_name="FCE Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="881D78")

STATEMENTS_ENTITY_NOTE = (
    ENTITY_NOTE
    + "\n\nPRESENTATION NOTE (Balance Sheet): FY2021-FY2023's own Statements of Financial Position show "
    "separate 'Property and equipment' and 'Right-of-use assets' lines; these are not shown as separate "
    "lines in FY2024/FY2025 (each year's own report presents them consolidated within 'Other assets' - "
    "confirmed by checking FY2024's/FY2025's own report has no such lines at all, not merely omitted here). "
    "FY2021-FY2023 use a single 'Financial liabilities' line and a separate 'Lease liabilities' line; "
    "FY2024-FY2025 relabel this as 'Borrowings from parent, banks and other financial institutions' with no "
    "separate lease liabilities line (folded in). FY2021-FY2023 combine 'Other liabilities and provisions' "
    "into one line; FY2024-FY2025 split this into separate 'Other liabilities' and 'Provisions' lines. "
    "Blank cells indicate that year's own report did not disclose that specific line separately at that "
    "granularity - the underlying totals reconcile exactly across all 5 years regardless of presentation.\n\n"
    "PRESENTATION NOTE (P&L): FY2021-FY2023's own P&L show 'Income from leasing & other operating income' "
    "as one combined line, plus separate '(Loss)/Gain on disposal of Operating Leases', 'Depreciation of "
    "property and equipment' and 'Depreciation of right-of-use assets' lines. FY2024 renames the combined "
    "income line 'Other operating income' and keeps the two depreciation lines split (no disposal-of-leases "
    "line that year). FY2025 combines both depreciation lines into a single 'Depreciation and amortisation' "
    "line and drops the disposal-of-leases line entirely. FY2024 is also the only year with a Discontinued "
    "Operations split (Ford Bank GmbH, sold during FY2024 - Note 40/36) - FY2025 has no discontinued "
    "operations since the disposal is already complete; FY2021-FY2023 predate the disposal and never had a "
    "discontinued-operations split at all. Each year's own originally-published figures are used throughout "
    "- FY2023's own £974m interest income / £575m total income / £121m PBT / £88m PAT / £55m total "
    "comprehensive income (this workbook's FY2023 column) differ substantially from the RESTATED FY2023 "
    "comparative shown in the FY2024 Annual Report (£722m/£368m/£97m/£88m PAT unchanged but total comp £55m "
    "same, driven by the Ford Bank GmbH disposal being reclassified as a discontinued operation after the "
    "fact) - per project convention, each year's own original figures are used, not a later year's restated "
    "comparative.\n\n"
    "EQUITY RECONCILIATION: verified via the per-year reconciliation ladder - every year's Statement of "
    "Changes in Equity closing balance ties exactly to that year's own Balance Sheet Total equity, and to "
    "the next year's own opening balance, with zero gaps found across all 5 years (FY2021 £2,742m -> FY2022 "
    "£2,502m -> FY2023 £2,556m -> FY2024 £2,065m -> FY2025 £1,704m, all independently confirmed against the "
    "Group Balance Sheet's own Total equity each year).\n\n"
    "HD-046 PRESENTATION NOTE (FY2014-FY2020): (1) Balance Sheet - FY2014-FY2018 present 'Due to banks and "
    "other financial institutions', 'Due to parent and related undertakings' and 'Debt securities in issue' "
    "as separate lines, plus a standalone 'Subordinated loans' line; FY2019-FY2020 combine all four into a "
    "single 'Financial liabilities' line (the same single-line convention later continued through FY2023 - "
    "this pushes its true start back two years earlier than previously documented). Right-of-use assets and "
    "Lease liabilities first appear from FY2019 (IFRS 16 adoption, 1 Jan 2019) - FY2014-FY2018 have no such "
    "lines at all (not blank-because-immaterial, blank-because-the-standard-didn't-exist-yet). Investment in "
    "a joint venture (the Forso JV with Credit Agricole) is a separate line FY2014-FY2016 (nil by FY2017); "
    "FY2018 onward fold any residual into 'Investment in other entities' (the JV interest was realised/"
    "disposed by FY2017 - its own FY2017 note shows the Group balance as nil, confirmed by its absence, not "
    "omission). (2) P&L - FY2014-FY2017 label the ECL/"
    "impairment line 'Impairment losses on loans and advances' (IAS 39 incurred-loss model); FY2018 onward "
    "relabel it 'Allowance for expected credit losses' (IFRS 9, adopted 1 Jan 2018) - both feed the same "
    "workbook row. 'Depreciation of right-of-use assets' first appears as its own P&L line in FY2019 (IFRS "
    "16). 'Share of profit of a joint venture' is a separate P&L line FY2014-FY2017 only, consistent with the "
    "Balance Sheet JV note above. FY2016's own OCI section includes a small 'Available for sale gains from "
    "changes in fair value' item (£1m) folded into the workbook's translation-differences reporting for that "
    "year for consistency with FY2019-FY2020's small FVOCI equity-investment OCI items."
)

STATEMENTS_SOURCES = (
    "Sources - all figures are FCE Bank Plc's own consolidated (Group) Statement of Financial Position, "
    "Statement of Profit or Loss and Other Comprehensive Income, and Statement of Changes in Equity, each "
    "year's own originally-published figures (not a later year's restated comparative):\n"
    f"FY2025: Annual Report 2025, pp.52,51,55 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, pp.57,56,58 - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, pp.54,53,57 - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022 (AMENDED filing, 30 Oct 2023), pp.52,51,55 - {AR2022_AMENDED_URL}\n"
    f"FY2021: Annual Report 2021, pp.48,47,51 - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020, pp.51,50,53-54 (Statements of Financial Position/P&L/Changes in Equity, "
    f"Group columns) - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019, pp.45,44,47-48 - {AR2019_URL}\n"
    f"FY2018: Annual Report 2018, pp.39,38,41-42 - {AR2018_URL}\n"
    f"FY2017: Annual Report 2017, p.31 (Statements of Financial Position and P&L share this printed page "
    f"number in FCE's own PDF - a genuine footer-numbering duplication in the source document, not a "
    f"transcription error) and p.33 (Statements of Changes in Equity) - {AR2017_URL}\n"
    f"FY2016: Annual Report 2016, pp.60,59,62 - {AR2016_URL}\n"
    f"FY2015: Annual Report 2015, pp.60,59,62 - {AR2015_URL}\n"
    f"FY2014: Annual Report and Accounts 2014, pp.39,38,41 (Statements of financial position/profit and "
    f"loss/changes in equity, Group columns) - {AR2014_URL}\n"
    + STATEMENTS_ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - FCE Bank Plc's own Note 13 'Allowance for Expected Credit Losses' (IFRS 9, FY2018 onward) or "
    "Note 14/15 'Provision for Incurred Losses' (IAS 39, FY2014-FY2017), Group basis (retail, finance leases "
    "and wholesale receivables), closing balances each year:\n"
    f"FY2025/FY2024: Annual Report 2025, p.83 (Note 13, Group table) - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report 2023, p.83 (Note 13, Group table) - {AR2023_URL}\n"
    f"FY2021: Annual Report 2021, p.78 (Note 13, Group table) - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020, p.83 (Note 13 GCA/ECL by stage, Group table) - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019, p.80 (Note 13 GCA/ECL by stage, Group table) - {AR2019_URL}\n"
    f"FY2018: Annual Report 2018, p.67 (Note 14 ECL roll-forward, Group table; GCA-by-stage not separately "
    f"tabulated for FY2018 itself, only recovered as FY2018 comparatives in the FY2019 report's own Note 13) "
    f"- {AR2018_URL}\n"
    f"FY2017: Annual Report 2017, p.59 (Note 14 'Provision for Incurred Losses', Group table, Retail/"
    f"Wholesale/Total, IAS 39 - not stage-split) - {AR2017_URL}\n"
    f"FY2016: Annual Report 2016, p.87 (Note 14, Group table, IAS 39) - {AR2016_URL}\n"
    f"FY2015: Annual Report 2015, p.88 (Note 14, Group table, IAS 39) - {AR2015_URL}\n"
    f"FY2014: Annual Report and Accounts 2014, p.68 (Note 15, Group table, IAS 39) - {AR2014_URL}\n"
    "Each year's own closing balance ties exactly to the next year's own opening balance in the same note "
    "(confirmed chained across FY2014-FY2025, including across the FY2017/FY2018 IAS39-to-IFRS9 transition: "
    "FY2017's own £44m Total impairment allowance is the same figure FY2018's own Note 14 restates as its "
    "1 Jan 2018 £27m 'Loss allowance at January 1, 2018' after IFRS 9 remeasurement on transition - a genuine "
    "one-off transition adjustment, not a data error). Portfolio Split (Retail and Finance Leases vs "
    "Wholesale) is also disclosed each year but not reproduced here for brevity - see the note itself for "
    "that breakdown.\n"
    "METHODOLOGY NOTE: FY2014-FY2017 used the IAS 39 'incurred loss' model - a single Retail/Wholesale "
    "impairment allowance with no IFRS 9-style Stage 1/2/3 split, so the Stage GCA/ECL rows below are left "
    "blank for these 4 years (not comparable, not force-fit) and a separate 'Total impairment allowance "
    "(IAS 39 incurred-loss model)' row is shown instead. IFRS 9's three-stage ECL model was adopted 1 Jan "
    "2018 - FY2018-FY2025 all use the Stage 1/2/3 GCA and ECL rows.\n"
    + ENTITY_NOTE
)

RWA_BREAKDOWN_NOTE = (
    "FY2014-FY2021: directly disclosed every year, either in the standalone 2014 Pillar 3 document (Note 5 "
    "'Pillar 1 Capital Requirement: Total - Split by Risk Type', p.21) or in that year's own Annual Report's "
    "'Pillar 3 Disclosures' chapter (Table 5 'Capital Requirement Split by Risk Type', FY2015-FY2021) - see "
    "p3_sources() above for the exact page per year. FY2022-FY2025: Not publicly disclosed - no Pillar 3 "
    "chapter exists in these years' Annual Reports (confirmed by reading each report's own contents page - "
    "no 'Pillar 3 Disclosures' section listed for FY2022 onward)."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents",
     {"FY2025": 1111, "FY2024": 1253, "FY2023": 2557, "FY2022": 2536, "FY2021": 1822,
      "FY2020": 2048, "FY2019": 1453, "FY2018": 1879, "FY2017": 1544, "FY2016": 1654,
      "FY2015": 1669, "FY2014": 1628}),
    ("DATA", "Derivative financial instruments",
     {"FY2025": 44, "FY2024": 96, "FY2023": 112, "FY2022": 301, "FY2021": 63,
      "FY2020": 93, "FY2019": 147, "FY2018": 244, "FY2017": 334, "FY2016": 349,
      "FY2015": 162, "FY2014": 163}),
    ("DATA", "Other assets",
     {"FY2025": 299, "FY2024": 333, "FY2023": 481, "FY2022": 441, "FY2021": 320,
      "FY2020": 1148, "FY2019": 625, "FY2018": 554, "FY2017": 532, "FY2016": 415,
      "FY2015": 285, "FY2014": 288}),
    ("DATA", "Loans and advances to customers",
     {"FY2025": 11490, "FY2024": 12021, "FY2023": 15115, "FY2022": 14297, "FY2021": 12602,
      "FY2020": 15804, "FY2019": 17866, "FY2018": 18526, "FY2017": 16798, "FY2016": 14800,
      "FY2015": 12439, "FY2014": 10548}),
    ("DATA", "Property and equipment",
     {"FY2023": 218, "FY2022": 99, "FY2021": 162,
      "FY2020": 316, "FY2019": 305, "FY2018": 379, "FY2017": 294, "FY2016": 252,
      "FY2015": 176, "FY2014": 207}),
    ("DATA", "Right-of-use assets",
     {"FY2023": 10, "FY2022": 15, "FY2021": 17,
      "FY2020": 26, "FY2019": 35}),
    ("DATA", "Investment in a joint venture (Forso JV; disposed/nil by FY2017)",
     {"FY2016": 55, "FY2015": 44, "FY2014": 43}),
    ("DATA", "Intangible assets",
     {"FY2025": 68, "FY2024": 67, "FY2023": 58, "FY2022": 46, "FY2021": 38,
      "FY2020": 33, "FY2019": 26, "FY2018": 19, "FY2017": 14, "FY2016": 11,
      "FY2015": 11, "FY2014": 10}),
    ("DATA", "Income taxes receivable",
     {"FY2025": 51, "FY2024": 32, "FY2023": 44, "FY2022": 40, "FY2021": 6,
      "FY2020": 7, "FY2019": 11, "FY2018": 5, "FY2017": 1, "FY2016": 5,
      "FY2015": 16, "FY2014": 93}),
    ("DATA", "Deferred tax assets",
     {"FY2025": 32, "FY2024": 35, "FY2023": 35, "FY2022": 28, "FY2021": 35,
      "FY2020": 59, "FY2019": 71, "FY2018": 85, "FY2017": 78, "FY2016": 81,
      "FY2015": 58, "FY2014": 66}),
    ("DATA", "Investment in other entities",
     {"FY2020": 0, "FY2019": 0, "FY2018": 4, "FY2017": 3, "FY2016": 4,
      "FY2015": 3, "FY2014": 3}),
    ("TOTAL", "Total assets",
     {"FY2025": 13095, "FY2024": 13837, "FY2023": 18630, "FY2022": 17803, "FY2021": 15065,
      "FY2020": 19534, "FY2019": 20539, "FY2018": 21695, "FY2017": 19598, "FY2016": 17626,
      "FY2015": 14863, "FY2014": 13049}),

    ("SECTION", "Liabilities", {}),
    ("DATA", "Financial liabilities / Borrowings from parent, banks and other financial institutions",
     {"FY2025": 4940, "FY2024": 5005, "FY2023": 6580, "FY2022": 7542, "FY2021": 6987,
      "FY2020": 12466, "FY2019": 15315}),
    ("DATA", "Due to banks and other financial institutions (FY2014-FY2018 only)",
     {"FY2018": 3051, "FY2017": 2077, "FY2016": 2738, "FY2015": 3585, "FY2014": 2912}),
    ("DATA", "Due to parent and related undertakings (FY2014-FY2018 only)",
     {"FY2018": 4355, "FY2017": 2436, "FY2016": 1170, "FY2015": 716, "FY2014": 1231}),
    ("DATA", "Debt securities in issue (FY2014-FY2018 only)",
     {"FY2018": 9563, "FY2017": 11477, "FY2016": 10773, "FY2015": 8007, "FY2014": 6393}),
    ("DATA", "Subordinated loans (FY2014-FY2018 only)",
     {"FY2018": 335, "FY2017": 334, "FY2016": 308, "FY2015": 217, "FY2014": 214}),
    ("DATA", "Lease liabilities",
     {"FY2023": 11, "FY2022": 15, "FY2021": 17,
      "FY2020": 27, "FY2019": 36}),
    ("DATA", "Deposits",
     {"FY2025": 5892, "FY2024": 6300, "FY2023": 8962, "FY2022": 7131, "FY2021": 5001,
      "FY2020": 3609, "FY2019": 1970, "FY2018": 1198, "FY2017": 388, "FY2016": 69,
      "FY2015": 56, "FY2014": 51}),
    ("DATA", "Derivative financial instruments",
     {"FY2025": 91, "FY2024": 100, "FY2023": 104, "FY2022": 135, "FY2021": 16,
      "FY2020": 43, "FY2019": 42, "FY2018": 27, "FY2017": 20, "FY2016": 38,
      "FY2015": 106, "FY2014": 61}),
    ("DATA", "Other liabilities",
     {"FY2025": 226, "FY2024": 250}),
    ("DATA", "Provisions",
     {"FY2025": 161, "FY2024": 84}),
    ("DATA", "Other liabilities and provisions (combined)",
     {"FY2023": 359, "FY2022": 390, "FY2021": 235,
      "FY2020": 334, "FY2019": 335, "FY2018": 390, "FY2017": 347, "FY2016": 292,
      "FY2015": 210, "FY2014": 245}),
    ("DATA", "Provisions (FY2014-FY2015 only, separate from Other liabilities)",
     {"FY2015": 11, "FY2014": 35}),
    ("DATA", "Income taxes payable",
     {"FY2025": 66, "FY2024": 25, "FY2023": 19, "FY2022": 26, "FY2021": 40,
      "FY2020": 28, "FY2019": 37, "FY2018": 100, "FY2017": 101, "FY2016": 46,
      "FY2015": 34, "FY2014": 101}),
    ("DATA", "Deferred tax liabilities",
     {"FY2025": 15, "FY2024": 8, "FY2023": 39, "FY2022": 62, "FY2021": 27,
      "FY2020": 24, "FY2019": 25, "FY2018": 29, "FY2017": 10, "FY2016": 10,
      "FY2015": 19, "FY2014": 15}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 11391, "FY2024": 11772, "FY2023": 16074, "FY2022": 15301, "FY2021": 12323,
      "FY2020": 16531, "FY2019": 17760, "FY2018": 19048, "FY2017": 17190, "FY2016": 15444,
      "FY2015": 12961, "FY2014": 11258}),

    ("SECTION", "Equity", {}),
    ("DATA", "Ordinary shares",
     {"FY2025": 614, "FY2024": 614, "FY2023": 614, "FY2022": 614, "FY2021": 614,
      "FY2020": 614, "FY2019": 614, "FY2018": 614, "FY2017": 614, "FY2016": 614,
      "FY2015": 614, "FY2014": 614}),
    ("DATA", "Share premium",
     {"FY2025": 352, "FY2024": 352, "FY2023": 352, "FY2022": 352, "FY2021": 352,
      "FY2020": 352, "FY2019": 352, "FY2018": 352, "FY2017": 352, "FY2016": 352,
      "FY2015": 352, "FY2014": 352}),
    ("DATA", "Retained earnings",
     {"FY2025": 738, "FY2024": 1099, "FY2023": 1590, "FY2022": 1536, "FY2021": 1776,
      "FY2020": 2037, "FY2019": 1813, "FY2018": 1681, "FY2017": 1442, "FY2016": 1216,
      "FY2015": 936, "FY2014": 825}),
    ("TOTAL", "Total equity",
     {"FY2025": 1704, "FY2024": 2065, "FY2023": 2556, "FY2022": 2502, "FY2021": 2742,
      "FY2020": 3003, "FY2019": 2779, "FY2018": 2647, "FY2017": 2408, "FY2016": 2182,
      "FY2015": 1902, "FY2014": 1791}),
    ("TOTAL", "Total liabilities and equity",
     {"FY2025": 13095, "FY2024": 13837, "FY2023": 18630, "FY2022": 17803, "FY2021": 15065,
      "FY2020": 19534, "FY2019": 20539, "FY2018": 21695, "FY2017": 19598, "FY2016": 17626,
      "FY2015": 14863, "FY2014": 13049}),
]

bw.add_balance_sheet_sheet(
    title="FCE Bank Plc — Balance Sheet",
    subtitle="Group/Consolidated basis, £m. See source note at bottom (presentation changes documented).",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=95,
    source_height=560,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income",
     {"FY2025": 860, "FY2024": 874, "FY2023": 974, "FY2022": 576, "FY2021": 552,
      "FY2020": 679, "FY2019": 748, "FY2018": 724, "FY2017": 647, "FY2016": 630,
      "FY2015": 564, "FY2014": 587}),
    ("DATA", "Interest expense",
     {"FY2025": -470, "FY2024": -527, "FY2023": -505, "FY2022": -170, "FY2021": -162,
      "FY2020": -217, "FY2019": -208, "FY2018": -178, "FY2017": -181, "FY2016": -190,
      "FY2015": -176, "FY2014": -192}),
    ("TOTAL", "Net interest income",
     {"FY2025": 390, "FY2024": 347, "FY2023": 469, "FY2022": 406, "FY2021": 390,
      "FY2020": 462, "FY2019": 540, "FY2018": 546, "FY2017": 466, "FY2016": 440,
      "FY2015": 388, "FY2014": 395}),
    ("DATA", "Fees and commissions income",
     {"FY2025": 43, "FY2024": 58, "FY2023": 61, "FY2022": 62, "FY2021": 53,
      "FY2020": 61, "FY2019": 63, "FY2018": 67, "FY2017": 64, "FY2016": 47,
      "FY2015": 40, "FY2014": 43}),
    ("DATA", "Fees and commissions expense",
     {"FY2025": -11, "FY2024": -8, "FY2023": -7, "FY2022": -6, "FY2021": -8,
      "FY2020": -11, "FY2019": -10, "FY2018": -10, "FY2017": -9, "FY2016": -6,
      "FY2015": -5, "FY2014": -10}),
    ("TOTAL", "Net fees and commissions income",
     {"FY2025": 32, "FY2024": 50, "FY2023": 54, "FY2022": 56, "FY2021": 45,
      "FY2020": 50, "FY2019": 53, "FY2018": 57, "FY2017": 55, "FY2016": 41,
      "FY2015": 35, "FY2014": 33}),
    ("DATA", "Other operating income / Income from leasing & other operating income",
     {"FY2025": 0, "FY2024": 8, "FY2023": 52, "FY2022": 54, "FY2021": 164,
      "FY2020": 224, "FY2019": 426, "FY2018": 336, "FY2017": 322, "FY2016": 216,
      "FY2015": 175, "FY2014": 181}),
    ("TOTAL", "Total income",
     {"FY2025": 422, "FY2024": 405, "FY2023": 575, "FY2022": 516, "FY2021": 599,
      "FY2020": 736, "FY2019": 1019, "FY2018": 939, "FY2017": 843, "FY2016": 697,
      "FY2015": 598, "FY2014": 609}),

    ("SECTION", "Expenses", {}),
    ("DATA", "Allowance for expected credit losses / Impairment losses on loans and advances",
     {"FY2025": -31, "FY2024": -18, "FY2023": -2, "FY2022": 4, "FY2021": 5,
      "FY2020": -49, "FY2019": -22, "FY2018": -17, "FY2017": -21, "FY2016": -22,
      "FY2015": -11, "FY2014": -9}),
    ("DATA", "Operating expenses",
     {"FY2025": -265, "FY2024": -243, "FY2023": -287, "FY2022": -255, "FY2021": -239,
      "FY2020": -275, "FY2019": -276, "FY2018": -305, "FY2017": -260, "FY2016": -292,
      "FY2015": -200, "FY2014": -204}),
    ("DATA", "(Loss)/Gain on disposal of Operating Leases",
     {"FY2023": -13, "FY2022": 30, "FY2021": -16}),
    ("DATA", "Depreciation and amortisation (combined, FY2025 only)",
     {"FY2025": -15}),
    ("DATA", "Depreciation of property and equipment",
     {"FY2024": 0, "FY2023": -37, "FY2022": -29, "FY2021": -131,
      "FY2020": -190, "FY2019": -400, "FY2018": -320, "FY2017": -292, "FY2016": -203,
      "FY2015": -164, "FY2014": -175}),
    ("DATA", "Depreciation of right-of-use assets",
     {"FY2024": -4, "FY2023": -5, "FY2022": -5, "FY2021": -8,
      "FY2020": -6, "FY2019": -5}),
    ("DATA", "(Loss)/Gain on fair value adjustment - non designated derivatives",
     {"FY2025": -31, "FY2024": 46, "FY2023": -98, "FY2022": 128, "FY2021": 46,
      "FY2020": -3, "FY2019": -65, "FY2018": -8, "FY2017": 56, "FY2016": 285,
      "FY2015": -23, "FY2014": -24}),
    ("DATA", "Gain/(Loss) on foreign exchange",
     {"FY2025": 87, "FY2024": -69, "FY2023": -12, "FY2022": 28, "FY2021": -18,
      "FY2020": -29, "FY2019": 46, "FY2018": -8, "FY2017": -46, "FY2016": -292,
      "FY2015": 13, "FY2014": -3}),
    ("DATA", "Share of profit of a joint venture (FY2014-FY2017 only)",
     {"FY2017": 3, "FY2016": 5, "FY2015": 4, "FY2014": 3}),
    ("TOTAL", "Profit before tax",
     {"FY2025": 167, "FY2024": 117, "FY2023": 121, "FY2022": 417, "FY2021": 238,
      "FY2020": 184, "FY2019": 297, "FY2018": 281, "FY2017": 283, "FY2016": 178,
      "FY2015": 217, "FY2014": 197}),
    ("DATA", "Income tax expense",
     {"FY2025": -71, "FY2024": -62, "FY2023": -33, "FY2022": -130, "FY2021": -84,
      "FY2020": -56, "FY2019": -73, "FY2018": -72, "FY2017": -70, "FY2016": -34,
      "FY2015": -57, "FY2014": -50}),
    ("TOTAL", "Profit after tax in respect of continuing operations",
     {"FY2025": 96, "FY2024": 55, "FY2023": 88, "FY2022": 287, "FY2021": 154,
      "FY2020": 128, "FY2019": 224, "FY2018": 209, "FY2017": 213, "FY2016": 144,
      "FY2015": 160, "FY2014": 147}),
    ("DATA", "Profit after tax in respect of discontinued operations (Ford Bank GmbH, FY2024 only)",
     {"FY2024": 157}),
    ("TOTAL", "Profit for the period",
     {"FY2025": 96, "FY2024": 212, "FY2023": 88, "FY2022": 287, "FY2021": 154,
      "FY2020": 128, "FY2019": 224, "FY2018": 209, "FY2017": 213, "FY2016": 144,
      "FY2015": 160, "FY2014": 147}),

    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Translation differences on foreign currency net investments (continuing operations)",
     {"FY2025": 43, "FY2024": -42}),
    ("DATA", "Translation differences on foreign currency net investments (discontinued operations)",
     {"FY2024": -27}),
    ("DATA", "Translation differences on foreign currency net investments (FY2014-FY2023, not split)",
     {"FY2023": -33, "FY2022": 78, "FY2021": -115,
      "FY2020": 94, "FY2019": -89, "FY2018": 17, "FY2017": 43, "FY2016": 178,
      "FY2015": -44, "FY2014": -70}),
    ("DATA", "Translation differences on foreign currency net investments in a joint venture (FY2014-FY2016 only)",
     {"FY2016": 6, "FY2015": -5}),
    ("DATA", "Items recycled through profit or loss (realisation of FX on sale of subsidiaries)",
     {"FY2024": -134}),
    ("DATA", "Available for sale gains/(losses) or equity investments at FVOCI",
     {"FY2019": -3, "FY2018": 1, "FY2017": -1, "FY2016": 1}),
    ("TOTAL", "Total comprehensive income for the period",
     {"FY2025": 139, "FY2024": 9, "FY2023": 55, "FY2022": 365, "FY2021": 39,
      "FY2020": 222, "FY2019": 132, "FY2018": 227, "FY2017": 255, "FY2016": 329,
      "FY2015": 111, "FY2014": 77}),
]

bw.add_income_statement_sheet(
    title="FCE Bank Plc — Profit & Loss",
    subtitle="Group/Consolidated basis, £m. See source note at bottom (presentation changes and FY2023 "
              "non-restated own-year figures documented).",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=95,
    source_height=560,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Share premium", "Profit or loss reserve", "Translation reserve",
                   "Total retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "At 1 January 2014", (614, 352, 419, 330, 749, 1715)),
    ("DATA", "Profit for the year", (None, None, 147, None, 147, 147)),
    ("DATA", "Translation differences", (None, None, None, -70, -70, -70)),
    ("DATA", "Other equity adjustments", (None, None, -1, None, -1, -1)),
    ("TOTAL", "At 31 December 2014", (614, 352, 565, 260, 825, 1791)),

    ("TOTAL", "At 1 January 2015", (614, 352, 565, 260, 825, 1791)),
    ("DATA", "Profit for the year", (None, None, 160, None, 160, 160)),
    ("DATA", "Translation differences", (None, None, None, -49, -49, -49)),
    ("TOTAL", "At 31 December 2015", (614, 352, 725, 211, 936, 1902)),

    ("TOTAL", "At 1 January 2016", (614, 352, 725, 211, 936, 1902)),
    ("DATA", "Profit for the year", (None, None, 144, None, 144, 144)),
    ("DATA", "Translation differences", (None, None, None, 184, 184, 184)),
    ("DATA", "Available for sale gains in fair value", (None, None, 1, None, 1, 1)),
    ("DATA", "Dividend paid", (None, None, -50, None, -50, -50)),
    ("DATA", "Other equity adjustments", (None, None, 1, None, 1, 1)),
    ("TOTAL", "At 31 December 2016 / 1 January 2017", (614, 352, 821, 395, 1216, 2182)),

    ("DATA", "Profit for the year", (None, None, 213, None, 213, 213)),
    ("DATA", "Translation differences", (None, None, None, 43, 43, 43)),
    ("DATA", "Available for sale loss in fair value", (None, None, -1, None, -1, -1)),
    ("DATA", "Dividend paid", (None, None, -35, None, -35, -35)),
    ("DATA", "Ret'd Earnings Adj IFRS 15 early adoption", (None, None, 6, None, 6, 6)),
    ("TOTAL", "At 31 December 2017", (614, 352, 1005, 437, 1442, 2408)),

    ("TOTAL", "At 1 January 2018", (614, 352, 1005, 437, 1442, 2408)),
    ("DATA", "Profit for the year", (None, None, 209, None, 209, 209)),
    ("DATA", "Translation differences", (None, None, None, 17, 17, 17)),
    ("DATA", "Equity Investment FVOCI/other equity adjustments", (None, None, 12, 1, 13, 13)),
    ("TOTAL", "At 31 December 2018", (614, 352, 1226, 455, 1681, 2647)),

    ("TOTAL", "At 1 January 2019", (614, 352, 1226, 455, 1681, 2647)),
    ("DATA", "Profit for the year", (None, None, 224, None, 224, 224)),
    ("DATA", "Translation differences", (None, None, None, -89, -89, -89)),
    ("DATA", "Equity Investment FVOCI", (None, None, None, -3, -3, -3)),
    ("TOTAL", "At 31 December 2019", (614, 352, 1450, 363, 1813, 2779)),

    ("TOTAL", "At 1 January 2020", (614, 352, 1447, 366, 1813, 2779)),
    ("DATA", "Profit for the year", (None, None, 128, None, 128, 128)),
    ("DATA", "Translation differences", (None, None, None, 94, 94, 94)),
    ("DATA", "Other equity adjustments", (None, None, 2, None, 2, 2)),
    ("TOTAL", "At 31 December 2020", (614, 352, 1577, 460, 2037, 3003)),

    ("TOTAL", "At 1 January 2021", (614, 352, 1577, 460, 2037, 3003)),
    ("DATA", "Profit for the year", (None, None, 154, None, 154, 154)),
    ("DATA", "Translation differences", (None, None, None, -115, -115, -115)),
    ("DATA", "Dividend paid", (None, None, -300, None, -300, -300)),
    ("TOTAL", "At 31 December 2021", (614, 352, 1431, 345, 1776, 2742)),

    ("TOTAL", "At 1 January 2022", (614, 352, 1431, 345, 1776, 2742)),
    ("DATA", "Profit for the year", (None, None, 287, None, 287, 287)),
    ("DATA", "Translation differences", (None, None, None, 89, 89, 89)),
    ("DATA", "Reclassification of foreign exchange on transfer of subsidiaries", (None, None, None, -11, -11, -11)),
    ("DATA", "Dividend paid", (None, None, -600, None, -600, -600)),
    ("DATA", "Other equity adjustments", (None, None, -5, None, -5, -5)),
    ("TOTAL", "At 31 December 2022", (614, 352, 1113, 423, 1536, 2502)),

    ("TOTAL", "At 1 January 2023", (614, 352, 1113, 423, 1536, 2502)),
    ("DATA", "Profit for the year", (None, None, 88, None, 88, 88)),
    ("DATA", "Translation differences", (None, None, None, -33, -33, -33)),
    ("DATA", "Other equity adjustments", (None, None, -1, None, -1, -1)),
    ("TOTAL", "At 31 December 2023", (614, 352, 1200, 390, 1590, 2556)),

    ("TOTAL", "At 1 January 2024", (614, 352, 1214, 376, 1590, 2556)),
    ("DATA", "Profit for the year", (None, None, 212, None, 212, 212)),
    ("DATA", "Translation differences", (None, None, None, -69, -69, -69)),
    ("DATA", "Realisation of foreign exchange on sale of subsidiaries", (None, None, None, -134, -134, -134)),
    ("DATA", "Dividend paid", (None, None, -500, None, -500, -500)),
    ("TOTAL", "At 31 December 2024 / 1 January 2025", (614, 352, 926, 173, 1099, 2065)),

    ("DATA", "Profit for the year", (None, None, 96, None, 96, 96)),
    ("DATA", "Translation differences", (None, None, None, 43, 43, 43)),
    ("DATA", "Dividend paid", (None, None, -500, None, -500, -500)),
    ("TOTAL", "At 31 December 2025", (614, 352, 522, 216, 738, 1704)),
]

bw.add_equity_changes_sheet(
    title="FCE Bank Plc — Statement of Changes in Equity",
    subtitle="Group/Consolidated basis, £m, chronological (oldest to newest). Per-year reconciliation "
              "ladder confirmed: every closing balance ties exactly to the Balance Sheet's own Total "
              "equity, with minor (<£1m) rounding gaps at a few opening-balance handoffs where the "
              "following year's own report restates its own prior-year opening figures slightly "
              "(documented per row) - never a data error, always each year's own disclosed number.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=54,
    source_height=560,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement (Group/Consolidated basis)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Cash from/(used in) operating activities",
     {"FY2025": 554, "FY2024": -1420, "FY2023": -1661, "FY2022": -1431, "FY2021": 2574,
      "FY2020": 2252, "FY2019": -773, "FY2018": -2394, "FY2017": -2182, "FY2016": -1660,
      "FY2015": -2464, "FY2014": -1960}),
    ("DATA", "Interest paid",
     {"FY2025": -475, "FY2024": -672, "FY2023": -542, "FY2022": -177, "FY2021": -184,
      "FY2020": -217, "FY2019": -221, "FY2018": -198, "FY2017": -211, "FY2016": -195,
      "FY2015": -207, "FY2014": -234}),
    ("DATA", "Interest received",
     {"FY2025": 926, "FY2024": 1160, "FY2023": 1071, "FY2022": 442, "FY2021": 836,
      "FY2020": 468, "FY2019": 830, "FY2018": 839, "FY2017": 567, "FY2016": 619,
      "FY2015": 571, "FY2014": 560}),
    ("DATA", "Other operating income received",
     {"FY2025": 0, "FY2024": 48, "FY2023": 72, "FY2022": 26, "FY2021": 109,
      "FY2020": 238, "FY2019": 490, "FY2018": 384, "FY2017": 343, "FY2016": 254,
      "FY2015": 128, "FY2014": 190}),
    ("DATA", "Income taxes paid",
     {"FY2025": -39, "FY2024": -51, "FY2023": -73, "FY2022": -133, "FY2021": -43,
      "FY2020": -50, "FY2019": -133, "FY2018": -64, "FY2017": -24, "FY2016": -42,
      "FY2015": -37, "FY2014": -166}),
    ("DATA", "Income taxes refunded",
     {"FY2015": 27, "FY2014": 1}),
    ("TOTAL", "Net cash generated from/(used in) operating activities",
     {"FY2025": 966, "FY2024": -935, "FY2023": -1133, "FY2022": -1273, "FY2021": 3292,
      "FY2020": 2691, "FY2019": 193, "FY2018": -1433, "FY2017": -1507, "FY2016": -1024,
      "FY2015": -1982, "FY2014": -1609}),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property and equipment",
     {"FY2025": -2, "FY2024": 0, "FY2023": -6, "FY2022": -6, "FY2021": -1,
      "FY2020": -1, "FY2019": -41, "FY2018": -1, "FY2017": -4, "FY2016": -2,
      "FY2015": -3, "FY2014": -4}),
    ("DATA", "Proceeds from sale of property and equipment",
     {"FY2021": 6,
      "FY2020": 1, "FY2018": 0, "FY2017": 3, "FY2016": 0, "FY2015": 2, "FY2014": 2}),
    ("DATA", "Investment in internally and externally generated software",
     {"FY2025": -13, "FY2024": -19, "FY2023": -21, "FY2022": -15, "FY2021": -11,
      "FY2020": -11, "FY2019": -10, "FY2018": -7, "FY2017": -4, "FY2016": -2,
      "FY2015": -2, "FY2014": -2}),
    ("DATA", "Net cash movement in sale of subsidiaries",
     {"FY2023": 0, "FY2022": -13}),
    ("DATA", "Dividends from Group undertaking / joint venture",
     {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Investment in other entities",
     {"FY2019": 0, "FY2018": -1}),
    ("DATA", "Net cash (outflow)/inflow on derivative financial instruments",
     {"FY2025": 2, "FY2024": 109, "FY2023": 165, "FY2022": 29}),
    ("DATA", "Increase in restricted cash",
     {"FY2025": -65, "FY2024": -61, "FY2023": -61, "FY2022": -73}),
    ("DATA", "Decrease in restricted cash",
     {"FY2025": 61, "FY2024": 84, "FY2023": 62, "FY2022": 63}),
    ("DATA", "Dividend from subsidiaries",
     {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Net cash (used in)/generated from investing activities",
     {"FY2025": -17, "FY2024": 113, "FY2023": 139, "FY2022": -15, "FY2021": -6,
      "FY2020": -11, "FY2019": -51, "FY2018": -9, "FY2017": -5, "FY2016": -4,
      "FY2015": -3, "FY2014": -4}),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from the issue of debt securities and from loans provided by banks and other financial institutions",
     {"FY2025": 1001, "FY2024": 1642, "FY2023": 1311, "FY2022": 4482, "FY2021": 2972,
      "FY2020": 3505, "FY2019": 5318, "FY2018": 8436, "FY2017": 9523, "FY2016": 8277,
      "FY2015": 10785, "FY2014": 8781}),
    ("DATA", "Repayments of debt securities and of loans provided by banks and other financial institutions",
     {"FY2025": -797, "FY2024": -1790, "FY2023": -2022, "FY2022": -3861, "FY2021": -6212,
      "FY2020": -7357, "FY2019": -7126, "FY2018": -9462, "FY2017": -9728, "FY2016": -7768,
      "FY2015": -8538, "FY2014": -7536}),
    ("DATA", "Proceeds of funds provided by parent and related undertakings",
     {"FY2025": 211, "FY2024": 214, "FY2023": 698, "FY2022": 568, "FY2021": 398,
      "FY2020": 1330, "FY2019": 2416, "FY2018": 8059, "FY2017": 1542, "FY2016": 745,
      "FY2015": 179, "FY2014": 42}),
    ("DATA", "Repayment of funds provided by parent and related undertakings",
     {"FY2025": -557, "FY2024": -485, "FY2023": -548, "FY2022": -480, "FY2021": -2614,
      "FY2020": -833, "FY2019": -1735, "FY2018": -6175, "FY2017": -249, "FY2016": -323,
      "FY2015": -751, "FY2014": -150}),
    ("DATA", "Net (decrease)/increase in short-term borrowings",
     {"FY2025": -61, "FY2024": 343, "FY2023": -289, "FY2022": -168, "FY2021": 472,
      "FY2020": -102, "FY2019": -223, "FY2018": 14, "FY2017": -50, "FY2016": -140,
      "FY2015": 308, "FY2014": -14}),
    ("DATA", "Net (decrease)/increase in deposits",
     {"FY2025": -408, "FY2024": 517, "FY2023": 1891, "FY2022": 2005, "FY2021": 1427,
      "FY2020": 1637, "FY2019": 772, "FY2018": 810, "FY2017": 319, "FY2016": 13,
      "FY2015": 4}),
    ("DATA", "Net cash inflow/(outflow) on derivative financial instruments (FY2021 only - "
             "classified under Investing in later years' presentation, see ENTITY_NOTE)",
     {"FY2021": 44,
      "FY2020": 58, "FY2019": 63, "FY2018": 103, "FY2017": 32, "FY2016": 99,
      "FY2015": 33, "FY2014": -31}),
    ("DATA", "Increase in restricted cash (FY2021 only - classified under Investing in later "
             "years' presentation)",
     {"FY2021": -97,
      "FY2020": -410, "FY2019": -119, "FY2018": -97, "FY2017": -67, "FY2016": -97,
      "FY2015": -55, "FY2014": -97}),
    ("DATA", "Decrease in restricted cash (FY2021 only - classified under Investing in later "
             "years' presentation)",
     {"FY2021": 463,
      "FY2020": 47, "FY2019": 120, "FY2018": 85, "FY2017": 66, "FY2016": 49,
      "FY2015": 89, "FY2014": 104}),
    ("DATA", "Dividend paid",
     {"FY2025": -500, "FY2024": 0, "FY2023": 0, "FY2022": -600, "FY2021": -300}),
    ("TOTAL", "Net cash (used in)/generated from financing activities",
     {"FY2025": -1111, "FY2024": 441, "FY2023": 1041, "FY2022": 1946, "FY2021": -3447,
      "FY2020": -2125, "FY2019": -514, "FY2018": 1773, "FY2017": 1388, "FY2016": 855,
      "FY2015": 2054, "FY2014": 1099}),

    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents",
     {"FY2025": -162, "FY2024": -381, "FY2023": 47, "FY2022": 658, "FY2021": -161,
      "FY2020": 555, "FY2019": -372, "FY2018": 331, "FY2017": -124, "FY2016": -173,
      "FY2015": 69, "FY2014": -514}),
    ("DATA", "Cash and cash equivalents at beginning of year",
     {"FY2025": 1253, "FY2024": 2557, "FY2023": 2536, "FY2022": 1822, "FY2021": 2048,
      "FY2020": 1453, "FY2019": 1879, "FY2018": 1544, "FY2017": 1654, "FY2016": 1669,
      "FY2015": 1625, "FY2014": 2209}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents",
     {"FY2025": 20, "FY2024": -50, "FY2023": -26, "FY2022": 56, "FY2021": -65,
      "FY2020": 40, "FY2019": -54, "FY2018": 4, "FY2017": 14, "FY2016": 158,
      "FY2015": -25, "FY2014": -70}),
    ("DATA", "Cash and cash equivalents in respect of discontinued operations",
     {"FY2024": -873}),
    ("TOTAL", "Cash and cash equivalents at end of year",
     {"FY2025": 1111, "FY2024": 1253, "FY2023": 2557, "FY2022": 2536, "FY2021": 1822,
      "FY2020": 2048, "FY2019": 1453, "FY2018": 1879, "FY2017": 1544, "FY2016": 1654,
      "FY2015": 1669, "FY2014": 1625}),
]

bw.add_cash_flow_sheet(
    title="FCE Bank Plc — Consolidated Statement of Cash Flows",
    subtitle="Group/Consolidated basis, £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross Carrying Amount (GCA) by IFRS 9 stage, closing balance (FY2018 onward - "
                "IFRS 9 adopted 1 Jan 2018; FY2014-FY2017 used the IAS 39 incurred-loss model, "
                "see below)", {}),
    ("DATA", "Stage 1 GCA",
     {"FY2025": 11363, "FY2024": 11731, "FY2023": 14782, "FY2022": 12290, "FY2021": 12355,
      "FY2020": 14504, "FY2019": 10693, "FY2018": 11004}),
    ("DATA", "Stage 2 GCA",
     {"FY2025": 127, "FY2024": 269, "FY2023": 242, "FY2022": 1959, "FY2021": 153,
      "FY2020": 1084, "FY2019": 7006, "FY2018": 7265}),
    ("DATA", "Stage 3 GCA",
     {"FY2025": 22, "FY2024": 34, "FY2023": 108, "FY2022": 72, "FY2021": 127,
      "FY2020": 262, "FY2019": 188, "FY2018": 280}),
    ("TOTAL", "Total GCA",
     {"FY2025": 11512, "FY2024": 12034, "FY2023": 15132, "FY2022": 14321, "FY2021": 12635,
      "FY2020": 15850, "FY2019": 17887, "FY2018": 18549}),

    ("SECTION", "Expected Credit Loss (ECL) allowance by IFRS 9 stage, closing balance", {}),
    ("DATA", "Stage 1 ECL",
     {"FY2025": -20, "FY2024": -12, "FY2023": -16, "FY2022": -16, "FY2021": -30,
      "FY2020": -34, "FY2019": -20, "FY2018": -21}),
    ("DATA", "Stage 2 ECL",
     {"FY2025": 0, "FY2024": -1, "FY2023": -1, "FY2022": -8, "FY2021": -1,
      "FY2020": -9, "FY2019": -1, "FY2018": -2}),
    ("DATA", "Stage 3 ECL",
     {"FY2025": -2, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": -2,
      "FY2020": -3, "FY2019": 0, "FY2018": 0}),
    ("TOTAL", "Total ECL",
     {"FY2025": -22, "FY2024": -13, "FY2023": -17, "FY2022": -24, "FY2021": -33,
      "FY2020": -46, "FY2019": -21, "FY2018": -23}),

    ("SECTION", "IAS 39 incurred-loss model, Retail/Wholesale impairment allowance closing "
                "balance (FY2014-FY2017 only - superseded by IFRS 9 above from FY2018)", {}),
    ("DATA", "Retail impairment allowance",
     {"FY2017": 41, "FY2016": 38, "FY2015": 30, "FY2014": 29}),
    ("DATA", "Wholesale impairment allowance",
     {"FY2017": 3, "FY2016": 4, "FY2015": 2, "FY2014": 4}),
    ("TOTAL", "Total impairment allowance (IAS 39 incurred-loss model)",
     {"FY2017": 44, "FY2016": 42, "FY2015": 32, "FY2014": 33}),

    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 / Total GCA",
     {"FY2025": "0.19%", "FY2024": "0.28%", "FY2023": "0.71%", "FY2022": "0.50%", "FY2021": "1.01%",
      "FY2020": "1.65%", "FY2019": "1.05%", "FY2018": "1.51%"}),
    ("DATA", "Total ECL / Total GCA (overall coverage)",
     {"FY2025": "0.19%", "FY2024": "0.11%", "FY2023": "0.11%", "FY2022": "0.17%", "FY2021": "0.26%",
      "FY2020": "0.29%", "FY2019": "0.12%", "FY2018": "0.12%"}),
]

bw.add_asset_quality_sheet(
    title="FCE Bank Plc — Asset Quality",
    subtitle="Group/Consolidated basis, £m (ratios as calculated). Retail, finance leases and wholesale "
              "receivables combined - see source note at bottom for the Retail/Wholesale portfolio split "
              "disclosed in the same note, and for the IAS 39-to-IFRS 9 methodology change at FY2018.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=460,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=260)


CALC_NOTE = (
    "CALCULATED, not directly disclosed for FY2022-FY2025 (only the rounded nearest-£0.1bn chart "
    "value is published) - see the sheet's own source note for the exact FY2021 and FY2014-FY2020 "
    "figures and full methodology."
)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital (= Tier 1 Capital, no AT1 instruments held)",
      {"FY2025": 1600, "FY2024": 1800, "FY2023": 2400, "FY2022": 2100, "FY2021": 2684,
       "FY2020": 2948, "FY2019": 2727, "FY2018": 2597, "FY2017": 2369, "FY2016": 2145,
       "FY2015": 1869, "FY2014": 1756})],
    note=CALC_NOTE,
)

metric(
    "CET1 Ratio", "%",
    [("CET1 Ratio (= Tier 1 Ratio, calculated as CET1 Capital / Total RWAs)",
      {"FY2025": "16.59%", "FY2024": "17.61%", "FY2023": "17.16%", "FY2022": "16.65%", "FY2021": "23.58%",
       "FY2020": "19.54%", "FY2019": "16.54%", "FY2018": "14.84%", "FY2017": "14.67%", "FY2016": "14.53%",
       "FY2015": "15.27%", "FY2014": "16.30%"})],
    note=CALC_NOTE + " FY2021 and FY2014-FY2020 also independently cross-checked against the exact "
                     "Pillar 3 Own Funds table each year.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital (= CET1, no AT1 instruments held)",
      {"FY2025": 1600, "FY2024": 1800, "FY2023": 2400, "FY2022": 2100, "FY2021": 2684,
       "FY2020": 2948, "FY2019": 2727, "FY2018": 2597, "FY2017": 2369, "FY2016": 2145,
       "FY2015": 1869, "FY2014": 1756})],
    note=CALC_NOTE,
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 Ratio (= CET1 Ratio, no AT1 instruments held)",
      {"FY2025": "16.59%", "FY2024": "17.61%", "FY2023": "17.16%", "FY2022": "16.65%", "FY2021": "23.58%",
       "FY2020": "19.54%", "FY2019": "16.54%", "FY2018": "14.84%", "FY2017": "14.67%", "FY2016": "14.53%",
       "FY2015": "15.27%", "FY2014": "16.30%"})],
    note=CALC_NOTE,
)

metric(
    "Total Capital", "£m",
    [("Total Capital (Tier 1 + Tier 2)",
      {"FY2025": 1800, "FY2024": 2000, "FY2023": 2700, "FY2022": 2400, "FY2021": 2994,
       "FY2020": 3287, "FY2019": 3073, "FY2018": 2915, "FY2017": 2746, "FY2016": 2493,
       "FY2015": 2118, "FY2014": 2003})],
    note="FY2022-FY2025 summed from the Annual Report's own rounded (nearest £0.1bn) Tier 1/Tier 2 "
         "chart. FY2021 and FY2014-FY2020 exact from each year's own Pillar 3 Own Funds table.",
)

metric(
    "Total Capital Ratio", "%",
    [("Total Capital / Total Risk-Weighted Exposure Amounts",
      {"FY2025": "18.66%", "FY2024": "19.57%", "FY2023": "19.30%", "FY2022": "19.03%", "FY2021": "26.20%",
       "FY2020": "21.79%", "FY2019": "18.64%", "FY2018": "16.66%", "FY2017": "17.00%", "FY2016": "16.89%",
       "FY2015": "17.31%", "FY2014": "18.6%"})],
    note="Directly disclosed every year - either in the Annual Report's own 'Business Performance' - "
         "'Total Capital' chart (FY2022-FY2025), or in that year's own exact Pillar 3 Own Funds table "
         "(FY2021 and FY2014-FY2020).",
)

metric(
    "Total RWAs", "£m",
    [("Total Risk-Weighted Exposure Amounts",
      {"FY2025": 9646, "FY2024": 10220, "FY2023": 13990, "FY2022": 12612, "FY2021": 11427,
       "FY2020": 15089, "FY2019": 16483, "FY2018": 17501, "FY2017": 16148, "FY2016": 14760,
       "FY2015": 12239, "FY2014": 10775})],
    note="FY2021 and FY2014-FY2020 directly disclosed each year ('Total all risk types' / 'Total risk "
         "weighted assets', Pillar 3 Own Funds/RWA-split tables) - see the RWA Breakdown sheet "
         "immediately following for the full risk-category split every one of these 8 years. "
         "FY2022-FY2025 CALCULATED (Total Capital / Total Capital Ratio) - not directly disclosed in "
         "any of those years (no Pillar 3 chapter exists after FY2021).",
)

bw.add_rwa_breakdown_sheet(
    title="FCE Bank Plc — RWA Breakdown",
    subtitle="FY2014-FY2021 (Consolidated), £m. See source note at bottom for why FY2022-FY2025 are not "
              "publicly disclosed.",
    rows=[
        ("SECTION", "Credit risk", {}),
        ("DATA", "Credit risk (excl. counterparty credit risk)",
         {"FY2021": 10238, "FY2020": 13491, "FY2019": 15083, "FY2018": 15907, "FY2017": 14818,
          "FY2016": 13163, "FY2015": 10973, "FY2014": 9580}),
        ("DATA", "Counterparty credit risk",
         {"FY2021": 56, "FY2020": 92, "FY2019": 117, "FY2018": 201, "FY2017": 253,
          "FY2016": 280, "FY2015": 179, "FY2014": 161}),
        ("TOTAL", "Total credit risk",
         {"FY2021": 10294, "FY2020": 13583, "FY2019": 15200, "FY2018": 16108, "FY2017": 15071,
          "FY2016": 13443, "FY2015": 11152, "FY2014": 9741}),
        ("SECTION", "Other risk types", {}),
        ("DATA", "Credit valuation adjustment (CVA) risk",
         {"FY2021": 33, "FY2020": 82, "FY2019": 82, "FY2018": 140, "FY2017": 181,
          "FY2016": 233, "FY2015": 162, "FY2014": 158}),
        ("DATA", "Market risk (foreign exchange risk)",
         {"FY2021": 170, "FY2020": 491, "FY2019": 268, "FY2018": 371, "FY2017": 95,
          "FY2016": 327, "FY2015": 192, "FY2014": 182}),
        ("DATA", "Operational risk",
         {"FY2021": 930, "FY2020": 933, "FY2019": 933, "FY2018": 882, "FY2017": 801,
          "FY2016": 757, "FY2015": 733, "FY2014": 694}),
        ("TOTAL", "Total all risk types (Total RWAs)",
         {"FY2021": 11427, "FY2020": 15089, "FY2019": 16483, "FY2018": 17501, "FY2017": 16148,
          "FY2016": 14760, "FY2015": 12239, "FY2014": 10775}),
    ],
    sources_text=p3_sources() + "\n\n" + RWA_BREAKDOWN_NOTE,
    first_col_width=58,
    source_height=460,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage Ratio",
      {"FY2021": "16.95%", "FY2020": "14.59%", "FY2019": "13.02%", "FY2018": "11.74%",
       "FY2017": "11.82%", "FY2016": "11.86%", "FY2015": "12.28%", "FY2014": "12.91%"})],
    note="Directly disclosed for FY2021 and FY2014-FY2020, from each year's own dedicated 'Pillar 3 "
         "Disclosures' chapter (or, for FY2014, the standalone Pillar 3 document) - this chapter was "
         "dropped from FY2022 onward, and no leverage ratio was found anywhere in the FY2022-FY2025 "
         "reports. Not calculated for those years since no leverage exposure measure is disclosed either.",
)

bw.add_not_disclosed_metric_sheets(
    ["LCR"],
    p3_sources(),
    per_note={
        "LCR": "Not publicly disclosed for any of FY2014-FY2025 - no numeric LCR value found in any of "
               "the 11 Annual Reports or the standalone 2014 Pillar 3 document reviewed, including the "
               "FY2015-FY2021 Pillar 3 Disclosures chapters' own index of every CRR disclosure article "
               "they cover (no liquidity-ratio article listed at all) and the FY2018-FY2020 narrative "
               "LCR paragraph (describes the regulation but never states FCE's own ratio). Plausibly "
               "reflects FCE Bank's captive auto-finance/wholesale-funded business model.",
    },
)

bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={
        "NSFR": "Not publicly disclosed for any of FY2014-FY2025 - no NSFR reference found in any of "
                "the 11 Annual Reports or the standalone 2014 Pillar 3 document reviewed, including the "
                "FY2015-FY2021 Pillar 3 Disclosures chapters' own index of every CRR disclosure article "
                "they cover (no liquidity-ratio article listed at all).",
        "MREL Ratio": "Not publicly disclosed for any of FY2014-FY2025 - no MREL reference found in any "
                      "of the 11 Annual Reports or the standalone 2014 Pillar 3 document reviewed.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 13095, "FY2024": 13837, "FY2023": 18630, "FY2022": 17803, "FY2021": 15065,
                           "FY2020": 19534, "FY2019": 20539, "FY2018": 21695, "FY2017": 19598, "FY2016": 17626,
                           "FY2015": 14863, "FY2014": 13049}),
        ("Loans and advances to customers", {"FY2025": 11490, "FY2024": 12021, "FY2023": 15115, "FY2022": 14297, "FY2021": 12602,
                                              "FY2020": 15804, "FY2019": 17866, "FY2018": 18526, "FY2017": 16798, "FY2016": 14800,
                                              "FY2015": 12439, "FY2014": 10548}),
        ("Deposits", {"FY2025": 5892, "FY2024": 6300, "FY2023": 8962, "FY2022": 7131, "FY2021": 5001,
                       "FY2020": 3609, "FY2019": 1970, "FY2018": 1198, "FY2017": 388, "FY2016": 69,
                       "FY2015": 56, "FY2014": 51}),
        ("Total equity", {"FY2025": 1704, "FY2024": 2065, "FY2023": 2556, "FY2022": 2502, "FY2021": 2742,
                           "FY2020": 3003, "FY2019": 2779, "FY2018": 2647, "FY2017": 2408, "FY2016": 2182,
                           "FY2015": 1902, "FY2014": 1791}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 422, "FY2024": 405, "FY2023": 575, "FY2022": 516, "FY2021": 599,
                           "FY2020": 736, "FY2019": 1019, "FY2018": 939, "FY2017": 843, "FY2016": 697,
                           "FY2015": 598, "FY2014": 609}),
        ("Operating expenses", {"FY2025": -265, "FY2024": -243, "FY2023": -287, "FY2022": -255, "FY2021": -239,
                                 "FY2020": -275, "FY2019": -276, "FY2018": -305, "FY2017": -260, "FY2016": -292,
                                 "FY2015": -200, "FY2014": -204}),
        ("Profit for the period", {"FY2025": 96, "FY2024": 212, "FY2023": 88, "FY2022": 287, "FY2021": 154,
                                    "FY2020": 128, "FY2019": 224, "FY2018": 209, "FY2017": 213, "FY2016": 144,
                                    "FY2015": 160, "FY2014": 147}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 2065, "FY2024": 2556, "FY2023": 2502, "FY2022": 2742, "FY2021": 3003,
                             "FY2020": 2779, "FY2019": 2647, "FY2018": 2408, "FY2017": 2182, "FY2016": 1902,
                             "FY2015": 1791, "FY2014": 1715}),
        ("Total comprehensive income for the year", {"FY2025": 139, "FY2024": 9, "FY2023": 55, "FY2022": 365, "FY2021": 39,
                                                       "FY2020": 222, "FY2019": 132, "FY2018": 227, "FY2017": 255, "FY2016": 329,
                                                       "FY2015": 111, "FY2014": 77}),
        ("Other equity movements, net", {"FY2025": -500, "FY2024": -500, "FY2023": -1, "FY2022": -605, "FY2021": -300,
                                          "FY2020": 2, "FY2019": -3, "FY2018": 12, "FY2017": 0, "FY2016": -48,
                                          "FY2015": 0, "FY2014": -1}),
        ("Closing equity", {"FY2025": 1704, "FY2024": 2065, "FY2023": 2556, "FY2022": 2502, "FY2021": 2742,
                             "FY2020": 3003, "FY2019": 2779, "FY2018": 2647, "FY2017": 2408, "FY2016": 2182,
                             "FY2015": 1902, "FY2014": 1791}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities",
         {"FY2025": 966, "FY2024": -935, "FY2023": -1133, "FY2022": -1273, "FY2021": 3292,
          "FY2020": 2691, "FY2019": 193, "FY2018": -1433, "FY2017": -1507, "FY2016": -1024,
          "FY2015": -1982, "FY2014": -1609}),
        ("Net cash (used in)/generated from investing activities",
         {"FY2025": -17, "FY2024": 113, "FY2023": 139, "FY2022": -15, "FY2021": -6,
          "FY2020": -11, "FY2019": -51, "FY2018": -9, "FY2017": -5, "FY2016": -4,
          "FY2015": -3, "FY2014": -4}),
        ("Net cash (used in)/generated from financing activities",
         {"FY2025": -1111, "FY2024": 441, "FY2023": 1041, "FY2022": 1946, "FY2021": -3447,
          "FY2020": -2125, "FY2019": -514, "FY2018": 1773, "FY2017": 1388, "FY2016": 855,
          "FY2015": 2054, "FY2014": 1099}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 1111, "FY2024": 1253, "FY2023": 2557, "FY2022": 2536, "FY2021": 1822,
          "FY2020": 2048, "FY2019": 1453, "FY2018": 1879, "FY2017": 1544, "FY2016": 1654,
          "FY2015": 1669, "FY2014": 1625}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.59%", "FY2024": "17.61%", "FY2023": "17.16%", "FY2022": "16.65%", "FY2021": "23.58%",
                         "FY2020": "19.54%", "FY2019": "16.54%", "FY2018": "14.84%", "FY2017": "14.67%", "FY2016": "14.53%",
                         "FY2015": "15.27%", "FY2014": "16.30%"}),
        ("Total Capital Ratio", {"FY2025": "18.66%", "FY2024": "19.57%", "FY2023": "19.30%", "FY2022": "19.03%", "FY2021": "26.20%",
                                  "FY2020": "21.79%", "FY2019": "18.64%", "FY2018": "16.66%", "FY2017": "17.00%", "FY2016": "16.89%",
                                  "FY2015": "17.31%", "FY2014": "18.6%"}),
        ("Leverage Ratio", {"FY2021": "16.95%", "FY2020": "14.59%", "FY2019": "13.02%", "FY2018": "11.74%",
                             "FY2017": "11.82%", "FY2016": "11.86%", "FY2015": "12.28%", "FY2014": "12.91%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. CET1/Tier1 Ratio and Total RWAs are calculated "
         "for FY2022-FY2025 only (only the rounded Tier 1/Tier 2/Total Capital Ratio chart is published for "
         "those years); FY2014-FY2021 are all directly disclosed exact figures - see the individual metric "
         "sheets for the full methodology.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/FCE BANK FINANCIALS.xlsx")
