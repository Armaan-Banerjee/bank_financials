import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Arab Bank Europe Plc (Companies House / trading name "Europe Arab Bank plc",
# company 05575857, FRN 446951) reports in EUR (its functional currency) - this
# workbook converts every € figure to £ at the established FX methodology (see
# FX_NOTE below). Only FY2021-FY2024 could be sourced (FY2025 Annual Report was
# still not incorporated as of the 2026-09-07 re-check even though a copy was
# finally found - see ENTITY_NOTE); ratios are never converted.
YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

# --- Source URLs -------------------------------------------------------------
# All three documents were published on eabplc.com, which is now DEAD: as at
# 2026-09-15 every https://www.eabplc.com/downloads/... path 301-redirects to the
# arabbankeurope.com homepage and serves no PDF. The dead original URLs are
# preserved below (ORIG_* constants) so the provenance chain stays readable; the
# citations point at Wayback Machine snapshots, which are the only working form.
#
# Repointed 2026-09-15 to the Wayback "id_" form (.../web/<timestamp>id_/<original>)
# rather than the bare .../web/<timestamp>/ form. The bare form returns the Wayback
# *viewer*, whose behaviour the Internet Archive can change at any time; "id_" is a
# contract to return the original archived bytes. Every snapshot below was re-fetched
# on 2026-09-15 in id_ form and verified to begin "%PDF" with the page count stated.
ORIG_AR2022_URL = "https://www.eabplc.com/downloads/202304_EABAnnualReport_v7_144ppi.pdf"
ORIG_AR2024_URL = "https://www.eabplc.com/downloads/202502_EABAnnualReport_v3.pdf"
ORIG_PILLAR3_2022_URL = "https://www.eabplc.com/downloads/Pillar3.pdf"

# Verified 2026-09-15: 1,951,936 bytes, 98pp.
AR2022_URL = "https://web.archive.org/web/20240714135652id_/" + ORIG_AR2022_URL
# Verified 2026-09-15: 14,927,337 bytes, 100pp.
AR2024_URL = "https://web.archive.org/web/20250805183352id_/" + ORIG_AR2024_URL

# Recovered 2026-09-07 (HD-081 item 4 re-check): the generic Pillar3.pdf that was
# previously found archived but truncated/corrupted on every retry now downloads
# intact. EAB Group's own standalone Pillar 3 disclosure as at 31 Dec 2022 (with a
# 31 Dec 2021 comparative) - covers FY2021/FY2022 only, on both an "EAB Group"
# (consolidated) and "EAB plc" (entity-only) basis; this workbook uses the EAB plc
# entity-only column throughout, consistent with every other sheet.
#
# UNDATED FILENAME - EDITION PINNED DELIBERATELY. "Pillar3.pdf" carries no year, so
# the same URL can hold different editions at different capture times (the trap that
# caught Metro Bank, where FY2013 and FY2014 shared one URL and differed only by
# capture). Timestamp 20240714131343 is pinned, and the financial year it actually
# covers was confirmed by opening the file on 2026-09-15 rather than inferred:
#   - page 1, verbatim: "This document comprises EAB Group's ("the Group") Pillar 3
#     disclosures as at 31 DEC 2022";
#   - internal PDF Title metadata: "Microsoft Word - Draft Pillar
#     3_EAB_consolidated_DEC22_Board approved_final_for publication".
#   => CONFIRMED FY2022 edition (as at 31 December 2022, FY2021 comparative).
# Verified 2026-09-15: 3,074,106 bytes, 35pp (not the 1 MiB truncation failure mode).
# The Wayback CDX index lists three captures of this URL. 20240714131343 and
# 20250505164839 share the IDENTICAL content digest MJ7ZTRM4IN3H5WCITTWXRFZGO2EVRAJL
# (both 2,537,938 compressed), i.e. they are byte-identical copies of this same
# FY2022 edition - so the newer capture is not a different edition. The earlier
# capture 20240713003435 has a DIFFERENT digest (IFQXMT5CEFV2KAUTJGNEQ6POP6YM5DB2,
# 1,036,749) and is very likely the truncated/corrupt copy earlier sessions hit; do
# not use it.
PILLAR3_2022_URL = "https://web.archive.org/web/20240714131343id_/" + ORIG_PILLAR3_2022_URL

# Dead-link register for this bank, quoted into the entity note below.
DEAD_URL_NOTE = (
    "DEAD SOURCE URL REGISTER (recorded 2026-09-15, nothing deleted): the three documents this "
    "workbook is built from were published at "
    f"{ORIG_AR2022_URL}, {ORIG_AR2024_URL} and {ORIG_PILLAR3_2022_URL}. All three of those original "
    "URLs are DEAD as at 2026-09-15 - eabplc.com has migrated wholesale to arabbankeurope.com and "
    "301-redirects every old /downloads/ path to that site's homepage, serving HTML rather than a PDF. "
    "They are kept on the record here because a citation's provenance chain must stay readable even "
    "once the host is gone. The working replacement for each is the Wayback Machine snapshot cited "
    "throughout this workbook, given in the 'id_' form (https://web.archive.org/web/<timestamp>id_/"
    "<original URL>), which returns the original archived bytes rather than the Wayback viewer page. "
    "Each snapshot was re-fetched and verified on 2026-09-15: FY2022 Annual Report 1,951,936 bytes / "
    "98pp; FY2024 Annual Report 14,927,337 bytes / 100pp; standalone Pillar3.pdf 3,074,106 bytes / 35pp. "
    "The standalone Pillar3.pdf has an UNDATED filename, so its capture timestamp (20240714131343) is "
    "pinned and the financial year it covers was confirmed by opening the file - page 1 states "
    "\"EAB Group's ... Pillar 3 disclosures as at 31 DEC 2022\" and the PDF's own Title metadata reads "
    "\"Draft Pillar 3_EAB_consolidated_DEC22_Board approved_final_for publication\": it is the FY2022 "
    "edition with a FY2021 comparative, recorded explicitly so the same URL can never later be mistaken "
    "for a different edition. The only other capture of that URL with intact content (20250505164839) "
    "carries the identical Wayback content digest (MJ7ZTRM4IN3H5WCITTWXRFZGO2EVRAJL), i.e. it is the "
    "same file, not a later edition. "
    "NO ARCHIVED COPY EXISTS for the FY2023 and FY2024 standalone Pillar 3 disclosures: a Wayback CDX "
    "query on https://www.eabplc.com/downloads/Pillar3EAB_PLC_2024.pdf and on .../Pillar3EABplc2023.pdf "
    "returned successfully with an EMPTY result set on 2026-09-15, and a domain-wide CDX scan of "
    "eabplc.com returned a full result set containing no 2023 or 2024 Pillar 3 file. This is an "
    "enumerated real absence, established by a query that worked - not a fetch failure or a throttled "
    "request."
)

# ---------------------------------------------------------------
# FX conversion: rates in market convention "£1 = €X" (Bank of England GBP/EUR
# spot reference rate). To convert a € amount to £: gbp = eur / rate.
# Source: Bank of England daily reference rates, via poundsterlinglive.com's
# published archive of the official BoE series
# (https://www.poundsterlinglive.com/bank-of-england-spot/historical-spot-exchange-rates/gbp/gbp-to-eur-<year>).
# "period_end" = spot rate on 31 December each year (or the last trading day
# if 31 Dec fell on a weekend); FY2021's *opening* balance needs 31 Dec 2020's
# rate too, included below. "average" = simple arithmetic mean of the daily
# reference rates across that calendar year.
FX_RATES = {
    "FY2020": {"period_end": 1.1118},  # 31 Dec 2020 only - needed for FY2021's opening cash balance
    "FY2021": {"period_end": 1.1907, "average": 1.1628},
    "FY2022": {"period_end": 1.1277, "average": 1.1717},
    "FY2023": {"period_end": 1.1539, "average": 1.1520},
    "FY2024": {"period_end": 1.2099, "average": 1.1824},
}
PRIOR_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023"}


def gbp_spot(eur_by_year):
    """Convert a {year: €'000} dict to £'000 using that year's OWN period-end spot rate (stocks)."""
    return {y: round(v / FX_RATES[y]["period_end"], 1) for y, v in eur_by_year.items()}


def gbp_spot_prior(eur_by_year):
    """Convert a {year: €'000} dict to £'000 using the PRIOR year's period-end spot rate
    (for opening cash balances, which are last year's closing balance)."""
    return {y: round(v / FX_RATES[PRIOR_YEAR[y]]["period_end"], 1) for y, v in eur_by_year.items()}


def gbp_avg(eur_by_year):
    """Convert a {year: €'000} dict to £'000 using that year's average rate (flows)."""
    return {y: round(v / FX_RATES[y]["average"], 1) for y, v in eur_by_year.items()}


FX_NOTE = (
    "FX CONVERSION NOTE: Arab Bank Europe Plc (trading/registered as \"Europe Arab Bank plc\") reports in Euros "
    "(its functional currency, per its own Annual Report) - this is the first EUR-reporting workbook in this "
    "series. Converted to £ following the same methodology used for this project's earlier USD-reporting banks "
    "(SMBC BI, Zenith, UBA UK, Access Bank UK, Union Bank of India UK): point-in-time/balance figures use the "
    "Bank of England GBP/EUR SPOT rate as at that fiscal year-end (31 December); flow figures (every cash flow "
    "statement line item) use the AVERAGE of the daily spot rates over that calendar year - both from Bank of "
    "England daily reference rates via poundsterlinglive.com's published archive. Rates used (£1 = €X): 31 Dec "
    "2020 spot 1.1118 (FY2021 opening cash only); FY2021 spot 1.1907 / average 1.1628; FY2022 spot 1.1277 / "
    "average 1.1717; FY2023 spot 1.1539 / average 1.1520; FY2024 spot 1.2099 / average 1.1824. All % ratios (CET1/"
    "Total Capital ratios - see ENTITY_NOTE for why this is all that's disclosed) are shown EXACTLY as reported "
    "in EUR and were NOT converted - a ratio is dimensionless and currency-invariant. Because stocks and flows "
    "are converted at different rates (standard practice for translating foreign-currency financial statements), "
    "a programmatically-computed 'Effect of GBP/EUR translation' reconciling line is included so opening + all "
    "flows + this line = closing exactly in £ terms."
)

ENTITY_NOTE = (
    "ENTITY NOTE: Arab Bank Europe Plc, FRN 446951, company 05575857 (incorporated 2005, trades and files "
    "financial statements under the name \"Europe Arab Bank plc\" - the PRA list's word order is reversed vs. "
    "Companies House/FCA register, confirmed as the same entity via FRN and company number match, not a guess). "
    "Wholly-owned subsidiary of Arab Bank plc (Jordan); UNLIKE many single-foreign-parent subsidiaries in this "
    "series, it does NOT take the FRS 101/102 cash-flow-statement exemption - a full Cash Flow Statement is "
    "published every year. eabplc.com's TLS configuration originally rejected every automated fetch attempted; "
    "re-checked 2026-09-07 (HD-081 item 4) and the domain now serves valid TLS but has migrated wholesale to "
    "arabbankeurope.com with a blanket 301 redirect to that site's homepage for every old eabplc.com URL "
    "(including PDF paths that Google's index still shows as live, e.g. Pillar3EABplc2023.pdf and "
    "Pillar3EAB_PLC_2024.pdf - both 301 to the new homepage, not obtainable, and neither is in the Wayback "
    "Machine: re-confirmed 2026-09-16 by a Wayback CDX query on each exact URL, both of which returned "
    "successfully with an EMPTY result set, which is an enumerated absence rather than a failed fetch), so most "
    "sourcing still relies on Wayback Machine snapshots. The FY2022 Annual Report (giving "
    "FY2021+FY2022) and the FY2024 Annual Report (giving FY2023+FY2024) remain the two Annual Reports used "
    "throughout this workbook. The FY2021 and FY2023 standalone Annual Reports were still not obtainable on "
    "re-check. The FY2025 Annual Report, previously unobtainable, WAS found on re-check (2026-09-07) live at "
    "arabbankeurope.com/downloads/annual-report-2025/ (Companies House confirms this FY2025 filing, filed 10 May "
    "2026) - not incorporated into this workbook (YEARS remains FY2021-FY2024; adding a 5th year requires a full "
    "statement transcription across every ST- sheet, out of scope for this correctness re-check - flagged for a "
    "future year-extension ticket). The generic 'Pillar3.pdf' previously found archived but truncated/corrupted "
    "on every retry attempted was RE-CHECKED 2026-09-07 and now downloads intact from its Wayback snapshot "
    f"({PILLAR3_2022_URL}, 3,074,106 bytes, 35pp, EAB Group's "
    "own standalone Pillar 3 disclosure as at 31 Dec 2022 with a 31 Dec 2021 comparative; the capture timestamp "
    "is pinned and that financial year was confirmed from the document's own page 1 and PDF Title metadata - see "
    "the dead-URL register below) - it gives full "
    "entity-level (\"EAB plc**\", i.e. Arab Bank Europe Plc solo, not the wider EAB Group) capital/RWA/leverage/"
    "LCR/NSFR amounts for FY2021 and FY2022, previously all marked 'Not publicly disclosed'; see the individual "
    "Pillar 3 metric sheets and the RWA Breakdown sheet for the recovered figures and their citation. No "
    "equivalent standalone document could be recovered for FY2023 or FY2024, so those two years remain limited "
    "to the Annual Report's own two headline ratios. "
    "Pillar 3 disclosure for FY2023/FY2024 is consequently still thin: only two ratios (Capital adequacy/Total "
    "Capital ratio, Common Equity Tier 1 ratio) are stated for those years, as headline percentages in the "
    "Annual Report's own "
    "'Other Key Performance Indicators' table (note 37 does not add any £/€ breakdown for those two years - CET1/"
    "Total Capital amounts, RWA, leverage, LCR and NSFR for FY2023/FY2024 are not disclosed anywhere in the "
    "sourced documents; MREL is not disclosed for any year) - the same narrative-KPI-only pattern seen at AIB "
    "Group (UK) and Bank of Ireland (UK), now only for FY2023/FY2024 rather than all four years. A genuine, "
    "undocumented cash bridge gap exists between FY2022's closing balance (per the FY2022 Annual Report, "
    "€158,856k) and FY2023's opening balance (per the FY2024 Annual Report's own comparative column, €538,633k) - "
    "the FY2023 Annual Report itself, which would show what happened during that year, was not obtainable "
    "(re-checked 2026-09-07, both eabplc.com direct and a broader Wayback search: still not archived anywhere). "
    "The FY2023 column shows a 'Loss on disposal of subsidiary' (€3,294k) and 'Disposal of subsidiaries' "
    "(€25,342k) line item not present in any other year, consistent with a subsidiary disposal/deconsolidation "
    "event during FY2023, but this does not come close to explaining the full €379,777k gap; the FY2025 Annual "
    "Report found on re-check (see above) only carries FY2024/FY2025 comparatives, one year too late to shed any "
    "light on FY2023, and contains no restatement note referencing FY2023 or FY2022 - left unbridged and flagged "
    "rather than silently forced to reconcile.\n\n"
    + DEAD_URL_NOTE
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Arab Bank Europe Plc's (Europe Arab Bank plc's) own Cash Flow Statement, converted "
    "from EUR to £'000 (see FX conversion note below):\n"
    f"FY2024/FY2023: Europe Arab Bank plc Annual Report and Financial Statements 2024, p.31 (Cash Flow Statement) "
    f"- {AR2024_URL}\n"
    f"FY2022/FY2021: Europe Arab Bank plc Annual Report and Financial Statements 2022, p.30 (Cash Flow Statement) "
    f"- {AR2022_URL}\n"
    "Each pair's own report was used for both its own year and its comparative column. FY2023/FY2024 use a "
    "materially different note structure to FY2021/FY2022 (new lines: trading gains on securities/derivatives, "
    "gain on lease modification, FX adjustments on ECL/ROU, loss on disposal of subsidiary/disposal of "
    "subsidiaries) - a genuine presentation evolution, not a gap; blank cells mark a line item that doesn't apply "
    "to that year's presentation, section TOTALs are unaffected and fully comparable.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)


def p3_sources(page):
    return (
        "Sources - Arab Bank Europe Plc's (Europe Arab Bank plc's) own Annual Report, 'Other Key Performance "
        "Indicators' table (% ratios only - see ENTITY_NOTE on the Cash Flow Statement sheet for why no £/€ "
        "breakdown, RWA, leverage, LCR, NSFR, or MREL figure could be sourced):\n"
        f"FY2024/FY2023: Annual Report and Financial Statements 2024, p.{page['FY2024']} - {AR2024_URL}\n"
        f"FY2022/FY2021: Annual Report and Financial Statements 2022, p.{page['FY2022']} - {AR2022_URL}"
    )


bw = BankWorkbook(bank_name="Arab Bank Europe Plc", years=YEARS, header_color="355070")

# ---------------------------------------------------------------
# ST- rollout: Balance Sheet, P&L, Statement of Changes in Equity, Asset
# Quality, RWA Breakdown. Same two Annual Reports as the Cash Flow Statement
# above (FY2022 report -> FY2021/FY2022; FY2024 report -> FY2023/FY2024);
# figures transcribed directly from each report's own primary statements
# (not its comparative columns, per this project's per-year-primary-source
# convention), then converted to £ with the same gbp_spot/gbp_avg/
# gbp_spot_prior helpers and rate table used above. All EUR figures below
# are as printed in the two Annual Reports - see BS_SOURCES/IS_SOURCES/
# EQ_SOURCES/AQ_SOURCES for exact page citations.
# ---------------------------------------------------------------

BS_SOURCES = (
    "Sources - Arab Bank Europe Plc's (Europe Arab Bank plc's) own Statement of Financial Position, converted "
    "from EUR to £'000 at each year's own period-end spot rate (see FX conversion note below):\n"
    f"FY2024/FY2023: Annual Report and Financial Statements 2024, p.29 (Statement of Financial Position) - {AR2024_URL}\n"
    f"FY2022/FY2021: Annual Report and Financial Statements 2022, p.28 (Statement of Financial Position) - {AR2022_URL}\n"
    "Presentation change: FY2021/FY2022 carry a separate 'Foreign exchange reserve' equity line (values -13/-16 "
    "EUR'000); FY2023/FY2024's own statement drops this line entirely (folded into Retained earnings, see the "
    "Statement of Changes in Equity sheet's note on the FY2022 restatement) - left blank for FY2023/FY2024 rather "
    "than forced into a still-existing line.\n\n" + ENTITY_NOTE + "\n\n" + FX_NOTE
)

IS_SOURCES = (
    "Sources - Arab Bank Europe Plc's (Europe Arab Bank plc's) own Income Statement and Statement of Comprehensive "
    "Income, converted from EUR to £'000 at each year's own average rate (see FX conversion note below):\n"
    f"FY2024/FY2023: Annual Report and Financial Statements 2024, pp.26-27 (Income Statement; Statement of "
    f"Comprehensive Income) - {AR2024_URL}\n"
    f"FY2022/FY2021: Annual Report and Financial Statements 2022, pp.25-26 (Income Statement; Statement of "
    f"Comprehensive Income) - {AR2022_URL}\n"
    "Presentation changes across the two reports (both genuine, not gaps): FY2021/FY2022 separately disclose "
    "'Other interest and similar expense', 'Dividend income', and a 'Total Income' subtotal (Net Operating Income "
    "+ Dividend income) that FY2023/FY2024's report does not carry (Net Operating Income flows straight to "
    "expenses) - left blank for FY2023/FY2024 rather than merged into another line. OCI detail: FY2021/FY2022 show "
    "an 'Exchange differences on translation of non-Euro denominated operations' line every year; FY2023/FY2024 "
    "show it only for FY2024 (blank/nil for FY2023, per the report's own '-' entry). All TOTAL rows (Net interest "
    "income, Net Operating Income, Total operating expenses before impairment losses, Profit before tax, Profit "
    "for the year, Other comprehensive income, Total comprehensive income) are fully comparable across all 4 "
    "years.\n\n" + ENTITY_NOTE + "\n\n" + FX_NOTE
)

EQ_SOURCES = (
    "Sources - Arab Bank Europe Plc's (Europe Arab Bank plc's) own Statement of Changes in Equity, converted from "
    "EUR to £'000 (movement rows at that year's average rate, Balance rows at that year-end's spot rate - see FX "
    "conversion note below):\n"
    f"FY2024/FY2023 + restated FY2022 closing: Annual Report and Financial Statements 2024, p.30 - {AR2024_URL}\n"
    f"FY2020 opening/FY2021/FY2022 (as originally reported): Annual Report and Financial Statements 2022, p.29 - "
    f"{AR2022_URL}\n"
    "FLAGGED DISCREPANCY (not silently reconciled): the FY2024 Annual Report's own comparative 'As at 31 December "
    "2022' balance differs from the FY2022 Annual Report's own closing balance for the same date - Fair value "
    "reserve €(10,515)k vs. €(10,516)k (€1k), Retained earnings €(263,496)k vs. €(263,479)k (€17k), and the "
    "Foreign exchange reserve line (€(16)k in the FY2022 report) is dropped entirely from the FY2024 report's "
    "restated column. Total equity is identical in both (€295,854k), so this reads as a reclassification of the "
    "FX reserve into Retained earnings with a small residual rounding difference, not a genuine restatement of "
    "total equity - but the components genuinely disagree between the two primary sources, so both the "
    "originally-reported and restated 31 Dec 2022 balances are shown as separate rows below rather than picking "
    "one silently. A second, much smaller rounding artefact: FY2022's own Statement of Comprehensive Income "
    "states Total comprehensive income of €2,614k, while summing that year's Statement of Changes in Equity "
    "movement rows (Profit €12,416k + OCI €(354)k + Changes in fair value €(9,446)k) gives €2,616k - a €2k "
    "difference present in the source tables themselves.\n\n" + ENTITY_NOTE + "\n\n" + FX_NOTE
)

AQ_SOURCES = (
    "Sources - Arab Bank Europe Plc's (Europe Arab Bank plc's) own Note 34/33 'Credit risk - Quality of Assets' "
    "table, 'Loans and advances to customers' column only (the note's other columns - cash/due from banks, "
    "financial investments at amortised cost, guarantees/LCs/unused facilities - are not loan-book exposures and "
    "are excluded here), converted from EUR to £'000 at each year's period-end spot rate:\n"
    f"FY2024/FY2023: Annual Report and Financial Statements 2024, pp.75-76 (Note 33, Credit risk, Quality of "
    f"Assets) - {AR2024_URL}\n"
    f"FY2022/FY2021: Annual Report and Financial Statements 2022, pp.72-73 (Note 34, Credit risk, Quality of "
    f"Assets) - {AR2022_URL}\n"
    "No by-product split is disclosed anywhere in either report - only the by-IFRS-9-stage breakdown shown here. "
    "FY2023/FY2024's table separately discloses an 'Interest Receivable' amount added after ECL to reach the net "
    "figure; FY2021/FY2022's table has no such line (net = gross - ECL exactly that year) - left blank for "
    "FY2021/FY2022 rather than forced to zero. Ratios (ECL coverage, Stage 3/NPL, Stage 3 coverage) are computed "
    "from the £-converted gross/ECL figures above, consistent with this project's convention "
    "elsewhere.\n\n" + ENTITY_NOTE + "\n\n" + FX_NOTE
)

SDDT_NOTE = (
    "THESE BLANKS ARE NOT A LAWFUL EXEMPTION - THEY ARE A MISSING DISCLOSURE. Arab Bank Europe is NOT an SDDT. "
    "The PRA's consolidated register of waivers and modifications for PRA-authorised firms carries exactly three "
    "rows for FRN 446951 'Europe Arab Bank plc' - Article 9 CRR (28/03/2018), Capital Buffers 5.1-5.3 "
    "(15/05/2023) and Article 400(2)(c) non-core large exposures (15/04/2024-15/04/2027) - and NO Disclosure "
    "(CRR) Rule 3.1 SDDT modification, which is the only waiver that removes the Pillar 3 duty. Unlike Cynergy, "
    "Methodist Chapel Aid, Griffin or Hampden, this bank therefore had a LIVE Pillar 3 disclosure obligation "
    "throughout FY2023, FY2024 and FY2025. The documents were required to exist; they simply are not published "
    "on any reachable host. USER-ACTIONABLE: request the FY2023-FY2025 editions from the Bank directly - there "
    "is a live regulatory obligation behind the request, which is not true of the SDDT cases elsewhere in this "
    "series.\n"
    "AVAILABILITY RE-ENUMERATED 2026-09-15 (positive evidence, not filename permutation). (a) The two "
    "Google-indexed paths https://www.eabplc.com/downloads/Pillar3EAB_PLC_2024.pdf and "
    ".../Pillar3EABplc2023.pdf were re-fetched this session: both return HTTP 200 but with Content-Type "
    "text/html and an identical 95,415-byte body, redirecting to https://arabbankeurope.com/ - they serve the "
    "Arab Bank Europe homepage, not a PDF. (b) An unfiltered Wayback CDX scan of the entire eabplc.com domain "
    "(1,546 unique captures) filtered for 'pillar' returns 12 Pillar 3 documents: a continuous annual series "
    "for 2009, 2010, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019 and 2020, and then a single 2024-07 "
    "capture of the FY2022 edition cited on these sheets. There is NO FY2021, NO FY2023 and NO FY2024 capture. "
    "PATH RECORDED 2026-09-16 so a future year extension does not have to rediscover it: that 2009-2020 series "
    "is NOT under /downloads/ (the path every earlier probe tried, and the path the FY2022 edition uses) but "
    "under https://www.eabplc.com/files/PDFs/ and https://www.eabplc.com/files/PDFs/Pillar%203/ - which is "
    "precisely why filename permutation under /downloads/ kept missing it. Confirmed archived 200 "
    "application/pdf, with capture timestamps: 'EAB 2020 Pillar 3.pdf' 20210918020429; 'EAB 2019 Pillar 3.pdf' "
    "20210918015853; 'Pillar III Disclosure 2018.pdf' 20210918014555 and 'EAB 2017 Pillar 3 - FINALv2.pdf' "
    "20210918014857, both under /files/PDFs/Pillar%203/; 'EAB 2016 Pillar 3 - CRDIV_FINAL.pdf' 20220707074618 "
    "(also /files/PDFs/Pillar%203/); 'EAB 2015 Pillar 3 - CRDIV.pdf' 20161108212906; 'EAB 2014 Pillar 3 - "
    "CRDIV Final Draft.pdf' 20161108192950; 'EAB 2013 Pillar Three - Final Draft.pdf' 20161108212844; "
    "'3.4 - EAB 2012 Pillar Three.pdf' 20161108212856; plus a 2009/2010 pair under /pdfs/ and "
    "/english/pdfs/. So the correct characterisation is that this bank published a standalone Pillar 3 for "
    "roughly nine years and then, after the FY2022 edition, stopped - NOT that it rarely or never published "
    "one. None of these documents is transcribed here: all of them predate this workbook's FY2021-FY2024 "
    "window, and recording the path is deliberately wording-only, not a year extension. "
    "(c) A CDX scan of the successor domain arabbankeurope.com returns 20 captures and no PDFs at all. FY2021's "
    "absence costs nothing beyond leverage/NSFR (see those sheets - the FY2022 edition's own comparative column "
    "supplies FY2021 capital, RWA and LCR, and flags leverage/NSFR 'n/a' as structural)."
)

BASIS_NOTE = (
    "BASIS DETERMINATION (verified 2026-09-15 by reading the document's own 'Scope' section, not inferred). The "
    "recovered Pillar 3 document is headed \"This document comprises EAB Group's ('the Group') Pillar 3 "
    "disclosures as at 31 DEC 2022\", and its Scope section (PDF p.5) states verbatim: \"The EAB Group comprising "
    "EAB plc and its subsidiary, Europe Arab Bank SA ('EAB SA'), operates through offices in four European "
    "countries.\" and \"In line with the requirements of the UK CRR, Pillar 3 disclosures have been prepared on "
    "consolidated basis, and where relevant, provide quantitative disclosures for both, Group and EAB plc solo "
    "entity.\" and \"EAB Group is subject to consolidated supervision, with EAB plc also subject to solo "
    "regulatory supervision by the PRA. Therefore, it is a requirement to calculate and maintain regulatory "
    "capital ratios on both a Group basis and on a solo basis for the EAB plc. Capital requirements for both "
    "Group and EAB plc have been presented in these disclosures.\" "
    "So 'EAB Group' is the UK entity's OWN consolidated basis (EAB plc consolidating its French subsidiary) and "
    "NOT the Jordanian parent Arab Bank plc's group - it would have been usable. This workbook nevertheless uses "
    "the narrower 'EAB plc' SOLO column throughout, because every other sheet in this workbook is entity-only and "
    "mixing a solo statement set with a consolidated capital set would breach this project's entity-basis rule. "
    "The two bases differ materially and must never be interchanged: at 31 Dec 2022, Group CET1 EUR290m / RWA "
    "EUR1,810m / CET1 ratio 16.0% / LCR 249% / NSFR 128% / leverage 11.4%, against solo CET1 EUR253m / RWA "
    "EUR1,631m / CET1 ratio 15.5% / LCR 218% / NSFR 120% / leverage 11.7%. Every Pillar 3 figure in this workbook "
    "is the solo column."
)

RWA_NOT_DISCLOSED_NOTE = (
    "Not disclosed in either sourced Annual Report (FY2021/FY2022 or FY2023/FY2024) - the Bank's only capital "
    "disclosure anywhere in these documents is the 'Other Key Performance Indicators' table's two headline ratios "
    "(Capital adequacy/Total Capital ratio, CET1 ratio - see the Total Capital Ratio and CET1 Ratio Pillar 3 "
    "sheets). No RWA amount, UK OV1 exposure-class breakdown, or standalone Pillar 3 document was obtainable (see "
    "ENTITY_NOTE on the Cash Flow Statement sheet).\n"
    "RE-VERIFIED 2026-09-12 (independent re-check of whether a post-FY2022 Pillar 3 has since appeared): it has "
    "not, and the FY2022 one is no longer live. The live https://www.eabplc.com/downloads/Pillar3.pdf path now "
    "returns HTTP 200 but serves the Arab Bank Europe HOMEPAGE as HTML (title 'Home - Arab Bank Europe'), not a "
    "PDF - the document was withdrawn in the site migration, so the web.archive.org capture cited on the other "
    "Pillar 3 sheets is now the only copy in existence. A Wayback CDX scan of the whole eabplc.com domain "
    "filtered for 'pillar' returns 12 documents, all FY2020 or earlier apart from that single 2024-07 capture, "
    "which was re-downloaded and re-read this session and confirmed to cover the year ended 31 Dec 2022 only "
    "(with FY2021 comparatives) - it does not reach FY2023. The FY2024 Annual Report was also re-read in full: "
    "its 'Other Key Performance Indicators' table gives only the two headline ratios already captured (Capital "
    "adequacy 23%/24%, CET1 16%/17% for FY2024/FY2023) and Note 37 'Capital management and risk' gives only net "
    "equity as a EUR amount - no RWA, leverage ratio, LCR or NSFR figure appears anywhere in it. FY2023-FY2025 "
    "therefore remain a genuine post-migration availability gap rather than a document this session failed to "
    "fetch.\n"
    "RE-VERIFIED AGAIN 2026-09-15, independently and via the FY2025 Annual Report (which was NOT available to "
    "the earlier checks in usable form). That report is now live and directly downloadable at "
    "https://arabbankeurope.com/wp-content/uploads/202602_EABAnnualReport_v9.pdf (111pp, real text layer, "
    "reached via arabbankeurope.com/downloads/annual-report-2025/, which 302s to that CDN path) - recording the "
    "resolved URL here because the migrated site exposes no document index. It CONFIRMS the FY2024 figures "
    "already held: its Key Performance Indicators table (p.6) gives Capital adequacy ratio 2024 = 23% and "
    "Common Equity Tier 1 capital ratio 2024 = 16%, both reproducing this workbook's FY2024 values exactly, so "
    "the basis is validated. It adds NOTHING further for FY2024: Note 36.6 'Capital management and risk' "
    "(p.109) again discloses only net equity (EUR330m 2025, EUR320m 2024) and perpetual/subordinated "
    "liabilities (EUR107m 2025, EUR121m 2024), and explicitly warns that 'The regulatory capital base differs "
    "slightly from amounts reported above due to differing treatment of certain reserves and consolidation "
    "adjustments' - an express statement by the Bank that net equity is NOT its regulatory capital, so CET1 / "
    "Tier 1 / Total Capital amounts are not derivable from it and remain blank. No RWA amount, no leverage "
    "ratio, no LCR and no NSFR figure appears anywhere in the FY2025 report either (liquidity is narrative "
    "only: 'liquidity coverage ratio above the regulatory requirements'). A Tier 1 RATIO is likewise not "
    "disclosed in any year: the Bank publishes only a CET1 ratio and a total capital ratio, and because it "
    "holds upper tier 2 subordinated liabilities, the Tier 1 ratio is a genuinely distinct third number that "
    "cannot be inferred from the other two. Five further Pillar 3 filename permutations were tried under the "
    "new /wp-content/uploads/ CDN path discovered above (all 404), and the migrated site has no "
    "regulatory-disclosures or downloads index page at all (arabbankeurope.com/regulatory-disclosures/ returns "
    "404). Conclusion unchanged and now doubly evidenced: Arab Bank Europe stopped publishing Pillar 3 after "
    "the FY2022 edition, and FY2023 onward is a genuine disclosure gap, not an access failure.\n"
    "CLOSED BY ENUMERATION 2026-09-15 (maximum-effort sweep, prior verdicts treated as unproven). The checks "
    "above all rest on filename permutations, which can only fail to find; these two are positive evidence of "
    "the complete set. (1) The migrated site runs WordPress, and its REST media endpoint "
    "(/wp-json/wp/v2/media?mime_type=application/pdf) enumerates the ENTIRE uploaded file set: 64 PDFs, of "
    "which exactly one is any kind of financial report (202602_EABAnnualReport_v9.pdf, the FY2025 Annual "
    "Report already cited) and NOT ONE is a Pillar 3 document. (2) The site's hidden downloads index was also "
    "recovered - /sitemap.xml chains to /eab_download-sitemap.xml, listing 53 download slugs including "
    "https://arabbankeurope.com/downloads/pillar-iii-disclosures/. That page still exists and still resolves "
    "HTTP 200, but carries NO attached file of any kind: the slug survived the migration and the document did "
    "not. The old host is fully collapsed - https://www.eabplc.com/ and .../downloads/Pillar3.pdf both now "
    "return the same 18,400-byte Arab Bank Europe homepage HTML under two different user agents.\n"
    "MATERIALLY NEW FINDING, AND IT CHANGES THE CLASSIFICATION: this entity is NOT exempt. The PRA's "
    "consolidated register of waivers and modifications for PRA-authorised firms (downloaded 2026-09-15 from "
    "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
    "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv, UTF-16 TSV, 2,919 rows, of which "
    "135 are SDDT Rule 3.1 rows) carries exactly three rows for FRN 446951 'Europe Arab Bank plc': Article 9 "
    "CRR (28/03/2018), Capital Buffers 5.1-5.3 (15/05/2023), and Article 400(2)(c) non-core large exposures "
    "(15/04/2024-15/04/2027). There is NO Rule 3.1 SDDT modification. So unlike Cynergy, Methodist Chapel "
    "Aid, Griffin or Hampden - whose post-opt-in blanks are a lawful structural exemption - Arab Bank Europe "
    "remained under a live Pillar 3 disclosure obligation throughout FY2023, FY2024 and FY2025. These blanks "
    "are therefore NOT structural. The documents were required to exist, and the bank's own disclosure "
    "practice simply stopped being published on a reachable host. USER-ACTIONABLE: the FY2023-FY2025 "
    "editions should be requested from the Bank directly - unlike an SDDT case, there is a live obligation "
    "behind the request."
)

# --- Balance Sheet ---
BS_CASH = {"FY2024": 224962, "FY2023": 136982, "FY2022": 158856, "FY2021": 174174}
BS_DUE_FROM_BANKS = {"FY2024": 434129, "FY2023": 489573, "FY2022": 379561, "FY2021": 402958}
BS_FVTPL = {"FY2024": 9812, "FY2023": 9463, "FY2022": 12565, "FY2021": 30911}
BS_FVOCI = {"FY2024": 134834, "FY2023": 101448, "FY2022": 128725, "FY2021": 86082}
BS_LOANS_CUSTOMERS = {"FY2024": 1023804, "FY2023": 931303, "FY2022": 838374, "FY2021": 919844}
BS_AMORTISED_COST = {"FY2024": 515123, "FY2023": 434776, "FY2022": 450135, "FY2021": 497729}
BS_DERIVATIVE_ASSETS = {"FY2024": 41899, "FY2023": 38935, "FY2022": 52987, "FY2021": 5648}
BS_INVESTMENT_SUBS = {"FY2024": 75000, "FY2023": 75000, "FY2022": 103636, "FY2021": 113081}
BS_PPE = {"FY2024": 7884, "FY2023": 6810, "FY2022": 6269, "FY2021": 3985}
BS_ROU = {"FY2024": 6494, "FY2023": 7205, "FY2022": 8246, "FY2021": 2828}
BS_OTHER_ASSETS = {"FY2024": 10557, "FY2023": 6489, "FY2022": 17946, "FY2021": 20647}
BS_DEFERRED_TAX = {"FY2024": 5775, "FY2023": 5776, "FY2022": 5775, "FY2021": 5768}
BS_TOTAL_ASSETS = {"FY2024": 2490273, "FY2023": 2243760, "FY2022": 2163075, "FY2021": 2263655}

BS_DEPOSITS_BANKS = {"FY2024": 541985, "FY2023": 551167, "FY2022": 449827, "FY2021": 668654}
BS_CUSTOMER_ACCOUNTS = {"FY2024": 1460718, "FY2023": 1229466, "FY2022": 1250949, "FY2021": 1164504}
BS_DERIVATIVE_LIAB = {"FY2024": 17389, "FY2023": 15765, "FY2022": 19265, "FY2021": 9542}
BS_OTHER_LIAB = {"FY2024": 13004, "FY2023": 13899, "FY2022": 17230, "FY2021": 8616}
BS_CURRENT_TAX_LIAB = {"FY2024": 2197, "FY2023": 1700}
BS_LEASE_LIAB = {"FY2024": 8683, "FY2023": 9450, "FY2022": 9350, "FY2021": 2963}
BS_RETIREMENT = {"FY2024": 4610, "FY2023": 3100, "FY2022": 3570, "FY2021": 6161}
BS_SUBORDINATED = {"FY2024": 120523, "FY2023": 112902, "FY2022": 117030, "FY2021": 109977}
BS_TOTAL_LIAB = {"FY2024": 2169109, "FY2023": 1937449, "FY2022": 1867221, "FY2021": 1970417}

BS_SHARE_CAPITAL = {"FY2024": 569998, "FY2023": 569998, "FY2022": 569998, "FY2021": 569998}
BS_RETAINED_EARNINGS = {"FY2024": -246271, "FY2023": -261961, "FY2022": -263479, "FY2021": -276880}
BS_FX_RESERVE = {"FY2022": -16, "FY2021": -13}
BS_FV_RESERVE = {"FY2024": -2706, "FY2023": -1845, "FY2022": -10516, "FY2021": 26}
BS_CFH_RESERVE = {"FY2024": 143, "FY2023": 119, "FY2022": -133, "FY2021": 107}
BS_TOTAL_EQUITY = {"FY2024": 321164, "FY2023": 306311, "FY2022": 295854, "FY2021": 293238}

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", gbp_spot(BS_CASH)),
    ("DATA", "Due from banks", gbp_spot(BS_DUE_FROM_BANKS)),
    ("DATA", "Financial assets at fair value through profit or loss", gbp_spot(BS_FVTPL)),
    ("DATA", "Financial investments at fair value through OCI", gbp_spot(BS_FVOCI)),
    ("DATA", "Loans and advances to customers", gbp_spot(BS_LOANS_CUSTOMERS)),
    ("DATA", "Financial investments at amortised cost", gbp_spot(BS_AMORTISED_COST)),
    ("DATA", "Derivative financial assets", gbp_spot(BS_DERIVATIVE_ASSETS)),
    ("DATA", "Investment in subsidiaries", gbp_spot(BS_INVESTMENT_SUBS)),
    ("DATA", "Property, plant and equipment", gbp_spot(BS_PPE)),
    ("DATA", "Right-of-use assets", gbp_spot(BS_ROU)),
    ("DATA", "Other assets", gbp_spot(BS_OTHER_ASSETS)),
    ("DATA", "Deferred tax", gbp_spot(BS_DEFERRED_TAX)),
    ("TOTAL", "Total assets", gbp_spot(BS_TOTAL_ASSETS)),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", gbp_spot(BS_DEPOSITS_BANKS)),
    ("DATA", "Customer accounts", gbp_spot(BS_CUSTOMER_ACCOUNTS)),
    ("DATA", "Derivative financial liabilities", gbp_spot(BS_DERIVATIVE_LIAB)),
    ("DATA", "Other liabilities", gbp_spot(BS_OTHER_LIAB)),
    ("DATA", "Current tax liabilities", gbp_spot(BS_CURRENT_TAX_LIAB)),
    ("DATA", "Lease liabilities", gbp_spot(BS_LEASE_LIAB)),
    ("DATA", "Retirement benefits - defined benefit scheme", gbp_spot(BS_RETIREMENT)),
    ("DATA", "Subordinated liabilities", gbp_spot(BS_SUBORDINATED)),
    ("TOTAL", "Total liabilities", gbp_spot(BS_TOTAL_LIAB)),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", gbp_spot(BS_SHARE_CAPITAL)),
    ("DATA", "Retained earnings", gbp_spot(BS_RETAINED_EARNINGS)),
    ("DATA", "Foreign exchange reserve", gbp_spot(BS_FX_RESERVE)),
    ("DATA", "Fair value reserve", gbp_spot(BS_FV_RESERVE)),
    ("DATA", "Cash flow hedge reserve", gbp_spot(BS_CFH_RESERVE)),
    ("TOTAL", "Total equity", gbp_spot(BS_TOTAL_EQUITY)),
    ("TOTAL", "Total liabilities and equity",
     {y: round(gbp_spot(BS_TOTAL_LIAB)[y] + gbp_spot(BS_TOTAL_EQUITY)[y], 1) for y in YEARS}),
]

