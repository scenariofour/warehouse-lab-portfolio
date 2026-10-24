# DQ foundation — risk and decision register

2026-10-18. AI-authored proposals and execution records; no independent human approval. Roles below are proposed and unassigned. G0–G4 PENDING. This register supplements, without changing, prior governance.

| Risk / priority / status | Evidence and decision consequence | Mitigation / closure evidence / proposed owner |
|---|---|---|
| DQ-R01 Semantic uncertainty / HIGH / OPEN | DQ-SIZE-001, STOCK-001, LAYOUT-001; size, quantity, as-of and topology can invalidate availability/travel interpretations | Retain assumptions and null physical measures; source dictionary, aligned inventory and surveyed topology required. Data/domain reviewer. |
| DQ-R02 False operational diagnosis / HIGH / OPEN | DQ-RECON-001, DUP-*, LOC-001, ABC-001; repeated/unmatched/different records do not establish failed service, invalid locations or wrong labels | Competing causes and UNKNOWN root cause retained. Authoritative transaction/state/scope/ABC definitions before any correction or loss claim. WMS/data reviewer. |
| DQ-R03 Confounded comparison / HIGH / OPEN | DQ-EXP-001, LOC-002, MASTER-001; equal totals mask unequal SKU/task/coverage populations | No policy winner; separately approved common-stock/task/topology protocol required. OR reviewer and owner. |
| DQ-R04 Aggregation error / HIGH / MITIGATED, REVIEW PENDING | Issues overlap; records, requested units, picking units, references, cells and pairs differ | Separate grains, COUNTD issues, one-metric share guard, no cross-issue affected total, exact CSV key/aggregate/replay tests. Workbook rendering and interaction QA still pending. Tableau author/QA reviewer. |
| DQ-R05 Unsupported closure or approval / HIGH / MITIGATED, REVIEW PENDING | AI-authored work is not independent review; no approved correction exists | Contract rejects unsupported closure/correction; pending reviewer fields, blank before/after and preserved gate hashes. Named human review required. Owner/independent reviewer. |
| DQ-R06 Sharing scope / MEDIUM / MITIGATED, OWNER REVIEW PENDING | Detailed ordinals/identifiers and local evidence links are inappropriate for the intended summary handoff | Four-file public allowlist, header checks, attribution and manual evidence-link/audience review. Nothing published. Project owner. |
| DQ-R07 Reproduction context / MEDIUM / MITIGATED | Prior untracked discovery and its tracked-file-inventory replay are context-dependent | Self-contained generator from 21 pinned sources; baseline preservation, deterministic replay and manifests. Existing research stays unchanged/untracked. Data engineer. |
| DQ-R08 Unproved usefulness / MEDIUM / OPEN | CSV technical correctness does not establish understandable Tableau workflow or a useful operating decision | Author one workbook locally, reproduce KPI/drill/filter acceptance tasks and record specialist feedback; source clarification may justify retaining the bounded finding and stopping. Analyst/operations reviewer. |

Decision DQ-D01 (M1): adopt aggregate issue records, exact source lineage, separate arithmetic/interpretation confidence and explicit approval rules. Addresses traceability and false closure; contract tests PASS. Human ratification pending.

Decision DQ-D02 (M2): retain 14 issues as source clarification required with UNKNOWN causes. Do not delete repeats, overwrite published ABC, invent geometry or adopt new stock semantics. Raw-source reconciliation and lineage checks PASS. Source evidence remains the blocker to semantic resolution.

Decision DQ-D03 (M3): supply separate-grain extracts and a summary-only public subset; preserve null unknown measures, fixed denominator definitions and no approved before/after. Automated CSV evaluation PASS; Tableau workbook authoring/review remains future work. Future synthetic library remains a separately approved design, with no generated records or model changes.

Git decision: use `codex/data-quality-foundation` on the already-configured `origin` (`https://github.com/scenariofour/warehouse-lab.git`); leave main and pre-existing untracked discovery untouched. No force pushes, history rewrite, merges or publication. Git delivery authorizes artifact transport only, never source correction, limitation acceptance or gate approval.
