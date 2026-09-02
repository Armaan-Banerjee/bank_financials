# Integrated Build Effort Review

**Last updated 2026-09-02.** This document synthesizes the whole project across
both of its phases and both of the concurrent sessions ("Claude" and "Codex")
that built it — something neither `Build Effort Review.md` (bank-build phase,
this session's own timing/token data) nor `Build Effort Review Codex.md`
(Codex's own execution records) captures alone, since each stays within its own
session's scope and `Build Effort Review.md`'s brief "Insights-map work"
section only covers the pipeline's first few days. Those two files remain the
detailed source of record for per-bank timing/token figures and Codex's raw
execution logs respectively — read them for that level of detail. This
document is the cross-phase narrative and current state.

## Project shape

Two sequential maps, both using the same local-markdown wayfinder tracker
convention (no git repo, manual session cadence, two models working
concurrently with a claim-before-work discipline):

1. **`wayfinder/map.md`** — the bank-workbook-build map. **Closed.** Produced
   the 145 Excel workbooks in `banks/`.
2. **`wayfinder/insights/map.md`** — the insights/clustering/deliverable map.
   **Effectively closed** — 36 of 37 `IN-*` tickets closed; one (IN-013,
   "shared SQLite analysis-query layer") still shows `in-progress`, claimed by
   Codex since 2026-08-30, and appears stale (its own scope — comparability,
   trend, outlier, and parent-group query helpers — looks superseded by
   `analysis_queries.py`, which IN-009/IN-013's downstream tickets already use;
   worth a status check next session rather than assuming abandoned work).

## Phase 1 — Bank workbook builds (closed)

**Final count: 145 of 148 banks in `Banks List 2608.xlsx` built** — 126 full
13-sheet workbooks (Cash Flow Statement + 11 Pillar 3 metrics), 19 Pillar-3-only
(no cash flow — FRS 101/102 exemption), plus a further subset later expanded to
14 sheets with an Interim Pillar 3 tab. **3 banks genuinely skipped**, each
verified against primary sources before being confirmed as a permanent skip
rather than a time-boxed guess (full detail in `Build Effort Review.md`'s "The
3 skipped banks" section):

1. **VTB Capital plc** — under UK sanctions and in insolvency administration
   since December 2022, with no accounts filed since. Not a data-availability
   problem: the entity is not a going concern.
2. **Bank Of Baroda (UK) Limited** — a permanent FRS 102 §7.1B cash-flow
   exemption (wholly-owned subsidiary), plus zero quantitative Pillar 3 data
   anywhere in either Annual Report reviewed (purely narrative capital
   sections, no fallback to build a Pillar-3-only workbook from). In a
   Solvent Wind Down since FY2024.
3. **Revolut Bank UK Ltd** (FRN 981170, Companies House 12871051) — easy to
   mistake for the well-known Revolut consumer app, but that's a *different
   legal entity* (Revolut Ltd, company 08804411, incorporated 2013, an
   e-money institution and out of scope for this project, which only covers
   PRA-authorised banks). Revolut Bank UK Ltd is separate and much younger:
   incorporated September 2020, granted its UK banking licence only in July
   2024, and renamed to its current name as recently as March 2026. Its
   FY2023–FY2025 accounts all claim the FRS 101 IAS 7 cash-flow exemption
   (permanent — its parent, Revolut Group Holdings Ltd, files the
   consolidated group cash-flow statement instead), FY2022 has no cash-flow
   statement at all, and the only Pillar 3 disclosure found anywhere is
   Revolut Group Holdings Ltd's own group-level one, not the standalone UK
   banking entity's. Reassessed once already at a prior user's request with
   a shorter FY2022–FY2025 window specifically to rule out the missing
   FY2021 filing as the deciding factor — it wasn't; the double blocker held
   regardless. Re-verified against live Companies House/FCA data on
   2026-09-01 and still holds.

Built across two concurrent, independently-timed tracks:

- **This session** (WF-001–WF-015, plus later revisit/fix passes) — every bank
  run as a tracked background agent from Santander UK onward, so real
  duration/tool-call/token data exists for 82 full builds, 9 self-skips, and 8
  Pillar-3-only builds. **Full builds: mean 16m 23s, 66.6 tool calls, 458,696
  tokens.** Pillar-3-only builds: mean 12m 23s, 51.5 tool calls, 378,905
  tokens. Rough cost bound (Sonnet 5 list pricing, prompt-cache-favorable):
  **~$1–7 per bank.**
- **Codex session** (WF-016–WF-025, the interim-Pillar-3 rollout, a later
  revisit sweep, and final-audit fix passes) — its tool interface never
  exposed per-bank duration/token metadata, so its own convention (followed
  consistently, no invented figures) records only approximate total
  wall-clock windows per 5-bank batch: typically 6–18 minutes per batch,
  30 minutes for the one-off wide-interim-layout conversion across 13
  workbooks.

**Failure modes catalogued and their fixes** (from `Build Effort Review.md`'s
"Observations" and difficulty-ranking notes — genuinely worth keeping as
institutional memory, not just a build log):

- A four-way taxonomy of what a session-limit cutoff can leave behind:
  nothing at all, a complete-but-unexecuted script (Coutts & Company —
  recovered for free by just running it), a fix applied but never rebuilt, or
  a real bug needing a dedicated fix fork (Charter Court — a cutoff fork's own
  "I'm building now" self-report was flatly wrong about what was actually on
  disk). Lesson generalized explicitly: never trust a terminated agent's
  self-reported state over what's actually on disk.
- Stream stalls (distinct from hitting the usage limit) resumed cleanly via
  `SendMessage` rather than restarted, preserving completed research
  (Barclays Bank Plc, Brown Shipley).
- A ~2x reconciliation gap at ClearBank that looked like a real data error but
  was a false alarm (an unbolded-subtotal-row bug, same class fixed earlier at
  Bank of Ireland UK) — even a prior fork's own diagnosis of its own problem
  needs independent verification.
- The FX opening-balance spot-rate bug recurred three times independently
  (Zenith Bank UK, Union Bank of India UK, FidBank UK) before being promoted
  to a standing checklist item for every FX-converted build.
- Two shared-library bugs found and fixed: `bank_scaffold.py`'s 20-color
  palette silently collided once the project passed 20 banks; `bank_workbook.py`'s
  `add_overview_sheet()` broke silently on `ratios=[]` (unlike the already-safe
  `cash_flow_totals=[]` case).

**Data-quality sweeps** (the bank-build phase's own version of what the
insights phase later repeated as automated audits): a full sanity-check pass
across all 47 then-built workbooks (2026-08-27) found and fixed 3 real
transcription/structural bugs (Bank Mandiri Europe and Bank Saderat's
scrambled sheet order, Starling's genuine FY2026 cash-flow transcription
error, Chetwood's 5 Company-vs-Group column mixups). A later full sheet-order
regression confirmed all 145 built workbooks match the standard order (a third
scrambled-order instance, Brown Shipley, was caught and fixed in the process).

**Difficulty ranking** (146 ranked positions, worst-to-best, full detail in
`Build Effort Review.md`): the top of the ranking is dominated by genuine
structural/legal blockers (VTB Capital's sanctions status; Bank Of Baroda
UK/Revolut's double blockers) and a tier of banks originally skipped for
tooling-access reasons (site 403s, Wayback outages, exhausted search quota) —
GB Bank, J.P. Morgan Europe, ICICI Bank UK, United Trust Bank, TD Bank Europe,
Citibank UK, Union Bancaire Privée UK, Philippine National Bank Europe,
Standard Chartered, THIS BANK, Afin Bank — that were **all successfully
recovered** on a later revisit once tooling budget reset, confirming the
project's own repeated lesson that a tooling-driven skip is worth a second
pass, not a permanent write-off. **Bank of Africa UK** is flagged as the
single most effort-intensive successful build (longest wall-clock build in the
series, heaviest OCR load, a genuine three-way restatement corroborated by an
auditor's note referencing a regulatory investigation) and the one build most
worth an independent double-check if the client ever questions a figure.

## Phase 2 — Insights pipeline (mostly closed)

`wayfinder/insights/map.md`'s destination: turn the 145 workbooks into
statistical peer-group clusterings, extended cross-bank trend findings, and a
refreshable client deliverable (HTML + PDF), backed by `research/insights.db`
as the single source of truth. Grouped by theme (see the map's own ticket
index for the full 37-ticket list):

**Foundation** — IN-001 (reusable metrics-extraction tool) → IN-007/IN-008
(SQLite database, migrated as the source of truth from the earlier flat
CSV/markdown files) → IN-002 (parent-group mapping) → IN-003 (statistical
clustering pass, winsorized/robust-scaled to resist known extreme-outlier
disclosures).

**Core analysis** — IN-004 (extended the original 4-finding, 29-bank trend
analysis to all 145 banks) → IN-009 (the central core-ratio
comparability/trend/outlier engine most later tickets build on) → IN-010
(parent-group dispersion/agreement) → IN-012 (absolute capital/RWA, size-aware
analysis) → IN-016 (distributional benchmarks, ranks, uncertainty context) →
IN-017 (source lineage and data-quality monitoring) → IN-020 (versioned
regulatory benchmark/threshold context) → IN-021 (regulatory headroom
trajectory / early-warning screening) → IN-022 (CET1 ratio movement
decomposition) → IN-023/IN-024/IN-025 (robust distribution visuals, persistent
trajectories and rank mobility, source-quality and disclosure-coverage views —
a coordinated 4-ticket visualization expansion opened together on 2026-08-30).

**Deliverable integration** — IN-005 and its 10 lettered follow-ups
(IN-005a–j: visual hierarchy, selectable trends, parent-group drill-down,
metric-guide polish) built the original single-file HTML prototype → IN-006
locked the delivery format and produced the fixed-layout PDF companion →
IN-011 and IN-014 folded IN-009/IN-010/IN-012's analysis into both
deliverables on a shared payload (the pattern every later analysis ticket
followed, so HTML and PDF can never silently report different numbers for the
same data) → **IN-026** (2026-09-01... closed) reworked the whole HTML page
into an actual dashboard shell: sticky sidebar navigation, executive KPI
cards, consistent card/badge/spacing system, all derived from the generated
payload rather than hand-duplicated → **IN-027** (opened by this session
2026-09-01 after reviewing IN-026's result and suggesting further additions;
closed the same day by Codex) added the cross-cutting watchlist/alerts panel,
full section navigation with stable anchors, a global bank search, a
bank-level drill-through panel, trend sparklines, and a data-freshness badge —
the PDF gained the watchlist-count and freshness-line equivalents.

**Enrichment and PowerBI groundwork** — IN-015 (period-aware interim/quarterly
disclosure enrichment, kept deliberately separate from the annual analysis)
→ IN-018 (PowerBI-ready star schema/semantic-model contract) → IN-019
(interactive PowerBI exploration experience) — real PowerBI *deployment*
stays explicitly out of scope ("a strong maybe for later," never built; only
the export contract exists).

**Data-correctness audits** (the insights phase's own recurring
quality-control thread, worth calling out as its own line of work since it
found real, user-impacting bugs three separate times):

1. **2026-08-30** — user spotted Barclays Bank Plc's leverage ratio listed as
   56465%. Root cause: `in009_analysis.py`'s row-selection fallback did a
   plain alphabetical sort of row labels when a bank's label wasn't in a
   small curated dict, so an absolute £m amount row occasionally outranked
   the true percentage row. Fixed with a shared `_is_percent_value()` helper
   and a `PERCENT_ONLY_SHEETS` guard; regression tests added.
2. **2026-08-30 (same day, follow-up)** — user reported still seeing 353873%.
   A *second*, independent instance of the same bug class in
   `in016_distribution.py`, which had its own unfixed row-selection logic
   never reconciled with the first fix. Fixed the same way; a syntax error in
   concurrently-landed Codex code (`in011_deliverables.py`) was also fixed
   opportunistically since it was blocking verification.
3. **2026-09-01** — user asked for a final, thorough, subagent-parallelized
   review of all bank data and every deliverable for correctness and
   cross-consistency. Five parallel read-only audits (workbook↔DB extraction,
   cross-payload consistency, HTML↔PDF consistency, full 145-bank anomaly
   sweep, pipeline health) found the pipeline in very good shape overall —
   219 tests passing at the time, 0 mismatches in workbook→DB extraction, 0
   mismatches in HTML↔PDF headline figures, all prior fixes confirmed still
   holding — but surfaced **2 further bugs**, a third and fourth instance of
   the identical root cause: `in016_distribution.py`'s independently
   duplicated selection logic, this time picking the wrong one of two
   *both-valid* percentage variants (21 leverage/MREL cells) and
   inconsistently choosing between valid row definitions for the same
   absolute metric across years (Kingdom Bank Limited's Total Capital).
   Logged as **IN-028**; fixed the same day by unifying `in016`'s selection
   paths onto `in009`'s canonical selector rather than patching a third
   independent implementation — the fix this ticket asked for explicitly,
   given the pattern's recurrence. Verified: 0 mismatches on a full 145-bank
   re-sweep, 222 tests passing, clean live refresh.

   **The recurring lesson across all three findings**: `in016_distribution.py`
   kept reimplementing "pick one row per bank/period" instead of calling
   `in009_analysis.py`'s selector, exactly the duplication
   `scripts/insights/README.md` already warned against. Worth treating as a
   standing review question for any *future* script in this pipeline: does it
   call the canonical selector, or does it quietly reimplement it.

## Current state

- **222 tests passing** (`python3 -m unittest discover -s scripts/insights -p 'test*.py'`),
  clean end-to-end `refresh_all.py`, byte-identical generated exports on a
  no-op refresh.
- **145/148 banks built**, 12,846 `annual_metrics` rows in `research/insights.db`.
- **Both client deliverables current**: `wayfinder/insights/deliverable/uk_bank_insights.html`
  (dashboard-style, watchlist/nav/drill-through/sparklines) and the matching
  PDF companion, both sourced from the same computed payloads.
- **36 of 37 insights tickets closed**; IN-013 is the one open item, likely
  stale rather than blocking — worth a status check.
- **Known minor doc drift, fixed as part of IN-028**: `scripts/insights/README.md`'s
  file table and pipeline diagram now match what's actually on disk and in
  `refresh_all.py`'s STEPS.

## Sources

- `Build Effort Review.md` — this session's own per-bank timing/token data,
  full 146-position difficulty ranking, tooling-bug catalogue.
- `Build Effort Review Codex.md` — Codex's own execution records, batch by
  batch, for WF-016 onward plus its insights-phase timing notes.
- `wayfinder/map.md` / `wayfinder/insights/map.md` — the two ticket-tracker
  maps; each ticket's own file holds its full scope and resolution record.
- `scripts/insights/README.md` — the insights pipeline's file-by-file
  architecture reference.
