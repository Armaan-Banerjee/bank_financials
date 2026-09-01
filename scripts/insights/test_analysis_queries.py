import os
import sqlite3
import tempfile
import unittest

import build_insights_db
from analysis_queries import AnalysisQueries, load_analysis_inputs


class AnalysisQueriesTests(unittest.TestCase):
    def setUp(self):
        handle, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(handle)
        conn = build_insights_db.connect(self.db_path)
        build_insights_db.write_banks_and_metrics(conn, [
            {
                "frn": "1", "bank": "Bank 1", "canonical_bank": "Bank 1",
                "source_filename_bank": "Bank 1", "source_workbook": "bank.xlsx",
                "workbook_kind": "full", "basis_note": "Entity basis",
                "sheet": "CET1 Ratio", "row_label": "CET1 ratio", "year": "FY2024",
                "value_raw": "12%", "value_numeric": "12", "is_numeric": "1",
                "unit": "", "reporting_basis": "", "restatement_note": "", "source_note": "",
            },
            {
                "frn": "1", "bank": "Bank 1", "canonical_bank": "Bank 1",
                "source_filename_bank": "Bank 1", "source_workbook": "bank.xlsx",
                "workbook_kind": "full", "basis_note": "Entity basis",
                "sheet": "CET1 Ratio", "row_label": "CET1 ratio", "year": "FY2024 (6m)",
                "value_raw": "11%", "value_numeric": "11", "is_numeric": "1",
                "unit": "", "reporting_basis": "", "restatement_note": "", "source_note": "",
            },
        ], "test")
        conn.close()

    def tearDown(self):
        os.unlink(self.db_path)

    def test_observations_normalize_and_filter_at_one_seam(self):
        queries = AnalysisQueries(self.db_path)
        rows = queries.observations(sheet="CET1 Ratio", annual_only=True, numeric_only=True)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["fiscal_year"], 2024)
        self.assertEqual(rows[0]["value_status"], "numeric")
        self.assertFalse(rows[0]["period_qualified"])

    def test_groups_and_combined_inputs_have_stable_shapes(self):
        queries = AnalysisQueries(self.db_path)
        self.assertEqual(queries.groups(), {})
        inputs = load_analysis_inputs(self.db_path)
        self.assertEqual(set(inputs), {"observations", "groups"})
        self.assertEqual(len(inputs["observations"]), 2)

    def test_adapter_does_not_enable_writes(self):
        AnalysisQueries(self.db_path).observations()
        conn = sqlite3.connect(self.db_path)
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM annual_metrics").fetchone()[0], 2)
        conn.close()

    def test_shared_annual_and_integrity_seams(self):
        queries = AnalysisQueries(self.db_path)
        self.assertEqual(len(queries.annual_observations(numeric_only=True)), 1)
        integrity = queries.annual_integrity()
        self.assertEqual(integrity["orphan_rows"], 0)
        self.assertEqual(integrity["identity_duplicates"], 0)
        self.assertIn("annual_metrics", integrity["tables"])
        self.assertIn("annual_metrics_count", queries.refresh_metadata())


if __name__ == "__main__":
    unittest.main()
