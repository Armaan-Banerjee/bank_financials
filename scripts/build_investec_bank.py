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
# Sheet 1: Cash Flow Statement
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

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Leverage exposure measure (£m)", {"FY2026": 31774, "FY2025": 27906, "FY2024": 26746, "FY2023": 24945, "FY2022": 23874}),
        ("Leverage ratio (%)", {"FY2026": "9.5%", "FY2025": "10.5%", "FY2024": "10.7%", "FY2023": "9.8%", "FY2022": "9.3%"}),
    ],
    p3_sources(280, 287, 270, "A summary of capital adequacy and leverage ratios"),
)

metric(
    "LCR", None,
    [("Liquidity Coverage Ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(280, 287, 270),
    note="IBP's Annual Financial Statements discuss the liquidity buffer and funding strategy qualitatively (see "
         "'Balance sheet risk' / 'Liquidity risk' notes) but do not publish a numeric LCR% for the solo entity. "
         "The statements note that full Pillar 3 disclosures for Investec plc and IBP are published in a standalone "
         "disclosure report on the Investec Group's website (with a subset in an 'Appendix A' of this report); that "
         "standalone report was not reachable this session — Investec's own site returned HTTP 403 to automated "
         "fetches and no Wayback Machine snapshot was found, and the Appendix A referenced was not located within "
         "the Companies House filing copies used as the primary source.",
)

metric(
    "NSFR", None,
    [("Net Stable Funding Ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(280, 287, 270),
    note="Same availability constraint as the LCR sheet — no numeric NSFR% found in the Companies House filing "
         "copies of IBP's Annual Financial Statements for any of the 5 years; the standalone Pillar 3 report "
         "referenced by those statements was not reachable this session.",
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
