import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022"]  # most recent first

AR26_URL = "https://find-and-update.company-information.service.gov.uk/company/00489604/filing-history/MzUzMDk3ODM1OWFkaXF6a2N4/document?format=pdf&download=0"
AR25_URL = "https://find-and-update.company-information.service.gov.uk/company/00489604/filing-history/MzQ3NDQ1NjE4M2FkaXF6a2N4/document?format=pdf&download=0"
AR23_URL = "https://find-and-update.company-information.service.gov.uk/company/00489604/filing-history/MzM5NTY4ODE2OWFkaXF6a2N4/document?format=pdf&download=0"

INTERIM_2025_URL = "https://www.investec.com/content/dam/investor-relations/basel-pillar-iii-regulatory-disclosures/2025/Investec-plc-group-and-Investec-Bank-plc-Pillar-3-disclosure-report-30-Sept-2025.pdf"
INTERIM_2024_URL = "https://www.investec.com/content/dam/investor-relations/basel-pillar-iii-regulatory-disclosures/2024/Investec-plc-Group-and-Investec-Bank-plc-Pillar-3-disclosure-report-30-Sept-2024.pdf"
INTERIM_2023_URL = "https://www.investec.com/content/dam/investor-relations/basel-pillar-iii-regulatory-disclosures/united-kingdom/2023/Investec-plc-group-and-Investec-Bank-plc-Pillar-3-disclosure-report%20-30-Sept-2023.pdf"
INTERIM_2022_URL = "https://www.investec.com/content/dam/investor-relations/financial-information/group-financial-results/2022/Investec-plc-group-Interim-Pillar-3-disclosure-report-30-September-2022.pdf"

# Standalone year-end (31 March) "Pillar 3 annual disclosure report" — a distinct
# document from the semi-annual (30 Sept) reports above, each containing Table 44
# "Key metrics (UK KM1)" as IBP's own Appendix A entity-level disclosure (signed by
# the IBP Finance Director / IBP Risk Officer). Retrieved this session via a
# Chrome-UA curl fetch against investec.com (the plain-curl/default-UA 403 the
# earlier session hit does not apply to these content/dam PDF paths).
ANNUAL_P3_2026_URL = "https://www.investec.com/content/dam/investor-relations/financial-information/group-financial-results/2026/Investec-plc-group-and-Investec-Bank-plc-Pillar-3-disclosure-report-March-2026.pdf"
ANNUAL_P3_2025_URL = "https://www.investec.com/content/dam/investor-relations/financial-information/group-financial-results/2025/Investec-plc-group-and-Investec-Bank-plc-Pillar-3-disclosure-report-March-2025.pdf"
ANNUAL_P3_2024_URL = "https://www.investec.com/content/dam/investor-relations/financial-information/group-financial-results/2024/Investec-plc-group-and-Investec-Bank-plc-Pillar-3-disclosure-report-March-2024.pdf"

CASH_FLOW_SOURCES = (
    "Sources — all figures are Investec Bank plc Group consolidated cash flow statement, £'000:\n"
    f"FY2026 & FY2025: Investec Bank plc Annual Financial Statements 2026, p.127 (Cash flow statements) — {AR26_URL}\n"
    f"FY2024: Investec Bank plc Annual Financial Statements 2025, p.123 (Cash flow statements) — {AR25_URL}\n"
    f"FY2023 & FY2022: Investec Bank plc Annual Financial Statements 2023, p.123 (Cash flow statements) — {AR23_URL}\n"
    "Note: these are Companies House filing copies (scanned/image-only PDFs — no text layer; transcribed via "
    "page-render + manual reading). Investec's own investor-relations site returned HTTP 403 to automated fetches "
    "throughout, and no Wayback Machine snapshot of the relevant IR pages was found, so Companies House was the "
    "only available source this session. Presentation granularity changed across report vintages: FY2026 itemises "
    "'acquisition of associates and joint venture holdings' / 'disposal of associate' as separate investing lines "
    "(FY2023-FY2022 net these into a single 'net disposal/(acquisition) of associates and joint venture holdings' "
    "line); FY2026 financing activities are funded via subordinated debt issuance/redemption where FY2025/FY2024 "
    "used Additional Tier 1 Securities issuance/redemption instead. Blank cells indicate that year's report did not "
    "disclose that specific line; where a value was disclosed as nil ('—') it is shown as 0. Section totals (net "
    "cash from operating/investing/financing activities, cash and cash equivalents) are consistent and reconcile "
    "exactly year-to-year across all 5 years (each year's opening cash balance ties to the prior year's closing "
    "balance)."
)

def p3_sources(page_26=None, page_25=None, page_23=None, label=""):
    return (
        f"Sources — Investec Bank plc (IBP) solo-entity capital adequacy disclosures{(' — ' + label) if label else ''}:\n"
        f"FY2026 & FY2025: Investec Bank plc Annual Financial Statements 2026, p.{page_26} (Notes to risk and capital "
        f"management — Capital management and allocation) — {AR26_URL}\n"
        f"FY2024: Investec Bank plc Annual Financial Statements 2025, p.{page_25} (Notes to risk and capital "
        f"management — Capital management and allocation) — {AR25_URL}\n"
        f"FY2023 & FY2022: Investec Bank plc Annual Financial Statements 2023, p.{page_23} (Notes to risk and "
        f"capital management — Capital management and allocation) — {AR23_URL}\n"
        "Ratios/RWAs include the deduction of foreseeable charges and dividends when calculating CET1 capital, per "
        "IBP's own disclosure basis (differs slightly from the Investec Group's year-end results booklet, which "
        "excludes this deduction). Figures for FY2025 and earlier are calculated applying IFRS 9 transitional "
        "arrangements; these ceased to apply from 1 April 2025, so FY2026 figures are presented on a fully-loaded "
        "basis (not directly comparable to the transitional-basis prior years on a like-for-like footing, though "
        "both bases are shown as disclosed each year)."
    )


