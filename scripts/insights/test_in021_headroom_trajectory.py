import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from in021_headroom_trajectory import applicable_context, build_headroom_payload


class In021HeadroomTests(unittest.TestCase):
    def _db_with_rows(self, rows):
        import tempfile
        import build_insights_db
        directory = tempfile.TemporaryDirectory()
        db = os.path.join(directory.name, "model.db")
        conn = build_insights_db.connect(db)
        build_insights_db.write_banks_and_metrics(conn, rows, "test")
        conn.close()
        return directory, db

    def _row(self, year, value, frn="1", basis="standalone", unit="%"):
        return {"bank": "Test Bank", "canonical_bank": "Test Bank", "source_filename_bank": "Test Bank",
                "source_workbook": "test.xlsx", "frn": frn, "workbook_kind": "full", "sheet": "CET1 Ratio",
                "row_label": "CET1 ratio", "year": year, "value_raw": str(value), "value_numeric": str(value),
                "is_numeric": "1", "unit": unit, "reporting_basis": None, "basis_note": basis,
                "restatement_note": "", "source_note": ""}

    def test_floor_includes_cet1_buffer(self):
        context = applicable_context({"unit": "%", "reporting_basis": "entity"}, "CET1 Ratio", 2025)
        self.assertEqual(context["minimum"], 4.5)
        self.assertEqual(context["buffer"], 2.5)
        self.assertEqual(context["floor"], 7.0)

    def test_context_requires_basis_and_unit(self):
        self.assertIsNone(applicable_context({"unit": "%"}, "CET1 Ratio", 2025))
        self.assertIsNone(applicable_context({"unit": "£", "reporting_basis": "entity"}, "CET1 Ratio", 2025))

    def test_empty_database_is_safe(self):
        import tempfile
        import build_insights_db
        with tempfile.TemporaryDirectory() as directory:
            db = os.path.join(directory, "model.db")
            conn = build_insights_db.connect(db)
            conn.close()
            payload = build_headroom_payload(db)
            self.assertEqual(payload["records"], [])

    def test_screened_record_combines_headroom_and_decline(self):
        directory, db = self._db_with_rows([self._row("FY2021", 12), self._row("FY2025", 10)])
        try:
            records = build_headroom_payload(db)["records"]
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["status"], "screened")
            self.assertEqual(records[0]["regulatory_floor"], 7.0)
            self.assertEqual(records[0]["current_headroom"], 3.0)
            self.assertEqual(records[0]["trend_direction"], "declining")
        finally:
            directory.cleanup()

    def test_matched_single_year_is_explicitly_insufficient(self):
        directory, db = self._db_with_rows([self._row("FY2025", 10)])
        try:
            self.assertEqual(build_headroom_payload(db)["records"][0]["status"], "insufficient_evidence")
        finally:
            directory.cleanup()

    def test_headroom_context_uses_same_canonical_latest_row_as_series(self):
        rows = [
            self._row("FY2024", 10),
            self._row("FY2025", 11),
            dict(self._row("FY2025", 999), row_label="Tier 1 capital available (£'000)", unit="£"),
        ]
        directory, db = self._db_with_rows(rows)
        try:
            record = build_headroom_payload(db)["records"][0]
            self.assertEqual(record["current_value"], 11.0)
            self.assertEqual(record["status"], "screened")
            self.assertEqual(record["current_headroom"], 4.0)
        finally:
            directory.cleanup()


if __name__ == "__main__":
    unittest.main()
