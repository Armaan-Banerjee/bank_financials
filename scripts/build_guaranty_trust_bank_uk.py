import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/05969821/filing-history/MzQ2NTE3NTM2NmFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/05969821/filing-history/MzQwNjA2NDkyOGFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/05969821/filing-history/MzM3MzI3NjAyMmFkaXF6a2N4/document?format=pdf&download=0"
P3_2025_URL = "https://gtbank-uk.files.svdcdn.com/production/download/GTBank-UK-Pillar-3-Disclosure-2025.pdf?dm=1784815695"
P3_2024_URL = "https://gtbank-uk.files.svdcdn.com/production/general/GTBank-UK-Pillar-3-Disclosure-2024.pdf?dm=1769088481"
P3_2023_URL = "https://gtbank-uk.files.svdcdn.com/production/general/GTBank-UK-Pillar-3-2023.pdf?dm=1731585289"
# A second, separately-hosted copy of the SAME FY2023 document. Re-verified 2026-09-15: both
# URLs return a real PDF; the two files are identical in content and in every printed figure
# (a full numeric diff of the extracted text found no differing value), and differ only in the
# bullet glyph used and in pagination - 26 pages in the file cited above, 27 in this one. All
# FY2023 page references in this script are to the 26-page GTBank-UK-Pillar-3-2023.pdf edition.
P3_2023_ALT_URL = "https://gtbank-uk.files.svdcdn.com/production/general/GTBUK-Pillar-3-2023.pdf"
P3_2022_URL = "https://gtbank-uk.files.svdcdn.com/production/media/GTBUK-Pillar-3-2022.pdf"

