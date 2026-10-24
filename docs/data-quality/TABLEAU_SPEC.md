# Tableau data model and dashboard specification — M3

2026-10-18 · Prepared for authoring and human review. CSVs are ready; no Tableau workbook has been authored or published. G0–G4 PENDING. All values describe the pinned published extract or declared derived calculations. No real warehouse failure, saved money or policy effect is established.

## Inputs and reproduction

Python 3.10+ standard library, repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/data_quality/build_registry.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/data_quality/export_tableau.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/data_quality/verify.py M3
```

Use [tableau/internal](tableau/internal) for local investigation. The four-file [public subset](tableau/public) is prepared for owner review only. No file is written to the app's served `public/` directory and no publishing API is called. [manifest.json](tableau/manifest.json) records exact columns, keys, grains, measures, row counts, code/input hashes and public allowlist. Rebuild registry before extracts if code/source contracts change; stop on hash disagreement.

CSV encoding: UTF-8 without BOM, comma delimiter, LF records, standard quoted text. Infer all identifiers and sizes as strings, including numeric-looking references and blank size; quantities/counts as whole numbers. Blank numeric/reviewer/approval/before/after values mean unknown or not present, never zero or an empty successful treatment. All fields are capped at 4,096 characters by consumer validation; complete long ordinal lists remain in the registry, reached via evidence/lineage references or compact raw-field selectors. `evidence_ref` is repository-relative; `#...` fragments are lookup instructions for the companion ledger, not a hosted web endpoint.

Source attribution on every dashboard/export handoff: Rodrigo Furlan de Assis, *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*, Mendeley Data v1, DOI [10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), CC BY 4.0. Derived registry/extracts prepared with AI assistance; independent review pending. Published fields/counts, derived findings, existing assumptions and synthetic scenarios must have separate labels. M3 contains no synthetic or simulation records.

## Extract dictionary

All tables have `category`, `status`, `unit`, `data_origin`, and `evidence_ref`. Every issue-linked table also has `issue_id`. `source_counts` instead represents a published source population and uses category SOURCE_POPULATION and status PUBLISHED_SNAPSHOT_MEANING_UNVERIFIED. Status fields are workflow/definition states, not operational outcomes.

| Internal CSV | Grain / primary key | Measurements / denominator and allowed aggregation |
|---|---|---|
| issues.csv | Investigation question / issue_id (14) | COUNTD issue_id is issue count, never unique affected records. Severity is proposed decision priority. All reviews pending; correction references blank. |
| issue_metrics.csv | Issue + metric / metric_key (18) | affected_count, unit, population, denominator, definition and calculation. Filter one metric_key; use MIN/ATTR for count and denominator. Cross-issue sum prohibited. Null physical quantities remain unknown. |
| issue_sources.csv | Issue/source/role selector / issue_source_id (35) | Selected ordinal count, full source record count, range count and source hash/columns. lineage_ref locates exact inclusive ranges. Contributing rows are not necessarily affected; source totals recur across issues. |
| decision_impacts.csv | Issue decision question / issue_id (14) | Decision category, hypothetical causes/consequences, options, next evidence request and readiness. Monetary impact blank. No sum of savings or ROI. |
| source_counts.csv | Original analytical CSV / source_id (9) | Original row count, source hash, header-excluded definition. Never call the sum unique transactions or units. |
| reconciliation_detail.csv | Positive-gap wave/reference/inferred-size key / reconciliation_id (5,242) | SUM gap_units = 13,003 within this table. Full requested denominator 228,195 is in issue_metrics. Customer/pick quantities here cover positive-gap keys only. Exact short source ordinal lists retained. |
| unmapped_locations.csv | Unmatched stripped picking location / location_id (22) | SUM picking_units = 23,609; source record counts and exact location selector. Full picking denominator 215,192 in issue_metrics. Not proof location is invalid. |
| classification_detail.csv | Demanded reference / reference (208) | SUM disagrees = 96; SUM customer_units = 228,195. Denominator COUNTD reference = 208. Published/derived columns are simultaneous classifications, not treatment before/after. Product ordinal and ledger reference retained. |
| policy_pairs.csv | Unordered policy pair / policy_pair_id (6) | differing_skus / union_skus for one pair, plus L1 encoded-cell difference. Do not sum across pairs. L1 is not moves or lost stock. |
| policy_supply.csv | Published policy / policy (4) | Raw/retained/excluded cells and distinct retained SKUs; conditional Σ min(demand, assumed cells). Same full demand denominator repeats per alternative. No receipts, date unknown, one-cell-unit assumption. Never sum alternative-policy ceilings or demand denominators. |

