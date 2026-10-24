# M5 data contract — proposed views, existing evidence

Design-only, 2026-10-21. [Brief](CONTROL_TOWER_DESIGN_BRIEF.md) · [Tableau plan](CONTROL_TOWER_TABLEAU_PLAN.md). The authoritative field dictionaries remain [M3](../data-quality/TABLEAU_SPEC.md) and [advanced](../data-quality/advanced/DATA_DICTIONARY.md); this document defines M5 consumption, not a replacement schema.

## Provenance and source inventory

Root source: Rodrigo Furlan de Assis, *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*, Mendeley Data v1, DOI [10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), CC BY 4.0. Retain attribution on every dashboard. Registry/decision preparation is AI-assisted; independent human/domain review is pending. Dataset version, review date and Tableau publication date are different concepts; no date here establishes current warehouse freshness.

Registry lineage: raw files → existing normalization/contract → `build_registry.py` → [registry manifest](../data-quality/registry/manifest.json) → `export_tableau.py` → [M3 manifest](../data-quality/tableau/manifest.json). Advanced lineage: same pinned inputs plus foundation → `build_advanced.py` → [advanced manifest](../data-quality/advanced/manifest.json). Do not regenerate these outputs for M5. Fresh verification results and exact hashes for consumed files are in [review/design-review.json](review/design-review.json).

Path aliases below are documentation shorthand, not new directories: **P** = `docs/data-quality/tableau/public/`; **A** = `docs/data-quality/advanced/public/`. Only existing public-allowlisted CSVs are candidates for a later public workbook. Internal detail ledgers and raw records remain local; no new CSV, enriched edge table, extract or snapshot dataset is created.

| Existing file | Rows / primary grain | Fields consumed / use |
|---|---|---|
| P/issues.csv | 14 / `issue_id` | `title`, `category`, `severity`, `root_cause`, `interpretation_confidence`, `review_state`, approval/before/after refs; issue selector and epistemic state |
| P/issue_metrics.csv | 18 / `metric_key` | `issue_id`, `affected_count`, `unit`, `denominator`, `calculation`, `population`, `evidence_ref`; three KPIs and selected evidence |
| P/decision_impacts.csv | 14 / `issue_id` | `potential_consequences`, `decision_readiness`, `measured_financial_impact`, `claim_limit`, original options; preserve the validated Decision Impact layer |
| A/decision_evidence.csv | 14 / `issue_id` | `decision_category`, `business_decision`, `business_mechanism`, `competing_explanations`, `recommendation`, `next_evidence_request`, `evidence_class`; richer request/decision wording |
| A/issue_evidence.csv | 35 / `issue_source_id` | `issue_id`, `source_id`, `lineage_role`, `selected_record_count`, `source_record_count`, `source_sha256`, `evidence_ref`; dependency matrix and lineage tooltip |
| A/policy_pairs.csv | 6 / `policy_pair_id` | `differing_skus`, `union_skus`, `l1_cell_difference`; six unequal comparisons in recommendation rationale |
| A/experiment_controls.csv | 14 / `control_id` | `scope`, `result`, `observation`, `required_evidence`; selected prerequisite explanation; no composite readiness score |
| A/reconciliation_summary.csv | 3 / `interpretation` | `customer_units`, `picking_units`, `matched_units`, `gap_units`, `excess_units`, `evidence_class`; sensitivity panel, independent of global KPIs |

Existing `A/reconciliation.csv`, `A/exception_pareto.csv`, `A/location_coverage.csv`, `A/abc_comparison.csv`, normalization tables and local registry ledgers support checks or existing drill destinations. They do not need a new M5 copy. `P/source_counts.csv` has nine analytical CSV populations; the matrix has **11** distinct evidence sources because notebook/README definition evidence also participates. Do not inner-join it to the nine-file count table and silently lose definitions.

## Logical model and fanout prevention

Preferred later model: P/issues as the issue dimension; logical one-to-one relationships on String `issue_id` to P/decision_impacts and A/decision_evidence; one-to-many relationship to A/issue_evidence. Keep P/issue_metrics as an independent source for global KPIs. Keep policy pairs, controls and interpretation summaries as independent sources. Use field aliases with source prefixes where repeated names exist, especially `status`, `title`, `evidence_ref`, and the two decision-category fields. The M5 category uses A/decision_evidence.`decision_category`; retain the original M3 category for traceability.

