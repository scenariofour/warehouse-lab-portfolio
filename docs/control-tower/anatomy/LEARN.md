# Reproduce the constellation independently

You need Python 3.9+ (standard library only) to generate geometry, a browser to explore the prototype, and free Tableau Desktop Public Edition or a working signed-in Public authoring session to construct the workbook. Node/npm is only needed to run this repository's browser tests.

## 1. Begin with the question, not the drawing

The registry already contains 14 unresolved issues. Every issue has a title, evidence association and proposed decision category. Read DQ-EXP-001 in the public decision extract: the question is whether unequal inventory permits a defensible placement-policy comparison. Its five registered sources support an investigation; they do not prove which explanation is correct.

The panel separates **decision**, **competing explanations**, and **next evidence request**. Follow those three fields for each selected issue. “AI proposed / human review pending” is part of the meaning, not a decorative disclaimer.

## 2. Understand the three different grains

- **Node:** one source, issue or decision category. There are 30.
- **Association:** one occupied source/issue pair (33), or one registered issue/category assignment (14). There are 47 drawn curves.
- **Lineage record:** one original role-bearing registration. There are 35. Two evidence pairs each have two roles, so 35 is not the number of evidence curves.

Look up DQ-DUP-CUSTOMER in `lineage_roles.csv`: both AFFECTED and CONTRIBUTING_POPULATION belong to the same source/issue pair. Draw one curve and preserve both roles in the ledger. An inner join against an analytical-source-only table would lose the definition-only sources; the generator instead takes the full source domain from issue_evidence.csv.

## 3. Separate presentation from evidence

Open [the generator](../../../scripts/control_tower/build_constellation.py). `load_sources` checks the four allowlisted public extracts against their existing manifests. `make_model` checks population, domain and role constraints, then assigns fixed editorial arcs. The short labels and coordinates improve legibility. They do not estimate importance, severity, similarity, travel distance or performance.

Each association uses a cubic Bézier curve. The two endpoints are its nodes; the two control points make its tangent calm and horizontal. At t=0 the curve is exactly the first node; at t=1 it is exactly the second. At t=0.5 its coordinates equal `(P0+3C1+3C2+P1)/8`. The integrity test checks that midpoint independently. Forty equal intervals produce 41 ordered points, suitable for Tableau's Line/Path mark. No random seed, force simulation, clustering or measured distance is involved.

Experiment in a temporary output directory, preserving the checked-in assets:

```sh
python3 -B scripts/control_tower/build_constellation.py --output-dir /tmp/m5-constellation-practice
```

Compare its manifest and CSVs with this directory. They should be byte-identical when the source and generator are unchanged. To try a different layout, edit the generator on a separate branch, regenerate and rerun tests; change only presentation parameters, never silently add relationships.

## 4. Learn why the selector scaffold exists

Tableau needs selection to emphasize a neighborhood while leaving other nodes visible. A normal issue filter can discard sources and curves. The scaffold precomputes 15 views: all associations, then each single-issue focus. Every view retains the same geometry; only the active/context style changes.

Pick `focus_issue=DQ-EXP-001` in the scaffold. There are 30 node rows and 47×41 path rows, plus one context row. Six paths are active: five evidence associations and one category assignment. That selection has exactly five sources, the focused issue and one category. No other issue is selected merely because it shares a source. The full scaffold repeats geometry, so its raw row count is not a KPI.

## 5. Build one worksheet before styling a dashboard

Follow [AUTHORING.md](AUTHORING.md), starting at CT01. First render just the paths with `MIN(x)` / `MIN(edge_y)`, edge_id Detail, path_order Path. Then add the node axis and synchronize/reverse it. Fix the ranges and inspect endpoints before hiding axis chrome. Finally add pIssue and the Boolean focus filter. This order makes alignment and selection errors visible while they are still easy to diagnose.

Build the six text worksheets only after the graph works. Use the one CONTEXT row to display full narrative text. Add role and metric tables as separate sources only if needed; do not join their many rows onto path points.

## 6. Use an acceptance example you can explain

Select DQ-RECON-001. Trace the source associations, read the proposed decision about eligible requested work, and compare the alternative explanations. The next evidence request asks for line statuses, cancellations and aligned extraction times. This is evidence planning, not proof that the gap is a fulfillment failure.

Then inspect the separate metrics: gap units and positive-gap keys use different units and denominators. Keep each metric_key and denominator definition visible. A mathematically reproducible calculation can still have unresolved source semantics.

