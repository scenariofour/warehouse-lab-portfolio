# Data quality and resolution contract — M1

Version 1.0, 2026-10-18. AI authored; independent human review PENDING. G0–G4 remain PENDING. This extension authorizes offline research artifacts only; the MVP, normalizer, published data, prior results and source interpretation rules remain unchanged.

Objective: make each discrepancy investigable and decision-relevant without treating an anomaly as a confirmed error. Acceptance criteria were recorded in `.planning/2026-10-18-data-quality-foundation/task_plan.md` before implementation.

## Taxonomy

| Category | Detect / investigate | Decision risk and permitted handling |
|---|---|---|
| IDENTIFIER | Missing/blank key; invalid format only against an authoritative dictionary; order number reused across waves | Wrong grouping or joins. Retain composite wave/order identity; seek business identity definition. Never infer invalidity from an unfamiliar token alone. |
| RECONCILIATION | Aggregate quantities by wave/reference/existing inferred size on both sides, then reconcile; key presence is separate | Wrong eligible-work or service numerator. Keep signed gaps, source populations and literal-size sensitivity; no stockout label. |
| DUPLICATE | Complete original raw field tuple repeated; count occurrences after first | Unit-expanded picks and legitimate customer repeats are possible. Retain all; dedup is a sensitivity only. |
| SKU_SIZE | Empty/non-numeric size or existing inferred half-size mapping; unmatched master reference | Unknown SKU eligibility. Missing stays missing; no imputation or silent remapping. |
| INVENTORY_SNAPSHOT | Payload meaning/UOM, as-of date and alignment unconfirmed | Stock and replenishment/availability claims unsupported. Count encoded cells conditionally; unknown real quantities remain null. |
| LOCATION | Blank ID or left join to Storage_Location with no match | Missing coverage is distinct from nonexistent/invalid physical location. Preserve unmatched records; no invented coordinates. |
| CLASSIFICATION | Published ABC differs from extract-volume 80/95 ABC | Different basis/date may be legitimate. Keep both labels, never overwrite published ABC. |
| EXPERIMENT_CONFOUNDER | SKU-counter inequality across policy pairs; differing coverage, horizon, task mix or physical assumptions | Cannot isolate placement effects. Retain descriptive configurations and require a separately approved controlled protocol. |

Physical scale/floor uncertainty belongs to LOCATION, independent of missing-ID coverage. Categories are diagnostic dimensions, not disjoint populations. A detected issue does not authenticate any hypothesis. Zero findings in a completed profile are evidence of that check's coverage, not proof of general quality.

## Record, measurement and lineage

The normative machine shape is [issue-record.schema.json](issue-record.schema.json); [contract.py](../../scripts/data_quality/contract.py) implements its used schema subset and cross-field rules using Python 3.10+ standard library. Schema additions require corresponding validator support. No runtime dependency installation is required.

One issue record is one stable aggregate investigation question, identified by `DQ-*`, with category, title, detection calculation, affected metrics, severity/confidence, causes, decision/consequences, options, status, review, evidence and remaining uncertainty. Root cause is `UNKNOWN` until supported. All M2 records are `REAL_SOURCE_DERIVED`; synthetic and simulation records are excluded.

Each metric has a unique local ID, affected count (nullable), unit, named population, denominator (nullable), denominator definition, calculation and additivity. Denominators must use the same unit/population as their numerator and cover the full declared extract; null is unknown/not applicable and never zero. Null is used for unmeasured physical inventory, costs or outcomes. Counts cannot be negative or exceed their denominator. L1 policy differences are separate nonadditive diagnostics, never percentages of unique affected stock. Severity is proposed decision priority (HIGH blocks intended decision, MEDIUM needs investigation, LOW informational), not measured loss. Arithmetic confidence describes reproducibility; interpretation confidence describes semantic support, not a probability or confidence interval.

Lineage identifies raw path, SHA-256, columns, role and ordered, disjoint inclusive logical CSV record ranges (header = 1, first record = 2). A range expands to every ordinal between its endpoints. Role `AFFECTED` identifies directly flagged records; `CONTRIBUTING_POPULATION` identifies aggregation/context inputs and must not be counted as affected units. `DEFINITION_EVIDENCE` uses no CSV ordinals for README/notebook meaning. Allocation lineage must name cell columns; a population includes all nonempty named cells in the selected rows. Detailed investigation ledgers preserve key-level values and cell selectors where needed. Row contributions to a gap do not assign particular customer units to failure. Hashes verify source identity, not field truth.

## Normalization, correction and retention

Normalization makes a declared representation consistent: BOM/whitespace handling, numeric spelling, or the existing **inferred** customer mapping `35,45,…,125 → 3.5,4.5,…,12.5`. That mapping is semantically uncertain even though retained as the established normalization rule. Its historical description as a repair is not source approval. Preserve original tokens, mapping rule and source ordinals. M1–M3 do not add or change normalization rules.

A correction changes an asserted value, removes a record, imputes a field or adopts a new source interpretation. It needs identified human/domain approval, versioned derived input, explicit before/after references, rationale, impact review and affected evaluation reruns before use. Original sources remain immutable. Retention preserves a discrepancy or unresolved meaning; it is a valid research outcome. Analytical alternatives such as literal sizes or dedup sensitivities are not successful treatments and must not populate correction before/after fields.

## Handling and review

| State | Meaning / next transition |
|---|---|
| Open | Detected with evidence; investigator/reviewer not yet assigned. Move to Investigating when an actual investigation is underway. |
| Investigating | Competing causes and evidence actively assessed. May return Open or become unresolved pending source evidence. |
| Unresolved — Source Clarification Required | Source meaning/cause cannot be established from available records. Request explicit definitions through owner; no correction. |
| Resolved | Identified human approves evidence that the question is answered or a versioned correction/treatment is valid. Count reductions alone do not qualify. |
| Accepted Limitation | Identified human accepts bounded intended use and documented residual risk. This is not a repaired source or an approved stage gate. |

AI can propose a state, priority, hypothesis or option and execute technical checks. It cannot identify itself as an independent human reviewer, accept a limitation for the owner or approve a correction/gate. Resolved/Accepted Limitation require review state APPROVED, named reviewer and approval evidence. Future reopenings preserve prior versions and decision history. Current review fields remain null/PENDING. Implementation milestones and Git authorization do not approve source interpretations or G0–G4.

## Acceptance and tests

1. Every required field and enum is validated; unknown fields, wrong types (including bool-as-int), missing evidence, synthetic origins, malformed ranges/hashes and duplicate issue/metric IDs fail.
2. Unknown counts stay null; same-unit denominator constraints reject negative or impossible counts. Population/unit definitions require reviewer semantic checking in addition to structural tests.
3. Approved closure/correction needs named reviewer and evidence; corrections also need before/after/approval references. Unapproved transformations fail. Retained uncertainty never gains an invented before/after.
4. Reproducible positive and mutation-negative tests run with `python3 -m unittest discover -s tests -p 'test_dq_contract.py' -v`. Fixtures are contract-only in-memory examples, not real registry rows or synthetic operational data.
5. Preservation checks hash the pre-task inventory, including untracked discovery prerequisites. Prior gate register bytes and all PENDING states must remain unchanged.

Decision DQ-D01: use aggregate issue records plus exact compressed source ordinals and separate investigation tables. This keeps individual observations distinct from interpretation and avoids duplicating source transaction data in public summaries. Remaining blocker: source/domain definitions and independent reviewer assignment are unavailable. See [milestone validation](evidence/m1-validation.json).
