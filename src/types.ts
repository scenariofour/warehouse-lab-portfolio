export type Policy = 'Random' | 'Class_Based' | 'Dedicated' | 'Hybrid';
export interface Location { id:string; x:number; z:number; level:number; source:[number,number,number] }
export interface OrderLine { sku:string; size:string; qty:number; row:number }
export interface SourceOrder { id:string; number:string; wave:string; created:string; lines:OrderLine[] }
export interface WarehouseData { provenance:{title:string;doi:string;author:string;license:string;url:string}; locations:Location[]; products:Record<string,{class:string;sector:string}>; navigation:{label:string;source:number[]}[]; audit:Record<string,any>; orders:SourceOrder[] }
export type Allocation = [string,string,string,string];
export interface Config { robotCount:number; speed:number; pickTime:number; unloadTime:number; dt:number; releaseInterval:number; seed:number; }
export const DEFAULT_CONFIG:Config = { robotCount:10,speed:1,pickTime:12,unloadTime:10,dt:.2,releaseInterval:6,seed:42 };
export const STATIONS = [{x:-58,z:16},{x:-46,z:16}];

// Hypothetical equipment envelopes, shared with routing (modeled meters).
export const EQUIPMENT_OBSTACLES = [
 ...STATIONS.map(p=>({x:p.x,z:1.8,w:5.5,d:18.2})),
 ...Array.from({length:5},(_,i)=>({x:-34+i%2*5,z:6+Math.floor(i/2)*5,w:3.5,d:3})),
 {x:-18,z:26,w:2.5,d:6.4},
 ...Array.from({length:10},(_,i)=>({x:-68+i*2,z:27.3,w:1.15,d:.25}))
];
