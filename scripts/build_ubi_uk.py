import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018"]  # most recent first, year ended 31 March
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2018": "FY2017", "FY2019": "FY2018", "FY2020": "FY2019", "FY2021": "FY2020",
             "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024",
             "FY2026": "FY2025"}

# ---------------------------------------------------------------
# FX conversion (Union Bank of India (UK) Limited reports in USD; converting
# to £ per this project's established methodology - see build_smbc.py/
# build_zenith.py precedent). Same 31 March year-ends as SMBC Bank
# International, so the same Bank of England GBP/USD spot/average rates
# apply (via poundsterlinglive.com's published archive), £1 = $X - the
# FY2017/2018/2019/2020 rates below are the same figures already used in
# build_smbc.py (same rate table, same source).
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2017": 1.2507,  # 31 Mar 2017 - only used for FY2018's opening cash balance
    "FY2018": 1.4033,
    "FY2019": 1.3030,
    "FY2020": 1.2403,
    "FY2021": 1.3796,
    "FY2022": 1.3162,
    "FY2023": 1.2364,
    "FY2024": 1.2632,
    "FY2025": 1.2910,
    "FY2026": 1.3188,
}
FX_AVG = {
    "FY2018": 1.3390,
    "FY2019": 1.3102,
    "FY2020": 1.2713,
    "FY2021": 1.3193,
    "FY2022": 1.3617,
    "FY2023": 1.2043,
    "FY2024": 1.2581,
    "FY2025": 1.2775,
    "FY2026": 1.3411,
}


def flow(usd):
    """Flow (cash flow statement line item) figures, £'000, at that year's average rate.
    Input values are already in USD '000 (per the source documents), so no /1000 here."""
    return {y: round(v / FX_AVG[y], 1) for y, v in usd.items()}


def stock(usd):
    """Point-in-time (balance/capital) figures, £'000, at that year's period-end spot rate.
    Input values are already in USD '000 (per the source documents), so no /1000 here."""
    return {y: round(v / FX_SPOT[y], 1) for y, v in usd.items()}


def opening_cash(usd):
    """Opening cash balance, £'000 - uses the PRIOR year's period-end spot rate (it's
    the same balance as that prior year's closing figure, so must convert identically).
    Input values are already in USD '000, so no /1000 here."""
    return {y: round(v / FX_SPOT[PREV_YEAR[y]], 1) for y, v in usd.items()}


def _stock1(v, y):
    """Single-value point-in-time conversion (see stock() for the dict form) - used by the
    ST-035 Balance Sheet/Equity/Asset Quality/RWA Breakdown sheets, which build up their
    year-dicts from per-year USD dicts rather than one dict-per-line-item."""
    return round(v / FX_SPOT[y], 1)


def _flow1(v, y):
    """Single-value flow conversion (see flow() for the dict form) - used by the ST-035
    Income Statement/Equity sheets."""
    return round(v / FX_AVG[y], 1)


# ---------------------------------------------------------------
# Source documents
# ---------------------------------------------------------------
BASE = "https://www.unionbankofindiauk.co.uk/Portals/0/pdf"
AR2026_URL = f"{BASE.rsplit('/pdf', 1)[0]}/Annual%20Accounts%20UBIUK%202026%20Signed_1.pdf"
AR2025_URL = f"{BASE}/Annual_report_UBI_UK_signed_31-03-2025.pdf"
AR2024_URL = f"{BASE}/Signed_UBI_UK_Annual_Report_28_05.pdf"
AR2023_URL = f"{BASE}/Annual_Report_March_2023_with_Final_Audit_report_24052023-signed.pdf"
AR2022_URL = f"{BASE}/Financial_Statements%20_31-03-2022.pdf"
AR2020_URL = f"{BASE}/Financial_Statements_UBI_UK_Mar_20_(Final)_Signed.pdf"
AR2019_URL = f"{BASE}/Annual_report_-_31_03_19_Signed..pdf"
AR2018_URL = f"{BASE}/Financial_Accounts_31_03_2018.pdf"

P3_2025_URL = f"{BASE}/Final_Pillar_3_Disclosure-31-03-2025.pdf"
P3_2024_URL = f"{BASE}/Pillar_3_Disclosures_2024.pdf"
P3_2023_URL = f"{BASE}/Pillar_3_Disclosure_2023.pdf"
P3_2022_URL = f"{BASE}/Pillar_III%20_Disclosures_2021_22.pdf"
P3_2021_URL = f"{BASE}/Pillar_III_%20Disclosures_(2020-21).pdf"
P3_2020_URL = f"{BASE}/Pillar_III_Disclosures_(2020)-Final.pdf"
P3_2019_URL = f"{BASE}/2019_Pillar_III_Disclosures_-_RCC_Approved.pdf"
P3_2018_URL = f"{BASE}/PIllar_3_Disclosures_31_03_2018.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Union Bank of India (UK) Limited (FRN 601551, Companies House 07653660) is an Indian-owned UK "
    "subsidiary bank (parent: Union Bank of India). Unlike other single-country Indian-subsidiary banks in this "
    "workbook series (ICICI Bank UK, State Bank of India UK - both skipped), this Bank does NOT take the FRS 101/102 "
    "cash-flow-statement exemption - it publishes a genuine Statement of Cash Flows every year. CET1 capital = "
    "Tier 1 capital in every year shown (no AT1 instruments); Total capital also equals CET1/Tier 1 from FY2022 "
    "onward (no Tier 2 instruments), but FY2021 Total capital ($115,017k) exceeds CET1/Tier 1 ($111,081k), implying "
    "the Bank held Tier 2 capital that year which had run off by FY2022. FY2021 cash flow figures are sourced from "
    "the FY2022 Annual Report's own comparative column (no dedicated FY2021 report was fetched), consistent with "
    "this project's practice of using the earliest practically available presentation of a year's figures. "
    "FY2018-FY2020 (added per HD-058, extending this workbook's floor back to FY2018, the Bank's confirmed "
    "historical floor) each use that year's own dedicated, originally-published Annual Report and Pillar 3 "
    "Disclosure, located on the Bank's own disclosures/financial-reports archive page and re-verified from the "
    "actual scanned PDFs. FY2018 predates the Bank's 1 April 2018 IFRS 9 transition (see ROUNDING/RESTATEMENT NOTE "
    "on the Balance Sheet sheet and the note on the Asset Quality sheet), so it has no IFRS 9 stage-based credit "
    "quality disclosure and no NSFR; its Income Statement/Balance Sheet/Cash Flow Statement also show a distinct "
    "'Operating lease' expense line and 'Deferred tax assets (net)' / 'Intra-group borrowings' items that the "
    "Bank's presentation later folded into other lines or paid off entirely (all reproduced here as originally "
    "presented, not restated to match the later years' line items)."
)

FX_NOTE = (
    "FX CONVERSION NOTE: Union Bank of India (UK) Limited reports in US Dollars. This workbook converts every $ "
    "amount to £, following the same methodology established for SMBC Bank International plc and Zenith Bank (UK) "
    "Limited: point-in-time/balance figures (capital, RWA, leverage exposure, HQLA, cash balances) use the Bank of "
    "England GBP/USD SPOT rate as at that fiscal year-end (31 March); flow figures (every cash flow statement line "
    "item) use the AVERAGE Bank of England rate over that fiscal year - both via poundsterlinglive.com's published "
    "Bank of England archive (same rate table as SMBC Bank International plc, which shares the same 31 March "
    "year-end; same table already used in build_smbc.py for its FY2017/FY2018/FY2019/FY2020 rates). Rates used "
    "(£1 = $X): 31 Mar 2017 spot 1.2507 (FY2018 opening cash only); FY2018 spot 1.4033 / average 1.3390; FY2019 "
    "spot 1.3030 / average 1.3102; FY2020 spot 1.2403 / average 1.2713; FY2021 spot 1.3796 / "
    "average 1.3193; FY2022 spot 1.3162 / average 1.3617; FY2023 spot 1.2364 / average 1.2043; FY2024 spot 1.2632 / "
    "average 1.2581; FY2025 spot 1.2910 / average 1.2775; FY2026 spot 1.3188 / average 1.3411. FY2026 RATE SOURCING (added 2026-09-15): the FY2026 pair was taken from the Bank of England's own Interactive Statistical Database rather than poundsterlinglive - series XUDLUSS (daily spot US$ into GBP): the spot is the 31 March 2026 daily rate (1.3188), and the average is the mean of the twelve month-end daily rates from 30 April 2025 to 31 March 2026 (1.3411). That aggregation was chosen because it reproduces the FY2018-FY2025 averages already carried above exactly (FY2018 1.3390, FY2019 1.3102, FY2020 1.2713, FY2022 1.3617, FY2023 1.2043, FY2024 1.2581) or to within 0.0001 (FY2025 1.2776 vs 1.2775); the one outlier is FY2021 (1.3180 computed vs 1.3193 carried, a 0.1% difference attributable to an Easter/holiday month-end date). A daily mean over the same window would give 1.3404 instead, so the FY2026 average carries roughly 0.05% of method uncertainty - immaterial at this scale but recorded here so the basis is reproducible. Every FY2026 spot rate is exact. All % ratios (CET1/Tier 1/Total Capital/Leverage/LCR/NSFR "
    "ratios) are shown EXACTLY as reported in USD and were NOT converted - a ratio is dimensionless and "
    "currency-invariant. This conversion was not explicitly requested for this specific bank but applied for "
    "consistency with the rest of the series (per the user's standing instruction on this batch of banks); flag if "
    "£'000 rather than the Bank's native US$'000 presentation is not what's wanted here."
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: this Bank's own statement presents 'Cash flows before changes in working capital' (or "
    "'...operating activities' in FY2021/FY2022) as the sum of the adjustment lines ONLY - it deliberately excludes "
    "'(Loss)/profit before tax for the year', which is carried forward separately and only folded in at the final "
    "'Net cash flows from/(used in) operating activities' total (verified: profit before tax + adjustments subtotal "
    "+ working capital change + loans/deposits movements = the operating total, exactly, in every year). A generic "
    "block-sum check that includes the profit-before-tax line together with the adjustment lines above that "
    "subtotal will therefore show an apparent mismatch equal to the profit/(loss) before tax figure - this is a "
    "structural feature of the source document's own layout, not a data error (also holds for FY2018-FY2020).\n\n"
    "FY2018-FY2020 PRESENTATION NOTE: these years' own Statements of Cash Flows classify 'repurchase agreements' "
    "movements and a single combined 'Proceeds from/(Repayment to) Intra-group borrowings' line within Operating "
    "and Financing activities respectively, but do not split intra-group borrowings into separate 'proceeds' and "
    "'repayment' rows the way FY2022/FY2023's own reports do, and do not disclose interest-received/interest-paid "
    "splits at all (all folded into the combined loans/deposits movement lines) - reproduced here exactly as each "
    "year's own report presents it. FY2019/FY2020 additionally show a 'Corporation tax credit/(charge) during the "
    "year' reconciling item (deferred tax movements) and, in FY2019 only, a one-off 'Impairment loss during "
    "transition period' ($907k) coinciding with the IFRS 9 transition impact of the same amount booked to opening "
    "retained earnings in the Statement of Changes in Equity - both figures are reproduced as the Bank's own "
    "report presents them; the coincidence in amount is not explained in the source and is not resolved here."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Union Bank of India (UK) Limited's own Statement of Cash Flows (converted from USD "
    "to £, see FX conversion note below):\n"
    f"FY2026: Annual Report and Financial Statements, year ended 31 March 2026, p.35 (Statement of Cash Flows) - {AR2026_URL}\n"
    f"FY2025: Annual Report and Financial Statements, year ended 31 March 2025, p.35 (Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements, year ended 31 March 2024, p.28 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements, year ended 31 March 2023, p.27 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements, year ended 31 March 2022, p.35 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: as presented in the FY2022 Annual Report's own comparative column (p.35) - {AR2022_URL}\n"
    f"FY2020: Financial Statements, year ended 31 March 2020, p.33 (Statement of Cash Flows) - {AR2020_URL}\n"
    f"FY2019: Annual Accounts, year ended 31 March 2019, p.26 (Statement of Cash Flows) - {AR2019_URL}\n"
    f"FY2018: Annual Accounts, year ended 31 March 2018, p.24 (Statement of Cash Flows) - {AR2018_URL}\n"
    "Note: FY2023's own report's FY2022 comparative figures for the operating/investing/financing subtotals differ "
    "from FY2022's own report (e.g. operating activities $(31,909)k restated vs $(30,053)k as originally reported) "
    "- a reclassification between activity categories, not a change to the overall cash movement (both agree the "
    "year-end balance was $5,170k). FY2022's own as-originally-reported figures are used throughout, per this "
    "project's convention of preferring each year's own report over a later restated comparative. FY2019's own "
    "report and FY2020's own report agree exactly on the FY2019 comparative figures shown in each (no restatement "
    "found between those two).\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + PRESENTATION_NOTE
)


