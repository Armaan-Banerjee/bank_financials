import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# PILLAR-3-ONLY WORKBOOK
# United Trust Bank Limited (company 00549690, FRN 204463) is the regulated
# operating bank within UTB Partners Plc.  The available Pillar 3 disclosures
# are prepared on the consolidated UTB Partners group basis, not as a solo UTB
# series.  The statutory accounts omit a cash-flow statement; consequently the
# workbook records the limitation and presents the available regulatory data.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

P3 = {
    "FY2025": "https://www.utbank.co.uk/wp-content/uploads/2026/03/UTB-Partners-Pillar-3-Disclosure-2025.pdf",
    "FY2024": "https://www.utbank.co.uk/wp-content/uploads/2025/03/UTB-Partners-Pillar-3-Disclosure-2024.pdf",
    "FY2023": "https://www.utbank.co.uk/wp-content/uploads/2024/03/UTB-Partners-Pillar-3-Disclosure-2023.pdf",
    "FY2022": "https://www.utbank.co.uk/wp-content/uploads/2023/03/UTB-Partners-Pillar-3-Disclosure-2022-.pdf",
    "FY2021": "https://rebrand-dev.utbank.co.uk/wp-content/uploads/2022/03/UTB-Partners-Pillar-3-Disclosure-2021-FINAL1-.pdf",
}
ACCOUNTS_2024 = "https://www.utbank.co.uk/wp-content/uploads/2025/03/UTB-Report-and-Accounts-2024.pdf"
CH = "https://find-and-update.company-information.service.gov.uk/company/00549690/filing-history"

ENTITY_NOTE = (
    "ENTITY AND BASIS: United Trust Bank Limited (company 00549690, FCA/PRA FRN 204463) is the regulated,"
    " material operating bank and wholly-owned subsidiary of UTB Partners Plc. The Pillar 3 reports used here"
    " constitute consolidated disclosures of UTB Partners Plc; UTB Partners is a financial holding company and"
    " the group is supervised on a consolidated basis. SOS Intelligence is immaterial and excluded from regulatory"
    " consolidation. Accordingly, all figures in this workbook are explicitly labelled CONSOLIDATED UTB PARTNERS"
    " BASIS and must not be read as standalone United Trust Bank Limited figures."
)

EXEMPTION_NOTE = (
    "CASH-FLOW LIMITATION: United Trust Bank Limited's published 2024 Report and Accounts contains the"
    " Income Statement, Statement of Comprehensive Income, Statement of Financial Position and Statement of"
    " Changes in Equity, but no Statement of Cash Flows; the Companies House filing history likewise describes"
    " the accounts as full accounts. The available accounts and source material do not provide a cash-flow"
    " statement suitable for this workbook. The Cash Flow Statement sheet therefore records this limitation"
    " rather than inferring or fabricating cash-flow values."
)


def sources():
    return (
        "Sources - consolidated UTB Partners Plc basis, £'000 unless stated:\n"
        "FY2025: UTB Partners Pillar 3 Disclosure 2025, Table KM1, pp.6-7 - " + P3["FY2025"] + "\n"
        "FY2024: UTB Partners Pillar 3 Disclosure 2024, Table KM1, pp.6-7 - " + P3["FY2024"] + "\n"
        "FY2023: UTB Partners Pillar 3 Disclosure 2023, Appendix 1 Table KM1, pp.44-45 - " + P3["FY2023"] + "\n"
        "FY2022: UTB Partners Pillar 3 Disclosure 2022, Appendix 1 Table KM1, p.43 - " + P3["FY2022"] + "\n"
        "FY2021: UTB Partners Pillar 3 Disclosure 2022 comparative column and 2021 disclosure, Appendix 1 /"
        " own-funds and leverage templates - " + P3["FY2021"] + "\n"
        "Accounts cross-check: United Trust Bank Report and Accounts 2024, pp.47-50 - " + ACCOUNTS_2024 + "\n"
        "Companies House entity and filing history (company 00549690) - " + CH + "\n\n" + ENTITY_NOTE
    )


CH_ACCOUNTS = {
    "FY2025": CH + "/MzUyMTk0MjExM2FkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": CH + "/MzQ2MzA3OTAyMGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": CH + "/MzQzMTMzNTk5OGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": CH + "/MzM3NzEyOTIyNWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": CH + "/MzMzMjI5NTg0MGFkaXF6a2N4/document?format=pdf&download=0",
}

