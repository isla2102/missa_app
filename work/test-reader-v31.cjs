const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const html=fs.readFileSync('review/02-ia-v31.html','utf8'),js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const walk=n=>[n,...n.children.flatMap(walk)];
class E{
 constructor(t){this.tagName=t;this.children=[];this.attrs={};this._text='';this.className='';this.classList={contains:c=>this.className.split(' ').includes(c),add:c=>{if(!this.classList.contains(c))this.className+=' '+c}};}
 get textContent(){return this._text+this.children.map(n=>n.textContent).join('')}set textContent(t){this._text=t;this.children=[]}
 append(...n){n.forEach(x=>{const old=x.parentElement;if(old){const i=old.children.indexOf(x);if(i>=0)old.children.splice(i,1);}x.parentElement=this;this.children.push(x);});}replaceChildren(...n){this._text='';this.children=[];this.append(...n)}
 replaceWith(n){const p=this.parentElement;if(p){p.children.splice(p.children.indexOf(this),1,n);n.parentElement=p;}}
 insertBefore(n,b){n.parentElement=this;this.children.splice(this.children.indexOf(b),0,n)}setAttribute(k,v){this.attrs[k]=v}getAttribute(k){return this.attrs[k]}addEventListener(){}closest(){return null}focus(){}
 querySelectorAll(s){return walk(this).slice(1).filter(x=>s[0]==='.'?x.classList.contains(s.slice(1)):x.tagName===s)}querySelector(s){return this.querySelectorAll(s)[0]}
}
const date={value:'2026-10-18'};const ui=new Map();
const slot={value:'main',selectedOptions:[{textContent:'교중미사'}]},mode={value:'beginner'};
const sandbox={document:{createElement:t=>new E(t),createElementNS:(_,t)=>new E(t),querySelector:s=>{if(s.includes('mode'))return mode;if(s.includes('slot'))return slot;if(s.includes('date'))return date;const key=s.match(/data-js="(.*?)"/)?.[1];if(!ui.has(key)){const e=new E('div');e.showModal=()=>e.open=true;e.close=()=>e.open=false;ui.set(key,e);}return ui.get(key);}}};vm.createContext(sandbox);vm.runInContext(js.slice(0,js.indexOf("find('part-prev').onclick")),sandbox);const run=c=>vm.runInContext(c,sandbox);
const roles=n=>walk(n).filter(x=>x.attrs['data-speech-role']);
const sign=run("renderBlock(flowBlocks(0).find(b=>b.item?.title==='성호경'))");assert.equal(roles(sign).filter(x=>x.attrs['data-speech-role']==='assembly').length,1);assert.ok(roles(sign).find(x=>x.attrs['data-speech-role']==='assembly').textContent.includes('아멘.'));
const greetings=run("flowBlocks(0).filter(b=>b.group==='인사')");assert.equal(greetings.length,3);assert.ok(greetings.slice(0,2).every(b=>!b.variant.text.includes('◎')));
const common=run("flowBlocks(0).filter(b=>b.group==='인사 합송')");assert.equal(common.length,0);assert.ok(greetings[2].variant.text.includes('◎ 또한 사제의 영과 함께.'));const greetingPair=run("renderBlock(flowBlocks(0).filter(b=>b.group==='인사')[2])");assert.ok(walk(greetingPair).some(n=>n.classList.contains('reader__dialogue')&&n.children.length===2));
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
date.value='2026-11-01';run('updateLiturgicalHeading()');assert.equal(ui.get('liturgical-day').textContent,'전례일 미연동');const unknown=run('renderCollect()');assert.ok(unknown.textContent.includes('연결 예정'));assert.equal(unknown.textContent.includes('모든 사람이 진리를'),false);date.value='2026-10-18';
assert.equal(run('hasSeenTutorial()'),false);run('showTutorial()');assert.equal(ui.get('tutorial').open,true);for(let i=0;i<4;i++)run('nextTutorial()');assert.equal(run('hasSeenTutorial()'),true);assert.equal(ui.get('tutorial').open,false);run('showTutorial()');assert.equal(ui.get('tutorial').open,true);
assert.ok(html.includes('z-index: var(--draft-choice-marker-z)'));
console.log('PASS: no repeated assembly labels, one greeting heading/three cards/two alternatives/common response, dated collect snapshot and stale-data guard, liturgical badge, first-run and replayable tutorial with storage fallback.');


