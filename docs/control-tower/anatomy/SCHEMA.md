# Data contract and Tableau import schemas

All paths below are relative to this directory. UTF-8, comma delimited, header row, quoted as needed, LF endings. Blank means absent/unknown, never zero. Coordinates have six-decimal precision. IDs are strings. Fields not declared numeric below are string dimensions; `path_order` must also be converted to a **discrete dimension** for Path. No geographical roles belong on XY fields.

The exact ordered columns, row counts and SHA-256 of every output are in [manifest.json](manifest.json). That manifest also pins the generator and each consumed public extract. No raw customer, order, wave, operator, reference or location identifiers are imported.

| CSV | Rows | Grain / key | Purpose |
|---|---:|---|---|
| [tableau/nodes.csv](tableau/nodes.csv) | 30 | one node / `node_id` | Authoritative node identities and editorial locations |
| [tableau/edges.csv](tableau/edges.csv) | 47 | one occupied association / `edge_id` | 33 evidence pairs + 14 decision assignments |
| [tableau/edge_points.csv](tableau/edge_points.csv) | 1,927 | one sampled point / `edge_id,path_order` | 41 points per cubic curve |
| [tableau/lineage_roles.csv](tableau/lineage_roles.csv) | 35 | one original lineage record / `lineage_id` | Lossless role bridge, including both multi-role pairs |
| [tableau/issue_context.csv](tableau/issue_context.csv) | 14 | one issue / `issue_id` | Source-backed investigation text |
| [tableau/issue_metrics.csv](tableau/issue_metrics.csv) | 18 | one measure / `metric_key` | Exact copy of the existing public metric extract |
| [tableau/tableau_marks.csv](tableau/tableau_marks.csv) | 29,370 | one focus slice + mark + point / `focus_issue,mark_kind,mark_id,path_order` | Native Tableau single-source build; non-edge Path is blank |

## Nodes

`node_id, node_type, label, short_label, x, y, label_x, label_y, label_align, shape, issue_id, source_id, decision_category`

- `node_type`: SOURCE (11), ISSUE (14), DECISION (5). Node ID is `S:` + existing source filename, unchanged issue ID, or `D:` + existing decision category. No raw row key is exposed.
- `label`: unchanged source filename, issue title or title-cased category. `short_label`: editorial display abbreviation; not a new classification. Full identities remain in tooltips/context.
- `x,y,label_x,label_y`: decimal presentation coordinates. Domains X=0–1000, Y=0–760, origin at top left. `label_align`: left/right; `shape`: diamond/circle/square. Node size is constant within type and has no quantitative meaning.
- Exactly one of `issue_id`, `source_id` identifies issue/source nodes; category nodes carry `decision_category`. Issue nodes also carry their registered category. Other identity cells are blank.

## Associations and paths

Edges: `edge_id, edge_kind, from_node, to_node, issue_id, source_id, decision_category, lineage_ids, roles, lineage_count, c1x, c1y, c2x, c2y`.

`edge_kind` is EVIDENCE_ASSOCIATION or DECISION_ASSOCIATION. `from_node,to_node` specify curve endpoints for rendering, **not causal direction**. There are no arrows. Evidence edge IDs `E01`–`E33` enumerate sorted existing issue/source pairs. Decision edge IDs `D01`–`D14` follow the pinned decision extract. An edge ID is local to this geometry version; use issue/source IDs for longitudinal identity.

`lineage_ids` preserves all original issue-source record IDs on that pair, pipe separated; `roles` is the sorted distinct registered role set. `lineage_count` is an integer metadata count, not affected records or severity. Decision associations have zero lineage records, blank roles and blank source IDs; they are derived from the AI-proposed decision category field, not added evidence. `c1x,c1y,c2x,c2y` are decimal Bézier control coordinates.

Path points: `edge_id, edge_kind, issue_id, source_id, decision_category, roles, lineage_count, path_order, x, y`.

`path_order` is integer 0–40; `t=path_order/40`. Every XY point is sampled from `B(t)=(1−t)³P0+3(1−t)²tC1+3(1−t)t²C2+t³P1`. P0/P1 are exact node locations. Edge metadata repeats on all 41 points; use ATTR, never SUM of `lineage_count`. Path length, crossings and node separation are not operational observations.

Lineage bridge: `edge_id, lineage_id, issue_id, source_id, lineage_role`.

