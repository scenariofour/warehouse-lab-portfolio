"""Independent source reconciliation, exact lineage and deterministic replay."""
from collections import Counter, defaultdict
import csv
from decimal import Decimal
import hashlib
import itertools
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/data-quality/registry'
sys.path.insert(0, str(ROOT / 'scripts/data_quality'))
from contract import validate_registry


def read(name):
    with (ROOT / 'data/raw' / (name + '.csv')).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=',' if name in ('Random_Storage', 'Storage_Location') else ';'))


def normalized(value, customer=False):
    value = value.strip()
    if not value: return ''
    n = Decimal(value)
    if customer and value in ('35','45','55','65','75','85','95','105','115','125'): n /= 10
    return format(n.normalize(), 'f')


def csv_rows(name):
    with (OUT / name).open(newline='') as f: return list(csv.DictReader(f))


def expand(line):
    return {i for first, last in line['record_ranges'] for i in range(first, last+1)}


class RegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.issues = json.loads((OUT / 'issues.json').read_text())
        cls.by_id = {r['issue_id']: r for r in cls.issues}
        cls.c, cls.p, cls.g, cls.prod = read('Customer_Order'), read('Picking_Wave'), read('Storage_Location'), read('Product')
        cls.db = sqlite3.connect(':memory:')
        cls.db.executescript('CREATE TABLE c(row INT, wave TEXT, ref TEXT, size TEXT, qty INT); CREATE TABLE p(row INT, wave TEXT, ref TEXT, size TEXT, qty INT, loc TEXT); CREATE TABLE g(loc TEXT);')
        cls.db.executemany('INSERT INTO c VALUES(?,?,?,?,?)', [(i, r['waveNumber'].strip(), r['Reference'].strip(), normalized(r['Size (US)'], True), int(r['quantity (units)'])) for i,r in enumerate(cls.c,2)])
        cls.db.executemany('INSERT INTO p VALUES(?,?,?,?,?,?)', [(i,r['waveNumber'].strip(),r['reference'].strip(),normalized(r['Size (US)']),int(r['quantityToPick (units)']),r['locations'].strip()) for i,r in enumerate(cls.p,2)])
        cls.db.executemany('INSERT INTO g VALUES(?)', [(r['originalLocation'].strip(),) for r in cls.g])
        cls.db.executescript('CREATE VIEW cq AS SELECT wave,ref,size,SUM(qty) q FROM c GROUP BY wave,ref,size; CREATE VIEW pq AS SELECT wave,ref,size,SUM(qty) q FROM p GROUP BY wave,ref,size;')

    @classmethod
    def tearDownClass(cls): cls.db.close()

    def value(self, issue_id, metric_id):
        return next(m['affected_count'] for m in self.by_id[issue_id]['metrics'] if m['metric_id'] == metric_id)

    def ids(self, issue_id, source, role=None):
        return set().union(*(expand(line) for line in self.by_id[issue_id]['source_lineage'] if line['source_file'] == 'data/raw/' + source + '.csv' and (role is None or line['role'] == role)))

    def test_contract_sources_review_and_hashes(self):
        validate_registry(self.issues)
        self.assertEqual(len(self.issues), 14)
        manifest = json.loads((OUT / 'manifest.json').read_text())
        publisher = json.loads((ROOT / 'data/manifest.json').read_text())
        self.assertEqual(len(manifest['source_hashes']), 21)
        for entry in publisher['files']:
            name = entry['filename']; actual = hashlib.sha256((ROOT / 'data/raw' / name).read_bytes()).hexdigest()
            self.assertEqual(actual, entry['content_details']['sha256_hash'])
            self.assertEqual(actual, manifest['source_hashes'][name])
        for name, expected in manifest['outputs'].items():
            self.assertEqual(hashlib.sha256((OUT / name).read_bytes()).hexdigest(), expected)
        for r in self.issues:
            self.assertEqual(r['root_cause'], 'UNKNOWN')
            self.assertEqual(r['review'], {'state': 'PENDING','reviewer': None,'evidence_ref': None})
            self.assertNotIn(r['status'], ('Resolved','Accepted Limitation'))
            self.assertIsNone(r['treatment']['before_ref']); self.assertIsNone(r['treatment']['after_ref'])
            for line in r['source_lineage']:
                path = ROOT / line['source_file']
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), line['sha256'])
                if path.suffix == '.csv':
                    rows = read(path.stem)
                    self.assertLessEqual(max(expand(line)), len(rows)+1)
                    self.assertTrue(set(line['columns']) <= rows[0].keys())
            for evidence in r['evidence_refs']: self.assertTrue((ROOT/evidence).is_file(), evidence)

    def test_independent_sql_primary_metrics(self):
        scalar = lambda sql: self.db.execute(sql).fetchone()[0]
        self.assertEqual(scalar('SELECT SUM(qty) FROM c'), 228195)
        self.assertEqual(scalar('SELECT SUM(qty) FROM p'), 215192)
        gap = scalar('SELECT SUM(MAX(cq.q-COALESCE(pq.q,0),0)) FROM cq LEFT JOIN pq USING(wave,ref,size)')
        self.assertEqual(gap, 13003); self.assertEqual(gap, self.value('DQ-RECON-001','gap_units'))
        self.assertEqual(scalar('SELECT SUM(MAX(pq.q-COALESCE(cq.q,0),0)) FROM pq LEFT JOIN cq USING(wave,ref,size)'),0)
        unmatched = scalar('SELECT SUM(qty) FROM p LEFT JOIN g USING(loc) WHERE g.loc IS NULL')
        self.assertEqual(unmatched,23609); self.assertEqual(unmatched,self.value('DQ-LOC-001','unmapped_picking_units'))
        expected_ids = {r[0] for r in self.db.execute('SELECT p.row FROM p LEFT JOIN g USING(loc) WHERE g.loc IS NULL')}
        self.assertEqual(self.ids('DQ-LOC-001','Picking_Wave','AFFECTED'),expected_ids)
        expected_customer = {r[0] for r in self.db.execute('SELECT c.row FROM c JOIN cq USING(wave,ref,size) LEFT JOIN pq USING(wave,ref,size) WHERE cq.q>COALESCE(pq.q,0)')}
        self.assertEqual(self.ids('DQ-RECON-001','Customer_Order'),expected_customer)

    def test_complete_reconciliation_lineage(self):
        customer_seen, picking_seen = [], []
        for row in csv_rows('reconciliation.csv'):
            key = (row['wave'],row['reference'],row['size'])
            ci = [int(i) for i in row['customer_rows'].split('|') if i]
            pi = [int(i) for i in row['picking_rows'].split('|') if i]
            for i in ci:
                r=self.c[i-2]; self.assertEqual((r['waveNumber'].strip(),r['Reference'].strip(),normalized(r['Size (US)'],True)),key)
            for i in pi:
                r=self.p[i-2]; self.assertEqual((r['waveNumber'].strip(),r['reference'].strip(),normalized(r['Size (US)'])),key)
            cn=sum(int(self.c[i-2]['quantity (units)']) for i in ci)
            pn=sum(int(self.p[i-2]['quantityToPick (units)']) for i in pi)
            self.assertEqual((cn,pn,cn-pn,min(cn,pn)),tuple(int(row[k]) for k in ('customer_units','picking_units','gap_units','matched_units')))
            customer_seen.extend(ci);picking_seen.extend(pi)
        self.assertEqual(sorted(customer_seen),list(range(2,len(self.c)+2)))
        self.assertEqual(sorted(picking_seen),list(range(2,len(self.p)+2)))

    def test_abc_and_customer_ambiguities(self):
        source={r['Reference'].strip():r['ABCCOD'].strip() for r in self.prod}
        counts=Counter(); ref_ids=defaultdict(list)
        for i,r in enumerate(self.c,2):counts[r['Reference'].strip()]+=int(r['quantity (units)']);ref_ids[r['Reference'].strip()].append(i)
        running=0;expected={}
        for ref,n in sorted(counts.items(),key=lambda x:(-x[1],x[0])):
            expected[ref]='A' if running < Decimal('0.8')*228195 else 'B' if running < Decimal('0.95')*228195 else 'C'
            running+=n
        mismatch=sum(expected[k]!=source[k] for k in counts)
        self.assertEqual(mismatch,96);self.assertEqual(mismatch,self.value('DQ-ABC-001','disagreeing_references'))
        for r in csv_rows('classification.csv'):
            ref=r['reference'];self.assertEqual(r['derived_abc'],expected[ref]);self.assertEqual(r['published_abc'],source[ref])
            self.assertEqual(int(r['customer_units']),counts[ref]);self.assertEqual(r['customer_rows'],'|'.join(map(str,ref_ids[ref])))
        for source_name,issue_id,qty in [('Customer_Order','DQ-DUP-CUSTOMER','quantity (units)'),('Picking_Wave','DQ-DUP-PICKING','quantityToPick (units)')]:
            rows=self.c if source_name=='Customer_Order' else self.p
            seen=set(); ids=[]
            for i,r in enumerate(rows,2):
                signature=tuple(r.values())
                if signature in seen:ids.append(i)
                seen.add(signature)
            self.assertEqual(set(ids),self.ids(issue_id,source_name,'AFFECTED'))
            self.assertEqual(len(ids),self.value(issue_id,'repeat_rows'))
            self.assertEqual(sum(int(rows[i-2][qty]) for i in ids),self.value(issue_id,'repeat_units'))
        self.assertEqual(self.value('DQ-SIZE-002','missing_size_rows'),16)
        self.assertEqual(self.value('DQ-SIZE-002','missing_size_units'),20)
        self.assertEqual(self.value('DQ-SIZE-001','mapped_rows'),sum(r['Size (US)'].strip() in ('35','45','55','65','75','85','95','105','115','125') for r in self.c))
        self.assertEqual(self.value('DQ-QTY-001','zero_quantity_rows'),33)
        by_order=defaultdict(set)
        for r in self.c:by_order[r['orderNumber'].strip()].add(r['waveNumber'].strip())
        self.assertEqual(self.value('DQ-ID-001','multi_wave_order_numbers'),sum(len(w)>1 for w in by_order.values()))
        for issue in ('DQ-STOCK-001','DQ-LAYOUT-001'):
            self.assertIsNone(self.by_id[issue]['metrics'][0]['affected_count'])
            self.assertIsNone(self.by_id[issue]['metrics'][0]['denominator'])

    def test_policy_cells_and_pairs(self):
        locations={r['originalLocation'].strip() for r in self.g}; masters={r['Reference'].strip() for r in self.prod}
        stocks={};excluded=[];unknown=[];total=0
        for policy in ('Random','Class_Based','Dedicated','Hybrid'):
            counter=Counter()
            for i,r in enumerate(read(policy+'_Storage'),2):
                loc=r.get('originalLocation',r.get('Location')).strip()
                for col,v in r.items():
                    if not (col.startswith('col_') or col.isdigit()) or not v.strip():continue
                    ref,s=v.strip().split(';');total+=1
                    cell={'policy':policy,'source_row':str(i),'column':col,'location':loc,'reference':ref,'token':s}
                    if loc in locations:counter[(ref,normalized(s))]+=1
                    else:excluded.append(cell)
                    if ref not in masters:unknown.append(cell)
            stocks[policy]=counter;self.assertEqual(sum(counter.values()),41256)
        self.assertEqual(csv_rows('excluded_cells.csv'),excluded)
        self.assertEqual(csv_rows('unknown_reference_cells.csv'),unknown)
        self.assertEqual(self.value('DQ-LOC-002','excluded_cells'),2610)
        self.assertEqual(self.value('DQ-MASTER-001','unknown_reference_cells'),len(unknown))
        for r in csv_rows('policy_skus.csv'):
            self.assertEqual(int(r['retained_encoded_cells']),stocks[r['policy']][r['reference'],r['size']])
        for r in csv_rows('policy_pairs.csv'):
            a,b=stocks[r['policy_a']],stocks[r['policy_b']];keys=a.keys()|b.keys()
            self.assertEqual(int(r['union_skus']),len(keys))
            self.assertEqual(int(r['differing_skus']),sum(a[k]!=b[k] for k in keys))
            self.assertEqual(int(r['l1_cell_difference']),sum(abs(a[k]-b[k]) for k in keys))
            self.assertGreater(int(r['differing_skus']),0)
        self.assertEqual(self.value('DQ-EXP-001','unequal_policy_pairs'),6)
        for issue in ('DQ-LOC-002','DQ-MASTER-001'):self.assertEqual(self.by_id[issue]['metrics'][0]['denominator'],total)

    def test_deterministic_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            run=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/data_quality/build_registry.py'),'--output-dir',tmp],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertEqual(sorted(p.name for p in Path(tmp).iterdir()),sorted(p.name for p in OUT.iterdir() if p.name != 'README.md'))
            for p in Path(tmp).iterdir():self.assertEqual(p.read_bytes(),(OUT/p.name).read_bytes(),p.name)


if __name__=='__main__':unittest.main()
