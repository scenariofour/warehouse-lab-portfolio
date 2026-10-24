# Four analytical experiences

Audience: warehouse analysts, industrial engineers, data stewards and product reviewers. The investigation path is question → population → source observation → declared interpretation → sensitivity → decision/evidence request. No visualization is a claim of failed warehouse service or operational benefit.

Each numbered item is one recommended worksheet, with only the views needed to answer a distinct question. Related sheets are built as batches in [the handoff](TABLEAU_HANDOFF.md). Use explicit text tables where evidence needs reading. D02 is reused on A rather than duplicated. Every sheet includes source attribution, full-extract scope, evidence class and a short limitation in its caption or tooltip. Visible filters must identify the active population; use text labels as well as color.

## A. Executive Intelligence

**A01 — Investigation Portfolio**

- Question: What kinds of investigation remain, and which decisions might they block?
- Source/grain: existing M3 public `issues.csv`, one issue. Fields: issue_id, category, severity, status, review_state, root_cause.
- Computation: COUNTD(issue_id), optionally grouped by category and proposed severity. Denominator: 14 registered questions only; no affected-unit share across issues.
- Filters/interactions: category, severity and status; explicit `pIssue` control opens the evidence/decision panels. A category selection does not propagate into unrelated operational facts.
- Evidence: SOURCE_DERIVED registry plus AI-proposed severity. Insight: prioritize review questions. Limit: registry coverage is not exhaustive; priority is not measured loss. All human reviews PENDING and causes UNKNOWN.

**A02 — Metric Evidence Card**

- Question: What exactly was counted for the selected issue, against which population?
- Source/grain: existing M3 public `issue_metrics.csv`, one issue/metric. Fields: issue_id, metric_id, affected_count, unit, population, denominator, denominator_definition, calculation, additivity.
- Computation: ATTR(affected_count), ATTR(denominator); optional share per individual metric with non-null positive denominator. Denominator belongs to that metric, never to the issue count.
- Filters/interactions: `pIssue`; show every metric of the selected issue as separate rows. Tooltips retain calculation and additivity. No total row.
- Evidence: SOURCE_DERIVED or unmeasured. Insight: see why 13,003/228,195 differs from 5,242/112,442. Limit: mixed units cannot be summed; physical stock/distance blanks are unknown.

**A03 — Completed Profile Checks**

- Question: Which basic key/quantity checks were run, including checks finding zero exceptions?
- Source/grain: advanced `profile_checks.csv`, source/field/check. Fields: source_id, field, check, affected_rows, population_rows.
- Computation: ATTR(affected_rows)/ATTR(population_rows) per check. Denominator: all rows of that source; never aggregate denominators across checks.
- Filters/interactions: source_id and check; table retains zero rows. No synthetic empty-check scaffolding.
- Evidence: PUBLISHED_SOURCE_OBSERVATION + SOURCE_DERIVED. Insight: distinguish a completed zero finding from an untested hypothesis. Limit: blank/negative/duplicate checks do not establish format, business-key or field-truth validity.

Display **D02 — Experiment Controls** on A as the decision-readiness panel: six failed pair controls and unresolved global prerequisites must remain visible even if issue filters are changed.

## B. Demand–Picking Reconciliation Explorer

**B01 — Reconciliation by Wave**

- Question: Which waves contribute unmatched quantities under the selected interpretation?
- Source/grain: advanced `reconciliation.csv`, union wave/reference/size key. Fields: wave_id, reference_id, size_key, three customer quantities and record counts, picking_units, picking_records.
- Computation: choose one customer quantity and presence count with `pInterpretation`; row matched = MIN(D,P), gap = MAX(D-P,0), excess = MAX(P-D,0). SUM these row fields at wave. Visible gap rate = SUM(gap)/SUM(selected D) for visible keys, null if denominator zero. Keep both signs as separate fields.
- Filters/interactions: `pInterpretation`, `pWave`, `pReference`, `pSize`; sort gap descending, search a wave to inspect. Full-scope totals live on C02, unaffected by wave/reference filters. Avoid showing 9,784 wave marks at once: use a selected wave or a top-wave overview with its scope label.
- Evidence: current = EXISTING_INFERRED_NORMALIZATION; alternatives = ANALYTICAL_SENSITIVITY. Insight: quantities can reconcile differently even with similar grand totals. Limit: no transaction status, cancellation/timing alignment or completion records; gaps are not stockouts or failed picks.

