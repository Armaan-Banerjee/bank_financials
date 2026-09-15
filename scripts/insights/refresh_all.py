"""
Single orchestration entrypoint for the insights refresh pipeline - runs
every step against the REAL research/ files, in the correct dependency
order, and stops immediately on the first failure. Exists because the
correct order isn't obvious from any one script's own docstring, and
getting it wrong fails silently rather than loudly: running
scripts/export_parent_group_tables.py before scripts/extract_metrics.py has
ever populated `banks` raises a clear error, but running
scripts/cluster_banks.py or a deliverable generator against a
freshly-rebuilt database that skipped the parent-group step just produces
an empty `groups` section - no crash, no warning, just quietly wrong output.
(Confirmed hit exactly this while building/testing IN-008's follow-up work.)

This script always targets the real `research/` files - it does not accept
a `--db` override. For an isolated run against temporary files (e.g. to
verify a change before touching the live deliverables), use
scripts/test_pipeline.py instead, which properly isolates every output path
in its own temp directory rather than just the database.

Usage:
    python3 scripts/refresh_all.py
    python3 scripts/refresh_all.py --stop-after cluster_banks.py   # refresh data without regenerating deliverables

Order and why:
    1. extract_metrics.py           workbooks -> banks/annual_metrics (DB) -> CSV export
    2. export_parent_group_tables.py  markdown -> parent_group_lookup/edges (DB) -> markdown export
       (needs banks/annual_metrics from step 1 - parent_group_lookup FKs to banks)
    3. cluster_banks.py              DB -> bank_clusters*.csv
       (needs annual_metrics from step 1)
    4. analyze_trends.py             DB -> stdout trend diagnostics
       (needs both halves from steps 1-2; run as a live sanity check, not
       because anything downstream consumes its stdout)
    5. in009_analysis.py             DB -> IN-009 JSON/Markdown quality outputs
       (needs annual_metrics from step 1)
    6. in010_parent_groups.py        DB -> IN-010 parent-group JSON output
       (needs IN-009's normalized analysis rules)
    7. in012_absolute_analysis.py    DB -> IN-012 absolute-analysis JSON output
       (needs unit and basis validation from the absolute metric rows)
    8. in022_ratio_decomposition.py  DB -> IN-022 ratio-decomposition JSON output
       (needs IN-009 ratio selection and IN-012 amount semantics)
    9. in016_distribution.py         DB -> IN-016 distribution JSON output
    10. in017_quality.py             DB -> IN-017 quality JSON output
    11. in023_distribution_visuals.py DB -> IN-023 visualisation payload
       (needs IN-016 distributions and IN-017 quality classifications)
    12. in024_trajectory.py          DB -> IN-024 trajectory JSON output
       (needs IN-016's percentile_rank helper)
    13. in025_quality_views.py       DB -> IN-025 quality-views JSON output
       (reads the DB directly; no upstream step dependency)
    14. in018_powerbi.py             DB -> Power BI hand-off tables
    15. in019_report_experience.py   DB -> report experience contract
    16. in020_regulatory_context.py  DB -> regulatory context outputs
    17. in021_headroom_trajectory.py DB -> headroom trajectory output
    18. review_trend_selection.py    DB -> in004_selection_review.md
       (needs annual_metrics from step 1)
    19. in040_risk_metrics.py        DB -> in040_risk_metrics.json
       (needs annual_metrics from step 1; kept fresh for consumers other
       than build_deliverable.py, which reads the DB directly - see below)
    20. in041_spend_metrics.py       DB -> in041_spend_metrics.json
       (same freshness note as in040_risk_metrics.py above)
    21. build_deliverable.py         DB -> deliverable/*.html
       (needs steps 1-3; reads research/insights.db directly via
       in040_risk_metrics.py's and in041_spend_metrics.py's payload
       builders, in-process - never depends on steps 19-20's JSON files
       staying fresh, only on their functions)
    22. build_in006_pdf.py            DB -> uk_bank_insights.pdf
       (needs steps 1-3; per IN-053, mirrors deliverable/comparison.html's
       own sections via headless-Chromium print-to-PDF (Playwright) instead
       of in011_deliverables.py's older hand-rolled PDF writer - see
       wayfinder/insights/tickets/IN-053.md)

Each step runs as a subprocess (not an in-process import) so a script's own
argparse/CLI behavior is exercised exactly as a human running it by hand
would see, and so one step's module-level state can't leak into the next.

build_in005_prototype.py (the older single-file uk_bank_insights.html
dashboard) deliberately isn't in this list any more - deliverable/ built by
build_deliverable.py is now the production HTML deliverable, per
wayfinder/insights/tickets/IN-051.md. build_in005_prototype.py and its
underlying in011_deliverables.py sections stay in the codebase (still
runnable standalone, kept per the grilled decision in
wayfinder/insights/tickets/IN-053.md) even though build_in006_pdf.py no
longer depends on them as of that ticket's rewrite.
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts" / "insights"

STEPS = [
    "extract_metrics.py",
    "export_parent_group_tables.py",
    "cluster_banks.py",
    "analyze_trends.py",
    "in009_analysis.py",
    "in010_parent_groups.py",
    "in012_absolute_analysis.py",
    "in022_ratio_decomposition.py",
    "in016_distribution.py",
    "in017_quality.py",
    "in023_distribution_visuals.py",
    "in024_trajectory.py",
    "in025_quality_views.py",
    "in018_powerbi.py",
    "in019_report_experience.py",
    "in020_regulatory_context.py",
    "in021_headroom_trajectory.py",
    "review_trend_selection.py",
    "in040_risk_metrics.py",
    "in041_spend_metrics.py",
    "build_deliverable.py",
    "build_in006_pdf.py",
]


def run_steps(steps, scripts_dir, root, stop_after=None):
    """The actual stop-on-failure orchestration loop, factored out of
    main() so it's unit-testable against a temp directory of dummy scripts
    without touching the real research/ files or subprocess-mocking
    main()'s own argument parsing. Returns the process exit code that
    should be used (0 for success, the failing step's exit code otherwise).
    `steps` is a list of script filenames run in order from `scripts_dir`,
    each invoked as `python3 <scripts_dir>/<step>` with cwd=`root`."""
    ran = []
    for name in steps:
        print(f"\n=== {name} ===")
        result = subprocess.run([sys.executable, str(Path(scripts_dir) / name)], cwd=root, text=True)
        ran.append(name)
        if result.returncode != 0:
            print(f"\n!! {name} failed (exit {result.returncode}) - stopping here. "
                  f"Nothing after this step ran, so no output was generated from "
                  f"stale or partially-refreshed upstream data.", file=sys.stderr)
            return result.returncode, ran

        if stop_after == name:
            print(f"\nStopped after {name} as requested (--stop-after).")
            return 0, ran

    print("\nAll refresh steps completed successfully.")
    return 0, ran


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--stop-after", default=None, choices=STEPS,
                         help="stop after this step - useful to refresh the DB/CSVs "
                              "without regenerating the client deliverables")
    args = parser.parse_args()

    exit_code, _ran = run_steps(STEPS, SCRIPTS, ROOT, stop_after=args.stop_after)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
