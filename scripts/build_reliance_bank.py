import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022"]
AR_URLS = {
    "FY2026": "https://find-and-update.company-information.service.gov.uk/company/00068835/filing-history/MzUzNTUyMDU0NWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/00068835/filing-history/MzQ3NTMwMjc2NGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": "https://find-and-update.company-information.service.gov.uk/company/00068835/filing-history/MzQzMDIwODk2MGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/00068835/filing-history/MzM5NDkwNzg3NmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": "https://find-and-update.company-information.service.gov.uk/company/00068835/filing-history/MzM1MjMwMDYyNWFkaXF6a2N4/document?format=pdf&download=0",
}
P3_2023_URL = "https://www.reliancebankltd.com/wp-content/uploads/2023/10/RBL-Pillar-3-Disclosures-31-March-2023-for-website-30Oct2023.pdf"

ENTITY_NOTE = (
    "Reliance Bank Limited (Companies House 00068835; FRN 204537) is the bank in the supplied bank list. "
    "The statements are the Bank's own entity accounts in £. The latest five available years are FY2022-FY2026 "
    "(31 March year ends). All Companies House reports were image-only scans and were transcribed after rendering/OCR. "
    "The 2024 accounts restate the 2023 cash-flow comparative (operating cash £(27,740,745) versus £(28,182,841) "
    "reported in the 2023 accounts), following a money-market-fund reclassification. Per project convention, each "
    "year uses its own originally published figures; the restatement is documented rather than silently applied. "
    "The FY2026 operating subtotal is £67,891 higher than its listed adjustments and its reported operating total "
    "is £67,891 lower than subtotal plus listed changes; FY2022 has £1 differences in both places. These are shown "
    "as source arithmetic differences, not estimates."
)
CASH_SOURCES = "Sources - Reliance Bank Limited entity cash flows, £:\n" + "\n".join(
    f"{y}: Annual Report and Accounts for year ended 31 March {y[-4:]}, cash-flow statement and notes 23-25, {AR_URLS[y]}"
    for y in YEARS
) + "\n\n" + ENTITY_NOTE