def p3_sources():
    return (
        "YEAR-END: Union Bank of India (UK) Limited has a 31 MARCH financial year-end, not 31 December. Every "
        "'FYnnnn' column below is the year ENDED 31 March of that calendar year - so FY2026 means the twelve "
        "months to 31 March 2026, and the Pillar 3 disclosure behind each column is dated 31-03-nnnn. This "
        "matters for any cross-bank comparison in this series: the same FY label on a December-year-end bank "
        "covers a window nine months earlier, and the two are not directly comparable without that caveat. It "
        "also drives the NSFR/leverage phase-in timing, since the PRA's disclosure requirements commenced on "
        "calendar-year boundaries rather than on this Bank's reporting dates.\n\n"
        "Sources - Union Bank of India (UK) Limited Pillar 3 Disclosures (UK KM1 - Key metrics / prudential "
        "regulatory metrics table), converted from USD to £ where a $ amount (see FX conversion note on the Cash "
        "Flow Statement sheet; % ratios are unconverted):\n"
        f"FY2025: Pillar 3 Disclosure 2024-25, p.9 (UK KM1 - Key metrics) - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosure 2023-24, p.9 (UK KM1 - Key metrics) - {P3_2024_URL}\n"
        f"FY2023: Pillar III Disclosure 2022-23, p.9 (UK KM1 - Key metrics) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosure 2022, p.28 (3.4 Bank's prudential regulatory metrics) - {P3_2022_URL}\n"
        f"FY2021: as presented in the FY2022 Pillar 3 Disclosure's own comparative column (p.28) - {P3_2022_URL}\n"
        f"FY2020: Pillar 3 Disclosure 2020, p.23 (3.4 Bank's prudential regulatory metrics) - {P3_2020_URL}\n"
        f"FY2019: Pillar III Disclosures 2019, p.13 (3.1.2 Bank's prudential regulatory metrics) - {P3_2019_URL}\n"
        f"FY2018: Pillar 3 Disclosures 2018, p.10 (3.1.2 Bank's prudential regulatory metrics) - {P3_2018_URL}\n"
        "\nFY2026 IS DELIBERATELY BLANK ON EVERY PILLAR 3 SHEET (verified 2026-09-15): the Bank's own "
        "disclosures/financial-reports page now lists 'Financial Accounts 31-03-2026' but its most recent "
        "Pillar 3 entry is still 'Pillar 3 Disclosure 31-03-2025', and every FY2026 filename permutation "
        "tried under /Portals/0/pdf/ returns the site's 82,647-byte soft-404 HTML page (content-type "
        "text/html) rather than a document, while the FY2025 file returns a real 2.3MB application/pdf. The "
        "FY2026 Annual Report itself contains NO quantitative capital disclosure: its Capital Risk note "
        "(p.67) is narrative only, and the Strategic Report (p.6) says the Capital Adequacy Ratio, LCR and "
        "NSFR 'remained well above regulatory requirements' without giving a single figure. Nothing on "
        "these sheets has been derived or back-solved from the audited equity figures - FY2026 should become "
        "fillable once the FY2026 Pillar 3 Disclosure is published.\n"
        "Re-checked independently later the same day and unchanged. The page at "
        "https://www.unionbankofindiauk.co.uk/disclosures/financial-reports is this entity's full document "
        "index: it runs from 2015 to 2026 and pairs an accounts document with a Pillar 3 document for every "
        "year EXCEPT 2026, where 'Financial Accounts 31-03-2026' appears with no Pillar 3 alongside it. Note "
        "the FY2026 accounts sit at /Portals/0/ rather than the /Portals/0/pdf/ used by every prior year, so "
        "FY2026 Pillar 3 permutations were re-tried against BOTH paths; all returned the same soft-404.\n"
        "THIRD INDEPENDENT RE-VERIFICATION (2026-09-15, maximum-effort sweep, prior verdict deliberately "
        "treated as unproven): confirmed again by three routes. (1) The live index was re-fetched with a "
        "browser user-agent and cookie jar and still lists 'Final_Pillar_3_Disclosure-31-03-2025.pdf' as the "
        "newest Pillar 3. (2) Six further FY2026 filename permutations were tried across both Portals paths; "
        "every one returns the identical 82,647-byte soft-404 HTML body, which is the site's signature for a "
        "missing file (a real PDF on this host returns megabytes - the FY2024 annual report returns "
        "4,761,221 bytes from the same directory, so the path and credentials are demonstrably working). "
        "(3) A full Wayback CDX sweep of the whole domain with no filter returns ten Pillar 3 PDFs, the newest "
        "being Pillar_3_Disclosures_2024.pdf - no FY2025 or FY2026 edition has ever been archived. One "
        "false lead was chased and cleared: 'Signed_UBI_UK_Annual_Report_28_05.pdf', an undated filename on "
        "the index, is a real 4.7MB PDF but its cover reads 'For the year ended on 31 March 2024' - it is the "
        "FY2024 annual report, not an unlabelled FY2026 document. The gap is genuine and is a publication "
        "lag, not an access failure.\n"
        "FOURTH INDEPENDENT CHECK (2026-09-15, separate session, prior verdicts again treated as unproven) - "
        "UNCHANGED, and now stated as a precise enumerated count rather than a description. The index page was "
        "re-fetched and every PDF link on it parsed out. It carries exactly ELEVEN Pillar 3 documents, an "
        "unbroken annual series with no missing year: 31-03-2015, 31-03-2016, 31-03-2017, 31-03-2018, "
        "31-03-2019, 31-03-2020, 31-03-2021, 31-03-2022, 31-03-2023, 31-03-2024 and 31-03-2025. There is no "
        "twelfth. Because the series is unbroken, its stopping point is informative rather than ambiguous: "
        "this Bank does not skip Pillar 3 years, so FY2026's absence reads as not-yet-published, not as a "
        "policy change or an SDDT opt-in. The FY2026 ANNUAL ACCOUNTS are already on that same index "
        "('Annual Accounts UBIUK 2026 Signed_1.pdf', which downloads as a real 2.7MB PDF), so the index is "
        "demonstrably current for FY2026 - the Pillar 3 is simply behind it, exactly the lag the Bank's own "
        "pattern predicts. THIS IS THE ONE RE-CHECKABLE NEGATIVE IN THIS WORKBOOK: re-fetch "
        "https://www.unionbankofindiauk.co.uk/disclosures/financial-reports and look for a 'Pillar 3 "
        "Disclosure 31-03-2026' entry; when it appears, every FY2026 Pillar 3 cell here becomes fillable in "
        "one pass. Contrast this with RCI Bank UK's FY2020-FY2022, which is a permanent negative because the "
        "documents were never produced at all.\n"
        "The FY2026 Annual Report was ALSO re-read in full this session to confirm nothing fillable was left "
        "in it, rather than trusting the earlier read. Its only capital and liquidity statements are "
        "narrative: the Strategic Report says 'Capital Adequacy Ratio remained well above regulatory "
        "requirements' and that 'both the Liquidity Coverage Ratio (LCR) and Net Stable Funding Ratio (NSFR) "
        "remained well within Board-approved thresholds', neither with a figure; the Capital Risk note (p.67) "
        "says only that the Bank 'has had surplus capital over and above the capital required as per the ICG "
        "during the year' and that 'The Bank's regulatory capital is categorised into Tier one capital, which "
        "includes ordinary share capital, and retained earnings as shown in statement of change in equity.' "
        "That last sentence is a pointer to the equity statement, NOT a regulatory capital disclosure - "
        "reading a Tier 1 figure across from book equity would be a back-solve and is expressly not done "
        "here. A full-text scan of the report for CET1, Tier 1, Tier 2, RWA, risk-weighted, own funds, "
        "capital ratio, leverage ratio, LCR, NSFR and MREL returns no quantitative disclosure of any of them."
    )


