import * as THREE from 'three';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import type {WarehouseData,Location} from './types';
import {STATIONS} from './types';
import type {Simulation,Robot} from './simulation';
const temp=new THREE.Object3D();
function texture(draw:(c:CanvasRenderingContext2D,w:number,h:number)=>void,w=512,h=256){const c=document.createElement('canvas');c.width=w;c.height=h;draw(c.getContext('2d')!,w,h);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t}
export class WarehouseScene {
 scene=new THREE.Scene(); camera:THREE.PerspectiveCamera; renderer:THREE.WebGLRenderer; controls:OrbitControls;
 robots:THREE.Group[]=[]; robotLabels:THREE.Sprite[]=[]; rackMeshes:THREE.Object3D[]=[]; rackIDs:string[]=[]; boxLocations:string[]=[]; boxes!:THREE.InstancedMesh; boxBase:THREE.Matrix4[]=[]; boxByLocation=new Map<string,number[]>();
 routes=new THREE.Group(); parcelGroup=new THREE.Group(); parcels:THREE.Mesh[]=[]; selection=new THREE.Group(); labels=new THREE.Group(); heatGroup=new THREE.Group(); heat=false; showRoutes=true; selectedRobot?:number; follow=false; selectedLocation?:string;
 raycaster=new THREE.Raycaster(); pointer=new THREE.Vector2(); lastRoute=''; lastStock=-1; lastHeat=0;
 frameCount=0;fps=60;drawCalls=0;private lastFps=performance.now();private resizeObserver:ResizeObserver;
 private boxGeometry=new THREE.BoxGeometry(1,1,1); private mats=new Map<string,THREE.MeshStandardMaterial>();
 onSelect:(kind:'robot'|'location',id:string)=>void=()=>{};
 constructor(public host:HTMLElement,public data:WarehouseData,public sim:Simulation){
   this.scene.background=new THREE.Color('#e7edf0');this.scene.fog=new THREE.Fog('#e7edf0',260,500);
   // Preserve depth precision between the floor and slab when zoomed out.
   this.camera=new THREE.PerspectiveCamera(35,1,1,650);this.camera.position.set(120,140,155);this.camera.zoom=1.08;this.camera.updateProjectionMatrix();
   this.renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'high-performance'});this.renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));
   this.renderer.shadowMap.enabled=true;this.renderer.shadowMap.type=THREE.PCFSoftShadowMap;this.renderer.toneMapping=THREE.ACESFilmicToneMapping;this.renderer.toneMappingExposure=.93;
   this.host.prepend(this.renderer.domElement);this.renderer.domElement.setAttribute('aria-label','Interactive 3D warehouse. Drag to orbit, scroll to zoom, click a robot or shelf to inspect.');this.renderer.domElement.tabIndex=0;
   this.controls=new OrbitControls(this.camera,this.renderer.domElement);this.controls.enableDamping=true;this.controls.dampingFactor=.065;this.controls.target.set(0,-3,0);this.controls.maxPolarAngle=Math.PI*.48;this.controls.minDistance=8;this.controls.maxDistance=330;
   this.scene.add(new THREE.HemisphereLight('#ffffff','#879ba8',1.8));
   const sun=new THREE.DirectionalLight('#fff4e3',2.7);sun.position.set(-45,110,65);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-110,right:110,top:100,bottom:-100,near:1,far:250});sun.shadow.bias=-.0006;sun.shadow.normalBias=.08;sun.shadow.radius=4;this.scene.add(sun);
   const fill=new THREE.DirectionalLight('#e5f3ff',.7);fill.position.set(60,70,-70);this.scene.add(fill);
   this.buildArchitecture();this.buildStorage();this.buildOperations();this.buildRobots();this.optimizeGeometry();this.scene.add(this.routes,this.parcelGroup,this.selection,this.heatGroup);
   this.resizeObserver=new ResizeObserver(()=>this.resize());this.resizeObserver.observe(host);this.resize();
   let down={x:0,y:0};this.renderer.domElement.addEventListener('pointerdown',e=>down={x:e.clientX,y:e.clientY});
   this.renderer.domElement.addEventListener('pointerup',e=>{if(Math.hypot(e.clientX-down.x,e.clientY-down.y)<5)this.pick(e)});
 }
 material(color:string,roughness=.7,metalness=0){const key=color+roughness+metalness;if(!this.mats.has(key))this.mats.set(key,new THREE.MeshStandardMaterial({color,roughness,metalness}));return this.mats.get(key)!}
 mesh(w:number,h:number,d:number,x:number,y:number,z:number,color:string,parent:THREE.Object3D=this.scene){const m=new THREE.Mesh(this.boxGeometry,this.material(color));m.scale.set(w,h,d);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m}
 cylinder(radius:number,height:number,x:number,y:number,z:number,color:string,parent:THREE.Object3D=this.scene){const m=new THREE.Mesh(new THREE.CylinderGeometry(radius,radius,height,12),this.material(color));m.position.set(x,y,z);m.castShadow=true;parent.add(m);return m}
 text(text:string,w:number,h:number,x:number,y:number,z:number,color='#60707c',size=48,parent:THREE.Object3D=this.scene,flat=true){
   const map=texture((c,cw,ch)=>{c.clearRect(0,0,cw,ch);c.fillStyle=color;c.font=`600 ${size}px Arial`;c.textAlign='center';c.textBaseline='middle';c.fillText(text,cw/2,ch/2)},1024,128);
   const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({map,transparent:true,depthWrite:false,side:THREE.DoubleSide}));m.position.set(x,y,z);if(flat)m.rotation.x=-Math.PI/2;parent.add(m);return m;
 }
 floorLine(x:number,z:number,w:number,d:number,color='#e2bd4a'){return this.mesh(w,.025,d,x,.06,z,color)}
 buildArchitecture(){
   const ground=new THREE.Mesh(new THREE.PlaneGeometry(1000,1000),this.material('#e7edf0'));ground.rotation.x=-Math.PI/2;ground.position.y=-1.3;ground.receiveShadow=true;this.scene.add(ground);
   const slab=this.mesh(168,1.2,85,0,-.65,1,'#bcc7ce');slab.receiveShadow=true;
   const floorMap=texture((c,w,h)=>{c.fillStyle='#e4e8e6';c.fillRect(0,0,w,h);c.strokeStyle='#cfd7d4';c.lineWidth=1;for(let i=0;i<=16;i++){c.beginPath();c.moveTo(i*w/16,0);c.lineTo(i*w/16,h);c.stroke();c.beginPath();c.moveTo(0,i*h/16);c.lineTo(w,i*h/16);c.stroke()}},1024,1024);floorMap.wrapS=floorMap.wrapT=THREE.RepeatWrapping;floorMap.repeat.set(3,1.5);
   const floor=new THREE.Mesh(new THREE.PlaneGeometry(167,84),new THREE.MeshStandardMaterial({map:floorMap,roughness:.95}));floor.rotation.x=-Math.PI/2;floor.position.set(0,-.02,1);floor.receiveShadow=true;this.scene.add(floor);
   // Low perimeter walls keep the entire industrial cutaway visible.
   this.mesh(168,2.4,.65,0,1.1,-41,'#f8fafb');this.mesh(.65,2.4,84,84,1.1,1,'#f8fafb');
   for(let x=-80;x<=80;x+=16){this.mesh(.6,5,.8,x,2.5,-40.5,'#b5c1c9');this.mesh(.8,.4,.9,x,5.1,-40.5,'#d4dce0')}
   for(const z of [-32,32])this.floorLine(0,z,161,.16,'#f4edc3');
   for(let x=-72;x<=72;x+=9){this.text('›',1.2,1,x,.08,33,'#e3bc41',96);this.text('‹',1.2,1,x,.08,-33,'#e3bc41',96)}
   this.text('STORAGE / Z1–Z4',26,2.1,18,.09,-37,'#7d8b90',55);
   this.text('ROBOT TRANSIT',17,1.6,21,.09,37,'#9ba7a9',50);
   this.scene.add(this.labels);
   for(let i=0;i<16;i++){const x=-72+(i<7?i*9:68.8+(i-7)*9);this.text(String(i+1).padStart(2,'0'),3.2,1.1,x,.08,-35.3,'#8c999e',60,this.labels)}
 }
 buildStorage(){
   const shelves:{p:number[];s:number[];color:string}[]=[],posts:typeof shelves=[],beams:typeof shelves=[];
   const boxPositions:{p:number[];s:number[];id:string;color:string}[]=[];
   const colors=['#c99347','#dca653','#c98737','#b98138','#e0b56a','#b98c55'];
   for(const l of this.data.locations){
     const y=(l.level-1)*1.45+.6,w=3,depth=l.level<=2?1.5:4.5;
     shelves.push({p:[l.x,y,l.z],s:[w,.12,depth],color:'#a9b5b8'});this.rackIDs.push(l.id);
     for(const dz of [-depth/2,depth/2])beams.push({p:[l.x,y+.02,l.z+dz],s:[3,.19,.09],color:'#c35b2e'});
     // Each level has its own structural posts, instanced to avoid individual draw calls.
     for(const dx of [-1.46,1.46])for(const dz of [-depth/2+.04,depth/2-.04])posts.push({p:[l.x+dx,y+.66,l.z+dz],s:[.09,1.45,.09],color:'#546d77'});
     const available=(this.sim.locationStock.get(l.id)??[]).reduce((n,s)=>n+s.remaining,0);
     for(let k=0;k<available;k++){
       const col=k%3,row=Math.floor(k/3)%3,layer=Math.floor(k/9),bw=.69,bd=depth/3*.78,bh=.43+((k+l.source[0])%3)*.04;
       boxPositions.push({p:[l.x+(col-1)*.89,y+.09+bh/2+layer*.51,l.z+(row-1)*depth/3],s:[bw,bh,bd],id:l.id,color:colors[(l.source[0]+l.source[1]+k)%colors.length]});
     }
   }
   const instance=(list:typeof shelves)=>{const m=new THREE.InstancedMesh(this.boxGeometry,this.material('#ffffff',.72,.12),list.length);list.forEach((v,i)=>{temp.position.set(v.p[0],v.p[1],v.p[2]);temp.scale.set(v.s[0],v.s[1],v.s[2]);temp.updateMatrix();m.setMatrixAt(i,temp.matrix);m.setColorAt(i,new THREE.Color(v.color))});m.castShadow=true;m.receiveShadow=true;this.scene.add(m);return m};
   const shadowMap=texture((c,w,h)=>{c.clearRect(0,0,w,h);c.filter='blur(18px)';c.fillStyle='#000';c.fillRect(60,50,w-120,h-100)},512,256);
   const footprints=new Map<string,{x:number;z:number;d:number}>();for(const l of this.data.locations){const key=l.x+':'+l.z;const old=footprints.get(key);footprints.set(key,{x:l.x,z:l.z,d:Math.max(old?.d??0,l.level<=2?1.5:4.5)})}
   const contact=new THREE.InstancedMesh(new THREE.PlaneGeometry(1,1),new THREE.MeshBasicMaterial({map:shadowMap,transparent:true,opacity:.2,depthWrite:false}),footprints.size);
   [...footprints.values()].forEach((p,i)=>{temp.position.set(p.x,.025,p.z);temp.rotation.set(-Math.PI/2,0,0);temp.scale.set(4.4,p.d+1.6,1);temp.updateMatrix();contact.setMatrixAt(i,temp.matrix)});this.scene.add(contact);temp.rotation.set(0,0,0);
   const sm=instance(shelves);sm.userData.kind='rack';this.rackMeshes.push(sm);sm.name='Rack shelves';instance(beams).name='Rack beams';instance(posts).name='Rack posts';
   const boxMap=texture((c,w,h)=>{c.fillStyle='#ffffff';c.fillRect(0,0,w,h);c.fillStyle='#e3d5ba';c.fillRect(w*.46,0,w*.09,h);c.strokeStyle='#775e3c';c.lineWidth=2;c.strokeRect(2,2,w-4,h-4);c.fillStyle='#f8f1df';c.fillRect(w*.1,h*.27,w*.27,h*.48);c.fillStyle='#3c3a33';c.font='bold 22px Arial';c.fillText('WL',w*.13,h*.43);for(let i=0;i<17;i++)c.fillRect(w*.13+i*6,h*.53,1+i%3,h*.13);c.font='18px Arial';c.fillText('↑ ↑',w*.74,h*.82)},512,256);
   this.boxes=new THREE.InstancedMesh(this.boxGeometry,new THREE.MeshStandardMaterial({map:boxMap,roughness:.9}),boxPositions.length);
   boxPositions.forEach((v,i)=>{temp.position.set(v.p[0],v.p[1],v.p[2]);temp.scale.set(v.s[0],v.s[1],v.s[2]);temp.updateMatrix();this.boxes.setMatrixAt(i,temp.matrix);this.boxBase.push(temp.matrix.clone());this.boxes.setColorAt(i,new THREE.Color(v.color));this.boxLocations.push(v.id);const list=this.boxByLocation.get(v.id)??[];list.push(i);this.boxByLocation.set(v.id,list)});
   this.boxes.castShadow=true;this.boxes.receiveShadow=true;this.boxes.userData.kind='inventory';this.scene.add(this.boxes);
 }
 buildOperations(){
   // Synthetic equipment in the source layout's open south-east floor area.
   this.mesh(39,.06,34,-53,.025,13,'#d4ded9');
   for(const [i,p] of STATIONS.entries()){
     this.floorLine(p.x,16,9,12,'#c7d7d5');
     for(const z of [10,22])this.floorLine(p.x,z,9,.13,'#f3c54d');for(const x of [p.x-4.5,p.x+4.5])this.floorLine(x,16,.13,12,'#f3c54d');
     this.mesh(5,1.5,2.5,p.x,1,9,'#af3f32');this.mesh(5.4,.18,2.8,p.x,1.85,9,'#d5dedd');
     this.mesh(.12,1,.12,p.x+1.7,2.4,8.8,'#667984');this.mesh(1.1,.7,.18,p.x+1.7,2.9,8.8,'#283d45');this.mesh(.9,.45,.2,p.x+1.7,2.9,8.94,'#68b6ae');
     this.text(`PACK ${String(i+1).padStart(2,'0')}`,7,1.2,p.x,.08,24,'#6c8d83',62);
     this.mesh(3,1.6,15,p.x,1.1,1,'#687c80');this.mesh(2.6,.15,15,p.x,2,1,'#3e4d50');
     for(let z=-6;z<=8;z+=.65)this.mesh(2.5,.12,.2,p.x,2.11,z,'#b1bcba');
     for(const x of [p.x-1.65,p.x+1.65])this.mesh(.16,.7,15,x,2,1,'#b94435');
     for(let k=0;k<4;k++)this.mesh(.2,2,.2,p.x-1.25,1,6-k*3,'#718486');
   }
   this.text('OUTBOUND',21,2,-52,.09,-12,'#74978b',70);
   // Receiving pallets, dock doors, and protective bollards.
   this.text('RECEIVING',14,1.5,-29,.09,25,'#9b8c62',65);
   for(let i=0;i<5;i++){
     const x=-34+i%2*5,z=6+Math.floor(i/2)*5;
     for(let k=0;k<3;k++)this.mesh(3.5,.18,.7,x,.16,z+(k-1)*.9,'#9d8054');
     for(let k=0;k<6;k++)this.mesh(1.25,.8,.85,x+(k%2-.5)*1.4,.65+Math.floor(k/4)*.9,z+(Math.floor(k/2)%2-.5)*1,'#c49a5a');
   }
   for(let i=0;i<3;i++){
     const x=-61+i*12;
     this.mesh(9,3,.5,x,1.5,42.7,'#f0f3f1');this.mesh(6.7,2.6,.55,x,1.4,43,'#7b9299');
     for(let k=0;k<6;k++)this.mesh(6.5,.06,.1,x,.4+k*.4,43.32,'#adc0c5');
     this.text(`DOCK 0${i+1}`,5,1,x,.08,39,'#758c94',60);
     for(const dx of [-4,4]){this.cylinder(.18,1.5,x+dx,.75,40,'#e9b946');this.cylinder(.19,.2,x+dx,.95,40,'#343d3f')}
   }
   // A parked forklift; it never invents an inbound inventory event.
   const forklift=new THREE.Group();forklift.position.set(-18,0,25);this.scene.add(forklift);
   this.mesh(2,1.1,3,0,.85,0,'#c74d32',forklift);this.mesh(1.5,.4,1.5,0,1.6,.1,'#374647',forklift);this.mesh(2.3,.18,2.8,0,3.6,0,'#df6141',forklift);
   for(const x of [-.9,.9]){this.mesh(.12,2,.12,x,2.5,-.9,'#404e50',forklift);this.mesh(.18,3.8,.2,x,1.9,1.8,'#49595c',forklift);this.mesh(.25,.14,2.5,x,.3,2.6,'#5c6b6b',forklift);for(const z of [-1,1])this.cylinder(.43,.3,x,.45,z,'#303c3e',forklift).rotation.z=Math.PI/2}
   this.text('AMR CHARGING',21,1.4,-58,.09,31,'#8b9c9d',58);
   for(let i=0;i<10;i++){const x=-68+i*2;this.mesh(1.25,.06,1.4,x,.07,26,'#b9cdcb');this.mesh(1.15,.7,.25,x,.35,27.3,'#4d7a77')}
 }
 buildRobots(){
   for(const r of this.sim.robots){
     const g=new THREE.Group();g.userData.robot=r.id;g.position.set(r.x,0,r.z);this.scene.add(g);this.robots.push(g);
     this.mesh(.78,.24,.78,0,.25,0,'#247c78',g);this.mesh(.72,.12,.72,0,.42,0,'#daf1e5',g);this.mesh(.65,.06,.65,0,.52,0,'#4b6060',g);
     for(const x of [-.36,.36])for(const z of [-.26,.26]){const wheel=this.cylinder(.12,.12,x,.17,z,'#293d40',g);wheel.rotation.z=Math.PI/2}
     this.mesh(.25,.05,.04,0,.37,.4,'#b8ffdd',g);this.cylinder(.06,.08,0,.57,0,'#e6be45',g);
     const cargo=this.mesh(.59,.43,.5,0,.76,0,'#d2a05d',g);cargo.name='cargo';cargo.visible=false;
     const labelMap=texture((c,w,h)=>{c.fillStyle='#ffffff';c.beginPath();c.roundRect(4,4,w-8,h-8,28);c.fill();c.strokeStyle='#c9d9d7';c.lineWidth=4;c.stroke();c.fillStyle='#176f67';c.font='bold 70px Arial';c.textAlign='center';c.textBaseline='middle';c.fillText(`R${String(r.id).padStart(2,'0')}`,w/2,h/2)},256,128);
     const label=new THREE.Sprite(new THREE.SpriteMaterial({map:labelMap,transparent:true,depthTest:false}));label.position.y=1.6;label.scale.set(1.8,.9,1);g.add(label);this.robotLabels.push(label);
     const ring=new THREE.Mesh(new THREE.RingGeometry(.67,.77,32),new THREE.MeshBasicMaterial({color:'#2ca18d',transparent:true,opacity:.7,side:THREE.DoubleSide}));ring.rotation.x=-Math.PI/2;ring.position.y=.07;ring.name='ring';g.add(ring);
   }
 }
 optimizeGeometry(){
   const statics=this.scene.children.filter((o):o is THREE.Mesh=>o instanceof THREE.Mesh&&!(o instanceof THREE.InstancedMesh)&&o.geometry===this.boxGeometry&&!o.userData.kind);
   const batch=new THREE.InstancedMesh(this.boxGeometry,this.material('#ffffff'),statics.length);
   statics.forEach((m,i)=>{m.updateMatrix();batch.setMatrixAt(i,m.matrix);batch.setColorAt(i,(m.material as THREE.MeshStandardMaterial).color);this.scene.remove(m)});batch.castShadow=true;batch.receiveShadow=true;this.scene.add(batch);
   let bodyGeometry:THREE.BufferGeometry|undefined;
   for(const g of this.robots){const parts=g.children.filter((o):o is THREE.Mesh=>o instanceof THREE.Mesh&&o.name!=='cargo'&&o.name!=='ring');
     if(!bodyGeometry){const geometries=parts.map(m=>{m.updateMatrix();const geo=m.geometry.clone().applyMatrix4(m.matrix),color=(m.material as THREE.MeshStandardMaterial).color;const colors=new Float32Array(geo.getAttribute('position').count*3);for(let i=0;i<colors.length;i+=3){colors[i]=color.r;colors[i+1]=color.g;colors[i+2]=color.b}geo.setAttribute('color',new THREE.BufferAttribute(colors,3));return geo});bodyGeometry=mergeGeometries(geometries)!;geometries.forEach(g=>g.dispose())}
     parts.forEach(m=>g.remove(m));const body=new THREE.Mesh(bodyGeometry,new THREE.MeshStandardMaterial({vertexColors:true,roughness:.65,metalness:.1}));body.castShadow=true;body.receiveShadow=true;g.add(body);
   }
 }
 resize(){const {width,height}=this.host.getBoundingClientRect();this.camera.aspect=width/height;this.camera.updateProjectionMatrix();this.renderer.setSize(width,height)}
 view(mode:'iso'|'top'|'outbound'){this.follow=false;this.controls.target.set(mode==='outbound'?-51:0,0,mode==='outbound'?10:0);this.camera.position.set(...(mode==='top'?[0,210,.01]:mode==='outbound'?[-10,65,75]:[120,140,155]) as [number,number,number]);this.controls.update()}
 selectRobot(id:number){this.selectedRobot=id;this.selectedLocation=undefined;this.highlight();this.lastRoute=''}
 selectLocation(id:string){this.selectedLocation=id;this.selectedRobot=undefined;this.follow=false;this.highlight();this.lastRoute=''}
 highlight(){this.clearGroup(this.selection);if(this.selectedLocation){const l=this.data.locations.find(l=>l.id===this.selectedLocation)!;const box=new THREE.Box3(new THREE.Vector3(l.x-1.55,(l.level-1)*1.45+.55,l.z-(l.level<=2?.8:2.3)),new THREE.Vector3(l.x+1.55,l.level*1.45+.7,l.z+(l.level<=2?.8:2.3)));const h=new THREE.Box3Helper(box,0x21a695);this.selection.add(h)}}
 clearGroup(group:THREE.Group){while(group.children.length){const c=group.children[0] as THREE.Mesh;group.remove(c);c.geometry?.dispose();if(c.material)for(const m of Array.isArray(c.material)?c.material:[c.material])m.dispose()}}
 pick(e:PointerEvent){const rect=this.renderer.domElement.getBoundingClientRect();this.pointer.set((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1);this.raycaster.setFromCamera(this.pointer,this.camera);
   const robotHit=this.raycaster.intersectObjects(this.robots,true)[0];if(robotHit){let o=robotHit.object;while(o.parent&&!o.userData.robot)o=o.parent;if(o.userData.robot){this.onSelect('robot',String(o.userData.robot));return}}
   const hit=this.raycaster.intersectObjects([this.boxes,...this.rackMeshes])[0];if(hit?.instanceId!==undefined)this.onSelect('location',hit.object===this.boxes?this.boxLocations[hit.instanceId]:this.rackIDs[hit.instanceId]);
 }
 updateInventory(){if(this.lastStock===this.sim.stockTotal)return;this.lastStock=this.sim.stockTotal;
   for(const [loc,ids] of this.boxByLocation){let count=(this.sim.locationStock.get(loc)??[]).reduce((n,s)=>n+s.remaining,0);for(let k=0;k<ids.length;k++){const i=ids[k];if(k<count)this.boxes.setMatrixAt(i,this.boxBase[i]);else{temp.position.set(0,-100,0);temp.scale.set(0,0,0);temp.updateMatrix();this.boxes.setMatrixAt(i,temp.matrix)}}}this.boxes.instanceMatrix.needsUpdate=true;
 }
 updateRoutes(){const robots=this.selectedRobot?[this.sim.robots[this.selectedRobot-1]]:this.sim.robots;const key=robots.map(r=>r.id+':'+r.cell+':'+r.route.join(',')).join('|')+this.showRoutes;if(key===this.lastRoute)return;this.lastRoute=key;this.clearGroup(this.routes);if(!this.showRoutes)return;
   for(const r of robots){if(!r.route.length)continue;const points=[new THREE.Vector3(r.x,.18,r.z),...r.route.map(n=>{const p=this.sim.grid.point(n);return new THREE.Vector3(p.x,.18,p.z)})];const line=new THREE.Line(new THREE.BufferGeometry().setFromPoints(points),new THREE.LineBasicMaterial({color:r.carrying?'#d69036':'#239e8b',transparent:true,opacity:this.selectedRobot?.9:.4}));this.routes.add(line)}
 }
 updateHeat(){this.heatGroup.visible=this.heat;if(!this.heat||this.sim.time-this.lastHeat<5)return;this.lastHeat=this.sim.time;this.clearGroup(this.heatGroup);const entries=[...this.sim.traffic.entries()].filter(([,v])=>v>1);if(!entries.length)return;const max=Math.max(...entries.map(([,v])=>v));const mesh=new THREE.InstancedMesh(new THREE.PlaneGeometry(.9,.9),new THREE.MeshBasicMaterial({transparent:true,opacity:.65,depthWrite:false,side:THREE.DoubleSide}),entries.length);entries.forEach(([n,v],i)=>{const p=this.sim.grid.point(n);temp.position.set(p.x,.12,p.z);temp.rotation.set(-Math.PI/2,0,0);temp.scale.set(1,1,1);temp.updateMatrix();mesh.setMatrixAt(i,temp.matrix);mesh.setColorAt(i,new THREE.Color().setHSL(.13*(1-v/max),.8,.55))});temp.rotation.set(0,0,0);this.heatGroup.add(mesh)}
 render(delta:number,alpha=1){
   this.updateInventory();this.updateRoutes();this.updateHeat();
   for(let i=0;i<this.robots.length;i++){
     const r=this.sim.robots[i],g=this.robots[i];g.position.set((r.previousX??r.x)+(r.x-(r.previousX??r.x))*alpha,0,(r.previousZ??r.z)+(r.z-(r.previousZ??r.z))*alpha);
     if(r.edge){const a=this.sim.grid.point(r.edge.from),b=this.sim.grid.point(r.edge.to);g.rotation.y=Math.atan2(b.x-a.x,b.z-a.z)}
     const cargo=g.getObjectByName('cargo')!;cargo.visible=r.carrying||r.status==='PICKING';
     if(r.status==='PICKING'){const progress=1-r.timer/this.sim.config.pickTime;cargo.scale.set(.59,.43,.5).multiplyScalar(Math.min(1,progress*3));cargo.position.y=.76+Math.sin(progress*Math.PI)*1.2}else if(r.status==='UNLOADING'){const progress=1-r.timer/this.sim.config.unloadTime;cargo.position.y=.76+progress*.9;cargo.scale.set(.59,.43,.5).multiplyScalar(Math.max(.1,1-progress))}else{cargo.position.y=.76;cargo.scale.set(.59,.43,.5)}
     const ring=g.getObjectByName('ring') as THREE.Mesh;ring.scale.setScalar(this.selectedRobot===r.id?1.8:1);(ring.material as THREE.MeshBasicMaterial).opacity=this.selectedRobot===r.id?1:.38;
   }
   // Every parcel is derived from a delivery event, using simulation time only.
   const deliveries=this.sim.events.filter(e=>e.type==='delivered'&&this.sim.time-e.time<16);
   while(this.parcels.length<deliveries.length){const m=new THREE.Mesh(new THREE.BoxGeometry(.9,.65,.8),this.material('#ce9a52'));m.castShadow=true;this.parcelGroup.add(m);this.parcels.push(m)}
   this.parcels.forEach((m,i)=>{m.visible=i<deliveries.length;if(m.visible){const e=deliveries[i],p=STATIONS[Number(e.detail)];m.position.set(p.x,2.5,8-(this.sim.time-e.time))}});
   if(this.follow&&this.selectedRobot){const r=this.sim.robots[this.selectedRobot-1],target=this.robots[r.id-1].position.clone();const diff=target.clone().sub(this.controls.target).multiplyScalar(Math.min(1,delta*4));this.controls.target.add(diff);this.camera.position.add(diff)}
   this.controls.update();this.renderer.render(this.scene,this.camera);this.drawCalls=this.renderer.info.render.calls;this.frameCount++;const now=performance.now();if(now-this.lastFps>=1000){this.fps=Math.round(this.frameCount*1000/(now-this.lastFps));this.frameCount=0;this.lastFps=now}
 }
 replaceSimulation(sim:Simulation){this.sim=sim;this.lastStock=-1;this.lastRoute='';this.lastHeat=-10;this.selectedRobot=undefined;this.selectedLocation=undefined;this.follow=false;this.clearGroup(this.selection)}
}
