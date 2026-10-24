#!/usr/bin/env python3
"""Export separate-grain Tableau CSVs; public subset uses an explicit allowlist."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path

from build_registry import DEFAULT_OUT as REGISTRY, digest, write_csv, write_json
from contract import ROOT, validate_registry

DEFAULT_OUT = ROOT / 'docs/data-quality/tableau'


def load_csv(name):
    with (REGISTRY / name).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def export(out):
    issues = json.loads((REGISTRY / 'issues.json').read_text())
    validate_registry(issues)
    registry_manifest = json.loads((REGISTRY / 'manifest.json').read_text())
    for name, expected in registry_manifest['outputs'].items():
        if digest(REGISTRY / name) != expected:
            raise ValueError('Registry fingerprint mismatch: ' + name)
    for name, expected in registry_manifest['source_hashes'].items():
        if digest(ROOT / 'data/raw' / name) != expected:
            raise ValueError('Raw source fingerprint mismatch: ' + name)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'internal').mkdir(exist_ok=True); (out / 'public').mkdir(exist_ok=True)
    by_id = {r['issue_id']: r for r in issues}
    table_specs = {}

    def common(issue_id, unit, evidence):
        r = by_id[issue_id]
        return {'issue_id': issue_id, 'category': r['category'], 'status': r['status'],
                'data_origin': r['data_origin'], 'unit': unit, 'evidence_ref': evidence}

    def emit(name, rows, pk, grain, measures, public=False):
        rows = list(rows)
        write_csv(out / 'internal', name + '.csv', rows)
        if public:
            write_csv(out / 'public', name + '.csv', rows)
        table_specs[name] = {'grain': grain, 'primary_key': pk, 'rows': len(rows),
                             'columns': list(rows[0]), 'measures': measures,
                             'public_eligible_subset': public,
                             'sha256': digest(out / 'internal' / (name + '.csv'))}

    summaries, metrics, sources, impacts = [], [], [], []
    for r in issues:
        key = r['issue_id']
        summaries.append({**common(key, 'investigation records', 'docs/data-quality/registry/issues.json#' + key),
                          'title': r['title'], 'severity': r['severity'], 'root_cause': r['root_cause'],
                          'arithmetic_confidence': r['confidence']['arithmetic'],
                          'interpretation_confidence': r['confidence']['interpretation'],
                          'review_state': r['review']['state'], 'reviewer': r['review']['reviewer'],
                          'review_evidence_ref': r['review']['evidence_ref'],
                          'treatment_kind': r['treatment']['kind'], 'approval_ref': r['treatment']['approval_ref'],
                          'before_ref': r['treatment']['before_ref'], 'after_ref': r['treatment']['after_ref'],
                          'detection_rule': r['detection_rule'], 'residual_uncertainty': r['residual_uncertainty'],
                          'business_decision_category': r['business_decision_category']})
        for m in r['metrics']:
            metrics.append({**common(key, m['unit'], 'docs/data-quality/registry/issues.json#' + key),
                            'metric_key': key + ':' + m['metric_id'], 'metric_id': m['metric_id'],
                            'affected_count': m['affected_count'], 'population': m['population'],
                            'denominator': m['denominator'], 'denominator_definition': m['denominator_definition'],
                            'calculation': m['calculation'], 'additivity': m['additivity'],
                            'cross_issue_sum_allowed': 'FALSE'})
        for i, line in enumerate(r['source_lineage'], 1):
            name = Path(line['source_file']).name
            sources.append({**common(key, 'source records', line['source_file']),
                            'issue_source_id': key + ':' + str(i), 'source_id': name,
                            'source_sha256': line['sha256'], 'lineage_role': line['role'],
                            'selected_record_count': sum(end - start + 1 for start,end in line['record_ranges']) if line['record_ranges'] else None,
                            'source_record_count': registry_manifest['source_record_counts'].get(name),
                            'source_count_definition': 'logical data records, header excluded; blank for non-CSV definition evidence',
                            'source_columns': '|'.join(line['columns']),
                            'record_range_count': len(line['record_ranges']),
                            'lineage_ref': 'docs/data-quality/registry/issues.json#' + key + '/source_lineage/' + str(i-1),
                            'count_rule': 'Contributing population is not necessarily affected; do not sum across issues or sources.'})
        impacts.append({**common(key, 'decision questions; monetary impact unmeasured', 'docs/data-quality/registry/issues.json#' + key),
                        'business_decision_category': r['business_decision_category'], 'business_decision': r['business_decision'],
                        'hypothesized_causes': ' | '.join(r['hypothesized_causes']),
                        'potential_consequences': ' | '.join(r['potential_consequences']),
                        'resolution_options': ' | '.join(r['resolution_options']),
                        'next_evidence_request': r['resolution_options'][-1],
                        'decision_readiness': 'SOURCE_CLARIFICATION_REQUIRED', 'measured_financial_impact': None,
                        'financial_unit': 'NOT_ESTIMATED', 'claim_limit': r['residual_uncertainty']})
    emit('issues', summaries, ['issue_id'], 'one aggregate investigation question', {}, public=True)
    emit('issue_metrics', metrics, ['metric_key'], 'one issue and metric with its own unit/population',
         {'affected_count': 'use only one metric_key at a time; never SUM across issues or metric IDs',
          'denominator': 'same-unit population total; use ATTR/MIN per metric_key, never sum duplicated populations'}, public=True)
    emit('issue_sources', sources, ['issue_source_id'], 'one issue/source lineage role selector',
         {'selected_record_count': 'exact selected ordinals; role may be contributing, not affected',
          'source_record_count': 'full source row count; do not sum repeated source totals'})
    emit('decision_impacts', impacts, ['issue_id'], 'one issue-to-decision question; no observed monetary outcome',
         {'measured_financial_impact': 'blank = unmeasured, never convert to zero'}, public=True)

    counts = []
    for name, n in sorted(registry_manifest['source_record_counts'].items()):
        counts.append({'source_id': name, 'category': 'SOURCE_POPULATION', 'status': 'PUBLISHED_SNAPSHOT_MEANING_UNVERIFIED',
                       'data_origin': 'REAL_SOURCE_DERIVED', 'unit': 'source records',
                       'source_record_count': n, 'denominator_definition': 'all logical data records in this CSV, header excluded',
                       'source_sha256': registry_manifest['source_hashes'][name], 'evidence_ref': 'data/raw/' + name})
    emit('source_counts', counts, ['source_id'], 'one pinned analytical source CSV',
         {'source_record_count': 'record counts may be summed only as records across files, never as unique entities/units'}, public=True)

    reconciliation = load_csv('reconciliation.csv')
    details = []
    for r in reconciliation:
        if int(r['gap_units']) <= 0: continue
        detail_id = hashlib.sha256(json.dumps([r['wave'],r['reference'],r['size']],separators=(',', ':')).encode()).hexdigest()
        details.append({**common('DQ-RECON-001','published customer/picking units','docs/data-quality/registry/reconciliation.csv'),
                        'reconciliation_id': detail_id, **r,
                        'denominator_scope': 'full demand denominator is in issue_metrics:gap_units; this table contains positive-gap keys only'})
    emit('reconciliation_detail', details, ['reconciliation_id'], 'one positive-gap wave/reference/inferred-size key',
         {'gap_units': 'SUM within this table = 13003; all keys disjoint',
          'customer_units': 'only contributing quantities at positive-gap keys, not total demand',
          'picking_units': 'only quantities at positive-gap keys', 'matched_units': 'only matched quantities at positive-gap keys'})

    from build_registry import read
    locations = {r['originalLocation'].strip() for r in read('Storage_Location')}
    location_rows = defaultdict(list)
    for i, r in enumerate(read('Picking_Wave'), 2):
        if r['locations'].strip() not in locations:
            location_rows[r['locations'].strip()].append((i, int(r['quantityToPick (units)'])))
    missing_locations = [{**common('DQ-LOC-001','published picking units','data/raw/Picking_Wave.csv'),
                          'location_id': loc, 'picking_units': sum(n for _,n in rows), 'picking_record_count': len(rows),
                          'source_selector': json.dumps({'file': 'data/raw/Picking_Wave.csv', 'stripped_locations_equals': loc}, separators=(',', ':')),
                          'denominator_scope': 'full picking quantity in issue_metrics:unmapped_picking_units'}
                         for loc,rows in sorted(location_rows.items())]
    emit('unmapped_locations', missing_locations, ['location_id'], 'one unmatched stripped picking location ID',
         {'picking_units': 'SUM = 23609; each picking record belongs to one location', 'picking_record_count': 'SUM unmatched source records'})
    classifications = [{**common('DQ-ABC-001','product references and published customer units','docs/data-quality/registry/classification.csv'),
                        **{k:v for k,v in r.items() if k != 'customer_rows'},
                        'lineage_ref': 'docs/data-quality/registry/classification.csv#reference=' + r['reference']} for r in load_csv('classification.csv')]
    emit('classification_detail', classifications, ['reference'], 'one demanded product reference, both classification bases',
         {'customer_units': 'SUM = 228195; disjoint references', 'disagrees': 'SUM = 96, denominator COUNTD reference = 208'})
    pairs = [{**common('DQ-EXP-001','SKU counters; L1 encoded cells','docs/data-quality/registry/policy_pairs.csv'),
              'policy_pair_id': r['policy_a'] + ':' + r['policy_b'], **r,
              'denominator_definition': 'union_skus is the reference/size-key union for this pair only',
              'additivity': 'NONADDITIVE_ACROSS_PAIRS'} for r in load_csv('policy_pairs.csv')]
    emit('policy_pairs', pairs, ['policy_pair_id'], 'one unordered pair of coordinate-retained published policies',
         {'differing_skus': 'one pair at a time, denominator union_skus',
          'l1_cell_difference': 'not unique affected stock or move count; never SUM across pairs'})

    # Reuse derived counters; no simulation or replenishment branch is run.
    demand = Counter()
    for r in reconciliation: demand[r['reference'],r['size']] += int(r['customer_units'])
    stock = defaultdict(Counter)
    for r in load_csv('policy_skus.csv'): stock[r['policy']][r['reference'],r['size']] = int(r['retained_encoded_cells'])
    excluded = Counter(r['policy'] for r in load_csv('excluded_cells.csv'))
    supply = []
    for policy,counts in sorted(stock.items()):
        supply.append({**common('DQ-EXP-001','assumed encoded-cell units; published requested units','docs/data-quality/registry/policy_skus.csv'),
                       'policy': policy, 'source_record_count': registry_manifest['source_record_counts'][policy+'_Storage.csv'],
                       'retained_encoded_cells': sum(counts.values()), 'excluded_cells': excluded[policy],
                       'raw_encoded_cells': sum(counts.values()) + excluded[policy],
                       'retained_size_skus': len(counts), 'conditional_supply_ceiling': sum(min(n,counts[k]) for k,n in demand.items()),
                       'demand_denominator_units': registry_manifest['totals']['customer_units'],
                       'denominator_definition': 'full customer units retaining repeats/zeros; 228195 per policy, never SUM across policies',
                       'interpretation': 'one cell assumed unit; finite undated snapshot, no receipts; arithmetic ceiling, not actual shortage or policy effect'})
    emit('policy_supply', supply, ['policy'], 'one published policy conditional finite-snapshot demand/supply arithmetic',
         {'conditional_supply_ceiling': 'SUM min(SKU demand, retained encoded cells) for one policy; do not sum alternatives',
          'retained_encoded_cells': 'assumed cells, not verified physical stock',
          'raw_encoded_cells': 'retained plus excluded cells', 'excluded_cells': 'coordinate exclusions by policy',
          'demand_denominator_units': 'full demand repeated per alternative policy; use ATTR/MIN'})
    write_json(out, 'manifest.json', {'tables': table_specs, 'registry_manifest_sha256': digest(REGISTRY / 'manifest.json'),
                                    'exporter_sha256': digest(Path(__file__)),
                                    'source_attribution': registry_manifest['source_doi'] + '; Rodrigo Furlan de Assis; CC BY 4.0',
                                    'null_encoding': 'empty field; unknown/unmeasured, not zero',
                                    'public_allowlist': [name+'.csv' for name,s in table_specs.items() if s['public_eligible_subset']],
                                    'publication_status': 'PREPARED_ONLY_REQUIRES_OWNER_REVIEW',
                                    'before_after_policy': 'no approved correction exists; all before/after references blank',
                                    'cross_issue_affected_total': 'UNDEFINED_OVERLAPPING_AND_INCOMPATIBLE_POPULATIONS'})
    return table_specs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args(); target = args.output_dir.resolve()
    if target != DEFAULT_OUT.resolve() and target.exists() and any(target.iterdir()):
        parser.error('Alternate output must be empty')
    if target == ROOT or any(target == ROOT/p or ROOT/p in target.parents for p in ('data','public','src','tests','scripts')):
        parser.error('Use an isolated research output directory')
    specs = export(target)
    print(json.dumps({'internal_tables': len(specs), 'public_tables': sum(s['public_eligible_subset'] for s in specs.values()),
                      'output': str(target), 'published': False}, indent=2))
