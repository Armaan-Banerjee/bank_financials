import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, y/e 31 Dec
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://assets.gatehousebank.com/production/downloads/Gatehouse-Bank-Annual-Report-2025.pdf"
AR2023_URL = "https://gatehousebank.com/downloads/gatehouse-bank-annual-report-2023"
AR2022_URL = "https://gatehousebank.com/downloads/gatehouse-bank-annual-report-2022"
AR2021_URL = "https://assets.gatehousebank.com/production/downloads/Gatehouse-Bank-Annual-Report-2021-FINAL-web.pdf"
P3_2024_URL = "https://assets.gatehousebank.com/production/downloads/Gatehouse-Bank-Pillar-III-Disclosure-2024-FINAL.pdf"
P3_2023_URL = "https://assets.gatehousebank.com/production/downloads/Gatehouse-Bank-Pillar-III-Disclosure-2023-FINAL.pdf"
P3_2022_URL = "https://gatehousebank.com/downloads/gatehouse-bank-pillar-3-disclosure-2022"
P3_2021_URL = "https://assets.gatehousebank.com/production/downloads/Gatehouse-Bank-Pillar-III-Disclosure-2021-FINAL_2022-08-23-154942_nofu.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Gatehouse Bank Plc (FRN 475346, company 06260053) is a UK Shariah-compliant "
    "(Islamic) bank - 'profit paid/received' in the cash flow statement is the functional equivalent "
    "of conventional interest paid/received, and financing/advances line items are Shariah-compliant "
    "structures (Wakala, Murabaha, ijara) presented here as the standard cash flow line items they "
    "represent. Figures are the Bank's own Consolidated Statement of Cash Flows from its Companies "
    "House 'Group of companies' accounts' filings.\n\n"
    "GENUINE MID-SERIES PRESENTATION CHANGE across 3 distinct eras, each kept on its own "
    "originally-published line items (blank cells where a line doesn't apply that year, not a gap): "
    "FY2021 (single combined profit line, no separate cash-tax-paid line); FY2022-FY2023 (profit "
    "split continuing/discontinued, 'Share in profit of associate' adjustment, cash tax paid shown "
    "separately within the operating-liabilities block); FY2024-FY2025 (adds Held-For-Sale "
    "adjustment/asset lines and an 'Intercompany payable receivable' line reflecting a disclosed "
    "business restructuring, and introduces a 'Cash generated from operations' subtotal not shown in "
    "earlier years). The 'Fair value movement in financial instruments held at FVTIS (derivative "
    "financial instruments)' caption is used TWICE within the same year's own statement - once as a "
    "non-cash P&L adjustment, once under operating-asset movements - kept as two distinct rows per "
    "the source, not a duplicate.\n\n"
    "FY2021 RESTATEMENT: the FY2022 Annual Report's own FY2021 comparative column reclassifies "
    "several FY2021 operating/investing line items (e.g. splits continuing/discontinued profit "
    "differently, renames 'Net investment in financial assets held at FVTIS/FVTOCI' into the "
    "derivative-FVTIS captions used from FY2022 onward) versus FY2021's own originally-published "
    "Annual Report. The two vintages' Net cash flow from operating/investing activities totals differ "
    "(12,357/17,325 as originally published vs 12,643/17,039 restated) but their SUM and the overall "
    "net cash movement (28,958) are identical in both - a pure reclassification between sections, not "
    "a value correction (the same pattern seen at FCE Bank Plc in this project). FY2021's own "
    "originally-published Annual Report figures are used here, consistent with every other year using "
    "its own primary source rather than a later restated comparative.\n\n"
    "Full opening-to-closing cash balance chain (including the separately-disclosed FX effect on cash) "
    "ties exactly across all 5 years."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Gatehouse Bank Plc's own Consolidated Statement of Cash Flows:\n"
    f"FY2025/FY2024: Annual Report and Financial Statements 2025, p.60-61 (Consolidated Statement of "
    f"Cash Flows) - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Financial Statements 2023, p.64-65 (Consolidated Statement of "
    f"Cash Flows) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.52 (Consolidated Statement of Cash Flows, "
    f"own originally-published FY2021 column - see ENTITY NOTE on the later FY2022 report's restated "
    f"comparative) - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources(page, extra=""):
    return (
        f"Sources - Gatehouse Bank Plc Pillar 3 disclosures, Article 447 Key Metrics table, p.{page}:\n"
        f"FY2024: Pillar III Disclosure 2024 (Dec-24 column) - {P3_2024_URL}\n"
        f"FY2023: Pillar III Disclosure 2023 (Dec-23 column) - {P3_2023_URL}\n"
        f"FY2022: Pillar III Disclosure 2022 (Dec-22 column, own year's disclosure - see restatement "
        f"note) - {P3_2022_URL}\n"
        f"FY2021: Annual Report and Financial Statements 2021, s.5 Capital Resources, p.11 (own "
        f"year-end capital resources note, cross-validated against the 2022 Pillar 3 disclosure's "
        f"Dec-21 comparative column) - {AR2021_URL}\n"
        f"FY2025: not yet published as at build date - Pillar 3 disclosures are typically published "
        f"some months after the Annual Report; left blank rather than guessed.\n"
        f"RESTATEMENT NOTE: the FY2023 Pillar 3 disclosure's own Dec-22 comparative column shows CET1 "
        f"capital of GBP98.0m / RWA of GBP579.1m / ratios of 16.9%/16.9%/18.5% / leverage 7.1% - "
        f"different from the FY2022 disclosure's own Dec-22 ('T') figures used here (GBP103.2m / "
        f"GBP594.7m / 17.4%/17.4%/18.9% / 7.5%). LCR and NSFR at Dec-22 match exactly between both "
        f"vintages (350.7% and 150.6%), so only the capital-side figures were later restated. Each "
        f"year's own primary disclosure is used throughout, consistent with the rest of this workbook."
        + extra
    )


