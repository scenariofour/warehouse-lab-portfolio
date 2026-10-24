# Tableau delivery and learning notebook

Recorded 2026-10-18 · scenariofour · [Published Operations Decision Studio](https://public.tableau.com/views/WarehouseLabOperationsDecisionStudio/Dashboard3?:showVizHome=n).

The publication contains two delivered dashboards and eight authored worksheets. This notebook records the observed delivery and the reasoning needed to rebuild it. The earlier [blueprint](../BLUEPRINT.md) and [handoff](../TABLEAU_HANDOFF.md) remain historical design references, not proof that every proposed feature was implemented.

## Portfolio and evidence

- [Dashboard 02 — Normalization & Interpretation Lab](DASHBOARD_02_CASE_STUDY.md)
- [Dashboard 03 — Reconciliation Investigation](DASHBOARD_03_CASE_STUDY.md)
- [Evidence register: observed, reported, calculated, untested](EVIDENCE_REGISTER.md)
- [Calculation and authoring reference](CALCULATION_REFERENCE.md)
- [Remaining QA and maintenance for the next dashboard](QA_AND_MAINTENANCE.md)

## Learn by concept or worksheet

Start with the searchable [LEARNING_INDEX](LEARNING_INDEX.md). Each note has a question, grain, equivalent web-authoring recipe, interaction scope, debugging lessons and three answered self-checks.

| Worksheet | Role | Delivery placement |
|---|---|---|
| [B01 — Reconciliation by Wave](worksheets/B01.md) | Prioritize waves by key-level positive gaps | Dashboard 03 |
| [B02 — Key Evidence Ledger](worksheets/B02.md) | Explain a selected wave using matching keys | Dashboard 03 |
| [B04 — Gap Concentration](worksheets/B04.md) | Read ranked contribution against a fixed denominator | Standalone published sheet |
| [B05 — Wave Outlier Explorer](worksheets/B05.md) | Inspect volume/gap patterns beyond the Top 20 | Dashboard 03 |
| [C01 — Normalization Transformation Ledger](worksheets/C01.md) | Inspect original/current/literal tokens | Dashboard 02 |
| [C01b — Rule Footprint Heatmap](worksheets/C01b.md) | Locate rule concentration by source | Dashboard 02 |
| [C02 — Interpretation Sensitivity](worksheets/C02.md) | Compare gap and excess across interpretations | Dashboard 02 |
| [C03 — ABC Classification Comparison](worksheets/C03.md) | Compare published and derived classification bases | Standalone published sheet |

The published C01b tab is spelled **“C01b · Rule Foorprint Heatmap”**. “Footprint” is the explanatory spelling in these notes; the workbook was not renamed.

## How to read the claims

**O** = observed in the published viewer; **U** = author-reported build experience/demonstration; **R** = verified against repository artifacts; **G** = equivalent reconstruction guidance, not an inspected workbook definition; **Q** = pending QA. See the [register](EVIDENCE_REGISTER.md) for exact scope.

First-person learning passages are editable summaries drafted from the owner's supplied build lessons and the visible design. They are not a verbatim diary, a claim to have observed every authoring session, or a personal mastery assessment. Review and add your own wording when revisiting a sheet. Error sections distinguish reported lessons from diagnostic patterns to watch for.

Git versions these notes, scripts, CSVs and prior computational evidence. No `.twb` or `.twbx` exists in the repository at this documentation snapshot; the published workbook itself is **not** version-controlled here. No screenshots or workbook exports are attached or invented. No model, data, calculations, gates or source interpretations were changed by this documentation task.

Attribution: Rodrigo Furlan de Assis, *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*, Mendeley Data v1, DOI [10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), CC BY 4.0. Warehouse Lab uses derived, pseudonymized research extracts and declared analytical interpretations; preparation was AI-assisted. Source semantics and independent domain review remain pending.
