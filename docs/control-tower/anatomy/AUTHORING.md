# Build the real Tableau dashboard

Start with **free Tableau Desktop Public Edition** for the full construction path, or try the core recipe in signed-in Public web authoring. No extension, paid feature, map service, spatial package or custom JavaScript is required. This construction recipe was written for the October 24 HTML prototype and CSVs. A manually authored Tableau Desktop version has since been [published](PUBLISHED.md). The dark palette and pixel placements below preserve the prototype recipe; the actual published version uses a warm editorial palette with Sage Green evidence and orange decision associations. See [capability evidence](CAPABILITIES.md) for historical observations and the separately dated publication review.

## 1. Connect and define view state

Connect to `tableau/tableau_marks.csv` as one text/CSV table. Do not join or relate other tables for the core build. Names below use the CSV's lowercase field names. Set all coordinates to Number (decimal), all identity/class/text fields to String dimensions, and `path_order` to Number (whole), then **Convert to Dimension**. Leave geographical roles unset. Use English field names unchanged to make these instructions reproducible.

Create a **String** parameter `pIssue`, allowable values **List**, current value `DQ-EXP-001`. Use “Add values from” `focus_issue` if available; otherwise enter this exact list. Display aliases are optional; underlying values must stay unchanged:

```text
__ALL__
DQ-RECON-001
DQ-LOC-001
DQ-ABC-001
DQ-EXP-001
DQ-STOCK-001
DQ-LAYOUT-001
DQ-DUP-CUSTOMER
DQ-DUP-PICKING
DQ-SIZE-001
DQ-SIZE-002
DQ-QTY-001
DQ-LOC-002
DQ-MASTER-001
DQ-ID-001
```

Show the parameter control as **Single Value (dropdown)**. Alias `__ALL__` to “All registered associations.” The control is the core selection interaction; do not make a filter action remove surrounding geometry.

Create calculated fields:

```tableau
// Focus slice
[focus_issue] = [pIssue]

// Panel row
[mark_kind] = "CONTEXT"

// Question heading
IF [focus_issue] = "__ALL__" THEN "Choose an investigation question"
ELSE [issue_id] + CHAR(10) + [title] END

// Decision text
IF [focus_issue] = "__ALL__" THEN
  "Select one question to reveal its registered evidence trail."
ELSE [business_decision] END

// Alternatives text
REPLACE([competing_explanations], " | ", CHAR(10) + "• ")

// Review text
"AI-proposed framing • Human review pending" + CHAR(10) +
IFNULL([claim_limit], "")

// Evidence summary (integer counts exist only on the one context row)
IF [focus_issue] = "__ALL__" THEN "33 evidence pairs · 35 lineage records"
ELSE STR([source_count]) + " sources · " + STR([lineage_record_count]) + " lineage records" END

// Issue to select — optional parameter action only
IF [mark_kind] = "NODE" AND [node_type] = "ISSUE"
THEN [issue_id] ELSE [pIssue] END
```

Apply `Focus slice=True` to **all worksheets using this data source**. Keep it workbook-wide. A single focus slice has 1,958 rows before worksheet-specific filters. Do not put `Panel row` on the network sheet.

## 2. Required worksheets, exact shelves

### CT01 · Evidence constellation

| Shelf / control | Exact setting |
|---|---|
| Columns | `MIN(x)`, continuous |
| Rows | `MIN(edge_y)`, continuous; then `MIN(node_y)`, continuous |
| Layering | Dual Axis on `MIN(node_y)`; Synchronize Axis; edit both Y axes to fixed 0–760, **Reversed**; X fixed 0–1000 |
| Filters | `Focus slice=True` only. Keep EDGE and NODE rows together. CONTEXT has null XY and produces no graph mark |
| All Marks | Leave Detail, Path, Color, Shape, Label empty; configure each layer separately |
| Edge Marks card | Line; `edge_id` on Detail; discrete numeric `path_order` on **Path**, ascending numeric; `style_key` on Color; constant thin Size; no arrow or area fill |
| Edge Tooltip | `ATTR(edge_kind)`, `ATTR(issue_id)`, `ATTR(source_id)`, `ATTR(decision_category)`, `ATTR(roles)`, `ATTR(lineage_count)`, followed by “Registered association. Curve length, position and direction have no analytical meaning. Decision associations are AI proposed.” |
| Node Marks card | Shape; `node_id` on Detail; `node_type` on Shape; `style_key` on Color; `ATTR(label)` on Label; constant Size |
| Node Tooltip | `ATTR(node_type)`, `ATTR(label)`, `ATTR(issue_id)`, `ATTR(source_id)`, `ATTR(decision_category)`; “Choose an issue in the parameter selector. Decision framing requires human review.” |
| Node shapes | SOURCE = native diamond, ISSUE = native circle, DECISION = native square; no size field |
| Node label | DM Sans if rendered consistently, otherwise Arial; 9–10 pt; position right middle; allow label overlap only after checking all labels individually |
| Sort | Edge path order ascending 0–40; no sorting by measures. Do not put `path_order` on Color or on the node card |
| Fit / chrome | Entire View; hide headers after range checks; no gridlines, zero lines, dividers, row/column bands, sheet title or captions; pane/background `#091720` |

