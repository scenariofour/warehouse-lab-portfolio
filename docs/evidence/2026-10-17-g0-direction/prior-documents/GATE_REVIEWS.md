# Stage gates and human review register

Owner: project owner. Author: AI assistant.  
Version: 0.1.0 · 2026-10-17. Status: DRAFT — PENDING HUMAN REVIEW.  
Review requirements: owner ratifies this procedure and appoints human data/QA/OR reviewers. No gate has been reviewed or signed by a human in this evidence package.

## Outcome semantics and approval procedure

A completed human review may record exactly one outcome:

- **APPROVED:** all criteria for the expressly named use are met; evidence and residual risks accepted by the responsible human.
- **CONDITIONALLY APPROVED:** only a bounded use is permitted; each condition has an owner, closure evidence and a due review date/event. A missing material validity prerequisite cannot be waived while retaining the corresponding operational claim.
- **BLOCKED:** unresolved blockers prevent progression for the requested use; record corrective work and resubmission evidence.

**PENDING is a review lifecycle state, not a fourth approval outcome.** Every current decision is null. AI recommendations are separate nonbinding advice and cannot transition a gate. The machine-readable [gate register](GATE_REVIEWS.json) preserves this separation.

Human procedure:

1. Owner names reviewers, intended use, evidence versions/hashes and criteria. Prerequisite gates must be decided for that same use; otherwise review may be prepared but progression is not authorized.
2. An independent reviewer examines raw/derived evidence, reproduces critical checks and challenges limits. The current AI author cannot count as independent review. Resolve reviewer conflicts explicitly; do not silently collapse business and technical criteria.
3. Responsible human records identity, date, outcome, rationale, evidence snapshot, permitted use, conditions/blockers and residual-risk acceptance. The owner confirms progression; technical reviewer concurrence is required for G1–G3, and the decision owner for G4. These appointments/confirmations are currently absent.
4. Keep review history; never backfill an unsigned approval, overwrite an accepted record or carry an approval across changed evidence. Material data/model/metric/use changes return affected gates to PENDING, with the prior decision preserved as superseded.

## Current register — recommendations only

| Gate | Review state | Human decision / reviewer / date | AI recommendation | Boundary / unresolved prerequisite |
|---|---|---|---|---|
| G0 | PENDING | None / unassigned / none | CONDITIONALLY APPROVED, if owner confirms sandbox-only purpose | Business success/decision and roles not ratified |
| G1 | PENDING | None / unassigned / none | CONDITIONALLY APPROVED for pinned sandbox inputs only | Stock, units, floors and order semantics unresolved; operational data readiness remains blocked |
| G2 | PENDING | None / unassigned / none | BLOCKED for operational model readiness | Software evidence available; independent model validation, physical references and accepted use envelope absent |
| G3 | PENDING | None / unassigned / none | BLOCKED for causal policy comparison | SKU supply and geometry coverage controls fail; no approved experimental protocol |
| G4 | PENDING | None / unassigned / none | BLOCKED for business/operational decisions | No valid treatment comparison, empirical baseline, cost model or risk acceptance |

A recommendation of conditional approval is **not permission to proceed** and does not satisfy a prerequisite. Existing implementation/evaluation work was authorized by the current assignment, not by these pending gates. [Assignment](evidence/2026-10-17/assignment.md).

## G0 — problem definition

- **Purpose:** agree what question this model can legitimately answer and who decides.
- **Required inputs:** user brief; inspected implementation; evidence of intended users and decision; business baseline if business benefit is claimed.
- **Deliverables:** approved PROJECT_CHARTER and REQUIREMENTS; named owners/reviewers; explicit non-goals and claim boundary.
- **Evaluation methods:** owner walkthrough, requirement-to-evaluation trace review, gap analysis against supplied business evidence.
- **Measurable exit criteria:** one named accountable owner; every requirement has a criterion/evaluation; no unstated operational/ROI target; one explicit intended-use statement and escalation boundary. For a business use, obtain an observed baseline and a decision loss/benefit definition before claiming value.
- **Evidence:** E-11 assignment, E-01 inspected baseline, charter, requirements, claim register; no interview or business-value evidence is supplied.
- **Responsible reviewer:** project owner; independent product/QA reviewer to be appointed.
- **Blocking conditions:** unspecified decision/user or unsupported benefit presented as fact; no accountable reviewer.
- **Approval procedure:** follow the common procedure; owner must expressly accept/revise bounded intended use. No G0 decision is recorded.

## G1 — data readiness

