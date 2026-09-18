import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014", "FY2013"]
Y_CORE = YEARS[:YEARS.index('FY2014') + 1]  # HD-072/075/079: FY2014-floor default for Pillar 3/Asset Quality/RWA Breakdown/Overview
  # most recent first
# HD-072 (2026-09-06): FY2013 added to the 4 statutory-statement sheets only (Balance Sheet, Profit & Loss,
# Statement of Changes in Equity, Cash Flow Statement) - Pillar 3, Asset Quality and RWA Breakdown remain FY2014-floored
# (out of scope for this ticket; those dicts simply have no FY2013 entry, same convention as any other undisclosed year).

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/07425398/filing-history"
AR25_URL = f"{CH_BASE}/MzUyNjQ0MDA3MmFkaXF6a2N4/document?format=pdf&download=0"
AR23_URL = f"{CH_BASE}/MzQyMDE3MTk5NWFkaXF6a2N4/document?format=pdf&download=0"
AR21_URL = f"{CH_BASE}/MzMzODgwNTQxMWFkaXF6a2N4/document?format=pdf&download=0"
# HD-052 (2026-09-05): FY2014-FY2020 extension, re-sourced from Companies House filing-history scans
# (image-only PDFs, OCR'd + page-rendered) rather than the live URLs above, which are FY2021+ only.
AR20_URL = f"{CH_BASE}/MzMyNTUwMDk3NmFkaXF6a2N4/document?format=pdf&download=0"
AR18_URL = f"{CH_BASE}/MzI0ODY3MjA2N2FkaXF6a2N4/document?format=pdf&download=0"
AR16_URL = f"{CH_BASE}/MzE3NTM0ODg3NmFkaXF6a2N4/document?format=pdf&download=0"
AR14_URL = f"{CH_BASE}/MzEyNTM4MDgyMGFkaXF6a2N4/document?format=pdf&download=0"

CASH_FLOW_SOURCES = (
    "Sources — all figures are Itau BBA International plc (\"IBBAInt\"/\"the Bank\") solo-entity (Bank, not Group) "
    "Statement of Cash Flows, USD'000:\n"
    f"FY2025 & FY2024: 2025 Annual Report, p.65 (Statements of Cash Flows) — {AR25_URL}\n"
    f"FY2023 & FY2022: 2023 Annual Report, p.57 (Statement of Cash Flows) — {AR23_URL}\n"
    f"FY2021: 2021 Annual Report, p.56 (Statement of Cash Flows) — {AR21_URL}\n"
    "Note: these are Companies House filing copies (fully scanned/image-only PDFs, no text layer — transcribed via "
    "page-render + manual reading). The bank's own site (itau.co.uk) returned HTTP 403 to every fetch, and the "
    "domain referenced throughout the Annual Report for further disclosures (www.itaubba.co.uk) was unreachable "
    "this session (connection refused/timed out, and no usable Wayback Machine snapshot was found — a genuine "
    "Internet Archive-side outage, not bank-specific), so Companies House was the only available source. "
    "[CORRECTED 2026-09-18, GA-018: 'connection refused/timed out' describes only port 443. The host is ALIVE — "
    "DNS resolves to 94.126.169.4 and PORT 80 returns HTTP 302 (nginx/1.22.1) redirecting to "
    "https://www.itau.com.br/itaubba-en/international, which then returns 403. Companies House remaining the "
    "practical source is unaffected; the description of the host is. Full measurements in BLOCKED_HOST_NOTE on "
    "the Pillar 3 sheets.] The source "
    "labels 'Derivatives designated as hedging instruments' twice per year (once within operating assets, once "
    "within operating liabilities) — disambiguated here as '(assets)' / '(liabilities)' for clarity; this is a "
    "labeling change only, not a data change. 'Purchases of financial assets measured at fair value through OCI' "
    "is printed with an inconsistent sign convention across report vintages (positive in the FY2025 report's own "
    "FY2025/FY2024 columns, negative in the FY2023 report's own FY2023/FY2022 columns) — transcribed exactly as "
    "each source year printed it, not normalized. Blank cells indicate that year's report did not disclose that "
    "specific line; a dash ('-') in the source is shown as 0. All 5 years' opening cash balances tie exactly to "
    "the prior year's closing balance. DATA QUALITY NOTE: summing FY2024's own individually-transcribed line "
    "items gives USD 233,960k for 'Net cash flow from operating activities before payment of income tax', a USD "
    "7k gap against the figure the source itself prints for that subtotal (USD 233,967k, used here) — an "
    "immaterial rounding artifact within the source document, not a transcription error (every individual line "
    "item ties exactly to the source page); flagged rather than silently adjusted, per this project's convention.\n"
    "HD-052 (2026-09-05) extension to FY2014-FY2020, Bank/solo basis, USD'000, from Companies House filing-history "
    "scans (image-only PDFs, OCR'd + page-rendered for reading; no live itau.co.uk/itaubba.co.uk source was "
    "reachable, same constraint as the FY2021-2025 years above):\n"
    f"FY2020 & FY2019: 2020 Annual Report, p.46 (Statement of Cash Flows) — {AR20_URL}\n"
    f"FY2018 & FY2017: 2018 Annual Report, p.35 (Statement of Cash Flows) — {AR18_URL}\n"
    f"FY2016 & FY2015: 2016 Annual Report, p.28 (Statement of Cash Flows) — {AR16_URL}\n"
    f"FY2014 & FY2013: 2014 Annual Report (the Bank-solo standalone report; the Companies House filing bundles this "
    f"together with a separate '2014 Consolidated Annual Report' covering the Group — only the Bank-solo report "
    f"is used, matching this sheet's entity basis), p.30 (Statement of Cash Flows) — {AR14_URL}\n"
    "HD-072 (2026-09-06): FY2013 added (Balance Sheet/P&L/Equity/Cash Flow only, per that ticket's scope) as the "
    "2014 Annual Report's own FY2013 comparative column on the same p.30 Statement of Cash Flows — same source "
    "document already downloaded for FY2014, re-read for its comparative column.\n"
    "DATA QUALITY / METHODOLOGY NOTE: both FY2014's and FY2013's own Statement of Cash Flows are presented under "
    "the DIRECT method (interest/commissions received and paid, payments to employees and suppliers, etc.) — "
    "genuinely different from the INDIRECT method (reconciliation from profit before tax) used in every "
    "FY2015-2025 report. Rather than force these two years' direct-method lines into the indirect-method row "
    "structure, FY2013-FY2014 are shown in their own section below with their own line items; the indirect-method "
    "rows are blank for FY2013/FY2014 only. All methods reconcile to the same cash position with no year skipped: "
    "FY2013's own closing cash of USD 131,819k ties exactly to FY2014's own opening cash of USD 131,819k, and "
    "FY2014's own closing cash of USD 205,351k ties exactly to FY2015's own opening cash of USD 205,351k (via the "
    "2016 Annual Report's own FY2015 column). FY2013's own 'Cash and cash equivalents at beginning of year' is "
    "genuinely blank ('-') in the source — 2013 was the year Itau BBA International plc merged with its former "
    "sister entity (see the Statement of Changes in Equity sheet's 'Share capital of the acquiree on the merger' "
    "row and this sheet's own 'Cash and equivalents acquired in the merger' line of USD 46,358k) — the pre-merger "
    "entity's own opening cash position is not disclosed as a comparative in this statement, not an omission here. "
    "DATA QUALITY NOTE: summing FY2020's own individually-transcribed Bank investing-activities line items gives "
    "USD (51,561)k, a USD 270k gap against the figure the source itself prints for 'Net cash flow from investing "
    "activities' (USD (51,831)k, used here) - every individual line item ties exactly to the source page, so this "
    "is an internal inconsistency in the source document itself, not a transcription error; flagged rather than "
    "silently adjusted, per this project's convention. FY2016's own source table prints the label '(Purchases) / "
    "Sales of fixed assets' twice with different values in the same investing-activities section (Bank: 28,975 "
    "and (84)) - both are transcribed as separate lines here (the first labeled 'initial disposal' for clarity), "
    "but summing all of FY2016's own individually-transcribed Bank investing-activities lines gives +USD 28,814k, "
    "the exact MAGNITUDE of the source's own printed 'Net cash flow from investing activities' subtotal but with "
    "the OPPOSITE SIGN (source prints USD (28,814)k) - every individual line ties exactly to the source page, so "
    "this is a sign inconsistency in the source document's own subtotal, not a transcription error; the source's "
    "own printed subtotal (negative) is used here and flagged rather than silently corrected."
)

ENTITY_NOTE = (
    "All 3 statement sheets (Balance Sheet, Profit & Loss, Statement of Changes in Equity) use the Bank/solo "
    "column (not Group/consolidated), matching the entity basis already used for this workbook's Cash Flow "
    "Statement. Asset Quality also uses the Bank column. Pillar 3 metric sheets (CET1/Tier 1/Total Capital, "
    "ratios, Total RWAs, Leverage Ratio) remain Group/consolidated basis, matching how the Annual Report's own "
    "'Capital' section is presented (Group level only, all 5 years) - this is a pre-existing, unchanged choice."
)

def statement_sources(page, doc_label, url, note_extra=""):
    return (
        f"Source — Itau BBA International plc Bank (solo, not Group) financial statements, {doc_label} Annual "
        f"Report, p.{page} — {url}\n"
        + ENTITY_NOTE + (" " + note_extra if note_extra else "")
    )

# itau.com.br is BLOCKED, NOT DEAD - an important distinction, and the reason the
# live publisher URL stays the primary citation on every sheet below. Re-tested
# 2026-09-16: all three URLs return HTTP 403 with a short text/html body (~438-458
# bytes), i.e. a Cloudflare/WAF bot challenge refusing an automated client. A 403
# is an UNKNOWN - it tells us the host declined to serve US, not that the document
# has been withdrawn; a human browser may well still retrieve it. So these are NOT
# treated as dead and are NOT replaced. The Wayback snapshot is recorded ALONGSIDE
# each live URL purely as a LABELLED FALLBACK for when the host refuses.
#
# Fallbacks upgraded 2026-09-16 from the bare .../web/<timestamp>/ viewer form to
# the "id_" form (.../web/<timestamp>id_/<original>), which is a contract to return
# the original archived bytes rather than the Wayback viewer page, and from http://
# to https://. Each was fetched and verified on 2026-09-16: begins "%PDF", page
# count as stated, correct entity ("Itau BBA International plc") and year on the
# cover, and the final page renders (so none is a truncated capture).
PILLAR3_2021_URL = "https://www.itau.com.br/content/dam/ibba/en/Pillar-3-2021.pdf"
# Verified 2026-09-16: 1,803,996 bytes, 54pp, cover "Itau BBA International plc / 2021 Pillar 3 Disclosures".
PILLAR3_2021_WAYBACK = "https://web.archive.org/web/20230502062443id_/" + PILLAR3_2021_URL
PILLAR3_2022_URL = "https://www.itau.com.br/media/dam/m/58b090bc84eddb94/original/Pillar-3-2022.pdf"
# Verified 2026-09-16: 1,036,900 bytes, 67pp, cover "2022 Pillar 3 Disclosures / Itau BBA International plc".
PILLAR3_2022_WAYBACK = "https://web.archive.org/web/20230502054346id_/" + PILLAR3_2022_URL
PILLAR3_2023_URL = "https://www.itau.com.br/media/dam/m/11e1e216dd5df1fd/original/Pillar-3-2023.pdf"
# Verified 2026-09-16: 1,144,738 bytes, 62pp, cover "Market Discipline - 2023 Pillar III / Itau BBA International plc".
PILLAR3_2023_WAYBACK = "https://web.archive.org/web/20240812211731id_/" + PILLAR3_2023_URL

BLOCKED_HOST_NOTE = (
    "BLOCKED SOURCE HOST - NOT A DEAD LINK (recorded 2026-09-16). The three standalone Pillar 3 documents "
    "cited on this sheet are hosted on itau.com.br, which refuses automated clients: re-tested 2026-09-16, "
    "each URL returns HTTP 403 with a short (~438-458 byte) text/html body, a Cloudflare/WAF bot challenge. "
    "A 403 is explicitly an UNKNOWN state, NOT evidence of removal - it records that the host declined to "
    "serve this project's automated fetcher, and the documents may well still be retrievable by a human "
    "browser or from a different network. For that reason the publisher's own live URL remains the PRIMARY "
    "citation for every figure on this sheet and has deliberately NOT been replaced. The Wayback Machine "
    "snapshot shown next to it is a LABELLED FALLBACK, provided only so the figure stays verifiable when the "
    "host refuses the reader as it refused this session. Fallbacks are given in the 'id_' form "
    "(https://web.archive.org/web/<timestamp>id_/<original URL>), which returns the original archived bytes "
    "rather than the Wayback viewer page, and each was fetched and verified on 2026-09-16: FY2021 1,803,996 "
    "bytes / 54pp; FY2022 1,036,900 bytes / 67pp; FY2023 1,144,738 bytes / 62pp. All three begin '%PDF', all "
    "three name 'Itau BBA International plc' and their stated year on the cover, and in all three the final "
    "page still renders, confirming none is a truncated capture. No figure was changed.\n\n"
    "HOST-REACH CORRECTION, MEASURED 2026-09-18 (GA-018, feeding GA-013) - THE CLAIM ABOVE THAT itau.com.br "
    "'REFUSES AUTOMATED CLIENTS' IS TOO STRONG AND IS CORRECTED HERE. It was an inference drawn from repeated "
    "failure, which is km1/map.md rule 9's own defect class. What actually happens, measured against a VERBATIM "
    "URL already cited in this script (the FY2023 document, .../11e1e216dd5df1fd/original/Pillar-3-2023.pdf - no "
    "slug was guessed):\n"
    "  • Full Chrome header set INCLUDING Referer and Sec-Fetch-Dest/Mode/Site/User, over HTTP/1.1 -> HTTP 200, "
    "Content-Type application/pdf, 1,043,167 bytes. The document served.\n"
    "  • The SAME URL over HTTP/2, same minute -> HTTP 403 (458-byte text/html).\n"
    "  • A bare browser user-agent with only Accept, over HTTP/1.1 -> HTTP 403.\n"
    "So the discriminator is PROTOCOL plus HEADER COMPLETENESS, precisely the Paragon finding in rule 9: try "
    "--http1.1 with a complete header set before writing any sentence about what a host does.\n"
    "  • HONEST QUALIFIER, recorded because it changes what may be concluded: a REPEAT of the identical winning "
    "rung minutes later returned 403 again. The host is INTERMITTENT, not simply unlocked. One 200 is enough to "
    "refute 'refuses every request'; it is NOT enough to call the host reachable, and a future session should "
    "expect to retry rather than to succeed first time.\n"
    "  • www.itaubba.co.uk - the domain this bank's own Annual Report names as the home of the Pillar 3 "
    "Disclosures - is ALIVE, contrary to the 'connection refused/timed out' wording elsewhere in this script. "
    "DNS resolves (94.126.169.4 on both apex and www). Port 443 times out on every rung tried. PORT 80 ANSWERS: "
    "HTTP 302, Server nginx/1.22.1, X-Powered-By PHP/7.2.2, Location "
    "https://www.itau.com.br/itaubba-en/international. That redirect target is an HTML page on a different path "
    "from the DAM file host, and it returned 403 to every rung including the winning one, which is why the "
    "FY2024 and FY2025 Pillar 3 URLs still could not be listed.\n"
    "  • The Internet Archive was DEGRADED during this session (an 'Internet Archive: Temporarily Offline' page, "
    "and HTTP 429 on the availability API), so its silence is an OUTAGE and carries no evidential weight either "
    "way."
)

