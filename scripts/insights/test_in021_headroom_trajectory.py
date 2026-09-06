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

    def _row(self, year, value, frn="1", basis="standalone", unit="%", bank="Test Bank"):
        return {"bank": bank, "canonical_bank": bank, "source_filename_bank": bank,
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

    def test_context_falls_back_to_percent_in_value_raw_when_unit_column_is_unset(self):
        # `unit` is NULL for every row in the real annual_metrics table (never
        # populated at extraction time) - a bank/year whose only percentage
        # signal is the literal "%" surviving in value_raw (e.g. "15.0%")
        # must still match, not be silently dropped as "no regulatory
        # context" for every single record in the database (found via
        # IN-052's migration survey).
        context = applicable_context(
            {"unit": None, "value_raw": "15.0%", "reporting_basis": "entity"}, "CET1 Ratio", 2025
        )
        self.assertEqual(context["floor"], 7.0)

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

    def test_long_run_change_uses_each_banks_own_earliest_year_not_a_shared_one(self):
        """The historical-depth (HD-series) extension effort gave some real
        banks a 10-year window (FY2016-FY2025) against most banks' standard
        5 (FY2021-FY2025). Confirms an extended bank's long-run change is
        computed from ITS OWN earliest year (FY2016), not silently clipped
        to the other bank's shorter window, and that the short-window
        bank's own record is unaffected by its peer's longer history."""
        rows = []
        for i, year in enumerate(range(2016, 2026)):  # LONGBANK: FY2016-FY2025, values 10..19
            rows.append(self._row(f"FY{year}", 10 + i, frn="1", bank="Long Window Bank"))
        for i, year in enumerate(range(2021, 2026)):  # SHORTBANK: FY2021-FY2025, values 20..24
            rows.append(self._row(f"FY{year}", 20 + i, frn="2", bank="Short Window Bank"))
        directory, db = self._db_with_rows(rows)
        try:
            records = {r["frn"]: r for r in build_headroom_payload(db)["records"]}
            long_record = records["1"]
            short_record = records["2"]
            self.assertEqual(long_record["comparable_year_count"], 10)
            self.assertEqual(long_record["latest_year"], 2025)
            # 19 (FY2025) - 10 (FY2016) = 9, NOT 19 - 14 (a wrongly-clipped
            # FY2021 start) = 5.
            self.assertEqual(long_record["trend_change"], 9)
            self.assertEqual(long_record["trend_direction"], "increasing")

            self.assertEqual(short_record["comparable_year_count"], 5)
            self.assertEqual(short_record["latest_year"], 2025)
            # 24 (FY2025) - 20 (FY2021) = 4 - unaffected by LONGBANK's
            # extra pre-2021 years existing in the same database.
            self.assertEqual(short_record["trend_change"], 4)
        finally:
            directory.cleanup()


if __name__ == "__main__":
    unittest.main()
