import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Calendar year-end (31 December). Most recent published Annual Report and Pillar 3
# disclosures are for FY2024 (signed 6 March 2025) - no FY2025 Annual Report and
# Accounts had yet been published as of the source-gathering date (2026-08-26),
# only summary H1/H2 2025 Pillar 3 KM1 disclosures (no cash flow statement, and
# no capital-amount breakdown, only headline ratios in the trading update) - not
# usable for this workbook's format, so FY2025 is left out entirely rather than
# filled in from an incompatible source. 5 years used: FY2024-FY2020.
YEARS = ["FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2024_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2024-annual-report-and-accounts.pdf"
AR2022_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2022-annual-report-and-accounts.pdf"
AR2020_URL = "https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/2020-annual-report-and-accounts.pdf"

P3_2024_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2024-pillar-3-disclosures.pdf"
P3_2022_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2022-pillar-3-disclosures.pdf"
P3_2025_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2025-h2-pillar-3-disclosures.pdf"
P3_2025_H1_URL = "https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2025-h1-pillar-3-disclosures.pdf"

ENTITY_NOTE = (
    "ENTITY/OWNERSHIP NOTE: The Co-operative Bank p.l.c. (company number 00990937, FRN 121885) is the PRA-"
    "authorised entity. It is a wholly-owned subsidiary of The Co-operative Bank Finance p.l.c., itself wholly-"
    "owned by The Co-operative Bank Holdings p.l.c. (the listed holding company; named 'The Co-operative Bank "
    "Holdings Limited' in the FY2020-FY2022 Annual Reports, re-registered as a p.l.c. by FY2023). Coventry "
    "Building Society completed its acquisition of The Co-operative Bank Holdings p.l.c. on 1 January 2025 - "
    "outside the FY2020-FY2024 period covered by this workbook, so it has no bearing on any figure shown here. "
    "Coventry and Co-operative Bank have proposed a Part VII transfer of the Bank's business (including 'smile') "
    "into Coventry Building Society, targeted for 1 January 2027 - not yet effective as of the most recent "
    "published accounts, watch for a cash-flow-statement exemption or entity change in future years similar to "
    "Clydesdale Bank PLC's Nationwide Part VII transfer in this same workbook series. "
    "This workbook uses The Co-operative Bank p.l.c.'s own entity-level ('Bank Company-only') figures throughout "
    "- both cash flow and Pillar 3 - not the wider consolidated Group (The Co-operative Bank Holdings p.l.c. and "
    "its subsidiaries), consistent with the PRA-authorised-entity basis used elsewhere in this workbook series."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are The Co-operative Bank p.l.c.'s own Bank Company-only Statement of Cashflows, £m:\n"
    f"FY2024: The Co-operative Bank p.l.c. 2024 Annual Report and Accounts, p.222 (Statement of Cashflows, Bank "
    f"Company-only) - {AR2024_URL}\n"
    f"FY2023: The Co-operative Bank p.l.c. 2024 Annual Report and Accounts, p.222 (FY2023 comparative column, "
    f"same statement) - {AR2024_URL}\n"
    f"FY2022: The Co-operative Bank p.l.c. 2022 Annual Report and Accounts, p.245 (Statement of Cashflows, Bank "
    f"Company-only) - {AR2022_URL}\n"
    f"FY2021: The Co-operative Bank p.l.c. 2022 Annual Report and Accounts, p.245 (FY2021 comparative column, "
    f"same statement) - {AR2022_URL}\n"
    f"FY2020: The Co-operative Bank p.l.c. 2020 Annual Report and Accounts, p.215 (Statement of Cashflows, Bank "
    f"Company-only) - {AR2020_URL}\n"
    "All 5 years cross-checked and tie exactly across adjacent reports (e.g. FY2020 closing cash and cash "
    "equivalents of £4,221.1m matches the FY2022 report's own FY2021 opening balance).\n\n"
    + ENTITY_NOTE
)


def p3_sources(page_2024="139-140", page_2022_23="101-102"):
    return (
        "Sources - The Co-operative Bank p.l.c. individual-entity Pillar 3 basis (Appendix 1, 'KM1 - Key Metrics "
        "(Individual)' / 'KM2 - Key Metrics MREL (Individual)'):\n"
        f"FY2024: The Co-operative Bank 2024 Pillar 3 Disclosures, p.{page_2024} - {P3_2024_URL}\n"
        f"FY2023: The Co-operative Bank 2024 Pillar 3 Disclosures, p.{page_2024} (FY2023 comparative column, same "
        f"tables) - {P3_2024_URL}\n"
        f"FY2022: The Co-operative Bank 2022 Pillar 3 Disclosures, p.{page_2022_23} - {P3_2022_URL}\n"
        f"FY2021: The Co-operative Bank 2022 Pillar 3 Disclosures, p.{page_2022_23} (31 Dec 21 column, same "
        f"tables) - {P3_2022_URL}\n"
        f"FY2020: The Co-operative Bank 2022 Pillar 3 Disclosures, p.{page_2022_23} (31 Dec 20 column, same "
        f"tables - the KM1/KM2 templates report the current period plus 4 prior half-year-end points) - "
        f"{P3_2022_URL}"
    )


bw = BankWorkbook(bank_name="The Co-operative Bank p.l.c.", years=YEARS, year_label=YEAR_LABEL, header_color="1E5631")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {
        "FY2024": 50.9, "FY2023": 105.6, "FY2022": 132.9, "FY2021": 49.4, "FY2020": -95.1,
    }),
    ("DATA", "Pension scheme adjustments", {
        "FY2024": -0.9, "FY2023": -3.4, "FY2022": -12.7, "FY2021": -5.6, "FY2020": -9.3,
    }),
    ("DATA", "Net credit impairment (gains)/losses", {
        "FY2024": -5.0, "FY2023": 0.6, "FY2022": 6.4, "FY2021": 1.1, "FY2020": 21.6,
    }),
    ("DATA", "Depreciation, amortisation and impairment", {
        "FY2024": 35.3, "FY2023": 34.8, "FY2022": 35.3, "FY2021": 36.6, "FY2020": 40.2,
    }),
    ("DATA", "Impairment of investment in subsidiaries", {
        "FY2024": 21.0, "FY2023": 0.1, "FY2022": -0.3, "FY2021": 28.6, "FY2020": -0.3,
    }),
    ("DATA", "Other non-cash movements (incl. exchange rate movements)", {
        "FY2024": 53.2, "FY2023": 54.9, "FY2022": 134.4, "FY2021": 121.4, "FY2020": 77.1,
    }),
    ("DATA", "Increase/(decrease) in deposits by banks", {
        "FY2024": -1571.7, "FY2023": -1394.5, "FY2022": 155.8, "FY2021": 3461.2, "FY2020": 922.7,
    }),
    ("DATA", "(Increase) in prepayments", {
        "FY2024": -11.6, "FY2023": -2.7, "FY2022": -1.1, "FY2021": -7.1, "FY2020": 8.4,
    }),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {
        "FY2024": 23.9, "FY2023": -9.7, "FY2022": -4.4, "FY2021": 2.0, "FY2020": -23.6,
    }),
    ("DATA", "Increase/(decrease) in customer accounts", {
        "FY2024": 759.5, "FY2023": -873.9, "FY2022": -1028.7, "FY2021": 769.2, "FY2020": 1367.9,
    }),
    ("DATA", "(Decrease) in debt securities in issue", {
        "FY2022": 0.0, "FY2021": -485.7, "FY2020": -121.9,
    }),
    ("DATA", "Decrease/(increase) in loans and advances to banks", {
        "FY2024": 25.7, "FY2023": -18.7, "FY2022": -19.9, "FY2021": -23.8, "FY2020": -16.9,
    }),
    ("DATA", "(Increase)/decrease in loans and advances to customers", {
        "FY2024": -210.7, "FY2023": 578.5, "FY2022": 31.5, "FY2021": -2358.6, "FY2020": -912.2,
    }),
    ("DATA", "Increase/(decrease) in amounts owed by Co-operative Bank undertakings", {
        "FY2024": -481.5, "FY2023": -5.5, "FY2022": -31.9, "FY2021": 1302.9, "FY2020": 132.9,
    }),
    ("DATA", "Increase/(decrease) in amounts owed to Co-operative Bank undertakings", {
        "FY2024": 70.8, "FY2023": -564.5, "FY2022": -86.0, "FY2021": -1342.7, "FY2020": -755.7,
    }),
    ("DATA", "Net movement of other assets and other liabilities", {
        "FY2024": 1.6, "FY2023": -64.5, "FY2022": -3.8, "FY2021": 49.3, "FY2020": -154.6,
    }),
    ("DATA", "Income tax paid", {
        "FY2024": -4.0, "FY2023": -2.7, "FY2022": -6.8, "FY2021": 0.0,
    }),
    ("TOTAL", "Net cash flows from/(used in) operating activities", {
        "FY2024": -1243.5, "FY2023": -2165.6, "FY2022": -699.3, "FY2021": 1598.2, "FY2020": 481.2,
    }),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase and construction of tangible and intangible assets", {
        "FY2024": -27.6, "FY2023": -55.0, "FY2022": -48.0, "FY2021": -28.9, "FY2020": -16.8,
    }),
    ("DATA", "Purchase of investment securities", {
        "FY2024": -1096.4, "FY2023": -1544.9, "FY2022": -471.6, "FY2021": -886.5, "FY2020": -969.6,
    }),
    ("DATA", "Proceeds from sale of property, plant and equipment", {
        "FY2022": 0.4, "FY2021": 1.9, "FY2020": 2.6,
    }),
    ("DATA", "Proceeds from sale of shares and other interests", {
        "FY2024": 13.6, "FY2023": 0.2, "FY2022": 20.4, "FY2021": 2.0, "FY2020": 38.6,
    }),
    ("DATA", "Proceeds from sale and maturity of investment securities", {
        "FY2024": 1972.6, "FY2023": 899.0, "FY2022": 750.8, "FY2021": 849.9, "FY2020": 2088.4,
    }),
    ("DATA", "Purchase of equity shares", {
        "FY2022": -0.8, "FY2021": -0.5,
    }),
    ("DATA", "Proceeds from sale of investment properties", {
        "FY2024": 0.2, "FY2023": 0.3, "FY2020": 0.0,
    }),
    ("DATA", "Dividends received", {
        "FY2024": 0.2, "FY2023": 6.8, "FY2022": 0.2, "FY2021": 0.3, "FY2020": 0.3,
    }),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {
        "FY2024": 862.6, "FY2023": -693.6, "FY2022": 251.4, "FY2021": -61.8, "FY2020": 1143.5,
    }),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issuance of Tier 2 notes / senior unsecured debt / MREL", {
        "FY2024": 199.1, "FY2023": 397.9, "FY2022": 248.4, "FY2020": 197.7,
    }),
    ("DATA", "Redemption of Tier 2 notes and senior unsecured debt", {
        "FY2024": -236.5, "FY2023": -163.5,
    }),
    ("DATA", "Proceeds from issuance of covered bonds", {
        "FY2024": 498.5, "FY2023": 0.0,
    }),
    ("DATA", "Interest paid on Tier 2 notes, senior unsecured debt and covered bonds", {
        "FY2024": -88.2, "FY2023": -62.7, "FY2022": -44.5, "FY2021": -37.0, "FY2020": -19.0,
    }),
    ("DATA", "Lease liability principal payments", {
        "FY2024": -5.6, "FY2023": -6.6, "FY2022": -14.6, "FY2021": -11.0, "FY2020": -10.0,
    }),
    ("DATA", "Dividends paid", {
        "FY2024": -95.0, "FY2023": 0.0,
    }),
    ("TOTAL", "Net cash flows from/(used in) financing activities", {
        "FY2024": 272.3, "FY2023": 165.1, "FY2022": 189.3, "FY2021": -48.0, "FY2020": 168.7,
    }),

    ("DATA", "Effect of exchange rate changes on cash and cash equivalents", {
        "FY2024": -8.6, "FY2023": -5.5,
    }),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2024": -117.2, "FY2023": -2699.6, "FY2022": -258.6, "FY2021": 1488.4, "FY2020": 1793.4,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2024": 2751.3, "FY2023": 5450.9, "FY2022": 5709.5, "FY2021": 4221.1, "FY2020": 2427.7,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2024": 2634.1, "FY2023": 2751.3, "FY2022": 5450.9, "FY2021": 5709.5, "FY2020": 4221.1,
    }),
    ("DATA", "Comprising: Cash and balances with central banks", {
        "FY2024": 2586.0, "FY2023": 2631.7, "FY2022": 5183.8, "FY2021": 5609.8, "FY2020": 3802.5,
    }),
    ("DATA", "Comprising: Loans and advances to banks", {
        "FY2024": 48.1, "FY2023": 119.6, "FY2022": 267.1, "FY2021": 99.7, "FY2020": 418.6,
    }),
]

