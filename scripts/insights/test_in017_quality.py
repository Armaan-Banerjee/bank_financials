import json
import os
import sqlite3
import tempfile
import unittest

import build_insights_db
from in017_quality import build_in017_payload


class In017QualityTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmpdir.name, "quality.db")
        conn = build_insights_db.connect(self.db)
        rows = []
        for frn in range(1, 9):
            rows.append({"bank": f"BANK{frn}", "canonical_bank": f"Bank {frn}", "source_filename_bank": f"BANK{frn}",
                         "source_workbook": f"BANK{frn}.xlsx", "frn": str(frn), "workbook_kind": "full",
                         "sheet": "CET1 Ratio", "row_label": "CET1 ratio", "year": "FY2025",
                         "value_raw": str(frn), "value_numeric": str(frn), "is_numeric": "1",
                         "basis_note": "entity", "unit": "%", "reporting_basis": "entity",
                         "restatement_note": "", "source_note": "Annual report"})
        build_insights_db.write_banks_and_metrics(conn, rows, metrics_source="test")
        conn.close()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_quality_payload_has_unique_bank_dimension_and_lineage(self):
        result = build_in017_payload(self.db)
        self.assertEqual(len(result["dimensions"]["banks"]), 8)
        self.assertEqual(len(result["lineage"]), 8)
        fact = next(item for item in result["quality_facts"] if item["metric"] == "CET1 Ratio")
        self.assertEqual(fact["numeric"], 8)
        self.assertEqual(fact["missing"], 0)
        self.assertEqual(fact["structural_status"], "ok")

    def test_structural_duplicate_is_rejected(self):
        conn = sqlite3.connect(self.db)
        conn.execute("INSERT INTO annual_metrics (frn,sheet,row_label,year,value_raw,value_numeric,is_numeric) VALUES (99,'CET1 Ratio','CET1 ratio','FY2025','9',9,1)")
        conn.commit()
        conn.close()
        with self.assertRaises(RuntimeError):
            build_in017_payload(self.db)


if __name__ == "__main__":
    unittest.main()
