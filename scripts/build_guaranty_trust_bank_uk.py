import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/05969821/filing-history/MzQ2NTE3NTM2NmFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/05969821/filing-history/MzQwNjA2NDkyOGFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/05969821/filing-history/MzM3MzI3NjAyMmFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "Guaranty Trust Bank (UK) Limited (FRN 466611, Companies House 05969821) is a wholly-owned UK\n"
    "subsidiary of Guaranty Trust Bank Limited ('GTBank Nigeria'), itself wholly owned by Guaranty Trust\n"
    "Holding Company Plc (GTCO). Unlike several other Nigerian-bank-owned UK subsidiaries in this project\n"
    "(Zenith Bank UK, UBA UK, FCMB UK, FidBank UK), this entity reports in GBP throughout - no FX\n"
    "conversion is required. FY2025 accounts (year ended 31 Dec 2025) had not yet been filed with\n"
    "Companies House as of this build (last filing: FY2024, filed 6 May 2025); FY2025 is left blank.\n\n"
    "DATA QUALITY NOTE - cash-equivalents basis discontinuity: the FY2022 Annual Report states that\n"
    "'cash and cash equivalents for 2021 have been re-presented to include money market placements with\n"
    "maturity of less than 3 months', quantifying the impact as an increase in the FY2021 opening balance\n"
    "from GBP193,625,102 to GBP276,931,087 and in the FY2021 closing balance from GBP174,352,252 to\n"
    "GBP290,627,822. However, neither of those 'old-basis' figures matches FY2021's own originally-filed\n"
    "Annual Report, which itself shows an opening balance of GBP83,305,985 and a closing balance of\n"
    "GBP116,275,570 for FY2021 - a discrepancy in the source documents themselves that could not be\n"
    "traced or resolved. Per this project's convention, each year below uses its own originally-published\n"
    "figures (so FY2021's closing balance will not visually chain into FY2022's opening balance); this gap\n"
    "is flagged here rather than forced to reconcile, the same treatment as Arab Bank Europe's unexplained\n"
    "cash-bridge gap elsewhere in this project.\n\n"
    "Also note: FY2021's own 'Operating cash flows before movement in working capital' subtotal\n"
    "(GBP(10,764,152)) is GBP360 different from the sum of its own printed component lines - an immaterial\n"
    "source rounding artifact, not corrected."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Guaranty Trust Bank (UK) Limited's own Statement of Cash Flows, as originally\n"
    "published in each year's own Companies House-filed Annual Report and Financial Statements (not a later\n"
    "year's restated comparative, except where noted):\n"
    f"FY2024: Annual Report for the year ended 31 Dec 2024, p.26-27 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: as above (FY2024 Annual Report's own FY2023 comparative column, p.26-27) - {AR2024_URL}\n"
    f"FY2022: Annual Report for the year ended 31 Dec 2022, p.25 (Statement of cash flows) - {AR2022_URL}\n"
    f"FY2021: Annual Report for the year ended 31 Dec 2021, p.24 (Statement of cash flows) - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Guaranty Trust Bank (UK) Limited does not publish a standalone Pillar 3 disclosure document.\n"
        "Confirmed via a full enumeration of every URL in gtbankuk.com's own sitemap.xml (all 8 sitemap\n"
        "sections: about, businessBanking, helpCentre, homepage, investorRelationsIndex, mediaCentre,\n"
        "personalBanking, securityCentre, staticPages) - no Pillar 3, regulatory-disclosures, or capital-ratio\n"
        "page/document exists anywhere on the site. The Strategic Report each year states that Pillar 3/CRD IV\n"
        "disclosures are 'set out in the Directors' Report' and risk management policies 'in Note 23', but the\n"
        "only quantitative capital figure actually given anywhere in the statutory accounts is Note 23.8(a)\n"
        "'Regulatory capital (unaudited)', reproduced below. No CET1/Total Capital/Leverage ratio, RWA,\n"
        "Leverage Ratio, LCR, NSFR, or MREL figure of any kind is disclosed for any year.\n"
        f"FY2024/FY2023: Annual Report FY2024, Note 23.8(a) 'Regulatory capital (unaudited)', p.68 - {AR2024_URL}\n"
        f"FY2022/FY2021: Annual Report FY2022, Note 23.8(a) 'Regulatory capital (unaudited)', p.62 - {AR2022_URL}\n"
        "(FY2021's own figure is confirmed identical in both the FY2021 Annual Report's own Note 23.8(a), "
        f"p.58 - {AR2021_URL} - and the FY2022 Annual Report's FY2021 comparative column.)\n\n"
        "The Bank states it has no Additional Tier 1 capital, so Common Equity Tier 1 = Tier 1 = Total\n"
        "regulatory capital throughout; the same figure is used on all three sheets below."
    )


