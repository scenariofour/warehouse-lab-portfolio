# Validation, public release review and limits

Run from repository root: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/data_quality/verify_advanced.py`. Machine evidence is [validation.json](evidence/validation.json); output identities and exact field contracts are in [manifest.json](manifest.json). The automated verdict applies to the pinned offline artifacts, not a Tableau workbook or source truth.

## Independent computational reconciliation

The verifier does not import the generator. It independently parses original CSVs and normalizes numeric tokens using Decimal, loads original records into SQLite, and aggregates current/literal/dedup populations separately. It checks every union key, all per-key quantities and source-presence counts, wave/order groups and their repeat/missing/zero counts, each source/location group, unknown-master overlap, ABC ranks/classes/cumulative totals, all six policy-counter pairs and each policy's existing conditional bound. It checks exact source hashes and the registry's issue/source role counts. This is a separate computational implementation by the same AI assistant, **not independent human validation**.

Three local source-lookup samples cover a current positive gap, a literal-only key and a repeated-customer key. For each sample and each interpretation, independently selected SQL source ordinals and quantities must match the lookup's exact compressed source ranges. Header=record 1; all selections are contributing populations, not identified failed units. The public file contains no long raw row lists.

The verifier loads every public CSV using declared types into `out_<table>` SQLite tables and executes [consumer_checks.sql](consumer_checks.sql). Its 36 checks assert concrete counts/totals usable for Tableau acceptance, including both sides of dedup discrepancies. See `consumer_checks` in the JSON for actual/expected values. These are separate from the full key/subgroup equality checks; grand-total agreement alone would miss compensating errors.

It replays the exporter in an empty temporary directory and compares 16 generated files byte-for-byte (14 CSVs, manifest and dictionary). M1–M3's 16 existing DQ test methods run without invoking their report writer or altering historical evidence. Five deliberate in-memory mutations must be rejected: sensitive extra header, duplicate issue key, spreadsheet formula, wrong quantity and false protocol approval. These mutations are validation inputs only, not synthetic operational CSVs or inventory scenarios.

## Evidence and population checks

| Population / calculation | Expected |
|---|---:|
| Advanced public tables / total rows | 14 / 202158 |
| Reconciliation union across interpretations | 148887 keys |
| Current requested / picking / matched | 228195 / 215192 / 215192 units |
| Current positive gap / excess | 13003 / 0 units |
| Current positive-gap keys | 5242 |
| Literal-size matched | 149514 units |
| Customer dedup demand / matched / gap / excess | 215460 / 202475 / 12985 / 12717 units |
| Current wave/order groups / source customer records | 39858 / 122370 |
| Missing-coordinate picking | 23609 of 215192 units, 22 IDs |
| Raw / retained / excluded cells, all policy files | 167634 / 165024 / 2610 cells (alternative files, not one warehouse inventory) |
| Unknown-master allocation cells | 6734 (can overlap coordinate exclusions) |
| ABC references / label disagreements | 208 / 96 |
| Failed pair equivalence controls | 6 of 6 pairs |
| Human approvals / source corrections | 0 / 0 |

Location denominators are per source; policy quantities are alternative configurations. Current/literal/dedup are alternative calculations. Issue categories overlap. None may be summed into an overall affected-unit count or combined service rate. Empty sizes remain unknown; current keys with zero quantity retain presence through source-record counts.

## Public release technical review

Every advanced public field is enumerated independently in the consumer header allowlist and described in the generated dictionary. Only the manifest's 14 CSVs plus the three reused M3 public summary sources are intended for the new workbook. Review findings:

- Published, anonymized research source under CC BY 4.0; attribution and transformation notice provided. No newly acquired private source or confidential operational performance is added.
- Customer codes, operator fields, original order numbers, original wave/reference/location IDs, creation timestamps, coordinates and source ordinal lists are absent from new public CSVs. Stable domain-separated SHA-256 pseudonyms support cross-table investigation; observed wave/reference/order/location domains are collision-checked. Hashing is pseudonymization, not irreversible anonymization. Small exact groups remain research observations; no population privacy guarantee is asserted.
- Exact size tokens are numeric/missing research measurements. Complete original tuple fields are used locally for duplicate detection but are not exported. The lookup prints source keys/ranges without personnel/customer fields and is not a public data source.
- Public text is bounded, has no formula-leading cells, and comes from controlled metadata or numeric tokens. No arbitrary source free text, credentials, emails, local home paths or private reviewer identities are added. Public lineage exposes pinned filenames/hashes/roles, not personnel records.
- Unknown physical stock/distance, approvals, reviewer identity, financial outcomes and actual operational failure measures are not invented. Workflow status remains pending/unresolved. Alternative interpretation and existing assumption labels are visible.

Technical public-field review passes when verifier reports PASS; independent human/domain and Tableau release reviews remain pending. The user authorized preparation and Git push. This task does not publish a workbook or treat a technical scan as human approval. Public workbook data is accessible beyond visible sheets; do not upload additional internal files to obtain drill-down.

## Preservation and scope

[Baseline inventory](evidence/baseline-preservation.json) pins 210 pre-existing files, including tracked foundation/application/data/results/gates and untracked Discovery prerequisites. All must remain byte-identical. The planning skill temporarily selected this task, then its shared selector was restored to original bytes; only this task's new planning directory is committed. No existing source/production normalizer/simulator/MVP output, test, gate record or historical validation record is changed. No operational simulation or synthetic inventory scenario runs. No Tableau publishing/authentication/edit API is called.

The pre-existing Discovery scripts/reports/evidence stay untracked and unmodified. M4 compares their stated headline findings but does not depend on them at runtime; raw, M2 and M3 are the reproducible committed inputs. Discovery's historical repository-inventory replay is context-dependent and is not reported as a fresh PASS after extension files are tracked.

## Remaining limits and manual acceptance

The published Dashboard01 URL could not be fetched by the web tool; its user-reported 14-issue summary was used as context. No workbook contents, existing calculations or actions were verified. This deliverable is ready for construction, with Tableau import, render, Public multi-source assembly capabilities, interaction scope, keyboard usability and reviewer comprehension **NOT TESTED**. Follow the handoff's manual checks; record results before claiming the studio is implemented.

Source truth, size codebook, order business identity, event expansion, cancellations/status/timing, stock UOM/date/receipts and physical scale/floor connectivity remain unresolved. Data is a nonrandom published/anonymized extract, not a representative annual operating sample. Source hashes prove byte identity only. There are no measured cost savings, confirmed warehouse failures or causal policy improvements. Experimental readiness is withheld until the documented controls and human protocol review are satisfied.

If future work changes source interpretation, inventory balance or production inputs, it needs separate approval, a versioned derived dataset and affected evaluation reruns. This handoff supplies no such correction or approval.
