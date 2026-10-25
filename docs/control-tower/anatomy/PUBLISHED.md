# Published project and verification record

Reviewed October 25, 2026. The source implementation is development commit `e55b3415613ba3d5216d706519e561f36035c8d8` on `codex/data-quality-foundation`. The completed visualization was manually authored in Tableau Desktop by Iris Li and published separately. Tableau Public shows first and last publication dates of **October 24, 2026**.

**Exact live URL:** [The Anatomy of a Decision](https://public.tableau.com/app/profile/jiaxin.iris.li/viz/Warehouse_Lab_Anatomy_of_a_Decision/TheAnatomyofaDecision).

## Three artifacts, three evidence boundaries

| Artifact | Preserved evidence | What it establishes |
|---|---|---|
| HTML prototype and geometry kit | [Prototype](index.html), [generator](../../../scripts/control_tower/build_constellation.py), [manifest](manifest.json), [original captures and tests](review/README.md) | Deterministic geometry, public-source lineage and tested HTML behavior; dark prototype styling |
| Manually authored Desktop implementation | Owner's completed publication; inspected local one-sheet `.twb` draft; published worksheet inventory | Desktop authorship is owner-reported; the draft confirms early Line/Path construction, not final-workbook configuration |
| Published Tableau Public dashboard | Signed-out browser, public JavaScript API summary reads, [default capture](review/tableau-public-default.png), [reconciliation capture](review/tableau-public-reconciliation.png), [validation record](review/published-validation.json) | Live CT01–CT07, warm editorial composition, Sage Green evidence, orange decision associations and parameter-driven panel data |

The published design is the final visual reference. The HTML recipe's dark hex values and fixed placements are retained for learning; they do not document the publication's exact fonts, color codes or dashboard pixel settings.

## Registered structure and source attribution

The graph contains **11 source nodes, 14 issue nodes and 5 decision categories**: Measurement Baseline, Source Definition, Spatial Feasibility, Experiment Design and Slotting Hypothesis. There are **33 occupied source–issue pairs** backed by **35 role-bearing lineage records**, plus **14 issue–category assignments**, for **47 curves**. Each issue has exactly one proposed category. Two source–issue pairs each hold both AFFECTED and CONTRIBUTING_POPULATION roles; they remain one curve each. DEFINITION_EVIDENCE remains distinct. Coordinates, curve lengths, crossings, color and orientation do not quantify risk, confidence or causality.

The generator reads only the four manifest-pinned public extracts listed in [SCHEMA.md](SCHEMA.md#provenance-and-safety-boundary). The seven geometry/context/metric CSVs retain those fields and their grain; they contain no raw customer/order/wave/operator/location/reference identifiers. The 15 focus slices are presentation scaffolding, not new observations.

Underlying dataset: Rodrigo Furlan de Assis, *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*, Mendeley Data v1 (2024), [DOI 10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Geometry and narrative are Warehouse Lab adaptations; no endorsement is implied. Analysis and decision framing were AI-assisted; human review remains pending. See [asset and code licenses](LICENSE.md) and [source/third-party notices](../../../THIRD_PARTY_NOTICES.md).

## Confirmed online behavior

A signed-out browser loaded the exact URL and exposed the dashboard title, CT01–CT07 and `pIssue` with all 14 issue IDs plus `__ALL__`. CT01's accessible description identifies Line + Shape, MIN(X), MIN(Edge Y), MIN(Node Y), Path Order, Edge Id, Node Id, Style Key and Issue to select. Clicking the visible dropdown and choosing **DQ-RECON-001** changed the parameter and CT02 question to the reconciliation issue. This is a manual-control check, not a circle-click action check.

Separately, the Tableau public JavaScript API changed `pIssue` through all **15 states**, then read each worksheet's summary data. An independent comparison against the archived CSVs verified:

- 47 curves × 41 ordered points and 30 node identities remain present in every state; published X/Y values match the archived geometry.
- Every edge and node has the expected active/context style for the chosen issue; default DQ-EXP-001 has five evidence curves and one category curve active.
- All 14 issue states return the exact question, business decision, next evidence request, uncertainty and source/lineage summary. Competing explanations match after trimming bullet/whitespace formatting; the published review prefix says “AI-assisted framing · Human review pending.”
- `__ALL__` keeps all geometry active, shows “Choose an investigation question” and “33 evidence pairs · 35 lineage records.” CT03 and CT05 return null rather than the construction guide's proposed explanatory sentence. This observed difference is recorded, not silently treated as recipe parity.

Summary-data equality is evidence about exposed online values; it does not establish uploaded extract byte identity or hidden calculation definitions. Captures were taken after allowing the rendered sheets to settle following parameter changes. The default and reconciliation images were visually inspected; they are actual iframe screenshots including Tableau's toolbar, with no mockup generation or retouching.

## Workbook disposition

No `.twbx` was found in the searched local **Documents, Downloads and Desktop** folders. This is a scoped search, not a claim that no copy exists elsewhere. The available `Warehouse_Lab_Anatomy_of_a_Decision.twb` was inspected as XML without modifying it. It contains only **Sheet 1**, no dashboard, a `tableau_marks.csv` text connection, `pIssue`, `Focus slice`, a Line mark, Edge Id on Detail, ordinal integer Path Order, and fixed/reversed axes. It also carries an absolute local data directory and a temporary Hyper-extract reference. No nonblank password was present in its connection metadata. This unpackaged draft does not contain an inspectable packaged extract and is not the final seven-sheet publication.

**The final editable workbook has not been archived or cleared for redistribution.** Neither the draft nor a downloaded workbook is included in the public archive. Rebuilding from the public CSVs is possible, but cannot reproduce unrecorded final formatting and actions exactly. A future final `.twbx` needs member inventory, actual extract/schema/value review, local-path/privacy review and a reopen comparison before publication; the fact that it is downloadable from Tableau is not a package audit.

## Remaining QA

- Issue-node Parameter Actions: actual circle clicks across issues, repeated and non-issue clicks, clearing selection, multi-selection and keyboard activation. Presence of Issue to select on Detail does not prove action wiring.
- Native node/edge tooltip completeness, role semantics and hover restoration; no parity with HTML hover is asserted.
- Visual text wrapping/clipping for all 14 issues, label collisions, small screens, phone layout and accessibility beyond the sampled control.
- Final Desktop workbook save/reopen, exact synchronized-axis settings, hidden formulas, action definitions and uploaded data/extract byte identity.
- Source/domain interpretation and human approval. Registered links do not prove fulfillment failures, stockouts, losses, ROI or causal policy improvements.

No existing dashboard, simulator, model or analytical source was changed by this archive task. [Worksheet learning case study](LEARN.md#worksheet-case-study-ct01ct07) · [Portfolio handoff](PORTFOLIO_HANDOFF.md).
