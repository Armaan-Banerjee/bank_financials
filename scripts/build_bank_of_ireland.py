import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016",
         "FY2015", "FY2014", "FY2013"]
Y_CORE = YEARS[:YEARS.index('FY2014') + 1]  # HD-072/075/079: FY2014-floor default for Pillar 3/Asset Quality/RWA Breakdown/Overview
  # most recent first, all 12mo to 31 Dec
# NOTE (HD-072): FY2013 added for the 4 statutory-statement sheets only (Balance Sheet, Profit & Loss, Statement
# of Changes in Equity, Cash Flow Statement) - Pillar 3/Asset Quality/RWA Breakdown remain capped at FY2014 (see
# those sheets' own build calls below, which simply have no FY2013 entries).

AR2025_URL = "https://www.bankofirelanduk.com/app/uploads/annual-report_2025_boi-uk.pdf"
AR2024_URL = "https://investorrelations.bankofireland.com/app/uploads/Annual-Report-UK-2024-web-version.pdf"
AR2023_URL = "https://investorrelations.bankofireland.com/app/uploads/BOI-UKPLC-2023-Annual-Report.pdf"
AR2022_URL = "https://www.bankofirelanduk.com/app/uploads/BOI-UK-Annual-Report-2022.pdf"
AR2021_URL = "https://www.bankofirelanduk.com/app/uploads/2017/04/Annual-Report-UK-2021.pdf"
# FY2014-FY2020: bank's own site archive doesn't reach these years; sourced via Companies House filing history
# (Bank of Ireland (UK) Plc, CH number 07022885) - each is that year's "Group of companies' accounts" filing.
AR2020_URL = "https://find-and-update.company-information.service.gov.uk/company/07022885/filing-history"
AR2019_URL = "https://find-and-update.company-information.service.gov.uk/company/07022885/filing-history"
AR2018_URL = "https://find-and-update.company-information.service.gov.uk/company/07022885/filing-history"
AR2017_URL = "https://find-and-update.company-information.service.gov.uk/company/07022885/filing-history"
AR2016_URL = "https://find-and-update.company-information.service.gov.uk/company/07022885/filing-history"
AR2015_URL = "https://find-and-update.company-information.service.gov.uk/company/07022885/filing-history"
AR2014_URL = "https://find-and-update.company-information.service.gov.uk/company/07022885/filing-history"
# FY2013: real statutory floor per HD-004/HD-072 - "Group of companies' accounts made up to 31 December 2013",
# filed at Companies House 14 Apr 2014 (document MzA5ODE5MzA0NWFkaXF6a2N4, 164 pages), verified directly.
AR2013_URL = "https://find-and-update.company-information.service.gov.uk/company/07022885/filing-history"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank of Ireland (UK) Plc (Companies House 07022885, FRN 512956) is a wholly owned subsidiary of "
    "Bank of Ireland Group plc (Ireland). Figures throughout are the CONSOLIDATED GROUP basis (not the standalone "
    "parent-only 'Bank' accounts, which separately take the FRS 101/IAS 7 cash-flow-statement exemption available "
    "to a qualifying entity - the consolidated Group accounts do not take that exemption and contain a full "
    "Consolidated cash flow statement every year). Bank of Ireland (UK) Plc stopped publishing a standalone Pillar "
    "3 disclosure document after the 2020 financial year; from FY2021 onward, its capital/leverage/liquidity/MREL "
    "ratios are instead disclosed directly within the Annual Report's Risk Management Report ('2.2 Funding and "
    "liquidity risk' and '3 Capital management' sections), which is what is cited below. Those sections give a full "
    "capital composition table (CET1/Tier 1/Total capital/RWA/leverage exposure) and headline LCR/NSFR/MREL ratios, "
    "but - unlike a formal Pillar 3 KM1 template - do not publish the underlying £m components behind the LCR "
    "(HQLA, net cash outflows) or NSFR (available/required stable funding) ratios, or a numeric MREL resources "
    "breakdown; only the headline percentages are available for FY2021-FY2025.\n\n"
    "HISTORICAL NOTE (FY2014-FY2020, added on extension to FY2014): FY2014-FY2020 Annual Report & Accounts were "
    "sourced via Companies House filing history (scanned/OCR'd), not the bank's own website, whose archive does not "
    "reach these years. A genuine 2012-2014 asset transfer from the Irish parent to this UK subsidiary (part of "
    "ring-fencing/subsidiarisation of the Group's UK business) explains a real deleveraging in the balance sheet - "
    "Total assets fell from £52.3bn (1 Jan 2013, restated) to £35.9bn (31 Dec 2013, restated) to £29.2bn (31 Dec "
    "2014) - this is a disclosed structural change, not a data gap. FY2019 saw a major share-capital reduction "
    "(£851m to £255m, approved by the UK High Court, with the released amount and the capital redemption reserve "
    "fund both transferred into retained earnings) followed by a FY2020 share repurchase (£253m total, split "
    "£58m/£195m between share capital and retained earnings) - both are real capital-structure events, reflected "
    "in the Statement of Changes in Equity. IFRS 9 transition at 1 January 2018 zeroed the 'Available for sale "
    "reserve' equity component (replaced by 'Debt securities at amortised cost' on the Balance Sheet) and the "
    "'Revaluation reserve - property' equity component and the Income Statement's 'Net leasing income' line both "
    "first appear from FY2017 (genuine new disclosures/business lines, not gaps in earlier years). Pre-2018 "
    "years use IAS 39 loan-quality categories (neither past due nor impaired / past due but not impaired / "
    "impaired) rather than IFRS 9 stages - see the Asset Quality sheet's own note. 'Common equity tier 1' Basel "
    "III/CRD IV terminology was already in use from FY2014 (the transitional CRD IV regime took effect 1 January "
    "2014), so no Basel II-era terminology substitution was needed for capital ratios; LCR was not yet in force "
    "before 1 October 2015 (FY2014 shown blank) and MREL was not disclosed as a ratio before FY2020.\n\n"
    "FY2013 ADDENDUM (HD-072, statutory statements only): FY2013 was added to the Balance Sheet/Profit & Loss/"
    "Statement of Changes in Equity/Cash Flow Statement sheets only - Pillar 3, Asset Quality and RWA Breakdown "
    "remain capped at FY2014, since Basel III/CRD IV Pillar 3 disclosures are not meaningfully comparable pre-2014. "
    "FY2013's own Annual Report (Companies House filing, 164 pages) uses a materially simpler balance sheet/income "
    "statement presentation than FY2014+ (no separate 'Property, plant and equipment', 'Debt securities in issue', "
    "'Lease liabilities' or 'Other equity instruments' lines existed yet; a single 'Cash and cash equivalents' "
    "balance-sheet caption of £4,125m is shown here under 'Cash and balances at central banks' for column "
    "consistency - this is NOT the same figure as the Cash Flow Statement's £5,918m closing cash and cash "
    "equivalents, which uses a broader definition including short-term bank placements, same as every other year). "
    "The FY2013 Annual Report's own closing Statement of Changes in Equity balance (Retained earnings £(1)m, Total "
    "equity £1,533m at 31 December 2013) does NOT tie exactly to the existing 'Balance at 1 January 2014' row "
    "carried in the Statement of Changes in Equity sheet (Retained earnings £14m, Total equity £1,548m, a £15m "
    "gap) - both figures are transcribed exactly as each year's own primary source states (per this project's "
    "'each year's own figures, not restated comparatives' convention); the £15m difference is presumed to reflect "
    "a prior-year adjustment first disclosed in the FY2014 Annual Report's own comparative column, which this "
    "workbook does not have independent access to confirm. The FY2013 Cash Flow Statement's closing cash and cash "
    "equivalents (£5,918m) DOES tie exactly to the FY2014 Cash Flow Statement's opening balance, with no gap - "
    "the cash-flow chain reconciles cleanly across the FY2013/FY2014 boundary even though the equity chain does not."
)

BASIS_NOTE = (
    "RATIO BASIS NOTE: CET1 ratio and Leverage ratio are quoted exactly as stated in each year's Annual Report, on "
    "the 'fully loaded' basis (i.e. excluding IFRS 9 transitional relief, which fully phased out at 31 December "
    "2024) throughout, for comparability across years. FY2024 and FY2025 Total Capital ratios are also explicitly "
    "stated on a fully loaded basis in the source; for FY2021-FY2023 only a 'regulatory' (IFRS 9 transitional) "
    "basis Total Capital ratio was stated as a headline figure, so the fully loaded Total Capital ratios shown for "
    "those years are calculated here as disclosed fully-loaded Total capital / disclosed RWA (both audited "
    "figures from the same capital composition table) rather than quoted verbatim - cross-checked and consistent "
    "with the FY2024/FY2025 years where both the calculated and stated fully-loaded figures are available. Tier 1 "
    "ratio is not quoted as a percentage in any year's Annual Report (only Tier 1 capital £m and RWA £m); it is "
    "calculated the same way (Tier 1 capital / RWA) for all 5 years.\n\n"
    "FY2014-FY2020 ADDENDUM: these years' Annual Reports label the two bases 'CRD IV Transitional' and 'Fully "
    "Loaded' (FY2014-FY2017) or 'Regulatory' and 'Fully loaded' (FY2018-FY2020) rather than FY2021+'s wording, but "
    "the same fully-loaded CET1 capital/ratio and Leverage ratio are used here for consistency across all 12 "
    "years. Tier 1 ratio and (for FY2019-FY2020, where only a transitional/regulatory-basis Total Capital ratio "
    "was quoted as text) Total Capital ratio are calculated from the disclosed fully-loaded £m figures the same "
    "way as FY2021+. From May 2015 the Group's capital restructure made the transitional and fully loaded bases "
    "identical, so FY2015 onward the two bases already coincide for CET1/Tier 1 capital; FY2014 is the only year "
    "where transitional and fully loaded CET1 capital genuinely differ (£1,236m vs £1,239m)."
)

REGULATORY_NOTE = (
    "REGULATORY NOTE: On 19 February 2026 the Payment Systems Regulator (not the PRA) fined Bank of Ireland (UK) "
    "Plc £3.78m for a 14-month delay implementing Confirmation of Payee send functionality (compliant from January "
    "2025). This relates to payment-systems conduct, not capital/liquidity adequacy, and has no bearing on the "
    "figures in this workbook."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank of Ireland (UK) Plc consolidated Group cash flow statement, £m:\n"
    f"FY2025: Bank of Ireland (UK) Annual Report 2025, p.80 (Consolidated cash flow statement) - {AR2025_URL}\n"
    f"FY2024: Bank of Ireland (UK) Annual Report 2024, p.85 (Consolidated cash flow statement) - {AR2024_URL}\n"
    f"FY2023: Bank of Ireland (UK) plc Annual Report 2023, p.79 (Consolidated cash flow statement) - {AR2023_URL}\n"
    f"FY2022: Bank of Ireland (UK) plc Annual Report 2022, p.81 (Consolidated cash flow statement) - {AR2022_URL}\n"
    f"FY2021: Bank of Ireland (UK) plc Annual Report 2021, p.87 (Consolidated cash flow statement) - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020 (Companies House filing), p.85 (Consolidated cash flow statement) - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019 (Companies House filing), p.77-78 (Consolidated cash flow statement) - {AR2019_URL}\n"
    f"FY2018: Annual Report 2018 (Companies House filing), p.74-75 (Consolidated cash flow statement) - {AR2018_URL}\n"
    f"FY2017: Annual Report 2017 (Companies House filing), p.82-83 (Consolidated cash flow statement) - {AR2017_URL}\n"
    f"FY2016: Annual Report 2016 (Companies House filing), p.94-95 (Consolidated cash flow statement) - {AR2016_URL}\n"
    f"FY2015: Annual Report 2015 (Companies House filing), p.91-92 (Consolidated cash flow statement) - {AR2015_URL}\n"
    f"FY2014: Annual Report 2014 (Companies House filing), p.80-81 (Consolidated cash flow statement) - {AR2014_URL}\n"
    f"FY2013: Annual Report 2013 (Companies House filing), p.67-68 (Consolidated cash flow statement) - {AR2013_URL}\n"
    "Note: each year's own report was used for its own column (all cross-checked against the following year's "
    "comparative column, which matched exactly in every case). Operating-activity adjustment line items vary "
    "slightly year to year (e.g. 'Net change in fair value changes due to interest rate risk of the hedged items "
    "in portfolio hedges' appears only in FY2023/FY2024); blank cells indicate that year's report did not include "
    "that specific line. Section totals and cash/cash equivalents figures are consistent and comparable across all "
    "years shown. FY2013's own report includes two items with no equivalent in any later year's report - 'Issue of "
    "share capital' (£35m, financing) and 'Disposal of intangible assets' (£2m, investing) - shown as their own new "
    "rows rather than folded elsewhere, since no comparable existing row fits. FY2013's closing cash and cash "
    "equivalents (£5,918m) ties exactly to FY2014's opening balance (£5,918m, unchanged from before this ticket) - "
    "the cash-flow chain reconciles cleanly across the FY2013/FY2014 boundary (contrast the Statement of Changes in "
    "Equity sheet, where the equivalent FY2013/FY2014 boundary does NOT reconcile exactly - see that sheet's own "
    "source note).\n\n"
    + ENTITY_NOTE + "\n\n" + REGULATORY_NOTE
)


