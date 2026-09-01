# Insights pipeline test report

Date: 2026-08-29

This report records automated coverage for IN-007/IN-008 and the final
deliverables. Tests use temporary databases and output files; the live
database, workbooks, research exports, and deliverables are not overwritten.

## Unit coverage

`python3 -m unittest discover -s scripts/insights -p 'test*.py'`

- Metric parsing: percentages, plain numbers, missing values, duplicate rows,
  conflicting duplicates, and missing-year behavior.
- FRN identity: sibling entities remain distinct and FRN is preferred to bank
  display names.
- Trend selection: preferred labels, exact fiscal-year periods, collisions,
  basis diagnostics, and cash-flow total selection.
- Database round-trips: raw/numeric/missing-value fidelity, metadata columns,
  effective dates, parent-group retention, and duplicate-key failures.
- Cluster input parity: DB and CSV row shape and feature-matrix equivalence.

## Integration coverage

`python3 scripts/insights/test_pipeline.py`

- Clean CSV/Markdown -> SQLite rebuild and schema validation.
- SQLite -> CSV byte parity.
- SQLite-vs-CSV clustering parity, including centroids and k-sweep outputs.
- Database-backed trend analysis and exception-report generation.
- Parent-group export idempotence, inode preservation on no-op, and
  hand-authored Markdown prose preservation.
- HTML payload shape, bank count, metric count, and generated JavaScript
  syntax.
- PDF header/EOF validity and `qpdf --check` when qpdf is installed.

## End-to-end coverage

The pipeline test runs `scripts/insights/extract_metrics.py` across the actual workbook
directory into a temporary database and CSV, confirming:

- 145 workbooks processed.
- 145 unique FRNs.
- 12,846 annual metric rows.
- Zero unmatched FRNs.
- Zero workbook processing failures.
- Temporary extraction CSV byte-identical to the current generated export.
- Parent map import produces 145 lookup rows and 36 typed edges.

## Result

31 tests pass. Python compilation passes for all scripts. SQLite integrity
checks pass, and the generated PDF passes `qpdf --check`.
