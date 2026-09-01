import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

# ---------------------------------------------------------------
# Source documents. FirstBank UK Limited (Companies House no. 04459383, FRN
# 216772) was named FBN Bank (UK) Limited until its FY2022/FY2023 rename -
# same legal entity throughout, continuity confirmed via Companies House
# filing history. It is a wholly-owned UK subsidiary of First Bank of Nigeria
# Limited. All Annual Report PDFs are DocuSign-flattened scans (0 extractable
# text) - every cash flow figure below was read directly off the rendered
# page image, not OCR'd/extracted text.
# ---------------------------------------------------------------
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04459383/filing-history/MzUyNzc5Nzc3MWFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/04459383/filing-history/MzQ3MzE2Nzc1OGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/04459383/filing-history/MzQyNjA0OTI3OWFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04459383/filing-history/MzM4NTMzODE5NmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/04459383/filing-history/MzM0MTI4NjI3MGFkaXF6a2N4/document?format=pdf&download=0"

P3_2024_URL = "https://www.fbnbank.co.uk/wp-content/uploads/2025/09/FirstBank-UK-Pillar-3-Dec-2024-1.pdf"
P3_2023_URL = "https://www.fbnbank.co.uk/wp-content/uploads/2019/06/FirstBank-UK-Pillar-3-Dec-2023.pdf"
P3_2022_URL = "https://www.fbnbank.co.uk/wp-content/uploads/2019/06/FirstBank-UK-Pillar-3-Dec-2022-V1.0.pdf"
P3_2021_URL = "https://www.fbnbank.co.uk/wp-content/uploads/2019/06/FBNUK-Pillar-3-Disclosures_-2021.pdf"

# ---------------------------------------------------------------
# Currency note: the Bank changed its presentation/functional currency from
# GBP to USD starting with its FY2023 Annual Report and FY2023 Pillar 3
# disclosures (both published in $ from that point on; FY2022 was restated
# by the Bank itself into $ as the FY2023 AR/Pillar 3's own comparative
# column). FY2021 has no $ figure published anywhere by the Bank - to keep
# this whole workbook on one consistent $ basis (rather than mixing £ and $
# across columns), FY2021 is converted here from the Bank's own as-reported
# £ figures using the same Bank of England GBP/USD spot/average methodology
# established for Zenith Bank (UK) Limited (see build_zenith.py): flow
# (P&L/cash-flow) figures at that year's average rate, £1 = $1.3752; balance
# (period-end/capital/RWA) figures at that year-end's spot rate, £1 = $1.3521
# (31 Dec 2021) / $1.3661 (31 Dec 2020, for FY2021's opening cash balance
# only). Rates are Bank of England GBP/USD archive values via
# poundsterlinglive.com's published archive, same source used for Zenith.
# Because flows and balances are converted at different rates, the cash flow
# sheet includes an explicit "Effect of GBP/USD translation" line for FY2021
# so opening + all flows + this line = closing exactly in $ terms - this
# line is purely an artefact of $ translation and has no bearing on the
# Bank's underlying £ results for that year.
# ---------------------------------------------------------------
FX_SPOT_2020 = 1.3661  # 31 Dec 2020 - only used for FY2021's opening cash balance
FX_SPOT_2021 = 1.3521  # 31 Dec 2021
FX_AVG_2021 = 1.3752

