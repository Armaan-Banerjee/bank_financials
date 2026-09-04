import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzUxNzE0OTI3NGFkaXF6a2N4/document?format=pdf&download=0")
AR2023_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzQxOTY5NDQ0MWFkaXF6a2N4/document?format=pdf&download=0")
AR2021_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzMzNzU0NDMwOWFkaXF6a2N4/document?format=pdf&download=0")

ENTITY_NOTE = (
    "Credit Suisse (UK) Limited ('CSUK', company 02009520, FRN 124269) - a UK private-banking/wealth-"
    "management subsidiary. Ultimate parent is UBS Group AG following UBS's acquisition of Credit Suisse "
    "Group (announced March 2023, completed June 2023) - CSUK itself remains an active, separately-"
    "reporting PRA entity throughout, still filing under its original name as of the FY2025 filing (Apr "
    "2026). All 5 Companies House filings were fully scanned/image-only, transcribed via page rendering.\n\n"
    "TWO MAJOR DISCLOSED BUSINESS EVENTS, both flagged rather than treated as anomalies:\n"
    "(1) FY2023: a pre-tax loss of £26.2m driven by £44.8m of UBS-acquisition-related expenses "
    "(accelerated lease costs, intangibles impairment, recharged transaction costs) - underlying "
    "profit before tax (excluding these) was £18.6m.\n"
    "(2) FY2025: on 20 June 2025 CSUK completed a Part VII business transfer (Financial Services and "
    "Markets Act 2000) of most of its wealth-management clients to UBS AG London Branch, following a "
    "Business Transfer Agreement signed 20 December 2024. This shows up directly in the FY2025 cash flow "
    "statement as a £539,843k 'Cash receipt from business transfer' investing-activities line and a "
    "£1,278k 'Loss from the business transfer' operating-activities adjustment, and drove RWAs down from "
    "£672m (FY2024) to £160m (FY2025) and CET1/leverage ratios sharply higher (smaller balance sheet, "
    "same capital base). CSUK's remaining business post-transfer is the limited-scope Credit Suisse "
    "London Nominees ('CSLN') hedge-fund sub-custody activity.\n\n"
    "Full opening-to-closing cash bridge ties across all 5 years, with two small immaterial gaps in the "
    "source documents' own printed figures, neither force-corrected: FY2022 closing £475,709k vs FY2023 "
    "opening £475,664k (£45k gap, explicitly explained by the FY2023 report's own footnote as the "
    "year-over-year change in the ECL allowance excluded from the cash figure); and FY2023's own three-line "
    "tail (opening £475,664k + net increase £97,529k - FX effect £24,570k = £548,623k) doesn't quite match "
    "FY2023's own printed closing balance of £548,659k (a £36k gap, source unexplained, not present in any "
    "other year - kept exactly as printed on both sides rather than adjusted to force a match). FY2021 "
    "closing £408,082k = FY2022 opening exactly; FY2023 closing £548,659k = FY2024 opening exactly; FY2024 "
    "closing £341,768k = FY2025 opening exactly."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Credit Suisse (UK) Limited's own Statement of Cash Flows:\n"
    "FY2025: Full accounts to 31 Dec 2025 (Companies House, filed 25 Apr 2026), "
    "Statement of Cash Flows p.47 - " + AR2025_URL + "\n"
    "FY2024: same FY2025 filing's own FY2024 comparative column, p.47\n"
    "FY2023: Full accounts to 31 Dec 2023 (Companies House, filed 27 Apr 2024), "
    "Statement of Cash Flows p.41 - " + AR2023_URL + "\n"
    "FY2022: same FY2023 filing's own FY2022 comparative column, p.41\n"
    "FY2021: Full accounts to 31 Dec 2021 (Companies House, filed 28 Apr 2022), "
    "Statement of Cash Flows p.46 - " + AR2021_URL + "\n\n"
    + ENTITY_NOTE
)

