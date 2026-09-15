import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: KEXIM Bank (UK) Limited (company 02693038, FRN 204490,
# formerly KEXIM International (U.K.) Limited) is the wholly-owned UK subsidiary of
# the Export-Import Bank of Korea ("KEXIM", the sole shareholder). It takes the FRS
# 101 "presentation of a cash flow statement" disclosure exemption every year -
# confirmed explicitly in Note 2 "Significant accounting policies" of the FY2025
# Annual Report ("As permitted by FRS 101, the Bank has taken advantage of the
# disclosure exemptions available under that standard in relation to ... presentation
# of a cash flow statement ...", with "a statement of cash flows for the period"
# listed as the first bulleted exemption applied). No Contents/statement list in any
# of the 5 filings includes a cash flow statement. Follows the BNY Mellon
# International / ABC International Bank / Bank Mandiri Europe / DB UK Bank
# precedent: 13-sheet Pillar-3-only structure.
#
# No dedicated Pillar 3 document exists for this entity and no reachable bank-owned
# website was found this session (see WEBSITE_NOTE below) - the ONLY capital metric
# disclosed anywhere in the 5 Annual Reports checked is a single combined "Common
# Equity Tier 1 and total capital adequacy ratio" percentage, stated once per report
# in the Strategic Report's "Review of the business" section, with a prior-year
# comparative given each time (independently cross-checked and consistent across all
# 5 consecutive report-pairs - no restatements). No £ CET1/Tier1/Total Capital
# amount, no RWA figure, no Tier 1-vs-CET1 breakdown, no Leverage Ratio, LCR, NSFR or
# MREL Ratio is disclosed anywhere in the Strategic Report, Directors' Report, Risk
# Management notes, or the Notes to the Financial Statements (including Note 27
# "Parent and subsidiary relationships", which only refers the reader to the parent
# Export-Import Bank of Korea's own group accounts, and Note 28, which is an
# unrelated Capital Requirements (Country-by-Country Reporting) Regulations 2013
# disclosure, not a Pillar 3/capital-adequacy note). All 5 Companies House filings
# are fully scanned (image-only, 0 extractable text layer) - transcribed via
# targeted page-image reads, not full-document OCR.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

FY2025_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzUzMDYxMTU0N2FkaXF6a2N4/document?format=pdf&download=0"
FY2024_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzQ2ODk1NTg1M2FkaXF6a2N4/document?format=pdf&download=0"
FY2023_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzQyMzUxMTIzMWFkaXF6a2N4/document?format=pdf&download=0"
FY2022_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzM4NTcxODk4NWFkaXF6a2N4/document?format=pdf&download=0"
FY2021_AR_URL = "https://find-and-update.company-information.service.gov.uk/company/02693038/filing-history/MzM0NjA0OTUyMGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: KEXIM Bank (UK) Limited (company 02693038, FRN 204490, incorporated 3 March 1992 as KEXIM "
    "International (U.K.) Limited) is a wholly-owned subsidiary of the Export-Import Bank of Korea (\"the Parent "
    "Bank\"), which is itself 100% owned by the Korean government and is registered in South Korea. The Bank's "
    "principal activity is wholesale banking - providing credit facilities to corporates with a Korean linkage. "
    "All figures below are on the Bank's own entity-level basis, reported in pound Sterling throughout (no FX "
    "conversion needed) - it has no subsidiaries of its own."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: the FY2025 Annual Report's Note 2 \"Significant accounting policies - Basis of "
    "accounting\" states the financial statements are prepared in accordance with FRS 101 'Reduced Disclosure "
    "Framework' and that the Bank has taken advantage of the available disclosure exemptions, the first bulleted "
    f"item being \"a statement of cash flows for the period\" - KEXIM Bank (UK) Limited Annual Report 2025, p.31 - "
    f"{FY2025_AR_URL}. No cash flow statement appears in any of the 5 filings checked (FY2021-FY2025), consistent "
    "with a standing structural feature of this entity's accounts, not a one-off. Per the project's established "
    "policy for this exemption (see The Bank of New York Mellon (International) Limited / ABC International Bank "
    "plc / Bank Mandiri (Europe) Limited / DB UK Bank Limited), this workbook is built as a PILLAR-3-ONLY variant: "
    "the capital metric that is disclosed is populated below, but no cash flow figures exist to show."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

WEBSITE_NOTE = (
    "ACCESS NOTE: the domain keximbank.co.uk (as listed in some directories) resolves to an unrelated Fasthosts "
    "domain-parking page, not the Bank's own site. Two other plausible domains (keximuk.com, kexim.co.uk) either "
    "did not resolve or refused connections this session, and the Wayback Machine returned persistent HTTP 429 "
    "rate-limit responses throughout this session (a known ongoing Internet Archive-side issue also seen on "
    "other tickets in this project - not bank-specific). No standalone Pillar 3 document could therefore be "
    "located this session; worth a revisit with fresh Wayback/WebSearch budget."
)

NOT_DISCLOSED_NOTE = (
    "Not disclosed in any of the 5 Annual Reports checked (FY2021-FY2025). The Bank's \"Capital risk "
    "management (unaudited)\" note (Note 28; Note 30 in FY2021) does disclose the CET1/Tier 1/Total capital "
    "RATIOS, the leverage ratio and the aggregate RWA figure - all now populated on their own sheets - but it "
    "gives no capital AMOUNT in GBP for CET1, Tier 1 or Total Capital, and no LCR, NSFR or MREL figure appears "
    "anywhere in any filing (searched full-document OCR text of the FY2025 filing for \"liquidity coverage\", "
    "\"LCR\", \"net stable funding\", \"NSFR\", \"MREL\", \"own funds\" and \"capital resources\" - the only "
    "hit is a narrative mention that capital resources exceed PRA requirements, with no figure). MREL is in "
    "any case not applicable to this entity: it is a wholly-owned subsidiary of a foreign parent and is not a "
    "UK resolution entity.\n\n"
    "HISTORY / CORRECTION (2026-09-12 re-audit): earlier passes recorded this bank as having NO capital-"
    "management note at all, having identified Note 28 as an unrelated Country-by-Country Reporting "
    "disclosure. That was wrong. All 5 filings are image-only scans with no text layer, and full page-image "
    "OCR of every page located the capital note in each year. The GBP capital amounts, LCR and NSFR are "
    "genuinely absent from the statutory accounts - they come instead from the Bank's own signposted "
    "standalone Pillar 3 document, which was obtained by manual browser fetch on 2026-09-15 and now populates "
    "those sheets for FY2025/FY2024 (see P3_SOURCES)."
)

STATEMENTS_SOURCES = (
    "Sources - KEXIM Bank (UK) Limited's own audited financial statements (each year's own primary statements, "
    "as originally published - all 5 Companies House filings scanned/image-only, visually transcribed):\n"
    f"FY2025: Annual Report 2025, Profit and loss account p.26, Statement of comprehensive income p.27, Balance "
    f"sheet p.28, Statement of changes in equity p.30 - {FY2025_AR_URL}\n"
    f"FY2024: Annual Report 2024, Profit and loss account p.26, Balance sheet p.28, Statement of changes in "
    f"equity p.30 - {FY2024_AR_URL}\n"
    f"FY2023: Annual Report 2023, Profit and loss account p.26, Balance sheet p.28, Statement of changes in "
    f"equity p.30 - {FY2023_AR_URL}\n"
    f"FY2022: Annual Report 2022, Profit and loss account p.24, Statement of comprehensive income p.25, Balance "
    f"sheet p.26, Statement of changes in equity p.28 - {FY2022_AR_URL}\n"
    f"FY2021: Annual Report 2021, Profit and loss account p.23, Balance sheet p.25, Statement of changes in "
    f"equity p.27 - {FY2021_AR_URL}\n\n"
)

STATEMENTS_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: all figures are the Bank's own whole-pound (not £'000) presentation, GBP throughout - "
    "no FX conversion needed. FY2021's own Balance Sheet uses a current/non-current split (Non-current assets / "
    "Current assets, Creditors due within one year / after more than one year) genuinely different from "
    "FY2022-FY2025's direct Assets/Liabilities/Capital structure - combined here into the same line-item "
    "structure as the later years for comparability (e.g. 'Loans and advances to banks' sums FY2021's own "
    "non-current £23,638,936 + current £11,057,274 = £34,696,210), with the combination verified to tie exactly "
    "to FY2021's own reported Total assets/Total liabilities. Genuine £1 rounding differences exist within "
    "FY2021's own Annual Report between its Balance Sheet's Revaluation reserve/Profit and loss account figures "
    "((341,980) / 15,786,654) and its Statement of Changes in Equity's own closing figures for the same date "
    "((341,981) / 15,786,655) - each sheet below reproduces its own source page's figure as printed, not "
    "force-reconciled. Deferred tax assets/liabilities and Corporation tax receivable/payable lines are shown "
    "only in the years the Bank had a recognised balance - blank cells mean that year's own statement has no "
    "such line, not that the value is unknown."
)