# Entity-level interim disclosures.  The September reports include the prior
# March comparative in the same Appendix A table, so each source URL is the
# official report containing both observations.
INTERIM_ROWS = [
    ("30 September 2025", "Semi-annual Pillar 3", "CET1 capital", 2119, "£m", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 1"),
    ("30 September 2025", "Semi-annual Pillar 3", "Tier 1 capital", 2469, "£m", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 2"),
    ("30 September 2025", "Semi-annual Pillar 3", "Total capital", 3166, "£m", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 3"),
    ("30 September 2025", "Semi-annual Pillar 3", "Total RWAs", 15946, "£m", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 4"),
    ("30 September 2025", "Semi-annual Pillar 3", "CET1 ratio", "13.3%", "%", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 5"),
    ("30 September 2025", "Semi-annual Pillar 3", "Tier 1 ratio", "15.5%", "%", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 6"),
    ("30 September 2025", "Semi-annual Pillar 3", "Total capital ratio", "19.9%", "%", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 7"),
    ("30 September 2025", "Semi-annual Pillar 3", "Leverage exposure measure", 23508, "£m", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 13"),
    ("30 September 2025", "Semi-annual Pillar 3", "Leverage ratio", "10.5%", "%", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 14"),
    ("30 September 2025", "Semi-annual Pillar 3", "LCR", "425%", "% (12-month average)", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.44, UK KM1 row 17"),
    ("30 September 2025", "Semi-annual Pillar 3", "NSFR", "144%", "%", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.44, UK KM1 row 20"),
    ("31 March 2025", "Semi-annual Pillar 3 comparative", "CET1 capital", 2006, "£m", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 1 comparative"),
    ("31 March 2025", "Semi-annual Pillar 3 comparative", "Tier 1 capital", 2356, "£m", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 2 comparative"),
    ("31 March 2025", "Semi-annual Pillar 3 comparative", "Total capital", 3051, "£m", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 3 comparative"),
    ("31 March 2025", "Semi-annual Pillar 3 comparative", "Total RWAs", 15234, "£m", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 4 comparative"),
    ("31 March 2025", "Semi-annual Pillar 3 comparative", "CET1 ratio", "13.2%", "%", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 5 comparative"),
    ("31 March 2025", "Semi-annual Pillar 3 comparative", "Tier 1 ratio", "15.5%", "%", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 6 comparative"),
    ("31 March 2025", "Semi-annual Pillar 3 comparative", "Total capital ratio", "20.0%", "%", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 7 comparative"),
    ("31 March 2025", "Semi-annual Pillar 3 comparative", "Leverage exposure measure", 22173, "£m", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 13 comparative"),
    ("31 March 2025", "Semi-annual Pillar 3 comparative", "Leverage ratio", "10.6%", "%", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.43, UK KM1 row 14 comparative"),
    ("31 March 2025", "Semi-annual Pillar 3 comparative", "LCR", "465%", "% (12-month average)", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.44, UK KM1 row 17 comparative"),
    ("31 March 2025", "Semi-annual Pillar 3 comparative", "NSFR", "145%", "%", "Investec Bank plc solo-consolidated", INTERIM_2025_URL, "p.44, UK KM1 row 20 comparative"),
    ("30 September 2024", "Semi-annual Pillar 3", "CET1 capital", 1940, "£m", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 1"),
    ("30 September 2024", "Semi-annual Pillar 3", "Tier 1 capital", 2399, "£m", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 2"),
    ("30 September 2024", "Semi-annual Pillar 3", "Total capital", 3094, "£m", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 3"),
    ("30 September 2024", "Semi-annual Pillar 3", "Total RWAs", 15035, "£m", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 4"),
    ("30 September 2024", "Semi-annual Pillar 3", "CET1 ratio", "12.9%", "%", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 5"),
    ("30 September 2024", "Semi-annual Pillar 3", "Tier 1 ratio", "16.0%", "%", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 6"),
    ("30 September 2024", "Semi-annual Pillar 3", "Total capital ratio", "20.6%", "%", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 7"),
    ("30 September 2024", "Semi-annual Pillar 3", "Leverage exposure measure", 22760, "£m", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 13"),
    ("30 September 2024", "Semi-annual Pillar 3", "Leverage ratio", "10.5%", "%", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 14"),
    ("30 September 2024", "Semi-annual Pillar 3", "LCR", "464%", "% (12-month average)", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.44, UK KM1 row 17"),
    ("30 September 2024", "Semi-annual Pillar 3", "NSFR", "141%", "%", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.44, UK KM1 row 20"),
    ("31 March 2024", "Semi-annual Pillar 3 comparative", "CET1 capital", 1880, "£m", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 1 comparative"),
    ("31 March 2024", "Semi-annual Pillar 3 comparative", "Tier 1 capital", 2338, "£m", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 2 comparative"),
    ("31 March 2024", "Semi-annual Pillar 3 comparative", "Total capital", 3033, "£m", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 3 comparative"),
    ("31 March 2024", "Semi-annual Pillar 3 comparative", "Total RWAs", 14888, "£m", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 4 comparative"),
    ("31 March 2024", "Semi-annual Pillar 3 comparative", "CET1 ratio", "12.6%", "%", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 5 comparative"),
    ("31 March 2024", "Semi-annual Pillar 3 comparative", "Tier 1 ratio", "15.7%", "%", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 6 comparative"),
    ("31 March 2024", "Semi-annual Pillar 3 comparative", "Total capital ratio", "20.4%", "%", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 7 comparative"),
    ("31 March 2024", "Semi-annual Pillar 3 comparative", "Leverage exposure measure", 21281, "£m", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 13 comparative"),
    ("31 March 2024", "Semi-annual Pillar 3 comparative", "Leverage ratio", "11.0%", "%", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.43, UK KM1 row 14 comparative"),
    ("31 March 2024", "Semi-annual Pillar 3 comparative", "LCR", "446%", "% (12-month average)", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.44, UK KM1 row 17 comparative"),
    ("31 March 2024", "Semi-annual Pillar 3 comparative", "NSFR", "138%", "%", "Investec Bank plc solo-consolidated", INTERIM_2024_URL, "p.44, UK KM1 row 20 comparative"),
    ("30 September 2023", "Semi-annual Pillar 3", "CET1 capital", 1822, "£m", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 1"),
    ("30 September 2023", "Semi-annual Pillar 3", "Tier 1 capital", 2072, "£m", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 2"),
    ("30 September 2023", "Semi-annual Pillar 3", "Total capital", 2767, "£m", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 3"),
    ("30 September 2023", "Semi-annual Pillar 3", "Total RWAs", 14411, "£m", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 4"),
    ("30 September 2023", "Semi-annual Pillar 3", "CET1 ratio", "12.6%", "%", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 5"),
    ("30 September 2023", "Semi-annual Pillar 3", "Tier 1 ratio", "14.4%", "%", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 6"),
    ("30 September 2023", "Semi-annual Pillar 3", "Total capital ratio", "19.2%", "%", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 7"),
    ("30 September 2023", "Semi-annual Pillar 3", "Leverage exposure measure", 21875, "£m", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 13"),
    ("30 September 2023", "Semi-annual Pillar 3", "Leverage ratio", "9.5%", "%", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 14"),
    ("30 September 2023", "Semi-annual Pillar 3", "LCR", "439%", "% (12-month average)", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.44, UK KM1 row 17"),
    ("30 September 2023", "Semi-annual Pillar 3", "NSFR", "138%", "%", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.44, UK KM1 row 20"),
    ("31 March 2023", "Semi-annual Pillar 3 comparative", "CET1 capital", 1764, "£m", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 1 comparative"),
    ("31 March 2023", "Semi-annual Pillar 3 comparative", "Tier 1 capital", 2014, "£m", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 2 comparative"),
    ("31 March 2023", "Semi-annual Pillar 3 comparative", "Total capital", 2778, "£m", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 3 comparative"),
    ("31 March 2023", "Semi-annual Pillar 3 comparative", "Total RWAs", 14087, "£m", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 4 comparative"),
    ("31 March 2023", "Semi-annual Pillar 3 comparative", "CET1 ratio", "12.5%", "%", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 5 comparative"),
    ("31 March 2023", "Semi-annual Pillar 3 comparative", "Tier 1 ratio", "14.3%", "%", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 6 comparative"),
    ("31 March 2023", "Semi-annual Pillar 3 comparative", "Total capital ratio", "19.7%", "%", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 7 comparative"),
    ("31 March 2023", "Semi-annual Pillar 3 comparative", "Leverage exposure measure", 20218, "£m", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 13 comparative"),
    ("31 March 2023", "Semi-annual Pillar 3 comparative", "Leverage ratio", "10.0%", "%", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.43, UK KM1 row 14 comparative"),
    ("31 March 2023", "Semi-annual Pillar 3 comparative", "LCR", "431%", "% (12-month average)", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.44, UK KM1 row 17 comparative"),
    ("31 March 2023", "Semi-annual Pillar 3 comparative", "NSFR", "136%", "%", "Investec Bank plc solo-consolidated", INTERIM_2023_URL, "p.44, UK KM1 row 20 comparative"),
]

for missing_period in ("30 September 2022", "30 September 2021"):
    for metric_name, unit in (
        ("CET1 capital", "£m"), ("Tier 1 capital", "£m"), ("Total capital", "£m"),
        ("Total RWAs", "£m"), ("CET1 ratio", "%"), ("Tier 1 ratio", "%"),
        ("Total capital ratio", "%"), ("Leverage exposure measure", "£m"),
        ("Leverage ratio", "%"), ("LCR", "%"), ("NSFR", "%"),
    ):
        INTERIM_ROWS.append((missing_period, "Semi-annual Pillar 3 (not published)", metric_name,
                             "Not publicly disclosed", unit, "Investec Bank plc solo-consolidated",
                             INTERIM_2022_URL, "p.5, policy statement: significant subsidiary disclosures annual"))

bw = BankWorkbook(bank_name="Investec Bank plc", years=YEARS, header_color="1B3B6F")

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
BS_SOURCES = (
    "Sources — all figures are Investec Bank plc Group consolidated balance sheet, £'000 (converted from the "
    "source documents' £'million):\n"
    f"FY2026 & FY2025: Investec Bank plc Annual Financial Statements 2026, p.125 (Balance sheets, Group) — {AR26_URL}\n"
    f"FY2024: Investec Bank plc Annual Financial Statements 2025, p.121 (Balance sheets, Group, 31 March 2024 "
    f"comparative — restated per note 57 for the Investec Wealth & Investment UK discontinued-operations "
    f"classification; no FY2024 own-year Annual Report was available this session, so this restated comparative "
    f"is the only source) — {AR25_URL}\n"
    f"FY2023 & FY2022: Investec Bank plc Annual Financial Statements 2023, p.121 (Balance sheets, Group) — {AR23_URL}\n"
    "Note: these are Companies House filing copies (scanned/image-only PDFs). Capital reserve was fully released "
    "to retained income during FY2025 (nil FY2026/FY2025); Deferred taxation assets and the 'Fair value adjustment "
    "for asset/liability portfolio hedged risk' lines only appear from FY2026 (new hedge accounting designation); "
    "Other securitised assets / Liabilities arising on securitisation of other assets only appear FY2022-FY2024. "
    "All Total equity figures tie exactly to the Statement of Changes in Equity sheet's own closing balances."
)

bw.add_balance_sheet_sheet(
    title="Investec Bank plc — Consolidated Balance Sheet",
    subtitle="Investec Bank plc Group (consolidated basis), £'000",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances at central banks", {"FY2026": 3173756, "FY2025": 4191750, "FY2024": 5661623, "FY2023": 5400401, "FY2022": 5379994}),
        ("DATA", "Loans and advances to banks", {"FY2026": 800615, "FY2025": 859802, "FY2024": 676001, "FY2023": 892791, "FY2022": 1467039}),
        ("DATA", "Reverse repurchase agreements and cash collateral on securities borrowed", {"FY2026": 1884699, "FY2025": 1640765, "FY2024": 1140115, "FY2023": 1338699, "FY2022": 1447473}),
        ("DATA", "Sovereign debt securities", {"FY2026": 3688138, "FY2025": 2524702, "FY2024": 1928134, "FY2023": 1221744, "FY2022": 1165777}),
        ("DATA", "Bank debt securities", {"FY2026": 473920, "FY2025": 324179, "FY2024": 297255, "FY2023": 204691, "FY2022": 61714}),
        ("DATA", "Other debt securities", {"FY2026": 1117751, "FY2025": 770722, "FY2024": 708285, "FY2023": 697275, "FY2022": 437649}),
        ("DATA", "Derivative financial instruments", {"FY2026": 370494, "FY2025": 325886, "FY2024": 432395, "FY2023": 680262, "FY2022": 717457}),
        ("DATA", "Securities arising from trading activities", {"FY2026": 44723, "FY2025": 149912, "FY2024": 157332, "FY2023": 127537, "FY2022": 163165}),
        ("DATA", "Loans and advances to customers", {"FY2026": 17803653, "FY2025": 16813723, "FY2024": 16570313, "FY2023": 15567809, "FY2022": 14426475}),
        ("DATA", "Fair value adjustment for asset portfolio hedged risk", {"FY2026": -20507}),
        ("DATA", "Other loans and advances", {"FY2026": 141301, "FY2025": 162882, "FY2024": 145545, "FY2023": 172087, "FY2022": 147025}),
        ("DATA", "Other securitised assets", {"FY2024": 66702, "FY2023": 78231, "FY2022": 93087}),
        ("DATA", "Investment portfolio", {"FY2026": 202146, "FY2025": 211753, "FY2024": 244140, "FY2023": 311618, "FY2022": 333221}),
        ("DATA", "Interests in associated undertakings and joint venture holdings", {"FY2026": 851867, "FY2025": 832141, "FY2024": 791272, "FY2023": 10851, "FY2022": 11444}),
        ("DATA", "Current taxation assets", {"FY2026": 60322, "FY2025": 7016, "FY2024": 13254, "FY2023": 9890, "FY2022": 15727}),
        ("DATA", "Deferred taxation assets", {"FY2026": 72671, "FY2025": 120918, "FY2024": 119730, "FY2023": 111513, "FY2022": 109542}),
        ("DATA", "Other assets", {"FY2026": 934758, "FY2025": 677318, "FY2024": 750347, "FY2023": 993385, "FY2022": 1161549}),
        ("DATA", "Property and equipment", {"FY2026": 149630, "FY2025": 58940, "FY2024": 72947, "FY2023": 121014, "FY2022": 155055}),
        ("DATA", "Goodwill", {"FY2026": 65113, "FY2025": 56934, "FY2024": 58082, "FY2023": 249503, "FY2022": 244072}),
        ("DATA", "Software", {"FY2026": 12458, "FY2025": 4742, "FY2024": 4571, "FY2023": 9415, "FY2022": 7066}),
        ("DATA", "Other acquired intangible assets", {"FY2023": 43887, "FY2022": 44145}),
        ("TOTAL", "Total assets", {"FY2026": 31827508, "FY2025": 29734085, "FY2024": 29838043, "FY2023": 28242603, "FY2022": 27588676}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits by banks", {"FY2026": 902677, "FY2025": 1477568, "FY2024": 2174305, "FY2023": 2172170, "FY2022": 2026573}),
        ("DATA", "Derivative financial instruments", {"FY2026": 419205, "FY2025": 274791, "FY2024": 409255, "FY2023": 704816, "FY2022": 863295}),
        ("DATA", "Other trading liabilities", {"FY2026": 19409, "FY2025": 16242, "FY2024": 18449, "FY2023": 28184, "FY2022": 42944}),
        ("DATA", "Repurchase agreements and cash collateral on securities lent", {"FY2026": 1065587, "FY2025": 178202, "FY2024": 85091, "FY2023": 139529, "FY2022": 154828}),
        ("DATA", "Customer accounts (deposits)", {"FY2026": 22534593, "FY2025": 21555444, "FY2024": 20851216, "FY2023": 19251399, "FY2022": 18616233}),
        ("DATA", "Fair value adjustment for liability portfolio hedged risk", {"FY2026": -10395}),
        ("DATA", "Debt securities in issue", {"FY2026": 1075112, "FY2025": 974371, "FY2024": 956887, "FY2023": 1140879, "FY2022": 1120841}),
        ("DATA", "Liabilities arising on securitisation of other assets", {"FY2024": 71751, "FY2023": 81609, "FY2022": 95885}),
        ("DATA", "Current taxation liabilities", {"FY2026": 9260, "FY2025": 9023, "FY2024": 8624, "FY2023": 4813, "FY2022": 2082}),
        ("DATA", "Other liabilities", {"FY2026": 1248340, "FY2025": 893546, "FY2024": 987437, "FY2023": 1198267, "FY2022": 1360071}),
        ("DATA", "Subordinated liabilities", {"FY2026": 697632, "FY2025": 682218, "FY2024": 668810, "FY2023": 731483, "FY2022": 758739}),
        ("TOTAL", "Total liabilities", {"FY2026": 27961420, "FY2025": 26061405, "FY2024": 26231825, "FY2023": 25453149, "FY2022": 25041491}),
        ("SECTION", "Equity", {}),
        ("DATA", "Ordinary share capital", {"FY2026": 1280550, "FY2025": 1280550, "FY2024": 1280550, "FY2023": 1280550, "FY2022": 1280550}),
        ("DATA", "Share premium", {"FY2026": 199538, "FY2025": 199538, "FY2024": 199538, "FY2023": 199538, "FY2022": 199538}),
        ("DATA", "Capital reserve", {"FY2024": 11274, "FY2023": 153177, "FY2022": 153177}),
        ("DATA", "Other reserves (fair value + cash flow hedge + FX translation)", {"FY2026": 162, "FY2025": 4674, "FY2024": 26524, "FY2023": 34814, "FY2022": 1667}),
        ("DATA", "Retained income", {"FY2026": 2034831, "FY2025": 1836722, "FY2024": 1627373, "FY2023": 870424, "FY2022": 661420}),
        ("TOTAL", "Shareholder's equity excluding non-controlling interests", {"FY2026": 3515081, "FY2025": 3321484, "FY2024": 3145259, "FY2023": 2538503, "FY2022": 2296352}),
        ("DATA", "Additional Tier 1 securities in issue", {"FY2026": 350000, "FY2025": 350000, "FY2024": 458108, "FY2023": 250000, "FY2022": 250000}),
        ("DATA", "Non-controlling interests in partially held subsidiaries", {"FY2026": 1007, "FY2025": 1196, "FY2024": 2851, "FY2023": 951, "FY2022": 833}),
        ("TOTAL", "Total equity", {"FY2026": 3866088, "FY2025": 3672680, "FY2024": 3606218, "FY2023": 2789454, "FY2022": 2547185}),
        ("TOTAL", "Total liabilities and equity", {"FY2026": 31827508, "FY2025": 29734085, "FY2024": 29838043, "FY2023": 28242603, "FY2022": 27588676}),
    ],
    sources_text=BS_SOURCES,
    first_col_width=72,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
PL_SOURCES = (
    "Sources — all figures are Investec Bank plc Group consolidated income statement, £'000 (converted from the "
    "source documents' £'million):\n"
    f"FY2026 & FY2025: Investec Bank plc Annual Financial Statements 2026, p.123-124 (Consolidated income "
    f"statement / Consolidated statement of total comprehensive income) — {AR26_URL}\n"
    f"FY2024: Investec Bank plc Annual Financial Statements 2025, p.119-120 (as the FY2025 report's own prior-"
    f"year comparative; no FY2024 own-year Annual Report was available this session) — {AR25_URL}\n"
    f"FY2023 & FY2022: Investec Bank plc Annual Financial Statements 2023, p.119-120 — {AR23_URL}\n"
    "Presentation structure genuinely changed across the 5 years, shown on each year's own basis rather than "
    "forced into one template: FY2023-FY2022 group operating income/expense under 'Operating profit before "
    "goodwill, acquired intangibles and strategic actions' with a separate 'Impairment of goodwill' line; "
    "FY2025-FY2026 instead group under 'Operating income'/'Operating income after expected credit loss "
    "impairment charges' with a 'Financial impact of strategic actions' line (no separate goodwill impairment "
    "line disclosed those years). FY2024 uniquely splits Profit after taxation into continuing vs discontinued "
    "operations (£395,600k discontinued - the Investec Wealth & Investment UK disposal); no other year has a "
    "discontinued-operations split. 'Share of post-taxation profit of associates and joint venture holdings' is "
    "shown as a single combined figure FY2023-FY2022 (no amortisation/integration-cost breakdown existed yet at "
    "that granularity). All 'Total comprehensive income' rows tie exactly to the Statement of Changes in Equity "
    "sheet's own 'Total comprehensive income for the year' rows."
)

bw.add_income_statement_sheet(
    title="Investec Bank plc — Consolidated Income Statement",
    subtitle="Investec Bank plc Group (consolidated basis), £'000",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest income", {"FY2026": 1735860, "FY2025": 1979851, "FY2024": 1933984, "FY2023": 1445322, "FY2022": 719538}),
        ("DATA", "Interest expense", {"FY2026": -1002655, "FY2025": -1189390, "FY2024": -1105027, "FY2023": -696297, "FY2022": -223230}),
        ("TOTAL", "Net interest income", {"FY2026": 733205, "FY2025": 790461, "FY2024": 828957, "FY2023": 749025, "FY2022": 496308}),
        ("DATA", "Fee and commission income", {"FY2026": 228134, "FY2025": 194340, "FY2024": 178770, "FY2023": 456215, "FY2022": 508929}),
        ("DATA", "Fee and commission expense", {"FY2026": -21489, "FY2025": -13864, "FY2024": -16381, "FY2023": -15372, "FY2022": -14697}),
        ("DATA", "Investment income", {"FY2026": 42880, "FY2025": 41811, "FY2024": 2625, "FY2023": 5003, "FY2022": 10579}),
        ("DATA", "Share of post-taxation profit of associates and joint venture holdings", {"FY2026": 60283, "FY2025": 38081, "FY2024": 9032, "FY2023": 660, "FY2022": 1988}),
        ("DATA", "Trading income arising from customer flow", {"FY2026": 91494, "FY2025": 85542, "FY2024": 103158, "FY2023": 87366, "FY2022": 60372}),
        ("DATA", "Trading income arising from balance sheet management and other trading activities", {"FY2026": 6013, "FY2025": 14248, "FY2024": 27119, "FY2023": 13060, "FY2022": -1305}),
        ("DATA", "Other operating income", {"FY2026": 21173, "FY2025": 6676, "FY2024": 2915, "FY2023": 12620, "FY2022": 11158}),
        ("TOTAL", "Operating income before expected credit loss impairment charges", {"FY2026": 1161693, "FY2025": 1157295, "FY2024": 1136195, "FY2023": 1308577, "FY2022": 1073332}),
        ("DATA", "Expected credit loss impairment charges", {"FY2026": -97349, "FY2025": -97040, "FY2024": -85997, "FY2023": -66740, "FY2022": -25363}),
        ("TOTAL", "Operating income after expected credit loss impairment charges", {"FY2026": 1064344, "FY2025": 1060255, "FY2024": 1050198, "FY2023": 1241837, "FY2022": 1047969}),
        ("DATA", "Operating costs", {"FY2026": -607310, "FY2025": -597719, "FY2024": -626732, "FY2023": -833061, "FY2022": -760286}),
        ("DATA", "Impairment of goodwill", {"FY2023": -805}),
        ("DATA", "Amortisation of acquired intangibles", {"FY2025": 0, "FY2024": -940, "FY2023": -12625, "FY2022": -12936}),
        ("DATA", "Closure and rundown of the Hong Kong direct investments business", {"FY2025": 319, "FY2024": -784, "FY2023": -480, "FY2022": -1203}),
        ("DATA", "Financial impact of strategic actions", {"FY2026": -17393, "FY2025": -16007}),
        ("TOTAL", "Profit before taxation", {"FY2026": 439641, "FY2025": 446848, "FY2024": 421742, "FY2023": 394866, "FY2022": 273544}),
        ("DATA", "Taxation on operating profit before acquired intangibles/goodwill and strategic actions", {"FY2026": -87619, "FY2025": -80222, "FY2024": -96956, "FY2023": -83288, "FY2022": -42174}),
        ("DATA", "Taxation on acquired intangibles/goodwill and strategic actions", {"FY2026": 1529, "FY2025": -195, "FY2024": 427, "FY2023": 2031, "FY2022": 1511}),
        ("TOTAL", "Profit after taxation from continuing operations", {"FY2026": 353551, "FY2025": 366431, "FY2024": 325213, "FY2023": 313609, "FY2022": 232881}),
        ("DATA", "Profit after taxation from discontinued operations", {"FY2024": 395600}),
        ("TOTAL", "Profit after taxation", {"FY2026": 353551, "FY2025": 366431, "FY2024": 720813, "FY2023": 313609, "FY2022": 232881}),
        ("DATA", "Profit/(loss) attributable to non-controlling interests", {"FY2026": -355, "FY2025": -12, "FY2024": -1204}),
        ("TOTAL", "Earnings attributable to shareholder/equity holders", {"FY2026": 353196, "FY2025": 366419, "FY2024": 719609, "FY2023": 313609, "FY2022": 232881}),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Fair value movements on cash flow hedges taken directly to OCI", {"FY2026": -8931, "FY2025": -11259, "FY2024": -9971}),
        ("DATA", "Gains/(losses) on realisation of debt instruments at FVOCI recycled through the income statement", {"FY2026": 2171, "FY2025": -166, "FY2024": -817, "FY2023": -313, "FY2022": -307}),
        ("DATA", "Fair value movements on debt instruments at FVOCI taken directly to OCI", {"FY2026": -128, "FY2025": -6120, "FY2024": 6078, "FY2023": 217, "FY2022": -2276}),
        ("DATA", "Foreign currency adjustments on translating foreign operations", {"FY2026": 3984, "FY2025": -4305, "FY2024": -3601, "FY2023": 5615, "FY2022": 5401}),
        ("DATA", "Hedge of net investment in subsidiary", {"FY2026": -2080}),
        ("DATA", "Share of other comprehensive income of associates and joint venture holdings", {"FY2026": 27, "FY2025": -3803, "FY2024": 257}),
        ("DATA", "Effect of rate change on deferred taxation relating to adjustment for IFRS 9", {"FY2023": -7, "FY2022": 617}),
        ("DATA", "Gains attributable to own credit risk", {"FY2022": 11059}),
        ("DATA", "Movement in post-retirement benefit liabilities", {"FY2023": 75, "FY2022": 40}),
        ("TOTAL", "Total comprehensive income for the year", {"FY2026": 348594, "FY2025": 340778, "FY2024": 712759, "FY2023": 346831, "FY2022": 247415}),
    ],
    sources_text=PL_SOURCES,
    first_col_width=80,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = [
    "Ordinary share capital", "Share premium", "Capital reserve account", "Fair value reserve",
    "Cash flow hedge reserve", "Foreign currency reserve", "Retained income",
    "Shareholder's equity excl. NCI", "Additional Tier 1 securities", "Non-controlling interests", "Total equity",
]
EQUITY_SOURCES = (
    "Sources — Investec Bank plc Group Statement of Changes in Equity, £'000:\n"
    f"1 Apr 2021 - 31 Mar 2023: Investec Bank plc Annual Financial Statements 2023, p.124-125 — {AR23_URL}\n"
    f"1 Apr 2023 - 31 Mar 2025: Investec Bank plc Annual Financial Statements 2025, p.124-125 — {AR25_URL}\n"
    f"1 Apr 2025 - 31 Mar 2026: Investec Bank plc Annual Financial Statements 2026, p.128-129 — {AR26_URL}\n"
    "Equity reconciliation ladder confirmed: every year's own closing Total equity ties exactly to (a) the next "
    "year's own reported opening balance and (b) that year's own Balance Sheet Total equity - zero plug rows "
    "needed anywhere across all 5 years (2,364,920 -> 2,547,185 -> 2,789,454 -> 3,606,218 -> 3,672,680 -> "
    "3,866,088). Movement rows follow each year's own labelling exactly (e.g. 'Release of capital reserve to "
    "retained income' is a net-zero internal reclassification, not a real gain/loss)."
)

bw.add_equity_changes_sheet(
    title="Investec Bank plc — Statement of Changes in Equity",
    subtitle="Investec Bank plc Group (consolidated basis), £'000. Chronological roll-forward, oldest to newest.",
    headers=EQUITY_HEADERS,
    rows=[
        ("TOTAL", "At 1 April 2021", (1280550, 199538, 153177, 3043, None, -4147, 494092, 2114530, 250000, 390, 2364920)),
        ("DATA", "Profit after taxation", (None, None, None, None, None, None, 232881, 232881, None, None, 232881)),
        ("DATA", "Effect of rate change on deferred taxation relating to adjustment for IFRS 9", (None, None, None, -47, None, None, None, 617, None, None, 617)),
        ("DATA", "Gains on realisation of debt instruments at FVOCI recycled through the income statement", (None, None, None, -307, None, None, None, -307, None, None, -307)),
        ("DATA", "Fair value movements on debt instruments at FVOCI taken directly to OCI", (None, None, None, -2276, None, None, None, -2276, None, None, -2276)),
        ("DATA", "Foreign currency adjustments on translating foreign operations", (None, None, None, None, None, 5401, None, 5401, None, None, 5401)),
        ("DATA", "Gains attributable to own credit risk", (None, None, None, None, None, None, None, None, None, None, 11059)),
        ("DATA", "Movement in post-retirement benefit liabilities", (None, None, None, None, None, None, 40, 40, None, None, 40)),
        ("TOTAL", "Total comprehensive income for the year", (None, None, None, -2630, None, 5401, 232921, 247415, None, None, 247415)),
        ("DATA", "Share-based payments adjustments", (None, None, None, None, None, None, 3637, 3637, None, None, 3637)),
        ("DATA", "Employee benefit liability recognised", (None, None, None, None, None, None, 4145, 4145, None, None, 4145)),
        ("DATA", "Dividends paid to ordinary shareholder", (None, None, None, None, None, None, -56500, -56500, None, None, -56500)),
        ("DATA", "Dividends declared to Additional Tier 1 security holders", (None, None, None, None, None, None, -16875, -16875, 16875, None, 0)),
        ("DATA", "Dividends paid to Additional Tier 1 security holders", (None, None, None, None, None, None, None, None, -16875, None, -16875)),
        ("DATA", "Net equity impact of non-controlling interest movements", (None, None, None, None, None, None, None, None, None, 443, 443)),
        ("TOTAL", "At 31 March 2022", (1280550, 199538, 153177, 413, None, 1254, 661420, 2296352, 250000, 833, 2547185)),
        ("DATA", "Profit after taxation", (None, None, None, None, None, None, 313609, 313609, None, None, 313609)),
        ("DATA", "Effect of rate change on deferred taxation relating to adjustment for IFRS 9", (None, None, None, -7, None, None, None, -7, None, None, -7)),
        ("DATA", "Gains on realisation of debt instruments at FVOCI recycled through the income statement", (None, None, None, -313, None, None, None, -313, None, None, -313)),
        ("DATA", "Fair value movements on cash flow hedges taken directly to OCI", (None, None, None, None, 27635, None, None, 27635, None, None, 27635)),
        ("DATA", "Fair value movements on debt instruments at FVOCI taken directly to OCI", (None, None, None, 217, None, None, None, 217, None, None, 217)),
        ("DATA", "Foreign currency adjustments on translating foreign operations", (None, None, None, None, None, 5615, None, 5615, None, None, 5615)),
        ("DATA", "Movement in post-retirement benefit liabilities", (None, None, None, None, None, None, 75, 75, None, None, 75)),
        ("TOTAL", "Total comprehensive income for the year", (None, None, None, -103, 27635, 5615, 313684, 346831, None, None, 346831)),
        ("DATA", "Share-based payments adjustments", (None, None, None, None, None, None, -295, -295, None, None, -295)),
        ("DATA", "Employee benefit liability recognised", (None, None, None, None, None, None, 7490, 7490, None, None, 7490)),
        ("DATA", "Dividends paid to ordinary shareholder", (None, None, None, None, None, None, -95000, -95000, None, None, -95000)),
        ("DATA", "Dividends declared to Additional Tier 1 security holders", (None, None, None, None, None, None, -16875, -16875, 16875, None, 0)),
        ("DATA", "Dividends paid to Additional Tier 1 security holders", (None, None, None, None, None, None, None, None, -16875, None, -16875)),
        ("DATA", "Net equity impact of non-controlling interest movements", (None, None, None, None, None, None, None, None, None, 118, 118)),
        ("TOTAL", "At 31 March 2023", (1280550, 199538, 153177, 310, 27635, 6869, 870424, 2538503, 250000, 951, 2789454)),
        ("DATA", "Profit after taxation", (None, None, None, None, None, None, 719609, 719609, None, 1204, 720813)),
        ("DATA", "Gains/(losses) on realisation of debt instruments at FVOCI recycled through the income statement", (None, None, None, -817, None, None, None, -817, None, None, -817)),
        ("DATA", "Fair value movements on cash flow hedges taken directly to OCI", (None, None, None, None, -9971, None, None, -9971, None, None, -9971)),
        ("DATA", "Fair value movements on debt instruments at FVOCI taken directly to OCI", (None, None, None, 6078, None, None, None, 6078, None, None, 6078)),
        ("DATA", "Foreign currency adjustments on translating foreign operations", (None, None, None, None, None, -3580, None, -3580, None, -21, -3601)),
        ("DATA", "Share of other comprehensive income of associates and joint venture holdings", (None, None, None, None, None, None, 257, 257, None, None, 257)),
        ("TOTAL", "Total comprehensive income for the year", (None, None, None, 5261, -9971, -3580, 719866, 711576, None, 1183, 712759)),
        ("DATA", "Share-based payments adjustments", (None, None, None, None, None, None, 5427, 5427, None, None, 5427)),
        ("DATA", "Employee benefit liability recognised", (None, None, None, None, None, None, 1740, 1740, None, None, 1740)),
        ("DATA", "Transaction with equity holders", (None, None, None, None, None, None, -2971, -2971, None, None, -2971)),
        ("DATA", "Issue of Additional Tier 1 security instruments", (None, None, None, None, None, None, None, None, 350000, None, 350000)),
        ("DATA", "Redemption of Additional Tier 1 security instruments", (None, None, None, None, None, None, None, None, -141892, None, -141892)),
        ("DATA", "Dividends paid to ordinary shareholder", (None, None, None, None, None, None, -89798, -89798, None, None, -89798)),
        ("DATA", "Dividends declared to Additional Tier 1 security holders", (None, None, None, None, None, None, -20638, -20638, 20638, None, 0)),
        ("DATA", "Dividends paid to Additional Tier 1 security holders", (None, None, None, None, None, None, None, None, -20638, None, -20638)),
        ("DATA", "Gains on Additional Tier 1 security instruments callback", (None, None, None, None, None, None, 1420, 1420, None, None, 1420)),
        ("DATA", "Net equity impact of non-controlling interest movements", (None, None, None, None, None, None, None, None, None, 717, 717)),
        ("DATA", "Release of capital reserve to retained income", (None, None, -141903, None, None, None, 141903, None, None, None, 0)),
        ("TOTAL", "At 31 March 2024", (1280550, 199538, 11274, 5571, 17664, 3289, 1627373, 3145259, 458108, 2851, 3606218)),
        ("DATA", "Profit after taxation", (None, None, None, None, None, None, 366419, 366419, None, 12, 366431)),
        ("DATA", "Gains on realisation of debt instruments at FVOCI recycled through the income statement", (None, None, None, -166, None, None, None, -166, None, None, -166)),
        ("DATA", "Fair value movements on cash flow hedges taken directly to OCI", (None, None, None, None, -11259, None, None, -11259, None, None, -11259)),
        ("DATA", "Fair value movements on debt instruments at FVOCI taken directly to OCI", (None, None, None, -6120, None, None, None, -6120, None, None, -6120)),
        ("DATA", "Foreign currency adjustments on translating foreign operations", (None, None, None, None, None, -4305, None, -4305, None, None, -4305)),
        ("DATA", "Share of other comprehensive income of associates and joint venture holdings", (None, None, None, None, None, None, -3803, -3803, None, None, -3803)),
        ("TOTAL", "Total comprehensive income for the year", (None, None, None, -6286, -11259, -4305, 362616, 340766, None, 12, 340778)),
        ("DATA", "Share-based payments adjustments", (None, None, None, None, None, None, 107, 107, None, None, 107)),
        ("DATA", "Employee benefit liability recognised", (None, None, None, None, None, None, 402, 402, None, None, 402)),
        ("DATA", "Redemption of Additional Tier 1 security instruments", (None, None, None, None, None, None, None, None, -108108, None, -108108)),
        ("DATA", "Dividends paid to ordinary shareholder", (None, None, None, None, None, None, -120000, -120000, None, None, -120000)),
        ("DATA", "Dividends declared to Additional Tier 1 security holders", (None, None, None, None, None, None, -38356, -38356, 38356, None, 0)),
        ("DATA", "Dividends paid to Additional Tier 1 security holders", (None, None, None, None, None, None, None, None, -38356, None, -38356)),
        ("DATA", "Net equity impact of non-controlling interest movements", (None, None, None, None, None, None, 1755, 1755, None, -1667, 88)),
        ("DATA", "Net equity movements in associates and joint ventures", (None, None, None, None, None, None, -8449, -8449, None, None, -8449)),
        ("DATA", "Release of capital reserve to retained income", (None, None, -11274, None, None, None, 11274, None, None, None, 0)),
        ("TOTAL", "At 31 March 2025", (1280550, 199538, 0, -715, 6405, -1016, 1836722, 3321484, 350000, 1196, 3672680)),
        ("DATA", "Profit after taxation", (None, None, None, None, None, None, 353196, 353196, None, 355, 353551)),
        ("DATA", "Gains on realisation of debt instruments at FVOCI recycled through the income statement", (None, None, None, 2171, None, None, None, 2171, None, None, 2171)),
        ("DATA", "Fair value movements on cash flow hedges taken directly to OCI", (None, None, None, None, -8931, None, None, -8931, None, None, -8931)),
        ("DATA", "Fair value movements on debt instruments at FVOCI taken directly to OCI", (None, None, None, -128, None, None, None, -128, None, None, -128)),
        ("DATA", "Foreign currency adjustments on translating foreign operations", (None, None, None, None, None, 4456, None, 4456, None, -472, 3984)),
        ("DATA", "Share of other comprehensive income of associates and joint venture holdings", (None, None, None, None, None, None, 27, 27, None, None, 27)),
        ("DATA", "Hedge of net investment in subsidiary", (None, None, None, None, None, -2080, None, -2080, None, None, -2080)),
        ("TOTAL", "Total comprehensive income for the year", (None, None, None, 2043, -8931, 2376, 353223, 348711, None, -117, 348594)),
        ("DATA", "Share-based payments adjustments", (None, None, None, None, None, None, 10515, 10515, None, None, 10515)),
        ("DATA", "Employee benefit liability recognised", (None, None, None, None, None, None, 238, 238, None, None, 238)),
        ("DATA", "Dividends paid to ordinary shareholder", (None, None, None, None, None, None, -137000, -137000, None, None, -137000)),
        ("DATA", "Dividends declared to Additional Tier 1 security holders", (None, None, None, None, None, None, -36750, -36750, 36750, None, 0)),
        ("DATA", "Dividends paid to Additional Tier 1 security holders", (None, None, None, None, None, None, None, None, -36750, None, -36750)),
        ("DATA", "Net equity impact of non-controlling interest movements", (None, None, None, None, None, None, None, None, None, -72, -72)),
        ("DATA", "Net equity movements in associates and joint ventures", (None, None, None, None, None, None, 7883, 7883, None, None, 7883)),
        ("TOTAL", "At 31 March 2026", (1280550, 199538, 0, 1328, -2526, 1360, 2034831, 3515081, 350000, 1007, 3866088)),
    ],
    sources_text=EQUITY_SOURCES,
    first_col_width=62,
    source_height=140,
)

# ---------------------------------------------------------------
# Sheet 4: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before taxation adjusted for non-cash items", {"FY2026": 547146, "FY2025": 552838, "FY2024": 567094, "FY2023": 509014, "FY2022": 350162}),
    ("DATA", "Taxation paid", {"FY2026": -73176, "FY2025": -64733, "FY2024": -110339, "FY2023": -74998, "FY2022": -53294}),
    ("DATA", "Increase in operating assets", {"FY2026": -3142293, "FY2025": -1317141, "FY2024": -1471004, "FY2023": -1268534, "FY2022": -823132}),
    ("DATA", "Increase/(decrease) in operating liabilities", {"FY2026": 1944798, "FY2025": -132847, "FY2024": 1273760, "FY2023": 435513, "FY2022": 3076202}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities", {"FY2026": -723525, "FY2025": -961883, "FY2024": 259511, "FY2023": -399005, "FY2022": 2549938}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Cash flow on acquisition of subsidiaries, net of cash acquired", {"FY2026": -1167, "FY2025": 0, "FY2024": -28559, "FY2023": -9720, "FY2022": 0}),
    ("DATA", "Cash flow on disposal of subsidiaries", {"FY2026": 0, "FY2025": 0, "FY2024": 0, "FY2023": 12, "FY2022": 14274}),
    ("DATA", "Derecognition of cash on deconsolidation/disposal of subsidiaries", {"FY2025": 0, "FY2024": -172615, "FY2023": 0, "FY2022": -4152}),
    ("DATA", "Cash flow on net disposal of non-controlling interest", {"FY2023": 118, "FY2022": 443}),
    ("DATA", "Cash flow on net disposal/(acquisition) of associates and joint venture holdings", {"FY2023": 565, "FY2022": -8780}),
    ("DATA", "Cash flow on acquisition of associates and joint venture holdings", {"FY2026": -5769}),
    ("DATA", "Cash flow on disposal of associate", {"FY2026": 1952}),
    ("DATA", "Cash flow on acquisition of property, equipment, software and other intangible assets", {"FY2026": -46946, "FY2025": -3943, "FY2024": -3848, "FY2023": -11712, "FY2022": -4931}),
    ("DATA", "Cash flow on disposal of property, equipment, software and other intangible assets", {"FY2026": 137, "FY2025": 204, "FY2024": 157, "FY2023": 23975, "FY2022": 4273}),
    ("TOTAL", "Net cash (outflow)/inflow from investing activities", {"FY2026": -51793, "FY2025": -3739, "FY2024": -204865, "FY2023": 3238, "FY2022": 1127}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Dividends paid to ordinary shareholder", {"FY2026": -137000, "FY2025": -120000, "FY2024": -89798, "FY2023": -95000, "FY2022": -56500}),
    ("DATA", "Dividends paid to other equity holders", {"FY2026": -36750, "FY2025": -42223, "FY2024": -16771, "FY2023": -16875, "FY2022": -16875}),
    ("DATA", "Proceeds on issue of Additional Tier 1 Securities", {"FY2025": 0, "FY2024": 350000}),
    ("DATA", "Redemption of Additional Tier 1 instruments", {"FY2026": 0, "FY2025": -108108, "FY2024": -140472}),
    ("DATA", "Proceeds from issue of subordinated debt", {"FY2026": 298343, "FY2023": 345590, "FY2022": 347536}),
    ("DATA", "Redemption of subordinated debt", {"FY2026": -290850, "FY2025": 0, "FY2024": -70000, "FY2023": -347925, "FY2022": -307962}),
    ("DATA", "Lease liabilities paid", {"FY2026": -143227, "FY2025": -43776, "FY2024": -42444, "FY2023": -44089, "FY2022": -43253}),
    ("TOTAL", "Net cash outflow from financing activities", {"FY2026": -309484, "FY2025": -314107, "FY2024": -9485, "FY2023": -158299, "FY2022": -77054}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2026": 7023, "FY2025": -1128, "FY2024": -498, "FY2023": 773, "FY2022": -607}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2026": -1077779, "FY2025": -1280857, "FY2024": 44663, "FY2023": -553293, "FY2022": 2473404}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2026": 5051552, "FY2025": 6332409, "FY2024": 6287746, "FY2023": 6841039, "FY2022": 4367635}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2026": 3973773, "FY2025": 5051552, "FY2024": 6332409, "FY2023": 6287746, "FY2022": 6841039}),
    ("SECTION", "Cash and cash equivalents at end of year comprise", {}),
    ("DATA", "Cash and balances at central banks", {"FY2026": 3173756, "FY2025": 4191750, "FY2024": 5661623, "FY2023": 5400401, "FY2022": 5379994}),
    ("DATA", "On demand loans and advances to banks", {"FY2026": 800017, "FY2025": 859802, "FY2024": 670786, "FY2023": 887345, "FY2022": 1461045}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2026": 3973773, "FY2025": 5051552, "FY2024": 6332409, "FY2023": 6287746, "FY2022": 6841039}),
]

bw.add_cash_flow_sheet(
    title="Investec Bank plc — Consolidated Cash Flow Statement",
    subtitle="Investec Bank plc Group (consolidated basis), £'000 unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=140,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources — IBP Group gross core loans subject to ECL, by IFRS 9 stage, £'million (as disclosed - not "
    "converted to £'000, unlike the other new statement sheets, to match each source table's own units):\n"
    f"FY2026: Investec Bank plc Annual Financial Statements 2026, p.247 ('An analysis of credit quality by "
    f"internal rating grade') — {AR26_URL}\n"
    f"FY2025 (own) & FY2024 (comparative): Investec Bank plc Annual Financial Statements 2025, p.252 ('An "
    f"analysis of gross core loans, asset quality and ECL') — {AR25_URL}\n"
    f"FY2023 (own) & FY2022 (comparative): Investec Bank plc Annual Financial Statements 2023, p.236 (same "
    f"table) — {AR23_URL}\n"
    "Note: FY2026's Annual Report re-presents FY2025 as 14,524/1,331/563 (Stage 1/2/3 gross) - marginally "
    "different from FY2025's own originally-published 14,520/1,328/536 shown here, a presentation re-mapping "
    "detailed on the FY2026 report's own p.252, not a transcription error; each year's own originally-published "
    "figure is used per project convention. Coverage ratios are each year's own disclosed percentages, not "
    "recomputed, to avoid rounding drift - except FY2026, whose Annual Report replaced the simple per-stage "
    "coverage-ratio table with a by-internal-rating-grade breakdown; FY2026's per-stage coverage ratios shown "
    "here are derived (ECL / gross exposure) rather than directly disclosed."
)

bw.add_asset_quality_sheet(
    title="Investec Bank plc — Asset Quality",
    subtitle="Investec Bank plc Group, gross core loans subject to ECL by IFRS 9 stage, £'million",
    rows=[
        ("SECTION", "Gross exposure", {}),
        ("DATA", "Stage 1", {"FY2026": 15354, "FY2025": 14520, "FY2024": 14181, "FY2023": 13494, "FY2022": 12665}),
        ("DATA", "Stage 2", {"FY2026": 1266, "FY2025": 1328, "FY2024": 1391, "FY2023": 1321, "FY2022": 992}),
        ("DATA", "Stage 3", {"FY2026": 582, "FY2025": 536, "FY2024": 531, "FY2023": 343, "FY2022": 291}),
        ("TOTAL", "Gross core loans subject to ECL", {"FY2026": 17202, "FY2025": 16384, "FY2024": 16103, "FY2023": 15158, "FY2022": 13948}),
        ("SECTION", "Expected credit loss (ECL)", {}),
        ("DATA", "Stage 1", {"FY2026": -37, "FY2025": -34, "FY2024": -43, "FY2023": -39, "FY2022": -32}),
        ("DATA", "Stage 2", {"FY2026": -28, "FY2025": -31, "FY2024": -33, "FY2023": -32, "FY2022": -35}),
        ("DATA", "Stage 3", {"FY2026": -142, "FY2025": -100, "FY2024": -111, "FY2023": -75, "FY2022": -67}),
        ("TOTAL", "Total ECL", {"FY2026": -207, "FY2025": -165, "FY2024": -187, "FY2023": -146, "FY2022": -134}),
        ("SECTION", "Coverage ratios (as disclosed)", {}),
        ("DATA", "Stage 1 coverage ratio", {"FY2026": "0.24%", "FY2025": "0.23%", "FY2024": "0.30%", "FY2023": "0.29%", "FY2022": "0.25%"}),
        ("DATA", "Stage 2 coverage ratio", {"FY2026": "2.2%", "FY2025": "2.3%", "FY2024": "2.4%", "FY2023": "2.4%", "FY2022": "3.5%"}),
        ("DATA", "Stage 3 coverage ratio", {"FY2026": "24.4%", "FY2025": "18.7%", "FY2024": "20.9%", "FY2023": "21.9%", "FY2022": "23.0%"}),
        ("DATA", "Stage 3 as a % of gross core loans subject to ECL", {"FY2026": "3.4%", "FY2025": "3.3%", "FY2024": "3.3%", "FY2023": "2.3%", "FY2022": "2.1%"}),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=170,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Consolidated basis, {unit}" if unit else "Consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=140)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2026": 2681, "FY2025": 2570, "FY2024": 2409, "FY2023": 2195, "FY2022": 1982})],
    p3_sources(283, 290, 272, "Capital structure"),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2026": "13.3%", "FY2025": "13.6%", "FY2024": "13.3%", "FY2023": "12.7%", "FY2022": "12.0%"})],
    p3_sources(280, 287, 270, "A summary of capital adequacy and leverage ratios"),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2026": 3031, "FY2025": 2920, "FY2024": 2867, "FY2023": 2445, "FY2022": 2232})],
    p3_sources(283, 290, 272, "Capital structure"),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2026": "15.0%", "FY2025": "15.4%", "FY2024": "15.9%", "FY2023": "14.1%", "FY2022": "13.6%"})],
    p3_sources(280, 287, 270, "A summary of capital adequacy and leverage ratios"),
)

metric(
    "Total Capital", "£m",
    [("Total regulatory capital", {"FY2026": 3751, "FY2025": 3632, "FY2024": 3579, "FY2023": 3209, "FY2022": 2998})],
    p3_sources(283, 290, 272, "Capital structure"),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total Capital ratio", {"FY2026": "18.6%", "FY2025": "19.2%", "FY2024": "19.8%", "FY2023": "18.5%", "FY2022": "18.2%"})],
    p3_sources(280, 287, 270, "A summary of capital adequacy and leverage ratios"),
)

metric(
    "Total RWAs", "£m",
    [("Risk weighted assets", {"FY2026": 20177, "FY2025": 18908, "FY2024": 18054, "FY2023": 17308, "FY2022": 16462})],
    p3_sources(280, 287, 270, "A summary of capital adequacy and leverage ratios"),
)

RWA_BREAKDOWN_SOURCES = (
    "Sources — IBP Group Risk weighted assets and capital requirements table, £'million (Notes to risk and "
    "capital management, 'Capital structure'):\n"
    f"FY2026 & FY2025: Investec Bank plc Annual Financial Statements 2026, p.283 — {AR26_URL}\n"
    f"FY2024: Investec Bank plc Annual Financial Statements 2025, p.290 — {AR25_URL}\n"
    f"FY2023 & FY2022: Investec Bank plc Annual Financial Statements 2023, p.272 — {AR23_URL}\n"
    "Each year's Total row ties exactly to the Total RWAs sheet's own disclosed figure. RWAs are calculated "
    "applying IFRS 9 transitional arrangements through FY2025; these ceased 1 April 2025, so FY2026 is on a "
    "fully-loaded basis (both bases shown as disclosed each year, not adjusted for comparability)."
)

bw.add_rwa_breakdown_sheet(
    title="Investec Bank plc — RWA Breakdown",
    subtitle="Investec Bank plc Group, risk weighted assets by category, £'million",
    rows=[
        ("DATA", "Credit risk", {"FY2026": 16572, "FY2025": 15575, "FY2024": 15276, "FY2023": 14118, "FY2022": 13332}),
        ("DATA", "Equity risk", {"FY2026": 178, "FY2025": 113, "FY2024": 89, "FY2023": 153, "FY2022": 57}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2026": 426, "FY2025": 463, "FY2024": 377, "FY2023": 487, "FY2022": 591}),
        ("DATA", "Credit valuation adjustment (CVA) risk", {"FY2026": 32, "FY2025": 30, "FY2024": 27, "FY2023": 37, "FY2022": 103}),
        ("DATA", "Market risk", {"FY2026": 371, "FY2025": 445, "FY2024": 428, "FY2023": 511, "FY2022": 608}),
        ("DATA", "Operational risk", {"FY2026": 2598, "FY2025": 2282, "FY2024": 1857, "FY2023": 2002, "FY2022": 1771}),
        ("TOTAL", "Total risk weighted assets", {"FY2026": 20177, "FY2025": 18908, "FY2024": 18054, "FY2023": 17308, "FY2022": 16462}),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=150,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Leverage exposure measure (£m)", {"FY2026": 31774, "FY2025": 27906, "FY2024": 26746, "FY2023": 24945, "FY2022": 23874}),
        ("Leverage ratio (%)", {"FY2026": "9.5%", "FY2025": "10.5%", "FY2024": "10.7%", "FY2023": "9.8%", "FY2022": "9.3%"}),
    ],
    p3_sources(280, 287, 270, "A summary of capital adequacy and leverage ratios"),
)

LCR_NSFR_SOURCES = (
    "Sources — Investec Bank plc (IBP) solo-entity liquidity disclosures, Table 44 'Key metrics (UK KM1)', "
    "Appendix A (IBP's own Pillar 3 disclosures, signed by the IBP Finance Director and IBP Risk Officer):\n"
    f"FY2026 (31 March 2026): Investec plc Group and Investec Bank plc Pillar 3 annual disclosure report 2026, "
    f"p.85, UK KM1 row 17 (LCR) / row 20 (NSFR) — {ANNUAL_P3_2026_URL}\n"
    f"FY2025 (31 March 2025): Investec plc Group and Investec Bank plc Pillar 3 annual disclosure report 2025, "
    f"p.85, UK KM1 row 17 / row 20 — {ANNUAL_P3_2025_URL}\n"
    f"FY2024 (31 March 2024): Investec plc Group and Investec Bank plc Pillar 3 annual disclosure report 2024, "
    f"p.85, UK KM1 row 17 / row 20 — {ANNUAL_P3_2024_URL}\n"
    f"FY2023 (31 March 2023): Investec plc group and Investec Bank plc Pillar 3 disclosure report, 30 Sept 2023, "
    f"p.44, UK KM1 row 17 / row 20 comparative column (no standalone 31 March 2023 annual Pillar 3 report was ever "
    f"published — confirmed via Wayback Machine snapshots of investec.com's regulatory-disclosures listing page "
    f"from 3 Oct 2023, which still shows no such document) — {INTERIM_2023_URL}\n"
    "LCR is the 12-month average ratio; NSFR is the trailing 4-quarter average ratio, per each report's own "
    "table footnotes. Figures cross-validate exactly against the comparative columns in the adjacent semi-annual "
    "reports (e.g. the FY2026 report's 31 March 2025 comparative matches the FY2025 report's own-year figure) and "
    "against the 31 March comparative rows already recorded on the 'Interim Pillar 3' sheet."
)

metric(
    "LCR", None,
    [("Liquidity Coverage Ratio", {
        "FY2026": "361%", "FY2025": "465%", "FY2024": "446%", "FY2023": "431%", "FY2022": "Not publicly disclosed",
    })],
    LCR_NSFR_SOURCES,
    note="FY2022 (31 March 2022): not publicly disclosed. No standalone Pillar 3 report for that period-end was "
         "ever published for Investec plc/Investec Bank plc — confirmed via Wayback Machine snapshots of "
         "investec.com's Basel Pillar III regulatory-disclosures listing page taken 30 Sept 2022 and 3 Oct 2023 "
         "(the most recent annual/semi-annual disclosure listed on both is the 2021 annual report; no 2022 entry "
         "appears on either snapshot). IBP's Annual Financial Statements 2023 discuss the liquidity buffer and "
         "funding strategy qualitatively for that year (see 'Balance sheet risk' / 'Liquidity risk' notes) but do "
         "not publish a numeric LCR% for the solo entity.",
)

metric(
    "NSFR", None,
    [("Net Stable Funding Ratio", {
        "FY2026": "141%", "FY2025": "145%", "FY2024": "138%", "FY2023": "136%", "FY2022": "Not publicly disclosed",
    })],
    LCR_NSFR_SOURCES,
    note="Same availability constraint as the LCR sheet for FY2022 (31 March 2022) — no standalone Pillar 3 "
         "report covering that period-end was ever published; confirmed via the same Wayback Machine snapshots "
         "(30 Sept 2022 and 3 Oct 2023) of investec.com's regulatory-disclosures listing page.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(280, 287, 270),
    note="No MREL ratio is disclosed as such in any of the 5 years. Per the 'Recovery and resolution planning' / "
         "'Liquidity risk' notes: at FY2022-FY2025, IBP's preferred resolution strategy was bank insolvency "
         "procedure (from March 2021, Modified Insolvency) with MREL set equal to IBP's Total Capital Requirement "
         "(Pillar 1 plus Pillar 2A) — i.e. no MREL requirement in excess of minimum capital requirements, so no "
         "separate ratio was tracked. The BoE confirmed in December 2025 that the preferred strategy is changing to "
         "bail-in with a binding MREL requirement; the MREL transition commenced 1 January 2026 (FY2026) in a "
         "phased manner, with end-state MREL applying from 1 January 2032 — so FY2026 is the first year with a "
         "binding requirement, but no numeric ratio had yet been published as at this report's cutoff.",
)

# ---------------------------------------------------------------
# Sheet 13: Interim Pillar 3
# ---------------------------------------------------------------
interim_ws = bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=INTERIM_ROWS,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(INTERIM_ROWS)},
    title="Investec Bank plc — Interim Pillar 3 Disclosures",
    subtitle="Investec Bank plc solo-consolidated basis; £m unless stated",
    note="Official entity-level Appendix A disclosures are available for September 2023, 2024 and 2025, with March comparatives. The 2022 report states that significant subsidiary disclosures continued to be published annually, so September 2021 and September 2022 gaps are recorded explicitly. LCR is a 12-month average; IFRS 9 transitional-basis comparatives are not separately duplicated here.",
)
# Keep the source register directly below the matrix so the generic verifier
# can discover it without treating the helper's spacer rows as end-of-data.
interim_ws.delete_rows(4 + len({row[2] for row in INTERIM_ROWS}) + 1, 2)
source_data_start = 4 + len({row[2] for row in INTERIM_ROWS}) + 3
for source_row in range(source_data_start, interim_ws.max_row + 1):
    source_cell = interim_ws.cell(row=source_row, column=3)
    if source_cell.value in (None, ""):
        break
    source_cell.hyperlink = source_cell.value
    source_cell.style = "Hyperlink"

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2026": 31827508, "FY2025": 29734085, "FY2024": 29838043, "FY2023": 28242603, "FY2022": 27588676}),
        ("Loans and advances to customers", {"FY2026": 17803653, "FY2025": 16813723, "FY2024": 16570313, "FY2023": 15567809, "FY2022": 14426475}),
        ("Customer accounts (deposits)", {"FY2026": 22534593, "FY2025": 21555444, "FY2024": 20851216, "FY2023": 19251399, "FY2022": 18616233}),
        ("Total equity", {"FY2026": 3866088, "FY2025": 3672680, "FY2024": 3606218, "FY2023": 2789454, "FY2022": 2547185}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income before expected credit loss impairment charges", {"FY2026": 1161693, "FY2025": 1157295, "FY2024": 1136195, "FY2023": 1308577, "FY2022": 1073332}),
        ("Operating costs", {"FY2026": -607310, "FY2025": -597719, "FY2024": -626732, "FY2023": -833061, "FY2022": -760286}),
        ("Profit after taxation", {"FY2026": 353551, "FY2025": 366431, "FY2024": 720813, "FY2023": 313609, "FY2022": 232881}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2026": 3672680, "FY2025": 3606218, "FY2024": 2789454, "FY2023": 2547185, "FY2022": 2364920}),
        ("Total comprehensive income for the year", {"FY2026": 348594, "FY2025": 340778, "FY2024": 712759, "FY2023": 346831, "FY2022": 247415}),
        ("Other equity movements, net", {"FY2026": -155186, "FY2025": -274316, "FY2024": 104005, "FY2023": -104562, "FY2022": -65150}),
        ("Closing equity", {"FY2026": 3866088, "FY2025": 3672680, "FY2024": 3606218, "FY2023": 2789454, "FY2022": 2547185}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash (outflow)/inflow from operating activities", {"FY2026": -723525, "FY2025": -961883, "FY2024": 259511, "FY2023": -399005, "FY2022": 2549938}),
        ("Net cash (outflow)/inflow from investing activities", {"FY2026": -51793, "FY2025": -3739, "FY2024": -204865, "FY2023": 3238, "FY2022": 1127}),
        ("Net cash outflow from financing activities", {"FY2026": -309484, "FY2025": -314107, "FY2024": -9485, "FY2023": -158299, "FY2022": -77054}),
        ("Cash and cash equivalents at the end of the year", {"FY2026": 3973773, "FY2025": 5051552, "FY2024": 6332409, "FY2023": 6287746, "FY2022": 6841039}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2026": "13.3%", "FY2025": "13.6%", "FY2024": "13.3%", "FY2023": "12.7%", "FY2022": "12.0%"}),
        ("Tier 1 Ratio", {"FY2026": "15.0%", "FY2025": "15.4%", "FY2024": "15.9%", "FY2023": "14.1%", "FY2022": "13.6%"}),
        ("Total Capital Ratio", {"FY2026": "18.6%", "FY2025": "19.2%", "FY2024": "19.8%", "FY2023": "18.5%", "FY2022": "18.2%"}),
        ("Leverage Ratio", {"FY2026": "9.5%", "FY2025": "10.5%", "FY2024": "10.7%", "FY2023": "9.8%", "FY2022": "9.3%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. LCR and NSFR are omitted from this chart — not publicly "
         "disclosed at the IBP solo-entity level in the sourced filings; see the LCR/NSFR sheets for detail.",
)

bw.save("/Users/armaan/code/katalysis/banks/INVESTEC BANK PLC FINANCIALS.xlsx")
