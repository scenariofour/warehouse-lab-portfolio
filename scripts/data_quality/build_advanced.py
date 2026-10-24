#!/usr/bin/env python3
"""M4-B offline public research exports. No production writes or simulation."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path

from build_registry import DEFAULT_OUT as REGISTRY, POLICIES, HALVES, read, size, digest
from contract import ROOT, validate_registry

DEFAULT_OUT = ROOT / 'docs/data-quality/advanced'
M3 = ROOT / 'docs/data-quality/tableau'
MISSING = 'MISSING'


def opaque(domain, *parts):
    payload = json.dumps([domain, *parts], ensure_ascii=False, separators=(',', ':'))
    return domain + '_' + hashlib.sha256(payload.encode()).hexdigest()[:20]


def load(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def authenticate():
    """Fail closed on changed source, registry, M3 extract or definition code."""
    inputs = {}
    for folder in (REGISTRY, M3):
        m = json.loads((folder / 'manifest.json').read_text())
        pins = {ROOT / p: h for p, h in m.get('code_hashes', {}).items()}
        if folder == REGISTRY:
            pins.update({folder / p: h for p, h in m['outputs'].items()})
            pins.update({ROOT / 'data/raw' / p: h for p, h in m['source_hashes'].items()})
        else:
            pins.update({folder / 'internal' / (p + '.csv'): t['sha256'] for p, t in m['tables'].items()})
            assert digest(REGISTRY / 'manifest.json') == m['registry_manifest_sha256']
        pins[folder / 'manifest.json'] = digest(folder / 'manifest.json')
        for path, expected in pins.items():
            if digest(path) != expected:
                raise ValueError('Pinned input changed: ' + str(path.relative_to(ROOT)))
            inputs[str(path.relative_to(ROOT))] = expected
    return inputs


# Each public field has an explicit type, nullability and aggregation contract.
# Shared definitions are reused only where units and meaning really agree.
FIELDS = {}


def fields(names, kind, definition, aggregation='DIMENSION', nullable=False):
    for name in names.split():
        FIELDS[name] = dict(type=kind, nullable=nullable, definition=definition, aggregation=aggregation)


fields('wave_id reference_id location_id order_id order_group_id reconciliation_id token_id member_id', 'string',
       'Stable domain-separated SHA-256 pseudonym (20 hex digits). String dimension; not proof of anonymization.')
fields('size_key', 'string', 'Numeric size spelling or MISSING; declared key under each interpretation, never a physical quantity.')
fields('current_customer_units', 'integer', 'Customer quantity at key under existing inferred size mapping; zeros/repeats retained.', 'SUM_WITHIN_SELECTED_KEYS')
fields('literal_customer_units', 'integer', 'Customer quantity at key with numeric spelling only and no half-token inference; analytical sensitivity.', 'SUM_WITHIN_SELECTED_KEYS')
fields('dedup_customer_units', 'integer', 'Customer quantity after keeping first complete original tuple under current size mapping; analytical sensitivity, not approved removal.', 'SUM_WITHIN_SELECTED_KEYS')
fields('picking_units', 'integer', 'Published picking quantity at this key/location, all repeat occurrences retained.', 'SUM_WITHIN_ONE_GRAIN')
fields('current_customer_records literal_customer_records dedup_customer_records picking_records', 'integer',
       'Contributing source-record count for named branch, including zero quantities. Presence is count > 0.', 'SUM_WITHIN_SELECTED_KEYS')
fields('interpretation', 'string', 'CURRENT_INFERRED (established but unconfirmed), LITERAL_SIZE or CUSTOMER_DEDUP (sensitivity only). Select one.')
fields('evidence_class', 'string', 'Provenance/interpretation label; does not establish source truth, cause or operational effect.')
fields('customer_units', 'integer', 'Sum of published customer quantities in the declared group or interpretation.', 'SUM_WITHIN_ONE_GRAIN')
fields('matched_units', 'integer', 'Sum of key-level min(customer,picking), for one interpretation.', 'SUM_WITHIN_ONE_INTERPRETATION')
fields('gap_units', 'integer', 'Sum of key-level max(customer-picking,0); unmatched quantity, not observed failed service.', 'SUM_WITHIN_ONE_DIMENSION_OR_INTERPRETATION')
fields('excess_units', 'integer', 'Sum of key-level max(picking-customer,0); not observed over-picking.', 'SUM_WITHIN_ONE_INTERPRETATION')
fields('customer_keys picking_keys union_keys positive_gap_keys', 'integer', 'Count of keys with source records (or positive gap for positive_gap_keys), not quantity.', 'ONE_INTERPRETATION_ONLY')
fields('dimension', 'string', 'wave or reference; each is an alternative grouping of the same positive-gap units.')
fields('rank', 'integer', 'One-based descending quantity rank; original source key ascending breaks ties.', 'DO_NOT_SUM')
fields('cumulative_gap_units', 'integer', 'Full-extract cumulative positive gap in fixed rank order, not recalculated after filters.', 'ATTR_OR_MIN_PER_MEMBER')
fields('gap_denominator_units', 'integer', 'Full current positive-gap population (13003), repeated per group. Not customer-demand denominator.', 'MIN_NEVER_SUM')
fields('source_records', 'integer', 'Contributing records in the wave/order group, including zeros and repeats.', 'SUM_WITHIN_ORDER_GROUPS')
fields('distinct_references distinct_size_skus', 'integer', 'Distinct members within a group; counts overlap between groups.', 'DO_NOT_SUM')
fields('repeat_records', 'integer', 'Complete original tuple occurrences after first in source; retained in current calculations.', 'SUM_WITHIN_ORDER_GROUPS')
fields('missing_size_records zero_quantity_records', 'integer', 'Source records satisfying named check in the group; checks can overlap.', 'SUM_SEPARATELY')
fields('order_wave_count', 'integer', 'Distinct source waves for this order pseudonym; repeated per wave/order group.', 'MIN_PER_ORDER_NEVER_SUM')
fields('source_scope source_id field check', 'string', 'Pinned source filename (without personal data), original field name or exact profile check name.')
fields('mapped', 'integer', '1 iff stripped location joins Storage_Location; 0 means unmatched, not physically invalid.', 'DIMENSION')
fields('quantity', 'integer', 'Picking units for Picking_Wave, nonempty encoded cells for allocation files; consult unit.', 'SUM_WITHIN_SOURCE_SCOPE')
fields('records', 'integer', 'Source records contributing to location; for allocation each row counted once, not once per cell.', 'SUM_WITHIN_SOURCE_SCOPE')
fields('unit', 'string', 'published picking units or encoded allocation cells; populations cannot be mixed.')
fields('scope_denominator', 'integer', 'Full same-source quantity (picking units or all raw nonempty allocation cells), repeated per location.', 'MIN_WITHIN_SOURCE_SCOPE')
fields('unknown_reference_cells', 'integer', 'Nonempty allocation cells absent from Product.Reference; may overlap unmapped cells.', 'SUM_WITHIN_SOURCE_SCOPE')
fields('published_abc', 'string', 'Product.ABCCOD as published; basis and effective date unverified.')
fields('derived_abc', 'string', 'Extract-volume 80/95 ABC using cumulative share BEFORE each reference; ties by original reference ascending.')
fields('disagrees', 'integer', '1 if published and derived ABC differ; not a confirmed source error.', 'SUM_WITHIN_REFERENCES')
fields('cumulative_customer_units', 'integer', 'Fixed full-extract demand cumulative through ranked reference; never sum.', 'ATTR_OR_MIN_PER_REFERENCE')
fields('demand_denominator_units', 'integer', 'Full customer demand (228195) repeated per alternative/reference; use MIN, never SUM.', 'MIN_NEVER_SUM')
fields('original_token', 'string', 'Exact source size spelling, including whitespace; blank means original missing size.', nullable=True)
fields('current_value', 'string', 'Existing trimmed Decimal numeric spelling, with customer half-token inference; blank stays unknown.', nullable=True)
fields('alternative_value', 'string', 'Literal trimmed Decimal spelling; alternative interpretation, not a correction.', nullable=True)
fields('token_records', 'integer', 'Records with exactly this original token in this source.', 'SUM_WITHIN_SOURCE')
fields('token_units', 'integer', 'Published quantity on records with exactly this original token.', 'SUM_WITHIN_SOURCE')
fields('rule_id', 'string', 'Declared rule identifier. A token uses its governing size rule; foundational parse/trim rules also apply.')
fields('rule_kind approval_state description affected_calculations', 'string', 'Declared normalization, retention or sensitivity and its semantic approval boundary; no source correction approval.')
fields('policy policy_a policy_b policy_pair_id', 'string', 'Published configuration name or unordered pair. Alternative configurations are not additive.')
fields('union_skus', 'integer', 'Union of coordinate-retained reference/size keys in this pair.', 'ONE_PAIR_ONLY')
fields('differing_skus', 'integer', 'Pair keys with unequal encoded-cell counts; denominator union_skus.', 'ONE_PAIR_ONLY')
fields('l1_cell_difference', 'integer', 'Sum of absolute pair SKU-counter differences; not required moves, stock loss or unique units.', 'ONE_PAIR_ONLY')
fields('raw_encoded_cells', 'integer', 'Nonempty numbered allocation cells before coordinate exclusion.', 'ONE_POLICY_ONLY')
fields('retained_encoded_cells', 'integer', 'Nonempty cells with joined coordinate IDs; each assumed one unit, physical stock unverified.', 'ONE_POLICY_ONLY')
fields('excluded_cells', 'integer', 'Nonempty cells without joined coordinate IDs; preserved in source.', 'ONE_POLICY_ONLY')
fields('conditional_supply_ceiling', 'integer', 'Existing M3 sum min(full-history SKU demand, retained encoded-cell count); one undated snapshot/no receipts assumption.', 'ONE_POLICY_ONLY')
fields('control_id scope control_name result observation required_evidence', 'string', 'Control identity/scope, explicit state and evidence needed. PASS_DESCRIPTIVE is not experiment approval.')
fields('issue_id title status review_state severity', 'string', 'Unmodified issue registry ID/title/workflow/review/proposed decision-priority; not measured business severity.')
fields('decision_category business_decision kpi_at_risk business_mechanism competing_explanations evidence_readiness recommendation next_evidence_request', 'string', 'AI-proposed decision interpretation anchored in issue evidence; unmeasured effects and human review remain explicit.')
fields('issue_source_id lineage_role source_sha256 evidence_ref', 'string', 'Registry lineage identity/role/hash/path. Hash authenticates bytes; contributing populations are not affected counts.')
fields('selected_record_count', 'integer', 'Exact selected source ordinals from registry role; not automatically affected records; blank for definition evidence.', 'DO_NOT_SUM_ACROSS_ISSUES', True)
fields('source_record_count', 'integer', 'All logical records in named source CSV; repeated per evidence relationship; blank for non-CSV definitions.', 'MIN_PER_SOURCE', True)
fields('affected_rows', 'integer', 'Source rows flagged by the named completed check; checks may overlap.', 'ONE_CHECK_ONLY')
fields('population_rows', 'integer', 'Full named source record denominator; repeated across checks.', 'MIN_PER_SOURCE')


DECISIONS = {
    'DQ-RECON-001': ('Eligible requested-work / service numerator', 'A mismatched baseline can misattribute extract differences to capacity or slotting.', 'One wave with line statuses, cancellations and aligned extraction times.'),
    'DQ-LOC-001': ('Spatial workload coverage', 'Dropping unmapped workload can bias a travel estimate.', 'Location-master record and process meaning for the largest unmatched location pseudonym.'),
    'DQ-ABC-001': ('Fast-mover study population', 'Changing classification basis changes which references receive priority.', 'ABC basis, effective date and one worked source classification.'),
    'DQ-EXP-001': ('Placement-effect isolation', 'Unequal SKU quantities confound availability/task mix with placement.', 'An approved common SKU-quantity ledger and eligibility definition for one controlled comparison.'),
    'DQ-STOCK-001': ('Availability and replenishment assumptions', 'Payload/UOM or timing errors change conditional stock arithmetic.', 'A decoded allocation cell with UOM and snapshot timestamp.'),
    'DQ-LAYOUT-001': ('Distance and accessibility assumptions', 'Unknown scale/floor access changes route feasibility and distance meaning.', 'One surveyed aisle segment and documented Z-to-floor/transfer mapping.'),
    'DQ-DUP-CUSTOMER': ('Demand quantity baseline', 'Removing legitimate repeated lines understates requested work.', 'Line event identifiers or source-owner explanation for one exact repeat pair.'),
    'DQ-DUP-PICKING': ('Published picking quantity baseline', 'Removing unit-expanded repeats can erase legitimate units.', 'One pick-event identifier and explanation of one-unit record expansion.'),
    'DQ-SIZE-001': ('SKU matching and eligibility', 'Half-token interpretation changes joins and matching quantity.', 'Authoritative size codebook with one 105/10.5 example.'),
    'DQ-SIZE-002': ('Known-size eligible work', 'Imputation would assign unsupported SKU identity to unknown demand.', 'Size field for one missing-size source record or explanation of intentional absence.'),
    'DQ-QTY-001': ('Positive-work versus record/group denominators', 'Counting placeholders as work changes task statistics.', 'Lifecycle meaning for one zero-quantity line.'),
    'DQ-LOC-002': ('Comparable geometry-retained placement population', 'Unequal exclusions change which cells enter policy comparisons.', 'Coordinate-master version and one excluded allocation location mapping.'),
    'DQ-MASTER-001': ('Active assortment/master eligibility', 'Master scope mismatch changes eligible inventory and ABC interpretation.', 'Master-effective-date and mapping for one unmatched allocation reference.'),
    'DQ-ID-001': ('Customer-order versus wave/order throughput', 'Split-wave identity changes the denominator and completion definition.', 'WMS business key and completion rule for one order spanning two waves.'),
}


RULES = [
    ('PARSE', 'AUTHORIZED_REPRESENTATION', 'NOT_A_SOURCE_CORRECTION', 'Existing delimiter/BOM parsing; raw bytes untouched.', 'All parsed fields and populations'),
    ('TRIM', 'AUTHORIZED_REPRESENTATION', 'NOT_A_SOURCE_CORRECTION', 'Existing whitespace-trimmed analytical keys; retain original tokens in token ledger.', 'Identifier joins; numeric parsing'),
    ('NUMERIC', 'AUTHORIZED_REPRESENTATION', 'NOT_A_SOURCE_CORRECTION', 'Existing Decimal spelling; missing remains missing.', 'Size-key equality'),
    ('HALF_SIZE', 'EXISTING_INFERRED_NORMALIZATION', 'SEMANTIC_APPROVAL_PENDING', 'Existing customer tokens 35,45,55,65,75,85,95,105,115,125 divided by ten.', 'Reconciliation; size eligibility; SKU demand'),
    ('LITERAL_SIZE', 'ANALYTICAL_SENSITIVITY', 'NOT_APPROVED_FOR_PRODUCTION', 'Customer half tokens remain literal numeric sizes. All source records retained.', 'Reconciliation; size-key population'),
    ('CUSTOMER_DEDUP', 'ANALYTICAL_SENSITIVITY', 'NOT_APPROVED_FOR_PRODUCTION', 'Keep first exact original customer tuple, then current normalization. No source rows removed.', 'Demand denominator; matched/gap/excess; key presence'),
    ('RETAIN', 'RETENTION', 'NO_CORRECTION_APPROVED', 'Keep repeated rows, zero quantities and missing sizes in current measures; unknown stays unknown.', 'All current populations'),
    ('ABC_VOLUME', 'DERIVED_ALTERNATIVE_BASIS', 'NOT_A_PUBLISHED_LABEL_REPLACEMENT', 'Rank full customer unit volume; cumulative-before thresholds 80/95, original reference tie order.', 'Derived ABC and classification disagreement'),
    ('CELL_ASSUMPTION', 'CONDITIONAL_ASSUMPTION', 'SEMANTIC_APPROVAL_PENDING', 'Existing token-as-size / one-cell-assumed-unit arithmetic; omit coordinate-excluded cells only for retained analysis.', 'Policy SKU counters; conditional finite-snapshot ceiling'),
]


def build(out):
    inputs = authenticate()
    issues = json.loads((REGISTRY / 'issues.json').read_text())
    validate_registry(issues)
    out.mkdir(parents=True, exist_ok=True)
    public = out / 'public'; public.mkdir(exist_ok=True)
    specs = {}

    def emit(name, rows, pk, grain, evidence, denominator):
        rows = list(rows)
        columns = list(rows[0])
        schema = {k: FIELDS[k] for k in columns}  # unexpected field is a hard failure
        keys = [tuple(r[k] for k in pk) for r in rows]
        if len(set(keys)) != len(keys):
            raise ValueError('Duplicate primary key: ' + name)
        for r in rows:
            assert list(r) == columns
            for k, value in r.items():
                s = schema[k]
                if value is None or value == '':
                    assert s['nullable'], (name, k, 'unexpected null')
                else:
                    assert type(value) is (int if s['type'] == 'integer' else str), (name, k, value)
                    if isinstance(value, str):
                        assert len(value) <= 4096 and not value.lstrip().startswith(('=', '+', '-', '@', '\t', '\r')), (name, k, 'unsafe cell')
        path = public / (name + '.csv')
        with path.open('w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=columns, lineterminator='\n'); w.writeheader(); w.writerows(rows)
        specs[name] = dict(grain=grain, primary_key=pk, rows=len(rows), fields=schema, evidence_class=evidence,
                           denominator=denominator, sha256=digest(path), bytes=path.stat().st_size)

    # Reuse the authenticated full current reconciliation; do not reimplement it.
    current = load(REGISTRY / 'reconciliation.csv')
    d, p, cr, pr = Counter(), Counter(), Counter(), Counter()
    for r in current:
        k = r['wave'], r['reference'], r['size']
        d[k] = int(r['customer_units']); p[k] = int(r['picking_units'])
        cr[k] = len(r['customer_rows'].split('|')) if r['customer_rows'] else 0
        pr[k] = len(r['picking_rows'].split('|')) if r['picking_rows'] else 0
    literal, dedup, lr, dr = Counter(), Counter(), Counter(), Counter()
    groups, tokens, seen = {}, {}, set()
    order_waves = defaultdict(set)
    for row in read('Customer_Order'):
        w, ref, order = (row[k].strip() for k in ('waveNumber', 'Reference', 'orderNumber'))
        raw_token = row['Size (US)']; token = raw_token.strip(); q = int(row['quantity (units)'])
        sk, lk = size(raw_token, True), size(raw_token)
        literal[w, ref, lk] += q; lr[w, ref, lk] += 1
        signature = tuple(row.values()); repeat = signature in seen; seen.add(signature)
        if not repeat:
            dedup[w, ref, sk] += q; dr[w, ref, sk] += 1
        g = groups.setdefault((w, order), dict(units=0, rows=0, refs=set(), skus=set(), repeats=0, missing=0, zeros=0))
        g['units'] += q; g['rows'] += 1; g['refs'].add(ref); g['skus'].add((ref, sk))
        g['repeats'] += repeat; g['missing'] += not token; g['zeros'] += q == 0
        order_waves[order].add(w)
        t = tokens.setdefault(('Customer_Order', raw_token), [0, 0]); t[0] += 1; t[1] += q
    for row in read('Picking_Wave'):
        t = tokens.setdefault(('Picking_Wave', row['Size (US)']), [0, 0])
        t[0] += 1; t[1] += int(row['quantityToPick (units)'])
    keys = sorted(d.keys() | p.keys() | literal.keys() | dedup.keys())
    emit('reconciliation', (
        dict(reconciliation_id=opaque('key', w, r, s), wave_id=opaque('wave', w), reference_id=opaque('ref', r),
             size_key=s or MISSING, current_customer_units=d[w, r, s], literal_customer_units=literal[w, r, s],
             dedup_customer_units=dedup[w, r, s], picking_units=p[w, r, s],
             current_customer_records=cr[w, r, s], literal_customer_records=lr[w, r, s],
             dedup_customer_records=dr[w, r, s], picking_records=pr[w, r, s]) for w, r, s in keys),
         ['reconciliation_id'], 'union wave/reference/size key across declared interpretations',
         'SOURCE_DERIVED + EXISTING_INFERRED_NORMALIZATION / ANALYTICAL_SENSITIVITY', 'selected interpretation SUM customer quantity; presence uses records > 0')
    summaries = []
    for label, qty, records in [('CURRENT_INFERRED', d, cr), ('LITERAL_SIZE', literal, lr), ('CUSTOMER_DEDUP', dedup, dr)]:
        active = records.keys() | {k for k in pr if pr[k] > 0}
        summaries.append(dict(interpretation=label, evidence_class='EXISTING_INFERRED_NORMALIZATION' if label == 'CURRENT_INFERRED' else 'ANALYTICAL_SENSITIVITY',
                              customer_units=sum(qty.values()), picking_units=sum(p.values()),
                              matched_units=sum(min(qty[k], p[k]) for k in active),
                              gap_units=sum(max(qty[k]-p[k], 0) for k in active), excess_units=sum(max(p[k]-qty[k], 0) for k in active),
                              customer_keys=sum(n > 0 for n in records.values()), picking_keys=sum(n > 0 for n in pr.values()),
                              union_keys=sum(records[k] > 0 or pr[k] > 0 for k in active), positive_gap_keys=sum(qty[k] > p[k] for k in active)))
    emit('reconciliation_summary', summaries, ['interpretation'], 'one full-extract interpretation', 'MIXED_EXPLICIT_PER_ROW', 'customer_units in same row; never sum interpretations')
    pareto = []
    for dim, pos, domain in [('wave', 0, 'wave'), ('reference', 1, 'ref')]:
        counts = Counter(); key_counts = Counter()
        for k in d:
            if d[k] > p[k]: counts[k[pos]] += d[k]-p[k]; key_counts[k[pos]] += 1
        cumulative = 0
        for rank, (key, n) in enumerate(sorted(counts.items(), key=lambda x: (-x[1], x[0])), 1):
            cumulative += n
            pareto.append(dict(dimension=dim, member_id=opaque(domain, key), rank=rank, gap_units=n,
                               positive_gap_keys=key_counts[key], cumulative_gap_units=cumulative, gap_denominator_units=sum(counts.values())))
    emit('exception_pareto', pareto, ['dimension', 'member_id'], 'positive current gap group within alternative dimension', 'SOURCE_DERIVED', 'gap_denominator_units MIN; each dimension totals 13003')
    emit('order_groups', (
        dict(order_group_id=opaque('group', w, o), wave_id=opaque('wave', w), order_id=opaque('order', o),
             customer_units=g['units'], source_records=g['rows'], distinct_references=len(g['refs']), distinct_size_skus=len(g['skus']),
             repeat_records=g['repeats'], missing_size_records=g['missing'], zero_quantity_records=g['zeros'], order_wave_count=len(order_waves[o]))
        for (w, o), g in sorted(groups.items())), ['order_group_id'], 'one wave/order source group; demand only', 'SOURCE_DERIVED', '39858 groups; picking has no order attribution')
    locations = {r['originalLocation'].strip() for r in read('Storage_Location')}
    products = {r['Reference'].strip() for r in read('Product')}
    coverage = []
    for source in ('Picking_Wave', *(x + '_Storage' for x in POLICIES)):
        counts, records, unknown = Counter(), Counter(), Counter()
        for row in read(source):
            loc = row['locations'].strip() if source == 'Picking_Wave' else row.get('originalLocation', row.get('Location')).strip()
            records[loc] += 1
            if source == 'Picking_Wave': counts[loc] += int(row['quantityToPick (units)'])
            else:
                for col, value in row.items():
                    if (col.startswith('col_') or col.isdigit()) and value.strip():
                        counts[loc] += 1; unknown[loc] += value.strip().split(';')[0] not in products
        for loc in sorted(records):
            coverage.append(dict(source_scope=source, location_id=opaque('loc', loc), mapped=int(loc in locations), quantity=counts[loc],
                                 records=records[loc], unit='published picking units' if source == 'Picking_Wave' else 'encoded allocation cells',
                                 scope_denominator=sum(counts.values()), unknown_reference_cells=unknown[loc]))
    emit('location_coverage', coverage, ['source_scope', 'location_id'], 'one source scope / stripped location', 'SOURCE_DERIVED', 'MIN scope_denominator within exactly one source scope; units differ')
    cumulative, abc = 0, []
    for rank, row in enumerate(sorted(load(REGISTRY / 'classification.csv'), key=lambda x: (-int(x['customer_units']), x['reference'])), 1):
        cumulative += int(row['customer_units'])
        abc.append(dict(reference_id=opaque('ref', row['reference']), published_abc=row['published_abc'], derived_abc=row['derived_abc'],
                        disagrees=int(row['disagrees']), customer_units=int(row['customer_units']), rank=rank,
                        cumulative_customer_units=cumulative, demand_denominator_units=sum(d.values())))
    emit('abc_comparison', abc, ['reference_id'], 'one demanded reference', 'PUBLISHED_SOURCE_OBSERVATION + SOURCE_DERIVED', '208 references or MIN demand_denominator_units for quantity share')
    emit('normalization_tokens', (
        dict(token_id=opaque('token', source, token), source_id=source + '.csv', field='Size (US)', original_token=token,
             current_value=size(token, source == 'Customer_Order'), alternative_value=size(token), token_records=n, token_units=q,
             rule_id='HALF_SIZE' if source == 'Customer_Order' and token.strip() in HALVES else 'RETAIN' if not token.strip() else 'NUMERIC')
        for (source, token), (n, q) in sorted(tokens.items())), ['token_id'], 'one source / original size token', 'PUBLISHED_SOURCE_OBSERVATION + EXISTING_INFERRED_NORMALIZATION', 'SUM token_records or token_units separately within source')
    emit('transformation_rules', (dict(zip(['rule_id', 'rule_kind', 'approval_state', 'description', 'affected_calculations'], r)) for r in RULES),
         ['rule_id'], 'one declared transformation, retention or scenario rule', 'MIXED_EXPLICIT_PER_ROW', 'not a rate; no approved corrections')
    pairs = [dict(policy_pair_id=r['policy_a'] + ':' + r['policy_b'], policy_a=r['policy_a'], policy_b=r['policy_b'],
                  union_skus=int(r['union_skus']), differing_skus=int(r['differing_skus']), l1_cell_difference=int(r['l1_cell_difference'])) for r in load(REGISTRY / 'policy_pairs.csv')]
    emit('policy_pairs', pairs, ['policy_pair_id'], 'one unordered published policy pair', 'CONDITIONAL_ASSUMPTION', 'union_skus per pair; no across-pair SUM')
    supply = [dict(policy=r['policy'], raw_encoded_cells=int(r['raw_encoded_cells']), retained_encoded_cells=int(r['retained_encoded_cells']),
                   excluded_cells=int(r['excluded_cells']), conditional_supply_ceiling=int(r['conditional_supply_ceiling']), demand_denominator_units=int(r['demand_denominator_units'])) for r in load(M3 / 'internal/policy_supply.csv')]
    emit('policy_supply', supply, ['policy'], 'one published policy, existing M3 stock arithmetic only', 'CONDITIONAL_ASSUMPTION', 'MIN demand_denominator_units; no alternative-policy SUM')
    controls = [dict(control_id='SKU:' + r['policy_pair_id'], scope=r['policy_pair_id'], control_name='Equal retained SKU quantities', result='FAIL',
                     observation=f"{r['differing_skus']} / {r['union_skus']} SKU counters differ; L1 {r['l1_cell_difference']} encoded cells.",
                     required_evidence='Approved common reference/size quantity ledger and eligibility population.') for r in pairs]
    for cid, name, result, observation, request in [
        ('TOTAL', 'Equal retained cell totals', 'PASS_DESCRIPTIVE', 'Each policy has 41256 retained encoded cells. Total equality does not imply SKU equality.', 'Retain this descriptive check alongside SKU-level controls.'),
        ('COVERAGE', 'Common coordinate coverage', 'FAIL', 'Raw excluded cells differ: Random 0, Class_Based 882, Dedicated 864, Hybrid 864.', 'Aligned location master and agreed common eligible placement domain.'),
        ('UOM', 'Verified payload and unit meaning', 'UNVERIFIED', 'README quantity wording and adopted size/one-cell-unit assumptions differ.', 'Source-owner decoded cell/UOM example.'),
        ('TIME', 'Aligned inventory and demand horizon', 'UNVERIFIED', 'Snapshot dates, receipts and inventory trajectories unavailable.', 'Dated inventory plus matching demand window and receipt rules.'),
        ('TASKS', 'Common eligible task mix', 'NOT_ESTABLISHED', 'Unequal supply can select different feasible tasks.', 'Predeclared same eligible SKU/task workload and service denominator.'),
        ('LAYOUT', 'Validated geometry and movement assumptions', 'UNVERIFIED', 'Scale, floors, transfers and access graph lack physical validation.', 'Surveyed path segment, floor transfer and safety/access constraints.'),
        ('OUTCOMES', 'Observed operational performance baseline', 'NOT_MEASURED', 'No completion durations, due dates or real cost observations.', 'Representative pick/release/completion events and agreed KPI baseline.'),
        ('PROTOCOL', 'Independent human-approved controlled protocol', 'NOT_APPROVED', 'G0–G4 PENDING; no controlled experiment authorized by this handoff.', 'Named reviewer, common-stock protocol, acceptance and stop conditions.'),
    ]:
        controls.append(dict(control_id=cid, scope='GLOBAL', control_name=name, result=result, observation=observation, required_evidence=request))
    emit('experiment_controls', controls, ['control_id'], 'one global or pair-scoped experiment control', 'AI_PROPOSED_REQUIRES_HUMAN_REVIEW', 'no readiness percentage: controls have different states/meaning')
    decisions = []
    for r in issues:
        kpi, mechanism, request = DECISIONS[r['issue_id']]
        decisions.append(dict(issue_id=r['issue_id'], title=r['title'], status=r['status'], review_state=r['review']['state'], severity=r['severity'],
                              decision_category=r['business_decision_category'], business_decision=r['business_decision'], kpi_at_risk=kpi,
                              business_mechanism=mechanism, competing_explanations=' | '.join(r['hypothesized_causes']),
                              evidence_readiness='ARITHMETIC_REPRODUCIBLE_SEMANTICS_PENDING' if any(m['affected_count'] is not None for m in r['metrics']) else 'SOURCE_DEFINITION_REQUIRED_UNMEASURED',
                              recommendation='Retain records and current declared assumptions; withhold source correction and operational intervention pending source evidence and human review.',
                              next_evidence_request=request, evidence_class='AI_PROPOSED_REQUIRES_HUMAN_REVIEW', evidence_ref='docs/data-quality/registry/issues.json#' + r['issue_id']))
    emit('decision_evidence', decisions, ['issue_id'], 'one issue-to-decision question', 'AI_PROPOSED_REQUIRES_HUMAN_REVIEW', 'COUNTD issue_id is questions, not unique affected units')
    emit('issue_evidence', (
        dict(issue_source_id=r['issue_source_id'], issue_id=r['issue_id'], source_id=r['source_id'], source_sha256=r['source_sha256'],
             lineage_role=r['lineage_role'], selected_record_count=int(r['selected_record_count']) if r['selected_record_count'] else None,
             source_record_count=int(r['source_record_count']) if r['source_record_count'] else None, evidence_ref=r['evidence_ref'])
        for r in load(M3 / 'internal/issue_sources.csv')), ['issue_source_id'], 'one issue/source lineage role', 'SOURCE_DERIVED', 'counts by role; no cross-issue affected count or source population sum')
    emit('profile_checks', (
        dict(source_id=r['source'], field=r['field'], check=r['check'], affected_rows=int(r['affected_rows']), population_rows=int(r['population_rows']))
        for r in load(REGISTRY / 'profile_checks.csv')), ['source_id', 'field', 'check'], 'one completed source/field/check', 'PUBLISHED_SOURCE_OBSERVATION + SOURCE_DERIVED', 'population_rows for that source/check, including zero results')
    manifest = dict(version='M4-B-1.0', tables=specs, inputs=inputs, generator_sha256=digest(Path(__file__)),
                    public_allowlist=[name + '.csv' for name in specs],
                    reused_public_sources=['docs/data-quality/tableau/public/' + name + '.csv' for name in ('issues', 'issue_metrics', 'source_counts')],
                    identifier_encoding='domain + SHA256(JSON compact [domain, original parts]) first 20 hex; pseudonymous, not anonymous',
                    approved_source_corrections=0, human_review='PENDING', synthetic_inventory_scenarios_generated=False,
                    publication='OFFLINE_PREPARED_NOT_UPLOADED', source_attribution='Rodrigo Furlan de Assis; Mendeley Data v1; 10.17632/pf2w725pw3.1; CC BY 4.0',
                    null_policy='CSV blank = unknown/not present; size_key MISSING preserves unknown identity; never numeric zero')
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + '\n')
    doc = ['# Advanced analytics data dictionary', '', 'Generated by `scripts/data_quality/build_advanced.py`; exact schema and hashes: `manifest.json`.', '',
           'UTF-8, comma, LF, quoted text. Import IDs and size_key as strings; integer measures as whole numbers. Blank = unknown; never ZN unknown physical measures. Evidence classes can differ between published fields and derived measures in the same table. No approved source correction. All quantities describe the full pinned extract, not warehouse truth.', '']
    for name, s in specs.items():
        doc += [f'## {name}.csv', '', f"Grain: {s['grain']}. Primary key: `{', '.join(s['primary_key'])}`. Rows: {s['rows']:,}.", '',
                f"Evidence: {s['evidence_class']}. Denominator: {s['denominator']}.", '', '| Field | Type / nullable | Meaning | Aggregation |', '|---|---|---|---|']
        for k, f in s['fields'].items():
            doc.append(f"| {k} | {f['type']} / {'yes' if f['nullable'] else 'no'} | {f['definition']} | {f['aggregation']} |")
        doc.append('')
    (out / 'DATA_DICTIONARY.md').write_text('\n'.join(doc) + '\n')
    return specs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=DEFAULT_OUT)
    target = parser.parse_args().output_dir.resolve()
    if target != DEFAULT_OUT.resolve() and target.exists() and any(target.iterdir()):
        parser.error('Alternate output must be empty')
    if target == ROOT or any(target == ROOT / p or ROOT / p in target.parents for p in ('data', 'public', 'src', 'tests', 'scripts')):
        parser.error('Use an isolated research output directory')
    specs = build(target)
    print(json.dumps({'tables': len(specs), 'rows': {k: v['rows'] for k, v in specs.items()}, 'published': False}, indent=2))
