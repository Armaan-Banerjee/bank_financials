import unittest

from build_deliverable import curate_equity_waterfall


def _row(label, **components):
    return {"label": label, "values": components}


class CurateEquityWaterfallTests(unittest.TestCase):
    """A restatement/reclassification checkpoint (e.g. Monzo's real FY2020
    "Restated balance as at 1 March 2020": +12,536 Other reserves, -12,536
    Retained losses, Total equity unchanged) creates a checkpoint-to-
    checkpoint segment whose only movement row nets to exactly zero on the
    grand total. Before the 2026-09-06 fix, this still emitted a segment
    with an empty bars list - a visually blank second "FY2020" chart row
    with no bars and no visible reason for its own existence (a 2026-09-06
    user report on Monzo's chart; the equivalent 111 other empty segments
    across ~30 real banks were confirmed the same way)."""

    def test_a_net_zero_restatement_checkpoint_produces_no_empty_segment(self):
        by_order = {
            1: _row("Balance as at 28 February 2019", **{"Retained losses": "-85640", "Total equity": "115670"}),
            2: _row("Loss for the year (FY2020)", **{"Retained losses": "-113816", "Total equity": "-113816"}),
            3: _row("Shares issued", **{"Share premium": "112993", "Total equity": "112993"}),
            4: _row(
                "Balance as at 1 March 2020 (as previously reported)",
                **{"Retained losses": "-199436", "Share premium": "112993", "Total equity": "129004"},
            ),
            5: _row(
                "Prior year adjustments",
                **{"Retained losses": "-12536", "Other reserves": "12536", "Total equity": "0"},
            ),
            6: _row(
                "Restated balance as at 1 March 2020",
                **{"Retained losses": "-211972", "Other reserves": "12536", "Share premium": "112993", "Total equity": "129004"},
            ),
        }
        components = ["Retained losses", "Total equity", "Share premium", "Other reserves"]
        segments = curate_equity_waterfall(by_order, components)

        years_2020 = [s for s in segments if s["year"] == "2020"]
        self.assertEqual(len(years_2020), 1, "a net-zero restatement checkpoint must not add a second FY2020 row")
        self.assertGreater(len(years_2020[0]["bars"]), 0)
        self.assertEqual(years_2020[0]["opening"], 115670.0)
        self.assertEqual(years_2020[0]["closing"], 129004.0)

    def test_a_genuine_reconciling_gap_still_emits_its_own_segment(self):
        """A real gap between one year's closing and the next year's
        opening with no explaining movement row (verified against
        ClearBank's real FY2023/FY2024 figures) must still surface as its
        own segment carrying a "reconciling" bar - the empty-segment fix
        must not also swallow a genuine, non-zero unexplained difference."""
        by_order = {
            1: _row("Balance as at 31 December 2023", **{"Total equity": "100"}),
            2: _row("Balance as at 31 December 2024", **{"Total equity": "150"}),
        }
        components = ["Total equity"]
        segments = curate_equity_waterfall(by_order, components)

        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0]["year"], "2024")
        buckets = [b["bucket"] for b in segments[0]["bars"]]
        self.assertEqual(buckets, ["reconciling"])
        self.assertEqual(segments[0]["bars"][0]["value"], 50.0)

    def test_a_normal_year_with_real_movements_is_unaffected(self):
        by_order = {
            1: _row("Balance as at 31 December 2023", **{"Retained losses": "0", "Total equity": "100"}),
            2: _row("Profit for the year", **{"Retained losses": "20", "Total equity": "20"}),
            3: _row("Balance as at 31 December 2024", **{"Retained losses": "20", "Total equity": "120"}),
        }
        components = ["Retained losses", "Total equity"]
        segments = curate_equity_waterfall(by_order, components)

        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0]["opening"], 100.0)
        self.assertEqual(segments[0]["closing"], 120.0)
        self.assertGreater(len(segments[0]["bars"]), 0)


if __name__ == "__main__":
    unittest.main()
