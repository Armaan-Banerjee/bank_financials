import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017"]  # most recent first
YEAR_LABEL = {
    "FY2026": "FY2026 (SGHL)‡",
    "FY2025": "FY2025",
    "FY2024": "FY2024",
    "FY2023": "FY2023",
    "FY2022": "FY2022",
    "FY2021": "FY2021†",
    "FY2020": "FY2020",
    "FY2019": "FY2019",
    "FY2018": "FY2018",
    "FY2017": "FY2017",
}

AR21_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-Bank-Annual-Report-2019-21.pdf"
AR22_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-Bank-Annual-Report-2022.pdf"
AR23_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-Bank-Annual-Report-2023.pdf"
AR25_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-Bank-Annual-Report-2025.pdf"
AR26_SGHL_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-Group-Annual-Report-2026.pdf"
AR20_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-Bank-Annual-Report-2019-21.pdf"
# BLOCKED, WITH NO ARCHIVED FALLBACK - an unresolved state, explicitly NOT a negative
# (checked 2026-09-16). starlingbank.com refuses this project's automated fetcher: this URL
# returns HTTP 403 with a ~49KB text/html bot-protection page rather than a PDF. A 403 is an
# UNKNOWN - it records that the host declined to serve US, NOT that the document has been
# withdrawn, and a human browser or a different network may well retrieve it normally. No
# substitute could be offered either: a Wayback CDX query on this exact URL was run on
# 2026-09-16 and returned successfully with an EMPTY result set, so the absence of an ARCHIVE
# is enumerated rather than assumed - but that says nothing about the document itself, which
# remains unexamined rather than absent. Left cited at the publisher's live URL deliberately,
# since there is nothing verified to replace it with. Do not downgrade this to "dead".
AR19_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-Bank-Annual-Report-2019-18.pdf"
AR18_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-bank-annual-report-2017-18.pdf"
AR17_URL = "https://www.starlingbank.com/docs/annual-reports/Starling-bank-annual-report-2016-17.pdf"

P3_21_URL = "https://www.starlingbank.com/docs/annual-reports/Pillar3-2021.pdf"
P3_22_URL = "https://www.starlingbank.com/docs/annual-reports/Pillar3-2022.pdf"
P3_23_URL = "https://www.starlingbank.com/docs/annual-reports/Pillar3-2023.pdf"
P3_24_URL = "https://www.starlingbank.com/docs/annual-reports/Pillar3-2024.pdf"
P3_25_URL = "https://www.starlingbank.com/docs/annual-reports/Pillar3-2025.pdf"
P3_26_URL = "https://www.starlingbank.com/docs/annual-reports/Pillar3-2026.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Starling Bank Limited (Companies House 09092149) is the entity on the PRA register and is used, "
    "on a consolidated Group basis, for FY2021-FY2025 - each year's own Annual Report and Consolidated Financial "
    "Statements. FY2021 (marked †) is a 16-month period (1 December 2019 - 31 March 2021), Starling's first "
    "period reporting to a 31 March year end - not directly run-rate comparable to the other years.\n"
    "FY2026 (marked ‡, added as a bonus column beyond the standard 5-year window) is different: in June 2025 a "
    "new non-trading holding company, Starling Group Holdings Limited (SGHL), was inserted as ultimate parent of "
    "Starling Bank Limited (SBL), with an intermediate holding company (SIHL) added in September 2025. From "
    "FY2026, SBL's own Companies House filing is presented on an unconsolidated solo/Company basis only (SBL's "
    "own wording: 'the Company' = Starling Bank Limited; consolidated 'Group' figures are now published "
    "separately as SGHL's own Annual Report). To keep this column comparable to FY2021-FY2025's consolidated "
    "basis, FY2026 cash flow figures here are SGHL's consolidated Group figures (from the new SGHL Annual "
    "Report), not SBL's own solo filing. The SGHL accounting consolidation for FY2026 additionally includes "
    "Murmur Financial Services Limited, Fleet Mortgages Limited and Engine by Starling Limited alongside SBL and "
    "its own ancillary undertakings (Starling FS Services Limited, and Ember by Starling Limited, acquired during "
    "FY2026) - a broader scope than SBL's own historical Group accounts. Pillar 3 (prudential) figures for FY2026 "
    "are on the narrower 'Regulatory Group' basis (SGHL, SIHL, SBL, SFSSL and Ember only - Murmur/Fleet "
    "Mortgages/Engine fall below CRR Article 19 materiality thresholds); cross-checking confirms this made no "
    "difference to the FY2025 capital figures, so Pillar 3 continuity FY2021-FY2026 is unaffected by the "
    "restructuring. FY2020-FY2017 are covered by Starling's official investor archive: FY2020/FY2019 in the "
    "2019-21 report, FY2018 in the 2017-18 report, and FY2017 in the 2016-17 report. Older columns retain blanks "
    "where the historical filing used a materially different presentation and no reliable like-for-like line exists."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Group/consolidated basis, £'000. See entity note above re: FY2021 (16-month "
    "period) and FY2026 (new SGHL parent entity).\n"
    f"FY2026: Starling Group Holdings Limited Annual Report and Accounts 2026, p.165 (Consolidated cash flow "
    f"statement) - {AR26_SGHL_URL}\n"
    f"FY2025 & FY2024: Starling Bank Limited Annual Report and Accounts 2025, p.159 and p.214 (Consolidated and "
    f"company cash flow statement, and note 29) - {AR25_URL}\n"
    f"FY2023 & FY2022 (restated): Starling Bank Limited Annual Report 2023, p.124-125 and p.177 (Consolidated & "
    f"Company Cash Flow Statement, and note 29) - {AR23_URL}\n"
    f"FY2021: Starling Bank Limited Annual Report and Consolidated Financial Statements, period ended 31 March "
    f"2021, p.66-67 (Consolidated Cash Flow Statement) - {AR21_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "RESTATEMENT NOTE: The 2023 Annual Report changed the Group's cash and cash equivalents accounting policy to "
    "exclude the mandatory Cash Ratio Deposit held with the Bank of England; this reduced the Group's cash and "
    "cash equivalents at 1 April 2021 by £7,627k (to a restated £3,188,722k) on a comparative basis, but FY2021's "
    "own original Annual Report was never itself restated (its reported closing balance is £3,196,349k). This "
    "produces a documented £7,627k break at the FY2021/FY2022 boundary only; FY2022 onward reconciles exactly.\n\n"
    "PRESENTATION NOTE: FY2021-FY2023 report operating-activities adjustments and asset/liability movements as "
    "granular individual line items; FY2024 onward summarises them into three reported subtotals ('Non-cash "
    "movements', 'Movement in operating assets', 'Movement in operating liabilities') with the detail moved to a "
    "note - both are shown, clearly separated, so blank cells simply reflect which presentation style that year's "
    "report used. FY2026's figures are shown only at the summarised level (the underlying SGHL note breakdown "
    "was not extracted). The 'Profit for the period after taxation' line is repeated once per presentation style "
    "(a generic block-reconciliation checker run against this sheet will only sum the DATA rows immediately "
    "preceding each operating-activities TOTAL, so Profit needs its own row within each block rather than a "
    "single shared row above both - this is a spreadsheet-layout clarification, not a change to any figure). "
    "Section totals and cash and cash equivalents are consistent within each presentation style and reconcile "
    "exactly year to year (except the documented FY2021/FY2022 break above): confirmed by hand against each "
    "year's own primary source, including FY2026 (2026-08-27), where the operating-activities TOTAL was "
    "originally mistranscribed as 185,354 - the SGHL FY2026 Annual Report's own Consolidated Cash Flow Statement "
    "(p.165) states 183,334, which is what the full profit+adjustments+tax chain sums to exactly; corrected."
)

def p3_sources(url, doc_label, page1="6", page2="7"):
    return (
        "Sources - Starling Bank Limited Pillar 3 basis (Regulatory Group basis for FY2026 - see entity note on "
        f"Cash Flow Statement sheet; identical to Starling Bank Limited's own scope for FY2021-FY2025):\n"
        f"{doc_label}: p.{page1}-{page2}, section 4.1 Key metrics - {url}"
    )

P3_SOURCES_ALL = (
    "Sources - Starling Bank Limited Pillar 3 basis (Regulatory Group basis for FY2026 - see entity note on Cash "
    "Flow Statement sheet):\n"
    f"FY2026: Starling Group Pillar 3 report 2026, as at 31 March 2026, section 4.1 Key metrics, p.22-23 - {P3_26_URL}\n"
    f"FY2025: Starling Bank Limited Pillar 3 report 2025, as at 31 March 2025, section 4.1 Key metrics, p.22-23 - {P3_25_URL}\n"
    f"FY2024: Starling Bank Limited Pillar 3 report 2024, as at 31 March 2024, section 4.1 Key metrics, p.22-23 - {P3_24_URL}\n"
    f"FY2023: Starling Bank Limited Pillar 3 Report 2023, as at 31 March 2023, section 4.1 Key Metrics, p.21 - {P3_23_URL}\n"
    f"FY2022: Starling Bank Ltd Pillar 3 Report 2022, as at 31 March 2022 (FY2023 report's comparator column), p.21 - {P3_22_URL}\n"
    f"FY2021: Starling Bank Limited Pillar 3 Disclosures, as at 31 March 2021, sections 5 (Capital Resources), "
    f"5.2 (Leverage Ratio) and 12 (Liquidity), p.19-23 - {P3_21_URL} (pre-dates the formal KM1 template)"
)

