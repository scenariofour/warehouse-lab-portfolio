# Warehouse Lab: scenario and proxy feasibility

Owner: project owner; data steward and warehouse-domain reviewers unassigned.  
Prepared with Codex assistance; no new scenarios, calibration or field validation performed.  
Version: 0.1.0 · 2026-10-18. Status: DRAFT — PENDING HUMAN REVIEW.  
Review requirements: owner authorizes any later study; domain reviewers establish units, data applicability and calibration. G0–G4 remain PENDING. This document is a research assessment, not a scenario-control specification.

## 1. Findings and interpretation rules

**No requested variable currently has a validated relationship to real warehouse performance in this model.** Some are represented abstractly, some are available only for descriptive analysis, and others are absent. Public proxies can help frame assumptions and screen alternatives; they cannot turn this single public dataset into interchangeable, realistic warehouses.

The primary research focus is picking diagnosis before a storage-policy change. Its immediate question is whether published differences can support a controlled comparison. The supply/control check needs analytics; simulation is warranted only for a remaining dynamic question. See the [opportunity assessment](PRODUCT_OPPORTUNITY_ASSESSMENT.md) for users, alternatives and economic reasoning.

Evidence labels used throughout: **V** inspected project fact; **R** externally supported observation; **A** analyst assumption/inference; **H** untested product hypothesis; **U** unsupported claim. Representation statuses are deliberately distinct from accuracy:

| Status | Meaning |
|---|---|
| Abstract only | Existing engine has an analogous parameter/state, but physical interpretation is unvalidated |
| Descriptive only | Published records support conditional counts/relationships, not the proposed operational scenario |
| Absent / different model | No relevant process or decision structure exists |

