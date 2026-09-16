"""
Corpus-wide check that every delivered workbook still matches its build script.

WHY THIS EXISTS. A workbook in banks/ is a client deliverable; the script in
scripts/ is its source. Nothing enforced that the two agree, and two distinct
ways of disagreeing were both found live on 2026-09-16:

  1. FCE Bank's script had a SyntaxError and had NEVER RUN. Six "£ mil" strings
     were written with straight double quotes nested inside double-quoted
     Python strings. The workbook on disk was real, verified and looked
     finished - built from an EARLIER version of the script that no longer
     existed anywhere. It could not be reproduced.
  2. Access Bank and National Bank of Kuwait International had scripts edited
     after their last build. The edits were sound; they simply had not been
     run, so the deliverable was a revision behind its own source.

Both are silent: the workbook opens, the verifier passes, and nothing in
either artifact says the two have diverged. `verify_workbook.py` cannot catch
this - it checks a workbook against ITSELF, and a stale workbook is perfectly
self-consistent. This check is the other axis.

WHAT IT CHECKS, cheapest first:

  compile   - every build script parses. A script that cannot parse cannot
              have produced the workbook sitting beside it.
  output    - every script names an output path and that file exists.
  freshness - no workbook is older than the script that builds it.

Freshness uses mtime, which is a heuristic in both directions: touching a
script without changing it reports a false positive, and a filesystem copy can
hide a real one. So a freshness hit is a PROMPT TO REBUILD AND DIFF, never a
verdict on its own - rebuild, then compare the cross-check and reconciliation
lines against the previous output before and after. Keep the pre-rebuild copy
until that comparison is done, not just until the rebuild finishes.

Usage:
    python3 scripts/check_builds_current.py           # report
    python3 scripts/check_builds_current.py --quiet   # only problems
"""

import glob
import os
import py_compile
import re
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build scripts end in `<workbook>.save("...FINANCIALS.xlsx")`. The receiver is
# `bw` in most scripts but not all - Shawbrook uses `b` - so the variable name
# is deliberately not anchored. Anchoring it silently skipped that one script,
# which is the same class of miss this file exists to catch.
SAVE_RE = re.compile(r"\w+\.save\(\s*['\"]([^'\"]+\.xlsx)['\"]")


def output_path(script_text):
    """The workbook a script writes, or None. The LAST save wins: a script that
    saves more than once is writing intermediate states to the same path."""
    found = SAVE_RE.findall(script_text)
    return found[-1] if found else None


def main():
    quiet = "--quiet" in sys.argv
    scripts = sorted(glob.glob(os.path.join(REPO, "scripts", "build_*.py")))

    uncompilable, no_output, missing_output, stale = [], [], [], []

    for script in scripts:
        rel = os.path.relpath(script, REPO)
        try:
            with tempfile.NamedTemporaryFile(suffix=".pyc", delete=False) as tmp:
                cfile = tmp.name
            py_compile.compile(script, cfile=cfile, doraise=True)
            os.unlink(cfile)
        except py_compile.PyCompileError as exc:
            uncompilable.append((rel, str(exc).strip().splitlines()[-1]))
            continue

        with open(script, encoding="utf-8") as fh:
            out = output_path(fh.read())
        if out is None:
            no_output.append(rel)
            continue
        out_abs = out if os.path.isabs(out) else os.path.join(REPO, out)
        if not os.path.exists(out_abs):
            missing_output.append((rel, out))
            continue

        # One second of slack: a rebuild writes the workbook moments after the
        # script is read, and some filesystems round mtimes.
        drift = os.path.getmtime(script) - os.path.getmtime(out_abs)
        if drift > 1:
            stale.append((drift / 86400.0, rel, os.path.relpath(out_abs, REPO)))

    problems = len(uncompilable) + len(no_output) + len(missing_output) + len(stale)

    if uncompilable:
        print(f"\n!! {len(uncompilable)} script(s) DO NOT COMPILE - the workbook "
              "beside them cannot have come from them:")
        for rel, err in uncompilable:
            print(f"   {rel}\n      {err}")
    if no_output:
        print(f"\n!! {len(no_output)} script(s) name no output workbook:")
        for rel in no_output:
            print(f"   {rel}")
    if missing_output:
        print(f"\n!! {len(missing_output)} script(s) name a workbook that does not exist:")
        for rel, out in missing_output:
            print(f"   {rel} -> {out}")
    if stale:
        print(f"\n!! {len(stale)} workbook(s) OLDER than the script that builds them. "
              "Rebuild, then diff the verifier output before and after - do not "
              "assume the edit was cosmetic:")
        for days, rel, out in sorted(stale, reverse=True):
            print(f"   {days:6.1f} days behind   {rel}")

    if problems == 0:
        print(f"All {len(scripts)} build scripts compile, name an existing "
              "workbook, and are no newer than it.")
    elif not quiet:
        print(f"\n{len(scripts) - problems} of {len(scripts)} scripts clean.")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