bw.add_balance_sheet_sheet(
    title="Arab Bank Europe Plc — Statement of Financial Position",
    subtitle="£'000, converted from EUR - see source note at bottom for FX methodology and rates used.",
    rows=balance_sheet_rows,
    sources_text=BS_SOURCES,
    first_col_width=58,
    source_height=200,
    unit_suffix=" (£'000, conv. from EUR)",
)

# --- Income Statement ---
IS_INTEREST_INCOME = {"FY2024": 116296, "FY2023": 96392, "FY2022": 56397, "FY2021": 32406}
IS_OTHER_INTEREST_INCOME = {"FY2024": 15926, "FY2023": 15880, "FY2022": 428, "FY2021": 1763}
IS_INTEREST_EXPENSE = {"FY2024": -80363, "FY2023": -64758, "FY2022": -23303, "FY2021": -5033}
IS_OTHER_INTEREST_EXPENSE = {"FY2022": -1019, "FY2021": -6866}
IS_NET_INTEREST_INCOME = {"FY2024": 51859, "FY2023": 47514, "FY2022": 32503, "FY2021": 22270}
IS_FEE_INCOME = {"FY2024": 5114, "FY2023": 5308, "FY2022": 6330, "FY2021": 6873}
IS_FEE_EXPENSE = {"FY2024": -507, "FY2023": -608, "FY2022": -564, "FY2021": -605}
IS_TRADING_GAINS = {"FY2024": 4052, "FY2023": 1665, "FY2022": 287, "FY2021": 1301}
IS_OTHER_OPERATING_INCOME = {"FY2024": 4302, "FY2023": 3738, "FY2022": 4049, "FY2021": 3499}
IS_NET_OPERATING_INCOME = {"FY2024": 64820, "FY2023": 57617, "FY2022": 42605, "FY2021": 33338}
IS_DIVIDEND_INCOME = {"FY2022": 12162, "FY2021": 206}
IS_TOTAL_INCOME = {"FY2022": 54767, "FY2021": 33544}
IS_DEPRECIATION = {"FY2024": -3228, "FY2023": -2990, "FY2022": -3159, "FY2021": -2588}
IS_OTHER_OPEX = {"FY2024": -36747, "FY2023": -37439, "FY2022": -34691, "FY2021": -28987}
IS_TOTAL_OPEX = {"FY2024": -39975, "FY2023": -40429, "FY2022": -37850, "FY2021": -31575}
IS_OP_PROFIT_PRE_IMPAIRMENT = {"FY2024": 24845, "FY2023": 17188, "FY2022": 16916, "FY2021": 1969}
IS_IMPAIRMENT = {"FY2024": -5401, "FY2023": -4315, "FY2022": -4500, "FY2021": -1567}
IS_PROFIT_BEFORE_TAX = {"FY2024": 19444, "FY2023": 12873, "FY2022": 12416, "FY2021": 402}
IS_TAX_CHARGE = {"FY2024": -2575, "FY2023": -1700, "FY2021": 359}
IS_PROFIT_FOR_YEAR = {"FY2024": 16869, "FY2023": 11173, "FY2022": 12416, "FY2021": 761}

