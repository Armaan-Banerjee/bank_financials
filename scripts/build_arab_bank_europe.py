import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Arab Bank Europe Plc (Companies House / trading name "Europe Arab Bank plc",
# company 05575857, FRN 446951) reports in EUR (its functional currency) - this
# workbook converts every € figure to £ at the established FX methodology (see
# FX_NOTE below). FY2021-FY2025 are sourced; FY2025 was added 2026-09-18 under
# GA-003 from the bank's own FY2025 Annual Report, which an earlier re-check had
# found but not incorporated. Ratios are never converted.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

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

# FY2025 Annual Report - LIVE on the bank's own migrated host, not an archive copy.
# Re-verified 2026-09-18 (GA-003): HTTP 200, Content-Type application/pdf,
# %PDF-1.7 magic bytes, 1,778,036 bytes, 111pp, PDF produced 15 April 2026,
# financial statements signed 27 February 2026. Reached directly; the migrated
# site exposes no document index page, so the resolved CDN path is recorded here.
# The human-facing route is https://arabbankeurope.com/downloads/annual-report-2025/.
AR2025_URL = "https://arabbankeurope.com/wp-content/uploads/202602_EABAnnualReport_v9.pdf"

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
    # FY2025 added 2026-09-18 (GA-003). Same pair already used for FY2025 in
    # build_bank_saderat.py, this project's other EUR-reporting bank: the
    # period-end spot is the BoE archive figure for 31 December 2025; the
    # average is a mid-month-sample estimate rather than a full daily mean and
    # is flagged as approximate in FX_NOTE.
    "FY2025": {"period_end": 1.1454, "average": 1.168},
}
PRIOR_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023",
              "FY2025": "FY2024"}


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
    "average 1.1717; FY2023 spot 1.1539 / average 1.1520; FY2024 spot 1.2099 / average 1.1824; FY2025 spot "
    "1.1454 / average 1.168. THE FY2025 AVERAGE IS APPROXIMATE - it is a mid-month-sample estimate rather than "
    "a full daily mean (the same figure already used for FY2025 in this project's other EUR-reporting bank, "
    "Bank Saderat), so FY2025 flow figures carry slightly more conversion uncertainty than the balance figures, "
    "whose 31 December 2025 spot rate is exact. All % ratios (CET1/"
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
    "NAME CHANGE (recorded 2026-09-19 from the Companies House filing history): the company was renamed from "
    "EUROPE ARAB BANK PLC to ARAB BANK EUROPE PLC by resolution of 1 July 2026 (RES15), with the certificate of "
    "incorporation on change of name issued 14 July 2026, so the registered name now matches the PRA list's word "
    "order. The entity is unchanged (company 05575857, FRN 446951). Every document cited in this workbook "
    "predates the change and was published under the former name 'Europe Arab Bank plc', which is why the "
    "citations use it. "
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
    "re-check. THE FY2025 ANNUAL REPORT IS NOW INCORPORATED (18 September 2026, GA-003). It was found live on a "
    "2026-09-07 re-check at arabbankeurope.com/downloads/annual-report-2025/ but left out of the workbook at "
    "that time because adding a fifth year needs a full statement transcription across every sheet; that "
    "transcription has now been done and YEARS runs FY2021-FY2025. The document is 111pp, signed 27 February "
    "2026, PDF produced 15 April 2026, and Companies House records the FY2025 filing on 10 May 2026. It was "
    "re-fetched 2026-09-18 straight from the bank's own host and verified HTTP 200 / Content-Type "
    "application/pdf / %PDF-1.7 magic bytes. Note the consequence for the Pillar 3 sheets: FY2025 brings a "
    "THIRD year of Annual-Report-only disclosure, so FY2023, FY2024 and FY2025 each carry just the two "
    "headline KPI ratios. The generic 'Pillar3.pdf' previously found archived but truncated/corrupted "
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
    f"FY2025: Europe Arab Bank plc Annual Report and Financial Statements 2025, p.32 (Statement of Cash Flows) "
    f"- {AR2025_URL}\n"
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
        f"FY2025: Annual Report and Financial Statements 2025, p.{page['FY2025']} - {AR2025_URL}\n"
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
    f"FY2025: Annual Report and Financial Statements 2025, p.30 (Statement of Financial Position) - {AR2025_URL}\n"
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
    f"FY2025: Annual Report and Financial Statements 2025, pp.28-29 (Income Statement; Statement of "
    f"Comprehensive Income) - {AR2025_URL}\n"
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
    f"FY2025: Annual Report and Financial Statements 2025, p.31 - {AR2025_URL}\n"
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
    f"FY2025: Annual Report and Financial Statements 2025, pp.59-60 (Note 17 'Loans and advances to customers', "
    f"internal-rating-grade stage table and ECL allowance roll-forward) - {AR2025_URL}\n"
    f"FY2024/FY2023: Annual Report and Financial Statements 2024, pp.75-76 (Note 33, Credit risk, Quality of "
    f"Assets) - {AR2024_URL}\n"
    f"FY2022/FY2021: Annual Report and Financial Statements 2022, pp.72-73 (Note 34, Credit risk, Quality of "
    f"Assets) - {AR2022_URL}\n"
    "No by-product split is disclosed anywhere in either report - only the by-IFRS-9-stage breakdown shown here. "
    "FY2023/FY2024's table separately discloses an 'Interest Receivable' amount added after ECL to reach the net "
    "figure; FY2021/FY2022's table has no such line (net = gross - ECL exactly that year) - left blank for "
    "FY2021/FY2022 rather than forced to zero. Ratios (ECL coverage, Stage 3/NPL, Stage 3 coverage) are computed "
    "from the £-converted gross/ECL figures above, consistent with this project's convention "
    "elsewhere.\n"
    "FY2025 COMES FROM A DIFFERENT NOTE IN A RESTRUCTURED REPORT, and its FY2024 comparative disagrees with the "
    "FY2024 column here. The FY2025 Annual Report moves this disclosure out of the credit-risk note and into "
    "Note 17 'Loans and advances to customers', where the same stage split is given by internal rating grade "
    "(1-3 investment grade, 4-5 standard monitoring, 6 special monitoring, 7 watch, 8-10 classified) with a "
    "separate ECL roll-forward. Its FY2024 comparative reads Stage 1 €976,718k / Stage 2 €21,996k / Stage 3 "
    "€49,225k, total €1,047,939k - Stage 3 restated down €3,404k from the €52,629k the FY2024 report itself "
    "printed. The FY2024 column above is the FY2024 report's own figure, per this project's "
    "each-year-from-its-own-edition rule; the restated comparative is recorded here rather than substituted.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
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
    "Not disclosed in any sourced Annual Report (FY2021/FY2022, FY2023/FY2024 or FY2025) - the Bank's only capital "
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
    "QUALIFIED 2026-09-18 (GA-018): the sentence immediately above draws the line in the wrong place and should "
    "be read with the KM1 sheet's note, which supersedes it. 'A genuine availability gap' is right; 'rather than "
    "a document this session failed to fetch' overstates it, because nothing here establishes that EAB did not "
    "PUBLISH a FY2023/FY2024/FY2025 Pillar 3 - only that no copy can now be obtained. Two findings from today "
    "point the other way: the live site still carries a published downloads entry titled 'Pillar III Disclosures' "
    "whose file field is literally null (so the link 302s to the homepage, while the sibling Annual Report entry "
    "301s to a real PDF), and every Annual Report states that the Pillar 3 ratios 'are published on EAB's "
    "website'. Europe Arab Bank plc (FRN 446951) also holds NO SDDT Rule 3.1 modification, so the disclosure duty "
    "stood in all three years. This is an UNREACHED gap, not an established absence, and it must stay visible "
    "as one: the cells were left EMPTY until 2026-09-19 and now carry the reserved 'Unreached today' phrase "
    "in one status row below the TOTAL (GA-020).\n"
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
    "behind the request.\n"
    "LATEST-EDITION CHECK RE-RUN 18 SEPTEMBER 2026 (GA-003), BY ENUMERATION AGAIN RATHER THAN BY GUESSING "
    "FILENAMES. The bank's WordPress media REST endpoint (/wp-json/wp/v2/media?mime_type=application/pdf) "
    "enumerates the ENTIRE uploaded file set - 64 PDFs - and exactly one of them is any kind of financial "
    "report: 202602_EABAnnualReport_v9.pdf, the FY2025 Annual Report now incorporated into this workbook. NOT "
    "ONE is a Pillar 3 document. The hidden downloads index (/sitemap.xml chaining to "
    "/eab_download-sitemap.xml) still lists the slug /downloads/pillar-iii-disclosures/, which still resolves "
    "HTTP 200 and still carries no attached file: the slug survived the site migration and the document did "
    "not. So the FY2025 position is the same as FY2023 and FY2024 - newest Annual Report FY2025 (published "
    "February 2026, the bank's normal ~2-month lag), newest Pillar 3 still the FY2022 edition, which exists "
    "now only as a Wayback capture. No FY2026 Annual Report would be expected before about February 2027."
)

