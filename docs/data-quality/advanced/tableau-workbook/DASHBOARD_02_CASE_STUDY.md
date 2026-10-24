# Dashboard 02 — Normalization & Interpretation Lab

[Published workbook](https://public.tableau.com/views/WarehouseLabOperationsDecisionStudio/Dashboard3?:showVizHome=n): choose **Dashboard 02 · Normalization & Interpretation Lab** in its tabs. The supplied URL opens Dashboard 03; a separate Dashboard 02 permalink was not independently established. [Evidence labels](EVIDENCE_REGISTER.md): O2/O6/O7, U1/U3, R1–R4.

## Audience, problem and intended value

For warehouse analysts, data stewards and BI reviewers, the problem is deciding whether an apparent demand–picking mismatch reflects operations or interpretation. The dashboard asks **“When Data Definitions Change the Answer”** and makes token-level assumptions visible before users act on aggregate gaps. Its intended value is a traceable definition review and a better evidence request, not a measured productivity or savings result.

The decision is whether size-code interpretation and repeated-record handling are sufficiently supported to use a reconciliation result in operational investigation. They are not authorized source corrections. Source-owner size definitions and event/line semantics remain needed before changing production inputs.

## Data, grain and analytical workflow

Source: Rodrigo Furlan de Assis, Mendeley Data v1, DOI [10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), CC BY 4.0. AI-assisted Warehouse Lab derivatives preserve raw sources. [Manifest](../manifest.json), [dictionary](../DATA_DICTIONARY.md), [builder](../../../../scripts/data_quality/build_advanced.py).

| Delivered worksheet | Data grain and role |
|---|---|
| [C01b — Rule Footprint Heatmap](worksheets/C01b.md) | normalization_tokens: one source/field/exact original token, aggregated to source/rule; locate where rules apply |
| [C01 — Normalization Transformation Ledger](worksheets/C01.md) | Same token extract; inspect original, current and literal representations plus record/unit populations |
| [C02 — Interpretation Sensitivity](worksheets/C02.md) | reconciliation_summary: one full-extract interpretation; compare gap and excess bars after understanding the rule |

These are separate sources/grains, not a physical join. C03 exists as a [standalone ABC worksheet](worksheets/C03.md); it was not observed on Dashboard 02. The planned C04/C05 panels are not claimed as delivered.

Current customer tokens 35…125 in the declared half-token set map to 3.5…12.5; literal interpretation retains the numeric token. Customer dedup keeps the first complete original tuple in a hypothetical branch. Reconciliation computes `min(D,P)`, `max(D-P,0)` and `max(P-D,0)` **per key before summing**. Full recipes: [calculation reference](CALCULATION_REFERENCE.md#selected-interpretation-calculations).

## Confirmed controls and behavior

Observed: published tabs, hover-capable worksheet descriptions and the three panels; C01 displays the Customer_Order/HALF_SIZE subset, C01b colors/labels Token Records, and C02 displays all three interpretations with gap/excess bars. Measure Names/Values structure is visible in C01/C02. The explanatory panel states that definitions can change results without changing warehouse activity.

Not confirmed: whether C01's subset is a permanent filter or a saved action state, any C01b → C01 filter action, every tooltip value, or full parameter synchronization. No pRule parameter or source/rule filter cards were observed on Dashboard 02 itself; C01's standalone cards are recorded separately. C02's three rows compare alternatives; a row is not itself a parameter action.

## Findings, assumptions and remaining QA

Repository-verified: current gap/excess = **13003 / 0**; literal = **78681 / 65678**; customer dedup = **12985 / 12717**. Half-token mapping covers **38846 customer records**. These are extract calculations, not an independent numerical audit of every rendered bar.

Assumptions: current inferred size meaning; literal and dedup as sensitivities; unconfirmed duplicate semantics. Hypotheses such as extraction differences, legitimate repeated demand or size-code mismatch remain competing explanations. Better arithmetic overlap does not validate a source correction. No physical activity, failed service, cost or policy effect is measured.

Remaining QA: [Q1–Q5](EVIDENCE_REGISTER.md#pending-and-historical-references), especially token source/rule filter provenance, missing-value display, per-branch values and readability/thumbnail rendering. No new QA result is invented.

## What I learned

*Editable first-person learning summary:* I learned to show the rule before asking someone to trust a result. Measure Names/Values let me compare several quantities without confusing their meanings; the heatmap and ledger answer different questions. An analytical alternative can expose sensitivity while remaining unapproved. For future BI work, I should ask “Which definition changed, at what grain, and who can confirm it?” before describing a gap as an operational problem.