INVESTMENT_BREAKDOWN_NOTE = (
    "INVESTMENT BREAKDOWN NOTE (added ST-insights investment-composition widening, 2026-09-07): 'Financial "
    "investments' (Note 17 in the FY2022-FY2025 Annual Reports; Note 18 in the FY2021 Annual Report, which "
    "instead numbers a separate, always-nil 'Financial assets designated at FVTPL' as its own Note 17) and "
    "'Debt securities: private placement bonds' (Note 16 in every year) are CONFIRMED SEPARATE, non-overlapping "
    "Balance Sheet asset lines, each with its own note and both summing independently into Total assets - not "
    "one nested inside the other. Note 17/18 'Financial investments' splits by measurement basis every year "
    "into 'measured at FVOCI' (fair value, IFRS 9) and 'measured at amortised cost' (net of ECL provision), "
    "which is reproduced below as 'Financial investments - measured at FVOCI'/'... - measured at amortised "
    "cost' for FY2021-FY2023 (no further note-level detail disclosed those years), each reconciling to the "
    "'Financial investments - total' row above (immaterial £1 rounding in FY2023 between the note's own "
    "component figures and its own stated total). For FY2024 and FY2025, the same note ALSO breaks each "
    "measurement-basis leg down by type of issuer (public ownership - governments/supranationals/other public "
    "sector bodies - vs other - banks/other issuers), reproduced below as five FVOCI issuer sub-rows and two "
    "amortised-cost issuer sub-rows in place of the two coarser measurement-basis rows for just those two "
    "years (FVOCI issuer sub-rows sum to £141,145,313 against the note's own stated FVOCI total of "
    "£141,145,314 for FY2025 - £1 rounding; FY2024's five FVOCI issuer sub-rows and both years' two amortised-"
    "cost issuer sub-rows reconcile exactly). Sources, all from KEXIM Bank (UK) Limited's own Companies House "
    "filings (image-only scans, visually transcribed), Note 16 'Debt securities: private placement bonds' and "
    "Note 17/18 'Financial investments':\n"
    f"FY2025: Annual Report 2025, Note 16 p.55, Note 17 pp.57-58 (issuer-type split p.58) - {FY2025_AR_URL}\n"
    f"FY2024: Annual Report 2024, Note 16 p.55, Note 17 p.58 (issuer-type split same page) - {FY2024_AR_URL}\n"
    f"FY2023: Annual Report 2023, Note 16 p.56, Note 17 p.59 (measurement-basis split only, no issuer-type "
    f"table) - {FY2023_AR_URL}\n"
    f"FY2022: Annual Report 2022, Note 16 p.55, Note 17 p.58 (measurement-basis split only) - {FY2022_AR_URL}\n"
    f"FY2021: Annual Report 2021, Note 16 pp.53-54, Note 18 p.56 (measurement-basis split only) - "
    f"{FY2021_AR_URL}\n\n"
    "'Debt securities: private placement bonds' shows no measurement-basis or issuer-type split in any of the "
    "5 years - its own Note 16 breaks it down only by maturity band and by internal credit-quality grade, "
    "never by FVOCI/amortised cost or by issuer type, in any of the 5 Annual Reports - so it is relabelled "
    "below to name its single measurement basis ('measured at amortised cost', consistent with its Note 16 "
    "gross/provision/net presentation, the same presentation used for loans and advances rather than the "
    "FVOCI/amortised-cost bifurcation Note 17/18 applies to 'Financial investments') rather than being split "
    "into sub-rows."
)


CAPITAL_NOTE_SOURCES = (
    "Sources - KEXIM Bank (UK) Limited's own \"Capital risk management (unaudited)\" note, table \"Capital, "
    "leverage and Risk Weighted Assets ('RWA')\", in each year's own Companies House full-accounts filing. All "
    "figures GBP (no FX conversion needed). Every figure below is independently cross-confirmed by appearing "
    "twice - once as its own year's column in its own Annual Report, and again as the prior-year comparative "
    "column in the following year's Annual Report - with no restatements found across the 5 consecutive "
    "report-pairs:\n"
    f"FY2025: Annual Report 2025, Note 28, p.86 - {FY2025_AR_URL}\n"
    f"FY2024: Annual Report 2024, Note 28, p.84 - {FY2024_AR_URL}\n"
    f"FY2023: Annual Report 2023, Note 28, p.85 - {FY2023_AR_URL}\n"
    f"FY2022: Annual Report 2022, Note 28, p.84 - {FY2022_AR_URL}\n"
    f"FY2021: Annual Report 2021, Note 30, p.83 (numbered 30 rather than 28 in this year's own note sequence) "
    f"- {FY2021_AR_URL}\n\n"
    "All 5 Companies House filings are fully scanned (image-only, no extractable text layer) - this note's "
    "table was transcribed via page-image OCR (2026-09-12 re-audit), not text extraction, which is why an "
    "earlier text-based pass over these same filings did not surface it."
)

PILLAR3_ACCESS_NOTE = (
    "ACCESS NOTE (2026-09-12 re-audit): the Bank's own Directors' Report states under the heading \"Pillar 3 "
    "Disclosures\" that \"The regulatory disclosures made in order to comply with the EU Directive and "
    "Regulation implementing the Basel capital framework ('the Pillar 3 disclosures') are available on the "
    "Kexim website at www.koreaexim.go.kr/site/uk\" (Annual Report 2025, Directors' Report, p.10). A full "
    "standalone Pillar 3 document therefore DOES exist and is publicly signposted - but that URL could not be "
    "reached from this environment: https://www.koreaexim.go.kr/site/uk returns HTTP 302 and then times out "
    "(20s, repeated attempts, both http:// and https://, with and without the www prefix); the Wayback Machine "
    "holds exactly one capture of that page (2021-03-04) and no archived PDF under it. The parent's Korean "
    "government domain appears to be geo-restricted or otherwise unreachable from here rather than absent. "
    "RESOLVED 2026-09-15: that manual browser fetch was done. The FY2025 edition of the document was obtained "
    "and has closed exactly the gaps predicted - CET1/Tier 1/Total Capital in GBP, LCR, NSFR, and a full UK "
    "OV1 RWA category breakdown, for FY2025 and FY2024. See P3_SOURCES for the document's details and the "
    "entity-scope verification.\n\n"
    "FULLY RESOLVED 2026-09-15 (second pass): the FY2021, FY2022 and FY2023 editions were ALSO retrieved, and "
    "the diagnosis above is now known to be wrong on its central point. The host is NOT geo-restricted and does "
    "NOT block scripted access - it runs a cookie challenge that makes an un-jarred curl redirect to itself "
    "indefinitely, which reads as a hang. A cookie jar clears it in one request, and the documents are indexed "
    "on the \"What's New\" board (/uk/HPHYEU015M01), not under /site/uk. No manual browser fetch was needed for "
    "any of the three. The full route is recorded in P3_EARLIER_EDITIONS_SOURCES so it can be re-walked, and "
    "the board also lists the FY2018-FY2020 editions if those years are ever wanted."
)