def p3_sources(page):
    urls = {"FY2025": AR2025_URL, "FY2024": AR2024_URL, "FY2023": AR2023_URL, "FY2022": AR2022_URL, "FY2021": AR2021_URL,
            "FY2020": AR2020_URL, "FY2019": AR2019_URL, "FY2018": AR2018_URL, "FY2017": AR2017_URL, "FY2016": AR2016_URL,
            "FY2015": AR2015_URL, "FY2014": AR2014_URL}
    names = {
        "FY2025": "Bank of Ireland (UK) Annual Report 2025",
        "FY2024": "Bank of Ireland (UK) Annual Report 2024",
        "FY2023": "Bank of Ireland (UK) plc Annual Report 2023",
        "FY2022": "Bank of Ireland (UK) plc Annual Report 2022",
        "FY2021": "Bank of Ireland (UK) plc Annual Report 2021",
        "FY2020": "Bank of Ireland (UK) plc Annual Report 2020 (Companies House filing)",
        "FY2019": "Bank of Ireland (UK) plc Annual Report 2019 (Companies House filing)",
        "FY2018": "Bank of Ireland (UK) plc Annual Report 2018 (Companies House filing)",
        "FY2017": "Bank of Ireland (UK) plc Annual Report 2017 (Companies House filing)",
        "FY2016": "Bank of Ireland (UK) plc Annual Report 2016 (Companies House filing)",
        "FY2015": "Bank of Ireland (UK) plc Annual Report 2015 (Companies House filing)",
        "FY2014": "Bank of Ireland (UK) plc Annual Report 2014 (Companies House filing)",
    }
    lines = ["Sources - Bank of Ireland (UK) Plc consolidated Group basis, from the Risk Management Report / "
             "Financial Review ('2.2 Funding and liquidity risk' / '3 Capital management' sections; FY2014-FY2020 "
             "from the equivalent 'Regulatory capital' / 'Capital management' sections):"]
    for y in YEARS:
        if y in page:
            lines.append(f"{y}: {names[y]}, p.{page[y]} - {urls[y]}")
    return "\n".join(lines) + "\n\n" + BASIS_NOTE


bw = BankWorkbook(bank_name="Bank of Ireland (UK) Plc", years=Y_CORE, year_label={y: y for y in YEARS}, header_color="00594F")

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
BALANCE_SHEET_SOURCES = (
    "Sources - Bank of Ireland (UK) Plc consolidated Group Balance sheet, £m, each year from its own primary "
    "report:\n"
    f"FY2025: Annual Report 2025, p.77 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.82 - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, p.28 (printed) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, p.26 (printed) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, p.85 - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020 (Companies House filing), p.83 - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019 (Companies House filing), p.77 - {AR2019_URL}\n"
    f"FY2018: Annual Report 2018 (Companies House filing), p.72 - {AR2018_URL}\n"
    f"FY2017: Annual Report 2017 (Companies House filing), p.80 - {AR2017_URL}\n"
    f"FY2016: Annual Report 2016 (Companies House filing), p.92 - {AR2016_URL}\n"
    f"FY2015: Annual Report 2015 (Companies House filing), p.89 - {AR2015_URL}\n"
    f"FY2014: Annual Report 2014 (Companies House filing), p.78 - {AR2014_URL}\n"
    f"FY2013: Annual Report 2013 (Companies House filing), p.65 (Consolidated Balance Sheet) - {AR2013_URL}\n"
    "Note: 'Fair value changes due to interest rate risk of hedged items in portfolio hedges' is shown as its own "
    "line FY2022-FY2025 (a voluntary presentation change adopted in the FY2022 report); FY2021's own report embeds "
    "it within Loans and advances to customers / Customer accounts instead - FY2021's own gross loan and customer-"
    "account figures are ~£71m/£1m lower than the FY2022 report's restated FY2021 comparative column as a result. "
    "Each year's own figures are used here (not restated comparatives) per project convention; both totals still "
    "reconcile internally. Current tax assets/Assets classified as held for sale are blank where not separately "
    "disclosed that year. FY2014-FY2017 report 'Available for sale financial assets' where FY2018+ report 'Debt "
    "securities at amortised cost' instead (IFRS 9 transition, 1 Jan 2018); 'Interest in joint venture' is labelled "
    "'Interest in joint venture' throughout. FY2014-FY2016 do not separately disclose 'Investment in subsidiaries' "
    "or 'Lease liabilities' (both blank, genuinely not yet applicable/disclosed - IFRS 16 leases were adopted "
    "later). Assets classified as held for sale (£539m) is a one-off FY2018-only disclosed item; the FY2014 "
    "figures reflect a real 2012-2014 deleveraging following an asset transfer from the Irish parent - see the "
    "Cash Flow Statement sheet's Entity Note. FY2013's own report predates the FY2014-2017 'Available for sale "
    "financial assets' caption split from cash and does not separately disclose 'Property, plant and equipment' as "
    "a balance sheet line (blank/embedded in Other assets, immaterial) - see the Cash Flow Statement sheet's Entity "
    "Note for the FY2013 addendum on caption differences and the equity roll-forward discontinuity at the FY2013/"
    "FY2014 boundary.\n\n" + ENTITY_NOTE
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 2306, "FY2024": 2069, "FY2023": 2213, "FY2022": 2239, "FY2021": 3456, "FY2020": 2050, "FY2019": 2134, "FY2018": 2567, "FY2017": 1836, "FY2016": 1172, "FY2015": 3269, "FY2014": 2964, "FY2013": 4125}),
    ("DATA", "Items in the course of collection from other banks", {"FY2025": 96, "FY2024": 67, "FY2023": 71, "FY2022": 79, "FY2021": 101, "FY2020": 111, "FY2019": 144, "FY2018": 168, "FY2017": 192, "FY2016": 131, "FY2015": 147, "FY2014": 276, "FY2013": 182}),
    ("DATA", "Derivative financial instruments", {"FY2025": 70, "FY2024": 179, "FY2023": 283, "FY2022": 379, "FY2021": 88, "FY2020": 53, "FY2019": 41, "FY2018": 32, "FY2017": 27, "FY2016": 55, "FY2015": 45, "FY2014": 59, "FY2013": 11}),
    ("DATA", "Loans and advances to banks", {"FY2025": 1157, "FY2024": 1171, "FY2023": 1248, "FY2022": 1461, "FY2021": 1574, "FY2020": 1672, "FY2019": 2158, "FY2018": 2348, "FY2017": 2764, "FY2016": 3369, "FY2015": 3949, "FY2014": 6312, "FY2013": 12824}),
    ("DATA", "Debt securities at amortised cost", {"FY2025": 881, "FY2024": 476, "FY2023": 489, "FY2022": 528, "FY2021": 798, "FY2020": 922, "FY2019": 846, "FY2018": 915}),
    ("DATA", "Available for sale financial assets", {"FY2017": 1008, "FY2016": 1140, "FY2015": 956, "FY2014": 991, "FY2013": 482}),
    ("DATA", "Fair value changes due to interest rate risk of hedged items in portfolio hedges", {"FY2025": 41, "FY2024": -58, "FY2023": -100, "FY2022": -276}),
    ("DATA", "Loans and advances to customers", {"FY2025": 14704, "FY2024": 14191, "FY2023": 14148, "FY2022": 14018, "FY2021": 16325, "FY2020": 21300, "FY2019": 21200, "FY2018": 19703, "FY2017": 19997, "FY2016": 19821, "FY2015": 19255, "FY2014": 18301, "FY2013": 17928}),
    ("DATA", "Interest in joint venture", {"FY2025": 60, "FY2024": 61, "FY2023": 67, "FY2022": 71, "FY2021": 47, "FY2020": 49, "FY2019": 64, "FY2018": 62, "FY2017": 61, "FY2016": 61, "FY2015": 60, "FY2014": 60, "FY2013": 55}),
    ("DATA", "Intangible assets and goodwill", {"FY2025": 24, "FY2024": 25, "FY2023": 26, "FY2022": 28, "FY2021": 32, "FY2020": 36, "FY2019": 48, "FY2018": 54, "FY2017": 61, "FY2016": 25, "FY2015": 30, "FY2014": 39, "FY2013": 46}),
    ("DATA", "Property, plant and equipment", {"FY2025": 272, "FY2024": 244, "FY2023": 215, "FY2022": 174, "FY2021": 143, "FY2020": 126, "FY2019": 138, "FY2018": 117, "FY2017": 104, "FY2016": 8, "FY2015": 8, "FY2014": 0}),
    ("DATA", "Other assets", {"FY2025": 102, "FY2024": 74, "FY2023": 65, "FY2022": 52, "FY2021": 42, "FY2020": 59, "FY2019": 111, "FY2018": 102, "FY2017": 106, "FY2016": 109, "FY2015": 132, "FY2014": 92, "FY2013": 110}),
    ("DATA", "Current tax assets", {"FY2025": 67, "FY2024": 23, "FY2021": 8, "FY2013": 4}),
    ("DATA", "Deferred tax assets", {"FY2025": 71, "FY2024": 75, "FY2023": 96, "FY2022": 108, "FY2021": 77, "FY2020": 23, "FY2019": 41, "FY2018": 85, "FY2017": 71, "FY2016": 69, "FY2015": 86, "FY2014": 105, "FY2013": 128}),
    ("DATA", "Retirement benefit asset", {"FY2025": 14, "FY2024": 14, "FY2023": 11, "FY2022": 10, "FY2021": 13, "FY2020": 10, "FY2019": 9, "FY2018": 8, "FY2017": 8, "FY2016": 0, "FY2015": 2, "FY2014": 1}),
    ("DATA", "Assets classified as held for sale", {"FY2021": 1, "FY2018": 539}),
    ("TOTAL", "Total assets", {"FY2025": 19865, "FY2024": 18611, "FY2023": 18832, "FY2022": 18871, "FY2021": 22705, "FY2020": 26419, "FY2019": 26934, "FY2018": 26700, "FY2017": 26235, "FY2016": 25960, "FY2015": 27939, "FY2014": 29209, "FY2013": 35895}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 2687, "FY2024": 2422, "FY2023": 3237, "FY2022": 3107, "FY2021": 3399, "FY2020": 4202, "FY2019": 3500, "FY2018": 3152, "FY2017": 3561, "FY2016": 2691, "FY2015": 2606, "FY2014": 5234, "FY2013": 11660}),
    ("DATA", "Customer accounts", {"FY2025": 12765, "FY2024": 12223, "FY2023": 11815, "FY2022": 12222, "FY2021": 15753, "FY2020": 18256, "FY2019": 19075, "FY2018": 19769, "FY2017": 18961, "FY2016": 19475, "FY2015": 21574, "FY2014": 20180, "FY2013": 20857}),
    ("DATA", "Fair value changes due to interest rate risk of hedged items in portfolio hedges", {"FY2025": -23, "FY2024": -87, "FY2023": -44, "FY2022": -130}),
    ("DATA", "Items in the course of transmission to other banks", {"FY2025": 127, "FY2024": 63, "FY2023": 86, "FY2022": 63, "FY2021": 62, "FY2020": 67, "FY2019": 95, "FY2018": 106, "FY2017": 108, "FY2016": 85, "FY2015": 74, "FY2014": 221, "FY2013": 94}),
    ("DATA", "Derivative financial instruments", {"FY2025": 223, "FY2024": 293, "FY2023": 326, "FY2022": 328, "FY2021": 65, "FY2020": 114, "FY2019": 59, "FY2018": 43, "FY2017": 65, "FY2016": 102, "FY2015": 56, "FY2014": 64, "FY2013": 11}),
    ("DATA", "Debt securities in issue", {"FY2025": 743, "FY2024": 514, "FY2023": 549, "FY2022": 379, "FY2021": 448, "FY2020": 511, "FY2019": 607}),
    ("DATA", "Current tax liabilities", {"FY2025": 0, "FY2024": 16, "FY2023": 6, "FY2022": 4, "FY2021": 2, "FY2020": 3, "FY2019": 3, "FY2018": 4, "FY2017": 5, "FY2016": 6, "FY2015": 2, "FY2014": 2, "FY2013": 0}),
    ("DATA", "Other liabilities", {"FY2025": 971, "FY2024": 1023, "FY2023": 1001, "FY2022": 1037, "FY2021": 1010, "FY2020": 1137, "FY2019": 1272, "FY2018": 1318, "FY2017": 1233, "FY2016": 1200, "FY2015": 1175, "FY2014": 1074, "FY2013": 1058}),
    ("DATA", "Lease liabilities", {"FY2025": 14, "FY2024": 14, "FY2023": 16, "FY2022": 12, "FY2021": 15, "FY2020": 19, "FY2019": 20}),
    ("DATA", "Provisions", {"FY2025": 377, "FY2024": 159, "FY2023": 8, "FY2022": 9, "FY2021": 14, "FY2020": 15, "FY2019": 30, "FY2018": 7, "FY2017": 13, "FY2016": 16, "FY2015": 13, "FY2014": 9, "FY2013": 24}),
    ("DATA", "Loss allowance provision on loan commitments and financial guarantees", {"FY2025": 6, "FY2024": 4, "FY2023": 3, "FY2022": 5, "FY2021": 4, "FY2020": 4, "FY2019": 3, "FY2018": 7}),
    ("DATA", "Subordinated liabilities", {"FY2025": 190, "FY2024": 190, "FY2023": 190, "FY2022": 190, "FY2021": 190, "FY2020": 290, "FY2019": 290, "FY2018": 290, "FY2017": 290, "FY2016": 335, "FY2015": 335, "FY2014": 658, "FY2013": 658}),
    ("TOTAL", "Total liabilities", {"FY2025": 18080, "FY2024": 16834, "FY2023": 17193, "FY2022": 17226, "FY2021": 20962, "FY2020": 24618, "FY2019": 24954, "FY2018": 24696, "FY2017": 24236, "FY2016": 23910, "FY2015": 25835, "FY2014": 27442, "FY2013": 34362}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 122, "FY2024": 122, "FY2023": 122, "FY2022": 122, "FY2021": 122, "FY2020": 197, "FY2019": 255, "FY2018": 851, "FY2017": 851, "FY2016": 851, "FY2015": 851, "FY2014": 1151, "FY2013": 1151}),
    ("DATA", "Retained earnings", {"FY2025": 1162, "FY2024": 1171, "FY2023": 1049, "FY2022": 1049, "FY2021": 1083, "FY2020": 957, "FY2019": 1149, "FY2018": 279, "FY2017": 254, "FY2016": 296, "FY2015": 374, "FY2014": 186, "FY2013": -1}),
    ("DATA", "Other reserves", {"FY2025": 351, "FY2024": 334, "FY2023": 318, "FY2022": 324, "FY2021": 388, "FY2020": 347, "FY2019": 276, "FY2018": 574, "FY2017": 594, "FY2016": 603, "FY2015": 579, "FY2014": 430, "FY2013": 383}),
    ("DATA", "Other equity instruments", {"FY2025": 150, "FY2024": 150, "FY2023": 150, "FY2022": 150, "FY2021": 150, "FY2020": 300, "FY2019": 300, "FY2018": 300, "FY2017": 300, "FY2016": 300, "FY2015": 300}),
    ("TOTAL", "Total equity attributable to owners of the Bank", {"FY2025": 1785, "FY2024": 1777, "FY2023": 1639, "FY2022": 1645, "FY2021": 1743, "FY2020": 1801, "FY2019": 1980, "FY2018": 2004, "FY2017": 1999, "FY2016": 2050, "FY2015": 2104, "FY2014": 1767, "FY2013": 1533}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 19865, "FY2024": 18611, "FY2023": 18832, "FY2022": 18871, "FY2021": 22705, "FY2020": 26419, "FY2019": 26934, "FY2018": 26700, "FY2017": 26235, "FY2016": 25960, "FY2015": 27939, "FY2014": 29209, "FY2013": 35895}),
]

