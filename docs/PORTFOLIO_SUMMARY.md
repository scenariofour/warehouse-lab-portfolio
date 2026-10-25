---
title: Warehouse Lab
summary: A 3D warehouse simulator and Tableau analytics portfolio that makes data-quality assumptions visible before they become operational decisions.
cover: /images/warehouse-overview.png
coverAlt: Warehouse Lab showing a 3D footwear warehouse with storage racks, ten autonomous robots, simulation controls and operational metrics.
status: Published
---

# Warehouse Lab

## Portfolio description

Warehouse Lab explores how warehouse data quality shapes operational decisions. I built an interactive Three.js digital twin from a published footwear order-picking dataset, with 2,292 storage locations and a deterministic simulation of ten autonomous robots. A Python pipeline verifies source hashes, preserves record lineage and prepares analytical extracts. Tableau dashboards connect issue summaries with normalization sensitivity, wave-level reconciliation and matching-key evidence. The project makes its assumptions explicit: storage tokens, spatial scale, order grouping and stock quantities require interpretation, while unequal policy inventories prevent causal rankings. Its contribution is a reproducible way to investigate discrepancies and communicate what the evidence can support. The simulator, dashboards, validation records and worksheet learning notes form a portfolio of data engineering, operations analysis, interactive visualization and evidence-based product judgment.

## Key contributions and verified skills

- TypeScript simulation: fixed-step execution, replay, stock reservations, event accounting and A* routing.
- Three.js: instanced warehouse geometry, robot visualization, selection and camera controls.
- Python and SQLite: source validation, reconciliation, deterministic exports and independent computational checks.
- Tableau: worksheet grain, Measure Names/Values, interpretation parameters, wave investigation, classification comparisons and denominator-aware concentration analysis.
- Product and analytical judgment: issue contracts, evidence boundaries, limitations and experiment controls.
- Delivery: Vite, Playwright, Node.js tests and GitHub Pages configuration.

## Links and cover

- [GitHub source](https://github.com/scenariofour/warehouse-lab-portfolio)
- [Live simulation](https://scenariofour.github.io/warehouse-lab-portfolio/)
- [Data Quality & Decision Intelligence](https://public.tableau.com/views/WarehouseLabDataQualityDecisionIntelligence/Dashboard01-DataQualityOverview?:showVizHome=n)
- [Normalization & Interpretation Lab](https://public.tableau.com/views/WarehouseLabOperationsDecisionStudio/Dashboard02NormalizationInterpretationLab2?:showVizHome=n)
- [Reconciliation Investigation](https://public.tableau.com/views/WarehouseLabOperationsDecisionStudio/Dashboard3?:showVizHome=n)
- [Gap Concentration](https://public.tableau.com/views/WarehouseLabOperationsDecisionStudio/B04GapConcentration?:showVizHome=n)
- Cover source: [actual application screenshot](images/warehouse-overview.png). Copy it to an Astro site's `public/images/warehouse-overview.png` to use the suggested frontmatter. It shows the production build with modeled warehouse geometry; it is not a warehouse photograph.

## What I learned

The worksheet notes taught me to define grain before combining measures, calculate reconciliation at key level before aggregation, and keep a fixed population denominator when displaying a Top 20 subset. Comparing literal and inferred sizes made the cost of an undocumented assumption tangible. I also learned to distinguish visible dashboard behavior, repository-verified calculations, authoring guidance and QA that remains pending. These lessons are grounded in the existing [learning index](data-quality/advanced/tableau-workbook/LEARNING_INDEX.md) and [evidence register](data-quality/advanced/tableau-workbook/EVIDENCE_REGISTER.md); they are a reusable reflection draft for the owner to personalize.

## Creative Tableau project handoff

[The Anatomy of a Decision — copy-ready description, verified preview image, Tableau/GitHub/simulator links and limitations](control-tower/anatomy/PORTFOLIO_HANDOFF.md).

This separately published project adds an evidence constellation linking 11 sources, 14 issues and five proposed decision categories, with a `pIssue` investigation panel. The [worksheet case study](control-tower/anatomy/LEARN.md#worksheet-case-study-ct01ct07) explains Line/Path, dual axes, parameters, actions, tooltips and the corrections recorded during archiving. The separate personal website was not modified.