Run the Python integrity tests and browser tests from the README. They verify data coverage, geometry and HTML interactions. They do **not** certify a Tableau workbook. The owner subsequently authored and published CT01–CT07. The [publication review](PUBLISHED.md) records the separate online checks; save/reopen and all issue-click Parameter Action branches remain distinct QA items.

## Troubleshooting

| Symptom | Check |
|---|---|
| One tangled path through everything | edge_id belongs on Line Detail; path_order belongs on Path |
| Curves zigzag | path_order must be numeric dimension, ascending 0–40, not alphabetic string or SUM |
| Nodes mirrored vertically | Synchronize both Y axes, then use the same fixed reversed 0–760 range |
| A layer disappeared | Undo any Filter Data operation on the null indicator; only hide the indicator |
| Selecting an issue hides the surrounding graph | Filter focus_issue against pIssue, not issue_id; disable Use as Filter |
| Counts are enormous | Do not count replicated path/scaffold rows; inspect the correct grain in SCHEMA.md |
| Some source nodes vanished | Do not restrict the 11-source domain to an analytical CSV subset |
| Web action/layout dialog missing | Use the manual parameter selector / tiled layout, or free Desktop Public |
| Labels overlap | Preserve fixed axes; adjust labels in Desktop, or keep the selector as the full-title navigation |

## Worksheet case study: CT01–CT07

This case study connects the existing recipe to the real published project. The owner created the Desktop implementation manually. The published accessibility description independently identifies Line and Shape layers, MIN coordinates, Path Order on Path, Edge Id on Detail, Node Id, Issue to select and the six text worksheets. The inspected local `.twb` is an earlier **Sheet 1** draft: it confirms Line Marks, Edge Id Detail, ordinal integer Path Order, fixed X and reversed Y, and `Focus slice`; it cannot establish the final dashboard's hidden settings. Shelf recipes below explain construction choices rather than claiming full final-workbook inspection.

### CT01: Line Marks, Edge ID and Path Order

One line represents one registered association. `edge_id` on **Detail** partitions points into 47 curves; `path_order` on **Path** orders the 41 sampled positions within each curve. They answer different questions: “which curve?” and “which point comes next?” Using Path Order as the only identity can connect unrelated associations; using Edge ID as a sequence cannot reconstruct a curve. The sampled Bézier points let Tableau draw the same deliberate layout as the HTML without a map service or extension.

**Dimension versus Measure** is about analytical role, independently of numeric data type or discrete/continuous display. Edge ID is a string dimension; Path Order is an integer **ordinal dimension**, sorted numerically 0–40. Summing it would destroy sequence. X, Edge Y and Node Y are continuous measures rendered with MIN to recover the fixed coordinate for each mark, not to measure warehouse performance. The local draft confirms these roles; the published view exposes MIN(X), MIN(Edge Y), MIN(Node Y) and Path Order.

### CT01: Dual Axis and synchronized coordinates

The Line layer uses `MIN(edge_y)` and the Shape layer uses `MIN(node_y)`, sharing `MIN(x)`. Dual Axis places both in one worksheet so source diamonds, issue circles and decision squares meet their curve endpoints. Synchronize Y, fix both ranges to 0–760 and reverse them; fix X to 0–1000. Reversal matches the top-left origin of the source geometry. Automatic or independently scaled axes can make a valid association appear detached. Verify endpoints before hiding headers. The online chart exposes both coordinate layers; exact final synchronization settings require the final workbook, which is not archived.

EDGE rows deliberately have null Node Y; NODE rows have null Edge Y. Hide the null indicator after checking the layers. “Filter Data” on that indicator can remove a whole mark type. Configure the two Marks cards separately; a Path field placed on All can fragment the node layer.

### CT01–CT07: parameters, calculated filters and selection-state scaffolds

`pIssue` is a string parameter with 14 issue IDs plus `__ALL__`. A parameter stores a value; it changes a view only through a referencing calculation. `Focus slice = [focus_issue] = [pIssue]`, filtered to True on every worksheet, chooses one of 15 precomputed views. Each view retains all 30 nodes and 47 curves, changing active/context styles instead of discarding surrounding evidence. Filtering `issue_id` directly would hide context and omit endpoint rows.

Each slice contains 1,927 edge-point rows, 30 node rows and one CONTEXT row: **1,958 rows, not 1,958 observations of risk**. The full CSV has 29,370 rows. Metadata and metrics must be interpreted at their declared grain, never summed across points or slices. Two pairs have two roles: 35 lineage records yield 33 evidence curves. Keep the optional role ledger separate so joining its multiple records cannot duplicate path geometry.

