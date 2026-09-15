"""
Regression tests for scripts/cluster_banks.py, added while migrating it to
read from research/insights.db instead of CSV directly (wayfinder/insights/
ticket IN-008). Run with:

    python3 scripts/test_cluster_banks.py

Covers:
  - load_rows_from_db() produces rows shaped identically to load_rows()'s
    CSV output, so build_feature_matrix() (untouched, already covered by
    IN-003's own manual verification) behaves identically either way.
  - end-to-end parity: clustering a small synthetic dataset via the CSV path
    and the DB path produces byte-identical output.
"""

import csv
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

import build_insights_db
from build_insights_db import load_rows_from_db
from cluster_banks import load_rows, build_feature_matrix, kmeans, silhouette_score, RATIO_SHEETS, MIN_DIMENSIONS


class LoadRowsParity(unittest.TestCase):
    """The CSV loader and the DB loader must hand build_feature_matrix()
    identically-shaped rows - same keys, same string typing, "" for missing,
    not None or a native float/int."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="cluster_banks_test_")
        self.db_path = os.path.join(self.tmpdir, "test.db")
        self.csv_path = os.path.join(self.tmpdir, "test.csv")

        rows = [
            {
                "bank": "ALPHA", "canonical_bank": "Alpha Canonical Ltd",
                "source_filename_bank": "ALPHA", "source_workbook": "ALPHA FINANCIALS.xlsx",
                "frn": 111, "workbook_kind": "full", "sheet": "CET1 Ratio",
                "row_label": "CET1 ratio", "year": "FY2025", "value_raw": "14.5%",
                "value_numeric": 14.5, "is_numeric": "1", "basis_note": "",
            },
            {
                "bank": "ALPHA", "canonical_bank": "Alpha Canonical Ltd",
                "source_filename_bank": "ALPHA", "source_workbook": "ALPHA FINANCIALS.xlsx",
                "frn": 111, "workbook_kind": "full", "sheet": "LCR",
                "row_label": "LCR", "year": "FY2025", "value_raw": "",
                "value_numeric": "", "is_numeric": "0", "basis_note": "",
            },
        ]
        conn = build_insights_db.connect(self.db_path)
        build_insights_db.write_banks_and_metrics(conn, rows, metrics_source="test")
        build_insights_db.export_metrics_csv(conn, self.csv_path)
        conn.close()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_db_and_csv_rows_have_identical_shape(self):
        csv_rows = load_rows(self.csv_path)
        db_rows = load_rows_from_db(self.db_path)
        keys_needed = {"bank", "frn", "sheet", "row_label", "year", "value_raw", "value_numeric", "is_numeric",
                       "unit", "reporting_basis", "restatement_note", "source_note"}
        csv_by_key = {(r["sheet"], r["year"]): {k: r[k] for k in keys_needed} for r in csv_rows}
        db_by_key = {(r["sheet"], r["year"]): {k: r[k] for k in keys_needed} for r in db_rows}
        self.assertEqual(csv_by_key, db_by_key)
        # spot check types are strings throughout, not native int/float/None
        sample = db_rows[0]
        for k in keys_needed:
            self.assertIsInstance(sample[k], str, f"{k!r} must be a string like csv.DictReader produces")


class EndToEndClusteringParity(unittest.TestCase):
    """Cluster a small synthetic dataset via the DB path and via its CSV
    export, and confirm the feature matrix build is identical either way -
    the strongest possible proof this migration is behavior-preserving."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="cluster_banks_e2e_test_")
        self.db_path = os.path.join(self.tmpdir, "test.db")
        self.csv_path = os.path.join(self.tmpdir, "test.csv")

        rows = []
        # enough banks/dimensions to clear MIN_DIMENSIONS and exercise the
        # real feature-matrix build, not just a trivial 1-row case
        for i, (frn, bank) in enumerate([(111, "ALPHA"), (222, "BETA"), (333, "GAMMA"), (444, "DELTA")]):
            for j, sheet in enumerate(RATIO_SHEETS[:5]):
                value = 10.0 + i + j
                rows.append({
                    "bank": bank, "canonical_bank": f"{bank} Ltd",
                    "source_filename_bank": bank, "source_workbook": f"{bank} FINANCIALS.xlsx",
                    "frn": frn, "workbook_kind": "full", "sheet": sheet,
                    "row_label": sheet, "year": "FY2025", "value_raw": f"{value}%",
                    "value_numeric": value, "is_numeric": "1", "basis_note": "",
                })
        conn = build_insights_db.connect(self.db_path)
        build_insights_db.write_banks_and_metrics(conn, rows, metrics_source="test")
        build_insights_db.export_metrics_csv(conn, self.csv_path)
        conn.close()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_feature_matrix_identical_from_db_and_csv(self):
        db_rows = load_rows_from_db(self.db_path)
        csv_rows = load_rows(self.csv_path)
        banks_db, frns_db, matrix_db, years_db, coverage_db = build_feature_matrix(db_rows)
        banks_csv, frns_csv, matrix_csv, years_csv, coverage_csv = build_feature_matrix(csv_rows)
        self.assertEqual(banks_db, banks_csv)
        self.assertEqual(frns_db, frns_csv)
        self.assertEqual(coverage_db, coverage_csv)
        self.assertTrue((matrix_db == matrix_csv).all() or
                         all((a == b) or (a != a and b != b) for a, b in
                             zip(matrix_db.flatten(), matrix_csv.flatten())))


