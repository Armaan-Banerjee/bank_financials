import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Kroo Bank Ltd (FRN 953772, Companies House 10359002, incorporated 5 Sept
# 2016) was authorised as a bank with restrictions on 7 July 2021 and only
# came within scope of UK bank regulation from that date. Only 4 Annual
# Reports have ever been published (FY2021-FY2024, year-end 31 December) -
# no FY2025 report exists yet as of this build (next one due ~Sept/Oct 2026)
# - so only 4 years are included here rather than padding to 5, the same
# pattern as Brown Shipley/Griffin Bank.
YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2021_URL = "https://www.kroo.com/files/kroo-annual-report-2021.pdf"
AR2022_URL = "https://www.kroo.com/files/kroo-annual-report-2022.pdf"
AR2023_URL = "https://www.kroo.com/files/kroo-annual-report-2023.pdf"
AR2024_URL = "https://www.kroo.com/files/kroo-annual-report-2024.pdf"
P3_2021_URL = "https://www.kroo.com/files/kroo-pillar-3-disclosures-2021.pdf"
P3_2022_URL = "https://www.kroo.com/files/kroo-pillar-3-disclosures-2022.pdf"
P3_2023_URL = "https://www.kroo.com/files/kroo-pillar-3-disclosures-2023.pdf"
P3_2024_URL = "https://www.kroo.com/files/kroo-pillar-3-disclosures-2024.pdf"

ENTITY_NOTE = (
    "Kroo Bank Ltd (Companies House 10359002) was authorised as a bank with restrictions on 7 July 2021 "
    "and only came within scope of UK bank regulation from that date - FY2021 is therefore its first "
    "reporting period as a regulated bank. Only 4 Annual Reports have ever been published "
    "(FY2021-FY2024) - no FY2025 Annual Report or Pillar 3 report exists yet as of this build, so only "
    "4 years are included here rather than padding to 5."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Kroo Bank Ltd's own Statement of Cash Flows, each year's own originally "
    "published figures used (no restatement affects the cash flow statement itself):\n"
    "FY2024: Annual Report 2024, p.37 (Statement of cash flows) - " + AR2024_URL + "\n"
    "FY2023: Annual Report 2023, p.38 (Statement of Cash Flows) - " + AR2023_URL + "\n"
    "FY2022: Annual Report 2022, p.28 (Statement of Cash Flows) - " + AR2022_URL + "\n"
    "FY2021: Annual Report 2021, p.27 (Statement of Cash Flows) - " + AR2021_URL + "\n"
    "Note: the FY2023 Annual Report's own FY2022 comparative column and the FY2022 Annual Report's own "
    "FY2022 figures present operating-activity line items with different labels/groupings (e.g. FY2022's "
    "own report shows a standalone 'Interest on debt securities' line, while FY2023's report combines "
    "this into a single 'Net interest income' line) - each year's own originally published report's own "
    "line items are used here rather than a later report's re-presentation, consistent with this "
    "project's convention.\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Kroo Bank Ltd Pillar 3 Disclosures, each year's own originally published figures used:\n"
        "FY2024: Pillar 3 Disclosures 2024, Table 3 (Key metrics, 31 Dec 2024 column) - " + P3_2024_URL + "\n"
        "FY2023: Pillar 3 Disclosures 2023, Table 3 (Key metrics, 31 Dec 2023 column) - " + P3_2023_URL + "\n"
        "FY2022: Pillar 3 Disclosures 2022, Table 3 (Capital resources)/Table 6 (Leverage ratio) - "
        + P3_2022_URL + "\n"
        "FY2021: Pillar 3 Disclosures 2021, Table 3 (Capital resources)/Table 6 (Leverage ratio) - "
        + P3_2021_URL + "\n"
        + extra
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Kroo Bank Ltd", years=YEARS, year_label=YEAR_LABEL, header_color="655905")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Loss before taxation", {
        "FY2024": -19287124, "FY2023": -27927373, "FY2022": -16318251, "FY2021": -9064658,
    }),
    ("DATA", "Depreciation", {"FY2024": 196429, "FY2023": 179217, "FY2022": 94230, "FY2021": 52641}),
    ("DATA", "Loss on disposal of fixed assets", {"FY2024": 25053}),
    ("DATA", "Impairment charge", {"FY2024": 1031330, "FY2023": 59996, "FY2022": 1151}),
    ("DATA", "Share option charge / Value of share options issued", {
        "FY2024": 613689, "FY2023": 760478, "FY2022": 454457, "FY2021": 711032,
    }),
    ("DATA", "Unauthorised overdraft operational loss", {"FY2024": -21790}),
    ("DATA", "Net interest income", {"FY2024": -9459226, "FY2023": -6159249}),
    ("DATA", "Interest on debt securities", {"FY2022": -116040}),
    ("DATA", "Interest on convertible loan", {"FY2021": 259205}),
    ("DATA", "(Increase)/decrease in other assets", {
        "FY2024": -1221715, "FY2023": -1960147, "FY2022": -934468, "FY2021": -232127,
    }),
    ("DATA", "Increase/(decrease) in other liabilities", {
        "FY2024": -2599814, "FY2023": 2769451, "FY2022": 1188991, "FY2021": 359711,
    }),
    ("DATA", "Movement in customer advances", {"FY2024": -14807003, "FY2023": -2315093}),
    ("DATA", "Movement in customer deposits", {"FY2024": 111086286, "FY2023": 850875499}),
    ("DATA", "Movement in customer balances", {"FY2022": 1231895}),
    ("DATA", "R&D tax credit received", {"FY2023": 1369199, "FY2021": 478309}),
    ("DATA", "Interest received", {"FY2024": 49131596, "FY2023": 27920335}),
    ("DATA", "Interest paid", {"FY2024": -39841442, "FY2023": -19112492}),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2024": 74846269, "FY2023": 826459821, "FY2022": -14398035, "FY2021": -7435887,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of tangible fixed assets", {
        "FY2024": -15265, "FY2023": -283243, "FY2022": -270719, "FY2021": -70707,
    }),
    ("DATA", "Proceeds of sale of tangible fixed assets", {"FY2022": 800}),
    ("DATA", "Purchase of debt securities", {"FY2022": -19976892}),
    ("DATA", "Sale of debt securities", {"FY2023": 10000000, "FY2022": 10120349}),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2024": -15265, "FY2023": 9716757, "FY2022": -10126462, "FY2021": -70707,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of convertible loan note", {}),
    ("DATA", "Issue of share capital / Issue of shares", {
        "FY2024": 12508985, "FY2023": 18020475, "FY2022": 27268402, "FY2021": 15064176,
    }),
    ("DATA", "Cost of share issues", {"FY2023": -72726}),
    ("TOTAL", "Net cash from financing activities", {
        "FY2024": 12508985, "FY2023": 17947749, "FY2022": 27268402, "FY2021": 15064176,
    }),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {
        "FY2024": 87339989, "FY2023": 854124327, "FY2022": 2743905, "FY2021": 7557582,
    }),
    ("DATA", "Cash at beginning of year", {
        "FY2024": 865759423, "FY2023": 11635096, "FY2022": 8891191, "FY2021": 1333609,
    }),
    ("TOTAL", "Cash at end of year", {
        "FY2024": 953099412, "FY2023": 865759423, "FY2022": 11635096, "FY2021": 8891191,
    }),
]

