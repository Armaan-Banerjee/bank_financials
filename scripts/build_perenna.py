import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Perenna Bank PLC (Companies House 13084174, PRA FRN 956138) was incorporated
# as Perenna FFL PLC and renamed on 30 September 2022.  The five available
# year-end filings are 31 December 2021-2025.  The 2021-2023 filings are
# company-only accounts; the 2024-2025 filings include consolidated statements
# and the workbook uses those consolidated cash flows for the two later years.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/13084174/filing-history/MzUyNTM5NTkxM2FkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/13084174/filing-history/MzQ3MjEwNTk2M2FkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/13084174/filing-history/MzQyNTQzMzk4MGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/13084174/filing-history/MzM4MjAzMDY1OWFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/13084174/filing-history/MzM1MTg2MDczOWFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: Perenna Bank PLC (Companies House 13084174; PRA FRN 956138) was incorporated as "
    "Perenna FFL PLC and changed its legal name on 30 September 2022. This is the same legal entity, "
    "not a substituted group or predecessor. It received a restricted banking licence in August 2022 "
    "and a full banking licence in 2023. FY2021-FY2023 are company-only accounts; FY2024-FY2025 also "
    "present consolidated Group accounts, and the consolidated cash-flow statement is used for those "
    "years. All figures below are in pounds (£), as reported."
)

DATA_QUALITY_NOTE = (
    "DATA QUALITY NOTE: The FY2024 and FY2025 reports contain an internal presentation/arithmetic "
    "inconsistency in the intermediate operating-cash subtotal labelled 'Cash used in operations'. "
    "The final reported net operating cash totals do reconcile to the full preceding line-item chain, "
    "so the intermediate subtotal is omitted rather than double-counted; all underlying line items and "
    "the final reported totals are transcribed as printed. FY2024's final net operating total is "
    "(£51,800,587), while FY2025's is (£62,911,585)."
)

CASH_FLOW_SOURCES = (
    "Sources - FY2021-FY2023 are Perenna Bank PLC's own company-only Statement of Cash Flows; "
    "FY2024-FY2025 are the consolidated Group Statement of Cash Flows:\n"
    f"FY2025: Group Annual Report and Financial Statements 2025, p.29-30 (Consolidated Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2024: Group Annual Report and Financial Statements 2024, p.32-33 (Consolidated Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.33-34 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.30-31 (Statement of Cash Flows; 2021 comparative is restated) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.14 (Statement of Cash Flows) - {AR2021_URL}\n"
    + ENTITY_NOTE + "\n\n" + DATA_QUALITY_NOTE
)


def p3_sources():
    return (
        "Sources - Perenna Bank PLC regulatory/key-metric disclosures:\n"
        f"FY2025 & FY2024: Group Annual Report and Financial Statements 2025, p.1 (Key Performance Indicators; "
        f"2025 and 2024 comparative) - {AR2025_URL}\n"
        f"FY2023 & FY2022: Annual Report and Financial Statements 2023, p.3 (Key performance indicators; "
        f"2023 and 2022 comparative) - {AR2023_URL}\n"
        "No separate Perenna Pillar 3/KM1 disclosure was located on the Bank's website or in its Companies "
        "House filings. The Annual Reports disclose only CET1 ratio and leverage ratio as named key metrics; "
        "the other fixed workbook metrics are therefore left explicitly not publicly disclosed.\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Perenna Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="0F5B78")

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Loss for the year/period", {"FY2025": -18291515, "FY2024": -18321432, "FY2023": -15409172, "FY2022": -10396474, "FY2021": -5797708}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": 55644, "FY2024": 82462, "FY2023": 64899, "FY2022": 43771, "FY2021": 14212}),
    ("DATA", "Amortisation of intangible fixed assets", {"FY2025": 826967, "FY2024": 926543, "FY2023": 226638, "FY2022": 10946}),
    ("DATA", "Impairment losses on intangible assets", {"FY2025": 643093, "FY2023": 18000}),
    ("DATA", "Interest received", {"FY2025": -555881, "FY2024": -28237}),
    ("DATA", "Interest paid", {"FY2025": 2796060, "FY2024": 445826}),
    ("DATA", "Fair value losses/(gain)", {"FY2025": 1254779, "FY2024": 10467, "FY2023": -7778, "FY2022": 13541}),
    ("DATA", "Investment income", {"FY2025": -199630, "FY2024": -618090, "FY2023": -386793, "FY2022": -93422}),
    ("DATA", "Investment income received", {"FY2022": 20529}),
    ("DATA", "Share-based payment expense", {"FY2024": 1291536, "FY2023": 2471965, "FY2022": 207333}),
    ("DATA", "Corporation tax charge", {"FY2025": 300, "FY2024": 175}),
    ("DATA", "Corporation tax paid", {"FY2025": -175}),
    ("DATA", "Impairment loss on loans and advances to customers", {"FY2024": 29621, "FY2023": 108}),
    ("DATA", "(Increase)/decrease in debtors", {"FY2021": -136084}),
    ("DATA", "Increase in creditors", {"FY2021": 581228}),
    ("DATA", "Increase in amounts owed to group companies", {"FY2021": 6853569}),
    ("DATA", "Increase in prepayments, accrued income and other assets", {"FY2025": -268941, "FY2024": -530597, "FY2023": -401076}),
    ("DATA", "Increase in trade and other payables", {"FY2025": 4535562, "FY2024": 105671, "FY2023": 1235718, "FY2022": 699493}),
    ("DATA", "Increase in loans and advances to customers", {"FY2025": -50911788, "FY2024": -34748706, "FY2023": -108791}),
    ("DATA", "Interest paid (cash flow movement)", {"FY2025": -2796060, "FY2024": -445826}),
    ("DATA", "Increase in trade and other receivables", {"FY2022": -259705}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": -62911585, "FY2024": -51800587, "FY2023": -12296282, "FY2022": -9753988, "FY2021": 1515217}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchases of property, plant and equipment", {"FY2025": -15782, "FY2024": -31732, "FY2023": -93225, "FY2022": -87449, "FY2021": -84976}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -128734, "FY2024": -386881, "FY2023": -428546, "FY2022": -1044109, "FY2021": -1120614}),
    ("DATA", "Sale/(purchases) of available-for-sale financial assets", {"FY2025": 1177153, "FY2024": 26544961, "FY2023": -19094097}),
    ("DATA", "Purchases of FVTPL investments", {"FY2022": -12807189}),
    ("DATA", "Investment income cash flow on maturity", {"FY2022": -20529}),
    ("DATA", "Interest received", {"FY2025": 555881, "FY2024": 28237}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": 1588518, "FY2024": 26154585, "FY2023": -19615868, "FY2022": -13959276, "FY2021": -1205590}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of ordinary shares", {"FY2025": 112430, "FY2023": 19726, "FY2022": 20149, "FY2021": 50000}),
    ("DATA", "Issue of ordinary shares at a premium", {"FY2025": 11130582, "FY2023": 42830263, "FY2022": 24453854}),
    ("DATA", "Transaction cost for share issuance", {"FY2025": -45262, "FY2024": -10907, "FY2023": -194583, "FY2022": -207333}),
    ("DATA", "Proceeds from loans and borrowings", {"FY2025": 54933000, "FY2024": 24650000}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": 66130750, "FY2024": 24639093, "FY2023": 42655406, "FY2022": 24266670, "FY2021": 50000}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 4807683, "FY2024": -1006909, "FY2023": 10743256, "FY2022": 553406, "FY2021": 359627}),
    ("DATA", "Cash and cash equivalents at the beginning of year/period", {"FY2025": 10649380, "FY2024": 11656289, "FY2023": 913033, "FY2022": 359627}),
    ("TOTAL", "Cash and cash equivalents at the end of year/period", {"FY2025": 15457063, "FY2024": 10649380, "FY2023": 11656289, "FY2022": 913033, "FY2021": 359627}),
]

