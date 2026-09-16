# Post-hoc column-extension audit — RESUME checkpoint

Started 2026-09-16. Follow-up to `research/RESUME_orphaned_citations.md`, whose
conclusion was: don't re-run the orphan sweep (2% hit rate), **audit every
post-hoc column-extension block instead**, because that is where the figure
bugs live.

Authorised to correct figures where a primary document proves the correction.

## Method

Two AST passes over all 145 `scripts/build_*.py`:

1. **Mutation-after-consumption**: for every name passed to an `add_*_sheet(...)`
   call, flag any `Subscript` assignment or `.update/.append/.insert/.extend`
   on that name at a line *after* the call. Plus every `bw.wb[...]` subscript
   (a direct write into an already-built sheet).
2. **Historical-year-only dicts**: module-level dict literals whose keys are all
   FY-year strings and which are disjoint from / older than the script's `YEARS`.

Pass 1 is the discriminating one. Pass 2 mostly returns `INTERIM_*` dicts, which
are a different (deliberate) feature — quarterly/half-year disclosure matrices —
and not this defect class.

## The population: 9 candidate blocks, 6 of them the real shape

The real shape is a **historical extension column bolted on after the sheets
were built**, via a dict keyed by one old year, written through a boilerplate
`for _sheet, _values in _fy17.items(): _ws = bw.wb[_sheet] ...` loop.
**Four scripts carry a byte-for-byte copy of that same loop** — one author, one
shortcut, one systematic risk.

| # | script | block | cells | year | citation covers it? | status |
|---|---|---|---|---|---|---|
| 1 | build_arbuthnot_latham.py | `_fy17` L594-604 | 4 | FY2017 | **NO** (`AR2017_URL` orphaned) | **DEFECTIVE — fixing** |
| 2 | build_starling.py | `_OLD_BS` L~220-260 | ~14 | FY2017/FY2018 | partial (prose, no URL) | **DEFECTIVE — fixing** |
| 3 | build_gatehouse.py | `_FY2017` L~800-853 | ~30 (BS+P&L+CF) | FY2017 | YES (L48/L75/L158) | TO AUDIT |
| 4 | build_lloyds_bank.py | `_fy17` L590-602 | 5 | FY2017 | YES (L46) | TO AUDIT — **highest exposure** (Lloyds Bank plc; entity-vs-Group risk) |
| 5 | build_national_bank_of_egypt_uk.py | `_fy17` L742-753 | 5 | FY2017 | YES (L283 `FY2017_SOURCE_NOTE`, cross-confirmed) | TO AUDIT |
| 6 | build_bank_of_beirut_uk.py | FY2017 block L504-560 | ~45 | FY2017 | YES (fixed 2026-09-15 by the orphan sweep) | ALREADY VERIFIED CLEAN |

### Not this defect class (false positives, no figures touched)

| script | block | why not |
|---|---|---|
| build_aldermore.py | L1077-1092 `interim_ws` | cosmetic only — `delete_rows` of helper spacer rows + applying hyperlink styling to the Interim Pillar 3 sheet. Writes no values. |
| build_coop_bank.py | L2392-2400 `interim_ws` | identical cosmetic hyperlink/spacer fix-up. Writes no values. |
| build_rbc_europe.py | L438 `rows.append` | function-local `rows` inside `add_interim_pillar3_sheet()`; the name collision with a module-level `rows` is what tripped the scan. |

## Latent bug shared by all four copies of the boilerplate loop

    _labels = {str(_ws.cell(r, 1).value).strip(): r for r in range(4, _ws.max_row + 1)}

This dict **dedupes duplicate row labels to the LAST occurrence**. Balance
sheets routinely carry the same label twice (e.g. "Derivative financial
instruments" as both an asset and a liability). Any future extension using that
label would silently land in the wrong section. Not currently triggered by any
of the four blocks' actual key sets, but it is a trap. The durable fix is to
stop using the loop and merge historical years into the row dicts directly,
which also restores the citation plumbing.

## Findings so far

### 1. build_arbuthnot_latham.py — ENTITY-BASIS violation (CONFIRMED, worse than reported)

Workbook's declared basis (`STATEMENT_SOURCES_HEAD`, L98): "Arbuthnot Latham &
Co., Limited's own Consolidated financial statements (the Bank + its own
subsidiaries), as filed at Companies House".