OCI_PENSION_REMEASUREMENT = {"FY2024": -1182, "FY2023": -957, "FY2022": 983, "FY2021": 8076}
OCI_FV_SUBSIDIARIES = {"FY2023": -66, "FY2022": -9446, "FY2021": 9773}
OCI_FVOCI_DEBT = {"FY2024": -861, "FY2023": 55, "FY2022": -1096, "FY2021": -804}
OCI_CASH_FLOW_HEDGE = {"FY2024": 24, "FY2023": 252, "FY2022": -240, "FY2021": 107}
OCI_FX_TRANSLATION = {"FY2024": 3, "FY2022": -3, "FY2021": 4}
OCI_TOTAL = {"FY2024": -2016, "FY2023": -716, "FY2022": -9802, "FY2021": 17156}
TOTAL_COMPREHENSIVE_INCOME = {"FY2024": 14853, "FY2023": 10457, "FY2022": 2614, "FY2021": 17917}

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income using the effective interest method", gbp_avg(IS_INTEREST_INCOME)),
    ("DATA", "Other interest and similar income", gbp_avg(IS_OTHER_INTEREST_INCOME)),
    ("DATA", "Interest and similar expense", gbp_avg(IS_INTEREST_EXPENSE)),
    ("DATA", "Other interest and similar expense", gbp_avg(IS_OTHER_INTEREST_EXPENSE)),
    ("TOTAL", "Net interest and similar income", gbp_avg(IS_NET_INTEREST_INCOME)),
    ("DATA", "Fee and commission income", gbp_avg(IS_FEE_INCOME)),
    ("DATA", "Fee and commission expense", gbp_avg(IS_FEE_EXPENSE)),
    ("DATA", "Net trading gains", gbp_avg(IS_TRADING_GAINS)),
    ("DATA", "Other operating income", gbp_avg(IS_OTHER_OPERATING_INCOME)),
    ("TOTAL", "Net Operating Income", gbp_avg(IS_NET_OPERATING_INCOME)),
    ("DATA", "Dividend income", gbp_avg(IS_DIVIDEND_INCOME)),
    ("TOTAL", "Total Income", gbp_avg(IS_TOTAL_INCOME)),
    ("DATA", "Depreciation of property, plant and equipment and right-of-use assets", gbp_avg(IS_DEPRECIATION)),
    ("DATA", "Other operating expenses", gbp_avg(IS_OTHER_OPEX)),
    ("TOTAL", "Total operating expenses before impairment losses", gbp_avg(IS_TOTAL_OPEX)),
    ("TOTAL", "Operating profit before impairment loss expense and tax expense", gbp_avg(IS_OP_PROFIT_PRE_IMPAIRMENT)),
    ("DATA", "Impairment loss expense", gbp_avg(IS_IMPAIRMENT)),
    ("TOTAL", "Profit before tax", gbp_avg(IS_PROFIT_BEFORE_TAX)),
    ("DATA", "Tax (charge)/credit", gbp_avg(IS_TAX_CHARGE)),
    ("TOTAL", "Profit for the year", gbp_avg(IS_PROFIT_FOR_YEAR)),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Re-measurement of net defined benefit pension liability", gbp_avg(OCI_PENSION_REMEASUREMENT)),
    ("DATA", "Fair value (loss)/gain taken to equity on investment in subsidiaries", gbp_avg(OCI_FV_SUBSIDIARIES)),
    ("DATA", "Fair value (loss)/gain taken to equity on financial investments - debt", gbp_avg(OCI_FVOCI_DEBT)),
    ("DATA", "Fair value (loss)/gain taken to equity on derivatives - cash flow hedge", gbp_avg(OCI_CASH_FLOW_HEDGE)),
    ("DATA", "Exchange differences on translation of non-Euro denominated operations", gbp_avg(OCI_FX_TRANSLATION)),
    ("TOTAL", "Other comprehensive income/(loss) for the year", gbp_avg(OCI_TOTAL)),
    ("TOTAL", "Total comprehensive income for the year", gbp_avg(TOTAL_COMPREHENSIVE_INCOME)),
]

