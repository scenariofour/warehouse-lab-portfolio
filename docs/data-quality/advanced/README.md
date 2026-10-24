# M4-B — Data Quality & Operations Decision Studio

2026-10-18. Offline analytical foundation and Tableau handoff. No workbook edits or publishing are performed. Independent human review and G0–G4 remain PENDING; there are no approved source corrections.

Start with [the audit and model contract](AUDIT_AND_MODEL.md), [dashboard blueprint](BLUEPRINT.md), [field dictionary](DATA_DICTIONARY.md), and [web authoring guide](TABLEAU_HANDOFF.md). [Decision evidence](DECISIONS.md) explains what can be decided now. [Validation](VALIDATION.md) records checks and remaining limits.

Later delivery, 2026-10-18: the owner published the Operations Decision Studio. The [Tableau delivery and learning notebook](tableau-workbook/README.md) records [Dashboard 02](tableau-workbook/DASHBOARD_02_CASE_STUDY.md), [Dashboard 03](tableau-workbook/DASHBOARD_03_CASE_STUDY.md), [worksheet lessons by concept](tableau-workbook/LEARNING_INDEX.md), and remaining QA. The blueprint and handoff above describe the earlier foundation; planned functionality is not evidence of implementation.

Reproduce from the repository root with Python 3.10+ standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/data_quality/build_advanced.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/data_quality/verify_advanced.py
```

The generator authenticates existing M2/M3 inputs and raw hashes, reuses the registry's normalization, and writes only this extension's extracts, dictionary and manifest. It does not rerun production normalization, Discovery, inventory scenarios or simulation. Verification independently reads original records and recomputes outputs in SQLite, then replays the generator in a temporary directory. See `manifest.json` for exact keys, columns, counts and SHA-256 hashes.

Only CSVs named in `manifest.json:public_allowlist` belong in Tableau Public. Original customer/operator/order IDs, exact timestamps, coordinates and raw row lists are omitted. Stable opaque identifiers preserve investigation across the new extracts; they are pseudonyms, not a claim of irreversible anonymization. Keep original sources and existing internal extracts out of the new workbook. CSVs contain public research data and derived quantities, not newly collected personnel information. Public sharing also exposes underlying downloadable data; hiding a sheet is not a privacy control.

Attribution on every dashboard: Rodrigo Furlan de Assis, *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*, Mendeley Data v1, DOI [10.17632/pf2w725pw3.1](https://data.mendeley.com/datasets/pf2w725pw3/1), CC BY 4.0. Changes: aggregation, pseudonymous identifiers, normalization and explicitly labeled sensitivity calculations. AI-assisted preparation; source semantics and independent human review pending. No measured operational failure, savings or causal policy benefit established.
