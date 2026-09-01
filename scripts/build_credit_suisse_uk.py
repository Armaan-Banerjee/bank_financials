import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzUxNzE0OTI3NGFkaXF6a2N4/document?format=pdf&download=0")
AR2023_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzQxOTY5NDQ0MWFkaXF6a2N4/document?format=pdf&download=0")
AR2021_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzMzNzU0NDMwOWFkaXF6a2N4/document?format=pdf&download=0")

ENTITY_NOTE = (
    "Credit Suisse (UK) Limited ('CSUK', company 02009520, FRN 124269) - a UK private-banking/wealth-"
    "management subsidiary. Ultimate parent is UBS Group AG following UBS's acquisition of Credit Suisse "
    "Group (announced March 2023, completed June 2023) - CSUK itself remains an active, separately-"
    "reporting PRA entity throughout, still filing under its original name as of the FY2025 filing (Apr "
    "2026). All 5 Companies House filings were fully scanned/image-only, transcribed via page rendering.\n\n"
    "TWO MAJOR DISCLOSED BUSINESS EVENTS, both flagged rather than treated as anomalies:\n"
    "(1) FY2023: a pre-tax loss of £26.2m driven by £44.8m of UBS-acquisition-related expenses "
    "(accelerated lease costs, intangibles impairment, recharged transaction costs) - underlying "
    "profit before tax (excluding these) was £18.6m.\n"
    "(2) FY2025: on 20 June 2025 CSUK completed a Part VII business transfer (Financial Services and "
    "Markets Act 2000) of most of its wealth-management clients to UBS AG London Branch, following a "
    "Business Transfer Agreement signed 20 December 2024. This shows up directly in the FY2025 cash flow "
    "statement as a £539,843k 'Cash receipt from business transfer' investing-activities line and a "
    "£1,278k 'Loss from the business transfer' operating-activities adjustment, and drove RWAs down from "
    "£672m (FY2024) to £160m (FY2025) and CET1/leverage ratios sharply higher (smaller balance sheet, "
    "same capital base). CSUK's remaining business post-transfer is the limited-scope Credit Suisse "
    "London Nominees ('CSLN') hedge-fund sub-custody activity.\n\n"
    "Full opening-to-closing cash bridge ties across all 5 years, with two small immaterial gaps in the "
    "source documents' own printed figures, neither force-corrected: FY2022 closing £475,709k vs FY2023 "
    "opening £475,664k (£45k gap, explicitly explained by the FY2023 report's own footnote as the "
    "year-over-year change in the ECL allowance excluded from the cash figure); and FY2023's own three-line "
    "tail (opening £475,664k + net increase £97,529k - FX effect £24,570k = £548,623k) doesn't quite match "
    "FY2023's own printed closing balance of £548,659k (a £36k gap, source unexplained, not present in any "
    "other year - kept exactly as printed on both sides rather than adjusted to force a match). FY2021 "
    "closing £408,082k = FY2022 opening exactly; FY2023 closing £548,659k = FY2024 opening exactly; FY2024 "
    "closing £341,768k = FY2025 opening exactly."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Credit Suisse (UK) Limited's own Statement of Cash Flows:\n"
    "FY2025: Full accounts to 31 Dec 2025 (Companies House, filed 25 Apr 2026), "
    "Statement of Cash Flows p.47 - " + AR2025_URL + "\n"
    "FY2024: same FY2025 filing's own FY2024 comparative column, p.47\n"
    "FY2023: Full accounts to 31 Dec 2023 (Companies House, filed 27 Apr 2024), "
    "Statement of Cash Flows p.41 - " + AR2023_URL + "\n"
    "FY2022: same FY2023 filing's own FY2022 comparative column, p.41\n"
    "FY2021: Full accounts to 31 Dec 2021 (Companies House, filed 28 Apr 2022), "
    "Statement of Cash Flows p.46 - " + AR2021_URL + "\n\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(bank_name="Credit Suisse (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="50B633")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax for the year",
     {"FY2025": 9803, "FY2024": 10804, "FY2023": -26199, "FY2022": 21421, "FY2021": 10907}),
    ("DATA", "Loss from the business transfer", {"FY2025": 1278}),
    ("DATA", "Amortisation and impairment of intangible assets",
     {"FY2024": 1137, "FY2023": 13582, "FY2022": 3566, "FY2021": 1852}),
    ("DATA", "Impairment on goodwill", {"FY2021": 13752}),
    ("DATA", "Accrued interest on long term debt",
     {"FY2025": 1836, "FY2024": 14677, "FY2023": 34049, "FY2022": 12300, "FY2021": 1635}),
    ("DATA", "Accrued interest on short-term borrowings",
     {"FY2025": 12765, "FY2024": 40087, "FY2023": 44712, "FY2022": 8822}),
    ("DATA", "Deferred fee income on loans",
     {"FY2025": -499, "FY2024": -2784, "FY2023": -3102, "FY2022": -3821}),
    ("DATA", "Foreign exchange (gain)/loss",
     {"FY2025": -2005, "FY2024": -1583, "FY2023": 1721, "FY2022": -2954, "FY2021": -1339}),
    ("DATA", "Share based Compensation (charge)/reversal",
     {"FY2024": -385, "FY2023": 394, "FY2022": -40}),
    ("DATA", "Allowance for expected credit losses (ECL)",
     {"FY2025": -489, "FY2024": 1526, "FY2023": 3094, "FY2022": 1754, "FY2021": -2571}),
    ("TOTAL", "Cash generated before changes in operating assets and liabilities",
     {"FY2025": 22689, "FY2024": 63479, "FY2023": 68251, "FY2022": 41048, "FY2021": 24236}),
    ("DATA", "Securities purchased under resale agreements",
     {"FY2025": 237260, "FY2024": -110148, "FY2023": 106208, "FY2022": 486194, "FY2021": -167802}),
    ("DATA", "Trading financial assets mandatorily at fair value through profit or loss",
     {"FY2025": 13944, "FY2024": -314, "FY2023": 5183, "FY2022": -4480, "FY2021": 20813}),
    ("DATA", "Loans and advances",
     {"FY2025": -39272, "FY2024": 489850, "FY2023": 398930, "FY2022": 336715, "FY2021": -48586}),
    ("DATA", "Interest bearing deposits with banks (excluding ECL)",
     {"FY2025": 25338, "FY2024": -8136, "FY2023": 31552, "FY2022": -48754, "FY2021": 187491}),
    ("DATA", "Other assets",
     {"FY2025": 17904, "FY2024": 13274, "FY2023": 8322, "FY2022": -8451, "FY2021": -1141}),
    ("TOTAL", "Net decrease/(increase) in operating assets",
     {"FY2025": 255174, "FY2024": 384526, "FY2023": 550195, "FY2022": 761224, "FY2021": -9225}),
    ("DATA", "Deposits",
     {"FY2025": -195682, "FY2024": -106841, "FY2023": -439790, "FY2022": -517522, "FY2021": -64484}),
    ("DATA", "Trading financial liabilities mandatorily at fair value through profit or loss",
     {"FY2025": -13849, "FY2024": 353, "FY2023": -5117, "FY2022": 4590, "FY2021": -20917}),
    ("DATA", "Share based compensation", {"FY2024": -220, "FY2023": -1774, "FY2022": -3649}),
    ("DATA", "Other liabilities and provisions",
     {"FY2025": -14841, "FY2024": -15915, "FY2023": 11963, "FY2022": 1266, "FY2021": -2672}),
    ("TOTAL", "Net decrease/(increase) in operating liabilities",
     {"FY2025": -224372, "FY2024": -122623, "FY2023": -434718, "FY2022": -515315, "FY2021": -88073}),
    ("DATA", "Income tax refunded/(paid)", {"FY2024": 119, "FY2021": 1101}),
    ("DATA", "Group relief received/(paid)",
     {"FY2025": 6127, "FY2024": -4800, "FY2023": -3319, "FY2022": -2522, "FY2021": 406}),
    ("TOTAL", "Net cash flow generated from/(used in) operating activities",
     {"FY2025": 59618, "FY2024": 320701, "FY2023": 180409, "FY2022": 284435, "FY2021": -71555}),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Cash receipt from business transfer", {"FY2025": 539843}),
    ("DATA", "Capital expenditures for intangible assets",
     {"FY2023": -786, "FY2022": -3455, "FY2021": -3799}),
    ("TOTAL", "Net cash flow generated from/(used in) investing activities",
     {"FY2025": 539843, "FY2024": 0, "FY2023": -786, "FY2022": -3455, "FY2021": -3799}),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividend paid", {"FY2023": -30000, "FY2022": -20000}),
    ("DATA", "Interest paid on long term debt",
     {"FY2025": -1916, "FY2024": -15460, "FY2023": -33420, "FY2022": -12293, "FY2021": -1620}),
    ("DATA", "Issuance of long term debt", {"FY2023": 530803, "FY2022": 500000}),
    ("DATA", "Repayment of long term debt",
     {"FY2025": -55000, "FY2024": -500000, "FY2023": -532693, "FY2022": -503689}),
    ("DATA", "Interest paid on short-term borrowings",
     {"FY2025": -17039, "FY2024": -39775, "FY2023": -43476, "FY2022": -6928}),
    ("DATA", "Issuance of short-term borrowings",
     {"FY2025": 12865, "FY2024": 713897, "FY2023": 601802, "FY2022": 615993}),
    ("DATA", "Repayment of short-term borrowings",
     {"FY2025": -845507, "FY2024": -689448, "FY2023": -575110, "FY2022": -824808}),
    ("TOTAL", "Net cash flow used in financing activities",
     {"FY2025": -906597, "FY2024": -530786, "FY2023": -82094, "FY2022": -251725, "FY2021": -1620}),

    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents",
     {"FY2025": -307136, "FY2024": -210085, "FY2023": 97529, "FY2022": 29255, "FY2021": -76974}),
    ("DATA", "Cash and cash equivalents at the beginning of the year",
     {"FY2025": 341768, "FY2024": 548659, "FY2023": 475664, "FY2022": 408082, "FY2021": 483717}),
    ("DATA", "Effect of exchange rate fluctuations on cash and cash equivalents",
     {"FY2025": -12923, "FY2024": 3194, "FY2023": -24570, "FY2022": 38372, "FY2021": 1339}),
    ("TOTAL", "Cash and cash equivalents at the end of the year",
     {"FY2025": 21709, "FY2024": 341768, "FY2023": 548659, "FY2022": 475709, "FY2021": 408082}),
]

