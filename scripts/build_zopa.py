import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017"]  # most recent first, calendar year-end (31 Dec)
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.datocms-assets.com/23873/1773841899-zopa_bank_ar25_web.pdf"
AR2024_URL = "https://www.datocms-assets.com/23873/1747055131-zopa-bank-2024-annual-report-signed-web-based.pdf"
AR2023_URL = "https://www.datocms-assets.com/23873/1713257733-zopa-group-2023-annual-report-signed_web-version.pdf"
AR2022_URL = "https://www.datocms-assets.com/23873/1694796852-zopa-bank-annual-report-2022-web.pdf"
AR2021_URL = "https://www.datocms-assets.com/23873/1658745948-zopa-bank-annual-report-2021.pdf"
AR2020_URL = "https://www.datocms-assets.com/23873/1658745479-zopa-bank-limited-annual-report-and-financial-statements-2020.pdf"

# FY2019/FY2018/FY2017: no zopa.com/datocms mirror was found (they predate the
# bank's public-facing annual-report web page) - sourced directly from
# Companies House's own scanned copy of each year's filed statutory accounts
# (company number 10627575), re-verified page-by-page via OCR against the
# rendered PDF, not assumed from an earlier scan's year signal alone.
CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/10627575/filing-history"
AR2019_URL = f"{CH_BASE}/MzI4NjUxOTIyNmFkaXF6a2N4/document?format=pdf&download=0"  # filed 21 Dec 2020, "Full accounts made up to 31 December 2019" (58pp)
AR2018_URL = f"{CH_BASE}/MzI0NjEzNjE0OWFkaXF6a2N4/document?format=pdf&download=0"  # filed 08 Oct 2019, "Full accounts made up to 31 December 2018" (45pp)
AR2017_URL = f"{CH_BASE}/MzIxNTk5NjMyMmFkaXF6a2N4/document?format=pdf&download=0"  # filed 04 Oct 2018, "Full accounts made up to 31 December 2017" (30pp)

P3_2025_URL = "https://www.datocms-assets.com/23873/1773842098-12-25-pillar-3-disclosures.pdf"
P3_2024_URL = "https://www.datocms-assets.com/23873/1745405670-2024-zopa-bank-pillar-3-disclosures.pdf"
P3_2023_URL = "https://www.datocms-assets.com/23873/1715596314-2023-pillar-3-disclosures-final.pdf"
P3_2022_URL = "https://www.datocms-assets.com/23873/1696603046-2022-pillar-3-disclosures-final_051023.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Zopa Bank Limited (FRN 800542, Companies House 10627575) is the PRA-authorised entity. It sits "
    "beneath a group holding company (Zopa Group Limited, later re-registered Zopa Group PLC) whose own separate "
    "consolidated accounts and Pillar 3 disclosures also exist - this workbook uses Zopa Bank Limited's own "
    "entity-level figures throughout (its own 'Statement of cash flows' in its own Annual Report and Accounts, "
    "and the dedicated 'Section 4: Disclosures for Zopa Bank Limited' within each year's Pillar 3 report, not the "
    "wider Group-level Section 3), consistent with the ring-fenced/individual-entity basis used elsewhere in this "
    "workbook series. Pillar 3 capital figures differ slightly from the Bank's own Annual Report & Accounts because "
    "they include audited profit and the full amount of Tier 2 capital (stated explicitly in each Pillar 3 report)."
)

HISTORICAL_FLOOR_NOTE = (
    "HISTORICAL FLOOR NOTE (independently re-verified, not assumed from Companies House incorporation date alone): "
    "Zopa Bank Limited was incorporated 20 February 2017 under the name 'Zopa Financial Services Limited' - a "
    "pre-launch entity with no banking licence, no customer lending and no regulatory capital reporting of any "
    "kind. It submitted its full Banking Licence application in February 2018 and was authorised WITH RESTRICTIONS "
    "in December 2018 (name changed to Zopa Bank Limited January 2019), during which it built its technology and "
    "began a small auto-loan book funded from its own capital, but could not yet take customer deposits. Full, "
    "unrestricted authorisation (mobilisation complete) was obtained in 2020, after which it began raising retail "
    "deposits (first shown on the FY2020 balance sheet). Consequently: FY2017's own real, audited financial "
    "statements exist (Balance Sheet/P&L/Equity/Cash Flow are populated below) but the entity had no banking "
    "business that year at all, so its Asset Quality sheet and all 11 Pillar 3 key metric sheets are genuinely "
    "blank for FY2017 - not a self-skip, an accurate reflection of 'not yet a bank'. FY2018 is the first year with "
    "any regulatory capital/RWA disclosure (unaudited Pillar 1 figures given in the Annual Report itself; Zopa had "
    "no standalone Pillar 3 document at this scale). FY2019 and FY2020 disclose a CET1 capital amount only (no "
    "RWA, no ratio, no Pillar 3 document) - genuinely absent from the source, not a transcription gap."
)

STATEMENTS_SOURCES = (
    "Sources - Zopa Bank Limited's own entity-level financial statements, £'000:\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025 - Statement of comprehensive income p.98, Statement of "
    f"financial position p.99, Statement of changes in equity p.100 - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Accounts 2023 - Statement of comprehensive income p.111, Statement of "
    f"financial position p.112, Statement of changes in equity p.113 - {AR2023_URL}\n"
    f"FY2021: Annual Report and Accounts 2021 - Statement of comprehensive income p.66, Statement of financial "
    f"position p.67, Statement of changes in equity p.68 - {AR2021_URL}\n"
    f"FY2020: Annual Report and Financial Statements 2020 (Companies House, accounts made up to 31 December 2020, "
    f"filed 2 Oct 2021) - Income statement p.27, Statement of Financial Position p.28, Statement of changes in "
    f"equity p.29 - {AR2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements 2019 (Companies House filing, 58pp) - Income statement p.21, "
    f"Statement of Financial Position p.22, Statement of changes in equity p.23 - {AR2019_URL}\n"
    f"FY2018: Annual Report and Financial Statements 2018 (Companies House filing, 45pp) - Statement of "
    f"comprehensive income p.15, Statement of financial position p.16, Statement of changes in equity p.17 - "
    f"{AR2018_URL}\n"
    f"FY2017: Zopa Financial Services Limited Annual Report and Financial Statements 2017 (Companies House filing, "
    f"30pp; entity's own accounts for the period 20 Feb-31 Dec 2017) - Statement of comprehensive income p.10, "
    f"Statement of financial position p.11, Statement of changes in equity p.12 - {AR2017_URL}. FY2017 balance "
    f"sheet/equity figures shown here use the rounded £'000 comparative column as re-printed in the FY2018 Annual "
    f"Report (p.16-17, cross-checked and matched exactly), since FY2017's own accounts were prepared in whole £, "
    f"not £'000 - this is a rounding basis only, not a different underlying transaction set.\n\n"
    + ENTITY_NOTE + "\n\n" + HISTORICAL_FLOOR_NOTE
    + "\n\nPRESENTATION NOTE: line-item structure and labels differ by report vintage (e.g. 'Total operating "
    "income' block only appears from FY2024 onward; the equity statement gained separate 'Share premium' and "
    "'Other equity instruments' columns only in FY2025, when the Bank issued AT1 instruments and restructured its "
    "share capital via a capital reduction - both columns are blank/nil for FY2017-FY2024, not a gap). FY2017/"
    "FY2018 predate the Bank's IFRS-style statement format entirely and use their own period's line items "
    "('Revenue'/'Cost of sales'/'Gross profit or loss', a single aggregated 'Trade and other payables' liability "
    "line, and non-current 'Loans and receivables' that is a rental deposit, not customer lending) - shown here as "
    "their own dedicated rows, blank in every other year, rather than force-mapped into later years' bank-specific "
    "line items. Every year's own Profit/(loss) before tax ties exactly to the pre-existing Cash Flow Statement "
    "sheet's own opening reconciliation line. Blank cells indicate that year's own statement did not disclose/"
    "include that specific line at all; a printed em-dash in the source was transcribed as 0 (an explicit nil, not "
    "a gap). Small (<£1k, rounding-only) cross-footing gaps in FY2017 (a whole-£ original converted independently "
    "to £'000 on each line) are reproduced exactly as computed, not forced to tie - e.g. Total liabilities (£6,583k) "
    "+ Total equity (-£3,806k) = £2,777k vs. stated Total assets £2,778k."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Zopa Bank Limited's own Statement of cash flows, £'000:\n"
    f"FY2025 & FY2024: Zopa Bank Limited Annual Report and Accounts 2025, p.101 (Statement of cash flows) - {AR2025_URL}\n"
    f"FY2023: Zopa Bank Limited Annual Report and Accounts 2023, p.114 (Statement of cash flows) - {AR2023_URL} "
    f"(cross-checked against its comparative appearance in the 2024 Annual Report, p.111 - {AR2024_URL} - matched exactly)\n"
    f"FY2022: Zopa Bank Limited Annual Report and Accounts 2022, p.95 (Statement of cash flows) - {AR2022_URL} "
    f"(cross-checked against its comparative appearance in the 2023 Annual Report, p.114 - matched exactly)\n"
    f"FY2021: Zopa Bank Limited Annual Report and Accounts 2021, p.69 (Statement of cash flows) - {AR2021_URL} "
    f"(cross-checked against its comparative appearance in the 2022 Annual Report, p.95 - matched exactly)\n"
    f"FY2020: Annual Report and Financial Statements 2020, p.30 (Statement of cash flows) - {AR2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements 2019, p.24 (Statement of cash flows) - {AR2019_URL} "
    f"(cross-checked against its comparative appearance in the 2020 report - matched exactly)\n"
    f"FY2018: Annual Report and Financial Statements 2018, p.18 (Statement of cash flows) - {AR2018_URL}\n"
    f"FY2017: Zopa Financial Services Limited Annual Report and Financial Statements 2017, p.13 - {AR2017_URL} "
    f"(re-presented in whole-£'000-rounded form as the comparative column of the FY2018 report, p.18 - both "
    "versions used together below; see PRESENTATION NOTE)\n"
    "Note: the 2021 Annual Report states 'the statement of cash flows has been represented' vs. its own prior-year "
    "presentation (details in that report's note 1.9) - not a concern for the FY2021-FY2025 figures shown here, "
    "which are all on a mutually consistent, cross-checked basis. Separately, FY2021's own opening cash balance "
    "(£69,456k) is £88k above FY2020's own closing cash balance (£69,368k) shown here - FY2020's own note explicitly "
    "states its closing cash EXCLUDES £88k of restricted balances, which the FY2021 presentation folds back in; "
    "both figures are reproduced exactly as each report states them, not forced to tie.\n\n"
    + ENTITY_NOTE + "\n\n"
    + "PRESENTATION NOTE: FY2017-FY2020 predate the current reconciliation format and are mapped onto the existing "
    "rows as follows - each year's 'Profit/(loss) before tax' plus a residual 'Non-cash items' figure (the "
    "difference between that year's own single 'cash generated from operations' reconciliation line and "
    "profit/(loss) before tax) plus 'Changes in operating assets and liabilities' (that year's own operating "
    "asset/liability movement lines, summed) together foot exactly to that year's own stated net operating cash "
    "flow. FY2018-FY2020 also disclose a small 'Interest received' investing line and (FY2019/FY2020 only) "
    "'Interest paid on intercompany loans' within financing, shown as their own rows, blank in other years."
)


