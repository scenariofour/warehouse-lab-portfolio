# M3 — Tableau-ready analytics and design-only exception proposal

Objective: turn the traceable registry into transparent Tableau inputs for data quality overview, issue investigation/resolution, and business/decision impact, without changing the model or publishing a dashboard.

Acceptance criteria recorded before implementation:
- Deterministic UTF-8 CSVs with documented grain, primary key, units, category, status and evidence; source counts, affected metrics and denominator definitions retained.
- Detail facts and issue/decision facts remain at separate grains; no summed cross-issue affected units, no fabricated unique-impact rate and no physical joins that multiply counts.
- Missing physical quantities and all absent approval/before/after fields remain blank/null; no invented successful resolution, money, stockout or causal ranking.
- Independent CSV parsing, keys/FKs, issue metric equality, reconciliation/classification/location/policy totals, schema/public allowlist and byte replay pass. Preserve all baseline files and PENDING gates.
- Tableau A/B/C worksheets, measures, filters, interactions, layout, labels and caveats are specified; public subset restricted and not automatically published.
- Synthetic exception library is design only: mechanisms, fixture requirements, detection expectations, operations implications, industry sources and unsupported assumptions. No new synthetic fixtures or simulation features.

Implementation and validation will be recorded below after verification.

Built: ten internal and four summary-only CSV tables, hashed extract dictionary/manifest, A/B/C Tableau worksheet/filter/action/layout specification, a separate risk/decision register, and seven design-only synthetic exception mechanisms with official industry references and explicit assumption limits. Complete long lineage stays in the registry; extracts use exact compact selectors/evidence links. No workbook or public dashboard is claimed.

Validation: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/data_quality/verify.py M3`; [execution evidence](evidence/m3-validation.json). All 16 contract/registry/CSV test methods pass, including five CSV consumer methods: keys, FKs, row counts, 4,096-character transport limit, registry metric identity, null before/after/reviewer/financial fields, detail and policy ceilings, explicit public headers/allowlist and all 15 generated-file byte comparisons. Registry primary source reconciliation and all 162 baseline file hashes are rechecked. G0–G4 PENDING. No simulation or new synthetic fixture executed/generated.

Decision DQ-D03: keep facts at separate grains, block cross-issue sums, define single-metric shares and label conditional supply explicitly. Use a four-file summary allowlist rather than transaction-level public detail. The business value demonstrated is traceable investigation/decision preparation, not a measured operating improvement.

Remaining limits: Tableau import/rendering/interactions and reviewer comprehension are not tested in an actual workbook; those checks are specified for the next authoring step. All 14 issue causes remain UNKNOWN and reviews PENDING. No actual approved correction exists, so before/after references are blank. Source semantics/stock dates/physical layout, reviewer assignment and public-sharing approval remain outstanding. Synthetic mechanisms are a proposal, not validated exceptions or authorized implementation.
