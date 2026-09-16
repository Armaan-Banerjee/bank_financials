# RESUME — OneSavings Bank plc: entity-level (solo) LCR

Task: purely ADDITIVE. Add OSB-solo (entity-level, point-in-time) LCR figures
that the OSB Group Pillar 3 documents state in NARRATIVE text, on their own
separately labelled row. Do NOT touch, re-label or withdraw any existing
parent-group figure — that scoping question is escalated elsewhere
(`research/RESUME_entity_basis_sweep.md`).

## Hard rule

The Group UK KM1 LCR rows already on the sheet (FY2022 197.0%, FY2021 195.5%,
FY2023 197.1%, FY2024 188.0%, FY2025 169.5%) are **12-month averages**.
The solo figures below are **point-in-time at 31 December**. Different
measures. Never merge, average, reconcile, or put on the same row.

Corroboration that they are different measures, from the primary itself:
FY2022 Pillar 3 p.9 prints BOTH — Group 12-month-average LCR 197.0% in UK KM1
row 17 on the same page, and in the "Liquidity Ratio" narrative "the Group LCR
was 185%" point-in-time. 197.0 vs 185 for the same Group at the same date.

## Document verification (all done 2026-09-16)

All PDFs fetched with `curl -L`, HTTP 200 + `application/pdf` + `%PDF` magic
bytes confirmed individually. Control filename
`https://www.osb.co.uk/media/nwwagqwf/this-file-does-not-exist-xyz.pdf`
returned a hard 404 (0 bytes) — no soft-404 behaviour on that host/directory.
No file was 1,048,576 bytes. Every edition dated from its own COVER page.

| Edition (cover) | URL constant | Pages | Solo LCR stated? |
|---|---|---|---|
| "PILLAR 3 DISCLOSURES For the year ended 31 December 2019" | P3_2019_URL | 73 | YES 199.4% |
| "...31 December 2020" | P3_2020_URL | 76 | YES 254.1% |
| "...31 December 2021" | P3_2021_URL | 72 | YES 240.1% |
| "...31 December 2022" | P3_2022_URL | 72 | YES 229% |
| "...31 December 2023" | P3_2023_URL | 90 | NO |
| "...31 December 2024" | P3_2024_URL | 94 | NO |
| "...31 December 2025" | P3_2025_URL | 72 | NO |

### Verbatim sentences (printed page = PDF page in every case; footers checked)

- **FY2019 — 199.4%**, p.8 (§1 Introduction and Key Regulatory Metrics,
  narrative under Table 1: Key metrics) and repeated p.60 (§9 Liquidity,
  under Table 50):
  "The liquidity for both OSB and CCFSG Banks remains strong. OSB solo has a
  Liquidity Coverage Ratio ('LCR') of 199.4% and CCFSG Bank 143.9%."
  p.60 adds: "Both OSB and CCFS' LCR at 199.4% and 143.9% respectively remain
  well above risk appetite and regulatory minimums."
- **FY2020 — 254.1%**, p.7 (§Key regulatory metrics, narrative under Table 1)
  and p.62 (§9 Liquidity, under Table 37):
  p.7: "The liquidity for both OSB and CCFSL remains strong. OSB solo has a
  Liquidity Coverage Ratio (LCR) of 254.1% and CCFSL 146.0%."
  p.62: "...OSB solo has a Liquidity Coverage Ratio (LCR) of 254.1%
  (Dec 19: 199.4%) and CCFSL 146.0% (Dec 19: 145%)." — independently
  confirms the FY2019 value.
- **FY2021 — 240.1%**, p.8 (§1.6 Key regulatory metrics, narrative under
  Table 4: Key metrics):
  "The liquidity for both OSB and CCFSL remains strong. OSB has a Liquidity
  Coverage Ratio (LCR) of 240.1% (2020: 254.1%) and CCFSL 157.9%
  (2020: 146.0%)." — independently confirms the FY2020 value.
- **FY2022 — 229%**, p.9 (§Liquidity Ratio narrative, directly under UK KM1):
  "As at 31 December 2022, OSB had a Liquidity Coverage Ratio (LCR) of 229%
  and CCFSL 148% (31 December 2021: 240% and 158%, respectively) and the
  Group LCR was 185% (31 December 2021: 196%)..."
  Transcribed as printed, "229%" — NOT normalised to 229.0%.

### Years with NO solo figure — left blank, not interpolated

FY2023, FY2024, FY2025. Each edition's Liquidity Ratio narrative gives only
the Group 12-month average ("The Group had a 12-month average Liquidity
Coverage Ratio (LCR) of 197.1% / 188.0% / 169.5%"). Searched each edition for
"OSB had", "OSB has", "solo", "LCR of", "CCFSL <number>": the only remaining
"solo" hits are risk-appetite prose ("Liquidity Risk management is carried out
at a solo bank level"), no numbers. No value carried across.

## Change made to build_onesavings.py

- `LCR` sheet: added ONE row,
  "Liquidity Coverage Ratio — OneSavings Bank plc solo (entity level),
  point-in-time at 31 December (%)", values FY2022 229% / FY2021 240.1% /
  FY2020 254.1% / FY2019 199.4%. Existing three Group rows untouched.
- New `LCR_SOURCES` string (LCR sheet only — the other 10 Pillar 3 sheets keep
  `p3_sources()` unchanged) citing document, printed page and narrative
  location per year.
- Sheet note rewritten to state the average-vs-point-in-time distinction
  explicitly, plus the 197.0 / 185 same-page proof.
- Overview "Pillar 3 Key Metrics" block: matching added row
  "LCR — OSB solo (entity level), point-in-time" (Overview is a COPY).
  Overview note extended.
- No existing figure changed anywhere.

## FY2019 basis question — REPORTED ONLY, nothing populated

See the final report. Short version: the FY2019 edition's own scope section
(p.5 Overview, p.6 "Scope and basis of disclosure") says it is
OneSavings Bank plc's OWN consolidation, and no parent existed above OSB plc
at 31 December 2019 (OSBG inserted November 2020). No cell was filled.

## Downstream consequence flagged, NOT actioned

`scripts/insights/extract_metrics.py` records every labelled row.
`in009_analysis.py::_select_metric_observations` picks the highest-count label
per FRN (Group row, 5 years) but then, for a year where ONLY the solo row has
a value, falls through to the solo row. So a future `refresh_all.py` would
make OSB's FY2019/FY2020 LCR series entries point-in-time solo while
FY2021-FY2025 stay 12-month-average Group. `analyze_trends.py` is unaffected
(its `LABEL_PRIORITY` exact-match is the first sort key).
refresh_all.py was NOT run.
