import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}
PREV_YEAR = {"FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024",
             "FY2020": "FY2019"}

# ---------------------------------------------------------------
# FX conversion (GIB UK reports in USD; converting to £ per this project's
# established FX methodology - same public Bank of England GBP/USD spot/
# average rates already used for Zenith Bank UK / Union Bank of India UK /
# Credit Suisse International, reused here rather than re-derived).
# ---------------------------------------------------------------
FX_SPOT = {
    "FY2019": 1.3210,  # 31 Dec 2019 - only used for FY2020's opening cash balance
    "FY2020": 1.3661,  # 31 Dec 2020
    "FY2021": 1.3521,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
    "FY2025": 1.3448,  # 31 Dec 2025
}
FX_AVG = {
    "FY2020": 1.2825,
    "FY2021": 1.3752,
    "FY2022": 1.2362,
    "FY2023": 1.2439,
    "FY2024": 1.2782,
    "FY2025": 1.3193,
}


# UNIT CONTRACT (fixed 2026-09-16, research/RESUME_fx_scale_sweep.md).
# EVERY source dict in this script holds US$'000 - that is the unit GIB UK's
# Annual Reports and Pillar 3 disclosures print. The three helpers below divide
# by the FX rate AND by 1000, so their OUTPUT IS £ MILLIONS, not £'000. Every
# sheet was previously labelled "£'000", which understated the Bank by 1000x to
# any reader and to scripts/insights/ (extract_metrics.py parses the unit label
# and in040/in041/build_deliverable.py scale by it, so GIB UK was entering every
# cross-bank absolute comparison as an £11.6m bank rather than an £11.6bn one).
# The FIGURES were right; the LABELS were wrong, so the labels were corrected to
# "£m" - matching Goldman Sachs International Bank, Credit Suisse International
# and SMBC, the three converted workbooks of comparable size. No figure changed.
# If you ever want true £'000 output here, drop the "/ 1000" AND relabel - do
# not do one without the other.


def flow(usd):
    """Flow (cash flow statement line item) figures: US$'000 in, £m out, at that year's average rate."""
    return {y: round(v / FX_AVG[y] / 1000, 1) for y, v in usd.items() if y in FX_AVG}


def stock(usd):
    """Point-in-time (balance/capital) figures: US$'000 in, £m out, at that year's period-end spot rate."""
    return {y: round(v / FX_SPOT[y] / 1000, 1) for y, v in usd.items() if y in FX_SPOT}


def opening_cash(usd):
    """Opening cash balance, US$'000 in, £m out - uses the PRIOR year's period-end spot rate (it's
    the same balance as that prior year's closing figure, so must convert identically)."""
    return {y: round(v / FX_SPOT[PREV_YEAR[y]] / 1000, 1) for y, v in usd.items() if PREV_YEAR.get(y) in FX_SPOT}


# ---------------------------------------------------------------
# Source documents
# ---------------------------------------------------------------
CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/01223938/filing-history"
AR2024_URL = f"{CH_BASE}/MzQ2MTE4ODYxN2FkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = f"{CH_BASE}/MzQxNzM5ODc0MWFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = f"{CH_BASE}/MzM3NTI0MDA2MmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = f"{CH_BASE}/MzM1NTYyODEwMGFkaXF6a2N4/document?format=pdf&download=0"
# HD-062 (2026-09-06) FY2020 extension: "Full accounts made up to 31 December
# 2020", filed 10 Sep 2021, re-verified directly against Companies House's own
# filing-history page 2 for this company (the FY2021 filing above only goes
# back to page 1) rather than assumed from the ticket's nominal floor.
AR2020_URL = f"{CH_BASE}/MzMxMzAyNDY0OGFkaXF6a2N4/document?format=pdf&download=0"

P3_2024_URL = "https://gib-am.files.svdcdn.com/production/documents/2024-GIBUK-Pillar-3-disclosures-Board-approved.pdf"
P3_2023_URL = "https://gib-am.files.svdcdn.com/production/documents/Fund-sustainability-related-documents/2023-GIBUK-Pillar-3-disclosures.pdf"
P3_2022_URL = "https://web.archive.org/web/20240223164517id_/https://gibam.com/assets/2022-GIBUK-Pillar-3-disclosures_VF.pdf"
# Note: the 20230927145657 snapshot originally cited here is truncated by the
# Wayback Machine's own crawler at 1,048,576 bytes (confirmed: it fails to
# open as a valid PDF at all) - the 20240223164517 snapshot above is a full,
# valid capture of the same document and was used for this workbook's RWA
# Breakdown sheet.
# FY2020 and FY2021 Pillar 3 editions: each survives as exactly ONE Wayback
# capture, and both captures are truncated at exactly 1,048,576 bytes. The
# truncation destroys the PDF cross-reference table only; the page objects are
# intact and both documents are fully recoverable. The complete account -
# the recovery recipe, what was verified, and the entity-basis trap - is in
# P3_CAPTURE_NOTE below, which is written onto every Pillar 3 metric sheet.
#
# Both are cited in the `id_` playback form: that is the form the recovery
# recipe uses and the form actually downloaded and read. This REVERSES the
# earlier "do not convert these two to id_" decision recorded in
# research/RESUME_linkrot_2b.md, which rested on the belief that the files were
# dead and that id_ would only make a damaged file look authoritative. They are
# not dead; id_ returns the raw archived bytes with no playback wrapper, which
# is exactly what the Ghostscript rebuild needs.
P3_2021_URL = "https://web.archive.org/web/20230329132856id_/https://gibam.com/assets/2021-GIBUK-Pillar-3_Final.pdf"
P3_2020_URL = "https://web.archive.org/web/20220518000354id_/https://gibam.com/assets/2020-GIBUK-Pillar-3_Final.pdf"

# FY2025 ANNUAL REPORT - FOUND 2026-09-18 (GA-006). It is NOT a Companies House
# filing: it is published on GIB AM's own document library, under a filename that
# names no entity and no "GIB UK". See FY2025_FIND_NOTE below for why that matters.
AR2025_URL = "https://gib-am.files.svdcdn.com/production/documents/Annual-and-Financial-Report-2025.pdf"
ENTITY_NOTE = (
    "ENTITY NOTE: Gulf International Bank (UK) Limited (\"GIB UK\", FRN 124772, company 01223938) is a wholly "
    "owned subsidiary of Gulf International Bank B.S.C. (Bahrain, sovereign-backed by several Gulf Cooperation "
    "Council states), trading as \"GIB Asset Management\" (GIB AM) for its investment-management business, with a "
    "branch in New York. It prepares standalone (non-consolidated) financial statements under UK-adopted "
    "international accounting standards, exempt from producing group accounts under Companies Act 2006 s.401 and "
    "IFRS 10 (its parent's consolidated accounts are filed in Bahrain). No cash-flow exemption applies - a full "
    "Statement of Cash Flow is presented every year.\n\n"
    "*** FY2025 STATUS - SUPERSEDED 2026-09-18. THE FY2025 ANNUAL REPORT EXISTS, WAS FOUND, AND IS NOW THE "
    "SOURCE FOR THE FY2025 COLUMN THROUGHOUT THIS WORKBOOK. The block immediately below is the 2026-09-15 "
    "reasoning, kept because it is accurate about Companies House and about Pillar 3 - both still hold - and "
    "because its ONE wrong sentence is worth preserving as a worked example. See FY2025 FIND NOTE after it. ***\n"
    "[SUPERSEDED] FY2025 STATUS (re-verified directly 2026-09-15 - FY2025 is blank throughout this workbook, on "
    "every sheet including all 11 Pillar 3 metric sheets, and this is a genuine not-yet-published, not a "
    "sourcing gap):\n"
    "(a) Statutory accounts. Companies House's filing history for company 01223938 shows the most recent accounts "
    "filing is 'Full accounts made up to 31 December 2024', filed 3 April 2025; there is no 2026 accounts filing "
    "of any kind. Companies House records the FY2025 accounts as next due 30 September 2026, so they are not yet "
    "overdue. The company is demonstrably still filing (confirmation statement 15 July 2026, TM01 31 July 2026), "
    "so this is a filing that has not happened yet rather than a dormant or struck-off entity. Note that FY2024's "
    "accounts were filed about 3 months after year-end, so FY2025 is running materially later than this entity's "
    "own recent habit; an auditor's resignation was also filed on 23 June 2025 (form AUD). No causal link between "
    "those two facts is asserted here - both are simply recorded as filed facts.\n"
    "(b) Pillar 3. GIB AM's own live document library (https://gibam.com/document-library, the page the Bank "
    "itself publishes these under) was fetched and every PDF link on it enumerated: the only Pillar 3 document "
    "listed is '2024-GIBUK-Pillar-3-disclosures-Board-approved.pdf'. A Wayback CDX domain scan of both "
    "gib-am.files.svdcdn.com and gibam.com filtered to Pillar-3 URLs returns captures for FY2020, FY2021, FY2022, "
    "FY2023 and FY2024 only - nothing for FY2025. Direct URL guesses following this entity's own established "
    "naming convention (2025-GIBUK-Pillar-3-disclosures-Board-approved.pdf and "
    "2025-GIBUK-Pillar-3-disclosures.pdf, both under the /production/documents/ path the FY2024 and FY2023 "
    "documents live at) both return a hard HTTP 404 with an XML error body, not a soft-404 HTML page. Note the "
    "Annual-and-Financial-Report-2025.pdf that does appear in that library is the Gulf International Bank B.S.C. "
    "(Bahrain) GROUP report, a different reporting entity - per this project's entity-scope rule no group figure "
    "is substituted into this entity-level workbook. [THIS LAST SENTENCE IS FALSE - see the FIND NOTE below.]\n\n"
    "FY2025 FIND NOTE (2026-09-18, GA-006) - THE FY2025 ANNUAL REPORT WAS ON THE BANK'S OWN DOCUMENT LIBRARY "
    "THE WHOLE TIME, AND THE ONLY THING HIDING IT WAS ITS FILENAME.\n"
    f"{AR2025_URL} is 'Gulf International Bank (UK) Limited - Annual Report and Financial Statements - 31 "
    "December 2025'. Its cover page, every page footer and its audit report all name GIB UK, FRN 124772, "
    "Registered No. 01223938 - this entity, not the Bahrain parent. It is a Docusign-signed, text-native PDF "
    "(%PDF-, application/pdf, 1,765,255 bytes), signed by Ralph Campbell, Director and Chief Financial Officer, "
    "and its Statement of Financial Position ties (assets 20,831,230 = liabilities 20,359,732 + equity 471,498, "
    "US$'000). Every FY2025 figure in this workbook comes from it.\n"
    "HOW IT WAS MISSED, because the failure mode generalises: the file is called "
    "'Annual-and-Financial-Report-2025.pdf'. It carries no 'GIBUK', no 'GIB-UK', no company number and no entity "
    "name at all - unlike every other document this entity publishes ('2024-GIBUK-Pillar-3-disclosures-"
    "Board-approved.pdf', '2025.12.31-Gulf-International-Bank-UK-Limited-Pension-Scheme-Implementation-"
    "Statement-Final...'). The 2026-09-15 pass enumerated this exact file on this exact page, and assigned it to "
    "the Bahrain group on the strength of the filename alone, then wrote that assignment down as a fact. IT WAS "
    "NEVER OPENED. An entity attribution is a property of the document's cover page, never of its URL; the file "
    "was one fetch away throughout. Nothing else in the 2026-09-15 block is wrong - Companies House really did "
    "hold no FY2025 accounts on that date, and there really is no FY2025 Pillar 3.\n"
    "COMPANIES HOUSE, re-read live 2026-09-18: the FY2025 accounts have since been filed - '16 Sep 2026, AA, "
    "Full accounts made up to 31 December 2025' - but the filing-history row carries NO document link and reads "
    "'This document is being processed and will be available in 10 days', i.e. from about 26 September 2026. "
    "That is a dated reach limit on the Companies House copy only; it has no bearing on the figures here, which "
    "come from the Bank's own published edition. When the CH image becomes available it is worth a cross-read "
    "against this workbook's FY2025 column, but nothing here depends on it.\n"
    "PILLAR 3 FOR FY2025: STILL NOT PUBLISHED, re-confirmed live 2026-09-18 and NOT carried over from the "
    "2026-09-15 pass, since that pass's other conclusion turned out to be wrong. The document library now lists "
    "25 PDFs and exactly one is a Pillar 3 - the FY2024 edition. The probe was verified before it was trusted: "
    "the known-good FY2024 URL returns HTTP 200 application/pdf from the same CDN in the same run, while "
    "2025-GIBUK-Pillar-3-disclosures-Board-approved.pdf, 2025-GIBUK-Pillar-3-disclosures.pdf, "
    "2025-GIBUK-Pillar-3_Final.pdf and GIBUK-Pillar-3-disclosures-2025.pdf all return a hard HTTP 404 with an "
    "application/xml error body. A Wayback CDX sweep of gib-am.files.svdcdn.com filtered to PDFs returns two "
    "Pillar 3 captures (FY2024, FY2023) and a sweep of gibam.com returns three (FY2022, FY2021, FY2020) - five "
    "editions, none later than FY2024. NOTE THE LIMIT OF THIS CONTROL, given what the filename trap above cost: "
    "these probes test a NAMING CONVENTION, and a convention can change. What actually carries the finding is "
    "the enumeration of the Bank's own library - and that library is the same page that was serving the FY2025 "
    "Annual Report under an unexpected name, so the FY2025 Pillar 3, if it is ever published, may well arrive "
    "under a name none of these probes would catch. Re-enumerate the page; do not re-run the probes.\n\n"
    "HD-062 (2026-09-06) FY2020 EXTENSION: FY2020 accounts and Pillar 3 disclosure both genuinely exist and were "
    "obtained and read in full (re-verified directly against Companies House and a Wayback CDX domain scan of "
    "gibam.com rather than assumed from the ticket's nominal 'confirmed floor FY2020' signal) - no self-skip was "
    "needed for this bank. FY2020's Pillar 3 Disclosures document (a Basel II-era 38-page document, titled "
    "'Basel II Pillar 3 Disclosures', predating the UK KM1/OV1 template rollout later years use) DOES disclose an "
    "LCR (section 5.3 'Liquidity and Funding Risk', reported as 'Liquidity Coverage ratio' with a 'Liquidity "
    "Buffer' and 'Total Net cash outflows' - functionally equivalent to later years' HQLA/net-cash-outflow KM1 "
    "fields, see the LCR sheet's own basis note for the two ratio variants disclosed). It genuinely has NO NSFR "
    "or MREL section anywhere in its own table of contents or body text (only a passing mention of the upcoming "
    "regulatory 'binding NSFR measure of 100%' requirement, not GIB UK's own NSFR ratio) - confirmed by reading "
    "the full document, not assumed from a missing keyword. It also predates the "
    "UK OV1 RWA-breakdown template used from FY2021 onward: no separate counterparty-credit-risk (CCR) or CVA "
    "line is disclosed for FY2020 in that document.\n"
    "UPDATED 2026-09-16 - THE ABOVE DESCRIBES THE FY2020 DOCUMENT ONLY, AND IS NO LONGER THE WHOLE STORY FOR THE "
    "FY2020 COLUMN. The FY2021 Pillar 3 edition was recovered on this date (see the CAPTURE NOTE on any Pillar 3 "
    "metric sheet) and carries a full prior-year 2020 comparative column on the CRR/CRD V basis. That column "
    "supplies, for FY2020, an NSFR (and its available/required stable funding components) and a CVA risk RWA - "
    "neither of which the FY2020 document itself discloses - so the NSFR sheet's FY2020 cells are NO LONGER blank "
    "and the RWA Breakdown sheet now carries a labelled FY2020 block on that restated basis. It also disagrees "
    "with the FY2020 document on capital, capital ratio and leverage; every such disagreement is recorded on its "
    "own separate labelled row rather than being reconciled or overwritten. MREL remains genuinely absent for "
    "FY2020 on both documents' evidence."
)

