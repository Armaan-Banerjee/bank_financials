# Orphaned-citation sweep — RESUME checkpoint

Started 2026-09-16. Task: sweep all 145 `scripts/build_*.py` for citations,
caveats and notes that exist in source but never reach the delivered workbook.

Method: `ast`-parse every build script; collect module-level assignment targets
whose literal value contains `http` or is substantial prose, plus every
module-level `FunctionDef`; count `ast.Name` loads of each name across the
module. Zero loads = orphan. Two passes were run (a name-pattern pass and a
broader "any prose/URL literal" pass) and unioned, so prose constants with
non-obvious names are included.

**Scan is complete. 86 orphaned definitions across 49 of 145 scripts.**
(79 constants + 7 functions.)

## Status legend

- `FIX` — intent unambiguous, wire in following the script's own conventions.
- `REPORT` — ambiguous / deliberate leftover / would change what a citation claims.
- `LOCKED` — another agent is editing this script right now; defer to a later pass.

Locked scripts (do NOT edit this pass): gulf_international_bank_uk,
arab_bank_europe, firstbank_uk, united_trust_bank, tsb, itau_bba_international,
philippine_national_bank_europe, aib_uk, melli_bank, and the `id_` conversion
batch (atom, bank_of_africa, chetwood, credit_suisse, fce, hampden, hsbc_uk,
methodist_chapel_aid, natwest, recognise, smbc, ubp, united_national,
unity_trust, vanquis, zenith).

---

## A. Full finding list (raw scan output, pre-triage)

| script | orphan | kind | line | year in YEARS? |
|---|---|---|---|---|
| build_abc_international_bank.py | AR2018_URL | const | 65 | yes |
| build_access_bank.py | convert_bs_rows | func | 212 | n/a |
| build_afin_bank.py | CH_OVERVIEW_URL | const | 36 | n/a |
| build_afin_bank.py | CH_2024_ACCOUNTS_URL | const | 38 | yes |
| build_aib_uk.py | CH_URL | const | 12 | n/a |
| build_aldermore.py | CH_2018_URL | const | 110 | yes |
| build_aldermore.py | INTERIM_HEADERS | const | — | n/a |
| build_allica.py | HISTORICAL_DEPTH_NOTE | const | 21 | n/a |
| build_alrayan.py | CH_URL | const | 28 | n/a |
| build_alrayan.py | AR2020_URL | const | 33 | yes |
| build_arbuthnot_latham.py | AR2017_URL | const | 10 | yes |
| build_atom_bank.py | AR17_URL, P3_FY24_URL, AR24_URL | const | 15/21/122 | yes |
| build_bank_of_africa_uk.py | AR2021_URL, AR2019_URL | const | 15/19 | yes |
| build_bank_of_beirut_uk.py | CH_URL, AR2024_URL, AR2017_URL | const | 13/15/18 | yes |
| build_bank_of_china_uk.py | AR2014_URL, AR2010_URL | const | 37/66 | yes |
| build_barclays_bank_plc.py | AR24_URL_STATEMENTS, P3_2023_URL | const | 36/292 | yes |
| build_birmingham_bank.py | P3_2023_URL | const | 23 | yes |
| build_blme.py | CH_URL | const | 18 | n/a |
| build_castle_trust.py | P3_2020_URL | const | 22 | **no** |
| build_cater_allen.py | SANT2023_URL, SANT2024_URL | const | 23/24 | yes |
| build_clearbank.py | AR2016_URL | const | 16 | **no** |
| build_coop_bank.py | INTERIM_HEADERS | const | — | n/a |
| build_cynergy_bank.py | P3_2021_CDN_URL, P3_2022_CDN_URL, P3_INDEX_URL | const | 79/80/82 | yes |
| build_db_uk_bank.py | P3_2025_URL, P3_2024_URL, P3_2023_URL | const | 93/94/95 | yes |
| build_fidbank_uk.py | CAPITAL_RATIO_NOTE | const | 164 | n/a |
| build_firstbank_uk.py | AR2022_URL | const | 20 | yes |
| build_gatehouse.py | AR2022_URL | const | 10 | yes |
| build_ghana_international_bank.py | CH_2019_URL | const | 63 | yes |
| build_hampden_co.py | P3_2022_URL | const | 49 | yes |
| build_handelsbanken.py | P3_2022_URL, AA2019_URL | const | 15/21 | yes |
| build_hsbc_uk_bank_plc.py | AR2022_URL | const | 10 | yes |
| build_icbc_london.py | P3_23_KM1_NOTE | const | 154 | yes |
| build_icbc_standard_bank.py | AR_STATEMENT_SOURCES_2015_2020 | const | 27 | yes |
| build_icici_bank_uk.py | AR2024_URL | const | 88 | yes |
| build_jp_morgan_europe.py | AR2024_URL | const | 21 | yes |
| build_jp_morgan_securities.py | P3_ARCHIVE_URL | const | 38 | n/a |
| build_kexim_bank_uk.py | NOT_DISCLOSED_NOTE, PILLAR3_ACCESS_NOTE, p3_sources | const/func | 76/182/206 | n/a |
| build_melli_bank.py | AR2022_URL | const | 14 | yes |
| build_metro_bank.py | INTERIM_HEADERS | const | — | n/a |
| build_national_westminster_bank.py | CH_COMPANY_URL | const | 79 | n/a |
| build_northern_bank.py | FY2021_REPORT_URL | const | 27 | yes |
| build_onesavings.py | AR_2022_URL | const | 14 | yes |
| build_punjab_national_bank_international.py | stock_rows | func | 513 | n/a |
| build_redwood_bank.py | CH_URL | const | 14 | n/a |
| build_santander_financial_services.py | AR2023_SANT, AR2022_SANT, AR2021_SANT | const | 22-24 | yes |
| build_starling.py | AR22/AR20/AR19/AR18/AR17_URL, p3_sources | const/func | 20-27/92 | yes |
| build_state_bank_of_india_uk.py | FS2024, FS2022 | const | 31/33 | yes |
| build_streambank.py | AR2026_SITE_URL | const | 31 | yes |
| build_tandem.py | AR2024_URL | const | 11 | yes |
| build_tsb.py | AR24_URL | const | 12 | yes |
| build_union_bancaire_privee_uk.py | AR2003..AR2007_URL (5) | const | 39-43 | yes |
| build_vanquis.py | AR2015_URL, AR2017_URL, AR2019_URL | const | 23/25/27 | yes |
| build_vida.py | rwa_not_disclosed_note | func | 317 | n/a |
| build_weatherbys.py | CH_URL, PRA_URL | const | 46/47 | n/a |
| build_zenith.py | opening_cash, pct | func | 135/141 | n/a |