bw = BankWorkbook(bank_name="Reliance Bank Limited", years=YEARS, header_color="0F5B78")
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax / operating loss", {"FY2026": 1097804, "FY2025": 1431126, "FY2024": 1918412, "FY2023": 233945, "FY2022": -749645}),
    ("DATA", "Add back revaluation of investment property", {"FY2023": 128301}),
    ("DATA", "Movement in provision for bad debts", {"FY2026": 230821, "FY2025": 83855, "FY2024": 9455, "FY2023": -221048, "FY2022": 16412}),
    ("DATA", "Movement in value of debt securities/investments", {"FY2026": 169844, "FY2025": 372879, "FY2024": 386849, "FY2023": -813173, "FY2022": 179932}),
    ("DATA", "Amortisation of intangible fixed assets", {"FY2026": 71120, "FY2025": 116162, "FY2024": 175719, "FY2023": 202157, "FY2022": 203839}),
    ("DATA", "Depreciation of tangible fixed assets", {"FY2026": 370918, "FY2025": 373648, "FY2024": 262446, "FY2023": 163234, "FY2022": 156387}),
    ("DATA", "Other operating items included in reported subtotal (source arithmetic difference)", {"FY2026": 67891, "FY2022": 1}),
    ("DATA", "(Decrease)/increase in prepayments and accrued income", {"FY2026": 111310, "FY2025": -142965, "FY2024": -274, "FY2023": 54848, "FY2022": -34482}),
    ("DATA", "(Decrease)/increase in accruals and deferred income", {"FY2026": 0, "FY2025": -915795, "FY2024": 722273, "FY2023": 303630, "FY2022": -64396}),
    ("DATA", "(Decrease)/increase in other liabilities", {"FY2026": -132129, "FY2025": 8354, "FY2024": -13969, "FY2023": -7297, "FY2022": 26197}),
    ("DATA", "(Increase)/decrease in other assets", {"FY2026": -47072, "FY2025": -11150, "FY2024": -524, "FY2023": 9499, "FY2022": -4671}),
    ("TOTAL", "Cash flows from operating activities before changes in operating assets and liabilities", {"FY2026": 1940507, "FY2025": 1316114, "FY2024": 3460387, "FY2023": 54096, "FY2022": -270426}),
    ("DATA", "Increase in loans and advances to customers", {"FY2026": -4886899, "FY2025": -16375104, "FY2024": -6940602, "FY2023": -22074877, "FY2022": -19032850}),
    ("DATA", "Increase/(decrease) in customer accounts", {"FY2026": 12880730, "FY2025": -10991390, "FY2024": 22178943, "FY2023": -6162060, "FY2022": 4708736}),
    ("DATA", "Other operating items included in reported operating cash total (source arithmetic difference)", {"FY2026": -67891, "FY2022": 1}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2026": 9866447, "FY2025": -26050380, "FY2024": 18698728, "FY2023": -28182841, "FY2022": -14594539}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Sale and maturity of debt securities", {"FY2026": 66320081, "FY2025": 74717939, "FY2024": 54372721, "FY2023": 49694094, "FY2022": 33000000}),
    ("DATA", "Purchase of debt securities", {"FY2026": -83182860, "FY2025": -80507526, "FY2024": -47513462, "FY2023": -47661362, "FY2022": -26840989}),
    ("DATA", "Purchase of intangible fixed assets", {"FY2026": -23026, "FY2025": -143693, "FY2024": -39045, "FY2023": -43194, "FY2022": -254508}),
    ("DATA", "Purchase of tangible fixed assets", {"FY2026": -105786, "FY2025": -758943, "FY2024": -72957, "FY2023": -215926, "FY2022": -26765}),
    ("DATA", "Movement in interest on security deposit", {"FY2026": 840758, "FY2025": 4899, "FY2024": -23038, "FY2023": -7249}),
    ("DATA", "Net movement in loans and advances to banks not recoverable on demand", {"FY2022": 14498971}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2026": -16150833, "FY2025": -6687324, "FY2024": 6724219, "FY2023": 1766363, "FY2022": 20376709}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Issue of ordinary shares", {"FY2026": 5000000, "FY2023": 7000000, "FY2022": 3000000}),
    ("DATA", "Distribution to parent company/Salvation Army", {"FY2026": -400000, "FY2025": -100000, "FY2024": -100000}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2026": 4600000, "FY2025": -100000, "FY2024": -100000, "FY2023": 7000000, "FY2022": 3000000}),
    ("TOTAL", "Increase/(decrease) in cash and cash equivalents", {"FY2026": -1684386, "FY2025": -32837704, "FY2024": 25322947, "FY2023": -19416478, "FY2022": 8782169}),
    ("DATA", "Cash and cash equivalents at 1 April/beginning of reporting period", {"FY2026": 87080370, "FY2025": 119918074, "FY2024": 94595127, "FY2023": 114011605, "FY2022": 105229436}),
    ("TOTAL", "Cash and cash equivalents at 31 March/end of reporting period", {"FY2026": 85395984, "FY2025": 87080370, "FY2024": 119918074, "FY2023": 94595127, "FY2022": 114011606}),
]
bw.add_cash_flow_sheet(
    title="Reliance Bank Limited - Entity Cash Flow Statement",
    subtitle="Entity basis, £; five latest available financial years FY2026-FY2022. See source note.",
    rows=rows, sources_text=CASH_SOURCES, first_col_width=70, source_height=220, unit_suffix=" (£)",
)