def pillar3_disclosure_sources(note_extra=""):
    return (
        "Source — Itau BBA International plc Group (consolidated) standalone Pillar 3 Disclosures documents — "
        "these are the same documents the Annual Report's own 'Capital' section refers readers to via "
        "www.itaubba.co.uk (see the p3_sources note on this workbook's other Pillar 3 sheets); that domain, and "
        "itau.co.uk, were unreachable this session, but the documents themselves were located on itau.com.br "
        "(the Brazilian parent Itau Unibanco's investor-relations site). Live fetches of itau.com.br also "
        "returned HTTP 403 this session (Cloudflare bot-challenge), so all figures below were retrieved via "
        "Wayback Machine archive snapshots instead:\n"
        f"FY2023: 'Market Discipline – 2023 Pillar III' (2023 Pillar 3 Disclosures), Template UK KM1 (Section 10 "
        f"'Key Metrics'), p.41 — live: {PILLAR3_2023_URL} — archived: {PILLAR3_2023_WAYBACK}\n"
        f"FY2022 (and FY2021 comparative column on the same table): '2022 Pillar 3 Disclosures', Template UK KM1 "
        f"(Section 10 'Key Metrics'), p.44 — live: {PILLAR3_2022_URL} — archived: {PILLAR3_2022_WAYBACK}\n"
        f"FY2021 LCR only (the 2021 document predates the UK KM1 template): '2021 Pillar 3 Disclosures', Table 26 "
        f"'Liquidity Coverage Ratio', p.46 — live: {PILLAR3_2021_URL} — archived: {PILLAR3_2021_WAYBACK}\n"
        "All figures are Group/consolidated (IBBAInt Group) basis, matching this workbook's other Pillar 3 sheets. "
        "FY2024/FY2025: no standalone Pillar 3 Disclosures document for either year has been obtained (see the "
        "host-reach correction below). THE TRAILING CLAUSE PREVIOUSLY HERE — that 'the Annual Report itself does "
        "not break out these figures for any year' — IS FALSE AND IS WITHDRAWN (GA-018, 2026-09-18). Each year's "
        "own Annual Report states BOTH the LCR and the NSFR, and the FY2025 and FY2024 figures on the LCR and "
        "NSFR sheets are now sourced from there. The false clause is exactly the self-sealing negative of "
        "km1/map.md rule 40: it explained the blanks well enough that nobody re-opened the document, and it was "
        "the neighbouring sheets' own Annual-Report sourcing (FY2015-FY2020) that should have contradicted it all "
        "along. The KM1 sheet stays blank for those two years regardless, because a KM1 is a TABLE and the Annual "
        "Report prints no key-metrics template — mapping its prose onto template row numbers would assert a "
        "correspondence the bank never published (rule 8).\n\n" +
        BLOCKED_HOST_NOTE +
        (" " + note_extra if note_extra else "")
    )

def p3_sources(page, doc_label, url, note_extra=""):
    return (
        f"Source — Itau BBA International plc Group (consolidated) regulatory capital summary, {doc_label} "
        f"Annual Report, p.{page} ('Capital' section of the Strategic Report) — {url}\n"
        "The Annual Report states in full that additional Pillar 3 Disclosures (capital detail, LCR, NSFR, MREL) "
        "are published as a separate, standalone unaudited document on www.itaubba.co.uk — that site was "
        "unreachable this session (connection refused/timed out; no usable Wayback Machine snapshot found), so "
        "only the summary figures printed directly in the Annual Report's own 'Capital' section are used here. "
        "Figures are Group/consolidated basis (the Annual Report's Capital section is presented at Group level "
        "only, not solo Bank level, throughout all 5 years)." + (" " + note_extra if note_extra else "")
    )