FX_NOTE = (
    "FX CONVERSION NOTE: GIB UK reports in US Dollars (its functional and presentation currency per its own "
    "accounting policy note). This workbook converts every $ amount to £ for consistency with the rest of this "
    "series, following the same methodology established for Zenith Bank UK/Union Bank of India UK/Credit Suisse "
    "International: point-in-time/balance figures (capital, RWA, leverage exposure, HQLA/stable-funding amounts, "
    "cash balances) use the Bank of England GBP/USD SPOT rate as at that fiscal year-end; flow figures (every "
    "cash flow statement line item) use the AVERAGE of Bank of England rates over that calendar year. Rates used "
    "(£1 = $X, reused from this project's existing FX rate table): 31 Dec 2019 spot 1.3210 (FY2020 opening cash "
    "only); FY2020 spot 1.3661 / average 1.2825; FY2021 spot 1.3521 / average 1.3752; FY2022 spot 1.2097 / "
    "average 1.2362; FY2023 spot 1.2732 / average 1.2439; FY2024 spot 1.2515 / average 1.2782; FY2025 spot "
    "1.3448 / average 1.3193 (added 2026-09-18 from the same project FX table already used by Goldman Sachs "
    "International Bank; cross-checked the same day against the Bank of England's own XUDLUSS daily series, "
    "which gives 31 Dec 2025 = 1.3451 and a 2025 mean of 1.3186 over 253 observations - agreeing to the third "
    "decimal. The project table was kept rather than the fresh BoE figures so that GIB UK converts on exactly "
    "the same basis as every other converted workbook in this series). All % ratios are "
    "shown exactly as reported in USD and "
    "were NOT converted - a ratio is dimensionless and currency-invariant. Because stocks and flows are converted "
    "at different rates, the cash flow statement includes an explicit 'Effect of GBP/USD translation' reconciling "
    "line, computed programmatically so it can never drift out of sync with the rates above, so that opening + "
    "all flows + this line = closing exactly in £ terms - this line is purely an artefact of £ translation and "
    "has no bearing on the Bank's underlying USD results. This conversion was not explicitly requested for this "
    "bank - applied for consistency with the rest of the series; flag if £m rather than the Bank's native "
    "US$'000 presentation is not what's wanted here. UNIT: every monetary figure in this workbook is in £ "
    "MILLIONS (£m). The Bank's own sources print US$'000, and the conversion divides by the FX rate and then "
    "by 1,000. Until 2026-09-16 these sheets were mislabelled \"£'000\" while carrying £m values - a 1000x "
    "labelling error that made an £11.6bn bank read as an £11.6m one. The labels were corrected; NO FIGURE WAS "
    "CHANGED, and every disclosed ratio is unaffected because a ratio is scale-invariant."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Gulf International Bank (UK) Limited's own Statement of Cash Flow (converted from "
    "USD to £, see FX conversion note below), transcribed from scanned/image-only Companies House filings (no "
    "text layer in any of the 5 filings):\n"
    f"FY2024: Annual Report and Financial Statements 2024, p.109 (Statement of Cash Flow) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.71 (Statement of Cash Flow, incl. FY2022 comparative) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.52 (Statement of Cash Flow) - {AR2021_URL}\n"
    f"FY2020: Annual Report and Financial Statements 2020, p.29 (Statement of Cash Flow) - {AR2020_URL}\n"
    "FY2022's own column is sourced from the FY2023 Annual Report's comparative column (p.71 above) rather than "
    "the FY2022 Annual Report directly - both would show the same figures for FY2022 (a bank's own prior-year "
    "comparative is not normally restated absent a disclosed reason, and none is disclosed here); the FY2022 "
    "filing itself is also fully scanned - see AR2022_URL for reference: " + AR2022_URL + ".\n"
    "FY2025 is blank: no FY2025 Annual Report has been filed with Companies House yet.\n"
    "All 5 years' opening-to-closing cash bridges reconcile exactly in USD as originally reported; the £ "
    "conversion is exact by construction (translation-effect line computed programmatically, see FX note). "
    "FY2020/FY2021/FY2023/FY2024's operating-activities line items also sum exactly (in USD) to each year's own "
    "printed subtotal (FY2020: independently re-summed to -$1,602,673k, exactly matching the source's own "
    "printed 'Net cash (used)/from operating activities' subtotal). FY2022's do not: summing FY2022's own line "
    "items above gives $285,026k vs the source's own printed $287,025k subtotal - a $1,999k (~0.7%) gap within "
    "the source document's own comparative column, not traceable to a specific mis-cast line (each line was "
    "independently re-checked against the source image). Flagged rather than forced to reconcile, per this "
    "project's convention for unexplained source-side gaps. FY2020 has no reported 'Net foreign exchange "
    "difference' line at all (unlike FY2022-FY2024) - its own opening-to-closing USD bridge already ties exactly "
    "without one ($6,861,304k - $1,604,216k = $5,257,088k), so that cell is genuinely blank for FY2020 rather "
    "than estimated; the programmatic £ translation-effect line still applies since GBP conversion at differing "
    "spot/average rates still requires a plug even when the USD bridge itself needs none.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)


# ---------------------------------------------------------------
# ONE reconciled account of the FY2020/FY2021 capture problem, replacing two
# earlier notes that contradicted each other on the single most important word.
# One (P3_COMPARATIVE_NOTE) called the two editions "unretrievable" and
# concluded FY2020 was permanently unsourceable; the other
# (P3_CAPTURE_INTEGRITY_NOTE) said truncated-but-recoverable and gave a working
# recipe. The second is correct; the first is withdrawn. Verified independently
# a third time on 2026-09-16 - both documents were recovered, and the FY2021
# edition turned out to carry a full prior-year 2020 comparative column, which
# is what makes FY2020 sourceable at all.
#
# Written onto every Pillar 3 metric sheet so the basis is visible on the sheet
# rather than buried in this file.
# ---------------------------------------------------------------
P3_CAPTURE_NOTE = (
    "CAPTURE NOTE, FY2020 AND FY2021 - TRUNCATED AS SERVED, BUT RECOVERABLE. READ THIS BEFORE CONCLUDING "
    "ANYTHING FROM A FAILED DOWNLOAD (settled 2026-09-16; supersedes and withdraws two earlier notes on these "
    "sheets, one of which described these editions as 'unretrievable' and FY2020 as permanently unsourceable - "
    "that conclusion was wrong).\n"
    "THE DAMAGE. Each year's Pillar 3 edition survives as exactly ONE Wayback capture "
    f"(FY2020: {P3_2020_URL}; FY2021: {P3_2021_URL}), and both are truncated by the Wayback Machine's own 1 MiB "
    "per-capture limit at exactly 1,048,576 bytes (md5 edfe2438dbff06fdc617e6a38efb6059 for FY2020, "
    "32d6206989581714144f61ffc6982ab5 for FY2021 - identical across the bare, if_ and id_ playback forms, so the "
    "truncation is in the capture itself, not in playback). What the cut removes is the PDF CROSS-REFERENCE "
    "TABLE, which sits at the END of the file. That breaks every tool that trusts the index - pdfinfo reports "
    "'Invalid XRef entry 0' and 'Couldn't find trailer dictionary', qpdf reports 'can't find startxref' - so the "
    "files look dead. They are not. The page objects themselves are intact.\n"
    "THE RECOVERY RECIPE (recorded here so nobody has to rediscover it). Ghostscript rebuilds by scanning objects "
    "rather than reading the index:\n"
    "    curl -sSL -A \"<browser user-agent>\" -o raw.pdf \"<the id_ URL above>\"\n"
    "    gs -o fixed.pdf -sDEVICE=pdfwrite raw.pdf\n"
    "FY2020: 1,048,576 B -> 795,035 B, 38 pages. FY2021: 1,048,576 B -> 697,523 B, 30 pages. Ghostscript prints "
    "'no startxref token found' and 'xref table was repaired' and completes; those warnings are expected. qpdf is "
    "the less reliable route - it reconstructs but does not reproduce the full page count. Reproduced "
    "independently by three separate passes, byte-for-byte identical each time.\n"
    "NOTHING WAS LOST IN THE REBUILD - checked against each document's own table of contents and page numbering, "
    "not assumed. FY2020: roman front matter i/ii/iii on PDF pages 1-3, then printed page N = PDF page N through "
    "38; the TOC's last entry is '10.6 Material Risk Takers ... 38' and PDF page 38 is printed page 38, carrying "
    "section 10.5's remuneration table and 10.6 in full and ending on the document's own closing paragraph. "
    "FY2021: printed page N = PDF page N+1; the TOC's last entry is '6.6 Material Risk Takers ... 28' = PDF page "
    "29, and PDF page 30 = printed page 29 completes section 6.6. Every page in both documents yields extractable "
    "text; there are no empty pages and no table straddles the damaged region, because the damaged region carries "
    "no content. Covers read 'GULF INTERNATIONAL BANK (UK) LTD / Basel II Pillar 3 Disclosures / 31 December "
    "2020' and 'GULF INTERNATIONAL BANK (UK) LTD / Pillar 3 disclosures / 31 December 2021'.\n"
    "ONE LEGIBILITY DEFECT, NOT CAUSED BY THE TRUNCATION: on FY2020 printed p.16 the caption under section 4.5 "
    "and the two buffer sub-headings in section 4.6 render as garbled non-Latin glyphs (a broken font cmap in the "
    "original document). The capital-adequacy table above that caption, and section 4.6's buffer figures, are in "
    "plain legible text. No figure in this workbook is taken from the garbled text.\n"
    "INDEPENDENT CORROBORATION THAT THE RECOVERY IS FAITHFUL, not a plausible reconstruction: the recovered "
    "FY2021 edition gives FY2021 CET1 of $371,866k, and the FY2022 edition's T-4 comparative column - an "
    "unrelated, fully intact document - gives exactly $371,866k. The recovered FY2021 edition also prints FY2021 "
    "leverage of 3.52% on a total exposure measure of $10,573,209k, confirming the as-reported rows on the "
    "Leverage Ratio sheet. Every FY2020 figure previously carried on these sheets (leverage 4.61%, Total Capital "
    "ratio 26.48%, Total RWAs $1,482m, capital base $393m, LCR 290%) was re-read from the recovered FY2020 "
    "edition and confirmed unchanged.\n"
    "WHY THIS STILL MATTERS FOR A READER: anyone who simply opens either URL in a browser or feeds it to a PDF "
    "tool will get a broken file. That is expected and is NOT evidence that these figures are unsourced. Do not "
    "blank a cell, do not mark a year unsourceable, and do not substitute another entity's document on the "
    "strength of a failed download - run the recipe above first.\n"
    "EXHAUSTED SEARCH FOR A CLEAN (UNTRUNCATED) COPY. The Wayback CDX index holds exactly ONE 200 capture per URL "
    "(the two above); every other capture of those paths is a 404. Live gibam.com 404s on the 2020, 2021 AND 2022 "
    "asset paths, /regulatory-information, /literature-library and /important-information all 404, and the site "
    "has no disclosures index page. GIB UK's documents moved to the CDN gib-am.files.svdcdn.com, which holds the "
    "2023 and 2024 editions ONLY - about ten filename permutations for 2020/2021/2022 all 404, and a Wayback "
    "sweep of the CDN host returns only those same two files. The Memento aggregator, Common Crawl (2023-50 "
    "index) and archive.today hold no capture of either URL. So the truncated captures are the only copies that "
    "exist, and the recipe above is the only way in.\n"
    "ENTITY-BASIS TRAP - READ BEFORE 'FIXING' THIS. gib.com is REACHABLE (it answers 200 to browser-shaped "
    "request headers; an earlier 403 came from a wrong path and is withdrawn - it is NOT a blocked host), and it "
    "hosts MANY Pillar 3 PDFs. Every one of them belongs to Gulf International Bank B.S.C. (the Bahrain parent), "
    "to the KSA entity under /ksa/, or to the Abu Dhabi branch. NONE is Gulf International Bank (UK) Limited's "
    "own disclosure. They were found, examined and REJECTED on entity basis: under this project's entity-scope "
    "rule no parent-, KSA- or branch-level figure may be substituted into this entity-level workbook. A search "
    "for 'Gulf International Bank Pillar 3' surfaces them immediately and they look superficially like the "
    "missing documents - they are not. Never substitute them.\n"
)

# ---------------------------------------------------------------
# What each surviving edition's prior-year comparative column supplies, and
# where those columns DISAGREE with the year's own edition. Every disagreement
# is recorded on its own labelled row on the relevant sheet; none is reconciled
# and none overwrites the other.
# ---------------------------------------------------------------
P3_COMPARATIVE_NOTE = (
    "COMPARATIVE-COLUMN BASIS (verified 2026-09-16). All four surviving editions were downloaded and read in "
    "full, and each was verified as the UK entity's own disclosure before any figure was read. The FY2022 edition "
    "is 1,137,898 bytes / 33 pages and the FY2023 edition 530,545 bytes / 33 pages (both intact as served); the "
    "FY2020 and FY2021 editions are the recovered 38-page and 30-page rebuilds described in the CAPTURE NOTE "
    "above. None is the Bahraini parent's, the KSA entity's or the Abu Dhabi branch's disclosure.\n"
    "Each edition reaches back exactly ONE year:\n"
    "  * FY2021 edition -> a full 2020 comparative column, on the CRR/CRD V basis. This is the column that makes "
    "FY2020 sourceable beyond its own Basel II-era edition, and it DISAGREES with that edition on capital, "
    "capital ratio and leverage while supplying two things the FY2020 edition does not disclose at all (an NSFR "
    "and a CVA risk RWA). Detail: printed p.6 'Key ratios', 2020 column - CET1 = Tier 1 = Total capital "
    "$378,549k, RWEA $1,482,468k, all three ratios 26.04%, leverage exposure $10,426,834k, leverage ratio 3.63%. "
    "Printed p.23, sections 4.1/4.2 own-funds reconciliation, 2020 column - Total equity $392,596k less pension "
    "asset net of deferred tax $13,932k less intangibles $0 less prudent valuation adjustment $115k = CET1 "
    "$378,549k (ties exactly, and the $392,596k ties to this workbook's own Balance Sheet Total equity for "
    "FY2020). Printed pp.24-25, section 5.2 Pillar 1 capital requirements, 2020 column - credit and counterparty "
    "risk RWA $1,206,179k, market risk $142,838k, operational risk $128,538k, CVA risk $4,913k, total "
    "$1,482,468k (the four components sum to the total EXACTLY). Printed p.7 quarterly liquidity table, 2020 row "
    "- Q4 2020 average LCR 291.28% on an average liquid assets buffer of $6,237,113k and average net flows of "
    "$2,141,287k (itself average outflows $3,085,596k less average inflows $944,309k, which ties exactly), and "
    "NSFR 103.23% on available stable funding $10,463,760k and required stable funding $10,136,594k (ties "
    "exactly).\n"
    "  * FY2022 edition, T-4 = 31-Dec-21. Its KM1 (p.6) independently confirms, figure-for-figure, the FY2021 "
    "CET1/Tier 1/Total capital ($371,866k), Total RWEA ($1,932,234k), all three capital ratios (19.22%), HQLA "
    "($6,737,809k) and LCR (480.13%); its OV1 (pp.26-27) likewise confirms all six FY2021 RWA-breakdown lines. It "
    "ALSO supplies one figure the FY2021 edition does not print in that form - FY2021 'Total net cash outflows "
    "(adjusted value)' of $1,403,343k (KM1 row 16) - and one figure on a DIFFERENT BASIS, the FY2021 leverage "
    "restatement recorded on the Leverage Ratio sheet. Its KM1 NSFR rows (18/19/20) are BLANK in the T-4 column, "
    "so the FY2021 NSFR figures rest on the FY2021 edition alone - now re-read and confirmed from the recovered "
    "copy.\n"
    "  * FY2023 edition, T-4 = 31-Dec-22. Its KM1 (p.6) and OV1 (pp.26-27) agree with every FY2022 figure already "
    "on these sheets - no restatement of any FY2022 figure between the two editions.\n"
    "NO FIGURE ANYWHERE ON THESE SHEETS IS BACK-SOLVED, DERIVED OR INFERRED. Every value is printed in a named "
    "document at a named page. Where two documents print different values for the same year, BOTH are carried on "
    "separate labelled rows and neither is reconciled away.\n"
    "ONE SOURCE-SIDE INCONSISTENCY, FLAGGED NOT FIXED: in the FY2021 edition's p.6 key-ratios table the printed "
    "2020 capital ratio of 26.04% does not reproduce from that same column's own capital and RWA figures "
    "($378,549k / $1,482,468k = 25.53%). The same table's 2021 column is very slightly off in the same direction "
    "($371,866k / $1,932,234k = 19.25% against a printed 19.22%, a figure the FY2022 edition independently "
    "reprints as 19.22%). Both ratios are recorded exactly as printed. The leverage ratios in that table DO tie "
    "exactly on both bases ($378,549k / $10,426,834k = 3.63%; $371,866k / $10,573,209k = 3.52%), as does the "
    "FY2020 edition's own 26.48% ($393m / $1,482m = 26.5%), so the discrepancy is confined to that one ratio "
    "block in that one document."
)


def p3_sources():
    return (
        "Sources - Gulf International Bank (UK) Limited Pillar 3 Disclosures (UK KM1 - Key Metrics table), "
        "converted from USD to £ where a $ amount (see FX conversion note on the Cash Flow Statement sheet; % "
        "ratios are unconverted):\n"
        f"FY2024: Pillar 3 Disclosures as at 31 December 2024 (Board-approved), p.6 (UK KM1) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures as at 31 December 2023, p.6 (UK KM1) - {P3_2023_URL}\n"
        f"FY2022: sourced from the FY2023 Pillar 3 Disclosures' own T-4/prior-year comparative column (p.6 above) - "
        f"{P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures as at 31 December 2021, printed p.6 (section 1.2 'Key ratios' - capital, "
        f"RWEA, capital ratios, leverage) and printed p.7 (section 1.2 quarterly liquidity table - LCR and NSFR "
        f"by quarter; FY2021 uses the Q4 column). Its 2020 comparative column is additionally the source for the "
        f"restated-basis FY2020 rows across these sheets - printed p.6 (key ratios), printed p.23 (sections "
        f"4.1/4.2 own funds), printed pp.24-25 (section 5.2 Pillar 1 capital requirements) and printed p.7 (2020 "
        f"quarterly liquidity block). Read from the recovered rebuild described in the CAPTURE NOTE below - "
        f"{P3_2021_URL}\n"
        f"FY2020: 'Basel II Pillar 3 Disclosures as at 31 December 2020', printed p.16 (the section 4.5 'Capital "
        f"adequacy' table - Total RWAs / Capital base / Tier 1 capital / Tier 1 ratio / Total Capital ratio; note "
        f"section 4.5's heading is on p.15 but the table itself is overleaf on p.16), printed p.13 (section 3.1 "
        f"'Capital base' - the $393m Tier 1 / nil Tier 2 table), printed p.35 (the section 7 'Leverage' "
        f"reconciliation table; section 7's heading is on p.34 and the table is overleaf on p.35) and printed "
        f"p.27 (section 5.3 'Liquidity and Funding Risk' - the LCR table). Read from the recovered rebuild "
        f"described in the CAPTURE NOTE below - {P3_2020_URL}\n"
        + P3_CAPTURE_NOTE
        + "*** FY2025, REWRITTEN 2026-09-18 (GA-006). THE PILLAR 3 HALF OF THE 2026-09-15 FINDING STILL STANDS; "
        "THE ANNUAL-REPORT HALF DID NOT. ***\n"
        "NO FY2025 PILLAR 3 EXISTS. Re-confirmed live on 2026-09-18 rather than carried forward: GIB AM's own "
        "document library now lists 25 PDFs and exactly one is a Pillar 3 - the FY2024 edition. The probe was "
        "verified before it was trusted (the known-good FY2024 URL returns HTTP 200 application/pdf from the same "
        "CDN in the same run) and four FY2025 name variants each return a hard HTTP 404 with an XML error body; a "
        "Wayback CDX sweep of both hosts returns five Pillar 3 captures, none later than FY2024. What carries this "
        "finding is the ENUMERATION of the Bank's own library, not the URL probes - see the FY2025 FIND NOTE in "
        "the ENTITY NOTE for why a naming-convention probe is the weaker instrument here.\n"
        "BUT THE FY2025 ANNUAL REPORT DOES EXIST, and it carries a full regulatory-capital disclosure, so these "
        "sheets are NO LONGER BLANK for FY2025. Source: Annual Report and Financial Statements 2025, capital "
        "management note, printed p.81 - the Bank's 'CET 1 capital position' table. It states directly, in "
        "US$'000 and for 2025 and 2024: CET1 capital 448,062 (2024: 435,464); Total Risk exposure amount "
        "1,988,661 (2024: 1,961,726) with its own four-way 'Of which' split (credit risk 1,752,265; market risk "
        "4,277; operational risk 214,785; credit valuation adjustment 17,334, summing to the total exactly); and, "
        "under 'Capital ratios and buffers', Common Equity Tier 1 22.53%, Tier 1 22.53% and Total capital 22.53% "
        f"(2024: 22.20% on all three) - {AR2025_URL}\n"
        "WHY ONE FIGURE FILLS THREE CAPITAL SHEETS AND ONE RATIO FILLS THREE RATIO SHEETS. It is the Bank's own "
        "structure, already documented on these sheets for every earlier year: GIB UK holds no AT1 and no Tier 2 "
        "instrument, so CET1 = Tier 1 = Total capital. The FY2025 note confirms it independently by printing all "
        "three RATIOS as the same 22.53%. Nothing is back-solved: the amount is stated, the RWA is stated, and "
        "448,062 / 1,988,661 = 22.53% is a check on the transcription, not the derivation of it.\n"
        "A CROSS-SOURCE DIVERGENCE AT FY2024, RECORDED AND NOT RECONCILED. For FY2024 the Annual Report's note "
        "gives CET1 435,464, RWA 1,961,726 and a 22.20% ratio, while the FY2024 PILLAR 3 gives 435,465, 1,963,743 "
        "and 22.18% - and it is the Pillar 3 figures that these sheets carry for FY2024, because FY2024 has its "
        "own Pillar 3 and this project takes each year from the document that reports it. So the FY2025 and FY2024 "
        "columns on the capital sheets rest on two different sources, by design. The gap is small (RWA differs by "
        "$2.0m, 0.1%) and is not an error in either document; it is the ordinary difference between a regulatory "
        "disclosure and an annual-report note. Do not 'fix' either to match the other.\n"
        "STILL BLANK FOR FY2025, and now stated as such in the cells rather than left empty: the Leverage Ratio, "
        "LCR and NSFR sheets, and the KM1 sheet. The FY2025 Annual Report contains no leverage ratio figure "
        "('leverage ratio' appears once, in a list of what the Board Risk Committee reviews), and the strings "
        "'liquidity coverage', 'LCR' and 'NSFR' appear ZERO times in its whole 836,000-character text "
        "extraction - against 334 '%' signs and a full capital note in the same extraction, so the zero is a "
        "fact about the document and not a failed search. Those three metrics live only in the Pillar 3, and "
        "there is no FY2025 Pillar 3. Nothing is substituted from the Bahraini parent's group disclosures.\n\n"
        + P3_COMPARATIVE_NOTE
    )


bw = BankWorkbook(bank_name="Gulf International Bank (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="38AD47")

STATEMENTS_SOURCES = (
    "Sources - Gulf International Bank (UK) Limited's own Statement of Financial Position / Statement of "
    "Income (converted from USD to £, see FX conversion note below), transcribed from Companies House filings "
    "(FY2024/FY2023 text-native; FY2022/FY2021/FY2020 scanned/image-only, no text layer):\n"
    f"FY2024/FY2023: Annual Report and Financial Statements 2024, pp.105-108 (Statement of Financial Position, "
    f"Statement of Income, Statement of Comprehensive Income, Statement of Changes in Equity) - {AR2024_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2023, pp.67-70 (own FY2022 comparative column) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, pp.48-51 - {AR2021_URL}\n"
    f"FY2020: Annual Report and Financial Statements 2020, pp.25-28 (Statement of Financial Position p.25, "
    f"Income Statement p.26, Statement of Comprehensive Income p.27, Statement of Changes in Equity p.28) - "
    f"{AR2020_URL}\n"
    f"FY2025: Annual Report and Financial Statements 2025, printed p.27 (Statement of Financial Position), "
    f"p.28 (Statement of Income), p.29 (Statement of Comprehensive Income), p.30 (Statement of Changes in "
    f"Equity), p.31 (Statement of Cash Flow) - text-native, Docusign-signed, published on the Bank's OWN "
    f"document library rather than Companies House - {AR2025_URL}\n"
    "FY2025 IS TAKEN FROM ITS OWN EDITION AND FY2024 IS NOT TOUCHED, which matters here because the FY2025 "
    "edition RE-PRESENTS and RESTATES its 2024 comparatives. Its Statement of Financial Position carries the "
    "footnote 'The Statement of Financial Position has been re-presented to better reflect the order of "
    "liquidity of assets and liabilities'; its note 6 labels the 2024 debt-securities column 'Restated' "
    "(gross 1,015,642 and allowance (169) against the FY2024 edition's own 1,015,473 and (20) - the same net "
    "1,015,473 either way); and its Statement of Cash Flow is headed '*Restated - refer to note 31', with a "
    "2024 operating total of (7,350,610) against the FY2024 edition's own (7,404,448). Every FY2024 cell in "
    "this workbook remains that year's OWN originally-published figure. None of the restated comparatives is "
    "used anywhere, and none is reconciled to the figures held here.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet (raw USD, then converted via stock())
# ---------------------------------------------------------------
balance_sheet_rows_usd = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 13858303, "FY2024": 7378636, "FY2023": 14883184, "FY2022": 5325978, "FY2021": 5599337, "FY2020": 5069290}),
    ("DATA", "Placements with banks", {"FY2025": 3942292, "FY2024": 5666838, "FY2023": 5290351, "FY2022": 3661166, "FY2021": 3805701, "FY2020": 4988056}),
    ("DATA", "Investment in group entities", {"FY2020": 341}),
    ("DATA", "Trading securities", {"FY2025": 157317, "FY2024": 141808, "FY2023": 111752, "FY2022": 73490, "FY2021": 56471, "FY2020": 33405}),
    ("DATA", "Derivative financial asset", {"FY2025": 66838, "FY2024": 89160, "FY2023": 73778, "FY2022": 69607, "FY2021": 22397, "FY2020": 15196}),
    ("DATA", "Debt securities at amortised cost", {"FY2025": 2634985, "FY2024": 1015473, "FY2023": 969443, "FY2022": 983131, "FY2021": 1001816, "FY2020": 277194}),
    ("DATA", "Property, plant and equipment", {"FY2025": 2237, "FY2024": 2762, "FY2023": 3363, "FY2022": 3915, "FY2021": 5087, "FY2020": 1390}),
    ("DATA", "Right-of-use assets", {"FY2025": 7837, "FY2024": 21499, "FY2023": 23857, "FY2022": 25740, "FY2021": 28260, "FY2020": 31706}),
    ("DATA", "Other assets", {"FY2025": 159938, "FY2024": 182679, "FY2023": 207336, "FY2022": 115596, "FY2021": 56297, "FY2020": 43583}),
    ("DATA", "Current tax asset", {"FY2022": 918, "FY2021": 1026, "FY2020": 2483}),
    # FY2025 edition's own caption for the same kind of item; kept as its own row
    # rather than folded into "Current tax asset" above, which is the caption the
    # FY2020-FY2022 editions print.
    ("DATA", "Current tax receivable", {"FY2025": 1483}),
    ("TOTAL", "Total assets", {"FY2025": 20831230, "FY2024": 14498855, "FY2023": 21563064, "FY2022": 10259541, "FY2021": 10576392, "FY2020": 10462644}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 1076079, "FY2024": 1159003, "FY2023": 76401, "FY2022": 370965, "FY2021": 35438, "FY2020": 180064}),
    ("DATA", "Deposits from customers", {"FY2025": 19161886, "FY2024": 12755439, "FY2023": 20851700, "FY2022": 9323428, "FY2021": 10022108, "FY2020": 9774293}),
    ("DATA", "Derivative financial liability", {"FY2025": 12565, "FY2024": 7739, "FY2023": 50031, "FY2022": 43543, "FY2021": 54878, "FY2020": 65930}),
    ("DATA", "Deferred tax liability", {"FY2025": 5612, "FY2024": 6226, "FY2023": 12219, "FY2022": 5032, "FY2021": 1851}),
    ("DATA", "Other liabilities", {"FY2025": 103590, "FY2024": 109076, "FY2023": 113887, "FY2022": 97890, "FY2021": 55256, "FY2020": 49761}),
    # DASH, as printed: the FY2025 edition prints a literal "-" in this row's 2025
    # column (Statement of Financial Position, printed p.27). Per the 2026-09-18
    # rule a printed dash is kept as "-", not blanked - the Bank is saying it had
    # no current tax liability, which is a different statement from silence. It is
    # handled after conversion (see DASH_CELLS below) because "-" is not a number.
    ("DATA", "Current tax liabilities", {"FY2024": 1546, "FY2023": 775}),
    ("TOTAL", "Total liabilities", {"FY2025": 20359732, "FY2024": 14039029, "FY2023": 21105013, "FY2022": 9840858, "FY2021": 10169531, "FY2020": 10070048}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 250000, "FY2024": 250000, "FY2023": 250000, "FY2022": 250000, "FY2021": 250000, "FY2020": 250000}),
    ("DATA", "Capital contribution", {"FY2025": 2279, "FY2024": 2279, "FY2023": 2279, "FY2022": 2279, "FY2021": 2279, "FY2020": 2279}),
    ("DATA", "Cashflow hedge reserve", {"FY2025": -324, "FY2024": 1928}),
    ("DATA", "Pension reserves", {"FY2025": 8738, "FY2024": 8724, "FY2023": 32878, "FY2022": 33390, "FY2021": 28678, "FY2020": 7473}),
    ("DATA", "Retained earnings", {"FY2025": 210805, "FY2024": 196895, "FY2023": 172894, "FY2022": 133014, "FY2021": 125904, "FY2020": 132844}),
    ("TOTAL", "Total equity", {"FY2025": 471498, "FY2024": 459826, "FY2023": 458051, "FY2022": 418683, "FY2021": 406861, "FY2020": 392596}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 20831230, "FY2024": 14498855, "FY2023": 21563064, "FY2022": 10259541, "FY2021": 10576392, "FY2020": 10462644}),
]

