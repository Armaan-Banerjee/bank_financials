import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

AR2025_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-278301"
AR2024_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-265184"
AR2023_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-223741"
AR2022_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-175531"
AR2021_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-141596"

P3_2025_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-278302"
P3_2023_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-223742"
P3_2022_URL = "https://www.handelsbanken.co.uk/tron/gbpu/info/contents/v1/document/52-175532"

ENTITY_NOTE = (
    "ENTITY NOTE: Handelsbanken plc (company number 11305395, FRN 806852) was incorporated 11 April 2018 as the "
    "UK-incorporated subsidiary that Handelsbanken's (Svenska Handelsbanken AB) UK business restructured into from "
    "a branch. Because of that youth, FY2021 (its third full year) is the earliest year for which the annual report "
    "distinguishes a consolidated 'UK Group' cash flow statement from the standalone parent-only 'Bank' one - the "
    "FY2021 Annual Report itself presents only a single, undifferentiated 'Cash Flow Statement' (i.e. Bank and "
    "Group were not yet reported separately). To keep this sheet on a consistent Group/consolidated basis "
    "throughout, FY2021 cash flow figures below are the Group-restated comparative column as re-presented in the "
    "FY2022 Annual Report (which differs modestly, line by line, from the FY2021 report's own originally-reported "
    "figures - net cash flow totals below are internally consistent with this restated basis)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Handelsbanken plc UK Group consolidated cash flow statement, £'000:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.83 (Consolidated cash flow statement, UK "
    f"Group) - {AR2025_URL}\n"
    f"FY2023: Annual Report 2023, p.87 (Cash flow statement, UK Group) - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, p.90 (Consolidated cash flow statement, UK Group) - {AR2022_URL}\n"
    f"FY2021: Annual Report 2022, p.90 (2021 comparative column, UK Group, restated) - {AR2022_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: line items shift modestly across vintages (e.g. 'Acquisition of right of use asset' moved "
    "from the Investing section in the FY2021 report to an Operating-activities adjustment from FY2022 onward; an "
    "'Accrued interest' line appears only in the FY2025 report). Blank cells indicate that year's statement did not "
    "show that specific line. Operating/investing/financing subtotals and the net cash movement for the year are "
    "internally consistent and reconcile exactly in every year shown; the opening-plus-movement-plus-FX bridge to "
    "the closing cash balance is exact for FY2021-FY2024, and within an immaterial £13k rounding difference (on a "
    "balance of £7.76bn) for FY2025, as published."
)


def p3_sources(source_doc="Risk and Capital Information according to Pillar 3 - 2025", page="8-9", url=P3_2025_URL):
    return (
        "Sources - Handelsbanken plc UK Group consolidated basis (UK KM1 Key metrics template):\n"
        f"{source_doc}, p.{page} - {url}"
    )


