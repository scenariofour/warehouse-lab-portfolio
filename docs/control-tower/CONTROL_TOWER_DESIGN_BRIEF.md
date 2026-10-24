# M5 — Operations Decision Control Tower

**Design proposal · 2026-10-21 · Approval pending.** This package contains documentation and a local HTML design mockup. It does not contain a Tableau workbook or authorize authoring, publishing, source correction, an operational intervention, or a gate decision.

[Open the mockup](index.html) · [Data contract](CONTROL_TOWER_DATA_CONTRACT.md) · [Tableau feasibility and plan](CONTROL_TOWER_TABLEAU_PLAN.md) · [Learning plan](CONTROL_TOWER_LEARNING_PLAN.md)

## View the review artifact

Open `docs/control-tower/index.html` directly in a browser; it uses local fonts and embedded, pinned presentation content, with no installation or server required. Select any issue, filter the map by source, expand the evidence drawer, and use Reset review. These local demonstrations do not test or configure Tableau. The published analysis links open separate existing views without passing selection context. [Desktop preview](review/desktop.jpg) and [narrow preview](review/narrow.jpg) document the inspected rendering; [review results](review/design-review.json) separate local checks from untested Tableau behavior.

## Intended outcome and audience

Help an operations leader decide **what can be concluded, what must be withheld, and which evidence to request next**. Demonstrate that a persuasive BI application can make uncertainty usable without turning extract discrepancies into warehouse failures.

Primary audience assumption: an operations/research sponsor reviewing the published footwear dataset, rather than a dispatcher running a live warehouse. Secondary audiences: a data analyst investigating source definitions and a portfolio reviewer assessing business judgment, lineage, and Tableau interaction design. No real participating stakeholder or reviewer is implied.

The business job is to protect the next operating decision from an unreliable baseline. A successful session ends with a bounded question and a small, explicit evidence request. It need not end with a policy winner or an intervention. The dashboard is an executive entry point to existing analysis, not a replacement for the reconciliation and normalization dashboards.

## Repository audit and reuse decisions

Audit base: current branch `codex/data-quality-foundation`; exact base commit and preservation results are recorded in [review/design-review.json](review/design-review.json). Existing unrelated untracked discovery files were read as context and excluded from this delivery. No input file, generator, simulation, prior document, gate record, or published workbook is edited.

| Existing asset | Authority and reuse | M5 decision |
|---|---|---|
| [Issue contract](../data-quality/CONTRACT.md), [registry](../data-quality/registry/README.md) | 14 investigation questions, 18 metrics, uncertainty and review semantics | Reference directly; no second issue registry |
| [M3 specification](../data-quality/TABLEAU_SPEC.md), [extract manifest](../data-quality/tableau/manifest.json) | Public issue, metric, decision-impact and source-count extracts | Reuse public extracts; no duplicated CSVs |
| [Advanced dictionary](../data-quality/advanced/DATA_DICTIONARY.md), [decision layer](../data-quality/advanced/DECISIONS.md), [manifest](../data-quality/advanced/manifest.json) | 14 existing public tables, including decision requests, interpretation alternatives, controls and lineage | Reuse only required tables, preserve original definitions |
| [Delivery notebook](../data-quality/advanced/tableau-workbook/README.md), [evidence register](../data-quality/advanced/tableau-workbook/EVIDENCE_REGISTER.md) | Two delivered dashboards, eight authored worksheets; separates observation from reconstruction | Link to existing work instead of rebuilding B/C investigations |
| [Existing QA](../data-quality/advanced/tableau-workbook/QA_AND_MAINTENANCE.md) | Branch/action/reset and uploaded-extract QA still incomplete | Carry those limits forward; do not mark them passed |
| `docs/OPERATIONS_DECISION_BRIEF.md`, `docs/WAREHOUSE_DISCOVERY_REPORT.md` | Pre-existing untracked work, including conditional assumptions | Context only; no new source for M5 measures or hypothetical economics |
| [Project charter](../PROJECT_CHARTER.md), [gate register](../GATE_REVIEWS.json) | Research intended use; G0–G4 pending | Preserve all gate states and frozen MVP |

