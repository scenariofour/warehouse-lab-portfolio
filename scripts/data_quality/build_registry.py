#!/usr/bin/env python3
"""Read-only raw-source profiling and issue registry. Python 3.10+ stdlib.

No production normalizer/simulator imports. Existing size assumptions are repeated
explicitly; no correction, deduplication or synthetic records enter the registry.
"""
import argparse
from collections import Counter, defaultdict
import csv
from decimal import Decimal
import hashlib
import itertools
import json
from pathlib import Path

from contract import ROOT, validate_registry

DEFAULT_OUT = ROOT / 'docs/data-quality/registry'
POLICIES = ('Random', 'Class_Based', 'Dedicated', 'Hybrid')
HALVES = {'35', '45', '55', '65', '75', '85', '95', '105', '115', '125'}
UNRESOLVED = 'Unresolved — Source Clarification Required'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    with (ROOT / f'data/raw/{name}.csv').open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=',' if name in ('Storage_Location', 'Random_Storage') else ';'))


def size(token, customer=False):
    token = token.strip()
    if not token:
        return ''
    n = Decimal(token) / (10 if customer and token in HALVES else 1)
    return format(n.normalize(), 'f')


def ranges(ordinals):
    result = []
    for i in sorted(set(ordinals)):
        if result and result[-1][1] + 1 == i:
            result[-1][1] = i
        else:
            result.append([i, i])
    return result


def write_csv(out, name, rows, fields=None):
    rows = list(rows)
    with (out / name).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields or list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)


def write_json(out, name, value):
    (out / name).write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n')


