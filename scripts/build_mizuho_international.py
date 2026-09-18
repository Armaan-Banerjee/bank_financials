import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# Mizuho International plc (company 01203696, FRN 119256), confirmed against
# Banks List 2608.xlsx and Companies House.  The reports present consolidated
# Mizuho International plc Group figures in GBP millions.
YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014", "FY2013", "FY2012", "FY2011", "FY2010", "FY2009", "FY2008"]
Y_CORE = YEARS[:YEARS.index("FY2014") + 1]  # HD-072/075/079: FY2014-floor default for Pillar 3/Asset Quality/RWA Breakdown/Overview


# HD-047: extended FY2014-FY2020 back from FY2021, capped at FY2014 by explicit
# project-wide decision (Pillar 3 pre-CRD IV/Basel III isn't comparable), even
# though the confirmed archive goes back to FY2008 (HD-004). FY2015-FY2020
# Annual Reports and all FY2014-FY2020 Pillar 3 disclosures are on Mizuho's own
# site; FY2014's Annual Report is not (see FY2014 Companies House note below).
#
# HD-075: extended the four statutory-statement sheets only (Balance Sheet,
# P&L, Statement of Changes in Equity, Cash Flow Statement) from FY2014 back
# to FY2008, the real statutory floor per HD-004's targeted scan. Pillar 3,
# Asset Quality and RWA Breakdown are explicitly OUT of scope for this
# extension and are unchanged - their dicts simply have no FY2008-FY2013
# entries, so those sheets still show FY2014 as their earliest column.
# FY2008-FY2013 are all sourced from Mizuho International plc's own
# Companies House statutory filings (see CH_STATUTORY below), the same
# source type already used for FY2014.
AR = {
    # FY2026 (year ended 31 March 2026) added 2026-09-17 from Mizuho's own
    # annual-reports page - the workbook had been a full year stale on this bank.
    "FY2026": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6a90390502fd9a373f296929_f9f197d433ba8e1bc5b2b2b036d0020b_Mizuho_MHI_Annual_Report_2026.pdf",
    "FY2025": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6949753a5e4af5e79887a666_MIzuho_MHI_Annual_Report_2025.pdf",
    "FY2024": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686301edbbd3ea24c5c8059f_mizuho_annual_report_2024_final_v02.pdf",
    "FY2023": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6863021624e9468651ae2fbd_mizuho_annual_report_2023_final_02.pdf",
    "FY2022": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686302389cf6e01446043fd2_2022-mizuho-international-plc-annual-report.pdf",
    "FY2021": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686302637f7fc2c72f2e2f59_2021-mizuho-international-plc-annual-report.pdf",
    "FY2020": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6863028d4802cdc23dd6552c_2020-mizuho-international-plc-annual-report.pdf",
    "FY2019": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686302ac32d1c7376f1f1877_2019-mizuho-international-plc-annual-report.pdf",
    "FY2018": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686302c5e1d535ec3306fbee_2018-mizuho-international-plc-annual-report-1.pdf",
    "FY2017": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686302d732d1c7376f1f2ad2_2017-mizuho-international-plc-annual-report.pdf",
    "FY2016": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686302eda925dd5c1687cecd_2016-mizuho-international-plc-annual-report.pdf",
    "FY2015": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/68630302eca4998ff565c8ea_2015-mizuho-international-plc-annual-report.pdf",
    # FY2014: not on Mizuho's own site (only a "Mizuho Securities UK Holdings"
    # 2014 report is there - a different, parent entity). Sourced instead from
    # Mizuho International plc's own statutory "Full accounts made up to 31
    # March 2014" filed with Companies House 04 Aug 2014 (70 pages).
    "FY2014": "https://find-and-update.company-information.service.gov.uk/company/01203696/filing-history/MzEwNDY4NTMyOGFkaXF6a2N4/document?format=pdf&download=0",
}

# HD-075: FY2008-FY2013 statutory-statement source PDFs, all Mizuho
# International plc's own "Full accounts" (FY2010-2013) / "Group of
# companies' accounts" (FY2008-2009) filed with Companies House - same
# source type as the FY2014 filing above. Confirmed live and downloaded
# 2026-09-06.
CH_STATUTORY = {
    "FY2013": "https://find-and-update.company-information.service.gov.uk/company/01203696/filing-history/MzA4MDE5NTMxMmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2012": "https://find-and-update.company-information.service.gov.uk/company/01203696/filing-history/MzA2NTI2MzY4MGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2011": "https://find-and-update.company-information.service.gov.uk/company/01203696/filing-history/MzA0NDQ4MDc5N2FkaXF6a2N4/document?format=pdf&download=0",
    "FY2010": "https://find-and-update.company-information.service.gov.uk/company/01203696/filing-history/MzAyMzM2MTY3OWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2009": "https://find-and-update.company-information.service.gov.uk/company/01203696/filing-history/MjA0MjM3OTU5NmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2008": "https://find-and-update.company-information.service.gov.uk/company/01203696/filing-history/MjAxMDQ0NzA1NmFkaXF6a2N4/document?format=pdf&download=0",
}
P3 = {
    # FY2026 added 2026-09-17, same latest-edition check as the FY2026 Annual
    # Report above (Mizuho's own Pillar 3 disclosures page).
    "FY2026": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6a903d9cec6eb609b9981dde_MHI%20consolidated%20Pillar%203%20disclosure%202026.pdf",
    "FY2025": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6a903f20d82fcd0100158b9f_MHI%20consolidated%20Pillar%203%20disclosure%202025.pdf",
    "FY2024": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6864747a2fb833ca68387b1e_mhi-consolidated-pillar-3-disclosure-2024-final.pdf",
    "FY2023": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/68647496be5f9b72fe43c3f9_mhi-consolidated-pillar-3-disclosure-2023-final.pdf",
    "FY2022": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686474abd90349ac917e208a_2022-mhi-consolidated-pillar-3-disclosure.pdf",
    "FY2021": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6864754eb71eb72dcfb8ec06_2021-mizuho-international-plc-pillar-3-disclosure.pdf",
    "FY2020": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686475629a3272fed34cef93_2020-pillar-3-disclosure.pdf",
    "FY2019": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686475789a3272fed34cf5a7_2019-pillar-3-disclosure.pdf",
    "FY2018": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6864758d6847432aa76ef044_2018-pillar-3-disclosure.pdf",
    "FY2017": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/6864759fa4cb331151bf5ee9_2017-pillar-3-disclosure.pdf",
    # FY2016/FY2015/FY2014 Pillar 3 disclosures were made at "Mizuho
    # Securities UK Holdings Ltd" (MSUKH) group level - MHI's immediate
    # parent and the entity these Pillar 3 documents describe as
    # consolidating MHI, its principal operating subsidiary - not at MHI
    # level directly; MHI-level figures only start appearing as the
    # disclosing entity from the FY2017 Pillar 3 document onward.
    "FY2016": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686475b6c99b915dfa9735fb_2016-pillar-3-disclosure.pdf",
    "FY2015": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686475c97ce484821ccefc82_2015-pillar-3-disclosure.pdf",
    "FY2014": "https://cdn.prod.website-files.com/67cb23eaf0c6c4d4080e059a/686475e150ef186144c44568_2014-pillar-3-disclosure.pdf",
}

ENTITY_NOTE = (
    "ENTITY NOTE: Mizuho International plc (company 01203696, FRN 119256; LEI "
    "213800HZ54TG54H2KV03) is the legal entity in Banks List 2608.xlsx. "
    "Companies House confirms the active UK public company. Figures are the "
    "consolidated Mizuho International plc Group basis used in the official reports, "
    "in £ millions. The company accounts use the FRS 102 exemption from preparing a "
    "separate company cash-flow statement (or, for FY2014-FY2018, the equivalent "
    "predecessor exemption; see the reporting-basis note below for those years)."
)

# HD-047 reporting-basis note: FY2019-FY2025 statements are all Consolidated
# Mizuho International plc Group basis (Group consolidation began with the
# FY2019 Annual Report). FY2015-FY2018 statements are Company-only (MHI did
# not yet prepare group accounts) under FRS 102, restated from UK GAAP as at
# 1 April 2015. FY2014 is Company-only, originally-filed UK GAAP (pre-FRS 102
# transition) sourced from the Companies House statutory filing, not
# restated - there is a real, disclosed ~£0.5m equity total break between the
# FY2014 closing position as originally filed and the FRS102-restated FY2015
# opening position shown in the FY2016 Annual Report (see the Statement of
# Changes in Equity's "FRS 102 transition adjustment" row). None of
# FY2014-FY2020 include a cash flow statement (FRS 1/FRS 102 exemption for a
# qualifying subsidiary whose ultimate parent publishes consolidated
# accounts, per each year's own Annual Report).
REPORTING_BASIS_NOTE = (
    "REPORTING BASIS: FY2019-FY2025 are Consolidated Mizuho International plc Group "
    "basis (Group consolidation began FY2019). FY2015-FY2018 are Company-only basis "
    "under FRS 102 (restated from UK GAAP as at 1 April 2015 transition date); the "
    "Company did not yet prepare group accounts. FY2010-FY2014 are Company-only, "
    "originally-filed UK GAAP (pre-FRS 102), sourced from the Companies House "
    "statutory filing rather than Mizuho's own site (see AR/P3/CH_STATUTORY source "
    "dict comments) - there is a real ~£0.5m equity break between FY2014 as "
    "originally filed and the FRS102-restated FY2015 opening position (see the "
    "Statement of Changes in Equity's transition row). FY2008-FY2009 are a mixed "
    "basis dictated by what each year's own filing actually presents: the Balance "
    "Sheet is Company-only (matching the FY2010-FY2014 convention) but the Profit "
    "and Loss Account is Consolidated (the Company did not present its own P&L "
    "those two years, relying on the Companies Act exemption for a subsidiary "
    "whose consolidated P&L is presented instead) - Total Equity is identical "
    "under either basis for FY2008/FY2009 (the Group/Company difference is "
    "confined to derivative and repo gross-up presentation on the asset/liability "
    "sides), so this mixed basis does not affect the equity reconciliation ladder. "
    "None of FY2008-FY2020 include a cash flow statement (FRS 1/FRS 102 exemption "
    "for a qualifying subsidiary whose ultimate parent publishes consolidated "
    "accounts, per each year's own Annual Report). FY2012's own filing discloses a "
    "voluntary accounting policy change made during FY2012, from trade-date to "
    "settlement-date accounting for regular-way trading securities transactions; "
    "applied retrospectively, it shrank the FY2011 comparative shown in FY2012's own "
    "report (Total Assets 29,781.5 -> 27,034.4, largely a reclassification out of "
    "'Other assets') versus FY2011's own originally-filed trade-date figures used "
    "for the FY2011 column here (per this project's own-year-filing sourcing rule) "
    "- a real, disclosed break between the FY2011 and FY2012 columns, not a "
    "transcription error."
)

