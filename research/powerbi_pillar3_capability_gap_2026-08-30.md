# Power BI capability gap review for the UK bank / Pillar 3 summary

**Research date:** 2026-08-30  
**Scope:** Current Power BI capabilities relevant to this project's bank financial and Pillar 3-style summary. Sources are Microsoft Learn, the Basel Committee, and the PRA only. This is research, not an implementation decision.

## Conclusion

The project already has a refreshable SQLite source of truth, explicit broad-versus-strict comparability, explainable outliers, trend and parent-group analysis, and unit-aware absolute capital/RWA and size-cohort analysis. The generated HTML/PDF should remain the authoritative printable narrative.

Power BI would add a complementary exploration layer. Its greatest value is allowing a reader to begin with an unusual observation and retain the metric, period, legal entity, parent group, reporting basis, unit, source workbook, and comparability status while investigating it. That supports Basel's requirements for clear, comprehensive, meaningful, consistent and comparable Pillar 3 information.[^basel]

## Local comparison baseline

| Area | Present locally | Power BI gap/opportunity |
|---|---|---|
| Data/provenance | `research/insights.db` is the source of truth. `annual_metrics` holds FRN, source workbook linkage, raw/numeric values, unit, reporting basis, restatement and source notes. | No interactive provenance drillthrough, report semantic model, workspace lineage, or governed catalogue. |
| Comparability | IN-009 has broad annual screening and strict known-basis comparisons, with explicit exclusions. | A reader cannot slice every visual by basis, unit, eligibility, or exclusion reason. |
| Analysis | IN-009 outliers/trends, IN-010 parent-group dispersion/agreement, and IN-012 absolute capital/RWA and size-aware comparisons are implemented. | Findings are generated fixed sections/tables, not interactive investigation paths. |
| Delivery | HTML has explanatory copy, accessible table fallbacks and collapsible diagnostics; PDF is a static summary. | No drillthrough, contextual tooltips, governed access, formal Power BI release path, or interactive filtering. |
| Analysis seam | IN-013 has started a read-only shared SQLite query layer. | Power BI must not independently reimplement unfinished eligibility/trend/outlier logic. |

## Concrete Power BI capabilities missing from the current experience

| Capability | Official capability | Implementation implication for this data |
|---|---|---|
| Decomposition tree | Aggregates a measure, drills supplied dimensions in any order, and can choose AI high/low splits for root-cause exploration.[^decomposition] | Use measures such as flagged observations, strict-comparable observations, absolute YoY movement, and latest capital/RWA. Explain by metric, FY, cluster, parent group, reporting basis, unit, workbook kind, and comparability/exclusion reason. Treat AI splits as exploration, never regulatory causation. |
| Key influencers | Ranks fields associated with a selected outcome and considers the number of data points.[^influencers] | Apply only to exploratory outcomes such as `is_outlier`, `strict_eligible`, or `large_YoY_move`; retain existing deterministic rules as the official outlier definition. Show an explicit association-not-causation and sparse-disclosure warning. |
| Anomaly detection | For a line-chart time series, detects spikes/dips, shows an expected range and offers possible explanations. It requires at least four points and does not support legends, multiple values, or secondary values.[^anomalies] | Add a per-bank, one-metric history page. Use only genuinely comparable annual periods. This adds bank-specific expected-range screening, which differs from existing population percentile/robust-score/YoY outlier tests. Do not combine incompatible group/entity basis or units to lengthen series. |
| Small multiples | Splits bar, column, line or area charts into panels; line charts can use shared y-axes for level comparisons or independent scales for relative shapes. Grid is at most 6×6 before scrolling.[^smallmultiples][^linechart] | Make a selected-metric trend matrix split by peer cluster or selected banks. Require a cohort filter before showing many banks. Default to shared y-axis; label independent scale as relative trend only. |
| Field parameters | Switch fields/measures in a visual. They need explicit measures for aggregation; AI visuals and Q&A do not support them. Tooltip/drillthrough pages need the underlying fields, not the parameter object.[^parameters] | Add controlled selectors for core ratio and analysis view (level, YoY, percentile, peer median gap, coverage). Keep ratios and absolute metrics separate. Bind detail pages to `Metric ID`/`Metric`, not the parameter. |
| Bookmarks/navigation | Saves page, filters, slicers, visual selection, sort, drill location and visibility; buttons/navigators support a guided story.[^bookmarks] | Provide bookmarked entry points: Executive snapshot, Comparability & coverage, Exceptions & investigation, and Capital/RWA scale. State the preserved filters; do not rely on bookmarks as a formal PDF result. |
| Drillthrough | Passes the selected data point's filter context to a detail page for context-specific investigation.[^drillthrough] | Build a `Bank / observation detail` page keyed by FRN, metric and FY: raw value, source workbook, unit, basis, notes, strict/broad eligibility, earlier period, cluster and parent-group caveat. This is the highest-value interaction after model design. |
| Report-page tooltips | Rich, filtered hover pages can include visuals/images/elements. Screen readers cannot read report-tooltip content; Microsoft directs interactive filtered use cases to drillthrough.[^tooltips] | Use a compact, redundant disclosure-context tooltip (value, FY, unit, basis, source, eligibility). Never put required interpretation or review action only in a tooltip. |