def p3_sources(extra=""):
    return (
        "Sources - KEXIM Bank (UK) Limited, all figures GBP (no FX conversion needed), from each year's own "
        "Companies House full-accounts filing, Strategic Report, 'Review of the business' section:\n"
        f"FY2025: Annual Report 2025, p.3 (\"The Bank's Common Equity Tier 1 and total capital adequacy ratios "
        f"decreased to 20.5% at the end of 2025 (2024: 20.9%)\") - {FY2025_AR_URL}\n"
        f"FY2024: Annual Report 2024, p.3 (\"...has decreased to 20.9% at the end of 2024 (2023: 22.8%)\") - "
        f"{FY2024_AR_URL} (independently cross-checked against the FY2025 report's own FY2024 comparative above - "
        "consistent, no restatement)\n"
        f"FY2023: Annual Report 2023, p.3 (\"...has increased slightly to 22.8% at the end of 2023 (2022: "
        f"22.5%)\") - {FY2023_AR_URL} (cross-checked against the FY2024 report's comparative - consistent)\n"
        f"FY2022: Annual Report 2022, p.3 (\"...has reduced to 22.5% at the end of 2022 (2021: 30%)\") - "
        f"{FY2022_AR_URL} (cross-checked against the FY2023 report's comparative - consistent)\n"
        f"FY2021: Annual Report 2021, p.3 (\"...ratios improved from 13.5% and 18.0% respectively at the end of "
        f"2019, to both being 36.4% at the end of 2020 and 30.0% following the partial deployment of this capital "
        f"by the end of 2021\") - {FY2021_AR_URL} (cross-checked against the FY2022 report's comparative - "
        "consistent). All 5 filings are fully scanned (image-only); figures transcribed via targeted page-image "
        "reads of the Strategic Report's 'Review of the business' section (p.3 in every filing).\n"
        + (extra + "\n" if extra else "")
    )


bw = BankWorkbook(bank_name="KEXIM Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="7A1F2B")

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 4915304, "FY2024": 10021152, "FY2023": 2688613, "FY2022": 19199889, "FY2021": 6262744}),
    ("TOTAL", "Financial investments — total", {"FY2025": 179394842, "FY2024": 181605174, "FY2023": 160938795, "FY2022": 143109644, "FY2021": 119019308}),
    ("DATA", "Financial investments — measured at FVOCI", {"FY2023": 119238695, "FY2022": 97278017, "FY2021": 86331939}),
    ("DATA", "Financial investments — measured at amortised cost", {"FY2023": 41700099, "FY2022": 45831627, "FY2021": 32687369}),
    ("DATA", "Financial investments (FVOCI) — government securities", {"FY2025": 867475, "FY2024": 3276023}),
    ("DATA", "Financial investments (FVOCI) — supranational organisations", {"FY2025": 10847689, "FY2024": 11311162}),
    ("DATA", "Financial investments (FVOCI) — other public sector bodies", {"FY2025": 7260851, "FY2024": 7386157}),
    ("DATA", "Financial investments (FVOCI) — issued by banks", {"FY2025": 72786477, "FY2024": 63380628}),
    ("DATA", "Financial investments (FVOCI) — other issuers", {"FY2025": 49382821, "FY2024": 54923213}),
    ("DATA", "Financial investments (amortised cost) — issued by banks", {"FY2025": 15202183, "FY2024": 22007019}),
    ("DATA", "Financial investments (amortised cost) — other issuers", {"FY2025": 23047345, "FY2024": 19320972}),
    ("DATA", "Debt securities: private placement bonds (measured at amortised cost)", {"FY2025": 90653832, "FY2024": 68218209, "FY2023": 72521740, "FY2022": 72526543, "FY2021": 61374708}),
    ("DATA", "Loans and advances to banks", {"FY2025": 55353800, "FY2024": 69952929, "FY2023": 64926885, "FY2022": 64280786, "FY2021": 34696210}),
    ("DATA", "Loans and advances to customers", {"FY2025": 272874882, "FY2024": 255692188, "FY2023": 221939171, "FY2022": 219863026, "FY2021": 162324430}),
    ("DATA", "Prepayments and other receivables", {"FY2025": 113759, "FY2024": 127231, "FY2023": 278605, "FY2022": 43913, "FY2021": 1839029}),
    ("DATA", "Intangible assets", {"FY2025": 91953, "FY2024": 16896, "FY2023": 28234, "FY2022": 61980, "FY2021": 85969}),
    ("DATA", "Tangible fixed assets", {"FY2025": 13991, "FY2024": 7280, "FY2023": 17751, "FY2022": 28945, "FY2021": 42073}),
    ("DATA", "'Right-of-use' asset", {"FY2025": 195759, "FY2024": 352367, "FY2023": 508975, "FY2022": 682036, "FY2021": 844708}),
    ("DATA", "Corporation tax receivable", {"FY2025": 620628}),
    ("DATA", "Deferred tax assets", {"FY2024": 14126, "FY2023": 401909, "FY2022": 1407543, "FY2021": 876}),
    ("TOTAL", "Total assets", {"FY2025": 604228751, "FY2024": 586007552, "FY2023": 524250678, "FY2022": 521204305, "FY2021": 386490055}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Borrowings from credit institutions", {"FY2025": -490903342, "FY2024": -475810294, "FY2023": -418559481, "FY2022": -406105536, "FY2021": -285675937}),
    ("DATA", "Accruals and other liabilities", {"FY2025": -4219189, "FY2024": -4490359, "FY2023": -4071702, "FY2022": -19163045, "FY2021": -3103150}),
    ("DATA", "Provisions for off-balance sheet items", {"FY2025": -61253, "FY2024": -80532, "FY2023": -35410, "FY2022": -3997}),
    ("DATA", "Corporation tax payable", {"FY2024": -548690, "FY2023": -458585, "FY2022": -274868, "FY2021": -155239}),
    ("DATA", "Deferred tax liabilities", {"FY2025": -425834}),
    ("DATA", "Lease liabilities", {"FY2025": -175022, "FY2024": -336374, "FY2023": -495550, "FY2022": -668190, "FY2021": -827158}),
    ("TOTAL", "Total liabilities", {"FY2025": -495784639, "FY2024": -481266249, "FY2023": -423620728, "FY2022": -426215636, "FY2021": -289761484}),
    ("SECTION", "Capital and reserves", {}),
    ("DATA", "Called up share capital", {"FY2025": 81283897, "FY2024": 81283897, "FY2023": 81283897, "FY2022": 81283897, "FY2021": 81283897}),
    ("DATA", "Revaluation reserve", {"FY2025": 1287040, "FY2024": -18375, "FY2023": -1328490, "FY2022": -4604133, "FY2021": -341980}),
    ("DATA", "Profit and loss account", {"FY2025": 25873175, "FY2024": 23475781, "FY2023": 20674543, "FY2022": 18308905, "FY2021": 15786654}),
    ("TOTAL", "Total shareholders' funds", {"FY2025": 108444112, "FY2024": 104741303, "FY2023": 100629950, "FY2022": 94988669, "FY2021": 96728571}),
]

bw.add_balance_sheet_sheet(
    title="KEXIM Bank (UK) Limited — Balance Sheet",
    subtitle="Entity-level basis (Bank has no subsidiaries of its own). Whole £, no FX conversion needed.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + STATEMENTS_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE + "\n\n" + INVESTMENT_BREAKDOWN_NOTE,
    first_col_width=68,
    source_height=560,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 29994776, "FY2024": 30655788, "FY2023": 25325615, "FY2022": 11556877, "FY2021": 4905429}),
    ("DATA", "Interest expense", {"FY2025": -21374863, "FY2024": -23894652, "FY2023": -20979927, "FY2022": -7253595, "FY2021": -1647023}),
    ("TOTAL", "Net interest income", {"FY2025": 8619913, "FY2024": 6761136, "FY2023": 4345688, "FY2022": 4303282, "FY2021": 3258406}),
    ("DATA", "Net loss on financial assets designated at FVTPL", {"FY2021": -10063}),
    ("DATA", "Net gain on derivatives", {"FY2021": 812}),
    ("DATA", "Fees and commission income", {"FY2025": 1358502, "FY2024": 746764, "FY2023": 1473358, "FY2022": 1456092, "FY2021": 1148928}),
    ("DATA", "Fees and commission expense", {"FY2025": -30523, "FY2024": -25301, "FY2023": -31231, "FY2022": -2908, "FY2021": -9309}),
    ("DATA", "Other operating income/(loss)", {"FY2025": -168584, "FY2024": 265263, "FY2023": -55678, "FY2022": 400171, "FY2021": -235485}),
    ("TOTAL", "Total operating income", {"FY2025": 9779308, "FY2024": 7747862, "FY2023": 5732137, "FY2022": 6156637, "FY2021": 4153289}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -4398250, "FY2024": -3657484, "FY2023": -2628149, "FY2022": -2806180, "FY2021": -2489926}),
    ("DATA", "Impairment charge on financial assets", {"FY2025": -1982010, "FY2024": -348957, "FY2023": -5459, "FY2022": -241383, "FY2021": -93026}),
    ("TOTAL", "Profit on ordinary activities before tax", {"FY2025": 3399048, "FY2024": 3741421, "FY2023": 3098529, "FY2022": 3109074, "FY2021": 1570337}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": -861590, "FY2024": -940183, "FY2023": -732891, "FY2022": -591640, "FY2021": -321939}),
    ("TOTAL", "Profit on ordinary activities after tax", {"FY2025": 2537458, "FY2024": 2801238, "FY2023": 2365638, "FY2022": 2517434, "FY2021": 1248398}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Reclassified to profit and loss", {"FY2025": -80276, "FY2024": -211575}),
    ("DATA", "Gain/(loss) arising during the year", {"FY2025": 1855966, "FY2024": 1936519, "FY2023": None, "FY2022": -5640570}),
    ("DATA", "Changes in allowance for expected credit losses during the year - FVOCI", {"FY2025": -35137, "FY2024": 21876, "FY2022": 9305}),
    ("DATA", "Credit/(debit) to deferred tax", {"FY2025": -435138, "FY2024": -436705, "FY2022": 1385670}),
    ("DATA", "Debit to deferred tax - prior year", {"FY2022": -16110}),
    ("TOTAL", "Other comprehensive income/(loss) for the year, net of tax", {"FY2025": 1305415, "FY2024": 1310115, "FY2023": 3275643, "FY2022": -4262152, "FY2021": -1442616}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 3842873, "FY2024": 4111353, "FY2023": 5641281, "FY2022": -1744718, "FY2021": -194218}),
]