STATEMENTS_NOTE = (
    "ENTITY AND BASIS - STATEMENTS ONLY: unlike the Pillar 3 sheets in this workbook (consolidated UTB"
    " Partners Plc basis), the Balance Sheet, Profit & Loss, Statement of Changes in Equity and Asset"
    " Quality sheets are sourced from United Trust Bank Limited's own entity-level statutory accounts"
    " (Companies House, company 00549690), which report full Income Statement, Statement of Comprehensive"
    " Income, Statement of Financial Position and Statement of Changes in Equity for all 5 years - only the"
    " Statement of Cash Flows is genuinely absent from the entity accounts (see the Cash Flow Statement"
    " sheet's note). All 5 filings are scanned/image-only; figures were transcribed directly from the"
    " rendered filing pages."
)


def statements_sources():
    return (
        "Sources - United Trust Bank Limited entity-level statutory accounts (Companies House filing"
        " history, company 00549690), £'000:\n"
        "FY2025: Report and Accounts 2025, Income Statement/Statement of Comprehensive Income p.45,"
        " Statement of Financial Position p.46, Statement of Changes in Equity p.47 - " + CH_ACCOUNTS["FY2025"] + "\n"
        "FY2024: comparative column in the Report and Accounts 2025 (own FY2024 filing not separately"
        " re-transcribed; figures are identical audited comparatives) - " + CH_ACCOUNTS["FY2024"] + "\n"
        "FY2023: Report and Accounts 2023, Income Statement/Statement of Comprehensive Income p.49,"
        " Statement of Financial Position p.50, Statement of Changes in Equity p.51 - " + CH_ACCOUNTS["FY2023"] + "\n"
        "FY2022: Report and Accounts 2022, Income Statement/Statement of Comprehensive Income p.57,"
        " Statement of Financial Position p.58, Statement of Changes in Equity p.59 - " + CH_ACCOUNTS["FY2022"] + "\n"
        "FY2021: comparative column in the Report and Accounts 2022 (own FY2021 filing not separately"
        " re-transcribed; figures are identical audited comparatives) - " + CH_ACCOUNTS["FY2021"] + "\n\n"
        + STATEMENTS_NOTE
    )


def asset_quality_sources():
    return (
        "Sources - United Trust Bank Limited entity-level statutory accounts (Companies House filing"
        " history, company 00549690), Note 8 (Loans and advances to customers) and Note 9 (Provision for"
        " impairment losses on loans and advances to customers), £'000:\n"
        "FY2025/FY2024: Report and Accounts 2025, pp.54-55 - " + CH_ACCOUNTS["FY2025"] + "\n"
        "FY2023/FY2022: Report and Accounts 2023, pp.57-58 - " + CH_ACCOUNTS["FY2023"] + "\n"
        "FY2021: comparative column in the Report and Accounts 2022, pp.65-66 - " + CH_ACCOUNTS["FY2022"] + "\n\n"
        "CLASSIFICATION: United Trust Bank Limited reports under FRS 102 (UK GAAP), not IFRS 9; there is no"
        " Stage 1/2/3 staged-ECL split in the source. Asset Quality is instead built from the entity's own"
        " loan-product portfolios (Property / Mortgages / Asset Finance / Finance lease and hire purchase)"
        " and its Individual/Collective impairment-provision classification. Note 9's own portfolio-level"
        " breakdown labels the finance-lease-and-hire-purchase book 'Asset Finance portfolio', distinct from"
        " Note 8's separately-disclosed (near-nil-impairment) 'Asset Finance portfolio loan receivables'"
        " direct-lending book; both are reproduced as their own rows below, matching the source, rather than"
        " merged. In FY2025 and FY2024 only, the Mortgages portfolio's own net figure also includes a fair"
        " value hedge adjustment (+£1,763k in FY2025, -£3,363k in FY2024) that is not part of the impairment"
        " provision; this is why gross-less-impairment does not exactly equal the net total in those two"
        " years (no such adjustment existed in FY2023-FY2021).\n\n" + STATEMENTS_NOTE
    )


