# Internal product, quality and AI-risk practices

Owner: project owner; product/QA reviewers unassigned. Author: AI assistant.  
Version: 0.2.0 · 2026-10-17. Status: DRAFT — PENDING HUMAN REVIEW.  
Review requirements: human owner ratifies practice adoption and role assignments. These are internal work practices, not new application features.

The confirmed hierarchy is operations improvement research (A), internal AI PM/TPM governance (C), and analytics/OR/simulation methodology (B). These practices govern the evidence and decisions without adding product features. A well-supported negative or inconclusive result may satisfy the research objective. [Charter](PROJECT_CHARTER.md), [D-01](RISK_AND_DECISION_LOG.md#d-01--owner-confirmed-intended-use-direction).

## Working vocabulary for this project

| Concept | Concrete application and boundary |
|---|---|
| PRD | PROJECT_CHARTER + REQUIREMENTS form a compact scope/need/acceptance record. User intent is evidenced; a business pain/ROI baseline is not. |
| Acceptance criteria | R-01–13 are proposed testable predicates. Their technical execution can pass before a human accepts scope or operational adequacy. |
| KPIs | Throughput, latency, travel and utilization must keep the group/unit/time definitions in REQUIREMENTS. Source-group throughput is not automatically customer throughput. |
| Guardrail metrics | Zero negative stock, duplicate deliveries, reservation conflicts and fabricated approvals; report failures and exclusions beside performance. A fast invalid run cannot be a success. |
| Data contract | Pin manifest/version, schemas, inference rules, record lineage and exclusions. Invalid imports must preserve originals. DATA_CARD distinguishes source values from assumptions. |
| Provenance | E-02 links raw hashes to normalized arrays. E-04/E-05 bind code, inputs, parameters and results. Hash identity does not prove field semantics. |
| Evals | Each EVAL has a claim, reference, procedure, metric/threshold, result, limitation and pending reviewer. An oracle must be appropriate to the claim. |
| Golden datasets | Raw snapshots are regression/provenance references. Scarcity and head-on fixtures test logic. Neither is labeled evidence of real robot performance. |
| Baselines | Capture prior source hashes/reports before correction. Compare default outcomes before/after a bug fix; do not invent a factory baseline from a simulated run. |
| Verification | Check the program against its declared rules: conservation, A*, replay and KPI equations. Current technical evidence supports this bounded claim. |
| Validation | Check whether those rules adequately represent reality for an agreed use. Stock/scale/floor/service references are missing for operational use. |
| Reproducibility | Same inputs/config/code should recreate the event hash. Seed aliases are not independent samples; environment and input fingerprints belong with results. |
| Sensitivity analysis | E-04 varies existing parameters locally and records outcomes. Chosen +/-20% settings are diagnostics, not measured parameter distributions or a robustness certificate. |
| Confounders | Different SKU supply, coverage and fulfilled tasks contaminate policy contrasts. EXPERIMENT_CREDIBILITY blocks causal ranking until controls are approved. |
| Risk management | RISK_AND_DECISION_LOG ties severity, impact, confidence, evidence and treatment to a responsible role and gate. Unknown facts are not assigned invented probabilities. |
| Decision records | Preserve context, alternatives, consequences and human disposition. D-01 records owner-confirmed intended-use direction; D-02–05 remain proposals. All formal gates remain pending; observed legacy implementation is not retrospective approval. |
| Human approval | The AI may prepare evidence/recommend outcomes. Only an identified human can record a gate decision for a specified use and evidence snapshot. |
| Stage gates | G0 purpose → G1 data → G2 model → G3 experiment → G4 decision. PENDING is review lifecycle; the three decided outcomes are APPROVED, CONDITIONALLY APPROVED and BLOCKED. |

Project evidence and operational definitions: [requirements](REQUIREMENTS.md), [data card](DATA_CARD.md), [model card](MODEL_CARD.md), [evaluation plan](EVALUATION_PLAN.md), [gates](GATE_REVIEWS.md). This vocabulary does not create a trained-AI subsystem; current queries are deterministic code in [analysis.ts](../src/analysis.ts).

## Methodology integrated into the work

The following is **our application** of public methods, not an external certification or a statement that every framework requirement is met.

| Method | Warehouse Lab practice |
|---|---|
| DMAIC | Define the bounded purpose; measure source/implementation properties; analyze stock/geometry/confounding gaps; improve reproduced defects only; control changes through hashes, regressions, risk review and gate reopening. |
| NIST GOVERN | Keep role ownership, scope, risk/decision history and human approval separate from AI authorship. |
| NIST MAP | State intended use, affected decisions, data origins and known limits before interpreting KPIs. |
| NIST MEASURE | Use explicit evaluation contracts; record missing measurable references; obtain independent/domain review rather than calling self-tests validation. |
| NIST MANAGE | Prioritize source-preservation/routing defects, restrict unsupported uses, and block decision claims that depend on unresolved risks. |
| Simulation V&V | Separate code verification from adequacy for intended use; preserve inputs, coordinate/units assumptions and result credibility evidence. |
| Experimental design | Agree estimand and controlled factors before inference; use justified workload blocks and replication, not unequal published stock or aliased seeds. |

Authoritative references consulted 2026-10-17:

- [ASQ, DMAIC](https://asq.org/quality-resources/dmaic): improvement phases for existing processes. Its application above is specific to this review, not evidence of measured process gains.
- [NIST AI RMF 1.0, NIST AI 100-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf), sections5.1–5.4 and MEASURE1.1/1.3/2.1/2.5: voluntary risk functions, documented measurements/limits and independent expertise. These principles are adapted to the deterministic sandbox; formal compliance is not asserted.
- [NASA-STD-7009B, 2024-03-05](https://standards.nasa.gov/sites/default/files/standards/NASA/B/1/NASA-STD-7009B-Final-3-5-2024.pdf), sections4.2.3/4.2.5/4.3.5/4.3.8: verification, validation, sensitivity and results reporting inform the distinction used here; no NASA approval or standards conformance is claimed.
- [NIST experimental-design objectives](https://www.itl.nist.gov/div898/handbook/pri/section3/pri33.htm) and [blocking](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm): justify a design by its question and nuisance factors. Our proposed protocol is not yet approved or executed.

## Applicable now versus hypothetical future AI

**Now:** data contracts and provenance, deterministic arithmetic/query tests, numerical oracles, source-to-claim traceability, uncertainty, risk ownership, review and intended-use restrictions.

**Only if future scope is separately authorized:** model training/validation/test splits for learned predictions, label quality and leakage checks, drift monitoring, model calibration, LLM factuality and prompt-injection evaluations, RAG retrieval metrics, model/provider cost/latency and tool-permission controls. None is a feature request or current deliverable. Do not create ML accuracy claims, training artifacts or AI modules for this frozen MVP. [Current assignment](evidence/2026-10-17/assignment.md).
