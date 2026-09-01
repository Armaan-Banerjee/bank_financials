---
label: wayfinder:map
title: "Bank financials insights & clustering map"
---

## Destination

A refreshable, in-house client deliverable that turns the 145 built bank
workbooks in `banks/` into: (1) statistical clusterings of UK banks — including
comparisons *within* the same parent regulatory group (e.g. HSBC's or Lloyds'
multiple separately-regulated UK entities) — and (2) trend findings, extending
`../../Cross-Bank Trends Analysis.md`'s existing 4 vetted findings from its
original 29-bank sample up to the full 145-bank dataset. The client cares about
clusterings and trends, not raw numbers — graphs are a priority in whatever the
final deliverable turns out to be. Real PowerBI integration is explicitly a
"strong maybe for later," not this map's target — see "Not yet specified."

Reached when: a normalized, re-runnable extraction tool exists in `scripts/`; a
bank→parent-group mapping exists; a real clustering pass has run and produced
documented peer groups; the trend analysis has been extended to all 145 banks
and folded in group-comparison findings; and a finished client deliverable
(format settled via IN-005a/IN-005b/IN-005c/IN-006, not pre-decided) has been produced.

## Notes

- **This map carries execution, not just decisions** — same deliberate override
  of wayfinder's plan-only default as `../map.md` (the bank-build map). Tickets
  produce the real tool, the real analysis, and the real deliverable.
- **Two models work this map concurrently — do not assume you're the only
  claimant.** Before starting any ticket: re-read its frontmatter fresh (don't
  trust a stale in-context copy), confirm `status` is still `open` and
  `claimed_by` is still empty, then immediately set `status: in-progress` and
  `claimed_by: <model/session identifier, e.g. "Claude — session starting
  2026-08-29 17:40">` before doing any other work. If you find a ticket already
  `in-progress` with a `claimed_by` set, do not touch it — pick a different
  unblocked ticket. This is a local-markdown tracker with no locking, so a
  race is possible if two sessions check and claim at nearly the same instant;
  if you discover after claiming that another session claimed the same ticket
  first, back off immediately and let their claim stand.