- **Purpose:** establish attributable inputs and an accepted interpretation for the intended use.
- **Required inputs:** G0 decision, publisher manifest/license/raw files, actual schemas, conversion code, data and assumption cards.
- **Deliverables:** signed DATA_CARD, versioned raw/normalized hashes, exception ledger, accepted stock/size/unit/floor/order and snapshot-time definitions or a restricted-use condition.
- **Evaluation methods:** SHA checks, complete record reconciliation, joins/missingness/duplicates review, source-domain interpretation review, rejected-import regressions.
- **Measurable exit criteria:**21/21 retained file hashes match; 100% normalized records/lineage reconcile under approved rules; zero unexplained dropped rows/cells; all known missing geometry/product/size cases enumerated; source originals not overwritten on rejected import. Operational use additionally needs authoritative quantity, scale/topology and inventory timing evidence, not just a disclaimer.
- **Evidence:** E-02, E-03/E-07, DATA_CARD, data-audit and C-01.
- **Responsible reviewer:** data steward + warehouse/WMS domain reviewer; owner accepts any bounded conditions.
- **Blocking conditions:** hash/reconciliation mismatch; unexplained source mutation; unsupported semantics required by a claimed use; missing attribution.
- **Approval procedure:** verify G0 scope, review exact input hashes and documented exclusions, then human-record an outcome. Current technical checks support only a proposed sandbox condition; operational readiness is not established.

## G2 — model verification and validation

- **Purpose:** distinguish a correct program from a credible model for the accepted use.
- **Required inputs:** G0/G1 decisions, MODEL_CARD, algorithm/contracts, complete relevant event logs, unit/browser/build evidence, calibration/validation references for physical claims.
- **Deliverables:** independent verification/validation review, accepted numerical and field criteria, tested envelope, deviations and residual limitations.
- **Evaluation methods:** BFS/KPI oracles; conservation, reservation and completion checks; replay; focused edge cases; sensitivity/time-step diagnostics; comparison to appropriate held-out empirical reference when physical predictions are intended.
- **Measurable exit criteria:**zero critical technical invariant violations in the named suite; exact replay; all KPI numerical errors <= proposed 1e-5; no uncaught browser failures/build errors; reviewer accepts representativeness and limitations. Physical thresholds must be set from observed measurement uncertainty and decision requirements before evaluation; none are invented here.
- **Evidence:** E-04–E-09, EVAL-02–07/09/11–13, correction-impact report.
- **Responsible reviewer:** independent simulation/QA reviewer + warehouse-domain reviewer; neither role is filled by the AI author.
- **Blocking conditions:** failing invariants; unsupported interpolation from technical tests to physical validity; missing required empirical reference; unknown service/floor feasibility; unaccepted time-step sensitivity.
- **Approval procedure:** human separately records verification result and validation adequacy for the named use, then a single gate outcome. Current operational model readiness is recommended BLOCKED.

## G3 — experiment readiness

- **Purpose:** ensure a proposed contrast identifies its intended effect.
- **Required inputs:** applicable G0–G2 decisions; estimand/hypothesis; inventory/demand/geometry equivalence checks; planned treatment inputs, parameters, workload blocks and analysis.
- **Deliverables:** pre-registered protocol, treatment/input hashes, confounder/exclusion ledger, run matrix, failure reporting and practical-effect/uncertainty plan.
- **Evaluation methods:** exact SKU-counter comparison, controlled input checks, paired-block rationale, seed analysis and independent experimental-design review.
- **Measurable exit criteria:**identical declared SKU quantities and unit demand across treatments; no unaccounted geometry exclusions; same non-treatment parameters/horizon rules; every planned run/failure retained. Any restriction/common-inventory remapping must be expressly labeled, justified and approved. Replication and effect thresholds require a statistical/decision rationale, not arbitrary seeds or a made-up sample size.
- **Evidence:** E-02/E-04/E-05, EXPERIMENT_CREDIBILITY and EVAL-08.
- **Responsible reviewer:** independent OR/experimental-design reviewer; data owner confirms treatments.
- **Blocking conditions:**current unequal stock/supported task mixes, changed demand without blocking rationale, inconsistent horizons, seed aliases used as independent replications, post-hoc selective reporting.
- **Approval procedure:** review/freeze protocol before a causal run; human records scope and outcome. Existing descriptive runs do not satisfy this gate.

## G4 — decision readiness

- **Purpose:** permit a specific consequential conclusion only when evidence and uncertainty support it.
- **Required inputs:** applicable G0–G3 decisions; complete results including failures; empirical baseline, costs and effect size relevant to the decision; model/experiment uncertainty and residual-risk review.
- **Deliverables:** decision brief with alternatives, claim/evidence map, sensitivity limits, recommendation, human acceptance/rejection and follow-up conditions.
- **Evaluation methods:** review decision relevance, external validity, confounding, practical significance, error costs and credible alternatives. Test a conclusion against unresolved risks rather than merely checking that a number exists.
- **Measurable exit criteria:**all critical decision claims supported by valid references;zero unresolved Critical findings affecting the decision; every material uncertainty has an accepted treatment/limit; named human decision owner signs for the exact use. No numerical business threshold is defensible until baseline/cost evidence exists.
- **Evidence:** final review, risk/decision log, claim register, EVAL-08/09/11 and any later field/business evidence. The latter is absent now.
- **Responsible reviewer:** business/operational decision owner with independent technical/domain concurrence.
- **Blocking conditions:**causal ranking from current policies, physical performance or ROI claims without validation, unresolved stock/scale/floor identity, no human residual-risk acceptance.
- **Approval procedure:** human records the particular decision, evidence snapshot, alternatives, conditions and residual-risk acceptance. Current G4 remains PENDING with AI recommendation BLOCKED.