STATEMENTS_SOURCES = (
    "Sources - Credit Suisse (UK) Limited's own Statement of Income / Statement of Financial Position / "
    "Statement of Changes in Equity, transcribed from each year's own Companies House filing (not a later "
    "year's comparative column):\n"
    "FY2025/FY2024: Full accounts to 31 Dec 2025 (Companies House, filed 25 Apr 2026), pp.44-47 - "
    + AR2025_URL + "\n"
    "FY2023/FY2022: Full accounts to 31 Dec 2023 (Companies House, filed 27 Apr 2024), pp.38-40 - "
    + AR2023_URL + "\n"
    "FY2021: Full accounts to 31 Dec 2021 (Companies House, filed 22 Apr 2022), pp.43-45 - "
    + AR2021_URL + "\n\n"
    + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: the Balance Sheet's own line items vary genuinely across years - 'Current tax "
    "assets' is absent from the FY2021 report (present FY2022-25); 'Deferred tax assets' appears only "
    "FY2021/FY2022; 'Intangible assets'/'Goodwill' are FY2021-23 only (goodwill fully impaired in FY2021, "
    "intangibles fully impaired/written off by FY2025); 'Short-term borrowings' as its own liability line "
    "first appears FY2022 onward (not disclosed as a separate line in FY2021). The Profit & Loss reflects "
    "two genuine one-off lines: FY2021's 'Impairment on goodwill' (£13,752k, no equivalent in later years) "
    "and FY2025's 'Loss from the business transfer' (£1,278k, tied to the Part VII transfer - see ENTITY "
    "NOTE above). All reproduced as reported, blank cells where a year's own report doesn't carry that line."
)

ASSET_QUALITY_SOURCES = (
    "Sources - Credit Suisse (UK) Limited's own Loans and advances / Expected Credit Loss notes:\n"
    "FY2025/FY2024: Full accounts to 31 Dec 2025, Note 'Loans' (ECL by IFRS 9 stage), pp.69-70, and "
    "Note 35 (Transfer of business to UBS AG London Branch), p.89 - " + AR2025_URL + "\n"
    "FY2023/FY2022: Full accounts to 31 Dec 2023, Note 11 (Loans and advances, by UK/Foreign x "
    "Commercial/Consumer), p.58 - " + AR2023_URL + "\n"
    "FY2021: Full accounts to 31 Dec 2021, Note 11 (Loans and advances, by UK/Foreign x "
    "Commercial/Consumer), p.64 - " + AR2021_URL + "\n\n"
    "GRANULARITY NOTE: the Bank's own disclosed granularity genuinely changes across years, confirmed by "
    "reading each year's own note in full (not assumed). FY2025/FY2024 use a full IFRS 9 Stage 1/2/3 "
    "gross-carrying-amount/allowance table (the format introduced from the FY2025 Annual Report); "
    "FY2023/FY2022/FY2021 instead disclose a UK-vs-Foreign, Commercial-vs-Consumer breakdown plus a single "
    "aggregate allowance figure and a 'Gross Impaired loans' total (the FY2023-and-earlier report format) - "
    "no Stage 1/2/3 split was found for those 3 years despite checking. Both are shown on their own basis "
    "rather than forced onto one; the FY2024 Stage-table's net figure (£820,752k = £829,923k gross less "
    "£9,171k ECL allowance) is £1,803k higher than the Balance Sheet's own £818,949k net Loans and advances "
    "figure for that year - the Stage table tracks ECL only, not the further 'Deferred fee income' "
    "deduction the FY2023/2022/2021 Note 11 shows separately (£4,043k/£6,449k/£7,733k respectively), which "
    "plausibly accounts for the FY2024 gap too even though it isn't separately disclosed that year - flagged "
    "as a probable explanation, not force-reconciled. FY2025's entire loan book (customer-facing business) "
    "was transferred to UBS AG London Branch on 20 June 2025 under a Part VII scheme (Note 35) - all FY2025 "
    "figures on this sheet are correctly nil, not a disclosure gap."
)

RWA_BREAKDOWN_SOURCES = (
    "Not publicly disclosed in any of the 5 years - confirmed by reading each year's Annual Report in "
    "full (all numbered notes through to the final note in each filing - Note 36 'Subsequent events' in "
    "the FY2025 report, similarly the last note in the FY2023/FY2021 reports), plus the existing Pillar 3 "
    "KPI-table sourcing already used for the CET1/Tier 1/Total RWAs/Leverage/LCR/NSFR sheets. No "
    "'Capital Adequacy' note with an RWA category breakdown (credit risk/counterparty credit risk/market "
    "risk/operational risk) exists in any of the 3 Companies House filings reviewed, and (per the existing "
    "Pillar 3 sheets' own source note) no standalone Pillar 3 document for this entity was located either - "
    "only the single aggregate Total RWA figure already used on the Total RWAs sheet is disclosed anywhere."
)

