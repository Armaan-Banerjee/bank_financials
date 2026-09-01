import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}
CH = "https://find-and-update.company-information.service.gov.uk/company/11734380/filing-history"
AR = {
    "FY2025": CH + "/MzQ5MTMwMDUxNWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": CH + "/MzQ0ODU3NTgzNmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": CH + "/MzQwNjUwNzIyNmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": CH + "/MzM2MTc0NDEyNGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": CH + "/MzMyMzU2MjI3MGFkaXF6a2N4/document?format=pdf&download=0",
}

ENTITY_NOTE = (
    "THIS BANK LIMITED (company 11734380, FRN 832786) is the UK bank formerly named JN Bank UK Ltd. "
    "The legal name changed on 19 January 2026; the FY2021-FY2025 Companies House accounts were filed under "
    "the former JN Bank UK Ltd name. The entity is a UK private bank authorised by the PRA and regulated by the "
    "PRA/FCA. The FY2025 accounts discuss the post-2024 change in ownership; figures in this workbook remain the "
    "UK entity's own annual-account figures, not parent-group figures."
)


def account_sources():
    return (
        "Sources - THIS BANK LIMITED / JN Bank UK Ltd own annual accounts, all figures in £'000 unless stated otherwise:\n"
        "FY2025: Annual report and financial statements for year ended 31 March 2025, Statement of cash flows p.33 and financial KPIs pp.6-7 - " + AR["FY2025"] + "\n"
        "FY2024: Annual report and financial statements for year ended 31 March 2024, Statement of cash flows pp.32-33 and financial KPIs pp.6-7 - " + AR["FY2024"] + "\n"
        "FY2023: Annual report and financial statements for year ended 31 March 2023, Statement of cash flows p.28 and risk/capital disclosures pp.71-72 - " + AR["FY2023"] + "\n"
        "FY2022: Annual report and financial statements for year ended 31 March 2022, Statement of cash flows p.27 and financial KPIs p.8 - " + AR["FY2022"] + "\n"
        "FY2021: Annual report and financial statements for year ended 31 March 2021, Statement of cash flows p.23 and financial KPIs p.7 - " + AR["FY2021"] + "\n"
        + ENTITY_NOTE + " All five Companies House PDFs are scanned/image-only; figures were transcribed using OCR and cross-checked against rendered pages."
    )


def p3_sources():
    return (
        "Sources - regulatory capital and liquidity figures disclosed in the entity's own annual accounts (not a separate public Pillar 3 archive):\n"
        "FY2025: financial KPIs and regulatory-capital table, pp.6-7 - " + AR["FY2025"] + "\n"
        "FY2024: financial KPIs and regulatory-capital table, p.6 - " + AR["FY2024"] + "\n"
        "FY2023: the FY2024 accounts' comparative KPI/capital figures are used where the FY2023 report does not present a numeric KPI table, p.6 - " + AR["FY2024"] + "\n"
        "FY2022: financial KPIs and regulatory-capital table, p.8 - " + AR["FY2022"] + "\n"
        "FY2021: 2021 comparative column in the FY2022 regulatory-capital table, p.8; FY2021 accounts' KPI narrative p.7 - " + AR["FY2022"] + " / " + AR["FY2021"] + "\n"
        + ENTITY_NOTE + " The accounts state that Pillar 3 disclosures were available on request rather than publishing a standalone Pillar 3 document."
    )


bw = BankWorkbook(bank_name="THIS BANK LIMITED", years=YEARS, year_label=YEAR_LABEL, header_color="5C2751")