const hanging=run("liturgyNode")('+ 사제의 긴 본문\n이어지는 줄\n◎ 신자의 응답\n[안내] 가슴을 치며 말한다.\n계속 바칩니다.');
const speechRows=walk(hanging).filter(n=>n.classList.contains('reader__speech-row'));assert.equal(speechRows.length,2);assert.equal(speechRows[0].children[0].textContent,'+');assert.equal(speechRows[1].children[0].textContent,'◎');assert.ok(speechRows.every(row=>row.children[1].classList.contains('reader__speech-body')));const guide=walk(hanging).find(n=>n.classList.contains('reader__guidance'));assert.equal(guide.parentElement.className,'reader__speech-body');assert.ok(guide.parentElement.textContent.includes('신자의 응답'));assert.ok(guide.parentElement.textContent.includes('계속 바칩니다.'));

for(const title of ['입당 성가','봉헌 성가','영성체 성가','파견 성가']){const n=run('renderHymnScore')(title);assert.equal(n.textContent.includes('mock'),false);const input=walk(n).find(x=>x.tagName==='input');input.value='365';walk(n).find(x=>x.tagName==='form').onsubmit({preventDefault(){}});assert.ok(walk(n).some(x=>x.tagName==='img'&&x.src.includes('2012040365.jpg')));const b=walk(n).find(x=>x.tagName==='button'&&x.textContent==='악보 크게 보기');assert.ok(b);assert.equal(b.className,'reader__score-enlarge');b.onclick();assert.ok(walk(ui.get('score-modal-body')).some(x=>x.tagName==='img'));input.value='529';walk(n).find(x=>x.tagName==='form').onsubmit({preventDefault(){}});assert.ok(n.textContent.includes('1부터 528'));}
run("kyrieView='ordinary'");const amen=run("renderPrayerFrame('아멘','아멘')");const enlarge=walk(amen).find(n=>n.tagName==='button'&&n.textContent==='악보 크게 보기');assert.ok(enlarge);enlarge.onclick();assert.ok(walk(ui.get('score-modal-body')).some(n=>n.tagName==='object'&&n.type==='application/pdf'&&decodeURI(n.data).includes('amen.pdf')));assert.ok(!walk(amen).some(n=>n.tagName==='a'&&n.textContent==='PDF 열기'));
for(const i of [0,1,2,3])for(const b of run(`flowBlocks(${i})`))assert.ok(run('renderBlock')(b));
const flow=run('flowBlocks(2)');assert.ok(flow.findIndex(b=>b.item?.title==='봉헌 성가')<flow.findIndex(b=>b.item?.title==='예물 준비 기도'));assert.equal(flow.filter(b=>b.item?.title==='예물 준비 기도').length,1);assert.ok(flow.some(b=>b.item?.title==='영성체 성가'));
for(const title of ['예물 기도','영성체 후 기도']){const n=run('renderItem')(run('contents.flat()').find(x=>x.title===title));assert.ok(walk(n).some(x=>x.attrs['data-content-source']==='cbck-daily-mock'));assert.ok(n.textContent.includes('mock'));assert.equal(n.textContent.includes('본문 없음'),false);}
const notice=run("renderItem(contents.flat().find(x=>x.title==='공지 사항'))");assert.ok(walk(notice).some(n=>n.attrs['data-content-source']==='parish-bulletin-mock'));assert.ok(notice.textContent.includes('신부님'));
const ep=run("ordinaryText('감사기도 제2양식')");for(const unwanted of ['미확정','[감사송 대화]','[인쇄본 수록 감사송'])assert.equal(ep.includes(unwanted),false);assert.ok(ep.includes('거룩하신 아버지'));assert.ok(flow.some(b=>b.item?.title==='감사기도 제2양식'));
const dismissal=run("flowBlocks(3).filter(b=>b.group==='파견')");assert.equal(dismissal.length,4);assert.ok(dismissal.every(b=>!b.variant.text.includes('◎')));assert.equal(run("flowBlocks(3).filter(b=>b.group==='파견 합송').length"),1);
const expected=[['2026-02-18','lent','이 빵을 먹고'],['2026-04-05','easter','십자가와 부활로'],['2026-05-24','easter','십자가와 부활로'],['2026-05-25','ordinary','부활을 선포'],['2026-10-18','ordinary','부활을 선포']];const crops=[];
for(const [d,key,phrase] of expected){date.value=d;assert.equal(run('currentSeason().key'),key);assert.ok(run("ordinaryText('신앙의 신비여')").includes(phrase));const assets=run("scoreAssets('신앙의 신비여')");assert.equal(assets.length,1);crops.push(assets[0].preview);}assert.equal(new Set(crops).size,3);
date.value='2026-04-03';assert.equal(run('currentSeason()'),null);assert.equal(run("scoreAssets('신앙의 신비여').length"),0);date.value='2026-10-18';run('showSeasonModal()');assert.equal(ui.get('season-modal').open,true);assert.ok(ui.get('season-modal-body').textContent.includes('5월 25일 ~ 11월 28일'));assert.equal(walk(ui.get('season-modal-body')).filter(n=>n.attrs['aria-current']==='true').length,1);date.value='2027-10-18';run('showSeasonModal()');assert.ok(ui.get('season-modal-body').textContent.includes('연결 전'));date.value='2026-10-18';
assert.ok(html.includes('<option value="youth">저녁미사</option>'));assert.ok(html.includes('.reader__session-select { width: max-content; }'));
assert.equal(/style="|!important/.test(html),false);
console.log('PASS: all score kinds enlarge in modal/PDF object, four hymn mocks, separate preparation, daily prayer mocks/bulletin notice, EP II label cleanup, seasonal response+3 crops/boundaries, four dismissal choices+one response, season period modal, short evening label/intrinsic select width.');

const acclamation=run('renderAlleluia()');const cards=walk(acclamation).filter(n=>n.attrs['data-acclamation-role']);assert.deepEqual(cards.map(n=>n.attrs['data-acclamation-role']),['assembly','choir','assembly']);assert.equal(cards[0].querySelector('img').src,cards[2].querySelector('img').src);assert.ok(cards[1].textContent.includes('너희는 가서 모든 민족들을'));
const aflow=run("flowBlocks(1).filter(b=>b.acclamationPart)");assert.equal(aflow.length,3);assert.deepEqual(Array.from(aflow,b=>b.acclamationPart),['first','choir','last']);for(const b of aflow)assert.ok(run('renderBlock')(b));
const a365=run("reengravedPrincipalScores['복음 환호송'][0]");run('showSourceDialog')(run("scoreSourceCatalog['복음 환호송']"));assert.ok(ui.get('source-dialog-body').textContent.includes('365번'));assert.ok(walk(ui.get('source-dialog-body')).some(n=>n.tagName==='a'&&n.href?.includes('sunggaId=365')));assert.ok(walk(ui.get('source-dialog-body')).some(n=>n.tagName==='a'&&n.download?.includes('365')));
assert.equal(run("scoreSourceCatalog['자비송'].confirmedNumber"),null);run('showSourceDialog')(run("scoreSourceCatalog['자비송']"));assert.ok(ui.get('source-dialog-body').textContent.includes('선율이 같은 번호는 아직 확인되지'));
assert.equal(run("scoreAssets('자비송')[0].kind"),'engraved');assert.equal(run("scoreAssets('주님의 기도 맺음 환호')[0].kind"),'engraved');slot.value='dawn';assert.equal(run("scoreAssets('복음 환호송')[0].kind"),'engraved');assert.equal(run("scoreAssets('자비송').length"),0);slot.value='main';
console.log('PASS: 365 refrain/choir/refrain ordered cards and identical one-line score, dated choir verse, confirmed-number source dialog/ENC link, unresolved candidates honestly labelled, additional finished PDFs and common-scope 365.');

date.value='2026-10-18';run('showSeasonModal()');const helpButtons=walk(ui.get('season-modal-body')).filter(n=>n.className==='reader__season-help');assert.equal(helpButtons.length,4);for(const b of helpButtons){assert.equal(b.attrs['aria-haspopup'],'dialog');b.onclick();assert.equal(ui.get('season-help-modal').open,true);assert.ok(ui.get('season-help-title').textContent.endsWith('란?'));assert.ok(ui.get('season-help-text').textContent.length>60);assert.equal(ui.get('season-modal').open,true);}console.log('PASS: four period help buttons, three meanings, nested dialog keeps calendar open.');

const universal=run("flowBlocks(1).filter(b=>b.group?.startsWith('보편 지향 기도'))");assert.equal(universal.filter(b=>b.group==='보편 지향 기도 합송').length,4);assert.equal(universal.at(-1).variant.text,'◎ 아멘.');assert.ok(universal.at(-2).variant.text.includes('mock'));assert.ok(run("ordinaryText('감사기도 제2양식')").includes('(타대오와 협력 주교들)'));const compact=run("renderPrayerFrame('주님의 기도 맺음 환호','주님의 기도 맺음 환호')");assert.ok(!compact.className.includes('item--score'));assert.ok(walk(compact).some(n=>n.attrs['data-score-layout']==='compact'));assert.equal(run("scoreAssets('하느님의 어린양')[0].kind"),'engraved');date.value='2026-10-19';assert.equal(run("universalPrayerBlocks(contents[1].at(-1)).filter(b=>b.group==='보편 지향 기도 합송').length"),1);date.value='2026-10-18';console.log('PASS: intercessions response per petition/conclusion/Amen, dated fallback, bishop override, compact doxology, Agnus crop.');

assert.equal(run('renderCollect()').textContent.includes('확인 자료'),false);assert.equal(run('renderCollect()').textContent.includes('두 수록 본문'),false);assert.equal(run("variantCards('참회 예식')[1].text").includes('호칭과 응답은 다음'),false);const homily=run("renderItem(contents[1].find(x=>x.title==='강론'))");assert.ok(homily.textContent.includes('강론을 듣습니다'));assert.ok(walk(homily).some(n=>n.className==='reader__content-card'));console.log('PASS: hymn number form, validation, remote score/modal, help removals, homily card, session response policy and engraved Agnus.');

const hymn=run("renderHymnScore('입당 성가')");assert.equal(hymn.children.length,2);assert.ok(walk(hymn.children[0]).some(n=>n.tagName==='form'));const entry=walk(hymn).find(n=>n.tagName==='input');entry.value='123';walk(hymn).find(n=>n.tagName==='form').onsubmit({preventDefault(){}});const figure=walk(hymn).find(n=>n.tagName==='figure');assert.equal(figure.querySelector('figcaption').textContent,'악보 크게 보기');assert.ok(!hymn.textContent.includes('가톨릭성가 123번'));assert.equal(figure.querySelector('img').onload,undefined);assert.ok(figure.querySelector('img').src.endsWith('2012040123.jpg'));console.log('PASS: exactly two explicit grid rows; form stays in header; no duplicate captions; remote image load cannot trigger reflow/reset scroll.');

const pen=run('renderPenitential()');const options=walk(pen).filter(n=>n.tagName==='button');assert.deepEqual(options.map(n=>n.textContent),['전능하신 하느님과','진심으로 뉘우치는']);options[1].onclick();assert.ok(pen.textContent.includes('진심으로 뉘우치는'));assert.ok(!pen.textContent.includes('형제들에게 고백하오니'));assert.equal(walk(pen).filter(n=>n.tagName==='button'&&n.attrs['aria-pressed']==='true').length,1);options[0].onclick();assert.ok(pen.textContent.includes('형제들에게 고백하오니'));assert.equal(run("flowBlocks(0).filter(b=>b.penitential).length"),1);const response=run('renderIntercessionResponse()');assert.equal(response.children.length,1);assert.equal(walk(response).filter(n=>n.tagName==='button').length,0);assert.ok(response.textContent.includes('주님, 저희의 기도를 들어주소서.'));assert.equal(run("scoreAssets('주님의 기도').length"),1);assert.ok(run("scoreAssets('주님의 기도').every(a=>a.kind==='engraved')"));console.log('PASS: one penitential card/two opening-phrase buttons/selected text, grouped recite-score response card, two engraved Lord prayer pages.');

const gospel=run("renderBlock(flowBlocks(1).find(b=>b.item?.title==='복음'))");assert.ok(gospel.textContent.includes('작은 십자 표시'));const pair=walk(gospel).find(n=>n.classList.contains('reader__dialogue'));assert.ok(pair);assert.equal(pair.children.length,2);assert.ok(pair.children[1].textContent.includes('또한 사제의 영과 함께'));
date.value='2026-03-01';run('renderCreed()');assert.equal(run('creedView'),'apostles');run("creedView='nicene'");run('renderCreed()');assert.equal(run('creedView'),'nicene');date.value='2026-05-03';run('renderCreed()');assert.equal(run('creedView'),'apostles');date.value='2026-10-18';run('renderCreed()');assert.equal(run('creedView'),'nicene');
run('scheduleReflow=()=>{}');const petition=run("renderBlock(flowBlocks(1).find(b=>b.group==='보편 지향 기도 지향'))");const toggle=walk(petition).filter(n=>n.tagName==='button');assert.equal(toggle.length,2);toggle.find(n=>n.textContent==='악보').onclick();for(let i=0;i<4;i++){const response=run('renderIntercessionResponse()');assert.equal(walk(response).filter(n=>n.tagName==='button').length,0);assert.ok(response.textContent.includes('악보 준비 중'));}run("intercessionView='recite'");
assert.ok(!html.includes('data-js="part-current"'));assert.ok(!html.includes('<footer'));assert.ok(html.indexOf('aria-label="미사 순서 이동"')<html.indexOf('data-js="book"'));assert.ok(html.includes('grid-column: 2; grid-row: 2;'));assert.ok(html.includes('reader__tools'));
for(const name of ['아멘','주님의 기도 맺음 환호','신앙의 신비여']){const card=run('renderPrayerFrame')(name,name);assert.ok(!card.className.includes('item--score'));}for(const name of ['대영광송','주님의 기도']){assert.equal(run('scoreAssets')(name).length,1);const card=run('renderPrayerFrame')(name,name);assert.equal(walk(card).filter(n=>n.tagName==='figure').length,1);assert.equal(walk(card).filter(n=>n.tagName==='img').length,1);}
assert.equal(run("scoreAssets('거룩하시도다')[0].kind"),'engraved');console.log('PASS: paired gospel, small-cross copy, season-default creed/manual override, one controller for all responses, header nav/tools and aligned rail, short score heights, single continuous Gloria/Lord score assets.');

// v26 comment-specific regressions
for(const title of ['제1독서','제2독서','복음']){
 const n=run(`renderBlock(flowBlocks(1).find(b=>b.item?.title==='${title}'))`);
 const pairs=walk(n).filter(x=>x.classList.contains('reader__dialogue'));
 assert.ok(pairs.some(x=>x.textContent.includes('주님의 말씀입니다.')&&x.children.length===2),title);
 assert.ok(!n.textContent.includes('[독서자]'));
}
run("intercessionView='chant'");const chantResponse=run('renderIntercessionResponse()');assert.equal(roles(chantResponse).length,0);assert.equal(chantResponse.textContent,'악보 준비 중');
run("intercessionView='recite'");assert.equal(roles(run('renderIntercessionResponse()')).length,1);
const sanctus=run("parishPrayerPresentation['거룩하시도다']='chant';renderPrayerFrame('거룩하시도다','거룩하시도다')");assert.ok(sanctus.className.includes('compact-score'));
assert.ok(html.includes('.reader__tools { grid-column: 2; grid-row: 3;'));
assert.ok(html.includes('reader__part-prev'));assert.ok(html.includes('grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr)'));
assert.ok(html.includes("visibleIds.has(entry.id)"));
console.log('PASS v26: closing response pairs, no lector prefix, chant hides recitation, natural Sanctus height, centered heading/navigation, tools below rail and visible spread TOC frame.');

run("part=0;spread=0;layouts=[{blocks:[{tocId:contents[0][3].id}]},{blocks:[{tocId:contents[0][4].id}]}];const railTest=document.createElement('aside');railTest.scrollTop=0;railTest.append(find('toc-rail'));renderToc();");
const tocNodes=walk(ui.get('toc-rail'));assert.equal(tocNodes.filter(n=>n.className.split(' ').includes('reader__toc-visible')).length,2);assert.equal(tocNodes.filter(n=>n.className.includes('visible--first')).length,1);assert.equal(tocNodes.filter(n=>n.className.includes('visible--last')).length,1);
console.log('PASS: TOC frames both current pages as one contiguous range.');
for(let i=0;i<4;i++)assert.ok(run(`flowBlocks(${i}).every(b=>b.transition===undefined)`));
assert.deepEqual(JSON.parse(JSON.stringify(run('pageTurnState(0,0,5)'))),{previous:false,next:true,previousPart:false,nextPart:false});
assert.ok(run('pageTurnState(0,2,5).nextPart'));assert.ok(run('pageTurnState(1,0,4).previousPart'));assert.equal(run('pageTurnState(3,1,4).next'),false);
const ep27=run("renderBlock(flowBlocks(2).find(b=>b.item?.title==='감사기도 제2양식'))");const epPairs=walk(ep27).filter(n=>n.classList.contains('reader__dialogue'));assert.equal(epPairs.length,3);assert.ok(epPairs.every(n=>n.children.length===2));
const oldRender=run('render');sandbox.renderedOptions=null;run('render=options=>{renderedOptions=options};part=0;spread=1;layouts=[{blocks:[{key:"start"}]},{blocks:[{key:"middle"}]},{blocks:[{key:"end"}]}];turnSpread(1)');assert.equal(run('part'),1);assert.equal(sandbox.renderedOptions.anchorKey,run('contents[1][0].id'));
run('spread=0;layouts=[{blocks:[{key:"first"}]}];turnSpread(-1)');assert.equal(run('part'),0);assert.equal(sandbox.renderedOptions.edge,'last');
run('part=0;spread=0;layouts=[{blocks:[{key:"first"}]}]');sandbox.renderedOptions=null;run('turnSpread(-1)');assert.equal(sandbox.renderedOptions,null);
for(const [x,y,expected] of [[-100,10,1],[100,8,-1],[20,0,0],[100,150,0],[70,60,0]])assert.equal(run(`swipeDirection(${x},${y})`),expected);
const events={};const swipeBook={addEventListener:(name,fn)=>events[name]=fn};sandbox.swipeBook=swipeBook;run('bindPageSwipe(swipeBook)');sandbox.swiped=0;run('turnSpread=d=>swiped=d');const pointer=(x,y,interactive=false)=>({isPrimary:true,button:0,pointerId:1,clientX:x,clientY:y,target:{closest:()=>interactive},cancelable:true,preventDefault(){}});
events.pointerdown(pointer(200,100));events.pointerup(pointer(100,110));assert.equal(sandbox.swiped,1);
sandbox.swiped=0;events.pointerdown(pointer(200,100));events.pointermove(pointer(205,180));events.pointerup(pointer(100,200));assert.equal(sandbox.swiped,0);
events.pointerdown(pointer(200,100,true));events.pointerup(pointer(100,100));assert.equal(sandbox.swiped,0);
events.pointerdown(pointer(200,100));events.pointercancel();events.pointerup(pointer(100,100));assert.equal(sandbox.swiped,0);
console.log('PASS v27: no transition-only pages, boundary navigation in both directions, 3 short EP dialogue pairs, horizontal swipe, vertical/control/cancel guards.');

// Image geometry is identical before loading, after loading, and after revisiting.
for(const title of run('Object.keys(reengravedPrincipalScores)')){
 const assets=run(`reengravedPrincipalScores[${JSON.stringify(title)}]`);
 for(let i=0;i<assets.length;i++){
  const node=run(`renderPhoto(reengravedPrincipalScores[${JSON.stringify(title)}][${i}])`);const img=walk(node).find(n=>n.tagName==='img');assert.ok(Number(img.attrs.width)>0&&Number(img.attrs.height)>0,title);
 }
}
const firstPreview=run("renderPhoto(reengravedPrincipalScores['복음 환호송'][0])"),repeatPreview=run("renderPhoto(reengravedPrincipalScores['복음 환호송'][0])");
assert.deepEqual(walk(firstPreview).find(n=>n.tagName==='img').attrs,walk(repeatPreview).find(n=>n.tagName==='img').attrs);
run('part=1;spread=0;layouts=[{blocks:[{key:"a",tocId:contents[1][0].id}]},{blocks:[{key:"b",tocId:contents[1][2].id}]},{blocks:[{key:"c",tocId:contents[1][4].id,item:contents[1][4]}]}]');assert.equal(run('turnDestination(1)'),'복음');assert.ok(run('turnDestination(-1)').includes('본기도'));
run('spread=1');assert.ok(run('turnDestination(1)').includes('성찬 전례'));assert.equal(run('turnDestination(-1)'),'제1독서');assert.equal(run("flowBlockTitle({tocId:contents[1][3].id,acclamationPart:'last'})"),'복음 환호송 · 합송');
console.log('PASS v28: every engraved preview reserves dimensions; first/repeat geometry matches; previous/next destination labels and response titles.');
run("intercessionView='recite'");const response29=run('renderIntercessionResponse()');const shell29=response29.children[0];assert.ok(shell29.className.includes('reader__content-card--liturgy'));assert.equal(roles(response29).length,1);
const plan29=run('readingPagePlan(flowBlocks(1))');assert.equal(plan29.leading.length,2);assert.deepEqual(Array.from(plan29.leading[0].blocks,b=>b.item.title),['제1독서','화답송']);assert.deepEqual(Array.from(plan29.leading[1].blocks,b=>b.item.title),['제2독서']);assert.equal(plan29.rest[0].acclamationPart,'first');assert.ok(plan29.leading.every(p=>p.reading));
for(const title of ['제1독서','제2독서']){const reading=run(`renderBlock(flowBlocks(1).find(b=>b.item?.title==='${title}'))`);assert.ok(reading.className.includes('reader__item--reading'));assert.equal(walk(reading).filter(n=>n.className.includes('reader__reading-body')).length,1);assert.ok(walk(reading).some(n=>n.classList.contains('reader__dialogue')&&n.textContent.includes('주님의 말씀입니다.')));}
assert.equal(run('readingPagePlan(flowBlocks(0)).leading.length'),0);assert.ok(html.includes('...plan.leading,...paginateSections(plan.rest,fits,split,plan.leading.length)'));
console.log('PASS v29: single response border; first reading+psalm left, second reading+response right; acclamation starts following spread; body stretches and closing dialogue preserved.');
for(const title of ['제1독서','제2독서','복음']){const block30=run(`renderBlock(flowBlocks(1).find(b=>b.item?.title==='${title}'))`);const pairs30=walk(block30).filter(n=>n.classList.contains('reader__dialogue'));assert.equal(pairs30.length,title==='복음'?2:1);assert.ok(pairs30.every(n=>n.classList.contains('reader__dialogue--stacked')));}
const components30=html.slice(html.indexOf('@layer components {'),html.indexOf('</style>'));assert.ok(components30.indexOf('.reader__reading-liturgy {')>components30.indexOf('.reader__liturgy {'));assert.ok(components30.includes('.reader__dialogue--stacked { grid-template-columns: minmax(0, 1fr); }'));
assert.ok(html.includes('.reader__reading-body { flex: 1; min-block-size: 0; overflow: auto; }'));
console.log('PASS v30: readings and both Gospel dialogues stack vertically; reading flex layout takes precedence over base grid, body alone fills remaining height.');
const sectionPlan31=run(`paginateSections([{key:'a',tocId:'a',size:1},{key:'b1',tocId:'b',size:1},{key:'b2',tocId:'b',size:1},{key:'c',tocId:'c',size:1}],blocks=>blocks.reduce((n,b)=>n+b.size,0)<=1,b=>[b])`);
assert.equal(sectionPlan31.length,5);assert.equal(sectionPlan31[1].blank,true);assert.equal(sectionPlan31[2].blocks[0].key,'b1');assert.equal(sectionPlan31[3].blocks[0].key,'b2');assert.equal(sectionPlan31[4].blocks[0].key,'c');
const onePage31=run(`paginateSections([{key:'a1',tocId:'a',size:1},{key:'a2',tocId:'a',size:1},{key:'b',tocId:'b',size:1}],blocks=>blocks.reduce((n,b)=>n+b.size,0)<=2,b=>[b])`);assert.equal(onePage31.length,2);assert.equal(onePage31[0].blocks.length,2);assert.equal(onePage31[1].blocks[0].key,'b');
const long31=run(`paginateSections([1,2,3,4].map(n=>({key:'a'+n,tocId:'a'})),blocks=>blocks.length<=1,b=>[b])`);assert.equal(long31.length,2);assert.equal(long31[1].oversize,true);assert.deepEqual(Array.from(long31.flatMap(p=>p.blocks),b=>b.key),['a1','a2','a3','a4']);
const offset31=run(`paginateSections([{key:'b1',tocId:'b'},{key:'b2',tocId:'b'}],blocks=>blocks.length<=1,b=>[b],1)`);assert.equal(offset31[0].blank,true);
const prayerKeys31=run("flowBlocks(1).filter(b=>b.tocId===contents[1][7].id).map(sectionFlowKey)");assert.equal(new Set(prayerKeys31).size,1);
console.log('PASS v31: one-page priority, new section starts new page, two-page sections aligned left, offset alignment, long content preserved in <=2 pages, universal prayer grouped through Amen.');
