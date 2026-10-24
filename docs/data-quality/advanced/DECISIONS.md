# Business decision evidence and experiment readiness

Current assessment: **withhold operational storage-policy recommendations and controlled placement-effect claims**. Arithmetic can guide clarification; it cannot authenticate source semantics, identify real service failures or measure savings. All 14 issue reviews and G0–G4 remain PENDING. No approved corrections exist.

## Issue-level decision layer

The following is generated from the public issue-decision table; AI-proposed interpretation requires independent human/domain review. Each item is one investigation question, not an additive business-loss estimate.

### DQ-RECON-001 — Demand/picking quantity reconciliation gap

Decision: Define eligible requested work before diagnosing fulfillment. KPI/assumption at risk: Eligible requested-work / service numerator.

Mechanism: A mismatched baseline can misattribute extract differences to capacity or slotting. Competing explanations: Cancellation or backlog | Extract timing/scope | Size encoding or missing master data.

Readiness: `ARITHMETIC_REPRODUCIBLE_SEMANTICS_PENDING`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **One wave with line statuses, cancellations and aligned extraction times.**

### DQ-LOC-001 — Picking locations lack matched coordinates

Decision: Establish spatial coverage before a route or travel claim. KPI/assumption at risk: Spatial workload coverage.

Mechanism: Dropping unmapped workload can bias a travel estimate. Competing explanations: Non-storage process locations | Different extract coverage | Incomplete location master.

Readiness: `ARITHMETIC_REPRODUCIBLE_SEMANTICS_PENDING`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **Location-master record and process meaning for the largest unmatched location pseudonym.**

### DQ-ABC-001 — Published versus extract-volume ABC disagreement

Decision: Confirm classification objective before choosing fast movers. KPI/assumption at risk: Fast-mover study population.

Mechanism: Changing classification basis changes which references receive priority. Competing explanations: ABC based on value/margin | Different effective period | Anonymization.

Readiness: `ARITHMETIC_REPRODUCIBLE_SEMANTICS_PENDING`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **ABC basis, effective date and one worked source classification.**

### DQ-EXP-001 — Unequal SKU inventory across published storage policies

Decision: Defer a causal policy ranking until common SKU quantities and eligible work are approved. KPI/assumption at risk: Placement-effect isolation.

Mechanism: Unequal SKU quantities confound availability/task mix with placement. Competing explanations: Different SKU composition | Published allocation construction | Unequal coordinate exclusions.

Readiness: `ARITHMETIC_REPRODUCIBLE_SEMANTICS_PENDING`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **An approved common SKU-quantity ledger and eligibility definition for one controlled comparison.**

### DQ-STOCK-001 — Stock payload units and snapshot alignment unresolved

Decision: Obtain quantity/UOM and stock-date definitions before availability or replenishment conclusions. KPI/assumption at risk: Availability and replenishment assumptions.

Mechanism: Payload/UOM or timing errors change conditional stock arithmetic. Competing explanations: Size-like allocation payload | Unknown snapshot date | Unknown carton/unit meaning.

Readiness: `SOURCE_DEFINITION_REQUIRED_UNMEASURED`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **A decoded allocation cell with UOM and snapshot timestamp.**

### DQ-LAYOUT-001 — Physical scale and floor connectivity unresolved

Decision: Obtain surveyed scale, origins and floor connectivity before route/capacity claims. KPI/assumption at risk: Distance and accessibility assumptions.

Mechanism: Unknown scale/floor access changes route feasibility and distance meaning. Competing explanations: Coordinate-scale convention | Separate physical floors | Unrecorded transfer/access rules.

Readiness: `SOURCE_DEFINITION_REQUIRED_UNMEASURED`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **One surveyed aisle segment and documented Z-to-floor/transfer mapping.**

### DQ-DUP-CUSTOMER — Exact repeated Customer_Order records retained

Decision: Clarify transaction granularity before any deletion. KPI/assumption at risk: Demand quantity baseline.

Mechanism: Removing legitimate repeated lines understates requested work. Competing explanations: Legitimate repeated lines | One-unit picking expansion | Extract duplication.

Readiness: `ARITHMETIC_REPRODUCIBLE_SEMANTICS_PENDING`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **Line event identifiers or source-owner explanation for one exact repeat pair.**

### DQ-DUP-PICKING — Exact repeated Picking_Wave records retained

Decision: Clarify transaction granularity before any deletion. KPI/assumption at risk: Published picking quantity baseline.

Mechanism: Removing unit-expanded repeats can erase legitimate units. Competing explanations: Legitimate repeated lines | One-unit picking expansion | Extract duplication.

Readiness: `ARITHMETIC_REPRODUCIBLE_SEMANTICS_PENDING`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **One pick-event identifier and explanation of one-unit record expansion.**

### DQ-SIZE-001 — Existing inferred customer half-size mapping

Decision: Seek source size dictionary before treating matching as authenticated. KPI/assumption at risk: SKU matching and eligibility.