bw.add_cash_flow_sheet(
    title="The Co-operative Bank p.l.c. — Statement of Cashflows (Bank Company-only)",
    subtitle="Bank Company-only basis (not the wider consolidated Group), £m",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=170,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=110)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2024": 923.5, "FY2023": 995.4, "FY2022": 947.3, "FY2021": 901.5, "FY2020": 874.9,
    })],
    p3_sources(),
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2024": "18.7%", "FY2023": "20.6%", "FY2022": "19.7%", "FY2021": "20.5%", "FY2020": "18.7%",
    })],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {
        "FY2024": 923.5, "FY2023": 995.4, "FY2022": 947.3, "FY2021": 901.5, "FY2020": 874.9,
    })],
    p3_sources(),
    note="Tier 1 capital equals CET1 capital in every year shown - the Bank holds no Additional Tier 1 (AT1) "
         "instruments at the individual entity level in this period.",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2024": "18.7%", "FY2023": "20.6%", "FY2022": "19.7%", "FY2021": "20.5%", "FY2020": "18.7%",
    })],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {
        "FY2024": 1123.9, "FY2023": 1231.8, "FY2022": 1141.5, "FY2021": 1103.7, "FY2020": 1084.9,
    })],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2024": "22.7%", "FY2023": "25.5%", "FY2022": "23.7%", "FY2021": "25.1%", "FY2020": "23.2%",
    })],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {
        "FY2024": 4950.8, "FY2023": 4830.6, "FY2022": 4806.7, "FY2021": 4399.8, "FY2020": 4668.4,
    })],
    p3_sources(),
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio (excluding claims on central banks)", {
        "FY2024": "4.0%", "FY2023": "4.2%", "FY2022": "4.0%", "FY2021": "3.7%", "FY2020": "3.8%",
    })],
    p3_sources(),
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {
        "FY2024": "193.4%", "FY2023": "215.4%", "FY2022": "270.4%", "FY2021": "207.6%", "FY2020": "188.2%",
    })],
    p3_sources(),
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {
        "FY2024": "133.3%", "FY2023": "132.1%",
    })],
    p3_sources(),
    note="Blank FY2020-FY2022: under PS22/21 ('Implementation of Basel Standards'), UK NSFR disclosure was not "
         "required until reporting periods starting after 1 January 2024 - the Bank's own Pillar 3 templates "
         "leave these rows blank for those years, not a data gap.",
)

