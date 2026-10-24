# Evidence index and reproduction

Owner: QA evidence custodian role unassigned. Author: AI assistant.  
Version: 0.1.0 · 2026-10-17. Status: DRAFT — PENDING HUMAN REVIEW.  
Review requirements: independent reviewer reproduces relevant checks, verifies hashes and judges adequacy; command success is not approval.

| ID | Evidence | What it establishes / does not establish |
|---|---|---|
| E-01 | [Baseline inventory](evidence/2026-10-17/baseline-inventory.json), [prior reports](evidence/2026-10-17/prior/validation-results.json), [baseline tests](evidence/2026-10-17/baseline-tests.log), [baseline scenarios](evidence/2026-10-17/baseline-scenarios.json) | Inspected code/input identity and earlier technical outcomes; no human sign-off or field baseline |
| E-02 | [Data evaluation](evidence/2026-10-17/data-evaluation.json), [log](evidence/2026-10-17/data-evaluation.log), [normalizer rerun](evidence/2026-10-17/normalization-rerun.log) | All raw hashes and exact transformations, joins, grouping and inventory-control measurements under existing rules |
| E-03 | [Pre-fix ZIP failure](evidence/2026-10-17/before-import-regression.log), [pre-fix routing failure](evidence/2026-10-17/before-routing-regression.log) | Reproduced defects in isolated fixtures; actual published raw files were not corrupted |
| E-04 | [Model evaluation](evidence/2026-10-17/model-evaluation.json), [log](evidence/2026-10-17/model-evaluation.log), [runner](../scripts/evaluate_governance.ts) |39 BFS references, complete-event/coordinate KPI oracles, exact replay and12 local sensitivity cases; no physical reference |
| E-05 | [Current scenarios](evidence/2026-10-17/scenarios.json), [log](evidence/2026-10-17/after-scenarios.log), [runner](../scripts/validate-scenarios.ts) | Four default 120-group terminal/invariant runs with current execution/input identity; not controlled policy effects |
| E-06 | [Post-fix unit tests](evidence/2026-10-17/after-unit-tests.log), [tests](../tests/simulation.test.ts) | Nine TypeScript tests including invalid routing, conservation, missing/scarce stock, replay and head-on behavior |
| E-07 | [Import tests](evidence/2026-10-17/after-import-regression.log), [fixtures](../tests/test_data_pipeline.py) | Five Python source-preservation regression fixtures, not real stock semantics |
| E-08 | [Browser test](evidence/2026-10-17/browser-tests.log), [specification](../tests/browser/warehouse.spec.ts) | Existing MVP controls, follow/inspection/export/policies, scene structure and responsive workflow; one tested browser environment |
| E-09 | [Build log](evidence/2026-10-17/build.log) | Typecheck/production compilation; bundle warning is visible; no operational validation |
| E-10 | [Correction impact](evidence/2026-10-17/correction-impact.json), [code diff](evidence/2026-10-17/corrections.diff), [document checks](evidence/2026-10-17/document-checks.json), [final evidence manifest](evidence/2026-10-17/evidence-manifest.json) | Source/data impact and structural traceability; hashes and structural checks cannot replace independent judgment |
| E-11 | [Assignment](evidence/2026-10-17/assignment.md) | Current human-authorized work boundaries; no gate review/approval |

## Reproduce from the project directory

```bash
npm ci
npm run audit:data
npm run test:data
npm test
npm run validate:scenarios
npm run evaluate:governance
npm run build
npm run test:browser
npm run check:governance -- --evidence-dir docs/evidence/2026-10-17
```

`audit:data` and the evaluation runner generate dated evidence using New York date and UTC execution metadata. Read the current paths printed/created by a new run; this review references the pinned 2026-10-17 snapshot. Capture command exit codes and retain fresh logs with the run identity. Never overwrite evidence already accepted by a human: use a new revision/run directory and link the superseded review. Current evidence is draft, unsigned review material.

Python 3.10+ standard library is used for ingestion/audit/import fixtures; TypeScript runners use the existing tsx dependency. Browser tests use the existing Playwright/Chrome setup documented in [README](../README.md). No new runtime dependency, dashboard or model feature is introduced.

The pending review custodian can explicitly refresh an unsigned packet with `npm run check:governance -- --evidence-dir docs/evidence/2026-10-17 --refresh-pending`; this refuses any recorded gate decision and does not approve a gate. After a human decision, preserve the packet and create a new revision rather than refreshing it.

The manifest covers named source/input/evidence files and records current hashes; it excludes itself and final document-check output to avoid circular hashing. A material hash change requires renewed affected evaluations and gate review; the checker can detect drift, not authenticate human identity. [Gate procedure](GATE_REVIEWS.md).