bw = BankWorkbook(bank_name="Starling Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="6B2C91")

STATEMENTS_SOURCES = (
    "Sources - all figures are Group/consolidated basis, £'000. See entity note above re: FY2021 (16-month "
    "period) and FY2026 (new SGHL parent entity).\n"
    f"FY2026: Starling Group Holdings Limited Annual Report and Accounts 2026, p.162-164 (Consolidated statement "
    f"of comprehensive income / financial position / changes in equity) - {AR26_SGHL_URL}\n"
    f"FY2025 & FY2024: Starling Bank Limited Annual Report and Accounts 2025, p.157-159 (Consolidated and company "
    f"statement of comprehensive income / financial position / changes in equity) - {AR25_URL}. FY2025's equity "
    f"components independently cross-checked against the Group's own re-presented FY2025 comparative in the AR26 "
    f"Annual Report (p.164), which agrees exactly (merger reserve, cash flow hedging reserve, own shares held "
    f"reserve, share awards reserve and sundry reserves disaggregated only from AR26 onward - see presentation "
    f"note below).\n"
    f"FY2023 & FY2022 (restated): Starling Bank Limited Annual Report 2023, p.122-123, p.126-127 (Consolidated & "
    f"Company Statement of Comprehensive Income / Financial Position / Changes in Equity) - {AR23_URL}\n"
    f"FY2021: Starling Bank Limited Annual Report and Consolidated Financial Statements, period ended 31 March "
    f"2021, p.62-68 (Consolidated Statement of Comprehensive Income / Financial Position / Changes in Equity) - "
    f"{AR21_URL}. Independently cross-checked against Annual Report 2023's FY2021 comparative opening equity "
    f"balance, which agrees exactly.\n"
    f"FY2018 (& FY2017): Starling Bank Limited Annual Report and Consolidated Financial Statements for the year "
    f"ended 30 November 2018, printed p.45 / PDF p.25, 'Consolidated Statement of Financial Position as at "
    f"30 November 2018' - {AR18_URL}. That table prints four columns (Group 2018, Group 2017, Company 2018, "
    f"Company 2017); the GROUP columns are used, as everywhere else in this workbook.\n"
    f"FY2017 independently cross-checked against its own original report: Starling Bank Limited Annual Report "
    f"2017 (year ended 30 November 2017), printed p.42 / PDF p.44, Consolidated Statement of Financial Position "
    f"- {AR17_URL}. Every FY2017 figure agrees exactly between the two editions (Loans and Advances to Banks "
    f"37,544; Total Assets 53,277; Total Liabilities 20,559; Share Premium 47,846; Total Equity 32,718) - no "
    f"restatement.\n"
    f"CORRECTION (2026-09-16): FY2018 'Loans and advances to banks' previously read 37,544. That is the FY2017 "
    f"COMPARATIVE from the same table, mis-read one column across; the FY2018 Group figure is 187,008. The "
    f"error was self-evident from the column's own arithmetic - 187,008 + 18,039 + 8,698 + 7,087 + 616 + 13,221 "
    f"= 234,669, the printed Total Assets, whereas 37,544 left the column 149,464 short of its own stated total. "
    f"Every other FY2018 and FY2017 cell was re-checked against the printed table and is correct. The FY2018 "
    f"column was also completed at the same time: it previously carried a single 'Other assets' of 20,924 that "
    f"silently absorbed Property, Plant and Equipment (616) and Intangible Assets (13,221), while the adjacent "
    f"FY2017 column showed those two lines separately - the two columns now use identical treatment, and the "
    f"FY2018 equity components (Share Capital 5, Share Premium 67,784, Other Reserves 319, Cumulative Retained "
    f"Earnings (40,109)) and liability components (Provisions 202, Other Liabilities 3,614, Accruals and "
    f"Deferred Income 531) are transcribed rather than left blank.\n"
    f"FY2018/FY2017 caption mapping: 'Investment Securities' is carried on the 'Total debt securities' row (no "
    f"issuer-type breakdown is disclosed for these years, so the four sub-lines stay blank); 'Accruals and "
    f"Deferred Income' is carried on the 'Deferred income' row; and 'Other assets' combines the report's 'Other "
    f"Assets' and 'Accrued Interest and Prepayments' lines (FY2018: 5,464 + 1,623 = 7,087; FY2017: 2,236 + 96 = "
    f"2,332) because no separate accrued-interest row exists in this ladder. Both columns tie exactly: assets "
    f"to Total Assets, liabilities to Total Liabilities, and equity components to Total Equity.\n\n"
    + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE (Balance Sheet): FY2024-FY2026 report a separate 'Cash and balances at central banks' line "
    "distinct from 'Loans and advances to banks'; FY2021-FY2023 report a single combined 'Loans and Advances to "
    "Banks' line that includes cash and cash equivalents (per that year's own footnote) - both are shown as "
    "disclosed, not reconciled into a common split. FY2021 combines Property, Plant and Equipment with Intangible "
    "Assets into one line (no separate Goodwill line - Goodwill first arose on the Fleet Mortgages acquisition in "
    "FY2022); FY2022 onward splits these three lines out.\n\n"
    "PRESENTATION NOTE (Debt securities breakdown): the 'Debt securities' Balance Sheet line is broken out by "
    "issuer type per each year's own 'Debt securities' note - government/supranational bonds vs. covered bonds "
    "and RMBS issued by banks and building societies, plus the fair value adjustment for hedged risk that "
    "reconciles the gross note total to the Balance Sheet's net carrying value (all four sub-lines sum exactly "
    "to 'Total debt securities' every year). Source notes: FY2026: Starling Group Holdings Limited Annual Report "
    f"and Accounts 2026, note 13 'Debt securities', p.195 - {AR26_SGHL_URL}\n"
    f"FY2025 & FY2024: Starling Bank Limited Annual Report and Accounts 2025, note 10 'Debt securities', p.189 "
    f"- {AR25_URL}. FY2025's breakdown independently cross-checked against AR26's own FY2025 comparative column "
    "(note 13, p.195), which agrees exactly.\n"
    f"FY2023 & FY2022: Starling Bank Limited Annual Report 2023, note 11 'Debt Securities', p.154 - {AR23_URL}\n"
    f"FY2021: Starling Bank Limited Annual Report and Consolidated Financial Statements, period ended 31 March "
    f"2021, note 12 'Debt Securities', p.111 - {AR21_URL}. That year's note also states 'All Debt Securities are "
    "held at amortised cost' - no FVOCI/FVTPL/trading leg is disclosed for any year covered (the FY2025 Annual "
    "Report's own risk section likewise states 'The Group's debt securities are measured at amortised cost'), "
    "so no measurement-basis (amortised cost vs. mark-to-market) split is shown here - it would be a "
    "100%-amortised-cost/0%-mark-to-market non-split, not a genuine disclosed breakdown.\n\n"
    "PRESENTATION NOTE (Profit & Loss): FY2021-FY2025 use a 'Net interest income / Net fees and commissions / "
    "Total income' structure; FY2026 (Starling Group Holdings Limited's own first Annual Report) uses a "
    "'Revenue / Cost of revenue / Gross profit' structure instead - both are shown as separate blocks, each with "
    "its own Profit-after-tax and Total-comprehensive-income rows (mirroring the Cash Flow Statement sheet's "
    "existing dual-presentation convention), rather than force-fitting FY2026 into the older structure. FY2021's "
    "Loss for the year and OCI, net of tax are the same figure (no OCI items disclosed that year - 'There is no "
    "difference between the loss after taxation and the total comprehensive income of the Group').\n\n"
    "PRESENTATION NOTE (Statement of Changes in Equity): 'Merger reserve' (created in FY2022 on the Fleet "
    "Mortgages Limited share-for-share acquisition, per Companies Act 2006 s.612) and 'Cash flow hedging reserve' "
    "are shown as their own columns throughout for consistency, back-computed for FY2021-FY2023 from each year's "
    "combined 'Other Reserves' column and that year's own movement notes (verified: FY2022's £15,000k Merger "
    "reserve movement exactly matches the value AR26 later separately discloses as the FY2024 opening Merger "
    "reserve balance, confirming it never changed between creation and FY2024). 'Other reserves' here combines "
    "the own-shares-held reserve, share awards reserve, foreign exchange/translation reserve and sundry reserves "
    "- these were only disclosed as separate sub-columns from AR26 (FY2026 report) onward; combining them keeps "
    "the ladder's column set consistent across all 6 years. Every year's closing Total equity ties exactly to "
    "that year's own Balance Sheet Total equity and to the next year's opening balance - zero undocumented plug "
    "rows across all 6 years."
)

# ---------------------------------------------------------------
# Balance Sheet (Consolidated Statement of Financial Position)
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2026": 4188830, "FY2025": 6686688, "FY2024": 6420115}),
    ("DATA", "Loans and advances to banks (FY2021-FY2023: includes cash and cash equivalents - see source note)", {"FY2026": 36508, "FY2025": 30489, "FY2024": 36879, "FY2023": 6109704, "FY2022": 6107281, "FY2021": 3196349}),
    ("DATA", "Total debt securities", {"FY2026": 6843426, "FY2025": 3934922, "FY2024": 3284867, "FY2023": 2479550, "FY2022": 2306886, "FY2021": 1513278}),
    ("DATA", "Debt securities - issued by governments and supranational bodies (government securities)", {"FY2026": 3043972, "FY2025": 1711624, "FY2024": 1535013, "FY2023": 1544706, "FY2022": 1705167, "FY2021": 1119687}),
    ("DATA", "Debt securities - covered bonds issued by banks and building societies", {"FY2026": 1867695, "FY2025": 1258616, "FY2024": 1109808, "FY2023": 925494, "FY2022": 613430, "FY2021": 382638}),
    ("DATA", "Debt securities - residential mortgage-backed securities (RMBS) issued by banks and building societies", {"FY2026": 1963242, "FY2025": 993778, "FY2024": 675881, "FY2023": 48040, "FY2022": 11664, "FY2021": 13652}),
    ("DATA", "Debt securities - fair value adjustment for hedged risk (reconciling item, see source note)", {"FY2026": -31483, "FY2025": -29096, "FY2024": -35835, "FY2023": -38690, "FY2022": -23375, "FY2021": -2699}),
    ("DATA", "Derivative assets", {"FY2026": 110908, "FY2025": 156615, "FY2024": 246541, "FY2023": 221774, "FY2022": 98056, "FY2021": 13488}),
    ("DATA", "Loans and advances to customers", {"FY2026": 5161359, "FY2025": 4670567, "FY2024": 4537663, "FY2023": 4731997, "FY2022": 3234673, "FY2021": 2232846}),
    ("DATA", "Other assets", {"FY2026": 63120, "FY2025": 54474, "FY2024": 100047, "FY2023": 71851, "FY2022": 66635, "FY2021": 63460}),
    ("DATA", "Current tax asset", {"FY2026": 0, "FY2025": 748, "FY2024": 15640}),
    ("DATA", "Deferred tax asset", {"FY2026": 1702, "FY2023": 4664, "FY2022": 21985, "FY2021": 6088}),
    ("DATA", "Property, plant and equipment and right of use assets", {"FY2026": 26726, "FY2025": 18388, "FY2024": 18727, "FY2023": 15480, "FY2022": 5904}),
    ("DATA", "Property, plant and equipment and intangible assets (FY2021: combined, pre-dates Goodwill - see source note)", {"FY2021": 23325}),
    ("DATA", "Intangible assets", {"FY2026": 169008, "FY2025": 108891, "FY2024": 71523, "FY2023": 40585, "FY2022": 28211}),
    ("DATA", "Goodwill", {"FY2026": 38347, "FY2025": 35890, "FY2024": 35890, "FY2023": 35890, "FY2022": 35890}),
    ("TOTAL", "Total assets", {"FY2026": 16639934, "FY2025": 15697672, "FY2024": 14767892, "FY2023": 13711495, "FY2022": 11905521, "FY2021": 7048834}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2026": 12691991, "FY2025": 12066650, "FY2024": 10970237, "FY2023": 10551820, "FY2022": 9027413, "FY2021": 5827581}),
    ("DATA", "Deposits from banks", {"FY2026": 2539524, "FY2025": 2278221, "FY2024": 2420471, "FY2023": 2274306, "FY2022": 2283821}),
    ("DATA", "Central Bank Facilities (FY2021 - TFSME drawdown, predates Deposits from banks presentation)", {"FY2021": 1000000}),
    ("DATA", "Derivative liabilities", {"FY2026": 39098, "FY2025": 49052, "FY2024": 51417, "FY2023": 55452, "FY2022": 330, "FY2021": 818}),
    ("DATA", "Other liabilities", {"FY2026": 106320, "FY2025": 145617, "FY2024": 367422, "FY2023": 96958, "FY2022": 138614, "FY2021": 39141}),
    ("DATA", "Deferred income", {"FY2026": 17245, "FY2025": 59980, "FY2024": 47873, "FY2023": 32380, "FY2022": 23059, "FY2021": 38463}),
    ("DATA", "Provisions", {"FY2026": 33775, "FY2025": 51396, "FY2024": 11507, "FY2023": 1342, "FY2022": 1242, "FY2021": 2000}),
    ("DATA", "Current tax liability", {"FY2026": 7036, "FY2023": 3960, "FY2022": 618}),
    ("DATA", "Deferred tax liability", {"FY2025": 704, "FY2024": 9195}),
    ("TOTAL", "Total liabilities", {"FY2026": 15434989, "FY2025": 14651620, "FY2024": 13878122, "FY2023": 13016218, "FY2022": 11475097, "FY2021": 6908003}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2026": 12, "FY2025": 12, "FY2024": 12, "FY2023": 12, "FY2022": 11, "FY2021": 9}),
    ("DATA", "Share premium", {"FY2026": 0, "FY2025": 608833, "FY2024": 608833, "FY2023": 608833, "FY2022": 478333, "FY2021": 253335}),
    ("DATA", "Merger reserve", {"FY2026": 623833, "FY2025": 15000, "FY2024": 15000, "FY2023": 15000, "FY2022": 15000}),
    ("DATA", "Cash flow hedging reserve", {"FY2026": 427, "FY2025": 9834, "FY2024": 17133, "FY2023": -10246}),
    ("DATA", "Other reserves (own shares held/share awards/sundry/FX - see source note)", {"FY2026": -19020, "FY2025": -31277, "FY2024": -44136, "FY2023": 9267, "FY2022": 7525, "FY2021": 2980}),
    ("DATA", "Retained earnings / (Accumulated losses)", {"FY2026": 599693, "FY2025": 443650, "FY2024": 292928, "FY2023": 72411, "FY2022": -70445, "FY2021": -115493}),
    ("TOTAL", "Total equity", {"FY2026": 1204945, "FY2025": 1046052, "FY2024": 889770, "FY2023": 695277, "FY2022": 430424, "FY2021": 140831}),
    ("TOTAL", "Total liabilities and equity", {"FY2026": 16639934, "FY2025": 15697672, "FY2024": 14767892, "FY2023": 13711495, "FY2022": 11905521, "FY2021": 7048834}),
]

# FY2017-FY2018 are transcribed from Starling's original official annual
# reports (rather than back-filled from later comparatives).  The old reports
# use a materially different line presentation, so only exact line matches
# are carried into the extended ladder.
_OLD_BS = {
    "FY2018": {"Loans and advances to banks (FY2021-FY2023: includes cash and cash equivalents - see source note)": 187008,
               "Total debt securities": 18039, "Loans and advances to customers": 8698,
               "Property, plant and equipment and right of use assets": 616,
               "Intangible assets": 13221, "Other assets": 7087, "Total assets": 234669,
               "Customer deposits": 202323, "Provisions": 202, "Other liabilities": 3614,
               "Deferred income": 531, "Total liabilities": 206670, "Share capital": 5,
               "Share premium": 67784, "Other reserves (own shares held/share awards/sundry/FX - see source note)": 319,
               "Retained earnings / (Accumulated losses)": -40109, "Total equity": 27999,
               "Total liabilities and equity": 234669},
    "FY2017": {"Loans and advances to banks (FY2021-FY2023: includes cash and cash equivalents - see source note)": 37544,
               "Total debt securities": 3014, "Loans and advances to customers": 804,
               "Property, plant and equipment and right of use assets": 253,
               "Intangible assets": 9330, "Other assets": 2332, "Total assets": 53277,
               "Customer deposits": 18083, "Provisions": 183, "Other liabilities": 808,
               "Deferred income": 1485, "Total liabilities": 20559, "Share capital": 5,
               "Share premium": 47846, "Other reserves (own shares held/share awards/sundry/FX - see source note)": -94,
               "Retained earnings / (Accumulated losses)": -15039, "Total equity": 32718,
               "Total liabilities and equity": 53277},
}
for _kind, _label, _values in balance_sheet_rows:
    for _year, _old in _OLD_BS.items():
        if _label in _old:
            _values[_year] = _old[_label]

bw.add_balance_sheet_sheet(
    title="Starling Bank Limited — Balance Sheet",
    subtitle="Group/consolidated basis, £'000. Total assets = Total liabilities + Total equity for every year; "
              "Total equity ties exactly to the Statement of Changes in Equity sheet's own opening/closing "
              "balances - zero plug rows. FY2021: 16-month period (†). FY2026: Starling Group Holdings Limited (‡).",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss (Consolidated Statement of Comprehensive Income) - two
# presentation blocks, mirroring the Cash Flow Statement sheet's existing
# FY2021-2023 vs FY2024-2026 convention (see PRESENTATION NOTE above).
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income (FY2021-FY2025 presentation)", {}),
    ("DATA", "Interest income", {"FY2025": 811695, "FY2024": 754808, "FY2023": 403103, "FY2022": 126614}),
    ("DATA", "Interest expense", {"FY2025": -221533, "FY2024": -161937, "FY2023": -54258, "FY2022": -4902}),
    ("TOTAL", "Net interest income", {"FY2025": 590162, "FY2024": 592871, "FY2023": 348845, "FY2022": 121712, "FY2021": 59253}),
    ("DATA", "Fees and commissions income", {"FY2025": 128306, "FY2024": 119467, "FY2023": 112413, "FY2022": 86041}),
    ("DATA", "Fees and commissions expense", {"FY2025": -33539, "FY2024": -35044, "FY2023": -38023, "FY2022": -28311}),
    ("TOTAL", "Net fees and commissions", {"FY2025": 94767, "FY2024": 84423, "FY2023": 74390, "FY2022": 57730, "FY2021": 33884}),
    ("DATA", "Other (expense)/income", {"FY2025": -4546, "FY2024": -30176, "FY2023": -8421, "FY2022": 8624, "FY2021": 4452}),
    ("DATA", "Credit for eligible spend (CIF)", {"FY2023": 10447, "FY2022": 32958, "FY2021": 46044}),
    ("TOTAL", "Total income", {"FY2025": 680383, "FY2024": 647118, "FY2023": 414814, "FY2022": 188066, "FY2021": 97589}),
    ("DATA", "Operating expenses / Administrative expenses", {"FY2025": -460213, "FY2024": -332130, "FY2023": -220674, "FY2022": -178336, "FY2021": -158981}),
    ("DATA", "Impairment release/(charge) and charge-offs", {"FY2025": 3243, "FY2024": -13889, "FY2023": -9991, "FY2022": -10636, "FY2021": -16106}),
    ("TOTAL", "Profit/(loss) before taxation", {"FY2025": 223413, "FY2024": 301099, "FY2023": 194596, "FY2022": 32052, "FY2021": -31454}),
    ("DATA", "Tax charge/(credit)", {"FY2025": -72691, "FY2024": -81098, "FY2023": -51740, "FY2022": 12886, "FY2021": 8135}),
    ("TOTAL", "Profit/(loss) after taxation", {"FY2025": 150722, "FY2024": 220001, "FY2023": 142856, "FY2022": 44938, "FY2021": -23319}),
    ("SECTION", "Other comprehensive income, net of tax (FY2021-FY2025 presentation)", {}),
    ("DATA", "Translation of subsidiary company", {"FY2025": 7, "FY2024": 25, "FY2023": 47, "FY2022": -4}),
    ("DATA", "Cash flow hedges (net of tax)", {"FY2025": -7299, "FY2024": 27379, "FY2023": -10246}),
    ("TOTAL", "Other comprehensive income/(loss), net of tax", {"FY2025": -7292, "FY2024": 27404, "FY2023": -10199, "FY2022": -4, "FY2021": 0}),
    ("TOTAL", "Total comprehensive income/(loss) for the year, net of tax (FY2021-FY2025 presentation)", {"FY2025": 143430, "FY2024": 247405, "FY2023": 132657, "FY2022": 44934, "FY2021": -23319}),
    ("SECTION", "Income statement (FY2026 presentation - Revenue/Cost of revenue/Gross profit structure)", {}),
    ("DATA", "Interest income (FY2026 presentation)", {"FY2026": 759202}),
    ("DATA", "Fee and commission income (FY2026 presentation)", {"FY2026": 128153}),
    ("TOTAL", "Revenue (FY2026 presentation)", {"FY2026": 887355}),
    ("DATA", "Interest expense (FY2026 presentation)", {"FY2026": -189263}),
    ("DATA", "Fee expense and cost of services (FY2026 presentation)", {"FY2026": -46579}),
    ("DATA", "Impairment (charge)/release (FY2026 presentation)", {"FY2026": -6649}),
    ("TOTAL", "Cost of revenue (FY2026 presentation)", {"FY2026": -242491}),
    ("TOTAL", "Gross profit (FY2026 presentation)", {"FY2026": 644864}),
    ("DATA", "Other income/(expense) (FY2026 presentation)", {"FY2026": 14209}),
    ("DATA", "Operating expenses (FY2026 presentation)", {"FY2026": -441955}),
    ("TOTAL", "Profit before taxation (FY2026 presentation)", {"FY2026": 217118}),
    ("DATA", "Tax charge (FY2026 presentation)", {"FY2026": -61075}),
    ("TOTAL", "Profit after taxation (FY2026 presentation)", {"FY2026": 156043}),
    ("SECTION", "Other comprehensive income, net of tax (FY2026 presentation)", {}),
    ("DATA", "Translation of subsidiary companies (FY2026 presentation)", {"FY2026": -11}),
    ("DATA", "Cash flow hedges (net of tax) (FY2026 presentation)", {"FY2026": -9407}),
    ("TOTAL", "Other comprehensive income/(loss), net of tax (FY2026 presentation)", {"FY2026": -9418}),
    ("TOTAL", "Total comprehensive income for the year, net of tax (FY2026 presentation)", {"FY2026": 146625}),
]

bw.add_income_statement_sheet(
    title="Starling Bank Limited — Profit & Loss",
    subtitle="Group/consolidated basis, £'000. 'Total comprehensive income/(loss) for the year' ties exactly to "
              "Profit/(loss) after taxation + Other comprehensive income for every year. FY2026 uses a different "
              "Revenue/Cost-of-revenue/Gross-profit presentation than FY2021-FY2025 - see source note.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - equity reconciliation ladder steps 2-3:
# built year-by-year, confirmed against next year's opening AND that
# year's own Balance Sheet Total equity above (all 6 years tie exactly).
# Zero undocumented plug rows. See PRESENTATION NOTE above for the
# Merger reserve / Cash flow hedging reserve / Other reserves column split.
# ---------------------------------------------------------------
EQUITY_HEADERS = [
    "Share capital", "Share premium", "Merger reserve", "Cash flow hedging reserve", "Other reserves",
    "Retained earnings", "Total equity",
]

equity_rows = [
    ("TOTAL", "Balance at 30 November 2019", (7, 159332, None, None, 761, -92174, 67926)),
    ("DATA", "Proceeds from issue of shares, less expenses", (2, 94003, None, None, None, None, 94005)),
    ("DATA", "Loss for the period", (None, None, None, None, None, -23319, -23319)),
    ("DATA", "Fair value of shares allocated to employees", (None, None, None, None, 2128, None, 2128)),
    ("DATA", "Translation of subsidiary company", (None, None, None, None, 91, None, 91)),
    ("TOTAL", "Balance at 31 March 2021", (9, 253335, None, None, 2980, -115493, 140831)),
    ("DATA", "Proceeds from issue of shares, less expenses (of which £15,000k created the Merger reserve on the Fleet Mortgages Limited acquisition)", (2, 224998, 15000, None, None, None, 240000)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 44938, 44938)),
    ("DATA", "Translation of subsidiary company", (None, None, None, None, -4, None, -4)),
    ("DATA", "Cost of share award schemes, net of tax", (None, None, None, None, 4549, 110, 4659)),
    ("TOTAL", "Balance at 31 March 2022 / 1 April 2022", (11, 478333, 15000, None, 7525, -70445, 430424)),
    ("DATA", "Proceeds from issue of shares, less expenses", (1, 130500, None, None, None, None, 130501)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 142856, 142856)),
    ("DATA", "Translation of subsidiary company", (None, None, None, None, 47, None, 47)),
    ("DATA", "Cash flow hedge", (None, None, None, -10246, None, None, -10246)),
    ("DATA", "Cost of share award schemes, net of tax", (None, None, None, None, 1695, None, 1695)),
    ("TOTAL", "Balance at 31 March 2023 / 1 April 2023", (12, 608833, 15000, -10246, 9267, 72411, 695277)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 220001, 220001)),
    ("DATA", "Cash flow hedge", (None, None, None, 27379, None, None, 27379)),
    ("DATA", "Translation of subsidiary company", (None, None, None, None, 25, None, 25)),
    ("DATA", "Purchase of own shares", (None, None, None, None, -56362, None, -56362)),
    ("DATA", "Cost of share award schemes, net of tax", (None, None, None, None, 3450, None, 3450)),
    ("DATA", "Transfer from share award reserve", (None, None, None, None, -516, 516, 0)),
    ("TOTAL", "Balance at 31 March 2024 / 1 April 2024", (12, 608833, 15000, 17133, -44136, 292928, 889770)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 150722, 150722)),
    ("DATA", "Cash flow hedge", (None, None, None, -7299, None, None, -7299)),
    ("DATA", "Translation of subsidiary company", (None, None, None, None, 7, None, 7)),
    ("DATA", "Cost of share award schemes, net of tax", (None, None, None, None, 12852, None, 12852)),
    ("TOTAL", "Balance at 31 March 2025 / 1 April 2025", (12, 608833, 15000, 9834, -31277, 443650, 1046052)),
    ("DATA", "Profit for the year", (None, None, None, None, None, 156043, 156043)),
    ("DATA", "Cash flow hedge", (None, None, None, -9407, None, None, -9407)),
    ("DATA", "Translation of subsidiary companies", (None, None, None, None, -11, None, -11)),
    ("DATA", "Merger reserve on Group reorganisation (SGHL inserted as new ultimate parent - see entity note)", (None, -608833, 608833, None, None, None, 0)),
    ("DATA", "Warrants issued", (None, None, None, None, 1372, None, 1372)),
    ("DATA", "Cost of share award schemes, net of tax", (None, None, None, None, 10896, None, 10896)),
    ("TOTAL", "Balance at 31 March 2026", (12, 0, 623833, 427, -19020, 599693, 1204945)),
]

