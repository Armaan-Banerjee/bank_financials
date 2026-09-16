# nd_targets.json — read this before using the list

`nd_targets.json` lists every **bank-year** whose Pillar 3 cells read "Not publicly disclosed"
while the script also cites an Annual Report / Companies House document for that same year.

Schema: `{script: {FY####: {"metrics": [sheet names], "doc": "<AR constant name>"}}}`.

Produced 2026-09-16 by an AST parse of all 145 build scripts (no execution, no fetching):
each script's `YEARS`, every `{year: "Not publicly disclosed"}` dict, every
`add_not_disclosed_metric_sheets(...)` call (whole sheets × every year), and every year-specific
AR/CH URL constant. **78 scripts, 487 bank-years.**

## Caveats — these are not optional context, they change what the list means

A machine-readable list with a clean schema is exactly the artifact a later reader will
over-trust, so:

- **It records where WE failed to find something, not where the BANK asserted publication.**
  Those are different sets that overlap only by accident.
- **It cannot see the case that matters most.** A bank-year whose cells were filled *from the
  Annual Report*, while that AR says a separate Pillar 3 was published, looks complete and never
  appears here. Melli was exactly that shape — and Melli is the instance that started this line of
  work. Any sweep scoped to this list inherits that blind spot.
- **It is inflated by metrics that never applied.** MREL at a firm that is not a UK resolution
  entity, LCR/NSFR before phase-in, anything pre-CRD IV. `nd_classified.json` quantifies this:
  the large majority of the 487 are MREL or pre-phase-in rows, i.e. cells the project's own
  convention would mark "Not applicable" rather than "Not publicly disclosed".
- **It is year-level, not metric-truth-level.** "metrics" names the sheets that carried the
  "Not publicly disclosed" string; it does not assert the figure exists at the bank.
- **An earlier, superseded version of this list said 17 scripts.** That was a grep heuristic and is
  wrong; it missed ~60 scripts. Use the AST figure (78 / 487).

## Related

- `nd_classified.json` — same rows bucketed as fully_structural / MREL_only / needs_human_read,
  with the rule applied. Counts only; **no cell in the repo was changed by me.**
- `RESUME_peer_search.md` — the running log of the link-rot and discovery work these came from.
