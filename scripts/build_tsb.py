import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR25_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2025/TSB-Bank-ARA-2025.pdf"
AR24_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2024/TSB-Bank-ARA-2024.pdf"
AR23_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2023/TSB-Bank-2023.pdf"
AR21_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2021/tsb-bank-ara-2021.pdf"

P3_25_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/tsb-large-subsidiary-disclosure-2025.pdf"
P3_24_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/TSB-Large-subsidiary-Disclosure-2024.pdf"
P3_23_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/TSB-large-subsidiary-disclosure-2023.pdf"
P3_22_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/TSB-Large-subsidiary-Disclosure-2022.pdf"
P3_21_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/TSB-Large-Subsidiary-Disclosure-2021.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: TSB Bank plc (Companies House SC095237) is the entity on the PRA register; its own Annual "
    "Report and Accounts (consolidated 'Bank (Consolidated)' column used throughout) is used for the cash flow "
    "statement. TSB Banking Group plc's only direct subsidiary is TSB Bank plc, so 'TSB Banking Group plc' "
    "consolidated Pillar 3 disclosures (published under that name, as TSB is a 'large subsidiary' of Banco "
    "Sabadell for CRR Article 13 purposes) are effectively the same consolidation scope and are used for all "
    "Pillar 3 metric sheets.\n"
    "CONTEXT: TSB was owned by Banco de Sabadell, S.A. (Spain) throughout FY2021-FY2025. Santander UK plc agreed "
    "to acquire TSB in July 2025 and completed the acquisition on 30 April 2026 (after this workbook's FY2025 "
    "year-end) - so all 5 years of data here reflect the Sabadell-owned period; TSB's board ceased dividend "
    "payments to Sabadell following the announcement per TSB's FY2025 Pillar 3 disclosure."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are TSB Bank plc, Bank (Consolidated) basis, £ million.\n"
    f"FY2025 & FY2024: TSB Bank plc Annual Report and Accounts 2025, p.49 and p.106 (Cash flow statements and "
    f"note 32) - {AR25_URL}\n"
    f"FY2023 & FY2022 (restated): TSB Bank plc Annual Report and Accounts 2023, p.33-34 and p.83-84 (Cash flow "
    f"statements and note 32) - {AR23_URL}\n"
    f"FY2021: TSB Bank plc Annual Report and Accounts 2021, p.29 and p.78 (Cash flow statements and note 31) "
    f"- {AR21_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "RESTATEMENT NOTE: The 2023 Annual Report restated FY2022 (and earlier) to include on-demand loans and "
    "advances to credit institutions within cash and cash equivalents; this added £56.1m to the FY2021 closing "
    "cash position and £159.2m to the FY2022 opening position on a comparative basis, but FY2021's own Annual "
    "Report was never itself restated. As a result, FY2021's closing cash and cash equivalents (£4,851.1m, as "
    "originally reported) does not exactly tie to FY2022's opening balance shown here (£4,907.2m, restated) - a "
    "known £56.1m definitional break at that one boundary, not a data error. FY2022 onward reconciles exactly. "
    "The 2023 Annual Report also reclassified a derivatives/hedge-accounting fair value line from 'change in "
    "operating assets and liabilities' into 'non-cash and other items' from FY2023 onward; FY2021 and FY2022 keep "
    "their original as-reported classification for that line (see the two separate rows below).\n\n"
    "PRESENTATION NOTE: Line items were relabelled and reorganised across these 5 years as TSB's funding mix "
    "evolved (e.g. 'Issue of debt securities in issue' in FY2021 became separate covered bond/senior "
    "unsecured/securitisation/AT1 lines by FY2024-25; a repurchase-agreements financing line appeared only in "
    "FY2022-23). Blank cells indicate that year's report did not disclose or did not have that specific line; "
    "'0' indicates the report explicitly showed a nil ('-') value. The 'Change in operating assets and "
    "liabilities' and 'Non-cash and other items' rows are TSB's own audited primary-statement subtotals; the "
    "rows above each are the supporting breakdown from the cash flow note."
)