bw.add_income_statement_sheet(
    title="KEXIM Bank (UK) Limited — Profit & Loss",
    subtitle="Entity-level basis, whole £. FY2023's own report discloses no OCI line-item breakdown beyond the "
              "net total - the FY2023 'Gain/(loss) arising during the year' cell is deliberately left blank, not "
              "guessed, while the Other comprehensive income TOTAL row (3,275,643) is the Bank's own disclosed "
              "figure. FY2021 alone discloses small FVTPL/derivatives lines, absent FY2022-2025.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + STATEMENTS_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE,
    first_col_width=72,
    source_height=420,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological) - built using the per-year
# reconciliation ladder: Balance Sheet built first (above), then each
# year's closing balance checked against both the next year's own opening
# balance and that year's own Balance Sheet Total. Ties exactly at every
# boundary (subject to the two documented £1 source-rounding artifacts and
# one £3 artifact within FY2025's own equity statement, all reproduced as
# disclosed, not force-reconciled - see source note).
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "Balance at 1 January 2021", (81283897, 1100635, 14578021, 96962553)),
    ("DATA", "Profit for the year (FY2021)", (None, None, 1248398, 1248398)),
    ("DATA", "Dividends paid during the year (FY2021)", (None, None, -39764, -39764)),
    ("DATA", "Other comprehensive loss for the year (FY2021)", (None, -1442616, None, -1442616)),
    ("TOTAL", "Balance at 31 December 2021 (per FY2021's own Equity Statement; FY2021's own Balance Sheet "
              "shows Revaluation reserve (341,980) and Profit and loss account 15,786,654, each £1 different - "
              "reproduced as disclosed)", (81283897, -341981, 15786655, 96728571)),
    ("DATA", "Prior year adjustment (corporation tax) (FY2022)", (None, None, 4816, 4816)),
    ("DATA", "Profit for the year (FY2022)", (None, None, 2517434, 2517434)),
    ("DATA", "Other comprehensive loss for the year (FY2022)", (None, -4262152, None, -4262152)),
    ("TOTAL", "Balance at 31 December 2022", (81283897, -4604133, 18308905, 94988669)),
    ("DATA", "Profit for the year (FY2023)", (None, None, 2365638, 2365638)),
    ("DATA", "Other comprehensive income for the year (FY2023)", (None, 3275643, None, 3275643)),
    ("TOTAL", "Balance at 31 December 2023", (81283897, -1328490, 20674543, 100629950)),
    ("DATA", "Profit for the year (FY2024)", (None, None, 2801238, 2801238)),
    ("DATA", "Other comprehensive income for the year (FY2024)", (None, 1310115, None, 1310115)),
    ("TOTAL", "Balance at 31 December 2024", (81283897, -18375, 23475781, 104741303)),
    ("DATA", "Dividends paid during the year (FY2025)", (None, None, -140062, -140062)),
    ("DATA", "Profit for the year (FY2025)", (None, None, 2537458, 2537458)),
    ("DATA", "Other comprehensive income for the year (FY2025) (per FY2025's own Equity Statement; the "
              "Statement of Comprehensive Income shows this year's OCI total as 1,305,415, £1 different - "
              "reproduced as disclosed, see source note)", (None, 1305416, None, 1305416)),
    ("TOTAL", "Balance at 31 December 2025 (FY2025's own Equity Statement's column arithmetic is £2-3 off its "
              "own printed closing total - reproduced exactly as printed, not recomputed)", (81283897, 1287040, 25873175, 108444112)),
]

bw.add_equity_changes_sheet(
    title="KEXIM Bank (UK) Limited — Statement of Changes in Equity",
    subtitle="Entity-level basis, whole £. Chronological roll-forward, oldest to newest. GBP throughout - no FX "
              "conversion needed. Ties exactly to the Balance Sheet's own Total shareholders' funds at every "
              "year-end (subject to the documented £1-3 source-rounding artifacts noted in each row).",
    headers=["Called up share capital", "Revaluation reserve", "Profit and loss account", "Total equity"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + STATEMENTS_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE,
    first_col_width=90,
    source_height=460,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the notes below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="KEXIM Bank (UK) Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source notes below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES + "\n\n" + WEBSITE_NOTE,
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Asset Quality - the Bank's own Note 15 "Loans and advances to customers"
# discloses a full IFRS 9 Stage 1/2/3 gross-carrying-amount roll-forward
# and a stage-by-rating-grade net-of-provision table for every year. All
# 5 years are 100% Stage 1 except FY2025 (Stage 2 appeared for the first
# time) and FY2024 (a small Stage 2 balance also existed) - confirmed by
# reading Note 15 in full for every year, cross-checked against the
# FY2025 Independent Auditor's Report's own Key Audit Matter figures
# (£266,875k Stage 1 / £9,030k Stage 2 at 31 December 2025, in thousands
# - matches the whole-£ note figures below exactly once rounded).
# ---------------------------------------------------------------
AQ_GROSS_S1 = {"FY2025": 266875202, "FY2024": 256529805, "FY2023": 222698727, "FY2022": 220649996, "FY2021": 162920170}
AQ_GROSS_S2 = {"FY2025": 9029903, "FY2024": 155589, "FY2023": 0, "FY2022": 0, "FY2021": 0}
AQ_GROSS_S3 = {y: 0 for y in YEARS}
AQ_GROSS_TOTAL = {y: AQ_GROSS_S1[y] + AQ_GROSS_S2[y] + AQ_GROSS_S3[y] for y in YEARS}
AQ_PROV_TOTAL = {"FY2025": 3030223, "FY2024": 993206, "FY2023": 759555, "FY2022": 786970, "FY2021": 595740}
AQ_NET_S1 = {"FY2025": 265322599, "FY2024": 255544563, "FY2023": None, "FY2022": None, "FY2021": None}
AQ_NET_S2 = {"FY2025": 7552283, "FY2024": 147626, "FY2023": None, "FY2022": None, "FY2021": None}
AQ_PROV_S1 = {y: (AQ_GROSS_S1[y] - AQ_NET_S1[y]) if AQ_NET_S1[y] is not None else None for y in YEARS}
AQ_PROV_S2 = {y: (AQ_GROSS_S2[y] - AQ_NET_S2[y]) if AQ_NET_S2[y] is not None else None for y in YEARS}
AQ_NET_TOTAL = {"FY2025": 272874882, "FY2024": 255692188, "FY2023": 221939172, "FY2022": 219863026, "FY2021": 162324430}
AQ_COVERAGE = {y: f"{AQ_PROV_TOTAL[y] / AQ_GROSS_TOTAL[y] * 100:.4f}%" for y in YEARS}
AQ_STAGE2_RATIO = {y: f"{AQ_GROSS_S2[y] / AQ_GROSS_TOTAL[y] * 100:.4f}%" for y in YEARS}

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)", AQ_GROSS_S1),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", AQ_GROSS_S2),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", AQ_GROSS_S3),
    ("TOTAL", "Total gross carrying amount", AQ_GROSS_TOTAL),
    ("SECTION", "Loss allowance (ECL) by stage - only disclosed by stage for FY2025/FY2024, "
                "when Stage 2 first appeared; FY2021-FY2023 were 100% Stage 1 so the total loss allowance "
                "IS the Stage 1 loss allowance", {}),
    ("DATA", "Stage 1 loss allowance", AQ_PROV_S1),
    ("DATA", "Stage 2 loss allowance", AQ_PROV_S2),
    ("DATA", "Total loss allowance", AQ_PROV_TOTAL),
    ("SECTION", "Net carrying amount", {}),
    ("TOTAL", "Total net carrying amount (ties to Balance Sheet's own Loans and advances to customers)", AQ_NET_TOTAL),
    ("SECTION", "Ratios", {}),
    ("DATA", "Stage 2 exposure ratio (Stage 2 / total gross carrying amount)", AQ_STAGE2_RATIO),
    ("DATA", "Overall coverage ratio (total loss allowance / total gross carrying amount)", AQ_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="KEXIM Bank (UK) Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Loans and advances to customers by IFRS 9 stage, whole £. Entity-level basis - the Bank has no "
              "subsidiaries of its own.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - KEXIM Bank (UK) Limited's own Note 15 'Loans and advances to customers' (gross carrying "
        "amount roll-forward and stage-by-rating-grade table), all 5 filings scanned/image-only, visually "
        "transcribed:\n"
        f"FY2025/FY2024: Annual Report 2025, Note 15, p.52-53 - {FY2025_AR_URL}\n"
        f"FY2023/FY2022: Annual Report 2023, Note 15, p.54-56 - {FY2023_AR_URL}\n"
        f"FY2021: Annual Report 2021, Note 15, p.50 - {FY2021_AR_URL}\n\n"
        "FY2021-FY2023 are genuinely 100% Stage 1 (confirmed by reading each year's own stage-by-rating-grade "
        "table in full, all showing nil Stage 2/Stage 3 columns) - Stage 2 first appears in FY2024 (£155,589, "
        "a single transferred exposure) and grows materially in FY2025 (£9,029,903). No Stage 3 (credit-impaired) "
        "balance has existed in any of the 5 years covered. Net-by-stage figures (and therefore per-stage loss "
        "allowance) are only derivable for FY2025/FY2024, since only those years' own tables show a nonzero "
        "Stage 2 net balance to work from - FY2021-FY2023's Total loss allowance is shown undivided since it is "
        "entirely Stage 1 by construction.\n\n" + ENTITY_NOTE
    ),
    first_col_width=88,
    source_height=440,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=190)