def p3_sources(page="14-15"):
    return (
        "Sources - Zopa Bank Limited basis (Section 4: 'Disclosures for Zopa Bank Limited', within each year's "
        "'Zopa Group' Pillar 3 Disclosures document):\n"
        f"FY2025 & FY2024: Pillar 3 Disclosures, year ended 31 December 2025, p.14-15 (Table 5: UK KM1 - Key "
        f"metrics table) - {P3_2025_URL}\n"
        f"FY2023: Pillar 3 Disclosures, year ended 31 December 2023, p.14-15 (Table 5: UK KM1) - {P3_2023_URL} "
        f"(cross-checked against its comparative in the 2024 report, p.14 - {P3_2024_URL} - matched exactly)\n"
        f"FY2022: Pillar 3 Disclosures, year ended 31 December 2022, p.13-14 (Table 5: UK KM1) - {P3_2022_URL} "
        f"(cross-checked against its comparative in the 2023 report, p.14 - matched exactly)\n"
        f"FY2021: as the comparative ('Dec-21') column in the Pillar 3 Disclosures, year ended 31 December 2022, "
        f"p.13-14 (Table 5: UK KM1) - {P3_2022_URL} (Zopa's FY2021 Pillar 3 document is titled/structured as a "
        "Group-only disclosure with no equivalent Bank-specific KM1 section, so the FY2022 report's own comparative "
        "column is used as the citable Bank-level source for FY2021 instead)\n"
        f"FY2020: two documents, and they say different things - both are used.\n"
        f"  (a) CET1 CAPITAL (the £ amount): note 24(d) 'Capital risk and management', Annual Report and "
        f"Financial Statements 2020, p.61 - {AR2020_URL}. That note prints a CET1 build-up ending 'Total Common "
        f"equity Tier 1 capital (CET1) 115,439' and, on the line below, 'Total capital resources 115,439'. The "
        f"two being equal is the Bank's own statement that it held no AT1 and no Tier 2 at 31 December 2020.\n"
        f"  (b) RWA AND RATIOS, ADDED 2026-09-18 (interior-gap sweep): the Annual Report and Accounts 2021's "
        f"Financial review, 'Capital position remains very strong' table, printed p.22, carries a full BANK-level "
        f"2020 COMPARATIVE COLUMN - RWAs £390.5m, CET1 ratio 29%, leverage ratio 38% - alongside its 2021 column, "
        f"and a companion 'Liquidity' table on the same page gives NSFR 152% and LCR 13,597% for 2020 - "
        f"{AR2021_URL}. These are comparatives and are labelled as such on every row that uses them.\n"
        f"  WHAT THIS CORRECTS: this note used to read 'no standalone Pillar 3 document existed at this scale' and "
        f"'No RWA or capital ratio of any kind was disclosed that year'. The first clause is still unproven either "
        f"way (zopa.com returned HTTP 503 to every rung of the fetching ladder on 2026-09-18 and the Internet "
        f"Archive was globally offline, so no document index could be read - an access limit, not a finding). The "
        f"second clause was simply wrong: it was true of the FY2020 Annual Report, which was the only document "
        f"searched, and the FY2021 Annual Report published all of it a year later.\n"
        f"FY2019: within note 24(d) 'Capital risk and management' of the Annual Report and Financial "
        f"Statements 2019, p.54 - {AR2019_URL}. CET1 capital only (£13,254k, again equal to 'Total capital "
        f"resources'). NO RWA AND NO CAPITAL RATIO - and unlike FY2020 this was tested properly: that filing is "
        f"an IMAGE-ONLY SCAN with a 58-character text layer across 58 pages, so a text search of it proves "
        f"nothing. All 58 pages were rendered at 200 dpi and OCR'd on 2026-09-18; the strings 'risk weighted', "
        f"'RWA', 'capital ratio' and 'leverage ratio' appear nowhere in the document, and the FY2020 Annual "
        f"Report (also an image-only scan, OCR'd the same way) carries no 2019 comparative for them either. "
        f"Whether a Zopa Group Pillar 3 covering 2019 exists is UNKNOWN - see the access limit noted for FY2020.\n"
        f"FY2018: within the Strategic Report's KPI table and note (unaudited Pillar 1 figures, explicitly marked "
        f"as such and 'not covered by the external auditor's opinion') of the Annual Report and Financial "
        f"Statements 2018, p.4 and p.35 - {AR2018_URL}. This is the first year any RWA/capital ratio was disclosed "
        "(the Bank's first restricted banking licence was granted in December 2018).\n"
        "FY2017: not applicable - Zopa Financial Services Limited had no banking licence and no regulatory capital "
        "reporting of any kind that year (see HISTORICAL FLOOR NOTE on the Balance Sheet sheet)."
    )


