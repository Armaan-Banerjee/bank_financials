import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: J.P. Morgan Securities plc ("JPMS plc", company 02711006,
# FRN 155240) is JPMorgan Chase & Co.'s principal UK operating subsidiary for
# Markets and Banking (investment banking advisory, equity/debt securities,
# derivatives, clearing). Its FY2025 Annual Report confirms it applies the FRS 101
# exemption from IAS 7 "Cash flow statement and related notes" (Note 2, Basis of
# preparation) - its largest and smallest parent groups (J.P. Morgan Capital
# Holdings Limited and ultimately JPMorgan Chase & Co.) publish consolidated cash
# flow statements instead. No Statement of Cash Flows appears anywhere in the
# Annual Report's own Contents page. Per the project's established policy for this
# exemption (see The Bank of New York Mellon (International) Limited / ABC
# International Bank plc / Bank Mandiri (Europe) Limited / DB UK Bank Limited),
# this is built as a PILLAR-3-ONLY workbook.
#
# Reports in USD ('000s) - the Company's functional currency (equity capital is
# held in USD per its own FX-risk-to-capital-ratio note). Point-in-time capital/RWA
# figures converted to GBP at each year-end's Bank of England GBP/USD spot rate,
# using the same rate table established for Zenith Bank (UK) Limited/other FX
# banks in this project; %-ratios are dimensionless and left unconverted.
#
# The official JPMorgan archive was recoverable in this revisit and exposes
# standalone JPMS plc annual Pillar 3 disclosures for FY2021-FY2025. These
# reports support the historical capital, RWA, leverage and LCR series directly;
# NSFR is supported from FY2022 onward. No standalone numeric MREL ratio is
# reported in the recovered disclosures, so that sheet remains explicitly
# unavailable rather than being inferred from subordinated capital instruments.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/02711006/filing-history/MzUxOTQxNzUzOGFkaXF6a2N4/document?format=pdf&download=0"
P3_ARCHIVE_URL = "https://jpmorganchaseco.gcs-web.com/financial-information/basel-pillar-3-us-lcr-disclosures"

FX_SPOT = {  # Bank of England GBP/USD spot rate, 31 December each year (USD per £1)
    "FY2021": 1.3521,
    "FY2022": 1.2097,
    "FY2023": 1.2732,
    "FY2024": 1.2515,
    "FY2025": 1.3448,
}


def stock(usd):
    """Point-in-time (capital/RWA) USD '000s -> GBP '000s at that year-end's spot rate."""
    return {y: round(v / FX_SPOT[y]) for y, v in usd.items()}


ENTITY_NOTE = (
    "ENTITY NOTE: J.P. Morgan Securities plc (\"JPMS plc\", company 02711006, FRN 155240, incorporated 30 April "
    "1992) is a public limited company, an indirect subsidiary of JPMorgan Chase Bank, N.A. and a principal "
    "operating subsidiary of JPMorgan Chase & Co. (\"the Firm\") in the UK, engaged in international investment "
    "banking activity across Markets (client-facing and trading entity for the majority of Markets EMEA ex EU) and "
    "Banking (primary M&A advisory entity). It also operates a branch in Zurich. FY2025: $831bn total assets, $50bn "
    "total equity, $9,542,478k net operating income - Annual Report 2025, Strategic Report p.2. All monetary "
    "figures below are the Company's own entity-level (not the wider JPMorgan Chase Group's consolidated) "
    "disclosure, reported in USD, converted to GBP at each year-end's spot rate (see FX_SPOT table) for point-in-"
    "time capital/RWA figures; %-ratios are shown exactly as reported (dimensionless, not converted)."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: the FY2025 Annual Report's Note 2 \"Basis of preparation\" states these financial "
    "statements are prepared under FRS 101 'Reduced Disclosure Framework' and lists the IFRS exemptions applied, "
    "including \"Cash flow statement and related notes, IAS 7 'Cash flow statements'\" - Annual Report 2025, Note "
    f"2, p.61 - {AR2025_URL}. The Annual Report's own Contents page (p.i) does not list a Statement of Cash Flows "
    "anywhere among its financial statements (Income statement p.57, Statement of comprehensive income p.58, "
    "Balance sheet p.59, Statement of changes in equity p.60, Notes p.61-112 - no cash flow statement). Note 1 "
    "confirms the Company's results are consolidated into both J.P. Morgan Capital Holdings Limited's accounts "
    "(smallest group) and JPMorgan Chase & Co.'s accounts (largest group), both of which publish their own "
    "consolidated cash flow statements. Per the project's established policy for this exemption, this workbook is "
    "built as a PILLAR-3-ONLY variant: no cash flow figures exist to show, while the recovered capital and liquidity "
    "metrics are populated below."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

ACCESS_GAP_NOTE = (
    "SOURCE COVERAGE NOTE: the official JPMorgan archive exposes standalone annual JPMS plc Pillar 3 disclosures "
    "for FY2021, FY2022, FY2023, FY2024 and FY2025. The FY2021 report uses the older Key Metrics format and does "
    "not provide an NSFR series; the FY2022 report provides FY2022 NSFR but not a FY2021 NSFR comparative. The "
    "recovered reports describe the MREL framework and capital instruments issued in support of the Firm's MREL "
    "strategy, but do not provide a JPMS plc numeric MREL ratio or requirement."
)

P3_2021_URL = "https://jpmorganchaseco.gcs-web.com/static-files/41a50bf4-81db-4063-8e55-8703a0fc500f"
P3_2022_URL = "https://jpmorganchaseco.gcs-web.com/static-files/d761ba10-ab1b-4309-8a4d-24cb70fd6cc1"
P3_2023_URL = "https://jpmorganchaseco.gcs-web.com/static-files/3645e9a4-c721-404e-a901-70fa73fac642"
P3_2024_URL = "https://jpmorganchaseco.gcs-web.com/static-files/a170e6df-d951-42fc-9897-2aa04d681885"
P3_2025_URL = "https://jpmorganchaseco.gcs-web.com/static-files/a51475c0-d908-423e-b8de-6410d277a867"


def p3_sources():
    return (
        "Sources - J.P. Morgan Securities plc, all $'000 figures converted to £'000 at the Bank of England GBP/USD "
        f"spot rate as at each year-end (FY2021: 1.3521, FY2022: 1.2097, FY2023: 1.2732, FY2024: 1.2515, FY2025: 1.3448):\n"
        f"FY2025: Annual Pillar 3 Disclosure 2025, UK KM1 Table 1 - {P3_2025_URL}\n"
        f"FY2024: Annual Pillar 3 Disclosure 2024, UK KM1 Table 1 - {P3_2024_URL}\n"
        f"FY2023: Annual Pillar 3 Disclosure 2023, UK KM1 Table 1 - {P3_2023_URL}\n"
        f"FY2022: Annual Pillar 3 Disclosure 2022, UK KM1 Table 4 - {P3_2022_URL}\n"
        f"FY2021: Annual Pillar 3 Disclosure 2021, Key Metrics Table 1 and LCR Table 47 - {P3_2021_URL}\n"
        f"FY2025/FY2024 capital precision cross-check: Annual Report 2025, Strategic Report, \"Capital risk\" table, p.10 - {AR2025_URL}\n\n"
        + ACCESS_GAP_NOTE
    )


bw = BankWorkbook(bank_name="J.P. Morgan Securities plc", years=YEARS, year_label=YEAR_LABEL, header_color="C104D3")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (not applicable - FRS 101 exemption)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Not applicable", {}),
    ("DATA", "J.P. Morgan Securities plc takes the FRS 101 exemption from preparing a Statement of Cash Flows "
             "(IAS 7) every year covered by this workbook - see source note below.", {}),
]

bw.add_cash_flow_sheet(
    title="J.P. Morgan Securities plc — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=260,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=140)


CET1_USD = {
    "FY2025": 37434585,
    "FY2024": 36053977,
    "FY2023": 34321000,
    "FY2022": 39571000,
    "FY2021": 41911000,
}
TIER1_USD = {
    "FY2025": 47434585,
    "FY2024": 46053977,
    "FY2023": 44321000,
    "FY2022": 44571000,
    "FY2021": 41911000,
}
TOTAL_CAP_USD = {
    "FY2025": 55987951,
    "FY2024": 55806030,
    "FY2023": 55230000,
    "FY2022": 56571000,
    "FY2021": 53911000,
}
RWA_USD = {
    "FY2025": 227965642,
    "FY2024": 195273360,
    "FY2023": 187226000,
    "FY2022": 166720000,
    "FY2021": 226258000,
}

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", stock(CET1_USD))],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2025": "16.4%", "FY2024": "18.5%", "FY2023": "18.33%",
        "FY2022": "23.73%", "FY2021": "18.52%",
    })],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Total Tier 1 capital (CET1 and Additional Tier 1)", stock(TIER1_USD))],
    p3_sources(),
    note="The source disclosures show no AT1 in FY2021, $5,000,000k in FY2022, and $10,000,000k from FY2023 onward; "
         "the Tier 1 series includes those directly reported AT1 instruments.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 capital ratio", {
        "FY2025": "20.8%", "FY2024": "23.6%", "FY2023": "23.67%",
        "FY2022": "26.73%", "FY2021": "18.52%",
    })],
    p3_sources(),
)

