# Profitability gap sweep — Monument and Tandem (round 3, 2026-10-12)

## Outcome

No new ROE, ROA or RoTE value can be collected for either bank under the
explicit-publication rule.

| bank | FY2025 result | exact perimeter | disposition |
|---|---|---|---|
| Monument Bank Limited | **Unresolved** — exact report found, but no value is accepted | Monument Bank Limited, company 10921940; the report is group accounts for the Bank and its subsidiary | Keep the FY2025 null/acquisition gap. Do not use a third-party ratio or calculate one from the statements. |
| Tandem Bank Limited | **No explicit ROE, ROA or RoTE is published in the exact bank report** | Tandem Bank Limited, company 00955491, company-only accounts | Close as a genuine non-disclosure. Do not substitute Tandem Money Limited group figures. |

No JSONL, README, worksheet, script, curated store, extract, CSV/XLSX or
deliverable was changed.

## Monument Bank Limited

The exact FY2025 source is now unambiguous:

- Monument's own [Financial Information page](https://webflow.dev.www.monument.co/annual-reports)
  lists a **2025 Annual Report** and links the first-party CDN PDF:
  [Monument Bank Limited — 2025 Annual Report](https://cdn.prod.website-files.com/6435124ea79f72c265f72807/6ab68b85f380864b01e45564_Monument%20Bank%20Limited%20-%202025%20Annual%20Report.pdf).
- [Companies House filing history](https://find-and-update.company-information.service.gov.uk/company/10921940/filing-history)
  independently identifies the same legal entity, company **10921940**, and
  records 166-page group accounts made up to 31 December 2025, filed 1 October
  2026. The direct document is
  [document `MzU0ODQzMjY2OWFkaXF6a2N4`](https://find-and-update.company-information.service.gov.uk/company/10921940/filing-history/MzU0ODQzMjY2OWFkaXF6a2N4/document?format=pdf&download=0).
- The Bank's official page states that Monument Bank Limited is company
  10921940 and PRA/FCA FRN 849724, confirming that this is the requested bank,
  not the unrelated US bank or Monument Mining.

Both first-party PDF routes failed at the document layer in this run: the CDN
object could not be opened, while Companies House redirected to an expired or
otherwise inaccessible signed object. The repository's hashed document cache
contains Monument's 82-page FY2024 filing, verified locally as the report that
publishes ROE of -22%/-44% for FY2024/FY2023, but it does **not** contain the
new 166-page FY2025 filing. Broad exact-title, exact-URL, company-number,
`"Return on Equity"`, `ROE`, `ROA` and `RoTE` searches exposed no indexed text
from the FY2025 document.

Accordingly, no FY2025 return value is recorded. In particular, a ratio must
not be back-solved from loss and equity, and third-party calculated ROE/ROA is
not evidence of an explicitly published bank KPI. The remaining decisive task
is acquisition and whole-document OCR of the 166-page PDF, with likely KPI
pages rendered for visual confirmation.

## Tandem Bank Limited

The exact bank source is also pinned down:

- [Companies House filing history](https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history)
  identifies **Tandem Bank Limited**, company **00955491**, and a 59-page set
  of full accounts made up to 31 December 2025, filed 12 July 2026. The direct
  filing is
  [document `MzUzMDYwOTUxN2FkaXF6a2N4`](https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history/MzUzMDYwOTUxN2FkaXF6a2N4/document?format=pdf&download=0).
- Tandem's official [Newsroom](https://www.tandem.co.uk/newsroom) separately
  lists **Annual Report 2025 — Annual Report and Accounts Year End 2025**, dated
  5 June 2026, as well as a separate 2025 Pillar 3 report.

The exact 59-page Companies House filing is image-only. It had already been
fully OCR'd with Tesseract and cross-checked against rendered page images for
the repository's Tandem workbook build; that source review covered the entire
report, not merely the primary statements. A renewed search of the preserved
project evidence and exact-report source trail found no published `return on
equity`, `ROE`, `return on assets`, `ROA`, `return on tangible equity` or `RoTE`
value in Tandem Bank Limited's FY2025 accounts. The report therefore supplies
no eligible profitability ratio to collect.

The official 2025 Pillar 3 document is not a substitute. It is for the wider
**Tandem Money Limited group** (Tandem Money Limited, Tandem Bank Limited and
Allium Lending Group Limited), not Tandem Bank Limited company-only. Its first-
party PDF is
[TML Pillar 3 Disclosures, 31 December 2025](https://cdn.prod.website-files.com/62b1c54534b6a11713c35c02/6a1da906ea626c65de0ea1b6_TML_Pillar%203%202025%20Final.pdf).
Even if that wider-perimeter document or a Tandem Money publication exposed a
return measure, it would not satisfy the requested bank perimeter.

## Collection decision

- **Monument FY2025:** retain one unresolved/null record. The exact official
  source and document ID are known, but the report itself still needs
  acquisition and visual/OCR inspection.
- **Tandem FY2025:** record no ratio and classify the gap as an exact-report
  non-disclosure, rather than an unresolved search. Do not calculate a return
  from the statements and do not use Tandem Money Limited group values.