bw.add_cash_flow_sheet(
    title="Kroo Bank Ltd — Statement of Cash Flows",
    subtitle="Bank-only, £; each year's own originally reported line items preserved (see source note)",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=180,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=48, source_height=150)


metric(
    "CET1 Capital", "£",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2024": 7327982, "FY2023": 14288553, "FY2022": 22428333, "FY2021": 9557150,
    })],
    p3_sources(
        "Note: the FY2024 Pillar 3 report's own FY2023 comparative shows a materially different, "
        "restated CET1/Tier 1/Total Capital figure of £13,429,696 (and RWA £30,694,218 vs the "
        "originally-published £30,694,218 - RWA is unchanged, only capital changed), explicitly "
        "attributed by the document itself to 'a prior year adjustment' detailed in note 1 of the "
        "2024 Annual Report. FY2023's own originally published figure (£14,288,553) is used here per "
        "this project's convention.\n"
    ),
)
metric(
    "CET1 Ratio", "%",
    [("Common equity tier 1 ratio", {
        "FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.18%", "FY2021": "287.76%",
    })],
    p3_sources(),
    note="Extreme early-year ratios (287.76% FY2021, 93.18% FY2022) reflect a genuine early-mobilisation "
         "position - capital raised well ahead of RWA growth, confirmed internally consistent against "
         "each year's own RWA figure, not a transcription error.",
)
metric(
    "Tier 1 Capital", "£",
    [("Tier 1 capital", {
        "FY2024": 7327982, "FY2023": 14288553, "FY2022": 22428333, "FY2021": 9557150,
    })],
    p3_sources(),
    note="No Additional Tier 1 instruments in issue any year - Tier 1 capital equals CET1 capital "
         "throughout, per the source's own Table 3/Key metrics.",
)
metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.18%", "FY2021": "287.76%",
    })],
    p3_sources(),
)
metric(
    "Total Capital", "£",
    [("Total capital", {
        "FY2024": 7327982, "FY2023": 14288553, "FY2022": 22428333, "FY2021": 9557150,
    })],
    p3_sources(),
    note="No Tier 2 instruments in issue any year - Total capital equals CET1/Tier 1 capital throughout.",
)
metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.18%", "FY2021": "287.76%",
    })],
    p3_sources(),
)
metric(
    "Total RWAs", "£",
    [("Total risk-weighted exposure amount", {
        "FY2024": 30590678, "FY2023": 30694218, "FY2022": 24070601, "FY2021": 3321197,
    })],
    p3_sources(),
)
metric(
    "Leverage Ratio", "%",
    [("Leverage ratio excluding claims on central banks", {
        "FY2024": "21.2%", "FY2023": "55.6%", "FY2022": "99.97%", "FY2021": "91.82%",
    })],
    p3_sources(),
    note="FY2021's own Pillar 3 report does not show the 'claims on central banks excluded, capped at "
         "level of liabilities' adjustment line that appears in every later year's reconciliation table "
         "- its 91.82% is computed on Total Balance Sheet Exposures with no such exclusion applied, a "
         "genuine methodology basis break in the Bank's first reporting year, not a transcription choice.",
)
metric(
    "LCR", "%",
    [("Liquidity coverage ratio", {
        "FY2024": "758%", "FY2023": "4248%", "FY2022": "12926%", "FY2021": "13333%",
    })],
    p3_sources(
        "Note: FY2022's own contemporaneous Pillar 3 report (Table 9) shows a materially different, "
        "much larger LCR of 258,343% for the 31 Dec 2022 quarter alone, apparently using a shorter/"
        "different averaging window than the full-year methodology used in the FY2023 report's own "
        "FY2022 comparative (12,926%, used here). Both the Bank's own FY2021 and FY2022 narrative "
        "sections explicitly caveat that these ratios are 'not representative' during the mobilisation "
        "phase, when the Bank held only small testing-purpose deposit balances - flagged here rather "
        "than silently reconciled.\n"
    ),
    note="Extreme ratios throughout (up to 13,333%) reflect the Bank's own explicit narrative that these "
         "are not representative during its early mobilisation/deposit-ramp phase - genuine per the "
         "source, not a transcription error.",
)
metric(
    "NSFR", "%",
    [("Net stable funding ratio", {"FY2024": "4522%", "FY2023": "5272%", "FY2022": "493%"})],
    p3_sources(),
    note="Not disclosed for FY2021 - the Bank's FY2021 Pillar 3 report discloses no NSFR table at all "
         "(only LCR), confirmed genuinely absent rather than an access gap.",
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], sources_text=p3_sources())

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2024": 74846269, "FY2023": 826459821, "FY2022": -14398035, "FY2021": -7435887,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2024": -15265, "FY2023": 9716757, "FY2022": -10126462, "FY2021": -70707,
        }),
        ("Net cash from financing activities", {
            "FY2024": 12508985, "FY2023": 17947749, "FY2022": 27268402, "FY2021": 15064176,
        }),
        ("Cash at end of year", {
            "FY2024": 953099412, "FY2023": 865759423, "FY2022": 11635096, "FY2021": 8891191,
        }),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.18%", "FY2021": "287.76%"}),
        ("Tier 1 Ratio", {"FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.18%", "FY2021": "287.76%"}),
        ("Total Capital Ratio", {"FY2024": "24.0%", "FY2023": "46.6%", "FY2022": "93.18%", "FY2021": "287.76%"}),
        ("Leverage Ratio", {"FY2024": "21.2%", "FY2023": "55.6%", "FY2022": "99.97%", "FY2021": "91.82%"}),
        ("LCR", {"FY2024": "758%", "FY2023": "4248%", "FY2022": "12926%", "FY2021": "13333%"}),
        ("NSFR", {"FY2024": "4522%", "FY2023": "5272%", "FY2022": "493%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's "
         "own source citation for the underlying document/page. Only 4 years shown - no FY2025 Annual "
         "Report or Pillar 3 report has been published yet.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/KROO BANK FINANCIALS.xlsx")