# --- Balance Sheet ---
BS_CASH = {"FY2025": 371417, "FY2024": 224962, "FY2023": 136982, "FY2022": 158856, "FY2021": 174174}
BS_DUE_FROM_BANKS = {"FY2025": 390065, "FY2024": 434129, "FY2023": 489573, "FY2022": 379561, "FY2021": 402958}
BS_FVTPL = {"FY2025": 3384, "FY2024": 9812, "FY2023": 9463, "FY2022": 12565, "FY2021": 30911}
BS_FVOCI = {"FY2025": 239944, "FY2024": 134834, "FY2023": 101448, "FY2022": 128725, "FY2021": 86082}
BS_LOANS_CUSTOMERS = {"FY2025": 1064684, "FY2024": 1023804, "FY2023": 931303, "FY2022": 838374, "FY2021": 919844}
BS_AMORTISED_COST = {"FY2025": 519028, "FY2024": 515123, "FY2023": 434776, "FY2022": 450135, "FY2021": 497729}
BS_DERIVATIVE_ASSETS = {"FY2025": 12892, "FY2024": 41899, "FY2023": 38935, "FY2022": 52987, "FY2021": 5648}
BS_INVESTMENT_SUBS = {"FY2025": 75000, "FY2024": 75000, "FY2023": 75000, "FY2022": 103636, "FY2021": 113081}
BS_PPE = {"FY2025": 7950, "FY2024": 7884, "FY2023": 6810, "FY2022": 6269, "FY2021": 3985}
BS_ROU = {"FY2025": 5629, "FY2024": 6494, "FY2023": 7205, "FY2022": 8246, "FY2021": 2828}
BS_OTHER_ASSETS = {"FY2025": 23888, "FY2024": 10557, "FY2023": 6489, "FY2022": 17946, "FY2021": 20647}
BS_DEFERRED_TAX = {"FY2025": 5775, "FY2024": 5775, "FY2023": 5776, "FY2022": 5775, "FY2021": 5768}
BS_TOTAL_ASSETS = {"FY2025": 2719656, "FY2024": 2490273, "FY2023": 2243760, "FY2022": 2163075, "FY2021": 2263655}

BS_DEPOSITS_BANKS = {"FY2025": 834596, "FY2024": 541985, "FY2023": 551167, "FY2022": 449827, "FY2021": 668654}
BS_CUSTOMER_ACCOUNTS = {"FY2025": 1399952, "FY2024": 1460718, "FY2023": 1229466, "FY2022": 1250949, "FY2021": 1164504}
BS_DERIVATIVE_LIAB = {"FY2025": 7918, "FY2024": 17389, "FY2023": 15765, "FY2022": 19265, "FY2021": 9542}
BS_OTHER_LIAB = {"FY2025": 16719, "FY2024": 13004, "FY2023": 13899, "FY2022": 17230, "FY2021": 8616}
BS_CURRENT_TAX_LIAB = {"FY2025": 895, "FY2024": 2197, "FY2023": 1700}
BS_LEASE_LIAB = {"FY2025": 7296, "FY2024": 8683, "FY2023": 9450, "FY2022": 9350, "FY2021": 2963}
BS_RETIREMENT = {"FY2025": 1426, "FY2024": 4610, "FY2023": 3100, "FY2022": 3570, "FY2021": 6161}
BS_SUBORDINATED = {"FY2025": 106592, "FY2024": 120523, "FY2023": 112902, "FY2022": 117030, "FY2021": 109977}
BS_TOTAL_LIAB = {"FY2025": 2375394, "FY2024": 2169109, "FY2023": 1937449, "FY2022": 1867221, "FY2021": 1970417}

