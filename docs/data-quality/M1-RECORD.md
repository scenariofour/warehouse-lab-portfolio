# M1 — Define data quality and resolution contracts

Objective and pre-implementation acceptance: `.planning/2026-10-18-data-quality-foundation/task_plan.md`; detailed criteria in [CONTRACT.md](CONTRACT.md).

Built: eight-category taxonomy, JSON issue-record schema, dependency-free subset validator, cross-field review/correction rules, and positive/mutation-negative contract tests. Normalization is explicitly separate from approved correction; no source interpretation changes.

Validation: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/data_quality/verify.py M1` passed; [retained result](evidence/m1-validation.json) includes executed test output and code/schema hashes. Five test methods include one negative case per required field and 20 malformed-state mutations. All 162 baseline files and G0–G4 PENDING preserved. Before M1, the existing discovery verifier passed 195 checks and 19 artifact byte comparisons; its existing verification file remains unchanged.

Decision DQ-D01: aggregate investigation records with compressed exact raw ordinals, separately typed metric populations and human closure evidence. This prevents false issue resolution and misleading unit totals.

Remaining limits: structural validation cannot establish semantic truth, human identity or warehouse accuracy. Independent data/domain review is unassigned. Git destination and treatment of pre-existing untracked prerequisites were raised to the owner; no unapproved source interpretation or gate decision is made.
