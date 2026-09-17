import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = ("https://find-and-update.company-information.service.gov.uk/company/01074897/"
              "filing-history/MzUzNzM1MjkyOGFkaXF6a2N4/document?format=pdf&download=0")
AR2024_URL = ("https://find-and-update.company-information.service.gov.uk/company/01074897/"
              "filing-history/MzQ4Mzc3NzE0NWFkaXF6a2N4/document?format=pdf&download=0")
AR2023_URL = ("https://find-and-update.company-information.service.gov.uk/company/01074897/"
              "filing-history/MzQ0MDMxMDc4MGFkaXF6a2N4/document?format=pdf&download=0")
AR2022_URL = ("https://find-and-update.company-information.service.gov.uk/company/01074897/"
              "filing-history/MzQyNDMxMDM1M2FkaXF6a2N4/document?format=pdf&download=0")
AR2021_URL = ("https://find-and-update.company-information.service.gov.uk/company/01074897/"
              "filing-history/MzM2MTYzNTYxM2FkaXF6a2N4/document?format=pdf&download=0")

ENTITY_NOTE = (
    "Havin Bank Limited (Companies House 01074897, formerly Havana International Bank Limited) "
    "is a UK-incorporated bank whose majority and ultimate controlling shareholder is Banco "
    "Central de Cuba (95.6%), with Banco Popular de Ahorro and Banco de Credito y Comercio "
    "(2.2% each) also Cuban state banks. All 5 Companies House filings used are scanned/"
    "image-only (0 extractable text) - transcribed via page-image rendering. PRESENTATION "
    "NOTE: cash and cash equivalents were redefined starting with the FY2022 Annual Report to "
    "include loans and advances to banks with a maturity up to 3 months (previously excluded); "
    "FY2022's own report states this restates FY2021's closing balance from GBP43,634,527 to "
    "GBP98,668,182 for comparability, but each year here is shown on its own originally-"
    "published basis per this project's convention, so FY2021's closing balance does NOT tie "
    "to FY2022's opening balance - this is a genuine, documented source-driven discontinuity, "
    "not a transcription error. A second presentational point: 'Interest paid' sits under "
    "Financing activities in every year's own original presentation (FY2021-FY2024); the "
    "FY2025 Annual Report reclassified it into the Operating activities note for FY2025 only "
    "(explicitly stated to have no impact on net cash movement), so FY2025's own Financing "
    "section only shows Dividends paid. FY2021's own Statement of Cash Flows title differs "
    "slightly across years but is the Bank's own primary statement throughout. FY2025's own "
    "Note 25 discloses two 2026 US Executive Orders (14380, 14404) expanding sanctions "
    "pressure on Cuba, flagged as a post balance sheet event potentially affecting the Bank's "
    "future business - not reflected in these historical figures."
)

