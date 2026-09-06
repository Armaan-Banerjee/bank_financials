# HD-078 Co-operative Bank FY2014–FY2012 deep verification

## Primary sources

- [2014 Annual Report and Accounts](https://www.co-operativebank.co.uk/assets/pdf/bank/investorrelations/annual-report.pdf), Bank statements pp.149–154 (PDF pages 149–154).
- [2013 Annual Report and Accounts](https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/financialresults/bank-r-and-a.pdf), Bank statements pp.128–133 (PDF pages 128–133).

Both reports identify the figures as the Bank financial statements (the Bank and its controlled subsidiaries), rather than the parent Company-only statements. The 2013 report states that the 2012 balance-sheet comparatives were restated for tangible/intangible/intercompany assets and deferred-tax presentation (p.130; note 3, pp.153–155).

## Findings

### FY2014

The existing FY2014 statutory statement data agrees with the 2014 report on the Bank income statement (p.149), Bank cash flow statement (pp.152–153), and Bank statement of changes in equity (p.154). The source prints Total equity as **£2,014.5m** (with a thousands separator); the builder's numeric `2014.5` is therefore correct and is **not** a transcription error. It ties: £35,568.4m liabilities + £2,014.5m equity = £37,582.9m total assets.

The source also confirms the 2014 cash-flow controls: operating **(1,583.2)**, investing **390.9**, financing **677.2**, net decrease **(515.1)**, opening cash **6,092.2**, closing cash **5,577.1** (2014 report pp.152–153).

### FY2013

The existing FY2013 income statement and equity data agree with the Bank statement in the 2013 report: operating income **270.1**, loss before tax **(586.2)**, tax **(161.8)**, loss attributable to equity holders **(748.9)**, and total equity **1,777.3** (pp.128, 130, 133). The source’s comprehensive-income statement gives total comprehensive expense **(841.4)** (p.129), while the equity roll-forward separates the LME-related £677.2m comprehensive-income effect (p.133).

The FY2013 Bank cash-flow statement is available and should be added to the currently FY2014-only cash-flow range. Exact controls from pp.131–132:

| Line | FY2013 | FY2012 restated comparative |
|---|---:|---:|
| Loss before taxation | (586.2) | (673.7) |
| Net cash from operating activities | (2,480.2) | 893.5 |
| Purchase tangible/intangible fixed assets | (55.7) | (90.4) |
| Proceeds sale fixed assets | 1.7 | 1.0 |
| Proceeds sale investment property | 1.3 | 0.9 |
| Purchase investment securities | (4,425.3) | (4,960.9) |
| Proceeds sale/maturity investment securities | 6,681.2 | 2,616.4 |
| Net cash from investing activities | 2,203.2 | (2,433.0) |
| Interest paid other borrowed funds | (83.9) | (87.4) |
| Repayment other borrowed funds | – | (256.5) |
| Issuance other borrowed funds | – | 235.4 |
| Dividends to securitisation holding companies | – | (0.3) |
| Dividends to minority interests | (0.2) | (0.3) |
| Preference share dividends | (5.9) | (5.6) |
| Capital contribution from parent | – | 80.0 |
| Cash proceeds relating to LME | 145.0 | – |
| Net cash from financing activities | 55.0 | (34.7) |
| Net decrease in cash and equivalents | (222.0) | (1,574.2) |
| Opening cash and equivalents | 6,314.2 | 7,888.4 |
| Closing cash and equivalents | 6,092.2 | 6,314.2 |

The cash-flow statement explains that the figures differ from balance-sheet movements because of non-cash Britannia transfer-of-engagement fair-value unwinds and restatement of amounts owed by/to Co-operative Group undertakings (p.132).

### FY2012 restatement issue

The current builder uses the FY2012 accounts’ originally reported Bank balance sheet values. The later 2013 report provides the Bank’s **restated** FY2012 comparative. These are not interchangeable. Examples (2013 report p.130; note 3 pp.153–155):

| Balance-sheet line | Current builder FY2012 | 2013 report restated FY2012 |
|---|---:|---:|
| Loans and advances to banks | 1,047.2 | 1,904.1 |
| Loans and advances to customers | 22,785.5 | 33,339.5 |
| Derivatives | 590.9 | 818.8 |
| Investment securities (sum of disclosed categories) | 6,744.7 | 6,889.8 |
| Property, plant and equipment | 46.2 | 113.4 |
| Intangible fixed assets | 33.8 | 263.2 |
| Amounts owed by Group undertakings | 12,813.0 | 56.8 |
| Current tax assets | 154.0 | 172.6 |
| Deferred tax assets | 138.8 | 159.6 |
| Total assets | 51,818.5 | 49,772.8 |
| Total liabilities | 50,189.4 | 47,922.6 |
| Total equity | 1,629.1 | 1,850.2 |

The 2013 report says the restatement moved assets funded by the Bank from CFSMS onto the Bank balance sheet: PPE **64.1 → 113.4**, intangible fixed assets **34.9 → 263.2**, and amounts owed by Group undertakings **256.4 → 56.8** at 31 December 2012; related liabilities changed from **112.0 → 190.0** (note 3, p.154). It says there was **no impact on 2012 income statement**, but the statement-of-cash-flow presentation changed; operating cash flow is shown as **886.5 as reported vs 1,209.9 restated** in the note (p.226), while the Bank cash-flow statement itself reports the restated comparative **893.5** (pp.131–132; the note's 886.5/1,209.9 appears to concern a different presentation/control and needs care).

### Recommendation

1. No FY2014 equity correction is needed; `2014.5` correctly represents £2,014.5m.
2. Add the Bank cash-flow statement for FY2013 and its restated FY2012 comparative using the table above, with source pages 131–132.
3. Decide whether the workbook’s historical convention is “each year as originally reported” or “latest restated comparative.” For analytical continuity, the later restated FY2012 balance sheet (and corresponding equity 1,850.2) is the stronger choice; if retaining original-year values, add an explicit restatement bridge rather than silently mixing bases. The FY2013 report’s restated balance sheet is internally coherent and is the basis used by the subsequent 2014 report, subject to the further FY2014 restatement of FY2013.