P3_SOURCES = (
    f"Reliance Bank Pillar 3 Disclosure for 31 March 2023, KM1/capital and risk disclosures, {P3_2023_URL}\n"
    "Reliance Bank Annual Reports and Accounts FY2022-FY2026, Strategic Report capital/liquidity sections and KPI tables, "
    + "; ".join(AR_URLS[y] for y in YEARS) + "\n"
    "Blank cells mean the metric was not explicitly disclosed; no capital amount, RWA, NSFR or MREL figure has been inferred."
)
def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, P3_SOURCES, note=note, first_col_width=54, source_height=180)

metric("CET1 Capital", "£", [("CET1 capital", {})], "The reviewed annual reports and 2023 Pillar 3 disclosure provide the CET1 ratio but no explicit absolute CET1 capital amount.")
metric("CET1 Ratio", "% of RWA", [("CET1 ratio", {"FY2026": "21.8%", "FY2025": "19.9%", "FY2024": "20.7%", "FY2023": "23.1%", "FY2022": "18.2%"})])
metric("Tier 1 Capital", "£", [("Tier 1 capital", {})], "Not publicly disclosed as an absolute amount; the Bank states its simple capital structure is primarily CET1 but this does not supply a Tier 1 amount.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {})], "Not publicly disclosed.")
metric("Total Capital", "£", [("Total capital", {})], "Not publicly disclosed as an absolute amount.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {})], "The accounts disclose total capital requirement (TCR), not a total capital ratio; TCR has not been substituted.")
metric("Total RWAs", "£", [("Total risk-weighted assets", {})], "Not publicly disclosed as an absolute amount.")
metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", {"FY2026": "13.3%", "FY2025": "11.0%", "FY2024": "10.8%", "FY2023": "11.5%", "FY2022": "7.6%"})], "FY2025's own report says 11.0%; FY2026's comparative chart labels FY2025 11.4%. The own-year figure is retained and the cross-report difference is documented.")
metric("LCR", "%", [("Liquidity Coverage Ratio", {"FY2026": "228%", "FY2025": "247%", "FY2024": "408%", "FY2023": "315%", "FY2022": "605%"})], "FY2021's 986% is outside the five-year window. Ratios are the Bank's year-end disclosures.")
metric("NSFR", "%", [("Net Stable Funding Ratio", {})], "Not publicly disclosed in the reviewed annual reports or 31 March 2023 Pillar 3 disclosure.")
metric("MREL Ratio", "%", [("MREL ratio", {})], "The reports describe the Bank as subject to an MREL requirement equal to its TCR/Pillar 1 and Pillar 2 requirements, but disclose no quantitative MREL ratio; no value is inferred.")

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2026": 9866447, "FY2025": -26050380, "FY2024": 18698728, "FY2023": -28182841, "FY2022": -14594539}),
        ("Net cash from/(used in) investing activities", {"FY2026": -16150833, "FY2025": -6687324, "FY2024": 6724219, "FY2023": 1766363, "FY2022": 20376709}),
        ("Net cash from/(used in) financing activities", {"FY2026": 4600000, "FY2025": -100000, "FY2024": -100000, "FY2023": 7000000, "FY2022": 3000000}),
        ("Cash and cash equivalents at end of reporting period", {"FY2026": 85395984, "FY2025": 87080370, "FY2024": 119918074, "FY2023": 94595127, "FY2022": 114011606}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2026": "21.8%", "FY2025": "19.9%", "FY2024": "20.7%", "FY2023": "23.1%", "FY2022": "18.2%"}),
        ("Leverage Ratio", {"FY2026": "13.3%", "FY2025": "11.0%", "FY2024": "10.8%", "FY2023": "11.5%", "FY2022": "7.6%"}),
        ("LCR", {"FY2026": "228%", "FY2025": "247%", "FY2024": "408%", "FY2023": "315%", "FY2022": "605%"}),
    ],
    note="Entity-only cash flows. Regulatory ratios are disclosed on the Bank's regulatory basis. Blank cells mean not disclosed, not zero. The 2023 cash-flow comparative restatement is explained on the cash-flow sheet.",
)
bw.save("/Users/armaan/code/katalysis/banks/RELIANCE BANK FINANCIALS.xlsx")
