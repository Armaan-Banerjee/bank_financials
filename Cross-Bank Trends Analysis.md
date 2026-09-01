# Cross-Bank Trends Analysis

Analysis of the 145 bank entities in `research/bank_metrics.csv`, using the
FRN as the entity key. The CSV is IN-001's normalized source of truth; figures
were not re-derived directly from workbooks. The repeatable extraction and
checks are in `scripts/insights/analyze_trends.py`.

The original 29-bank analysis supplied four findings. This pass re-checked
those findings at the full-bank scale and added a within-parent-group view
using `research/bank_parent_groups.md`. Comparisons below use the best numeric
series selected deterministically per FRN and metric, but should still be read
with each entity's basis and source-year notes in mind.

## 145-bank refresh

| Metric and comparison | Comparable entities | Down | Up | Unchanged | Interpretation |
|---|---:|---:|---:|---:|---|
| CET1, FY2021→FY2022 | 99 | 58 | 39 | 2 | Broad softening remains visible |
| Total capital, FY2021→FY2022 | 96 | 55 | 38 | 3 | Broad softening remains visible |
| CET1, FY2023→FY2024 | 108 | 61 | 44 | 3 | Broad softening remains visible |
| Total capital, FY2023→FY2024 | 101 | 58 | 42 | 1 | Broad softening remains visible |
| LCR, FY2021→FY2022 | 73 | 38 | 35 | 0 | Near-even; the original majority does not generalize |
| Operating cash flow, FY2021→FY2022 | 109 | 60 | 49 | 0 | Slight negative majority, not universal |

Counts are directional checks, not estimates of causal effects. “Down” and
“up” mean the selected numeric value changed between the two labelled fiscal
years; entities without both years are excluded from that row.

### 1. Leverage ratio reporting basis changed around FY2022

This finding survives as a disclosure-methodology caveat, not as an economic
shock. Multiple entities retain parallel leverage rows around the transition,
including variants that include or exclude central-bank claims and explicit
2022 KM1-format rows. A pre/post-2022 leverage comparison must therefore use
the like-for-like row and preserve the entity's reporting-basis note.

### 2. Operating cash flow moved sharply around FY2022, especially at larger entities

The full dataset still shows the original direction, but less dramatically:
60 of 109 comparable entities declined and 49 rose. The clearest examples
remain the larger or more balance-sheet-sensitive entities, where operating
cash flow can change sign. For example, the existing sample's Barclays, RBS,
Santander UK and Co-operative Bank moves remain present in the normalized data.
The broader result should be described as a 2022 concentration of large moves,
not a universal banking-sector reversal. The 2023→2024 check reverses the
directional balance (70 up versus 49 down across 119 entities), consistent with
reversal in several large entities.

The timing remains compatible with the 2022 rate-hiking, gilt-market and
balance-sheet-liability environment, but the normalized data alone does not
establish causation. Cash-flow totals also differ in consolidation perimeter
and business mix, so this is a pattern for investigation rather than a
valuation or stress conclusion.

### 3. LCR softening in FY2021→FY2022 is sample-sensitive

The original 16-bank sample had 10 declines and 6 rises. At full scale, only
73 entities have comparable selected LCR values: 38 declined and 35 rose.
That is a small directional majority, but not strong evidence of an
industry-wide event. The finding is therefore downgraded to a near-even,
sample-sensitive pattern. Possible funding-market explanations such as the
TFSME drawdown window closing remain hypotheses, not conclusions supported by
this cross-sectional check alone.

### 4. Capital ratios softened in two windows

This finding is strengthened by the larger sample. Both CET1 and Total Capital
show a clear downward majority in FY2021→FY2022 and FY2023→FY2024 (see the
table above). The pattern is consistent with a mixture of IFRS 9 transitional
relief tapering and post-COVID balance-sheet/RWA growth, but reporting-basis
changes and entity-specific events remain material caveats. The counts show
directional prevalence, not that every decline has the same cause.

## Additional time-cluster scan

The scan also covered operating-cash-flow totals and headline CET1, Total
Capital, Leverage, LCR and NSFR rows for every available fiscal year. No new
time-clustered pattern was sufficiently broad, comparable and robust to the
known single-bank quirks to add as a standalone finding.

NSFR is especially unsuitable for a simple long-run event claim: only 35
entities have comparable FY2021→FY2022 values because adoption and disclosure
windows differ. The 2023→2024 direction (46 down, 37 up, 3 unchanged among 86)
is worth monitoring, but is not promoted to a finding without more like-for-
like basis and cadence control.

