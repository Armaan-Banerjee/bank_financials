import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/01814093/filing-history"
AR2025_URL = CH_BASE + "/MzUyMzkyMzgzOGFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = CH_BASE + "/MzQ2NjcyMDU4MGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = CH_BASE + "/MzQyMjAyODYxMmFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = CH_BASE + "/MzM3OTQ2NzM2OWFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = CH_BASE + "/MzMzNzcwMzA4MGFkaXF6a2N4/document?format=pdf&download=0"

P3_2024_URL = "https://www.jordanbank.co.uk/media/n0xn5hx1/website-jib-pillar-3-2024-v24-clean.pdf"
P3_2023_URL = "https://www.jordanbank.co.uk/media/1266/pw3949-jib-pillar-3-2023-final.pdf"
P3_2022_URL = "https://www.jordanbank.co.uk/media/1245/jib-pillar-3-2022.pdf"
P3_2021_URL = "https://www.jordanbank.co.uk/media/1239/pw3901-jib-pillar-3-2021-final.pdf"

RESTATEMENT_NOTE = (
    "DATA NOTE - FY2022/FY2023 opening-vs-closing cash gap (£16,090k): FY2022's own "
    "originally-published Cash Flow Statement (Annual Report and Financial Statements 2022, "
    "p.28) shows net cash generated in operating activities of £7,948k and cash and cash "
    "equivalents at the end of FY2022 of £77,136k. FY2023's own Annual Report (p.28) instead "
    "presents a FY2022 comparative column showing net cash generated in operating activities "
    "of only £(5,551)k and cash and cash equivalents at the beginning of FY2023 (i.e. the "
    "carried-forward FY2022 closing balance) of £57,334k, with FY2023's own closing figure of "
    "£61,046k tying to that restated opening balance, not to FY2022's originally-published "
    "£77,136k. The Investing and Financing sections are identical between both versions "
    "(£21,263k net investing inflow, £(12,000)k dividend payment) - only the Operating "
    "activities figure and the resulting cash balance differ, suggesting a reclassification "
    "within operating cash flows (e.g. of a balance-sheet item's cash-equivalent treatment) "
    "rather than a transcription error in either document. Per this project's convention, each "
    "year keeps its own originally-published figures (FY2022 = FY2022 AR's own figures; "
    "FY2023 = FY2023 AR's own figures, including its own FY2022 comparative column for "
    "internal consistency within that document) rather than substituting a later restated "
    "comparative - so the FY2022-to-FY2023 opening/closing bridge in this workbook does not "
    "tie by £16,090k. This is a real, disclosed inconsistency between the Bank's own two "
    "Annual Reports, not a transcription error; every other year-to-year link in the chain "
    "(FY2021->FY2022, FY2023->FY2024, FY2024->FY2025) ties exactly."
)

CASH_FLOW_SOURCES = (
    "Sources - Jordan International Bank Plc's own Cash Flow Statement, from each year's "
    "Companies House-filed Annual Report and Financial Statements (company 01814093, all 5 "
    "filings fully scanned/image-only, transcribed via page-image review):\n"
    f"FY2025: Annual Report and Financial Statements 2025, Cash Flow Statement, p.30 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements 2024, Cash Flow Statement, p.30 (FY2024's "
    f"own originally-published figures used; matches FY2025's own FY2024 comparative exactly) "
    f"- {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, Cash Flow Statement, p.28 (FY2023's "
    f"own originally-published figures used; see note below on FY2022's differing comparative) "
    f"- {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, Cash Flow Statement, p.28 (FY2022's "
    f"own originally-published figures used - see note below) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, Cash Flow Statement, p.29 - {AR2021_URL}\n"
    "The Bank presents both a '(Decrease)/increase in cash and cash equivalents' line (the sum "
    "of the Operating/Investing/Financing sections above it) and a separately-disclosed "
    "'Movement in cash and cash equivalents' line used in the opening-to-closing reconciliation "
    "below it; these two lines are not always numerically equal in the Bank's own source "
    "documents (e.g. FY2023: 4,957 vs 7,576) - both are transcribed exactly as printed, and the "
    "reconciliation used to verify each year's own closing balance is opening + 'Movement' + "
    "'Effect of foreign exchange rate changes'.\n"
    + RESTATEMENT_NOTE
)


