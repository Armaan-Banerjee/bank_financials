# Coverage tools

Measures how complete the Pillar 3 data is across all bank workbooks, and renders the
gap register. Reads `research/insights.db`, so run `scripts/insights/refresh_all.py`
first if build scripts have changed.

```bash
python3 research/coverage_tools/coverage.py    # headline % and per-metric/per-year breakdown
python3 research/coverage_tools/by_metric.py   # -> by_metric.json, the per-bank register data
python3 research/coverage_tools/gen_page.py    # -> disclosure_gaps.html, reads by_metric.json
```

`gen_page.py` must run after `by_metric.py`. Its header statistics are **hardcoded** —
update them by hand to match `coverage.py`'s output before republishing.

Published register (same URL on every republish):
https://claude.ai/code/artifact/20a1ec6e-d815-41f4-ab25-03bc1e707750

## What counts as a gap

The **spine** is the years a bank has real Balance Sheet data for; the **window** is its
last five such years. Coverage is measured only inside that window, so a bank that reports
three years is not penalised for the two it never had.

Three distinct states, deliberately kept apart:

| Cell reads | Treated as | Why |
|---|---|---|
| a figure | filled | — |
| empty, or "not publicly disclosed" | **open gap** | the figure exists at the bank; it just isn't published, or nobody has looked yet |
| **"not applicable"** | **removed from the denominator** | the year structurally cannot carry the metric |

That third row is the subtle one. "Not applicable" marks a year a bank could never have
reported — before it held a banking licence, or before the metric existed as a requirement.
Those cells can never be filled, so counting them as gaps overstates the remaining work and
sends researchers after figures that do not exist. Counting them as *filled* would be just
as wrong, inflating the rate. They leave the denominator entirely.

An earlier version counted them: it reported 85.4% and 1,037 open cells where the true
figures were 86.2% and 970. Fixed 2026-09-15.

**MREL is excluded throughout.** Only UK resolution entities carry an MREL requirement, so
its absence is structural for roughly 130 of the 145 banks and would swamp the signal.

**Pre-2022 NSFR blanks are structural** — the UK had no NSFR requirement or disclosure
template before 1 January 2022 (PRA PS17/21). The four-quarter-average rule pushes first
disclosures past 1 January 2023, so many FY2022 blanks are structural too, non-December
year-ends especially. `coverage.py` reports these separately at the end of its output.

## Gotchas

- **Year strings carry annotations** — `"FY2025 (y/e 30 Jun 25)"`, not `"FY2025"`. Always
  regex-extract the prefix (`re.match(r"(FY\d{4})", year)`), never compare exact strings.
  Do not compute `int(y[2:])` on the raw value.
- The register's `"ever"` field lists every year a bank **has** disclosed a metric, including
  years outside its window. That history is what separates a sourcing miss from a bank that
  genuinely never discloses, and it drives the page's "Disclosed before" filter — the
  highest-yield cohort to work.
