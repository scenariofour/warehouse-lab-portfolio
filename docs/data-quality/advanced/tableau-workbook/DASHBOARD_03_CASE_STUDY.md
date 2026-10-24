# Dashboard 03 — Reconciliation Investigation

[Open the delivered dashboard](https://public.tableau.com/views/WarehouseLabOperationsDecisionStudio/Dashboard3?:showVizHome=n). [Evidence labels](EVIDENCE_REGISTER.md): O3/O8, U1–U3, R1–R4.

## Audience, problem and intended value

Warehouse analysts and industrial-engineering reviewers need to move from a large reconciliation gap to a specific, inspectable evidence question. A top-wave chart alone hides the broader population; a scatter alone cannot explain the contributing product/size keys. The dashboard combines prioritization, context and detail to support the decision **which source evidence to investigate next**.

Intended value: let a reviewer select a wave and inspect its matching-key evidence without treating a discrepancy as a stockout or fulfillment failure. No investigation-time reduction or business-performance gain was measured.

## Provenance, grain and worksheet roles

Public research source: Rodrigo Furlan de Assis, *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*, Mendeley Data v1, DOI [10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), CC BY 4.0. The visible footer identifies pseudonymized derived extracts, inferred size normalization, alternative scenarios, AI assistance and pending domain validation. See [dictionary](../DATA_DICTIONARY.md), [manifest](../manifest.json), [builder](../../../../scripts/data_quality/build_advanced.py).

| Delivered worksheet | Analytical role and display grain |
|---|---|
| [B01 — Reconciliation by Wave](worksheets/B01.md) | Top 20 bars prioritize waves by SUM of key-level positive gaps; one wave per bar |
| [B05 — Wave Outlier Explorer](worksheets/B05.md) | Broader wave population on continuous picking/gap axes; Wave Id on Detail and Wave Gap Share on Color |
| [B02 — Key Evidence Ledger](worksheets/B02.md) | Source detail at wave × reference × size, with presence and separate customer/picking/matched/gap/excess columns |

All use the reconciliation extract's union key across interpretations: `reconciliation_id`, with string wave/reference identifiers and a string size key. Different display grains do not require joining facts. [B04](worksheets/B04.md) is a standalone concentration view; it is not a fourth panel on Dashboard 03. The earlier B03 order-group plan is not claimed as implemented.

The selected interpretation chooses customer quantity and record count; published picking quantities stay fixed. For each key, `gap=max(D-P,0)` and `excess=max(P-D,0)`. Only then aggregate to wave. A ratio of wave sums is not an average of key percentages. [Calculation reference](CALCULATION_REFERENCE.md#selected-interpretation-calculations).

## Implemented interactions and their evidence

- **U2: manually demonstrated** B01 → B02 Wave drill-down and B05 → B02 Wave drill-down. These are author-reported demonstrations; no retrospective screenshot/test artifact is fabricated.
- **O3: observed** `pInterpretation`, with “Current inferred” selected; Top 20 bars, scatter, detail table and methodology/attribution panels.
- **O8: observed** B01 tooltip field list includes Selected Customer Units; B05 lists Selected Customer Records. Those units must not be conflated. B02 exposes Reconciliation Id as a tooltip field for local source lookup.

Reconstruction uses the wave field as the action mapping, with B01/B05 as sources and B02 as target. Exact stored action names, selected-field settings, clearing behavior and all branch-dependent recalculations were not inspected. A filter action and a parameter have different jobs; selecting a wave is not changing the interpretation. See [action lessons](CALCULATION_REFERENCE.md#filter-action-direction).

## Findings versus assumptions and hypotheses

Repository baseline: 228195 requested, 215192 picking, 13003 positive-gap units, zero excess. These are validated extract quantities, not a complete rendered-workbook audit. The Top 20/current-gap subset totals 1720 units; the scatter's intended broader scope is stated in the published methodology panel. Its exact mark population and overplotting remain QA items.

Current size normalization is inferred, source dates/status alignment are unresolved, and source records may reflect differing extraction scopes. Cancellation/backlog, legitimate repeated lines and encoding differences are hypotheses. No pick order number exists to establish fulfillment for an individual order. A wave outlier prioritizes investigation; it does not identify the cause.

## Limitations, references and learning

Full branch QA, clearing/combined actions, multi-select, tooltip numerators, mark population and thumbnail/layout rendering remain [pending](QA_AND_MAINTENANCE.md). Independent source semantics and human review are not approved by publication. [Existing computational evidence](../evidence/validation.json) and [local source lookup](../../../../scripts/data_quality/lookup_advanced.py) support investigation without altering raw records.

*Editable first-person learning summary:* I learned that the unit of matching and the unit of display can differ. A wave chart must inherit key-level calculations rather than hide opposing differences in a net total. I also learned to check the direction of a dashboard action: the selected chart supplies a wave value, and the ledger receives it. In future BI tasks I should verify source, target, key type, denominator and clearing behavior separately instead of calling an interaction “working” after one successful selection.