CAPITAL_RATIO = {"FY2025": "20.5%", "FY2024": "20.9%", "FY2023": "22.8%", "FY2022": "22.5%", "FY2021": "30.0%"}
LEVERAGE_RATIO = {"FY2025": "16.9%", "FY2024": "16.1%", "FY2023": "17.3%", "FY2022": "16.7%", "FY2021": "23.0%"}
RWA = {"FY2025": 517644568, "FY2024": 488424781, "FY2023": 431163080, "FY2022": 405644306, "FY2021": 316997557}

# Pillar 3 basis (standalone Pillar 3 document, obtained 2026-09-15 by manual
# browser fetch of the parent-hosted URL that blocks scripted access). These are
# the Bank's own regulatory-capital AMOUNTS, which the statutory accounts' Note 28
# never gives - so they close a genuine gap rather than duplicating anything.
# CET1 = Tier 1 = Total capital exactly: section 4 "Own Funds" (p.22) shows
# Additional Tier 1 and Total Tier 2 capital as "-" in both years, so all three
# tiers are the same single figure as disclosed, not an assumption.
# IMPORTANT - see P3_VS_NOTE28_BASIS_NOTE: this document's ratios/RWA/leverage do
# NOT equal the Note 28 figures above for the same year-ends. Both sets are
# internally consistent; they are different bases. The sheets below keep the two
# apart rather than mixing them.
# FY2023/FY2022/FY2021 added 2026-09-15 from the FY2023, FY2022 and FY2021
# editions of the same document (see P3_EARLIER_EDITIONS_SOURCES). Those three
# editions disclose capital to £'000 only, where the FY2025 edition gives whole
# pounds - so these three are the printed £'000 figure scaled by 1,000 and are
# precise to +/-£500. Each reconciles to this workbook's own Balance Sheet
# shareholders' funds for the same year-end (FY2023 100,629,950 / FY2022
# 94,988,669 / FY2021 96,728,571), which is the expected relationship: the Own
# Funds tables show no deductions and nil AT1/Tier 2 in every year.
P3_CAPITAL_AMOUNT = {
    "FY2025": 108444112, "FY2024": 104741303,
    "FY2023": 100630000, "FY2022": 94989000, "FY2021": 96729000,
}
P3_LCR = {
    "FY2025": "1,375%", "FY2024": "1,164%",
    "FY2023": "893%", "FY2022": "189%", "FY2021": "349%",
}
# FY2021 is deliberately absent, not missing: the FY2021 and FY2022 editions
# contain zero occurrences of "net stable funding" or "NSFR" anywhere in the
# document. That is exactly what PRA PS17/21 predicts - the UK had no NSFR
# disclosure template before 1 January 2022, and the four-quarter-average rule
# pushed first required disclosure to after 1 January 2023. FY2022's value is
# the FY2023 edition's own comparative column, which is where the Bank first
# published it.
P3_NSFR = {
    "FY2025": "111.1%", "FY2024": "124.5%",
    "FY2023": "113.6%", "FY2022": "114.6%",
}

P3_SOURCES = (
    "Sources - KEXIM Bank (UK) Limited, \"Pillar 3 and Remuneration Code Disclosures at 31 December 2025\" "
    "(42pp, real text layer). ENTITY SCOPE VERIFIED before use: this is the UK entity's own solo disclosure, "
    "not the Korean parent's group document - every page is footed \"Kexim Bank (UK) Limited\", section 1 "
    "identifies the subject as \"KEXIM Bank (UK) Limited ('KEXIM UK' or 'the Bank') ... a UK-incorporated bank "
    "authorised by the Prudential Regulation Authority\", and section 1.2 states \"The Bank is a single entity "
    "and no consolidation is performed.\" No group figures are used anywhere on these sheets.\n"
    "Figures taken from: section 4 \"Own Funds\" capital-resources table, p.22 (columns headed 31-12-2025 and "
    "31-12-2024); \"UK OV1 - Overview of risk weighted exposure amounts\", p.26; and \"UK KM1 - Key metrics\", "
    "Appendix I, p.38.\n"
    "OBTAINED 2026-09-15 BY MANUAL BROWSER FETCH. The Bank's Directors' Report signposts these disclosures at "
    "www.koreaexim.go.kr/site/uk (the parent's Korean government domain), which returns HTTP 302 and then "
    "times out to scripted requests from this environment and has no usable Wayback capture - so the PDF was "
    "downloaded by hand in an ordinary browser and transcribed from the local copy.\n\n"
    "COMPARATIVE-COLUMN CORRECTION (the Bank's own formatting error, resolved not guessed): the KM1 template "
    "on p.38 prints its comparative figures in column \"e\", which its own header labels T-4 (i.e. FY2021), "
    "leaving columns b/c/d (T-1/T-2/T-3) empty. Those figures are in fact T-1 = FY2024, confirmed four "
    "independent ways: (1) the OV1 table on p.26 carries the identical totals (502,801,056 and 492,924,960) in "
    "columns properly labelled a=T and b=T-1; (2) the section 4 Own Funds table on p.22 gives the identical "
    "capital amounts under explicit \"31-12-2025\"/\"31-12-2024\" column headings; (3) the document's own "
    "narrative describes the movements as year-on-year (\"capital adequacy ratio year-on-year from 21.25% to "
    "21.6%\", \"Leverage Ratio from 16.56% to 17.29%\"); and (4) this workbook's FY2021 figures from the "
    "statutory accounts (30.0% ratio, 23.0% leverage, RWA 316,997,557) bear no resemblance to them. The "
    "comparatives are therefore recorded here as FY2024."
)

