# Warehouse Lab — project charter

Owner: Project owner (requester), accountable for project direction and gate progression; document maintainer role unassigned.  
Author: AI assistant; independent human review not performed.  
Version: 0.2.0 · 2026-10-17. Status: DRAFT — PENDING HUMAN REVIEW.  
Review requirements: intended-use direction is owner-confirmed in D-01; formal G0 review of this charter, proposed criteria and reviewer appointments remains pending. Domain and independent technical reviewers assess G1–G4 evidence for the named use. No signature or gate approval is implied.

## Purpose and intended users

Warehouse Lab is an educational and portfolio-oriented, evidence-grounded warehouse operations research project. Its primary objective is to demonstrate an end-to-end internal operations improvement process: discover and bound a business question, diagnose available operational evidence, formulate testable hypotheses, assess improvements through controlled experiments where defensible, and produce conditional recommendations with explicit uncertainty. A negative or inconclusive finding can be a useful research outcome. The owner confirmed this direction in [D-01](RISK_AND_DECISION_LOG.md#d-01--owner-confirmed-intended-use-direction); that confirmation is separate from formal G0 approval. [Owner instruction](evidence/2026-10-17-g0-direction/owner-confirmation.md).

Intended users are the project owner/researcher and human reviewers or portfolio evaluators examining the evidence, method and decision reasoning. The current application is a local exploratory and communication instrument within that research. Its operation is not evidence that a real warehouse has improved or that a specific business problem has been established. No customer interviews, measured labor/cost baseline or quantified business benefit is supplied in the inspected evidence. [Initial assignment](evidence/2026-10-17/assignment.md), [inspection baseline](evidence/2026-10-17/baseline-inventory.json).

## Strategic hierarchy

| Priority / role | Application to this project |
|---|---|
| **A — primary objective: end-to-end operations improvement** | Evidence-driven discovery → diagnosis → hypotheses → controlled experimentation → conditional research recommendations; actual inefficiencies remain questions until supported. |
| **C — internal management framework: AI Product Management and Technical Program Management** | Requirements, acceptance criteria, evaluation protocols, risk management, evidence traceability, decision records, gates and human authority govern the work. They create no user-facing features. |
| **B — technical research methodology: data analytics, operations research and simulation** | Published real data, quantitative analysis, optimization methods and simulation investigate the questions. Three.js helps understand processes and communicate findings; visual fidelity does not establish operational validity. |

This hierarchy describes purpose, governance and method; it is not a claim that every research phase has been completed. [Owner confirmation](evidence/2026-10-17-g0-direction/owner-confirmation.md), [internal practices](INTERNAL_PRODUCT_PRACTICES.md).

## Research question and bounds

"How can real-world warehouse data be used to identify operational inefficiencies, evaluate potential improvements, and support better business decisions?"

For this project, investigation is bounded to the published footwear warehouse dataset, its documented order/allocation/layout relationships, and the current abstract 10-robot model. Candidate questions include which source patterns merit further investigation and whether the existing storage scenarios allow a defensible comparison. Neither a bottleneck nor a superior policy is presumed. Real-business decision support means transparent research reasoning and evidence requirements; it does not authorize acting on this model in a facility. [Data card](DATA_CARD.md), [experiment credibility](EXPERIMENT_CREDIBILITY.md).

## Research objectives and outputs

1. Define candidate operational questions from traceable source evidence and identify missing stakeholder/field evidence before diagnosing a real problem. Output: a bounded problem statement or a documented inability to establish one.
2. Distinguish source observations, derived analytical measures, modeling assumptions and simulated results. Output: auditable lineage, exception records, assumption and claim registers.
3. Formulate falsifiable improvement hypotheses with an estimand, common demand/supply controls and evaluation protocol before interpreting differences as effects. Output: an experiment-readiness assessment; an inconclusive comparison is acceptable when controls fail.
4. Verify the implemented model separately from validating its adequacy for a stated use. Output: reproducible technical evidence and an explicit account of unresolved physical/operational validity.
5. Produce conditional educational research recommendations, including “do not conclude,” “do not change” or “obtain more evidence.” Output: decision reasoning, alternatives, uncertainty and evidence needed for any later study; no procurement or deployment advice.

These are research outcomes, not new application requirements. The existing viewport, controls, inspectors, robot lifecycle and metrics support exploration; their functionality is specified separately in [REQUIREMENTS](REQUIREMENTS.md). Existing results do not establish completed discovery, controlled causal experiments or field validation. [Evaluation plan](EVALUATION_PLAN.md).

## Frozen MVP scope and non-goals

Preserve the existing Vite/TypeScript/Three.js warehouse, 10-AMR default, published storage configurations, routing, picking/delivery lifecycle, controls, inspectors, metrics, exports and deterministic query panel. The current assignment authorizes documentation and governance consistency checks only. It authorizes no changes to the simulation, source/normalized data, KPI equations, tests, visual design or previous evaluation evidence. [Owner instruction](evidence/2026-10-17-g0-direction/owner-confirmation.md), [MVP scope](../README.md).

Excluded: new modules, dashboards, user journeys, algorithms, optimization policies, learned AI models, replenishment, physical robot subsystems, real-world deployment, equipment procurement recommendations, staffing/layout investment advice, safety certification, productivity guarantees and ROI claims. The broader research methodology does not authorize implementation of additional experiments or features in this revision. Any later scope or model change needs separate authorization and affected gate review. [Decision log](RISK_AND_DECISION_LOG.md), [gate procedure](GATE_REVIEWS.md).

## Assumptions and evidence boundaries

| Evidence class | Current meaning and limitation |
|---|---|
| Observed source records | Publisher CSV/layout records and retained bytes establish what is published, not verified live stock or performance. Some data are anonymized/randomized. |
| Derived values | Normalized joins, wave/order grouping and descriptive counts follow declared conversion rules; source ambiguities and exclusions remain visible. |
| Assumed model inputs | One carton per allocation cell, size-token interpretation, 0.1 modeled m/source unit, stacked-tier treatment of source floors and hypothetical AMR/service/release settings are unvalidated assumptions. |
| Simulated outputs | Travel, completions, failures, utilization and congestion are model-relative outcomes, not observed warehouse operations or causal improvement evidence. |

Stock semantics, physical scale/floor connectivity, order reporting unit and representative workload remain unresolved. Published policies have unequal SKU-level supply; their current results cannot isolate a policy effect. No empirical AMR/stock/cost reference establishes operational accuracy or business benefit. No positive effect, physical error threshold or ROI target is invented. [Data card](DATA_CARD.md), [model card](MODEL_CARD.md), [findings F-02–F-12](RISK_AND_DECISION_LOG.md), [comparison assessment](EXPERIMENT_CREDIBILITY.md).

## Proposed success and guardrail metrics

These are proposed research-review criteria, not ratified gate thresholds. Existing EVAL results and numerical tolerances are retained unchanged; technical PASS does not validate a physical warehouse. No positive optimization result is required.

| Dimension | Proposed success / guardrail measure | Evidence / acceptance boundary |
|---|---|---|
| Evidence quality | 100% of material claims have a source/evaluation link, evidence class and stated limit; unsupported field/causal/ROI claims: zero | [Claim register](CLAIM_REGISTER.json), EVAL-01/10; source semantics need domain review even when hashes reconcile. |
| Methodological validity | Every proposed causal contrast declares its estimand, workload, SKU supply, geometry and parameter controls before ranking; failed controls yield INCONCLUSIVE, not a winner | EVAL-08/09, [experiment assessment](EXPERIMENT_CREDIBILITY.md); no minimum effect size or statistical confidence is yet justified. |
| Technical correctness | Exact pinned-source reconciliation; zero named stock/accounting/reservation violations; routing and KPI oracle agreement at existing proposed tolerances | R-01–08/13, EVAL-01–07/13; evaluated cases only, separate from operational validity. |
| Reproducibility | Identical pinned data/code/configuration reproduce the event hash in the tested environment; record run identity and all exceptions | EVAL-05/10; priority-seed aliases are not independent replications. |
| Decision usefulness | Every research recommendation identifies the question, evidence, alternatives, assumptions, uncertainty, limits and next evidence/action; withholding a recommendation is valid | Owner + independent reviewer assess clarity and warranted scope at G0/G4; no empirical business-value threshold is available. |
| Scope / authority guardrail | Zero MVP/data/KPI changes in this documentation revision; five PENDING gates and zero recorded gate decisions until formal review | [Preservation check](evidence/2026-10-17-g0-direction/preservation-checks.json), [gate register](GATE_REVIEWS.json); D-01 direction confirmation is not gate approval. |

For any separately authorized future operational study, domain reviewers would need empirical references and decision-specific tolerances before validating a model or claiming business impact. EVAL-11 remains INCONCLUSIVE and is a transfer boundary, not a requirement that this educational project prove a real-world benefit. [Evaluation plan](EVALUATION_PLAN.md).

## Stakeholders, authority and outstanding appointments

| Stakeholder / role | Current status and authority |
|---|---|
| Project owner (requester) | Confirmed D-01 intended-use direction; accountable for scope and progression. Must formally review the charter/criteria, appoint reviewers and record any gate outcome. No formal gate decision is recorded. |
| Independent product/QA reviewer | Unassigned. Needed for G0 evidence/criteria review and challenge of author conclusions; no independent review claimed. |
| Data steward / warehouse-domain reviewer | Unassigned. Needed to resolve source/stock/order/geometry meanings and review data applicability at G1 and later gates. |
| Independent simulation/OR reviewer | Unassigned. Needed for technical evidence, model adequacy and experiment controls at G2–G3. |
| G4 research decision reviewer / owner | Project owner accountable; reviewer appointment and review still pending. Judges whether conditional research conclusions follow from evidence; cannot extend intended use to deployment. |
| AI assistant | Documents, checks and recommends; is not an independent reviewer, human approver or source of operational ground truth. |

No actual warehouse operator, procurement authority, customer representative or independent validator is claimed as a participating stakeholder. G0 preparation evaluates document completeness separately from formal approval. All five gates stay PENDING. [G0 readiness assessment](G0_READINESS_ASSESSMENT.md), [gate procedure](GATE_REVIEWS.md).
