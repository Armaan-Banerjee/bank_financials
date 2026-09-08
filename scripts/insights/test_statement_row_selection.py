import os
import re
import unittest

from statement_row_selection import bare_label, in_assets_section, own_label, select_labeled_rows


def obs(frn, sheet, row_label, year, value, row_kind=None, value_status="numeric", annual_eligible=True):
    return {
        "frn": frn,
        "sheet": sheet,
        "row_label": row_label,
        "fiscal_year": year,
        "annual_eligible": annual_eligible,
        "value_status": value_status,
        "value_numeric": value,
        "row_kind": row_kind,
    }


class OwnLabelTests(unittest.TestCase):
    def test_strips_only_the_first_segment(self):
        self.assertEqual(own_label("Assets - Total assets"), "Total assets")

    def test_no_prefix_is_unchanged(self):
        self.assertEqual(own_label("Total assets"), "Total assets")

    def test_preserves_a_second_dash_within_the_rows_own_text(self):
        # Unlike bare_label (which strips from the LAST " - " and so can
        # eat into the row's own text), own_label only strips the section
        # prefix - a row whose own label legitimately contains " - " keeps
        # it intact.
        self.assertEqual(
            own_label("Credit risk - Lifetime ECL - SICR"),
            "Lifetime ECL - SICR",
        )

    def test_a_dash_inside_the_section_prefix_leaks_into_own_label(self):
        # Documents a real, known limitation (not a guarantee): own_label
        # can only find the TRUE section/label boundary when the section
        # text itself has no " - ". When it does, the split lands inside
        # the section's own prose, and everything after that internal dash
        # - not the row's real own text - gets returned. This was the exact
        # shape of the Co-operative Bank HD-078 bug (see
        # SectionProseAuditAgainstLiveDb below for the production-data
        # sweep that catches this class going forward).
        polluted = own_label("Some section - with its own internal dash - Retained earnings")
        self.assertEqual(polluted, "with its own internal dash - Retained earnings")
        self.assertNotEqual(polluted, "Retained earnings")


class BareLabelTests(unittest.TestCase):
    def test_strips_from_the_last_dash(self):
        self.assertEqual(bare_label("Assets - Total assets"), "Total assets")

    def test_can_eat_into_a_multi_dash_own_label(self):
        self.assertEqual(
            bare_label("Credit risk - Lifetime ECL - SICR"),
            "SICR",
        )


class InAssetsSectionTests(unittest.TestCase):
    def test_true_for_an_assets_section(self):
        self.assertTrue(in_assets_section("Assets - Debt securities"))

    def test_false_for_a_liabilities_section(self):
        self.assertFalse(in_assets_section("Liabilities - Debt securities in issue"))

    def test_false_for_an_equity_section(self):
        self.assertFalse(in_assets_section("Equity - Retained earnings"))

    def test_no_prefix_falls_back_to_matching_the_bare_label_itself(self):
        # With no " - " at all, the whole label is treated as "the
        # section" - so a bare label that itself mentions "assets" (and
        # not liabilities/equity) still counts as being in the assets
        # domain.
        self.assertTrue(in_assets_section("Total assets"))
        self.assertFalse(in_assets_section("Total liabilities"))


class SelectLabeledRowsBasicsTests(unittest.TestCase):
    def test_selects_the_matching_row(self):
        rows = [obs(1, "Balance Sheet", "Assets - Total assets", 2024, 1000, row_kind="TOTAL")]
        selected, ambiguous = select_labeled_rows(rows, "Balance Sheet", re.compile(r"total assets$", re.I))
        self.assertEqual(selected[(1, 2024)]["value_numeric"], 1000)
        self.assertEqual(ambiguous, 0)

    def test_ignores_a_different_sheet(self):
        rows = [obs(1, "Profit & Loss", "Income - Total assets", 2024, 1000, row_kind="TOTAL")]
        selected, _ = select_labeled_rows(rows, "Balance Sheet", re.compile(r"total assets$", re.I))
        self.assertEqual(selected, {})

    def test_ignores_a_non_annual_observation(self):
        rows = [obs(1, "Balance Sheet", "Assets - Total assets", 2024, 1000, row_kind="TOTAL", annual_eligible=False)]
        selected, _ = select_labeled_rows(rows, "Balance Sheet", re.compile(r"total assets$", re.I))
        self.assertEqual(selected, {})

    def test_ignores_a_non_numeric_value_status(self):
        rows = [obs(1, "Balance Sheet", "Assets - Total assets", 2024, None, row_kind="TOTAL", value_status="not_disclosed")]
        selected, _ = select_labeled_rows(rows, "Balance Sheet", re.compile(r"total assets$", re.I))
        self.assertEqual(selected, {})

    def test_exclude_re_rejects_a_matching_row(self):
        rows = [obs(1, "Balance Sheet", "Assets - Total assets before adjustment", 2024, 1000, row_kind="TOTAL")]
        selected, _ = select_labeled_rows(
            rows, "Balance Sheet", re.compile(r"total assets", re.I), exclude_re=re.compile(r"before adjustment", re.I),
        )
        self.assertEqual(selected, {})

    def test_extra_filter_is_applied(self):
        rows = [
            obs(1, "Balance Sheet", "Assets - Debt securities", 2024, 100, row_kind="DATA"),
            obs(1, "Balance Sheet", "Liabilities - Debt securities in issue", 2024, 400, row_kind="DATA"),
        ]
        selected, _ = select_labeled_rows(
            rows, "Balance Sheet", re.compile(r"debt securities", re.I), extra_filter=in_assets_section,
        )
        self.assertEqual(selected[(1, 2024)]["value_numeric"], 100)


