# Coding standards

These standards apply to both models and to all scripts in this data project.
They are deliberately practical: correctness, traceability, and safe refreshes
take priority over abstraction.

## Source of truth and data flow

- From IN-008 onward, read analytical data from `research/insights.db`.
  `bank_metrics.csv` and `bank_parent_groups.md` are generated exports.
- Keep the direction of travel explicit: source workbooks or researched graph
  data -> SQLite -> CSV/Markdown exports -> analyses and deliverables.
- **The insights pipeline lives in `scripts/insights/`** (split out from the
  flat `scripts/` directory 2026-08-29 - see `scripts/insights/README.md`
  for the full file-by-file map). The ~145 one-off `build_<bank>.py`
  workbook scripts and their shared `bank_workbook.py` stay in `scripts/`.
- **Refresh the whole pipeline with `python3 scripts/insights/refresh_all.py`.** The
  steps have a real dependency order (e.g. `export_parent_group_tables.py`
  needs `banks` populated by `extract_metrics.py` first) that isn't obvious
  from any single script, and skipping a step doesn't crash - it just
  produces quietly-wrong output (an empty parent-group section, a stale
  deliverable). Running each script by hand in the wrong order is a known
  way to lose an afternoon; don't. Use `--stop-after <script>.py` to refresh
  data without regenerating the client deliverables.
- A consumer may read an export only when it has a documented reason, such as
  an explicit CSV fallback or a human spreadsheet hand-off.
- Never silently mix database and CSV values in one calculation.
- Keep stable FRNs as join keys. Display names are for presentation only.

## Missing data and units

- Preserve missing values as `NULL` in SQLite and blank strings in CSV/Excel
  exports; never substitute zero unless the source explicitly reports zero.
- Preserve raw source text alongside parsed numeric values.
- Carry units, fiscal year/period, reporting basis, restatement status, and
  source/provenance wherever they exist in the input.
- Do not compare percentages, absolute amounts, currencies, or consolidation
  bases without an explicit conversion or caveat.
- A derived statistic must state its denominator and comparable sample size.

## Refresh and database safety

- Refresh operations must be re-runnable and idempotent.
- Write temporary outputs first and replace the destination only after
  validation succeeds. If generated content is unchanged, do not replace it.
- Validate row counts, unique keys, FRN coverage, null fidelity, and joins on
  every full refresh. Consumer scripts should fail clearly if the database is
  missing or structurally invalid.
- Keep independent refresh domains isolated, but do not leave known orphaned
  relationships silently. Either enforce foreign keys or run an equivalent
  validation before reporting success.
- Do not modify workbooks or hand-authored Markdown prose from an extraction
  or export script unless that file is explicitly in scope.

## Scripts and interfaces

- Use the standard library where practical and the project's existing global
  dependencies; do not introduce a virtual environment or dependency manifest
  for a one-off data script without a clear need.
- Give scripts a small CLI with safe defaults, explicit input/output options,
  and `--help` text. Keep fallback paths explicit, e.g. `--in` for CSV.
- Keep reusable database/query logic in one helper module rather than copying
  SQL or row-shaping logic into every consumer.
- Avoid hardcoding data-derived figures in generated deliverables. Compute
  them from the current source-of-truth data, with optional CLI overrides for
  editorial headline text.
- Use deterministic ordering and seeded algorithms for analyses so reruns can
  be compared byte-for-byte where practical.

## Validation and handoff

- Add or update focused tests for every migration or parsing rule.
- Run syntax compilation, relevant unit tests, a clean temporary rebuild, and
  an output-parity check before declaring a data pipeline change complete.
- Report what was tested, what was not tested, any remaining caveat, and the
  exact generated output paths.
- Do not claim a no-op when a file's content, metadata, or inode was changed.
- Keep ticket progress and timing notes factual; authoritative token usage is
  recorded only when the tooling exposes it.