bw = BankWorkbook(bank_name="Itau BBA International plc", years=Y_CORE, year_label={y: y for y in YEARS}, header_color="F58220")

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 17, "FY2024": 16, "FY2023": 16, "FY2022": 15, "FY2021": 16, "FY2020": 15, "FY2019": 401875, "FY2018": 809786, "FY2017": 574246, "FY2016": 16750, "FY2015": 817, "FY2014": 1307, "FY2013": 1380}),
    ("DATA", "Trading assets", {"FY2025": 10362, "FY2024": 6920, "FY2023": 11783, "FY2022": 12227, "FY2021": 20508, "FY2020": 27431, "FY2019": 49862, "FY2018": 49523, "FY2017": 140450, "FY2016": 163278, "FY2015": 105991, "FY2014": 195901, "FY2013": 158774}),
    ("DATA", "Financial assets designated at fair value through profit or loss", {"FY2024": 44509, "FY2023": 49259, "FY2022": 438169, "FY2021": 1022915, "FY2020": 1237426, "FY2019": 308020, "FY2018": 395983, "FY2017": 687126, "FY2016": 444390, "FY2015": 204368, "FY2014": 275784, "FY2013": 158276}),
    ("DATA", "Financial assets measured at fair value through OCI", {"FY2025": 1735647, "FY2024": 1824171, "FY2023": 2029771, "FY2022": 1175521, "FY2020": 0, "FY2019": 276047}),
    ("DATA", "Financial assets available for sale", {"FY2018": 0, "FY2017": 301336, "FY2016": 302717, "FY2015": 342258, "FY2014": 337948}),
    ("DATA", "Derivative financial instruments", {"FY2025": 402429, "FY2024": 489006, "FY2023": 264447, "FY2022": 414210, "FY2021": 402295, "FY2020": 335193, "FY2019": 216982, "FY2018": 244608, "FY2017": 315430, "FY2016": 231558, "FY2015": 542604, "FY2014": 452290, "FY2013": 251894}),
    ("DATA", "Loans and advances to banks", {"FY2025": 890765, "FY2024": 1714874, "FY2023": 1122546, "FY2022": 665708, "FY2021": 658659, "FY2020": 553156, "FY2019": 513070, "FY2018": 696054, "FY2017": 349304, "FY2016": 573263, "FY2015": 927460, "FY2014": 489512, "FY2013": 1069983}),
    ("DATA", "Loans and advances to customers", {"FY2025": 4044575, "FY2024": 4104314, "FY2023": 3868767, "FY2022": 3604470, "FY2021": 3221895, "FY2020": 3181399, "FY2019": 3864886, "FY2018": 3779281, "FY2017": 3056151, "FY2016": 2782210, "FY2015": 3179457, "FY2014": 2855295, "FY2013": 2334930}),
    ("DATA", "Debt securities at amortised cost", {"FY2023": 2192, "FY2021": 2192}),
    ("DATA", "Property, plant and equipment", {"FY2025": 390, "FY2024": 1188, "FY2023": 2007, "FY2022": 570, "FY2021": 1672, "FY2020": 625, "FY2019": 4221, "FY2018": 4811, "FY2017": 4748, "FY2016": 7384, "FY2015": 9048, "FY2014": 9906, "FY2013": 10115}),
    ("DATA", "Goodwill and intangible assets", {"FY2025": 7, "FY2024": 37, "FY2023": 7, "FY2022": 291, "FY2021": 183, "FY2020": 291, "FY2019": 297, "FY2018": 204, "FY2017": 261, "FY2016": 348, "FY2015": 658, "FY2014": 860, "FY2013": 642}),
    ("DATA", "Investments in subsidiaries", {"FY2025": 803125, "FY2024": 743998, "FY2023": 719482, "FY2022": 629248, "FY2021": 627841, "FY2020": 585738, "FY2019": 531772, "FY2018": 512112, "FY2017": 512112, "FY2016": 512112, "FY2015": 538943, "FY2014": 541625, "FY2013": 473653}),
    ("DATA", "Current tax assets", {"FY2025": 0, "FY2024": 1107, "FY2023": 1148, "FY2022": 55, "FY2021": 1143, "FY2020": 1836, "FY2019": 27, "FY2018": 0, "FY2017": 0, "FY2016": 333, "FY2015": 356, "FY2014": 921, "FY2013": 3449}),
    ("DATA", "Deferred tax assets", {"FY2025": 2970, "FY2024": 2528, "FY2023": 2675, "FY2022": 2637, "FY2021": 1070, "FY2020": 1496, "FY2019": 1606, "FY2018": 1834, "FY2017": 2389, "FY2016": 2549, "FY2015": 2882, "FY2014": 4977, "FY2013": 2958}),
    ("DATA", "Other assets", {"FY2025": 5947, "FY2024": 4515, "FY2023": 13667, "FY2022": 38860, "FY2021": 3125, "FY2020": 6472, "FY2019": 8554, "FY2018": 9439, "FY2017": 9794, "FY2016": 6114, "FY2015": 13756, "FY2014": 11094, "FY2013": 28878}),
    ("TOTAL", "Total Assets", {"FY2025": 7896227, "FY2024": 8937146, "FY2023": 8085575, "FY2022": 6981727, "FY2021": 5963514, "FY2020": 5931078, "FY2019": 6177219, "FY2018": 6859779, "FY2017": 5953347, "FY2016": 5043006, "FY2015": 5868598, "FY2014": 5177420, "FY2013": 4804226}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Trading liabilities", {"FY2025": 10306, "FY2024": 6911, "FY2023": 11786, "FY2022": 9587, "FY2021": 18584, "FY2020": 24694, "FY2019": 48864, "FY2018": 49476, "FY2017": 140419, "FY2016": 159266, "FY2015": 105497, "FY2014": 195787, "FY2013": 158541}),
    ("DATA", "Financial liabilities designated at fair value through profit or loss", {"FY2024": 44456, "FY2023": 49259, "FY2021": 410, "FY2020": 1807, "FY2019": 5402, "FY2018": 12119, "FY2017": 17205}),
    ("DATA", "Derivative financial instruments", {"FY2025": 526233, "FY2024": 462780, "FY2023": 278452, "FY2022": 404354, "FY2021": 405816, "FY2020": 351394, "FY2019": 228126, "FY2018": 245399, "FY2017": 315578, "FY2016": 241506, "FY2015": 544015, "FY2014": 442663, "FY2013": 287438}),
    ("DATA", "Deposits from banks", {"FY2025": 1053183, "FY2024": 925795, "FY2023": 1358652, "FY2022": 837569, "FY2021": 851201, "FY2020": 1396331, "FY2019": 1431447, "FY2018": 2076646, "FY2017": 1490689, "FY2016": 804465, "FY2015": 1454042, "FY2014": 882495, "FY2013": 1110038}),
    ("DATA", "Customer accounts", {"FY2025": 1740013, "FY2024": 2745061, "FY2023": 1709639, "FY2022": 1914084, "FY2021": 1751887, "FY2020": 1242218, "FY2019": 1304375, "FY2018": 1194983, "FY2017": 752508, "FY2016": 453090, "FY2015": 176000, "FY2014": 204392, "FY2013": 217286}),
    ("DATA", "Debt securities in issue", {"FY2025": 2364797, "FY2024": 2613477, "FY2023": 2688433, "FY2022": 2373670, "FY2021": 1571907, "FY2020": 1580814, "FY2019": 1814008, "FY2018": 2014685, "FY2017": 2083476, "FY2016": 2266682, "FY2015": 2502404, "FY2014": 2259901, "FY2013": 1904488}),
    ("DATA", "Provisions", {"FY2025": 236, "FY2024": 258, "FY2023": 319, "FY2022": 525, "FY2021": 428, "FY2020": 2937, "FY2019": 1181, "FY2018": 587, "FY2017": 1596, "FY2016": 1330, "FY2015": 183, "FY2014": 308, "FY2013": 163}),
    ("DATA", "Current tax liabilities", {"FY2025": 285, "FY2024": 1186, "FY2023": 0, "FY2022": 15, "FY2021": 580, "FY2020": 43, "FY2019": 6745, "FY2018": 6617, "FY2017": 3576, "FY2016": 3354, "FY2015": 883, "FY2014": 413, "FY2013": 27}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 54, "FY2024": 101, "FY2023": 315, "FY2022": 20, "FY2021": 29, "FY2020": 16, "FY2019": 16, "FY2018": 18, "FY2017": 0, "FY2016": 144, "FY2015": 260, "FY2014": 240}),
    ("DATA", "Subordinated liabilities", {"FY2016": 30128, "FY2015": 30071, "FY2014": 30055, "FY2013": 30059}),
    ("DATA", "Other liabilities", {"FY2025": 46646, "FY2024": 74207, "FY2023": 25004, "FY2022": 43366, "FY2021": 32798, "FY2020": 26927, "FY2019": 37261, "FY2018": 29811, "FY2017": 25449, "FY2016": 36832, "FY2015": 31502, "FY2014": 151288, "FY2013": 83565}),
    ("TOTAL", "Total Liabilities", {"FY2025": 5741753, "FY2024": 6874232, "FY2023": 6121859, "FY2022": 5583190, "FY2021": 4633640, "FY2020": 4627181, "FY2019": 4878425, "FY2018": 5630341, "FY2017": 4830496, "FY2016": 3996797, "FY2015": 4844857, "FY2014": 4167542, "FY2013": 3791605}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called-up share capital", {"FY2025": 1221034, "FY2024": 1221034, "FY2023": 1221034, "FY2022": 935000, "FY2021": 600000, "FY2020": 600000, "FY2019": 600000, "FY2018": 600000, "FY2017": 600000, "FY2016": 600000, "FY2015": 600000, "FY2014": 600000, "FY2013": 600000}),
    ("DATA", "Share premium", {"FY2025": 213966, "FY2024": 213966, "FY2023": 213966, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Revaluation reserves", {"FY2025": 205, "FY2024": -1273, "FY2023": -1644, "FY2022": -4029, "FY2021": 53, "FY2020": 0, "FY2019": -345, "FY2018": -3273, "FY2017": -4223, "FY2016": -3902, "FY2015": -1091, "FY2014": 1706, "FY2013": -1786}),
    ("DATA", "Other reserves", {"FY2022": 0, "FY2021": 332948, "FY2020": 332948, "FY2019": 332948, "FY2018": 324856, "FY2017": 324856, "FY2016": 324856, "FY2015": 324856, "FY2014": 324856, "FY2013": 324856}),
    ("DATA", "Retained earnings (including profit for the year)", {"FY2025": 719269, "FY2024": 629187, "FY2023": 530360, "FY2022": 467566, "FY2021": 396873, "FY2020": 370949, "FY2019": 366191, "FY2018": 307855, "FY2017": 202218, "FY2016": 125255, "FY2015": 99976, "FY2014": 83316, "FY2013": 89551}),
    ("TOTAL", "Total Equity", {"FY2025": 2154474, "FY2024": 2062914, "FY2023": 1963716, "FY2022": 1398537, "FY2021": 1329874, "FY2020": 1303897, "FY2019": 1298794, "FY2018": 1229438, "FY2017": 1122851, "FY2016": 1046209, "FY2015": 1023741, "FY2014": 1009878, "FY2013": 1012621}),
    ("TOTAL", "Total Liabilities and Equity", {"FY2025": 7896227, "FY2024": 8937146, "FY2023": 8085575, "FY2022": 6981727, "FY2021": 5963514, "FY2020": 5931078, "FY2019": 6177219, "FY2018": 6859779, "FY2017": 5953347, "FY2016": 5043006, "FY2015": 5868598, "FY2014": 5177420, "FY2013": 4804226}),
]

bw.add_balance_sheet_sheet(
    title="Itau BBA International plc — Balance Sheet (Bank, solo)",
    subtitle="Itau BBA International plc (Bank/solo basis, not Group), USD'000 unless stated",
    rows=balance_sheet_rows,
    sources_text=statement_sources(61, "2025", AR25_URL) + "\n\n"
        + statement_sources(53, "2023", AR23_URL, "Covers FY2023/FY2022.") + "\n\n"
        + statement_sources(52, "2021", AR21_URL, "Covers FY2021 (FY2020 comparative not used). "
            "'Other reserves' only appears as a distinct line for FY2021 - subsequently merged/relabelled; "
            "'Financial assets designated at fair value through profit or loss' and 'Debt securities at "
            "amortised cost' are genuinely nil/blank for FY2025 and FY2022/FY2023/FY2020 respectively per each "
            "year's own disclosure, not omissions.") + "\n\n"
        + statement_sources(46, "2020", AR20_URL, "Covers FY2020/FY2019.") + "\n\n"
        + statement_sources(30, "2018", AR18_URL, "Covers FY2018/FY2017.") + "\n\n"
        + statement_sources(24, "2016", AR16_URL, "Covers FY2016/FY2015.") + "\n\n"
        + statement_sources(27, "2014", AR14_URL, "Covers FY2014 (the Bank-solo standalone report within the "
            "combined filing) and, per HD-072 (2026-09-06), its own FY2013 comparative column on the same page. "
            "'Financial assets available for sale' is this era's label for what later becomes 'Financial assets "
            "measured at fair value through OCI' post-IFRS 9 (1 Jan 2018) - shown as separate rows since the "
            "categories aren't identical, not merged. 'Subordinated liabilities' is present FY2013-2016 and "
            "genuinely absent from FY2017 onward (a real repayment/maturity event, not an omission) - confirmed by "
            "reading each year's own note in full. 'Financial liabilities designated at fair value through profit "
            "or loss' is genuinely absent as a distinct Balance Sheet line in FY2013 (this era's Balance Sheet did "
            "not break it out separately) - not an omission. 'Deferred tax liabilities' is genuinely nil/blank for "
            "FY2013 per the source's own '-' entry."),
    first_col_width=68,
    source_height=190,
    unit_suffix=" (USD'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 355575, "FY2024": 419820, "FY2023": 365401, "FY2022": 148478, "FY2021": 87382, "FY2020": 123207, "FY2019": 185078, "FY2018": 178374, "FY2017": 137523, "FY2016": 150124, "FY2015": 133084, "FY2014": 100510, "FY2013": 79959}),
    ("DATA", "Interest expense", {"FY2025": -280371, "FY2024": -317737, "FY2023": -278379, "FY2022": -94759, "FY2021": -47981, "FY2020": -87133, "FY2019": -139462, "FY2018": -119963, "FY2017": -77860, "FY2016": -92584, "FY2015": -73742, "FY2014": -58667, "FY2013": -48510}),
    ("TOTAL", "Net interest income", {"FY2025": 75204, "FY2024": 102083, "FY2023": 87022, "FY2022": 53719, "FY2021": 39401, "FY2020": 36074, "FY2019": 45616, "FY2018": 58411, "FY2017": 59663, "FY2016": 57540, "FY2015": 59342, "FY2014": 41843, "FY2013": 31449}),
    ("DATA", "Fee and commission income", {"FY2025": 9457, "FY2024": 11268, "FY2023": 10932, "FY2022": 13581, "FY2021": 12554, "FY2020": 8449, "FY2019": 8437, "FY2018": 14478, "FY2017": 7173, "FY2016": 11576, "FY2015": 9859, "FY2014": 13152, "FY2013": 12485}),
    ("DATA", "Fee and commission expense", {"FY2025": -6329, "FY2024": -8787, "FY2023": -11488, "FY2022": -12687, "FY2021": -17808, "FY2020": -11279, "FY2019": -9369, "FY2018": -8638, "FY2017": -12275, "FY2016": -13792, "FY2015": -9460, "FY2014": -3488, "FY2013": -4199}),
    ("TOTAL", "Net fee and commission income / (expense)", {"FY2025": 3128, "FY2024": 2481, "FY2023": -556, "FY2022": 894, "FY2021": -5254, "FY2020": -2830, "FY2019": -932, "FY2018": 5840, "FY2017": -5102, "FY2016": -2216, "FY2015": 399, "FY2014": 9664, "FY2013": 8286}),
    ("DATA", "Net income on financial assets and liabilities at fair value through profit or loss", {"FY2025": 66407, "FY2024": 45201, "FY2023": 19474, "FY2022": 32120, "FY2020": 14485, "FY2019": 39915, "FY2018": 20035, "FY2017": 11255, "FY2016": 9854, "FY2015": 7041, "FY2014": 9434, "FY2013": 16656}),
    ("DATA", "Net income / (expense) on financial assets at fair value through OCI", {"FY2025": -89, "FY2024": -778, "FY2023": 985, "FY2022": -57, "FY2020": 2492, "FY2019": 20, "FY2018": -174, "FY2017": -305, "FY2016": 1716, "FY2015": 1857, "FY2014": 605, "FY2013": 441}),
    ("DATA", "Dividend income", {"FY2024": 5, "FY2023": 0, "FY2022": 20004, "FY2021": 23797, "FY2020": 5, "FY2019": 20004, "FY2018": 64500, "FY2017": 50000, "FY2014": 6474, "FY2013": 85962}),
    ("DATA", "Net income on other financial operations", {"FY2025": 8208, "FY2024": 9387, "FY2023": 7943, "FY2022": 4469, "FY2021": 5590, "FY2020": 5339, "FY2019": 7110, "FY2018": 5206, "FY2017": -22, "FY2016": 2326, "FY2015": 3147, "FY2014": 2617, "FY2013": 2773}),
    ("TOTAL", "Net income on financial operations", {"FY2025": 74526, "FY2024": 53811, "FY2023": 28402, "FY2022": 56536, "FY2021": 29192, "FY2020": 22321, "FY2019": 67049, "FY2018": 89567, "FY2017": 60928, "FY2016": 13896, "FY2015": 12045, "FY2014": 19130, "FY2013": 105832}),
    ("DATA", "Other operating income", {"FY2025": 5050, "FY2024": 5344, "FY2023": 6806, "FY2022": 6646, "FY2021": 7438, "FY2020": 8604, "FY2019": 11483, "FY2018": 11176, "FY2017": 8937, "FY2016": 8162, "FY2015": 6361, "FY2014": 10132, "FY2013": 2149}),
    ("TOTAL", "Total operating income", {"FY2025": 157908, "FY2024": 163719, "FY2023": 121674, "FY2022": 117795, "FY2021": 70777, "FY2020": 64169, "FY2019": 123216, "FY2018": 164994, "FY2017": 124426, "FY2016": 77382, "FY2015": 78147, "FY2014": 80769, "FY2013": 147716}),
    ("DATA", "Credit impairment reversals / (charges) and other provisions", {"FY2025": 64, "FY2024": 306, "FY2023": -6669, "FY2022": 4188, "FY2021": 9753, "FY2020": -22264, "FY2019": -1893, "FY2018": 1272, "FY2017": 3702, "FY2016": -651, "FY2015": -2531, "FY2014": -20294, "FY2013": -4845}),
    ("TOTAL", "Net operating income", {"FY2025": 157972, "FY2024": 164025, "FY2023": 115005, "FY2022": 121983, "FY2021": 80530, "FY2020": 41905, "FY2019": 121688, "FY2018": 166266, "FY2017": 128128, "FY2016": 76731, "FY2015": 75616, "FY2014": 60475, "FY2013": 142871}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -20143, "FY2024": -15973, "FY2023": -17838, "FY2022": -19576, "FY2021": -19475, "FY2020": -25591, "FY2019": -37325, "FY2018": -34865, "FY2017": -29637, "FY2016": -30945, "FY2015": -36441, "FY2014": -45380, "FY2013": -34830}),
    ("DATA", "General and administrative expenses", {"FY2025": -16306, "FY2024": -14730, "FY2023": -12211, "FY2022": -11842, "FY2021": -11634, "FY2020": -7305, "FY2019": -9143, "FY2018": -10962, "FY2017": -10920, "FY2016": -10531, "FY2015": -14065, "FY2014": -17895, "FY2013": -13146}),
    ("DATA", "Depreciation and impairment of property, plant and equipment", {"FY2025": -831, "FY2024": -852, "FY2023": -969, "FY2022": -1135, "FY2021": -1107, "FY2020": -1301, "FY2019": -2743, "FY2018": -1487, "FY2017": -2861, "FY2016": -1748, "FY2015": -1725, "FY2014": -1689, "FY2013": -1352}),
    ("DATA", "Amortisation and impairment of intangible assets", {"FY2024": -7, "FY2023": -30, "FY2022": -145, "FY2021": -169, "FY2020": -170, "FY2019": -129, "FY2018": -187, "FY2017": -245, "FY2016": -387, "FY2015": -477, "FY2014": -507, "FY2013": -427}),
    ("DATA", "Other operating expenses", {"FY2025": -525, "FY2024": -660, "FY2023": -432, "FY2022": -408, "FY2021": -668, "FY2020": -1422, "FY2019": -907, "FY2018": -1061, "FY2017": -1211, "FY2016": -1225, "FY2015": -1437, "FY2014": -1163, "FY2013": -2067}),
    ("TOTAL", "Total operating expenses", {"FY2025": -37805, "FY2024": -32222, "FY2023": -31480, "FY2022": -33106, "FY2021": -33053, "FY2020": -35789, "FY2019": -50247, "FY2018": -48562, "FY2017": -44874, "FY2016": -44836, "FY2015": -54145, "FY2014": -66634, "FY2013": -51822}),
    ("TOTAL", "Profit before tax", {"FY2025": 120167, "FY2024": 131803, "FY2023": 83525, "FY2022": 88877, "FY2021": 47477, "FY2020": 6116, "FY2019": 71441, "FY2018": 117704, "FY2017": 83254, "FY2016": 31895, "FY2015": 21471, "FY2014": -6159, "FY2013": 91049}),
    ("DATA", "Income tax", {"FY2025": -30085, "FY2024": -32976, "FY2023": -20731, "FY2022": -16132, "FY2021": -4467, "FY2020": -1358, "FY2019": -12105, "FY2018": -12163, "FY2017": -6291, "FY2016": -6616, "FY2015": -4811, "FY2014": -76, "FY2013": -1623}),
    ("TOTAL", "Profit for the year", {"FY2025": 90082, "FY2024": 98827, "FY2023": 62794, "FY2022": 72745, "FY2021": 43010, "FY2020": 4758, "FY2019": 59336, "FY2018": 105541, "FY2017": 76963, "FY2016": 25279, "FY2015": 16660, "FY2014": -6235, "FY2013": 89426}),
]

bw.add_income_statement_sheet(
    title="Itau BBA International plc — Income Statement (Bank, solo)",
    subtitle="Itau BBA International plc (Bank/solo basis, not Group), USD'000 unless stated",
    rows=income_statement_rows,
    sources_text=statement_sources(62, "2025", AR25_URL) + "\n\n"
        + statement_sources(54, "2023", AR23_URL, "Covers FY2023/FY2022.") + "\n\n"
        + statement_sources(53, "2021", AR21_URL, "Covers FY2021. FY2021's report structures "
            "Interest income/expense as single lines (no 'using effective interest rate method' sub-split "
            "shown from FY2022 onward) - both years' Net interest income tie exactly regardless.") + "\n\n"
        + statement_sources(43, "2020", AR20_URL, "Covers FY2020/FY2019.") + "\n\n"
        + statement_sources(31, "2018", AR18_URL, "Covers FY2018/FY2017. Dividend income of USD 64,500k (2018) "
            "and USD 50,000k (2017) reflects real related-party dividends from subsidiaries, not an anomaly - "
            "confirmed against the Investments in subsidiaries note.") + "\n\n"
        + statement_sources(25, "2016", AR16_URL, "Covers FY2016/FY2015.") + "\n\n"
        + statement_sources(28, "2014", AR14_URL, "Covers FY2014 (Bank-solo standalone report) and, per HD-072 "
            "(2026-09-06), its own FY2013 comparative column on the same page. FY2014's Profit/(loss) for the "
            "year of USD (6,235)k is a genuine Bank-level loss, driven by a USD 20,294k credit impairment charge "
            "against a much smaller dividend income than FY2013's own one-off USD 85,962k dividend (the latter "
            "reflecting a large distribution ahead of the 2013 merger) - confirmed by reading the note in full, "
            "not a transcription anomaly."),
    first_col_width=76,
    source_height=170,
    unit_suffix=" (USD'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Called-up share capital", "Share premium", "Revaluation reserves", "Other reserves", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "Balance as at 1 January 2013 (Bank)", (200000, None, 0, 0, 125, 200125)),
    ("DATA", "Profit for the year", (None, None, None, None, 89426, 89426)),
    ("DATA", "Other comprehensive expense for the year (revaluation reserves)", (None, None, -1786, None, None, -1786)),
    ("DATA", "Share capital of the acquiree on the merger (Note 39/Directors' Report - see source note)", (725771, None, None, None, None, 725771)),
    ("DATA", "Post-merger capital reallocation", (-325771, None, None, 325771, None, 0)),
    ("DATA", "Other movements (reserves)", (None, None, None, -915, None, -915)),
    ("TOTAL", "Balance as at 31 December 2013 / 1 January 2014 (Bank)", (600000, None, -1786, 324856, 89551, 1012621)),
    ("DATA", "Loss for the year", (None, None, None, None, -6235, -6235)),
    ("DATA", "Other comprehensive income for the year (revaluation reserves)", (None, None, 3492, None, None, 3492)),
    ("TOTAL", "Balance as at 31 December 2014", (600000, None, 1706, 324856, 83316, 1009878)),
    ("DATA", "Profit for the year", (None, None, None, None, 16660, 16660)),
    ("DATA", "Other comprehensive expense for the year (revaluation reserves)", (None, None, -2797, None, None, -2797)),
    ("TOTAL", "Balance as at 31 December 2015", (600000, None, -1091, 324856, 99976, 1023741)),
    ("DATA", "Profit for the year", (None, None, None, None, 25279, 25279)),
    ("DATA", "Other comprehensive expense for the year (revaluation reserves)", (None, None, -2811, None, None, -2811)),
    ("TOTAL", "Balance as at 31 December 2016", (600000, None, -3902, 324856, 125255, 1046209)),
    ("DATA", "Profit for the year", (None, None, None, None, 76963, 76963)),
    ("DATA", "Other comprehensive expense for the year (revaluation reserves)", (None, None, -321, None, None, -321)),
    ("TOTAL", "Balance as at 31 December 2017", (600000, None, -4223, 324856, 202218, 1122851)),
    ("DATA", "Impact of initial application of IFRS 9 (Note 2)", (None, None, None, None, 96, 96)),
    ("TOTAL", "Balance as at 1 January 2018 (IFRS 9 transition)", (600000, None, -4223, 324856, 202314, 1122947)),
    ("DATA", "Profit for the year", (None, None, None, None, 105541, 105541)),
    ("DATA", "Other comprehensive income for the year (revaluation reserves)", (None, None, 950, None, None, 950)),
    ("TOTAL", "Balance as at 31 December 2018", (600000, None, -3273, 324856, 307855, 1229438)),
    ("DATA", "Profit for the year", (None, None, None, None, 59336, 59336)),
    ("DATA", "Other comprehensive income for the year (revaluation reserves)", (None, None, 2928, None, None, 2928)),
    ("DATA", "Dividend distribution", (None, None, None, None, -1000, -1000)),
    ("DATA", "Merger with IPI and IEI (Note 27)", (None, None, None, 8092, None, 8092)),
    ("TOTAL", "Balance as at 31 December 2019", (600000, None, -345, 332948, 366191, 1298794)),
    ("DATA", "Profit for the year", (None, None, None, None, 4758, 4758)),
    ("DATA", "Other comprehensive income for the year (revaluation reserves)", (None, None, 345, None, None, 345)),
    ("TOTAL", "Balance as at 31 December 2020 (FY2020 closing, Bank)", (600000, None, 0, 332948, 370949, 1303897)),
    ("DATA", "Profit for the year", (None, None, None, None, 43010, 43010)),
    ("DATA", "Other comprehensive income for the year (cash flow hedge reserve)", (None, None, 53, None, None, 53)),
    ("DATA", "Dividend distribution", (None, None, None, None, -17086, -17086)),
    ("TOTAL", "Balance as at 31 December 2021 (source labels this row \"31 December 2020\" in the Bank's own "
             "equity statement - a genuine labelling error in the primary source, not a transcription error here; "
             "the movements above are unambiguously FY2021's own, and this closing total ties exactly to AR2023's "
             "own restated \"Balances at 1 January 2022\" row)", (600000, None, 53, 332948, 396873, 1329874)),
    ("DATA", "Profit for the year", (None, None, None, None, 72745, 72745)),
    ("DATA", "Other comprehensive income for the year (FVOCI reserves)", (None, None, -4029, None, None, -4029)),
    ("DATA", "Capitalisation of reserves and retained earnings", (335000, None, None, -332948, -2052, 0)),
    ("TOTAL", "Balance as at 31 December 2022 (per FY2023's own restated comparative)", (935000, None, -4029, 0, 467566, 1398537)),
    ("DATA", "Profit for the year", (None, None, None, None, 62794, 62794)),
    ("DATA", "Other comprehensive income for the year (FVOCI + cash flow hedge)", (None, None, 2385, None, None, 2385)),
    ("DATA", "Share capital increase", (286034, 213966, None, None, None, 500000)),
    ("TOTAL", "Balance as at 31 December 2023", (1221034, 213966, -1644, 0, 530360, 1963716)),
    ("DATA", "Profit for the year", (None, None, None, None, 98827, 98827)),
    ("DATA", "Other comprehensive income for the year (FVOCI + own credit + cash flow hedge)", (None, None, 371, None, None, 371)),
    ("TOTAL", "Balance as at 31 December 2024", (1221034, 213966, -1273, 0, 629187, 2062914)),
    ("DATA", "Profit for the year", (None, None, None, None, 90082, 90082)),
    ("DATA", "Other comprehensive income for the year (FVOCI + own credit + cash flow hedge)", (None, None, 1478, None, None, 1478)),
    ("TOTAL", "Balance as at 31 December 2025", (1221034, 213966, 205, 0, 719269, 2154474)),
]