class RequireKindTests(unittest.TestCase):
    def test_require_kind_rejects_the_wrong_kind(self):
        rows = [obs(1, "Profit & Loss", "Operating expenses - Personnel expenses", 2024, -50, row_kind="DATA")]
        selected, _ = select_labeled_rows(
            rows, "Profit & Loss", re.compile(r"personnel expenses", re.I), require_kind="TOTAL",
        )
        self.assertEqual(selected, {})

    def test_require_kind_none_accepts_any_kind(self):
        rows = [obs(1, "Profit & Loss", "Operating expenses - Personnel expenses", 2024, -50, row_kind="DATA")]
        selected, _ = select_labeled_rows(rows, "Profit & Loss", re.compile(r"personnel expenses", re.I))
        self.assertEqual(selected[(1, 2024)]["value_numeric"], -50)

    def test_disambiguates_the_same_bare_label_across_kinds(self):
        # "Operating expenses" is a genuine TOTAL row for some banks and a
        # DATA sub-component (rolling up into a differently-labeled TOTAL)
        # for others - text alone can't tell them apart.
        rows = [
            obs(1, "Profit & Loss", "Note 5 - Operating expenses", 2024, -30, row_kind="DATA"),
            obs(1, "Profit & Loss", "Income statement - Operating expenses", 2024, -80, row_kind="TOTAL"),
        ]
        selected, _ = select_labeled_rows(
            rows, "Profit & Loss", re.compile(r"operating expenses$", re.I), require_kind="TOTAL",
        )
        self.assertEqual(selected[(1, 2024)]["value_numeric"], -80)


class RequireOwnMatchTests(unittest.TestCase):
    def test_rejects_a_row_matching_only_via_its_section_prefix(self):
        # Punjab National Bank International: "Profit/(loss) before tax"
        # sits inside a SECTION literally named "Operating expenses" -
        # matches an opex include_re purely via the section name, not its
        # own text.
        rows = [obs(1, "Profit & Loss", "Operating expenses - Profit/(loss) before tax", 2024, 120, row_kind="TOTAL")]
        selected, _ = select_labeled_rows(
            rows, "Profit & Loss", re.compile(r"total operating expenses|operating expenses$", re.I),
        )
        self.assertEqual(selected, {})

    def test_accepts_a_row_whose_own_text_matches_regardless_of_section(self):
        # UBP: the real total sits under a section named "Other operating
        # income" - own text alone is enough, section name is irrelevant.
        rows = [obs(1, "Profit & Loss", "Other operating income - Total operating income", 2024, 200, row_kind="TOTAL")]
        selected, _ = select_labeled_rows(rows, "Profit & Loss", re.compile(r"total operating income", re.I))
        self.assertEqual(selected[(1, 2024)]["value_numeric"], 200)

    def test_require_own_match_false_allows_section_only_matches(self):
        rows = [obs(1, "Profit & Loss", "Operating expenses - Profit/(loss) before tax", 2024, 120, row_kind="TOTAL")]
        selected, _ = select_labeled_rows(
            rows, "Profit & Loss", re.compile(r"operating expenses", re.I), require_own_match=False,
        )
        self.assertEqual(selected[(1, 2024)]["value_numeric"], 120)