CASH_FLOW_SOURCES = (
    "Sources - Havin Bank Limited's own Statement of Cash Flows (face of statement, each "
    "year's own primary presentation, not a later restated comparative) from its Companies "
    "House-filed Annual Report and Financial Statements:\n"
    f"FY2025: Annual Report FY2025, p.22 - {AR2025_URL}\n"
    f"FY2024: Annual Report FY2024, p.21 - {AR2024_URL}\n"
    f"FY2023: Annual Report FY2024, p.21 (FY2023 comparative column; FY2023's own report was "
    f"not independently re-verified for this line since the FY2024 comparative is consistent "
    f"with the FY2022 report's own FY2022 closing balance) - {AR2024_URL}\n"
    f"FY2022: Annual Report FY2022, p.27 - {AR2022_URL}\n"
    f"FY2021: Annual Report FY2021, p.21 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Havin Bank Limited's own statutory accounts. Confirmed non-disclosure "
        "(two independent search attempts): the Bank's own Directors' report states verbatim "
        "under 'Pillar 3 disclosures' and 'Country by country disclosures': \"Full disclosures "
        "are available on request\" (Annual Report FY2024, p.2, and consistent in other years) "
        "- i.e. for the years in this workbook the Bank supplies its Pillar 3 disclosure only "
        "privately on request. CORRECTION 2026-09-15: earlier editions of this note said the "
        "Bank \"does not publish a Pillar 3 document\" and that its site was JavaScript-rendered "
        "with the Wayback Machine unavailable. Both statements were too strong and are corrected "
        "below - the Bank DID publish Pillar 3 disclosures openly on its website for FY2010 "
        "through FY2019, and the site and archive are both readable. What is true is narrower: "
        "publication stopped after the FY2019 edition, so no Pillar 3 exists online for any year "
        "in this workbook's FY2021-FY2025 window:\n"
        f"FY2025/FY2024: Annual Report FY2025, Note 23 'Capital', p.43 - {AR2025_URL}\n"
        f"FY2023/FY2022: Annual Report FY2023, Note 23 'Capital', p.47 - {AR2023_URL}\n"
        f"FY2021: Annual Report FY2021, Note 22 'Capital', p.42-43 (this year's disclosure "
        f"gives only Total Tier One Capital - no Deductions from Capital/Total Regulatory "
        f"Capital breakdown was published for FY2021, a thinner format than later years) - "
        f"{AR2021_URL}\n\n"
        "No Risk Weighted Assets figure, and no CET1/Tier 1/Total Capital Ratio, Leverage "
        "Ratio, LCR, NSFR, or MREL figure is disclosed anywhere in the statutory accounts for "
        "any year (only an unaudited 'Capital surplus over regulatory minimum' % from FY2022 "
        "onward, which is a different metric to a standard CRR capital ratio and is not used "
        "here). CET1 = Tier 1 = Total Capital throughout, since no Additional Tier 1 or Tier 2 "
        "instruments are disclosed in any year.\n\n"
        "RE-VERIFIED 2026-09-12 (independent disclosure re-audit, full page-image OCR of the "
        "FY2024 and FY2025 filings - these are scanned documents with no text layer, so every "
        "check was done on rendered page images):\n"
        "- The \"Pillar 3 disclosures\" / \"Country by country disclosures\" headings in the "
        "Directors' report still read, verbatim and unchanged in the newest (FY2025) filing: "
        "\"Full disclosures are available on request.\"\n"
        "- Note 23 'Capital' in the FY2025 filing has the identical structure to prior years - "
        "Core tier one capital (Share Capital + Reserves), Total Tier One Capital, Deductions "
        "from Capital, Total Regulatory Capital, Overall Capital Requirement (Pillar 1 & Pillar "
        "2), Capital surplus, and Capital surplus over regulatory minimum. FY2025 figures: "
        "Total Tier One Capital 22,827,949; Total Regulatory Capital 22,532,098; Overall Capital "
        "Requirement 8,299,180; Capital surplus 14,232,918; surplus over regulatory minimum "
        "171.50%. Still NO RWA figure and NO CRR capital ratio of any kind.\n"
        "- NOT DERIVED ON PURPOSE: the 'Overall Capital Requirement' is explicitly a combined "
        "Pillar 1 AND Pillar 2 figure. This project derives RWA from a disclosed capital "
        "requirement x 12.5 for some other banks, but that conversion is only valid for a "
        "Pillar 1 requirement; applying it to a blended Pillar 1+2 number would overstate RWA "
        "by the Pillar 2 add-on. No RWA is therefore shown, rather than a derived figure.\n"
        "- LCR/NSFR: the FY2025 filing states only that \"the Bank complies with requirements "
        "in respect of Liquidity Coverage Ratio and Net Stable Funding Ratio laid down by the "
        "Prudential Regulation Authority\" - a compliance assertion with no percentage "
        "attached, in any year.\n\n"
        "RE-VERIFIED 2026-09-15 (third pass, full site enumeration rather than URL guessing). "
        "The Bank's website homepage at hib.uk.com is obfuscated - every page is a document."
        "write() of a URL-escaped string - which is what defeated the earlier attempts. Decoding "
        "that escaping exposes a plain document index at http://www.hib.uk.com/annrep.html, and "
        "that page is the Bank's own authoritative list of what it has ever published:\n"
        "- Pillar 3 disclosures listed: hibp3disc2010.pdf through hibp3disc2019.pdf, and NOTHING "
        "after 2019. An unfiltered Wayback CDX sweep of hib.uk.com returns exactly the same ten "
        "files and no more; sweeps of havanaintbank.co.uk and havinbank.com return zero (the "
        "latter is only an HTML frameset wrapping hib.uk.com, not a separate site).\n"
        "- The index page's own text reads: \"The Annual Report for 2024 is available. The Pillar "
        "3 Disclosure and Country by Country report are available upon request. The Pillar 3 "
        "Disclosure for 2019 is now available online via this website.\" That is the Bank stating "
        "directly that 2019 was the last edition it put online.\n"
        "- The FY2019 edition was retrieved and read in full to be certain it is this bank and "
        "not the similarly-abbreviated HBL Bank UK: it names Havin Bank and says \"As the Bank "
        "does not have any subsidiaries the disclosures are made on a solo basis.\" It is a "
        "BIPRU-basis document reporting FY2019/FY2018 only, so none of its figures fall in this "
        "workbook's FY2021-FY2025 window and none are used here.\n"
        "- The Bank's FY2024 Annual Report was also retrieved directly from its own site "
        "(http://www.hib.uk.com/hibacc2024.pdf, a native-text PDF rather than the scanned "
        "Companies House image filing) and independently confirms the Total Regulatory Capital "
        "figures used in this workbook: FY2024 23,791,445 and FY2023 23,105,954. Its Note 23 "
        "'Capital' again carries no RWA and no CRR ratio of any kind.\n\n"
        "USER-ACTIONABLE: for FY2021-FY2025 this bank's non-disclosure is a POLICY choice, not a "
        "dead link or a blocked website - the Bank states it will supply full Pillar 3 and "
        "country-by-country disclosures ON REQUEST. A direct written request to Havin Bank "
        "Limited is therefore the only realistic route to the RWA, capital-ratio, leverage, LCR "
        "and NSFR figures for this entity; the site has now been enumerated rather than guessed "
        "at, so further online searching is not expected to surface them."
    )


