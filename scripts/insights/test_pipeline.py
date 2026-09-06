"""Integration and end-to-end tests for the insights refresh pipeline.

All commands use temporary databases and output files. The live database,
workbooks, research exports, and deliverables are never overwritten.
Run with:

    python3 scripts/test_pipeline.py
"""

import csv
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
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM annual_metrics").fetchone()[0], 101193)
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
        # Threshold raised 2026-09-06 (IN-065): the historical-depth (HD-series)
        # extension grew annual_metrics from 58,668 to 101,193 rows (~1.72x),
        # which grows this raw per-row client payload proportionally - confirmed
        # via the two assertNotIn checks above (still absent) that this is real
        # data growth, not a reintroduced duplicate-embedding regression.
        self.assertLess(len(html_text), 55_000_000,
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
        # A bare "<style>" substring match undercounts a tag carrying an
        # attribute (e.g. '<style id="dashboard-chart-css">') - match the
        # opening tag itself, not one specific spelling of it.
        self.assertEqual(len(re.findall(r"<style\b", html_text)), html_text.count("</style>"))
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

        deliverable_dir = self.tmpdir / "deliverable"
        deliverable = run_script("build_deliverable.py", "--db", self.db, "--out", deliverable_dir)
        self.assertIn("145 bank-<slug>.html", deliverable.stdout)
        self.assertTrue((deliverable_dir / "comparison.html").exists())
        self.assertTrue((deliverable_dir / "banks.html").exists())
        self.assertTrue((deliverable_dir / "deliverable_shared.css").exists())
        self.assertTrue((deliverable_dir / "deliverable_shared.js").exists())
        # IN-052: the deliverable vendors Chart.js locally (matching IN-036's
        # original "no CDN dependency" acceptance criterion, which IN-051's
        # migration had silently dropped by loading it from jsdelivr) -
        # every page must reference the local copy, never a CDN URL.
        self.assertTrue((deliverable_dir / "chart.umd.min.js").exists())
        self.assertEqual(len(list(deliverable_dir.glob("bank-*.html"))), 145)
        self.assertEqual(len(list(deliverable_dir.glob("workbook-*.html"))), 145)
        monzo_html = (deliverable_dir / "bank-monzo.html").read_text()
        self.assertIn("Monzo", monzo_html)
        self.assertIn('href="deliverable_shared.css"', monzo_html)
        self.assertIn('src="deliverable_shared.js"', monzo_html)
        self.assertIn('src="chart.umd.min.js"', monzo_html)
        self.assertNotIn("cdn.jsdelivr.net", monzo_html)
        self.assertTrue((deliverable_dir / "assets" / "logos" / "monzo.svg").exists())
        self.assertTrue((deliverable_dir / "assets" / "logos" / "manifest.json").exists())
        self.assertIn('class="bank-identity"', monzo_html)
        self.assertIn('src="assets/logos/monzo.svg"', monzo_html)
        self.assertIn('alt=""', monzo_html)
        # build_deliverable.py must read every metric straight from the DB
        # at generation time (per IN-051's decision), never from a cached
        # research/in040_risk_metrics.json or in041_spend_metrics.json
        # snapshot that could silently go stale - assert the old file-
        # reading variables are gone, not the bare filename string (which
        # legitimately still appears in the module's own docstring).
        build_deliverable_source = (SCRIPTS / "build_deliverable.py").read_text()
        self.assertNotIn("RISK_JSON", build_deliverable_source)
        self.assertNotIn("SPEND_JSON", build_deliverable_source)
        self.assertIn("build_in040_payload(DB_PATH)", build_deliverable_source)
        self.assertIn("build_in041_payload(DB_PATH)", build_deliverable_source)
        # IN-052: trajectories + regulatory headroom trajectory, the two
        # old-dashboard sections with no equivalent anywhere else in
        # deliverable/, migrated onto comparison.html only (not every
        # per-bank page). Both sections are client-rendered from the
        # embedded "trends-data" payload (same pattern as every other
        # comparison.html block), so the section titles live in
        # deliverable_shared.js's template strings, not the static HTML.
        comparison_html = (deliverable_dir / "comparison.html").read_text()
        self.assertIn('id="trends-data"', comparison_html)
        self.assertIn('id="outliers-data"', comparison_html)
        self.assertIn('id="parent-groups-data"', comparison_html)
        self.assertIn("renderComparisonPage(DATA, Object.keys(DATA), TRENDS, OUTLIERS, PARENT_GROUPS, EFFICIENCY, BUBBLES, CLUSTERS)", comparison_html)
        deliverable_js = (deliverable_dir / "deliverable_shared.js").read_text()
        self.assertIn("Ratio trajectories", deliverable_js)
        self.assertIn("Regulatory headroom trajectory", deliverable_js)
        self.assertIn("Most extreme", deliverable_js)
        self.assertIn("Parent groupings", deliverable_js)
        self.assertIn("build_in024_payload(DB_PATH)", build_deliverable_source)
        self.assertIn("build_headroom_payload(DB_PATH)", build_deliverable_source)
        self.assertIn("build_in010_payload(DB_PATH)", build_deliverable_source)
        self.assertIn("detect_outliers(observations, metric, sheet)", build_deliverable_source)

        # 2026-09-05 follow-up: parent groups get their own overview page
        # (click a group in the Parent groupings table -> group-<slug>.html),
        # with a member roster, a Total P&L headline, and the same ratio-
        # dispersion table scoped to just that group.
        group_pages = list(deliverable_dir.glob("group-*.html"))
        self.assertEqual(len(group_pages), 6)  # the 6 real multi-member groups in this fixture DB
        lloyds_html = (deliverable_dir / "group-lloyds-banking-group.html").read_text()
        self.assertIn('id="group-data"', lloyds_html)
        self.assertIn("renderGroupPage(GROUP_DATA, BANKS_INDEX)", lloyds_html)
        self.assertIn('href="deliverable_shared.css"', lloyds_html)
        self.assertIn('src="chart.umd.min.js"', lloyds_html)
        self.assertIn("total_pnl_by_year", lloyds_html)
        self.assertIn("group-${slugify(row.group)}.html", deliverable_js)

        # 2026-09-05 follow-up: one unified parent-groupings table (not one
        # per metric) plus, on each group's own page, a per-member balance-
        # sheet (Total assets) contribution chart and a "reported only at
        # the parent-group level" section surfacing metrics some members
        # don't disclose solo (found via each such member's own DB
        # restatement_note, e.g. Bank of Scotland's LCR/NSFR/MREL Ratio).
        self.assertIn("parentGroupsTableHtml", deliverable_js)
        self.assertIn("groupMetricChartsHtml", deliverable_js)
        self.assertIn("groupLevelMetricsHtml", deliverable_js)
        self.assertIn("member_total_assets", lloyds_html)
        self.assertIn("total_assets_by_year", lloyds_html)
        self.assertIn("group_level_metrics", lloyds_html)
        self.assertIn("Reported only at the parent-group level", deliverable_js)
        self.assertIn("curate_total_assets(conn, m", build_deliverable_source)
        self.assertIn("curate_group_level_metrics(data, parent_groups", build_deliverable_source)

        # 2026-09-05 follow-up: what those assets/liabilities actually ARE
        # (not just the total) per member, plus a group-level income mix
        # showing where the whole group's P&L came from.
        self.assertIn("curate_liability_composition(conn, m", build_deliverable_source)
        self.assertIn("member_capital_deployment", lloyds_html)
        self.assertIn("member_liability_composition", lloyds_html)
        self.assertIn("total_income_breakdown_by_year", lloyds_html)
        self.assertIn("What those assets &amp; liabilities are", deliverable_js)
        self.assertIn("Where the group made its profit &amp; loss", deliverable_js)

        # 2026-09-05 follow-up: combine members' own £ figures into one
        # parent-group asset/liability composition (e.g. "how much of HSBC
        # group's combined assets are customer loans"), shown alongside
        # each member's own bar as a "<group> — combined" row.
        self.assertIn("curate_asset_composition_absolute(conn, m", build_deliverable_source)
        self.assertIn("group_asset_composition", lloyds_html)
        self.assertIn("group_liability_composition", lloyds_html)
        self.assertIn("combined", deliverable_js)

        # 2026-09-05 follow-up: for metrics flagged as parent-group-level
        # only with no in-dataset member substitute (e.g. MREL Ratio, set
        # by every group's resolution entity - itself not one of Katalysis's
        # 145 workbooks), look up whether that ultimate/resolution parent
        # itself publicly discloses the figure and surface it, cited,
        # distinct from the existing sibling-member "substitute" case.
        self.assertIn("ultimate_parent", lloyds_html)
        self.assertIn("ULTIMATE_PARENT_METRICS", build_deliverable_source)
        self.assertIn("Lloyds Banking Group plc", build_deliverable_source)
        self.assertIn("entry.ultimate_parent", deliverable_js)

        # 2026-09-05 follow-up 2: extend the ultimate-parent lookup to
        # LCR/NSFR too, and - unlike MREL, where it only filled a gap -
        # consult it even where a sibling-member substitute already
        # exists, since the group's own consolidated ratio beats one
        # non-resolution-entity subsidiary's solo figure standing in for
        # the whole group ("try search in the ultimate parent as well,
        # and see if that can get a better picture for the whole group").
        self.assertIn('"LCR"', build_deliverable_source)
        self.assertIn('"NSFR"', build_deliverable_source)
        self.assertIn("NatWest Group plc", build_deliverable_source)
        self.assertIn("ultimate_parent = ULTIMATE_PARENT_METRICS.get(group, {}).get(sheet)", build_deliverable_source)

        # IN-053 rewrite: build_in006_pdf.py no longer hand-draws PDF syntax
        # from in011_deliverables.py's old dashboard - it mirrors
        # comparison.html's own sections via Playwright printing a
        # dedicated print-only HTML page (build_deliverable.py's curators,
        # called in-process, same as write_comparison() itself). No
        # --clusters flag any more - clusters come from
        # curate_comparison_clusters()'s own fixed CLUSTERS_CSV path, same
        # as build_deliverable.py already relies on.
        pdf_path = self.tmpdir / "deliverable.pdf"
        pdf = run_script("build_in006_pdf.py", "--db", self.db, "--out", pdf_path)
        self.assertIn("deliverable.pdf", pdf.stdout)
        self.assertIn("145 banks", pdf.stdout)
        pdf_bytes = pdf_path.read_bytes()
        self.assertTrue(pdf_bytes.startswith(b"%PDF-1."))
        self.assertTrue(pdf_bytes.rstrip().endswith(b"%%EOF"))
        if shutil.which("qpdf"):
            checked = subprocess.run(["qpdf", "--check", str(pdf_path)], capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        # Chromium's PDF output stream-compresses its content, unlike the
        # old hand-rolled writer's plain-text streams - extract via
        # pdftotext (poppler) rather than decoding raw bytes.
        if shutil.which("pdftotext"):
            pdf_text = subprocess.run(
                ["pdftotext", "-layout", str(pdf_path), "-"], capture_output=True, text=True, check=True
            ).stdout
            self.assertIn("UK bank Pillar 3", pdf_text)
            self.assertIn("Loan concentration", pdf_text)
            self.assertIn("Capital, liquidity & RWA", pdf_text)
            self.assertIn("Capital ratios", pdf_text)
            self.assertIn("Liquidity ratios", pdf_text)
            self.assertIn("RWA breakdown", pdf_text)
            self.assertIn("Balance sheet", pdf_text)
            self.assertIn("Parent", pdf_text)
            self.assertIn("Regulatory", pdf_text)
            self.assertIn("headroom", pdf_text.lower())
            self.assertIn("Parent group summaries", pdf_text)
            self.assertIn("Combined total assets", pdf_text)
            self.assertIn("Combined profit for the year", pdf_text)
            self.assertIn("Lloyds Banking Group", pdf_text)

    def test_real_workbook_extraction_to_temporary_source_of_truth(self):
        metrics_csv = self.tmpdir / "bank_metrics.csv"
        extracted = run_script("extract_metrics.py", "--db", self.db, "--out", metrics_csv)
        self.assertIn("Wrote 145 banks / 101193 annual_metrics rows", extracted.stdout)
        self.assertIn("Exported 101193 rows", extracted.stdout)
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


class SyntheticVariableYearWindowPipeline(unittest.TestCase):
    """End-to-end proof (IN-065 follow-up) that a bank with a much longer
    year window than its peers - exactly what the historical-depth
    (HD-series) extension effort produced for ~24 real banks - flows
    correctly through extract_metrics.py -> cluster_banks.py ->
    in018_powerbi.py, using synthetic workbooks built with the real
    BankWorkbook class (not hand-rolled openpyxl) in an isolated scratch
    --banks-dir, never the real banks/ directory - so this test never
    depends on which real banks happen to be extended on any given day.

    write_banks_and_metrics() requires every row to carry a real FRN (it
    raises rather than accept a None/empty one - "this indicates a
    regression in FRN coverage"), and there's no --bank-list override on
    extract_metrics.py to point it at a fixture list instead of the real
    `Banks List 2608.xlsx`. So this fixture reuses two REAL, distinct bank
    names purely so match_frn() resolves them against the real bank list -
    every number inside the two workbooks themselves is 100% fabricated,
    and the scratch --banks-dir never touches or reads the real banks/
    directory, so this in no way asserts anything about the real Monzo or
    Atom Bank workbooks."""

    LONG_BANK_NAME = "MONZO"       # real FRN 730427 - used here only so match_frn() resolves it; content is fake
    SHORT_BANK_NAME = "ATOM BANK"  # real FRN 661960 - same reasoning
    LONG_YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016"]
    SHORT_YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
    RATIO_SHEETS = ["CET1 Ratio", "Tier 1 Ratio", "Total Capital Ratio", "Leverage Ratio"]

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="synthetic_variable_year_test_"))
        self.banks_dir = self.tmpdir / "banks"
        self.banks_dir.mkdir()
        self.db = self.tmpdir / "insights.db"
        sys.path.insert(0, str(SCRIPTS))
        sys.path.insert(0, str(SCRIPTS.parent))
        global BankWorkbook
        from bank_workbook import BankWorkbook  # noqa: local import, see module docstring convention

        self._build_workbook(self.LONG_BANK_NAME, self.LONG_YEARS)
        self._build_workbook(self.SHORT_BANK_NAME, self.SHORT_YEARS)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _build_workbook(self, bank_name, years):
        bw = BankWorkbook(bank_name=bank_name, years=years, header_color="336699")
        for i, sheet in enumerate(self.RATIO_SHEETS):
            value = 10.0 + i  # distinct per-sheet base so a wrong-dimension bug would show up as a wrong cluster value
            rows_data = [(sheet, {y: f"{value + j * 0.1}%" for j, y in enumerate(years)})]
            bw.add_metric_sheet(sheet, "% of RWA", rows_data, sources_text="Test fixture - not a real source.")
        path = self.banks_dir / f"{bank_name} FINANCIALS.xlsx"
        bw.save(str(path))
        return path

    def test_extract_metrics_keeps_each_banks_own_year_count_independent(self):
        extracted = run_script("extract_metrics.py", "--banks-dir", self.banks_dir, "--db", self.db,
                                "--out", self.tmpdir / "metrics.csv")
        self.assertIn("Wrote 2 banks", extracted.stdout)
        self.assertIn("Banks with no FRN match (0)", extracted.stdout)

        conn = sqlite3.connect(self.db)
        try:
            rows = conn.execute(
                "SELECT b.filename_bank_name, COUNT(*) FROM annual_metrics m "
                "JOIN banks b ON b.frn = m.frn GROUP BY b.filename_bank_name"
            ).fetchall()
            counts = dict(rows)
            long_years = {
                row[0] for row in conn.execute(
                    "SELECT DISTINCT m.year FROM annual_metrics m JOIN banks b ON b.frn = m.frn "
                    "WHERE b.filename_bank_name = ?", (self.LONG_BANK_NAME,)
                ).fetchall()
            }
        finally:
            conn.close()
        # 4 ratio sheets x each bank's own year count - the long-window bank
        # must NOT be truncated to the short bank's 5 years, and the short
        # bank must NOT be padded up to the long bank's 10.
        self.assertEqual(counts[self.LONG_BANK_NAME], 4 * len(self.LONG_YEARS))
        self.assertEqual(counts[self.SHORT_BANK_NAME], 4 * len(self.SHORT_YEARS))
        self.assertEqual(long_years, set(self.LONG_YEARS))

    def test_cluster_banks_uses_one_row_per_bank_at_its_own_latest_year(self):
        run_script("extract_metrics.py", "--banks-dir", self.banks_dir, "--db", self.db,
                   "--out", self.tmpdir / "metrics.csv")
        cluster_out = self.tmpdir / "clusters.csv"
        # Only 2 fixture banks exist, and k must be < n_banks (silhouette
        # needs at least 2 points per candidate cluster) - k=1 is the only
        # triable value here. That's fine: this test isn't checking cluster
        # quality, only that build_feature_matrix() (exercised identically
        # regardless of k) picks one row per bank at its own latest year.
        result = run_script("cluster_banks.py", "--db", self.db, "--out", cluster_out,
                             "--k-min", "1", "--k-max", "1")
        self.assertEqual(result.returncode, 0)

        with open(cluster_out, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        # exactly one row per bank, regardless of the long-window bank
        # having 2x the raw annual_metrics rows of the short-window bank -
        # extra historical years must never become extra clustering
        # observations.
        self.assertEqual(len(rows), 2)
        by_bank = {r["bank"]: r for r in rows}
        # Both banks' fixture assigns CET1 Ratio's FY2025 value as the base
        # 10.0 (j=0 in _build_workbook's enumerate, since FY2025 is index 0
        # in both year lists) and FY2016's as the highest, 10.9 - a bank
        # whose year-selection logic wrongly picked its OLDEST disclosed
        # year instead of its latest would show 10.9 for the long-window
        # bank here, not 10.0. Asserting the _year column too makes the
        # failure mode unambiguous rather than inferring it from the value
        # alone.
        self.assertEqual(by_bank[self.LONG_BANK_NAME]["CET1 Ratio_year"], "FY2025")
        self.assertEqual(by_bank[self.SHORT_BANK_NAME]["CET1 Ratio_year"], "FY2025")
        self.assertAlmostEqual(float(by_bank[self.LONG_BANK_NAME]["CET1 Ratio_value"]), 10.0, places=3)
        self.assertAlmostEqual(float(by_bank[self.SHORT_BANK_NAME]["CET1 Ratio_value"]), 10.0, places=3)

    def test_powerbi_star_schema_has_no_dangling_fks_across_unequal_windows(self):
        run_script("extract_metrics.py", "--banks-dir", self.banks_dir, "--db", self.db,
                   "--out", self.tmpdir / "metrics.csv")
        out_dir = self.tmpdir / "powerbi"
        result = run_script("in018_powerbi.py", "--db", self.db, "--out-dir", out_dir)
        self.assertEqual(result.returncode, 0)

        def load_ids(path, key):
            with open(path, newline="", encoding="utf-8") as f:
                return {row[key] for row in csv.DictReader(f)}

        dim_period = load_ids(out_dir / "dim_period.csv", "period_id")
        dim_bank = load_ids(out_dir / "dim_bank.csv", "bank_id")
        # dim_period must span the UNION of both banks' years, not be
        # truncated to whichever bank happens to be processed last/first.
        self.assertEqual(dim_period, set(self.LONG_YEARS) | set(self.SHORT_YEARS))

        with open(out_dir / "fact_observation.csv", newline="", encoding="utf-8") as f:
            facts = list(csv.DictReader(f))
        self.assertEqual(len(facts), 4 * (len(self.LONG_YEARS) + len(self.SHORT_YEARS)))
        self.assertEqual(sum(1 for r in facts if r["period_id"] not in dim_period), 0)
        self.assertEqual(sum(1 for r in facts if r["bank_id"] not in dim_bank), 0)
        # every one of the long-window bank's own extra (pre-2021) years
        # must actually appear as a fact - not silently dropped because its
        # peer bank in the same run only has 5 years.
        long_bank_id = next(r["bank_id"] for r in facts if r["reported_year"] == "FY2016")
        pre2021_facts = [r for r in facts if r["bank_id"] == long_bank_id and r["reported_year"] in
                         ("FY2016", "FY2017", "FY2018", "FY2019", "FY2020")]
        self.assertEqual(len(pre2021_facts), 4 * 5)  # 4 ratio sheets x 5 pre-2021 years


if __name__ == "__main__":
    unittest.main(verbosity=2)