bw.add_income_statement_sheet(
    title="Arab Bank Europe Plc — Income Statement and Statement of Comprehensive Income",
    subtitle="£'000, converted from EUR - see source note at bottom for FX methodology and rates used.",
    rows=income_statement_rows,
    sources_text=IS_SOURCES,
    first_col_width=70,
    source_height=260,
    unit_suffix=" (£'000, conv. from EUR)",
)

# --- Statement of Changes in Equity (chronological, EUR converted at the row's own logic) ---
EQUITY_HEADERS = ["Ordinary share capital", "Fair value reserve", "Cash flow hedge reserve",
                   "Foreign exchange reserve", "Retained earnings", "Total equity"]


def eq_gbp_spot(y, eur_vals):
    """Convert one chronological equity row's (col->EUR) values to £ using year y's period-end spot rate."""
    rate = FX_RATES[y]["period_end"]
    return tuple(round(v / rate, 1) if v is not None else None for v in eur_vals)


def eq_gbp_avg(y, eur_vals):
    """Convert one chronological equity row's (col->EUR) values to £ using year y's average rate."""
    rate = FX_RATES[y]["average"]
    return tuple(round(v / rate, 1) if v is not None else None for v in eur_vals)


equity_changes_rows = [
    ("TOTAL", "Balance at 31 December 2020", eq_gbp_spot("FY2021", (569998, -8943, None, -17, -285717, 275321))),
    ("DATA", "Profit for the year (2021)", eq_gbp_avg("FY2021", (None, None, None, None, 761, 761))),
    ("DATA", "Other comprehensive income (2021)", eq_gbp_avg("FY2021", (None, -804, 107, 4, 8076, 7383))),
    ("DATA", "Changes in fair value (2021)", eq_gbp_avg("FY2021", (None, 9773, None, None, None, 9773))),
    ("TOTAL", "Balance at 31 December 2021", eq_gbp_spot("FY2021", (569998, 26, 107, -13, -276880, 293238))),
    ("DATA", "Profit for the year (2022)", eq_gbp_avg("FY2022", (None, None, None, None, 12416, 12416))),
    ("DATA", "Other comprehensive income (2022)", eq_gbp_avg("FY2022", (None, -1096, -240, -3, 983, -354))),
    ("DATA", "Changes in fair value (2022)", eq_gbp_avg("FY2022", (None, -9446, None, None, None, -9446))),
    ("TOTAL", "Balance at 31 December 2022 (as originally reported, FY2022 Annual Report)",
     eq_gbp_spot("FY2022", (569998, -10516, -133, -16, -263479, 295854))),
    ("DATA", "Balance at 31 December 2022 (restated opening balance per FY2024 Annual Report - FX reserve folded "
             "into Retained earnings, €1k rounding difference in Fair value reserve; see EQ_SOURCES flag)",
     eq_gbp_spot("FY2022", (569998, -10515, -133, None, -263496, 295854))),
    ("DATA", "Profit for the year (2023)", eq_gbp_avg("FY2023", (None, None, None, None, 11173, 11173))),
    ("DATA", "Other comprehensive income (2023)", eq_gbp_avg("FY2023", (None, 55, 252, None, -957, -650))),
    ("DATA", "Changes in fair value (2023)", eq_gbp_avg("FY2023", (None, 8615, None, None, -8681, -66))),
    ("TOTAL", "Balance at 31 December 2023", eq_gbp_spot("FY2023", (569998, -1845, 119, None, -261961, 306311))),
    ("DATA", "Profit for the year (2024)", eq_gbp_avg("FY2024", (None, None, None, None, 16869, 16869))),
    ("DATA", "Other comprehensive income (2024)", eq_gbp_avg("FY2024", (None, -861, 24, None, -1179, -2016))),
    ("TOTAL", "Total comprehensive income for the year (2024)",
     eq_gbp_avg("FY2024", (None, -861, 24, None, 15690, 14853))),
    ("TOTAL", "Balance at 31 December 2024", eq_gbp_spot("FY2024", (569998, -2706, 143, None, -246271, 321164))),
]

