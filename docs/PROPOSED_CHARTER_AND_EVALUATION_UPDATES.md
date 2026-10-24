# Warehouse Lab: proposed charter and evaluation amendments

Owner: project owner; independent product, domain and simulation reviewers unassigned.  
Prepared with Codex assistance; recommendations are not owner decisions or independent review.  
Version: 0.1.0 · 2026-10-18. Status: PROPOSAL — PENDING HUMAN REVIEW.  
Review requirements: owner accepts, revises or rejects each proposed amendment; existing formal gate procedure remains authoritative. G0–G4 stay PENDING. No original charter, requirement, evaluation record, claim register or human decision is amended by this file.

## 1. Assessment of the current charter

The current [charter](PROJECT_CHARTER.md) already fits the confirmed A → C → B direction: operations-improvement research is the objective; AI PM governs evidence and authority; analytics/OR/simulation are methods. Its separation of verification from validation, support for inconclusive findings, and scope/claim guardrails should be retained. The issue is decision specificity and audience proof, not a need for more application features.

| Dimension | Current coverage | Specific gap / proposed response |
|---|---|---|
| Portfolio purpose | Explicit educational/portfolio purpose | Identify the professional audience and the skills its members can actually audit; do not invent an employer/client |
| Specialized audience | Owner/researcher and reviewers named | Add warehouse IE/OR, automation solution-design and operations-focused AI PM evaluation audience |
| Business value reasoning | Conditional recommendations, zero unsupported ROI | Require an action-to-KPI-to-economic-mechanism chain and cheaper alternatives; measured dollars are not necessary |
| User and decision relevance | Broad question about inefficiencies and better decisions | Bound one research decision: whether evidence warrants a controlled storage-policy study after diagnosing availability/workload differences |
| Technical credibility | Extensive implementation and evidence checks | Require a model-adequacy map for the selected decision; keep accounting/routing PASS distinct from physical applicability |
| Research quality | Traceability, falsifiable hypotheses and controls | Add external-source independence classification, disconfirming evidence and explicit stakeholder hypotheses |
| Decision usefulness | Recommendation contains evidence, alternatives and uncertainty | Evaluate comprehension and action appropriateness with an independent human task; artifact completeness alone is insufficient |
| Uncertainty | Assumptions and current gaps explicit | Distinguish structural, parameter, sampling and economic uncertainty; show whether each could change the decision |
| Differentiation | Local exploratory/communication instrument | Explain contribution as a transparent portfolio research case; no demonstrated market gap, twin capability or reason to replace Excel/WMS |

