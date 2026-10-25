#!/usr/bin/env python3
"""Compile verified public evidence into deterministic presentation geometry.

No raw warehouse records are read. XY locations and curve control points are
editorial layout only; no distance, direction, weight or causality is encoded.
"""
import argparse
from collections import defaultdict
import csv
import hashlib
from html import escape
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUTS = {
    'evidence': 'docs/data-quality/advanced/public/issue_evidence.csv',
    'decisions': 'docs/data-quality/advanced/public/decision_evidence.csv',
    'issues': 'docs/data-quality/tableau/public/issues.csv',
    'metrics': 'docs/data-quality/tableau/public/issue_metrics.csv',
}
ROLES = {'AFFECTED', 'CONTRIBUTING_POPULATION', 'DEFINITION_EVIDENCE'}
DECISIONS = ['MEASUREMENT_BASELINE', 'SOURCE_DEFINITION', 'SPATIAL_FEASIBILITY',
             'EXPERIMENT_DESIGN', 'SLOTTING_HYPOTHESIS']
SHORT = ['Quantity gap', 'Unmapped picks', 'ABC disagreement', 'Unequal inventory',
         'Stock meaning', 'Floor connectivity', 'Repeated orders', 'Repeated picks',
         'Size encoding', 'Missing sizes', 'Zero quantities', 'Excluded cells',
         'Master coverage', 'Order identity']