bw = BankWorkbook(bank_name="Zopa Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="1B4332")

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Statement of financial position). Total assets =
# Total liabilities + Total equity for every year. Ties exactly to the
# Statement of Changes in Equity sheet's own closing balances every year.
# FY2017 has a small (<£1k), independently-rounded cross-footing gap - see
# source note, not a plug.
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents / balances - Central bank(s)", {"FY2025": 2225694, "FY2024": 2761315, "FY2023": 1336105, "FY2022": 1397062, "FY2021": 191148, "FY2020": 35024}),
    ("DATA", "Cash and cash equivalents / balances - Other bank(s)", {"FY2025": 82231, "FY2024": 58428, "FY2023": 66063, "FY2022": 21429, "FY2021": 30366, "FY2020": 22189, "FY2019": 2577, "FY2018": 2402, "FY2017": 194}),
    ("DATA", "Debt securities (cash-like)", {"FY2025": 30572, "FY2024": 0, "FY2023": 13988, "FY2022": 13386, "FY2021": 16244, "FY2020": 12243, "FY2019": 243, "FY2018": 10019}),
    ("DATA", "Amounts due from other Group undertakings", {"FY2025": 39724, "FY2024": 642, "FY2023": 1431, "FY2022": 0, "FY2021": 1808, "FY2020": 3080, "FY2019": 646}),
    ("DATA", "Derivative financial instruments", {"FY2025": 141, "FY2024": 5946, "FY2023": 7974, "FY2022": 8346, "FY2021": 11}),
    ("DATA", "Loans and advances to customers", {"FY2025": 3506654, "FY2024": 2865635, "FY2023": 2478213, "FY2022": 1937964, "FY2021": 1173013, "FY2020": 225390, "FY2019": 16372}),
    ("DATA", "Investment securities (held at FVOCI)", {"FY2025": 1253125, "FY2024": 455157, "FY2023": 80710, "FY2022": 0}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 8578, "FY2024": 6445, "FY2023": 4891, "FY2022": 5007, "FY2021": 2489, "FY2020": 1480, "FY2019": 1634}),
    ("DATA", "Other assets", {"FY2025": 22470, "FY2024": 22259, "FY2023": 13814, "FY2022": 28358, "FY2021": 1960, "FY2020": 567, "FY2019": 103, "FY2018": 976}),
    ("DATA", "Current tax asset", {"FY2020": 522, "FY2019": 585}),
    ("DATA", "Property, plant and equipment", {"FY2025": 1676, "FY2024": 1150, "FY2023": 1307, "FY2022": 788, "FY2021": 1054, "FY2020": 1376, "FY2019": 1417, "FY2018": 1733, "FY2017": 1372}),
    ("DATA", "Right-of-use assets", {"FY2025": 17109, "FY2024": 2137, "FY2023": 4135, "FY2022": 1559, "FY2021": 3526, "FY2020": 511, "FY2019": 889}),
    ("DATA", "Intangible assets", {"FY2025": 43949, "FY2024": 32360, "FY2023": 16055, "FY2022": 9435, "FY2021": 9352, "FY2020": 12183, "FY2019": 6384, "FY2018": 6228, "FY2017": 914}),
    ("DATA", "Deferred tax assets", {"FY2025": 11788, "FY2024": 17573, "FY2023": 24401, "FY2022": 0}),
    ("DATA", "Loans and receivables (non-current; pre-banking-licence entity - a rental deposit, not customer lending)", {"FY2018": 7244, "FY2017": 234}),
    ("TOTAL", "Total assets", {"FY2025": 7243711, "FY2024": 6229047, "FY2023": 4049087, "FY2022": 3423334, "FY2021": 1430971, "FY2020": 314565, "FY2019": 30850, "FY2018": 28602, "FY2017": 2778}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Derivative financial instruments", {"FY2025": 6020, "FY2024": 1087, "FY2023": 3388, "FY2022": 757, "FY2021": 0, "FY2020": 97}),
    ("DATA", "Amounts due to banks", {"FY2025": 50783, "FY2024": 157227, "FY2023": 159239, "FY2022": 180074, "FY2021": 175193, "FY2020": 11}),
    ("DATA", "Deposits by customers", {"FY2025": 6393598, "FY2024": 5455740, "FY2023": 3357724, "FY2022": 2922845, "FY2021": 968000, "FY2020": 177823}),
    ("DATA", "Amounts due to other Group undertakings", {"FY2025": 34361, "FY2024": 4, "FY2023": 615, "FY2022": 106, "FY2021": 17000, "FY2020": 3128, "FY2019": 7867}),
    ("DATA", "Subordinated liabilities", {"FY2025": 76086, "FY2024": 76086, "FY2023": 78817, "FY2022": 0}),
    ("DATA", "Accruals", {"FY2025": 17498, "FY2024": 16747, "FY2023": 12483, "FY2022": 10449, "FY2021": 8887, "FY2020": 3446, "FY2019": 1512}),
    ("DATA", "Provisions", {"FY2025": 10521, "FY2024": 3110, "FY2023": 2131, "FY2022": 1370, "FY2021": 1372, "FY2020": 224, "FY2019": 103}),
    ("DATA", "Other liabilities", {"FY2025": 15313, "FY2024": 20016, "FY2023": 27237, "FY2022": 7087, "FY2021": 5113, "FY2020": 1747, "FY2019": 928}),
    ("DATA", "Lease liabilities", {"FY2025": 16314, "FY2024": 1739, "FY2023": 3038, "FY2022": 1039, "FY2021": 3151, "FY2020": 467, "FY2019": 802}),
    ("DATA", "Trade and other payables (aggregate; pre-banking-licence/restricted-licence entity, not yet split by category)", {"FY2018": 6788, "FY2017": 6583}),
    ("TOTAL", "Total liabilities", {"FY2025": 6620494, "FY2024": 5731756, "FY2023": 3644672, "FY2022": 3123727, "FY2021": 1178716, "FY2020": 186943, "FY2019": 11212, "FY2018": 6788, "FY2017": 6583}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called-up share capital", {"FY2025": 68542, "FY2024": 554819, "FY2023": 486319, "FY2022": 421319, "FY2021": 349319, "FY2020": 192319, "FY2019": 54160, "FY2018": 39160, "FY2017": 0}),
    ("DATA", "Share premium", {"FY2025": 6146, "FY2024": 0}),
    ("DATA", "Other equity instruments", {"FY2025": 78298, "FY2024": 0}),
    ("DATA", "Other reserves", {"FY2025": 21826, "FY2024": 9428, "FY2023": 6829, "FY2022": 5902, "FY2021": 6180, "FY2020": 4324, "FY2019": 1786, "FY2018": 1088, "FY2017": 195}),
    ("DATA", "Retained earnings/(accumulated losses)", {"FY2025": 448405, "FY2024": -66956, "FY2023": -88733, "FY2022": -127614, "FY2021": -103244, "FY2020": -69021, "FY2019": -36308, "FY2018": -18434, "FY2017": -4001}),
    ("TOTAL", "Total equity", {"FY2025": 623217, "FY2024": 497291, "FY2023": 404415, "FY2022": 299607, "FY2021": 252255, "FY2020": 127622, "FY2019": 19638, "FY2018": 21814, "FY2017": -3806}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 7243711, "FY2024": 6229047, "FY2023": 4049087, "FY2022": 3423334, "FY2021": 1430971, "FY2020": 314565, "FY2019": 30850, "FY2018": 28602, "FY2017": 2778}),
]

