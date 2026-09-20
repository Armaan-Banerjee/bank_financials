import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018",
         "FY2017", "FY2016", "FY2015", "FY2014",
         "FY2013", "FY2012", "FY2011", "FY2010", "FY2009"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024",
             "FY2020": "FY2019", "FY2019": "FY2018", "FY2018": "FY2017", "FY2017": "FY2016",
             "FY2016": "FY2015", "FY2015": "FY2014", "FY2014": "FY2013"}

# HD-073 (2026-09-06/07) held Pillar 3 (all 11 metric sheets), RWA Breakdown and Asset Quality to
# FY2014-FY2025, because no Pillar 3 disclosure older than FY2014 had been located at that point.
#
# 2026-09-15 (historical Pillar 3 recovery): that exclusion is lifted to the full YEARS range.
# A genuine Zenith Bank (UK) Limited Pillar 3 edition for FY2011 was recovered from the Wayback
# Machine and read cover to cover (see HIST_P3_NOTE). It is a Basel II / BIPRU document, so its
# figures go on their own explicitly-labelled rows, never onto the CRR series. The remaining
# FY2009/FY2010/FY2012/FY2013 columns stay empty of capital data because no Pillar 3 edition
# exists for them in any archive, but the structurally-inapplicable metrics (CET1, leverage, LCR,
# NSFR, MREL) are now marked "Not applicable" across all five years rather than left blank.
# A FY2008 edition was also recovered but yielded NO cell - see HIST_P3_NOTE for why.
PILLAR3_YEARS = list(YEARS)

# HD-073: Zenith Bank (UK) Limited's own Annual Reports for FY2009-FY2013 (recovered from Companies
# House, company 05713749) are reported natively in GBP - the Bank's redenomination to USD (see
# HD048_NOTE below) had not yet happened. These 5 years therefore need NO FX conversion at all; they
# are shown directly as £'000. stock2()/flow2()/opening_cash2() below are FX-aware wrappers around
# stock()/flow()/opening_cash() that pass native-£ years straight through (divide by 1000 only) and
# apply the existing USD FX rates unchanged for every other year - so FY2014 onward behave exactly
# as before this ticket.
NATIVE_GBP_YEARS = {"FY2013", "FY2012", "FY2011", "FY2010", "FY2009"}

# ---------------------------------------------------------------
# FX conversion (Zenith Bank UK reports in USD; converting to £ per this
# project's established FX methodology - see build_smbc.py precedent).
# FY2020-FY2025 rates are Bank of England GBP/USD spot/average via
# poundsterlinglive.com's published archive, £1 = $X. FY2014-FY2019 rates
# (added for the HD-048 FY2014 extension) are pulled directly from the Bank
# of England's own Interactive Statistical Database, series XUDLGBD (spot
# exchange rate, US dollar into Sterling), inverted to £1 = $X and rounded to
# 4dp - same underlying BoE series poundsterlinglive republishes, queried
# directly since the third-party archive wasn't practical to browse
# interactively for this many historical dates. Year-end spot = last trading
# day of that calendar year; year average = mean of all daily observations
# in that calendar year (253-254 trading days each year, matching a full
# year of BoE publication days).
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2013": 1.6529,  # 31 Dec 2013 - only used for FY2014's opening cash balance
    "FY2014": 1.5608,  # 31 Dec 2014
    "FY2015": 1.4819,  # 31 Dec 2015
    "FY2016": 1.2303,  # 30 Dec 2016 (31st was a Saturday)
    "FY2017": 1.3510,  # 29 Dec 2017 (31st was a Sunday)
    "FY2018": 1.2770,  # 31 Dec 2018
    "FY2019": 1.3210,  # 31 Dec 2019
    "FY2020": 1.3661,  # 31 Dec 2020 - only used for FY2021's opening cash balance
    "FY2021": 1.3521,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
    "FY2025": 1.3448,  # 31 Dec 2025
}
FX_AVG = {
    "FY2014": 1.6465,
    "FY2015": 1.5281,
    "FY2016": 1.3488,
    "FY2017": 1.2878,
    "FY2018": 1.3335,
    "FY2019": 1.2757,
    "FY2020": 1.2825,
    "FY2021": 1.3752,
    "FY2022": 1.2362,
    "FY2023": 1.2439,
    "FY2024": 1.2782,
    "FY2025": 1.3193,
}


def flow(usd):
    """Flow (cash flow statement line item) figures, £'000, at that year's average rate."""
    return {y: round(v / FX_AVG[y] / 1000, 1) for y, v in usd.items()}


def stock(usd):
    """Point-in-time (balance/capital) figures, £'000, at that year's period-end spot rate.

    Input is RAW USD (whole dollars) - the Annual Report statements are transcribed at full
    precision, e.g. Share Capital US$136,701,620 - so reaching £'000 needs BOTH the FX divide
    and a divide by 1,000. Use stock_k() instead for any figure already denominated in
    thousands. See the comment on stock_k() for why the two must stay separate.
    """
    return {y: (v if not isinstance(v, (int, float)) or isinstance(v, bool)
                else round(v / FX_SPOT[y] / 1000, 1)) for y, v in usd.items()}


def stock_k(usd_thousands):
    """Point-in-time figures ALREADY IN US$'000, converted to £'000 at that year's spot rate.

    *** DO NOT MERGE THIS BACK INTO stock(). THE TWO VARIANTS EXIST FOR A REAL REASON. ***
    This script transcribes from two source families that publish at two different scales,
    and a single helper cannot serve both:

      - The Annual Report statements (Balance Sheet, P&L, Statement of Changes in Equity,
        Cash Flow Statement, Asset Quality) print WHOLE DOLLARS and are transcribed that way
        -> stock() / flow(), which divide by 1,000 on top of the FX rate.
      - The Pillar 3 disclosures (all 11 metric sheets and the RWA Breakdown sheet) print
        US$'000 and are transcribed that way -> stock_k(), FX only, NO divide by 1,000.

    The FY2024 Pillar 3's UK KM1 and UK OV1 tables suffix every figure with a literal " k"
    ("Common Equity Tier 1 (CET1) capital 378,325 k"), and its own footnote writes the unit
    out in prose ("the average ASF US$1,136,904k / the average RSF US$768,308k = 147.98%").
    The FY2015 edition heads its capital tables "US$000's". The decisive cross-check: the
    Bank's share capital is "136,701,620 ordinary shares of US$1", which the Annual Report
    carries as 136701620 and the Pillar 3 prints as "136,702 k" - the same money, two scales.

    Applying stock()'s extra /1,000 to the Pillar 3 dicts is exactly the defect fixed on
    2026-09-15: it made every Pillar 3 and RWA Breakdown cell 1000x too small for its "£'000"
    label (effectively £m), so CET1 read 302.3 against a Balance Sheet Total equity of
    305,356.2. Ratios hid it, being scale-invariant. See P3_SCALE_FIX_NOTE.

    There is deliberately no flow_k(): every Pillar 3 figure on these sheets is a
    point-in-time stock, so no averaging-rate variant is needed. If a thousands-denominated
    FLOW figure is ever added, add flow_k() alongside rather than reusing flow().

    Native-GBP years (NATIVE_GBP_YEARS, FY2009-FY2013) never reach this helper: the only
    pre-redenomination Pillar 3 figures are FY2011's, which are native GBP'000 and are
    written straight onto their own rows (FY2011_TIER1_ACCOUNTS / FY2011_REG_AVAILABLE)
    with no conversion of any kind. FX_SPOT has no key before FY2013, so an accidental
    native-GBP year passed in here raises KeyError rather than converting silently.
    """
    return {y: round(v / FX_SPOT[y], 1) for y, v in usd_thousands.items()}


def opening_cash(usd):
    """Opening cash balance, £'000 - uses the PRIOR year's period-end spot rate (it's the
    same balance as that prior year's closing figure, so must convert identically)."""
    return {y: round(v / FX_SPOT[PREV_YEAR[y]] / 1000, 1) for y, v in usd.items()}


def pct(usd_strings):
    """Ratios are NOT converted - dimensionless and currency-invariant."""
    return usd_strings


# ---------------------------------------------------------------
# PRINTED DASHES.  The FY2025 Annual Report prints a literal "-" in several
# statement cells (Deferred tax assets and Current tax liabilities on the
# balance sheet; "Net loss on derecognition of financial instruments" in the
# P&L; "Loss on derecognition of assets" in the cash flow statement).  A dash
# is the Bank's own glyph and is NOT the same statement as a zero or as a
# blank, so it is carried through to the workbook verbatim rather than being
# converted to 0 (which would assert a measured nil) or dropped (which would
# assert no disclosure).  Every converting helper below therefore passes any
# non-numeric value through untouched - there is nothing to apply an exchange
# rate to.  Do not "simplify" this by coercing to a number.
# ---------------------------------------------------------------
def _passthrough(v):
    return not isinstance(v, (int, float)) or isinstance(v, bool)


def stock2(vals):
    """Like stock(), but FY2009-FY2013 (native £, see NATIVE_GBP_YEARS) pass through as £'000 directly."""
    return {y: (v if _passthrough(v) else
                (round(v / 1000, 1) if y in NATIVE_GBP_YEARS else round(v / FX_SPOT[y] / 1000, 1)))
            for y, v in vals.items()}


def flow2(vals):
    """Like flow(), but FY2009-FY2013 (native £, see NATIVE_GBP_YEARS) pass through as £'000 directly."""
    return {y: (v if _passthrough(v) else
                (round(v / 1000, 1) if y in NATIVE_GBP_YEARS else round(v / FX_AVG[y] / 1000, 1)))
            for y, v in vals.items()}


def opening_cash2(vals):
    """Like opening_cash(), but FY2012/FY2013 (native £) pass through as £'000 directly."""
    return {y: (round(v / 1000, 1) if y in NATIVE_GBP_YEARS else round(v / FX_SPOT[PREV_YEAR[y]] / 1000, 1))
            for y, v in vals.items()}

# ---------------------------------------------------------------
# Source documents
# ---------------------------------------------------------------
BASE = "https://www.zenith-bank.co.uk/media"
# FY2025 Annual Report, located 2026-09-18. IT IS NOT ON THE BANK'S OWN SITE:
# zenith-bank.co.uk's "Statutory Accounts & Tax Strategy" page (the Bank's own
# enumerating index, read live that day) lists annual reports only to 2024,
# while its separate /pillar-3/ page already carries the FY2025 Pillar 3. The
# FY2025 statutory accounts exist only as the Companies House filing below -
# "Full accounts made up to 31 December 2025", filed 18 May 2026, 122 pages,
# approved by the Board on 13 March 2026. Like the FY2009-FY2013 filings it is
# a go-tiff2pdf SCAN with no text layer at all (pdftotext yields 122 bytes for
# the whole document), so every figure taken from it was read VISUALLY from
# pages rendered at 300 dpi, never OCR'd - OCR was used only to index which
# page held which statement.
AR2025_URL = ("https://find-and-update.company-information.service.gov.uk/company/05713749/"
              "filing-history/MzUyMjI1NjUwM2FkaXF6a2N4/document?format=pdf&download=0")
AR2024_URL = f"{BASE}/2273/2024-annual-report-and-financial-statements.pdf"
AR2023_URL = f"{BASE}/2253/2023-annual-report-and-financial-statements.pdf"
AR2022_URL = f"{BASE}/2237/2022-annual-report-and-financial-statements.pdf"
AR2021_URL = f"{BASE}/2205/2021-annual-report-and-financial-statements.pdf"
AR2020_URL = f"{BASE}/2199/zenith-bank-uk-limited-annual-report-2020.pdf"
AR2019_URL = f"{BASE}/2169/258558-zenith-web.pdf"
AR2018_URL = f"{BASE}/2151/2018-annual-report.pdf"
AR2017_URL = f"{BASE}/2142/2017-annual-report-and-financial-statements.pdf"
AR2016_URL = f"{BASE}/1009/statutory_accounts_year_ended_31st_december_2016.pdf"
AR2015_URL = f"{BASE}/1011/zenith_bank_-uk-_ltd_-_annual_report_and_financial_statements_2015.pdf"
AR2014_URL = f"{BASE}/1010/zenith_bank_-uk-_ltd_-_annual_report_and_accounts_2014.pdf"

P3_2025_URL = f"{BASE}/2290/pillar-3-zbuk-31dec25.pdf"
P3_2024_URL = f"{BASE}/2274/31dec24-pillar-3-zbuk.pdf"
P3_2023_URL = f"{BASE}/2260/pillar-3-31dec23-final.pdf"
P3_2022_URL = f"{BASE}/2238/zbuk-31dec22-pillar-3-disclosures.pdf"
P3_2021_URL = f"{BASE}/2228/31dec21-pillar-3.pdf"
# FY2014/FY2015 Pillar 3 disclosures: no longer live on zenith-bank.co.uk (the current
# Pillar 3 page only lists FY2021 onward) but recovered from the Internet Archive
# Wayback Machine, where the original /uploads/ URLs (the Bank's pre-2018 site
# structure) were captured intact.
P3_2014_URL = "http://web.archive.org/web/20160826052010id_/http://www.zenith-bank.co.uk/uploads/ZBL_Pillar_3_Disclosure_Document_2014.pdf"
P3_2015_URL = "http://web.archive.org/web/20161128044735id_/http://www.zenith-bank.co.uk/uploads/ZBL_Pillar_3_Disclosure_Document_2015.pdf"
# 2026-09-15 historical recovery: two further editions, from the Bank's even older
# /documents/ and /docs/ site structures. Both cite the full timestamped capture,
# since the filenames alone no longer resolve anywhere.
P3_2011_URL = "https://web.archive.org/web/20130616222348id_/http://www.zenith-bank.co.uk:80/docs/ZBL_Pillar_3_Disclosure_Document_2011.pdf"
P3_2008_URL = "https://web.archive.org/web/20090424153904id_/http://www.zenith-bank.co.uk:80/documents/ZBL_Pillar_3_Disclosure_Document.pdf"

# HD-073 (2026-09-06/07): FY2009-FY2013 Annual Reports, recovered from Companies House (company
# 05713749) since these pre-date the Bank's own website archive. All native-text was unavailable
# (scanned filings) - transcribed via 150dpi page-image rendering, no OCR.
CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/05713749/filing-history/"
AR2013_URL = CH_BASE + "MzEwNDk3MzAyNmFkaXF6a2N4/document?format=pdf&download=0"
AR2012_URL = CH_BASE + "MzA4MDQyODAzOGFkaXF6a2N4/document?format=pdf&download=0"
AR2011_URL = CH_BASE + "MzA1NjQzNDY0OWFkaXF6a2N4/document?format=pdf&download=0"
AR2010_URL = CH_BASE + "MzAzNjAzNzkzN2FkaXF6a2N4/document?format=pdf&download=0"
AR2009_URL = CH_BASE + "MzAxMzk0ODA3MmFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: Zenith Bank (UK) Limited (FRN 451720) is a UK subsidiary of Zenith Bank Plc (Nigeria). Unlike "
    "several other foreign-subsidiary banks in this workbook series (ICICI Bank UK, Philippine National Bank "
    "Europe, Citibank UK, State Bank of India UK), it prepares full financial statements under UK-adopted "
    "International Accounting Standards (not FRS 101/102 reduced disclosure), including a genuine Statement of "
    "Cash Flows every year - no cash-flow exemption applies. The Bank's own capital structure is CET1-only (no "
    "AT1 or Tier 2 instruments), so CET1 capital = Tier 1 capital = Total capital in every year shown."
)

HD048_NOTE = (
    "HD-048 EXTENSION NOTE (2026-09-06): this workbook was extended from its original FY2021-FY2025 window back "
    "to FY2014 under wayfinder ticket HD-048, capped at FY2014 by explicit project-wide user decision even though "
    "Zenith Bank (UK) Limited's own disclosure archive genuinely extends to FY2009 (Pillar 3 pre-CRD IV/Basel III "
    "isn't considered comparable to later years, and this project caps historical depth at FY2014 across all "
    "extended banks). FY2014-FY2020 Annual Report and Financial Statements were re-sourced directly from the "
    "Bank's own live website (zenith-bank.co.uk/why-us/statutory-accounts-tax-strategy/), each verified by opening "
    "the actual PDF and checking its cover/contents page states the claimed year - this caught the site's own "
    "'2015' link actually serving a byte-identical copy of the FY2018 report (same file, two URLs); the genuine "
    "FY2015 Annual Report was recovered from Internet Archive Wayback Machine crawl data instead (media/1011). "
    "FY2014-FY2015 Pillar 3 disclosures were similarly recovered from Wayback Machine captures of the Bank's "
    "pre-2018 site (see Pillar 3 sources note). No Pillar 3 disclosure document for FY2016-FY2020 could be found "
    "on the live site or in the Wayback Machine despite a thorough search (CDX API queries against every "
    "plausible URL pattern, including two specific leads from an earlier interrupted session that both proved to "
    "be unarchived 404s on further verification) - the Bank's Pillar 3 page itself was archived several times "
    "across those years and confirms the underlying PDF links existed at the time, but the PDF binaries "
    "themselves were never crawled by the Wayback Machine. Annual Report-sourced sheets (Balance Sheet, P&L, "
    "Statement of Changes in Equity, Cash Flow Statement, Asset Quality) are fully populated for all of "
    "FY2014-FY2020.\n"
    "SUPERSEDED IN PART, 2026-09-18 - DO NOT READ THE PARAGRAPH ABOVE AS 'NO CAPITAL DATA EXISTS FOR "
    "FY2016-FY2019'. It said, in its original form, that all 11 Pillar 3 metric sheets and the RWA Breakdown "
    "sheet were 'therefore genuinely blank for FY2016-FY2020'. The word 'therefore' was the error: the absence "
    "of a Pillar 3 DOCUMENT was treated as the absence of the DATA, and nobody opened the Annual Reports "
    "looking for capital. They carry a 'Capital Management' note with a Capital Resources table every year. "
    "FY2016-FY2019 capital, and FY2017/FY2018 CET1 ratios, are now populated from that source (and FY2012/"
    "FY2013 from the same note in the Companies House filings). What remains genuinely absent for FY2016-FY2019 "
    "is RWA, the RWA breakdown, the leverage ratio and the LCR. See the ANNUAL-REPORT CAPITAL RECOVERY note on "
    "the capital sheets."
)

FX_NOTE = (
    "FX CONVERSION NOTE: Zenith Bank (UK) Limited reports in US Dollars. This workbook converts every $ amount to "
    "£ for consistency with the rest of this series, following the same methodology established for SMBC Bank "
    "International plc: point-in-time/balance figures (capital, RWA, leverage exposure, HQLA, cash balances) use "
    "the Bank of England GBP/USD SPOT rate as at that fiscal year-end (31 December); flow figures (every cash "
    "flow statement line item) use the AVERAGE of Bank of England rates over that calendar year. FY2020-FY2025 "
    "rates are via poundsterlinglive.com's published Bank of England archive; FY2014-FY2019 rates (added under "
    "HD-048) were pulled directly from the Bank of England's own Interactive Statistical Database (series "
    "XUDLGBD, spot exchange rate US dollar into Sterling), inverted and rounded to 4dp - the same underlying BoE "
    "series poundsterlinglive republishes. Rates used (£1 = $X): 31 Dec 2013 spot 1.6529 (FY2014 opening cash "
    "only); FY2014 spot 1.5608 / average 1.6465; FY2015 spot 1.4819 / average 1.5281; FY2016 spot 1.2303 / "
    "average 1.3488; FY2017 spot 1.3510 / average 1.2878; FY2018 spot 1.2770 / average 1.3335; FY2019 spot "
    "1.3210 / average 1.2757; FY2020 spot 1.3661 / average 1.2825 (FY2020 spot pre-dates HD-048 and is kept "
    "unchanged from the original build for continuity - a fresh BoE query for the same date gives 1.3648, a "
    "~0.1% difference attributable to archive rounding, immaterial at 1dp in £'000 terms); FY2021 spot 1.3521 / "
    "average 1.3752; FY2022 spot 1.2097 / average 1.2362; FY2023 spot 1.2732 / average 1.2439; FY2024 spot "
    "1.2515 / average 1.2782; FY2025 spot 1.3448 / average 1.3193. All % ratios (CET1/Tier 1/Total "
    "Capital/Leverage/LCR/NSFR ratios) are shown EXACTLY as reported in USD and were NOT converted - a ratio is "
    "dimensionless and currency-invariant. Because stocks and flows are converted at different rates, the cash "
    "flow statement includes an explicit 'Effect of GBP/USD translation' reconciling line so opening + all flows "
    "+ this line = closing exactly in £ terms - this line is purely an artefact of £ translation and has no "
    "bearing on the Bank's underlying USD results. This conversion was not explicitly requested for this bank "
    "(unlike SMBC) - applied for consistency with the rest of the series; flag if £'000 rather than the Bank's "
    "native US$'000 presentation is not what's wanted here."
)

HD073_NOTE = (
    "HD-073 EXTENSION NOTE (2026-09-06/07): this workbook was extended from its FY2014 floor back to "
    "FY2009 under wayfinder ticket HD-073, using the Bank's own statutory accounts recovered from "
    "Companies House (company 05713749) - the Bank's own website archive does not go back this far. "
    "CURRENCY: FY2009-FY2013 are reported by the Bank natively in GBP (its redenomination to USD, "
    "see the FX conversion note above, happened during 2013/2014) - these 5 years require NO FX "
    "conversion at all and are shown as £'000 directly (see stock2()/flow2()/opening_cash2() in this "
    "script). STATEMENT AVAILABILITY: FY2012 and FY2013 have full IFRS-style statements (Statement of "
    "Comprehensive Income, Statement of Financial Position, Statement of Changes in Equity, Statement "
    "of Cash Flows), all populated here. FY2009-FY2011 pre-date the Bank's IFRS adoption entirely - "
    "each year's own report contains only a 'Profit and loss account' and 'Balance sheet' under old UK "
    "GAAP, and each explicitly states 'There are no recognised gains or losses for the year other than "
    "as stated above. Accordingly no Statement of Total Recognised Gains and Losses has been prepared' "
    "and contains no Statement of Cash Flows at all - a genuine, disclosed absence (not a small-company "
    "cash-flow exemption assumption), so the Statement of Changes in Equity and Cash Flow Statement "
    "sheets are genuinely blank for FY2009-FY2011. PRESENTATION BRIDGE (Balance Sheet, FY2009-FY2011): "
    "these years predate the Trading/Investment securities split (a single 'Securities' line is shown "
    "here as 'Securities measured at amortised cost') and the Deposits by banks/corporates split shown "
    "from FY2012 ('Deposits by corporates' maps to 'Deposits from customers', consistent with later "
    "years' convention); 'Other assets' combines the Bank's own separate 'Other assets' and "
    "'Prepayments' lines (no dedicated Prepayments row exists in this sheet's modern label set); "
    "'Other liabilities' holds the Bank's own 'Accrued expenses' line. FY2009's own report does not "
    "separately disclose a 'Cash' line at all (folded into 'Loans and advances to banks', £275,505,662) "
    "- FY2010's own report later reclassifies out a £35,421 'Cash' balance for its FY2009 comparative; "
    "FY2009's own as-originally-reported combined figure is used here, per this project's convention of "
    "preferring each year's own report. PRESENTATION BRIDGE (P&L, FY2009-FY2010): neither year "
    "separately discloses Personnel expenses/Depreciation and amortisation - a single 'Administrative "
    "expenses' line is shown here as 'Other expenses' (Personnel expenses/Depreciation and "
    "amortisation blank, not zero, for these two years only). RESTATEMENT NOTE: FY2011's own report "
    "(profit before tax £5,104,963, profit for the year £3,622,457) differs from the FY2012 Annual "
    "Report's own restated FY2011 IFRS comparative (profit before tax £4,973,686, profit for the year "
    "£3,491,180) - a reclassification between interest/fee/expense lines under the Bank's FY2012 IFRS "
    "conversion, not a change to the audited FY2011 result. FY2011's own report figures are used "
    "throughout, consistent with this project's convention of preferring each year's own report over a "
    "later restated comparative. Similarly, FY2009's own report labels ('Interest receivable', 'Fees & "
    "commissions receivable', 'Exchange profits') differ from FY2010's own report's FY2009 comparative "
    "labels ('Interest earned', 'Fees & commission earned', 'Trading profits (Net)') with a like-for-"
    "like £518,750 shift between the interest and fee/trading lines - Operating income and Profit for "
    "the year are identical either way; FY2009's own report figures are used. BRIDGE GAP (FY2013/"
    "FY2014 boundary): FY2013's own report shows closing Total equity of £74,509,003 and closing cash "
    "of £119,758,144; the Bank's own FY2014 Annual Report separately expresses its 1 January 2014 "
    "opening position in USD (used, unchanged, by the pre-existing FY2014 opening rows in this "
    "workbook) which back-converts via the 31 Dec 2013 spot rate to approximately £74,543,010 total "
    "equity and £119,819,001 opening cash - a small (~0.05%) gap attributable to the Bank's own "
    "USD-conversion/rounding at the point of redenomination, not reconciled further; both figures are "
    "shown exactly as each source discloses them."
)

