#!/usr/bin/env python3
"""Download, verify, audit and normalize Mendeley v1. Python standard library only."""
import argparse, ast, collections, csv, datetime as dt, hashlib, json, pathlib, subprocess, tempfile
from import_source_zip import import_source_zip
ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / 'data/raw'
OUT = ROOT / 'public/data'
parser = argparse.ArgumentParser()
parser.add_argument('--zip', type=pathlib.Path, help='Official Download All ZIP')
parser.add_argument('--download', action='store_true')
a = parser.parse_args()
RAW.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
meta_path = ROOT / 'data/manifest.json'
if not meta_path.exists():
    subprocess.run(['curl','-fsSL','https://data.mendeley.com/public-api/datasets/pf2w725pw3','-o',str(meta_path)],check=True)
meta = json.loads(meta_path.read_text())
if meta['version'] != 1: raise SystemExit('Expected dataset v1; inspect a newer version before importing.')
if a.zip:
    import_source_zip(a.zip, RAW, meta['files'])
checks = []
for f in meta['files']:
    p = RAW / f['filename']
    if not p.exists() and a.download:
        with tempfile.TemporaryDirectory(dir=RAW) as tmp:
            candidate=pathlib.Path(tmp)/p.name
            subprocess.run(['curl','-fsSL','--retry','2',f['content_details']['download_url'],'-o',str(candidate)], check=True)
            if hashlib.sha256(candidate.read_bytes()).hexdigest()!=f['content_details']['sha256_hash']:
                raise SystemExit(f'Hash mismatch in download: {p.name}; source not imported')
            candidate.replace(p)
    if p.exists():
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != f['content_details']['sha256_hash']: raise SystemExit(f'Hash mismatch: {p.name}; source preserved for review')
        checks.append({'file': p.name, 'bytes': p.stat().st_size, 'sha256': actual})
def read(name):
    p = RAW / (name + '.csv')
    if not p.exists(): raise SystemExit(f'Missing {p}. Run npm run data -- --download, or npm run data -- --zip /path/to/official.zip')
    with p.open(encoding='utf-8-sig', newline='') as f:
        return [{k: (v or '').strip() for k,v in r.items()} for r in csv.DictReader(f, delimiter=',' if name in ['Storage_Location','Random_Storage'] else ';')]
def size(v, customer=False):
    if not v: return ''
    n=float(v)
    # Existing inferred repair of tokens such as 85,95,105; not an authoritative source definition.
    # Only these tokens have matching half-size counterparts in Picking_Wave.
    if customer and v in {'35','45','55','65','75','85','95','105','115','125'}: n/=10
    return format(n,'g')
source = {n:read(n) for n in ['Storage_Location','Random_Storage','Class_Based_Storage','Dedicated_Storage','Hybrid_Storage','Product','Customer_Order','Picking_Wave','Support_Points_Navigation']}
locs=[]
for r in source['Storage_Location']:
    locs.append({'id':r['originalLocation'],'x':round(float(r['y'])*.1-72,3),'z':round(float(r['x'])*.1-37.6,3),'level':int(r['z']),'source':[int(r['x']),int(r['y']),int(r['z'])]})
loc_ids={r['id'] for r in locs}; products={r['Reference']:{'class':r['ABCCOD'],'sector':r['Sector']} for r in source['Product']}
policies={}; policy_audit={}
for name in ['Random','Class_Based','Dedicated','Hybrid']:
    inv=[]; missing=[]; unknown=set(); counts=collections.Counter(); duplicates=collections.Counter()
    for r in source[name+'_Storage']:
        location=r.get('originalLocation',r.get('Location')); duplicates[location]+=1
        for k,v in r.items():
            if not (k.startswith('col_') or k.isdigit()) or not v: continue
            ref,token=v.split(';'); sku=ref+'|'+size(token); counts[sku]+=1
            if location not in loc_ids: missing.append(location); continue
            if ref not in products: unknown.add(ref)
            inv.append([location,ref,size(token),token])
    policies[name]=inv
    policy_audit[name]={'rows':len(source[name+'_Storage']),'cells':sum(counts.values()),'importedCells':len(inv),'missingGeometryLocations':sorted(set(missing)),'cellsWithoutGeometry':len(missing),'unknownReferences':sorted(unknown),'duplicateLocations':{k:v for k,v in duplicates.items() if v>1},'distinctSKUs':len(counts)}
    (OUT/(name.lower()+'.json')).write_text(json.dumps(inv,separators=(',',':')))
