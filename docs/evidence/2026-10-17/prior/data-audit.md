# Data audit

Source: Rodrigo Furlan de Assis. *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*, Mendeley Data v1, DOI [10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), CC BY 4.0. Downloaded 2026-10-15. All 21 published files verified against publisher SHA-256 hashes. Raw records remain in `data/raw`; manifest in `data/manifest.json`. No fabricated fallback records.

## Actual schemas

- **Storage_Location.csv**: 2,292 rows; columns: `originalLocation`, `position`, `x`, `y`, `z`.
- **Random_Storage.csv**: 2,292 rows; columns: `originalLocation`, `col_1`, `col_2`, `col_3`, `col_4`, `col_5`, `col_6`, `col_7`, `col_8`, `col_9`, `col_10`, `col_11`, `col_12`, `col_13`, `col_14`, `col_15`, `col_16`, `col_17`, `col_18`.
- **Class_Based_Storage.csv**: 2,341 rows; columns: `Location`, `ABCCOD`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`.
- **Dedicated_Storage.csv**: 2,340 rows; columns: `Location`, `XYZCOD`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`.
- **Hybrid_Storage.csv**: 2,340 rows; columns: `Location`, `XYZCOD`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`.
- **Product.csv**: 208 rows; columns: `Reference`, `ABCCOD`, `Sector`.
- **Customer_Order.csv**: 122,370 rows; columns: `codCustomer`, `orderNumber`, `orderToCollect`, `Reference`, `Size (US)`, `quantity (units)`, `creationDate`, `waveNumber`, `operator`.
- **Picking_Wave.csv**: 215,192 rows; columns: `waveNumber`, `reference`, `Size (US)`, `quantityToPick (units)`, `locations`, `operator`.
- **Support_Points_Navigation.csv**: 44 rows; columns: `points_specified`, `labels`.

CSV delimiters: Storage_Location and Random_Storage use commas; all other CSVs use semicolons. UTF-8 BOM and whitespace are stripped. A nonempty numbered storage cell is split once into product reference and its original numeric token. All original numeric tokens are retained.

## Critical interpretation limits

**Storage payload ambiguity.** README describes `reference;quantity`, but tokens include half values such as 8.5, 9.5 and 10.5, match the wave shoe-size domain, and dedicated rows repeat identical values in all 18 cells. There is no authoritative reconciliation in the notebook. This app explicitly assumes the numeric token is a size and one encoded cell is one available carton/unit; it does NOT claim these are verified stock quantities. Inventory counts, depletion and stockouts are conditional on this model. The first raw token is retained for inspection. Fractional tokens are never presented as measured quantities.

**Size normalization.** Customer sizes 35,45,55,65,75,85,95,105,115,125 are mapped to 3.5…12.5, consistent with Picking_Wave half sizes. Other integers (including 215…305) stay unchanged. Missing sizes remain missing and become unfulfillable demand. This is an inferred repair, not a source fact.

**Geometry and units.** README calls X,Y,Z meters. The notebook instead names Z=1…4 floors and draws 15×30 source-unit blocks on Z1/2 and 45×30 on Z3/4. We preserve all 2,292 source coordinates and relative XY distances, but use an explicit hypothetical horizontal calibration of 0.1 modeled meters/source unit. No claim of surveyed metric accuracy. Three.js X = source Y × 0.1 − 72; Three.js Z = source X × 0.1 − 37.6. This is a rigid rotation/reflection and uniform horizontal scaling. Vertical display Y = (source Z − 1) × 1.45 + 0.6. Z levels are displayed as four rack tiers with abstract shelf service, not real autonomous travel between floors. The original notebook and SVGs treat them as separate floors. Robot travel distances and 1m/s therefore use **modeled meters**.

Rack footprints follow notebook block dimensions (1.5×3 modeled m on levels1/2, 4.5×3 on levels3/4). Raster routing excludes the union of footprints on every tier, inflated by robot radius. 44 source navigation support points are retained; the published sparse points alone do not define a complete traversable graph, so routing uses a derived 1m occupancy grid. Outer access lanes, receiving, packing, conveyors and two outbound stations are synthetic and positioned outside rack footprints. Equipment footprints and a 0.48m AMR clearance are also excluded from the routing grid. DWG downloaded and hash-verified, not decoded; geometry reconstructed from CSV and notebook block rules.

## Validation results

```json
{
  "counts": {
    "Storage_Location": 2292,
    "Random_Storage": 2292,
    "Class_Based_Storage": 2341,
    "Dedicated_Storage": 2340,
    "Hybrid_Storage": 2340,
    "Product": 208,
    "Customer_Order": 122370,
    "Picking_Wave": 215192,
    "Support_Points_Navigation": 44
  },
  "sha256Verified": 21,
  "orderCount": 39858,
  "customerOrderNumberCount": 32634,
  "dateMin": "2023-01-05T07:42:00",
  "dateMax": "2023-10-19T07:18:00",
  "duplicateCustomerRows": 2559,
  "duplicatePickingRows": 102201,
  "missingOrderSizes": 16,
  "orderRowsMatchingWaveSKU": 116277,
  "waveLocationsMissingGeometry": [
    "C-014",
    "C-021",
    "C-022",
    "C-023",
    "C-024",
    "C-026",
    "C-061",
    "C-102",
    "E-25-20",
    "EX-01",
    "EX-04",
    "EX-11",
    "G-25-10",
    "I-25-20",
    "J-25-20",
    "K-25-20",
    "K-26-20",
    "RC-01",
    "RC-03",
    "RC-04",
    "RC-05",
    "ZN-COR"
  ],
  "waveReferencesMissingProduct": [],
  "orderRowsWithoutRandomSKU": 12551,
  "negativeOrderQuantities": 0,
  "duplicateGeometryIDs": 0,
  "modeledStock": 41256
}
```

## Storage configurations

### Random
```json
{
  "rows": 2292,
  "cells": 41256,
  "importedCells": 41256,
  "missingGeometryLocations": [],
  "cellsWithoutGeometry": 0,
  "unknownReferences": [],
  "duplicateLocations": {},
  "distinctSKUs": 2980
}
```
### Class_Based
```json
{
  "rows": 2341,
  "cells": 42138,
  "importedCells": 41256,
  "missingGeometryLocations": [
    "E-25-10",
    "E-25-20",
    "E-26-10",
    "E-26-20",
    "F-25-10",
    "F-25-20",
    "G-25-10",
    "G-25-20",
    "H-25-10",
    "H-25-20",
    "I-25-10",
    "I-25-20",
    "J-25-10",
    "J-25-20",
    "K-25-10",
    "K-25-20",
    "K-26-10",
    "K-26-20",
    "L-25-10",
    "L-25-20",
    "M-25-10",
    "M-25-20",
    "N-25-10",
    "N-25-20",
    "O-25-10",
    "O-25-20",
    "P-25-10",
    "P-25-20",
    "Q-25-10",
    "Q-25-20",
    "Q-26-10",
    "Q-26-20",
    "R-01-01",
    "R-01-02",
    "R-01-03",
    "R-01-04",
    "R-01-05",
    "R-01-06",
    "R-01-07",
    "R-01-08",
    "R-01-09",
    "R-01-10",
    "R-01-11",
    "R-01-12",
    "R-01-13",
    "R-01-14",
    "R-01-15",
    "R-25-10",
    "R-25-20"
  ],
  "cellsWithoutGeometry": 882,
  "unknownReferences": [
    "10090TO",
    "102SP",
    "12123XPJ",
    "12133XPJ",
    "12261XP",
    "12314XP",
    "14010TO",
    "2002XP",
    "2005XP",
    "2010XP",
    "2017XP",
    "2019XPC22",
    "2020XPC",
    "2027XP",
    "2035XP",
    "2039XP",
    "2041XPC",
    "2047XPC",
    "2081XP",
    "2133XP",
    "2135XP",
    "2149XPC",
    "2152XPC",
    "2161XP",
    "2162XP",
    "2209XP",
    "2215XP",
    "2225XP",
    "2251XPJ",
    "2261XPC",
    "2265XP",
    "2274GT",
    "2286XP",
    "2312XPJ",
    "2700GT",
    "300FW",
    "3120QD",
    "4019XPC",
    "4161XP",
    "452687JV",
    "5003DD",
    "541SP",
    "5650GT",
    "5651GT",
    "5691GT",
    "5701GTR",
    "5706GT",
    "5750GT",
    "5752AG",
    "5790AG",
    "5791GT",
    "59220JV",
    "602SP2AG",
    "6300MG",
    "6300VT",
    "6300VTAG",
    "7100B9",
    "750FW",
    "7580AF",
    "7601AF",
    "7607AF",
    "7620AF",
    "7781JV",
    "7781JV000001",
    "7783TR",
    "7816JV",
    "7820TR",
    "7902TR",
    "7960VI",
    "7968TR",
    "7972TR",
    "801PG",
    "8199JV",
    "8401FLX",
    "8422FLX",
    "8490FLX",
    "8551FLX",
    "8552FLX",
    "8622FLX",
    "8707CH",
    "8732TR",
    "8733B4",
    "8736TR",
    "8746CH",
    "9800DLX",
    "9820DLX",
    "9900DLX",
    "9901DLX",
    "9920DLX",
    "9922DLX",
    "99433X",
    "DCB01",
    "LOTB21",
    "VC1708C",
    "VC1711",
    "VF001",
    "VF002",
    "VF003",
    "VF004",
    "VF005",
    "VF006",
    "VF007",
    "VF008",
    "VF009",
    "VS5792",
    "VS5794",
    "VT10010",
    "VT10013",
    "VT30012"
  ],
  "duplicateLocations": {},
  "distinctSKUs": 7163
}
```
### Dedicated
```json
{
  "rows": 2340,
  "cells": 42120,
  "importedCells": 41256,
  "missingGeometryLocations": [
    "E-25-10",
    "E-25-20",
    "E-26-10",
    "E-26-20",
    "F-25-10",
    "F-25-20",
    "G-25-10",
    "G-25-20",
    "H-25-10",
    "H-25-20",
    "I-25-10",
    "I-25-20",
    "J-25-10",
    "J-25-20",
    "K-25-10",
    "K-25-20",
    "K-26-10",
    "K-26-20",
    "L-25-10",
    "L-25-20",
    "M-25-10",
    "M-25-20",
    "N-25-10",
    "N-25-20",
    "O-25-10",
    "O-25-20",
    "P-25-10",
    "P-25-20",
    "Q-25-10",
    "Q-25-20",
    "Q-26-10",
    "R-01-01",
    "R-01-02",
    "R-01-03",
    "R-01-04",
    "R-01-05",
    "R-01-06",
    "R-01-07",
    "R-01-08",
    "R-01-09",
    "R-01-10",
    "R-01-11",
    "R-01-12",
    "R-01-13",
    "R-01-14",
    "R-01-15",
    "R-25-10",
    "R-25-20"
  ],
  "cellsWithoutGeometry": 864,
  "unknownReferences": [],
  "duplicateLocations": {},
  "distinctSKUs": 3262
}
```
### Hybrid
```json
{
  "rows": 2340,
  "cells": 42120,
  "importedCells": 41256,
  "missingGeometryLocations": [
    "E-25-10",
    "E-25-20",
    "E-26-10",
    "E-26-20",
    "F-25-10",
    "F-25-20",
    "G-25-10",
    "G-25-20",
    "H-25-10",
    "H-25-20",
    "I-25-10",
    "I-25-20",
    "J-25-10",
    "J-25-20",
    "K-25-10",
    "K-25-20",
    "K-26-10",
    "K-26-20",
    "L-25-10",
    "L-25-20",
    "M-25-10",
    "M-25-20",
    "N-25-10",
    "N-25-20",
    "O-25-10",
    "O-25-20",
    "P-25-10",
    "P-25-20",
    "Q-25-10",
    "Q-25-20",
    "Q-26-10",
    "R-01-01",
    "R-01-02",
    "R-01-03",
    "R-01-04",
    "R-01-05",
    "R-01-06",
    "R-01-07",
    "R-01-08",
    "R-01-09",
    "R-01-10",
    "R-01-11",
    "R-01-12",
    "R-01-13",
    "R-01-14",
    "R-01-15",
    "R-25-10",
    "R-25-20"
  ],
  "cellsWithoutGeometry": 864,
  "unknownReferences": [],
  "duplicateLocations": {},
  "distinctSKUs": 3532
}
```

Additional configurations have different SKU distributions and missing geometry locations; those cells are excluded and reported above. They are experimental scenarios, not inventory-equivalent controlled storage-policy experiments. The app rebuilds SKU indices for each policy and never reuses historical pick coordinates. Demand window and all engineering parameters remain the same when switching.

## Order and time semantics

Customer creation dates span 2023-01-05T07:42:00 through 2023-10-19T07:18:00; 39,858 wave/order groups (32,634 distinct order numbers). Order keys combine wave and order number. 116,277 of 122,370 customer rows join a wave/reference/normalized-size tuple. 12,551 rows lack that SKU in the baseline stock model.

Customer creationDate is the only timestamp in these CSVs. Picking_Wave has no pick-start, pick-end, robot motion, or completion timestamps. It cannot support measured service durations or a historical robot replay. Original order sequence and source row numbers are preserved. Default session is the first 120 complete source wave/order groups; larger windows/all demand can be loaded. Orders release every six simulated seconds (configurable), rather than compressing historical dates invisibly. Repeated customer rows are preserved as demand, because they may represent legitimate repeated lines. Identical picking rows are preserved in the raw files but not replayed as extra orders: the file has repeated one-unit picks. Historical location joins are audited only; every new task is routed using the active configuration.

## Simulation assumptions and metrics

10 AMRs; 1 modeled m/s; one assumed carton/unit per trip; pick12s; unload10s; two exclusive outbound stations and ten approach staging cells; step0.2s; deterministic seed42. Source stock is reserved once at dispatch and decremented at pick; orders complete only when all units unload. Missing SKU/size, depleted stock, or inaccessible locations generate explicit failed units, so partially failed orders never appear completed. Queue is FIFO with deterministic nearest eligible inventory choice. Robots reserve both edge endpoints while moving; opposing edges and occupied destinations are blocked. Replanning avoids reserved cells. In a contested cell, the higher-ID robot pulls aside and holds for four seconds to prevent symmetric detour livelock; waiting and traffic are accumulated from actual fixed-step state. Shelf picking is an abstract service, not an implemented industrial manipulator.

Conveyor parcels spawn only on actual unload events and move for16 simulated seconds; packing and belt travel are synthetic. Receiving area is a static context model; no invented inbound replenishment. No truck operation or robotic arm is implemented.

Throughput = completed whole orders / elapsed hours. Completion time is release-to-final-unload for successful orders. Utilization = moving + picking + unloading robot-seconds / available robot-seconds; congestion waiting is separate. Travel sums actual edge progress. Occupancy is nonempty modeled storage locations / geometry locations; stock is the remaining assumed carton count. Warmup, modeled dimensions and ambiguous stock mean these are comparative sandbox results, not validated factory predictions. Every event includes simulation time; exports include config, source and scenario.