bw = BankWorkbook(bank_name="Union Bank of India (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="0F5B78")

# ---------------------------------------------------------------
# ST-035: Balance Sheet, Profit & Loss, Statement of Changes in Equity,
# Asset Quality, RWA Breakdown. All figures are Union Bank of India (UK)
# Limited's own reported USD'000 figures, converted to £ using the same
# stock()/flow() methodology as the Cash Flow Statement sheet - see
# FX_NOTE. Each year uses that year's own originally-published report
# (not a later restated comparative) except FY2021, which - consistent
# with the existing Cash Flow Statement/Pillar 3 sheets in this workbook
# - is sourced from the FY2022 Annual Report/Pillar 3 Disclosure's own
# comparative column (no dedicated FY2021 report exists).
# ---------------------------------------------------------------
STATEMENTS_RESTATEMENT_NOTE = (
    "RESTATEMENT NOTE: the FY2024 Annual Report's own FY2023 comparative Balance Sheet is labelled '(Restated)' and "
    "differs from FY2023's own originally-published figures (e.g. Total Assets $482,454k restated vs $483,606k as "
    "originally reported in the FY2023 Annual Report; Total Liabilities $368,617k restated vs $369,770k as "
    "originally reported) - the underlying reclassification is not explained in either report. Per this project's "
    "convention of preferring each year's own report over a later restated comparative, FY2023's Balance Sheet/"
    "Profit & Loss/Equity figures throughout this workbook use the FY2023 Annual Report's own originally-published "
    "figures, not the FY2024 report's restated comparative.\n\n"
    "ROUNDING NOTE: the Bank's own Statement of Changes in Equity closing balances for FY2022 and FY2023 differ from "
    "that same year's own Balance Sheet Total equity/Accumulated losses figures by exactly $1k (e.g. FY2022 ladder "
    "closing Accumulated losses $(33,446)k vs Balance Sheet $(33,447)k; FY2023 ladder closing Total equity $113,838k "
    "vs Balance Sheet $113,837k) - a genuine rounding artefact within the Bank's own source documents, not a "
    "transcription error here. The Balance Sheet's own figures are used as each year's authoritative Total equity; "
    "the equity ladder's own movement figures (profit/loss, OCI) are used for that year's movements; the resulting "
    "$1k gap is absorbed into the 'Effect of GBP/USD translation' reconciling row alongside the FX rate-differential "
    "effect (see FX_NOTE) rather than silently adjusted away.\n\n"
    "FY2018-FY2020 PRESENTATION NOTE: these years' own Balance Sheets show a 'Deferred tax assets (net)' asset "
    "line and an 'Intra-group borrowings' liability line, both absent from FY2021 onward (deferred tax assets "
    "appear to have run off; intra-group borrowings were repaid in full during FY2020 - see the Cash Flow "
    "Statement's 'Repayment to Intra-group borrowings' line). They also show no separate 'Provisions' line for "
    "FY2018/FY2019 (provisions are folded into 'Other liabilities' those two years); FY2020's own report is the "
    "first to break 'Provisions' ($112k) out of 'Other liabilities' - confirmed by cross-checking FY2020's own "
    "report's FY2019 comparative ('Provisions' $98k + 'Other liabilities' $632k = $730k), which reconciles exactly "
    "to FY2019's own report's single combined $730k 'Other liabilities' figure (used here, per this project's "
    "convention of preferring each year's own originally-published presentation)."
)

BS_SOURCES = (
    "Sources - all figures are Union Bank of India (UK) Limited's own Statement of Financial Position (converted "
    "from USD to £, see FX conversion note below):\n"
    f"FY2026: Annual Report and Financial Statements, year ended 31 March 2026, p.32-33 (Statement of Financial Position) - {AR2026_URL}\n"
    f"FY2025: Annual Report and Financial Statements, year ended 31 March 2025, p.32-33 (Statement of Financial Position) - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements, year ended 31 March 2024, p.25-26 (Statement of Financial Position) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements, year ended 31 March 2023, p.24-25 (Statement of Financial Position) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements, year ended 31 March 2022, p.32-33 (Statement of Financial Position) - {AR2022_URL}\n"
    f"FY2021: as presented in the FY2022 Annual Report's own comparative column (p.32-33) - {AR2022_URL}\n"
    f"FY2020: Financial Statements, year ended 31 March 2020, p.30-31 (Statement of Financial Position) - {AR2020_URL}\n"
    f"FY2019: Annual Accounts, year ended 31 March 2019, p.24 (Statement of Financial Position) - {AR2019_URL}\n"
    f"FY2018: Annual Accounts, year ended 31 March 2018, p.22 (Statement of Financial Position) - {AR2018_URL}\n\n"
    + "FY2025 RECLASSIFICATION, not adopted (noted 2026-09-15): the FY2026 Annual Report's own FY2025 "
      "comparative column moves $105k from 'Other assets' to 'Intangible assets' (restated FY2025: "
      "intangibles $123k, other assets $1,896k; as originally reported: $18k and $2,001k). Total assets are "
      "unchanged at $481,017k either way. FY2025 is left as that year's own report originally presented it, "
      "per this project's standing convention of preferring each year's own report over a later restated "
      "comparative - so the FY2025 and FY2026 columns of those two lines are not strictly like-for-like. "
      "Every other FY2025 comparative in the FY2026 report (Income Statement, Statement of Financial "
      "Position, Statement of Changes in Equity, Statement of Cash Flows and the IFRS 9 stage tables) was "
      "checked line by line and agrees exactly with the figures already carried here - no other restatement.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + STATEMENTS_RESTATEMENT_NOTE
)

IS_SOURCES = (
    "Sources - all figures are Union Bank of India (UK) Limited's own Income Statement / Statement of Other "
    "Comprehensive Income (converted from USD to £, see FX conversion note below):\n"
    f"FY2026: Annual Report and Financial Statements, year ended 31 March 2026, p.30-31 (Income Statement / Statement of Other Comprehensive Income) - {AR2026_URL}\n"
    f"FY2025: Annual Report and Financial Statements, year ended 31 March 2025, p.30-31 (Income Statement / Statement of Other Comprehensive Income) - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements, year ended 31 March 2024, p.23-24 (Income Statement / Statement of Other Comprehensive Income) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements, year ended 31 March 2023, p.22-23 (Income Statement / Statement of Other Comprehensive Income) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements, year ended 31 March 2022, p.30-31 (Income Statement / Statement of Other Comprehensive Income) - {AR2022_URL}\n"
    f"FY2021: as presented in the FY2022 Annual Report's own comparative column (p.30-31) - {AR2022_URL}\n"
    f"FY2020: Financial Statements, year ended 31 March 2020, p.28-29 (Income Statement / Statement of Comprehensive Income) - {AR2020_URL}\n"
    f"FY2019: Annual Accounts, year ended 31 March 2019, p.22 (Income Statement) - {AR2019_URL}\n"
    f"FY2018: Annual Accounts, year ended 31 March 2018, p.20 (Income Statement) - {AR2018_URL}\n"
    "Presentation note: a standalone 'Finance Cost' line only appears from FY2023 onward - FY2021/FY2022's own "
    "reports fold this into 'Other expenses' instead (both years' own 'Operating expenses before impairment loss "
    "allowances' subtotal is unaffected either way; the FY2021/FY2022 rows are left blank for the 'Finance Cost' "
    "line rather than estimating a split). No taxation was charged or credited in any year shown from FY2021 "
    "onward; FY2018/FY2019/FY2020 each show a genuine tax charge or credit (a distinct 'Corporation tax (charge)/"
    "credit' line, reproduced here). FY2018-FY2020 each show a distinct 'Operating lease' expense line (IFRS 16 "
    "right-of-use depreciation replaces it from FY2020's own report onward, which is why the FY2020 figure is nil) "
    "- reproduced here as its own row rather than folded into 'Other expenses'. FY2020 also shows a 'Fair value "
    "Loss' line between impairment and profit/loss before tax, reproduced under the same 'Fair value gain/(loss) "
    "on Foreign Exchange Derivatives' row used for that item in FY2021 onward.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

EQ_SOURCES = (
    "Sources - Union Bank of India (UK) Limited's own Statement of Changes in Equity (converted from USD to £; "
    "opening/closing balances at that year-end's SPOT rate, in-year movements at that year's AVERAGE rate - see FX "
    "conversion note on the Cash Flow Statement sheet):\n"
    f"FY2026: Annual Report and Financial Statements, year ended 31 March 2026, p.34 - {AR2026_URL}\n"
    f"FY2025: Annual Report and Financial Statements, year ended 31 March 2025, p.34 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements, year ended 31 March 2024, p.27 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements, year ended 31 March 2023, p.26 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements, year ended 31 March 2022, p.34 - {AR2022_URL}\n"
    f"FY2021: as presented in the FY2022 Annual Report's own comparative column (p.34) - {AR2022_URL}\n"
    f"FY2020: Financial Statements, year ended 31 March 2020, p.32 - {AR2020_URL}\n"
    f"FY2019: Annual Accounts, year ended 31 March 2019 (Statement of Changes in Equity), as presented in the "
    f"FY2020 Financial Statements' own comparative column (p.32; agrees exactly with FY2019's own report) - {AR2020_URL}\n"
    f"FY2018: Annual Accounts, year ended 31 March 2018, p.23 - {AR2018_URL}\n"
    f"Opening balance at 1 April 2020: as presented in the FY2022 Annual Report's own comparative column (p.34) - {AR2022_URL}\n"
    f"Opening balance at 1 April 2017: as presented in the FY2018 Annual Accounts' own comparative column (p.23) - {AR2018_URL}\n\n"
    "'Effect of GBP/USD translation' rows are computed programmatically (closing balance at spot, less opening "
    "balance at prior year's spot, less that year's movements at average rate) - they absorb both the FX "
    "rate-differential (opening/closing use spot, movements use average - see FX_NOTE) and the Bank's own $1k "
    "source-document rounding artefacts in FY2022/FY2023 (see ROUNDING NOTE on the Balance Sheet sheet). This Bank "
    "has no treasury shares, share-based payments, or FX/translation reserve movements in any year shown - the "
    "only two equity-component columns are Fair value reserves and Retained earnings (plus Issued capital), and "
    "Issued capital is static from FY2021 onward; FY2018/FY2019/FY2020 each saw a real cash share issuance "
    "($10,000k FY2018, $10,000k FY2019, $50,000k FY2020, reproduced as a distinct 'Issue of share capital' row). "
    "FY2019 additionally shows a one-off 'Impact of IFRS 9 transition' row (Fair value reserves +$246k, Retained "
    "earnings +$907k, booked to opening equity at 1 April 2018 rather than through FY2019's own profit or OCI) - "
    "see the Cash Flow Statement's FY2018-FY2020 presentation note for the CF statement's separate $907k "
    "'Impairment loss during transition period' line, which coincides with this amount.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

AQ_SOURCES = (
    "Sources - Union Bank of India (UK) Limited's own IFRS 9 credit quality note for Loans and advances to "
    "customers (converted from USD to £ at each year-end's SPOT rate - a point-in-time balance, see FX conversion "
    "note on the Cash Flow Statement sheet):\n"
    f"FY2026 and FY2025: Annual Report and Financial Statements, year ended 31 March 2026, p.60 (IFRS 9 Credit Quality - stage tables for both 31 March 2026 and 31 March 2025) and p.51 (Note 11 Loans and Advances to Customers, for the unamortised processing-fee bridge) - {AR2026_URL}\n"
    f"FY2025: Annual Report and Financial Statements, year ended 31 March 2025, p.58 (IFRS 9 Credit Quality) - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements, year ended 31 March 2024, p.51 (IFRS 9 Credit Quality) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements, year ended 31 March 2023, p.51 (Credit Risk) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements, year ended 31 March 2022, p.64-65 (Credit Risk) - {AR2022_URL}\n"
    f"FY2021: as presented in the FY2022 Annual Report's own comparative column (p.65) - {AR2022_URL}\n"
    f"FY2020: Financial Statements, year ended 31 March 2020, p.64 (Country risk exposure - credit exposure "
    f"stagewise) and p.61-62 (ECL provision rollforward) - {AR2020_URL}\n"
    f"FY2019: Annual Accounts, year ended 31 March 2019, p.55 (Credit Risk Review - Loans to Customers by stage) - {AR2019_URL}\n\n"
    "SELF-SKIP - FY2018: no IFRS 9 stage-based credit quality disclosure exists for FY2018 - the Bank adopted "
    "IFRS 9 (replacing the IAS 39 incurred-loss model) from 1 April 2018, i.e. the start of FY2019, so its FY2018 "
    "Annual Accounts only disclose loans by 'neither past due nor impaired / past due but not impaired / impaired' "
    "(an IAS 39-style category, not Stage 1/2/3) - genuinely not the same disclosure as this sheet, not a search "
    "failure. FY2018 is therefore left blank on this sheet rather than force-mapped into IFRS 9 stages.\n\n"
    "FY2020 note: FY2020's own Annual Report does not repeat the FY2019-style 'Loans to Customers as at [date]' "
    "gross-carrying/ECL-provision-by-stage table in one place; the FY2020 Stage 1/2/3 gross carrying figures used "
    "here are its own 'credit exposure stagewise' summary table (p.64, which reconciles exactly to the Balance "
    "Sheet's 'Loans and advances to customers' net figure once the ECL provision rollforward's own 31 March 2020 "
    "closing figures, by stage, are deducted), and the ECL provision figures are that same rollforward's own "
    "closing balances (p.61-62) - both are the Bank's own figures, just assembled from two adjacent notes rather "
    "than one combined table as in FY2019/FY2021 onward.\n\n"
    "'Net amounts receivable' (by stage) sums to a 'Loans and advances to customers (net of impairment, before "
    "unamortised processing fees)' subtotal, which is then bridged to the Balance Sheet's own 'Loans and advances "
    "to customers' line via a 'Less: unamortised portion of processing fees' row - reproducing the Bank's own note "
    "structure exactly (only FY2024/FY2025 disclose this fee bridge explicitly; earlier years' net-by-stage total "
    "ties to the Balance Sheet directly, within $1k rounding - see ROUNDING NOTE on the Balance Sheet sheet). NPL "
    "ratio = Stage 3 gross carrying amount / Total gross carrying amount; Stage 3 coverage ratio = Stage 3 "
    "impairment provision / Stage 3 gross carrying amount; overall ECL coverage ratio = Total impairment provision "
    "/ Total gross carrying amount - all derived, not separately disclosed by the Bank.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

RWA_SOURCES = (
    "Sources - Union Bank of India (UK) Limited's own Pillar 3 UK OV1 (Overview of risk-weighted exposure amounts) "
    "disclosure, or its pre-UK-OV1-template equivalent for FY2022/FY2021 (converted from USD to £ at each "
    "year-end's SPOT rate; see FX conversion note on the Cash Flow Statement sheet):\n"
    f"FY2025: Pillar 3 Disclosure 2024-25, p.7-8 (UK OV1) - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosure 2023-24, p.7-8 (UK OV1) - {P3_2024_URL}\n"
    f"FY2023: Pillar III Disclosure 2022-23, p.7-8 (UK OV1) - {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosure 2022, p.28 (3.5 Overview of total RWA) - {P3_2022_URL}\n"
    f"FY2021: Pillar 3 Disclosure 2021, p.26 (3.5 Overview of total RWA) - {P3_2021_URL}\n"
    f"FY2020: Pillar 3 Disclosure 2020, p.23 (3.5 Overview of total RWA) - {P3_2020_URL}\n"
    f"FY2019: Pillar III Disclosures 2019, p.13 (3.1.3 Overview of total RWA) - {P3_2019_URL}\n"
    f"FY2018: Pillar 3 Disclosures 2018, p.11 (3.1.3 Overview of total RWA) - {P3_2018_URL}\n"
    "FY2026: BLANK - no FY2026 Pillar 3 Disclosure has been published (verified 2026-09-15; the Bank's own "
    "disclosures page still lists FY2025 as its latest Pillar 3, and the FY2026 Annual Report discloses no "
    "risk-weighted asset figure of any kind). See the note on the Total RWAs sheet.\n\n"
    "PRESENTATION NOTE: FY2021/FY2022's own Pillar 3 Disclosures predate the Bank's adoption of the UK OV1 template "
    "- both years' own '3.5 Overview of total RWA' table groups standardised credit risk together with counterparty "
    "credit risk (excluding CVA) into a single 'Credit risk: Standardised approach' line ($314,895k FY2021 / "
    "$330,859k FY2022), showing CVA separately ($1,018k FY2021 / $347k FY2022) but with no distinct 'Counterparty "
    "credit risk (CCR)' category of its own - reproduced here exactly as presented (the 'Counterparty credit risk "
    "(CCR)' row is left blank for FY2021/FY2022, not populated with an estimate). FY2023 onward uses the UK OV1 "
    "template, which separates 'Credit risk (excluding CCR)' from 'Counterparty credit risk (CCR)' (itself "
    "sub-showing CVA as one component of CCR) - both are populated from FY2023 onward. FY2021's category-level "
    "breakdown ($314,895k + $1,018k + $6,003k market risk + $21,231k operational risk) sums to exactly $343,147k, "
    "reconciling to the Total RWAs headline figure already on file for that year. FY2018/FY2019/FY2020's own "
    "Pillar 3 Disclosures use the same pre-UK-OV1 '3.1.3/3.5 Overview of total RWA' table format as FY2021/FY2022 "
    "(single combined 'Credit risk: Standardised approach' line, CVA shown separately, no distinct CCR category) - "
    "the 'Counterparty credit risk (CCR)' row is left blank for these three years too, on the same basis.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

# --- Balance Sheet ---
BS_USD = {
    "FY2021": dict(cash=6150, lab=8000, lac=256757, fi_am=17329, fi_fvtpl=1316, deriv_a=1436, fi_fvoci=98207, ppe=978, intang=99, cwip=41, other_assets=902, total_assets=391215,
                   dep_banks=0, dep_cust=271130, repo=5223, deriv_l=0, provisions=114, other_liab=2930, total_liab=279397,
                   share_cap=150000, fv_res=537, acc_loss=-38719, total_equity=111818),
    "FY2022": dict(cash=5170, lab=19194, lac=286830, fi_am=11796, fi_fvtpl=1450, deriv_a=0, fi_fvoci=75923, ppe=644, intang=151, cwip=0, other_assets=1447, total_assets=402605,
                   dep_banks=6011, dep_cust=275587, repo=5149, deriv_l=586, provisions=113, other_liab=1915, total_liab=289361,
                   share_cap=150000, fv_res=-3309, acc_loss=-33447, total_equity=113244),
    "FY2023": dict(cash=18856, lab=57971, lac=318969, fi_am=6875, fi_fvtpl=2232, deriv_a=224, fi_fvoci=77408, ppe=239, intang=132, cwip=0, other_assets=700, total_assets=483606,
                   dep_banks=35826, dep_cust=332484, repo=0, deriv_l=0, provisions=113, other_liab=1347, total_liab=369770,
                   share_cap=150000, fv_res=-4582, acc_loss=-31581, total_equity=113837),
    "FY2024": dict(cash=8336, lab=43027, lac=339650, fi_am=4983, fi_fvtpl=3270, deriv_a=0, fi_fvoci=103558, ppe=5207, intang=71, cwip=0, other_assets=1402, total_assets=509504,
                   dep_banks=0, dep_cust=387541, repo=0, deriv_l=194, provisions=172, other_liab=4714, total_liab=392621,
                   share_cap=150000, fv_res=-3024, acc_loss=-30093, total_equity=116883),
    "FY2026": dict(cash=14344, lab=86003, lac=348451, fi_am=0, fi_fvtpl=2300, deriv_a=0, fi_fvoci=101212, ppe=3982, intang=416, cwip=0, other_assets=953, total_assets=557661,
                   dep_banks=60939, dep_cust=346324, repo=30902, deriv_l=375, provisions=196, other_liab=5479, total_liab=444215,
                   share_cap=150000, fv_res=-96, acc_loss=-36458, total_equity=113446),
    "FY2025": dict(cash=14195, lab=20202, lac=340434, fi_am=1997, fi_fvtpl=2761, deriv_a=0, fi_fvoci=94823, ppe=4586, intang=18, cwip=0, other_assets=2001, total_assets=481017,
                   dep_banks=0, dep_cust=348633, repo=15240, deriv_l=1436, provisions=184, other_liab=3924, total_liab=369417,
                   share_cap=150000, fv_res=-1699, acc_loss=-36701, total_equity=111600),
    # FY2018-FY2020 (added per HD-058): own-report figures, each year's own Annual Accounts/Financial Statements -
    # see STATEMENTS_RESTATEMENT_NOTE's FY2018-FY2020 PRESENTATION NOTE for the 'dta'/'intragroup_borrow'/
    # 'provisions' line items unique to these years.
    "FY2020": dict(cash=6411, lab=44054, lac=256273, fi_am=12062, fi_fvtpl=None, deriv_a=0, fi_fvoci=72563, ppe=1388, intang=230, cwip=0, dta=None, other_assets=5025, total_assets=398004,
                   dep_banks=21256, intragroup_borrow=0, dep_cust=241918, repo=8941, deriv_l=3210, provisions=112, other_liab=1558, total_liab=276995,
                   share_cap=150000, fv_res=-1211, acc_loss=-27781, total_equity=121008),
    "FY2019": dict(cash=4244, lab=26337, lac=302055, fi_am=12239, fi_fvtpl=0, deriv_a=409, fi_fvoci=103268, ppe=290, intang=164, cwip=70, dta=2372, other_assets=2651, total_assets=454100,
                   dep_banks=29387, intragroup_borrow=60564, dep_cust=239778, repo=30326, deriv_l=0, provisions=None, other_liab=730, total_liab=360785,
                   share_cap=100000, fv_res=-964, acc_loss=-5719, total_equity=93317),
    "FY2018": dict(cash=1355, lab=0, lac=336818, fi_am=13807, fi_fvtpl=1916, deriv_a=0, fi_fvoci=82281, ppe=395, intang=49, cwip=70, dta=809, other_assets=1794, total_assets=439294,
                   dep_banks=32140, intragroup_borrow=62429, dep_cust=215566, repo=33081, deriv_l=426, provisions=None, other_liab=1061, total_liab=344703,
                   share_cap=90000, fv_res=-2478, acc_loss=7069, total_equity=94591),
}


def bs_line(key):
    return {y: _stock1(d[key], y) for y, d in BS_USD.items() if d.get(key) is not None}


bw.add_balance_sheet_sheet(
    title="Union Bank of India (UK) Limited — Statement of Financial Position",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and cash equivalents", bs_line("cash")),
        ("DATA", "Loans and advances to Banks", bs_line("lab")),
        ("DATA", "Loans and advances to customers", bs_line("lac")),
        ("DATA", "Financial investments (amortised cost)", bs_line("fi_am")),
        ("DATA", "Financial investments (FVTPL)", bs_line("fi_fvtpl")),
        ("DATA", "Derivative financial instruments (assets)", bs_line("deriv_a")),
        ("DATA", "Financial investments (FVOCI)", bs_line("fi_fvoci")),
        ("DATA", "Property, plant and equipment", bs_line("ppe")),
        ("DATA", "Intangible assets", bs_line("intang")),
        ("DATA", "Capital work in progress", bs_line("cwip")),
        ("DATA", "Deferred tax assets (net)", bs_line("dta")),
        ("DATA", "Other assets", bs_line("other_assets")),
        ("TOTAL", "Total Assets", bs_line("total_assets")),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits from Banks", bs_line("dep_banks")),
        ("DATA", "Intra-group borrowings", bs_line("intragroup_borrow")),
        ("DATA", "Deposits from customers", bs_line("dep_cust")),
        ("DATA", "Repurchase agreements", bs_line("repo")),
        ("DATA", "Derivative financial instruments (liabilities)", bs_line("deriv_l")),
        ("DATA", "Provisions", bs_line("provisions")),
        ("DATA", "Other liabilities", bs_line("other_liab")),
        ("TOTAL", "Total Liabilities", bs_line("total_liab")),
        ("SECTION", "Equity", {}),
        ("DATA", "Share capital", bs_line("share_cap")),
        ("DATA", "Fair value reserves", bs_line("fv_res")),
        ("DATA", "Accumulated losses", bs_line("acc_loss")),
        ("TOTAL", "Total Shareholder's equity", bs_line("total_equity")),
    ],
    sources_text=BS_SOURCES,
    first_col_width=64,
    source_height=380,
    unit_suffix=" (£'000, conv. from USD)",
)

# --- Profit & Loss ---
IS_USD = {
    "FY2021": dict(int_inc=13690, int_exp=-4823, nii=8867, fee_inc=366, trading=30, other_inc=1026, derecog=237, total_op_inc=10526,
                   personnel=-3173, dep_amort=-528, finance_cost=None, other_exp=-3171, op_exp_before_impair=-6872, op_profit_before_impair=3654,
                   impair=-14789, fv_fx=197, pbt=-10939, tax=0, pat=-10939, oci=1749, tci=-9190),
    "FY2022": dict(int_inc=11415, int_exp=-3219, nii=8196, fee_inc=782, trading=18, other_inc=808, derecog=0, total_op_inc=9804,
                   personnel=-3809, dep_amort=-518, finance_cost=None, other_exp=-3424, op_exp_before_impair=-7751, op_profit_before_impair=2053,
                   impair=3129, fv_fx=91, pbt=5273, tax=0, pat=5273, oci=-3846, tci=1427),
    "FY2023": dict(int_inc=19884, int_exp=-6912, nii=12972, fee_inc=573, trading=-66, other_inc=882, derecog=None, total_op_inc=14361,
                   personnel=-3881, dep_amort=-514, finance_cost=-149, other_exp=-2818, op_exp_before_impair=-7362, op_profit_before_impair=6999,
                   impair=-5066, fv_fx=-67, pbt=1866, tax=0, pat=1866, oci=-1273, tci=593),
    "FY2024": dict(int_inc=31029, int_exp=-16852, nii=14177, fee_inc=712, trading=46, other_inc=1494, derecog=None, total_op_inc=16429,
                   personnel=-4456, dep_amort=-649, finance_cost=-304, other_exp=-4064, op_exp_before_impair=-9473, op_profit_before_impair=6956,
                   impair=-5593, fv_fx=125, pbt=1488, tax=0, pat=1488, oci=1558, tci=3046),
    "FY2026": dict(int_inc=29993, int_exp=-17845, nii=12148, fee_inc=17, trading=-799, other_inc=440, derecog=None, total_op_inc=11806,
                   personnel=-5364, dep_amort=-688, finance_cost=-463, other_exp=-3628, op_exp_before_impair=-10143, op_profit_before_impair=1663,
                   impair=-1407, fv_fx=-13, pbt=243, tax=0, pat=243, oci=1603, tci=1846),
    "FY2025": dict(int_inc=32247, int_exp=-19934, nii=12313, fee_inc=583, trading=-204, other_inc=635, derecog=None, total_op_inc=13327,
                   personnel=-5063, dep_amort=-685, finance_cost=-466, other_exp=-3520, op_exp_before_impair=-9734, op_profit_before_impair=3593,
                   impair=-10245, fv_fx=44, pbt=-6608, tax=0, pat=-6608, oci=1325, tci=-5283),
    # FY2018-FY2020 (added per HD-058): own-report figures. 'lease' = Operating lease expense (own line these
    # three years; folded into 'Other expenses'/replaced by IFRS 16 depreciation from FY2021 onward - see
    # IS_SOURCES presentation note). No 'Fair value gain/(loss) on Foreign Exchange Derivatives' line in
    # FY2018/FY2019; FY2020's own report shows one labelled just 'Fair value Loss'.
    "FY2020": dict(int_inc=20313, int_exp=-8087, nii=12226, fee_inc=150, trading=424, other_inc=845, derecog=None, total_op_inc=13645,
                   personnel=-2785, lease=0, dep_amort=-586, finance_cost=None, other_exp=-3070, op_exp_before_impair=-6440, op_profit_before_impair=7204,
                   impair=-26546, fv_fx=-546, pbt=-19887, tax=-2174, pat=-22061, oci=-247, tci=-22308),
    "FY2019": dict(int_inc=22527, int_exp=-9179, nii=13348, fee_inc=263, trading=54, other_inc=-106, derecog=None, total_op_inc=13559,
                   personnel=-2300, lease=-316, dep_amort=-160, finance_cost=None, other_exp=-2237, op_exp_before_impair=-5013, op_profit_before_impair=8546,
                   impair=-25181, fv_fx=None, pbt=-16635, tax=2939, pat=-13696, oci=1268, tci=-12427),
    "FY2018": dict(int_inc=17389, int_exp=-6327, nii=11062, fee_inc=541, trading=256, other_inc=374, derecog=None, total_op_inc=12233,
                   personnel=-2032, lease=-307, dep_amort=-140, finance_cost=None, other_exp=-1442, op_exp_before_impair=-3921, op_profit_before_impair=8312,
                   impair=-1930, fv_fx=None, pbt=6382, tax=-1214, pat=5168, oci=-1964, tci=3204),
}


def is_line(key):
    return {y: _flow1(d[key], y) for y, d in IS_USD.items() if d.get(key) is not None}


bw.add_income_statement_sheet(
    title="Union Bank of India (UK) Limited — Income Statement & Statement of Other Comprehensive Income",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest and similar income", is_line("int_inc")),
        ("DATA", "Interest and similar expense", is_line("int_exp")),
        ("TOTAL", "Net interest income", is_line("nii")),
        ("DATA", "Fees and commission income", is_line("fee_inc")),
        ("DATA", "Net trading income/(expense)", is_line("trading")),
        ("DATA", "Net other operating income", is_line("other_inc")),
        ("DATA", "Derecognition gain", is_line("derecog")),
        ("TOTAL", "Total Operating income", is_line("total_op_inc")),
        ("DATA", "Personnel costs", is_line("personnel")),
        ("DATA", "Operating lease", is_line("lease")),
        ("DATA", "Depreciation and amortisation", is_line("dep_amort")),
        ("DATA", "Finance Cost", is_line("finance_cost")),
        ("DATA", "Other expenses", is_line("other_exp")),
        ("TOTAL", "Operating expenses before impairment loss allowances", is_line("op_exp_before_impair")),
        ("TOTAL", "Operating profit before impairment loss allowances", is_line("op_profit_before_impair")),
        ("DATA", "Impairment loss allowances/(reversal)", is_line("impair")),
        ("DATA", "Fair value gain/(loss) on Foreign Exchange Derivatives", is_line("fv_fx")),
        ("TOTAL", "Profit/(Loss) before tax", is_line("pbt")),
        ("DATA", "Corporation tax (charge)/credit", is_line("tax")),
        ("TOTAL", "Profit/(Loss) after tax", is_line("pat")),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Fair value gain/(loss) on FVTOCI debt instruments", is_line("oci")),
        ("TOTAL", "Total comprehensive income/(loss) for the year", is_line("tci")),
    ],
    sources_text=IS_SOURCES,
    first_col_width=64,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# --- Statement of Changes in Equity ---
EQ_HEADERS = ["Issued capital", "Fair value reserves", "Retained earnings", "Total equity"]
EQ_BALANCES_USD = {
    "FY2017_open": (80000, -514, 1901, 81387),
    "FY2018_close": (90000, -2478, 7069, 94591),
    "FY2019_close": (100000, -964, -5719, 93317),
    "FY2020_open": (150000, -1211, -27781, 121008),
    "FY2021_close": (150000, 537, -38719, 111818),
    "FY2022_close": (150000, -3309, -33447, 113244),
    "FY2023_close": (150000, -4582, -31581, 113837),
    "FY2024_close": (150000, -3024, -30093, 116883),
    "FY2025_close": (150000, -1699, -36701, 111600),
    "FY2026_close": (150000, -96, -36458, 113446),
}
EQ_MOVEMENTS_USD = {
    "FY2018": dict(profit=5168, oci=-1964, tci=3204),
    "FY2019": dict(profit=-13696, oci=1268, tci=-12427),
    "FY2020": dict(profit=-22061, oci=-247, tci=-22308),
    "FY2021": dict(profit=-10939, oci=1749, tci=-9190),
    "FY2022": dict(profit=5273, oci=-3846, tci=1427),
    "FY2023": dict(profit=1866, oci=-1273, tci=593),
    "FY2024": dict(profit=1488, oci=1558, tci=3046),
    "FY2025": dict(profit=-6608, oci=1325, tci=-5283),
    "FY2026": dict(profit=243, oci=1603, tci=1846),
}
# FY2018/FY2019/FY2020 each saw a real cash share issuance (converted at that year's own AVERAGE rate, like a
# flow item, since it's a discrete during-year transaction) - see EQ_SOURCES.
EQ_ISSUE_USD = {"FY2018": 10000, "FY2019": 10000, "FY2020": 50000}
# FY2019 only: IFRS 9 transition impact, booked to opening equity at 1 April 2018 (i.e. converted at FY2018's own
# period-end SPOT rate, the same rate used for the FY2019 opening balance) rather than through FY2019's own
# profit or OCI - see EQ_SOURCES.
EQ_IFRS9_TRANSITION_USD = {"FY2019": (0, 246, 907, 1153)}
EQ_OPEN_KEY = {"FY2018": "FY2017_open", "FY2019": "FY2018_close", "FY2020": "FY2019_close",
               "FY2021": "FY2020_open", "FY2022": "FY2021_close", "FY2023": "FY2022_close", "FY2024": "FY2023_close", "FY2025": "FY2024_close", "FY2026": "FY2025_close"}
EQ_OPEN_SPOT_YEAR = {"FY2018": "FY2017", "FY2019": "FY2018", "FY2020": "FY2019",
                      "FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024", "FY2026": "FY2025"}
EQ_CLOSE_KEY = {"FY2018": "FY2018_close", "FY2019": "FY2019_close", "FY2020": "FY2020_open",
                "FY2021": "FY2021_close", "FY2022": "FY2022_close", "FY2023": "FY2023_close", "FY2024": "FY2024_close", "FY2025": "FY2025_close", "FY2026": "FY2026_close"}
EQ_CLOSE_LABEL = {"FY2018": "31 March 2018", "FY2019": "31 March 2019", "FY2020": "31 March 2020",
                   "FY2021": "31 March 2021", "FY2022": "31 March 2022", "FY2023": "31 March 2023", "FY2024": "31 March 2024", "FY2025": "31 March 2025", "FY2026": "31 March 2026"}
EQ_OPEN_LABEL = {"FY2018": "1 April 2017", "FY2019": "31 March 2018", "FY2020": "31 March 2019",
                  "FY2021": "1 April 2020", "FY2022": "31 March 2021", "FY2023": "31 March 2022", "FY2024": "31 March 2023", "FY2025": "31 March 2024", "FY2026": "31 March 2025"}

EQ_ROWS = []
_eq_years_chrono = ["FY2018", "FY2019", "FY2020", "FY2021", "FY2022", "FY2023", "FY2024", "FY2025", "FY2026"]
for i, y in enumerate(_eq_years_chrono):
    ob = EQ_BALANCES_USD[EQ_OPEN_KEY[y]]
    cb = EQ_BALANCES_USD[EQ_CLOSE_KEY[y]]
    oy = EQ_OPEN_SPOT_YEAR[y]
    ob_gbp = tuple(_stock1(v, oy) for v in ob)
    cb_gbp = tuple(_stock1(v, y) for v in cb)
    m = EQ_MOVEMENTS_USD[y]
    profit_gbp = _flow1(m["profit"], y)
    oci_gbp = _flow1(m["oci"], y)
    tci_gbp = _flow1(m["tci"], y)
    issue_usd = EQ_ISSUE_USD.get(y)
    issue_gbp = _flow1(issue_usd, y) if issue_usd is not None else 0
    transition_usd = EQ_IFRS9_TRANSITION_USD.get(y)
    transition_gbp = tuple(_stock1(v, oy) for v in transition_usd) if transition_usd is not None else (0, 0, 0, 0)
    plug = (
        round(cb_gbp[0] - ob_gbp[0] - issue_gbp - transition_gbp[0], 1),
        round(cb_gbp[1] - ob_gbp[1] - oci_gbp - transition_gbp[1], 1),
        round(cb_gbp[2] - ob_gbp[2] - profit_gbp - transition_gbp[2], 1),
        round(cb_gbp[3] - ob_gbp[3] - tci_gbp - transition_gbp[3], 1),
    )
    if i == 0:
        EQ_ROWS.append(("TOTAL", f"Balance as at {EQ_OPEN_LABEL[y]}", ob_gbp))
    if transition_usd is not None:
        EQ_ROWS.append(("DATA", "Impact of IFRS 9 transition", transition_gbp))
    if issue_usd is not None:
        EQ_ROWS.append(("DATA", "Issue of share capital", (issue_gbp, None, None, issue_gbp)))
    profit_label = "(Loss)/Profit for the year" if m["profit"] < 0 else "Profit for the year"
    EQ_ROWS.append(("DATA", profit_label, (None, None, profit_gbp, profit_gbp)))
    EQ_ROWS.append(("DATA", "Other comprehensive income/(expense) - FV movement on FVTOCI debt instruments", (None, oci_gbp, None, oci_gbp)))
    tci_label = "Total comprehensive (loss)/income for the year" if m["tci"] < 0 else "Total comprehensive income for the year"
    EQ_ROWS.append(("TOTAL", tci_label, (None, None, None, tci_gbp)))
    EQ_ROWS.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", plug))
    EQ_ROWS.append(("TOTAL", f"Balance as at {EQ_CLOSE_LABEL[y]}", cb_gbp))

bw.add_equity_changes_sheet(
    title="Union Bank of India (UK) Limited — Statement of Changes in Equity",
    subtitle="£'000, converted from USD - chronological 1 April 2017 through 31 March 2026 - see source note for FX methodology.",
    headers=EQ_HEADERS,
    rows=EQ_ROWS,
    sources_text=EQ_SOURCES,
    first_col_width=70,
    source_height=380,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD, converted via flow()/stock()/opening_cash())
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "(Loss)/profit before tax for the year", {"FY2026": 243, "FY2025": -6608, "FY2024": 1488, "FY2023": 1866, "FY2022": 5273, "FY2021": -10939, "FY2020": -19887, "FY2019": -16635, "FY2018": 6382}),
    ("DATA", "Interest Income", {"FY2026": -29993, "FY2025": -32247, "FY2024": -31029, "FY2023": -19884}),
    ("DATA", "Interest Expense", {"FY2026": 17845, "FY2025": 19934, "FY2024": 16852, "FY2023": 6912}),
    ("DATA", "Impairment loss allowances", {"FY2026": 1407, "FY2025": 10245, "FY2024": 5593, "FY2023": 5066}),
    ("DATA", "Impairment loss during transition period", {"FY2019": 907}),
    ("DATA", "Amortisation of intangible non-current asset", {"FY2026": 70, "FY2025": 57, "FY2024": 62, "FY2023": 83, "FY2022": 99, "FY2021": 131, "FY2020": 155, "FY2019": 40, "FY2018": 18}),
    ("DATA", "Depreciation for property, plant and equipment", {"FY2026": 618, "FY2025": 628, "FY2024": 587, "FY2023": 431, "FY2022": 420, "FY2021": 421, "FY2020": 430, "FY2019": 120, "FY2018": 122}),
    ("DATA", "FV movement in derivatives", {"FY2026": 13, "FY2025": -44, "FY2024": -125, "FY2023": 67, "FY2022": -92, "FY2021": -197, "FY2020": 546}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents (operating adjustment)", {"FY2026": 327, "FY2025": 126, "FY2024": 122, "FY2023": 148, "FY2022": 33, "FY2021": -5}),
    ("DATA", "FV movement of investments at FVTPL", {"FY2026": 461, "FY2025": 509, "FY2024": -1038}),
    ("DATA", "Corporation tax credit/(charge) during the year", {"FY2020": -2174, "FY2019": 2939}),
    ("DATA", "Finance Charge on Lease", {"FY2026": 224, "FY2025": 247, "FY2024": 166, "FY2023": 10, "FY2022": 24, "FY2021": 38, "FY2020": 53}),
    ("TOTAL", "Cash flows before changes in working capital (excl. profit before tax - see presentation note)", {"FY2026": -9028, "FY2025": -545, "FY2024": -8811, "FY2023": -7167, "FY2022": 484, "FY2021": 388, "FY2020": -989, "FY2019": 4006, "FY2018": 140}),
    ("DATA", "(Increase)/Decrease in receivables & prepayments", {"FY2026": 1184, "FY2025": -599, "FY2024": -702, "FY2023": 747, "FY2022": -545, "FY2021": 4123, "FY2020": -2482, "FY2019": 371, "FY2018": -949}),
    ("DATA", "Tax paid", {"FY2022": 0, "FY2021": 0, "FY2019": -1228}),
    ("DATA", "(Decrease)/Increase in other liabilities", {"FY2026": 1950, "FY2025": -584, "FY2024": 794, "FY2023": -146, "FY2022": -568, "FY2021": 1775, "FY2020": 1835, "FY2019": -1895, "FY2018": -1774}),
    ("TOTAL", "Net change in working capital", {"FY2026": 3134, "FY2025": -1183, "FY2024": 92, "FY2023": 601, "FY2022": -1113, "FY2021": 5898, "FY2020": -647, "FY2019": -2752, "FY2018": -2723}),
    ("DATA", "(Decrease)/Increase in loans and advances to customers", {"FY2026": -8333, "FY2025": -8058, "FY2024": -24458, "FY2023": -34904, "FY2022": -30074, "FY2021": -485, "FY2020": 45782, "FY2019": 34763, "FY2018": -59833}),
    ("DATA", "Interest received on loans and advances to customers", {"FY2026": 23340, "FY2025": 22391, "FY2024": 22218, "FY2023": 14354}),
    ("DATA", "Decrease/(Increase) in loans and advances to banks", {"FY2026": -65616, "FY2025": 22748, "FY2024": 15018, "FY2023": -38776, "FY2022": -11194, "FY2021": 36054, "FY2020": -17717, "FY2019": -26337, "FY2018": 7000}),
    ("DATA", "Interest received on loans and advances to banks", {"FY2026": 2654, "FY2025": 3769, "FY2024": 3509, "FY2023": 1464}),
    ("DATA", "Decrease in deposits from Banks", {"FY2022": 0, "FY2021": -21256, "FY2020": -8131, "FY2019": -2753, "FY2018": -3561}),
    ("DATA", "(Decrease)/Increase in deposits from customers", {"FY2026": 38, "FY2025": -37899, "FY2024": 47737, "FY2023": 53780, "FY2022": 4457, "FY2021": 29212, "FY2020": 2141, "FY2019": 24212, "FY2018": 46624}),
    ("DATA", "Interest paid on deposits from customers", {"FY2026": -17589, "FY2025": -20076, "FY2024": -8478, "FY2023": -2832}),
    ("DATA", "Decrease/(Increase) in derivative financial instruments - Assets", {"FY2025": 0, "FY2024": 224, "FY2023": -224, "FY2022": 1436, "FY2021": -1436, "FY2020": 409, "FY2019": -409, "FY2018": 324}),
    ("DATA", "Increase/(Decrease) in derivative financial instruments - Liabilities", {"FY2026": -1074, "FY2025": 1286, "FY2024": 316, "FY2023": -654, "FY2022": 678, "FY2021": -3013, "FY2020": 3210, "FY2019": -426, "FY2018": 426}),
    ("DATA", "Increase/(Decrease) in repurchase agreements (see FY2018-FY2020 presentation note)", {"FY2020": -21385, "FY2019": -2755, "FY2018": 33081}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2026": -72231, "FY2025": -24175, "FY2024": 48856, "FY2023": -12492, "FY2022": -30053, "FY2021": 34423, "FY2020": -17215, "FY2019": 10915, "FY2018": 27860}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Disposal/(Acquisition) of Investments - FVOCI", {"FY2022": 18437, "FY2021": -23895, "FY2020": 30458, "FY2019": -19473, "FY2018": -47633}),
    ("DATA", "Acquisition of Investments - FVOCI", {"FY2026": -35223, "FY2025": -15132, "FY2024": -24308, "FY2023": -2692}),
    ("DATA", "Proceeds from Investments", {"FY2026": 32570, "FY2025": 28142}),
    ("DATA", "Disposal/(Acquisition) of Investments - Amortised cost", {"FY2022": 5533, "FY2021": -5266, "FY2020": 177, "FY2019": 1568, "FY2018": 57}),
    ("DATA", "Proceeds from Investments - Amortised cost", {"FY2024": 1892, "FY2023": 4921}),
    ("DATA", "(Acquisition)/Disposal of Investments - FVTPL", {"FY2023": -782, "FY2022": -133, "FY2021": -1316, "FY2019": 1916, "FY2018": -1916}),
    ("DATA", "Interest received on Investments", {"FY2026": 2584, "FY2025": 3228, "FY2024": 1980, "FY2023": 1698}),
    ("DATA", "Disposal of property, plant and equipment", {"FY2022": 3, "FY2021": 2}),
    ("DATA", "Acquisition of property, plant and equipment", {"FY2026": -14, "FY2025": -12, "FY2024": -1745, "FY2023": -25, "FY2022": -48, "FY2021": -54, "FY2020": -33, "FY2019": -15, "FY2018": -56}),
    ("DATA", "Acquisition of intangible assets", {"FY2026": -604, "FY2025": -4, "FY2023": -64, "FY2022": -151, "FY2020": -244, "FY2019": -155, "FY2018": -36}),
    ("DATA", "(Increase)/decrease in capital work in progress", {"FY2019": 0, "FY2018": -1}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2026": -687, "FY2025": 16222, "FY2024": -22181, "FY2023": 3056, "FY2022": 23641, "FY2021": -30530, "FY2020": 30358, "FY2019": -16159, "FY2018": -49585}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issue of equity share capital", {"FY2020": 50000, "FY2019": 10000, "FY2018": 10000}),
    ("DATA", "Proceeds from Intra-group/Inter Bank borrowings", {"FY2023": 35000, "FY2022": 6011}),
    ("DATA", "Repayment of Inter Bank borrowings", {"FY2024": -35000, "FY2023": -6000}),
    # FY2026 only: the Bank took deposits from banks again in FY2026 (nil in FY2025), disclosed under
    # its own financing line "Proceeds from Deposits from Banks" rather than the intra-group/inter-bank
    # borrowings label used in FY2022/FY2023.
    ("DATA", "Proceeds from Deposits from Banks", {"FY2026": 59276}),
    ("DATA", "Interest Paid on Inter bank borrowings", {"FY2026": -349, "FY2025": -23, "FY2024": -1880, "FY2023": -124}),
    ("DATA", "Proceeds from/(Repayment to) Intra-group borrowings (net, see FY2018-FY2020 presentation note)", {"FY2020": -60565, "FY2019": -1867, "FY2018": 12161}),
    ("DATA", "Decrease in repurchase agreements", {"FY2022": -74, "FY2021": -3718}),
    ("DATA", "Proceeds from Repurchase agreements", {"FY2026": 30860, "FY2025": 15052}),
    ("DATA", "Repayment of Repurchase agreements", {"FY2026": -15052, "FY2023": -5145}),
    ("DATA", "Interest Paid on Repurchase agreements", {"FY2026": -737, "FY2025": -656, "FY2023": -29}),
    ("DATA", "Repayment of Lease (Principal amt)", {"FY2026": -604, "FY2025": -435, "FY2024": -193, "FY2023": -432, "FY2022": -448, "FY2021": -402, "FY2020": -360}),
    ("DATA", "Payment of Interest on Lease", {"FY2022": -24, "FY2021": -38, "FY2020": -53}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {"FY2026": 73394, "FY2025": 13938, "FY2024": -37073, "FY2023": 23270, "FY2022": 5465, "FY2021": -4158, "FY2020": -10977, "FY2019": 8133, "FY2018": 22161}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2026": 476, "FY2025": 5985, "FY2024": -10399, "FY2023": 13834, "FY2022": -947, "FY2021": -265, "FY2020": 2166, "FY2019": 2889, "FY2018": 436}),
    ("DATA", "Cash and cash equivalents at beginning of the year", {"FY2026": 14195, "FY2025": 8336, "FY2024": 18856, "FY2023": 5170, "FY2022": 6150, "FY2021": 6410, "FY2020": 4244, "FY2019": 1355, "FY2018": 919}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents (closing bridge)", {"FY2026": -327, "FY2025": -126, "FY2024": -122, "FY2023": -148, "FY2022": -33, "FY2021": 5, "FY2020": 0, "FY2019": 0, "FY2018": 0}),
    ("TOTAL", "Cash and cash equivalents at close of the year", {"FY2026": 14344, "FY2025": 14195, "FY2024": 8336, "FY2023": 18856, "FY2022": 5170, "FY2021": 6150, "FY2020": 6410, "FY2019": 4244, "FY2018": 1355}),
]

# £ translation plug (see FX_NOTE): the closing cash balance is a point-in-time
# stock figure, converted at that year-end's own SPOT rate (like the opening
# balance), while everything above it (net change, reported FX-effect line) is
# a flow converted at the AVERAGE rate - so the statement needs an explicit
# reconciling line to tie exactly, per the SMBC/Zenith precedent. Computed
# programmatically (not hand-derived) as closing(spot) - opening(spot) -
# net_change(avg) - reported_FX_effect(avg), per year.
_usd_by_label = {label: usd for _, label, usd in rows_usd}
_closing_spot = stock(_usd_by_label["Cash and cash equivalents at close of the year"])
_opening_spot = opening_cash(_usd_by_label["Cash and cash equivalents at beginning of the year"])
_net_change_avg = flow(_usd_by_label["Net increase/(decrease) in cash and cash equivalents"])
_fx_effect_avg = flow(_usd_by_label["Effects of exchange rate changes on cash and cash equivalents (closing bridge)"])
TRANSLATION_PLUG_GBP = {
    y: round(_closing_spot[y] - _opening_spot[y] - _net_change_avg[y] - _fx_effect_avg[y], 1)
    for y in YEARS
}

rows = []
for kind, label, usd in rows_usd:
    if kind == "SECTION":
        rows.append((kind, label, {}))
    elif label == "Cash and cash equivalents at beginning of the year":
        rows.append((kind, label, opening_cash(usd)))
    elif label == "Cash and cash equivalents at close of the year":
        rows.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", TRANSLATION_PLUG_GBP))
        rows.append((kind, label, stock(usd)))
    else:
        rows.append((kind, label, flow(usd)))

bw.add_cash_flow_sheet(
    title="Union Bank of India (UK) Limited — Statement of Cash Flows",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Asset Quality (loan book by IFRS 9 stage, £'000 converted from USD at
# each year-end's spot rate) - placed after Cash Flow Statement, before
# the Pillar 3 sheets.
# ---------------------------------------------------------------
AQ_USD = {
    "FY2021": dict(s1_gross=208754, s2_gross=25739, s3_gross=83031, total_gross=317525,
                   s1_ecl=-2691, s2_ecl=-2212, s3_ecl=-55865, total_ecl=-60767,
                   s1_net=206064, s2_net=23528, s3_net=27166, total_net=256758, fee_bridge=None),
    "FY2022": dict(s1_gross=256441, s2_gross=6689, s3_gross=41018, total_gross=304148,
                   s1_ecl=-1892, s2_ecl=-611, s3_ecl=-14815, total_ecl=-17318,
                   s1_net=254549, s2_net=6078, s3_net=26203, total_net=286830, fee_bridge=None),
    "FY2023": dict(s1_gross=286278, s2_gross=8700, s3_gross=40298, total_gross=335276,
                   s1_ecl=-789, s2_ecl=-48, s3_ecl=-15470, total_ecl=-16307,
                   s1_net=285489, s2_net=8652, s3_net=24828, total_net=318969, fee_bridge=None),
    "FY2024": dict(s1_gross=290852, s2_gross=19502, s3_gross=51973, total_gross=362327,
                   s1_ecl=-1776, s2_ecl=-349, s3_ecl=-19682, total_ecl=-21807,
                   s1_net=289076, s2_net=19153, s3_net=32291, total_net=340520, fee_bridge=-870),
    "FY2026": dict(s1_gross=291755, s2_gross=36641, s3_gross=38974, total_gross=367370,
                   s1_ecl=-1375, s2_ecl=-3422, s3_ecl=-13510, total_ecl=-18307,
                   s1_net=290380, s2_net=33219, s3_net=25464, total_net=349063, fee_bridge=-612),
    "FY2025": dict(s1_gross=281344, s2_gross=38295, s3_gross=42424, total_gross=362063,
                   s1_ecl=-1598, s2_ecl=-4440, s3_ecl=-14805, total_ecl=-20843,
                   s1_net=279746, s2_net=33855, s3_net=27619, total_net=341220, fee_bridge=-786),
    # FY2019/FY2020 added per HD-058 - own-report IFRS 9 stage disclosure (see AQ_SOURCES). FY2018 is genuinely
    # self-skipped (pre-IFRS-9-transition, no stage-based disclosure exists) - not included in this dict at all.
    "FY2020": dict(s1_gross=175505, s2_gross=51196, s3_gross=83756, total_gross=310457,
                   s1_ecl=-4586, s2_ecl=-2891, s3_ecl=-46708, total_ecl=-54184,
                   s1_net=170919, s2_net=48305, s3_net=37048, total_net=256273, fee_bridge=None),
    "FY2019": dict(s1_gross=222183, s2_gross=43388, s3_gross=63956, total_gross=329528,
                   s1_ecl=-416, s2_ecl=-35, s3_ecl=-27022, total_ecl=-27473,
                   s1_net=221767, s2_net=43353, s3_net=36935, total_net=302055, fee_bridge=None),
}


def aq_line(key):
    return {y: _stock1(d[key], y) for y, d in AQ_USD.items() if d.get(key) is not None}


def aq_ratio(numer_key, denom_key, sign=1):
    out = {}
    for y, d in AQ_USD.items():
        n, dn = d.get(numer_key), d.get(denom_key)
        if n is None or dn is None or dn == 0:
            continue
        out[y] = f"{sign * n / dn * 100:.2f}%"
    return out


bw.add_asset_quality_sheet(
    title="Union Bank of India (UK) Limited — Asset Quality (Loans and advances to customers, by IFRS 9 stage)",
    subtitle="£'000, converted from USD at each year-end's spot rate - see source note at bottom for FX methodology.",
    rows=[
        ("SECTION", "Gross carrying amount", {}),
        ("DATA", "Stage 1 (12-month ECL)", aq_line("s1_gross")),
        ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", aq_line("s2_gross")),
        ("DATA", "Stage 3 (credit-impaired)", aq_line("s3_gross")),
        ("TOTAL", "Total gross carrying amount", aq_line("total_gross")),
        ("SECTION", "Impairment provision (ECL)", {}),
        ("DATA", "Stage 1 impairment provision", aq_line("s1_ecl")),
        ("DATA", "Stage 2 impairment provision", aq_line("s2_ecl")),
        ("DATA", "Stage 3 impairment provision", aq_line("s3_ecl")),
        ("TOTAL", "Total impairment provision", aq_line("total_ecl")),
        ("SECTION", "Net amounts receivable", {}),
        ("DATA", "Stage 1 net amounts receivable", aq_line("s1_net")),
        ("DATA", "Stage 2 net amounts receivable", aq_line("s2_net")),
        ("DATA", "Stage 3 net amounts receivable", aq_line("s3_net")),
        ("TOTAL", "Total net amounts receivable (before processing-fee bridge)", aq_line("total_net")),
        ("DATA", "Less: unamortised portion of processing fees", aq_line("fee_bridge")),
        ("TOTAL", "Loans and advances to customers (per Balance Sheet)", {y: round(_stock1(d["total_net"], y) + (_stock1(d["fee_bridge"], y) if d.get("fee_bridge") else 0), 1) for y, d in AQ_USD.items()}),
        ("SECTION", "Derived ratios", {}),
        ("DATA", "NPL ratio (Stage 3 gross / Total gross)", aq_ratio("s3_gross", "total_gross")),
        ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", aq_ratio("s3_ecl", "s3_gross", sign=-1)),
        ("DATA", "Overall ECL coverage ratio (Total ECL / Total gross)", aq_ratio("total_ecl", "total_gross", sign=-1)),
    ],
    sources_text=AQ_SOURCES,
    first_col_width=70,
    source_height=380,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=48, source_height=130)


CET1_TIER1_USD = {"FY2025": 111479, "FY2024": 116706, "FY2023": 113622, "FY2022": 113013, "FY2021": 111081, "FY2020": 120703, "FY2019": 92980, "FY2018": 94472}
TOTAL_CAP_USD = {"FY2025": 111479, "FY2024": 116706, "FY2023": 113622, "FY2022": 113013, "FY2021": 115017, "FY2020": 120703, "FY2019": 92980, "FY2018": 94472}
RWA_USD = {"FY2025": 409920, "FY2024": 421729, "FY2023": 385186, "FY2022": 352650, "FY2021": 343147, "FY2020": 354835, "FY2019": 443828, "FY2018": 459690}
CAP_RATIO = {"FY2025": "27.20%", "FY2024": "27.67%", "FY2023": "29.50%", "FY2022": "32.05%", "FY2021": "32.37%", "FY2020": "34.02%", "FY2019": "20.95%", "FY2018": "20.55%"}

metric("CET1 Capital", "£'000 (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", stock(CET1_TIER1_USD))], p3_sources())
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CAP_RATIO)], p3_sources())
metric("Tier 1 Capital", "£'000 (conv. from USD)", [("Tier 1 capital", stock(CET1_TIER1_USD))], p3_sources(),
       note="Equal to CET1 capital in every year - the Bank holds no Additional Tier 1 (AT1) instruments.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CAP_RATIO)], p3_sources())
metric("Total Capital", "£'000 (conv. from USD)", [("Total capital", stock(TOTAL_CAP_USD))], p3_sources(),
       note="Equal to CET1/Tier 1 capital in every year except FY2021 (no Tier 2 instruments); FY2021 Total "
            "capital ($115,017k) exceeds CET1/Tier 1 ($111,081k), implying Tier 2 capital held that year which "
            "had run off by FY2022 (not explicitly explained in the source).")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {**CAP_RATIO, "FY2021": "33.52%"})], p3_sources())