bw.add_equity_changes_sheet(
    title="Arab Bank Europe Plc — Statement of Changes in Equity",
    subtitle="£'000, converted from EUR - Balance rows at each year-end's spot rate, movement rows at that "
             "year's average rate (see FX conversion note at bottom).",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQ_SOURCES,
    first_col_width=90,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw EUR '000 figures, converted at build time)
# ---------------------------------------------------------------
PROFIT_ADJ = {"FY2024": 19444, "FY2023": 12873, "FY2022": 12416, "FY2021": 402}
DEPRECIATION = {"FY2024": 3228, "FY2023": 2990, "FY2022": 1564, "FY2021": 1361}
IMPAIRMENT_LOSS = {"FY2024": 5378, "FY2023": 4608, "FY2022": 4500, "FY2021": 1567}
LOSS_ON_DISPOSAL_FA = {"FY2022": 0, "FY2021": 1056}
LOSS_ON_DISPOSAL_SUB = {"FY2023": 3294}
FX_LOSS_SUBORDINATED = {"FY2024": 7620, "FY2023": -4128, "FY2022": 7053, "FY2021": 7784}
INTEREST_EXP_LEASE = {"FY2024": 411, "FY2023": 505, "FY2022": 379, "FY2021": 46}
TRADING_GAINS = {"FY2024": -1334, "FY2023": -456}
GAIN_LEASE_MOD = {"FY2023": -398}
FX_ADJ_ECL = {"FY2024": 1757, "FY2023": -2328}
FX_ADJ_ROU = {"FY2024": -340}
OPERATING_ADJ_SUBTOTAL = {"FY2024": 36164, "FY2023": 16960, "FY2022": 25912, "FY2021": 12216}

CHG_LOANS_CUSTOMERS = {"FY2024": -99312, "FY2023": -88176, "FY2022": 76970, "FY2021": -31138}
CHG_LOANS_BANKS = {"FY2022": 23398, "FY2021": 207372}
CHG_FVTPL_DERIVATIVES = {"FY2024": -1689, "FY2023": 14110, "FY2022": -19270, "FY2021": 123184}
CHG_FVOCI = {"FY2022": -42644, "FY2021": -86081}
CHG_AMORTISED_COST_INVESTMENTS = {"FY2022": 47594, "FY2021": -86211}
CHG_OTHER_ASSETS = {"FY2024": -4068, "FY2023": -1829, "FY2022": -2717, "FY2021": -6137}
CHG_ASSETS_SUBTOTAL = {"FY2024": -105069, "FY2023": -75895, "FY2022": 83331, "FY2021": 120989}

CHG_CUSTOMER_DEPOSITS = {"FY2024": 231252, "FY2023": -27011, "FY2022": 86445, "FY2021": 75042}
CHG_FUNDS_FROM_BANKS = {"FY2024": -9181, "FY2023": 98566, "FY2022": -218828, "FY2021": -166377}
CHG_OTHER_LIABILITIES = {"FY2024": -768, "FY2023": 4667, "FY2022": 13392, "FY2021": -159}
CHG_LIABILITIES_SUBTOTAL = {"FY2024": 221302, "FY2023": 76222, "FY2022": -118990, "FY2021": -91494}

TAXES_PAID = {"FY2024": -2289, "FY2023": 0, "FY2022": 0, "FY2021": 0}
INTEREST_PAID_LEASE = {"FY2022": -379, "FY2021": -46}
NET_OPERATING = {"FY2024": 150109, "FY2023": 17287, "FY2022": -10126, "FY2021": 41665}

CHG_FVOCI_INVESTING = {"FY2024": -33386, "FY2023": 27277}
CHG_AMORTISED_COST_INVESTING = {"FY2024": -79759, "FY2023": 21229}
ACQUISITION_PPE = {"FY2024": -3251, "FY2023": -2410, "FY2022": -3848, "FY2021": -1674}
DISPOSAL_SUBSIDIARIES = {"FY2023": 25342}
INVESTMENT_IN_SUBSIDIARIES = {"FY2022": 0, "FY2021": 0}
NET_INVESTING = {"FY2024": -116396, "FY2023": 71438, "FY2022": -3848, "FY2021": -1674}

PAYMENT_LEASE_LIABILITIES = {"FY2024": -1178, "FY2023": -803, "FY2022": -1344, "FY2021": -1335}
NET_FINANCING = {"FY2024": -1178, "FY2023": -803, "FY2022": -1344, "FY2021": -1335}

NET_CHANGE = {"FY2024": 32535, "FY2023": 87922, "FY2022": -15318, "FY2021": 38656}
CASH_BEGIN = {"FY2024": 626555, "FY2023": 538633, "FY2022": 174174, "FY2021": 135518}
CASH_END = {"FY2024": 659090, "FY2023": 626555, "FY2022": 158856, "FY2021": 174174}

cash_begin_gbp = gbp_spot_prior(CASH_BEGIN)
cash_end_gbp = gbp_spot(CASH_END)
net_change_gbp = gbp_avg(NET_CHANGE)
# Reconciling line absorbing the spot-vs-average rate differential exactly (see FX_NOTE).
# NOTE: FY2023's translation line also absorbs the genuine, undocumented €379,777k cash-bridge
# gap described in ENTITY_NOTE (FY2022 closing vs FY2023 opening don't reconcile in EUR either) -
# flagged prominently there rather than silently smoothed over.
GBP_TRANSLATION_EFFECT = {
    y: round(cash_end_gbp[y] - cash_begin_gbp[y] - net_change_gbp[y], 1)
    for y in YEARS
}

rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit before tax", gbp_avg(PROFIT_ADJ)),
    ("DATA", "Depreciation", gbp_avg(DEPRECIATION)),
    ("DATA", "Impairment loss expense", gbp_avg(IMPAIRMENT_LOSS)),
    ("DATA", "Loss on disposal/write-off of fixed assets", gbp_avg(LOSS_ON_DISPOSAL_FA)),
    ("DATA", "Loss on disposal of subsidiary", gbp_avg(LOSS_ON_DISPOSAL_SUB)),
    ("DATA", "Net foreign exchange loss/(gain) on subordinated liability", gbp_avg(FX_LOSS_SUBORDINATED)),
    ("DATA", "Interest expense on lease liabilities", gbp_avg(INTEREST_EXP_LEASE)),
    ("DATA", "Trading gains on securities and derivatives", gbp_avg(TRADING_GAINS)),
    ("DATA", "Gain on lease modification", gbp_avg(GAIN_LEASE_MOD)),
    ("DATA", "FX adjustments on expected credit losses", gbp_avg(FX_ADJ_ECL)),
    ("DATA", "FX adjustments on right-of-use assets", gbp_avg(FX_ADJ_ROU)),
    ("TOTAL", "Profit before tax, adjusted for non-cash items - subtotal", gbp_avg(OPERATING_ADJ_SUBTOTAL)),
    ("SECTION", "Decrease/(Increase) in operating and other assets", {}),
    ("DATA", "Loans advanced to customers", gbp_avg(CHG_LOANS_CUSTOMERS)),
    ("DATA", "Loans advanced to banks", gbp_avg(CHG_LOANS_BANKS)),
    ("DATA", "Fair value through profit or loss and derivatives", gbp_avg(CHG_FVTPL_DERIVATIVES)),
    ("DATA", "Fair value through other comprehensive income", gbp_avg(CHG_FVOCI)),
    ("DATA", "Financial investments at amortised cost", gbp_avg(CHG_AMORTISED_COST_INVESTMENTS)),
    ("DATA", "Other assets", gbp_avg(CHG_OTHER_ASSETS)),
    ("TOTAL", "Decrease/(Increase) in operating and other assets - subtotal", gbp_avg(CHG_ASSETS_SUBTOTAL)),
    ("SECTION", "(Decrease)/Increase in operating and other liabilities", {}),
    ("DATA", "Customer deposits", gbp_avg(CHG_CUSTOMER_DEPOSITS)),
    ("DATA", "Funds received from banks", gbp_avg(CHG_FUNDS_FROM_BANKS)),
    ("DATA", "Other liabilities and retirement benefit liabilities", gbp_avg(CHG_OTHER_LIABILITIES)),
    ("TOTAL", "(Decrease)/Increase in operating and other liabilities - subtotal", gbp_avg(CHG_LIABILITIES_SUBTOTAL)),
    ("DATA", "Income taxes paid", gbp_avg(TAXES_PAID)),
    ("DATA", "Interest paid on lease liabilities", gbp_avg(INTEREST_PAID_LEASE)),
    ("TOTAL", "Net cash (outflows)/inflows from operating activities", gbp_avg(NET_OPERATING)),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Fair value through other comprehensive income (investing)", gbp_avg(CHG_FVOCI_INVESTING)),
    ("DATA", "Financial investments at amortised cost (investing)", gbp_avg(CHG_AMORTISED_COST_INVESTING)),
    ("DATA", "Acquisition of property, plant and equipment", gbp_avg(ACQUISITION_PPE)),
    ("DATA", "Disposal of subsidiaries", gbp_avg(DISPOSAL_SUBSIDIARIES)),
    ("DATA", "Investment in subsidiaries", gbp_avg(INVESTMENT_IN_SUBSIDIARIES)),
    ("TOTAL", "Net cash (outflows)/inflows from investing activities", gbp_avg(NET_INVESTING)),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payment of lease liabilities", gbp_avg(PAYMENT_LEASE_LIABILITIES)),
    ("TOTAL", "Net cash outflows from financing activities", gbp_avg(NET_FINANCING)),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", net_change_gbp),
    ("DATA", "Effect of GBP/EUR translation (£ conversion artefact - see FX note; FY2023 also absorbs an "
             "undocumented cash-bridge gap, see ENTITY_NOTE)", GBP_TRANSLATION_EFFECT),
    ("DATA", "Cash and cash equivalents at 1 January", cash_begin_gbp),
    ("TOTAL", "Cash and cash equivalents at 31 December", cash_end_gbp),
]