def p3_sources(page_km1, table_km1="Table 1: Key metrics (KM1)"):
    return (
        "Sources - TSB Banking Group plc consolidated Pillar 3 basis (see entity note on Cash Flow Statement "
        "sheet):\n"
        f"FY2025: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2025, p.6 ({table_km1}) "
        f"- {P3_25_URL}\n"
        f"FY2024: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2024, p.6 (Table 1a: Key "
        f"metrics (KM1)) - {P3_24_URL}\n"
        f"FY2023: TSB Banking Group plc Large Subsidiary Disclosures 2023, p.6 (Table 1a: Key metrics (KM1)) "
        f"- {P3_23_URL}\n"
        f"FY2022: TSB Banking Group plc Large Subsidiary Disclosures 2022, p.6 (Table 1a: Key metrics (KM1)) "
        f"- {P3_22_URL}\n"
        f"FY2021: TSB Banking Group plc Large Subsidiary Disclosures 2021, p.5 (Table 1: Key metrics (KM1 / IFRS "
        f"9-FL)) - {P3_21_URL}"
    )


bw = BankWorkbook(bank_name="TSB Bank plc", years=YEARS, header_color="002D5B")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    (
        "DATA",
        "Profit/(loss) before taxation",
        {
            "FY2025": 339.4,
            "FY2024": 285.1,
            "FY2023": 235.5,
            "FY2022": 181.1,
            "FY2021": 155.5,
        },
    ),
    ("DATA", "Decrease in loans to central banks", {"FY2025": 0, "FY2024": 136.0}),
    (
        "DATA",
        "Increase in loans to central banks (FY2021 presentation)",
        {"FY2021": -22.7},
    ),
    ("DATA", "(Increase)/decrease in loans to credit institutions", {"FY2021": -12.8}),
    (
        "DATA",
        "Decrease/(increase) in loans and advances to customers",
        {
            "FY2025": -1.4,
            "FY2024": -124.6,
            "FY2023": 1719.2,
            "FY2022": -722.5,
            "FY2021": -4070.2,
        },
    ),
    (
        "DATA",
        "Increase in reverse repurchase agreements",
        {"FY2025": -62.0, "FY2024": 0},
    ),
    (
        "DATA",
        "Decrease in reverse purchase agreements (FY2021 presentation)",
        {"FY2021": 0},
    ),
    (
        "DATA",
        "Decrease/(increase) in other advances",
        {
            "FY2025": 63.3,
            "FY2024": 79.3,
            "FY2023": 493.6,
            "FY2022": -622.6,
            "FY2021": 136.8,
        },
    ),
    (
        "DATA",
        "Net change in derivative financial instruments and FV adjustments for portfolio hedged risk (within operating assets/liabilities - FY2021/22 as originally presented)",
        {"FY2022": -63.1, "FY2021": -147.6},
    ),
    (
        "DATA",
        "Decrease/(increase) in other assets",
        {"FY2025": 11.2, "FY2024": 2.0, "FY2023": -6.5, "FY2022": 72.4, "FY2021": 18.6},
    ),
    (
        "DATA",
        "(Decrease)/increase in deposits from credit institutions (FY2021 presentation)",
        {"FY2021": 0},
    ),
    (
        "DATA",
        "Increase/(decrease) in customer deposits",
        {
            "FY2025": 176.0,
            "FY2024": 280.8,
            "FY2023": -1666.5,
            "FY2022": 357.0,
            "FY2021": 1591.2,
        },
    ),
    (
        "DATA",
        "(Decrease)/increase in other financial liabilities",
        {
            "FY2025": -148.8,
            "FY2024": -91.9,
            "FY2023": -156.4,
            "FY2022": 1126.5,
            "FY2021": 141.9,
        },
    ),
    (
        "DATA",
        "(Decrease)/increase in provisions",
        {
            "FY2025": -13.4,
            "FY2024": -33.5,
            "FY2023": -46.5,
            "FY2022": 17.6,
            "FY2021": -40.4,
        },
    ),
    (
        "DATA",
        "Increase/(decrease) in other liabilities",
        {
            "FY2025": 16.4,
            "FY2024": -3.3,
            "FY2023": -11.6,
            "FY2022": -25.4,
            "FY2021": 0.7,
        },
    ),
    (
        "TOTAL",
        "Change in operating assets and liabilities (as reported)",
        {
            "FY2025": 41.3,
            "FY2024": 244.8,
            "FY2023": 333.6,
            "FY2022": 202.3,
            "FY2021": -2404.5,
        },
    ),
    (
        "DATA",
        "Interest expense on financing activities",
        {"FY2025": 291.1, "FY2024": 402.3, "FY2023": 398.8, "FY2022": 160.0},
    ),
    (
        "DATA",
        "Interest income on investing activities",
        {"FY2025": -63.4, "FY2024": -63.2, "FY2023": -60.0, "FY2022": -33.2},
    ),
    (
        "DATA",
        "Net change in derivative financial instruments and FV adjustments for portfolio hedged risk (within non-cash items - FY2023 onward presentation)",
        {"FY2025": 127.1, "FY2024": 259.6, "FY2023": 147.6},
    ),
    (
        "DATA",
        "Depreciation and amortisation",
        {
            "FY2025": 63.4,
            "FY2024": 72.5,
            "FY2023": 67.0,
            "FY2022": 66.0,
            "FY2021": 70.2,
        },
    ),
    (
        "DATA",
        "Net movement in allowance for credit impairment losses",
        {"FY2025": -8.9, "FY2024": -31.7},
    ),
    (
        "DATA",
        "Impairment losses on loans and advances to customers (FY2021-23 presentation)",
        {"FY2023": 13.8, "FY2022": 57.8, "FY2021": 2.6},
    ),
    ("DATA", "Exchange differences", {"FY2021": 0}),
    (
        "DATA",
        "Other non-cash items",
        {
            "FY2025": -48.8,
            "FY2024": -115.5,
            "FY2023": 97.4,
            "FY2022": -64.2,
            "FY2021": 39.2,
        },
    ),
    (
        "TOTAL",
        "Non-cash and other items (as reported)",
        {
            "FY2025": 360.5,
            "FY2024": 524.0,
            "FY2023": 664.6,
            "FY2022": 247.4,
            "FY2021": 112.0,
        },
    ),
    (
        "DATA",
        "Taxation paid",
        {
            "FY2025": -78.8,
            "FY2024": -57.0,
            "FY2023": -33.0,
            "FY2022": -34.4,
            "FY2021": -8.7,
        },
    ),
    (
        "TOTAL",
        "Net cash (used in)/provided by operating activities",
        {
            "FY2025": 662.4,
            "FY2024": 996.9,
            "FY2023": 1200.7,
            "FY2022": 596.4,
            "FY2021": -2145.7,
        },
    ),
    ("SECTION", "Cash flows from investing activities", {}),
    (
        "DATA",
        "Purchase of property and equipment",
        {
            "FY2025": -18.3,
            "FY2024": -22.2,
            "FY2023": -20.2,
            "FY2022": -36.8,
            "FY2021": -44.5,
        },
    ),
    (
        "DATA",
        "Purchase and development of intangible assets",
        {
            "FY2025": -38.4,
            "FY2024": -41.8,
            "FY2023": -28.0,
            "FY2022": -17.5,
            "FY2021": -30.3,
        },
    ),
    (
        "DATA",
        "Purchase of debt securities",
        {
            "FY2025": -247.4,
            "FY2024": -124.7,
            "FY2023": -219.8,
            "FY2022": -580.1,
            "FY2021": -1324.5,
        },
    ),
    (
        "DATA",
        "Sale of debt securities",
        {"FY2024": 0, "FY2023": 252.6, "FY2022": 442.6, "FY2021": 500.9},
    ),
    (
        "DATA",
        "Proceeds from maturing investments",
        {
            "FY2025": 169.3,
            "FY2024": 141.7,
            "FY2023": 39.3,
            "FY2022": 67.0,
            "FY2021": 23.0,
        },
    ),
    (
        "DATA",
        "Interest received on debt securities",
        {
            "FY2025": 67.6,
            "FY2024": 68.1,
            "FY2023": 64.6,
            "FY2022": 44.5,
            "FY2021": 36.3,
        },
    ),
    (
        "TOTAL",
        "Net cash (used in)/provided by investing activities",
        {
            "FY2025": -67.2,
            "FY2024": 21.1,
            "FY2023": 88.5,
            "FY2022": -80.3,
            "FY2021": -839.1,
        },
    ),
    ("SECTION", "Cash flows from financing activities", {}),
    (
        "DATA",
        "Additional borrowings from central banks",
        {"FY2025": 5.0, "FY2024": 0, "FY2023": 5.0, "FY2022": 510.0, "FY2021": 5500.0},
    ),
    (
        "DATA",
        "Repayment of borrowing from central banks",
        {
            "FY2025": -797.0,
            "FY2024": -2620.0,
            "FY2023": -1500.0,
            "FY2022": -510.0,
            "FY2021": -3065.0,
        },
    ),
    (
        "DATA",
        "Interest paid on borrowings from central banks",
        {
            "FY2025": -46.2,
            "FY2024": -177.1,
            "FY2023": -191.7,
            "FY2022": -57.3,
            "FY2021": -7.8,
        },
    ),
    (
        "DATA",
        "Issue of covered bonds",
        {"FY2025": 495.5, "FY2024": 926.1, "FY2023": 1750.0, "FY2022": 0},
    ),
    ("DATA", "Repayment of covered bonds", {"FY2025": 0, "FY2024": -500.0}),
    ("DATA", "Buyback of covered bonds", {"FY2023": -251.0, "FY2022": -500.0}),
    (
        "DATA",
        "Interest paid on covered bonds",
        {"FY2025": -143.2, "FY2024": -144.4, "FY2023": -120.1, "FY2022": -29.5},
    ),
    ("DATA", "Issue of securitisation notes", {"FY2025": 0, "FY2024": 498.3}),
    ("DATA", "Repayment of securitisation notes", {"FY2025": -20.0, "FY2024": -5.0}),
    (
        "DATA",
        "Interest paid on securitisation notes",
        {"FY2025": -24.2, "FY2024": -11.8},
    ),
    ("DATA", "Issue of Additional Tier 1 securities", {"FY2025": 0, "FY2024": 249.7}),
    (
        "DATA",
        "Issue of senior unsecured debt securities",
        {"FY2024": 0, "FY2023": 200.0, "FY2022": 700.0},
    ),
    (
        "DATA",
        "Repayment of senior unsecured debt securities",
        {"FY2025": -250.0, "FY2024": 0, "FY2023": 0, "FY2022": -450.0},
    ),
    (
        "DATA",
        "Interest paid on senior unsecured debt securities",
        {"FY2025": -65.3, "FY2024": -72.4, "FY2023": -51.1, "FY2022": -15.8},
    ),
    (
        "DATA",
        "Issue of debt securities in issue (FY2021 presentation)",
        {"FY2021": 500.0},
    ),
    (
        "DATA",
        "Interest paid on debt securities in issue (FY2021 presentation)",
        {"FY2021": -21.0},
    ),
    ("DATA", "Issue of subordinated liabilities", {"FY2021": 300.0}),
    ("DATA", "Repayment of subordinated liabilities", {"FY2021": -385.0}),
    (
        "DATA",
        "Interest paid on subordinated liabilities",
        {
            "FY2025": -10.3,
            "FY2024": -10.3,
            "FY2023": -10.3,
            "FY2022": -10.3,
            "FY2021": -18.8,
        },
    ),
    (
        "DATA",
        "(Repayment)/issue of repurchase agreements",
        {"FY2023": -359.9, "FY2022": 359.9},
    ),
    (
        "DATA",
        "Interest paid on repurchase agreements",
        {"FY2023": -1.0, "FY2022": -2.6},
    ),
    ("DATA", "Net securitisation funding (FY2021 presentation)", {"FY2021": 0}),
    (
        "DATA",
        "Lease payments",
        {
            "FY2025": -16.2,
            "FY2024": -18.8,
            "FY2023": -17.8,
            "FY2022": -19.7,
            "FY2021": -22.8,
        },
    ),
    (
        "DATA",
        "Distributions on other equity instruments",
        {"FY2025": -17.6, "FY2024": 0},
    ),
    (
        "DATA",
        "Dividends paid",
        {"FY2025": -300.0, "FY2024": -120.0, "FY2023": -50.0, "FY2022": 0},
    ),
    (
        "TOTAL",
        "Net cash (used in)/provided by financing activities",
        {
            "FY2025": -1189.5,
            "FY2024": -2005.7,
            "FY2023": -597.9,
            "FY2022": -25.3,
            "FY2021": 2779.6,
        },
    ),
    (
        "TOTAL",
        "Change in cash and cash equivalents",
        {
            "FY2025": -594.3,
            "FY2024": -987.7,
            "FY2023": 691.3,
            "FY2022": 490.8,
            "FY2021": -205.2,
        },
    ),
    (
        "DATA",
        "Cash and cash equivalents at 1 January",
        {
            "FY2025": 5101.6,
            "FY2024": 6089.3,
            "FY2023": 5398.0,
            "FY2022": 4907.2,
            "FY2021": 5056.3,
        },
    ),
    (
        "TOTAL",
        "Cash and cash equivalents at 31 December",
        {
            "FY2025": 4507.3,
            "FY2024": 5101.6,
            "FY2023": 6089.3,
            "FY2022": 5398.0,
            "FY2021": 4851.1,
        },
    ),
]

