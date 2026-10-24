#!/usr/bin/env python3
"""Read-only assessment of published records and existing normalized inputs; not a semantic validation."""
from pathlib import Path
from collections import Counter, defaultdict
import csv, datetime as dt, hashlib, json
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parent.parent
REVIEW_DATE=dt.datetime.now(ZoneInfo('America/New_York')).date().isoformat()
OUT=ROOT/'docs/evidence'/REVIEW_DATE

def read(name):
    with (ROOT/'data/raw'/f'{name}.csv').open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f,delimiter=',' if name in ('Storage_Location','Random_Storage') else ';'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(v,customer=False):
    v=v.strip()
    if not v:return ''
    n=float(v)
    if customer and v in {'35','45','55','65','75','85','95','105','115','125'}:n/=10
    return format(n,'g')
manifest=json.loads((ROOT/'data/manifest.json').read_text());checks=[]
for f in manifest['files']:
    p=ROOT/'data/raw'/f['filename'];actual=h(p)
    checks.append({'file':f['filename'],'expected':f['content_details']['sha256_hash'],'actual':actual,'matches':actual==f['content_details']['sha256_hash']})
loc=read('Storage_Location');products=read('Product');customers=read('Customer_Order');waves=read('Picking_Wave');nav=read('Support_Points_Navigation')
locids={r['originalLocation'].strip() for r in loc};refs={r['Reference'].strip() for r in products}
base=json.loads((ROOT/'public/data/warehouse.json').read_text());orders=json.loads((ROOT/'public/data/orders.json').read_text())
expectedloc=[{'id':r['originalLocation'].strip(),'x':round(float(r['y'])*.1-72,3),'z':round(float(r['x'])*.1-37.6,3),'level':int(r['z']),'source':[int(r['x']),int(r['y']),int(r['z'])]} for r in loc]
lineage=[];groups=defaultdict(list)
for i,r in enumerate(customers):groups[r['waveNumber'].strip()+'-'+r['orderNumber'].strip()].append((i+2,r))
expectedorders=[]
for key,rows in groups.items():
    r=rows[0][1]
    expectedorders.append({'id':key,'number':r['orderNumber'].strip(),'wave':r['waveNumber'].strip(),'created':dt.datetime.strptime(r['creationDate'].strip(),'%d/%m/%Y %H:%M').isoformat(),'lines':[{'sku':v['Reference'].strip(),'size':norm(v['Size (US)'],True),'qty':int(v['quantity (units)']),'row':idx} for idx,v in rows]})
for o in orders:
    for l in o['lines']:lineage.append(l['row'])
def demand_counter(selected):
    c=Counter()
    for o in selected:
        for l in o['lines']:c[(l['sku'],l['size'])]+=l['qty']
    return c
full_demand=demand_counter(orders);default_demand=demand_counter(base['orders']);policies={};counters={}
for policy in ['Random','Class_Based','Dedicated','Hybrid']:
    rows=read(policy+'_Storage');expected=[];dropped=[];rawrefs=set();loccounts=Counter();tokens=[]
    for r in rows:
        location=r.get('originalLocation',r.get('Location')).strip();loccounts[location]+=1
        for k,v in r.items():
            if (k.startswith('col_') or k.isdigit()) and v and v.strip():
                ref,token=v.strip().split(';');rawrefs.add(ref);tokens.append(float(token))
                cell=[location,ref,norm(token),token]
                if location in locids:expected.append(cell)
                else:dropped.append(cell)
    actual=json.loads((ROOT/'public/data'/f'{policy.lower()}.json').read_text());c=Counter((r[1],r[2]) for r in actual);counters[policy]=c
    matched=sum(l['qty'] for o in base['orders'] for l in o['lines'] if (l['sku'],l['size']) in c)
    policies[policy]={'sourceRows':len(rows),'sourceCells':len(tokens),'normalizedCells':len(actual),'exactNormalizedRowMatch':actual==expected,'excludedCells':len(dropped),'excludedLocations':sorted({r[0] for r in dropped}),'unknownReferencesRaw':sorted(rawrefs-refs),'unknownReferencesNormalized':sorted({r[1] for r in actual}-refs),'distinctNormalizedSKUs':len(c),'duplicateSourceLocationIDs':{k:v for k,v in loccounts.items() if v>1},'fractionalPayloadCells':sum(not v.is_integer() for v in tokens),'defaultDemandUnitsWithAnySKUStock':matched,'defaultDemandUnitsWithoutAnySKUStock':sum(default_demand.values())-matched,'defaultSupplyUpperBoundUnits':sum(min(n,c[k]) for k,n in default_demand.items()),'fullSupplyUpperBoundUnits':sum(min(n,c[k]) for k,n in full_demand.items())}
