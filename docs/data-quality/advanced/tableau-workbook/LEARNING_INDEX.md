# Learning index

Search this file by Tableau term, analytical question or worksheet ID. Use [calculation recipes](CALCULATION_REFERENCE.md) to reconstruct and [evidence labels](EVIDENCE_REGISTER.md) to distinguish delivery from guidance. Each linked worksheet includes three answered self-checks.

## Structure the question and the data

| Concept / search terms | Reasoning to carry to the next BI task | Where I used it |
|---|---|---|
| Grain; key-level versus wave-level aggregation | Define the matching unit before deciding display aggregation; sum key discrepancies to wave | [B01](worksheets/B01.md), [B02](worksheets/B02.md), [B05](worksheets/B05.md) |
| String identifiers; size tokens; missingness | Codes describe identity, not magnitude; preserve MISSING and raw spelling | [B02](worksheets/B02.md), [C01](worksheets/C01.md) |
| Dimensions versus measures | Decide what groups observations and what is measured; numeric inference is not analytical meaning | [B01](worksheets/B01.md), [B04](worksheets/B04.md), [C03](worksheets/C03.md) |
| Discrete versus continuous; blue/green pills | Headers separate categories; axes position quantities; this differs from role/type | [B04](worksheets/B04.md), [B05](worksheets/B05.md), [C01b](worksheets/C01b.md) |
| SUM(Rank); ordinal; sort | Rank supplies sequence; adding positions does not measure a business quantity | [B04](worksheets/B04.md) |
| COUNTD; distinct entities; bad joins | State the entity counted; distinct counts do not repair duplicated SUM measures | [C03](worksheets/C03.md) |
| Source records versus aggregate rows versus units | SUM the contributing population field; COUNT(token rows) answers another question | [C01](worksheets/C01.md), [C01b](worksheets/C01b.md), [B05](worksheets/B05.md) |

## Choose an encoding and explain it

| Concept / search terms | Reasoning | Where I used it |
|---|---|---|
| Sorted bars; Top 20; selection bias | Prioritize magnitude while labeling the subset; keep broader context separately | [B01](worksheets/B01.md), [B04](worksheets/B04.md), [B05](worksheets/B05.md) |
| Scatter; Marks Detail; one point per entity | Put the entity on Detail; axes alone produce an aggregate point | [B05](worksheets/B05.md) |
| Heatmap; count versus volume | Define cell grain and color/label measure before interpreting darkness | [C01b](worksheets/C01b.md), [C03](worksheets/C03.md) |
| Measure Names / Measure Values; multiple measures | Headers and values are separate; remove irrelevant measures and verify each aggregation | [B02](worksheets/B02.md), [C01](worksheets/C01.md), [C02](worksheets/C02.md) |
| Tooltips; full identifiers; labels and units | A hover value needs a unit, scope and route back to evidence | [B01](worksheets/B01.md), [B02](worksheets/B02.md), [B05](worksheets/B05.md), [C03](worksheets/C03.md) |

## Design interactions and qualified conclusions

| Concept / search terms | Reasoning | Where I used it |
|---|---|---|
| Selected interpretation; parameter; CASE | A parameter chooses logic only in referencing calculations; it is not automatically a filter | [B01](worksheets/B01.md), [B02](worksheets/B02.md), [B05](worksheets/B05.md), [C02](worksheets/C02.md) |
| Filter Actions; source versus target; Wave drill-down | Selected source sends a wave value; ledger is the target; verify mapping/types and scope | [B01](worksheets/B01.md), [B02](worksheets/B02.md), [B05](worksheets/B05.md) |
| Clearing selection; combined filters; reset | One successful selection does not establish clearing, sequential or multi-select behavior | [QA checklist](QA_AND_MAINTENANCE.md#remaining-workbook-qa) |
| Fixed denominator; cumulative share; percent of total | Filtering a ranked subset does not redefine the question's reference population | [B04](worksheets/B04.md) |
| Ratio of sums versus average of ratios | Weight by the quantity denominator; small keys should not implicitly equal large keys | [B05](worksheets/B05.md), [shared formulas](CALCULATION_REFERENCE.md#selected-interpretation-calculations) |
| Presence versus quantity; zero records | A present zero-quantity key differs from an absent key | [B02](worksheets/B02.md) |
| Sensitivity versus correction; source truth | Compare interpretations without inventing source approval or physical operational change | [C01](worksheets/C01.md), [C02](worksheets/C02.md), [Dashboard 02](DASHBOARD_02_CASE_STUDY.md) |
| Published versus derived ABC; classification basis | Disagreement can reflect different objectives or periods; preserve both labels | [C03](worksheets/C03.md) |
| Evidence readiness; anomaly versus operational failure | An anomaly justifies investigation, not a causal or financial claim | [Dashboard 03](DASHBOARD_03_CASE_STUDY.md), [evidence register](EVIDENCE_REGISTER.md) |
| Documentation versus workbook version control | Notes/CSVs in Git do not imply a saved Tableau workbook exists there | [Notebook README](README.md), [maintenance](QA_AND_MAINTENANCE.md#maintain-the-next-dashboard) |

To test whether I understand a view, I should be able to state: **one mark means ___; its numerator is ___; its denominator is ___; selecting it changes ___; the decision it cannot establish is ___.** If any blank is unclear, inspect the source grain and controls before changing the chart.