metric("Total RWAs", "£'000 (conv. from USD)", [("Total risk-weighted exposure amount", stock(RWA_USD))], p3_sources())

# ---------------------------------------------------------------
# RWA Breakdown (placed right after Total RWAs, since it's itself a
# Pillar 3 disclosure) - £'000, converted from USD at each year-end's
# spot rate. See RWA_SOURCES for the FY2021/FY2022 presentation
# difference (pre-UK-OV1-template).
# ---------------------------------------------------------------
RWAB_USD = {
    "FY2021": dict(credit_std=314895, ccr=None, cva=1018, market=6003, op=21231, total=343147),
    "FY2022": dict(credit_std=330859, ccr=None, cva=347, market=1454, op=19990, total=352650),
    "FY2023": dict(credit_std=362454, ccr=1068, cva=334, market=587, op=21077, total=385186),
    "FY2024": dict(credit_std=391024, ccr=3199, cva=999, market=3774, op=23733, total=421729),
    "FY2025": dict(credit_std=375817, ccr=3925, cva=1213, market=2875, op=27304, total=409920),
    "FY2020": dict(credit_std=320681, ccr=None, cva=339, market=9686, op=24129, total=354835),
    "FY2019": dict(credit_std=400674, ccr=None, cva=318, market=21872, op=20964, total=443828),
    "FY2018": dict(credit_std=436976, ccr=None, cva=63, market=7238, op=15413, total=459690),
}