bw = BankWorkbook(bank_name="Credit Suisse (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="50B633")

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents / cash and due from banks",
     {"FY2025": 21709, "FY2024": 341768, "FY2023": 548659, "FY2022": 475664, "FY2021": 408064}),
    ("DATA", "Interest-bearing deposits with banks",
     {"FY2024": 25335, "FY2023": 17198, "FY2022": 48748}),
    ("DATA", "Securities purchased under resale agreements",
     {"FY2025": 328684, "FY2024": 565944, "FY2023": 455796, "FY2022": 562004, "FY2021": 1048198}),
    ("DATA", "Trading financial assets mandatorily at FVTPL",
     {"FY2024": 13944, "FY2023": 13630, "FY2022": 18813, "FY2021": 14333}),
    ("DATA", "Loans and advances, net",
     {"FY2024": 818949, "FY2023": 1307573, "FY2022": 1706528, "FY2021": 2041139}),
    ("DATA", "Current tax assets", {"FY2025": 38, "FY2024": 3057, "FY2023": 2058}),
    ("DATA", "Other assets",
     {"FY2025": 2097, "FY2024": 32158, "FY2023": 46419, "FY2022": 56795, "FY2021": 48352}),
    ("DATA", "Deferred tax assets", {"FY2022": 3304, "FY2021": 5041}),
    ("DATA", "Intangible assets", {"FY2023": 1137, "FY2022": 13933, "FY2021": 14044}),
    ("DATA", "Goodwill", {}),
    ("TOTAL", "Total assets",
     {"FY2025": 352528, "FY2024": 1801155, "FY2023": 2392470, "FY2022": 2885789, "FY2021": 3579171}),

    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits",
     {"FY2025": 27218, "FY2024": 548119, "FY2023": 654960, "FY2022": 1094750, "FY2021": 3118581}),
    ("DATA", "Trading financial liabilities mandatorily at FVTPL",
     {"FY2024": 13849, "FY2023": 13496, "FY2022": 18613, "FY2021": 14023}),
    ("DATA", "Current income tax liability",
     {"FY2025": 6238, "FY2022": 7676, "FY2021": 4747}),
    ("DATA", "Other liabilities",
     {"FY2025": 3610, "FY2024": 26128, "FY2023": 43883, "FY2022": 34128, "FY2021": 32883}),
    ("DATA", "Provisions", {"FY2024": 1388, "FY2023": 1403, "FY2022": 713, "FY2021": 2709}),
    ("DATA", "Short-term borrowings",
     {"FY2025": 9661, "FY2024": 857231, "FY2023": 831176, "FY2022": 827333}),
    ("DATA", "Long term debt",
     {"FY2024": 55000, "FY2023": 555000, "FY2022": 556890, "FY2021": 55000}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 46727, "FY2024": 1501715, "FY2023": 2099918, "FY2022": 2540103, "FY2021": 3227943}),

    ("SECTION", "Shareholders' equity", {}),
    ("DATA", "Share capital",
     {"FY2025": 245230, "FY2024": 245230, "FY2023": 245230, "FY2022": 245230, "FY2021": 245230}),
    ("DATA", "Share premium",
     {"FY2025": 11200, "FY2024": 11200, "FY2023": 11200, "FY2022": 11200, "FY2021": 11200}),
    ("DATA", "Capital contribution",
     {"FY2025": 27500, "FY2024": 27500, "FY2023": 27500, "FY2022": 57500, "FY2021": 57500}),
    ("DATA", "Retained earnings",
     {"FY2025": 21871, "FY2024": 15510, "FY2023": 8622, "FY2022": 31756, "FY2021": 37298}),
    ("TOTAL", "Total shareholders' equity",
     {"FY2025": 305801, "FY2024": 299440, "FY2023": 292552, "FY2022": 345686, "FY2021": 351228}),
    ("TOTAL", "Total liabilities and shareholders' equity",
     {"FY2025": 352528, "FY2024": 1801155, "FY2023": 2392470, "FY2022": 2885789, "FY2021": 3579171}),
]

