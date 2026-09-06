"""
Tests for the computed (not hardcoded) content in build_in005_prototype.py's
HTML deliverable generator. These are exactly the functions built to fix the
"hardcoded headline counts" bug (73 of 99, etc.) - without a test asserting
their output is numerically correct against a KNOWN input, a future
regression in pairwise_counts() or a metric_series() mapping would only be
caught by someone eyeballing the deliverable, which is the same failure mode
that let the original bug ship.

build_in006_pdf.py's own equivalent tests were removed here on its IN-053
rewrite (2026-09-05) - it no longer computes bullet-point text or hand-draws
PDF pages; it mirrors comparison.html's own sections via Playwright, so its
correctness now rides on build_deliverable.py's already-tested curators plus
test_pipeline.py's end-to-end PDF assertions.
"""

import csv
import os
import re
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))

import build_insights_db
from build_in005_prototype import (
    build_key_takeaways_html,
    compute_groups_payload,
    compute_trends_payload,
    GROUP_VERDICTS,
    TEMPLATE,
    decorate_dashboard_html,
)
from build_in005_prototype import escape_html


def _series(frn_to_year_values):
    """Builds the {frn: {year_int: value}} shape extract()/metric_series()
    produce, from a plain {frn: {year: value}} dict of ints."""
    return {frn: dict(years) for frn, years in frn_to_year_values.items()}


class KeyTakeawaysHtmlCorrectness(unittest.TestCase):
    """build_in005_prototype.py's HTML equivalent - same arithmetic, must
    produce the same counts as the PDF's headline_signal_lines() for the
    same underlying data (the two must never quietly disagree)."""

    def test_computed_numbers_match_hand_calculated_expectation(self):
        # trend_series uses STRING years (as build_in005_prototype.py's
        # main() converts them before calling this function)
        trend_series = {
            "RWA": {"1": {"2022": 100.0, "2023": 110.0}, "2": {"2022": 100.0, "2023": 90.0}},
            "CET1 ratio": {"1": {"2023": 20.0, "2024": 18.0}},
            "Operating cash flow": {"1": {"2023": 10.0, "2024": 20.0}},
        }
        html = build_key_takeaways_html(trend_series)
        self.assertIn("1 of 2", html)  # RWA FY2022->FY2023: 1 up of 2
        self.assertIn("Key takeaways", html)
        self.assertIn("<article", html)  # still valid-looking HTML structure


class ComputeTrendsPayload(unittest.TestCase):
    def test_only_adjacent_year_pairs_with_data_are_included(self):
        trend_series = {"CET1 ratio": {"1": {"2021": 10.0, "2022": 12.0}}}
        trends = compute_trends_payload(trend_series)
        periods = {t["period"] for t in trends}
        self.assertIn("FY2021→FY2022", periods)
        self.assertNotIn("FY2022→FY2023", periods)  # no data for that pair

    def test_empty_series_produces_no_trend_rows(self):
        self.assertEqual(compute_trends_payload({"CET1 ratio": {}}), [])


class OutputSafety(unittest.TestCase):
    def test_html_escape_covers_markup_quotes_and_ampersands(self):
        self.assertEqual(
            escape_html("<script>alert('x') & \"y\"</script>"),
            "&lt;script&gt;alert(&#39;x&#39;) &amp; &quot;y&quot;&lt;/script&gt;",
        )


