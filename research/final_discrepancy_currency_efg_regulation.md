# Final discrepancy research: FirstBank UK and EFG Private Bank

**Research date:** 29 August 2026  
**Scope:** FirstBank UK FY2022 RWA discrepancy; EFG Private Bank FY2022 cash-flow discrepancy; whether UK prudential changes introduced around 2022 explain either issue.  
**Source rule:** primary sources only. No workbook, builder, ticket, map, or shared review document was modified.

## Executive conclusions

1. **FirstBank UK is a currency/vintage presentation issue, not a disagreement between two USD RWA figures.** The 2022 FirstBank Pillar 3 report reports FY2022 in GBP: RWA **£1,019,070k**. The 2023 Pillar 3 report says the Bank changed reporting and functional currency to USD from 1 January 2023 and restated 2022 figures in USD; its FY2022 comparative is **$1,230,686k**. The same implied GBP/USD conversion is also present in the CET1 and total-capital figures, and the ratios are unchanged. The current workbook's FY2022 RWA value of `1,019,070` under a `$'000` unit is therefore the item that needs correction; the underlying FirstBank disclosures are not contradictory.

2. **EFG's £4,840k cash-flow difference is fully explained by a later restatement.** EFG's own 2022 report included a **£4,840k** term deposit in cash and cash equivalents. The 2023 report states that it was long-term dated and did not meet the cash-and-cash-equivalents definition, so the 2022 comparative was restated to exclude it. That changed the 2022 net operating cash flow from **£547,141k** to **£542,301k**, net cash outflows from **£(57,736)k** to **£(62,576)k**, and closing cash from **£1,308,463k** to **£1,303,623k**. The apparent **£4,840k** arithmetic gap is the reclassification, not an unexplained source error.

3. **The UK 2022 regulatory changes explain a disclosure/basis change for NSFR, not either disputed amount.** FirstBank itself says the new CRR2 NSFR rules commenced on 1 January 2022 and that the prior period was not comparable. The PRA's implementation material confirms the Basel/CRR policy took effect on 1 January 2022. These prudential changes do not explain FirstBank's USD conversion and do not explain EFG's statutory cash-equivalent reclassification.

## 1. FirstBank UK: currency and source-vintage reconciliation

### Source figures

FirstBank's **2022 Pillar 3 Disclosures**, Table 6 (printed p.19), reports the Bank's 31 December 2022 reporting/functional currency as GBP and gives:

| FY2022 metric | FirstBank 2022 report, GBP'000 |
|---|---:|
| CET1 capital | 229,026 |
| Total capital | 265,764 |
| Total risk-weighted exposure amounts | 1,019,070 |
| CET1 ratio | 22.47% |
| Total capital ratio | 26.08% |

The same report states that, as at 31 December 2022, the reporting and functional currency was GBP and that it changed to USD from 1 January 2023. It also states that the new NSFR rules arising from CRR2 commenced on 1 January 2022.

FirstBank's **2023 Pillar 3 Disclosures**, printed p.1 and Table 1 (printed p.3), state that the Bank changed its reporting and functional currency from GBP to USD on 1 January 2023 and that 2022 figures were restated in USD. The FY2022 comparative is:

| FY2022 metric | FirstBank 2023 report, USD'000 |
|---|---:|
| CET1 capital | 276,585 |
| Total capital | 320,951 |
| Total risk-weighted exposure amounts | 1,230,686 |
| CET1 ratio | 22.47% |
| Total capital ratio | 26.08% |

### Calculation

The implied conversion factors are:

```text
RWA:          1,230,686 / 1,019,070 = 1.207656 USD per GBP
CET1 capital:   276,585 /   229,026 = 1.207658 USD per GBP
Total capital:  320,951 /   265,764 = 1.207654 USD per GBP
```

The tiny differences are rounding. Applying the RWA-implied factor to the original GBP RWA gives exactly the reported USD comparative:

```text
£1,019,070k × 1.207656 ≈ $1,230,686k
```

The ratios also reconcile on both bases:

```text
£229,026k / £1,019,070k = 22.4740%  → reported 22.47%
$276,585k / $1,230,686k = 22.4741%  → reported 22.47%

