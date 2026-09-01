import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {
    "FY2025": "FY2025",
    "FY2024": "FY2024*",
    "FY2023": "FY2023",
    "FY2022": "FY2022",
    "FY2021": "FY2021†",
}

AR25_URL = "https://chetwoodbank.co.uk/documents/chetwood-bank-annual-report.pdf"
AR24_URL = "http://web.archive.org/web/20240920030034/https://chetwood.co/static/97d26e488d5277699e5b9a9983db4d5b/AnnualReport.pdf"
AR22_URL = "http://web.archive.org/web/20230131231341/https://chetwood.co/static/7fbc3d1ed9c0913dca3435f640a5a570/AnnualReport.pdf"
AR21_URL = "http://web.archive.org/web/20210830132929/https://chetwood.co/static/3d0ade6e892213e246ca03dc1d84b417/AnnualReport.pdf"

P3_25_URL = "https://chetwoodbank.co.uk/documents/chetwood-bank-pillar-three-disclosures.pdf"
P3_23_URL = "http://web.archive.org/web/20240315022245/https://chetwood.co/static/330c40d433df90b83d3b3e5c673e21cc/Pillar3Disclosures.pdf"
P3_22_URL = "http://web.archive.org/web/20230131235943/https://chetwood.co/static/815e2dd174c4655ddf55a93ca1029ce3/Pillar3Disclosures.pdf"
P3_21_URL = "http://web.archive.org/web/20211128171331/https://chetwood.co/static/221a3946677e4d8c49c5525d22f9b534/Pillar3Disclosures.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Chetwood Financial Limited (trading as Chetwood Bank) is the entity on the PRA register - no "
    "holding-company substitution was needed here (unlike Monzo). All years are Chetwood Financial Limited, "
    "consolidated/Group basis, EXCEPT FY2021 (marked †), which is Chetwood's own standalone entity accounts - "
    "the Group didn't exist yet (Chetwood acquired Yobota Limited on 1 March 2022, and CHL Mortgages for "
    "Intermediaries Limited later still), so there is no consolidated cash flow statement for FY2021. Companies "
    "House confirms FY2021 accounts were filed as 'Full accounts' (solo), while FY2022-FY2025 were filed as "
    "'Group of companies' accounts' (consolidated). Per user direction, FY2021 is included on a standalone basis "
    "and clearly flagged, rather than omitted.\n"
    "FY2024 (marked *) is consolidated, but no Pillar 3 disclosure for 'as at 31 March 2024' was ever published or "
    "archived - see the note on each Pillar 3 sheet."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Chetwood Financial Limited Group (consolidated) cash flow statement, £'000, unless "
    "noted. See entity note above re: FY2021 (standalone) and FY2024 (Pillar 3 gap).\n"
    f"FY2025: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2025, "
    f"p.48-49 (Consolidated and company statement of cashflows) - {AR25_URL}\n"
    f"FY2024: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2024, "
    f"p.29 (Consolidated and Company Statement of Cashflows) - {AR24_URL}\n"
    f"FY2023: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2024, "
    f"p.29 (prior-year comparative column) - {AR24_URL}. (The FY2023 Annual Report's own PDF has a text-encoding "
    f"fault that corrupts extracted figures; the FY2024 report's clean comparative column was used instead - "
    f"both present the same audited FY2023 statutory figures.)\n"
    f"FY2022: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2022, "
    f"p.26 (Consolidated and Company Statement of Cashflows) - {AR22_URL}\n"
    f"FY2021: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2021, "
    f"p.28 (Statement of Cashflows, standalone entity) - {AR21_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: Line items changed across the five years as the business grew (e.g. debt securities and "
    "derivative-related lines were introduced/split differently year to year, and FY2025 switched the starting "
    "line from 'Loss after tax' to '(Loss)/profit before tax'). Blank cells indicate that year's report did not "
    "disclose that specific split. Section totals (net cash from operating/investing/financing, cash and cash "
    "equivalents) are consistent and reconcile exactly across all 5 years.\n\n"
    "DATA QUALITY NOTE (added 2026-08-27, found during a project-wide sanity check): the AR24/AR25 source "
    "statements print BOTH a Group and a Company column side by side for each year; three line items were "
    "originally transcribed from the wrong column or with a digit error, causing FY2023/FY2024's operating and "
    "investing TOTALs to not reconcile to their own line items. Corrected against both AR24 (own-year figures) "
    "and AR25's FY2024 comparative column (cross-checked, both agree): 'Fair value adjustment on hedged items' "
    "FY2024 corrected from -11,182 to the Group figure -11,782 (a transcription slip); 'Interest received from "
    "investing activities' FY2024 corrected from 11,601 to the Group figure 17,601 (transcription slip); 'Loss on "
    "disposal of property, plant and equipment' FY2023 corrected from 4 to the Group figure 8 (was the Company "
    "figure); 'Impairment of investment in subsidiary/Yobota' FY2023 corrected from 6,753 to 0/nil (the Group "
    "figure is nil - 6,753 was the Company-only figure); 'Subscription of shares in subsidiary undertaking' "
    "FY2023 (-1,500) removed entirely - it is a Company-only line with no Group-basis equivalent, so it never "
    "belonged in this Group-basis statement. All four sections now reconcile exactly to the penny against the "
    "primary source."
)