**B02 — Key Evidence Ledger**

- Question: Is a discrepancy absent key, quantity difference on present keys, zero demand or unknown size?
- Source/grain: same independent reconciliation source and key as B01. Fields: selected D/record count, P/record count, row gap/excess/match, size_key, key-presence label, reconciliation_id.
- Computation: record counts determine presence; a zero-quantity customer row is a present key. Distinguish Customer only, Picking only and Both. Exclude keys with no records in the selected branch even if another branch uses that key. Denominator: visible key quantities only.
- Filters/interactions: same explicit controls as B01; require a wave/ref before reading the ledger. Copy the key/pseudonyms into the local source-evidence lookup described in the handoff. Do not put all 148,887 rows on screen.
- Evidence: published quantities with derived join and branch semantics. Insight: explain which key contributes a gap, including missing size. Limit: contributing rows do not identify failed individual customer units. A pseudonym is an investigative reference, not an enterprise WMS ID.

**B03 — Demand Order Groups**

- Question: How do wave/order identity, repeats, zeros and missing sizes affect the requested-work population?
- Source/grain: `order_groups.csv`, one wave/order group. Fields: wave_id, order_id, order_group_id, customer_units, source_records, distinct_references, distinct_size_skus, repeat_records, missing_size_records, zero_quantity_records, order_wave_count.
- Computation: group quantities/records additive across groups; distinct references/SKUs and order_wave_count are nonadditive. COUNTD(order_group_id) and COUNTD(order_id) answer different questions. Full scope: 39,858 groups / 32,634 order numbers; 4,024 order numbers span waves.
- Filters/interactions: `pWave`; order_id filter optionally investigates other waves for an order (reset pWave to ALL first). Show a permanent “Current retained demand only; no order-level pick attribution” label. pReference/pSize and scenario controls do not apply because this table is neither SKU-grained nor scenario-expanded.
- Evidence: SOURCE_DERIVED. Insight: repeated order numbers and tuples need semantic investigation. Limit: no order IDs in picking, no completion metric; do not allocate wave picks proportionally to groups.

**B04 — Gap Concentration**

- Question: Where should a reviewer start to investigate the 13,003 current-gap units?
- Source/grain: `exception_pareto.csv`, positive-gap wave or reference group. Fields: dimension, member_id, rank, gap_units, positive_gap_keys, cumulative_gap_units, gap_denominator_units.
- Computation: gap share = SUM(gap_units)/MIN(gap_denominator_units) per member; cumulative share = MIN(cumulative_gap_units)/MIN(gap_denominator_units). Fixed full-gap denominator 13,003. A top-N filter never rebases it.
- Filters/interactions: `pParetoDimension` = wave/reference; `pTopN` filters rank. Sort supplied rank; tooltip lists cumulative and member shares. Copy member_id into matching wave/ref control for B01. This sheet is fixed CURRENT_INFERRED; scenario and operational-key filters do not apply.
- Evidence: SOURCE_DERIVED. Insight: concentrate evidence requests efficiently. Limit: wave and reference groupings describe the same units and cannot be summed; high concentration does not establish cause, severity or failure rate.

## C. Data Cleaning & Normalization Lab

**C01 — Original and Interpreted Tokens**

- Question: Which source spellings change under current representation and the literal interpretation?
- Source/grain: `normalization_tokens.csv`, source/field/exact original size token. Fields: original_token, current_value, alternative_value, token_records, token_units, rule_id.
- Computation: sum records/units within one source; current versus literal token mapping is displayed side by side. Blank remains missing, not zero. Denominator: all token records/units in the selected source. No “correction success” rate.
- Filters/interactions: source_id and rule_id; select HALF_SIZE to focus on 38,846 customer rows. Use labels for blank token and current missing value while retaining raw fields in tooltip. C02 quantifies branch changes.
- Evidence: PUBLISHED_SOURCE_OBSERVATION + EXISTING_INFERRED_NORMALIZATION; alternative literal spelling = ANALYTICAL_SENSITIVITY. Insight: inspect the exact mapping behind joins. Limit: aggregate token table omits row-specific quantities/identities; improved matching is not provider approval.

**C02 — Interpretation Sensitivity**

