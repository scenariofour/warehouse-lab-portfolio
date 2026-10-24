# Risk, findings, corrections and decisions

Owner: project owner; independent data/QA/OR reviewers unassigned. Author: AI assistant.  
Version: 0.2.0 · 2026-10-17. Status: DRAFT — PENDING HUMAN REVIEW.  
Review requirements: owner assigns reviewers, accepts residual risks only for a named use, and records decisions in GATE_REVIEWS. Fix implementation is not human acceptance.

Severity is about consequence within the stated use: **Critical** prevents a defensible operational/business conclusion; **High** threatens source integrity, model/accounting contracts or governance authority; **Medium** limits evidence quality or generalization. Confidence refers to evidence for the finding, not certainty about unknown warehouse facts. No numerical probability or invented risk-priority score is assigned.

## Findings register

| ID | Severity; impact; confidence | Finding and cause | Required action / current treatment | Evidence; gate; responsible role |
|---|---|---|---|---|
| F-01 | High; purpose/ROI; high confidence in evidence gap | User intent is documented, but no economic problem baseline, buyer research or decision loss function is supplied | D-01 direction confirmed; formal G0 review of proposed criteria and reviewer appointments remains pending; no savings/ROI assertion | E-01/E-11; G0/G4; project owner |
| F-02 | Critical; stock/service conclusions; high confidence in ambiguity | README quantity label conflicts with size-like tokens; one carton per cell and size interpretation are assumptions; inventory as-of date unknown | Retain explicit model, obtain source-domain clarification before real stock claims; no silent reinterpretation | E-02, DATA_CARD; G1–G4; data steward/domain reviewer |
| F-03 | Critical; routing/time/capacity; high confidence in mismatch | Meter labels vs notebook floors; assumed 0.1 calibration and stacked-tier display; no physical inter-floor service model | Obtain surveyed units/topology and feasible picking constraints; current model stays an abstraction | Source README/notebook; MODEL_CARD; G1/G2/G4; domain/OR reviewer |
| F-04 | Critical; comparative decisions; high | Equal totals hide unequal SKU-level supply and geometry exclusions; feasible demand differs by policy | Mark causal effect INCONCLUSIVE; require common-inventory/control protocol before ranking | E-02/E-05, EXPERIMENT_CREDIBILITY; G3/G4; OR reviewer |
| F-05 | High; customer-throughput meaning; high | 4,024 customer order numbers occur in multiple waves; engine counts 39,858 wave/order groups vs 32,634 numbers | Owner/WMS reviewer defines decision unit; retain current grouping and label its interpretation in internal contracts | E-02; G0/G1/G4; business/data reviewer |
| F-06 | High; raw preservation; high/reproduced | ZIP extraction wrote directly over existing files before hash rejection | C-01 implemented: validate first; never replace preserved conflicting bytes; review regression and raw hashes | E-03/E-07; G1; data steward |
| F-07 | High; routing API validity; high/reproduced | Identical start/goal returned empty route before checking blocked/invalid endpoints; coordinate overflow could alias a valid index | C-02 implemented: index/endpoint guards, no default-run output change; independent review pending | E-03/E-04/E-06; G2; routing reviewer |
| F-08 | Medium; evidence provenance; high | Scenario report hardcoded 2026-10-15 and omitted input/code identity | C-03 implemented: execution date/UTC timestamp and input/code hashes; retain prior report as historical evidence | E-01/E-05; G2/G3; QA reviewer |
| F-09 | Medium; reproducibility/statistics; high | Seed is a priority offset modulo robot count, not random allocation/demand;42 and 52 are aliases | Do not treat aliases or repeated deterministic runs as independent replications; design workload blocks before inference | E-04, Simulation.step; G3; OR reviewer |
| F-10 | High; generalization; high | Source prefix is not chronological/random; no replenishment; full 228,195-unit history is not aligned with an inventory snapshot | Restrict tested envelope; do not call full-history mode a historical replay; request workload/snapshot rationale | E-02/E-04; G2–G4; domain reviewer |
| F-11 | High; ingestion semantics; high | Missing sizes, 2,559 repeated customer rows, unmatched geometry and 109 Class-Based references lack authoritative resolution | Preserve source exceptions; no unsupported deduplication/imputation or guessed geometry | E-02; G1/G3; data steward |
| F-12 | Medium; timing/audit completeness; high | Step-quantized service/event clock, parking-based horizon, and 20,000-event retention limit | Require complete log for event oracles; state denominator/quantization; define decision-relevant tolerance with reviewers | E-04, Simulation.emit/step; G2–G4; simulation reviewer |
| F-13 | High; approval credibility; high | Author/executor is the AI that also contributed implementation; independent reviewer roles are not staffed | Every human gate remains PENDING, no signatures/approvals fabricated; request role appointments | GATE_REVIEWS, assignment; all gates; project owner |