BS_SHARE_CAPITAL = {"FY2025": 569998, "FY2024": 569998, "FY2023": 569998, "FY2022": 569998, "FY2021": 569998}
BS_RETAINED_EARNINGS = {"FY2025": -226147, "FY2024": -246271, "FY2023": -261961, "FY2022": -263479, "FY2021": -276880}
BS_FX_RESERVE = {"FY2022": -16, "FY2021": -13}
BS_FV_RESERVE = {"FY2025": -309, "FY2024": -2706, "FY2023": -1845, "FY2022": -10516, "FY2021": 26}
BS_CFH_RESERVE = {"FY2025": 720, "FY2024": 143, "FY2023": 119, "FY2022": -133, "FY2021": 107}
BS_TOTAL_EQUITY = {"FY2025": 344262, "FY2024": 321164, "FY2023": 306311, "FY2022": 295854, "FY2021": 293238}

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
IS_INTEREST_INCOME = {"FY2025": 109179, "FY2024": 116296, "FY2023": 96392, "FY2022": 56397, "FY2021": 32406}
IS_OTHER_INTEREST_INCOME = {"FY2025": 7767, "FY2024": 15926, "FY2023": 15880, "FY2022": 428, "FY2021": 1763}
IS_INTEREST_EXPENSE = {"FY2025": -66773, "FY2024": -80363, "FY2023": -64758, "FY2022": -23303, "FY2021": -5033}
IS_OTHER_INTEREST_EXPENSE = {"FY2022": -1019, "FY2021": -6866}
IS_NET_INTEREST_INCOME = {"FY2025": 50173, "FY2024": 51859, "FY2023": 47514, "FY2022": 32503, "FY2021": 22270}
IS_FEE_INCOME = {"FY2025": 5632, "FY2024": 5114, "FY2023": 5308, "FY2022": 6330, "FY2021": 6873}
IS_FEE_EXPENSE = {"FY2025": -536, "FY2024": -507, "FY2023": -608, "FY2022": -564, "FY2021": -605}
IS_TRADING_GAINS = {"FY2025": 7326, "FY2024": 4052, "FY2023": 1665, "FY2022": 287, "FY2021": 1301}
IS_OTHER_OPERATING_INCOME = {"FY2025": 4699, "FY2024": 4302, "FY2023": 3738, "FY2022": 4049, "FY2021": 3499}
IS_NET_OPERATING_INCOME = {"FY2025": 67294, "FY2024": 64820, "FY2023": 57617, "FY2022": 42605, "FY2021": 33338}
IS_DIVIDEND_INCOME = {"FY2022": 12162, "FY2021": 206}
IS_TOTAL_INCOME = {"FY2022": 54767, "FY2021": 33544}
IS_DEPRECIATION = {"FY2025": -3674, "FY2024": -3228, "FY2023": -2990, "FY2022": -3159, "FY2021": -2588}
IS_OTHER_OPEX = {"FY2025": -38600, "FY2024": -36747, "FY2023": -37439, "FY2022": -34691, "FY2021": -28987}
IS_TOTAL_OPEX = {"FY2025": -42274, "FY2024": -39975, "FY2023": -40429, "FY2022": -37850, "FY2021": -31575}
IS_OP_PROFIT_PRE_IMPAIRMENT = {"FY2025": 25020, "FY2024": 24845, "FY2023": 17188, "FY2022": 16916, "FY2021": 1969}
IS_IMPAIRMENT = {"FY2025": -5738, "FY2024": -5401, "FY2023": -4315, "FY2022": -4500, "FY2021": -1567}
IS_PROFIT_BEFORE_TAX = {"FY2025": 19282, "FY2024": 19444, "FY2023": 12873, "FY2022": 12416, "FY2021": 402}
IS_TAX_CHARGE = {"FY2025": -2690, "FY2024": -2575, "FY2023": -1700, "FY2021": 359}
IS_PROFIT_FOR_YEAR = {"FY2025": 16592, "FY2024": 16869, "FY2023": 11173, "FY2022": 12416, "FY2021": 761}

OCI_PENSION_REMEASUREMENT = {"FY2025": 3532, "FY2024": -1182, "FY2023": -957, "FY2022": 983, "FY2021": 8076}
OCI_FV_SUBSIDIARIES = {"FY2023": -66, "FY2022": -9446, "FY2021": 9773}
OCI_FVOCI_DEBT = {"FY2025": 2397, "FY2024": -861, "FY2023": 55, "FY2022": -1096, "FY2021": -804}
OCI_CASH_FLOW_HEDGE = {"FY2025": 577, "FY2024": 24, "FY2023": 252, "FY2022": -240, "FY2021": 107}
# FY2025 carries no entry: the FY2025 edition prints this row as a DASH (nil) in
# its own column while printing 3 in its FY2024 comparative. See IS_SOURCES.
OCI_FX_TRANSLATION = {"FY2024": 3, "FY2022": -3, "FY2021": 4}
OCI_TOTAL = {"FY2025": 6506, "FY2024": -2016, "FY2023": -716, "FY2022": -9802, "FY2021": 17156}
TOTAL_COMPREHENSIVE_INCOME = {"FY2025": 23098, "FY2024": 14853, "FY2023": 10457, "FY2022": 2614, "FY2021": 17917}

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
    ("DATA", "Profit for the year (2025)", eq_gbp_avg("FY2025", (None, None, None, None, 16592, 16592))),
    ("DATA", "Other comprehensive income (2025)", eq_gbp_avg("FY2025", (None, 2397, 577, None, 3532, 6506))),
    ("TOTAL", "Total comprehensive income for the year (2025)",
     eq_gbp_avg("FY2025", (None, 2397, 577, None, 20124, 23098))),
    ("TOTAL", "Balance at 31 December 2025", eq_gbp_spot("FY2025", (569998, -309, 720, None, -226147, 344262))),
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
PROFIT_ADJ = {"FY2025": 19282, "FY2024": 19444, "FY2023": 12873, "FY2022": 12416, "FY2021": 402}
DEPRECIATION = {"FY2025": 3674, "FY2024": 3228, "FY2023": 2990, "FY2022": 1564, "FY2021": 1361}
IMPAIRMENT_LOSS = {"FY2025": 5738, "FY2024": 5378, "FY2023": 4608, "FY2022": 4500, "FY2021": 1567}
LOSS_ON_DISPOSAL_FA = {"FY2022": 0, "FY2021": 1056}
LOSS_ON_DISPOSAL_SUB = {"FY2023": 3294}
FX_LOSS_SUBORDINATED = {"FY2025": -13931, "FY2024": 7620, "FY2023": -4128, "FY2022": 7053, "FY2021": 7784}
INTEREST_EXP_LEASE = {"FY2025": 324, "FY2024": 411, "FY2023": 505, "FY2022": 379, "FY2021": 46}
TRADING_GAINS = {"FY2025": -5846, "FY2024": -1334, "FY2023": -456}
GAIN_LEASE_MOD = {"FY2023": -398}
FX_ADJ_ECL = {"FY2025": -2910, "FY2024": 1757, "FY2023": -2328}
# FY2024 edition captions this row 'FX adjustments on right-of-use assets';
# FY2025 captions the same row 'FX adjustments on lease liability'. Label drift
# between editions, recorded in CASH_FLOW_SOURCES rather than merged silently.
FX_ADJ_ROU = {"FY2025": -230, "FY2024": -340}
OPERATING_ADJ_SUBTOTAL = {"FY2025": 6101, "FY2024": 36164, "FY2023": 16960, "FY2022": 25912, "FY2021": 12216}

CHG_LOANS_CUSTOMERS = {"FY2025": -37616, "FY2024": -99312, "FY2023": -88176, "FY2022": 76970, "FY2021": -31138}
CHG_LOANS_BANKS = {"FY2022": 23398, "FY2021": 207372}
CHG_FVTPL_DERIVATIVES = {"FY2025": 32004, "FY2024": -1689, "FY2023": 14110, "FY2022": -19270, "FY2021": 123184}
CHG_FVOCI = {"FY2022": -42644, "FY2021": -86081}
CHG_AMORTISED_COST_INVESTMENTS = {"FY2022": 47594, "FY2021": -86211}
CHG_OTHER_ASSETS = {"FY2025": -13331, "FY2024": -4068, "FY2023": -1829, "FY2022": -2717, "FY2021": -6137}
CHG_ASSETS_SUBTOTAL = {"FY2025": -18943, "FY2024": -105069, "FY2023": -75895, "FY2022": 83331, "FY2021": 120989}

