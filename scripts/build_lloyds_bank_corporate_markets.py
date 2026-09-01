import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR_URLS = {
    "FY2025": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2025/q4/2025-lbcm-annual-report.pdf",
    "FY2024": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2024/q4/2024-lbcm-annual-report.pdf",
    "FY2023": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2023/q4/2023-lbcm-annual-report.pdf",
    "FY2022": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2022/q4/2022-lbcm-annual-report.pdf",
    "FY2021": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2021/2021-lbcm-annual-report.pdf",
}
P3_URLS = {
    "FY2025": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2025/q4/2025-lbcm-fy-pillar-3.pdf",
    "FY2024": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2024/q4/2024-lbcm-fy-pillar-3.pdf",
    "FY2023": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2023/q4/2023-lbcm-fy-pillar-3.pdf",
    "FY2022": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2022/q4/2022-lbcm-fy-pillar-3.pdf",
    "FY2021": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2021/2021-lbcm-fy-pillar3.pdf",
}
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/10399850"

ENTITY_NOTE = (
    "Entity: Lloyds Bank Corporate Markets plc, company number 10399850, FRN 763256, "
    "LEI 213800MBWEIJDM5CU638. Companies House confirms the active bank company. "
    "This is the non-ring-fenced wholesale/markets entity created as part of Lloyds "
    "Banking Group's 2018 ring-fencing restructuring, DISTINCT from the ring-fenced "
    "Lloyds Bank plc (FRN 119278, built separately as 'LLOYDS BANK FINANCIALS.xlsx'). "
    "All figures below are the Bank (solo) column, not the Group consolidated column "
    "also shown in each source document."
)


def annual_sources(kind):
    pages = {
        "annual": {"FY2025": 61, "FY2024": 68, "FY2023": 67, "FY2022": 63, "FY2021": 36},
        "p3": {"FY2025": 4, "FY2024": 4, "FY2023": 4, "FY2022": 5, "FY2021": 5},
    }[kind]
    urls = AR_URLS if kind == "annual" else P3_URLS
    label = "Annual Report and Accounts, Cash flow statements (Bank column)" if kind == "annual" else "Year-End Pillar 3 disclosure, KM1 Key Metrics (Bank-level)"
    return "\n".join(
        [f"{y}: Lloyds Bank Corporate Markets plc {label}, p.{pages[y]} — {urls[y]}" for y in YEARS]
        + [ENTITY_NOTE, f"Companies House — {CH_URL}"]
    )


bw = BankWorkbook("Lloyds Bank Corporate Markets plc", YEARS, header_color="6A1B9A")

cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 583, "FY2024": 468, "FY2023": 399, "FY2022": 436, "FY2021": 293}),
    ("DATA", "Change in operating assets", {"FY2025": 863, "FY2024": -5920, "FY2023": -3331, "FY2022": -1657, "FY2021": 180}),
    ("DATA", "Change in operating liabilities", {"FY2025": -4782, "FY2024": 4619, "FY2023": 3614, "FY2022": -2881, "FY2021": -3502}),
    ("DATA", "Non-cash and other items", {"FY2025": 623, "FY2024": 282, "FY2023": 702, "FY2022": -296, "FY2021": -152}),
    ("DATA", "Tax paid, net", {"FY2025": -87, "FY2024": -84, "FY2023": -96, "FY2022": -58, "FY2021": -38}),
    ("TOTAL", "Net cash provided by/(used in) operating activities", {"FY2025": -2800, "FY2024": -635, "FY2023": 1288, "FY2022": -4456, "FY2021": -3219}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of financial assets", {"FY2024": 0, "FY2023": -3, "FY2022": -27, "FY2021": -85}),
    ("DATA", "Proceeds from sale and maturity of financial assets", {"FY2024": 0, "FY2023": 10, "FY2022": 132, "FY2021": 138}),
    ("DATA", "Purchase of fixed assets", {"FY2025": -3, "FY2024": -2, "FY2023": -2, "FY2022": -5, "FY2021": -1}),
    ("DATA", "Purchase of intangible assets", {"FY2025": 0, "FY2024": -4}),
    ("DATA", "Proceeds from sale of fixed assets", {"FY2025": 0, "FY2024": 1}),
    ("DATA", "Dividends received from subsidiaries", {"FY2022": 22, "FY2021": 44}),
    ("TOTAL", "Net cash provided by/(used in) investing activities", {"FY2025": -3, "FY2024": -5, "FY2023": 5, "FY2022": 122, "FY2021": 96}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid to ordinary shareholders", {"FY2024": -450, "FY2022": -220, "FY2021": -200}),
    ("DATA", "Distributions on other equity instruments", {"FY2025": -210, "FY2024": -78, "FY2023": -80, "FY2022": -43, "FY2021": -33}),
    ("DATA", "Issue of ordinary shares", {"FY2022": 250}),
    ("DATA", "Interest paid on subordinated liabilities", {"FY2025": -24, "FY2024": -54, "FY2023": -58, "FY2022": -25, "FY2021": -16}),
    ("DATA", "Finance leases", {"FY2025": -5, "FY2024": -4, "FY2023": -5, "FY2022": -8}),
    ("DATA", "Proceeds from issue of subordinated liabilities", {"FY2023": 299}),
    ("DATA", "Repayment of subordinated liabilities", {"FY2025": -730, "FY2023": -284}),
    ("DATA", "Loss on repayment of other equity instruments", {"FY2023": -15}),
    ("DATA", "Proceeds from issue of other equity instruments", {"FY2025": 3637, "FY2023": 289}),
    ("DATA", "Repurchases and redemptions of other equity instruments", {"FY2025": -296, "FY2023": -263}),
    ("TOTAL", "Net cash provided by/(used in) financing activities", {"FY2025": 2372, "FY2024": -586, "FY2023": -117, "FY2022": -46, "FY2021": -249}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents", {"FY2025": -521, "FY2024": 116, "FY2023": -403, "FY2022": 693, "FY2021": 69}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2025": -952, "FY2024": -1110, "FY2023": 773, "FY2022": -3687, "FY2021": -3303}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 20633, "FY2024": 21743, "FY2023": 19396, "FY2022": 23083, "FY2021": 26341}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 19681, "FY2024": 20633, "FY2023": 20169, "FY2022": 19396, "FY2021": 23038}),
]

CASH_NOTE = (
    "Two genuine restatements exist between years' opening/closing cash balances; each "
    "year's own originally-published figure is used (not the following year's restated "
    "comparative), per this project's standard convention: (1) FY2021's own report shows "
    "Bank closing cash of £23,038m, but FY2022's own report's FY2021 comparative shows "
    "£23,083m (a £45m gap). (2) FY2023's own report shows Bank closing cash of £20,169m, "
    "but FY2024's own report's FY2023 comparative shows £21,743m (a much larger £1,574m "
    "gap) — flagged prominently as it is the larger of the two and not further explained "
    "in either source document. FY2024→FY2025 and FY2022→FY2023 both tie exactly."
)
bw.add_cash_flow_sheet(
    "Lloyds Bank Corporate Markets plc — Cash Flow Statement",
    "Lloyds Bank Corporate Markets plc, Bank (solo) basis, £m. " + CASH_NOTE,
    cash_rows,
    annual_sources("annual"),
    first_col_width=66,
    unit_suffix=" (£m)",
)

