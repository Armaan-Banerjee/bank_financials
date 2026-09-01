import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# STANDARD CHARTERED BANK (ZC000018 / FRN 114276)
# The annual reports provide distinct Group and Company columns.  Cash-flow
# values below are the standalone Bank Company column.  Regulatory capital
# disclosures in the reports are explicitly for Standard Chartered Bank Group
# on a solo-consolidated basis (including four subsidiaries), so Group Pillar 3
# figures are intentionally not imported into this Bank-level workbook.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

REPORTS = {
    "FY2025": "https://www.sc.com/en/uploads/sites/66/content/docs/sc-bank-2025-report.pdf",
    "FY2024": "https://www.sc.com/en/uploads/sites/66/content/docs/sc-bank-2024-results.pdf",
    "FY2023": "https://www.sc.com/EN/uploads/sites/66/content/docs/sc-bank-2023-annual-report.pdf",
    "FY2022": "https://www.sc.com/en/uploads/sites/66/content/docs/sc-bank-2022-annual-report.pdf",
    "FY2021": "https://www.sc.com/EN/uploads/sites/66/content/docs/sc-bank-2021-results.pdf",
}
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/ZC000018/filing-history"

ENTITY_NOTE = (
    "ENTITY AND BASIS: Standard Chartered Bank (Companies House Royal Charter reference ZC000018, FRN 114276) "
    "is incorporated in England with limited liability by Royal Charter 1853. The source reports distinguish "
    "Standard Chartered Bank Group (the Bank and subsidiaries) from Standard Chartered Bank Company (the "
    "standalone legal entity). All cash-flow rows in this workbook use the Company column only."
)

REGULATORY_GAP_NOTE = (
    "REGULATORY BASIS LIMITATION: the reports state that capital disclosures are provided on the Standard "
    "Chartered Bank Group basis and that PRA requirements are set on a solo-consolidated basis. That basis includes "
    "four subsidiaries (Standard Chartered Holdings (International) B.V., Standard Chartered Grindlays Pty "
    "Limited, SCMB Overseas Limited and Corrasi Covered Bonds LLP). No complete five-year standalone Company KM1 "
    "series was located. Group Pillar 3/capital figures have therefore not been substituted for the requested "
    "Bank-level series."
)

SOURCE_NOTE = (
    "Sources - standalone Standard Chartered Bank Company cash flows, $million:\n"
    "FY2025: Directors' Report and Financial Statements 2025, cash flow statement p.89 - " + REPORTS["FY2025"] + "\n"
    "FY2024: Directors' Report and Financial Statements 2024, cash flow statement p.89 - " + REPORTS["FY2024"] + "\n"
    "FY2023: Directors' Report and Financial Statements 2023, cash flow statements p.165 - " + REPORTS["FY2023"] + "\n"
    "FY2022: Directors' Report and Financial Statements 2022, cash flow statements p.172 - " + REPORTS["FY2022"] + "\n"
    "FY2021: Directors' Report and Financial Statements 2021, cash flow statements p.172 - " + REPORTS["FY2021"] + "\n"
    "Entity filing history and identity: Companies House ZC000018 - " + CH_URL + "\n\n" + ENTITY_NOTE
)

bw = BankWorkbook(
    bank_name="Standard Chartered Bank (standalone Company basis)",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="005A70",
)