bw.add_equity_changes_sheet(
    title="Itau BBA International plc — Statement of Changes in Equity (Bank, solo)",
    subtitle="Itau BBA International plc (Bank/solo basis, not Group), chronological roll-forward, USD'000",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=statement_sources(64, "2025", AR25_URL) + "\n\n"
        + statement_sources(56, "2023", AR23_URL, "Covers FY2022/FY2023 movements.") + "\n\n"
        + statement_sources(55, "2021", AR21_URL, "Covers FY2021 movements. Reconciliation ladder confirmed: every "
            "year's own closing balance ties exactly to both the next year's own reported opening balance and "
            "that year's own Balance Sheet Total equity, with one exception reproduced as disclosed - the FY2021 "
            "Annual Report's own equity statement mislabels its final closing-balance row \"Balances at 31 "
            "December 2020\" (should read 2021; the movements above it are unambiguously FY2021's, and the "
            "closing total of USD 1,329,874k ties exactly to AR2023's own restated \"Balances at 1 January 2022\" "
            "row) - a genuine source-document labelling error, not a transcription error here.") + "\n\n"
        + statement_sources(45, "2020", AR20_URL, "Covers FY2020/FY2019 movements, incl. FY2019's genuine "
            "USD 1,000,000k dividend distribution to the Bank's then-sole shareholder ('IIH') and the FY2019 "
            "'Merger with IPI and IEI' capital reorganisation (Note 27), both confirmed against the source's own "
            "footnotes.") + "\n\n"
        + statement_sources(34, "2018", AR18_URL, "Covers FY2017/FY2018 movements, including the 1 Jan 2018 "
            "IFRS 9 transition impact (adjustment to fair value of financial assets +94; remeasurement of "
            "modified assets +41; remeasurement of ECL allowance (19); deferred taxes on the above (20); total "
            "impact +96 to retained earnings) - a genuine one-off transition entry per the source's own Note 2, "
            "not a data anomaly.") + "\n\n"
        + statement_sources(27, "2016", AR16_URL, "Covers FY2015/FY2016 movements.") + "\n\n"
        + statement_sources(29, "2014", AR14_URL, "Covers FY2014 movements (Bank-solo standalone report within "
            "the combined filing) and, per HD-072 (2026-09-06), its own FY2013 opening balance and movements from "
            "the same page's second (FY2013) table. FY2013 was the year Itau BBA International plc merged with "
            "its former sister entity - the pre-merger opening balance of USD 200,125k (Share Capital 200,000 + "
            "Retained earnings 125) grows to USD 1,012,621k by 31 Dec 2013 via a genuine one-off 'Share capital of "
            "the acquiree on the merger' contribution of USD 725,771k (immediately reallocated from Share Capital "
            "to Other reserves per 'Post-merger capital reallocation'), not a data anomaly - confirmed against the "
            "Balance Sheet's own FY2013 Total Equity and the Directors' Report's own results/dividends note on the "
            "same 2014 Annual Report. Reconciliation ladder confirmed end to end: every year's own closing balance "
            "from FY2013 through FY2020 ties exactly to both the next year's own reported opening balance and that "
            "year's own Balance Sheet Total Equity, with no year skipped."),
    first_col_width=70,
    source_height=190,
)