def p3_sources(extra_note=""):
    return (
        "Sources (see entity note on Cash Flow Statement sheet):\n"
        f"FY2025: Chetwood Bank Pillar 3 Disclosures, September 2025 (as at 31 March 2025), Section 5 (Key Metrics "
        f"- KM1) - {P3_25_URL}\n"
        f"FY2024: No Pillar 3 disclosure 'as at 31 March 2024' was found - not published on Chetwood's live site "
        f"(which hosts only the current edition at a non-dated URL) and no snapshot was captured by the Internet "
        f"Archive Wayback Machine between the FY2023 edition (published Jan 2024) and the FY2025 edition "
        f"(published Sept 2025). Left blank.\n"
        f"FY2023: Chetwood Financial Ltd Pillar 3 Disclosure, as at 31 March 2023, Section 6 (Key Metrics - KM1) "
        f"and Section 7.1 (Capital Resources) - {P3_23_URL}\n"
        f"FY2022: Chetwood Financial Ltd Pillar 3 Disclosure, as at 31 March 2022, Annex B (Key Metrics - KM1) "
        f"- {P3_22_URL}\n"
        f"FY2021: Chetwood Financial Ltd Pillar 3 Disclosure, as at 31 March 2021, Section 1.2 (Summary Analysis) "
        f"and Section 4 (Capital Resources) - {P3_21_URL} (pre-dates the formal KM1 template; Chetwood adopted the "
        f"CRR KM1 annex from the FY2022 report onward)" + (f"\n{extra_note}" if extra_note else "")
    )

