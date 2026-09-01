import os
import tempfile
import unittest

from analyze_trends import METRICS, extract, load_groups, pairwise_counts


def row(frn, label, period, value, basis=""):
    return {
        "frn": str(frn),
        "sheet": "LCR",
        "row_label": label,
        "year": period,
        "value_raw": f"{value}%",
        "value_numeric": str(value),
        "is_numeric": "1",
        "basis_note": basis,
        "unit": "%",
    }


def metric_row(frn, sheet, label, period, value, basis=""):
    result = row(frn, label, period, value, basis)
    result["sheet"] = sheet
    return result


class ExtractTests(unittest.TestCase):
    def test_preferred_headline_wins_a_label_tie(self):
        rows = [
            row(1, "LCR", "FY2021", 101), row(1, "LCR", "FY2022", 102),
            row(1, "Liquidity Coverage Ratio", "FY2021", 201),
            row(1, "Liquidity Coverage Ratio", "FY2022", 202),
        ]
        values, diagnostics = extract(rows, "LCR", METRICS["LCR"])
        self.assertEqual(values["1"], {2021: 201.0, 2022: 202.0})
        self.assertEqual(diagnostics["label_ties"], 1)

    def test_exact_fy_period_wins_and_collision_is_reported(self):
        rows = [
            row(2, "LCR", "FY2024*", 400, "group"),
            row(2, "LCR", "FY2024", 401, "bank"),
        ]
        values, diagnostics = extract(rows, "LCR", METRICS["LCR"])
        self.assertEqual(values["2"][2024], 401.0)
        self.assertEqual(diagnostics["period_collisions"], 1)

    def test_basis_variants_are_reported(self):
        rows = [
            row(3, "LCR", "FY2023", 300, "solo"),
            row(3, "LCR", "FY2024", 301, "group"),
        ]
        _, diagnostics = extract(rows, "LCR", METRICS["LCR"])
        self.assertEqual(diagnostics["basis_variants"], 1)

    def test_percent_only_sheet_excludes_an_absolute_amount_row(self):
        # Regression for a real bug: extract() used to rely solely on regex
        # label matching + a small `excluded` substring list, with no
        # percent-vs-absolute guard at all - a supporting absolute-amount row
        # phrased differently from the curated `excluded` list (e.g. "NSFR
        # eligible liabilities (£m)") would match the NSFR pattern, evade
        # `excluded`, and get reported as if it were the ratio. The same bug
        # class already fixed three times in in009_analysis.py/
        # in016_distribution.py.
        rows = [
            {"frn": "9", "sheet": "NSFR", "row_label": "NSFR eligible liabilities (£m)",
             "year": "FY2024", "value_raw": "450000", "value_numeric": "450000",
             "is_numeric": "1", "basis_note": "", "unit": ""},
            {"frn": "9", "sheet": "NSFR", "row_label": "Net stable funding ratio (%)",
             "year": "FY2024", "value_raw": "112.4%", "value_numeric": "112.4",
             "is_numeric": "1", "basis_note": "", "unit": "%"},
        ]
        values, _ = extract(rows, "NSFR", METRICS["NSFR"])
        self.assertEqual(values["9"], {2024: 112.4})

    def test_cash_flow_uses_net_total_not_component(self):
        rows = [
            metric_row(4, "Cash Flow Statement", "Cash flows from operating activities before changes in operating assets and liabilities", "FY2024", 10),
            metric_row(4, "Cash Flow Statement", "Net cash from/(used in) operating activities", "FY2024", 20),
        ]
        values, diagnostics = extract(rows, "Operating cash flow", METRICS["Operating cash flow"])
        self.assertEqual(values["4"][2024], 20.0)
        self.assertEqual(diagnostics["period_collisions"], 0)