P3_EARLIER_EDITIONS_SOURCES = (
    "FY2023/FY2022/FY2021 SOURCES - RETRIEVED 2026-09-15, NO MANUAL FETCH NEEDED. The earlier editions were "
    "obtained directly from the Bank's own site, which corrects the prior conclusion (recorded below and now "
    "superseded) that they were unreachable from this environment.\n"
    "THE ROUTE, recorded so it can be re-walked: www.koreaexim.go.kr does not block scripted access - it runs "
    "a COOKIE CHALLENGE. A first request to /site/uk returns HTTP 302 with Location: /site/uk (i.e. redirecting "
    "to itself) while issuing Set-Cookie. curl without a cookie jar therefore follows the redirect forever and "
    "appears to hang, which is what every earlier attempt observed and misread as geo-blocking or a dead host. "
    "Adding a cookie jar (curl -c/-b) so the WMONID/JSESSIONID cookies are stored and replayed returns HTTP 200 "
    "immediately. No proxy, no special TLS handling and no manual browser were required.\n"
    "THE INDEX: the documents are not under /site/uk at all. They sit on the \"What's New\" board at "
    "https://www.koreaexim.go.kr/uk/HPHYEU015M01, which lists every edition from FY2018 to FY2025, each with a "
    "direct attachment link of the form /comm/getFile?srvcId=BBSTY1&upperNo=<id>&fileTy=ATTACH&fileNo=1. The "
    "ids used here are FY2023=108650, FY2022=104242, FY2021=101611 (FY2020=64305, FY2019=63045 and FY2018=61575 "
    "are also listed and remain available). This is a stable board index, not the server-generated timestamp "
    "filenames the earlier note reported, so URL permutation was never the right approach - the board listing "
    "was simply behind the cookie challenge.\n"
    "ENTITY SCOPE VERIFIED for all three: every page of each document is footed \"Kexim Bank (UK) Limited\" and "
    "each cover reads \"Pillar 3 Disclosures for the year ended 31 December <year>\". These are the UK entity's "
    "solo disclosures, not the Korean parent's group document.\n"
    "YEAR IDENTITY VERIFIED - the FY2022 edition carries a STALE RUNNING HEADER reading \"Pillar 3 and "
    "Remuneration Code Disclosures at 31 December 2021\" on every page, an uncorrected copy-forward by the "
    "Bank. Its title page, its section 5.2 table (\"at 31 December 2022\") and its data all say FY2022, and the "
    "figures chain correctly across the three editions: FY2021 CET1 96,729 -> FY2022 prints 94,989 with 96,729 "
    "as its comparative -> FY2023 prints 100,630 with 94,989 as its comparative. The document was confirmed to "
    "be FY2022 from its content, never from its filename or header.\n"
    "FIGURES TAKEN FROM: \"Key metrics\" dashboard, p.3 (LCR, leverage, NSFR); section 4 \"Own Funds\" "
    "capital-resources table (CET1 / AT1 / Tier 2 / total regulatory capital, all in £'000); and section 5.2 "
    "\"Pillar 1 capital requirements\", the \"Minimum Capital Requirement (8%)\" table, p.27-28 (RWA by risk "
    "type).\n"
    "ARITHMETIC CHECK - each year's risk-type rows sum exactly to that year's printed Total Risk Exposure "
    "Amount, with no residual: FY2023 419,544 + 10,128 + 1,491 = 431,163 (printed TREA 431,163,079); FY2022 "
    "396,552 + 8,614 + 273 = 405,439 (printed 405,438,868); FY2021 308,848 + 5,976 + 2,174 = 316,998 (printed "
    "316,997,557). CVA is printed as \"-\" in all three years and is recorded as 0.\n"
)

P3_VS_NOTE28_BASIS_NOTE = (
    "BASIS DIFFERENCE - DO NOT CROSS-DIVIDE THESE SHEETS. The capital AMOUNTS, LCR, NSFR and RWA Breakdown on "
    "this workbook come from the Bank's standalone Pillar 3 document, whereas the CET1/Tier 1/Total Capital "
    "RATIOS, the Leverage Ratio and the aggregate Total RWAs come from the statutory accounts' \"Capital risk "
    "management (unaudited)\" note (Note 28). For the same year-ends the two sources genuinely disagree, and "
    "each is internally consistent on its own basis:\n"
    "  FY2025 - Pillar 3: capital 108,444,112 / RWA 502,801,056 / ratio 21.6% / leverage 17.29%. "
    "Note 28: RWA 517,644,568 / ratio 20.5% / leverage 16.9%.\n"
    "  FY2024 - Pillar 3: capital 104,741,303 / RWA 492,924,960 / ratio 21.25% / leverage 16.56%. "
    "Note 28: RWA 488,424,781 / ratio 20.9% / leverage 16.1%.\n"
    "(Pillar 3's own figures tie exactly: 108,444,112 / 502,801,056 = 21.57%, and its OV1 categories sum "
    "precisely to its own total in both years.) The Bank does not explain the difference in either document. "
    "The two bases are kept on separate sheets rather than blended, and the ratio/leverage/Total RWAs sheets "
    "were deliberately NOT overwritten with the Pillar 3 values, because those sheets carry all 5 years "
    "FY2021-FY2025 on one consistent Note 28 basis and substituting 2 years would silently break that series. "
    "Dividing a capital amount from one sheet by an RWA figure from another will not reproduce either "
    "published ratio.\n"
    "RE-VERIFIED 2026-09-15 (RWA cross-sheet sweep - do not re-flag): a sweep comparing every bank's Total "
    "RWAs sheet against its own RWA Breakdown total flagged KEXIM FY2024 (488,424,781 vs 492,924,960, a 0.9% "
    "gap). The Total RWAs figure was re-read straight from the source image rather than from any cached "
    "value: the FY2025 Companies House filing (image-only, OCR of the capital risk management note page) "
    "prints the table 'Capital, leverage and Risk Weighted Assets (RWA)' with 'RWA (£) 517,644,568 "
    "488,424,781' and CET1/T1/Total ratios of 20.5% (2025) and 20.9% (2024). Both sides of the gap are "
    "therefore correctly transcribed and it is NOT the credit-risk-subtotal defect seen at Redwood and Ghana "
    "International - the Pillar 3 breakdown already contains credit + market + operational and foots exactly "
    "to its own printed total. Note also that Note 28's RWA is LOWER than Pillar 3's while its ratio is also "
    "LOWER, which is only possible if the two bases differ in capital as well as RWA - further confirmation "
    "these are two genuinely different measurements rather than one wrong one. Neither figure is to be "
    "changed to make the two sheets agree."
)

RATIO_NOTE = (
    "Disclosed as its own line in the Bank's \"Capital risk management (unaudited)\" note's table \"Capital, "
    "leverage and Risk Weighted Assets ('RWA')\", which lists \"CET1 ratio\", \"T1 capital ratio\" and \"Total "
    "capital ratio\" as three separate rows carrying the same percentage in every one of the 5 years - so CET1 "
    "= Tier 1 = Total Capital Ratio here is the Bank's own explicit disclosure, not an assumption (consistent "
    "with no AT1 or Tier 2 instruments being disclosed in any year). The same table also states each ratio's "
    "PRA minimum (CET1 4.5%, T1 6%, Total 8%, leverage 5%). The Strategic Report's 'Review of the business' "
    "section separately narrates the same combined figure each year, which independently corroborates it. "
    "CORRECTION (2026-09-12 re-audit): this note was previously recorded as not existing - the earlier passes "
    "over these image-only filings identified Note 28 as an unrelated Country-by-Country Reporting disclosure "
    "and concluded no capital-management note was present. Full page-image OCR of all 5 filings found the "
    "capital note in every year, which is also the source of the now-populated Tier 1 Ratio, Leverage Ratio "
    "and Total RWAs sheets."
)