def rwab_line(key):
    return {y: _stock1(d[key], y) for y, d in RWAB_USD.items() if d.get(key) is not None}


bw.add_rwa_breakdown_sheet(
    title="Union Bank of India (UK) Limited — RWA Breakdown (UK OV1 - Overview of risk-weighted exposure amounts)",
    subtitle="£'000, converted from USD - see source note for the FY2021/FY2022 presentation difference (pre-UK-OV1-template).",
    rows=[
        ("DATA", "Credit risk (excluding CCR) / Standardised approach", rwab_line("credit_std")),
        ("DATA", "Counterparty credit risk (CCR)", rwab_line("ccr")),
        ("DATA", "  of which: Credit valuation adjustment (CVA)", rwab_line("cva")),
        ("DATA", "Market risk", rwab_line("market")),
        ("DATA", "Operational risk", rwab_line("op")),
        ("TOTAL", "Total RWAs (risk-weighted exposure amount)", rwab_line("total")),
    ],
    sources_text=RWA_SOURCES,
    first_col_width=64,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

metric(
    "Leverage Ratio", "£'000 / % (conv. from USD)",
    [
        ("Leverage ratio total exposure measure", stock({"FY2025": 496976, "FY2024": 511751, "FY2023": 475110, "FY2022": 411084, "FY2021": 402973, "FY2020": 410130, "FY2019": 460623, "FY2018": 445036})),
        ("Leverage ratio (%)", {"FY2025": "22.43%", "FY2024": "22.81%", "FY2023": "23.92%", "FY2022": "27.49%", "FY2021": "27.57%", "FY2020": "29.43%", "FY2019": "20.19%", "FY2018": "21.23%"}),
    ],
    p3_sources(),
    note="FY2021/FY2022 disclosed on the 'Basel III leverage ratio' basis (per that era's Pillar 3 template); "
         "FY2023 onward uses the 'UK KM1' leverage ratio template. Both are shown on the same row for continuity "
         "since the Bank's own reports do not draw an excluding/including-central-banks distinction in any year. "
         "FY2018-FY2020 also use the 'Basel III leverage ratio' basis.",
)

metric(
    "LCR", "£'000 / % (conv. from USD)",
    [
        ("Total high-quality liquid assets (HQLA), weighted value", stock({"FY2025": 43965, "FY2024": 43840, "FY2023": 48637, "FY2022": 36977, "FY2021": 64886, "FY2020": 30713, "FY2019": 49916, "FY2018": 24913})),
        ("Total net cash outflows, adjusted value", stock({"FY2025": 3017, "FY2024": 4815, "FY2023": 1637, "FY2022": 3888, "FY2021": 4486, "FY2020": 2067, "FY2019": 4485, "FY2018": 6086})),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "1457%", "FY2024": "910%", "FY2023": "2971%", "FY2022": "951%", "FY2021": "1446%", "FY2020": "1486%", "FY2019": "1113%", "FY2018": "409%"}),
    ],
    p3_sources(),
)