bw = BankWorkbook(bank_name="Gatehouse Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="76773E")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) after tax from continuing operations",
     {"FY2025": -13291, "FY2024": -1248, "FY2023": 3157, "FY2022": 6488}),
    ("DATA", "Profit after tax from discontinued operations",
     {"FY2025": 1924, "FY2024": 5048, "FY2023": 0, "FY2022": 1640}),
    ("DATA", "Operating profit on ordinary activities after tax (combined, not split this year)",
     {"FY2021": 3464}),
    ("TOTAL", "Profit/(loss) after tax for the year",
     {"FY2025": -11367, "FY2024": 3800, "FY2023": 3157, "FY2022": 8128, "FY2021": 3464}),
    ("DATA", "Depreciation and amortisation",
     {"FY2025": 1043, "FY2024": 930, "FY2023": 1302, "FY2022": 1319, "FY2021": 1222}),
    ("DATA", "Impairment charge/(release)",
     {"FY2025": 2725, "FY2024": -192, "FY2023": 847, "FY2022": 5714, "FY2021": 806}),
    ("DATA", "(Negative)/positive revaluation of financial instruments held at FVTIS (unquoted investments)",
     {"FY2025": 207, "FY2024": -1969, "FY2023": -22, "FY2022": -2904, "FY2021": 210}),
    ("DATA", "Positive revaluation on investment properties", {"FY2021": -1412}),
    ("DATA", "Loss/(gain) on sale of property held for sale", {"FY2021": 472}),
    ("DATA", "Share in profit of associate", {"FY2023": 0, "FY2022": -1640, "FY2021": -904}),
    ("DATA", "Fair value movement in derivative financial instruments (non-cash adjustment)",
     {"FY2025": 1844, "FY2024": 341, "FY2023": -1083, "FY2022": -1634, "FY2021": 160}),
    ("DATA", "Foreign exchange (gains)/losses",
     {"FY2025": -321, "FY2024": -120, "FY2023": 145, "FY2022": -264, "FY2021": 461}),
    ("DATA", "Taxation/income tax expense (non-cash adjustment)",
     {"FY2025": -1947, "FY2024": -2167, "FY2023": -4, "FY2022": -3933, "FY2021": 153}),
    ("DATA", "Adjustment for assets/liabilities held for sale", {"FY2025": 3134, "FY2024": 3148}),
    ("DATA", "Net (increase)/decrease in other assets",
     {"FY2025": -30867, "FY2024": -964, "FY2023": -1712, "FY2022": 3007, "FY2021": -1816}),
    ("DATA", "Changes in financing and advances at amortised cost",
     {"FY2025": 52974, "FY2024": 36152, "FY2023": -130754, "FY2022": -332498, "FY2021": -199760}),
    ("DATA", "Fair value movement in derivative financial instruments (operating assets)",
     {"FY2025": -8196, "FY2024": -4080, "FY2023": -14824, "FY2022": 26558}),
    ("DATA", "Net investment in financial assets held at FVTIS", {"FY2021": 8683}),
    ("DATA", "Net investment in financial assets held at FVTOCI", {"FY2021": -286}),
    ("DATA", "Changes in assets and liabilities held for sale", {"FY2025": -4183, "FY2024": -3876}),
    ("DATA", "Intercompany payable/receivable", {"FY2025": 51, "FY2024": 0}),
    ("DATA", "Changes in financial liabilities measured at amortised cost",
     {"FY2025": -2094, "FY2024": -27632, "FY2023": -148024, "FY2022": 263503, "FY2021": 196339}),
    ("DATA", "Net increase/(decrease) in other liabilities",
     {"FY2025": 2578, "FY2024": -534, "FY2023": 156, "FY2022": -3953, "FY2021": 4565}),
    ("TOTAL", "Cash generated from operations", {"FY2025": 5581, "FY2024": 2837}),
    ("DATA", "Income tax paid (cash)",
     {"FY2025": -1506, "FY2024": -850, "FY2023": -592, "FY2022": -330}),
    ("TOTAL", "Net cash flow from/(used in) operating activities",
     {"FY2025": 4075, "FY2024": 1987, "FY2023": 4640, "FY2022": -38927, "FY2021": 12357}),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisitions of property, plant and equipment",
     {"FY2025": -278, "FY2024": -150, "FY2023": -416, "FY2022": -637, "FY2021": -632}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 57, "FY2024": 30}),
    ("DATA", "Acquisition of intangible assets",
     {"FY2025": -1535, "FY2024": -1057, "FY2023": -623, "FY2022": -878, "FY2021": -320}),
    ("DATA", "Purchases of financial assets held at FVOCI",
     {"FY2025": -14050, "FY2024": -15693, "FY2021": -17000}),
    ("DATA", "Proceeds from sale of financial assets held at FVTOCI",
     {"FY2025": 5098, "FY2024": 7254, "FY2023": 0, "FY2022": 2061, "FY2021": 11617}),
    ("DATA", "Purchase of financial assets held at FVTIS (unquoted investments)",
     {"FY2025": -143, "FY2024": -1775, "FY2023": -1195, "FY2022": -600}),
    ("DATA", "Held for sale investing activities", {"FY2025": -647, "FY2024": -1391}),
    ("DATA", "Proceeds from sale of financial assets held at FVTIS (unquoted investments)",
     {"FY2025": 4394, "FY2024": 14735, "FY2023": 0, "FY2022": 11468, "FY2021": 23238}),
    ("DATA", "Cash flow received from discontinued operations", {"FY2023": 0, "FY2022": 14253}),
    ("DATA", "Dividend received from associate", {"FY2021": 859}),
    ("DATA", "Investments in subsidiaries", {"FY2021": -437}),
    ("DATA", "Net proceeds from disposal of property held for sale",
     {"FY2023": 0, "FY2022": 4537, "FY2021": 0}),
    ("TOTAL", "Net cash flow from/(used in) investing activities",
     {"FY2025": -7104, "FY2024": 1953, "FY2023": -2234, "FY2022": 30204, "FY2021": 17325}),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Acquisition of subsidiaries", {"FY2023": 0, "FY2022": -9218}),
    ("DATA", "Cash outflow for lease liabilities",
     {"FY2025": -267, "FY2024": -401, "FY2023": -701, "FY2022": -672, "FY2021": -724}),
    ("DATA", "Held for sale financing activities", {"FY2025": -40, "FY2024": -296}),
    ("TOTAL", "Net cash flow from/(used in) financing activities",
     {"FY2025": -307, "FY2024": -697, "FY2023": -701, "FY2022": -9890, "FY2021": -724}),

    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents",
     {"FY2025": -3336, "FY2024": 3243, "FY2023": 1705, "FY2022": -18613, "FY2021": 28958}),
    ("DATA", "Cash and cash equivalents at beginning of year",
     {"FY2025": 27823, "FY2024": 24596, "FY2023": 22845, "FY2022": 41598, "FY2021": 12644}),
    ("DATA", "Effect of exchange rate fluctuations on cash held",
     {"FY2025": 112, "FY2024": -16, "FY2023": 46, "FY2022": -140, "FY2021": -4}),
    ("TOTAL", "Cash and cash equivalents at end of year",
     {"FY2025": 24599, "FY2024": 27823, "FY2023": 24596, "FY2022": 22845, "FY2021": 41598}),

    ("SECTION", "Additional information on operational cash flows from profit and dividends", {}),
    ("DATA", "Profit paid", {"FY2025": 48829, "FY2024": 53847, "FY2023": 23431, "FY2022": 14671}),
    ("DATA", "Profit received", {"FY2025": 65797, "FY2024": 65387, "FY2023": 55817, "FY2022": 43043}),
    ("DATA", "Dividend received", {"FY2025": 0, "FY2024": 659, "FY2023": 845, "FY2022": 844}),
]