# Company column only.  FY2022 uses the 2022 report's own as-reported figures;
# the 2023 report restated the FY2022 comparative, so the discontinuity is
# documented in the source note below.
CF = {
    "Profit before taxation": {"FY2025": 3245, "FY2024": 3058, "FY2023": 3088, "FY2022": 2996, "FY2021": 2496},
    "Adjustments for non-cash items and other adjustments": {"FY2025": -429, "FY2024": -1, "FY2023": -790, "FY2022": 381, "FY2021": -659},
    "Change in operating assets": {"FY2025": 273, "FY2024": -26161, "FY2023": 23104, "FY2022": -5451, "FY2021": -1178},
    "Change in operating liabilities": {"FY2025": 11452, "FY2024": 13864, "FY2023": -13891, "FY2022": 4521, "FY2021": 18902},
    "Contributions to defined benefit schemes": {"FY2025": -46, "FY2024": -39, "FY2023": -46, "FY2022": -36, "FY2021": -82},
    "UK and overseas taxes paid": {"FY2025": -711, "FY2024": -720, "FY2023": -658, "FY2022": -359, "FY2021": -274},
    "Net cash from/(used in) operating activities": {"FY2025": 13784, "FY2024": -9999, "FY2023": 10807, "FY2022": 2052, "FY2021": 19205},
    "Internally generated capitalised software": {"FY2025": -521, "FY2024": -246, "FY2023": -378, "FY2022": -501, "FY2021": -503},
    "Purchase of property, plant and equipment": {"FY2025": -149, "FY2024": -176, "FY2023": -53, "FY2022": -59, "FY2021": -67},
    "Disposal of property, plant and equipment": {"FY2025": 3, "FY2024": 15, "FY2023": 1, "FY2022": 14, "FY2021": 6},
    "Dividends received from subsidiaries, associates and joint ventures": {"FY2025": 1260, "FY2024": 1052, "FY2023": 2060, "FY2022": 1046, "FY2021": 1626},
    "Disposals of subsidiaries, associates and joint ventures / held-for-sale assets": {"FY2025": 0, "FY2024": 26, "FY2023": 108, "FY2022": 0, "FY2021": 0},
    "Purchase of investment securities": {"FY2025": -68809, "FY2024": -84630, "FY2023": -91970, "FY2022": -114671, "FY2021": -131168},
    "Disposal and maturity of investment securities": {"FY2025": 72962, "FY2024": 91907, "FY2023": 97216, "FY2022": 98999, "FY2021": 113905},
    "Net cash from/(used in) investing activities": {"FY2025": 4746, "FY2024": 7948, "FY2023": 6984, "FY2022": -15172, "FY2021": -16201},
    "Premises and equipment lease liability principal payment": {"FY2025": -42, "FY2024": -43, "FY2023": -45, "FY2022": -78, "FY2021": -72},
    "Issue of ordinary and preference share capital, net of expenses": {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 1273},
    "Cancellation of shares including share buyback": {"FY2025": 0, "FY2024": 0, "FY2023": -750, "FY2022": 0, "FY2021": 0},
    "Issue of Additional Tier 1 capital, net of expenses": {"FY2025": 0, "FY2024": 980, "FY2023": 992, "FY2022": 1000, "FY2021": 2750},
    "Redemption of Tier 1 capital": {"FY2025": 0, "FY2024": 0, "FY2023": -1000, "FY2022": -999, "FY2021": -1042},
    "Gross proceeds from issue of subordinated liabilities": {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 750, "FY2021": 0},
    "Interest paid on subordinated liabilities": {"FY2025": -492, "FY2024": -528, "FY2023": -583, "FY2022": -378, "FY2021": -456},
    "Repayment of subordinated liabilities": {"FY2025": -2173, "FY2024": -1000, "FY2023": -2160, "FY2022": -1008, "FY2021": -16},
    "Proceeds from issue of senior debts": {"FY2025": 2455, "FY2024": 3114, "FY2023": 4820, "FY2022": 4091, "FY2021": 660},
    "Repayment of senior debts": {"FY2025": -3986, "FY2024": -2471, "FY2023": -1806, "FY2022": -298, "FY2021": -422},
    "Interest paid on senior debts": {"FY2025": -374, "FY2024": -282, "FY2023": -235, "FY2022": -1, "FY2021": -16},
    "Distributions and dividends paid to preference shareholders and AT1 securities": {"FY2025": -389, "FY2024": -349, "FY2023": -363, "FY2022": -311, "FY2021": -292},
    "Dividends paid to ordinary shareholders": {"FY2025": -2276, "FY2024": -2395, "FY2023": -2599, "FY2022": -575, "FY2021": -1511},
    "Net cash used in financing activities": {"FY2025": -7277, "FY2024": -2974, "FY2023": -3729, "FY2022": 2193, "FY2021": 856},
    "Net increase/(decrease) in cash and cash equivalents": {"FY2025": 11253, "FY2024": -5025, "FY2023": 14062, "FY2022": -10927, "FY2021": 3860},
    "Cash and cash equivalents at beginning of year": {"FY2025": 48101, "FY2024": 53988, "FY2023": 40264, "FY2022": 59406, "FY2021": 56151},
    "Effect of exchange rate movements on cash and cash equivalents": {"FY2025": -64, "FY2024": -862, "FY2023": -338, "FY2022": -861, "FY2021": -605},
    "Cash and cash equivalents at end of year": {"FY2025": 59290, "FY2024": 48101, "FY2023": 53988, "FY2022": 47618, "FY2021": 59406},
}