RWA_NOTE = (
    "RWA BREAKDOWN - CONSOLIDATED UTB PARTNERS BASIS, Table UK OV1 (Overview of risk-weighted exposure"
    " amounts): each year uses that year's own disclosure document's own-year column, consistent with"
    " project convention. The FY2021 disclosure predates the OV1 template (it only publishes an 8%-capital"
    " exposure-class table); FY2021's OV1-format category split is instead taken from the FY2022 Pillar 3"
    " disclosure's own 2021 comparative column, the earliest year an OV1 table is available. Each year's OV1"
    " Total differs immaterially (<0.02%) from the Total RWAs metric sheet's KM1-sourced figure - both are"
    " the bank's own published numbers; the gap is a KM1-vs-OV1 rounding difference of the same kind already"
    " documented on the Total RWAs sheet, not a data error."
)


def rwa_sources():
    return (
        "Sources - consolidated UTB Partners Plc basis, Table UK OV1, £'000:\n"
        "FY2025: UTB Partners Pillar 3 Disclosure 2025, Table UK OV1, p.11 - " + P3["FY2025"] + "\n"
        "FY2024: UTB Partners Pillar 3 Disclosure 2024, Table UK OV1, p.11 - " + P3["FY2024"] + "\n"
        "FY2023: UTB Partners Pillar 3 Disclosure 2023, Table UK OV1, pp.31-32 - " + P3["FY2023"] + "\n"
        "FY2022: UTB Partners Pillar 3 Disclosure 2022, Table UK OV1, p.32 - " + P3["FY2022"] + "\n"
        "FY2021: UTB Partners Pillar 3 Disclosure 2022, Table UK OV1, 2021 (T-1) comparative column,"
        " p.32 - " + P3["FY2022"] + "\n\n" + RWA_NOTE
    )


bw = BankWorkbook(
    bank_name="United Trust Bank Limited (consolidated UTB Partners basis)",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="1B4965",
)

bw.add_balance_sheet_sheet(
    title="United Trust Bank Limited — Balance Sheet",
    subtitle="Entity (Company-only) basis, £'000. Statement of Financial Position.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Loans and advances to banks/central banks", {
            "FY2025": 369339 + 63472, "FY2024": 204053 + 77909, "FY2023": 241996 + 52696,
            "FY2022": 243506 + 25356, "FY2021": 181074 + 23577,
        }),
        ("DATA", "Loans and advances to customers", {
            "FY2025": 3895213, "FY2024": 3487345, "FY2023": 3104356,
            "FY2022": 2426021, "FY2021": 1808607,
        }),
        ("DATA", "Loans to group companies", {
            "FY2025": 700, "FY2024": 499, "FY2023": 369, "FY2022": 205, "FY2021": 120,
        }),
        ("DATA", "Debt securities", {
            "FY2025": 100346, "FY2024": 118562, "FY2023": 19510, "FY2022": 84783, "FY2021": 221816,
        }),
        ("DATA", "Derivative financial instruments (assets)", {
            "FY2025": 1207, "FY2024": 3600, "FY2023": 2039, "FY2022": 3561,
        }),
        ("DATA", "Equity shares", {
            "FY2025": 1300, "FY2024": 1300, "FY2023": 1000, "FY2022": 1000,
        }),
        ("DATA", "Tangible fixed assets", {
            "FY2025": 757, "FY2024": 697, "FY2023": 1003, "FY2022": 812, "FY2021": 552,
        }),
        ("DATA", "Intangible assets", {
            "FY2025": 7885, "FY2024": 6790, "FY2023": 5288, "FY2022": 4092, "FY2021": 3280,
        }),
        ("DATA", "Other assets", {
            "FY2025": 10418, "FY2024": 12505, "FY2023": 11911, "FY2022": 8981, "FY2021": 15152,
        }),
        ("TOTAL", "Total assets", {
            "FY2025": 4450637, "FY2024": 3913260, "FY2023": 3440168,
            "FY2022": 2798317, "FY2021": 2254178,
        }),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits from customers", {
            "FY2025": 3847845, "FY2024": 3407271, "FY2023": 2797361,
            "FY2022": 2208300, "FY2021": 1715596,
        }),
        ("DATA", "Loans from banks/central banks", {
            "FY2025": 80462, "FY2024": 60648, "FY2023": 263441, "FY2022": 302135, "FY2021": 300079,
        }),
        ("DATA", "Loans from group companies", {
            "FY2025": 1678, "FY2024": 3048, "FY2023": 1522, "FY2022": 1879, "FY2021": 1259,
        }),
        ("DATA", "Derivative financial instruments (liabilities)", {
            "FY2025": 2388, "FY2024": 279, "FY2023": 1329, "FY2022": 96,
        }),
        ("DATA", "Other liabilities", {
            "FY2025": 18224, "FY2024": 22549, "FY2023": 20076, "FY2022": 17474, "FY2021": 12356,
        }),
        ("DATA", "Long-term subordinated debt", {
            "FY2025": 27204, "FY2024": 56603, "FY2023": 56640, "FY2022": 29324, "FY2021": 29256,
        }),
        ("TOTAL", "Total liabilities", {
            "FY2025": 3977801, "FY2024": 3550398, "FY2023": 3140369,
            "FY2022": 2559208, "FY2021": 2058546,
        }),
        ("SECTION", "Capital and Reserves", {}),
        ("DATA", "Share capital", {
            "FY2025": 10500, "FY2024": 10350, "FY2023": 10350, "FY2022": 10350, "FY2021": 10350,
        }),
        ("DATA", "Share premium", {
            "FY2025": 33030, "FY2024": 25680, "FY2023": 25680, "FY2022": 25680, "FY2021": 25680,
        }),
        ("DATA", "Contingent convertible securities", {
            "FY2025": 65913, "FY2024": 16851, "FY2023": 16851, "FY2022": 16851, "FY2021": 16851,
        }),
        ("DATA", "Retained earnings", {
            "FY2025": 363393, "FY2024": 309981, "FY2023": 246918, "FY2022": 186228, "FY2021": 142751,
        }),
        ("TOTAL", "Total capital and reserves", {
            "FY2025": 472836, "FY2024": 362862, "FY2023": 299799,
            "FY2022": 239109, "FY2021": 195632,
        }),
        ("TOTAL", "Total equity and liabilities", {
            "FY2025": 4450637, "FY2024": 3913260, "FY2023": 3440168,
            "FY2022": 2798317, "FY2021": 2254178,
        }),
    ],
    sources_text=statements_sources(),
    first_col_width=58,
    source_height=210,
)

