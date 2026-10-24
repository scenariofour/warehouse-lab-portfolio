import {test,expect} from '@playwright/test';

test('the opaque floor occludes its foundation at distant camera angles',async({page})=>{
 await page.goto('./');
 await page.waitForFunction(()=>(window as any).warehouseLab?.scene);
 const views=await page.evaluate(()=>{
  const s=(window as any).warehouseLab.scene,renderer=s.renderer,gl=renderer.getContext();
  s.controls.enableDamping=false;s.controls.target.set(0,0,0);
  let slab:any,index=-1,original:any;
  for(const mesh of s.scene.children.filter((o:any)=>o.isInstancedMesh&&o.geometry.type==='BoxGeometry')){
   for(let i=0;i<mesh.count;i++){
    const matrix=s.camera.matrix.clone();mesh.getMatrixAt(i,matrix);
    if(Math.abs(matrix.elements[0]-168)<.01&&Math.abs(matrix.elements[13]+.65)<.01){slab=mesh;index=i;original=matrix}
   }
  }
  if(!slab)throw Error('Warehouse foundation not found');
  return [[120,180,155],[200,170,200],[0,330,.01]].map(position=>{
   s.camera.position.set(...position);s.controls.update();s.camera.updateMatrixWorld();
   const points:number[][]=[];
   // Interior floor strip: far from the exposed slab edge, across the transit aisle.
   for(let x=-70;x<=70;x+=2)for(let z=28;z<=35;z+=.5){
    const p=s.camera.position.clone().set(x,-.02,z).project(s.camera);
    if(Math.abs(p.x)<1&&Math.abs(p.y)<1)points.push([
     Math.floor((p.x+1)*gl.drawingBufferWidth/2),Math.floor((p.y+1)*gl.drawingBufferHeight/2)
    ]);
   }
   const sample=()=>{
    renderer.render(s.scene,s.camera);
    return points.map(([x,y])=>{
     const pixel=new Uint8Array(4);gl.readPixels(x,y,1,1,gl.RGBA,gl.UNSIGNED_BYTE,pixel);return [...pixel];
    });
   };
   const visible=sample(),hidden=original.clone();
   // An opaque floor must look identical with its buried foundation removed.
   hidden.elements[13]=-100;slab.setMatrixAt(index,hidden);slab.instanceMatrix.needsUpdate=true;
   const reference=sample();
   slab.setMatrixAt(index,original);slab.instanceMatrix.needsUpdate=true;
   const changed=visible.filter((pixel,i)=>pixel.some((value,k)=>Math.abs(value-reference[i][k])>2)).length;
   return {position,samples:points.length,changed};
  });
 });
 for(const view of views){
  expect(view.samples).toBeGreaterThan(1000);
  expect(view.changed,`foundation bleeding through the floor at ${view.position}`).toBe(0);
 }
 await page.locator('#viewport').screenshot({path:test.info().outputPath('floor-depth.png')});
});