## Model, governance and operations capabilities

| Capability | Official capability | Implementation implication for this data |
|---|---|---|
| Star-schema semantic model | Microsoft recommends a star schema with dimension tables for filtering/grouping and consistently grained fact tables for summarisation.[^star] | Model `annual_metrics` as the observation fact at FRN × metric/sheet × row label × FY. Create Date, Bank, Metric, Parent Group (with caveat/effective dates), Reporting Basis, Unit, and Quality/Comparability dimensions. Keep trend/outlier outputs in a separate findings fact; do not recompute them differently per visual. |
| Calculation groups/common measures | Calculation groups apply reusable DAX calculation items to measures and reduce duplication. Adding them makes report measures variant type and implicit measures must be handled explicitly.[^calculationgroups] | Use explicit base measures, then calculation items only where meanings are fixed: latest available, YoY, long-run change, peer median gap, percentile, broad and strict. Reconcile every DAX result with Python before release. Defer until IN-013's contract is complete/stable. |
| Lineage and data quality | Workspace lineage displays artifact relationships, external sources, refresh time and endorsed status. Microsoft also documents metadata/auditing and best-practice-rule use for model quality and governance.[^lineage][^auditing] | Carry source workbook, notes, unit, basis, refresh timestamp, coverage and quality status into the model. Add a technical quality/lineage page and data dictionary. Workspace lineage is useful operationally, but it is not cell-level source proof. |
| RLS | RLS filters rows, not columns, measures or other model objects. Microsoft recommends security groups, role testing and dimension filtering where possible.[^rls] | Do not introduce RLS for public regulatory source data alone. If internal annotations/client data are added, use Entra groups plus an access bridge through dimensions. Put confidential commentary in a separate model/report if column hiding is required; RLS cannot solve that. |
| Deployment | Deployment pipelines promote content through Development, Test and Production; Microsoft advises against manual direct publication to Test/Production. Developer mode supports projects, source control and CI/CD.[^deployment][^developermode] | Use PBIP source control, Dev/Test/Prod workspaces and a release gate: Python refresh/tests, model count/coverage checks, sampled IN-009/10/12 reconciliations, accessibility checks, then promotion. This should be a companion product release, not a replacement for HTML/PDF. |
| Accessibility | Power BI supports keyboard use, screen readers, high contrast, alt text, descriptive titles and logical tab order, but authors must configure it.[^accessibility] | Require titles that state the conclusion, useful alt text, logical tab order, sufficient contrast, no colour-only indicators, and visible table/drillthrough alternatives. The project's current visible explanations and table fallbacks are a good standard to retain. |

