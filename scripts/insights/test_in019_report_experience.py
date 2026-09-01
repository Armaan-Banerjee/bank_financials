import os
import tempfile
import unittest

import build_insights_db
from in019_report_experience import build_report_experience, export_report_experience


class In019ReportExperienceTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmpdir.name, "model.db")
        conn = build_insights_db.connect(self.db)
        rows = [{"bank": "BANK1", "canonical_bank": "Bank 1", "source_filename_bank": "BANK1",
                 "source_workbook": "BANK1.xlsx", "frn": "1", "workbook_kind": "full",
                 "sheet": "CET1 Ratio", "row_label": "CET1 ratio", "year": "FY2025",
                 "value_raw": "10", "value_numeric": "10", "is_numeric": "1", "basis_note": "entity",
                 "unit": "%", "reporting_basis": "entity", "restatement_note": "", "source_note": "Annual report"}]
        build_insights_db.write_banks_and_metrics(conn, rows, metrics_source="test")
        conn.close()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_pages_define_denominators_and_filters(self):
        report = build_report_experience(self.db)
        self.assertEqual({page["id"] for page in report["pages"]}, {"executive", "comparability", "investigate", "scale"})
        visuals = [visual for page in report["pages"] for visual in page["visuals"]]
        self.assertTrue(all(visual["denominator"] and visual["comparability_filter"] for visual in visuals))
        self.assertIn("non-causal", report["governance"]["non_causal_warning"])

    def test_export_writes_report_and_findings(self):
        out = os.path.join(self.tmpdir.name, "powerbi")
        report, findings = export_report_experience(self.db, out)
        self.assertTrue(os.path.exists(os.path.join(out, "report_experience.json")))
        self.assertTrue(os.path.exists(os.path.join(out, "finding_detail.csv")))
        self.assertEqual(report["drillthrough"]["required_fields"], ["bank_id", "metric_id", "period_id"])
        self.assertIsInstance(findings, list)


if __name__ == "__main__":
    unittest.main()