bw.add_balance_sheet_sheet(
    title="Zopa Bank Limited — Balance Sheet",
    subtitle="Zopa Bank Limited (entity-level), £'000. Total assets = Total liabilities + Total equity for every "
              "year (FY2017 has a <£1k rounding-only gap - see source note). Ties exactly to the Statement of "
              "Changes in Equity sheet's own closing Total equity every year. FY2017 is Zopa Financial Services "
              "Limited, the same Companies House entity pre-banking-licence - see HISTORICAL FLOOR NOTE at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=420,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Statement of comprehensive income). Every year's
# own Profit/(loss) before tax ties exactly to the Cash Flow Statement
# sheet's own opening reconciliation line.
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Revenue (pre-banking-licence entity; intercompany services + minor interest, not split by type)", {"FY2018": 4584, "FY2017": 69}),
    ("DATA", "Cost of sales (pre-banking-licence entity)", {"FY2018": -98, "FY2017": -81}),
    ("TOTAL", "Gross profit/(loss) (pre-banking-licence entity)", {"FY2018": 4486, "FY2017": -12}),
    ("DATA", "Interest income", {"FY2025": 598989, "FY2024": 503794, "FY2023": 349917, "FY2022": 200049, "FY2021": 61146, "FY2020": 7228, "FY2019": 640}),
    ("DATA", "Interest expense", {"FY2025": -239341, "FY2024": -224454, "FY2023": -136957, "FY2022": -33937, "FY2021": -5466, "FY2020": -610, "FY2019": -173}),
    ("TOTAL", "Net interest income", {"FY2025": 359648, "FY2024": 279340, "FY2023": 212960, "FY2022": 166112, "FY2021": 55680, "FY2020": 6618, "FY2019": 467}),
    ("DATA", "Fee and commission income", {"FY2025": 15232, "FY2024": 14347, "FY2023": 13020, "FY2022": 8133, "FY2021": 2432, "FY2020": 152}),
    ("DATA", "Fee and commission expense", {"FY2025": -16633, "FY2024": -14033, "FY2023": -10684, "FY2022": -9040, "FY2021": -3275, "FY2020": -2072, "FY2019": -450}),
    ("TOTAL", "Net fee and commission income/(expense)", {"FY2025": -1401, "FY2024": 314, "FY2023": 2336, "FY2022": -907, "FY2021": -843, "FY2020": -1920, "FY2019": -450}),
    ("DATA", "Other operating income", {"FY2025": 266, "FY2024": 2478, "FY2023": 1261, "FY2022": 279, "FY2021": 12807, "FY2020": 16114, "FY2019": 12491}),
    ("DATA", "Net gains/(losses) on derecognition of financial assets at amortised cost", {"FY2025": 212, "FY2024": 10095, "FY2023": 2984, "FY2022": -21049, "FY2021": -2234}),
    ("DATA", "Net losses on disposal of property, plant and equipment", {"FY2021": 0}),
    ("DATA", "Changes in fair value of financial instruments measured at FVTPL", {"FY2025": 827, "FY2024": 5561, "FY2023": 2889, "FY2022": 6089, "FY2021": -182, "FY2020": 71}),
    ("DATA", "Other interest receivable and similar income (pre-banking-licence/restricted-licence entity)", {"FY2018": 26}),
    ("TOTAL", "Total operating income", {"FY2025": 359552, "FY2024": 297788, "FY2023": 222430, "FY2022": 150524, "FY2021": 65228, "FY2020": 20883, "FY2019": 12508}),
    ("SECTION", "Operating expenses and impairment", {}),
    ("DATA", "Operating expenses", {"FY2025": -136999, "FY2024": -107992, "FY2023": -83266, "FY2022": -75578, "FY2021": -57640, "FY2020": -38567, "FY2019": -30798, "FY2018": -18895, "FY2017": -3990}),
    ("TOTAL", "Net operating income/(loss)", {"FY2025": 222553, "FY2024": 189796, "FY2023": 139164, "FY2022": 74946, "FY2021": 7588, "FY2020": -17684, "FY2019": -18290, "FY2018": -14409, "FY2017": -4001}),
    ("DATA", "Change in expected credit losses and other credit impairment charges", {"FY2025": -167501, "FY2024": -156229, "FY2023": -122817, "FY2022": -100609, "FY2021": -41812, "FY2020": -12788, "FY2019": -162, "FY2018": -49}),
    ("DATA", "Change in provisions for other liabilities and charges", {"FY2025": -10200, "FY2024": -2017, "FY2023": -530, "FY2022": -325, "FY2021": 0}),
    ("DATA", "Loss on disposal of assets", {"FY2020": -82}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": 44852, "FY2024": 31550, "FY2023": 15817, "FY2022": -25988, "FY2021": -34224, "FY2020": -30554, "FY2019": -18452, "FY2018": -14432, "FY2017": -4001}),
    ("DATA", "Taxation", {"FY2025": -11472, "FY2024": -9773, "FY2023": 23064, "FY2022": 0, "FY2021": 1, "FY2020": 9, "FY2019": 585, "FY2018": 0, "FY2017": 0}),
    ("TOTAL", "Profit/(loss) after tax", {"FY2025": 33380, "FY2024": 21777, "FY2023": 38881, "FY2022": -25988, "FY2021": -34223, "FY2020": -30545, "FY2019": -17867, "FY2018": -14432, "FY2017": -4001}),
    ("SECTION", "Other comprehensive income/(loss)", {}),
    ("DATA", "Changes in fair value of investment securities held at FVOCI", {"FY2025": 187, "FY2024": -46, "FY2023": -49}),
    ("TOTAL", "Total other comprehensive income/(loss)", {"FY2025": 187, "FY2024": -46, "FY2023": -49}),
    ("TOTAL", "Total comprehensive income/(loss)", {"FY2025": 33567, "FY2024": 21731, "FY2023": 38832, "FY2022": -25988, "FY2021": -34223, "FY2020": -30545, "FY2019": -17867, "FY2018": -14432, "FY2017": -4001}),
]

bw.add_income_statement_sheet(
    title="Zopa Bank Limited — Profit & Loss",
    subtitle="Zopa Bank Limited (entity-level), £'000. All profits/losses are from continuing operations. "
              "FY2017-FY2022 disclose no other comprehensive income items at all (confirmed via each source "
              "statement's own text, not a gap) - Total comprehensive income equals Profit/(loss) after tax "
              "exactly in those years. Every year's Profit/(loss) before tax ties exactly to the Cash Flow "
              "Statement sheet's own opening reconciliation line. FY2017/FY2018 use their own period's distinct "
              "line items (Revenue/Cost of sales/Gross profit) - see PRESENTATION NOTE on the Balance Sheet sheet.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=420,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity - chronological, ties exactly to
# the Balance Sheet sheet's own Total equity every year and chains
# correctly across all boundaries, back to incorporation (20 February
# 2017). Zero undocumented plug rows.
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Called-up share capital", "Share premium", "Other equity instruments", "Other reserves", "Retained earnings/(accumulated losses)", "Total equity"]

equity_rows = [
    ("TOTAL", "Balance at 20 February 2017 (incorporation, as Zopa Financial Services Limited)", (0, None, None, 0, 0, 0)),
    ("DATA", "Total comprehensive expense", (None, None, None, None, -4001, -4001)),
    ("DATA", "Issue of new shares", (0, None, None, None, None, 0)),
    ("DATA", "Share based payment charge", (None, None, None, 195, None, 195)),
    ("TOTAL", "Balance at 31 December 2017 / 1 January 2018", (0, None, None, 195, -4001, -3806)),
    ("DATA", "Changes on initial application of new accounting standards", (None, None, None, None, -1, -1)),
    ("TOTAL", "Balance at 1 January 2018 (restated)", (0, None, None, 195, -4002, -3807)),
    ("DATA", "Total comprehensive expense", (None, None, None, None, -14432, -14432)),
    ("DATA", "Issue of share capital", (39160, None, None, None, None, 39160)),
    ("DATA", "Share based payment charge", (None, None, None, 893, None, 893)),
    ("TOTAL", "Balance at 31 December 2018 / 1 January 2019", (39160, None, None, 1088, -18434, 21814)),
    ("DATA", "Change on initial application of IFRS 16", (None, None, None, None, -7, -7)),
    ("TOTAL", "Balance at 1 January 2019 (restated)", (39160, None, None, 1088, -18441, 21807)),
    ("DATA", "Total comprehensive expense", (None, None, None, None, -17867, -17867)),
    ("DATA", "Issue of share capital", (15000, None, None, None, None, 15000)),
    ("DATA", "Share based payment charge", (None, None, None, 698, None, 698)),
    ("TOTAL", "Balance at 31 December 2019 / 1 January 2020", (54160, None, None, 1786, -36308, 19638)),
    ("DATA", "Total comprehensive expense", (None, None, None, None, -30545, -30545)),
    ("DATA", "Issue of share capital", (138159, None, None, None, None, 138159)),
    ("DATA", "Share based payment charge", (None, None, None, 920, None, 920)),
    ("DATA", "Transfer of assets from related party", (None, None, None, None, -2168, -2168)),
    ("DATA", "Capital contribution", (None, None, None, 1618, None, 1618)),
    ("TOTAL", "Balance at 31 December 2020 / 1 January 2021", (192319, None, None, 4324, -69021, 127622)),
    ("DATA", "Total comprehensive loss", (None, None, None, None, -34223, -34223)),
    ("DATA", "Shares issued", (157000, None, None, None, None, 157000)),
    ("DATA", "Net share option movements", (None, None, None, 1856, None, 1856)),
    ("TOTAL", "Balance at 31 December 2021 / 1 January 2022", (349319, None, None, 6180, -103244, 252255)),
    ("DATA", "Total comprehensive loss", (None, None, None, None, -25988, -25988)),
    ("DATA", "Shares issued", (72000, None, None, None, None, 72000)),
    ("DATA", "Net share option movements", (None, None, None, 1340, None, 1340)),
    ("DATA", "Transfer of capital contribution reserve", (None, None, None, -1618, 1618, 0)),
    ("TOTAL", "Balance at 31 December 2022 / 1 January 2023", (421319, None, None, 5902, -127614, 299607)),
    ("DATA", "Profit for the year", (None, None, None, None, 38881, 38881)),
    ("DATA", "Other comprehensive loss relating to investment securities held at FVOCI", (None, None, None, -49, None, -49)),
    ("TOTAL", "Total comprehensive income", (None, None, None, -49, 38881, 38832)),
    ("DATA", "Shares issued", (65000, None, None, None, None, 65000)),
    ("DATA", "Net share option movements", (None, None, None, 976, None, 976)),
    ("TOTAL", "Balance at 31 December 2023 / 1 January 2024", (486319, None, None, 6829, -88733, 404415)),
    ("DATA", "Profit for the year", (None, None, None, None, 21777, 21777)),
    ("DATA", "Other comprehensive loss relating to investment securities", (None, None, None, -46, None, -46)),
    ("TOTAL", "Total comprehensive income", (None, None, None, -46, 21777, 21731)),
    ("DATA", "Shares issued", (68500, None, None, None, None, 68500)),
    ("DATA", "Net share option movements", (None, None, None, 2645, None, 2645)),
    ("TOTAL", "Balance at 31 December 2024 / 1 January 2025", (554819, 0, 0, 9428, -66956, 497291)),
    ("DATA", "Profit for the year", (None, None, None, None, 33380, 33380)),
    ("DATA", "Other comprehensive income relating to investment securities", (None, None, None, 187, None, 187)),
    ("TOTAL", "Total comprehensive income", (None, None, None, 187, 33380, 33567)),
    ("DATA", "Shares issued", (854, 6146, None, None, None, 7000)),
    ("DATA", "Capital reduction", (-487131, None, None, None, 487131, 0)),
    ("DATA", "Issue of other equity instruments", (None, None, 78298, None, None, 78298)),
    ("DATA", "Coupons paid on other equity instruments", (None, None, None, None, -5150, -5150)),
    ("DATA", "Net share option movements", (None, None, None, 12211, None, 12211)),
    ("TOTAL", "Balance at 31 December 2025", (68542, 6146, 78298, 21826, 448405, 623217)),
]

bw.add_equity_changes_sheet(
    title="Zopa Bank Limited — Statement of Changes in Equity",
    subtitle="Zopa Bank Limited (entity-level), £'000, chronological (oldest to newest), back to incorporation on "
              "20 February 2017. Zero undocumented plug rows across all years - ties exactly to the Balance Sheet "
              "sheet's own Total equity every year and chains correctly across every boundary. 'Share premium' and "
              "'Other equity instruments' columns only exist from FY2025 (blank/nil in earlier years, not a gap).",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=54,
    source_height=420,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit/(loss) before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 44852, "FY2024": 31550, "FY2023": 15817, "FY2022": -25988, "FY2021": -34224, "FY2020": -30554, "FY2019": -18452, "FY2018": -14432, "FY2017": -4001}),
    ("DATA", "Non-cash items", {"FY2025": 108122, "FY2024": 67370, "FY2023": 66198, "FY2022": 92460, "FY2021": 50828, "FY2020": 5009, "FY2019": 3297, "FY2018": 689, "FY2017": 4500}),
    ("DATA", "Changes in operating assets and liabilities", {"FY2025": 216056, "FY2024": 1640591, "FY2023": -133115, "FY2022": 1082800, "FY2021": -192441, "FY2020": -31433, "FY2019": -10439, "FY2018": -7060}),
    ("DATA", "Current tax expense", {"FY2025": -5687, "FY2024": -3439, "FY2023": -1337}),
    ("DATA", "Tax received", {"FY2021": 0}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 363343, "FY2024": 1736072, "FY2023": -52437, "FY2022": 1149272, "FY2021": -175837, "FY2020": -56978, "FY2019": -25594, "FY2018": -20803, "FY2017": 500}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of investment securities", {"FY2025": -948990, "FY2024": -431925, "FY2023": -80367}),
    ("DATA", "Investment securities matured during the year", {"FY2025": 154254, "FY2024": 67356}),
    ("DATA", "Disposal of property, plant and equipment", {"FY2021": 0}),
    ("DATA", "Purchase of non-current assets from related party", {"FY2021": 0}),
    ("DATA", "Purchase of debt securities", {"FY2018": -10019}),
    ("DATA", "Interest received", {"FY2020": 24, "FY2019": 31, "FY2018": 26}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -1486, "FY2024": -659, "FY2023": -1167, "FY2022": -610, "FY2021": -519, "FY2020": -221, "FY2019": -184, "FY2018": -740, "FY2017": -66}),
    ("DATA", "Purchase and development of intangible assets", {"FY2025": -21194, "FY2024": -23775, "FY2023": -10779, "FY2022": -3948, "FY2021": -2036, "FY2020": -2675, "FY2019": -1307, "FY2018": -5416, "FY2017": -5}),
    ("DATA", "Purchase of loans and receivables (pre-banking-licence entity - a rental deposit)", {"FY2017": -234}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -817416, "FY2024": -389003, "FY2023": -92313, "FY2022": -4558, "FY2021": -2555, "FY2020": -2872, "FY2019": -1460, "FY2018": -16149, "FY2017": -305}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Shares issued", {"FY2025": 7000, "FY2024": 68500, "FY2023": 65000, "FY2022": 72000, "FY2021": 157000, "FY2020": 138159, "FY2019": 15000, "FY2018": 39160, "FY2017": 0}),
    ("DATA", "Issuance of other equity instruments", {"FY2025": 80000}),
    ("DATA", "Transaction costs on issuance of other equity instruments", {"FY2025": -1702}),
    ("DATA", "Coupon payment on other equity instruments", {"FY2025": -5150}),
    ("DATA", "Proceeds from issuance of subordinated liabilities", {"FY2023": 75000}),
    ("DATA", "Repayment of TFSME borrowings", {"FY2025": -150000}),
    ("DATA", "Proceeds from ILTR borrowings", {"FY2025": 50000}),
    ("DATA", "Change in TFSME and ILTR borrowings", {"FY2023": -19316, "FY2022": -3791}),
    ("DATA", "Change in amounts due to banks", {"FY2021": 175182}),
    ("DATA", "Change in non-trading amounts due to and from other Group undertakings", {"FY2025": -5393, "FY2024": 4, "FY2023": -74, "FY2022": -16507, "FY2021": 15144, "FY2020": -11499, "FY2019": 2522}),
    ("DATA", "Interest paid on intercompany loans", {"FY2020": -178, "FY2019": -153}),
    ("DATA", "Cash payments/principal elements on lease liabilities", {"FY2025": -1928, "FY2024": -1822, "FY2023": -1745, "FY2022": -2297, "FY2021": -632}),
    ("TOTAL", "Net cash (used in)/generated from financing activities", {"FY2025": -27173, "FY2024": 66682, "FY2023": 118865, "FY2022": 49405, "FY2021": 346694, "FY2020": 126482, "FY2019": 17369, "FY2018": 39160, "FY2017": 0}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -481246, "FY2024": 1413751, "FY2023": -25885, "FY2022": 1194119, "FY2021": 168302, "FY2020": 66632, "FY2019": -9685, "FY2018": 2208, "FY2017": 194}),
    ("DATA", "Cash and cash equivalents at start of year", {"FY2025": 2819743, "FY2024": 1405992, "FY2023": 1431877, "FY2022": 237758, "FY2021": 69456, "FY2020": 2736, "FY2019": 12421, "FY2018": 194, "FY2017": 0}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 2338497, "FY2024": 2819743, "FY2023": 1405992, "FY2022": 1431877, "FY2021": 237758, "FY2020": 69368, "FY2019": 2736, "FY2018": 2402, "FY2017": 194}),
]

