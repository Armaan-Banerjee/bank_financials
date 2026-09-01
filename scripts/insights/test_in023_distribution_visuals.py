import unittest

from in011_deliverables import render_html_analysis, render_pdf_analysis_lines
from in023_distribution_visuals import coverage_state, distribution_band


class DistributionVisualTests(unittest.TestCase):
    def test_distribution_band_uses_robust_summary_not_mean(self):
        result = distribution_band([10, 11, 12, 13, 14, 15, 16, 100])
        self.assertEqual(result["n"], 8)
        self.assertEqual(result["median"], 13.5)
        self.assertEqual(result["q1"], 11.75)
        self.assertEqual(result["q3"], 15.25)
        self.assertEqual(result["status"], "small_n")
        self.assertNotIn("mean", result)

    def test_coverage_states_distinguish_missing_and_non_numeric(self):
        self.assertEqual(coverage_state([]), "missing")
        self.assertEqual(coverage_state([{"value_status": "non_numeric_disclosure", "annual_eligible": True}]), "non_numeric")

    def test_coverage_marks_shortened_period_before_missing(self):
        rows = [{"value_status": "numeric", "annual_eligible": False, "period_type": "annual", "period_length_months": 15}]
        self.assertEqual(coverage_state(rows), "shortened_period")

    def test_unknown_basis_is_visible_on_numeric_observation(self):
        rows = [{"value_status": "numeric", "annual_eligible": True, "reporting_basis": None}]
        self.assertEqual(coverage_state(rows), "numeric_unknown_basis")

    def test_known_basis_wins_when_a_cell_has_multiple_numeric_rows(self):
        rows = [
            {"value_status": "numeric", "annual_eligible": True, "reporting_basis": None},
            {"value_status": "numeric", "annual_eligible": True, "reporting_basis": "group"},
        ]
        self.assertEqual(coverage_state(rows), "numeric")

    def test_distribution_visuals_have_accessible_html_and_pdf_fallback(self):
        # in016's distributions are a sibling of in023 in the assembled
        # payload, not nested inside it - build_in011_payload() stopped
        # embedding a full copy of in016/in017 inside in023 to avoid
        # doubling the client-facing HTML deliverable's size for no reason.
        in016 = {"distributions": {"CET1 ratio": {"broad": [{
            "fiscal_year": 2024,
            "summary": {"n": 12, "p10": 10.0, "median": 12.0, "p90": 15.0,
                        "iqr": 3.0, "mad": 1.0, "status": "coverage_only"},
        }], "strict": []}}}
        in023 = {
            "coverage": {
                "years": [2024], "metrics": ["CET1 ratio"],
                "cells": [{"frn": "1", "bank": "Example Bank", "metric": "CET1 ratio", "year": 2024, "state": "numeric"}],
                "state_counts": {"numeric": 1},
            },
        }
        base = {"in009": {"metadata": {"metrics": []}, "coverage": {}, "outliers": {"broad": [], "strict": []}},
                "in010": {"parent_groups": {}}, "in016": in016, "in023": in023}
        html = render_html_analysis(base)
        self.assertIn("Robust distributions and evidence coverage", html)
        self.assertIn("P10", html)
        self.assertIn('id="in023-coverage-filter"', html)
        self.assertIn("Bank × metric × year evidence coverage", html)
        self.assertGreater(html.index("Robust distributions and evidence coverage"), html.index("</tbody></table></div></details>"))
        pdf_lines = render_pdf_analysis_lines(base)
        self.assertIn("Robust distributions and evidence coverage", pdf_lines)
        self.assertTrue(any(isinstance(line, dict) and line["type"] == "distribution_chart" for line in pdf_lines))


if __name__ == "__main__":
    unittest.main()
