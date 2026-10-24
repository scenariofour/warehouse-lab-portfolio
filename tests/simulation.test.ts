import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {Simulation} from '../src/simulation';
import {Grid} from '../src/pathfinding';
import type {WarehouseData,Allocation} from '../src/types';
const data:WarehouseData=JSON.parse(fs.readFileSync('public/data/warehouse.json','utf8'));
const inv:Allocation[]=JSON.parse(fs.readFileSync('public/data/random.json','utf8'));
test('real data: publisher verified, complete geometry, unique source row lineage',()=>{
 assert.equal(data.locations.length,2292);assert.equal(inv.length,41256);assert.equal(data.audit.sha256Verified,21);
 assert.equal(new Set(data.locations.map(l=>l.id)).size,2292);
 assert.ok(data.orders.every(o=>o.lines.every(l=>l.row>=2&&Number.isInteger(l.qty)&&l.qty>=0)));
});
test('all source storage locations have a reachable rack-free service cell',()=>{
 const g=new Grid(data.locations);assert.equal(g.services.size,2292);
 for(const [id,cell] of g.services){assert.ok(g.reachable.has(cell),id);assert.ok(!g.blocked.has(cell),id)}
 const p=g.path(g.at(-68,26),g.services.get('A-14-11')!);assert.ok(p);for(const n of p)assert.ok(!g.blocked.has(n));
});
test('pause is exact, reset starts clean, repeated fixed seed is reproducible',()=>{
 const a=new Simulation(data,inv,data.orders.slice(0,8)), b=new Simulation(data,inv,data.orders.slice(0,8));
 a.advance(100);assert.equal(a.time,0);a.running=b.running=true;
 a.advance(300);b.advance(300);assert.deepEqual(a.snapshot(),b.snapshot());
 const snap=JSON.stringify(a.snapshot());a.running=false;a.advance(100);assert.equal(JSON.stringify(a.snapshot()),snap);
 const reset=new Simulation(data,inv);assert.equal(reset.delivered,0);assert.equal(reset.stockTotal,41256);assert.equal(reset.time,0);
});
test('10 robots complete a real demand window; stock, collision, and task lifecycle invariants',()=>{
 const sim=new Simulation(data,inv,data.orders.slice(0,12));sim.running=true;
 let minSeparation=Infinity;
 for(let t=0;t<65000&&!sim.finished;t++){
  sim.step();const occupied=new Set<number>();
  for(const r of sim.robots){
   assert.ok(!sim.grid.blocked.has(r.cell));assert.ok(!occupied.has(r.cell),'overlapping occupied cells');occupied.add(r.cell);
   if(r.edge){assert.ok(!sim.grid.blocked.has(r.edge.to));assert.ok(!occupied.has(r.edge.to),'conflicting reserved cell');occupied.add(r.edge.to)}
  }
  if(t%5===0)for(let i=0;i<10;i++)for(let j=i+1;j<10;j++)minSeparation=Math.min(minSeparation,Math.hypot(sim.robots[i].x-sim.robots[j].x,sim.robots[i].z-sim.robots[j].z));
 }
 assert.ok(sim.finished,`not finished after ${sim.time}s; ${sim.robots.map(r=>r.status+':'+r.task?.id).join(',')}`);
 assert.ok(sim.completedOrders>0);assert.equal(sim.completedOrders+sim.failedOrders,12);assert.ok(minSeparation>=.99);
 assert.ok(sim.stock.every(s=>s.remaining>=0&&s.reserved>=0&&s.reserved<=s.remaining));
 assert.equal(sim.initialStock-sim.stockTotal,sim.delivered);
 const deliveries=sim.events.filter(e=>e.type==='delivered');assert.equal(new Set(deliveries.map(e=>e.task)).size,sim.delivered);
 assert.ok(Math.abs([...sim.congestionByCell.values()].reduce((n,v)=>n+v,0)-sim.congestion)<1e-6);
 assert.ok(sim.averageCompletion>0);assert.equal(sim.throughput,sim.completedOrders/(sim.time/3600));
 console.log(JSON.stringify({time:sim.time,completed:sim.completedOrders,failed:sim.failedOrders,delivered:sim.delivered,distance:sim.distance,minSeparation}));
});
test('unknown SKU fails explicitly and does not consume stock or complete successfully',()=>{
 const sim=new Simulation(data,inv,[{id:'test',number:'test',wave:'test',created:'',lines:[{sku:'NO_SUCH_PRODUCT',size:'10',qty:2,row:1}]}]);sim.running=true;sim.step();
 assert.equal(sim.failedUnits,2);assert.equal(sim.completedOrders,0);assert.equal(sim.failedOrders,1);assert.equal(sim.stockTotal,sim.initialStock);assert.equal(sim.events.filter(e=>e.type==='task_failed').length,2);
});
test('different policy remaps inventory and same inputs give identical task choices',()=>{
 const alloc:Allocation[]=JSON.parse(fs.readFileSync('public/data/dedicated.json','utf8'));
 const s=new Simulation(data,alloc,data.orders.slice(0,2),{},'Dedicated');s.running=true;s.advance(2);
 assert.equal(s.policy,'Dedicated');for(const r of s.robots)if(r.task)assert.ok(alloc.some(a=>a[0]===r.task!.stock!.location&&a[1]===r.task!.sku&&a[2]===r.task!.size));
});
test('head-on conflict near outbound stations yields without a symmetric detour livelock',()=>{
 const s=new Simulation(data,inv,[],{robotCount:2});
 for(const [i,r] of s.robots.entries()){
  const p={x:-54+i,z:17};r.cell=s.grid.at(p.x,p.z);r.x=p.x;r.z=p.z;r.goal=s.grid.at(i===0?-46:-58,16);r.phase='park';r.status='MOVING';r.route=s.grid.path(r.cell,r.goal)!;
 }
 s.running=true;s.advance(200);
 assert.ok(s.finished,`head-on routes did not clear: ${s.robots.map(r=>r.x+','+r.z+' '+r.status).join('; ')}`);
});
test('exhausted stock is reserved once, fractional speed integrates correctly, and unavailable units fail',()=>{
 const unit=inv[0];const s=new Simulation(data,[unit],[{id:'scarce',number:'scarce',wave:'test',created:'',lines:[{sku:unit[1],size:unit[2],qty:3,row:2}]}],{speed:2.3});
 s.running=true;for(let i=0;i<4000&&!s.finished;i++)s.step();
 assert.ok(s.finished);assert.equal(s.delivered,1);assert.equal(s.failedUnits,2);assert.equal(s.failedOrders,1);assert.equal(s.stockTotal,0);assert.equal(s.stock[0].reserved,0);
 for(const r of s.robots)assert.ok(Math.abs(r.distance-r.moving*2.3)<1e-6);
});
test('A* rejects blocked and out-of-grid endpoints, including identical invalid endpoints',()=>{
 const g=new Grid(data.locations),blocked=[...g.blocked][0],free=g.at(-68,26);
 assert.equal(g.path(blocked,blocked),null);
 assert.equal(g.path(blocked,free),null);
 assert.equal(g.path(-1,-1),null);
 assert.equal(g.path(free,g.width*g.height),null);
 assert.equal(g.at(g.minX+g.width,g.minZ),-1);
 assert.deepEqual(g.neighbors(-1),[]);
});