- Question: Which calculations change if half-token inference or customer repeat retention is changed?
- Source/grain: `reconciliation_summary.csv`, one full-extract interpretation. Fields: interpretation, evidence_class, customer_units, picking_units, matched_units, gap_units, excess_units, customer_keys, picking_keys, union_keys, positive_gap_keys.
- Computation: compare quantities and key counts in separately labeled panes; gap share = gap_units/customer_units for each row. Delta is alternative minus CURRENT_INFERRED within the same measure. No sum across branches. Fixed full-scope comparison, not affected by B filters.
- Filters/interactions: show all three rows by default; optional measure-name selection. Explicitly label current versus alternative interpretation; pInterpretation used for B does not hide the comparison here.
- Evidence: existing inferred normalization versus analytical sensitivities. Insight: dedup gives nearly equal grand totals but creates 12,717 key-level excess pick units. Limit: no approved dedup or literal-size correction; customer dedup alone changes the demand denominator. Do not dedup picking rows or call these treatments.

**C03 — ABC Basis Comparison**

- Question: How does the study population change with published ABC versus extract unit-volume ABC?
- Source/grain: `abc_comparison.csv`, demanded reference. Fields: reference_id, published_abc, derived_abc, disagrees, customer_units, rank, cumulative_customer_units, demand_denominator_units.
- Computation: heatmap COUNTD(reference_id); tooltip SUM(customer_units). Disagreement = SUM(disagrees)/COUNTD(reference_id) in visible reference subset. Global acceptance is 96/208. Fixed demand share uses MIN(228195); rank/cumulative remain full-extract even after filters.
- Filters/interactions: published/derived ABC, reference_id, disagreement. Show both count and quantity so a cell is not mistaken for unit impact.
- Evidence: published label + SOURCE_DERIVED alternate basis. Insight: published A differs from current volume A. Limit: published basis/date unverified; neither label replaces the other. Volume thresholds use cumulative BEFORE reference, original reference ascending for ties.

**C04 — Transformation and Review Register**

- Question: Which transformations are representations, inferred semantics, retention rules or alternatives requiring review?
- Source/grain: `transformation_rules.csv`, one rule. Fields: rule_id, rule_kind, approval_state, description, affected_calculations.
- Computation: text only; no progress percentage or treatment success measure. Denominator not applicable.
- Filters/interactions: rule_kind/approval_state; optional pRule string equality control shared with C01. Foundational PARSE/TRIM rules do not uniquely map to a token row.
- Evidence: explicit mixed rule provenance. Insight: current calculation support is separate from source approval. Limit: no source corrections exist; the register is not a human sign-off or authorization log.

**C05 — Location Coverage and Unresolved Groups**

- Question: How much of each source has coordinate mapping, and which unresolved groups dominate?
- Source/grain: `location_coverage.csv`, one source/location. Fields: source_scope, location_id, mapped, quantity, records, unit, scope_denominator, unknown_reference_cells.
- Computation: SUM(quantity) by mapped; coverage share = SUM(quantity)/MIN(scope_denominator) for exactly one source. Detail rows retain unmatched location IDs and unknown-reference-cell count. Every location group is disjoint within source; unknown-master cells may overlap unmapped cells.
- Filters/interactions: single `pLocationSource`, mapped and location_id; keep full source denominator after filtering. Sort unmatched groups by quantity. A second presentation of the same worksheet can be duplicated as C05b for a compact detail table if dashboard space requires it; it adds no new metric.
- Evidence: SOURCE_DERIVED. Insight: 23,609 unmapped pick units and unequal allocation exclusions have different populations. Limit: mapping absence is not invalid physical location or spare capacity; policy cells and pick units must never share a total. No map is proposed because physical scale/topology are unverified.

## D. Business Decision Intelligence

**D01 — Decision Evidence and Next Request**

- Question: What decision is at risk, what competing explanations survive, and what is the smallest useful next request?
- Source/grain: `decision_evidence.csv`, one issue. Fields: business_decision, kpi_at_risk, business_mechanism, competing_explanations, evidence_readiness, recommendation, next_evidence_request, status, review_state.
- Computation: text panels for one issue; no monetary estimate, quantified operational severity or weighted score. Denominator not applicable.
- Filters/interactions: pIssue is shared with A02 and D05. Decision category filter is optional for a list view, cleared when investigating one issue.
- Evidence: AI_PROPOSED_REQUIRES_HUMAN_REVIEW. Insight: distinguish a reproducible calculation from sufficient decision evidence. Limit: recommendations are evidence requests and withholding reasons; no operational intervention or cause is validated.

**D02 — Experiment Controls**

