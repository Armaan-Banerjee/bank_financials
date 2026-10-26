"""
Regression tests for the Overview DERIVATION (standing objective (b)):
the Overview's headline blocks are computed from the detail sheets rather
than hand-copied alongside them, so a correction applied to a detail sheet
can no longer be missed on the Overview.

    cd scripts/insights && python3 -m unittest discover -s . -p 'test_*.py'

The ratio tests here are anchored on a defect this code actually had and
shipped into 145 workbooks before `check_overview_ties.py` caught it: the
ratio block took each metric sheet's FIRST NUMERIC value, so ABC
International's Overview LCR row printed 748.628 - the HQLA balance, in
millions - in place of the 250.1% on the LCR sheet two rows below. 877
Overview cells broke the same way. CLAUDE.md names this trap explicitly for
Leverage Ratio, LCR and NSFR, and `check_overview_ties.py` already avoided
it; the derivation reimplemented the rule more loosely instead of mirroring
it, which is the whole lesson.
"""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)

from bank_workbook import BankWorkbook  # noqa: E402


def workbook():
    return BankWorkbook(
        bank_name="Test Bank",
        years=[2025, 2024, 2023],
        header_color="305496",
    )


class RatioBlockTakesThePrintedPercentage(unittest.TestCase):
    """Leverage Ratio / LCR / NSFR sheets LEAD with an amount, not a ratio."""

    def setUp(self):
        self.bw = workbook()
        # the real shape of an LCR sheet: HQLA first, then the ratio
        self.bw._metric_rows["LCR"] = [
            ("High-quality liquid assets (£m)", {2025: 748.628, 2024: 854.893}),
            ("Net cash outflows (£m)", {2025: 299.3, 2024: 252.1}),
            ("Liquidity coverage ratio", {2025: "250.1%", 2024: "339.1%"}),
        ]

    def test_the_leading_amount_is_not_mistaken_for_the_ratio(self):
        (_label, derived), = self.bw._derive_ratios(
            [("LCR", {2025: "250.1%", 2024: "339.1%"})], [2025, 2024, 2023]
        )
        self.assertEqual(derived[2025], "250.1%")
        self.assertEqual(derived[2024], "339.1%")

    def test_a_corrected_sheet_carries_through_to_the_overview(self):
        """The point of the exercise: fix the sheet, the Overview follows."""
        self.bw._metric_rows["LCR"][2][1][2025] = "251.4%"
        (_label, derived), = self.bw._derive_ratios(
            [("LCR", {2025: "250.1%"})], [2025, 2024, 2023]
        )
        self.assertEqual(derived[2025], "251.4%")

    def test_a_year_the_metric_sheet_lacks_keeps_its_literal(self):
        """Blanking a figure a reader can see today would be worse than the
        drift derivation removes - the same rule as _keep_what_detail_lacks."""
        (_label, derived), = self.bw._derive_ratios(
            [("LCR", {2025: "250.1%", 2024: "339.1%", 2023: "369.0%"})],
            [2025, 2024, 2023],
        )
        self.assertEqual(derived[2023], "369.0%")

    def test_a_sheet_with_no_percentage_at_all_leaves_the_block_alone(self):
        """A bank that prints only an amount, or "Not publicly disclosed",
        must not have its Overview row emptied."""
        self.bw._metric_rows["MREL Ratio"] = [
            ("MREL requirement", {2025: "Not publicly disclosed"}),
        ]
        (_label, derived), = self.bw._derive_ratios(
            [("MREL Ratio", {2025: "Not publicly disclosed"})], [2025]
        )
        self.assertEqual(derived[2025], "Not publicly disclosed")

    def test_an_unknown_sheet_name_is_passed_through_untouched(self):
        (_label, derived), = self.bw._derive_ratios(
            [("Some Bespoke Ratio", {2025: "12.0%"})], [2025]
        )
        self.assertEqual(derived, {2025: "12.0%"})


class MoneyBlocksAreDerivedFromTheirDetailSheet(unittest.TestCase):
    def setUp(self):
        self.bw = workbook()
        self.bw._detail_rows["Balance Sheet"] = {
            "total assets": {2025: 1000.0, 2024: 900.0},
            "loans and advances to customers": {2025: 600.0, 2024: 550.0},
            "deposits from customers": {2025: 800.0, 2024: 700.0},
        }

    def test_a_row_resolves_by_its_own_label(self):
        out = self.bw._derive_block(
            "Balance Sheet",
            [("Total assets", {2025: 999.0, 2024: 900.0})],
            "balance sheet",
            [2025, 2024],
        )
        self.assertEqual(out[0][1][2025], 1000.0)

    def test_a_row_the_detail_sheet_does_not_carry_keeps_its_literal(self):
        out = self.bw._derive_block(
            "Balance Sheet",
            [("Shareholders' equity", {2025: 120.0})],
            "balance sheet",
            [2025],
        )
        self.assertEqual(out[0][1][2025], 120.0)


if __name__ == "__main__":
    unittest.main()
