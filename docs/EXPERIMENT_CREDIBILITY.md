# Storage-policy experiment credibility

Owner: OR reviewer role unassigned. Author: AI assistant.  
Version: 0.1.0 · 2026-10-17. Status: DRAFT — PENDING HUMAN REVIEW.  
Review requirements: domain owner confirms estimand, comparable stock and geometry; independent experimental-design reviewer approves protocol before any ranking.

## Question and disposition

A causal question such as “Does changing storage policy reduce travel for the same workload and inventory?” is different from “What does each published allocation produce under this simulator?” The current implementation supports the latter descriptive question only. **Policy-effect comparisons are INCONCLUSIVE; decision use is recommended BLOCKED.** [E-02 input controls](evidence/2026-10-17/data-evaluation.json), [E-05 scenario outputs](evidence/2026-10-17/scenarios.json).

## Controls checked

| Control | Observed finding | Consequence |
|---|---|---|
| Demand | Same first 120 source wave/order groups and 922 units in all four scenario runs | Controlled prefix, not a representative random sample of historical operations |
| Parameters | Same default robot/service/release parameters and seed 42 | Controlled computational settings; parameters remain hypothetical |
| Geometry | Same normalized 2,292 locations; 0 / 882 / 864 / 864 source allocation cells excluded by policy | Imported geometry frame shared, but raw treatment coverage differs |
| Stock totals | 41,256 modeled cartons in every imported policy | Necessary count agreement; insufficient for exchangeable workloads |
| SKU supply | All six pairs have unequal reference/normalized-size counters; Dedicated vs Hybrid differs on 2,468 SKU quantities, L1 difference 20,726 cartons | Stock composition is a major confounder, even in the closest-looking pair |
| Availability | Demand-only stock upper bounds are 825 / 807 / 916 / 916 units | Policies face different feasible work before any robot travels |
| Seed/replay | Exact repeated Random event hash matches; seeds 42 and 52 are aliases at fleet size 10 | Reproducible algorithm, not independent randomized replication |
| Outcome denominator | Successful groups and fulfilled units differ; time includes workload drain and parking | Raw distance, throughput and completion means have different task mixes and horizons |

Evidence: [E-02](evidence/2026-10-17/data-evaluation.json), [E-04](evidence/2026-10-17/model-evaluation.json), [E-05](evidence/2026-10-17/scenarios.json). L1 is the sum of absolute SKU-count differences; it is not the number of unique physical cartons to move.

## Observed sandbox outcomes — not a ranking

| Published configuration | Successful / failed groups | Delivered / failed units | Terminal modeled seconds |
|---|---|---|---:|
| Random | 83 / 37 | 825 / 97 | 17,837.6 |
| Class-Based | 95 / 25 | 807 / 115 | 17,849.0 |
| Dedicated | 117 / 3 | 916 / 6 | 20,374.6 |
| Hybrid | 118 / 2 | 916 / 6 | 18,469.8 |

All 120 groups reach a terminal result. Each delivery total equals the corresponding SKU-level supply upper bound for this window. More successful groups cannot establish a routing advantage; fewer delivered units can mechanically reduce travel and drain time. Dividing travel by delivered unit does not eliminate differences in SKU mix, destination distance or congestion. [E-02](evidence/2026-10-17/data-evaluation.json), [E-05](evidence/2026-10-17/scenarios.json).

## Proposed credible design — not executed or approved

1. The owner specifies an estimand and horizon: e.g. total travel for the **same fulfilled unit tasks**, plus service/failure/congestion guardrails. Define whether wave groups or aggregated customer orders are the demand unit.
2. Obtain an authoritative common SKU/size/quantity inventory and dimensions/topology. Agree whether to construct new policy-specific placements of this common inventory or restrict to an explicitly shared supported subset. Do not silently replace the published treatments; remapped inputs would be separately identified derived experiments requiring approval.
3. Hold inventory counters, order sequence/release rules, geometry coverage, robots and service assumptions constant. Match dispatch logic; recompute SKU-to-location maps for each treatment.
4. Pre-register paired workloads/blocks and analysis before running. Independent demand windows and field-calibrated scenarios, not arbitrary aliases of a priority seed, supply the replication rationale. Report every planned run, failure and exclusion.
5. Use a reviewer-approved practical effect size and uncertainty method. No defensible accuracy/effect threshold, power target or sample size exists yet because a business loss function and variance/baseline evidence are missing.

This design adapts the distinction between comparative and other experimental objectives and the use of blocks for nuisance factors from the [NIST experimental-design handbook](https://www.itl.nist.gov/div898/handbook/pri/section3/pri33.htm) and [blocking guidance](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm). It is an internal proposal, not a completed experiment.

## Claim classes

- **Descriptive source fact:** file row counts, product coverage and missing geometry IDs; E-02.
- **Derived analytical measure:** SKU-counter L1 differences and supply upper bounds under declared token semantics; E-02.
- **Hypothetical simulation result:** the table above and all generated travel/utilization values; E-04/E-05.
- **Experimentally supported comparison:** none isolating storage-policy effects in the current package; EVAL-08 is INCONCLUSIVE.
- **Requires field validation:** real warehouse speed/service levels, customer throughput, capacity, safety, savings and ROI; EVAL-11 is INCONCLUSIVE.
