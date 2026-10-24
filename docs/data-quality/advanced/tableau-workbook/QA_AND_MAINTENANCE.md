# Remaining QA and maintenance

[Notebook](README.md) · [Evidence scope](EVIDENCE_REGISTER.md). This is a checklist, not a test-results claim. Record actual observations before changing a row to PASS.

## Remaining workbook QA

| ID | Next check and expected reasoning | Current evidence |
|---|---|---|
| Q1-branches | For every interpretation, compare B01/B02/B05 selected quantities and key-presence logic; restore current state. Full-scope comparison values below come from the CSV, not a Top 20 subtotal | Full branch QA pending; parameter control observed |
| Q1-keys | Check literal-only keys, MISSING sizes, zero-demand/present keys and zero denominators; avoid division by zero and inactive phantom keys | Repository definitions verified; rendered edge cases pending |
| Q2-B01 | Select a wave in B01, verify all B02 rows belong to that wave and expected quantities match source keys | Author-reported manual demonstration, not exhaustive |
| Q2-B05 | Repeat from B05; verify wave identity despite overlapping points | Author-reported manual demonstration, not exhaustive |
| Q2-reset | Clear each source separately, then select sequentially from both sources; inspect multi-select and Revert; record actual clearing policy | Pending; Show all values is a proposed rebuild choice, not confirmed setting |
| Q2-scope | Confirm B01 stays Top 20 while B05 retains broader waves; confirm C02 comparison is not accidentally filtered by a Wave action | Scope described in published methodology; all state combinations pending |
| Q3-ledger | Explain why C01 displays HALF_SIZE/Customer_Order while standalone filter cards show broader selections; inspect saved action/filter state in a suitable authoring environment | Cause not established; do not invent a heatmap action |
| Q3-tooltips | Check actual values/units, full identifiers, B05 records versus B01 units, fixed B04 denominator and all nine C03 cells | Tooltip metadata observed; comprehensive values pending |
| Q3-render | Check saved thumbnail, share preview, full dashboard, viewport sizes, truncation, legends and keyboard navigation | Not fully verified; no screenshot evidence archived |
| Q4-version | If deliberately exporting later, record actual `.twb`/`.twbx` path, date/hash and any embedded-data implications | No workbook file currently in repository |
| Q5-domain | Confirm size codebook, duplicate/event meaning, scope/timing and business interpretation with named domain reviewer | Pending; source correction approvals and gate decisions unchanged |

Reference full-extract values from [reconciliation_summary.csv](../public/reconciliation_summary.csv):

| Branch | Demand | Picking | Matched | Positive gap | Excess |
|---|---:|---:|---:|---:|---:|
| CURRENT_INFERRED | 228195 | 215192 | 215192 | 13003 | 0 |
| LITERAL_SIZE | 228195 | 215192 | 149514 | 78681 | 65678 |
| CUSTOMER_DEDUP | 215460 | 215192 | 202475 | 12985 | 12717 |

Use a full-scope worksheet for these checks; a Top 20 or selected wave cannot be compared directly to full-extract totals. Repository checks do not prove the uploaded Tableau data is byte-identical. No operational performance or financial test has been performed.

## Maintain the next dashboard

1. **Record what was delivered.** Add the exact published title/tab, workbook URL, date, actual worksheet inventory and new case-study link. Keep proposed panels outside the delivered inventory until observed.
2. **Write the reasoning first.** State audience/decision, one-mark grain, source key, numerator/denominator and a decision the view cannot establish. Link to existing definitions; avoid silently redefining measures in notes.
3. **Add a worksheet note from the structure below.** Use an exact title and filename; add it to both README and the concept index. Record errors actually experienced separately from diagnostic patterns.
4. **Capture evidence honestly.** Record observer/date, source/action/parameter setting, expected versus actual value, clear/reset outcome and remaining limits. Attach only real artifacts deliberately captured; do not manufacture screenshots or retroactive PASS records. Update first-person learning wording yourself.
5. **Validate and commit documentation.** Check links including fragments, worksheet coverage and source/output hashes. Stage explicit note paths and the permitted navigation edit; preserve unrelated work. Commit by meaningful deliverable and push normally only on the existing authorized branch after checking divergence. A documentation publication does not change source approvals or gates.

Reusable worksheet structure:

```text
# Exact worksheet ID and title
Evidence: observed / author-reported / repository / rebuild guidance / QA
Question, visualization reason, decision and limitation
Source, source grain/key, display grain, field types/roles
Equivalent web rebuild: shelves, Marks, calculations, tooltip
Parameters, local filters, action source/target/field and clearing scope
Experienced error and fix OR explicitly labeled diagnostic risk
Editable first-person learning takeaway
Three short questions with answers
Remaining QA and links
```

For a completed QA entry, use `date | observer | workbook/view | starting state | action | expected | observed | evidence path or explicit no-artifact note | remaining limits`. Neither a visual “looks right” nor one successful drill-down replaces population and reset checks.