bw = BankWorkbook(bank_name="Havin Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="2858A5")

STATEMENTS_SOURCES = (
    "Sources - Havin Bank Limited's own Statement of Financial Position, Income Statement and "
    "Statement of Changes in Equity (face of each statement, each year's own primary presentation, "
    "not a later restated comparative) from its Companies House-filed Annual Report and Financial "
    "Statements:\n"
    f"FY2025: Annual Report FY2025, pp.19-21 - {AR2025_URL}\n"
    f"FY2024: Annual Report FY2024, pp.18-20 - {AR2024_URL}\n"
    f"FY2023: Annual Report FY2023, pp.22-24 - {AR2023_URL}\n"
    f"FY2022: Annual Report FY2022, pp.24-26 - {AR2022_URL}\n"
    f"FY2021: Annual Report FY2021, pp.18-20 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nEQUITY RECONCILIATION LADDER: built year-by-year, Balance Sheet first. Ties exactly at "
    "every boundary from FY2022 onward. One small documented source-driven rounding artifact at the "
    "FY2021 boundary: the Bank's own FY2021 Annual Report shows Shareholders' funds of GBP22,508,678 "
    "on the face of the Balance Sheet but GBP22,508,676 as the closing balance on the face of the "
    "Statement of Changes in Equity (a GBP2 internal inconsistency within the Bank's own single "
    "document, not introduced by this workbook); FY2022's own Annual Report then shows its opening "
    "balance as GBP22,508,677 (a further GBP1 from the equity statement's own figure). All three "
    "figures are reproduced exactly as each document states them, not force-reconciled to a single "
    "number. PRESENTATION NOTE: 'Receivables/debtors' only appears as its own Balance Sheet line "
    "FY2024/FY2025 - it is folded into 'Other assets' in FY2021-FY2023. The Profit & Loss statement's "
    "'Impairment losses and loans advances' line does not appear at all in FY2021's own presentation "
    "(no impairment note existed as a separate income statement line that year); FY2022 shows it "
    "explicitly as nil."
)

ASSET_QUALITY_SOURCES = (
    "Sources - Havin Bank Limited's own 'Loans and advances to customers' note (each year's own "
    "primary presentation) from its Companies House-filed Annual Report and Financial Statements:\n"
    f"FY2025/FY2024: Annual Report FY2025, Note 10, p.30 - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report FY2023, Note 10, p.34 - {AR2023_URL}\n"
    f"FY2021: Annual Report FY2021, Note 9, p.29 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nThe Bank applies FRS 102/IAS 39 incurred-loss impairment (individually-assessed, no "
    "collective provision, no IFRS 9 Stage 1/2/3 split disclosed in any year) - shown here by "
    "repayment-status band (impaired / past due / by maturity) rather than by IFRS 9 stage, matching "
    "the Bank's own disclosure basis throughout. 'Over five years' only appears as its own band in "
    "FY2025 - not disclosed as a separate band in any earlier year (folded into 'between one and 5 "
    "years' previously, per the Bank's own note wording). The disclosed 'impaired or past due loans' "
    "figure each year is not a single consistently-labelled line across all 5 years - FY2024/FY2025 "
    "call it 'non-performing loans' explicitly, FY2021-FY2023 the narrative text only ('the amount of "
    "impaired or past due loans to customers is...') - both variants are the same underlying disclosure "
    "and are shown here on one consistent 'Non-performing / impaired-or-past-due loans, as disclosed' row."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bw.add_balance_sheet_sheet(
    title="Havin Bank Limited — Statement of Financial Position",
    subtitle="As originally published in each year's own Annual Report (each year's own primary "
             "presentation, not a later restated comparative)",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances at central banks", {
            "FY2025": 35346327, "FY2024": 29954158, "FY2023": 38342174,
            "FY2022": 31789983, "FY2021": 25347880,
        }),
        ("DATA", "Loans and advances to banks and other financial institutions", {
            "FY2025": 61460562, "FY2024": 64606314, "FY2023": 71371023,
            "FY2022": 68737878, "FY2021": 83320302,
        }),
        ("DATA", "Loans and advances to customers", {
            "FY2025": 10391111, "FY2024": 12428931, "FY2023": 8992307,
            "FY2022": 18482200, "FY2021": 8634018,
        }),
        ("DATA", "Intangible assets", {
            "FY2025": 295851, "FY2024": 391887, "FY2023": 488076,
            "FY2022": 584296, "FY2021": 484067,
        }),
        ("DATA", "Tangible fixed assets", {
            "FY2025": 1555105, "FY2024": 1540079, "FY2023": 1577233,
            "FY2022": 1616026, "FY2021": 1656490,
        }),
        ("DATA", "Prepayments and accrued income", {
            "FY2025": 892060, "FY2024": 858809, "FY2023": 889996,
            "FY2022": 675544, "FY2021": 1004699,
        }),
        ("DATA", "Receivables/debtors", {
            "FY2025": 39945, "FY2024": 39905,
        }),
        ("DATA", "Other assets", {
            "FY2025": 354626, "FY2024": 249260, "FY2023": 296927,
            "FY2022": 496494, "FY2021": 591406,
        }),
        ("TOTAL", "Total Assets", {
            "FY2025": 110335587, "FY2024": 110109348, "FY2023": 121957736,
            "FY2022": 122383421, "FY2021": 121038862,
        }),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits by banks", {
            "FY2025": 83183992, "FY2024": 81344620, "FY2023": 91487208,
            "FY2022": 92659763, "FY2021": 90838505,
        }),
        ("DATA", "Customer accounts", {
            "FY2025": 2805620, "FY2024": 3305718, "FY2023": 5137804,
            "FY2022": 5737501, "FY2021": 6927373,
        }),
        ("DATA", "Due to parent undertaking", {
            "FY2025": 538675, "FY2024": 130304, "FY2023": 169587,
            "FY2022": 191756, "FY2021": 200058,
        }),
        ("DATA", "Accruals and other liabilities", {
            "FY2025": 769119, "FY2024": 863560, "FY2023": 1196153,
            "FY2022": 774301, "FY2021": 441394,
        }),
        ("DATA", "Deferred tax liability", {
            "FY2025": 79469, "FY2024": 87265, "FY2023": 88287,
            "FY2022": 131928, "FY2021": 122854,
        }),
        ("DATA", "Corporation tax liability", {
            "FY2025": 130763, "FY2024": 194549, "FY2023": 284667,
            "FY2022": 14517,
        }),
        ("TOTAL", "Total Liabilities", {
            "FY2025": 87507638, "FY2024": 85926016, "FY2023": 98363706,
            "FY2022": 99509766, "FY2021": 98530184,
        }),
        ("SECTION", "Equity", {}),
        ("DATA", "Called up share capital", {
            "FY2025": 22000000, "FY2024": 22000000, "FY2023": 22000000,
            "FY2022": 22000000, "FY2021": 22000000,
        }),
        ("DATA", "Profit and loss account", {
            "FY2025": 827949, "FY2024": 2183332, "FY2023": 1594030,
            "FY2022": 873655, "FY2021": 508678,
        }),
        ("TOTAL", "Total equity (Shareholders' funds)", {
            "FY2025": 22827949, "FY2024": 24183332, "FY2023": 23594030,
            "FY2022": 22873655, "FY2021": 22508678,
        }),
        ("TOTAL", "Total liabilities and equity", {
            "FY2025": 110335587, "FY2024": 110109348, "FY2023": 121957736,
            "FY2022": 122383421, "FY2021": 121038862,
        }),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=62,
    source_height=280,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