CURRENCY_NOTE = (
    "CURRENCY NOTE: FirstBank UK Limited changed its presentation currency from GBP to USD starting with its "
    "FY2023 Annual Report and FY2023 Pillar 3 disclosures (FY2022 was restated by the Bank itself into $ as "
    "that year's own comparative). FY2021 is not published in $ anywhere by the Bank - to keep this whole "
    "To keep this workbook on one consistent $ basis, the apparent FY2022 RWA difference is a currency restatement rather "
    "than a disagreement between two USD figures: the original £1,019,070k became $1,230,686k at the Bank's "
    "implied restatement rate. GBP/USD volatility means the original GBP and restated USD amounts should not "
    "be compared as if they were the same currency. FY2021 figures below are converted from the Bank's own as-reported £ "
    "figures using the Bank of England GBP/USD spot/average methodology established for Zenith Bank (UK) "
    "Limited: flow figures at the FY2021 average rate (£1 = $1.3752), balance figures at the FY2021 year-end "
    "spot rate (£1 = $1.3521; the FY2020 year-end spot rate of £1 = $1.3661 is used only for FY2021's opening "
    "cash balance). Ratios are NOT converted - dimensionless and currency-invariant, so FY2021's ratios below "
    "are the Bank's own as-reported % figures unchanged. The FY2021 cash flow column includes an explicit "
    "'Effect of GBP/USD translation' line so opening + flows + this line = closing exactly in $ terms; this "
    "line is a translation artefact only and has no bearing on the Bank's underlying £ results for FY2021."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are FirstBank UK Limited's own Statement of Cash Flows (page images, statutory "
    "accounts filed at Companies House - each report's own accounts are DocuSign-flattened scans):\n"
    f"FY2025: Annual Report and Financial Statements for the year ended 31 December 2025, p.56 (Statement of "
    f"Cash Flows), as filed at Companies House 03 Jul 2026 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements for the year ended 31 December 2024, p.48 (Statement of "
    f"Cash Flows), as filed at Companies House 10 Jul 2025 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 December 2023, p.42 (Statement of "
    f"Cash Flows), as filed at Companies House 26 Jun 2024 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for the year ended 31 December 2023, p.42 (Statement of "
    f"Cash Flows, Restated 31 December 2022 comparative column, $ - the Bank's own USD restatement), as filed "
    f"at Companies House 26 Jun 2024 - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements (as FBN Bank (UK) Limited) for the year ended 31 December "
    f"2021, p.33 (Statement of Cash Flows, £ as originally reported), as filed at Companies House 08 Jun 2022 - "
    f"{AR2021_URL} - converted to $ per the currency note below.\n\n"
    + CURRENCY_NOTE
)


def p3_sources(page2024=None, page2023=None, page2022=None, page2021=None, table=None):
    lines = ["Sources - FirstBank UK Limited Pillar 3 Disclosures (UK KM1 - Key Metrics" +
             (f", {table}" if table else "") + "):\n"]
    if page2024:
        lines.append(f"FY2024: Pillar 3 Disclosures, 31st December 2024, p.{page2024} - {P3_2024_URL}\n")
    lines.append(f"FY2023: Pillar 3 Disclosures, 31st December 2023, p.{page2023} ($, own report) - {P3_2023_URL}\n")
    lines.append(f"FY2022: Pillar 3 Disclosures, 31st December 2023, p.{page2023} (Table 1, 2022 comparative "
                 f"column, $ - the Bank's own USD restatement) - {P3_2023_URL}\n")
    lines.append(f"FY2021: Pillar 3 Disclosures (as FBN Bank (UK) Limited), 31st December 2022, p.{page2022} "
                 f"(Table 6, 2021 comparative column, £ as originally reported) - {P3_2022_URL} - converted to "
                 f"$ per the Cash Flow Statement sheet's currency note (ratios unconverted).\n")
    lines.append("FY2025: not yet published as of this workbook's build date - no FY2025 Pillar 3 Disclosures "
                 "document has been released.\n")
    return "".join(lines)


bw = BankWorkbook(bank_name="FirstBank UK Limited", years=YEARS, year_label=YEAR_LABEL, header_color="060F0B")


def th(rows):
    """Rescale whole-dollar cash flow figures to $'000, matching this project's usual scale for a bank this
    size (see build_fidbank_uk.py's £'000 precedent for the same Nigerian-subsidiary FX-conversion pattern)."""
    out = []
    for kind, label, values in rows:
        scaled = {y: (round(v / 1000) if isinstance(v, (int, float)) else v) for y, v in values.items()}
        out.append((kind, label, scaled))
    return out


def th2(rows):
    """Same as th() but for the (label, values) pairs add_overview_sheet's cash_flow_totals expects."""
    out = []
    for label, values in rows:
        scaled = {y: (round(v / 1000) if isinstance(v, (int, float)) else v) for y, v in values.items()}
        out.append((label, scaled))
    return out


# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("DATA", "Profit for the year before taxation", {
        "FY2025": 54183785, "FY2024": 61068239, "FY2023": 47553062, "FY2022": 47583861,
        "FY2021": 39555278,
    }),
    ("SECTION", "Adjustment to reconcile profit to cash flow from operating activities", {}),
    ("DATA", "Depreciation of property and equipment", {
        "FY2025": 1234619, "FY2024": 1305257, "FY2023": 1553258, "FY2022": 1577263,
        "FY2021": 1869076,
    }),
    ("DATA", "Amortisation of intangible assets", {
        "FY2025": 209127, "FY2024": 710483, "FY2023": 834713, "FY2022": 1059948,
        "FY2021": 1214143,
    }),
    ("DATA", "Interest expenses on subordinated liability", {
        "FY2025": 5475000, "FY2024": 5490000, "FY2023": 5475000, "FY2022": 11863324,
        "FY2021": 5640848,
    }),
    ("DATA", "Net gains/(loss) from sale of investment securities", {
        "FY2025": 354336, "FY2024": -242362, "FY2023": 747336, "FY2022": 2509443,
        "FY2021": -407341,
    }),
    ("DATA", "Net gains on sale of financial assets at FVTPL", {
        "FY2025": -102818, "FY2024": -28597,
        # not a separate line in the FY2023 AR's own FY2023 column, or in the FY2022/FY2021-era format
    }),
    ("DATA", "Foreign currency revaluation (gains)/losses", {
        "FY2025": -6402369, "FY2024": 3201086, "FY2023": 5819509, "FY2022": 3830135,
        "FY2021": 1828225,
    }),
    ("DATA", "Credit impairment losses/(gains)", {
        "FY2025": 5279783, "FY2024": 1786453, "FY2023": 10652655, "FY2022": 1144902,
        "FY2021": -1356255,
    }),
    ("TOTAL", "Operating cash flow before changes in operating assets/liabilities", {
        "FY2025": 60231463, "FY2024": 73290559, "FY2023": 72635533, "FY2022": 69568876,
        "FY2021": 48343973,
    }),
    ("SECTION", "Net (increase)/decrease in assets relating to operating activities", {}),
    ("DATA", "Loans and advances to banks", {
        "FY2025": 66031212, "FY2024": 36160880, "FY2023": 22100735, "FY2022": -76514233,
        "FY2021": -253446737,
    }),
    ("DATA", "Loans and advances to customers", {
        "FY2025": -342954781, "FY2024": -74018980, "FY2023": -139867128, "FY2022": 105947878,
        "FY2021": 64373734,
    }),
    ("DATA", "Financial assets held at fair value through profit or loss", {
        "FY2025": -453774426, "FY2024": 3250178, "FY2023": -5642530, "FY2022": -12894565,
        "FY2021": 15583489,
    }),
    ("DATA", "Other assets", {
        "FY2025": -1391047, "FY2024": -29588, "FY2023": -851334, "FY2022": -159470,
        "FY2021": -342346,
    }),
    ("TOTAL", "Net (increase)/decrease in assets relating to operating activities", {
        "FY2025": -732089042, "FY2024": -34637510, "FY2023": -124260257, "FY2022": 16379610,
        "FY2021": -173831862,
    }),
    ("SECTION", "Net (decrease)/increase in liabilities relating to operating activities", {}),
    ("DATA", "Deposits from banks", {
        "FY2025": -729802922, "FY2024": 804463093, "FY2023": -1050768435, "FY2022": 101289192,
        "FY2021": 226547256,
    }),
    ("DATA", "Deposits from customers", {
        "FY2025": 612656527, "FY2024": -189309183, "FY2023": 41248076, "FY2022": 288002144,
        "FY2021": -17623266,
    }),
    ("DATA", "Other liabilities", {
        "FY2025": -11465920, "FY2024": 66945979, "FY2023": -41704800, "FY2022": -91730351,
        "FY2021": 42689697,
    }),
    ("DATA", "Financial liabilities at fair value through profit or loss", {
        "FY2025": 3774572, "FY2024": -17087478, "FY2023": -17047705, "FY2022": 6824115,
        "FY2021": 17704719,
    }),
    ("DATA", "Income taxes paid", {
        "FY2025": -6545402, "FY2024": -8679449, "FY2023": -5819386, "FY2022": -2567718,
        "FY2021": -2032427,
    }),
    ("TOTAL", "Net (decrease)/increase in liabilities relating to operating activities", {
        "FY2025": -131383145, "FY2024": 656332962, "FY2023": -1074092250, "FY2022": 301817382,
        "FY2021": 267285979,
    }),
    ("TOTAL", "Net cashflow from/(used in) operating activities", {
        # not an explicit line item in the FY2023 AR (own FY2023 column) or FY2022/FY2021-era reports -
        # left blank rather than a figure this project computed itself; see the three subtotals above.
        "FY2025": -803240724, "FY2024": 694986011,
    }),
    ("SECTION", "Cash flows from/(used in) investing activities", {}),
    ("DATA", "Acquisition of property, plant and equipment", {
        "FY2025": -52523, "FY2024": -123689, "FY2023": -186105, "FY2022": -86580,
        "FY2021": -147944,
    }),
    ("DATA", "Acquisition of intangible assets", {
        "FY2025": -24776, "FY2024": -5653, "FY2023": -175283, "FY2022": -379395,
        "FY2021": -213771,
    }),
    ("DATA", "Proceeds from sale/maturity of investment securities", {
        "FY2025": 2625720668, "FY2024": 2958772741,
    }),
    ("DATA", "Purchase of investment securities", {
        "FY2025": -1744047207, "FY2024": -3780168736,
    }),
    ("DATA", "Proceeds from/(purchase of) financial investments at amortised cost", {
        "FY2023": 1105994751, "FY2022": -131164090, "FY2021": -388494432,
    }),
    ("DATA", "Proceeds from sale of property and equipment", {
        "FY2023": 3171,
    }),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": 881596162, "FY2024": -821525337, "FY2023": 1105636534, "FY2022": -131630065,
        "FY2021": -388856147,
    }),
    ("SECTION", "Cash flows used in financing activities", {}),
    ("DATA", "Interest paid on subordinated liability", {
        "FY2025": -5460000, "FY2024": -5505000, "FY2023": -5475000, "FY2022": -5459692,
        "FY2021": -4809745,
    }),
    ("DATA", "Principal element of lease payment", {
        "FY2025": -1313025, "FY2024": -931173, "FY2023": -1253403, "FY2022": -1225171,
        "FY2021": -1721371,
    }),
    ("TOTAL", "Net cash used in financing activities", {
        "FY2025": -6773025, "FY2024": -6436173, "FY2023": -6728403, "FY2022": -6684863,
        "FY2021": -6531116,
    }),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {
        "FY2025": 71582413, "FY2024": -132975499, "FY2023": -26808842, "FY2022": 249450940,
        "FY2021": -253589172,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 362737524, "FY2024": 495730749, "FY2023": 522342258, "FY2022": 274093095,
        "FY2021": 621026011,
    }),
    ("DATA", "Exchange difference", {
        "FY2025": 520174, "FY2024": -17726, "FY2023": 197332, "FY2022": -1201776,
    }),
    ("DATA", "Effect of GBP/USD translation (FY2021 only - see currency note)", {
        "FY2021": -2104691,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 434840111, "FY2024": 362737524, "FY2023": 495730748, "FY2022": 522342259,
        "FY2021": 365332148,
    }),
]

