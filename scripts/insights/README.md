# Insights pipeline

This directory holds the whole "bank insights" pipeline — normalizing the
145 built bank workbooks into a queryable database, clustering banks into
peer groups, extending the cross-bank trend analysis, and producing the
client deliverable. It's the code behind the `wayfinder/insights/` map
(`wayfinder/insights/map.md` and its `IN-*` tickets) — read that map for
*why* this exists and what decisions shaped it; this file is the *how it
fits together* reference for maintaining it.

It was split out of the flat `scripts/` directory (2026-08-29) because it's
an actively-developed, cohesive system, unlike the ~145 one-off
`build_<bank>.py` scripts next door, which are a finished, largely-static
body of work per bank (see the top-level `CLAUDE.md`). The one file this
pipeline still depends on from up there is `scripts/bank_workbook.py`
(`PILLAR3_SHEET_NAMES`, and `BankWorkbook` in tests) — every script here
that needs it does `sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))`
before importing it.

## Source of truth

**`research/insights.db` (SQLite) is the source of truth.** `research/
bank_metrics.csv` and `research/bank_parent_groups.md` are *generated
exports* of it, not independently-maintained files — see
`CODING_STANDARDS.md` at the repo root for the full rule set this pipeline
follows (missing-data handling, refresh idempotency, no hardcoded
data-derived figures, etc.). Read that file before changing anything here.

Refresh path, in order (see `refresh_all.py`'s own docstring for the
full why):

```
banks/*.xlsx  ──extract_metrics.py──▶  insights.db (banks, annual_metrics)
                                              │
research/bank_parent_groups.md ──export_parent_group_tables.py──▶  insights.db (parent_group_lookup, parent_group_edges)
                                              │
                                              ▼
                          cluster_banks.py, analyze_trends.py, in009_analysis.py,
                          in010_parent_groups.py, in012_absolute_analysis.py,
                          in022_ratio_decomposition.py,
                          in016_distribution.py, in017_quality.py,
                          in023_distribution_visuals.py,
                          in024_trajectory.py,
                          in025_quality_views.py,
                          in018_powerbi.py,
                          in019_report_experience.py,
                          in020_regulatory_context.py,
                          in021_headroom_trajectory.py,
                          review_trend_selection.py
                                              │
                                              ▼
                    build_in005_prototype.py, build_in006_pdf.py  (client deliverables)
```

`extract_metrics.py`, `export_parent_group_tables.py`, `in009_analysis.py`, and `in010_parent_groups.py` also regenerate
`bank_metrics.csv` / `bank_parent_groups.md` as exports FROM the database
they just wrote — those exports are provably derived, never a second
independent copy that could drift.

## Files