bw.add_cash_flow_sheet(
    title="Zopa Bank Limited — Cash Flow Statement",
    subtitle="Zopa Bank Limited (entity-level), £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality. Credit performance of loans and advances to
# customers by IFRS 9 stage (on-balance sheet only), Note 15/37.1.11-12
# (FY2025-FY2022), the FY2021 rating-distribution tier table (Note
# 34.1.10, aggregated across tiers), and the equivalent stage tables in
# each year's own Annual Report notes for FY2020-FY2018. FY2017 is
# genuinely blank - Zopa Financial Services Limited had no banking
# licence and no customer lending that year (see HISTORICAL FLOOR NOTE
# on the Balance Sheet sheet) - not a self-skip.
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - Zopa Bank Limited entity-level credit quality disclosures (on-balance sheet loans and advances to "
    "customers only), £'000:\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025, Note 37.1.11 'Credit performance' and Note 37.1.12 'Credit "
    f"quality', p.158 - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Accounts 2023, Note 37.1.11 'Credit performance' and Note 37.1.12 'Credit "
    f"quality', p.167 - {AR2023_URL}\n"
    f"FY2021: Annual Report and Accounts 2021, Note 34.1.10 'Rating distribution' (Zopa risk ratings tier table), "
    f"p.107-108 - aggregated across all 4 Tier bands to a single Stage 1/2/3 figure, since no consolidated by-"
    f"stage summary table exists in this earlier report vintage - {AR2021_URL}\n"
    f"FY2020: Annual Report and Financial Statements 2020, Note 13 'Loans and advances to customers' and the ECL/"
    f"gross-carrying-amount stage tables in Note 24(a), p.56-57 - {AR2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements 2019, Note 24(a) 'Credit risk' stage tables, p.49-50 - "
    f"{AR2019_URL} (cross-checked against its comparative appearance in the 2020 Annual Report, p.56-57 - matched "
    f"exactly)\n"
    f"FY2018: Annual Report and Financial Statements 2018, Note 3 'Management of financial risks' stage tables, "
    f"p.30 - {AR2018_URL} (cross-checked against its comparative appearance in the 2019 Annual Report, p.49-50 - "
    "matched exactly)\n"
    "FY2017: not applicable - Zopa Financial Services Limited had no banking licence and no customer lending that "
    "year (the only 'loan' on its FY2017 balance sheet is a rental deposit - see Balance Sheet sheet). Left blank, "
    "not a self-skip.\n\n"
    + ENTITY_NOTE
    + "\n\nGENUINE, IMMATERIAL DISCREPANCY (not forced to tie): FY2023's on-balance sheet net figure "
    "(£2,475,917k) is £2,296k below the Balance Sheet's own Loans and advances to customers line (£2,478,213k); "
    "FY2022's (£1,939,768k) is £1,804k above the Balance Sheet's own figure (£1,937,964k). Both gaps are under "
    "0.1% of the balance and are reproduced exactly as each note states them, not plugged. FY2025/FY2024 tie "
    "exactly once the Balance Sheet's own fair value hedge adjustment (+£4,037k / -£714k, see Balance Sheet "
    "sheet note 14) is added back; FY2021/FY2020/FY2019/FY2018 tie exactly with no adjustment needed."
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, gross carrying amount by IFRS 9 stage (on-balance sheet)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 3337595, "FY2024": 2728099, "FY2023": 2336414, "FY2022": 1794856, "FY2021": 1151567, "FY2020": 229988, "FY2019": 15180, "FY2018": 6853}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 252301, "FY2024": 228781, "FY2023": 214897, "FY2022": 216507, "FY2021": 55351, "FY2020": 7346, "FY2019": 1330, "FY2018": 310}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 181656, "FY2024": 110477, "FY2023": 97665, "FY2022": 65747, "FY2021": 14802, "FY2020": 732, "FY2019": 70, "FY2018": 13}),
    ("DATA", "POCI (purchased or originated credit-impaired)", {"FY2025": 0, "FY2024": 450, "FY2023": 1305, "FY2022": 3743, "FY2021": 4725}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 3771552, "FY2024": 3067807, "FY2023": 2650281, "FY2022": 2080853, "FY2021": 1226445, "FY2020": 238066, "FY2019": 16580, "FY2018": 7176}),
    ("SECTION", "ECL allowance by IFRS 9 stage (on-balance sheet)", {}),
    ("DATA", "Stage 1 allowance", {"FY2025": 75836, "FY2024": 58414, "FY2023": 44313, "FY2022": 38924, "FY2021": 27069, "FY2020": 9649, "FY2019": 98, "FY2018": 29}),
    ("DATA", "Stage 2 allowance", {"FY2025": 71644, "FY2024": 67210, "FY2023": 60155, "FY2022": 53373, "FY2021": 15713, "FY2020": 2075, "FY2019": 65, "FY2018": 15}),
    ("DATA", "Stage 3 allowance", {"FY2025": 121455, "FY2024": 75822, "FY2023": 69847, "FY2022": 48454, "FY2021": 10650, "FY2020": 952, "FY2019": 45, "FY2018": 6}),
    ("DATA", "POCI allowance", {"FY2024": 12, "FY2023": 49, "FY2022": 334}),
    ("TOTAL", "Total ECL allowance", {"FY2025": 268935, "FY2024": 201458, "FY2023": 174364, "FY2022": 141085, "FY2021": 53432, "FY2020": 12676, "FY2019": 208, "FY2018": 50}),
    ("TOTAL", "Net loans and advances to customers (on-balance sheet)", {"FY2025": 3502617, "FY2024": 2866349, "FY2023": 2475917, "FY2022": 1939768, "FY2021": 1173013, "FY2020": 225390, "FY2019": 16372, "FY2018": 7126}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross)", {"FY2025": "4.82%", "FY2024": "3.60%", "FY2023": "3.69%", "FY2022": "3.16%", "FY2021": "1.21%", "FY2020": "0.31%", "FY2019": "0.42%", "FY2018": "0.18%"}),
    ("DATA", "Coverage ratio (Total ECL allowance / Total gross)", {"FY2025": "7.13%", "FY2024": "6.57%", "FY2023": "6.58%", "FY2022": "6.78%", "FY2021": "4.36%", "FY2020": "5.32%", "FY2019": "1.25%", "FY2018": "0.70%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross)", {"FY2025": "66.86%", "FY2024": "68.63%", "FY2023": "71.52%", "FY2022": "73.70%", "FY2021": "71.95%", "FY2020": "130.05%", "FY2019": "64.29%", "FY2018": "46.15%"}),
]