orders={}; sku_inv=collections.Counter((r[1],r[2]) for r in policies['Random']); missing_sizes=0
for i,r in enumerate(source['Customer_Order']):
    key=r['waveNumber']+'-'+r['orderNumber']
    if key not in orders:
        orders[key]={'id':key,'number':r['orderNumber'],'wave':r['waveNumber'],'created':dt.datetime.strptime(r['creationDate'],'%d/%m/%Y %H:%M').isoformat(),'lines':[]}
    s=size(r['Size (US)'],True)
    if not s:missing_sizes+=1
    orders[key]['lines'].append({'sku':r['Reference'],'size':s,'qty':int(r['quantity (units)']),'row':i+2})
all_orders=list(orders.values())
nav=[{'label':r['labels'],'source':list(ast.literal_eval(r['points_specified']))} for r in source['Support_Points_Navigation']]
counts={n:len(v) for n,v in source.items()}
stock=sum(sku_inv.values()); dates=[o['created'] for o in all_orders]
wave=source['Picking_Wave']; wave_locs={r['locations'].strip() for r in wave}; wave_ref={r['reference'] for r in wave}
wave_keys={(r['waveNumber'],r['reference'],size(r['Size (US)'])) for r in wave}
order_wave_match=sum((r['waveNumber'],r['Reference'],size(r['Size (US)'],True)) in wave_keys for r in source['Customer_Order'])
audit={'counts':counts,'policy':policy_audit,'sha256Verified':len(checks),'orderCount':len(all_orders),'customerOrderNumberCount':len({r['orderNumber'] for r in source['Customer_Order']}),'dateMin':min(dates),'dateMax':max(dates),'duplicateCustomerRows':len(source['Customer_Order'])-len({tuple(r.values()) for r in source['Customer_Order']}),'duplicatePickingRows':len(wave)-len({tuple(r.values()) for r in wave}),'missingOrderSizes':missing_sizes,'orderRowsMatchingWaveSKU':order_wave_match,'waveLocationsMissingGeometry':sorted(wave_locs-loc_ids),'waveReferencesMissingProduct':sorted(wave_ref-set(products)),'orderRowsWithoutRandomSKU':sum((r['Reference'],size(r['Size (US)'],True)) not in sku_inv for r in source['Customer_Order']),'negativeOrderQuantities':sum(int(r['quantity (units)'])<0 for r in source['Customer_Order']),'duplicateGeometryIDs':len(locs)-len(loc_ids),'modeledStock':stock,'checks':checks}
base={'provenance':{'title':meta['name'],'doi':'10.17632/pf2w725pw3.1','author':'Rodrigo Furlan de Assis','license':'CC BY 4.0','url':'https://data.mendeley.com/datasets/pf2w725pw3/1'},'locations':locs,'products':products,'navigation':nav,'audit':audit,'orders':all_orders[:120]}
(OUT/'warehouse.json').write_text(json.dumps(base,separators=(',',':')))
(OUT/'orders.json').write_text(json.dumps(all_orders,separators=(',',':')))
(OUT/'audit.json').write_text(json.dumps(audit,indent=2))
lines=['# Data audit','', 'Source: Rodrigo Furlan de Assis. *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*, Mendeley Data v1, DOI [10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), CC BY 4.0. Downloaded 2026-10-15. All '+str(len(checks))+' published files verified against publisher SHA-256 hashes. Raw records remain in `data/raw`; manifest in `data/manifest.json`. No fabricated fallback records.','', '## Actual schemas','']
for n,rows in source.items():
    lines.append(f'- **{n}.csv**: {len(rows):,} rows; columns: '+', '.join('`'+c+'`' for c in rows[0])+'.')
