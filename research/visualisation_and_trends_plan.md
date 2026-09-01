# Visualisation and deeper-trends plan

**Date:** 2026-08-30  
**Scope:** planning only; no production visualisation code is proposed in this note.

## Executive recommendation

The next analytical layer should be a **coverage-aware, entity-level exploration product** built around robust distributions, trajectories, rank movement, cross-metric relationships, peer-relative comparisons, and source-quality drillthrough. The existing up/down trend bars should remain as an orientation view, but should not be the main analytical surface.

The strongest initial implementation choices are:

1. **Python-first analysis with Plotly or another Python charting layer**, generating a self-contained enhanced HTML pack and controlled PDF companion.
2. Keep the existing repo-native HTML/SVG/PDF approach as a fallback for deterministic, dependency-light output; introduce a charting library only where it materially improves distribution, rank, or linked analytical views.
3. Treat Vega-Lite/ECharts as future alternatives if interaction density or portability becomes a constraint; they are not needed to choose the next analytical slice.

Power BI should be retained as a possible enterprise/analyst companion because the repository already has a star-schema hand-off and report-experience contract. Superset or Metabase make sense for internal SQL self-service, not as the core advanced-statistics layer. Flourish is best reserved for selected editorial storytelling.

## Product brief agreed for the next iteration

- **Audience:** banking- and Basel-literate readers who need a fast, defensible summary across the full bank population and do not have time to inspect every workbook.
- **Primary output:** an enhanced HTML research pack with a matching controlled PDF pack.
- **Default analytical mode:** broad comparability for discovery and pattern-finding, with strict/comparable cohorts available as a validation lens where reporting basis, units, or entity perimeter materially affect the result.
- **Implementation preference:** Python-first, reusing the existing SQLite pipeline and generating derived analytical tables/figures from the same snapshot.

The pack should be designed as a layered read:

1. **Executive page:** the few most important sector findings, each with direction, magnitude, comparable N, and a short caveat.
2. **Diagnostic pages:** distribution, ratio decomposition, persistent trajectories, rank movement, and cross-metric divergence.
3. **Investigation appendix:** bank-level tables, source lineage, quality flags, basis/unit notes, and reviewed outliers.

This audience does not need every chart to be interactive. Interactivity should be reserved for filtering and validating a finding; the PDF should remain intelligible without hover states or hidden tooltips.

## What is in the data now

The source of truth is `research/insights.db`, not the generated CSV. It contains:

- 145 bank entities and 12,846 annual metric rows;
- 12 metric families: capital amounts/ratios, RWAs, leverage, liquidity, MREL, and cash flow;
- 1,498 interim observations covering quarterly, semi-annual, and point-in-time disclosures;
- parent-group lookup/edges, cluster outputs, source notes, raw values, quality fields, and a Power BI star-schema export;
- annual data from FY2020–FY2026, but with uneven coverage and non-standard year labels.

The current pipeline already implements several important safeguards: stable FRN keys, missing values as missing rather than zero, broad versus strict comparability, robust outlier screening, unit-aware absolute analysis, rank movement, parent-group dispersion, regulatory headroom screening, and source-lineage outputs.

### Evidence that surface-level averages are unsafe

The live database profile shows the following numeric coverage in FY2025:

| Metric | Banks with numeric observations | Median | 90th percentile | Maximum |
|---|---:|---:|---:|---:|
| CET1 ratio | 97 | 18.0% | 79.4% | 331.0% |
| Leverage ratio | 82 | 9.45% | 21.4% | 980,935% |
| LCR | 86 | 244.1% | 579.7% | 9,081.1% |
| NSFR | 73 | 148.7% | 260.4% | 20,366.5% |
| Total RWAs | 91 | 117,463 | 2,624,404 | 169,516,391 |

The maxima are not necessarily errors, but they demonstrate that arithmetic means and ordinary linear axes can be dominated by atypical RWA denominators, reporting conventions, or small entities. Use medians, quantiles, MAD/IQR, log axes for positive amounts, winsorised or robust summaries, and explicit outlier flags.