# ---------------------------------------------------------------
# Sheet 4: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities (indirect method, FY2015-FY2025)", {}),
    ("DATA", "Profit before tax and dividends", {"FY2025": 120167, "FY2024": 131803, "FY2023": 83525, "FY2022": 68873, "FY2021": 23680, "FY2020": 6111, "FY2019": 51437, "FY2018": 53203, "FY2017": 33254, "FY2016": 31895, "FY2015": 21471}),
    ("DATA", "Credit impairment charges and other provisions", {"FY2025": -64, "FY2024": -306, "FY2023": 6669, "FY2022": -4188, "FY2021": -9753, "FY2020": 22264, "FY2019": 1893, "FY2018": -1272, "FY2017": -3702, "FY2016": 651, "FY2015": 2531}),
    ("DATA", "Depreciation, amortisation and impairment of property, plant, equipment and intangibles", {"FY2025": 831, "FY2024": 852, "FY2023": 999, "FY2022": 1280, "FY2021": 1276, "FY2020": 1472, "FY2019": 2872, "FY2018": 1674, "FY2017": 3106, "FY2016": 2135, "FY2015": 2203}),
    ("DATA", "Other non-cash movements", {"FY2025": -104138, "FY2024": 31363, "FY2023": -33091, "FY2022": 9264, "FY2021": 1017, "FY2020": 67, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": -1429, "FY2015": 0}),
    ("DATA", "Trading assets and financial assets designated at fair value", {"FY2025": 124541, "FY2024": -213757, "FY2023": 501113, "FY2022": 629204, "FY2021": 156038, "FY2020": -749221, "FY2019": 196346, "FY2018": 400641, "FY2017": -300159, "FY2016": 49417, "FY2015": 60768}),
    ("DATA", "Loans and advances to banks", {"FY2025": 135096, "FY2024": -240931, "FY2023": 23043, "FY2022": -200127, "FY2021": 37815, "FY2020": 91151, "FY2019": -75375, "FY2018": -122750, "FY2017": 353239, "FY2016": 361529, "FY2015": -508984}),
    ("DATA", "Balances at central banks (mandatory reserves)", {"FY2021": 0, "FY2020": 401863, "FY2019": 407900, "FY2018": -235535, "FY2017": -557507, "FY2016": -15940, "FY2015": 498}),
    ("DATA", "Loans and advances to customers", {"FY2025": 60053, "FY2024": -235192, "FY2023": -263283, "FY2022": -378299, "FY2021": -32696, "FY2020": 662957, "FY2019": -86994, "FY2018": -722973, "FY2017": -270184, "FY2016": 397743, "FY2015": -323835}),
    ("DATA", "Derivatives designated as hedging instruments (assets)", {"FY2025": 3103, "FY2024": -1190, "FY2023": 38012, "FY2022": -48100, "FY2021": -1705, "FY2020": 530, "FY2019": 2655, "FY2018": -1334, "FY2017": -2541, "FY2016": 201, "FY2015": 428}),
    ("DATA", "Other operating assets", {"FY2025": 17431, "FY2024": 12645, "FY2023": 22312, "FY2022": -33257, "FY2021": 3638, "FY2020": 391, "FY2019": 2780, "FY2018": 96, "FY2017": -3448, "FY2016": 6007, "FY2015": -2662}),
    ("DATA", "Trading liabilities", {"FY2025": 71537, "FY2024": 178116, "FY2023": -113085, "FY2022": -37506, "FY2021": 56410, "FY2020": 90494, "FY2019": -21840, "FY2018": -160709, "FY2017": 55887, "FY2016": -246796, "FY2015": 12109}),
    ("DATA", "Financial liabilities designated at fair value", {"FY2025": -44456, "FY2024": -4802, "FY2023": 49259, "FY2022": -410, "FY2021": -1396, "FY2020": -3595, "FY2019": -6717, "FY2018": -5087, "FY2017": 17205}),
    ("DATA", "Deposits from banks", {"FY2025": 127432, "FY2024": -432800, "FY2023": 521131, "FY2022": -13577, "FY2021": -545052, "FY2020": -35409, "FY2019": -645198, "FY2018": 585957, "FY2017": 686223, "FY2016": -649576, "FY2015": 571546}),
    ("DATA", "Customer accounts", {"FY2025": -994100, "FY2024": 1035388, "FY2023": -204474, "FY2022": 162167, "FY2021": 509622, "FY2020": -61975, "FY2019": 109392, "FY2018": 442475, "FY2017": 299418, "FY2016": 277090, "FY2015": -28392}),
    ("DATA", "Debt securities in issue", {"FY2025": -259630, "FY2024": -75268, "FY2023": 314516, "FY2022": 802330, "FY2021": -8907, "FY2020": -233194, "FY2019": -200677, "FY2018": -68791, "FY2017": -183206, "FY2016": -235722, "FY2015": 242504}),
    ("DATA", "Derivatives designated as hedging instruments (liabilities)", {"FY2025": -4690, "FY2024": 1337, "FY2023": -10618, "FY2022": 27046, "FY2021": -8097, "FY2020": 7603, "FY2019": 4954, "FY2018": -412, "FY2017": -663, "FY2016": -1944, "FY2015": -1047}),
    ("DATA", "Other operating liabilities", {"FY2025": -45452, "FY2024": 46702, "FY2023": -16839, "FY2022": 8370, "FY2021": 4105, "FY2020": -6409, "FY2019": 3016, "FY2018": 4636, "FY2017": -11654, "FY2016": 6970, "FY2015": -117103}),
    ("TOTAL", "Net cash flow from operating activities before payment of income tax", {"FY2025": -792339, "FY2024": 233967, "FY2023": 919189, "FY2022": 993070, "FY2021": 185995, "FY2020": 195100, "FY2019": -253556, "FY2018": 169819, "FY2017": 115268, "FY2016": -17769, "FY2015": -67965}),
    ("DATA", "Income tax paid", {"FY2025": -30862, "FY2024": -31922, "FY2023": -22344, "FY2022": -15859, "FY2021": -2809, "FY2020": -9790, "FY2019": -12364, "FY2018": -8635, "FY2017": -5489, "FY2016": -3063, "FY2015": -1066}),
    ("TOTAL", "Net cash flow from operating activities", {"FY2025": -823201, "FY2024": 202045, "FY2023": 896845, "FY2022": 977211, "FY2021": 183186, "FY2020": 185310, "FY2019": -265920, "FY2018": 161184, "FY2017": 109779, "FY2016": -20832, "FY2015": -69031}),
    ("SECTION", "Cash flows from investing activities (FY2015-FY2025)", {}),
    ("DATA", "Sales/(Purchases) of debt investments at amortised cost", {"FY2022": 2192, "FY2021": -2192}),
    ("DATA", "Purchases of financial assets measured at fair value through OCI", {"FY2025": 90366, "FY2024": 206101, "FY2023": -851115, "FY2022": -1180856}),
    ("DATA", "Sales/(Purchases) of subsidiaries", {"FY2025": -550, "FY2024": -55880, "FY2023": -65061, "FY2022": -10670, "FY2021": -45297, "FY2020": -53697, "FY2019": -19660}),
    ("DATA", "Dividends received", {"FY2024": 1, "FY2022": 20004, "FY2021": 8888, "FY2020": 5, "FY2019": 20004, "FY2018": 64500, "FY2017": 50000}),
    ("DATA", "Sales of fixed assets (initial disposal, source's own duplicate 'Purchases/Sales of fixed assets' label)", {"FY2016": 28975}),
    ("DATA", "Purchases of intangible assets", {"FY2021": -61, "FY2020": -164, "FY2019": -222, "FY2018": -129, "FY2017": -158, "FY2016": -77}),
    ("DATA", "Sales/(Purchases) of fixed assets", {"FY2025": -33, "FY2024": -33, "FY2023": -2406, "FY2022": -33, "FY2021": -2155, "FY2020": 2295, "FY2019": -2154, "FY2018": -1550, "FY2017": -225, "FY2016": -84, "FY2015": -1307}),
    ("TOTAL", "Net cash flow from investing activities", {"FY2025": 89783, "FY2024": 150189, "FY2023": -918582, "FY2022": -1169363, "FY2021": -40817, "FY2020": -51831, "FY2019": -2032, "FY2018": 62821, "FY2017": 49617, "FY2016": -28814, "FY2015": -1307}),
    ("SECTION", "Cash flows from financing activities (FY2015-FY2025)", {}),
    ("DATA", "Dividends paid (financing activities)", {"FY2019": -1000}),
    ("DATA", "Merger with IEI and IPI (financing activities, Note 27)", {"FY2019": 8092}),
    ("DATA", "Leasing Contracts", {"FY2025": -862, "FY2024": -838, "FY2023": 1619, "FY2022": -926, "FY2021": 948, "FY2020": -4131, "FY2019": 4383}),
    ("DATA", "Sub-Lease Contracts", {"FY2020": 1893, "FY2019": -1893}),
    ("DATA", "Issue/(Repayment) of subordinated debt", {"FY2018": 0, "FY2017": -30000}),
    ("DATA", "Interest from financing activities", {"FY2018": 0, "FY2017": -128, "FY2016": 57, "FY2015": 16}),
    ("DATA", "Share Capital Increase", {"FY2023": 500000}),
    ("TOTAL", "Net cash flow from financing activities", {"FY2025": -862, "FY2024": -838, "FY2023": 501619, "FY2022": -926, "FY2021": 948, "FY2020": -2238, "FY2019": 9582, "FY2018": 0, "FY2017": -30128, "FY2016": 57, "FY2015": 16}),
    ("TOTAL", "Increase/(decrease) in cash and cash equivalents", {"FY2025": -734280, "FY2024": 351396, "FY2023": 479882, "FY2022": -193078, "FY2021": 143317, "FY2020": 131241, "FY2019": -258370, "FY2018": 224005, "FY2017": 129268, "FY2016": 7324, "FY2015": -71029}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 1149307, "FY2024": 797911, "FY2023": 318029, "FY2022": 511107, "FY2021": 367790, "FY2020": 236549, "FY2019": 494919, "FY2018": 270914, "FY2017": 141646, "FY2016": 134322, "FY2015": 205351}),
    ("DATA", "Effects of exchange rate change on cash and cash equivalents", {"FY2025": 45560, "FY2024": 0, "FY2021": 0}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 460587, "FY2024": 1149307, "FY2023": 797911, "FY2022": 318029, "FY2021": 511107, "FY2020": 367790, "FY2019": 236549, "FY2018": 270914, "FY2017": 141646, "FY2016": 141646, "FY2015": 134322}),
    ("SECTION", "Cash and cash equivalents comprise (FY2015-FY2025)", {}),
    ("DATA", "Cash and balances at Central Banks", {"FY2025": 17, "FY2024": 16, "FY2023": 16, "FY2022": 15, "FY2021": 16, "FY2020": 15, "FY2019": 12, "FY2018": 23, "FY2017": 17, "FY2016": 29, "FY2015": 36}),
    ("DATA", "Loans and advances to banks with original maturity less than three months", {"FY2025": 460570, "FY2024": 1149291, "FY2023": 797895, "FY2022": 318014, "FY2021": 511091, "FY2020": 367775, "FY2019": 236537, "FY2018": 494896, "FY2017": 270897, "FY2016": 141617, "FY2015": 134286}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 460587, "FY2024": 1149307, "FY2023": 797911, "FY2022": 318029, "FY2021": 511107, "FY2020": 367790, "FY2019": 236549, "FY2018": 270914, "FY2017": 141646, "FY2016": 141646, "FY2015": 134322}),
    ("SECTION", "Cash flows from operating activities (FY2013-FY2014 - DIRECT method; see DATA QUALITY / METHODOLOGY NOTE in the source citation below)", {}),
    ("DATA", "Interest and commissions received", {"FY2014": 112779, "FY2013": 93454}),
    ("DATA", "Interest and commissions paid", {"FY2014": -72127, "FY2013": -77380}),
    ("DATA", "Payments to employees and suppliers", {"FY2014": -60385, "FY2013": -59699}),
    ("TOTAL", "Operating income before changes in operating assets and liabilities", {"FY2014": -19733, "FY2013": -43625}),
    ("DATA", "Trading assets and Financial assets available for sale", {"FY2014": -373900, "FY2013": 89046}),
    ("DATA", "Loans and advances to banks (direct-method)", {"FY2014": 722948, "FY2013": -320626}),
    ("DATA", "Balances at central banks (direct-method)", {"FY2014": 80, "FY2013": -442}),
    ("DATA", "Loans and advances to customers (direct-method)", {"FY2014": -520992, "FY2013": 16120}),
    ("DATA", "Other operating assets (direct-method)", {"FY2014": 28278, "FY2013": 20124}),
    ("DATA", "Trading liabilities (direct-method)", {"FY2014": 197152, "FY2013": -119239}),
    ("DATA", "Deposits from banks (direct-method)", {"FY2014": -224432, "FY2013": 414450}),
    ("DATA", "Customer accounts (direct-method)", {"FY2014": -12851, "FY2013": 48120}),
    ("DATA", "Debt securities in issue (direct-method)", {"FY2014": 362448, "FY2013": -194761}),
    ("DATA", "Other operating liabilities (direct-method)", {"FY2014": -4666, "FY2013": 63371}),
    ("TOTAL", "Changes in operating assets and liabilities", {"FY2014": 174065, "FY2013": 16163}),
    ("TOTAL", "Net cash flow from operating activities before payment of income tax (direct-method)", {"FY2014": 154332, "FY2013": -27462}),
    ("DATA", "Income tax (direct-method)", {"FY2014": -119, "FY2013": 2640}),
    ("TOTAL", "Net cash flow from operating activities (direct-method)", {"FY2014": 154213, "FY2013": -24822}),
    ("SECTION", "Cash flows from investing activities (FY2013-FY2014)", {}),
    ("DATA", "Cash and equivalents acquired in the merger", {"FY2014": 0, "FY2013": 46358}),
    ("DATA", "Dissolution of subsidiaries", {"FY2014": 104, "FY2013": 0}),
    ("DATA", "Subsidiaries' capital increase", {"FY2014": -70000, "FY2013": 0}),
    ("DATA", "Dividends received (direct-method section)", {"FY2014": 6474, "FY2013": 85962}),
    ("DATA", "Purchase of fixed assets (direct-method section)", {"FY2014": -3215, "FY2013": -4417}),
    ("TOTAL", "Net cash flow from investing activities (direct-method section)", {"FY2014": -66637, "FY2013": 127903}),
    ("SECTION", "Cash flows from financing activities (FY2013-FY2014)", {}),
    ("DATA", "Purchases/(Sales) of subordinated debt (direct-method section)", {"FY2014": 0, "FY2013": 30000}),
    ("DATA", "Interest paid from financing activities (direct-method section)", {"FY2014": -221, "FY2013": -142}),
    ("TOTAL", "Net cash flow from financing activities (direct-method section)", {"FY2014": -221, "FY2013": 29858}),
    ("DATA", "Effects of exchange rate change on cash and cash equivalents (direct-method section)", {"FY2014": -13823, "FY2013": -1120}),
    ("TOTAL", "Increase/(decrease) in cash and cash equivalents (direct-method section)", {"FY2014": 73532, "FY2013": 131819}),
    ("DATA", "Cash and cash equivalents at beginning of year (direct-method section)", {"FY2014": 131819, "FY2013": 0}),
    ("TOTAL", "Cash and cash equivalents at end of year (direct-method section)", {"FY2014": 205351, "FY2013": 131819}),
    ("SECTION", "Cash and cash equivalents comprise (FY2013-FY2014)", {}),
    ("DATA", "Cash (direct-method section)", {"FY2014": 29, "FY2013": 22}),
    ("DATA", "Loans and advances to banks repayable on demand (direct-method section)", {"FY2014": 205322, "FY2013": 131797}),
    ("TOTAL", "Cash and cash equivalents at end of year (direct-method section, comprise)", {"FY2014": 205351, "FY2013": 131819}),
]

bw.add_cash_flow_sheet(
    title="Itau BBA International plc — Statement of Cash Flows (Bank, solo)",
    subtitle="Itau BBA International plc (Bank/solo basis, not Group), USD'000 unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=170,
    unit_suffix=" (USD'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, guarantees and commitments, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 gross maximum exposure", {"FY2025": 4433270, "FY2024": 4784996, "FY2023": 4407196, "FY2022": 3926594, "FY2021": 3347695, "FY2020": 3133226, "FY2019": 4594070, "FY2018": 4477123}),
    ("DATA", "Stage 1 ECL provisions", {"FY2025": -1071, "FY2024": -1135, "FY2023": -1441, "FY2022": -2657, "FY2021": -3212, "FY2020": -2251, "FY2019": -1856, "FY2018": -1474}),
    ("DATA", "Stage 1 cash collateral", {"FY2025": -850, "FY2024": -7303, "FY2023": -15535, "FY2022": -47791, "FY2021": -196179, "FY2020": -471424, "FY2019": -719479, "FY2018": -895973}),
    ("TOTAL", "Stage 1 net exposure", {"FY2025": 4431349, "FY2024": 4776558, "FY2023": 4390220, "FY2022": 3876146, "FY2021": 3148304, "FY2020": 2661802, "FY2019": 3874591, "FY2018": 3581150}),
    ("DATA", "Stage 2 gross maximum exposure", {"FY2025": 38424, "FY2024": 41564, "FY2023": 15922, "FY2022": 152346, "FY2021": 249586, "FY2020": 563149, "FY2019": 32094, "FY2018": 12824}),
    ("DATA", "Stage 2 ECL provisions", {"FY2022": -32, "FY2021": -3665, "FY2020": -14380, "FY2019": -1153, "FY2018": -7}),
    ("DATA", "Stage 2 cash collateral", {"FY2024": -5627, "FY2020": -101442, "FY2019": -17871}),
    ("TOTAL", "Stage 2 net exposure", {"FY2025": 38424, "FY2024": 35937, "FY2023": 15922, "FY2022": 152314, "FY2021": 245921, "FY2020": 461707, "FY2019": 14223, "FY2018": 12824}),
    ("DATA", "Stage 3 gross maximum exposure", {"FY2025": 91484}),
    ("DATA", "Stage 3 cash collateral", {"FY2025": -250}),
    ("TOTAL", "Stage 3 net exposure", {"FY2025": 91234}),
    ("TOTAL", "Total gross maximum exposure", {"FY2025": 4563178, "FY2024": 4826560, "FY2023": 4423118, "FY2022": 4078940, "FY2021": 3597281, "FY2020": 3696375, "FY2019": 4626164, "FY2018": 4489947}),
    ("TOTAL", "Total ECL provisions", {"FY2025": -1071, "FY2024": -1135, "FY2023": -1441, "FY2022": -2689, "FY2021": -6877, "FY2020": -16631, "FY2019": -3009, "FY2018": -1481}),
    ("TOTAL", "Total cash collateral", {"FY2025": -1100, "FY2024": -12930, "FY2023": -15535, "FY2022": -47791, "FY2021": -196179, "FY2020": -572866, "FY2019": -737350, "FY2018": -895973}),
    ("TOTAL", "Total net exposure", {"FY2025": 4561007, "FY2024": 4812495, "FY2023": 4406142, "FY2022": 4028460, "FY2021": 3394225, "FY2020": 3123509, "FY2019": 3888814, "FY2018": 3593974}),
    ("SECTION", "Loans and advances to customers, by IAS 39 category (Bank) - FY2014-FY2016, pre-IFRS 9 (transition 1 Jan 2018); figures as disclosed by the source, USD m (not USD'000 like the rest of this sheet - see source note)", {}),
    ("DATA", "Neither past due nor impaired (USD m)", {"FY2016": 2800, "FY2015": 3198, "FY2014": 2868}),
    ("DATA", "Past due but not impaired (USD m)", {"FY2016": 0, "FY2015": 0, "FY2014": 4}),
    ("DATA", "Impaired (USD m)", {"FY2016": 6, "FY2015": 8, "FY2014": 8}),
    ("DATA", "Commissions related to amortised cost, net (USD m)", {"FY2016": -13, "FY2015": -15, "FY2014": -13}),
    ("TOTAL", "Gross amount of loans and advances to customers (USD m)", {"FY2016": 2793, "FY2015": 3191, "FY2014": 2867}),
    ("DATA", "Loan impairment (USD m)", {"FY2016": -11, "FY2015": -12, "FY2014": -12}),
    ("TOTAL", "Net amount of loans and advances to customers (USD m)", {"FY2016": 2782, "FY2015": 3179, "FY2014": 2855}),
]