pairs=[]
for i,a in enumerate(counters):
    for b in list(counters)[i+1:]:
        keys=set(counters[a])|set(counters[b]);diff={k:counters[a][k]-counters[b][k] for k in keys if counters[a][k]!=counters[b][k]}
        pairs.append({'a':a,'b':b,'equalTotalStock':sum(counters[a].values())==sum(counters[b].values()),'identicalSKUQuantities':not diff,'differingSKUCounts':len(diff),'l1CartonDifference':sum(abs(v) for v in diff.values()),'sharedSKUs':len(set(counters[a])&set(counters[b]))})
wavekeys={(r['waveNumber'].strip(),r['reference'].strip(),norm(r['Size (US)'])) for r in waves}
size_evidence=[]
for token in ['35','45','55','65','75','85','95','105','115','125']:
    subset=[r for r in customers if r['Size (US)'].strip()==token]
    size_evidence.append({'customerToken':token,'rows':len(subset),'literalWaveJoinRows':sum((r['waveNumber'].strip(),r['Reference'].strip(),norm(token)) in wavekeys for r in subset),'normalizedWaveJoinRows':sum((r['waveNumber'].strip(),r['Reference'].strip(),norm(token,True)) in wavekeys for r in subset)})
numwaves=defaultdict(set);numcustomers=defaultdict(set)
for r in customers:numwaves[r['orderNumber'].strip()].add(r['waveNumber'].strip());numcustomers[r['orderNumber'].strip()].add(r['codCustomer'].strip())
dates=[dt.datetime.strptime(r['creationDate'].strip(),'%d/%m/%Y %H:%M').isoformat() for r in customers]
report={'reviewDate':REVIEW_DATE,'recordedAtUTC':dt.datetime.now(dt.timezone.utc).isoformat(),'claimBoundary':'Exact transformations are checked under the EXISTING size/stock/grouping assumptions; this does not confirm their real-world semantics.','sourceManifestVersion':manifest['version'],'rawHashes':checks,'rawUnchangedAndVerified':all(x['matches'] for x in checks),'counts':{'locations':len(loc),'products':len(products),'customerRows':len(customers),'pickingRows':len(waves),'navigationPoints':len(nav),'normalizedGroups':len(orders),'distinctOrderNumbers':len(numwaves),'defaultGroups':len(base['orders']),'defaultUnits':sum(default_demand.values()),'fullDemandUnits':sum(full_demand.values())},'integrity':{'geometryExact':base['locations']==expectedloc,'productsExact':base['products']=={r['Reference'].strip():{'class':r['ABCCOD'].strip(),'sector':r['Sector'].strip()} for r in products},'ordersExactUnderCurrentRules':orders==expectedorders,'defaultIsFirst120Groups':base['orders']==orders[:120],'lineageUniqueAndComplete':sorted(lineage)==list(range(2,len(customers)+2)),'duplicateGeometryIDs':len(loc)-len(locids),'negativeOrderQuantities':sum(int(r['quantity (units)'])<0 for r in customers),'missingSizes':sum(not r['Size (US)'].strip() for r in customers),'duplicateCustomerRows':len(customers)-len({tuple(r.values()) for r in customers}),'duplicatePickingRows':len(waves)-len({tuple(r.values()) for r in waves})},'timeCoverage':{'min':min(dates),'max':max(dates),'groupsWithMultipleCreationDates':sum(len({r['creationDate'].strip() for _,r in rows})>1 for rows in groups.values()),'groupsWithMultipleCustomers':sum(len({r['codCustomer'].strip() for _,r in rows})>1 for rows in groups.values()),'orderNumbersWithMultipleWaves':sum(len(v)>1 for v in numwaves.values()),'orderNumbersWithMultipleCustomers':sum(len(v)>1 for v in numcustomers.values()),'sourceDatesNondecreasing':all(a<=b for a,b in zip(dates,dates[1:]))},'halfSizeInference':size_evidence,'policies':policies,'pairwiseInventoryControls':pairs,'normalizedHashes':{str(p.relative_to(ROOT)):h(p) for p in sorted((ROOT/'public/data').glob('*.json'))}}
OUT.mkdir(parents=True,exist_ok=True);(OUT/'data-evaluation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['rawHashes','normalizedHashes','policies']},indent=2))
for p,v in policies.items():print(p,json.dumps({k:x for k,x in v.items() if not isinstance(x,list)},sort_keys=True))
assert report['rawUnchangedAndVerified'] and all(report['integrity'][k] for k in ['geometryExact','productsExact','ordersExactUnderCurrentRules','defaultIsFirst120Groups','lineageUniqueAndComplete'])
assert all(p['exactNormalizedRowMatch'] for p in policies.values())