# FY2026 added 2026-09-17 from the Annual Report 2026's Consolidated Statement
# of Cash Flows (p.84). That statement presents four lines the FY2021-FY2025
# statements do not: the sale and purchase of a subsidiary (investing), and the
# gross issuance/redemption of debt securities in place of the single net line
# used previously (financing). They are added as their own rows rather than
# netted into the existing ones, so each year keeps the presentation its own
# source used; every year's own components still sum to its own printed
# subtotal.
CF = {
    "Profit / (loss) before tax": {"FY2026": 20.5, "FY2025": 5.8, "FY2024": 15.0, "FY2023": -10.4, "FY2022": -37.6, "FY2021": 43.8},
    "Non-cash items included in profit / (loss) before tax": {"FY2026": -33.0, "FY2025": -30.0, "FY2024": -23.0, "FY2023": -6.3, "FY2022": 12.6, "FY2021": 23.3},
    "Provision for liabilities": {"FY2026": 7.5, "FY2025": 0.1, "FY2024": -0.9, "FY2023": 0.9, "FY2022": -0.2, "FY2021": -0.4},
    "Movement in Other Comprehensive Income": {"FY2026": -0.3, "FY2025": -0.5, "FY2024": -0.4, "FY2023": -0.1, "FY2022": -0.4, "FY2021": -0.5},
    "Change in operating assets": {"FY2026": -785.1, "FY2025": 846.1, "FY2024": 2479.7, "FY2023": -5424.2, "FY2022": -3613.0, "FY2021": 6374.7},
    "Change in operating liabilities": {"FY2026": 1171.5, "FY2025": -938.8, "FY2024": -2313.4, "FY2023": 5456.5, "FY2022": 4012.7, "FY2021": -6952.2},
    "Interest paid": {"FY2026": -67.5, "FY2025": -93.3, "FY2024": -92.7, "FY2023": -0.1, "FY2022": -0.2, "FY2021": -1.3},
    "Interest received": {"FY2026": 100.9, "FY2025": 124.2, "FY2024": 139.8, "FY2023": 11.0, "FY2022": 14.4, "FY2021": 16.4},
    "Tax (paid) / received": {"FY2026": 3.2, "FY2025": -6.1, "FY2024": 12.6, "FY2023": -2.0, "FY2022": -3.4, "FY2021": 10.5},
    "Net cash flows from operating activities": {"FY2026": 417.7, "FY2025": -92.5, "FY2024": 216.7, "FY2023": 25.3, "FY2022": 384.9, "FY2021": -485.7},
    "Net investment in shares in group undertakings": {"FY2026": -5.8, "FY2025": -1.4, "FY2024": -0.1, "FY2023": -0.5, "FY2022": -2.0, "FY2021": -0.1},
    "Dividends from investment in shares in group undertakings": {"FY2026": 0.5, "FY2025": 0.4, "FY2024": 0.2, "FY2023": 0.3, "FY2022": 0.7, "FY2021": 0.4},
    "Sale of subsidiary (net of cash disposed)": {"FY2026": 15.4},
    "Purchase of subsidiary (net of cash acquired)": {"FY2026": -38.7},
    "Purchase of intangible assets": {"FY2026": -51.4, "FY2025": -43.8, "FY2024": -27.2, "FY2023": -28.7, "FY2022": -25.3, "FY2021": -21.8},
    "Purchase of tangible assets": {"FY2026": -2.4, "FY2025": -5.2, "FY2024": -5.8, "FY2023": -2.7, "FY2022": -6.4, "FY2021": -3.6},
    "Net cash flows used in investing activities": {"FY2026": -82.4, "FY2025": -50.0, "FY2024": -32.9, "FY2023": -31.6, "FY2022": -33.0, "FY2021": -25.1},
    "Proceeds from issuance of debt securities": {"FY2026": 738.1},
    "Payment on redemption of debt securities in issue": {"FY2026": -1029.3},
    "Net repayment from debt securities in issue": {"FY2025": -101.5, "FY2024": -221.2, "FY2023": -139.6, "FY2022": -87.8, "FY2021": 75.6},
    "Net repayment of subordinated liabilities": {"FY2022": -45.0},
    "Proceeds from the issuance of equity": {"FY2026": 55.0, "FY2025": 45.0},
    "Net cash flows from / (used in) financing activities": {"FY2026": -236.2, "FY2025": -56.5, "FY2024": -221.2, "FY2023": -139.6, "FY2022": -132.8, "FY2021": 75.6},
    "Net (decrease) / increase in cash and cash equivalents": {"FY2026": 99.1, "FY2025": -199.0, "FY2024": -37.4, "FY2023": -145.9, "FY2022": 219.1, "FY2021": -435.2},
    "Effects of exchange rates on cash and cash equivalents": {"FY2026": 2.7, "FY2025": -0.9, "FY2024": -4.2, "FY2023": 4.3, "FY2022": 2.2, "FY2021": -6.6},
    "Cash and cash equivalents at beginning of the period": {"FY2026": 175.7, "FY2025": 375.6, "FY2024": 417.2, "FY2023": 558.8, "FY2022": 337.5, "FY2021": 779.3},
    "Cash and cash equivalents at the end of the period": {"FY2026": 277.5, "FY2025": 175.7, "FY2024": 375.6, "FY2023": 417.2, "FY2022": 558.8, "FY2021": 337.5},
}

# GA-006 (2026-09-18): FY2008-FY2020 held no cell on any row, so thirteen year
# columns were blank to a reader and to audit_gaps.py even though the reason is
# fully established and quoted in the sheet subtitle - a formal FRS 1/FRS 102
# exemption, confirmed by HD-075 as explicitly invoked in each FY2008-FY2013
# Companies House filing. The statement now appears IN those columns, one cell
# per year, the same fix applied to ICICI Bank UK and Morgan Stanley Bank
# International in this ticket. No column is suppressed (GA-001) - they are all
# still printed, they now say something.
NO_CF_YEARS = ["FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015",
               "FY2014", "FY2013", "FY2012", "FY2011", "FY2010", "FY2009", "FY2008"]
ROWS = [
    ("DATA", "No statement of cash flows prepared - FRS 1 / FRS 102 exemption (see note below)",
     {y: "Not published - no statement of cash flows prepared (FRS 1/FRS 102 exemption)" for y in NO_CF_YEARS}),
    ("SECTION", "Operating activities", {}),
]
for label in list(CF)[:10]:
    ROWS.append(("TOTAL" if label == "Net cash flows from operating activities" else "DATA", label, CF[label]))
ROWS.append(("SECTION", "Investing activities", {}))
for label in list(CF)[10:17]:
    ROWS.append(("TOTAL" if label == "Net cash flows used in investing activities" else "DATA", label, CF[label]))
ROWS.append(("SECTION", "Financing activities", {}))
for label in list(CF)[17:23]:
    ROWS.append(("TOTAL" if label == "Net cash flows from / (used in) financing activities" else "DATA", label, CF[label]))
for label in list(CF)[23:]:
    ROWS.append(("TOTAL" if "cash equivalents" in label else "DATA", label, CF[label]))

def sources():
    return ENTITY_NOTE + "\n\nOfficial sources — Mizuho International plc Annual Reports: " + "; ".join(f"{y}: {u}" for y, u in AR.items())

def p3_sources():
    return ENTITY_NOTE + "\n\nOfficial Mizuho International plc Pillar 3 disclosures: " + "; ".join(f"{y}: {u}" for y, u in P3.items())

STATEMENTS_SOURCES = (
    sources()
    + "\n\nOfficial Companies House statutory filing sources for the FY2008-FY2013 extension (HD-075): "
    + "; ".join(f"{y}: {u}" for y, u in CH_STATUTORY.items())
    + "\n\nBalance Sheet/P&L/Equity figures are the Consolidated Mizuho International plc Group basis "
      "for FY2019-FY2025 (distinct from the Company-only basis also shown in each Annual Report). "
      "FY2026: Annual Report 2026 (year ended 31 March 2026), Consolidated Statement of Comprehensive "
      "Income p.79, Consolidated Statement of Financial Position p.80, Consolidated Statement of "
      "Changes in Equity p.82, Consolidated Statement of Cash Flows p.84. "
      "FY2025/FY2024: Annual Report 2025, Consolidated Statement of Comprehensive Income and Consolidated "
      "Statement of Financial Position p.88-89, Consolidated Statement of Changes in Equity p.90-91. "
      "FY2023/FY2022: Annual Report 2024, same statements p.86-89. FY2021: Annual Report 2022, Consolidated "
      "Statement of Comprehensive Income p.84-85, Consolidated Statement of Financial Position and "
      "Consolidated Statement of Changes in Equity p.86, 88. FY2020: Annual Report 2020, Consolidated "
      "Statement of Comprehensive Income/Financial Position/Changes in Equity/Cash Flows p.34-39. FY2019: "
      "Annual Report 2019, same Consolidated statements p.22-27."
    + "\n\n" + REPORTING_BASIS_NOTE
    + "\n\nFY2015-FY2018 (Company-only basis): FY2018 Annual Report, Statement of Comprehensive Income "
      "p.22, Statement of Financial Position p.23, Statement of Changes in Equity p.24. FY2017 Annual "
      "Report, same statements p.15-17. FY2016 Annual Report, same statements p.14-16 (FY2016 report's "
      "own FY2015 comparative column is the source for FY2015, restated to FRS 102). FY2014 (originally-"
      "filed UK GAAP, Company-only): Companies House 'Full accounts made up to 31 March 2014' filing, "
      "Profit and Loss Account p.13, Balance Sheet p.14, Consolidated Statement of Total Recognised Gains "
      "and Losses p.15."
    + "\n\nHD-075 (FY2008-FY2013, all Companies House statutory filings, see CH_STATUTORY above): FY2013 "
      "'Full accounts made up to 31 March 2013' filing, Profit and Loss Account p.12, Balance Sheet p.13, "
      "Statement of Total Recognised Gains and Losses p.14, Equity note (note 26, also source for the "
      "FY2012 comparative column) p.45. FY2012 'Full accounts made up to 31 March 2012' filing, Profit "
      "and Loss Account p.14, Balance Sheet p.15, Statement of Total Recognised Gains and Losses p.16, "
      "Changes in accounting policy note (settlement-date vs trade-date accounting change disclosed "
      "against the FY2011 comparative) p.18. FY2011 'Full accounts made up to 31 March 2011' filing (own "
      "originally-filed trade-date basis, not FY2012's restated comparative), Profit and Loss Account "
      "p.13, Balance Sheet p.14, Statement of Total Recognised Gains and Losses p.15. FY2010 'Full "
      "accounts made up to 31 March 2010' filing, Profit and Loss Account p.13, Balance Sheet p.14, "
      "Statement of Total Recognised Gains and Losses p.16 (own FY2009 comparative column cross-checked "
      "against the FY2009 filing below). FY2009 'Group of companies' accounts made up to 31 March 2009' "
      "filing: Company Balance Sheet p.15 (Company-only basis used here, per REPORTING BASIS note above); "
      "Consolidated Profit and Loss Account p.12 and Statement of Total Recognised Gains and Losses p.14 "
      "(no separate Company P&L presented that year - Companies Act exemption); Equity note (note 28, "
      "also source for the FY2008 comparative column and dividend disclosure) p.52. FY2008 'Group of "
      "companies' accounts made up to 31 March 2008' filing: Balance Sheet (Company-only) p.16, "
      "Consolidated Profit and Loss Account p.13, Statement of Total Recognised Gains and Losses p.15, "
      "Called Up Share Capital note 27 p.51, Equity note 28 (share capital movements, dividends paid, "
      "actuarial loss, fair value reserve release, and the FY2007 opening position used as the equity "
      "ladder's starting row) p.52."
)

