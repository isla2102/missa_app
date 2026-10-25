const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const html=fs.readFileSync('review/02-ia-v17.html','utf8'),js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const walk=n=>[n,...n.children.flatMap(walk)];
class E{
 constructor(t){this.tagName=t;this.children=[];this.attrs={};this._text='';this.className='';this.classList={contains:c=>this.className.split(' ').includes(c),add:c=>{if(!this.classList.contains(c))this.className+=' '+c}};}
 get textContent(){return this._text+this.children.map(n=>n.textContent).join('')}set textContent(t){this._text=t;this.children=[]}
 append(...n){n.forEach(x=>x.parentElement=this);this.children.push(...n)}replaceChildren(...n){this._text='';this.children=[];this.append(...n)}
 replaceWith(n){const p=this.parentElement;if(p){p.children.splice(p.children.indexOf(this),1,n);n.parentElement=p;}}
 insertBefore(n,b){n.parentElement=this;this.children.splice(this.children.indexOf(b),0,n)}setAttribute(k,v){this.attrs[k]=v}getAttribute(k){return this.attrs[k]}addEventListener(){}closest(){return null}focus(){}
 querySelectorAll(s){return walk(this).slice(1).filter(x=>s[0]==='.'?x.classList.contains(s.slice(1)):x.tagName===s)}querySelector(s){return this.querySelectorAll(s)[0]}
}
const date={value:'2026-10-18'};const ui=new Map();
const slot={value:'main',selectedOptions:[{textContent:'교중미사'}]},mode={value:'beginner'};
const sandbox={document:{createElement:t=>new E(t),createElementNS:(_,t)=>new E(t),querySelector:s=>{if(s.includes('mode'))return mode;if(s.includes('slot'))return slot;if(s.includes('date'))return date;const key=s.match(/data-js="(.*?)"/)?.[1];if(!ui.has(key)){const e=new E('div');e.showModal=()=>e.open=true;e.close=()=>e.open=false;ui.set(key,e);}return ui.get(key);}}};vm.createContext(sandbox);vm.runInContext(js.slice(0,js.indexOf("find('part-prev').onclick")),sandbox);const run=c=>vm.runInContext(c,sandbox);
const roles=n=>walk(n).filter(x=>x.attrs['data-speech-role']);
const sign=run("renderBlock(flowBlocks(0).find(b=>b.item?.title==='성호경'))");assert.equal(roles(sign).filter(x=>x.attrs['data-speech-role']==='assembly').length,1);assert.ok(roles(sign).find(x=>x.attrs['data-speech-role']==='assembly').textContent.includes('아멘.'));
const greetings=run("flowBlocks(0).filter(b=>b.group==='인사')");assert.equal(greetings.length,3);assert.ok(greetings.every(b=>!b.variant.text.includes('◎')));
const common=run("flowBlocks(0).filter(b=>b.group==='인사 합송')");assert.equal(common.length,1);assert.equal(common[0].variant.text,'◎ 또한 사제의 영과 함께.');
const conf=run("renderBlock(flowBlocks(0).find(b=>b.group==='참회 예식'))");const assembly=roles(conf).filter(x=>x.attrs['data-speech-role']==='assembly');assert.equal(assembly.length,2);assert.ok(assembly[0].textContent.includes('형제들에게'));assert.ok(assembly[0].textContent.includes('제 탓이요'));assert.ok(assembly[0].textContent.includes('빌어 주소서'));assert.ok(assembly[0].querySelector('.reader__guidance'));assert.ok(assembly[1].textContent.includes('아멘'));
assert.ok(roles(conf).find(x=>x.attrs['data-speech-role']==='priest').textContent.includes('형제 여러분'));
// Every marked response in each reference is assigned to an assembly segment, including continuation lines.
for(const record of run('localOrdinaryReference.records')){const segments=run('spokenSegments')(record.text);const markers=record.text.split('\n').filter(l=>l.trim().startsWith('◎'));for(const line of markers)assert.ok(segments.some(s=>s.kind==='assembly'&&s.parts.some(p=>p.text===line.trim())),record.key+line);}
for(let i=0;i<4;i++)for(const block of run(`flowBlocks(${i})`)){const node=run('renderBlock')(block);assert.ok(node);}
const creed=run('renderCreed()');assert.equal(walk(creed).filter(x=>x.attrs['data-variant']).length,2);assert.ok(roles(creed).some(x=>x.attrs['data-speech-role']==='assembly'));
const continuation=run("renderBlock({key:'test',tocId:'test',variant:{title:'참회',text:'◎ 형제들에게 고백하오니\\n제 탓이오'},fragmentText:'제 탓이오',fragmentRole:'assembly'})");assert.equal(roles(continuation)[0].attrs['data-speech-role'],'assembly');
run("kyrieView='invocations'");const kyrie=run("renderPrayerFrame('자비송','자비송')");assert.equal(roles(kyrie).filter(x=>x.attrs['data-speech-role']==='assembly').length,4);
assert.ok(html.includes('font-weight: var(--draft-response-weight)'));assert.ok(html.includes('color: var(--draft-guide-ink)'));assert.ok(!/style="|!important/.test(html));
console.log('PASS: separate highlighted assembly cards, three priest greeting choices + one common response, two confession response groups with embedded guidance, all reference ◎ markers, every part renders, creed internal cards, continuation role, invocation responses.');

mode.value='regular';const regular=run("renderBlock(flowBlocks(0).find(b=>b.group==='참회 예식'))");assert.equal(walk(regular).filter(x=>x.classList.contains('reader__guidance')).length,0);assert.ok(roles(regular).some(x=>x.textContent.includes('빌어 주소서')));mode.value='beginner';
console.log('PASS: regular mode hides guidance while preserving assembly text.');

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


const hanging=run("liturgyNode")('+ 사제의 긴 본문\n이어지는 줄\n◎ 신자의 응답\n[안내] 가슴을 치며 말한다.\n계속 바칩니다.');
const speechRows=walk(hanging).filter(n=>n.classList.contains('reader__speech-row'));assert.equal(speechRows.length,2);assert.equal(speechRows[0].children[0].textContent,'+');assert.equal(speechRows[1].children[0].textContent,'◎');assert.ok(speechRows.every(row=>row.children[1].classList.contains('reader__speech-body')));const guide=walk(hanging).find(n=>n.classList.contains('reader__guidance'));assert.equal(guide.parentElement.className,'reader__speech-body');assert.ok(guide.parentElement.textContent.includes('신자의 응답'));assert.ok(guide.parentElement.textContent.includes('계속 바칩니다.'));
const entrance=run('renderEntranceScore()');assert.ok(entrance.className.includes('reader__item--score'));assert.ok(entrance.textContent.includes('악보 표시 영역 · mock'));assert.equal(entrance.textContent.includes('자료에'),false);assert.equal(entrance.textContent.includes('오늘 미사의 입당송'),false);assert.ok(walk(entrance).some(n=>n.className==='reader__score-scroll'));assert.ok(walk(entrance).some(n=>n.tagName==='img'&&n.src==='../docs/mock/entrance-score.svg'));
run("kyrieView='ordinary'");const ready=run("scoreAssets('아멘')");assert.equal(ready.length,1);assert.equal(ready[0].kind,'engraved');const amen=run("renderPrayerFrame('아멘','아멘')");assert.ok(walk(amen).some(n=>n.attrs['data-score-kind']==='reengraved'));assert.ok(walk(amen).some(n=>n.tagName==='a'&&decodeURI(n.href).endsWith('reengraved/amen.pdf')));assert.equal(walk(amen).filter(n=>n.tagName==='image').length,0);assert.equal(run("scoreAssets('자비송')[0].kind"),undefined);slot.value='dawn';assert.equal(run("scoreAssets('아멘').length"),0);slot.value='main';
console.log('PASS: guidance nested inside speech body; full-page entrance mock; Amen uses vector edition/PDF link, other photos and parish scope retained.');