## Power BI export/PDF limitations

Power BI is not a drop-in replacement for the existing formal PDF. Microsoft documents that report PDF export excludes hidden and tooltip pages; does not reliably preserve several interactive states (including drilled/scroll states and bookmark-navigator selection); has URL/current-filter and bookmark-state caveats; limits reports to 50 pages and 250 MB; uses 1,280×720 rendering; and can substitute custom fonts or have page-size fidelity issues.[^pdf]

**Implementation implication:** keep the generated HTML/PDF as the controlled client summary and use Power BI for exploration. If a formal Power BI-originated pack is required, create a separate paginated report with fixed filters/layout and test its PDF. Microsoft describes the paginated renderer as physical-page based and documents accessible PDF (PDF/UA) support in the Power BI service.[^paginated]

## Recommended order — no tickets created

1. Define a semantic-model/reconciliation contract only after completing or freezing IN-013: grain, metric dictionary, broad/strict eligibility, parent-group treatment, and expected values from IN-009/10/12.
2. Build the minimum exploration report: Executive, Comparability & coverage, Exceptions with bank/observation drillthrough, and Capital/RWA scale. Add provenance tooltips and visible evidence tables first.
3. Add small multiples and decomposition tree. Add anomaly detection only to bank-level comparable annual series. Add key influencers only with an agreed outcome and non-causal wording.
4. Add accessibility acceptance tests, explicit security decision, lineage/data dictionary, PBIP source control, Dev/Test/Prod deployment and PDF acceptance tests.

This sequence protects the project's existing comparability guardrails from being weakened by attractive but ambiguous interactive analysis.

## Primary sources

[^basel]: [Basel Framework DIS10: Definitions and applications — Bank for International Settlements](https://www.bis.org/committees/bcbs/basel-framework/standard/dis/10/inforce/2027-01-01/published/2024-07-17).
[^decomposition]: [Create and view decomposition tree visuals — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-decomposition-tree).
[^influencers]: [Key influencers visualizations tutorial — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-influencers).
[^anomalies]: [Anomaly detection tutorial for Power BI — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-anomaly-detection).
[^smallmultiples]: [Create small multiples in Power BI — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-small-multiples).
[^linechart]: [Line charts in Power BI — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-line-chart).
[^parameters]: [Use field parameters in Power BI reports — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters).
[^bookmarks]: [Create report bookmarks in Power BI — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-bookmarks).
[^drillthrough]: [Set up drillthrough in Power BI reports — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-drillthrough).
[^tooltips]: [Create report tooltips in Power BI — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-tooltips).
[^star]: [Understand star schema and the importance for Power BI — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema).
[^calculationgroups]: [Create calculation groups in Power BI — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/calculation-groups).
[^lineage]: [Data lineage — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-data-lineage).
[^auditing]: [Data-level auditing implementation planning — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-auditing-monitoring-data-level-auditing).
[^rls]: [Row-level security guidance — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance).
[^deployment]: [Deploy content implementation planning — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-content-lifecycle-management-deploy).
[^developermode]: [Power BI Desktop developer mode — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/developer/projects/).
[^accessibility]: [Design Power BI reports for accessibility — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports).
[^pdf]: [Export Power BI reports to PDF — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/collaborate-share/end-user-pdf).
[^paginated]: [Export a Power BI paginated report to PDF — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/paginated-reports/report-builder/export-pdf-file-report-builder).

## UK regulatory context

The Basel source supplies the disclosure principles used in this review. For any future UK template or disclosure expansion, validate against the current PRA rulebook rather than infer requirements from a visual. The PRA's Basel 3.1 policy statement confirms that its Pillar 3 updates relate to Pillar 1 RWA calculation/disclosure.[^pra]

[^pra]: [PS9/24: Implementation of the Basel 3.1 standards — Bank of England / PRA](https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/policy-statement/2024/september/ps924-full.pdf).