ANNUAL = {
    "CET1 Capital": [3085, 2797, 2725, 2948, 2423],
    "CET1 Ratio": ["13.7%", "13.6%", "13.3%", "14.6%", "13.1%"],
    "Tier 1 Capital": [7137, 3580, 3508, 3705, 3180],
    "Tier 1 Ratio": ["31.8%", "17.4%", "17.1%", "18.3%", "17.2%"],
    "Total Capital": [7137, 4171, 4109, 4285, 3709],
    "Total Capital Ratio": ["31.8%", "20.2%", "20.1%", "21.2%", "20.1%"],
    "Total RWAs": [22442, 20605, 20492, 20195, 18436],
    "Leverage Ratio": ["8.4%", "4.5%", "4.7%", "5.4%", "3.5%"],
    "LCR": ["169%", "168%", "166%", "170%", None],
    "NSFR": ["133%", "138%", "145%", "137%", None],
}
NOTES = {
    "Leverage Ratio": (
        "FY2021's 3.5% is on the original CRR basis (inclusive of claims on central "
        "banks), explicitly confirmed by a footnote in the FY2022 Pillar 3 report. "
        "FY2022 onward are 'excluding claims on central banks' under the revised basis "
        "— a genuine methodology break, not a data error."
    ),
    "NSFR": (
        "FY2021 NSFR was not disclosed at all in that year's Pillar 3 report (the metric "
        "predates this entity's KM1 template). FY2022's 137% was not shown in FY2022's "
        "own report either — recovered from FY2023's own report's FY2022 comparative "
        "column, per this project's standard convention for a metric a bank starts "
        "disclosing only in a later year."
    ),
    "LCR": "FY2021 LCR was not disclosed at all in that year's Pillar 3 report — genuinely absent, not an access gap.",
}
for name, values in ANNUAL.items():
    unit = "%" if "Ratio" in name or name in {"LCR", "NSFR"} else "£m"
    row = [(name, {y: v for y, v in zip(YEARS, values) if v is not None})]
    bw.add_metric_sheet(name, unit, row, annual_sources("p3"), note=NOTES.get(name), first_col_width=58)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    annual_sources("p3"),
    per_note={
        "MREL Ratio": (
            "Each year's own Pillar 3 report explicitly states MREL disclosures for this "
            "entity are made via Template TLAC 2 within Lloyds Banking Group plc's own "
            "consolidated Pillar 3 disclosures, not at this solo entity level — the same "
            "not-a-resolution-entity pattern seen at RBS plc/Coutts & Company/several HSBC "
            "ring-fenced subsidiaries in this project. Group-level MREL figures are not "
            "substituted here."
        )
    },
)

# Sheet 13: Interim Pillar 3
INTERIM_URLS = {
    "2025-Q1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2025/q1/2025-lbcm-q1-pillar-3.pdf",
    "2025-H1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2025/q2/2025-lbcm-hy-pillar-3.pdf",
    "2025-Q3": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2025/q3/2025-lbcm-q3-pillar-3.pdf",
    "2024-Q1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2024/q1/2024-lbcm-q1-pillar-3.pdf",
    "2024-H1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2024/q2/2024-lbcm-hy-pillar-3.pdf",
    "2024-Q3": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2024/q3/2024-lbcm-q3-pillar-3.pdf",
    "2023-Q1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2023/q1/2023-lbcm-q1-pillar-3.pdf",
    "2023-H1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2023/q2/2023-lbcm-hy-pillar-3.pdf",
    "2023-Q3": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2023/q3/2023-lbcm-q3-pillar-3.pdf",
    "2022-Q1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2022/q1/2022-lbcm-q1-pillar-3.pdf",
    "2022-H1": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2022/half-year/2022-lbcm-hy-pillar-3.pdf",
    "2022-Q3": "https://www.lloydsbankinggroup.com/assets/pdfs/investors/financial-performance/lloyds-bank-corporate-markets-plc/2022/q3/2022-lbcm-q3-pillar-3.pdf",
}
# Only H1 (half-year) reports publish the full KM1 table (CET1/Tier 1/Total
# Capital amounts and ratios, plus NSFR). Q1/Q3 reports publish only LR2
# (leverage), OV1 (RWA) and LIQ1 (LCR) — a genuine, source-confirmed scope
# difference from Lloyds Bank plc's own quarterly disclosures, not a gap in
# this project's research. The Q1/Q3 2022 reports additionally omit the
# leverage template entirely (it wasn't yet part of LBCM's quarterly
# disclosure set); NSFR first appears in the Dec-2022 comparative column of
# the 2023-H1 report. No interim (non-year-end) Pillar 3 disclosures exist
# for LBCM in 2021 (confirmed: every 2021 interim URL pattern 404s).
INTERIM_VALUES = {
    "2025-Q1": [None, None, None, 21775, None, None, None, 81263, "4.4%", "166%", None],
    "2025-H1": [2971, 6950, 6950, 22419, "13.3%", "31.0%", "31.0%", 84779, "8.2%", "167%", "132%"],
    "2025-Q3": [None, None, None, 23391, None, None, None, 86981, "8.0%", "168%", None],
    "2024-Q1": [None, None, None, 20805, None, None, None, 76908, "4.6%", "167%", None],
    "2024-H1": [2908, 3691, 4283, 21204, "13.7%", "17.4%", "20.2%", 78930, "4.7%", "168%", "145%"],
    "2024-Q3": [None, None, None, 21229, None, None, None, 79004, "4.4%", "165%", None],
    "2023-Q1": [None, None, None, 20597, None, None, None, 75981, "4.9%", "171%", None],
    "2023-H1": [3055, 3812, 4380, 21079, "14.5%", "18.1%", "20.8%", 76243, "5.0%", "167%", "139%"],
    "2023-Q3": [None, None, None, 21460, None, None, None, 80485, "4.7%", "165%", None],
    "2022-Q1": [None, None, None, 20326, None, None, None, None, None, "166%", None],
    "2022-H1": [2588, 3345, 3941, 20572, "12.6%", "16.3%", "19.2%", 74898, "4.5%", "168%", None],
    "2022-Q3": [None, None, None, 22093, None, None, None, None, None, "169%", None],
}
INTERIM_METRICS = [
    ("CET1 capital", "£m"), ("Tier 1 capital", "£m"), ("Total capital", "£m"),
    ("Total risk-weighted exposure amount", "£m"), ("CET1 ratio", "%"),
    ("Tier 1 ratio", "%"), ("Total capital ratio", "%"),
    ("Total exposure measure excluding claims on central banks", "£m"),
    ("Leverage ratio excluding claims on central banks", "%"),
    ("Average liquidity coverage ratio", "%"), ("Average net stable funding ratio", "%"),
]
interim_rows = []
for period, values in INTERIM_VALUES.items():
    for metric_name, unit, value in [(m, u, v) for (m, u), v in zip(INTERIM_METRICS, values)]:
        if value is None:
            continue
        interim_rows.append([period, "Quarterly/interim Pillar 3 disclosure", metric_name, value, unit, "Lloyds Bank Corporate Markets plc Bank (solo) basis", INTERIM_URLS[period], "KM1/LR2/OV1/LIQ1"])
