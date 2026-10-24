# M4-B Advanced Tableau Analytics

Goal: reproducible public-safe investigation extracts, four purposeful Tableau experiences, independently reconciled evidence and atomic commits/push on codex/data-quality-foundation.

## Phases
1. Audit M1–M3 and Discovery, preserve all existing files — complete
2. Define model/grains/public boundaries and acceptance — complete
3. Generate extracts reusing registry definitions — complete
4. Blueprint and web authoring handoff — complete
5. Independent source validation, release review, preservation — complete
6. Atomic commits and non-force push to existing origin branch — complete

## Assumptions
Current request authorizes new offline extracts and Git push, not workbook edits or gate/source approvals. Discovery work is pre-existing untracked input and stays unmodified/uncommitted. No synthetic inventory generation. Alternative interpretations are analytical scenarios only.

## Next Step
Complete: foundation delivered. Manual Tableau construction/import/interaction and named human reviews remain pending as documented.

## Errors Encountered
Published Tableau URL returned web fetch error; workbook contents cannot be verified through that endpoint. User-reported 14-issue dashboard accepted as context only.

Validation development: first SQL run interrupted after spotting missing correlated-query order index; added index before group reconciliation and restarted. Read-only performance fix; no source/output mutation. Audit read of Discovery long-row CSV exceeded default csv field limit; switched to schema/summary inspection; raw verification has no long lineage fields.
