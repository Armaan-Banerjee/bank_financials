"""
Regression tests for BankWorkbook._fit_height / ._fitted (wayfinder/gaps
ticket GA-030). Run with the rest of the suite:

    cd scripts/insights && python3 -m unittest discover -s . -p 'test_*.py'

GA-030: an explicit row height disables Excel's auto-fit, so text past that
height is simply not drawn. 2,347 merged note and source cells across all 145
workbooks were clipped that way, hiding ~10.8m characters of the evidence
trail the gaps map exists to produce. The fix derives the height from the
text, so a call site can no longer ask for a row that hides its own content.

The constants in `_fit_height` were MEASURED in Microsoft Excel rather than
modelled, by auto-fitting a grid of text lengths against column widths and
reading the heights back. `EXCEL_AUTOFIT` below is that measurement, kept
here as the regression anchor: the property that matters is that the model
never asks for LESS room than Excel itself would, because too tall is
harmless and too short is the defect.
"""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)

from bank_workbook import BankWorkbook  # noqa: E402

# Heights Excel chose for itself: {column width: [height for each length]}.
# Measured on macOS, 2026-10-10, in the 9pt italic face the note and source
# cells use. Lengths are LENGTHS below.
LENGTHS = [300, 600, 900, 1200, 1800]
EXCEL_AUTOFIT = {
    46: [65, 117, 169, 234, 332],
    61: [52, 91, 130, 182, 260],
    91: [39, 65, 91, 117, 182],
    106: [26, 52, 78, 104, 156],
    121: [26, 52, 65, 91, 130],
}
WORD = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod "


def prose(length):
    return (WORD * ((length // len(WORD)) + 2))[:length]


class FitHeightMatchesExcel(unittest.TestCase):
    def test_never_asks_for_less_room_than_excel_itself(self):
        """The one property the fix depends on, over the measured grid."""
        for width, heights in EXCEL_AUTOFIT.items():
            for length, excel_height in zip(LENGTHS, heights):
                model = BankWorkbook._fit_height(prose(length), width)
                self.assertGreaterEqual(
                    model,
                    excel_height,
                    f"width {width}, {length} chars: model {model} < "
                    f"Excel's own {excel_height} - text would be clipped",
                )

    def test_does_not_overshoot_wildly(self):
        """Erring tall is the point, but a 3x row would be its own defect."""
        for width, heights in EXCEL_AUTOFIT.items():
            for length, excel_height in zip(LENGTHS, heights):
                model = BankWorkbook._fit_height(prose(length), width)
                self.assertLess(model, excel_height * 2.0 + 30)


class FitHeightWrapping(unittest.TestCase):
    def test_explicit_newlines_each_end_a_line(self):
        """The old GA-030 detector averaged chars-per-line and so missed
        these entirely - which is why it under-counted the defect at 1,743
        when the real figure is 2,347."""
        one_para = BankWorkbook._fit_height("word " * 20, 120)
        twenty_paras = BankWorkbook._fit_height("word\n" * 20, 120)
        self.assertGreater(twenty_paras, one_para)

    def test_an_unbreakable_url_takes_whole_lines_of_its_own(self):
        """A citation URL cannot wrap mid-token, so it occupies entire lines
        and leaves the line before it short. Averaging characters per line -
        what the first GA-030 detector did - hides that."""
        width = 40  # ~56 characters per line
        url = "https://" + "a" * 400 + ".pdf"
        # A naive wrapper charges an unbreakable token a single line and so
        # loses the rest of it off the bottom of the row. This one charges it
        # every line it actually occupies.
        self.assertGreaterEqual(
            BankWorkbook._fit_height(url, width), (len(url) / 56) * 13.0
        )
        # and it scales with the token, rather than flattening to one line
        longer = "https://" + "a" * 1200 + ".pdf"
        self.assertGreater(
            BankWorkbook._fit_height(longer, width),
            BankWorkbook._fit_height(url, width) * 2,
        )

    def test_empty_and_missing_inputs_are_not_guessed_at(self):
        self.assertIsNone(BankWorkbook._fit_height("", 100))
        self.assertIsNone(BankWorkbook._fit_height(None, 100))
        self.assertIsNone(BankWorkbook._fit_height("text", 0))
        self.assertIsNone(BankWorkbook._fit_height("text", None))


class SpillingLongTextAcrossRows(unittest.TestCase):
    """Text too long for one row spills into further rows (user decision,
    2026-10-10) rather than growing one enormous row, because ~409.5pt is the
    tallest row a READER can set by hand - above that the row can never be
    restored once touched.

    The split is a PARTITION, never a reflow. Losing or duplicating text at a
    seam is the one way this could silently corrupt the evidence trail, so
    reassembly is asserted directly.
    """

    WIDTH = 121

    def _reassemble(self, chunks):
        return " ".join(" ".join(c.split()) for c in chunks)

    def test_nothing_is_lost_or_duplicated_at_the_seams(self):
        for length in (8000, 16000, 40000):
            text = prose(length)
            chunks = BankWorkbook._split_to_height(text, self.WIDTH)
            self.assertGreater(len(chunks), 1, f"{length} chars should spill")
            self.assertEqual(
                self._reassemble(chunks),
                " ".join(text.split()),
                f"text altered when split at {length} chars",
            )

    def test_text_with_many_newlines_also_round_trips(self):
        text = "\n\n".join(f"Paragraph {i}. " + prose(400) for i in range(40))
        chunks = BankWorkbook._split_to_height(text, self.WIDTH)
        self.assertEqual(self._reassemble(chunks), " ".join(text.split()))

    def test_every_chunk_fits_in_one_displayable_row(self):
        from bank_workbook import MAX_DISPLAY_HEIGHT

        for chunk in BankWorkbook._split_to_height(prose(30000), self.WIDTH):
            self.assertLessEqual(
                BankWorkbook._fit_height(chunk, self.WIDTH), MAX_DISPLAY_HEIGHT
            )

    def test_short_text_is_left_in_a_single_row(self):
        self.assertEqual(
            BankWorkbook._split_to_height("a short note", self.WIDTH),
            ["a short note"],
        )

    def test_an_unbreakable_token_longer_than_a_row_still_terminates(self):
        """A single 20,000-character token has no break point anywhere; the
        splitter must hard-cut rather than loop forever."""
        chunks = BankWorkbook._split_to_height("x" * 20000, self.WIDTH)
        self.assertGreater(len(chunks), 1)
        self.assertEqual("".join(chunks), "x" * 20000)


class FittedIsAFloorNotAnOverride(unittest.TestCase):
    """~1,200 hardcoded heights already sit in the build scripts. They are
    left exactly as they are, which is only safe because _fitted treats them
    as a minimum."""

    def test_a_generous_call_site_keeps_its_height_up_to_the_display_cap(self):
        from bank_workbook import MAX_DISPLAY_HEIGHT

        # honoured below the cap...
        self.assertEqual(BankWorkbook._fitted(300, "short note", 120), 300)
        # ...and capped above it, because text needing more than one row's
        # worth now spills into further rows instead of growing the row.
        self.assertEqual(
            BankWorkbook._fitted(1700, "short note", 120), MAX_DISPLAY_HEIGHT
        )

    def test_a_too_small_call_site_is_raised_to_fit(self):
        long_text = prose(1800)
        self.assertGreater(BankWorkbook._fitted(60, long_text, 121), 60)
        self.assertEqual(
            BankWorkbook._fitted(60, long_text, 121),
            BankWorkbook._fit_height(long_text, 121),
        )

    def test_unknown_width_leaves_the_request_untouched(self):
        self.assertEqual(BankWorkbook._fitted(60, "text", None), 60)


if __name__ == "__main__":
    unittest.main()
