"""
Tests for scripts/refresh_all.py's stop-on-failure orchestration logic -
the whole point of that script is "don't silently continue after a step
fails," so that behavior deserves its own coverage, not just an eyeballed
manual run.

Uses a temp directory of tiny dummy Python scripts instead of the real
insights pipeline - refresh_all.py deliberately has no --db override (see
its own docstring), so testing it against real scripts would mean either
touching the real research/ files or a much larger mocking setup. Testing
run_steps() (the extracted, script-name-agnostic loop) against fakes proves
the orchestration logic itself is correct, independent of what the real
steps do - which is exactly what's untested today.
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from refresh_all import run_steps


class RunStepsStopsOnFailure(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="refresh_all_test_"))
        self.marker_dir = self.tmpdir / "ran"
        self.marker_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_step(self, name, body):
        (self.tmpdir / name).write_text(body)

    def _make_recording_step(self, name, exit_code=0):
        """A dummy step that records that it ran (by creating a marker
        file) and exits with `exit_code`."""
        self._write_step(name, (
            "import pathlib\n"
            f"pathlib.Path(r'{self.marker_dir}') .joinpath('{name}').touch()\n"
            f"raise SystemExit({exit_code})\n"
        ))

    def test_all_steps_run_in_order_on_success(self):
        steps = ["a.py", "b.py", "c.py"]
        for s in steps:
            self._make_recording_step(s, exit_code=0)
        exit_code, ran = run_steps(steps, self.tmpdir, self.tmpdir)
        self.assertEqual(exit_code, 0)
        self.assertEqual(ran, steps)
        for s in steps:
            self.assertTrue((self.marker_dir / s).exists(), f"{s} should have run")

    def test_stops_immediately_on_first_failure_and_skips_the_rest(self):
        self._make_recording_step("a.py", exit_code=0)
        self._make_recording_step("b.py", exit_code=1)  # fails
        self._make_recording_step("c.py", exit_code=0)
        exit_code, ran = run_steps(["a.py", "b.py", "c.py"], self.tmpdir, self.tmpdir)
        self.assertEqual(exit_code, 1)
        self.assertEqual(ran, ["a.py", "b.py"])  # c.py never even attempted
        self.assertTrue((self.marker_dir / "a.py").exists())
        self.assertTrue((self.marker_dir / "b.py").exists())
        self.assertFalse((self.marker_dir / "c.py").exists(), "c.py must not run after b.py failed")

    def test_failure_exit_code_is_propagated_not_flattened(self):
        # A caller (e.g. a CI script) needs the REAL exit code, not just
        # "something failed" - confirms a non-1 exit code survives.
        self._make_recording_step("a.py", exit_code=17)
        exit_code, ran = run_steps(["a.py", "b.py"], self.tmpdir, self.tmpdir)
        self.assertEqual(exit_code, 17)
        self.assertEqual(ran, ["a.py"])

    def test_stop_after_halts_before_later_steps_even_on_success(self):
        for s in ("a.py", "b.py", "c.py"):
            self._make_recording_step(s, exit_code=0)
        exit_code, ran = run_steps(["a.py", "b.py", "c.py"], self.tmpdir, self.tmpdir, stop_after="b.py")
        self.assertEqual(exit_code, 0)
        self.assertEqual(ran, ["a.py", "b.py"])
        self.assertFalse((self.marker_dir / "c.py").exists())

    def test_a_missing_step_script_fails_loudly_not_silently(self):
        # No a.py written at all - python3 <missing file> exits nonzero.
        exit_code, ran = run_steps(["a.py"], self.tmpdir, self.tmpdir)
        self.assertNotEqual(exit_code, 0)
        self.assertEqual(ran, ["a.py"])

    def test_failing_downstream_step_does_not_modify_existing_artifact(self):
        artifact = self.tmpdir / "deliverable.html"
        original = b"previous validated deliverable"
        artifact.write_bytes(original)
        self._make_recording_step("a.py", exit_code=0)
        self._write_step("b.py", "raise SystemExit(23)\n")
        exit_code, ran = run_steps(["a.py", "b.py"], self.tmpdir, self.tmpdir)
        self.assertEqual(exit_code, 23)
        self.assertEqual(ran, ["a.py", "b.py"])
        self.assertEqual(artifact.read_bytes(), original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