bw.add_cash_flow_sheet(
    title="Arab Bank Europe Plc — Cash Flow Statement",
    subtitle="£'000, converted from EUR - see source note at bottom for FX methodology and rates used.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=80,
    source_height=380,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# Asset Quality (loans and advances to customers only - see AQ_SOURCES for
# why no by-product split exists)
# ---------------------------------------------------------------
AQ_STAGE1_GROSS = {"FY2024": 976718, "FY2023": 850363, "FY2022": 773748, "FY2021": 829249}
AQ_STAGE2_GROSS = {"FY2024": 21996, "FY2023": 20240, "FY2022": 4108, "FY2021": 34421}
AQ_STAGE3_GROSS = {"FY2024": 52629, "FY2023": 91057, "FY2022": 122535, "FY2021": 110803}
AQ_GROSS_TOTAL = {"FY2024": 1051343, "FY2023": 961660, "FY2022": 900391, "FY2021": 974473}
AQ_STAGE1_ECL = {"FY2024": 3155, "FY2023": 5759, "FY2022": 6944, "FY2021": 2732}
AQ_STAGE2_ECL = {"FY2024": 50, "FY2023": 55, "FY2022": 41, "FY2021": 3859}
AQ_STAGE3_ECL = {"FY2024": 32987, "FY2023": 33240, "FY2022": 55032, "FY2021": 48038}
AQ_ECL_TOTAL = {"FY2024": 36192, "FY2023": 39054, "FY2022": 62017, "FY2021": 54629}
AQ_INTEREST_RECEIVABLE = {"FY2024": 8653, "FY2023": 8697}
AQ_NET = {"FY2024": 1023804, "FY2023": 931303, "FY2022": 838374, "FY2021": 919844}

AQ_ECL_COVERAGE = {y: f"{AQ_ECL_TOTAL[y] / AQ_GROSS_TOTAL[y] * 100:.2f}%" for y in YEARS}
AQ_NPL_RATIO = {y: f"{AQ_STAGE3_GROSS[y] / AQ_GROSS_TOTAL[y] * 100:.2f}%" for y in YEARS}
AQ_STAGE3_COVERAGE = {y: f"{AQ_STAGE3_ECL[y] / AQ_STAGE3_GROSS[y] * 100:.2f}%" for y in YEARS}

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers by IFRS 9 stage (gross, £'000)", {}),
    ("DATA", "Stage 1 (performing)", gbp_spot(AQ_STAGE1_GROSS)),
    ("DATA", "Stage 2 (underperforming / significant increase in credit risk)", gbp_spot(AQ_STAGE2_GROSS)),
    ("DATA", "Stage 3 (credit-impaired / non-performing)", gbp_spot(AQ_STAGE3_GROSS)),
    ("TOTAL", "Gross loans and advances to customers", gbp_spot(AQ_GROSS_TOTAL)),
    ("SECTION", "Expected credit loss (ECL) allowance by stage (£'000)", {}),
    ("DATA", "Stage 1 ECL", gbp_spot(AQ_STAGE1_ECL)),
    ("DATA", "Stage 2 ECL", gbp_spot(AQ_STAGE2_ECL)),
    ("DATA", "Stage 3 ECL", gbp_spot(AQ_STAGE3_ECL)),
    ("TOTAL", "Total ECL allowance", gbp_spot(AQ_ECL_TOTAL)),
    ("DATA", "Interest receivable (added after ECL - FY2023/FY2024 presentation only, see AQ_SOURCES)",
     gbp_spot(AQ_INTEREST_RECEIVABLE)),
    ("TOTAL", "Net loans and advances to customers", gbp_spot(AQ_NET)),
    ("SECTION", "Asset quality ratios (computed from £-converted figures above)", {}),
    ("DATA", "ECL coverage ratio (Total ECL / Gross loans)", AQ_ECL_COVERAGE),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / Gross loans)", AQ_NPL_RATIO),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", AQ_STAGE3_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="Arab Bank Europe Plc — Asset Quality / Credit Risk Disclosures",
    subtitle="£'000, converted from EUR at each year's period-end spot rate - loans and advances to customers "
             "only (see source note for why no by-product split is disclosed).",
    rows=asset_quality_rows,
    sources_text=AQ_SOURCES,
    first_col_width=78,
    source_height=220,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets. FY2023/FY2024 still have only the Annual Report's two
# headline ratios (see ENTITY_NOTE). FY2021/FY2022 now have full entity-level
# (EAB plc solo) capital/RWA/leverage/LCR/NSFR amounts, recovered 2026-09-07
# (HD-081 item 4 re-check) from the standalone Pillar3.pdf that was previously
# found archived but corrupted on every download attempt - see ENTITY_NOTE and
# PILLAR3_SOURCES below.
# ---------------------------------------------------------------
RATIO_PAGES = {"FY2024": "6", "FY2022": "9"}

# More precise than the AR's rounded whole-percent KPI table, since FY2021/FY2022
# are now sourced from the Pillar3.pdf's own "EAB plc**" (entity-only) column
# instead - see PILLAR3_SOURCES. FY2023/FY2024 unchanged (AR KPI table only).
TOTAL_CAPITAL_RATIO = {"FY2024": "23%", "FY2023": "24%", "FY2022": "22.7%", "FY2021": "22.4%"}
CET1_RATIO = {"FY2024": "16%", "FY2023": "17%", "FY2022": "15.5%", "FY2021": "15.6%"}

# EAB plc (entity-only, "**" column) figures from Pillar3.pdf's "Overview of key
# metrics" table, EURm as published, held here before £'000 conversion.
P3_CET1_CAPITAL_EUR = {"FY2022": 253000, "FY2021": 252000}
P3_TIER1_CAPITAL_EUR = {"FY2022": 253000, "FY2021": 252000}  # AT1 = nil both years
P3_TOTAL_CAPITAL_EUR = {"FY2022": 370000, "FY2021": 362000}
P3_TOTAL_RWA_EUR = {"FY2022": 1631000, "FY2021": 1616000}
p3_cet1_capital_gbp = gbp_spot(P3_CET1_CAPITAL_EUR)
p3_tier1_capital_gbp = gbp_spot(P3_TIER1_CAPITAL_EUR)
p3_total_capital_gbp = gbp_spot(P3_TOTAL_CAPITAL_EUR)
p3_total_rwa_gbp = gbp_spot(P3_TOTAL_RWA_EUR)

# Leverage ratio and NSFR are both flagged 'n/a' in Pillar3.pdf's own FY2021
# comparative column - the PRA's leverage/NSFR disclosure templates only took
# effect from 1 Jan 2022, so no FY2021 comparative was ever produced (not a
# gap in sourcing - the document itself says so). LCR has both years.
LEVERAGE_RATIO = {"FY2024": "Not publicly disclosed", "FY2023": "Not publicly disclosed",
                   "FY2022": "11.7%", "FY2021": "Not publicly disclosed"}
LCR_RATIO = {"FY2024": "Not publicly disclosed", "FY2023": "Not publicly disclosed",
             "FY2022": "218%", "FY2021": "267%"}
NSFR_RATIO = {"FY2024": "Not publicly disclosed", "FY2023": "Not publicly disclosed",
              "FY2022": "120%", "FY2021": "Not publicly disclosed"}

PILLAR3_SOURCES = (
    "FY2022/FY2021 (this row only): Europe Arab Bank plc's standalone Pillar 3 Disclosures as at 31 December "
    "2022, PDF page 8 of 35 ('Overview of key metrics' table), 'EAB plc**' entity-only column (** = 'EAB plc "
    "regulatory numbers are based on entity only basis', per the document's own footnote) - not the wider 'EAB "
    "Group' column, for consistency with every other sheet in this workbook, which is entity-only throughout. "
    f"{PILLAR3_2022_URL}\n"
    "Recovered 2026-09-07 (HD-081 item 4 re-check) - this document was previously found archived at the same "
    "Wayback URL but was corrupted/truncated on every earlier download attempt; it now downloads intact as a "
    "readable 35-page PDF. No equivalent standalone document could be found for FY2023 or FY2024 (see "
    "ENTITY_NOTE).\n\n"
    + BASIS_NOTE
)


def metric(name, unit, rows_data, note=None, extra_sources=None):
    sources = p3_sources(RATIO_PAGES) + (("\n\n" + extra_sources) if extra_sources else "")
    bw.add_metric_sheet(name, f"Entity-level basis, {unit}" if unit else "Entity-level basis",
                         rows_data, sources, note=note,
                         first_col_width=46, source_height=140)


NOT_DISCLOSED_NOTE = (
    "Not disclosed in any of the two sourced Annual Reports (FY2021/FY2022 or FY2023/FY2024) - the Bank's only "
    "capital/liquidity disclosure is the 'Other Key Performance Indicators' table's two headline ratios (Capital "
    "adequacy ratio, Common Equity Tier 1 ratio). No standalone Pillar 3 document was obtainable (see ENTITY_NOTE "
    "on the Cash Flow Statement sheet) and no other figure for this metric appears anywhere in either report.\n"
    + SDDT_NOTE
)

FY2324_ONLY_NOTE = (
    "FY2021/FY2022 now sourced from the recovered standalone Pillar3.pdf (see PILLAR3_SOURCES below and "
    "ENTITY_NOTE). FY2023/FY2024 remain 'Not publicly disclosed' - the Bank's only capital disclosure for those "
    "two years is the Annual Report's 'Other Key Performance Indicators' table's two headline ratios (Capital "
    "adequacy ratio, Common Equity Tier 1 ratio); no standalone Pillar 3 document could be recovered for either "
    "year despite a re-check of both eabplc.com/arabbankeurope.com directly and a broader Wayback CDX search "
    "(2026-09-07, HD-081 item 4), re-confirmed independently 2026-09-15.\n"
    + SDDT_NOTE
)

metric("CET1 Capital", None,
       [("Common Equity Tier 1 (CET1) capital (£'000)",
         {"FY2024": "Not publicly disclosed", "FY2023": "Not publicly disclosed",
          "FY2022": p3_cet1_capital_gbp["FY2022"], "FY2021": p3_cet1_capital_gbp["FY2021"]})],
       note=FY2324_ONLY_NOTE, extra_sources=PILLAR3_SOURCES)

metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CET1_RATIO)],
       note="FY2021/FY2022 values (15.6%/15.5%) are the recovered Pillar3.pdf's own precise figures on the "
            "same 'EAB plc' entity-only basis, rather than the Annual Report's rounded whole-percent KPI table "
            "(which shows 16% for both years) - both are the Bank's own disclosures and are consistent once "
            "rounded, so the more precise source is preferred. FY2023/FY2024 (17%/16%) remain from the Annual "
            "Report's KPI table, the only source found for those two years.",
       extra_sources=PILLAR3_SOURCES)