bw.add_equity_changes_sheet(
    title="Starling Bank Limited — Statement of Changes in Equity",
    subtitle="Group/consolidated basis, £'000, chronological (oldest to newest). Each year's closing Total equity "
              "ties exactly to that year's own Balance Sheet Total equity and to the next year's opening balance - "
              "zero undocumented plug rows across all 6 years.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=380,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) for the period after taxation (FY2021-FY2023 presentation)", {"FY2023": 142856, "FY2022": 44938, "FY2021": -23319}),
    ("SECTION", "Adjustments for non-cash items (FY2021-FY2023 presentation)", {}),
    ("DATA", "Depreciation and Amortisation", {"FY2023": 10953, "FY2022": 6384, "FY2021": 7045}),
    ("DATA", "Cost of Share Award Schemes, Net of Tax / FV of Shares Allocated to Employees", {"FY2023": 1323, "FY2022": 4659, "FY2021": 1927}),
    ("DATA", "Change in Derivatives and Fair Value on Hedging Relationships", {"FY2023": 6487, "FY2022": -7905}),
    ("DATA", "Net Increase in Fair Value of Derivatives (FY2021 presentation)", {"FY2021": -12670}),
    ("DATA", "Net Increase in Fair Value of Assets Designated as Hedged Items (FY2021 presentation)", {"FY2021": 12520}),
    ("DATA", "Impairment and Charge-offs", {"FY2023": 9991, "FY2022": 10226, "FY2021": 16106}),
    ("DATA", "Recognition of Right of Use Asset (FY2021 presentation)", {"FY2021": -5527}),
    ("DATA", "Foreign Exchange Losses on Consolidation (FY2021 presentation)", {"FY2021": 91}),
    ("DATA", "Disposal of Intangible Assets (FY2021 presentation)", {"FY2021": 358}),
    ("DATA", "Net Increase in Deferred Tax Asset (adjustment)", {"FY2021": -6088}),
    ("DATA", "Taxation Charged to the Income Statement", {"FY2023": 51740}),
    ("DATA", "Other Non-Cash Items", {"FY2023": -13652, "FY2022": 1479}),
    ("SECTION", "Net changes in operating assets and liabilities (FY2021-FY2023 presentation)", {}),
    ("DATA", "Movement in Loans and Advances to Banks", {"FY2023": -9835, "FY2022": -16523}),
    ("DATA", "Net (Increase) in Loans and Advances to Customers", {"FY2023": -1567215, "FY2022": -1007837, "FY2021": -2203378}),
    ("DATA", "Net (Increase) in Deferred Tax Asset (asset movement)", {"FY2022": -15897}),
    ("DATA", "Net (Increase) in Other Assets", {"FY2023": -5399, "FY2022": -61397, "FY2021": -31818}),
    ("DATA", "Net Increase in Customer Deposits", {"FY2023": 1524407, "FY2022": 3199715, "FY2021": 4820298}),
    ("DATA", "Net Increase in Central Bank Facilities (FY2021 presentation)", {"FY2021": 1000000}),
    ("DATA", "Net (Decrease)/Increase in Deposits from Banks", {"FY2023": -9515, "FY2022": 1281380}),
    ("DATA", "Net Increase/(Decrease) in Provisions for Liabilities and Charges", {"FY2023": 232, "FY2022": -758, "FY2021": -680}),
    ("DATA", "Net (Decrease)/Increase in Other Liabilities and Accruals", {"FY2023": -51253, "FY2022": 104310, "FY2021": 969}),
    ("DATA", "Net Increase/(Decrease) in Deferred Income", {"FY2023": 16202, "FY2022": -3994, "FY2021": -44894}),
    ("DATA", "Taxation Paid (FY2022-FY2023 presentation)", {"FY2023": -26720, "FY2022": -3321}),
    ("TOTAL", "Net Cash Flows from Operating Activities (FY2021-FY2023 presentation)", {"FY2023": 80602, "FY2022": 3535459, "FY2021": 3530940}),
    ("SECTION", "Adjustments and net changes (FY2024-FY2026 presentation, summarised - see note for breakdown)", {}),
    ("DATA", "Profit for the period after taxation (FY2024-FY2026 presentation)", {"FY2026": 156043, "FY2025": 150722, "FY2024": 220001}),
    ("DATA", "Non-cash movements (as reported)", {"FY2026": 109080, "FY2025": 165605, "FY2024": 155782}),
    ("DATA", "Movement in operating assets (as reported)", {"FY2026": -541473, "FY2025": -30989, "FY2024": 194795}),
    ("DATA", "Movement in operating liabilities (as reported)", {"FY2026": 505769, "FY2025": 793034, "FY2024": 813947}),
    ("DATA", "Taxation paid (FY2024-FY2026 presentation)", {"FY2026": -46085, "FY2025": -61999, "FY2024": -94266}),
    ("TOTAL", "Net cash flows from operating activities (FY2024-FY2026 presentation)", {"FY2026": 183334, "FY2025": 1016373, "FY2024": 1290259}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of Property, Plant and Equipment", {"FY2023": -2824, "FY2022": -1279, "FY2021": -1131}),
    ("DATA", "Purchase of property, plant and equipment (FY2024-FY2026 presentation)", {"FY2026": -6034, "FY2025": -3167, "FY2024": -4728}),
    ("DATA", "Net Purchases of Debt Securities (FY2022-FY2023 presentation)", {"FY2023": -161608, "FY2022": -814284}),
    ("DATA", "Net Increase in Debt Securities (FY2021 presentation)", {"FY2021": -1184380}),
    ("DATA", "Purchases of debt securities (FY2024-FY2026 presentation)", {"FY2026": -4462187, "FY2025": -1378404, "FY2024": -1577646}),
    ("DATA", "Proceeds from maturity and sale of debt securities (FY2024-FY2026 presentation)", {"FY2026": 1575165, "FY2025": 735088, "FY2024": 748813}),
    ("DATA", "Acquisition of Subsidiary, Net of Cash Acquired", {"FY2022": -36160}),
    ("DATA", "PPE and Intangibles on Acquisition of Subsidiary", {"FY2022": -8377}),
    ("DATA", "Net cash on acquisition of subsidiary (FY2026 presentation)", {"FY2026": -2205}),
    ("DATA", "Purchase and Development of Intangible Assets", {"FY2023": -27643, "FY2022": -19170}),
    ("DATA", "Capitalisation of Intangible Assets (FY2021 presentation)", {"FY2021": -5623}),
    ("DATA", "Purchase and development of intangible assets (FY2024-FY2026 presentation)", {"FY2026": -75792, "FY2025": -56997, "FY2024": -43278}),
    ("TOTAL", "Net Cash Flows from Investing Activities", {"FY2026": -2971053, "FY2025": -703480, "FY2024": -876839, "FY2023": -192075, "FY2022": -879270, "FY2021": -1191134}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Issuance of Ordinary Shares Less Cost of Issuance", {"FY2023": 130500, "FY2022": 240000, "FY2021": 94012}),
    ("DATA", "Purchase of own shares", {"FY2024": -56362}),
    ("DATA", "Drawdown of funding from central banks", {"FY2026": 900000}),
    ("DATA", "Repayment of funding from central banks", {"FY2026": -600000, "FY2025": -50000}),
    ("DATA", "Repayment of Lease Liabilities", {"FY2023": -68, "FY2022": -1780, "FY2021": -2174}),
    ("DATA", "Repayment of lease liabilities (FY2024-FY2026 presentation)", {"FY2026": -4120, "FY2025": -2710, "FY2024": -2154}),
    ("TOTAL", "Net Cash Flows from Financing Activities", {"FY2026": 295880, "FY2025": -52710, "FY2024": -58516, "FY2023": 130432, "FY2022": 238220, "FY2021": 91838}),
    ("TOTAL", "Net Increase/(Decrease) in Cash and Cash Equivalents", {"FY2026": -2491839, "FY2025": 260183, "FY2024": 354904, "FY2023": 18859, "FY2022": 2894409, "FY2021": 2431644}),
    ("DATA", "Cash and Cash Equivalents at Beginning of Period/Year", {"FY2026": 6717177, "FY2025": 6456994, "FY2024": 6102090, "FY2023": 6083131, "FY2022": 3188722, "FY2021": 764705}),
    ("TOTAL", "Cash and Cash Equivalents at End of Period/Year", {"FY2026": 4225338, "FY2025": 6717177, "FY2024": 6456994, "FY2023": 6102090, "FY2022": 6083131, "FY2021": 3196349}),
]

bw.add_cash_flow_sheet(
    title="Starling Bank Limited — Consolidated Cash Flow Statement",
    subtitle="Group/consolidated basis, £'000. FY2021: 16-month period (†). FY2026: Starling Group Holdings Limited (‡). See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=250,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality - lending exposure and impairment provision by IFRS 9
# stage, Group basis. FY2021 genuinely doesn't disclose a by-stage table
# (introduced from the FY2022 Annual Report onward, coinciding with the
# Fleet Mortgages acquisition and Government-scheme lending buildout) -
# confirmed non-disclosure, not an access gap - left blank.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Total exposure after guarantee, by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2026": 4862307, "FY2025": 4165490, "FY2024": 3725761, "FY2023": 3571338, "FY2022": 1633418}),
    ("DATA", "Stage 2", {"FY2026": 252112, "FY2025": 228850, "FY2024": 266374, "FY2023": 144105, "FY2022": 43581}),
    ("DATA", "Stage 3", {"FY2026": 163254, "FY2025": 159469, "FY2024": 160167, "FY2023": 103707, "FY2022": 55960}),
    ("TOTAL", "Total exposure after guarantee", {"FY2026": 5277673, "FY2025": 4553809, "FY2024": 4152302, "FY2023": 3819150, "FY2022": 1732959}),
    ("SECTION", "Impairment provision, by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2026": 7767, "FY2025": 6344, "FY2024": 9174, "FY2023": 11462, "FY2022": 13637}),
    ("DATA", "Stage 2", {"FY2026": 5471, "FY2025": 5166, "FY2024": 9974, "FY2023": 5779, "FY2022": 3663}),
    ("DATA", "Stage 3", {"FY2026": 11239, "FY2025": 10403, "FY2024": 28722, "FY2023": 18381, "FY2022": 9772}),
    ("TOTAL", "Total impairment provision", {"FY2026": 24477, "FY2025": 21913, "FY2024": 47870, "FY2023": 35622, "FY2022": 27072}),
    ("SECTION", "Net exposure, by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2026": 4854540, "FY2025": 4159146, "FY2024": 3716587, "FY2023": 3559876, "FY2022": 1619781}),
    ("DATA", "Stage 2", {"FY2026": 246641, "FY2025": 223684, "FY2024": 256400, "FY2023": 138326, "FY2022": 39918}),
    ("DATA", "Stage 3", {"FY2026": 152015, "FY2025": 149066, "FY2024": 131445, "FY2023": 85326, "FY2022": 46188}),
    ("TOTAL", "Net exposure", {"FY2026": 5253196, "FY2025": 4531896, "FY2024": 4104432, "FY2023": 3783528, "FY2022": 1705887}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "% Coverage - Stage 1", {"FY2026": "0.2%", "FY2025": "0.2%", "FY2024": "0.2%", "FY2023": "0.3%", "FY2022": "0.8%"}),
    ("DATA", "% Coverage - Stage 2", {"FY2026": "2.2%", "FY2025": "2.3%", "FY2024": "3.7%", "FY2023": "4.0%", "FY2022": "8.4%"}),
    ("DATA", "% Coverage - Stage 3", {"FY2026": "6.9%", "FY2025": "6.5%", "FY2024": "17.9%", "FY2023": "17.7%", "FY2022": "17.5%"}),
    ("DATA", "% Coverage - Total", {"FY2026": "0.5%", "FY2025": "0.5%", "FY2024": "1.2%", "FY2023": "0.9%", "FY2022": "1.6%"}),
    ("DATA", "NPL ratio (Stage 3 exposure / Total exposure after guarantee)", {"FY2026": "3.09%", "FY2025": "3.50%", "FY2024": "3.86%", "FY2023": "2.72%", "FY2022": "3.23%"}),
]