bw.add_cash_flow_sheet(
    title="Perenna Bank PLC — Statement of Cash Flows",
    subtitle="FY2021-FY2023 company-only; FY2024-FY2025 consolidated Group basis; £; see source and data-quality notes",
    rows=rows, sources_text=CASH_FLOW_SOURCES, first_col_width=70, source_height=250, unit_suffix=" (£)",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=170)


metric("CET1 Capital", None, [("CET1 capital", {y: "Not publicly disclosed" for y in YEARS})])
metric("CET1 Ratio", "%", [("CET1 ratio", {"FY2025": "48%", "FY2024": "133%", "FY2023": "269%", "FY2022": "101.66%"})],
       note="The Annual Reports disclose this ratio as a Key Performance Indicator, but do not provide a separate Pillar 3/KM1 capital amount. No FY2021 ratio is disclosed.")
metric("Tier 1 Capital", None, [("Tier 1 capital", {y: "Not publicly disclosed" for y in YEARS})])
metric("Tier 1 Ratio", None, [("Tier 1 ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("Total Capital", None, [("Total capital", {y: "Not publicly disclosed" for y in YEARS})])
metric("Total Capital Ratio", None, [("Total capital ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("Total RWAs", None, [("Total risk-weighted assets", {y: "Not publicly disclosed" for y in YEARS})])
metric("Leverage Ratio", "%", [("Leverage ratio", {"FY2025": "21.47%", "FY2024": "46.38%", "FY2023": "91.97%", "FY2022": "91.05%"})],
       note="The Annual Reports disclose this ratio as a Key Performance Indicator. No FY2021 ratio is disclosed.")
metric("LCR", None, [("Liquidity coverage ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("NSFR", None, [("Net stable funding ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})])

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -62911585, "FY2024": -51800587, "FY2023": -12296282, "FY2022": -9753988, "FY2021": 1515217}),
        ("Net cash from/(used in) investing activities", {"FY2025": 1588518, "FY2024": 26154585, "FY2023": -19615868, "FY2022": -13959276, "FY2021": -1205590}),
        ("Net cash from/(used in) financing activities", {"FY2025": 66130750, "FY2024": 24639093, "FY2023": 42655406, "FY2022": 24266670, "FY2021": 50000}),
        ("Cash and cash equivalents at end of year/period", {"FY2025": 15457063, "FY2024": 10649380, "FY2023": 11656289, "FY2022": 913033, "FY2021": 359627}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2025": "48%", "FY2024": "133%", "FY2023": "269%", "FY2022": "101.66%"}),
        ("Leverage Ratio", {"FY2025": "21.47%", "FY2024": "46.38%", "FY2023": "91.97%", "FY2022": "91.05%"}),
    ],
    note="The ratio figures are the Annual Reports' named Key Performance Indicators, not a substitute Pillar 3/KM1 dataset. No FY2021 ratio was disclosed; other fixed workbook metrics are explicitly not publicly disclosed.",
)

bw.save("/Users/armaan/code/katalysis/banks/PERENNA FINANCIALS.xlsx")
