# Warehouse Lab: product opportunity and business value assessment

Owner: project owner; domain and independent reviewers unassigned.  
Prepared with Codex assistance for internal research; no interviews or independent validation performed.  
Version: 0.1.0 · 2026-10-18. Status: DRAFT — PENDING HUMAN REVIEW.  
Review requirements: owner reviews opportunity selection and proposed criteria; specialist reviewers challenge operational applicability. This report changes no approved decision. G0–G4 remain PENDING.

## Recommendation and decision boundary

Focus the portfolio case on **picking diagnosis before a storage-policy change**, for a warehouse industrial engineer or operations analyst preparing a recommendation to an operations manager. The decision is whether the evidence warrants a controlled re-slotting study, or whether supply, workload and measurement problems must be resolved first. This is a research recommendation about what to investigate; it is not advice to change a facility.

The strongest current finding is a reason to withhold a policy recommendation: all four published configurations deliver exactly their respective SKU-supply upper bounds under the sandbox assumptions, while their SKU supplies differ. A shorter run or more completed groups cannot isolate the effect of storage policy. This provides a concrete business-judgment case: avoid choosing an intervention from a confounded comparison. It does not establish that the real warehouse has a stock problem, that travel is efficient, or that robots would improve it. [Existing experiment assessment](EXPERIMENT_CREDIBILITY.md), [data evaluation](evidence/2026-10-17/data-evaluation.json).

Use SQL/spreadsheets first for demand and supply checks. Simulation becomes useful only for a question about interactions over time, such as whether a comparable workload creates aisle blocking or station queues. The present Three.js application can communicate abstract behavior; its visual detail does not increase the credibility of its inputs. The appropriate current product form is a **research/consulting deliverable with an optional simulation walkthrough**, not a live operating dashboard or commercial digital twin.

Two secondary opportunities are descriptive workload characterization for growth/peak planning, and conditional research on robot/station congestion. The first primarily needs analytics; the second would need additional evidence and separate authorization before new experiments. No application work is proposed for this assignment.

## 1. Method and evidence language

This is a targeted desk review, not a systematic literature review or customer discovery study. On 2026-10-18, searches covered warehouse picking/slotting, capacity, AMR sizing, wave release, network design, existing planning software and public cost/demand proxies. Priority went to the dataset publisher, original research/institutional records, operators' own descriptions, official product documentation and government data. Vendor cases were retained to establish documented decisions and workflows, not transferable effect sizes. General market-size claims, unattributed savings and promotional claims without an identifiable application were excluded from the recommendation.

Academic coverage is limited: the cited university abstracts and publisher abstract establish problem/method relevance, not a full independent review of experimental validity. No paywalled full-text results are represented as audited. Source access limitations and conflicts are recorded in section 9. Public cases are selected successes and may omit failed projects, costs and implementation difficulties.

| Label | Meaning here |
|---|---|
| **V — verified project fact** | Inspected local document or retained machine evidence establishes the stated artifact/result. Historical technical checks were read, not rerun for this report. This does not verify physical truth. |
| **R — research-supported observation** | An identified external source documents a method, use or workflow; source type and independence constrain the claim. |
| **A — reasonable assumption** | Analyst inference about workflow, frequency or economic mechanism, to be checked with a relevant practitioner. |
| **H — untested product hypothesis** | A proposed user, need or value proposition for Warehouse Lab with no direct adoption evidence. |
| **U — unsupported claim** | No adequate evidence; may not be used as a project conclusion. |

The workflow tables and opportunity scores below are **A/H** unless directly tied to a source. No contacted customers, purchase intent, willingness to pay, validated personas or confirmed economic buyer exist in this evidence package.

## 2. Audit of the seven governing documents

| Document inspected | Demonstrated/documented evidence | What it cannot establish; implication |
|---|---|---|
| [PROJECT_CHARTER](PROJECT_CHARTER.md) | A → C → B hierarchy; educational/portfolio purpose; owner/researcher and reviewers; useful negative findings; frozen MVP | Broad research question lacks one specific industry decision and audience specialization. Direction confirmation D-01 is distinct from G0 approval. |
| [REQUIREMENTS](REQUIREMENTS.md) | R-01–13 specify provenance, accounting, routes, replay, KPIs, controls and authority | Acceptance contract verifies an abstract application. Numerical tolerances and ten robots do not establish a real service/capacity standard. |
| [DATA_CARD](DATA_CARD.md) | 21 retained source files; 122,370 customer rows; 2,292 locations; 39,858 wave/order groups; published allocations and explicit exclusions | Quantity/size semantics, stock date, floor topology and scale unresolved. WMS origin is not permission to infer observed AMR performance. |
| [MODEL_CARD](MODEL_CARD.md) | Fixed-step deterministic simulation, source-demand unit tasks, A*, reservations, pick/unload lifecycle, ten default robots | No calibrated human labor, charging, acceleration, failures, replenishment or real floor transfer. No learned AI model. Not an operationally validated twin. |
| [EVALUATION_PLAN](EVALUATION_PLAN.md) | EVAL-01–07/12/13 provide technical evidence; EVAL-08/09/11 disclose inconclusive causality, robustness and field transfer | No operational accuracy threshold, practical effect size or business loss function has been established. Passing invariants cannot supply these. |
| [EXPERIMENT_CREDIBILITY](EXPERIMENT_CREDIBILITY.md) | All six policy pairs fail SKU-stock equivalence; different fulfillment sets/horizons; a controlled future design is outlined | No ranking of storage policy effects, even after dividing distance by delivered units. Changing treatments requires authorization. |
| [G0_READINESS_ASSESSMENT](G0_READINESS_ASSESSMENT.md) | Nine document-content items present; reviewer appointments, ratification and formal review outstanding | Document completeness is not formal approval. Five machine gate records remain PENDING with null human decisions. |