class PairwiseCountsTests(unittest.TestCase):
    """pairwise_counts() now drives every headline number in both
    deliverables (build_in005_prototype.py, build_in006_pdf.py) - it had
    no direct test before, only indirect coverage via ExtractTests above."""

    def test_basic_down_up_same_split(self):
        values = {"1": {2021: 100.0, 2022: 90.0},   # down
                  "2": {2021: 100.0, 2022: 110.0},  # up
                  "3": {2021: 100.0, 2022: 100.0}}  # unchanged
        c = pairwise_counts(values, 2021, 2022)
        self.assertEqual(c, {"down": 1, "up": 1, "same": 1, "n": 3})

    def test_entities_missing_either_year_are_excluded_not_counted_as_zero(self):
        values = {"1": {2021: 100.0, 2022: 90.0},
                  "2": {2021: 100.0},  # no 2022 - must not count toward n
                  "3": {2022: 90.0}}   # no 2021 - must not count toward n
        c = pairwise_counts(values, 2021, 2022)
        self.assertEqual(c["n"], 1)

    def test_empty_input_gives_all_zero_not_an_error(self):
        c = pairwise_counts({}, 2021, 2022)
        self.assertEqual(c, {"down": 0, "up": 0, "same": 0, "n": 0})

    def test_negative_values_and_deltas_handled(self):
        values = {"1": {2021: -50.0, 2022: -60.0},  # more negative = down
                  "2": {2021: -50.0, 2022: -40.0}}   # less negative = up
        c = pairwise_counts(values, 2021, 2022)
        self.assertEqual(c["down"], 1)
        self.assertEqual(c["up"], 1)

    def test_down_up_same_always_sum_to_n(self):
        values = {str(i): {2021: float(i), 2022: float(i) + (i % 3 - 1)} for i in range(10)}
        c = pairwise_counts(values, 2021, 2022)
        self.assertEqual(c["down"] + c["up"] + c["same"], c["n"])


class LoadGroupsMarkdownParsing(unittest.TestCase):
    """load_groups() only ever ran against the real, well-formed
    bank_parent_groups.md - never against a deliberately malformed table,
    which is exactly where a markdown-parsing function is most likely to
    misbehave silently."""

    def _write(self, content):
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8")
        f.write(content)
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def test_well_formed_table_row_is_parsed(self):
        path = self._write(
            "## Bank-level lookup\n\n"
            "| Bank/legal entity | FRN | Immediate parent or ownership | Ultimate/group node | Status and reporting caveat | Evidence |\n"
            "|---|---:|---|---|---|---|\n"
            "| ALPHA Bank | 111 | Parent Co | Parent Group | confirmed | test |\n"
        )
        groups = load_groups(path)
        self.assertEqual(groups, {"111": ("ALPHA Bank", "Parent Group", "confirmed")})

    def test_header_and_separator_rows_are_not_parsed_as_data(self):
        path = self._write(
            "| Bank/legal entity | FRN | Immediate parent or ownership | Ultimate/group node | Status and reporting caveat | Evidence |\n"
            "|---|---:|---|---|---|---|\n"
        )
        self.assertEqual(load_groups(path), {})

    def test_row_with_non_numeric_frn_is_skipped_not_crashed_on(self):
        path = self._write(
            "| Bank/legal entity | FRN | Immediate parent or ownership | Ultimate/group node | Status and reporting caveat | Evidence |\n"
            "|---|---:|---|---|---|---|\n"
            "| Weird Row | N/A | Parent Co | Parent Group | confirmed | test |\n"
        )
        self.assertEqual(load_groups(path), {})

    def test_row_with_too_few_columns_is_skipped_not_crashed_on(self):
        path = self._write(
            "| Bank/legal entity | FRN | Immediate parent or ownership | Ultimate/group node | Status and reporting caveat | Evidence |\n"
            "|---|---:|---|---|---|---|\n"
            "| ALPHA Bank | 111 | Parent Co |\n"  # only 3 columns, not 6
        )
        self.assertEqual(load_groups(path), {})

    def test_non_table_prose_lines_are_ignored(self):
        path = self._write(
            "## Conventions\n\n"
            "This is hand-authored prose, not a table row.\n\n"
            "| Bank/legal entity | FRN | Immediate parent or ownership | Ultimate/group node | Status and reporting caveat | Evidence |\n"
            "|---|---:|---|---|---|---|\n"
            "| ALPHA Bank | 111 | Parent Co | Parent Group | confirmed | test |\n"
        )
        groups = load_groups(path)
        self.assertEqual(len(groups), 1)


if __name__ == "__main__":
    unittest.main()
