# M4-B milestone evidence

2026-10-18. Authorized branch: `codex/data-quality-foundation`; remote: `origin` (`https://github.com/scenariofour/warehouse-lab.git`).

- Data-model/audit contract: `3d97b658d5562a65ddfc8bef16c6dd0e1440447b`.
- Analytics/extracts/blueprint/handoff: `75a3856d47f95cb6321cb9e1b7b708bd41e6d75e`.
- Validation milestone: the commit introducing this file and `verify_advanced.py`; identify with `git log --format=%H -- scripts/data_quality/verify_advanced.py`. Its hash is reported in the final delivery; a commit cannot contain its own hash.

Fresh validation: PASS, 386 checks including 36 CSV-consumer SQL assertions and 210 preservation hashes; five invalid mutations rejected; all 16 M1–M3 test methods pass; 16 generated artifacts byte-identical on replay. Validation/lookup code hashes and artifact hashes are in `validation.json`. Local lookup is tested against independent exact source ordinals for current-gap, literal-only and customer-repeat keys.

Tableau Public import/render/interactions and independent human/domain comprehension review remain PENDING. Source correction approvals = 0; G0–G4 PENDING. Existing published workbook, raw/normalized data, simulation/MVP, historical results and untracked Discovery work preserved. No simulation or synthetic inventory scenario generated.

Push procedure: non-force `git push origin HEAD:refs/heads/codex/data-quality-foundation`, followed by remote head equality against local HEAD. Actual push result and final commit hash are reported in the final delivery after this validation commit; no predicted push result is recorded here.
