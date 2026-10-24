# Warehouse Lab — requirements and acceptance contract

Owner: Project owner; QA reviewer role unassigned. Author: AI assistant.  
Version: 0.2.0 · 2026-10-17. Status: DRAFT — PENDING HUMAN REVIEW.  
Review requirements: owner ratifies frozen scope; independent reviewer ratifies thresholds and the evidence envelope. Technical PASS does not approve a requirement for operational use.

The original MVP defines existing capabilities; the [owner direction instruction](evidence/2026-10-17-g0-direction/owner-confirmation.md) governs this documentation revision and preserves that MVP. Criteria below formalize existing capabilities and evidence obligations; they introduce no product feature. [Initial assignment](evidence/2026-10-17/assignment.md), [README](../README.md).

The research objective is evidence-driven end-to-end operations improvement; AI PM/TPM governs the work and data analytics/OR/simulation supplies the methodology. Research success is evidence quality, methodological validity, technical correctness, reproducibility and decision usefulness, including negative/inconclusive outcomes. No specific warehouse inefficiency is established by this requirement list. The [charter](PROJECT_CHARTER.md) defines research objectives and proposed guardrails separately from the existing application requirements below. D-01 confirms intended-use direction only; formal gates and criterion ratification remain pending. [D-01](RISK_AND_DECISION_LOG.md#d-01--owner-confirmed-intended-use-direction).

| ID | Existing requirement / constraint | Proposed acceptance criterion | Verification and limit |
|---|---|---|---|
| R-01 | Preserve published input provenance | All 21 retained files match version-1 manifest; no fabricated production records | EVAL-01; hashes authenticate bytes against the pinned manifest, not warehouse semantics |
| R-02 | Preserve transformations and lineage | Exact reconciliation of 2,292 coordinates, four allocation arrays and all 122,370 customer rows; each logical source row appears once | EVAL-01; current inferred sizes and wave/order grouping stay explicit |
| R-03 | Nonnegative, conserved modeled inventory | At every checked state: `remaining >= reserved >= 0`; terminal initial stock − remaining = delivered; no active cargo/reservations at completion | EVAL-02, EVAL-06; only the one-carton-per-cell model |
| R-04 | Navigable, rack-free routes | Valid free endpoints; cardinal adjacent cells; selected A* lengths equal independent BFS reference | EVAL-03; the declared grid is the reference, not a surveyed aisle map |
| R-05 | Ten independently scheduled default robots avoid conflicts | Zero shared current/destination reservations per fixed step; sampled center distance >= 0.99 modeled m | EVAL-04; a numerical guard for the modeled 1m grid, not a physical safety margin |
| R-06 | Picking/delivery/failure accounting | Unique unit delivery IDs; successful + failed groups = released groups at terminal horizon; delivered + failed units = demanded units | EVAL-06; throughput counts **wave/order groups**, not necessarily distinct customer orders |
| R-07 | Deterministic replay and reliable controls | Identical pinned run produces identical event hash; pause leaves state unchanged; reset restores inputs; browser exercises speed, follow, inspection, export and all policies | EVAL-05, EVAL-12 |
| R-08 | Correct, event/state-derived KPIs | Event-count/latency, coordinate-travel, service-time, occupancy and working-time oracles reconcile within `1e-5` numerical units | EVAL-07; numerical tolerance is not real-world accuracy |
| R-09 | Honest policy comparison | No causal ranking unless SKU-level inventory, demand, geometry and control conditions pass an agreed design | EVAL-08; current published scenarios fail necessary inventory controls |
| R-10 | Explicit assumptions and business limits | Stock, size, scale, floors, service, release, seed and experiment limits linked to source and decision records | EVAL-09/10/11; no ROI or deployment-readiness assertion |
| R-11 | Preserve the local MVP | Production build and existing browser workflow pass; visual/UI modules and model calculations remain in frozen scope | EVAL-12; scenario completion covers default 120 groups only |
| R-12 | Preserve human authority | Each gate remains review-state PENDING and decision null until an identified human records a formal gate decision; AI recommendations stay separate | EVAL-10; document checker does not authenticate a human identity |
| R-13 | Reject unsafe local-data replacements | Invalid ZIP payload, duplicate source name or conflicting preserved bytes causes rejection before any source replacement | EVAL-13; isolated fixtures, not adversarial certification |

## KPI contract

`throughput = successful wave/order groups / elapsed modeled hours`; `averageCompletion = mean(final-success event − release event)` over successful groups only; `distance = integrated cardinal robot travel`, including clearing trips; `utilization = moving + picking + unloading robot-seconds / available robot-seconds`; `congestion = route/yield waiting`, excluding outbound station queue time; `occupancy = locations with modeled stock / 2,292`. Traffic is arrival counts, not delay. Equations are in [Simulation getters](../src/simulation.ts); independent reconciliation is [E-04](evidence/2026-10-17/model-evaluation.json).

Event timestamps follow fixed-step bookkeeping; there is no claim of sub-step or measured wall-clock warehouse accuracy. The terminal horizon includes parking, so it differs from final customer-group delivery time. Failures must be reported beside throughput to avoid interpreting lower workload as better efficiency. [Model card](MODEL_CARD.md), [experiment assessment](EXPERIMENT_CREDIBILITY.md).

## Change control

This revision authorizes documentation changes and consistency checks only; application, data, KPI, test and design changes are excluded. For separately authorized future work, a supported defect fix requires a reproducible failure, minimal correction, regression and impact evidence. Changing stock semantics, size rules, customer-order aggregation, metric calibration, topology or policy controls requires an owner/domain decision first. Any such change invalidates affected prior evaluations and reopens G1–G4. New product scope needs a separate authorization. [Risk and decision log](RISK_AND_DECISION_LOG.md).
