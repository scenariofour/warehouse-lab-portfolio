# Warehouse Lab — model card

Owner: simulation maintainer role unassigned; project owner accountable for intended use. Author: AI assistant.  
Version: 0.2.0 · 2026-10-17. Status: DRAFT — PENDING HUMAN REVIEW.  
Review requirements: independent simulation/OR reviewer assesses implementation and numerical tolerances; warehouse-domain reviewer assesses applicability. This card records an abstract model, not an operationally validated digital twin.

## Model and intended use

A deterministic, fixed-step discrete-state simulation schedules source-demand units onto AMRs. Three.js renders state and interpolates motion; the query panel calculates deterministic answers. There is no trained ML model, LLM, training dataset or learned predictive accuracy to certify. The owner-confirmed use is educational/portfolio warehouse operations research in [the charter](PROJECT_CHARTER.md) and [D-01](RISK_AND_DECISION_LOG.md#d-01--owner-confirmed-intended-use-direction). This model is one research and communication instrument; operating the application is not the end-to-end research objective. D-01 does not approve G0 or validate the operational model. [Simulation](../src/simulation.ts), [renderer](../src/scene.ts), [analysis](../src/analysis.ts).

| Component | Declared behavior | Material assumption / limit |
|---|---|---|
| Demand | FIFO source-file groups; quantities expand into unique unit tasks; releases at fixed cadence | A group is wave/order, not necessarily a full customer order; no historical robot replay |
| Stock | Reserve at dispatch; decrement at pick; one carton per cell; no replenishment | Actual stock quantity, carton/unit correspondence and as-of time are unconfirmed |
| Allocation | Active published configuration indexes reference + inferred size to locations | Manhattan-nearest service-cell heuristic; not fleet or path-cost optimization |
| Routing | 1m cardinal grid; A*; shelf/equipment footprints inflated by 0.48m | Geometry scale, tier/floor abstraction and service reach are unvalidated |
| Traffic | Current and destination cells reserved; no swaps; blocked-path replanning; higher-ID pull-out/hold | Heuristic liveness in tested cases; no proof for all workloads/configurations or hardware safety |
| Service | Timed abstract picking and exclusive station unload; delivery updates group accounting | No shelf manipulator, elevator/floor transfer, battery, acceleration, charger demand or human dynamics |
| Failure | Missing SKU/size, exhausted stock or static service inaccessibility fails units explicitly | Insufficient stock is a model-relative failure, not observed warehouse service failure |
| Presentation | Conveyor parcels follow deliveries; receiving/forklift context is static | Synthetic support equipment and belt timing; no inbound/truck operation |

Sources: [types/defaults](../src/types.ts), [Grid](../src/pathfinding.ts), [state transitions](implementation.md), [data card](DATA_CARD.md).

## Parameters and numerical conventions

Default: 10 robots; speed 1 modeled m/s; pick 12s; unload 10s; step 0.2s; release interval 6s; priority seed 42; one carton capacity; two stations. Horizontal calibration 0.1m/source unit and displayed tier spacing 1.45m are assumptions. Source floors are treated as stacked service tiers, not navigable floors. Service durations are quantized to steps; event timestamps use fixed-step bookkeeping. A sub-step or measured field-time accuracy claim is unsupported. [Defaults](../src/types.ts), [Simulation.step/emit](../src/simulation.ts), [normalizer](../scripts/prepare_data.py).

The seed shifts deterministic update priority modulo fleet size. It does not randomize demand or allocations, and seed 42 and 52 produce identical events with 10 robots. Such seeds are not independent statistical replications. [E-04](evidence/2026-10-17/model-evaluation.json).

## Technical evidence and boundaries

The default Random run processes 120 groups and 922 demand units: 83 successful groups, 37 failed groups, 825 delivered units and 97 failed units. These values are hypothetical outputs, not historical performance. The terminal horizon is 17,837.6 modeled seconds including parking. Independent event/coordinate/service-time oracles reconcile the default KPIs; 39 A* samples equal BFS distances over the same assumed grid. Exact repeat produces the same full event hash. [E-04](evidence/2026-10-17/model-evaluation.json).

Four published configurations each reach a terminal result in the default window with zero checked cell-reservation conflicts. This verifies implementation properties in those cases. It does not validate physical aisle geometry, robot safety, stock semantics, the plausibility of duration assumptions, or policy causality. [E-05](evidence/2026-10-17/scenarios.json), [evaluation plan](EVALUATION_PLAN.md).

Twelve local diagnostic variants change speed, pick/unload time, release interval, priority or time step. All retain accounting and occupancy invariants. They do not establish real parameter distributions, calibrated errors, confidence intervals or an accepted sensitivity tolerance. Scale, stock and floor-topology uncertainty remain unquantified. [E-04](evidence/2026-10-17/model-evaluation.json), [risk log](RISK_AND_DECISION_LOG.md).

The engine retains at most 20,000 recent events and 720 chart samples; cumulative counters can remain available after event truncation. An event-oracle evaluation must require `droppedEvents == 0`, as E-04 does. A 600-group or full-history completion guarantee is outside the current verified envelope. [Simulation.emit/history](../src/simulation.ts).

## Release/use conditions

Any change to scope, raw-data version, size/stock semantics, grouping, calibrated geometry, default parameters, dispatch/routing, KPI equations or event-clock interpretation requires impact analysis and rerun of affected evaluations. Conditional educational research recommendations must disclose assumptions, evidence gaps and uncertainty. Real-world deployment, equipment procurement recommendations, productivity guarantees and ROI claims are excluded by D-01; any future operational use would require separately authorized scope as well as G2–G4 human review and decision-appropriate evidence. Current gate decisions are pending, not approved. [Gate reviews](GATE_REVIEWS.md).