bw.add_balance_sheet_sheet(
    title="Bank of Ireland (UK) Plc — Consolidated Statement of Financial Position",
    subtitle="Consolidated Group basis, £m. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=78,
    source_height=180,
    unit_suffix=" (£m)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
INCOME_STATEMENT_SOURCES = (
    "Sources - Bank of Ireland (UK) Plc consolidated Group Income statement / Statement of other comprehensive "
    "income, £m, each year from its own primary report:\n"
    f"FY2025: Annual Report 2025, p.75-76 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.80-81 - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, p.76 (printed) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, p.78 (printed) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, p.84 - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020 (Companies House filing), p.82 - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019 (Companies House filing), p.76 - {AR2019_URL}\n"
    f"FY2018: Annual Report 2018 (Companies House filing), p.71 - {AR2018_URL}\n"
    f"FY2017: Annual Report 2017 (Companies House filing), p.79, cross-checked against Annual Report 2018's clean "
    f"FY2017 comparative column (own-report FY2017 OCR was internally inconsistent on PBT) - {AR2017_URL}\n"
    f"FY2016: Annual Report 2016 (Companies House filing), p.94 - {AR2016_URL}\n"
    f"FY2015: Annual Report 2015 (Companies House filing), p.91 - {AR2015_URL}\n"
    f"FY2014: Annual Report 2014 (Companies House filing), p.77 - {AR2014_URL}\n"
    f"FY2013: Annual Report 2013 (Companies House filing), p.64 (Consolidated Income Statement / Consolidated "
    f"Statement of Other Comprehensive Income) - {AR2013_URL}\n"
    "Note: minor one-off gains (profit on disposal of PP&E/business activities/financial assets) are combined into "
    "a single 'Other gains, net' row since none is consistently disclosed as its own line every year; blank/0 cells "
    "reflect that year's own disclosure (0 = explicitly nil in the source, blank = line not applicable that year). "
    "All totals reconcile exactly to (Loss)/profit before taxation and Total comprehensive income. FY2014-FY2016 "
    "report a single undifferentiated 'Interest income' line (shown here in the 'effective interest method' row, "
    "with 'Other interest income' blank); FY2018 onward split out interest income on finance leases/hire purchase "
    "receivables separately (shown here folded into 'Other interest income' for comparability). 'Net leasing "
    "income' and its 'Other leasing income/expense' components are not disclosed as their own lines before FY2018 "
    "(FY2014-FY2017's small finance-lease income is embedded within the single interest/other-income totals); an "
    "'Available for sale reserve' other comprehensive income line applies only FY2014-FY2017, replaced by IFRS 9 "
    "at 1 January 2018 - see the Cash Flow Statement sheet's Entity Note. FY2013's own report predates the split "
    "of leasing income and shows a single undifferentiated 'Interest income' line and no cash flow hedge reserve "
    "in other comprehensive income that year (genuinely nil/not yet designated, not a gap).\n\n" + ENTITY_NOTE
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income calculated using the effective interest method", {"FY2025": 684, "FY2024": 796, "FY2023": 792, "FY2022": 580, "FY2021": 532, "FY2020": 564, "FY2019": 624, "FY2018": 630, "FY2017": 593, "FY2016": 762, "FY2015": 814, "FY2014": 901, "FY2013": 1101}),
    ("DATA", "Other interest income", {"FY2025": 215, "FY2024": 177, "FY2023": 131, "FY2022": 83, "FY2021": 78, "FY2020": 89, "FY2019": 82, "FY2018": 65, "FY2017": 58}),
    ("TOTAL", "Total interest income", {"FY2025": 899, "FY2024": 973, "FY2023": 923, "FY2022": 663, "FY2021": 610, "FY2020": 653, "FY2019": 706, "FY2018": 695, "FY2017": 651, "FY2016": 762, "FY2015": 814, "FY2014": 901, "FY2013": 1101}),
    ("DATA", "Interest expense", {"FY2025": -442, "FY2024": -481, "FY2023": -340, "FY2022": -108, "FY2021": -99, "FY2020": -189, "FY2019": -225, "FY2018": -187, "FY2017": -180, "FY2016": -265, "FY2015": -319, "FY2014": -400, "FY2013": -686}),
    ("TOTAL", "Net interest income", {"FY2025": 457, "FY2024": 492, "FY2023": 583, "FY2022": 555, "FY2021": 511, "FY2020": 464, "FY2019": 481, "FY2018": 508, "FY2017": 471, "FY2016": 497, "FY2015": 495, "FY2014": 501, "FY2013": 415}),
    ("DATA", "Net leasing income", {"FY2025": 24, "FY2024": 19, "FY2023": 26, "FY2022": 22, "FY2021": 14, "FY2020": 9, "FY2019": 8, "FY2018": 9}),
    ("DATA", "Other leasing income", {"FY2025": 104, "FY2024": 92, "FY2023": 80, "FY2022": 60, "FY2021": 55, "FY2020": 58, "FY2019": 54, "FY2018": 46}),
    ("DATA", "Other leasing expense", {"FY2025": -80, "FY2024": -73, "FY2023": -54, "FY2022": -38, "FY2021": -41, "FY2020": -49, "FY2019": -46, "FY2018": -37}),
    ("DATA", "Fee and commission income", {"FY2025": 31, "FY2024": 32, "FY2023": 35, "FY2022": 37, "FY2021": 57, "FY2020": 78, "FY2019": 95, "FY2018": 104, "FY2017": 114, "FY2016": 118, "FY2015": 115, "FY2014": 114, "FY2013": 118}),
    ("DATA", "Fee and commission expense", {"FY2025": -50, "FY2024": -67, "FY2023": -91, "FY2022": -88, "FY2021": -50, "FY2020": -56, "FY2019": -89, "FY2018": -110, "FY2017": -115, "FY2016": -121, "FY2015": -118, "FY2014": -108, "FY2013": -112}),
    ("DATA", "Net trading income", {"FY2025": 14, "FY2024": 20, "FY2023": 15, "FY2022": 7, "FY2021": 3, "FY2020": -2, "FY2019": 4, "FY2018": 5, "FY2017": -1, "FY2016": -6, "FY2015": -1, "FY2013": 0}),
    ("DATA", "Other operating income", {"FY2025": 0, "FY2024": 2, "FY2023": 3, "FY2022": 0, "FY2021": 0, "FY2020": 2, "FY2019": 2, "FY2018": 9, "FY2017": 2, "FY2016": 6, "FY2015": 1, "FY2014": 5, "FY2013": 1}),
    ("TOTAL", "Total operating income", {"FY2025": 476, "FY2024": 498, "FY2023": 571, "FY2022": 533, "FY2021": 535, "FY2020": 495, "FY2019": 501, "FY2018": 525, "FY2017": 471, "FY2016": 494, "FY2015": 492, "FY2014": 512, "FY2013": 422}),
    ("SECTION", "Expenses and impairment", {}),
    ("TOTAL", "Operating expenses", {"FY2025": -485, "FY2024": -382, "FY2023": -222, "FY2022": -247, "FY2021": -272, "FY2020": -310, "FY2019": -317, "FY2018": -351, "FY2017": -328, "FY2016": -313, "FY2015": -300, "FY2014": -287, "FY2013": -274}),
    ("TOTAL", "Operating profit/(loss) before impairment charges on financial assets", {"FY2025": -9, "FY2024": 116, "FY2023": 349, "FY2022": 286, "FY2021": 263, "FY2020": 185, "FY2019": 184, "FY2018": 174, "FY2017": 143, "FY2016": 181, "FY2015": 192, "FY2014": 225, "FY2013": 148}),
    ("DATA", "Net impairment (losses)/gains on financial instruments", {"FY2025": -25, "FY2024": 8, "FY2023": -43, "FY2022": -64, "FY2021": 54, "FY2020": -151, "FY2019": -40, "FY2018": -34, "FY2017": -26, "FY2016": -23, "FY2015": -44, "FY2014": -61, "FY2013": -125}),
    ("TOTAL", "Operating profit/(loss)", {"FY2025": -34, "FY2024": 124, "FY2023": 306, "FY2022": 222, "FY2021": 317, "FY2020": 34, "FY2019": 144, "FY2018": 140, "FY2017": 117, "FY2016": 158, "FY2015": 148, "FY2014": 164, "FY2013": 23}),
    ("DATA", "Share of profit/(loss) after tax of joint venture", {"FY2025": 22, "FY2024": 24, "FY2023": 25, "FY2022": 28, "FY2021": -2, "FY2020": -1, "FY2019": 30, "FY2018": 33, "FY2017": 34, "FY2016": 35, "FY2015": 35, "FY2014": 35, "FY2013": 34}),
    ("DATA", "Other gains, net (disposal of PP&E/business activities/financial assets)", {"FY2025": 0, "FY2024": 33, "FY2023": 0, "FY2022": 1, "FY2021": 95, "FY2020": 7, "FY2019": -19, "FY2015": 41}),
    ("TOTAL", "Profit/(loss) before taxation", {"FY2025": -12, "FY2024": 181, "FY2023": 331, "FY2022": 251, "FY2021": 410, "FY2020": 40, "FY2019": 155, "FY2018": 173, "FY2017": 151, "FY2016": 193, "FY2015": 224, "FY2014": 199, "FY2013": 57}),
    ("DATA", "Taxation credit/(charge)", {"FY2025": 11, "FY2024": -48, "FY2023": -72, "FY2022": -23, "FY2021": -12, "FY2020": -13, "FY2019": -58, "FY2018": -22, "FY2017": -21, "FY2016": -29, "FY2015": -36, "FY2014": -27, "FY2013": 4}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": -1, "FY2024": 133, "FY2023": 259, "FY2022": 228, "FY2021": 398, "FY2020": 27, "FY2019": 97, "FY2018": 151, "FY2017": 130, "FY2016": 164, "FY2015": 188, "FY2014": 172, "FY2013": 61}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Net change in cash flow hedge reserve, net of tax", {"FY2025": 17, "FY2024": 17, "FY2023": -5, "FY2022": -63, "FY2021": -35, "FY2020": 14, "FY2019": 1, "FY2018": -17, "FY2017": -9, "FY2016": 21, "FY2015": -15, "FY2014": 26}),
    ("DATA", "Net change in available for sale reserve, net of tax", {"FY2017": -1, "FY2016": 3, "FY2015": -1, "FY2014": 6, "FY2013": -4}),
    ("DATA", "Net actuarial gain/(loss) on defined benefit schemes", {"FY2025": 0, "FY2024": 1, "FY2023": 0, "FY2022": -3, "FY2021": 2, "FY2020": 0, "FY2019": 1, "FY2018": -1, "FY2017": 6, "FY2016": -3, "FY2015": 0, "FY2014": 0, "FY2013": 1}),
    ("DATA", "Net change in revaluation reserve, net of tax", {"FY2025": 0, "FY2024": -1, "FY2023": -1, "FY2022": -1, "FY2021": 1, "FY2020": -1, "FY2019": 1, "FY2018": 1, "FY2017": 1}),
    ("TOTAL", "Other comprehensive income/(expense) for the year, net of tax", {"FY2025": 17, "FY2024": 17, "FY2023": -6, "FY2022": -67, "FY2021": -32, "FY2020": 13, "FY2019": 3, "FY2018": -17, "FY2017": -2, "FY2016": 21, "FY2015": -16, "FY2014": 32, "FY2013": -3}),
    ("TOTAL", "Total comprehensive income/(loss) for the year, net of tax", {"FY2025": 16, "FY2024": 150, "FY2023": 253, "FY2022": 161, "FY2021": 366, "FY2020": 40, "FY2019": 100, "FY2018": 134, "FY2017": 128, "FY2016": 185, "FY2015": 172, "FY2014": 204, "FY2013": 58}),
]

bw.add_income_statement_sheet(
    title="Bank of Ireland (UK) Plc — Consolidated Statement of Comprehensive Income",
    subtitle="Consolidated Group basis, £m. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=78,
    source_height=180,
    unit_suffix=" (£m)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_CHANGES_SOURCES = (
    "Sources - Bank of Ireland (UK) Plc consolidated Group Statement of changes in equity, £m, each year from its "
    "own primary report (own-year 'Balance at 31 December' column used for that year's closing balances):\n"
    f"FY2021: Annual Report 2021, p.86 - {AR2021_URL}\n"
    f"FY2022: Annual Report 2022, p.80 (printed) - {AR2022_URL}\n"
    f"FY2023: Annual Report 2023, p.78 (printed) - {AR2023_URL}\n"
    f"FY2024: Annual Report 2024, p.83 - {AR2024_URL}\n"
    f"FY2025: Annual Report 2025, p.78 - {AR2025_URL}\n"
    f"FY2020: Annual Report 2020 (Companies House filing), p.84 (clean render; also carries the FY2019 comparative "
    f"column) - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019 (Companies House filing), p.73 - {AR2019_URL}\n"
    f"FY2018: Annual Report 2018 (Companies House filing), p.73 (also carries the FY2017 comparative column) - "
    f"{AR2018_URL}\n"
    f"FY2017: Annual Report 2017 (Companies House filing), p.80 (own-year detail; closing balance cross-checked "
    f"against Annual Report 2018's FY2017 comparative) - {AR2017_URL}\n"
    f"FY2016: Annual Report 2016 (Companies House filing), p.93 (also carries the FY2015 comparative column) - "
    f"{AR2016_URL}\n"
    f"FY2015: Annual Report 2015 (Companies House filing), p.79-ish (own-year detail, cross-checked against Annual "
    f"Report 2016's FY2015 comparative) - {AR2015_URL}\n"
    f"FY2014: Annual Report 2014 (Companies House filing), p.79 - {AR2014_URL}\n"
    f"FY2013: Annual Report 2013 (Companies House filing), p.66 (own-year detail, both 1 January and 31 December "
    f"2013 columns) - {AR2013_URL}\n"
    "Note: Revaluation reserve, Cash flow hedge reserve, Capital contribution and Capital redemption reserve fund "
    "are reported as 'Other reserves' sub-components in the source; Capital contribution never moves across all 5 "
    "years shown (£266m throughout) so no separate movement row is needed for it. Each year's opening balance ties "
    "exactly to the prior year's own closing balance. An 'Available for sale reserve' component (last column) "
    "existed FY2014-FY2017 only, zeroed out by the IFRS 9 transition at 1 January 2018 - see the Cash Flow "
    "Statement sheet's Entity Note; 'Revaluation reserve' and 'Capital redemption reserve fund' did not exist "
    "before FY2017 and FY2015 respectively (both genuinely blank/not-yet-applicable before those dates, not gaps). "
    "Net movement rows combine each reserve's fair-value-change and deferred-tax sub-lines into one figure, "
    "consistent with FY2021+ presentation.\n\n"
    "FY2013 ADDENDUM (HD-072): 'Balance at 31 December 2013' below is transcribed directly from the FY2013 Annual "
    "Report's own closing column (Retained earnings £(1)m, Total equity £1,533m) and ties exactly to that report's "
    "own Consolidated Balance Sheet and to the prior year's own closing balance (£1,354m at 31 December 2012, per "
    "the FY2013 Annual Report's comparative column). It does NOT tie to the very next row below, 'Balance at 1 "
    "January 2014' (Retained earnings £14m, Total equity £1,548m, a £15m gap) - that row is unchanged from before "
    "this ticket and was sourced from the FY2014 Annual Report's own opening column, which apparently carries a "
    "prior-year adjustment not disclosed in the FY2013 Annual Report itself (this workbook has no independent way "
    "to confirm the adjustment's nature). Both balances are shown exactly as each year's own primary source states, "
    "per this project's convention of not silently restating one year's figures to match another's; see the Cash "
    "Flow Statement sheet's Entity Note for the equivalent addendum, where the FY2013/FY2014 cash chain (unlike "
    "this equity chain) does tie exactly.\n\n" + ENTITY_NOTE
)

EQUITY_HEADERS = ["Share capital", "Retained earnings", "Other equity instruments", "Revaluation reserve",
                   "Cash flow hedge reserve", "Capital contribution", "Capital redemption reserve fund", "Total equity",
                   "Available for sale reserve"]

equity_changes_rows = [
    ("TOTAL", "Balance at 1 January 2013", (1116, -63, None, None, None, 300, None, 1354, 1)),
    ("DATA", "Issuance of share capital", (35, None, None, None, None, None, None, 35, None)),
    ("DATA", "Profit for the year", (None, 61, None, None, None, None, None, 61, None)),
    ("DATA", "Net actuarial gain on defined benefit schemes", (None, 1, None, None, None, None, None, 1, None)),
    ("DATA", "Available for sale reserve movement, net of tax", (None, None, None, None, None, None, None, -4, -4)),
    ("DATA", "Capital contribution during the period", (None, None, None, None, None, 86, None, 86, None)),
    ("TOTAL", "Balance at 31 December 2013", (1151, -1, None, None, None, 386, None, 1533, -3)),
    ("TOTAL", "Balance at 1 January 2014", (1151, 14, None, None, 0, 386, None, 1548, -3)),
    ("DATA", "Profit for the year", (None, 172, None, None, None, None, None, 172, None)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, 26, None, None, 26, None)),
    ("DATA", "Available for sale reserve movement, net of tax", (None, None, None, None, None, None, None, 6, 6)),
    ("DATA", "Capital contribution during the period", (None, None, None, None, None, 15, None, 15, None)),
    ("TOTAL", "Balance at 31 December 2014", (1151, 186, None, None, 26, 401, None, 1767, 3)),
    ("DATA", "Profit for the year", (None, 188, None, None, None, None, None, 188, None)),
    ("DATA", "Repurchase of preference shares", (-300, None, None, None, None, None, None, -300, None)),
    ("DATA", "Issuance of other equity instruments", (None, None, 300, None, None, None, None, 300, None)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, -15, None, None, -15, None)),
    ("DATA", "Available for sale reserve movement, net of tax", (None, None, None, None, None, None, None, -1, -1)),
    ("DATA", "Capital contribution during the period", (None, None, None, None, None, 165, None, 165, None)),
    ("DATA", "Transfer of capital contribution to capital redemption reserve fund", (None, None, None, None, None, -300, 300, 0, None)),
    ("TOTAL", "Balance at 31 December 2015", (851, 374, 300, None, 11, 266, 300, 2104, 2)),
    ("DATA", "Profit for the year", (None, 164, None, None, None, None, None, 164, None)),
    ("DATA", "Dividend on ordinary shares", (None, -220, None, None, None, None, None, -220, None)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -19, None, None, None, None, None, -19, None)),
    ("DATA", "Remeasurement of the net defined benefit pension liability", (None, -3, None, None, None, None, None, -3, None)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, 21, None, None, 21, None)),
    ("DATA", "Available for sale reserve movement, net of tax", (None, None, None, None, None, None, None, 3, 3)),
    ("TOTAL", "Balance at 31 December 2016", (851, 296, 300, None, 32, 266, 300, 2050, 5)),
    ("DATA", "Profit for the year", (None, 130, None, None, None, None, None, 130, None)),
    ("DATA", "Dividend on ordinary shares", (None, -160, None, None, None, None, None, -160, None)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -18, None, None, None, None, None, -18, None)),
    ("DATA", "Remeasurement of the net defined benefit pension liability", (None, 6, None, None, None, None, None, 6, None)),
    ("DATA", "Revaluation of property", (None, None, None, 1, None, None, None, 1, None)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, -9, None, None, -9, None)),
    ("DATA", "Available for sale reserve movement, net of tax", (None, None, None, None, None, None, None, -1, -1)),
    ("TOTAL", "Balance at 31 December 2017", (851, 254, 300, 1, 23, 266, 300, 1999, 4)),
    ("DATA", "Impact of adopting IFRS 9, net of tax", (None, -37, None, None, None, None, None, -41, -4)),
    ("DATA", "Profit for the year", (None, 151, None, None, None, None, None, 151, None)),
    ("DATA", "Dividend on ordinary shares", (None, -70, None, None, None, None, None, -70, None)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -18, None, None, None, None, None, -18, None)),
    ("DATA", "Remeasurement of the net defined benefit pension liability", (None, -1, None, None, None, None, None, -1, None)),
    ("DATA", "Revaluation of property", (None, None, None, 1, None, None, None, 1, None)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, -17, None, None, -17, None)),
    ("TOTAL", "Balance at 31 December 2018", (851, 279, 300, 2, 6, 266, 300, 2004, 0)),
    ("DATA", "Reduction in share capital transferred to retained earnings", (-596, 596, None, None, None, None, None, 0, None)),
    ("DATA", "Profit for the year", (None, 97, None, None, None, None, None, 97, None)),
    ("DATA", "Dividend on ordinary shares", (None, -100, None, None, None, None, None, -100, None)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -24, None, None, None, None, None, -24, None)),
    ("DATA", "Transferred from capital redemption reserve fund", (None, 300, None, None, None, None, -300, 0, None)),
    ("DATA", "Remeasurement of the net defined benefit pension asset", (None, 1, None, None, None, None, None, 1, None)),
    ("DATA", "Revaluation of property", (None, None, None, 1, None, None, None, 1, None)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, 1, None, None, 1, None)),
    ("TOTAL", "Balance at 31 December 2019", (255, 1149, 300, 3, 7, 266, 0, 1980, None)),
    ("DATA", "Share repurchase", (-58, -195, None, None, None, None, 58, -195, None)),
    ("DATA", "Profit for the year", (None, 27, None, None, None, None, None, 27, None)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -24, None, None, None, None, None, -24, None)),
    ("DATA", "Revaluation of property", (None, None, None, -1, None, None, None, -1, None)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, 14, None, None, 14, None)),
    ("TOTAL", "Balance at 1 January 2021", (197, 957, 300, 2, 21, 266, 58, 1801)),
    ("DATA", "Profit for the year", (None, 398, None, None, None, None, None, 398)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -25, None, None, None, None, None, -25)),
    ("DATA", "Share repurchase", (-75, -250, None, None, None, None, 75, -250)),
    ("DATA", "Remeasurement of the net defined benefit pension asset", (None, 3, None, None, None, None, None, 3)),
    ("DATA", "Repayment of other equity instruments", (None, None, -300, None, None, None, None, -300)),
    ("DATA", "Issuance of other equity instruments", (None, None, 150, None, None, None, None, 150)),
    ("DATA", "Revaluation of property", (None, None, None, 1, None, None, None, 1)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, -35, None, None, -35)),
    ("TOTAL", "Balance at 31 December 2021", (122, 1083, 150, 3, -14, 266, 133, 1743)),
    ("DATA", "Profit for the year", (None, 228, None, None, None, None, None, 228)),
    ("DATA", "Dividend on ordinary shares", (None, -250, None, None, None, None, None, -250)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -9, None, None, None, None, None, -9)),
    ("DATA", "Remeasurement of the net defined benefit pension asset", (None, -3, None, None, None, None, None, -3)),
    ("DATA", "Revaluation of property", (None, None, None, -1, None, None, None, -1)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, -63, None, None, -63)),
    ("TOTAL", "Balance at 31 December 2022", (122, 1049, 150, 2, -77, 266, 133, 1645)),
    ("DATA", "Profit for the year", (None, 259, None, None, None, None, None, 259)),
    ("DATA", "Dividend on ordinary shares", (None, -250, None, None, None, None, None, -250)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -9, None, None, None, None, None, -9)),
    ("DATA", "Revaluation of property", (None, None, None, -1, None, None, None, -1)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, -5, None, None, -5)),
    ("TOTAL", "Balance at 31 December 2023", (122, 1049, 150, 1, -82, 266, 133, 1639)),
    ("DATA", "Profit for the year", (None, 133, None, None, None, None, None, 133)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -9, None, None, None, None, None, -9)),
    ("DATA", "Remeasurement of the net defined benefit pension asset", (None, 1, None, None, None, None, None, 1)),
    ("DATA", "Other movements", (None, -3, None, None, None, None, None, -3)),
    ("DATA", "Revaluation of property", (None, None, None, -1, None, None, None, -1)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, 17, None, None, 17)),
    ("TOTAL", "Balance at 31 December 2024", (122, 1171, 150, 0, -65, 266, 133, 1777)),
    ("DATA", "(Loss) for the year", (None, -1, None, None, None, None, None, -1)),
    ("DATA", "Distribution on other equity instruments - AT1 coupon", (None, -9, None, None, None, None, None, -9)),
    ("DATA", "Other movements", (None, 1, None, None, None, None, None, 1)),
    ("DATA", "Cash flow hedge reserve movement, net of tax", (None, None, None, None, 17, None, None, 17)),
    ("TOTAL", "Balance at 31 December 2025", (122, 1162, 150, 0, -48, 266, 133, 1785)),
]