# Cells the Bank prints as a literal dash rather than a figure. Applied AFTER
# conversion, because a dash is not a number and must not go through stock().
# A dash is the Bank stating the row does not apply to it - not a blank (never
# published) and not a zero (a measured nil). Rule changed 2026-09-18.
DASH_CELLS_BALANCE_SHEET = {"Current tax liabilities": ["FY2025"]}

balance_sheet_rows = []
for kind, label, usd in balance_sheet_rows_usd:
    if kind == "SECTION":
        balance_sheet_rows.append((kind, label, {}))
        continue
    vals = dict(stock(usd))
    for y in DASH_CELLS_BALANCE_SHEET.get(label, []):
        vals[y] = "-"
    balance_sheet_rows.append((kind, label, vals))

bw.add_balance_sheet_sheet(
    title="Gulf International Bank (UK) Limited — Statement of Financial Position",
    subtitle="£m, converted from USD - see source note at bottom for FX methodology and rates used. FY2025 added 2026-09-18 from the Bank's own FY2025 Annual Report.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=409,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (raw USD, then converted via flow())
# ---------------------------------------------------------------
income_statement_rows_usd = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income from financial instruments at amortised cost", {"FY2025": 706142, "FY2024": 1030743, "FY2023": 702928, "FY2022": 222570, "FY2021": 27749, "FY2020": 66271}),
    ("DATA", "Other interest income/(expense)", {"FY2025": -2603, "FY2024": 30875, "FY2023": 57071, "FY2022": 399, "FY2021": -6645, "FY2020": -12565}),
    ("DATA", "Interest expense from financial instruments at amortised cost", {"FY2025": -628602, "FY2024": -987369, "FY2023": -679131, "FY2022": -184447, "FY2021": -9043, "FY2020": -39415}),
    ("TOTAL", "Net interest income", {"FY2025": 74937, "FY2024": 74249, "FY2023": 80868, "FY2022": 38522, "FY2021": 12061, "FY2020": 14291}),
    ("DATA", "Net fee and commission income", {"FY2025": 2482, "FY2024": 5455, "FY2023": 3415, "FY2022": 2128, "FY2021": 4036, "FY2020": 5188}),
    ("DATA", "Net trading income/(loss)", {"FY2025": -3972, "FY2024": 5358, "FY2023": 7376, "FY2022": 4753, "FY2021": 3371, "FY2020": -4106}),
    ("DATA", "Foreign exchange income and revaluation of foreign currencies", {"FY2025": 8600, "FY2024": 8150, "FY2023": 15526, "FY2022": 11764, "FY2021": 10845, "FY2020": 10204}),
    ("DATA", "Expected credit loss charge/(release) on financial assets", {"FY2025": -436, "FY2024": 166, "FY2023": -199, "FY2022": -140, "FY2021": -162, "FY2020": -149}),
    ("DATA", "Other operating income/(loss)", {"FY2025": 2490, "FY2024": 4133, "FY2023": 2852, "FY2022": 4801, "FY2021": 491, "FY2020": -5803}),
    ("DATA", "Impairment of right-of-use asset", {"FY2021": -1199}),
    ("DATA", "Operating expenses", {"FY2025": -65634, "FY2024": -65407, "FY2023": -57344, "FY2022": -52682, "FY2021": -43014, "FY2020": -38820}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": 18467, "FY2024": 32104, "FY2023": 52494, "FY2022": 9146, "FY2021": -13571, "FY2020": -19195}),
    ("DATA", "Income tax (expense)/credit", {"FY2025": -4557, "FY2024": -8103, "FY2023": -12614, "FY2022": -2036, "FY2021": 6631, "FY2020": 2416}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 13910, "FY2024": 24001, "FY2023": 39880, "FY2022": 7110, "FY2021": -6940, "FY2020": -16779}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Net movement in cash flow hedge reserve", {"FY2025": -3003, "FY2024": 2571}),
    ("DATA", "Tax relating to cash flow hedge reserve", {"FY2025": 751, "FY2024": -643}),
    ("DATA", "Remeasurement of defined benefit pension fund", {"FY2025": -31, "FY2024": -32186, "FY2023": -426, "FY2022": 6016, "FY2021": 28694, "FY2020": 17500}),
    ("DATA", "Tax relating to defined benefit pension", {"FY2025": 45, "FY2024": 8032, "FY2023": -86, "FY2022": -1304, "FY2021": -7489, "FY2020": -2451}),
    ("TOTAL", "Other comprehensive income for the year, net of tax", {"FY2025": -2238, "FY2024": -22226, "FY2023": -512, "FY2022": 4712, "FY2021": 21205, "FY2020": 15049}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 11672, "FY2024": 1775, "FY2023": 39368, "FY2022": 11822, "FY2021": 14265, "FY2020": -1730}),
]
income_statement_rows = [
    (kind, label, {} if kind == "SECTION" else flow(usd))
    for kind, label, usd in income_statement_rows_usd
]