bw.add_asset_quality_sheet(
    title="Zopa Bank Limited — Asset Quality",
    subtitle="Zopa Bank Limited (entity-level), £'000, on-balance sheet loans and advances to customers only. "
              "Ties exactly to Balance Sheet net loans for FY2025/FY2024 (after the fair value hedge adjustment) "
              "and every other disclosed year; FY2023/FY2022 have a small (<0.1%) genuine gap - see source note, "
              "not a plug. FY2017 is genuinely blank (no banking licence, no customer lending that year - see "
              "HISTORICAL FLOOR NOTE on the Balance Sheet sheet), not a self-skip. FY2020's unusually high >100% "
              "Stage 3 coverage ratio is reproduced exactly as the source states it (a rapidly-growing, then-"
              "young auto-loan book with a high loss-given-default assumption that year, per the source note).",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=76,
    source_height=360,
    unit_suffix=" (£'000)",
)

KM1_SOURCES = (
    "Sources — Zopa Bank Limited's own entity-level Table 5: UK KM1 – Key metrics table, £m; the wider "
    "Group Table 2 in the same documents was deliberately not used:\n"
    f"FY2025: 2025 Pillar 3, printed pp.14-15 — {P3_2025_URL}\n"
    f"FY2024: 2024 Pillar 3, printed pp.14-15 — {P3_2024_URL}\n"
    f"FY2023: 2023 Pillar 3, printed pp.14-15 — {P3_2023_URL}\n"
    f"FY2022: 2022 Pillar 3, printed pp.13-14 — {P3_2022_URL}\n"
    f"FY2021: 2022 Pillar 3 comparative column, printed pp.13-14 — {P3_2022_URL}\n\n"
    "Each FY2022-FY2025 column uses its own edition; FY2021 uses the first later-edition comparative because "
    "Zopa had not yet published an entity-level UK KM1. Row 9 for FY2021 carries a literal '-' because the "
    "2022 edition prints a dash in that column - re-read on 2026-09-18, where the same row prints '1.00%' "
    "for 2022 beside it - and a dash is the Bank saying the buffer did not apply, not a figure it withheld. "
    "The "
    "source's explicit 'n/a' leverage and LCR cells remain 'n/a'. Rows 18-20 were omitted from the 2022 "
    "template because the Bank states NSFR was not applicable until 1 January 2023, so FY2021/FY2022 are blank. "
    "No UK KM1 exists for FY2017-FY2020 and those columns remain blank. Zopa's live investor-information page "
    "was checked on 17 September 2026: FY2025 remains the newest annual Pillar 3 edition; the H1 2026 disclosure "
    "is interim and does not replace a year-end column."
    "\n\n"
    "ROWS 1, 2 AND 3 ARE EQUAL IN THE SOURCE FOR FY2022 AND FY2021 - READ FROM THE DOCUMENT ON 2026-09-18 AND "
    "RECORDED HERE SO THE QUESTION IS NOT RE-OPENED. The Pillar 3 Disclosures 2022 prints 290 on rows 1, 2 and 3 "
    "at Dec-22 and 243 at Dec-21, with no Additional Tier 1 or Tier 2 line populated. ENTITY: that edition prints "
    "the template TWICE - Table 2 headed 'GROUP' and Table 5 headed 'Bank'. This sheet is the BANK series. The "
    "two tables agree at Dec-22 (290 on both) and differ at Dec-21 (Group 255, Bank 243), so the Dec-21 column is "
    "the only place where the choice of table is visible at all. FY2024 and FY2023 are DISTINCT in the source "
    "(448 against 523; 364 against 439) and are held that way here.\n"
)