## Supported corrections

### C-01 — preserve source bytes on rejected import

- **Previous behavior / root cause:** `prepare_data.py` flattened ZIP members directly into `data/raw` before verifying hashes. A malformed Product.csv replaced the preserved file even though conversion then failed.
- **Evidence:** isolated pre-fix regression fails with changed bytes; E-03 `before-import-regression.log`. The actual published raw files were not used as mutation fixtures.
- **Change:** `import_source_zip.py` checks recognized member hashes, duplicate basenames and existing conflicting bytes before any import; existing identical files are skipped. Downloads are staged and hash-checked before insertion. Version/hash failures no longer rely on Python `assert` being enabled.
- **Validation:** five temporary-directory fixtures pass; all 21 actual raw hashes rechecked; normalized arrays remain unchanged. E-07/E-02 and E-10 correction-impact evidence.
- **Remaining limits:** provider stock/geometry semantics remain unresolved. This is not a comprehensive archive-security certification or a multi-file filesystem transaction across disk failures.

### C-02 — reject invalid route endpoints

- **Previous behavior / root cause:** `Grid.path(blocked,blocked)` returned `[]`; endpoints were not both validated. `Grid.at` could encode an out-of-bounds coordinate as another row's index.
- **Evidence:** pre-fix test reports `[] !== null`; E-03 `before-routing-regression.log`.
- **Change:** validate coordinate/index bounds and both free/reachable endpoints before empty-route handling; invalid neighbor requests return no neighbors.
- **Validation:** focused regression,39 independent BFS comparisons, existing lifecycle/collision tests and all four default scenario runs pass. Default numerical outcomes match the pre-fix baseline; E-04/E-05/E-06/E-10.
- **Remaining limits:** correct routing over the assumed grid does not validate real geometry, floor access, robot safety or global dispatch optimality.

### C-03 — make scenario evidence attributable

- **Previous behavior / root cause:** a new run still wrote the original hardcoded validation date; report lacked source/code fingerprints.
- **Evidence:** captured baseline runner and prior report in E-01; new execution log identified the mismatch.
- **Change:** report actual New York execution date, UTC timestamp, and SHA-256 hashes for geometry/default demand, policy inputs and engine/grid/config source.
- **Validation:** fresh report has 2026-10-17 execution identity and actual hashes; prior report retained in `evidence/2026-10-17/prior/`. E-05.
- **Remaining limits:** timestamps and hashes provide identity, not independent review, external validity or cryptographically authenticated human approval.

No stock/size/grouping/scale/topology rule or KPI formula was changed. Existing UI and scene sources remain unchanged. [Correction impact](evidence/2026-10-17/correction-impact.json).

## Decision records — direction confirmed, formal gates pending