bw = BankWorkbook(bank_name="Handelsbanken plc", years=YEARS, header_color="003D6B")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 421832, "FY2024": 498022, "FY2023": 574764, "FY2022": 343916, "FY2021": 135366}),
    ("DATA", "Net credit (gains)/losses", {"FY2025": -7162, "FY2024": -10164, "FY2023": 3788, "FY2022": 4415, "FY2021": -7945}),
    ("DATA", "Net losses/(gains) on disposal of property, equipment and intangible assets", {"FY2025": 101, "FY2024": 13, "FY2023": 65, "FY2022": -818, "FY2021": -775}),
    ("DATA", "Depreciation, amortisation and impairment", {"FY2025": 36386, "FY2024": 28159, "FY2023": 25129, "FY2022": 23420, "FY2021": 32815}),
    ("DATA", "Lease liability interest expense", {"FY2025": 3222, "FY2024": 1734, "FY2023": 1535, "FY2022": 1328, "FY2021": 1555}),
    ("DATA", "Acquisition of right of use asset", {"FY2025": -40681, "FY2024": -8854, "FY2023": -8866, "FY2022": -7388, "FY2021": -3100}),
    ("DATA", "Provisions", {"FY2025": -75, "FY2024": -2381, "FY2023": -6112, "FY2022": 4654, "FY2021": 3526}),
    ("DATA", "Other loans to central banks", {"FY2024": 88371, "FY2023": 11529, "FY2022": 2879, "FY2021": -4386}),
    ("DATA", "Loans to other credit institutions", {"FY2025": 87866, "FY2024": 1634611, "FY2023": 289812, "FY2022": -1598199, "FY2021": -241068}),
    ("DATA", "Loans to the public", {"FY2025": -580612, "FY2024": 207791, "FY2023": 1000930, "FY2022": 1144359, "FY2021": 688529}),
    ("DATA", "Due to credit institutions", {"FY2025": -964086, "FY2024": -1907801, "FY2023": -352481, "FY2022": -636336, "FY2021": -1358541}),
    ("DATA", "Deposits from the public", {"FY2025": 587411, "FY2024": 521089, "FY2023": -127216, "FY2022": 1284768, "FY2021": 122809}),
    ("DATA", "Issued securities", {"FY2025": -383229, "FY2024": 1568, "FY2023": -55354, "FY2022": -786756, "FY2021": -3147}),
    ("DATA", "Lease liabilities (change)", {"FY2025": 38681, "FY2024": 9469, "FY2023": 7327, "FY2022": 4549, "FY2021": 2589}),
    ("DATA", "Income tax paid", {"FY2025": -119110, "FY2024": -140399, "FY2023": -161747, "FY2022": -90301, "FY2021": -32713}),
    ("DATA", "Other assets", {"FY2025": 91100, "FY2024": -89575, "FY2023": 25690, "FY2022": -25292, "FY2021": 5058}),
    ("DATA", "Prepaid expenses and accrued income", {"FY2025": -28, "FY2024": -2256, "FY2023": -2198, "FY2022": -75, "FY2021": -1632}),
    ("DATA", "Other liabilities", {"FY2025": 4528, "FY2024": 658, "FY2023": -1424, "FY2022": -3036, "FY2021": -711}),
    ("DATA", "Accrued expenses and deferred income", {"FY2025": 695, "FY2024": -1614, "FY2023": 1097, "FY2022": -3233, "FY2021": -5470}),
    ("DATA", "Accrued interest", {"FY2025": 3884, "FY2024": 7868}),
    ("DATA", "Other operating items", {"FY2022": -11971, "FY2021": -369}),
    ("TOTAL", "Cash (outflow)/inflow from operating activities", {"FY2025": -819277, "FY2024": 836309, "FY2023": 1215640, "FY2022": -351346, "FY2021": -670515}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Assets held for sale", {"FY2022": 963, "FY2021": 65}),
    ("DATA", "Acquisitions of property and equipment", {"FY2025": -14385, "FY2024": -7728, "FY2023": -7000, "FY2022": -4714, "FY2021": -3323}),
    ("DATA", "Disposal of property and equipment", {"FY2025": 100, "FY2024": 277, "FY2023": 166, "FY2022": 1216, "FY2021": 996}),
    ("DATA", "Acquisitions/development of intangible assets", {"FY2025": -5526, "FY2024": -10663, "FY2023": -11138, "FY2022": -6635, "FY2021": -3463}),
    ("TOTAL", "Cash outflow from investing activities", {"FY2025": -19811, "FY2024": -18114, "FY2023": -17972, "FY2022": -9170, "FY2021": -5725}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividends paid to company's shareholders", {"FY2025": -484687, "FY2024": -625341, "FY2023": -265516}),
    ("DATA", "Payments made for lease liabilities", {"FY2025": -11901, "FY2024": -11884, "FY2023": -12424, "FY2022": -12141, "FY2021": -13551}),
    ("TOTAL", "Cash outflow from financing activities", {"FY2025": -496588, "FY2024": -637225, "FY2023": -277940, "FY2022": -12141, "FY2021": -13551}),
    ("TOTAL", "Cash (outflow)/inflow for the year", {"FY2025": -1335676, "FY2024": 180970, "FY2023": 919728, "FY2022": -372657, "FY2021": -689791}),
    ("DATA", "Cash balance at beginning of year", {"FY2025": 9097190, "FY2024": 8916214, "FY2023": 7996622, "FY2022": 8368955, "FY2021": 9058894}),
    ("DATA", "Net foreign exchange differences", {"FY2024": 6, "FY2023": -136, "FY2022": 324, "FY2021": -148}),
    ("TOTAL", "Cash balance at end of year", {"FY2025": 7761527, "FY2024": 9097190, "FY2023": 8916214, "FY2022": 7996622, "FY2021": 8368955}),
]

bw.add_cash_flow_sheet(
    title="Handelsbanken plc — Consolidated Cash Flow Statement",
    subtitle="Handelsbanken plc UK Group (consolidated basis), £'000 unless stated. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=220,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"UK Group consolidated basis, {unit}" if unit else "UK Group consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=100)


FY2021_BASIS_NOTE = (
    "No Pillar 3 / UK KM1 report was published for FY2021 (the earliest found on Handelsbanken plc's own site is "
    "2022). FY2021 figures instead come from the 'Capital adequacy ratios'/'Capital resources' sections of the "
    f"FY2021 Annual Report ({AR2021_URL}), which pre-date the Group/Bank split noted on the Cash Flow Statement "
    "sheet - treat FY2021 as the entity's own (Bank=Group) basis at that time, not a formal KM1 disclosure."
)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 2155, "FY2024": 2089, "FY2023": 2214, "FY2022": 2426, "FY2021": 2464})],
    p3_sources(),
    note=FY2021_BASIS_NOTE,
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "17.5%", "FY2024": "18.0%", "FY2023": "20.0%", "FY2022": "21.3%", "FY2021": "20.2%"})],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " FY2025/FY2023 ratios are shown after deduction of that year's recommended dividend "
         "(the Board's stated practice - e.g. the FY2025 dividend recommendation reduced the CET1 ratio from 19.5% "
         "to the 17.5% shown here).",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 2155, "FY2024": 2089, "FY2023": 2214, "FY2022": 2426, "FY2021": 2464})],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " Equal to CET1 capital in every year shown - the Bank has not issued any Additional "
         "Tier 1 (AT1) capital.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "17.5%", "FY2024": "18.0%", "FY2023": "20.0%", "FY2022": "21.3%", "FY2021": "20.2%"})],
    p3_sources(),
    note=FY2021_BASIS_NOTE,
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 2456, "FY2024": 2389, "FY2023": 2614, "FY2022": 2826, "FY2021": 2864})],
    p3_sources(),
    note=FY2021_BASIS_NOTE,
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "20.0%", "FY2024": "20.6%", "FY2023": "23.6%", "FY2022": "24.8%", "FY2021": "23.5%"})],
    p3_sources(),
    note=FY2021_BASIS_NOTE,
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 12309, "FY2024": 11605, "FY2023": 11066, "FY2022": 11404, "FY2021": 12176})],
    p3_sources(),
    note=FY2021_BASIS_NOTE,
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 23011, "FY2024": 22473, "FY2023": 24356, "FY2022": 25680}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "9.4%", "FY2024": "9.3%", "FY2023": "9.1%", "FY2022": "9.4%"}),
        ("Leverage ratio - CRR2 total exposure basis, £m (FY2021 only, pre-KM1 methodology)", {"FY2021": 33635}),
        ("Leverage ratio - CRR2 basis (%) (FY2021 only, pre-KM1 methodology)", {"FY2021": "7.3%"}),
    ],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " The UK Group is not in scope of the binding UK leverage ratio minimum requirement "
         "(below the size threshold) but the PRA expects a ratio above 3.25%, which it has maintained throughout. "
         "FY2021's figure uses a different, larger exposure measure (Tier 1 capital / total CRR2 exposure, "
         "including claims on central banks) than the 'excluding claims on central banks' KM1 basis used from "
         "FY2022 onward - the two are not directly comparable, hence the separate rows.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 8039, "FY2024": 8853, "FY2023": 7946, "FY2022": 7904}),
        ("Total net cash outflows (adjusted value)", {"FY2025": 4572, "FY2024": 5400, "FY2023": 5220, "FY2022": 5377}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "180%", "FY2024": "165%", "FY2023": "153%", "FY2022": "147%", "FY2021": "Not disclosed (KM1 basis)"}),
    ],
    p3_sources(),
    note=FY2021_BASIS_NOTE + " LCR is a 12-month average of month-end observations. The FY2023 and FY2024 Annual "
         "Reports separately quote a narrower, single-point 'as at year end' LCR narrative (147% and 180% "
         "respectively) that happens to coincide with the average-basis KM1 figures shown here for those two years, "
         "but the FY2022 narrative figure (147%) differs from an earlier average-basis disclosure; treat the KM1 "
         "table above as the primary source. The FY2021 Annual Report separately states a spot LCR of 475% at "
         "31 December 2021 - not on the same (averaged, KM1) basis as the figures above, so not included as a "
         "comparable data point.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2025": 19047, "FY2024": 19210, "FY2023": 19525, "FY2022": 20678}),
        ("Total required stable funding", {"FY2025": 14676, "FY2024": 14166, "FY2023": 14950, "FY2022": 15953}),
        ("NSFR ratio (%)", {"FY2025": "130%", "FY2024": "136%", "FY2023": "131%", "FY2022": "130%", "FY2021": "Not disclosed"}),
    ],
    p3_sources(),
    note=FY2021_BASIS_NOTE,
)