Map the discrete Color values manually; they are styling categories, not measures:

| style_key | Hex |
|---|---|
| EVIDENCE_ASSOCIATION_ACTIVE | `#7FD9C7` |
| EVIDENCE_ASSOCIATION_CONTEXT | `#18353E` |
| DECISION_ASSOCIATION_ACTIVE | `#E3B781` |
| DECISION_ASSOCIATION_CONTEXT | `#34342F` |
| SOURCE_ACTIVE / ISSUE_ACTIVE | `#B1F0D9` |
| SOURCE_CONTEXT / ISSUE_CONTEXT | `#638F91` |
| DECISION_ACTIVE | `#E3B781` |
| DECISION_CONTEXT | `#957953` |

Use a modest constant line size and moderate opacity for the edge card; keep node opacity 100%. Active/context color is precomputed so no measure-driven opacity is necessary. The line path has 41 ordered points per edge; it is not a smoothed time series. Tableau renders sampled segments rather than the HTML's exact cubic primitive, with identical source geometry.

Both layers intentionally contain null measures for the other mark type. Hide the null indicator if necessary; **do not choose Filter Data** on that indicator, which can remove a layer. Check each layer's expected marks: 47 paths and 30 node groups. Depending on Tableau version, the status bar may report underlying path points rather than path groups; inspect `COUNTD(edge_id)` on an EDGE-only audit sheet, not the raw status number.

The HTML positions some issue labels to the left to protect negative space. Core Tableau automatic labels need a visual pass; adjust individual label positions in Desktop if necessary. Label text abbreviations are editorial and full titles remain available in the context panel. Do not use the static overview SVG behind live marks, which would duplicate the network.

### CT02–CT07 · Investigation panel

Duplicate a blank text worksheet six times. For **each**: Columns empty; Rows empty; Marks **Text**; Filters `Focus slice=True`, `Panel row=True`; Detail empty; Color constant `#E6EEE9`; Tooltip disabled; Fit Entire View; hide title, headers, dividers and borders; background `#10212B`. Text alignment top left, Wrap on. Insert the specified aggregate into the Text editor; all fields are from exactly one context row after filtering.

| Sheet | Marks Text | Formatting / content |
|---|---|---|
| CT02 · Question | `ATTR(Question heading)` | Issue ID and full title, Georgia 19–21 pt; pending review label as adjacent dashboard text |
| CT03 · Business decision | `ATTR(Decision text)` | Arial 10 pt, full source-backed text; preceding dashboard label “THE BUSINESS DECISION” |
| CT04 · Competing explanations | `ATTR(Alternatives text)` | Arial 10 pt; literal alternatives split across lines; “COMPETING EXPLANATIONS” label |
| CT05 · Next evidence | `ATTR(next_evidence_request)` | Georgia 12 pt warm white; amber border/background container; “THE NEXT PIECE OF EVIDENCE” label |
| CT06 · Review and limits | `ATTR(Review text)` | Arial 9 pt; keep full residual uncertainty in tooltip if panel room is insufficient, and show the AI-proposed/pending sentence visibly |
| CT07 · Evidence summary | `ATTR(Evidence summary)` | Arial 10 pt mint; metadata counts, not performance KPIs |

If the first alternatives bullet is desired, prepend `"• "` to the text expression for nonblank alternatives. The supplied formula preserves all alternatives and inserts subsequent bullets. Do not shorten alternatives into asserted causes. CT05 is intentionally blank in `__ALL__`; a dashboard static prompt can explain selection, while CT02/CT03 supply the clear state.

### Optional CT08 · Role ledger

Connect separately to `tableau/lineage_roles.csv`. Create `Role focus = [pIssue] = "__ALL__" OR [issue_id] = [pIssue]`. Rows `issue_id`, `source_id`, `lineage_role`; Columns empty; Marks Text `ATTR(lineage_id)`; Detail empty; Color constant teal; Filters `Role focus=True`; tooltip repeats all four IDs/role. Show as a lower detail section or on a second dashboard tab. There must be two role rows for each multi-role pair. Do not join it to geometry and do not label all 35 records “affected.”

### Optional CT09 · Individual source metrics

Connect separately to `tableau/issue_metrics.csv`; filter `[issue_id]=[pIssue]`. Rows `metric_key` (dimension). Columns empty; Marks Text: `ATTR(affected_count)`, `ATTR(unit)`, `ATTR(population)`, `ATTR(denominator)`, `ATTR(denominator_definition)`, `ATTR(calculation)`, `ATTR(additivity)`. Color constant; Detail empty; Tooltip explicitly includes `cross_issue_sum_allowed`. Hide grand totals/subtotals. Keep metric keys as separate rows, never sum. In `__ALL__` this sheet is intentionally empty. Use it below the first fold, preserving the visualization-led hierarchy.

## 3. Fixed desktop dashboard, no fragile overlay required

