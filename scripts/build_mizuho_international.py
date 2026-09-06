import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# Mizuho International plc (company 01203696, FRN 119256), confirmed against
# Banks List 2608.xlsx and Companies House.  The reports present consolidated
# Mizuho International plc Group figures in GBP millions.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]

# HD-047: extended FY2014-FY2020 back from FY2021, capped at FY2014 by explicit
# project-wide decision (Pillar 3 pre-CRD IV/Basel III isn't comparable), even
# though the confirmed archive goes back to FY2008 (HD-004). FY2015-FY2020
# Annual Reports and all FY2014-FY2020 Pillar 3 disclosures are on Mizuho's own
# site; FY2014's Annual Report is not (see FY2014 Companies House note below).
AR = {
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
P3 = {
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
    "Company did not yet prepare group accounts. FY2014 is Company-only, originally-"
    "filed UK GAAP (pre-FRS 102), sourced from the Companies House statutory filing "
    "rather than Mizuho's own site (see AR/P3 source dict comments) - there is a real "
    "~£0.5m equity break between FY2014 as originally filed and the FRS102-restated "
    "FY2015 opening position (see the Statement of Changes in Equity's transition row). "
    "None of FY2014-FY2020 include a cash flow statement (FRS 1/FRS 102 exemption for "
    "a qualifying subsidiary whose ultimate parent publishes consolidated accounts)."
)

CF = {
    "Profit / (loss) before tax": {"FY2025": 5.8, "FY2024": 15.0, "FY2023": -10.4, "FY2022": -37.6, "FY2021": 43.8},
    "Non-cash items included in profit / (loss) before tax": {"FY2025": -30.0, "FY2024": -23.0, "FY2023": -6.3, "FY2022": 12.6, "FY2021": 23.3},
    "Provision for liabilities": {"FY2025": 0.1, "FY2024": -0.9, "FY2023": 0.9, "FY2022": -0.2, "FY2021": -0.4},
    "Movement in Other Comprehensive Income": {"FY2025": -0.5, "FY2024": -0.4, "FY2023": -0.1, "FY2022": -0.4, "FY2021": -0.5},
    "Change in operating assets": {"FY2025": 846.1, "FY2024": 2479.7, "FY2023": -5424.2, "FY2022": -3613.0, "FY2021": 6374.7},
    "Change in operating liabilities": {"FY2025": -938.8, "FY2024": -2313.4, "FY2023": 5456.5, "FY2022": 4012.7, "FY2021": -6952.2},
    "Interest paid": {"FY2025": -93.3, "FY2024": -92.7, "FY2023": -0.1, "FY2022": -0.2, "FY2021": -1.3},
    "Interest received": {"FY2025": 124.2, "FY2024": 139.8, "FY2023": 11.0, "FY2022": 14.4, "FY2021": 16.4},
    "Tax (paid) / received": {"FY2025": -6.1, "FY2024": 12.6, "FY2023": -2.0, "FY2022": -3.4, "FY2021": 10.5},
    "Net cash flows from operating activities": {"FY2025": -92.5, "FY2024": 216.7, "FY2023": 25.3, "FY2022": 384.9, "FY2021": -485.7},
    "Net investment in shares in group undertakings": {"FY2025": -1.4, "FY2024": -0.1, "FY2023": -0.5, "FY2022": -2.0, "FY2021": -0.1},
    "Dividends from investment in shares in group undertakings": {"FY2025": 0.4, "FY2024": 0.2, "FY2023": 0.3, "FY2022": 0.7, "FY2021": 0.4},
    "Purchase of intangible assets": {"FY2025": -43.8, "FY2024": -27.2, "FY2023": -28.7, "FY2022": -25.3, "FY2021": -21.8},
    "Purchase of tangible assets": {"FY2025": -5.2, "FY2024": -5.8, "FY2023": -2.7, "FY2022": -6.4, "FY2021": -3.6},
    "Net cash flows used in investing activities": {"FY2025": -50.0, "FY2024": -32.9, "FY2023": -31.6, "FY2022": -33.0, "FY2021": -25.1},
    "Net repayment from debt securities in issue": {"FY2025": -101.5, "FY2024": -221.2, "FY2023": -139.6, "FY2022": -87.8, "FY2021": 75.6},
    "Net repayment of subordinated liabilities": {"FY2022": -45.0},
    "Proceeds from the issuance of equity": {"FY2025": 45.0},
    "Net cash flows from / (used in) financing activities": {"FY2025": -56.5, "FY2024": -221.2, "FY2023": -139.6, "FY2022": -132.8, "FY2021": 75.6},
    "Net (decrease) / increase in cash and cash equivalents": {"FY2025": -199.0, "FY2024": -37.4, "FY2023": -145.9, "FY2022": 219.1, "FY2021": -435.2},
    "Effects of exchange rates on cash and cash equivalents": {"FY2025": -0.9, "FY2024": -4.2, "FY2023": 4.3, "FY2022": 2.2, "FY2021": -6.6},
    "Cash and cash equivalents at beginning of the period": {"FY2025": 375.6, "FY2024": 417.2, "FY2023": 558.8, "FY2022": 337.5, "FY2021": 779.3},
    "Cash and cash equivalents at the end of the period": {"FY2025": 175.7, "FY2024": 375.6, "FY2023": 417.2, "FY2022": 558.8, "FY2021": 337.5},
}

ROWS = [("SECTION", "Operating activities", {})]
for label in list(CF)[:10]:
    ROWS.append(("TOTAL" if label == "Net cash flows from operating activities" else "DATA", label, CF[label]))
ROWS.append(("SECTION", "Investing activities", {}))
for label in list(CF)[10:15]:
    ROWS.append(("TOTAL" if label == "Net cash flows used in investing activities" else "DATA", label, CF[label]))
ROWS.append(("SECTION", "Financing activities", {}))
for label in list(CF)[15:19]:
    ROWS.append(("TOTAL" if label == "Net cash flows from / (used in) financing activities" else "DATA", label, CF[label]))
for label in list(CF)[19:]:
    ROWS.append(("TOTAL" if "cash equivalents" in label else "DATA", label, CF[label]))

def sources():
    return ENTITY_NOTE + "\n\nOfficial sources — Mizuho International plc Annual Reports: " + "; ".join(f"{y}: {u}" for y, u in AR.items())

def p3_sources():
    return ENTITY_NOTE + "\n\nOfficial Mizuho International plc Pillar 3 disclosures: " + "; ".join(f"{y}: {u}" for y, u in P3.items())

STATEMENTS_SOURCES = (
    sources()
    + "\n\nBalance Sheet/P&L/Equity figures are the Consolidated Mizuho International plc Group basis "
      "for FY2019-FY2025 (distinct from the Company-only basis also shown in each Annual Report). "
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
)

bw = BankWorkbook("Mizuho International plc", YEARS, header_color="7A3E9D")

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total Equity is the independent check value for the equity
# sheet below. All 5 years tie exactly.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 115.5, "FY2024": 328.5, "FY2023": 370.4, "FY2022": 481.0, "FY2021": 227.5, "FY2020": 601.0, "FY2019": 3.3, "FY2018": 230.2, "FY2017": 112.5, "FY2016": 27.3}),
    ("DATA", "Loans and advances to banks", {"FY2025": 60.2, "FY2024": 47.1, "FY2023": 46.8, "FY2022": 77.8, "FY2021": 110.0, "FY2020": 178.3, "FY2019": 143.6, "FY2018": 126.2, "FY2017": 166.4, "FY2016": 106.9, "FY2015": 95.9, "FY2014": 96.1}),
    ("DATA", "Loans and advances to customers", {"FY2015": 3.2, "FY2014": 0.4}),
    ("DATA", "Reverse repurchase agreements with banks", {"FY2025": 4055.8, "FY2024": 5131.0, "FY2023": 5841.9, "FY2022": 3854.3, "FY2021": 2107.5, "FY2020": 963.0, "FY2019": 2052.7, "FY2018": 2756.6, "FY2017": 4091.3, "FY2016": 3268.7, "FY2015": 11535.2, "FY2014": 24398.2},
     ),
    ("DATA", "Reverse repurchase agreements with customers", {"FY2025": 4587.1, "FY2024": 3059.6, "FY2023": 2303.5, "FY2022": 5417.0, "FY2021": 4288.6, "FY2020": 5895.2, "FY2019": 7204.8, "FY2018": 4636.4, "FY2017": 5106.9, "FY2016": 3176.7, "FY2015": 5083.7}),
    ("DATA", "Debt and other fixed income securities", {"FY2025": 5644.9, "FY2024": 5463.7, "FY2023": 5087.2, "FY2022": 4772.0, "FY2021": 4261.9, "FY2020": 4998.0, "FY2019": 5087.0, "FY2018": 5248.4, "FY2017": 4054.6, "FY2016": 5268.4, "FY2015": 4191.1, "FY2014": 3907.2}),
    ("DATA", "Equity shares", {"FY2025": 2.6, "FY2024": 4.3, "FY2023": 6.1, "FY2022": 3.5, "FY2021": 1.8, "FY2020": 1.6, "FY2019": 1.2, "FY2018": 1.3, "FY2017": 1.5, "FY2016": 1.0, "FY2015": 6.3}),
    ("DATA", "Derivative assets", {"FY2025": 8520.1, "FY2024": 9707.7, "FY2023": 13072.6, "FY2022": 6443.1, "FY2021": 6513.8, "FY2020": 11566.9, "FY2019": 4451.4, "FY2018": 2136.2, "FY2017": 1498.4, "FY2016": 424.0, "FY2015": 301.9, "FY2014": 204.7}),
    ("DATA", "Shares in group undertakings", {"FY2025": 17.6, "FY2024": 13.2, "FY2023": 9.9, "FY2022": 8.1, "FY2021": 6.8, "FY2020": 7.0, "FY2019": 8.6, "FY2018": 6.0, "FY2017": 5.8, "FY2016": 3.8, "FY2015": 3.6}),
    ("DATA", "Intangible assets", {"FY2025": 96.3, "FY2024": 76.7, "FY2023": 73.7, "FY2022": 66.2, "FY2021": 63.2, "FY2020": 67.8, "FY2019": 73.2, "FY2018": 66.0, "FY2017": 71.5, "FY2016": 61.6, "FY2015": 47.6}),
    ("DATA", "Tangible fixed assets", {"FY2025": 25.1, "FY2024": 27.1, "FY2023": 27.3, "FY2022": 29.0, "FY2021": 27.0, "FY2020": 27.9, "FY2019": 31.2, "FY2018": 31.1, "FY2017": 33.2, "FY2016": 28.4, "FY2015": 10.3, "FY2014": 12.7}),
    ("DATA", "Other assets", {"FY2025": 559.8, "FY2024": 897.9, "FY2023": 449.5, "FY2022": 832.2, "FY2021": 517.6, "FY2020": 659.1, "FY2019": 236.4, "FY2018": 210.9, "FY2017": 193.0, "FY2016": 752.2, "FY2015": 159.0, "FY2014": 217.7}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 229.9, "FY2024": 177.1, "FY2023": 90.0, "FY2022": 74.7, "FY2021": 82.7, "FY2020": 79.3, "FY2019": 90.7, "FY2018": 68.0, "FY2017": 60.1, "FY2016": 73.8, "FY2015": 49.7, "FY2014": 46.2}),
    ("TOTAL", "Total Assets", {"FY2025": 23914.9, "FY2024": 24933.9, "FY2023": 27378.9, "FY2022": 22058.9, "FY2021": 18208.4, "FY2020": 25045.1, "FY2019": 19384.1, "FY2018": 15517.3, "FY2017": 15395.2, "FY2016": 13192.8, "FY2015": 21487.5, "FY2014": 28883.2}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 678.7, "FY2024": 519.1, "FY2023": 292.1, "FY2022": 1153.3, "FY2021": 285.5, "FY2020": 471.6, "FY2019": 196.2, "FY2018": 398.0, "FY2017": 318.9, "FY2016": 613.1, "FY2015": 655.7, "FY2014": 744.1}),
    ("DATA", "Customer accounts", {"FY2025": 473.5, "FY2024": 707.5, "FY2023": 897.9, "FY2022": 295.7, "FY2021": 228.6, "FY2020": 909.7, "FY2019": 610.0, "FY2018": 337.8, "FY2017": 432.0, "FY2016": 310.2, "FY2015": 273.2, "FY2014": 294.0}),
    ("DATA", "Repurchase agreements with banks", {"FY2025": 4580.9, "FY2024": 3769.7, "FY2023": 1675.3, "FY2022": 1775.5, "FY2021": 1984.1, "FY2020": 1614.4, "FY2019": 1734.2, "FY2018": 1861.6, "FY2017": 2448.5, "FY2016": 2462.1, "FY2015": 3515.8, "FY2014": 23465.2}),
    ("DATA", "Repurchase agreements with customers", {"FY2025": 4078.0, "FY2024": 3425.7, "FY2023": 5231.3, "FY2022": 5799.8, "FY2021": 3133.7, "FY2020": 3638.8, "FY2019": 4572.0, "FY2018": 3301.7, "FY2017": 3779.3, "FY2016": 2992.4, "FY2015": 11966.0}),
    ("DATA", "Debt securities in issue", {"FY2025": 1292.3, "FY2024": 1395.0, "FY2023": 1616.5, "FY2022": 1760.1, "FY2021": 1851.6, "FY2020": 1776.6, "FY2019": 1453.2, "FY2018": 1773.3, "FY2017": 1387.9, "FY2016": 879.3, "FY2015": 1142.7, "FY2014": 976.6}),
    ("DATA", "Short trading positions", {"FY2025": 2889.1, "FY2024": 3925.7, "FY2023": 3418.7, "FY2022": 3560.9, "FY2021": 3072.9, "FY2020": 3728.3, "FY2019": 5208.7, "FY2018": 4561.1, "FY2017": 4297.7, "FY2016": 4570.4, "FY2015": 2892.2, "FY2014": 2600.9}),
    ("DATA", "Derivative liabilities", {"FY2025": 8548.4, "FY2024": 9603.3, "FY2023": 12833.5, "FY2022": 6422.7, "FY2021": 6481.2, "FY2020": 11514.0, "FY2019": 4285.1, "FY2018": 2030.6, "FY2017": 1433.1, "FY2016": 421.4, "FY2015": 250.9, "FY2014": 181.6}),
    ("DATA", "Other liabilities", {"FY2025": 365.8, "FY2024": 651.2, "FY2023": 581.4, "FY2022": 452.1, "FY2021": 225.3, "FY2020": 504.3, "FY2019": 380.7, "FY2018": 296.2, "FY2017": 357.3, "FY2016": 307.3, "FY2015": 257.2, "FY2014": 95.3}),
    ("DATA", "Accruals and deferred income", {"FY2025": 234.5, "FY2024": 212.9, "FY2023": 120.5, "FY2022": 123.3, "FY2021": 155.4, "FY2020": 139.0, "FY2019": 153.6, "FY2018": 137.8, "FY2017": 141.7, "FY2016": 116.2, "FY2015": 79.4, "FY2014": 69.6}),
    ("DATA", "Provisions for liabilities", {"FY2025": 0.2, "FY2024": 3.1, "FY2023": 4.0, "FY2022": 3.1, "FY2021": 3.3, "FY2020": 3.9, "FY2019": 4.9, "FY2018": 12.4, "FY2017": 17.2, "FY2016": 14.4, "FY2015": 12.8, "FY2014": 16.3}),
    ("DATA", "Subordinated liabilities", {"FY2021": 45.2, "FY2020": 45.3, "FY2019": 45.3, "FY2018": 45.2, "FY2017": 45.2, "FY2016": 45.2}),
    ("TOTAL", "Total Liabilities", {"FY2025": 23141.4, "FY2024": 24213.2, "FY2023": 26671.2, "FY2022": 21346.5, "FY2021": 17466.8, "FY2020": 24345.9, "FY2019": 18643.9, "FY2018": 14755.7, "FY2017": 14658.8, "FY2016": 12732.0, "FY2015": 21045.9, "FY2014": 28443.6}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 754.9, "FY2024": 709.9, "FY2023": 709.9, "FY2022": 709.9, "FY2021": 709.9, "FY2020": 709.9, "FY2019": 709.9, "FY2018": 709.9, "FY2017": 709.9, "FY2016": 2875.3, "FY2015": 2840.3, "FY2014": 2840.3}),
    ("DATA", "Share premium account", {"FY2025": 15.6, "FY2024": 15.6, "FY2023": 15.6, "FY2022": 15.6, "FY2021": 15.6, "FY2020": 15.6, "FY2019": 15.6, "FY2018": 15.6, "FY2017": 15.6, "FY2016": 15.6, "FY2015": 15.6, "FY2014": 15.6}),
    ("DATA", "Pension reserve", {"FY2025": -7.1, "FY2024": -6.8, "FY2023": -6.5, "FY2022": -6.2, "FY2021": -5.9, "FY2020": -5.9, "FY2019": -5.6, "FY2018": -3.7, "FY2017": -1.3, "FY2016": -16.8, "FY2015": -16.4}),
    ("DATA", "Other reserves", {"FY2025": -0.8, "FY2024": -0.6, "FY2023": -0.4, "FY2022": -0.5, "FY2021": -0.4}),
    ("DATA", "Profit and loss account", {"FY2025": 10.9, "FY2024": 2.6, "FY2023": -10.9, "FY2022": -6.4, "FY2021": 22.4, "FY2020": -20.4, "FY2019": 20.3, "FY2018": 39.8, "FY2017": 12.2, "FY2016": -2413.3, "FY2015": -2397.9, "FY2014": -2416.3}),
    ("TOTAL", "Total Equity", {"FY2025": 773.5, "FY2024": 720.7, "FY2023": 707.7, "FY2022": 712.4, "FY2021": 741.6, "FY2020": 699.2, "FY2019": 740.2, "FY2018": 761.6, "FY2017": 736.4, "FY2016": 460.8, "FY2015": 441.6, "FY2014": 439.6}),
    ("TOTAL", "Total Liabilities and Equity", {"FY2025": 23914.9, "FY2024": 24933.9, "FY2023": 27378.9, "FY2022": 22058.9, "FY2021": 18208.4, "FY2020": 25045.1, "FY2019": 19384.1, "FY2018": 15517.3, "FY2017": 15395.2, "FY2016": 13192.8, "FY2015": 21487.5, "FY2014": 28883.2}),
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
              "zero. £m.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=72,
    source_height=260,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 28.4, "FY2024": 33.3, "FY2023": 18.2, "FY2022": 7.5, "FY2021": 4.0, "FY2020": 3.1, "FY2019": 2.4, "FY2018": 1.4, "FY2017": 1.1, "FY2016": 0.6, "FY2015": 0.2, "FY2014": 0.5}),
    ("DATA", "Interest payable", {"FY2025": -105.7, "FY2024": -103.3, "FY2023": -38.7, "FY2022": -4.0, "FY2021": -5.4, "FY2020": -24.9, "FY2019": -19.7, "FY2018": -11.5, "FY2017": -11.9, "FY2016": -15.8, "FY2015": -21.8, "FY2014": -9.3}),
    ("TOTAL", "Net interest income/(expense)", {"FY2025": -77.3, "FY2024": -70.0, "FY2023": -20.5, "FY2022": 3.5, "FY2021": -1.4, "FY2020": -21.8, "FY2019": -17.3, "FY2018": -10.1, "FY2017": -10.8, "FY2016": -15.2, "FY2015": -21.6, "FY2014": -8.8}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 198.7, "FY2024": 178.8, "FY2023": 132.1, "FY2022": 175.6, "FY2021": 182.4, "FY2020": 128.2, "FY2019": 153.1, "FY2018": 148.9, "FY2017": 140.0, "FY2016": 133.8, "FY2015": 91.8, "FY2014": 71.3}),
    ("DATA", "Fees and commissions payable", {"FY2025": -76.0, "FY2024": -71.9, "FY2023": -53.4, "FY2022": -91.3, "FY2021": -99.5, "FY2020": -56.6, "FY2019": -73.9, "FY2018": -65.2, "FY2017": -58.1, "FY2016": -82.1, "FY2015": -43.5, "FY2014": -28.5}),
    ("TOTAL", "Net fees and commissions", {"FY2025": 122.7, "FY2024": 106.9, "FY2023": 78.7, "FY2022": 84.3, "FY2021": 82.9, "FY2020": 71.6, "FY2019": 79.2, "FY2018": 83.7, "FY2017": 81.9, "FY2016": 51.7, "FY2015": 48.3, "FY2014": 42.8}),
    ("DATA", "Dealing profit", {"FY2025": 175.1, "FY2024": 204.9, "FY2023": 130.7, "FY2022": 77.1, "FY2021": 183.1, "FY2020": 107.4, "FY2019": 112.3, "FY2018": 161.3, "FY2017": 144.5, "FY2016": 101.6, "FY2015": 97.5, "FY2014": 53.5}),
    ("DATA", "Other operating income", {"FY2025": 152.9, "FY2024": 2.3, "FY2023": 5.5, "FY2022": 1.4, "FY2021": 0.5, "FY2020": 0.3, "FY2019": 0.4, "FY2018": 0.1, "FY2017": 4.7, "FY2016": 7.5, "FY2015": 7.6, "FY2014": 0.1}),
    ("TOTAL", "Net income from operations", {"FY2025": 373.4, "FY2024": 244.1, "FY2023": 194.4, "FY2022": 166.3, "FY2021": 265.1, "FY2020": 157.5, "FY2019": 174.6, "FY2018": 235.0, "FY2017": 220.3, "FY2016": 145.6, "FY2015": 131.8, "FY2014": 87.6}),
    ("DATA", "Administrative expenses", {"FY2025": -338.6, "FY2024": -200.7, "FY2023": -178.3, "FY2022": -178.5, "FY2021": -192.0, "FY2020": -176.6, "FY2019": -177.4, "FY2018": -178.4, "FY2017": -174.8, "FY2016": -146.4, "FY2015": -124.0, "FY2014": -111.8}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -28.9, "FY2024": -29.3, "FY2023": -25.6, "FY2022": -25.4, "FY2021": -29.5, "FY2020": -31.6, "FY2019": -28.8, "FY2018": -26.6, "FY2017": -20.8, "FY2016": -12.8, "FY2015": -6.2, "FY2014": -4.4}),
    ("DATA", "Provisions for liabilities", {"FY2025": -0.1, "FY2024": 0.9, "FY2023": -0.9, "FY2021": 0.2, "FY2020": 0.6, "FY2019": 2.3, "FY2018": -0.2, "FY2017": -12.5, "FY2016": -1.8, "FY2015": 3.3, "FY2014": 0.6}),
    ("TOTAL", "Operating expenses", {"FY2025": -367.6, "FY2024": -229.1, "FY2023": -204.8, "FY2022": -203.9, "FY2021": -221.3, "FY2020": -207.6, "FY2019": -203.9, "FY2018": -205.2, "FY2017": -208.1, "FY2016": -161.0, "FY2015": -126.9, "FY2014": -115.6}),
    ("TOTAL", "Profit/(loss) on ordinary activities before taxation", {"FY2025": 5.8, "FY2024": 15.0, "FY2023": -10.4, "FY2022": -37.6, "FY2021": 43.8, "FY2020": -50.1, "FY2019": -29.3, "FY2018": 29.8, "FY2017": 12.2, "FY2016": -15.4, "FY2015": 4.9, "FY2014": -28.0}),
    ("DATA", "Tax credit/(charge) on profit/(loss) on ordinary activities", {"FY2025": 1.4, "FY2024": -1.5, "FY2023": 5.9, "FY2022": 8.8, "FY2021": -1.0, "FY2020": 9.4, "FY2019": 9.8, "FY2018": -2.2, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 7.2, "FY2024": 13.5, "FY2023": -4.5, "FY2022": -28.8, "FY2021": 42.8, "FY2020": -40.7, "FY2019": -19.5, "FY2018": 27.6, "FY2017": 12.2, "FY2016": -15.4, "FY2015": 4.9, "FY2014": -28.0}),
    ("SECTION", "Other comprehensive income/(loss)", {}),
    ("DATA", "Re-measurement losses from defined benefit scheme", {"FY2025": -0.3, "FY2024": -0.3, "FY2023": -0.3, "FY2022": -0.3, "FY2020": -0.3, "FY2019": -1.9, "FY2018": -2.4, "FY2017": -4.5, "FY2016": -0.4, "FY2015": -2.4, "FY2014": -2.5}),
    ("DATA", "FX translation gain/(loss) relating to net investment in subsidiary", {"FY2025": -0.2, "FY2024": -0.2, "FY2023": 0.1, "FY2022": -0.1, "FY2021": -0.4}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 6.7, "FY2024": 13.0, "FY2023": -4.7, "FY2022": -29.2, "FY2021": 42.4, "FY2020": -41.0, "FY2019": -21.4, "FY2018": 25.2, "FY2017": 7.7, "FY2016": -15.8, "FY2015": 2.5, "FY2014": -30.5}),
]
bw.add_income_statement_sheet(
    title="Mizuho International plc — Profit & Loss",
    subtitle="Consolidated Group basis for FY2019-FY2025; Company-only basis for FY2014-FY2018 (see the "
              "'REPORTING BASIS' source note). Re-measurement losses from defined benefit scheme were nil (not "
              "disclosed as a line) in FY2021; Provisions for liabilities was nil in FY2021 Company statement "
              "terms and is shown blank for FY2021 Consolidated as the report discloses no separate figure. "
              "FY2014-FY2020 did not disclose a separate FX translation line (shown blank, not zero). FY2014-"
              "FY2017 each disclosed a £nil tax charge/credit (shown here as 0, per each year's own source).",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=240,
    unit_suffix=" (£m)",
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
]
bw.add_equity_changes_sheet(
    title="Mizuho International plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest. Consolidated Group basis FY2019 onward; Company-only "
              "basis FY2014-FY2018 (see the 'REPORTING BASIS' source note). £m. Equity reconciliation ladder "
              "confirmed: every year's own closing balance ties exactly to both the next year's own opening "
              "balance and that year's own Balance Sheet Total Equity across all 12 years, with one disclosed "
              "exception: a real ~£0.5m break between FY2014's closing position as originally filed (UK GAAP, "
              "Companies House) and the FRS102-restated FY2015 opening position shown in the FY2016 Annual "
              "Report - the 'FRS 102 transition adjustment' row makes that break explicit rather than silently "
              "plugging it. FY2025's Capital injection/Equity contribution/Transfer-to-P&L rows relate to a "
              "capital raise and the release of a net dilapidation provision following termination of the "
              "Company's sub-lease, per the source's own explanatory note. The FY2017 'Share capital reduction' "
              "cancelled MHI's cumulative loss balance (135,000,000 JPY ordinary shares and £111,534,584 "
              "ordinary shares were cancelled per the source's own explanatory note).",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
)