The `_fy17` block took figures from the **Arbuthnot Banking Group PLC Report &
Accounts 2017** instead. Three sources are in play and must not be conflated:

- ABG Group consolidated (PDF p.15) — the parent. **Wrong entity.**
- ABG's "Arbuthnot Latham" segmental summary (PDF p.16) — right entity, but the
  report states it is *before consolidation adjustments* for intergroup
  activities and recharges. **Wrong basis.**
- **Arbuthnot Latham & Co., Ltd's own statutory consolidated accounts**, filed
  at Companies House, y/e 31 Dec 2017 — **the basis the workbook declares.**

The handover brief said "3 of 4 wrong, AL's own PBT is 10,959". Both refinements
are wrong: **all 4 are wrong**, and 10,959 is the *segmental* PBT, not the
statutory one. Statutory PBT is **9,477**.

| row | script had | source of that | correct (AL statutory) |
|---|---|---|---|
| Loans and advances to customers | 1,049,269 | ABG Group / segment | **1,060,769** |
| Total assets | 1,853,232 | ABG Group | **1,783,675** |
| Operating income from banking activities | 54,616 | ABG Group | **54,925** |
| Profit before tax | 6,971 | ABG Group | **9,477** |

Correct source: Companies House, company 00819519, "Group of companies' accounts
made up to 31 December 2017", filed 15 Jun 2018 —
`/company/00819519/filing-history/MzIwNzQ3NTM0M2FkaXF6a2N4/document?format=pdf&download=0`
(HTTP 200, `application/pdf`, `%PDF-1.1`, 95pp). Scanned PDF, no text layer;
OCR-located then **read visually at 300 dpi** from the rendered page.
Consolidated Statement of Comprehensive Income = PDF p.25 / printed p.22;
Consolidated Statement of Financial Position = PDF p.26 / printed p.23;
Consolidated Statement of Cash Flows = PDF p.30.

Also: the Overview sheet (a COPY) has **no** FY2017 values at all — the `_fy17`
block never wrote to it. Must be updated too.

### 2. build_starling.py — comparative column read as the current year

FY2018 "Loans and advances to banks" = 37,544 is the FY2017 comparative;
the report says 187,008. To be re-verified against the 2017-18 Annual Report
and the whole column swept for the same off-by-one-year error.
`AR19_URL` = HTTP 403 = BLOCKED, an unknown, not an absence.

## OUTCOME — audit complete, 2026-09-16

**6 real post-hoc blocks. 3 were defective, 2 were clean, 1 was already
verified clean by the previous pass. Zero unverifiable.**

| script | verdict | sheets before/after |
|---|---|---|
| build_arbuthnot_latham.py | **DEFECTIVE — fixed** (entity-basis violation, 4 cells) | 18/18 |
| build_starling.py | **DEFECTIVE — fixed** (comparative-as-current, 1 cell + 7 gaps) | 18/18 |
| build_gatehouse.py | **DEFECTIVE — fixed** (2 whole lines dropped; column did not add up) | 18/18 |
| build_lloyds_bank.py | CLEAN (all 5 figures verified); structure + Overview fixed | 19/19 |
| build_national_bank_of_egypt_uk.py | CLEAN (all 5 figures verified); no edit | — |
| build_bank_of_beirut_uk.py | CLEAN (verified by the previous pass) | — |

### Fixes applied

**1. build_arbuthnot_latham.py — entity-basis violation.** Worse than reported:
all 4 cells wrong, not 3, and the brief's proposed replacement PBT of 10,959 was
itself the wrong basis (segmental, pre-consolidation-adjustment). Replaced with
Arbuthnot Latham & Co., Limited's own statutory consolidated accounts filed at
Companies House:

| row | was | now |
|---|---|---|
| Loans and advances to customers | 1,049,269 | **1,060,769** |
| Total assets | 1,853,232 | **1,783,675** |
| Operating income from banking activities | 54,616 | **54,925** |
| Profit before tax | 6,971 | **9,477** |

The `_fy17` loop was deleted and FY2017 merged into the row dicts, so it now
flows through `STATEMENT_SOURCES_HEAD`. The whole FY2017 Balance Sheet and P&L
columns were transcribed (24 + 18 cells) and tie exactly. Overview (a copy)
updated. Cash Flow FY2017 deliberately left blank — the 2017 investing section
has lines this sheet has no rows for, so a partial column would not reconcile.

**2. build_starling.py — comparative column read as current year.** FY2018
"Loans and advances to banks" 37,544 → **187,008**. The tell was that FY2018 and
FY2017 carried the *identical* value. Every other FY2018/FY2017 cell re-checked
against the printed table; all correct, and the Group (not Company) columns were
used throughout. The FY2018 column was also completed: it had a single "Other
assets" of 20,924 silently absorbing PPE (616) and Intangibles (13,221) while
FY2017 showed them separately, and its equity/liability components were blank.
Both columns now tie exactly. AR18_URL and AR17_URL wired in; FY2017
cross-checked against its own 2016-17 report — agrees exactly, no restatement.

**3. build_gatehouse.py — two whole lines silently dropped.** Not the hunted
failure mode, but a real one found by the same audit. The FY2017 column omitted
"Due from financial institutions" 77,251 (27.5% of total assets — this ladder had
no row for it at all) and the derivative **liability** 506. The delivered column
therefore did not add up: assets summed to 203,275 against a printed Total assets
of 280,526. Added an FY2017-only row plus the derivative liability; both sections
now tie. Figures otherwise all verified against printed p.35.

**4. build_lloyds_bank.py — clean, structurally repaired.** All 5 figures
verified against the Lloyds Bank plc Annual Report 2017 (Group columns, not
Lloyds Banking Group plc and not the Company columns). Removed the `_fy17` loop,
merged FY2017 into the row dicts, completed the P&L column (which now ties), and
filled the Overview copy, which had been left entirely blank for FY2017.

### AR19_URL (Starling) — still BLOCKED

Retried 2026-09-16 with full browser headers + Referer via curl, and
independently via python urllib. Both return **HTTP 403** with a ~49KB
`text/html` bot-protection page. BLOCKED = unknown, not an absence. Not wired
in, not downgraded to dead. The script's existing comment is accurate; left as is.

### Blocks left structurally as-is

gatehouse, nbe_uk and bank_of_beirut still use the boilerplate loop. All three
are now verified correct and cited, so the citation-bypass risk is discharged;
converting them is larger surgery for no figure benefit. The duplicate-label
trap does not bite any of them (their key sets contain no duplicated caption).

### Does the "bolted-on column" structure predict figure bugs?

**Yes — far better than the orphan sweep did.** 3 of 6 blocks (50%) carried a
real figure defect, against the orphan sweep's 2% hit rate. Restricting to the
4 blocks that were *not* already audited, it is 3 of 4. The predictor is the
structure, not the missing citation: Gatehouse was fully cited with correct page
references and still had 27.5% of its FY2017 assets missing, because nobody ever
added the column up. What these blocks share is that they bypass the review the
normal path gets — the citation helper, and the habit of checking a column
against its own printed total.

**The cheapest test is arithmetic, not provenance.** Every one of the three
defects was visible from the column's own internal sums before any document was
opened: Starling's column was 149,464 short of its stated total, Gatehouse's
77,251 short, and Arbuthnot's four figures came from a statement whose own
segmental table contradicted them. A "does each historical column tie to its own
printed totals?" check would have caught all three.

## Rules observed

No refresh_all.py, no test suite, no commits. No locked script edited (none of
the 6 was on the locked list). Every edited script rebuilt; sheet count unchanged
in all four. Every URL verified for HTTP status, Content-Type and `%PDF` magic
bytes individually. The one scanned source (Arbuthnot's Companies House filing,
no text layer) was read visually from 300 dpi renders, not from OCR output.