bw = BankWorkbook(bank_name="Guaranty Trust Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="00B721")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(Loss) for the period before taxation", {
        "FY2024": 11480721, "FY2023": 13958934, "FY2022": 5121885, "FY2021": -9732637,
    }),
    ("DATA", "Amortisation of investment securities", {
        "FY2022": -1476950, "FY2021": -1408658,
    }),
    ("DATA", "Interest income from investment securities", {
        "FY2024": -7475529, "FY2023": -7178103,
    }),
    ("DATA", "Depreciation", {
        "FY2024": 592042, "FY2023": 517052, "FY2022": 379244, "FY2021": 570173,
    }),
    ("DATA", "Net (increase)/decrease in fair value of securities", {
        "FY2021": -1192264,
    }),
    ("DATA", "Expected credit losses / allowances for credit impairment charge/(reversal)", {
        "FY2024": 74019, "FY2023": -12663, "FY2022": 120728,
    }),
    ("DATA", "Effective interest rate adjustment", {
        "FY2024": -166166, "FY2023": -271506, "FY2022": -126000,
    }),
    ("DATA", "Lease finance charge", {
        "FY2024": 410509, "FY2023": 415986, "FY2022": 209082,
    }),
    ("DATA", "Provision for lease dilapidation", {
        "FY2024": 11240, "FY2023": 10833,
    }),
    ("DATA", "Depreciation of leasehold right of use asset", {
        "FY2024": 778533, "FY2023": 1042960, "FY2022": 1797381, "FY2021": 999594,
    }),
    ("TOTAL", "Operating cash flows before movement in working capital", {
        "FY2024": 5705369, "FY2023": 8483493, "FY2022": 6025370, "FY2021": -10764152,
    }),
    ("DATA", "(Increase)/decrease in loans and advances to banks", {
        "FY2024": -44371958, "FY2023": 54491422, "FY2022": -6313430, "FY2021": 29961133,
    }),
    ("DATA", "(Increase)/decrease in loans and advances to customers", {
        "FY2024": -4695033, "FY2023": 4426364, "FY2022": -4402308, "FY2021": -6639736,
    }),
    ("DATA", "Increase/(decrease) in other assets", {
        "FY2024": -126192, "FY2023": -149057, "FY2022": 606644, "FY2021": 52687,
    }),
    ("DATA", "Increase/(decrease) in deposits by banks", {
        "FY2024": 112584567, "FY2023": -127254322, "FY2022": 53231890, "FY2021": 23544174,
    }),
    ("DATA", "Increase/(decrease) in deposits by customers", {
        "FY2024": -5344634, "FY2023": -35392588, "FY2022": 68307416, "FY2021": 9653264,
    }),
    ("DATA", "Increase/(decrease) in other liabilities", {
        "FY2024": -1147659, "FY2023": -6957695, "FY2022": 491009, "FY2021": 6491319,
    }),
    ("TOTAL", "Changes in working capital (cumulative, incl. operating cash flows above)", {
        "FY2024": 62604460, "FY2023": -102352383, "FY2022": 117946591, "FY2021": 52298689,
    }),
    ("DATA", "Interest paid on leases", {
        "FY2022": -209082,
    }),
    ("DATA", "Corporation tax (paid)/received", {
        "FY2024": -4669205, "FY2023": 25181, "FY2021": 0,
    }),
    ("TOTAL", "Net cash flow from/(used in) operating activities", {
        "FY2024": 57935255, "FY2023": -102327202, "FY2022": 117737509, "FY2021": 52298689,
    }),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisition of investment securities", {
        "FY2024": -309552620, "FY2023": -322726031, "FY2022": -243814896, "FY2021": -160562399,
    }),
    ("DATA", "Sale and maturity of investment securities", {
        "FY2024": 315933183, "FY2023": 280019392, "FY2022": 219731160, "FY2021": 142726224,
    }),
    ("DATA", "Interest received from investment securities", {
        "FY2024": 6597200, "FY2023": 5617158,
    }),
    ("DATA", "Acquisition of property and equipment", {
        "FY2024": -1140481, "FY2023": -1422698, "FY2022": -1980378, "FY2021": -81236,
    }),
    ("TOTAL", "Net cash flow from/(used in) investing activities", {
        "FY2024": 11837282, "FY2023": -38512179, "FY2022": -26064114, "FY2021": -17917411,
    }),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of lease", {
        "FY2024": -705754, "FY2023": -570000,
    }),
    ("DATA", "Increase/(decrease) in lease liabilities", {
        "FY2022": -1892429, "FY2021": -1411693,
    }),
    ("TOTAL", "Net cash flow from/(used in) financing activities", {
        "FY2024": -705754, "FY2023": -570000, "FY2022": -1892429, "FY2021": -1411693,
    }),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {
        "FY2024": 69066783, "FY2023": -141409381, "FY2022": 89780966, "FY2021": 32969585,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2024": 238999407, "FY2023": 380408788, "FY2022": 290627822, "FY2021": 83305985,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2024": 308066190, "FY2023": 238999407, "FY2022": 380408788, "FY2021": 116275570,
    }),
]