bw.add_cash_flow_sheet(
    title="Gatehouse Bank Plc — Consolidated Cash Flow Statement",
    subtitle="Consolidated basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=88,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, page, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(page), note=note, first_col_width=48, source_height=260)


CET1_CAPITAL = {"FY2024": 108.6, "FY2023": 108.2, "FY2022": 103.2, "FY2021": 94.5}
TOTAL_CAPITAL = {"FY2024": 127.1, "FY2023": 126.7, "FY2022": 112.2, "FY2021": 103.5}
TOTAL_RWA = {"FY2024": 636.7, "FY2023": 644.8, "FY2022": 594.7, "FY2021": 523.0}
CET1_RATIO = {"FY2024": "17.1%", "FY2023": "16.8%", "FY2022": "17.4%", "FY2021": "18.1%"}
TOTAL_CAPITAL_RATIO = {"FY2024": "20.0%", "FY2023": "19.6%", "FY2022": "18.9%", "FY2021": "19.8%"}
LEVERAGE_RATIO = {"FY2024": "7.4%", "FY2023": "7.3%", "FY2022": "7.5%", "FY2021": "9.2%"}
LCR = {"FY2024": "447.6%", "FY2023": "691.6%", "FY2022": "350.7%", "FY2021": "365.4%"}
NSFR = {"FY2024": "153.5%", "FY2023": "151.1%", "FY2022": "150.6%"}

NO_AT1_NOTE = "No Additional Tier 1 or Tier 2 instruments disclosed any year - Tier 1 capital equals CET1 capital throughout."
NSFR_NOTE = "Not disclosed for FY2021 - the Article 447 Key Metrics NSFR rows first appear from the FY2022 Pillar 3 disclosure onward."

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)], "32")
metric("CET1 Ratio", "%", [("CET1 ratio", CET1_RATIO)], "32")
metric("Tier 1 Capital", "£m", [("Tier 1 capital", CET1_CAPITAL)], "32", note=NO_AT1_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CET1_RATIO)], "32", note=NO_AT1_NOTE)
metric("Total Capital", "£m", [("Total capital", TOTAL_CAPITAL)], "32")
metric("Total Capital Ratio", "%", [("Total capital ratio", TOTAL_CAPITAL_RATIO)], "32")
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", TOTAL_RWA)], "32")
metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", LEVERAGE_RATIO)], "32")
metric("LCR", "%", [("Liquidity coverage ratio", LCR)], "32")
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)], "32", note=NSFR_NOTE)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources("n/a"),
    per_note={"MREL Ratio": "Not publicly disclosed any year, no exemption stated - consistent with a "
                             "small deposit taker below MREL-setting thresholds."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flow from/(used in) operating activities",
         {"FY2025": 4075, "FY2024": 1987, "FY2023": 4640, "FY2022": -38927, "FY2021": 12357}),
        ("Net cash flow from/(used in) investing activities",
         {"FY2025": -7104, "FY2024": 1953, "FY2023": -2234, "FY2022": 30204, "FY2021": 17325}),
        ("Net cash flow from/(used in) financing activities",
         {"FY2025": -307, "FY2024": -697, "FY2023": -701, "FY2022": -9890, "FY2021": -724}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 24599, "FY2024": 27823, "FY2023": 24596, "FY2022": 22845, "FY2021": 41598}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="Gatehouse Bank Plc is a UK Shariah-compliant (Islamic) bank; 'profit paid/received' is the "
         "functional equivalent of interest paid/received. FY2025 Pillar 3 ratios are blank - not yet "
         "published as at build date. See the Cash Flow Statement sheet's source note for the 3-era "
         "presentation change and the FY2021/FY2022 restatement notes. Figures are duplicated from the "
         "detail sheets for at-a-glance trend viewing.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/GATEHOUSE BANK FINANCIALS.xlsx")
