# Data Quality Foundation

## Objective
Deliver M1 contracts, M2 real-source registry, and M3 Tableau extracts as separately validated atomic commits. Preserve source, MVP, simulation outcomes and G0–G4 PENDING.

## Acceptance criteria recorded before implementation
- M1: eight-category taxonomy; versioned machine-validated issue contract; lineage, counts/units/denominators, detection, confidence, causes, decisions/options, review/status/evidence/uncertainty; normalization vs correction and human approval rules; positive/negative contract tests.
- M2: deterministic registry reproduces 13003 demand-gap units, 23609 unlocated picking units, 96 ABC disagreements; all six unequal policy SKU counters; stock/layout questions retained unresolved. Exact source row/cell lineage, pinned source hashes, no synthetic input, independent checks and deterministic replay.
- M3: documented grains/IDs, metrics/denominators/evidence, isolated fact tables with nonadditivity controls; actual treatment only for before/after; Tableau A/B/C specification and public-sharing review; validated CSVs and reproducibility.
- Synthetic design only: documented mechanisms, fixtures, expectations, supported rules and assumptions; no fixture generation or simulation work.
- Each milestone: decision record, retained test evidence, atomic commit, intended remote/branch push if owner clarifies safe destination. No stage gate approval.

## Phases
1. Baseline review and preservation inventory — complete
2. M1 contract and tests — complete, 93adfdb pushed
3. M2 registry and tests — complete, 2f01713 pushed
4. M3 extracts, dashboard specification, synthetic design — complete; commit/push delivery next

## Next Step
Commit/push validated M3 and verify origin tip equals local HEAD. All implementation acceptance criteria met; Tableau authoring/human review remain explicitly pending.

## Errors / risks
- Existing discovery prerequisites remain untracked and unchanged; self-contained generator removes dependency.
- New codex/data-quality-foundation tracks intended origin; main left unchanged.
- Legacy discovery replay inventories all tracked files; future commits change its preservation inventory. New verification must distinguish immutable analytical outputs from that context-dependent inventory.

- M2 pre-commit whitespace check rejected default CSV CRLF endings. Fixed generator to emit LF, rebuilt and reran checks before commit. No source data changed.

- M3 consumer test found CSV lineage fields over default 131072-character parser limit. Replaced oversized Tableau fields with exact selectors/evidence references; complete ordinals remain in registry. Added a 4096-character transport cap test.
