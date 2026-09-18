# Research triage for `bank_probs.txt`

Checked: 17 September 2026

## Scope and method

This is a research note only. No bank workbook was edited or saved. I read `bank_probs.txt`, inspected the relevant workbooks read-only to identify the bank and the exact gap, and then checked first-party material: the bank's own publication archive/reports, Companies House filings, and regulatory disclosures. Existing worksheet links were treated only as search leads. They were not used as evidence that a missing item was unavailable.

This is a triage, not a claim that every historical URL permutation has been exhausted. `High` confidence means the bank itself explicitly states the position or its live publication index enumerates the relevant series. `Medium` means a first-party report or filing was found, but the exact metric/basis still needs transcription-level review. `Low` means the highlighted issue remains a research queue item.

## Main conclusions

1. **The 2026 requests for HSBC Bank plc, HSBC UK Bank plc and National Westminster Bank plc are actionable, but they are interim periods, not FY2026 annual data.** HSBC Bank plc published a Pillar 3 report at **30 June 2026** containing KM1 and OV1; HSBC's subsidiary archive also lists the equivalent HSBC UK Bank plc report. NatWest's results centre lists an H1 2026 Pillar 3 report specifically for NatWest Bank plc. These should be labelled `30 Jun 2026` / `H1 2026`, not silently mixed into annual FY columns. [HSBC subsidiary reporting archive](https://www.hsbc.com/investors/results-and-announcements/all-reporting/subsidiaries?company-new=hsbc-bank-plc&page=1&take=40), [HSBC Bank plc Pillar 3 at 30 June 2026](https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2026/interim/pdfs/hsbc-bank-plc/260810-hsbc-bank-plc-pillar-3-disclosures-at-30-june-2026.pdf), [NatWest results centre](https://investors.natwestgroup.com/results-centre)

2. **SDDT is a real reason for several recent Pillar 3 gaps, but it must be evidenced bank by bank.** Cynergy's own 2024 annual report says its SDDT modification was approved on 17 January 2025 and that it was therefore not required to publish Pillar 3 at 31 December 2024; its 2025 report repeats the position for 31 December 2025. CAF Bank's live disclosure page also explicitly says it is a non-listed SDDT and is not required to publish a Pillar 3 report. Those are primary-source explanations, not conclusions drawn from a dead or missing worksheet link. [Cynergy 2024 annual report](https://assets.ctfassets.net/xzmqg68ot16t/2AeSbXsBP7fwKhngGTLWxb/83b43e8ab9ec77bc1ec46f72784e68de/Annual_Report_2024.pdf), [Cynergy 2025 annual report](https://assets.ctfassets.net/xzmqg68ot16t/1aUkuB7BcAd8Pj5Kq0RNqh/101ced4af6be2d55cd37fad3542829b2/Cynergy_Bank_-_Annual_Report_2025.pdf), [CAF Bank Pillar 3 notice](https://www.cafonline.org/home/caf-bank/about-us/legal-information/pillar-3-disclosure)

3. **A publication page labelled “Pillar 3 Disclosure 2025” is not necessarily a report.** CAF's archive link resolves to the SDDT notice above, not a 2025 PDF. It therefore does not supply 2025 KM1 or an RWA breakdown.

4. **Several “2025 missing” cases are supported by enumerated first-party archives, rather than by old source links.** Access Bank's live report page has annual reports through 2025 but Pillar 3 only through 2023. Cambridge & Counties has a 2025 annual report but its Pillar 3 list stops at 2024. Gatehouse has a 2025 annual report but its Pillar III list stops at 2024. Weatherbys likewise publishes its 2025 annual report while identifying 2024 as its latest Pillar 3 report. Griffin's report page has annual reports for 2024 and 2025 but only one Pillar 3 report, for 2023. [Access reports](https://www.theaccessbankukltd.co.uk/about-us/our-reports/), [Cambridge & Counties annual results](https://ccbank.co.uk/about-us/annual-results/), [Gatehouse corporate governance archive](https://gatehousebank.com/about-us/corporate-governance), [Weatherbys corporate information](https://www.weatherbys.bank/about-us/corporate-information/), [Griffin reports](https://griffin.com/reports)

5. **Triodos must be kept on the UK-entity basis.** The Triodos Bank UK publication page lists a UK 2025 annual report but UK Pillar 3 reports only through 2024. A separate 2025 Pillar 3 report exists for the wider Triodos Bank group; it is not a substitute for Triodos Bank UK Limited. [Triodos Bank UK reports](https://www.triodos.co.uk/press-and-media)

6. **“No KM1” before the UK KM1 template existed is not itself a data defect.** Do not create empty pre-template year headers merely to record an absence. Where older reports disclose capital/RWA measures in another table, preserve their own presentation and do not relabel them as KM1.

7. **Entity scope is the largest remaining false-positive risk.** DB UK Bank's available Pillar 3 is for its PRA consolidation group (DBIGB), not clean DB UK Bank solo data. Nomura Bank International ceased to be included as a significant subsidiary in the relevant group Pillar 3 series after 2021. Group reports for Triodos, HSBC, Santander, or a foreign parent should not be used for a UK legal entity without explicit scope support.

## Highest-priority recoverable or correctable items

| Bank / item | Finding | Confidence / action |
|---|---|---|
| HSBC Bank plc (#36) | KM1, OV1/RWA, leverage and liquidity are published at 30 June 2026. | **High — recoverable.** Add only with an interim-period label. |
| HSBC UK Bank plc (#38) | HSBC's subsidiary archive lists the 30 June 2026 Pillar 3 report for the ring-fenced bank. | **High — recoverable.** Interim label required. |
| National Westminster Bank plc (#52) | NatWest's results centre lists H1 2026 results and Pillar 3 specifically for NatWest Bank plc. | **High — recoverable.** Interim label required. |
| Santander UK (#63) | Santander's site has 2026 quarterly management and additional capital/risk disclosures, while the latest annual report remains year ended 31 December 2025. | **High on timing; medium on entity/table extraction.** Do not call Q1/H1 data FY2026 annual. [Santander UK 2025 annual report announcement](https://www.santander.co.uk/about-santander/investor-relations/stock-exchange-announcements/santander-uk-plc-annual-report-and-financial-statements-for-the-year-end-31-december-2025) |
| Arbuthnot Latham (#5) | A 2026 interim Pillar 3 report is live and may carry a 2025 comparative, but it is on Arbuthnot Banking Group scope. | **Medium — inspect scope/comparative before using.** [2026 interim Pillar 3](https://www.arbuthnotlatham.co.uk/sites/default/files/documents/ABG-Pillar-3-Disclosures-2026-Interim.pdf) |
| Arab Bank Europe (#4) | Standalone 2023 and 2024 Pillar 3 documents exist; they should be checked for KM1/OV1 rather than treating those years as absent. | **High — recoverable subject to EAB Group scope label.** [Arab Bank Europe disclosures](https://arabbankeurope.com/downloads/pillar-iii-disclosures/) |
| Bank of Beirut UK (#7) | A first-party 2025 Pillar III report is live, and it should close the apparent latest-year prudential gap. | **High — recoverable.** [2025 Pillar III](https://www.bankofbeirut.co.uk/Content/uploads/PillarDisclosure/Bank_of_Beirut_UK_Ltd_-_Pillar_III_Disclosures_-_31_December_2025.pdf) |
| KFH / Kuwait Finance House (#44) | The present workbook already contains a populated 2025 RWA breakdown while Total RWAs is labelled unavailable. This is an internal contradiction requiring source-table review; do not derive a total by summing categories unless the report itself prints it. | **High contradiction; medium extraction.** |
| Marks & Spencer Financial Services (#45) | The current workbook has populated RWA and other prudential sheets despite the “no Pillar 3” wording. The basis/source narrative needs correction even if KM1 itself remains unavailable. | **High contradiction.** |
| Turkish Bank UK (#69) | The bank now publishes a Pillar 3 document and a 2025 annual report. The document labelled “2024” must be mapped by its stated reporting date, not upload date; check it directly for CET1 ratio before retaining “not publicly disclosed.” | **Medium — source-level extraction needed.** [Turkish Bank reports](https://www.turkishbank.co.uk/reports/) |
| Zenith (duplicate #72) | A 2025 Pillar 3 report is live and contains the latest prudential series. The 2025 balance-sheet gap is separate: the latest annual-report archive still needs an entity-level filing check. | **High for 2025 Pillar 3.** [Zenith 2025 Pillar 3](https://www.zenith-bank.co.uk/media/2290/pillar-3-zbuk-31dec25.pdf) |

## Confirmed recent non-publication / structural cases

| Bank / item | First-party evidence | Confidence |
|---|---|---|
| Access Bank UK (#1) | Live archive: annual reports through 2025, Pillar 3 through 2023 only. This supports no separate 2024/2025 Pillar 3, but the annual reports still need checking for any embedded RWA total. | High for archive endpoint; medium for every metric. |
| CAF Bank (#16) | Its own live page says the non-listed SDDT is not required to publish a Pillar 3 report. The archive's “2025” link is this notice, not a report. | High. |
| Cambridge & Counties (#17) | Live archive has the 2025 annual report and Pillar 3 only through 2024. | High for no 2025 Pillar 3; annual-report capital note remains usable where explicit. |
| Cynergy (#23) | 2024 and 2025 annual reports explicitly state the SDDT-driven Pillar 3 non-publication. | High. |
| Griffin (#30) | Live archive enumerates annual reports for 2023–2025 but only a 2023 Pillar 3 report. | High. |
| Gatehouse (#28) | Live archive has the 2025 annual report and Pillar III only through 2024. | High. |
| Hampden & Co (#33) | The bank's shareholder page publishes 2024/2025 annual reports; the identifiable standalone Pillar 3 report is for 2023. | Medium-high. [Hampden shareholder information](https://www.hampdenbank.com/about-us/shareholder-information), [2023 Pillar 3](https://www.hampdenbank.com/content/hampden/content/Hampden-Co-plc-2023-Pillar-3-Disclosures.pdf) |
| Methodist Chapel Aid (#47) | The live financial-information page and 2024/2025 annual reports do not provide a post-2023 Pillar 3 report. This is a publication-series endpoint, not a broken-link inference. | Medium-high. [Financial information](https://www.mcafundingforchurches.co.uk/about-us/financial-information/) |
| Triodos Bank UK (#68) | UK page lists the 2025 annual report but UK Pillar 3 only through 2024. The group 2025 report is out of scope. | High. |
| Weatherbys (#72) | The bank's live corporate page calls 2024 its latest Pillar 3 while separately publishing the 2025 annual report. | High. |

## Bank-by-bank triage

`Recoverable` means a first-party report likely resolves at least part of the highlighted gap. `Supported gap` means the bank's current publication set or explicit statement supports the absence. `Needs deep read` means no safe conclusion should yet be entered.

| # | Bank | Triage result | Confidence |
|---:|---|---|---|
| 1 | Access Bank UK | Supported gap for standalone P3 after 2023; inspect 2024/25 annual reports for explicit RWA totals. | High / Medium |
| 2 | Allica | KM1/total RWA now present; detailed RWA split still appears undisclosed. | Medium |
| 3 | Alpha Bank London | No KM1 series found; use only expressly disclosed annual-report capital items, no back-solving. | Medium |
| 4 | Arab Bank Europe | 2023–24 Pillar 3 is recoverable; label EAB Group scope. | High |
| 5 | Arbuthnot Latham | 2026 interim P3 may supply 2025 comparatives; group-scope check required. | Medium |
| 6 | Bank of Africa UK | Total RWA/capital are available for recent years; missing detailed splits need report-by-report review. | Medium |
| 7 | Bank of Beirut UK | 2025 Pillar III is recoverable; historical 2018–20 gap remains separate. | High |
| 8 | Bank of Ceylon UK | Recent RWA figures are now populated; KM1 absence appears presentation/template-related. | Medium |
| 9 | Bank of Ireland UK | Recent total RWA exists; detailed split and KM1 remain entity/basis questions. | Medium |
| 10 | Bank of the Philippine Islands Europe | Recent total RWA and risk split are now present; KM1 remains absent. | Medium |
| 11 | Bank Saderat | 2024–25 detailed RWA/KM1 remains unresolved; annual filings alone do not prove non-disclosure. | Low |
| 12 | Birmingham Bank | RWA breakdown and total exist; bank did not use a KM1 template in the reviewed series. | Medium-high |
| 13 | BLME | KM1/total RWA are present through 2025; detailed split stops after 2021. | Medium-high |
| 14 | Brown Shipley | RWA is now populated through 2025; KM1 gap still needs entity-specific disclosure check. | Medium |
| 15 | C. Hoare & Co | 2026 total RWA is in the financial report; no separate 2026 KM1/OV1 located. | Medium-high |
| 16 | CAF Bank | Supported gap: explicit SDDT non-publication notice. | High |
| 17 | Cambridge & Counties | 2025 annual report exists; P3 archive ends 2024. | High |
| 18 | Castle Trust Capital | Current workbook has 2022–25 RWA/KM1 populated; remove/rename any combined `FY2022-FY2023` artefact only if later authorised. | High on status |
| 19 | Cater Allen | No standalone KM1/OV1 located; do not use capital ÷ ratio back-solves as disclosed RWA. | High caution |
| 20 | Charity Bank | 2024–25 annual reports exist; recent standalone P3 not located. RWA total may be explicit in annual accounts. | Medium |
| 21 | Charter Court Financial Services | Holding-company/entity-basis issue; no safe standalone bank prudential series established. | Medium |
| 22 | Citibank UK | 2025 annual financial statements are public; asset-quality lines are recoverable only where explicitly disclosed. | Medium |
| 23 | Cynergy Bank | Supported gap: explicit SDDT statements for 2024 and 2025. | High |
| 24 | DB UK Bank | Do not substitute DBIGB PRA-consolidation-group templates for solo DB UK Bank without a basis decision. | High |
| 25 | FCMB UK | No KM1 template found; other capital/RWA measures may still be explicitly disclosed. | Medium |
| 26 | FidBank UK | P3 series reaches 2024; 2025 annual filing exists but 2025 P3 not established. | Medium-high |
| 27 | FirstBank UK | P3 reaches 2024; no verified 2025 standalone P3 yet. | Medium-high |
| 28 | Gatehouse Bank | Supported gap for 2025 P3; official list ends at 2024. | High |
| 29 | Ghana International Bank | 2025 annual report exists; official P3 located through 2024. | Medium-high |
| 30 | Griffin Bank | Supported gap after 2023 from enumerated report archive. | High |
| 31 | Guaranty Trust Bank UK | 2025 P3 exists and prudential data are populated; 2025 financial statements remain a separate filing question. | High / Medium |
| 32 | Gulf International Bank UK | 2025 remains a filing/publication search item; do not use asset-manager or parent-group material. | Low |
| 33 | Hampden & Co | 2024–25 annual reports exist; standalone P3 located only through 2023. | Medium-high |
| 34 | Havin Bank | No KM1/OV1 established; annual-account capital figures should not be expanded by derivation. | Medium |
| 35 | HBL Bank UK | Detailed RWA and total are available; KM1 absence appears to be report-format choice. | Medium |
| 36 | HSBC Bank plc | Recoverable at 30 June 2026. | High |
| 37 | HSBC Innovation Bank | Standalone P3 located for 2022 only; later treatment may sit within HSBC UK reporting scope and must not be substituted without an entity table. | Medium-high |
| 38 | HSBC UK Bank plc | Recoverable at 30 June 2026. | High |
| 39 | Itaú BBA International | 2024–25 KM1 absence still needs direct P3 template review; other prudential metrics are present. | Medium |
| 40 | Jordan International Bank | 2024 P3 exists; 2025 annual/P3 endpoint not established. | Medium-high |
| 41 | Julian Hodge Bank | Annual reports continue, but the public P3 series located ends at 2023. | High for archive endpoint |
| 42 | Kexim Bank UK | KM1 is present only for 2025; do not create earlier KM1 headers where the template was not published. | Medium-high |
| 43 | Kingdom Bank | 2022–25 RWA/KM1 remains a source-level research item; avoid assuming absence from older links. | Low |
| 44 | Kuwait Finance House | RWA breakdown is present; total-RWA “not disclosed” wording is contradictory and needs direct table review. | High contradiction |
| 45 | Marks & Spencer Financial Services | Prudential sheets are populated despite “no P3” wording; source/basis narrative needs correction. | High contradiction |
| 46 | Melli Bank | Total RWA exists; no detailed split/KM1 established. | Medium |
| 47 | Methodist Chapel Aid | Supported post-2023 P3 endpoint; annual reports do not supply equivalent KM1/OV1. | Medium-high |
| 48 | Metro Bank | 2025 annual report and P3 exist; balance sheet/cash-flow gap is recoverable. | High |
| 49 | Monument Bank | Official report archive needs a fresh 2025 check; current 2025 blank should not be called unavailable yet. | Low |
| 50 | Morgan Stanley Bank International | Own prudential metrics exist, but the bank does not appear to publish a standalone KM1 template. | Medium |
| 51 | National Bank of Kuwait International | 2023 and later KM1/RWA are now populated; highlighted 2023 gap appears stale. | High on status |
| 52 | National Westminster Bank plc | Recoverable for H1 2026, not FY2026 annual. | High |
| 53 | Nomura Bank International | 2026 annual report exists, but NBI is excluded from group P3 from FY2022; do not import parent/group RWA. | High |
| 54 | Northern Bank | Capital/RWA metrics exist; no standalone KM1 template established. | Medium |
| 55 | Perenna | Early-stage/legal-entity history needs direct review; no safe P3 conclusion yet. | Low |
| 56 | Persia International Bank | Recent annual figures exist; 2022–25 OV1/KM1 remains unresolved. | Low |
| 57 | Philippine National Bank Europe | Recent RWA split is populated; historical 2018/2022 and KM1 remain format/source issues. | Medium |
| 58 | Rathbones Investment Management | A 2024 Pillar 3 exists, but it is an investment-firm disclosure; bank-style KM1/OV1 expectations may be inapplicable. | High caution |
| 59 | RCI Bank UK | 2023 and 2024 P3 reports exist; earlier CET1 amount gap should be checked against those reports' comparatives, not derived from ratios. | High |
| 60 | Redwood Bank | P3 located through 2023; 2024–25 annual reports exist but no later P3 established. | Medium-high |
| 61 | Reliance Bank | 2024–26 RWA gap remains; KM1 is not used in its disclosure format. | Medium |
| 62 | Santander Financial Services | No entity-level KM1/OV1 established; Santander UK group disclosures are not an automatic substitute. | High caution |
| 63 | Santander UK | 2026 interim capital/risk data exist; latest annual period is 31 December 2025. | High |
| 64 | Schroder | Investment-firm/entity classification likely makes bank-style KM1/OV1 inappropriate; verify regulatory perimeter first. | Medium-high caution |
| 65 | StreamBank | FY2026 annual report exists; no FY2026 P3 located as of the check date. Publication timing remains plausible, so recheck rather than asserting permanent non-disclosure. | Medium-high |
| 66 | The Bank of London Group | Group/entity and authorisation history must be resolved before treating KM1/RWA as missing. | Low |
| 67 | This Bank | Annual-report metrics exist; no standalone KM1/OV1 established. | Medium |
| 68 | Triodos Bank UK | UK 2025 annual report exists; UK P3 archive ends 2024. Do not use group 2025 P3. | High |
| 69 | Turkish Bank UK | 2025 accounts and a P3 document exist; verify the document's stated reporting date and CET1 ratio. | Medium-high |
| 70 | Union Bancaire Privée UK | 2025 filing/report search remains open; do not use Swiss parent data. | Low |
| 71 | United National | CET1 capital is disclosed, but CET1 ratio/total RWA/KM1 are not established; do not back-solve. | Medium |
| 72 | Weatherbys | 2025 annual report exists; official page identifies 2024 as latest P3. | High |
| 72b | Zenith | 2025 P3 is recoverable; 2025 balance-sheet filing remains a separate check. | High / Medium |

## Mapping of unnamed lines

The unnamed entries were identified read-only from alphabetical position plus the exact year pattern in the relevant sheets:

- #12 Birmingham Bank
- #13 BLME
- #24 DB UK Bank
- #38 HSBC UK Bank plc
- #47 Methodist Chapel Aid
- #61 Reliance Bank
- second #72 Zenith

## Recommended next research order

1. Extract the three clearly available 2026 interim sets (HSBC Bank, HSBC UK Bank, NatWest Bank) into a staging note, preserving the exact 30 June/H1 date.
2. Resolve the direct contradictions at KFH and Marks & Spencer Financial Services against the first-party tables.
3. Deep-read the identified live reports for Arab Bank Europe, Bank of Beirut UK, Arbuthnot and Turkish Bank UK, with entity/basis labels captured before any figures.
4. Recheck unresolved 2025 endpoints for Monument, Kingdom, Persia, Gulf International Bank UK and Union Bancaire Privée UK through Companies House and the banks' current publication pages.
5. Keep SDDT-supported gaps distinct from simple publication lag, and do not add empty KM1 headers for periods in which no KM1 template was published.

## Metro Bank PLC: Companies House company-statement verification

Checked 17 September 2026. Companies House records Metro Bank PLC (company 06419578) accounts for the years ended 31 December 2025 and 31 December 2024, filed on 13 August 2026 and 27 May 2025 respectively. Contrary to the earlier missing-data premise, the 2025 filing contains a separate **Company balance sheet** (p.153) and **Company cash flow statement** (p.155), each with a FY2024 comparative column. The 2024 filing independently contains the Company statements on pp.145–147. Permanent first-party filing links: [FY2025 Companies House filing](https://find-and-update.company-information.service.gov.uk/company/06419578/filing-history/MzUzODAzNTg0NWFkaXF6a2N4/document?download=0&format=pdf), [FY2024 Companies House filing](https://find-and-update.company-information.service.gov.uk/company/06419578/filing-history/MzQ2NzY4OTg1OGFkaXF6a2N4/document?download=0&format=pdf), and [filing-history metadata](https://find-and-update.company-information.service.gov.uk/company/06419578/filing-history).

### Company balance sheet (reported £m)

| Line item | FY2025 | FY2024 |
|---|---:|---:|
| Cash and balances with other banks | 2,176 | 2,811 |
| Loans and advances to customers | 8,040 | 8,472 |
| Investment securities held at FVOCI | 218 | 377 |
| Investment securities held at amortised cost | 3,942 | 4,113 |
| Derivative financial assets | 23 | 16 |
| Property, plant and equipment | 705 | 711 |
| Intangible assets | 138 | 121 |
| Investment in subsidiaries | 15 | 15 |
| Prepayments and accrued income | 70 | 84 |
| Deferred tax assets (net) | 225 | 237 |
| Other assets | 949 | 640 |
| **Total assets** | **16,501** | **17,597** |
| Deposits from customers | 13,445 | 14,458 |
| Deposits from central banks | 400 | 400 |
| Debt securities | 688 | 679 |
| Repurchase agreements | 73 | 391 |
| Derivative financial liabilities | — | 1 |
| Lease liabilities | 185 | 205 |
| Deferred grants | 10 | 13 |
| Provisions | 6 | 11 |
| Other liabilities | 181 | 237 |
| **Total liabilities** | **14,988** | **16,395** |
| Called-up share capital and share premium | 144 | 144 |
| Retained earnings | 1,096 | 1,040 |
| Other equity instruments | 250 | — |
| Other reserves | 23 | 18 |
| **Total equity** | **1,513** | **1,202** |
| **Total equity and liabilities** | **16,501** | **17,597** |

The em dash above is the filing's presentation, not an inferred zero. Source: FY2025 Companies House filing, p.153 (FY2025 and comparative FY2024); cross-check FY2024 filing, p.145.

### Company cash flow (reported £m)

| Line item | FY2025 | FY2024 verification status |
|---|---:|---:|
| Profit/(loss) before tax | 94 | See note below |
| Non-cash items | (401) | See note below |
| Interest received | 748 | See note below |
| Interest paid | (319) | See note below |
| Changes in other operating assets | 96 | See note below |
| Changes in other operating liabilities | (1,323) | See note below |
| **Net cash outflows from operating activities** | **(1,105)** | **(1,383)** |
| Sales, redemptions and maturities of investment securities | 1,154 | 1,017 |
| Purchase of investment securities | (816) | (630) |
| Purchase of property, plant and equipment | (34) | (41) |
| Purchase and development of intangible assets | (48) | (19) |
| **Net cash inflows from investing activities** | **256** | **327** |
| Repayment of capital elements of leases | (19) | (22) |
| Issuance of shares and other equity instruments | 250 | — |
| Distributions on other equity instruments | (17) | — |
| **Net cash inflows/(outflows) from financing activities** | **214** | **(22)** |
| **Net decrease in cash and cash equivalents** | **(635)** | **(1,078)** |
| Cash and cash equivalents at start of year | 2,811 | 3,889 |
| **Cash and cash equivalents at end of year** | **2,176** | **2,811** |

Source: FY2025 Companies House filing, p.155; FY2024 filing, p.147. The FY2024 investing, financing and cash-reconciliation figures above are company-level figures and reconcile exactly: (1,383) + 327 + (22) = (1,078), and 3,889 − 1,078 = 2,811. **Extraction limitation:** the browser-accessible text rendition of the 2025 filing dropped the second numeric column for the six FY2024 operating-reconciliation components (profit/loss, non-cash items, interest received/paid, and the two operating-asset/liability movements). I therefore have not copied the consolidated figures into those company cells or fabricated values; those six cells still require direct page-147/PDF extraction. The company total is independently fixed at £(1,383)m by the filed cash reconciliation.

### Fit against `scripts/build_metro_bank.py` (read-only review)

- The existing balance-sheet rows accept every FY2025/FY2024 amount except the separately reported **Other equity instruments** (£250m in FY2025). The script correctly leaves that £250m inside total equity rather than misclassifying it, but a complete component presentation cannot be achieved without adding a row. Also, the current label “Cash and balances with the Bank of England” is narrower than the filing's “Cash and balances with other banks”.
- The existing cash-flow rows accept all FY2024 lines shown above without splitting the table. For FY2025, the £250m issuance can occupy the existing issuance row only if its label is broadened from “new shares” to “shares and other equity instruments”; the separate £(17)m distribution line has no existing row. Net financing cash flow of £214m is already exact, but fully faithful components require one added row.
- The amounts already present in `bs_rows` for FY2025/FY2024 and in `cash_rows` for FY2025 agree with the filed company statements. The material outstanding population is the FY2024 company cash-flow column, particularly its six operating-reconciliation components. No worksheet or script was modified in this research pass.