bw.add_equity_changes_sheet(
    title="Bank of Ireland (UK) Plc — Consolidated Statement of Changes in Equity",
    subtitle="Consolidated Group basis, £m; chronological, oldest to newest. See source note at bottom.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    source_height=200,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before taxation", {"FY2025": -12, "FY2024": 181, "FY2023": 331, "FY2022": 251, "FY2021": 410, "FY2020": 40, "FY2019": 155, "FY2018": 173, "FY2017": 151, "FY2016": 193, "FY2015": 224, "FY2014": 199, "FY2013": 57}),
    ("DATA", "Interest expense on subordinated liabilities and other capital instruments", {"FY2025": 28, "FY2024": 31, "FY2023": 34, "FY2022": 14, "FY2021": 17, "FY2020": 18, "FY2019": 14, "FY2018": 13, "FY2017": 24, "FY2016": 24, "FY2015": 50, "FY2014": 52, "FY2013": 52}),
    ("DATA", "Interest expense on lease liabilities", {"FY2025": 1, "FY2024": 1, "FY2023": 1, "FY2022": 1, "FY2020": 1, "FY2019": 1}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 48, "FY2024": 46, "FY2023": 34, "FY2022": 27, "FY2021": 31, "FY2020": 35, "FY2019": 38, "FY2018": 31, "FY2017": 11, "FY2016": 10, "FY2015": 12, "FY2014": 11, "FY2013": 9}),
    ("DATA", "Net impairment losses/(gains) on financial instruments", {"FY2025": 25, "FY2024": -8, "FY2023": 43, "FY2022": 64, "FY2021": -54, "FY2020": 151, "FY2019": 40, "FY2018": 34, "FY2017": 26, "FY2016": 23, "FY2015": 44, "FY2014": 61, "FY2013": 125}),
    ("DATA", "Impairment of intangible assets and goodwill", {"FY2020": 8}),
    ("DATA", "Impairment of property, plant and equipment", {"FY2020": 2}),
    ("DATA", "Profit on sale of financial assets", {"FY2024": -33}),
    ("DATA", "(Gain)/loss on disposal of financial assets", {"FY2021": -94}),
    ("DATA", "(Gain)/loss on disposal of business activities", {"FY2021": -1, "FY2020": -7, "FY2019": 19, "FY2015": -41}),
    ("DATA", "(Gain)/loss on sale of property, plant, equipment", {"FY2022": -1}),
    ("DATA", "Share of results of joint venture", {"FY2025": -22, "FY2024": -24, "FY2023": -25, "FY2022": -28, "FY2021": 2, "FY2020": 1, "FY2019": -30, "FY2018": -33, "FY2017": -34, "FY2016": -35, "FY2015": -35, "FY2014": -35, "FY2013": -34}),
    ("DATA", "Net change in prepayments and interest receivable", {"FY2025": -5, "FY2024": 9, "FY2022": -4, "FY2021": 10, "FY2020": 11, "FY2018": 10, "FY2017": 6, "FY2016": 11, "FY2015": 9, "FY2014": 8, "FY2013": 18}),
    ("DATA", "Net change in accruals and interest payable", {"FY2025": -9, "FY2024": 8, "FY2023": 94, "FY2022": 36, "FY2021": -28, "FY2020": -43, "FY2019": 38, "FY2018": 9, "FY2017": -24, "FY2016": -43, "FY2015": 9, "FY2014": -20, "FY2013": -101}),
    ("DATA", "Retirement benefit obligation (non-cash charge)", {"FY2016": 0, "FY2015": 1, "FY2014": 2, "FY2013": 1}),
    ("DATA", "Charge for provisions", {"FY2025": 236, "FY2024": 148, "FY2023": 3, "FY2022": 2, "FY2021": 13, "FY2020": 6, "FY2018": 5, "FY2017": 11, "FY2016": 12, "FY2015": 17, "FY2014": 15, "FY2013": 17}),
    ("DATA", "Other non-cash items", {"FY2025": -18, "FY2024": -98, "FY2023": -127, "FY2022": -45, "FY2021": 7, "FY2020": 30, "FY2019": 6, "FY2018": 10, "FY2017": 20, "FY2016": 13, "FY2015": 5}),
    ("TOTAL", "Cash flows from operating activities before changes in operating assets and liabilities", {"FY2025": 272, "FY2024": 261, "FY2023": 388, "FY2022": 317, "FY2021": 313, "FY2020": 253, "FY2019": 281, "FY2018": 252, "FY2017": 191, "FY2016": 208, "FY2015": 295, "FY2014": 293, "FY2013": 144}),
    ("DATA", "Net change in items in the course of collection to/from banks", {"FY2025": 35, "FY2024": -19, "FY2023": 31, "FY2022": 24, "FY2021": 5, "FY2020": 5, "FY2019": 13, "FY2018": 22, "FY2017": -38, "FY2016": 27, "FY2015": -18, "FY2014": 33, "FY2013": -68}),
    ("DATA", "Net change in derivative financial instruments", {"FY2025": 26, "FY2024": 97, "FY2023": 97, "FY2022": 30, "FY2021": -9, "FY2020": -19, "FY2019": -9, "FY2018": -36, "FY2017": -4, "FY2016": 17, "FY2015": -8, "FY2014": -9, "FY2013": 1}),
    ("DATA", "Net change in loans and advances to banks", {"FY2025": 32, "FY2024": -51, "FY2023": -45, "FY2021": 4, "FY2020": 203, "FY2019": 363, "FY2018": 350, "FY2017": 571, "FY2016": 676, "FY2015": 1962, "FY2014": 6872, "FY2013": 1284}),
    ("DATA", "Net change in fair value changes due to interest rate risk of hedged items in portfolio hedges", {"FY2023": -146}),
    ("DATA", "Net change in loans and advances to customers", {"FY2025": -536, "FY2024": -671, "FY2023": 101, "FY2022": 2316, "FY2021": 2051, "FY2020": -202, "FY2019": -1486, "FY2018": -327, "FY2017": -217, "FY2016": -576, "FY2015": -996, "FY2014": -434, "FY2013": -35}),
    ("DATA", "Net change in deposits from banks", {"FY2025": 265, "FY2024": -815, "FY2023": 130, "FY2022": -292, "FY2021": -803, "FY2020": 702, "FY2019": 348, "FY2018": -409, "FY2017": 800, "FY2016": 85, "FY2015": -2628, "FY2014": -6426, "FY2013": -14082}),
    ("DATA", "Net change in customer accounts", {"FY2025": 542, "FY2024": 408, "FY2023": -537, "FY2022": -3532, "FY2021": -2495, "FY2020": -820, "FY2019": -699, "FY2018": 807, "FY2017": -514, "FY2016": -2098, "FY2015": 1397, "FY2014": -879, "FY2013": -2418}),
    ("DATA", "Net change in debt securities in issue", {"FY2025": 229, "FY2024": -35, "FY2023": 170, "FY2022": -69, "FY2021": -63, "FY2020": -96, "FY2019": 607}),
    ("DATA", "Net change in provisions", {"FY2025": -18, "FY2024": -8, "FY2023": -4, "FY2022": -7, "FY2021": -14, "FY2020": -15, "FY2019": -10, "FY2018": -11, "FY2017": -14, "FY2016": -9, "FY2015": -13, "FY2014": -15, "FY2013": -15}),
    ("DATA", "Net change in retirement benefit obligation", {"FY2025": -1, "FY2024": -1, "FY2022": -1, "FY2021": -1, "FY2020": -1, "FY2019": -1, "FY2018": -2, "FY2017": -2, "FY2016": -2, "FY2015": -1, "FY2014": -2, "FY2013": -2}),
    ("DATA", "Net change in other assets and other liabilities", {"FY2025": -65, "FY2024": -7, "FY2023": -143, "FY2022": -14, "FY2021": -90, "FY2020": -49, "FY2019": -91, "FY2018": 70, "FY2017": 46, "FY2016": 80, "FY2015": 43, "FY2014": 44, "FY2013": 63}),
    ("TOTAL", "Net cash flow from operating assets and liabilities", {"FY2025": 509, "FY2024": -1102, "FY2023": -346, "FY2022": -1545, "FY2021": -1415, "FY2020": -292, "FY2019": -965, "FY2018": 464, "FY2017": 628, "FY2016": -1800, "FY2015": -262, "FY2014": -616, "FY2013": -15272}),
    ("TOTAL", "Net cash flow from operating activities before taxation", {"FY2025": 781, "FY2024": -841, "FY2023": 42, "FY2022": -1228, "FY2021": -1102, "FY2020": -39, "FY2019": -684, "FY2018": 716, "FY2017": 819, "FY2016": -1592, "FY2015": 33, "FY2014": -323, "FY2013": -15128}),
    ("DATA", "Taxation paid/(refunded)", {"FY2025": -51, "FY2024": -47, "FY2023": -56, "FY2022": -21, "FY2021": -53, "FY2020": -9, "FY2019": -14, "FY2018": -13, "FY2017": -14, "FY2016": -10, "FY2015": -114, "FY2014": 5, "FY2013": 24}),
    ("TOTAL", "Net cash flow from operating activities", {"FY2025": 730, "FY2024": -888, "FY2023": -14, "FY2022": -1249, "FY2021": -1155, "FY2020": -48, "FY2019": -698, "FY2018": 703, "FY2017": 805, "FY2016": -1602, "FY2015": 22, "FY2014": -318, "FY2013": -15104}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Proceeds from sale of financial assets", {"FY2024": 680, "FY2021": 2942}),
    ("DATA", "Acquisition of a subsidiary, net of cash acquired", {"FY2017": -41}),
    ("DATA", "Disposal of business activities", {"FY2019": 516}),
    ("DATA", "Additions to available for sale financial assets", {"FY2017": -82, "FY2016": -301, "FY2014": -553, "FY2013": -167}),
    ("DATA", "Redemptions and disposals of available for sale financial assets", {"FY2017": 198, "FY2016": 133, "FY2015": 26, "FY2014": 71, "FY2013": 19}),
    ("DATA", "Profit on disposal of business activities (investing proceeds)", {"FY2015": 41}),
    ("DATA", "Additions to debt securities at amortised cost", {"FY2025": -461, "FY2024": -77, "FY2023": -145, "FY2022": -26, "FY2021": -252, "FY2020": -143, "FY2019": -242, "FY2018": -156}),
    ("DATA", "Disposal/redemption of debt securities at amortised cost", {"FY2025": 69, "FY2024": 90, "FY2023": 196, "FY2022": 266, "FY2021": 359, "FY2020": 65, "FY2019": 309, "FY2018": 232}),
    ("DATA", "Dividends received from joint venture", {"FY2025": 23, "FY2024": 30, "FY2023": 29, "FY2022": 3, "FY2020": 14, "FY2019": 28, "FY2018": 33, "FY2017": 34, "FY2016": 35, "FY2015": 35, "FY2014": 30, "FY2013": 33}),
    ("DATA", "Additions to intangible assets", {"FY2019": -1, "FY2018": -1, "FY2017": -1, "FY2016": -1, "FY2014": -1, "FY2013": -3}),
    ("DATA", "Disposal of intangible assets", {"FY2013": 2}),
    ("DATA", "Additions to property, plant and equipment", {"FY2025": -105, "FY2024": -97, "FY2023": -82, "FY2022": -70, "FY2021": -54, "FY2020": -37, "FY2019": -46, "FY2018": -43, "FY2017": -19, "FY2015": -4, "FY2014": -4}),
    ("DATA", "Disposal of property, plant and equipment", {"FY2025": 37, "FY2024": 33, "FY2023": 29, "FY2022": 23, "FY2021": 18, "FY2020": 24, "FY2019": 18, "FY2018": 12}),
    ("TOTAL", "Cash flows from investing activities", {"FY2025": -437, "FY2024": 659, "FY2023": 27, "FY2022": 196, "FY2021": 3013, "FY2020": -77, "FY2019": 582, "FY2018": 78, "FY2017": 89, "FY2016": -134, "FY2015": 98, "FY2014": -457, "FY2013": -116}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of share capital", {"FY2013": 35}),
    ("DATA", "Share repurchase", {"FY2021": -250, "FY2020": -195}),
    ("DATA", "Dividend paid on ordinary shares", {"FY2023": -250, "FY2022": -250, "FY2019": -100, "FY2018": -70, "FY2017": -160, "FY2016": -220}),
    ("DATA", "Proceeds from issue of AT1", {"FY2021": 150}),
    ("DATA", "Redemption of AT1", {"FY2021": -300}),
    ("DATA", "Additional tier 1 coupon paid", {"FY2025": -9, "FY2024": -9, "FY2023": -9, "FY2022": -9, "FY2021": -25, "FY2020": -24, "FY2019": -24, "FY2018": -24, "FY2017": -24, "FY2016": -24}),
    ("DATA", "Capital contribution", {"FY2015": 165}),
    ("DATA", "Redemption/repurchase of subordinated liabilities", {"FY2022": -90, "FY2021": -200, "FY2017": -135, "FY2015": -523}),
    ("DATA", "Proceeds from issue of subordinated liabilities", {"FY2022": 90, "FY2021": 100, "FY2017": 90, "FY2015": 200}),
    ("DATA", "Repurchase of preference shares", {"FY2015": -300}),
    ("DATA", "Net proceeds from the issue of other equity instruments", {"FY2015": 300}),
    ("DATA", "Interest paid on subordinated liabilities", {"FY2025": -28, "FY2024": -31, "FY2023": -34, "FY2022": -14, "FY2021": -17, "FY2020": -18, "FY2019": -14, "FY2018": -13, "FY2017": -24, "FY2016": -24, "FY2015": -50, "FY2014": -52, "FY2013": -52}),
    ("DATA", "Payment of lease liability", {"FY2025": -1, "FY2024": -3, "FY2023": -4, "FY2022": -4, "FY2021": -4, "FY2020": -4, "FY2019": -5}),
    ("TOTAL", "Cash flows from financing activities", {"FY2025": -38, "FY2024": -43, "FY2023": -297, "FY2022": -277, "FY2021": -546, "FY2020": -241, "FY2019": -143, "FY2018": -107, "FY2017": -253, "FY2016": -268, "FY2015": -208, "FY2014": -52, "FY2013": -17}),
    ("TOTAL", "Net change in cash and cash equivalents", {"FY2025": 255, "FY2024": -272, "FY2023": -284, "FY2022": -1330, "FY2021": 1312, "FY2020": -366, "FY2019": -259, "FY2018": 674, "FY2017": 641, "FY2016": -2004, "FY2015": -88, "FY2014": -827, "FY2013": -15237}),
    ("DATA", "Opening cash and cash equivalents", {"FY2025": 3115, "FY2024": 3387, "FY2023": 3671, "FY2022": 5001, "FY2021": 3689, "FY2020": 4055, "FY2019": 4314, "FY2018": 3640, "FY2017": 2999, "FY2016": 5003, "FY2015": 5091, "FY2014": 5918, "FY2013": 21155}),
    ("TOTAL", "Closing cash and cash equivalents", {"FY2025": 3370, "FY2024": 3115, "FY2023": 3387, "FY2022": 3671, "FY2021": 5001, "FY2020": 3689, "FY2019": 4055, "FY2018": 4314, "FY2017": 3640, "FY2016": 2999, "FY2015": 5003, "FY2014": 5091, "FY2013": 5918}),
]

bw.add_cash_flow_sheet(
    title="Bank of Ireland (UK) Plc — Consolidated Cash Flow Statement",
    subtitle="Consolidated Group basis, £m. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=260,
    unit_suffix=" (£m)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - Bank of Ireland (UK) Plc consolidated Group basis, loans and advances to customers at amortised "
    "cost, £m, each year from its own primary report's IFRS 9 stage/product note (own-year gross carrying amount "
    "and impairment loss allowance tables):\n"
    f"FY2025: Annual Report 2025, p.111-113 (Note 19) - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.111-113 (Note 19, prior-period comparative) - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, p.114-115 (Note 18, printed) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, p.120-121 (Note 20, printed) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, p.128-130 (Note 20) - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020 (Companies House filing), p.122-131 (Note 19) - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019 (Companies House filing), p.112-114 (Note 19) - {AR2019_URL}\n"
    f"FY2018: Annual Report 2018 (Companies House filing), p.90-91 (Note 20) - {AR2018_URL}\n"
    f"FY2017: Annual Report 2017 (Companies House filing), p.42-44 ('Asset quality - loans and advances to "
    f"customers') - {AR2017_URL}\n"
    f"FY2016: Annual Report 2016 (Companies House filing), p.44-45 - {AR2016_URL}\n"
    f"FY2015: Annual Report 2015 (Companies House filing), p.44-45 - {AR2015_URL}\n"
    f"FY2014: Annual Report 2014 (Companies House filing), p.28-29 - {AR2014_URL}\n"
    "Note: by-product split (Residential mortgages / Non-property SME and corporate / Commercial property and "
    "construction / Consumer) is disclosed at Group level for FY2022-FY2025 only; FY2021's Group-level table shows "
    "only stage totals (a by-product split exists but only at Bank/solo level for FY2021, not reused here for a "
    "Group-basis sheet) - by-product cells are blank for FY2021, the stage-level rows are complete for all 5 years. "
    "FY2021's gross carrying amount (£16,503m) is ~£71m lower than the FY2022 report's restated FY2021 comparative "
    "(£16,574m) - see the Balance Sheet sheet's note on the same reclassification; each year's own figures are used "
    "here. Net loans (gross minus impairment loss allowance) tie exactly to the Balance Sheet's Loans and advances "
    "to customers line for every year. Ratios are calculated here (not separately disclosed as ratios in the "
    "source).\n\n"
    "FY2014-FY2017 ADDENDUM: these years pre-date IFRS 9 (adopted 1 January 2018) and use the IAS 39 loan-quality "
    "classification (neither past due nor impaired / past due but not impaired / impaired) instead of the IFRS 9 "
    "stage 1/2/3 model - see the separate 'Gross carrying amount by IAS 39 classification' section below (a "
    "genuine accounting-standard difference, not a data gap; the by-product split above still applies to all "
    "years on a consistent basis, since it is a loan-book categorisation independent of either impairment model). "
    "FY2018's gross carrying amount and impairment loss allowance include £539m/£(27)m relating to loans classified "
    "as held for sale that year (a one-off item also shown on the Balance Sheet), so net loans per this sheet "
    "(£20,240m gross-less-allowance) do not exactly equal the Balance Sheet's £19,703m Loans and advances to "
    "customers line for FY2018 alone (the £539m/£(27)m difference is the held-for-sale carve-out) - FY2019/FY2020 "
    "and all other years tie out exactly. Impairment loss allowance for FY2014-FY2017 is not separately tabulated "
    "by IAS 39 category in the source; it is calculated here as Total gross carrying amount less the Balance "
    "Sheet's own Loans and advances to customers (net) line, and cross-checked exactly against the disclosed "
    "closing impairment allowance figure for FY2017 (£155m, disclosed in the FY2018 Annual Report's IFRS 9 "
    "transition note) - a hard, non-approximate confirmation for that one year.\n\n" + ENTITY_NOTE
)

asset_quality_rows = [
    ("SECTION", "Gross carrying amount by product", {}),
    ("DATA", "Residential mortgages", {"FY2025": 10750, "FY2024": 10639, "FY2023": 9811, "FY2022": 9742, "FY2020": 16787, "FY2019": 16610, "FY2018": 15880, "FY2017": 16043, "FY2016": 15964, "FY2015": 15463, "FY2014": 14182}),
    ("DATA", "Non-property SME and corporate", {"FY2025": 1157, "FY2024": 1278, "FY2023": 1306, "FY2022": 1355, "FY2020": 1469, "FY2019": 1327, "FY2018": 1320, "FY2017": 1371, "FY2016": 1453, "FY2015": 1562, "FY2014": 1670}),
    ("DATA", "Commercial property and construction", {"FY2025": 207, "FY2024": 203, "FY2023": 216, "FY2022": 274, "FY2020": 369, "FY2019": 412, "FY2018": 502, "FY2017": 652, "FY2016": 961, "FY2015": 1377, "FY2014": 1917}),
    ("DATA", "Consumer", {"FY2025": 2684, "FY2024": 2159, "FY2023": 2966, "FY2022": 2831, "FY2020": 2948, "FY2019": 2997, "FY2018": 2697, "FY2017": 2086, "FY2016": 1709, "FY2015": 1307, "FY2014": 1145}),
    ("SECTION", "Gross carrying amount by IFRS 9 stage (FY2018 onward)", {}),
    ("DATA", "Stage 1 - 12 month ECL (not credit-impaired)", {"FY2025": 13409, "FY2024": 13113, "FY2023": 12501, "FY2022": 12615, "FY2021": 14769, "FY2020": 19744, "FY2019": 20497, "FY2018": 19357}),
    ("DATA", "Stage 2 - Lifetime ECL (not credit-impaired)", {"FY2025": 1210, "FY2024": 901, "FY2023": 1502, "FY2022": 1288, "FY2021": 1208, "FY2020": 1293, "FY2019": 569, "FY2018": 694}),
    ("DATA", "Stage 3 - Lifetime ECL (credit-impaired)", {"FY2025": 179, "FY2024": 265, "FY2023": 296, "FY2022": 299, "FY2021": 526, "FY2020": 536, "FY2019": 280, "FY2018": 348}),
    ("TOTAL", "Total gross carrying amount (IFRS 9 basis)", {"FY2025": 14798, "FY2024": 14279, "FY2023": 14299, "FY2022": 14202, "FY2021": 16503, "FY2020": 21573, "FY2019": 21346, "FY2018": 20399}),
    ("SECTION", "Impairment loss allowance by IFRS 9 stage (FY2018 onward)", {}),
    ("DATA", "Stage 1 - 12 month ECL (not credit-impaired)", {"FY2025": 22, "FY2024": 17, "FY2023": 40, "FY2022": 40, "FY2021": 47, "FY2020": 117, "FY2019": 48, "FY2018": 42}),
    ("DATA", "Stage 2 - Lifetime ECL (not credit-impaired)", {"FY2025": 30, "FY2024": 23, "FY2023": 66, "FY2022": 44, "FY2021": 46, "FY2020": 55, "FY2019": 27, "FY2018": 31}),
    ("DATA", "Stage 3 - Lifetime ECL (credit-impaired)", {"FY2025": 42, "FY2024": 48, "FY2023": 45, "FY2022": 100, "FY2021": 85, "FY2020": 101, "FY2019": 71, "FY2018": 86}),
    ("TOTAL", "Total impairment loss allowance (IFRS 9 basis)", {"FY2025": 94, "FY2024": 88, "FY2023": 151, "FY2022": 184, "FY2021": 178, "FY2020": 273, "FY2019": 146, "FY2018": 159}),
    ("SECTION", "Gross carrying amount by IAS 39 classification (FY2014-FY2017, pre-IFRS 9)", {}),
    ("DATA", "Neither past due nor impaired", {"FY2017": 19445, "FY2016": 19197, "FY2015": 18390, "FY2014": 17125}),
    ("DATA", "Past due but not impaired", {"FY2017": 432, "FY2016": 415, "FY2015": 518, "FY2014": 590}),
    ("DATA", "Impaired", {"FY2017": 275, "FY2016": 475, "FY2015": 801, "FY2014": 1199}),
    ("TOTAL", "Total gross carrying amount (IAS 39 basis)", {"FY2017": 20152, "FY2016": 20087, "FY2015": 19709, "FY2014": 18914}),
    ("DATA", "Total impairment loss allowance (IAS 39 basis; calculated - see note)", {"FY2017": 155, "FY2016": 266, "FY2015": 454, "FY2014": 613}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 14704, "FY2024": 14191, "FY2023": 14148, "FY2022": 14018, "FY2021": 16325, "FY2020": 21300, "FY2019": 21200, "FY2018": 19703, "FY2017": 19997, "FY2016": 19821, "FY2015": 19255, "FY2014": 18301}),
    ("SECTION", "Ratios (calculated)", {}),
    ("DATA", "ECL coverage ratio (total allowance / total gross carrying amount)", {"FY2025": "0.64%", "FY2024": "0.62%", "FY2023": "1.06%", "FY2022": "1.30%", "FY2021": "1.08%"}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross carrying amount)", {"FY2025": "1.21%", "FY2024": "1.86%", "FY2023": "2.07%", "FY2022": "2.11%", "FY2021": "3.19%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross)", {"FY2025": "23.46%", "FY2024": "18.11%", "FY2023": "15.20%", "FY2022": "33.44%", "FY2021": "16.16%"}),
]

