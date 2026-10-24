# Tableau showcase

Warehouse Lab's published analytics move from data-quality triage to interpretation sensitivity and reconciliation evidence. Links and visible titles were checked in the signed-out Tableau Public viewer on October 23, 2026. Existing workbook notes remain the detailed source of methodology and learning history.

## Data Quality & Decision Intelligence

[Open Dashboard 01 · Data Quality Overview](https://public.tableau.com/views/WarehouseLabDataQualityDecisionIntelligence/Dashboard01-DataQualityOverview?:showVizHome=n).

This overview introduces the real-source issue registry and the distinction between an observed discrepancy, a data-definition question and a decision that needs review. It gives reviewers an entry point into source counts, issue metrics and decision impacts, with the methodological limits kept beside the findings. Use it to understand where investigation is needed before interpreting discrepancies as operational failures.

[Foundation](../data-quality/README.md) · [Dashboard specification](../data-quality/TABLEAU_SPEC.md) · [Public summary CSVs](../data-quality/tableau/public/) · [Extraction manifest](../data-quality/tableau/manifest.json).

## Operations Decision Studio

### Dashboard 02 · Normalization & Interpretation Lab

[Open Dashboard 02](https://public.tableau.com/views/WarehouseLabOperationsDecisionStudio/Dashboard02NormalizationInterpretationLab2?:showVizHome=n).

The normalization ledger, source/rule heatmap and interpretation sensitivity bars show how the same underlying records can produce different reconciliation results. Current inferred, literal-size and exact-customer-dedup interpretations are explicit alternatives. The dashboard supports reviewing definitions before drawing operational conclusions; changing an interpretation does not change physical warehouse activity. Its exact URL was obtained from Tableau's Share dialog after selecting the published dashboard tab.

[Case study](../data-quality/advanced/tableau-workbook/DASHBOARD_02_CASE_STUDY.md) · [C01 ledger](../data-quality/advanced/tableau-workbook/worksheets/C01.md) · [C01b heatmap](../data-quality/advanced/tableau-workbook/worksheets/C01b.md) · [C02 sensitivity](../data-quality/advanced/tableau-workbook/worksheets/C02.md).

### Dashboard 03 · Reconciliation Investigation

[Open Dashboard 03](https://public.tableau.com/views/WarehouseLabOperationsDecisionStudio/Dashboard3?:showVizHome=n).

A Top 20 wave view and broader wave scatter help prioritize investigation, while the key evidence ledger explains gaps at wave × product reference × size grain. Key-level positive gaps are calculated before aggregation to avoid cancellation between different products or sizes. The interpretation parameter exposes the calculation's dependence on source assumptions. Existing notes distinguish author-demonstrated drill-down behavior from interaction branches that still need QA.

[Case study](../data-quality/advanced/tableau-workbook/DASHBOARD_03_CASE_STUDY.md) · [B01 wave view](../data-quality/advanced/tableau-workbook/worksheets/B01.md) · [B02 evidence ledger](../data-quality/advanced/tableau-workbook/worksheets/B02.md) · [B05 outlier explorer](../data-quality/advanced/tableau-workbook/worksheets/B05.md).

### B04 · Gap Concentration

[Open the standalone worksheet](https://public.tableau.com/views/WarehouseLabOperationsDecisionStudio/B04GapConcentration?:showVizHome=n).

The ranked view separates the visible Top 20 waves from the full gap denominator. Its 1,720 displayed gap units are part of 13,003 current positive-gap units, rather than the entire population. This makes concentration useful for investigation without presenting a selected subset as a warehouse-wide rate. [Worksheet explanation and denominator lessons](../data-quality/advanced/tableau-workbook/worksheets/B04.md).

## Reproduce and learn

[14 analytical CSVs](../data-quality/advanced/public/) · [Data dictionary](../data-quality/advanced/DATA_DICTIONARY.md) · [Manifest](../data-quality/advanced/manifest.json) · [Audit and model](../data-quality/advanced/AUDIT_AND_MODEL.md) · [Calculation reference](../data-quality/advanced/tableau-workbook/CALCULATION_REFERENCE.md) · [Learning index](../data-quality/advanced/tableau-workbook/LEARNING_INDEX.md) · [Evidence register](../data-quality/advanced/tableau-workbook/EVIDENCE_REGISTER.md) · [Remaining QA](../data-quality/advanced/tableau-workbook/QA_AND_MAINTENANCE.md).

Use only the designated public CSVs when rebuilding a published workbook. `tableau/internal/` contains detailed research lineage and raw identifiers; its name describes intended analytical use, not a claim that it contains credentials. Those files are retained for reproducibility but are not embedded in this showcase or included in the deployed simulator.

## Provenance and limits

Rodrigo Furlan de Assis, *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*, Mendeley Data v1 (2024), [DOI 10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Warehouse Lab uses derived, pseudonymized analytical extracts, inferred normalization and declared alternatives. Preparation and analysis were AI-assisted. [Transformation and license notice](../../THIRD_PARTY_NOTICES.md).

Published labels and visible charts were inspected; hidden formulas, uploaded extract byte identity, all parameter branches and every filter action were not independently verified. Source semantics and domain review remain pending. Reconciliation gaps do not establish stockouts, unfulfilled orders, measured losses or causal improvements. Historical notes retain their original evidence dates and qualifications.

## Workbook archive status

**No Tableau workbook was archived in Git.** The public viewer offered a workbook download, but the attempted download did not produce an inspectable local artifact. No package or extract has therefore been cleared for redistribution here. The interactive workbooks remain hosted on Tableau Public; repository CSVs and notes are versioned separately. The generated image URL from Tableau’s embed code returned HTTP 404, so it is not embedded. The repository’s application screenshot is a verified local capture. No Tableau Public workbook was edited.