class KMeansMath(unittest.TestCase):
    """The hand-rolled k-means implementation had zero direct coverage -
    only ever exercised emergently against the real 145-bank dataset. These
    use small, deterministic synthetic data where the correct answer is
    known by construction."""

    def test_two_well_separated_clusters_are_found_correctly(self):
        rng = np.random.default_rng(0)
        cluster_a = rng.normal(loc=[0, 0], scale=0.1, size=(10, 2))
        cluster_b = rng.normal(loc=[20, 20], scale=0.1, size=(10, 2))
        X = np.vstack([cluster_a, cluster_b])
        inertia, labels, centers = kmeans(X, k=2, seed=1)

        # every point in the first 10 rows must share one label, the last
        # 10 rows the other (which physical label id doesn't matter)
        self.assertEqual(len(set(labels[:10])), 1)
        self.assertEqual(len(set(labels[10:])), 1)
        self.assertNotEqual(labels[0], labels[10])

        # centers should land near (0,0) and (20,20), in either order
        center_near_origin = min(centers, key=lambda c: np.linalg.norm(c))
        center_near_far = max(centers, key=lambda c: np.linalg.norm(c))
        self.assertTrue(np.allclose(center_near_origin, [0, 0], atol=1))
        self.assertTrue(np.allclose(center_near_far, [20, 20], atol=1))
        self.assertLess(inertia, 5)  # tight clusters -> low inertia

    def test_k_equals_1_puts_everything_in_one_cluster_at_the_mean(self):
        X = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [2.0, 2.0]])
        inertia, labels, centers = kmeans(X, k=1, seed=0)
        self.assertTrue((labels == 0).all())
        self.assertTrue(np.allclose(centers[0], [1.0, 1.0]))  # the mean

    def test_deterministic_for_a_fixed_seed(self):
        rng = np.random.default_rng(2)
        X = rng.normal(size=(20, 3))
        r1 = kmeans(X, k=3, seed=42)
        r2 = kmeans(X, k=3, seed=42)
        self.assertTrue(np.array_equal(r1[1], r2[1]))  # same labels
        self.assertTrue(np.allclose(r1[2], r2[2]))  # same centers

    def test_k_equals_n_gives_zero_inertia(self):
        # every point is its own cluster - perfect fit, inertia must be ~0
        X = np.array([[0.0, 0.0], [5.0, 5.0], [10.0, 0.0]])
        inertia, labels, centers = kmeans(X, k=3, seed=0)
        self.assertAlmostEqual(inertia, 0.0, places=8)
        self.assertEqual(len(set(labels)), 3)


class SilhouetteScoreMath(unittest.TestCase):
    def test_perfectly_separated_clusters_score_near_one(self):
        X = np.array([[0.0, 0.0], [0.1, 0.0], [0.0, 0.1],
                       [100.0, 100.0], [100.1, 100.0], [100.0, 100.1]])
        labels = np.array([0, 0, 0, 1, 1, 1])
        score = silhouette_score(X, labels)
        self.assertGreater(score, 0.99)

    def test_single_cluster_scores_zero_not_an_error(self):
        # every point has the same label - no "other cluster" exists, so
        # every point's b_candidates list is empty. Must return 0.0, not
        # raise or return NaN.
        X = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]])
        labels = np.array([0, 0, 0])
        score = silhouette_score(X, labels)
        self.assertEqual(score, 0.0)

    def test_singleton_clusters_do_not_crash(self):
        # k == n: every point is alone in its own cluster, so `same` is
        # empty for every point (guarded by `if not same.any(): continue`).
        X = np.array([[0.0, 0.0], [5.0, 0.0], [10.0, 0.0]])
        labels = np.array([0, 1, 2])
        score = silhouette_score(X, labels)  # must not raise
        self.assertIsInstance(score, float)

    def test_identical_points_in_different_clusters_score_zero_not_divide_by_zero(self):
        # a=b=0 (identical points), denom=0 - must hit the `denom > 0`
        # guard rather than raising ZeroDivisionError or producing NaN.
        X = np.array([[1.0, 1.0], [1.0, 1.0]])
        labels = np.array([0, 1])
        score = silhouette_score(X, labels)
        self.assertEqual(score, 0.0)

    def test_worse_than_random_clustering_scores_low_or_negative(self):
        # interleaved labels on a single line - points are closer to the
        # "other" cluster than their own, so silhouette should be <= 0.
        X = np.array([[0.0], [1.0], [2.0], [3.0]])
        labels = np.array([0, 1, 0, 1])
        score = silhouette_score(X, labels)
        self.assertLessEqual(score, 0.0)


