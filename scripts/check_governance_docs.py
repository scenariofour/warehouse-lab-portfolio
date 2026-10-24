#!/usr/bin/env python3
"""Structural evidence/document checks only. Never writes a gate decision or authenticates approval."""
from pathlib import Path
import argparse, datetime as dt, difflib, hashlib, json, re
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parent.parent
DATE=dt.datetime.now(ZoneInfo('America/New_York')).date().isoformat()
parser=argparse.ArgumentParser()
parser.add_argument('--evidence-dir',type=Path)
parser.add_argument('--refresh-pending',action='store_true',help='Refresh unsigned evidence identity only; refuses any recorded gate decision')
args=parser.parse_args()
OUT=(ROOT/args.evidence_dir).resolve() if args.evidence_dir else ROOT/'docs/evidence'/DATE

if args.refresh_pending:
    gates=json.loads((ROOT/'docs/GATE_REVIEWS.json').read_text())['gates']
    assert all(g['reviewState']=='PENDING' and g['decision'] is None for g in gates),'Never overwrite evidence attached to recorded decisions'
    old=json.loads((OUT/'baseline-inventory.json').read_text())
    hashes={f['path']:f['sha256'] for f in old['files']}
    h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    changed=[p for p,sha in hashes.items() if (ROOT/p).is_file() and h(ROOT/p)!=sha]
    before=json.loads((OUT/'baseline-scenarios.json').read_text())['results'];after=json.loads((OUT/'scenarios.json').read_text())['results']
    keys=['policy','time','completed','failed','failedUnits','delivered','distance','utilization','minSeparation']
    comparisons=[{k:a[k]==b[k] for k in keys}|{'policyName':a['policy']} for a,b in zip(before,after)]
    impact={'reviewDate':DATE,'comparedAgainst':'baseline-inventory.json / baseline-scenarios.json','changedBaselineFiles':changed,'normalizedJSONFilesChanged':[p for p in changed if p.startswith('public/data/')],'runtimeSourceFilesChanged':[p for p in changed if p.startswith('src/')],'uiSceneSimulationCalculationSourcesUnchanged':all(h(ROOT/p)==hashes[p] for p in ['src/main.ts','src/scene.ts','src/style.css','src/simulation.ts','src/analysis.ts','src/types.ts']),'defaultPolicyOutcomeComparisons':comparisons,'allDefaultNumericalOutcomesUnchanged':all(all(a[k]==b[k] for k in keys) for a,b in zip(before,after)),'rawHashesStillMatchPublisher':json.loads((OUT/'data-evaluation.json').read_text())['rawUnchangedAndVerified']}
    (OUT/'correction-impact.json').write_text(json.dumps(impact,indent=2)+'\n')
    diff=[]
    for p in ['scripts/prepare_data.py','src/pathfinding.ts','scripts/validate-scenarios.ts','tests/simulation.test.ts','scripts/import_source_zip.py','tests/test_data_pipeline.py','package.json','README.md']:
        previous=ROOT/'work/governance-baseline'/p
        previous_text=previous.read_text().splitlines(keepends=True) if previous.exists() else []
        diff.extend(difflib.unified_diff(previous_text,(ROOT/p).read_text().splitlines(keepends=True),fromfile='before/'+p,tofile='after/'+p))
    # A supplied review diff is preserved on extracted packages that lack scratch baseline sources.
    if (ROOT/'work/governance-baseline').is_dir():(OUT/'corrections.diff').write_text(''.join(diff))
    files=[]
    for folder in ['src','scripts','tests','docs','data','public/data']:
        files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and not p.name.startswith(('evidence-manifest','document-checks')))
    files.extend(ROOT/p for p in ['README.md','package.json','package-lock.json','tsconfig.json','playwright.config.ts','vite.config.ts'])
    manifest={'reviewDate':DATE,'recordedAtUTC':dt.datetime.now(dt.timezone.utc).isoformat(),'authority':'Identity of pending review evidence only; no approval','files':[{'path':str(p.relative_to(ROOT)),'sha256':h(p)} for p in sorted(set(files))]}
    (OUT/'evidence-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
core=['PROJECT_CHARTER','REQUIREMENTS','DATA_CARD','MODEL_CARD','EVALUATION_PLAN','RISK_AND_DECISION_LOG','GATE_REVIEWS']
extra=['EXPERIMENT_CREDIBILITY','INTERNAL_PRODUCT_PRACTICES','EVIDENCE_INDEX','FINAL_REVIEW']
checked_links=0
for name in core+extra:
    p=ROOT/'docs'/f'{name}.md';text=p.read_text()
    for field in ['Owner:','Version:','Status:','Review requirements:']:
        assert field in text,f'{p.name}: missing {field}'
    assert 'PENDING HUMAN REVIEW' in text,p.name
    for href in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
        if href.startswith(('https:','http:','mailto:','#')):continue
        target=href.split('#')[0]
        resolved=(p.parent/target).resolve()
        assert resolved.exists() or resolved==(OUT/'document-checks.json').resolve(),f'{p.name}: unresolved {href}'
        checked_links+=1
plan=(ROOT/'docs/EVALUATION_PLAN.md').read_text()
for i in range(1,14):assert f'EVAL-{i:02}' in plan
register=json.loads((ROOT/'docs/GATE_REVIEWS.json').read_text())
assert register['allowedHumanOutcomes']==['APPROVED','CONDITIONALLY APPROVED','BLOCKED']
for gate in register['gates']:
    if gate['reviewState']=='PENDING':
        assert gate['decision'] is None and gate['humanReviewer'] is None and gate['decisionDate'] is None and gate['evidenceSnapshot'] is None
    else:
        assert gate['decision'] in register['allowedHumanOutcomes'] and gate['humanReviewer'] and gate['decisionDate'] and gate['evidenceSnapshot']
        assert 'AI' not in gate['humanReviewer'],'AI authorship cannot be a human approval'
claims=json.loads((ROOT/'docs/CLAIM_REGISTER.json').read_text())['claims']
assert len({c['id'] for c in claims})==len(claims)
for c in claims:
    assert c['evaluationStatus'] in ['PASS','FAIL','INCONCLUSIVE']
    assert c['limitations'] and c['evidence']
    for ref in c['evidence']:assert (ROOT/ref).is_file(),f"{c['id']}: missing {ref}"
manifest=json.loads((OUT/'evidence-manifest.json').read_text());verified=0
for f in manifest['files']:
    assert hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256'],f"Evidence drift: {f['path']}"
    verified+=1
model=json.loads((OUT/'model-evaluation.json').read_text())
for name,sha in model['inputHashes'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,f'Stale model evaluation: {name}'
scenario=json.loads((OUT/'scenarios.json').read_text())
for name,sha in scenario['inputSHA256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,f'Stale scenario evidence: {name}'
report={'reviewDate':DATE,'recordedAtUTC':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS','scope':'Structural references/metadata/input identity only; not semantic validation or human approval','requiredCoreDocuments':len(core),'additionalReviewDocuments':len(extra),'checkedLocalLinks':checked_links,'evaluationContracts':13,'claimRecords':len(claims),'gatesPending':sum(g['reviewState']=='PENDING' for g in register['gates']),'humanDecisionsRecorded':sum(g['decision'] is not None for g in register['gates']),'manifestFilesVerified':verified}
(OUT/'document-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
