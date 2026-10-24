# Audit and analytical model contract

M4-B, 2026-10-18. The existing branch is `codex/data-quality-foundation`, remote `origin` (`scenariofour/warehouse-lab`). The user authorizes new research extracts, documentation, atomic commits and push on that branch. Raw files, production inputs, Three.js application, simulator, results, gate records and pre-existing Discovery work are protected by `evidence/baseline-preservation.json`.

## Available foundation

| Layer | Existing artifacts / validated definitions | M4-B reuse / missing support |
|---|---|---|
| Source | 21 hash-pinned files; nine analytical CSVs; README dictionary and notebook; source DOI and CC BY 4.0 attribution | Authenticate all source bytes. README payload quantity wording conflicts with adopted size interpretation; retain uncertainty. |
| Production/M1 | `docs/DATA_CARD.md`, `scripts/prepare_data.py`, DQ contract/schema and validator | Use the explicit M2 `size()` function, not a second production transformation. Do not import production code with write side effects. |
| M2 | 14 issue records; `reconciliation.csv` (112,442 union keys), `classification.csv` (208 demanded references), `policy_skus.csv` (16,819 counters), `policy_pairs.csv` (6 pairs), excluded/unknown cells and 12 profile checks | Reuse validated aggregates and exact raw lineage. Keep counts by unit/population. All causes UNKNOWN, human reviews PENDING. |
| M3 | 10 internal / 4 public CSVs; grain/key/hash manifest; public issues, metrics, source counts and decision impacts | Reuse summary files directly, without copying them. Internal positive-gap reconciliation contains only 5,242 keys; it cannot support full matched denominators. New public detail needs explicit field minimization. |
| Discovery 01 | Scripts, summary, verification, wave/SKU reconciliation, wave/order groups, ABC, locations, supply, daily/monthly profiles, geometry proxies | Inspected as pre-existing untracked work, excluded from new commits. Independently compare stated key totals. Do not add runtime dependence on untracked artifacts or rerun its repository-wide inventory replay after new tracked files are added. No old evidence is rewritten. |
| Published workbook | User-reported Dashboard01 summarizes 14 issues | URL fetch failed during audit; appearance, calculations and actions were not inspected. Preserve it. Build a separate workbook through this handoff. |

Discovery's `verify_discovery.py` recomputes source metrics but its full replay fingerprints all currently tracked files. Adding M1–M4 changes that inventory; an old verification PASS is historical evidence, not a fresh M4 test. The self-contained M4 verifier reads pinned sources and checks key-level quantities instead. Existing M1–M3 test suites are also run without rewriting their historical reports.

## New tables and why they exist

| Extract | Exact grain / primary key | Purpose |
|---|---|---|
| reconciliation | Union wave/reference/size key across current, literal and customer-dedup interpretations / `reconciliation_id` (also wave_id, reference_id, size_key unique) | Full two-sided investigation. Alternative customer quantities are side-by-side columns; picking quantities stay single. |
| reconciliation_summary | One interpretation / `interpretation` | Auditable full-scope totals and denominators; never sum alternatives. |
| exception_pareto | Positive current-gap group within dimension wave or reference / `(dimension, member_id)` | Rank gap concentration on a fixed full-gap denominator; dimensions overlap. |
| order_groups | Current source wave/order group / `order_group_id` | Investigate demand identity, repeats and missing sizes without falsely allocating picks to orders. |
| location_coverage | Source scope and stripped location / `(source_scope, location_id)` | Picking coverage and allocation cell exclusions, with independent unit/denominator by source. |
| abc_comparison | Demanded reference / `reference_id` | Published versus derived ABC plus demand rank/concentration. |
| normalization_tokens | Source, field and exact original size token / `token_id` | Actual raw spelling, current normalization and literal interpretation, with row/unit populations. |
| transformation_rules | Declared transformation/retention/scenario rule / `rule_id` | Semantic approval boundaries and affected calculations. |
| policy_pairs | One unordered published policy pair / `policy_pair_id` | Counter inequality and L1 diagnostics; reuse M2 counts. |
| policy_supply | Published policy / `policy` | Existing M3 conditional one-snapshot arithmetic, not measured stock or simulated outcome. |
| experiment_controls | One control at global or pair scope / `control_id` | Failed, unverified, unmeasured and unapproved controls separately; no invented readiness score. |
| decision_evidence | One issue's decision question / `issue_id` | KPI/assumption risk, mechanism, alternatives, next evidence and recommendation. |
| issue_evidence | One issue-to-source lineage role / `issue_source_id` | Exact evidence relationship and role; selected records are not automatically affected records. |
| profile_checks | Source/field/check / `(source_id, field, check)` | Completed checks including zero findings. No general-quality score inferred. |