wide_interim_rows = [row[:6] + [INTERIM_URLS[row[0]], row[7]] for row in interim_rows]
bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=wide_interim_rows,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(wide_interim_rows)},
    title="Lloyds Bank Corporate Markets plc — Interim Pillar 3",
    subtitle="Quarterly and half-year disclosures, 2022–2025 (Bank solo basis)",
    note=(
        "Official LBCM reports publish limited Pillar 3 disclosures at interim quarter "
        "ends and half-year, on the Bank's own (solo) basis. Only the half-year (H1) "
        "reports include the full KM1 table (CET1/Tier 1/Total Capital and their ratios, "
        "plus NSFR); Q1/Q3 reports disclose only LR2 (leverage), OV1 (total RWA) and LIQ1 "
        "(LCR) — confirmed by direct inspection of each report's table of contents, not an "
        "extraction gap. No leverage template was published in the Q1/Q3 2022 reports "
        "(first appears from the 2022 half-year report onward). NSFR was not disclosed "
        "before the 31 December 2022 comparative shown in the 2023 half-year report. No "
        "interim (non-year-end) Pillar 3 disclosures exist for LBCM for 2021 — confirmed "
        "via direct URL-pattern checks against the same archive structure used for "
        "2022–2025, all of which 404."
    ),
)

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash provided by/(used in) operating activities", {"FY2025": -2800, "FY2024": -635, "FY2023": 1288, "FY2022": -4456, "FY2021": -3219}),
        ("Net cash provided by/(used in) investing activities", {"FY2025": -3, "FY2024": -5, "FY2023": 5, "FY2022": 122, "FY2021": 96}),
        ("Net cash provided by/(used in) financing activities", {"FY2025": 2372, "FY2024": -586, "FY2023": -117, "FY2022": -46, "FY2021": -249}),
        ("Cash and cash equivalents at end of year", {"FY2025": 19681, "FY2024": 20633, "FY2023": 20169, "FY2022": 19396, "FY2021": 23038}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {y: v for y, v in zip(YEARS, ANNUAL["CET1 Ratio"])}),
        ("Tier 1 Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Tier 1 Ratio"])}),
        ("Total Capital Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Total Capital Ratio"])}),
        ("Leverage Ratio", {y: v for y, v in zip(YEARS, ANNUAL["Leverage Ratio"])}),
    ],
    note="All figures are Lloyds Bank Corporate Markets plc's own Bank (solo) basis, not the wider Lloyds Banking Group.",
)

bw.save("/Users/armaan/code/katalysis/banks/LLOYDS BANK CORPORATE MARKETS FINANCIALS.xlsx")
print("Saved.")