bw.add_balance_sheet_sheet(
    title="Credit Suisse (UK) Limited — Statement of Financial Position",
    subtitle="Entity basis, £'000. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income",
     {"FY2025": 42437, "FY2024": 124113, "FY2023": 156430, "FY2022": 88830, "FY2021": 56275}),
    ("DATA", "Interest expense",
     {"FY2025": -18060, "FY2024": -73480, "FY2023": -94427, "FY2022": -28065, "FY2021": -5122}),
    ("TOTAL", "Net interest income",
     {"FY2025": 24377, "FY2024": 50633, "FY2023": 62003, "FY2022": 60765, "FY2021": 51153}),
    ("DATA", "Commission and fee income",
     {"FY2025": 18904, "FY2024": 31922, "FY2023": 42185, "FY2022": 54048, "FY2021": 55219}),
    ("DATA", "Commission and fee expense",
     {"FY2025": -79, "FY2024": -737, "FY2023": -472, "FY2022": -740, "FY2021": -1068}),
    ("TOTAL", "Net commission and fee income",
     {"FY2025": 18825, "FY2024": 31185, "FY2023": 41713, "FY2022": 53308, "FY2021": 54151}),
    ("DATA", "Reversal of/(allowance for) expected credit losses",
     {"FY2025": 489, "FY2024": -1526, "FY2023": -3167, "FY2022": -1754, "FY2021": 2571}),
    ("DATA", "Net gain from financial assets/liabilities at FVTPL",
     {"FY2025": 63, "FY2024": 151, "FY2023": 88, "FY2022": 172, "FY2021": 195}),
    ("DATA", "Loss from business transfer", {"FY2025": -1278}),
    ("DATA", "Other revenue and foreign exchange fluctuations",
     {"FY2025": 5331, "FY2024": 2302, "FY2023": 271, "FY2022": -8, "FY2021": -196}),
    ("TOTAL", "Net revenue",
     {"FY2025": 47807, "FY2024": 82745, "FY2023": 100908, "FY2022": 112483, "FY2021": 107874}),

    ("SECTION", "Operating expenses", {}),
    ("DATA", "Compensation and benefits",
     {"FY2025": -11338, "FY2024": -36643, "FY2023": -42927, "FY2022": -39202, "FY2021": -41686}),
    ("DATA", "General and administrative expenses",
     {"FY2025": -26666, "FY2024": -35298, "FY2023": -84180, "FY2022": -51860, "FY2021": -41529}),
    ("DATA", "Impairment on goodwill", {"FY2021": -13752}),
    ("TOTAL", "Total operating expenses",
     {"FY2025": -38004, "FY2024": -71941, "FY2023": -127107, "FY2022": -91062, "FY2021": -96967}),

    ("TOTAL", "Profit/(loss) before tax",
     {"FY2025": 9803, "FY2024": 10804, "FY2023": -26199, "FY2022": 21421, "FY2021": 10907}),
    ("DATA", "Income tax benefit/(expense)",
     {"FY2025": -3442, "FY2024": -3916, "FY2023": 3065, "FY2022": -6963, "FY2021": -852}),
    ("TOTAL", "Profit/(loss) after tax",
     {"FY2025": 6361, "FY2024": 6888, "FY2023": -23134, "FY2022": 14458, "FY2021": 10055}),
    ("TOTAL", "Total comprehensive income/(loss) for the year",
     {"FY2025": 6361, "FY2024": 6888, "FY2023": -23134, "FY2022": 14458, "FY2021": 10055}),
]

bw.add_income_statement_sheet(
    title="Credit Suisse (UK) Limited — Statement of Income",
    subtitle="Entity basis, £'000. No items of other comprehensive income in any year. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Share premium", "Capital contribution", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2021", (245230, 11200, 57500, 27243, 341173)),
    ("DATA", "Total comprehensive income for the year (FY2021)", (None, None, None, 10055, 10055)),
    ("TOTAL", "At 31 December 2021", (245230, 11200, 57500, 37298, 351228)),
    ("DATA", "Total comprehensive income for the year (FY2022)", (None, None, None, 14458, 14458)),
    ("DATA", "Dividend paid (FY2022)", (None, None, None, -20000, -20000)),
    ("TOTAL", "At 31 December 2022", (245230, 11200, 57500, 31756, 345686)),
    ("DATA", "Total comprehensive loss for the year (FY2023)", (None, None, None, -23134, -23134)),
    ("DATA", "Dividend paid (FY2023)", (None, None, -30000, None, -30000)),
    ("TOTAL", "At 31 December 2023", (245230, 11200, 27500, 8622, 292552)),
    ("DATA", "Total comprehensive income for the year (FY2024)", (None, None, None, 6888, 6888)),
    ("TOTAL", "At 31 December 2024", (245230, 11200, 27500, 15510, 299440)),
    ("DATA", "Total comprehensive income for the year (FY2025)", (None, None, None, 6361, 6361)),
    ("TOTAL", "At 31 December 2025", (245230, 11200, 27500, 21871, 305801)),
]