bw.add_asset_quality_sheet(
    title="Starling Bank Limited — Asset Quality",
    subtitle="Group/consolidated basis, £'000. Lending exposure and impairment provision by IFRS 9 stage, 'Total "
              "exposure after guarantee' basis (includes off-balance-sheet undrawn facilities net of UK "
              "government guarantees). FY2021 genuinely does not disclose a by-stage table - see source note.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Group basis, 'Lending exposure and impairment provision, by stage and coverage' table:\n"
        f"FY2026: Starling Group Holdings Limited Annual Report and Accounts 2026, p.112 - {AR26_SGHL_URL}\n"
        f"FY2025 & FY2024: Starling Bank Limited Annual Report and Accounts 2025, p.106 - {AR25_URL}\n"
        f"FY2023 & FY2022: Starling Bank Limited Annual Report 2023, p.69-70 - {AR23_URL}\n"
        "FY2021: not disclosed at this granularity - Starling Bank Limited's Annual Report and Consolidated "
        "Financial Statements for the period ended 31 March 2021 does not include a lending-exposure-by-IFRS-9-"
        "stage table (this disclosure was introduced from the FY2022 Annual Report onward); only an aggregate "
        "impairment-provision-sensitivity figure (£17,256k, Retail + SME + undrawn overdrafts) is disclosed for "
        "FY2021, which is not on a comparable 'exposure after guarantee, all products' basis - confirmed "
        "non-disclosure at this granularity, not an access gap.\n"
        "NPL ratio is derived (Stage 3 exposure after guarantee / Total exposure after guarantee); not itself a "
        "disclosed figure.\n\n" + ENTITY_NOTE
    ),
    first_col_width=62,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES_ALL, note=note, first_col_width=52, source_height=150)

