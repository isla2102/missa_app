from pathlib import Path
s=Path('work/test-assembly-v13.cjs').read_text(encoding='utf-8').replace('02-ia-v13.html','02-ia-v15.html')
s=s.replace("const slot={", "const date={value:'2026-10-18'};const ui=new Map();\nconst slot={",1)
s=s.replace("querySelector:s=>s.includes('mode')?mode:slot", "querySelector:s=>{if(s.includes('mode'))return mode;if(s.includes('slot'))return slot;if(s.includes('date'))return date;const key=s.match(/data-js=\"(.*?)\"/)?.[1];if(!ui.has(key)){const e=new E('div');e.showModal=()=>e.open=true;e.close=()=>e.open=false;ui.set(key,e);}return ui.get(key);}")
s+='''
assert.equal(html.includes('◎ 합송 · 함께 바칩니다'),false);
const greetingNodes=run("flowBlocks(0).filter(b=>b.group==='인사'||b.group==='인사 합송').map(renderBlock)");
assert.equal(greetingNodes.flatMap(walk).filter(n=>n.tagName==='h3').length,1);
assert.equal(greetingNodes.flatMap(walk).filter(n=>n.classList.contains('reader__alternative-marker')).length,2);
assert.equal(greetingNodes.flatMap(walk).filter(n=>n.attrs['data-speech-role']==='assembly').length,1);
run('updateLiturgicalHeading()');assert.ok(ui.get('liturgical-day').textContent.includes('연중 제29주일'));assert.equal(ui.get('liturgical-season').textContent,'연중 시기');
const collect=run('renderCollect()');assert.ok(walk(collect).some(n=>n.attrs['data-content-source']==='cbck-daily-collect'&&n.textContent.includes('모든 사람이 진리를')));assert.equal(roles(collect).filter(n=>n.attrs['data-speech-role']==='assembly').length,1);
date.value='2026-11-01';run('updateLiturgicalHeading()');assert.equal(ui.get('liturgical-day').textContent,'전례일 미연동');const unknown=run('renderCollect()');assert.ok(unknown.textContent.includes('mock'));assert.equal(unknown.textContent.includes('모든 사람이 진리를'),false);date.value='2026-10-18';
assert.equal(run('hasSeenTutorial()'),false);run('showTutorial()');assert.equal(ui.get('tutorial').open,true);for(let i=0;i<4;i++)run('nextTutorial()');assert.equal(run('hasSeenTutorial()'),true);assert.equal(ui.get('tutorial').open,false);run('showTutorial()');assert.equal(ui.get('tutorial').open,true);
assert.ok(html.includes('z-index: var(--draft-choice-marker-z)'));
console.log('PASS: no repeated assembly labels, one greeting heading/three cards/two alternatives/common response, dated collect snapshot and stale-data guard, liturgical badge, first-run and replayable tutorial with storage fallback.');
'''
Path('work/test-reader-v15.cjs').write_text(s,encoding='utf-8',newline='\r\n')