Earlier M3 documents say no workbook existed at that milestone; the later delivery notebook records publication. Use the later evidence register for delivery status without rewriting historical documents. There is no tracked `.twb`, `.twbx` or `.hyper`; the validated CSV extracts are the available local handoff, not proof of uploaded Tableau byte identity.

## Decisions and alternatives

1. **Recommend: decision-first evidence tower.** A visible recommendation, bounded KPIs, dependency map, decision exposure, and evidence-request queue. Fits the actual evidence; offers distinctive BI work without inventing operational telemetry.
2. **Issue-reporting grid.** Fast to author but repeats the existing foundation and buries business judgment in a table.
3. **Live operations cockpit.** Visually familiar but requires completion events, service targets, costs, timestamps and validated physical quantities that are absent. Excluded from this design.

The signature element is an **Evidence Dependency Map**: source columns × investigation rows, followed by a selected decision explanation. This is an incidence matrix of documented analytical dependencies, not a causal graph, workflow progress chart, physical warehouse map or weighted risk network.

## Business questions and hierarchy

| Reading order | User question | Proposed component | Decision boundary |
|---|---|---|---|
| First glance | Should we recommend a storage policy? | Navy recommendation band: “Hold the storage-policy recommendation.” Six unequal SKU-counter pairs; approval still pending | AI-proposed research judgment, not a changed gate or operating instruction |
| Evidence | What does the extract actually show? | Three KPI cards: reconciliation, coordinate coverage, ABC disagreement | Separate units and denominators; no combined affected total |
| Dependencies | Which questions depend on the same sources? | Source × issue matrix, role legend, selected issue | Shared source is not shared affected population or causation |
| Decision exposure | What claim would be premature? | Category counts and selected issue's decision, mechanism and claim limit | Counts are questions; exposure has no monetary/risk score |
| Uncertainty | What could explain this result? | Competing explanations and “Not established” panel | No asserted root cause, physical stock, savings or readiness score |
| Investigation | What is the smallest next evidence request? | Four curated starting points; full 14-issue selection remains available | Editorial sequence, not an estimated value-of-information ranking |
| Drill | Where can I inspect the analysis? | Existing published investigation and normalization views; local evidence notes | External navigation does not promise a filtered destination |

Default focus is DQ-EXP-001. The global recommendation and three KPI cards retain full-extract scope while selecting another issue. The selected panel is visibly titled with its issue ID; category counts retain their own “All 14 questions” scope. There is no date picker or warehouse/supplier selector unsupported by the extracts.

## Visual system and composition

Palette: ink navy `#142B40`, header navy `#102638`, restrained teal `#176B68`, warm canvas `#F3F1EC`, white surfaces `#FFFFFF`, investigation amber `#8A5A16`. Text secondary `#536371`; dividers `#D9DFDF`. Amber denotes clarification, not verified failure; teal denotes selection/evidence, not success. Text labels accompany every state.

Type: existing local DM Sans for interface and reading; existing Manrope for headings and numeric emphasis. In Tableau, use Arial as a reliable baseline unless the deployed renderer demonstrably supports the preferred faces. Never depend on custom fonts for layout. Sentence case, tabular numbers, left-aligned explanations, right-aligned comparable quantities. Minimum target 12 px labels and 14 px reading text at the intended desktop size; visible scope/limitations are not hidden in tooltips.

Composition: a narrow navigation rail, a navy application header, a prominent recommendation band, then three quiet KPI cards. A wide matrix sits beside a narrower decision panel; a lower band pairs investigation priorities with interpretation sensitivity and unknowns. Use 8 px spacing increments, 24 px section padding, 16 px gaps, small surface radii and almost no shadow. Distinctive structure comes from the dependency matrix and decision framing, not ornamental logistics imagery.

