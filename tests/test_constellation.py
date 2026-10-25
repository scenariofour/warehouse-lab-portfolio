"""M5 geometry is a reproducible presentation of registered associations."""
import collections
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/control_tower/build_constellation.py'


def read(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


class ConstellationIntegrity(unittest.TestCase):
    def generate(self, output):
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--output-dir', str(output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads((output / 'manifest.json').read_text())

    def test_registered_populations_and_decision_partition(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); manifest = self.generate(out)
            nodes = read(out / 'tableau/nodes.csv')
            self.assertEqual(collections.Counter(n['node_type'] for n in nodes), {'SOURCE': 11, 'ISSUE': 14, 'DECISION': 5})
            self.assertEqual(manifest['populations'], {'issues': 14, 'sources': 11, 'lineage_records': 35, 'occupied_issue_source_pairs': 33, 'decision_categories': 5, 'decision_associations': 14})
            decisions = read(ROOT / 'docs/data-quality/advanced/public/decision_evidence.csv')
            actual = {r['issue_id']: r['decision_category'] for r in read(out / 'tableau/edges.csv') if r['edge_kind'] == 'DECISION_ASSOCIATION'}
            self.assertEqual(actual, {r['issue_id']: r['decision_category'] for r in decisions})

    def test_relationship_coverage_and_each_original_role(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); self.generate(out)
            raw = read(ROOT / 'docs/data-quality/advanced/public/issue_evidence.csv')
            roles = read(out / 'tableau/lineage_roles.csv')
            self.assertEqual({(r['lineage_id'], r['issue_id'], r['source_id'], r['lineage_role']) for r in roles},
                             {(r['issue_source_id'], r['issue_id'], r['source_id'], r['lineage_role']) for r in raw})
            edges = [e for e in read(out / 'tableau/edges.csv') if e['edge_kind'] == 'EVIDENCE_ASSOCIATION']
            self.assertEqual({(e['issue_id'], e['source_id']) for e in edges}, {(r['issue_id'], r['source_id']) for r in raw})
            self.assertEqual(sum(int(e['lineage_count']) for e in edges), 35)
            self.assertEqual(sum(e['roles'] == 'AFFECTED|CONTRIBUTING_POPULATION' for e in edges), 2)

    def test_paths_have_exact_node_endpoints_and_independent_bezier_midpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); self.generate(out)
            nodes = {r['node_id']: r for r in read(out / 'tableau/nodes.csv')}
            paths = collections.defaultdict(list)
            for row in read(out / 'tableau/edge_points.csv'): paths[row['edge_id']].append(row)
            for edge in read(out / 'tableau/edges.csv'):
                points = paths[edge['edge_id']]; a, b = nodes[edge['from_node']], nodes[edge['to_node']]
                self.assertEqual([int(p['path_order']) for p in points], list(range(41)))
                for field in ['x', 'y']:
                    self.assertEqual(float(points[0][field]), float(a[field]))
                    self.assertEqual(float(points[-1][field]), float(b[field]))
                    midpoint = (float(a[field]) + 3*float(edge['c1'+field]) + 3*float(edge['c2'+field]) + float(b[field])) / 8
                    self.assertAlmostEqual(float(points[20][field]), midpoint, places=4)
                self.assertTrue(all(0 <= float(p['x']) <= 1000 and 0 <= float(p['y']) <= 760 for p in points))

    def test_selection_scaffold_preserves_context_and_only_registered_neighbors(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); self.generate(out)
            rows = read(out / 'tableau/tableau_marks.csv')
            focus = [r for r in rows if r['focus_issue'] == 'DQ-EXP-001']
            self.assertEqual(len([r for r in focus if r['mark_kind'] == 'NODE']), 30)
            selected = {r['source_id'] for r in focus if r['mark_kind'] == 'NODE' and r['node_type'] == 'SOURCE' and r['is_selected'] == '1'}
            self.assertEqual(selected, {'Random_Storage.csv', 'Class_Based_Storage.csv', 'Dedicated_Storage.csv', 'Hybrid_Storage.csv', 'Storage_Location.csv'})
            self.assertEqual(len([r for r in focus if r['mark_kind'] == 'EDGE' and r['is_selected'] == '1']), 6*41)
            self.assertEqual(len([r for r in focus if r['mark_kind'] == 'CONTEXT']), 1)
            contexts = read(out / 'tableau/issue_context.csv')
            self.assertEqual(next(r for r in contexts if r['issue_id'] == 'DQ-STOCK-001')['evidence_class'], 'AI_PROPOSED_REQUIRES_HUMAN_REVIEW')

    def test_outputs_are_byte_deterministic_and_inputs_untouched(self):
        inputs = [ROOT / 'docs/data-quality/advanced/public/issue_evidence.csv', ROOT / 'docs/data-quality/advanced/public/decision_evidence.csv', ROOT / 'docs/GATE_REVIEWS.json', ROOT / 'docs/control-tower/index.html']
        before = [p.read_bytes() for p in inputs]
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            self.generate(Path(a)); self.generate(Path(b))
            files = [p.relative_to(a) for p in Path(a).rglob('*') if p.is_file()]
            self.assertGreater(len(files), 7)
            for p in files: self.assertEqual((Path(a)/p).read_bytes(), (Path(b)/p).read_bytes(), str(p))
        self.assertEqual(before, [p.read_bytes() for p in inputs])

    def test_import_schemas_and_values_are_public_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); manifest = self.generate(out)
            for name, schema in manifest['tables'].items():
                rows = read(out / 'tableau' / (name+'.csv'))
                self.assertEqual(list(rows[0]), schema['columns'])
                for row in rows:
                    for value in row.values():
                        self.assertFalse(value.startswith(('=', '+', '@', '\t', '\r')))
                        self.assertNotIn('/Users/', value); self.assertNotIn('codCustomer', value)
                self.assertEqual(hashlib.sha256((out/'tableau'/(name+'.csv')).read_bytes()).hexdigest(), schema['sha256'])

    def test_checked_in_exports_are_fresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); self.generate(out)
            committed = ROOT / 'docs/control-tower/anatomy'
            for path in out.rglob('*'):
                if path.is_file():
                    self.assertEqual(path.read_bytes(), (committed/path.relative_to(out)).read_bytes(), str(path.relative_to(out)))

    def test_metrics_retain_units_denominators_and_nonadditivity(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); self.generate(out)
            self.assertEqual(read(out/'tableau/issue_metrics.csv'), read(ROOT/'docs/data-quality/tableau/public/issue_metrics.csv'))
            self.assertEqual(len(read(out/'tableau/issue_metrics.csv')), 18)

    def test_unknown_roles_and_changed_populations_are_rejected(self):
        spec = importlib.util.spec_from_file_location('constellation', SCRIPT)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        sources = module.load_sources(ROOT)
        with self.assertRaisesRegex(ValueError, 'role'):
            module.make_model([{**r, 'lineage_role': 'CAUSAL'} if i == 0 else r for i, r in enumerate(sources['evidence'])], sources['decisions'], sources['issues'], sources['metrics'])
        with self.assertRaisesRegex(ValueError, '35'):
            module.make_model(sources['evidence'][:-1], sources['decisions'], sources['issues'], sources['metrics'])


if __name__ == '__main__': unittest.main()
