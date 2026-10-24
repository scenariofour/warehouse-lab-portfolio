# Simulator guide

A working Three.js warehouse sandbox built from **Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company**, Mendeley Data v1, Rodrigo Furlan de Assis, DOI [10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), **CC BY 4.0**.

The application includes all 2,292 storage coordinates, 208 product references, four published allocation files, 39,858 normalized wave/order groups from 122,370 customer rows, and a deterministic 10-AMR picking simulation. The default demand window is the first 120 complete source orders. All 21 publisher files were downloaded and SHA-256 verified; no fabricated fallback dataset is used.

## Internal governance and evidence (2026-10-17)

The MVP remains frozen. The [internal review](FINAL_REVIEW.md), [gate register](GATE_REVIEWS.md), and [evaluation contract](EVALUATION_PLAN.md) separate software verification from model/experiment/business validity. All human gate reviews are **PENDING**; no operational validation or policy ranking is approved. The technical evidence does not establish real-world savings or physical accuracy.

Internal QA commands (Python3.10+ standard library for data checks):

```bash
npm run audit:data
npm run test:data
npm test
npm run validate:scenarios
npm run evaluate:governance
npm run build
npm run test:browser
npm run check:governance
```

See the [evidence index](EVIDENCE_INDEX.md) for input hashes, execution logs, limits and review procedure. Existing data interpretation rules and default scenario outcomes were preserved; supported fixes protect source ZIP imports and reject invalid routing endpoints. Stage-gate review and unresolved business/methodological decisions require an identified human.

## Run locally

Prerequisite: Node.js **20.19+ or 22.12+** and npm. A WebGL-capable browser is required. From this project directory:

```bash
npm install
npm run dev
```