bw.add_asset_quality_sheet(
    title="Bank of Ireland (UK) Plc — Asset Quality / Credit Risk Disclosures",
    subtitle="Consolidated Group basis, loans and advances to customers at amortised cost, £m. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    source_height=220,
)

# ---------------------------------------------------------------
# Pillar 3 / capital metric sheets
# ---------------------------------------------------------------
CAP_PAGE = {"FY2025": "55", "FY2024": "57-58", "FY2023": "54-55", "FY2022": "55-56", "FY2021": "60",
            "FY2020": "61-62", "FY2019": "55-57", "FY2018": "55-56", "FY2017": "20-21", "FY2016": "21-22",
            "FY2015": "21-22", "FY2014": "19-21"}
LIQ_PAGE = {"FY2025": "48", "FY2024": "49-50", "FY2023": "45-46", "FY2022": "45-46", "FY2021": "51-52",
            "FY2020": "10-11", "FY2019": "9-10", "FY2018": "10", "FY2017": "20-21", "FY2016": "21-22",
            "FY2015": "21-22", "FY2014": "19-21"}
# FY2014-FY2017 LCR/NSFR/loan-to-deposit ratios are shown in the "Key performance summary" panel of the Strategic
# Report, the same pages as the capital table; FY2018-FY2020 in an earlier "Capital"/liquidity summary chart page.


