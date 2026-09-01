import unittest

from in011_deliverables import default_bank_mix, render_html_analysis, render_pdf_analysis_lines
from in024_trajectory import _metric_rows, direction, fixed_panel_mobility, score_fingerprint


class TrajectoryTests(unittest.TestCase):
    def test_default_bank_mix_spans_large_medium_small_and_international(self):
        names = [
            "HSBC Bank Plc", "Metro Bank PLC", "Shawbrook Bank Limited", "Aldermore Bank Plc",
            "Oxbury Bank PLC", "Atom Bank PLC", "Starling Bank Limited", "Goldman Sachs International Bank",
        ]
        records = [{"bank": name, "years": [{"year": 2021, "value": 1}, {"year": 2022, "value": 2}],
                    "score": {"label": "mixed", "robust_total_change": 1}} for name in names]
        self.assertEqual(default_bank_mix(records, [2021, 2022]), set(names))

    def test_direction_preserves_missing_and_ignores_tiny_noise(self):
        self.assertEqual(direction(None), "missing")
        self.assertEqual(direction(0.001), "flat")
        self.assertEqual(direction(-0.01), "down")
        self.assertEqual(direction(0.01), "up")

    def test_persistence_requires_a_sufficient_series(self):
        result = score_fingerprint(["up", "up"])
        self.assertEqual(result["status"], "insufficient_series")
        self.assertIsNone(result["label"])

    def test_persistence_identifies_dominant_direction_and_magnitude(self):
        result = score_fingerprint(["up", "up", "down", "up"], magnitudes=[1.0, 2.0, -0.5, 3.0])
        self.assertEqual(result["status"], "eligible")
        self.assertEqual(result["label"], "persistent_up")
        self.assertEqual(result["up_changes"], 3)
        self.assertEqual(result["down_changes"], 1)
        self.assertEqual(result["persistence_score"], 0.75)
        self.assertEqual(result["total_change"], 5.5)
        self.assertEqual(result["robust_total_change"], 5.5)

    def test_ratio_row_is_preferred_over_leverage_exposure_measure(self):
        rows = [
            {"frn": "143336", "sheet": "Leverage Ratio", "fiscal_year": 2021,
             "annual_eligible": True, "value_status": "numeric", "value_numeric": 3409123,
             "value_raw": "3409123", "row_label": "Total Basel III leverage ratio measure"},
            {"frn": "143336", "sheet": "Leverage Ratio", "fiscal_year": 2021,
             "annual_eligible": True, "value_status": "numeric", "value_numeric": 5.2,
             "value_raw": "5.2%", "row_label": "Basel III leverage ratio (%)"},
        ]
        selected = _metric_rows(rows, "Leverage Ratio")
        self.assertEqual(selected[("143336", 2021)]["value_numeric"], 5.2)

    def test_fixed_panel_uses_common_basis_and_rank_one_is_highest(self):
        def row(frn, year, value, basis="entity"):
            return {"frn": frn, "sheet": "CET1 Ratio", "fiscal_year": year,
                    "annual_eligible": True, "value_status": "numeric",
                    "value_numeric": value, "value_raw": f"{value}%", "reporting_basis": basis,
                    "period_key": f"FY{year}", "row_label": "CET1 ratio"}
        rows = [row("1", 2023, 10), row("1", 2024, 20),
                row("2", 2023, 20), row("2", 2024, 10),
                row("3", 2023, 15, "group"), row("3", 2024, 16, "group")]
        panel = fixed_panel_mobility(rows, "CET1 ratio", "CET1 Ratio", [2023, 2024])[0]
        self.assertEqual(panel["reporting_basis"], "entity")
        self.assertEqual(panel["n"], 2)
        ranks = {item["frn"]: item for item in panel["records"]}
        self.assertEqual(ranks["1"]["start_rank"], 2)
        self.assertEqual(ranks["1"]["end_rank"], 1)

    def test_trajectory_visuals_expose_filter_and_pdf_table_fallback(self):
        trajectory = {"bank": "Example Bank", "frn": "1", "metric": "CET1 ratio",
                      "years": [{"year": 2020, "value": 9, "status": "numeric", "source_note": "entity basis"},
                                {"year": 2021, "value": 10, "status": "numeric", "source_note": "entity basis"},
                                 {"year": 2024, "value": 12, "status": "numeric", "source_note": "entity basis"}],
                      "changes": [{"start_year": 2023, "end_year": 2024, "change": 2, "direction": "up"}],
                      "score": {"status": "insufficient_series", "label": None, "changes": 1,
                                "persistence_score": None, "total_change": 2}}
        payload = {"in009": {"metadata": {"metrics": []}, "coverage": {},
                             "outliers": {"broad": [], "strict": []}},
                   "in010": {"parent_groups": {}},
                   "in024": {"metadata": {"minimum_changes": 3},
                             "trajectories": {"CET1 ratio": [trajectory]},
                             "rank_mobility": {"CET1 ratio": [{"status": "eligible", "n": 2,
                                                                  "start_year": 2023, "end_year": 2024,
                                                                  "records": [{"frn": "1", "start_rank": 1,
                                                                              "end_rank": 2, "rank_change": 1},
                                                                             {"frn": "2", "start_rank": 2,
                                                                              "end_rank": 1, "rank_change": -1}]}]},
                             "coverage_churn": {"CET1 ratio": []}}}
        html = render_html_analysis(payload)
        self.assertIn("Persistent trajectories and rank mobility", html)
        self.assertIn('id="in024-filter"', html)
        self.assertIn("y-axis is metric-specific percentage points", html)
        self.assertIn("persistent up: ≥75%", html)
        self.assertIn("Drag across a chart region to zoom", html)
        self.assertIn("in024-chart-layout", html)
        self.assertIn("in024-bank-list", html)
        self.assertIn("in024-tooltip", html)
        self.assertIn("in024-point", html)
        self.assertIn('class="in024-point"', html)
        self.assertIn('rx="2.25"', html)
        self.assertIn('ry=".18"', html)
        self.assertIn("Representative default mix", html)
        self.assertIn("mousemove", html)
        self.assertIn("in024-data-layer", html)
        self.assertIn("refreshDomain", html)
        self.assertIn("resetView", html)
        self.assertNotIn("svg.addEventListener('dblclick',reset)", html)
        self.assertIn("in024-brush", html)
        self.assertIn("in024-reset-zoom", html)
        self.assertIn('class="in024-bank-toggle"', html)
        self.assertIn("data-bank=", html)
        self.assertIn('class="in024-y-axis"', html)
        self.assertIn("updateYAxis", html)
        chart_section = html.split('class="grid in024-trajectories">', 1)[1].split("<h3>Direction and magnitude heatmap", 1)[0]
        self.assertIn("FY2021", chart_section)
        self.assertNotIn("FY2020", chart_section)
        self.assertNotIn("FY2026", chart_section)
        self.assertIn('vector-effect="non-scaling-stroke"', html)
        self.assertIn('data-base-stroke-width="1.8"', html)
        self.assertIn('class="in024-rank-line"', html)
        self.assertIn("setAttribute('stroke-width'", html)
        self.assertIn("Fixed-panel percentile-rank slopegraphs", html)
        lines = render_pdf_analysis_lines(payload)
        self.assertIn("Persistent trajectories and rank mobility", lines)
        self.assertTrue(any(isinstance(line, dict) and line["type"] == "trajectory_candidates" for line in lines))


if __name__ == "__main__":
    unittest.main()
