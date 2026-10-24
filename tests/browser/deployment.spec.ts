import {test,expect} from '@playwright/test';

test('deployment: subpath resources, WebGL, provenance links and full demand load',async({page})=>{
 const failures:string[]=[];
 page.on('pageerror',error=>failures.push(error.message));
 page.on('console',message=>{if(message.type()==='error')failures.push(message.text())});
 page.on('requestfailed',request=>failures.push(request.url()+': '+request.failure()?.errorText));
 page.on('response',response=>{if(response.status()>=400)failures.push(response.status()+': '+response.url())});
 await page.goto('./');
 await page.waitForFunction(()=>(window as any).warehouseLab?.scene);
 await page.evaluate(()=>document.fonts.ready);
 const rendering=await page.evaluate(()=>{
  const scene=(window as any).warehouseLab.scene;
  const gl=scene.renderer.getContext();
  return {lost:gl.isContextLost(),calls:scene.renderer.info.render.calls,canvas:document.querySelectorAll('canvas').length};
 });
 expect(rendering.lost).toBe(false);expect(rendering.calls).toBeGreaterThan(0);expect(rendering.canvas).toBeGreaterThan(0);
 const resources=await page.evaluate(()=>performance.getEntriesByType('resource').map(entry=>entry.name));
 const base=new URL(page.url());
 for(const resource of resources.filter(url=>new URL(url).origin===base.origin))expect(new URL(resource).pathname.startsWith(base.pathname)).toBe(true);
 expect(resources.some(url=>url.includes('.ttf'))).toBe(true);
 await page.screenshot({path:test.info().outputPath('warehouse-overview.png'),fullPage:true});
 await page.getByRole('tab',{name:'Data & provenance',exact:true}).click();
 for(const name of ['normalized geometry and default source orders','all source demand','the full data audit']){
  const href=await page.getByRole('link',{name,exact:true}).getAttribute('href');
  expect(href?.startsWith(base.pathname)).toBe(true);
  expect((await page.request.get(href!)).status()).toBe(200);
 }
 await page.getByRole('button',{name:'Close dialog'}).click();
 await page.getByRole('tab',{name:'Experiments',exact:true}).click();
 await page.locator('#demand-window').selectOption('600');
 await expect(page.locator('#demand-label')).toHaveText('600 orders');
 expect(failures).toEqual([]);
});
