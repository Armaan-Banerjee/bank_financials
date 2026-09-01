# Follow-up: provisional parent classifications

Research date: 2026-08-29. Sources are official Companies House records and
the banks' own reports/sites. The aim was to decide whether a third
classification is needed. Conclusion: it is not. The map can use two
operational categories, provided the second is named **standalone or
non-single-parent ownership** and historical ownership is retained as a
time-bounded edge.

## Findings

### Allica Bank Limited

Companies House currently identifies Warwick Capital Partners LLP as an
active person with significant control, with more than 25% but not more than
50% of shares/votes and director-appointment rights. Earlier institutional
controllers (including TCV XI AB Holdings and ACM AB Equity Holdings) are
shown as ceased. Allica's own investor-relations page confirms the bank's
annual reports and Pillar 3 publications but does not identify a single
ultimate corporate parent.

**Classification:** standalone/non-single-parent ownership, specifically
institutional-investor controlled. Keep an `owned_by` edge to Warwick Capital
Partners LLP and do not invent a single ultimate-parent node.

Sources: [Companies House PSC record](https://find-and-update.company-information.service.gov.uk/company/07706156/persons-with-significant-control), [Allica investor relations](https://www.allica.bank/investor-relations).

### Alpha Bank London Limited

The current Companies House PSC record identifies Alpha Bank S.A. as active,
with 75% or more of shares and votes, notified on 20 April 2021. It also
records Alpha Services and Holdings SA and Alpha Bank A.E. as ceased PSCs on
that date. This resolves the previous uncertainty: the UK entity belongs to
Alpha Bank S.A.'s group, while the older holding-company identity is
historical.

**Classification:** confirmed group-owned. Add `Alpha Bank S.A.` as the
immediate parent and the wider Alpha group as the ultimate/group node.

Source: [Companies House PSC record](https://find-and-update.company-information.service.gov.uk/company/00185070/persons-with-significant-control).

### Birmingham Bank Limited

Companies House records Better Home and Finance Holding Company, a Delaware
holding company, as an active PSC with 75% or more of shares and votes,
notified on 22 December 2025. The filing history shows that this replaced the
prior “no registrable person or relevant legal entity” statement, which was
withdrawn on the same date. Therefore ownership was genuinely unresolved in
the historical workbook window but is confirmed currently.

**Classification:** confirmed group-owned from 22 December 2025; retain a
historical pre-acquisition standalone/no-registrable-parent state for the
2021–2025 observations.

Sources: [Companies House PSC record](https://find-and-update.company-information.service.gov.uk/company/00555071/persons-with-significant-control), [Companies House filing history](https://find-and-update.company-information.service.gov.uk/company/00555071/filing-history).

### ClearBank Limited

Companies House identifies Clearbank Group Holdings Limited as the active PSC
from 8 December 2023, with director-appointment rights. ClearBank's 2023
annual report identifies that company as the immediate parent and CB Growth
Holdings Limited as the ultimate parent. The 2025 annual report likewise
describes CB Growth Holdings Limited as the ultimate parent and ClearBank
Limited/ClearBank Europe N.V. as subsidiaries.

**Classification:** confirmed group-owned. Use the chain
`ClearBank Limited → Clearbank Group Holdings Limited → CB Growth Holdings
Limited`; the prior PPF/CFFI investor structure is historical.

Sources: [Companies House PSC record](https://find-and-update.company-information.service.gov.uk/company/09736376/persons-with-significant-control), [ClearBank 2023 annual report](https://marketing.clear.bank/hubfs/Reports/ClearBank-Annual-reports-and-accounts-2023.pdf), [ClearBank 2025 annual report](https://clear.bank/uploads/assets/ClearBank-Annual-Report-2025.pdf).

### Griffin Bank Ltd

Companies House records an active statement, notified on 10 August 2020,
that the company knows or has reasonable cause to believe there is no
registrable person or registrable relevant legal entity. The former founders'
PSC entries are ceased. This is stronger evidence than simply failing to find
a parent.

**Classification:** confirmed standalone/non-single-parent ownership, with a
Companies House “no registrable parent/controller” qualification. No group
parent should be inferred from the Griffin brand.

Source: [Companies House PSC record](https://find-and-update.company-information.service.gov.uk/company/10842931/persons-with-significant-control).

### Monument Bank Limited

Companies House records an active “no registrable person or registrable
relevant legal entity” statement, notified on 17 January 2024. The previous
PSC entries (including Mintoo Bhandari) are ceased. Monument Technology
Limited is a subsidiary of Monument Bank, not its parent. The bank's official
annual-report page confirms that the available reports are published for
Monument Bank itself.

**Classification:** confirmed standalone/non-single-parent ownership. The
existing “Monument Bank Group” wording should describe an internal reporting
group only, not an external parent.

Sources: [Companies House PSC record](https://find-and-update.company-information.service.gov.uk/company/10921940/persons-with-significant-control), [Monument Bank official reports](https://www.monument.co/annual-reports), [Monument Technology PSC record](https://find-and-update.company-information.service.gov.uk/company/15281121/persons-with-significant-control).

### GB Bank Limited

Companies House currently records Sameer Gehlaut as active, holding more than
50% but less than 75% of shares and at least 75% of voting rights, and the
Teeside Pension Fund/Middlesbrough Council as an active voting-rights
controller. No corporate parent is shown. This is an ownership/control
structure, not an unidentified bank group. The possible SilverRock regulatory
consolidation noted in the bank's disclosure is a reporting-scope issue, not
evidence of a parent company.

**Classification:** standalone/non-single-parent ownership, with named
investor/local-authority controllers. Keep any SilverRock relationship as a
separate `regulatory_consolidated_into` edge if it becomes effective.

Source: [Companies House PSC record](https://find-and-update.company-information.service.gov.uk/company/10702260/persons-with-significant-control).

## Proposed map treatment

Reclassify Alpha Bank London, Birmingham Bank (from 22 December 2025), and
ClearBank into confirmed group-owned. Reclassify Allica, Griffin, Monument,
and GB Bank into confirmed standalone/non-single-parent ownership. Keep the
effective dates and pre-change states as historical edges. This removes the
third provisional category without pretending that every bank has a single
ultimate corporate parent.