metric(
    "NSFR", "£'000 / % (conv. from USD)",
    [
        ("Total available stable funding", stock({"FY2025": 431914, "FY2024": 412656, "FY2023": 408381, "FY2022": 346323})),
        ("Total required stable funding", stock({"FY2025": 318358, "FY2024": 314809, "FY2023": 282448, "FY2022": 247487})),
        ("Net Stable Funding Ratio (%)", {"FY2025": "136%", "FY2024": "131%", "FY2023": "145%", "FY2022": "140%",
                                          "FY2021": "Not disclosed", "FY2020": "Not disclosed", "FY2019": "Not disclosed", "FY2018": "Not disclosed"}),
    ],
    p3_sources(),
    note="The UK NSFR regime took effect from 1 January 2022, so no FY2018-FY2021 figures exist (consistent with "
         "other banks in this series). FY2022 figures are as presented in the FY2023 Pillar 3 report's own "
         "comparative column (FY2022's own Pillar 3 report predates NSFR disclosure for this Bank).",
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(),
    per_note={"MREL Ratio": "No MREL disclosure (numeric or qualitative) or UK KM2 template found in any year's "
                             "Pillar 3 report - consistent with the Bank's small size relative to typical "
                             "MREL-in-scope thresholds."})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
cf_totals_usd = {
    "Net cash generated from/(used in) operating activities": {"FY2026": -72231, "FY2025": -24175, "FY2024": 48856, "FY2023": -12492, "FY2022": -30053, "FY2021": 34423, "FY2020": -17215, "FY2019": 10915, "FY2018": 27860},
    "Net cash generated from/(used in) investing activities": {"FY2026": -687, "FY2025": 16222, "FY2024": -22181, "FY2023": 3056, "FY2022": 23641, "FY2021": -30530, "FY2020": 30358, "FY2019": -16159, "FY2018": -49585},
    "Net cash generated from/(used in) financing activities": {"FY2026": 73394, "FY2025": 13938, "FY2024": -37073, "FY2023": 23270, "FY2022": 5465, "FY2021": -4158, "FY2020": -10977, "FY2019": 8133, "FY2018": 22161},
}
cf_close_usd = {"FY2026": 14344, "FY2025": 14195, "FY2024": 8336, "FY2023": 18856, "FY2022": 5170, "FY2021": 6150, "FY2020": 6410, "FY2019": 4244, "FY2018": 1355}

