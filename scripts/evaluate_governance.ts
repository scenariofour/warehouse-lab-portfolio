/** Internal verification/sensitivity only. No production UI or model assumptions are changed. */
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {Simulation} from '../src/simulation';
import {Grid} from '../src/pathfinding';
import {DEFAULT_CONFIG,type WarehouseData,type Allocation,type Config} from '../src/types';
const date=new Intl.DateTimeFormat('en-CA',{timeZone:'America/New_York'}).format(new Date());
const out=path.join('docs/evidence',date);fs.mkdirSync(out,{recursive:true});
const data:WarehouseData=JSON.parse(fs.readFileSync('public/data/warehouse.json','utf8'));
const allocations:Allocation[]=JSON.parse(fs.readFileSync('public/data/random.json','utf8'));
const digest=(v:unknown)=>createHash('sha256').update(JSON.stringify(v)).digest('hex');
const hashFile=(p:string)=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const inputHashes=Object.fromEntries(['public/data/warehouse.json','public/data/random.json','public/data/orders.json','src/simulation.ts','src/pathfinding.ts','src/types.ts','scripts/evaluate_governance.ts'].map(p=>[p,hashFile(p)]));
function bfs(grid:Grid,start:number,goal:number){
 const queue=[start],cost=new Map([[start,0]]);
 for(let i=0;i<queue.length;i++){const n=queue[i];if(n===goal)return cost.get(n)!;
  const p=grid.point(n);
  for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]]){const next=grid.at(p.x+dx,p.z+dz);if(next>=0&&!grid.blocked.has(next)&&!cost.has(next)){cost.set(next,cost.get(n)!+1);queue.push(next)}}
 }return null;
}
const grid=new Grid(data.locations),routing=[];
for(const l of data.locations.filter((_,i)=>i%59===0)){
 const start=grid.at(-68,26),goal=grid.services.get(l.id)!,route=grid.path(start,goal),reference=bfs(grid,start,goal);
 assert.ok(route);assert.equal(route.length,reference);let prev=start;
 for(const n of route){const a=grid.point(prev),b=grid.point(n);assert.equal(Math.abs(a.x-b.x)+Math.abs(a.z-b.z),1);assert.ok(!grid.blocked.has(n));prev=n}
 routing.push({location:l.id,length:route.length,referenceBFS:reference});
}
function evaluate(config:Partial<Config>,label:string){
 const sim=new Simulation(data,allocations,data.orders,config);sim.running=true;let positionTravel=0,conflicts=0,steps=0,minSeparation=Infinity;
 while(!sim.finished&&sim.time<60000){
  const before=sim.robots.map(r=>({x:r.x,z:r.z}));sim.step();steps++;
  const occupied=new Set<number>();
  for(const [i,r] of sim.robots.entries()){
   positionTravel+=Math.abs(r.x-before[i].x)+Math.abs(r.z-before[i].z);
   if(r.task?.stock){const stock=r.task.stock;assert.ok(stock.remaining>=stock.reserved&&stock.reserved>=0,label+' active stock invariant')}
   for(const n of r.edge?[r.cell,r.edge.to]:[r.cell]){if(occupied.has(n)||sim.grid.blocked.has(n))conflicts++;occupied.add(n)}
  }
  if(steps%10===0)for(let i=0;i<sim.robots.length;i++)for(let j=i+1;j<sim.robots.length;j++)minSeparation=Math.min(minSeparation,Math.hypot(sim.robots[i].x-sim.robots[j].x,sim.robots[i].z-sim.robots[j].z));
 }
 const events=sim.events,release=new Map(events.filter(e=>e.type==='order_released').map(e=>[e.order!,e.time]));
 const complete=events.filter(e=>e.type==='order_completed'),failed=events.filter(e=>e.type==='order_failed'),delivered=events.filter(e=>e.type==='delivered'),failedUnits=events.filter(e=>e.type==='task_failed');
 const average=complete.reduce((sum,e)=>sum+e.time-release.get(e.order!)!,0)/(complete.length||1);
 const working=sim.robots.reduce((n,r)=>n+r.moving+r.picking+r.unloading,0);
 const referenceWorking=positionTravel/sim.config.speed+delivered.length*(Math.ceil(sim.config.pickTime/sim.config.dt-1e-8)*sim.config.dt+Math.ceil(sim.config.unloadTime/sim.config.dt-1e-8)*sim.config.dt);
 const stockSum=sim.stock.reduce((n,s)=>n+s.remaining,0),busy=sim.robots.filter(r=>r.task).length;
 const demanded=data.orders.reduce((n,o)=>n+o.lines.reduce((m,l)=>m+l.qty,0),0);
 const occupiedLocations=new Set(sim.stock.filter(s=>s.remaining>0).map(s=>s.location));
 const errors={travel:Math.abs(positionTravel-sim.distance),averageCompletion:Math.abs(average-sim.averageCompletion),workingSeconds:Math.abs(working-referenceWorking),throughput:Math.abs(sim.throughput-complete.length*3600/sim.time),utilization:Math.abs(sim.utilization-referenceWorking/(sim.time*sim.robots.length)),occupancy:Math.abs(sim.occupancy-occupiedLocations.size/data.locations.length),stock:Math.abs(stockSum-sim.stockTotal)};
 assert.ok(sim.finished,label+' did not finish before internal guard horizon');assert.equal(conflicts,0);assert.ok(minSeparation>=.99);
 assert.equal(sim.droppedEvents,0,'Oracle requires a complete event log');assert.equal(complete.length,sim.completedOrders);assert.equal(failed.length,sim.failedOrders);assert.equal(complete.length+failed.length,data.orders.length);
 assert.equal(delivered.length,sim.delivered);assert.equal(new Set(delivered.map(e=>e.task)).size,sim.delivered);assert.equal(failedUnits.length,sim.failedUnits);assert.equal(delivered.length+failedUnits.length,demanded);
 const unitsByGroup=new Map<string,number>();for(const e of [...delivered,...failedUnits])unitsByGroup.set(e.order!,1+(unitsByGroup.get(e.order!)??0));
 for(const order of data.orders)assert.equal(unitsByGroup.get(order.id)??0,order.lines.reduce((n,l)=>n+l.qty,0),label+' per-group units '+order.id);
 assert.equal(sim.initialStock-sim.stockTotal,sim.delivered);assert.equal(busy,0);assert.ok(sim.stock.every(s=>s.reserved===0&&s.remaining>=0));
 for(const [key,value] of Object.entries(errors))assert.ok(value<=1e-5,label+' '+key+' oracle discrepancy '+value);
 assert.ok(sim.utilization>=0&&sim.utilization<=1+1e-9);
 const result={label,config:sim.config,steps,time:sim.time,completedGroups:sim.completedOrders,failedGroups:sim.failedOrders,delivered:sim.delivered,failedUnits:sim.failedUnits,distance:sim.distance,throughput:sim.throughput,averageCompletion:sim.averageCompletion,utilization:sim.utilization,congestion:sim.congestion,positionTravel,minSeparation,conflicts,oracleErrors:errors,eventCount:events.length,eventHash:digest(events)};
 console.log(label,JSON.stringify({time:result.time,completed:result.completedGroups,delivered:result.delivered,conflicts,maxOracleError:Math.max(...Object.values(errors))}));return result;
}
const baseline=evaluate({},'baseline');const replay=evaluate({},'exact replay');
assert.deepEqual(baseline.eventHash,replay.eventHash);assert.equal(baseline.distance,replay.distance);assert.equal(baseline.time,replay.time);
const cases:[string,Partial<Config>][]=[['speed 0.8',{speed:.8}],['speed 1.2',{speed:1.2}],['pick 9.6s',{pickTime:9.6}],['pick 14.4s',{pickTime:14.4}],['unload 8s',{unloadTime:8}],['unload 12s',{unloadTime:12}],['release 4.8s',{releaseInterval:4.8}],['release 7.2s',{releaseInterval:7.2}],['priority seed 43',{seed:43}],['priority seed 52',{seed:52}],['time step 0.1s',{dt:.1}],['time step 0.4s',{dt:.4}]];
const sensitivity=cases.map(([label,config])=>evaluate(config,label));
const alias=sensitivity.find(r=>r.config.seed===52)!;assert.equal(alias.eventHash,baseline.eventHash);
const report={reviewDate:date,recordedAtUTC:new Date().toISOString(),kind:'Technical verification and hypothetical local sensitivity, not operational validation',inputHashes,demandHash:digest(data.orders),routing:{samples:routing.length,reference:'Independent queue-based BFS over the same declared occupancy grid',results:routing},baseline,replay:{eventHash:replay.eventHash,time:replay.time,distance:replay.distance,exactMatch:true},sensitivity,sensitivityLimitations:['Values are analyst-selected +/-20% diagnostics, not measured field ranges.','Only source-order prefix of 120 groups and the adopted stock/geometry assumptions are covered.','Seeds are deterministic priority offsets, not random experimental replications; seed 42 and 52 are equivalent with 10 robots.','No calibrated scale, stock, floor topology, or real service-time ground truth is available.','No causal ranking, confidence interval, ROI, or deployment recommendation is established.']};
fs.writeFileSync(path.join(out,'model-evaluation.json'),JSON.stringify(report,null,2)+'\n');