km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1 Common Equity Tier 1 (CET1) capital (£m)", {"FY2025": 489, "FY2024": 448, "FY2023": 364, "FY2022": 290, "FY2021": 243}),
    ("DATA", "2 Tier 1 capital (£m)", {"FY2025": 567, "FY2024": 448, "FY2023": 364, "FY2022": 290, "FY2021": 243}),
    ("DATA", "3 Total capital (£m)", {"FY2025": 642, "FY2024": 523, "FY2023": 439, "FY2022": 290, "FY2021": 243}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4 Total risk-weighted exposure amount (£m)", {"FY2025": 3364, "FY2024": 2670, "FY2023": 2205, "FY2022": 1663, "FY2021": 1060}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5 Common Equity Tier 1 ratio (%)", {"FY2025": "14.54%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%"}),
    ("DATA", "6 Tier 1 ratio (%)", {"FY2025": "16.87%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%"}),
    ("DATA", "7 Total capital ratio (%)", {"FY2025": "19.10%", "FY2024": "19.57%", "FY2023": "19.90%", "FY2022": "17.44%", "FY2021": "22.92%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a Additional CET1 SREP requirements (%)", {"FY2025": "1.30%", "FY2024": "1.96%", "FY2023": "1.96%", "FY2022": "1.79%", "FY2021": "1.79%"}),
    ("DATA", "UK 7b Additional AT1 SREP requirements (%)", {"FY2025": "0.43%", "FY2024": "0.65%", "FY2023": "0.65%", "FY2022": "0.60%", "FY2021": "0.60%"}),
    ("DATA", "UK 7c Additional T2 SREP requirements (%)", {"FY2025": "0.58%", "FY2024": "0.87%", "FY2023": "0.87%", "FY2022": "0.80%", "FY2021": "0.80%"}),
    ("DATA", "UK 7d Total SREP own funds requirements (%)", {"FY2025": "10.31%", "FY2024": "11.48%", "FY2023": "11.48%", "FY2022": "11.18%", "FY2021": "11.18%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8 Capital conservation buffer (%)", {"FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "9 Institution specific countercyclical capital buffer (%)", {"FY2025": "2.00%", "FY2024": "2.00%", "FY2023": "2.00%", "FY2022": "1.00%", "FY2021": "-"}),
    ("DATA", "11 Combined buffer requirement (%)", {"FY2025": "4.50%", "FY2024": "4.50%", "FY2023": "4.50%", "FY2022": "3.50%", "FY2021": "2.50%"}),
    ("DATA", "UK 11a Overall capital requirements (%)", {"FY2025": "14.81%", "FY2024": "15.98%", "FY2023": "15.98%", "FY2022": "14.68%", "FY2021": "13.96%"}),
    ("DATA", "12 CET1 available after meeting the total SREP own funds requirements (%)", {"FY2025": "8.74%", "FY2024": "10.31%", "FY2023": "10.05%", "FY2022": "11.16%", "FY2021": "16.63%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13 Total exposure measure excluding claims on central banks (£m)", {"FY2025": 4998, "FY2024": 3445, "FY2023": 2699, "FY2022": 2024, "FY2021": "n/a"}),
    ("DATA", "14 Leverage ratio excluding claims on central banks (%)", {"FY2025": "11.36%", "FY2024": "12.99%", "FY2023": "13.48%", "FY2022": "14.34%", "FY2021": "n/a"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15 Total high-quality liquid assets (HQLA) (Weighted value - average) (£m)", {"FY2025": 2970, "FY2024": 2347, "FY2023": 1701, "FY2022": 626, "FY2021": "n/a"}),
    ("DATA", "UK 16a Cash outflows - Total weighted value (£m)", {"FY2025": 755, "FY2024": 550, "FY2023": 312, "FY2022": 97, "FY2021": "n/a"}),
    ("DATA", "UK 16b Cash inflows - Total weighted value (£m)", {"FY2025": 140, "FY2024": 120, "FY2023": 79, "FY2022": 36, "FY2021": "n/a"}),
    ("DATA", "16 Total net cash outflows (adjusted value) (£m)", {"FY2025": 614, "FY2024": 430, "FY2023": 233, "FY2022": 61, "FY2021": "n/a"}),
    ("DATA", "17 Liquidity coverage ratio (%)", {"FY2025": "484%", "FY2024": "546%", "FY2023": "730%", "FY2022": "1,033%", "FY2021": "n/a"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18 Total available stable funding (£m)", {"FY2025": 5761, "FY2024": 4918, "FY2023": 3701}),
    ("DATA", "19 Total required stable funding (£m)", {"FY2025": 2562, "FY2024": 2162, "FY2023": 1785}),
    ("DATA", "20 NSFR ratio (%)", {"FY2025": "225%", "FY2024": "227%", "FY2023": "207%"}),
]

bw.add_km1_sheet(
    title="Zopa Bank Limited — KM1 Key Metrics",
    subtitle="The Bank-only Table 5 UK KM1, reproduced in its own row order, row numbering and precision. Amounts are £m; LCR/NSFR figures are trailing-period averages as described by Zopa.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    source_height=310,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Zopa Bank Limited basis, {unit}" if unit else "Zopa Bank Limited basis",
                         rows_data, sources_text, note=note, first_col_width=44, source_height=200)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 489, "FY2024": 448, "FY2023": 364, "FY2022": 290, "FY2021": 243, "FY2020": 115.4, "FY2019": 13.3, "FY2018": 15.6})],
    p3_sources(),
    note="FY2017: not applicable - Zopa Financial Services Limited had no banking licence and no regulatory "
         "capital of any kind that year. FY2018 is the first year of any capital disclosure (restricted banking "
         "licence granted December 2018).",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "14.54%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%", "FY2020": "29%", "FY2018": "19%"})],
    p3_sources(),
    note="FY2020 ADDED 2026-09-18: 29%, printed as the 2020 comparative in the Annual Report and Accounts 2021's "
         "Financial review capital table (p.22), a Bank-level table headed 'Bank | 2021 | 2020 | Change'. It is a "
         "comparative, not an own-year disclosure, and is whole-percent as the Bank prints it - note that the "
         "same table's 2021 column reads 23% where this row's FY2021 figure, taken from the KM1 template, is "
         "22.92%, so the two sources agree to the Bank's own rounding. FY2019 remains genuinely blank: its "
         "Annual Report (an image-only scan, OCR'd in full) discloses CET1 capital only, no RWA and no ratio, "
         "and no later report carries a 2019 comparative for either. "
         "FY2018's 19% is an unaudited Pillar 1 figure the Bank itself flags as 'not covered by the external "
         "auditor's opinion'. FY2017: not applicable (no banking licence that year).",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 567, "FY2024": 448, "FY2023": 364, "FY2022": 290, "FY2021": 243, "FY2020": 115.4, "FY2019": 13.3, "FY2018": 15.6})],
    p3_sources(),
    note="Tier 1 = CET1 in every disclosed year except FY2025, where the Bank issued £80m of other (AT1) equity "
         "instruments during the year (see Cash Flow Statement sheet), taking Tier 1 above CET1 for the first "
         "time. FY2017: not applicable (no banking licence that year).",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "16.87%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%", "FY2020": "29%", "FY2018": "19%"})],
    p3_sources(),
    note="FY2020 ADDED 2026-09-18: 29%. Zopa published ONE capital ratio for 2020 - the CET1 ratio, as the 2020 "
         "comparative in the Annual Report and Accounts 2021 (p.22, see CET1 Ratio sheet). It is repeated here "
         "because the Bank's own FY2020 capital note states that CET1 WAS its entire capital base: note 24(d) of "
         "the Annual Report and Financial Statements 2020, p.61, prints 'Total Common equity Tier 1 capital "
         "(CET1) 115,439' and 'Total capital resources 115,439' - no AT1, no Tier 2. Tier 1 therefore equals CET1 "
         "that year as a matter of the Bank's disclosure, which is the same reasoning this workbook already "
         "applies to the FY2020 cell of the Tier 1 Capital and Total Capital sheets (all three carry £115.4m). "
         "Nothing here is computed from RWA. FY2019 remains blank: no ratio of any kind was published for it "
         "(see CET1 Ratio sheet note). FY2017: not applicable (no banking licence that year).",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 642, "FY2024": 523, "FY2023": 439, "FY2022": 290, "FY2021": 243, "FY2020": 115.4, "FY2019": 13.3, "FY2018": 15.6})],
    p3_sources(),
    note="Total capital includes Tier 2 capital (subordinated debt) from FY2023 onward - £75m issued, of which "
         "£63m/£72m/£73m was eligible as at FY2023/FY2024/FY2025 respectively (stated in each year's Pillar 3 "
         "report). No Tier 2 capital existed in FY2018-FY2022, so Total Capital = Tier 1 = CET1 in those years. "
         "FY2017: not applicable (no banking licence that year).",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "19.10%", "FY2024": "19.57%", "FY2023": "19.90%", "FY2022": "17.44%", "FY2021": "22.92%", "FY2020": "29%", "FY2018": "19%"})],
    p3_sources(),
    note="FY2020 ADDED 2026-09-18: 29%, on exactly the same footing as the Tier 1 Ratio sheet's FY2020 cell - "
         "the only 2020 ratio Zopa published is the CET1 ratio (Annual Report and Accounts 2021, p.22, 2020 "
         "comparative column), and the FY2020 capital note (Annual Report 2020, p.61) prints total capital "
         "resources equal to CET1 to the pound, so Total capital ratio and CET1 ratio are the same published "
         "number that year. Not derived from RWA. FY2019 remains blank. FY2017: not "
         "applicable (no banking licence that year).",
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 3364, "FY2024": 2670, "FY2023": 2205, "FY2022": 1663, "FY2021": 1060, "FY2020": 390.5, "FY2018": 82.5})],
    p3_sources(),
    note="FY2020 ADDED 2026-09-18: £390.5m, printed as the 2020 comparative in the Annual Report and Accounts "
         "2021's Financial review capital table (p.22). The note this replaces said no RWA figure appeared "
         "'anywhere in the document' - true of the FY2020 Annual Report, which was the document searched, and "
         "false of the Bank, which published the figure in the following year's report. The two columns of that "
         "table are internally consistent: it states RWA growth of '+171%' between them, and 390.5 x 2.71 = "
         "1,058, against the FY2021 figure of £1,059.3m already on this row. "
         "FY2019 is NOT disclosed: its own Annual Report is an image-only scan whose 58 pages were rendered and "
         "OCR'd in full on 2026-09-18 with no RWA figure anywhere, and no later report carries a 2019 "
         "comparative. FY2018's £82.5m is an unaudited "
         "Pillar 1 figure. FY2017: not applicable (no banking licence that year).",
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Zopa Bank Limited basis, Table 4: UK OV1 - Overview of risk weighted exposure amounts (within "
    "each year's 'Section 4: Disclosures for Zopa Bank Limited'), £m:\n"
    f"FY2025 & FY2024: Pillar 3 Disclosures, year ended 31 December 2025, p.14 - {P3_2025_URL}\n"
    f"FY2023: Pillar 3 Disclosures, year ended 31 December 2023, p.14 - {P3_2023_URL} (cross-checked against its "
    f"comparative in the 2024 report - matched exactly)\n"
    f"FY2022: Pillar 3 Disclosures, year ended 31 December 2022, p.13 - {P3_2022_URL} (cross-checked against its "
    f"comparative in the 2023 report - matched exactly)\n"
    f"FY2021: as the comparative ('2021') column in the Pillar 3 Disclosures, year ended 31 December 2022, p.13 - "
    f"{P3_2022_URL} (same access-gap basis as the FY2021 Total RWAs figure elsewhere in this workbook - no "
    "standalone FY2021 OV1 table exists, so the FY2022 report's own comparative column is used)\n"
    "Category sums round to the Total RWAs figure each year (a <£1m rounding gap in FY2024 only, both figures "
    "reproduced exactly as the source states them).\n"
    "FY2020/FY2019/FY2018/FY2017: not disclosed - no OV1-style RWA category breakdown exists in any Zopa Bank "
    "Limited document for these years (FY2018's single Pillar 1 RWA total is on the Total RWAs sheet, with no "
    "component split available; FY2017 is not applicable, no banking licence that year).\n\n"
    + ENTITY_NOTE
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk RWA (excluding CCR)", {"FY2025": 2804, "FY2024": 2249, "FY2023": 1921, "FY2022": 1502, "FY2021": 898}),
    ("DATA", "Counterparty Credit Risk RWA", {"FY2025": 0.6, "FY2024": 1, "FY2023": 0.5, "FY2022": 0.3, "FY2021": 0}),
    ("DATA", "Securitisation exposures RWA (non-trading book, after the cap)", {"FY2025": 23, "FY2024": 0}),
    ("DATA", "Operational risk RWA", {"FY2025": 537, "FY2024": 421, "FY2023": 283, "FY2022": 161, "FY2021": 162}),
    ("TOTAL", "Total RWAs", {"FY2025": 3364, "FY2024": 2670, "FY2023": 2205, "FY2022": 1663, "FY2021": 1060}),
]

