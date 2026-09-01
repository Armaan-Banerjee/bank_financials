# Handoff: katalysis insights pipeline

**Date**: 2026-08-29
**Repo**: `/Users/armaan/code/katalysis` (no git — a data project, not a software repo)
**Session focus**: chartered and drove the `wayfinder/insights/` map end-to-end
(IN-001 → IN-008 and beyond), then did a deliberate test-coverage hardening pass.

## Read these first, don't re-derive them

- `/Users/armaan/code/katalysis/CLAUDE.md` — repo orientation, points to both
  the bank-build side and the insights pipeline.
- `/Users/armaan/code/katalysis/CODING_STANDARDS.md` — the rules governing
  this codebase (source-of-truth direction, missing-data handling, refresh
  safety, no hardcoded data-derived figures, testing bar). Both models
  (this Claude session and a concurrent Codex session) are expected to
  follow it. **Read before touching any script.**
- `/Users/armaan/code/katalysis/scripts/insights/README.md` — file-by-file
  map of the pipeline: what each script reads/writes, the two deliberately
  hand-curated exceptions (`GROUP_VERDICTS` in `build_in005_prototype.py`,
  `GROUP_DISPLAY_NAMES` in `build_in006_pdf.py`), and known deliberate gaps.
- `/Users/armaan/code/katalysis/wayfinder/insights/map.md` — the actual
  decision log for this effort (destination, Notes, Decisions-so-far, ticket
  index). **This is the map — don't reconstruct it from memory or from this
  handoff.** All `IN-001` through `IN-008` tickets (plus `IN-005a`–`IN-005j`)
  are `closed`.
- Memory (auto-loaded, but named here for clarity): `wayfinder_insights_map`
  and `wayfinder_map` in this project's memory store — the insights map
  entry should already point here.

## Project shape (two halves)

1. **Bank-workbook builds** (`wayfinder/map.md`, closed) — 145 Excel
   workbooks in `banks/`, one per UK PRA-authorised bank. Static, finished.
   Its ~150 build scripts live in `scripts/` (flat, untouched this session).