Mechanism: Half-token interpretation changes joins and matching quantity. Competing explanations: Implied decimal in customer encoding | Other size-system meaning.

Readiness: `ARITHMETIC_REPRODUCIBLE_SEMANTICS_PENDING`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **Authoritative size codebook with one 105/10.5 example.**

### DQ-SIZE-002 — Missing customer sizes retained

Decision: Clarify SKU identity for eligibility. KPI/assumption at risk: Known-size eligible work.

Mechanism: Imputation would assign unsupported SKU identity to unknown demand. Competing explanations: Omitted value | Source-specific unspecified size.

Readiness: `ARITHMETIC_REPRODUCIBLE_SEMANTICS_PENDING`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **Size field for one missing-size source record or explanation of intentional absence.**

### DQ-QTY-001 — Zero-quantity customer records retained

Decision: Define eligible lines and group denominators. KPI/assumption at risk: Positive-work versus record/group denominators.

Mechanism: Counting placeholders as work changes task statistics. Competing explanations: Canceled line | Placeholder | Extract convention.

Readiness: `ARITHMETIC_REPRODUCIBLE_SEMANTICS_PENDING`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **Lifecycle meaning for one zero-quantity line.**

### DQ-LOC-002 — Allocation cells excluded from geometry-dependent analysis

Decision: Clarify location master coverage before comparing eligible placements. KPI/assumption at risk: Comparable geometry-retained placement population.

Mechanism: Unequal exclusions change which cells enter policy comparisons. Competing explanations: Different location master version | Locations outside coordinate scope.

Readiness: `ARITHMETIC_REPRODUCIBLE_SEMANTICS_PENDING`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **Coordinate-master version and one excluded allocation location mapping.**

### DQ-MASTER-001 — Allocation references absent from published product master

Decision: Confirm active assortment/master coverage. KPI/assumption at risk: Active assortment/master eligibility.

Mechanism: Master scope mismatch changes eligible inventory and ABC interpretation. Competing explanations: Different master scope | Allocation construction or anonymization.

Readiness: `ARITHMETIC_REPRODUCIBLE_SEMANTICS_PENDING`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **Master-effective-date and mapping for one unmatched allocation reference.**

### DQ-ID-001 — Order numbers reused across waves; business identity unresolved

Decision: Agree customer service identity and throughput denominator. KPI/assumption at risk: Customer-order versus wave/order throughput.

Mechanism: Split-wave identity changes the denominator and completion definition. Competing explanations: Legitimate split waves | Order-number scope convention.

Readiness: `ARITHMETIC_REPRODUCIBLE_SEMANTICS_PENDING`. Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.

Smallest next evidence request: **WMS business key and completion rule for one order spanning two waves.**

## Controlled storage-policy experimentation

All six policy pairs fail equality of retained reference/size quantities, despite equal 41,256-cell retained totals. Unequal exclusions also fail common raw-to-coordinate coverage. Equal totals are a descriptive PASS only. Payload/UOM, stock dates/receipts, physical scale/floor transfers, representative task mix and observed service baseline remain unverified or unmeasured. No independent controlled protocol is approved. Therefore placement effects are not identifiable from these policy files. Do not divide unequal-workload simulated outputs by deliveries and call the result causal.

The smallest experiment-preparation request is a source-owner decoded cell with UOM/date plus a common-SKU quantity ledger for one proposed comparison. These unblock meaning/eligibility review; they do not by themselves authorize an experiment. Before any study, a named industrial-engineering/domain reviewer must approve common SKU quantities, eligible task mix, demand horizon/receipts, surveyed geometry/access constraints, measurement definitions, representative workload, repeatability/seeds where relevant, acceptance/stop criteria and independent review. Predeclare comparison direction and denominators before evaluating outcomes.

Potential future study metrics include travel in verified units per common eligible unit, completion time distribution, eligible-work completion and failed-task reasons under a fixed protocol. All are proposed metrics; none is measured here. No real costs, savings, operational failure rates or causal improvements are claimed.

## Separate future proposal boundary

This assignment creates no synthetic inventory scenarios. A future common-stock experiment would require separate authorization and a versioned protocol; no such fixtures, simulator edits or inventory rescaling are included. Existing design-only proposals remain unchanged. Current work stops at a traceable evidence request and explicit withholding reason.

## AI Product Management acceptance

Automated acceptance checks cover arithmetic, keys, public field boundaries, reproducibility and preservation. Human acceptance is separate: a named reviewer must correctly identify the population/denominator, evidence class, competing explanation, missing decision prerequisite and smallest next request on each of the three blueprint journeys (proposed 15/15, zero false correction/causal claims). A second reviewer checks all 14 decision relationships for source support. Record actual reviewer names, date, artifact hashes, responses and changes requested in a new review artifact. No reviewer or result is prefilled; Tableau is read-only evidence navigation, not an approval workflow.