CHG_CUSTOMER_DEPOSITS = {"FY2025": -60766, "FY2024": 231252, "FY2023": -27011, "FY2022": 86445, "FY2021": 75042}
CHG_FUNDS_FROM_BANKS = {"FY2025": 292611, "FY2024": -9181, "FY2023": 98566, "FY2022": -218828, "FY2021": -166377}
CHG_OTHER_LIABILITIES = {"FY2025": 531, "FY2024": -768, "FY2023": 4667, "FY2022": 13392, "FY2021": -159}
CHG_LIABILITIES_SUBTOTAL = {"FY2025": 232376, "FY2024": 221302, "FY2023": 76222, "FY2022": -118990, "FY2021": -91494}

TAXES_PAID = {"FY2025": -3929, "FY2024": -2289, "FY2023": 0, "FY2022": 0, "FY2021": 0}
INTEREST_PAID_LEASE = {"FY2022": -379, "FY2021": -46}
NET_OPERATING = {"FY2025": 215605, "FY2024": 150109, "FY2023": 17287, "FY2022": -10126, "FY2021": 41665}

CHG_FVOCI_INVESTING = {"FY2025": -103651, "FY2024": -33386, "FY2023": 27277}
CHG_AMORTISED_COST_INVESTING = {"FY2025": -5307, "FY2024": -79759, "FY2023": 21229}
ACQUISITION_PPE = {"FY2025": -2611, "FY2024": -3251, "FY2023": -2410, "FY2022": -3848, "FY2021": -1674}
DISPOSAL_SUBSIDIARIES = {"FY2023": 25342}
INVESTMENT_IN_SUBSIDIARIES = {"FY2022": 0, "FY2021": 0}
NET_INVESTING = {"FY2025": -111569, "FY2024": -116396, "FY2023": 71438, "FY2022": -3848, "FY2021": -1674}

PAYMENT_LEASE_LIABILITIES = {"FY2025": -1645, "FY2024": -1178, "FY2023": -803, "FY2022": -1344, "FY2021": -1335}
NET_FINANCING = {"FY2025": -1645, "FY2024": -1178, "FY2023": -803, "FY2022": -1344, "FY2021": -1335}

NET_CHANGE = {"FY2025": 102391, "FY2024": 32535, "FY2023": 87922, "FY2022": -15318, "FY2021": 38656}
# FY2025's own edition opens at EUR659,091k where the FY2024 edition closed at
# EUR659,090k - a EUR1k difference between editions, each year taken from its
# own edition (see CASH_FLOW_SOURCES).
CASH_BEGIN = {"FY2025": 659091, "FY2024": 626555, "FY2023": 538633, "FY2022": 174174, "FY2021": 135518}
CASH_END = {"FY2025": 761482, "FY2024": 659090, "FY2023": 626555, "FY2022": 158856, "FY2021": 174174}

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
AQ_STAGE1_GROSS = {"FY2025": 1003650, "FY2024": 976718, "FY2023": 850363, "FY2022": 773748, "FY2021": 829249}
AQ_STAGE2_GROSS = {"FY2025": 45257, "FY2024": 21996, "FY2023": 20240, "FY2022": 4108, "FY2021": 34421}
AQ_STAGE3_GROSS = {"FY2025": 42524, "FY2024": 52629, "FY2023": 91057, "FY2022": 122535, "FY2021": 110803}
AQ_GROSS_TOTAL = {"FY2025": 1091431, "FY2024": 1051343, "FY2023": 961660, "FY2022": 900391, "FY2021": 974473}
AQ_STAGE1_ECL = {"FY2025": 3287, "FY2024": 3155, "FY2023": 5759, "FY2022": 6944, "FY2021": 2732}
AQ_STAGE2_ECL = {"FY2025": 60, "FY2024": 50, "FY2023": 55, "FY2022": 41, "FY2021": 3859}
AQ_STAGE3_ECL = {"FY2025": 32263, "FY2024": 32987, "FY2023": 33240, "FY2022": 55032, "FY2021": 48038}
AQ_ECL_TOTAL = {"FY2025": 35610, "FY2024": 36192, "FY2023": 39054, "FY2022": 62017, "FY2021": 54629}
AQ_INTEREST_RECEIVABLE = {"FY2025": 8863, "FY2024": 8653, "FY2023": 8697}
AQ_NET = {"FY2025": 1064684, "FY2024": 1023804, "FY2023": 931303, "FY2022": 838374, "FY2021": 919844}

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
RATIO_PAGES = {"FY2025": "4", "FY2024": "6", "FY2022": "9"}

# More precise than the AR's rounded whole-percent KPI table, since FY2021/FY2022
# are now sourced from the Pillar3.pdf's own "EAB plc**" (entity-only) column
# instead - see PILLAR3_SOURCES. FY2023/FY2024 unchanged (AR KPI table only).
TOTAL_CAPITAL_RATIO = {"FY2025": "22%", "FY2024": "23%", "FY2023": "24%", "FY2022": "22.7%", "FY2021": "22.4%"}
CET1_RATIO = {"FY2025": "16%", "FY2024": "16%", "FY2023": "17%", "FY2022": "15.5%", "FY2021": "15.6%"}

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
# GA-020 (2026-09-19): FY2021 is the bank's own printed "n/a" (Pillar 3 at 31 Dec
# 2022, p.8, 31 Dec 2021 column); FY2023-FY2025 are UNREACHED (see GA020_NOTE).
# P3_UNREACHED is defined below with GA020_NOTE, so these are filled in there.
LEVERAGE_RATIO = {"FY2022": "11.7%", "FY2021": "N/A (as printed)"}
LCR_RATIO = {"FY2022": "218%", "FY2021": "267%"}
NSFR_RATIO = {"FY2022": "120%", "FY2021": "N/A (as printed)"}

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


# ---------------------------------------------------------------
# GA-020 statement vocabulary (2026-09-19). The FY2023-FY2025 Pillar 3 editions
# are UNREACHED, not established absences (see KM1_SOURCES): the duty stood (no
# SDDT Ru 3.1 row for FRN 446951) and every Annual Report says the Pillar 3
# ratios 'are published on EAB's website'. Cells now carry the reserved phrase.
# ---------------------------------------------------------------
def _p3_unreached(y):
    # Second pass 2026-09-19 (GA-020 unreached): wording extended with the new routes; see GA020_NOTE (B).
    return (f"Unreached today – {y} Pillar 3 not obtained: bank's download slot empty; WP media (.com/.eu), "
            "Wayback + Common Crawl (eabplc.com, arabbankeurope.com/.eu, eabsa.eu), archive.today hold none; "
            "Annual Report prints no such figure, 2026-09-19")


P3_UNREACHED = {y: _p3_unreached(y) for y in ("FY2025", "FY2024", "FY2023")}
LEVERAGE_RATIO = {**P3_UNREACHED, **LEVERAGE_RATIO}
LCR_RATIO = {**P3_UNREACHED, **LCR_RATIO}
NSFR_RATIO = {**P3_UNREACHED, **NSFR_RATIO}

MREL_STATEMENTS = {
    **P3_UNREACHED,
    "FY2022": ("Not published – EAB Pillar 3 Disclosures at 31 Dec 2022 (35pp, text-searched 2026-09-19) "
               "and Annual Report 2022 contain no MREL figure or mention"),
    "FY2021": ("Unreached today – no FY2021 Pillar 3 in Wayback (full eabplc.com CDX), Common Crawl or "
               "archive.today; Wayback AR 2021 copy is 1 MiB-truncated; FY2022 edition and AR 2022 carry no "
               "MREL, 2026-09-19"),
}

