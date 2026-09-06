import unittest

from in011_deliverables import render_html_analysis, render_pdf_analysis_lines
from in022_ratio_decomposition import decompose_pair, fit_trend


def amount(value, unit="GBP_million", basis="entity"):
    return {
        "value_numeric": value,
        "value_status": "numeric",
        "amount_unit": unit,
        "reporting_basis": basis,
    }


def ratio(value):
    return {"value_numeric": value, "value_status": "numeric"}


class RatioDecompositionTests(unittest.TestCase):
    def test_fit_trend_returns_slope_intercept_and_r_squared(self):
        result = fit_trend([{"x": 1, "y": 2}, {"x": 2, "y": 4}, {"x": 3, "y": 6}], "x", "y")
        self.assertEqual(result["n"], 3)
        self.assertEqual(result["slope"], 2.0)
        self.assertEqual(result["intercept"], 0.0)
        self.assertEqual(result["r_squared"], 1.0)

    def test_fit_trend_suppresses_degenerate_axis(self):
        result = fit_trend([{"x": 1, "y": 2}, {"x": 1, "y": 4}], "x", "y")
        self.assertEqual(result["status"], "insufficient_variation")
        self.assertIsNone(result["r_squared"])
    def test_capital_only_movement_is_identified(self):
        result = decompose_pair(amount(100), amount(120), amount(1000), amount(1000), ratio(10), ratio(12))
        self.assertEqual(result["status"], "comparable")
        self.assertEqual(result["movement_pattern"], "capital_only")
        self.assertEqual(result["capital_change_pct"], 20.0)
        self.assertEqual(result["rwa_change_pct"], 0.0)
        self.assertEqual(result["ratio_change_pp"], 2.0)

    def test_rwa_only_movement_is_identified(self):
        result = decompose_pair(amount(100), amount(100), amount(1000), amount(1200), ratio(10), ratio(8.33))
        self.assertEqual(result["movement_pattern"], "rwa_only")
        self.assertAlmostEqual(result["rwa_change_pct"], 20.0)

    def test_both_moving_preserves_signed_relative_changes(self):
        result = decompose_pair(amount(100), amount(110), amount(1000), amount(1200), ratio(10), ratio(9.17))
        self.assertEqual(result["movement_pattern"], "both")
        self.assertEqual(result["capital_change_pct"], 10.0)
        self.assertEqual(result["rwa_change_pct"], 20.0)
        self.assertEqual(result["ratio_change_pp"], -0.83)

    def test_missing_required_observation_is_explicit(self):
        result = decompose_pair(amount(100), None, amount(1000), amount(1200), ratio(10), ratio(8.33))
        self.assertEqual(result["status"], "insufficient_data")
        self.assertEqual(result["reason"], "missing_amount_observation")

    def test_unit_mismatch_is_not_comparable(self):
        result = decompose_pair(amount(100), amount(120, unit="GBP_thousand"), amount(1000), amount(1000), ratio(10), ratio(12))
        self.assertEqual(result["status"], "incompatible")
        self.assertEqual(result["reason"], "unit_mismatch")

    def test_unknown_basis_is_allowed_broad_but_not_strict(self):
        broad = decompose_pair(amount(100, basis=None), amount(120, basis=None), amount(1000, basis=None), amount(1000, basis=None), ratio(10), ratio(12), mode="broad")
        strict = decompose_pair(amount(100, basis=None), amount(120, basis=None), amount(1000, basis=None), amount(1000, basis=None), ratio(10), ratio(12), mode="strict")
        self.assertEqual(broad["status"], "comparable")
        self.assertEqual(strict["status"], "incompatible")
        self.assertEqual(strict["reason"], "unknown_basis")


def payload():
    record = {
        "frn": "1", "bank": "Bank One", "start_year": 2023, "end_year": 2024,
        "capital_start": 100, "capital_end": 110, "rwa_start": 1000,
        "rwa_end": 1200, "latest_capital": 110, "capital_change_pct": 10.0,
        "rwa_change_pct": 20.0, "ratio_change_pp": -1.0,
        "movement_pattern": "both", "amount_unit": "GBP_million",
        "reporting_basis": "entity", "capital_source_note": "Capital source",
        "rwa_source_note": "RWA source",
    }
    return {"in009": {"metadata": {"metrics": []}, "coverage": {}, "outliers": {"broad": [], "strict": []}}, "in010": {"parent_groups": {}}, "in022": {"broad": {"start_year": 2023, "end_year": 2024, "coverage": {"candidate_banks": 1, "comparable_banks": 1, "exclusions": {}}, "records": [record]}, "strict": {"start_year": 2023, "end_year": 2024, "coverage": {"candidate_banks": 1, "comparable_banks": 1, "exclusions": {}}, "records": [record]}}}


class DecompositionDeliverableTests(unittest.TestCase):
    def test_html_contains_visual_and_accessible_table(self):
        rendered = render_html_analysis(payload())
        self.assertIn("CET1 ratio movement decomposition", rendered)
        self.assertRegex(rendered, r'<details(?: id="[^"]+")? class="card wide analysis-collapsible">')
        self.assertNotIn('<details class="card wide analysis-collapsible" open>', rendered)
        self.assertIn("Capital change (%)", rendered)
        self.assertIn('id="in022-x-axis"', rendered)
        self.assertIn('id="in022-y-axis"', rendered)
        self.assertIn("R²", rendered)
        self.assertIn("trend-line", rendered)
        self.assertIn('role="img"', rendered)
        self.assertIn("requestAnimationFrame(render)", rendered)
        self.assertIn("Bank One", rendered)
        self.assertIn("comparable N=1", rendered)

    def test_pdf_contains_decomposition_marker_and_summary(self):
        rendered = render_pdf_analysis_lines(payload())
        self.assertIn("CET1 ratio movement decomposition", "\n".join(str(item) for item in rendered))
        self.assertTrue(any(isinstance(item, dict) and item["type"] == "decomposition_chart" for item in rendered))


if __name__ == "__main__":
    unittest.main()
