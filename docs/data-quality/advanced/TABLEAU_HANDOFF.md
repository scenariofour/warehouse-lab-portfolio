# Tableau Public construction handoff

Build a **new** workbook, `Warehouse Lab — Decision Studio M4-B`; leave Dashboard01 unchanged. This handoff is a construction specification, not a tested workbook. Use [the blueprint](BLUEPRINT.md) for each view's research question and limitations; [the dictionary](DATA_DICTIONARY.md) defines every field.

## Supported baseline and boundaries

Tableau Public supports browser authoring and public file-based data. Its [Public FAQ](https://help.tableau.com/current/pro/desktop/en-us/public_faq.htm) explains that published workbooks are public and can expose underlying data. [File connection guidance](https://help.tableau.com/current/online/en-us/creator_connect.htm) explicitly includes uploading supported files to Public. Upload only allowlisted CSVs; never upload the raw/internal directories or a repository archive.

Use ordinary sheets, calculated fields, filter cards, manual parameter controls, text tooltips and visible sheet/dashboard tabs. [Parameter documentation](https://help.tableau.com/current/pro/desktop/en-us/parameters_create.htm) applies to Public and documents workbook-wide parameters used in calculations. The [web/Desktop comparison](https://help.tableau.com/current/pro/desktop/en-us/server_desktop_web_edit_differences.htm) documents web calculations/parameters/table calculations but applies to Cloud/Server/Desktop; it is not a blanket guarantee for every Public deployment. Actual Public import/render remains to be checked.

Optional Desktop assembly: custom parameter/set/URL/Go-to-Sheet actions and Viz in Tooltip are outside this web baseline. The comparison documents Desktop configuration for actions and Viz in Tooltip; do not promise them in a browser-only build. Dashboard [Use as Filter](https://help.tableau.com/current/pro/desktop/en-us/actions_dashboards.htm) is a simpler documented interaction, but still validate the Public UI and target scope before enabling it. No extension is required. Use tabs when navigation objects/actions are absent.

**First authoring check:** import `reconciliation.csv`, make a basic total sheet, then try adding `reconciliation_summary.csv` as an **independent new data source**, not a join or union. Confirm switching sources works without automatic relationships. If the current Public interface cannot add the required independent file sources, use free Tableau Desktop Public Edition to assemble a workbook with separate sources, then continue editing supported sheets on the web. Do not flatten unrelated grains to bypass the UI limitation. Browser-only fallback is separate single-source workbooks with manual navigation; parameters cannot synchronize across those workbooks. A seamless four-dashboard workbook then remains pending Desktop assembly. This contingency is explicit, not an assertion that Public provides every multi-source authoring control.

## Batch 1 — Sources, types and controls

Import the 14 advanced CSVs as independent sources. Reuse three existing M3 public sources: `issues.csv`, `issue_metrics.csv`, `source_counts.csv`. `decision_impacts.csv` is optional historical context and unnecessary because advanced decision_evidence supplies the fuller question. Do not connect the M3 internal facts. Source names: `M4_reconciliation`, `M4_order_groups`, etc.; `M3_issues`, `M3_issue_metrics`, `M3_source_counts`.

Before building sheets, set every ID, size_key and token/value field to String/Dimension; `rank` and boolean-coded `mapped`/`disagrees` are dimensions when used categorically. Counts and quantities are whole numbers. Blank numeric fields in M3 must remain null. Never make size_key numeric: `MISSING` is intentional. Compare the Data pane field list to the manifest. A preview may show only a subset of the 148,887 reconciliation rows; validate aggregate totals, not the preview row count. Never pivot customer alternatives into duplicated picking rows.

Create workbook controls:

| Parameter | Type / allowed values / default | Used on |
|---|---|---|
| pInterpretation | String list: CURRENT_INFERRED, LITERAL_SIZE, CUSTOMER_DEDUP; default CURRENT_INFERRED | B01/B02 only; visible title states interpretation |
| pIssue | String list of the 14 registry issue_id values; default DQ-RECON-001 | A02, D01, D05; not portfolio/control totals |
| pWave | String, All values; default ALL; type/copy opaque wave ID | B01/B02/B03 |
| pReference | String, All values; default ALL | B01/B02 |
| pSize | String, All values; default ALL; exact numeric spelling or MISSING | B01/B02 |
| pParetoDimension | String list wave/reference; default wave | B04 |
| pTopN | Integer range 5–100, step 5; default 20 | B04 fixed supplied rank |
| pLocationSource | String list Picking_Wave, Random_Storage, Class_Based_Storage, Dedicated_Storage, Hybrid_Storage; default Picking_Wave | C05/C05b |
| pPair | String list ALL and six policy_pair_id values; default ALL | D02/D03 |
| pRule (optional) | String list ALL and nine rule_id values; default ALL | C01/C04; explain foundational rules have no exclusive token assignment |

Case matters. ALL is an explicit sentinel, not a data member. A typo in an opaque ID produces no rows; instruct users to reset to ALL and copy an ID from a table. Avoid very large parameter lists for waves/references. A single-source searchable filter card is also acceptable; it does not synchronize to a different source automatically.

## Batch 2 — Reconciliation and order investigation

Create these **row-level** calculated fields in M4_reconciliation:

```tableau
// Selected Customer Units
CASE [pInterpretation]
WHEN "CURRENT_INFERRED" THEN [current_customer_units]
WHEN "LITERAL_SIZE" THEN [literal_customer_units]
WHEN "CUSTOMER_DEDUP" THEN [dedup_customer_units]
END

// Selected Customer Records
CASE [pInterpretation]
WHEN "CURRENT_INFERRED" THEN [current_customer_records]
WHEN "LITERAL_SIZE" THEN [literal_customer_records]
WHEN "CUSTOMER_DEDUP" THEN [dedup_customer_records]
END

// Active Key
[Selected Customer Records] > 0 OR [picking_records] > 0

// Matched Units
MIN([Selected Customer Units], [picking_units])

// Positive Gap Units
MAX([Selected Customer Units] - [picking_units], 0)

// Picking Excess Units
MAX([picking_units] - [Selected Customer Units], 0)

// Key Presence
IF [Selected Customer Records] > 0 AND [picking_records] > 0 THEN "Both"
ELSEIF [Selected Customer Records] > 0 THEN "Customer only"
ELSEIF [picking_records] > 0 THEN "Picking only"
ELSE "Inactive in selected interpretation" END

// Visible Gap Share (aggregate field)
IF SUM([Selected Customer Units]) > 0
THEN SUM([Positive Gap Units]) / SUM([Selected Customer Units]) END

// Keep Operational Selection
([pWave] = "ALL" OR [wave_id] = [pWave])
AND ([pReference] = "ALL" OR [reference_id] = [pReference])
AND ([pSize] = "ALL" OR [size_key] = [pSize])
```

Put Active Key = True and Keep Operational Selection = True on B01/B02. Keep Operational Selection is not applied to unrelated sources. On M4_order_groups create `Keep Wave = [pWave] = "ALL" OR [wave_id] = [pWave]`; filter True on B03. No reference/size/scenario calculation belongs on B03.

| Sheet | Rows | Columns | Marks / configuration |
|---|---|---|---|
| B01 Reconciliation by Wave | wave_id | SUM(Positive Gap Units) | Bar; sort descending. Tooltip SUM selected customer, picking, matched, excess, records and Visible Gap Share. Add wave/reference/size/interpretation controls; title “Visible key population”. For unfiltered overview, a local top-wave filter is allowed only with a top-subset caption. |
| B02 Key Evidence Ledger | wave_id, reference_id, size_key, Key Presence | Measure Names | Text; Measure Values: selected customer, picking, matched, positive gap, excess and both record counts. reconciliation_id on Tooltip/Detail. Require selected wave or reference before displaying the detailed ledger (optional Boolean `pWave<>"ALL" OR pReference<>"ALL"` filter). |
| B03 Demand Order Groups | wave_id, order_id, order_group_id | Measure Names | Text; customer_units/source_records/repeat_records/missing_size_records/zero_quantity_records SUM; distinct_references, distinct_size_skus and order_wave_count MIN per group. Keep Wave True. No order-level picking columns. |
| B04 Gap Concentration | member_id, discrete rank | SUM(gap_units) | Bar; color single neutral, sort rank ascending. Filter dimension=pParetoDimension and rank<=pTopN. Tooltip MIN(cumulative_gap_units)/MIN(gap_denominator_units) and SUM(gap_units)/MIN(gap_denominator_units). Keep scope fixed CURRENT_INFERRED. No table calculation needed. |

B04's supplied cumulative is fixed to the original rank; a member filter does not recompute its cumulative. Do not apply pWave/pReference/pInterpretation to it. An optional dual axis cumulative line is unnecessary; keep the percent in labels/tooltips. This avoids fragile table-calculation addressing.

For authorized local source investigation, reverse any public reconciliation_id, including literal-only keys, without uploading source rows. From repository root:

```sh
python3 -B scripts/data_quality/lookup_advanced.py key_COPY_FROM_TABLEAU
```

The lookup authenticates inputs, then returns source hashes, original wave/reference/size key and exact compressed ordinals for current, literal, customer-dedup and picking contributors. Header=logical record 1. It uses the same declared normalization and complete original tuples for repeat selection; no customer/operator fields are printed. Zero contributing records and zero quantities remain distinct. Full source selectors are local evidence, not an extra public upload. Never map a literal-only key to a current key by nearest size.

## Batch 3 — Normalization, classification and mapping

| Sheet | Rows | Columns | Marks / configuration |
|---|---|---|---|
| C01 Original and Interpreted Tokens | source_id, rule_id, original_token, current_value, alternative_value | Measure Names | Text; SUM(token_records), SUM(token_units). Label missing using `IF ISNULL([original_token]) OR [original_token]="" THEN "[blank source token]" ELSE [original_token] END`; keep exact original field on tooltip. Source/rule filters. |
| C02 Interpretation Sensitivity | interpretation | Measure Names | Text/highlight table; MIN customer/picking/matched/gap/excess, then key counts. Use separate quantity/count panes if colors imply unit comparability. Each row one scenario; no grand totals. `Full Gap Share = MIN(gap_units)/MIN(customer_units)`. Keep all branches visible. |
| C03 ABC Basis Comparison | published_abc | derived_abc | Square; COUNTD(reference_id) on Color/Label; SUM(customer_units) on tooltip. Add both ABC filters and optional disagrees filter. Caption 96/208 at full scope, not hard-coded into filtered result. |
| C04 Transformation Register | rule_id, rule_kind, approval_state | none | Text description + affected_calculations in Tooltip or separate wide text column. Use readable wrapped text. No treatment success color. |
| C05 Location Coverage | discrete mapped | SUM(quantity) | Bar; source_scope=pLocationSource. Tooltip `SUM(quantity)/MIN(scope_denominator)`, MIN(unit), SUM(records). Keep denominator full-source. mapped=0 label “Unmatched coordinates”; mapped=1 “Coordinate joined”. |
| C05b Location Evidence (optional detail presentation) | location_id, mapped | Measure Names | Text SUM(quantity), SUM(records), SUM(unknown_reference_cells); same source parameter, optional mapped=0 filter. Sort quantity descending. Header states correct unit. |

For branch deltas, C02's baseline is the same-measure CURRENT_INFERRED row. Prefer a simple three-row comparison. If explicit deltas are required, create FIXED baseline fields in this source, e.g. `{ FIXED : MIN(IF [interpretation]="CURRENT_INFERRED" THEN [matched_units] END) }`, then `MIN([matched_units])-MIN([Baseline Matched])`; no scenario filter in context. Baseline should remain 215,192 even when selecting an alternative. This is optional, not required for core acceptance.

Published/derived ABC use different bases; no trend line or accuracy target is appropriate. `SUM(disagrees)/COUNTD(reference_id)` describes visible references, whereas `SUM(customer_units)/MIN(demand_denominator_units)` describes fixed full-extract unit share. Do not substitute one denominator for the other.

## Batch 4 — Executive, decisions and evidence

Create `Keep Issue = [issue_id]=[pIssue]` independently in M3_issue_metrics, M4_decision_evidence and M4_issue_evidence. Same workbook parameter, same string ID, no data blending. Create `Keep Pair Control = [scope]="GLOBAL" OR [pPair]="ALL" OR [scope]=[pPair]` in experiment_controls; in policy_pairs use `pPair="ALL" OR policy_pair_id=pPair`.

| Sheet | Rows | Columns | Marks / configuration |
|---|---|---|---|
| A01 Investigation Portfolio | category | COUNTD(issue_id) | Bar; severity on Color, issue_id/title/status/review_state in Tooltip; category/severity/status filters. Do not apply Keep Issue; portfolio retains context. |
| A02 Metric Evidence Card | metric_id, unit | Measure Names | Text; MIN affected_count/denominator; population/denominator_definition/calculation/additivity in Tooltip. Keep Issue True. No grand totals. |
| A03 Completed Profile Checks | source_id, field, check | Measure Names | Text MIN affected_rows/population_rows. Rate if wanted MIN(affected_rows)/MIN(population_rows) per row. Keep zeros visible. |
| D01 Decision Evidence | issue_id, title | none | Text panels for decision, KPI risk, mechanism, competing explanations, evidence_readiness, recommendation and next request; Keep Issue True. Use several same-source text worksheets if required for legible wrapping; these are panels, not extra metrics. |
| D02 Experiment Controls | scope, control_name | result | Text observation/required_evidence on Tooltip; result on Color and Label; Keep Pair Control True. Preserve global controls. Reuse on A and D. |
| D03 Policy Counter Diagnostics | policy_pair_id | Measure Names | Text MIN differing_skus, union_skus, L1; pair discrepancy share = MIN(differing_skus)/MIN(union_skus). Pair filter. No totals. |
| D04 Conditional Supply Arithmetic | policy | MIN(conditional_supply_ceiling) | Bar; fixed source order Random/Class_Based/Dedicated/Hybrid, not recommendation rank. Tooltip MIN raw/retained/excluded and MIN demand denominator. Persistent assumption caption. |
| D05 Issue Source Evidence | issue_source_id, source_id, lineage_role | Measure Names | Text MIN selected/source record counts; hash and evidence_ref on Tooltip. Keep Issue True. Do not sum definition/population/affected roles. |

Optional A02 share, safely guarded to a single metric:

```tableau
IF COUNTD([metric_key]) = 1 AND NOT ISNULL(MIN([affected_count]))
AND MIN([denominator]) > 0
THEN MIN([affected_count]) / MIN([denominator]) END
```

Do not use ZN() on unknown stock/distance or missing denominators. Format an unknown measure as “Unknown / unmeasured” using a separate display calculation; never replace null with zero in the numeric field. Source status and human approval are not editable through a Tableau filter.

## Batch 5 — Dashboards, navigation and interaction validation

Use the four dashboard names/layout in BLUEPRINT.md. Shared parameters persist across tabs in the same workbook, but only affect sheets with matching calculations. Every dashboard displays the relevant controls and a scope note; hide irrelevant controls. Reset pWave/pReference/pSize to ALL and pInterpretation to CURRENT_INFERRED for a clean starting view. Tabs are the supported baseline navigation. A text instruction can send readers to an exposed detail worksheet; do not depend on custom actions.

Same-source filtering can be enabled after checking selected marks/clear selection. Cross-source filters are **not automatic**: B01 wave may identify many B03 groups, but its reference/size cannot filter that table correctly. An issue selection must not filter reconciliation units as though one issue owns each key. C05 locations cannot filter reconciliation because locations are not in its grain. pIssue links only issue-aware sources; pWave links only wave-aware sources; pPair links only relevant controls/pairs. Clearing a mark action should show all data; clearing a parameter requires setting ALL. Never claim that a parameter reset in one workbook resets another workbook.

Keep conventional tooltips and visible filters as the browser-first solution. Configure cross-dashboard drill actions, parameter actions, set actions, custom evidence URL actions and Viz in Tooltip in Desktop if later desired; test the published Public view. Do not infer that an action present in a Desktop-published view is authorable in web UI.

## Batch 6 — Validation and acceptance

Run `python3 -B scripts/data_quality/verify_advanced.py`. `consumer_checks.sql` contains executable source-consumer queries; the verifier loads public CSVs into `out_<name>` SQLite tables with declared types and executes them. `evidence/validation.json:consumer_checks` records actual/expected values, including:

| Check | Expected full scope |
|---|---|
| Current D / P / matched / gap / excess | 228195 / 215192 / 215192 / 13003 / 0 |
| Current customer keys / pick keys / positive gap keys | 112442 / 107283 / 5242 |
| Literal matched | 149514 |
| Customer dedup matched / gap / excess | 202475 / 12985 / 12717 |
| Wave/order groups / order numbers / multi-wave numbers | 39858 / 32634 / 4024 |
| Unmapped pick units / IDs | 23609 / 22 |
| ABC references / disagreements / quantity | 208 / 96 / 228195 |
| Unknown-master / excluded allocation cells | 6734 / 2610; may overlap |
| Unequal policy pairs / failed controls | 6 / 7 (six pair controls and one coverage control) |
| Policy ceilings Random / Class_Based / Dedicated / Hybrid | 28392 / 17079 / 33093 / 32201; conditional only |

Manual Tableau acceptance is **PENDING** until an author/reviewer records evidence:

1. Import aggregate totals match above despite any preview truncation; no physical joins, extra rows or numeric ID inference. Each CSV row count matches manifest.
2. Switch all three interpretations: current values recover exactly; current inactive literal-only keys disappear; missing-size keys remain. Both gap and excess appear under dedup. C02 stays full-scope while B filters change.
3. Choose a wave/ref/size; B01/B02 agree, B03 only responds to wave and shows retained demand. No order-level pick result appears. pWave ALL restores full populations.
4. In Pareto, top N changes visible marks but fixed denominator remains 13,003; each dimension independently totals that quantity. Sort uses supplied rank. Location source switch changes unit and denominator; unmatched picking yields 23,609/215,192, not a sum across policies.
5. A02/D01/D05 respond to the same pIssue. Unknown stock/distance remain unknown; no source correction/reviewer approval is invented. D02 retains global blockers after pair selection.
6. Readable captions/tooltips, keyboard-accessible controls, non-color state labels, empty-selection explanation, tabs and reset instructions work in the actual published view. Capture screenshots/worksheet totals as manual evidence; no automatic publication is authorized here.

AI Product Management review: a named domain reviewer independently performs the three blueprint journeys and answers five prompts correctly: denominator, evidence class, competing explanation, missing prerequisite, and smallest next request. Proposed acceptance: 15/15 correct answers, zero interpretations of analytical sensitivities as approved corrections, zero claims of measured savings/failure/causal policy benefit, and 100% expected arithmetic checks. A second reviewer checks all 14 issue-decision requests for relevance and source support. These are proposed acceptance thresholds; no reviewer result is fabricated. Failing comprehension requires wording/interaction revision before release, not source-data rewriting.