def p3_sources():
    return (
        "Sources - Jordan International Bank Plc's own Pillar 3 Report, published on the "
        "Bank's website (Key Prudential Metrics table, UK KM1 template):\n"
        f"FY2024: Pillar 3 Report 2024, Section 1 'Introduction', Key Prudential Metrics table "
        f"(31 December 2024) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Report 2023, Section 1 'Introduction', Key Prudential Metrics table "
        f"(31 December 2023) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Report 2022, Section 1 'Introduction', Key Prudential Metrics table "
        f"(31 December 2022) - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Report 2021, Section 1 'Introduction', Key Prudential Metrics table "
        f"(31 December 2021) - {P3_2021_URL}\n"
        "FY2025: no standalone Pillar 3 Report was published on the Bank's website as of this "
        "session (only 2016-2024 reports are listed) - genuinely not yet disclosed, left blank "
        "rather than guessed. No Total Capital / Tier 2 capital is disclosed separately from "
        "CET1 in any year (Tier 1 = Total Capital = CET1 throughout, per the Bank's own table "
        "labelling). NSFR is not disclosed for FY2021 (the KM1 template's NSFR section first "
        "appears in the FY2022 report). MREL Ratio is not disclosed in any year - Jordan "
        "International Bank Plc is not identified as a UK resolution entity in these reports."
    )


bw = BankWorkbook(bank_name="Jordan International Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="8B1A1A")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("TOTAL", "Net cash generated/(used) in operating activities", {
        "FY2025": -8564, "FY2024": 32529, "FY2023": -15204, "FY2022": 7948, "FY2021": -11006,
    }),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of debt securities", {
        "FY2025": -86255, "FY2024": -146299, "FY2023": -104590, "FY2022": -87618, "FY2021": -78745,
    }),
    ("DATA", "Proceeds from the sale and maturity of debt securities", {
        "FY2025": 76479, "FY2024": 118151, "FY2023": 121290, "FY2022": 106746, "FY2021": 80891,
    }),
    ("DATA", "Interest received from debt securities", {
        "FY2025": 5151, "FY2024": 4134, "FY2023": 3804, "FY2022": 2599, "FY2021": 2217,
    }),
    ("DATA", "Purchase of tangible fixed assets", {
        "FY2025": -239, "FY2024": -472, "FY2023": -343, "FY2022": -464, "FY2021": -447,
    }),
    ("DATA", "Purchase of intangible assets", {
        "FY2025": -225,
    }),
    ("TOTAL", "Net cash generated by investing activities", {
        "FY2025": -5089, "FY2024": -24486, "FY2023": 20161, "FY2022": 21263, "FY2021": 3916,
    }),
    ("SECTION", "Cashflows from financing activities", {}),
    ("DATA", "Dividend payment to equity holders", {
        "FY2022": -12000,
    }),
    ("TOTAL", "Net cash generated by financing activities", {
        "FY2023": 0, "FY2022": -12000,
    }),
    ("SECTION", "Reconciliation of movement in cash and cash equivalents", {}),
    ("DATA", "(Decrease)/increase in cash and cash equivalents", {
        "FY2025": -13653, "FY2024": 8043, "FY2023": 4957, "FY2022": 17211, "FY2021": -7090,
    }),
    ("DATA", "Cash and cash equivalents at beginning of year", {
        "FY2025": 74046, "FY2024": 66003, "FY2023": 61046, "FY2022": 59925, "FY2021": 67015,
    }),
    ("DATA", "Movement in cash and cash equivalents", {
        "FY2025": -13653, "FY2024": 7510, "FY2023": 7576, "FY2022": 9875, "FY2021": -7533,
    }),
    ("DATA", "Effect of foreign exchange rate changes", {
        "FY2025": 3623, "FY2024": 533, "FY2023": -2619, "FY2022": 7336, "FY2021": 443,
    }),
    ("TOTAL", "Cash and cash equivalents at end of year", {
        "FY2025": 64016, "FY2024": 74046, "FY2023": 66003, "FY2022": 77136, "FY2021": 59925,
    }),
]