RESTATEMENT_NOTE = (
    "RESTATEMENT NOTE: FY2023's own Annual Report cash flow figures (used for FY2023's column here) differ "
    "slightly from the 'restated' FY2023 comparative shown in the FY2024 Annual Report (e.g. operating activities "
    "$(344,220,013) as originally reported vs $(346,336,139) restated) - both report the same $276,069,567 "
    "closing balance, so the restatement is a reclassification between line items, not a change to overall cash "
    "movement. FY2023's own as-originally-reported figures are used throughout, consistent with this project's "
    "convention of preferring each year's own report over a later restated comparative."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Zenith Bank (UK) Limited's own Statement of Cash Flows (converted from USD to £, "
    "see FX conversion note below):\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.44-45 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.36 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.34 (Statement of Cash Flows) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.32 (Statement of Cash Flows) - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020, p.34 (Statement of Cash Flows) - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019, p.23 (Statement of Cash Flows) - {AR2019_URL}\n"
    f"FY2018: Annual Report and Financial Statements 2018, p.21 (Statement of Cash Flows) - {AR2018_URL}\n"
    f"FY2017: Annual Report and Financial Statements 2017, p.20 (Statement of Cash Flows) - {AR2017_URL}\n"
    f"FY2016: Annual Report and Accounts 2016, p.12 (Statement of Cash Flows) - {AR2016_URL}\n"
    f"FY2015: Annual Report and Financial Statements 2015, p.13 (Statement of cash flows) - {AR2015_URL}\n"
    f"FY2014: Annual Report and Financial Statements 2014, p.13 (Statement of cash flows) - {AR2014_URL}\n"
    f"FY2025: Annual Report and Financial Statements 2025, pp.42-43 printed (PDF pp.44-45), Statement of Cash "
    f"Flows - {AR2025_URL}\n"
    "FY2025 WAS BLANK UNTIL 18 SEPTEMBER 2026 and the reason it filled matters for the next reader: no FY2025 "
    "Annual Report was ever published on zenith-bank.co.uk (its own 'Statutory Accounts & Tax Strategy' page "
    "still lists annual reports only to 2024, though its separate Pillar 3 page carries the FY2025 edition), so "
    "checking the Bank's own site - the route every other year here uses - would have kept returning nothing. "
    "The FY2025 statutory accounts exist only as the Companies House filing cited above ('Full accounts made "
    "up to 31 December 2025', filed 18 May 2026, 122 pages). That filing is a go-tiff2pdf scan with no text "
    "layer whatsoever, so every FY2025 figure in this workbook was read VISUALLY from pages rendered at 300 "
    "dpi; OCR was used only to index which page held which statement, never to read a number.\n"
    "FY2025 PRESENTATION CHANGES, each kept as the Bank printed it rather than forced onto the FY2024 shape: "
    "(a) financing activities now split the lease outflow into 'Repayment of Lease liability' (926,443) and "
    "'Interest payment on Lease liability' (340,871), where FY2024's own report printed a single 672,177 - "
    "this workbook keeps FY2024 as its own edition printed it and gives FY2025 its own two rows; (b) 'Loss on "
    "derecognition of assets' prints a literal dash for FY2025, carried through as '-' and NOT as 0.\n"
    "Note: FY2021's own report presents operating cash flow more simply than later years - net interest is not "
    "separately reversed out of profit and re-added on a cash basis (no 'Interest income'/'Interest expense' "
    "adjustment lines, no 'Interest income received'/'Interest expense paid' cash lines); FY2022 onward introduced "
    "this more granular presentation. Blank cells for FY2021 on those rows reflect this, not missing data. "
    "FY2014-FY2020's own reports present operating cash flow even more simply than FY2021 - none of them "
    "separately reverse out net interest on a cash basis at all (that level of granularity was only introduced "
    "FY2022 onward); blank cells for FY2014-FY2020 on those specific reconciliation rows reflect this, not "
    "missing data. FY2014-FY2017 (pre-IFRS 9) show a single 'Impairment provision charge' line rather than the "
    "IFRS 9-era split used from FY2018; FY2014 shows none at all (the Bank recognised zero impairment charge that "
    "year, per its own report). FY2019-FY2020 add 'Interest expense (transition to IFRS 16)'/lease-related lines "
    "not present in earlier years, reflecting the Bank's genuine IFRS 16 adoption (1 January 2019) - blank, not "
    "zero, for years before that transition.\n"
    "Activity-total rows may be off by up to £0.2k from summing the visible line items above them, since each £ "
    "line is independently rounded to 1 decimal place before summing; the full statement ties exactly end-to-end "
    "via the net change, opening balance, exchange-rate-effect and translation-effect lines (verified to the "
    "penny in £'000 terms for every populated year).\n"
    f"FY2013: Financial Statements for the year ended 31 December 2013, p.12 (Consolidated statement of cash "
    f"flows) - {AR2013_URL}\n"
    f"FY2012: Financial Statements as at 31 December 2012, p.11 (Statement of cash flows, FY2013's own FY2012 "
    f"comparative column) - {AR2013_URL} (cross-checked against FY2012's own Annual Report, same document as "
    f"the FY2012 sources row above)\n"
    "FY2009-FY2011 cash flow is blank: these years' own Annual Reports contain no Statement of Cash Flows at "
    "all (see HD-073 extension note below) - a genuine, disclosed absence.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + RESTATEMENT_NOTE + "\n\n" + HD048_NOTE + "\n\n" + HD073_NOTE
)


P3_SCALE_FIX_NOTE = (
    "*** UNIT-SCALE DEFECT FOUND AND FIXED 2026-09-15 - READ BEFORE COMPARING AGAINST ANY EARLIER COPY ***\n"
    "For a period earlier on 2026-09-15, every absolute-amount cell on the 11 Pillar 3 metric sheets and the RWA "
    "Breakdown sheet of this workbook was 1000x smaller than its \"£'000\" unit label claimed - the figures were "
    "effectively GBP MILLIONS. The symptom: FY2024 CET1 capital read 302.3 while the Balance Sheet sheet showed "
    "FY2024 Total equity as 305,356.2 under the same \"£'000, conv. from USD\" header - two figures that should be "
    "within a few percent of each other, three orders of magnitude apart.\n"
    "CAUSE (a units-handling bug in this build script, NOT a transcription error - no source figure was ever "
    "wrong): the Annual Report statements print WHOLE DOLLARS and are transcribed that way, so stock()/flow() "
    "divide by 1,000 on top of the FX rate to reach £'000. The Pillar 3 disclosures print US$'000 and are "
    "transcribed that way, but were being passed through that same stock(), applying the divide-by-1,000 twice "
    "over to figures that were already in thousands. FIX: a separate stock_k() helper (FX conversion only, no "
    "divide by 1,000) now serves every Pillar 3 and RWA Breakdown call site; the transcribed source figures were "
    "not touched.\n"
    "THE SOURCE SCALE IS EXPLICIT IN THE DOCUMENTS, not inferred. The FY2024 edition's UK KM1 and UK OV1 tables "
    "suffix every figure with a literal \" k\" (\"Common Equity Tier 1 (CET1) capital 378,325 k\"; \"Total "
    "risk-weighted exposure amount 1,475,750 k\") and its own footnote writes it out in prose: \"the average ASF "
    "US$1,136,904k / the average RSF US$768,308k = 147.98%\". The FY2015 edition heads its capital tables "
    "\"US$000's\". The decisive cross-check: the Bank's share capital is \"136,701,620 ordinary shares of US$1\", "
    "which the Annual Report carries as 136,701,620 and the Pillar 3 prints as \"136,702 k\" - the same money at "
    "two scales.\n"
    "WHAT DID NOT CHANGE, AND WHY THE DEFECT SURVIVED SO LONG: every ratio on these sheets (CET1/Tier 1/Total "
    "Capital/Leverage/LCR/NSFR) is dimensionless, so numerator and denominator were scaled identically and every "
    "printed ratio reproduced both before and after the fix - there was no ratio symptom to catch. The statement "
    "sheets (Balance Sheet, Profit & Loss, Statement of Changes in Equity, Cash Flow Statement, Asset Quality) "
    "were never affected: they are sourced from the Annual Reports in whole dollars and stock()/flow() were "
    "always correct for them. The Overview sheet carries no Pillar 3 absolute amount at all (only statement "
    "totals and ratios), so it needed no rescaling either.\n"
    "FY2011 FOOTNOTE: the two Basel II capital figures on the Tier 1 Capital and Total Capital sheets were "
    "entered as 43.6 and 40.0 during the window in which the defect stood, deliberately matching the wrong scale "
    "so as not to create a mixed-unit defect inside a single sheet. They now read 43,631 and 40,002 - the figures "
    "the FY2011 edition actually prints, in GBP'000."
)

HIST_P3_NOTE = (
    "HISTORICAL PILLAR 3 RECOVERY (2026-09-15) - FY2008 and FY2011 editions recovered from the Wayback Machine\n"
    f"FY2011: Zenith Bank (UK) Limited, \"Pillar 3 Disclosures for the year ended 31 December 2011\" (17pp, "
    f"'Reviewed May 2012'), section 4.2 Capital Resources and section 4.3 Capital Allocation, p.7-8 - {P3_2011_URL}\n"
    f"FY2008: Zenith Bank (UK) Limited, \"Pillar 3 Disclosures for the year ending 31 December 2008\" (9pp, "
    f"'Reviewed December 2008'), section 1 Capital Adequacy Overview & Resources, p.6 - {P3_2008_URL}\n\n"
    "*** FY2008: RECOVERED, READ, AND DELIBERATELY NOT USED FOR ANY CELL ***\n"
    "This document's cover is internally contradictory - it says 'FOR THE YEAR ENDING 31 DECEMBER 2008' but also "
    "'Reviewed December 2008' and, on its last page, 'This Disclosure will be published in December 2008'. The "
    "contradiction was resolved from the FIGURES, not the cover, and the figures are decisive. The document's "
    "ONLY quantitative table is introduced verbatim as: \"Tier 1 capital based on our 31 December 2007 audited "
    "accounts as adjusted for a GBP 15 million capital injection in May 2008 is as follows: Share capital 35,001 "
    "/ Profit and loss reserve (1,473) / Total tier 1 capital 33,528\" (GBP'000). Two further statements confirm "
    "it: \"The disclosures should be read in conjunction with the ZBL Annual Report and Financial Statements for "
    "the corresponding financial year WHICH WILL BE PUBLISHED IN MARCH 2009\", and \"The disclosures herein are "
    "based on the ICAAP last approved in September 2008\". So this is an in-year disclosure written before the "
    "2008 year-end and before the 2008 accounts existed; 'for the year ending' means the year then in progress, "
    "not an as-at date. THE FIGURE IS THEREFORE NEITHER AN FY2008 NOR AN FY2007 POSITION - it is 31 December 2007 "
    "audited reserves combined with share capital that already includes a May 2008 injection. There is no year "
    "column in this workbook it can honestly occupy, and mapping it to FY2008 (or to FY2007) would misdate it. "
    "No cell was written from it. It is recorded here in full so the document is part of this workbook's record "
    "and is not re-chased as an open lead. The edition contains no RWA, no capital requirement and no ratio of "
    "any kind, so nothing further was available from it in any case.\n\n"
    "FY2011 - TRANSCRIBED. Cover date is unambiguous ('for the year ended 31 December 2011', reviewed May 2012) "
    "and the capital table is explicitly headed 'Tier 1 capital as at 31 December 2011 audited accounts'. Native "
    "GBP: this pre-dates the Bank's redenomination to USD, so NO FX conversion is applied to these figures (see "
    "NATIVE_GBP_YEARS on the statement sheets for the same treatment). Figures, GBP'000:\n"
    "  Capital table - Share capital at 31 December 2011 35,001; Profit and loss reserve 8,630; TOTAL TIER 1 "
    "CAPITAL 43,631. The Bank states 'The Bank's entire capital base is Tier 1 capital which consists of fully "
    "issued ordinary shares satisfying all the criteria for a Tier 1 instrument (as outlined in GENPRU 2.2.83 R) "
    "and audited reserves' - so there is no AT1 and no Tier 2, by the Bank's own statement.\n"
    "  Pillar 1 capital requirements - Credit Risk 18,156; Market Risk 27; Operational Risk 1,503; TOTAL 19,686. "
    "Regulatory Available Capital 40,002.\n"
    "  Pillar 1 credit risk capital requirement by exposure class (each stated as 8% of the risk weighted "
    "exposure amount) - Financial Institutions 5,768; Corporates 7,461; Retail 25; Bonds 3,899; Sovereigns 896; "
    "Multilateral Development Banks 0; Fixed and other assets 107; total 18,156.\n"
    "  Pillar 2 - Own Capital Assessment total 29,802 against Regulatory 19,686; capital resources at assessment "
    "date 40,002 on both bases.\n\n"
    "NO RWA IS RECORDED FOR FY2011, AND THAT IS DELIBERATE. The edition discloses capital REQUIREMENTS, not "
    "risk-weighted amounts. Dividing each requirement by 8% would produce a total RWA of 246,075 - but that is a "
    "derivation, and this project's standing rule is to transcribe only what a document states directly. The "
    "requirement figures are preserved verbatim above instead. READ THIS ALONGSIDE THE PRE-CRD IV METHODOLOGY "
    "NOTE BELOW: the FY2014/FY2015 Total RWA figures already on these sheets WERE produced by exactly that "
    "division, in an earlier pass. That pre-existing derivation is left untouched here (removing populated data "
    "is not this pass's call) but it is flagged, and it was deliberately NOT propagated backwards to FY2011.\n\n"
    "*** CAPITAL-COVER RATIO TRAP - WHY FY2011's RATIO CELLS ARE 'Not publicly disclosed' RATHER THAN 203% ***\n"
    "The FY2011 edition prints 'Solvency Ratio against Pillar 1 203%' and, in its Pillar 2 table, 'Capital "
    "Adequacy Ratio 203% / 134%'. These are NOT CRR-style capital ratios. The source annotates the first one "
    "itself: '(capital divided by Total amount)', i.e. available capital divided by the capital REQUIREMENT - a "
    "capital-cover multiple of roughly 12.5x a true capital/RWA ratio. Writing 203% into the Total Capital Ratio "
    "sheet would overstate the Bank's capitalisation by an order of magnitude. This exact mistake has been caught "
    "three separate times elsewhere in this project. The ratio cells for FY2011 are therefore 'Not publicly "
    "disclosed', and the 203%/134% figures live here in the note where they cannot be mistaken for CRR ratios.\n\n"
    "TWO FY2011 CAPITAL FIGURES, BOTH CARRIED, NEITHER PREFERRED SILENTLY. 'Total tier 1 capital' per the "
    "audited accounts is 43,631; 'Regulatory Available Capital' (post regulatory deductions) is 40,002. Both are "
    "on their own rows on the capital sheets. A DATING CAVEAT ON THE SECOND ONE, recorded because it could not be "
    "resolved from the document: the Pillar 2 table labels the same 40,002 'Capital resources (AT ASSESSMENT "
    "DATE)', not as at 31 December 2011, and 40,002 is also - to the GBP'000 - this workbook's FY2010 closing "
    "Total equity of GBP 40,002,338. That may be coincidence or it may mean the ICAAP assessment was run off the "
    "FY2010 year-end position. The document does not say, so no conclusion is asserted; the 43,631 figure is the "
    "one the document explicitly dates to 31 December 2011.\n\n"
    "VALIDATION GATE - PASSED CLEANLY, ACROSS THREE YEARS. The FY2011 edition's operational-risk table (section "
    "4.3.3) prints three full years of actual income in GBP, and every single line reproduces this workbook's "
    "Profit & Loss sheet to the pound: 2011 interest receivable 11,927,839 / interest payable (3,564,624) / net "
    "interest income 8,363,215 / fees and commissions 2,827,687 / exchange profits 859,674 / OPERATING INCOME "
    "12,050,576; 2010 8,243,082 / (1,269,122) / 6,973,960 / 2,106,201 / 288,424 / 9,368,585; 2009 8,943,064 / "
    "(3,027,983) / 5,915,081 / 2,050,411 / 681,633 / 8,647,125. That independently corroborates the FY2009-FY2011 "
    "P&L figures recovered from Companies House under HD-073, from a completely separate document. "
    "ONE SMALL DIVERGENCE, documented not corrected: the Pillar 3's 'Profit and loss reserve 8,630' against this "
    "workbook's FY2011 retained earnings of 8,623,795 (a GBP 6.2k gap that simple rounding to GBP'000 does not "
    "explain - 8,623,795 rounds to 8,624), and correspondingly 'Total tier 1 capital 43,631' against Total equity "
    "43,624,795. Share capital agrees exactly at 35,001. Neither figure was overwritten.\n\n"
    "*** ARCHIVE STATUS OF THE REMAINING YEARS - three genuinely different statements, kept distinct ***\n"
    "(a) FY2016 and FY2019 - PUBLISHED BUT LOST. These editions demonstrably existed: archived captures of the "
    "Bank's own Pillar 3 index page name the files. But the PDFs themselves 404 on the live site and were never "
    "captured by any crawler. This is a stronger and more useful statement than 'not found': the disclosure was "
    "made, and it is the archive that failed, so no amount of further searching of the Bank's own site will "
    "recover it. Second pass 2026-09-19 also tried archive.ph, Wayback CDX of every Zenith domain without the "
    "PDF mimetype filter, the following year's Annual Report for a comparative, the parent Zenith Bank Plc's "
    "Pillar 3 (no separate UK-entity disclosure in what is readable; live copies 403, archived copies truncated) "
    "and a web search - all negative.\n"
    "(b) FY2017, FY2018 and FY2020 - APPARENTLY NEVER POSTED. The Bank's index page only ever displayed the "
    "single latest edition, and it still showed FY2016 as at February 2019 and still showed FY2019 as at "
    "September 2021 - which implies no FY2017, FY2018 or FY2020 edition was ever published to the site. "
    "THIS IS AN INFERENCE, NOT PROOF, AND THE CAVEAT IS RECORDED DELIBERATELY: there are no index-page captures "
    "at all between February 2019 and January 2021, so an edition could have been posted and replaced inside that "
    "window without leaving a trace. (FY2020's figures are nonetheless held on these sheets, recovered from the "
    "FY2021 edition's own comparative column - see FY2020_COMPARATIVE_NOTE - so for FY2020 the question is moot.)\n"
    "(c) FY2009, FY2010, FY2012 and FY2013 - NO CAPTURE AT ALL. Neither the PDFs nor any index page naming them "
    "survives, so it is not known whether editions for these years were ever published.\n"
    "These three states are recorded separately on purpose. 'Published but lost' closes a lead permanently; "
    "'apparently never posted' is a rebuttable inference; 'no capture at all' is a genuine unknown."
)


def p3_sources():
    return (
        "Sources - Zenith Bank (UK) Limited Pillar 3 Disclosures (UK KM1 - Key Metrics; pre-CRD IV Pillar 1/2 "
        "disclosures for FY2014-FY2015 - see methodology note below), converted from USD to £ where a $ amount "
        "(see FX conversion note on the Cash Flow Statement sheet; % ratios are unconverted):\n"
        f"FY2025: Pillar 3 Disclosures as at 31 Dec 2025, p.16 (Section 10, Key Metrics) - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures as at 31 Dec 2024, p.17 (Section 9, Key Metrics) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures as at 31 Dec 2023, p.17 (Section 9, Key Metrics) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures as at 31 Dec 2022, p.24 (Section 10, Key Metrics) - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures as at 31 Dec 2021, p.23 (Section 10, Key Metrics) - {P3_2021_URL}\n"
        f"FY2015: Pillar 3 Disclosures 31 December 2015, p.8-9 (Section 4, Capital Adequacy Overview & Resources) "
        f"- {P3_2015_URL}\n"
        f"FY2014: Pillar 3 Disclosures 31 December 2014, p.8-9 (Section 4, Capital Adequacy Overview & Resources) "
        f"- {P3_2014_URL}\n"
        "FY2016-FY2019 PILLAR 3 DOCUMENTS: unobtainable, and the full fetch ladder was re-run on 2026-09-18 "
        "with every rung failing, so this is a statement about ACCESS and is recorded as such. The two file "
        "names are known from archived captures of the Bank's own Pillar 3 index page - "
        "https://zenith-bank.co.uk/media/1013/zbl_pillar_3_disclosure_document_2016.pdf (named on the 2018-04-01 "
        "and 2019-02-15 captures, the older capture pointing at the pre-2018 path "
        "http://www.zenith-bank.co.uk/uploads/ZBL_Pillar_3_Disclosure_Document_2016.pdf) and "
        "https://zenith-bank.co.uk/media/2177/zenith-bank-uk-limited-pillar-3-disclosure-2019.pdf (named on the "
        "2021-01-27 and 2021-09-19 captures). Rungs tried against each, all failing: plain curl (404 "
        "text/html), curl -L (404), curl --http1.1 -L (404), browser User-Agent with an Accept header (404); "
        "the old /uploads/ path 301-redirects to the same 404. A Wayback 'id_' raw fetch 404s for all three "
        "URLs, and a CDX enumeration of both zenith-bank.co.uk and www.zenith-bank.co.uk returns no capture of "
        "any Pillar 3 binary between the FY2015 and FY2021 editions. THIS IS NOT A STATEMENT THAT THE BANK "
        "PUBLISHED NOTHING - for FY2016 and FY2019 it demonstrably did. It is a statement that the archive "
        "failed. The capital data for these years was obtained from a completely different source family "
        "instead: see the ANNUAL-REPORT CAPITAL RECOVERY note on the capital sheets. FY2020's figures come from "
        "the FY2021 edition's own comparative column (see FY2020_COMPARATIVE_NOTE), so FY2020 needs no document "
        "of its own.\n\n"
        "PRE-CRD IV METHODOLOGY NOTE (FY2014-FY2015 only): these two years pre-date the Bank's adoption of the "
        "modern UK KM1 template and CRD IV/Basel III concepts entirely - there is no 'CET1' concept, no Leverage "
        "Ratio, no LCR and no NSFR disclosed (LCR/NSFR minimums were not yet phased in for a firm this size; the "
        "Bank's own disclosure is a Pillar 1/Pillar 2 ICAAP-style capital adequacy summary). Because the Bank's "
        "entire capital base was ordinary share capital and audited reserves (no AT1 or Tier 2 instruments then "
        "either), its single 'Tier 1 capital' figure is shown here as CET1/Tier 1/Total Capital alike, consistent "
        "with the modern-era convention used elsewhere in this workbook - but note the figure used is the "
        "Bank's own 'Regulatory Available Capital' (post regulatory deductions, the figure actually used in its "
        "published solvency ratio), not its larger undeducted 'Total tier 1 capital per audited accounts' memo "
        "figure (FY2014: $185,197k memo vs $170,802k regulatory available; FY2015: $190,521k memo vs $188,483k "
        "regulatory available). Total RWAs for FY2014/FY2015 are derived (not directly disclosed) by dividing "
        "each disclosed Pillar 1 capital requirement by 8% (the standard Basel capital-to-RWA ratio), per "
        "component (Credit/Market/Operational Risk) and summed - FY2014's derived total ($765,350k) differs by "
        "$12.5k from an alternative derivation off the disclosed grand total capital requirement ($765,363k), a "
        "rounding artefact of the source's own component figures; the per-component sum is used throughout for "
        "internal consistency with the RWA Breakdown sheet. The resulting CET1/Tier1/Total Capital ratio "
        "(regulatory available capital / derived RWA) is NOT the same figure as the Bank's own headline "
        "'Solvency Ratio against Pillar 1' (available capital / capital REQUIREMENT, i.e. roughly 12.5x this "
        "ratio) - both are shown in the RWA Breakdown sheet's source note for transparency.\n\n"
        + HIST_P3_NOTE + "\n\n" + P3_SCALE_FIX_NOTE + "\n\n" + Z16_SOURCE_NOTE
    )


