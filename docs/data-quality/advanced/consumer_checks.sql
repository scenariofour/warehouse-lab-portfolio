-- Executed by verify_advanced.py against independently loaded public CSV tables.
-- Each row is check_name, actual, expected. All actual values must equal expected.
SELECT 'current customer units', SUM(current_customer_units), 228195 FROM out_reconciliation
UNION ALL SELECT 'picking units', SUM(picking_units), 215192 FROM out_reconciliation
UNION ALL SELECT 'current matched units', SUM(MIN(current_customer_units,picking_units)), 215192 FROM out_reconciliation
UNION ALL SELECT 'current positive gap', SUM(MAX(current_customer_units-picking_units,0)), 13003 FROM out_reconciliation
UNION ALL SELECT 'current picking excess', SUM(MAX(picking_units-current_customer_units,0)), 0 FROM out_reconciliation
UNION ALL SELECT 'literal matched units', SUM(MIN(literal_customer_units,picking_units)), 149514 FROM out_reconciliation
UNION ALL SELECT 'dedup matched units', SUM(MIN(dedup_customer_units,picking_units)), 202475 FROM out_reconciliation
UNION ALL SELECT 'dedup positive gap', SUM(MAX(dedup_customer_units-picking_units,0)), 12985 FROM out_reconciliation
UNION ALL SELECT 'dedup picking excess', SUM(MAX(picking_units-dedup_customer_units,0)), 12717 FROM out_reconciliation
UNION ALL SELECT 'current positive-gap keys', COUNT(*), 5242 FROM out_reconciliation WHERE current_customer_units>picking_units
UNION ALL SELECT 'current customer-key presence', COUNT(*), 112442 FROM out_reconciliation WHERE current_customer_records>0
UNION ALL SELECT 'picking-key presence', COUNT(*), 107283 FROM out_reconciliation WHERE picking_records>0
UNION ALL SELECT 'order groups', COUNT(*), 39858 FROM out_order_groups
UNION ALL SELECT 'order numbers', COUNT(DISTINCT order_id), 32634 FROM out_order_groups
UNION ALL SELECT 'multiwave order numbers', COUNT(DISTINCT order_id), 4024 FROM out_order_groups WHERE order_wave_count>1
UNION ALL SELECT 'order-group source records', SUM(source_records), 122370 FROM out_order_groups
UNION ALL SELECT 'order-group demand', SUM(customer_units), 228195 FROM out_order_groups
UNION ALL SELECT 'customer repeat occurrences', SUM(repeat_records), 2559 FROM out_order_groups
UNION ALL SELECT 'missing size records', SUM(missing_size_records), 16 FROM out_order_groups
UNION ALL SELECT 'zero quantity records', SUM(zero_quantity_records), 33 FROM out_order_groups
UNION ALL SELECT 'unmapped picking units', SUM(quantity), 23609 FROM out_location_coverage WHERE source_scope='Picking_Wave' AND mapped=0
UNION ALL SELECT 'unmapped picking locations', COUNT(*), 22 FROM out_location_coverage WHERE source_scope='Picking_Wave' AND mapped=0
UNION ALL SELECT 'all raw allocation cells', SUM(quantity), 167634 FROM out_location_coverage WHERE source_scope<>'Picking_Wave'
UNION ALL SELECT 'all excluded allocation cells', SUM(quantity), 2610 FROM out_location_coverage WHERE source_scope<>'Picking_Wave' AND mapped=0
UNION ALL SELECT 'all unknown master cells', SUM(unknown_reference_cells), 6734 FROM out_location_coverage
UNION ALL SELECT 'ABC references', COUNT(*), 208 FROM out_abc_comparison
UNION ALL SELECT 'ABC disagreements', SUM(disagrees), 96 FROM out_abc_comparison
UNION ALL SELECT 'ABC demand', SUM(customer_units), 228195 FROM out_abc_comparison
UNION ALL SELECT 'published A demand', SUM(customer_units), 89593 FROM out_abc_comparison WHERE published_abc='A'
UNION ALL SELECT 'derived A demand', SUM(customer_units), 183619 FROM out_abc_comparison WHERE derived_abc='A'
UNION ALL SELECT 'half-size mapped records', SUM(token_records), 38846 FROM out_normalization_tokens WHERE rule_id='HALF_SIZE'
UNION ALL SELECT 'wave Pareto gap population', SUM(gap_units), 13003 FROM out_exception_pareto WHERE dimension='wave'
UNION ALL SELECT 'reference Pareto gap population', SUM(gap_units), 13003 FROM out_exception_pareto WHERE dimension='reference'
UNION ALL SELECT 'unequal policy pairs', COUNT(*), 6 FROM out_policy_pairs WHERE differing_skus>0
UNION ALL SELECT 'failed controls', COUNT(*), 7 FROM out_experiment_controls WHERE result='FAIL'
UNION ALL SELECT 'pending issue reviews', COUNT(*), 14 FROM out_decision_evidence WHERE review_state='PENDING';