bw.add_income_statement_sheet(
    title="Gulf International Bank (UK) Limited — Statement of Income",
    subtitle="£m, converted from USD - see source note at bottom for FX methodology and rates used. FY2025 added 2026-09-18 from the Bank's own FY2025 Annual Report.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=409,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity - built year-by-year per the map's
# per-year reconciliation ladder: each TOTAL "At 31 December YYYY" row below
# was checked to tie to (a) its own component's Balance Sheet figure above
# and (b) the following year's own opening row, in USD, before conversion.
# A "FX translation effect on equity, net" plug row (Total column only,
# computed as the balancing figure) makes each year's roll-forward tie
# exactly in GBP too, since opening/movement/closing convert at different
# point-in-time rates (same pattern as this entity's own Cash Flow FX plug).
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Capital contribution", "Pension reserve", "Cashflow hedge reserve", "Retained earnings", "Total equity"]
EQUITY_ROWS_USD = [
    ("TOTAL", "At 1 January 2020", [250000, 2279, -7576, None, 149480, 394183], "spot", "FY2019"),
    ("DATA", "Opening adjustment - GIBUK/GIB AM income reclassification (FY2020)", [None, None, None, None, 143, 143], "avg", "FY2020"),
    ("DATA", "Deferred tax liability on defined benefit pension (FY2020)", [None, None, -2451, None, None, -2451], "avg", "FY2020"),
    ("DATA", "Pension reserves (FY2020)", [None, None, 17500, None, None, 17500], "avg", "FY2020"),
    ("TOTAL", "Total other comprehensive income (FY2020)", [None, None, 15049, None, None, 15049], "avg", "FY2020"),
    ("DATA", "Net loss for the year (FY2020)", [None, None, None, None, -16779, -16779], "avg", "FY2020"),
    ("TOTAL", "Total comprehensive income for the year (FY2020)", [None, None, 15049, None, -16779, -1730], "avg", "FY2020"),
    ("DATA", "FX translation effect on equity, net (FY2020)", [None, None, None, None, None, None], "plug", "FY2020"),
    ("TOTAL", "At 31 December 2020", [250000, 2279, 7473, None, 132844, 392596], "spot", "FY2020"),

    ("DATA", "Deferred tax liability on defined benefit pension (FY2021)", [None, None, -7489, None, None, -7489], "avg", "FY2021"),
    ("DATA", "Pension reserves (FY2021)", [None, None, 28694, None, None, 28694], "avg", "FY2021"),
    ("TOTAL", "Total other comprehensive income (FY2021)", [None, None, 21205, None, None, 21205], "avg", "FY2021"),
    ("DATA", "Net loss for the year (FY2021)", [None, None, None, None, -6940, -6940], "avg", "FY2021"),
    ("TOTAL", "Total comprehensive income for the year (FY2021)", [None, None, 21205, None, -6940, 14265], "avg", "FY2021"),
    ("DATA", "FX translation effect on equity, net (FY2021)", [None, None, None, None, None, None], "plug", "FY2021"),
    ("TOTAL", "At 31 December 2021", [250000, 2279, 28678, None, 125904, 406861], "spot", "FY2021"),

    ("DATA", "Deferred tax liability on defined benefit pension (FY2022)", [None, None, -1304, None, None, -1304], "avg", "FY2022"),
    ("DATA", "Pension reserves (FY2022)", [None, None, 6016, None, None, 6016], "avg", "FY2022"),
    ("TOTAL", "Total other comprehensive income (FY2022)", [None, None, 4712, None, None, 4712], "avg", "FY2022"),
    ("DATA", "Net profit for the year (FY2022)", [None, None, None, None, 7110, 7110], "avg", "FY2022"),
    ("TOTAL", "Total comprehensive income for the year (FY2022)", [None, None, 4712, None, 7110, 11822], "avg", "FY2022"),
    ("DATA", "FX translation effect on equity, net (FY2022)", [None, None, None, None, None, None], "plug", "FY2022"),
    ("TOTAL", "At 31 December 2022", [250000, 2279, 33390, None, 133014, 418683], "spot", "FY2022"),

    ("DATA", "Deferred tax liability on defined benefit pension (FY2023)", [None, None, -86, None, None, -86], "avg", "FY2023"),
    ("DATA", "Pension reserves (FY2023)", [None, None, -426, None, None, -426], "avg", "FY2023"),
    ("TOTAL", "Total other comprehensive income (FY2023)", [None, None, -512, None, None, -512], "avg", "FY2023"),
    ("DATA", "Net profit for the year (FY2023)", [None, None, None, None, 39880, 39880], "avg", "FY2023"),
    ("TOTAL", "Total comprehensive income for the year (FY2023)", [None, None, -512, None, 39880, 39368], "avg", "FY2023"),
    ("DATA", "FX translation effect on equity, net (FY2023)", [None, None, None, None, None, None], "plug", "FY2023"),
    ("TOTAL", "At 31 December 2023", [250000, 2279, 32878, None, 172894, 458051], "spot", "FY2023"),

    ("DATA", "Pension reserves (FY2024)", [None, None, -32186, None, None, -32186], "avg", "FY2024"),
    ("DATA", "Deferred tax liability on defined benefit pension (FY2024)", [None, None, 8032, None, None, 8032], "avg", "FY2024"),
    ("DATA", "Net movement in cash flow hedge reserve (FY2024)", [None, None, None, 2571, None, 2571], "avg", "FY2024"),
    ("DATA", "Tax relating to cash flow hedge reserve (FY2024)", [None, None, None, -643, None, -643], "avg", "FY2024"),
    ("TOTAL", "Total other comprehensive income (FY2024)", [None, None, -24154, 1928, None, -22226], "avg", "FY2024"),
    ("DATA", "Net profit for the year (FY2024)", [None, None, None, None, 24001, 24001], "avg", "FY2024"),
    ("TOTAL", "Total comprehensive income for the year (FY2024)", [None, None, -24154, 1928, 24001, 1775], "avg", "FY2024"),
    ("DATA", "FX translation effect on equity, net (FY2024)", [None, None, None, None, None, None], "plug", "FY2024"),
    ("TOTAL", "At 31 December 2024", [250000, 2279, 8724, 1928, 196895, 459826], "spot", "FY2024"),

    # FY2025 block added 2026-09-18 (GA-006) from the FY2025 Annual Report's own
    # Statement of Changes in Equity, printed p.30. Ties in USD exactly, which is
    # the test this sheet applies to every year: opening 459,826 + total
    # comprehensive income 11,672 = 471,498, and 471,498 is independently the
    # FY2025 Statement of Financial Position's own Total equity (printed p.27).
    # Each component also ties: pension 8,724 + 14 = 8,738; hedge 1,928 - 2,252 =
    # (324); retained 196,895 + 13,910 = 210,805.
    ("DATA", "Pension reserves (FY2025)", [None, None, -31, None, None, -31], "avg", "FY2025"),
    ("DATA", "Deferred tax liability on defined benefit pension (FY2025)", [None, None, 45, None, None, 45], "avg", "FY2025"),
    ("DATA", "Net movement in cash flow hedge reserve (FY2025)", [None, None, None, -3003, None, -3003], "avg", "FY2025"),
    ("DATA", "Tax relating to cash flow hedge reserve (FY2025)", [None, None, None, 751, None, 751], "avg", "FY2025"),
    ("TOTAL", "Total other comprehensive income (FY2025)", [None, None, 14, -2252, None, -2238], "avg", "FY2025"),
    ("DATA", "Net profit for the year (FY2025)", [None, None, None, None, 13910, 13910], "avg", "FY2025"),
    ("TOTAL", "Total comprehensive income for the year (FY2025)", [None, None, 14, -2252, 13910, 11672], "avg", "FY2025"),
    ("DATA", "FX translation effect on equity, net (FY2025)", [None, None, None, None, None, None], "plug", "FY2025"),
    ("TOTAL", "At 31 December 2025", [250000, 2279, 8738, -324, 210805, 471498], "spot", "FY2025"),
]


def _rate(rtype, ry):
    return FX_SPOT[ry] if rtype == "spot" else FX_AVG[ry]


_equity_totals_usd = {}
for _kind, _label, _vals, _rtype, _ry in EQUITY_ROWS_USD:
    if _kind == "TOTAL" and _rtype == "spot":
        _equity_totals_usd[_label] = _vals

EXTRA_MOVEMENT_LABELS = {
    # FY2020's roll-forward includes a one-off retained-earnings reclassification
    # adjustment (see source note) that is not itself part of "Total comprehensive
    # income" - it must be folded into the movement sum below, else the FX plug
    # would silently absorb it as if it were a currency-translation effect.
    "FY2020": ["Opening adjustment - GIBUK/GIB AM income reclassification (FY2020)"],
}

FX_PLUG_GBP = {}
for _ry in ["FY2020", "FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]:
    _prev_year = PREV_YEAR[_ry]
    _open_label = "At 1 January 2020" if _ry == "FY2020" else f"At 31 December {int(_prev_year[2:])}"
    _close_label = f"At 31 December {int(_ry[2:])}"
    _opening_gbp = round(_equity_totals_usd[_open_label][-1] / FX_SPOT[_prev_year] / 1000, 1)
    _closing_gbp = round(_equity_totals_usd[_close_label][-1] / FX_SPOT[_ry] / 1000, 1)
    _movement_gbp = round(
        sum(
            v[-1] for k, l, v, rt, ry in EQUITY_ROWS_USD
            if ry == _ry and rt == "avg"
            and (
                (k == "TOTAL" and l.startswith("Total comprehensive income"))
                or l in EXTRA_MOVEMENT_LABELS.get(_ry, [])
            )
        ) / FX_AVG[_ry] / 1000,
        1,
    )
    FX_PLUG_GBP[_ry] = round(_closing_gbp - _opening_gbp - _movement_gbp, 1)

equity_changes_rows = []
for kind, label, vals, rtype, ry in EQUITY_ROWS_USD:
    if rtype == "plug":
        row_vals = [None] * (len(EQUITY_HEADERS) - 1) + [FX_PLUG_GBP[ry]]
    else:
        rate = _rate(rtype, ry)
        row_vals = [None if v is None else round(v / rate / 1000, 1) for v in vals]
    equity_changes_rows.append((kind, label, row_vals))

EQUITY_SOURCES = (
    STATEMENTS_SOURCES + "\n\n"
    "FX METHODOLOGY FOR THIS SHEET: opening/closing balances converted at that year-end's spot rate, movement "
    "lines at that year's average rate - the same convention used throughout this workbook. Converting stocks "
    "and flows at different rates within one year means the roll-forward doesn't tie exactly in GBP even though "
    "it ties exactly in USD (independently verified against each year's own source table before conversion) - "
    "an explicit 'FX translation effect on equity, net' row (Total column only, computed as the balancing "
    "figure) is included each year, same treatment as this entity's own Cash Flow Statement's 'Effect of "
    "GBP/USD translation' line. Zero plug rows were needed in USD terms - every year's own closing balance ties "
    "exactly to both the next year's own opening balance and that year's Balance Sheet Total equity.\n\n"
    "FY2020 has one additional wrinkle, disclosed in the Annual Report and Financial Statements 2020's own "
    "Statement of Changes in Equity footnote (p.28): a $143k 'Opening adjustment' to retained earnings, "
    "explained as 'in relation to the classification error whereby the 2019 GIBUK income had been classified as "
    "GIB AIM income. This had been corrected at the time of the preparation of prior year GIB AIM financial "
    "statements. Given these financial statements are prepared on a standalone basis, therefore it has been "
    "disclosed as an opening adjustment.' Included in this sheet as its own row (converted at FY2020's average "
    "rate, folded into the FX-plug movement calculation so it isn't mistaken for a currency-translation effect) "
    "- USD ties exactly: $394,183k (1 Jan 2020) + $143k (adjustment) + -$1,730k (total comprehensive loss) = "
    "$392,596k (31 Dec 2020), matching both the Balance Sheet's own Total equity and the FY2021 roll-forward's "
    "own opening balance."
)

bw.add_equity_changes_sheet(
    title="Gulf International Bank (UK) Limited — Statement of Changes in Equity",
    subtitle="£m, converted from USD - chronological, oldest to newest. See source note for FX methodology.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=56,
    source_height=409,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD, then converted via flow()/stock()/opening_cash())
# ---------------------------------------------------------------
rows_usd = [
    ("SECTION", "Operating cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 18467, "FY2024": 32104, "FY2023": 52494, "FY2022": 9146, "FY2021": -13571, "FY2020": -19195}),
    ("DATA", "Income tax (paid)/received", {"FY2025": -8149, "FY2024": -6050, "FY2023": -3870, "FY2022": 0, "FY2021": 2400, "FY2020": -1049}),
    ("DATA", "Depreciation of property and equipment", {"FY2025": 708, "FY2024": 902, "FY2023": 1060, "FY2022": 1211, "FY2021": 1270, "FY2020": 1320}),
    ("DATA", "Depreciation of ROU assets", {"FY2025": 2167, "FY2024": 2358, "FY2023": 1883, "FY2022": 2520, "FY2021": 2247, "FY2020": 2121}),
    ("DATA", "Change in accrued interest receivable", {"FY2025": 61479, "FY2024": -4050, "FY2023": -90461, "FY2022": -47278, "FY2021": 10789, "FY2020": 8386}),
    ("DATA", "Change in accrued interest payable", {"FY2025": -31841, "FY2024": -4230, "FY2023": 7017, "FY2022": 45097, "FY2021": -649, "FY2020": -6604}),
    ("DATA", "Change in other net assets (incl. movements to pension reserve)", {"FY2023": 11798, "FY2022": -68074, "FY2021": -7360, "FY2020": 38153}),
    ("DATA", "Change in other operating assets and liabilities", {"FY2025": 17247, "FY2024": -56920}),
    ("DATA", "Change in trading securities", {"FY2025": -15509, "FY2024": -30056, "FY2023": -38262, "FY2022": -17018, "FY2021": -23066, "FY2020": -5937}),
    ("DATA", "Change in placements with banks", {"FY2025": 1724546, "FY2024": -376341, "FY2023": -1629689, "FY2022": 144535, "FY2021": 994557, "FY2020": -226199}),
    ("DATA", "Change in debt securities at amortised cost/investment securities net", {"FY2023": 13993, "FY2022": 18566, "FY2021": -724622, "FY2020": -99922}),
    ("DATA", "Change in debt securities at amortised cost", {"FY2024": -46010}),
    ("DATA", "Change in deposits from banks", {"FY2025": -82924, "FY2024": 1179214, "FY2023": -536019, "FY2022": 893757, "FY2021": -144626, "FY2020": -631458}),
    ("DATA", "Change in deposits from customers", {"FY2025": 6406447, "FY2024": -8096261, "FY2023": 11528272, "FY2022": -698680, "FY2021": 247815, "FY2020": -665755}),
    ("DATA", "Finance costs (lease liability)", {"FY2025": 955, "FY2024": 1058, "FY2023": 1093, "FY2022": 1125}),
    ("DATA", "Finance costs (lease liability) and FX loss on reval of lease liability", {"FY2021": 940, "FY2020": 3466}),
    # FY2025-only add-back, a line the earlier editions do not print.
    ("DATA", "Unrealised gains or losses on debt securities", {"FY2025": 21082}),
    ("DATA", "Impairment", {"FY2025": 436, "FY2024": -166, "FY2023": 199, "FY2022": 119, "FY2021": 1199}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities", {"FY2025": 8115111, "FY2024": -7404448, "FY2023": 9319508, "FY2022": 287025, "FY2021": 347323, "FY2020": -1602673}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Net purchase of property and equipment", {"FY2025": -183, "FY2024": -302, "FY2023": -508, "FY2022": -39, "FY2021": -4966, "FY2020": -735}),
    # FY2025 splits debt-securities activity into gross purchases and gross
    # sales/maturities inside INVESTING, where earlier editions carried a single
    # net movement inside OPERATING. Two different presentations of the same
    # activity; neither is restated onto the other.
    ("DATA", "Purchase of debt securities at amortised cost", {"FY2025": -3209049}),
    ("DATA", "Sale and maturity of debt securities at amortised cost", {"FY2025": 1568142}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -1641090, "FY2024": -302, "FY2023": -508, "FY2022": -39, "FY2021": -4966, "FY2020": -735}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Payment of principal portion of lease liabilities", {"FY2025": -3437, "FY2024": -3186, "FY2023": -3249, "FY2022": -2115, "FY2021": -108, "FY2020": -808}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": -3437, "FY2024": -3186, "FY2023": -3249, "FY2022": -2115, "FY2021": -108, "FY2020": -808}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": 6470584, "FY2024": -7407936, "FY2023": 9315751, "FY2022": 284871, "FY2021": 342249, "FY2020": -1604216}),
    ("DATA", "Net foreign exchange difference (as reported, USD)", {"FY2025": 9083, "FY2024": -96612, "FY2023": 241455, "FY2022": -558230}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 7378636, "FY2024": 14883184, "FY2023": 5325978, "FY2022": 5599337, "FY2021": 5257088, "FY2020": 6861304}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 13858303, "FY2024": 7378636, "FY2023": 14883184, "FY2022": 5325978, "FY2021": 5599337, "FY2020": 5257088}),
]

