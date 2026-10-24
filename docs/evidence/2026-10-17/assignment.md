# Warehouse Lab: AI Product Management, Evaluation & Governance

Act as a Senior AI Product Manager, Technical Program Manager, Operations Research Analyst, and Independent Quality Reviewer.

We have already implemented Warehouse Lab, a real-data-grounded warehouse simulation using Three.js, historical warehouse records, and 10 autonomous mobile robots.

**This is a governance, documentation, evaluation, and quality-improvement assignment. The MVP feature scope is frozen.**

Do not redesign the application, add dashboard modules, introduce new AI capabilities, or expand the simulation's functional scope.

## Objective

Establish a rigorous, evidence-driven internal product development process for Warehouse Lab.

Apply relevant principles from:

- AI Product Management
- DMAIC and continuous process improvement
- NIST AI Risk Management Framework
- Simulation Verification and Validation
- Experimental Design
- Product Quality Assurance
- Engineering Decision Management

These methodologies should be internalized into how the project is developed, evaluated, reviewed, and approved.

They are not additional user-facing product features.

## Step 1: Audit the Current Project

Inspect the existing repository, implementation, data pipelines, tests, README, and `data-audit.md`.

Evaluate the current state against the project's intended purpose.

Pay particular attention to:

- Business problem definition and evidence
- Requirements and scope clarity
- Data provenance and integrity
- Ambiguous stock quantity interpretations
- Warehouse geometry and coordinate calibration
- Differences between storage-policy datasets
- Order and inventory accounting
- Simulation assumptions
- Reproducibility
- Routing and collision avoidance
- KPI definitions and correctness
- Validity of comparative experiments
- Limitations of business conclusions

Do not assume that passing tests establishes operational validity.

Classify findings by severity, impact, confidence, and required corrective action.

## Step 2: Establish Stage Gates

Create formal approval criteria for:

G0: Problem Definition  
G1: Data Readiness  
G2: Model Verification and Validation  
G3: Experiment Readiness  
G4: Decision Readiness

For each gate, define:

Purpose, required inputs, deliverables, evaluation methods, measurable exit criteria, evidence requirements, responsible reviewer, blocking conditions, and approval procedure.

Use three possible outcomes:

APPROVED  
CONDITIONALLY APPROVED  
BLOCKED

The AI may recommend a decision, but must never fabricate human approval or independently sign off on its own work.

Any unreviewed gate must remain pending.

## Step 3: Create Core Documentation

Create or update the following documents, reusing existing work wherever possible:

`docs/PROJECT_CHARTER.md`  
`docs/REQUIREMENTS.md`  
`docs/DATA_CARD.md`  
`docs/MODEL_CARD.md`  
`docs/EVALUATION_PLAN.md`  
`docs/RISK_AND_DECISION_LOG.md`  
`docs/GATE_REVIEWS.md`

Make documents concise, professional, and evidence-driven.

Every factual claim must reference a source file, experiment, test result, or clearly identified assumption.

Record document owner, version, status, and review requirements.

Avoid generic templates filled with speculative content.

## Step 4: Define an Evaluation Protocol

Establish an evaluation contract for every critical capability and claim.

Each evaluation should record:

Evaluation ID  
Claim being tested  
Data or scenario used  
Ground truth or reference baseline  
Test procedure  
Metric and proposed threshold  
Actual result  
Evidence location  
Limitations  
Reviewer  
Pass / Fail / Inconclusive status

Cover at minimum:

Data ingestion accuracy, inventory conservation, routing validity, collision avoidance, deterministic replay, order completion accounting, KPI correctness, experiment fairness, sensitivity to assumptions, and claim traceability.

Use quantitative acceptance thresholds whenever scientifically justified.

Where no defensible threshold exists, explain the missing evidence and propose a method for establishing one.

Do not invent empirical benchmark values.

## Step 5: Review Existing Findings and Correctness

Prioritize known issues documented in the data audit.

Investigate their causes and evaluate their effects on model validity.

Determine which issues can be corrected using existing source data.

Where necessary, make narrowly scoped fixes to existing data-processing logic, tests, or simulation calculations.

Do not introduce new product features.

For each correction, document:

Previous behavior  
Root cause  
Evidence  
Change made  
Validation performed  
Remaining limitations

Preserve original raw data.

Do not silently reinterpret ambiguous data.

## Step 6: Evaluate Experiment Credibility

Assess whether existing Random, Class-Based, Dedicated, and Hybrid scenarios constitute fair comparisons.

Check inventory equivalence, SKU coverage, order-demand consistency, geometry coverage, fixed simulation parameters, and random-seed reproducibility.

Distinguish:

Descriptive findings based on published records  
Derived analytical measures  
Hypothetical simulation outcomes  
Experimentally supported comparisons  
Claims requiring real-world validation

If a comparison fails necessary controls, mark it INCONCLUSIVE or BLOCKED and explain why.

## Step 7: Internalize AI PM Practices

Create a short internal reference explaining key concepts and how they apply to this specific project.

Cover PRD, acceptance criteria, KPIs, guardrail metrics, data contracts, provenance, evals, golden datasets, baselines, verification, validation, reproducibility, sensitivity analysis, confounders, risk management, decision records, human approval, and stage-gate governance.

Separate currently applicable practices from concepts relevant only to potential future AI features.

Do not turn this reference into additional application functionality.

## Step 8: Final Quality Review

Run the existing automated tests, data integrity checks, and production build.

Add focused regression tests only where they validate an existing requirement or correct a discovered deficiency.

Do not mark a gate approved merely because tests pass.

Generate a final internal review report containing:

Current project maturity  
Verified strengths  
Critical issues  
Open questions  
Evidence gaps  
Recommended gate status  
Approved scope of continued work  
Next corrective actions requiring approval

Keep all original features operational.

## Execution Rules

Begin with inspection and assessment.

Preserve the current MVP.

Prioritize correctness, traceability, and defensible decision-making.

Do not fabricate findings, approvals, validation results, or real-world business impact.

Keep technical quality assurance separate from business-model validity.

Complete the documentation and safe corrections that can be supported with current evidence.

Escalate unresolved methodological or business decisions for my review.

At the end, summarize what changed, what was verified, what remains uncertain, and which approvals are needed from me.

Do not claim the governance process is complete until the required evidence exists.