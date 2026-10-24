"""Standard-library validator for the JSON Schema subset used by our issue contract.

Not a general JSON Schema engine. Schema evolution must extend this validator/tests
or use a full standards implementation before adding new validation keywords.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / 'docs/data-quality/issue-record.schema.json').read_text())


def validate_shape(value, schema, path='$'):
    kinds = schema.get('type', [])
    kinds = [kinds] if isinstance(kinds, str) else kinds
    types = {'object': dict, 'array': list, 'string': str, 'integer': int, 'null': type(None)}
    if kinds and not any(type(value) is types[k] for k in kinds):
        raise ValueError(f'{path}: expected {kinds}')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(f'{path}: invalid enum')
    if isinstance(value, dict):
        missing = set(schema.get('required', [])) - value.keys()
        extra = value.keys() - schema.get('properties', {}).keys()
        if missing or (schema.get('additionalProperties') is False and extra):
            raise ValueError(f'{path}: missing {missing}, extra {extra}')
        for key, item in value.items():
            if key in schema.get('properties', {}):
                validate_shape(item, schema['properties'][key], f'{path}.{key}')
    if isinstance(value, (str, list)):
        lo, hi = ('minLength', 'maxLength') if isinstance(value, str) else ('minItems', 'maxItems')
        if len(value) < schema.get(lo, 0) or len(value) > schema.get(hi, float('inf')):
            raise ValueError(f'{path}: length out of bounds')
        if isinstance(value, list):
            for i, item in enumerate(value):
                validate_shape(item, schema.get('items', {}), f'{path}[{i}]')
    if type(value) is int and value < schema.get('minimum', float('-inf')):
        raise ValueError(f'{path}: below minimum')


def validate_issue(issue):
    validate_shape(issue, SCHEMA)
    if not issue['issue_id'].startswith('DQ-'):
        raise ValueError('Issue ID must start DQ-')
    metric_ids = [m['metric_id'] for m in issue['metrics']]
    if len(metric_ids) != len(set(metric_ids)):
        raise ValueError('Duplicate metric ID')
    for metric in issue['metrics']:
        n, d = metric['affected_count'], metric['denominator']
        if n is not None and d is not None and n > d:
            raise ValueError('Affected count exceeds denominator')
        if d == 0 and n not in (None, 0):
            raise ValueError('Nonzero count with empty population')
    for lineage in issue['source_lineage']:
        h = lineage['sha256']
        if len(h) != 64 or any(c not in '0123456789abcdef' for c in h):
            raise ValueError('Invalid source hash')
        p = Path(lineage['source_file'])
        if p.is_absolute() or '..' in p.parts or not str(p).startswith('data/raw/'):
            raise ValueError('Lineage must reference a repository raw source')
        last = 1
        for first, end in lineage['record_ranges']:
            if first > end or first <= last:
                raise ValueError('Ranges must be ordered, disjoint, inclusive')
            last = end
        if not lineage['record_ranges'] and lineage['role'] != 'DEFINITION_EVIDENCE':
            raise ValueError('CSV populations require record ordinals')
    review = issue['review']
    if review['state'] == 'APPROVED' and not (review['reviewer'] and review['evidence_ref']):
        raise ValueError('Human approval needs reviewer and evidence')
    if review['state'] == 'PENDING' and (review['reviewer'] or review['evidence_ref']):
        raise ValueError('Pending review cannot imply sign-off')
    if issue['status'] in ('Resolved', 'Accepted Limitation') and review['state'] != 'APPROVED':
        raise ValueError('Closure requires human review')
    t = issue['treatment']
    if t['kind'] == 'CORRECTION':
        if not all(t[k] for k in ('approval_ref', 'before_ref', 'after_ref')) or review['state'] != 'APPROVED':
            raise ValueError('Correction requires approval and before/after evidence')
    elif any(t[k] is not None for k in ('approval_ref', 'before_ref', 'after_ref')):
        raise ValueError('Only approved corrections use before/after treatment fields')
    return issue


def validate_registry(issues):
    ids = [r['issue_id'] for r in issues]
    if not issues or len(ids) != len(set(ids)):
        raise ValueError('Registry must be nonempty with unique IDs')
    for issue in issues:
        validate_issue(issue)
