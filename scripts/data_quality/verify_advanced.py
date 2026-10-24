#!/usr/bin/env python3
"""Independent raw-to-public SQLite reconciliation; never imports the exporter."""
import argparse
from collections import Counter
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/data-quality/advanced'
HEADERS = {
    'reconciliation': 'reconciliation_id wave_id reference_id size_key current_customer_units literal_customer_units dedup_customer_units picking_units current_customer_records literal_customer_records dedup_customer_records picking_records',
    'reconciliation_summary': 'interpretation evidence_class customer_units picking_units matched_units gap_units excess_units customer_keys picking_keys union_keys positive_gap_keys',
    'exception_pareto': 'dimension member_id rank gap_units positive_gap_keys cumulative_gap_units gap_denominator_units',
    'order_groups': 'order_group_id wave_id order_id customer_units source_records distinct_references distinct_size_skus repeat_records missing_size_records zero_quantity_records order_wave_count',
    'location_coverage': 'source_scope location_id mapped quantity records unit scope_denominator unknown_reference_cells',
    'abc_comparison': 'reference_id published_abc derived_abc disagrees customer_units rank cumulative_customer_units demand_denominator_units',
    'normalization_tokens': 'token_id source_id field original_token current_value alternative_value token_records token_units rule_id',
    'transformation_rules': 'rule_id rule_kind approval_state description affected_calculations',
    'policy_pairs': 'policy_pair_id policy_a policy_b union_skus differing_skus l1_cell_difference',
    'policy_supply': 'policy raw_encoded_cells retained_encoded_cells excluded_cells conditional_supply_ceiling demand_denominator_units',
    'experiment_controls': 'control_id scope control_name result observation required_evidence',
    'decision_evidence': 'issue_id title status review_state severity decision_category business_decision kpi_at_risk business_mechanism competing_explanations evidence_readiness recommendation next_evidence_request evidence_class evidence_ref',
    'issue_evidence': 'issue_source_id issue_id source_id source_sha256 lineage_role selected_record_count source_record_count evidence_ref',
    'profile_checks': 'source_id field check affected_rows population_rows',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ident(domain, *parts):
    # Independent implementation of documented public identifier wire format.
    return domain + '_' + hashlib.sha256(json.dumps([domain, *parts], separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()[:20]


def norm(token, inferred=False):
    v = token.strip()
    if not v: return ''
    n = Decimal(v)
    if inferred and v in ('35', '45', '55', '65', '75', '85', '95', '105', '115', '125'):
        n /= Decimal(10)
    return str(int(n)) if n == n.to_integral() else format(n.normalize(), 'f')


def read_raw(name):
    with (ROOT / 'data/raw' / (name + '.csv')).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=',' if name in ('Random_Storage', 'Storage_Location') else ';'))


def validate_csv(name, rows, headers, spec):
    assert headers == HEADERS[name].split(), ('public header allowlist', name)
    assert set(spec['fields']) == set(headers)
    assert len(rows) == spec['rows'], ('row count', name)
    seen = set()
    for row in rows:
        assert set(row) == set(headers), ('ragged record', name)
        key = tuple(row[k] for k in spec['primary_key'])
        assert all(key) and key not in seen, ('duplicate/blank key', name, key)
        seen.add(key)
        for k, v in row.items():
            field = spec['fields'][k]
            assert v is not None and len(v) <= 4096, ('transport', name, k)
            assert v != '' or field['nullable'], ('unexpected null', name, k)
            assert not v.lstrip().startswith(('=', '+', '-', '@', '\t', '\r')), ('formula cell', name, k)
            if v and field['type'] == 'integer':
                assert str(int(v)) == v and int(v) >= 0, ('invalid count', name, k)


def equal(actual, expected, label):
    assert actual == expected, (label, str(actual)[:300], str(expected)[:300])


def verify(out=OUT):
    checks = []
    def check(label, actual, expected):
        equal(actual, expected, label); checks.append(label)
    m = json.loads((out / 'manifest.json').read_text())
    check('exact public table allowlist', set(m['public_allowlist']), {n + '.csv' for n in HEADERS})
    check('no extra public files', {p.name for p in (out / 'public').iterdir()}, set(m['public_allowlist']))
    for path, expected in m['inputs'].items(): check('input hash ' + path, sha(ROOT / path), expected)
    check('generator code hash', sha(ROOT / 'scripts/data_quality/build_advanced.py'), m['generator_sha256'])
    data = {}
    for name in HEADERS:
        with (out / 'public' / (name + '.csv')).open(encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f); rows = list(reader)
            validate_csv(name, rows, reader.fieldnames, m['tables'][name])
        check('public output hash ' + name, sha(out / 'public' / (name + '.csv')), m['tables'][name]['sha256'])
        data[name] = rows
    checks.append('all public schemas, unique keys, count/null types, transport and formula safety')

    c, p = read_raw('Customer_Order'), read_raw('Picking_Wave')
    db = sqlite3.connect(':memory:')
    db.executescript('''
      CREATE TABLE c(ordinal INT, wave TEXT, ord TEXT, ref TEXT, size TEXT, literal TEXT, qty INT, original TEXT, signature TEXT);
      CREATE TABLE p(ordinal INT, wave TEXT, ref TEXT, size TEXT, qty INT, loc TEXT, original TEXT);
      CREATE TABLE g(loc TEXT PRIMARY KEY);
      CREATE TABLE products(ref TEXT PRIMARY KEY, abc TEXT);
      CREATE TABLE cells(policy TEXT, ordinal INT, loc TEXT, ref TEXT, size TEXT);
      CREATE TABLE allocation_rows(policy TEXT, ordinal INT, loc TEXT);
    ''')
    for table, rows in data.items():
        columns = HEADERS[table].split()
        definitions = ','.join('"' + k + '" ' + ('INTEGER' if m['tables'][table]['fields'][k]['type'] == 'integer' else 'TEXT') for k in columns)
        db.execute(f'CREATE TABLE out_{table} ({definitions})')
        db.executemany(f"INSERT INTO out_{table} VALUES({','.join('?' for _ in columns)})", [
            tuple(None if r[k] == '' else int(r[k]) if m['tables'][table]['fields'][k]['type'] == 'integer' else r[k] for k in columns) for r in rows])
    query_path = OUT / 'consumer_checks.sql'
    consumer_checks = []
    for label, actual_value, expected_value in db.execute(query_path.read_text()):
        check('CSV consumer SQL ' + label, actual_value, expected_value)
        consumer_checks.append(dict(check=label, actual=actual_value, expected=expected_value))
    db.executemany('INSERT INTO c VALUES(?,?,?,?,?,?,?,?,?)', [
        (i, r['waveNumber'].strip(), r['orderNumber'].strip(), r['Reference'].strip(), norm(r['Size (US)'], True),
         norm(r['Size (US)']), int(r['quantity (units)']), r['Size (US)'], json.dumps(list(r.values()))) for i, r in enumerate(c, 2)])
    db.executemany('INSERT INTO p VALUES(?,?,?,?,?,?,?)', [
        (i, r['waveNumber'].strip(), r['reference'].strip(), norm(r['Size (US)']), int(r['quantityToPick (units)']), r['locations'].strip(), r['Size (US)']) for i, r in enumerate(p, 2)])
    db.executemany('INSERT INTO g VALUES(?)', [(r['originalLocation'].strip(),) for r in read_raw('Storage_Location')])
    db.executemany('INSERT INTO products VALUES(?,?)', [(r['Reference'].strip(), r['ABCCOD'].strip()) for r in read_raw('Product')])
    for domain, originals in [('wave', {r['waveNumber'].strip() for r in c + p}),
                              ('ref', {r['Reference'].strip() for r in c} | {r['reference'].strip() for r in p}),
                              ('order', {r['orderNumber'].strip() for r in c})]:
        check('pseudonym collision check ' + domain, len({ident(domain, v) for v in originals}), len(originals))
    db.executescript('''
      CREATE TABLE cd AS SELECT * FROM c WHERE ordinal IN (SELECT MIN(ordinal) FROM c GROUP BY signature);
      CREATE TABLE cq AS SELECT wave,ref,size,SUM(qty) q,COUNT(*) n FROM c GROUP BY wave,ref,size;
      CREATE TABLE lq AS SELECT wave,ref,literal size,SUM(qty) q,COUNT(*) n FROM c GROUP BY wave,ref,literal;
      CREATE TABLE dq AS SELECT wave,ref,size,SUM(qty) q,COUNT(*) n FROM cd GROUP BY wave,ref,size;
      CREATE TABLE pq AS SELECT wave,ref,size,SUM(qty) q,COUNT(*) n FROM p GROUP BY wave,ref,size;
      CREATE TABLE keys AS SELECT wave,ref,size FROM cq UNION SELECT wave,ref,size FROM lq UNION SELECT wave,ref,size FROM dq UNION SELECT wave,ref,size FROM pq;
      CREATE UNIQUE INDEX ci ON cq(wave,ref,size);
      CREATE UNIQUE INDEX li ON lq(wave,ref,size);
      CREATE UNIQUE INDEX di ON dq(wave,ref,size);
      CREATE UNIQUE INDEX pi ON pq(wave,ref,size);
      CREATE INDEX cord ON c(ord);
    ''')
    expected = {}
    for w, ref, size, cq, lq, dq, pq, cn, ln, dn, pn in db.execute('''
       SELECT k.wave,k.ref,k.size,COALESCE(c.q,0),COALESCE(l.q,0),COALESCE(d.q,0),COALESCE(p.q,0),
       COALESCE(c.n,0),COALESCE(l.n,0),COALESCE(d.n,0),COALESCE(p.n,0)
       FROM keys k LEFT JOIN cq c USING(wave,ref,size) LEFT JOIN lq l USING(wave,ref,size)
       LEFT JOIN dq d USING(wave,ref,size) LEFT JOIN pq p USING(wave,ref,size)'''):
        key = ident('key', w, ref, size)
        assert key not in expected, 'pseudonym collision'
        expected[key] = (ident('wave', w), ident('ref', ref), size or 'MISSING', cq, lq, dq, pq, cn, ln, dn, pn)
    actual = {r['reconciliation_id']: tuple(r[k] if i < 3 else int(r[k]) for i, k in enumerate(HEADERS['reconciliation'].split()[1:])) for r in data['reconciliation']}
    check('every reconciliation key, quantities, presence counts and identifiers from independent SQL', actual, expected)
    summary = {}
    for label, table in [('CURRENT_INFERRED', 'cq'), ('LITERAL_SIZE', 'lq'), ('CUSTOMER_DEDUP', 'dq')]:
        result = db.execute(f'''WITH k AS (SELECT wave,ref,size FROM {table} UNION SELECT wave,ref,size FROM pq)
           SELECT SUM(COALESCE(c.q,0)),SUM(COALESCE(p.q,0)),SUM(MIN(COALESCE(c.q,0),COALESCE(p.q,0))),
           SUM(MAX(COALESCE(c.q,0)-COALESCE(p.q,0),0)),SUM(MAX(COALESCE(p.q,0)-COALESCE(c.q,0),0)),
           COUNT(c.n),COUNT(p.n),COUNT(*),SUM(COALESCE(c.q,0)>COALESCE(p.q,0))
           FROM k LEFT JOIN {table} c USING(wave,ref,size) LEFT JOIN pq p USING(wave,ref,size)''').fetchone()
        row = next(r for r in data['reconciliation_summary'] if r['interpretation'] == label)
        check('SQL summary ' + label, tuple(int(row[k]) for k in HEADERS['reconciliation_summary'].split()[2:]), result)
        check('summary evidence class ' + label, row['evidence_class'], 'EXISTING_INFERRED_NORMALIZATION' if label == 'CURRENT_INFERRED' else 'ANALYTICAL_SENSITIVITY')
        summary[label] = dict(zip(HEADERS['reconciliation_summary'].split()[2:], result))
    check('current reference acceptance', tuple(summary['CURRENT_INFERRED'][k] for k in ('customer_units', 'picking_units', 'matched_units', 'gap_units', 'excess_units', 'positive_gap_keys')), (228195, 215192, 215192, 13003, 0, 5242))
    check('literal match reference acceptance', summary['LITERAL_SIZE']['matched_units'], 149514)
    check('dedup reference acceptance', tuple(summary['CUSTOMER_DEDUP'][k] for k in ('matched_units', 'gap_units', 'excess_units')), (202475, 12985, 12717))
    for dim, col, domain in [('wave', 'wave', 'wave'), ('reference', 'ref', 'ref')]:
        rows = db.execute(f'''SELECT c.{col},SUM(c.q-COALESCE(p.q,0)) q,COUNT(*) n
                FROM cq c LEFT JOIN pq p USING(wave,ref,size) WHERE c.q>COALESCE(p.q,0)
                GROUP BY c.{col} ORDER BY q DESC,c.{col}''').fetchall()
        cumulative, want = 0, {}
        for rank, (member, q, n) in enumerate(rows, 1):
            cumulative += q; want[ident(domain, member)] = (rank, q, n, cumulative, 13003)
        got = {r['member_id']: tuple(int(r[k]) for k in ('rank', 'gap_units', 'positive_gap_keys', 'cumulative_gap_units', 'gap_denominator_units')) for r in data['exception_pareto'] if r['dimension'] == dim}
        check('SQL Pareto fixed denominator/ranks ' + dim, got, want)
    group_expected = {}
    for w, o, q, n, nr, ns, repeats, missing, zeros, waves in db.execute('''
        SELECT wave,ord,SUM(qty),COUNT(*),COUNT(DISTINCT ref),COUNT(DISTINCT ref||char(0)||size),
        SUM(ordinal NOT IN (SELECT ordinal FROM cd)),SUM(size=''),SUM(qty=0),
        (SELECT COUNT(DISTINCT wave) FROM c a WHERE a.ord=c.ord)
        FROM c GROUP BY wave,ord'''):
        group_expected[ident('group', w, o)] = (ident('wave', w), ident('order', o), q, n, nr, ns, repeats, missing, zeros, waves)
    got = {r['order_group_id']: tuple(r[k] if i < 2 else int(r[k]) for i, k in enumerate(HEADERS['order_groups'].split()[1:])) for r in data['order_groups']}
    check('all SQL wave/order groups and exception counts', got, group_expected)
    check('group lineage population', (len(got), sum(int(r['source_records']) for r in data['order_groups']), sum(int(r['customer_units']) for r in data['order_groups'])), (39858, 122370, 228195))
    samples = [
        db.execute('SELECT c.wave,c.ref,c.size FROM cq c LEFT JOIN pq p USING(wave,ref,size) WHERE c.q>COALESCE(p.q,0) LIMIT 1').fetchone(),
        db.execute('SELECT l.wave,l.ref,l.size FROM lq l LEFT JOIN cq c USING(wave,ref,size) WHERE c.n IS NULL LIMIT 1').fetchone(),
        db.execute('SELECT wave,ref,size FROM c WHERE ordinal NOT IN (SELECT ordinal FROM cd) LIMIT 1').fetchone(),
    ]
    for index, raw_key in enumerate(samples, 1):
        run = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/data_quality/lookup_advanced.py'), ident('key', *raw_key)],
                             check=True, capture_output=True, text=True)
        lookup = json.loads(run.stdout)
        check('local lookup raw key ' + str(index), tuple(lookup['raw_key'][k] for k in ('wave', 'reference', 'size')), raw_key)
        for label, table, size_column in [('CURRENT_INFERRED', 'c', 'size'), ('LITERAL_SIZE', 'c', 'literal'), ('CUSTOMER_DEDUP', 'cd', 'size'), ('PICKING', 'p', 'size')]:
            original = db.execute(f'SELECT ordinal,qty FROM {table} WHERE wave=? AND ref=? AND {size_column}=? ORDER BY ordinal', raw_key).fetchall()
            selection = lookup['selections'][label]
            expanded = [i for a, b in selection['record_ranges'] for i in range(a, b+1)]
            check('local lookup exact ordinals/quantity ' + str(index) + ':' + label,
                  (expanded, selection['record_count'], selection['quantity']), ([i for i, q in original], len(original), sum(q for i, q in original)))

    policies = ('Random', 'Class_Based', 'Dedicated', 'Hybrid')
    for policy in policies:
        cells, records = [], []
        for i, r in enumerate(read_raw(policy + '_Storage'), 2):
            loc = r.get('originalLocation', r.get('Location')).strip(); records.append((policy, i, loc))
            for col, value in r.items():
                if (col.startswith('col_') or col.isdigit()) and value.strip():
                    ref, token = value.strip().split(';'); cells.append((policy, i, loc, ref, norm(token)))
        db.executemany('INSERT INTO cells VALUES(?,?,?,?,?)', cells)
        db.executemany('INSERT INTO allocation_rows VALUES(?,?,?)', records)
    db.executescript('''
        CREATE INDEX cellloc ON cells(policy,loc);
        CREATE TABLE stock AS SELECT policy,ref,size,COUNT(*) q FROM cells JOIN g USING(loc) GROUP BY policy,ref,size;
        CREATE UNIQUE INDEX stocki ON stock(policy,ref,size);
    ''')
    coverage = {}
    for loc, qty, n, mapped in db.execute('SELECT p.loc,SUM(qty),COUNT(*),g.loc IS NOT NULL FROM p LEFT JOIN g USING(loc) GROUP BY p.loc'):
        coverage['Picking_Wave', ident('loc', loc)] = (mapped, qty, n, 'published picking units', 215192, 0)
    for policy in policies:
        denominator = db.execute('SELECT COUNT(*) FROM cells WHERE policy=?', (policy,)).fetchone()[0]
        for loc, n, qty, unknown, mapped in db.execute('''
            SELECT a.loc,COUNT(DISTINCT a.ordinal),COUNT(v.ref),SUM(v.ref IS NOT NULL AND m.ref IS NULL),g.loc IS NOT NULL
            FROM allocation_rows a LEFT JOIN cells v ON a.policy=v.policy AND a.ordinal=v.ordinal
            LEFT JOIN products m ON v.ref=m.ref LEFT JOIN g ON a.loc=g.loc WHERE a.policy=? GROUP BY a.loc''', (policy,)):
            coverage[policy + '_Storage', ident('loc', loc)] = (mapped, qty, n, 'encoded allocation cells', denominator, unknown)
    got = {(r['source_scope'], r['location_id']): (int(r['mapped']), int(r['quantity']), int(r['records']), r['unit'], int(r['scope_denominator']), int(r['unknown_reference_cells'])) for r in data['location_coverage']}
    check('every SQL source/location mapping/unknown-master group', got, coverage)
    all_locations = {r['locations'].strip() for r in p}
    for policy in policies:
        all_locations.update(r.get('originalLocation', r.get('Location')).strip() for r in read_raw(policy + '_Storage'))
    check('pseudonym collision check loc', len({ident('loc', v) for v in all_locations}), len(all_locations))
    unmapped = [r for r in data['location_coverage'] if r['source_scope'] == 'Picking_Wave' and r['mapped'] == '0']
    check('picking unmapped acceptance', (len(unmapped), sum(int(r['quantity']) for r in unmapped)), (22, 23609))
    rank, running, abc = 0, 0, {}
    for ref, q, published in db.execute('SELECT c.ref,SUM(qty) q,products.abc FROM c JOIN products USING(ref) GROUP BY c.ref ORDER BY q DESC,c.ref'):
        rank += 1; derived = 'A' if running * 100 < 80 * 228195 else 'B' if running * 100 < 95 * 228195 else 'C'
        running += q; abc[ident('ref', ref)] = (published, derived, int(published != derived), q, rank, running, 228195)
    got = {r['reference_id']: tuple(r[k] if i < 2 else int(r[k]) for i, k in enumerate(HEADERS['abc_comparison'].split()[1:])) for r in data['abc_comparison']}
    check('all SQL ABC references, original-key ties and cumulative-before thresholds', got, abc)
    check('ABC disagreement acceptance', sum(v[2] for v in abc.values()), 96)
    token_expected = {}
    for source, table in [('Customer_Order', 'c'), ('Picking_Wave', 'p')]:
        for token, n, q in db.execute(f'SELECT original,COUNT(*),SUM(qty) FROM {table} GROUP BY original'):
            rule = 'HALF_SIZE' if source == 'Customer_Order' and token.strip() in ('35','45','55','65','75','85','95','105','115','125') else 'RETAIN' if not token.strip() else 'NUMERIC'
            token_expected[ident('token', source, token)] = (source + '.csv', 'Size (US)', token, norm(token, source == 'Customer_Order'), norm(token), n, q, rule)
    got = {r['token_id']: tuple(int(r[k]) if k in ('token_records', 'token_units') else r[k] for k in HEADERS['normalization_tokens'].split()[1:]) for r in data['normalization_tokens']}
    check('all SQL original/current/literal token populations', got, token_expected)
    stocks = {policy: dict(((ref, size), n) for ref, size, n in db.execute('SELECT ref,size,q FROM stock WHERE policy=?', (policy,))) for policy in policies}
    for r in data['policy_pairs']:
        a, b = stocks[r['policy_a']], stocks[r['policy_b']]; keys = a.keys() | b.keys()
        want = len(keys), sum(a.get(k, 0) != b.get(k, 0) for k in keys), sum(abs(a.get(k, 0)-b.get(k, 0)) for k in keys)
        check('raw SKU counters pair ' + r['policy_pair_id'], tuple(int(r[k]) for k in ('union_skus', 'differing_skus', 'l1_cell_difference')), want)
    for r in data['policy_supply']:
        policy = r['policy']
        raw, retained = db.execute('SELECT COUNT(*),SUM(g.loc IS NOT NULL) FROM cells LEFT JOIN g USING(loc) WHERE policy=?', (policy,)).fetchone()
        bound = db.execute('''WITH d AS (SELECT ref,size,SUM(qty) q FROM c GROUP BY ref,size)
            SELECT SUM(MIN(d.q,COALESCE(s.q,0))) FROM d LEFT JOIN stock s ON d.ref=s.ref AND d.size=s.size AND s.policy=?''', (policy,)).fetchone()[0]
        check('SQL policy raw/retained/excluded and bound ' + policy, tuple(int(r[k]) for k in ('raw_encoded_cells', 'retained_encoded_cells', 'excluded_cells', 'conditional_supply_ceiling', 'demand_denominator_units')), (raw, retained, raw-retained, bound, 228195))
    states = {r['control_id']: r['result'] for r in data['experiment_controls']}
    wanted_states = {'SKU:' + r['policy_pair_id']: 'FAIL' for r in data['policy_pairs']}
    wanted_states.update(TOTAL='PASS_DESCRIPTIVE', COVERAGE='FAIL', UOM='UNVERIFIED', TIME='UNVERIFIED', TASKS='NOT_ESTABLISHED', LAYOUT='UNVERIFIED', OUTCOMES='NOT_MEASURED', PROTOCOL='NOT_APPROVED')
    check('control states cannot imply readiness', states, wanted_states)
    rules = {r['rule_id']: r['approval_state'] for r in data['transformation_rules']}
    check('explicit rule approval boundaries', rules, dict(PARSE='NOT_A_SOURCE_CORRECTION', TRIM='NOT_A_SOURCE_CORRECTION', NUMERIC='NOT_A_SOURCE_CORRECTION', HALF_SIZE='SEMANTIC_APPROVAL_PENDING', LITERAL_SIZE='NOT_APPROVED_FOR_PRODUCTION', CUSTOMER_DEDUP='NOT_APPROVED_FOR_PRODUCTION', RETAIN='NO_CORRECTION_APPROVED', ABC_VOLUME='NOT_A_PUBLISHED_LABEL_REPLACEMENT', CELL_ASSUMPTION='SEMANTIC_APPROVAL_PENDING'))
    issues = json.loads((ROOT / 'docs/data-quality/registry/issues.json').read_text())
    check('all issue decisions covered', {r['issue_id'] for r in data['decision_evidence']}, {r['issue_id'] for r in issues})
    for r in data['decision_evidence']:
        source = next(i for i in issues if i['issue_id'] == r['issue_id'])
        check('decision lineage/status ' + r['issue_id'], (r['title'], r['status'], r['review_state'], r['business_decision'], r['competing_explanations']),
              (source['title'], source['status'], 'PENDING', source['business_decision'], ' | '.join(source['hypothesized_causes'])))
        assert r['next_evidence_request'] and r['business_mechanism'] and r['recommendation']
    lineages = {}
    counts = json.loads((ROOT / 'docs/data-quality/registry/manifest.json').read_text())['source_record_counts']
    for r in issues:
        for i, line in enumerate(r['source_lineage'], 1):
            source = Path(line['source_file']).name
            lineages[r['issue_id'] + ':' + str(i)] = (r['issue_id'], source, sha(ROOT / line['source_file']), line['role'],
                  str(sum(b-a+1 for a, b in line['record_ranges'])) if line['record_ranges'] else '', str(counts.get(source, '')), line['source_file'])
    check('all issue-source roles, counts and raw hashes', {r['issue_source_id']: tuple(r[k] for k in HEADERS['issue_evidence'].split()[1:]) for r in data['issue_evidence']}, lineages)
    for r in data['profile_checks']:
        raw = read_raw(Path(r['source_id']).stem); vals = [row[r['field']].strip() for row in raw]
        n = sum(not v for v in vals) if r['check'] == 'blank_identifier' else len(vals)-len(set(vals)) if r['check'] == 'duplicate_master_id_after_first' else sum(int(v) < 0 for v in vals)
        check('independent profile ' + r['source_id'] + ':' + r['field'] + ':' + r['check'], (int(r['affected_rows']), int(r['population_rows'])), (n, len(raw)))

    # Mutation checks exercise the same consumer gates using altered real records.
    negative = []
    def rejects(label, fn):
        try: fn()
        except (AssertionError, ValueError, KeyError): negative.append(label)
        else: raise AssertionError('Invalid mutation accepted: ' + label)
    small = data['decision_evidence']; spec = m['tables']['decision_evidence']; headers = HEADERS['decision_evidence'].split()
    rejects('extra sensitive header', lambda: validate_csv('decision_evidence', small, headers + ['operator'], spec))
    rejects('duplicate issue key', lambda: validate_csv('decision_evidence', small[:-1] + [small[0]], headers, spec))
    rejects('spreadsheet formula', lambda: validate_csv('decision_evidence', [{**small[0], 'title': '=HYPERLINK("external")'}] + small[1:], headers, spec))
    changed = dict(actual); first = next(iter(changed)); values = list(changed[first]); values[3] += 1; changed[first] = tuple(values)
    rejects('wrong source-to-output quantity', lambda: equal(changed, expected, 'quantity mutation'))
    rejects('false experiment approval', lambda: equal({**states, 'PROTOCOL': 'PASS'}, wanted_states, 'approval mutation'))
    check('zero source corrections / no synthetic inventory scenarios', (m['approved_source_corrections'], m['synthetic_inventory_scenarios_generated'], m['human_review']), (0, False, 'PENDING'))
    protected = json.loads((OUT / 'evidence/baseline-preservation.json').read_text())
    for path, expected_hash in protected.items(): check('preserved ' + path, sha(ROOT / path), expected_hash)
    gates = json.loads((ROOT / 'docs/GATE_REVIEWS.json').read_text())['gates']
    assert len(gates) == 5 and all(g['reviewState'] == 'PENDING' and g['decision'] is None for g in gates)
    db.close()
    return dict(status='PASS', independent_method='Separately implemented SQLite aggregates from original CSVs; no generator imports. Independent computational method, not independent human review.',
                checks=checks, negative_checks=negative, preserved_files=len(protected), totals=summary,
                tables={k: len(v) for k, v in data.items()}, consumer_checks=consumer_checks, consumer_sql_sha256=sha(query_path), source_corrections_approved=0,
                simulation_executed=False, synthetic_inventory_scenarios_generated=False,
                workbook_import_render_and_interactions='NOT_TESTED_MANUAL_HANDOFF', human_review='PENDING', gates='G0–G4 PENDING')


def main():
    report = verify()
    with tempfile.TemporaryDirectory() as tmp:
        replay = Path(tmp)
        subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/data_quality/build_advanced.py'), '--output-dir', tmp], check=True, capture_output=True, text=True)
        names = ['manifest.json', 'DATA_DICTIONARY.md'] + ['public/' + name + '.csv' for name in HEADERS]
        for name in names: equal((replay / name).read_bytes(), (OUT / name).read_bytes(), 'byte replay ' + name)
    report['byte_identical_replayed_files'] = len(names)
    run = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_dq_*.py', '-v'], cwd=ROOT, capture_output=True, text=True)
    assert run.returncode == 0, run.stdout + run.stderr
    report['foundation_test_output'] = run.stdout + run.stderr
    report['validator_sha256'] = sha(Path(__file__))
    report['lookup_sha256'] = sha(ROOT / 'scripts/data_quality/lookup_advanced.py')
    report['manifest_sha256'] = sha(OUT / 'manifest.json')
    report['artifact_hashes'] = {name: sha(OUT / name) for name in names}
    (OUT / 'evidence/validation.json').write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('checks', 'foundation_test_output', 'artifact_hashes', 'totals')}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    main()