### CT01: Parameter Actions and tooltips

The published chart exposes an `Issue to select` field on Detail. The recipe's guarded calculation returns `issue_id` only for issue nodes and otherwise retains `pIssue`. A Change Parameter action can use that field on Select, targeting `pIssue`, with Keep current value on clearing. That makes a circle a navigation control while source, edge and category marks retain their meaning. A visible field does **not** prove the action is correctly configured: online circle clicks, non-issue clicks, clearing, repeated selection and keyboard activation remain separate QA. Keep the manual dropdown available.

Node tooltips should expose the full label, type and relevant identifier because spatial labels are abbreviated. Edge tooltips should expose association kind, issue/source/category, role set and `ATTR(lineage_count)` because role counts repeat at every path point. Include the registered-association and AI-proposed caveats. A source's other neighbors should not silently become the selected issue. The HTML's temporary incident-edge hover effect is not evidence of identical Tableau behavior; online tooltip completeness still needs checking.

### CT02–CT07: one context row, six narrative roles

CT02 shows the issue ID and question; CT03 the business decision; CT04 competing explanations; CT05 the next evidence request; CT06 review state and uncertainty; CT07 source/lineage metadata. Each filters `Focus slice=True` and `Panel row=True`, with `Panel row = [mark_kind] = "CONTEXT"`. ATTR displays the single row without inventing an aggregation. REPLACE converts pipe-separated alternatives to line breaks; the clear state uses a prompt rather than pretending to resolve an issue.

For DQ-EXP-001, the panel asks for an approved common SKU-quantity ledger before ranking allocation policies. Its five associated sources and five lineage records justify an investigation, not a causal ranking. DQ-RECON-001 instead asks for aligned line-status and extraction-time evidence. The publication review compares panel text and counts against the archived context CSV, independently of the HTML tests.

### Desktop formatting and dashboard composition

The owner adapted the original dark prototype into a **warm editorial composition**: Sage Green distinguishes evidence associations and orange distinguishes proposed decision associations. Color separates relationship types and focus state; it does not encode severity, probability or lineage role. The network remains the main graphic, with `pIssue` and CT02–CT07 forming a persistent investigation panel. Static headings and the source/uncertainty footer explain how to read it.

Use fixed coordinate ranges, controlled font size, text wrapping and worksheet Fit settings before removing axes, gridlines and redundant sheet titles. Build the chart before arranging dashboard objects so formatting cannot mask a geometry mistake. The original AUTHORING.md dimensions and dark hex values preserve the prototype construction recipe; they are not the final publication's measured layout or exact palette. Default and reconciliation screenshots record the published result. Full text wrapping across every state and a phone layout still require visual QA.

### Corrections and mistakes to remember

Documented project corrections are distinct from troubleshooting examples; no personal click history is inferred where none was recorded.

| Recorded correction or construction failure mode | Why it matters and how to correct it |
|---|---|
| Archive text still said no workbook was published | Updated current status and retained dated prototype evidence; publication does not retroactively validate earlier authoring claims. |
| Local workbook filename looked like the final project | XML inspection found one Sheet 1 and no dashboard. Excluded it from final-workbook publication instead of archiving a misleading artifact. |
| Confusing 35 lineage records with the number of evidence curves | Preserve 33 occupied pairs and both roles on each of two multi-role pairs; do not fabricate two extra curves. |
| Tangled or zigzag line (recipe troubleshooting) | Separate Edge ID on Detail from numeric Path Order on Path; never SUM the sequence or sort it as text. |
| Mirrored/misaligned nodes or a missing layer (recipe troubleshooting) | Synchronize and reverse both Y axes; hide intentional null indicators instead of filtering their rows. |
| Losing the surrounding network when selecting (recipe troubleshooting) | Use the focus-state scaffold and parameter calculation, not a direct issue filter or Use as Filter. |
| Giant or misleading totals (recipe troubleshooting) | Count at node, association or lineage grain; use ATTR/MIN for repeated metadata and keep different metric units separate. |

Self-checks: **One curve means?** One registered source–issue pair or one proposed issue–category assignment. **What changes with pIssue?** The chosen focus slice, emphasis and narrative; the underlying source data does not change. **What remains unproved?** Causality, physical warehouse outcomes, human approval and untested Tableau interaction branches.