The public subset contains issues, issue_metrics, decision_impacts and source_counts only. It excludes transaction/customer/operator/date identifiers, SKU/location IDs, source ordinal selections and internal investigation detail. No hypothetical economics from prior discovery enters these exports. Allowlist and header tests verify the boundary; the owner still reviews audience, attribution, text and evidence-link visibility before sharing. The original source is public; this subset does not claim anonymity guarantees or new permission to publish unrelated work.

## Model and counting rules

Create a core Tableau source using logical relationships on issue_id: `issues` (one) to `issue_metrics` (many), `issue_sources` (many), and `decision_impacts` (one). The keys are CSV-tested; all issue-linked child rows match issues. Never physically join these child tables into one flat table. Keep source_counts as a separate source-count worksheet. Definition evidence (README/notebook) has no row in the analytical CSV source-count table; no forced inner join should drop it.

Create separate single-table sources for reconciliation_detail, unmapped_locations, classification_detail, policy_pairs and policy_supply. Dashboard actions pass selected issue_id to compatible investigation sheets. This avoids cross-fact duplication and does not require a new multi-fact feature. Relationships preserve table grains; they do not make overlapping issue populations additive. Tableau's [data-model guidance](https://help.tableau.com/current/pro/desktop/en-us/datasource_datamodel.htm) distinguishes logical relationships from row-merging physical joins and describes measure duplication risks. [Relationship FAQ](https://help.tableau.com/current/pro/desktop/en-us/datasource_datamodel_faq.htm). Documentation checked 2026-10-18; actual workbook behavior still requires the authoring checks below.

Apply these calculations to issue_metrics with a single metric_key on the mark/filter:

```text
Affected count (single metric) =
IF COUNTD([metric_key]) = 1 THEN MIN([affected_count]) END

Affected share (single metric) =
IF COUNTD([metric_key]) = 1 AND MIN([denominator]) > 0
THEN MIN([affected_count]) / MIN([denominator]) END
```

Show “Unknown / not measured” when affected_count or denominator is null; show “Select one metric” for multiple keys. Hide automatic totals/subtotals for these fields. Do not expose SUM(affected_count) as a default KPI. For detail filters such as a wave or reference, detail sums change but global denominators remain fixed: label this “selected contribution / full extract denominator.” Recompute a subset denominator only from a separately complete population table, which is not supplied for positive-gap-only detail.

There is no total unique affected-unit measure or quality score. Customer demand, picking units, source records, references, cells, policy pairs and unknown physical stock are different populations. Missing sizes/repeats/order reuse can overlap demand gaps; unknown master cells overlap some geometry exclusions. Unit conversions and percentages cannot remove those overlaps. COUNTD issue_id counts investigation questions only.

## A — Data Quality Overview

Audience: analyst deciding where evidence is insufficient. Suggested fixed desktop canvas 1,360 × 900 with tiled containers and a vertically stacked narrow-screen alternative. Top 80px: title, source version/attribution, “Derived from published data; review pending; G0–G4 PENDING.” Next 140px: three single-metric KPI cards:

- “Demand/picking quantity gap: 13,003 / 228,195 requested units (5.70%).” Tooltip: existing inferred size mapping, repeats retained, cause unknown, not failed fulfillment.
- “Picking units without coordinate match: 23,609 / 215,192 (10.97%).” Tooltip: source coverage gap, not invalid physical location.
- “ABC label disagreements: 96 / 208 references (46.15%).” Tooltip: extract-volume versus published basis, no label correction.

