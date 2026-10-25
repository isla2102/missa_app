const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {build,validateConfig}=require('./build-prototype.cjs');
const {chromium}=require('C:/Users/imsup/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
const config=JSON.parse(fs.readFileSync('prototype/source/build.json','utf8'));
const duplicated=structuredClone(config);duplicated.bindings.dailyDocuments.paths.push(duplicated.bindings.dailyDocuments.paths[0]);assert.throws(()=>build(duplicated),/Duplicate daily date/);
const escaped=structuredClone(config);escaped.bindings.dailyDocuments.paths=['../outside.json'];assert.throws(()=>validateConfig(escaped),/outside project/);
const b=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
try{const p=await b.newPage({viewport:{width:1024,height:768}});const errors=[];p.on('pageerror',e=>errors.push(e.message));await p.goto(pathToFileURL(path.resolve('prototype/index.html')).href);await p.waitForTimeout(300);
const checks=await p.evaluate(()=>{const out=[];const ok=(v,label)=>out.push({pass:Boolean(v),label});find('date').value='2026-10-24';find('date').dispatchEvent(new Event('change'));
ok(dailyDocuments.length===31,'31 October documents');ok(selectedMassDocument().observance==='연중 제29주간 토요일','date document');ok(find('liturgical-day').textContent==='연중 제29주간 토요일','heading follows date');ok(find('content-readiness').textContent.includes('일부 연결'),'partial readiness');
for(const title of ['본기도','예물 기도','영성체 후 기도']){const n=title==='본기도'?renderCollect():renderDailySection(title);ok(n.textContent.includes(dailySection(title).paragraphs[0].text.split('\n')[1]),title+' selected text');ok(n.textContent.split('아멘.').length===2,title+' one Amen');ok(n.querySelector('[data-daily-source]')?.getAttribute('href').includes('고유기도문.hwp'),title+' local HWP source');}
ok(readingFrameText('복음').includes('미연결'),'no borrowed Gospel');ok(selectedCollectVariants().length===1,'one weekday collect');for(const title of ['입당송','영성체송'])ok(Boolean(dailyText(title)),title+' linked');
find('date').value='2026-10-18';find('date').dispatchEvent(new Event('change'));ok(selectedCollectVariants().length===2,'prior date alternatives retained');ok(!readingFrameText('복음').includes('미연결'),'prior Gospel retained');find('date').value='2026-10-24';find('date').dispatchEvent(new Event('change'));return out;});
await p.reload();await p.waitForTimeout(300);checks.push({label:'date restored on reload',pass:await p.locator('[data-js="date"]').inputValue()==='2026-10-24'});await p.screenshot({path:'work/browser-qa/date-link-20261024.png',fullPage:true});assert.equal(errors.length,0);fs.writeFileSync('work/browser-qa/date-link.json',JSON.stringify({checks,errors,buildChecks:2},null,2));console.log(JSON.stringify({checks:checks.length+2,failed:checks.filter(c=>!c.pass),errors}));assert(checks.every(c=>c.pass));}finally{await b.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
