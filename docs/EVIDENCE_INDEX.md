# Evidence index and reproduction

Owner: QA evidence custodian role unassigned. Author: AI assistant.  
Version: 0.2.0 · 2026-10-17. Status: DRAFT — PENDING HUMAN REVIEW.  
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
| E-11 | [Assignment](evidence/2026-10-17/assignment.md) | Initial human-authorized work boundaries; no gate review/approval |
| E-12 | [Owner direction](evidence/2026-10-17-g0-direction/owner-confirmation.md), [G0 readiness](G0_READINESS_ASSESSMENT.md), [change summary](G0_CHANGE_SUMMARY.md), [revision provenance](evidence/2026-10-17-g0-direction/README.md), [new document checks](evidence/2026-10-17-g0-direction/document-checks.json), [preservation checks](evidence/2026-10-17-g0-direction/preservation-checks.json) | Owner-confirmed direction and current documentation checks; no new simulation result, independent review or gate approval |

## Current documentation revision

The owner confirmed intended-use direction in D-01 after the original review. E-01–11 and FINAL_REVIEW remain historical evidence, preserved byte-for-byte. Their snapshot manifest records the earlier document hashes; it is not a claim that those hashes match the revised charter. E-12 supplies the new revision identity. Do not refresh or overwrite the earlier packet for this documentation task. GATE_REVIEWS.json remains unchanged with five PENDING gates.

Current documentation check (no technical reruns):

```bash
npm run check:governance -- --evidence-dir docs/evidence/2026-10-17-g0-direction
```

## Original technical reproduction commands — use an isolated copy

These earlier commands can write dated reports. Run them in a separate copy or preserve new outputs under a new run identity; they were not executed for the current documentation-only revision.

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

The checker supports `--refresh-pending` for a deliberately prepared unsigned packet and refuses recorded gate decisions. Do not use that flag on the retained original packet in this revision; the current owner instruction preserves previous evidence. A future review should use a new revision/run directory and retain its predecessor.

The manifest covers named source/input/evidence files and records current hashes; it excludes itself and final document-check output to avoid circular hashing. A material hash change requires renewed affected evaluations and gate review; the checker can detect drift, not authenticate human identity. [Gate procedure](GATE_REVIEWS.md).