- Question: Is placement effect identifiable with the published policy files?
- Source/grain: `experiment_controls.csv`, global or pair control. Fields: scope, control_name, result, observation, required_evidence.
- Computation: categorical states; no readiness rate. Six pair failures plus global prerequisites. Equal retained cell totals get PASS_DESCRIPTIVE only.
- Filters/interactions: pair scope filter may narrow pair checks, but keep GLOBAL controls in view. Prefer all controls initially; never apply issue filters. Text + distinct neutral/amber/red states, no unqualified green approval.
- Evidence: observed/derived arithmetic with AI-proposed control interpretation. Insight: total equality does not control SKU mix, stock timing, eligibility or geometry. Limit: control design and protocol require a named human reviewer; G0–G4 unchanged.

**D03 — Policy Counter Diagnostics**

- Question: Which SKU counters differ between a chosen pair, and how large is that diagnostic?
- Source/grain: `policy_pairs.csv`, one unordered pair. Fields: policy_pair_id, union_skus, differing_skus, l1_cell_difference.
- Computation: differing_skus/union_skus per pair; L1 shown separately without percentage or relocation interpretation. No total row.
- Filters/interactions: choose one pair or read six individual rows; pair control can be copied to D02 scope control. No numeric sum across pairs.
- Evidence: CONDITIONAL_ASSUMPTION (size/one-cell unit and coordinate-retention rules). Insight: all six pairs differ despite equal totals. Limit: shared stock across comparisons overlaps; L1 is not observed stock loss, required moves or measured effect.

**D04 — Conditional Supply Arithmetic**

- Question: How strongly do the existing stock assumptions limit the interpretation of a policy comparison?
- Source/grain: `policy_supply.csv`, published policy. Fields: raw_encoded_cells, retained_encoded_cells, excluded_cells, conditional_supply_ceiling, demand_denominator_units.
- Computation: ceiling = existing M3 sum of min(full-history SKU demand, retained cell count); optional ratio per policy uses MIN(demand_denominator_units). Label “one undated snapshot, no receipts, one assumed unit/cell”. Do not sort as a recommendation ranking.
- Filters/interactions: policy, with paired raw/retained/excluded counts in tooltip; full demand denominator unchanged. Fixed existing branch; no new inventory scenarios.
- Evidence: CONDITIONAL_ASSUMPTION. Insight: a modeled availability ceiling can confound a placement comparison. Limit: no actual shortage, service rate, stock trajectory or cost measured; high ceiling is not a superior policy result.

**D05 — Issue Source Evidence**

- Question: Which sources support the selected question and what role do selected records play?
- Source/grain: `issue_evidence.csv`, issue/source lineage role. Fields: source_id, source_sha256, lineage_role, selected_record_count, source_record_count, evidence_ref.
- Computation: text/ATTR counts by row only; complete original selectors remain in M2 registry. Null count on README/notebook means definition evidence, not zero observations.
- Filters/interactions: pIssue shared with A02/D01. Display repository-relative evidence_ref as a lookup, not an automatically working web URL.
- Evidence: SOURCE_DERIVED lineage. Insight: distinguish affected rows from contributing populations and definition evidence. Limit: hashes authenticate source bytes, not business semantics; do not sum counts across roles/issues.

## Layout and narrative

Four dashboard tabs: `A Executive`, `B Reconciliation`, `C Normalization`, `D Decisions`. Prefer fixed 1280×900 with vertically tiled containers and readable scrolling evidence tables; no floating objects needed. Each has title/scope, visible relevant controls, primary question view, evidence panel and always-visible qualification/source footer. On C, use token/rule panels above sensitivity and ABC/coverage; use tabs/containers or worksheet tabs for deeper tables if cramped. Do not shrink 17 sheets into four unreadable screens: primary dashboards can link the detailed worksheets through visible workbook tabs. A uses A01/A02/A03/D02; B uses B01/B02/B03/B04; C uses C01/C02/C03/C04/C05; D uses D01/D02/D03/D04/D05. The exact number of views is optional; every remaining view answers its documented question.

Required reviewer journey: A02 select RECON → B inspect a wave/key → C compare raw token and branch totals → D read competing explanations and smallest evidence request. A second journey starts LOC-001 → C05 unmapped group → D01/D05 evidence request. A third uses D03/D02 to explain why a controlled storage experiment is not ready. All journeys must work using explicit controls and tabs without advanced actions.