def metric(name, unit, rows_data, page, note=None):
    bw.add_metric_sheet(name, f"Consolidated Group basis, {unit}" if unit else "Consolidated Group basis",
                         rows_data, p3_sources(page), note=note, first_col_width=44, source_height=140)


metric(
    "CET1 Capital", "£m",
    [("Common equity tier 1 capital", {"FY2025": 1601, "FY2024": 1548, "FY2023": 1412, "FY2022": 1394, "FY2021": 1497, "FY2020": 1391, "FY2019": 1553, "FY2018": 1533, "FY2017": 1508, "FY2016": 1552, "FY2015": 1612, "FY2014": 1239})],
    CAP_PAGE,
    note="Fully-loaded basis throughout, consistent with the FY2021-FY2025 convention. FY2014 is the only year "
         "where transitional and fully-loaded bases genuinely differ (transitional CET1 capital was £1,236m) - see "
         "the Ratio Basis Note addendum on the Cash Flow Statement sheet.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio (fully loaded)", {"FY2025": "19.6%", "FY2024": "19.9%", "FY2023": "17.8%", "FY2022": "18.2%", "FY2021": "17.2%", "FY2020": "12.9%", "FY2019": "14.2%", "FY2018": "14.5%", "FY2017": "14.7%", "FY2016": "15.5%", "FY2015": "16.3%", "FY2014": "12.7%"})],
    CAP_PAGE,
)