£265,764k / £1,019,070k = 26.0791%  → reported 26.08%
$320,951k / $1,230,686k = 26.0790%  → reported 26.08%
```

### Finding for the workbook

This is **not** a disagreement in FirstBank's own USD figures. It is the same FY2022 regulatory position shown first in GBP and later restated by FirstBank in USD. The workbook currently mixes the 2023 report's USD capital/ratio figures with the 2022 report's unconverted GBP RWA number while labelling the sheet `$'000`. If the workbook remains USD-based, the defensible FY2022 RWA value is **$1,230,686k**, sourced to the Bank's 2023 comparative. No change was made during this research pass.

## 2. EFG Private Bank: FY2022 cash-flow reconciliation

### Original FY2022 report

EFG's **Annual Report 2022**, Cash Flow Statement (printed p.22), reports in GBP'000:

| FY2022 line | Original 2022 report |
|---|---:|
| Net cash from operating activities | 547,141 |
| Net cash from investing activities | (597,130) |
| Net cash from financing activities | (7,747) |
| Net cash inflows/(outflows) | (57,736) |
| Effect of foreign exchange on cash and cash equivalents | (3,042) |
| Cash and cash equivalents at beginning | 1,369,241 |
| Cash and cash equivalents at end | 1,308,463 |

The original statement's cash-flow arithmetic is:

```text
547,141 - 597,130 - 7,747 = (57,736)
(57,736) - 3,042 = (60,778)
1,369,241 - 60,778 = 1,308,463
```

Thus the original report's operating/investing/financing subtotal, FX line, opening balance, and closing balance are internally consistent with a **£(60,778)k** net change.

EFG's Note 10 (printed p.31) explains that the original £1,308,463k total included **£4,840k** due from other banks at term. The note also states that cash and cash equivalents for the cash-flow statement comprise balances with less than 90 days' maturity. The £4,840k balance was also shown as pledged due from other banks.

### Later restatement in the 2023 report

EFG's **Annual Report 2023**, Cash Flow Statement (printed pp.24–25), presents a restated FY2022 comparative:

| FY2022 line | Original 2022 report | Restated in 2023 report | Change |
|---|---:|---:|---:|
| Net cash from operating activities | 547,141 | 542,301 | (4,840) |
| Net cash from investing activities | (597,130) | (597,130) | — |
| Net cash from financing activities | (7,747) | (7,747) | — |
| Net cash outflows | (57,736) | (62,576) | (4,840) |
| FX effect | (3,042) | (3,042) | — |
| Net change in cash | implied (60,778) | (65,618) | (4,840) |
| Closing cash | 1,308,463 | 1,303,623 | (4,840) |

The restated arithmetic is:

```text
542,301 - 597,130 - 7,747 = (62,576)
(62,576) - 3,042 = (65,618)
1,369,241 - 65,618 = 1,303,623
```

The 2023 report explicitly says that prior-year closing cash was restated to exclude the **£4,840k bank term deposit**, because it was long-term dated and did not meet the definition of cash and cash equivalents. It further says that the movement is reflected in the `(Increase) in other assets` line. The restated comparative shows that line as **£(6,859)k**, versus **£(2,019)k** in the original 2022 report—a difference of exactly **£(4,840)k**.

### Finding for the workbook

The issue is a **mixed-vintage presentation** in the current workbook: it retains the original 2022 report's **£(57,736)k** net outflows and **£1,308,463k** closing cash, but uses the later restated **£(65,618)k** net-change figure. The original 2022 vintage should reconcile to **£(60,778)k** net change; the later restated vintage should use **£(62,576)k**, **£(65,618)k**, and **£1,303,623k** together.

Given the project's stated preference in the builder for each year's own originally published statement, the cleanest future fix would be either:

- retain the original 2022 vintage and change the net-change figure to **£(60,778)k**, documenting the later £4,840k restatement; or
- adopt the later restated comparative consistently across all affected lines.

This research pass did not modify the workbook or builder.

## 3. UK regulatory changes around 2022

The relevant change identified in the primary regulatory material is the UK's implementation of the Basel/CRR changes, including the NSFR framework. The PRA's **PS22/21 – Implementation of Basel standards** says the policy material would take effect on **1 January 2022**. The PRA's later Strong and Simple consultation describes the NSFR as introduced by the PRA on **1 January 2022**. FirstBank's own 2022 Pillar 3 report independently states that the new CRR2 NSFR rules commenced on that date and that prior-period NSFR data was not available on a comparable basis.