# ---------------------------------------------------------------
# KM1 Key Metrics - Starling's own published key-metrics template.
#
# Starling prints the template UNNUMBERED and heads it "4.1 Key metrics"
# rather than "KM1" - the string "KM1" appears nowhere in any edition. It is
# nonetheless the template: the full UK row set is there, in template order,
# from own funds through SREP, buffers, leverage, LCR and NSFR. Rows are
# therefore reproduced with the bank's own labels and no row numbers invented.
#
# FY2026-FY2022 come from their own editions. FY2021 is filled from the
# FY2022 edition's 31 March 2021 comparative column - the FY2021 edition
# pre-dates the template and prints capital, leverage and liquidity in three
# separate bespoke sections instead. FY2020-FY2017 are blank: no Pillar 3
# report exists for those years (Starling's Pillar 3 series begins with 2021).
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) capital (£'000)",
     {"FY2026": 1123255, "FY2025": 1000231, "FY2024": 870769, "FY2023": 710614, "FY2022": 397502, "FY2021": 136769}),
    ("DATA", "Tier 1 capital (£'000)",
     {"FY2026": 1123255, "FY2025": 1000231, "FY2024": 870769, "FY2023": 710614, "FY2022": 397502, "FY2021": 136769}),
    ("DATA", "Total capital (£'000)",
     {"FY2026": 1123255, "FY2025": 1000231, "FY2024": 870769, "FY2023": 710614, "FY2022": 397502, "FY2021": 136769}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "Total risk-weighted exposure amount (£'000)",
     {"FY2026": 3930308, "FY2025": 3170032, "FY2024": 2675477, "FY2023": 1894758, "FY2022": 994828, "FY2021": 285689}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Common Equity Tier 1 ratio (%)",
     {"FY2026": "28.58 %", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.90%"}),
    ("DATA", "Tier 1 ratio (%)",
     {"FY2026": "28.58 %", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.90%"}),
    ("DATA", "Total capital ratio (%)",
     {"FY2026": "28.58 %", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.90%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Additional CET1 SREP requirements (%)",
     {"FY2026": "1.40 %", "FY2025": "2.94%", "FY2024": "2.94%", "FY2023": "2.94%", "FY2022": "0%", "FY2021": "5.33%"}),
    ("DATA", "Additional AT1 SREP requirements (%)",
     {"FY2026": "0.46 %", "FY2025": "0.97%", "FY2024": "0.97%", "FY2023": "0.97%", "FY2022": "0%", "FY2021": "1.78%"}),
    ("DATA", "Additional T2 SREP requirements (%)",
     {"FY2026": "0.62 %", "FY2025": "1.31%", "FY2024": "1.31%", "FY2023": "1.31%", "FY2022": "0%", "FY2021": "2.37%"}),
    ("DATA", "Total SREP own funds requirements (%)",
     {"FY2026": "10.48 %", "FY2025": "13.22%", "FY2024": "13.22%", "FY2023": "13.22%", "FY2022": "8.00%", "FY2021": "17.47%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Capital conservation buffer (%)",
     {"FY2026": "2.50 %", "FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.5%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "Institution specific countercyclical capital buffer (%)",
     {"FY2026": "2.00 %", "FY2025": "2.00%", "FY2024": "2.00%", "FY2023": "1%", "FY2022": "0%", "FY2021": "0%"}),
    ("DATA", "Combined buffer requirement (%)",
     {"FY2026": "4.50 %", "FY2025": "4.50%", "FY2024": "4.50%", "FY2023": "3.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "Overall capital requirements (%)",
     {"FY2026": "14.98 %", "FY2025": "17.72%", "FY2024": "17.72%", "FY2023": "16.72%", "FY2022": "10.50%", "FY2021": "19.97%"}),
    ("DATA", "CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2026": "22.68 %", "FY2025": "24.12%", "FY2024": "25.11%", "FY2023": "30.07%", "FY2022": 293045, "FY2021": 79716}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "Total exposure measure excluding claims on central banks (£'000)",
     {"FY2026": 12608384, "FY2025": 8976790, "FY2024": 8383435, "FY2023": 7641617, "FY2022": 5063481, "FY2021": 2546904}),
    ("DATA", "Leverage ratio excluding claims on central banks (%)",
     {"FY2026": "8.91 %", "FY2025": "11.14%", "FY2024": "10.39%", "FY2023": "9.30%", "FY2022": "7.85%", "FY2021": "5.37%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "Total HQLA (average weighted value) (£'000)",
     {"FY2026": 7038393, "FY2025": 6812037, "FY2024": 6510731, "FY2023": 6413925, "FY2022": 5128346, "FY2021": 2402238}),
    ("DATA", "Cash outflows (total weighted value) (£'000)",
     {"FY2026": 1326072, "FY2025": 1477094, "FY2024": 1891560, "FY2023": 1711200, "FY2022": 1211430, "FY2021": 531222}),
    ("DATA", "Cash inflows (total weighted value) (£'000)",
     {"FY2026": 89112, "FY2025": 156237, "FY2024": 446533, "FY2023": 311926, "FY2022": 209396, "FY2021": 41655}),
    ("DATA", "Total net cash outflows (adjusted value) (£'000)",
     {"FY2026": 1236960, "FY2025": 1320857, "FY2024": 1445027, "FY2023": 1399274, "FY2022": 1002034, "FY2021": 489567}),
    ("DATA", "Liquidity Coverage Ratio (%)",
     {"FY2026": "569.01 %", "FY2025": "515.73%", "FY2024": "450.56%", "FY2023": "460%", "FY2022": "515%", "FY2021": "522%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "Total available stable funding (£'000)",
     {"FY2026": 14206855, "FY2025": 13448876, "FY2024": 12578157, "FY2023": 11944952, "FY2022": 10660584}),
    ("DATA", "Total required stable funding (£'000)",
     {"FY2026": 5754691, "FY2025": 5555204, "FY2024": 5646537, "FY2023": 4870012, "FY2022": 4088546}),
    ("DATA", "Net stable funding ratio (%)",
     {"FY2026": "246.87 %", "FY2025": "242.10%", "FY2024": "222.76%", "FY2023": "245%", "FY2022": "261%"}),
]

KM1_SOURCES = (
    "Sources - Starling's own key-metrics template (section 4.1 Key metrics), £'000 and % as printed:\n"
    f"FY2026: Starling Group Pillar 3 report 2026, as at 31 March 2026, p.22-23 - {P3_26_URL}\n"
    f"FY2025: Starling Bank Limited Pillar 3 report 2025, as at 31 March 2025, p.22-23 - {P3_25_URL}\n"
    f"FY2024: Starling Bank Limited Pillar 3 report 2024, as at 31 March 2024, p.23-24 - {P3_24_URL}\n"
    f"FY2023: Starling Bank Limited Pillar 3 Report 2023, as at 31 March 2023, p.21 - {P3_23_URL}\n"
    f"FY2022: Starling Bank Ltd Pillar 3 Report 2022, as at 31 March 2022, p.19 - {P3_22_URL}\n"
    f"FY2021: the FY2022 report's 31 March 2021 comparative column, p.19 - {P3_22_URL}\n\n"
    "LATEST-EDITION CHECK, 2026-09-17: starlingbank.com's investor page refuses this project's automated "
    "fetcher (HTTP 403 with a bot-protection HTML body) - that is a statement about our reach, NOT about what "
    "Starling has published, so it is recorded as blocked rather than as an absence. The documents themselves "
    "fetch normally with a browser user-agent, and were probed directly: Pillar3-2026.pdf returns a 12MB file "
    "with %PDF magic bytes (year ended 31 March 2026, the newest edition and already held here); "
    "Pillar3-2027.pdf does not exist, and is not due. Checked, none newer.\n\n"
    "WHY THIS IS THE KM1 TEMPLATE EVEN THOUGH IT SAYS 'KEY METRICS'. Starling never writes 'KM1' and never "
    "prints the template's row numbers. The test applied here is the ROW SET, not the title or the numbering: "
    "the table carries own funds, risk-weighted exposure amounts, the three capital ratios, the four SREP rows, "
    "the combined-buffer block, the leverage block and the full LCR and NSFR blocks, in template order. Row "
    "numbers have deliberately NOT been added, because the bank did not print them.\n\n"
    "ENTITY: FY2026 is Starling Group Holdings Limited's Regulatory Group (SGHL, SIHL, SBL, SFSSL and Ember), "
    "the basis on which prudential figures are now published following the June 2025 group restructuring - the "
    "same basis as this workbook's other FY2026 Pillar 3 columns, and the reason the FY2026 header carries the "
    "SGHL marker. FY2025-FY2021 are Starling Bank Limited. See the entity note on the Cash Flow Statement "
    "sheet; Starling's own cross-check confirmed the restructuring made no difference to the FY2025 capital "
    "figures, so the series is continuous.\n\n"
    "WHY FY2021 IS FILLED FROM THE FY2022 EDITION: the Pillar 3 Disclosures for 31 March 2021 pre-date the "
    "template and print no key-metrics table at all - capital resources, leverage and liquidity appear in three "
    "separate bespoke sections (5, 5.2 and 12). The FY2022 report prints a full 31 March 2021 comparative "
    "column, which is the only place this table exists for that date, so the FY2021 column here is that "
    "comparative and is labelled as such.\n\n"
    "SOURCE DEFECT, REPRODUCED NOT CORRECTED: in the FY2022 edition the row 'CET1 available after meeting the "
    "total SREP own funds requirements (%)' is captioned as a percentage but printed as a £'000 AMOUNT - "
    "293,045 for 2022 and 79,716 for 2021. The FY2023 edition prints the same two dates as 30.07% and 29.46%. "
    "Both columns here are the FY2022 edition's own figures, as published; the later edition's percentages have "
    "not been substituted, and the amounts have not been converted into percentages.\n\n"
    "CROSS-EDITION DIFFERENCES WORTH KNOWING (each year is its own edition's figure):\n"
    "- FY2023 CET1/Tier 1/Total capital read 710,614 in the FY2023 edition and 710,616 in the FY2024 edition's "
    "comparative. The FY2023 edition's own figure is used, as it is on the metric sheets.\n"
    "- FY2021's LCR reads 522% in the FY2022 edition's comparative (used here) against 506% in the FY2021 "
    "edition's own liquidity section (used on the LCR metric sheet, since that is the figure Starling published "
    "for the year at the time). The same pair of editions differ on the FY2021 HQLA and net-outflow amounts "
    "(2,402,238 / 489,567 here against 3,410,070 / 674,460 on the metric sheet). This is a genuine restatement "
    "between two Starling documents, not a transcription difference, and neither figure has been altered to "
    "match the other.\n"
    "- FY2023's LCR and NSFR are printed to whole percents in their own edition ('460%', '245%') and to two "
    "decimals in the FY2024 edition's comparative. The bank's own precision for the year is kept.\n\n"
    "PRINTED-FORM NOTE: the FY2026 edition puts a space before the per-cent sign ('28.58 %') where earlier "
    "editions do not ('31.55%'). Reproduced as published.\n\n"
    "ROWS LEFT BLANK: FY2021's three NSFR rows are printed as 'n/a' in the FY2022 edition, with its own "
    "footnote explaining that 'NSFR is a new requirement introduced in 2022 as part of CRR 2, thus the Bank "
    "does not provide comparative information for the prior period'. FY2020-FY2017 are blank because Starling "
    "published no Pillar 3 report for those years at all - its series begins with the 31 March 2021 document."
)

bw.add_km1_sheet(
    title="Starling Bank Limited — KM1 Key Metrics",
    subtitle="Starling's own published key-metrics template (its section 4.1), reproduced whole in the bank's "
             "row order, labels and printed precision. Starling prints the template UNNUMBERED and never uses "
             "the string 'KM1', so no row numbers have been added - it is the template on the row-set test. "
             "Amounts in £'000, ratios as printed. FY2026-FY2022 come from their own editions; FY2021 is the "
             "FY2022 edition's comparative column (that year's own report pre-dates the template). FY2026 is "
             "the SGHL Regulatory Group basis - see the source note. FY2020-FY2017 are blank: no Pillar 3 "
             "report exists for those years.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=72,
    source_height=460,
)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2026": 1123255, "FY2025": 1000231, "FY2024": 870769, "FY2023": 710614, "FY2022": 397502, "FY2021": 136769})],
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2026": "28.58%", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.9%"})],
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2026": 1123255, "FY2025": 1000231, "FY2024": 870769, "FY2023": 710614, "FY2022": 397502, "FY2021": 136769})],
    note="Equal to CET1 capital in every year - Starling has never issued Additional Tier 1 or Tier 2 capital ('All "
         "of Starling Bank's capital is Common Equity Tier 1 (CET1)' - FY2024 Pillar 3 report).",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2026": "28.58%", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.9%"})],
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2026": 1123255, "FY2025": 1000231, "FY2024": 870769, "FY2023": 710614, "FY2022": 397502, "FY2021": 136769})],
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2026": "28.58%", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.9%"})],
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2026": 3930308, "FY2025": 3170032, "FY2024": 2675477, "FY2023": 1894758, "FY2022": 994828, "FY2021": 285689})],
)