bw = BankWorkbook(bank_name="Zenith Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="2A3E5C")

# ---------------------------------------------------------------
# Statement sources (Balance Sheet / P&L / Equity all come from the same
# Annual Reports already used for the Cash Flow Statement)
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - all figures are Zenith Bank (UK) Limited's own primary statements (converted from USD to £, see FX "
    "conversion note below):\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.42-43 (Statement of Profit or Loss and OCI), p.41 "
    f"(Statement of Financial Position) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.35 (Statement of Profit or Loss and OCI), p.34 "
    f"(Statement of Financial Position) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.33 (Statement of Profit or Loss and OCI), p.32 "
    f"(Statement of Financial Position) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.31 (Statement of Profit or Loss and OCI), p.30 "
    f"(Statement of Financial Position) - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020, p.31 (Statement of Comprehensive Income), p.32 (Statement of Financial "
    f"Position) - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019, p.20 (Statement of Profit or Loss and OCI), p.21 (Statement of Financial "
    f"Position) - {AR2019_URL}\n"
    f"FY2018: Annual Report and Financial Statements 2018, p.18 (Statement of Profit or Loss), p.19 (Statement "
    f"of Financial Position) - {AR2018_URL}\n"
    f"FY2017: Annual Report and Financial Statements 2017, p.17 (Statement of Profit and Loss), p.18 (Statement "
    f"of Financial Position) - {AR2017_URL}\n"
    f"FY2016: Annual Report and Accounts 2016, p.9 (Statement of Profit and Loss), p.10 (Statement of Financial "
    f"Position) - {AR2016_URL}\n"
    f"FY2015: Annual Report and Financial Statements 2015, p.9 (Statement of Profit and Loss), p.10 (Statement "
    f"of Other Comprehensive Income), p.11 (Statement of Financial Position) - {AR2015_URL}\n"
    f"FY2014: Annual Report and Financial Statements 2014, p.9 (Statement of Profit and Loss), p.10 (Statement "
    f"of Other Comprehensive Income), p.11 (Statement of Financial Position) - {AR2014_URL}\n"
    f"FY2025: Annual Report and Financial Statements 2025, pp.39-40 printed (PDF pp.41-42), Statement of Profit "
    f"or Loss and Other Comprehensive Income / Statement of Financial Position - {AR2025_URL}\n"
    "FY2025 ADDED 2026-09-18 from the Companies House filing, which is an image-only scan read VISUALLY at 300 "
    "dpi (see the Cash Flow Statement sheet's note for why the Bank's own site has no FY2025 report). The "
    "FY2025 balance sheet ties exactly: total assets 2,994,786,108 = total liabilities 2,558,955,031 + total "
    "equity 435,831,077, in USD before conversion, with no plug row.\n"
    "FY2025 NEW LINES: 'Deferred tax liabilities' (67,847) and 'Reserves (foreign currency translation)' "
    "(3,091,802) appear for the first time; in the P&L, 'Net gains realised on disposal of securities measured "
    "at amortised cost' (537,511) and 'Foreign operations - foreign currency translation differences' "
    "(3,091,802) likewise. 'Deferred tax assets' and 'Current tax liabilities' print literal DASHES for "
    "FY2025 and are carried through as '-', not as 0 - the Bank held the opposite balance in each case "
    "(a deferred tax LIABILITY and a current tax ASSET), which a zero would misstate.\n"
    "FY2024 IS RESTATED IN THE FY2025 EDITION AND THIS WORKBOOK DOES NOT USE THE RESTATEMENT. The FY2025 "
    "report heads its comparative column '2024 (Restated)' and moves US$839,784 between personnel and other "
    "expenses (personnel 22,907,160 and other 12,661,084 restated, against 23,746,944 and 11,821,300 as "
    "originally published). Every subtotal is unaffected - operating expenses, profit before tax and profit for "
    "the year are identical on both bases - so this is a pure reclassification. Per this project's standing "
    "rule the FY2024 column keeps its OWN edition's figures; the restatement is recorded here, not applied.\n"
    f"FY2013: Financial Statements for the year ended 31 December 2013, p.9 (Statement of Comprehensive Income), "
    f"p.10 (Statement of Financial Position) - {AR2013_URL}\n"
    f"FY2012: Financial Statements as at 31 December 2012, p.8 (Statement of Comprehensive Income), p.9 "
    f"(Statement of Financial Position) - {AR2012_URL}\n"
    f"FY2011: Annual report and financial statements for the year ended 31 December 2011, p.8 (Profit and loss "
    f"account), p.9 (Balance sheet) - {AR2011_URL}\n"
    f"FY2010: Annual report and financial statements for the year ended 31 December 2010, p.7 (Profit and loss "
    f"account), p.8 (Balance sheet) - {AR2010_URL}\n"
    f"FY2009: Annual report and financial statement for the year ended 31 December 2009, p.7 (Profit and loss "
    f"account), p.8 (Balance sheet) - {AR2009_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + HD048_NOTE + "\n\n" + HD073_NOTE
)