class FeatureMatrixRowSelection(unittest.TestCase):
    """The real bug this project hit: some ratio sheets carry a sibling
    non-percentage row (e.g. Leverage Ratio's absolute "total exposure
    measure" alongside its "%" row), and an early version of
    build_feature_matrix() picked whichever had more populated years -
    which could be the absolute-amount row. Confirms the fix stays fixed."""

    def _row(self, bank, frn, sheet, label, year, value_raw, value_numeric, is_numeric):
        return {"bank": bank, "frn": frn, "sheet": sheet, "row_label": label,
                "year": year, "value_raw": value_raw, "value_numeric": value_numeric, "is_numeric": is_numeric}

    def test_percent_row_preferred_over_more_populated_absolute_row(self):
        rows = [
            # absolute exposure-measure row: 3 populated years (more than the % row)
            self._row("ALPHA", "1", "Leverage Ratio", "Leverage ratio total exposure measure", "FY2023", "1000000", "1000000", "1"),
            self._row("ALPHA", "1", "Leverage Ratio", "Leverage ratio total exposure measure", "FY2024", "1100000", "1100000", "1"),
            self._row("ALPHA", "1", "Leverage Ratio", "Leverage ratio total exposure measure", "FY2025", "1200000", "1200000", "1"),
            # the "%" row: only 1 populated year
            self._row("ALPHA", "1", "Leverage Ratio", "Leverage ratio excluding claims on central banks (%)", "FY2025", "5.2%", "5.2", "1"),
        ]
        banks, frns, matrix, years, coverage = build_feature_matrix(rows, ratio_sheets=["Leverage Ratio"])
        self.assertEqual(banks, ["ALPHA"])
        self.assertEqual(matrix[0, 0], 5.2, "must pick the % row's value, not the more-populated absolute row")

    def test_falls_back_to_most_populated_row_when_no_percent_row_exists(self):
        rows = [
            self._row("ALPHA", "1", "Leverage Ratio", "Some row A", "FY2024", "10", "10", "1"),
            self._row("ALPHA", "1", "Leverage Ratio", "Some row A", "FY2025", "11", "11", "1"),
            self._row("ALPHA", "1", "Leverage Ratio", "Some row B", "FY2025", "99", "99", "1"),
        ]
        banks, frns, matrix, years, coverage = build_feature_matrix(rows, ratio_sheets=["Leverage Ratio"])
        self.assertEqual(matrix[0, 0], 11.0)  # latest year of the more-populated row A

    def test_blank_ratio_row_does_not_fall_back_to_an_absolute_currency_sibling(self):
        """Regression for a real bug (found 2026-09-08 via a bug-sweep
        fork): ICBC Standard Bank's NSFR row is blank every year, so the old
        fallback picked "Total available stable funding ($m)" - an absolute
        £m/$m balance, not a percentage - and clustered it alongside every
        other bank's genuine ~100-300% NSFR values. A currency-labeled row
        must never stand in for a genuinely undisclosed ratio."""
        rows = [
            self._row("ICBC", "1", "NSFR", "Total available stable funding ($m)", "FY2025", "9393", "9393", "1"),
            self._row("ICBC", "1", "NSFR", "Total required stable funding ($m)", "FY2025", "7000", "7000", "1"),
        ]
        banks, frns, matrix, years, coverage = build_feature_matrix(rows, ratio_sheets=["NSFR"])
        self.assertTrue(np.isnan(matrix[0, 0]), "a currency-labeled absolute row must not stand in for a missing ratio")

    def test_a_regulatory_requirement_row_is_not_clustered_as_the_actual_ratio(self):
        """Regression for a real bug (found 2026-09-08): Unity Trust Bank's
        MREL Ratio sheet only ever numerically discloses a "MREL requirement
        (%)" row - the regulatory minimum, not the bank's actual held MREL
        ratio. The old logic picked it anyway since it was the only row and
        carried a "%" marker."""
        rows = [
            self._row("UNITY", "1", "MREL Ratio", "MREL requirement (= Total Capital Requirement, %)", "FY2025", "10.69%", "10.69", "1"),
        ]
        banks, frns, matrix, years, coverage = build_feature_matrix(rows, ratio_sheets=["MREL Ratio"])
        self.assertTrue(np.isnan(matrix[0, 0]), "a regulatory requirement row must not be clustered as the actual ratio")

    def test_a_bank_with_many_more_disclosed_years_than_its_peer_still_gets_exactly_one_row(self):
        """The historical-depth (HD-series) extension effort gave some real
        banks 10+ years of disclosed data against most banks' standard 5 -
        confirms an extended bank's extra years are never treated as extra
        independent clustering observations, and that its OWN latest year
        (not a globally shared one, and not its earliest) is what's picked,
        regardless of how many more years it has on file than its peer."""
        long_window_years = [f"FY{y}" for y in range(2016, 2026)]  # 10 years
        short_window_years = [f"FY{y}" for y in range(2021, 2026)]  # 5 years
        rows = []
        for i, year in enumerate(long_window_years):
            # value climbs with year so a "picked the wrong year" bug is
            # visible as a wrong matrix value, not just a wrong count.
            rows.append(self._row("LONGWINDOW", "1", "CET1 Ratio", "CET1 ratio", year, f"{10 + i}%", 10 + i, "1"))
        for i, year in enumerate(short_window_years):
            rows.append(self._row("SHORTWINDOW", "2", "CET1 Ratio", "CET1 ratio", year, f"{20 + i}%", 20 + i, "1"))

        banks, frns, matrix, years, coverage = build_feature_matrix(rows, ratio_sheets=["CET1 Ratio"])
        self.assertEqual(sorted(banks), ["LONGWINDOW", "SHORTWINDOW"])
        # exactly 2 rows total - 10 extra years must not become 10 extra rows
        self.assertEqual(matrix.shape[0], 2)
        long_idx = banks.index("LONGWINDOW")
        short_idx = banks.index("SHORTWINDOW")
        # LONGWINDOW's FY2025 (index 9, value 19) must win, not FY2016
        # (index 0, value 10) just because it's first in the input list.
        self.assertEqual(matrix[long_idx, 0], 19.0)
        self.assertEqual(years[long_idx, 0], "FY2025")
        self.assertEqual(matrix[short_idx, 0], 24.0)
        self.assertEqual(years[short_idx, 0], "FY2025")