GA020_NOTE = (
    "GA-020 RECLASSIFICATION, 19 September 2026. Every bare 'Not publicly disclosed'/'n/a' cell and every "
    "deliberately-empty UNREACHED cell on this workbook now states its outcome. (1) FY2023/FY2024/FY2025 on "
    "every Pillar 3 metric sheet other than the two Annual Report KPI ratios, the KM1 sheet and the RWA "
    "Breakdown sheet read 'Unreached today', because the document that would carry them - that year's "
    "standalone Pillar 3 - exists (every Annual Report says the Pillar 3 ratios 'are published on EAB's "
    "website': AR 2022 PDF p.13, AR 2024 PDF p.11, AR 2025 PDF p.11) and the duty stood "
    "(PRA consolidated waivers register re-downloaded 2026-09-19: 2,900 rows, 67 strict 'SDDT Regime - "
    "General Application' + 'Ru 3.1' rows, none for FRN 446951, whose three rows are Ar 9, CA.BU.5.1-5.3 "
    "and Ar 400(2)(c)). What was tried on 2026-09-19: https://arabbankeurope.com/downloads/pillar-iii-"
    "disclosures/ still 302s to the homepage and the REST record (post 2923, modified 2026-07-07) still has "
    "\"eab_file\": null; the REST media library still lists 64 PDFs, none a Pillar 3 (search 'pillar' "
    "returns []; control search 'annual' returns the FY2025 Annual Report); the record's guid names a "
    "staging host abemigration.wpenginepowered.com, which answers HTTP 401 (authorisation required); "
    "https://www.eabplc.com/downloads/Pillar3EABplc2023.pdf, .../Pillar3EAB_PLC_2024.pdf and .../Pillar3.pdf "
    "all serve the 95,415-byte homepage HTML; Wayback CDX for both named 2023/2024 paths returns HTTP 200 "
    "with no rows; CDX of eabplc.com filtered on 'pillar' returns the same 12 URLs (2009-2020 series plus "
    "downloads/Pillar3.pdf); CDX of arabbankeurope.com holds no PDF. THE ONE UNEXAMINED CAPTURE WAS OPENED: "
    "downloads/Pillar3.pdf at 20240713003435 (digest IFQXMT5C..., different from the pinned copy) is exactly "
    "1,048,576 bytes, i.e. the Wayback 1 MiB truncation; five pages were salvaged by rebuilding the page "
    "tree and its cover page image reads 'EAB Group - Pillar 3 Disclosures / 31 December 2022' - the SAME "
    "FY2022 edition, not a later one. The Pillar 3 is not a Companies House filing, so the filing history "
    "was not a route for it. (2) KM1 FY2021 leverage/NSFR 'n/a' cells carry the plain '-' (locked KM1 rule 2; "
    "glyph printed: 'n/a'); the matching FY2021 cells on the Leverage Ratio and NSFR sheets read 'N/A (as "
    "printed)'. In both places the bank printed 'n/a' in the 31 Dec 2021 "
    "column of its Key metrics table (Pillar 3 at 31 Dec 2022, p.8, page image checked 2026-09-19). "
    "(3) MREL FY2022 reads 'Not published': the FY2022 Pillar 3 (text layer confirmed - 395 lines contain "
    "' the ') and the FY2022, FY2024 and FY2025 Annual Reports contain no 'MREL' or 'eligible liabilities' "
    "anywhere. MREL FY2021 is 'Unreached today' because that year's own Pillar 3 edition was never obtained.\n"
    "(B) GA-020 SECOND PASS, 19 September 2026 - routes the first pass did not use. NO FIGURE WAS FOUND; all 34 "
    "cells stay 'Unreached today'. ENTITY BASIS CONFIRMED: EAB plc SOLO - the FY2022/FY2021 cells are the "
    "Pillar 3's 'EAB plc**' entity-only column, and the Annual Reports are EAB plc's individual accounts (the "
    "Directors' Report of AR 2024 and AR 2025 states the s.401 exemption: EAB SA's results are not "
    "consolidated). Nothing below uses the EAB Group basis or the Jordanian parent. (i) OWN ANNUAL REPORTS read "
    "beyond the KPI table: AR 2024 and AR 2025 (bank's text PDFs, searched for risk-weighted, own funds, tier 1, "
    "leverage, liquidity coverage, stable funding, HQLA, MREL) and the FY2023 accounts, which exist only as the "
    "Companies House filing of 31 May 2024 (140pp image scan, OCR-searched; control: 1,387 lines contain "
    "' the '). Each prints only the CET1 and capital adequacy ratios already on the ratio sheets; the capital "
    "management note gives net equity and perpetual subordinated liabilities only, and liquidity is narrative "
    "('liquidity coverage ratio substantially above the regulatory requirements'). No CET1/Tier 1/Total "
    "capital amount, Tier 1 ratio, RWA, leverage ratio, LCR, NSFR or MREL. The FY2024 and FY2025 Companies "
    "House filings (133pp and 132pp scans, OCR-searched) hit the same terms only on the same pages. Filing "
    "history read on pages 1 and 2 (back to April 2017). (ii) THE EDITIONS EXISTED: web search still indexes "
    "https://www.eabplc.com/downloads/Pillar3EAB_PLC_2024.pdf under the title 'EAB Group - Pillar 3 "
    "Disclosures - 31 December 2024' and .../Pillar3EABplc2023.pdf under 'Pillar III Disclosures'. Neither "
    "Bing nor DuckDuckGo offers a cached copy. No FY2025 edition is indexed. (iii) COMMON CRAWL: 27 indexes "
    "(CC-MAIN-2023-06 to CC-MAIN-2025-51) enumerated for eabplc.com (matchType=domain). The only Pillar 3 "
    "capture is downloads/Pillar3.pdf on 13 Jul 2024, the same 1 MiB-truncated FY2022 copy (digest "
    "IFQXMT5C...). For arabbankeurope.com the only hit is the 302 of downloads/pillar-iii-disclosures/ (Aug "
    "2026). (iv) WAYBACK ON EVERY DOMAIN, without mimetype filter: eabplc.com full-domain CDX (12,185 rows) "
    "has Pillar 3 files for 2009-2020 plus downloads/Pillar3.pdf, and nothing else; its 361 rows since 2023 "
    "hold none. Three domains were newly found this pass: eabsa.eu (the French subsidiary's old site, 194 "
    "rows, Pillar 3 mirror to 2018 only), eabplc.net (14 rows, no PDF) and the staging host "
    "abemigration.wpenginepowered.com (0 rows). (v) ARCHIVE.TODAY: no capture of either named PDF, three "
    "pre-2014 pages for www.eabplc.com, nothing for arabbankeurope.com. (vi) SISTER SITE arabbankeurope.eu "
    "(eabsa.eu now 301s there; Cloudflare 403 over HTTP/2, 200 over HTTP/1.1). Its WordPress media library "
    "(393 items, 29 PDFs) and sitemap (163 URLs) hold a 'Rapport de Pilier 3' at 31 Dec 2023 for Arab Bank "
    "Europe SA, a DIFFERENT legal entity (EAB plc's French subsidiary), so it was not used. Its July 2026 "
    "pitchbook prints no regulatory metric. The arabbankeurope.com media library was re-enumerated in full "
    "(435 items, 64 PDFs) and still holds no Pillar 3. (vii) PARENT: the Arab Bank Group Annual Report 2023 "
    "names EAB only as a subsidiary (paid capital EUR570m) and prints no separately labelled EAB capital or "
    "liquidity table. (viii) MREL FY2021: the Wayback copy of the FY2021 Annual Report "
    "(files/PDFs/annual_reports/2021_EAB_Annual_Report.pdf, both captures share one digest) and the 2020 "
    "Pillar 3 capture are each exactly 1,048,576 bytes, the Wayback 1 MiB truncation, and neither opens. "
    "WHAT WOULD CLOSE THESE CELLS: the FY2023-FY2025 Pillar 3 PDFs, obtained from the bank on request (see "
    "the SDDT note: the duty stood)."
)