ENTITY_NOTE = (
    "Guaranty Trust Bank (UK) Limited (FRN 466611, Companies House 05969821) is a wholly-owned UK\n"
    "subsidiary of Guaranty Trust Bank Limited ('GTBank Nigeria'), itself wholly owned by Guaranty Trust\n"
    "Holding Company Plc (GTCO). Unlike several other Nigerian-bank-owned UK subsidiaries in this project\n"
    "(Zenith Bank UK, UBA UK, FCMB UK, FidBank UK), this entity reports in GBP throughout - no FX\n"
    "conversion is required.\n\n"
    "FY2025 STATUS (re-verified 2026-09-15): the FY2025 statutory accounts (year ended 31 Dec 2025) still had\n"
    "NOT been filed with Companies House - the company's own filing history shows its most recent accounts\n"
    "filing is 'Full accounts made up to 31 December 2024', filed 6 May 2025, and Companies House records the\n"
    "FY2025 accounts as next due 30 September 2026 (i.e. not yet overdue, just not filed). Every statutory-\n"
    "statement sheet in this workbook (Balance Sheet, Profit & Loss, Statement of Changes in Equity, Cash Flow\n"
    "Statement, Asset Quality) is therefore genuinely blank for FY2025.\n"
    "The Pillar 3 sheets are NOT blank for FY2025: the Bank published its own standalone 'Pillar 3 Disclosure\n"
    "2025' (as at 31 December 2025, PDF created 23 July 2026, linked from its own site at\n"
    "https://www.gtbankuk.com/about-gtbank-uk/our-company), and every Pillar 3 metric below is transcribed\n"
    "from it - see the Pillar 3 sheets' own source citation.\n\n"
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
        "Sources - Guaranty Trust Bank (UK) Limited's own standalone Pillar 3 disclosures (not GTBank Nigeria or GTCO).\n"
        f"FY2025: 'Pillar 3 Disclosure 2025' (as at 31 December 2025), section 5.2 'Key Prudential Metrics'\n"
        f"Table 2 pp.12-13, section 7.1 'Available Capital' Table 4 p.15, section 7.3 'Minimum Capital\n"
        f"Requirement' Table 5 p.16 - {P3_2025_URL}\n"
        f"FY2024: Key Metrics pp.14-15, Available Capital/MCR pp.16-18 - {P3_2024_URL}\n"
        f"FY2023: 'GTBank UK Pillar 3 Disclosures 2023', section 5.2 'Key Prudential Metrics' table pp.13-14,\n"
        f"section 7.1 'Available Capital' table p.16, section 7.3 'Minimum Capital Requirement - Pillar 1'\n"
        f"table p.17, section 7.6 'Leverage' narrative p.17 - {P3_2023_URL}\n"
        f"        (a second, identical copy of the same FY2023 document is also live at {P3_2023_ALT_URL};\n"
        f"        it differs only in pagination - 27 pages instead of 26 - and carries no differing figure.)\n"
        f"FY2022: KPI/Eligible Capital/CAR/Leverage pp.4-6 and MCR/TCR pp.14-16 - {P3_2022_URL}\n"
        "FY2021 is included as the comparative column in the FY2022 disclosure; FY2022's NSFR (the one metric\n"
        "the FY2022 edition never reports) is taken from the FY2023 edition's own FY2022 comparative column.\n"
        "These disclosures provide CET1, Tier 1 and total capital, RWA, capital ratios, leverage ratio, LCR\n"
        "and (from FY2022, via that comparative) NSFR.\n"
        "MREL is not numerically disclosed in any of the reviewed standalone reports, the FY2025 one included\n"
        "(the FY2025 document contains no occurrence of 'MREL' or 'minimum requirement for own funds' at all).\n"
        f"FY2024/FY2023 also cross-check the statutory accounts' regulatory-capital Note 23.8(a) - {AR2024_URL}.\n\n"
        "The Bank states it has no Additional Tier 1 capital, so Common Equity Tier 1 = Tier 1 = Total\n"
        "regulatory capital throughout; the same figure is used on all three sheets below.\n\n"
        "FY2025 DATA-QUALITY NOTES (read before using the FY2025 column):\n"
        "(1) CET1 basis. The FY2025 Key Metrics table's own 'Common Equity Tier 1 (\"CET1\") capital' row prints\n"
        "    37,000 for BOTH 2025 and 2024 - that is the Bank's paid-up share capital, not its CET1 capital, and\n"
        "    is an internal error in the Bank's own table (the FY2024 report prints the same 37,000 in that row\n"
        "    while its own leverage narrative states Tier 1 capital of GBP48,075,379). The same document's\n"
        "    section 7.1 'Available Capital' table builds capital from paid-up share capital 37,000 + P&L reserve\n"
        "    17,563 + fair value reserve 41 - intangibles nil = 54,604, labelled 'Sub-Total' and then 'Total\n"
        "    Capital Available' with Tier 2 and subordinated debt both nil; section 7.3 repeats 54,604 as 'Total\n"
        "    Capital Resource'. 54,604 is used here for CET1/Tier 1/Total Capital, which also ties the disclosed\n"
        "    ratio exactly: 54,604 / 148,821 = 36.69%, the ratio printed in the Key Metrics table. This is the\n"
        "    same treatment already applied to FY2024 (37,000,000 + 11,019,326 + 56,053 = 48,075,379).\n"
        "(2) FY2025 precision. The FY2025 capital figure is only available at GBP'000 precision (54,604) because\n"
        "    no FY2025 Annual Report has been filed with Companies House yet (due 30 Sep 2026), so the exact\n"
        "    pound figure from Note 23.8(a) that every earlier year uses does not exist for FY2025. The CET1/\n"
        "    Tier 1/Total Capital sheets therefore show FY2025 as 54,604,000 - the disclosed thousands figure\n"
        "    scaled, not an exact-to-the-pound amount. Earlier years remain exact to the pound.\n"
        "(3) Stale prose in the FY2025 document. Its section 7.6 'Leverage' narrative and section 7.4 still refer\n"
        "    to '31st December 2024' and 'during 2024' - unrevised copy carried over from the prior edition. Its\n"
        "    numeric tables ARE updated (Table 1 financial performance, Table 2 key metrics, Table 4 available\n"
        "    capital and Table 5 MCR each carry a distinct 2025 column alongside the 2024 comparative, and the\n"
        "    2024 comparatives match this workbook's existing FY2024 figures exactly). All FY2025 values here are\n"
        "    taken from those tables, never from the stale narrative paragraphs.\n\n"
        "FY2023 RESTATEMENT (recorded 2026-09-15, when the FY2023 Pillar 3 report itself was obtained and read as a\n"
        "primary source for the first time - until then FY2023 was carried from the FY2024 edition's comparative\n"
        "column). The FY2024 edition materially RESTATES its FY2023 comparative. Both bases are shown on this\n"
        "workbook's sheets, on separate labelled rows, rather than one overwriting the other:\n"
        "                                        FY2023 as first published   FY2023 as restated in FY2024 edition\n"
        "  Total risk-weighted exposure amount              105,275                       108,387\n"
        "  CET1 / Tier 1 / Total capital ratio               32.34%                        32.30%\n"
        "  Leverage ratio (narrative basis)                   8.29%                         8.30%\n"
        "  Credit risk MCR                                    5,712                         6,037\n"
        "  Operational risk MCR                               2,643                         2,621\n"
        "  Pillar 1 requirement                               8,368                         8,671\n"
        "  HQLA (12m average, weighted)                     230,533                       197,710\n"
        "  Cash outflows (weighted)                         199,752 -- unchanged --        199,752\n"
        "CONFIRMED UNCHANGED between the two editions, so the following FY2023 figures in this workbook are now\n"
        "verified against the primary source and not merely against a later comparative: Tier 1 capital and Total\n"
        "capital 39,391 (GBP'000; the FY2023 report's section 7.6 gives the exact figure GBP39,390,993, which ties\n"
        "to the FY2023 Balance Sheet's own Total equity), CET1 capital row printed as 37,000 in both (the known\n"
        "share-capital-not-CET1 error), total net cash outflows 74,454, LCR 250%, NSFR 310% with its components\n"
        "194,572 / 62,864, and the capital-conservation (2.50%) and countercyclical (2.00%) buffers.\n"
        "NOT CONFIRMED: the leverage ratio of 8.30% previously carried here. The FY2023 report's own section 7.6\n"
        "says 8.29%, computed there from Tier 1 GBP39,390,993 against total on- and off-balance-sheet footings of\n"
        "GBP475,263,939; the FY2024 edition restates those footings to GBP474,761,920 and so prints 8.30%. The\n"
        "FY2023 report's own Key Metrics table is a third value again, 6.00%, which is contradicted by its own\n"
        "narrative on the very next page and is not reproducible from any pair of figures it discloses - the same\n"
        "row in the FY2022, FY2024 and FY2025 editions always equals that edition's narrative leverage ratio\n"
        "(4.38%, 8.02%, 9.11%), so the FY2023 6.00% is an error in the Bank's own table. See the Leverage Ratio\n"
        "sheet, which carries all three on separate rows."
    )