_usd_by_label = {label: usd for _, label, usd in rows_usd}
rows = []
for kind, label, usd in rows_usd:
    if kind == "SECTION":
        rows.append((kind, label, {}))
    elif label == "Cash and cash equivalents at beginning of year":
        rows.append((kind, label, opening_cash(usd)))
    elif label == "Cash and cash equivalents at end of year":
        rows.append((kind, label, stock(usd)))
    else:
        rows.append((kind, label, flow(usd)))
    if label == "Net foreign exchange difference (as reported, USD)":
        # £ translation plug (see FX_NOTE): stocks (opening/closing) and flows
        # (everything else) are converted at different rates, so the £ statement
        # needs an explicit reconciling line to tie exactly. Computed programmatically
        # from the actual converted figures, per year, so it can never drift out of
        # sync with the rates above.
        opening_gbp = opening_cash(_usd_by_label["Cash and cash equivalents at beginning of year"])
        closing_gbp = stock(_usd_by_label["Cash and cash equivalents at end of year"])
        net_change_gbp = flow(_usd_by_label["Net (decrease)/increase in cash and cash equivalents"])
        fx_gbp = flow(usd)
        plug = {
            y: round(closing_gbp[y] - opening_gbp[y] - net_change_gbp[y] - fx_gbp.get(y, 0), 1)
            for y in closing_gbp
        }
        rows.append(("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", plug))