# ---------------------------------------------------------------
# RWA Breakdown - Pillar 3 UK OV1 template (FY2022-FY2026); FY2021 uses
# the older CRR-era 4-category table (predates the formal KM1/OV1
# template - see ENTITY_NOTE / P3_SOURCES_ALL). All 6 years tie exactly
# to the Total RWAs metric above.
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (Pillar 3 UK OV1 template; FY2021 uses an older CRR-era 4-category "
                "structure - see source note)", {}),
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2026": 2471912, "FY2025": 1987150, "FY2024": 1840844, "FY2023": 1689562, "FY2022": 835048, "FY2021": 227167}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2026": 3283, "FY2025": 4723, "FY2024": 4499, "FY2023": 46355, "FY2022": 92241, "FY2021": 13498}),
    ("DATA", "Credit valuation adjustment (CVA) (FY2021: shown as a separate line, not within CCR)", {"FY2021": 19949}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2026": 231185, "FY2025": 105727, "FY2024": 80923, "FY2023": 4805, "FY2022": 1166}),
    ("DATA", "Market risk (FY2021: de minimis, none shown per Article 351 CRR)", {"FY2021": 0}),
    ("DATA", "Operational risk", {"FY2026": 1223928, "FY2025": 1072432, "FY2024": 749211, "FY2023": 154036, "FY2022": 66372, "FY2021": 25075}),
    ("DATA", "Memo: amounts below thresholds for deduction (250% risk-weight; already included in Credit risk above, not additive)", {"FY2026": 125427, "FY2025": 125427, "FY2024": 125427, "FY2023": 125427, "FY2022": 98731}),
    ("TOTAL", "Total RWAs", {"FY2026": 3930308, "FY2025": 3170032, "FY2024": 2675477, "FY2023": 1894758, "FY2022": 994828, "FY2021": 285689}),
]

