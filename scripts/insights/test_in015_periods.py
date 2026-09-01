import tempfile
import unittest
from pathlib import Path

import openpyxl

from extract_metrics import extract_interim_sheet
from analysis_queries import AnalysisQueries
import build_insights_db
from in009_analysis import normalize_observation, normalize_period


class In015PeriodTests(unittest.TestCase):
    def test_common_interim_periods_are_typed_and_not_annual(self):
        cases = {
            "2025 Q3": ("quarterly", 2025, 3, "2025-09-30"),
            "2025-Q1": ("quarterly", 2025, 3, "2025-03-31"),
            "2025 H1": ("semi_annual", 2025, 6, "2025-06-30"),
            "31 March 2022": ("point_in_time", 2022, None, "2022-03-31"),
            "Sep-25": ("point_in_time", 2025, None, "2025-09-30"),
            "2025-09-30": ("point_in_time", 2025, None, "2025-09-30"),
            "H1 2025": ("semi_annual", 2025, 6, "2025-06-30"),
        }
        for period, expected in cases.items():
            with self.subTest(period=period):
                actual = normalize_period(period)
                self.assertEqual(
                    (actual["period_type"], actual["fiscal_year"], actual["period_length_months"], actual["period_end"]),
                    expected,
                )
                self.assertFalse(actual["annual_eligible"])

    def test_annual_qualified_period_remains_annual_but_long_period_is_excluded(self):
        self.assertEqual(normalize_period("FY2025*")["period_type"], "annual")
        self.assertTrue(normalize_period("FY2025*")["annual_eligible"])
        self.assertFalse(normalize_period("FY2023 (15m)")["annual_eligible"])

    def test_observation_exposes_period_metadata_to_existing_consumers(self):
        observation = normalize_observation({"year": "2025 H1", "value_raw": "15%", "value_numeric": "15", "is_numeric": "1"})
        self.assertEqual(observation["period_type"], "semi_annual")
        self.assertFalse(observation["annual_eligible"])

    def test_interim_sheet_extracts_metric_unit_basis_and_raw_period(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "interim.xlsx"
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Interim Pillar 3"
            sheet.append(["Title"])
            sheet.append(["Entity-level interim disclosures"])
            sheet.append([])
            sheet.append(["Metric", "Unit", "Basis", "2025 Q3", "2025 H1"])
            sheet.append(["CET1 capital", "£m", "Bank solo basis", 100, 98])
            sheet.append(["CET1 ratio", "%", "Bank solo basis", "15.2%", "14.9%"])
            workbook.save(path)
            workbook.close()

            workbook = openpyxl.load_workbook(path, data_only=True)
            rows, warning = extract_interim_sheet(workbook.active)
            workbook.close()

        self.assertIsNone(warning)
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0]["period"], "2025 Q3")
        self.assertEqual(rows[0]["unit"], "£m")
        self.assertEqual(rows[0]["basis"], "Bank solo basis")
        self.assertEqual(rows[-1]["value"], "14.9%")

    def test_interim_domain_is_separate_from_annual_metrics(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "insights.db"
            conn = build_insights_db.connect(db_path)
            conn.execute("INSERT INTO banks (frn, canonical_name, filename_bank_name, source_workbook, workbook_kind) VALUES (1, 'Alpha', 'ALPHA', 'ALPHA.xlsx', 'full')")
            build_insights_db.write_interim_observations(conn, [{
                "frn": 1, "source_workbook": "ALPHA.xlsx", "source_sheet": "Interim Pillar 3",
                "source_cell": "D5", "row_label_raw": "CET1 ratio", "metric_key": "ratio.cet1",
                "normalization_status": "mapped", "unit_raw": "%", "basis_raw": "Bank solo",
                "reporting_basis": "entity", "period_label_raw": "2025 Q3", "period_type": "quarterly",
                "period_end_date": "2025-09-30", "period_precision": "inferred_or_unknown",
                "period_end_year": 2025, "period_end_month": 9, "period_sequence": None,
                "period_length_months": 3, "annual_status": "interim", "value_raw": "15%",
                "value_numeric": 15.0, "is_numeric": 1, "sheet_note": None,
            }], [])
            conn.close()
            query = AnalysisQueries(db_path)
            self.assertEqual(len(query.interim_observations(numeric_only=True)), 1)
            self.assertEqual(query.interim_coverage()["observations"], 1)
            conn = build_insights_db.connect(db_path)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM annual_metrics").fetchone()[0], 0)
            conn.close()


if __name__ == "__main__":
    unittest.main()