## Within-parent-group comparison

The IN-002 lookup contains six parent groups with at least two built entities.
The comparison below uses FRN joins and retains legal-entity distinctions;
group membership does not justify substituting a parent's consolidated metric
for an entity's own disclosure.

| Group | Built entities | FY2021→FY2022 result |
|---|---|---|
| HSBC group | HSBC Bank plc; HSBC Innovation Bank; HSBC UK Bank plc; Marks and Spencer Financial Services | CET1 declined in all three comparable entities; Total Capital was mixed because HSBC Bank plc was flat while the other two declined; operating cash flow was mixed |
| Lloyds Banking Group | Bank of Scotland; Lloyds Bank; Lloyds Bank Corporate Markets | CET1, Total Capital and operating cash flow were mixed, showing entity-specific perimeter/business effects |
| NatWest group | National Westminster Bank; NatWest Markets; RBS | CET1 and Total Capital declined in all three; LCR declined in the two comparable entities; operating cash flow was mixed because NatWest Markets rose while the other two declined |
| Banco Santander S.A. | Cater Allen; Santander Financial Services; Santander UK | Operating cash flow was mixed: Cater Allen rose, while Santander Financial Services and Santander UK declined |
| UBS group (current) | Credit Suisse International; Credit Suisse UK | Operating cash flow rose in both comparable entities, but the Credit Suisse/UBS acquisition and wind-down transition makes this a perimeter-sensitive comparison |
| JPMorgan Chase group | J.P. Morgan Europe; J.P. Morgan Securities | No FY2021→FY2022 pair was sufficiently populated by the selected headline series for a directional claim |

The strongest within-group evidence is therefore directional capital alignment
at HSBC and NatWest, alongside divergence in operating cash flow and in the
Lloyds/Santander entity sets. This supports using group membership as an
additional analytical dimension, not as a replacement for entity-level
metrics. Historical acquisitions, ring-fencing and solo-versus-group bases
must remain visible in any downstream chart.

## Flagged as noise, not signal

- **LCR/NSFR “every bank moved” statistics.** These ratios commonly sit at
  100–1000%+, so small year-on-year movements are not economically comparable.
  The full-bank LCR result above is deliberately reported as near-even.
- **Leverage pre/post-2022 raw comparisons.** Parallel rows and the central-bank
  claims treatment make an unqualified before/after comparison misleading.
- **Monzo's CET1 swings (99%→155%→54%).** This is the known Monzo Bank Ltd →
  Monzo Bank Holding Group restructuring/entity-identity artifact.
- **Chetwood's LCR (51,086%→4,823%→1,015%→194%) and BNY Mellon's very high
  capital ratios.** These reflect unusually small or atypical RWA bases and are
  not comparable to mainstream retail-bank movements.

## Notable standalone outlier

**Vanquis** still shows a sustained CET1 decline every year from FY2021 to
FY2025 (29.1% → 26.4% → 20.5% → 18.8% → 16.5%), rather than only participating
in a single sector-wide window. This remains consistent with its own
credit-quality and restructuring context and is not evidence of a universal
banking-sector trend.

## Method and limitations

The analysis uses the normalized FRN-keyed rows from IN-001. For each metric and
FRN, `scripts/insights/analyze_trends.py` applies explicit headline-label priorities,
including the requested leverage-ratio-excluding-central-bank rule and the
primary net operating-cash-total rule, then uses coverage and alphabetical
tie-breaking within the remaining candidates.
It extracts the year from the disclosure label, prefers an unqualified `FY####`
period when multiple labels represent the same year, reports those collisions,
and compares only entities with both years present. The live run found only two
remaining leverage-label ties and two operating-cash-flow-label ties; it also
reported 25 leverage and eight operating-cash-flow same-year period collisions.
Those collisions are now visible diagnostics, but they remain a reason to treat
exact values in those two metrics as provisional until the affected entities are
reviewed on a like-for-like basis. The script reports basis-note variation too;
the current selected rows did not expose additional basis-note variants.

This is a durable screening method, not a substitute for reading source notes:
disclosure basis, consolidation perimeter, restatements, FX conversions,
interim/annual cadence, and entity changes can all affect a series. Findings are
retained only when they survive those known-quirk checks documented in the build
reviews.