All suggested proxies and studies below are proposals. None has been substituted into production inputs, used to create a new numerical simulation result, or authorized for implementation. A broad publisher statement about possible applications does not establish that the retained schemas contain the observations needed for those applications. [Dataset description](https://data.mendeley.com/datasets/pf2w725pw3/1), [local schemas and exceptions](DATA_CARD.md).

## 2. Variable-by-variable assessment

### 2.1 Facility size and layout

- **Decision affected:** aisle and station arrangement, travel/congestion, relocation and expansion feasibility. Storage area and total building area have different meanings.
- **Required data:** surveyed aisle/rack footprints and dimensions, usable clear height, doors, floor boundaries/connectivity, lifts/stairs, turning/passing rules, staging/dock areas, equipment envelopes and station positions; actual path/service observations.
- **Possible proxy:** retained Cartesian location relationships and notebook/SVG block rules are a **V** description of published geometry. A scaled schematic can support an **A** toy sensitivity question. CAD/PDF files are retained but the engine has not decoded them. A generic public building footprint would indicate an exterior shell, not usable internal flow.
- **Uncertainty:** README says meters while the model adopts 0.1 modeled meter/source unit; source levels are treated as rack tiers although notebook/SVGs call them floors. The inferred grid and synthetic support areas are not a survey.
- **Existing status:** **abstract only**. A* shortest paths are verified against BFS on the same assumed grid, not measured warehouse routes. No current claim of accurate physical size, floors or capacity is defensible. [Data/model cards](MODEL_CARD.md).
- **Needed before extension:** authoritative unit/topology interpretation and a surveyed traversable graph, then held-out route/time checks. Geometry/floor changes require separately authorized data/model work and affected gate review. Uniformly scaling a renderer changes distances without establishing aisle access, rack count, station/dock capacity or robot maneuverability.

### 2.2 Physical storage capacity

- **Decision affected:** overflow, storage media, pick-face size, inventory policy and whether more usable storage is needed.
- **Required data:** SKU/package dimensions and orientations, stackability, weight/load and compatibility limits, rack/bin capacities, usable positions by type, maximum inventory trajectory, reserve/pick-face stock and replenishment rules.
- **Possible proxy:** count published locations and encoded cells; inspect assumed item-to-location relationships. A declared carton-volume × inventory worksheet can illustrate cube arithmetic if dimensions are explicitly hypothetical. The Georgia Tech method provides a credible structure joining product/storage geometry and picking/restocking labor. [Warehouse Science](https://www.warehouse-science.com/apps/forward/cartons/).
- **Uncertainty:** 2,292 locations and 41,256 modeled cells are not measured pallet positions, cubic capacity or available slots. One carton per cell is assumed. Empty/occupied locations do not express cube, weight, mixing, floor/staging constraints or replenishment headroom.
- **Existing status:** **abstract only** for depletion/location occupancy; **absent** for physical capacity. `occupancy = locations with modeled stock / 2,292` cannot validate an expansion decision. [KPI contract](REQUIREMENTS.md#kpi-contract).
- **Needed before extension:** product and storage master dimensions, compatible-location rules, inventory snapshots/trajectories and inbound/replenishment data; likely a cube/slotting model before a dynamic flow model. Additional processes and capacity controls would be future scope.

### 2.3 Number of SKUs

- **Decision affected:** slot count, forward/reserve assortment, replenishment complexity, route dispersion and long-tail service.
- **Required data:** agreed SKU identifier and unit of measure, active assortment by date, dimensions/constraints, demand and inventory per SKU, introductions/discontinuations and substitutions.
- **Possible proxy:** distinct `(reference, normalized size)` in order/allocation data; reference-only counts for a separately labeled aggregation; demand-ranked concentration within the observed sample.
- **Uncertainty:** Product.csv has 208 references, not 208 size-specific SKUs. Allocation distinct-SKU counts differ by policy: 2,980 / 7,062 / 3,245 / 3,532 under current interpretation. Unknown references and inferred half-sizes affect joins. Duplicating or renaming identifiers would invent an assortment without observed demand/space relationships.
- **Existing status:** **descriptive only**, with SKU lookup represented abstractly. Accurate future assortment effects are unsupported. [Data card](DATA_CARD.md), [data audit](data-audit.md).
- **Needed before extension:** reconciled active SKU master and units, assortment/date coverage and joint demand/stock assumptions. Any synthetic additions need separate experiment identity and authorization; a SKU-count slider alone is not a realistic scenario.

### 2.4 Inventory distribution

- **Decision affected:** availability versus accessibility, slotting, reserve allocation, replenishment and whether a route/traffic intervention can address missed fulfillment.
- **Required data:** reconciled quantity by SKU/location/as-of time, allocations/reservations, demand/stock alignment, replenishment and receipts, eligibility and alternative locations.
- **Possible proxy:** existing one-carton-per-cell counters and derived demand-only supply bounds. Useful for testing internal consistency of the sandbox. A common supported SKU subset could be a proposed experiment, explicitly changing the question/population.
- **Uncertainty:** README calls the payload quantity; engine interprets it as size. Snapshot date and carton/unit equivalence are unresolved. Equal total cells mask different SKU counters; Class-Based/Dedicated/Hybrid also exclude cells lacking geometry. Current inferred stock cannot establish a real stockout.
- **Existing status:** **abstract only**. All six policy pairs fail stock equivalence. Matching delivered totals or dividing distance by deliveries does not repair different task mixes. [Experiment credibility](EXPERIMENT_CREDIBILITY.md).
- **Needed before extension:** source clarification first. A common-stock placement design or shared subset needs owner/domain agreement, explicit exclusions and new derived experiment inputs; it cannot silently replace the published configurations. Replenishment effects require new processes and data.

### 2.5 Order volume and composition

- **Decision affected:** pick workload, batch/route complexity, resource headroom and service risk under growth.
- **Required data:** line/unit/order identity, creation/release/cutoff/due times, cancellations, batching, units/cartons, order-size and SKU-affinity distributions, forecast assumptions and representative periods.
- **Possible proxy:** 122,370 published customer rows, their quantities, waves and dates; descriptive lines/units per wave/order group and co-occurrence. Observed blocks could support a proposed replay study; hypothetical multipliers can support only labeled stress questions.
- **Uncertainty:** 32,634 order numbers map to 39,858 wave/order groups; 4,024 numbers span waves. There are 2,559 exact repeated customer rows, retained without unsupported deduplication. Source rows are not chronological; absence of completion times prevents measuring historical processing performance. A multiplier holding mix constant may miss more small orders, bulky lines or correlated SKU demand.
- **Existing status:** **descriptive only** for source demand; **abstract only** for fulfillment. Default first 120 file groups/922 units at six-second release is a regression window, not demand replay. [Data card](DATA_CARD.md).
- **Needed before extension:** agree demand/service units and preserve source exceptions, define sampling/blocks and matched inventory, then obtain observed release/service events. Changing order ordering, releases, workload construction or stock requires a separately authorized experiment; do not rerun a full year against an unknown stock snapshot.

### 2.6 Robot capacity

- **Decision affected:** whether an extra robot can increase useful output, fleet/station balance and investment-study requirements.
- **Required data:** actual payload/task architecture, speeds/acceleration/turning, pickup interfaces, charging/battery cycles, availability/repair, traffic management, dispatch behavior and station capacities; representative arrivals and due times.
- **Possible proxy:** current ten robots, one-carton capacity, 1 modeled m/s, 12s pick and 10s unload for an **A** conceptual cycle-time budget. Published robot queueing research offers an analytical alternative and structural checklist, not a transferable calibration. [EJOR research](https://pure.eur.nl/en/publications/estimating-performance-in-a-robotic-mobile-fulfillment-system/).
- **Uncertainty:** public research on pod-carrying robots has a different service architecture. Nominal speed and payload from a datasheet would be upper-bound component inputs, not an observed fleet cycle or congestion curve. No charging, acceleration or robot breakdown is modeled.
- **Existing status:** **abstract only**. Ten is a default, not an optimized count; there is no current fleet response curve or measured purchasing recommendation. Priority seed offsets are not independent demand replications. [Model card](MODEL_CARD.md).
- **Needed before extension:** supplier/site traces, actual operating constraints, model adequacy review and demand/service calibration. Fleet/station sweeps and battery/failure models require separate authorization. A real procurement study belongs in an engineering model reviewed against acceptance tests.

### 2.7 Labor capacity

- **Decision affected:** shift staffing, skills allocation, overtime, cross-training and how automation changes tasks.
- **Required data:** people/skill roster, shifts and breaks, paid versus productive time, observed or engineered standards, walking/handling ergonomics, learning/fatigue and attendance, work sharing with equipment.
- **Possible proxy:** raw operator identifiers describe assignments in the source; they are not paid-hour or productivity observations. Hypothetical task-minutes and available-hours arithmetic can demonstrate a staffing worksheet. Dynamics documents a workload-capacity planning workflow. [Official documentation](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/schedule-workload-capacity).
- **Uncertainty:** identifiers may be anonymized; assigning a uniform rate to every operator invents performance. Robot busy time cannot be translated directly to a worker's productive/paid time. No measured breaks, skills, shifts or effort exist here.
- **Existing status:** **absent**. No valid labor utilization, staffing forecast or headcount-saving output.
- **Needed before extension:** time study and agreed workload standards with labor/domain review. Use a workload/shift optimization worksheet first; human-robot interaction or task-based labor simulation would be a distinct model extension.

### 2.8 Geographic location

- **Decision affected:** site selection, labor/facility cost context, inbound/outbound reach and disruption exposure; not an internal routing policy by itself.
- **Required data:** actual supplier/customer and candidate-site coordinates, demand/flows, transport modes and service commitments, local labor/property and site constraints.
- **Possible proxy:** declared hypothetical candidate cities, regional wage/rent context, aggregated public freight origins/destinations. Census CFS provides regional shipment context. [2022 CFS tables](https://www.census.gov/data/tables/2022/econ/cfs/aff-2022.html).
- **Uncertainty:** customer codes are not addresses. No calibrated geography-to-demand or geography-to-process mapping exists. US regional examples cannot be assigned to the original warehouse as if observed, nor establish its costs or origin-destination network.
- **Existing status:** **absent / different model**. A geographic label has no causal effect on internal physics.
- **Needed before extension:** a separately authorized network decision with geocoded data, candidate sites, cost/service matrices and optimization. Local operating assumptions could later feed that model through a documented interface, not a map label.

### 2.9 Local labor costs

- **Decision affected:** economic comparison of task changes, labor/automation and candidate sites; distinct from physical throughput.
- **Required data:** role-specific hourly rates, overtime, benefits, agency costs, payroll taxes, staffing/contract rules, currency/price date and genuinely avoidable expense.
- **Possible proxy:** fixed-vintage BLS metro occupational wage estimates, choosing relevant jobs such as stockers/order fillers versus material movers, plus separately declared compensation assumptions. BLS compensation concepts distinguish wages and benefit components. [May 2024 metro tables](https://www.bls.gov/oes/2024/may/oessrcma.htm), [NCS concepts](https://www.bls.gov/opub/hom/ncs/concepts.htm).
- **Uncertainty:** metro/cross-industry estimates are not site offers, warehouse-only productivity or fully loaded cost. Agency/overtime/benefits cannot be silently inferred. US wages do not calibrate an unidentified Canadian/other-location operation. Fixed 2024 tables are an illustrative source, not a claim about the latest labor market.
- **Existing status:** **absent**. Costs can be a hypothetical external worksheet, not an accurate simulator output; changing dollars does not change travel/service behavior.
- **Needed before extension:** match job, geography, date, currency and paid-hour basis, obtain employer/finance evidence, and separate released task capacity from avoided payroll. See the [hypothetical economics](PRODUCT_OPPORTUNITY_ASSESSMENT.md#transparent-hypothetical-financial-model). No labor saving is measured here.

### 2.10 Facility costs

- **Decision affected:** lease/expand/relocate alternatives, storage media and automation investment trade-offs.
- **Required data:** rentable/usable area, lease/ownership terms, fit-out/racking, taxes/insurance, utilities, maintenance, concessions, escalation, relocation and stranded cost.
- **Possible proxy:** brokerage industrial asking-rent reports, with market, asset type, lease basis and date pinned. The Salt Lake City Q3 2026 report specifies per-square-foot **monthly** NNN asking rent—a useful example of why units and included costs must be recorded. [Cushman & Wakefield](https://www.cushmanwakefield.com/en/united-states/insights/us-marketbeats/salt-lake-city-marketbeats/industrial).
- **Uncertainty:** asking is not achieved rent or total occupancy cost; industrial averages differ from a particular warehouse's clear height, power and location. NNN obligations, fit-out, concessions and area conventions matter. Renderer floor area is not a rentable-area measurement.
- **Existing status:** **absent**. No supported real-estate/capital cost estimate or area-based savings.
- **Needed before extension:** owner/finance-approved cost baseline, comparable quotes and cash-flow assumptions in an external worksheet. Neither a rent overlay nor a larger scene creates a facility sizing model.

### 2.11 Transportation distances

- **Decision affected:** site/customer allocation, landed cost and delivery promises; these are interfacility/outbound network choices.
- **Required data:** actual OD shipment volumes by lane/mode, road paths/travel times, truck restrictions, rates/tariffs, frequency, minimum charges, handling and border/port constraints.
- **Possible proxy:** published regional CFS shipment geography/distance and freight context; straight-line distance can be a labeled lower-bound screening approximation. A future road-network route estimate would improve distance geometry but would still not be a rate or delivery commitment. [CFS methods](https://www.census.gov/programs-surveys/cfs/technical-documentation/methodology.html).
- **Uncertainty:** aggregate flows cannot recover customers, lanes or modes for this company. Straight-line distance ignores roads; road distance alone ignores rates, congestion, schedules and truck restrictions. Do not convert internal modeled robot meters into transport mileage.
- **Existing status:** **absent / different model**. No transport processes or customer geography represented.
- **Needed before extension:** actual OD/geocoding and service/cost matrices, then a capacitated location/allocation model; simulation only if timing/disruption remains decision-relevant. No routing proxy is ingested in this assessment.

### 2.12 Demand seasonality

- **Decision affected:** peak staffing/equipment, temporary space, replenishment timing and service commitments.
- **Required data:** multiple full seasonal cycles of arrivals, mix and cancellations, promotional calendar, outages, closures, backlog, demand censoring/stock availability and forecast error.
- **Possible proxy:** weekly/monthly profiles within the observed January–October sample, explicitly descriptive. Census unadjusted retail sales and seasonal factors can suggest an **A** stress shape for a US sector, not local warehouse units. [Seasonal-factor archive](https://www.census.gov/retail/mrts/historic_releases.html).
- **Uncertainty:** missing November/December and lack of repeated years prevent estimating annual patterns reliably. Retail dollars reflect prices and channel mix; a manufacturing warehouse is a different flow. Seasonally adjusted series remove the pattern being investigated. A 2×/3× multiplier is an assumption, not an inferred peak forecast.
- **Existing status:** **descriptive only** for dates; **absent** for calibrated time-varying seasonal arrivals and replenishment. Current release cadence is fixed.
- **Needed before extension:** define forecast population, collect representative history and validate on unseen periods. First use workload arithmetic/mix analysis. New release schedules, synthetic workloads or peak experiments need separate authorization and clear identities.

### 2.13 Service-level requirements

- **Decision affected:** capacity sufficiency, release priority, backlog recovery and the minimum acceptable resource design.
- **Required data:** promised unit (customer order, line, wave or shipment), due/cutoff times, priority class, calendars, completeness/error rules, downstream pack/load/transit times, late/cancel handling and contractual loss consequences.
- **Possible proxy:** an explicitly hypothetical target horizon and the fraction of demanded units/groups completed by it. A tail-latency statistic can be proposed if the sample and treatment of failures are declared. No generic “same day” promise should be imputed.
- **Uncertainty:** source creation time is neither due time nor model release time. Mean completion of successful wave/order groups ignores failures and tails; terminal throughput including parking is not on-time complete customer shipment performance. A failed group's partial deliveries do not make it a successful customer order. [KPI contract](REQUIREMENTS.md#kpi-contract).
- **Existing status:** **abstract only** for model release-to-success timing; **absent** for an actual SLA, deadlines and end-to-end outbound service. The synthetic conveyor is not packing/shipping capacity.
- **Needed before extension:** decision-owner-defined service contract and corresponding observed timestamps; align numerator, denominator and horizon before validation. New priorities, SLA metrics, deadlines or downstream processes would need separate scope authorization; this report changes no KPI equation.

## 3. Internal operations and network planning are separate problems

| Boundary | Internal warehouse operations | Facility location / network planning |
|---|---|---|
| Decisions | Picking/release/slotting/resource allocation within one facility | Open/close/select sites, allocate demand and inventory, route flows |
| State/constraints | Tasks, inventory locations, aisles, stations, queues, shifts | OD demand, candidate sites, lane costs, site capacities, transit/service coverage |
| Natural first methods | SQL, workload arithmetic, slotting/routing OR, queueing; DES for material dynamic interactions | Cost/service screening, capacitated mixed-integer optimization, robust/scenario analysis |
| Lab today | Abstract unit tasks and robots on an assumed grid | None |
| Potential future interface | Conditional throughput/cost envelope with demand, units and uncertainty declared | Consume externally validated capacity/cost/service assumptions, never a raw animation result |

The [facility-location example](https://www.gurobi.com/resources/demos/facility-location-problem-demo) illustrates fixed facility cost versus distribution cost. [Amazon's network account](https://www.amazon.science/blog/navigating-uncertainty-in-amazons-middle-mile-network) illustrates flow uncertainty and network structure. These are methodological references, not evidence that Warehouse Lab can solve network design. A site can have favorable labor cost and poor transport/service economics; an inexpensive lease can require costly handling or migration. A single geographic ranking would conceal these trade-offs.

## 4. Proxy acceptance protocol for any later authorized study

Use a proxy only if it answers a declared question more credibly than leaving the parameter unknown. More input numbers do not necessarily create more information. Proposed protocol:

1. **Define the decision and mechanism.** State how the variable could change the selected action, not merely a KPI. Choose the simplest sufficient model.
2. **Record identity and units.** Source URL/file/version, access date, geography, population, period, unit/pack size, currency/price year and transformations. Keep direct observations, derived values and assumptions separate.
3. **Assess transfer.** Compare the source architecture, task mix, facility constraints and time period with the target; document what is missing. Do not call an aggregate population proxy a local observation.
4. **Check dependencies.** Larger orders may alter batching and service time; higher stock changes aisle use and replenishment; more robots change station/traffic queues. Independent multipliers can violate these relationships.
5. **Assign uncertainty honestly.** Use low/base/high assumptions or bounded cases where supported. Do not assign confidence intervals or probabilities without a sampling/calibration rationale. Structural stock/floor uncertainty can dominate small timing changes.
6. **Test decision sensitivity.** Compare assumptions to an analytical bound/reference first. If credible inputs switch the action, report an unstable conclusion and seek the input with greatest decision relevance. If a proxy never changes the action, avoid unnecessary model detail.
7. **Stop at the claim boundary.** No physical capacity, fleet, service or savings claim without an empirical reference and decision-specific tolerance; no automatic gate progression. Calibration observations must be separate from held-out validation.

This protocol draws on intended-use credibility and VVUQ principles, not a claim of standards conformance. [NIST digital twins program](https://www.nist.gov/programs-projects/digital-twins-advanced-manufacturing). A calibrated component does not validate the whole model or an architecture absent from it.

### Dependencies worth retaining in the research narrative

| Example change | Coupled effects that a simple scale/label misses | Consequence for interpreting a scenario |
|---|---|---|
| More SKUs at fixed inventory | SKU coverage, slot fragmentation, velocity/affinity and replenishment all change | Same units need not mean same work or available stock |
| More area at fixed stations | Paths, aisle count/width, equipment envelopes and station travel change nonuniformly | Scaling coordinates is not a new warehouse design |
| More demand at unchanged stock | More units become unfulfillable before capacity is tested | Missing deliveries cannot automatically be attributed to traffic or fleet size |
| More robots with fixed station capacity | Robot travel availability rises while queues/blocking may increase | High fleet utilization or longer terminal time can be misleading without useful output and wait decomposition |
| Lower local wage | Changes economic valuation, not robot physics | A cost worksheet and a process model answer different questions |
| Shorter dispatch window | Changes whether the same delays are acceptable | Terminal completion alone does not establish adequate service |

## 5. What can be reported now versus what remains proposed

| Evidence/work item | Current permitted conclusion | Additional evidence / authority boundary |
|---|---|---|
| Read retained source audit and experiment outputs | Published counts and conditional supply bounds; current comparisons are confounded | No new data treatment or study executed here |
| Explain stock checks using existing outcomes | Every current scenario reaches its own assumed supply ceiling at termination | Does not establish real stockouts, adequate speed or SLA achievement |
| Use existing 10-robot walkthrough | Illustrate abstract movement, dispatch and contention with disclosed assumptions | No calibrated capacity, safety or investment recommendation |
| Consider demand/mix characterization | A promising SQL-first research opportunity; incomplete period limits forecasting | New workload analyses or derived experiments should be separately defined/authorized |
| Consider robot/station sensitivity | Potential dynamic research question; retained diagnostics verify invariants, not operational robustness | New experiment runs/designs, parameter controls or model processes require separate authorization |
| Consider labor/rent/transport proxies | Identify public source types and unit/transfer risks | External hypothetical economic worksheet only; no data loaded or benefits measured |
| Consider network/location planning | Different, credible industry problem | New data and model; outside the frozen MVP and present intended use |

The next evidence priority is authoritative stock/unit/date and order/topology interpretation, then practitioner decision artifacts and matched timing observations. If those cannot be obtained, an honest portfolio result is a bounded diagnostic case explaining why operational recommendations cannot yet be made. Do not compensate by adding scenario sliders or uncalibrated geography/cost overlays.
