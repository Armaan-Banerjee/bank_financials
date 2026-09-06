# HD-045–HD-052 blank/source-gap review

Date: 2026-09-06

This is a triage review of the completed FY2014-capped extension tickets. It
does not treat every blank as an omission: blanks caused by a pre-disclosure
regime, a genuine FRS 101 exemption, an entity/group basis mismatch, or a
document that explicitly lacks the requested granularity are retained. The
primary-source URLs below are the URLs recorded in the bank build scripts;
the ticket notes describe the page-level checks already performed.

## Actionable or still doubtful items

### Cynergy Bank — FY2020 RWA category breakdown

`scripts/build_cynergy_bank.py` says that the FY2020 Pillar 3 document has a
direct Total RWA figure but that its category table was “not captured this
batch”, and the ticket explicitly flags this for a future pass. This is a
true transcription/review gap rather than a source-supported non-disclosure.
The FY2020 primary document is linked as:

<https://www.cynergybank.co.uk/media/liqngpna/pillar-3-disclosures-2020.pdf>

The table should be checked for credit, operational, market, CCR,
securitisation and any other UK OV1/Pillar 1 categories. Do not derive rows
from the total or capital requirement if the table is absent or internally
inconsistent.

The same script notes that FY2021 may also have a standalone Pillar 3
document despite the earlier “no document” claim. That year is outside the
HD-051 extension but is a separate audit candidate.

### British Arab Commercial Bank — FY2024/FY2025 RWA detail

The FY2021–FY2023 modern UK OV1 aggregate rows were recovered in the deep
verification addendum. The current script still says that FY2024/FY2025
exposure-class detail was not found. This is not yet a confirmed omission,
but those two own-year Pillar 3 PDFs should receive a direct table search
before the blank is labelled final:

- <https://files.bacb.co.uk/production/files/BACB_Pillar3_YE2024web-05.pdf>
- <https://files.bacb.co.uk/production/files/BACB_Pillar3_YE2025web-03.pdf>

### NatWest plc — FY2014 equity roll-forward gap

The HD-050 resolution records a £1,391m difference: FY2014 equity
components total £11,921m while the independently reported Balance Sheet
Total equity is £13,312m. This is a genuine unresolved source/data-quality
gap, not a justified blank. The FY2014 Companies House annual-report filing
is linked in `scripts/build_national_westminster_bank.py` as `NWB_CH_AR["FY2014"]`
(company 00929027). The equity note and preference-share history should be
re-read from the filing and later comparative notes. No balancing value
should be inserted without a source-backed component.

### QIB (UK) — FY2015 cash-flow sign error

The script documents that the own FY2015 report prints a positive operating
cash-flow subtotal while its adjustment lines, cash movement and other
subtotals require a negative figure. This is an explicit source-quality
finding, not a blank. It has already been handled transparently with a data
quality flag and should not be “corrected” silently. The official report URL
and page are recorded in `scripts/build_qib_uk.py` (`AR["FY2015"]`, p.14).

## Source-supported blanks that should remain blank pending new evidence

- Union Bancaire Privée UK: FY2014–FY2020 Pillar 3 metrics; the ticket
  records a domain-wide Wayback search finding only remuneration-code
  documents, not capital/RWA disclosures. The cash-flow exemption is also
  confirmed in the entity accounts.
- Co-operative Bank: pre-regime LCR/NSFR/MREL and presentation/basis changes
  documented against the bank’s own reports.
- Kingdom Bank: Total Capital, Total RWAs, NSFR, MREL and RWA breakdown;
  the ticket records these as a persistent SDDT/non-disclosure pattern after
  the previously wrongly-blanked KPI rows were recovered.
- FCE Bank: LCR/NSFR/MREL; the ticket records full-document searches of the
  available reports with no numeric references.
- Bank of China (UK): pre-disclosure liquidity metrics and unavailable
  category-level RWA rows; the FY2014 £100k cash discrepancy is an explicit
  source inconsistency, not an omitted value.
- ICICI Bank UK: NSFR/MREL and the RWA gap between Pillar-1-derived and
  later directly disclosed totals; the latter is explicitly flagged rather
  than force-reconciled.
- Mizuho International: FY2014–FY2016 Pillar 3 documents are parent-group
  disclosures, not MHI entity disclosures.
- Aldermore: FY2017 is not a standalone period; scanned pre-/transition-year
  Asset Quality stage splits were not disclosed at the requested granularity.
- Clydesdale: FY2018 90+ DPD narrative was dropped from that year’s own
  report; numeric pre-disclosure MREL remains unsupported.
- Morgan Stanley Bank International: FY2014 has no capital-metric
  disclosure in the filing or later comparative reach-back.
- Punjab National Bank International: FY2021 is a pre-existing historical
  gap outside this capped extension and needs a separate source-recovery
  task, not interpolation.
- Zenith Bank UK: FY2016–FY2020 Pillar 3 PDFs were exhaustively searched in
  Wayback and not crawled; the landing page alone is not evidence of the
  missing binaries.
- Itau BBA International: Asset Quality FY2017 remains a documented
  self-skip because the later report does not restate the IFRS 9 stage table.
- SMBC Bank International: metric/year-specific pre-regime blanks and the
  documented RWA/derivatives basis issue remain source-supported.

## Recommended next pass

Prioritise the Cynergy FY2020 RWA table, then BACB FY2024/FY2025 RWA tables,
and separately investigate the NatWest FY2014 equity gap. These are the only
items in HD-045–HD-052 that the ticket text itself identifies as an uncaptured
or unresolved data gap rather than a deliberate, source-supported blank.