# ---------------------------------------------------------------
# KM1 Key Metrics - EAB's own "Key metrics" table, reproduced as printed.
#
# Four things make this bank's table unlike any other in the project, and all
# four are preserved rather than normalised:
#
#   1. NO ROW NUMBERS AND NO "KM1" HEADING. EAB's table is headed simply "Key
#      metrics" and carries none of the template's row numbers (1, 2, UK 7a...).
#      It is nonetheless the UK KM1 template - the row labels, their order and
#      the section headings match it line for line. Any search keyed on the
#      string "KM1" or on a row number will report this bank as having no KM1.
#
#   2. FOUR COLUMNS ACROSS TWO ENTITIES. The single printed table is
#      "EAB Group" (31-Dec-22, 31-Dec-21) beside "EAB plc**" (31-Dec-22,
#      31-Dec-21), where ** is the document's own footnote "EAB plc regulatory
#      numbers are based on entity only basis". This workbook is entity-only
#      throughout, so the EAB plc columns are the ones carried here. The EAB
#      Group figures are recorded in full in the source citation so nothing is
#      lost.
#
#   3. EUROS, NOT STERLING. EAB reports in EUR and the table is in €m. This is
#      the ONE sheet in this workbook left in the source currency, because a
#      KM1 sheet's job is to reproduce what the bank published; every other
#      sheet converts to £ (see FX_NOTE). The £ equivalents actually used on
#      the metric sheets are given in the citation.
#
#   4. "n/a" IS THE BANK'S OWN WORD for the FY2021 leverage and NSFR rows, not
#      a gap in sourcing: the PRA's leverage and NSFR templates took effect on
#      1 January 2022 and the document states "Prior periods, 'n/a' indicates
#      that the disclosure is new or changed and no comparatives are being
#      provided." Those cells carry "n/a", not a blank and not a back-filled
#      figure from another basis.
#
# FY2023 and FY2024 are blank: EAB published no Pillar 3 document for either
# year that could be recovered (see ENTITY_NOTE), so there is no KM1 to show.
# ---------------------------------------------------------------
# The bank printed "n/a" (p.8). On the KM1 sheet the LOCKED KM1 rule 2 (wayfinder/km1/map.md) governs: a
# printed dash glyph - "-", "—" or "n/a" - is carried as the plain ASCII "-", with the glyph recorded in the
# note. User decision 2026-09-19: KM1 rule 2 wins on KM1 sheets; BRIEF.md's "N/A (as printed)" is for
# non-KM1 sheets only (the Leverage Ratio and NSFR sheets below keep it).
_EAB_NA = "-"