CONTEXT = ['title', 'review_state', 'business_decision', 'kpi_at_risk',
           'business_mechanism', 'competing_explanations', 'next_evidence_request',
           'recommendation', 'evidence_class', 'evidence_ref', 'claim_limit',
           'source_count', 'lineage_record_count']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_sources(root):
    result = {}
    for name, relative in INPUTS.items():
        path = root / relative
        manifest = json.loads((path.parent.parent / 'manifest.json').read_text())
        if path.name not in manifest['public_allowlist']:
            raise ValueError(f'Not allowlisted: {relative}')
        table = manifest['tables'][path.stem]
        if sha(path) != table['sha256']:
            raise ValueError(f'Input hash changed: {relative}; review the source contract first')
        with path.open(encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            if set(reader.fieldnames) != set(table.get('fields', table.get('columns', []))):
                raise ValueError(f'Input schema changed: {relative}')
            result[name] = list(reader)
    return result


def make_model(evidence, decisions, issues, metrics):
    if any(r['lineage_role'] not in ROLES for r in evidence):
        raise ValueError('Unknown lineage role')
    if len(evidence) != 35:
        raise ValueError('Expected exactly 35 lineage records')
    ids = [r['issue_id'] for r in decisions]
    sources = sorted({r['source_id'] for r in evidence})
    pairs = defaultdict(list)
    for row in evidence:
        if row['issue_id'] not in ids:
            raise ValueError('Unregistered issue in lineage')
        pairs[(row['issue_id'], row['source_id'])].append(row)
    if (len(ids), len(set(ids)), len(sources), len(pairs)) != (14, 14, 11, 33):
        raise ValueError('Expected 14 issues, 11 sources and 33 occupied pairs')
    if len({r['issue_source_id'] for r in evidence}) != 35:
        raise ValueError('Lineage IDs must be unique')
    issue_lookup = {r['issue_id']: r for r in issues}
    if set(issue_lookup) != set(ids) or len(issues) != 14:
        raise ValueError('Issue registry does not match decision issues')
    if set(r['decision_category'] for r in decisions) != set(DECISIONS):
        raise ValueError('Decision category domain changed')
    if any(r['decision_category'] != issue_lookup[r['issue_id']]['business_decision_category'] for r in decisions):
        raise ValueError('Decision categories disagree with issue registry')
    if any(r['issue_id'] not in ids for r in metrics):
        raise ValueError('Metric points outside the issue registry')
    nodes = []

    def node(key, kind, label, short, x, y):
        nodes.append(dict(node_id=key, node_type=kind, label=label, short_label=short,
                          x=round(x, 6), y=round(y, 6), label_x=round(x+17, 6),
                          label_y=round(y+4, 6), label_align='left',
                          shape={'SOURCE': 'diamond', 'ISSUE': 'circle', 'DECISION': 'square'}[kind],
                          issue_id='', source_id='', decision_category=''))

    # Fixed editorial arrangement; source/issue order is not a metric.
    for i, source in enumerate(sources):
        node('S:'+source, 'SOURCE', source, source.replace('_', ' ').rsplit('.', 1)[0],
             126-46*math.sin(math.pi*i/10), 100+55*i)
        nodes[-1]['source_id'] = source
    for i, row in enumerate(decisions):
        angle = math.radians(-90+i*360/14)
        node(row['issue_id'], 'ISSUE', row['title'], SHORT[i],
             514+173*math.cos(angle), 382+247*math.sin(angle))
        nodes[-1]['issue_id'] = row['issue_id']
        nodes[-1]['decision_category'] = row['decision_category']
        if i >= 7:
            nodes[-1]['label_x'] = round(nodes[-1]['x']-17, 6)
            nodes[-1]['label_align'] = 'right'
    for i, category in enumerate(DECISIONS):
        node('D:'+category, 'DECISION', category.replace('_', ' ').title(),
             category.replace('_', ' ').title(), 846+18*math.sin(i*math.pi/4), 150+i*116)
        nodes[-1]['decision_category'] = category
    lookup = {n['node_id']: n for n in nodes}
    edges, roles, points = [], [], []

    def edge(key, kind, a, b, issue, source='', category='', lineage=()):
        start, end = lookup[a], lookup[b]
        dx = end['x']-start['x']
        # Horizontal tangents give a calm, traceable curve without force layout.
        controls = dict(c1x=round(start['x']+dx*.44, 6), c1y=start['y'],
                        c2x=round(end['x']-dx*.40, 6), c2y=end['y'])
        row = dict(edge_id=key, edge_kind=kind, from_node=a, to_node=b,
                   issue_id=issue, source_id=source, decision_category=category,
                   lineage_ids='|'.join(sorted(r['issue_source_id'] for r in lineage)),
                   roles='|'.join(sorted({r['lineage_role'] for r in lineage})),
                   lineage_count=len(lineage), **controls)
        edges.append(row)
        for r in sorted(lineage, key=lambda r: r['issue_source_id']):
            roles.append(dict(edge_id=key, lineage_id=r['issue_source_id'], issue_id=issue,
                              source_id=source, lineage_role=r['lineage_role']))
        for order in range(41):
            t = order/40
            xy = {axis: round((1-t)**3*start[axis] + 3*(1-t)**2*t*controls['c1'+axis]
                              + 3*(1-t)*t*t*controls['c2'+axis] + t**3*end[axis], 6)
                  for axis in ['x', 'y']}
            points.append(dict(edge_id=key, edge_kind=kind, issue_id=issue, source_id=source,
                               decision_category=category, roles=row['roles'],
                               lineage_count=len(lineage), path_order=order, **xy))

    for index, ((issue, source), lineage) in enumerate(sorted(pairs.items()), 1):
        edge(f'E{index:02}', 'EVIDENCE_ASSOCIATION', 'S:'+source, issue, issue,
             source=source, lineage=lineage)
    for index, r in enumerate(decisions, 1):
        edge(f'D{index:02}', 'DECISION_ASSOCIATION', r['issue_id'], 'D:'+r['decision_category'],
             r['issue_id'], category=r['decision_category'])
    contexts = []
    for r in decisions:
        contexts.append(dict(issue_id=r['issue_id'], decision_category=r['decision_category'],
                             **{k: r[k] for k in CONTEXT if k in r},
                             claim_limit=issue_lookup[r['issue_id']]['residual_uncertainty'],
                             source_count=len({e['source_id'] for e in evidence if e['issue_id'] == r['issue_id']}),
                             lineage_record_count=sum(e['issue_id'] == r['issue_id'] for e in evidence)))
    return dict(nodes=nodes, edges=edges, edge_points=points, lineage_roles=roles,
                issue_context=contexts, issue_metrics=metrics)


def selection_scaffold(model):
    fields = ['focus_issue', 'mark_kind', 'mark_id', 'node_id', 'node_type', 'edge_id',
              'edge_kind', 'issue_id', 'source_id', 'decision_category', 'label', 'roles',
              'lineage_count', 'path_order', 'x', 'y', 'edge_y', 'node_y', 'label_x', 'label_y', 'label_align', 'style_key',
              'is_selected'] + CONTEXT
    output = []
    for focus in ['__ALL__'] + [r['issue_id'] for r in model['issue_context']]:
        selected_edges = {e['edge_id'] for e in model['edges'] if e['issue_id'] == focus or focus == '__ALL__'}
        selected_nodes = {e[k] for e in model['edges'] if e['edge_id'] in selected_edges for k in ['from_node', 'to_node']}

        def mark(kind, identity, values, selected):
            row = dict.fromkeys(fields, '')
            row.update(values, focus_issue=focus, mark_kind=kind, mark_id=identity,
                       is_selected=int(selected))
            row['style_key'] = (row['node_type'] if kind == 'NODE' else row['edge_kind']) + ('_ACTIVE' if selected else '_CONTEXT')
            output.append(row)

        for n in model['nodes']:
            mark('NODE', n['node_id'], {k: n[k] for k in ['node_id', 'node_type', 'issue_id', 'source_id', 'decision_category', 'x', 'y', 'label_x', 'label_y', 'label_align']} |
                 dict(label=n['short_label'], node_y=n['y']), n['node_id'] in selected_nodes)
        for p in model['edge_points']:
            mark('EDGE', p['edge_id'], p | dict(edge_y=p['y']), p['edge_id'] in selected_edges)
        context = next((r for r in model['issue_context'] if r['issue_id'] == focus),
                       dict(title='Choose an investigation question', evidence_class='AI_PROPOSED_REQUIRES_HUMAN_REVIEW'))
        mark('CONTEXT', 'CONTEXT', context, False)
    return output


def static_svg(model):
    paths = []
    lookup = {n['node_id']: n for n in model['nodes']}
    for e in model['edges']:
        a, b = lookup[e['from_node']], lookup[e['to_node']]
        color = '#7fd9c7' if e['edge_kind'] == 'EVIDENCE_ASSOCIATION' else '#deb47b'
        paths.append(f'<path d="M{a["x"]},{a["y"]} C{e["c1x"]},{e["c1y"]} {e["c2x"]},{e["c2y"]} {b["x"]},{b["y"]}" fill="none" stroke="{color}" stroke-opacity=".25"/>')
    for n in model['nodes']:
        color = '#deb47b' if n['node_type'] == 'DECISION' else '#b6f3df'
        x, y = n['x'], n['y']
        shape = f'<circle cx="{x}" cy="{y}" r="5"/>' if n['node_type'] == 'ISSUE' else f'<rect x="{x-4}" y="{y-4}" width="8" height="8" transform="rotate({45 if n["node_type"] == "SOURCE" else 0} {x} {y})"/>'
        paths.append(f'<g fill="{color}">{shape}<text x="{n["label_x"]}" y="{n["label_y"]}" text-anchor="{"end" if n["label_align"] == "right" else "start"}" font-size="10" font-family="sans-serif">{escape(n["short_label"])}</text></g>')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 760" role="img" aria-labelledby="title desc"><title id="title">The Anatomy of a Decision</title><desc id="desc">Registered evidence associations. Positions are editorial, not measured. Decision framing is AI proposed and pending human review.</desc><rect width="1000" height="760" fill="#091720"/>'+''.join(paths)+'</svg>\n'


def build(output, root=ROOT):
    sources = load_sources(root)
    model = make_model(**sources)
    tables = model | dict(tableau_marks=selection_scaffold(model))
    (output/'tableau').mkdir(parents=True, exist_ok=True)
    (output/'assets').mkdir(exist_ok=True)
    metadata = {}
    for name, rows in tables.items():
        columns = list(rows[0])
        for row in rows:
            for value in row.values():
                value = str(value)
                if value.startswith(('=', '+', '@', '\t', '\r')) or '/Users/' in value or 'codCustomer' in value:
                    raise ValueError(f'Unsafe public value in {name}')
        path = output/'tableau'/(name+'.csv')
        with path.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=columns, lineterminator='\n')
            writer.writeheader(); writer.writerows(rows)
        metadata[name] = dict(columns=columns, rows=len(rows), sha256=sha(path))
    # Script-local payload lets the prototype work offline without a fetch server.
    payload = {k: v for k, v in model.items() if k not in ['edge_points']}
    (output/'data.js').write_text('window.CONSTELLATION = '+json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')+';\n', encoding='utf-8')
    (output/'assets/constellation-overview.svg').write_text(static_svg(model), encoding='utf-8')
    manifest = dict(version='M5-anatomy-1', geometry_only=True,
                    encoding='Registered associations; no causality, weights, or measured distances. Decision associations are AI proposed.',
                    generator_sha256=sha(Path(__file__)),
                    inputs={path: sha(root/path) for path in INPUTS.values()},
                    geometry=dict(viewbox=[0, 0, 1000, 760], points_per_edge=41,
                                  curve='cubic Bezier; t=path_order/40', layout='fixed editorial arcs; no metric scaling'),
                    populations=dict(issues=14, sources=11, lineage_records=35,
                                     occupied_issue_source_pairs=33, decision_categories=5, decision_associations=14),
                    null_policy='Blank is absent/unknown, never zero. Context and metrics must not be summed across geometry points.',
                    tables=metadata,
                    attribution='Source: Rodrigo Furlan de Assis, Mendeley Data v1, DOI 10.17632/pf2w725pw3.1, CC BY 4.0. Interpretation: AI proposed, pending human review.')
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT/'docs/control-tower/anatomy')
    args = parser.parse_args()
    result = build(args.output_dir)
    print(json.dumps(result['populations'], sort_keys=True))