---

## B. Triage and fixes

### The dominant result: most orphans are harmless duplicates, not citation gaps

The decisive test is not "is the constant referenced?" but "does its **value**
reach a workbook cell?" Many citations hardcode the same URL inline rather than
interpolating the constant, so the constant is dead code while the URL still
reaches the reader. Splitting the 79 constants that way:

- **~33 are DUPLICATES** — the identical URL (or the same document via a
  different host/path) already appears inline in a citation string. No
  reader-visible defect; dead code only.
- **~30 never reach any citation.** Of these the large majority are
  *deliberate* — superseded editions, out-of-window years, dead sources kept
  as a provenance record, or navigational index pages.
- **A small number are the real defect.** They are listed below.

### B1. REAL DEFECT — figures delivered with no citation at all

#### build_arbuthnot_latham.py — `AR2017_URL` (**REPORT, DO NOT FIX — figure defect found**)

`YEARS` includes `FY2017`. At the bottom of the script (L591-604) four FY2017
figures are written **directly into cells after the sheets were built**,
bypassing `sources_text` entirely:

    Balance Sheet:  Loans and advances to customers 1,049,269 ; Total assets 1,853,232
    Profit & Loss:  Operating income from banking activities 54,616 ; Profit before tax 6,971

`AR2017_URL` (the ABG Report & Accounts 2017) is defined at L10 and never
referenced, so the FY2017 column reaches the client **entirely uncited** — the
provenance lives only in a Python comment.

Wiring the citation in was attempted and **revealed a figure defect instead.**
Source verified (`%PDF-1.6`, 122pp, HTTP 200, `application/pdf`). The report's
own segment reconciliation (PDF p.14, "31 December 2017") reads:

