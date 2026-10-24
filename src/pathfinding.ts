import {EQUIPMENT_OBSTACLES,type Location} from './types';
export class Grid {
  readonly minX=-82; readonly minZ=-39; readonly width=165; readonly height=84;
  blocked=new Set<number>(); reachable=new Set<number>(); services=new Map<string,number>();
  constructor(locations:Location[]) {
    for(const l of locations) {
      const hz=(l.level<=2?.75:2.25)+.48, hx=1.5+.48;
      for(let x=Math.ceil(l.x-hx);x<=Math.floor(l.x+hx);x++)for(let z=Math.ceil(l.z-hz);z<=Math.floor(l.z+hz);z++)this.blocked.add(this.at(x,z));
    }
    for(const b of EQUIPMENT_OBSTACLES)for(let x=Math.ceil(b.x-b.w/2-.48);x<=Math.floor(b.x+b.w/2+.48);x++)for(let z=Math.ceil(b.z-b.d/2-.48);z<=Math.floor(b.z+b.d/2+.48);z++)this.blocked.add(this.at(x,z));
    const start=this.at(-68,26), queue=[start]; this.reachable.add(start);
    for(let i=0;i<queue.length;i++)for(const n of this.neighbors(queue[i]))if(!this.reachable.has(n)){this.reachable.add(n);queue.push(n)}
    for(const l of locations) {
      let best=-1,dist=Infinity;
      for(let x=Math.floor(l.x-6);x<=Math.ceil(l.x+6);x++)for(let z=Math.floor(l.z-6);z<=Math.ceil(l.z+6);z++){
        const n=this.at(x,z),d=Math.hypot(x-l.x,z-l.z);
        if(this.reachable.has(n)&&d<dist){dist=d;best=n}
      }
      if(best>=0)this.services.set(l.id,best);
    }
  }
  at(x:number,z:number){const col=Math.round(x)-this.minX,row=Math.round(z)-this.minZ;return Number.isFinite(col)&&Number.isFinite(row)&&col>=0&&col<this.width&&row>=0&&row<this.height?row*this.width+col:-1}
  valid(n:number){return Number.isInteger(n)&&n>=0&&n<this.width*this.height}
  point(n:number){return {x:n%this.width+this.minX,z:Math.floor(n/this.width)+this.minZ}}
  neighbors(n:number){
    if(!this.valid(n))return [];
    const x=n%this.width,z=Math.floor(n/this.width), result:number[]=[];
    if(x>0)result.push(n-1);if(x<this.width-1)result.push(n+1);if(z>0)result.push(n-this.width);if(z<this.height-1)result.push(n+this.width);
    return result.filter(v=>!this.blocked.has(v));
  }
  path(start:number,goal:number,occupied:Set<number>=new Set()):number[]|null {
    if(!this.valid(start)||!this.valid(goal)||this.blocked.has(start)||this.blocked.has(goal)||occupied.has(goal)||!this.reachable.has(start)||!this.reachable.has(goal))return null;
    if(start===goal)return [];
    const heap:{n:number;f:number}[]=[];
    const push=(v:{n:number;f:number})=>{heap.push(v);let i=heap.length-1;while(i>0){const p=(i-1)>>1;if(heap[p].f<=v.f)break;heap[i]=heap[p];i=p}heap[i]=v};
    const pop=()=>{const top=heap[0],v=heap.pop()!;if(heap.length){let i=0;while(i*2+1<heap.length){let c=i*2+1;if(c+1<heap.length&&heap[c+1].f<heap[c].f)c++;if(heap[c].f>=v.f)break;heap[i]=heap[c];i=c}heap[i]=v}return top};
    const g=new Map<number,number>([[start,0]]), from=new Map<number,number>(),closed=new Set<number>();
    const gp=this.point(goal), h=(n:number)=>{const p=this.point(n);return Math.abs(p.x-gp.x)+Math.abs(p.z-gp.z)};
    push({n:start,f:h(start)});
    while(heap.length){
      const {n}=pop();if(closed.has(n))continue;
      if(n===goal){const path:number[]=[];let cur=n;while(cur!==start){path.push(cur);cur=from.get(cur)!}return path.reverse()}
      closed.add(n);
      for(const next of this.neighbors(n)){
        if(occupied.has(next)||closed.has(next))continue;
        const cost=g.get(n)!+1;
        if(cost<(g.get(next)??Infinity)){g.set(next,cost);from.set(next,n);push({n:next,f:cost+h(next)})}
      }
    }
    return null;
  }
}