bw.add_equity_changes_sheet(
    title="Credit Suisse (UK) Limited — Statement of Changes in Equity",
    subtitle="£'000, chronological. Every year's closing balance ties exactly to the Balance Sheet's own "
              "Total shareholders' equity and to the next year's own opening balance - no plug row needed. "
              "See source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax for the year",
     {"FY2025": 9803, "FY2024": 10804, "FY2023": -26199, "FY2022": 21421, "FY2021": 10907}),
    ("DATA", "Loss from the business transfer", {"FY2025": 1278}),
    ("DATA", "Amortisation and impairment of intangible assets",
     {"FY2024": 1137, "FY2023": 13582, "FY2022": 3566, "FY2021": 1852}),
    ("DATA", "Impairment on goodwill", {"FY2021": 13752}),
    ("DATA", "Accrued interest on long term debt",
     {"FY2025": 1836, "FY2024": 14677, "FY2023": 34049, "FY2022": 12300, "FY2021": 1635}),
    ("DATA", "Accrued interest on short-term borrowings",
     {"FY2025": 12765, "FY2024": 40087, "FY2023": 44712, "FY2022": 8822}),
    ("DATA", "Deferred fee income on loans",
     {"FY2025": -499, "FY2024": -2784, "FY2023": -3102, "FY2022": -3821}),
    ("DATA", "Foreign exchange (gain)/loss",
     {"FY2025": -2005, "FY2024": -1583, "FY2023": 1721, "FY2022": -2954, "FY2021": -1339}),
    ("DATA", "Share based Compensation (charge)/reversal",
     {"FY2024": -385, "FY2023": 394, "FY2022": -40}),
    ("DATA", "Allowance for expected credit losses (ECL)",
     {"FY2025": -489, "FY2024": 1526, "FY2023": 3094, "FY2022": 1754, "FY2021": -2571}),
    ("TOTAL", "Cash generated before changes in operating assets and liabilities",
     {"FY2025": 22689, "FY2024": 63479, "FY2023": 68251, "FY2022": 41048, "FY2021": 24236}),
    ("DATA", "Securities purchased under resale agreements",
     {"FY2025": 237260, "FY2024": -110148, "FY2023": 106208, "FY2022": 486194, "FY2021": -167802}),
    ("DATA", "Trading financial assets mandatorily at fair value through profit or loss",
     {"FY2025": 13944, "FY2024": -314, "FY2023": 5183, "FY2022": -4480, "FY2021": 20813}),
    ("DATA", "Loans and advances",
     {"FY2025": -39272, "FY2024": 489850, "FY2023": 398930, "FY2022": 336715, "FY2021": -48586}),
    ("DATA", "Interest bearing deposits with banks (excluding ECL)",
     {"FY2025": 25338, "FY2024": -8136, "FY2023": 31552, "FY2022": -48754, "FY2021": 187491}),
    ("DATA", "Other assets",
     {"FY2025": 17904, "FY2024": 13274, "FY2023": 8322, "FY2022": -8451, "FY2021": -1141}),
    ("TOTAL", "Net decrease/(increase) in operating assets",
     {"FY2025": 255174, "FY2024": 384526, "FY2023": 550195, "FY2022": 761224, "FY2021": -9225}),
    ("DATA", "Deposits",
     {"FY2025": -195682, "FY2024": -106841, "FY2023": -439790, "FY2022": -517522, "FY2021": -64484}),
    ("DATA", "Trading financial liabilities mandatorily at fair value through profit or loss",
     {"FY2025": -13849, "FY2024": 353, "FY2023": -5117, "FY2022": 4590, "FY2021": -20917}),
    ("DATA", "Share based compensation", {"FY2024": -220, "FY2023": -1774, "FY2022": -3649}),
    ("DATA", "Other liabilities and provisions",
     {"FY2025": -14841, "FY2024": -15915, "FY2023": 11963, "FY2022": 1266, "FY2021": -2672}),
    ("TOTAL", "Net decrease/(increase) in operating liabilities",
     {"FY2025": -224372, "FY2024": -122623, "FY2023": -434718, "FY2022": -515315, "FY2021": -88073}),
    ("DATA", "Income tax refunded/(paid)", {"FY2024": 119, "FY2021": 1101}),
    ("DATA", "Group relief received/(paid)",
     {"FY2025": 6127, "FY2024": -4800, "FY2023": -3319, "FY2022": -2522, "FY2021": 406}),
    ("TOTAL", "Net cash flow generated from/(used in) operating activities",
     {"FY2025": 59618, "FY2024": 320701, "FY2023": 180409, "FY2022": 284435, "FY2021": -71555}),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Cash receipt from business transfer", {"FY2025": 539843}),
    ("DATA", "Capital expenditures for intangible assets",
     {"FY2023": -786, "FY2022": -3455, "FY2021": -3799}),
    ("TOTAL", "Net cash flow generated from/(used in) investing activities",
     {"FY2025": 539843, "FY2024": 0, "FY2023": -786, "FY2022": -3455, "FY2021": -3799}),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividend paid", {"FY2023": -30000, "FY2022": -20000}),
    ("DATA", "Interest paid on long term debt",
     {"FY2025": -1916, "FY2024": -15460, "FY2023": -33420, "FY2022": -12293, "FY2021": -1620}),
    ("DATA", "Issuance of long term debt", {"FY2023": 530803, "FY2022": 500000}),
    ("DATA", "Repayment of long term debt",
     {"FY2025": -55000, "FY2024": -500000, "FY2023": -532693, "FY2022": -503689}),
    ("DATA", "Interest paid on short-term borrowings",
     {"FY2025": -17039, "FY2024": -39775, "FY2023": -43476, "FY2022": -6928}),
    ("DATA", "Issuance of short-term borrowings",
     {"FY2025": 12865, "FY2024": 713897, "FY2023": 601802, "FY2022": 615993}),
    ("DATA", "Repayment of short-term borrowings",
     {"FY2025": -845507, "FY2024": -689448, "FY2023": -575110, "FY2022": -824808}),
    ("TOTAL", "Net cash flow used in financing activities",
     {"FY2025": -906597, "FY2024": -530786, "FY2023": -82094, "FY2022": -251725, "FY2021": -1620}),

    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents",
     {"FY2025": -307136, "FY2024": -210085, "FY2023": 97529, "FY2022": 29255, "FY2021": -76974}),
    ("DATA", "Cash and cash equivalents at the beginning of the year",
     {"FY2025": 341768, "FY2024": 548659, "FY2023": 475664, "FY2022": 408082, "FY2021": 483717}),
    ("DATA", "Effect of exchange rate fluctuations on cash and cash equivalents",
     {"FY2025": -12923, "FY2024": 3194, "FY2023": -24570, "FY2022": 38372, "FY2021": 1339}),
    ("TOTAL", "Cash and cash equivalents at the end of the year",
     {"FY2025": 21709, "FY2024": 341768, "FY2023": 548659, "FY2022": 475709, "FY2021": 408082}),
]

