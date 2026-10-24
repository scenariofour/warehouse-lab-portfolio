# Warehouse Lab — Data Quality Visualization Foundation

Offline portfolio research extension, 2026-10-18. AI-assisted implementation and analysis; independent human/domain review remains PENDING. The original MVP, simulator, raw and normalized source data, prior research and recorded results are preserved. G0–G4 remain PENDING.

| Milestone | Deliverable / decision purpose | Validation evidence |
|---|---|---|
| M1 | [Issue and resolution contract](CONTRACT.md), taxonomy and schema; distinguish a discrepancy, normalization and approved correction | [M1 record](M1-RECORD.md), [test evidence](evidence/m1-validation.json) |
| M2 | [14 real-source investigation records](registry/README.md), exact lineage and reproducible analytical ledgers; prevent unsupported failure or policy claims | [M2 record](M2-RECORD.md), [test evidence](evidence/m2-validation.json) |
| M3 | [Tableau authoring specification](TABLEAU_SPEC.md), ten internal/four summary CSVs; connect uncertainty to investigation and decision choices | [M3 record](M3-RECORD.md), [test evidence](evidence/m3-validation.json) |

Read [risk and decision tracking](RISK_AND_DECISIONS.md) and the [future synthetic exception proposal](SYNTHETIC_EXCEPTION_PROPOSAL.md). The latter is design-only and requires separate approval before fixtures or features are built. No correction, deduplication, new source interpretation, operational intervention or publication was performed.

## Reproduce

From repository root, Python 3.10+ standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/data_quality/build_registry.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/data_quality/export_tableau.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/data_quality/verify.py M3
```

The final command runs all 16 contract/registry/CSV test methods, including independent original-source arithmetic, full row/cell lineage checks, shape/review/null invariants, public boundaries, baseline preservation and byte-identical replay. It writes a new execution timestamp/test-duration record in m3-validation.json. Analytical outputs are byte deterministic; validation timestamps/durations are execution metadata. Nothing executes the simulation, normalizer, external contacts or a publishing API. Stop on a failed source fingerprint or test; never edit source records to make checks pass.

## Tableau handoff

- [Internal investigation CSV directory](tableau/internal): ten files; source-level selectors and derived details.
- [Summary sharing subset](tableau/public): four allowlisted files prepared for owner review. This directory is not a published site.
- [Extract manifest](tableau/manifest.json): table grains, keys, fields, measure aggregation rules and hashes.

Key findings reproduce 13,003/228,195 requested units unreconciled, 23,609/215,192 picking units without coordinates, 96/208 ABC disagreements, and all six unequal SKU-counter policy pairs. These are extract discrepancies, not confirmed warehouse failures. All root causes remain UNKNOWN; all 14 issue states require source clarification. Unmeasured physical stock/distance and financial impact stay null. No approved treatment before/after exists. Overlapping/incompatible issue populations have no combined affected-unit total.

Next action: author the specified Tableau workbook locally and execute its import/filter/drill/counting acceptance checks with an independent reviewer. In parallel, the project owner can seek source clarification for transaction/repeat/size definitions, inventory date/UOM, ABC basis and physical topology. Any correction, synthetic test implementation, public sharing or formal gate decision needs its own evidence and appropriate human authorization.

Source attribution: Rodrigo Furlan de Assis, *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*, Mendeley Data v1, DOI [10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), CC BY 4.0. No independent warehouse truth, current operational state or business savings is claimed.