metric(
    "MREL Ratio", "£m / %",
    [
        ("MREL-eligible senior non-preferred debt issued", {"FY2025": 450, "FY2024": 200, "FY2023": 50, "FY2022": 150, "FY2021": 200}),
        ("Total capital resources (Total capital, see Total Capital sheet)", {"FY2025": 2456, "FY2024": 2389, "FY2023": 2614, "FY2022": 2826, "FY2021": 2864}),
        ("Total MREL ratio (% of RWA)", {"FY2025": "23.6%"}),
    ],
    (
        "Sources - Handelsbanken plc UK Group, Risk and Capital Management section of each Annual Report:\n"
        f"FY2025: Annual Report 2025, p.67 - {AR2025_URL}\n"
        f"FY2024: Annual Report 2024, p.65 - {AR2024_URL}\n"
        f"FY2023: Annual Report 2023, p.70 - {AR2023_URL}\n"
        f"FY2022: Annual Report 2022, p.79 - {AR2022_URL}\n"
        f"FY2021: Annual Report 2021, p.63 - {AR2021_URL}"
    ),
    note="Handelsbanken plc, as a material subsidiary of a foreign-owned group, is subject to MREL (21.2% of RWA "
         "as at FY2025, reduced by any applicable Bank of England scalar; the end-state 21.6%-of-RWA requirement "
         "took effect 1 January 2023, following an 18%-of-RWA interim requirement from 1 January 2020). No Pillar "
         "3/KM1-format numeric MREL resources or ratio was found for any year except FY2025, where the Annual "
         "Report directly states a combined 'total capital and MREL ratio of 23.6% of RWA' (£450m MREL-eligible "
         "debt plus £2,456m of capital resources). Other years' ratio cells are left blank rather than computed by "
         "us from the two rows above, since the Bank did not itself state a ratio for those years (a reader can "
         "derive an approximate figure from the two rows shown, but we have not presented it as a disclosed fact).",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -819277, "FY2024": 836309, "FY2023": 1215640, "FY2022": -351346, "FY2021": -670515}),
        ("Net cash from/(used in) investing activities", {"FY2025": -19811, "FY2024": -18114, "FY2023": -17972, "FY2022": -9170, "FY2021": -5725}),
        ("Net cash from/(used in) financing activities", {"FY2025": -496588, "FY2024": -637225, "FY2023": -277940, "FY2022": -12141, "FY2021": -13551}),
        ("Cash balance at end of year", {"FY2025": 7761527, "FY2024": 9097190, "FY2023": 8916214, "FY2022": 7996622, "FY2021": 8368955}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "17.5%", "FY2024": "18.0%", "FY2023": "20.0%", "FY2022": "21.3%", "FY2021": "20.2%"}),
        ("Tier 1 Ratio", {"FY2025": "17.5%", "FY2024": "18.0%", "FY2023": "20.0%", "FY2022": "21.3%", "FY2021": "20.2%"}),
        ("Total Capital Ratio", {"FY2025": "20.0%", "FY2024": "20.6%", "FY2023": "23.6%", "FY2022": "24.8%", "FY2021": "23.5%"}),
        ("Leverage Ratio", {"FY2025": "9.4%", "FY2024": "9.3%", "FY2023": "9.1%", "FY2022": "9.4%", "FY2021": "7.3%"}),
        ("LCR", {"FY2025": "180%", "FY2024": "165%", "FY2023": "153%", "FY2022": "147%"}),
        ("NSFR", {"FY2025": "130%", "FY2024": "136%", "FY2023": "131%", "FY2022": "130%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Handelsbanken plc is a young UK-incorporated entity "
         "(2018) - FY2021 pre-dates its Group/Bank consolidated-reporting split and its first formal Pillar 3/KM1 "
         "disclosure (first published for FY2022), so FY2021's leverage ratio uses a different, non-comparable "
         "methodology (see Leverage Ratio sheet) and has no LCR/NSFR figure at all.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HANDELSBANKEN FINANCIALS.xlsx")
