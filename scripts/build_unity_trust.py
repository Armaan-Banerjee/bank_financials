import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-Annual-Report-and-Accounts-2025.pdf"
AR2024_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-Annual-Report-and-Accounts-2024.pdf"
AR2023_URL = "https://assets.unity.co.uk/U798_0324_Unity_Trust_Bank_Annual-Report-and-Accounts_2023.pdf"
AR2021_URL = "https://assets.unity.co.uk/2022/08/Unity-Trust-Bank_Report-and-Accounts-2021.pdf"

P3_2025_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-PILLAR3-2025-1.pdf"
P3_2024_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-PILLAR3-2024.pdf"
P3_2023_URL = "https://assets.unity.co.uk/Unity-Trust-Bank-PILLAR3-2023-1.pdf"
P3_2022_URL = "https://assets.unity.co.uk/2023/03/Unity-Trust-Bank_2022-Pillar-3-Disclosures.pdf"
P3_2021_URL = "https://assets.unity.co.uk/2022/08/PILLAR3-2021-FINAL.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Unity Trust Bank Plc (FRN 204570) is an independent UK bank with no ultimate parent company - "
    "owned by a mix of trade unions, co-operative and charitable bodies, and other institutions, focused on "
    "lending to charities, social enterprises, housing providers, SMEs and public sector bodies. Its own accounts "
    "state it 'does not have an ultimate parent company'. The Bank presents its results on an 'extended entity "
    "basis' combining itself with a small dormant subsidiary, Unity EBT Limited (the trustee of an employee share "
    "scheme, one £1 ordinary share, 100% held) - not a full IFRS 10 consolidation, which the Bank elected not to "
    "apply on materiality grounds (Companies Act 2006 s405(2)); in practice this makes no discernible difference "
    "to the figures. All years reconcile exactly (operating + investing + financing = net change; opening + net "
    "change = closing) with no restatements or presentation-basis changes across the 5 years covered."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Unity Trust Bank Plc's own Statement of Cash Flows, £'000:\n"
    f"FY2025: Report & Accounts 2025, p.51 (Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2024: Report & Accounts 2024, p.39 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Report & Accounts 2023, p.41-42 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Report & Accounts 2023, p.41-42 (Statement of Cash Flows, 2022 comparative column) - {AR2023_URL}\n"
    f"FY2021: Report & Accounts 2021, p.35-36 (Statement of Cash Flows) - {AR2021_URL}\n"
    "Each year's own report was used for its own column (FY2022 taken from the FY2023 report's comparative, since "
    "no standalone FY2022 annual report was separately sourced); every year's own figure was cross-checked against "
    "its appearance as the following year's comparative column and matched exactly in every case - no material "
    "arithmetic errors found, no presentation-basis restatements across the 5 years (FY2025's single 'Finance "
    "costs' line was split into lease/central-bank components that year only, kept on separate rows). FY2022's "
    "operating-activities line items sum to £1k more than the operating total as printed (immaterial rounding, not "
    "corrected).\n\n"
    + ENTITY_NOTE
)


def p3_sources(page="6"):
    return (
        "Sources - Unity Trust Bank Plc Pillar 3 Disclosures, 'Summary of Key Metrics' table:\n"
        f"FY2025: Pillar 3 Disclosures 2025, p.{page} - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures 2024, p.6 - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 2023, p.6 - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures 2022, p.5 - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures 2021, p.4 (Tier 1/Total Capital and NSFR rows sourced instead from the "
        f"following year's comparative column, Pillar 3 Disclosures 2022, p.5, since the 2021 report itself only "
        f"published CET1 and LCR) - {P3_2021_URL} / {P3_2022_URL}"
    )