bw.add_cash_flow_sheet(
    title="Gulf International Bank (UK) Limited — Statement of Cash Flow",
    subtitle="£m, converted from USD - see source note at bottom for FX methodology and rates used. FY2025 added 2026-09-18 from the Bank's own FY2025 Annual Report.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=409,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality - GIB UK does not lend to customers (its own filings
# confirm no "Loans and advances to customers" line exists anywhere on the
# Balance Sheet); credit risk sits in Placements with banks (Note 4) and
# Debt securities at amortised cost (Note 6), each with their own IFRS 9
# stage/internal-rating table. Every year, both are 100% Stage 1 /
# Investment grade 1-4 - confirmed by reading each note in full, not
# assumed from the aggregate ECL charge being small.
# ---------------------------------------------------------------
asset_quality_rows_usd = [
    ("SECTION", "Placements with banks - gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (Investment grade 1-4)", {"FY2025": 3942912, "FY2024": 5667335, "FY2023": 5290994, "FY2022": 3661305, "FY2021": 3805820, "FY2020": 4988141}),
    ("DATA", "Stage 2 (Sub-investment grade 5-7)", {}),
    ("DATA", "Stage 3 (Classified 8-10)", {}),
    ("TOTAL", "Total gross placements with banks", {"FY2025": 3942912, "FY2024": 5667335, "FY2023": 5290994, "FY2022": 3661305, "FY2021": 3805820, "FY2020": 4988141}),
    ("DATA", "Less: allowance for impairment losses", {"FY2025": -620, "FY2024": -497, "FY2023": -643, "FY2022": -139, "FY2021": -119, "FY2020": -85}),
    ("TOTAL", "Net placements with banks", {"FY2025": 3942292, "FY2024": 5666838, "FY2023": 5290351, "FY2022": 3661166, "FY2021": 3805701, "FY2020": 4988056}),
    ("SECTION", "Debt securities at amortised cost - gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (Investment grade 1-4)", {"FY2025": 2635467, "FY2024": 1015473, "FY2023": 969443, "FY2022": 983625, "FY2021": 1002191, "FY2020": 277441}),
    ("DATA", "Stage 2 (Sub-investment grade 5-7)", {}),
    ("DATA", "Stage 3 (Classified 8-10)", {}),
    ("TOTAL", "Total gross debt securities at amortised cost", {"FY2025": 2635467, "FY2024": 1015473, "FY2023": 969443, "FY2022": 983625, "FY2021": 1002191, "FY2020": 277441}),
    ("DATA", "Less: allowance for impairment losses", {"FY2025": -482, "FY2024": -20, "FY2023": -305, "FY2022": -494, "FY2021": -375, "FY2020": -247}),
    ("TOTAL", "Net debt securities at amortised cost", {"FY2025": 2634985, "FY2024": 1015473, "FY2023": 969443, "FY2022": 983131, "FY2021": 1001816, "FY2020": 277194}),
]
# DASHES, as printed (rule changed 2026-09-18). Both FY2025 stage tables print a
# literal "-" in every Stage 2 and Stage 3 cell - the Bank stating it has no
# stage-2 or stage-3 exposure, which is a stronger statement than a blank. Only
# FY2025 is converted here: FY2020-FY2024 were transcribed under the old rule
# that blanked a dash, and re-reading five earlier editions to convert them is
# the dedicated conversion pass's job, not this one's. So on these two rows a
# "-" means "read under the new rule" and a blank means "not yet re-read" - NOT
# "never published".
DASH_CELLS_ASSET_QUALITY = {"Stage 2 (Sub-investment grade 5-7)": ["FY2025"],
                            "Stage 3 (Classified 8-10)": ["FY2025"]}

asset_quality_rows = []
for kind, label, usd in asset_quality_rows_usd:
    if kind == "SECTION":
        asset_quality_rows.append((kind, label, {}))
        continue
    vals = dict(stock(usd))
    for y in DASH_CELLS_ASSET_QUALITY.get(label, []):
        vals[y] = "-"
    asset_quality_rows.append((kind, label, vals))
# Coverage ratios - genuinely trivial (0.00-0.04%) given every asset is
# Stage 1/Investment grade; computed from the USD figures directly (a
# dimensionless ratio, so FX conversion doesn't change it).
_placements_gross_usd = {"FY2025": 3942912, "FY2024": 5667335, "FY2023": 5290994, "FY2022": 3661305, "FY2021": 3805820, "FY2020": 4988141}
_placements_ecl_usd = {"FY2025": 620, "FY2024": 497, "FY2023": 643, "FY2022": 139, "FY2021": 119, "FY2020": 85}
_debt_sec_gross_usd = {"FY2025": 2635467, "FY2024": 1015473, "FY2023": 969443, "FY2022": 983625, "FY2021": 1002191, "FY2020": 277441}
_debt_sec_ecl_usd = {"FY2025": 482, "FY2024": 20, "FY2023": 305, "FY2022": 494, "FY2021": 375, "FY2020": 247}
asset_quality_rows.append((
    "DATA", "Placements with banks - ECL coverage ratio",
    {y: f"{_placements_ecl_usd[y] / _placements_gross_usd[y] * 100:.3f}%" for y in _placements_gross_usd},
))
asset_quality_rows.append((
    "DATA", "Debt securities - ECL coverage ratio",
    {y: f"{_debt_sec_ecl_usd[y] / _debt_sec_gross_usd[y] * 100:.3f}%" for y in _debt_sec_gross_usd},
))

ASSET_QUALITY_SOURCES = (
    "Sources - Gulf International Bank (UK) Limited's own Note 4 (Placements with banks) / Note 6 (Debt "
    "securities at amortised cost) IFRS 9 stage and internal-credit-rating tables, converted from USD to £ (see "
    "FX conversion note on the Cash Flow Statement sheet):\n"
    f"FY2024/FY2023: Annual Report and Financial Statements 2024, pp.124-128 (Notes 4, 4.1, 6, 6.1) - {AR2024_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2023, pp.87-93 (Notes 4, 4.1, 6, 6.1, own FY2022 "
    f"comparative) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, pp.68-70 (Notes 4, 4.1, 6, 6.1) - {AR2021_URL}\n"
    f"FY2020: Annual Report and Financial Statements 2020, pp.46-50 (Notes 4, 4.1 Placements with banks; Note 6, "
    f"6.1 'Financial investments other than those measured at FVTPL' - FY2020's own note numbering/title for "
    f"what later years call 'Debt securities at amortised cost') - {AR2020_URL}\n\n"
    "GIB UK does not lend to customers - confirmed by reading: there is no 'Loans and advances to customers' "
    "line anywhere in the Balance Sheet across all 5 years reviewed. Its credit risk instead sits entirely in "
    "Placements with banks and Debt securities at amortised cost, each disclosed on the Bank's own internal "
    "credit rating scale (Investment grade 1-4 / Sub-investment grade 5-7 / Classified 8-10) cross-referenced "
    "to IFRS 9 stage. Every year, both asset classes are 100% Stage 1 / Investment grade 1-4, with no transfers "
    "to Stage 2 or 3 disclosed in any year - confirmed by reading each note in full, not assumed from the small "
    "ECL charge. ECL coverage ratios are correspondingly minimal (well under 0.1%).\n\n"
    + ENTITY_NOTE
)

bw.add_asset_quality_sheet(
    title="Gulf International Bank (UK) Limited — Asset Quality",
    subtitle="£m, converted from USD - see source note. GIB UK does not lend to customers; credit risk sits in Placements with banks and Debt securities at amortised cost. FY2025 added 2026-09-18; its Stage 2/Stage 3 cells carry the literal '-' the Bank prints.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=409,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    # source_height: 140 -> 320 earlier on 2026-09-16 (the citation gained the
    # comparative-column basis block), then -> 409 later the same day, when the
    # capture/recovery account and the FY2020 two-bases blocks took it past
    # 12,000 characters. 409 points is Excel's MAXIMUM row height, so the cell
    # still cannot show the whole citation at once - a reader may need to widen
    # the row or read it in the formula bar. The text is complete in the cell;
    # only the default display is short.
    # note_height: 60 -> 200 for the same reason (the longest per-sheet note,
    # Leverage Ratio's, is now ~4,000 characters).
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52,
                        source_height=409, note_height=200)


CAPITAL_USD = {"FY2025": 448062, "FY2024": 435465, "FY2023": 411658, "FY2022": 368416, "FY2021": 371866, "FY2020": 393000}
RWA_USD = {"FY2025": 1988661, "FY2024": 1963743, "FY2023": 1809984, "FY2022": 1557567, "FY2021": 1932234, "FY2020": 1482000}
CAPITAL_RATIO = {"FY2025": "22.53%", "FY2024": "22.18%", "FY2023": "22.74%", "FY2022": "23.65%", "FY2021": "19.22%", "FY2020": "26.48%"}

# ---------------------------------------------------------------
# FY2020 ON TWO BASES (found 2026-09-16 when the FY2021 edition was recovered).
# The dicts above are each year's OWN edition as reported. For FY2020 that is
# the Basel II-era FY2020 edition: capital base $393,000k (Share Capital $250m
# + Retained Earnings $143m, reported to the regulator, no CRR deductions),
# Total RWAs $1,482,000k ($1,482m as printed in $ millions), Tier 1 and Total
# Capital ratio both 26.48%.
#
# The FY2021 edition's own 2020 comparative column restates all three onto the
# CRR/CRD V basis: CET1 $378,549k (after deducting the pension asset net of
# deferred tax, intangibles and the prudent valuation adjustment - see the
# COMPARATIVE-COLUMN BASIS note), RWEA $1,482,468k (the same total to $'000
# precision rather than $ millions), and a ratio of 26.04%.
#
# These are DIFFERENT DEFINITIONS, not a correction of an error, so both are
# carried on separate labelled rows. Neither is reconciled and neither
# overwrites the other. The dicts below hold only the FY2020 restated values.
# ---------------------------------------------------------------
CAPITAL_USD_FY2020_RESTATED = {"FY2020": 378549}
RWA_USD_FY2020_RESTATED = {"FY2020": 1482468}
CAPITAL_RATIO_FY2020_RESTATED = {"FY2020": "26.04%"}

RESTATED_LABEL = "(FY2020 as restated in the FY2021 edition's own 2020 comparative column, CRR basis)"

FY2020_BASIS_NOTE = (
    "\n\nFY2020 IS CARRIED ON TWO BASES (added 2026-09-16, both kept, deliberately NOT reconciled). The first row "
    "above is the FY2020 Pillar 3 edition's own as-reported figure, on the Basel II-era basis that document uses. "
    "The second row is the FY2021 Pillar 3 edition's own 2020 comparative column, which restates FY2020 onto the "
    "CRR/CRD V basis that applies from FY2021 onward. The difference in the capital figure is definitional: the "
    "FY2020 edition reports a capital base of $393,000k (Share Capital $250m plus Retained Earnings $143m, as "
    "reported to the regulator, with no regulatory deductions applied), whereas the FY2021 edition arrives at "
    "$378,549k by starting from Total equity of $392,596k - which ties exactly to this workbook's own Balance "
    "Sheet for FY2020 - and deducting the defined benefit pension asset net of deferred tax ($13,932k), "
    "intangibles ($0) and the prudent valuation adjustment ($115k), per CRR Article 36(1). Neither figure is "
    "wrong; they answer different questions. A trend read across FY2020-FY2024 should use the restated row, "
    "because FY2021 onward is on the CRR basis. Note also that the FY2021 edition prints the 2020 RWA total to "
    "$'000 precision ($1,482,468k) where the FY2020 edition prints $ millions ($1,482m) - the same underlying "
    "total, carried at both precisions rather than one silently replacing the other."
)

# ---------------------------------------------------------------
# KM1 Key Metrics - GIB UK's own published UK KM1 template, reproduced as
# printed. Called BEFORE the first add_metric_sheet() so the sheet lands
# immediately after Asset Quality and immediately before CET1 Capital.
#
# CURRENCY. Left in US$'000 exactly as GIB UK publishes it, even though every
# other sheet in this workbook is converted to £m. That is KM1-004 rule (d):
# a KM1 sheet stays in the currency the bank published it in, because this
# sheet reproduces a disclosure rather than deriving a view. Do NOT run these
# through stock()/flow() - the conversion helpers are for the metric sheets.
#
# WHICH EDITION EACH COLUMN COMES FROM. GIB UK adopted the template in its
# FY2022 edition. Each edition prints TWO value columns, the reporting year
# and one prior year, so:
#   FY2024 <- FY2024 edition, "T - Current year" column (31-Dec-24)
#   FY2023 <- FY2023 edition, "T - Current year" column (31-Dec-23)
#   FY2022 <- FY2022 edition, "T - Current year" column (31-Dec-22)
#   FY2021 <- FY2022 edition's PRIOR-YEAR column (31-Dec-21). FY2021 has no
#             own-edition KM1 - see the row-set test in KM1_SOURCES.
#   FY2020 <- blank. The FY2020 edition is a Basel II-era document that
#             predates the template entirely.
#   FY2025 <- blank. No FY2025 Pillar 3 has been published.
#
# ROW SET drifts between editions and this sheet shows the UNION in the
# template's canonical order: rows 14a and 14b are printed ONLY by the FY2023
# edition (which fills them for its own year alone), the FY2022 edition prints
# them as empty cells, and the FY2024 edition omits both rows outright.
#
# ZERO GLYPHS. GIB UK uses NO dashes in this table - every unused cell is a
# shaded EMPTY cell, confirmed by rendering the page and looking at it, not by
# trusting the text layer. Those are left blank here. The single "0.00%" in the
# FY2021 column of row 9 is a printed measured zero and is kept as a zero.
# ---------------------------------------------------------------
km1_rows = [
    # GA-006 (2026-09-18): FY2025 and FY2020 held no cell at all, so a reader saw
    # two blank year columns and the census scored FY2025 as a gap. Both absences
    # are established and are stated in the sources note; they now appear IN the
    # columns. Labelled so verify_workbook's _metric_sheet_for resolves them to no
    # metric sheet - these are statement rows, not template rows, and nothing on
    # the template itself is computed, reordered or restated.
    ("DATA", "[No UK KM1 published for this year - see note below]",
     {"FY2025": "Not published - no FY2025 Pillar 3 disclosure",
      "FY2020": "Not applicable - FY2020 edition predates the UK KM1 template"}),
    ("SECTION", "Available own funds (amounts) — US$'000", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital",
     {"FY2024": 435465, "FY2023": 411658, "FY2022": 368416, "FY2021": 371866}),
    ("DATA", "2    Tier 1 capital",
     {"FY2024": 435465, "FY2023": 411658, "FY2022": 368416, "FY2021": 371866}),
    ("DATA", "3    Total capital",
     {"FY2024": 435465, "FY2023": 411658, "FY2022": 368416, "FY2021": 371866}),
    ("SECTION", "Risk-weighted exposure amounts — US$'000", {}),
    ("DATA", "4    Total risk-weighted exposure amount",
     {"FY2024": 1963743, "FY2023": 1809984, "FY2022": 1557567, "FY2021": 1932234}),
    ("SECTION", "Capital ratios  (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2024": "22.18%", "FY2023": "22.74%", "FY2022": "23.65%", "FY2021": "19.22%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2024": "22.18%", "FY2023": "22.74%", "FY2022": "23.65%", "FY2021": "19.22%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2024": "22.18%", "FY2023": "22.74%", "FY2022": "23.65%", "FY2021": "19.22%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted "
                "exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2024": "4.05%", "FY2023": "5.21%", "FY2022": "5.21%", "FY2021": "7.13%"}),
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)", {}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)", {}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2024": "12.05%", "FY2023": "13.21%", "FY2022": "13.21%", "FY2021": "15.13%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "UK 8a    Conservation buffer due to macro-prudential or systemic risk identified at the "
             "level of a Member State (%)", {}),
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2024": "0.12%", "FY2023": "0.13%", "FY2022": "0.08%", "FY2021": "0.00%"}),
    ("DATA", "UK 9a    Systemic risk buffer (%)", {}),
    ("DATA", "10    Global Systemically Important Institution buffer (%)", {}),
    ("DATA", "UK 10a    Other Systemically Important Institution buffer", {}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2024": "2.62%", "FY2023": "2.63%", "FY2022": "2.58%", "FY2021": "2.50%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2024": "14.67%", "FY2023": "15.84%", "FY2022": "15.79%", "FY2021": "17.63%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2024": "10.13%", "FY2023": "9.53%", "FY2022": "10.44%", "FY2021": "4.09%"}),
    ("SECTION", "Leverage ratio — US$'000 / %", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks",
     {"FY2024": 8682283, "FY2023": 7795728, "FY2022": 5136739, "FY2021": 5268295}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2024": "5.02%", "FY2023": "5.28%", "FY2022": "7.17%", "FY2021": "7.06%"}),
    ("SECTION", "Additional leverage ratio disclosure requirements", {}),
    ("DATA", "14a    Fully loaded ECL accounting model leverage ratio excluding claims on central "
             "banks (%)  [row printed only in the FY2023 edition]", {"FY2023": "5.28%"}),
    ("DATA", "14b    Leverage ratio including claims on central banks (%)  [row printed only in the "
             "FY2023 edition]", {"FY2023": "1.92%"}),
    ("DATA", "14c    Average leverage ratio excluding claims on central banks (%)", {}),
    ("DATA", "14d    Average leverage ratio including claims on central banks (%)", {}),
    ("DATA", "14e    Countercyclical leverage ratio buffer (%)", {}),
    ("SECTION", "Liquidity Coverage Ratio — US$'000 / %", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value -average)",
     {"FY2024": 8650825, "FY2023": 15980246, "FY2022": 9198733, "FY2021": 6737809}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value",
     {"FY2024": 3507666, "FY2023": 6524697, "FY2022": 3302507, "FY2021": 2006717}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value",
     {"FY2024": 486306, "FY2023": 944921, "FY2022": 705128, "FY2021": 603374}),
    ("DATA", "16    Total net cash outflows (adjusted value)",
     {"FY2024": 3021360, "FY2023": 5579776, "FY2022": 2597379, "FY2021": 1403343}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2024": "286.32%", "FY2023": "286.40%", "FY2022": "354.15%", "FY2021": "480.13%"}),
    ("SECTION", "Net Stable Funding Ratio — US$'000 / %", {}),
    ("DATA", "18    Total available stable funding",
     {"FY2024": 5139351, "FY2023": 4607371, "FY2022": 4297495}),
    ("DATA", "19    Total required stable funding",
     {"FY2024": 2225713, "FY2023": 1822687, "FY2022": 1031978}),
    ("DATA", "20    NSFR ratio (%)",
     {"FY2024": "230.91%", "FY2023": "252.78%", "FY2022": "416.49%"}),
]

KM1_SOURCES = (
    "Sources - Gulf International Bank (UK) Limited's own \"Key metrics (UK KM1)\" template, US$'000 and "
    "percentages exactly as printed, entity basis (GIB UK is a standalone non-consolidated reporting entity; "
    "see the ENTITY NOTE on the other Pillar 3 sheets):\n"
    f"FY2024: 2024 Pillar 3 disclosures, printed p.6, \"Key metrics (UK KM1)\", \"T - Current year\" column "
    f"(31-Dec-24) - {P3_2024_URL}\n"
    f"FY2023: 2023 Pillar 3 disclosures, printed p.6, same table, \"T - Current year\" column (31-Dec-23) - "
    f"{P3_2023_URL}\n"
    f"FY2022: 2022 Pillar 3 disclosures, printed p.6, same table, \"T - Current year\" column (31-Dec-22) - "
    f"{P3_2022_URL}\n"
    f"FY2021: the PRIOR-YEAR column (31-Dec-21) of that same FY2022 edition - see the edition note below - "
    f"{P3_2022_URL}\n"
    "\n"
    "CURRENCY. This sheet is in US$'000, the currency GIB UK publishes the template in, while every other "
    "sheet in this workbook is converted to £m at the Bank of England rates listed on those sheets. That is "
    "deliberate: the KM1 sheet reproduces a published disclosure rather than deriving a view, so it is not "
    "converted. Do not compare its amount rows against the £m sheets without converting first; the ratio rows "
    "are currency-free and do compare directly.\n"
    "\n"
    "SOURCE DEFECT IN THE COLUMN HEADER, REPRODUCED NOT CORRECTED. Every edition heads its second value "
    "column \"T-4 - Prior year\" while dating it one year before the reporting date (the FY2024 edition's "
    "reads \"T-4 - Prior year / 31-Dec-23\"). T-4 would be 31-Dec-20. The DATE is right and the T-label is "
    "wrong - the column is the immediately preceding year throughout, which is confirmed by the figures "
    "themselves: the FY2024 edition's prior-year column reproduces the FY2023 edition's current-year column "
    "exactly ($411,658k CET1, 1,809,984 RWEA, 22.74%). Columns here are assigned by the printed DATE, not by "
    "the T-label.\n"
    "\n"
    "EDITION CHOICE, AND WHY FY2021 COMES FROM THE FY2022 EDITION. GIB UK adopted the template in its FY2022 "
    "edition, so FY2024, FY2023 and FY2022 each come from the edition in which that year is the reporting "
    "year. The FY2021 edition publishes NO KM1 - its contents page has no key-metrics entry, and a full-text "
    "search of the recovered document returns zero hits on \"KM1\", \"key metric\" and \"UK KM\" while "
    "returning 65 hits on \"capital\", 102 on \"ratio\", 19 on \"buffer\" and 15 on \"leverage\", so the zero "
    "is a fact about the document and not a failure of the search. What that edition prints instead, under "
    "the heading \"Key ratios / 1. Capital\", is a 13-row summary that FAILS THE TEMPLATE'S ROW-SET TEST: it "
    "has no Total SREP own funds requirement, no overall capital requirement, no \"CET1 available after "
    "meeting the total SREP\" row, and no template liquidity rows at all - its LCR and NSFR are disclosed in "
    "a wholly different shape, as a separate quarterly table with Q1/Q2/Q3/Q4 columns rather than the "
    "template's single average column. It also adds a row the template does not have (\"Pension add-on "
    "44,500\", an amount printed inside a percentage section), and its leverage row is on the OTHER SIDE OF "
    "THE 1 JANUARY 2022 BASIS BREAK - \"Total leverage exposure measure 10,573,209 / Leverage ratio 3.52%\", "
    "which includes claims on central banks, against the template's excluding-central-bank-claims basis. That "
    "is a different and shorter table, not an unnumbered template, so it is NOT reproduced here and its rows "
    "are NOT mapped onto template row numbers. FY2021 is instead taken from the FY2022 edition's prior-year "
    "column, which is the earliest place the year appears inside the template itself. The FY2021 edition's "
    "own figures are not lost: they sit on their own labelled rows of the Leverage Ratio, LCR and NSFR "
    "sheets, on their own bases, and are not reconciled to these.\n"
    "\n"
    "FY2020 IS BLANK, AND THAT IS A DATED FACT ABOUT THE TEMPLATE, NOT A SOURCING GAP. The FY2020 edition is "
    "titled \"Basel II Pillar 3 Disclosures\" on its own cover and predates the UK KM1 template's "
    "introduction, so no edition of any year prints a FY2020 KM1 column: the FY2022 edition, the earliest "
    "that uses the template, reaches back only to 31-Dec-21. A full-text search of the recovered FY2020 "
    "document returns zero hits on \"KM1\", \"key metric\" and \"key ratios\" against 94 hits on \"capital\", "
    "80 on \"ratio\" and 20 on \"leverage\", so that zero is likewise a fact about the document. The image "
    "trap was checked too rather than assumed away: the three embedded bitmaps in that edition were rendered "
    "and LOOKED AT, and all three are diagrams - two governance org-charts on printed p.7 and the Bank's "
    "functional organisation chart on p.10 - with no key-metrics table among them. Nothing has been "
    "back-filled from the statutory accounts, which are a different basis.\n"
    "\n"
    "FY2025 IS BLANK. No FY2025 Pillar 3 has been published. Re-checked 16 September 2026 against the Bank's "
    "OWN live document library (https://gibam.com/document-library), not against this script's citation list: "
    "the page enumerates 27 PDFs, of which exactly one is a Pillar 3 document - the FY2024 edition. The page "
    "is demonstrably current (it carries 2025-dated documents including a 31-Dec-2025 pension implementation "
    "statement), so the absence is the Bank's and not our reach. Direct URL probes following this entity's "
    "own naming convention (2025-GIBUK-Pillar-3-disclosures-Board-approved.pdf, "
    "2025-GIBUK-Pillar-3-disclosures.pdf and 2025-GIBUK-Pillar-3_Final.pdf under the /production/documents/ "
    "path the FY2024 and FY2023 editions live at) each return a hard HTTP 404 with an XML error body, not a "
    "soft-404 HTML page. Checked, none newer.\n"
    "\n"
    "ROW SET, AND WHICH BLANKS MEAN WHAT. Rows UK 7b, UK 7c, UK 8a, UK 9a, 10, UK 10a, 14c, 14d and 14e are "
    "printed by GIB UK in every edition as EMPTY shaded cells - the Bank prints the row and leaves it "
    "unfilled - and are shown blank here. Rows 14a and 14b are different: only the FY2023 edition prints "
    "those two rows at all, filling them for its own reporting year only (5.28% and 1.92%); the FY2022 "
    "edition prints both rows empty in both its columns, and the FY2024 edition OMITS the two rows entirely "
    "from its table. Their blanks in the FY2024, FY2022 and FY2021 columns are therefore \"the Bank did not "
    "print a value\", not \"a value was not found\". Rows 18-20 are blank in the FY2021 column because the "
    "FY2022 edition leaves that whole NSFR block empty in its prior-year column. No row is blank here because "
    "it could not be located.\n"
    "\n"
    "ZERO GLYPHS. GIB UK uses NO dash or em-dash anywhere in this table; every unused cell is a shaded empty "
    "cell. This was confirmed by rendering the FY2024 page at 200 dpi and looking at it, because a dash and "
    "an empty cell are indistinguishable in a text-layer dump and the difference is load-bearing (a dash "
    "would still be a printed glyph). The one \"0.00%\" in row 9's FY2021 column is a printed measured zero "
    "and is kept as a zero, not blanked.\n"
    "\n"
    "TEXT-NATIVE, NO IMAGE TRAP IN THE TEMPLATE EDITIONS. The FY2024, FY2023 and FY2022 tables all extract as "
    "live text and were additionally verified against a 200 dpi render of the FY2024 page. The only embedded "
    "bitmaps in the FY2024 edition's KM1 page region are the GIB wordmark.\n"
    "\n"
    + P3_CAPTURE_NOTE
)

bw.add_km1_sheet(
    title="Gulf International Bank (UK) Limited — KM1 Key Metrics",
    subtitle="The Bank's own published UK key-metrics (KM1) template, reproduced in GIB UK's row order with "
             "its own template row numbers, labels and printed precision. Amounts in US$'000 AS PUBLISHED - "
             "this sheet is deliberately NOT converted to sterling, unlike every other sheet in this "
             "workbook. Entity basis. FY2025 and FY2020 carry a statement rather than figures because no edition "
             "publishes a KM1 for those years - FY2025 has no Pillar 3 at all, and the FY2020 edition predates "
             "the template; FY2021 comes from the FY2022 edition because the FY2021 edition prints a shorter "
             "bespoke table that is not the template.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=78,
    source_height=409,
)

metric("CET1 Capital", "£m (conv. from USD)",
       [
           ("Common Equity Tier 1 (CET1) capital", stock(CAPITAL_USD)),
           (f"CET1 capital after CRR regulatory adjustments {RESTATED_LABEL}", stock(CAPITAL_USD_FY2020_RESTATED)),
       ], p3_sources(),
       note="GIB UK's regulatory capital consists entirely of CET1 (fully paid-up ordinary shares, capital contribution, and audited retained earnings/reserves) - no AT1 or Tier 2 instruments in any year. FY2020's Basel II-era Pillar 3 document calls this figure 'Total regulatory capital' (comprising Share Capital $250m + Retained Earnings $143m = $393m, Tier 1 only, no Tier 2) rather than 'CET1' by name; the word 'CET1' does not appear anywhere in that document." + FY2020_BASIS_NOTE)
metric("CET1 Ratio", "% of RWA",
       [
           ("Common Equity Tier 1 (CET1) ratio", CAPITAL_RATIO),
           (f"CET1 ratio {RESTATED_LABEL}", CAPITAL_RATIO_FY2020_RESTATED),
       ], p3_sources(),
       note="FY2020's own edition prints no ratio called 'CET1 ratio' - it prints a Tier 1 ratio and a Total Capital ratio, both 26.48%, and that figure is used on all three ratio sheets for FY2020. The FY2021 edition's 2020 comparative column does name a CET1 ratio, 26.04%." + FY2020_BASIS_NOTE)
metric("Tier 1 Capital", "£m (conv. from USD)",
       [
           ("Tier 1 capital", stock(CAPITAL_USD)),
           (f"Tier 1 capital after CRR regulatory adjustments {RESTATED_LABEL}", stock(CAPITAL_USD_FY2020_RESTATED)),
       ], p3_sources(),
       note="Equal to CET1 capital in every year - the Bank holds no Additional Tier 1 (AT1) instruments." + FY2020_BASIS_NOTE)
metric("Tier 1 Ratio", "% of RWA",
       [
           ("Tier 1 ratio", CAPITAL_RATIO),
           (f"Tier 1 ratio {RESTATED_LABEL}", CAPITAL_RATIO_FY2020_RESTATED),
       ], p3_sources(), note=FY2020_BASIS_NOTE.strip())
metric("Total Capital", "£m (conv. from USD)",
       [
           ("Total capital", stock(CAPITAL_USD)),
           (f"Total capital after CRR regulatory adjustments {RESTATED_LABEL}", stock(CAPITAL_USD_FY2020_RESTATED)),
       ], p3_sources(),
       note="Equal to CET1/Tier 1 capital in every year - the Bank holds no AT1 or Tier 2 instruments." + FY2020_BASIS_NOTE)
metric("Total Capital Ratio", "% of RWA",
       [
           ("Total capital ratio", CAPITAL_RATIO),
           (f"Total capital ratio {RESTATED_LABEL}", CAPITAL_RATIO_FY2020_RESTATED),
       ], p3_sources(), note=FY2020_BASIS_NOTE.strip())
metric("Total RWAs", "£m (conv. from USD)",
       [
           ("Total risk-weighted exposure amount", stock(RWA_USD)),
           (f"Total risk-weighted exposure amount {RESTATED_LABEL}", stock(RWA_USD_FY2020_RESTATED)),
       ], p3_sources(),
       note="FY2020's own edition prints its RWA total in $ millions ($1,482m); the FY2021 edition's 2020 "
            "comparative column prints the same total to $'000 ($1,482,468k), and it is that finer figure to "
            "which the FY2020 RWA Breakdown components sum exactly. Both are shown." + FY2020_BASIS_NOTE)

# ---------------------------------------------------------------
# RWA Breakdown (UK OV1) - fully disclosed all 4 later years. FY2024/FY2023 from
# the Bank's own FY2024 Pillar 3 document (text-native); FY2022 from its
# own FY2023 Pillar 3 document; FY2021 sourced from that same FY2023
# Pillar 3 document's own T-4/prior-year comparative column (matches this
# project's existing convention, e.g. p3_sources() already does this for
# other metrics) rather than the dedicated FY2021 Pillar 3 document, since
# both give identical figures where legible. Each year's own Total ties
# exactly to the Total RWAs sheet above.
#
# FY2020 predates the UK OV1 template entirely - it's a Basel II-style
# disclosure with separate Credit risk / Market risk / Operational risk
# sections (section 4 of that document) and no CCR/CVA breakout at all (the
# document's own credit-risk table folds any counterparty exposure into the
# single Credit risk total). Market risk RWA ($143.75m) is stated directly;
# Operational risk RWA is not stated directly - only its capital requirement
# ($10.3m) is - so it's derived here as capital requirement x 12.5 (the same
# multiplier the document itself uses to turn market risk's capital
# requirement into an RWA figure, per its own section 4.2 methodology
# description). Summing the three derived FY2020 components (1,206.0 +
# 143.75 + 128.75 = 1,478.5) falls short of the document's own separately
# reported Total RWAs of $1,482m by $3.5m (~0.24%).
#
# THAT GAP IS NOW EXPLAINED AND CLOSED (2026-09-16). It was the missing CVA
# charge. The recovered FY2021 edition's section 5.2 table carries a full 2020
# comparative column on the CRR basis, and it states all four components
# directly, to $'000: credit and counterparty risk 1,206,179; market risk
# 142,838; operational risk 128,538 (stated, not derived); CVA risk 4,913.
# Those four sum to 1,482,468 EXACTLY, which is that table's own total and the
# $'000-precision version of the FY2020 edition's $1,482m. So the shortfall was
# the FY2020 edition simply not breaking out a CVA charge, plus $-million
# rounding - not a mis-cast line.
#
# Both presentations are kept. The original rows below are the FY2020 edition's
# own Basel II-era figures; a clearly labelled block at the end carries the
# FY2021 edition's restated 2020 column. Neither is reconciled away.
# ---------------------------------------------------------------
rwa_breakdown_rows_usd = [
    ("SECTION", "Credit risk", {}),
    ("DATA", "Credit risk (excluding CCR) - standardised approach", {"FY2024": 1704126, "FY2023": 1588788, "FY2022": 1426851, "FY2021": 1633319, "FY2020": 1206000}),
    ("SECTION", "Counterparty credit risk", {}),
    ("DATA", "Of which credit valuation adjustment (CVA)", {"FY2024": 15040, "FY2023": 20994, "FY2022": 20625, "FY2021": 12553}),
    ("DATA", "Of which other CCR", {"FY2024": 45049, "FY2023": 39716, "FY2022": 21799, "FY2021": 23092}),
    ("TOTAL", "Total counterparty credit risk - CCR", {"FY2024": 60089, "FY2023": 60709, "FY2022": 42424, "FY2021": 35645}),
    ("SECTION", "Market risk", {}),
    ("DATA", "Position, foreign exchange and commodities risks - standardised approach", {"FY2024": 819, "FY2023": 11263, "FY2022": 2332, "FY2021": 166380, "FY2020": 143750}),
    ("SECTION", "Operational risk", {}),
    ("DATA", "Operational risk - standardised approach", {"FY2024": 198710, "FY2023": 149224, "FY2022": 85961, "FY2021": 96890, "FY2020": 128750}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2024": 1963743, "FY2023": 1809984, "FY2022": 1557567, "FY2021": 1932234, "FY2020": 1482000}),
    # FY2020 on the CRR basis, as stated in the FY2021 edition's own 2020
    # comparative column (printed pp.24-25, section 5.2). Every figure below is
    # printed in that table - none is derived. Kept alongside, not instead of,
    # the FY2020 edition's own figures above.
    # FY2025 comes from a DIFFERENT TEMPLATE and therefore gets its own section
    # (this map's general point 2: a breakdown assembled from more than one source
    # template shows its templates as separate sections, so a reader can see which
    # basis each year came from). There is no FY2025 Pillar 3 and so no UK OV1 for
    # 2025; the only FY2025 RWA breakdown the Bank publishes is the four-way "Of
    # which" split inside its Annual Report's own capital-management note (printed
    # p.81). Its component set is NOT the OV1's: it prints a single combined
    # "Credit risk" where OV1 separates credit risk excluding CCR from other CCR,
    # so its credit line is not comparable with the rows above and is not placed on
    # them. The four components sum to 1,988,661 exactly, which is that note's own
    # separately-printed Total Risk exposure amount - no residual, nothing derived.
    ("SECTION", "FY2025 - Annual Report capital-management note (no FY2025 Pillar 3 / UK OV1 exists)", {}),
    ("DATA", "Credit risk (FY2025, AR basis - combines what UK OV1 splits into credit risk excl. CCR and other CCR)", {"FY2025": 1752265}),
    ("DATA", "Credit valuation adjustment (FY2025, AR basis)", {"FY2025": 17334}),
    ("DATA", "Market risk (FY2025, AR basis)", {"FY2025": 4277}),
    ("DATA", "Operational risk (FY2025, AR basis)", {"FY2025": 214785}),
    ("TOTAL", "Total risk exposure amount (FY2025, AR basis) - the four rows above sum to this exactly", {"FY2025": 1988661}),
    ("SECTION", "FY2020 restated - FY2021 edition's own 2020 comparative column (CRR basis, section 5.2)", {}),
    ("DATA", "Credit and counterparty risk, combined as the FY2021 edition presents it (FY2020 restated)", {"FY2020": 1206179}),
    ("DATA", "CVA risk (FY2020 restated) - not broken out at all in the FY2020 edition", {"FY2020": 4913}),
    ("DATA", "Market risk (FY2020 restated)", {"FY2020": 142838}),
    ("DATA", "Operational risk (FY2020 restated) - stated directly, not derived", {"FY2020": 128538}),
    ("TOTAL", "Total risk-weighted exposure amount (FY2020 restated) - the four rows above sum to this exactly", {"FY2020": 1482468}),
]
rwa_breakdown_rows = [
    (kind, label, {} if kind == "SECTION" else stock(usd))
    for kind, label, usd in rwa_breakdown_rows_usd
]

RWA_BREAKDOWN_SOURCES = (
    "Sources - Gulf International Bank (UK) Limited's own UK OV1 (Pillar 1 capital requirements) table (FY2021 "
    "onward) / Basel II-style capital requirements tables (FY2020 - see note below), converted from USD to £ "
    "(see FX conversion note on the Cash Flow Statement sheet; the underlying $ RWA figures are unconverted "
    "regulatory exposure amounts, converted here at spot rate for consistency with the rest of this workbook):\n"
    f"FY2024/FY2023: Pillar 3 Disclosures as at 31 December 2024 (Board-approved), pp.27-28 (section 6.2, UK "
    f"OV1) - {P3_2024_URL}\n"
    f"FY2022/FY2021: Pillar 3 Disclosures as at 31 December 2022, pp.26-27 (section 6.2, UK OV1) - FY2021 is "
    f"that document's own T-4/prior-year comparative column - {P3_2022_URL}\n"
    f"FY2020 (first block, the FY2020 edition's own Basel II-era figures): 'Basel II Pillar 3 Disclosures as at "
    f"31 December 2020', printed p.14 (section 4.1 credit risk RWA table, total 1,206; section 4.2 market risk "
    f"RWA table, total 143.75) and printed p.15 (section 4.3 operational risk - capital requirement of $10.3m "
    f"only) - {P3_2020_URL}. That edition predates the UK OV1 template and breaks out no CCR or CVA charge; its "
    "operational risk RWA is DERIVED here as capital requirement x 12.5, the same multiplier the document itself "
    "applies to market risk in its own section 4.2.\n"
    f"FY2020 (second block, restated): Pillar 3 Disclosures as at 31 December 2021, printed pp.24-25 (section 5.2 "
    f"'Pillar 1 capital requirements'), 2020 comparative column - {P3_2021_URL}. Every figure in that block is "
    "STATED in that table, including the operational risk RWA (so it is no longer derived) and a CVA risk RWA of "
    "$4,913k that the FY2020 edition does not disclose at all.\n"
    "THE PREVIOUSLY FLAGGED $3.5m FY2020 GAP IS NOW EXPLAINED AND CLOSED (2026-09-16). The three derivable "
    "FY2020-edition components sum to $1,478.5m against that edition's own separately reported Total RWAs of "
    "$1,482m. The restated block shows why: the missing piece is the CVA charge ($4,913k), which the Basel II-era "
    "edition does not break out, and the residual is $-million rounding. On the restated basis the four "
    "components sum to $1,482,468k exactly, with no gap. This is no longer an unexplained source-side "
    "discrepancy.\n\n"
    + ENTITY_NOTE
)

bw.add_rwa_breakdown_sheet(
    title="Gulf International Bank (UK) Limited — RWA Breakdown",
    subtitle="£m, converted from USD - see source note. UK OV1 template for FY2021-FY2024, with FY2025 and "
             "FY2020 in their own separately-labelled sections because each comes from a different source "
             "template (FY2025 from the Annual Report's capital note - there is no FY2025 Pillar 3; FY2020 from "
             "the Basel II-era edition, plus its restatement in the FY2021 edition).",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=68,
    source_height=409,
    unit_suffix=" (£m, conv. from USD)",
)

metric(
    "Leverage Ratio", "£m (conv. from USD) / %",
    [
        ("Total exposure measure", stock({
            "FY2024": 8682283, "FY2023": 7795728, "FY2022": 5136739, "FY2021": 10573209, "FY2020": 8524000,
        })),
        ("Leverage ratio (%)", {"FY2025": "Not published - no FY2025 Pillar 3; no leverage ratio in the FY2025 Annual Report", "FY2024": "5.02%", "FY2023": "5.28%", "FY2022": "7.17%", "FY2021": "3.52%", "FY2020": "4.61%"}),
        # RESTATEMENT, NOT A CORRECTION - see note. The FY2022 edition restates
        # FY2021 onto the excluding-central-bank-claims basis that took effect
        # 1 Jan 2022. Recorded on its own labelled rows alongside FY2021's
        # original as-reported figures above; the two are NOT reconciled and
        # neither overwrites the other.
        ("Total exposure measure excl. claims on central banks (FY2021 as restated in the FY2022 edition)", stock({
            "FY2021": 5268295,
        })),
        ("Leverage ratio excl. claims on central banks (%) (FY2021 as restated in the FY2022 edition)", {"FY2021": "7.06%"}),
        # Additional-disclosure row printed only in the FY2023 edition (KM1 14b);
        # the FY2022 edition leaves it blank, so it exists for FY2023 alone.
        ("Leverage ratio incl. claims on central banks (%) (additional disclosure, KM1 row 14b)", {"FY2023": "1.92%"}),
        # SAME PATTERN ONE YEAR EARLIER, found 2026-09-16 when the FY2021 edition
        # was recovered: its 2020 comparative column restates FY2020's leverage
        # on the CRR basis. Own labelled rows; the FY2020 edition's own 8,524 /
        # 4.61% above is untouched. Neither is reconciled to the other.
        ("Total exposure measure (FY2020 as restated in the FY2021 edition's own 2020 comparative column)", stock({
            "FY2020": 10426834,
        })),
        ("Leverage ratio (%) (FY2020 as restated in the FY2021 edition's own 2020 comparative column)", {"FY2020": "3.63%"}),
    ],
    p3_sources(),
    note="Basis change: FY2022 onward reports 'Total exposure measure EXCLUDING claims on central banks' (the "
         "Bank's own FY2021 report states it was 'not, currently, in scope of the UK Leverage Framework' that "
         "introduced this exclusion, effective 1 January 2022); FY2021/FY2020's figures on the first two rows are "
         "the single (unqualified) leverage ratio/exposure measure as originally reported those years, on an "
         "including-central-bank-claims basis. Each year's own as-reported figure is used rather than forcing a "
         "common basis. FY2020's own document reconciles this exposure measure directly from Total Assets per "
         "the Financial Statements ($10,463m) less securities-financing-transaction credit risk mitigation "
         "($1,928m) plus derivative add-ons ($25m) and other adjustments (-$35m) = $8,524m.\n\n"
         "FY2021 RESTATEMENT BETWEEN EDITIONS (found 2026-09-16, both figures kept, deliberately NOT reconciled). "
         "FY2021's leverage is printed on two different bases by two different documents, and rows 3-4 above "
         "record the second one: (a) the FY2021 Pillar 3 edition, as originally reported, gives a total exposure "
         "measure of $10,573,209k and a ratio of 3.52% - rows 1-2 above; (b) the FY2022 Pillar 3 edition's own "
         "T-4/prior-year (31-Dec-21) comparative column, KM1 rows 13-14, restates the same year EXCLUDING claims "
         "on central banks at $5,268,295k and 7.06% - rows 3-4 above, sourced from the FOLLOWING year's edition "
         "rather than the FY2021 edition itself. Neither is miscast: both tie internally against the same FY2021 "
         "CET1 of $371,866k ($371,866k / $10,573,209k = 3.52%; $371,866k / $5,268,295k = 7.06%), and the "
         "difference between the two exposure measures ($5,304,914k) is of the same order as FY2021 cash and cash "
         "equivalents ($5,599,337k), consistent with central bank claims being the item removed. This is the "
         "FY2022 edition presenting FY2021 on the new UK Leverage Framework basis for comparability with its own "
         "current year, as its section 6.6 describes; it is a restatement of basis, not a correction of a figure, "
         "so both are shown rather than one being chosen. Consequence for reading the trend: rows 1-2 are NOT a "
         "like-for-like series across FY2020-FY2024 (FY2020/FY2021 include central bank claims, FY2022 onward "
         "exclude them); for a like-for-like excluding-central-banks comparison use row 3-4's FY2021 against "
         "FY2022-FY2024, and for a like-for-like including-central-banks comparison FY2023's 1.92% on row 5 is "
         "the only later year for which the Bank publishes that basis.\n\n"
         "FY2020 RESTATEMENT BETWEEN EDITIONS (found 2026-09-16 on recovery of the FY2021 edition; the same "
         "two-bases pattern as FY2021, one year earlier; both figures kept, deliberately NOT reconciled). Rows 6-7 "
         "above record it. (a) The FY2020 edition, as originally reported, gives a total exposure measure of "
         "$8,524m and a ratio of 4.61% - rows 1-2 above - reconciled in its own section 7 table from Total Assets "
         "of $10,463m less SFT credit risk mitigation of $1,928m plus derivative add-ons of $25m and other "
         "adjustments of -$35m. (b) The FY2021 edition's own 2020 comparative column (printed p.6, key ratios) "
         "gives $10,426,834k and 3.63% - rows 6-7 above. Neither is miscast: the FY2020 edition's 4.61% ties "
         "against its own Tier 1 of $393m ($393m / $8,524m = 4.61%), and the FY2021 edition's 3.63% ties against "
         "its own restated FY2020 CET1 of $378,549k ($378,549k / $10,426,834k = 3.63%). The difference between "
         "the two exposure measures ($1,902,834k) is of the same order as the FY2020 edition's own SFT credit "
         "risk mitigation adjustment of $1,928m, consistent with the CRR basis not applying that netting - but "
         "that is an observation, not a reconciliation, and no figure here is derived from it. Consequence for "
         "reading the trend: rows 1-2 mix three bases across FY2020-FY2024 (FY2020 Basel II-era, FY2021 CRR "
         "including central bank claims, FY2022 onward CRR excluding them). Any leverage comparison should be "
         "made from this sheet, choosing rows on a single basis, rather than from the Overview sheet's single "
         "headline row.",
)

metric(
    "LCR", "£m (conv. from USD) / %",
    [
        ("Total high-quality liquid assets (HQLA / average liquid assets buffer)", stock({
            "FY2024": 8650825, "FY2023": 15980246, "FY2022": 9198733, "FY2021": 6737809, "FY2020": 5860000,
        })),
        ("Total net cash outflows, adjusted value", stock({
            "FY2024": 3021360, "FY2023": 5579776, "FY2022": 2597379, "FY2021": 1403343, "FY2020": 2019000,
        })),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "Not published - no FY2025 Pillar 3; no LCR in the FY2025 Annual Report", "FY2024": "286.32%", "FY2023": "286.40%", "FY2022": "354.15%", "FY2021": "480.13%", "FY2020": "290%"}),
        # FY2020 ON THE OTHER BASIS. Rows 1-3 carry FY2020 as the FY2020 edition
        # reports it: a point-in-time LCR "as at 31 December 2020". The FY2021
        # edition's quarterly table additionally gives FY2020 on the QUARTERLY-
        # AVERAGE basis - which is the basis FY2021's own figures on rows 1-3
        # use. Kept on separate rows: a point-in-time LCR and an average LCR are
        # not the same measure and must never be merged.
        ("Average liquid assets buffer, Q4 2020 (quarterly-average basis, FY2021 edition)", stock({
            "FY2020": 6237113,
        })),
        ("Average net flows, Q4 2020 (quarterly-average basis, FY2021 edition)", stock({
            "FY2020": 2141287,
        })),
        ("Average liquidity coverage ratio, Q4 2020 (%) (quarterly-average basis, FY2021 edition)", {"FY2020": "291.28%"}),
    ],
    p3_sources(),
    note="Methodology differs for FY2021: that year's Pillar 3 report discloses LCR as a quarterly (not annual) "
         "average - Q4 2021 is used here as the closest analogue to later years' 12-month-average KM1 figure. "
         "FY2021 NET CASH OUTFLOWS, RE-SOURCED 2026-09-16: this cell was previously blank because the FY2021 "
         "edition's own 'Average net flows' caption is not the later KM1 'Total net cash outflows (adjusted "
         "value)' definition and was not approximated. It is now filled with $1,403,343k taken from the FY2022 "
         "Pillar 3 Disclosures' own T-4/prior-year (31-Dec-21) comparative column, KM1 row 16 - i.e. from the "
         "FOLLOWING year's edition, not the FY2021 edition itself - where the Bank restates FY2021 onto the exact "
         "KM1 definition used for FY2022 onward, making it directly comparable. Two cross-checks passed: (a) that "
         "same column's HQLA ($6,737,809k) and LCR (480.13%) are identical to the figures already transcribed here "
         "from the FY2021 edition, so the two documents are on the same basis rather than two different ones; and "
         "(b) $6,737,809k / $1,403,343k = 480.13%, exactly reproducing the printed ratio. The FY2022 edition also "
         "prints the gross components for FY2021 ($2,006,717k cash outflows and $603,374k cash inflows, total "
         "weighted value, KM1 rows UK 16a/16b); these are not rows on this sheet for any other year and were not "
         "added for FY2021 alone. THE HESITATION BEHIND THAT NOTE IS NOW RESOLVED (2026-09-16): when the FY2021 "
         "edition was recovered and its own quarterly liquidity table read directly, its Q4 2021 'Average net "
         "flows' turned out to be $1,403,343k - numerically IDENTICAL to the FY2022 edition's KM1 row 16 figure "
         "above - and its Q4 2021 average outflows and inflows ($2,006,717k and $603,374k) are likewise identical "
         "to that edition's KM1 rows UK 16a/16b. So the two differently-captioned figures are the same number "
         "reported twice, and the FY2021 figure on this row is now corroborated by the FY2021 edition itself, not "
         "only by the following year's. FY2020's document uses its own pre-KM1 "
         "terms 'Liquidity Buffer' (used here as the HQLA-equivalent figure) and 'Total Net cash outflows'; its "
         "own headline LCR of 290% is 'excluding PRA Scalar' (its own footnote), with a lower 153% figure "
         "disclosed as the alternative including a 5% PRA Scalar add-on - the as-reported headline (excl. PRA "
         "Scalar) figure is used here for consistency with how later years' single as-reported ratio is shown, "
         "but the alternative basis is flagged since it is not a like-for-like methodology across all years.\n\n"
         "FY2020 IS ALSO CARRIED ON A SECOND, AVERAGING BASIS (rows 4-6 above, added 2026-09-16 on recovery of "
         "the FY2021 edition). This matters because the two are NOT the same measure and must not be merged. The "
         "FY2020 edition's own table (its section 5.3) is explicitly 'LCR as reported to the regulator AS AT 31 "
         "December 2020' - a point-in-time ratio - and that is what rows 1-3 carry for FY2020. The FY2021 "
         "edition's quarterly liquidity table (printed p.7) additionally reports FY2020 by quarter on an "
         "AVERAGING basis, and its Q4 2020 column gives an average liquidity coverage ratio of 291.28% on an "
         "average liquid assets buffer of $6,237,113k and average net flows of $2,141,287k. Two cross-checks "
         "passed: $6,237,113k / $2,141,287k = 291.28%, exactly reproducing the printed ratio; and that column's "
         "average net flows equal its own average outflows ($3,085,596k) less average inflows ($944,309k) "
         "exactly. This averaging basis is the SAME basis as the FY2021 figures already on rows 1-3 (which are "
         "that edition's Q4 2021 column), so rows 4-6 are what make FY2020 and FY2021 comparable to each other. "
         "Rows 1-3's FY2020 column is not comparable with its own FY2021 column, and neither FY2020 basis is "
         "identical to the 12-month-average KM1 figure used from FY2022 onward. Nothing was averaged, blended or "
         "back-solved here - every figure is printed in one of the two documents.",
)