bw.add_cash_flow_sheet(
    title="Credit Suisse (UK) Limited — Statement of Cash Flows",
    subtitle="Entity basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=88,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loan book by borrower type, gross (FY2021-FY2023 basis)", {}),
    ("DATA", "United Kingdom - Commercial", {"FY2023": 1069, "FY2022": 1556, "FY2021": 8891}),
    ("DATA", "United Kingdom - Consumer", {"FY2023": 612720, "FY2022": 791672, "FY2021": 940312}),
    ("DATA", "Foreign - Commercial", {"FY2023": 15870, "FY2022": 18896, "FY2021": 14577}),
    ("DATA", "Foreign - Consumer", {"FY2023": 689570, "FY2022": 905338, "FY2021": 1093926}),
    ("TOTAL", "Total gross loans and advances, by borrower type",
     {"FY2023": 1319229, "FY2022": 1717462, "FY2021": 2057706}),

    ("SECTION", "Loan book by IFRS 9 stage, gross (FY2024-FY2025 basis)", {}),
    ("DATA", "Stage 1 - gross carrying amount", {"FY2025": 0, "FY2024": 630187}),
    ("DATA", "Stage 2 - gross carrying amount", {"FY2025": 0, "FY2024": 107024}),
    ("DATA", "Stage 3 - gross carrying amount", {"FY2025": 0, "FY2024": 92712}),
    ("TOTAL", "Total gross loans, IFRS 9 stage basis", {"FY2025": 0, "FY2024": 829923}),

    ("SECTION", "Expected credit loss allowance", {}),
    ("DATA", "Stage 1 allowance", {"FY2025": 0, "FY2024": -537}),
    ("DATA", "Stage 2 allowance", {"FY2025": 0, "FY2024": -342}),
    ("DATA", "Stage 3 allowance", {"FY2025": 0, "FY2024": -8292}),
    ("DATA", "Allowance for credit losses, aggregate (FY2021-FY2023 basis)",
     {"FY2023": -7613, "FY2022": -4485, "FY2021": -8834}),
    ("TOTAL", "Total ECL allowance",
     {"FY2025": 0, "FY2024": -9171, "FY2023": -7613, "FY2022": -4485, "FY2021": -8834}),
    ("DATA", "Deferred fee income",
     {"FY2023": -4043, "FY2022": -6449, "FY2021": -7733}),
    ("TOTAL", "Total Loans and advances, net (ties to Balance Sheet)",
     {"FY2025": 0, "FY2024": 818949, "FY2023": 1307573, "FY2022": 1706528, "FY2021": 2041139}),

    ("SECTION", "Credit quality indicators", {}),
    ("DATA", "Gross impaired loans / Stage 3 gross carrying amount",
     {"FY2025": 0, "FY2024": 92712, "FY2023": 175850, "FY2022": 105926, "FY2021": 177499}),
    ("DATA", "Impaired/Stage 3 loans as % of total gross loans",
     {"FY2024": "11.17%", "FY2023": "13.33%", "FY2022": "6.17%", "FY2021": "8.63%"}),
    ("DATA", "ECL coverage of impaired/Stage 3 loans",
     {"FY2024": "8.94%", "FY2023": "4.33%", "FY2022": "4.23%", "FY2021": "4.98%"}),
]