Generated `DATA_DICTIONARY.md` and `manifest.json` enumerate every column, type, definition, nullability and allowed aggregation. No new inventory scenarios are generated. Literal customer sizes and exact customer deduplication are competing record interpretations of the existing extract. The latter compares complete original tuples, including omitted private fields, and is never adopted as cleaning.

## Model and evidence boundaries

Use one independent Tableau source per extract. Do not physically join issue, metric, reconciliation, location, order or policy facts. Optional relationships from a unique dimension to a fact require cardinality verification; no such relationship is required for the web-first design. A selected wave/ref/size never uniquely identifies an order, pick location or issue. Picks have no order number: order fulfillment is unmeasured.

Evidence classes: `PUBLISHED_SOURCE_OBSERVATION` for tokens/labels and profile populations; `SOURCE_DERIVED` for reproducible joins/aggregates; `EXISTING_INFERRED_NORMALIZATION` for current sizes; `ANALYTICAL_SENSITIVITY` for literal/dedup branches; `CONDITIONAL_ASSUMPTION` for stock arithmetic; `AI_PROPOSED_REQUIRES_HUMAN_REVIEW` for business interpretation. A row can combine published fields and derived measures; the dictionary identifies both. None authenticates source truth.

All identifiers are string dimensions; sizes use `MISSING` for the unresolved empty source size, not size zero. Original empty tokens remain CSV blank in the token table. Numeric blanks mean unknown, never zero. Quantity fields use integer counts. Current/literal/dedup quantities share one union-key table; select one customer quantity before computing row-level overlap/gap. Presence comes from record counts, including zero-quantity keys. `SUM(MAX(D-P,0))` is a sum of row-level differences; `MAX(SUM(D)-SUM(P),0)` would hide opposing gaps.

## Acceptance criteria recorded before generation

1. Full current totals reconcile to 228,195 requested / 215,192 picking / 215,192 matched / 13,003 positive gap / zero excess units. Every union key agrees with independently aggregated raw records. Current positive-gap keys = 5,242.
2. Literal matched = 149,514; customer dedup matched = 202,475, positive gap = 12,985, excess = 12,717. Alternate totals are scenario-labeled and kept out of current summary measures.
3. All customer records belong to one wave/order group; current groups = 39,858. No measured picking completion per order is invented.
4. Picking location totals = 215,192, unmapped = 23,609 across 22 IDs. For every allocation source, raw cells = retained + excluded; all retained totals = 41,256; exclusions = 0 / 882 / 864 / 864. Unknown-master cells are tracked independently and can overlap exclusions.
5. ABC totals = 208 references / 228,195 units / 96 disagreements; deterministic tie order and cumulative-before 80/95 thresholds match M2. Six policy comparisons fail SKU equivalence even though retained totals agree.
6. Every public CSV has an explicit field schema and unique primary key, no original human/customer/operator/order identifiers, timestamps, coordinates, arbitrary source text or spreadsheet formula cells. Pseudonyms are collision-checked and consistent across tables. Public source evidence uses filenames/hash/roles, not personnel rows. Source approval, reviewer, savings and source-correction fields remain absent or explicitly unknown.
7. Independently written SQLite checks from raw CSVs validate per-key and subgroup outputs; deterministic replay agrees byte-for-byte. Negative checks reject schema drift, duplicate keys, false controls, wrong quantities and unsafe cells. All 210 pre-existing files in the preservation inventory remain byte-identical; G0–G4 remain PENDING.
8. Each worksheet has a question, grain, denominator, filters, insight and limitation. Web baseline uses visible controls and tabs; unsupported advanced action authoring is flagged. Manual Tableau import/render and independent human comprehension review remain explicit pending acceptance, not claimed PASS.