| | Arbuthnot Latham & Co. | Retail Banking Associate | Group Centre | Arbuthnot Banking Group |
|---|---|---|---|---|
| Profit before tax | **10,959** | 4,437 | (8,425) | **6,971** |

and the two Summarised Balance Sheets (PDF p.15 = ABG Group, PDF p.16 =
Arbuthnot Latham) read:

| | Arbuthnot Latham (p.16) | ABG Group (p.15) | script wrote |
|---|---|---|---|
| Total assets | **1,783,675** | **1,853,232** | 1,853,232 |
| Operating income | **54,925** | **54,616** | 54,616 |
| Profit before tax | **10,959** | **6,971** | 6,971 |
| Loans and advances | 1,049,269 | 1,049,269 | 1,049,269 (agrees) |

**Three of the four FY2017 figures are Arbuthnot Banking Group PLC consolidated
figures sitting in a workbook whose own `ENTITY_NOTE` states the workbook covers
Arbuthnot Latham & Co., Limited and explicitly warns the two bases must not be
blended.** Wiring `AR2017_URL` in would have made the workbook *assert* an
ABG-Group provenance for a Bank-basis column. Per the task's rule (change no
figure; report when the source cannot support it) this is left untouched and
escalated. The missing citation is what hid the basis error.

#### build_bank_of_beirut_uk.py — `AR2017_URL` (**FIXED**)

Identical shape, clean outcome. `YEARS` includes `FY2017`; L504-560 writes ~45
FY2017 figures into Balance Sheet, Profit & Loss and Cash Flow Statement after
the sheets are built. `AR2017_URL` defined L18, never referenced — so three
sheets carried a fully-populated FY2017 column with **no FY2017 line in any
source citation**.