- **Dependencies are real edges, not a strict chain** (unlike the bank-build
  map's linear WF-001→WF-002→… numbering). Multiple tickets are unblocked from
  the start specifically so two models can work different tickets in parallel.
  Check each ticket's own `blocked_by` field — do not assume ticket order
  implies dependency order.
- **Tracker**: local-markdown, same mechanism as `../map.md` but in its own
  namespace to avoid confusion with the closed 145-bank build queue: this file
  plus one file per ticket under `wayfinder/insights/tickets/IN-NNN.md`. Ticket
  ids are `IN-001`, `IN-002`, etc. Frontmatter carries `status` (`blocked` /
  `open` / `in-progress` / `closed`), `blocked_by` (a list of ticket ids, or
  `null`), and `claimed_by` (empty until claimed, per the concurrency note
  above).
- **Source data**: `banks/*.xlsx`, one workbook per bank, 13 sheets (Cash Flow
  Statement + the 11 `PILLAR3_SHEET_NAMES` metrics from `scripts/bank_workbook.py`)
  or 14 where an "Interim Pillar 3" sheet was later added. 126 are full
  workbooks (have a populated Cash Flow Statement), 19 are Pillar-3-only (no
  cash flow — FRS 101/102 exemption applies); corrected 2026-08-29 by IN-001
  from a prior 119/26 figure in `Build Effort Review.md`, now fixed there
  too. 3 banks were never built (VTB Capital plc,
  Bank Of Baroda (UK) Limited, Revolut Bank UK Ltd) — exclude them, don't treat
  their absence as a data gap to chase.
- **All insights-pipeline scripts live in `scripts/insights/`** (moved there
  from the flat `scripts/` directory 2026-08-29, alongside the ~145
  bank-build scripts that stayed put — see `scripts/insights/README.md` for
  the full file-by-file map and `CODING_STANDARDS.md` for the rules this
  pipeline follows). Any path below is relative to that directory unless
  stated otherwise; `scripts/bank_workbook.py` is the one file this pipeline
  still imports from the parent `scripts/` directory.
- **`research/insights.db` is the source of truth for any ticket on this map
  from IN-008 onward (2026-08-29)** — not `research/bank_metrics.csv` or
  `research/bank_parent_groups.md`, which are now *generated exports* of the
  database, kept for a quick look or a spreadsheet hand-off. **Refresh with
  `python3 scripts/insights/refresh_all.py`** rather than running scripts
  individually — the dependency order matters and getting it wrong fails
  silently (see that script's own docstring). It runs: `extract_metrics.py`
  (writes `banks`/`annual_metrics` directly, workbooks → DB, then exports
  the CSV FROM the DB — byte-parity enforced, not re-derived) →
  `export_parent_group_tables.py` (imports the markdown's two mechanical
  tables into `parent_group_lookup`/`parent_group_edges`, then regenerates
  and splices those same two tables back into the file, leaving its
  hand-authored Conventions/Mermaid/Quality prose sections untouched) →
  `cluster_banks.py` → `analyze_trends.py` → `review_trend_selection.py` →
  both deliverable generators. Any new analysis ticket should read the
  database directly (`cluster_banks.py`/`analyze_trends.py` do, via the
  shared `build_insights_db.load_rows_from_db()`/`load_groups_from_db()`)
  rather than the CSV, unless there's a specific reason to want the
  flat-file view. See `scripts/insights/build_insights_db.py`'s module
  docstring for the full schema and refresh-ownership model, and
  IN-007/IN-008 for how this was built.
- **Start with annual data only.** Interim/quarterly sheets exist on only a
  subset of banks and are sparse/inconsistent — real enrichment material for
  later, not part of this map's first pass (see "Not yet specified").
- **Every workbook's own source-citation cells already document known data
  quirks** (FX conversion, Group-vs-entity basis, restatements, non-disclosure)
  — `Build Effort Review.md` has a fuller catalogue of these patterns. The
  extraction tool and every analysis ticket must treat these as real
  constraints (e.g. don't silently average a GBP bank with a Group-basis EUR
  bank as if they're on equal footing) rather than noise to smooth over.
- **Build on prior work, don't redo it**: `../../Cross-Bank Trends Analysis.md`
  (4 findings, already checked against known single-bank data quirks) is a
  foundation to extend, not a draft to discard. `../../Extra Pillar 3
  Disclosures.md` (cadence classification: quarterly/semi-annual/annual/
  irregular) is adjacent groundwork for the deferred interim-data enrichment,
  not something this map's first pass needs to consume directly.
- **Session cadence is manual**, same as the bank-build map — no cloud/cron
  automation. Partial completion is expected and fine: log progress in a
  ticket's own body and leave it `open`/`in-progress` rather than closing it
  prematurely or losing work to a session cutoff.

## Decisions so far

- [HTML deliverable was 131MB and effectively unusable (2026-09-01)](tickets/IN-034.md) —
  user reported the live dashboard "seems to have broken" (blank except the
  sidebar, search doing nothing). Root cause was NOT any of IN-033's edits
  (diff-tested, byte-identical) - the deliverable's embedded JSON payload was
  131.7MB, of which ~78MB was two independent bugs: `in023` embedding full
  wholesale copies of `in016`/`in017` (nothing reads the `in017` copy at all;
  the `in016` copy only for one sub-key), and `in016`/`in017["lineage"]`/
  `in025["trace"]` being large server-only aggregate/raw-observation data
  that no client-side JS ever reads but was embedded in full anyway. Fixed by
  de-duplicating `in023` and dropping/truncating the unused server-only data
  from the client payload right before JSON-serializing it (rendering the
  server-side HTML tables first, since they still need the full data).
  **131.7MB -> 11.1MB (91.5% smaller)**, nothing lost - full CSS/section/tag
  verification unchanged, PDF unaffected, 231 tests passing (one new
  regression test added guarding against this bug class recurring).
- [Follow-up audit after IN-029–032 (2026-09-01)](tickets/IN-033.md) — a
  fresh 4-fork re-audit after IN-029–032 closed found 3 more issues: dead
  no-op `.replace()` calls left in `decorate_dashboard_html()` (same shape
  as IN-030's root cause, but harmless - superseded by a later correct
  replace each time); `in020`/`in021`'s "must agree" regulatory-floor guard
  actually diverged (`floor==0` vs `minimum==0`), now aligned; and 10 build
  scripts (Aldermore, Co-operative Bank, HSBC UK Bank plc, Investec Bank,
  Lloyds Bank Corporate Markets, Lloyds Bank, Metro Bank, National
  Westminster Bank plc, Nomura Bank International, Paragon) had real source
  URLs on hand but never wired them into `add_wide_interim_sheet()`'s
  `hyperlink_cells` - fixed using each script's own existing URL data (no
  new research needed) and all 10 workbooks rebuilt. Swept all 145
  workbooks with an interim sheet: 0 missing hyperlinks anywhere. 231 tests
  passing, live refresh clean.
- [IN-029 through IN-032 fixed (2026-09-01)](tickets/IN-030.md) — user asked
  to work the 4 tickets opened from the same-day audit. All fixed and
  verified (231 tests passing, live refresh clean): IN-029's `analyze_trends.py`
  now guards against the percent-vs-absolute row-selection bug, plus 4
  related tie-break/dedup fixes. IN-030's fix turned out deeper than
  originally scoped: `build_in005_prototype.py`'s `TEMPLATE` had a *stale
  duplicate* of the dashboard shell baked directly into it (pre-dating the
  9-link nav/watchlist/search/sparklines), which silently defeated every
  patch `decorate_dashboard_html()` tried to apply - removing that duplicate
  fixed the missing CSS, missing nav, and missing global-search box all at
  once, not just the `.kpi-sparkline` rule originally flagged; also fixed
  the unclosed `<section>`, a latent `</script>`-injection risk, the
  hardcoded PDF date (now computed from the database's own refresh
  timestamp), and a PDF legend-overlap edge case. IN-031's `verify_workbook.py`
  dead branch is now live; the 342 broken interim hyperlinks (NatWest
  Markets, SMBC) turned out to be workbooks that were simply stale relative
  to already-correct build-script source data (SMBC) or a build script that
  sourced real URLs but never wired them into `hyperlink_cells` (NatWest
  Markets) - both rebuilt, 0 non-URL hyperlinks remain, swept all 145 banks
  to confirm no other bank is affected. IN-032's `extract_metrics.py` now
  fails loudly on a partial-extraction failure instead of validating a
  reduced bank count against itself, plus 4 minor edge-case hardening fixes.

- [Aggressive full-codebase bug audit + deliverable rendering verification
  (2026-09-01)](tickets/IN-029.md) — user asked for an aggressive audit of
  all code plus confirmation the deliverables visually match expectation. No
  headless browser exists in this environment, so "visual" verification used
  the closest provable proxy (parsing HTML/CSS/JS directly, re-simulating
  chart math against real data) rather than an actual screenshot — this
  limitation was stated explicitly rather than claiming to have "seen" the
  page. Ran 5 parallel read-only audits covering all of `scripts/insights/`,
  `bank_workbook.py`/`verify_workbook.py`, a security/robustness sweep, and
  deliverable-rendering verification. Security came back genuinely clean (no
  SQL injection, no XSS gap, no resource leaks). Found and ticketed 4 new
  issues: **IN-029** — `analyze_trends.py` is a 4th independent,
  unguarded row-selection implementation feeding the live HTML trend chart
  (same recurring bug class as IN-028, never fixed there), plus 4 related
  tie-break/dedup inconsistencies (in020's dormant minimum+buffer bug,
  in009's basis tie-break, analysis_queries' lexical "latest interim"
  fallback, extract_metrics' unit/basis-blind dedup). **IN-030** — the most
  user-visible finding: IN-027's watchlist panel, freshness badge, and
  sparklines have **zero matching CSS anywhere in the file**, so despite that
  ticket's Resolution claiming it was "implemented and validated," those
  elements currently render as unstyled plain divs/text — directly
  contradicts what the user asked IN-027 to deliver. Also an unclosed
  `<section id="overview">` (its own fix code is dead — targets a
  placeholder string already substituted away), a latent `</script>`-breakage
  risk in the main JSON payload, and a hardcoded stale "29 August 2026" date
  on the PDF cover page that's been visibly wrong through multiple
  regenerations since. **IN-031** — `verify_workbook.py`'s wide-format
  Interim Pillar 3 checks are dead code (wrong branch — every interim sheet
  built today gets zero structural verification from this tool), plus 342 of
  1,409 interim hyperlink cells (NatWest Markets, SMBC) fall back to non-URL
  text, contradicting the earlier "final-audit citation remediation" record.
  **IN-032** — lower-priority: `extract_metrics.py` can't detect its own
  partial-extraction failure (validates the DB against the count it just
  wrote, not a true independent expectation), plus minor edge-case hardening.
  Not fixed — user asked to hold all implementation until their weekly usage
  limit resets; logged as findings/tickets only.

- [Full data-correctness review (2026-09-01)](tickets/IN-028.md) — user asked
  for a final thorough check that all data in the banks and every deliverable
  is correct and consistent across places it's shown more than once. Ran 5
  parallel read-only audits: workbook↔DB extraction (0 mismatches, 22 banks ×
  7 ratio sheets + 5 cash-flow statements), cross-payload consistency
  (in009/in016/in017/in021-025 JSON + CSV + parent-groups markdown),
  HTML↔PDF deliverable consistency (0 mismatches across 11+ headline
  figures; no leaked ticket IDs/tracebacks), full 145-bank anomaly sweep
  (confirmed the 2026-08-30 fixes hold everywhere, no trace of the old bad
  values), and pipeline health (219 tests passing, clean `refresh_all.py`,
  byte-parity exports). Found the pipeline overall in very good shape, plus
  2 new confirmed bugs, both in `in016_distribution.py`'s independently
  duplicated row-selection logic (same root cause as the 2026-08-30 fix,
  different manifestations it didn't cover): (1) a lexical string-sort
  tie-break picks the wrong one of two both-valid percentage variants
  (21 leverage/MREL cells, e.g. Barclays Bank UK PLC's FY2021 leverage ratio
  showing 5.6% in one deliverable section and 4.1% in another for the same
  bank/year), and (2) Kingdom Bank Limited's Total Capital absolute figure
  inconsistently selects a different row definition across years, understating
  it in 3 of 5 years. Opened IN-028 to fix both at the root (unify into
  in009's canonical selector rather than patching in016 a third time) and to
  fix minor README doc-drift (missing file-table entries, undocumented
  refresh_all.py steps) found in the same pass. The implementation and
  verification are recorded in the IN-028 resolution below.

- [IN-028 selector unification (2026-09-01)](tickets/IN-028.md) — closed after
  moving IN-016's ratio, rank-cohort, and absolute-metric selection onto
  IN-009's canonical selector, reconciling IN-024 and IN-025, updating README
  documentation, and re-running the full 145-bank sweep with zero mismatches.

- [Leverage/LCR/NSFR/MREL row-selection bug fix (2026-08-30)](../../scripts/insights/in009_analysis.py)
  — the user spotted Barclays Bank Plc's leverage ratio listed as 56465% and
  asked for it to be checked. Root cause: `_select_metric_observations`/
  `_label_rank` in `in009_analysis.py` picked one row per bank/sheet using a
  small curated preferred-label dict, falling back to plain alphabetical
  sort of the label text when a bank's real label wasn't in that dict.
  "Tier 1 (T1) capital used in leverage calculation (£m)" = 56465 sorted
  before "UK leverage ratio (%)" = 5.8% purely because "T" < "U", so the
  absolute £m figure was reported as if it were the ratio. Re-running the
  real selection logic against all 145 banks found 65 wrong (bank, year)
  selections across the Leverage Ratio, LCR, MREL Ratio, and NSFR sheets
  (CET1/Tier 1/Total Capital Ratio were already fully covered by the
  curated dict, so unaffected; the absolute-only sheets like CET1 Capital
  were never affected). Fixed by adding `_is_percent_value()` (checks the
  `unit` field and a literal `%` in `value_raw`) so percentage rows are
  always preferred over absolute-amount rows before falling back to
  alphabetical, and a `PERCENT_ONLY_SHEETS` guard so a bank/year with no
  disclosed percentage is excluded outright rather than silently backfilled
  with an unrelated absolute figure (caught 4 more wrong selections for
  Handelsbanken's undisclosed FY2021-24 MREL ratio). Verified: real-data
  re-check now shows 0 wrong selections across all 7 ratio sheets; 3 new
  regression tests added to `test_in009_analysis.py` (188 tests total, all
  passing); live `refresh_all.py` rerun end-to-end confirmed the fix reaches
  the HTML/PDF deliverables and all downstream JSON outputs (in016, in017,
  in021, Power BI exports) that consume `in009_analysis`'s selection.

- [Ticket 1 implementation graph (2026-08-30)](tickets/IN-009.md) — the next
  work was initially split into seven tickets. IN-009 owns evidence-backed metric/period
  normalization, strict/broad comparability, core-ratio trends, and outliers;
  IN-010 owns parent-group dispersion and trend agreement after IN-009;
  IN-011 integrates both analyses into the HTML/PDF deliverables; IN-012 adds
  absolute and size-aware capital/RWA analysis after IN-009; and IN-013 adds
  the shared SQLite analysis-query layer, with permission to split it further
  if its seams become independently substantial. IN-014 integrates the
  absolute-analysis payload into the existing HTML/PDF deliverables after
  IN-011 and IN-012.

  ```text
  IN-008 (SQLite source of truth)
      |
      v
  IN-009 (normalization + core trends + outliers)
      |\\
      | \\--> IN-012 (absolute/size-aware analysis)
      |       |
      |       v
      |     IN-014 (absolute visualisation integration)
      v
  IN-010 (parent-group analysis) ----\\
      |                                v
      +----------------------------> IN-011 (HTML/PDF integration)
      |
      +----------------------------> IN-013 (shared analysis queries)

  Enrichment / Power BI follow-on graph (2026-08-30):

      IN-013 ──┬──> IN-015 (interim + period model) ──┐
               ├──> IN-017 (quality + lineage)       ├──> IN-018 (Power BI model)
               └──> IN-016 (benchmarks + uncertainty)┘          |
                                                                 v
                                                        IN-019 (report experience) [closed]
      IN-017 ───────────────────────────────> IN-020 (regulatory context)
      IN-009 ───────────────────────────────> IN-021 (headroom trajectory)
      IN-020 ───────────────────────────────> IN-021
  ```

- [IN-011 — deliverable integration](tickets/IN-011.md) — closed 2026-08-30;
  the HTML and PDF now consume shared IN-009/IN-010 payloads for coverage,
  outlier, and parent-group analysis, with 149 insights tests passing. IN-012
  adds unit-aware absolute capital/RWA trends, size cohorts, and scale-adjusted
  relationships, with explicit metadata on latest values and comparison
  coverage.

- [IN-014 — absolute-analysis visualisation integration](tickets/IN-014.md) —
  closed 2026-08-30 after IN-012. It extends the existing HTML/PDF
  deliverables with unit-aware absolute-capital/RWA visualisations and
  accessible tabular fallbacks.
- [Power BI and Pillar 3 enrichment review](../../research/powerbi_pillar3_capability_gap_2026-08-30.md)
  (2026-08-30) — current data review recommends IN-015 through IN-020:
  period-aware interim data, distributional benchmarks, a Power BI-ready star
  schema, source-quality monitoring, an interactive investigation experience,
  and versioned regulatory context. IN-017 is the recommended first ticket;
  richer visuals should follow evidence and comparability contracts.
- [IN-015 — interim and quarterly enrichment](tickets/IN-015.md) — closed
  2026-08-30. The 14 interim sheets are represented in separate SQLite
  observation/source-register tables and surfaced as cadence/coverage context;
  annual analyses remain isolated.
- [IN-021 — regulatory headroom trajectory and early-warning screening](tickets/IN-021.md) — closed 2026-08-30. Added a shared annual headroom screen that combines dated regulatory floors (including applicable CET1 buffer context) with observed multi-year movement, explicitly retaining insufficient-evidence and unavailable-context states. The screen is integrated into both HTML and PDF deliverables and deliberately does not project breach dates or future values. The live dataset currently has 480 bank-metric records, all marked `no_regulatory_context` because IN-020's safe basis-matching policy cannot classify the annual reporting basis; this is surfaced rather than manufactured into coverage. Full suite: 185 tests passing.

- [New visualisation tickets (2026-08-30)](tickets/IN-022.md) — the user
  confirmed the audience is banking/Basel-literate readers who need a fast
  summary across all banks, the primary output is enhanced HTML/PDF, broad
  comparability is acceptable for deeper discovery, and Python is preferred.
  IN-022 through IN-025 therefore prioritise ratio decomposition, robust
  distributions, persistent trajectories/rank movement, and source-quality
  coverage. Broad mode is the default discovery lens; strict mode remains a
  validation lens. The intended reading order is executive findings, compact
  diagnostics, then source-trace appendix.

  ```text
  IN-009 + IN-012 ──> IN-022 (capital-ratio decomposition)
  IN-016 + IN-017 ──> IN-023 (robust distributions + coverage visuals)
  IN-009 + IN-016 ──> IN-024 (persistent trajectories + rank mobility)
  IN-015 + IN-017 ──> IN-025 (source quality + disclosure coverage)
  IN-022 ─┐
  IN-023 ─┼──> enhanced HTML/PDF integration pass
  IN-024 ─┤
  IN-025 ─┘
  ```

- [Charting this map](map.md) — destination, tracker design (new `IN-` prefix,
  real dependency edges instead of a strict chain, concurrent-claiming
  convention), and initial ticket set settled via `/wayfinder` + `/grilling`
  on 2026-08-29.
- [IN-001 — metrics-extraction tool](tickets/IN-001.md) — built
  `scripts/extract_metrics.py`, normalizing all 145 workbooks into
  `research/bank_metrics.csv` (12,881 rows). All 145 banks matched a unique
  FRN. Found the actual full/pillar3-only split is 126/19, not the 119/26
  `Build Effort Review.md` stated — root cause (Morgan Stanley Bank
  International mislabelled as full) found and both fixed. MREL Ratio is
  almost entirely non-numeric (644 of 713 non-numeric) — noted for IN-003 to
  weigh, not excluded outright (the user clarified non-numeric there usually
  just means genuine non-disclosure, not bad data, so it can still be a
  meaningful clustering signal). Unblocks IN-003 and IN-004.
  **Follow-up (2026-08-29, spec from Codex/IN-002)**: added `canonical_bank`/
  `source_filename_bank` columns, deduplicated 35 identical-valued duplicate
  rows (a genuine source pattern, not a bug — some Cash Flow Statements
  restate the closing-cash total a second time as a breakdown subtotal),
  added structural-omission warnings. `research/bank_metrics.csv` now has
  12,846 rows (was 12,881); IN-003's clustering output unaffected.
  **Second follow-up (2026-08-29)**: identity key switched to `frn` (was
  `bank`) for dedup/grouping, stable under a filename rename; added
  `source_workbook` column; added `scripts/test_extract_metrics.py` (13
  regression tests, including the real Barclays/HSBC sibling-entity repro
  case); added a `SCHEMA_VERSION` + `research/bank_metrics.csv.schema.json`
  manifest written on every run. Row count/kind split unchanged, all tests
  pass. Flagged for IN-007 (SQLite database build, since split into
  IN-007/IN-008 — see below) to read this ticket's schema-manifest work
  before starting.
- [IN-002 — parent-group mapping](tickets/IN-002.md) — closed 2026-08-29;
  published `../../research/bank_parent_groups.md` with all 145 bank nodes,
  typed/effective-dated ownership and regulatory edges, lookup tables, and
  Mermaid cluster views. IN-004 can now proceed with confirmed group
  comparisons; non-single-parent rows must retain their ownership caveats.
- [IN-007 — SQLite database build](tickets/IN-007.md) — split 2026-08-29 at
  the user's request from the original combined "SQLite source of truth"
  ticket, which bundled building the database with migrating existing
  consumers onto it (touching working code like `scripts/cluster_banks.py`)
  — too large and too risky as one ticket. IN-007 is build-and-validate
  only: normalized annual metrics from IN-001 plus the typed parent-group
  graph from IN-002, imported into `research/insights.db`, CSV/markdown left
  completely untouched. **Closed 2026-08-29**: built
  `scripts/build_insights_db.py` (5 tables: banks, annual_metrics,
  parent_group_lookup, parent_group_edges, refresh_metadata). All
  validation passed on the first real run: 145 banks/FRNs, 12,846
  annual_metrics rows matching IN-001's schema manifest exactly, 0
  duplicate keys, 0 orphaned rows, all 145 parent_group_lookup rows join by
  FRN with zero crosswalk. Neither input file was touched (confirmed via
  mtimes). Unblocks IN-008.
- [IN-008 — migrate to the SQLite source of truth](tickets/IN-008.md) — the
  other half of the split. Migrates `cluster_banks.py`/this map's Notes onto
  the database. Blocked by IN-007. Carries explicit (non-blocking) guidance
  to wait for IN-004/IN-005a/IN-005b/IN-005c/IN-006 to close first, since those are actively
  building the client deliverable against the CSV/markdown and migrating the
  data source out from under them mid-build would just be churn.
  **Source-of-truth decision (2026-08-29, the user)**: the database is the
  source of truth going forward; `research/bank_metrics.csv` and
  `research/bank_parent_groups.md` become generated exports FROM the
  database (IN-001/IN-002's scripts get their refresh path inverted), not
  independently-maintained files the database is built from. IN-008's
  ticket updated to reflect this as settled, not open.
  **Closed 2026-08-29**: proceeded without waiting on IN-006 (nothing was
  in-flight yet to disrupt). `research/insights.db` is now what
  `extract_metrics.py`/`export_parent_group_tables.py` (new) write to, and
  what `cluster_banks.py` reads from by default (`--in <csv>` kept as an
  explicit fallback). CSV/markdown export scoped to "splice just the two
  mechanical tables" for the markdown, per the user's choice — the
  Conventions/Mermaid/Quality prose stays hand-authored, untouched by any
  script. Verified byte-for-byte parity end-to-end on a clean-slate rebuild
  against pre-migration backups: CSV, markdown, and all cluster outputs
  (including the `--exclude-mrel` variant) identical; clustering result
  unchanged (k=2, 95/18 split, silhouette 0.6599). Two real bugs caught and
  fixed while building this (an FK-enforcement DROP ordering error, and a
  markdown row-order mismatch from re-sorting instead of preserving source
  order) — both would have surfaced as silent data corruption if shipped
  unnoticed. Added 6 new regression tests (4 in `test_extract_metrics.py`,
  a new `test_cluster_banks.py`); 19 total across the project's test
  suites, all passing.
  **Follow-up (2026-08-29, per CODING_STANDARDS.md)**: (1) `analyze_trends.py`/
  `review_trend_selection.py` now read the database by default too, via a
  new shared `load_groups_from_db()`, with explicit `--csv`/`--markdown`
  fallbacks that are never silently mixed; (2) the HTML/PDF deliverable
  generators' hardcoded headline counts ("73 of 99" etc.) are now computed
  live via a new shared `analyze_trends.pairwise_counts()` — caught a real
  bug en route (a naive mean-based cluster-centroid recomputation gave a
  wrong number; fixed by reading IN-003's own correct centroids CSV
  instead); (3) added nullable `unit`/`reporting_basis`/`restatement_note`/
  `source_note` (annual_metrics) and `effective_from`/`effective_to`
  (parent_group_edges) columns, migrated onto the existing database with
  zero data loss (verified against a backup), populated where mechanically
  extractable and left NULL (not guessed) where not — `reporting_basis` is
  NULL for every row, flagged as a real gap; (4) `export_parent_group_tables.py`
  now leaves a no-op file's inode/mtime completely untouched instead of
  always rewriting it. 9 more regression tests added (27 total, all
  passing); full clean-slate pipeline rerun end-to-end with byte-parity
  checks throughout.
- [Build Effort Review.md correction](../../Build%20Effort%20Review.md) —
  fixed the stale "119 full + 26 Pillar-3-only" summary line and Morgan
  Stanley Bank International's ranking entry to match IN-001's ground-truth
  126/19 split, at the user's request.
- [IN-003 — statistical clustering](tickets/IN-003.md) — built
  `scripts/cluster_banks.py`; clusters on the 7 Pillar 3 ratio sheets
  (MREL kept in per the user, despite sparse coverage). k=2 chosen by
  silhouette score: a 95-bank "low CET1/Tier 1 Ratio" cluster (established/
  mainstream banks) vs. an 18-bank "high CET1/Tier 1 Ratio" cluster
  (smaller/specialist banks with much larger capital buffers). 113/145
  banks clustered, 32 flagged "insufficient data" (<4/7 dimensions
  populated) rather than forced in. Output at `research/bank_clusters.csv`,
  with source-year columns plus persisted centroids and k-sweep results.
  MREL is retained in the primary run despite 9/145 numeric observations;
  `--exclude-mrel` sensitivity output is also saved and raises the k=2
  silhouette from 0.6599 to 0.6912 without changing the 95/18 split.
  Unblocks IN-005 once IN-004 also closes.
- [IN-004 — cross-bank trend extension](tickets/IN-004.md) — closed 2026-08-29;
  added `scripts/analyze_trends.py` and refreshed `../../Cross-Bank Trends
  Analysis.md` against all 145 FRN-keyed entities. Capital-ratio softening
  remains a broad directional pattern, while the original LCR majority is
  sample-sensitive at full scale (38 down / 35 up). Added within-group checks
  for the six multi-entity parent groups; no additional time-clustered finding
  survived the basis and single-bank-quirk checks yet.
- [IN-006 — final delivery format](tickets/IN-006.md) — closed 2026-08-29;
  settled on a presentation-ready interactive HTML Artifact as primary, with
  a fixed PDF snapshot and reproducible Python generation scripts.
- [IN-005 — client deliverable prototype](tickets/IN-005.md) — closed 2026-08-29;
  its refined prototype informed the final HTML/PDF format settled in IN-006.
- [IN-005a — prototype visual refinement](tickets/IN-005a.md) — closed 2026-08-29; improves
  plain-language labels, chart legibility, scale explanations, and takeaways.
- [IN-005b — selectable trend analysis](tickets/IN-005b.md) — closed 2026-08-29; adds period
  and metric-count controls after the visual baseline is clear.
- [IN-005c — parent-group drill-down](tickets/IN-005c.md) — closed 2026-08-29; adds clickable
  entity-level inspection while preserving reporting-basis caveats.
- [IN-005d — expanded trend controls](tickets/IN-005d.md) — closed 2026-08-29; adds
  all adjacent year windows, more metrics, and responsive count layout.
- [IN-005e — parent-group metric selector](tickets/IN-005e.md) — closed 2026-08-29;
  lets users choose the metrics shown in group drill-downs.
- [IN-005f — independent trend rows](tickets/IN-005f.md) — closed 2026-08-29;
  adds per-row metric selectors and arbitrary start/end-year comparisons,
  including total RWA.
- [IN-005g — metric terminology and chart polish](tickets/IN-005g.md) — closed
  2026-08-29; separates trend counts, clarifies Total Capital, and defines all
  selectable metrics.
- [IN-005h — default trends and peer-group exploration](tickets/IN-005h.md) —
  closed 2026-08-29; sets useful defaults and makes all peer categories
  clickable.
- [IN-005i — peer toggles and dual parent metrics](tickets/IN-005i.md) — closed
  2026-08-29; adds list toggles, label clearance, a vertical metric guide, and
  two simultaneous parent-group metrics.
- [IN-005j — distinct key takeaways](tickets/IN-005j.md) — closed 2026-08-29;
  replaces duplicated explanatory points with cross-bank trend signals.
- [IN-006 — final client deliverable](tickets/IN-006.md) — closed 2026-08-29;
  primary interactive HTML Artifact and fixed PDF companion are generated.
- [Insights pipeline moved to `scripts/insights/`](../../scripts/insights/README.md)
  — 2026-08-29, for maintainability: the 13 actively-developed insights
  scripts (+ their tests) were separated from the ~145 static one-off
  bank-build scripts in the flat `scripts/` directory. All internal imports,
  path constants, and `refresh_all.py`/`test_pipeline.py`'s subprocess
  targets were updated for the new depth; full test suite (34 tests) and a
  live `refresh_all.py` run confirmed working from both the new directory
  and an unrelated `cwd`, with byte-parity preserved on every export. Only
  `scripts/bank_workbook.py` stays imported from the parent directory (used
  for `PILLAR3_SHEET_NAMES` and, in tests, `BankWorkbook`). See the new
  `scripts/insights/README.md` for the full file-by-file reference.
- [Test coverage review](../../scripts/insights/README.md) — 2026-08-29. A
  careful pass over the existing 34 tests found real gaps concentrated in
  complex/failure-path logic that had never been exercised: the hand-rolled
  k-means/silhouette implementation, `validate()`'s and
  `validate_cluster_inputs()`'s failure paths (only their happy paths were
  tested), the idempotent schema migration (previously verified manually
  only), `review_trend_selection.py` (zero tests for the whole file), the
  computed (not hardcoded) deliverable numbers, `refresh_all.py`'s
  stop-on-failure behaviour, and the per-workbook error-continuation path in
  `extract_metrics.py` (added a `--banks-dir` override specifically to make
  this testable, mirroring the project's existing `--db`/`--csv`/`--markdown`
  pattern). 6 new test files added (`test_build_insights_db.py`,
  `test_review_trend_selection.py`, `test_export_parent_group_tables.py`,
  `test_deliverables.py`, `test_refresh_all.py`, plus substantial additions
  to `test_cluster_banks.py`/`test_analyze_trends.py`/`test_extract_metrics.py`).
  116 tests total, all passing; full live `refresh_all.py` run and
  byte-parity check confirm no regression. One real bug caught by a test's
  own hand-calculated expectation being wrong, not the source (a mismatched
  year window in a headline-numbers test) — fixed the test, not the source.

- [New insight review (2026-08-30)](tickets/IN-021.md) — reviewed the full
  current state of the pipeline (IN-009 through IN-020) against what a
  PowerBI/data-platform build would typically surface next. Found one angle
  none of the existing tickets cover: IN-009 computes trend direction/magnitude
  per metric, and IN-020 attaches a static regulatory minimum, but nothing
  combines the two into a forward-looking "which banks' own trajectory is
  eroding headroom toward their regulatory floor fastest" screen — a
  leading-indicator view distinct from IN-016's point-in-time peer ranking.
  Opened IN-021 (regulatory headroom trajectory and early-warning screening),
  with an explicit ban on numeric/date extrapolation — it screens by trend
  magnitude and current headroom, not a fabricated forecast. Unlike the
  IN-009→IN-011/IN-012→IN-014 precedent of a separate deliverable-integration
  ticket, the user asked for HTML/PDF integration to be carried in this same
  ticket, so its scope includes wiring the screen into both
  `build_in005_prototype.py` and `build_in006_pdf.py`, not just producing the
  underlying JSON.

## Not yet specified

- Real PowerBI integration (an actual data export/pipeline feeding a live
  PowerBI dashboard) — now sharpened into IN-017 and IN-019 after the
  2026-08-30 enrichment review; actual service deployment remains future work.
- Folding in the 14th "Interim Pillar 3" sheets (quarterly/semi-annual data,
  present on only some banks) — now IN-015, with annual-only compatibility as
  a hard requirement.
- Any refresh-automation trigger (e.g. re-running the extraction tool
  automatically when `banks/` changes) — the bank-build map considered and
  deferred the equivalent (cloud/cron session automation) for lack of a git
  repo/GitHub remote; likely the same answer here, but not decided yet.

## Out of scope

(none yet)

## Ticket index

| Ticket | Title | Status |
|---|---|---|
| [IN-001](tickets/IN-001.md) | Build the reusable metrics-extraction tool | closed |
| [IN-002](tickets/IN-002.md) | Research and build the bank → parent-group mapping | closed |
| [IN-003](tickets/IN-003.md) | Statistical clustering pass | closed |
| [IN-004](tickets/IN-004.md) | Extend the cross-bank trend analysis to all 145 banks | closed |
| [IN-005](tickets/IN-005.md) | Prototype the client deliverable | closed |
| [IN-006](tickets/IN-006.md) | Lock delivery format and finish the deliverable | closed |
| [IN-007](tickets/IN-007.md) | Build a SQLite database from current data | closed |
| [IN-008](tickets/IN-008.md) | Migrate scripts and docs to the SQLite source of truth | closed |
| [IN-009](tickets/IN-009.md) | Core-ratio comparability, trends, and outliers | closed |
| [IN-010](tickets/IN-010.md) | Parent-group dispersion and trend agreement | closed |
| [IN-011](tickets/IN-011.md) | Integrate the new analysis into HTML and PDF deliverables | closed |
| [IN-012](tickets/IN-012.md) | Absolute capital/RWA and size-aware analysis | closed |
| [IN-013](tickets/IN-013.md) | Shared SQLite analysis-query layer | closed |
| [IN-014](tickets/IN-014.md) | Absolute-analysis visualisation integration | closed |
| [IN-005a](tickets/IN-005a.md) | Refine prototype visual hierarchy and trend readability | closed |
| [IN-005b](tickets/IN-005b.md) | Add selectable trend analysis to the prototype | closed |
| [IN-005c](tickets/IN-005c.md) | Add clickable parent-group drill-down | closed |
| [IN-005d](tickets/IN-005d.md) | Expand trend controls across years and ratios | closed |
| [IN-005e](tickets/IN-005e.md) | Add parent-group metric selector | closed |
| [IN-005f](tickets/IN-005f.md) | Make trend rows independently selectable | closed |
| [IN-005g](tickets/IN-005g.md) | Polish prototype metric terminology and chart layout | closed |
| [IN-005h](tickets/IN-005h.md) | Refine default trends and peer-group exploration | closed |
| [IN-005i](tickets/IN-005i.md) | Add peer-group toggles and dual parent-group metrics | closed |
| [IN-005j](tickets/IN-005j.md) | Replace duplicated key takeaways with cross-bank signals | closed |
| [IN-015](tickets/IN-015.md) | Period-aware interim and quarterly disclosure enrichment | closed |
| [IN-016](tickets/IN-016.md) | Distributional benchmarks, ranks, and uncertainty context | closed |
| [IN-017](tickets/IN-017.md) | Source lineage and data-quality monitoring view | closed |
| [IN-018](tickets/IN-018.md) | Power BI-ready star schema and semantic-model contract | closed |
| [IN-019](tickets/IN-019.md) | Interactive Power BI exploration and investigation experience | closed |
| [IN-020](tickets/IN-020.md) | Versioned regulatory benchmark and threshold context | closed |
| [IN-021](tickets/IN-021.md) | Regulatory headroom trajectory and early-warning screening | closed |
| [IN-022](tickets/IN-022.md) | Decompose capital-ratio movements | closed |
| [IN-023](tickets/IN-023.md) | Add robust distribution and coverage visuals | closed |
| [IN-024](tickets/IN-024.md) | Show persistent trajectories and rank mobility | closed |
| [IN-025](tickets/IN-025.md) | Add source-quality and disclosure-coverage views | closed |
| [IN-026](tickets/IN-026.md) | Give the HTML deliverable a dashboard-style analytical layout | closed |
| [IN-027](tickets/IN-027.md) | Dashboard redesign: watchlist panel, full section nav, bank drill-through, trend sparklines | closed |
| [IN-028](tickets/IN-028.md) | in016_distribution.py's independent row-selection logic diverges from in009's canonical selector (2 confirmed bugs) | closed |
| [IN-029](tickets/IN-029.md) | analyze_trends.py is an unguarded 4th duplicated row-selection implementation, plus related tie-break/dedup inconsistencies | closed |
| [IN-030](tickets/IN-030.md) | Deliverable rendering defects: IN-027 watchlist/freshness/sparklines have no CSS, unclosed &lt;section&gt;, stale PDF date | closed |
| [IN-031](tickets/IN-031.md) | verify_workbook.py's wide-format interim checks are dead code; 342 broken interim hyperlinks (NatWest Markets, SMBC) | closed |
| [IN-032](tickets/IN-032.md) | Pipeline robustness: extract_metrics.py can't detect its own partial-extraction failure, plus minor edge-case hardening | closed |
| [IN-033](tickets/IN-033.md) | Follow-up audit after IN-029–032: dead no-op string replaces, a fragile tie-break agreement, and 10 build scripts with unwired interim hyperlinks | closed |
| [IN-034](tickets/IN-034.md) | HTML deliverable was 131MB and effectively unusable in a browser: in023 duplicated in016/in017 wholesale, and in016/in017/in025 embedded large server-only data the client never reads | closed |

This table is bookkeeping only, kept in sync manually — a ticket's frontmatter
`status` field is the source of truth if the two ever disagree.