bw.add_cash_flow_sheet(
    "Mizuho International plc — Consolidated Statement of Cash Flows",
    "Consolidated Group basis, £ millions. FY2014-FY2020 are blank (not zero): none of those years' Annual "
    "Reports include a cash flow statement, each invoking the FRS 1/FRS 102 exemption for a qualifying "
    "subsidiary whose ultimate parent (Mizuho Financial Group, Inc.) publishes consolidated financial "
    "statements including the Company - the same exemption basis as FY2021-FY2025's ENTITY NOTE.",
    ROWS, sources(), first_col_width=66, source_height=240, unit_suffix=" (£m)")

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
    ("DATA", "Credit quality step 1", {"FY2025": 158.3, "FY2024": 368.5, "FY2023": 403.5, "FY2022": 531.4, "FY2021": 303.7, "FY2020": 611.6, "FY2019": 8.5, "FY2018": 234.5, "FY2017": 114.1, "FY2016": 31.7, "FY2015": 5.3, "FY2014": 6.1}),
    ("DATA", "Credit quality step 2", {"FY2025": 102.2, "FY2024": 72.2, "FY2023": 57.5, "FY2022": 29.7, "FY2021": 31.3, "FY2020": 57.9, "FY2019": 108.9, "FY2018": 52.0, "FY2017": 128.4, "FY2016": 54.3, "FY2015": 69.7, "FY2014": 61.2}),
    ("DATA", "Credit quality step 3", {"FY2025": 0.0, "FY2024": 57.8, "FY2023": 56.2, "FY2022": 20.4, "FY2020": 0.0, "FY2019": 0.0, "FY2018": 0.0, "FY2016": 0.1}),
    ("DATA", "Credit quality step 4", {}),
    ("DATA", "Credit quality step 5", {"FY2025": 17.7, "FY2024": 13.2, "FY2023": 9.9, "FY2022": 8.1, "FY2021": 6.9, "FY2020": 7.2, "FY2019": 8.7, "FY2015": 3.7, "FY2014": 3.2}),
    ("DATA", "Credit quality step 6", {"FY2025": 1.1, "FY2024": 4.0, "FY2023": 3.9, "FY2022": 2.5, "FY2021": 1.7, "FY2020": 1.6, "FY2019": 1.1, "FY2018": 6.8, "FY2017": 0.8, "FY2016": 0.6}),
    ("DATA", "Unrated", {"FY2025": 96.5, "FY2024": 70.1, "FY2023": 78.4, "FY2022": 70.5, "FY2021": 64.7, "FY2020": 64.7, "FY2019": 55.9, "FY2018": 81.1, "FY2017": 90.7, "FY2016": 89.3, "FY2015": 96.1, "FY2014": 48.9}),
    ("TOTAL", "Total net credit exposure", {"FY2025": 375.8, "FY2024": 585.7, "FY2023": 609.5, "FY2022": 662.7, "FY2021": 408.2, "FY2020": 743.0, "FY2019": 183.1, "FY2018": 374.5, "FY2017": 334.0, "FY2016": 175.9, "FY2015": 174.8, "FY2014": 119.4}),
    ("DATA", "Memo: Total gross credit exposure (before CRM)", {"FY2025": 420.8, "FY2024": 665.7, "FY2023": 681.1, "FY2022": 725.0, "FY2021": 437.9, "FY2020": 834.2, "FY2019": 257.9, "FY2018": 405.5, "FY2017": 401.6, "FY2016": 228.7, "FY2015": 174.8, "FY2014": 119.4}),
    ("DATA", "Credit risk RWAs (excluding CCR)", {"FY2025": 150.5, "FY2024": 148.4, "FY2023": 140.1, "FY2022": 108.2, "FY2021": 92.8, "FY2020": 85.9, "FY2019": 88.0, "FY2018": 98.7, "FY2017": 117.7, "FY2016": 101.1, "FY2015": 118.5, "FY2014": 64.3}),
    ("DATA", "Credit risk RWA density (RWAs / net credit exposure)", {"FY2025": "40.05%", "FY2024": "25.34%", "FY2023": "22.99%", "FY2022": "16.33%", "FY2021": "22.73%", "FY2020": "11.56%", "FY2019": "48.06%", "FY2018": "26.36%", "FY2017": "35.24%", "FY2016": "57.48%", "FY2015": "67.79%", "FY2014": "53.87%"}),
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

