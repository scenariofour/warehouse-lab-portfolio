# Implementation notes

The app is a local Vite/TypeScript site. Simulation state is the single authority; Three.js never dispatches orders, changes inventory or completes tasks. There is no backend or API key. Rendering interpolates between fixed simulation steps. Every parcel animation derives from an actual delivery event and simulation time.

## State transitions

| Engine phase | Visible states | Completion action |
|---|---|---|
| Reserve and travel to source | MOVING / WAITING | Start timed shelf service at reachable location service cell |
| Abstract shelf service | PICKING | Decrement stock exactly once, release reservation, carry carton |
| Travel to individual outbound staging cell | DELIVERING / WAITING | Wait for either outbound station |
| Reserve a free station and travel | DELIVERING / WAITING | Start exclusive timed unload |
| Outbound service | UNLOADING | Emit delivery, update order, free station, dispatch next task |
| Clear station if no queued demand | MOVING / WAITING | Park, become IDLE or COMPLETED |

Orders retain their source wave/order key and CSV line row. Every unit of a source quantity becomes a uniquely identified task. Missing SKU/size or exhausted stock emits a failure with a reason and does not consume stock. Reservation availability is on-hand minus reservations; only picking decrements on-hand. Deliveries are the only operation that increments delivered units. A partially failed order reaches a failed terminal state, never successful completion.

Grid cell spacing is one modeled meter. Every cell under a shelf footprint or synthetic equipment envelope is excluded, including a robot-radius clearance. A* chooses cardinal paths in reachable free space. Moving robots reserve both endpoints; other robots cannot start a conflicting edge or swap cells. Priority rotates deterministically using the seed. The higher-ID robot in a contested cell pulls aside and holds for four seconds to break symmetric detour livelock. This is a heuristic traffic controller, not an optimal cooperative multi-agent path solver. Four complete default-demand runs and a targeted regression check liveness under the tested scenarios.

The renderer batches static boxes, instances 41,256 cartons, and instances shelf plates, beams, posts, and contact shadows. Robot body geometry is merged and shared. Source location IDs map both carton and shelf raycasts to the inventory inspector. The model is an open architectural cutaway, with low walls to preserve line of sight. Local font files and textures drawn on canvas avoid runtime network dependencies.

## Validation scope

`npm test` exercises real-data integrity, service reachability, deterministic replay and reset, full lifecycle accounting, occupied-cell and edge conflicts, minimum separation, stock exhaustion and missing references, fractional speeds, policy remapping, and a head-on livelock regression. `npm run validate:scenarios` checks every fixed step's occupied/reserved cells across all four full 120-order runs, checks physical separation samples, validates every order terminal count, reconciles all 922 demanded units with delivered/failed units, and checks unique delivery IDs. Results are saved with the seed and parameters in `validation-results.json`.

The browser acceptance test uses Playwright with real WebGL in Chrome. It covers playback controls and pause stability, robot follow, a run producing deliveries, source-location stock inspection, assistant answers, JSON export, all policy switches, reset, responsive layout and uncaught page errors. The production build also typechecks the source. No claim is made that full historical-demand windows or arbitrary modified settings are exhaustively validated.

Read `data-audit.md` for the material inventory, size, geometry, and timing ambiguities. The source's geometric dimensions and stock semantics need domain confirmation before making operational decisions from the outputs.
