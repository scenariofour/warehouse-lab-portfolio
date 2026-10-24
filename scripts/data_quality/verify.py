#!/usr/bin/env python3
"""Validate the DQ foundation without executing or rewriting the simulator."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
DQ = ROOT / 'docs/data-quality'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preservation():
    pinned = json.loads((DQ / 'evidence/baseline-preservation.json').read_text())
    for path, expected in pinned.items():
        assert digest(ROOT / path) == expected, f'Preserved file changed: {path}'
    gates = json.loads((ROOT / 'docs/GATE_REVIEWS.json').read_text())['gates']
    assert len(gates) == 5
    assert all(g['reviewState'] == 'PENDING' and g['decision'] is None for g in gates)
    return len(pinned)


def run_tests(pattern):
    run = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', pattern, '-v'],
                         cwd=ROOT, capture_output=True, text=True)
    assert run.returncode == 0, run.stdout + run.stderr
    return run.stdout + run.stderr


def main(milestone):
    report = {'milestone': milestone, 'status': 'PASS',
              'executed_at_utc': datetime.now(timezone.utc).isoformat(),
              'preserved_files': preservation(), 'gates': 'G0–G4 PENDING',
              'simulation_executed': False,
              'tests': run_tests('test_dq_contract.py'),
              'input_hashes': {p: digest(ROOT / p) for p in (
                  'docs/data-quality/issue-record.schema.json', 'scripts/data_quality/contract.py',
                  'tests/test_dq_contract.py')}}
    if milestone in ('M2', 'M3'):
        report['tests'] += run_tests('test_dq_registry.py')
        report['registry_manifest_sha256'] = digest(DQ / 'registry/manifest.json')
        for path in ('scripts/data_quality/build_registry.py', 'tests/test_dq_registry.py'):
            report['input_hashes'][path] = digest(ROOT / path)
    if milestone == 'M3':
        report['tests'] += run_tests('test_dq_tableau.py')
        report['tableau_manifest_sha256'] = digest(DQ / 'tableau/manifest.json')
        for path in ('scripts/data_quality/export_tableau.py', 'tests/test_dq_tableau.py'):
            report['input_hashes'][path] = digest(ROOT / path)
        report['tableau_authored_or_published'] = False
        report['synthetic_fixtures_generated'] = False
    (DQ / f'evidence/{milestone.lower()}-validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('tests', 'input_hashes')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('milestone', choices=['M1', 'M2', 'M3'])
    main(parser.parse_args().milestone)