bw = BankWorkbook(bank_name="Unity Trust Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="7A0C2E")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": 52415, "FY2024": 65751, "FY2023": 63862, "FY2022": 27352, "FY2021": 11053}),
    ("DATA", "Finance costs on lease liabilities", {"FY2025": 58}),
    ("DATA", "Finance costs on central bank facilities", {"FY2025": 145}),
    ("DATA", "Finance costs (combined, as reported)", {"FY2024": 73, "FY2023": 85, "FY2022": 249, "FY2021": 240}),
    ("DATA", "Impairment losses, net of reversals, on financial assets", {"FY2025": 1206, "FY2024": 1017, "FY2023": 3548, "FY2022": 2477, "FY2021": 470}),
    ("DATA", "Non-cash movements in relation to investment securities", {"FY2025": -24580, "FY2024": -10770, "FY2023": -8428, "FY2022": -3871}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": 368, "FY2024": 280, "FY2023": 283, "FY2022": 270, "FY2021": 305}),
    ("DATA", "Depreciation of right-of-use assets", {"FY2025": 262, "FY2024": 266, "FY2023": 250, "FY2022": 269, "FY2021": 276}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 15, "FY2024": 6, "FY2023": 16, "FY2022": 38, "FY2021": 50}),
    ("DATA", "Loss on disposal of property, plant and equipment", {"FY2024": 0, "FY2023": 3, "FY2021": 12}),
    ("DATA", "Increase/(decrease) in provisions", {"FY2025": 1642, "FY2024": 1441, "FY2023": 567, "FY2022": 320, "FY2021": 88}),
    ("DATA", "Fair value loss on derivatives", {"FY2025": 1106, "FY2024": 153}),
    ("DATA", "Share-based payment expense", {"FY2025": 853, "FY2024": 174}),
    ("DATA", "Pension administration expense", {"FY2025": 289, "FY2024": 172}),
    ("DATA", "Other non-cash movements", {"FY2021": 244}),
    ("DATA", "(Increase)/decrease in prepayments and accrued income", {"FY2025": -955, "FY2024": 87, "FY2023": -386, "FY2022": -59, "FY2021": -424}),
    ("DATA", "(Increase)/decrease in other operating assets", {"FY2025": -759, "FY2024": 69, "FY2023": 155, "FY2022": -151, "FY2021": 28}),
    ("DATA", "(Increase) in derivatives", {"FY2025": -770}),
    ("DATA", "Increase in loans and advances to customers", {"FY2025": -120381, "FY2024": -1187, "FY2023": -180618, "FY2022": -115530, "FY2021": -122183}),
    ("DATA", "(Increase)/decrease in Bank of England mandatory reserve", {"FY2024": 3448, "FY2023": 310, "FY2022": -355, "FY2021": -1294}),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {"FY2025": 1007, "FY2024": 984, "FY2023": 337, "FY2022": 382, "FY2021": 28}),
    ("DATA", "Increase in customer deposits", {"FY2025": 144076, "FY2024": 157895, "FY2023": 20652, "FY2022": 31430, "FY2021": 171502}),
    ("DATA", "Increase/(decrease) in other operating liabilities", {"FY2025": -251, "FY2024": -361, "FY2023": 527, "FY2022": -101, "FY2021": 655}),
    ("DATA", "Income tax paid", {"FY2025": -25649, "FY2024": -14668, "FY2023": -8698, "FY2022": -3180, "FY2021": -1328}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 30097, "FY2024": 204830, "FY2023": -107535, "FY2022": -60460, "FY2021": 59722}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -852, "FY2024": -565, "FY2023": -218, "FY2022": -163, "FY2021": -390}),
    ("DATA", "Intangible asset additions", {"FY2025": -461, "FY2021": 0}),
    ("DATA", "Interest received from investment securities", {"FY2025": 23945}),
    ("DATA", "Purchase of investment securities", {"FY2025": -576821, "FY2024": -159028, "FY2023": -96260, "FY2022": -261001, "FY2021": -30302}),
    ("DATA", "Proceeds from sale and redemption of investment securities", {"FY2025": 73615, "FY2024": 106314, "FY2023": 116948, "FY2022": 209523, "FY2021": 73666}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2025": -480574, "FY2024": -53279, "FY2023": 20470, "FY2022": -51641, "FY2021": 42974}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid", {"FY2025": -2979, "FY2024": -1734, "FY2023": -1361, "FY2022": -949, "FY2021": -741}),
    ("DATA", "Repayment of lease liabilities", {"FY2025": -474, "FY2024": -285, "FY2023": -468, "FY2022": -380, "FY2021": -186}),
    ("DATA", "Proceeds on issue of share capital, net of transaction costs", {"FY2025": 86, "FY2024": 91, "FY2023": 0, "FY2022": 50, "FY2021": 8520}),
    ("DATA", "Drawdown on central bank facilities", {"FY2025": 50000}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {"FY2025": 46633, "FY2024": -1928, "FY2023": -1829, "FY2022": -1279, "FY2021": 7593}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -403844, "FY2024": 149623, "FY2023": -88894, "FY2022": -113380, "FY2021": 110289}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 624587, "FY2024": 474964, "FY2023": 563858, "FY2022": 677238, "FY2021": 566949}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 220743, "FY2024": 624587, "FY2023": 474964, "FY2022": 563858, "FY2021": 677238}),
]