bw = BankWorkbook("Mizuho International plc", Y_CORE, year_label={y: y for y in YEARS}, header_color="7A3E9D")

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total Equity is the independent check value for the equity
# sheet below. All 5 years tie exactly.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2026": 217.0, "FY2025": 115.5, "FY2024": 328.5, "FY2023": 370.4, "FY2022": 481.0, "FY2021": 227.5, "FY2020": 601.0, "FY2019": 3.3, "FY2018": 230.2, "FY2017": 112.5, "FY2016": 27.3}),
    ("DATA", "Loans and advances to banks", {"FY2026": 60.5, "FY2025": 60.2, "FY2024": 47.1, "FY2023": 46.8, "FY2022": 77.8, "FY2021": 110.0, "FY2020": 178.3, "FY2019": 143.6, "FY2018": 126.2, "FY2017": 166.4, "FY2016": 106.9, "FY2015": 95.9, "FY2014": 96.1, "FY2013": 43.0, "FY2012": 112.4, "FY2011": 55.5, "FY2010": 186.8, "FY2009": 80.5, "FY2008": 38.2}),
    ("DATA", "Loans and advances to customers", {"FY2015": 3.2, "FY2014": 0.4, "FY2013": 0, "FY2012": 40.7, "FY2011": 65.1, "FY2010": 117.3, "FY2009": 55.1, "FY2008": 9.1}),
    ("DATA", "Reverse repurchase agreements with banks", {"FY2026": 2321.3, "FY2025": 4055.8, "FY2024": 5131.0, "FY2023": 5841.9, "FY2022": 3854.3, "FY2021": 2107.5, "FY2020": 963.0, "FY2019": 2052.7, "FY2018": 2756.6, "FY2017": 4091.3, "FY2016": 3268.7, "FY2015": 11535.2, "FY2014": 24398.2, "FY2013": 27598.4, "FY2012": 23596.2, "FY2011": 24795.3, "FY2010": 29267.2, "FY2009": 15811.8, "FY2008": 19168.6},
     ),
    ("DATA", "Reverse repurchase agreements with customers", {"FY2026": 5981.7, "FY2025": 4587.1, "FY2024": 3059.6, "FY2023": 2303.5, "FY2022": 5417.0, "FY2021": 4288.6, "FY2020": 5895.2, "FY2019": 7204.8, "FY2018": 4636.4, "FY2017": 5106.9, "FY2016": 3176.7, "FY2015": 5083.7}),
    ("DATA", "Debt and other fixed income securities", {"FY2026": 5327.2, "FY2025": 5644.9, "FY2024": 5463.7, "FY2023": 5087.2, "FY2022": 4772.0, "FY2021": 4261.9, "FY2020": 4998.0, "FY2019": 5087.0, "FY2018": 5248.4, "FY2017": 4054.6, "FY2016": 5268.4, "FY2015": 4191.1, "FY2014": 3907.2, "FY2013": 2857.7, "FY2012": 1421.0, "FY2011": 1440.4, "FY2010": 926.1, "FY2009": 1421.5, "FY2008": 2361.2}),
    ("DATA", "Equity shares", {"FY2026": 1.0, "FY2025": 2.6, "FY2024": 4.3, "FY2023": 6.1, "FY2022": 3.5, "FY2021": 1.8, "FY2020": 1.6, "FY2019": 1.2, "FY2018": 1.3, "FY2017": 1.5, "FY2016": 1.0, "FY2015": 6.3, "FY2013": 59.4, "FY2012": 53.2, "FY2011": 86.7, "FY2010": 82.7, "FY2009": 73.2, "FY2008": 78.1}),
    ("DATA", "Derivative assets", {"FY2026": 9910.3, "FY2025": 8520.1, "FY2024": 9707.7, "FY2023": 13072.6, "FY2022": 6443.1, "FY2021": 6513.8, "FY2020": 11566.9, "FY2019": 4451.4, "FY2018": 2136.2, "FY2017": 1498.4, "FY2016": 424.0, "FY2015": 301.9, "FY2014": 204.7, "FY2013": 281.3, "FY2012": 382.7, "FY2011": 480.5, "FY2010": 828.6, "FY2009": 1925.9, "FY2008": 1468.7}),
    ("DATA", "Shares in group undertakings", {"FY2026": 29.8, "FY2025": 17.6, "FY2024": 13.2, "FY2023": 9.9, "FY2022": 8.1, "FY2021": 6.8, "FY2020": 7.0, "FY2019": 8.6, "FY2018": 6.0, "FY2017": 5.8, "FY2016": 3.8, "FY2015": 3.6}),
    ("DATA", "Intangible assets", {"FY2026": 160.4, "FY2025": 96.3, "FY2024": 76.7, "FY2023": 73.7, "FY2022": 66.2, "FY2021": 63.2, "FY2020": 67.8, "FY2019": 73.2, "FY2018": 66.0, "FY2017": 71.5, "FY2016": 61.6, "FY2015": 47.6}),
    ("DATA", "Tangible fixed assets", {"FY2026": 21.6, "FY2025": 25.1, "FY2024": 27.1, "FY2023": 27.3, "FY2022": 29.0, "FY2021": 27.0, "FY2020": 27.9, "FY2019": 31.2, "FY2018": 31.1, "FY2017": 33.2, "FY2016": 28.4, "FY2015": 10.3, "FY2014": 12.7, "FY2013": 9.0, "FY2012": 11.3, "FY2011": 10.1, "FY2010": 8.5, "FY2009": 13.1, "FY2008": 18.2}),
    ("DATA", "Other assets", {"FY2026": 590.4, "FY2025": 559.8, "FY2024": 897.9, "FY2023": 449.5, "FY2022": 832.2, "FY2021": 517.6, "FY2020": 659.1, "FY2019": 236.4, "FY2018": 210.9, "FY2017": 193.0, "FY2016": 752.2, "FY2015": 159.0, "FY2014": 217.7, "FY2013": 159.0, "FY2012": 201.1, "FY2011": 2786.9, "FY2010": 1983.5, "FY2009": 2360.3, "FY2008": 1534.4}),
    ("DATA", "Prepayments and accrued income", {"FY2026": 220.3, "FY2025": 229.9, "FY2024": 177.1, "FY2023": 90.0, "FY2022": 74.7, "FY2021": 82.7, "FY2020": 79.3, "FY2019": 90.7, "FY2018": 68.0, "FY2017": 60.1, "FY2016": 73.8, "FY2015": 49.7, "FY2014": 46.2, "FY2013": 52.0, "FY2012": 54.5, "FY2011": 61.0, "FY2010": 35.1, "FY2009": 73.8, "FY2008": 84.6}),
    ("TOTAL", "Total Assets", {"FY2026": 24841.5, "FY2025": 23914.9, "FY2024": 24933.9, "FY2023": 27378.9, "FY2022": 22058.9, "FY2021": 18208.4, "FY2020": 25045.1, "FY2019": 19384.1, "FY2018": 15517.3, "FY2017": 15395.2, "FY2016": 13192.8, "FY2015": 21487.5, "FY2014": 28883.2, "FY2013": 31059.8, "FY2012": 25873.1, "FY2011": 29781.5, "FY2010": 33435.8, "FY2009": 21815.2, "FY2008": 24761.1}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2026": 625.3, "FY2025": 678.7, "FY2024": 519.1, "FY2023": 292.1, "FY2022": 1153.3, "FY2021": 285.5, "FY2020": 471.6, "FY2019": 196.2, "FY2018": 398.0, "FY2017": 318.9, "FY2016": 613.1, "FY2015": 655.7, "FY2014": 744.1, "FY2013": 724.2, "FY2012": 841.4, "FY2011": 863.4, "FY2010": 727.3, "FY2009": 832.3, "FY2008": 741.2}),
    ("DATA", "Customer accounts", {"FY2026": 553.8, "FY2025": 473.5, "FY2024": 707.5, "FY2023": 897.9, "FY2022": 295.7, "FY2021": 228.6, "FY2020": 909.7, "FY2019": 610.0, "FY2018": 337.8, "FY2017": 432.0, "FY2016": 310.2, "FY2015": 273.2, "FY2014": 294.0, "FY2013": 311.4, "FY2012": 124.5, "FY2011": 137.4, "FY2010": 241.9, "FY2009": 29.4, "FY2008": 4.8}),
    ("DATA", "Repurchase agreements with banks", {"FY2026": 6118.5, "FY2025": 4580.9, "FY2024": 3769.7, "FY2023": 1675.3, "FY2022": 1775.5, "FY2021": 1984.1, "FY2020": 1614.4, "FY2019": 1734.2, "FY2018": 1861.6, "FY2017": 2448.5, "FY2016": 2462.1, "FY2015": 3515.8, "FY2014": 23465.2, "FY2013": 27233.0, "FY2012": 21279.6, "FY2011": 22658.3, "FY2010": 27548.1, "FY2009": 14302.6, "FY2008": 18464.7}),
    ("DATA", "Repurchase agreements with customers", {"FY2026": 2872.6, "FY2025": 4078.0, "FY2024": 3425.7, "FY2023": 5231.3, "FY2022": 5799.8, "FY2021": 3133.7, "FY2020": 3638.8, "FY2019": 4572.0, "FY2018": 3301.7, "FY2017": 3779.3, "FY2016": 2992.4, "FY2015": 11966.0}),
    ("DATA", "Debt securities in issue", {"FY2026": 994.4, "FY2025": 1292.3, "FY2024": 1395.0, "FY2023": 1616.5, "FY2022": 1760.1, "FY2021": 1851.6, "FY2020": 1776.6, "FY2019": 1453.2, "FY2018": 1773.3, "FY2017": 1387.9, "FY2016": 879.3, "FY2015": 1142.7, "FY2014": 976.6, "FY2013": 866.8, "FY2012": 1189.7, "FY2011": 1350.3, "FY2010": 1468.3, "FY2009": 2051.2, "FY2008": 1514.5}),
    ("DATA", "Short trading positions", {"FY2026": 2145.3, "FY2025": 2889.1, "FY2024": 3925.7, "FY2023": 3418.7, "FY2022": 3560.9, "FY2021": 3072.9, "FY2020": 3728.3, "FY2019": 5208.7, "FY2018": 4561.1, "FY2017": 4297.7, "FY2016": 4570.4, "FY2015": 2892.2, "FY2014": 2600.9, "FY2013": 1061.9, "FY2012": 1439.6, "FY2011": 1317.2, "FY2010": 178.0, "FY2009": 148.3, "FY2008": 706.3}),
    ("DATA", "Derivative liabilities", {"FY2026": 9801.3, "FY2025": 8548.4, "FY2024": 9603.3, "FY2023": 12833.5, "FY2022": 6422.7, "FY2021": 6481.2, "FY2020": 11514.0, "FY2019": 4285.1, "FY2018": 2030.6, "FY2017": 1433.1, "FY2016": 421.4, "FY2015": 250.9, "FY2014": 181.6, "FY2013": 283.6, "FY2012": 391.3, "FY2011": 513.3, "FY2010": 920.8, "FY2009": 2563.0, "FY2008": 2021.0}),
    ("DATA", "Other liabilities", {"FY2026": 603.3, "FY2025": 365.8, "FY2024": 651.2, "FY2023": 581.4, "FY2022": 452.1, "FY2021": 225.3, "FY2020": 504.3, "FY2019": 380.7, "FY2018": 296.2, "FY2017": 357.3, "FY2016": 307.3, "FY2015": 257.2, "FY2014": 95.3, "FY2013": 83.9, "FY2012": 116.2, "FY2011": 2594.5, "FY2010": 1836.7, "FY2009": 1447.4, "FY2008": 602.4}),
    ("DATA", "Accruals and deferred income", {"FY2026": 274.0, "FY2025": 234.5, "FY2024": 212.9, "FY2023": 120.5, "FY2022": 123.3, "FY2021": 155.4, "FY2020": 139.0, "FY2019": 153.6, "FY2018": 137.8, "FY2017": 141.7, "FY2016": 116.2, "FY2015": 79.4, "FY2014": 69.6, "FY2013": 52.7, "FY2012": 67.6, "FY2011": 74.6, "FY2010": 89.5, "FY2009": 82.5, "FY2008": 162.1}),
    ("DATA", "Provisions for liabilities", {"FY2026": 7.7, "FY2025": 0.2, "FY2024": 3.1, "FY2023": 4.0, "FY2022": 3.1, "FY2021": 3.3, "FY2020": 3.9, "FY2019": 4.9, "FY2018": 12.4, "FY2017": 17.2, "FY2016": 14.4, "FY2015": 12.8, "FY2014": 16.3, "FY2013": 17.2, "FY2012": 75.6, "FY2011": 3.0, "FY2010": 3.4, "FY2009": 4.4, "FY2008": 13.0}),
    ("DATA", "Subordinated liabilities", {"FY2021": 45.2, "FY2020": 45.3, "FY2019": 45.3, "FY2018": 45.2, "FY2017": 45.2, "FY2016": 45.2, "FY2008": 18.6}),
    ("DATA", "Pension liabilities", {"FY2026": 0.1}),
    ("TOTAL", "Total Liabilities", {"FY2026": 23996.3, "FY2025": 23141.4, "FY2024": 24213.2, "FY2023": 26671.2, "FY2022": 21346.5, "FY2021": 17466.8, "FY2020": 24345.9, "FY2019": 18643.9, "FY2018": 14755.7, "FY2017": 14658.8, "FY2016": 12732.0, "FY2015": 21045.9, "FY2014": 28443.6, "FY2013": 30634.7, "FY2012": 25525.5, "FY2011": 29512.0, "FY2010": 33014.0, "FY2009": 21461.1, "FY2008": 24248.6}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2026": 809.9, "FY2025": 754.9, "FY2024": 709.9, "FY2023": 709.9, "FY2022": 709.9, "FY2021": 709.9, "FY2020": 709.9, "FY2019": 709.9, "FY2018": 709.9, "FY2017": 709.9, "FY2016": 2875.3, "FY2015": 2840.3, "FY2014": 2840.3, "FY2013": 2795.3, "FY2012": 2712.3, "FY2011": 2462.3, "FY2010": 2462.3, "FY2009": 2426.4, "FY2008": 2314.6}),
    ("DATA", "Share premium account", {"FY2026": 15.6, "FY2025": 15.6, "FY2024": 15.6, "FY2023": 15.6, "FY2022": 15.6, "FY2021": 15.6, "FY2020": 15.6, "FY2019": 15.6, "FY2018": 15.6, "FY2017": 15.6, "FY2016": 15.6, "FY2015": 15.6, "FY2014": 15.6, "FY2013": 15.6, "FY2012": 15.6, "FY2011": 15.6, "FY2010": 15.6, "FY2009": 15.6, "FY2008": 15.6}),
    ("DATA", "Pension reserve", {"FY2026": -7.4, "FY2025": -7.1, "FY2024": -6.8, "FY2023": -6.5, "FY2022": -6.2, "FY2021": -5.9, "FY2020": -5.9, "FY2019": -5.6, "FY2018": -3.7, "FY2017": -1.3, "FY2016": -16.8, "FY2015": -16.4}),
    ("DATA", "Other reserves", {"FY2026": 0, "FY2025": -0.8, "FY2024": -0.6, "FY2023": -0.4, "FY2022": -0.5, "FY2021": -0.4}),
    ("DATA", "Profit and loss account", {"FY2026": 27.1, "FY2025": 10.9, "FY2024": 2.6, "FY2023": -10.9, "FY2022": -6.4, "FY2021": 22.4, "FY2020": -20.4, "FY2019": 20.3, "FY2018": 39.8, "FY2017": 12.2, "FY2016": -2413.3, "FY2015": -2397.9, "FY2014": -2416.3, "FY2013": -2385.8, "FY2012": -2380.3, "FY2011": -2208.4, "FY2010": -2056.1, "FY2009": -2087.9, "FY2008": -1817.7}),
    ("TOTAL", "Total Equity", {"FY2026": 845.2, "FY2025": 773.5, "FY2024": 720.7, "FY2023": 707.7, "FY2022": 712.4, "FY2021": 741.6, "FY2020": 699.2, "FY2019": 740.2, "FY2018": 761.6, "FY2017": 736.4, "FY2016": 460.8, "FY2015": 441.6, "FY2014": 439.6, "FY2013": 425.1, "FY2012": 347.6, "FY2011": 269.5, "FY2010": 421.8, "FY2009": 354.1, "FY2008": 512.5}),
    ("TOTAL", "Total Liabilities and Equity", {"FY2026": 24841.5, "FY2025": 23914.9, "FY2024": 24933.9, "FY2023": 27378.9, "FY2022": 22058.9, "FY2021": 18208.4, "FY2020": 25045.1, "FY2019": 19384.1, "FY2018": 15517.3, "FY2017": 15395.2, "FY2016": 13192.8, "FY2015": 21487.5, "FY2014": 28883.2, "FY2013": 31059.8, "FY2012": 25873.1, "FY2011": 29781.5, "FY2010": 33435.8, "FY2009": 21815.2, "FY2008": 24761.1}),
]
bw.add_balance_sheet_sheet(
    title="Mizuho International plc — Balance Sheet",
    subtitle="Consolidated Group basis for FY2019-FY2025; Company-only basis for FY2014-FY2018 (see the "
              "'REPORTING BASIS' source note). FY2021 shows a genuine structural difference from FY2022 onward: "
              "the standalone 'Subordinated liabilities' line was fully repaid during FY2022 (see the Cash Flow "
              "Statement's 'Net repayment of subordinated liabilities' row) and is absent from FY2022 onward; it "
              "was first issued in FY2016 and continued unbroken FY2016-FY2021. FY2014 (originally-filed UK GAAP, "
              "pre-FRS 102) combines several lines that later years disclose separately: 'Reverse repurchase "
              "agreements with banks' and 'Repurchase agreements with banks' each carry the FY2014 source's single "
              "undifferentiated repo total (not split by bank/customer counterparty - the 'with customers' rows "
              "are blank for FY2014 only); 'Derivative assets'/'Derivative liabilities' sum the FY2014 source's "
              "separate trading and risk-management derivative lines; 'Debt and other fixed income securities' "
              "carries the FY2014 source's combined 'Trading financial assets' line (equity shares not split out); "
              "'Short trading positions' carries the FY2014 source's 'Trading financial liabilities' line; 'Other "
              "liabilities' includes the FY2014 source's separately-disclosed £2.3m defined benefit pension "
              "liability. FY2014 has no separate Cash/Shares in group undertakings/Intangible assets/Pension "
              "reserve lines (nil or not yet recognised as separate categories pre-FRS 102) - shown blank, not "
              "zero. HD-075: FY2008-FY2013 follow the same FY2014-style combined presentation (single 'Reverse "
              "repurchase agreements with banks'/'Repurchase agreements with banks' lines, combined 'Derivative "
              "assets'/'Derivative liabilities', 'Debt and other fixed income securities' carrying that year's "
              "combined trading financial assets total) since each year's own primary Balance Sheet presents "
              "them the same undifferentiated way; 'Equity shares' for FY2008-FY2013 carries that year's "
              "separately-disclosed 'Financial investments' note (unlisted equity securities designated at fair "
              "value) rather than a trading-book equity split, which those years don't disclose. 'Other "
              "liabilities' folds in each year's own separately-disclosed defined benefit pension liability where "
              "one exists (FY2010: £3.8m; FY2011: £0.9m; FY2008: £0.4m; nil FY2009/FY2012/FY2013). 'Subordinated "
              "liabilities' (£18.6m) appears only in FY2008 - fully repaid before FY2009's balance sheet date, "
              "not disclosed again until FY2016. FY2008/FY2009 Balance Sheet figures are Company-only (this "
              "Company did not present a separate Company P&L those two years - see the REPORTING BASIS note). "
              "FY2011's own originally-filed balance sheet (not FY2012's later restated comparative) is used, "
              "following a disclosed voluntary change from trade-date to settlement-date accounting made during "
              "FY2012 - see the REPORTING BASIS note for the resulting break in 'Other assets'/'Debt and other "
              "fixed income securities' between FY2011 and FY2012. £m.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=72,
    source_height=260,
    unit_suffix=" (£m)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2026": 22.4, "FY2025": 28.4, "FY2024": 33.3, "FY2023": 18.2, "FY2022": 7.5, "FY2021": 4.0, "FY2020": 3.1, "FY2019": 2.4, "FY2018": 1.4, "FY2017": 1.1, "FY2016": 0.6, "FY2015": 0.2, "FY2014": 0.5, "FY2013": 0.4, "FY2012": 0.4, "FY2011": 3.0, "FY2010": 5.7, "FY2009": 18.9, "FY2008": 31.6}),
    ("DATA", "Interest payable", {"FY2026": -79.2, "FY2025": -105.7, "FY2024": -103.3, "FY2023": -38.7, "FY2022": -4.0, "FY2021": -5.4, "FY2020": -24.9, "FY2019": -19.7, "FY2018": -11.5, "FY2017": -11.9, "FY2016": -15.8, "FY2015": -21.8, "FY2014": -9.3, "FY2013": -9.9, "FY2012": -12.8, "FY2010": 0, "FY2009": -0.3, "FY2008": -2.9}),
    ("TOTAL", "Net interest income/(expense)", {"FY2026": -56.8, "FY2025": -77.3, "FY2024": -70.0, "FY2023": -20.5, "FY2022": 3.5, "FY2021": -1.4, "FY2020": -21.8, "FY2019": -17.3, "FY2018": -10.1, "FY2017": -10.8, "FY2016": -15.2, "FY2015": -21.6, "FY2014": -8.8, "FY2013": -9.5, "FY2012": -12.4, "FY2011": 3.0, "FY2010": 5.7, "FY2009": 18.6, "FY2008": 28.7}),
    ("DATA", "Fees and commissions receivable", {"FY2026": 234.4, "FY2025": 198.7, "FY2024": 178.8, "FY2023": 132.1, "FY2022": 175.6, "FY2021": 182.4, "FY2020": 128.2, "FY2019": 153.1, "FY2018": 148.9, "FY2017": 140.0, "FY2016": 133.8, "FY2015": 91.8, "FY2014": 71.3, "FY2013": 42.1, "FY2012": 67.9, "FY2011": 69.8, "FY2010": 69.8, "FY2009": 32.9, "FY2008": 32.7}),
    ("DATA", "Fees and commissions payable", {"FY2026": -112.9, "FY2025": -76.0, "FY2024": -71.9, "FY2023": -53.4, "FY2022": -91.3, "FY2021": -99.5, "FY2020": -56.6, "FY2019": -73.9, "FY2018": -65.2, "FY2017": -58.1, "FY2016": -82.1, "FY2015": -43.5, "FY2014": -28.5, "FY2013": -28.8, "FY2012": -36.6, "FY2011": -49.2, "FY2010": -56.3, "FY2009": -33.8, "FY2008": -53.4}),
    ("TOTAL", "Net fees and commissions", {"FY2026": 121.5, "FY2025": 122.7, "FY2024": 106.9, "FY2023": 78.7, "FY2022": 84.3, "FY2021": 82.9, "FY2020": 71.6, "FY2019": 79.2, "FY2018": 83.7, "FY2017": 81.9, "FY2016": 51.7, "FY2015": 48.3, "FY2014": 42.8, "FY2013": 13.3, "FY2012": 31.3, "FY2011": 20.6, "FY2010": 13.5, "FY2009": -0.9, "FY2008": -20.7}),
    ("DATA", "Dealing profit", {"FY2026": 161.1, "FY2025": 175.1, "FY2024": 204.9, "FY2023": 130.7, "FY2022": 77.1, "FY2021": 183.1, "FY2020": 107.4, "FY2019": 112.3, "FY2018": 161.3, "FY2017": 144.5, "FY2016": 101.6, "FY2015": 97.5, "FY2014": 53.5, "FY2013": 90.0, "FY2012": -11.0, "FY2011": -41.0, "FY2010": 140.6, "FY2009": -149.3, "FY2008": -1850.4}),
    ("DATA", "Other operating income", {"FY2026": 170.9, "FY2025": 152.9, "FY2024": 2.3, "FY2023": 5.5, "FY2022": 1.4, "FY2021": 0.5, "FY2020": 0.3, "FY2019": 0.4, "FY2018": 0.1, "FY2017": 4.7, "FY2016": 7.5, "FY2015": 7.6, "FY2014": 0.1, "FY2013": 0.1, "FY2012": 0.1, "FY2011": 0.1, "FY2010": 0, "FY2009": 0.4, "FY2008": 2.0}),
    ("TOTAL", "Net income from operations", {"FY2026": 396.7, "FY2025": 373.4, "FY2024": 244.1, "FY2023": 194.4, "FY2022": 166.3, "FY2021": 265.1, "FY2020": 157.5, "FY2019": 174.6, "FY2018": 235.0, "FY2017": 220.3, "FY2016": 145.6, "FY2015": 131.8, "FY2014": 87.6, "FY2013": 93.9, "FY2012": 8.0, "FY2011": -17.3, "FY2010": 159.8, "FY2009": -131.2, "FY2008": -1840.4}),
    ("DATA", "Administrative expenses", {"FY2026": -334.6, "FY2025": -338.6, "FY2024": -200.7, "FY2023": -178.3, "FY2022": -178.5, "FY2021": -192.0, "FY2020": -176.6, "FY2019": -177.4, "FY2018": -178.4, "FY2017": -174.8, "FY2016": -146.4, "FY2015": -124.0, "FY2014": -111.8, "FY2013": -104.7, "FY2012": -105.5, "FY2011": -134.6, "FY2010": -120.9, "FY2009": -128.5, "FY2008": -183.8}),
    ("DATA", "Depreciation and amortisation", {"FY2026": -34.1, "FY2025": -28.9, "FY2024": -29.3, "FY2023": -25.6, "FY2022": -25.4, "FY2021": -29.5, "FY2020": -31.6, "FY2019": -28.8, "FY2018": -26.6, "FY2017": -20.8, "FY2016": -12.8, "FY2015": -6.2, "FY2014": -4.4, "FY2013": -4.2, "FY2012": -4.4, "FY2011": -3.9, "FY2010": -5.1, "FY2009": -6.2, "FY2008": -6.6}),
    ("DATA", "Provisions for liabilities", {"FY2026": -7.5, "FY2025": -0.1, "FY2024": 0.9, "FY2023": -0.9, "FY2021": 0.2, "FY2020": 0.6, "FY2019": 2.3, "FY2018": -0.2, "FY2017": -12.5, "FY2016": -1.8, "FY2015": 3.3, "FY2014": 0.6, "FY2013": -16.2, "FY2012": -68.8, "FY2010": 0, "FY2009": -1.4, "FY2008": -8.7}),
    ("TOTAL", "Operating expenses", {"FY2026": -376.2, "FY2025": -367.6, "FY2024": -229.1, "FY2023": -204.8, "FY2022": -203.9, "FY2021": -221.3, "FY2020": -207.6, "FY2019": -203.9, "FY2018": -205.2, "FY2017": -208.1, "FY2016": -161.0, "FY2015": -126.9, "FY2014": -115.6, "FY2013": -125.1, "FY2012": -178.7, "FY2011": -138.5, "FY2010": -126.0, "FY2009": -136.1, "FY2008": -199.1}),
    ("DATA", "Disposal of Custody business", {"FY2013": 28.2}),
    ("TOTAL", "Profit/(loss) on ordinary activities before taxation", {"FY2026": 20.5, "FY2025": 5.8, "FY2024": 15.0, "FY2023": -10.4, "FY2022": -37.6, "FY2021": 43.8, "FY2020": -50.1, "FY2019": -29.3, "FY2018": 29.8, "FY2017": 12.2, "FY2016": -15.4, "FY2015": 4.9, "FY2014": -28.0, "FY2013": -3.0, "FY2012": -170.7, "FY2011": -155.8, "FY2010": 33.8, "FY2009": -267.3, "FY2008": -2039.5}),
    ("DATA", "Tax credit/(charge) on profit/(loss) on ordinary activities", {"FY2026": -3.5, "FY2025": 1.4, "FY2024": -1.5, "FY2023": 5.9, "FY2022": 8.8, "FY2021": -1.0, "FY2020": 9.4, "FY2019": 9.8, "FY2018": -2.2, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0, "FY2013": 0, "FY2012": 0.4, "FY2011": 3.0, "FY2010": 1.4, "FY2009": -0.2, "FY2008": -1.2}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2026": 17.0, "FY2025": 7.2, "FY2024": 13.5, "FY2023": -4.5, "FY2022": -28.8, "FY2021": 42.8, "FY2020": -40.7, "FY2019": -19.5, "FY2018": 27.6, "FY2017": 12.2, "FY2016": -15.4, "FY2015": 4.9, "FY2014": -28.0, "FY2013": -3.0, "FY2012": -170.3, "FY2011": -152.8, "FY2010": 35.2, "FY2009": -267.5, "FY2008": -2040.7}),
    ("SECTION", "Other comprehensive income/(loss)", {}),
    ("DATA", "Re-measurement losses from defined benefit scheme", {"FY2026": -0.3, "FY2025": -0.3, "FY2024": -0.3, "FY2023": -0.3, "FY2022": -0.3, "FY2020": -0.3, "FY2019": -1.9, "FY2018": -2.4, "FY2017": -4.5, "FY2016": -0.4, "FY2015": -2.4, "FY2014": -2.5, "FY2013": -2.5, "FY2012": -1.6, "FY2011": 0.5, "FY2010": -3.4, "FY2009": -2.7, "FY2008": -0.6}),
    ("DATA", "FX translation gain/(loss) relating to net investment in subsidiary", {"FY2026": 0, "FY2025": -0.2, "FY2024": -0.2, "FY2023": 0.1, "FY2022": -0.1, "FY2021": -0.4}),
    ("DATA", "Valuation adjustments on available-for-sale financial investments released from equity", {"FY2008": 0.2}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2026": 16.7, "FY2025": 6.7, "FY2024": 13.0, "FY2023": -4.7, "FY2022": -29.2, "FY2021": 42.4, "FY2020": -41.0, "FY2019": -21.4, "FY2018": 25.2, "FY2017": 7.7, "FY2016": -15.8, "FY2015": 2.5, "FY2014": -30.5, "FY2013": -5.5, "FY2012": -171.9, "FY2011": -152.3, "FY2010": 31.8, "FY2009": -270.2, "FY2008": -2041.1}),
]
bw.add_income_statement_sheet(
    title="Mizuho International plc — Profit & Loss",
    subtitle="Consolidated Group basis for FY2019-FY2025; Company-only basis for FY2014-FY2018 (see the "
              "'REPORTING BASIS' source note). Re-measurement losses from defined benefit scheme were nil (not "
              "disclosed as a line) in FY2021; Provisions for liabilities was nil in FY2021 Company statement "
              "terms and is shown blank for FY2021 Consolidated as the report discloses no separate figure. "
              "FY2014-FY2020 did not disclose a separate FX translation line (shown blank, not zero). FY2014-"
              "FY2017 each disclosed a £nil tax charge/credit (shown here as 0, per each year's own source). "
              "HD-075: FY2008/FY2009 figures are Consolidated (the Company did not present its own P&L those two "
              "years - a Companies Act exemption for a subsidiary whose consolidated P&L is presented instead; "
              "see the REPORTING BASIS note); FY2010-FY2013 are Company-only. FY2011's original statement did "
              "not disclose a separate 'Interest payable' line at all (folded into 'Dealing profit' - shown "
              "blank here, not zero; FY2012's report separated it out for FY2011's restated comparative, but "
              "this project sources FY2011 from FY2011's own filing - see the REPORTING BASIS note). FY2010 "
              "disclosed £nil for Interest payable, Other operating income and Provisions for liabilities (shown "
              "as 0, not blank). 'Disposal of Custody business' (£28.2m, FY2013 only) reflects the sale of the "
              "Company's Custody business to Mizuho Trust & Banking (Luxembourg) S.A., disclosed as a separate "
              "line between operating expenses and profit before tax in the FY2013 source. 'Valuation "
              "adjustments on available-for-sale financial investments released from equity' (£0.2m, FY2008 "
              "only) is a one-off item disclosed in the FY2008 Statement of Total Recognised Gains and Losses.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=240,
    unit_suffix=" (£m)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder confirmed:
# every year's own closing balance ties exactly to both the next year's own
# opening balance and that year's own Balance Sheet Total Equity. Zero plug
# rows needed anywhere across all 5 years. Ladder's mandated scan of each
# year's equity note caught the FY2025 capital injection, equity
# contribution, and transfer-to-P&L rows arising from the sub-lease
# termination described in the source's own explanatory note.
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Share premium account", "Pension reserve", "Other reserves",
                   "Profit and loss account", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 April 2007 (FY2008 opening)", (257.6, 15.6, None, -0.2, 243.6, 516.6)),
    ("DATA", "Increase in paid up share capital", (2057.0, None, None, None, None, 2057.0)),
    ("DATA", "Loss for the year", (None, None, None, None, -2040.7, -2040.7)),
    ("DATA", "Dividends paid", (None, None, None, None, -20.0, -20.0)),
    ("DATA", "Actuarial loss on defined benefit scheme and related deferred tax", (None, None, None, None, -0.6, -0.6)),
    ("DATA", "Fair value reserve released", (None, None, None, 0.2, None, 0.2)),
    ("TOTAL", "At 31 March 2008 (FY2008 closing)", (2314.6, 15.6, None, 0, -1817.7, 512.5)),
    ("DATA", "Increase in paid up share capital", (111.8, None, None, None, None, 111.8)),
    ("DATA", "Loss for the year", (None, None, None, None, -267.5, -267.5)),
    ("DATA", "Actuarial loss on defined benefit scheme", (None, None, None, None, -2.7, -2.7)),
    ("TOTAL", "At 31 March 2009 (FY2009 closing)", (2426.4, 15.6, None, 0, -2087.9, 354.1)),
    ("DATA", "Increase in paid up share capital", (35.9, None, None, None, None, 35.9)),
    ("DATA", "Profit for the year", (None, None, None, None, 35.2, 35.2)),
    ("DATA", "Actuarial loss on defined benefit scheme", (None, None, None, None, -3.4, -3.4)),
    ("TOTAL", "At 31 March 2010 (FY2010 closing)", (2462.3, 15.6, None, 0, -2056.1, 421.8)),
    ("DATA", "Loss for the year", (None, None, None, None, -152.8, -152.8)),
    ("DATA", "Actuarial gain on defined benefit scheme", (None, None, None, None, 0.5, 0.5)),
    ("TOTAL", "At 31 March 2011 (FY2011 closing, originally-filed trade-date basis)", (2462.3, 15.6, None, 0, -2208.4, 269.5)),
    ("DATA", "Increase in paid up share capital", (250.0, None, None, None, None, 250.0)),
    ("DATA", "Loss for the year", (None, None, None, None, -170.3, -170.3)),
    ("DATA", "Actuarial loss on defined benefit scheme", (None, None, None, None, -1.6, -1.6)),
    ("TOTAL", "At 31 March 2012 (FY2012 closing)", (2712.3, 15.6, None, 0, -2380.3, 347.6)),
    ("DATA", "Increase in paid up share capital", (83.0, None, None, None, None, 83.0)),
    ("DATA", "Loss for the year", (None, None, None, None, -3.0, -3.0)),
    ("DATA", "Actuarial loss on defined benefit scheme", (None, None, None, None, -2.5, -2.5)),
    ("TOTAL", "At 1 April 2013 (FY2014 opening, originally-filed UK GAAP)", (2795.3, 15.6, None, None, -2385.8, 425.1)),
    ("DATA", "Increase in paid up share capital", (45.0, None, None, None, None, 45.0)),
    ("DATA", "Loss for the year", (None, None, None, None, -28.0, -28.0)),
    ("DATA", "Actuarial loss on defined benefit scheme", (None, None, None, None, -2.5, -2.5)),
    ("TOTAL", "At 31 March 2014 (FY2014 closing, originally-filed UK GAAP)", (2840.3, 15.6, None, None, -2416.3, 439.6)),
    ("DATA", "FRS 102 transition adjustment (1 April 2014) - reclassifies a pension "
             "reserve out of the profit and loss account plus a further ~£0.5m net restatement", (None, None, -14.0, None, 13.5, -0.5)),
    ("TOTAL", "At 1 April 2014 (FY2015 opening, FRS 102-restated)", (2840.3, 15.6, -14.0, 0, -2402.8, 439.1)),
    ("DATA", "Profit for the year", (None, None, None, None, 4.9, 4.9)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -2.4, None, None, -2.4)),
    ("TOTAL", "At 31 March 2015 (FY2015 closing)", (2840.3, 15.6, -16.4, 0, -2397.9, 441.6)),
    ("DATA", "Increase in paid up share capital", (35.0, None, None, None, None, 35.0)),
    ("DATA", "Loss for the year", (None, None, None, None, -15.4, -15.4)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -0.4, None, None, -0.4)),
    ("TOTAL", "At 31 March 2016 (FY2016 closing)", (2875.3, 15.6, -16.8, 0, -2413.3, 460.8)),
    ("DATA", "Increase in paid up share capital", (267.9, None, None, None, None, 267.9)),
    ("DATA", "Share capital reduction (cancels cumulative loss)", (-2433.3, None, 20.0, None, 2413.3, None)),
    ("DATA", "Profit for the year", (None, None, None, None, 12.2, 12.2)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -4.5, None, None, -4.5)),
    ("TOTAL", "At 31 March 2017 (FY2017 closing)", (709.9, 15.6, -1.3, 0, 12.2, 736.4)),
    ("DATA", "Profit for the year", (None, None, None, None, 27.6, 27.6)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -2.4, None, None, -2.4)),
    ("TOTAL", "At 31 March 2018 (FY2018 closing)", (709.9, 15.6, -3.7, 0, 39.8, 761.6)),
    ("DATA", "Loss for the year", (None, None, None, None, -19.5, -19.5)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -1.9, None, None, -1.9)),
    ("TOTAL", "At 31 March 2019 (FY2019 closing)", (709.9, 15.6, -5.6, 0, 20.3, 740.2)),
    ("DATA", "Loss for the year", (None, None, None, None, -40.7, -40.7)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -0.3, None, None, -0.3)),
    ("TOTAL", "At 31 March 2020 (FY2020 closing)", (709.9, 15.6, -5.9, 0, -20.4, 699.2)),
    ("TOTAL", "At 1 April 2020 (FY2021 opening)", (709.9, 15.6, -5.9, 0, -20.4, 699.2)),
    ("DATA", "Profit for the year", (None, None, None, None, 42.8, 42.8)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, None, -0.4, None, -0.4)),
    ("TOTAL", "At 31 March 2021 (FY2021 closing)", (709.9, 15.6, -5.9, -0.4, 22.4, 741.6)),
    ("DATA", "Loss for the year", (None, None, None, None, -28.8, -28.8)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -0.3, -0.1, None, -0.4)),
    ("TOTAL", "At 31 March 2022 (FY2022 closing)", (709.9, 15.6, -6.2, -0.5, -6.4, 712.4)),
    ("DATA", "Loss for the year", (None, None, None, None, -4.5, -4.5)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -0.3, 0.1, None, -0.2)),
    ("TOTAL", "At 31 March 2023 (FY2023 closing)", (709.9, 15.6, -6.5, -0.4, -10.9, 707.7)),
    ("DATA", "Profit for the year", (None, None, None, None, 13.5, 13.5)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -0.3, -0.2, None, -0.5)),
    ("TOTAL", "At 31 March 2024 (FY2024 closing)", (709.9, 15.6, -6.8, -0.6, 2.6, 720.7)),
    ("DATA", "Profit for the year", (None, None, None, None, 7.2, 7.2)),
    ("DATA", "Capital injection", (45.0, None, None, None, None, 45.0)),
    ("DATA", "Equity contribution", (None, None, None, 1.1, None, 1.1)),
    ("DATA", "Transfer to profit and loss account", (None, None, None, -1.1, 1.1, None)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -0.3, -0.2, None, -0.5)),
    ("TOTAL", "At 31 March 2025 (FY2025 closing)", (754.9, 15.6, -7.1, -0.8, 10.9, 773.5)),
    ("DATA", "Profit for the year", (None, None, None, None, 17.0, 17.0)),
    ("DATA", "Capital injection", (55.0, None, None, None, None, 55.0)),
    ("DATA", "Transfer to profit and loss account", (None, None, None, 0.8, -0.8, None)),
    ("DATA", "Other comprehensive income/(loss)", (None, None, -0.3, None, None, -0.3)),
    ("TOTAL", "At 31 March 2026 (FY2026 closing)", (809.9, 15.6, -7.4, 0, 27.1, 845.2)),
]
bw.add_equity_changes_sheet(
    title="Mizuho International plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest. Consolidated Group basis FY2019 onward; Company-only "
              "basis FY2010-FY2018 (mixed Company-only Balance Sheet / Consolidated P&L basis for FY2008-FY2009 "
              "- see the 'REPORTING BASIS' source note; Total Equity is unaffected by that mix, since it nets "
              "out on consolidation). £m. Equity reconciliation ladder confirmed: every year's own closing "
              "balance ties exactly to both the next year's own opening balance and that year's own Balance "
              "Sheet Total Equity across all 18 years (FY2008-FY2025), with one disclosed exception: a real "
              "~£0.5m break between FY2014's closing position as originally filed (UK GAAP, Companies House) "
              "and the FRS102-restated FY2015 opening position shown in the FY2016 Annual Report - the 'FRS 102 "
              "transition adjustment' row makes that break explicit rather than silently plugging it. FY2025's "
              "Capital injection/Equity contribution/Transfer-to-P&L rows relate to a capital raise and the "
              "release of a net dilapidation provision following termination of the Company's sub-lease, per "
              "the source's own explanatory note. The FY2017 'Share capital reduction' cancelled MHI's "
              "cumulative loss balance (135,000,000 JPY ordinary shares and £111,534,584 ordinary shares were "
              "cancelled per the source's own explanatory note). HD-075: FY2008-FY2013 fold each year's own "
              "separately-disclosed 'Pension reserve' equity component into the 'Profit and loss account' "
              "column (Pension reserve left blank, matching the immediately following 'At 1 April 2013' row's "
              "own convention) since each year's own primary Balance Sheet shows only one combined 'Profit and "
              "loss account' line - the underlying source notes (note 26/28 'Equity') disclose the pension "
              "split for readers who want it, but it plays no part in this sheet's own column totals. The FY2008 "
              "opening row (1 April 2007) and that year's large £2,057.0m share capital increase, £20.0m "
              "dividend paid, and £0.2m fair value reserve release are all sourced from the FY2008 filing's own "
              "Equity note (note 28), which also gives the FY2007 opening position used as this ladder's "
              "starting point. FY2011's closing row uses that year's own originally-filed figures.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
)