Open the localhost address Vite prints (normally **http://localhost:5173**). The normalized dataset and local fonts are already included. **Python, network access, a paid API, and a database are not needed to run the app.** Dependency installation initially requires npm access. All runtime assets are served locally.

```bash
npm run build
npm run preview
```

The production site is generated in `dist/`. Serve it through HTTP, not by double-clicking the HTML file.

## Try it

1. Start simulation. Choose **20×** for a faster overview; an actual carton trip can take several modeled minutes. Lower speeds are useful when following a robot.
2. Click an AMR in the scene or fleet list. Select **Follow robot** to see its route, loading service, carried carton, and delivery. Its details include source CSV row and destination.
3. Click a shelf/carton to inspect location stock, products, sizes, original payload tokens, and Product.csv classifications. The inventory tab also accepts exact IDs such as `A-14-11`.
4. Drag to orbit, scroll to zoom, right-drag to pan. Camera buttons offer isometric, top-down, and outbound views. Route, traffic, and label overlays can be toggled.
5. Pause/resume with the playback button or Space. Reset reconstructs original inventory and clears all event-derived metrics.
6. Open **Experiments** for Class-Based, Dedicated or Hybrid allocations, a 600-order/full demand window, and a session comparison table. Every switch resets the run and rebuilds SKU/location indices.
7. Open parameters from the rail gear to change speed, service times, release cadence, or seed. Values are applied only after resetting the run.
8. Ask the local operations assistant about busiest robots, congestion, long-running orders, or efficiency. Export a run for JSON metrics, configuration, robot activity and events.

## What is real, and what is modeled?

Read **[docs/data-audit.md](data-audit.md)** before interpreting results as operational evidence. The same audit is available in the application.

- **Real:** original location IDs and XY relationships; product references, classes and sectors; allocation cells; customer order IDs, quantities, creation timestamps and waves; picking records and navigation support points. Source row lineage is retained.
- **Ambiguous inventory:** README says allocation cells encode `product;quantity`, but half values and wave size domains suggest `product;shoe-size`. This implementation explicitly assumes **one carton/unit per encoded cell**, and interprets the numeric token as a size. Original tokens are preserved; carton totals and depletion are **modeled, not verified real quantities**. Missing stock fails explicitly.
- **Modeled geometry:** README calls coordinates meters; the notebook describes Z1–4 as floors. Horizontal coordinates are uniformly calibrated at **0.1 modeled m/source unit**. These floors are rendered as four rack tiers with abstract shelf service. Three.js X = source Y × 0.1 − 72, Z = source X × 0.1 − 37.6; display height follows source level. This preserves horizontal geometry but is not a surveyed building reconstruction.
- **Modeled operation:** 10 robots, 1 m/s, capacity 1 carton, pick 12s, unload 10s, two exclusive stations, 0.2s fixed step, orders released every 6s, seed 42. Source creation timestamps are displayed/audited but not falsely treated as pick-completion events. Simulation time starts at zero.
- **Synthetic support equipment:** receiving pallets, charging bays, packing stations, conveyors, dock doors and a parked forklift. Conveyor cartons appear only after simulated deliveries. No synthetic inbound replenishment changes inventory.
- **Experimental policies:** additional files are used as published; 49 Class-Based and 48 Dedicated/Hybrid locations lack geometry and are excluded. Class-Based has references absent from Product.csv. The stock distributions differ, so policy comparisons are not controlled, inventory-equivalent optimization experiments.

Default source orders contain demand unavailable in the baseline size/stock interpretation. Failed orders are an honest outcome, not a simulated success. Partially failed orders never count toward successful throughput.

## Data acquisition / local ZIP import

All raw and normalized files ship with this project. To regenerate derived inputs with Python **3.10+**, no third-party Python packages are needed:

```bash
npm run data
```

To download missing files using the pinned publisher manifest (requires `curl`):

```bash
npm run data -- --download
```

If programmatic access is blocked, open the [official version-1 dataset page](https://data.mendeley.com/datasets/pf2w725pw3/1), choose **Download All**, then supply the actual downloaded ZIP:

```bash
npm run data -- --zip "/absolute/path/to/your-downloaded-file.zip"
```

The importer validates recognized ZIP members against `data/manifest.json` before importing missing files into `data/raw/`, preserves existing source bytes, reads actual schemas, and regenerates `public/data/*.json`, `docs/data-audit.md`, and the app's audit copy. Missing required files stop conversion with an actionable message; hash mismatches stop it rather than accepting changed data. Run the dev server again or reload after import.

Acquired source files include `Storage_Location.csv`, `Random_Storage.csv`, `Customer_Order.csv`, `Product.csv`, `Picking_Wave.csv`, `Support_Points_Navigation.csv`, the other three policy CSVs, all four SVGs and PDFs, `Full layout.dwg`, `README.txt`, the notebook, and the empty published `Link Colab.txt`. DWG was downloaded/verified but not decoded. CSVs and the notebook's block rules drive geometry. SVG drawings and the notebook were inspected for level and block conventions; PDFs were downloaded and hash-verified.

## Simulation and routing

`src/simulation.ts` has no Three.js dependency. Dispatch reserves a single stock unit; picking decrements on-hand and releases that reservation. A source order finishes only after all units have delivered or failed. Availability is indexed by reference + normalized size and active policy. Historical pick locations are never reused to route a different storage configuration.

`src/pathfinding.ts` derives a four-neighbor, 1m occupancy grid from the union of source shelf footprints, with a 0.48m robot clearance. Synthetic equipment is excluded too. Every location has a reachable service cell. A* uses a binary min-heap and Manhattan heuristic. Robots exclusively reserve current and destination cells while traversing an edge; swaps are forbidden. Blocked routes replan around other robots. A deterministic higher-ID yield-and-hold rule breaks symmetric detour conflicts. Robot motion integrates travel budgets, including fractional speeds. Render interpolation smooths motion without changing simulation outcomes.

Source orders release in source file order, not chronological order. IDs combine wave and order number because an order number can appear in more than one wave. The default release cadence is engineered, not historical. Customer size tokens `85`, `95`, `105`, etc. are repaired to half sizes consistent with picking records; uncommon three-digit values such as `265` are preserved. Repeated customer lines remain demand.

Metrics:

- **Throughput:** fully successful whole orders / elapsed simulated hours.
- **Average completion:** release-to-final-unload time for successful orders; unavailable until one finishes.
- **Travel:** integrated robot motion in modeled meters, including station-clearance trips.
- **Working utilization:** moving + picking + unloading robot-seconds / total available robot-seconds. Waiting is separate.
- **Congestion:** actual route-wait/yield seconds. Per-robot waiting also includes outbound station queues.
- **Warehouse utilization:** nonempty modeled storage locations / 2,292 locations, shown as location occupancy. Floor-area/cubic utilization is not claimed.
- **Traffic overlay:** actual navigation cell arrival counts, not an inferred delay map.

The UI retains 720 ten-second chart samples and the most recent 20,000 events. Cumulative KPIs and order accounting remain exact if older events are dropped. JSON export includes `droppedEvents`; export earlier for a complete small-run log. Saved comparison rows persist only for the browser session.

## Validation

```bash
npm test
npm run validate:scenarios
npm run test:browser
npm run build
```

- Unit/integration tests use the real normalized data. They check all 2,292 service cells, obstacle-free A*, 10-robot occupancy and edge reservations, physical separation, inventory conservation, unique deliveries, correct order metrics, unknown/depleted stock failures, fractional-speed integration, deterministic replay, pause/reset, and policy remapping. A targeted regression reproduces the outbound head-on detour livelock and verifies it clears.
- `validate:scenarios` runs the full default 120-order window for **all four** published configurations. It requires every order to reach a terminal result, asserts stock conservation and robot separation, and writes measured results to `docs/validation-results.json`.
- Browser tests exercise start/pause/speeds, following, actual picking/delivery, source inventory inspection, assistant answers, JSON export, reset, all four policies and a 390px mobile layout. They also assert no uncaught page errors.
- Browser tests use installed Google Chrome by default. If unavailable, install Playwright's Chromium and select it:

```bash
npx playwright install chromium
PLAYWRIGHT_CHROMIUM_CHANNEL=chromium npm run test:browser
```

Diagnostics in the operations panel show measured fps and draw calls. On the implementation machine's headless Chrome the initial 41,256-carton overview was approximately 60 fps and 193 draw calls; this is an environment-specific observation, not a hardware guarantee. Shelves, posts, beams, inventory and static facility parts use instances; robot bodies use merged geometry. Pixel ratio is capped at 1.7 and shadows use a single 2048px directional map plus instanced contact shadows.

## Files

```text
src/main.ts          Dashboard, controls, inspectors, exports
src/scene.ts         Three.js warehouse, instancing, selection, animation
src/simulation.ts    Fixed-step deterministic engine and event accounting
src/pathfinding.ts   Occupancy grid, service cells, A*
src/types.ts         Dataset contracts and centralized engineering defaults
src/analysis.ts      Deterministic operations questions
scripts/prepare_data.py       Download / ZIP import / hash audit / conversion
scripts/validate-scenarios.ts Full default-demand scenario validation
public/data/         Normalized source demand, geometry, allocations, audit
public/fonts/        Locally served OFL fonts and licenses
data/raw/            Original, verified publisher files
data/manifest.json   Publisher metadata and file SHA-256 hashes
docs/                Data audit, validation results, implementation notes
tests/               Simulation tests and browser acceptance test
```

## Limitations / incomplete features

No measured warehouse stock quantity reconciliation, surveyed dimensions, actual inter-floor robot movement, physical shelf-picking manipulator, inbound replenishment simulation, articulated arm, moving truck or WMS connection is implemented. Layout Z levels are abstracted into rack tiers, and the binary DWG is not decoded. The four policies are useful published-allocation scenarios, but inventory differences preclude a causal storage-policy ranking. The 600-order and all-demand windows are available; the automated end-to-end scenario completion validation covers the default 120-order window, not the entire historical dataset. Larger runs may take substantial simulated time and retain a bounded event log.

The sandbox runs locally and demonstrates a real demand-driven autonomous workflow. Its performance figures are conditional on the explicit modeling assumptions above.

## Attribution

Dataset: Rodrigo Furlan de Assis, *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*, Mendeley Data, v1 (2024), [DOI 10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), licensed CC BY 4.0. Original source data is unchanged; application JSON transformations and modeled behaviors are described in the audit. Three.js and Lucide licenses are available in their npm packages. Bundled DM Sans and Manrope fonts are licensed under the SIL Open Font License; copies are in `public/fonts/`.