Roles retain their original meaning: AFFECTED (8 records), CONTRIBUTING_POPULATION (24), DEFINITION_EVIDENCE (3). Contributing population is not an affected count. The Customer_Order/DQ-DUP-CUSTOMER and Picking_Wave/DQ-DUP-PICKING pairs each preserve both AFFECTED and CONTRIBUTING_POPULATION. The two roles share one curve; neither record is dropped. Do not join this bridge physically to path points: it would fan out paths and duplicate role records.

## Context and metrics

Context: `issue_id, decision_category, title, review_state, business_decision, kpi_at_risk, business_mechanism, competing_explanations, next_evidence_request, recommendation, evidence_class, evidence_ref, claim_limit, source_count, lineage_record_count`.

All text comes unchanged from `decision_evidence.csv`, except `claim_limit` comes from the matching public issue's `residual_uncertainty`. The two integer counts are distinct associated source filenames and original lineage rows for that issue. They are relationship metadata, not risk estimates. Explanation alternatives are pipe separated. `evidence_class` remains AI_PROPOSED_REQUIRES_HUMAN_REVIEW. `review_state` is PENDING; no source correction or intervention is approved here.

Metrics: `issue_id, category, status, data_origin, unit, evidence_ref, metric_key, metric_id, affected_count, population, denominator, denominator_definition, calculation, additivity, cross_issue_sum_allowed`.

`affected_count` and `denominator` are nullable integers in this extract. Everything else is a string dimension, including `cross_issue_sum_allowed` (FALSE). `metric_key` uniquely identifies each measure; the same issue may have several incompatible units/populations. Preserve the original population, denominator definition, calculation and additivity beside any value. **Never sum across metric keys, issues, unit types, or focus slices.** A blank denominator remains unknown. Metrics are shown only in a secondary, expandable prototype section and a separate optional Tableau sheet.

## Single-source Tableau scaffold

Columns are `focus_issue, mark_kind, mark_id, node_id, node_type, edge_id, edge_kind, issue_id, source_id, decision_category, label, roles, lineage_count, path_order, x, y, edge_y, node_y, label_x, label_y, label_align, style_key, is_selected`, followed by context fields `title, review_state, business_decision, kpi_at_risk, business_mechanism, competing_explanations, next_evidence_request, recommendation, evidence_class, evidence_ref, claim_limit, source_count, lineage_record_count`.

Numeric fields: decimal `x,y,edge_y,node_y,label_x,label_y`; whole-number `lineage_count,path_order,is_selected,source_count,lineage_record_count`. All are non-additive across marks/slices; use MIN/ATTR as directed in the recipe. Other columns are strings. Empty fields are intentional for incompatible mark types.

There are 15 slices: `__ALL__` and each of the 14 issue IDs. Each slice has 30 NODE rows, 1,927 EDGE rows and **one CONTEXT row**. Geometry persists in every slice, enabling selection without removing the surrounding register. `is_selected=1` on the focused issue's real incident edges and their endpoint nodes; all marks are active in `__ALL__`. No orphan or category-neighbor expansion occurs. `style_key` combines node type / edge kind with `_ACTIVE` / `_CONTEXT`. CONTEXT rows have no XY and never produce graph marks. Only these rows carry panel text and source/lineage summary counts; this avoids repeating the panel's measures on every path point.

Filter `focus_issue=[pIssue]` before interpreting any scaffold count. This leaves 1,958 rows. Do not SUM `is_selected`, count scaffold rows as issues, or join metrics into the scaffold. For authoritative counts, use nodes/edges/lineage tables at their own grains, or source manifest constants clearly labeled as register counts.

## Provenance and safety boundary

The generator reads these four public extracts and verifies their hashes and column sets against existing manifests before building:

1. `docs/data-quality/advanced/public/issue_evidence.csv` → pair membership, original lineage IDs and roles.
2. `docs/data-quality/advanced/public/decision_evidence.csv` → issue titles, proposed categories and decision narrative.
3. `docs/data-quality/tableau/public/issues.csv` → issue domain, category agreement, residual uncertainty.
4. `docs/data-quality/tableau/public/issue_metrics.csv` → metrics copied without arithmetic reinterpretation.

It never reads raw source rows, internal extracts, secrets or local system paths. CSV publication guard rejects spreadsheet formula prefixes and local home paths. Automated tests check allowlisted schemas, SHA-256, original role preservation, exact edge coverage, endpoint geometry, selection context, source immutability and deterministic bytes. Public-safe means limited to these already approved public issue/metric fields; it does not turn AI-proposed interpretations into verified source truth.

Source attribution: Rodrigo Furlan de Assis, *Order Picking Dataset*, Mendeley Data v1, [DOI 10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), CC BY 4.0. Registry calculations and interpretations retain the evidence classes of their existing contracts.
