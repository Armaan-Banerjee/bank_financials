# Bank-level missing metric counts — FY2021–FY2025

Counts are out of 145 workbooks. A bank is counted for a metric/year when the corresponding
year column contains no numeric or dash figure on that sheet. This includes documented
non-disclosure/not-applicable entries and pending/unreached statements; it is therefore a
coverage table, not a claim that the bank failed to publish the metric. The counts below use the
corrected audit header parser, which ignores FY years embedded in unit annotations such as
“FY2025 ($'000, FY2021 conversion)”.

| Metric | FY2025 | FY2024 | FY2023 | FY2022 | FY2021 |
|---|---:|---:|---:|---:|---:|
| Balance Sheet | 8 | 1 | 0 | 3 | 7 |
| Profit & Loss | 8 | 1 | 0 | 3 | 8 |
| Cash Flow Statement | 29 | 22 | 20 | 21 | 25 |
| Asset Quality | 10 | 4 | 3 | 7 | 15 |
| KM1 Key Metrics | 61 | 48 | 44 | 50 | 73 |
| CET1 Capital | 22 | 12 | 9 | 13 | 14 |
| CET1 Ratio | 24 | 12 | 11 | 17 | 19 |
| Tier 1 Capital | 21 | 12 | 10 | 13 | 15 |
| Tier 1 Ratio | 31 | 19 | 15 | 20 | 20 |
| Total Capital | 18 | 10 | 7 | 10 | 14 |
| Total Capital Ratio | 22 | 14 | 10 | 15 | 17 |
| Total RWAs | 38 | 25 | 18 | 22 | 23 |
| RWA Breakdown | 43 | 28 | 22 | 26 | 26 |
| Leverage Ratio | 38 | 23 | 19 | 26 | 33 |
| LCR | 31 | 20 | 19 | 22 | 36 |
| NSFR | 51 | 35 | 28 | 36 | 86 |
| MREL Ratio | 136 | 136 | 136 | 136 | 136 |

Source: corrected `scripts/audit_gaps.py --json`, run 19 September 2026.

Interpretation notes: the apparent FY2025/FY2024 Balance Sheet and P&L shortfalls are mostly
publication-period effects. FY2023 has 0 missing Balance Sheet and 0 missing P&L columns. FY2024's
single missing bank is Clydesdale, which has a documented 18-month FY2025 period and no separate FY2024
year. FY2025's eight are AFIN, Kroo, RCI and UBA (latest accounts FY2024), Co-operative Bank (FY2025
Pillar 3 exists but the FY2025 statutory accounts column is not yet included), and Guaranty Trust UK,
Monument and UBP (FY2025 statutory statements marked not published yet).

KM1 totals should not be read as “banks not reporting Pillar 3”. For FY2025, 61 banks have no numeric
value in the workbook's *standard UK KM1-template* sheet. Of these, 52 have an explicit documented
non-disclosure outcome, six have no FY2025 KM1 edition/column, two are marked pending and one is an
unreached source check. The 52 are heterogeneous: the bank notes identify (approximately) 20 with no
standalone Pillar 3 disclosure, 16 that publish Pillar 3 but do not use the UK KM1 template, six whose
latest KM1 edition does not reach FY2025, and ten other documented entity-/period-specific cases. In
fact, 55 of the 61 still have other FY2025 prudential or financial figures elsewhere in their workbook;
the six with no FY2025 KM1 column are AFIN, Cambridge & Counties, Charity, Kroo, RCI and UBA, whereas
the six with no FY2025 figures on any audited sheet are AFIN, Kroo, Monument, RCI, UBA and UBP. These
are different sets. The standing
KM1 rule permits a later edition's standard-template comparative to stand in for a year whose own
edition had no table; it does not permit constructing a synthetic KM1 from separate capital sheets
when no standard-template table exists.

## FY2025 follow-up: AFIN, Kroo, RCI and UBA

The four FY2025 Balance Sheet/P&L gaps were rechecked against the live Companies House profiles on
19 September 2026. All four still show FY2024 as their latest filed accounts:

| Bank | Company | FY2025 accounts deadline | Result |
|---|---:|---:|---|
| AFIN Bank | 13090556 | 30 Sep 2026 | Not filed yet; FY2024 remains latest |
| Kroo Bank | 10359002 | 31 Dec 2026 | Not filed yet; FY2024 remains latest |
| RCI Bank UK | 11429127 | 30 Sep 2026 | Not filed yet; FY2024 remains latest |
| UBA UK | 03104974 | 31 Dec 2026 | Not filed yet; FY2024 remains latest |

Therefore no FY2025 statutory balance-sheet or P&L figures can be added safely at this date. AFIN and
RCI are approaching their filing deadline; Kroo and UBA are not yet due. The workbook build notes also
record that no FY2025 Pillar 3 edition was found for these four, so there is no prudential document that
can substitute for the statutory statements.
