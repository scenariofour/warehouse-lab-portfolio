#!/usr/bin/env python3
"""Local source selectors for a public reconciliation key, including alternatives.

Prints source keys and exact compressed CSV ordinals, never customer/operator fields.
Not an extract for uploading to Tableau Public. Header is logical CSV record 1.
"""
import argparse
import json
import re

from build_advanced import authenticate, opaque
from build_registry import read, size, ranges, digest
from contract import ROOT


def lookup(key):
    authenticate()
    selections = {name: {'ordinals': [], 'quantity': 0} for name in ('CURRENT_INFERRED', 'LITERAL_SIZE', 'CUSTOMER_DEDUP', 'PICKING')}
    raw_key, seen = None, set()
    for ordinal, row in enumerate(read('Customer_Order'), 2):
        w, ref = row['waveNumber'].strip(), row['Reference'].strip()
        signature = tuple(row.values()); repeat = signature in seen; seen.add(signature)
        for label, s, include in [('CURRENT_INFERRED', size(row['Size (US)'], True), True),
                                  ('LITERAL_SIZE', size(row['Size (US)']), True),
                                  ('CUSTOMER_DEDUP', size(row['Size (US)'], True), not repeat)]:
            if opaque('key', w, ref, s) == key:
                raw_key = (w, ref, s)
                if include:
                    selections[label]['ordinals'].append(ordinal)
                    selections[label]['quantity'] += int(row['quantity (units)'])
    for ordinal, row in enumerate(read('Picking_Wave'), 2):
        k = row['waveNumber'].strip(), row['reference'].strip(), size(row['Size (US)'])
        if opaque('key', *k) == key:
            raw_key = k; selections['PICKING']['ordinals'].append(ordinal)
            selections['PICKING']['quantity'] += int(row['quantityToPick (units)'])
    if raw_key is None:
        raise ValueError('Key not in any declared interpretation')
    result = {}
    for label, selection in selections.items():
        source = 'Picking_Wave.csv' if label == 'PICKING' else 'Customer_Order.csv'
        ids = selection['ordinals']
        result[label] = dict(source_file='data/raw/' + source, source_sha256=digest(ROOT / 'data/raw' / source),
                             lineage_role='CONTRIBUTING_POPULATION', record_count=len(ids), quantity=selection['quantity'],
                             record_ranges=ranges(ids))
    return dict(reconciliation_id=key, raw_key=dict(zip(('wave', 'reference', 'size'), raw_key)),
                evidence='LOCAL_SOURCE_SELECTORS_NOT_PUBLIC_EXTRACT', selections=result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reconciliation_id')
    key = parser.parse_args().reconciliation_id
    if not re.fullmatch(r'key_[0-9a-f]{20}', key): parser.error('Expected key_ and 20 lowercase hex digits')
    print(json.dumps(lookup(key), indent=2, ensure_ascii=False))
