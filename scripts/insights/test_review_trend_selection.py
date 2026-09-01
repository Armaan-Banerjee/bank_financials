"""
Tests for scripts/review_trend_selection.py - previously zero coverage for
this entire file. Only ever exercised via the live 145-bank pipeline run,
which proves the script doesn't crash but says nothing about whether
collision_rows() actually flags the right rows (and only the right rows).
"""

import csv
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from analyze_trends import METRICS
from review_trend_selection import collision_rows
import build_insights_db


def row(frn, sheet, label, year, value="10", is_numeric="1"):
    return {"frn": str(frn), "sheet": sheet, "row_label": label, "year": year,
            "value_numeric": value, "is_numeric": is_numeric, "basis_note": ""}


class CollisionRows(unittest.TestCase):
    def setUp(self):
        self.spec = METRICS["Leverage ratio"]  # (sheet, pattern, excluded-words)

    def test_two_distinct_labels_same_frn_same_year_is_a_collision(self):
        rows = [
            row(1, "Leverage Ratio", "Leverage ratio excluding claims on central banks (%)", "FY2025"),
            row(1, "Leverage Ratio", "Leverage ratio including claims on central banks (%)", "FY2025"),
        ]
        collisions = collision_rows(rows, "Leverage ratio", self.spec)
        self.assertEqual(len(collisions), 1)
        self.assertIn((str(1), 2025), collisions)

    def test_same_label_repeated_is_not_a_collision(self):
        # identical (row_label, year) pair twice - e.g. an exact duplicate
        # row, not a genuine label/period variant - must not be flagged.
        rows = [
            row(1, "Leverage Ratio", "Leverage ratio excluding claims on central banks (%)", "FY2025"),
            row(1, "Leverage Ratio", "Leverage ratio excluding claims on central banks (%)", "FY2025"),
        ]
        self.assertEqual(collision_rows(rows, "Leverage ratio", self.spec), {})

    def test_different_periods_for_the_same_label_is_not_a_collision(self):
        rows = [
            row(1, "Leverage Ratio", "Leverage ratio excluding claims on central banks (%)", "FY2024"),
            row(1, "Leverage Ratio", "Leverage ratio excluding claims on central banks (%)", "FY2025"),
        ]
        self.assertEqual(collision_rows(rows, "Leverage ratio", self.spec), {})

    def test_excluded_word_row_is_never_a_collision_candidate(self):
        # METRICS["Leverage ratio"]'s excluded words include "exposure" and
        # "measure" - an absolute exposure-measure row must be filtered out
        # before collision detection even sees it, same as cluster_banks.py's
        # equivalent guard.
        rows = [
            row(1, "Leverage Ratio", "Leverage ratio total exposure measure", "FY2025"),
            row(1, "Leverage Ratio", "Leverage ratio excluding claims on central banks (%)", "FY2025"),
        ]
        collisions = collision_rows(rows, "Leverage ratio", self.spec)
        self.assertEqual(collisions, {})  # only one real candidate row survives the filter

    def test_non_numeric_row_is_excluded(self):
        rows = [
            row(1, "Leverage Ratio", "Leverage ratio excluding claims on central banks (%)", "FY2025", is_numeric="0"),
            row(1, "Leverage Ratio", "Leverage ratio including claims on central banks (%)", "FY2025"),
        ]
        self.assertEqual(collision_rows(rows, "Leverage ratio", self.spec), {})

    def test_wrong_sheet_row_is_excluded(self):
        rows = [
            row(1, "LCR", "Leverage ratio excluding claims on central banks (%)", "FY2025"),
            row(1, "Leverage Ratio", "Leverage ratio including claims on central banks (%)", "FY2025"),
        ]
        self.assertEqual(collision_rows(rows, "Leverage ratio", self.spec), {})

    def test_different_frns_do_not_collide_with_each_other(self):
        rows = [
            row(1, "Leverage Ratio", "Leverage ratio excluding claims on central banks (%)", "FY2025"),
            row(2, "Leverage Ratio", "Leverage ratio including claims on central banks (%)", "FY2025"),
        ]
        self.assertEqual(collision_rows(rows, "Leverage ratio", self.spec), {})

    def test_different_fiscal_years_for_different_labels_do_not_collide(self):
        rows = [
            row(1, "Leverage Ratio", "Leverage ratio excluding claims on central banks (%)", "FY2024"),
            row(1, "Leverage Ratio", "Leverage ratio including claims on central banks (%)", "FY2025"),
        ]
        self.assertEqual(collision_rows(rows, "Leverage ratio", self.spec), {})

    def test_three_way_collision_is_still_one_group(self):
        rows = [
            row(1, "Leverage Ratio", "Leverage ratio variant A", "FY2025"),
            row(1, "Leverage Ratio", "Leverage ratio variant B", "FY2025"),
            row(1, "Leverage Ratio", "Leverage ratio variant C", "FY2025"),
        ]
        collisions = collision_rows(rows, "Leverage ratio", self.spec)
        self.assertEqual(len(collisions), 1)
        self.assertEqual(len(collisions[(str(1), 2025)]), 3)


class MainEndToEnd(unittest.TestCase):
    """Runs the real script as a subprocess against a small temp database
    with a known, deliberately-planted collision - proves the generated
    markdown report actually reflects what collision_rows() found, not
    just that the script exits 0."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="review_trend_test_")
        self.db_path = os.path.join(self.tmpdir, "test.db")
        rows = [
            {"bank": "ALPHA", "canonical_bank": "Alpha Ltd", "source_filename_bank": "ALPHA",
             "source_workbook": "ALPHA FINANCIALS.xlsx", "frn": 111, "workbook_kind": "full",
             "sheet": "Leverage Ratio", "row_label": "Leverage ratio excluding claims on central banks (%)",
             "year": "FY2025", "value_raw": "5.2%", "value_numeric": 5.2, "is_numeric": "1", "basis_note": ""},
            {"bank": "ALPHA", "canonical_bank": "Alpha Ltd", "source_filename_bank": "ALPHA",
             "source_workbook": "ALPHA FINANCIALS.xlsx", "frn": 111, "workbook_kind": "full",
             "sheet": "Leverage Ratio", "row_label": "Leverage ratio including claims on central banks (%)",
             "year": "FY2025", "value_raw": "4.4%", "value_numeric": 4.4, "is_numeric": "1", "basis_note": ""},
        ]
        conn = build_insights_db.connect(self.db_path)
        build_insights_db.write_banks_and_metrics(conn, rows, metrics_source="test")
        conn.close()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_report_contains_the_planted_collision(self):
        script = os.path.join(os.path.dirname(__file__), "review_trend_selection.py")
        out_path = os.path.join(self.tmpdir, "report.md")
        result = subprocess.run(
            [sys.executable, script, "--db", self.db_path, "--out", out_path],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with open(out_path) as f:
            content = f.read()
        self.assertIn("Leverage ratio (1 FRN-year collisions)", content)
        self.assertIn("111", content)
        self.assertIn("excluding claims on central banks", content)
        self.assertIn("including claims on central banks", content)
        self.assertIn("Total exception groups: 1.", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