bw.add_income_statement_sheet(
    title="Havin Bank Limited — Income Statement",
    subtitle="As originally published in each year's own Annual Report (each year's own primary "
             "presentation, not a later restated comparative)",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest receivable and similar income", {
            "FY2025": 4654931, "FY2024": 5679555, "FY2023": 5336644,
            "FY2022": 2785468, "FY2021": 1612507,
        }),
        ("DATA", "Interest payable and similar expenses", {
            "FY2025": -1288150, "FY2024": -1710521, "FY2023": -1501108,
            "FY2022": -442855, "FY2021": -104074,
        }),
        ("TOTAL", "Net interest income", {
            "FY2025": 3366781, "FY2024": 3969034, "FY2023": 3835536,
            "FY2022": 2342613, "FY2021": 1508433,
        }),
        ("DATA", "Fees and commissions receivable", {
            "FY2025": 201787, "FY2024": 249690, "FY2023": 276851,
            "FY2022": 343373, "FY2021": 269558,
        }),
        ("DATA", "Fees and commissions payable", {
            "FY2025": -155818, "FY2024": -113049, "FY2023": -35548,
            "FY2022": -25951, "FY2021": -27007,
        }),
        ("DATA", "Foreign exchange profits", {
            "FY2025": 277248, "FY2024": 303470, "FY2023": 435780,
            "FY2022": 513709, "FY2021": 318954,
        }),
        ("DATA", "Other operating income", {
            "FY2025": 8516, "FY2024": 10492, "FY2023": 4756,
            "FY2022": 9512, "FY2021": 9512,
        }),
        ("TOTAL", "Total operating income", {
            "FY2025": 3698514, "FY2024": 4419637, "FY2023": 4517375,
            "FY2022": 3183256, "FY2021": 2079450,
        }),
        ("SECTION", "Expenses", {}),
        ("DATA", "Administrative expenses", {
            "FY2025": -3352586, "FY2024": -2684867, "FY2023": -3270406,
            "FY2022": -2576449, "FY2021": -2227306,
        }),
        ("DATA", "Impairment losses and loans advances", {
            "FY2025": 150716, "FY2024": -840614, "FY2023": -162886,
            "FY2022": 0,
        }),
        ("DATA", "Amortisation of intangible assets", {
            "FY2025": -96036, "FY2024": -96189, "FY2023": -96219,
            "FY2022": -84761, "FY2021": -83521,
        }),
        ("DATA", "Depreciation of tangible fixed assets", {
            "FY2025": -53656, "FY2024": -37153, "FY2023": -38793,
            "FY2022": -40464, "FY2021": -53141,
        }),
        ("TOTAL", "Operating profit/(loss)", {
            "FY2025": 346952, "FY2024": 760814, "FY2023": 949071,
            "FY2022": 481582, "FY2021": -284518,
        }),
        ("TOTAL", "Profit/(loss) before tax", {
            "FY2025": 346952, "FY2024": 760814, "FY2023": 949071,
            "FY2022": 481582, "FY2021": -284518,
        }),
        ("DATA", "Tax on profit", {
            "FY2025": -102335, "FY2024": -173696, "FY2023": -228696,
            "FY2022": -116604, "FY2021": 20154,
        }),
        ("TOTAL", "Profit/(loss) for the year and total comprehensive income/(loss)", {
            "FY2025": 244617, "FY2024": 587118, "FY2023": 720375,
            "FY2022": 364978, "FY2021": -264364,
        }),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=66,
    source_height=280,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