bw.add_income_statement_sheet(
    title="United Trust Bank Limited — Profit & Loss",
    subtitle="Entity (Company-only) basis, £'000. Income Statement and Statement of Comprehensive Income.",
    rows=[
        ("DATA", "Interest receivable and similar income", {
            "FY2025": 342801, "FY2024": 320696, "FY2023": 259393, "FY2022": 153034, "FY2021": 119015,
        }),
        ("DATA", "Interest payable and similar charges", {
            "FY2025": -166396, "FY2024": -155666, "FY2023": -105094, "FY2022": -38374, "FY2021": -23857,
        }),
        ("TOTAL", "Net interest income", {
            "FY2025": 176405, "FY2024": 165030, "FY2023": 154299, "FY2022": 114660, "FY2021": 95158,
        }),
        ("DATA", "Other income/(charges)", {
            "FY2025": 26, "FY2024": -59, "FY2023": -153, "FY2022": -18, "FY2021": -18,
        }),
        ("TOTAL", "Operating income", {
            "FY2025": 176431, "FY2024": 164971, "FY2023": 154146, "FY2022": 114642, "FY2021": 95140,
        }),
        ("DATA", "Administrative expenses", {
            "FY2025": -82353, "FY2024": -75360, "FY2023": -65369, "FY2022": -51245, "FY2021": -43483,
        }),
        ("DATA", "Depreciation and amortisation", {
            "FY2025": -1763, "FY2024": -1578, "FY2023": -1256, "FY2022": -1452, "FY2021": -765,
        }),
        ("DATA", "Provision for impairment losses", {
            "FY2025": -13629, "FY2024": -1664, "FY2023": -4782, "FY2022": -1789, "FY2021": -6455,
        }),
        ("TOTAL", "Profit on ordinary activities before tax", {
            "FY2025": 78686, "FY2024": 86369, "FY2023": 82739, "FY2022": 60156, "FY2021": 44437,
        }),
        ("DATA", "Tax charge for the year", {
            "FY2025": -18006, "FY2024": -20597, "FY2023": -19465, "FY2022": -14761, "FY2021": -9015,
        }),
        ("TOTAL", "Profit after tax retained for the financial year", {
            "FY2025": 60680, "FY2024": 65772, "FY2023": 63274, "FY2022": 45395, "FY2021": 35422,
        }),
        ("SECTION", "Statement of Comprehensive Income", {}),
        ("DATA", "Other comprehensive income", {
            "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0,
        }),
        ("TOTAL", "Total comprehensive income", {
            "FY2025": 60680, "FY2024": 65772, "FY2023": 63274, "FY2022": 45395, "FY2021": 35422,
        }),
    ],
    sources_text=(
        statements_sources() + "\n\n"
        "The FY2022 report's own tax-reconciliation note (Note 6) shows FY2021 profit before tax as"
        " £44,368k, £69k below the Income Statement's own FY2021 figure of £44,437k used here; both are"
        " genuine figures from the same source document and the gap is not resolved further. No OCI items"
        " (revaluation reserves, FX translation, cash-flow hedge reserves, etc.) are reported in any of the"
        " 5 years - profit for the year equals total comprehensive income throughout."
    ),
    first_col_width=58,
    source_height=240,
)