bw.add_asset_quality_sheet(
    title="Itau BBA International plc — Asset Quality (Bank, solo)",
    subtitle="Itau BBA International plc (Bank/solo basis, not Group), USD'000 - covers loans and advances to "
             "customers PLUS off-balance-sheet guarantees and commitments (the Bank's own disclosed population "
             "for this note), not just the on-balance loan book, so totals will not tie exactly to the Balance "
             "Sheet's own 'Loans and advances to customers' line",
    rows=asset_quality_rows,
    sources_text=statement_sources(151, "2025", AR25_URL, "'Quality of the portfolio of Loans and advances to "
        "customers, guarantees and committments' table.") + "\n\n"
        + statement_sources(162, "2023", AR23_URL, "Covers FY2023/FY2022 (same table).") + "\n\n"
        + statement_sources(143, "2021", AR21_URL, "Covers FY2021 (same table; FY2020 comparative not used). "
            "As of every year end covered, the Bank had zero Stage 3 exposure except FY2025 (confirmed by reading "
            "each year's own note in full - not a gap, a genuine feature until FY2025's one impaired loan, "
            "covered by guarantees per the Bank's own disclosure).") + "\n\n"
        + statement_sources(46, "2020", AR20_URL, "Covers FY2020/FY2019 (same IFRS 9 stage table).") + "\n\n"
        + statement_sources(35, "2018", AR18_URL, "Covers FY2018 only (same IFRS 9 stage table; this is the first "
            "year under the new IFRS 9 stage-based note format - the FY2018 Annual Report does not restate FY2017 "
            "to this categorisation, IFRS 9 permitting no restatement of prior-year ECL disclosures). SELF-SKIP: "
            "FY2017 Asset Quality is left blank for this reason - the FY2018 Annual Report's own note only shows "
            "31.12.18, and no FY2017-native filing was downloaded this session to source the old IAS 39-format "
            "comparative directly (FY2017's Balance Sheet/Income Statement/Equity/Pillar 3 figures ARE populated, "
            "sourced from this same FY2018 Annual Report's comparative column - only this one sheet's FY2017 "
            "column is affected).") + "\n\n"
        + statement_sources(24, "2016", AR16_URL, "Covers FY2016/FY2015 - pre-IFRS 9 (transition 1 Jan 2018), "
            "'Quality of the portfolio of Loans and advances to customers' note (a narrower population than the "
            "IFRS 9-era note above - customers only, no guarantees/commitments - and disclosed in USD m, not "
            "USD'000; both figures tie exactly to this sheet's Balance Sheet Loans and advances to customers line "
            "when rounded to the nearest USD m).") + "\n\n"
        + statement_sources(27, "2014", AR14_URL, "Covers FY2014 (Bank-solo standalone report; same pre-IFRS 9 "
            "note, USD m). FY2014's one impaired loan (USD 8m) is fully identified in the source's own text as a "
            "single loan to an insolvent subsidiary of a Spanish company, 100% impaired as at 31 Dec 2014 - not a "
            "residual/unexplained balance."),
    first_col_width=64,
    source_height=190,
    unit_suffix=" (USD'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Group/consolidated basis, {unit}" if unit else "Group/consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=150)

# ---------------------------------------------------------------
# KM1 Key Metrics (the bank's own UK KM1 template, reproduced whole).
# Called BEFORE the first add_metric_sheet() so the sheet lands immediately
# after Asset Quality and immediately before CET1 Capital.
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Sources — Itau BBA International plc's own 'Template UK KM1: Key Metrics', reproduced as published. "
    "IBBAInt Group (consolidated basis — the document states the disclosures refer to the IBBAInt Group, "
    "comprising the Bank and its subsidiaries), amounts in thousands of US dollars, the unit the template "
    "itself is printed in.\n"
    f"FY2023: 'Market Discipline - 2023 Pillar III' (2023 Pillar 3 Disclosures), Section 10 'Key Metrics', "
    f"Template UK KM1, p.41, its OWN reporting year — live: {PILLAR3_2023_URL} — archived: {PILLAR3_2023_WAYBACK}\n"
    f"FY2022: '2022 Pillar 3 Disclosures', Section 10 'Key Metrics', Template UK KM1, p.44, its OWN reporting "
    f"year — live: {PILLAR3_2022_URL} — archived: {PILLAR3_2022_WAYBACK}\n"
    f"FY2021: NOT from a FY2021 KM1 — the 2021 Pillar 3 Disclosures document predates the template and prints "
    f"none (see the sheet note). The FY2021 column here is the 2022 edition's own 'Dez 21' COMPARATIVE column, "
    f"p.44 — live: {PILLAR3_2022_URL} — archived: {PILLAR3_2022_WAYBACK}\n"
    "The columns carry the template's own reference letters 'a' (reporting date) and 'e' (comparative), and "
    "the bank heads them 'Dez 22' / 'Dez 21' in Portuguese-style abbreviation; both are 31 December dates.\n\n"
    + BLOCKED_HOST_NOTE
    + "\n\n"
    "ROWS 1, 2 AND 3 ARE EQUAL IN THE SOURCE FOR FY2022 AND FY2021 - READ FROM THE DOCUMENTS ON 2026-09-18 AND "
    "RECORDED HERE SO THE QUESTION IS NOT RE-OPENED. The Pillar 3 2022 edition prints 1,334,422 on rows 1, 2 and "
    "3 for 2022 and 1,317,685 for 2021, and that edition's CC1 row 59, 'Total capital (TC = T1 + T2)', prints the "
    "same 1,334,422 as its row 29 CET1. The FY2021 edition states the reason outright - 'IBBAInt holds no Tier 2 "
    "capital instrument as of December 2021' - with its Tier 2 capital row printed as a dash. FY2023 is DISTINCT "
    "in the source (CET1 1,938,639 against Total capital 1,939,956) and is held that way here. UNIT NOTE, "
    "recorded because it is not otherwise visible on this sheet: the FY2021 edition prints these amounts in GBP "
    "millions (1,319) while the FY2022 edition prints the same date in GBP thousands (1,317,685), and the figure "
    "carried here is the FY2022 edition's comparative column.\n"
)

KM1_NOTE = (
    "FY2025 AND FY2024 ARE BLANK BECAUSE NO PILLAR 3 DOCUMENT FOR EITHER YEAR COULD BE LOCATED — NOT BECAUSE "
    "THE BANK IS KNOWN NOT TO PUBLISH ONE. This is an unknown, not a finding. itau.com.br, which hosts the "
    "three documents cited above, refused every automated request this session (HTTP 403 with a short "
    "text/html WAF body, re-tested with browser user-agent, Accept and Referer headers); itaubba.com timed "
    "out; itau.co.uk returned 403; and the Internet Archive was itself unavailable for part of the session "
    "(HTTP 503 'temporarily offline', then HTTP 429). A blocked host is never evidence of absence.\n"
    "  UPDATED 2026-09-18 (GA-018): the conclusion — these two years are an UNKNOWN, not a finding — is "
    "UNCHANGED and the cells stay EMPTY so the gap remains visible. Two of the supporting claims are not, and "
    "the corrected measurements are in the host-reach correction at the end of this note: itau.com.br did serve "
    "a cited Pillar 3 PDF (HTTP 200, 1,043,167 bytes) on an HTTP/1.1 request with a complete browser header set, "
    "though only intermittently; and www.itaubba.co.uk is alive on port 80 (HTTP 302 to "
    "itau.com.br/itaubba-en/international) rather than refusing connections. POSITIVE EVIDENCE THAT THE "
    "DOCUMENTS EXIST, which strengthens the case for leaving these blank rather than declaring an absence: the "
    "FY2025 Annual Report's own front matter states that the Group presents regulatory capital and risk "
    "information 'in a separate document (\"Pillar 3 Disclosures\")' and that these 'are published on "
    "www.itaubba.co.uk', and its Audit Committee report records that the Committee 'Reviewed the ILAAP, the "
    "ICAAP, the Pillar 3 Disclosures, and recommended their approval to the Board'. A FY2025 Pillar 3 was "
    "therefore prepared and approved; this project simply cannot reach it.\n\n"
    "FY2021 IS FILLED FROM A COMPARATIVE. The 2021 Pillar 3 Disclosures document prints no UK KM1 template at "
    "all — it predates it, disclosing liquidity instead through its own 'Table 26: Liquidity Coverage Ratio'. "
    "A full-text search of that document for 'KM1' and 'key metric' returns nothing while the same document "
    "returns healthy counts on neighbouring prudential terms (countercyclical 9, own funds 5, liquidity "
    "coverage ratio 4, Common Equity Tier 1 4), so the zero is a fact about the document rather than about the "
    "search. Since there is no own-edition table for FY2021 to displace, the column here is the 2022 edition's "
    "own Dez 21 comparative.\n\n"
    "THE LEVERAGE CAPTIONS CHANGE BETWEEN THE TWO EDITIONS AND ARE NOT MERGED. The 2022 edition captions row "
    "13 'Leverage ratio total exposure measure' and row 14 'Leverage ratio'; the 2023 edition captions the "
    "same row numbers 'Total exposure measure excluding claims on central banks' and 'Leverage ratio excluding "
    "claims on central banks'. These are two different exposure bases, so they are shown as two separate "
    "caption blocks with nothing carried across them, even though the row numbers are identical.\n\n"
    "THE UK 14 BLOCK IS A DIFFERENT BLOCK IN EACH EDITION, FOR THE SAME REASON. The 2022 edition prints UK "
    "14a-14f under the heading 'Additional own funds requirements to address risks of excessive leverage', all "
    "six as an explicit 0.00%. The 2023 edition prints UK 14a-14e under a different heading, 'Additional "
    "leverage ratio disclosure requirements', with entirely different row meanings (fully-loaded and "
    "including-central-bank leverage ratios, average leverage ratios, and a countercyclical leverage buffer). "
    "Same numbers, different metrics — they are kept apart. In the 2023 block, UK 14c, 14d and 14e are printed "
    "as a dash and are therefore left BLANK; the 2022 block's zeros are printed zeros and are kept as zeros.\n\n"
    "Row UK 8a appears only in the 2022 edition (printed 0.00%); the 2023 edition omits it. The bank prints "
    "the countercyclical buffer to five decimal places (0.00449%, 0.00171%, 0.00964%) and the LCR and NSFR as "
    "whole percentages; both precisions are its own and are reproduced unchanged. The 2022 edition's NSFR "
    "comparative for Dez 21 is blank with the footnote 'No prior comparative available', the NSFR having only "
    "become a PRA requirement on 1 January 2022 — blank here, not zero. LCR is a trailing average of 12 "
    "month-end observations and NSFR a trailing average of the last four quarter-ends, per each edition's own "
    "footnotes."
)