2. **Insights pipeline** (`wayfinder/insights/map.md`) — normalizes those
   145 workbooks into `research/insights.db` (SQLite, **the source of
   truth**), clusters banks into peer groups, extends a cross-bank trend
   analysis, and produces a client deliverable (HTML + PDF). This is what
   the whole session was about. Lives in `scripts/insights/` (moved there
   from flat `scripts/` this session, for maintainability — see the
   README's rationale).

**Refresh the whole pipeline with `python3 scripts/insights/refresh_all.py`**
— never run the individual scripts by hand in the wrong order; the
dependency order isn't obvious and getting it wrong fails *silently*
(produces an empty parent-group section, not a crash). This bit me once
during the session — see its docstring.

## What happened this session, roughly in order

1. Charted the `wayfinder/insights/` map via `/wayfinder` + grilling — destination,
   tracker design (new `IN-` ticket prefix, **real dependency edges not a
   strict chain**, since two models work this map concurrently).
2. Built `scripts/insights/extract_metrics.py` (IN-001): workbooks → normalized
   rows, FRN-based identity (found and fixed real sibling-entity collisions —
   Barclays Bank Plc vs Barclays Bank UK PLC, the two Credit Suisse/HSBC
   entities), deduplication, schema-versioned CSV export.
3. Reviewed/verified a concurrent Codex session's IN-002 (parent-group graph)
   and IN-004 (trend analysis) work — found and got fixed a real FRN-vs-name
   join gap in IN-002's first pass.
4. Built `cluster_banks.py` (IN-003): dependency-free NumPy k-means/silhouette
   clustering on 7 Pillar-3 ratio dimensions. k=2 chosen (95 "established"
   banks vs 18 "high-buffer" banks). Two real bugs caught and fixed en route:
   percent-vs-absolute-amount row selection, and outlier-robust (median/IQR,
   winsorized) standardization instead of naive mean/std.
5. Split ticket **IN-007 → IN-007 (build SQLite DB) + IN-008 (migrate to it as
   source of truth)** at the user's request — IN-007 alone was too large/risky.
   IN-008 inverted the refresh path (DB written first, CSV/markdown are now
   *generated exports*, not independently maintained) and went through
   several rounds of user-reviewed follow-ups: schema completeness
   (`unit`/`reporting_basis`/`restatement_note`/`source_note` columns —
   `reporting_basis` is **deliberately left NULL for every row**, a real
   documented gap, not an oversight), dynamic (not hardcoded) headline
   numbers in the deliverables, an exporter no-op/inode-preservation fix,
   shared SQLite loaders for `analyze_trends.py`/`review_trend_selection.py`.
6. Merged concurrent Codex timing-log additions into `Build Effort Review.md`.
7. Split `scripts/` → `scripts/`/`scripts/insights/` for maintainability
   (13→18 insights files moved, all path/import depth fixed, new README).
8. **Test-coverage hardening pass** (this session's last major piece): found
   10 high-priority gaps (clustering math had zero direct tests, `validate()`
   only had happy-path coverage, `review_trend_selection.py` had zero tests,
   etc.) and fixed all 10 — added `--banks-dir` to `extract_metrics.py` and
   extracted `refresh_all.py`'s loop into a testable `run_steps()` specifically
   to make previously-untestable paths testable. Test count went 34 → 116.

## Current state — verify before trusting

I last ran the full suite at **122 tests, all passing** (up from the 116 I
reported to the user — **Codex added 6 more concurrently** while I was
writing this handoff: a rollback-preservation test in
`test_build_insights_db.py`, a stop-on-failure artifact-preservation test in
`test_refresh_all.py`, and HTML/PDF output-safety tests — escaping, PDF
pagination — in `test_deliverables.py`). This is a live, two-model
concurrent session. **Re-run before doing anything else:**

```bash
cd /Users/armaan/code/katalysis
python3 -m py_compile scripts/insights/*.py scripts/*.py
python3 -m unittest discover -s scripts/insights -p 'test*.py'
python3 scripts/insights/refresh_all.py   # live pipeline, real files
```

All `IN-*` tickets on the insights map are `closed`. There is no formal
"next ticket" queued — the map's destination (refreshable client deliverable,
DB source of truth) has been reached. What's live right now is informal
test-hardening, done in direct response to user requests rather than tracked
as tickets.

## Not yet done / worth knowing about

- **Medium-priority test gaps I flagged but did NOT implement** (deliberately
  scoped out as lower-value): `normalize_name()`/accent-stripping as isolated
  unit tests (only indirectly covered via sibling-entity tests), and
  `deduplicate()` with 3+ duplicate rows (2 identical + 1 conflicting) —
  currently only tested with exactly 2.
- **Map's own "Not yet specified" fog** (see `wayfinder/insights/map.md`):
  real PowerBI integration (explicitly deferred by the user, "a strong maybe
  for future sessions"), folding in the 14th "Interim Pillar 3" sheets some
  workbooks have (annual-only was this map's scope), any refresh-automation
  trigger (deferred, same reasoning as the bank-build map: no git repo/GitHub
  remote to hang a cron job off).
- **`reporting_basis` column is NULL for every row** — a real, permanent,
  documented gap (no source cleanly separates it from the free-text
  `basis_note` already captured per-bank). Don't try to backfill it without
  re-reading IN-008's reasoning first.
- Two curated dicts (`GROUP_VERDICTS`, `GROUP_DISPLAY_NAMES`) will silently
  omit (with a printed warning, not a crash) any future multi-entity parent
  group not already in them — if new banks get added to a shared parent
  group, someone needs to notice the warning and add the verdict by hand.

## Patterns worth repeating (this session's own experience)

- **Concurrent-claiming protocol** (see `wayfinder/insights/map.md`'s Notes):
  before starting any ticket, re-read its frontmatter fresh, confirm
  `status: open` and empty `claimed_by`, then claim immediately. This is a
  local-markdown tracker with no locking.
- **Take a backup before touching a working pipeline, then diff against it
  at every stage.** Several real bugs in this session (an FK/DROP-TABLE
  ordering issue, a row-order-preservation issue, a naive-mean-vs-real-centroid
  bug in a deliverable generator) were caught exactly this way, not by unit
  tests alone.
- **When a file is flagged "changed on disk since you last read it,"
  re-read before editing** — this session had frequent concurrent edits
  from the other model.
- Full test suite + a live `refresh_all.py` run + byte-parity diff against a
  pre-change backup, every time, before calling a pipeline change done.

## Suggested skills for the next session

- **`wayfinder`** — if the user wants to chart new work (e.g. finally
  tackling the PowerBI fog, or a formal ticket for the remaining medium-
  priority test gaps) or resume ticket-based work on either map.
- No other specialized skill is obviously needed for continuing the current
  thread (it's been direct implementation + testing, not design/research
  work) — but if the user pivots to deciding *what's next* rather than
  *keep hardening what exists*, `grilling` (via `/wayfinder`'s own charting
  flow) is the right tool, not a fresh planning pass from scratch.