bw.add_cash_flow_sheet(
    title="Unity Trust Bank Plc — Statement of Cash Flows",
    subtitle="Extended entity basis (Bank + Unity EBT Limited), £'000",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=48, source_height=130)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 259127, "FY2024": 222740, "FY2023": 172898, "FY2022": 122931, "FY2021": 104260})],
    p3_sources(),
    note="The Bank has no Additional Tier 1 or Tier 2 capital instruments in any year shown - CET1 capital, Tier 1 "
         "capital and Total capital are identical figures throughout.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.7%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 259127, "FY2024": 222740, "FY2023": 172898, "FY2022": 122931, "FY2021": 104260})],
    p3_sources(),
    note="Equal to CET1 capital in every year - the Bank has no Additional Tier 1 capital instruments.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.69%"})],
    p3_sources(),
    note="FY2021's own Pillar 3 report only stated a CET1 ratio (no separate Tier 1 figure); the FY2021 Tier 1 "
         "ratio shown here (17.69%) is taken from the FY2022 Pillar 3 report's own FY2021 comparative column, "
         "which confirms Tier 1 capital equalled CET1 capital that year too.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 259127, "FY2024": 222740, "FY2023": 172898, "FY2022": 122931, "FY2021": 104260})],
    p3_sources(),
    note="Equal to CET1 capital in every year - the Bank has no Tier 2 capital instruments.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.69%"})],
    p3_sources(),
    note="FY2021's own Pillar 3 report only stated a CET1 ratio; the FY2021 figure shown here is taken from the "
         "FY2022 Pillar 3 report's own FY2021 comparative column (see Tier 1 Ratio sheet note).",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets (RWA)", {"FY2025": 1065248, "FY2024": 925984, "FY2023": 878472, "FY2022": 672893, "FY2021": 589551})],
    p3_sources(),
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total UK leverage ratio exposure measure", {"FY2025": 2045234, "FY2024": 1394612}),
        ("UK leverage ratio, excl. temporary central bank reserves exemption (%)", {"FY2025": "12.67%", "FY2024": "15.97%"}),
        ("Total Basel III leverage ratio exposure measure", {"FY2025": 2263918, "FY2024": 2016510, "FY2023": 1797760, "FY2022": 1710211, "FY2021": 1673611}),
        ("Basel III leverage ratio, incl. temporary central bank reserves exemption (%)", {"FY2025": "11.45%", "FY2024": "11.05%", "FY2023": "9.62%", "FY2022": "7.19%", "FY2021": "5.7%"}),
    ],
    p3_sources(),
    note="Unity introduced a separate 'UK leverage ratio' (excluding the temporary central bank reserves "
         "exemption) alongside its existing 'Basel III leverage ratio' (including that exemption) from the FY2024 "
         "Pillar 3 report onward - FY2021-FY2023 only ever disclosed the Basel III basis. FY2021's Basel III "
         "leverage ratio is shown here as originally reported that year (5.7%); the FY2022 Pillar 3 report's own "
         "FY2021 comparative column restates this to 6.23% (including)/6.22% (excluding the exemption) - a basis "
         "change, not a data error, so the original 5.7% figure is kept as the primary FY2021 value.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA)", {"FY2025": 915263, "FY2024": 913969, "FY2023": 697018, "FY2022": 782783, "FY2021": 822783}),
        ("Total net cash outflow", {"FY2025": 405412, "FY2024": 400945, "FY2023": 332338, "FY2022": 355595, "FY2021": 303007}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "225.76%", "FY2024": "227.95%", "FY2023": "210%", "FY2022": "220%", "FY2021": "272%"}),
    ],
    p3_sources(),
    note="LCR figures are as at year-end (31 December), not a trailing average - per the Pillar 3 report's own "
         "footnote, this does not agree to the average LCR balances disclosed elsewhere in the same report.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 1420532, "FY2024": 1303839, "FY2023": 1200480, "FY2022": 1144865, "FY2021": 1077138}),
        ("Total required stable funding", {"FY2025": 955318, "FY2024": 845763, "FY2023": 909694, "FY2022": 741481, "FY2021": 628367}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "148.70%", "FY2024": "154.16%", "FY2023": "131.97%", "FY2022": "154.4%", "FY2021": "171.4%"}),
    ],
    p3_sources(),
    note="FY2021's own Pillar 3 report did not disclose NSFR at all; the FY2021 figures shown here are taken from "
         "the FY2022 Pillar 3 report's own FY2021 comparative column instead.",
)