bw.add_equity_changes_sheet(
    title="United Trust Bank Limited — Statement of Changes in Equity",
    subtitle="Entity (Company-only) basis, £'000. Chronological roll-forward, 1 January 2021 to 31 December 2025.",
    headers=["Share capital", "Share premium", "Contingent convertible securities", "Retained earnings", "Total"],
    rows=[
        ("TOTAL", "At 1 January 2021", (10350, 25680, 16851, 121155, 174036)),
        ("DATA", "Profit for the financial year", (None, None, None, 35422, 35422)),
        ("DATA", "Coupon paid on contingent convertible securities", (None, None, None, -1826, -1826)),
        ("DATA", "Dividend paid", (None, None, None, -12000, -12000)),
        ("TOTAL", "At 31 December 2021", (10350, 25680, 16851, 142751, 195632)),
        ("DATA", "Profit for the financial year", (None, None, None, 45395, 45395)),
        ("DATA", "Coupon paid on contingent convertible securities", (None, None, None, -1918, -1918)),
        ("DATA", "Share based payments charge", (None, None, None, 619, 619)),
        ("DATA", "Share based payments recharged to parent", (None, None, None, -619, -619)),
        ("DATA", "Dividend paid", (None, None, None, 0, 0)),
        ("TOTAL", "At 31 December 2022", (10350, 25680, 16851, 186228, 239109)),
        ("DATA", "Profit for the financial year", (None, None, None, 63274, 63274)),
        ("DATA", "Coupon payable on contingent convertible securities", (None, None, None, -2584, -2584)),
        ("DATA", "Share based payments charge", (None, None, None, 744, 744)),
        ("DATA", "Share based payments recharged to parent", (None, None, None, -744, -744)),
        ("TOTAL", "At 31 December 2023", (10350, 25680, 16851, 246918, 299799)),
        ("DATA", "Profit for the financial year", (None, None, None, 65772, 65772)),
        ("DATA", "Coupon payable on contingent convertible securities", (None, None, None, -2709, -2709)),
        ("DATA", "Share based payments charge", (None, None, None, 1526, 1526)),
        ("DATA", "Share based payments recharged from parent", (None, None, None, -1526, -1526)),
        ("TOTAL", "At 31 December 2024", (10350, 25680, 16851, 309981, 362862)),
        ("DATA", "Profit for the financial year", (None, None, None, 60680, 60680)),
        ("DATA", "Shares issued (net of issue costs)", (150, 7350, None, None, 7500)),
        ("DATA", "Contingent convertible securities issued (net of issue costs)", (None, None, 49062, None, 49062)),
        ("DATA", "Coupon payable on contingent convertible securities", (None, None, None, -7268, -7268)),
        ("DATA", "Share based payments charge", (None, None, None, 1805, 1805)),
        ("DATA", "Share based payments recharged from parent", (None, None, None, -1805, -1805)),
        ("TOTAL", "At 31 December 2025", (10500, 33030, 65913, 363393, 472836)),
    ],
    sources_text=statements_sources(),
    first_col_width=54,
    source_height=210,
)

bw.add_cash_flow_sheet(
    title="United Trust Bank Limited — Cash Flow Statement",
    subtitle="Not available in the published statutory accounts; this is a Pillar-3-only workbook.",
    rows=[
        ("SECTION", "No Statement of Cash Flows available for the covered entity", {}),
        ("DATA", "See the source note below. No cash-flow values are inferred.", {}),
    ],
    sources_text=ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE + "\n\n" + sources(),
    first_col_width=90,
    source_height=270,
    unit_suffix="",
)