metric(
    "NSFR", "£m (conv. from USD) / %",
    [
        # FY2020 FILLED 2026-09-16 (was blank). Source is NOT the FY2020 edition,
        # which discloses no NSFR at all, but the FY2021 edition's quarterly
        # liquidity table (printed p.7), whose 2020 block gives Q4 2020 directly.
        # Same Q4 quarterly basis as the FY2021 figures alongside, so these go in
        # the existing rows rather than on separate ones.
        ("Total available stable funding", stock({
            "FY2024": 5139351, "FY2023": 4607371, "FY2022": 4297495, "FY2021": 10511066, "FY2020": 10463760,
        })),
        ("Total required stable funding", stock({
            "FY2024": 2225713, "FY2023": 1822687, "FY2022": 1031978, "FY2021": 9455958, "FY2020": 10136594,
        })),
        ("Net Stable Funding Ratio (%)", {"FY2025": "Not published - no FY2025 Pillar 3; no NSFR in the FY2025 Annual Report", "FY2024": "230.91%", "FY2023": "252.78%", "FY2022": "416.49%", "FY2021": "111.16%", "FY2020": "103.23%"}),
    ],
    p3_sources(),
    note="FY2021 is that year's Q4 (year-end) quarterly figure, as originally disclosed in quarterly form; "
         "FY2022 onward is each year's single annual KM1 figure.\n\n"
         "FY2020 FILLED 2026-09-16 - THIS SHEET'S FY2020 COLUMN WAS PREVIOUSLY BLANK AND THE REASON GIVEN FOR "
         "THAT IS NOW SUPERSEDED. The old reason was correct as far as it went: the FY2020 Basel II-era Pillar 3 "
         "document genuinely discloses no NSFR ratio and no available/required stable funding figure of its own "
         "anywhere - its only mention of the concept is the upcoming regulatory 'binding NSFR measure of 100%' in "
         "its CRD V/CRR II preview section, which is not GIB UK's own ratio (re-confirmed by full-text search of "
         "the recovered document: 'NSFR' and 'stable funding' occur exactly once between them, in that preview). "
         "But the FY2021 edition, recovered on this date, carries a quarterly liquidity table (printed p.7) that "
         "reports BOTH 2021 and 2020 by quarter, and its Q4 2020 column states an NSFR of 103.23% on available "
         "stable funding of $10,463,760k and required stable funding of $10,136,594k. Those are the figures now "
         "in the FY2020 column. They are on the SAME Q4 quarterly basis as the FY2021 figures alongside them - "
         "which is why they occupy the same rows rather than separate labelled ones - and they are directly "
         "comparable with FY2021 but not strictly with the single annual KM1 figures from FY2022 onward. Cross-"
         "check passed: $10,463,760k / $10,136,594k = 103.23%, exactly reproducing the printed ratio. Nothing was "
         "derived: the ratio and both components are each printed in that table. FY2025 remains blank (no FY2025 "
         "edition published).",
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), source_height=409,
    per_note={"MREL Ratio": "No separate MREL ratio or instruments disclosed in any year, including FY2020 (its "
                             "Basel II-era Pillar 3 document has no MREL section or mention at all - a different, "
                             "and more basic, non-disclosure than later years' explained non-disclosure below). "
                             "The Bank's own FY2021 Pillar 3 report is the first to explain why: following the "
                             "Bank of England's 3 December 2021 Statement of Policy on MREL, 'GIB (UK)'s MREL "
                             "requirement is equal to its CRD V requirement under Pillar 1 and Pillar 2A. "
                             "Consequently, the Bank does not need to hold any MREL compliant instruments in "
                             "addition to those needed to satisfy its CRD V requirement' - i.e. MREL is fully "
                             "satisfied by ordinary capital, with no incremental MREL-specific ratio or "
                             "instrument stock to disclose.\nTHE PARENT-DISCLOSURE ROUTE WAS CONSIDERED AND DOES NOT APPLY HERE (checked 2026-09-16). A subsidiary's figures are often published only in its PARENT's Pillar 3, as columns of a shared table or in an appendix, so that is the first place to look before writing any non-disclosure. It does not rescue this row, for a reason that is about the obligation rather than about the documents: GIB (UK)'s OWN Pillar 3 states affirmatively that its MREL requirement EQUALS its CRD V Pillar 1 + Pillar 2A requirement and that it need hold no MREL-compliant instruments beyond those, so there is no separate MREL ratio in existence for any document to carry. This is affirmative evidence from the entity itself, not an absence inferred from a failed search. Note also that the parent is Gulf International Bank B.S.C. (Bahrain), a non-UK entity outside the Bank of England's MREL regime, and that under this project's entity-scope rule no parent-, KSA- or Abu Dhabi-branch figure may be substituted here in any case. FETCH STATUS, RECORDED HONESTLY: on 2026-09-16 www.gib.com returned HTTP 403 to every path tried INCLUDING the site root, so the parent's site was BLOCKED to us on that date. That is a fact about our reach and NOT evidence about what the parent publishes - and it supersedes this script's earlier note that gib.com is reachable. Nothing on this sheet rests on that blocked fetch."})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