bw.add_cash_flow_sheet(
    "Mizuho International plc — Consolidated Statement of Cash Flows",
    "Consolidated Group basis, £ millions. FY2008-FY2020 carry a statement rather than figures (and are "
    "certainly not zero): none of those years' Annual "
    "Reports/statutory filings include a cash flow statement, each invoking the FRS 1/FRS 102 exemption for a "
    "qualifying subsidiary whose ultimate parent (Mizuho Financial Group, Inc.) publishes consolidated financial "
    "statements including the Company - the same exemption basis as FY2021-FY2025's ENTITY NOTE. HD-075 "
    "confirmed the exemption is invoked explicitly in each of the FY2008-FY2013 Companies House filings too.",
    ROWS, sources(), first_col_width=66, source_height=240, unit_suffix=" (£m)", years=YEARS)

# ---------------------------------------------------------------
# Asset Quality - Mizuho is a wholesale/markets subsidiary (loans and
# advances to customers is a minor balance sheet line, e.g. £60.2m of
# £23,914.9m total assets in FY2025); its Pillar 3 disclosures do not
# publish an IFRS 9 stage split. Substituted with the Pillar 3 credit-risk
# exposures by credit quality step table (Table 23), the closest available
# disclosure of counterparty/credit risk quality across the book.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Credit risk exposures by credit quality step (standardised approach), net of CRM", {}),
    ("DATA", "Credit quality step 1", {"FY2026": 281.1, "FY2025": 158.3, "FY2024": 368.5, "FY2023": 403.5, "FY2022": 531.4, "FY2021": 303.7, "FY2020": 611.6, "FY2019": 8.5, "FY2018": 234.5, "FY2017": 114.1, "FY2016": 31.7, "FY2015": 5.3, "FY2014": 6.1}),
    ("DATA", "Credit quality step 2", {"FY2026": 205.9, "FY2025": 102.2, "FY2024": 72.2, "FY2023": 57.5, "FY2022": 29.7, "FY2021": 31.3, "FY2020": 57.9, "FY2019": 108.9, "FY2018": 52.0, "FY2017": 128.4, "FY2016": 54.3, "FY2015": 69.7, "FY2014": 61.2}),
    ("DATA", "Credit quality step 3", {"FY2026": 46.1, "FY2025": 0.0, "FY2024": 57.8, "FY2023": 56.2, "FY2022": 20.4, "FY2020": 0.0, "FY2019": 0.0, "FY2018": 0.0, "FY2016": 0.1}),
    ("DATA", "Credit quality step 4", {}),
    ("DATA", "Credit quality step 5", {"FY2026": 29.9, "FY2025": 17.7, "FY2024": 13.2, "FY2023": 9.9, "FY2022": 8.1, "FY2021": 6.9, "FY2020": 7.2, "FY2019": 8.7, "FY2015": 3.7, "FY2014": 3.2}),
    ("DATA", "Credit quality step 6", {"FY2026": 0.5, "FY2025": 1.1, "FY2024": 4.0, "FY2023": 3.9, "FY2022": 2.5, "FY2021": 1.7, "FY2020": 1.6, "FY2019": 1.1, "FY2018": 6.8, "FY2017": 0.8, "FY2016": 0.6}),
    ("DATA", "Unrated", {"FY2026": 99.6, "FY2025": 96.5, "FY2024": 70.1, "FY2023": 78.4, "FY2022": 70.5, "FY2021": 64.7, "FY2020": 64.7, "FY2019": 55.9, "FY2018": 81.1, "FY2017": 90.7, "FY2016": 89.3, "FY2015": 96.1, "FY2014": 48.9}),
    ("TOTAL", "Total net credit exposure", {"FY2026": 663.1, "FY2025": 375.8, "FY2024": 585.7, "FY2023": 609.5, "FY2022": 662.7, "FY2021": 408.2, "FY2020": 743.0, "FY2019": 183.1, "FY2018": 374.5, "FY2017": 334.0, "FY2016": 175.9, "FY2015": 174.8, "FY2014": 119.4}),
    ("DATA", "Memo: Total gross credit exposure (before CRM)", {"FY2026": 752.1, "FY2025": 420.8, "FY2024": 665.7, "FY2023": 681.1, "FY2022": 725.0, "FY2021": 437.9, "FY2020": 834.2, "FY2019": 257.9, "FY2018": 405.5, "FY2017": 401.6, "FY2016": 228.7, "FY2015": 174.8, "FY2014": 119.4}),
    ("DATA", "Credit risk RWAs (excluding CCR)", {"FY2026": 210.2, "FY2025": 150.5, "FY2024": 148.4, "FY2023": 140.1, "FY2022": 108.2, "FY2021": 92.8, "FY2020": 85.9, "FY2019": 88.0, "FY2018": 98.7, "FY2017": 117.7, "FY2016": 101.1, "FY2015": 118.5, "FY2014": 64.3}),
    ("DATA", "Credit risk RWA density (RWAs / net credit exposure)", {"FY2026": "31.70%", "FY2025": "40.05%", "FY2024": "25.34%", "FY2023": "22.99%", "FY2022": "16.33%", "FY2021": "22.73%", "FY2020": "11.56%", "FY2019": "48.06%", "FY2018": "26.36%", "FY2017": "35.24%", "FY2016": "57.48%", "FY2015": "67.79%", "FY2014": "53.87%"}),
]
bw.add_asset_quality_sheet(
    title="Mizuho International plc — Asset Quality",
    subtitle="Pillar 3 credit risk exposures by credit quality step (Table 23; the equivalent table carries a "
              "different number in earlier disclosures, e.g. Table 25 for FY2014, Table 18 for FY2015-FY2016), "
              "standardised approach, £m — substitutes for an IFRS 9 stage split, which this Group does not "
              "disclose (it runs no material customer lending book). FY2014-FY2016 report at 'Mizuho Securities "
              "UK Holdings Ltd' (MSUKH) group level, MHI's immediate parent, not at MHI level directly (see the "
              "P3 source dict comment) — broadly but not exactly comparable to the MHI-level figures used from "
              "FY2017 onward, since MHI is described in those disclosures as MSUKH's principal operating "
              "subsidiary rather than its sole business.",
    rows=asset_quality_rows,
    sources_text=p3_sources() + "\n\nCredit risk exposures and RWAs by credit quality step table, section 'Analysis of credit risk exposures', in each year's own Pillar 3 disclosure document listed above.",
    first_col_width=74,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# KM1 Key Metrics - Mizuho's own "Table 6: Key regulatory metrics", which
# each edition from 2022 onward states is "In line with PRA disclosure
# template 'UK KM1 - Key metrics template'". TWO CAPTION BLOCKS, deliberately
# not merged (map rule 24): the UK template from the FY2022 edition onward,
# and the older Basel/EBA-era key-metrics table the FY2018-FY2021 editions
# print, which is unnumbered and carries different captions ("Tier 2" as its
# own line, "EBA leverage ratio", no SREP rows and no NSFR rows). Each year
# comes from the edition in which it is the reporting year; FY2017 is the one
# exception and is flagged as such on the sheet.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "UK KM1 template - FY2022 to FY2026 editions (£m and %)", {}),
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1 Common Equity Tier 1 (CET1) capital (£m)", {"FY2026": 679.8, "FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8}),
    ("DATA", "2 Tier 1 capital (£m)", {"FY2026": 679.8, "FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8}),
    ("DATA", "3 Total capital (£m)", {"FY2026": 679.8, "FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8}),
    ("SECTION", "Risk-weighted assets amounts (RWAs)", {}),
    ("DATA", "4 Total risk-weighted assets (RWAs) (£m)", {"FY2026": 2595.5, "FY2025": 3353.2, "FY2024": 2790.7, "FY2023": 2241.7, "FY2022": 2057.9}),
    ("SECTION", "Capital ratios (as a percentage of RWAs)", {}),
    ("DATA", "5 Common Equity Tier 1 ratio (%)", {"FY2026": "26.19%", "FY2025": "20.00%", "FY2024": "22.84%", "FY2023": "28.00%", "FY2022": "31.14%"}),
    ("DATA", "6 Tier 1 ratio (%)", {"FY2026": "26.19%", "FY2025": "20.00%", "FY2024": "22.84%", "FY2023": "28.00%", "FY2022": "31.14%"}),
    ("DATA", "7 Total capital ratio (%)", {"FY2026": "26.19%", "FY2025": "20.00%", "FY2024": "22.84%", "FY2023": "28.00%", "FY2022": "31.14%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of RWAs)", {}),
    ("DATA", "7a Additional CET1 SREP requirements (%)", {"FY2026": "1.52%", "FY2025": "1.52%", "FY2024": "1.86%", "FY2023": "1.98%", "FY2022": "2.04%"}),
    ("DATA", "7d Total SREP own funds requirements (%)", {"FY2026": "9.52%", "FY2025": "9.52%", "FY2024": "9.86%", "FY2023": "9.98%", "FY2022": "10.04%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of RWAs)", {}),
    ("DATA", "8 Capital conservation buffer (%)", {"FY2026": "2.50%", "FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%"}),
    ("DATA", "9 Institution-specific countercyclical capital buffer (%)", {"FY2026": "0.73%", "FY2025": "0.93%", "FY2024": "0.61%", "FY2023": "0.28%", "FY2022": "0.04%"}),
    ("DATA", "11 Combined buffer requirement (%)", {"FY2026": "3.23%", "FY2025": "3.43%", "FY2024": "3.11%", "FY2023": "2.78%", "FY2022": "2.54%"}),
    ("DATA", "11a Overall capital requirements (%)", {"FY2026": "12.75%", "FY2025": "12.95%", "FY2024": "12.97%", "FY2023": "12.76%", "FY2022": "12.57%"}),
    ("DATA", "12 CET1 available after meeting the total SREP own funds requirements (%)", {"FY2026": "16.67%", "FY2025": "10.48%", "FY2024": "12.98%", "FY2023": "18.02%", "FY2022": "21.10%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13 Total exposure measure excluding claims on central banks (£m)", {"FY2026": 15334.8, "FY2025": 15999.6, "FY2024": 15668.5, "FY2023": 14812.8, "FY2022": 15727.1}),
    ("DATA", "14 Leverage ratio excluding claims on central banks (%)", {"FY2026": "4.43%", "FY2025": "4.19%", "FY2024": "4.07%", "FY2023": "4.24%", "FY2022": "4.07%"}),
    ("DATA", "14a Fully loaded ECL accounting model leverage ratio excluding claims on central banks (%)", {"FY2026": "4.43%", "FY2025": "4.19%", "FY2024": "4.07%", "FY2023": "4.24%"}),
    ("DATA", "14b Leverage ratio including claims on central banks (%)", {"FY2026": "4.37%", "FY2025": "4.16%", "FY2024": "3.98%", "FY2023": "4.13%", "FY2022": "3.95%"}),
    ("DATA", "14c Average leverage ratio excluding claims on central banks (%)", {"FY2026": "4.22%", "FY2025": "4.15%", "FY2024": "3.91%", "FY2023": "4.04%"}),
    ("DATA", "14d Average leverage ratio including claims on central banks (%)", {"FY2026": "4.16%", "FY2025": "4.12%", "FY2024": "3.83%", "FY2023": "3.91%"}),
    ("DATA", "14e Countercyclical leverage ratio buffer (%)", {"FY2026": "0.30%", "FY2025": "0.30%", "FY2024": "0.20%", "FY2023": "0.10%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15 Total high-quality liquid assets (HQLA) (Weighted value - average) (£m)", {"FY2026": 1931.8, "FY2025": 2014.2, "FY2024": 2079.7, "FY2023": 2090.2, "FY2022": 2035.9}),
    ("DATA", "16a Cash outflows - Total weighted value (£m)", {"FY2026": 2883.0, "FY2025": 3395.1, "FY2024": 3357.2, "FY2023": 2664.6, "FY2022": 2279.3}),
    ("DATA", "16b Cash inflows - Total weighted value (£m)", {"FY2026": 2445.6, "FY2025": 2710.9, "FY2024": 2775.5, "FY2023": 2173.1, "FY2022": 2007.4}),
    ("DATA", "16 Total net cash outflows (adjusted value) (£m)", {"FY2026": 720.8, "FY2025": 850.4, "FY2024": 839.3, "FY2023": 716.3, "FY2022": 574.9}),
    ("DATA", "17 Liquidity coverage ratio (%)", {"FY2026": "272.4%", "FY2025": "239.20%", "FY2024": "250.39%", "FY2023": "302.67%", "FY2022": "364.04%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18 Total available stable funding (£m)", {"FY2026": 2776.7, "FY2025": 3196.7, "FY2024": 2768.8, "FY2023": 2253.8, "FY2022": 2509.6}),
    ("DATA", "19 Total required stable funding (£m)", {"FY2026": 1883.5, "FY2025": 2609.1, "FY2024": 2151.9, "FY2023": 1602.3, "FY2022": 1412.2}),
    ("DATA", "20 NSFR ratio (%)", {"FY2026": "147.4%", "FY2025": "122.52%", "FY2024": "128.67%", "FY2023": "140.66%", "FY2022": "177.71%"}),
    ("SECTION", "Pre-2022 key regulatory metrics table - FY2018 to FY2021 editions, as printed: unnumbered rows, different captions (£m and %)", {}),
    ("SECTION", "Available capital (amounts)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) (£m)", {"FY2021": 675.6, "FY2020": 623.7, "FY2019": 662.5, "FY2018": 690.9, "FY2017": 658.3}),
    ("DATA", "Tier 2 (£m)", {"FY2021": 36.0, "FY2020": 45.0, "FY2019": 45.0, "FY2018": 45.0, "FY2017": 45.0}),
    ("DATA", "Total capital (£m)", {"FY2021": 711.6, "FY2020": 668.7, "FY2019": 707.5, "FY2018": 735.9, "FY2017": 703.3}),
    ("SECTION", "Risk-weighted assets (amounts)", {}),
    ("DATA", "Total risk-weighted assets (RWA) (£m)", {"FY2021": 2171.0, "FY2020": 3115.3, "FY2019": 2385.8, "FY2018": 2257.0, "FY2017": 2002.2}),
    ("SECTION", "Risk-based capital ratios as a percentage of RWA", {}),
    ("DATA", "Common Equity Tier 1 ratio (%)", {"FY2021": "31.12%", "FY2020": "20.02%", "FY2019": "27.8%", "FY2018": "30.6%", "FY2017": "32.9%"}),
    ("DATA", "Tier 1 ratio", {"FY2021": "31.12%", "FY2020": "20.02%", "FY2019": "27.8%", "FY2018": "30.6%", "FY2017": "32.9%"}),
    ("DATA", "Total capital ratio (%)", {"FY2021": "32.78%", "FY2020": "21.46%", "FY2019": "29.7%", "FY2018": "32.6%", "FY2017": "35.1%"}),
    ("SECTION", "Additional CET1 buffer requirements as a percentage of RWA", {}),
    ("DATA", "Capital conservation buffer requirement (2.5% from 2019) (%)", {"FY2021": "2.50%", "FY2020": "2.50%", "FY2019": "2.5%", "FY2018": "1.875%", "FY2017": "1.250%"}),
    ("DATA", "Countercyclical buffer requirement (%)", {"FY2021": "0.04%", "FY2020": "0.09%", "FY2019": "0.256%", "FY2018": "0.074%", "FY2017": "0.081%"}),
    ("DATA", "Total of bank CET1 specific buffer requirements (%)", {"FY2021": "2.54%", "FY2020": "2.59%", "FY2019": "2.756%", "FY2018": "1.949%", "FY2017": "1.331%"}),
    ("SECTION", "EBA leverage ratio", {}),
    ("DATA", "Total EBA leverage ratio exposure measure (£m)", {"FY2021": 14224.7, "FY2020": 16674.5, "FY2019": 17704.5, "FY2018": 15347.8, "FY2017": 15108.3}),
    ("DATA", "EBA leverage ratio (%)", {"FY2021": "4.75%", "FY2020": "3.74%", "FY2019": "3.74%", "FY2018": "4.50%", "FY2017": "4.36%"}),
    ("SECTION", "Liquidity Coverage Ratio (LCR)", {}),
    ("DATA", "Total High Quality Liquid Assets (HQLA) (£m)", {"FY2021": 2166.4, "FY2020": 2073.6, "FY2019": 2040.4, "FY2018": 1996.8, "FY2017": "N/A"}),
    ("DATA", "Total net cash outflow (£m)", {"FY2021": 724.9, "FY2020": 649.0, "FY2019": 513.3, "FY2018": 517.3, "FY2017": "N/A"}),
    ("DATA", "LCR ratio (%)", {"FY2021": "303%", "FY2020": "340%", "FY2019": "416%", "FY2018": "396%", "FY2017": "N/A"}),
]

bw.add_km1_sheet(
    title="Mizuho International plc — KM1 Key Metrics",
    subtitle="The Group's own \"Table 6: Key regulatory metrics\", reproduced whole in Mizuho's own row "
             "order, row numbers, labels and precision, on the consolidated Mizuho International plc "
             "Group basis the Pillar 3 disclosures use. TWO BLOCKS, deliberately not merged: the UK KM1 "
             "template as printed in the FY2022-FY2026 editions (numbered rows), and the older "
             "Basel/EBA-era key-metrics table the FY2018-FY2021 editions print (no row numbers, a "
             "separate \"Tier 2\" line, \"EBA leverage ratio\", and no SREP or NSFR rows at all). Every "
             "column is that year's own edition except FY2017, which is the FY2018 edition's comparative "
             "— see the source note. £m for amounts, percentages as printed.",
    rows=km1_rows,
    sources_text=p3_sources() + "\n\n" + (
        "KM1 SHEET SOURCES - one edition per column, per this project's own-year sourcing rule. Each is "
        "\"Table 6: Key regulatory metrics\", cited at the folio printed on the page itself:\n"
        "FY2026: Pillar 3 disclosures 2026, Table 6, p.17.\n"
        "FY2025: Pillar 3 disclosures 2025, Table 6, p.18.\n"
        "FY2024: Pillar 3 disclosures 2024, Table 6, p.18.\n"
        "FY2023: Pillar 3 disclosures 2023, Table 6, p.17.\n"
        "FY2022: Pillar 3 disclosures 2022, Table 6, p.15.\n"
        "FY2021: Pillar 3 disclosures 2021, Table 6, p.14.\n"
        "FY2020: Pillar 3 disclosures 2020, Table 6, p.16.\n"
        "FY2019: Pillar 3 disclosures 2019, Table 6, p.14.\n"
        "FY2018: Pillar 3 disclosures 2018, Table 6, p.15.\n"
        "FY2017: NO KEY-METRICS TABLE EXISTS IN THE FY2017 EDITION - this column is the FY2018 "
        "edition's own 2017 comparative column (Table 6, p.15), and is the only column on this sheet "
        "not taken from its own year's edition. It is filled rather than left blank because the "
        "FY2017 document publishes no such table at all, so there is no original disclosure for a "
        "later one to displace; the distinction matters, and a BLANK on this sheet means the figure "
        "was never published for that date in any edition. The FY2017 and FY2016 editions were both "
        "read in full: neither contains a key-metrics table, and the extraction is not at fault - the "
        "FY2017 document is rich on neighbouring terms and does print a leverage exposure table and a "
        "CC1-style own-funds template, but has no line 'Total risk-weighted assets', no 'Liquidity "
        "Coverage Ratio' heading and no 'Total capital ratio' row anywhere.\n"
        "FY2016 AND EARLIER ARE BLANK FOR TWO REASONS AT ONCE: no edition prints the table, and the "
        "FY2014-FY2016 Pillar 3 documents are in any case disclosures of Mizuho Securities UK "
        "Holdings Ltd (MSUKH), MHI's immediate parent, not of MHI - a parent's consolidated figures "
        "are not this entity's and are not reproduced here on any sheet.\n\n"
        "WHY TWO BLOCKS RATHER THAN ONE SERIES. The template changed at 1 January 2022 and the two "
        "versions are not row-compatible: the pre-2022 table has no SREP rows, no NSFR rows, no "
        "'including claims on central banks' leverage variants and no average-leverage rows, while it "
        "does carry a standalone 'Tier 2' line that the UK template does not. Its leverage rows are "
        "also on the EBA exposure measure, which is the basis break map rule 5 exists for. Nothing is "
        "carried across the boundary and no row is filled by inference from the other block.\n\n"
        "ROWS THE BANK DID NOT PRINT ARE BLANK, NOT ZERO. Each FY2022-FY2026 edition states: 'Only "
        "rows relevant to the Group are shown in Table 6, remaining rows from the PRA disclosure "
        "template have been left out as these are nil rows' - which is why rows 10, UK 8a, UK 9a and "
        "UK 10a never appear. Within the UK block, rows 14a, 14c, 14d and 14e are blank for FY2022 "
        "because the FY2022 edition does not print them (it prints 'n/a' in its own 2021 comparative "
        "column for several rows, but that column is not used here - FY2021 comes from the FY2021 "
        "edition). The FY2018 edition prints 'N/A' for all three LCR rows in its 2017 comparative, "
        "footnoted 'Not applicable as this disclosure is being made for the first time in 2018'; that "
        "glyph is reproduced as printed rather than blanked.\n\n"
        "FY2025 LCR - THREE DIFFERENT PUBLISHED FIGURES FOR ONE DATE, ALL RECORDED, NONE RECONCILED.\n"
        "  (a) This sheet's FY2025 column carries the FY2025 edition's own figures: HQLA 2,014.2, net "
        "cash outflows 850.4, LCR 239.20%.\n"
        "  (b) The FY2026 edition RESTATES that comparative, with its own footnote: 'Values for the "
        "year ended 31 March 2025 were reported incorrectly before. Comparative values have been "
        "restated' - giving HQLA 2,056.1, net cash outflows 891.2 and LCR 236.5%. Under this "
        "project's own-year rule the original stands in the FY2025 column and the restatement is "
        "recorded here rather than substituted.\n"
        "  (c) The LCR metric sheet in this workbook carries 268.7% for FY2025, from the Annual "
        "Report 2025's KPI section. The Pillar 3 row is explicitly a twelve-month AVERAGE (row 15 is "
        "captioned 'Weighted value - average'); the Annual Report states its figure without that "
        "qualification. Two of the bank's own documents, two bases, both transcribed as printed - the "
        "workbook's own verifier reports this as a KM1-vs-metric-sheet disagreement and that report "
        "is correct and expected.\n\n"
        "OTHER SMALL DISAGREEMENTS WITH THE SINGLE-METRIC SHEETS, all rounding rather than substance: "
        "the Leverage Ratio sheet carries FY2025 as 4.2% (Annual Report) against row 14's 4.19% "
        "(Pillar 3), and the CET1/Tier 1/Total Capital Ratio sheets carry one-decimal forms for "
        "FY2025 and FY2024 where the template prints two. Nothing has been re-rounded in either "
        "direction to make them agree."
    ),
    first_col_width=86,
    source_height=420,
)


def metric(name, unit, values, note=None):
    bw.add_metric_sheet(name, unit, [(name, values)], p3_sources(), note=note, first_col_width=48, source_height=220)

metric("CET1 Capital", "£ millions", {"FY2026": 679.8, "FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8, "FY2021": 675.6, "FY2020": 623.7, "FY2019": 662.5, "FY2018": 690.9, "FY2017": 658.3, "FY2016": 408.3, "FY2015": 451.9, "FY2014": 456.9}, "FY2025 Annual Report states regulatory capital consists solely of Tier 1 capital; treated as CET1 for this metric because no Tier 2 capital is reported. FY2014-FY2016 capital resources consisted solely of common equity Tier 1 (no Tier 2 issued yet); FY2014-FY2016 are MSUKH group-level figures, not MHI-level (see the P3 source dict comment).")
metric("CET1 Ratio", "%", {"FY2026": "26.19%", "FY2025": "20.0%", "FY2024": "22.8%", "FY2023": "28.0%", "FY2022": "31.14%", "FY2021": "31.12%", "FY2020": "20.02%", "FY2019": "27.8%", "FY2018": "30.6%", "FY2017": "32.9%", "FY2016": "36.4%", "FY2015": "49.5%", "FY2014": "50.3%"})
metric("Tier 1 Capital", "£ millions", {"FY2026": 679.8, "FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8, "FY2021": 675.6, "FY2020": 623.7, "FY2019": 662.5, "FY2018": 690.9, "FY2017": 658.3, "FY2016": 408.3, "FY2015": 451.9, "FY2014": 456.9})
metric("Tier 1 Ratio", "%", {"FY2026": "26.19%", "FY2025": "20.0%", "FY2024": "22.84%", "FY2023": "28.00%", "FY2022": "31.14%", "FY2021": "31.12%", "FY2020": "20.02%", "FY2019": "27.8%", "FY2018": "30.6%", "FY2017": "32.9%", "FY2016": "36.4%", "FY2015": "49.5%", "FY2014": "50.3%"})
metric("Total Capital", "£ millions", {"FY2026": 679.8, "FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8, "FY2021": 711.6, "FY2020": 668.7, "FY2019": 707.5, "FY2018": 735.9, "FY2017": 703.3, "FY2016": 453.3, "FY2015": 451.9, "FY2014": 456.9}, "FY2015/FY2014: Total capital equals Tier 1 capital because no Tier 2 capital had yet been issued (first appears FY2016).")
metric("Total Capital Ratio", "%", {"FY2026": "26.19%", "FY2025": "20.0%", "FY2024": "22.84%", "FY2023": "28.00%", "FY2022": "31.14%", "FY2021": "32.78%", "FY2020": "21.46%", "FY2019": "29.7%", "FY2018": "32.6%", "FY2017": "35.1%", "FY2016": "40.4%", "FY2015": "49.5%", "FY2014": "50.3%"})
metric("Total RWAs", "£ millions", {"FY2026": 2595.5, "FY2025": 3353.2, "FY2024": 2790.7, "FY2023": 2241.7, "FY2022": 2057.9, "FY2021": 2171.0, "FY2020": 3115.3, "FY2019": 2385.8, "FY2018": 2257.0, "FY2017": 2002.2, "FY2016": 1122.3, "FY2015": 913.7, "FY2014": 908.5})

# RWA Breakdown - Pillar 3 UK OV1 template, placed right after Total RWAs
# per the locked sheet order. All 5 available years tie exactly to the
# Total RWAs figure above (each year's own disclosed Total row used
# directly, not a recomputed sum - individual risk-type rows carry £0.1-
# 0.2m source rounding artifacts against that Total, consistent with the
# pattern seen across other banks in this rollout).
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2026": 210.2, "FY2025": 150.5, "FY2024": 148.4, "FY2023": 140.1, "FY2022": 108.2, "FY2021": 92.8, "FY2020": 85.9, "FY2019": 88.0, "FY2018": 98.7, "FY2017": 117.7, "FY2016": 101.1, "FY2015": 118.5, "FY2014": 64.3}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2026": 550.3, "FY2025": 682.4, "FY2024": 638.9, "FY2023": 530.6, "FY2022": 357.3, "FY2021": 259.6, "FY2020": 232.8, "FY2019": 181.4, "FY2018": 182.3, "FY2017": 184.5, "FY2016": 134.0, "FY2015": 91.6, "FY2014": 123.8}),
    ("DATA", "Concentration risk", {"FY2016": 0.0, "FY2015": 34.4}),
    ("DATA", "Settlement risk", {"FY2026": 0.0, "FY2025": 0.0, "FY2024": 0.2, "FY2023": 0.1, "FY2022": 0.2, "FY2021": 0.1}),
    ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2026": 1189.4, "FY2025": 2014.2, "FY2024": 1626.8, "FY2023": 1166.8, "FY2022": 1224.3, "FY2021": 1445.4, "FY2020": 2442.2, "FY2019": 1722.7, "FY2018": 1598.7, "FY2017": 1393.4, "FY2016": 659.7, "FY2015": 552.0, "FY2014": 633.3}),
    ("DATA", "Large exposures", {"FY2023": 14.6}),
    ("DATA", "Operational risk", {"FY2026": 645.6, "FY2025": 506.1, "FY2024": 376.6, "FY2023": 389.6, "FY2022": 368.1, "FY2021": 373.3, "FY2020": 354.4, "FY2019": 393.6, "FY2018": 377.3, "FY2017": 306.7, "FY2016": 235.1, "FY2015": 117.1, "FY2014": 87.1}),
    ("TOTAL", "Total", {"FY2026": 2595.5, "FY2025": 3353.2, "FY2024": 2790.7, "FY2023": 2241.7, "FY2022": 2057.9, "FY2021": 2171.0, "FY2020": 3115.3, "FY2019": 2385.8, "FY2018": 2257.0, "FY2017": 2002.2, "FY2016": 1122.3, "FY2015": 913.7, "FY2014": 908.5}),
]
bw.add_rwa_breakdown_sheet(
    title="Mizuho International plc — RWA Breakdown",
    subtitle="Consolidated Group basis FY2019 onward; MHI Company-only basis FY2017-FY2018; MSUKH group-level "
              "basis FY2014-FY2016 (see the P3 source dict comment). Pillar 3 RWA-by-risk-type template (labelled "
              "'UK OV1' from FY2021 onward, an unlabelled equivalent table in earlier years - Table 10 for "
              "FY2018-FY2020, Table 9 for FY2014-FY2017; column/row numbering shifts across years but the risk "
              "categories are consistent), only non-nil rows shown per each source document's own convention, £m. "
              "'Large exposures' (row 22a of the PRA template) only appears as a non-nil row in the FY2023 report. "
              "'Concentration risk' was only disclosed as a separate line in the FY2015-FY2016 MSUKH Pillar 3 "
              "documents (nil/folded into credit risk in all other years). FY2016's own five risk-type rows here "
              "sum to £1,129.9m against the FY2016 document's own stated Total of £1,122.3m (a ~£7.6m/0.7% "
              "reconciling difference disclosed in the source table itself, not a transcription error here - each "
              "row is transcribed as printed).",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + "\n\nRWAs and Pillar 1 capital requirements table (by risk type) in each year's own Pillar 3 disclosure document listed above.",
    first_col_width=76,
    source_height=260,
    unit_suffix=" (£m)",
)
metric("Leverage Ratio", "%", {"FY2026": "4.43%", "FY2025": "4.2%", "FY2024": "4.07%", "FY2023": "4.24%", "FY2022": "4.07%", "FY2021": "4.75%", "FY2020": "3.74%", "FY2019": "3.74%", "FY2018": "4.50%", "FY2017": "4.36%", "FY2016": "3.28%", "FY2015": "1.87%"}, "FY2014 leverage ratio was discussed qualitatively (implementation of PRA bank-level reporting was noted as having 'commenced') but no computed ratio was numerically disclosed in the FY2014 Pillar 3 document.")
metric("LCR", "%", {"FY2026": "272.4%", "FY2025": "268.7%", "FY2024": "250.39%", "FY2023": "302.67%", "FY2022": "364.04%", "FY2021": "303.00%", "FY2020": "340%", "FY2019": "416%", "FY2018": "396%"}, "LCR was first disclosed in the FY2018 Pillar 3 document (the document itself states this); not disclosed FY2014-FY2017.")
metric("NSFR", "%", {"FY2026": "147.4%", "FY2025": "122.5%", "FY2024": "128.67%", "FY2023": "140.66%", "FY2022": "177.71%"}, "NSFR was not disclosed in the 2021 report or any FY2014-FY2020 report; 2025 is from the Annual Report KPI section.")
# GA-006 (2026-09-18): this sheet was WHOLLY empty - 13 year columns, not one
# cell - with the finding sitting only in the note. It is the whole of this
# bank's leading-empty count in the census. The finding is now in the cells.
# Note the old note stopped at FY2025 and the workbook already carried FY2026,
# so the newest year was not covered by the claim at all; re-established below
# against the two newest editions directly.
MREL_NA = "Not disclosed - MHI publishes no MREL ratio in any edition"
metric("MREL Ratio", "%",
       {y: MREL_NA for y in ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
                             "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]},
       "MREL ratio is not numerically disclosed in any Mizuho International plc annual report or Pillar 3 "
       "disclosure. RE-ESTABLISHED WITH A CONTROL 2026-09-18 rather than carried forward - the previous "
       "note asserted this for FY2014-FY2025 and was already out of date, since the workbook carries "
       "FY2026. Whole-document search of the two newest editions, both text-native and downloaded fresh "
       "(%PDF-, application/pdf): the FY2026 consolidated Pillar 3 (217,429 characters) returns ZERO hits "
       "for 'MREL', 'minimum requirement for own funds' and 'TLAC', against 145 hits for 'capital', "
       "231 for 'ratio' and 10 for 'own funds' in the same extraction; the FY2025 edition (224,343 "
       "characters) returns the same three zeros against 152 and 228. So the zero is a fact about the "
       "documents, not a failure of the search. The FY2026 Annual Report (696,912 characters) likewise "
       "returns zero for all three.\n"
       "WHAT THE DOCUMENTS DO SAY, which is consistent with there being nothing to find. The FY2026 "
       "Pillar 3 reproduces the PRA's 'UK CCA: Main features of regulatory own funds instruments and "
       "eligible liabilities instruments' template - i.e. the template that WOULD carry an eligible-"
       "liabilities instrument if MHI had one - and its only instrument is ordinary share capital, with "
       "row 34a 'Type of subordination (only for eligible liabilities)' printed 'n/a'. The FY2026 "
       "Annual Report states that the Group 'continues to participate actively in Mizuho Financial "
       "Group's recovery and resolution planning', i.e. resolution is planned at the Japanese parent "
       "level. That is context, not proof of a scope exclusion, and it is recorded as context: what is "
       "established here is that MHI publishes no MREL ratio, not why.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total Assets", {"FY2026": 24841.5, "FY2025": 23914.9, "FY2024": 24933.9, "FY2023": 27378.9, "FY2022": 22058.9, "FY2021": 18208.4, "FY2020": 25045.1, "FY2019": 19384.1, "FY2018": 15517.3, "FY2017": 15395.2, "FY2016": 13192.8, "FY2015": 21487.5, "FY2014": 28883.2}),
        ("Reverse repurchase agreements with customers", {"FY2026": 5981.7, "FY2025": 4587.1, "FY2024": 3059.6, "FY2023": 2303.5, "FY2022": 5417.0, "FY2021": 4288.6, "FY2020": 5895.2, "FY2019": 7204.8, "FY2018": 4636.4, "FY2017": 5106.9, "FY2016": 3176.7, "FY2015": 5083.7}),
        ("Derivative assets", {"FY2026": 9910.3, "FY2025": 8520.1, "FY2024": 9707.7, "FY2023": 13072.6, "FY2022": 6443.1, "FY2021": 6513.8, "FY2020": 11566.9, "FY2019": 4451.4, "FY2018": 2136.2, "FY2017": 1498.4, "FY2016": 424.0, "FY2015": 301.9, "FY2014": 204.7}),
        ("Total Equity", {"FY2026": 845.2, "FY2025": 773.5, "FY2024": 720.7, "FY2023": 707.7, "FY2022": 712.4, "FY2021": 741.6, "FY2020": 699.2, "FY2019": 740.2, "FY2018": 761.6, "FY2017": 736.4, "FY2016": 460.8, "FY2015": 441.6, "FY2014": 439.6}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Net income from operations", {"FY2026": 396.7, "FY2025": 373.4, "FY2024": 244.1, "FY2023": 194.4, "FY2022": 166.3, "FY2021": 265.1, "FY2020": 157.5, "FY2019": 174.6, "FY2018": 235.0, "FY2017": 220.3, "FY2016": 145.6, "FY2015": 131.8, "FY2014": 87.6}),
        ("Operating expenses", {"FY2026": -376.2, "FY2025": -367.6, "FY2024": -229.1, "FY2023": -204.8, "FY2022": -203.9, "FY2021": -221.3, "FY2020": -207.6, "FY2019": -203.9, "FY2018": -205.2, "FY2017": -208.1, "FY2016": -161.0, "FY2015": -126.9, "FY2014": -115.6}),
        ("Profit/(loss) for the year", {"FY2026": 17.0, "FY2025": 7.2, "FY2024": 13.5, "FY2023": -4.5, "FY2022": -28.8, "FY2021": 42.8, "FY2020": -40.7, "FY2019": -19.5, "FY2018": 27.6, "FY2017": 12.2, "FY2016": -15.4, "FY2015": 4.9, "FY2014": -28.0}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2026": 773.5, "FY2025": 720.7, "FY2024": 707.7, "FY2023": 712.4, "FY2022": 741.6, "FY2021": 699.2, "FY2020": 740.2, "FY2019": 761.6, "FY2018": 736.4, "FY2017": 460.8, "FY2016": 441.6, "FY2015": 439.1, "FY2014": 425.1}),
        ("Profit/(loss) for the year", {"FY2026": 17.0, "FY2025": 7.2, "FY2024": 13.5, "FY2023": -4.5, "FY2022": -28.8, "FY2021": 42.8, "FY2020": -40.7, "FY2019": -19.5, "FY2018": 27.6, "FY2017": 12.2, "FY2016": -15.4, "FY2015": 4.9, "FY2014": -28.0}),
        ("Other equity movements, net", {"FY2026": 54.7, "FY2025": 45.6, "FY2024": -0.5, "FY2023": -0.2, "FY2022": -0.4, "FY2021": -0.4, "FY2020": -0.3, "FY2019": -1.9, "FY2018": -2.4, "FY2017": 263.4, "FY2016": 34.6, "FY2015": -2.4, "FY2014": 42.5}),
        ("Closing equity", {"FY2026": 845.2, "FY2025": 773.5, "FY2024": 720.7, "FY2023": 707.7, "FY2022": 712.4, "FY2021": 741.6, "FY2020": 699.2, "FY2019": 740.2, "FY2018": 761.6, "FY2017": 736.4, "FY2016": 460.8, "FY2015": 441.6, "FY2014": 439.6}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[("Net cash flow from operating activities", CF["Net cash flows from operating activities"]), ("Net cash flows used in investing activities", CF["Net cash flows used in investing activities"]), ("Cash and cash equivalents at end of period", CF["Cash and cash equivalents at the end of the period"])],
    cash_flow_unit="£m",
    ratios=[("CET1 Ratio", {"FY2026": "26.19%", "FY2025": "20.0%", "FY2024": "22.8%", "FY2023": "28.0%", "FY2022": "31.14%", "FY2021": "31.12%", "FY2020": "20.02%", "FY2019": "27.8%", "FY2018": "30.6%", "FY2017": "32.9%", "FY2016": "36.4%", "FY2015": "49.5%", "FY2014": "50.3%"}), ("Leverage Ratio", {"FY2026": "4.43%", "FY2025": "4.2%", "FY2024": "4.07%", "FY2023": "4.24%", "FY2022": "4.07%", "FY2021": "4.75%", "FY2020": "3.74%", "FY2019": "3.74%", "FY2018": "4.50%", "FY2017": "4.36%", "FY2016": "3.28%", "FY2015": "1.87%"})],
    note="Annual data; Consolidated Group basis FY2019-FY2025, Company-only basis FY2014-FY2018 (see the Balance Sheet sheet's REPORTING BASIS note). Cash flow totals are blank for FY2014-FY2020 (no cash flow statement prepared those years).",
)

bw.save("/Users/armaan/code/katalysis/banks/MIZUHO INTERNATIONAL FINANCIALS.xlsx")