metric(
    "Total Capital", "£'000",
    [("Total capital (CET1, Additional Tier 1 and Tier 2)", stock(TOTAL_CAP_USD))],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {
        "FY2025": "24.6%", "FY2024": "28.6%", "FY2023": "29.50%",
        "FY2022": "33.93%", "FY2021": "23.83%",
    })],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total Risk Weighted Assets (RWA)", stock(RWA_USD))],
    p3_sources(),
    note="Comprises Credit RWAs, Market RWAs and Operational RWAs - Annual Report 2025 p.10 gives the full "
         "breakdown (not reproduced here; this sheet shows the total only, consistent with other banks in this "
         "project's Total RWAs sheet).",
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Leverage exposure", stock({
            "FY2025": 757149645, "FY2024": 607589034, "FY2023": 572319000,
            "FY2022": 580992000, "FY2021": 729749000,
        })),
        ("Leverage ratio (%)", {
            "FY2025": "6.3%", "FY2024": "7.6%", "FY2023": "7.74%",
            "FY2022": "7.67%", "FY2021": "5.74%",
        }),
    ],
    p3_sources(),
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA) (weighted value - average)", stock({
            "FY2025": 124463000, "FY2024": 101202000, "FY2023": 78544000,
            "FY2022": 76119000, "FY2021": 71625000,
        })),
        ("Cash outflows - total weighted value", stock({
            "FY2025": 171627000, "FY2024": 143440000, "FY2023": 136030000,
            "FY2022": 145955000,
        })),
        ("Cash inflows - total weighted value", stock({
            "FY2025": 97895000, "FY2024": 89342000, "FY2023": 106007000,
            "FY2022": 121958000,
        })),
        ("Total net cash outflows (adjusted value)", stock({
            "FY2025": 73732000, "FY2024": 54098000, "FY2023": 35384000,
            "FY2022": 36489000, "FY2021": 33228000,
        })),
        ("Liquidity coverage ratio", {
            "FY2025": "174.25%", "FY2024": "192.75%", "FY2023": "222.82%",
            "FY2022": "208.50%", "FY2021": "216%",
        }),
    ],
    p3_sources(),
    note="FY2021's older LCR table reports liquidity buffer and total net cash outflows but does not separately report the cash-outflow and cash-inflow components; those two cells are intentionally blank for FY2021.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", stock({
            "FY2025": 222212000, "FY2024": 205106000, "FY2023": 171918000,
            "FY2022": 171384000,
        })),
        ("Total required stable funding", stock({
            "FY2025": 187812000, "FY2024": 175883000, "FY2023": 147370000,
            "FY2022": 142084000,
        })),
        ("NSFR ratio", {
            "FY2025": "118.55%", "FY2024": "117.56%", "FY2023": "116.64%",
            "FY2022": "121.09%",
        }),
    ],
    p3_sources(),
    note="The FY2021 standalone disclosure does not contain an NSFR series; the recovered FY2022 disclosure provides NSFR from FY2022 onward but no FY2021 comparative.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "The recovered standalone disclosures describe the MREL framework and identify subordinated instruments issued in support of the Firm's MREL strategy, but no JPMS plc numeric MREL ratio or requirement is reported. No ratio is inferred from the capital instruments.",
    },
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.4%", "FY2024": "18.5%", "FY2023": "18.33%", "FY2022": "23.73%", "FY2021": "18.52%"}),
        ("Tier 1 Ratio", {"FY2025": "20.8%", "FY2024": "23.6%", "FY2023": "23.67%", "FY2022": "26.73%", "FY2021": "18.52%"}),
        ("Total Capital Ratio", {"FY2025": "24.6%", "FY2024": "28.6%", "FY2023": "29.50%", "FY2022": "33.93%", "FY2021": "23.83%"}),
        ("Leverage Ratio", {"FY2025": "6.3%", "FY2024": "7.6%", "FY2023": "7.74%", "FY2022": "7.67%", "FY2021": "5.74%"}),
        ("LCR", {"FY2025": "174.25%", "FY2024": "192.75%", "FY2023": "222.82%", "FY2022": "208.50%", "FY2021": "216%"}),
        ("NSFR", {"FY2025": "118.55%", "FY2024": "117.56%", "FY2023": "116.64%", "FY2022": "121.09%"}),
    ],
    note="This is a PILLAR-3-ONLY workbook: J.P. Morgan Securities plc takes the FRS 101 cash-flow-statement exemption every year (see the Cash Flow Statement sheet), so no cash-flow summary or chart is shown here. The recovered archive provides standalone JPMS plc capital, leverage and LCR data for FY2021-FY2025, NSFR data for FY2022-FY2025, and no numeric MREL ratio.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/JP MORGAN SECURITIES FINANCIALS.xlsx")
