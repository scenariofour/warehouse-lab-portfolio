import {Grid} from './pathfinding';
import {DEFAULT_CONFIG,STATIONS,type Config,type WarehouseData,type Allocation,type SourceOrder,type Policy} from './types';
export type Status='IDLE'|'MOVING'|'PICKING'|'DELIVERING'|'WAITING'|'UNLOADING'|'COMPLETED';
export interface Stock {location:string;sku:string;size:string;token:string;initial:number;remaining:number;reserved:number}
export interface Task {id:string;order:string;sku:string;size:string;row:number;stock?:Stock}
export interface RunOrder {source:SourceOrder;total:number;done:number;failed:number;releasedAt:number;completedAt?:number}
export interface Robot {id:number;cell:number;x:number;z:number;previousX?:number;previousZ?:number;route:number[];edge?:{from:number;to:number;progress:number};status:Status;phase:'pick'|'deliver'|'park'|'stage';task?:Task;goal?:number;carrying:boolean;timer:number;distance:number;moving:number;picking:number;waiting:number;unloading:number;completed:number;blockedFor:number;station?:number;yieldCell?:number;yieldUntil?:number;}
export interface SimEvent {time:number;type:string;robot?:number;order?:string;task?:string;detail?:string}
export class Simulation {
  grid:Grid; config:Config; robots:Robot[]=[]; stock:Stock[]=[]; skuIndex=new Map<string,Stock[]>(); locationStock=new Map<string,Stock[]>(); orders:RunOrder[]=[]; orderById=new Map<string,RunOrder>(); queue:Task[]=[]; queueHead=0; events:SimEvent[]=[]; droppedEvents=0;
  time=0; running=false; nextOrder=0; completedOrders=0; failedOrders=0; failedUnits=0; delivered=0; completionTotal=0; initialStock=0; stockTotal=0; congestion=0;
  stations:(number|undefined)[]=[undefined,undefined]; traffic=new Map<number,number>(); congestionByCell=new Map<number,number>(); history:{time:number;completed:number;queue:number}[]=[]; policy:Policy;
  constructor(public data:WarehouseData,allocations:Allocation[],public demand:SourceOrder[]=data.orders,config:Partial<Config>={},policy:Policy='Random'){
    this.policy=policy;this.config={...DEFAULT_CONFIG,...config}; this.grid=new Grid(data.locations);
    for(const [location,sku,size,token] of allocations){
      const key=sku+'|'+size, list=this.skuIndex.get(key)??[];
      let s=list.find(s=>s.location===location);
      if(s){s.initial++;s.remaining++}else{s={location,sku,size,token,initial:1,remaining:1,reserved:0};this.stock.push(s);list.push(s);this.skuIndex.set(key,list);const ls=this.locationStock.get(location)??[];ls.push(s);this.locationStock.set(location,ls)}
    }
    this.initialStock=this.stock.reduce((n,s)=>n+s.initial,0);this.stockTotal=this.initialStock;
    for(let i=0;i<this.config.robotCount;i++){
      const x=-68+i*2,z=26;
      this.robots.push({id:i+1,cell:this.grid.at(x,z),x,z,route:[],status:'IDLE',phase:'park',carrying:false,timer:0,distance:0,moving:0,picking:0,waiting:0,unloading:0,completed:0,blockedFor:0});
    }
  }
  emit(e:Omit<SimEvent,'time'>){if(this.events.length>=20000){this.events.splice(0,1000);this.droppedEvents+=1000}this.events.push({time:+this.time.toFixed(1),...e})}
  recordDelay(r:Robot,seconds:number){this.congestion+=seconds;this.congestionByCell.set(r.cell,(this.congestionByCell.get(r.cell)??0)+seconds)}
  occupied(except?:Robot){const set=new Set<number>();for(const r of this.robots)if(r!==except){set.add(r.cell);if(r.edge)set.add(r.edge.to)}return set}
  release(){
    while(this.nextOrder<this.demand.length&&this.time+1e-6>=this.nextOrder*this.config.releaseInterval){
      const source=this.demand[this.nextOrder++],o:RunOrder={source,total:source.lines.reduce((n,l)=>n+l.qty,0),done:0,failed:0,releasedAt:this.time};this.orders.push(o);this.orderById.set(source.id,o);
      for(const l of source.lines)for(let unit=0;unit<l.qty;unit++)this.queue.push({id:`${source.id}/${l.row}/${unit}`,order:source.id,sku:l.sku,size:l.size,row:l.row});
      this.emit({type:'order_released',order:source.id});this.finishOrder(o);
    }
  }
  finishOrder(o:RunOrder){
    if(o.completedAt!==undefined||o.done+o.failed<o.total)return;
    o.completedAt=this.time;
    if(o.failed){this.failedOrders++;this.emit({type:'order_failed',order:o.source.id,detail:`${o.failed} unfulfillable units`})}
    else{this.completedOrders++;this.completionTotal+=this.time-o.releasedAt;this.emit({type:'order_completed',order:o.source.id})}
  }
  fail(task:Task,reason:string){const o=this.orderById.get(task.order)!;o.failed++;this.failedUnits++;this.emit({type:'task_failed',order:task.order,task:task.id,detail:reason});this.finishOrder(o)}
  assign(r:Robot){
    while(this.queueHead<this.queue.length){
      const task=this.queue[this.queueHead++],candidates=(this.skuIndex.get(task.sku+'|'+task.size)??[]).filter(s=>s.remaining>s.reserved&&this.grid.services.has(s.location));
      candidates.sort((a,b)=>{const p=this.grid.point(this.grid.services.get(a.location)!),q=this.grid.point(this.grid.services.get(b.location)!);return Math.abs(p.x-r.x)+Math.abs(p.z-r.z)-Math.abs(q.x-r.x)-Math.abs(q.z-r.z)||a.location.localeCompare(b.location)});
      let chosen:Stock|undefined,path:number[]|null=null;
      for(const s of candidates){path=this.grid.path(r.cell,this.grid.services.get(s.location)!);if(path){chosen=s;break}}
      if(!chosen){const all=this.skuIndex.get(task.sku+'|'+task.size)??[];const reason=!all.length?'SKU/size absent from active allocation':!all.some(s=>s.remaining>s.reserved)?'All remaining stock already reserved or exhausted':candidates.length?'No navigable service path':'Stock has no reachable service location';this.fail(task,`${task.sku} US ${task.size||'(missing)'}: ${reason}`);continue}
      chosen.reserved++;task.stock=chosen;r.task=task;r.goal=this.grid.services.get(chosen.location);r.route=path!;r.phase='pick';r.status='MOVING';r.blockedFor=0;
      this.emit({type:'task_assigned',robot:r.id,order:task.order,task:task.id,detail:`${task.sku} US ${task.size} at ${chosen.location}`});return;
    }
    r.status=this.nextOrder===this.demand.length?'COMPLETED':'IDLE';
  }
  requestStation(r:Robot){
    const free=STATIONS.map((p,i)=>({p,i})).filter(({i})=>this.stations[i]===undefined).sort((a,b)=>Math.hypot(a.p.x-r.x,a.p.z-r.z)-Math.hypot(b.p.x-r.x,b.p.z-r.z));
    if(!free.length){r.status='WAITING';return}
    const {p,i}=free[0];this.stations[i]=r.id;r.station=i;r.goal=this.grid.at(p.x,p.z);r.route=this.grid.path(r.cell,r.goal)??[];r.phase='deliver';r.status='DELIVERING';r.blockedFor=0;
  }
  arrive(r:Robot){
    if(r.phase==='park'){r.goal=undefined;r.status='IDLE';return}
    if(r.phase==='stage'){r.status='WAITING';return}
    if(r.phase==='pick'){r.status='PICKING';r.timer=this.config.pickTime;this.emit({type:'pick_started',robot:r.id,task:r.task?.id})}
    else{r.status='UNLOADING';r.timer=this.config.unloadTime;this.emit({type:'unload_started',robot:r.id,task:r.task?.id})}
  }
  step(){
    if(!this.running)return;
    const dt=this.config.dt;this.release();
    for(const r of this.robots){r.previousX=r.x;r.previousZ=r.z}
    // Rotate priority deterministically. Exclusive endpoints also forbid edge swaps.
    const shift=(Math.floor(this.time/dt)+this.config.seed)%this.robots.length;
    const ordered=[...this.robots.slice(shift),...this.robots.slice(0,shift)];
    for(const r of ordered){
      if(!r.task&&r.phase!=='park')r.phase='park';
      if(['IDLE','COMPLETED'].includes(r.status)){this.assign(r);if(!r.task)continue}
      if(r.status==='PICKING'){
        r.picking+=dt;r.timer-=dt;
        if(r.timer<1e-6){const s=r.task!.stock!;if(s.remaining<1||s.reserved<1)throw Error('Inventory invariant violated');s.remaining--;s.reserved--;this.stockTotal--;r.carrying=true;this.emit({type:'picked',robot:r.id,task:r.task!.id,order:r.task!.order,detail:s.location});r.phase='stage';r.goal=this.grid.at(-68+(r.id-1)*2,22);r.route=this.grid.path(r.cell,r.goal)??[];r.status='DELIVERING'}
        continue;
      }
      if(r.status==='UNLOADING'){
        r.unloading+=dt;r.timer-=dt;
        if(r.timer<1e-6){const t=r.task!,o=this.orderById.get(t.order)!;o.done++;this.delivered++;r.completed++;r.carrying=false;
          this.emit({type:'delivered',robot:r.id,task:t.id,order:t.order,detail:String(r.station)});this.finishOrder(o);this.stations[r.station!]=undefined;r.station=undefined;r.task=undefined;r.goal=undefined;r.status='IDLE';r.phase='park';
          if(this.queueLength){this.assign(r);if(r.task)continue}
          // Clear the shared unloading cell even when demand has ended.
          const park=this.grid.at(-68+(r.id-1)*2,26);r.goal=park;r.route=this.grid.path(r.cell,park)??[];
          r.status='MOVING';
        }continue;
      }
      if(r.carrying&&r.phase==='stage'&&r.cell===r.goal){r.waiting+=dt;this.requestStation(r);continue}
      if(r.yieldUntil!==undefined&&this.time<r.yieldUntil&&r.cell===r.yieldCell){r.status='WAITING';r.waiting+=dt;this.recordDelay(r,dt);continue}
      let budget=this.config.speed*dt;
      while(budget>1e-8){
        if(!r.edge){
          if(r.goal===r.cell){this.arrive(r);break}
          if(r.goal===undefined){r.status='IDLE';break}
          const occupied=this.occupied(r),next=r.route[0];
          if(next!==undefined&&!occupied.has(next)){
            r.edge={from:r.cell,to:r.route.shift()!,progress:0};r.status=r.carrying?'DELIVERING':'MOVING';r.blockedFor=0;
          }else{
            const delay=budget/this.config.speed;r.status='WAITING';r.waiting+=delay;r.blockedFor+=delay;this.recordDelay(r,delay);
            if(r.blockedFor>=1){
              const blocker=this.robots.find(other=>other!==r&&other.cell===next&&!other.edge);
              if(blocker&&r.id>blocker.id){
                const here=this.grid.point(r.cell),there=this.grid.point(blocker.cell);
                const escape=this.grid.neighbors(r.cell).filter(n=>!occupied.has(n)).sort((a,b)=>{
                  const p=this.grid.point(a),q=this.grid.point(b);
                  // Prefer a perpendicular pull-out, then wait so the other robot can pass.
                  return Math.abs((p.x-here.x)*(there.x-here.x)+(p.z-here.z)*(there.z-here.z))-Math.abs((q.x-here.x)*(there.x-here.x)+(q.z-here.z)*(there.z-here.z))||a-b;
                })[0];
                if(escape!==undefined){r.route=[escape];r.yieldCell=escape;r.yieldUntil=this.time+4;r.blockedFor=0;this.emit({type:'robot_yielded',robot:r.id,detail:`Giving way to R${blocker.id}`});break}
              }
              const path=this.grid.path(r.cell,r.goal,occupied);
              if(path){r.route=path;r.blockedFor=0}
              else if(r.blockedFor>=4){
                const options=this.grid.neighbors(r.cell).filter(n=>!occupied.has(n));
                if(options.length){r.route=[options[(r.id+Math.floor(this.time))%options.length]];r.blockedFor=0}
              }
            }
            break;
          }
        }
        const e=r.edge,travel=Math.min(budget,1-e.progress);e.progress+=travel;budget-=travel;r.distance+=travel;r.moving+=travel/this.config.speed;
        const a=this.grid.point(e.from),b=this.grid.point(e.to);r.x=a.x+(b.x-a.x)*e.progress;r.z=a.z+(b.z-a.z)*e.progress;
        if(e.progress>=1-1e-8){r.cell=e.to;r.x=b.x;r.z=b.z;r.edge=undefined;this.traffic.set(r.cell,(this.traffic.get(r.cell)??0)+1);if(r.cell===r.goal){this.arrive(r);break}}
      }
    }
    this.time=+(this.time+dt).toFixed(6);
    if(Math.floor(this.time/10)>Math.floor((this.time-dt)/10))this.history.push({time:this.time,completed:this.completedOrders,queue:this.queueLength});
    if(this.history.length>720)this.history.shift();
  }
  advance(seconds:number){const n=Math.floor(seconds/this.config.dt);for(let i=0;i<n;i++)this.step()}
  get queueLength(){return this.queue.length-this.queueHead}
  get activeOrders(){return this.orders.filter(o=>o.completedAt===undefined).length}
  get distance(){return this.robots.reduce((n,r)=>n+r.distance,0)}
  get utilization(){return this.time?this.robots.reduce((n,r)=>n+r.moving+r.picking+r.unloading,0)/(this.time*this.robots.length):0}
  get throughput(){return this.time?this.completedOrders/(this.time/3600):0}
  get averageCompletion(){return this.completedOrders?this.completionTotal/this.completedOrders:0}
  get occupancy(){return [...this.locationStock.values()].filter(v=>v.some(s=>s.remaining>0)).length/this.data.locations.length}
  get finished(){return this.nextOrder===this.demand.length&&this.queueLength===0&&this.robots.every(r=>!r.task&&r.status==='COMPLETED')}
  snapshot(){return {assumptions:{stock:'One modeled carton per encoded allocation cell; numeric token interpreted as shoe size',horizontalMetersPerSourceUnit:.1,sourceZDisplay:'Source floors rendered as rack tiers; abstract shelf service',capacityCartons:1,outboundStations:2,navigationCellMeters:1,releaseTiming:'Source file order at engineered intervals'},source:this.data.provenance,policy:this.policy,config:this.config,time:this.time,demandOrders:this.demand.length,completed:this.completedOrders,failedOrders:this.failedOrders,failedUnits:this.failedUnits,delivered:this.delivered,distance:this.distance,utilization:this.utilization,throughput:this.throughput,averageCompletion:this.averageCompletion,congestionSeconds:this.congestion,congestionCells:[...this.congestionByCell.entries()].sort((a,b)=>b[1]-a[1]).slice(0,20).map(([cell,seconds])=>({...this.grid.point(cell),seconds})),stock:this.stockTotal,events:this.events,droppedEvents:this.droppedEvents,robots:this.robots.map(r=>({id:r.id,status:r.status,distance:r.distance,moving:r.moving,picking:r.picking,waiting:r.waiting,unloading:r.unloading,delivered:r.completed}))}}
}