cf_totals_usd = {
    "Net cash (outflow)/inflow from operating activities": {"FY2024": -7404448, "FY2023": 9319508, "FY2022": 287025, "FY2021": 347323, "FY2020": -1602673},
    "Net cash used in investing activities": {"FY2024": -302, "FY2023": -508, "FY2022": -39, "FY2021": -4966, "FY2020": -735},
    "Net cash used in financing activities": {"FY2024": -3186, "FY2023": -3249, "FY2022": -2115, "FY2021": -108, "FY2020": -808},
}
cf_close_usd = {"FY2024": 7378636, "FY2023": 14883184, "FY2022": 5325978, "FY2021": 5599337, "FY2020": 5257088}

balance_sheet_totals_usd = {
    "Total assets": {"FY2024": 14498855, "FY2023": 21563064, "FY2022": 10259541, "FY2021": 10576392, "FY2020": 10462644},
    "Placements with banks": {"FY2024": 5666838, "FY2023": 5290351, "FY2022": 3661166, "FY2021": 3805701, "FY2020": 4988056},
    "Deposits from customers": {"FY2024": 12755439, "FY2023": 20851700, "FY2022": 9323428, "FY2021": 10022108, "FY2020": 9774293},
    "Total equity": {"FY2024": 459826, "FY2023": 458051, "FY2022": 418683, "FY2021": 406861, "FY2020": 392596},
}
income_statement_totals_usd = {
    "Net interest income": {"FY2024": 74249, "FY2023": 80868, "FY2022": 38522, "FY2021": 12061, "FY2020": 14291},
    "Operating expenses": {"FY2024": -65407, "FY2023": -57344, "FY2022": -52682, "FY2021": -43014, "FY2020": -38820},
    "Profit/(loss) for the year": {"FY2024": 24001, "FY2023": 39880, "FY2022": 7110, "FY2021": -6940, "FY2020": -16779},
}
equity_changes_totals_usd = {
    "Opening equity": {"FY2024": 458051, "FY2023": 418683, "FY2022": 406861, "FY2021": 392596, "FY2020": 394183},
    "Total comprehensive income/(loss) for the year": {"FY2024": 1775, "FY2023": 39368, "FY2022": 11822, "FY2021": 14265, "FY2020": -1730},
    "Closing equity": {"FY2024": 459826, "FY2023": 458051, "FY2022": 418683, "FY2021": 406861, "FY2020": 392596},
}

bw.add_overview_sheet(
    cash_flow_totals=[(label, flow(vals)) for label, vals in cf_totals_usd.items()]
                      + [("Cash and cash equivalents at end of year", stock(cf_close_usd))],
    cash_flow_unit="£m (conv. from USD)",
    balance_sheet_totals=[(label, stock(vals)) for label, vals in balance_sheet_totals_usd.items()],
    balance_sheet_unit="£m (conv. from USD)",
    income_statement_totals=[(label, flow(vals)) for label, vals in income_statement_totals_usd.items()],
    income_statement_unit="£m (conv. from USD)",
    equity_changes_totals=[
        ("Opening equity", opening_cash(equity_changes_totals_usd["Opening equity"])),
        ("Total comprehensive income/(loss) for the year", flow(equity_changes_totals_usd["Total comprehensive income/(loss) for the year"])),
        ("Closing equity", stock(equity_changes_totals_usd["Closing equity"])),
    ],
    equity_changes_unit="£m (conv. from USD)",
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Tier 1 Ratio", CAPITAL_RATIO),
        ("Total Capital Ratio", CAPITAL_RATIO),
        ("Leverage Ratio", {"FY2024": "5.02%", "FY2023": "5.28%", "FY2022": "7.17%", "FY2021": "3.52%", "FY2020": "4.61%"}),
        ("LCR", {"FY2024": "286.32%", "FY2023": "286.40%", "FY2022": "354.15%", "FY2021": "480.13%", "FY2020": "290%"}),
        # FY2020 added 2026-09-16 to match the NSFR detail sheet, which is no
        # longer blank for that year. Overview is a COPY and does not inherit
        # detail-sheet changes, so it has to be updated alongside.
        ("NSFR", {"FY2024": "230.91%", "FY2023": "252.78%", "FY2022": "416.49%", "FY2021": "111.16%", "FY2020": "103.23%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation. All £ figures are converted from the Bank's native USD reporting (see Cash Flow Statement "
         "sheet's FX conversion note) - this conversion was not explicitly requested for this bank but applied "
         "for consistency with the rest of the series. FY2025 is blank throughout (no FY2025 Annual Report or "
         "Pillar 3 Disclosure published yet). FY2020's equity roll-forward row alone does not sum to the cent "
         "(Opening $394,183k + Total comprehensive income/(loss) -$1,730k = $392,453k, $143k short of the actual "
         "$392,596k closing balance) because of a one-off $143k retained-earnings reclassification adjustment "
         "disclosed that year (see the Statement of Changes in Equity sheet's own source note) - not an error.\n\n"
         "LEVERAGE RATIO - READ WITH CARE: the single Leverage Ratio row above is each year's own as-reported "
         "headline and is NOT a like-for-like series. FY2020 and FY2021 include claims on central banks in the "
         "exposure measure; FY2022 onward exclude them, following the UK Leverage Framework change effective "
         "1 January 2022. The FY2022 Pillar 3 edition's own prior-year comparative column additionally restates "
         "FY2021 onto the excluding-central-banks basis at 7.06% (vs the 3.52% shown above), and the FY2023 "
         "edition additionally publishes FY2023 on the including-central-banks basis at 1.92% (vs the 5.28% "
         "shown above). Both alternative-basis figures are recorded in full on the Leverage Ratio detail sheet, "
         "which is where any leverage comparison across years should be made from; they are omitted here only "
         "because this sheet carries one row per metric. As of 2026-09-16 there is a THIRD basis in play: the "
         "FY2021 Pillar 3 edition's own 2020 comparative column restates FY2020's leverage at 3.63% on an "
         "exposure measure of $10,426,834k (vs the 4.61% and $8,524m shown above, which are the FY2020 edition's "
         "own Basel II-era figures). So the single row above mixes three bases, not two. It is also recorded in "
         "full on the Leverage Ratio detail sheet.\n\n"
         "FY2020 CAPITAL AND CAPITAL RATIOS - READ WITH CARE (added 2026-09-16). The CET1/Tier 1/Total Capital "
         "Ratio rows above show 26.48% for FY2020, which is the FY2020 Pillar 3 edition's own as-reported figure "
         "on its Basel II-era basis, against a capital base of $393m and Total RWAs of $1,482m. The FY2021 "
         "edition's own 2020 comparative column restates the same year onto the CRR/CRD V basis at 26.04%, on "
         "CET1 of $378,549k (Total equity of $392,596k less the pension asset net of deferred tax, intangibles "
         "and the prudent valuation adjustment) and RWEA of $1,482,468k. Both are recorded on separate labelled "
         "rows on each capital and capital-ratio detail sheet; neither has been reconciled to the other or "
         "allowed to overwrite the other, and only the as-reported one is shown here because this sheet carries "
         "one row per metric. For a like-for-like trend across FY2020-FY2024, use the restated FY2020 row on the "
         "detail sheets, since FY2021 onward is already on the CRR basis.\n\n"
         "NSFR FY2020 (added 2026-09-16): this row was previously blank for FY2020 and is now 103.23%. The FY2020 "
         "Pillar 3 edition discloses no NSFR at all; the figure comes from the FY2021 edition's quarterly "
         "liquidity table, Q4 2020 column, which is the same quarterly basis as the FY2021 figure beside it. See "
         "the NSFR detail sheet. The FY2020 LCR of 290% above remains the FY2020 edition's own point-in-time "
         "ratio as at 31 December 2020; the LCR detail sheet additionally carries FY2020 on the quarterly-"
         "averaging basis (291.28%), which is the basis the FY2021 figure above uses. A point-in-time LCR and an "
         "average LCR are different measures and are deliberately not merged.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/GULF INTERNATIONAL BANK UK FINANCIALS.xlsx")