The annual directional results also show why direction alone is incomplete. For broad comparable CET1 ratios, FY2023→FY2024 had 63 declines and 44 rises across 110 entities, while the median change was only -0.48 percentage points. The important questions are therefore: how large were the changes, which banks moved persistently, did the distribution shift, and were changes concentrated in a size/basis/peer cohort?

## Recommended visual analyses

### 1. Ratio decomposition: capital versus RWA — highest priority

**Question:** Why did a bank's capital ratio change?

A falling CET1 ratio can result from CET1 capital falling, RWAs increasing faster than capital, or both numerator and denominator growing at different rates. Use a four-quadrant scatter plot:

- x-axis: percentage/log change in total RWAs;
- y-axis: percentage/log change in CET1 capital;
- colour: CET1-ratio change in percentage points;
- point size: latest CET1 capital, only where units and basis are comparable;
- tooltip/drillthrough: numerator, denominator, ratio, unit, basis, source, and eligibility.

IN-012 already contains the absolute capital/RWA work needed to support this view, with roughly 84 banks having known-unit CET1 observations and about 79 suitable for scale-adjusted comparisons. This is likely the most valuable missed view because it turns “capital ratio down” into an interpretable balance-sheet mechanism while preserving the caveat that it is not causal.

### 2. Distribution and coverage explorer

**Question:** What does the sector distribution look like, and how much of it is actually comparable?

Visuals:

- violin/box/strip or beeswarm plot by metric and fiscal year;
- ECDF with selectable bank, parent group, cluster, and reporting basis;
- percentile-band trend (p10, median, p90) with comparable N beside each year;
- bank × metric × year disclosure heatmap, with missing/non-numeric/basis-unknown states separated;
- default to broad comparability for discovery, with a visible broad/strict toggle and an explanation of what changes between modes.

Why it matters: this exposes skew, cohort changes, missingness, and the difference between a sector-wide distribution shift and a handful of extreme observations. It also makes the current coverage weakness of NSFR/MREL visible instead of hiding it behind a headline.

### 3. Fixed-panel trajectory and rank movement

**Question:** Which banks are persistently moving, and which are merely noisy or entering/leaving the sample?

Visuals:

- bank small multiples with a common metric scale and a clear missing-data state;
- slopegraph/bump chart for percentile rank at two selected years;
- “trajectory fingerprint” matrix: four adjacent-year changes coloured by sign and sized by magnitude;
- persistence table: number of consecutive declines/rises, total change, median annual change, and number of comparable years.

Initial candidates for review from the existing data include persistent CET1 declines for ClearBank, GB Bank, Lloyds Bank, OakNorth, RBS, Union Bank of India UK, and Vanquis, alongside persistent rises for Bank Sepah, Goldman Sachs International Bank, and Unity Trust. These are review queues, not conclusions: each needs basis, entity, denominator, and source-note inspection.

Rank views should use a fixed eligible panel when measuring rank movement. A separate “all available” view can show coverage churn, but it must not be presented as the same trend.

### 4. Change-versus-level quadrant

**Question:** Which banks have low/high current levels and are improving/deteriorating?

For a selected metric and period:

- x-axis: latest level or percentile rank;
- y-axis: robust change from prior year or multi-year slope;
- point size: log total RWAs or capital amount where units/basis permit;
- colour: parent group or capital-buffer cluster;
- labels: only reviewed outliers, with a searchable table for all entities.

This distinguishes “high but falling”, “low but improving”, “high and stable”, and “low and falling”—four materially different stories that a red/blue direction bar cannot show.

### 5. Cross-metric divergence and resilience map

**Question:** Are capital, leverage, liquidity, and scale moving together?

Use a linked scatterplot matrix or heatmap of robust rank correlations and a bank-level divergence table. Candidate derived fields:

- CET1 change versus leverage change;
- CET1 change versus LCR/NSFR change;
- capital amount growth versus RWA growth;
- ratio change decomposed into numerator growth and denominator growth where the underlying capital/RWA amounts are comparable;
- a divergence flag when capital improves while liquidity worsens, or vice versa.

The FY2023→FY2024 data already shows examples such as NatWest Markets (capital ratios up while LCR fell), the Co-operative Bank (capital ratios down while NSFR rose), and Credit Suisse UK (large CET1 increase with LCR decline). These are useful investigation paths, not causal findings. Extreme leverage/liquidity values must be excluded or transformed before correlation calculations.

