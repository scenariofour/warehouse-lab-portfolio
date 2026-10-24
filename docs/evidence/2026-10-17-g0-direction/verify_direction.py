from pathlib import Path
import hashlib, json, datetime, re, sys, unicodedata
ROOT=Path(__file__).resolve().parents[2] if Path(__file__).resolve().parent.name=='g0-direction-review' else Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/evidence/2026-10-17-g0-direction'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
allowed={'docs/'+n for n in ['PROJECT_CHARTER.md','REQUIREMENTS.md','EVALUATION_PLAN.md','MODEL_CARD.md','GATE_REVIEWS.md','RISK_AND_DECISION_LOG.md','CLAIM_REGISTER.json','INTERNAL_PRODUCT_PRACTICES.md','EVIDENCE_INDEX.md']}
before=json.loads((OUT/'before-inventory.json').read_text())['files']
changed=[];missing=[];package_omissions=[];unchanged=[]
for f in before:
    p=ROOT/f['path']
    if not p.exists():
        (package_omissions if f['path'].startswith('outputs/') else missing).append(f['path'])
    elif h(p)!=f['sha256']:changed.append(f['path'])
    else:unchanged.append(f['path'])
assert not missing,missing
assert set(changed)==allowed,changed
protected=[f['path'] for f in before if f['path'] not in allowed]
assert all(p in unchanged or p in package_omissions for p in protected)
for name in ['model-evaluation.json','scenarios.json']:
    assert (OUT/name).read_bytes()==(ROOT/'docs/evidence/2026-10-17'/name).read_bytes()
report={'recordedAtUTC':now(),'status':'PASS','scope':'Byte preservation only; not rerun evaluation, semantic validity or approval','baselineFiles':len(before),'unchangedFiles':len(unchanged),'changedFiles':changed,'missingUnexpectedFiles':missing,'packageOutputOmissions':package_omissions,'priorEvidenceFilesVerified':sum(p.startswith('docs/evidence/2026-10-17/') for p in unchanged),'priorOutputFilesVerified':sum(p.startswith('outputs/') for p in unchanged),'nonDocumentationChanges':[],'historicalReportsCopiedExactly':True}
(OUT/'preservation-checks.json').write_text(json.dumps(report,indent=2)+'\n')
charter=(ROOT/'docs/PROJECT_CHARTER.md').read_text()
question='How can real-world warehouse data be used to identify operational inefficiencies, evaluate potential improvements, and support better business decisions?'
assert question in charter
for text in ['**A — primary objective','**C — internal management','**B — technical research','No positive optimization result is required','Observed source records','Derived values','Assumed model inputs','Simulated outputs']:
    assert text in charter,text
risk=(ROOT/'docs/RISK_AND_DECISION_LOG.md').read_text();prior=(OUT/'prior-documents/RISK_AND_DECISION_LOG.md').read_text()
assert 'D-01 — OWNER-CONFIRMED DIRECTION' in risk
assert risk.split('## Supported corrections')[1].split('## Decision records')[0]==prior.split('## Supported corrections')[1].split('## Decision records')[0]
for i in range(2,6):
    assert next(l for l in risk.splitlines() if l.startswith(f'| D-0{i}'))==next(l for l in prior.splitlines() if l.startswith(f'| D-0{i}'))
plan=(ROOT/'docs/EVALUATION_PLAN.md').read_text();oldplan=(OUT/'prior-documents/EVALUATION_PLAN.md').read_text()
assert plan.split('## Evaluation register')[1].split('## References and golden cases')[0]==oldplan.split('## Evaluation register')[1].split('## References and golden cases')[0]
new=json.loads((ROOT/'docs/CLAIM_REGISTER.json').read_text())['claims'];old=json.loads((OUT/'prior-documents/CLAIM_REGISTER.json').read_text())['claims']
assert len(new)==15 and len(old)==14
for a,b in zip(old,new):
    assert a['id']==b['id'] and a['evaluationStatus']==b['evaluationStatus'] and a['evidence']==b['evidence']
    if a['id']!='CL-14':assert a==b
assert (ROOT/'docs/GATE_REVIEWS.json').read_bytes()==(OUT/'prior-documents/GATE_REVIEWS.json').read_bytes()
gates=json.loads((ROOT/'docs/GATE_REVIEWS.json').read_text())['gates']
assert len(gates)==5 and {g['gate'] for g in gates}=={'G0','G1','G2','G3','G4'}
for g in gates:
    assert g['reviewState']=='PENDING'
    assert all(g[k] is None for k in ['decision','humanReviewer','decisionDate','evidenceSnapshot'])
readiness=(ROOT/'docs/G0_READINESS_ASSESSMENT.md').read_text()
rows=[l for l in readiness.splitlines() if re.match(r'\| G0-D\d\d \|',l)]
assert len(rows)==9 and len(set(re.findall(r'G0-D\d\d','\n'.join(rows))))==9
assert all(re.search(r'\*\*(PASS|FAIL|INCONCLUSIVE)\*\*',l) and '](' in l for l in rows)
# Check current changed/new Markdown and linked section anchors. Historical copies retain old links.
active=[ROOT/p for p in sorted(allowed) if p.endswith('.md')]+[ROOT/'docs/G0_READINESS_ASSESSMENT.md',ROOT/'docs/G0_CHANGE_SUMMARY.md']
linkcount=0;anchorcount=0
for p in active:
    for href in re.findall(r'\[[^\]]+\]\(([^)]+)\)',p.read_text()):
        if href.startswith(('https:','http:','mailto:')):continue
        target,sep,anchor=href.partition('#');dest=(p.parent/target).resolve() if target else p
        assert dest.exists() or dest in {OUT/n for n in ['document-checks.json','direction-checks.json','evidence-manifest.json']},(str(p),href)
        linkcount+=1
        if anchor and dest.suffix=='.md':
            headings=[]
            for line in dest.read_text().splitlines():
                if line.startswith('#'):
                    text=re.sub(r'^#+\s*','',line).strip().lower()
                    slug=''.join(c for c in text if c.isalnum() or c in [' ','-','_']).replace(' ','-')
                    headings.append(slug)
            assert anchor in headings,(str(p),href,headings)
            anchorcount+=1
result={'recordedAtUTC':now(),'status':'PASS','scope':'Document predicates/alignment only; AI check, not independent review or G0 approval','exactResearchQuestion':True,'hierarchy':'A primary objective; C internal governance; B technical method','readinessDocumentFindings':{re.search(r'G0-D\d\d',r)[0]:re.search(r'\*\*(PASS|FAIL|INCONCLUSIVE)\*\*',r)[1] for r in rows},'formalReadiness':'INCONCLUSIVE; appointment, ratification, independent review and formal record outstanding','gatesPending':5,'gateRegisterBytesUnchanged':True,'gateDecisionsRecorded':0,'historicalEvaluationRowsUnchanged':13,'historicalClaimOutcomesAndEvidenceUnchanged':14,'correctionHistoryUnchanged':True,'proposedDecisionsD02ThroughD05Unchanged':True,'currentLocalLinksChecked':linkcount,'currentHeadingAnchorsChecked':anchorcount}
(OUT/'direction-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'preservation':report,'direction':result},indent=2))
