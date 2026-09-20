# Recoverable missing worksheet cells — primary-source pass (2026-09-19)

## Scope and method

The research phase was read-only: it reviewed the current built workbooks, `scripts/audit_gaps.py`, the gap wayfinder and its latest handoffs/checkpoints. The confirmed findings were subsequently implemented in the build scripts and rebuilt workbooks, as recorded below.

The current census reports **zero wholly empty unexplained sheet-years**. The useful remainder is therefore narrower: numeric cells hidden inside otherwise classified coverage, or years trimmed from an individual sheet because every value for that year is presently absent. Structural blanks, not-yet-published periods and `NEVER_PUBLISHED` findings are excluded. HSBC UK Bank plc was not investigated.

The items below were checked against the current workbook and the bank's own disclosure or Companies House filing. They are ordered by confidence and ease of implementation.

## 1. ICBC (London) plc — FY2015/FY2016 regulatory metrics

**Confidence: high.** These are exact printed values from the UK entity's own solo Pillar 3 reports, in the same USD '000 / percentage basis used by the existing metric sheets. The relevant sheets currently end at FY2017, so FY2015/FY2016 are trimmed rather than shown as visible blank columns.

### Direct metric-sheet fills

| Sheet | Existing row | Missing year | Candidate figure | Primary source |
|---|---|---:|---:|---|
| CET1 Ratio | Common Equity Tier 1 ratio | FY2016 | 21.24% | 2016 Pillar 3, Table 1, PDF p.11 / printed p.8 |
| Tier 1 Ratio | Tier 1 ratio | FY2016 | 21.24% | 2016 Pillar 3, Table 1, PDF p.11 / printed p.8 |
| Total Capital Ratio | Total capital ratio | FY2016 | 26.98% | 2016 Pillar 3, Table 1, PDF p.11 / printed p.8 |
| Total RWAs | Total risk-weighted exposure amount | FY2016 | 1,777,358 | 2016 Pillar 3, Table 1, PDF p.11 / printed p.8 |
| Leverage Ratio | Leverage ratio total exposure measure ($'000) | FY2016 | 2,951,237 | 2016 Pillar 3, Tables 8–9, PDF p.16 / printed p.13 |
| Leverage Ratio | Leverage ratio (%) | FY2016 | 12.79% | 2016 Pillar 3, Tables 8–9, PDF p.16 / printed p.13 |
| CET1 Ratio | Common Equity Tier 1 ratio | FY2015 | 18.29% | 2015 Pillar 3, Table 1, PDF p.10 / printed p.7 |
| Tier 1 Ratio | Tier 1 ratio | FY2015 | 18.29% | 2015 Pillar 3, Table 1, PDF p.10 / printed p.7 |
| Total Capital Ratio | Total capital ratio | FY2015 | 23.51% | 2015 Pillar 3, Table 1, PDF p.10 / printed p.7 |
| Total RWAs | Total risk-weighted exposure amount | FY2015 | 1,953,629 | 2015 Pillar 3, Table 1, PDF p.10 / printed p.7 |

Sources:

- [ICBC (London) plc Pillar 3 Disclosures 2016](https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2017/2016_Pillar_3_Disclosures.pdf)
- [ICBC (London) plc Pillar 3 Disclosures 2015](https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2015/2015_Pillar_3_Disclosures.pdf)

The FY2016 report has a source-side £1k inconsistency: Table 1 prints headline RWA of **1,777,358**, while Table 5 prints a `Grand Total` of **1,777,359** even though its component rows add to 1,777,358. For the existing `Total RWAs` row, 1,777,358 is the higher-confidence transcription because it is the headline value used beside the report's printed capital ratios. The anomaly should be noted, not reconciled by altering either printed figure.

Follow-up against the bank's own FY2017 edition added two further exact fills: leverage exposure **2,717,039** and leverage ratio **14.64%**. Its Table 5 also provides the FY2017 pre-OV1 RWA categories: credit risk **1,666,837**, operational risk **125,483**, position risk **135**, CVA **1,919**, total **1,794,374**. The own-year Table 1 total is **1,794,374**, replacing the workbook's former **1,793,374** taken from the FY2018 comparative, in accordance with the project's own-edition rule. Source: [ICBC (London) plc Pillar 3 Disclosures 2017](https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2018/2017_Pillar_3_Disclosures.pdf), Table 1 PDF p.15, Table 5 PDF p.17, and Tables 8–9 PDF pp.20–21.

### RWA Breakdown section recoverable from the same reports

The current RWA Breakdown starts at FY2021. The earlier reports support a distinct pre-OV1 section (do not force these into the FY2021 UK OV1 categories without showing the source-template break):

| Printed row | FY2016 | FY2015 | Source |
|---|---:|---:|---|
| Total Credit and Counterparty Credit Risk / Total Credit Risk | 1,640,881 | 1,811,655 | Table 5, PDF p.14 in both reports |
| Operational risk | 127,677 | 107,701 | Table 5, PDF p.14 |
| Market risk (Position risk) | 243 | 90 | Table 5, PDF p.14 |
| Credit valuation adjustment | 8,557 | 34,183 | Table 5, PDF p.14 |
| Grand Total, as printed | 1,777,359 | 1,953,629 | Table 5, PDF p.14 |

FY2016's components sum to 1,777,358, not the printed Table 5 grand total of 1,777,359. Preserve the bank's printed total if reproducing that table and document the £1k break.

## 2. Zopa Bank Limited — FY2019 leverage and LCR

**Confidence: high, with an explicit basis label required.** Zopa's own FY2020 Pillar 3 report is explicitly a Zopa Bank Limited disclosure and prints an FY2019 comparative. The existing sheets already contain separate `Annual Report basis, year-end` rows, but their mappings stop at FY2020, causing FY2019 to be trimmed from both sheets.

| Sheet | Existing row | Missing year | Candidate figure | Primary source |
|---|---|---:|---:|---|
| Leverage Ratio | Leverage ratio (%) — Annual Report basis, year-end (see note) | FY2019 | 54.3% | FY2020 Pillar 3, `Key ratios` comparative / leverage section, PDF p.17 |
| LCR | Liquidity Coverage Ratio (%) — Annual Report basis, year-end position (see note) | FY2019 | 10,059% | FY2020 Pillar 3, liquidity disclosure, PDF p.29 |

Source: [Zopa Bank Limited Pillar 3 Disclosures, 31 December 2020](https://www.datocms-assets.com/23873/1658745471-2020-zopa-pillar-3-disclosures.pdf).

These should not be inserted into Zopa's later UK-KM1 rows: those rows use different definitions (including a later central-bank-claims exclusion for leverage and a trailing-average LCR). They fit the separate year-end-basis rows already present in the workbook.

The same source also prints FY2020 RWA **£390.9m** and CET1 ratio **29.5%**, versus the workbook's **£390.5m / 29%** taken from the FY2021 Annual Report comparative. Those are source differences in populated cells, not missing data; retain both only if the project chooses to add an own-edition row rather than overwrite a published comparative.

## 3. Union Bancaire Privée (UK) Limited / Hambros Bank — visible FY1994 blank

**Confidence: high.** This is an existing row and a literal blank cell in the built workbook, unlike the trimmed years above.

| Sheet | Cell | Existing row | Missing year | Candidate figure | Primary source |
|---|---|---|---:|---:|---|
| Balance Sheet | `AG14` | Interests in associates / participating interest (equity shares in FY2008) | FY1994 | 4 (£'000) | Hambros Bank Limited balance sheet, PDF p.22 / printed p.19 |

Source: [Hambros Bank Limited full accounts to 31 March 1994, Companies House document MTM5Njc1NjQ0YWRpcXprY3g](https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MTM5Njc1NjQ0YWRpcXprY3g/document?format=pdf&download=0).

The printed FY1994 asset list includes `Investments in associated undertaking` of **£4k**. It also independently foots as part of total assets of £5,549,175k. The surrounding FY1994 balance-sheet values in the workbook match the same page, making entity, period and unit alignment strong.

The same rendered balance-sheet page also resolves six further omitted FY1994 categories. These are separate printed rows, not values derived from the totals:

| Printed row | FY1994 (£'000) |
|---|---:|
| Treasury bills and other eligible bills | 10,039 |
| Settlement accounts — assets | 388,710 |
| Equity shares | 242 |
| Settlement accounts — liabilities | 239,338 |
| Debt securities in issue | 280,334 |
| Loan capital | 131,487 |

Together with the associated-undertaking value above, the four added asset rows close the prior £398,995 asset shortfall exactly and the three added liability rows close the prior £651,159 liability shortfall exactly. Both sides then reproduce the filing's printed total of £5,549,175k without inference.

## Recommended implementation order

1. ICBC FY2016's six direct metric cells: cleanest single-document batch and no row-model change.
2. ICBC FY2015's four direct metric cells, then add the FY2015/FY2016 pre-OV1 RWA section with the printed-total anomaly recorded.
3. UBP `Balance Sheet!AG14`: one exact visible blank, same filing already used for the rest of that column.
4. Zopa FY2019 year-end leverage/LCR: exact values, but keep them confined to the existing basis-specific rows.

## Second tranche — open leads from `wayfinder/gaps/RESUME.md`

This tranche checked the four named leads against the built workbooks and the banks' own disclosures. It separates literal blank cells from years absent from a sheet's current header range, and records negative results where a source exists but cannot fill the current workbook safely.

### 4. Clydesdale Bank PLC — four literal leverage-exposure blanks, with a basis caveat

**Confidence: high for transcription and entity; medium for insertion into the current row.** These are literal blank cells in the built workbook. Each source table is a dedicated `Disclosures for Clydesdale Bank PLC` appendix and states the **individual consolidated** basis, so this is not a CYBG parent-only series.

| Sheet / cell | Existing row | Missing year | Candidate figure | Primary source |
|---|---|---:|---:|---|
| `Leverage Ratio!I4` | Total exposure measure excluding claims on central banks | FY2018 | £45,471m | 2018 Pillar 3, Appendix 1, Table 46 `LRCom`, row 21, printed p.63 |
| `Leverage Ratio!J4` | same | FY2017 | £45,541m | 2017 Pillar 3, Appendix 1, Table 40 `LRSum` row 8 / Table 41 `LRCom` row 21, printed pp.57–58 |
| `Leverage Ratio!K4` | same | FY2016 | £43,518m | 2016 Pillar 3, Appendix 1, Table 32 `Leverage Ratio`, printed p.56; repeated as the FY2016 comparative in the 2017 tables |
| `Leverage Ratio!L4` | same | FY2015 | £41,970m | 2016 Pillar 3, Appendix 1, Table 32 `Leverage Ratio`, FY2015 comparative, printed p.56 |

Sources:

- [CYBG PLC Pillar 3 Disclosures 2018](https://www.virginmoneyukplc.com/downloads/pdf/cybg-pillar-3-2018.pdf)
- [CYBG PLC Pillar 3 Disclosures 2017](https://www.virginmoneyukplc.com/downloads/pdf/cybg-pillar-3-2017.pdf)
- [CYBG PLC Pillar 3 Disclosures 2016](https://www.virginmoneyukplc.com/downloads/pdf/cybg-pillar-3-2016.pdf)

Do **not** silently paste these four values into the present row. The older tables call the measure plain `Total leverage ratio exposure`; they pre-date the later central-bank-claims split implied by the row's current label. In addition, their individual-consolidated capital/RWA/ratio series differs systematically from the current Annual Report series: for example, FY2018 leverage is 5.7% and RWA £19,952m in the appendix versus 5.6% and £20,117m in the workbook; FY2017 is 6.3% / £19,885–19,886m versus 6.2% / £20,055m; FY2016 is 6.5% versus 6.8%; and FY2015 is 6.7% versus 7.2%. The clean implementation is a separately labelled historical regulatory-basis row (or an explicit documented decision that the existing row may change basis). FY2014 exposure remains unrecovered.

### 5. Credit Suisse (UK) Limited — FY2016 Pillar 3 metrics omitted from individual sheets

**Confidence: high.** The official archive's entity-specific 2016 Pillar 3 report directly disproves the workbook notes that treat these metrics as unavailable. These are not literal cells in the built sheets: FY2016 is absent from each sheet's header range. They are exact new year/mapping entries. The FY2016 total RWA is already present in `RWA Breakdown`, which independently anchors the figure and entity.

| Sheet | Existing row | Missing year | Candidate figure | Primary source |
|---|---|---:|---:|---|
| CET1 Ratio | CET1 Ratio (combined with Tier 1) | FY2016 | 20.9% | 2016 Pillar 3, capital composition and ratios table, PDF p.5 |
| Tier 1 Ratio | Tier 1 Ratio (combined with CET1) | FY2016 | 20.9% | same table, PDF p.5 |
| Total Capital Ratio | Total Capital Ratio | FY2016 | 23.7% | same table, PDF p.5 |
| Total RWAs | Risk Weighted Assets (RWA) | FY2016 | £888.838m | `RWA and capital requirements (£000s)`, PDF p.6: printed total 888,838 |
| Leverage Ratio | Leverage Ratio | FY2016 | 6.2% | `Leverage Ratio Common Disclosure`, PDF p.20; exposure 2,996,370 (£000s) |

Source: [Credit Suisse (UK) Limited Pillar 3 Disclosures 2016](https://www.ubs.com/global/en/investor-relations/complementary-financial-information/disclosure-legal-entities/archive-credit-suisse/_jcr_content/root/contentarea/mainpar/toplevelgrid_1145414446/col_1/accordionbox/accordionsplit_edb9/table_672121609.1602187955.file/dGFibGVUZXh0PS9jb250ZW50L2RhbS9hc3NldHMvY2MvaW52ZXN0b3ItcmVsYXRpb25zL2NvbXBsZW1lbnRhcnktZmluYW5jaWFsLWluZm9ybWF0aW9uL2FyY2hpdmUvMjAxNi8yMDE2LWNzdWstcGlsbGFyLTMtZGlzY2xvc3VyZXMucGRm/2016-csuk-pillar-3-disclosures.pdf), reached from the [official UBS Credit Suisse legal-entity archive](https://www.ubs.com/global/en/investor-relations/complementary-financial-information/disclosure-legal-entities/archive-credit-suisse.html).

The RWA table prints credit/CCR 748,287, market risk 56, other risks 140,496, and total 888,838 (£000s). Its components sum to 888,839, a source-side £1k break; preserve the bank's printed headline total, consistent with the existing `RWA Breakdown` row. The £2,996.370m leverage exposure is also directly disclosed but there is no current exposure row on this workbook's `Leverage Ratio` sheet, so it is supporting evidence rather than a blank-cell fill.

### 6. Alrayan Bank Limited — FY2022 own edition closes a provenance lead, not a data gap

**Result: no missing numeric cell. Confidence: high.** The bank's FY2022 Pillar 3 PDF is live and contains the complete Annex I KM1 and OV1 tables. Every FY2022 value currently populated in `KM1 Key Metrics` and `RWA Breakdown` matches the own-year edition exactly; the workbook currently cites the FY2023 comparative instead.

The own-year KM1 values on printed p.29 are: CET1 £152.7m; Tier 1 £155.7m; total capital £178.4m; RWA £1,022.3m; capital ratios 14.93%, 15.23% and 17.45%; UK 7a 2.82%; UK 7d 10.82%; conservation buffer 2.50%; countercyclical buffer 0.65%; combined buffer 3.15%; overall requirement 13.97%; row 12 28%; leverage exposure £2,306.6m and ratio 6.7%; HQLA £173.6m; outflows £159.4m; inflows £255.1m; net outflows £39.8m; LCR 442%; available stable funding £1,982.3m; required stable funding £1,280.8m; NSFR 155%. The OV1 table on printed p.30 likewise matches the workbook: credit risk excluding CCR £936.3m, CCR £0.1m, operational risk £85.9m, total £1,022.3m.

Source: [Al Rayan Bank Pillar 3 Disclosures, 31 December 2022](https://www.alrayanbank.co.uk/sites/default/files/media/file-uploads/2023-08/al_rayan_pillar_three_32pp_brochure_-_final.pdf), linked from the bank's [regulatory information page](https://www.alrayanbank.co.uk/investor-relations-regulatory-information). The actionable change is citation/provenance only, outside this pass's missing-data scope.

### 7. AIB Group (UK) p.l.c. — historical XLSX files do not resolve current blanks

**Result: no current blank is safely recoverable.** The current literal blanks are `RWA Breakdown!F4:F6` (FY2021 credit risk, operational risk and CVA). The FY2021 Annual Financial Report gives movements and total RWA £6,611m, not an absolute closing category split. AIB UK's FY2020 XLSX gives prior-period absolute categories in EUR, so using it to back-solve FY2021 GBP values would be derived, currency-mixed and rounding-unsafe.

The [official AIB Group (UK) FY2020 Pillar 3 workbook](https://aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/pillar3/2020/aib-group-UK-2020-pillar-3-report.xlsx) does support a future, explicitly transitional/EUR FY2020 extension: Table 1 cells B17/B19/B21 CET1/Tier 1/total capital €1,693m; B24 credit RWA €7,573m; B25 market €0m; B26 operational €605m; B27 CVA €0m; B28 total RWA €8,178m; B31:B33 ratios 20.7%; Table 4 C16 / Table 5 C38 leverage exposure €14,728m; and Table 5 C40 leverage ratio 11.5%. The [official FY2019 UK workbook](https://aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/pillar3/pillar-3-2019-uk-300320.xlsx) is also available. Neither UK workbook contains LCR, NSFR or MREL figures. These are historical extension leads, not fills for the current FY2021–FY2025 blank cells.

### Second-tranche implementation priority

1. Credit Suisse UK FY2016 ratios/RWA/leverage: five direct, entity-specific additions with no basis ambiguity inside the source.
2. Clydesdale FY2015–FY2018 leverage exposures: four exact literal blanks, but only on a separately labelled historical regulatory-basis row or after an explicit basis decision.
3. Al Rayan FY2022: update provenance to the own-year edition; do not count it as recovered data.
4. AIB UK: leave `RWA Breakdown!F4:F6` blank; consider FY2019/FY2020 only as a separate historical EUR/transitional extension.

## Implementation outcome

The two tranches recovered **45 previously blank numeric cells** across five banks, plus one correction to an already populated later-comparative figure:

- Union Bancaire Privée UK: seven FY1994 balance-sheet lines.
- ICBC (London): 27 cells across FY2015-FY2017 metrics and the pre-OV1 RWA breakdown; FY2017 Total RWA corrected from the later-comparative 1,793,374 to the own-edition 1,794,374.
- Zopa: two FY2019 year-end-basis ratio cells.
- Credit Suisse UK: five FY2016 capital/RWA/leverage metric cells.
- Clydesdale: four FY2015-FY2018 leverage-exposure cells on a new, separately labelled historical individual-consolidated-basis row.

All five workbooks were rebuilt. The repository-wide gap audit reports one wholly empty block, Credit Suisse UK Total Capital Ratio FY2017-FY2020; it is the documented false positive described below. The remaining 109 `Unreached today` cells are explicit research limits rather than cells silently inferred to be non-disclosures. The verifier continues to show documented source-side and pre-existing reconciliation warnings, including the printed £1k RWA breaks in ICBC FY2016 and Credit Suisse UK FY2016.

## Follow-up screening — no further safe numeric fills

A further interior-gap scan covered the remaining candidates highlighted by the Wayfinder:

- Bank of Ceylon UK FY2022 Total RWAs, leverage exposure and leverage ratio remain unsupported. Its FY2022/FY2023 accounts contain no RWA or leverage figure, and the available ratios are too coarsely rounded for a safe back-solve.
- Triodos Bank UK FY2023 prints an NSFR percentage but no available-stable-funding or required-stable-funding amounts. Those component rows remain blank rather than being reconstructed from the ratio.
- Kuwait Finance House's Total RWAs row is deliberately marked as not directly disclosed. Its report prints Pillar 1 requirement components, while the RWA Breakdown total is explicitly derived; copying that derived value into the direct-total row would misstate provenance.
- Turkish Bank UK FY2025's standalone Pillar 3 is not yet due: the latest edition is FY2024 and the observed publication lag places FY2025 around February 2027. Its annual report prints a regulatory-capital amount and total RWA, but no corresponding ratio.
- Zenith FY2019 remains a published-but-lost document: the bank's archive confirms the edition existed, but the full live/Wayback fetch ladder found no recoverable PDF. Existing annual-report figures are retained; no unsupported replacement was added.

These checks produced no additional workbook edits.

Before the second attempt, the repository audit flagged Credit Suisse UK Total Capital Ratio
FY2017-FY2020 as an "unexplained" empty year block. That flag is now closed by the archive recovery
below; the values were not derived from capital amounts.

## Second attempt — Credit Suisse UK archive recovery

The official UBS Credit Suisse legal-entity archive exposes the previously unrecovered standalone
CSUK Pillar 3 PDFs for 2017, 2018, 2019 and 2020. Their capital-ratio tables directly print Total
Capital ratios of **19.2% (FY2017), 27.0% (FY2018), 25.9% (FY2019), and 26.20% (FY2020)**. These
were added to the Total Capital Ratio sheet and the build script; no calculation was used. The
archive page is [UBS's Credit Suisse disclosure archive](https://www.ubs.com/global/en/investor-relations/complementary-financial-information/disclosure-legal-entities/archive-credit-suisse.html),
with the figures on pages 4, 4, 4 and 4 of the respective PDFs.

The next strongest lead is Itaú BBA International: its official investor-relations page lists
the missing **2016** and **2014** Pillar 3 editions and exposes the direct filenames
`IBBAInt_Cons_Pillar3_2016_FINAL.PDF` and `IBBAInt_Cons_Pillar3_2014_FINAL.PDF`. The archive/search
layer identified the links, but the PDFs were not fetchable in this environment (DNS/cache failure),
so no Itaú values were transcribed. Those two files are the most useful links for a user-assisted
follow-up.

The same page also lists a 2013 edition at
`https://www.itau.com.br/content/dam/ibba/en/IBBAInt_Cons_Pillar3_2013_FINAL_20140625.pdf`.
It is likewise a likely source for the Itaú 2013 gaps, but could not be fetched here.

## Kingdom, Monzo and AIB follow-up

The three requested leads were checked against the current build outputs on 20 September 2026.

### Kingdom Bank — FY2019 Tier 2

This lead was already implemented in the current workbook. The FY2019 Pillar 3 disclosure prints
Tier 2 capital (no deductions) of **£1.0m**; the value is present on the `Total Capital` sheet as
**1,000 (£'000)** with the Pillar 3 basis explicitly labelled. The same FY2019 disclosure also
supports the existing capital, total-capital and leverage entries. No further Kingdom FY2019 numeric
cell was identified that could be added without deriving it.

### Monzo — FY2018/FY2019 comparative recovery

This lead was also already implemented. The FY2020 Pillar 3's printed FY2019 comparative supplies:

- CET1 capital **£97,632k**;
- Tier 1 capital **£97,632k**;
- total capital **£97,632k**;
- total RWAs **£93,972k**;
- CET1 and total-capital ratios **104%**;
- leverage ratio **15.5%** on total exposure **£631,369k**; and
- LCR **663%**, with liquidity buffer **£510,314k** and adjusted net outflows **£76,994k**.

The workbook preserves the separate FY2019 annual-report CET1-ratio figure of **126%**, because
that is a genuine source disagreement rather than a value to overwrite. FY2019 NSFR, MREL and RWA
breakdown remain blank because the available editions do not print those figures for the comparative
year. The FY2018 edition has likewise been transcribed where it prints figures; its Tier 1 capital
amount remains undisclosed.

### AIB Group (UK) — FY2019/FY2020 Pillar 3 workbooks

AIB Group (UK) did publish entity-specific pre-2022 EU-format Pillar 3 workbooks for FY2019 and
FY2020. They are not UK KM1 templates, and the FY2020 workbook reports amounts in EUR, while the
current AIB workbook is a five-year FY2021–FY2025 series in GBP. The FY2021–FY2025 gaps therefore
cannot be filled from these older files, and the Irish parent’s Pillar 3 cannot substitute for the UK
entity. A separate historical FY2019/FY2020 EUR-basis extension is possible, but it would require
adding clearly labelled pre-2021 columns rather than inserting the figures into the current GBP series.

The official files remain:

- `https://aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/pillar3/2020/aib-group-UK-2020-pillar-3-report.xlsx`
- `https://aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/pillar3/pillar-3-2019-uk-300320.xlsx`

The AIB workbook now contains three separate auxiliary sheets — `Historical P3 Capital EUR`,
`Historical P3 RWA EUR` and `Historical P3 Leverage EUR` — covering FY2019 and FY2020. They are
intentionally separate from the current GBP FY2021–FY2025 metric sheets. All three build scripts
compile and the current workbooks pass the build-current check.

The user supplied the 2013 and 2017 PDFs. The 2013 capital-resources table (p.11) directly reports
CET1 capital **USD 891m**, CET1 ratio **17.7%**, total regulatory capital **USD 913m**, total
capital ratio **18.1%**, and total RWA **USD 5,042m**. These five FY2013 values were added to the
corresponding Itaú sheets. The 2017 PDF's Table 1 reports FY2017 and FY2016 comparatives; its FY2016
figures (CET1 USD 992m, CET1 ratio 18.0%, total capital USD 1,000m, total capital ratio 18.2%, RWA
USD 5,506m) already matched the workbook, so no duplicate edits were made. Its FY2017 figures also
confirm the existing values (CET1 USD 1,049m, total capital USD 1,051m, total capital ratio 19.5%,
RWA USD 5,399m).

Additional source screening found one promising non-Itaú lead: Arab Bank Europe’s official
[Important Information page](https://arabbankeurope.com/important-information/) currently lists a
“Pillar III Disclosures” document, but the site exposes it through a non-document SVG link in the
search layer, so the PDF URL cannot be resolved automatically here. A user download of that linked
Pillar III PDF could potentially address Arab Bank Europe’s FY2023-FY2025 unreached KM1/capital cells.
Kingdom Bank’s 2023 annual report explicitly says SDDTs no longer require Pillar 3 after periods ending
31 December 2023, so it is not currently a strong recovery lead.

## Unreached-source batch — 20 September 2026

The next unreached batch was screened against current first-party pages and surviving archives:

- **Melli Bank:** the live official site exposes an intact FY2016 Pillar 3 PDF, but the FY2023 gap in
  the workbook remains marked “available on request”; no FY2023 document was exposed by the bank's
  current site or the archive route. No figure was added.
- **Persia International Bank:** search results expose a third-party report catalogue, but not a
  first-party downloadable FY2019/FY2022 Pillar 3 document. No secondary-host figure was used.
- **Weatherbys:** the official corporate-information page now links an intact FY2024 Pillar 3 PDF.
  It contains capital, RWA, leverage and liquidity tables, but no MREL disclosure, so it does not
  fill the remaining FY2016–FY2018 MREL cells. The current workbook already contains the FY2024
  capital/liquidity metrics from the bank's own report.
- **Zopa:** the current official investor page lists Pillar 3 editions from FY2021 onward, but no
  FY2019 or FY2020 predecessor edition. The FY2019 MREL gap therefore remains unrecovered.
- **Kingdom:** the FY2022/FY2023 leads remain blocked by the bank's discontinued/removed Pillar 3
  archive; no new first-party document was found.

This pass produced no safe numeric additions. The remaining unreached cells in these banks are now
negative source findings or “available on request” cases, rather than silently empty gaps.

One additional search hit was a Philippine National Bank (Europe) FY2025 Pillar 3 PDF hosted on the
parent group's official domain. It is a genuine PNBE disclosure, dated 31 December 2025, and contains
own-funds and risk-exposure tables. The current PNBE workbook already contains its FY2025 figures, so
this is corroborating provenance rather than a new fill. Source: [PNB (Europe) FY2025 Pillar 3]
(https://www.pnb.com.ph/storage/asset-libraries/Me1hxgtaSlrRs32Dvl6SIB1qgOfY1WbTDfGv2ZzQ.pdf).

## Melli and Persia follow-up

The banks' own sites were searched again on 20 September 2026. Persia's official site exposes a genuine
FY2021 Pillar 3 PDF — [Persia Pillar 3, 31 March 2021](https://www.persiabank.co.uk/Pillar%203%202021%20v3.pdf) —
but the current Persia workbook already uses the FY2021 capital, RWA, leverage and LCR figures from that
document. The remaining FY2019/FY2022 NSFR and MREL gaps require editions that were not found.

Melli's FY2023 annual report confirms that a Pillar 3 disclosure exists on the bank's website, but no
FY2023 PDF or direct download was exposed by the live site, search index or available archive route.
The only first-party Pillar 3 file recovered in this pass is the older [Melli FY2016 disclosure]
(https://www.mellibank.com/File/DownloadReportFiles?filename=Melli+Bank+-+Pillar+3++Disclosures+2016+-+Final.pdf),
which does not address the FY2023 gap. No figures were added from either bank.