EQUITY_SOURCES = (
    "Sources - Zenith Bank (UK) Limited's own Statement of Changes in Equity (converted from USD to £, see FX "
    "conversion note below):\n"
    f"FY2025: Annual Report and Financial Statements 2025, p.41 printed (PDF p.43) - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.45 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.37 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.35 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.33 - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020, p.33 - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019, p.22 - {AR2019_URL}\n"
    f"FY2018: Annual Report and Financial Statements 2018, p.20 - {AR2018_URL}\n"
    f"FY2017: Annual Report and Financial Statements 2017, p.19 - {AR2017_URL}\n"
    f"FY2016: Annual Report and Accounts 2016, p.11 - {AR2016_URL}\n"
    f"FY2015: Annual Report and Financial Statements 2015, p.12 - {AR2015_URL}\n"
    f"FY2014: Annual Report and Financial Statements 2014, p.12 - {AR2014_URL}\n"
    f"FY2013: Financial Statements for the year ended 31 December 2013, p.11 - {AR2013_URL}\n"
    f"FY2012: Financial Statements as at 31 December 2012, p.11 (also giving the FY2013 report's own FY2012 "
    f"comparative column, cross-checked) - {AR2012_URL}\n"
    "FY2009-FY2011 equity roll-forward is blank: these years' own Annual Reports contain no Statement of "
    "Changes in Equity or Statement of Total Recognised Gains and Losses at all (see HD-073 extension note "
    "below) - a genuine, disclosed absence.\n"
    "Opening balance (1 January 2014, the earliest year shown before this HD-073 extension) is converted using the 31 Dec 2013 GBP/USD spot "
    "rate (1.6529) since it is the same balance as FY2013's closing position (outside this workbook's window). "
    "Every other opening balance is converted using that prior year's own 31 December spot rate for the same "
    "reason (e.g. 1 Jan 2021 uses the 31 Dec 2020 rate, 1.3661). Profit/OCI/dividend movements use each year's "
    "average rate; balances (opening/closing) use that date's spot rate - consistent with the rest of this "
    "workbook's FX methodology (see FX conversion note). Every year ties exactly: each closing balance matches "
    "both the next year's opening balance and that year's own Balance Sheet Total equity figure, to the penny in "
    "USD before conversion. Zero plug rows. FY2014 includes a one-off 'Currency Translation Reserve' movement "
    "(-$2,227,602, fully unwound to nil by 31 December 2014) arising from the Bank's own change of functional "
    "and presentation currency (GBP to USD) during 2013/2014, per the Bank's own report note 2(b) - a genuine "
    "historical accounting event unrelated to this workbook's own USD-to-£ conversion overlay, kept as its own "
    "distinct column rather than merged into the 'FVOCI Reserves' column (a different underlying reserve concept "
    "that wasn't introduced until FY2017 (AFS Reserve)/FY2018 (renamed FVOCI Reserve)). See the Profit & Loss "
    "sheet's own source note for a flagged discrepancy between FY2018's P&L-stated Other Comprehensive Income "
    "and this sheet's own FY2018 FVOCI Reserve movement ($(35,856) shown here, per the Bank's own Statement of "
    "Changes in Equity).\n"
    "FY2025 ADDED 2026-09-18 from the Companies House filing of the FY2025 accounts (the Bank's own site "
    "publishes annual reports only to FY2024 - see the Cash Flow Statement sheet note), which is an "
    "image-only scan read VISUALLY at 300 dpi. FY2025 ties the same way every other year does: the closing "
    "balance 435,831,077 is the FY2025 Balance Sheet Total equity, and the opening balance is FY2024's "
    "closing 382,153,296, both in USD before conversion. The Currency Translation Reserve column, nil since "
    "FY2014, moves again in FY2025 (+3,091,802) - the Bank's own 'Foreign operations - foreign currency "
    "translation differences' line, a new disclosure that year.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE + "\n\n" + HD048_NOTE + "\n\n" + HD073_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Zenith Bank (UK) Limited's own credit risk / loan impairment notes (converted from USD to £, see "
    "FX conversion note below):\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.66-68 (Credit risk note, ECL by stage) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.58-60 (Credit risk note, ECL by stage) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.56-58 (Credit risk note, ECL by stage) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.54-56 (Credit risk note, ECL by stage) - {AR2021_URL}\n"
    f"FY2020: Annual Report 2020, note 14 (Loans and advances to customers) and note 25 (Financial risk "
    f"management, IFRS 9 ECL Staging Analysis and sectoral gross exposure/impairment table) - {AR2020_URL}\n"
    f"FY2019: Annual Report 2019, note 14 and note 25 (same structure as FY2020) - {AR2019_URL}\n"
    f"FY2018: Annual Report and Financial Statements 2018, note 14 (Loans and advances to customers) and note "
    f"25 (Financial risk management, IFRS 9 ECL Staging Analysis) - {AR2018_URL}\n"
    f"FY2017: Annual Report and Financial Statements 2017, note 14 (Loans and advances to customers) - "
    f"{AR2017_URL}\n"
    f"FY2016: Annual Report and Accounts 2016, note 12 (Loans and advances to customers) - {AR2016_URL}\n"
    f"FY2015: Annual Report and Financial Statements 2015, note 12 (Loans and advances to customers) - "
    f"{AR2015_URL}\n"
    f"FY2014: Annual Report and Financial Statements 2014, note 12 (Loans and advances to customers) - "
    f"{AR2014_URL}\n"
    f"FY2025: Annual Report and Financial Statements 2025, note 18 'Loans and advances to customers' (p.63 "
    f"printed, PDF p.65), note 20a 'Movements in Impairment' (p.64 printed, PDF p.66) and the credit-risk "
    f"note's ECL-allowance reconciliation by class (p.104 printed, PDF p.106) - {AR2025_URL}\n"
    "FY2025 ADDED 2026-09-18 from the Companies House filing, read VISUALLY at 300 dpi (image-only scan). The "
    "three sources tie: gross 651,917,069 less allowance 4,755,653 = net 647,161,416, which is the balance "
    "sheet figure, and the stage split 4,099,161 + 656,492 sums to that same 4,755,653.\n"
    "FY2025 STAGE 3 IS BLANK FOR A STRUCTURAL REASON, NOT A ZERO. In FY2018-FY2024 the Bank printed a "
    "'Lifetime ECL credit-impaired' column for loans and advances to customers and filled it with an explicit "
    "nil, which is why those years show 0 here. The FY2025 edition's loans-to-customers reconciliation prints "
    "only TWO stage columns - 12-month ECL and Lifetime ECL not credit-impaired - with no Stage 3 column at "
    "all (its securities tables on the facing pages do still carry three). A column that is not printed is a "
    "different finding from a column printed as nil, so FY2025 is left blank rather than carried forward as 0.\n"
    "IFRS 9 STAGING NOTE: the Bank discloses the ECL ALLOWANCE by stage for loans and advances to customers in "
    "every year shown FY2018-FY2024 (IFRS 9 was adopted 1 January 2018), but does NOT separately disclose the "
    "GROSS CARRYING AMOUNT by stage for this specific line in FY2021-FY2024 (only the allowance split) - so a "
    "gross-exposure-based NPL ratio cannot be honestly derived from what's disclosed for those years and is not "
    "shown there. FY2019 and FY2020 uniquely DO disclose a gross-exposure/impairment sectoral breakdown (shown "
    "in the 'Impairment as % of gross exposure' row for those two years, sourced from that breakdown rather than "
    "the ECL staging table). Stage 3 (credit-impaired/default) ECL allowance is exactly nil for loans and "
    "advances to customers in every IFRS 9-era year shown (FY2018-FY2024) - a genuine finding (no identified "
    "defaulted customer exposures in the disclosed period), not an omission.\n\n"
    "HD-048 PRE-IFRS 9 NOTE (FY2014-FY2017): these four years pre-date IFRS 9 entirely and use the IAS 39 "
    "incurred-loss impairment model, which has no 'stage' concept - the IFRS 9 ECL stage rows above are "
    "genuinely blank (not zero) for FY2014-FY2017. FY2016 and FY2017 do disclose an individual/collective "
    "impairment split (a different, IAS 39-specific distinction, shown in its own section above) but not staged "
    "ECL. FY2015 discloses a single undifferentiated 'Impairment provision' with no individual/collective split "
    "at all. FY2014 discloses zero impairment provision on loans and advances to customers - an explicit "
    "disclosed nil (confirmed by the FY2015 Annual Report's own FY2014 comparative column showing '-'), not a "
    "gap. 'Gross exposure' for FY2014-FY2017 is computed as the sum of the Bank's own disclosed 'Loans to "
    "individuals' and 'Loans and advances to corporates' lines (both components of the same note); each year's "
    "own report figures are used throughout (not a later year's restated comparative) - e.g. FY2017's own report "
    "restates FY2016's corporates/individual-impairment comparatives, but FY2016's own report figures are used "
    "for the FY2016 column here, consistent with this project's convention.\n\n"
    "FY2009-FY2013 COLUMNS (added 2026-09-15): these columns appear on this sheet because the Pillar 3 year "
    "range was extended back to FY2009 to carry the newly-recovered FY2011 Pillar 3 edition. They are EMPTY of "
    "asset-quality data on purpose. The FY2011 edition is a Basel II / BIPRU capital-adequacy disclosure and "
    "contains no impairment provision figure, no arrears or default table and no exposure-quality breakdown of "
    "any kind; no Pillar 3 edition exists at all for FY2009, FY2010, FY2012 or FY2013. Nothing was carried over "
    "from the Annual Reports for these years either, since that would mix a different source basis into rows "
    "sourced from Pillar 3 disclosures. See the Pillar 3 sources note on the metric sheets for the full "
    "archive-status breakdown.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bs_rows_usd = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 428080578, "FY2024": 480233340, "FY2023": 276069567, "FY2022": 629660723, "FY2021": 882609330,
        "FY2020": 787588384, "FY2019": 572254591, "FY2018": 710130745, "FY2017": 763285083, "FY2016": 639648140,
        "FY2015": 291413936, "FY2014": 418928093,
        "FY2013": 119758144, "FY2012": 125827641, "FY2011": 82736, "FY2010": 82578}),
    ("DATA", "Derivative financial assets", {"FY2025": 2283351, "FY2024": 1517779, "FY2023": 2410504, "FY2022": 2217579, "FY2021": 5109817,
        "FY2020": 10468197, "FY2019": 2799287}),
    ("DATA", "Loans and advances to banks", {"FY2025": 195655785, "FY2024": 112643670, "FY2023": 153876803, "FY2022": 170490516, "FY2021": 154001591,
        "FY2020": 183248463, "FY2019": 265692663, "FY2018": 171079202, "FY2017": 148616109, "FY2016": 212684055,
        "FY2015": 183535220, "FY2014": 439530986,
        "FY2013": 270069035, "FY2012": 76078225, "FY2011": 167144868, "FY2010": 163499252, "FY2009": 275505662}),
    ("DATA", "Loans and advances to customers", {"FY2025": 647161416, "FY2024": 443603255, "FY2023": 353457523, "FY2022": 315202777, "FY2021": 353514574,
        "FY2020": 160807529, "FY2019": 65286592, "FY2018": 84944158, "FY2017": 121429111, "FY2016": 199388737,
        "FY2015": 367549862, "FY2014": 394374170,
        "FY2013": 265311190, "FY2012": 237794910, "FY2011": 165610568, "FY2010": 64048008, "FY2009": 17711641}),
    ("DATA", "Securities measured at fair value through profit or loss", {"FY2025": 858941, "FY2024": 4295068, "FY2023": 5106226, "FY2022": 2568446, "FY2021": 10529212,
        "FY2020": 11054949, "FY2019": 9230962, "FY2018": 50484784, "FY2017": 519995000, "FY2016": 125421660,
        "FY2015": 123501908, "FY2014": 171083814,
        "FY2013": 62069977, "FY2012": 58615627}),
    ("DATA", "Securities measured at fair value through OCI", {"FY2025": 1450126248, "FY2024": 1373024636, "FY2023": 1662513466, "FY2022": 1808390552, "FY2021": 1280759668,
        "FY2020": 971378629, "FY2019": 637735288, "FY2018": 791564517, "FY2017": 6833479}),
    ("DATA", "Securities measured at amortised cost", {"FY2025": 248905012, "FY2024": 213536320, "FY2023": 197839485, "FY2022": 194149391, "FY2021": 186251678,
        "FY2020": 175451938, "FY2019": 129654918, "FY2018": 90201310, "FY2017": 110557422, "FY2016": 139419045,
        "FY2015": 183767433, "FY2014": 172529548,
        "FY2013": 128290277, "FY2012": 110703457, "FY2011": 161808737, "FY2010": 179356464, "FY2009": 134554290}),
    ("DATA", "Right-of-use assets", {"FY2025": 7727163, "FY2024": 8693058, "FY2023": 1217453}),
    ("DATA", "Property and equipment", {"FY2025": 712536, "FY2024": 168467, "FY2023": 353650, "FY2022": 2585683, "FY2021": 3690371,
        "FY2020": 4512682, "FY2019": 4817131, "FY2018": 1217934, "FY2017": 1186214, "FY2016": 1216627,
        "FY2015": 1467395, "FY2014": 536187,
        "FY2013": 508180, "FY2012": 792741, "FY2011": 1343634, "FY2010": 1791849, "FY2009": 1773052}),
    ("DATA", "Intangible assets", {"FY2025": 3001518, "FY2024": 2446032, "FY2023": 771955, "FY2022": 993670, "FY2021": 1045877,
        "FY2020": 1395348, "FY2019": 2018933, "FY2018": 1877831, "FY2017": 991705, "FY2016": 554602,
        "FY2015": 916850, "FY2014": 1060727,
        "FY2013": 469422, "FY2012": 520450}),
    ("DATA", "Current tax assets", {"FY2025": 1306934, "FY2024": 519490, "FY2023": 569334}),
    ("DATA", "Deferred tax assets", {"FY2025": "-", "FY2024": 1024013, "FY2023": 2958195, "FY2022": 7028290, "FY2021": 1135311,
        "FY2020": 202142, "FY2019": 1050871, "FY2018": 1476943, "FY2017": 1359, "FY2016": 168609,
        "FY2015": 203170, "FY2014": 213878,
        "FY2013": 137013, "FY2012": 146656, "FY2011": 95996, "FY2010": 152097, "FY2009": 196126}),
    ("DATA", "Other assets", {"FY2025": 8966626, "FY2024": 7348853, "FY2023": 2940642, "FY2022": 1675207, "FY2021": 1811204,
        "FY2020": 1146492, "FY2019": 1031802, "FY2018": 1357582, "FY2017": 2866637, "FY2016": 928423,
        "FY2015": 1775347, "FY2014": 2761836,
        "FY2013": 3383238, "FY2012": 584023, "FY2011": 955346, "FY2010": 915276, "FY2009": 904113}),
    ("TOTAL", "Total assets", {"FY2025": 2994786108, "FY2024": 2649053981, "FY2023": 2660084803, "FY2022": 3134962834, "FY2021": 2880458633,
        "FY2020": 2307254753, "FY2019": 1691573038, "FY2018": 1904335006, "FY2017": 1675762119, "FY2016": 1319429898,
        "FY2015": 1154131121, "FY2014": 1601019239,
        "FY2013": 849996476, "FY2012": 611063730, "FY2011": 497041885, "FY2010": 409845524, "FY2009": 430644884}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 398654, "FY2024": 3094465, "FY2023": 529436, "FY2022": 455372, "FY2021": 3737253,
        "FY2020": 3256422, "FY2019": 415114}),
    ("DATA", "Deposits from banks", {"FY2025": 1467870447, "FY2024": 1285833708, "FY2023": 1283720090, "FY2022": 1971527508, "FY2021": 1891966488,
        "FY2020": 1291398297, "FY2019": 1021102222, "FY2018": 1348249858, "FY2017": 1257922170, "FY2016": 818951535,
        "FY2015": 767035698, "FY2014": 1222148447,
        "FY2013": 662795365, "FY2012": 467664981, "FY2011": 416570635, "FY2010": 341266656, "FY2009": 387577652}),
    ("DATA", "Deposits from customers", {"FY2025": 1053913293, "FY2024": 871249258, "FY2023": 985581621, "FY2022": 778495366, "FY2021": 652949933,
        "FY2020": 727848497, "FY2019": 401039700, "FY2018": 320923844, "FY2017": 203850037, "FY2016": 303070736,
        "FY2015": 191570895, "FY2014": 187633045,
        "FY2013": 109159094, "FY2012": 74161619, "FY2011": 34303520, "FY2010": 26986689, "FY2009": 4083343}),
    ("DATA", "Repurchase agreements and other similar secured borrowing", {"FY2025": 14432159, "FY2024": 88965017, "FY2023": 45992015, "FY2022": 76385080, "FY2021": 45573102}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 67847}),
    ("DATA", "Current tax liabilities", {"FY2025": "-", "FY2024": 2070141, "FY2023": 0, "FY2022": 1223535, "FY2021": 1038468,
        "FY2020": 363468, "FY2019": 4538570}),
    ("DATA", "Impairment allowance on committed/off-balance-sheet facilities", {"FY2025": 703830, "FY2024": 625420, "FY2023": 0, "FY2022": 712297, "FY2021": 792249,
        "FY2020": 287850, "FY2019": 1440717}),
    ("DATA", "Lease obligation", {"FY2025": 8497932, "FY2024": 8819920, "FY2023": 1055479, "FY2022": 1852896, "FY2021": 2957523,
        "FY2020": 4252988, "FY2019": 3760787}),
    ("DATA", "Other liabilities", {"FY2025": 12889834, "FY2024": 6073358, "FY2023": 7184781, "FY2022": 16905766, "FY2021": 7110089,
        "FY2020": 4274013, "FY2019": 5105347, "FY2018": 9761745, "FY2017": 7202616, "FY2016": 4249228,
        "FY2015": 5003866, "FY2014": 6041199,
        "FY2013": 3533014, "FY2012": 2401046, "FY2011": 2542935, "FY2010": 1589841, "FY2009": 1598730}),
    ("DATA", "Provision", {"FY2025": 181035, "FY2024": 169398}),
    ("TOTAL", "Total liabilities", {"FY2025": 2558955031, "FY2024": 2266900685, "FY2023": 2324063422, "FY2022": 2847557820, "FY2021": 2606125105,
        "FY2020": 2031681535, "FY2019": 1437402457, "FY2018": 1678935447, "FY2017": 1468974823, "FY2016": 1126271499,
        "FY2015": 963610459, "FY2014": 1415822691,
        "FY2013": 775487473, "FY2012": 544227646, "FY2011": 453417090, "FY2010": 369843186, "FY2009": 393259725}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share Capital", {"FY2025": 136701620, "FY2024": 136701620, "FY2023": 136701620, "FY2022": 136701620, "FY2021": 136701620,
        "FY2020": 136701620, "FY2019": 136701620, "FY2018": 136701620, "FY2017": 136701620, "FY2016": 136701620,
        "FY2015": 136701620, "FY2014": 136701620,
        "FY2013": 53459131, "FY2012": 53459131, "FY2011": 35001000, "FY2010": 35001000, "FY2009": 35001000}),
    ("DATA", "FVOCI Reserves", {"FY2025": 1500226, "FY2024": -598009, "FY2023": -4506575, "FY2022": -15885531, "FY2021": 543670,
        "FY2020": 4231821, "FY2019": 740531, "FY2018": -99803, "FY2017": 0}),
    ("DATA", "Reserves (foreign currency translation)", {"FY2025": 3091802}),
    ("DATA", "Retained earnings", {"FY2025": 294537429, "FY2024": 246049685, "FY2023": 203826336, "FY2022": 166588925, "FY2021": 137088238,
        "FY2020": 134639777, "FY2019": 116728430, "FY2018": 88797742, "FY2017": 70085676, "FY2016": 56456779,
        "FY2015": 53819042, "FY2014": 48494928,
        "FY2013": 21049872, "FY2012": 13376953, "FY2011": 8623795, "FY2010": 5001338, "FY2009": 2384159}),
    ("TOTAL", "Total equity", {"FY2025": 435831077, "FY2024": 382153296, "FY2023": 336021381, "FY2022": 287405014, "FY2021": 274333528,
        "FY2020": 275573218, "FY2019": 254170581, "FY2018": 225399559, "FY2017": 206787296, "FY2016": 193158399,
        "FY2015": 190520662, "FY2014": 185196548,
        "FY2013": 74509003, "FY2012": 66836084, "FY2011": 43624795, "FY2010": 40002338, "FY2009": 37385159}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 2994786108, "FY2024": 2649053981, "FY2023": 2660084803, "FY2022": 3134962834, "FY2021": 2880458633,
        "FY2020": 2307254753, "FY2019": 1691573038, "FY2018": 1904335006, "FY2017": 1675762119, "FY2016": 1319429898,
        "FY2015": 1154131121, "FY2014": 1601019239,
        "FY2013": 849996476, "FY2012": 611063730, "FY2011": 497041885, "FY2010": 409845524, "FY2009": 430644884}),
]
bw.add_balance_sheet_sheet(
    title="Zenith Bank (UK) Limited — Statement of Financial Position",
    subtitle="£'000 (FY2009-FY2013 native GBP, FY2014 onward converted from USD) - see source note at bottom for "
              "FX methodology and rates used.",
    rows=[(k, l, stock2(v) if k != "SECTION" else {}) for k, l, v in bs_rows_usd],
    sources_text=STATEMENTS_SOURCES
        + "\n\nPRESENTATION NOTE: 'Right-of-use assets' and 'Current tax assets' are shown as separate balance "
          "sheet lines only from FY2023 onward - FY2021/FY2022's own balance sheets do not present a right-of-use "
          "asset line at all (embedded within 'Property and equipment') and show no current tax asset line "
          "(the Bank held a current tax LIABILITY, not asset, in those years). FY2023 explicitly discloses both "
          "'Current tax liabilities' and 'Impairment allowance on committed but undrawn facilities' as nil (US$0), "
          "shown as 0 here (a confirmed disclosed nil, not a gap). All years FY2021-FY2024 tie exactly: Total "
          "assets = Total liabilities + Total equity, to the penny in USD before conversion - zero plug rows.\n\n"
          "HD-048 HISTORICAL STRUCTURE NOTE (FY2014-FY2020): the Bank's balance sheet classification changed "
          "materially over this period and rows are mapped onto the modern (FY2021+) labels above for "
          "comparability, per this project's convention of holding row labels constant across relabelling. "
          "FY2014-FY2017 pre-date IFRS 9 (adopted 1 January 2018): 'Securities measured at fair value through "
          "profit or loss' represents the Bank's own 'Securities Trading'/'Securities designated at fair value' "
          "line (IAS 39 FVTPL); 'Securities measured at amortised cost' represents the Bank's own 'Securities "
          "Investment (HTM: Amortised Cost)' held-to-maturity line; 'Securities measured at fair value through "
          "OCI' is blank (not zero) for FY2014-FY2016 since the Bank held no available-for-sale securities in "
          "those years, and holds the Bank's own 'Securities available for sale' figure for FY2017 (an AFS "
          "reserve of exactly $0 was disclosed alongside it that year). 'Derivative financial assets/ "
          "liabilities', 'Current tax liabilities', 'Impairment allowance on committed/off-balance-sheet "
          "facilities' and 'Lease obligation' are blank (not zero) for FY2014-FY2018 - genuinely not disclosed as "
          "separate line items until the Bank's IFRS 9 (FY2018) and IFRS 16 (FY2019) transitions respectively. "
          "'FVOCI Reserves' holds the Bank's own 'AFS Reserve' for FY2017 (both a fair-value-through-OCI type "
          "reserve on securities, renamed at the FY2018 IFRS 9 transition) - shown as a disclosed nil (0) for "
          "FY2017. All years FY2014-FY2020 individually tie exactly: Total assets = Total liabilities + Total "
          "equity, to the penny in USD before conversion - zero plug rows in any year.\n\n"
          "See the HD-073 extension note below for the FY2009-FY2013 presentation bridge (native GBP, no split "
          "Trading/Investment securities or banks/customers deposits categories, combined Other assets/"
          "Prepayments). All years FY2009-FY2013 individually tie exactly: Total assets = Total liabilities + "
          "Total equity, to the penny in £ - zero plug rows.",
    first_col_width=64,
    source_height=340,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
pl_rows_usd = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 152855012, "FY2024": 150477684, "FY2023": 148015884, "FY2022": 78988040, "FY2021": 43357525,
        "FY2020": 45697001, "FY2019": 55620170, "FY2018": 44010593, "FY2017": 32593165, "FY2016": 37726147,
        "FY2015": 43897893, "FY2014": 53163699,
        "FY2013": 28518012, "FY2012": 15116657, "FY2011": 11927839, "FY2010": 8243082, "FY2009": 8943064}),
    ("DATA", "Interest expense", {"FY2025": -67960654, "FY2024": -70136461, "FY2023": -51787199, "FY2022": -14995830, "FY2021": -5116838,
        "FY2020": -9687863, "FY2019": -11444742, "FY2018": -5389317, "FY2017": -4289571, "FY2016": -9027106,
        "FY2015": -21599705, "FY2014": -29768264,
        "FY2013": -15179027, "FY2012": -7289584, "FY2011": -3564624, "FY2010": -1269122, "FY2009": -3027983}),
    ("TOTAL", "Net interest income", {"FY2025": 84894358, "FY2024": 80341223, "FY2023": 96228685, "FY2022": 63992210, "FY2021": 38240687,
        "FY2020": 36009138, "FY2019": 44175428, "FY2018": 38621276, "FY2017": 28303594, "FY2016": 28699041,
        "FY2015": 22298188, "FY2014": 23395435,
        "FY2013": 13338985, "FY2012": 7827073, "FY2011": 8363215, "FY2010": 6973960, "FY2009": 5915081}),
    ("DATA", "Fee and commission income", {"FY2025": 12484862, "FY2024": 9673145, "FY2023": 10403918, "FY2022": 10543909, "FY2021": 8876199,
        "FY2020": 7537541, "FY2019": 6214426, "FY2018": 6231760, "FY2017": 5715902, "FY2016": 5344589,
        "FY2015": 7525215, "FY2014": 7779889,
        "FY2013": 4366386, "FY2012": 4044857, "FY2011": 2827687, "FY2010": 2106201, "FY2009": 2050411}),
    ("DATA", "Trading income", {"FY2025": 4132785, "FY2024": 3955862}),
    ("DATA", "Trading and other income", {"FY2023": 2490366, "FY2022": 5262139, "FY2021": 1121346,
        "FY2020": 8071784, "FY2019": 7678545, "FY2018": 4809574, "FY2017": 5938513, "FY2016": 3140792,
        "FY2015": 2490892, "FY2014": 2771434,
        "FY2013": 727684, "FY2012": 2573067, "FY2011": 859674, "FY2010": 288424, "FY2009": 681633}),
    ("DATA", "Net gains/(losses) on disposal of securities measured at FVOCI", {"FY2025": 1652553, "FY2024": -210586, "FY2023": -1656333}),
    ("DATA", "Net gains realised on disposal of securities measured at amortised cost", {"FY2025": 537511}),
    ("DATA", "Net loss on derecognition of financial instruments", {"FY2025": "-", "FY2024": -7486009}),
    ("DATA", "Fair value movement on financial derivatives (net)", {"FY2025": 3461383, "FY2024": -3457754, "FY2023": 150805, "FY2022": -6904275}),
    ("DATA", "Exchange differences", {"FY2025": -2836893, "FY2024": 2466208, "FY2023": -1415863, "FY2022": 4359385}),
    ("DATA", "Revaluation loss", {"FY2021": -4304574, "FY2020": -2178091}),
    ("TOTAL", "Operating income", {"FY2025": 104326559, "FY2024": 85282089, "FY2023": 106201578, "FY2022": 77253368, "FY2021": 43933658,
        "FY2020": 49440372, "FY2019": 58068399, "FY2018": 49662610, "FY2017": 39958009, "FY2016": 37184422,
        "FY2015": 32314295, "FY2014": 33946758,
        "FY2013": 18433055, "FY2012": 14444997, "FY2011": 12050576, "FY2010": 9368585, "FY2009": 8647125}),
    ("DATA", "Personnel expenses", {"FY2025": -25420871, "FY2024": -23746944, "FY2023": -22411476, "FY2022": -17086793, "FY2021": -17001905,
        "FY2020": -16505084, "FY2019": -15264115, "FY2018": -13552715, "FY2017": -11094584, "FY2016": -9582063,
        "FY2015": -10903849, "FY2014": -10216790,
        "FY2013": -5188618, "FY2012": -4630847, "FY2011": -4336107}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -2201577, "FY2024": -1684109, "FY2023": -1624921, "FY2022": -1674804, "FY2021": -1777063,
        "FY2020": -2131922, "FY2019": -1876779, "FY2018": -1042000, "FY2017": -676971, "FY2016": -782432,
        "FY2015": -1078502, "FY2014": -963537,
        "FY2013": -761420, "FY2012": -584051}),
    ("DATA", "Other expenses", {"FY2025": -14918196, "FY2024": -11821300, "FY2023": -8600456, "FY2022": -7959047, "FY2021": -7826210,
        "FY2020": -7524345, "FY2019": -6229315, "FY2018": -5751386, "FY2017": -5378682, "FY2016": -5393488,
        "FY2015": -4895048, "FY2014": -3764272,
        "FY2013": -2423272, "FY2012": -2302011, "FY2011": -2609506, "FY2010": -5690338, "FY2009": -5394780}),
    ("TOTAL", "Operating expenses", {"FY2025": -42540644, "FY2024": -37252353, "FY2023": -32636853, "FY2022": -26720644, "FY2021": -26605178,
        "FY2020": -26161351, "FY2019": -23370209, "FY2018": -20346101, "FY2017": -17150237, "FY2016": -15757983,
        "FY2015": -16877399, "FY2014": -14944599,
        "FY2013": -8373310, "FY2012": -7516909, "FY2011": -6945613, "FY2010": -5690338, "FY2009": -5394780}),
    ("TOTAL", "Operating profit before impairment provision and taxation", {"FY2025": 61785915, "FY2024": 48029736, "FY2023": 73564725, "FY2022": 50532724, "FY2021": 17328480,
        "FY2020": 23279021, "FY2019": 34698190, "FY2018": 29316509, "FY2017": 22807772, "FY2016": 21426439,
        "FY2015": 15436896, "FY2014": 19002159,
        "FY2013": 10059745, "FY2012": 6928088, "FY2011": 5104963, "FY2010": 3678247, "FY2009": 3252345}),
    ("DATA", "Net impairment credit/(charge) on financial assets", {"FY2025": 2869499, "FY2024": 8225131, "FY2023": -771074, "FY2022": -5269233, "FY2021": -3692274,
        "FY2020": -1396175, "FY2019": 23518, "FY2018": 4522490, "FY2017": -6798273, "FY2016": -18000806,
        "FY2015": -8338078, "FY2014": 0}),
    ("TOTAL", "Profit before tax", {"FY2025": 64655414, "FY2024": 56254867, "FY2023": 72793651, "FY2022": 45263491, "FY2021": 13636206,
        "FY2020": 21882846, "FY2019": 34721708, "FY2018": 33838999, "FY2017": 16009499, "FY2016": 3425633,
        "FY2015": 7098818, "FY2014": 19002159,
        "FY2013": 10059745, "FY2012": 6928088, "FY2011": 5104963, "FY2010": 3678247, "FY2009": 3252345}),
    ("DATA", "Income tax expense", {"FY2025": -16167670, "FY2024": -14031518, "FY2023": -17956240, "FY2022": -10062804, "FY2021": -2232071,
        "FY2020": -3971499, "FY2019": -6791020, "FY2018": -6329242, "FY2017": -2380602, "FY2016": -787896,
        "FY2015": -1774704, "FY2014": -4608024,
        "FY2013": -2386826, "FY2012": -1696136, "FY2011": -1482506, "FY2010": -1061068, "FY2009": -910656}),
    ("TOTAL", "Profit for the year", {"FY2025": 48487744, "FY2024": 42223349, "FY2023": 54837411, "FY2022": 35200687, "FY2021": 11404135,
        "FY2020": 17911347, "FY2019": 27930688, "FY2018": 27509757, "FY2017": 13628897, "FY2016": 2637737,
        "FY2015": 5324114, "FY2014": 14394135,
        "FY2013": 7672919, "FY2012": 5231952, "FY2011": 3622457, "FY2010": 2617179, "FY2009": 2341689}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Foreign operations - foreign currency translation differences", {"FY2025": 3091802}),
    ("DATA", "Net change in fair value of debt instruments at FVOCI", {"FY2025": 4890069, "FY2024": 5614429, "FY2023": 13774075, "FY2022": -22511501, "FY2021": -3808346,
        "FY2020": 5396456, "FY2019": 1362245, "FY2018": -120245}),
    ("DATA", "Net change in fair value of debt instruments reclassified to profit or loss", {"FY2025": -1652553, "FY2024": 210586, "FY2023": 1656333, "FY2022": -50484, "FY2021": -598380,
        "FY2020": -1063043, "FY2019": -349794}),
    ("DATA", "Expected credit loss reversals/(gains) recognised in income statement", {"FY2025": -329902, "FY2024": -460195, "FY2023": -193850}),
    ("DATA", "Income tax on items reclassified subsequently to profit or loss", {"FY2025": -809379, "FY2024": -1456254, "FY2023": -3857602, "FY2022": 6132784, "FY2021": 718575,
        "FY2020": -842123, "FY2019": -172117, "FY2018": 20442}),
    ("DATA", "Currency translation reserve arising from change of functional and presentation currency", {"FY2014": -2227602}),
    ("TOTAL", "Other comprehensive income for the year (net of tax)", {"FY2025": 5190037, "FY2024": 3908566, "FY2023": 11378956, "FY2022": -16429201, "FY2021": -3688151,
        "FY2020": 3491290, "FY2019": 840334, "FY2018": -99803, "FY2017": 0, "FY2016": 0, "FY2015": 0,
        "FY2014": -2227602,
        "FY2013": 0, "FY2012": 0, "FY2011": 0, "FY2010": 0, "FY2009": 0}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 53677781, "FY2024": 46131915, "FY2023": 66216367, "FY2022": 18771486, "FY2021": 7715984,
        "FY2020": 21402637, "FY2019": 28771022, "FY2018": 27409954, "FY2017": 13628897, "FY2016": 2637737,
        "FY2015": 5324114, "FY2014": 12166533,
        "FY2013": 7672919, "FY2012": 5231952, "FY2011": 3622457, "FY2010": 2617179, "FY2009": 2341689}),
]
bw.add_income_statement_sheet(
    title="Zenith Bank (UK) Limited — Statement of Profit or Loss and Other Comprehensive Income",
    subtitle="£'000 (FY2009-FY2013 native GBP, FY2014 onward converted from USD) - see source note at bottom for "
              "FX methodology and rates used.",
    rows=[(k, l, flow2(v) if k != "SECTION" else {}) for k, l, v in pl_rows_usd],
    sources_text=STATEMENTS_SOURCES
        + "\n\nPRESENTATION NOTE: row labels are held constant across years for comparability where the underlying "
          "concept is the same, even though the Bank's own report relabels/regroups some lines year to year - e.g. "
          "FY2022/FY2023's own reports label the pre-impairment subtotal 'Net operating income' rather than "
          "'Operating profit before impairment provision and taxation' (FY2021/FY2024's label, used here "
          "throughout); 'Trading income' (FY2024) replaces 'Trading and other income' (FY2021-FY2023) as a "
          "relabelling, not a scope change; FY2021's FV-movement/exchange-difference/FVOCI-disposal lines are "
          "combined into a single 'Revaluation loss' line in that year's report (not split as in later years, and "
          "NOT split to match AR2022's restated FY2021 comparative - FY2021's own report figure is used). "
          "'Net gains/(losses) on disposal of securities measured at FVOCI' and 'Expected credit loss "
          "reversals/(gains) recognised in income statement' are new lines first disclosed in FY2023's own report "
          "(present for FY2023 and FY2024 only; blank, not zero, for FY2021/FY2022 since those years' own reports "
          "genuinely do not disclose them as separate items - each is a carve-out of a few tens of thousands of "
          "dollars from a pre-existing broader line, with zero effect on any subtotal). "
          "RESTATEMENT NOTE: FY2023's own P&L (used for FY2023's column here, net interest income $96,228,685) "
          "differs from the FY2024 Annual Report's restated FY2023 comparative (interest income revised down to "
          "$147,456,638, net interest income $95,669,439) - FY2023's own report figure is used, consistent with "
          "this project's convention and the same restatement already documented on the Cash Flow Statement sheet. "
          "All totals tie exactly to the penny in USD before conversion for FY2021-FY2024 - zero plug rows.\n\n"
          "HD-048 HISTORICAL NOTE (FY2014-FY2020): FY2014-FY2017 (pre-IFRS 9) show a single 'Net impairment "
          "credit/(charge)' figure that was always a charge (never a credit) under the IAS 39 incurred-loss "
          "model then in force - FY2014 discloses this as an explicit nil ($0, per the comparative column in "
          "its own FY2015 Annual Report), not a genuine gap. 'Trading and other income' holds the Bank's own "
          "'Other Income' (FY2014-FY2015) and 'Trading and other income' (FY2016-FY2019) lines - the same "
          "broad non-interest, non-fee income category (including FX gains) under differing labels each year. "
          "FY2014's Other Comprehensive Income is a one-off 'Currency translation reserve arising from change "
          "of functional and presentation currency' movement (-$2,227,602, fully unwound by year-end), per the "
          "Bank's own note 2(b) - a genuine historical accounting event (the Bank changed its functional and "
          "presentation currency from GBP to USD during 2013/2014), not a fair-value item, and unrelated to "
          "this workbook's own USD-to-£ conversion overlay. DISCREPANCY NOTE: FY2018's own P&L states Other "
          "Comprehensive Income for the year as $(99,803) (shown here, tying to Total Comprehensive Income "
          "$27,409,954), but the Statement of Changes in Equity's own FVOCI Reserve column moves by only "
          "$(35,856) that year (from $(63,947) post-IFRS 9 transition to $(99,803) closing) - the $63,947 gap "
          "exactly equals the FY2018 opening IFRS 9 transition adjustment, suggesting the Bank's own P&L 'OCI "
          "for the year' line may have inadvertently included that opening adjustment rather than showing only "
          "the year's movement. Both figures are shown exactly as each statement discloses them (P&L here; "
          "Statement of Changes in Equity on its own sheet) rather than forcing an artificial reconciliation - "
          "flagged as a genuine apparent inconsistency in the Bank's own FY2018 Annual Report, not a data-entry "
          "error in this workbook. All other years FY2014-FY2020 tie exactly to the penny in USD before "
          "conversion - zero plug rows.\n\n"
          "HD-073 EXTENSION NOTE (FY2009-FY2013): 'Net impairment credit/(charge)' is blank (not zero) for all "
          "five years - none of these years' own P&L accounts separately disclose an impairment charge, so it "
          "cannot be honestly distinguished from 'Other expenses' below. 'Personnel expenses' and 'Depreciation "
          "and amortisation' are blank (not zero) for FY2009/FY2010 - both years' own reports show a single "
          "combined 'Administrative expenses' line (shown here under 'Other expenses'); FY2011 splits out "
          "'Employee costs' (shown as 'Personnel expenses') but still combines depreciation within its own "
          "'Administrative expenses' line (shown here under 'Other expenses'). Each year FY2009-FY2013 ties "
          "exactly: Operating income - Operating expenses = Operating profit before tax = Profit before tax "
          "(no separate impairment line in any of these years' own reports), and Profit before tax - tax = "
          "Profit for the year, to the penny in £ - zero plug rows. Other Comprehensive Income is shown as an "
          "explicit disclosed nil (0) for FY2009-FY2013: each year's own report states 'There are no recognised "
          "gains or losses for the year other than as stated above' (FY2009-FY2011) or explicitly discloses "
          "'Other Comprehensive Income for the year: -' (FY2012-FY2013). See the HD-073 extension note on the "
          "Cash Flow Statement sheet for the restatement/relabelling discrepancies between each year's own "
          "report and later years' comparative columns.",
    first_col_width=68,
    source_height=420,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity (chronological, oldest to newest)
# ---------------------------------------------------------------
EQ_HEADERS = ["Share Capital", "Currency Translation Reserve", "FVOCI Reserves", "Retained Earnings", "Total Equity"]


def eq_stock(usd_tuple, year):
    return tuple(round(v / FX_SPOT[year] / 1000, 1) for v in usd_tuple)


def eq_flow(usd_tuple, year):
    return tuple(round(v / FX_AVG[year] / 1000, 1) for v in usd_tuple)


def eq_gbp(gbp_tuple):
    """HD-073: FY2012/FY2013 equity rows are native £ (see NATIVE_GBP_YEARS) - no FX conversion needed."""
    return tuple(round(v / 1000, 1) for v in gbp_tuple)


EQ_ROWS = [
    ("TOTAL", "Balance as at 1 January 2012", eq_gbp((35001000, 0, 0, 8108518, 43109518))),
    ("DATA", "Profit for the year (FY2012)", eq_gbp((0, 0, 0, 5231952, 5231952))),
    ("DATA", "Transfer from reserves (FY2012)", eq_gbp((0, 0, 0, 36483, 36483))),
    ("DATA", "Shares issued (FY2012)", eq_gbp((18458131, 0, 0, 0, 18458131))),
    ("TOTAL", "Balance as at 31 December 2012 / 1 January 2013", eq_gbp((53459131, 0, 0, 13376953, 66836084))),
    ("DATA", "Profit for the year (FY2013)", eq_gbp((0, 0, 0, 7672919, 7672919))),
    ("TOTAL", "Balance as at 31 December 2013 (per FY2013's own Annual Report)", eq_gbp((53459131, 0, 0, 21049872, 74509003))),
    ("TOTAL", "Balance as at 1 January 2014", eq_stock((86887142, 2227602, 0, 34100793, 123215537), "FY2013")),
    ("DATA", "Profit for the year (FY2014)", eq_flow((0, 0, 0, 14394135, 14394135), "FY2014")),
    ("DATA", "Adjustment resulting from redenomination (FY2014)", eq_flow((-185522, 0, 0, 0, -185522), "FY2014")),
    ("DATA", "Issuance of new shares (FY2014)", eq_flow((50000000, 0, 0, 0, 50000000), "FY2014")),
    ("DATA", "Currency translation reserve movement (FY2014)", eq_flow((0, -2227602, 0, 0, -2227602), "FY2014")),
    ("TOTAL", "Balance as at 31 December 2014", eq_stock((136701620, 0, 0, 48494928, 185196548), "FY2014")),
    ("DATA", "Profit for the year (FY2015)", eq_flow((0, 0, 0, 5324114, 5324114), "FY2015")),
    ("TOTAL", "Balance as at 31 December 2015", eq_stock((136701620, 0, 0, 53819042, 190520662), "FY2015")),
    ("DATA", "Profit for the year (FY2016)", eq_flow((0, 0, 0, 2637737, 2637737), "FY2016")),
    ("TOTAL", "Balance as at 31 December 2016", eq_stock((136701620, 0, 0, 56456779, 193158399), "FY2016")),
    ("DATA", "Profit for the year (FY2017)", eq_flow((0, 0, 0, 13628897, 13628897), "FY2017")),
    ("TOTAL", "Balance as at 31 December 2017", eq_stock((136701620, 0, 0, 70085676, 206787296), "FY2017")),
    ("DATA", "Impact of adopting IFRS 9 at 1 January 2018", eq_flow((0, 0, -63947, -8797691, -8861638), "FY2018")),
    ("DATA", "Profit for the year (FY2018)", eq_flow((0, 0, 0, 27509757, 27509757), "FY2018")),
    ("DATA", "Fair value reserve movement, debt instruments (FY2018)", eq_flow((0, 0, -35856, 0, -35856), "FY2018")),
    ("TOTAL", "Balance as at 31 December 2018", eq_stock((136701620, 0, -99803, 88797742, 225399559), "FY2018")),
    ("DATA", "Profit for the year (FY2019)", eq_flow((0, 0, 0, 27930688, 27930688), "FY2019")),
    ("DATA", "Fair value reserve movement, net of tax (FY2019)", eq_flow((0, 0, 840334, 0, 840334), "FY2019")),
    ("TOTAL", "Balance as at 31 December 2019", eq_stock((136701620, 0, 740531, 116728430, 254170581), "FY2019")),
    ("DATA", "Profit for the year (FY2020)", eq_flow((0, 0, 0, 17911347, 17911347), "FY2020")),
    ("DATA", "Fair value reserve movement, net of tax (FY2020)", eq_flow((0, 0, 3491290, 0, 3491290), "FY2020")),
    ("TOTAL", "Balance as at 31 December 2020", eq_stock((136701620, 0, 4231821, 134639777, 275573218), "FY2020")),
    ("DATA", "Profit for the year (FY2021)", eq_flow((0, 0, 0, 11404135, 11404135), "FY2021")),
    ("DATA", "Other comprehensive income (FY2021)", eq_flow((0, 0, -3688151, 0, -3688151), "FY2021")),
    ("DATA", "Dividends paid to shareholders (FY2021)", eq_flow((0, 0, 0, -8955674, -8955674), "FY2021")),
    ("TOTAL", "Balance as at 31 December 2021", eq_stock((136701620, 0, 543670, 137088238, 274333528), "FY2021")),
    ("DATA", "Profit for the year (FY2022)", eq_flow((0, 0, 0, 35200687, 35200687), "FY2022")),
    ("DATA", "Other comprehensive income (FY2022)", eq_flow((0, 0, -16429201, 0, -16429201), "FY2022")),
    ("DATA", "Dividends paid to shareholders (FY2022)", eq_flow((0, 0, 0, -5700000, -5700000), "FY2022")),
    ("TOTAL", "Balance as at 31 December 2022", eq_stock((136701620, 0, -15885531, 166588925, 287405014), "FY2022")),
    ("DATA", "Profit for the year (FY2023)", eq_flow((0, 0, 0, 54837411, 54837411), "FY2023")),
    ("DATA", "Other comprehensive income (FY2023)", eq_flow((0, 0, 11378956, 0, 11378956), "FY2023")),
    ("DATA", "Dividends paid to shareholders (FY2023)", eq_flow((0, 0, 0, -17600000, -17600000), "FY2023")),
    ("TOTAL", "Balance as at 31 December 2023", eq_stock((136701620, 0, -4506575, 203826336, 336021381), "FY2023")),
    ("DATA", "Profit for the year (FY2024)", eq_flow((0, 0, 0, 42223349, 42223349), "FY2024")),
    ("DATA", "Other comprehensive income (FY2024)", eq_flow((0, 0, 3908566, 0, 3908566), "FY2024")),
    ("DATA", "Dividends paid to shareholders (FY2024)", eq_flow((0, 0, 0, 0, 0), "FY2024")),
    ("TOTAL", "Balance as at 31 December 2024", eq_stock((136701620, 0, -598009, 246049685, 382153296), "FY2024")),
    ("DATA", "Profit for the year (FY2025)", eq_flow((0, 0, 0, 48487744, 48487744), "FY2025")),
    ("DATA", "Other comprehensive income (FY2025)", eq_flow((0, 3091802, 2098235, 0, 5190037), "FY2025")),
    ("DATA", "Dividends paid to shareholders (FY2025)", eq_flow((0, 0, 0, 0, 0), "FY2025")),
    ("TOTAL", "Balance as at 31 December 2025", eq_stock((136701620, 3091802, 1500226, 294537429, 435831077), "FY2025")),
]
bw.add_equity_changes_sheet(
    title="Zenith Bank (UK) Limited — Statement of Changes in Equity",
    subtitle="£'000 (FY2012-FY2013 native GBP, FY2014 onward converted from USD) - chronological 1 January 2012 "
              "through 31 December 2025. No FY2009-FY2011 movement shown (no Statement of Changes in Equity "
              "disclosed those years - see HD-073 extension note).",
    headers=EQ_HEADERS,
    rows=EQ_ROWS,
    sources_text=EQUITY_SOURCES,
    first_col_width=56,
    source_height=460,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD, then converted via flow()/stock()/opening_cash())
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit for the year", {"FY2025": 48487744, "FY2024": 42223349, "FY2023": 54837411, "FY2022": 35200687, "FY2021": 11404135,
        "FY2020": 17911347, "FY2019": 27930688, "FY2018": 27509757, "FY2017": 13628897, "FY2016": 2637737,
        "FY2015": 5324114, "FY2014": 14394135,
        "FY2013": 7672919, "FY2012": 5231952}),
    ("DATA", "Impairment provision charge/(reversal)", {"FY2025": -2869499, "FY2024": -8225131, "FY2023": 771074, "FY2022": 5269233, "FY2021": 3692274,
        "FY2020": 1396175, "FY2019": -23518, "FY2018": -4522490, "FY2017": 6798273, "FY2016": 18000806,
        "FY2015": 8338078}),
    ("DATA", "Depreciation of property and equipment", {"FY2025": 1151977, "FY2024": 1184560, "FY2023": 1074768, "FY2022": 1131020, "FY2021": 1114950,
        "FY2020": 1124032, "FY2019": 924552, "FY2018": 226148, "FY2017": 198830, "FY2016": 258695,
        "FY2015": 445765, "FY2014": 393679,
        "FY2013": 413782, "FY2012": 255337}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 1049600, "FY2024": 499549, "FY2023": 550153, "FY2022": 543784, "FY2021": 662113,
        "FY2020": 1007890, "FY2019": 952227, "FY2018": 815852, "FY2017": 478141, "FY2016": 523737,
        "FY2015": 632737, "FY2014": 569858,
        "FY2013": 347638, "FY2012": 328714}),
    ("DATA", "Interest expense on Right-of-use lease obligations", {"FY2025": 340871, "FY2024": 346769, "FY2023": 18326, "FY2021": 49200, "FY2020": 39715}),
    ("DATA", "Interest expense (transition to IFRS 16)", {"FY2019": 33523}),
    ("DATA", "Exchange difference on property and equipment", {"FY2018": -109316}),
    ("DATA", "Exchange difference on intangible assets", {"FY2018": -362033}),
    ("DATA", "Gain on disposal of property and equipment", {"FY2016": 0, "FY2015": -8418}),
    ("DATA", "Recoveries of bad debts written off", {"FY2022": -69063}),
    ("DATA", "Current income tax expense", {"FY2025": 15885189, "FY2024": 13553590, "FY2023": 17745025, "FY2022": 9439732, "FY2021": 2232071}),
    ("DATA", "Deferred income tax expense", {"FY2025": 282481, "FY2024": 477928, "FY2023": 211215, "FY2022": 239806}),
    ("DATA", "Income tax expense (not split current/deferred - pre-FY2021 presentation)", {"FY2020": 3971499, "FY2019": 6791020,
        "FY2018": 6308800, "FY2017": 2380602, "FY2016": 787896, "FY2015": 1774704, "FY2014": 4608024,
        "FY2013": 2386826, "FY2012": 1696136}),
    ("DATA", "Foreign currency translation gain - Right-of-use assets", {"FY2021": -211646}),
    ("DATA", "Foreign currency translation gain/(loss) - Lease obligation", {"FY2023": 110592, "FY2022": -317849, "FY2021": -307066, "FY2020": 100768}),
    ("DATA", "Foreign currency translation gain - Deferred tax assets", {"FY2022": 45}),
    ("DATA", "Foreign currency translation (gain)/loss - Corporation tax liability", {"FY2023": -123381, "FY2022": -43758, "FY2021": -2756, "FY2020": 256863}),
    ("DATA", "Deferred tax asset write-off (legacy)", {"FY2023": 1278}),
    ("DATA", "Impairment on equity investments", {"FY2021": 66644, "FY2020": 715000}),
    ("DATA", "Interest income", {"FY2025": -152855012, "FY2024": -150477684, "FY2023": -148015884, "FY2022": -78988040}),
    ("DATA", "Interest expense", {"FY2025": 67619783, "FY2024": 69789692, "FY2023": 51768873, "FY2022": 14995830}),
    ("DATA", "Fair value movement on securities measured at FVTPL", {"FY2025": -16957, "FY2024": 69201}),
    ("DATA", "Fair value movement on derivative contracts", {"FY2025": -3461383, "FY2024": 3457754}),
    ("DATA", "Unrealised foreign exchange (gains)/losses", {"FY2025": 2836893, "FY2024": -2466206}),
    ("DATA", "Loss on derecognition of assets", {"FY2025": "-", "FY2024": 7486009}),
    ("DATA", "Decrease/(Increase) in loans and advances to banks", {"FY2025": -78759931, "FY2024": 37241172, "FY2023": 17720794, "FY2022": -16995457, "FY2021": 29588441,
        "FY2020": 84541499, "FY2019": -96133912, "FY2018": -24710757, "FY2017": 64067945, "FY2016": -29148835,
        "FY2015": 247657688, "FY2014": 7082177,
        "FY2013": -193990810, "FY2012": -14659225}),
    ("DATA", "(Increase)/Decrease in loans and advances to customers", {"FY2025": -181060997, "FY2024": -92041493, "FY2023": -37968440, "FY2022": 39931143, "FY2021": -196507247,
        "FY2020": -96046865, "FY2019": 22399433, "FY2018": 36689839, "FY2017": 71161353, "FY2016": 150160319,
        "FY2015": 26824308, "FY2014": 44370945,
        "FY2013": -27516280, "FY2012": -72540579}),
    ("DATA", "(Increase)/Decrease in securities measured at fair value through profit or loss", {"FY2025": 2036105, "FY2024": -120096, "FY2023": -1751539, "FY2022": 6591830, "FY2021": 525737,
        "FY2020": -1823987, "FY2019": 41253822, "FY2018": 469510216, "FY2017": -394573340, "FY2016": -1919752,
        "FY2015": 47581906, "FY2014": -68438693,
        "FY2013": -3454350, "FY2012": 1004827}),
    ("DATA", "Decrease/(Increase) in securities measured at FVOCI", {"FY2025": -26080929, "FY2024": 314536239, "FY2023": 155867577, "FY2022": -568931339, "FY2021": -313837082,
        "FY2020": -330316519, "FY2019": 153839342, "FY2018": -784800380, "FY2017": -6833479}),
    ("DATA", "(Increase)/Decrease in other assets", {"FY2025": -2401341, "FY2024": -4408211, "FY2023": -1265435, "FY2022": 135997, "FY2021": -577710,
        "FY2020": -201692, "FY2019": 325780, "FY2018": 1509055, "FY2017": -1964229, "FY2016": 1281923,
        "FY2015": 997352, "FY2014": 168049,
        "FY2013": -2799216, "FY2012": 183296}),
    ("DATA", "(Decrease)/Increase in deposits from banks", {"FY2025": 184299969, "FY2024": -7577015, "FY2023": -688088465, "FY2022": 79243126, "FY2021": 600568191,
        "FY2020": 270296075, "FY2019": -327147636, "FY2018": 90327688, "FY2017": 438970636, "FY2016": 51915837,
        "FY2015": -455112749, "FY2014": 126083752,
        "FY2013": 195130384, "FY2012": 51198910}),
    ("DATA", "(Decrease)/Increase in deposits from customers", {"FY2025": 111357906, "FY2024": -104968633, "FY2023": 200100437, "FY2022": 123837261, "FY2021": -74898564,
        "FY2020": 326808797, "FY2019": 80115856, "FY2018": 117073807, "FY2017": -99220699, "FY2016": 111499841,
        "FY2015": 3937850, "FY2014": 7116651,
        "FY2013": 34997475, "FY2012": 39858099}),
    ("DATA", "Increase/(Decrease) in repurchase agreements and other similar secured borrowing", {"FY2025": -74667742, "FY2024": 43001229, "FY2023": -30579358, "FY2022": 30379006, "FY2021": 45573102}),
    ("DATA", "(Increase)/Decrease in derivative financial instruments (net)", {"FY2023": -118861, "FY2022": -389643, "FY2021": 5839211,
        "FY2020": -4827602, "FY2019": -4137670}),
    ("DATA", "Increase/(Decrease) in other liabilities", {"FY2025": 5419946, "FY2024": 4871782, "FY2023": -9720985, "FY2022": 9795677, "FY2021": 2836076,
        "FY2020": -831334, "FY2019": 877939, "FY2018": 2108560, "FY2017": 572785, "FY2016": -890837,
        "FY2015": 188469, "FY2014": 198654,
        "FY2013": 930910, "FY2012": 274720}),
    ("DATA", "Interest income received", {"FY2025": 104378215, "FY2024": 104041078, "FY2023": 136365040, "FY2022": 86951488}),
    ("DATA", "Interest expense paid", {"FY2025": -60066733, "FY2024": -53649527, "FY2023": -44315715, "FY2022": -12499405}),
    ("DATA", "Income tax paid", {"FY2025": -18680207, "FY2024": -11483449, "FY2023": -19414513, "FY2022": -9210907, "FY2021": -1768909,
        "FY2020": -8396868, "FY2019": -5607218, "FY2018": -5733070, "FY2017": 0, "FY2016": -651696,
        "FY2015": -3000505, "FY2014": -4274901,
        "FY2013": -2194624, "FY2012": -1674305}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": -55774052, "FY2024": 207362455, "FY2023": -344220013, "FY2022": -243759796, "FY2021": 116041165,
        "FY2020": 265724803, "FY2019": -97605772, "FY2018": -68158324, "FY2017": 95665715, "FY2016": 304455671,
        "FY2015": -114418701, "FY2014": 132272330,
        "FY2013": 11924654, "FY2012": 11157882}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of securities measured at amortised cost", {"FY2025": -98093757, "FY2024": -81087234, "FY2023": -26729752, "FY2022": -47624983, "FY2021": -42913212,
        "FY2020": -55052328, "FY2019": -55163699, "FY2018": -49210034}),
    ("DATA", "Proceeds from redemption of securities measured at amortised cost", {"FY2025": 72160896, "FY2024": 69818444, "FY2023": 21071506, "FY2022": 27641163, "FY2021": 32279901,
        "FY2020": 5513488, "FY2019": 16783131, "FY2018": 65702517}),
    ("DATA", "Net change in securities measured at amortised cost (pre-FY2018 combined presentation)", {"FY2017": 28861623, "FY2016": 44348388,
        "FY2015": -11237885, "FY2014": 39624083,
        "FY2013": -17586820, "FY2012": -8861658}),
    ("DATA", "Interest income received (investing)", {"FY2025": 17432597, "FY2024": 14053675, "FY2023": 15202064, "FY2022": 17837082}),
    ("DATA", "Acquisition of property and equipment", {"FY2025": -730151, "FY2024": -62128, "FY2023": -60188, "FY2022": -26331, "FY2021": -34354,
        "FY2020": -285977, "FY2019": -191136, "FY2018": -148552, "FY2017": -50492, "FY2016": -269604,
        "FY2015": -1431853, "FY2014": -127582,
        "FY2013": -129221, "FY2012": -233396}),
    ("DATA", "Proceeds from sale of property and equipment", {"FY2016": 0, "FY2015": 52412, "FY2014": 0, "FY2013": 18500}),
    ("DATA", "Additions to Right-of-use assets", {"FY2021": -46639, "FY2020": -533606}),
    ("DATA", "Acquisition of intangible assets", {"FY2025": -1605086, "FY2024": -2173626, "FY2023": -328438, "FY2022": -491577, "FY2021": -312642,
        "FY2020": -384305, "FY2019": -1093329, "FY2018": -1339945, "FY2017": -839903, "FY2016": -300251,
        "FY2015": -478130, "FY2014": -884781,
        "FY2013": -296610, "FY2012": -320212}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2025": -10835501, "FY2024": 549131, "FY2023": 9155192, "FY2022": -2664646, "FY2021": -11026946,
        "FY2020": -50742728, "FY2019": -39665033, "FY2018": 15003986, "FY2017": 27971228, "FY2016": 43778533,
        "FY2015": -13095456, "FY2014": 38611720,
        "FY2013": -17994151, "FY2012": -9415266}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of lease liability/obligation", {"FY2025": -926443, "FY2024": -672177, "FY2023": -926335, "FY2022": -824165, "FY2021": -1084238,
        "FY2020": -181888, "FY2019": -571826}),
    ("DATA", "Interest payment on Lease liability", {"FY2025": -340871}),
    ("DATA", "Addition of new lease obligation", {"FY2021": 46639, "FY2020": 533606}),
    ("DATA", "Interest payment on lease obligation (transition to IFRS 16)", {"FY2020": 0, "FY2019": -33523}),
    ("DATA", "Proceeds from issue of share capital", {"FY2014": 50000000, "FY2013": 0, "FY2012": 18458131}),
    ("DATA", "Dividends paid to shareholders", {"FY2023": -17600000, "FY2022": -5700000, "FY2021": -8955674}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {"FY2025": -1267314, "FY2024": -672177, "FY2023": -18526335, "FY2022": -6524165, "FY2021": -9993273,
        "FY2020": 351718, "FY2019": -605349, "FY2014": 50000000,
        "FY2013": 0, "FY2012": 18458131}),
    ("TOTAL", "Net (decrease)/increase of cash and cash equivalents", {"FY2025": -67876867, "FY2024": 207239409, "FY2023": -353591156, "FY2022": -252948607, "FY2021": 95020946,
        "FY2020": 215333793, "FY2019": -137876154, "FY2018": -53154338, "FY2017": 123636943, "FY2016": 348234204,
        "FY2015": -127514157, "FY2014": 220884050,
        "FY2013": -6069497, "FY2012": 20200747}),
    ("DATA", "Cash and cash equivalents as at 1 January", {"FY2025": 480233340, "FY2024": 276069567, "FY2023": 629660723, "FY2022": 882609330, "FY2021": 787588384,
        "FY2020": 572254591, "FY2019": 710130745, "FY2018": 763285083, "FY2017": 639648140, "FY2016": 291413936,
        "FY2015": 418928093, "FY2014": 198044043,
        "FY2013": 125827641, "FY2012": 105626894}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents (as reported, USD)", {"FY2025": 15724105, "FY2024": -3075636}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 428080578, "FY2024": 480233340, "FY2023": 276069567, "FY2022": 629660723, "FY2021": 882609330,
        "FY2020": 787588384, "FY2019": 572254591, "FY2018": 710130745, "FY2017": 763285083, "FY2016": 639648140,
        "FY2015": 291413936, "FY2014": 418928093,
        "FY2013": 119758144, "FY2012": 125827641}),
]

