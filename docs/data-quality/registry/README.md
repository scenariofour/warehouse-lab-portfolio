# Real-source issue registry — M2

Python 3.10+ standard library; run from repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/data_quality/build_registry.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/data_quality/verify.py M2
```

No production normalizer, simulator, synthetic data or uncommitted discovery dependency is used. All 21 raw files are authenticated against `data/manifest.json`; nine original CSVs supply the analytical populations. Sources: Rodrigo Furlan de Assis, *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*, Mendeley Data v1, DOI [10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), CC BY 4.0.

| Artifact | Grain / evidence use |
|---|---|
| issues.json | 14 aggregate investigation questions; contract validated. Exact raw ordinal ranges, source columns, hash, affected versus contributing roles; unknown causes and pending review. |
| manifest.json | Source hashes, code hashes, record counts, totals, transformation/assumption labels and generated-output hashes. |
| reconciliation.csv | Every union wave/reference/existing inferred-size key; both quantities, matched quantity, signed gap, full customer/picking raw ordinal lists. All source ordinals appear once. Empty size preserved. |
| classification.csv | Each demanded reference, both ABC classifications, full customer ordinals and Product.csv ordinal. Derived 80/95 rule uses cumulative volume before each ranked reference. |
| policy_skus.csv | Each coordinate-retained policy/reference/numeric-size counter. Conditional encoded-cell counts, not verified warehouse stock. |
| policy_pairs.csv | Six unordered policy pairs; union SKU counts, differing counters and L1 cell difference. Pairs overlap; L1 is not unique stock or required moves. |
| excluded_cells.csv | Each allocation cell without a coordinate join; exact policy/raw ordinal/column selector and original token. |
| unknown_reference_cells.csv | Each allocation cell with a reference absent from Product.csv, including coordinate-excluded cells. Exact cell selector. |
| profile_checks.csv | Source/field/check counts and source-row denominators, including zero findings. Blank key checks are separate from unestablished format/business validity. |

Raw delimiters/BOM, whitespace joins and inferred half-token mapping follow the established rules; Decimal supplies stable numeric spelling. All raw zeros and repeated occurrences remain in primary quantities. Repeated tuples are compared before trimming. Header = record 1. Compressed ranges are exact inclusive logical ordinals, never estimates. For aggregate metrics, contributing rows define the calculation population; a positive key gap does not identify which individual requested units failed. For allocation exceptions, the cell ledger defines the flagged cells within contributing rows.

Stock/date and layout questions intentionally have null physical quantity/distance metrics. Numeric UNKNOWN must not be read as zero. No source question has been resolved or limitation accepted by a human. No before/after correction values exist. Potential operational consequences are hypotheses; no observed stockout, service failure, lost sales, monetary benefit or causal policy effect is established.

Overlaps: missing sizes, inferred sizes, repeats, positive reconciliation gaps and order reuse can share customer records. Unknown master cells can share missing geometry cells; policy stock comparisons reuse the same policies. Do not sum affected units/counts across issues or categories. No overall unique affected-unit percentage is supplied because these are incompatible and overlapping populations.

Validation independently recomputes the primary quantities in SQLite, classifies demand using Decimal thresholds, checks all original row lists and allocation-cell selectors, all six policy pairs, source hashes, contract/review invariants, baseline preservation and deterministic output replay. Historical discovery evidence was inspected and its verifier passed before adding tracked files. Its legacy replay inventories all tracked files, so adding this extension changes that inventory; use the self-contained M2 verifier for the extension. No old evidence or script has been altered to hide that context dependence.
