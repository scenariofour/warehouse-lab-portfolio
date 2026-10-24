# Evidence register

Snapshot date: 2026-10-18. Public URL: [Operations Decision Studio](https://public.tableau.com/views/WarehouseLabOperationsDecisionStudio/Dashboard3?:showVizHome=n). The text fetch failed, but read-only browser inspection successfully loaded the workbook and its published tabs. No editor, workbook download or publishing operation was used.

## Evidence classes and observed delivery

| ID | Class | What the evidence establishes | Boundary |
|---|---|---|---|
| U1 | Author report | Two dashboards completed; B01, B02, B04, B05, C01, C01b, C02, C03 authored | Supplied in this documentation request, not a recovered chat history |
| U2 | Author report | B01 → B02 and B05 → B02 Wave drill-down manually demonstrated | No test log/screenshots supplied; not an exhaustive action test |
| U3 | Author report | Build lessons include SUM(Rank), discrete/continuous, roles, COUNTD, Measure Names/Values, action direction and interpretation parameters | Exact error messages, click sequence and resolution dates are not available |
| O1 | Published viewer | Workbook title “Warehouse Lab \| Operations Decision Studio”, author scenariofour; first/last publication labels Oct 18, 2026; eight worksheet and two dashboard tabs | Date labels are publication metadata, not evidence of data freshness |
| O2 | Published viewer | Dashboard 02 visibly contains C01, C01b, C02 and interpretation/business framing | No C03 panel observed on that dashboard; no heatmap-to-ledger action was tested |
| O3 | Published viewer | Dashboard 03 contains B01 Top 20 bar view, B05 scatter, B02 text ledger; pInterpretation visible with “Current inferred” selected; methodology and source attribution shown | Control presence is not proof that every branch updates every sheet correctly |
| O4 | Published viewer | B04: Rank 1–20, wave dimension, Gap Units bars, Member Id and Cumulative Gap Share in visualization description; caption explains 1,720 visible vs 13,003 total gap | Source filter/caption observed; filter edge cases not exercised |
| O5 | Published viewer | C03: published/derived ABC highlight table, color/label “Distinct References”, Customer Units tooltip field; caption states 96 of 208 references differ | Viewer labels do not expose the exact COUNTD calculated-field definition |
| O6 | Published viewer | C01 shows Source Id, Rule Id, Original Token Display, Current Value, Alternative Value, Token Records/Units. Its standalone sheet exposes source/rule filter cards and a Measure Names filter. C01b is a source/rule highlight table colored/labeled Token Records, tooltip Token Units | C01 displayed Customer_Order / HALF_SIZE despite broader standalone source/rule selections; origin of that state is not established |
| O7 | Published viewer | C02 is a **bar chart**, with CURRENT_INFERRED, CUSTOMER_DEDUP, LITERAL_SIZE and Gap Units/Excess Units | Planned text-table formatting is not the delivered chart; full numerical branch QA remains pending |
| O8 | Published viewer | B01 tooltip field list includes selected customer **units**; B05 includes selected customer **records**. B05 has continuous picking/gap axes, Wave Id Detail and Wave Gap Share color. B02 uses Measure Names/Values, gap/excess and Reconciliation Id tooltip fields | A listed tooltip field is observed metadata, not a separately checked value for every mark |

These entries summarize actual accessibility text and visible published content. They are not screenshot files. No workbook XML/shelf expressions, filter-action configuration, hidden-sheet inventory or uploaded-extract byte identity was inspected. Reconstruction recipes are labeled **G** throughout.

## Repository evidence

| ID | Reference | What was verified for these notes |
|---|---|---|
| R1 | [Dictionary](../DATA_DICTIONARY.md), [manifest](../manifest.json), [builder](../../../../scripts/data_quality/build_advanced.py) | Grains, public fields, source normalization, cumulative-before ABC and declared alternatives; all 14 existing public CSV hashes match the manifest |
| R2 | [Reconciliation summary](../public/reconciliation_summary.csv) | Current: 228195 demand, 215192 picks, 215192 matched, 13003 gap, 0 excess. Literal: 149514 matched, 78681 gap, 65678 excess. Customer dedup: 215460 demand, 202475 matched, 12985 gap, 12717 excess |
| R3 | [Pareto](../public/exception_pareto.csv), [tokens](../public/normalization_tokens.csv), [ABC](../public/abc_comparison.csv) | Fresh read-only sums: Top 20 wave gaps 1720; first wave 168; half-token mapping 38846 customer records / 67383 customer units; ABC 208 references / 96 differing labels |
| R4 | [Existing validation report](../evidence/validation.json), [verifier](../../../../scripts/data_quality/verify_advanced.py), [consumer SQL](../consumer_checks.sql) | Historical PASS: 386 checks, five rejection checks, 16 foundation tests and 16 replayed files; current verifier hash matches recorded hash. These computational tests were **not rerun** or rewritten by this documentation task |
| R5 | [Integrity baseline](evidence/integrity-baseline.json) and documentation validation report | Baseline pins 243 pre-existing files, including unrelated untracked Discovery work. Only the existing advanced README is allowed to change; its original is recoverable at the recorded base commit. No tracked workbook file exists |

Repository equality validates the supplied extracts and definitions, not hidden calculations or the exact data uploaded into Tableau. The new [documentation validation report](evidence/documentation-validation.json) records link/anchor checks, fresh CSV checks and preservation checks; it is not a workbook QA report.

## Pending and historical references

**Q1:** all parameter branches, all affected sheets, null/zero-denominator behavior and inactive keys. **Q2:** selection clearing, sequential/combined actions, multi-select and source-versus-target configuration. **Q3:** thumbnail/share-preview rendering and layout across viewport sizes. **Q4:** exact workbook calculations, uploaded-extract identity and a real workbook export/versioning decision. **Q5:** independent domain review, source semantics and comprehension testing. All remain unverified; no performance gain, cost saving, fulfillment failure or causal improvement is inferred.

The original [blueprint](../BLUEPRINT.md), [handoff](../TABLEAU_HANDOFF.md) and [validation limitations](../VALIDATION.md) describe the earlier foundation. In particular, the handoff's conservative action-authoring caveat must not erase U2's later demonstrated runtime behavior. Conversely, U2 does not prove the authoring dialog is supported in every Public deployment. The notes preserve both scopes without changing those historical documents.
