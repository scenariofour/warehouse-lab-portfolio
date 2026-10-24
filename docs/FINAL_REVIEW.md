# Final internal quality review — 2026-10-17

Owner: project owner. Author/executor: AI assistant.  
Version: 0.1.0. Status: DRAFT — PENDING HUMAN REVIEW.  
Review requirements: independent human data/simulation/OR review and owner gate decisions. This is an evidence-backed self-assessment; it is not independent sign-off or a completed governance process.

## Current maturity

Warehouse Lab is a technically verified **abstract research sandbox within the tested envelope**, with unresolved operational-model and experimental validity. The frozen MVP has been preserved. There is no evidential basis yet for a real warehouse investment, safety, productivity, policy-ranking or ROI decision. [Evaluation results](EVALUATION_PLAN.md), [risk log](RISK_AND_DECISION_LOG.md), [gate register](GATE_REVIEWS.md).

## Verified strengths

- All 21 publisher raw hashes match; all normalized coordinates, products, four allocation arrays and 122,370 customer rows reconcile under the **existing assumptions**. Lineage is complete; no production record was fabricated or raw file changed. [E-02](evidence/2026-10-17/data-evaluation.json).
- Nine TypeScript tests and five Python import fixtures pass. Four default 120-group scenarios reach a terminal outcome; checked stock/accounting/reservation invariants pass. Thirty-nine A* paths match independent BFS on the declared grid. [E-04](evidence/2026-10-17/model-evaluation.json), [E-05](evidence/2026-10-17/scenarios.json), [E-06](evidence/2026-10-17/after-unit-tests.log), [E-07](evidence/2026-10-17/after-import-regression.log).
- Independent event/coordinate/service-time KPI oracles reconcile across 14 baseline/replay/diagnostic executions; the largest numerical discrepancy is below 4.1e-6 in corresponding modeled units. Full-default event replay is exact. These are verification findings, not factory accuracy measurements. [E-04](evidence/2026-10-17/model-evaluation.json).
- Existing browser acceptance workflow and production build pass; the Three.js bundle-size warning remains visible. UI, scene and simulation-calculation sources are unchanged; the only runtime-source correction is the routing endpoint guard. [Browser evidence](evidence/2026-10-17/browser-tests.log), [build evidence](evidence/2026-10-17/build.log), [correction impact](evidence/2026-10-17/correction-impact.json).

## Corrective work completed within this assignment

C-01 prevents a rejected ZIP from replacing preserved raw bytes and stages downloaded candidates before hash acceptance. C-02 rejects blocked/out-of-grid routing endpoints, including the empty-path shortcut. Both have captured pre-fix failing regressions and post-fix passing tests. C-03 replaces a hardcoded scenario-report date with real execution metadata and input/code hashes. Raw data, normalized JSON and default numerical scenario outcomes are unchanged. [Corrections and remaining limits](RISK_AND_DECISION_LOG.md), [reviewable diff](evidence/2026-10-17/corrections.diff), [impact evidence](evidence/2026-10-17/correction-impact.json).

## Critical issues and evidence gaps

1. **Stock:** the source's quantity label conflicts with size-like payloads; one carton per cell is unconfirmed, and snapshot date alignment is unknown. No warehouse stock or service-failure claim is validated. F-02, [data card](DATA_CARD.md).
2. **Geometry/service:** 0.1 horizontal scale, floor-to-tier abstraction and timed shelf service lack surveyed/physical references. No real distance, capacity, inter-floor travel or AMR safety claim is validated. F-03, [model card](MODEL_CARD.md).
3. **Comparisons:** equal 41,256-carton totals conceal different SKU quantities. For the same 922 demanded units, supply upper bounds are 825/807/916/916; all six policy pairs fail inventory equivalence. Current policy-effect comparisons are **INCONCLUSIVE**, not a ranking. F-04, [experiment assessment](EXPERIMENT_CREDIBILITY.md).
4. **Decision meaning:** 4,024 order numbers span waves; engine throughput counts wave/order groups. Business success criteria, baseline economics, deployment tolerances and an empirical validation dataset are not supplied. F-01/F-05/F-10, [charter](PROJECT_CHARTER.md).

Other open risks include duplicate/missing-record semantics, source-prefix bias, step sensitivity, bounded event retention and the use of aliased priority seeds as if they were random replications. All are recorded with severity, confidence, consequence and responsible role in [the risk log](RISK_AND_DECISION_LOG.md). No human reviewer roles are staffed in this package.

## Recommended gate status — not actual approval

| Gate | Actual review state / human decision | AI recommendation |
|---|---|---|
| G0 problem | PENDING / none | CONDITIONALLY APPROVED only if the owner confirms bounded sandbox intent and ownership |
| G1 data | PENDING / none | CONDITIONALLY APPROVED for pinned, assumption-labeled sandbox inputs; operational readiness blocked |
| G2 model | PENDING / none | BLOCKED for operational readiness pending independent/domain validation |
| G3 experiment | PENDING / none | BLOCKED for causal storage-policy comparison |
| G4 decision | PENDING / none | BLOCKED for operational/business conclusions |

Only identified humans may record the three formal outcomes for a specified use and evidence revision. The AI has not signed off on its own work. [Detailed criteria/procedure](GATE_REVIEWS.md), [machine-readable pending register](GATE_REVIEWS.json).

## Currently authorized scope and approvals needed

The current user assignment authorizes inspection, documentation, offline evaluation, regressions and safe supported correctness fixes; those are the boundaries used here. It does not grant a new product feature scope or a gate approval. [Assignment](evidence/2026-10-17/assignment.md).

Next human decisions:

1. Confirm sandbox-only intended use or define a specific operational/business decision; name the accountable owner and independent data/QA/OR reviewers (D-01, G0).
2. Obtain source-domain clarification of payload quantities/sizes, inventory timing, geometry units/floors and customer order/wave aggregation. Approve any interpretation change **before** changing normalized inputs or calculations (D-02/D-04, G1–G2).
3. Decide whether to authorize a separately labeled common-inventory experiment and approve its estimand, controls, workload blocks and analysis plan. This has not been implemented as a product feature (D-03, G3).
4. Establish empirical references, practical error/effect thresholds and cost/risk criteria before operational claims. Stock/scale/floor sensitivity cannot be certified from the current data (D-05, G2/G4).

The documentation and technical checks are ready for review. Governance remains incomplete until the required evidence, independent review and actual human decisions exist. [Claim register](CLAIM_REGISTER.json), [reproduction/evidence index](EVIDENCE_INDEX.md).