metric(
    "Tier 1 Capital", "£m",
    [("Total tier 1 capital", {"FY2025": 1751, "FY2024": 1698, "FY2023": 1562, "FY2022": 1544, "FY2021": 1647, "FY2020": 1691, "FY2019": 1853, "FY2018": 1833, "FY2017": 1803, "FY2016": 1852, "FY2015": 1912, "FY2014": 1239})],
    CAP_PAGE,
    note="Tier 1 ratio (see Tier 1 Ratio sheet) is calculated from this figure - see the Ratio Basis Note on the "
         "Cash Flow Statement sheet. FY2014's fully-loaded Total tier 1 capital equals its CET1 capital (£1,239m): "
         "the Bank's £240m non-cumulative callable preference shares did not qualify as Additional Tier 1 on a "
         "fully-loaded CRD IV basis that year (only on the transitional basis, giving transitional Total tier 1 of "
         "£1,476m) - resolved by a May 2015 capital restructure (see the Statement of Changes in Equity sheet).",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio (fully loaded; calculated as Tier 1 capital / RWA)", {"FY2025": "21.4%", "FY2024": "21.9%", "FY2023": "19.7%", "FY2022": "20.1%", "FY2021": "19.0%", "FY2020": "15.7%", "FY2019": "16.9%", "FY2018": "17.5%", "FY2017": "17.7%", "FY2016": "18.4%", "FY2015": "19.3%", "FY2014": "12.7%"})],
    CAP_PAGE,
    note="Not stated as a percentage in any year's Annual Report (only Tier 1 capital £m and RWA £m are disclosed); "
         "calculated here as Tier 1 capital / Total risk weighted assets - see the Ratio Basis Note on the Cash "
         "Flow Statement sheet. FY2017's ratio is disclosed directly in the source as 'W7%' due to an OCR/print "
         "artefact in the scanned filing; corrected to 17.7% (1,803/10,231), consistent with the calculated method "
         "used for all other years.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 1941, "FY2024": 1888, "FY2023": 1752, "FY2022": 1734, "FY2021": 1837, "FY2020": 1977, "FY2019": 2143, "FY2018": 2123, "FY2017": 2098, "FY2016": 2187, "FY2015": 2247, "FY2014": 2197})],
    CAP_PAGE,
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio (fully loaded)", {"FY2025": "23.7%", "FY2024": "24.3%", "FY2023": "22.1%", "FY2022": "22.5%", "FY2021": "21.2%", "FY2020": "18.3%", "FY2019": "19.5%", "FY2018": "20.2%", "FY2017": "20.5%", "FY2016": "21.8%", "FY2015": "22.7%", "FY2014": "22.5%"})],
    CAP_PAGE,
    note="Explicitly stated on a fully loaded basis for FY2024/FY2025 only; FY2021-FY2023 and FY2014-FY2019 are "
         "calculated as Total capital / RWA (both disclosed fully-loaded figures); FY2020 and FY2016-FY2018 are "
         "disclosed directly as a fully-loaded percentage - see the Ratio Basis Note on the Cash Flow Statement "
         "sheet.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk weighted assets", {"FY2025": 8180, "FY2024": 7767, "FY2023": 7939, "FY2022": 7699, "FY2021": 8686, "FY2020": 10780, "FY2019": 10971, "FY2018": 10550, "FY2017": 10231, "FY2016": 10034, "FY2015": 9897, "FY2014": 9747})],
    CAP_PAGE,
    note="FY2017's Total RWA is disclosed in the source as '40,231' due to an OCR/print artefact in the scanned "
         "filing; corrected to 10,231, confirmed both by the narrative text ('RWAs increased from £10.0 billion "
         "to...') and by consistency with the Tier 1 ratio (1,803/10,231 = 17.7%, matching the disclosed ratio).",
)

RWA_BREAKDOWN_SOURCES = (
    p3_sources(CAP_PAGE) + "\n\nNote: no formal Pillar 3 KM1/OV1-style template has been published at this UK-"
    "entity level since FY2020 (see the Cash Flow Statement sheet's entity note) - the Annual Report's Capital "
    "management section discloses only the aggregate Total risk weighted assets figure, not a category breakdown "
    "(credit risk / counterparty credit risk / market risk / operational risk). Checked directly against all 5 "
    "years' Capital management sections - genuinely not publicly disclosed at category level, not merely omitted "
    "here. The Total row ties exactly to the Total RWAs sheet for every year.\n\n"
    "FRESH RE-VERIFICATION (2026-09-12): independently re-downloaded and full-text-searched all 5 FY2021-FY2025 "
    "Annual Report PDFs directly (not relying on the prior claim) for any OV1/EU OV1 table, 'credit risk "
    "(excluding CCR)' style line items, or a numeric Pillar 1 risk-type table - none found in any year. The only "
    "RWA-adjacent numeric disclosure in any of the 5 reports is the single aggregate 'Total risk weighted assets' "
    "line in the Capital management note (p.55 FY2025, cited above) and a purely narrative 'Counterparty credit "
    "risk (unaudited)' paragraph (describing netting arrangements with the Irish Parent, with no RWA figure "
    "attached) appearing in every year's Credit risk section. Confirms the prior non-disclosure claim still "
    "holds for FY2021-FY2025.\n\n"
    "FY2014-FY2017 ADDENDUM: unlike FY2018 onward, these 4 years' own Annual Reports DO disclose a genuine Pillar "
    "1 capital requirements RWA breakdown (Credit and counterparty risk / Operational risk, each on a Basel III/"
    "CRD IV standardised-approach basis) - a real finding that MORE granular RWA data is available for these older "
    "years than for FY2018-2025 at this UK-entity level. Sourced from each year's own 'Pillar 1 capital "
    "requirements' table (Strategic Report, same section as the capital table); cross-checked using each "
    "subsequent year's prior-period comparative column, which in every case ties exactly to the Total RWAs sheet."
)