bs_overview_totals = [
    ("Total assets", bs_line("total_assets")),
    ("Loans and advances to customers", bs_line("lac")),
    ("Deposits from customers", bs_line("dep_cust")),
    ("Total Shareholder's equity", bs_line("total_equity")),
]
is_overview_totals = [
    ("Total Operating income", is_line("total_op_inc")),
    ("Operating expenses before impairment loss allowances", is_line("op_exp_before_impair")),
    ("Profit/(Loss) after tax", is_line("pat")),
]
eq_overview_open = {y: _stock1(EQ_BALANCES_USD[EQ_OPEN_KEY[y]][3], EQ_OPEN_SPOT_YEAR[y]) for y in YEARS}
eq_overview_close = {y: _stock1(EQ_BALANCES_USD[EQ_CLOSE_KEY[y]][3], y) for y in YEARS}
eq_overview_tci = {y: _flow1(EQ_MOVEMENTS_USD[y]["tci"], y) for y in YEARS}
eq_overview_totals = [
    ("Opening equity", eq_overview_open),
    ("Total comprehensive income/(loss) for the year", eq_overview_tci),
    ("Closing equity", eq_overview_close),
]

bw.add_overview_sheet(
    balance_sheet_totals=bs_overview_totals,
    balance_sheet_unit="£'000 (conv. from USD)",
    income_statement_totals=is_overview_totals,
    income_statement_unit="£'000 (conv. from USD)",
    equity_changes_totals=eq_overview_totals,
    equity_changes_unit="£'000 (conv. from USD)",
    cash_flow_totals=[(label, flow(vals)) for label, vals in cf_totals_usd.items()]
                      + [("Cash and cash equivalents at end of year", flow(cf_close_usd))],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CAP_RATIO),
        ("Tier 1 Ratio", CAP_RATIO),
        ("Total Capital Ratio", {**CAP_RATIO, "FY2021": "33.52%"}),
        ("Leverage Ratio", {"FY2025": "22.43%", "FY2024": "22.81%", "FY2023": "23.92%", "FY2022": "27.49%", "FY2021": "27.57%", "FY2020": "29.43%", "FY2019": "20.19%", "FY2018": "21.23%"}),
        ("LCR", {"FY2025": "1457%", "FY2024": "910%", "FY2023": "2971%", "FY2022": "951%", "FY2021": "1446%", "FY2020": "1486%", "FY2019": "1113%", "FY2018": "409%"}),
        ("NSFR", {"FY2025": "136%", "FY2024": "131%", "FY2023": "145%", "FY2022": "140%"}),
    ],
    note="FY2026 was added on 2026-09-15 from the Annual Report and Financial Statements for the year ended 31 "
         "March 2026 (approved 16 June 2026), published on the Bank's own disclosures/financial-reports page. "
         "IMPORTANT: FY2026 populates the Balance Sheet, Profit & Loss, Statement of Changes in Equity, Cash "
         "Flow Statement and Asset Quality sheets only. Every Pillar 3 sheet (CET1/Tier 1/Total Capital and "
         "their ratios, Total RWAs, RWA Breakdown, Leverage Ratio, LCR, NSFR) is blank for FY2026 because no "
         "FY2026 Pillar 3 Disclosure has been published yet and the FY2026 Annual Report gives no quantitative "
         "capital, RWA or liquidity figure anywhere - nothing was derived to fill the gap. "
         "Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation. All £ figures are converted from the Bank's native USD reporting (see Cash Flow Statement "
         "sheet's FX conversion note) - this conversion was not explicitly requested for this bank but applied for "
         "consistency with the rest of the series.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/UNION BANK OF INDIA UK FINANCIALS.xlsx")