```text
┌──────────┬───────────────────────────────────────────────────────────┐
│ Warehouse│ Operations Decision Control Tower / snapshot / mockup     │
│ Lab      ├───────────────────────────────────────────────────────────┤
│          │ Hold recommendation          │ smallest evidence request  │
│ Overview ├──────────────────┬───────────────────┬────────────────────┤
│ Evidence │ demand gap       │ coordinate gap    │ ABC disagreement   │
│ Queue    ├──────────────────────────────────────┬────────────────────┤
│          │ Evidence Dependency Map             │ Decision exposure  │
│ Existing │ 14 questions × 11 sources           │ selected issue,    │
│ analysis │ roles; no-link ≠ complete coverage  │ causes, next ask   │
│          ├──────────────────────────────────────┼────────────────────┤
│          │ Investigation priorities            │ Sensitivity and    │
│          │ curated starting points             │ unknowns           │
└──────────┴──────────────────────────────────────┴────────────────────┘
```

Target Tableau desktop canvas: 1440 × 2000, vertically scrollable on shorter screens. The HTML reflows for review at narrow widths, with the matrix in its own horizontal scroll region. HTML responsiveness is not evidence of Tableau device-layout support; a later Tableau narrow layout requires separate construction and QA.

## Reference study and limits

Read-only browser study on 2026-10-21: each exact title/author and the initially visible dashboard region were inspected visually. Some right/lower content was outside the viewport. No dashboard filter, parameter branch, hover/drill action, export, calculation or hidden workbook configuration was tested; no claim is made about those interactions. No artwork, logos, screenshots or layout assets from these works are included in M5.

| Reference | Direct inspected view | Principle adapted, not copied |
|---|---|---|
| Amazon Sales Overview #VOTD — Mila Kholodii | [Sales view](https://public.tableau.com/app/profile/mila.kholodii/viz/AmazonSalesOverview_17899965275850/AmaonSalesPerformance) | Coherent application framing and consistent metric framing; omit period comparisons unsupported here |
| Supply Chain Performance & Vendor Operations — La'Princia Mance | [Performance view](https://public.tableau.com/app/profile/laprincia.johnson/viz/SupplyChainPerformanceVendorOperations/SupplyChainPerformanceOverview) | Navy header, aligned KPI rhythm, navigation separated from analysis; no supplier measures imported |
| Hospital ER Operation - Healthcare Analytics — Hue Vuong | [ER view](https://public.tableau.com/app/profile/hue.vuong1433/viz/EmergencyRoomOperation/ERDashboard) | Restrained teal and readable grouped panels; no sparkline without a defensible historical series |
| Northstar Logistics — Karen Biltcliffe | [Control tower](https://public.tableau.com/app/profile/karen.biltcliffe/viz/NorthstarLogisticsOperationsControlTowerBusinessDashboard/OperationsControlTower) | Prominent performance-watch narrative before detailed charts; M5 uses evidence prerequisites rather than operational performance claims |

The reviewed plan avoids an interchangeable KPI grid by making the next decision and its dependencies central. Sparklines, donut readiness scores, carrier/vendor maps and live-alert chrome were deliberately omitted because the supplied evidence does not support them.

## Review journeys and proposed success criteria

These are acceptance targets for the future workbook, not measured user-research results or gate criteria.

1. **Executive, 30 seconds:** state the recommendation, cite the six unequal pairs, and name the common SKU-quantity ledger as a next request. Recognize that no operational policy effect is established.
2. **Analyst, two minutes:** select DQ-RECON-001, identify its two contributing sources, explain 13,003 / 228,195 and the current inferred-size basis, then reach the existing reconciliation analysis. No inferred order-level fulfillment rate.
3. **Reviewer:** find a source-definition dependency, name a competing explanation, and distinguish blank financial/physical quantities from zero. Explain why literal-size sensitivity is not an approved correction.

Arithmetic must match the contract exactly before rounding. Selection must never change the three global KPI denominators. All 35 lineage records, including both roles on two repeated-record cells, must remain inspectable. No cross-issue affected sum, source-row fanout, readiness percentage, policy winner or invented financial value may appear. Nulls, multi-selection, no rows, clear/reset, keyboard access, text contrast, link targets and narrow rendering require explicit checks.

Approval requested only after reviewing this package: accept/revise the narrative, composition and dependency-matrix approach. **Stop here until design approval.** The Tableau plan is a feasibility specification for that review, not the start of authoring. All later Tableau authoring, publishing and application work remains outside this delivery.
