const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert');
const root=process.argv[2],report=process.argv[3]||'/tmp/sinter-v3-browser.json';
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH});
const results=[];
try {
 for(const ev of fs.readdirSync(root).filter(x=>x.startsWith('eval-')).sort()){
  const out=path.join(root,ev,'with_skill/run-1/outputs'),domain=fs.readdirSync(out).find(x=>x.startsWith('dominio-'));
  const page=await browser.newPage({viewport:{width:1440,height:1000}}), errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('file://'+path.join(out,domain,'site/index.html'),{waitUntil:'networkidle',timeout:30000});
  await page.locator('#doc h1').waitFor();
  const pages=await page.locator('nav a[data-p]').evaluateAll(as=>[...new Set(as.map(a=>a.dataset.p))].filter(x=>x.endsWith('.md')));
  const checks=[];
  for(const name of pages){
   await page.locator(`nav a[data-p="${name}"]`).first().click();
   await page.waitForFunction(() => [...document.querySelectorAll('#doc .mermaid')].every(d => d.querySelector('svg')), {timeout:20000});
   const state=await page.evaluate(()=>{const ids=[...document.querySelectorAll('#doc [id]')].map(e=>e.id);return {duplicates:ids.filter((id,i)=>ids.indexOf(id)!==i),h1:document.querySelector('#doc h1')?.textContent,syntaxErrors:document.querySelectorAll('#doc .error-icon,#doc .error-text').length,rawDiagrams:document.querySelectorAll('#doc code.language-mermaid').length};});
   assert.equal(state.duplicates.length,0,domain+': duplicated IDs in '+name);
   assert.equal(state.syntaxErrors,0,domain+': Mermaid error in '+name);
   checks.push({page:name,...state});
  }
  await page.locator('nav a[data-p="3-servicos.md"]').first().click();
  const anchors=await page.locator('nav a[data-p="3-servicos.md"][data-a]').evaluateAll(as=>as.filter(a=>a.textContent.includes('Consome')).map(a=>a.dataset.a));
  for(const anchor of anchors){
   const parent=await page.locator(`nav a[data-p="3-servicos.md"][data-a="${anchor}"]`).getAttribute('data-pai');
   if(parent) await page.locator(`nav a[data-p="3-servicos.md"][data-a="${parent}"]`).click();
   await page.locator(`nav a[data-p="3-servicos.md"][data-a="${anchor}"]`).click();
   assert.equal(await page.locator(`#doc [data-anchor="${anchor}"]`).count(),1,domain+': anchor not unique '+anchor);
  }
  await page.locator('nav a[data-p="1-negocio.md"]').first().click();
  const links=await page.locator('#doc a[href]').evaluateAll(as=>as.map(a=>a.getAttribute('href')).filter(h=>h.includes('6-referencia.md')));
  assert(links.length,domain+': business should reference canonical definitions');
  if(links.length){await page.locator(`#doc a[href="${links[0]}"]`).first().click();await page.waitForTimeout(150);assert(page.url().includes('/site/index.html'),domain+': content link left HTML');assert((await page.locator('#doc h1').innerText()).includes('Referência'),domain+': reference link target');}
  await page.locator('#tema').click();assert.equal(await page.locator('html').getAttribute('data-tema'),'escuro');
  await page.locator('#tema').click();assert.equal(await page.locator('html').getAttribute('data-tema'),'claro');
  await page.setViewportSize({width:390,height:844});await page.waitForTimeout(100);
  const mobile=await page.evaluate(()=>({width:innerWidth,body:document.body.scrollWidth,doc:document.documentElement.scrollWidth}));
  mobile.pass=mobile.doc <= mobile.width+2;
  if(!mobile.pass) mobile.offenders=await page.evaluate(()=>[...document.body.children].map(e=>({tag:e.tagName,id:e.id,cl:e.className,right:e.getBoundingClientRect().right,html:e.outerHTML.slice(0,250)})).filter(e=>e.right>innerWidth+2));
  results.push({domain,pages:checks,anchors:anchors.length,contentLinkTested:links.length>0,mobile,errors});
  assert.equal(errors.length,0,domain+': errors '+errors.join(';'));
  await page.screenshot({path:'/tmp/'+domain+'-v3-mobile.png',fullPage:false});
  await page.close();
 }
 fs.writeFileSync(report,JSON.stringify({status:results.every(x=>x.mobile.pass)?'pass':'fail',results},null,2));console.log(JSON.stringify(results,null,2)); if(results.some(x=>!x.mobile.pass)) process.exitCode=1;
} finally {await browser.close();}
})().catch(e=>{fs.writeFileSync(report,JSON.stringify({status:'fail',error:e.stack,},null,2));console.error(e.stack);process.exit(1)});