bw.add_asset_quality_sheet(
    title="United Trust Bank Limited — Asset Quality",
    subtitle="Entity (Company-only) basis, £'000. FRS 102 classification (no IFRS 9 stage split disclosed) - see source note.",
    rows=[
        ("SECTION", "Gross loans and advances to customers, by portfolio", {}),
        ("DATA", "Property portfolio", {
            "FY2025": 1967527, "FY2024": 1812420, "FY2023": 1656511, "FY2022": 1314165, "FY2021": 1030804,
        }),
        ("DATA", "Mortgages portfolio", {
            "FY2025": 1369028, "FY2024": 1223848, "FY2023": 1065867, "FY2022": 792848, "FY2021": 577629,
        }),
        ("DATA", "Asset Finance portfolio loan receivables", {
            "FY2025": 30646, "FY2024": 12639, "FY2023": 7479, "FY2022": 3568, "FY2021": 0,
        }),
        ("DATA", "Finance lease and hire purchase receivables (net investment)", {
            "FY2025": 545508, "FY2024": 450120, "FY2023": 382623, "FY2022": 320348, "FY2021": 209457,
        }),
        ("TOTAL", "Gross loans and advances to customers", {
            "FY2025": 3912709, "FY2024": 3499027, "FY2023": 3112480,
            "FY2022": 2430929, "FY2021": 1817890,
        }),
        ("SECTION", "Less: provision for impairment losses, by portfolio", {}),
        ("DATA", "Property portfolio", {
            "FY2025": -16163, "FY2024": -4449, "FY2023": -4320, "FY2022": -2972, "FY2021": -5531,
        }),
        ("DATA", "Mortgages portfolio", {
            "FY2025": -1651, "FY2024": -2184, "FY2023": -2209, "FY2022": -985, "FY2021": -1135,
        }),
        ("DATA", "Asset Finance portfolio loan receivables", {
            "FY2025": -125, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0,
        }),
        ("DATA", "Finance lease and hire purchase receivables", {
            "FY2025": -1320, "FY2024": -1686, "FY2023": -1595, "FY2022": -951, "FY2021": -2617,
        }),
        ("TOTAL", "Total provision for impairment losses", {
            "FY2025": -19259, "FY2024": -8319, "FY2023": -8124, "FY2022": -4908, "FY2021": -9283,
        }),
        ("SECTION", "Net loans and advances to customers, by portfolio", {}),
        ("DATA", "Property portfolio", {
            "FY2025": 1951364, "FY2024": 1807971, "FY2023": 1652191, "FY2022": 1311193, "FY2021": 1025273,
        }),
        ("DATA", "Mortgages portfolio (incl. fair value hedge adjustment)", {
            "FY2025": 1369140, "FY2024": 1218301, "FY2023": 1063658, "FY2022": 791863, "FY2021": 576494,
        }),
        ("DATA", "Asset Finance portfolio loan receivables", {
            "FY2025": 30521, "FY2024": 12639, "FY2023": 7479, "FY2022": 3568, "FY2021": 0,
        }),
        ("DATA", "Finance lease and hire purchase receivables", {
            "FY2025": 544188, "FY2024": 448434, "FY2023": 381028, "FY2022": 319397, "FY2021": 206840,
        }),
        ("TOTAL", "Net loans and advances to customers", {
            "FY2025": 3895213, "FY2024": 3487345, "FY2023": 3104356,
            "FY2022": 2426021, "FY2021": 1808607,
        }),
        ("SECTION", "Impairment provision by FRS 102 classification (balance at 31 December)", {}),
        ("DATA", "Individual impairment provision", {
            "FY2025": 16053, "FY2024": 5248, "FY2023": 5350, "FY2022": 2618, "FY2021": 7471,
        }),
        ("DATA", "Collective impairment provision", {
            "FY2025": 3206, "FY2024": 3071, "FY2023": 2774, "FY2022": 2290, "FY2021": 1812,
        }),
        ("TOTAL", "Total impairment provision", {
            "FY2025": 19259, "FY2024": 8319, "FY2023": 8124, "FY2022": 4908, "FY2021": 9283,
        }),
    ],
    sources_text=asset_quality_sources(),
    first_col_width=64,
    source_height=260,
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(
        name, unit, rows_data, sources(), note=note, first_col_width=54, source_height=235
    )


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {
    "FY2025": 390450, "FY2024": 330662, "FY2023": 268495,
    "FY2022": 209850, "FY2021": 170785,
})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {
    "FY2025": "14.01%", "FY2024": "13.04%", "FY2023": "11.79%",
    "FY2022": "12.07%", "FY2021": "12.74%",
})])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {
    "FY2025": 453206, "FY2024": 344803, "FY2023": 283710,
    "FY2022": 226701, "FY2021": 187636,
})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {
    "FY2025": "16.27%", "FY2024": "13.60%", "FY2023": "12.46%",
    "FY2022": "13.04%", "FY2021": "14.00%",
})])
metric("Total Capital", "£'000", [("Total capital", {
    "FY2025": 482806, "FY2024": 400094, "FY2023": 340213,
    "FY2022": 257803, "FY2021": 218186,
})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {
    "FY2025": "17.33%", "FY2024": "15.78%", "FY2023": "14.94%",
    "FY2022": "14.83%", "FY2021": "16.28%",
})])
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", {
    "FY2025": 2785964, "FY2024": 2535096, "FY2023": 2277864,
    "FY2022": 1738779, "FY2021": 1340432,
})], note=(
    "Each year's own published figure is preserved. The 2024 report's OV1 table shows 2,535,339 for 2024 "
    "versus the KM1 figure 2,535,096; the KM1 value is used for consistency with the capital ratios."
))