Start at **1600×1000**, navy `#08141D`, zero outer padding, hidden sheet titles. Coordinates below are dashboard pixels, not the CSV's geometry coordinates. Build with floating placement for precise editorial proportions in Desktop, or nested tiled containers using the same sizes. The core network itself is **one dual-axis worksheet**; it does not require transparent stacked chart worksheets.

| Object | X / Y | Width / Height | Notes |
|---|---|---|---|
| Masthead | 28 / 16 | 1544 / 48 | Brand left; optional guide link right, no external URL action required |
| Headline + eyebrow | 28 / 82 | 1170 / 80 | “The Anatomy of a Decision”, Georgia 36; mint italic final phrase |
| Chart frame | 28 / 178 | 1200 / 794 | 59.6% of viewport; thin dark border |
| CT01 worksheet | 44 / 214 | 1168 / 708 | Within frame, no visible axis titles or toolbars |
| Legend / caveat | 50 / 931 | 1156 / 26 | Diamond / circle / square key; “Connections ≠ causes” |
| Investigation background | 1252 / 178 | 320 / 794 | `#10212B`, 2 px mint top edge |
| pIssue control | 1274 / 246 | 276 / 48 | Always visible; human-readable aliases optional |
| CT02 | 1274 / 315 | 276 / 142 | Full issue title; pending label adjacent |
| CT03 | 1274 / 478 | 276 / 90 | Use source text, wrap |
| CT04 | 1274 / 586 | 276 / 94 | All alternatives visible |
| CT05 | 1274 / 705 | 276 / 139 | Amber bordered container with heading above text |
| CT06 | 1274 / 859 | 276 / 61 | Visible review caveat; full uncertainty in tooltip |
| CT07 | 1274 / 932 | 276 / 27 | Source and lineage metadata |
| Register footer | 28 / 976 | 1544 / 24 | 14 issues / 11 sources / 35 lineage records / 33 pairs, secondary 9 pt |

Verify text wrapping for **all 14 issues**; these are starting construction dimensions, not a claim that a workbook layout was tested. CT06 can move to a lower detail dashboard if needed, but the pending/AI-proposed statement must stay visible. Use a native top-level vertical container and a horizontal chart/panel container if exact floating placement is unavailable. Fixed-size geometry is more predictable than Automatic layout. On a smaller display use dashboard scrolling; design and test a separate phone layout in Desktop later. HTML responsiveness is not automatically transferred to Tableau.

Optional decoration: a small dashboard Text object in the empty ring center can display the prototype's two-line editorial phrase. Native lines/shapes remain interactive. Do not place decorative objects over nodes. The SVG overview is a reusable static reference/export, not a substitute for the live worksheet.

For exact label placement beyond native automatic labels, the scaffold includes `label_x,label_y,label_align`. An **optional Desktop-only construction route to validate** is a second dual-axis Text worksheet with `MIN(label_x)` on Columns and two row measures: `IF [mark_kind]="NODE" AND [label_align]="left" THEN [label_y] END` and its right-aligned counterpart. Set fixed axes identical to CT01; Text cards get node_id on Detail and ATTR(label) on Text; use left alignment on the first and right alignment on the second. Remove CT01 labels, set label sheet background to None, and align plot bounds exactly. This additional overlay can intercept selections, so it is **not part of the core build**: use the selector and verify interactions, or retain native labels. Its Public rendering and transparent layering are unverified in this session.

## 4. Optional issue-click action, Desktop route

Dashboard → Actions → Change Parameter. Source CT01; Run on **Select**; target `pIssue`; source field **Issue to select**, aggregation **None** (one value per mark); clearing selection **Keep current value**. Use the guarded calculated field above, so clicking an edge, source or category retains the current issue. Keep the dropdown available. A “View all” state is selected explicitly via `__ALL__`; no clearing-action trick is necessary.

If Public web authoring lacks this action dialog, skip it or author it in free Desktop Public Edition and test after publishing a **new** workbook. The full analytical selection works via the parameter control alone. No exact incident-edge hover action parity is claimed; native tooltips are the dependable fallback. Do not configure Use as Filter on CT01, because it can remove context or filter away the panel.

## 5. Acceptance checklist for a Tableau publication

Follow [the interaction acceptance checks](INTERACTIONS.md). Also inspect numeric data types, fixed/reversed axes, no Path aggregation, no raw SUM metrics, no joins that fan out paths, no geometry mapped as latitude/longitude, and no fabricated direction/weight encodings. Compare the default and reconciliation screenshots under `review/` with the authored dashboard. Test Save/reopen, manual parameter changes, optional actions, tooltip content, keyboard use and a published Public view separately.

Historical implementation boundary (October 24 prototype task): no workbook was authored by that task. The owner subsequently built and published CT01–CT07 in Desktop. For reconstruction, connect Desktop Public Edition to `tableau/tableau_marks.csv`, build CT01 first, then assemble the text sheets. Use [PUBLISHED.md](PUBLISHED.md) for observed online behavior and outstanding acceptance items; the original pixel recipe is not a measurement of the published dashboard.