bw.add_cash_flow_sheet(
    title="FirstBank UK Limited — Statement of Cash Flows",
    subtitle="Consolidated basis, as filed at Companies House ($ throughout - FY2021 converted from £, see source note)",
    rows=th(rows),
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=220,
    unit_suffix=" ($'000, FY2021 conv. from £)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=140)


metric(
    "CET1 Capital", "$'000",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2024": 363763, "FY2023": 309460, "FY2022": 276585, "FY2021": 272998,
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
    note="CET1 capital equals Tier 1 capital for this Bank - it holds no Additional Tier 1 instruments (CET1 "
         "ratio and Tier 1 ratio are identical every year, see the Tier 1 Ratio and CET1 Ratio sheets).",
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2024": "26.07%", "FY2023": "25.05%", "FY2022": "22.47%", "FY2021": "17.79%",
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
)

metric(
    "Tier 1 Capital", "$'000",
    [("Tier 1 capital", {
        "FY2024": 363763, "FY2023": 309460, "FY2022": 276585, "FY2021": 272998,
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
    note="Tier 1 capital equals CET1 capital for this Bank - it holds no Additional Tier 1 instruments.",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2024": "26.07%", "FY2023": "25.05%", "FY2022": "22.47%", "FY2021": "17.79%",
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
)

metric(
    "Total Capital", "$'000",
    [("Total capital (TC = T1 + T2)", {
        "FY2024": 414074, "FY2023": 353999, "FY2022": 320951, "FY2021": 326148,
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2024": "29.67%", "FY2023": "28.65%", "FY2022": "26.08%", "FY2021": "21.25%",
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
)

metric(
    "Total RWAs", "$'000",
    [("Total risk-weighted exposure amounts", {
        "FY2024": 1395598, "FY2023": 1235478, "FY2022": 1019070, "FY2021": 1534738,
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {
        "FY2024": "14.12%", "FY2023": "19.64%", "FY2022": "9.84%", "FY2021": "6.83%",
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (12-month trailing average)", {
        "FY2024": "409.09%", "FY2023": "383.17%", "FY2022": "240.65%", "FY2021": "243.08%",
    })],
    p3_sources(page2024=3, page2023=3, page2022=26, table="Table 1 / Table 6"),
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {
        "FY2024": "213%", "FY2023": "286.37%", "FY2022": "274.71%",
        # FY2021: not disclosed on a comparable basis - the CRR2 NSFR rules commenced 1 Jan 2022 and the
        # Bank's own Pillar 3 Dec-2022 report states prior-period data is "not available on an equivalent basis"
    })],
    p3_sources(page2024=3, page2023=3, page2022=26, table="Table 1 / Table 6"),
    note="FY2021 not disclosed: the CRR2 NSFR rules commenced 1 January 2022 and the Bank's own Pillar 3 "
         "Disclosures (Dec 2022) state prior-period NSFR data is 'not available on an equivalent basis'.",
)

metric(
    "MREL Ratio", None,
    [("Minimum Requirement for Own Funds and Eligible Liabilities (MREL) ratio", {
        y: "Not publicly disclosed" for y in bw.years
    })],
    "Sources - FirstBank UK Limited Pillar 3 Disclosures (31st December 2022, p.26) describes the Bank's MREL "
    "requirement qualitatively (set equal to its Pillar 1 + Pillar 2A capital requirements by the Bank of "
    "England as resolution authority under the BRRD) but does not disclose a quantitative MREL ratio figure in "
    f"any year's Pillar 3 Disclosures reviewed for this workbook - {P3_2022_URL}",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=th2([
        ("Net cashflow from/(used in) operating activities", {
            "FY2025": -803240724, "FY2024": 694986011,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": 881596162, "FY2024": -821525337, "FY2023": 1105636534, "FY2022": -131630065,
            "FY2021": -388856147,
        }),
        ("Net cash used in financing activities", {
            "FY2025": -6773025, "FY2024": -6436173, "FY2023": -6728403, "FY2022": -6684863,
            "FY2021": -6531116,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 434840111, "FY2024": 362737524, "FY2023": 495730748, "FY2022": 522342259,
            "FY2021": 365332148,
        }),
    ]),
    cash_flow_unit="$'000",
    ratios=[
        ("CET1 Ratio", {
            "FY2024": "26.07%", "FY2023": "25.05%", "FY2022": "22.47%", "FY2021": "17.79%",
        }),
        ("Tier 1 Ratio", {
            "FY2024": "26.07%", "FY2023": "25.05%", "FY2022": "22.47%", "FY2021": "17.79%",
        }),
        ("Total Capital Ratio", {
            "FY2024": "29.67%", "FY2023": "28.65%", "FY2022": "26.08%", "FY2021": "21.25%",
        }),
        ("Leverage Ratio", {
            "FY2024": "14.12%", "FY2023": "19.64%", "FY2022": "9.84%", "FY2021": "6.83%",
        }),
        ("LCR", {
            "FY2024": "409.09%", "FY2023": "383.17%", "FY2022": "240.65%", "FY2021": "243.08%",
        }),
        ("NSFR", {
            "FY2024": "213%", "FY2023": "286.37%", "FY2022": "274.71%",
        }),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. The Bank changed its presentation currency from "
         "GBP to USD in FY2023 - see the Cash Flow Statement sheet's currency note for how FY2021/FY2022 were "
         "put on a consistent $ basis here.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/FIRSTBANK UK FINANCIALS.xlsx")