Evidence for this assessment: all seven governing documents audited in the [opportunity assessment](PRODUCT_OPPORTUNITY_ASSESSMENT.md#2-audit-of-the-seven-governing-documents). The report's role/frequency/economic assumptions remain untested; no customer discovery has been completed.

## 2. Proposed text for owner review

These are separately reviewable insertions. They supplement the owner-confirmed direction and preserve the current central research question verbatim. They do not replace it, expand operational authority or ratify criteria.

| Proposal | Target location if owner accepts | Proposed amendment text |
|---|---|---|
| P-01 Audience specificity | Charter: purpose/intended users | “The primary portfolio audience is warehouse industrial engineering/OR practitioners, automation solution-design engineers and reviewers assessing operations-focused AI product management. The current users remain the owner/researcher and reviewers. Industry user segments are hypotheses until supported by direct discovery evidence.” |
| P-02 Bounded research decision | Charter: research question and bounds, after the existing question | “The initial decision case is picking diagnosis before a storage-policy change: should an analyst advance a proposal to controlled study, or withhold a recommendation until supply, workload and measurement issues are resolved? The research does not presume a bottleneck or superior policy.” |
| P-03 Economic reasoning | Charter: objectives/outputs | “For each recommendation, document the action, operational mechanism, outcome definition, implementation constraints and potential economic consequence. Separate released capacity from avoidable expense. Where costs/effects are unavailable, use labeled hypothetical arithmetic or state that value is unquantified; no measured savings or ROI is implied.” |
| P-04 Method selection | Charter: objectives/non-goals | “Use SQL, spreadsheet and analytical bounds before simulation. Justify simulation only for an unresolved dynamic mechanism capable of changing the research decision. A simpler adequate method and a decision not to extend the model are acceptable outcomes.” |
| P-05 Intended-use clarity | Model card/charter: use conditions, only if reviewed | “The existing application supports abstract process exploration and research communication. It is not a real-time operating dashboard, validated digital twin, staffing tool, network optimizer or equipment selection system. Such uses require new evidence and separate scope authorization.” |
| P-06 Auditable review | Charter metrics / evaluation plan, as proposed appendix | “Evaluate decision relevance, evidence boundaries, alternatives and uncertainty using the proposed research checks below. Human reviewer observations and formal approvals must be recorded separately from automated verification. Missing review evidence is NOT ASSESSED, not PASS.” |

**Owner review record:** P-01–P-06 all PENDING; no acceptance, rejection, reviewer signature or decision date has been recorded. This proposal file is the only place these amendments currently exist. D-01 remains unchanged. For any acceptance, retain the exact reviewed revision and rationale in the existing governance process; do not infer acceptance from silence or this report's creation.

## 3. Proposed auditable success criteria

These thresholds are proposed portfolio-review criteria chosen for auditability, not validated predictors of hiring outcomes or operational success. They do not change R-01–13 or EVAL-01–13. No positive optimization effect, observed dollar saving, “95% accurate” model or customer purchase is required.

All checks below are **PROPOSED / NOT EXECUTED AS ACCEPTANCE EVALUATIONS**. Some required artifacts now exist, but this author has not independently certified their adequacy or declared these criteria accepted.

| Proposed ID | Criterion / proposed acceptance rule | Review evidence and responsibility |
|---|---|---|
| RES-01 Decision relevance | Exactly one primary research decision, with role, trigger, alternatives, horizon, information requirements and reason to withhold/advance. Separate actual users from hypothetical users in every persona summary | A one-page decision brief traceable to the opportunity assessment; owner and independent product/domain reviewer judge relevance |
| RES-02 Claim discipline | Every material conclusion/numerical claim links to source or explicit derivation, carries V/R/A/H/U meaning and states applicability. Zero invented interviews, buyers, savings, approvals or field-validation claims | A source-to-claim audit of the final memo, all result tables and executive statements; reviewer records exceptions, including unsupported claims removed |
| RES-03 Industry research | Each of the eight requested decision areas has at least one relevant primary method/application reference; all vendor outcomes labeled; academic access limits and negative evidence retained | Coverage matrix and source register; domain reviewer verifies whether a source actually supports the associated use. Multiple sources from one marketing case are not independent evidence |
| RES-04 Simpler-method comparison | Every recommended use case names a simpler baseline and states what extra decision information simulation could add. At least one explicit circumstance where simulation should be skipped | Decision-method table and one worked analytical bound; independent OR reviewer challenges method necessity |
| RES-05 Comparison integrity | For each proposed treatment comparison, declare task population, SKU quantities/eligibility, geometry coverage, parameters, horizon and estimand. Any failed necessary control yields INCONCLUSIVE and no winner | EVAL-08 input checks plus proposed comparison protocol; domain/OR review. Current stock controls fail; do not reinterpret them as passing |
| RES-06 Metric interpretation | All reported performance tables identify units, numerator/denominator, failures/exclusions and horizon. Every service conclusion accounts for all relevant demand, rather than successful-only latency | KPI crosswalk to current equations; reviewer verifies no equation was changed. New deadline/tail measures remain proposals requiring authorization |
| RES-07 Uncertainty and next evidence | For every recommendation, list material structural, parameter, sampling and economic uncertainties, whether each could change the action, and the smallest useful evidence request. Label any unknown action sensitivity UNKNOWN | Assumption-to-decision table; domain and decision reviewers. A sensitivity run on speed alone cannot clear stock/floor uncertainty |
| RES-08 Economic logic | Every hypothetical calculation states all inputs/units, price/currency basis, avoidability and exclusions; arithmetic reproducible. Include a zero-benefit or unfavorable case, with no double-counting of revenue and labor capacity | External worksheet or transparent equations; finance/domain reviewer. No measured economic threshold until a real decision and baseline exist |
| RES-09 Decision comprehension | At least two independent human reviewers, collectively covering warehouse domain and analytical method, complete the task below. Both identify the decision and all critical limitations; zero critical misinterpretations remain unresolved after revision/retest | Preserve questions, responses, rubric, reviewer role/independence and revisions. Reviewer appointments pending; this proposed small sample tests communication, not market adoption |
| RES-10 Reproducibility and scope | Every reused result cites its historical execution identity; all newly authorized analyses retain input/code/config identity and exclusions. For this assignment, only the three requested Markdown files are additions; existing tracked bytes unchanged; five PENDING/null human decisions | File comparison and link checks; historical EVAL results remain untouched. Automated scope checks are not gate review or semantic validation |

For RES-03, “eight areas” means facility sizing, location/network, slotting, fleet, demand/seasonality, labor/equipment, bottlenecks and automation investment. The opportunity scoring separates some of these into narrower candidates; it does not omit any area.

### Proposed independent reviewer task

Give reviewers the executive brief, the existing scenario outcome/control table and the declared model assumptions. Ask them independently, without coaching:

1. What decision can the evidence inform, and who would own it?
2. Can they select a superior storage policy from the current results? Why?
3. Can they infer the real warehouse's required fleet, annual capacity or savings? Why?
4. What simpler analysis should come first, and what question would justify simulation?
5. What missing evidence would most affect the next decision?

Proposed critical errors: interpreting simulation as observed warehouse performance; claiming a causal policy winner despite unequal SKU supply; recommending a fleet/investment/staffing action from this package; treating the first source prefix as annual demand; treating AI assessment as gate approval. A reviewer may reasonably disagree with the recommended research priority; capture that disagreement rather than marking it a comprehension failure. Wrong conclusions after reading the brief signal a communication defect or unresolved ambiguity to address, not a reviewer to discard.

## 4. Evaluation-method extensions and limits

### 4.1 Preserve the existing verification record

EVAL-01–07/12/13 remain historical technical checks with their recorded outcomes. EVAL-08/09/11 remain INCONCLUSIVE for the claims they test. The current read-only research assignment does not rerun the engine or change evidence hashes, numerical outputs, thresholds, inputs, KPI equations or historical review states. This document adds proposed research evaluation, not new completed EVAL records.

Provenance, numerical accounting, operational validity and decision usefulness answer different questions. A valid source hash establishes file identity; a correct SKU counter establishes the arithmetic under an interpretation; neither establishes physical stock. The proposed independent reviewer task evaluates whether the research communicates these differences.

### 4.2 A staged method for a later authorized study

| Stage | Proposed procedure | Reason and stop condition |
|---|---|---|
| Define | Fix the action, service unit, horizon, comparison and cost of a wrong decision; obtain a recent practitioner decision artifact if available | Stop if no bounded decision or responsible stakeholder can be specified; do not build generic controls |
| Diagnose analytically | Reconcile stock/date/size/order semantics; derive SKU-coverage bounds and workload composition; compare against retained outcomes | If availability explains terminal missing units, do not call those missing units evidence of a traffic bottleneck. Delay may still require investigation |
| Assess model adequacy | Map each decision mechanism to represented process, data reference, calibration and missing structure | Stop if the decision depends on absent replenishment, floors, labor, charging or network processes; propose evidence or a different model |
| Design comparison | Declare matched fulfilled task population, SKU inventory, geometry and parameter controls; block by defensible workload periods | Failed controls require INCONCLUSIVE. NIST design/blocking principles inform the proposal, not a preapproved statistical design. [Design selection](https://www.itl.nist.gov/div898/handbook/pri/section3/pri33.htm), [blocking](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm) |
| Validate if operational use is separately authorized | Fit on calibration observations; assess unseen periods/sites appropriate to intended use; compare relevant distributions/queues/throughput with measured references | Reviewer defines errors and tolerances from decision consequences and measurement uncertainty before interpreting results; EVAL-11 cannot become PASS from internal consistency |
| Evaluate uncertainty | Separate structural scenarios, parameter ranges, workload variability and economic assumptions; examine action reversals and regret | Deterministic repeats prove replay, not statistical replication; priority seeds 42/52 alias at ten robots. Do not bootstrap seed aliases or describe arbitrary parameter ranges as confidence intervals |
| Decide and communicate | Compare simpler method, current practice and do-nothing; report useful output/service/failures and conditional economic implications | Recommend no action where uncertainty dominates. Human review remains separate from experiment execution |

Suggested future estimand, **not executed**: for an explicitly common feasible unit-task set, compare total modeled travel or completion-by-an-agreed-horizon while holding common inventory and release conditions fixed; report all failures and queue/service guardrails. This is a sandbox comparison until calibrated externally. Restricting to a common SKU subset changes the target population and could exclude difficult products; disclose that selection rather than generalizing to the full warehouse.

No sample size or effect threshold is prescribed without workload variability and a decision loss function. For deterministic fixed inputs, confidence intervals from identical reruns are meaningless. For stochastic future studies, define the source of randomness and use paired workloads/appropriate independent blocks; do not claim experimental control over real warehouses from a simulator contrast alone.

### 4.3 Proposed evidence-to-decision uncertainty table

| Uncertainty class | Current example | What would resolve or bound it | Current disposition |
|---|---|---|---|
| Structural | Payload size/quantity, floors versus tiers, missing replenishment | Source/domain confirmation, topology and process data; possibly a different model | Action sensitivity UNKNOWN; no real operational recommendation |
| Parameter | Speed, service times, release rule | Observed matched traces, uncertainty and held-out validation | Existing ±20% diagnostics are hypothetical, not empirical bounds |
| Sampling | Nonchronological first 120 groups and partial year | Business-defined sample frame, seasonal coverage and independent periods | No annual demand/capacity generalization |
| Economic | Labor avoidability, equipment/support and migration costs | Employer/finance baseline and alternative quotes | Hypothetical arithmetic only |
| Product/user | Analyst workflow, audience comprehension, adoption | Actual decision artifacts, independent tasks and later discovery | Industry need documented; Warehouse Lab demand unvalidated |

## 5. Governance and next decision

The [G0 readiness assessment](G0_READINESS_ASSESSMENT.md) records document preparation separately from formal ratification, independent review and gate outcome. These proposals do not fulfill the missing human steps. All five gate records remain PENDING; no reviewer is appointed by being described as a target audience.

Recommended owner review sequence:

1. Review P-01–P-06 and the proposed success criteria; keep, revise or reject each explicitly. Preserve the confirmed hierarchy, central question and frozen MVP.
2. Choose whether to commission source/domain clarification and practitioner review for the primary picking-diagnosis case. Define access, reviewer roles and evidence outputs before new analysis/development.
3. If evidence supports a dynamic question, authorize a bounded study separately. If it supports only descriptive analytics or an inconclusive result, finish a credible portfolio narrative at that boundary.
4. Follow the existing formal gate process only when its independent review and evidence requirements are satisfied; this assignment provides no gate progression.

The portfolio should demonstrate that the analyst knows which decision matters, can reject a misleading result and can explain the next evidence needed. More controls, more robots, geographic overlays and a positive improvement percentage are not success requirements.
