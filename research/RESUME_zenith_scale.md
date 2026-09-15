# Zenith 1000x scale defect — fix log (2026-09-15)

Target: `scripts/build_zenith.py` -> `banks/ZENITH FINANCIALS.xlsx`
Ticket source: `research/RESUME_SESSION.md` section 8a.

## 1. VERIFICATION OF THE DIAGNOSIS — CONFIRMED FROM PRIMARY SOURCES

The Pillar 3 dictionaries hold **US$'000**, not raw USD. Confirmed by opening the cited
source PDFs, not by inference.

### FY2024 Pillar 3 (`media/2274/31dec24-pillar-3-zbuk.pdf`, section 9 "Key Metrics", p.17)
Table header reads `Available own funds (US$)` and **every figure carries a literal
trailing " k"**:

```
Common Equity Tier 1 (CET1) capital                            378,325 k    338,086 k
Tier 1 capital                                                 378,325 k    338,086 k
Total capital                                                  378,325 k    338,086 k
Total risk-weighted exposure amount*                         1,475,750 k  1,203,364 k
Total exposure measure excluding claims on central banks      2,987,483 k  2,872,422 k
Total high-quality liquid assets (HQLA) (Weighted – average)  1,013,789 k  1,147,653 k
Total net cash outflows (adjusted value)                        306,820 k    369,648 k
Total available stable funding (avg last four quarters)       1,136,904 k  1,066,880 k
Total required stable funding (avg last four quarters)          768,308 k    744,377 k
```

The same page's footnote spells the unit out in prose: *"the average ASF **US$1,136,904k**
/ the average RSF **US$768,308k** = 147.98%"*.

Independent corroboration inside the same document (section UK CC1, p.20): the Bank's
share capital is **"136,701,620 ordinary shares of US$1"** and the capital table renders
that line as **`136,702 k`**. A figure known to be US$136,701,620 printed as 136,702 is
proof that the table scale is thousands.

### FY2024 Pillar 3, UK OV1 (p.21) — the RWA Breakdown source
Column header `US$`, every cell suffixed ` k`:
`Credit Risk (excluding CCR) 1,205,520 k / CCR 98,068 k / of which CVA 1,392 k /
Market risk 4,202 k / Operational Risk (BIA) 167,960 k / Amounts below thresholds 1,024 k /
Total 1,475,750 k`. All match `rwa_rows_usd` literally.

### FY2015 Pillar 3 (Wayback `ZBL_Pillar_3_Disclosure_Document_2015.pdf`, s.4.2/4.3)
Explicit column header **`US$000's`**:
`Share capital 136,702 / Profit and loss reserve 53,819 / Total tier 1 capital 190,521`
and `Credit Risk 68,766 / Market Risk 451 / Operational Risk 4,755 / Total 73,972 /
Regulatory Available Capital 188,483`.
188,483 == `CET1_TIER1_TOTAL_USD["FY2015"]`. 68,766/0.08 = 859,575 == the FY2015 Credit
Risk row; 451/0.08 = 5,638; 4,755/0.08 = 59,438; sum 924,650 == `RWA_USD["FY2015"]`.

### Contrast — the statement dicts really are raw USD
`bs_rows_usd` FY2024 Share Capital = **136,701,620**, i.e. the same capital expressed in
whole dollars. So `stock()`/`flow()`'s `/1000` is correct there and only there.

**Conclusion: diagnosis confirmed. The `/1000` in `stock()` must not be applied to the
Pillar 3 / RWA Breakdown dicts.**

## 2. CALL SITES CHANGED

New helper `stock_k()` added next to `stock()` (FX only, no `/1000`). Repointed:

| # | Sheet | Line (pre-edit) | Was | Now |
|---|---|---|---|---|
| 1 | CET1 Capital | 1309 | `stock(CET1_TIER1_TOTAL_USD)` | `stock_k(...)` |
| 2 | Tier 1 Capital | 1313 | `stock(CET1_TIER1_TOTAL_USD)` | `stock_k(...)` |
| 3 | Total Capital | 1317 | `stock(CET1_TIER1_TOTAL_USD)` | `stock_k(...)` |
| 4 | Total RWAs | 1321 | `stock(RWA_USD)` | `stock_k(...)` |
| 5 | RWA Breakdown | 1352 | `stock(v)` per row | `stock_k(v)` |
| 6 | Leverage Ratio | 1411 | `stock({exposure measure})` | `stock_k(...)` |
| 7 | LCR | 1435 | `stock({HQLA})` | `stock_k(...)` |
| 8 | LCR | 1436 | `stock({net cash outflows})` | `stock_k(...)` |
| 9 | NSFR | 1472 | `stock({ASF})` | `stock_k(...)` |
| 10 | NSFR | 1473 | `stock({RSF})` | `stock_k(...)` |
| 11 | FY2011 Basel II rows | 1275-1276 | `43.6` / `40.0` | `43631` / `40002` (true £'000 per HIST_P3_NOTE) |

NOT changed (verified, deliberately):
- `stock2`/`flow2`/`opening_cash2`/`eq_stock`/`eq_flow`/`eq_gbp` — statement sheets, raw USD
  or raw GBP. Correct as they stand.
- Asset Quality (`aq_rows_usd`, `stock()` at line 1182) — sourced from the Annual Reports,
  raw USD (FY2024 gross exposure 446,909,206). Correct as it stands.
- Overview sheet — passes only statement totals (raw USD) and ratio strings. It carries no
  Pillar 3 absolute amount at all, so it needed no rescaling. Verified by reading the
  `add_overview_sheet(...)` call and by re-reading the built sheet after the rebuild.
- All ratio series (`CAPITAL_RATIO`, leverage %, LCR %, NSFR %) — strings, scale-invariant.

## 3. CONSISTENCY / RATIO-REPRODUCTION RESULTS

(filled in after rebuild — see section 4)
