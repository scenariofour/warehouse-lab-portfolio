# Calculation and authoring reference

[Evidence register](EVIDENCE_REGISTER.md) · [Learning index](LEARNING_INDEX.md). This is **G: equivalent reconstruction guidance** anchored in repository definitions, not extracted workbook XML. Tableau may display `wave_id` as “Wave Id”; formulas below use original CSV names. Preserve equivalent logic when adapting display aliases.

## Types, roles and display

Ask three separate questions: what type is the value (String/Number), what role does it play (Dimension/Measure), and how should it display (Discrete/Continuous)? String IDs remain dimensions. Integer rank is an ordinal label, not an additive business quantity. Discrete pills create headers; continuous pills create axes. Blue does not mean “all dimensions”, and green does not mean “all measures”. [Tableau field roles](https://help.tableau.com/current/pro/desktop/en-us/datafields_typesandroles.htm).

In these sheets: wave/reference/size are discrete dimensions; quantities are usually continuous SUM measures; rank is a discrete dimension for the concentration sequence; ABC/source/rule are discrete dimensions for matrix cells. Keep `size_key` as String so `MISSING` survives. Do not add ranks or identifiers just because Tableau inferred a numeric measure.

## Selected interpretation calculations

Use [reconciliation.csv](../public/reconciliation.csv), one union wave/reference/size key across interpretations. Create a String list parameter `pInterpretation`: CURRENT_INFERRED (default), LITERAL_SIZE, CUSTOMER_DEDUP. Display aliases may say “Current inferred”, etc.; the published viewer showed that friendly label, not its stored code. Adjust CASE values to the actual parameter values when rebuilding. A parameter changes a calculation only where referenced; it is not a row filter by itself. [Parameter concepts](https://help.tableau.com/current/pro/desktop/en-us/parameters_create.htm).

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

// Active Key — filter True when reconstructing B01/B02/B05
[Selected Customer Records] > 0 OR [picking_records] > 0

// Matched Units — row-level scalar minimum
MIN([Selected Customer Units], [picking_units])

// Positive Gap Units — row-level, not a wave net difference
MAX([Selected Customer Units] - [picking_units], 0)

// Picking Excess Units
MAX([picking_units] - [Selected Customer Units], 0)

// Key Presence
IF [Selected Customer Records] > 0 AND [picking_records] > 0 THEN "Both"
ELSEIF [Selected Customer Records] > 0 THEN "Customer only"
ELSEIF [picking_records] > 0 THEN "Picking only"
ELSE "Inactive in selected interpretation" END

// Wave Gap Share — aggregate, at wave marks in B05
IF SUM([Selected Customer Units]) > 0
THEN SUM([Positive Gap Units]) / SUM([Selected Customer Units]) END
```

Source presence uses records, not quantity: a zero-quantity record is still a present key. At wave display grain, SUM the row-level measures. For an illustrative pair of keys (D=10/P=0 and D=0/P=10), gap/excess are each 10 although net D−P is zero. This is a teaching example, not a warehouse observation or new operational fixture. Do not average key gap percentages to obtain a wave share. Unknown denominators stay null; do not silently turn them into zero.

## Fixed denominators and counts

B04 uses [exception_pareto.csv](../public/exception_pareto.csv), already aggregated by dimension/member. Filter `dimension="wave"`, `rank` 1–20. Per member, `Cumulative Gap Share = MIN([cumulative_gap_units])/MIN([gap_denominator_units])`. The denominator is 13003, repeated across rows; SUM would duplicate it. The visible Top 20 subtotal is 1720. Their shares answer different questions: 168/13003 ≈ 1.29% of all gaps versus 168/1720 ≈ 9.77% of the visible subset. Filtering does not regenerate the supplied cumulative rank.

C03 uses `Distinct References = COUNTD([reference_id])`; SUM(customer_units) answers a separate volume question. COUNTD counts non-null distinct IDs and follows the visible filters; it does not validate a join. This extract already has one reference per row, so COUNT and COUNTD happen to coincide before any model change. [Aggregate functions](https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_aggregate_create.htm).

## Measure Names and Values

In B02/C01, place discrete Measure Names on Columns and Measure Values on Text; retain only intended measures. C02 uses the same generated fields to create adjacent bars for gap/excess by interpretation. Remove unintended counts/ranks from the Measure Values card as well as checking the Measure Names filter. Inspect the aggregation separately for each measure. The generated field names describe presentation, not new data grain. [Tableau reference](https://help.tableau.com/current/pro/desktop/en-us/datafields_understanddatawindow_meavalues.htm).

## Filter action direction

**U2 establishes runtime drill-down**, not the exact stored settings. Equivalent rebuild: on Dashboard 03 create a Select Filter Action with **B01 as source, B02 as target**, mapping String wave_id → String wave_id. Repeat for **B05 → B02**. B05 must retain Wave Id on Detail. Avoid All Fields if it unintentionally transmits measure values or filters the target below wave scope. Verify two separate action names and target coverage rather than assuming one generated action does both.

Use the dashboard's Actions control if exposed by the current Public editor; inspect source/target settings there. Use as Filter can generate an action, but check its targets. If editing those settings is unavailable in that deployment, action configuration needs an authoring environment that supports it; do not promise a missing menu. Existing published interactions still run in the viewer. The [Filter Actions reference](https://help.tableau.com/current/pro/desktop/en-us/actions_filter.htm) explains source values, target mapping and the choices when a selection is cleared.

Proposed clearing behavior is Show all values; the published choice is **Q2, not verified**. A second action may leave another filter active. Test one source at a time, then sequential selections and resets. Reverse direction (B02 as source) does not make clicking B01 filter B02. A parameter change recomputes fields; an action changes the visible row population. Neither approves a source interpretation.

## Reconstruct in Tableau Public Web Authoring

Connect the specific CSV as its own source, set types before dragging, create only required calculated fields, then build the shelf/Marks recipe in each worksheet note. Configure tooltips with both value and unit, label scope and inspect filters. Assemble related sheets in tiled dashboard containers, then add actions and test their targets. Interface wording can vary; [web authoring guidance](https://help.tableau.com/current/pro/desktop/en-us/getstarted_web_authoring.htm) describes the shelves and Marks workflow. Viewer inspection in this task does not establish which menu sequence the original author used.