bw = BankWorkbook(bank_name="Chetwood Financial Limited", years=YEARS, year_label=YEAR_LABEL, header_color="003232")

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Loss after tax", {"FY2024": -8861, "FY2023": -58148, "FY2022": -29753, "FY2021": -21310}),
    ("DATA", "(Loss)/profit before tax", {"FY2025": -4702}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": 615, "FY2024": 560, "FY2023": 496, "FY2022": 322, "FY2021": 347}),
    ("DATA", "Remeasurement of right-of-use asset", {"FY2023": -217, "FY2022": 304}),
    ("DATA", "Amortisation of intangibles", {"FY2025": 536, "FY2024": 1261, "FY2023": 2235, "FY2022": 694, "FY2021": 106}),
    ("DATA", "Impairment of intangibles", {"FY2024": 985, "FY2023": 3069}),
    ("DATA", "Interest income on debt securities", {"FY2025": -50560, "FY2024": -18163, "FY2023": -1885}),
    ("DATA", "Interest expense/(income) on financing activities", {"FY2025": 6800, "FY2024": 180, "FY2023": 36, "FY2022": 35, "FY2021": 40}),
    ("DATA", "Equity-settled share-based payment transactions", {"FY2025": 144, "FY2024": 284, "FY2023": 85, "FY2022": 209, "FY2021": 102}),
    ("DATA", "Movement in fair value of financial instruments at FVTPL", {"FY2025": -22983, "FY2024": 9208, "FY2023": 1399}),
    ("DATA", "Movement in fair value of derivative financial assets", {"FY2022": -119, "FY2021": -15}),
    ("DATA", "Movement in fair value of derivative financial liabilities", {"FY2022": 452, "FY2021": -4}),
    ("DATA", "Fair value adjustment on hedged items", {"FY2025": 9005, "FY2024": -11782, "FY2023": -2217}),
    ("DATA", "Loss on disposal of property, plant and equipment", {"FY2025": 1, "FY2023": 8, "FY2022": 1, "FY2021": 12}),
    ("DATA", "Profit on sale of investments in debt securities", {"FY2025": -1, "FY2024": -42}),
    ("DATA", "Discount unwind on debt securities", {"FY2025": 536}),
    ("DATA", "Loss on disposal of intangible assets", {"FY2022": 18, "FY2021": 402}),
    ("DATA", "Movement in provision", {"FY2025": -657, "FY2024": 894, "FY2023": 1424, "FY2022": 591}),
    ("DATA", "Impairment of investment in subsidiary / impairment of Yobota", {"FY2024": 0, "FY2023": 0}),
    ("DATA", "Net gain arising from derecognition of financial assets measured at amortised cost", {"FY2022": -4369}),
    ("DATA", "Net increase in loans and advances to customers", {"FY2025": -857836, "FY2024": -1184232, "FY2023": -346633, "FY2022": -146297, "FY2021": -19344}),
    ("DATA", "Net interest paid on derivative financial assets", {"FY2025": 25551, "FY2024": 1448, "FY2023": 37}),
    ("DATA", "Net cash flow on derivative financial instruments", {"FY2024": -52498, "FY2023": 325}),
    ("DATA", "Increase/(decrease) in prepayments and accrued income", {"FY2025": 324, "FY2024": -3353, "FY2023": -69, "FY2022": -175, "FY2021": 223}),
    ("DATA", "Increase in other assets", {"FY2025": -20076, "FY2024": -25013, "FY2023": -10277, "FY2022": -4696, "FY2021": -2881}),
    ("DATA", "(Increase)/decrease in tax asset", {"FY2023": 64, "FY2022": -19, "FY2021": -45}),
    ("DATA", "Increase/(decrease) in customer deposits", {"FY2025": 955692, "FY2024": 1473432, "FY2023": 1060680, "FY2022": 162610, "FY2021": -52195}),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {"FY2025": 507, "FY2024": 2487, "FY2023": 489, "FY2022": 1612, "FY2021": 2838}),
    ("DATA", "Increase/(decrease) in other liabilities", {"FY2025": 142, "FY2024": 2725, "FY2023": 2518, "FY2022": 1447, "FY2021": -396}),
    ("DATA", "Purchase of mortgage portfolio", {"FY2022": 157842}),
    ("DATA", "Derecognition of assets at amortised cost on sale", {"FY2022": -123733}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": 43038, "FY2024": 189520, "FY2023": 653419, "FY2022": 16976, "FY2021": -92120}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Proceeds from sale and maturity of debt securities", {"FY2025": 1401, "FY2024": 36835, "FY2023": 11031}),
    ("DATA", "Acquisition of debt securities", {"FY2025": -910238, "FY2024": -505077, "FY2023": -135674, "FY2022": -5003}),
    ("DATA", "Principal repayments on investments in debt securities", {"FY2025": 134509, "FY2024": 61327}),
    ("DATA", "Interest received from investing activities", {"FY2025": 40802, "FY2024": 17601, "FY2023": 1760}),
    ("DATA", "Net maturity/(purchase) of debt securities", {"FY2021": 30170}),
    ("DATA", "Purchase of loans and advances to customers", {"FY2022": -157842}),
    ("DATA", "Purchases of property, plant and equipment", {"FY2025": -617, "FY2024": -461, "FY2023": -843, "FY2022": -119, "FY2021": -116}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 11}),
    ("DATA", "Investment in Intangible assets", {"FY2025": -9, "FY2023": -402, "FY2022": -1852, "FY2021": -3201}),
    ("DATA", "Acquisition of subsidiary net of cash acquired", {"FY2025": -7497, "FY2022": -12903}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -741638, "FY2024": -389775, "FY2023": -124128, "FY2022": -177719, "FY2021": 26853}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Principal drawdowns on amounts owed to credit institutions", {"FY2025": 476000, "FY2024": 9000}),
    ("DATA", "Interest paid on amounts owed to credit institutions", {"FY2025": -2930}),
    ("DATA", "Issuance of ordinary shares", {"FY2025": 27001, "FY2024": 89000, "FY2023": 84609, "FY2022": 55000, "FY2021": 29000}),
    ("DATA", "Issuance of debt securities", {"FY2024": 100}),
    ("DATA", "Repayment of debt securities", {"FY2025": -10}),
    ("DATA", "Interest (paid)/received on debt securities", {"FY2025": -6}),
    ("DATA", "Interest expense on debt securities", {"FY2024": 0}),
    ("DATA", "Proceeds from the sale of loans and advances at amortised cost", {"FY2022": 128103}),
    ("DATA", "Interest paid on lease liabilities", {"FY2025": -39, "FY2024": -73, "FY2023": -36, "FY2022": -35, "FY2021": -40}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": 500016, "FY2024": 98027, "FY2023": 84573, "FY2022": 183068, "FY2021": 28960}),
    ("TOTAL", "Net cash flows for the period", {"FY2025": -198584, "FY2024": -102228, "FY2023": 613864, "FY2022": 22325, "FY2021": -36307}),
    ("DATA", "Opening cash and cash equivalents", {"FY2025": 586134, "FY2024": 688362, "FY2023": 74498, "FY2022": 52173, "FY2021": 88480}),
    ("TOTAL", "Closing cash and cash equivalents", {"FY2025": 387550, "FY2024": 586134, "FY2023": 688362, "FY2022": 74498, "FY2021": 52173}),
]

