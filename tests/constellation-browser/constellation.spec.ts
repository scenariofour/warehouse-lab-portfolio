import {test,expect} from '@playwright/test';
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
const route='/docs/control-tower/anatomy/';
const model=JSON.parse(readFileSync('docs/control-tower/anatomy/data.js','utf8').replace('window.CONSTELLATION = ','').replace(/;\s*$/,''));
const review='docs/control-tower/anatomy/review/';

test('registered network, source-backed selection, hover, reset and keyboard',async({page})=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(route);await page.evaluate(()=>document.fonts.ready);
  await expect(page.locator('.node')).toHaveCount(30);await expect(page.locator('.edge')).toHaveCount(47);
  for(const context of model.issue_context){
    await page.locator('#issue-select').selectOption(context.issue_id);
    await expect(page.locator('.issue-title')).toHaveText(context.title);
    const edges=model.edges.filter((e:any)=>e.issue_id===context.issue_id);
    expect(await page.locator('.edge.active').evaluateAll(els=>els.map(e=>e.getAttribute('data-edge')).sort())).toEqual(edges.map((e:any)=>e.edge_id).sort());
    expect(await page.locator('.node.active').evaluateAll(els=>els.map(e=>e.getAttribute('data-node')).sort())).toEqual([...new Set(edges.flatMap((e:any)=>[e.from_node,e.to_node]))].sort());
    await expect(page.locator('#context')).toContainText(context.business_decision);
    await expect(page.locator('#context')).toContainText(context.next_evidence_request);
    await expect(page.locator('.explanations li')).toHaveCount(context.competing_explanations.split('|').length);
  }
  await page.locator('[data-node="DQ-DUP-CUSTOMER"]').focus();await page.keyboard.press('Enter');
  await page.locator('summary').filter({hasText:'Inspect the evidence trail'}).click();
  await expect(page.locator('.ledger')).toContainText('AFFECTED + CONTRIBUTING_POPULATION');
  const source=page.locator('[data-node="S:Customer_Order.csv"]');await source.hover();
  await expect(page.locator('#tooltip')).toBeVisible();
  expect(await page.locator('.edge.hovered').evaluateAll(els=>els.map(e=>e.getAttribute('data-edge')).sort())).toEqual(model.edges.filter((e:any)=>e.source_id==='Customer_Order.csv').map((e:any)=>e.edge_id).sort());
  await page.locator('h1').hover();await expect(page.locator('#tooltip')).toBeHidden();
  await expect(page.locator('.edge.hovered')).toHaveCount(0);
  await page.locator('#reset').click();await expect(page.locator('.edge.active')).toHaveCount(47);
  await expect(page.locator('#context')).toHaveAttribute('data-issue','__ALL__');
  await page.locator('[data-node="DQ-STOCK-001"]').focus();await page.keyboard.press('Space');
  await expect(page.locator('#context')).toContainText('Stock payload units and snapshot alignment unresolved');
  await page.keyboard.press('Escape');await expect(page.locator('#tooltip')).toBeHidden();
  expect(errors).toEqual([]);
});

for(const viewport of [{width:1600,height:1000},{width:1440,height:900}]){
  test(`desktop composition ${viewport.width}: focal area and actual screenshots`,async({page})=>{
    await page.setViewportSize(viewport);await page.goto(route);await page.evaluate(()=>document.fonts.ready);
    const bounds=await page.locator('.constellation').boundingBox();
    expect(bounds!.width*bounds!.height/(viewport.width*viewport.height)).toBeGreaterThanOrEqual(.55);
    expect(bounds!.y+bounds!.height).toBeLessThanOrEqual(viewport.height+1);
    expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(viewport.width);
    await expect(page.locator('.next-ask')).toBeInViewport();
    await page.screenshot({path:`${review}desktop-${viewport.width}.png`});
    if(viewport.width===1600){
      await page.locator('#issue-select').selectOption('DQ-RECON-001');
      await page.screenshot({path:`${review}desktop-reconciliation.png`});
    }
  });
}

test('narrow viewport retains a native question selector without page overflow',async({page})=>{
  await page.setViewportSize({width:390,height:844});await page.goto(route);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBe(390);
  await page.locator('#issue-select').selectOption('DQ-LAYOUT-001');
  await expect(page.locator('.issue-title')).toHaveText('Physical scale and floor connectivity unresolved');
  await page.locator('#issue-select').scrollIntoViewIfNeeded();
  await page.screenshot({path:`${review}narrow.png`});
});

test('prototype also works directly from disk without external resource requests',async({page})=>{
  const external:string[]=[];
  page.on('request',request=>{if(/^https?:/.test(request.url())) external.push(request.url());});
  await page.goto(pathToFileURL(resolve('docs/control-tower/anatomy/index.html')).href);
  await expect(page.locator('.node')).toHaveCount(30);
  await page.locator('#issue-select').selectOption('DQ-ABC-001');
  await expect(page.locator('#context')).toContainText('Confirm classification objective before choosing fast movers.');
  await page.evaluate(()=>document.fonts.ready);
  expect(external).toEqual([]);
});