bw.add_asset_quality_sheet(
    title="Credit Suisse (UK) Limited — Asset Quality",
    subtitle="Entity basis, £'000 unless %. Disclosed granularity genuinely changes across years - see "
              "source note at bottom. FY2025 loan book transferred to UBS AG London Branch (Part VII, 20 "
              "June 2025) - all FY2025 figures on this sheet are correctly nil.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=70,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


def p3_sources(page_note=""):
    return (
        "Sources - Credit Suisse (UK) Limited's own Annual Report 'Key Performance Indicators (KPIs)' "
        "table (no standalone Pillar 3 document was located for CSUK; the FY2025 Annual Report's own "
        "Strategic Report states 'Pillar 3 disclosures can be found separately at "
        "https://www.ubs.com/global/en/investor-relations', but a CSUK-specific document was not "
        "identified there within budget - WebSearch quota was already exhausted):\n"
        "FY2025/FY2024: FY2025 Annual Report, KPI table p.6 - " + AR2025_URL + "\n"
        "FY2023/FY2022: FY2023 Annual Report, KPI table p.7 - " + AR2023_URL + "\n"
        "FY2021: FY2021 Annual Report, KPI table p.8 - " + AR2021_URL + "\n"
        + page_note
    )


CET1_TIER1_CAPITAL = {"FY2025": 306, "FY2024": 299, "FY2023": 291, "FY2022": 330, "FY2021": 336}
CET1_TIER1_RATIO = {"FY2025": "191%", "FY2024": "45%", "FY2023": "29.15%", "FY2022": "29.39%", "FY2021": "25.09%"}
RWA = {"FY2025": 160, "FY2024": 672, "FY2023": 1000, "FY2022": 1124, "FY2021": 1340}
LEVERAGE_RATIO = {"FY2025": "87%", "FY2024": "17%"}
LCR = {"FY2025": "1,154%", "FY2024": "451%", "FY2023": "554.67%", "FY2022": "216.40%"}
NSFR = {"FY2025": "3,600%", "FY2024": "167%", "FY2023": "129.25%", "FY2022": "131.72%"}

COMBINED_NOTE = (
    "The Bank's own KPI table discloses a single combined 'Tier 1 and Common Equity Tier 1 (CET1)' "
    "line, not separate Tier 1/CET1 figures - used identically for both the CET1 and Tier 1 sheets."
)

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital (combined with Tier 1)", CET1_TIER1_CAPITAL)],
       p3_sources(), note=COMBINED_NOTE)
metric("CET1 Ratio", "%", [("CET1 Ratio (combined with Tier 1)", CET1_TIER1_RATIO)], p3_sources(), note=COMBINED_NOTE)
metric("Tier 1 Capital", "£m", [("Tier 1 Capital (combined with CET1)", CET1_TIER1_CAPITAL)], p3_sources(), note=COMBINED_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 Ratio (combined with CET1)", CET1_TIER1_RATIO)], p3_sources(), note=COMBINED_NOTE)

TOTAL_CAPITAL_NOTE = (
    "Not directly disclosed as a separate figure in any of the 5 years' KPI tables - only a combined "
    "'Tier 1 and CET1' figure is given, with no mention of AT1 or Tier 2 instruments anywhere. NOT "
    "assumed equal to Tier 1/CET1 without an explicit statement to that effect, per project convention - "
    "left blank rather than guessed."
)
bw.add_not_disclosed_metric_sheets(
    ["Total Capital", "Total Capital Ratio"], p3_sources(),
    per_note={"Total Capital": TOTAL_CAPITAL_NOTE, "Total Capital Ratio": TOTAL_CAPITAL_NOTE},
)

metric("Total RWAs", "£m", [("Risk Weighted Assets (RWA)", RWA)], p3_sources())

# ---------------------------------------------------------------
# Sheet: RWA Breakdown (placed right after Total RWAs)
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category", {}),
    ("TOTAL", "Total RWAs", {y: "Not publicly disclosed" for y in YEARS}),
]