Do not physically join issue_metrics to issue_evidence: an issue can have several metrics and several lineage rows, multiplying both. Relationships preserve grains but do not make overlapping questions additive. One-to-one keys, complete issue-domain equality and lineage parent matches must be checked against current CSVs before modeling. If Public cannot construct this model, use independent sources and a shared manual issue parameter as described in the plan; never flatten the child facts as a UI workaround.

## Visual and measure contracts

| Component | Data and display grain | Measure / formula / expected full scope | Provenance and limit |
|---|---|---|---|
| Recommendation | A/policy_pairs, all six unordered pairs; static reviewed narrative | `COUNTD(IF differing_skus > 0 THEN policy_pair_id END)` = 6; total `COUNTD(policy_pair_id)` = 6 | Conditional encoded-cell SKU counters, not verified stock. “Hold” is an AI-proposed recommendation, not gate approval. A/experiment_controls UOM/TIME/TASKS/LAYOUT/OUTCOMES/PROTOCOL explain prerequisites |
| Demand gap KPI | P/issue_metrics; `metric_key="DQ-RECON-001:gap_units"` only | 13,003 / 228,195 published customer units = **5.70%** | Sum of positive key gaps under existing inferred size mapping; zeros/repeats retained. Not failed fulfillment, backlog or stockouts |
| Coordinate coverage KPI | Same; `DQ-LOC-001:unmapped_picking_units` only | 23,609 / 215,192 published picking units = **10.97%** | Stripped picking locations absent from coordinate master, not invalid physical locations |
| ABC disagreement KPI | Same; `DQ-ABC-001:disagreeing_references` only | 96 / 208 demanded product references = **46.15%** | Published labels versus cumulative-before extract-volume 80/95 ABC; no proof either classification is incorrect |
| Evidence Dependency Map | A/issue_evidence related to issue dimension; mark = `issue_id × source_id` | 35 lineage records collapse to **33 occupied issue/source cells** across 14 issues and 11 sources. Text role `A`, `C`, `D` or `A+C`; no quantitative size encoding | A = ledger role AFFECTED; C = CONTRIBUTING_POPULATION; D = DEFINITION_EVIDENCE. “Affected” describes an analytical selection, not verified warehouse failure. A blank cell means no registered link, not no dependency |
| Decision exposure | A/decision_evidence; one mark/category | `COUNTD(issue_id)`: measurement baseline 5; source definition 4; spatial feasibility 2; experiment design 2; slotting hypothesis 1 | Mutually exclusive assigned decision categories partition 14 questions. They do not partition records, units, loss or physical problems |
| Selected decision | Issue ID; P/decision_impacts + A/decision_evidence + P/issues | `ATTR` for decision, consequence, mechanism, competing explanations, claim limit, next request, state | Preserve unmeasured financial impact as null. Original M3 generic next request remains traceable; display A's specific next request. No split-on-pipe summation of explanations |
| Uncertainty | Issue or explicit static scope | Stock, physical distance and financial outcomes: “Not measured / not established”; reviews PENDING | P/issue_metrics physical stock/distance null; all 14 P/decision_impacts financial values blank; lack of measurements cannot become zero |
| Interpretation sensitivity | A/reconciliation_summary; one row/interpretation | Current: 13,003 gap / 228,195 demand; literal: 78,681 / 228,195; customer dedup: 12,985 / 215,460. Excess: 0 / 65,678 / 12,717 respectively | Three mutually exclusive analytical interpretations, not time, interventions or improvement results. Do not sum across rows; demand denominator changes for dedup |
| Investigation queue | A/decision_evidence, issue grain, four editorial starting points | DQ-EXP-001, DQ-STOCK-001, DQ-SIZE-001, DQ-RECON-001 in that display order; preserve full request text in detail | Editorial rationale: comparison validity, unit meaning, key interpretation, service baseline. No numerical score, monetary ranking, SLA, due date or invented assignee |
| Investigation drill | Existing published Dashboard3 and Dashboard2; local evidence links | Navigation only in mockup. Later filtering only after target fields and behavior are tested | Existing published views unchanged. No promise of issue/wave context transfer into a separately published workbook |

### Safe aggregate calculations for Tableau

Use a separate metric-key filter per global KPI. Hide automatic grand totals for issue metrics.