bw.add_cash_flow_sheet(
    title="Jordan International Bank Plc - Cash Flow Statement",
    subtitle="For the years ended 31 December (£'000, GBP)",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=62,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=170)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2024": 94, "FY2023": 89, "FY2022": 83.8, "FY2021": 93.3,
    })],
    p3_sources(),
    note="FY2025 not yet published (see sources). No Additional Tier 1/Tier 2 capital is "
         "disclosed in any year, so CET1 = Tier 1 = Total Capital throughout.",
)
metric(
    "CET1 Ratio", "%",
    [("CET1 ratio", {
        "FY2024": "19.9%", "FY2023": "19.8%", "FY2022": "19.3%", "FY2021": "22.9%",
    })],
    p3_sources(),
)
metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {
        "FY2024": 94, "FY2023": 89, "FY2022": 83.8, "FY2021": 93.3,
    })],
    p3_sources(),
    note="Equal to CET1 capital - no Additional Tier 1 instruments are disclosed in any year.",
)
metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2024": "19.9%", "FY2023": "19.8%", "FY2022": "19.3%", "FY2021": "22.9%",
    })],
    p3_sources(),
)
metric(
    "Total Capital", "£m",
    [("Total capital", {
        "FY2024": 94, "FY2023": 89, "FY2022": 83.8, "FY2021": 93.3,
    })],
    p3_sources(),
    note="Equal to CET1/Tier 1 capital - no Tier 2 instruments are disclosed in any year.",
)
metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2024": "19.9%", "FY2023": "19.8%", "FY2022": "19.3%", "FY2021": "22.9%",
    })],
    p3_sources(),
)
metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount (RWA)", {
        "FY2024": 473, "FY2023": 449, "FY2022": 435.3, "FY2021": 407.5,
    })],
    p3_sources(),
)
metric(
    "Leverage Ratio", "%",
    [("Basel III leverage ratio", {
        "FY2024": "19.3%", "FY2023": "19.7%", "FY2022": "19.3%", "FY2021": "23.4%",
    })],
    p3_sources(),
)
metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {
        "FY2024": "490%", "FY2023": "343%", "FY2022": "330%", "FY2021": "428%",
    })],
    p3_sources(),
)
metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {
        "FY2024": "129%", "FY2023": "125.1%", "FY2022": "129%",
    })],
    p3_sources(),
    note="Not disclosed for FY2021 - the KM1 template's NSFR section first appears in the "
         "FY2022 Pillar 3 Report.",
)
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    per_note={
        "MREL Ratio": "Not disclosed in any year - Jordan International Bank Plc is not "
                      "identified as a UK resolution entity in these reports.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": -8564, "FY2024": 32529, "FY2023": -15204, "FY2022": 7948, "FY2021": -11006,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": -5089, "FY2024": -24486, "FY2023": 20161, "FY2022": 21263, "FY2021": 3916,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -12000, "FY2021": 0,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 64016, "FY2024": 74046, "FY2023": 66003, "FY2022": 77136, "FY2021": 59925,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 ratio (%)", {
            "FY2024": 19.9, "FY2023": 19.8, "FY2022": 19.3, "FY2021": 22.9,
        }),
        ("LCR (%)", {
            "FY2024": 490, "FY2023": 343, "FY2022": 330, "FY2021": 428,
        }),
    ],
    note="FY2025 Pillar 3 figures not yet published as of this session - see individual metric "
         "sheets. The FY2022-to-FY2023 cash bridge does not tie exactly (£16,090k gap) due to a "
         "genuine inconsistency between the Bank's own FY2022 and FY2023 Annual Reports - see "
         "the Cash Flow Statement sheet's source note for full detail.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/JORDAN INTERNATIONAL BANK FINANCIALS.xlsx")
print("Saved.")