bw.add_cash_flow_sheet(
    title="Credit Suisse (UK) Limited — Statement of Cash Flows",
    subtitle="Entity basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=88,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


def p3_sources(page_note=""):
    return (
        "Sources - Credit Suisse (UK) Limited's own Annual Report 'Key Performance Indicators (KPIs)' "
        "table (no standalone Pillar 3 document was located for CSUK; the FY2025 Annual Report's own "
        "Strategic Report states 'Pillar 3 disclosures can be found separately at "
        "https://www.ubs.com/global/en/investor-relations', but a CSUK-specific document was not "
        "identified there within budget - WebSearch quota was already exhausted):\n"
        "FY2025/FY2024: FY2025 Annual Report, KPI table p.6 - " + AR2025_URL + "\n"
        "FY2023/FY2022: FY2023 Annual Report, KPI table p.7 - " + AR2023_URL + "\n"
        "FY2021: FY2021 Annual Report, KPI table p.8 - " + AR2021_URL + "\n"
        + page_note
    )


CET1_TIER1_CAPITAL = {"FY2025": 306, "FY2024": 299, "FY2023": 291, "FY2022": 330, "FY2021": 336}
CET1_TIER1_RATIO = {"FY2025": "191%", "FY2024": "45%", "FY2023": "29.15%", "FY2022": "29.39%", "FY2021": "25.09%"}
RWA = {"FY2025": 160, "FY2024": 672, "FY2023": 1000, "FY2022": 1124, "FY2021": 1340}
LEVERAGE_RATIO = {"FY2025": "87%", "FY2024": "17%"}
LCR = {"FY2025": "1,154%", "FY2024": "451%", "FY2023": "554.67%", "FY2022": "216.40%"}
NSFR = {"FY2025": "3,600%", "FY2024": "167%", "FY2023": "129.25%", "FY2022": "131.72%"}

COMBINED_NOTE = (
    "The Bank's own KPI table discloses a single combined 'Tier 1 and Common Equity Tier 1 (CET1)' "
    "line, not separate Tier 1/CET1 figures - used identically for both the CET1 and Tier 1 sheets."
)

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital (combined with Tier 1)", CET1_TIER1_CAPITAL)],
       p3_sources(), note=COMBINED_NOTE)