Main 420px: category × handling-state heatmap using COUNTD issue_id; severity is a symbol/label, not a loss estimate. Adjacent panel: source counts and declared population definitions. Lower panel: 14-issue text table with issue ID, title, priority, confidence and state. Do not show an all-category affected-units total or a resolution progress percentage that implies approved success. All 14 currently await source clarification; resolved and accepted limitation counts are zero.

Filters: category, state, proposed severity, interpretation confidence, decision category. The three global KPI sheets remain explicitly labeled “Full extract” unless the selected issue applies; do not partially filter numerator and denominator. Source-file filtering applies only to lineage/source-count views, never a fanout-driven resumming of metric totals. Color by handling state, use labels/icons as well as color; reserve neutral gray for unknown, amber for investigation priority, no error-red warehouse-failure label.

## B — Investigation and Resolution

Left 260px: selectable issue list. Right top 220px: selected title, detection equation, population, unit/denominator, confidence, unknown cause, pending reviewer, options and residual uncertainty. Under it, use a navigation parameter for compatible detail views:

- Reconciliation: positive-gap keys ranked by gap, with wave/reference/size filters and exact source row list. Labels distinguish key count from quantity gap. Display 5,242 keys and retained full-extract denominator.
- Locations: unmatched-location quantities and record counts; no map point or fabricated coordinate. Filter one location, use source_selector to reproduce raw rows.
- Classification: published × derived ABC cross-tab, COUNTD reference and optional SUM customer units; adjacent both-label table and lineage link. Neither side is “corrected.”
- Policy controls: six pair rows, differing/union SKU counters and L1 in separate labeled measures; policy_supply bars show conditional ceilings of 28,392 / 17,079 / 33,093 / 32,201 for Random/Class-Based/Dedicated/Hybrid, without a “best policy” rank.
- Other issues: lineage source/role/count table and evidence instructions. For stock/layout, display unavailable physical quantity/distance and required definitions.

Select mark → filter selected issue/details and highlight evidence. Clear selection → restore overview. Source-detail action opens a repository evidence URL only after the author configures a reviewed base URL; do not blindly publish internal file paths as web links. Current before/after panel reads “No approved correction or treatment recorded”; reference fields are blank. No synthetic trend, resolution date, reviewer name or successful correction chart is supplied. Future approved treatment needs a versioned record and revalidation; this snapshot is not a history/event table.

## C — Business and Decision Impact

Main left: decision category × issue table (COUNTD issue_id) with states. Right: selected decision, potential consequence, competing causes, next evidence request and options. Labels: “Potential consequence — not observed business loss” and “Decision currently requires source clarification.” A small dependency panel connects definition → reliable measure → controlled study → possible operating decision; it is a proposed workflow, not stage-gate completion.

Use stock and policy examples to explain why availability/task mix can confound a slotting recommendation. No ROI bar, financial benefit estimate, policy winner, real stockout count or capacity-saving metric. measured_financial_impact stays null. The appropriate action may be to retain uncertainty and stop if source definitions cannot be obtained.

## Acceptance in Tableau — still pending authoring

The automated M3 checks validate CSVs and counting contracts, not a Tableau rendering. A human author/reviewer must:

1. Import identifiers as strings and blanks as null, confirm table row counts/keys against manifest, and verify no hidden physical joins.
2. Reproduce the three KPI numerators/denominators above and six unequal pairs; confirm category/lineage selections do not multiply totals. Confirm multiple metric selection suppresses shares and missing physical quantities render unknown.
3. Drill one reconciliation key and one location to exact original rows; explain the contributing-row versus failed-unit distinction. Explain why the two ABC columns and policy alternatives are not before/after corrections.
4. Test select/clear/filter actions, fixed denominator labels, keyboard focus, readable contrast, labels/tooltips and the narrow layout. Review source links, attribution and export scope.
5. Record reviewer, workbook version/hash, software version and evidence screenshots/results; owner approves public sharing separately. No Tableau Public publication is authorized by this artifact. G0–G4 remain PENDING.
