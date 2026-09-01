import os
import tempfile
import unittest

import build_insights_db
from in025_quality_views import cadence_summary, classify_quality, trace_completeness
from in011_deliverables import render_html_analysis, render_pdf_analysis_lines


class QualityViewTests(unittest.TestCase):
    def test_quality_keeps_non_numeric_distinct_from_missing_and_flags_basis_unit(self):
        self.assertEqual(classify_quality({"value_status": "missing"}), "missing")
        self.assertEqual(classify_quality({"value_status": "non_numeric_disclosure"}), "non_numeric")
        self.assertEqual(classify_quality({"value_status": "numeric", "reporting_basis": None, "unit": "%"}), "numeric_unknown_basis")
        self.assertEqual(classify_quality({"value_status": "numeric", "reporting_basis": "entity", "unit": None}), "numeric_unknown_unit")

    def test_cadence_summary_separates_annual_and_interim_domains(self):
        rows = [
            {"source_domain": "annual", "period_type": "annual", "value_status": "numeric"},
            {"source_domain": "annual", "period_type": "annual", "value_status": "missing"},
            {"source_domain": "interim", "period_type": "quarterly", "value_status": "numeric"},
            {"source_domain": "interim", "period_type": "point_in_time", "value_status": "non_numeric_disclosure"},
        ]
        result = cadence_summary(rows)
        self.assertEqual(result["annual"]["period_types"], {"annual": 2})
        self.assertEqual(result["annual"]["quality_states"]["missing"], 1)
        self.assertEqual(result["interim"]["period_types"], {"point_in_time": 1, "quarterly": 1})
        self.assertEqual(result["interim"]["quality_states"]["non_numeric"], 1)

    def test_trace_completeness_reports_missing_fields_without_dropping_row(self):
        result = trace_completeness([{"frn": "1", "source_workbook": "A.xlsx", "row_label": "CET1"}], ["frn", "source_workbook", "row_label", "value_raw"])
        self.assertEqual(result["rows"], 1)
        self.assertEqual(result["complete_rows"], 0)
        self.assertEqual(result["missing_fields"], {"value_raw": 1})

    def test_sqlite_join_check_detects_no_orphan_source_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            db = os.path.join(directory, "quality.db")
            conn = build_insights_db.connect(db)
            conn.execute("INSERT INTO banks (frn, canonical_name, filename_bank_name, source_workbook, workbook_kind) VALUES (1, 'Alpha', 'ALPHA', 'ALPHA.xlsx', 'full')")
            conn.execute("INSERT INTO annual_metrics (frn, sheet, row_label, year, value_raw, value_numeric, is_numeric) VALUES (1, 'CET1 Ratio', 'CET1', 'FY2025', '10%', 10, 1)")
            conn.commit()
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM annual_metrics m LEFT JOIN banks b ON b.frn=m.frn WHERE b.frn IS NULL").fetchone()[0], 0)
            conn.close()

    def test_quality_views_expose_searchable_trace_and_pdf_summary(self):
        payload = {"in009": {"metadata": {"metrics": []}, "coverage": {}, "outliers": {"broad": [], "strict": []}},
                   "in010": {"parent_groups": {}},
                   "in025": {"coverage": {"banks": 1, "metrics": ["CET1 Ratio"], "years": [2025],
                                           "cells": [{"frn": "1", "bank": "Alpha", "metric": "CET1 Ratio", "year": 2025, "state": "numeric_unknown_basis", "display_value": "10%", "n": 1, "flags": ["unknown_basis"]}]},
                             "cadence": {"annual": {"banks": 1, "observations": 1, "period_types": {"annual": 1}, "quality_states": {"numeric_unknown_basis": 1}},
                                         "interim": {"banks": 0, "observations": 0, "period_types": {}, "quality_states": {}}},
                             "trace_completeness": {"rows": 1, "complete_rows": 1},
                             "join_checks": {"annual_orphan_rows": 0, "interim_orphan_rows": 0},
                             "trace": [{"frn": "1", "source_workbook": "A.xlsx", "sheet": "CET1 Ratio", "row_label": "CET1", "year": "FY2025", "value_raw": "10%", "unit": "%", "reporting_basis": "", "quality_status": "numeric_unknown_basis"}]}}
        html = render_html_analysis(payload)
        self.assertIn("Source quality and disclosure coverage", html)
        self.assertIn('id="in025-filter"', html)
        self.assertIn("Searchable source trace", html)
        self.assertIn('>10%</td>', html)
        self.assertIn('<th>FY2020</th>', html)
        self.assertIn('<th>FY2026</th>', html)
        self.assertIn('>N/A</td>', html)
        self.assertNotIn('>TEXT</td>', html)
        self.assertNotIn('>UNIT?</td>', html)
        self.assertNotIn('>BASIS?</td>', html)
        lines = render_pdf_analysis_lines(payload)
        self.assertIn("Source quality and disclosure coverage", lines)


if __name__ == "__main__":
    unittest.main()