### The most decision-relevant existing result

Historical outputs from 2026-10-17, reproduced here by inspection, not a new run:

| Configuration | Assumed SKU-supply upper bound, units | Delivered units | Successful / failed wave/order groups |
|---|---:|---:|---:|
| Random | 825 | 825 | 83 / 37 |
| Class-Based | 807 | 807 | 95 / 25 |
| Dedicated | 916 | 916 | 117 / 3 |
| Hybrid | 916 | 916 | 118 / 2 |

All runs use the same first 120 source groups/922 demanded units and hypothetical settings. The bound is `sum over SKU(size,reference) of min(demand, modeled stock)` with no replenishment. Equality means those terminal delivery totals do not require a traffic-based explanation for the missing units. It does **not** exclude severe delay, congestion or inability to meet a deadline: no empirical deadline was supplied, and the run drains to termination. [Data/model evidence](EVALUATION_PLAN.md#evaluation-register), [controls and outputs](EXPERIMENT_CREDIBILITY.md).

Other material boundaries:

- **V:** 208 Product.csv references are not the number of reference-size SKUs in the allocations. Normalized distinct SKUs range from 2,980 to 7,062 by policy; counts depend on inferred size semantics. Equal 41,256 modeled cells do not establish equal stock or physical capacity. [Data card](DATA_CARD.md).
- **V:** Source creation dates span 2023-01-05–2023-10-19; the first 120 file groups are not chronological sampling. Release every six modeled seconds is engineered, not historical demand replay. Annual seasonality and sustainable capacity cannot be inferred. [Data card](DATA_CARD.md).
- **V:** Source floors are rendered as rack tiers, horizontal scale is 0.1 modeled meter/source unit, and stock is one assumed carton per encoded cell. These are material structural assumptions, not small parameter errors. [Model card](MODEL_CARD.md).
- **V:** Default utilization includes movement, picking and unloading; congestion excludes outbound station queue time; completion averages cover successful groups only; elapsed terminal time includes parking. These denominators matter before interpreting efficiency. [KPI contract](REQUIREMENTS.md#kpi-contract).

## 3. What industry evidence actually supports

| Documented organization/research | Decision and method | Evidence classification and lesson for Warehouse Lab |
|---|---|---|
| DHL / Tetra Pak, Singapore | DHL describes a real-time IoT/data representation used by supervisors for congestion, workload and resource planning | **R, operator press release, 2019; self-reported deployment, no independently audited savings.** Live observations and operational integration distinguish this workflow from a static sandbox. [DHL announcement](https://group.dhl.com/en/media-relations/press-releases/2019/dhl-supply-chain-partners-tetra-pak-implement-first-digital-twin-warehouse-asia-pacific.html). |
| DHL Supply Chain, wave-release study | Simulation compared original and dynamic release processes across outbound stages | **R, software-vendor case based on a DHL conference presentation, 2021.** Reported cycle/resource benefits are model/case claims, not a transferable labor-reduction promise. It illustrates why work release and downstream constraints must be modeled together. [AnyLogic case](https://www.anylogic.com/resources/case-studies/optimizing-e-commerce-warehouse-operations/). |
| Browns Shoes / SimWell | Growth prompted evaluation of picking stations, conveyor loops, decant/packing equipment and additional system lanes | **R, vendor-hosted integrator case, conference 2023.** The description includes conveyor blocking and recovery; it documents alternatives to simply adding storage/robots, not independently measured ROI. [Case study](https://www.anylogic.com/resources/case-studies/increasing-the-efficiency-of-an-automated-warehouse-system-to-meet-demand/). |
| MOSIMTEC / DCS, unnamed pet-supply client | Preconstruction simulation of AMRs, gantries, wrapping and slotting against an operating window | **R, vendor/integrator case, conference 2024; client identity not independently established.** Vendor reports roughly 30% fewer required AMRs than the initial design estimate. This is a design-estimate claim, not verified realized savings. [Case study](https://www.anylogic.com/resources/case-studies/warehouse-modeling-designing-an-automated-distribution-center-with-simulation/). |
| Canadian shoe manufacturer, de Assis et al. | Research on routes in random storage with mixed product types per location, using WMS-derived data | **R, peer-reviewed IEEE Access article (2024), institutional abstract inspected.** Supports the relevance of picking-route questions; it does not validate this project's AMR abstraction or establish a named customer. [ÉTS publication record](https://pure.etsmtl.ca/en/publications/optimising-warehouse-order-picking-real-case-application-in-the-s/). |
| Two warehouse case studies, 2019 | Integrated layout, allocation, strategy and routing evaluation implemented in Excel | **R, Computers & Industrial Engineering publisher abstract; full text inaccessible in this review.** A direct counterexample to assuming a sophisticated 3D workspace is necessary. No numerical benefit imported here. [Article abstract](https://www.sciencedirect.com/science/article/pii/S0360835219304942). |
| Amazon middle-mile network | Company researchers describe optimization and scenarios for consolidation/routing under demand uncertainty | **R, company technical account, 2026; self-reported use.** This is an interfacility graph/flow decision, distinct from aisle-level operations. It does not show that geographic labels belong in Warehouse Lab. [Amazon Science](https://www.amazon.science/blog/navigating-uncertainty-in-amazons-middle-mile-network). |
| ARAUCO / Aleph5 | Optimization of production/distribution plans using demand, facilities, costs and business rules | **R, solver-vendor case; self-reported deployment.** Illustrates a planning system integrating operational data and scenarios; not evidence for internal robot simulation or for facility-opening benefits. [Gurobi case](https://www.gurobi.com/resources/case-studies/arauco-supply-chain-planning-optimization). |

Two methodological sources refine the opportunity. Queueing-network research estimates throughput, cycle times and utilization for robots carrying pods to workstations; an analytical model may be sufficient before detailed simulation. Its system architecture differs from Warehouse Lab's unit-picking robots. [Lamballais Tessensohn, Roy & de Koster, 2017](https://pure.eur.nl/en/publications/estimating-performance-in-a-robotic-mobile-fulfillment-system/). Georgia Tech's slotting method combines SKU/storage geometry with picking and replenishment labor, showing why pick distance alone is not an economic objective. [Warehouse Science](https://www.warehouse-science.com/apps/forward/cartons/).

These sources establish that organizations study these decisions. They do not establish demand for **Warehouse Lab**, a market gap, or willingness to replace an existing tool. Academic work is independent of this project's implementation, but is not independent validation of vendor case outcomes.

## 4. Users, jobs and actual decision workflow

Candidate frequencies and role divisions are **A**, not observations from interviews. WMS planning procedures and documented cases inform the workflow hypotheses. In a small organization one person may fill several roles; the decision and approval responsibilities still differ.

| ID / user segment | Decision owned or influenced; trigger | Current workflow and alternatives | Information needed; frequency hypothesis; cost of error |
|---|---|---|---|
| U1 Industrial engineer / operations analyst | Diagnose picking performance; decide if re-slotting deserves testing. Trigger: missed dispatch, excess travel or conflicting policy results | Extract WMS order/inventory/location data → reconcile units and timestamps → Pareto/coverage/travel analysis → floor observation → propose matched comparison → review with ops. SQL, Excel, WMS, OR and consultant models | Matched stock/demand, route/task timestamps, reachable layout, replenishment and change constraints. Weekly diagnosis / monthly or seasonal policy review. Error: moves and disruption without removing the binding constraint. |
| U2 Demand / supply-chain analyst | Define growth/peak workload and whether a capacity study is needed. Trigger: promotion, customer win or forecast change | ERP/WMS history → forecast and mix analysis → peak-day/hour profiles → capacity worksheet → service review. SQL, BI, Excel and forecasting tools | Multiple years of arrivals, lines/units/order, promotions, cutoffs, inventory availability and forecast error. Monthly with seasonal planning; exceptions weekly. Error: overstaffing or missed peak commitments. |
| U3 Automation engineer / integrator | Influence robot/station count and bottleneck resolution. Trigger: new design, throughput shortfall or equipment quote | Requirements/specifications → cycle-time budget and queueing bounds → supplier model → calibrated simulation → design review/pilot. Queueing, OR, commercial simulators, supplier tools | Fleet capabilities, battery/recovery, station capacity, traffic rules, workload distributions, downtime and SLA. Project milestones plus quarterly growth review. Error: stranded equipment or inadequate capacity. |
| U4 Shift/operations manager, supported by labor planner | Allocate people/equipment and release work. Trigger: shift start, absence, backlog or conveyor failure | WMS/WES backlog + attendance → productivity standard × workload → assignments → live exceptions → handover. WMS/WES, labor system, spreadsheet and BI | Skills/availability, engineered or observed task times, breaks, priorities, due times, upstream/downstream backlog. Daily/intrashift. Error: overtime, imbalance, missed service and poor working conditions. |
| U5 Facilities / industrial engineering planner | Size storage/staging and decide whether expansion study is warranted. Trigger: SKU growth, overflow or lease event | Inventory/cube and peak-stock analysis → slot compatibility/aisle/staging requirements → CAD alternatives → flow check → facilities review. Excel, CAD, slotting tools, consultant DES | Item/package dimensions, rack limits, inventory trajectories, replenishment, docks and building constraints. Annual planning or infrequent capital projects. Error: costly space with insufficient usable positions or flow. |
| U6 Network strategy analyst | Recommend candidate sites and customer allocation. Trigger: expansion, acquisition, transport-cost/service change | Geocode actual demand/supply → cost/service matrix → capacitated network optimization → scenarios → site diligence. GIS, spreadsheet screening, mixed-integer optimization, planning systems | Candidate sites, OD volumes, rates, transit/service times, taxes/leases, capacity and resilience constraints. Annual review; major redesign episodic. Error: recurring freight and inventory costs plus locked-in property. |
| U7 Automation program manager | Assemble invest/defer/pilot business case. Trigger: budget cycle, vendor proposal or obsolescence | Baseline process and spend → alternatives/quotes → throughput and integration-risk assessment → finance review → staged pilot/acceptance. Excel financial model, integrator studies, commercial simulation | Avoidable costs, supported demand, lifecycle costs, installation ramp, outages, fallback and contract acceptance criteria. Project/budget cycle. Error: failed integration, sunk capital and missed service. |

U1 covers both storage allocation and bottleneck identification; these share a diagnosis workflow but are scored separately below. A heat map of arrivals is not a delay diagnosis; a claimed bottleneck requires persistent queues/blocked work, resource constraints and a counterfactual test.

| Use | Daily operational user | Analytical user | Hypothetical economic buyer / budget sponsor | Decision approver hypothesis | Appropriate home |
|---|---|---|---|---|---|
| Picking/slotting and bottleneck investigation | Supervisor/picking lead supplies context | U1 | Site operations manager / continuous-improvement budget | Site leader with WMS/domain owner; engineering review for changes | Analytical workspace plus decision memo; BI for monitoring |
| Demand/seasonal planning | Supervisor consumes workload plan | U2 with U1 | Operations planning lead | Site/regional operations leader | Planning worksheet/system and BI |
| Robot/station sizing | Fleet supervisor provides traces | U3 | Automation sponsor | Engineering + operations + capital committee/finance | Engineering simulation study, not live dispatch |
| Labor/equipment allocation | U4 | Labor planner / U1 | Site operations leader | Shift manager within delegated authority; HR/finance for staffing changes | WMS/WES/labor planning and dashboard |
| Facility sizing | Site manager supplies operating constraints | U5 | Regional operations / real estate sponsor | Capital committee + facilities specialists | Facilities planning/CAD and study deliverable |
| Network/location | Transport planner supplies lanes | U6 | Supply-chain strategy leader | Executive/finance/real-estate committee | Network planning/GIS/optimization system |
| Automation investment | Operations lead consumes ramp plan | U7 with U3/finance | Capital sponsor | Finance/capital committee and operations owner | Business case and integration/pilot review |

**Current actual users:** owner/researcher and portfolio reviewers. **Proposed primary professional audience:** warehouse IE/OR practitioners, automation solution-design engineers, and hiring reviewers for operations-focused AI PM roles. They can assess whether the project frames the right decision, chooses the simplest adequate method and communicates an evidence boundary. The operational roles above are potential users of an appropriately validated future study, not established users of this application.

### How the proposed primary case fits a workflow

1. An analyst receives a claim that one storage arrangement has higher throughput. Clarify the service unit, decision horizon and action under consideration.
2. Reconcile demand against SKU-level availability and geometry coverage. Show exclusions and failures alongside completions. A spreadsheet/SQL join can resolve this stage.
3. Review the existing simulator as a conditional process explanation. Ask which time-varying mechanism remains unanswered; do not infer a physical bottleneck from animation or utilization alone.
4. Present one memo: what the evidence says, what it cannot say, alternatives including doing nothing, and the smallest evidence acquisition that would change the next decision.
5. Only after owner-authorized scope and specialist review, consider a controlled study. Operational change or pilot approval would be a separate decision.

The **H** is that this package demonstrates useful analytical judgment to specialists. Validate that hypothesis with reviewer tasks in the [proposed evaluation updates](PROPOSED_CHARTER_AND_EVALUATION_UPDATES.md); downloading or viewing the visualization would not validate decision usefulness.

## 5. Alternatives and the burden of proving a reason to simulate

| Method | Good fit / documented capability | Limitation relevant to the decision | Reason to use Warehouse Lab instead, if any |
|---|---|---|---|
| Excel + SQL | Demand grouping, SKU coverage, ABC/affinity, cube/workload arithmetic, transparent financial assumptions; integrated picking analysis has been implemented in Excel [2019 abstract](https://www.sciencedirect.com/science/article/pii/S0360835219304942) | Static averages do not automatically represent interactions and queues; a spreadsheet can still implement sophisticated models | **No established advantage for these calculations.** Use simpler analysis for the primary supply-control check and demand secondary. Lab adds an inspectable process illustration. |
| BI dashboards | Historical trends, exceptions and recurring KPI review | Describes observed performance; counterfactual effects require a model or study beyond the chart | Lab is a research explanation of hypothetical mechanisms, not a replacement for live KPI monitoring. No adoption advantage demonstrated. |
| WMS | Records inventory/work and supports execution/planning; Dynamics documents demand-based slotting and replenishment work [slotting workflow](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/warehouse-slotting) and [workload capacity](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/schedule-workload-capacity) | Product-specific coverage; data quality and calibration still matter; transactional execution and offline experimentation have different goals | No reason to replace WMS. A future validated offline study could consume its exports, but no integration is present or authorized. |
| WES | Coordinates work release, labor and automation; Honeywell describes intelligent release and workstation orchestration [official capability description](https://automation.honeywell.com/us/en/support/warehouse-automation/resources/brochures/momentum-warehouse-execution-system) | Vendor capability claims are not measured results; real-time coordination needs live integration and reliable controls | Lab lacks this scope. A future offline model might test a proposal before execution, not serve as the WES. |
| OR / analytical models | Allocation, assignment, routing, shifts, queueing and network location; explicit objective/constraints. [Queueing research](https://pure.eur.nl/en/publications/estimating-performance-in-a-robotic-mobile-fulfillment-system/), [facility-location example](https://www.gurobi.com/resources/demos/facility-location-problem-demo) | Adequacy depends on assumptions; detailed blocking/dispatch interactions can become cumbersome | Prefer OR for network design and static allocations. Lab supplies an existing abstract behavior model, not an optimizer or proof of optimality. |
| Commercial simulation, e.g. AnyLogic | Detailed process/resource models and scenario studies as in Browns Shoes/MOSIMTEC cases above | Data collection, model building and validation still required; software capability does not establish field validity | Lab offers inspectable local source and a bounded portfolio narrative. No proven accuracy, cost-of-ownership or capability advantage over mature tools. |
| Digital twin platforms | Connected representation, operational state and lifecycle data; DHL/Tetra Pak provides an application example | Requires data integration, maintenance and intended-use validation; NIST emphasizes VVUQ and traceability [NIST program](https://www.nist.gov/programs-projects/digital-twins-advanced-manufacturing) | Current Lab is a static-data research simulation. There is no verified competitive differentiation as a digital twin. |

By use case: slotting starts with demand/geometry/replenishment analytics and OR; bottlenecks start with observed queues and cycle decomposition; fleet sizing starts with workload/cycle-time bounds; growth starts with history/forecast error; staffing starts with workload × measured standards; storage sizing starts with cube and compatibility; network planning starts with OD cost/service optimization; investment starts with alternatives and incremental cash flows. Detailed simulation is justified only when its additional mechanisms could change the decision. No use case earns it merely by having a 3D scene.

## 6. Business value: mechanism, not a savings claim

All mechanisms below are **A/H**, contingent on better evidence and a feasible intervention. Current measured economic benefits for Warehouse Lab: **none**. A simulated operational metric is an intermediate result; economic value needs an operational link, an implementable action and an avoidable cash-flow effect.

| Use case | Operating cost / labor and equipment utilization | Capacity / throughput / service levels | Capital expenditure / implementation risk / decision uncertainty |
|---|---|---|---|
| Picking diagnosis / bottlenecks | Direct investigation at the binding constraint; avoid interpreting busy robots as productive labor. Require activity/time and payroll mapping | Separate unserviceable demand, queues and travel; may identify recoverable flow, but terminal completion does not prove a deadline | Could prevent an irrelevant change study or premature equipment justification; no actual avoided purchase demonstrated |
| Storage allocation / slotting | Less travel may reduce task hours, offset by replenishment, move labor and compatibility constraints | Slot choice can change congestion, pick-face capacity and completion tails; highest occupancy need not yield best service | Often less capital than expansion, but move disruption and downstream constraints matter; equal SKU controls reduce false rankings |
| Fleet sizing | Balance robot availability against station/traffic delay; more fleet can increase blocking and costs | Estimate marginal fulfilled work within a service window, not just robot utilization | Compare increments against lifecycle cost; batteries, maintenance and supplier constraints are currently missing |
| Demand growth / seasonality | Match overtime, leased equipment and workload plans to credible scenarios | Identify headroom/overflow and late-order exposure under mix changes; total units alone are insufficient | Could defer or accelerate study of expansion; forecast uncertainty can dominate simulated precision |
| Labor/equipment allocation | Reduce imbalance/overtime only if shift/skills and payment constraints allow | Balance process stages and cutoffs; utilization alone is not a staffing target | Usually operating-budget choices; automation or staffing changes need specialist review and ramp/fallback evidence |
| Facility/storage sizing | Space, handling and replenishment trade off; rent is not the full facility cost | Physical positions/cube and flow capacity are separate; staging/docks may bind before storage | Avoid undersized/oversized designs; no justified area scaling or expansion recommendation from this model |
| Automation investment | Translate achievable task-hour changes into avoidable expense; include support/integration/ramp costs | Check end-to-end throughput and service under outages and peak load, not local equipment speed | Potentially large irreversible spend; compare do-nothing/process change/pilot/vendor alternatives and uncertainty |
| Facility/network location | Freight, inventory, handling and facility/labor costs vary jointly | Service reach, transport lead time and site capacity constrain allocation | Long-lived leases/builds and migration risk; requires a different model and data, not warehouse relabeling |

### Transparent hypothetical financial model

Illustration only, USD in an assumed common price year; no values are sourced from Warehouse Lab, a quote, or an actual employer. Suppose a separately validated manual-picking intervention saved 20 labor-seconds on each of 1,000,000 comparable annual lines:

- Gross task capacity released = `1,000,000 × 20 / 3,600 = 5,555.6 hours/year`.
- At assumed loaded cost `$30/hour` and **40% actually avoidable paid hours**, potential cash benefit = `$66,666.7/year`. The other 60% is capacity, not payroll savings.
- With `$20,000/year` incremental recurring cost, net = `$46,666.7/year`; at `$80,000` one-time cost, simple undiscounted payback is about `1.71 years`, ignoring tax, ramp and residual value.
- At 0% avoidability, net is `−$20,000/year`; at 100%, `$146,666.7/year`. At 10 seconds and 40%, net is `$13,333.3/year`. These ranges demonstrate dependence on assumptions, not a probabilistic confidence interval.

This example is **not** a conversion of robot travel savings into human savings. A decision-grade business case would separately estimate productive paid hours, task mix, shift coverage, downtime, retraining, relocation costs and avoidability. For robots use incremental equipment/support/energy costs and constrained output, not a human wage rate. Revenue should use contribution margin on genuinely additional sellable orders, with demand and downstream capacity checks; do not add it to labor savings for the same released capacity without accounting for the overlap.

General investment worksheet: `NPV = −initial cost + sum_t[(avoidable operating cost reduction + incremental contribution − incremental operating/ramp costs)/(1+r)^t]`. Discount rate, horizon, tax treatment and residual values are owner/finance inputs, absent here. No project NPV has been estimated.

### Value of information and a stopping rule

An analysis has value if it changes the action or clarifies that evidence is insufficient. With loss `L(action,state)`, expected information value is `min_a E[L(a,state)] − E_information[min_a E[L(a,state) | information]]`, before study cost. Probabilities and loss estimates must be elicited or observed; simulation output does not supply them automatically.

Illustration: an assumed `$500,000` avoidable loss with 20% probability has expected loss `$100,000`. If a study reduced the residual chance of that mistake to 8%, expected loss would be `$40,000`; gross information value `$60,000`, net `$35,000` for a `$25,000` study. These invented probabilities illustrate the arithmetic only. There is no evidence that Warehouse Lab could achieve that reduction. If the action is unchanged across credible scenarios, or a stock join resolves the uncertainty, a more detailed simulation may have little incremental value.

The current demonstrable contribution is **analytical risk control**: trace a misleading ranking to violated comparison conditions and specify what evidence could resolve it. Neither dollars saved nor actual prevention of a wrong decision has been observed.

## 7. Opportunity prioritization

### Explicit rubric

Scores are **analyst judgments, not empirical market measurements**. Each criterion uses 1–5; 2 and 4 are intermediate. Weighted score = `sum(weight × score / 5)`, maximum 100. Weights reflect a bounded professional portfolio, not a commercial market-entry objective.

| Code / criterion | Weight | 1 / 3 / 5 anchors |
|---|---:|---|
| P Problem importance | 10 | Minor inconvenience / operationally material / service or continuity critical |
| V Decision value | 10 | Little action sensitivity / meaningful choice / expensive or irreversible choice |
| D Evidence of demand for the decision class | 10 | Hypothesis only / one credible application or research case / multiple documented applications and workflow support |
| F Frequency | 5 | Capital-event only / monthly-seasonal / daily or weekly |
| Q Data availability/quality for this project | 15 | Critical inputs absent / conditional partial evidence / representative and decision-valid inputs |
| S Simulation suitability | 10 | Static analysis sufficient / useful for some residual questions / dynamic interactions central |
| I Business impact potential | 10 | Indirect/local / plausible material mechanism / potentially end-to-end service/capital effect |
| T Technical feasibility here | 10 | Different system/model required / substantial calibration/model work / present evidence can answer bounded research question |
| M Compatibility with frozen MVP | 10 | Unrelated model/new features / partial fit / achievable interpretation of retained evidence |
| R Portfolio relevance | 10 | Weak evidence of target skill / useful narrow example / clear business-method-governance reasoning |

Separate evidence grade: **E0** assertion only; **E1** method/documentation; **E2** documented case or original research application; **E3** multiple application types plus workflow evidence. This grades relevance of the *decision class*, not measured effect reliability. Every row has **E0 direct evidence of Warehouse Lab adoption**.

| Candidate | P | V | D | F | Q | S | I | T | M | R | /100 | External class evidence; basis / limiting reason |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Picking diagnosis before policy change | 4 | 4 | 4 | 4 | 3 | 3 | 4 | 5 | 5 | 5 | **81** | E3: picking research, DHL/Browns process cases, WMS workflows. Existing confounding/availability evidence supports a bounded diagnostic conclusion; physical diagnosis remains unvalidated. |
| Demand/peak workload characterization | 4 | 4 | 4 | 4 | 3 | 2 | 4 | 4 | 4 | 4 | **73** | E2: Browns growth case and capacity workflow. Source order mix useful; no full annual history; simulation often unnecessary. |
| Robot/station congestion research | 4 | 4 | 4 | 3 | 2 | 5 | 4 | 3 | 3 | 5 | **73** | E3: robot queueing research, MOSIMTEC/Browns cases. Dynamic fit; physical traces and station detail absent. |
| Storage-policy optimization / re-slotting | 4 | 4 | 5 | 3 | 2 | 4 | 4 | 2 | 3 | 5 | **71** | E3: WMS, academic and analytical slotting examples. Unequal inventory and missing replenishment/cube block a winner recommendation. |
| Robot fleet sizing for a real facility | 4 | 5 | 4 | 2 | 1 | 5 | 5 | 2 | 2 | 4 | **67** | E2: MOSIMTEC and robot performance research. High value, low data fit; no calibrated fleet model or procurement authority. |
| Automation investment planning | 5 | 5 | 4 | 1 | 1 | 4 | 5 | 1 | 1 | 4 | **62** | E2: Browns/MOSIMTEC cases. Missing lifecycle cost, manual baseline, integration and downtime; attractive problem, unsuitable current decision support. |
| Labor/equipment shift allocation | 5 | 4 | 4 | 5 | 1 | 3 | 4 | 1 | 1 | 3 | **58** | E2: WMS/WES workflows and DHL release case. Daily frequency cannot compensate for no human labor/shift model. |
| Facility/storage capacity sizing | 4 | 5 | 4 | 1 | 1 | 3 | 5 | 1 | 1 | 3 | **56** | E2: warehouse design cases, slotting geometry method. No usable cube, surveyed topology, inventory trajectories or modeled inbound/staging. |
| Facility location/network planning | 4 | 5 | 4 | 1 | 1 | 1 | 5 | 1 | 1 | 2 | **50** | E2: Amazon/ARAUCO applications, facility-location method. Different problem; OD/cost/service/candidate-site data absent. |

Scoring rationale: decision value reflects the consequence of a choice, while impact potential reflects its plausible mechanism; neither estimates dollars. Q and M deliberately penalize lack of fit even for important industry problems. D reflects documented activity, not buyer demand. P/V/I/R remain judgment-heavy and correlated, so totals are only a transparent discussion aid.

**Sensitivity:** moving the primary case's S from 3 to 1 reduces it to 77; it still leads under these weights. Increasing data quality's weight from 15 to 25 and reducing portfolio relevance from 10 to 0 yields scores 77/71/67 for the selected top three. Demand characterization and robot/station research tie at 73 in the base rubric; demand characterization is listed first because its initial analytical method is simpler and needs less calibration. Increasing the robot/station opportunity's Q, T and M by one each raises it to 80; combined with S=1 for the primary, it would lead. That change would require new evidence/authorization, not score editing. Do not interpret small point differences as validated precision.

### Selection and trade-offs

1. **Primary: picking diagnosis before a storage-policy change.** Strongest fit to retained evidence and professional judgment. Deliverable: a diagnostic decision memo separating inventory coverage, task mix, travel/queues and unknowns, with a justified decision to withhold or advance a controlled study. It may require no new simulation. Its limitation is modest operational ambition: no improvement effect is yet established.
2. **Secondary: workload characterization for growth/peak planning.** Examine lines, units, order composition and temporal coverage if later analysis is authorized. SQL/Excel are likely enough initially. Do not call partial 2023 records a demand forecast or annual seasonal model.
3. **Secondary: conditional robot/station congestion research.** Use the existing model as a conceptual instrument, then specify the observations needed to compare resource/release alternatives. Any new runs, controls, scenarios or model changes require separate authorization. This is not fleet sizing or a procurement recommendation.

Deprioritize operational slotting recommendations until equivalent inventory and geometry are resolved; real fleet sizing until capability/service/downtime calibration; daily staffing until task and human constraints exist; storage sizing until physical cube/inbound/staging are represented; automation ROI until a matched baseline and costs exist; network location because it needs a different model. High problem importance does not make the present data adequate.

## 8. Evidence to obtain before further development

These are proposed research activities, not claims of completed validation or requests sent to anyone:

| Priority | Question / evidence | How it could change the decision |
|---|---|---|
| 1 | Source/domain clarification of payload quantity versus size, carton/unit relationship, stock as-of date and order identity | Without this, modeled coverage is an assumption; it might be an encoding issue rather than an operations issue |
| 2 | Practitioner walkthrough of one recent picking-improvement decision: actual extracts, competing explanations, tools, action and approver | Could show that the proposed job is already served by a spreadsheet or WMS and does not need simulation |
| 3 | Surveyed paths/floors and timestamped release/pick/queue/delivery observations matched to stock | Determines whether any traffic/station mechanism can be validated for a bounded use |
| 4 | Representative workloads including peaks and actual dispatch/service requirements | Defines relevant outcomes and tests whether conclusions generalize beyond the regression prefix |
| 5 | Incremental cost/avoidability, implementation constraints and approval criteria | Converts a verified operational mechanism into a possible economic decision; needed only if a future operational business case is authorized |

For proposed practitioner discovery, sample contrasting roles: IE/analyst, supervisor, and automation/finance sponsor. Ask about a recent decision and its artifacts, not whether they “like” a 3D tool. Record disconfirming evidence, existing alternatives and missing access. Until conversations actually occur, all persona and adoption hypotheses remain untested. No outreach is authorized or performed by this report.

## 9. Source register and research limits

All external links in this report and its companion documents were researched on 2026-10-18. This register records what was inspected, rather than implying access to an entire study or independent verification of its results.

| Source | Inspected material / classification | Supported use and boundary |
|---|---|---|
| [Mendeley v1 dataset, 2024](https://data.mendeley.com/datasets/pf2w725pw3/1) | Publisher landing description; original data source | WMS origin, anonymization/randomization and intended research uses; broad publisher performance language does not override the actual local schema |
| [de Assis et al., IEEE Access, 2024](https://pure.etsmtl.ca/en/publications/optimising-warehouse-order-picking-real-case-application-in-the-s/) | University publication record/abstract | Real picking/routing research; no full-method audit or AMR validation here |
| [Integrated picking design, C&IE, 2019](https://www.sciencedirect.com/science/article/pii/S0360835219304942) | Publisher abstract surfaced in search; direct full-page fetch returned 403 | Excel-based method and two cases only; full text and benefit magnitude not reviewed |
| [Robot queueing research, EJOR, 2017](https://pure.eur.nl/en/publications/estimating-performance-in-a-robotic-mobile-fulfillment-system/) | University record/abstract | Analytical alternative; pods-to-person architecture differs from Lab |
| [Warehouse Science slotting](https://www.warehouse-science.com/apps/forward/cartons/) | Academic author's method page | Geometry plus picking/restocking trade-off; no software execution or runtime recommendation |
| [DHL/Tetra Pak, 2019](https://group.dhl.com/en/media-relations/press-releases/2019/dhl-supply-chain-partners-tetra-pak-implement-first-digital-twin-warehouse-asia-pacific.html) | Operator press release | Reported deployment/workflow, not audited benefits |
| [DHL wave-release case](https://www.anylogic.com/resources/case-studies/optimizing-e-commerce-warehouse-operations/), [Browns Shoes case](https://www.anylogic.com/resources/case-studies/increasing-the-efficiency-of-an-automated-warehouse-system-to-meet-demand/), [MOSIMTEC/DCS case](https://www.anylogic.com/resources/case-studies/warehouse-modeling-designing-an-automated-distribution-center-with-simulation/) | Vendor case pages, identifying conference presentations in 2021/2023/2024 | Documented scenario questions; outcomes remain vendor/integrator-reported and are not Lab targets |
| [Amazon Science, May 2026](https://www.amazon.science/blog/navigating-uncertainty-in-amazons-middle-mile-network), [ARAUCO/Gurobi](https://www.gurobi.com/resources/case-studies/arauco-supply-chain-planning-optimization) | Company technical account and solver case | Network/planning methods and workflows; not independent economic audits |
| [Dynamics slotting](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/warehouse-slotting), [capacity scheduling](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/schedule-workload-capacity), [Honeywell WES](https://automation.honeywell.com/us/en/support/warehouse-automation/resources/brochures/momentum-warehouse-execution-system) | Official software documentation/capability descriptions | Credible existing alternatives; no broad claim that every WMS/WES offers all features |
| [Gurobi facility-location demo](https://www.gurobi.com/resources/demos/facility-location-problem-demo) | Official model example | Static location cost trade-off; example is not customer validation |
| [NIST digital twins program](https://www.nist.gov/programs-projects/digital-twins-advanced-manufacturing), [NIST design selection](https://www.itl.nist.gov/div898/handbook/pri/section3/pri33.htm), [blocking](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm) | Government research/method guidance | Intended-use credibility and experimental design principles; no conformance/certification claim |
| [BLS fixed May 2024 metro wage tables](https://www.bls.gov/oes/2024/may/oessrcma.htm), [compensation concepts](https://www.bls.gov/opub/hom/ncs/concepts.htm) | Government tables/methods | Candidate wage/benefit proxies; fixed vintage used to avoid an unstable “current” alias, not claimed latest |
| [Census 2022 CFS tables](https://www.census.gov/data/tables/2022/econ/cfs/aff-2022.html), [CFS methods](https://www.census.gov/programs-surveys/cfs/technical-documentation/methodology.html), [retail seasonal-factor archive](https://www.census.gov/retail/mrts/historic_releases.html) | Government tables/methods/archive | Regional flows and aggregate seasonality context; no local demand validation |
| [Cushman & Wakefield, Salt Lake City Q3 2026](https://www.cushmanwakefield.com/en/united-states/insights/us-marketbeats/salt-lake-city-marketbeats/industrial) | Brokerage market page, asking rents/lease basis | Illustrative facility-cost proxy type; no Lab site, lease or negotiated cost |

The search-index BLS “current” result and fetched title disagreed on vintage; therefore no current wage amount is asserted. A CBRE search result redirected to a generic index and a national Cushman PDF fetch failed; neither supplies a numerical claim. No transportation routing API, market price series or proxy has been ingested, and no financial or new scenario output has been generated. Findings may change with source clarification or disconfirming practitioner evidence.

## 10. Executive recommendation

- **Primary user/audience:** an industrial engineer or warehouse operations analyst evaluating a picking-change proposal; the current actual audience remains the owner and specialized portfolio reviewers.
- **Decision:** whether a storage-policy improvement study is warranted and sufficiently controlled, before recommending a change or attributing poor outcomes to capacity.
- **Why investigate:** documented industry work involves consequential picking, release and equipment choices; the local evidence already exposes a realistic failure mode in reasoning—ranking policies with different feasible demand.
- **Role of simulation:** unnecessary for SKU-coverage arithmetic; potentially useful for residual timing, shared-resource and congestion questions. The present model is an explanatory research instrument, not validated operations decision support.
- **What data supports:** provenance/lineage, descriptive published demand/allocation relationships, assumed supply bounds, deterministic abstract behavior and identification of confounded comparisons.
- **Critical missing evidence:** authoritative stock/size/unit/date semantics, surveyed topology, matched observed process times, representative demand/service requirements, practitioner decision artifacts and avoidable costs.
- **Realistic demonstrated value:** show why a recommendation should be withheld, identify cheaper adequate analysis, and make the next evidence request explicit. No measured operational savings, customer validation or ROI can be claimed.
- **Next:** owner reviews the proposed research focus and [charter/evaluation amendments](PROPOSED_CHARTER_AND_EVALUATION_UPDATES.md), then chooses whether to authorize source clarification, practitioner review and a bounded analytical study. Preserve the MVP and G0–G4 PENDING; no new controls, model changes or gate approvals follow from this report.
