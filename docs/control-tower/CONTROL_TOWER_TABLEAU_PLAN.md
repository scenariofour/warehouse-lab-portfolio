# M5 Tableau Public plan and feasibility review

**Proposed only · 2026-10-21 · Do not begin authoring before design approval.** [Brief](CONTROL_TOWER_DESIGN_BRIEF.md) · [Data contract](CONTROL_TOWER_DATA_CONTRACT.md) · [Learning plan](CONTROL_TOWER_LEARNING_PLAN.md)

## Feasibility verdict

The evidence-first dashboard and native text-mark dependency matrix are analytically feasible with existing CSVs. No new operational fact table, generated network coordinates, custom extension, Sankey scaffold, paid service or new dataset is needed. A force-directed network would imply a topology/weighting absent from the data and add authoring complexity; omit it.

**Conditional technical feasibility:** Public supports file-based browser authoring, calculations and parameters. The current signed-in Public authoring controls for multiple independent sources, logical relationships, action configuration and layout have not been inspected in M5. Documentation for Cloud/Server is not blanket proof of Public editor parity. The HTML is not a workbook prototype and cannot establish those capabilities.

Preserve [Operations Decision Studio](https://public.tableau.com/views/WarehouseLabOperationsDecisionStudio/Dashboard3?:showVizHome=n). After approval, create a separate M5 workbook rather than editing the published dashboards. Reuse their public URLs for investigation. This package performs no login, upload, editor action, workbook download, publication or remote edit.

## Capability register

Official documentation checked 2026-10-21. “Documented” below describes source support, not a successful M5 editor test.

| Capability | Evidence and applicability | M5 choice and fallback |
|---|---|---|
| Public browser authoring, CSV upload | [Public FAQ](https://help.tableau.com/current/public/desktop/en-us/public_faq.htm); [Connect to data on the web](https://help.tableau.com/current/online/en-us/creator_connect.htm), explicitly includes Public and file upload | Existing public CSVs only. First later feasibility check: one file, types and totals. No authoring attempted now |
| Calculated fields and manual parameters | [Create parameters](https://help.tableau.com/current/pro/desktop/en-us/parameters_create.htm), applies to Public; existing notebook records an interpretation control in the published viewer | Baseline manual `pIssue`; retain unknowns and use aggregate guards. Viewer presence does not prove every editor menu |
| Multiple independent sources / relationships | [Data model](https://help.tableau.com/current/pro/desktop/en-us/datasource_datamodel.htm); [web/Desktop comparison](https://help.tableau.com/current/pro/desktop/en-us/server_desktop_web_edit_differences.htm) covers Cloud/Server/Desktop, not Public parity | Test adding a second independent file after approval. If unavailable, assemble with free Desktop Public Edition; browser-only fallback is separate single-source workbooks with manual navigation and unlinked selectors |
| Text matrix, bars, tables, tooltips | Native shelf/Marks workflow; [field roles](https://help.tableau.com/current/pro/desktop/en-us/datafields_typesandroles.htm); analogous sheets documented in existing delivery notebook | Text marks for A/C/D/A+C; conventional tooltip and companion ledger. No custom glyph/image import dependency |
| Tiled layout, padding, fixed size | [Size and layout](https://help.tableau.com/current/pro/desktop/en-us/dashboards_organize_floatingandtiled.htm), Cloud/Server/Desktop scope | Fixed 1440 × 2000 target, tiled containers, ordinary borders/shading. If Public lacks controls, Desktop assembly or simpler stacked layout; HTML font/rounding precision is not guaranteed |
| Use as Filter / targeted filter actions | [Actions and dashboards](https://help.tableau.com/current/pro/desktop/en-us/actions_dashboards.htm), [Filter actions](https://help.tableau.com/current/pro/desktop/en-us/actions_filter.htm), Cloud/Server/Desktop scope; existing workbook notebook records author-reported B01/B05 → B02 runtime drills | Try targeted issue action only if editor exposes configuration. Verify source, target and clear behavior. Manual shared parameter is the baseline fallback; do not infer web authoring support from published runtime |
| Parameter actions / URL actions / Go to Sheet | [Parameter actions](https://help.tableau.com/current/pro/desktop/en-us/actions_parameters.htm), [URL actions](https://help.tableau.com/current/pro/desktop/en-us/actions_url.htm); not established in this Public editor | Optional enhancement after capability check. Use visible manual parameter and published tabs/static hyperlink text when unavailable. Desktop configuration may be needed |
| Responsive/device layouts | Public FAQ discusses display; device-layout construction differs from CSS | Desktop-first Tableau deliverable; separately author/check phone layout if approved and supported. HTML reflow is only local mockup behavior |

The existing [handoff](../data-quality/advanced/TABLEAU_HANDOFF.md) and later [delivery evidence](../data-quality/advanced/tableau-workbook/EVIDENCE_REGISTER.md) are complementary: the handoff is conservative about authoring menus; the later evidence records runtime actions and a parameter. Neither establishes an exhaustive M5 feature test.

## Required worksheets and object inventory

Names are proposed M5 identifiers, not already-authored sheets. P/A aliases follow the data contract. Distinguish source grain from mark grain.

| ID / sheet | Source → mark grain | Shelves/Marks and aggregation | Scope / tooltip |
|---|---|---|---|
| T01 Demand gap | P/issue_metrics → one metric | Text guarded MIN count/share; filter exact gap metric key | Full extract, inferred-size basis; 13,003 / 228,195; cause unknown |
| T02 Coordinate coverage gap | P/issue_metrics → one metric | Text guarded MIN count/share; filter exact unmapped-picking key | Full picking extract; 23,609 / 215,192; no assertion of invalid location |
| T03 ABC disagreement | P/issue_metrics → one metric | Text guarded MIN count/share; filter exact ABC key | 96 / 208 demanded references; label bases differ |
| T04 Policy comparison prerequisite | A/policy_pairs → full set | Text COUNTD unequal pair IDs and COUNTD all pair IDs | 6 / 6 comparisons; conditional SKU counters, no total L1 |
| T05 Evidence Dependency Map | A/issue_evidence → issue/source cell | Rows issue title + issue_id; Columns source_id; aggregate Role label on Text/Color; COUNTD issue_source_id in tooltip. No role on Detail | 33 occupied cells / 35 records. Retain A+C cells; blank cells are unregistered links |
| T06 Decision exposure | A/decision_evidence → decision category | Rows category; Columns COUNTD issue_id; Bar with count label | Fixed all-issue context: 5/4/2/2/1. Label “questions”, never risk amount |
| T07 Selected decision and request | Related issue/impact/decision source → one issue | Text ATTR decision, mechanism, competing explanations, consequence, claim_limit, request; separate text worksheets if wrapping demands | `pIssue` exact match; multi/no selection has explicit prompt; show AI-proposed / review pending |
| T08 Selected metric evidence | P/issue_metrics → metric_key | Text table metric_id, count, unit, denominator; guarded values | `pIssue`, plus single metric selector; suppress multi-key share; physical nulls show Not measured |
| T09 Lineage detail | A/issue_evidence → issue_source_id | Rows source_id, role; Text selected count; MIN source count, hash, evidence_ref in tooltip | `pIssue`; two records remain separate for A+C cells. Selected records are not presumed failed units |
| T10 Interpretation sensitivity | A/reconciliation_summary → interpretation | Rows interpretation; Text Measure Names/Values restricted to MIN gap/customer/excess | All three rows; never grand total; label alternative assumptions, not trend or treatment |
| T11 Investigation priorities | A/decision_evidence → issue | Text issue title, next request; filter four curated IDs, manual display order | Counts not required. All 14 remain selectable through `pIssue`; no due date, owner, ROI or fabricated score |
| T12 Experiment prerequisites | A/experiment_controls → control_id | Rows control_name; Text result and required_evidence | GLOBAL controls + selected pair if provided; no percent complete, no green protocol-ready state |

Dashboard objects: title/source snapshot, explicit research boundary, recommendation text, attribution, source/decision selector instructions and investigation hyperlinks. Do not spend a worksheet on decorative icons. T04 supports the recommendation; T08/T09/T12 can be below the primary canvas or in a separate “Evidence detail” dashboard within the new workbook. Existing B/C worksheets are external investigation destinations, not copies required for M5.

For source abbreviations, alias only display labels, never stored source_id. Keep full source filename in tooltip and lineage detail. Matrix source order: customer, picking, product, locations, navigation, random, class-based, dedicated, hybrid, README, notebook. Use registered roles only; no filled-in links for aesthetically complete rows. Tableau can omit entirely empty source columns after filtering; retain a “Selected issue only” scope label if this happens.

## Parameters and filter scope

**Baseline `pIssue`:** String list of the 14 exact issue IDs, default `DQ-EXP-001`. Same-workbook parameter used in T07/T08/T09, each source explicitly calculating `[issue_id] = [pIssue]`. T05 shows all rows with a calculated selection highlight `[issue_id] = [pIssue]`; T11 can highlight the same ID. Manual controls are required even if actions are added, so keyboard users can reach every issue. Changing a parameter does nothing unless each sheet references it.

**T05 source filter:** multi-select source_id, local to T05 only; default All. It changes visible registered links, not T01–T04 or T06, the issue selector, or decision readiness. Never filter the nine source-count populations through it. **T08 metric filter:** single metric_key relevant to selected issue; if no valid metric remains show a prompt and allow reset. **T12 optional pair filter:** local control scope, default all relevant controls; do not add a global policy selector that appears to compare outcomes.

M5 does not need an interpretation parameter: T10 deliberately displays all three branches as a comparison, and global T01 stays current inferred. Existing Dashboard3's interpretation parameter is controlled independently in the destination workbook. No sync is promised across workbooks.

Reset baseline: pIssue = DQ-EXP-001, source filter = All, metric filter = All with guarded prompt if multiple, clear all optional mark actions. Native Revert can be used after checking the saved state. Reset is a user action; changing one issue selector does not automatically clear every independent filter. Display active scope to prevent silent empty views.

## Optional action specifications, contingent on editor support

| Action | Source and trigger | Target / mapping | Clear, multi-select and exclusions |
|---|---|---|---|
| Select issue | T05 or T11, Select one issue | Parameter action `issue_id → pIssue`, if available | Clear retains previous pIssue; multi-select keeps prior value and displays “Choose one issue”; manual selector always available. This avoids shrinking the matrix to one row |
| Filter lineage fallback | T05, Select | T09 only, String issue_id → String issue_id, Selected Fields (not All Fields) | Clear Show all values **only in an action-driven variant with no pIssue filter on T09**. Do not stack this with a retained issue parameter on the same target; use one selection model |
| Inspect reconciliation | Explicit menu/link, never automatic on hover | Published [Dashboard3](https://public.tableau.com/views/WarehouseLabOperationsDecisionStudio/Dashboard3?:showVizHome=n) | Opens unfiltered current saved view. No invented issue/wave URL filter. Explain scope change |
| Inspect normalization | Explicit menu/link | Published [Dashboard2](https://public.tableau.com/views/WarehouseLabOperationsDecisionStudio/Dashboard02NormalizationInterpretationLab2?:showVizHome=n) | Same navigation boundary; verify destination title after approval |
| Read evidence notes | Menu URL action on selected issue, if available | Reviewed documentation URL and issue lookup text | No raw/internal links or file:// URLs. Registry JSON fragments are not live anchors; retain full ID in visible text |

T01–T04 and T06 are excluded from all optional issue/source filter actions. T10 is excluded too. If fine-grained action targeting is unavailable, do not enable Use as Filter indiscriminately: retain the manual parameter. Existing B01/B05 → B02 interactions remain in their published workbook, unchanged and subject to existing QA limits.

## Later construction sequence and acceptance

This sequence is an implementation outline for assessing feasibility, not authorization to execute it.

1. After approval, confirm file upload, String IDs, nulls, second independent source and relationship support in a separate M5 workbook. Stop and report any capability mismatch; agree on Desktop assembly or simpler single-source navigation before compromising grains.
2. Build T01–T04 and verify exact numerators/denominators. Add the issue model and T05/T09; verify 14 parents, 35 role records, 33 occupied cells and both A+C cases before adding style.
3. Add T06–T12, manual selector and scoped filters. Verify counts 5/4/2/2/1, all 14 next requests, blank financial/physical measures and all sensitivity rows.
4. Assemble tiled layout, visible evidence labels and conventional tooltips. Add optional actions only after verifying editor availability. Provide manual navigation as a complete fallback.
5. Test every issue, every metric including the two unmeasured metrics, source combinations, empty selections, zero denominator and hypothetical multi-key selections without changing source files. Confirm global cards unchanged after each selection. Verify the native clear/revert state and saved initial state.
6. Execute the three comprehension journeys in the brief with a named reviewer; capture actual workbook version, uploaded-file hashes where obtainable, screenshots, expected/actual results and remaining limitations. Review attribution and public scope. Publication requires later explicit authorization; no G0–G4 state changes follow from building a dashboard.

M5's present local review proves only source integrity, design arithmetic, artifact consistency and HTML rendering/affordances. **Tableau import, calculations, rendering, authoring-menu availability, action behavior, uploaded-extract identity and human comprehension remain untested in Tableau.**
