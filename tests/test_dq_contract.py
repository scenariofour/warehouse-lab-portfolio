"""Contract mutation tests only; no generated warehouse scenario records."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts/data_quality'))
from contract import SCHEMA, validate_issue, validate_registry


def example():
    return {
        'contract_version': '1.0', 'issue_id': 'DQ-TEST', 'title': 'Contract example',
        'category': 'RECONCILIATION', 'data_origin': 'REAL_SOURCE_DERIVED',
        'source_lineage': [{'source_file': 'data/raw/Customer_Order.csv', 'sha256': 'a'*64,
                            'record_ranges': [[2, 3]], 'columns': ['quantity (units)'], 'role': 'AFFECTED'}],
        'detection_rule': 'Compare quantities by a declared key',
        'metrics': [{'metric_id': 'gap', 'affected_count': 1, 'unit': 'published customer units',
                     'population': 'customer demand', 'denominator': 2, 'denominator_definition': 'sum of quantities',
                     'calculation': 'sum positive key gaps', 'additivity': 'WITHIN_METRIC_ONLY'}],
        'severity': 'HIGH', 'confidence': {'arithmetic': 'HIGH', 'interpretation': 'UNKNOWN', 'rationale': 'Example only'},
        'root_cause': 'UNKNOWN', 'hypothesized_causes': ['Extract scope'],
        'business_decision_category': 'MEASUREMENT_BASELINE', 'business_decision': 'Define eligible demand',
        'potential_consequences': ['Misleading service rate'], 'resolution_options': ['Seek source definition'],
        'status': 'Unresolved — Source Clarification Required',
        'review': {'state': 'PENDING', 'reviewer': None, 'evidence_ref': None},
        'evidence_refs': ['contract-only example'], 'residual_uncertainty': 'Cause unknown',
        'treatment': {'kind': 'RETENTION', 'approval_ref': None, 'before_ref': None, 'after_ref': None, 'description': 'Retained'},
    }


class ContractTests(unittest.TestCase):
    def test_valid_and_unknown_metrics(self):
        validate_issue(example())
        r = example(); r['metrics'][0]['affected_count'] = None; r['metrics'][0]['denominator'] = None
        validate_issue(r)

    def test_each_required_field(self):
        for key in SCHEMA['required']:
            with self.subTest(key=key):
                r = example(); del r[key]
                with self.assertRaises(ValueError): validate_issue(r)

    def test_malformed_mutations(self):
        mutations = [
            lambda r: r.update(extra='unexpected'),
            lambda r: r.update(data_origin='SYNTHETIC'),
            lambda r: r.update(status='UNKNOWN'),
            lambda r: r['metrics'][0].update(affected_count=-1),
            lambda r: r['metrics'][0].update(affected_count=3),
            lambda r: r['metrics'][0].update(affected_count=True),
            lambda r: r['metrics'][0].update(denominator=0),
            lambda r: r['source_lineage'][0].update(sha256='bad'),
            lambda r: r['source_lineage'][0].update(source_file='../private.csv'),
            lambda r: r['source_lineage'][0].update(record_ranges=[[3, 2]]),
            lambda r: r['source_lineage'][0].update(record_ranges=[[2, 3], [3, 4]]),
            lambda r: r['source_lineage'][0].update(record_ranges=[]),
            lambda r: r.update(evidence_refs=[]),
            lambda r: r.update(status='Resolved'),
            lambda r: r.update(status='Accepted Limitation'),
            lambda r: r['review'].update(state='APPROVED'),
            lambda r: r['review'].update(reviewer='Unsubstantiated reviewer'),
            lambda r: r['treatment'].update(kind='CORRECTION'),
            lambda r: r['treatment'].update(after_ref='invented result'),
            lambda r: r['metrics'].append(copy.deepcopy(r['metrics'][0])),
        ]
        for i, mutation in enumerate(mutations):
            with self.subTest(mutation=i):
                r = example(); mutation(r)
                with self.assertRaises(ValueError): validate_issue(r)

    def test_closure_and_correction_evidence(self):
        r = example(); r['status'] = 'Resolved'
        r['review'] = {'state': 'APPROVED', 'reviewer': 'Contract test human', 'evidence_ref': 'test approval'}
        r['treatment'].update(kind='CORRECTION', approval_ref='test approval', before_ref='test before', after_ref='test after')
        validate_issue(r)
        for key in ('approval_ref', 'before_ref', 'after_ref'):
            bad = copy.deepcopy(r); bad['treatment'][key] = None
            with self.assertRaises(ValueError): validate_issue(bad)

    def test_unique_registry_ids(self):
        with self.assertRaises(ValueError): validate_registry([example(), example()])
        with self.assertRaises(ValueError): validate_registry([])


if __name__ == '__main__': unittest.main()