bw.add_cash_flow_sheet(
    title="TSB Bank plc — Consolidated Cash Flow Statement",
    subtitle="Bank (Consolidated) basis, £ million unless stated. See source note at bottom (incl. an FY2021/FY2022 restatement break).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=80,
    source_height=220,
    unit_suffix=" (£m)",
)


# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        sources_text,
        note=note,
        first_col_width=52,
        source_height=120,
    )


metric(
    "CET1 Capital",
    "£'000",
    [
        (
            "Common Equity Tier 1 (CET1) capital",
            {
                "FY2025": 1949276,
                "FY2024": 1738133,
                "FY2023": 1842646,
                "FY2022": 1791545,
                "FY2021": 1724002,
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "CET1 Ratio",
    "% of RWA",
    [
        (
            "Common Equity Tier 1 (CET1) ratio",
            {
                "FY2025": "16.74%",
                "FY2024": "15.45%",
                "FY2023": "16.7%",
                "FY2022": "17.2%",
                "FY2021": "15.9%",
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "Tier 1 Capital",
    "£'000",
    [
        (
            "Tier 1 capital",
            {
                "FY2025": 2198973,
                "FY2024": 1987837,
                "FY2023": 1842646,
                "FY2022": 1791545,
                "FY2021": 1724002,
            },
        )
    ],
    p3_sources("6"),
    note="Equal to CET1 capital through FY2023 - TSB held no Additional Tier 1 (AT1) capital until it issued "
    "£249.7m of AT1 securities during FY2024 (see the Cash Flow Statement sheet), which is why Tier 1 "
    "capital first exceeds CET1 capital from FY2024 onward.",
)

metric(
    "Tier 1 Ratio",
    "% of RWA",
    [
        (
            "Tier 1 ratio",
            {
                "FY2025": "18.88%",
                "FY2024": "17.67%",
                "FY2023": "16.7%",
                "FY2022": "17.2%",
                "FY2021": "15.9%",
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "Total Capital",
    "£'000",
    [
        (
            "Total capital",
            {
                "FY2025": 2498973,
                "FY2024": 2287837,
                "FY2023": 2167829,
                "FY2022": 2109761,
                "FY2021": 2024002,
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "Total Capital Ratio",
    "% of RWA",
    [
        (
            "Total capital ratio",
            {
                "FY2025": "21.46%",
                "FY2024": "20.33%",
                "FY2023": "19.6%",
                "FY2022": "20.2%",
                "FY2021": "18.7%",
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "Total RWAs",
    "£'000",
    [
        (
            "Total risk-weighted exposure amount",
            {
                "FY2025": 11646331,
                "FY2024": 11250820,
                "FY2023": 11052751,
                "FY2022": 10442066,
                "FY2021": 10851867,
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "Leverage Ratio",
    "£'000 / %",
    [
        (
            "Leverage ratio total exposure measure excluding claims on central banks",
            {
                "FY2025": 40220383,
                "FY2024": 40126116,
                "FY2023": 40338726,
                "FY2022": 42544451,
                "FY2021": 42569754,
            },
        ),
        (
            "Leverage ratio excluding claims on central banks (%)",
            {
                "FY2025": "5.47%",
                "FY2024": "4.95%",
                "FY2023": "4.57%",
                "FY2022": "4.2%",
                "FY2021": "4.0%",
            },
        ),
        (
            "Leverage ratio total exposure measure including claims on central banks (FY2021 as originally reported, pre-2022 PRA methodology)",
            {"FY2021": 47412008},
        ),
        (
            "Leverage ratio including claims on central banks (%) (FY2021 as originally reported, pre-2022 PRA methodology)",
            {"FY2021": "3.6%"},
        ),
    ],
    p3_sources("6"),
    note="From the PRA Rulebook change effective January 2022, TSB's leverage ratio is calculated excluding "
    "central bank claims; FY2021 figures on that basis (42,569,754 / 4.0%) are a restatement published "
    "as the FY2021 comparator in the FY2022 disclosure, not TSB's own FY2021 report - which itself reported "
    "on the pre-2022 basis including central bank claims (47,412,008 / 3.6%, kept on its own row).",
)

metric(
    "LCR",
    "£'000 / %",
    [
        (
            "Total high-quality liquid assets (HQLA) (weighted value - average)",
            {
                "FY2025": 6476199,
                "FY2024": 6921589,
                "FY2023": 7371627,
                "FY2022": 6788964,
                "FY2021": 6441563,
            },
        ),
        (
            "Cash outflows - total weighted value",
            {
                "FY2025": 3765659,
                "FY2024": 4056488,
                "FY2023": 4134068,
                "FY2022": 4326960,
                "FY2021": 4123393,
            },
        ),
        (
            "Cash inflows - total weighted value",
            {
                "FY2025": 250510,
                "FY2024": 230451,
                "FY2023": 218878,
                "FY2022": 260513,
                "FY2021": 202253,
            },
        ),
        (
            "Total net cash outflows (adjusted value)",
            {
                "FY2025": 3515149,
                "FY2024": 3826038,
                "FY2023": 3915190,
                "FY2022": 4066447,
                "FY2021": 3921140,
            },
        ),
        (
            "Liquidity Coverage Ratio (%)",
            {
                "FY2025": "185%",
                "FY2024": "182%",
                "FY2023": "188%",
                "FY2022": "168%",
                "FY2021": "165%",
            },
        ),
    ],
    p3_sources("6"),
    note="LCR is a twelve-month simple average per TSB's disclosed methodology.",
)

metric(
    "NSFR",
    "£'000 / %",
    [
        (
            "Total available stable funding",
            {
                "FY2025": 40945691,
                "FY2024": 42119435,
                "FY2023": 42368266,
                "FY2022": 42774578,
            },
        ),
        (
            "Total required stable funding",
            {
                "FY2025": 26999917,
                "FY2024": 27582817,
                "FY2023": 27601540,
                "FY2022": 28845131,
            },
        ),
        (
            "Net Stable Funding Ratio (%)",
            {
                "FY2025": "152%",
                "FY2024": "153%",
                "FY2023": "154%",
                "FY2022": "148%",
                "FY2021": "Not disclosed",
            },
        ),
    ],
    p3_sources("6"),
    note="NSFR is a four-quarter simple average per TSB's disclosed methodology. Not disclosed for FY2021: the "
    "PRA's averaging methodology for NSFR was only introduced from 1 January 2022, so no FY2021 comparative "
    "was reported (confirmed explicitly in the FY2022 disclosure). Separately, the FY2024 disclosure's own "
    "FY2023 comparator shows NSFR as 153% rather than the 154% in TSB's own FY2023 disclosure used here - a "
    "1 percentage point drift, most likely rounding/methodology refinement between report vintages rather "
    "than an error; both are reproduced faithfully from their respective source documents.",
)

MREL_SOURCES = (
    "Sources - TSB Banking Group plc consolidated Pillar 3 basis, Section 4.4 'Minimum requirement for own funds "
    "and eligible liabilities (MREL)' (see entity note on Cash Flow Statement sheet):\n"
    f"FY2025: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2025, p.13 - {P3_25_URL}\n"
    f"FY2024: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2024, p.16 - {P3_24_URL}\n"
    f"FY2023: TSB Banking Group plc Large Subsidiary Disclosures 2023, p.16 - {P3_23_URL}\n"
    f"FY2022: TSB Banking Group plc Large Subsidiary Disclosures 2022, p.17 - {P3_22_URL}\n"
    f"FY2021: TSB Banking Group plc Large Subsidiary Disclosures 2021, p.14 - {P3_21_URL}"
)

metric(
    "MREL Ratio",
    "%",
    [
        (
            "MREL ratio",
            {
                "FY2025": "27.04%",
                "FY2024": "28.33%",
                "FY2023": "27.8%",
                "FY2022": "26.9%",
                "FY2021": "22.8%",
            },
        ),
        (
            "Internal MREL requirement (TSB is a UK subsidiary of Banco Sabadell; not a resolution entity in its own right)",
            {
                "FY2025": "23.58%",
                "FY2024": "24.03%",
                "FY2023": "18.4%",
                "FY2022": "16.2%",
                "FY2021": "16.2%",
            },
        ),
    ],
    MREL_SOURCES,
    note="TSB is subject to an internal MREL requirement (not external/resolution-entity MREL) as a UK subsidiary "
    "of Banco Sabadell. The requirement shown is TSB's disclosed internal MREL requirement each year - basis "
    "changed from 'excluding regulatory stress buffers' (FY2021-23) to an all-in figure 'including regulatory "
    "stress buffers' (FY2024-25), per TSB's own wording each year; TSB's MREL ratio exceeded its requirement "
    "in every year shown.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash (used in)/provided by operating activities", {"FY2025": 662.4, "FY2024": 996.9, "FY2023": 1200.7, "FY2022": 596.4, "FY2021": -2145.7}),
        ("Net cash (used in)/provided by investing activities", {"FY2025": -67.2, "FY2024": 21.1, "FY2023": 88.5, "FY2022": -80.3, "FY2021": -839.1}),
        ("Net cash (used in)/provided by financing activities", {"FY2025": -1189.5, "FY2024": -2005.7, "FY2023": -597.9, "FY2022": -25.3, "FY2021": 2779.6}),
        ("Cash and cash equivalents at 31 December", {"FY2025": 4507.3, "FY2024": 5101.6, "FY2023": 6089.3, "FY2022": 5398.0, "FY2021": 4851.1}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.74%", "FY2024": "15.45%", "FY2023": "16.7%", "FY2022": "17.2%", "FY2021": "15.9%"}),
        ("Tier 1 Ratio", {"FY2025": "18.88%", "FY2024": "17.67%", "FY2023": "16.7%", "FY2022": "17.2%", "FY2021": "15.9%"}),
        ("Total Capital Ratio", {"FY2025": "21.46%", "FY2024": "20.33%", "FY2023": "19.6%", "FY2022": "20.2%", "FY2021": "18.7%"}),
        ("Leverage Ratio", {"FY2025": "5.47%", "FY2024": "4.95%", "FY2023": "4.57%", "FY2022": "4.2%", "FY2021": "4.0%"}),
        ("LCR", {"FY2025": "185%", "FY2024": "182%", "FY2023": "188%", "FY2022": "168%", "FY2021": "165%"}),
        ("NSFR", {"FY2025": "152%", "FY2024": "153%", "FY2023": "154%", "FY2022": "148%", "FY2021": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
    "citation for the underlying document/page. Tier 1 capital first exceeds CET1 from FY2024 onward following "
    "TSB's first AT1 issuance that year. Leverage ratio shown on the 'excluding claims on central banks' basis "
    "for comparability across years (FY2021 was originally reported on the pre-2022 'including' basis - see "
    "Leverage Ratio sheet).",
)

bw.save("/Users/armaan/code/katalysis/banks/TSB FINANCIALS.xlsx")