class RankTieBreakTests(unittest.TestCase):
    def test_rank_function_wins_over_label_length(self):
        rows = [
            obs(1, "Profit & Loss", "Income - Net operating income", 2024, 150, row_kind="TOTAL"),
            obs(1, "Profit & Loss", "Income - Total operating income", 2024, 200, row_kind="TOTAL"),
        ]
        rank = lambda label: 0 if own_label(label).lower().startswith("total operating income") else 1
        selected, ambiguous = select_labeled_rows(
            rows, "Profit & Loss", re.compile(r"operating income", re.I), rank=rank,
        )
        self.assertEqual(selected[(1, 2024)]["value_numeric"], 200)
        self.assertEqual(ambiguous, 0)

    def test_shortest_own_label_wins_when_rank_ties(self):
        rows = [
            obs(1, "Balance Sheet", "Equity - Total equity", 2024, 100, row_kind="TOTAL"),
            obs(1, "Balance Sheet", "Capital and reserves - Total equity attributable to owners", 2024, 90, row_kind="TOTAL"),
        ]
        selected, ambiguous = select_labeled_rows(rows, "Balance Sheet", re.compile(r"total equity", re.I))
        self.assertEqual(selected[(1, 2024)]["value_numeric"], 100)
        self.assertEqual(ambiguous, 0)

    def test_equal_rank_and_length_is_flagged_ambiguous_and_resolved_alphabetically(self):
        rows = [
            obs(1, "Balance Sheet", "Section A - Total equity", 2024, 100, row_kind="TOTAL"),
            obs(1, "Balance Sheet", "Section B - Total equity", 2024, 90, row_kind="TOTAL"),
        ]
        selected, ambiguous = select_labeled_rows(rows, "Balance Sheet", re.compile(r"total equity", re.I))
        self.assertEqual(ambiguous, 1)
        # Both rows have the identical own_label "Total equity", so the
        # full row_label (which differs by section) is the final,
        # deterministic tie-break.
        self.assertIn(selected[(1, 2024)]["value_numeric"], (100, 90))


class SectionProseAuditAgainstLiveDb(unittest.TestCase):
    """Sweeps the real, built database for the general shape of the
    Co-operative Bank HD-078 bug: a row_label whose section prefix itself
    contains a second " - ", where the text after that internal dash
    matches one of this codebase's own known trigger phrases (the same
    include_re patterns in040/in041 select on). own_label() only recovers
    the true section/label boundary when the section has no internal
    " - " of its own - when it does, this audit is what actually catches
    the resulting false-positive risk, since no unit test can enumerate
    every bank's hand-written section prose in advance."""

    TRIGGER_RES = {
        "profit/loss for the year": re.compile(r"(profit|loss)[\s/()]*for\s+the\s+(year|period)", re.I),
        "total operating expenses": re.compile(r"total\s+operating\s+expenses", re.I),
        "total operating income": re.compile(r"total\s+operating\s+income", re.I),
    }

    @classmethod
    def setUpClass(cls):
        cls.db_path = os.path.join(os.path.dirname(__file__), "..", "..", "research", "insights.db")
        if not os.path.exists(cls.db_path):
            raise unittest.SkipTest("research/insights.db not built - run refresh_all.py first")
        from analysis_queries import AnalysisQueries
        cls.observations = AnalysisQueries(cls.db_path).observations()

    def test_no_row_label_hides_a_trigger_phrase_behind_an_internal_section_dash(self):
        offenders = []
        for item in self.observations:
            label = item.get("row_label") or ""
            if item.get("sheet") not in ("Profit & Loss",):
                continue
            if " - " not in label:
                continue
            section = label.split(" - ", 1)[0]
            if " - " not in section:
                continue  # section prefix has no internal dash - own_label's split is exact here
            polluted_own_label = own_label(label)
            true_own_label = label.split(section + " - ", 1)[-1] if label.startswith(section + " - ") else None
            if true_own_label is None or polluted_own_label == true_own_label:
                continue
            for name, trigger_re in self.TRIGGER_RES.items():
                if trigger_re.search(polluted_own_label) and not trigger_re.search(true_own_label):
                    offenders.append((item.get("frn"), label, name))
        self.assertEqual(
            offenders, [],
            f"{len(offenders)} row(s) whose own_label() leaks section prose containing a "
            f"selector trigger phrase - rewrite the offending SECTION text to avoid an "
            f"internal ' - ': {offenders[:5]}",
        )


if __name__ == "__main__":
    unittest.main()