| ID / status | Context and options | AI recommendation and consequence | Required human disposition |
|---|---|---|---|
| D-01 — OWNER-CONFIRMED DIRECTION | End-to-end operations research is the primary objective; AI PM/TPM governs; analytics/OR/simulation provide methods | Educational/portfolio use only; current application is a research instrument; no deployment, procurement, productivity or ROI claims | Intended use confirmed by requester; formal G0 review, proposed criteria ratification and reviewer appointments remain pending |
| D-02 — PROPOSED; existing rules retained | Interpret payload as quantity, size/carton slots, or obtain source clarification; source is contradictory | Do not adopt a new interpretation during this review; preserve current inputs and disclose uncertainty | Data-domain owner resolves semantics and snapshot timing at G1 |
| D-03 — PROPOSED | Compare published unequal allocations descriptively, or create separately labeled controlled common-inventory treatments | Current ranking is INCONCLUSIVE; a controlled remapping needs explicit approval and a new protocol | Owner + OR reviewer decide estimand, inventory and workload controls at G3 |
| D-04 — PROPOSED | Aggregate across waves as customer orders, or retain wave/order task groups | Retain current computational unit; clarify internal throughput meaning; no unsupported regrouping | WMS/business reviewer decides reporting unit and treatment of repeated rows |
| D-05 — PROPOSED | Accept a numerical/model validity tolerance, or defer until reference evidence exists | Keep numeric roundoff tolerances for QA; do not invent field-accuracy or business thresholds | Owner/domain reviewer sets decision-specific criteria at G2/G4 |

### D-01 — owner-confirmed intended-use direction

**Status:** OWNER-CONFIRMED DIRECTION, recorded 2026-10-17 from the project owner's current chat instruction. This supersedes D-01's prior PROPOSED intended-use wording only. **G0–G4 remain PENDING; no formal gate decision, signature or independent validation is recorded.** [Owner evidence](evidence/2026-10-17-g0-direction/owner-confirmation.md), [prior decision record](evidence/2026-10-17-g0-direction/prior-documents/RISK_AND_DECISION_LOG.md).

**Context and alternatives:** the earlier record proposed an inspectable sandbox and left project purpose unconfirmed. The owner has now selected an evidence-driven operations improvement research project. A simulation-feature-led objective and an operational deployment/procurement project are outside that confirmed direction; no comparative scoring of alternatives was performed.

**Decision and rationale:** **A** is primary: demonstrate discovery, diagnosis, hypotheses, controlled experimentation and conditional recommendations. **C** is internal governance: AI Product Management and Technical Program Management practices manage requirements, evidence, evaluation, risk and human decisions without adding UI features. **B** is method: real-data analytics, operations research, optimization and simulation investigate operational questions; Three.js communicates processes/findings. Technical verification stays separate from operational-model validation. This hierarchy follows the owner's instruction, not an AI inference of proven warehouse problems.

**Intended use and consequences:** educational and portfolio-oriented, evidence-grounded warehouse operations research. The current Three.js/10-robot application remains intact as an instrument. Research may find no improvement, an invalid comparison or insufficient evidence. Conditional research recommendations must disclose evidence and uncertainty. This direction does not authorize real-world deployment, equipment procurement recommendations, productivity guarantees or ROI claims. It does not validate stock, geometry, causal effects or economic benefit, or approve D-02–05.

**Authority and next review:** the requester/project owner is the source of this intended-use confirmation; the AI records it and cannot sign as an independent reviewer. The current task authorizes documentation alignment and checks only. Formal G0 still requires review of the revised charter, proposed success/guardrail criteria, named reviewer appointments and a gate record under [the procedure](GATE_REVIEWS.md). No reviewer identity, decision date, signature, accepted evidence snapshot or gate outcome is filled in by this confirmation. [Charter](PROJECT_CHARTER.md), [G0 readiness](G0_READINESS_ASSESSMENT.md).

Review cadence proposal: inspect open findings at every data/model/claim change and before a gate decision. Reopen affected gates if their evidence hashes, approved use, assumptions or criteria change. This proposal creates no scheduled automation and no approval by itself.