### 6. Scale and denominator analysis

**Question:** Are apparent ratio outliers a property of the business or of a very small denominator?

Visuals:

- log-log scatter of CET1 capital, total RWAs, and CET1 ratio;
- size-cohort distributions using small/medium/large bands, with cohort cut points recomputed from the selected year;
- capital growth versus RWA growth quadrant;
- “ratio reliability” view showing numerator, denominator, ratio, unit, and basis together;
- optional robust regression/LOESS line, clearly marked exploratory.

This is particularly important for Afin, Chetwood, BNY Mellon, and other entities already flagged for unusual ratios or denominators.

### 7. Parent-group and legal-entity dispersion

**Question:** Does membership in the same parent group imply similar behaviour?

Use a parent-group dot plot or connected small multiples showing each legal entity, group median, within-group range, and trend agreement. Keep entity-level observations separate from parent-level observations. Add effective dates and acquisition/restructuring annotations from `parent_group_edges`.

The current evidence suggests alignment in some capital measures for HSBC and NatWest, but mixed cash-flow or entity-specific behaviour in Lloyds and Santander. This is exactly where a group aggregate would conceal useful information.

### 8. Disclosure cadence and data-quality dashboard

**Question:** Where can the product support strong inference, and where is the evidence thin?

Visuals:

- bank × year publication/observation calendar;
- metric coverage by cadence (annual, semi-annual, quarterly, point-in-time);
- source and basis-quality funnel;
- uncertainty badge beside every chart: comparable N, strict/broad mode, unit/basis count, and number of unresolved label collisions;
- source-trace drillthrough to workbook, row label, raw value, source note, and source URL.

Only 14 banks currently contribute interim observations, and LCR/NSFR interim coverage is much thinner than capital metrics. A cadence view prevents users from interpreting a publication gap as a stable bank trend.

### 9. Regulatory headroom and observed erosion

The current IN-021 output should not yet be treated as an analytical finding: its records are currently classified as `no_regulatory_context`, despite regulatory-context artefacts existing in the repository. First diagnose the matching policy between `research/in021_headroom_trajectory.json` and `research/powerbi/regulatory_context.json`. Once valid matches exist, use a ranked dot plot or bullet chart of observed headroom and multi-year erosion, split into `screened`, `insufficient_evidence`, and `no_regulatory_context`. Do not forecast breach dates from this dataset. Keep the current IN-021 policy: screening only, no projected breach or future value.

## Statistical rules for the next layer

- Report **N and denominator** next to every distribution, trend, percentile, and rank statistic.
- Prefer median, IQR, MAD, trimmed mean, and quantile bands; show the mean only as a secondary diagnostic.
- Use percentage-point changes for ratios, relative/log changes for positive amounts, and never mix units or reporting bases without an explicit conversion.
- Use robust scaling and winsorisation only for exploratory visuals, while preserving raw values and showing which observations were clipped or excluded.
- Separate level outliers from movement outliers. A bank can be structurally high without having an unusual annual change.
- Make sample entry/exit visible. Compare fixed panels for ranks and all-available cohorts for coverage monitoring.
- Treat correlations, clusters, anomaly flags, and regression lines as exploratory and non-causal.
- For broad exploratory visuals, expose the reporting-basis/unit mix and allow a strict validation view rather than suppressing potentially useful patterns too early.
- Add bootstrap confidence intervals for medians/quantiles only when the cohort is large enough and the resampling unit is the bank, not individual rows.
- Use permutation tests or robust effect sizes for cohort comparisons rather than relying on p-values alone; small and selected bank cohorts make formal significance fragile.
- Preserve the source note and comparison eligibility behind every plotted observation.

## Tool/platform research

The following claims are based on first-party documentation.