metric("Tier 1 Capital", None,
       [("Tier 1 capital (£'000)",
         {"FY2024": "Not publicly disclosed", "FY2023": "Not publicly disclosed",
          "FY2022": p3_tier1_capital_gbp["FY2022"], "FY2021": p3_tier1_capital_gbp["FY2021"]})],
       note=FY2324_ONLY_NOTE + " Additional Tier 1 (AT1) capital is nil in both FY2021 and FY2022 per Pillar3.pdf, "
                               "so Tier 1 = CET1 exactly in those two years.",
       extra_sources=PILLAR3_SOURCES)

metric("Tier 1 Ratio", None,
       [("Tier 1 ratio",
         {"FY2024": "Not publicly disclosed", "FY2023": "Not publicly disclosed",
          "FY2022": "15.5%", "FY2021": "15.6%"})],
       note=FY2324_ONLY_NOTE + " Tier 1 ratio = CET1 ratio in both FY2021 and FY2022 since AT1 is nil (see Tier 1 "
                               "Capital sheet). For FY2023/FY2024, the KPI table's 'Capital adequacy ratio' is "
                               "Total Capital, not Tier 1 - not substituted here since that would misrepresent a "
                               "different metric.",
       extra_sources=PILLAR3_SOURCES)

metric("Total Capital", None,
       [("Total capital (£'000)",
         {"FY2024": "Not publicly disclosed", "FY2023": "Not publicly disclosed",
          "FY2022": p3_total_capital_gbp["FY2022"], "FY2021": p3_total_capital_gbp["FY2021"]})],
       note=FY2324_ONLY_NOTE, extra_sources=PILLAR3_SOURCES)

