const fs=require('node:fs');const {pathToFileURL}=require('node:url');const path=require('node:path');
const {chromium}=require('C:/Users/imsup/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});const page=await browser.newPage({viewport:{width:1024,height:768}});const errors=[];page.on('pageerror',e=>errors.push(e.message));const results=[];
for(const file of ['prototype/index.html','review/07-system-sample-v1.html']){
 await page.goto(pathToFileURL(path.resolve(file)).href);await page.waitForTimeout(800);
 const checks=await page.evaluate(()=>{
  const out=[];const assert=(ok,label)=>{out.push({label,pass:Boolean(ok)});};
  assert(missalOrdinary.penitentialForms.length===3,'three independent penitential forms');
  for(let i=0;i<3;i++){penitentialView=i;const n=renderPenitential();assert(n.getAttribute('class').includes('reader__item')&&n.querySelector('[data-missal-form]')?.getAttribute('data-missal-form')==='form-'+(i+1),'form '+(i+1)+' renderer');assert(n.textContent.includes('사죄가 이어진다.'),'form '+(i+1)+' absolution instruction');if(i===1)assert(n.textContent.includes('저희는 주님께 죄를 지었나이다.')&&!n.textContent.includes('원문 자료 미연결'),'missing second form filled');if(i===2)assert(!n.textContent.includes('가슴을 치며'),'third form does not leak first form gestures');}penitentialView=0;
  for(const mode of ['beginner','regular']){find('mode').value=mode;for(let partIndex=0;partIndex<4;partIndex++){const blocks=flowBlocks(partIndex);for(const block of blocks){const node=renderBlock(block);assert(!node.textContent.includes('[원문 지침]'),mode+' '+block.key+' rubric prefix stripped');}assert(blocks.length>0,mode+' part '+partIndex+' rendered');}const node=liturgyNode(referenceText('참회 예식 제1양식'));assert(node.querySelectorAll('[data-source-kind="missal-rubric"]').length>=4,mode+' original rubrics retained');assert(node.textContent.includes('가슴을 치며 말한다.'),mode+' gesture visible');}
  assert(!referenceText('감사 기도').includes('종을 치면'),'unverified bell/bowing instructions removed');assert(!referenceText('감사 기도').includes('레오14세'),'personal names are source placeholders');
  assert(referenceText('감사 기도').indexOf('사제는 허리를 조금 굽힌다.')<referenceText('감사 기도').indexOf('너희는 모두 이것을 받아 먹어라.'),'institution rubric anchored before words');
  return out;
 });results.push({file,checks});
}
await page.screenshot({path:'work/browser-qa/missal-rubrics.png',fullPage:false});await browser.close();const fail=results.flatMap(r=>r.checks.filter(x=>!x.pass).map(x=>({file:r.file,...x})));const summary={checks:results.reduce((a,r)=>a+r.checks.length,0),failures:fail,errors};fs.writeFileSync('work/browser-qa/missal-rubrics.json',JSON.stringify({summary,results},null,2));console.log(JSON.stringify(summary));if(fail.length||errors.length)process.exitCode=1;})().catch(e=>{console.error(e);process.exitCode=1;});
