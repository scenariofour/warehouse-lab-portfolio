# Warehouse Lab — project charter

Owner: Project owner (requester); technical document maintainer role unassigned.  
Author: AI assistant; independent human review not performed.  
Version: 0.1.0 · 2026-10-17. Status: DRAFT — PENDING HUMAN REVIEW.  
Review requirements: project owner confirms intended use and success criteria at G0; data and simulation specialists review assumptions at G1–G2. No signature is implied.

## Purpose and evidence

The requester wants to observe and inspect an autonomous warehouse and explore operational efficiency, while grounding demand and layout in the published footwear dataset. The current assignment freezes the MVP and asks for governance, evaluation, and supported corrections. These are documented user needs, **not evidence of an economic warehouse problem**. No customer interviews, measured labor baseline, purchasing decision, cost model, or quantified business benefit is present in the inspected evidence inventory. [Assignment](evidence/2026-10-17/assignment.md), [inspection baseline](evidence/2026-10-17/baseline-inventory.json), [original implementation scope](../README.md).

Proposed intended use: a local, inspectable research/learning sandbox showing how declared robot and inventory assumptions generate outcomes. This intended-use restriction needs G0 confirmation. It does not authorize layout investment, staffing changes, AMR procurement, safety certification, or a claim that one published storage policy improves a real facility. [Data card](DATA_CARD.md), [experiment assessment](EXPERIMENT_CREDIBILITY.md).

## Frozen scope and boundaries

Preserve the existing Vite/TypeScript/Three.js application, 10-AMR default, published input configurations, routing, picking/delivery lifecycle, inspectors, controls, metrics, exports, and deterministic query panel. This assignment permits documentation, offline evaluation, regression tests, and narrowly supported fixes. No dashboard redesign, additional module, new AI capability, optimization policy, replenishment process, or physical robot subsystem is authorized. [Assignment](evidence/2026-10-17/assignment.md), [requirements](REQUIREMENTS.md).

The operational model has no learned predictor or LLM dependency. Risk-management principles are applied to its data, assumptions, calculations, interpretation, and human decisions; this is not a claim of NIST certification. [Analysis implementation](../src/analysis.ts), [methods reference](INTERNAL_PRODUCT_PRACTICES.md).

## Proposed success and guardrails

| Question | Proposed success criterion | Evidence / decision boundary |
|---|---|---|
| Are input records faithfully represented? | Exact publisher hashes and transformation reconciliation; all exclusions and inference rules recorded | EVAL-01 in [evaluation plan](EVALUATION_PLAN.md); semantic truth remains unconfirmed |
| Is the declared abstract model implemented correctly? | Zero stock/accounting/occupancy violations in named tests; independent routing and KPI oracles within numerical tolerances | EVAL-02–07; does not establish physical validity |
| Are results reproducible and attributable? | Same pinned inputs/configuration yield identical event hash; every material claim has an evidence path | EVAL-05/10 |
| Can a storage-policy effect be identified? | Equivalent SKU-level supply and agreed controls before ranking | EVAL-08; currently INCONCLUSIVE |
| Can a real-world decision be supported? | Decision-specific field reference, tolerances, uncertainty assessment and human review | EVAL-09/11; currently INCONCLUSIVE |

No improvement percentage, ROI target, field-accuracy threshold, adoption metric, or delivery deadline has been approved. The owner must choose those only after defining a decision and obtaining a usable empirical baseline. [Gate reviews](GATE_REVIEWS.md).

## Responsibility and approval

The requester is the proposed accountable product owner. A data-domain reviewer, an independent simulation/QA reviewer, and a decision owner must be named before relevant gate decisions. Roles are requested, not staffed. The AI prepares evidence and recommendations; it cannot supply independent review or human approval. [Gate procedure](GATE_REVIEWS.md).

DMAIC control for this assignment: Define this charter → Measure pinned records and invariants → Analyze confounders and defects → Improve only supported defects → Control through versioned tests, evidence hashes and reopened gates after material changes. This is a project-specific application of [ASQ DMAIC](https://asq.org/quality-resources/dmaic), not a completed continuous-improvement program.