P3_CAPITAL_AMOUNT_NOTE = (
    "FY2025/FY2024 added 2026-09-15 from the Bank's own standalone Pillar 3 document (section 4 \"Own Funds\" "
    "capital-resources table, p.22, cross-confirmed against the UK KM1 template, p.38). This closes a real "
    "gap: the statutory accounts' Note 28 discloses capital RATIOS but never a capital AMOUNT, so no earlier "
    "pass could source these. CET1 = Tier 1 = Total capital exactly, as disclosed rather than assumed - the "
    "Own Funds table shows \"Additional Tier 1 capital\" and \"Total Tier 2 capital\" as \"-\" in both years, "
    "so all three tiers are the same figure.\n\n"
    "FY2023/FY2022/FY2021 added 2026-09-15 from the FY2023, FY2022 and FY2021 editions of the same document, "
    "each from its own section 4 \"Own Funds\" table. The prior statement that these years must remain blank "
    "because only the FY2025 edition could be obtained is SUPERSEDED - all three editions were retrieved from "
    "the Bank's own site; see the route note below. CET1 = Tier 1 = Total regulatory capital in these years "
    "too, disclosed rather than assumed: \"Additional Tier 1 capital\", \"Subordinated loan\" and \"Total Tier "
    "2 capital\" are each printed as \"-\", and \"Deductions for non-qualifying items\" is also \"-\", in all "
    "three editions. PRECISION LIMIT: these three editions disclose capital in £'000 (96,729 / 94,989 / "
    "100,630), where the FY2025 edition gives whole pounds - so the FY2021-FY2023 amounts are accurate to "
    "+/-£500 and are not directly comparable at sub-£1,000 precision with FY2024/FY2025.\n\n"
    + P3_EARLIER_EDITIONS_SOURCES + "\n"
    + P3_VS_NOTE28_BASIS_NOTE
)

metric(
    "CET1 Capital", "GBP",
    [("Common Equity Tier 1 (CET1) capital", P3_CAPITAL_AMOUNT)],
    P3_SOURCES,
    note=P3_CAPITAL_AMOUNT_NOTE,
)

metric(
    "CET1 Ratio", "%",
    [("CET1 ratio", CAPITAL_RATIO)],
    CAPITAL_NOTE_SOURCES,
    note=RATIO_NOTE,
)

metric(
    "Tier 1 Capital", "GBP",
    [("Tier 1 capital", P3_CAPITAL_AMOUNT)],
    P3_SOURCES,
    note=P3_CAPITAL_AMOUNT_NOTE,
)

metric(
    "Tier 1 Ratio", "%",
    [("T1 capital ratio", CAPITAL_RATIO)],
    CAPITAL_NOTE_SOURCES,
    note=RATIO_NOTE,
)

metric(
    "Total Capital", "GBP",
    [("Total regulatory capital", P3_CAPITAL_AMOUNT)],
    P3_SOURCES,
    note=P3_CAPITAL_AMOUNT_NOTE,
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", CAPITAL_RATIO)],
    CAPITAL_NOTE_SOURCES,
    note=RATIO_NOTE,
)

metric(
    "Total RWAs", "GBP",
    [("Risk Weighted Assets (RWA)", RWA)],
    CAPITAL_NOTE_SOURCES,
    note="Disclosed as the \"RWA (£)\" row of the Bank's own \"Capital, leverage and Risk Weighted Assets\" "
         "table in its Capital risk management note, in whole pounds (not £'000), for every year FY2021-FY2025. "
         "Only this aggregate figure is given - the note carries no split by risk category (credit / market / "
         "operational / CVA). Each year's figure is cross-confirmed against the following year's own "
         "prior-year comparative column.\n"
         "This sheet is the Note 28 statutory-accounts basis. The RWA Breakdown sheet is the Pillar 3 basis "
         "and its Total does NOT equal this sheet in any overlapping year (FY2025 502,801,056 vs 517,644,568; "
         "FY2024 492,924,960 vs 488,424,781) - see that sheet's basis note. Re-verified 2026-09-15 by OCR of "
         "the FY2025 filing's capital note, which prints 'RWA (£) 517,644,568 488,424,781'; both sheets are "
         "correct on their own basis and must not be reconciled.\n"
         + P3_VS_NOTE28_BASIS_NOTE,
)

# UK OV1 category breakdown, FY2025/FY2024 - recovered 2026-09-15 from the
# standalone Pillar 3 document (p.26). Both years' categories sum EXACTLY to that
# table's own Total row (FY2025: 486,313,006 + 1,897,575 + 14,590,475 =
# 502,801,056; FY2024: 480,244,922 + 332,038 + 12,348,000 = 492,924,960).
# Counterparty credit risk, settlement risk, securitisation and CVA are all
# printed blank in the source - the Bank has no such exposures - so they are
# omitted rather than shown as zero.
# NOTE: this Total is the Pillar 3 basis and so does NOT equal the Total RWAs
# sheet's Note 28 figure for the same year-ends - see the basis note below.
# TAXONOMY NOTE - the two vintages of this document split credit risk
# differently, so the rows are kept separate rather than mapped onto each other.
# The FY2025 edition uses the UK OV1 template, which reports "credit risk
# (excluding CCR)". The FY2021-FY2023 editions predate that template and use the
# Bank's own "Minimum Capital Requirement (8%)" table (section 5.2), which
# reports credit and counterparty credit risk as a single combined line. CVA is
# disclosed as nil ("-") in all three of those years, so nothing is hidden in the
# combination - but the labels are not interchangeable and are not presented as
# though they were.
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR) - standardised approach",
     {"FY2025": 486313006, "FY2024": 480244922}),
    ("DATA", "Credit and counterparty credit risk (standardised approach, combined as disclosed)",
     {"FY2023": 419544000, "FY2022": 396552000, "FY2021": 308848000}),
    ("DATA", "Position, foreign exchange and commodities risks (market risk) - standardised approach",
     {"FY2025": 1897575, "FY2024": 332038,
      "FY2023": 1491000, "FY2022": 273000, "FY2021": 2174000}),
    ("DATA", "Operational risk - basic indicator approach",
     {"FY2025": 14590475, "FY2024": 12348000,
      "FY2023": 10128000, "FY2022": 8614000, "FY2021": 5976000}),
    ("DATA", "Credit valuation adjustment risk - standardised approach",
     {"FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Total risk weighted exposure amount (Pillar 3 basis)",
     {"FY2025": 502801056, "FY2024": 492924960,
      "FY2023": 431163079, "FY2022": 405438868, "FY2021": 316997557}),
]