```tableau
// Single metric count; one metric_key must be in scope
IF COUNTD([metric_key]) = 1 THEN MIN([affected_count]) END

// Single metric share; unknowns remain null
IF COUNTD([metric_key]) = 1 AND MIN([denominator]) > 0
THEN MIN([affected_count]) / MIN([denominator]) END

// One matrix cell, WITHOUT lineage_role on Detail
IF COUNTD([lineage_role]) > 1 THEN "A+C"
ELSE CASE MIN([lineage_role])
WHEN "AFFECTED" THEN "A"
WHEN "CONTRIBUTING_POPULATION" THEN "C"
WHEN "DEFINITION_EVIDENCE" THEN "D"
END END
```

The combined-role expression is valid for the audited snapshot only: its only multi-role cells are DQ-DUP-CUSTOMER/Customer_Order and DQ-DUP-PICKING/Picking_Wave, both A+C. Any new role combination requires contract review, not silent relabeling. Tooltip shows `COUNTD(issue_source_id)` and MIN/MAX role names for one cell; a separate lineage detail worksheet exposes all individual role records. Do not SUM `selected_record_count` on a combined-role cell.

Selected metrics use the same single-key guard plus a manual metric-key selector when an issue has multiple metrics. No arbitrary MIN over multiple different metrics. Multi-key selection displays “Select one metric”; no rows displays “No metric for this selection”; a single null numerator displays “Not measured”; a zero numerator with positive denominator remains a real 0. A zero/unknown denominator has no percentage.

Sensitivity display: `MIN(gap_units)` and `MIN(customer_units)` per interpretation, with optional `MIN(gap_units)/MIN(customer_units)` only in that row. No aggregate across interpretations. The underlying reconciliation equation is Σ_key max(customer quantity − picking quantity, 0), not max(Σcustomer − Σpicking, 0). Source presence uses record counts; zero quantity does not mean absent key.

## Overlap, grain and unit audit

- Reconciliation, repeated rows, missing sizes, inferred sizes, reused order identifiers and zero quantities can concern the same customer population. Categories are labels on questions, not disjoint affected units. Neither source rows nor demand-unit issue metrics may be added across these categories.
- A fresh check of A/location_coverage finds **363 encoded cells** simultaneously unmapped and missing from Product, all in Class_Based_Storage. The global 2,610 excluded cells and 6,734 unknown-reference cells therefore overlap. Their union is not their sum. No combined defect KPI is proposed.
- Encoded cells, published units, rows, distinct references, order numbers, wave/reference/size keys, policy pairs and meters are different units. Picking happens to have one unit per row in this extract; that does not make rows and quantities universally interchangeable.
- Source counts repeat across issue links. Source hashes authenticate bytes, not business semantics. Selected counts on CONTRIBUTING_POPULATION rows are contributing selections and must not be renamed affected units. Definition evidence counts are blank, not zero.
- Policy alternatives are overlapping configurations. Six pair comparisons reuse policies and SKUs. L1 encoded-cell difference is neither physical moves nor losses. No across-pair L1 sum or policy performance ranking is valid.
- Issue classification/severity and decision categories are different dimensions. Proposed severity currently has 10 high, 3 medium, 1 low; it is editorial priority, not measured operational risk. No ordinal arithmetic on HIGH/MEDIUM/LOW.
- There is no fulfillment denominator by order: picking lacks order attribution. A wave/order demand group cannot be turned into service completion. No supplier KPI, live trend, operational throughput, real cost, ROI, stockout count or readiness percentage is supported.

## Public boundary and change policy

Use existing public headers only. Do not upload raw/internal CSVs, row selectors, local filesystem paths, the repository archive or hypothetical economics. Pseudonyms in advanced data are not a guarantee of anonymity. Registry `#issue_id` fragments are lookup instructions; a GitHub JSON URL is not a functioning issue anchor. Link to a real documentation page and show the issue ID as lookup text instead.

The HTML is a pinned **presentation** of selected values/text from these extracts. Its embedded display content is not a new authoritative dataset or a live query engine. Evidence selection, source focus and reset are simulated review affordances. Numeric cards stay fixed. Source files and manifest hashes remain the authority; design changes cannot approve a source interpretation or mutate any data.

Any later source change requires hash/key/row-count review, rerunning existing validation through a non-mutating entry point or authorized output location, then rechecking workbook calculations and interaction scope. A repository PASS does not establish Tableau rendering, the data uploaded into the workbook, domain validation, or changed gates.
