"""
Tests for the computed (not hardcoded) content in the HTML/PDF deliverable
generators - build_in005_prototype.py and build_in006_pdf.py. These are
exactly the functions built to fix the "hardcoded headline counts" bug
(73 of 99, etc.) - without a test asserting their output is numerically
correct against a KNOWN input, a future regression in pairwise_counts() or
a metric_series() mapping would only be caught by someone eyeballing the
deliverable, which is the same failure mode that let the original bug ship.
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
from build_in006_pdf import (
    headline_signal_lines, five_year_summary_lines, year_on_year_lines,
    executive_pages, _snapshot_date_label,
    parent_group_coverage_line, peer_groups_line,
    GROUP_DISPLAY_NAMES, make_pages, pdf_escape, write_pdf,
    _line_chart_commands,
)
from build_in005_prototype import escape_html


def _series(frn_to_year_values):
    """Builds the {frn: {year_int: value}} shape extract()/metric_series()
    produce, from a plain {frn: {year: value}} dict of ints."""
    return {frn: dict(years) for frn, years in frn_to_year_values.items()}


class HeadlineSignalLinesCorrectness(unittest.TestCase):
    """build_in006_pdf.py's PDF bullet text - hand-verify the arithmetic
    for a small known series and confirm the generated text matches."""

    def test_computed_numbers_match_hand_calculated_expectation(self):
        # 3 entities: RWA up for 2 of 3 in FY2022->FY2023, CET1 down for 1
        # of 2 in FY2023->FY2024, operating cash flow up for 1 of 1 in
        # FY2023->FY2024 - all hand-countable from the series below.
        series = {
            "RWA": _series({
                "1": {2022: 100.0, 2023: 110.0},  # up
                "2": {2022: 100.0, 2023: 120.0},  # up
                "3": {2022: 100.0, 2023: 90.0},   # down
                "4": {2023: 100.0, 2024: 90.0},   # not in the 2022->2023 window
            }),
            "CET1 ratio": _series({
                "1": {2022: 15.0, 2023: 15.0, 2024: 14.0},  # down 2023->2024
                "2": {2023: 15.0, 2024: 15.0},               # unchanged
                "5": {2024: 10.0, 2025: 9.0},                # down 2024->2025
            }),
            "Operating cash flow": _series({
                "1": {2023: 50.0, 2024: 60.0},  # up
                "5": {2024: 60.0, 2025: 50.0},  # down
            }),
        }
        lines = headline_signal_lines(series)
        # collapse whitespace - the source text is manually word-wrapped
        # across list entries, so a naive join can leave irregular spacing
        # at the wrap points; that's a PDF layout detail, not what this
        # test checks (the actual computed counts).
        joined = re.sub(r"\s+", " ", " ".join(lines))
        self.assertIn("increased for 2 of 3 comparable entities in FY2022->FY2023", joined)
        self.assertIn("declined for 1 of 2 in FY2023->FY2024", joined)
        self.assertIn("declined for 1 of 2 in FY2023->FY2024 and 1 of 1 in FY2024->FY2025", joined)
        self.assertIn("improved for 1 of 1 entities in FY2023->FY2024", joined)
        self.assertIn("declines for 1 of 1 in FY2024->FY2025", joined)

    def test_zero_comparable_entities_does_not_crash(self):
        empty_series = {"RWA": {}, "CET1 ratio": {}, "Operating cash flow": {}}
        lines = headline_signal_lines(empty_series)
        joined = re.sub(r"\s+", " ", " ".join(lines))
        self.assertIn("0 of 0", joined)

    def test_executive_summary_has_five_year_graph_and_movement(self):
        series = {"CET1 ratio": _series({"1": {2021: 10, 2025: 12}}),
                  "Tier 1 ratio": {}, "Total capital ratio": {}, "Leverage ratio": {},
                  "RWA": _series({"1": {2021: 100, 2025: 120}}),
                  "Operating cash flow": {}}
        lines = five_year_summary_lines(series)
        text = "\n".join(lines)
        self.assertIn("Median ratio trajectory", text)
        self.assertIn("FY21", text)
        self.assertIn("Five-year comparable movement", text)
        self.assertIn("CET1 ratio: 1 increased", text)

    def test_year_on_year_section_precedes_appendix_content(self):
        lines = year_on_year_lines({"CET1 ratio": _series({"1": {2021: 10, 2022: 12}})})
        self.assertEqual(lines[0], "YEAR-ON-YEAR MOVEMENT BY METRIC")
        self.assertIn("FY2021->FY2022", "\n".join(lines))

    def test_executive_summary_has_two_pages_and_vector_chart_markers(self):
        series = {metric: {} for metric in ("CET1 ratio", "Tier 1 ratio", "Total capital ratio", "Leverage ratio", "RWA", "Operating cash flow")}
        pages = executive_pages(series, "test", "1 September 2026")
        self.assertEqual(len(pages), 2)
        self.assertEqual(pages[0][0], "UK BANK INSIGHTS - TEST")
        self.assertEqual(pages[0][1], "Fixed snapshot | 1 September 2026")
        self.assertEqual(pages[0][12]["type"], "line_chart")
        self.assertEqual(pages[1][7]["type"], "movement_chart")

    def test_snapshot_date_is_computed_from_refresh_metadata_not_hardcoded(self):
        # Regression for a real bug: the PDF cover page used to hardcode
        # "29 August 2026" as a literal string, staying visibly wrong through
        # every subsequent regeneration. _snapshot_date_label() must read the
        # database's own refresh timestamp instead.
        import os
        import tempfile
        import build_insights_db as _db
        with tempfile.TemporaryDirectory() as directory:
            db_path = os.path.join(directory, "model.db")
            conn = _db.connect(db_path)
            conn.execute(
                "UPDATE refresh_metadata SET metrics_built_at = ? WHERE id = 1",
                ("2026-03-15T12:00:00+00:00",),
            )
            conn.commit()
            conn.close()
            self.assertEqual(_snapshot_date_label(db_path), "15 March 2026")

    def test_legend_labels_do_not_overlap_when_two_metrics_share_identical_values(self):
        # Regression for a real bug: the legend y-position used to be
        # `chart["trends"].index((metric, values))`, which returns the FIRST
        # matching position for any two metrics whose `values` lists are
        # equal (e.g. both all-None because neither has data for the
        # plotted years) - silently rendering the second metric's label on
        # top of the first's.
        chart = {"years": [2021, 2022], "trends": [("Metric A", [None, None]), ("Metric B", [None, None])]}
        commands = _line_chart_commands(chart, x=50, y=200)
        td_lines = [line for line in commands if line.endswith(" Td")]
        # Each metric's legend text is preceded by its own "x y Td" command -
        # the two y-coordinates (second token) must differ.
        y_values = [line.split()[1] for line in td_lines[-2:]]
        self.assertEqual(len(set(y_values)), 2)


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

    def test_pdf_escape_covers_pdf_delimiters_and_backslashes(self):
        self.assertEqual(pdf_escape(r"a\\b(c)"), r"a\\\\b\(c\)")


class DashboardShellContract(unittest.TestCase):
    """The generated client page keeps a dashboard-style navigation shell."""

    def test_template_exposes_dashboard_navigation_and_kpi_seam(self):
        html = decorate_dashboard_html(TEMPLATE.replace("__IN011_ANALYSIS__", '<section class="grid in011-analysis"></section>'))
        self.assertIn('class="dashboard-shell"', html)
        self.assertIn('class="dashboard-sidebar"', html)
        self.assertIn('id="dashboard-kpis"', html)
        self.assertIn('href="#overview"', html)
        self.assertIn('href="#trend-signals"', html)
        self.assertIn('href="#analysis"', html)

    def test_template_preserves_accessible_dashboard_landmarks(self):
        html = decorate_dashboard_html(TEMPLATE.replace("__IN011_ANALYSIS__", '<section class="grid in011-analysis"></section>'))
        self.assertIn('aria-label="Dashboard navigation"', html)
        self.assertIn('aria-label="Executive summary"', html)
        self.assertIn('id="analysis"', html)

    def test_long_pdf_input_is_paginated_without_losing_lines(self):
        lines = [f"line {i}" for i in range(100)]
        pages = make_pages(lines)
        self.assertEqual(len(pages), 3)
        self.assertEqual([line for page in pages for line in page], lines)

    def test_written_pdf_has_one_page_object_per_page(self):
        with tempfile.TemporaryDirectory(prefix="pdf_output_test_") as tmp:
            path = os.path.join(tmp, "out.pdf")
            write_pdf(make_pages([f"line {i}" for i in range(100)]), path)
            with open(path, "rb") as handle:
                data = handle.read()
            self.assertTrue(data.startswith(b"%PDF-1.4"))
            self.assertEqual(data.count(b"/Type /Page "), 3)
            self.assertTrue(data.endswith(b"%%EOF\n"))


class PeerGroupsAndParentGroupCoverageLines(unittest.TestCase):
    def test_peer_groups_line_counts_match_input_rows(self):
        rows = [
            {"cluster_id": "0", "insufficient_data": "0"},
            {"cluster_id": "0", "insufficient_data": "0"},
            {"cluster_id": "1", "insufficient_data": "0"},
            {"cluster_id": "", "insufficient_data": "1"},
        ]
        lines = peer_groups_line(rows)
        joined = " ".join(lines)
        self.assertIn("2 entities", joined)  # cluster 0
        self.assertIn("cluster: 1", joined)  # cluster 1's size, exact-ish check below
        self.assertIn("1 entities", joined)  # insufficient count

    def test_peer_groups_line_all_zero_when_no_rows(self):
        lines = peer_groups_line([])
        joined = " ".join(lines)
        self.assertIn("0 entities", joined)


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

    def test_parent_group_coverage_line_omits_uncurated_group_too(self):
        self._build_db_with_group("Some Brand New Conglomerate")
        line = parent_group_coverage_line(self.db_path)
        self.assertNotIn("Some Brand New Conglomerate", line)
        self.assertIn("none", line)  # no curated groups matched


if __name__ == "__main__":
    unittest.main(verbosity=2)