bw.add_rwa_breakdown_sheet(
    title="Credit Suisse (UK) Limited — RWA Breakdown",
    subtitle="Not publicly disclosed in any year. See source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
)

metric("Leverage Ratio", "%", [("Leverage Ratio", LEVERAGE_RATIO)], p3_sources(
    "\nLeverage Ratio only appears in the KPI table format used from the FY2025 Annual Report onward - "
    "FY2023/FY2022/FY2021's KPI tables (an earlier format) don't include this metric at all, confirmed "
    "genuinely absent rather than omitted by search."))

metric("LCR", "%", [("Liquidity Coverage Ratio (LCR)", LCR)], p3_sources(
    "\nFY2021's KPI table (earliest format) discloses only a 'Liquidity Buffer (£m)' figure, no LCR% - "
    "confirmed genuinely absent for that year, not omitted by search."))

metric("NSFR", "%", [("Net Stable Funding Ratio (NSFR)", NSFR)], p3_sources(
    "\nFY2021's KPI table (earliest format) discloses only a 'Liquidity Buffer (£m)' figure, no NSFR% - "
    "confirmed genuinely absent for that year, not omitted by search."))

MREL_NOTE = (
    "Not disclosed anywhere in the 3 Annual Reports reviewed, no exemption stated. Plausibly below the "
    "Bank of England's MREL threshold given CSUK's small and (post-Part-VII-transfer) shrinking balance "
    "sheet, but not confirmed - left blank rather than guessed."
)
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": MREL_NOTE})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets",
         {"FY2025": 352528, "FY2024": 1801155, "FY2023": 2392470, "FY2022": 2885789, "FY2021": 3579171}),
        ("Loans and advances, net",
         {"FY2025": 0, "FY2024": 818949, "FY2023": 1307573, "FY2022": 1706528, "FY2021": 2041139}),
        ("Deposits",
         {"FY2025": 27218, "FY2024": 548119, "FY2023": 654960, "FY2022": 1094750, "FY2021": 3118581}),
        ("Total equity",
         {"FY2025": 305801, "FY2024": 299440, "FY2023": 292552, "FY2022": 345686, "FY2021": 351228}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net revenue",
         {"FY2025": 47807, "FY2024": 82745, "FY2023": 100908, "FY2022": 112483, "FY2021": 107874}),
        ("Total operating expense",
         {"FY2025": -38004, "FY2024": -71941, "FY2023": -127107, "FY2022": -91062, "FY2021": -96967}),
        ("Profit/(loss) for the year",
         {"FY2025": 6361, "FY2024": 6888, "FY2023": -23134, "FY2022": 14458, "FY2021": 10055}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity",
         {"FY2025": 299440, "FY2024": 292552, "FY2023": 345686, "FY2022": 351228, "FY2021": 341173}),
        ("Total comprehensive income/(loss) for the year",
         {"FY2025": 6361, "FY2024": 6888, "FY2023": -23134, "FY2022": 14458, "FY2021": 10055}),
        ("Other equity movements, net",
         {"FY2025": 0, "FY2024": 0, "FY2023": -30000, "FY2022": -20000, "FY2021": 0}),
        ("Closing equity",
         {"FY2025": 305801, "FY2024": 299440, "FY2023": 292552, "FY2022": 345686, "FY2021": 351228}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flow generated from/(used in) operating activities",
         {"FY2025": 59618, "FY2024": 320701, "FY2023": 180409, "FY2022": 284435, "FY2021": -71555}),
        ("Net cash flow generated from/(used in) investing activities",
         {"FY2025": 539843, "FY2024": 0, "FY2023": -786, "FY2022": -3455, "FY2021": -3799}),
        ("Net cash flow used in financing activities",
         {"FY2025": -906597, "FY2024": -530786, "FY2023": -82094, "FY2022": -251725, "FY2021": -1620}),
        ("Cash and cash equivalents at the end of the year",
         {"FY2025": 21709, "FY2024": 341768, "FY2023": 548659, "FY2022": 475709, "FY2021": 408082}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1/Tier 1 Ratio", CET1_TIER1_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="FY2025's cash flow figures reflect a major one-off event: the 20 June 2025 Part VII transfer of "
         "most of CSUK's business to UBS AG London Branch (a £539,843k cash receipt in investing "
         "activities), which also drove RWAs and capital ratios sharply post-transfer. See the Cash Flow "
         "Statement sheet's source note for detail. Figures are duplicated from the detail sheets for "
         "at-a-glance trend viewing.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CREDIT SUISSE UK FINANCIALS.xlsx")