bw = BankWorkbook(bank_name="Guaranty Trust Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="00B721")

STATEMENTS_SOURCES = (
    "Sources - all figures are Guaranty Trust Bank (UK) Limited's own statements, as originally published in\n"
    "each year's own Companies House-filed Annual Report and Financial Statements (FY2023 sourced from the\n"
    "FY2024 Annual Report's own FY2023 comparative column, since no separate FY2023 filing exists as a\n"
    "standalone document - the same convention already used for the Cash Flow Statement sheet):\n"
    f"FY2024: Annual Report for the year ended 31 Dec 2024, p.23-25 (Statement of comprehensive income,\n"
    f"Statement of financial position, Statement of changes in equity) - {AR2024_URL}\n"
    f"FY2023: as above (FY2024 Annual Report's own FY2023 comparative column, p.23-25) - {AR2024_URL}\n"
    f"FY2022: Annual Report for the year ended 31 Dec 2022, p.22-24 - {AR2022_URL}\n"
    f"FY2021: Annual Report for the year ended 31 Dec 2021, p.21-23 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bw.add_balance_sheet_sheet(
    title="Guaranty Trust Bank (UK) Limited — Statement of Financial Position",
    subtitle="As originally published in each year's own Annual Report",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and money market funds", {
            "FY2024": 100662477, "FY2023": 94365231,
        }),
        ("DATA", "Cash and cash equivalents", {
            "FY2022": 97716359, "FY2021": 116275570,
        }),
        ("DATA", "Loans and advances to banks", {
            "FY2024": 259678468, "FY2023": 152612406, "FY2022": 345107924, "FY2021": 230460594,
        }),
        ("DATA", "Loans and advances to customers", {
            "FY2024": 62534590, "FY2023": 57675796, "FY2022": 61872149, "FY2021": 57660949,
        }),
        ("DATA", "Investment securities (FVOCI - government securities, 100% UK/US/Belgium sovereign)", {
            "FY2024": 146470054, "FY2023": 151922722, "FY2022": 107015424, "FY2021": 82190414,
        }),
        ("DATA", "Property and equipment", {
            "FY2024": 3746354, "FY2023": 3197915, "FY2022": 2292269, "FY2021": 691135,
        }),
        ("DATA", "Right-of-use leasehold property", {
            "FY2024": 9777616, "FY2023": 10556149, "FY2022": 11599109, "FY2021": 616484,
        }),
        ("DATA", "Other assets", {
            "FY2024": 567044, "FY2023": 440852, "FY2022": 291795, "FY2021": 898439,
        }),
        ("DATA", "Deferred tax asset", {
            "FY2024": 9284, "FY2023": 12379, "FY2022": 949586, "FY2021": 2042560,
        }),
        ("TOTAL", "Total assets", {
            "FY2024": 583445887, "FY2023": 470783450, "FY2022": 626844615, "FY2021": 490836145,
        }),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits by banks", {
            "FY2024": 329988520, "FY2023": 217403953, "FY2022": 344658275, "FY2021": 291426385,
        }),
        ("DATA", "Deposits by customers", {
            "FY2024": 191532438, "FY2023": 196877072, "FY2022": 232269660, "FY2021": 163962244,
        }),
        ("DATA", "Leasehold liability", {
            "FY2024": 10765913, "FY2023": 11061158, "FY2022": 11215172, "FY2021": 704605,
        }),
        ("DATA", "Other liabilities", {
            "FY2024": 2832498, "FY2023": 5875018, "FY2022": 10338218, "FY2021": 9598620,
        }),
        ("DATA", "Deferred tax liability", {
            "FY2024": 251139, "FY2023": 175256, "FY2022": 18912, "FY2021": 54650,
        }),
        ("TOTAL", "Total liabilities", {
            "FY2024": 535370508, "FY2023": 431392457, "FY2022": 598500237, "FY2021": 465746504,
        }),
        ("SECTION", "Equity", {}),
        ("DATA", "Called up share capital", {
            "FY2024": 37000000, "FY2023": 37000000, "FY2022": 37000000, "FY2021": 37000000,
        }),
        ("DATA", "Retained earnings", {
            "FY2024": 11019326, "FY2023": 2380687, "FY2022": -8026214, "FY2021": -11900852,
        }),
        ("DATA", "Fair value reserves", {
            "FY2024": 56053, "FY2023": 10306, "FY2022": -629408, "FY2021": -9507,
        }),
        ("TOTAL", "Shareholders' funds (Total equity)", {
            "FY2024": 48075379, "FY2023": 39390993, "FY2022": 28344378, "FY2021": 25089641,
        }),
        ("TOTAL", "Total liabilities and shareholders' funds", {
            "FY2024": 583445887, "FY2023": 470783450, "FY2022": 626844615, "FY2021": 490836145,
        }),
    ],
    sources_text=(
        "The Bank's own Statement of financial position labels the cash line 'Cash and money market funds'\n"
        "FY2023-FY2024 and 'Cash and cash equivalents' FY2021-FY2022 - same line, presentation relabelled;\n"
        "shown on separate rows above rather than merged, to match each year's own disclosed label.\n\n"
        "Investment securities note (Note 14, 'Investment securities'): all years' Annual Reports disclose the\n"
        "entire book as held at Fair Value through Other Comprehensive Income (FVOCI), with the Bank stating no\n"
        "financial assets are held at amortised cost or FVTPL, and as securities issued solely by government\n"
        "institutions (UK, US and, per the FY2024 Annual Report, Belgium) - FY2024: p.46; FY2022/FY2021: p.43\n"
        "of the FY2022 Annual Report (Note 14).\n\n"
        + STATEMENTS_SOURCES
    ),
    first_col_width=62,
    source_height=260,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