class DashboardShellContract(unittest.TestCase):
    """The generated client page keeps a dashboard-style navigation shell."""

    def test_template_exposes_dashboard_navigation_and_kpi_seam(self):
        html = decorate_dashboard_html(TEMPLATE.replace("__IN011_ANALYSIS__", '<section class="grid in011-analysis"></section>'))
        self.assertIn('class="dashboard-shell"', html)
        self.assertIn('class="dashboard-sidebar"', html)
        self.assertIn('id="dashboard-kpis"', html)
        self.assertIn("Katalysis Charts 0.1.0", html)
        self.assertIn("chartjs-4.5.0", html)
        self.assertIn("chartjsVersion", html)
        self.assertIn("maintainAspectRatio:false", html)
        self.assertIn("height: 100% !important", html)
        self.assertIn("filter:(item,data)=>!data.datasets[item.datasetIndex].hidden", html)
        self.assertIn("KatalysisCharts.observe();KatalysisCharts.refresh()", html)
        self.assertIn("originalRange=originalMax-originalMin", html)
        self.assertIn("options.scales.y.min", html)
        self.assertIn("fitYAxis", html)
        self.assertIn(".in024-chart-layout{display:block;width:100%", html)
        self.assertIn('id="dashboard-chart-css"', html)
        self.assertIn(".dashboard-shell .in024-chart-layout", html)
        self.assertIn("display: block !important", html)
        self.assertIn("width:100%;align-items:center", html)
        self.assertIn("align-self:stretch", html)
        self.assertIn("pointRadius:1.8", html)
        self.assertIn("type:\"linear\"", html)
        self.assertIn('svg.style.display="none"', html)
        self.assertIn('destroy,reset,refresh', html)
        self.assertIn("KatalysisCharts", html)
        self.assertIn("KatalysisCharts.observe();KatalysisCharts.refresh()", html)
        self.assertIn("data-chart-contract", html)
        self.assertIn("KatalysisCharts.observe()", html)
        self.assertNotIn('src="https://', html)
        self.assertIn("Review signals", html)
        self.assertIn("grid-template-columns:repeat(5", html)
        self.assertIn('font-family:system-ui', html)
        self.assertIn('href="#overview"', html)
        self.assertIn('href="#trend-signals"', html)
        self.assertIn('href="#analysis"', html)

    def test_template_preserves_accessible_dashboard_landmarks(self):
        html = decorate_dashboard_html(TEMPLATE.replace("__IN011_ANALYSIS__", '<section class="grid in011-analysis"></section>'))
        self.assertIn('aria-label="Dashboard navigation"', html)
        self.assertIn('aria-label="Executive summary"', html)
        self.assertIn('id="analysis"', html)

class GroupVerdictAndDisplayNameFallback(unittest.TestCase):
    """A future multi-entity parent group with no curated verdict/display
    name must be OMITTED and WARNED about, never guessed - this is the
    specific safety property that replaced the original hardcoded list."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="deliverables_test_")
        self.db_path = os.path.join(self.tmpdir, "test.db")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _build_db_with_group(self, ultimate_group_name, n_members=2):
        conn = build_insights_db.connect(self.db_path)
        rows = []
        lookup_rows = []
        for i in range(n_members):
            frn = 100 + i
            rows.append({
                "bank": f"BANK{i}", "canonical_bank": f"Bank {i} Ltd", "source_filename_bank": f"BANK{i}",
                "source_workbook": f"BANK{i} FINANCIALS.xlsx", "frn": frn, "workbook_kind": "full",
                "sheet": "CET1 Ratio", "row_label": "CET1 ratio", "year": "FY2025",
                "value_raw": "14.5%", "value_numeric": 14.5, "is_numeric": "1", "basis_note": "",
            })
            lookup_rows.append({"frn": frn, "bank_name": f"Bank {i}", "immediate_parent": "Parent Co",
                                 "ultimate_group": ultimate_group_name, "status_caveat": "confirmed", "evidence": "test"})
        build_insights_db.write_banks_and_metrics(conn, rows, metrics_source="test")
        build_insights_db.write_parent_group(conn, lookup_rows, edge_rows=[])
        conn.close()

    def test_curated_group_is_included_with_its_verdict(self):
        # use a real curated group name so the happy path is also proven
        curated_name = next(iter(GROUP_VERDICTS))
        self._build_db_with_group(curated_name)
        payload = compute_groups_payload(self.db_path)
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["entities"], 2)
        self.assertEqual(payload[0]["name"], GROUP_VERDICTS[curated_name]["name"])

    def test_uncurated_group_is_omitted_not_guessed(self):
        self._build_db_with_group("Some Brand New Conglomerate")
        payload = compute_groups_payload(self.db_path)
        self.assertEqual(payload, [])  # omitted entirely, no fabricated verdict

    def test_uncurated_group_prints_a_warning(self):
        import io
        from contextlib import redirect_stdout
        self._build_db_with_group("Some Brand New Conglomerate")
        buf = io.StringIO()
        with redirect_stdout(buf):
            compute_groups_payload(self.db_path)
        self.assertIn("Some Brand New Conglomerate", buf.getvalue())
        self.assertIn("no curated verdict", buf.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