bw.add_rwa_breakdown_sheet(
    title="Zopa Bank Limited — RWA Breakdown",
    subtitle="Zopa Bank Limited basis, £m. Category sums tie to the Total RWAs sheet's own figures every year "
              "(a <£1m rounding gap in FY2024 only). Securitisation exposures only appear from FY2025. No "
              "category breakdown was ever disclosed for FY2017-FY2020 - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=64,
    source_height=300,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 4998, "FY2024": 3445, "FY2023": 2699, "FY2022": 2024}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "11.36%", "FY2024": "12.99%", "FY2023": "13.48%", "FY2022": "14.34%", "FY2021": "Not disclosed"}),
        ("Leverage ratio (%) - Annual Report basis, year-end (see note)", {"FY2021": "20%", "FY2020": "38%"}),
    ],
    p3_sources(),
    note="TWO ROWS, TWO DOCUMENTS. The Pillar 3 row is the KM1 template's 'excluding claims on central banks' "
         "measure, and its Dec-21 comparative column really does print 'n/a' for both the exposure measure and "
         "the ratio, with no explanation given.\n"
         "THE THIRD ROW WAS ADDED 2026-09-18 AND CORRECTS THIS NOTE'S OWN PREVIOUS CLAIM, which read 'no "
         "leverage ratio of any kind appears in any FY2017-FY2020 Annual Report either'. It does. The Annual "
         "Report and Accounts 2021, Financial review, 'Capital position remains very strong' table on printed "
         "p.22, publishes a Bank-level leverage ratio of 20% for 2021 and 38% for 2020, next to the RWA and "
         "CET1-ratio figures this workbook now uses on other sheets. The claim was a statement about the "
         "documents that had been searched - the FY2017-FY2020 reports - presented as a statement about the "
         "Bank, and the answer was in the FY2021 report all along.\n"
         "The two rows are NOT merged and neither is adjusted toward the other: the Annual Report figures are "
         "year-end and whole-percent, and the Bank never says whether its own KPI leverage ratio uses the "
         "central-bank-claims exclusion, so they are not known to be the same measure. FY2020 is a comparative "
         "column of the FY2021 report.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 2970, "FY2024": 2347, "FY2023": 1701, "FY2022": 626}),
        ("Total net cash outflows, adjusted value", {"FY2025": 614, "FY2024": 430, "FY2023": 233, "FY2022": 61}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "484%", "FY2024": "546%", "FY2023": "730%", "FY2022": "1,033%", "FY2021": "Not disclosed"}),
        ("Liquidity Coverage Ratio (%) - Annual Report basis, year-end position (see note)", {"FY2021": "9,360%", "FY2020": "13,597%"}),
    ],
    p3_sources(),
    note="TWO BASES, AND THE BANK NAMES THE DIFFERENCE ITSELF. The Pillar 3 LCR row is a 12-month simple average "
         "of month-end observations, which the Pillar 3 report says 'differs to the metrics reported in the Bank "
         "ARA, which present the position at the year-end date'. LCR is a new Pillar 3 disclosure from the FY2022 "
         "report onward and no earlier Pillar 3 comparative was provided, which is why that row starts at "
         "FY2022.\n"
         "THE YEAR-END ROW WAS ADDED 2026-09-18. The Annual Report and Accounts 2021's Financial review "
         "'Liquidity' table, printed p.22, publishes exactly the ARA-basis metric the Pillar 3 footnote refers "
         "to: LCR 9,360% for 2021 and 13,597% for 2020 (FY2020 being that table's comparative column). This "
         "note previously said LCR was 'Not disclosed for FY2017-FY2021'; that was true of the Pillar 3 reports "
         "and false of the Annual Reports. The two rows are kept separate because averaged and year-end LCR are "
         "different measures - the year-end figures are enormous because Zopa Bank was holding very large "
         "central-bank balances against a small deposit book at those dates, not because either number is "
         "wrong.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2025": 5761, "FY2024": 4918, "FY2023": 3701}),
        ("Total required stable funding", {"FY2025": 2562, "FY2024": 2162, "FY2023": 1785}),
        ("NSFR ratio (%)", {"FY2025": "225%", "FY2024": "227%", "FY2023": "207%", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
        ("Net Stable Funding Ratio (%) - Annual Report basis (see note)", {"FY2021": "136%", "FY2020": "152%"}),
    ],
    p3_sources(),
    note="NSFR was not a REQUIRED Pillar 3 disclosure until 1 January 2023 (PRA PS22/21), which is why the "
         "template row above starts at FY2023 and marks FY2021/FY2022 'Not applicable'. That is a statement "
         "about the disclosure obligation and it stands.\n"
         "IT IS NOT A STATEMENT ABOUT THE BANK, and this note used to end 'so no FY2017-FY2022 figures exist', "
         "which is a different claim and a false one. Corrected 2026-09-18: Zopa published an NSFR voluntarily, "
         "before it had to. The Annual Report and Accounts 2021's Financial review 'Liquidity' table, printed "
         "p.22, gives a Bank-level Net Stable Funding Ratio of 136% for 2021 and 152% for 2020 (comparative "
         "column) - added as the row above. Not required to disclose is not the same as did not disclose.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed" for y in YEARS if y != "FY2017"})],
    p3_sources(),
    note="No MREL disclosure of any kind (numeric or qualitative) was found in Zopa Bank Limited's Annual Reports "
         "or Pillar 3 reports for any year reviewed (FY2018-FY2025) - unlike some smaller banks in this workbook "
         "series, no report explicitly states an SNCI/below-threshold exemption reason, it is simply absent from "
         "every KM1 template and surrounding narrative. FY2017: not applicable (no banking licence that year).",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 7243711, "FY2024": 6229047, "FY2023": 4049087, "FY2022": 3423334, "FY2021": 1430971, "FY2020": 314565, "FY2019": 30850, "FY2018": 28602, "FY2017": 2778}),
        ("Loans and advances to customers", {"FY2025": 3506654, "FY2024": 2865635, "FY2023": 2478213, "FY2022": 1937964, "FY2021": 1173013, "FY2020": 225390, "FY2019": 16372}),
        ("Deposits by customers", {"FY2025": 6393598, "FY2024": 5455740, "FY2023": 3357724, "FY2022": 2922845, "FY2021": 968000, "FY2020": 177823}),
        ("Total equity", {"FY2025": 623217, "FY2024": 497291, "FY2023": 404415, "FY2022": 299607, "FY2021": 252255, "FY2020": 127622, "FY2019": 19638, "FY2018": 21814, "FY2017": -3806}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 359552, "FY2024": 297788, "FY2023": 222430, "FY2022": 150524, "FY2021": 65228, "FY2020": 20883, "FY2019": 12508}),
        ("Profit/(loss) before tax", {"FY2025": 44852, "FY2024": 31550, "FY2023": 15817, "FY2022": -25988, "FY2021": -34224, "FY2020": -30554, "FY2019": -18452, "FY2018": -14432, "FY2017": -4001}),
        ("Profit/(loss) after tax", {"FY2025": 33380, "FY2024": 21777, "FY2023": 38881, "FY2022": -25988, "FY2021": -34223, "FY2020": -30545, "FY2019": -17867, "FY2018": -14432, "FY2017": -4001}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 497291, "FY2024": 404415, "FY2023": 299607, "FY2022": 252255, "FY2021": 127622, "FY2020": 19638, "FY2019": 21814, "FY2018": -3806, "FY2017": 0}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 33567, "FY2024": 21731, "FY2023": 38832, "FY2022": -25988, "FY2021": -34223, "FY2020": -30545, "FY2019": -17867, "FY2018": -14432, "FY2017": -4001}),
        ("Other equity movements, net", {"FY2025": 92359, "FY2024": 71145, "FY2023": 65976, "FY2022": 73340, "FY2021": 158856, "FY2020": 138529, "FY2019": 15691, "FY2018": 40052, "FY2017": 195}),
        ("Closing equity", {"FY2025": 623217, "FY2024": 497291, "FY2023": 404415, "FY2022": 299607, "FY2021": 252255, "FY2020": 127622, "FY2019": 19638, "FY2018": 21814, "FY2017": -3806}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 363343, "FY2024": 1736072, "FY2023": -52437, "FY2022": 1149272, "FY2021": -175837, "FY2020": -56978, "FY2019": -25594, "FY2018": -20803, "FY2017": 500}),
        ("Net cash from/(used in) investing activities", {"FY2025": -817416, "FY2024": -389003, "FY2023": -92313, "FY2022": -4558, "FY2021": -2555, "FY2020": -2872, "FY2019": -1460, "FY2018": -16149, "FY2017": -305}),
        ("Net cash from/(used in) financing activities", {"FY2025": -27173, "FY2024": 66682, "FY2023": 118865, "FY2022": 49405, "FY2021": 346694, "FY2020": 126482, "FY2019": 17369, "FY2018": 39160, "FY2017": 0}),
        ("Cash and cash equivalents at end of year", {"FY2025": 2338497, "FY2024": 2819743, "FY2023": 1405992, "FY2022": 1431877, "FY2021": 237758, "FY2020": 69368, "FY2019": 2736, "FY2018": 2402, "FY2017": 194}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "14.54%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%", "FY2018": "19%"}),
        ("Tier 1 Ratio", {"FY2025": "16.87%", "FY2024": "16.76%", "FY2023": "16.50%", "FY2022": "17.44%", "FY2021": "22.92%", "FY2018": "19%"}),
        ("Total Capital Ratio", {"FY2025": "19.10%", "FY2024": "19.57%", "FY2023": "19.90%", "FY2022": "17.44%", "FY2021": "22.92%", "FY2018": "19%"}),
        ("Leverage Ratio", {"FY2025": "11.36%", "FY2024": "12.99%", "FY2023": "13.48%", "FY2022": "14.34%"}),
        ("LCR", {"FY2025": "484%", "FY2024": "546%", "FY2023": "730%", "FY2022": "1,033%"}),
        ("NSFR", {"FY2025": "225%", "FY2024": "227%", "FY2023": "207%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. All figures are Zopa Bank Limited's own entity-level basis, "
         "not the wider Zopa Group. FY2017 is the pre-banking-licence entity (Zopa Financial Services Limited); "
         "FY2018-FY2020 predate full, unrestricted authorisation - see HISTORICAL FLOOR NOTE on the Balance Sheet "
         "sheet.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ZOPA FINANCIALS.xlsx")