Source verified (`%PDF-1.5`, 31pp, HTTP 200, `application/pdf`; 2-up spreads,
primary statements on PDF pp.12-14 = printed pp.23-27 as the script's comment
claims). Figures confirmed against the document: Total assets 520,774,100;
Total liabilities 424,170; Total equity 96,604; Loans and advances 178,336,200
(script stores £'000, matching its own stated rounding). Same entity, same
basis — no figure issue. Citation wired in.

#### build_starling.py — `AR17_URL`, `AR18_URL`, `AR19_URL` (**REPORT, DO NOT FIX — figure defect found**)

Third instance of the same shape, and the one that most resembles Rathbones.
`ENTITY_NOTE` (L55-57) **does** reach the workbook and states:

> "FY2020-FY2017 are covered by Starling's official investor archive: FY2020/FY2019
> in the 2019-21 report, FY2018 in the 2017-18 report, and FY2017 in the 2016-17 report."

The claim reaches the client; the three URL constants that would support it
(`AR17_URL`, `AR18_URL`, `AR19_URL`, L25-27) are orphaned. So the reader is told
which documents were used but given no link and no page — thinner than the
project's stated convention ("names the exact document, page, and table, plus
the source URL"). FY2017/FY2018 figures are merged into `balance_sheet_rows`
at L220-237 before the sheet is built, so they do flow through
`STATEMENTS_SOURCES`; only the URLs are missing.

URL verification:

| constant | result |
|---|---|
| `AR18_URL` 2017-18 report | HTTP 200, `%PDF`, 55pp, title "Starling Bank - Annual Report - 2017-18", "Year Ended 30 November 2018" — **verified** |
| `AR17_URL` 2016-17 report | HTTP 200, `%PDF`, 102pp, title "Starling Bank • Annual Report 2017" — **verified** |
| `AR19_URL` `...-2019-18.pdf` | **HTTP 403 — BLOCKED, an unknown, not an absence.** Not wired in. |
| `AR20_URL` | byte-identical value to `AR21_URL` (already cited) — harmless duplicate |

Chasing the citation again surfaced a **figure defect**. The 2017-18 Annual
Report's Group balance sheet (PDF p.25) reads:

| line | FY2018 (report) | FY2017 (report) | script has for FY2018 |
|---|---|---|---|
| Loans and Advances to Banks | **187,008** | 37,544 | **37,544** |
| Loans and Advances to Customers | 8,698 | 804 | 8,698 ✓ |
| Total Assets | 234,669 | 53,277 | 234,669 ✓ |
| Customer Deposits | 202,323 | 18,083 | 202,323 ✓ |
| Total Liabilities | 206,670 | 20,559 | 206,670 ✓ |
| Total Equity | 27,999 | 32,718 | 27,999 ✓ |

`_OLD_BS["FY2018"]["Loans and advances to banks"] = 37544` is the **FY2017
comparative column value carried into the FY2018 row**. The arithmetic confirms
it: 187,008 + 18,039 + 8,698 + 20,924 = 234,669 exactly, whereas the script's
37,544 leaves the FY2018 column £149.5m short of its own stated total. Every
other FY2017 and FY2018 figure checks out, and the Group (not Company) column
was correctly used.

**Deliberately not fixed, and the citation deliberately not wired in.** Adding
the URL while 37,544 stands would make the workbook cite a document that
contradicts its own cell — a verifiable false claim, worse than the current
silent gap. The citation fix should land **together with** the figure
correction, in one change, by someone authorised to touch figures.

### B2. STALE / CONTRADICTED NOTES — report for deletion, must NOT be wired in

These are notes that were correctly unwired because a later pass disproved
them. Wiring them in would put a known-false claim in front of the client.

- **build_fidbank_uk.py `CAPITAL_RATIO_NOTE`** — asserts the FY2025 Financial
  Highlights table states 21.46%. The Total Capital Ratio sheet's *live* note
  (L505-512) says 21.46% "appears NOWHERE in the FY2025 Annual Report and was a
  transcription error", and the correct figure is 21.99%/21.64%. The orphan is
  a superseded, now-incorrect draft. Recommend deletion.
- **build_icbc_london.py `P3_23_KM1_NOTE`** — a parenthetical fragment
  asserting "the OV1 category-level RWA breakdown table is not available for
  FY2023 or earlier". The live RWA Breakdown citation (L291-312) says that
  exact claim "was wrong", and FY2021/FY2022/FY2023 OV1 tables are now
  transcribed. Superseded. Recommend deletion.
- **build_kexim_bank_uk.py `NOT_DISCLOSED_NOTE`, `PILLAR3_ACCESS_NOTE`,
  `p3_sources()`** — all three describe a Pillar 3 document that "could not be
  reached". Their own text records the situation as "RESOLVED 2026-09-15" /
  "FULLY RESOLVED", and the live `P3_SOURCES` / `P3_EARLIER_EDITIONS_SOURCES`
  (wired into every Pillar 3 sheet) supersede them. Recommend deletion.
- **build_icbc_standard_bank.py `AR_STATEMENT_SOURCES_2015_2020`** — a full
  FY2015-FY2020 citation block. Superseded: `BALANCE_SHEET_SOURCES` and
  `INCOME_STATEMENT_SOURCES` already enumerate every one of those years with
  the same URLs, and the "FY2015 is the entity's genuine historical floor"
  paragraph it uniquely carries is separately present in the live Statement of
  Changes in Equity and Overview citations (L326-328, L686). Nothing is lost.
  Recommend deletion.

### B3. Reader-visible wart — script variable names leaking into client citations

Not an orphan defect, but found alongside and worth a human read. Several
delivered citation cells name Python constants the reader cannot see:

- **build_allica.py** — `HISTORICAL_DEPTH_NOTE` is orphaned, yet **five** live
  citations (L65, L111, L194, L251, L693) tell the reader "See
  HISTORICAL_DEPTH_NOTE in this script for why FY2019/FY2018 are not
  included." The workbook points the client at a note that is not in the
  workbook. Left unfixed because the author's wording ("in this script") reads
  as a deliberate maintainer-facing pointer, and wiring the 20-line note into
  five sheets would materially change five citations. Needs a human decision.
- **build_bank_of_china_uk.py** — `AR2010_SCAN_NOTE` / `AR2014_SCAN_NOTE` are
  live and reach the workbook, and their text literally begins "AR2010_URL
  note: ...". `AR2010_URL` / `AR2014_URL` are themselves orphaned *deliberately*
  (both PDFs are untextable scans; the FY2011/FY2015 comparative columns are
  used instead, which the note explains). The provenance logic is sound; only
  the variable-name phrasing leaks. Cosmetic.

### B4. Deliberate leftovers — report only, no action

- **Out-of-window editions** (correctly unused): `build_castle_trust.py`
  `P3_2020_URL` (FY2020 outside the FY2021-FY2025 window; comment explains it
  is recorded as corroboration), `build_clearbank.py` `AR2016_URL` (FY2016
  pre-operational stub, excluded by an explicit floor-verification note).
- **Superseded alternates** where the document IS cited from another host or
  another year's comparative column: `build_santander_financial_services.py`
  (`AR2021/2022/2023_SANT` — cited via `assets.santandermedia.com`),
  `build_gatehouse.py` `AR2022_URL` and `build_onesavings.py` `AR_2022_URL`
  (FY2022 cited from the FY2023 report's comparative column),
  `build_starling.py` `AR20_URL`, `build_streambank.py` `AR2026_SITE_URL`.
- **Navigational index pages, not document citations** (wiring them in would
  add a link that is not the document cited): `CH_URL` /
  `CH_OVERVIEW_URL` / `CH_COMPANY_URL` in afin, alrayan, blme, redwood,
  weatherbys, bank_of_beirut, aib_uk, natwest; `build_tandem.py` `AR2024_URL`
  (filing-history index); `build_cynergy_bank.py` `P3_INDEX_URL`;
  `build_jp_morgan_securities.py` `P3_ARCHIVE_URL`; `build_weatherbys.py`
  `PRA_URL`.
- **build_db_uk_bank.py `P3_2023/2024/2025_URL`** — three Pillar 3 URLs found
  2026-09-15. The script itself carries a live note: "PARTIALLY OUT OF DATE,
  flagged 2026-09-15, NOT yet acted on", because wiring them in contradicts the
  workbook's standing claim that "no dedicated Pillar 3 document is published by
  this entity" and would change figures. Explicitly a known-open item belonging
  to another workstream. **Not touched.**
- **Redundant aliases**: `build_northern_bank.py` `FY2021_REPORT_URL`
  (= `AR_URLS["FY2021"]`, which is itself cited),
  `build_barclays_bank_plc.py`, `build_birmingham_bank.py`,
  `build_aldermore.py`, `build_ghana_international_bank.py`,
  `build_handelsbanken.py` `AA2019_URL`, `build_icici_bank_uk.py`,
  `build_jp_morgan_europe.py`, `build_cynergy_bank.py` CDN pair.

### B5. Dead helper functions (check (c)) — no citation impact

`build_access_bank.py convert_bs_rows`, `build_punjab_national_bank_international.py
stock_rows`, `build_vida.py rwa_not_disclosed_note`, `build_zenith.py
opening_cash` / `pct` (locked), `build_starling.py p3_sources`,
`build_kexim_bank_uk.py p3_sources`. Also `INTERIM_HEADERS` in aldermore,
coop_bank and metro_bank (a header list, not a citation). All are unreferenced
dead code; none changes what any workbook says. `build_vida.py
rwa_not_disclosed_note` is the only one worth a look — it is a fully-written
"no OV1 table exists" explanation that is never emitted; the RWA Breakdown
sheet should be checked for whether it says anything equivalent.

### B6. Deferred — locked scripts (findings only, NOT edited)

| script | orphan(s) | note |
|---|---|---|
| build_atom_bank.py | `P3_FY24_URL` | **value reaches no citation** — worth a look in the later pass |
| build_atom_bank.py | `AR17_URL`, `AR24_URL` | duplicates, harmless |
| build_hsbc_uk_bank_plc.py | `AR2022_URL` | **value reaches no citation** — worth a look |
| build_melli_bank.py | `AR2022_URL` | **value reaches no citation** — worth a look |
| build_tsb.py | `AR24_URL` | **value reaches no citation** — worth a look |
| build_hampden_co.py | `P3_2022_URL` | f-string over `P3_HOST`; check whether FY2022 P3 is cited |
| build_union_bancaire_privee_uk.py | `AR2003`-`AR2007_URL` | "supplied locally" placeholders, not URLs |
| build_vanquis.py | `AR2015/2017/2019_URL` | CH filing URLs |
| build_aib_uk.py, build_firstbank_uk.py, build_bank_of_africa_uk.py, build_national_westminster_bank.py | various | duplicates, harmless |
| build_zenith.py | `opening_cash`, `pct` | dead helpers |

No orphans found in the other locked scripts (chetwood, credit_suisse, fce,
methodist_chapel_aid, recognise, smbc, united_national, unity_trust,
gulf_international_bank_uk, arab_bank_europe, united_trust_bank,
itau_bba_international, philippine_national_bank_europe).


---

## C. Outcome

**Sweep complete.** 86 orphaned definitions found across 49 of 145 scripts
(79 constants + 7 functions). Orphan count after this pass: 85.

### Fixed (1)

- `scripts/build_bank_of_beirut_uk.py` — `AR2017_URL` wired into
  `STATEMENT_SOURCES` and `CASH_FLOW_SOURCES`. Rebuilt with
  `python3 scripts/build_bank_of_beirut_uk.py`; **18 sheets before and after**,
  citation confirmed present in the Balance Sheet, Profit & Loss and Cash Flow
  Statement source cells. Source verified before wiring (HTTP 200,
  `application/pdf`, `%PDF-1.5`, 31pp, not Wayback-truncated) and all figures
  confirmed against it.

### Reported, deliberately not fixed (3 high-value + the B2/B3/B4 lists)

- `build_arbuthnot_latham.py` — uncited FY2017 column; **3 of 4 figures are
  Arbuthnot Banking Group PLC figures in a Bank-basis workbook.** Needs a
  figure correction, not a citation.
- `build_starling.py` — FY2017/FY2018 documents named without URLs; **FY2018
  "Loans and advances to banks" is the FY2017 comparative (37,544 vs 187,008).**
  `AR19_URL` additionally returns **HTTP 403 = BLOCKED**, an unknown.
- `build_db_uk_bank.py` — 3 Pillar 3 URLs the script itself marks "NOT yet
  acted on"; belongs to another workstream.

### Judgement: is this defect class widespread?

**No — it is rare, but it is a reliable marker of something worse.**

Only 3 scripts of 145 (2%) had a citation that genuinely fails to reach the
workbook, and a further 4 carry stale notes that are correctly unwired. The
other ~75 orphans are dead code with no reader-visible effect: URLs duplicated
inline in the citation, out-of-window editions, alternate hosts, or
navigational index pages. The raw scan badly overstates the problem, and the
discriminating test is **"does the constant's value reach a workbook cell?"**,
not "is the constant referenced?".

The finding that matters is *where* the real instances clustered. All three —
Arbuthnot, Beirut, Starling — share one structure: **a historical extension
column bolted on after the main sheets were built**, via a post-hoc `_fy17` /
`_OLD_BS` dict. Every one of them skipped the citation plumbing, because that
plumbing sits in a `*_SOURCES` constant defined far above the append. And in
**two of the three**, the missing citation was hiding a wrong figure: a
wrong-entity column in Arbuthnot, a mis-copied comparative in Starling. Nobody
had reconciled those columns against the source, precisely because no citation
pointed at one.

So the recommendation is not "sweep for orphaned constants again" — that hit
rate is 2%. It is: **audit every post-hoc column-extension block in the
corpus.** They are cheap to find (a `for` loop writing into `bw.wb[...]` or
mutating `*_rows` after the row list is defined) and they bypass both the
citation convention and, evidently, the figure-checking that the normal path
gets. A grep for that pattern across the remaining ~142 scripts is the natural
follow-up, and it should be done by someone authorised to correct figures.

### Not done / out of scope

- The ~25 locked scripts were scanned and reported but **not edited** (see B6).
  Four of them (`atom`, `hsbc_uk`, `melli`, `tsb`) have an orphan whose value
  reaches no citation and deserve a look in the later pass.
- `refresh_all.py` not run; test suite not run; nothing committed.
- Only `scripts/build_bank_of_beirut_uk.py` and
  `banks/BANK OF BEIRUT UK FINANCIALS.xlsx` were modified by this pass. All
  other modified files in the working tree belong to concurrent agents.