bw.add_km1_sheet(
    title="Itau BBA International plc — UK KM1 Key Metrics Template",
    subtitle="IBBAInt Group (consolidated basis), as published. Amounts in USD'000; ratios as printed.",
    rows=[
        ("SECTION", "Available own funds (amounts)", {}),
        ("DATA", "1 Common Equity Tier 1 (CET1) capital (USD'000)", {"FY2023": 1938639, "FY2022": 1334422, "FY2021": 1317685}),
        ("DATA", "2 Tier 1 capital (USD'000)", {"FY2023": 1938639, "FY2022": 1334422, "FY2021": 1317685}),
        ("DATA", "3 Total capital (USD'000)", {"FY2023": 1939956, "FY2022": 1334422, "FY2021": 1317685}),
        ("SECTION", "Risk-weighted exposure amounts", {}),
        ("DATA", "4 Total risk-weighted exposure amount (USD'000)", {"FY2023": 7170116, "FY2022": 6811769, "FY2021": 5835714}),
        ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "5 Common Equity Tier 1 ratio (%)", {"FY2023": "27.04%", "FY2022": "19.59%", "FY2021": "22.58%"}),
        ("DATA", "6 Tier 1 ratio (%)", {"FY2023": "27.04%", "FY2022": "19.59%", "FY2021": "22.58%"}),
        ("DATA", "7 Total capital ratio (%)", {"FY2023": "27.06%", "FY2022": "19.59%", "FY2021": "22.58%"}),
        ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "UK 7a Additional CET1 SREP requirements (%)", {"FY2023": "2.16%", "FY2022": "2.13%", "FY2021": "2.23%"}),
        ("DATA", "UK 7b Additional AT1 SREP requirements (%)", {"FY2023": "0.71%", "FY2022": "0.00%", "FY2021": "0.00%"}),
        ("DATA", "UK 7c Additional T2 SREP requirements (%)", {"FY2023": "0.96%", "FY2022": "0.00%", "FY2021": "0.00%"}),
        ("DATA", "UK 7d Total SREP own funds requirements (%)", {"FY2023": "11.83%", "FY2022": "11.83%", "FY2021": "12.03%"}),
        ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "8 Capital conservation buffer (%)", {"FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
        ("DATA", "UK 8a Conservation buffer due to macro-prudential or systemic risk identified at the level of a Member State (%)", {"FY2022": "0.00%", "FY2021": "0.00%"}),
        ("DATA", "9 Institution specific countercyclical capital buffer (%)", {"FY2023": "0.00964%", "FY2022": "0.0045%", "FY2021": "0.00171%"}),
        ("DATA", "UK 9a Systemic risk buffer (%)", {"FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
        ("DATA", "10 Global Systemically Important Institution buffer (%)", {"FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
        ("DATA", "UK 10a Other Systemically Important Institution buffer", {"FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
        ("DATA", "11 Combined buffer requirement (%)", {"FY2023": "2.51%", "FY2022": "2.50%", "FY2021": "2.50%"}),
        ("DATA", "UK 11a Overall capital requirements (%)", {"FY2023": "14.34%", "FY2022": "14.34%", "FY2021": "14.53%"}),
        ("DATA", "12 CET1 available after meeting the total SREP own funds requirements (%)", {"FY2023": "20.41%", "FY2022": "12.96%", "FY2021": "15.84%"}),
        ("SECTION", "Leverage ratio — 2023 edition caption ('excluding claims on central banks')", {}),
        ("DATA", "13 Total exposure measure excluding claims on central banks (USD'000)", {"FY2023": 11582569}),
        ("DATA", "14 Leverage ratio excluding claims on central banks (%)", {"FY2023": "16.74%"}),
        ("SECTION", "Leverage ratio — 2022 edition caption (total exposure measure, no central-bank exclusion stated)", {}),
        ("DATA", "13 Leverage ratio total exposure measure (USD'000)", {"FY2022": 11217813, "FY2021": 9007527}),
        ("DATA", "14 Leverage ratio (%)", {"FY2022": "11.90%", "FY2021": "14.63%"}),
        ("SECTION", "Additional leverage ratio disclosure requirements — 2023 edition block", {}),
        ("DATA", "UK 14a Fully loaded ECL accounting model leverage ratio excluding claims on central banks (%)", {"FY2023": "16.74%"}),
        ("DATA", "UK 14b Leverage ratio including claims on central banks (%)", {"FY2023": "16.74%"}),
        ("DATA", "UK 14c Average leverage ratio excluding claims on central banks (%)", {}),
        ("DATA", "UK 14d Average leverage ratio including claims on central banks (%)", {}),
        ("DATA", "UK 14e Countercyclical leverage ratio buffer (%)", {}),
        ("SECTION", "Additional own funds requirements to address risks of excessive leverage (as a percentage of leverage ratio total exposure amount) — 2022 edition block", {}),
        ("DATA", "UK 14a Additional CET1 leverage ratio requirements (%) [2022 edition block]", {"FY2022": "0.00%", "FY2021": "0.00%"}),
        ("DATA", "UK 14b Additional AT1 leverage ratio requirements (%) [2022 edition block]", {"FY2022": "0.00%", "FY2021": "0.00%"}),
        ("DATA", "UK 14c Additional T2 leverage ratio requirements (%) [2022 edition block]", {"FY2022": "0.00%", "FY2021": "0.00%"}),
        ("DATA", "UK 14d Total SREP leverage ratio requirements (%) [2022 edition block]", {"FY2022": "0.00%", "FY2021": "0.00%"}),
        ("DATA", "UK 14e Applicable leverage buffer [2022 edition block]", {"FY2022": "0.00%", "FY2021": "0.00%"}),
        ("DATA", "UK 14f Overall leverage ratio requirements (%) [2022 edition block]", {"FY2022": "0.00%", "FY2021": "0.00%"}),
        ("SECTION", "Liquidity Coverage Ratio (trailing average of 12 month-end observations)", {}),
        ("DATA", "15 Total high-quality liquid assets (HQLA) (Weighted value - average) (USD'000)", {"FY2023": 1705730, "FY2022": 1767960, "FY2021": 1484567}),
        ("DATA", "UK 16a Cash outflows - Total weighted value (USD'000)", {"FY2023": 1436296, "FY2022": 1612829, "FY2021": 1459720}),
        ("DATA", "UK 16b Cash inflows - Total weighted value (USD'000)", {"FY2023": 616585, "FY2022": 674593, "FY2021": 580600}),
        ("DATA", "16 Total net cash outflows (adjusted value) (USD'000)", {"FY2023": 819710, "FY2022": 938236, "FY2021": 879120}),
        ("DATA", "17 Liquidity coverage ratio (%)", {"FY2023": "208%", "FY2022": "188%", "FY2021": "169%"}),
        ("SECTION", "Net Stable Funding Ratio (trailing average of the last four quarter-ends)", {}),
        ("DATA", "18 Total available stable funding (USD'000)", {"FY2023": 6583126, "FY2022": 6022050}),
        ("DATA", "19 Total required stable funding (USD'000)", {"FY2023": 4097473, "FY2022": 4007354}),
        ("DATA", "20 NSFR ratio (%)", {"FY2023": "161%", "FY2022": "150%"}),
    ],
    sources_text=KM1_SOURCES + "\n\n" + KM1_NOTE,
    first_col_width=104,
    source_height=380,
)

metric(
    "CET1 Capital", "USD m",
    [("Common equity tier 1 (CET1) capital", {"FY2025": 2276, "FY2024": 2073, "FY2023": 1939, "FY2022": 1334, "FY2021": 1318, "FY2020": 1291, "FY2019": 1210, "FY2018": 1127, "FY2017": 1049, "FY2016": 992, "FY2015": 945, "FY2014": 933})],
    p3_sources(21, "2025", AR25_URL) + "\n\nHD-052 (2026-09-05) FY2014-FY2020: same Annual Report 'Regulatory "
        f"Capital composition' table, Group basis — FY2020/FY2019: 2020 Annual Report, p.136 — {AR20_URL}; "
        f"FY2018/FY2017: 2018 Annual Report, p.124 — {AR18_URL}; FY2016/FY2015: 2016 Annual Report, p.102 — "
        f"{AR16_URL}; FY2014: 2014 Consolidated Annual Report, p.10 (FY2013 comparative not used) — {AR14_URL}.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common equity tier 1 ratio", {"FY2025": "29.0%", "FY2024": "23.9%", "FY2023": "27.0%", "FY2022": "19.6%", "FY2021": "22.6%", "FY2020": "23.9%", "FY2019": "19.9%", "FY2018": "19.2%", "FY2017": "19.4%", "FY2016": "18.0%", "FY2015": "17.9%", "FY2014": "17.8%"})],
    p3_sources(21, "2025", AR25_URL) + "\n\nHD-052 (2026-09-05) FY2014-FY2020: same source as the CET1 Capital sheet.",
)

metric(
    "Tier 1 Capital", "USD m",
    [("Tier 1 capital", {"FY2025": 2276, "FY2024": 2073, "FY2023": 1939, "FY2022": 1334, "FY2021": 1318})],
    pillar3_disclosure_sources(),
    note="No distinct Tier 1 capital figure is broken out in the Annual Report's own 'Capital' section in any "
         "year (only 'Common equity tier 1 capital' and 'Total regulatory capital' are shown there — see the "
         "CET1 Capital and Total Capital sheets), but the standalone Pillar 3 Disclosures documents' Template UK "
         "KM1 table does disclose a distinct 'Tier 1 capital' line for FY2023/FY2022/FY2021 — identical to CET1 "
         "capital in every one of those years (Tier 2 capital is nil), confirming the earlier inference. "
         "FY2025/FY2024 added 2026-09-15 and are NOT estimates: still no Pillar 3 Disclosures document for either "
         "year, but in both years the Annual Report's own Capital section states CET1 capital and Total regulatory "
         "capital as the SAME figure (FY2025: USD 2,276m; FY2024: USD 2,073m — see the CET1 Capital and Total "
         "Capital sheets). Since Tier 1 = CET1 + AT1 and Total = Tier 1 + Tier 2, both AT1 and Tier 2 must be nil "
         "and Tier 1 capital is arithmetically forced to that same figure — there is no other value it can take. "
         "This is the same Tier 1 = CET1 = Total pattern the FY2021-FY2023 Pillar 3 KM1 tables confirm directly, "
         "and it is consistent with FY2023, where CET1 (1,939) and Total (1,940) differ by exactly the 1 of Tier 2 "
         "and Tier 1 is the disclosed 1,939. "
         "HD-052 (2026-09-05): FY2014-FY2020 also remain blank — no standalone Pillar 3 Disclosures document for "
         "any of those years was searched for this session (out of scope for this batch); the Annual Report's own "
         "Tier 2 capital line for every one of those years (see the RWA Breakdown/Total Capital sheets) is small "
         "relative to CET1 capital, consistent with the same Tier 1 = CET1 pattern confirmed for FY2021-2023, but "
         "not independently confirmed for FY2014-FY2020.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "29.0%", "FY2024": "23.9%", "FY2023": "27.0%", "FY2022": "19.6%", "FY2021": "22.6%"})],
    pillar3_disclosure_sources(),
    note="Same basis as the Tier 1 Capital sheet — the Annual Report's own 'Capital' section does not break out "
         "a distinct Tier 1 ratio (see the CET1 Ratio and Total Capital Ratio sheets), but the standalone Pillar "
         "3 Disclosures documents' Template UK KM1 table discloses one directly for FY2023/FY2022/FY2021 — "
         "identical to the CET1 ratio and Total capital ratio in every one of those years. "
         "FY2025/FY2024 added 2026-09-15 on the same forced-arithmetic basis as the Tier 1 Capital sheet: in both "
         "years the Annual Report states the CET1 ratio and the Total capital ratio as the same figure (FY2025: "
         "29.0%; FY2024: 23.9%), and since CET1 Ratio <= Tier 1 Ratio <= Total Capital Ratio always holds, the "
         "Tier 1 ratio is squeezed to exactly that value. Not an estimate, and not sourced from a Pillar 3 "
         "document — none exists for either year.",
)

metric(
    "Total Capital", "USD m",
    [("Total regulatory capital", {"FY2025": 2276, "FY2024": 2073, "FY2023": 1940, "FY2022": 1334, "FY2021": 1318, "FY2020": 1291, "FY2019": 1212, "FY2018": 1129, "FY2017": 1051, "FY2016": 1000, "FY2015": 955, "FY2014": 949})],
    p3_sources(21, "2025", AR25_URL) + "\n\nHD-052 (2026-09-05) FY2014-FY2020: same source as the CET1 Capital sheet.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "29.0%", "FY2024": "23.9%", "FY2023": "27.1%", "FY2022": "19.6%", "FY2021": "22.6%", "FY2020": "23.9%", "FY2019": "19.9%", "FY2018": "19.2%", "FY2017": "19.5%", "FY2016": "18.2%", "FY2015": "18.1%", "FY2014": "18.1%"})],
    p3_sources(21, "2025", AR25_URL) + "\n\nHD-052 (2026-09-05) FY2014-FY2020: same source as the CET1 Capital sheet.",
)

metric(
    "Total RWAs", "USD m",
    [("Risk-weighted assets (RWA)", {"FY2025": 7855, "FY2024": 8660, "FY2023": 7170, "FY2022": 6812, "FY2021": 5836, "FY2020": 5408, "FY2019": 6089, "FY2018": 5879, "FY2017": 5399, "FY2016": 5506, "FY2015": 5280, "FY2014": 5232})],
    p3_sources(21, "2025", AR25_URL) + "\n\nHD-052 (2026-09-05) FY2014-FY2020: same source as the CET1 Capital sheet.",
)

# ---------------------------------------------------------------
# RWA Breakdown
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Credit Risk (Standardised Approach; incl. counterparty credit risk)", {"FY2025": 6987.5, "FY2024": 7875.0, "FY2023": 6525.0, "FY2022": 6250.0, "FY2021": 5362.5, "FY2020": 4875.0, "FY2019": 5562.5, "FY2018": 5362.5, "FY2017": 4862.5, "FY2016": 4962.5, "FY2015": 4800.0, "FY2014": 4725.0}),
    ("DATA", "Credit Valuation Adjustment Risk", {"FY2025": 62.5, "FY2024": 37.5, "FY2023": 25.0, "FY2022": 50.0, "FY2021": 25.0, "FY2020": 12.5, "FY2019": 25.0, "FY2018": 12.5, "FY2017": 25.0, "FY2016": 12.5, "FY2015": 25.0, "FY2014": 25.0}),
    ("DATA", "Market Risk", {"FY2025": 12.5, "FY2024": 50.0, "FY2023": 62.5, "FY2022": 25.0, "FY2021": 25.0, "FY2020": 62.5, "FY2019": 12.5, "FY2018": 37.5, "FY2017": 75.0, "FY2016": 100.0, "FY2015": 37.5, "FY2014": 100.0}),
    ("DATA", "Operational Risk (Basic Indicator Approach)", {"FY2025": 787.5, "FY2024": 700.0, "FY2023": 562.5, "FY2022": 487.5, "FY2021": 425.0, "FY2020": 462.5, "FY2019": 487.5, "FY2018": 462.5, "FY2017": 437.5, "FY2016": 425.0, "FY2015": 412.5, "FY2014": 387.5}),
    ("TOTAL", "Total RWA (derived, sum of above)", {"FY2025": 7850.0, "FY2024": 8662.5, "FY2023": 7175.0, "FY2022": 6812.5, "FY2021": 5837.5, "FY2020": 5412.5, "FY2019": 6087.5, "FY2018": 5875.0, "FY2017": 5400.0, "FY2016": 5500.0, "FY2015": 5275.0, "FY2014": 5237.5}),
]

bw.add_rwa_breakdown_sheet(
    title="Itau BBA International plc — RWA Breakdown (Group)",
    subtitle="Group/consolidated basis, USD m - DERIVED, not directly disclosed as a UK OV1 table",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Source — Itau BBA International plc Group 'Capital requirements By Risk Type' table (Note 41 'Capital "
        "Management'/'Capital requirements'), each year's own Annual Report — "
        f"FY2025/FY2024: 2025 Annual Report, p.170 — {AR25_URL}; "
        f"FY2023/FY2022: 2023 Annual Report, p.186 — {AR23_URL}; "
        f"FY2021: 2021 Annual Report, p.163 — {AR21_URL}.\n"
        "The Annual Report discloses capital REQUIREMENTS by risk type (Credit Risk, Credit Valuation Adjustment, "
        "Market Risk, Operational Risk), not RWA directly - each category's RWA here is derived by multiplying "
        "its capital requirement by 12.5 (the same 8% capital ratio convention the Bank's own 'Risk-weighted "
        "assets (RWA)' = 'Total capital requirements' x 12.5 footnote uses on the Total RWAs sheet, and "
        "independently confirmed against AR2021's own 'Risk-weighted assets - Credit Risk' table, p.164, which "
        "discloses Credit Risk RWA directly as USD 5,363m for FY2021 - ties to the derived USD 5,362.5m here "
        "exactly). No standalone Pillar 3 UK OV1 category-level table was found (the Annual Report states further "
        "Pillar 3 disclosures are published separately on www.itaubba.co.uk, which was unreachable this session, "
        "same constraint as the LCR/NSFR/MREL sheets). Each year's derived Total RWA is within ~USD 5m of the "
        "pre-existing Total RWas sheet's disclosed figure (a rounding artifact from the Bank's own capital "
        "requirement figures being rounded to the nearest USD 1m) - not force-reconciled to match exactly.\n"
        "HD-052 (2026-09-05) FY2014-FY2020, same DERIVED methodology, Group basis, from each year's own Annual "
        "Report 'Capital requirements By Risk Type' table — "
        f"FY2020/FY2019: 2020 Annual Report, p.137 — {AR20_URL}; FY2018/FY2017: 2018 Annual Report, p.125 — "
        f"{AR18_URL}; FY2016/FY2015: 2016 Annual Report, p.103 — {AR16_URL}; FY2014: 2014 Consolidated Annual "
        f"Report, p.11 — {AR14_URL}. FY2014's own table nests 'Credit Value Adjustment' (USD 2m) as a sub-line "
        "of 'Market Risk' (USD 10m total) rather than as its own top-level category (introduced as a separate "
        "line from the 2016 report onward) - split out here for consistency with later years (Market Risk shown "
        "as USD 8m ex-CVA, CVA as USD 2m), an apportionment not a data change; both derived figures sum to the "
        "source's own USD 10m Market Risk total exactly."
    ),
    first_col_width=64,
    source_height=200,
    unit_suffix=" (USD m)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2025": "19.1%", "FY2024": "16.4%", "FY2023": "16.7%", "FY2022": "11.9%", "FY2021": "14.6%", "FY2020": "14.4%", "FY2019": "13.5%", "FY2018": "11.9%", "FY2017": "12.4%", "FY2016": "11.3%", "FY2015": "10.3%", "FY2014": "10.5%"})],
    p3_sources(21, "2025", AR25_URL, "The Leverage Ratio is quoted in the Capital section's narrative text (not the composition table) each year.")
        + "\n\nHD-052 (2026-09-05) FY2014-FY2020: same Annual Reports' own Key Performance Indicators tables.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio", {"FY2025": "172%", "FY2024": "302%", "FY2023": "208%", "FY2022": "188%", "FY2021": "169%", "FY2020": "153%", "FY2019": "267%", "FY2018": "181%", "FY2017": "129%", "FY2016": "289%", "FY2015": "307%"})],
    pillar3_disclosure_sources(),
    note="FY2025 AND FY2024 RECOVERED 2026-09-18 (GA-018), FROM THE ANNUAL REPORT — REVERSING THIS SHEET'S OWN "
         "PRIOR CLAIM. Sources, each year from its OWN edition (Companies House filing copies; both are "
         "image-only PDFs and were OCR'd with ocrmypdf --force-ocr before reading):\n"
         "  FY2025: 172% — 2025 Annual Report, 'Performance Highlights' table, row 'Liquidity Coverage Ratio "
         "(LCR)', printed folio 18 (Strategic Report). CORROBORATED within the same edition by the Performance "
         "Review narrative: 'a liquidity coverage ratio of 172% (2024: 302%)'. HQLA eligible USD 2,134m, "
         "liquidity pool USD 4,016m on the same table.\n"
         "  FY2024: 302% — 2024 Annual Report, 'Performance Highlights' table, same row, printed folio 17 "
         "(Strategic Report; the page's own footer reads 'Strategic Report 17'). CORROBORATED twice — by that "
         "edition's own liquidity chart, and by the FY2025 edition quoting 302% as its comparative. HQLA "
         "eligible USD 1,810m.\n"
         "  BASIS BREAK — DO NOT READ THIS SERIES AS ONE MEASURE. FY2025 and FY2024 are POINT-IN-TIME year-end "
         "ratios taken from the Annual Report, exactly like FY2020-FY2015 below; FY2023/FY2022/FY2021 are "
         "12-MONTH TRAILING AVERAGES taken from the Pillar 3 documents, per those documents' own footnotes. The "
         "two are not comparable and are deliberately not reconciled. They are left on one row because that is "
         "how this sheet already carried the identical FY2020-FY2015 vs FY2023-FY2021 break.\n"
         "  WHY THIS WAS MISSED BEFORE, recorded so the pattern is recognised rather than repeated: the note "
         "previously asserted the figure was 'Not found anywhere in the Annual Report's own pages'. The FY2024 "
         "and FY2025 filings are wholly scanned, so every text search over them returned nothing — an "
         "instrument's reach reported as a fact about the bank (km1/map.md rules 15 and 40). The sheet's own "
         "FY2020-FY2015 block, sourced from Annual Report KPI tables, contradicted the claim the whole time.\n"
         "PRIOR TEXT, RETAINED: not found in the Annual Report's own pages (Strategic Report or Notes) for "
         "FY2023-FY2021 — for those years the Annual Report "
         "defers all liquidity Pillar 3 detail to the standalone Pillar 3 Disclosures documents. Those documents "
         "were located (via Wayback Machine, after itau.co.uk/itaubba.co.uk/live itau.com.br all proved "
         "unreachable) for FY2023/FY2022/FY2021, each disclosing LCR as a 12-month trailing average. "
         "FY2024/FY2025 remain blank — no Pillar 3 Disclosures document for either year was found this session. "
         "HD-052 (2026-09-05): FY2020-FY2015 were found directly in each year's own Annual Report Key Performance "
         "Indicators table (a point-in-time figure, not the trailing average the Pillar 3 documents disclose for "
         "FY2021-2023 — a genuine presentation difference between the two source types, not a data error). "
         "FY2014 is genuinely blank — no LCR appears anywhere in the 2014 Annual Report, consistent with the "
         "CRD IV LCR phase-in only beginning in 2015 (confirmed against this project's own finding for other "
         "banks, e.g. Bank of Ireland UK).",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {"FY2025": "168%", "FY2024": "155%", "FY2023": "161%", "FY2022": "150%"})],
    pillar3_disclosure_sources(),
    note="FY2025 AND FY2024 RECOVERED 2026-09-18 (GA-018), FROM THE ANNUAL REPORT — REVERSING THIS SHEET'S OWN "
         "PRIOR CLAIM THAT THE ANNUAL REPORT DOES NOT DISCLOSE THIS METRIC. Each year from its OWN edition "
         "(Companies House filing copies, image-only, OCR'd before reading):\n"
         "  FY2025: 168% — 2025 Annual Report, Risk Management / liquidity risk, printed folio 28, stated in the "
         "Bank's own words: 'showing a NSFR of 168% as of 31 December 2025 (31.12.24: 155%)'.\n"
         "  FY2024: 155% — 2024 Annual Report, Risk Management / liquidity risk, printed folio 28 (the page's own "
         "footer reads 'Strategic Report 28'): 'showing a NSFR of 155% as of 31 December 2024 (31.12.23: 166%)'. "
         "INDEPENDENTLY CORROBORATED by the FY2025 edition quoting 155% as its 31.12.24 comparative.\n"
         "  BASIS BREAK, NOT RECONCILED: FY2025 and FY2024 are POINT-IN-TIME year-end ratios as printed in the "
         "Annual Report; FY2023 and FY2022 are TRAILING FOUR-QUARTER AVERAGES from the Pillar 3 documents, per "
         "those documents' own footnotes. Note the consequence — the FY2024 report's own 31.12.23 comparative is "
         "166%, against the 161% this sheet carries for FY2023 from the Pillar 3 document. THOSE TWO FIGURES ARE "
         "NOT IN CONFLICT AND NEITHER IS WRONG: one is a year-end point and the other a four-quarter average of "
         "the same year. Each is reproduced from its own source and they are deliberately NOT merged; FY2023 "
         "keeps the Pillar 3 figure because that is its own edition's own-year disclosure.\n"
         "PRIOR TEXT, RETAINED AND NOW LIMITED TO FY2023/FY2022: same availability constraint as the LCR sheet — "
         "deferred by the Annual Report to the standalone Pillar "
         "3 Disclosures documents, located via Wayback Machine for FY2023/FY2022 (trailing four-quarter average). "
         "FY2021 is blank because NSFR was not yet subject to the PRA's reporting requirement (effective 1 "
         "January 2022, per both the FY2022 and FY2023 documents' own notes) — no NSFR % appears in the FY2021 "
         "document. FY2024/FY2025 remain blank — no Pillar 3 Disclosures document for either year was found this "
         "session. HD-052 (2026-09-05): FY2014-FY2020 also remain blank for the same reason — NSFR was not yet a "
         "PRA reporting requirement, and no NSFR % appears in any of those years' own Annual Reports (searched "
         "in full this session).",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS if y != "FY2013"})],
    p3_sources(21, "2025", AR25_URL),
    note="No MREL ratio or resolution-strategy discussion was found in the Annual Report's own pages; deferred to "
         "the unreachable standalone Pillar 3 report, same as LCR/NSFR. FY2013 is left blank (not \"Not publicly "
         "disclosed\") per HD-072 (2026-09-06) - Pillar 3 is out of scope for that ticket's FY2013 extension, so "
         "this sheet's dict is intentionally not extended to FY2013, same as every other Pillar 3 sheet.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total Assets", {"FY2025": 7896227, "FY2024": 8937146, "FY2023": 8085575, "FY2022": 6981727, "FY2021": 5963514, "FY2020": 5931078, "FY2019": 6177219, "FY2018": 6859779, "FY2017": 5953347, "FY2016": 5043006, "FY2015": 5868598, "FY2014": 5177420}),
        ("Loans and advances to customers", {"FY2025": 4044575, "FY2024": 4104314, "FY2023": 3868767, "FY2022": 3604470, "FY2021": 3221895, "FY2020": 3181399, "FY2019": 3864886, "FY2018": 3779281, "FY2017": 3056151, "FY2016": 2782210, "FY2015": 3179457, "FY2014": 2855295}),
        ("Customer accounts", {"FY2025": 1740013, "FY2024": 2745061, "FY2023": 1709639, "FY2022": 1914084, "FY2021": 1751887, "FY2020": 1242218, "FY2019": 1304375, "FY2018": 1194983, "FY2017": 752508, "FY2016": 453090, "FY2015": 176000, "FY2014": 204392}),
        ("Total Equity", {"FY2025": 2154474, "FY2024": 2062914, "FY2023": 1963716, "FY2022": 1398537, "FY2021": 1329874, "FY2020": 1303897, "FY2019": 1298794, "FY2018": 1229438, "FY2017": 1122851, "FY2016": 1046209, "FY2015": 1023741, "FY2014": 1009878}),
    ],
    balance_sheet_unit="USD'000",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 157908, "FY2024": 163719, "FY2023": 121674, "FY2022": 117795, "FY2021": 70777, "FY2020": 64169, "FY2019": 123216, "FY2018": 164994, "FY2017": 124426, "FY2016": 77382, "FY2015": 78147, "FY2014": 80769}),
        ("Total operating expenses", {"FY2025": -37805, "FY2024": -32222, "FY2023": -31480, "FY2022": -33106, "FY2021": -33053, "FY2020": -35789, "FY2019": -50247, "FY2018": -48562, "FY2017": -44874, "FY2016": -44836, "FY2015": -54145, "FY2014": -66634}),
        ("Profit for the year", {"FY2025": 90082, "FY2024": 98827, "FY2023": 62794, "FY2022": 72745, "FY2021": 43010, "FY2020": 4758, "FY2019": 59336, "FY2018": 105541, "FY2017": 76963, "FY2016": 25279, "FY2015": 16660, "FY2014": -6235}),
    ],
    income_statement_unit="USD'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 2062914, "FY2024": 1963716, "FY2023": 1398537, "FY2022": 1329874, "FY2021": 1303897, "FY2020": 1298794, "FY2019": 1229438, "FY2018": 1122851, "FY2017": 1046209, "FY2016": 1023741, "FY2015": 1009878, "FY2014": 1012621}),
        ("Total comprehensive income for the year", {"FY2025": 91560, "FY2024": 99198, "FY2023": 65179, "FY2022": 68663, "FY2021": 43063, "FY2020": 5103, "FY2019": 62264, "FY2018": 106491, "FY2017": 76642, "FY2016": 22468, "FY2015": 13863, "FY2014": -2743}),
        ("Other equity movements, net", {"FY2025": 0, "FY2024": 0, "FY2023": 500000, "FY2022": 0, "FY2021": -17086, "FY2020": 0, "FY2019": 7092, "FY2018": 96, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
        ("Closing equity", {"FY2025": 2154474, "FY2024": 2062914, "FY2023": 1963716, "FY2022": 1398537, "FY2021": 1329874, "FY2020": 1303897, "FY2019": 1298794, "FY2018": 1229438, "FY2017": 1122851, "FY2016": 1046209, "FY2015": 1023741, "FY2014": 1009878}),
    ],
    equity_changes_unit="USD'000",
    cash_flow_totals=[
        ("Net cash flow from operating activities", {"FY2025": -823201, "FY2024": 202045, "FY2023": 896845, "FY2022": 977211, "FY2021": 183186, "FY2020": 185310, "FY2019": -265920, "FY2018": 161184, "FY2017": 109779, "FY2016": -20832, "FY2015": -69031, "FY2014": 154213}),
        ("Net cash flow from investing activities", {"FY2025": 89783, "FY2024": 150189, "FY2023": -918582, "FY2022": -1169363, "FY2021": -40817, "FY2020": -51831, "FY2019": -2032, "FY2018": 62821, "FY2017": 49617, "FY2016": -28814, "FY2015": -1307, "FY2014": -66637}),
        ("Net cash flow from financing activities", {"FY2025": -862, "FY2024": -838, "FY2023": 501619, "FY2022": -926, "FY2021": 948, "FY2020": -2238, "FY2019": 9582, "FY2018": 0, "FY2017": -30128, "FY2016": 57, "FY2015": 16, "FY2014": -221}),
        ("Cash and cash equivalents at end of year", {"FY2025": 460587, "FY2024": 1149307, "FY2023": 797911, "FY2022": 318029, "FY2021": 511107, "FY2020": 367790, "FY2019": 236549, "FY2018": 270914, "FY2017": 141646, "FY2016": 141646, "FY2015": 134322, "FY2014": 205351}),
    ],
    cash_flow_unit="USD'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "29.0%", "FY2024": "23.9%", "FY2023": "27.0%", "FY2022": "19.6%", "FY2021": "22.6%", "FY2020": "23.9%", "FY2019": "19.9%", "FY2018": "19.2%", "FY2017": "19.4%", "FY2016": "18.0%", "FY2015": "17.9%", "FY2014": "17.8%"}),
        ("Total Capital Ratio", {"FY2025": "29.0%", "FY2024": "23.9%", "FY2023": "27.1%", "FY2022": "19.6%", "FY2021": "22.6%", "FY2020": "23.9%", "FY2019": "19.9%", "FY2018": "19.2%", "FY2017": "19.5%", "FY2016": "18.2%", "FY2015": "18.1%", "FY2014": "18.1%"}),
        ("Leverage Ratio", {"FY2025": "19.1%", "FY2024": "16.4%", "FY2023": "16.7%", "FY2022": "11.9%", "FY2021": "14.6%", "FY2020": "14.4%", "FY2019": "13.5%", "FY2018": "11.9%", "FY2017": "12.4%", "FY2016": "11.3%", "FY2015": "10.3%", "FY2014": "10.5%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Cash flow figures are Bank/solo basis; capital ratios are "
         "Group/consolidated basis (the only basis the Annual Report discloses for capital). Tier 1 Ratio, LCR and "
         "NSFR are omitted from this chart — each is only available for a subset of years. UPDATED 2026-09-18 "
         "(GA-018): the subset is no longer the one this note used to state. The LCR now runs FY2025-FY2015 and "
         "the NSFR FY2025-FY2024 plus FY2023-FY2022, because each year's own Annual Report was found to disclose "
         "both ratios after all; but the two metrics still cross a basis break mid-series (Annual Report "
         "point-in-time vs Pillar 3 trailing average — see those sheets' notes), which is now the reason they "
         "stay off a single trend chart. Tier 1 Ratio remains FY2025-FY2021 only, "
         "via the standalone Pillar 3 Disclosures documents, not the full 5-year "
         "span this chart otherwise shows; see each metric's own sheet for the figures and detail.",
)

bw.save("/Users/armaan/code/katalysis/banks/ITAU BBA INTERNATIONAL FINANCIALS.xlsx")