km1_rows = [
    ("DATA", "[Edition status for this year - not a KM1 template row]", dict(P3_UNREACHED)),
    ("SECTION", "Available capital (€m)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) capital", {"FY2022": 253, "FY2021": 252}),
    ("DATA", "Tier 1 capital", {"FY2022": 253, "FY2021": 252}),
    ("DATA", "Total capital", {"FY2022": 370, "FY2021": 362}),
    ("SECTION", "Risk-weighted Assets ('RWA') (€m)", {}),
    ("DATA", "Total RWA", {"FY2022": 1631, "FY2021": 1616}),
    ("SECTION", "Capital ratios (as a percentage of RWA) (%)", {}),
    ("DATA", "Common Equity Tier 1 ratio", {"FY2022": "15.5%", "FY2021": "15.6%"}),
    ("DATA", "Tier 1 ratio", {"FY2022": "15.5%", "FY2021": "15.6%"}),
    ("DATA", "Total capital ratio", {"FY2022": "22.7%", "FY2021": "22.4%"}),
    ("SECTION", "Additional own funds requirements based on SREP (% of RWA)", {}),
    ("DATA", "Additional CET1 SREP requirements", {"FY2022": "2.3%", "FY2021": "2.3%"}),
    ("DATA", "Additional AT1 SREP requirements", {"FY2022": "0.8%", "FY2021": "0.8%"}),
    ("DATA", "Additional T2 SREP requirements", {"FY2022": "1.0%", "FY2021": "1.0%"}),
    ("DATA", "Total SREP own funds requirements", {"FY2022": "12.03%", "FY2021": "12.04%"}),
    ("SECTION", "Combined buffer requirement (% of RWA)", {}),
    ("DATA", "Capital conservation buffer", {"FY2022": "2.5%", "FY2021": "2.5%"}),
    ("DATA", "Institution specific countercyclical capital buffer", {"FY2022": "0.1%", "FY2021": "0.0%"}),
    ("DATA", "Combined buffer requirement", {"FY2022": "2.6%", "FY2021": "2.5%"}),
    ("DATA", "Overall capital requirements", {"FY2022": "14.7%", "FY2021": "14.6%"}),
    ("DATA", "CET1 available after meeting the total SREP own funds requirements",
     {"FY2022": "3.5%", "FY2021": "3.4%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "Total exposure measure excluding claims on central banks (€m)",
     {"FY2022": 2144, "FY2021": _EAB_NA}),
    ("DATA", "Leverage ratio excluding claims on central banks (%)",
     {"FY2022": "11.7%", "FY2021": _EAB_NA}),
    ("SECTION", "Liquidity Coverage Ratio ('LCR')", {}),
    ("DATA", "Total high-quality liquid assets (HQLA) (Weighted value average) (€m)",
     {"FY2022": 291, "FY2021": 355}),
    ("DATA", "Cash outflows - Total weighted value (€m)", {"FY2022": 522, "FY2021": 538}),
    ("DATA", "Cash inflows - Total weighted value (€m)", {"FY2022": 442, "FY2021": 435}),
    ("DATA", "Total net cash outflows (adjusted value) (€m)", {"FY2022": 137, "FY2021": 137}),
    ("DATA", "Liquidity coverage ratio (%)", {"FY2022": "218%", "FY2021": "267%"}),
    ("SECTION", "Net Stable Funding Ratio ('NSFR')", {}),
    ("DATA", "Total available stable funding (€m)", {"FY2022": 1396, "FY2021": _EAB_NA}),
    ("DATA", "Total required stable funding (€m)", {"FY2022": 1163, "FY2021": _EAB_NA}),
    ("DATA", "NSFR ratio (%)", {"FY2022": "120%", "FY2021": _EAB_NA}),
]

KM1_SOURCES = (
    "Sources - Europe Arab Bank plc's standalone Pillar 3 Disclosures as at 31 December 2022, PDF page 8 of "
    "35, the table headed 'Key metrics', 'EAB plc**' entity-only columns:\n"
    f"FY2022 & FY2021: {PILLAR3_2022_URL}\n"
    "This is the ONLY Pillar 3 document EAB has published that could be recovered.\n\n"
    "FY2025/FY2024/FY2023 ARE AN UNRESOLVED AVAILABILITY GAP, NOT AN ESTABLISHED ABSENCE — CORRECTED "
    "2026-09-18 (GA-018, feeding GA-013). The previous wording here and in the sheet subtitle said 'no "
    "equivalent document exists for those years'. That claim was never evidenced and is now withdrawn: it "
    "was an inference from three years of failed retrieval, which is the self-sealing negative this project "
    "has repeatedly been bitten by (km1/map.md rules 9 and 40). Nothing found today shows the bank did not "
    "publish; the evidence points the other way, and it is recorded so the question is not re-opened from "
    "scratch or closed the wrong way:\n"
    "• THE BANK STILL ADVERTISES THE DOCUMENT AND THE LINK IS BROKEN. arabbankeurope.com publishes a "
    "downloads entry titled 'Pillar III Disclosures' (post id 2923, slug 'pillar-iii-disclosures', status "
    "'publish', categories 44 and 26), listed in the site's own Yoast sitemap at "
    "https://arabbankeurope.com/eab_download-sitemap.xml. Its ACF file field is LITERALLY NULL "
    "(\"eab_file\": null), so the entry resolves to nothing: fetching "
    "https://arabbankeurope.com/downloads/pillar-iii-disclosures/ returns HTTP 302 to the site homepage. The "
    "CONTROL that makes this a fact about that entry rather than about the fetch is the sibling entry "
    "'Annual Report 2025' (post id 2924, same creation and modification timestamps, \"eab_file\": 3807), "
    "which returns HTTP 301 straight to the real PDF at .../wp-content/uploads/202602_EABAnnualReport_v9.pdf. "
    "Same site, same request shape, same minute of authoring — one resolves to a document and one is an "
    "empty slot. The Pillar 3 file was not carried across the site migration.\n"
    "• THE MIGRATED MEDIA LIBRARY HAS NO PILLAR 3 IN IT. The WordPress REST media endpoint was enumerated in "
    "full (per_page=100, media_type=application; page 2 returns 'rest_post_invalid_page_number', so 64 PDFs "
    "is the COMPLETE library, not a first page). No Pillar 3 document of any year is among them. Positive "
    "control on the same endpoint: ?search=annual returns the FY2025 Annual Report, so the endpoint answers "
    "and the zero is a fact about the library.\n"
    "• THE ANNUAL REPORTS SAY THE DOCUMENT SHOULD EXIST. Every edition read states that EAB's regulatory "
    "capital ratios 'required under Pillar 3 are published on EAB's website' (FY2025 Annual Report p.596 of "
    "the text extraction; the FY2024, FY2023 and FY2025 Companies House filings carry the same sentence). A "
    "bank pointing readers at a Pillar 3 on its website is not a bank that published none.\n"
    "• NO SDDT EXEMPTION EXPLAINS IT. Europe Arab Bank plc, FRN 446951, holds NO 'SDDT Regime - General "
    "Application' Rule 3.1 modification in the PRA consolidated waivers register (read first-hand "
    "2026-09-18; its three rows are Ar 9, CA.BU.5.1-5.3 and a Non-Core Large Exposures Ar 400(2)(c)). The "
    "Pillar 3 duty therefore STOOD in all three gap years, so 'not required to publish' is not available as "
    "an explanation either.\n"
    "• WHAT WAS SEARCHED AND CAME BACK EMPTY, recorded per km1/map.md rule 37 so it is not re-run blind: the "
    "live downloads sitemap (53 entries), the page sitemap (26 pages), the eab_download_category/financials/ "
    "listing (which shows only the Annual Report and an FSCS guide), the full REST media library, and a "
    "Wayback CDX sweep of eabplc.com filtered on 'pillar' — 12 captures, every one FY2020 or earlier except "
    "the single 2024-07-13 capture of .../downloads/Pillar3.pdf that is the FY2022 edition already cited "
    "here. The old host is gone and the archive holds no 2023, 2024 or 2025 edition.\n"
    "THE STATE TO RECORD IS THEREFORE 'UNREACHED'. Until 2026-09-19 the cells were left EMPTY on purpose so "
    "the gap stayed visible; under GA-020 the three year columns instead carry the reserved 'Unreached "
    "today' phrase in a single '[Edition status for this year - not a KM1 template row]' row placed ABOVE "
    "the bank's own rows, which are untouched (same order, labels and precision). audit_gaps.py scores that "
    "phrase 'u', a limit on our reach, never 'not published'. The five FY2021 cells where the bank printed "
    "'n/a' carry the plain '-' (KM1 rule 2, locked; glyph printed: 'n/a'); 'N/A (as printed)' is used only on "
    "non-KM1 sheets, per the user's decision of 19 September 2026.\n\n"
    + GA020_NOTE + "\n\n"
    "KM1 presentation notes:\n"
    "• NOT LABELLED 'KM1' AND NOT ROW-NUMBERED. EAB heads the table 'Key metrics' and prints no template "
    "row numbers at all, but the row labels, their order and the section headings are the UK KM1 template "
    "line for line. Reproduced here exactly as printed, without adding the numbers EAB omitted.\n"
    "• FOUR COLUMNS, TWO ENTITIES, ONE TABLE. EAB prints 'EAB Group' (31-Dec-22, 31-Dec-21) beside "
    "'EAB plc**' (31-Dec-22, 31-Dec-21); the footnote reads '** EAB plc regulatory numbers are based on "
    "entity only basis'. The EAB plc columns are used here, for consistency with every other sheet in this "
    "workbook. The EAB Group figures for the same two dates, recorded so nothing is lost: CET1 €290m/€293m; "
    "Tier 1 €290m/€293m; Total capital €407m/€403m; Total RWA €1,810m/€1,767m; CET1 & Tier 1 ratio "
    "16.0%/16.6%; Total capital ratio 22.5%/22.8%; SREP add-ons CET1 2.2%/2.2%, AT1 0.7%/0.7%, T2 "
    "1.0%/1.0%, total 11.93%/11.95%; conservation buffer 2.5%/2.5%; CCyB 0.1%/0.0%; combined buffer "
    "2.6%/2.5%; overall capital requirement 14.5%/14.5%; CET1 available after SREP 4.1%/4.6%; leverage "
    "exposure €2,557m/n.a. and ratio 11.4%/n.a.; HQLA €625m/€705m, outflows €590m/€528m, inflows "
    "€325m/€255m, net outflows €264m/€272m, LCR 249%/272%; ASF €1,631m/n.a., RSF €1,277m/n.a., NSFR "
    "128%/n.a.\n"
    "• EUROS, NOT STERLING. EAB reports in EUR and this table is in €m. This is the only sheet in the "
    "workbook left in the source currency, because the sheet exists to reproduce what the bank published. "
    "Every other sheet converts to £ at the rates described in FX_NOTE; the £'000 equivalents carried on "
    "the CET1 Capital / Tier 1 Capital / Total Capital / Total RWAs sheets are derived from exactly these "
    "€m figures.\n"
    "• 'n/a' IN FY2021 IS THE BANK'S OWN WORD, in five cells, and marks a disclosure that did not yet "
    "exist rather than one that is missing. The document states: 'These disclosures have been implemented "
    "from 1 January 2022 and are based on the PRA's disclosure templates and instructions which came into "
    "force at that time. Prior periods, \"n/a\" indicates that the disclosure is new or changed and no "
    "comparatives are being provided.'\n"
    "• FOOTNOTED BASES, per EAB's own footnotes: capital and RWA are on the UK CRR Article 473a IFRS 9 "
    "transitional arrangements (add-back 75% in 2022, 100% in 2021); the SREP figures are the outcome of "
    "the then-current SREP, which the document notes was being re-run; and the LCR weighted values are the "
    "simple average of the 12 preceding month-end observations.\n\n"
    + BASIS_NOTE
)

bw.add_km1_sheet(
    title="Europe Arab Bank plc — KM1 Key Metrics",
    subtitle="The bank's own published key-metrics table (the UK KM1 template, though EAB neither labels it "
             "'KM1' nor prints its row numbers), reproduced in EAB's row order and printed precision. "
             "Amounts in €m as published — this is the one sheet in this workbook left in the source "
             "currency. 'EAB plc' entity-only columns, not the EAB Group columns printed beside them. "
             "FY2025, FY2024 and FY2023 read 'Unreached today' (top row only) because no Pillar 3 document "
             "for those years could be OBTAINED — not because the bank is known not to have published one. "
             "See the source note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    source_height=300,
)


def metric(name, unit, rows_data, note=None, extra_sources=None):
    sources = p3_sources(RATIO_PAGES) + (("\n\n" + extra_sources) if extra_sources else "")
    bw.add_metric_sheet(name, f"Entity-level basis, {unit}" if unit else "Entity-level basis",
                         rows_data, sources, note=note,
                         first_col_width=46, source_height=140)


NOT_DISCLOSED_NOTE = (
    "Not disclosed in any of the three sourced Annual Reports (FY2021/FY2022, FY2023/FY2024 or FY2025) - the "
    "Bank's only capital/liquidity disclosure is the 'Other Key Performance Indicators' table's two headline "
    "ratios (Capital adequacy ratio, Common Equity Tier 1 ratio). No standalone Pillar 3 document was obtainable (see ENTITY_NOTE "
    "on the Cash Flow Statement sheet) and no other figure for this metric appears anywhere in either report.\n"
    + SDDT_NOTE + "\n" + GA020_NOTE
)

FY2324_ONLY_NOTE = (
    "FY2021/FY2022 now sourced from the recovered standalone Pillar3.pdf (see PILLAR3_SOURCES below and "
    "ENTITY_NOTE). FY2023/FY2024 (and FY2025) read 'Unreached today' (GA-020, 2026-09-19; see below) - the Bank's only capital disclosure for those "
    "two years is the Annual Report's 'Other Key Performance Indicators' table's two headline ratios (Capital "
    "adequacy ratio, Common Equity Tier 1 ratio); no standalone Pillar 3 document could be recovered for either "
    "year despite a re-check of both eabplc.com/arabbankeurope.com directly and a broader Wayback CDX search "
    "(2026-09-07, HD-081 item 4), re-confirmed independently 2026-09-15 and again 2026-09-18. FY2025 joins them: "
    "its Annual Report is now the newest edition in this workbook and it too discloses only those two ratios.\n"
    + SDDT_NOTE + "\n" + GA020_NOTE
)

metric("CET1 Capital", None,
       [("Common Equity Tier 1 (CET1) capital (£'000)",
         {**P3_UNREACHED,
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
         {**P3_UNREACHED,
          "FY2022": p3_tier1_capital_gbp["FY2022"], "FY2021": p3_tier1_capital_gbp["FY2021"]})],
       note=FY2324_ONLY_NOTE + " Additional Tier 1 (AT1) capital is nil in both FY2021 and FY2022 per Pillar3.pdf, "
                               "so Tier 1 = CET1 exactly in those two years.",
       extra_sources=PILLAR3_SOURCES)

metric("Tier 1 Ratio", None,
       [("Tier 1 ratio",
         {**P3_UNREACHED,
          "FY2022": "15.5%", "FY2021": "15.6%"})],
       note=FY2324_ONLY_NOTE + " Tier 1 ratio = CET1 ratio in both FY2021 and FY2022 since AT1 is nil (see Tier 1 "
                               "Capital sheet). For FY2023/FY2024, the KPI table's 'Capital adequacy ratio' is "
                               "Total Capital, not Tier 1 - not substituted here since that would misrepresent a "
                               "different metric.",
       extra_sources=PILLAR3_SOURCES)

metric("Total Capital", None,
       [("Total capital (£'000)",
         {**P3_UNREACHED,
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
         {**P3_UNREACHED,
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
        # GA-020: placed AFTER the TOTAL, never inside the DATA block, so verify_workbook.py
        # does not skip a reconciled column for a text cell.
        + [("DATA", "[Edition status for this year - not an RWA category row]", dict(P3_UNREACHED))]
    ),
    sources_text=(
        "FY2022/FY2021: recovered Pillar3.pdf's 'Overview of RWA' table, 'EAB PLC' entity-only RWA columns "
        "(not the 'EAB Group' columns, for consistency with the rest of this workbook), converted from EUR to "
        "£'000 at each year's period-end spot rate. " + PILLAR3_SOURCES + "\n\n"
        "FY2023/FY2024: " + RWA_NOT_DISCLOSED_NOTE + "\n\n" + GA020_NOTE
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
    statements={"MREL Ratio": MREL_STATEMENTS},
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
EQ_OPENING_EUR = {"FY2021": 275321, "FY2022": 293238, "FY2023": 295854, "FY2024": 306311, "FY2025": 321164}
EQ_CLOSING_EUR = {"FY2021": 293238, "FY2022": 295854, "FY2023": 306311, "FY2024": 321164, "FY2025": 344262}
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
         "are plotted here (CET1 Ratio, Total Capital Ratio, both disclosed for all 5 years) - Tier 1 Ratio, "
         "Leverage Ratio, LCR and NSFR are only disclosed for FY2021/FY2022 (LCR)/FY2022 (Leverage, NSFR), via a "
         "recovered standalone Pillar 3 document, and not at all for FY2023, FY2024 or FY2025, see the "
         "individual Pillar 3 sheets and ENTITY_NOTE for why. FY2025 WAS ADDED 18 September 2026 from the bank's "
         "own Annual Report and Financial Statements 2025, live on its current host; the earlier note here "
         "saying FY2025 was excluded is superseded. 'Other movements, net' in "
         "the equity bridge absorbs the FX spot/average rate differential (near-zero in EUR-native terms).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ARAB BANK EUROPE FINANCIALS.xlsx")