# convert: SECTION rows pass through unchanged; opening-cash uses opening_cash2()
# (prior year's spot rate); closing cash uses stock2() (this year's spot rate) since
# it's a point-in-time balance, NOT a flow; everything else (DATA/TOTAL) uses flow2().
# (FY2012/FY2013 are native £ - see NATIVE_GBP_YEARS - so *2 pass those years through unconverted.)
_usd_by_label = {label: usd for _, label, usd in rows_usd}
rows = []
for kind, label, usd in rows_usd:
    if kind == "SECTION":
        rows.append((kind, label, {}))
    elif label == "Cash and cash equivalents as at 1 January":
        rows.append((kind, label, opening_cash2(usd)))
    elif label == "Cash and cash equivalents at 31 December":
        rows.append((kind, label, stock2(usd)))
    else:
        rows.append((kind, label, flow2(usd)))
    if label == "Effect of exchange rate changes on cash and cash equivalents (as reported, USD)":
        # £ translation plug (see FX_NOTE): stocks (opening/closing) and flows
        # (everything else) are converted at different rates, so the £ statement
        # needs an explicit reconciling line to tie exactly. Computed programmatically
        # as closing(£) - opening(£) - net change(£) - reported FX-effect(£), per year,
        # rather than hardcoded, so it can never drift out of sync with the rates above.
        opening_gbp = opening_cash2(_usd_by_label["Cash and cash equivalents as at 1 January"])
        closing_gbp = stock2(_usd_by_label["Cash and cash equivalents at 31 December"])
        net_change_gbp = flow2(_usd_by_label["Net (decrease)/increase of cash and cash equivalents"])
        fx_gbp = flow2(usd)
        plug = {
            y: round(closing_gbp[y] - opening_gbp[y] - net_change_gbp[y] - fx_gbp.get(y, 0), 1)
            for y in closing_gbp
        }
        rows.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", plug))

bw.add_cash_flow_sheet(
    title="Zenith Bank (UK) Limited — Statement of Cash Flows",
    subtitle="£'000 (FY2012-FY2013 native GBP, FY2014 onward converted from USD) - see source note at bottom for "
              "FX methodology and rates used. No FY2009-FY2011 column shown (no Statement of Cash Flows disclosed "
              "those years - see HD-073 extension note).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=520,
    unit_suffix=" (£'000, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality (placed after Cash Flow Statement, before Pillar 3 sheets)
# ---------------------------------------------------------------
aq_rows_usd = [
    ("SECTION", "Loans and advances to customers", {}),
    ("DATA", "Gross exposure", {"FY2025": 651917069, "FY2024": 446909206, "FY2023": 359647626, "FY2022": 320279907, "FY2021": 359441063,
        "FY2020": 163000460, "FY2019": 67668595, "FY2018": 90068028, "FY2017": 154831334, "FY2016": 225727621,
        "FY2015": 375887940, "FY2014": 394374170}),
    ("DATA", "IFRS 9 impairment allowance", {"FY2025": -4755653, "FY2024": -3305951, "FY2023": -6190103, "FY2022": -5077130, "FY2021": -5926489,
        "FY2020": -2192931, "FY2019": -2382003, "FY2018": -5123870}),
    ("DATA", "IAS 39 impairment allowance (pre-IFRS 9)", {"FY2017": -33402223, "FY2016": -26338884, "FY2015": -8338078, "FY2014": 0}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 647161416, "FY2024": 443603255, "FY2023": 353457523, "FY2022": 315202777, "FY2021": 353514574,
        "FY2020": 160807529, "FY2019": 65286592, "FY2018": 84944158, "FY2017": 121429111, "FY2016": 199388737,
        "FY2015": 367549862, "FY2014": 394374170}),
    ("SECTION", "IAS 39 individual/collective allowance split (pre-IFRS 9, FY2016-FY2017 only)", {}),
    ("DATA", "Individual impairment allowance", {"FY2017": -28557874, "FY2016": -25359601}),
    ("DATA", "Collective impairment allowance", {"FY2017": -4844349, "FY2016": -979283}),
    ("SECTION", "IFRS 9 ECL allowance by stage (Loans and advances to customers)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 4099161, "FY2024": 2871738, "FY2023": 5808582, "FY2022": 4303234, "FY2021": 5236789,
        "FY2020": 2157893, "FY2019": 1401300, "FY2018": 86118}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 656492, "FY2024": 434213, "FY2023": 381521, "FY2022": 773896, "FY2021": 689700,
        "FY2020": 35038, "FY2019": 980703, "FY2018": 5037752}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired/default)", {"FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0,
        "FY2020": 0, "FY2019": 0, "FY2018": 0}),
    ("TOTAL", "Total ECL allowance", {"FY2025": 4755653, "FY2024": 3305951, "FY2023": 6190103, "FY2022": 5077130, "FY2021": 5926489,
        "FY2020": 2192931, "FY2019": 2382003, "FY2018": 5123870}),
]
aq_rows = [(k, l, stock(v)) if k != "SECTION" else (k, l, {}) for k, l, v in aq_rows_usd]
aq_rows.insert(5, ("DATA", "Impairment as % of gross exposure", {"FY2025": "0.7%", "FY2024": "0.7%", "FY2023": "1.7%", "FY2022": "1.6%", "FY2021": "1.6%",
    "FY2020": "1.3%", "FY2019": "3.5%", "FY2018": "5.7%", "FY2017": "21.6%", "FY2016": "11.7%",
    "FY2015": "2.2%", "FY2014": "0.0%"}))