bw.add_income_statement_sheet(
    title="Guaranty Trust Bank (UK) Limited — Statement of Comprehensive Income",
    subtitle="As originally published in each year's own Annual Report",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest income", {
            "FY2024": 26095367, "FY2023": 24585386, "FY2022": 12096324, "FY2021": 3155907,
        }),
        ("DATA", "Interest expense", {
            "FY2024": -8140535, "FY2023": -5078320, "FY2022": -1902227, "FY2021": -780155,
        }),
        ("TOTAL", "Net interest income", {
            "FY2024": 17954832, "FY2023": 19507066, "FY2022": 10194097, "FY2021": 2375752,
        }),
        ("DATA", "Fees and commissions income", {
            "FY2024": 3222120, "FY2023": 3544250, "FY2022": 3569967, "FY2021": 2462438,
        }),
        ("DATA", "Other operating income", {
            "FY2024": 4532851, "FY2023": 4410543, "FY2022": 3764651, "FY2021": 2587967,
        }),
        ("TOTAL", "Operating income", {
            "FY2024": 25709803, "FY2023": 27461859, "FY2022": 17528715, "FY2021": 7426157,
        }),
        ("SECTION", "Operating expenses", {}),
        ("DATA", "Personnel expenses", {
            "FY2024": -8202750, "FY2023": -8017084, "FY2022": -5831341, "FY2021": -5096462,
        }),
        ("DATA", "Depreciation", {
            "FY2024": -1370575, "FY2023": -1560012, "FY2022": -2176624, "FY2021": -1569766,
        }),
        ("DATA", "Other operating expenses", {
            "FY2024": -4581738, "FY2023": -3959278, "FY2022": -4458281, "FY2021": -10651872,
        }),
        ("TOTAL", "Total operating expenses", {
            "FY2024": -14155063, "FY2023": -13536374, "FY2022": -12466246, "FY2021": -17318100,
        }),
        ("DATA", "Other income", {
            "FY2022": 180144, "FY2021": 176822,
        }),
        ("DATA", "Rental income", {
            "FY2023": 20786,
        }),
        ("DATA", "Expected credit impairment losses (charge)/reversal", {
            "FY2024": -74019, "FY2023": 12663, "FY2022": -120728, "FY2021": -17516,
        }),
        ("TOTAL", "Profit/(Loss) before taxation", {
            "FY2024": 11480721, "FY2023": 13958934, "FY2022": 5121885, "FY2021": -9732637,
        }),
        ("DATA", "Taxation (charge)/credit", {
            "FY2024": -2842082, "FY2023": -3552033, "FY2022": -1247247, "FY2021": 1402823,
        }),
        ("TOTAL", "Profit/(Loss) for the year", {
            "FY2024": 8638639, "FY2023": 10406901, "FY2022": 3874638, "FY2021": -8329814,
        }),
        ("SECTION", "Other comprehensive income, net of corporation tax", {}),
        ("DATA", "Fair value gain/(loss) on FVOCI investment securities, net of tax", {
            "FY2024": 56053, "FY2023": 10306, "FY2022": -629408, "FY2021": -6686,
        }),
        ("DATA", "Fair value (gain)/loss reclassified to profit or loss", {
            "FY2024": -10306, "FY2023": 629408, "FY2022": 9507, "FY2021": -9507,
        }),
        ("TOTAL", "Total comprehensive income/(loss) for the year, net of tax", {
            "FY2024": 8684386, "FY2023": 11046615, "FY2022": 3254737, "FY2021": -8346007,
        }),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=200,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
