# Regulatory benchmark and threshold context

**Research date:** 2026-08-30  
**Purpose:** source-backed context for IN-020. These are reference points, not
universal pass/fail tests. A displayed observation must match metric, unit,
jurisdiction, firm scope, consolidation basis, and effective period before a
distance-to-context value is permitted.

## Supported context records

| Metric | Context type | Value | Scope and basis | Effective/date caveat | Source |
|---|---|---:|---|---|---|
| CET1 ratio | Pillar 1 minimum | 4.5% of RWAs | UK firms subject to the risk-based capital framework | Minimum requirement; excludes firm-specific Pillar 2A and buffers | [PRA/BoE Basel 3.1 implementation summary](https://www.bankofengland.co.uk/prudential-regulation/publication/2022/november/implementation-of-the-basel-3-1-standards/output-floor) |
| Tier 1 ratio | Pillar 1 minimum | 6.0% of RWAs | UK firms subject to the risk-based capital framework | Minimum requirement; excludes firm-specific Pillar 2A and buffers | [PRA/BoE Basel 3.1 implementation summary](https://www.bankofengland.co.uk/prudential-regulation/publication/2022/november/implementation-of-the-basel-3-1-standards/output-floor) |
| Total capital ratio | Pillar 1 minimum | 8.0% of RWAs | UK firms subject to the risk-based capital framework | Minimum requirement; excludes firm-specific Pillar 2A and buffers | [PRA/BoE Basel 3.1 implementation summary](https://www.bankofengland.co.uk/prudential-regulation/publication/2022/november/implementation-of-the-basel-3-1-standards/output-floor) |
| CET1 ratio | Capital conservation buffer | 2.5% of RWAs | UK banks, as a buffer expected above minimum requirements | Buffer, not a standalone minimum; usable in stress and distinct from PRA buffer | [BoE bank capital framework](https://www.bankofengland.co.uk/-/media/boe/files/stress-testing/2024/boes-approach-to-stress-testing-the-uk-banking-system.pdf) |
| Leverage ratio | UK minimum/expectation | 3.25% of UK leverage exposure measure | Requirement applies to major UK firms and firms with significant non-UK assets; other firms have a supervisory expectation | Current cited framework; scope thresholds and buffers matter; exposure measure excludes qualifying central-bank claims | [PRA CP2/25](https://www.bankofengland.co.uk/prudential-regulation/publication/2025/march/leverage-ratio-changes-to-the-retail-deposits-threshold-for-application-of-the-requirement) |
| LCR | Liquidity requirement | 100% | Credit institutions under the UK liquidity framework | May fall below 100% during stress under the stated derogation; not a capital threshold | [PRA CRR Instrument 2021](https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/policy-statement/2021/october/ps2221app1.pdf) |
| NSFR | Stable-funding requirement | 100% | Firms under the UK NSFR framework, subject to applicable permissions/exemptions | One-year horizon; the PRA recognises stress conditions may produce a lower ratio | [PRA CP5/21](https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/consultation-paper/2021/february/cp521.pdf) |
| MREL | Firm-specific resolution requirement | No universal value | UK resolution entities with bail-in or transfer strategies | Annual, firm-specific; may be expressed on RWA or leverage-exposure basis; 2026 publication applies from 1 Jan 2026 | [BoE MRELs 2026](https://www.bankofengland.co.uk/financial-stability/resolution/mrels-2026) |

## Interpretation rules

- A regulatory minimum, buffer, supervisory expectation, management target, and
  observed value are different fields and must not be combined.
- The 4.5/6/8% capital records are Pillar 1 minima, not a bank's complete
  binding requirement. Pillar 2A, systemic buffers, countercyclical buffers,
  and the PRA buffer may apply in addition; the PRA buffer is firm-specific and
  not publicly disclosed in the cited framework.
- MREL is deliberately represented as firm-specific context. The Bank of
  England's 2026 table provides selected firm values, but it is not a universal
  threshold for every bank in this dataset.
- Historical observations are only matched where the context record's
  effective interval is known and the observation's scope/basis is compatible.
  Otherwise the output says why context is unavailable.