lines+=['','CSV delimiters: Storage_Location and Random_Storage use commas; all other CSVs use semicolons. UTF-8 BOM and whitespace are stripped. A nonempty numbered storage cell is split once into product reference and its original numeric token. All original numeric tokens are retained.','', '## Critical interpretation limits','', '**Storage payload ambiguity.** README describes `reference;quantity`, but tokens include half values such as 8.5, 9.5 and 10.5, match the wave shoe-size domain, and dedicated rows repeat identical values in all 18 cells. There is no authoritative reconciliation in the notebook. This app explicitly assumes the numeric token is a size and one encoded cell is one available carton/unit; it does NOT claim these are verified stock quantities. Inventory counts, depletion and stockouts are conditional on this model. The first raw token is retained for inspection. Fractional tokens are never presented as measured quantities.','', '**Size normalization.** Customer sizes 35,45,55,65,75,85,95,105,115,125 are mapped to 3.5…12.5, consistent with Picking_Wave half sizes. Other integers (including 215…305) stay unchanged. Missing sizes remain missing and become unfulfillable demand. This is an inferred repair, not a source fact.','', '**Geometry and units.** README calls X,Y,Z meters. The notebook instead names Z=1…4 floors and draws 15×30 source-unit blocks on Z1/2 and 45×30 on Z3/4. We preserve all 2,292 source coordinates and relative XY distances, but use an explicit hypothetical horizontal calibration of 0.1 modeled meters/source unit. No claim of surveyed metric accuracy. Three.js X = source Y × 0.1 − 72; Three.js Z = source X × 0.1 − 37.6. This is a rigid rotation/reflection and uniform horizontal scaling. Vertical display Y = (source Z − 1) × 1.45 + 0.6. Z levels are displayed as four rack tiers with abstract shelf service, not real autonomous travel between floors. The original notebook and SVGs treat them as separate floors. Robot travel distances and 1m/s therefore use **modeled meters**.','', 'Rack footprints follow notebook block dimensions (1.5×3 modeled m on levels1/2, 4.5×3 on levels3/4). Raster routing excludes the union of footprints on every tier, inflated by robot radius. 44 source navigation support points are retained; the published sparse points alone do not define a complete traversable graph, so routing uses a derived 1m occupancy grid. Outer access lanes, receiving, packing, conveyors and two outbound stations are synthetic and positioned outside rack footprints. Equipment footprints and a 0.48m AMR clearance are also excluded from the routing grid. DWG downloaded and hash-verified, not decoded; geometry reconstructed from CSV and notebook block rules.','', '## Validation results','', '```json',json.dumps({k:v for k,v in audit.items() if k not in ['checks','policy']},indent=2),'```','', '## Storage configurations','']
for k,v in policy_audit.items():lines += ['### '+k,'```json',json.dumps(v,indent=2),'```']
lines+=['','Additional configurations have different SKU distributions and missing geometry locations; those cells are excluded and reported above. They are experimental scenarios, not inventory-equivalent controlled storage-policy experiments. The app rebuilds SKU indices for each policy and never reuses historical pick coordinates. Demand window and all engineering parameters remain the same when switching.','', '## Order and time semantics','',f"Customer creation dates span {min(dates)} through {max(dates)}; {len(all_orders):,} wave/order groups ({audit['customerOrderNumberCount']:,} distinct order numbers). Order keys combine wave and order number. {order_wave_match:,} of {counts['Customer_Order']:,} customer rows join a wave/reference/normalized-size tuple. {audit['orderRowsWithoutRandomSKU']:,} rows lack that SKU in the baseline stock model.",'', 'Customer creationDate is the only timestamp in these CSVs. Picking_Wave has no pick-start, pick-end, robot motion, or completion timestamps. It cannot support measured service durations or a historical robot replay. Original order sequence and source row numbers are preserved. Default session is the first 120 complete source wave/order groups; larger windows/all demand can be loaded. Orders release every six simulated seconds (configurable), rather than compressing historical dates invisibly. Repeated customer rows are preserved as demand, because they may represent legitimate repeated lines. Identical picking rows are preserved in the raw files but not replayed as extra orders: the file has repeated one-unit picks. Historical location joins are audited only; every new task is routed using the active configuration.','', '## Simulation assumptions and metrics','', '10 AMRs; 1 modeled m/s; one assumed carton/unit per trip; pick12s; unload10s; two exclusive outbound stations and ten approach staging cells; step0.2s; deterministic seed42. Source stock is reserved once at dispatch and decremented at pick; orders complete only when all units unload. Missing SKU/size, depleted stock, or inaccessible locations generate explicit failed units, so partially failed orders never appear completed. Queue is FIFO with a deterministic Manhattan-nearest service-cell heuristic; it does not optimize total fleet travel or compare every candidate path length. Robots reserve both edge endpoints while moving; opposing edges and occupied destinations are blocked. Replanning avoids reserved cells. In a contested cell, the higher-ID robot pulls aside and holds for four seconds to prevent symmetric detour livelock; waiting and traffic are accumulated from actual fixed-step state. Shelf picking is an abstract service, not an implemented industrial manipulator.','', 'Conveyor parcels spawn only on actual unload events and move for16 simulated seconds; packing and belt travel are synthetic. Receiving area is a static context model; no invented inbound replenishment. No truck operation or robotic arm is implemented.','', 'Throughput = completed whole orders / elapsed hours. Completion time is release-to-final-unload for successful orders. Utilization = moving + picking + unloading robot-seconds / available robot-seconds; congestion waiting is separate. Travel sums actual edge progress. Occupancy is nonempty modeled storage locations / geometry locations; stock is the remaining assumed carton count. Warmup, modeled dimensions and ambiguous stock mean these are comparative sandbox results, not validated factory predictions. Every event includes simulation time; exports include config, source and scenario.']
(ROOT/'docs/data-audit.md').write_text('\n'.join(lines)+'\n')
(ROOT/'public/data-audit.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({k:v for k,v in audit.items() if k not in ['checks','policy']},indent=2))
print('Normalized files generated in public/data; audit in docs/data-audit.md')