bw.add_cash_flow_sheet(
    title="Guaranty Trust Bank (UK) Limited — Statement of Cash Flows",
    subtitle="As originally published in each year's own Annual Report (see DATA QUALITY note on a "
              "FY2021/FY2022 cash-equivalents basis discontinuity in the source citation below)",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=230,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=48, source_height=170)


REG_CAPITAL = {"FY2024": 48075379, "FY2023": 39390993, "FY2022": 28344378, "FY2021": 25089641}

metric(
    "CET1 Capital", "£",
    [("Common Equity Tier 1 (CET1) capital", REG_CAPITAL)],
    p3_sources(),
)
bw.add_not_disclosed_metric_sheets(["CET1 Ratio"], p3_sources())
metric(
    "Tier 1 Capital", "£",
    [("Tier 1 capital", REG_CAPITAL)],
    p3_sources(),
    note="The Bank has no Additional Tier 1 capital, so Tier 1 capital equals CET1 capital.",
)
bw.add_not_disclosed_metric_sheets(["Tier 1 Ratio"], p3_sources())
metric(
    "Total Capital", "£",
    [("Total regulatory capital (unaudited)", REG_CAPITAL)],
    p3_sources(),
    note="The Bank has no Tier 2 capital, so Total Capital equals Tier 1 capital equals CET1 capital.",
)

bw.add_not_disclosed_metric_sheets([
    "Total Capital Ratio", "Total RWAs",
    "Leverage Ratio", "LCR", "NSFR", "MREL Ratio",
], p3_sources())

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash flow from/(used in) operating activities", {
            "FY2024": 57935255, "FY2023": -102327202, "FY2022": 117737509, "FY2021": 52298689,
        }),
        ("Net cash flow from/(used in) investing activities", {
            "FY2024": 11837282, "FY2023": -38512179, "FY2022": -26064114, "FY2021": -17917411,
        }),
        ("Net cash flow from/(used in) financing activities", {
            "FY2024": -705754, "FY2023": -570000, "FY2022": -1892429, "FY2021": -1411693,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2024": 308066190, "FY2023": 238999407, "FY2022": 380408788, "FY2021": 116275570,
        }),
    ],
    cash_flow_unit="£",
    ratios=[],
    note="No Pillar 3 ratios (CET1/Tier 1/Total Capital/Leverage/LCR/NSFR/MREL) are disclosed for this "
         "entity at all - only a single £ regulatory-capital figure (see the CET1/Tier 1/Total Capital "
         "sheets). Figures above are duplicated from the Cash Flow Statement sheet for at-a-glance trend "
         "viewing; see that sheet's own source citation, including a flagged FY2021/FY2022 basis "
         "discontinuity in the cash-equivalents figures.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/GUARANTY TRUST BANK UK FINANCIALS.xlsx")