def metric(name, unit, values, note=None):
    bw.add_metric_sheet(name, unit, [(name, values)], p3_sources(), note=note, first_col_width=48, source_height=220)

metric("CET1 Capital", "£ millions", {"FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8, "FY2021": 675.6, "FY2020": 623.7, "FY2019": 662.5, "FY2018": 690.9, "FY2017": 658.3, "FY2016": 408.3, "FY2015": 451.9, "FY2014": 456.9}, "FY2025 Annual Report states regulatory capital consists solely of Tier 1 capital; treated as CET1 for this metric because no Tier 2 capital is reported. FY2014-FY2016 capital resources consisted solely of common equity Tier 1 (no Tier 2 issued yet); FY2014-FY2016 are MSUKH group-level figures, not MHI-level (see the P3 source dict comment).")
metric("CET1 Ratio", "%", {"FY2025": "20.0%", "FY2024": "22.8%", "FY2023": "28.0%", "FY2022": "31.14%", "FY2021": "31.12%", "FY2020": "20.02%", "FY2019": "27.8%", "FY2018": "30.6%", "FY2017": "32.9%", "FY2016": "36.4%", "FY2015": "49.5%", "FY2014": "50.3%"})
metric("Tier 1 Capital", "£ millions", {"FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8, "FY2021": 675.6, "FY2020": 623.7, "FY2019": 662.5, "FY2018": 690.9, "FY2017": 658.3, "FY2016": 408.3, "FY2015": 451.9, "FY2014": 456.9})
metric("Tier 1 Ratio", "%", {"FY2025": "20.0%", "FY2024": "22.84%", "FY2023": "28.00%", "FY2022": "31.14%", "FY2021": "31.12%", "FY2020": "20.02%", "FY2019": "27.8%", "FY2018": "30.6%", "FY2017": "32.9%", "FY2016": "36.4%", "FY2015": "49.5%", "FY2014": "50.3%"})
metric("Total Capital", "£ millions", {"FY2025": 670.5, "FY2024": 637.4, "FY2023": 627.7, "FY2022": 640.8, "FY2021": 711.6, "FY2020": 668.7, "FY2019": 707.5, "FY2018": 735.9, "FY2017": 703.3, "FY2016": 453.3, "FY2015": 451.9, "FY2014": 456.9}, "FY2015/FY2014: Total capital equals Tier 1 capital because no Tier 2 capital had yet been issued (first appears FY2016).")
metric("Total Capital Ratio", "%", {"FY2025": "20.0%", "FY2024": "22.84%", "FY2023": "28.00%", "FY2022": "31.14%", "FY2021": "32.78%", "FY2020": "21.46%", "FY2019": "29.7%", "FY2018": "32.6%", "FY2017": "35.1%", "FY2016": "40.4%", "FY2015": "49.5%", "FY2014": "50.3%"})
metric("Total RWAs", "£ millions", {"FY2025": 3353.2, "FY2024": 2790.7, "FY2023": 2241.7, "FY2022": 2057.9, "FY2021": 2171.0, "FY2020": 3115.3, "FY2019": 2385.8, "FY2018": 2257.0, "FY2017": 2002.2, "FY2016": 1122.3, "FY2015": 913.7, "FY2014": 908.5})

# RWA Breakdown - Pillar 3 UK OV1 template, placed right after Total RWAs
# per the locked sheet order. All 5 available years tie exactly to the
# Total RWAs figure above (each year's own disclosed Total row used
# directly, not a recomputed sum - individual risk-type rows carry £0.1-
# 0.2m source rounding artifacts against that Total, consistent with the
# pattern seen across other banks in this rollout).
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 150.5, "FY2024": 148.4, "FY2023": 140.1, "FY2022": 108.2, "FY2021": 92.8, "FY2020": 85.9, "FY2019": 88.0, "FY2018": 98.7, "FY2017": 117.7, "FY2016": 101.1, "FY2015": 118.5, "FY2014": 64.3}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 682.4, "FY2024": 638.9, "FY2023": 530.6, "FY2022": 357.3, "FY2021": 259.6, "FY2020": 232.8, "FY2019": 181.4, "FY2018": 182.3, "FY2017": 184.5, "FY2016": 134.0, "FY2015": 91.6, "FY2014": 123.8}),
    ("DATA", "Concentration risk", {"FY2016": 0.0, "FY2015": 34.4}),
    ("DATA", "Settlement risk", {"FY2025": 0.0, "FY2024": 0.2, "FY2023": 0.1, "FY2022": 0.2, "FY2021": 0.1}),
    ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2025": 2014.2, "FY2024": 1626.8, "FY2023": 1166.8, "FY2022": 1224.3, "FY2021": 1445.4, "FY2020": 2442.2, "FY2019": 1722.7, "FY2018": 1598.7, "FY2017": 1393.4, "FY2016": 659.7, "FY2015": 552.0, "FY2014": 633.3}),
    ("DATA", "Large exposures", {"FY2023": 14.6}),
    ("DATA", "Operational risk", {"FY2025": 506.1, "FY2024": 376.6, "FY2023": 389.6, "FY2022": 368.1, "FY2021": 373.3, "FY2020": 354.4, "FY2019": 393.6, "FY2018": 377.3, "FY2017": 306.7, "FY2016": 235.1, "FY2015": 117.1, "FY2014": 87.1}),
    ("TOTAL", "Total", {"FY2025": 3353.2, "FY2024": 2790.7, "FY2023": 2241.7, "FY2022": 2057.9, "FY2021": 2171.0, "FY2020": 3115.3, "FY2019": 2385.8, "FY2018": 2257.0, "FY2017": 2002.2, "FY2016": 1122.3, "FY2015": 913.7, "FY2014": 908.5}),
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
metric("Leverage Ratio", "%", {"FY2025": "4.2%", "FY2024": "4.07%", "FY2023": "4.24%", "FY2022": "4.07%", "FY2021": "4.75%", "FY2020": "3.74%", "FY2019": "3.74%", "FY2018": "4.50%", "FY2017": "4.36%", "FY2016": "3.28%", "FY2015": "1.87%"}, "FY2014 leverage ratio was discussed qualitatively (implementation of PRA bank-level reporting was noted as having 'commenced') but no computed ratio was numerically disclosed in the FY2014 Pillar 3 document.")
metric("LCR", "%", {"FY2025": "268.7%", "FY2024": "250.39%", "FY2023": "302.67%", "FY2022": "364.04%", "FY2021": "303.00%", "FY2020": "340%", "FY2019": "416%", "FY2018": "396%"}, "LCR was first disclosed in the FY2018 Pillar 3 document (the document itself states this); not disclosed FY2014-FY2017.")
metric("NSFR", "%", {"FY2025": "122.5%", "FY2024": "128.67%", "FY2023": "140.66%", "FY2022": "177.71%"}, "NSFR was not disclosed in the 2021 report or any FY2014-FY2020 report; 2025 is from the Annual Report KPI section.")
metric("MREL Ratio", "%", {}, "MREL ratio was not numerically disclosed in any FY2014-FY2025 official annual/Pillar 3 report checked.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total Assets", {"FY2025": 23914.9, "FY2024": 24933.9, "FY2023": 27378.9, "FY2022": 22058.9, "FY2021": 18208.4, "FY2020": 25045.1, "FY2019": 19384.1, "FY2018": 15517.3, "FY2017": 15395.2, "FY2016": 13192.8, "FY2015": 21487.5, "FY2014": 28883.2}),
        ("Reverse repurchase agreements with customers", {"FY2025": 4587.1, "FY2024": 3059.6, "FY2023": 2303.5, "FY2022": 5417.0, "FY2021": 4288.6, "FY2020": 5895.2, "FY2019": 7204.8, "FY2018": 4636.4, "FY2017": 5106.9, "FY2016": 3176.7, "FY2015": 5083.7}),
        ("Derivative assets", {"FY2025": 8520.1, "FY2024": 9707.7, "FY2023": 13072.6, "FY2022": 6443.1, "FY2021": 6513.8, "FY2020": 11566.9, "FY2019": 4451.4, "FY2018": 2136.2, "FY2017": 1498.4, "FY2016": 424.0, "FY2015": 301.9, "FY2014": 204.7}),
        ("Total Equity", {"FY2025": 773.5, "FY2024": 720.7, "FY2023": 707.7, "FY2022": 712.4, "FY2021": 741.6, "FY2020": 699.2, "FY2019": 740.2, "FY2018": 761.6, "FY2017": 736.4, "FY2016": 460.8, "FY2015": 441.6, "FY2014": 439.6}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Net income from operations", {"FY2025": 373.4, "FY2024": 244.1, "FY2023": 194.4, "FY2022": 166.3, "FY2021": 265.1, "FY2020": 157.5, "FY2019": 174.6, "FY2018": 235.0, "FY2017": 220.3, "FY2016": 145.6, "FY2015": 131.8, "FY2014": 87.6}),
        ("Operating expenses", {"FY2025": -367.6, "FY2024": -229.1, "FY2023": -204.8, "FY2022": -203.9, "FY2021": -221.3, "FY2020": -207.6, "FY2019": -203.9, "FY2018": -205.2, "FY2017": -208.1, "FY2016": -161.0, "FY2015": -126.9, "FY2014": -115.6}),
        ("Profit/(loss) for the year", {"FY2025": 7.2, "FY2024": 13.5, "FY2023": -4.5, "FY2022": -28.8, "FY2021": 42.8, "FY2020": -40.7, "FY2019": -19.5, "FY2018": 27.6, "FY2017": 12.2, "FY2016": -15.4, "FY2015": 4.9, "FY2014": -28.0}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 720.7, "FY2024": 707.7, "FY2023": 712.4, "FY2022": 741.6, "FY2021": 699.2, "FY2020": 740.2, "FY2019": 761.6, "FY2018": 736.4, "FY2017": 460.8, "FY2016": 441.6, "FY2015": 439.1, "FY2014": 425.1}),
        ("Profit/(loss) for the year", {"FY2025": 7.2, "FY2024": 13.5, "FY2023": -4.5, "FY2022": -28.8, "FY2021": 42.8, "FY2020": -40.7, "FY2019": -19.5, "FY2018": 27.6, "FY2017": 12.2, "FY2016": -15.4, "FY2015": 4.9, "FY2014": -28.0}),
        ("Other equity movements, net", {"FY2025": 45.6, "FY2024": -0.5, "FY2023": -0.2, "FY2022": -0.4, "FY2021": -0.4, "FY2020": -0.3, "FY2019": -1.9, "FY2018": -2.4, "FY2017": 263.4, "FY2016": 34.6, "FY2015": -2.4, "FY2014": 42.5}),
        ("Closing equity", {"FY2025": 773.5, "FY2024": 720.7, "FY2023": 707.7, "FY2022": 712.4, "FY2021": 741.6, "FY2020": 699.2, "FY2019": 740.2, "FY2018": 761.6, "FY2017": 736.4, "FY2016": 460.8, "FY2015": 441.6, "FY2014": 439.6}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[("Net cash flow from operating activities", CF["Net cash flows from operating activities"]), ("Net cash flows used in investing activities", CF["Net cash flows used in investing activities"]), ("Cash and cash equivalents at end of period", CF["Cash and cash equivalents at the end of the period"])],
    cash_flow_unit="£m",
    ratios=[("CET1 Ratio", {"FY2025": "20.0%", "FY2024": "22.8%", "FY2023": "28.0%", "FY2022": "31.14%", "FY2021": "31.12%", "FY2020": "20.02%", "FY2019": "27.8%", "FY2018": "30.6%", "FY2017": "32.9%", "FY2016": "36.4%", "FY2015": "49.5%", "FY2014": "50.3%"}), ("Leverage Ratio", {"FY2025": "4.2%", "FY2024": "4.07%", "FY2023": "4.24%", "FY2022": "4.07%", "FY2021": "4.75%", "FY2020": "3.74%", "FY2019": "3.74%", "FY2018": "4.50%", "FY2017": "4.36%", "FY2016": "3.28%", "FY2015": "1.87%"})],
    note="Annual data; Consolidated Group basis FY2019-FY2025, Company-only basis FY2014-FY2018 (see the Balance Sheet sheet's REPORTING BASIS note). Cash flow totals are blank for FY2014-FY2020 (no cash flow statement prepared those years).",
)

bw.save("/Users/armaan/code/katalysis/banks/MIZUHO INTERNATIONAL FINANCIALS.xlsx")