bw.add_rwa_breakdown_sheet(
    title="Starling Bank Limited — RWA Breakdown",
    subtitle="Group/consolidated basis for FY2026 (Regulatory Group - see entity note), Bank basis FY2021-FY2025, "
              "£'000. The 'Memo' row is already included within Credit risk and must NOT be added when summing to "
              "Total RWAs (per the source template's own footnote) - the other categories sum exactly to Total RWAs.",
    rows=rwa_breakdown_rows,
    sources_text=P3_SOURCES_ALL + (
        "\n\nRWA breakdown table specifically ('Overview of risk weighted exposure amounts' / '4.2'):\n"
        f"FY2026: p.24 - {P3_26_URL}\n"
        f"FY2025 & FY2024: p.24 - {P3_25_URL}\n"
        f"FY2023 & FY2022: p.21 - {P3_23_URL}\n"
        f"FY2021: 5.1 Risk Weighted Exposure Amounts, p.23 (older 4-category CRR-era structure: Credit Risk, "
        f"Counterparty Credit Risk, Credit Valuation Adjustment shown separately from CCR, Market Risk, "
        f"Operational Risk - no Securitisation line disclosed that year) - {P3_21_URL}"
    ),
    first_col_width=68,
    source_height=250,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2026": 12608384, "FY2025": 8976790, "FY2024": 8383435, "FY2023": 7641617, "FY2022": 5063481}),
        ("Leverage ratio excluding claims on central banks / UK leverage ratio (%)", {"FY2026": "8.91%", "FY2025": "11.14%", "FY2024": "10.39%", "FY2023": "9.30%", "FY2022": "7.85%", "FY2021": "5.4%"}),
        ("Leverage ratio including claims on central banks / CRR (EU) leverage ratio (%) (FY2021 only, pre-KM1 template)", {"FY2021": "1.9%"}),
    ],
    note="FY2021 predates the formal KM1 template and did not disclose a £ exposure measure, only two ratios: "
         "a 'UK leverage ratio' (excluding central bank exposures, matching the 'excluding claims on central "
         "banks' basis used from FY2022 onward) and a 'CRR (EU) leverage ratio' (including them). Starling noted "
         "it was 'not subject to the PRA Handbook's (UK) leverage ratio' at the time, i.e. this was disclosed "
         "voluntarily rather than as a binding requirement in FY2021.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA) (average weighted value)", {"FY2026": 7038393, "FY2025": 6812037, "FY2024": 6510731, "FY2023": 6413925, "FY2022": 5128346, "FY2021": 3410070}),
        ("Cash outflows (total weighted value)", {"FY2026": 1326072, "FY2025": 1477094, "FY2024": 1891560, "FY2023": 1711200, "FY2022": 1211430}),
        ("Cash inflows (total weighted value)", {"FY2026": 89112, "FY2025": 156237, "FY2024": 446533, "FY2023": 311926, "FY2022": 209396}),
        ("Total net cash outflows (adjusted value)", {"FY2026": 1236960, "FY2025": 1320857, "FY2024": 1445027, "FY2023": 1399274, "FY2022": 1002034, "FY2021": 674460}),
        ("Liquidity Coverage Ratio (%)", {"FY2026": "569.01%", "FY2025": "515.73%", "FY2024": "450.56%", "FY2023": "460%", "FY2022": "515%", "FY2021": "506%"}),
    ],
    note="FY2021 disclosed only Total HQLA and Total Net Cash Outflow (no separate cash inflow/outflow split) - "
         "predates the formal KM1 template. LCR/NSFR are averages over the year in every year shown.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2026": 14206855, "FY2025": 13448876, "FY2024": 12578157, "FY2023": 11944952, "FY2022": 10660584, "FY2021": 6366591}),
        ("Total required stable funding", {"FY2026": 5754691, "FY2025": 5555204, "FY2024": 5646537, "FY2023": 4870012, "FY2022": 4088546, "FY2021": 2127872}),
        ("Net Stable Funding Ratio (%)", {"FY2026": "246.87%", "FY2025": "242.10%", "FY2024": "222.76%", "FY2023": "245%", "FY2022": "261%", "FY2021": "299%"}),
    ],
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed (no numeric ratio published)" for y in YEARS})],
    note="MREL became applicable to Starling from April 2023 (previously not applicable, as for a small "
         "institution). From then, Starling states its capital is maintained 'above MREL requirements plus "
         "buffers at all times' but has never published a numeric MREL ratio or resources figure in any Pillar 3 "
         "report reviewed, FY2021-FY2026 - only this qualitative statement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2026": 16639934, "FY2025": 15697672, "FY2024": 14767892, "FY2023": 13711495, "FY2022": 11905521, "FY2021": 7048834, "FY2018": 234669, "FY2017": 53277}),
        ("Loans and advances to customers", {"FY2026": 5161359, "FY2025": 4670567, "FY2024": 4537663, "FY2023": 4731997, "FY2022": 3234673, "FY2021": 2232846, "FY2018": 8698, "FY2017": 804}),
        ("Customer deposits", {"FY2026": 12691991, "FY2025": 12066650, "FY2024": 10970237, "FY2023": 10551820, "FY2022": 9027413, "FY2021": 5827581, "FY2018": 202323, "FY2017": 18083}),
        ("Total equity", {"FY2026": 1204945, "FY2025": 1046052, "FY2024": 889770, "FY2023": 695277, "FY2022": 430424, "FY2021": 140831, "FY2018": 27999, "FY2017": 32718}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income / Revenue", {"FY2026": 887355, "FY2025": 680383, "FY2024": 647118, "FY2023": 414814, "FY2022": 188066, "FY2021": 97589}),
        ("Operating expenses", {"FY2026": -441955, "FY2025": -460213, "FY2024": -332130, "FY2023": -220674, "FY2022": -178336, "FY2021": -158981}),
        ("Profit/(loss) after taxation", {"FY2026": 156043, "FY2025": 150722, "FY2024": 220001, "FY2023": 142856, "FY2022": 44938, "FY2021": -23319}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2026": 1046052, "FY2025": 889770, "FY2024": 695277, "FY2023": 430424, "FY2022": 140831, "FY2021": 67926}),
        ("Total comprehensive income/(loss) for the year", {"FY2026": 146625, "FY2025": 143430, "FY2024": 247405, "FY2023": 132657, "FY2022": 44934, "FY2021": -23319}),
        ("Other equity movements, net", {"FY2026": 12268, "FY2025": 12852, "FY2024": -52912, "FY2023": 132196, "FY2022": 244659, "FY2021": 96224}),
        ("Closing equity", {"FY2026": 1204945, "FY2025": 1046052, "FY2024": 889770, "FY2023": 695277, "FY2022": 430424, "FY2021": 140831}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flows from operating activities", {
            "FY2023": 80602, "FY2022": 3535459, "FY2021": 3530940,  # FY2021-FY2023 presentation
            "FY2026": 183334, "FY2025": 1016373, "FY2024": 1290259,  # FY2024-FY2026 presentation
        }),
        ("Net cash flows from investing activities", {"FY2026": -2971053, "FY2025": -703480, "FY2024": -876839, "FY2023": -192075, "FY2022": -879270, "FY2021": -1191134}),
        ("Net cash flows from financing activities", {"FY2026": 295880, "FY2025": -52710, "FY2024": -58516, "FY2023": 130432, "FY2022": 238220, "FY2021": 91838}),
        ("Cash and cash equivalents at end of period/year", {"FY2026": 4225338, "FY2025": 6717177, "FY2024": 6456994, "FY2023": 6102090, "FY2022": 6083131, "FY2021": 3196349}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2026": "28.58%", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.9%"}),
        ("Tier 1 Ratio", {"FY2026": "28.58%", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.9%"}),
        ("Total Capital Ratio", {"FY2026": "28.58%", "FY2025": "31.55%", "FY2024": "32.55%", "FY2023": "37.50%", "FY2022": "39.96%", "FY2021": "47.9%"}),
        ("Leverage Ratio", {"FY2026": "8.91%", "FY2025": "11.14%", "FY2024": "10.39%", "FY2023": "9.30%", "FY2022": "7.85%", "FY2021": "5.4%"}),
        ("LCR", {"FY2026": "569.01%", "FY2025": "515.73%", "FY2024": "450.56%", "FY2023": "460%", "FY2022": "515%", "FY2021": "506%"}),
        ("NSFR", {"FY2026": "246.87%", "FY2025": "242.10%", "FY2024": "222.76%", "FY2023": "245%", "FY2022": "261%", "FY2021": "299%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Net cash from operating activities combines two reporting "
         "presentations Starling used across this period (FY2021-FY2023 vs. FY2024-FY2026); see the Cash Flow "
         "Statement sheet for the distinction. Leverage ratio shown on the 'excluding claims on central banks' "
         "basis for comparability (FY2021 disclosed on the since-retired 'including' CRR basis instead - see "
         "Leverage Ratio sheet).",
)

bw.save("/Users/armaan/code/katalysis/banks/STARLING FINANCIALS.xlsx")