| Tool | Useful strengths for this product | Main limitation/role |
|---|---|---|
| Vega-Lite | Declarative aggregation, binning, density, quantiles, regression/LOESS, faceting, linked selections, and portable JSON specifications. [Transform docs](https://vega.github.io/vega-lite/docs/transform.html) · [regression](https://vega.github.io/vega-lite/docs/regression.html) · [overview](https://vega.github.io/vega-lite/docs/) | Statistical modelling beyond visual transforms belongs upstream; best as a governed chart specification layer. |
| Observable Framework | Strong notebook-to-static-app workflow and a natural narrative/research surface around linked charts. [Framework](https://observablehq.com/framework/) · [embeds](https://observablehq.com/framework/embeds) | JavaScript/data-loader workflow adds a second runtime beside the Python pipeline. |
| Plotly/Dash | Box, violin, ECDF, scatter-matrix, facets, distributions, error bands, and linear/nonlinear trendlines; Dash supports Python app callbacks. [Statistical charts](https://plotly.com/python/statistical-charts/) | More procedural and application-oriented; deployment and callback architecture need to be designed. |
| Apache ECharts | Declarative transforms, rich events/actions, data zoom, drilldown-style interactions, Canvas/SVG rendering, and server-side rendering options. [Transforms](https://echarts.apache.org/handbook/en/concepts/data-transform/) · [events](https://echarts.apache.org/handbook/en/concepts/event/) · [SSR](https://echarts.apache.org/handbook/en/how-to/cross-platform/server/) | More frontend engineering; analytical semantics need to be documented in application code. |
| Power BI | Existing semantic-model path; strong drillthrough, decomposition tree, key influencers, anomaly detection, bookmarks, and governed slicers. [Drillthrough](https://learn.microsoft.com/en-us/power-bi/guidance/report-drillthrough) · [key influencers](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-influencers) | Licensing/capacity and export constraints; retain generated HTML/PDF as controlled narrative outputs. |
| Tableau | Mature trendlines, clustering, predictive modelling, reference lines, and dashboard actions. [Trendlines](https://help.tableau.com/current/pro/desktop/en-us/trendlines_add.htm) · [predictions](https://help.tableau.com/current/pro/desktop/en-us/predictions_overview.htm) | Commercial platform and governance overhead; strongest as analyst workbench if already licensed. |
| Apache Superset | SQL-first exploration, dashboards, filters, and self-hosted deployment/embedding. [Dashboard workflow](https://superset.apache.org/user-docs/using-superset/creating-your-first-dashboard/) · [embedding](https://superset.apache.org/user-docs/6.1.0/using-superset/embedding/) | Advanced robust statistics would remain upstream in Python/SQL. |
| Metabase | Easy query-builder/dashboard experience and modular/full-app embedding. [Embedding](https://www.metabase.com/docs/latest/embedding/start) | Lower analytical/statistical depth; better for internal self-service than the core product. |
| Flourish | Fast narrative templates, animation, and embeddable public storytelling. [Publishing/embedding](https://helpcenter.flourish.studio/hc/en-us/articles/8761565550607-Exporting-publishing-embedding-and-sharing) | Prepare statistics upstream; unsuitable as the governed source-linked analytical core. |

## Suggested delivery sequence

### Phase 1: analytical contract and quality surface

Define one long-format visualisation view in SQLite or an exported analytical table with: FRN, display name, metric, period, numeric value, unit, reporting basis, comparability status, source, quality status, parent group, cluster, size cohort, and derived change/rank fields. Add tests for denominator, fixed-panel eligibility, outlier treatment, and no unit/basis mixing.

### Phase 2: four high-value views

Build ratio decomposition, distribution/coverage, trajectory/rank, and source-quality/drillthrough views. Use one selected metric and year range first; generalise only after the interaction contract is clear.

### Phase 3: relationships and context

Add cross-metric divergence, scale/denominator, parent-group dispersion, interim cadence, and headroom views. Add regulatory and acquisition annotations only where the source evidence is explicit.

### Phase 4: Python-first productionisation

Implement the selected views in Python, preferably by adding a reusable analytical-view layer that reads the SQLite snapshot and emits both HTML-ready data/figures and PDF-safe static figures. Decide between Plotly and the existing SVG approach based on export fidelity, accessibility, source-trace behaviour, and maintenance cost—not chart count. A full dashboard framework is optional; the primary artefact is the enhanced HTML/PDF pack.

## Remaining decision

The main unresolved scope question is whether regulatory headroom should be part of the next pack after its matching policy is repaired, or remain an explicitly deferred appendix until the regulatory context has broader coverage.