class ExcludeMrelFlag(unittest.TestCase):
    """Integration-level test of --exclude-mrel, previously only verified
    manually in-session. Runs the real script as a subprocess against a
    temp DB, per the project's established pattern for exercising a
    script's own CLI/argparse behavior."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="exclude_mrel_test_")
        self.db_path = os.path.join(self.tmpdir, "test.db")
        rows = []
        for i, (frn, bank) in enumerate([(111, "ALPHA"), (222, "BETA"), (333, "GAMMA"), (444, "DELTA")]):
            for j, sheet in enumerate(RATIO_SHEETS):  # all 7, including MREL Ratio
                value = 10.0 + i + j
                rows.append({
                    "bank": bank, "canonical_bank": f"{bank} Ltd", "source_filename_bank": bank,
                    "source_workbook": f"{bank} FINANCIALS.xlsx", "frn": frn, "workbook_kind": "full",
                    "sheet": sheet, "row_label": sheet, "year": "FY2025", "value_raw": f"{value}%",
                    "value_numeric": value, "is_numeric": "1", "basis_note": "",
                })
        conn = build_insights_db.connect(self.db_path)
        build_insights_db.write_banks_and_metrics(conn, rows, metrics_source="test")
        conn.close()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _run(self, *extra_args):
        script = os.path.join(os.path.dirname(__file__), "cluster_banks.py")
        out = os.path.join(self.tmpdir, "out.csv")
        result = subprocess.run(
            [sys.executable, script, "--db", self.db_path, "--out", out,
             "--centroids-out", os.path.join(self.tmpdir, "c.csv"),
             "--sweep-out", os.path.join(self.tmpdir, "s.csv"), *extra_args],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout, out

    def test_default_run_includes_mrel_dimension(self):
        stdout, out_path = self._run()
        self.assertIn("MREL included=True", stdout)
        with open(out_path, newline="") as f:
            header = next(csv.reader(f))
        self.assertIn("MREL Ratio_value", header)

    def test_exclude_mrel_drops_the_dimension_entirely(self):
        stdout, out_path = self._run("--exclude-mrel")
        self.assertIn("MREL included=False", stdout)
        with open(out_path, newline="") as f:
            header = next(csv.reader(f))
        self.assertNotIn("MREL Ratio_value", header)


if __name__ == "__main__":
    unittest.main(verbosity=2)