bw.add_rwa_breakdown_sheet(
    title="United Trust Bank Limited — RWA Breakdown",
    subtitle="Consolidated UTB Partners Plc basis, £'000. Table UK OV1 - Overview of risk-weighted exposure amounts.",
    rows=[
        ("DATA", "Credit risk (excluding CCR)", {
            "FY2025": 2654604, "FY2024": 2420072, "FY2023": 2198914, "FY2022": 1702127, "FY2021": 1261719,
        }),
        ("DATA", "Counterparty credit risk (CCR), of which credit valuation adjustment (CVA)", {
            "FY2025": 2328, "FY2024": 1429, "FY2023": 1646, "FY2022": 1604, "FY2021": 0,
        }),
        ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {
            "FY2025": -146838, "FY2024": -157263, "FY2023": -150150, "FY2022": -145475, "FY2021": -70700,
        }),
        ("DATA", "Operational risk", {
            "FY2025": 275870, "FY2024": 271100, "FY2023": 227455, "FY2022": 180522, "FY2021": 149412,
        }),
        ("TOTAL", "Total risk-weighted exposure amount (Table UK OV1)", {
            "FY2025": 2785964, "FY2024": 2535339, "FY2023": 2277865, "FY2022": 1738778, "FY2021": 1340342,
        }),
    ],
    sources_text=rwa_sources(),
    first_col_width=68,
    source_height=200,
)