metric(
    "MREL Ratio", "%",
    [
        ("Total MREL resources available as a % of RWAs", {
            "FY2024": "36.0%", "FY2023": "39.1%", "FY2022": "33.2%", "FY2021": "29.6%", "FY2020": "27.5%",
        }),
        ("Total MREL resources available as a % of UK leverage exposure", {
            "FY2024": "7.7%", "FY2023": "8.0%", "FY2022": "6.8%", "FY2021": "5.4%", "FY2020": "5.6%",
        }),
    ],
    p3_sources(),
    note="The Bank's own KM2 Pillar 3 template discloses MREL adequacy on both an RWA basis and a UK leverage-"
         "exposure basis; both are shown here (the RWA-basis row is the headline figure used elsewhere in this "
         "workbook series).",
)

# ---------------------------------------------------------------
# Interim / semi-annual Pillar 3 disclosures
# ---------------------------------------------------------------
# The December 2025 report is headed and prepared for The Co-operative Bank
# p.l.c. itself. Its KM1 tables provide the current 31 December 2025 values
# on pp.4-5. The June 2025 report is deliberately represented as a gap: it is
# a Bank Holdings UK Consolidation Group disclosure, not an individual Bank
# plc disclosure, and therefore must not be mixed into this entity-level set.
INTERIM_HEADERS = [
    "Period", "Disclosure type", "Metric", "Value", "Unit", "Basis",
    "Source document", "Page / table",
]

