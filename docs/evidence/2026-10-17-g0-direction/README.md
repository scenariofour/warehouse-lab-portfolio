# G0 direction revision — evidence provenance

Recorded: 2026-10-17. Author/recorder: AI assistant. Status: PENDING HUMAN REVIEW. No formal gate outcome or independent review is recorded.

This new evidence directory preserves the original `docs/evidence/2026-10-17` packet. Its evidence-manifest hashes describe the earlier document revision; do not refresh that historical packet to make it match the revised charter.

- `owner-confirmation.md`: selected verbatim excerpts from the current owner chat instruction, with a labeled summary of remaining instructions. Confirms intended-use direction only; not a signed G0 approval.
- `before-inventory.json`: hashes captured before this revision's edits, including previous outputs, all original evidence and existing application/data/configuration files. It excludes scratch work, dependencies, cache files and OS metadata. Hashes establish byte identity, not external or human validity.
- `prior-documents/`: preserved copies of the ten governance documents inspected for alignment, including the unchanged machine gate register. Relative links in these historical copies retain their original text; use the active documents or original packet for navigation. They are not a separately relocated runnable document set.
- `preservation-checks.json`: baseline-to-current comparison permitting only the nine named existing Markdown/JSON documentation edits. Also confirms untouched runtime, datasets, tests, scripts, configurations, previous results and previous output packages.
- `direction-checks.json`: automated document predicates: strategic hierarchy/question, nine readiness rows, all gates unchanged/PENDING/null, retained EVAL register rows/claim outcomes/correction history, and links/headings in current revised documents. These predicates do not validate narrative adequacy or satisfy independent review.
- `model-evaluation.json` and `scenarios.json`: **byte-identical copies of historical reports from the original 2026-10-17 packet**, solely to satisfy the existing documentation checker's expected input paths. Original run timestamps/hashes/results remain unchanged. No new technical execution or approval is implied.
- `evidence-manifest.json`: current revision file hashes, covering source, scripts, tests, docs, raw/normalized data and root build configuration/README. The manifest excludes itself and the final documentation checker output/log to avoid circular hashing. Historical evidence and prior-document copies are included as bytes, not reinterpreted as current document hashes.
- `document-checks.json` and `documentation-checks.log`: fresh execution of the existing documentation checker against this revision. Its scope is structural metadata, local links, identifiers and input identity; not physical-model validation or human identity authentication.
- `verify_direction.py`: retained copy of the scratch verification procedure used for the new direction/preservation checks. It is review tooling, not application or simulation code.

Reproduction from the project root:

```bash
python3 docs/evidence/2026-10-17-g0-direction/verify_direction.py
npm run check:governance -- --evidence-dir docs/evidence/2026-10-17-g0-direction
```

The direction check compares against the original workspace inventory. A review package intentionally omits previous output archives to avoid recursive packaging; missing baseline paths under `outputs/` are reported as package omissions, not as verified preserved bytes in that copy. The authoritative preservation report is from the original workspace. Rerunning a check writes a new result; preserve the existing packet first and capture reruns under a new review identity. No `--refresh-pending`, ingestion, simulation, browser or build command was run for this revision.