metric("CET1 Ratio", "%", [("CET1 Ratio (combined with Tier 1)", CET1_TIER1_RATIO)], p3_sources(), note=COMBINED_NOTE)
metric("Tier 1 Capital", "£m", [("Tier 1 Capital (combined with CET1)", CET1_TIER1_CAPITAL)], p3_sources(), note=COMBINED_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 Ratio (combined with CET1)", CET1_TIER1_RATIO)], p3_sources(), note=COMBINED_NOTE)

TOTAL_CAPITAL_NOTE = (
    "Not directly disclosed as a separate figure in any of the 5 years' KPI tables - only a combined "
    "'Tier 1 and CET1' figure is given, with no mention of AT1 or Tier 2 instruments anywhere. NOT "
    "assumed equal to Tier 1/CET1 without an explicit statement to that effect, per project convention - "
    "left blank rather than guessed."
)
bw.add_not_disclosed_metric_sheets(
    ["Total Capital", "Total Capital Ratio"], p3_sources(),
    per_note={"Total Capital": TOTAL_CAPITAL_NOTE, "Total Capital Ratio": TOTAL_CAPITAL_NOTE},
)

metric("Total RWAs", "£m", [("Risk Weighted Assets (RWA)", RWA)], p3_sources())

metric("Leverage Ratio", "%", [("Leverage Ratio", LEVERAGE_RATIO)], p3_sources(
    "\nLeverage Ratio only appears in the KPI table format used from the FY2025 Annual Report onward - "
    "FY2023/FY2022/FY2021's KPI tables (an earlier format) don't include this metric at all, confirmed "
    "genuinely absent rather than omitted by search."))

metric("LCR", "%", [("Liquidity Coverage Ratio (LCR)", LCR)], p3_sources(
    "\nFY2021's KPI table (earliest format) discloses only a 'Liquidity Buffer (£m)' figure, no LCR% - "
    "confirmed genuinely absent for that year, not omitted by search."))

metric("NSFR", "%", [("Net Stable Funding Ratio (NSFR)", NSFR)], p3_sources(
    "\nFY2021's KPI table (earliest format) discloses only a 'Liquidity Buffer (£m)' figure, no NSFR% - "
    "confirmed genuinely absent for that year, not omitted by search."))

MREL_NOTE = (
    "Not disclosed anywhere in the 3 Annual Reports reviewed, no exemption stated. Plausibly below the "
    "Bank of England's MREL threshold given CSUK's small and (post-Part-VII-transfer) shrinking balance "
    "sheet, but not confirmed - left blank rather than guessed."
)
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": MREL_NOTE})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flow generated from/(used in) operating activities",
         {"FY2025": 59618, "FY2024": 320701, "FY2023": 180409, "FY2022": 284435, "FY2021": -71555}),
        ("Net cash flow generated from/(used in) investing activities",
         {"FY2025": 539843, "FY2024": 0, "FY2023": -786, "FY2022": -3455, "FY2021": -3799}),
        ("Net cash flow used in financing activities",
         {"FY2025": -906597, "FY2024": -530786, "FY2023": -82094, "FY2022": -251725, "FY2021": -1620}),
        ("Cash and cash equivalents at the end of the year",
         {"FY2025": 21709, "FY2024": 341768, "FY2023": 548659, "FY2022": 475709, "FY2021": 408082}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1/Tier 1 Ratio", CET1_TIER1_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="FY2025's cash flow figures reflect a major one-off event: the 20 June 2025 Part VII transfer of "
         "most of CSUK's business to UBS AG London Branch (a £539,843k cash receipt in investing "
         "activities), which also drove RWAs and capital ratios sharply post-transfer. See the Cash Flow "
         "Statement sheet's source note for detail. Figures are duplicated from the detail sheets for "
         "at-a-glance trend viewing.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CREDIT SUISSE UK FINANCIALS.xlsx")