This matters for interpreting the regulatory sheets: a 2022 NSFR value can appear while a comparable 2021 NSFR value is absent, and the reporting template/basis can change. It does **not** provide an explanation for the FirstBank RWA issue because FirstBank's RWA discrepancy is exactly explained by the Bank's GBP-to-USD restatement. It also does **not** provide an explanation for EFG's £4,840k difference because EFG's later statutory accounts expressly attribute that difference to the maturity/classification of a bank term deposit in the cash-and-cash-equivalents definition.

The PRA's 2022 **PS7/22** also amended the NSFR disclosure template/instructions, with the relevant policy changes implemented on 1 September 2022. That is a disclosure/reporting change, not evidence of a change to EFG's statutory cash-flow classification.

## Sources inspected

### FirstBank UK

- [FirstBank UK Pillar 3 Disclosures, 31 December 2022](https://www.fbnbank.co.uk/wp-content/uploads/2019/06/FirstBank-UK-Pillar-3-Dec-2022-V1.0.pdf) — printed pp.1–2, 19, and 23; Table 6 and OV1.
- [FirstBank UK Pillar 3 Disclosures, 31 December 2023](https://www.fbnbank.co.uk/wp-content/uploads/2019/06/FirstBank-UK-Pillar-3-Dec-2023.pdf) — printed pp.1 and 3; Table 1 and currency/basis statement.
- [FirstBank UK Companies House filing history](https://find-and-update.company-information.service.gov.uk/company/04459383/filing-history) — entity and annual-report filing context; the builder's direct filed-report URLs were also inspected locally.

### EFG Private Bank

- [EFG Private Bank Annual Report 2022](https://www.efginternational.com/doc/jcr%3A66b888d9-09dc-4c14-9db2-8c6006ca4a8c/EFGL_2022_Annual_Report_FINAL_BDO%20signed.pdf/lang%3Aen/EFGL_2022_Annual_Report_FINAL_BDO%20signed.pdf) — printed p.22 Cash Flow Statement and p.31 Note 10.
- [EFG Private Bank Annual Report 2023](https://www.efginternational.com/doc/jcr%3Ab5a29f1b-48a8-4112-8c77-4aa74359ec2e/Annual%20Report%20and%20Financial%20Statements%2031%20December%202023.pdf/lang%3Aen/Annual%20Report%20and%20Financial%20Statements%2031%20December%202023.pdf) — printed pp.24–25 Cash Flow Statement and restatement explanation.
- [EFG Private Bank Companies House filing history](https://find-and-update.company-information.service.gov.uk/company/02321802/filing-history) — confirms the 2022 accounts were filed on 4 August 2023 and the 2023 accounts on 10 May 2024.

### UK regulatory material

- [PRA PS22/21 – Implementation of Basel standards](https://www.bankofengland.co.uk/prudential-regulation/publication/2021/october/implementation-of-basel-standards) — final policy material effective 1 January 2022.
- [PRA CP4/23 – Strong and Simple Framework: Liquidity and Disclosure requirements](https://www.bankofengland.co.uk/prudential-regulation/publication/2023/february/strong-and-simple-framework) — explains that the PRA introduced NSFR on 1 January 2022.
- [PRA PS7/22 – Responses to Occasional Consultation Paper](https://www.bankofengland.co.uk/prudential-regulation/publication/2022/march/occassional-consultation-paper-march-2022) — includes amendments to the NSFR disclosure template and instructions.

## Files inspected and timing

Read-only local inspection covered `scripts/build_firstbank_uk.py`, `scripts/build_efg_private_bank.py`, the corresponding FirstBank and EFG workbooks, and `wayfinder/tickets/WF-009.md`. Official FirstBank and EFG reports, Companies House filing-history pages, and PRA regulatory pages were then checked against the local figures. Completion timestamp: **29 August 2026, 13:57:45 BST**. The orchestration did not expose a reliable start timestamp, so an elapsed duration is not fabricated. No repository files other than this research note were changed.
