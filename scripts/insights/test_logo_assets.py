"""Regression tests for the source-tracked bank-logo registry."""

import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(__file__))

import build_deliverable


class LogoRegistryTests(unittest.TestCase):
    def test_verified_monzo_asset_has_complete_provenance(self):
        entry = build_deliverable.LOGO_REGISTRY["monzo"]
        self.assertEqual(entry["status"], "verified")
        self.assertEqual(entry["asset"], "monzo.svg")
        self.assertTrue((build_deliverable.LOGOS_DIR / entry["asset"]).is_file())
        for field in ("source_url", "retrieved_on", "source_context", "use_note"):
            self.assertTrue(entry[field])

    def test_verified_mark_is_decorative_and_has_a_monogram_failure_fallback(self):
        markup = build_deliverable.render_bank_heading("Monzo")
        self.assertIn('src="assets/logos/monzo.svg"', markup)
        self.assertIn('alt=""', markup)
        self.assertIn('aria-hidden="true"', markup)
        self.assertIn('class="bank-monogram">M', markup)

    def test_deliberately_unresolved_entry_renders_initials_without_an_image(self):
        unresolved = {"example-bank": {"status": "unresolved", "asset": None}}
        with patch.object(build_deliverable, "LOGO_REGISTRY", unresolved):
            markup = build_deliverable.render_bank_heading("Example Bank")
        self.assertIn('class="bank-monogram">EB', markup)
        self.assertNotIn("<img", markup)


if __name__ == "__main__":
    unittest.main()