bw.add_equity_changes_sheet(
    title="Havin Bank Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest. Equity reconciliation ladder confirmed: "
             "each year's own closing balance ties exactly to the next year's own opening balance and "
             "to that year's own Balance Sheet Total equity from FY2022 onward - a small GBP1-2 "
             "documented rounding artifact within the Bank's own FY2021/FY2022 filings is reproduced "
             "as disclosed, not force-reconciled (see source note).",
    headers=["Called-up capital", "Profit and loss account", "Total equity"],
    rows=[
        ("DATA", "Balance as at 1 January 2021 (FY2021's own opening, = FY2020 closing)", (22000000, 773040, 22773040)),
        ("DATA", "Total comprehensive loss for the year", (None, -264364, -264364)),
        ("TOTAL", "Balance as at 31 December 2021 (per FY2021's own Equity Statement)", (22000000, 508676, 22508676)),
        ("DATA", "Total comprehensive profit for the year", (None, 364978, 364978)),
        ("TOTAL", "Balance as at 31 December 2022 (per FY2022's own Annual Report; FY2022's own opening was GBP22,508,677, a GBP1 difference from the row above - reproduced as disclosed)", (22000000, 873655, 22873655)),
        ("DATA", "Total comprehensive profit for the year", (None, 720375, 720375)),
        ("TOTAL", "Balance as at 31 December 2023", (22000000, 1594030, 23594030)),
        ("DATA", "Total comprehensive profit for the year", (None, 587118, 587118)),
        ("DATA", "Prior year adjustment", (None, 2184, 2184)),
        ("TOTAL", "Balance as at 31 December 2024", (22000000, 2183332, 24183332)),
        ("DATA", "Total comprehensive profit for the year", (None, 244617, 244617)),
        ("DATA", "Dividends in respect of prior years", (None, -1600000, -1600000)),
        ("TOTAL", "Balance as at 31 December 2025", (22000000, 827949, 22827949)),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Cash (outflows)/inflows from operating activities", {
        "FY2025": 3521073, "FY2024": 1528221, "FY2023": -3161495,
        "FY2022": 1121795, "FY2021": -13679377,
    }),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2025": 3521073, "FY2024": 1528221, "FY2023": -3161495,
        "FY2022": 1121795, "FY2021": -13679377,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Interest received", {"FY2021": 1590087}),
    ("DATA", "Payments to acquire intangible assets", {"FY2022": -184990, "FY2023": 0}),
    ("DATA", "Payments to acquire tangible fixed assets", {"FY2025": -68081, "FY2021": -2152}),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": -68081, "FY2023": 0, "FY2022": -184990, "FY2021": 1587935,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Interest paid", {
        "FY2024": -1680946, "FY2023": -1518544, "FY2022": -211750, "FY2021": -106956,
    }),
    ("DATA", "Dividend paid", {"FY2025": -1600000}),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2025": -1600000, "FY2024": -1680946, "FY2023": -1518544,
        "FY2022": -211750, "FY2021": -106956,
    }),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2025": 1852992, "FY2024": -152725, "FY2023": -4680040,
        "FY2022": 725055, "FY2021": -12198398,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 94560472, "FY2024": 94713197, "FY2023": 99393237,
        "FY2022": 98668182, "FY2021": 55832925,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 96413464, "FY2024": 94560472, "FY2023": 94713197,
        "FY2022": 99393237, "FY2021": 43634527,
    }),
]

