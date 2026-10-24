"""CSV consumer tests: grains, aggregates, nulls, public boundaries and replay."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/data-quality/tableau'
REG = ROOT / 'docs/data-quality/registry'


def rows(name, scope='internal'):
    with (OUT / scope / (name + '.csv')).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


class TableauTests(unittest.TestCase):
    def test_keys_headers_grains_and_foreign_keys(self):
        manifest=json.loads((OUT/'manifest.json').read_text())
        issue_ids={r['issue_id'] for r in rows('issues')}
        self.assertEqual(len(issue_ids),14)
        for name,spec in manifest['tables'].items():
            records=rows(name)
            self.assertEqual(len(records),spec['rows'])
            self.assertEqual(list(records[0]),spec['columns'])
            keys=[tuple(r[k] for k in spec['primary_key']) for r in records]
            self.assertTrue(all(all(k) for k in keys));self.assertEqual(len(keys),len(set(keys)),name)
            self.assertTrue({'category','status','unit','data_origin','evidence_ref'} <= records[0].keys())
            self.assertEqual(hashlib.sha256((OUT/'internal'/(name+'.csv')).read_bytes()).hexdigest(),spec['sha256'])
            for r in records:
                if 'issue_id' in r:self.assertIn(r['issue_id'],issue_ids)
                self.assertTrue(all(len(v) <= 4096 for v in r.values()), name)
                self.assertEqual(r['data_origin'],'REAL_SOURCE_DERIVED')
                self.assertTrue((ROOT/r['evidence_ref'].split('#')[0]).is_file())
        self.assertEqual(manifest['registry_manifest_sha256'],hashlib.sha256((REG/'manifest.json').read_bytes()).hexdigest())

    def test_metric_identity_and_missing_treatments(self):
        issues=json.loads((REG/'issues.json').read_text())
        exported={r['metric_key']:r for r in rows('issue_metrics')}
        self.assertEqual(len(exported),sum(len(r['metrics']) for r in issues))
        for issue in issues:
            for m in issue['metrics']:
                r=exported[issue['issue_id']+':'+m['metric_id']]
                for key in ('affected_count','denominator'):
                    self.assertEqual(r[key],'' if m[key] is None else str(m[key]))
                for key in ('unit','population','denominator_definition','calculation','additivity'):
                    self.assertEqual(r[key],m[key])
                self.assertEqual(r['cross_issue_sum_allowed'],'FALSE')
        for r in rows('issues'):
            for key in ('before_ref','after_ref','approval_ref','reviewer','review_evidence_ref'):self.assertEqual(r[key],'')
            self.assertEqual(r['review_state'],'PENDING')
        for r in rows('decision_impacts'):
            self.assertEqual(r['measured_financial_impact'],'')
            self.assertEqual(r['decision_readiness'],'SOURCE_CLARIFICATION_REQUIRED')

    def test_detail_measures_and_population_totals(self):
        gaps=rows('reconciliation_detail')
        self.assertEqual(len(gaps),5242);self.assertEqual(sum(int(r['gap_units']) for r in gaps),13003)
        self.assertTrue(all(int(r['customer_units'])-int(r['picking_units'])==int(r['gap_units'])>0 for r in gaps))
        unlocated=rows('unmapped_locations')
        self.assertEqual(sum(int(r['picking_units']) for r in unlocated),23609)
        with (ROOT/'data/raw/Picking_Wave.csv').open(encoding='utf-8-sig',newline='') as f:
            raw=list(csv.DictReader(f,delimiter=';'))
        for r in unlocated:
            selector=json.loads(r['source_selector'])
            selected=[v for v in raw if v['locations'].strip()==selector['stripped_locations_equals']]
            self.assertEqual(len(selected),int(r['picking_record_count']))
            self.assertEqual(sum(int(v['quantityToPick (units)']) for v in selected),int(r['picking_units']))
        abc=rows('classification_detail')
        self.assertEqual(len(abc),208);self.assertEqual(sum(int(r['disagrees']) for r in abc),96)
        self.assertEqual(sum(int(r['customer_units']) for r in abc),228195)
        self.assertTrue(all(int(r['disagrees'])==int(r['published_abc']!=r['derived_abc']) for r in abc))
        pairs=rows('policy_pairs');self.assertEqual(len(pairs),6)
        self.assertTrue(all(0<int(r['differing_skus'])<=int(r['union_skus']) for r in pairs))
        closest=next(r for r in pairs if r['policy_a']=='Dedicated' and r['policy_b']=='Hybrid')
        self.assertEqual((int(closest['differing_skus']),int(closest['l1_cell_difference'])),(2468,20726))
        expected={'Random':28392,'Class_Based':17079,'Dedicated':33093,'Hybrid':32201}
        for r in rows('policy_supply'):
            self.assertEqual(int(r['conditional_supply_ceiling']),expected[r['policy']])
            self.assertEqual(int(r['retained_encoded_cells']),41256)
            self.assertEqual(int(r['raw_encoded_cells']),int(r['retained_encoded_cells'])+int(r['excluded_cells']))
            self.assertEqual(int(r['demand_denominator_units']),228195)
        counts={r['source_id']:int(r['source_record_count']) for r in rows('source_counts')}
        self.assertEqual(counts['Customer_Order.csv'],122370);self.assertEqual(counts['Picking_Wave.csv'],215192)
        self.assertEqual(counts['Product.csv'],208);self.assertEqual(counts['Storage_Location.csv'],2292)
        for r in rows('issue_sources'):
            if r['source_id'] in counts:self.assertEqual(int(r['source_record_count']),counts[r['source_id']])
            issues={i['issue_id']:i for i in json.loads((REG/'issues.json').read_text())}
            index=int(r['issue_source_id'].split(':')[-1])-1
            ranges=issues[r['issue_id']]['source_lineage'][index]['record_ranges']
            selected=sum(b-a+1 for a,b in ranges)
            self.assertEqual(r['selected_record_count'],str(selected) if selected else '')
            self.assertEqual(int(r['record_range_count']),len(ranges))

    def test_public_allowlist_and_no_transaction_identifiers(self):
        expected={'issues.csv','issue_metrics.csv','decision_impacts.csv','source_counts.csv'}
        self.assertEqual({p.name for p in (OUT/'public').iterdir()},expected)
        forbidden={'wave','reference','customer_rows','picking_rows','inclusive_record_ranges','source_columns',
                   'location_id','orderNumber','codCustomer','operator','creationDate','product_row'}
        for name in expected:
            records=rows(Path(name).stem,'public')
            self.assertFalse(forbidden & records[0].keys(),name)
            self.assertEqual((OUT/'public'/name).read_bytes(),(OUT/'internal'/name).read_bytes())
        self.assertFalse((OUT/'public'/'issues.json').exists())

    def test_deterministic_csv_and_manifest_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            run=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/data_quality/export_tableau.py'),'--output-dir',tmp],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            generated=[p for p in Path(tmp).rglob('*') if p.is_file()]
            self.assertEqual(len(generated),15)
            for p in generated:self.assertEqual(p.read_bytes(),(OUT/p.relative_to(tmp)).read_bytes(),p.name)


if __name__=='__main__':unittest.main()