rwa_breakdown_rows = [
    ("DATA", "Category breakdown (credit risk / market risk / operational risk)", {"FY2025": "Not publicly disclosed", "FY2020": "Not publicly disclosed", "FY2019": "Not publicly disclosed", "FY2018": "Not publicly disclosed"}),
    ("DATA", "Credit and counterparty risk", {"FY2017": 9475, "FY2016": 9255, "FY2015": 9151, "FY2014": 9105}),
    ("DATA", "Operational risk", {"FY2017": 756, "FY2016": 779, "FY2015": 746, "FY2014": 642}),
    ("TOTAL", "Total risk weighted assets", {"FY2025": 8180, "FY2024": 7767, "FY2023": 7939, "FY2022": 7699, "FY2021": 8686, "FY2020": 10780, "FY2019": 10971, "FY2018": 10550, "FY2017": 10231, "FY2016": 10034, "FY2015": 9897, "FY2014": 9747}),
]

bw.add_rwa_breakdown_sheet(
    title="Bank of Ireland (UK) Plc — RWA Breakdown",
    subtitle="Consolidated Group basis, £m. Category breakdown not publicly disclosed - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total leverage ratio exposures", {"FY2025": 19437, "FY2024": 17664, "FY2023": 16678, "FY2022": 16948, "FY2021": 22879, "FY2020": 26708, "FY2019": 27317, "FY2018": 27377, "FY2017": 27260, "FY2016": 26985, "FY2015": 29915, "FY2014": 34417}),
        ("Leverage ratio (fully loaded)", {"FY2025": "9.0%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "9.1%", "FY2021": "7.2%", "FY2020": "6.3%", "FY2019": "6.8%", "FY2018": "6.7%", "FY2017": "6.6%", "FY2016": "6.9%", "FY2015": "6.4%", "FY2014": "3.6%"}),
    ],
    CAP_PAGE,
    note="FY2014's leverage exposure figure is calculated (Tier 1 capital / leverage ratio) rather than directly "
         "sourced - that year's own Annual Report discloses the fully-loaded leverage ratio (3.6%) and Tier 1 "
         "capital (£1,239m) but not a leverage-exposure reconciliation table (first introduced in the FY2015 "
         "report); all other years' exposure figures are directly disclosed.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {"FY2025": "161%", "FY2024": "154%", "FY2023": "168%", "FY2022": "178%", "FY2021": "268%", "FY2020": "142%", "FY2019": "147%", "FY2018": "158%", "FY2017": "127%", "FY2016": "115%", "FY2015": "194%"})],
    LIQ_PAGE,
    note="Only the headline LCR percentage is disclosed in the Annual Report's Funding and liquidity risk section; "
         "the underlying £m components (HQLA, net cash outflows) are not published for any year. The LCR came into "
         "force on 1 October 2015 (Commission Delegated Regulation (EU) 2015/61); FY2014 is blank because the "
         "Bank's own FY2015 Annual Report shows the FY2014 comparative as 'n/a' for this reason, not because the "
         "figure is missing.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {"FY2025": "135%", "FY2024": "130%", "FY2023": "135%", "FY2022": "135%", "FY2021": "139%", "FY2020": "133%", "FY2019": "133%", "FY2018": "134%", "FY2017": "130%", "FY2016": "130%", "FY2015": "145%"})],
    LIQ_PAGE,
    note="Only the headline NSFR percentage is disclosed; the underlying £m components (available/required stable "
         "funding) are not published for any year - see the LCR sheet's note. FY2014 is blank on the same basis as "
         "the LCR (not disclosed as an EU-standardised ratio until FY2015).",
)

metric(
    "MREL Ratio", "%",
    [("MREL ratio", {"FY2025": "26.2%", "FY2024": "26.9%", "FY2023": "24.6%", "FY2022": "26.7%", "FY2021": "24.9%", "FY2020": "21.8%"})],
    CAP_PAGE,
    note="Only the headline MREL ratio percentage is disclosed each year (a 'Key points' bullet in the Capital "
         "management section); no £m MREL resources/requirement breakdown is published. The Bank has been subject "
         "to an internal MREL requirement on a transitional basis since 1 January 2020; the Parent (Bank of "
         "Ireland Group plc), as sole shareholder, is expected to provide any future core MREL resources. FY2020 is "
         "the first year an MREL ratio is disclosed at all (consistent with the 1 January 2020 requirement date); "
         "FY2014-FY2019 are blank because no MREL requirement existed for this entity yet, not because of a "
         "sourcing gap.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 19865, "FY2024": 18611, "FY2023": 18832, "FY2022": 18871, "FY2021": 22705, "FY2020": 26419, "FY2019": 26934, "FY2018": 26700, "FY2017": 26235, "FY2016": 25960, "FY2015": 27939, "FY2014": 29209}),
        ("Loans and advances to customers", {"FY2025": 14704, "FY2024": 14191, "FY2023": 14148, "FY2022": 14018, "FY2021": 16325, "FY2020": 21300, "FY2019": 21200, "FY2018": 19703, "FY2017": 19997, "FY2016": 19821, "FY2015": 19255, "FY2014": 18301}),
        ("Customer accounts", {"FY2025": 12765, "FY2024": 12223, "FY2023": 11815, "FY2022": 12222, "FY2021": 15753, "FY2020": 18256, "FY2019": 19075, "FY2018": 19769, "FY2017": 18961, "FY2016": 19475, "FY2015": 21574, "FY2014": 20180}),
        ("Total equity", {"FY2025": 1785, "FY2024": 1777, "FY2023": 1639, "FY2022": 1645, "FY2021": 1743, "FY2020": 1801, "FY2019": 1980, "FY2018": 2004, "FY2017": 1999, "FY2016": 2050, "FY2015": 2104, "FY2014": 1767}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 476, "FY2024": 498, "FY2023": 571, "FY2022": 533, "FY2021": 535, "FY2020": 495, "FY2019": 501, "FY2018": 525, "FY2017": 471, "FY2016": 494, "FY2015": 492, "FY2014": 512}),
        ("Operating expenses", {"FY2025": -485, "FY2024": -382, "FY2023": -222, "FY2022": -247, "FY2021": -272, "FY2020": -310, "FY2019": -317, "FY2018": -351, "FY2017": -328, "FY2016": -313, "FY2015": -300, "FY2014": -287}),
        ("Profit/(loss) for the year", {"FY2025": -1, "FY2024": 133, "FY2023": 259, "FY2022": 228, "FY2021": 398, "FY2020": 27, "FY2019": 97, "FY2018": 151, "FY2017": 130, "FY2016": 164, "FY2015": 188, "FY2014": 172}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1777, "FY2024": 1639, "FY2023": 1645, "FY2022": 1743, "FY2021": 1801, "FY2020": 1980, "FY2019": 2004, "FY2018": 1999, "FY2017": 2050, "FY2016": 2104, "FY2015": 1767, "FY2014": 1548}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 16, "FY2024": 150, "FY2023": 253, "FY2022": 161, "FY2021": 366, "FY2020": 40, "FY2019": 100, "FY2018": 134, "FY2017": 128, "FY2016": 185, "FY2015": 172, "FY2014": 204}),
        ("Other equity movements, net", {"FY2025": -8, "FY2024": -12, "FY2023": -259, "FY2022": -259, "FY2021": -424, "FY2020": -219, "FY2019": -124, "FY2018": -129, "FY2017": -178, "FY2016": -239, "FY2015": 165, "FY2014": 15}),
        ("Closing equity", {"FY2025": 1785, "FY2024": 1777, "FY2023": 1639, "FY2022": 1645, "FY2021": 1743, "FY2020": 1801, "FY2019": 1980, "FY2018": 2004, "FY2017": 1999, "FY2016": 2050, "FY2015": 2104, "FY2014": 1767}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash flow from operating activities", {"FY2025": 730, "FY2024": -888, "FY2023": -14, "FY2022": -1249, "FY2021": -1155, "FY2020": -48, "FY2019": -698, "FY2018": 703, "FY2017": 805, "FY2016": -1602, "FY2015": 22, "FY2014": -318}),
        ("Cash flows from investing activities", {"FY2025": -437, "FY2024": 659, "FY2023": 27, "FY2022": 196, "FY2021": 3013, "FY2020": -77, "FY2019": 582, "FY2018": 78, "FY2017": 89, "FY2016": -134, "FY2015": 98, "FY2014": -457}),
        ("Cash flows from financing activities", {"FY2025": -38, "FY2024": -43, "FY2023": -297, "FY2022": -277, "FY2021": -546, "FY2020": -241, "FY2019": -143, "FY2018": -107, "FY2017": -253, "FY2016": -268, "FY2015": -208, "FY2014": -52}),
        ("Closing cash and cash equivalents", {"FY2025": 3370, "FY2024": 3115, "FY2023": 3387, "FY2022": 3671, "FY2021": 5001, "FY2020": 3689, "FY2019": 4055, "FY2018": 4314, "FY2017": 3640, "FY2016": 2999, "FY2015": 5003, "FY2014": 5091}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "19.6%", "FY2024": "19.9%", "FY2023": "17.8%", "FY2022": "18.2%", "FY2021": "17.2%", "FY2020": "12.9%", "FY2019": "14.2%", "FY2018": "14.5%", "FY2017": "14.7%", "FY2016": "15.5%", "FY2015": "16.3%", "FY2014": "12.7%"}),
        ("Tier 1 Ratio", {"FY2025": "21.4%", "FY2024": "21.9%", "FY2023": "19.7%", "FY2022": "20.1%", "FY2021": "19.0%", "FY2020": "15.7%", "FY2019": "16.9%", "FY2018": "17.5%", "FY2017": "17.7%", "FY2016": "18.4%", "FY2015": "19.3%", "FY2014": "12.7%"}),
        ("Total Capital Ratio", {"FY2025": "23.7%", "FY2024": "24.3%", "FY2023": "22.1%", "FY2022": "22.5%", "FY2021": "21.2%", "FY2020": "18.3%", "FY2019": "19.5%", "FY2018": "20.2%", "FY2017": "20.5%", "FY2016": "21.8%", "FY2015": "22.7%", "FY2014": "22.5%"}),
        ("Leverage Ratio", {"FY2025": "9.0%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "9.1%", "FY2021": "7.2%", "FY2020": "6.3%", "FY2019": "6.8%", "FY2018": "6.7%", "FY2017": "6.6%", "FY2016": "6.9%", "FY2015": "6.4%", "FY2014": "3.6%"}),
        ("LCR", {"FY2025": "161%", "FY2024": "154%", "FY2023": "168%", "FY2022": "178%", "FY2021": "268%", "FY2020": "142%", "FY2019": "147%", "FY2018": "158%", "FY2017": "127%", "FY2016": "115%", "FY2015": "194%"}),
        ("NSFR", {"FY2025": "135%", "FY2024": "130%", "FY2023": "135%", "FY2022": "135%", "FY2021": "139%", "FY2020": "133%", "FY2019": "133%", "FY2018": "134%", "FY2017": "130%", "FY2016": "130%", "FY2015": "145%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Tier 1 Ratio and part of the Total Capital Ratio series are "
         "calculated (capital / RWA), not directly quoted - see the Ratio Basis Note on the Cash Flow Statement "
         "sheet. No standalone Pillar 3 document has been published for this entity since FY2020; all figures here "
         "come from the Annual Report's Risk Management Report instead.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF IRELAND UK FINANCIALS.xlsx")