bw.add_cash_flow_sheet(
    title="Havin Bank Limited — Statement of Cash Flows",
    subtitle="As presented in each year's own primary Statement of Cash Flows (Operating "
             "activities shown as the single reconciled figure the face of each year's own "
             "statement discloses, referencing that year's own supporting note for detail)",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=210,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
bw.add_asset_quality_sheet(
    title="Havin Bank Limited — Asset Quality",
    subtitle="Loans and advances to customers, by repayment status, as originally published each year "
             "(no IFRS 9 Stage 1/2/3 split is disclosed - the Bank applies FRS 102/IAS 39 incurred-loss "
             "impairment with individual, not collective, assessment)",
    rows=[
        ("SECTION", "Loans and advances to customers, by repayment status", {}),
        ("DATA", "Impaired", {
            "FY2024": 238799, "FY2023": 238844, "FY2022": 238799, "FY2021": 238799,
        }),
        ("DATA", "Past due", {
            "FY2024": 2301049, "FY2023": 1086023, "FY2021": 369139,
        }),
        ("DATA", "Within three months", {
            "FY2025": 836250, "FY2024": 304461, "FY2023": 1150339,
            "FY2022": 546367, "FY2021": 1707498,
        }),
        ("DATA", "Between three months and one year", {
            "FY2025": 4944742, "FY2024": 5264412, "FY2023": 4761704,
            "FY2022": 13476280, "FY2021": 2441092,
        }),
        ("DATA", "Between one and five years", {
            "FY2025": 4293397, "FY2024": 5562209, "FY2023": 2157082,
            "FY2022": 4459553, "FY2021": 4116289,
        }),
        ("DATA", "Over five years", {
            "FY2025": 1169507,
        }),
        ("TOTAL", "Total before impairment provision", {
            "FY2025": 11243896, "FY2024": 13671230, "FY2023": 9393992,
            "FY2022": 18720999, "FY2021": 8872817,
        }),
        ("DATA", "Impairment losses on loans and advances", {
            "FY2025": -852785, "FY2024": -1242299, "FY2023": -401685,
            "FY2022": -238799, "FY2021": -238799,
        }),
        ("TOTAL", "Total after impairment provision", {
            "FY2025": 10391111, "FY2024": 12428931, "FY2023": 8992307,
            "FY2022": 18482200, "FY2021": 8634018,
        }),
        ("SECTION", "Impairment allowance roll-forward", {}),
        ("DATA", "As at 1 January", {
            "FY2025": 1242299, "FY2024": 401685, "FY2023": 238799,
            "FY2022": 238799, "FY2021": 238799,
        }),
        ("DATA", "Provision (charge)/release for the year", {
            "FY2025": -150716, "FY2024": 840614, "FY2023": 162886,
        }),
        ("DATA", "Write-off", {
            "FY2025": -238798,
        }),
        ("TOTAL", "As at 31 December", {
            "FY2025": 852785, "FY2024": 1242299, "FY2023": 401685,
            "FY2022": 238799, "FY2021": 238799,
        }),
        ("SECTION", "Asset quality ratios (derived)", {}),
        ("DATA", "Non-performing / impaired-or-past-due loans, as disclosed", {
            "FY2025": 4852633, "FY2024": 2539848, "FY2023": 1324822,
            "FY2022": 238799, "FY2021": 607938,
        }),
        ("DATA", "Impairment coverage ratio (impairment / total before provision)", {
            "FY2025": "7.58%", "FY2024": "9.09%", "FY2023": "4.28%",
            "FY2022": "1.28%", "FY2021": "2.69%",
        }),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=66,
    source_height=280,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=140)


CAPITAL_VALUES = {
    "FY2025": 22532098, "FY2024": 23791445, "FY2023": 23105954,
    "FY2022": 22291259, "FY2021": 22508676,
}
CAPITAL_NOTE = ("FY2021 is Total Tier One Capital (Share Capital + Reserves) as no Deductions "
                 "from Capital were separately disclosed that year; FY2022-FY2025 are Total "
                 "Regulatory Capital (Total Tier One Capital less Deductions from Capital). No "
                 "AT1/T2 capital is disclosed in any year, so CET1 = Tier 1 = Total Capital.")

bw.add_km1_sheet(
    title="Havin Bank Limited — KM1 Key Metrics",
    subtitle="Not applicable — the Bank publishes no Pillar 3 disclosure at all for any year in this workbook "
             "(FY2021-FY2025), so there is no UK KM1 key-metrics template to reproduce. This is the Bank's own "
             "stated policy rather than a document this project failed to find; the evidence is set out in the "
             "source note below.",
    rows=[
        ("DATA", "UK KM1 key-metrics template", {
            y: "No Pillar 3 published for this year" for y in YEARS
        }),
    ],
    sources_text=(
        "Sources and evidence - four independent findings, each affirmative rather than a failed search:\n\n"
        "1. THE BANK'S OWN DOCUMENT INDEX SAYS SO. Havin Bank Limited's website publishes a plain document "
        "index at http://www.hib.uk.com/annrep.html (the homepage obfuscates its links through a "
        "document.write() of a URL-escaped string; decoding that escaping exposes the index). Re-read "
        "2026-09-17, it lists Pillar 3 Disclosures for 2010 through 2019 and NOTHING after 2019, alongside "
        "Annual Reports up to 2024, and states in its own words: \"The Annual Report for 2024 is available. The "
        "Pillar 3 Disclosure and Country by Country report are available upon request. The Pillar 3 Disclosure "
        "for 2019 is now available online via this website.\" The Bank is therefore stating directly that 2019 "
        "was the last edition it put online and that later ones are supplied privately on request.\n\n"
        "2. THE ANNUAL REPORTS SAY THE SAME THING, VERBATIM, EVERY YEAR. Under the headings 'Pillar 3 "
        "disclosures' and 'Country by country disclosures' the Directors' report reads \"Full disclosures are "
        "available on request\" - unchanged in the newest filing.\n\n"
        "3. NO KM1-SHAPED CONTENT EXISTS IN THE ACCOUNTS EITHER, AND THAT WAS CHECKED ON PHRASES RATHER THAN "
        "ON A HIT COUNT. The Bank's own native-text FY2024 Annual Report (http://www.hib.uk.com/hibacc2024.pdf, "
        "151,281 characters, re-fetched and re-read 2026-09-17 rather than relying on the scanned Companies "
        "House image filings) contains zero occurrences of 'risk-weighted', 'own funds', 'total exposure "
        "measure', 'combined buffer', 'countercyclical', 'Leverage ratio', 'Key metric' and 'KM1'. The single "
        "hit for 'risk weighted' is prose (\"All capital and Risk Weighted Assets (RWA) calculations reflect "
        "the Bank's interpretation of the current rules\") with no figure attached; the single hit for 'Pillar "
        "3' is the 'available on request' sentence itself; and the only liquidity sentence is a compliance "
        "assertion with no percentage (\"the Bank complies with requirements in respect of Liquidity Coverage "
        "Ratio and Net Stable Funding Ratio laid down by the Prudential Regulation Authority\"). Nothing was "
        "back-filled from the statutory accounts' Note 23 'Capital', which is a different basis and carries no "
        "RWA and no CRR ratio in any year.\n\n"
        "4. NO PARENT DISCLOSURE CARRIES THIS ENTITY EITHER. Havin Bank Limited's majority and ultimate "
        "controlling shareholder is Banco Central de Cuba (95.6%), with Banco Popular de Ahorro and Banco de "
        "Credito y Comercio (2.2% each), all Cuban state banks. There is no UK or EU holding company above the "
        "Bank and therefore no parent that owes a UK Article 433 or EU Article 13(1) disclosure in which a "
        "Havin block could appear - so the absence here is not the 'look in the parent's Pillar 3' case. The "
        "Bank's own FY2019 edition confirms it is the top of its own UK disclosure scope: \"As the Bank does "
        "not have any subsidiaries the disclosures are made on a solo basis.\" That FY2019 edition is a "
        "BIPRU-basis document reporting FY2019/FY2018 only - it pre-dates the UK KM1 template entirely, "
        "contains no KM1, and none of its figures fall in this workbook's FY2021-FY2025 window.\n\n"
        "NOT AN SDDT CASE, CHECKED AND RULED OUT: the PRA's consolidated waivers register (checked 2026-09-17) "
        "records only one modification for Havin Bank Ltd (FRN 204481) - CRR Article 26(3), from 23/08/2017. "
        "There is no SDDT Regime - General Application Rule 3.1 modification, which is the opt-in that removes "
        "the Pillar 3 disclosure duty. So the Bank's non-publication is a choice about the channel of "
        "publication, not a regulatory exemption.\n\n"
        "USER-ACTIONABLE, UNCHANGED: for FY2021-FY2025 this bank's non-disclosure is a POLICY choice, not a "
        "dead link or a blocked website. The Bank states it will supply full Pillar 3 and country-by-country "
        "disclosures ON REQUEST, so a direct written request to Havin Bank Limited is the only realistic route "
        "to a KM1 for these years. The site has been enumerated rather than guessed at, so further online "
        "searching is not expected to surface one.\n\n"
        "LATEST-EDITION CHECK 2026-09-17: the Bank's own index page (above) was read directly rather than "
        "relying on this project's cited URLs. Newest Pillar 3 published online: 2019. Newest Annual Report "
        "listed: 2024, with the FY2025 statutory accounts already held here from Companies House. Nothing "
        "newer exists on the Bank's own site."
    ),
    first_col_width=48,
    source_height=420,
)

metric("CET1 Capital", "£", [("Common Equity Tier 1 (CET1) capital", dict(CAPITAL_VALUES))],
       p3_sources(), note=CAPITAL_NOTE)
bw.add_not_disclosed_metric_sheets(["CET1 Ratio"], p3_sources())
metric("Tier 1 Capital", "£", [("Tier 1 capital", dict(CAPITAL_VALUES))],
       p3_sources(), note=CAPITAL_NOTE)
bw.add_not_disclosed_metric_sheets(["Tier 1 Ratio"], p3_sources())
metric("Total Capital", "£", [("Total regulatory capital", dict(CAPITAL_VALUES))],
       p3_sources(), note=CAPITAL_NOTE)

bw.add_not_disclosed_metric_sheets(["Total Capital Ratio", "Total RWAs"], p3_sources())

bw.add_rwa_breakdown_sheet(
    title="Havin Bank Limited — RWA Breakdown",
    subtitle="Not publicly disclosed - confirmed (Bank states disclosures are \"available on request\" only). See source note at bottom.",
    rows=[("DATA", "Not publicly disclosed", {})],
    sources_text=p3_sources(),
    first_col_width=54,
    source_height=280,
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2025": 110335587, "FY2024": 110109348, "FY2023": 121957736,
            "FY2022": 122383421, "FY2021": 121038862,
        }),
        ("Loans and advances to customers", {
            "FY2025": 10391111, "FY2024": 12428931, "FY2023": 8992307,
            "FY2022": 18482200, "FY2021": 8634018,
        }),
        ("Customer accounts", {
            "FY2025": 2805620, "FY2024": 3305718, "FY2023": 5137804,
            "FY2022": 5737501, "FY2021": 6927373,
        }),
        ("Total equity", {
            "FY2025": 22827949, "FY2024": 24183332, "FY2023": 23594030,
            "FY2022": 22873655, "FY2021": 22508678,
        }),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Total operating income", {
            "FY2025": 3698514, "FY2024": 4419637, "FY2023": 4517375,
            "FY2022": 3183256, "FY2021": 2079450,
        }),
        ("Administrative expenses", {
            "FY2025": -3352586, "FY2024": -2684867, "FY2023": -3270406,
            "FY2022": -2576449, "FY2021": -2227306,
        }),
        ("Profit/(loss) for the year", {
            "FY2025": 244617, "FY2024": 587118, "FY2023": 720375,
            "FY2022": 364978, "FY2021": -264364,
        }),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {
            "FY2025": 24183332, "FY2024": 23594030, "FY2023": 22873655,
            "FY2022": 22508676, "FY2021": 22773040,
        }),
        ("Total comprehensive income/(loss) for the year", {
            "FY2025": 244617, "FY2024": 587118, "FY2023": 720375,
            "FY2022": 364978, "FY2021": -264364,
        }),
        ("Other equity movements, net", {
            "FY2025": -1600000, "FY2024": 2184,
        }),
        ("Closing equity", {
            "FY2025": 22827949, "FY2024": 24183332, "FY2023": 23594030,
            "FY2022": 22873655, "FY2021": 22508676,
        }),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": 3521073, "FY2024": 1528221, "FY2023": -3161495,
            "FY2022": 1121795, "FY2021": -13679377,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": -68081, "FY2023": 0, "FY2022": -184990, "FY2021": 1587935,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": -1600000, "FY2024": -1680946, "FY2023": -1518544,
            "FY2022": -211750, "FY2021": -106956,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 96413464, "FY2024": 94560472, "FY2023": 94713197,
            "FY2022": 99393237, "FY2021": 43634527,
        }),
    ],
    cash_flow_unit="£",
    ratios=[],
    note="No Pillar 3 ratios are disclosed for this entity (see the individual metric sheets) "
         "- CET1/Tier 1/Total Capital £ figures are shown on their own sheets instead. Figures "
         "are duplicated from the detail sheets for at-a-glance trend viewing; see each "
         "sheet's own source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HAVIN BANK FINANCIALS.xlsx")