bw.add_rwa_breakdown_sheet(
    title="KEXIM Bank (UK) Limited — RWA Breakdown",
    subtitle="Pillar 3 basis, GBP, all five years. FY2025/FY2024 from the UK OV1 template; FY2023-FY2021 from "
             "each year's own section 5.2 'Minimum Capital Requirement (8%)' table, which combines credit and "
             "counterparty credit risk into one line - see source note. Also explains why this total differs "
             "from the Total RWAs sheet.",
    rows=rwa_breakdown_rows,
    sources_text=P3_SOURCES + "\n\n"
    + "CORRECTION (2026-09-15): this sheet previously stated that no category-level RWA split was published "
      "for this bank. That was wrong - it was an ACCESS gap, not a non-disclosure. The Bank publishes a "
      "category split every year; it simply sits on the parent's Korean domain behind a cookie challenge.\n\n"
    + "SECOND CORRECTION (2026-09-15, same day): an earlier version of this note recorded FY2021-FY2023 as "
      "\"BACKFILL ATTEMPTED AND BLOCKED - USER-ACTIONABLE\", on the reasoning that the host was geo-restricted "
      "or TLS-broken, that Wayback held no usable capture, and that download URLs embedded unguessable "
      "server-generated timestamp filenames. That diagnosis was WRONG and all three years are now filled. The "
      "host runs an ordinary cookie challenge: the first request to /site/uk returns HTTP 302 with Location "
      "pointing back at /site/uk while setting a cookie, so a curl without a cookie jar follows the redirect "
      "indefinitely and appears to hang. Supplying a cookie jar returns HTTP 200 on the first retry. The "
      "documents are indexed on the \"What's New\" board at /uk/HPHYEU015M01 - not under /site/uk - with "
      "stable attachment ids, so the 'unguessable filename' obstacle did not exist either. No manual browser "
      "fetch was required. The lesson worth keeping: a redirect-to-self plus Set-Cookie is a cookie challenge, "
      "not a block, and 'it hangs' is not evidence that a document is unobtainable.\n\n"
      "THE STATUTORY ACCOUNTS STILL CANNOT SUBSTITUTE, and nothing here is derived from them. The FY2023 "
      "filing (Companies House, 87pp, scanned image-only) carries only an aggregate \"RWA (GBP) 431,163,080 "
      "(2023) / 405,644,306 (2022)\" with no category split. Note that the Pillar 3's own FY2023 total "
      "(431,163,079) sits £1 from the statutory figure and its FY2022 total (405,438,868) differs from the "
      "statutory 405,644,306 by £205,438 - a further instance of the basis difference described below.\n\n"
    + P3_EARLIER_EDITIONS_SOURCES + "\n"
    + P3_VS_NOTE28_BASIS_NOTE,
    first_col_width=90,
    source_height=300,
    # Whole pounds, not £'000 - matching the Total RWAs sheet's "GBP" unit and
    # the source's own presentation (the OV1 table prints full amounts).
    unit_suffix=" (GBP)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", LEVERAGE_RATIO)],
    CAPITAL_NOTE_SOURCES,
    note="Disclosed as the \"Leverage ratio\" row of the Bank's own \"Capital, leverage and Risk Weighted "
         "Assets\" table in its Capital risk management note, against a stated PRA minimum of 5% (the minimum "
         "column is blank in the FY2021 and FY2022 filings' own printing of the table, but the ratio itself is "
         "given in both). Each year's figure is cross-confirmed against the following year's own prior-year "
         "comparative column.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio", P3_LCR)],
    P3_SOURCES + "\n\n" + P3_EARLIER_EDITIONS_SOURCES,
    note="FY2025/FY2024 added 2026-09-15 from the UK KM1 template's \"Liquidity coverage ratio (%)\" line "
         "(row 17, p.38) in the Bank's own standalone Pillar 3 document. No LCR figure appears anywhere in the "
         "statutory accounts, so this was previously blank for every year. The FY2025 figure is the "
         "31 December 2025 year-end position: it equals the Q4 column of the Bank's own quarterly LCR table "
         "(section 3.5.3.1, p.19 - liquidity buffer GBP13,356,306 / net outflows GBP971,234 = 1,375%), and the "
         "same HQLA and net-outflow amounts appear on the KM1 rows immediately above the ratio. Note the KM1 "
         "labels its HQLA row \"Weighted value -average\" while the figure itself is the year-end one; shown "
         "here as the Bank presents it. The other quarters of FY2025 were 1,017% (Q1), 891% (Q2) and 1,868% "
         "(Q3) - a volatile ratio driven by a small and lumpy net-outflow denominator.\n\n"
         "FY2023 (893%), FY2022 (189%) and FY2021 (349%) added 2026-09-15 from the corresponding editions of "
         "the same document - the \"Liquid Coverage Ratio\" / \"Liquidity Coverage Ratio\" tile of each "
         "edition's \"Key metrics\" dashboard on p.3. The prior statement that these years must remain blank "
         "because only the FY2025 edition could be obtained is SUPERSEDED; see the route note. Each year is "
         "cross-confirmed by the following edition's own comparative on the same tile (the FY2022 edition "
         "prints \"2021: 349%\" and the FY2023 edition prints \"2022: 189%\"). BASIS CAVEAT: these three are "
         "year-end positions from the Key metrics dashboard, whereas FY2024/FY2025 come from the UK KM1 "
         "template - and this Bank's LCR is genuinely volatile quarter to quarter on a small net-outflow "
         "denominator, so the year-on-year steps in this row should not be read as smooth trend.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", P3_NSFR)],
    P3_SOURCES + "\n\n" + P3_EARLIER_EDITIONS_SOURCES,
    note="FY2025/FY2024 added 2026-09-15 from the UK KM1 template's \"NSFR ratio (%)\" line (row 20, p.38) in "
         "the Bank's own standalone Pillar 3 document; no NSFR figure appears anywhere in the statutory "
         "accounts. Each year ties to its own available/required stable funding rows on the same table "
         "(FY2025: GBP492,037,595 / GBP442,729,289; FY2024: GBP530,220,476 / GBP425,889,742). The Bank "
         "attributes the year-on-year fall from 124.5% to 111.1% to \"differences in residual maturity\".\n\n"
         "FY2023 (113.6%) and FY2022 (114.6%) added 2026-09-15 from the FY2023 edition's \"Key metrics\" "
         "dashboard, p.3, which prints the NSFR tile as \"113.6% / 2022: 114.6%\". The prior statement that "
         "these years must remain blank because only the FY2025 edition could be obtained is SUPERSEDED; see "
         "the route note.\n\n"
         "FY2021 IS STRUCTURALLY ABSENT, NOT MISSING. The FY2021 and FY2022 editions were both retrieved and "
         "searched in full: neither contains a single occurrence of \"NSFR\" or \"net stable funding\" "
         "anywhere. The FY2023 edition is the first to carry the metric, and it introduces it complete with a "
         "FY2022 comparative. That is precisely the pattern PRA PS17/21 predicts - the UK had no NSFR "
         "requirement or disclosure template before 1 January 2022, and the four-quarter-average rule pushed "
         "first required disclosure to after 1 January 2023. No FY2021 NSFR should be expected to exist.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    CAPITAL_NOTE_SOURCES + "\n\n" + P3_SOURCES,
    per_note={"MREL Ratio": (
        "Not disclosed, and not applicable to this entity. MREL is not mentioned anywhere in any of the 5 "
        "Annual Reports, nor anywhere in the Bank's own standalone Pillar 3 document obtained 2026-09-15 "
        "(searched in full: zero occurrences of \"MREL\" or \"minimum requirement for own funds\"). KEXIM Bank "
        "(UK) Limited is a wholly-owned subsidiary of a foreign parent and is not a UK resolution entity, so "
        "no MREL requirement is set for it."
    )},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 604228751, "FY2024": 586007552, "FY2023": 524250678, "FY2022": 521204305, "FY2021": 386490055}),
        ("Loans and advances to customers", {"FY2025": 272874882, "FY2024": 255692188, "FY2023": 221939171, "FY2022": 219863026, "FY2021": 162324430}),
        ("Borrowings from credit institutions", {"FY2025": 490903342, "FY2024": 475810294, "FY2023": 418559481, "FY2022": 406105536, "FY2021": 285675937}),
        ("Total shareholders' funds", {"FY2025": 108444112, "FY2024": 104741303, "FY2023": 100629950, "FY2022": 94988669, "FY2021": 96728571}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 9779308, "FY2024": 7747862, "FY2023": 5732137, "FY2022": 6156637, "FY2021": 4153289}),
        ("Administrative expenses", {"FY2025": -4398250, "FY2024": -3657484, "FY2023": -2628149, "FY2022": -2806180, "FY2021": -2489926}),
        ("Profit on ordinary activities after tax", {"FY2025": 2537458, "FY2024": 2801238, "FY2023": 2365638, "FY2022": 2517434, "FY2021": 1248398}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 104741303, "FY2024": 100629950, "FY2023": 94988669, "FY2022": 96728571, "FY2021": 96962553}),
        ("Profit for the year", {"FY2025": 2537458, "FY2024": 2801238, "FY2023": 2365638, "FY2022": 2517434, "FY2021": 1248398}),
        ("Other movements, net", {"FY2025": 1165351, "FY2024": 1310115, "FY2023": 3275643, "FY2022": -4257336, "FY2021": -1482380}),
        ("Closing equity", {"FY2025": 108444112, "FY2024": 104741303, "FY2023": 100629950, "FY2022": 94988669, "FY2021": 96728571}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 / Total Capital Ratio", CAPITAL_RATIO),
    ],
    note="No cash flow summary or chart is shown here: KEXIM Bank (UK) Limited takes the FRS 101 cash-flow-"
         "statement exemption every year (see the Cash Flow Statement sheet). Balance Sheet, Profit & Loss and "
         "Statement of Changes in Equity headline blocks are all fully populated below, sourced from the Bank's "
         "own primary financial statements (not just the Strategic Report). No dedicated Pillar 3 document is "
         "published by this entity, and a thorough re-check of every note in all 5 Annual Reports during this "
         "ST-024 build confirmed no RWA or capital-management figure exists anywhere - the only capital metric "
         "disclosed anywhere is a single combined CET1/Total Capital adequacy ratio, stated once per year in each "
         "Annual Report's Strategic Report - all 5 years fully cross-checked and consistent, no restatements.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/KEXIM BANK UK FINANCIALS.xlsx")
