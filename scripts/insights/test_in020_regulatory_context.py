import unittest

from in020_regulatory_context import build_context_payload, match_context


class In020RegulatoryContextTests(unittest.TestCase):
    def test_matching_requires_scope_and_returns_distance(self):
        # CET1 Ratio has two simultaneously-applicable 2025 records: the 4.5%
        # Pillar 1 minimum and the 2.5% buffer - distance must be against
        # their sum (7.0), not just the minimum alone (a prior bug picked one
        # arbitrary matching record and silently ignored the buffer).
        result = match_context({"metric": "CET1 Ratio", "fiscal_year": 2025, "unit": "%", "reporting_basis": "entity", "value_numeric": "10"})
        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["value"], 7.0)
        self.assertEqual(result["distance"], 3.0)
        self.assertIn("source", result)

    def test_matching_sums_minimum_and_buffer_not_first_candidate(self):
        # Regression for a real bug: match_context() used to do
        # `next(item for item in candidates if item["value"] is not None)`,
        # returning whichever CONTEXT record happened to come first in list
        # order (the 4.5% minimum) rather than minimum+buffer (7.0) - the
        # same fix in021_headroom_trajectory.py's applicable_context()
        # already applies to the identical CONTEXT table, and the two must
        # agree on what "the floor" means for the same metric/year.
        result = match_context({"metric": "CET1 Ratio", "fiscal_year": 2022, "unit": "%", "reporting_basis": "consolidated_group", "value_numeric": "12"})
        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["value"], 7.0)
        self.assertEqual(result["distance"], 5.0)

    def test_matches_when_unit_column_is_unset_but_value_raw_carries_percent(self):
        # Regression: `unit` is NULL for virtually every real row in
        # annual_metrics (never populated at extraction time) - the original
        # `observation.get("unit") != "%"` check here returned
        # "context_unavailable" for 100% of real observations, silently
        # emptying the whole observation_context.csv Power BI export. Must
        # fall back to the literal "%" surviving in value_raw, exactly like
        # in021_headroom_trajectory.py's applicable_context() already does
        # against this identical CONTEXT table.
        result = match_context({"metric": "CET1 Ratio", "fiscal_year": 2025, "value_raw": "10%", "reporting_basis": "entity", "value_numeric": "10"})
        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["value"], 7.0)

    def test_unclassified_basis_is_not_given_a_threshold(self):
        result = match_context({"metric": "CET1 Ratio", "fiscal_year": 2025, "unit": "%", "value_numeric": "10"})
        self.assertEqual(result["status"], "context_unavailable")
        self.assertIn("basis", result["reason"])

    def test_nonnumeric_disclosure_is_not_converted_to_float(self):
        result = match_context({"metric": "LCR", "fiscal_year": 2025,
                                "value_raw": "Not published", "reporting_basis": "entity",
                                "value_numeric": ""})
        self.assertEqual(result["status"], "context_unavailable")
        self.assertIn("numeric value", result["reason"])

    def test_firm_specific_mrel_is_not_treated_as_universal(self):
        result = match_context({"metric": "MREL Ratio", "fiscal_year": 2026, "unit": "%", "reporting_basis": "entity", "value_numeric": "20"})
        self.assertEqual(result["status"], "context_unavailable")
        self.assertIn("firm-specific", result["reason"])

    def test_payload_is_versioned_and_separates_context_types(self):
        payload = build_context_payload()
        self.assertEqual(payload["schema_version"], "1.0")
        self.assertTrue(any(row["context_type"] == "buffer" for row in payload["records"]))
        self.assertTrue(any(row["context_type"] == "firm_specific_requirement" for row in payload["records"]))

    def test_observation_export_records_unavailable_reason(self):
        import os
        import tempfile
        import build_insights_db
        from in020_regulatory_context import export_context
        with tempfile.TemporaryDirectory() as directory:
            db = os.path.join(directory, "model.db")
            conn = build_insights_db.connect(db)
            build_insights_db.write_banks_and_metrics(conn, [{"bank": "B", "canonical_bank": "B", "source_filename_bank": "B", "source_workbook": "B.xlsx", "frn": "1", "workbook_kind": "full", "sheet": "MREL Ratio", "row_label": "MREL", "year": "FY2025", "value_raw": "20", "value_numeric": "20", "is_numeric": "1", "unit": "%", "reporting_basis": "entity", "basis_note": "", "restatement_note": "", "source_note": ""}], metrics_source="test")
            conn.close()
            export_context(directory, db)
            with open(os.path.join(directory, "observation_context.csv"), encoding="utf-8") as handle:
                self.assertIn("no dated context record", handle.read())


if __name__ == "__main__":
    unittest.main()