bw.add_asset_quality_sheet(
    title="Zenith Bank (UK) Limited — Asset Quality",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=aq_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=460,
    unit_suffix=" (£'000, conv. from USD)",
    years=PILLAR3_YEARS,
)

KM1_SOURCES = (
    "Sources — Zenith Bank (UK) Limited's own Key Metrics / UK KM1 tables; amounts are US$ thousands as "
    "printed and have not been converted to GBP:\n"
    f"FY2025: 2025 Pillar 3, printed p.16 — {P3_2025_URL}\n"
    f"FY2024: 2024 Pillar 3, printed p.17 — {P3_2024_URL}\n"
    f"FY2023: 2023 Pillar 3, printed p.17 — {P3_2023_URL}\n"
    f"FY2022: 2022 Pillar 3, printed p.24 — {P3_2022_URL}\n"
    f"FY2021: 2021 Pillar 3, printed p.23 — {P3_2021_URL}\n"
    f"FY2020: 2021 Pillar 3 comparative column, printed p.23 — {P3_2021_URL}\n\n"
    "Each FY2021-FY2025 value comes from that year's own edition, retaining revisions rather than replacing "
    "them with later comparative figures. FY2020 uses the first later-edition comparative that prints the full "
    "row set. The table has no printed row numbers, so none are invented here. FY2021's own table predates the "
    "UK NSFR requirement and explicitly says NSFR would be shown from 1 January 2022; its NSFR cells and all "
    "pre-FY2020 columns therefore remain blank. The Bank's live Pillar 3 page was checked on 17 September 2026 "
    "and FY2025 remains the newest listed annual edition."
)

