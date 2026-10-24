# Warehouse Lab — data card

Owner: data steward role unassigned; project owner accountable for interpretation. Author: AI assistant.  
Version: 0.1.0 · 2026-10-17. Status: DRAFT — PENDING HUMAN REVIEW.  
Review requirements: independent data reviewer checks transformations; source-domain reviewer confirms quantity, units, floor and order identity semantics. No such confirmation is recorded.

## Provenance and actual contents

Rodrigo Furlan de Assis, *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*, Mendeley Data v1, DOI [10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), CC BY 4.0. The publisher describes WMS-derived records with anonymization/randomization. Source files were acquired on 2026-10-15; the 2026-10-17 audit freshly verifies all 21 hashes against [the pinned manifest](../data/manifest.json). Byte agreement does not establish factual accuracy of anonymized fields. [E-02](evidence/2026-10-17/data-evaluation.json), [full schemas](data-audit.md).

| Source | Observed records | Use / transformation |
|---|---:|---|
| Storage_Location.csv | 2,292 | Unique IDs and original XYZ; uniform XY display calibration; all retained |
| Random_Storage.csv | 2,292 rows / 41,256 cells | Default location/reference/payload allocations |
| Class_Based_Storage.csv | 2,341 rows / 42,138 cells | 882 cells at 49 missing geometry IDs excluded |
| Dedicated_Storage.csv | 2,340 rows / 42,120 cells | 864 cells at 48 missing geometry IDs excluded |
| Hybrid_Storage.csv | 2,340 rows / 42,120 cells | 864 cells at 48 missing geometry IDs excluded |
| Product.csv | 208 | Reference, ABC classification, sector |
| Customer_Order.csv | 122,370 | Real quantities and source-row lineage; 39,858 wave/order groups |
| Picking_Wave.csv | 215,192 | Historical wave/reference/size/location audit; not robot events or extra demand |
| Support_Points_Navigation.csv | 44 | Retained source navigation points; full routing graph is derived |

Normalized order JSON retains number, wave, first group creation date, product reference, normalized size, quantity and source-record ordinal. Customer code, operator and collection sequence remain in the preserved raw CSV and are not simulated.

The notebook and four SVGs describe level/block conventions. DWG/PDF files are retained/hash-verified, not decoded by the simulation. Schemas, delimiters, timestamp coverage and exclusions are enumerated in [data-audit.md](data-audit.md); exact normalized-array reconciliation is in [E-02](evidence/2026-10-17/data-evaluation.json).

## Interpretation contract and unresolved meaning

| Issue | Observed evidence | Adopted sandbox rule / unresolved decision |
|---|---|---|
| Storage payload | Source README calls it quantity; Random has 7,524 fractional numeric tokens; half-size values also occur in picking records | Token interpreted as size; **one assumed carton per encoded cell**. Quantity truth and snapshot date require source confirmation; do not silently convert to literal numeric quantities |
| Customer sizes | E-02 compares each changed token to wave/reference joins: e.g. `105` has 0 literal joins and 12,442 normalized joins among 12,753 rows | Existing inferred `35…125` half-size mappings retained; evidence supports an inference, not provider approval; uncommon three-digit values remain unchanged |
| Coordinates and Z | Source README says meters; notebook/SVGs call Z1–4 floors | `X3D=0.1*sourceY−72`, `Z3D=0.1*sourceX−37.6`; floors displayed as rack tiers. Scale and topology are not surveyed facts |
| Identity | 32,634 distinct order numbers; 4,024 occur in multiple waves; no mixed customers/creation dates within a wave/order group | Engine unit is wave + order number (39,858 groups). Whether customer throughput should aggregate waves requires business/WMS review |
| Duplicates | 2,559 exact customer-row duplicates; 102,201 repeated picking rows | Customer lines preserved; picking records are not replayed as duplicate orders. No evidence justifies automatic deduplication |
| Missingness | 16 customer sizes missing; source policy locations absent from geometry; Class-Based has 109 references absent from Product.csv | Preserve/record source exceptions; unfulfillable tasks fail under the adopted stock model. No imputation or invented geometry |
| Time | Creation dates 2023-01-05–2023-10-19; source sequence is not chronological; no pick-completion/motion durations in relevant CSV schemas | Default first 120 source groups/922 units release at engineered 6s cadence. Inventory date alignment and actual service times are unknown |

Evidence: [source README](../data/raw/README.txt), [normalizer](../scripts/prepare_data.py), [E-02](evidence/2026-10-17/data-evaluation.json). The column called `row` is the logical source data-record ordinal plus its header; original raw files remain the authority. No source interpretation was changed in this review.

## Integrity controls and usage limits

Fresh checks reconcile every normalized geometry record, product, allocation cell and customer line against source under the existing rules; row lineage is complete and unique; all four normalized configurations contain 41,256 modeled cells. The total does **not** imply SKU-equivalent supply. Normalized SKU counts are Random 2,980; Class-Based 7,062; Dedicated 3,245; Hybrid 3,532. [E-02](evidence/2026-10-17/data-evaluation.json).

ZIP imports now validate recognized files and reject conflicting content before writes; existing raw files are preserved. Download candidates are hash-checked before insertion. Synthetic regression fixtures are confined to temporary directories. [Importer](../scripts/import_source_zip.py), [E-03](evidence/2026-10-17/before-import-regression.log), [E-07](evidence/2026-10-17/after-import-regression.log).

Permissible proposed use: inspect anonymized published records and reproduce the declared model. Prohibited inference without further evidence: measured factory stock, real travel distance/capacity, observed AMR performance, a representative annual workload, inventory-equivalent policy effects or quantified business benefit. Hashes, raw snapshots and model outputs are separate evidence classes. A source change or approved interpretation change reopens G1 and downstream reviews. [Gates](GATE_REVIEWS.md).