INTERIM_ROWS = [
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Common Equity Tier 1 (CET1) capital", 968, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 1"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Tier 1 capital", 968, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 2"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total capital", 1169, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 3"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total risk-weighted exposure amount", 5112, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 4"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Common Equity Tier 1 (CET1) ratio", "18.9%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 5"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Tier 1 ratio", "18.9%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 6"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total capital ratio", "22.9%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 7"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Leverage ratio total exposure measure", 22035, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 13"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Leverage ratio", "4.4%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.4, Table 1, row 14"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total high-quality liquid assets (HQLA), weighted value average", 3816, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 15"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Cash outflows, total weighted value", 2292, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, UK 16a"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Cash inflows, total weighted value", 154, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, UK 16b"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total net cash outflows, adjusted value", 2138, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 16"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Liquidity coverage ratio (LCR)", "179.8%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 17"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total available stable funding", 21719, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 18"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Total required stable funding", 16129, "£m", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 19"),
    ("31 Dec 2025", "Year-end Pillar 3 (KM1)", "Net stable funding ratio (NSFR)", "134.7%", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "p.5, Table 2, row 20"),
    ("31 Dec 2025", "Year-end Pillar 3", "MREL ratio", "Not disclosed", "%", "The Co-operative Bank p.l.c. individual entity", P3_2025_URL, "No MREL table in report"),
    ("30 Jun 2025", "Half-year Pillar 3 (KM1)", "Entity-level Bank plc KM1 metrics", "Not disclosed", "n/a", "The source is Bank Holdings UK Consolidation Group, not the individual Bank plc entity", P3_2025_H1_URL, "pp.3-4, overview and Table 1"),
]

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=INTERIM_ROWS,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(INTERIM_ROWS)},
    subtitle="Entity-level semi-annual and interim Pillar 3 observations; £m unless stated",
    note=(
        "Coverage note: the 31 December 2025 report is an entity-level disclosure for The Co-operative Bank "
        "p.l.c. The 30 June 2025 report is excluded from the entity metric series because it is prepared for "
        "The Co-operative Bank Holdings p.l.c. UK Consolidation Group. MREL is not disclosed in the December "
        "2025 KM1 report. The December report's LCR is a 12-month average and NSFR is an average of the current "
        "and preceding three quarters."
    ),
)
# Keep the source register directly below the matrix so the generic verifier
# can discover it without treating the helper's spacer rows as end-of-data.
interim_ws = bw.wb["Interim Pillar 3"]
interim_ws.delete_rows(24, 2)
source_register_row = next(
    row for row in range(5, interim_ws.max_row + 1)
    if interim_ws.cell(row=row, column=1).value == "Source register"
)
for offset, source_row in enumerate(INTERIM_ROWS, start=2):
    source_cell = interim_ws.cell(row=source_register_row + offset, column=3)
    source_cell.hyperlink = source_row[6]
    source_cell.style = "Hyperlink"

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flows from/(used in) operating activities", {
            "FY2024": -1243.5, "FY2023": -2165.6, "FY2022": -699.3, "FY2021": 1598.2, "FY2020": 481.2,
        }),
        ("Net cash flows from/(used in) investing activities", {
            "FY2024": 862.6, "FY2023": -693.6, "FY2022": 251.4, "FY2021": -61.8, "FY2020": 1143.5,
        }),
        ("Net cash flows from/(used in) financing activities", {
            "FY2024": 272.3, "FY2023": 165.1, "FY2022": 189.3, "FY2021": -48.0, "FY2020": 168.7,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2024": 2634.1, "FY2023": 2751.3, "FY2022": 5450.9, "FY2021": 5709.5, "FY2020": 4221.1,
        }),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {
            "FY2024": 18.7, "FY2023": 20.6, "FY2022": 19.7, "FY2021": 20.5, "FY2020": 18.7,
        }),
        ("Tier 1 Ratio", {
            "FY2024": 18.7, "FY2023": 20.6, "FY2022": 19.7, "FY2021": 20.5, "FY2020": 18.7,
        }),
        ("Total Capital Ratio", {
            "FY2024": 22.7, "FY2023": 25.5, "FY2022": 23.7, "FY2021": 25.1, "FY2020": 23.2,
        }),
        ("Leverage Ratio", {
            "FY2024": 4.0, "FY2023": 4.2, "FY2022": 4.0, "FY2021": 3.7, "FY2020": 3.8,
        }),
        ("LCR", {
            "FY2024": 193.4, "FY2023": 215.4, "FY2022": 270.4, "FY2021": 207.6, "FY2020": 188.2,
        }),
        ("NSFR", {
            "FY2024": 133.3, "FY2023": 132.1,
        }),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. " + ENTITY_NOTE,
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CO-OPERATIVE BANK FINANCIALS.xlsx")
print("Saved CO-OPERATIVE BANK FINANCIALS.xlsx")
