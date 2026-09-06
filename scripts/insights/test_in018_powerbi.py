import os
import tempfile
import unittest

import build_insights_db
from in018_powerbi import _period_id, build_powerbi_model, semantic_contract


class In018PowerBiTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmpdir.name, "model.db")
        conn = build_insights_db.connect(self.db)
        rows = []
        for frn in (1, 2):
            rows.append({"bank": f"BANK{frn}", "canonical_bank": f"Bank {frn}", "source_filename_bank": f"BANK{frn}",
                         "source_workbook": f"BANK{frn}.xlsx", "frn": str(frn), "workbook_kind": "full",
                         "sheet": "CET1 Ratio", "row_label": "CET1 ratio", "year": "FY2025",
                         "value_raw": str(frn * 10), "value_numeric": str(frn * 10), "is_numeric": "1",
                         "basis_note": "entity", "unit": "%", "reporting_basis": "entity",
                         "restatement_note": "", "source_note": "Annual report"})
        build_insights_db.write_banks_and_metrics(conn, rows, metrics_source="test")
        conn.close()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_fact_has_one_row_per_source_observation_and_dimensions_are_unique(self):
        model = build_powerbi_model(self.db)
        self.assertEqual(len(model["tables"]["fact_observation"]), 2)
        self.assertEqual(len(model["tables"]["dim_bank"]), 2)
        self.assertEqual(len(model["tables"]["dim_metric"]), 1)
        fact = model["tables"]["fact_observation"][0]
        self.assertEqual(fact["quality_id"], "numeric")
        self.assertEqual(fact["period_id"], "FY2025")
        self.assertEqual(fact["source_id"], "bank1_xlsx")

    def test_contract_exposes_relationships_measures_and_rules(self):
        contract = semantic_contract()
        self.assertIn("Comparable N", contract["measures"])
        self.assertGreaterEqual(len(contract["relationships"]), 7)
        self.assertTrue(any("unit_id" in rule for rule in contract["authoring_rules"]))

    def test_dim_period_spans_the_union_when_banks_have_unequal_year_windows(self):
        """The historical-depth (HD-series) extension effort left some real
        banks with a 10+ year window against most banks' standard 5 - if
        dim_period were built from a fixed/pre-generated year range (rather
        than derived from whatever fiscal_year values are actually present),
        an extended bank's older years would either be dropped from the
        dimension entirely or produce a fact row with a dangling FK."""
        db2 = os.path.join(self.tmpdir.name, "model2.db")
        conn = build_insights_db.connect(db2)
        rows = []
        for year in range(2016, 2026):  # LONGBANK: 10 years
            rows.append({"bank": "LONGBANK", "canonical_bank": "Long Bank", "source_filename_bank": "LONGBANK",
                         "source_workbook": "LONGBANK.xlsx", "frn": "1", "workbook_kind": "full",
                         "sheet": "CET1 Ratio", "row_label": "CET1 ratio", "year": f"FY{year}",
                         "value_raw": "10%", "value_numeric": "10", "is_numeric": "1",
                         "basis_note": "entity", "unit": "%", "reporting_basis": "entity",
                         "restatement_note": "", "source_note": "Annual report"})
        for year in range(2021, 2026):  # SHORTBANK: 5 years, the standard window
            rows.append({"bank": "SHORTBANK", "canonical_bank": "Short Bank", "source_filename_bank": "SHORTBANK",
                         "source_workbook": "SHORTBANK.xlsx", "frn": "2", "workbook_kind": "full",
                         "sheet": "CET1 Ratio", "row_label": "CET1 ratio", "year": f"FY{year}",
                         "value_raw": "20%", "value_numeric": "20", "is_numeric": "1",
                         "basis_note": "entity", "unit": "%", "reporting_basis": "entity",
                         "restatement_note": "", "source_note": "Annual report"})
        build_insights_db.write_banks_and_metrics(conn, rows, metrics_source="test")
        conn.close()

        model = build_powerbi_model(db2)
        period_ids = {p["period_id"] for p in model["tables"]["dim_period"]}
        self.assertEqual(period_ids, {f"FY{y}" for y in range(2016, 2026)})

        bank_ids = {b["bank_id"] for b in model["tables"]["dim_bank"]}
        facts = model["tables"]["fact_observation"]
        self.assertEqual(len(facts), 15)  # 10 + 5, none dropped/padded
        self.assertEqual(sum(1 for f in facts if f["period_id"] not in period_ids), 0)
        self.assertEqual(sum(1 for f in facts if f["bank_id"] not in bank_ids), 0)
        long_bank_id = next(f["bank_id"] for f in facts if f["reported_year"] == "FY2016")
        self.assertEqual(sum(1 for f in facts if f["bank_id"] == long_bank_id), 10)

    def test_period_id_preserves_qualified_reporting_periods(self):
        ordinary = {"fiscal_year": 2023, "year": "FY2023"}
        fifteen_month = {"fiscal_year": 2023, "year": "FY2023 (15m)"}
        fifteen_month_spelled = {"fiscal_year": 2023, "year": "FY2023 (15mo)"}
        self.assertEqual(_period_id(ordinary), "FY2023")
        self.assertNotEqual(_period_id(fifteen_month), _period_id(fifteen_month_spelled))
        self.assertNotEqual(_period_id(ordinary), _period_id(fifteen_month))


if __name__ == "__main__":
    unittest.main()