metric("Leverage Ratio", "£'000 / %", [
    ("Total exposure measure excluding claims on central banks", {
        "FY2025": 4500670, "FY2024": 3979115, "FY2023": 3502424,
        "FY2022": 2878801, "FY2021": 2318303,
    }),
    ("Leverage ratio excluding claims on central banks", {
        "FY2025": "10.1%", "FY2024": "8.7%", "FY2023": "8.1%",
        "FY2022": "7.9%", "FY2021": "8.1%",
    }),
])
metric("LCR", "£'000 / %", [
    ("Total high-quality liquid assets (HQLA), weighted value - average", {
        "FY2025": 384058, "FY2024": 322714, "FY2023": 257050,
        "FY2022": 252352,
    }),
    ("Total net cash outflows, adjusted value", {
        "FY2025": 113223, "FY2024": 40033, "FY2023": 32258,
        "FY2022": 19185,
    }),
    ("Liquidity coverage ratio", {
        "FY2025": "398.42%", "FY2024": "806.12%", "FY2023": "796.86%",
        "FY2022": "1315.36%", "FY2021": "1013.36%",
    }),
], note=(
    "The FY2021 disclosure does not provide a KM1 LCR table; only the headline ratio is available in the FY2022 "
    "comparative column. The FY2022 and FY2023 reports contain materially different comparative LCR figures; "
    "this series preserves each year's own as-reported value."
))
metric("NSFR", "£'000 / %", [
    ("Total available stable funding", {
        "FY2025": 3590720, "FY2024": 3376614, "FY2023": 3057724,
        "FY2022": 2555002,
    }),
    ("Total required stable funding", {
        "FY2025": 2570256, "FY2024": 2367394, "FY2023": 2057282,
        "FY2022": 1648317,
    }),
    ("NSFR ratio", {
        "FY2025": "139.71%", "FY2024": "142.63%", "FY2023": "148.63%",
        "FY2022": "155.01%",
    }),
], note="No 2021 NSFR headline or component values were located in the 2021 disclosure or the 2022 comparative column.")
metric("MREL Ratio", "£'000 / %", [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], note=(
    "No MREL ratio or numeric MREL requirement was located in the five UTB Partners Pillar 3 reports reviewed."
))

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 4450637, "FY2024": 3913260, "FY2023": 3440168, "FY2022": 2798317, "FY2021": 2254178}),
        ("Loans and advances to customers", {"FY2025": 3895213, "FY2024": 3487345, "FY2023": 3104356, "FY2022": 2426021, "FY2021": 1808607}),
        ("Deposits from customers", {"FY2025": 3847845, "FY2024": 3407271, "FY2023": 2797361, "FY2022": 2208300, "FY2021": 1715596}),
        ("Total capital and reserves", {"FY2025": 472836, "FY2024": 362862, "FY2023": 299799, "FY2022": 239109, "FY2021": 195632}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income", {"FY2025": 176431, "FY2024": 164971, "FY2023": 154146, "FY2022": 114642, "FY2021": 95140}),
        ("Profit on ordinary activities before tax", {"FY2025": 78686, "FY2024": 86369, "FY2023": 82739, "FY2022": 60156, "FY2021": 44437}),
        ("Profit after tax retained for the financial year", {"FY2025": 60680, "FY2024": 65772, "FY2023": 63274, "FY2022": 45395, "FY2021": 35422}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 362862, "FY2024": 299799, "FY2023": 239109, "FY2022": 195632, "FY2021": 174036}),
        ("Total comprehensive income for the year", {"FY2025": 60680, "FY2024": 65772, "FY2023": 63274, "FY2022": 45395, "FY2021": 35422}),
        ("Other equity movements, net", {"FY2025": 49294, "FY2024": -2709, "FY2023": -2584, "FY2022": -1918, "FY2021": -13826}),
        ("Closing equity", {"FY2025": 472836, "FY2024": 362862, "FY2023": 299799, "FY2022": 239109, "FY2021": 195632}),
    ],
    equity_changes_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "14.01%", "FY2024": "13.04%", "FY2023": "11.79%", "FY2022": "12.07%", "FY2021": "12.74%"}),
        ("Tier 1 Ratio", {"FY2025": "16.27%", "FY2024": "13.60%", "FY2023": "12.46%", "FY2022": "13.04%", "FY2021": "14.00%"}),
        ("Total Capital Ratio", {"FY2025": "17.33%", "FY2024": "15.78%", "FY2023": "14.94%", "FY2022": "14.83%", "FY2021": "16.28%"}),
        ("Leverage Ratio", {"FY2025": "10.1%", "FY2024": "8.7%", "FY2023": "8.1%", "FY2022": "7.9%", "FY2021": "8.1%"}),
        ("LCR", {"FY2025": "398.42%", "FY2024": "806.12%", "FY2023": "796.86%", "FY2022": "1315.36%", "FY2021": "1013.36%"}),
        ("NSFR", {"FY2025": "139.71%", "FY2024": "142.63%", "FY2023": "148.63%", "FY2022": "155.01%"}),
    ],
    note=(
        "Statutory cash-flow data is not available in the entity accounts (see the Cash Flow Statement "
        "sheet); the Balance Sheet, Profit & Loss, Statement of Changes in Equity and Asset Quality sheets "
        "are entity (Company-only) basis, while the ratio/RWA and other Pillar 3 metrics are consolidated "
        "UTB Partners basis, not standalone UTB Limited - see each sheet's own source note. FY2021 LCR is "
        "headline-only and FY2021 NSFR is unavailable; MREL is not publicly disclosed."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/UNITED TRUST BANK FINANCIALS.xlsx")