bw.add_equity_changes_sheet(
    title="Guaranty Trust Bank (UK) Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest. Equity reconciliation ladder confirmed: each year's "
              "own closing balance ties exactly to the next year's own opening balance and to that year's own "
              "Balance Sheet Total equity - zero plug rows needed anywhere in this chain.",
    headers=["Share capital", "Retained earnings", "Fair value reserve", "Total equity"],
    rows=[
        ("DATA", "Balance as at 1 January 2021", (37000000, -3571038, 6686, 33435648)),
        ("DATA", "Loss for the year", (None, -8329814, None, -8329814)),
        ("DATA", "Net change in fair value", (None, None, -6686, -6686)),
        ("DATA", "Net amount reclassified to P&L", (None, None, -9507, -9507)),
        ("TOTAL", "Balance as at 31 December 2021", (37000000, -11900852, -9507, 25089641)),
        ("DATA", "Profit for the year", (None, 3874638, None, 3874638)),
        ("DATA", "Fair value (loss) on FVOCI investment securities, net of tax", (None, None, -629408, -629408)),
        ("DATA", "Net profit/(loss) reclassified to profit or loss", (None, None, 9507, 9507)),
        ("TOTAL", "Balance as at 31 December 2022", (37000000, -8026214, -629408, 28344378)),
        ("DATA", "Profit for the year", (None, 10406901, None, 10406901)),
        ("DATA", "Fair value gain on FVOCI investment securities, net of tax", (None, None, 10306, 10306)),
        ("DATA", "Fair value loss reclassified to profit or loss", (None, None, 629408, 629408)),
        ("TOTAL", "Balance as at 31 December 2023", (37000000, 2380687, 10306, 39390993)),
        ("DATA", "Profit for the year", (None, 8638639, None, 8638639)),
        ("DATA", "Fair value gain on FVOCI investment securities, net of tax", (None, None, 56053, 56053)),
        ("DATA", "Fair value gain reclassified to profit or loss", (None, None, -10306, -10306)),
        ("TOTAL", "Balance as at 31 December 2024", (37000000, 11019326, 56053, 48075379)),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=54,
    source_height=200,
)

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
# Sheet: Asset Quality
# ---------------------------------------------------------------
bw.add_asset_quality_sheet(
    title="Guaranty Trust Bank (UK) Limited — Asset Quality",
    subtitle="Loan book by maturity band and Expected Credit Loss (ECL) allowance, as originally published "
              "each year. The Bank does not disclose an IFRS 9 Stage 1/2/3 split anywhere in its Annual "
              "Report - only a single aggregate ECL figure per loan category - confirmed by reading Notes "
              "12/13 and Note 23 (credit risk) in full each year; see source note.",
    rows=[
        ("SECTION", "Loans and advances to banks", {}),
        ("DATA", "Three months or less", {
            "FY2024": 207403713, "FY2023": 144634176, "FY2022": 335020113, "FY2021": 218116770,
        }),
        ("DATA", "One year or less but over three months", {
            "FY2024": 52375036, "FY2023": 8003078, "FY2022": 10166817, "FY2021": 12416941,
        }),
        ("DATA", "Expected credit losses", {
            "FY2024": -100281, "FY2023": -24848, "FY2022": -79006, "FY2021": -73117,
        }),
        ("TOTAL", "Net loans and advances to banks", {
            "FY2024": 259678468, "FY2023": 152612406, "FY2022": 345107924, "FY2021": 230460594,
        }),
        ("SECTION", "Loans and advances to customers", {}),
        ("DATA", "Three months or less", {
            "FY2024": 1784014, "FY2023": 1022971, "FY2022": 1040567, "FY2021": 1416091,
        }),
        ("DATA", "One year or less but over three months", {
            "FY2024": 5175504, "FY2023": 4571746, "FY2022": 6260705, "FY2021": 4406409,
        }),
        ("DATA", "Five years or less but over one year", {
            "FY2024": 17362794, "FY2023": 15880590, "FY2022": 15958829, "FY2021": 16188919,
        }),
        ("DATA", "Over five years", {
            "FY2024": 38770629, "FY2023": 36660770, "FY2022": 39112659, "FY2021": 35959033,
        }),
        ("DATA", "Less: Deferred Mortgage Arrangement Fees (EIR liability)", {
            "FY2024": -532746, "FY2023": -437081, "FY2022": -389084, "FY2021": -307451,
        }),
        ("DATA", "Expected credit losses", {
            "FY2024": -25605, "FY2023": -23200, "FY2022": -111527, "FY2021": -2052,
        }),
        ("TOTAL", "Net loans and advances to customers", {
            "FY2024": 62534590, "FY2023": 57675796, "FY2022": 61872149, "FY2021": 57660949,
        }),
        ("SECTION", "Derived ratios (not directly disclosed, computed for reference)", {}),
        ("DATA", "ECL coverage - loans and advances to customers (ECL / gross carrying amount)", {
            "FY2024": "0.04%", "FY2023": "0.04%", "FY2022": "0.18%", "FY2021": "0.00%",
        }),
    ],
    sources_text=(
        "Sources - Notes 12 (Loans and advances to banks) and 13 (Loans and advances to customers) of each "
        "year's own Annual Report (same documents as the Balance Sheet sheet above); FY2023 sourced from the "
        "FY2024 Annual Report's own FY2023 comparative column. Each year's own Annual Report states 'All "
        "loans and advances to banks were performing' and loans and advances to customers were 'performing or "
        "adequately collateralised' - no non-performing loan balance is disclosed for any year. The ECL "
        "coverage ratio row is calculated (ECL / (gross carrying amount before ECL)), not a figure the Bank "
        "itself publishes - shown for reference only.\n\n" + ENTITY_NOTE
    ),
    first_col_width=68,
    source_height=210,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=48, source_height=170)


# FY2025 is the disclosed GBP'000 figure (54,604) scaled - no FY2025 Annual Report
# exists yet to give the exact pound amount; see p3_sources() note (2). FY2021-FY2024
# are exact to the pound, from each year's own Annual Report Note 23.8(a).
REG_CAPITAL = {"FY2025": 54604000, "FY2024": 48075379, "FY2023": 39390993, "FY2022": 28344378, "FY2021": 25089641}
# FY2023 = 32.34%, the figure printed in the FY2023 Pillar 3 report's OWN Key Metrics table
# (obtained and read as a primary source 2026-09-15). The 32.30% previously carried here is the
# FY2024 edition's restated FY2023 comparative, kept on its own labelled row below.
CAPITAL_RATIO = {"FY2025": "36.69%", "FY2024": "26.89%", "FY2023": "32.34%", "FY2022": "20.68%", "FY2021": "25.02%"}
RESTATED_2023_RATIO = {"FY2023": "32.30%"}
RATIO_RESTATEMENT_NOTE = (
    "Row 1 is each year as first published, in that year's own Pillar 3 report's Key Metrics table. Row 2 "
    "records that the FY2024 edition restates its FY2023 comparative to 32.30% (alongside restating FY2023 "
    "RWAs from 105,275 to 108,387 - see the Total RWAs sheet). Neither figure is overwritten by the other. "
    "Note that the Bank's printed ratio does not reconcile to its own capital and RWA on either basis "
    "(39,391 / 105,275 = 37.42%; 39,391 / 108,387 = 36.34%); both values are transcribed exactly as printed "
    "and no attempt is made to recompute them."
)

metric(
    "CET1 Capital", "£",
    [("Common Equity Tier 1 (CET1) capital", REG_CAPITAL)],
    p3_sources(),
)
metric("CET1 Ratio", "%",
       [("CET1 ratio (as first published)", CAPITAL_RATIO),
        ("CET1 ratio - FY2023 as restated in the FY2024 Pillar 3 edition", RESTATED_2023_RATIO)],
       p3_sources(), note=RATIO_RESTATEMENT_NOTE)
metric(
    "Tier 1 Capital", "£",
    [("Tier 1 capital", REG_CAPITAL)],
    p3_sources(),
    note="The Bank has no Additional Tier 1 capital, so Tier 1 capital equals CET1 capital.",
)
metric("Tier 1 Ratio", "%",
       [("Tier 1 ratio (as first published)", CAPITAL_RATIO),
        ("Tier 1 ratio - FY2023 as restated in the FY2024 Pillar 3 edition", RESTATED_2023_RATIO)],
       p3_sources(), note=RATIO_RESTATEMENT_NOTE)
metric(
    "Total Capital", "£",
    [("Total regulatory capital (unaudited)", REG_CAPITAL)],
    p3_sources(),
    note="The Bank has no Tier 2 capital, so Total Capital equals Tier 1 capital equals CET1 capital.",
)

metric("Total Capital Ratio", "%",
       [("Total Capital Ratio (as first published)", CAPITAL_RATIO),
        ("Total Capital Ratio - FY2023 as restated in the FY2024 Pillar 3 edition", RESTATED_2023_RATIO)],
       p3_sources(), note=RATIO_RESTATEMENT_NOTE)
metric("Total RWAs", "£'000",
       [("Total risk-weighted exposure amount (as first published)",
         {"FY2025": 148821, "FY2024": 157370, "FY2023": 105275, "FY2022": 187034, "FY2021": 100287}),
        ("Total risk-weighted exposure amount - FY2023 as restated in the FY2024 Pillar 3 edition",
         {"FY2023": 108387})],
       p3_sources(),
       note="FY2023 appears twice because the two editions disagree materially and neither is allowed to "
            "overwrite the other. 105,275 is the figure in the FY2023 Pillar 3 report's own Key Metrics table "
            "(read as a primary source 2026-09-15); 108,387 is the restated FY2023 comparative in the FY2024 "
            "edition. The restatement is not a rounding difference - it is 3.0% - and it is the restated figure, "
            "not the original, that reconciles exactly to the Bank's own disclosed Pillar 1 capital requirement "
            "(8,671 x 12.5 = 108,387.5, against 8,368 x 12.5 = 104,600 on the original basis versus 105,275 "
            "printed). See the RWA Breakdown sheet for what this means for the FY2023 risk-type split.")

RWA_BREAKDOWN_SOURCES = (
    "Sources - Guaranty Trust Bank (UK) Limited's own standalone Pillar 3 disclosures (not GTBank Nigeria or GTCO):\n"
    f"FY2022 & FY2021 (directly disclosed as risk-weighted assets, not derived): GTBank UK Pillar 3 Disclosures 2022, "
    f"section 2.4 'Risk-Weighted Assets (RWAs)' table (Total/Credit/Operational/Market RWA) - {P3_2022_URL}\n"
    f"FY2025 (derived, not directly disclosed as RWA): GTBank UK Pillar 3 Disclosure 2025, Table 5 'Minimum Capital "
    f"Requirement (\"MCR\")', p.16 (Credit Risk 7,857 / Market Risk 22 / Operational Risk 4,027, GBP'000, summing to "
    f"the same table's own printed Pillar 1 requirement of 11,906) - each figure below is that capital requirement "
    f"divided by 8% (x12.5), the exact Basel/CRR Article 92 identity, not an estimate. Derived total 148,825 vs the "
    f"same document's own separately disclosed Total Risk-Weighted Exposure Amount of 148,821 - a gap of 4 (0.003%), "
    f"comfortably inside the +/-19 maximum attributable to GBP'000 rounding of three components, so the x12.5 "
    f"identity reconciles cleanly for this year (unlike FY2023, see below) - {P3_2025_URL}\n"
    f"FY2024 (derived, not directly disclosed as RWA): GTBank UK Pillar 3 Disclosure 2024, Table 5 'Minimum Capital "
    f"Requirement (\"MCR\")', p.14, only discloses the Pillar 1 MINIMUM CAPITAL REQUIREMENT by risk type - so each "
    f"category figure below is that table's own capital-requirement figure divided by 8% (multiplied by 12.5), the "
    f"standard, exact Basel/CRR Article 92 identity, not an estimate. Reconciles to within £5k of the Total RWAs "
    f"sheet's own FY2024 figure (157,370) - {P3_2024_URL}\n"
    f"FY2023: checked against the FY2023 Pillar 3 report itself and still NOT added. THE BANK PUBLISHES NO FY2023 "
    f"RWA BREAKDOWN BY RISK TYPE ANYWHERE - this is a disclosure gap in the source, not a research gap. The FY2023 "
    f"report's section 6.4 'Risk-Weighted Assets' (p.15) merely names the three categories in prose and prints no "
    f"table; its Key Metrics table (pp.13-14) gives a single aggregate Total Risk-Weighted Exposure Amount of "
    f"105,275 with no split; and the only category-level figures in the entire document are CAPITAL REQUIREMENTS "
    f"(section 7.3, p.17: Credit Risk 5,712 / Market Risk 13 / Operational Risk 2,643, GBP'000), never RWAs - "
    f"{P3_2023_URL}\n"
    f"    On the original FY2023 basis the x12.5 identity does not reconcile: 8,368 x 12.5 = 104,600 against the "
    f"same report's own printed 105,275, a gap of 675 (0.6%), far beyond the +/-19 attributable to GBP'000 "
    f"rounding of three components. On the FY2024 edition's RESTATED FY2023 basis it reconciles exactly (Credit "
    f"6,037 / Market 13 / Operational 2,621 = 8,671; 8,671 x 12.5 = 108,387.5 against that edition's own restated "
    f"FY2023 RWA of 108,387). FY2023 is nonetheless still left blank here, for two reasons: (a) the derived rows "
    f"would have to sit on the restated 108,387 basis while the Total RWAs sheet's primary FY2023 row is the "
    f"as-first-published 105,275, silently mixing two bases in one column - exactly the trap this workbook's "
    f"convention exists to avoid; and (b) no FY2023 figure in either edition is a disclosed RWA. If a future pass "
    f"decides the derived basis is acceptable for FY2023, it must add the row under the restated total, label it "
    f"as such, and not reconcile it against 105,275.\n"
    "(2026-09-12 independent re-verification: re-fetched this exact document and re-read section 5.2 'Key "
    "Prudential Metrics' [Total Risk-Weighted Exposure Amount 105,275, single aggregate figure, no category "
    "split] and section 7.3 'Minimum Capital Requirement - Pillar 1' [Credit Risk 5,712 / Market Risk 13 / "
    "Operational Risk 2,643] directly - confirms this analysis exactly, no cleaner reconciling source exists "
    "anywhere else in the document. This remains a genuine internal inconsistency in the Bank's own filing, "
    "not a research gap.)\n"
    "(2026-09-15 THIRD verification, re-reading the full FY2023 document rather than the prior notes. Confirms "
    "FY2023 stays out, and strengthens the case: section 6.4 'Risk-Weighted Assets' is narrative only [it names "
    "the three categories but publishes no table], and the ONLY category-level figures anywhere in the document "
    "are capital requirements, never RWAs. The FY2023 credit MCR of 5,712 is itself internally sound - section "
    "8.3 breaks it into exposure classes that sum to it exactly [Financial Institutions 2,830 + Retail 4 + "
    "Corporate 0 + Secured against Real Estate 1,612 + Fixed and Other Assets 1,266 = 5,712] - so the 675 gap "
    "cannot be pinned on a misprinted credit figure and remains unexplained. Do not add FY2023 on the x12.5 "
    "basis.)\n"
    "(2026-09-15 SEPARATE FINDING, recorded here because it was found in the same document and bears on FY2022's "
    "reliability rather than FY2023's: the FY2023 report's own FY2022 COMPARATIVE column misprints the credit "
    "risk MCR as 9,343. The FY2022 figures carried in this sheet are NOT affected and are correct - they come "
    "from the FY2022 report's own directly-disclosed RWA table, they sum exactly to the FY2022 total of 187,034, "
    "and that total is independently confirmed by this FY2023 document's own comparative column. The FY2022 "
    "operational and market MCRs also reconcile cleanly on x12.5 [1,602 -> 20,025 vs 20,026 disclosed; 17 -> "
    "212.5 vs 215 disclosed]. Only credit does not: 9,343 x 12.5 = 116,788 against the disclosed 166,793, "
    "whereas the disclosed RWA implies an MCR of 13,343.44 - a difference of almost exactly 4,000, the signature "
    "of a leading-digit transcription error [13,343 printed as 9,343] in the comparative. Flagged so that a "
    "future pass does not 'correct' this sheet's sound FY2022 figures to match a misprinted comparative.)"
)

bw.add_rwa_breakdown_sheet(
    title="Guaranty Trust Bank (UK) Limited — RWA Breakdown",
    subtitle="Standalone Pillar 3 disclosures, £'000. FY2022/FY2021 as directly disclosed; FY2025/FY2024 derived "
             "from disclosed Pillar 1 capital requirement x 12.5 - see the two SECTION blocks below and the sources "
             "note. FY2023: no reliable risk-type breakdown recoverable - see sources note.",
    rows=[
        ("SECTION", "Standalone Pillar 3 — risk-weighted assets, as disclosed", {}),
        ("DATA", "Credit risk RWA", {"FY2022": 166793, "FY2021": 77962}),
        ("DATA", "Operational risk RWA", {"FY2022": 20026, "FY2021": 22148}),
        ("DATA", "Market risk RWA", {"FY2022": 215, "FY2021": 177}),
        ("TOTAL", "Total RWA", {"FY2022": 187034, "FY2021": 100287}),
        ("SECTION", "Pillar 1 capital requirement × 12.5 (derived from disclosed capital requirement)", {}),
        ("DATA", "Credit risk RWA (derived)", {"FY2025": 98212.5, "FY2024": 113012.5}),
        ("DATA", "Market risk RWA (derived)", {"FY2025": 275, "FY2024": 175}),
        ("DATA", "Operational risk RWA (derived)", {"FY2025": 50337.5, "FY2024": 44187.5}),
        ("TOTAL", "Total RWA (derived)", {"FY2025": 148825, "FY2024": 157375}),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=280,
)

metric("Leverage Ratio", "%",
       [("Leverage Ratio (as first published in each year's own Pillar 3 report)",
         {"FY2025": "9.11%", "FY2024": "8.02%", "FY2023": "8.29%", "FY2022": "4.38%", "FY2021": "5.04%"}),
        ("FY2023 as restated in the FY2024 and FY2025 Pillar 3 editions", {"FY2023": "8.30%"}),
        ("FY2023 as printed in the FY2023 report's own Key Metrics table (contradicted - see note)",
         {"FY2023": "6.00%"})],
       p3_sources(),
       note="FY2023 carries three rows because the Bank publishes three different numbers for it, and none is "
            "allowed to overwrite another.\n"
            "  Row 1, 8.29%: the FY2023 Pillar 3 report's own section 7.6 (p.17), which shows its working - Tier 1 "
            "capital GBP39,390,993 against total on- and off-balance-sheet footings of GBP475,263,939. That "
            "division reproduces 8.29% exactly, and the Tier 1 figure ties to this workbook's own FY2023 Tier 1 "
            "Capital sheet and Balance Sheet Total equity. This is the as-first-published basis used for every "
            "other year in row 1.\n"
            "  Row 2, 8.30%: the same measure in the FY2024 and FY2025 editions, which restate the footings to "
            "GBP474,761,920 (Tier 1 unchanged at GBP39,390,993). A GBP502,019 restatement of the denominator, "
            "worth one basis point. This is the value this workbook carried before 2026-09-15, when it was "
            "sourced from the FY2024 edition's comparative rather than from the FY2023 report itself.\n"
            "  Row 3, 6.00%: the figure printed in the FY2023 report's own Key Metrics table, in the row labelled "
            "'Leverage ratio excluding claims on central banks (%)'. It is NOT used as the headline because it is "
            "contradicted by that same report's narrative one page later and is not reproducible from any pair of "
            "figures the report discloses; and because in the FY2022, FY2024 and FY2025 editions that identically-"
            "labelled row always prints exactly the same value as that edition's narrative leverage ratio (4.38%, "
            "8.02%, 9.11% respectively), i.e. the Bank never actually excludes central bank claims in it. It is "
            "recorded rather than discarded.\n"
            "FY2025 (9.11%) is taken from the FY2025 report's Key Metrics table, NOT from its section 7.6 "
            "narrative, which was left unrevised from the prior edition and still quotes the 31 December 2024 "
            "position (8.02%). See note (3) in the source citation below.")
metric("LCR", "%", [("Liquidity Coverage Ratio", {"FY2025": "197%", "FY2024": "309%", "FY2023": "250%", "FY2022": "274%", "FY2021": "356%"})], p3_sources(),
       note="Every year is the Bank's own disclosed headline LCR, taken as printed from the Key Metrics table. "
            "Basis is consistent across editions: the FY2024 value printed in the FY2025 report's comparative "
            "column (309%) matches the FY2024 report's own figure exactly, and likewise FY2023 (250%) between "
            "the FY2024 and FY2023 editions.\n"
            "DO NOT RE-DERIVE THESE FROM THE PUBLISHED COMPONENTS. The Bank's own LCR component rows do not "
            "reconcile to its own printed ratio in ANY year, consistently and by a wide margin: FY2025 HQLA "
            "228,692 / net outflows 234,753 = 97%, not the printed 197%; FY2024 188,372 / 42,483 = 443%, not "
            "309%; FY2023 230,533 / 74,454 = 310%, not 250% (all GBP'000; the FY2023 HQLA figure here is from "
            "the FY2023 report itself, read 2026-09-15 - the FY2024 edition restates it to 197,710, which "
            "gives 266%, also not 250%, so the mismatch survives the restatement). The component arithmetic is "
            "internally sound - gross outflows less inflows does equal the stated net outflows every year - so "
            "the mismatch is between the components and the ratio, not within the components. The likely cause "
            "is a mixed basis: the HQLA row is explicitly labelled 'average of last 12mths' while the ratio "
            "appears to be struck on a different (probably year-end) basis. The disclosed ratio is used here "
            "because it is the Bank's own headline figure and the only one comparable across years and across "
            "banks in this project; no attempt is made to correct or recompute it.\n"
            "By contrast the NSFR components DO reconcile exactly every year (see that sheet), which is why "
            "this caveat is specific to LCR.")
metric("NSFR", "%",
       [("Net Stable Funding Ratio", {"FY2025": "211%", "FY2024": "260%", "FY2023": "310%", "FY2022": "253%"})],
       p3_sources(),
       note="FY2022 (253%) was added 2026-09-15. The FY2022 Pillar 3 report itself never mentions NSFR at all "
            "(the string does not occur in the document), but the FY2023 report's Key Metrics table carries a "
            "full FY2022 comparative column for it - Total available stable funding 214,036 / Total required "
            "stable funding 84,527 (GBP'000), printed ratio 253%. That is the Bank's own figure for its own "
            "entity, on the same basis as every other year on this sheet, so it is transcribed here; the same "
            "comparative-column convention is already used for FY2021 elsewhere in this workbook.\n"
            "FY2021 remains blank: no NSFR is disclosed for it in any reviewed edition, and nothing is "
            "substituted from another entity.\n"
            "Unlike the LCR sheet, the NSFR components reconcile to the printed ratio exactly in every disclosed "
            "year: FY2025 198,459 / 94,033 = 211%; FY2024 200,729 / 77,347 = 260%; FY2023 194,572 / 62,864 = "
            "310%; FY2022 214,036 / 84,527 = 253% (GBP'000).")
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources())

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2024": 583445887, "FY2023": 470783450, "FY2022": 626844615, "FY2021": 490836145,
        }),
        ("Loans and advances to customers", {
            "FY2024": 62534590, "FY2023": 57675796, "FY2022": 61872149, "FY2021": 57660949,
        }),
        ("Total liabilities", {
            "FY2024": 535370508, "FY2023": 431392457, "FY2022": 598500237, "FY2021": 465746504,
        }),
        ("Shareholders' funds (Total equity)", {
            "FY2024": 48075379, "FY2023": 39390993, "FY2022": 28344378, "FY2021": 25089641,
        }),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Operating income", {
            "FY2024": 25709803, "FY2023": 27461859, "FY2022": 17528715, "FY2021": 7426157,
        }),
        ("Total operating expenses", {
            "FY2024": -14155063, "FY2023": -13536374, "FY2022": -12466246, "FY2021": -17318100,
        }),
        ("Profit/(Loss) for the year", {
            "FY2024": 8638639, "FY2023": 10406901, "FY2022": 3874638, "FY2021": -8329814,
        }),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Total equity, end of year", {
            "FY2024": 48075379, "FY2023": 39390993, "FY2022": 28344378, "FY2021": 25089641,
        }),
    ],
    equity_changes_unit="£",
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
    note="Pillar 3 ratios ARE disclosed for this entity (CET1/Tier 1/Total Capital ratio, leverage ratio, "
         "LCR, and NSFR from FY2023) - see those individual metric sheets; only MREL is never numerically "
         "disclosed. They are not repeated in the ratio block above. The statutory-statement figures above "
         "are blank for FY2025 because no FY2025 Annual Report has been filed with Companies House yet "
         "(next due 30 Sep 2026), even though the FY2025 Pillar 3 disclosure has been published - so the "
         "Pillar 3 sheets do carry a full FY2025 column. Figures above are duplicated from the Cash Flow "
         "Statement sheet for at-a-glance trend viewing; see that sheet's own source citation, including a "
         "flagged FY2021/FY2022 basis discontinuity in the cash-equivalents figures.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/GUARANTY TRUST BANK UK FINANCIALS.xlsx")