cash_rows = []
for label in list(CF):
    if label == "Profit before taxation":
        cash_rows.append(("SECTION", "Cash flows from operating activities", {}))
    elif label == "Internally generated capitalised software":
        cash_rows.append(("SECTION", "Cash flows from investing activities", {}))
    elif label == "Premises and equipment lease liability principal payment":
        cash_rows.append(("SECTION", "Cash flows from financing activities", {}))
    elif label == "Net increase/(decrease) in cash and cash equivalents":
        cash_rows.append(("SECTION", "Cash and cash equivalents reconciliation", {}))
    kind = "TOTAL" if label.startswith("Net cash") or label.startswith("Cash and cash") or label.startswith("Net increase") else "DATA"
    cash_rows.append((kind, label, CF[label]))

bw.add_cash_flow_sheet(
    title="Standard Chartered Bank — Cash Flow Statement",
    subtitle="Standalone Bank Company column, $million; Group figures deliberately excluded.",
    rows=cash_rows,
    sources_text=SOURCE_NOTE + "\n\n" + REGULATORY_GAP_NOTE + "\n\nNote: the FY2023 report restates FY2022 cash-flow comparatives; FY2022 above preserves the FY2022 report's own as-reported Company figures.",
    first_col_width=72,
    source_height=260,
    unit_suffix="",
)


def unavailable(name, note):
    bw.add_metric_sheet(
        name,
        "$million / %",
        [(name + " — standalone Bank Company basis", {y: "Not publicly disclosed" for y in YEARS})],
        SOURCE_NOTE + "\n\n" + REGULATORY_GAP_NOTE,
        note=note,
        first_col_width=58,
        source_height=230,
    )


for metric_name in [
    "CET1 Capital", "CET1 Ratio", "Tier 1 Capital", "Tier 1 Ratio",
    "Total Capital", "Total Capital Ratio", "Total RWAs", "Leverage Ratio",
    "LCR", "NSFR", "MREL Ratio",
]:
    unavailable(
        metric_name,
        "No complete five-year standalone Company regulatory series was located in the Bank reports. The available "
        "capital review and Pillar 3 materials use the Bank Group solo-consolidated basis; those figures are not "
        "appropriate substitutes for this Bank-level workbook.",
    )

bw.add_overview_sheet(
    cash_flow_totals=[("Net cash from/(used in) operating activities", CF["Net cash from/(used in) operating activities"]),
                      ("Net cash from/(used in) investing activities", CF["Net cash from/(used in) investing activities"]),
                      ("Net cash used in financing activities", CF["Net cash used in financing activities"]),
                      ("Net increase/(decrease) in cash and cash equivalents", CF["Net increase/(decrease) in cash and cash equivalents"])],
    cash_flow_unit="$million",
    ratios=[],
    note=(
        "Annual standalone Company cash flows are available for FY2021-FY2025. Regulatory metric sheets are left "
        "as not publicly disclosed because the available regulatory capital basis is Bank Group solo-consolidated, "
        "not the standalone Company. No Bank-level interim metrics sufficient to justify a 14th worksheet were proven."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/STANDARD CHARTERED BANK FINANCIALS.xlsx")