metric(
    "MREL Ratio", None,
    [("MREL requirement (= Total Capital Requirement, %)", {"FY2025": "10.69%", "FY2024": "10.69%", "FY2023": "10.69%", "FY2022": "10.10%", "FY2021": "10.14%"})],
    p3_sources(),
    note="Unity is in the lowest resolution risk category, where its MREL requirement is set to equal its Total "
         "Capital Requirement (TCR) - no separate numeric MREL resources figure or MREL ratio distinct from TCR is "
         "published in any year.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 30097, "FY2024": 204830, "FY2023": -107535, "FY2022": -60460, "FY2021": 59722}),
        ("Net cash from/(used in) investing activities", {"FY2025": -480574, "FY2024": -53279, "FY2023": 20470, "FY2022": -51641, "FY2021": 42974}),
        ("Net cash from/(used in) financing activities", {"FY2025": 46633, "FY2024": -1928, "FY2023": -1829, "FY2022": -1279, "FY2021": 7593}),
        ("Cash and cash equivalents at end of year", {"FY2025": 220743, "FY2024": 624587, "FY2023": 474964, "FY2022": 563858, "FY2021": 677238}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.7%"}),
        ("Tier 1 Ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.69%"}),
        ("Total Capital Ratio", {"FY2025": "24.33%", "FY2024": "24.05%", "FY2023": "19.68%", "FY2022": "18.27%", "FY2021": "17.69%"}),
        ("Leverage Ratio (Basel III)", {"FY2025": "11.45%", "FY2024": "11.05%", "FY2023": "9.62%", "FY2022": "7.19%", "FY2021": "5.7%"}),
        ("LCR", {"FY2025": "225.76%", "FY2024": "227.95%", "FY2023": "210%", "FY2022": "220%", "FY2021": "272%"}),
        ("NSFR", {"FY2025": "148.70%", "FY2024": "154.16%", "FY2023": "131.97%", "FY2022": "154.4%", "FY2021": "171.4%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Leverage Ratio shown on the Basel III basis (available for "
         "all 5 years) rather than the UK basis (only introduced from FY2024) - see Leverage Ratio sheet for both.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/UNITY TRUST FINANCIALS.xlsx")