metric("Total Capital Ratio", "% of RWA", [("Capital adequacy (Total Capital) ratio", TOTAL_CAPITAL_RATIO)],
       note="FY2021/FY2022 values (22.4%/22.7%) are the recovered Pillar3.pdf's own precise figures on the "
            "same 'EAB plc' entity-only basis, rather than the Annual Report's rounded whole-percent KPI table "
            "(which shows 22%/23%) - both are the Bank's own disclosures and are consistent once rounded, so "
            "the more precise source is preferred. FY2023/FY2024 (24%/23%) remain from the Annual Report's KPI "
            "table, the only source found for those two years.",
       extra_sources=PILLAR3_SOURCES)

metric("Total RWAs", "£'000",
       [("Total risk-weighted assets (£'000)",
         {"FY2024": "Not publicly disclosed", "FY2023": "Not publicly disclosed",
          "FY2022": p3_total_rwa_gbp["FY2022"], "FY2021": p3_total_rwa_gbp["FY2021"]})],
       note=FY2324_ONLY_NOTE, extra_sources=PILLAR3_SOURCES)

# EAB plc (entity-only) RWA breakdown from Pillar3.pdf's "Overview of RWA" table
# (UK OV1-style split by risk category), EURm as published.
RWA_BREAKDOWN_EUR = {
    "Credit risk (excluding counterparty credit risk)": {"FY2022": 1382000, "FY2021": 1376000},
    "Counterparty credit risk": {"FY2022": 12000, "FY2021": 4000},
    "Credit valuation adjustment": {"FY2022": 1000, "FY2021": 10000},
    "Securitisation exposures in the non-trading book": {"FY2022": 163000, "FY2021": 168000},
    "Position, foreign exchange and commodities risks": {"FY2022": 6000, "FY2021": 0},
    "Operational risk": {"FY2022": 67000, "FY2021": 57000},
}
bw.add_rwa_breakdown_sheet(
    title="Arab Bank Europe Plc — RWA Breakdown",
    subtitle="Entity-level basis",
    rows=(
        [("DATA", label, gbp_spot(eur)) for label, eur in RWA_BREAKDOWN_EUR.items()]
        + [("TOTAL", "Total risk-weighted assets", {y: p3_total_rwa_gbp[y] for y in ("FY2022", "FY2021")})]
    ),
    sources_text=(
        "FY2022/FY2021: recovered Pillar3.pdf's 'Overview of RWA' table, 'EAB PLC' entity-only RWA columns "
        "(not the 'EAB Group' columns, for consistency with the rest of this workbook), converted from EUR to "
        "£'000 at each year's period-end spot rate. " + PILLAR3_SOURCES + "\n\n"
        "FY2023/FY2024: " + RWA_NOT_DISCLOSED_NOTE
    ),
    first_col_width=54,
    source_height=200,
)

metric("Leverage Ratio", None,
       [("Leverage ratio excluding claims on central banks", LEVERAGE_RATIO)],
       note="FY2022 only - Pillar3.pdf's own FY2021 comparative is flagged 'n/a': the PRA's leverage ratio "
            "disclosure template only took effect from 1 Jan 2022, so no FY2021 comparative was ever produced "
            "(not a sourcing gap). FY2023/FY2024: " + NOT_DISCLOSED_NOTE,
       extra_sources=PILLAR3_SOURCES)

metric("LCR", None, [("Liquidity Coverage Ratio (12-month average basis)", LCR_RATIO)],
       note="BASIS: these are 12-MONTH AVERAGE LCRs, not point-in-time. The source document's own footnote 3 "
            "states verbatim: 'The weighted values represent the simple average of the 12 preceding month-end "
            "observations used to calculate the LCR.' They are therefore NOT comparable with a point-in-time "
            "year-end LCR of the kind annual reports usually quote, and must never be merged into one series "
            "with one. The underlying EAB plc solo components are HQLA EUR291m/EUR355m, net cash outflows "
            "EUR137m/EUR137m for FY2022/FY2021. FY2023/FY2024: " + NOT_DISCLOSED_NOTE,
       extra_sources=PILLAR3_SOURCES)

metric("NSFR", None, [("Net Stable Funding Ratio", NSFR_RATIO)],
       note="FY2022 only - Pillar3.pdf's own FY2021 comparative is flagged 'n/a': the PRA's NSFR disclosure "
            "template only took effect from 1 Jan 2022, so no FY2021 comparative was ever produced (not a "
            "sourcing gap). FY2023/FY2024: " + NOT_DISCLOSED_NOTE,
       extra_sources=PILLAR3_SOURCES)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(RATIO_PAGES) + "\n\n" + PILLAR3_SOURCES,
    per_note={
        "MREL Ratio": NOT_DISCLOSED_NOTE + " Not disclosed in the recovered Pillar3.pdf either (no MREL section "
                                            "anywhere in that document) - EAB plc is likely below the MREL "
                                            "threshold that would require this disclosure. MREL is the one "
                                            "metric here whose absence is plausibly structural rather than a "
                                            "withheld disclosure; every other blank metric is not (see the "
                                            "SDDT note above).",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
# Equity bridge headline block: Opening/Closing at that year's spot rate, Total
# comprehensive income at that year's average rate, Other movements as the
# residual (absorbs the spot/average FX differential - see FX_NOTE; genuinely
# ~0 in EUR-native terms per the Statement of Changes in Equity sheet).
EQ_OPENING_EUR = {"FY2021": 275321, "FY2022": 293238, "FY2023": 295854, "FY2024": 306311}
EQ_CLOSING_EUR = {"FY2021": 293238, "FY2022": 295854, "FY2023": 306311, "FY2024": 321164}
eq_opening_gbp = gbp_spot_prior(EQ_OPENING_EUR)
eq_closing_gbp = gbp_spot(EQ_CLOSING_EUR)
eq_tci_gbp = gbp_avg(TOTAL_COMPREHENSIVE_INCOME)
eq_other_gbp = {y: round(eq_closing_gbp[y] - eq_opening_gbp[y] - eq_tci_gbp[y], 1) for y in YEARS}

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", gbp_spot(BS_TOTAL_ASSETS)),
        ("Loans and advances to customers", gbp_spot(BS_LOANS_CUSTOMERS)),
        ("Customer accounts", gbp_spot(BS_CUSTOMER_ACCOUNTS)),
        ("Total equity", gbp_spot(BS_TOTAL_EQUITY)),
    ],
    balance_sheet_unit="£'000 (conv. from EUR)",
    income_statement_totals=[
        ("Net Operating Income", gbp_avg(IS_NET_OPERATING_INCOME)),
        ("Total operating expenses before impairment losses", gbp_avg(IS_TOTAL_OPEX)),
        ("Profit for the year", gbp_avg(IS_PROFIT_FOR_YEAR)),
    ],
    income_statement_unit="£'000 (conv. from EUR)",
    equity_changes_totals=[
        ("Opening equity", eq_opening_gbp),
        ("Total comprehensive income", eq_tci_gbp),
        ("Other movements, net", eq_other_gbp),
        ("Closing equity", eq_closing_gbp),
    ],
    equity_changes_unit="£'000 (conv. from EUR)",
    cash_flow_totals=[
        ("Net cash (outflows)/inflows from operating activities", gbp_avg(NET_OPERATING)),
        ("Net cash (outflows)/inflows from investing activities", gbp_avg(NET_INVESTING)),
        ("Net cash outflows from financing activities", gbp_avg(NET_FINANCING)),
        ("Cash and cash equivalents at 31 December", cash_end_gbp),
    ],
    cash_flow_unit="£'000 (conv. from EUR)",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing (spend and risk lens: "
         "Balance Sheet/P&L/Equity blocks show where the bank's money goes and how it runs itself; Pillar 3 "
         "ratios and Asset Quality - see that sheet - show the risk it's taking). ALL £ figures in this "
         "workbook are converted from Arab Bank Europe Plc's (Europe Arab Bank plc's) native EUR reporting - see "
         "the Cash Flow Statement sheet's source note for the full FX methodology and exact rates used. Ratios "
         "(%) are shown exactly as reported in EUR and were not converted. Only 2 of the usual 6 headline ratios "
         "are plotted here (CET1 Ratio, Total Capital Ratio, both disclosed for all 4 years) - Tier 1 Ratio, "
         "Leverage Ratio, LCR and NSFR are only disclosed for FY2021/FY2022 (LCR)/FY2022 (Leverage, NSFR), via a "
         "recovered standalone Pillar 3 document, and not at all for FY2023/FY2024, see the individual Pillar 3 "
         "sheets and ENTITY_NOTE for why. FY2025 is excluded entirely - its Annual Report was found on a "
         "2026-09-07 re-check but not yet incorporated (see ENTITY_NOTE for why). 'Other movements, net' in "
         "the equity bridge absorbs the FX spot/average rate differential (near-zero in EUR-native terms).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ARAB BANK EUROPE FINANCIALS.xlsx")