def build(out):
    manifest = json.loads((ROOT / 'data/manifest.json').read_text())
    hashes = {}
    for entry in manifest['files']:
        name = entry['filename']; hashes[name] = digest(ROOT / 'data/raw' / name)
        if hashes[name] != entry['content_details']['sha256_hash']:
            raise ValueError(f'Source hash mismatch: {name}')
    out.mkdir(parents=True, exist_ok=True)
    raw = {n: read(n) for n in ('Customer_Order', 'Picking_Wave', 'Product', 'Storage_Location',
                               'Support_Points_Navigation', *(p + '_Storage' for p in POLICIES))}
    clean = {n: [{k: v.strip() for k, v in r.items()} for r in rows] for n, rows in raw.items()}
    c, p = clean['Customer_Order'], clean['Picking_Wave']
    g = {r['originalLocation']: r for r in clean['Storage_Location']}
    products = {r['Reference']: (i, r) for i, r in enumerate(clean['Product'], 2)}
    dc, pc = Counter(), Counter()
    ci, pi, refs, ref_rows = defaultdict(list), defaultdict(list), Counter(), defaultdict(list)
    for i, r in enumerate(c, 2):
        key = r['waveNumber'], r['Reference'], size(r['Size (US)'], True)
        dc[key] += int(r['quantity (units)']); ci[key].append(i)
        refs[r['Reference']] += int(r['quantity (units)']); ref_rows[r['Reference']].append(i)
    for i, r in enumerate(p, 2):
        key = r['waveNumber'], r['reference'], size(r['Size (US)'])
        pc[key] += int(r['quantityToPick (units)']); pi[key].append(i)
    demand_units, picking_units = sum(dc.values()), sum(pc.values())
    reconciliation = []
    for k in sorted(dc.keys() | pc.keys()):
        reconciliation.append({'wave': k[0], 'reference': k[1], 'size': k[2],
                               'customer_units': dc[k], 'picking_units': pc[k],
                               'matched_units': min(dc[k], pc[k]), 'gap_units': dc[k] - pc[k],
                               'customer_rows': '|'.join(map(str, ci[k])), 'picking_rows': '|'.join(map(str, pi[k]))})
    write_csv(out, 'reconciliation.csv', reconciliation)
    gaps = [r for r in reconciliation if r['gap_units'] > 0]
    gap_keys = {(r['wave'], r['reference'], r['size']) for r in gaps}
    unmapped = [i for i, r in enumerate(p, 2) if r['locations'] not in g]
    missing = [i for i, r in enumerate(c, 2) if not r['Size (US)']]
    mapped = [i for i, r in enumerate(c, 2) if r['Size (US)'] in HALVES]
    zero = [i for i, r in enumerate(c, 2) if int(r['quantity (units)']) == 0]
    duplicate_rows = {}
    for name in ('Customer_Order', 'Picking_Wave'):
        seen, repeats = {}, []
        for i, row in enumerate(raw[name], 2):
            key = tuple(row.values())
            if key in seen:
                repeats.append((i, seen[key]))
            else:
                seen[key] = i
        duplicate_rows[name] = repeats
    abc, running = [], 0
    for ref, n in sorted(refs.items(), key=lambda item: (-item[1], item[0])):
        label = 'A' if running * 100 < 80 * demand_units else 'B' if running * 100 < 95 * demand_units else 'C'
        running += n
        abc.append({'reference': ref, 'customer_units': n, 'published_abc': products[ref][1]['ABCCOD'],
                    'derived_abc': label, 'disagrees': int(label != products[ref][1]['ABCCOD']),
                    'product_row': products[ref][0], 'customer_rows': '|'.join(map(str, ref_rows[ref]))})
    write_csv(out, 'classification.csv', abc)
    stocks, stock_rows, excluded, unknown = {}, {}, [], []
    total_cells = 0
    for policy in POLICIES:
        stock = Counter(); stock_rows[policy] = []
        for i, r in enumerate(clean[policy + '_Storage'], 2):
            loc = r.get('originalLocation', r.get('Location'))
            for col, token in r.items():
                if not (col.startswith('col_') or col.isdigit()) or not token:
                    continue
                total_cells += 1
                ref, s = token.split(';')
                cell = {'policy': policy, 'source_row': i, 'column': col, 'location': loc,
                        'reference': ref, 'token': s}
                if loc in g:
                    stock[ref, size(s)] += 1
                    stock_rows[policy].append(i)
                else:
                    excluded.append(cell)
                if ref not in products:
                    unknown.append(cell)
        stocks[policy] = stock
    write_csv(out, 'excluded_cells.csv', excluded)
    write_csv(out, 'unknown_reference_cells.csv', unknown)
    pairs = []
    for a, b in itertools.combinations(POLICIES, 2):
        keys = stocks[a].keys() | stocks[b].keys()
        pairs.append({'policy_a': a, 'policy_b': b, 'union_skus': len(keys),
                      'differing_skus': sum(stocks[a][k] != stocks[b][k] for k in keys),
                      'l1_cell_difference': sum(abs(stocks[a][k] - stocks[b][k]) for k in keys)})
    write_csv(out, 'policy_pairs.csv', pairs)
    write_csv(out, 'policy_skus.csv', [
        {'policy': policy, 'reference': k[0], 'size': k[1], 'retained_encoded_cells': n}
        for policy in POLICIES for k, n in sorted(stocks[policy].items())])

    def lineage(name, ids=None, columns=None, role='AFFECTED'):
        filename = name if '.' in name else name + '.csv'
        rows = [] if ids is None and filename not in {n + '.csv' for n in raw} else (
            range(2, len(raw[name]) + 2) if ids is None else ids)
        return {'source_file': 'data/raw/' + filename, 'sha256': hashes[filename],
                'record_ranges': ranges(rows), 'columns': columns or list(raw.get(name, [{}])[0]), 'role': role}

    def population(name):
        return lineage(name, role='CONTRIBUTING_POPULATION')

    def metric(key, n, unit, pop, d, definition, calc, additive='WITHIN_METRIC_ONLY'):
        return {'metric_id': key, 'affected_count': n, 'unit': unit, 'population': pop,
                'denominator': d, 'denominator_definition': definition, 'calculation': calc, 'additivity': additive}

    def issue(key, title, category, sources, metrics, rule, decision_category, decision, causes, consequences,
              uncertainty, options=None, severity='HIGH', status=UNRESOLVED, kind='RETENTION', interpretation='UNKNOWN'):
        return {'contract_version': '1.0', 'issue_id': 'DQ-' + key, 'title': title, 'category': category,
                'data_origin': 'REAL_SOURCE_DERIVED', 'source_lineage': sources, 'detection_rule': rule,
                'metrics': metrics, 'severity': severity,
                'confidence': {'arithmetic': 'HIGH' if any(m['affected_count'] is not None for m in metrics) else 'NOT_APPLICABLE',
                               'interpretation': interpretation, 'rationale': 'Raw-file arithmetic is reproducible; semantic cause and operational effect are not independently validated.'},
                'root_cause': 'UNKNOWN', 'hypothesized_causes': causes,
                'business_decision_category': decision_category, 'business_decision': decision,
                'potential_consequences': consequences,
                'resolution_options': options or ['Retain current interpretation and disclose uncertainty', 'Obtain authoritative source definitions before a separately approved treatment'],
                'status': status, 'review': {'state': 'PENDING', 'reviewer': None, 'evidence_ref': None},
                'evidence_refs': ['docs/data-quality/registry/manifest.json', 'docs/data-quality/CONTRACT.md'],
                'residual_uncertainty': uncertainty,
                'treatment': {'kind': kind, 'approval_ref': None, 'before_ref': None, 'after_ref': None,
                              'description': 'Preserve raw records and existing interpretation; no approved correction or successful resolution.'}}

    issues = []
    issues.append(issue('RECON-001', 'Demand/picking quantity reconciliation gap', 'RECONCILIATION',
        [lineage('Customer_Order', [i for k in gap_keys for i in ci[k]], role='CONTRIBUTING_POPULATION'),
         lineage('Picking_Wave', [i for k in gap_keys for i in pi[k]], role='CONTRIBUTING_POPULATION')],
        [metric('gap_units', sum(r['gap_units'] for r in gaps), 'published customer units', 'full customer demand', demand_units,
                'SUM Customer_Order.quantity (units), including zeros and repeats', 'SUM MAX(customer_qty - picking_qty,0) over wave/reference/inferred-size keys'),
         metric('positive_gap_keys', len(gaps), 'wave/reference/inferred-size keys', 'customer reconciliation keys', len(dc),
                'distinct customer wave/reference/inferred-size keys', 'COUNT keys with positive gap')],
        'Aggregate each file first by wave/reference/existing inferred size; never multiply quantities through a row join.',
        'MEASUREMENT_BASELINE', 'Define eligible requested work before diagnosing fulfillment.',
        ['Cancellation or backlog', 'Extract timing/scope', 'Size encoding or missing master data'],
        ['A false service-failure baseline could misdirect a capacity or slotting study.'],
        'No transaction status, cancellation history or timing alignment proves the gap is failed warehouse service.'))
    issues[-1]['evidence_refs'].append('docs/data-quality/registry/reconciliation.csv')
    issues.append(issue('LOC-001', 'Picking locations lack matched coordinates', 'LOCATION',
        [lineage('Picking_Wave', unmapped), population('Storage_Location')],
        [metric('unmapped_picking_units', sum(int(p[i-2]['quantityToPick (units)']) for i in unmapped), 'published picking units',
                'full picking extract', picking_units, 'SUM Picking_Wave.quantityToPick (units), retaining repeats',
                'SUM quantities where stripped locations has no coordinate key')],
        'LEFT JOIN stripped picking locations to Storage_Location.originalLocation; retain unmatched.',
        'SPATIAL_FEASIBILITY', 'Establish spatial coverage before a route or travel claim.',
        ['Non-storage process locations', 'Different extract coverage', 'Incomplete location master'],
        ['Excluding unmatched units can bias a spatial workload estimate.'],
        'Unmatched coordinates do not prove invalid locations, lost units or inaccessible physical stock.'))
    disagreed = [r for r in abc if r['disagrees']]
    issues.append(issue('ABC-001', 'Published versus extract-volume ABC disagreement', 'CLASSIFICATION',
        [lineage('Product', [r['product_row'] for r in disagreed]), population('Customer_Order')],
        [metric('disagreeing_references', len(disagreed), 'product references', 'demanded product references', len(refs),
                'distinct references in full customer extract', 'COUNT reference where published ABC != derived volume ABC')],
        'Rank SUM customer units descending, reference ascending for ties; classify using cumulative share BEFORE reference: <80% A, <95% B, else C.',
        'SLOTTING_HYPOTHESIS', 'Confirm classification objective before choosing fast movers.',
        ['ABC based on value/margin', 'Different effective period', 'Anonymization'],
        ['Published classes could select a different study population than unit velocity.'],
        'Neither classification is an approved replacement for the other.'))
    issues[-1]['evidence_refs'].append('docs/data-quality/registry/classification.csv')
    issues.append(issue('EXP-001', 'Unequal SKU inventory across published storage policies', 'EXPERIMENT_CONFOUNDER',
        [lineage(policy + '_Storage', stock_rows[policy], role='CONTRIBUTING_POPULATION') for policy in POLICIES] + [population('Storage_Location')],
        [metric('unequal_policy_pairs', sum(r['differing_skus'] > 0 for r in pairs), 'policy pairs', 'all unordered pairs of four published policies',
                len(pairs), '4 choose 2 = 6 pairs', 'COUNT pairs with any retained SKU-counter difference', 'NONADDITIVE')],
        'Count nonempty coordinate-retained cells by reference/numeric size per policy under one-cell assumption; compare all six pairs.',
        'EXPERIMENT_DESIGN', 'Defer a causal policy ranking until common SKU quantities and eligible work are approved.',
        ['Different SKU composition', 'Published allocation construction', 'Unequal coordinate exclusions'],
        ['Apparent efficiency can reflect availability and task mix instead of placement.'],
        'Encoded cells are assumed stock units; L1 differences are not observed losses or relocation counts.'))
    issues[-1]['evidence_refs'] += ['docs/data-quality/registry/policy_pairs.csv', 'docs/data-quality/registry/policy_skus.csv']
    definitions = [lineage('README.txt', columns=['allocation payload and coordinate definitions'], role='DEFINITION_EVIDENCE')]
    issues.append(issue('STOCK-001', 'Stock payload units and snapshot alignment unresolved', 'INVENTORY_SNAPSHOT',
        [population(policy + '_Storage') for policy in POLICIES] + definitions,
        [metric('verified_physical_stock', None, 'verified physical inventory units', 'aligned source inventory snapshot', None,
                'UNKNOWN: no verified snapshot date/UOM or inventory trajectory', 'Not measurable from allocation-cell counts', 'NONADDITIVE')],
        'README quantity wording conflicts with size-like tokens; neither snapshot timing nor carton/unit equivalence is established.',
        'SOURCE_DEFINITION', 'Obtain quantity/UOM and stock-date definitions before availability or replenishment conclusions.',
        ['Size-like allocation payload', 'Unknown snapshot date', 'Unknown carton/unit meaning'],
        ['Unverified stock arithmetic could be misreported as real stockouts.'],
        'Existing one-cell-one-assumed-unit and token-as-size rules are retained, not confirmed.'))
    issues.append(issue('LAYOUT-001', 'Physical scale and floor connectivity unresolved', 'LOCATION',
        [population('Storage_Location'), population('Support_Points_Navigation')] + definitions +
        [lineage('Order_Picking_dataset.ipynb', columns=['floor and block conventions'], role='DEFINITION_EVIDENCE')],
        [metric('verified_physical_distance', None, 'verified physical meters', 'surveyed traversable layout', None,
                'UNKNOWN: surveyed scale and traversable inter-floor graph absent', 'Cannot infer physical travel from renderer calibration', 'NONADDITIVE')],
        'Published coordinate unit wording and notebook floor conventions do not validate the renderer scale/tier abstraction.',
        'SPATIAL_FEASIBILITY', 'Obtain surveyed scale, origins and floor connectivity before route/capacity claims.',
        ['Coordinate-scale convention', 'Separate physical floors', 'Unrecorded transfer/access rules'],
        ['Travel, safety and capacity inferences could rely on an invalid topology.'],
        'Source units remain source units; no floor transfer, path or physical metric is repaired.'))
    for name, suffix, qty in [('Customer_Order', 'CUSTOMER', 'quantity (units)'), ('Picking_Wave', 'PICKING', 'quantityToPick (units)')]:
        repeats = duplicate_rows[name]; n = len(raw[name]); repeated_ids = [i for i, _ in repeats]
        issues.append(issue('DUP-' + suffix, f'Exact repeated {name} records retained', 'DUPLICATE',
            [lineage(name, repeated_ids), lineage(name, [first for _, first in repeats], role='CONTRIBUTING_POPULATION')],
            [metric('repeat_rows', len(repeats), 'source records', name + ' full extract', n, 'all logical data records, excluding header',
                    'COUNT occurrences after first of identical complete original field tuple'),
             metric('repeat_units', sum(int(clean[name][i-2][qty]) for i in repeated_ids), 'published ' + ('customer' if suffix == 'CUSTOMER' else 'picking') + ' units',
                    name + ' full quantity extract', sum(int(r[qty]) for r in clean[name]), 'SUM published quantities retaining repeats',
                    'SUM quantity on repeated occurrences after first')],
            'Compare full untrimmed raw tuples, preserve all primary-analysis records; do not deduplicate.',
            'MEASUREMENT_BASELINE', 'Clarify transaction granularity before any deletion.',
            ['Legitimate repeated lines', 'One-unit picking expansion', 'Extract duplication'],
            ['Deduplication can remove legitimate requested or picking work.'],
            'Row equality is confirmed; duplicate transaction identity and deletion eligibility remain unknown.', severity='MEDIUM'))
    issues.append(issue('SIZE-001', 'Existing inferred customer half-size mapping', 'SKU_SIZE',
        [lineage('Customer_Order', mapped), population('Picking_Wave')],
        [metric('mapped_rows', len(mapped), 'customer source records', 'full customer extract', len(c), 'all Customer_Order data records',
                'COUNT exact stripped size tokens in {35,45,55,65,75,85,95,105,115,125}')],
        'Apply only established exact-token customer mapping to /10; retain all other tokens and original source.',
        'SOURCE_DEFINITION', 'Seek source size dictionary before treating matching as authenticated.',
        ['Implied decimal in customer encoding', 'Other size-system meaning'],
        ['Key matching and availability depend on this inferred representation.'],
        'Better matching supports an inference; it is not source confirmation.', kind='NORMALIZATION', severity='HIGH'))
    issues.append(issue('SIZE-002', 'Missing customer sizes retained', 'SKU_SIZE', [lineage('Customer_Order', missing)],
        [metric('missing_size_units', sum(int(c[i-2]['quantity (units)']) for i in missing), 'published customer units',
                'full customer demand', demand_units, 'SUM full customer quantities', 'SUM quantities on blank-size records'),
         metric('missing_size_rows', len(missing), 'customer source records', 'full customer extract', len(c),
                'all Customer_Order data records', 'COUNT blank stripped Size (US)')],
        'Blank stripped size stays empty; never impute or discard.', 'SOURCE_DEFINITION', 'Clarify SKU identity for eligibility.',
        ['Omitted value', 'Source-specific unspecified size'], ['Imputation could assign demand to the wrong SKU.'],
        'Missing size semantics and fulfillment eligibility are unknown.', severity='MEDIUM'))
    issues.append(issue('QTY-001', 'Zero-quantity customer records retained', 'RECONCILIATION', [lineage('Customer_Order', zero)],
        [metric('zero_quantity_rows', len(zero), 'customer source records', 'full customer extract', len(c), 'all customer data records',
                'COUNT quantity (units) = 0')], 'Profile integer quantity without removing zeros.',
        'MEASUREMENT_BASELINE', 'Define eligible lines and group denominators.', ['Canceled line', 'Placeholder', 'Extract convention'],
        ['Line and group counts can differ from positive-work counts.'], 'Zero does not establish cancellation or error.', severity='LOW'))
    issues.append(issue('LOC-002', 'Allocation cells excluded from geometry-dependent analysis', 'LOCATION',
        [lineage(policy + '_Storage', [r['source_row'] for r in excluded if r['policy'] == policy], role='CONTRIBUTING_POPULATION')
         for policy in POLICIES if any(r['policy'] == policy for r in excluded)] + [population('Storage_Location')],
        [metric('excluded_cells', len(excluded), 'encoded allocation cells', 'nonempty cells across four raw policies',
                total_cells, 'all nonempty numbered cells across four published allocations',
                'COUNT nonempty cells with no coordinate match', 'NONADDITIVE')],
        'Keep raw cells; exclude only from explicitly geometry-retained counters. Cell selectors are in excluded_cells.csv.',
        'EXPERIMENT_DESIGN', 'Clarify location master coverage before comparing eligible placements.',
        ['Different location master version', 'Locations outside coordinate scope'],
        ['Policy exclusions differ and can bias comparison populations.'], 'No invented location or actual physical inaccessibility claim.'))
    issues[-1]['evidence_refs'].append('docs/data-quality/registry/excluded_cells.csv')
    issues.append(issue('MASTER-001', 'Allocation references absent from published product master', 'IDENTIFIER',
        [lineage(policy + '_Storage', [r['source_row'] for r in unknown if r['policy'] == policy], role='CONTRIBUTING_POPULATION')
         for policy in POLICIES if any(r['policy'] == policy for r in unknown)] + [population('Product')],
        [metric('unknown_reference_cells', len(unknown), 'encoded allocation cells', 'nonempty cells across four raw policies',
                total_cells, 'all nonempty numbered cells across four raw policies',
                'COUNT cells where reference absent from Product.Reference', 'NONADDITIVE')],
        'LEFT JOIN cell reference to Product.Reference; no unknown label is silently corrected.',
        'SOURCE_DEFINITION', 'Confirm active assortment/master coverage.', ['Different master scope', 'Allocation construction or anonymization'],
        ['Unmatched assortment can distort eligible stock and ABC interpretation.'], 'Absence from master does not prove an invalid SKU.'))
    issues[-1]['evidence_refs'].append('docs/data-quality/registry/unknown_reference_cells.csv')
    by_order = defaultdict(set)
    for r in c:
        by_order[r['orderNumber']].add(r['waveNumber'])
    repeated_orders = {order for order, waves in by_order.items() if len(waves) > 1}
    issues.append(issue('ID-001', 'Order numbers reused across waves; business identity unresolved', 'IDENTIFIER',
        [lineage('Customer_Order', [i for i, r in enumerate(c, 2) if r['orderNumber'] in repeated_orders])],
        [metric('multi_wave_order_numbers', len(repeated_orders), 'distinct order numbers', 'full customer order-number domain',
                len(by_order), 'COUNT distinct Customer_Order.orderNumber', 'COUNT order numbers with more than one distinct wave')],
        'Engine grouping remains waveNumber + orderNumber; profile orderNumber reuse, do not call reuse an invalid ID.',
        'MEASUREMENT_BASELINE', 'Agree customer service identity and throughput denominator.',
        ['Legitimate split waves', 'Order-number scope convention'], ['Wave/order throughput may differ from customer-order throughput.'],
        'Business completeness across waves is undefined.'))

    # Supplemental zero/nonzero profile checks are evidence, never invented issues.
    profiles = []
    for name, fields in [('Customer_Order', ['waveNumber', 'orderNumber', 'Reference']),
                         ('Picking_Wave', ['waveNumber', 'reference', 'locations']),
                         ('Product', ['Reference']), ('Storage_Location', ['originalLocation'])]:
        for field in fields:
            profiles.append({'source': name + '.csv', 'check': 'blank_identifier', 'field': field,
                             'affected_rows': sum(not r[field] for r in clean[name]), 'population_rows': len(clean[name])})
    for name, field in [('Product', 'Reference'), ('Storage_Location', 'originalLocation')]:
        profiles.append({'source': name + '.csv', 'check': 'duplicate_master_id_after_first', 'field': field,
                         'affected_rows': len(clean[name]) - len({r[field] for r in clean[name]}), 'population_rows': len(clean[name])})
    for name, field in [('Customer_Order', 'quantity (units)'), ('Picking_Wave', 'quantityToPick (units)')]:
        profiles.append({'source': name + '.csv', 'check': 'negative_quantity', 'field': field,
                         'affected_rows': sum(int(r[field]) < 0 for r in clean[name]), 'population_rows': len(clean[name])})
    write_csv(out, 'profile_checks.csv', profiles)
    validate_registry(issues)
    write_json(out, 'issues.json', issues)
    write_json(out, 'manifest.json', {
        'contract_version': '1.0', 'data_origin': 'REAL_SOURCE_DERIVED', 'source_doi': '10.17632/pf2w725pw3.1',
        'author': 'Rodrigo Furlan de Assis', 'license': 'CC BY 4.0', 'source_hashes': hashes,
        'code_hashes': {str(path.relative_to(ROOT)): digest(path) for path in [Path(__file__), Path(__file__).with_name('contract.py')]},
        'source_record_counts': {name + '.csv': len(rows) for name, rows in raw.items()},
        'totals': {'customer_units': demand_units, 'picking_units': picking_units,
                   'matched_units': sum(min(dc[k], pc[k]) for k in dc),
                   'gap_units': sum(max(dc[k]-pc[k], 0) for k in dc),
                   'picking_excess_units': sum(max(pc[k]-dc[k], 0) for k in pc)},
        'normalization': 'Exact existing customer half-token mapping; Decimal numeric spelling; whitespace joins; raw tuples for repeats; zero/repeat records retained.',
        'assumptions': ['Allocation token interpreted as size and one cell as assumed unit, not verified stock.',
                        'Source row is logical CSV ordinal, header=1.', 'No synthetic or simulation input; no correction or closure.'],
        'outputs': {path.name: digest(path) for path in sorted(out.glob('*.csv'))} | {'issues.json': digest(out / 'issues.json')},
    })
    return issues


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    target = args.output_dir.resolve()
    if target != DEFAULT_OUT.resolve() and (target.exists() and any(target.iterdir())):
        parser.error('Alternate output must be empty')
    if target == ROOT or any(target == ROOT/p or ROOT/p in target.parents for p in ('data', 'public', 'src', 'tests', 'scripts')):
        parser.error('Use an isolated research output directory')
    result = build(target)
    print(json.dumps({'issues': len(result), 'output': str(target), 'synthetic_records': 0}, indent=2))