# The source statements provide complete annual activity totals and opening/
# closing cash balances. The totals are retained exactly as reported; detailed
# OCR line-item transcription is avoided where the scans are ambiguous.
cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": -200221, "FY2024": 199773, "FY2023": 19008, "FY2022": -16676, "FY2021": 16721}),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": 16885, "FY2024": 31630, "FY2023": -28783, "FY2022": 9735, "FY2021": -11912}),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": 26463, "FY2024": 10880, "FY2023": 10880, "FY2022": 4380, "FY2021": -155}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -156873, "FY2024": 242283, "FY2023": 1105, "FY2022": -2561, "FY2021": 4654}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 247547, "FY2024": 5264, "FY2023": 4159, "FY2022": 6720, "FY2021": 2066}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 90674, "FY2024": 247547, "FY2023": 5264, "FY2022": 4159, "FY2021": 6720}),
]
bw.add_cash_flow_sheet(
    title="THIS BANK LIMITED — Statement of Cash Flows",
    subtitle="Own entity basis; £'000; years ended 31 March; activity totals transcribed from the filed annual accounts.",
    rows=cash_rows,
    sources_text=account_sources() + "\nReconciliation: each year's net change equals operating + investing + financing totals; closing cash equals opening cash + net change.",
    first_col_width=68,
    source_height=290,
    unit_suffix=" (£'000)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, p3_sources(), note=note, first_col_width=58, source_height=250)


CET1 = {"FY2025": 25927, "FY2024": 8254, "FY2023": 8101, "FY2022": 8012, "FY2021": 11965}
CET1_RATIO = {"FY2025": "16.44%", "FY2024": "19.20%", "FY2023": "16.28%", "FY2022": "15.90%", "FY2021": "66.50%"}
LCR = {"FY2025": "554%", "FY2024": "4840%", "FY2023": "7758%", "FY2022": "Not publicly disclosed", "FY2021": "Not publicly disclosed"}
DISCLOSURE_NOTE = (
    "The accounts provide entity-level regulatory capital data but do not publish a complete standalone Pillar 3 "
    "template. FY2023 values use the FY2024 report's comparative KPI/capital figures. FY2021 values use the FY2022 "
    "report's 2021 comparative regulatory-capital column. Ratios are as reported; no RWA, leverage, NSFR, or MREL "
    "values are derived from them. Where narrative KPI percentages differ from the regulatory-capital table, the "
    "regulatory-capital table is used: FY2025 narrative CET1 ratio 16.58% versus table 16.44%, and FY2025's "
    "comparative FY2024 presentation differs from the FY2024 own-year table."
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CET1)], DISCLOSURE_NOTE)
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", CET1_RATIO)], DISCLOSURE_NOTE)
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", CET1)], "No AT1 capital is reported; Tier 1 equals CET1 in the reviewed accounts.\n" + DISCLOSURE_NOTE)
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CET1_RATIO)], DISCLOSURE_NOTE)
metric("Total Capital", "£'000", [("Total regulatory capital", CET1)], "No Tier 2 capital is reported; total regulatory capital equals CET1 in the reviewed accounts.\n" + DISCLOSURE_NOTE)
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", CET1_RATIO)], DISCLOSURE_NOTE)
bw.add_not_disclosed_metric_sheets(
    ["Total RWAs", "Leverage Ratio"],
    p3_sources(),
    per_note={name: "No numeric standalone value was identified in the FY2021-FY2025 annual accounts reviewed; no value has been derived." for name in ["Total RWAs", "Leverage Ratio"]},
)
metric("LCR", "%", [("Liquidity coverage ratio", LCR)], "FY2022 and FY2021 accounts disclose HQLA amounts and describe LCR as above minimum, but do not provide a numeric LCR ratio.\n" + DISCLOSURE_NOTE)
bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={name: "No numeric standalone value was identified in the FY2021-FY2025 annual accounts reviewed; no value has been derived." for name in ["NSFR", "MREL Ratio"]},
)

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -200221, "FY2024": 199773, "FY2023": 19008, "FY2022": -16676, "FY2021": 16721}),
        ("Net cash from/(used in) investing activities", {"FY2025": 16885, "FY2024": 31630, "FY2023": -28783, "FY2022": 9735, "FY2021": -11912}),
        ("Net cash from/(used in) financing activities", {"FY2025": 26463, "FY2024": 10880, "FY2023": 10880, "FY2022": 4380, "FY2021": -155}),
        ("Cash and cash equivalents at end of year", {"FY2025": 90674, "FY2024": 247547, "FY2023": 5264, "FY2022": 4159, "FY2021": 6720}),
    ],
    cash_flow_unit="£'000",
    ratios=[("CET1 Ratio", CET1_RATIO), ("Tier 1 Ratio", CET1_RATIO), ("Total Capital Ratio", CET1_RATIO), ("LCR", LCR)],
    note="Full annual accounts build for the entity formerly named JN Bank UK Ltd. See detail sheets for source basis and disclosure gaps.",
)

bw.save("/Users/armaan/code/katalysis/banks/THIS BANK FINANCIALS.xlsx")