bw.add_cash_flow_sheet(
    title="Chetwood Financial Limited — Cash Flow Statement",
    subtitle="£'000 unless stated. Consolidated (Group) basis except FY2021 († standalone entity). See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=66,
    source_height=150,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=46, source_height=150)

FY2024_GAP_NOTE = "FY2024 is blank - no Pillar 3 disclosure 'as at 31 March 2024' was published/archived. See source note."

metric(
    "CET1 Capital", "£'000, Group/consolidated basis (FY2021: standalone entity)",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 187605, "FY2023": 91268, "FY2022": 57554, "FY2021": 50637})],
    p3_sources(),
    note=FY2024_GAP_NOTE,
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "15.2%", "FY2023": "26.6%", "FY2022": "29.3%", "FY2021": "28%"})],
    p3_sources(),
    note=FY2024_GAP_NOTE + " FY2021 is as stated in the source (rounded to the nearest whole percent; no decimal figure was disclosed that year).",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 187605, "FY2023": 91268, "FY2022": 57554, "FY2021": 50637})],
    p3_sources(),
    note=FY2024_GAP_NOTE + " Equal to CET1 capital in every year shown - Chetwood has no Additional Tier 1 (AT1) instruments.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "15.2%", "FY2023": "26.6%", "FY2022": "29.3%", "FY2021": "28%"})],
    p3_sources(),
    note=FY2024_GAP_NOTE,
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 187605, "FY2023": 91268, "FY2022": 57554, "FY2021": 50637})],
    p3_sources(),
    note=FY2024_GAP_NOTE + " Equal to CET1/Tier 1 capital in every year shown - Chetwood has no Tier 2 capital either.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "15.2%", "FY2023": "26.6%", "FY2022": "29.3%", "FY2021": "28%"})],
    p3_sources(),
    note=FY2024_GAP_NOTE,
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": 1233321, "FY2023": 343668, "FY2022": 196750, "FY2021": 178987})],
    p3_sources(),
    note=FY2024_GAP_NOTE,
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Leverage ratio total exposure measure", {"FY2025": 3615720, "FY2023": 1519817, "FY2022": 394658, "FY2021": 216375}),
        ("Leverage ratio (%)", {"FY2025": "5.19%", "FY2023": "6.01%", "FY2022": "14.58%", "FY2021": "23.4%"}),
    ],
    p3_sources(),
    note=FY2024_GAP_NOTE + " Unlike Barclays/Monzo, Chetwood's disclosures do not distinguish an 'excluding/including "
         "claims on central banks' basis in any year - a single leverage ratio definition is used throughout "
         "(Tier 1 capital / total exposure measure). FY2021 used a pre-KM1 narrative table; FY2022 onward uses the "
         "formal KM1 rows 13-14.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA) (weighted value - average)", {"FY2025": 897493, "FY2023": 302266, "FY2022": 67841}),
        ("Cash outflows - total weighted value", {"FY2025": 489794, "FY2023": 52035, "FY2022": 5627}),
        ("Cash inflows - total weighted value", {"FY2025": 28009, "FY2023": 15169, "FY2022": 13656}),
        ("Total net cash outflows (adjusted value)", {"FY2025": 461785, "FY2023": 36865, "FY2022": 1407}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "194%", "FY2023": "1,015%", "FY2022": "4,823%", "FY2021": "51,086%"}),
    ],
    p3_sources(),
    note=FY2024_GAP_NOTE + " FY2021 disclosed only the headline ratio in narrative form (no HQLA/outflow £ breakdown "
         "was published that year - the formal KM1 liquidity rows were introduced from FY2022). Chetwood's LCR "
         "ratios are extremely high because, as a young/small deposit-taker at the time, its regulatory outflow "
         "assumptions were small relative to its liquid asset holdings - this is as disclosed by Chetwood, not a "
         "transcription error.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 3677559, "FY2023": 1387511, "FY2022": 380549}),
        ("Total required stable funding", {"FY2025": 2536343, "FY2023": 572002, "FY2022": 233566}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "145%", "FY2023": "243%", "FY2022": "162.9%", "FY2021": "146.5%"})
    ],
    p3_sources(),
    note=FY2024_GAP_NOTE + " FY2021's NSFR figure (146.5%) is quoted exactly as printed in the FY2021 Pillar 3 "
         "report, which oddly labels it 'as at the 31 March 2020' in a document otherwise dated 'as at 31 March "
         "2021' - this looks like a typo in Chetwood's own document, but it is reproduced verbatim rather than "
         "silently corrected; no £ breakdown was published for FY2021 (the formal KM1 NSFR rows were introduced "
         "from FY2022).",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not applicable" for y in YEARS})],
    p3_sources(),
    note="Chetwood is classified as a 'small and non-complex institution' (SNCI) and is not subject to any MREL "
         "requirement above its minimum capital requirement - stated explicitly in the FY2021, FY2022 and FY2023 "
         "Pillar 3 reports ('...has no minimum requirements for Own funds and Eligible Liabilities (MREL) above "
         "its [minimum capital requirement]'). The FY2025 report uses a shorter reduced-disclosure format that "
         "omits this narrative section, but there is no indication Chetwood's MREL/SNCI status has changed.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": 43038, "FY2024": 189520, "FY2023": 653419, "FY2022": 16976, "FY2021": -92120}),
        ("Net cash from/(used in) investing activities", {"FY2025": -741638, "FY2024": -389775, "FY2023": -124128, "FY2022": -177719, "FY2021": 26853}),
        ("Net cash from/(used in) financing activities", {"FY2025": 500016, "FY2024": 98027, "FY2023": 84573, "FY2022": 183068, "FY2021": 28960}),
        ("Closing cash and cash equivalents", {"FY2025": 387550, "FY2024": 586134, "FY2023": 688362, "FY2022": 74498, "FY2021": 52173}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.2%", "FY2023": "26.6%", "FY2022": "29.3%", "FY2021": "28%"}),
        ("Tier 1 Ratio", {"FY2025": "15.2%", "FY2023": "26.6%", "FY2022": "29.3%", "FY2021": "28%"}),
        ("Total Capital Ratio", {"FY2025": "15.2%", "FY2023": "26.6%", "FY2022": "29.3%", "FY2021": "28%"}),
        ("Leverage Ratio", {"FY2025": "5.19%", "FY2023": "6.01%", "FY2022": "14.58%", "FY2021": "23.4%"}),
        ("LCR", {"FY2025": "194%", "FY2023": "1,015%", "FY2022": "4,823%", "FY2021": "51,086%"}),
        ("NSFR", {"FY2025": "145%", "FY2023": "243%", "FY2022": "162.9%", "FY2021": "146.5%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. " + FY2024_GAP_NOTE,
)

bw.save("/Users/armaan/code/katalysis/banks/CHETWOOD FINANCIALS.xlsx")
