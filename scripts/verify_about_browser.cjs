const {chromium}=require('playwright');
const fs=require('fs');
const path=require('path');
const output=process.env.ABOUT_ARTIFACT_DIR || 'reports/tmp/about';
const base=process.env.ABOUT_BASE_URL || 'http://127.0.0.1:4173';
fs.mkdirSync(output,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true,channel:process.env.ABOUT_BROWSER_CHANNEL || undefined});
 const results=[];
 for(const width of [390,768,1440]){
  const page=await browser.newPage({viewport:{width,height:1000},reducedMotion:'reduce'});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`${base}/about/`);await page.evaluate(()=>document.fonts.ready);
  await page.screenshot({path:path.join(output,`about-${width}.png`),fullPage:true});
  if(await page.locator('h1').count()!==1)throw Error('h1');
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('overflow '+width);
  const summary=page.locator('#disclosure-index > summary');await summary.focus();await page.keyboard.press('Enter');
  if(!(await page.locator('#disclosure-index').getAttribute('open')!==null))throw Error('keyboard disclosure');
  await page.locator('#disclosure-search').fill('CVE-2024-2793');
  if(await page.locator('#disclosure-records > li:visible').count()!==1)throw Error('CVE filter');
  await page.getByRole('button',{name:'Clear',exact:true}).click();
  if(await page.locator('#disclosure-records > li:visible').count()!==40)throw Error('reset');
  await page.locator('#disclosure-severity').selectOption('High');
  if(await page.locator('#disclosure-records > li:visible').count()!==3)throw Error('severity');
  await page.locator('#disclosure-search').fill('no-such-product');
  if(!(await page.locator('#disclosure-empty').isVisible()))throw Error('empty');
  await page.getByRole('button',{name:'Clear',exact:true}).click();
  await page.addScriptTag({path:require.resolve('axe-core/axe.min.js')});
  const axe=await page.evaluate(async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}}));
  results.push({width,errors,violations:axe.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})),checks:'search, severity, reset, empty state, keyboard disclosure, overflow'});
  if(width===1440)await page.screenshot({path:path.join(output,'about-index-desktop.png'),fullPage:true});
  await page.close();
 }
 const nojs=await browser.newPage({javaScriptEnabled:false,viewport:{width:390,height:844}});await nojs.goto(`${base}/about/`);await nojs.locator('#disclosure-index > summary').click();if(await nojs.locator('#disclosure-records > li:visible').count()!==40)throw Error('no JS records');if(await nojs.locator('.about-filter').isVisible())throw Error('no JS filter');
 fs.writeFileSync(path.join(output,'about-browser-checks.json'),JSON.stringify({results,noJavaScript:'40 readable disclosures; native toggle works'},null,2));
 console.log(JSON.stringify(results));await browser.close();
 if(results.some(r=>r.violations.length || r.errors.length))process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