km1_rows = [
    ("SECTION", "Available own funds (US$)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) capital (US$ k)", {"FY2025": 431376, "FY2024": 378325, "FY2023": 338086, "FY2022": 290721, "FY2021": 281088, "FY2020": 280619}),
    ("DATA", "Tier 1 capital (US$ k)", {"FY2025": 431376, "FY2024": 378325, "FY2023": 338086, "FY2022": 290721, "FY2021": 281088, "FY2020": 280619}),
    ("DATA", "Total capital (US$ k)", {"FY2025": 431376, "FY2024": 378325, "FY2023": 338086, "FY2022": 290721, "FY2021": 281088, "FY2020": 280619}),
    ("SECTION", "Risk-weighted exposure amount", {}),
    ("DATA", "Total risk-weighted exposure amount (US$ k)", {"FY2025": 1843312, "FY2024": 1475750, "FY2023": 1167888, "FY2022": 1125146, "FY2021": 1352803, "FY2020": 991779}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Common Equity Tier 1 ratio (%)", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%", "FY2020": "28.29%"}),
    ("DATA", "Tier 1 ratio (%)", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%", "FY2020": "28.29%"}),
    ("DATA", "Total capital ratio (%)", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%", "FY2020": "28.29%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Total SREP own funds requirements (%)", {"FY2025": "14.04%", "FY2024": "14.04%", "FY2023": "14.04%", "FY2022": "12.89%", "FY2021": "12.89%", "FY2020": "12.89%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Capital conservation buffer (%)", {"FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%", "FY2020": "2.50%"}),
    ("DATA", "Institution specific countercyclical capital buffer (%)", {"FY2025": "0.56%", "FY2024": "0.43%", "FY2023": "0.47%", "FY2022": "0.16%", "FY2021": "0.00%", "FY2020": "0.00%"}),
    ("DATA", "Combined buffer requirement (%)", {"FY2025": "3.06%", "FY2024": "2.93%", "FY2023": "2.97%", "FY2022": "2.66%", "FY2021": "2.50%", "FY2020": "2.50%"}),
    ("DATA", "Overall capital requirement (%)", {"FY2025": "17.10%", "FY2024": "16.97%", "FY2023": "17.01%", "FY2022": "15.55%", "FY2021": "15.39%", "FY2020": "15.39%"}),
    ("DATA", "CET1 available after the total SREP own funds requirements (%)", {"FY2025": "9.36%", "FY2024": "11.60%", "FY2023": "14.91%", "FY2022": "10.29%", "FY2021": "5.39%", "FY2020": "12.90%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "Total exposure measure excluding claims on central banks (US$ k)", {"FY2025": 3171798, "FY2024": 2987483, "FY2023": 2872422, "FY2022": 3409175, "FY2021": 3219954, "FY2020": 2483697}),
    ("DATA", "Leverage ratio excluding claims on central banks (%)", {"FY2025": "12.08%", "FY2024": "11.25%", "FY2023": "9.76%", "FY2022": "7.32%", "FY2021": "8.36%", "FY2020": "10.68%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "Total high-quality liquid assets (HQLA) (Weighted value) (US$ k)", {"FY2025": 952538, "FY2024": 1013789, "FY2023": 1147653, "FY2022": 1227530, "FY2021": 932821, "FY2020": 782801}),
    ("DATA", "Cash outflows – Total weighted value (US$ k)", {"FY2025": 896970, "FY2024": 714951, "FY2023": 838802, "FY2022": 1075133, "FY2021": 1350918, "FY2020": 719583}),
    ("DATA", "Cash inflows – Total weighted value (US$ k)", {"FY2025": 544428, "FY2024": 408131, "FY2023": 469155, "FY2022": 726923, "FY2021": 1022071, "FY2020": 818015}),
    ("DATA", "Total net cash outflows (adjusted value) (US$ k)", {"FY2025": 352543, "FY2024": 306820, "FY2023": 369648, "FY2022": 374822, "FY2021": 337730, "FY2020": 179896}),
    ("DATA", "Liquidity coverage ratio (%)", {"FY2025": "270.19%", "FY2024": "330.42%", "FY2023": "310%", "FY2022": "343%", "FY2021": "276%", "FY2020": "435%"}),
    ("SECTION", "Net Stable Funding Ratio (NSFR)", {}),
    ("DATA", "Total available stable funding (US$ k)", {"FY2025": 1316936, "FY2024": 1136904, "FY2023": 1066880, "FY2022": 912816}),
    ("DATA", "Total required stable funding (US$ k)", {"FY2025": 948441, "FY2024": 768308, "FY2023": 744377, "FY2022": 735763}),
    ("DATA", "Net Stable Funding Ratio (%)", {"FY2025": "138.85%", "FY2024": "147.98%", "FY2023": "143%", "FY2022": "124%"}),
]

bw.add_km1_sheet(
    title="Zenith Bank (UK) Limited — KM1 Key Metrics",
    subtitle="The Bank's published Key Metrics / UK KM1 table in its own row order and precision. Amounts are native US$ thousands as printed; LCR/NSFR figures are averages where the source says so.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    source_height=285,
    years=PILLAR3_YEARS,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=48, source_height=120,
                         years=PILLAR3_YEARS)


# FY2020 added 2026-09-15 from the FY2021 Pillar 3's own section 10 "Key
# Metrics" table, which carries a complete 31 December 2020 comparative column
# (see FY2020_COMPARATIVE_NOTE). Earlier passes took only the section 11.2 RWA
# split from this document and never opened section 10 or 11.1.
CET1_TIER1_TOTAL_USD = {"FY2025": 431376, "FY2024": 378325, "FY2023": 338086, "FY2022": 290721, "FY2021": 281088,
                         "FY2020": 280619,
                         "FY2015": 188483, "FY2014": 170802}
RWA_USD = {"FY2025": 1843312, "FY2024": 1475750, "FY2023": 1167888, "FY2022": 1125146, "FY2021": 1352803,
           "FY2020": 991779,
           "FY2015": 924650, "FY2014": 765350}
CAPITAL_RATIO = {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%",
                  "FY2020": "28.29%",
                  "FY2015": "20.38%", "FY2014": "22.32%"}

FY2020_COMPARATIVE_NOTE = (
    "FY2020 SOURCE (added 2026-09-15): Zenith Bank (UK) Limited, \"Pillar 3 Disclosures as at 31 December "
    "2021\", section 10 \"Key Metrics\", p.22 - a two-column table headed \"31st December 2021 / 31st December "
    "2020\" that carries a complete FY2020 comparative, and section 11.1 \"Composition of Regulatory Own "
    "Funds\", p.24, which states it shows FY2021 \"with 31st December 2020 added for comparison purposes\". "
    "No separate FY2020 Pillar 3 document was needed or used.\n"
    "WHY THIS WAS MISSED BEFORE: earlier passes read only section 11.2 (the RWA-by-risk-type table, which is "
    "explicitly headed \"for both periods\") and recorded the FY2020 RWA split from it, but never opened "
    "sections 10 or 11.1 of the same PDF - so the capital amounts, all three capital ratios, the leverage "
    "ratio and the LCR sat unread in a document already cited in this script. The sheets' prior claim that "
    "FY2016-FY2020 are blank because \"no Pillar 3 document is recoverable\" was true about DOCUMENTS and "
    "wrong about DATA; it is now narrowed to FY2016-FY2019.\n"
    "INTERNAL CONSISTENCY CHECKS, all passing: the section 10 CET1/Tier 1/Total capital figure of "
    "US$280,619k reconciles exactly to section 11.1's own build-up (CET1 before regulatory adjustments "
    "275,574 + total regulatory adjustments 5,045 = 280,619); the section 10 RWA of US$991,779k equals the "
    "section 11.2 category sum already recorded on the RWA Breakdown sheet (888,907 + 3,617 + 6,955 + 92,300 "
    "= 991,779); and 280,619 / 991,779 = 28.29%, reproducing the printed ratio. The document also states "
    "\"The Bank's entire capital base qualifies as Common Equity Tier 1 capital\" and \"has no Additional "
    "Tier 1 (AT1), Tier 2 or Tier 3 Capital\", so CET1 = Tier 1 = Total capital is the Bank's own statement, "
    "not an inference. It further confirms solo scope: \"The Bank reports as a solo UK institution and has no "
    "consolidation adjustments.\""
)
# 2026-09-15 historical Pillar 3 recovery. FY2009-FY2013 explicit markers - a blank
# cell is indistinguishable from an unresearched gap and gets re-chased forever.
HIST_P3_YEARS = ["FY2013", "FY2012", "FY2011", "FY2010", "FY2009"]
NA_BASEL2 = "Not applicable (Basel II)"
NO_EDITION = "No Pillar 3 edition exists in any archive"


def hist_na(label=NA_BASEL2):
    """Structurally inapplicable across FY2009-FY2013 - the metric did not exist under
    the Basel II / BIPRU regime these years were reported under, so it would be absent
    even from the years whose editions were never located."""
    return {y: label for y in HIST_P3_YEARS}


def hist_nd(fy2011):
    """FY2011's edition survives and either states the figure or demonstrably does not;
    the other four years have no edition at all, which is a different statement."""
    return dict({y: NO_EDITION for y in HIST_P3_YEARS}, FY2011=fy2011)


# FY2011 Basel II / BIPRU capital - NOT FX-converted (this pre-dates the Bank's
# redenomination to USD). Both figures the edition prints are carried; see
# HIST_P3_NOTE for the dating caveat on Regulatory Available Capital.
#
# SCALE: these are the figures the FY2011 edition prints, verbatim, in GBP'000 -
# "Total tier 1 capital 43,631" and "Regulatory Available Capital 40,002" (see
# HIST_P3_NOTE). They now sit on the same £'000 scale as every other cell on these
# metric sheets, and match the sheets' "£'000" label.
#
# HISTORY, so this is not "corrected" back: between being added and the scale fix
# later the same day (2026-09-15) these read 43.6 and 40.0. That was a deliberate
# stopgap - the rest of the sheet was then 1000x understated for its label (the
# defect fixed by stock_k(), see P3_SCALE_FIX_NOTE), and matching the neighbouring
# cells was judged less bad than a mixed-unit defect inside one sheet. With the
# sheet-wide scale now correct, the true source figures are restored.
FY2011_TIER1_ACCOUNTS = {"FY2011": 43631}
FY2011_REG_AVAILABLE = {"FY2011": 40002}


PRE_CRDIV_NOTE = (
    "PRE-CRD IV NOTE (FY2014/FY2015): see the PRE-CRD IV METHODOLOGY NOTE in the Pillar 3 sources above for full "
    "detail - these two figures are the Bank's own 'Regulatory Available Capital' (not its larger undeducted "
    "'Total tier 1 capital per audited accounts' memo figure) divided by a derived Total RWA (each Pillar 1 "
    "capital requirement component divided by 8%, summed). FY2016-FY2020 are blank - no Pillar 3 disclosure "
    "document recoverable for those years (see Pillar 3 sources note)."
)

# ---------------------------------------------------------------
# 2026-09-18 INTERIOR-GAP PASS. Capital figures for FY2012/FY2013 and
# FY2016-FY2019 recovered from the ANNUAL REPORTS' own "Capital Management"
# note - a source family nobody had opened for capital, because every prior
# pass looked only for a Pillar 3 document and concluded "unobtainable".
# ---------------------------------------------------------------
AR_CAPITAL_NOTE = (
    "*** ANNUAL-REPORT CAPITAL RECOVERY, 2026-09-18 - READ THIS BEFORE RE-CHASING FY2012/FY2013 OR "
    "FY2016-FY2019 ***\n"
    "Every prior pass treated FY2016-FY2019 as a closed gap on the reasoning that no Pillar 3 disclosure "
    "document is recoverable for those years. That reasoning was about DOCUMENTS OF ONE KIND. It is still "
    "true (see the archive-status note below - the ladder was re-run in full on 2026-09-18 and every rung "
    "failed again), but it was never a statement about the Bank's CAPITAL DISCLOSURE, because Zenith Bank "
    "(UK) Limited also prints a 'Capital Management' note inside note 25 'Financial risk management' of "
    "EVERY Annual Report, and that note carries a Capital Resources table. Those tables were read on "
    "2026-09-18 and are the source of the FY2012, FY2013, FY2016, FY2017, FY2018 and FY2019 capital rows on "
    "this sheet. NONE of them discloses a risk-weighted exposure amount, which is why Total RWAs and the RWA "
    "Breakdown sheet stay empty of figures for those years.\n"
    "THE ROWS ARE SEPARATE FROM THE CRR/KM1 ROW ABOVE ON PURPOSE. A Pillar 3 UK KM1 'CET1 capital' figure and "
    "an Annual Report 'Capital Resources' figure are not guaranteed to be struck on the same basis, and for "
    "this Bank they demonstrably are not in some years (FY2018's own Annual Report reconciles statutory "
    "capital of US$225,399,559 down to regulatory Tier 1 of US$202,258,835 through an IFRS 9 transition "
    "add-back, an IFRS 9 year-1 deduction, a prudential valuation adjustment and an intangibles deduction). "
    "Splicing either figure onto the KM1 row would create a silent basis break mid-series, so each basis "
    "keeps its own labelled row and no cell is merged across the break.\n"
    "WHAT EACH YEAR'S OWN EDITION ACTUALLY PRINTS (all US$ unless stated):\n"
    f"  FY2016 (Annual Report and Accounts 2016, printed p.34 / PDF p.37 - {AR2016_URL}): a two-line Capital "
    "Resources table, Share capital 136.7 / Retained earnings 56.5 / TOTAL TIER 1 CAPITAL 193.2, printed in "
    "US$ MILLIONS to one decimal. There is no regulatory-deduction reconciliation, no RWA and no ratio in "
    "this edition. The figure carried here is 193,158,399 rather than 193,200,000: that is the same "
    "edition's own share capital (136,701,620) plus its own retained earnings (56,456,779), both printed in "
    "full dollars on its Statement of Financial Position and Statement of Changes in Equity, i.e. exactly "
    "the addition the capital note itself performs at a coarser scale. The FY2017 edition's comparative "
    "column prints the same line as 193,158,399 to the dollar, confirming it.\n"
    f"  FY2017 (Annual Report and Financial Statements 2017, printed p.48 / PDF p.50 - {AR2017_URL}): Share "
    "capital 136,701,620 / Retained earnings 70,085,676 / Total Tier 1 capital 206,787,296. This edition "
    "prints NO post-deduction regulatory figure at all - the FY2017 regulatory Tier 1 of 193,158,399 exists "
    "only as the FY2018 edition's comparative column, and is therefore carried on its own explicitly "
    "comparative-labelled row rather than alongside own-edition figures.\n"
    f"  FY2018 (Annual Report and Financial Statements 2018, printed p.57 / PDF p.59 - {AR2018_URL}): Share "
    "capital 136,701,620 / Reserves (99,803) / Retained earnings 88,797,742 / Total statutory capital "
    "225,399,559; then IFRS 9 transition adjustment 8,861,638, Profit or loss attributable to owners of the "
    "parent (27,509,757), IFRS 9 transition adjustment year 1 impact (1,772,328), value adjustments due to "
    "the requirements for prudential valuation (unaudited) (842,446), other intangible assets before "
    "deduction of deferred tax liabilities (1,877,831) = TOTAL REGULATORY CAPITAL (TIER 1) 202,258,835. The "
    "reconciliation foots exactly.\n"
    f"  FY2019 (Annual Report and Financial Statements 2019, printed p.60 / PDF p.62 - {AR2019_URL}): Share "
    "capital 136,701,620 / Reserves 740,531 / Retained earnings 116,728,430 / Total statutory capital "
    "254,170,581; then IFRS 9 transition adjustment (3,544,655), prudential valuation (649,575), other "
    "intangible assets (2,018,933) and profit for the year (27,930,688) = TOTAL REGULATORY CAPITAL (TIER 1) "
    "EXCLUDING AUDITED PROFIT 220,026,730; the same table then adds the profit back to give TOTAL REGULATORY "
    "CAPITAL (TIER 1) INCLUDING AUDITED PROFIT 247,957,418. BOTH are printed, so both are carried, on "
    "separate rows; neither is preferred silently. (The same table's FY2018 comparative column restates "
    "FY2018 on the including-profit basis as 229,768,592 - recorded here in the note only, since FY2018's "
    "own edition printed no such line.)\n"
    f"  FY2013 (Financial Statements for the year ended 31 December 2013, printed p.39 / PDF p.41 - "
    f"{AR2013_URL}): 'Total capital at 31 December 2013 was GBP 74,509,003 (2012: GBP 66,836,084) ... Total "
    "Regulatory Capital as at 31 December 2013 was GBP 72,342,265 (2012: GBP 62,082,926)', with a Capital "
    "Resources table reading Tier one Capital / Shareholders' Funds 72,342,265 / TOTAL TIER 1 CAPITAL "
    "72,342,265.\n"
    f"  FY2012 (Financial Statements as at 31 December 2012, printed p.38 / PDF p.40 - {AR2012_URL}): the "
    "same note, 'Total capital at 31 December 2012 was GBP 66,836,084 (2011 GBP 43,109,518) ... Total "
    "Regulatory Capital as at 31 December 2012 was GBP 62,082,926 (2011 GBP 40,002,338)', table TOTAL TIER 1 "
    "CAPITAL 62,082,926.\n"
    "FY2012/FY2013 ARE NATIVE GBP AND ARE NOT FX-CONVERTED - they pre-date the Bank's redenomination to USD "
    "(see the FX conversion note on the Cash Flow Statement sheet and NATIVE_GBP_YEARS in the build script), "
    "so they sit on these sheets in GBP'000 exactly as printed, on the same scale as the FY2011 Basel II "
    "rows. Both editions are IMAGE-ONLY SCANS from Companies House (company 05713749) with a zero-character "
    "text layer; they were OCR'd to locate the page and then EVERY FIGURE WAS CONFIRMED VISUALLY against the "
    "page rendered at 260 dpi. No figure here rests on OCR output alone.\n"
    "TWO CORROBORATIONS AND ONE DIVERGENCE, none of them adjusted. (1) The FY2012 edition's 2011 comparative "
    "Total Regulatory Capital of GBP 40,002,338 matches, to the pound, the 'Regulatory Available Capital "
    "40,002' (GBP'000) that the recovered FY2011 Pillar 3 prints - two independent documents agreeing, and "
    "it also resolves the dating caveat recorded against that FY2011 Pillar 3 figure in favour of it being a "
    "genuine 31 December 2011 position rather than a FY2010 one. (2) The FY2012 edition's 2011 comparative "
    "'total capital' of GBP 43,109,518 does NOT match this workbook's FY2011 total equity of GBP 43,624,795 "
    "(taken from FY2011's own report) - a GBP 515,277 gap, consistent with the FY2012 IFRS-conversion "
    "restatement already documented in the HD-073 extension note. Each year keeps its own report's figure; "
    "nothing was reconciled.\n"
    "WHAT IS STILL GENUINELY ABSENT AFTER THIS PASS: no Zenith Bank (UK) Annual Report in any year "
    "FY2012-FY2019 prints a risk-weighted exposure amount, an RWA breakdown, a leverage ratio, an LCR or an "
    "NSFR. Each of those four editions was searched in full text for 'risk weighted', 'risk-weighted', "
    "'RWA', 'leverage', 'liquidity coverage' and 'stable funding'; the only hits are the boilerplate sentence "
    "'a ratio of total regulatory capital to risk-weighted exposures at or above a level determined for each "
    "institution' and narrative liquidity-management prose naming the LCR and NSFR without any figure. Those "
    "cells therefore carry explicit stated-absence markers rather than blanks."
)

# Statutory ('Total capital' / 'Total Tier 1 capital' as the audited accounts strike it,
# before any regulatory deduction), each from that year's OWN edition. Raw whole USD ->
# stock() applies FX and the divide by 1,000.
AR_STATUTORY_CAPITAL_USD = {"FY2019": 254170581, "FY2018": 225399559, "FY2017": 206787296, "FY2016": 193158399}
# Post-deduction regulatory Tier 1, each from that year's OWN edition.
AR_REG_TIER1_USD = {"FY2019": 220026730, "FY2018": 202258835}
# FY2017's post-deduction figure exists ONLY as the FY2018 edition's comparative column.
AR_REG_TIER1_COMPARATIVE_USD = {"FY2017": 193158399}
# The FY2019 edition's own second presentation, adding audited profit back.
AR_REG_TIER1_INCL_PROFIT_USD = {"FY2019": 247957418}
# FY2012/FY2013 are native GBP - NOT FX-converted, already whole pounds -> /1000 only.
AR_GBP_TIER1 = {"FY2013": round(72342265 / 1000, 1), "FY2012": round(62082926 / 1000, 1)}
AR_GBP_STATUTORY = {"FY2013": round(74509003 / 1000, 1), "FY2012": round(66836084 / 1000, 1)}

AR_CAPITAL_ROWS = [
    ("Total statutory capital per the Annual Report 'Capital Management' note, before regulatory deductions "
     "(each year's own edition)", stock(AR_STATUTORY_CAPITAL_USD)),
    ("Total regulatory capital (Tier 1) after regulatory deductions, per the Annual Report 'Capital Management' "
     "note (each year's own edition)", stock(AR_REG_TIER1_USD)),
    ("Total regulatory capital (Tier 1) after deductions - FY2017 COMPARATIVE COLUMN of the FY2018 Annual Report "
     "(FY2017's own edition prints no post-deduction figure)", stock(AR_REG_TIER1_COMPARATIVE_USD)),
    ("Total regulatory capital (Tier 1) INCLUDING audited profit for the year - the FY2019 edition's own second "
     "presentation of the same table", stock(AR_REG_TIER1_INCL_PROFIT_USD)),
    ("Total statutory capital per the Annual Report 'Capital Management' note, Basel II era (native GBP, NOT "
     "FX-converted)", AR_GBP_STATUTORY),
    ("Total Tier 1 / Total Regulatory Capital per the Annual Report 'Capital Management' note, Basel II era "
     "(native GBP, NOT FX-converted)", AR_GBP_TIER1),
]

# Explicit stated-absence markers, so a researched absence is never re-chased as a blank.
# The three archive states are kept distinct (see HIST_P3_NOTE): FY2016/FY2019 editions
# demonstrably existed and are lost; FY2017/FY2018 were apparently never posted.
# GA-020 (2026-09-19): "published but lost" is a limit on OUR reach, so it now carries the
# reserved "Unreached today" phrase. Re-tried today: both named PDFs (media/1013/...2016.pdf,
# media/2177/...2019.pdf, plus the old /uploads/ 2016 path) return HTTP 404 text/html while the
# FY2025 edition on the same host returns 200 application/pdf (positive control); a Wayback CDX
# pdf sweep of zenith-bank.co.uk lists the 2008/2011/2014/2015/2021-2024 editions and neither of
# these. The year's Annual Report (read in full 2026-09-18) prints no such figure. Companies
# House holds only the accounts, not the Pillar 3.
# GA-020 second pass (2026-09-19) added routes, all negative: archive.ph (newest) for all four
# URL forms of the two PDFs -> 404; Wayback CDX matchType=domain WITHOUT the mimetype filter on
# zenith-bank.co.uk, zenithbank.co.uk, zenith-bank.com and zenithbank.com -> no capture of either
# file (media/1013 and media/2177 never captured); the NEXT year's Annual Report (FY2017 for
# FY2016, FY2020 for FY2019) read for a comparative ratio/RWA/leverage/LCR/MREL -> none (FY2020's
# prints only the 2019 CET1 capital AMOUNT, 260,687,679); parent Zenith Bank Plc's Dec-2016 and
# Dec-2019 Pillar 3s (zenithbank.com media/2117 and media/3149): live 403 (a block, not a negative),
# Wayback captures truncated at 1 MiB, and the readable part names Zenith Bank (UK) only as a
# subsidiary with no entity-level capital table - and under the tightened brief a parent figure may
# be used only if printed as a separate labelled UK-entity disclosure, which none is; web search
# for the titles returns only FY2023/FY2024 UK editions and the parent's reports.
def _p3_lost(y):
    # cdn-sweep (2026-09-19): only FY2019 is still lost; FY2016 was recovered (see Z16_* below).
    assert y == "FY2019", y
    return ("Unreached today – FY2019 Pillar 3 named on archived index page; PDF 404 live; no copy in "
            "Wayback, archive.ph, Common Crawl (74 crawls) or the Azure origin host (2026-09-19); "
            "FY2019/FY2020 ARs print none")
# GA-020 cdn-sweep (2026-09-19): the FY2016 edition WAS recovered - Common Crawl captured it at its
# pre-2018 address http://www.zenith-bank.co.uk/uploads/ZBL_Pillar_3_Disclosure_Document_2016.pdf on
# 2018-02-24 (CC-MAIN-2018-09). Read on page images; see Z16_SOURCE_NOTE. It is the same pre-CRD IV
# Pillar 1/Pillar 2 format as FY2014/FY2015, so it prints NONE of these metrics.
Z16_DOC = "FY2016 Pillar 3 (recovered via Common Crawl, 17pp)"
Z16_RATIO = ("Not published – FY2016 AR prints no ratio; recovered FY2016 Pillar 3 p.9-10 prints only a 365% "
             "'Solvency Ratio against Pillar 1' (capital/requirement), no CET1 ratio")
Z16_RWA = ("Not published – " + Z16_DOC + " p.9-10 prints Pillar 1 capital requirements (total "
           "US$52,940k), not risk-weighted amounts; nothing derived")
Z16_LEV = "Not published – " + Z16_DOC + " prints no leverage ratio (capital section p.8-11 read)"
Z16_LCR = ("Not published – " + Z16_DOC + " names LCR only as a PRA standard it maintains (p.8, "
           "s.3.3.1); no LCR figure")
Z16_MREL = "Not published – " + Z16_DOC + " has no MREL or eligible-liabilities figure"
Z16_SOURCE_NOTE = (
    "FY2016 PILLAR 3 RECOVERED (GA-020 cdn-sweep, 2026-09-19) - this supersedes the FY2016 half of the "
    "'unobtainable' paragraph above. The Bank's pre-2018 site served files from /uploads/, and Common Crawl "
    "captured http://www.zenith-bank.co.uk/uploads/ZBL_Pillar_3_Disclosure_Document_2016.pdf on 2018-02-24 "
    "(crawl CC-MAIN-2018-09; WARC crawl-data/CC-MAIN-2018-09/segments/1518891815318.53/warc/"
    "CC-MAIN-20180224033332-20180224053332-00132.warc.gz, offset 592640953, length 648238; retrieve with an "
    "HTTP Range request against https://data.commoncrawl.org/). HTTP 200 application/pdf, Last-Modified "
    "2018-01-02, 713,641 bytes = the stated Content-Length, %PDF ... %%EOF, 17 pages; title page 'ZENITH BANK "
    "(UK) LIMITED - PILLAR 3 DISCLOSURES FOR THE YEAR ENDED 31 DECEMBER 2016'. Read on the page images: p.8 "
    "s.3.3.1 names 'LCR, NSFR, Funding concentration' only as PRA standards the Bank maintains, with no figure; "
    "p.9 s.4.2 Total CET-1 capital US$192,990k (2015: 190,521) and s.4.3.1 Pillar 1 capital requirements "
    "Credit 47,135 / Market 633 / Operational 5,172 / Total 52,940 (US$000), Regulatory Available Capital "
    "192,990; p.10 'Solvency Ratio against Pillar 1 (Available capital / Required capital)' 365% (2015: 258%) "
    "and the credit-risk capital requirement (8%) by exposure class; p.11 Pillar 2A allocation, total 94,675. "
    "It is the same pre-CRD IV Pillar 1/Pillar 2 format as FY2014/FY2015: no CET1/capital ratio, no "
    "risk-weighted amount, no leverage ratio, no LCR/NSFR figure and no MREL anywhere in its 17 pages (text "
    "layer on every page; the only image is the p.1 logo). So the FY2016 ratio, RWA, leverage, LCR and MREL "
    "cells read 'Not published' from the edition itself. The RWA is NOT derived from the requirements by "
    "dividing by 8%, following the FY2011 treatment (the FY2014/FY2015 derivation stays flagged, not "
    "extended). The 365% cover multiple is NOT a capital ratio (see the Tier 1 Ratio note). The capital "
    "AMOUNT (US$192,990k) is not written anywhere by this pass: the capital sheets' FY2016 cells come from "
    "the Annual Report and were not in this pass's scope - a later pass may cross-check them against it. "
    "FY2019 remains unreached: its media/2177 file was never captured by Wayback or by any of 74 Common Crawl "
    "crawls (2016-2023) of zenith-bank.co.uk/media/*, and the Azure origin zenithbank-uk.azurewebsites.net "
    "301s to the same 404."
)
P3_LOST = None  # retained name; per-year text is built by _p3_lost()
P3_ABSENT = "Not disclosed (no Pillar 3 located; Annual Report prints none)"
NO_P3_1619 = {"FY2019": _p3_lost("FY2019"), "FY2018": P3_ABSENT, "FY2017": P3_ABSENT}
# GA-020 (2026-09-19): the FY2011 Basel II edition survives and was read (see notes on the
# Tier 1 Ratio / Total RWAs sheets); what it lacks is recorded as NOT PUBLISHED, with the reason.
FY2011_NO_RATIO = ("Not published – FY2011 Pillar 3 (Basel II) prints no capital ratio; its 203% "
                   "'Solvency Ratio against Pillar 1' is capital/requirement, not a ratio - see note")
FY2011_NO_RWA = ("Not published – FY2011 Pillar 3 (Basel II) prints Pillar 1 capital requirements "
                 "(total GBP 19,686k), not risk-weighted amounts; nothing derived - see note")
PRE_CRDIV_ABSENT = {"FY2015": "Not disclosed (pre-CRD IV edition prints no such metric)",
                    "FY2014": "Not disclosed (pre-CRD IV edition prints no such metric)"}

BASEL2_CAPITAL_ROWS = [
    ("Total Tier 1 capital per audited accounts, Basel II / GENPRU 2.2 basis (native GBP, NOT FX-converted)", FY2011_TIER1_ACCOUNTS),
    ("Regulatory Available Capital, Basel II basis, post regulatory deductions (native GBP, NOT FX-converted)", FY2011_REG_AVAILABLE),
]
HIST_CAPITAL_NOTE = (
    "FY2011 ADDED 2026-09-15 on its own two rows, not on the row above. The recovered FY2011 Pillar 3 is a "
    "Basel II / BIPRU document computed under GENPRU 2.2 - a different capital definition from the CRR/CRD IV "
    "series, and reported in native GBP rather than the USD that every FY2014+ figure on this sheet is converted "
    "from. It is therefore NOT continuous with the row above and is deliberately not spliced onto it. The Bank's "
    "own words: 'The Bank's entire capital base is Tier 1 capital which consists of fully issued ordinary shares "
    "satisfying all the criteria for a Tier 1 instrument (as outlined in GENPRU 2.2.83 R) and audited reserves' - "
    "so the absence of AT1 and Tier 2 in FY2011 is the Bank's statement, not an inference. Both figures the "
    "edition prints are carried, with a dating caveat on the second; see the source note below. The source "
    "figures are GBP 43,631k and GBP 40,002k and they appear here exactly as printed, in £'000, on the same scale "
    "as the CRR-basis row above. (They briefly read 43.6/40.0 earlier on 2026-09-15, while the sheet-wide "
    "unit-scale defect described in the source note below still stood; that defect is now fixed.)\n"
    "FY2009/FY2010/FY2012/FY2013 read 'No Pillar 3 edition exists in any archive' rather than being left blank, "
    "so the distinction between 'searched and genuinely absent' and 'never looked at' survives in the sheet "
    "itself. See the source note for how that differs from FY2016/FY2019 (published but lost) and "
    "FY2017/FY2018/FY2020 (apparently never posted).\n\n"
)

AR_RATIO_ROW_NOTE = (
    "THE ANNUAL-REPORT RATIO ROW (FY2017/FY2018, added 2026-09-18) IS A SEPARATE ROW FOR A REASON. Neither "
    "figure comes from a Pillar 3 UK KM1 template - no Pillar 3 edition survives for either year (see the "
    "Annual-Report capital recovery note below). FY2018's 32.38% is stated in the Strategic Report of the "
    f"FY2018 Annual Report, printed p.8 / PDF p.10 ({AR2018_URL}): 'The Bank's strong capital position at the "
    "end of 2018, which reflects a Common Equity Tier 1 (CET1) ratio of 32.38%'. FY2017's 35.53% is stated in "
    f"the Strategic Report of the FY2017 Annual Report, printed p.11 / PDF p.13 ({AR2017_URL}), in an 'IFRS 9 "
    "implications' passage that gives three figures for the same transition - '35.53% under IAS 39 at 31 "
    "December 2017 / 34.40% under IFRS 9 at 1 January 2018 before transitional relief / 35.47% under IFRS 9 at "
    "1 January 2018 after transitional relief'. ONLY THE FIRST IS A 31 DECEMBER 2017 POSITION; the other two "
    "are 1 January 2018 opening positions and belong to no year column here, so they are recorded in this note "
    "and nowhere else. The Bank's entire capital base is CET1 (its own statement - no AT1, no Tier 2), so the "
    "same figure is the Tier 1 ratio and the Total capital ratio, exactly as for every year sourced from a KM1 "
    "template on these sheets.\n"
    "A TRAJECTORY ODDITY, FLAGGED AND DELIBERATELY NOT RESOLVED: 35.53% (FY2017) and 32.38% (FY2018) sit well "
    "above the 20.38% recorded for FY2015 and the 28.29% for FY2020, and neither the FY2017 nor the FY2018 "
    "Annual Report prints the RWA that would explain the movement. Nothing has been back-solved from capital "
    "and ratio to produce one - that is barred by this project's rules and would in any case be a derivation "
    "presented as a disclosure. The ratios are carried as printed; the RWA cells stay stated-absent.\n"
    "FY2016 and FY2019 get no ratio at all: those two Annual Reports print a Capital Resources table but no "
    "capital ratio anywhere. FY2016's Pillar 3 was recovered on 2026-09-19 (see the Z16 note in the source "
    "cell) and prints no capital ratio either - only a 365% capital-cover multiple - so FY2016 is 'Not "
    "published'; FY2019's Pillar 3 demonstrably existed and is still lost, so FY2019 is 'Unreached today'."
)
AR_RATIO = {"FY2018": "32.38%", "FY2017": "35.53%"}
AR_RATIO_LABEL = ("Common Equity Tier 1 (CET1) ratio as stated in that year's own ANNUAL REPORT "
                  "(not from a Pillar 3 / UK KM1 template)")

metric("CET1 Capital", "£'000 (conv. from USD)",
       [("Common Equity Tier 1 (CET1) capital", dict(stock_k(CET1_TIER1_TOTAL_USD), **hist_na()))] + AR_CAPITAL_ROWS[:4],
       p3_sources(),
       note="FY2009-FY2013 'Not applicable (Basel II)': the CET1 concept is a CRD IV construct and does not exist in the recovered FY2011 Basel II edition, which discloses a single undifferentiated Tier 1 capital figure (carried on the Tier 1 Capital and Total Capital sheets). The FY2012/FY2013 Basel II Annual Report capital rows are for the same reason carried on the Tier 1 Capital and Total Capital sheets only, not here.\n\n"
            + AR_CAPITAL_NOTE + "\n\n" + PRE_CRDIV_NOTE)
metric("CET1 Ratio", "% of RWA",
       [("Common Equity Tier 1 (CET1) ratio", dict(CAPITAL_RATIO, **hist_na())),
        (AR_RATIO_LABEL, dict(AR_RATIO, FY2019=_p3_lost("FY2019"), FY2016=Z16_RATIO))],
       p3_sources(),
       note="FY2009-FY2013 'Not applicable (Basel II)' - no CET1 concept existed (see CET1 Capital sheet).\n\n"
            + AR_RATIO_ROW_NOTE + "\n\n" + AR_CAPITAL_NOTE + "\n\n" + PRE_CRDIV_NOTE)
metric("Tier 1 Capital", "£'000 (conv. from USD)", [("Tier 1 capital (CRR/CRD IV basis)", stock_k(CET1_TIER1_TOTAL_USD))] + BASEL2_CAPITAL_ROWS + AR_CAPITAL_ROWS, p3_sources(),
       note=HIST_CAPITAL_NOTE + "Equal to CET1 capital in every year - the Bank holds no Additional Tier 1 (AT1) instruments.\n\n" + AR_CAPITAL_NOTE + "\n\n" + PRE_CRDIV_NOTE)
metric("Tier 1 Ratio", "% of RWA",
       [("Tier 1 ratio", dict(CAPITAL_RATIO, **hist_nd(FY2011_NO_RATIO))),
        (AR_RATIO_LABEL.replace("Common Equity Tier 1 (CET1) ratio", "Tier 1 ratio (= the CET1 ratio; no AT1 in issue)"),
         dict(AR_RATIO, FY2019=_p3_lost("FY2019"), FY2016=Z16_RATIO))],
       p3_sources(),
       note="FY2011 'Not publicly disclosed': the recovered FY2011 edition states no capital/RWA ratio at all. It DOES print a 'Solvency Ratio against Pillar 1' of 203%, but that is capital divided by the capital REQUIREMENT - a capital-cover multiple, roughly 12.5x a true capital ratio - and putting it here would overstate the Bank's capitalisation by an order of magnitude. See the source note. Nothing is back-solved from the capital and capital-requirement figures either.\n\n"
            + AR_RATIO_ROW_NOTE + "\n\n" + AR_CAPITAL_NOTE + "\n\n" + PRE_CRDIV_NOTE)
metric("Total Capital", "£'000 (conv. from USD)", [("Total capital (CRR/CRD IV basis)", stock_k(CET1_TIER1_TOTAL_USD))] + BASEL2_CAPITAL_ROWS + AR_CAPITAL_ROWS, p3_sources(),
       note=HIST_CAPITAL_NOTE + "Equal to CET1/Tier 1 capital in every year - the Bank holds no AT1 or Tier 2 instruments.\n\n" + AR_CAPITAL_NOTE + "\n\n" + PRE_CRDIV_NOTE)
metric("Total Capital Ratio", "% of RWA",
       [("Total capital ratio", dict(CAPITAL_RATIO, **hist_nd(FY2011_NO_RATIO))),
        (AR_RATIO_LABEL.replace("Common Equity Tier 1 (CET1) ratio", "Total capital ratio (= the CET1 ratio; no AT1 or Tier 2 in issue)"),
         dict(AR_RATIO, FY2019=_p3_lost("FY2019"), FY2016=Z16_RATIO))],
       p3_sources(),
       note="FY2011 'Not publicly disclosed' - see the Tier 1 Ratio sheet's note on the 203% capital-cover trap.\n\n"
            + AR_RATIO_ROW_NOTE + "\n\n" + AR_CAPITAL_NOTE + "\n\n" + PRE_CRDIV_NOTE)
metric("Total RWAs", "£'000 (conv. from USD)", [("Total risk-weighted exposure amount", dict(stock_k(RWA_USD), **dict(hist_nd(FY2011_NO_RWA), FY2016=Z16_RWA, **NO_P3_1619)))], p3_sources(),
       note="FY2011 'Not publicly disclosed' (2026-09-15): the recovered FY2011 Basel II edition discloses Pillar 1 capital "
            "REQUIREMENTS (Credit 18,156 / Market 27 / Operational 1,503 / Total 19,686, GBP'000), not risk-weighted amounts. "
            "Dividing those by 8% would give a total RWA of 246,075, but that is a derivation and this project transcribes only "
            "what a document states directly, so the cell is left as a stated absence and the requirement figures are preserved "
            "verbatim in the source note. NOTE THE INCONSISTENCY THIS EXPOSES: the FY2014/FY2015 figures on this very row WERE "
            "produced by exactly that division in an earlier pass. That pre-existing derivation was not removed here (withdrawing "
            "populated data is not this pass's decision) but it is flagged, and it was not propagated backwards.\n\n"
            "FY2023's figure (own report, the £'000 equivalent of $1,167,888k) differs from the FY2024 report's restated FY2023 "
            "comparative ($1,203,364k) - a Basic Indicator Approach operational-risk methodology update. FY2023's own "
            "report figure is used, consistent with this project's convention of preferring each year's own report.\n\n"
            "FY2016-FY2019 CHANGED FROM BLANK TO AN EXPLICIT STATED ABSENCE 2026-09-18, and the wording distinguishes "
            "two different situations rather than flattening them. All four years' Annual Reports were read in full on "
            "that date (the capital rows on the CET1/Tier 1/Total Capital sheets come from them) and NONE of the four "
            "prints a risk-weighted exposure amount - each was searched for 'risk weighted', 'risk-weighted' and 'RWA' "
            "and the only hit is the boilerplate 'a ratio of total regulatory capital to risk-weighted exposures at or "
            "above a level determined for each institution'. On top of that, FY2016 and FY2019 had a Pillar 3 edition "
            "that demonstrably existed and is lost (named on archived index pages, 404 live, never crawled), whereas "
            "FY2017 and FY2018 have no evidence of an edition ever being posted. NOTHING WAS BACK-SOLVED: FY2017's and "
            "FY2018's own CET1 ratios (35.53%, 32.38%) and their capital figures are both now on this workbook, and "
            "dividing one by the other would produce an RWA - that is a derivation, it is barred here, and it was not "
            "done.\n\n"
            + AR_CAPITAL_NOTE + "\n\n" + PRE_CRDIV_NOTE)

rwa_rows_usd = [
    ("SECTION", "Template UK OV1 'Overview of risk weighted exposure amounts' — each year's own Pillar 3 report (FY2025-FY2020)", {}),
    ("DATA", "Credit Risk (excluding CCR)", {"FY2025": 1646471, "FY2024": 1205520, "FY2023": 1003271, "FY2022": 939921, "FY2021": 1242586,
        "FY2020": 888907}),
    ("DATA", "Counterparty Credit Risk (CCR)", {"FY2025": 6886, "FY2024": 98068, "FY2023": 54106, "FY2022": 79324}),
    ("DATA", "of which: Credit Valuation Adjustment (CVA)", {"FY2025": 1085, "FY2024": 1392, "FY2023": 1301, "FY2022": 1025, "FY2021": 4500,
        "FY2020": 3617}),
    ("DATA", "Settlement Risk", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0}),
    ("DATA", "Market Risk (FX and commodities)", {"FY2025": 5073, "FY2024": 4202, "FY2023": 3869, "FY2022": 11250, "FY2021": 7485,
        "FY2020": 6955}),
    ("DATA", "Operational Risk", {"FY2025": 184881, "FY2024": 167960, "FY2023": 106641, "FY2022": 94651, "FY2021": 98232,
        "FY2020": 92300}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 1843312, "FY2024": 1475750, "FY2023": 1167888, "FY2022": 1125146, "FY2021": 1352803,
        "FY2020": 991779}),
    ("DATA", "Memo: amounts below thresholds for deduction (already included within Credit Risk above)", {"FY2025": 0, "FY2024": 1024}),
    ("SECTION", "DERIVED from each year's own disclosed Pillar 1 CAPITAL requirement divided by 8% (FY2015-FY2014). These two years pre-date the UK OV1 template entirely, so the figures above are not disclosed as risk-weighted amounts by the Bank; no counterparty-credit-risk, CVA or settlement-risk line exists in the source for either year, which is why those rows are absent here rather than zero", {}),
    ("DATA", "Credit Risk (excluding CCR)", {"FY2015": 859575, "FY2014": 710200}),
    ("DATA", "Market Risk (FX and commodities)", {"FY2015": 5638, "FY2014": 1613}),
    ("DATA", "Operational Risk", {"FY2015": 59438, "FY2014": 53538}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2015": 924650, "FY2014": 765350}),
]
# FY2016-FY2019 stated-absence marker row (2026-09-18). Placed outside rwa_rows_usd so it
# is NOT passed through stock_k() - these are text cells, and it is NOT a DATA/TOTAL row,
# so it plays no part in the block reconciliation the verifier runs on this sheet.
RWA_ABSENCE_ROWS = [
    ("SECTION", "FY2016-FY2019 - STATED ABSENCE, added 2026-09-18. Each of those four Annual Reports was read in "
                "full that day; every one prints a Capital Resources table (now on the capital sheets) and NONE "
                "prints a risk-weighted exposure amount or any RWA split. Nothing is back-solved from the FY2017 "
                "/ FY2018 capital and ratio figures - see the note below", {}),
    ("DATA", "Total risk-weighted exposure amount", dict(NO_P3_1619, FY2016=Z16_RWA)),
]
bw.add_rwa_breakdown_sheet(
    title="Zenith Bank (UK) Limited — RWA Breakdown (UK OV1)",
    subtitle="£'000, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=[(k, l, stock_k(v)) for k, l, v in rwa_rows_usd] + RWA_ABSENCE_ROWS,
    sources_text=p3_sources()
        + "\n\nUK OV1 template (Overview of risk weighted exposure amounts). Each year's own Pillar 3 report is "
          "used. FY2024's own report splits Credit Risk (excl. CCR) $1,205,520k / CCR $98,068k, while the FY2025 "
          "report's restated FY2024 comparative shows a different split ($1,280,947k / $22,641k) - same total "
          "($1,475,750k) either way; a reclassification between the two lines, not a change to overall RWAs. "
          "FY2021's own report pre-dates the UK OV1 template's current form: it combines most Counterparty Credit "
          "Risk into the 'Credit Risk' line (footnoted in the source as immaterial, <1% of Credit Risk) while "
          "still separately disclosing CVA - so FY2021's CCR row is blank (not zero) and its Credit Risk row "
          "includes that CCR. FY2023's total ($1,167,888k) is $1k off the sum of its own visible rows due to "
          "source-side rounding of each row to the nearest $1k - not a plug. Settlement Risk is nil (explicitly "
          "disclosed, immaterial) in every year. The 'amounts below thresholds for deduction' memo line (FY2024 "
          "only, $1,024k) is explicitly excluded from the Total per the source's own footnote (already counted "
          "within Credit Risk) - not additive.\n\n"
          "FY2014/FY2015 pre-date the UK OV1 template entirely (see PRE-CRD IV METHODOLOGY NOTE above) - rows are "
          "DERIVED by dividing each year's own disclosed Pillar 1 capital requirement per risk category by 8% "
          "(the standard Basel capital-to-RWA ratio), not directly disclosed as risk-weighted amounts. No CCR/CVA "
          "breakout or Settlement Risk line exists in the source for these two years (blank, not zero - the "
          "source's Credit Risk capital requirement may include an immaterial counterparty risk component not "
          "separately identifiable).\n\n"
          "FY2020 RECOVERED 2026-09-15 from the FY2021 report's own COMPARATIVE COLUMN, not from a FY2020 "
          f"document (none exists - see the Pillar 3 sources note). {P3_2021_URL}, section 11.2 'Overview of risk "
          "weighted exposure and own funds requirements', p.25: that table is explicitly headed 'the risk "
          "weighted exposures by risk type under Pillar 1 for BOTH PERIODS' and carries a full '31st December "
          "2020' column alongside 31st December 2021 - Credit Risk 888,907k / CVA 3,617k / Settlement Risk nil / "
          "Market risk 6,955k / Operational Risk 92,300k / Total 991,779k (US$). Validated three ways: the five "
          "components sum to exactly the printed total of 991,779k with no rounding residual; the same table's "
          "FY2021 column reproduces this sheet's existing FY2021 figures exactly, line for line; and FY2020 "
          "follows FY2021's own taxonomy, so the CCR row is left BLANK (not zero) and CVA is shown separately, "
          "exactly as for FY2021, per the source's footnote that other CCR is under 1% of Credit Risk and is "
          "therefore folded into the Credit Risk line. Note this means FY2020's Credit Risk row, like FY2021's, "
          "includes an immaterial unseparated CCR component. Converted to GBP at the FY2020 period-end spot rate "
          "per the FX methodology above.\n\n"
          "FY2016-FY2019 remain blank - no Pillar 3 disclosure document is recoverable for those years, and no "
          "surviving document's comparative column reaches them (the FY2021 report is the earliest modern "
          "edition, and its comparative reaches only FY2020; see Pillar 3 sources note above for the search "
          "performed).\n\n"
          "FY2009-FY2013 COLUMNS (added 2026-09-15) ARE BLANK ON PURPOSE, AND NO RWA WAS DERIVED FOR THEM. The "
          "recovered FY2011 Pillar 3 edition discloses Pillar 1 CAPITAL REQUIREMENTS, not risk-weighted amounts: "
          "Credit Risk 18,156 / Market Risk 27 / Operational Risk 1,503 / Total 19,686 (GBP'000, native, not "
          "FX-converted), with credit risk further split by exposure class as Financial Institutions 5,768, "
          "Corporates 7,461, Retail 25, Bonds 3,899, Sovereigns 896, Multilateral Development Banks 0 and Fixed "
          "and other assets 107. Every one of those is 8% of the corresponding risk weighted exposure amount by "
          "the source's own definition, so each could be grossed up - and that is exactly what an earlier pass "
          "did to produce the FY2014/FY2015 rows on this sheet. It was NOT done here, because grossing up is a "
          "derivation and this project's standing rule is to transcribe only what a document states directly. "
          "The requirement figures are preserved verbatim in this note instead, which loses nothing. This does "
          "leave FY2014/FY2015 on a derived basis and FY2011 on a stated-absence basis on the same sheet; that "
          "inconsistency is flagged rather than resolved by adding a second derivation. FY2009, FY2010, FY2012 "
          "and FY2013 have no Pillar 3 edition in any archive.",
    first_col_width=64,
    source_height=440,
    unit_suffix=" (£'000, conv. from USD)",
    years=PILLAR3_YEARS,
)

metric(
    "Leverage Ratio", "£'000 / % (conv. from USD)",
    [
        ("Total exposure measure excluding claims on central banks", stock_k({"FY2025": 3171798, "FY2024": 2987483, "FY2023": 2872422, "FY2022": 3409175, "FY2021": 3219954, "FY2020": 2483697})),
        ("Leverage ratio excluding claims on central banks (%)", dict({"FY2025": "12.08%", "FY2024": "11.25%", "FY2023": "9.76%", "FY2022": "7.32%", "FY2021": "8.36%", "FY2020": "10.68%"}, **dict(hist_na(), FY2016=Z16_LEV, **NO_P3_1619, **PRE_CRDIV_ABSENT))),
    ],
    p3_sources(),
    note="FY2009-FY2013 'Not applicable (Basel II)' (2026-09-15): the regulatory leverage ratio is a CRD IV "
         "construct with no Basel II counterpart, and the recovered FY2011 edition mentions no leverage ratio "
         "anywhere. Marked structurally inapplicable rather than left blank.\n\n"
         "FY2020 added 2026-09-15 from the FY2021 Pillar 3's section 10 Key Metrics comparative column - same "
         "row label and same 'excluding claims on central banks' basis as the years above it, so this "
         "continues the series without a basis change. The exposure measure (US$2,483,697k) and ratio "
         "(10.68%) are both printed; 280,619 / 2,483,697 = 11.30% on the capital shown, and the Bank's 10.68% "
         "reflects its own tier-1-for-leverage measurement, so the printed figure is carried as disclosed and "
         "nothing is derived.\n\n"
         "FY2014-FY2019 CARRY EXPLICIT STATED-ABSENCE MARKERS AS OF 2026-09-18, replacing blanks. FY2014 and "
         "FY2015: both surviving Pillar 3 editions were re-downloaded and searched on that date, and neither "
         "contains the string 'leverage' anywhere - the CRD IV/UK leverage ratio framework did not apply to a "
         "firm this size then. FY2016-FY2019: no Pillar 3 document is recoverable (the fetch ladder was re-run "
         "in full on 2026-09-18 and every rung failed - see the archive-status note), and each of those four "
         "years' Annual Reports was read that day and mentions no leverage ratio at all. NOTE the prior "
         "version of this note said FY2016-FY2020 - that was corrected once the FY2021 document's comparative "
         "column was read.\n\n"
         + FY2020_COMPARATIVE_NOTE + "\n\n" + AR_CAPITAL_NOTE,
)

metric(
    "LCR", "£'000 / % (conv. from USD)",
    [
        ("Total high-quality liquid assets (HQLA), weighted value", stock_k({"FY2025": 952538, "FY2024": 1013789, "FY2023": 1147653, "FY2022": 1227530, "FY2021": 932821, "FY2020": 782801})),
        ("Total net cash outflows, adjusted value", stock_k({"FY2025": 352543, "FY2024": 306820, "FY2023": 369648, "FY2022": 374822, "FY2021": 337730, "FY2020": 179896})),
        ("Liquidity Coverage Ratio (%) (12-month simple average)", {"FY2025": "270.19%", "FY2024": "330.42%", "FY2023": "310%", "FY2022": "343%"}),
        ("Liquidity Coverage Ratio (%) (point-in-time at year-end)", dict({"FY2021": "276%", "FY2020": "435%"},
            **dict(hist_na("Not applicable (pre-LCR regime)"), FY2016=Z16_LCR, **NO_P3_1619, **PRE_CRDIV_ABSENT))),
    ],
    p3_sources(),
    note="FY2009-FY2013 'Not applicable (pre-LCR regime)' (2026-09-15): the LCR was not a UK requirement in those "
         "years - the recovered FY2011 Basel II edition manages liquidity under the pre-LCR ILAA/BIPRU regime and "
         "discloses no quantitative liquidity metric at all. The marker is placed on the point-in-time row purely "
         "because that is the row FY2020/FY2021 use; it applies to the metric as a whole, not to one basis. "
         "Marked structurally inapplicable rather than left blank.\n\n"
         "TWO DIFFERENT BASES, deliberately kept on separate rows (2026-09-15). FY2021 is a point-in-time "
         "(year-end) figure as originally disclosed; FY2022 onward is a 12-month simple average, per each year's "
         "own report. They are NOT comparable, so FY2021 is shown on its own row rather than continuing the "
         "average row with a different-basis number - an earlier revision of this workbook carried all five years "
         "in a single row, which implied a like-for-like 276% -> 343% move that the sources do not support. The "
         "HQLA and net-cash-outflow rows above carry the same vintage split (FY2021 point-in-time, FY2022 onward "
         "averaged) and are left as single rows, following the same convention used for Access Bank. FY2022's own "
         "report (374,822k/343%) differs from the FY2023 report's restated FY2022 comparative (348,210k/352%) - "
         "FY2022's own report figure is used, per this project's convention.\n\n"
         "FY2020 (435%) added 2026-09-15 and placed on the POINT-IN-TIME row, not the average row: it comes "
         "from the FY2021 report's section 10 comparative column, i.e. the same table and the same basis as "
         "FY2021's 276%. Its HQLA (US$782,801k) and net cash outflows (US$179,896k) divide to 435.1%, "
         "reproducing the printed ratio. Reading FY2020 -> FY2021 as 435% -> 276% is therefore like-for-like; "
         "reading FY2020 -> FY2022 across the two rows is not.\n\n"
         "FY2014-FY2019 CARRY EXPLICIT STATED-ABSENCE MARKERS AS OF 2026-09-18, replacing blanks, on the "
         "point-in-time row (the HQLA and net-cash-outflow rows above stay blank, since a text marker on an "
         "amount row would sit in a £'000 column). LCR minimum requirements were phased in for UK firms from "
         "October 2015; FY2014's and FY2015's own surviving Pillar 3 editions were re-downloaded and searched "
         "on 2026-09-18 and contain no occurrence of 'LCR', 'liquidity coverage' or 'stable funding' at all. "
         "For FY2016-FY2019 no Pillar 3 document is recoverable (ladder re-run in full that day, every rung "
         "failed) and each year's own Annual Report was read: all four describe managing liquidity 'as per the "
         "PRA's liquidity guidelines, primarily the Liquidity Coverage Ratio' in narrative form and print NO "
         "LCR figure. NOTE the prior version of this note said FY2014-FY2020 - corrected once the FY2021 "
         "document's comparative column was read.\n\n"
         + FY2020_COMPARATIVE_NOTE + "\n\n" + AR_CAPITAL_NOTE,
)

metric(
    "NSFR", "£'000 / % (conv. from USD)",
    [
        ("Total available stable funding", stock_k({"FY2025": 1316936, "FY2024": 1136904, "FY2023": 1066880, "FY2022": 912816})),
        ("Total required stable funding", stock_k({"FY2025": 948441, "FY2024": 768308, "FY2023": 744377, "FY2022": 735763})),
        ("Net Stable Funding Ratio (%)", dict({"FY2025": "138.85%", "FY2024": "147.98%", "FY2023": "143%", "FY2022": "124%",
                     "FY2021": "Not published – FY2021 Pillar 3 s.10 p.22: NSFR 'adopted' from 1 Jan 2022 and "
                               "'will be shown in the next Pillar 3 disclosure'; no FY2021 figure printed"},
            **dict(hist_na("Not applicable – no UK NSFR requirement before 1 Jan 2022 (PRA PS17/21; Bank's "
                           "FY2021 Pillar 3 p.22); FY2011 Basel II Pillar 3 has none"),
                   **{y: "Not applicable (pre-NSFR regime)" for y in
                      ("FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014")}))),
    ],
    p3_sources(),
    note="FY2009-FY2013 'Not applicable' (2026-09-15): the NSFR did not exist as a UK requirement until 1 January "
         "2022, so those years are structurally inapplicable, not gaps. (Plain 'Not applicable' rather than the "
         "'(Basel II)' qualifier used on the neighbouring sheets, because the NSFR post-dates CRD IV too.)\n\n"
         "STRUCTURAL, NOT MISSING - and the Bank says so in its own words. The FY2021 Pillar 3, section 10 "
         "(p.22), states: \"From 1st January 2022 the new UK Net Stable Funding Ratio (NSFR) was adopted and "
         "will be shown in the next Pillar 3 disclosure.\" So FY2021 and every earlier year genuinely have no "
         "NSFR to disclose, and FY2022 is correctly the first year populated. This matches the UK-wide "
         "position under PRA PS17/21: no NSFR requirement and no disclosure template existed before "
         "1 January 2022. Re-verified 2026-09-15 by re-reading the FY2021 document in full.\n\n"
         "FY2014-FY2020 CHANGED FROM BLANK TO 'Not applicable (pre-NSFR regime)' ON 2026-09-18 - the reason "
         "is the regulatory one just given, not a search failure, and an explicit marker stops these seven "
         "columns being re-chased as gaps. (This is the one metric in this workbook where FY2016-FY2019 do "
         "NOT get the 'Pillar 3 lost / no Pillar 3 located' wording used on the neighbouring sheets: recovering "
         "those documents would not produce an NSFR, because there was no NSFR to disclose.) "
         "Note that a FY2020 column IS now available "
         "for the other Pillar 3 metrics on this workbook (see the CET1/leverage/LCR sheets) because the "
         "FY2021 report carries a full FY2020 comparative - but that comparative contains no NSFR either, "
         "which is exactly what the adoption date predicts. The prior version of this note said no Pillar 3 "
         "document could be recovered for FY2016-FY2020; that is now narrowed to FY2016-FY2019.",
)

# Written out explicitly rather than via add_not_disclosed_metric_sheets so that
# FY2009-FY2013 can be marked "Not applicable" (MREL did not exist as a UK regime
# then) instead of "Not publicly disclosed", which would imply a real gap.
metric("MREL Ratio", None,
       [("MREL Ratio", dict({y: (f"Not published – Zenith UK {y} Pillar 3 has no MREL/eligible-liabilities "
                                 "figure or KM2 (text probe 0 hits, 2026-09-19)")
                             for y in ("FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2015", "FY2014")},
                            FY2020=("Not published – no MREL in FY2021 Pillar 3 (carries FY2020 comparatives) "
                                    "or FY2020 Annual Report (text probe 0 hits, 2026-09-19)"),
                            FY2019=_p3_lost("FY2019"), FY2016=Z16_MREL,
                            FY2018=P3_ABSENT, FY2017=P3_ABSENT,
                            **hist_na("Not applicable (pre-dates MREL regime)")))],
       p3_sources(),
       note="No MREL disclosure (numeric or qualitative) or UK KM2 template found in any year's "
            "Pillar 3 report - not explicitly stated as an exemption, but consistent with the "
            "Bank's small size relative to typical MREL-in-scope thresholds. MREL did not exist "
            "as a UK regime for FY2014-FY2020 in any case.\n\n"
            "FY2009-FY2013 changed from 'Not publicly disclosed' to 'Not applicable (pre-dates MREL regime)' "
            "2026-09-15: MREL was introduced by the BRRD and had no UK existence in those years, so those cells "
            "are structurally inapplicable rather than a disclosure gap. The recovered FY2011 Basel II edition "
            "contains no occurrence of 'MREL'.")

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
cf_totals_usd = {
    "Net cash generated from/(used in) operating activities": {"FY2025": -55774052, "FY2024": 207362455, "FY2023": -344220013, "FY2022": -243759796, "FY2021": 116041165,
        "FY2020": 265724803, "FY2019": -97605772, "FY2018": -68158324, "FY2017": 95665715, "FY2016": 304455671,
        "FY2015": -114418701, "FY2014": 132272330},
    "Net cash generated from/(used in) investing activities": {"FY2025": -10835501, "FY2024": 549131, "FY2023": 9155192, "FY2022": -2664646, "FY2021": -11026946,
        "FY2020": -50742728, "FY2019": -39665033, "FY2018": 15003986, "FY2017": 27971228, "FY2016": 43778533,
        "FY2015": -13095456, "FY2014": 38611720},
    "Net cash generated from/(used in) financing activities": {"FY2025": -1267314, "FY2024": -672177, "FY2023": -18526335, "FY2022": -6524165, "FY2021": -9993273,
        "FY2020": 351718, "FY2019": -605349, "FY2014": 50000000},
}
cf_close_usd = {"FY2025": 428080578, "FY2024": 480233340, "FY2023": 276069567, "FY2022": 629660723, "FY2021": 882609330,
    "FY2020": 787588384, "FY2019": 572254591, "FY2018": 710130745, "FY2017": 763285083, "FY2016": 639648140,
    "FY2015": 291413936, "FY2014": 418928093}

bw.add_overview_sheet(
    cash_flow_totals=[(label, flow(vals)) for label, vals in cf_totals_usd.items()]
                      + [("Cash and cash equivalents at end of year", stock(cf_close_usd))],
    cash_flow_unit="£'000",
    balance_sheet_totals=[
        ("Total assets", stock({"FY2025": 2994786108, "FY2024": 2649053981, "FY2023": 2660084803, "FY2022": 3134962834, "FY2021": 2880458633,
            "FY2020": 2307254753, "FY2019": 1691573038, "FY2018": 1904335006, "FY2017": 1675762119, "FY2016": 1319429898,
            "FY2015": 1154131121, "FY2014": 1601019239})),
        ("Total liabilities", stock({"FY2025": 2558955031, "FY2024": 2266900685, "FY2023": 2324063422, "FY2022": 2847557820, "FY2021": 2606125105,
            "FY2020": 2031681535, "FY2019": 1437402457, "FY2018": 1678935447, "FY2017": 1468974823, "FY2016": 1126271499,
            "FY2015": 963610459, "FY2014": 1415822691})),
        ("Total equity", stock({"FY2025": 435831077, "FY2024": 382153296, "FY2023": 336021381, "FY2022": 287405014, "FY2021": 274333528,
            "FY2020": 275573218, "FY2019": 254170581, "FY2018": 225399559, "FY2017": 206787296, "FY2016": 193158399,
            "FY2015": 190520662, "FY2014": 185196548})),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", flow({"FY2025": 84894358, "FY2024": 80341223, "FY2023": 96228685, "FY2022": 63992210, "FY2021": 38240687,
            "FY2020": 36009138, "FY2019": 44175428, "FY2018": 38621276, "FY2017": 28303594, "FY2016": 28699041,
            "FY2015": 22298188, "FY2014": 23395435})),
        ("Operating income", flow({"FY2025": 104326559, "FY2024": 85282089, "FY2023": 106201578, "FY2022": 77253368, "FY2021": 43933658,
            "FY2020": 49440372, "FY2019": 58068399, "FY2018": 49662610, "FY2017": 39958009, "FY2016": 37184422,
            "FY2015": 32314295, "FY2014": 33946758})),
        ("Profit before tax", flow({"FY2025": 64655414, "FY2024": 56254867, "FY2023": 72793651, "FY2022": 45263491, "FY2021": 13636206,
            "FY2020": 21882846, "FY2019": 34721708, "FY2018": 33838999, "FY2017": 16009499, "FY2016": 3425633,
            "FY2015": 7098818, "FY2014": 19002159})),
        ("Profit for the year", flow({"FY2025": 48487744, "FY2024": 42223349, "FY2023": 54837411, "FY2022": 35200687, "FY2021": 11404135,
            "FY2020": 17911347, "FY2019": 27930688, "FY2018": 27509757, "FY2017": 13628897, "FY2016": 2637737,
            "FY2015": 5324114, "FY2014": 14394135})),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Total equity (period end)", stock({"FY2025": 435831077, "FY2024": 382153296, "FY2023": 336021381, "FY2022": 287405014, "FY2021": 274333528,
            "FY2020": 275573218, "FY2019": 254170581, "FY2018": 225399559, "FY2017": 206787296, "FY2016": 193158399,
            "FY2015": 190520662, "FY2014": 185196548})),
    ],
    equity_changes_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%",
            "FY2020": "28.29%", "FY2018": "32.38%", "FY2017": "35.53%", "FY2015": "20.38%", "FY2014": "22.32%"}),
        ("Tier 1 Ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%",
            "FY2020": "28.29%", "FY2018": "32.38%", "FY2017": "35.53%", "FY2015": "20.38%", "FY2014": "22.32%"}),
        ("Total Capital Ratio", {"FY2025": "23.40%", "FY2024": "25.64%", "FY2023": "28.95%", "FY2022": "25.84%", "FY2021": "20.78%",
            "FY2020": "28.29%", "FY2018": "32.38%", "FY2017": "35.53%", "FY2015": "20.38%", "FY2014": "22.32%"}),
        ("Leverage Ratio", {"FY2025": "12.08%", "FY2024": "11.25%", "FY2023": "9.76%", "FY2022": "7.32%", "FY2021": "8.36%",
            "FY2020": "10.68%"}),
        ("LCR", {"FY2025": "270.19%", "FY2024": "330.42%", "FY2023": "310%", "FY2022": "343%"}),
        ("NSFR", {"FY2025": "138.85%", "FY2024": "147.98%", "FY2023": "143%", "FY2022": "124%"}),
    ],
    note="FY2017 (35.53%) and FY2018 (32.38%) CAPITAL RATIOS ADDED 2026-09-18 and they are NOT from a Pillar 3 "
         "document - no Pillar 3 edition survives for either year. Both are stated in the Strategic Report of "
         "that year's own Annual Report (FY2017 printed p.11, FY2018 printed p.8); FY2017's is specifically the "
         "'35.53% under IAS 39 at 31 December 2017' figure, not either of the two 1 January 2018 IFRS 9 "
         "transition figures printed beside it. They appear on all three capital-ratio rows because the Bank's "
         "entire capital base is CET1 by its own statement (no AT1, no Tier 2). The corresponding RWA is NOT "
         "shown anywhere in this workbook for those years and was not derived from capital and ratio - see the "
         "Total RWAs sheet. FY2016 and FY2019 still have no ratio: their editions print a capital table but no "
         "ratio, and their Pillar 3 documents are lost.\n"
         "FY2020 LCR (435%) and FY2021 LCR (276%) are deliberately omitted from this at-a-glance row: both are "
         "point-in-time year-end figures, whereas FY2022 onward are 12-month simple averages, and the two bases "
         "are not comparable on a single trend line. Both bases are shown, on separate rows, on the LCR sheet "
         "itself. The FY2020 capital ratios (28.29%) and leverage ratio (10.68%) ARE shown above: those are "
         "single-basis metrics with no such split, and they were missing from this Overview only because the "
         "pass that recovered FY2020 from the FY2021 report's comparative column populated the detail sheets "
         "without copying the values up here. Corrected 2026-09-15; the figures are a straight duplication of "
         "the CET1/Tier 1/Total Capital Ratio and Leverage Ratio sheets, nothing recomputed. "
         "Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation. All £ figures are converted from the Bank's native USD reporting (see Cash Flow Statement "
         "sheet's FX conversion note) - this conversion was not explicitly requested for this bank but applied for "
         "consistency with the rest of the series. FY2025 statement figures come from the Companies House filing of "
         "the FY2025 accounts, not from the Bank's own site, which publishes annual reports only to FY2024 "
         "(see the Cash Flow Statement sheet note). Window extended back to FY2014 under HD-048 (capped by "
         "explicit user decision - see the HD-048 extension note on the Cash Flow Statement sheet); CET1/Tier "
         "1/Total Capital Ratio for FY2014/FY2015 use a pre-CRD IV methodology (see Pillar 3 sources note on "
         "those sheets) and Leverage Ratio/LCR/NSFR are blank for all of FY2014-FY2020 (not yet in force, and/or "
         "no Pillar 3 document recoverable for FY2016-FY2020). "
         "2026-09-15 HISTORICAL PILLAR 3: a FY2011 Basel II Pillar 3 edition was recovered and transcribed, so the "
         "Pillar 3, RWA Breakdown and Asset Quality sheets now run to FY2009 alongside the statutory statements. "
         "NOTHING FROM IT APPEARS ON THIS OVERVIEW, and the FY2009-FY2013 ratio cells above are blank by design: "
         "that edition states no capital ratio, no leverage ratio and no liquidity metric, and the only ratio it "
         "does print (a 203% 'Solvency Ratio against Pillar 1') is capital over the capital REQUIREMENT, not over "
         "RWA - it is excluded deliberately rather than by omission, because showing it on a ratio trend line "
         "would overstate capitalisation by roughly 12.5x. Its Basel II capital figures sit on their own separate "
         "rows on the Tier 1 Capital and Total Capital sheets. A FY2008 edition was also recovered but produced no "
         "cell anywhere - its only figure is dated to 31 December 2007 accounts adjusted for a May 2008 event, so "
         "it belongs to no year column; see the Pillar 3 sources note.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ZENITH FINANCIALS.xlsx")