| File | Reads | Writes | Purpose |
|---|---|---|---|
| `build_insights_db.py` | `bank_metrics.csv`/`bank_parent_groups.md` (standalone CLI mode only) | `insights.db` schema + shared query helpers | **The schema owner.** Also the shared home for cross-script DB helpers - `load_rows_from_db()`, `load_groups_from_db()`, `multi_entity_groups()`, `cluster_size_summary()`, `validate_cluster_inputs()`, `export_metrics_csv()`. Everything else imports from here rather than re-writing SQL. Has its own standalone CLI (`python3 build_insights_db.py`) for disaster recovery (rebuild the whole DB from the current CSV/markdown) - not the normal refresh path. |
| `extract_metrics.py` | `banks/*.xlsx`, `Banks List 2608.xlsx` | `insights.db` (banks, annual_metrics), `bank_metrics.csv` (+ `.schema.json`) | Parses every workbook sheet, matches each bank to its FRN (handling real sibling-entity ambiguity, e.g. Barclays Bank PLC vs Barclays Bank UK PLC), deduplicates on `(frn, sheet, row_label, year)`. |
| `export_parent_group_tables.py` | `bank_parent_groups.md` | `insights.db` (parent_group_lookup, parent_group_edges), splices the same two tables back into the markdown | The markdown's hand-authored prose (Conventions, Mermaid diagrams, Quality notes) is never touched - only its two mechanical pipe-tables are regenerated. No-op runs leave the file's content/mtime/inode completely untouched. |
| `cluster_banks.py` | `insights.db` (default) or `--in <csv>` | `bank_clusters*.csv` | Dependency-free NumPy k-means/silhouette clustering on the 7 Pillar 3 ratio sheets. See its own module docstring for the winsorization/robust-scaling rationale - don't "simplify" that without re-reading why it's there (a plain mean/std z-score lets a couple of known extreme disclosures dominate the whole fit). |
| `analyze_trends.py` | `insights.db` (default) or `--csv`/`--markdown` | stdout only | Cross-bank trend screening (up/down/comparable counts per metric per fiscal-year pair) and within-parent-group agreement. Exposes `pairwise_counts()` - the one shared counting function every deliverable's headline numbers must use, not a hand-typed figure. |
| `in009_analysis.py` | `insights.db` | `in009_analysis.json`, `in009_quality.md` | IN-009's evidence-backed core-ratio normalization, strict/broad coverage, movement trends, and explainable outlier screening. |
| `in010_parent_groups.py` | `insights.db` | `in010_parent_groups.json` | IN-010's latest-level parent-group dispersion and adjacent-year trend-agreement analysis. |
| `in012_absolute_analysis.py` | `insights.db` | `in012_absolute_analysis.json` | IN-012's unit-aware absolute capital/RWA trends, size cohorts, and scale-adjusted capital-to-RWA relationships. |
| `in022_ratio_decomposition.py` | `insights.db` | `in022_ratio_decomposition.json` | CET1 ratio movement decomposed into CET1 capital and total RWA changes, with broad/strict eligibility and source trace. |
| `in016_distribution.py` | `insights.db` | `in016_distribution.json` | IN-016's exact-year/basis ratio and amount distributions, fixed-panel rank movement, robust scores, and group benchmark guardrails. |
| `in017_quality.py` | `insights.db` | `in017_quality.json` | IN-017's row-level source lineage, metric quality facts, dimensions, structural checks, and refresh metadata. |
| `in023_distribution_visuals.py` | `insights.db` | `in023_distribution_visuals.json` | Robust broad/strict distribution inputs and bank × metric × year evidence-coverage states for HTML/PDF visuals. |
| `in024_trajectory.py` | `insights.db` | `in024_trajectory.json` | Persistent bank-level fingerprints, fixed-panel rank mobility, and separate coverage-churn inputs for trajectory visuals. |
| `in025_quality_views.py` | `insights.db` | `in025_quality_views.json` | Annual/interim quality states, cadence coverage, source trace completeness, and FRN join checks. |
| `in011_deliverables.py` | `insights.db` | - | Shared IN-011 adapter and HTML/PDF presentation helpers that assemble upstream analysis payloads. |
| `in018_powerbi.py` | `insights.db` | `research/powerbi/*.csv`, `semantic_model.json` | IN-018's Power BI star-schema hand-off and semantic-model contract. |
| `in019_report_experience.py` | `insights.db`, IN-009 findings | `research/powerbi/report_experience.json`, `finding_detail.csv` | IN-019's governed report pages, interaction contract, drillthrough/tooltips, exploratory warnings, navigation, accessibility and export fallbacks. |
| `in020_regulatory_context.py` | `insights.db`, authoritative context records | `research/powerbi/regulatory_context.json`, `regulatory_context.csv`, `observation_context.csv` | IN-020's dated regulatory minima, buffers, firm-specific MREL context, source citations, and safe observation-level matching policy. |
| `in021_headroom_trajectory.py` | `insights.db`, IN-009 annual series, IN-020 context | `in021_headroom_trajectory.json` | Headroom and observed erosion screen; explicitly separates screened, insufficient-evidence, and no-context cases without forecasting. |
| `analysis_queries.py` | `insights.db` | - | IN-013/IN-015's shared read-only analysis interface for annual and period-aware interim observations. |
| `review_trend_selection.py` | `insights.db` (default) or `--csv` | `in004_selection_review.md` | Manual-review queue of every FRN-year where more than one label/period variant exists (e.g. a leverage ratio's "excluding vs. including central bank claims" pair) - makes selection ambiguity visible instead of silently picking one. |
| `build_in005_prototype.py` | `insights.db`, `bank_clusters*.csv` | `wayfinder/insights/deliverable/uk_bank_insights.html` | The interactive client deliverable, including the dashboard shell, watchlist, global search, bank drill-through, and KPI sparklines. Validates its cluster-CSV inputs aren't stale relative to the database before generating anything (`build_insights_db.validate_cluster_inputs()`). |
| `build_in006_pdf.py` | `insights.db`, `bank_clusters.csv` | `wayfinder/insights/deliverable/uk_bank_insights.pdf` | Fixed PDF companion, stdlib-only PDF writer. Same staleness guard as the HTML generator. |
| `refresh_all.py` | - | runs the other 20 scripts in order | **Run this, not the individual scripts by hand**, unless you specifically want one step. The dependency order isn't obvious from any single script and skipping a step doesn't crash - it silently produces wrong output (e.g. an empty parent-group section). Always targets the real `research/` files; has no `--db` override (see its docstring for why). |
| `test_extract_metrics.py`, `test_build_insights_db.py`, `test_cluster_banks.py`, `test_analyze_trends.py`, `test_review_trend_selection.py`, `test_export_parent_group_tables.py`, `test_deliverables.py`, `test_analysis_queries.py`, `test_in009_analysis.py`, `test_in010_parent_groups.py`, `test_in011_deliverables.py`, `test_in012_absolute_analysis.py`, `test_in014_deliverables.py`, `test_in015_periods.py`, `test_in016_distribution.py`, `test_in017_quality.py`, `test_in018_powerbi.py`, `test_in019_report_experience.py`, `test_in020_regulatory_context.py`, `test_in021_headroom_trajectory.py`, `test_in022_ratio_decomposition.py`, `test_in023_distribution_visuals.py`, `test_in024_trajectory.py`, `test_in025_quality_views.py`, `test_refresh_all.py` | - | - | Unit/regression tests, run against temp files (or, for `test_refresh_all.py`, dummy scripts) only - never the real database, workbooks, or deliverables. |
| `test_pipeline.py` | - | - | Integration tests - runs every script as a real subprocess against temp databases and output files. The live database, workbooks, research exports, and deliverables are never touched by any test. |

225 tests total (`python3 -m unittest discover -s scripts/insights -p 'test*.py'`). Coverage
deliberately isn't 100% - see the "before changing anything" checklist below - but every
piece of genuinely complex logic has direct tests: the hand-rolled k-means/silhouette
implementation, `validate()`'s and `validate_cluster_inputs()`'s FAILURE paths (not just
the happy path), the idempotent schema migration against a real pre-migration schema, the
percent-vs-absolute-amount row-selection rule, every computed (not hardcoded) deliverable
number, `refresh_all.py`'s stop-on-failure behaviour, and the per-workbook
error-continuation path (a corrupt/unreadable file is skipped and logged, not a crash).

## Two curated exceptions, deliberately not computed

Two pieces of the HTML/PDF deliverables are genuine editorial judgment, not
derivable from the data, and stay hand-maintained:

- `build_in005_prototype.py`'s `GROUP_VERDICTS` - the "Aligned"/"Mixed"/"Not
  comparable" capital/cash-flow verdicts per parent group, from IN-004's
  human-reviewed analysis. Group *membership* itself is NOT in this map -
  it's loaded live via `multi_entity_groups()`.
- `build_in006_pdf.py`'s `GROUP_DISPLAY_NAMES` - short display names
  ("HSBC" vs. the database's "HSBC group") for the same groups.

If a new multi-entity parent group appears in future data (a bank added to
`research/bank_parent_groups.md` that shares a group with an existing one),
both scripts print a warning and *omit* that group from the deliverable
rather than guess a verdict or display name - go add it to the relevant
dict once you know what the right verdict is.

## Known, deliberate gaps

- `annual_metrics.reporting_basis` is a real schema column that is **NULL
  for every row**. No source in the workbooks cleanly separates "basis" as
  a per-metric field from the free-text `basis_note` already captured
  per-bank; inventing a classification risked being actively wrong, so it
  was left undone rather than faked. See IN-008's ticket for the reasoning.
- Interim/quarterly Pillar 3 data is loaded into separate
  `interim_observations` and `interim_source_register` tables by IN-015. It is
  not included in annual analyses; period-aware query and deliverable policies
  must opt in explicitly.
- Real PowerBI integration was explicitly deferred by the user - "a strong
  maybe for future sessions," not built.

## Running things

```bash
# Full refresh (the normal case)
python3 scripts/insights/refresh_all.py

# Refresh data without regenerating the client deliverables
python3 scripts/insights/refresh_all.py --stop-after cluster_banks.py

# Run the whole test suite
python3 -m unittest discover -s scripts/insights -p 'test*.py'

# Any single script's --help documents its own flags
python3 scripts/insights/cluster_banks.py --help
```

## Before changing anything here

1. Read `CODING_STANDARDS.md` (repo root).
2. Read this file's "Files" table for which script owns what.
3. After any change: `python3 -m py_compile scripts/insights/*.py`, then the
   full test suite, then `python3 scripts/insights/refresh_all.py` against
   the real files, then check `research/bank_metrics.csv`/`bank_parent_groups.md`
   for byte-parity where you didn't intend a change (`diff` against a
   pre-change copy) - several real bugs in this pipeline's history were
   caught exactly this way, not by unit tests alone.
