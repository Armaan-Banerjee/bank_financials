"""Integration and end-to-end tests for the insights refresh pipeline.

All commands use temporary databases and output files. The live database,
workbooks, research exports, and deliverables are never overwritten.
Run with:

    python3 scripts/test_pipeline.py
"""

import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts" / "insights"


def run_script(name, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *map(str, args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


class FullInsightsPipeline(unittest.TestCase):
    """Run every IN-007/IN-008 consumer against a clean temporary DB."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="insights_pipeline_test_"))
        self.db = self.tmpdir / "insights.db"
        self.md = self.tmpdir / "bank_parent_groups.md"
        shutil.copy(ROOT / "research" / "bank_parent_groups.md", self.md)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_clean_build_and_all_consumers(self):
        built = run_script("build_insights_db.py", "--db", self.db)
        self.assertIn("All validation checks passed", built.stdout)

        conn = sqlite3.connect(self.db)
        try:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM banks").fetchone()[0], 145)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM annual_metrics").fetchone()[0], 58587)
            self.assertEqual(conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        finally:
            conn.close()

        db_cluster = self.tmpdir / "clusters_db.csv"
        csv_cluster = self.tmpdir / "clusters_csv.csv"
        run_script("cluster_banks.py", "--db", self.db, "--out", db_cluster)
        run_script("cluster_banks.py", "--in", ROOT / "research" / "bank_metrics.csv", "--out", csv_cluster)
        self.assertEqual(db_cluster.read_bytes(), csv_cluster.read_bytes())
        self.assertEqual(
            (self.tmpdir / "clusters_db_centroids.csv").read_bytes(),
            (self.tmpdir / "clusters_csv_centroids.csv").read_bytes(),
        )
        self.assertEqual(
            (self.tmpdir / "clusters_db_sweep.csv").read_bytes(),
            (self.tmpdir / "clusters_csv_sweep.csv").read_bytes(),
        )

        decomposition = self.tmpdir / "in022_ratio_decomposition.json"
        run_script("in022_ratio_decomposition.py", "--db", self.db, "--out", decomposition)
        decomposition_payload = json.loads(decomposition.read_text())
        self.assertIn("broad", decomposition_payload)
        self.assertIn("strict", decomposition_payload)
        self.assertGreater(decomposition_payload["broad"]["coverage"]["comparable_banks"], 0)

        distributions = self.tmpdir / "in023_distribution_visuals.json"
        run_script("in023_distribution_visuals.py", "--db", self.db, "--out", distributions)
        distributions_payload = json.loads(distributions.read_text())
        self.assertIn("coverage", distributions_payload)
        self.assertIn("state_counts", distributions_payload["coverage"])

        trajectories = self.tmpdir / "in024_trajectory.json"
        run_script("in024_trajectory.py", "--db", self.db, "--out", trajectories)
        trajectory_payload = json.loads(trajectories.read_text())
        self.assertIn("trajectories", trajectory_payload)
        self.assertIn("rank_mobility", trajectory_payload)
        self.assertIn("coverage_churn", trajectory_payload)

        quality_views = self.tmpdir / "in025_quality_views.json"
        run_script("in025_quality_views.py", "--db", self.db, "--out", quality_views)
        quality_payload = json.loads(quality_views.read_text())
        self.assertIn("cadence", quality_payload)
        self.assertIn("trace", quality_payload)
        self.assertEqual(quality_payload["join_checks"]["annual_orphan_rows"], 0)

        trend = run_script("analyze_trends.py", "--db", self.db)
        self.assertIn("Metrics source: database", trend.stdout)
        self.assertIn("Parent-group source: database", trend.stdout)
        self.assertIn("CET1 ratio: FY2021->FY2022", trend.stdout)

        review_path = self.tmpdir / "trend_review.md"
        review = run_script("review_trend_selection.py", "--db", self.db, "--out", review_path)
        self.assertIn("Metrics source: database", review.stdout)
        self.assertIn("Rows are from `", review_path.read_text())

        html_path = self.tmpdir / "deliverable.html"
        html = run_script("build_in005_prototype.py", "--db", self.db, "--out", html_path,
                          "--clusters", db_cluster, "--centroids", self.tmpdir / "clusters_db_centroids.csv")
        self.assertIn("145 cluster rows", html.stdout)
        html_text = html_path.read_text()
        self.assertIn("CLIENT DELIVERABLE", html_text)
        payload = json.loads(re.search(r"const D=(.*?);\nfunction esc", html_text, re.S).group(1))
        self.assertEqual(len(payload["banks"]), 145)
        self.assertEqual(len(payload["trend_series"]), 8)
        self.assertIn("in011", payload)
        self.assertIn("in009", payload["in011"])
        self.assertIn("in010", payload["in011"])
        self.assertIn("in012", payload["in011"])
        self.assertIn("in022", payload["in011"])
        self.assertIn("in023", payload["in011"])
        self.assertIn("in024", payload["in011"])
        self.assertIn("in025", payload["in011"])
        self.assertIn("in021", payload["in011"])
        # build_in011_payload() used to embed full copies of in016/in017
        # inside in023 on top of them already being siblings, and in025's
        # unused-client-side "trace" raw dump used to be serialized into the
        # client payload wholesale - together these bloated the HTML
        # deliverable to 130+MB, which was slow/unusable enough in a real
        # browser to look "broken" (nothing but the static sidebar ever
        # rendered). Guard against both regressing.
        self.assertNotIn("in016", payload["in011"]["in023"])
        self.assertNotIn("in017", payload["in011"]["in023"])
        self.assertNotIn("trace", payload["in011"]["in025"])
        self.assertLess(len(html_text), 35_000_000,
                         "deliverable HTML grew unexpectedly large - check for a "
                         "reintroduced duplicate/unused payload the way in023/in025 once had")
        self.assertIn("Regulatory headroom trajectory", html_text)
        self.assertIn('id="headroom-table"', html_text)
        self.assertEqual(html_text.count('class="sort-headroom"'), 9)
        self.assertNotRegex(html_text, r"IN-[0-9]{3}")
        self.assertIn("Strict versus broad coverage", html_text)
        self.assertIn("Outlier investigation", html_text)
        self.assertNotRegex(html_text, r'<details id="outliers"[^>]*\bopen\b')
        self.assertIn('button.closest("#watchlist")', html_text)
        self.assertIn("Parent-group dispersion and agreement", html_text)
        self.assertIn("CET1 ratio movement decomposition", html_text)
        self.assertIn("Capital change (%)", html_text)
        self.assertIn("Robust distributions and evidence coverage", html_text)
        self.assertIn("Bank × metric × year evidence coverage", html_text)
        self.assertIn("Persistent trajectories and rank mobility", html_text)
        self.assertIn('id="in024-filter"', html_text)
        self.assertIn("Source quality and disclosure coverage", html_text)
        self.assertIn('id="in025-filter"', html_text)
        self.assertLess(html_text.index("Trend signals"), html_text.index("Strict versus broad coverage"))
        self.assertLess(html_text.index("Inside the parent groups"), html_text.index("Strict versus broad coverage"))
        self.assertIn("Banks to review", html_text)
        self.assertIn('id="watchlist"', html_text)
        self.assertLess(html_text.index("<header>"), html_text.index('id="watchlist"'))
        self.assertLess(html_text.index('id="dashboard-kpis"'), html_text.index('id="watchlist"'))
        self.assertIn('id="global-bank-search"', html_text)
        self.assertIn('id="bank-drillthrough"', html_text)
        self.assertEqual(html_text.count('id="bank-drillthrough"'), 1)
        self.assertLess(html_text.index('id="watchlist"'), html_text.index('id="bank-drillthrough"'))
        self.assertLess(html_text.index('id="bank-drillthrough"'), html_text.index('id="overview"'))
        self.assertIn("bindReliableBankSearch", html_text)
        self.assertIn("focusTrajectoryBank", html_text)
        self.assertIn("trajectorySearchState", html_text)
        self.assertIn("restoreTrajectorySearchState", html_text)
        self.assertIn("startsWith(normalised)", html_text)
        self.assertIn("toggle.dispatchEvent(new Event(\"change\"", html_text)
        self.assertIn('data-default-visible="true"', html_text)
        self.assertNotIn('tr[data-search],tr[data-bank],.in024-bank-toggle,.in024-point', html_text)
        self.assertIn('section=document.querySelector("#trajectories")', html_text)
        self.assertIn('toggle.dispatchEvent(new Event("change"', html_text)
        self.assertEqual(len(re.findall(r'<details[^>]*\sopen(?:\s|=|>)', html_text)), 1)
        self.assertIn("freshness-badge", html_text)
        self.assertEqual(html_text.count("<style>"), html_text.count("</style>"))
        self.assertIn("</style></head>", html_text)
        self.assertIn("kpi-sparkline", html_text)
        # Regression: the dashboard's JS used to generate elements with these
        # class names while decorate_dashboard_html()'s own CSS injection was
        # a silent no-op (a stale duplicate of the dashboard shell baked
        # directly into TEMPLATE pre-empted every one of its replace()
        # targets) - the substring checks above only prove the class name
        # text appears SOMEWHERE (e.g. in the JS that generates it), not that
        # a matching CSS rule exists, which is how that bug shipped past a
        # "verified the complete test suite" claim undetected. Assert the
        # actual CSS rule, not just the class name string.
        for css_class in (".dashboard-watchlist{", ".watchlist-grid{", ".watch-item{",
                           ".freshness-badge{", ".kpi-sparkline{", ".global-search{",
                           ".bank-drillthrough{"):
            self.assertIn(css_class, html_text, f"no CSS rule found for {css_class!r}")
        self.assertEqual(html_text.count("<section"), html_text.count("</section>"),
                          "every <section> opened in the dashboard shell must be closed")
        for anchor in ("coverage", "ratio-decomposition", "distribution-visuals", "trajectories", "quality", "outliers", "headroom"):
            self.assertIn(f'id="{anchor}"', html_text)
        self.assertNotIn("__DATA__", html_text)

        pdf_path = self.tmpdir / "deliverable.pdf"
        pdf = run_script("build_in006_pdf.py", "--db", self.db, "--out", pdf_path, "--clusters", db_cluster)
        self.assertIn("deliverable.pdf", pdf.stdout)
        self.assertTrue(pdf_path.read_bytes().startswith(b"%PDF-1.4"))
        self.assertTrue(pdf_path.read_bytes().endswith(b"%%EOF\n"))
        pdf_text = pdf_path.read_bytes().decode("latin-1")
        self.assertIn("Core-ratio coverage", pdf_text)
        self.assertIn("Dashboard watchlist", pdf_text)
        self.assertIn("Evidence freshness", pdf_text)
        self.assertNotIn("IN-009", pdf_text)
        self.assertNotIn("trend=insufficient", pdf_text)
        self.assertIn("Outlier investigation", pdf_text)
        self.assertIn("Parent-group dispersion and agreement", pdf_text)
        self.assertIn("CET1 ratio movement decomposition", pdf_text)
        self.assertIn(r"RWA change \(%\)", pdf_text)
        self.assertIn("OLS R2=", pdf_text)
        self.assertIn("Regulatory headroom trajectory", pdf_text)
        self.assertIn("Persistent trajectories and rank mobility", pdf_text)
        self.assertIn("Source quality and disclosure coverage", pdf_text)
        self.assertNotIn("IN-021", pdf_text)
        if shutil.which("qpdf"):
            checked = subprocess.run(["qpdf", "--check", str(pdf_path)], capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_real_workbook_extraction_to_temporary_source_of_truth(self):
        metrics_csv = self.tmpdir / "bank_metrics.csv"
        extracted = run_script("extract_metrics.py", "--db", self.db, "--out", metrics_csv)
        self.assertIn("Wrote 145 banks / 58587 annual_metrics rows", extracted.stdout)
        self.assertIn("Exported 58587 rows", extracted.stdout)
        self.assertIn("Banks with no FRN match (0)", extracted.stdout)
        self.assertNotIn("Workbooks that failed to process (", extracted.stdout)
        self.assertEqual(metrics_csv.read_bytes(), (ROOT / "research" / "bank_metrics.csv").read_bytes())

        exported_md = self.tmpdir / "bank_parent_groups.md"
        shutil.copy(ROOT / "research" / "bank_parent_groups.md", exported_md)
        run_script("export_parent_group_tables.py", "--db", self.db, "--markdown", exported_md)
        conn = sqlite3.connect(self.db)
        try:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM parent_group_lookup").fetchone()[0], 145)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM parent_group_edges").fetchone()[0], 36)
        finally:
            conn.close()

    def test_parent_export_is_idempotent_and_preserves_hand_authored_prose(self):
        run_script("build_insights_db.py", "--db", self.db)
        before = self.md.read_text()
        first = run_script("export_parent_group_tables.py", "--db", self.db, "--markdown", self.md)
        self.assertIn("no change", first.stdout)
        self.assertEqual(self.md.read_text(), before)
        inode_before = self.md.stat().st_ino
        second = run_script("export_parent_group_tables.py", "--db", self.db, "--markdown", self.md)
        self.assertIn("no change", second.stdout)
        self.assertEqual(self.md.stat().st_ino, inode_before)

        self.assertIn("## Conventions", self.md.read_text())
        self.assertIn("## Mermaid multi-bank cluster views", self.md.read_text())
        self.assertIn("## Quality and follow-up", self.md.read_text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
