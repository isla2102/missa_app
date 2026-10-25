function createReaderButton(label='',variant='default'){const button=document.createElement('button');button.type='button';button.classList.add('missa-button');if(variant==='primary')button.classList.add('missa-button--primary');button.textContent=label;return button;}
// Prototype persistence is namespaced; legacy reader keys are read once, never overwritten.
const localStorage=(()=>{const native=window.localStorage,key='missa.prototype.v1.snapshot';let data={};try{const raw=native.getItem(key);if(raw){const parsed=JSON.parse(raw);if(parsed&&typeof parsed==='object'&&!Array.isArray(parsed))data=parsed;}else{for(let i=0;i<native.length;i++){const k=native.key(i);if(k?.startsWith('missa.')&&!k.startsWith('missa.prototype.'))data[k]=native.getItem(k);}}}catch{}const save=()=>native.setItem(key,JSON.stringify(data));return {get length(){return Object.keys(data).length;},key:i=>Object.keys(data)[i]??null,getItem:k=>Object.hasOwn(data,k)?String(data[k]):null,setItem(k,v){const previous=data[k],had=Object.hasOwn(data,k);data[k]=String(v);try{save();}catch(e){if(had)data[k]=previous;else delete data[k];throw e;}},removeItem(k){const previous=data[k],had=Object.hasOwn(data,k);delete data[k];try{save();}catch(e){if(had)data[k]=previous;throw e;}},clear(){const previous=data;data={};try{save();}catch(e){data=previous;throw e;}}};})();
function applyComponentStyles(root){root.querySelectorAll('button').forEach(b=>{b.classList.add('missa-button');if(b.hasAttribute('aria-pressed')&&!b.hasAttribute('aria-label'))b.setAttribute('aria-label',b.textContent);});root.querySelectorAll('input, select').forEach(n=>n.classList.add('missa-input'));}
const majorPrayerCatalog = {{majorPrayerCatalog}};
const bulletinProvider = {{bulletinProvider}};
const hymnScheduleCatalog = {{hymnScheduleCatalog}};
const parishConfig = {{parishConfig}};
function selectedParishName(){try{return localStorage.getItem('missa.parish.name.v1')?.trim()||parishConfig.name;}catch{return parishConfig.name;}}
let parishSessionDate=null;
function automaticParishSession(sessions,date,now=new Date()){
 const today=[now.getFullYear(),String(now.getMonth()+1).padStart(2,'0'),String(now.getDate()).padStart(2,'0')].join('-');
 const fallback=sessions.find(session=>session.id===parishConfig.defaultSession)||sessions[0];
 if(date!==today||parishConfig.automaticSelection!=='nearest-start')return fallback?.id;
 const minutes=now.getHours()*60+now.getMinutes();
 return sessions.filter(session=>/^\d{2}:\d{2}$/.test(session.time||'')).map(session=>({id:session.id,start:Number(session.time.slice(0,2))*60+Number(session.time.slice(3))})).sort((a,b)=>Math.abs(a.start-minutes)-Math.abs(b.start-minutes)||b.start-a.start)[0]?.id||fallback?.id;
}
function updateParishSessions(){
 const select=find('slot'),previous=select.value,date=find('date').value;
 const weekday=new Date(date+'T12:00:00').getDay();
 const sessions=parishConfig.sessions.filter(session=>session.weekdays===null||session.weekdays.includes(weekday));
 select.replaceChildren();
 sessions.forEach(session=>{const option=document.createElement('option');option.value=session.id;option.textContent=session.label;select.append(option);});
 if(parishSessionDate!==date)select.value=automaticParishSession(sessions,date)||parishConfig.defaultSession;else if(sessions.some(session=>session.id===previous))select.value=previous;else select.value=automaticParishSession(sessions,date)||parishConfig.defaultSession;
 parishSessionDate=date;
 if(!sessions.length){const option=document.createElement('option');option.value=parishConfig.defaultSession;option.textContent='선택 날짜 미사 일정 없음';select.append(option);}
 select.disabled=!sessions.length;find('parish-name').textContent=selectedParishName();
}


'use strict';
const find = name => document.querySelector(`[data-js="${name}"]`);
const parts = [
 {title:'시작 예식', pages:[['입당 · 성호경과 인사','공식 본문을 연결할 첫 번째 쪽입니다.'],['참회 예식 · 자비송 · 대영광송 · 본기도','같은 시작 예식의 이어지는 두 번째 쪽입니다.']]},
 {title:'말씀 전례', pages:[['독서 · 화답송','말씀 전례의 첫 번째 쪽입니다.'],['복음 환호송 · 복음','말씀 전례의 두 번째 쪽입니다.'],['강론 · 신앙 고백','말씀 전례의 세 번째 쪽입니다.'],['보편 지향 기도','말씀 전례의 네 번째 쪽입니다.']]},
 {title:'성찬 전례', pages:[['예물 준비 · 예물 기도','성찬 전례의 첫 번째 쪽입니다.'],['감사 기도','성찬 전례의 두 번째 쪽입니다.'],['주님의 기도 · 평화 예식','성찬 전례의 세 번째 쪽입니다.'],['영성체 · 영성체 후 기도','성찬 전례의 네 번째 쪽입니다.']]},
 {title:'마침 예식', pages:[['공지 · 강복','마침 예식의 첫 번째 쪽입니다.'],['파견 · 파견 성가','마침 예식의 이어지는 두 번째 쪽입니다.']]}
];

const contents = [
 [['입당 성가',0],['성호경',0],['인사',0],['참회 예식',1],['자비송',1],['대영광송',1],['본기도',1]],
 [['제1독서',0],['화답송',0],['제2독서',0],['복음 환호송',1],['복음',1],['강론',2],['신앙 고백',2],['보편 지향 기도',3]],
 [['봉헌 성가',0],['예물 기도',0],['감사기도 제2양식',1],['주님의 기도',2],['평화 예식',2],['영성체 예식 · 영성체 성가',3],['영성체 후 기도',3]],
 [['공지 사항',0],['강복',0],['파견',1],['파견 성가',1]]
].map((items, partIndex) => items.map(([title, page], index) => ({id:`part-${partIndex}-item-${index}`, title, page})));
const frameSpecs = {"입당 성가": {"kind": "hymn", "source": "hymnSet", "role": "entrance"}, "성호경": {"kind": "prayer", "source": "ordinary", "prayerId": "성호경", "scoreSlot": false}, "인사": {"kind": "choice", "source": "celebrant", "guide": "사제가 선택한 인사 양식에 따라 참여합니다."}, "참회 예식": {"kind": "choice", "source": "celebrant", "guide": "사제가 선택한 참회 예식 양식에 따라 참여합니다."}, "자비송": {"kind": "prayer", "source": "ordinary", "condition": "선택한 예식에 따라 적용", "prayerId": "자비송", "scoreSlot": true}, "대영광송": {"kind": "prayer", "source": "ordinary", "condition": "전례일에 따라 포함 여부 결정", "prayerId": "대영광송", "scoreSlot": true}, "본기도": {"kind": "proper", "source": "liturgicalDay"}, "제1독서": {"kind": "proper", "source": "liturgicalDay"}, "화답송": {"kind": "proper", "source": "liturgicalDay"}, "제2독서": {"kind": "proper", "source": "liturgicalDay", "condition": "전례일에 따라 적용"}, "복음 환호송": {"kind": "proper", "source": "liturgicalDay"}, "복음": {"kind": "proper", "source": "liturgicalDay"}, "강론": {"kind": "choice", "source": "celebrant", "guide": "사제 또는 부제의 강론을 듣습니다."}, "신앙 고백": {"kind": "prayer", "source": "celebrant", "guide": "적용되는 전례일에 선택된 신앙 고백 양식으로 참여합니다.", "prayerId": "신앙 고백", "scoreSlot": true}, "보편 지향 기도": {"kind": "choice", "source": "parish", "guide": "본당에서 준비한 기도 지향에 따라 함께 기도합니다."}, "예물 준비 · 봉헌 성가": {"kind": "hymn", "source": "hymnSet", "role": "offertory"}, "예물 기도": {"kind": "proper", "source": "liturgicalDay"}, "감사 기도": {"kind": "choice", "source": "celebrant", "guide": "사제가 선택한 감사 기도 양식에 따라 참여합니다."}, "주님의 기도": {"kind": "prayer", "source": "ordinary", "prayerId": "주님의 기도", "scoreSlot": true}, "평화 예식": {"kind": "choice", "source": "celebrant", "guide": "사제의 안내에 따라 평화 예식에 참여합니다."}, "영성체 예식 · 영성체 성가": {"kind": "proper", "source": "liturgicalDay", "role": "communion"}, "영성체 후 기도": {"kind": "proper", "source": "liturgicalDay"}, "공지 사항": {"kind": "choice", "source": "parish", "guide": "본당 공지가 있으면 안내를 듣습니다."}, "강복": {"kind": "choice", "source": "celebrant", "guide": "사제가 선택한 강복 양식에 따라 참여합니다."}, "파견": {"kind": "choice", "source": "celebrant", "guide": "선택된 파견 양식에 따라 응답합니다."}, "파견 성가": {"kind": "hymn", "source": "hymnSet", "role": "recessional"}};
contents[2].splice(1,0,{id:'part-2-item-0-preparation',title:'예물 준비 기도',page:0});
contents[2].splice(contents[2].findIndex(x=>x.id==='part-2-item-5')+1,0,{id:'part-2-item-5-hymn',title:'영성체 성가',page:3});
frameSpecs['봉헌 성가']={kind:'hymn',source:'hymnSet'};frameSpecs['예물 준비 기도']={kind:'prayer',source:'ordinary'};frameSpecs['감사기도 제2양식']=frameSpecs['감사 기도'];frameSpecs['영성체 성가']={kind:'hymn',source:'hymnSet'};

const missalOrdinary = {{missalOrdinary}};
const localOrdinaryReference = missalOrdinary;


// Printed ◎ starts the assembly response; guidance does not end that speech turn.
function spokenSegments(text, initial='text'){
 const segments=[];let role=initial,current=null;
 const add=(kind,value)=>{if(!current || current.kind!==kind){current={kind,parts:[]};segments.push(current);}current.parts.push(value);};
 for(const raw of text.split('\n')){
  const line=raw.trim();if(!line)continue;if(line==='[본문]'){role='text';current=null;continue;}
  if(/^\[(?:원문 지침|안내|프레임 안내|자료 안내)/.test(line) || line.startsWith('인쇄본 안내:')){
   const part={kind:line.startsWith('[원문 지침]')?'rubric':'guide',text:line};if(current && current.kind==='assembly' && (part.kind==='guide'||/^\[원문 지침\] (?:가슴을 치며|이어서 계속한다|밑줄 부분)/.test(line)))current.parts.push(part);else{segments.push({kind:'guide',parts:[part]});current=null;}continue;
  }
  if(line.startsWith('◎'))role='assembly';
  else if(line.startsWith('+'))role='priest';
  else if(line.startsWith('◆'))role='lector';
  else if(line.startsWith('[')){segments.push({kind:'guide',parts:[{kind:'guide',text:line}]});current=null;continue;}
  add(role,{kind:'text',text:line});
 }
 return segments;
}
function spokenRoleAt(text,offset,initial='text'){
 let role=initial;for(const line of text.slice(0,offset).split('\n')){if(line.trim().startsWith('◎'))role='assembly';else if(line.trim().startsWith('+'))role='priest';else if(line.trim().startsWith('◆'))role='lector';}return role;
}
function liturgyNode(text,initial='text'){
 const stack=document.createElement('div');stack.className='reader__liturgy';stack.__sourceText=text;stack.__initialRole=initial;
 spokenSegments(text,initial).forEach(segment=>{
  const parts=find('mode').value==='regular'?segment.parts.filter(part=>part.kind!=='guide'):segment.parts;if(!parts.length)return;
  const card=document.createElement('div');card.className=`reader__speech-card reader__speech-card--${segment.kind}`;
  card.setAttribute('data-speech-role',segment.kind);
  if(['assembly','priest','lector'].includes(segment.kind))card.setAttribute('aria-label',({assembly:'합송',priest:'사제의 부분',lector:'독서자의 부분'})[segment.kind]);

  let speechBody=null;
  const openRow=markerText=>{const row=document.createElement('div');row.className='reader__speech-row';const marker=document.createElement('span');marker.className='reader__speech-marker';marker.setAttribute('aria-hidden','true');marker.textContent=markerText;speechBody=document.createElement('div');speechBody.className='reader__speech-body';row.append(marker,speechBody);card.append(row);};
  parts.forEach(part=>{
   if(part.kind==='guide'||part.kind==='rubric'){const p=document.createElement('p');p.className='reader__speech-text reader__guidance';p.textContent=part.text.replace(/^\[(?:원문 지침|안내|프레임 안내|자료 안내)\]\s*|^인쇄본 안내:\s*/,'');if(part.kind==='rubric'){p.setAttribute('data-source-kind','missal-rubric');const ref=missalOrdinary.rubrics.find(ref=>part.text.includes(ref.text));if(ref){p.setAttribute('data-pdf-page',String(ref.pdfPage));p.title=`경본 ${ref.item}항 · PDF ${ref.pdfPage}쪽`;}}if(!speechBody)openRow('');speechBody.append(p);return;}
   const match=part.text.match(/^([+◎◆○●✠])\s*/);if(match||!speechBody)openRow(match?match[1]:'');
   const p=document.createElement('p');p.className='reader__speech-text';p.textContent=match?part.text.slice(match[0].length):part.text;if(/성령으로 인하여|동정 마리아에게서 육신|사람이 되셨/.test(p.textContent))p.className+=' reader__bow-phrase';const blessing=p.textContent.match(/성부와\s*\+\s*성자와\s*성령/);if(blessing){const full=p.textContent;const before=document.createElement('span');before.textContent=full.slice(0,blessing.index);const marked=document.createElement('span');marked.className='reader__bow-phrase';marked.textContent=blessing[0];const after=document.createElement('span');after.textContent=full.slice(blessing.index+blessing[0].length);p.textContent='';p.append(before,marked,after);}speechBody.append(p);
  });
  stack.append(card);
 });return stack;
}
function normalizeGuidance(root){
 root.querySelectorAll('.reader__guidance').forEach(note=>{
  if(note.closest('.reader__speech-body'))return;
  const card=document.createElement('div');card.className='reader__speech-card reader__speech-card--guide';card.setAttribute('data-guidance-layout','second-column');
  const row=document.createElement('div');row.className='reader__speech-row';const marker=document.createElement('span');marker.className='reader__speech-marker';marker.setAttribute('aria-hidden','true');
  const body=document.createElement('div');body.className='reader__speech-body';note.replaceWith(card);body.append(note);row.append(marker,body);card.append(row);
 });
}
function decorateLiturgy(root){
 Array.from(root.querySelectorAll('.reader__item-text')).forEach(p=>{
  const source=p.textContent;if(!source || p.parentElement?.getAttribute('data-content-source')==='cbck-daily-collect')return;
  const parent=p.parentElement;p.replaceWith(liturgyNode(source));
  if(parent?.classList.contains('reader__content-card') && !parent.classList.contains('reader__content-card--score'))parent.classList.add('reader__content-card--liturgy');
 });
}
function replaceLiturgyText(root,text,initial='text'){
 const target=root.querySelector('.reader__liturgy')||root.querySelector('.reader__item-text');
 if(target){const parent=target.parentElement;target.replaceWith(liturgyNode(text,initial));if(parent?.classList.contains('reader__content-card') && !parent.classList.contains('reader__content-card--score'))parent.classList.add('reader__content-card--liturgy');}
}

const dailyMissaSnapshot = {{dailyMissaSnapshot}};

const dailyDocuments = {{dailyDocuments}};
const dailySources = {{dailySources}};
'use strict';
{{DAILY_DOCUMENT}}
if(validateDocument(dailyDocuments[0],dailySources).length)throw new Error("Invalid daily document");

function updateContentReadiness(){const status=contentReadiness(find('date').value,dailyDocuments,bulletinProvider,hymnScheduleCatalog);const node=find('content-readiness');if(!node)return;node.textContent=find('date').value+' · 본문 '+({ready:'연결됨',partial:'일부 연결 · 미연결 항목 있음',missing:'미연결'}[status.body])+' / 대구 주보 '+(status.bulletin?'해당 날짜 링크 있음':'해당 날짜 미확인 · 목록에서 확인')+' / 성가표 '+(status.hymns?'추천 있음 · 회차 미확정':'미등록');}
function selectedMassDocument(){return selectDocument(dailyDocuments,find('date').value);}
function dailySection(title){return selectedMassDocument()?.sections.find(s=>s.title===title)||null;}
function dailyText(title){const section=dailySection(title);return section?.status==='verified'?section.paragraphs.map(p=>p.text).join('\n'):null;}
function selectedCollectVariants(){
 const record=dailySection('본기도');if(record?.status!=='verified')return [];
 const paragraphs=record.paragraphs;
 return paragraphs.length>1&&paragraphs.every(p=>p.role==='priest'&&p.text.includes('\n'))?paragraphs.map(p=>p.text):[paragraphs.map(p=>p.text).join('\n')];
}
function appendDailySource(root,title){
 const section=dailySection(title);if(section?.status!=='verified')return;
 const refs=[...new Set(section.paragraphs.map(p=>p.sourceRef))];
 refs.forEach(ref=>{const source=dailySources[ref];if(!source?.url)return;const link=document.createElement('a');link.href=source.url;link.target='_blank';link.rel='noopener noreferrer';link.textContent='출처 · '+find('date').value+' '+title;link.setAttribute('data-daily-source',ref);root.append(link);});
}
function stripTerminalResponse(text,response){
 const lines=text.trim().split('\n');
 while(lines.length&&[response,response.replace(/^◎\s*/,''),'주님의 말씀입니다.','◆ 주님의 말씀입니다.','+ 주님의 말씀입니다.'].includes(lines.at(-1).trim()))lines.pop();
 return lines.join('\n').trim();
}
function properPrayerText(title,text){
 if(!text)return '[선택 날짜 '+title+' 자료 미연결]';
 const lines=text.trim().split('\n');while(lines.length&&/^(?:◎\s*)?아멘[.!]?$/.test(lines.at(-1).trim()))lines.pop();
 if(/^[+]?\s*기도합시다\.$/.test(lines[0]?.trim()||''))lines.shift();
 const body=lines.join('\n').trim().replace(/^\+\s*/,'');
 return '+ '+body+'\n◎ 아멘.';
}
function renderDailySection(title){
 const section=document.createElement('section');section.className=title==='화답송'?'reader__item reader__item--psalm':'reader__item';const h=document.createElement('h3');h.className='reader__item-title';h.textContent=title;section.append(h);
 const card=document.createElement('div');card.className='reader__content-card reader__content-card--liturgy';
 if(title==='화답송'){card.className+=' reader__psalm-content';card.tabIndex=0;card.setAttribute('aria-label','화답송 본문 스크롤');}
 const verified=dailySection(title)?.status==='verified';card.setAttribute('data-content-source',verified?'daily-verified-section':'daily-missing');
 const prayer=title==='예물 기도'||title==='영성체 후 기도';
 const invitation=title==='영성체 후 기도'?'+ 기도합시다.\n[원문 지침] '+missalOrdinary.boundaryNotes[title].text+'\n':'';
 if(verified){card.append(liturgyNode(invitation+(prayer?properPrayerText(title,dailyText(title)):dailyText(title))));appendDailySource(card,title);}
 else{if(invitation)card.append(liturgyNode(invitation));const p=document.createElement('p');p.textContent='선택 날짜 자료 미연결';card.append(p);}
 if(title==='화답송'){const p=document.createElement('p');p.textContent=verified?'주보 화답송 악보 미등록 · 현재는 매일미사 텍스트를 표시합니다.':'선택 날짜 화답송 텍스트·악보 미연결';card.append(p);}
 section.append(card);return section;
}

const liturgicalCalendar = {{liturgicalCalendar}};
function selectedCalendarDay(){return liturgicalCalendar.days.find(day=>day.date===find('date').value)||null;}
function selectedDailyData(){return find('date').value===dailyMissaSnapshot.date?dailyMissaSnapshot:null;}
function updateLiturgicalHeading(){
 const calendar=selectedCalendarDay();const season=calendar?.seasonLabel||currentSeason()?.title.replace(/ 시기$/,'')||'시기 미확인';find('liturgical-season').textContent=season;find('liturgical-season').setAttribute('aria-label',season+' 시기 알아보기');find('liturgical-day').textContent=calendar?.label||'전례력 미연결';find('liturgical-day').title=calendar?'전례력 기준 시기·주차 · '+liturgicalCalendar.sourceUrl:'확인된 전례력 범위 밖';const observance=find('mass-observance');if(observance)observance.textContent='현재 자료의 미사 양식: '+(selectedMassDocument()?.observance||'미연결');
}

function renderCollect(){
 const section=document.createElement('section');section.className='reader__item reader__item--collect';const h=document.createElement('h3');h.className='reader__item-title';h.textContent='본기도';const heading=document.createElement('div');heading.className='reader__item-heading';heading.append(h);section.append(heading);
 const invitation=referenceText('본기도').split('[선택 날짜 본기도 자료 미연결]')[0];
 const card=document.createElement('div');card.className='reader__content-card reader__collect-scroll';card.tabIndex=0;card.setAttribute('aria-label','선택 날짜 본기도 본문');
 const variants=selectedCollectVariants();collectView=Math.max(0,Math.min(collectView,variants.length-1));card.setAttribute('data-content-source',variants.length?'daily-verified-collect':'daily-missing');
 if(variants.length){
  if(variants.length>1){const group=document.createElement('div');group.className='reader__prayer-option';group.setAttribute('role','group');group.setAttribute('aria-label','수록 본기도 표시');heading.append(group);variants.forEach((text,index)=>{const button=createReaderButton('본문 '+(index+1));button.setAttribute('aria-pressed',String(collectView===index));button.onclick=()=>{collectView=index;scheduleReflow(section.getAttribute('data-flow-key'));};group.append(button);});}
  card.append(liturgyNode(invitation+properPrayerText('본기도',variants[collectView])));appendDailySource(card,'본기도');
 }else card.append(liturgyNode(invitation+'[선택 날짜 본기도 자료 미연결]'));
 section.append(card);return section;
}
let collectView=0;


const seasonCalendar2026={year:2026,sourceUrl:'https://missa.cbck.or.kr/Liturgy',periods:[
 {key:'ordinary',title:'연중 시기',start:'2026-01-12',end:'2026-02-17',description:'1월 12일 ~ 2월 17일'},
 {key:'lent',title:'사순 시기',start:'2026-02-18',end:'2026-04-01',description:'2월 18일 재의 수요일 ~ 4월 2일 주님 만찬 미사 전'},
 {key:'easter',title:'부활 시기',start:'2026-04-05',end:'2026-05-24',description:'4월 5일 주님 부활 대축일 ~ 5월 24일 성령 강림 대축일 (부활 성야부터)'},
 {key:'ordinary',title:'연중 시기',start:'2026-05-25',end:'2026-11-28',description:'5월 25일 ~ 11월 28일'},
 {key:'advent',title:'대림 시기',start:'2026-11-29',end:'2026-12-24',description:'11월 29일 대림 제1주일 ~ 12월 24일'},
 {key:'christmas',title:'성탄 시기',start:'2026-12-25',end:'2026-12-31',description:'확인 범위:12월 25일 ~ 12월 31일. 다음 해 경계는 별도 확인'}
]};
function currentSeason(date=find('date').value){return seasonCalendar2026.periods.find(x=>date>=x.start && date<=x.end) || null;}
const parishMemorialResponses={
 ordinary:{label:'연중 시기',text:'◎ 주님께서 오실 때까지 주님의 죽음을 전하며 부활을 선포하나이다.',crop:[2050,540,1800,760]},
 lent:{label:'사순 시기',text:'◎ 주님께서 오실 때까지 이 빵을 먹고 이 잔을 마실 적마다 주님의 죽음을 전하나이다.',crop:[2050,1330,1800,710]},
 easter:{label:'부활 시기',text:'◎ 십자가와 부활로 저희를 구원하신 주님, 길이 영광받으소서.',crop:[2050,2100,1800,700]}
};
function memorialResponse(){const season=currentSeason();return season?parishMemorialResponses[season.key]:null;}
let scoreModalOpener=null,seasonModalOpener=null;
function enlargeScoreButton(asset){const b=createReaderButton();b.type='button';b.textContent='크게 보기';b.setAttribute('aria-label','악보 크게 보기');b.classList.add('reader__score-enlarge');b.setAttribute('data-score-path',asset.path);b.setAttribute('aria-haspopup','dialog');b.onclick=()=>showScoreModal([asset],asset.title,b);return b;}
function showScoreModal(assets,title,trigger){
 scoreModalOpener=trigger;const body=find('score-modal-body');body.replaceChildren();find('score-modal-title').textContent=title+' · 악보 크게 보기';
 assets.forEach(asset=>{
  body.append(renderPhoto(asset,true));
 });find('score-modal').showModal();find('score-modal-close').focus();
}
const seasonMeanings = {
 ordinary: {title:'연중 시기', text:'예수 그리스도의 구원 신비 전체를 묵상하며, 그분의 말씀과 삶을 일상에서 따라 살아가는 시기입니다. 성탄 시기 뒤와 부활 시기 뒤, 두 구간으로 나뉩니다.'},
 lent: {title:'사순 시기', text:'예수님의 수난과 죽음을 묵상하며 부활을 준비하는 시기입니다. 기도와 회개, 절제와 이웃을 위한 나눔으로 하느님께 돌아가도록 초대받습니다.'},
 easter: {title:'부활 시기', text:'예수 그리스도의 부활을 기뻐하며 새 생명과 희망을 나누는 시기입니다. 주님 부활 대축일부터 성령 강림 대축일까지 이어지며, 부활하신 주님의 증인으로 살아가도록 초대받습니다.'}
};
let seasonHelpOpener=null;
function showSeasonHelp(key,trigger){
 const meaning=seasonMeanings[key];if(!meaning)return;
 seasonHelpOpener=trigger;find('season-help-title').textContent=meaning.title+'란?';find('season-help-text').textContent=meaning.text;
 find('season-help-source').href='https://home.catholic.or.kr/pdsm/bbs_view.asp?id=185256&menu=4798';
 find('season-help-modal').showModal();find('season-help-close').focus();
}
function showSeasonModal(trigger){
 seasonModalOpener=trigger;const body=find('season-modal-body');body.replaceChildren();const year=find('date').value.slice(0,4);find('season-modal-title').textContent=year+'년 전례 시기';
 if(year==='2026'){
  const current=currentSeason();seasonCalendar2026.periods.forEach(period=>{
   const card=document.createElement('section');card.className='reader__content-card';card.style.padding='var(--reader-content-inset)';
   if(current===period){card.setAttribute('aria-current','true');card.style.borderColor='var(--reader-theme-accent)';card.style.background='var(--state-selected-surface)';}
   const heading=document.createElement('div');heading.className='overlay__header';
   const h=document.createElement('h3');h.className='reader__item-title';h.textContent=period.title+(current===period?' · 현재 선택한 시기':'');
   if(current===period)h.style.color='var(--reader-theme-accent)';
   const help=createReaderButton('?');help.type='button';help.setAttribute('aria-label',period.title+' 의미 알아보기');help.setAttribute('aria-haspopup','dialog');help.setAttribute('aria-controls','season-help-dialog');help.title=period.title+'란?';help.onclick=()=>showSeasonHelp(period.key,help);help.hidden=!seasonMeanings[period.key];
   heading.append(h,help);
   const p=document.createElement('p');p.className='reader__item-text';p.textContent=period.description;
   card.append(heading,p);body.append(card);
  });
  const note=document.createElement('p');note.className='reader__guidance';note.textContent='성주간 목요일 저녁부터 부활 성야 전까지는 파스카 성삼일입니다. 현재 확인한 대림·성탄 범위는 2026년 말까지이며 다음 해 경계·상세 미사 선택은 별도 자료입니다.';body.append(note);
  const source=externalSourceLink(seasonCalendar2026.sourceUrl,'2026년 전례력 자료');body.append(source);
 }else{const p=document.createElement('p');p.className='reader__guidance';p.textContent='선택한 연도의 전례 시기 자료 연결 전입니다.';body.append(p);}
 find('season-modal').showModal();find('season-modal-close').focus();
}

function externalSourceLink(url,label){const link=document.createElement('a');link.href=url;link.target='_blank';link.rel='noopener noreferrer';link.textContent=label;return link;}
function appendMajorPrayerSources(body){const heading=document.createElement('h3');heading.textContent='굿뉴스 주요기도문';const list=document.createElement('ul');majorPrayerCatalog.items.forEach(item=>{const li=document.createElement('li');li.append(externalSourceLink(item.url,item.title+' · 원문'));list.append(li);});body.append(heading,list);}
function appendHymnRecommendations(body,applyRecommendation){const day=hymnScheduleCatalog.days.find(day=>day.date===find('date').value);if(!day){const note=document.createElement('p');note.textContent='선택 날짜 성가표 미등록';body.append(note);return;}const heading=document.createElement('h3');heading.textContent='참고 성가표 · '+hymnScheduleCatalog.edition;const note=document.createElement('p');note.textContent='본당·회차별 확정 전 추천 번호입니다.';body.append(heading,note);[['entrance','입당'],['offertory','예물 준비'],['communion','영성체'],['recessional','파견']].forEach(([key,label])=>{const p=document.createElement('p');p.textContent=label+' · '+(day.recommendations[key].join(', ')||'미등록');body.append(p);});if(applyRecommendation){const apply=createReaderButton('', 'primary');apply.type='button';apply.textContent='이 회차에 적용';apply.onclick=()=>applyRecommendation(day.recommendations);body.append(apply);}body.append(externalSourceLink(hymnScheduleCatalog.sourceUrl,'성가표 출처'));}
function appendBulletinSource(body){const issue=bulletinProvider.issues.find(issue=>issue.date===find('date').value);const p=document.createElement('p');p.append(externalSourceLink(issue?issue.viewUrl:bulletinProvider.indexUrl,'대구대교구 주보'+(issue?' · '+issue.date:'')));if(issue)p.append(externalSourceLink(issue.pdfUrl,' · PDF 열기'));body.append(p);}

function renderMockTextCard(title,source){
 const section=document.createElement('section');section.className='reader__item';const h=document.createElement('h3');h.className='reader__item-title';h.textContent=title;
 const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source',source);const label=document.createElement('p');label.textContent=source==='parish-bulletin-mock'?'주보 공지 · mock · 신부님 안내':'매일미사 본문 · mock';const p=document.createElement('p');p.textContent=frameMock;card.append(label,p);section.append(h,card);
 if(title==='공지 사항'){p.textContent='본당 공지 자료 미연결';appendBulletinSource(section);}else section.append(liturgyNode('◎ 아멘.'));return section;
}
function dismissalChoices(){return referenceText('파견').split('\n').filter(line=>line.startsWith('+')).map((text,i)=>({key:'dismissal-'+i,title:'파견',text}));}

const scoreSourceCatalog = {"자비송": {"title": "자비송", "confirmedNumber": null, "matchStatus": "unresolved", "candidates": [{"numbers": [306], "file": "306 자비송-김대붕(2009-9-13).enc", "path": "../docs/references/catholic-enc/306 자비송-김대붕(2009-9-13).enc", "sha256": "26b04c5f15a51c0074b1d140da4ced6db035ec1881944c358614b84f0189a353", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=306"]}, {"numbers": [310], "file": "310 자비송-손상오(2009-9-18).enc", "path": "../docs/references/catholic-enc/310 자비송-손상오(2009-9-18).enc", "sha256": "88bf262a74423662cf154c37870fb7ae7c86c17ac6afad34b00fc41693d1822d", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=310"]}, {"numbers": [315], "file": "315 자비송-이문근(2009-9-27).enc", "path": "../docs/references/catholic-enc/315 자비송-이문근(2009-9-27).enc", "sha256": "73057d5a828e7ec1e7e8771bfeea4a5ce6bf881b43d094ce6635f01bcbaa6fe9", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=315"]}, {"numbers": [320], "file": "320 자비송-이문근(2009-9-27).enc", "path": "../docs/references/catholic-enc/320 자비송-이문근(2009-9-27).enc", "sha256": "db361099a3271db93aa52b30503a8d8e7a5db1bcffdabb3b0fa2e1609b6ac87c", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=320"]}, {"numbers": [325], "file": "325 자비송-이문근(2009-10-6).enc", "path": "../docs/references/catholic-enc/325 자비송-이문근(2009-10-6).enc", "sha256": "add4fc1788de6125761326b9facd0d0b018a32cf33f93f7a6ebd2d5d81f5fceb", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=325"]}, {"numbers": [350], "file": "350 자비송(위령)-김대붕(2009-12-3).enc", "path": "../docs/references/catholic-enc/350 자비송(위령)-김대붕(2009-12-3).enc", "sha256": "1ae08c3ee71b81dfdec960abf0ac2b3eca46cd6bef585424f3d9edb732dfc77e", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=350"]}, {"numbers": [354], "file": "354 자비송(2009-12-3).enc", "path": "../docs/references/catholic-enc/354 자비송(2009-12-3).enc", "sha256": "f6a9b443bbdeb5c8f3d1c12f58e850ae19c114592491df229c4e855934d62522", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=354"]}]}, "대영광송": {"title": "대영광송", "confirmedNumber": null, "matchStatus": "unresolved", "candidates": [{"numbers": [307], "file": "307 대영광송(2009-9-13).enc", "path": "../docs/references/catholic-enc/307 대영광송(2009-9-13).enc", "sha256": "ad1bab1be99aaa9db78028840b473249f061e9f80cec0d2a5bd2cf846e290d27", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=307"]}, {"numbers": [311], "file": "311 대영광송(2009-9-24).enc", "path": "../docs/references/catholic-enc/311 대영광송(2009-9-24).enc", "sha256": "5f8e123b74bd0ed2b45bcdb4c12be7b1f577fd9d6e5487502adc8339f7f88678", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=311"]}, {"numbers": [316], "file": "316 대영광송(2009-9-27).enc", "path": "../docs/references/catholic-enc/316 대영광송(2009-9-27).enc", "sha256": "9d986eb7da4c31e4dd48c6c7f7ef8360d971c6d294fdc3209527753fa3ee4cc9", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=316"]}, {"numbers": [321], "file": "321 대영광송(2009-9-28).enc", "path": "../docs/references/catholic-enc/321 대영광송(2009-9-28).enc", "sha256": "43e61ac039a835f2a7e693905ad5ed359400f9d4914931239f574e228496b7a0", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=321"]}, {"numbers": [326], "file": "326 대영광송(2009-10-7).enc", "path": "../docs/references/catholic-enc/326 대영광송(2009-10-7).enc", "sha256": "9b4439417f6592004d9ea0c0c9f5045a26b6a7b769cebb87c35898a8d95ba926", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=326"]}]}, "거룩하시도다": {"title": "거룩하시도다", "confirmedNumber": null, "matchStatus": "unresolved", "candidates": [{"numbers": [308], "file": "308 거룩하시도다(2009-9-18).enc", "path": "../docs/references/catholic-enc/308 거룩하시도다(2009-9-18).enc", "sha256": "1ae2aee929fa408a61da26781ffab1902e198498e8f6d01694c350b9c14144c7", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=308"]}, {"numbers": [312], "file": "312 거룩하시도다(2009-9-24).enc", "path": "../docs/references/catholic-enc/312 거룩하시도다(2009-9-24).enc", "sha256": "fb8661e838273aad102ab9c407774840d845e17c9f63178435dc43d77e1a2ec3", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=312"]}, {"numbers": [317], "file": "317 거룩하시도다(2009-9-27).enc", "path": "../docs/references/catholic-enc/317 거룩하시도다(2009-9-27).enc", "sha256": "70cc8a61ee4c161a26e779f7dcfca9add0e8c0fd3b4ea608436c19a8b3e95437", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=317"]}, {"numbers": [322], "file": "322 거룩하시도다(2009-9-30).enc", "path": "../docs/references/catholic-enc/322 거룩하시도다(2009-9-30).enc", "sha256": "3dc8d7d09209cd42830861b1d0559026167b6af26bb55801eb3980856658230d", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=322"]}, {"numbers": [327], "file": "327 거룩하시도다(2009-10-12).enc", "path": "../docs/references/catholic-enc/327 거룩하시도다(2009-10-12).enc", "sha256": "31792820c3de0b4d51d264a0d527546762765fb2f0a394c8db85a43d97f94a5c", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=327"]}, {"numbers": [333], "file": "333 거룩하시도다.enc", "path": "../docs/references/catholic-enc/333 거룩하시도다.enc", "sha256": "088717b54c1dfc69aefed50d755d656ec9567f97a274b00256b1a03563fecf93", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=333"]}, {"numbers": [341], "file": "341 거룩하시도다(2009-10-28).enc", "path": "../docs/references/catholic-enc/341 거룩하시도다(2009-10-28).enc", "sha256": "831d02283c643d04af1b958d1244f63c083fc8c3e61ca232153f5f10afa46371", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=341"]}, {"numbers": [348], "file": "348 거룩하시도다(2009-11-4).enc", "path": "../docs/references/catholic-enc/348 거룩하시도다(2009-11-4).enc", "sha256": "31408d56b55b42de48fd5108941714f5234f038ee1a4137bc25596165216e307", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=348"]}, {"numbers": [351], "file": "351 거룩하시도다(2009-12-3).enc", "path": "../docs/references/catholic-enc/351 거룩하시도다(2009-12-3).enc", "sha256": "106176d3709f912a76535e28ca87d1d840792e3828f935c7e253deb14c92c7f6", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=351"]}, {"numbers": [357], "file": "357 거룩하시도다(2010-11-1).enc", "path": "../docs/references/catholic-enc/357 거룩하시도다(2010-11-1).enc", "sha256": "cfa6b8ef26f3695f26b43971f9035782811e2013d4467c0cae4ca7aef6841b02", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=357"]}]}, "신앙의 신비여": {"title": "신앙의 신비여", "confirmedNumber": null, "matchStatus": "unresolved", "candidates": [{"numbers": [314], "file": "314 신앙의 신비여(2009-9-24).enc", "path": "../docs/references/catholic-enc/314 신앙의 신비여(2009-9-24).enc", "sha256": "5ad591ace24afaeebf7106bea7ec2f4a56c5aa198e13c87dcef7ade6929b1fc8", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=314"]}, {"numbers": [373], "file": "373 신앙의 신비여(2014-4-26).enc", "path": "../docs/references/catholic-enc/373 신앙의 신비여(2014-4-26).enc", "sha256": "68e4b0372d361c2f29846ca1bece6f2cb709fb049f1b853ce8c5b94004e8376e", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=373"]}, {"numbers": [374], "file": "374 신앙의 신비여(2014-4-26).enc", "path": "../docs/references/catholic-enc/374 신앙의 신비여(2014-4-26).enc", "sha256": "b93791d45854b94173f18502ae1673ea2e035a0e9eee04295125424231144db2", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=374"]}, {"numbers": [375], "file": "375 신앙의 신비여(2014-4-26).enc", "path": "../docs/references/catholic-enc/375 신앙의 신비여(2014-4-26).enc", "sha256": "507f524a9b0c5757fb2501c1cda7acfc7b7e582891d1d2bd693aee283008d342", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=375"]}, {"numbers": [376], "file": "376 신앙의 신비여(2014-4-26).enc", "path": "../docs/references/catholic-enc/376 신앙의 신비여(2014-4-26).enc", "sha256": "98a5f4c5623ad1732b6a1ad06295393dd57c08fc3f393f2c5e1eef4c10c11487", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=376"]}]}, "아멘": {"title": "아멘", "confirmedNumber": null, "matchStatus": "unresolved", "candidates": [{"numbers": [377, 378, 379], "file": "377-379 아멘(2014-4-27).enc", "path": "../docs/references/catholic-enc/377-379 아멘(2014-4-27).enc", "sha256": "52af94040330f2e50ca40b708c1036458ce39fbf83f99b983b698d27494e20fc", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=377", "https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=378", "https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=379"]}, {"numbers": [380, 381, 382], "file": "380-382 아멘(2014-4-27).enc", "path": "../docs/references/catholic-enc/380-382 아멘(2014-4-27).enc", "sha256": "c8a340cd13b3264b1f2fa15051b0f6e45560b861183eca9e81cedb96bb88e9da", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=380", "https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=381", "https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=382"]}, {"numbers": [383, 384, 385], "file": "383-385 아멘(2014-4-27).enc", "path": "../docs/references/catholic-enc/383-385 아멘(2014-4-27).enc", "sha256": "01513ddd59142bc59074566f9438e00dfd194739ac53287ec12501a95e047c24", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=383", "https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=384", "https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=385"]}, {"numbers": [386], "file": "386 아멘(2014-4-27).enc", "path": "../docs/references/catholic-enc/386 아멘(2014-4-27).enc", "sha256": "4ed3b4aa646431606c2b0befa67bac9d666db05bc8bf84750712225b620da8af", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=386"]}]}, "주님의 기도": {"title": "주님의 기도", "confirmedNumber": null, "matchStatus": "unresolved", "candidates": [{"numbers": [318], "file": "318 주님의 기도(2009-9-27).enc", "path": "../docs/references/catholic-enc/318 주님의 기도(2009-9-27).enc", "sha256": "179a17c57afdbf9931032b6b0748043c664ab82123cfc30e77e323c4a316840f", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=318"]}, {"numbers": [323], "file": "323 주님의 기도(2009-9-30).enc", "path": "../docs/references/catholic-enc/323 주님의 기도(2009-9-30).enc", "sha256": "ee5aa831e80549abcb51cc73cda12ad5005c538942de46f984a3f7596842bdec", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=323"]}, {"numbers": [387], "file": "387 주님의 기도.enc", "path": "../docs/references/catholic-enc/387 주님의 기도.enc", "sha256": "b6883255a14f5a98b32e3014a65b991c1050e94141319a755367d26319da11a9", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=387"]}, {"numbers": [388], "file": "388 주님의 기도(2014-4-27).enc", "path": "../docs/references/catholic-enc/388 주님의 기도(2014-4-27).enc", "sha256": "fc80e9a533598ea2c4a7d5279a03088135c9b4231b43160e02ac20d42a229af5", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=388"]}]}, "하느님의 어린양": {"title": "하느님의 어린양", "confirmedNumber": null, "matchStatus": "unresolved", "candidates": [{"numbers": [497], "file": "497 하느님의 어린양.enc", "path": "../docs/references/catholic-enc/497 하느님의 어린양.enc", "sha256": "d883b34591ce673b9ec9898b11a9004c6a3d631ed5a0509be26cb18fc0a71960", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=497"]}, {"numbers": [160], "file": "160 하느님의 어린양.enc", "path": "../docs/references/catholic-enc/160 하느님의 어린양.enc", "sha256": "7095af3d48b7d73b4f947a28c2ba98d2cc0c4f24404d714099f4e61c631973ef", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=160"]}, {"numbers": [309], "file": "309 하느님의 어린양(2009-9-18).enc", "path": "../docs/references/catholic-enc/309 하느님의 어린양(2009-9-18).enc", "sha256": "e434f9ea294311353939a0ae8dfde69d05ba4e376f9cc3879b387dc8d876d4e8", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=309"]}, {"numbers": [313], "file": "313 하느님의 어린양(2009-9-24).enc", "path": "../docs/references/catholic-enc/313 하느님의 어린양(2009-9-24).enc", "sha256": "3922bd85718868d748ba036da923e56c2cdaa578f8abba158f6f705fcefd0b1e", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=313"]}, {"numbers": [319], "file": "319 하느님의 어린양(2009-9-27).enc", "path": "../docs/references/catholic-enc/319 하느님의 어린양(2009-9-27).enc", "sha256": "980060472649b01d84f32a01fa546beaf374088a2c42bf9cfd3101ac435f2356", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=319"]}, {"numbers": [324], "file": "324 하느님의 어린양(2009-10-6).enc", "path": "../docs/references/catholic-enc/324 하느님의 어린양(2009-10-6).enc", "sha256": "38851bcf8de1e03a66e8af0eb51f5ab2079e3208e71943d69944c070af059e02", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=324"]}, {"numbers": [328], "file": "328 하느님의 어린양(2009-10-12).enc", "path": "../docs/references/catholic-enc/328 하느님의 어린양(2009-10-12).enc", "sha256": "809e72b4f2211254ece0490924b3ea336190bdf0c1422df5709ee28557e0bb37", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=328"]}, {"numbers": [335], "file": "335 하느님의 어린양.enc", "path": "../docs/references/catholic-enc/335 하느님의 어린양.enc", "sha256": "b6befbfd4313b8df6dcd1ea5e187ef1208466560efcd76236c9599c39f3ed3c4", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=335"]}, {"numbers": [343], "file": "343 하느님의 어린양(2009-10-28).enc", "path": "../docs/references/catholic-enc/343 하느님의 어린양(2009-10-28).enc", "sha256": "730d87ddd20324a7dd2e01fa1a726f9ecb24f0bc4aadbc6fc8f758bb10cc98a7", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=343"]}, {"numbers": [343], "file": "343 하느님의 어린양.enc", "path": "../docs/references/catholic-enc/343 하느님의 어린양.enc", "sha256": "a877f41f2bc30d63854d1d366b319cd053d61fa727074b30e5ec7c4e0591fa6f", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=343"]}, {"numbers": [352], "file": "352 하느님의 어린양(2009-12-3).enc", "path": "../docs/references/catholic-enc/352 하느님의 어린양(2009-12-3).enc", "sha256": "d6ee75feea580529f22d526e0a6f82e4787b98ccf3057fcbfbdc12a2e6a42e96", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=352"]}, {"numbers": [358], "file": "358 하느님의 어린양(2011-1-20).enc", "path": "../docs/references/catholic-enc/358 하느님의 어린양(2011-1-20).enc", "sha256": "a70d7a96d274bb71a365f1fea0e02b80bf244482719c383097800d9989502a8c", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=358"]}]}, "복음 환호송": {"title": "복음 환호송", "confirmedNumber": 365, "matchStatus": "user-confirmed-and-16-note-melody-checked", "candidates": [{"numbers": [331], "file": "331 복음환호송(2009-10-12).enc", "path": "../docs/references/catholic-enc/331 복음환호송(2009-10-12).enc", "sha256": "286db98b05df2da30fd512d76e56d3317e11a2720d9609e9d80b18440fbf55fc", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=331"]}, {"numbers": [339], "file": "339 복음 환호송(2009-10-28).enc", "path": "../docs/references/catholic-enc/339 복음 환호송(2009-10-28).enc", "sha256": "fed4d455950085ef6c23e8b74e0f3bfb990814eacef1daa149b0b7f229425020", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=339"]}, {"numbers": [364], "file": "364 복음환호송(2012-7-14).enc", "path": "../docs/references/catholic-enc/364 복음환호송(2012-7-14).enc", "sha256": "8dadf870a8bde815480b05f28e3e00e9906a9b289c9c1315944885cb972d07ba", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=364"]}, {"numbers": [365], "file": "365 복음환호송(2014-4-25).enc", "path": "../docs/references/catholic-enc/365 복음환호송(2014-4-25).enc", "sha256": "678709a6cf60abeb7e335aa4b2e992d6b08a747a48d2bc4b092d1490c1c28fcd", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=365"]}, {"numbers": [366], "file": "366 복음환호송(2014-4-25).enc", "path": "../docs/references/catholic-enc/366 복음환호송(2014-4-25).enc", "sha256": "68dbf2fb12bc0c7b23acfcfff69b3fb11c1a807be034f68448aec920d43f2166", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=366"]}], "sourceUrl": "https://app.catholic.or.kr/web/sungga/default.asp?flag=5&sunggaId=365"}, "주님의 기도 맺음 환호": {"title": "주님의 기도 맺음 환호", "confirmedNumber": null, "matchStatus": "unresolved", "candidates": [{"numbers": [318], "file": "318 주님의 기도(2009-9-27).enc", "path": "../docs/references/catholic-enc/318 주님의 기도(2009-9-27).enc", "sha256": "179a17c57afdbf9931032b6b0748043c664ab82123cfc30e77e323c4a316840f", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=318"]}, {"numbers": [323], "file": "323 주님의 기도(2009-9-30).enc", "path": "../docs/references/catholic-enc/323 주님의 기도(2009-9-30).enc", "sha256": "ee5aa831e80549abcb51cc73cda12ad5005c538942de46f984a3f7596842bdec", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=323"]}, {"numbers": [387], "file": "387 주님의 기도.enc", "path": "../docs/references/catholic-enc/387 주님의 기도.enc", "sha256": "b6883255a14f5a98b32e3014a65b991c1050e94141319a755367d26319da11a9", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=387"]}, {"numbers": [388], "file": "388 주님의 기도(2014-4-27).enc", "path": "../docs/references/catholic-enc/388 주님의 기도(2014-4-27).enc", "sha256": "fc80e9a533598ea2c4a7d5279a03088135c9b4231b43160e02ac20d42a229af5", "matchStatus": "title-only-not-melody-confirmed", "officialPages": ["https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=388"]}], "note": "주님의 기도 항목에 수록된 맺음 환호가 같은 곡인지 추가 대조 필요"}};

let sourceDialogOpener=null;
function sourceForAsset(asset){return scoreSourceCatalog[asset.sourceKey] || Object.values(scoreSourceCatalog).find(x=>asset.title.startsWith(x.title));}
function sourceCaption(asset){
 const entry=sourceForAsset(asset);if(!entry)return null;const b=document.createElement('small');b.className='reader__score-source';b.textContent=entry.confirmedNumber?'가톨릭성가 '+entry.confirmedNumber+'번':'출처 · 번호 미확인';return b;
}
function showSourceDialog(entry,trigger){
 sourceDialogOpener=trigger;find('source-dialog-title').textContent=entry.title+' · 출처';const body=find('source-dialog-body');body.replaceChildren();const note=document.createElement('p');note.textContent=entry.confirmedNumber?'가톨릭성가 '+entry.confirmedNumber+'번 · 본당 사용곡 사용자 확인 및 알렐루야 선율 대조':'동일 제목의 ZIP 수록 후보입니다. 사진 악보와 선율이 같은 번호는 아직 확인되지 않았습니다. 사진의 17·18 등은 인쇄물 번호이며 가톨릭성가 번호로 확정하지 않습니다.';body.append(note);
 if(entry.sourceUrl){const a=document.createElement('a');a.href=entry.sourceUrl;a.target='_blank';a.rel='noopener noreferrer';a.textContent='굿뉴스 · 지정 성가 출처';body.append(a);}
 const list=document.createElement('ul');entry.candidates.forEach(candidate=>{if(entry.confirmedNumber && !candidate.numbers.includes(entry.confirmedNumber))return;const li=document.createElement('li');const a=document.createElement('a');a.href=encodeURI(candidate.path);a.download=candidate.file;a.textContent=candidate.file;li.append(a);candidate.officialPages.forEach((url,i)=>{const link=document.createElement('a');link.href=url;link.target='_blank';link.rel='noopener noreferrer';link.textContent=' · '+candidate.numbers[i]+'번 정보';li.append(link);});list.append(li);});body.append(list);find('source-dialog').showModal();find('source-dialog-close').focus();
}
function renderAlleluia(part=null){
 const section=document.createElement('section');section.className='reader__item';const row=document.createElement('div');row.className='reader__item-heading';const h=document.createElement('h3');h.className='reader__item-title';h.textContent='복음 환호송';row.append(h);section.append(row);
 const mode=parishPrayerPresentation['복음 환호송']||'chant';const group=document.createElement('div');group.className='reader__prayer-option';group.setAttribute('role','group');group.setAttribute('aria-label','알렐루야 표시 방식');row.append(group);
 [['recite','낭송'],['chant','성가']].forEach(([key,label])=>{const b=createReaderButton();b.type='button';b.classList.add('reader__prayer-button');b.textContent=label;b.setAttribute('aria-pressed',String(mode===key));b.onclick=()=>{parishPrayerPresentation['복음 환호송']=key;scheduleReflow(section.getAttribute('data-flow-key'));};group.append(b);});
 const response=()=>{const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-acclamation-role','assembly');if(mode==='chant')card.append(renderPhoto(reengravedPrincipalScores['복음 환호송'][0]));else {card.className+=' reader__content-card--liturgy';card.append(liturgyNode('◎ 알렐루야, 알렐루야, 알렐루야.'));}return card;};
 const first=response();const choir=document.createElement('div');choir.className='reader__content-card';choir.setAttribute('data-acclamation-role','choir');choir.setAttribute('data-content-source','daily-acclamation-verse');const label=document.createElement('p');label.textContent='성가대';const p=document.createElement('p');p.className='reader__item-text';p.textContent=dailyText('복음 환호송')?.split('\n').find(line=>line.startsWith('○'))||'[선택 날짜의 복음 환호송 구절 미연결]';choir.append(label,p);const last=response();section.append(first,choir,last);if(part==='first')section.replaceChildren(row,first);else if(part==='choir')section.replaceChildren(choir);else if(part==='last')section.replaceChildren(last);return section;
}

const frameMock='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.';
let creedView='nicene';
function referenceText(key){return localOrdinaryReference.records.find(x=>x.key===key)?.text || '';}
function variantCards(key){
 const text=referenceText(key);
 if(key==='인사')return text.split(/\[(?:또는 )?선택지 [123]\]/).slice(1).map((text,i)=>({key:`greeting-${i+1}`,title:`인사 · 선택지 ${i+1}`,text:text.split("\n").filter(line=>!line.trim().startsWith("◎")).join("\n").trim()}));
 if(key==='참회 예식'){
  const parts=text.split(/\[(?:또는 )?선택지 [12] ·[^\]]*\]/).slice(1);
  return parts.map((text,i)=>({key:`penitential-${i+1}`,title:`참회 예식 · 선택지 ${i+1}`,text:i===0?text.trim():text.split('+ 진심으로')[0].trim()}));
 }return [];
}
function kyrieText(){return referenceText('자비송');}
function creedVariants(){
 const text=referenceText('신앙 고백');
 const nicene=text.split(/\[니케아[^\]]*\]/)[1]?.split('[또는 사도 신경]')[0]?.trim() || '';
 const apostles=text.split('[또는 사도 신경]')[1]?.trim() || '';
 return [{key:'nicene',title:'니케아 콘스탄티노플 신경',text:nicene},{key:'apostles',title:'사도 신경',text:apostles}];
}
const readingSelections=Object.create(null);
function readingOptions(title){const doc=selectedMassDocument();return doc?doc.sections.filter(s=>(s.title===title||s.title.startsWith(title+' · 대안 '))&&s.status==='verified'):[];}
function readingSelectionText(title){const options=readingOptions(title);const key=find('date').value+'|'+title;const index=Math.min(readingSelections[key]||0,Math.max(0,options.length-1));return options[index]?.paragraphs.map(p=>p.text).join('\n')||null;}
const dailyRubrics = {{dailyRubrics}};
function selectedRubrics(){return dailyRubrics.days.find(day=>day.date===find('date').value)||null;}
function isItemApplicable(item){const rule=selectedRubrics();if(rule&&item.title==='대영광송')return rule.gloria;if(rule&&item.title==='신앙 고백')return rule.creed;return item.title!=='제2독서'||dailySection('제2독서')?.status!=='not-applicable';}
function addReadingOptions(section,heading,item){const options=readingOptions(item.title);if(options.length<2)return;const row=document.createElement('div');row.className='reader__item-heading';heading.replaceWith(row);const group=document.createElement('div');group.className='reader__prayer-option';group.setAttribute('role','group');group.setAttribute('aria-label',item.title+' 수록 본문 선택');const key=find('date').value+'|'+item.title;options.forEach((option,index)=>{const button=createReaderButton('본문 '+(index+1));button.setAttribute('aria-pressed',String((readingSelections[key]||0)===index));button.onclick=()=>{readingSelections[key]=index;scheduleReflow(item.id);};group.append(button);});row.append(heading,group);}
function readingFrameText(title){
 const actual=readingSelectionText(title);if(!actual)return '[선택 날짜 자료 미연결]';
 if(title==='복음'){
  const lines=actual.split('\n');const intro=lines.find(line=>/^[✠+]/.test(line));if(!intro)return '[선택 날짜 복음 도입문 확인 필요]';
  const body=stripTerminalResponse(lines.filter(line=>line!==intro).join('\n'),'◎ 그리스도님, 찬미합니다.');
  return '+ 주님께서 여러분과 함께.\n◎ 또한 사제(부제)의 영과 함께.\n+ '+intro.replace(/^[✠+]\s*/,'')+'\n[원문 지침] 이렇게 말하며 책과 이마와 입술과 가슴에 십자 표시를 한다.\n◎ 주님, 영광받으소서.\n[본문]\n'+body+'\n+ 주님의 말씀입니다.\n◎ 그리스도님, 찬미합니다.';
 }
 return stripTerminalResponse(actual,'◎ 하느님, 감사합니다.')+'\n◆ 주님의 말씀입니다.\n◎ 하느님, 감사합니다.';
}

function ordinaryText(key, mode='beginner') {
 if(key==='신앙의 신비여'){const response=memorialResponse();return '+ 신앙의 신비여!\n'+(response?response.text:'[선택 날짜의 시기 자료 연결 전]');}
 if(key==='감사기도 제2양식')key='감사 기도';
 if(key==='자비송')return kyrieText();
 if(key==='보편 지향 기도 응답')return '◎ 주님, 저희의 기도를 들어주소서.';
 const keys=key==='거룩하시도다 · 신앙의 신비여'?['거룩하시도다','신앙의 신비여']:[key];
 let text=keys.map(name=>localOrdinaryReference.records.find(record=>record.key===name)?.text || '[제공 통상문 자료에 이 본문 없음]').join('\n\n');
 if(key==='영성체 예식 · 영성체 성가')text=text.split('\n').filter(line=>!line.startsWith('[자료에 오늘 영성체송')).join('\n');
 if(key==='감사 기도')text=text.replace('(타대오와 요한보스코)','(타대오와 협력 주교들)');
 if(key==='감사 기도')text=text.split('\n').filter(line=>!line.startsWith('[자료 안내] 인쇄본에 감사기도') && line!=='[감사송 대화]' && line!=='[감사기도 제2양식 고유 감사송 · 선택 가능]').join('\n');
 return mode==='regular'?text.split('\n').filter(line=>!line.startsWith('[안내]')).join('\n'):text;
}

// The prototype holds parish presentation choices in memory only, shared by all Sunday sessions.
const parishPrayerPresentation = Object.create(null);
parishPrayerPresentation['보편 지향 기도 응답']='chant';
const prayerSourceRefs = {textRef:null, scoreRef:null, sourceUrl:null, licenseStatus:'unverified'};
const temporaryPrincipalScores = {"자비송": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020.jpg", "title": "자비송", "rotation": 0, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}], "대영광송": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_01.jpg", "title": "대영광송 앞부분", "rotation": -90, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}, {"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_02.jpg", "title": "대영광송 이어지는 부분", "rotation": 180, "width": 4000, "height": 3000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}], "거룩하시도다 · 신앙의 신비여": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_03.jpg", "title": "거룩하시도다 · 신앙의 신비여 (함께 촬영)", "rotation": 180, "width": 4000, "height": 3000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}], "아멘": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_04.jpg", "title": "아멘", "rotation": 0, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}], "주님의 기도": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_05.jpg", "title": "주님의 기도 앞부분", "rotation": 0, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}, {"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_06.jpg", "title": "주님의 기도 이어지는 부분", "rotation": 0, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}], "주님의 기도 맺음 환호": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_07.jpg", "title": "주님의 기도 맺음 환호 · 하느님의 어린양 (함께 촬영)", "rotation": 0, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}], "하느님의 어린양": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_07.jpg", "title": "하느님의 어린양 · 주님의 기도 맺음 환호 (함께 촬영)", "rotation": 0, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}]};

temporaryPrincipalScores['거룩하시도다']=temporaryPrincipalScores['거룩하시도다 · 신앙의 신비여'];
temporaryPrincipalScores['신앙의 신비여']=temporaryPrincipalScores['거룩하시도다 · 신앙의 신비여'];

temporaryPrincipalScores['대영광송']=temporaryPrincipalScores['대영광송'].flatMap((asset,index)=>[
 {...asset,title:`대영광송 ${index*2+1}쪽`,crop:[0,0,2000,3000]},
 {...asset,title:`대영광송 ${index*2+2}쪽`,crop:[2000,0,2000,3000]}
]);
temporaryPrincipalScores['거룩하시도다']=temporaryPrincipalScores['거룩하시도다'].map(asset=>({...asset,crop:[0,0,2000,3000],title:'거룩하시도다'}));
temporaryPrincipalScores['신앙의 신비여']=temporaryPrincipalScores['신앙의 신비여'].map(asset=>({...asset,crop:[2000,0,2000,3000],title:'신앙의 신비여'}));

temporaryPrincipalScores['하느님의 어린양']=temporaryPrincipalScores['하느님의 어린양'].map(asset=>({...asset,crop:[360,1800,2460,1960],title:'하느님의 어린양'}));

const reengravedPrincipalScores = {{reengravedPrincipalScores}};
function scoreAssets(prayerId) { if(prayerId==='복음 환호송')return reengravedPrincipalScores[prayerId]||[]; if(prayerId==='신앙의 신비여'){const season=currentSeason()?.key;return find('slot').value==='main' && season?(reengravedPrincipalScores[prayerId]||[]).filter(asset=>asset.season===season):[];}return find('slot').value === 'main' ? (reengravedPrincipalScores[prayerId] || temporaryPrincipalScores[prayerId] || []) : []; }
function selectedSlotName() { return find('slot').selectedOptions[0].textContent; }

const scorePreviewSizes = {{scorePreviewSizes}};
function renderPhoto(asset,enlarged=false){
 const figure=document.createElement('figure');figure.className='reader__score';figure.setAttribute('data-score-kind',asset.kind==='engraved'?'reengraved':asset.kind==='mock'?'mock':'photo');
 const caption=document.createElement('figcaption');caption.className='reader__score-heading';caption.textContent=asset.kind==='remote'?'':(asset.kind==='engraved'?'교중미사 재조판 · ':asset.kind==='mock'?'악보 목데이터 · ':asset.kind==='remote'?'':'교중미사 임시 악보 · ')+asset.title+' ';if(!enlarged){caption.textContent='';caption.append(enlargeScoreButton(asset));}if(!enlarged)figure.append(caption);
 if(asset.kind==='engraved'||asset.kind==='mock'||asset.kind==='remote'){
  const preview=document.createElement('img');preview.className='reader__score-photo';const dimensions=scorePreviewSizes[asset.preview||asset.path];if(dimensions){preview.setAttribute('width',String(dimensions[0]));preview.setAttribute('height',String(dimensions[1]));}preview.src=encodeURI(asset.preview||asset.path);preview.alt=asset.title+(asset.kind==='mock'?' · 악보 목데이터':asset.kind==='remote'?' · 굿뉴스 단성 악보':' · PDF와 동일한 조판');if(asset.kind==='remote'){const message=document.createElement('p');message.setAttribute('role','status');message.textContent=asset.title+' · 악보 불러오는 중';const retry=createReaderButton();retry.type='button';retry.textContent='악보 다시 시도';retry.hidden=true;const loaded=()=>{message.textContent='';retry.hidden=true;preview.hidden=false;};preview.onload=loaded;preview.onerror=()=>{preview.hidden=true;message.textContent=asset.title+' · 악보를 불러오지 못했습니다. 번호와 인터넷 연결을 확인해 주세요.';retry.hidden=false;};retry.onclick=()=>{message.textContent=asset.title+' · 악보 불러오는 중';retry.hidden=true;preview.src=encodeURI(asset.preview||asset.path);};figure.append(message,retry);if(preview.complete&&preview.naturalWidth>0)loaded();}figure.append(preview);
 }else{
  const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('class','reader__score-photo');svg.setAttribute('role','img');svg.setAttribute('aria-label',asset.title+' · 사용자 제공 사진');
  const quarter=Math.abs(asset.rotation)===90;const width=quarter?asset.height:asset.width;const height=quarter?asset.width:asset.height;svg.setAttribute('viewBox',asset.crop?asset.crop.join(' '):`0 0 ${width} ${height}`);
  const image=document.createElementNS('http://www.w3.org/2000/svg','image');image.setAttribute('href',encodeURI(asset.path));image.setAttribute('width',String(asset.width));image.setAttribute('height',String(asset.height));if(asset.rotation===-90)image.setAttribute('transform',`translate(0 ${asset.width}) rotate(-90)`);if(asset.rotation===180)image.setAttribute('transform',`translate(${asset.width} ${asset.height}) rotate(180)`);svg.append(image);figure.append(svg);
 }if(!enlarged){const source=sourceCaption(asset);if(source)figure.append(source);}applyComponentStyles(figure);return figure;
}
let guidanceOpener=null,guidanceAnchor=null;
function compactLongGuidance(root){
 const notes=Array.from(root.querySelectorAll('.reader__guidance')).filter(note=>!note.hasAttribute('data-source-kind')&&!note.hidden&&!note.closest('[hidden]')&&note.textContent.trim().length>80);
 if(!notes.length)return;
 const heading=root.querySelector('.reader__item-heading');if(!heading)return;
 const button=createReaderButton();button.type='button';button.classList.add('reader__guidance-toggle');button.innerHTML='<svg class="reader__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10v.01"/></svg>';button.setAttribute('aria-haspopup','dialog');button.setAttribute('aria-label',(root.querySelector('h3')?.textContent||'기도')+' 안내');
 const text=notes.map(note=>note.textContent.replace(/^안내\s*·\s*/, '').trim()).join('\n\n');notes.forEach(note=>note.remove());
 button.onclick=()=>{guidanceOpener=button;guidanceAnchor=root.getAttribute('data-flow-key');find('guidance-title').textContent=(root.querySelector('h3')?.textContent||'기도')+' 안내';find('guidance-copy').textContent=text;find('guidance-dialog').showModal();find('guidance-close').focus();};heading.append(button);
}
function renderPrayerFrame(title, prayerId, scoreSlot=true, level=3) {
 const frame=document.createElement('section');frame.className='reader__item';
 const headingRow=document.createElement('div');headingRow.className='reader__item-heading';
 const heading=document.createElement(`h${level}`);heading.className='reader__item-title';heading.textContent=title;headingRow.append(heading);
 const group=document.createElement('div');group.className='reader__prayer-option';group.setAttribute('role','group');group.setAttribute('aria-label',`${title} 표시 방식`);
 const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source','ordinary+temporaryPrincipalScores');
 if(scoreSlot)headingRow.append(group);frame.append(headingRow,card);
 let printedGuide=null;
 if(prayerId==='대영광송'){
  printedGuide=document.createElement('p');printedGuide.className='reader__guidance';printedGuide.textContent=referenceText('대영광송').split('\n')[0].replace(/^\[(?:원문 지침|안내)\]\s*/, '');frame.insertBefore(printedGuide,card);
 }
 function fill() {
  card.replaceChildren();group.replaceChildren();if(printedGuide){printedGuide.hidden=false;printedGuide.setAttribute('data-source-kind','missal-rubric');}const assets=scoreAssets(prayerId);
  const mode=parishPrayerPresentation[prayerId] || (assets.length?'chant':'recite');
  const compactScore=assets.length===1 && assets[0].systems>0 && (assets[0].systems<=3 || prayerId==='거룩하시도다');
  const fullScorePage=mode==='chant' && assets.length>0 && !compactScore;
  frame.className=fullScorePage?'reader__item reader__item--score':compactScore && mode==='chant'?'reader__item reader__item--compact-score':'reader__item';

  card.className=fullScorePage?'reader__content-card reader__content-card--score':'reader__content-card';
  if(compactScore){card.setAttribute('data-score-layout','compact');if(mode==='chant')card.className+=' reader__content-card--compact';}
  if(scoreSlot)[['recite','낭송'],['chant','성가']].forEach(([value,text])=>{
   const button=createReaderButton();button.type='button';button.classList.add('reader__prayer-button');button.textContent=text;button.setAttribute('aria-pressed',String(mode===value));button.setAttribute('data-prayer-mode',value);
   button.onclick=()=>{parishPrayerPresentation[prayerId]=value;fill();group.querySelector(`[data-prayer-mode="${value}"]`)?.focus();
     if(frame.closest('.reader__book')){pendingPrayerFocus={key:frame.getAttribute('data-flow-key'),mode:value};scheduleReflow(frame.getAttribute('data-flow-key'));}
    };group.append(button);
  });
  if(mode==='chant' && scoreSlot){
   if(assets.length){
    const scoreWindow=document.createElement('div');scoreWindow.className='reader__score-scroll';scoreWindow.setAttribute('tabindex','0');scoreWindow.setAttribute('role','region');scoreWindow.setAttribute('aria-label',`${title} 악보 · 카드 안에서 스크롤`);
    assets.forEach(asset=>scoreWindow.append(renderPhoto(asset)));card.append(scoreWindow);
   }
   else{const p=document.createElement('p');p.textContent=`${selectedSlotName()} · 이 기도문의 임시 악보 미등록`;card.append(p);}
  } else {const p=document.createElement('p');p.className='reader__item-text';p.lang='ko';const text=ordinaryText(prayerId,find('mode').value);p.textContent=prayerId==='대영광송'?text.split('\n').filter(line=>line.trim()!==referenceText('대영광송').split('\n')[0].trim()).join('\n'):text;card.append(p);}
  if(mode==='chant'&&prayerId!=='대영광송'){const source=missalOrdinary.records.find(r=>r.key===prayerId);const first=source?.rubrics?.[0];if(first){const p=document.createElement('p');p.className='reader__guidance';p.setAttribute('data-source-kind','missal-rubric');p.setAttribute('data-pdf-page',String(first.pdfPage));p.textContent=first.text;card.prepend(p);}}
  decorateLiturgy(card);normalizeGuidance(card);
 }
 fill();normalizeGuidance(frame);compactLongGuidance(frame);return frame;
}

let creedDate=null;
function renderCreed(){
 const date=find('date').value;if(creedDate!==date){creedDate=date;creedView=['lent','easter'].includes(currentSeason()?.key)?'apostles':'nicene';}
 const frame=document.createElement('section');frame.className='reader__item reader__item--score';
 const row=document.createElement('div');row.className='reader__item-heading reader__creed-heading';
 const h=document.createElement('h3');h.className='reader__item-title';h.textContent='신앙 고백';row.append(h);
 const group=document.createElement('div');group.className='reader__prayer-option';group.setAttribute('role','group');group.setAttribute('aria-label','신앙 고백 양식 표시');row.append(group);frame.append(row);
 const cards=[];const buttons=[];
 creedVariants().forEach(variant=>{
  const card=document.createElement('div');card.className='reader__content-card reader__content-card--score reader__creed-panel';card.setAttribute('data-variant',variant.key);
  const scroll=document.createElement('div');scroll.className='reader__text-scroll';scroll.tabIndex=0;scroll.setAttribute('role','region');scroll.setAttribute('aria-label',variant.title+' · 카드 내부 스크롤');
  
  const p=document.createElement('p');p.className='reader__item-text';p.textContent=variant.text;scroll.append(p);card.append(scroll);frame.append(card);cards.push([variant.key,card]);
  const b=createReaderButton();b.type='button';b.classList.add('reader__prayer-button');b.textContent=variant.key==='nicene'?'니케아 신경':'사도 신경';b.setAttribute('data-creed-view',variant.key);b.onclick=()=>{creedView=variant.key;sync();};group.append(b);buttons.push([variant.key,b]);
 });
 function sync(){cards.forEach(([key,card])=>card.hidden=key!==creedView);buttons.forEach(([key,b])=>b.setAttribute('aria-pressed',String(key===creedView)));}
 const help=createReaderButton();help.innerHTML='<svg class="reader__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10v.01"/></svg>';help.classList.add('reader__guidance-toggle');help.setAttribute('aria-label','신앙 고백 안내');help.title='신앙 고백 안내';help.setAttribute('aria-haspopup','dialog');help.onclick=()=>{guidanceOpener=help;guidanceAnchor=frame.getAttribute('data-flow-key');find('guidance-title').textContent='신앙 고백';find('guidance-copy').textContent=missalOrdinary.boundaryNotes['신앙 고백'].text;find('guidance-dialog').showModal();find('guidance-close').focus();};row.append(help);decorateLiturgy(frame);sync();return frame;
}

{{HYMN_STATE}}
{{HYMN_BACKUP}}
const hymnTitles={'입당 성가':'entrance','봉헌 성가':'offertory','영성체 성가':'communion','파견 성가':'recessional'};
function defaultHymnsForDate(date=find('date').value){
 const day=hymnScheduleCatalog?.days?.find(d=>d.date===date);
 if(!day?.recommendations)return cleanHymnSet(null);
 return {
  entrance:day.recommendations.entrance?[...day.recommendations.entrance]:[],
  offertory:day.recommendations.offertory?[...day.recommendations.offertory]:[],
  communion:day.recommendations.communion?[...day.recommendations.communion]:[],
  recessional:day.recommendations.recessional?[...day.recommendations.recessional]:[]
 };
}
function currentHymns(){
 try{
  const saved=readHymnSet(localStorage,find('date').value,find('slot').value);
  const hasAny=hymnRoles.some(role=>saved[role]?.length>0);
  if(hasAny)return saved;
 }catch{}
 return defaultHymnsForDate(find('date').value);
}
function saveCurrentHymns(value){return writeHymnSet(localStorage,find('date').value,find('slot').value,value);}
function appendHymnEditor(body){
 const heading=document.createElement('p');heading.textContent=find('date').value+' · '+selectedSlotName()+' · 사용자 편성';body.append(heading);
 const form=document.createElement('form'),inputs={},status=document.createElement('p');form.className='reader__hymn-form';status.setAttribute('role','status');
 for(const [title,role] of Object.entries(hymnTitles)){const label=document.createElement('label');label.className='reader__hymn-field';const name=document.createElement('span');name.textContent=title;label.append(name);const input=document.createElement('input');input.type='text';input.setAttribute('aria-label',title+' 편성 번호');input.value=currentHymns()[role].join(', ');inputs[role]=input;label.append(input);form.append(label);}
 const save=createReaderButton('', 'primary');save.type='submit';save.classList.add('reader__hymn-save');save.textContent='편성 저장';form.append(save);body.append(form,status);appendHymnBackupControls(body);
 let undo=null;const undoButton=createReaderButton();undoButton.type='button';undoButton.textContent='적용 취소';undoButton.hidden=true;body.append(undoButton);
 const commit=value=>{try{const previous=currentHymns();if(hymnRoles.every(role=>JSON.stringify(previous[role])===JSON.stringify(value[role]))){status.textContent='현재 편성과 같습니다.';return true;}saveCurrentHymns(value);undo=previous;for(const role of hymnRoles)inputs[role].value=value[role].join(', ');undoButton.hidden=false;status.textContent='저장했습니다.';scheduleReflow(currentAnchor);return true;}catch{status.textContent='저장하지 못했습니다. 브라우저 저장소 설정을 확인해 주세요.';return false;}};
 form.onsubmit=event=>{event.preventDefault();try{const value={};for(const role of hymnRoles)value[role]=parseHymnNumbers(inputs[role].value);commit(value);}catch(error){status.textContent=error.message;}};
 undoButton.onclick=()=>{if(undo&&commit(undo)){undo=null;undoButton.hidden=true;status.textContent='이전 편성으로 복원했습니다.';}};
 const legacyButton=createReaderButton();legacyButton.type='button';legacyButton.textContent='구버전 번호 가져오기 검토';body.append(legacyButton);legacyButton.onclick=()=>{try{const legacy=readLegacyHymnNumbers(localStorage,find('date').value,find('slot').value);if(!legacy){status.textContent='현재 날짜·회차의 구버전 내 본당 편성이 없습니다. 다른 파일·브라우저의 저장소는 여기서 읽을 수 없습니다.';return;}const box=document.createElement('div'),note=document.createElement('p');note.textContent='번호만 가져옵니다. 구버전 제목·가사·메모·URL은 원래 저장소에 유지되며, 새 번호 백업에는 포함되지 않습니다.';box.append(note);for(const [title,role] of Object.entries(hymnTitles)){const line=document.createElement('p');line.textContent=title+' · '+(currentHymns()[role].join(', ')||'미등록')+' → '+(legacy[role].join(', ')||'미등록');box.append(line);}const apply=createReaderButton();apply.type='button';apply.textContent='구버전 번호 적용';apply.onclick=()=>{if(commit(legacy))box.remove();};const cancel=createReaderButton();cancel.type='button';cancel.textContent='가져오기 취소';cancel.onclick=()=>box.remove();box.append(apply,cancel);body.append(box);}catch(error){status.textContent='가져오지 못했습니다 · '+error.message;}};
 appendHymnRecommendations(body,commit);
}
function hymnAssignmentKey(title){return find('date').value+'|'+find('slot').value+'|'+title;}
function hymnScoreAsset(number,title){return {kind:'remote',title:'가톨릭성가 '+number+'번 · '+title,path:'https://maria.catholic.or.kr/sungga/Files/img/2012/201204'+String(number).padStart(4,'0')+'.jpg'};}
function renderHymnScore(headingTitle){
 const section=document.createElement('section');section.className='reader__item reader__item--score';
 const row=document.createElement('div');row.className='reader__item-heading reader__hymn-heading';const title=document.createElement('h3');title.className='reader__item-title';title.textContent=headingTitle;row.append(title);
 const form=document.createElement('form');form.className='reader__hymn-number-form';
 const label=document.createElement('label');const id='hymn-number-'+({'입당 성가':'entrance','봉헌 성가':'offertory','영성체 성가':'communion','파견 성가':'recessional'})[headingTitle];label.htmlFor=id;label.textContent='번호';const input=document.createElement('input');input.id=id;input.type='text';input.setAttribute('aria-label',headingTitle+' 성가 번호');input.value=currentHymns()[hymnTitles[headingTitle]].join(', ');
 const submit=createReaderButton();submit.type='submit';submit.textContent='확인';form.append(label,input,submit);
 const card=document.createElement('div');card.className='reader__content-card reader__content-card--score';card.setAttribute('data-content-source','goodnews-monophonic-score');
 const scroll=document.createElement('div');scroll.className='reader__score-scroll';scroll.setAttribute('tabindex','0');scroll.setAttribute('role','region');scroll.setAttribute('aria-label',headingTitle+' 악보');
 const status=document.createElement('p');status.setAttribute('aria-live','polite');
 const fill=()=>{scroll.replaceChildren();const numbers=currentHymns()[hymnTitles[headingTitle]];if(numbers.length){numbers.forEach(number=>scroll.append(renderPhoto(hymnScoreAsset(number,headingTitle))));status.textContent='';status.hidden=true;}else{status.textContent='성가 번호를 입력해 주세요.';status.hidden=false;}};
 form.onsubmit=event=>{event.preventDefault();try{const numbers=parseHymnNumbers(input.value);saveCurrentHymns({...currentHymns(),[hymnTitles[headingTitle]]:numbers});fill();}catch(error){status.hidden=false;status.textContent=error.message;}};
 row.append(form);card.append(status,scroll);section.append(row,card);fill();return section;
}
let intercessionView='recite';
function intercessionControls(anchor){const group=document.createElement('div');group.className='reader__prayer-option';group.setAttribute('role','group');group.setAttribute('aria-label','보편 지향 기도 응답 네 곳 표시');[['recite','낭송'],['chant','악보']].forEach(([value,label])=>{const b=createReaderButton();b.type='button';b.classList.add('reader__prayer-button');b.textContent=label;b.setAttribute('aria-pressed',String(intercessionView===value));b.onclick=()=>{intercessionView=value;scheduleReflow(anchor);};group.append(b);});return group;}
function renderIntercessionResponse(){const node=document.createElement('section');node.className='reader__item';const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source','parish-response-card');card.setAttribute('data-response-view',intercessionView);if(intercessionView==='recite')card.className+=' reader__content-card--liturgy';if(intercessionView==='chant'){const p=document.createElement('p');p.textContent='악보 준비 중';card.append(p);}else card.append(liturgyNode('◎ 주님, 저희의 기도를 들어주소서.'));node.append(card);return node;}
let penitentialView=0;
function renderPenitential(){
 const frameAnchor=contents[0].find(item=>item.title==='참회 예식').id;const node=document.createElement('section');node.className='reader__item reader__item--score';const row=document.createElement('div');row.className='reader__item-heading reader__penitential-heading';const h=document.createElement('h3');h.className='reader__item-title';h.textContent='참회 예식';row.append(h);
 const group=document.createElement('div');group.className='reader__prayer-option';group.setAttribute('role','group');group.setAttribute('aria-label','참회 예식 양식');row.append(group);
 const card=document.createElement('div');card.className='reader__content-card reader__collect-scroll';const fill=()=>{group.replaceChildren();card.replaceChildren();['제1양식','제2양식','제3양식'].forEach((label,index)=>{const b=createReaderButton();b.type='button';b.textContent=label;b.classList.add('reader__prayer-button');b.setAttribute('aria-pressed',String(penitentialView===index));b.onclick=()=>{penitentialView=index;scheduleReflow(frameAnchor);};group.append(b);});const form=missalOrdinary.penitentialForms[penitentialView];card.setAttribute('data-missal-form',form.id);card.append(liturgyNode(referenceText(form.key)));};node.append(row,card);fill();return node;
}

function renderItem(item) {
 if(item.title==='자비송'&&penitentialView===2){const node=document.createElement('section');node.className='reader__item';const heading=document.createElement('h3');heading.className='reader__item-title';heading.textContent='자비송';const note=document.createElement('p');note.className='reader__guidance';note.textContent='제3양식에 포함되어 따로 반복하지 않습니다.';node.append(heading,note);return node;}
 if(['예물 기도','영성체 후 기도','화답송'].includes(item.title))return renderDailySection(item.title);
 if(['입당 성가','봉헌 성가','영성체 성가','파견 성가'].includes(item.title))return renderHymnScore(item.title);
 
 if(item.title==='강론'){const node=document.createElement('section');node.className='reader__item';const h=document.createElement('h3');h.className='reader__item-title';h.textContent='강론';const card=document.createElement('div');card.className='reader__content-card';const p=document.createElement('p');p.className='reader__guidance';p.setAttribute('data-source-kind','missal-rubric');p.textContent=missalOrdinary.boundaryNotes['강론'].text;card.append(p);node.append(h,card);return node;}
 if(item.title==='공지 사항')return renderMockTextCard(item.title,'parish-bulletin-mock');
 if(item.title==='예물 준비 기도'){const node=renderMockTextCard(item.title,'ordinary');node.replaceChildren();const h=document.createElement('h3');h.className='reader__item-title';h.textContent=item.title;node.append(h,liturgyNode(referenceText('예물 준비 · 봉헌 성가').split('\n').filter(line=>!line.startsWith('[자료 안내]')).join('\n')));return node;}
 const spec=frameSpecs[item.title];
 if(item.title==='본기도')return renderCollect();
 if(item.title==='신앙 고백')return renderCreed();
 if(item.title==='복음 환호송')return renderAlleluia();
 let section;
 if(spec.kind==='prayer') section=renderPrayerFrame(item.title,spec.prayerId,spec.scoreSlot);
 else {
  section=document.createElement('section');section.className='reader__item';
  const h=document.createElement('h3');h.className='reader__item-title';h.textContent=item.title;section.append(h);
  if(['제1독서','제2독서','복음'].includes(item.title))addReadingOptions(section,h,item);
  if(['제1독서','제2독서','복음','보편 지향 기도'].includes(item.title)){
   const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source',dailyText(item.title)?'daily-verified-section':'daily-missing');const p=document.createElement('p');p.className='reader__item-text';p.textContent=readingFrameText(item.title);card.append(p);appendDailySource(card,item.title);section.append(card);
  }else if(item.title==='화답송'){
   const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source','parish-bulletin-score');const p=document.createElement('p');p.textContent='주보 화답송 악보 표시 영역 · 악보 미등록';const note=document.createElement('p');note.textContent='주보 악보를 연결하면 이 카드 안에 표시합니다.';card.append(p,note);section.append(card);
  }else if(item.title==='본기도'){
   const card=document.createElement('div');card.className='reader__content-card';const p=document.createElement('p');p.className='reader__item-text';p.textContent=ordinaryText('본기도',find('mode').value);card.append(p);section.append(card);
  }else if(spec.kind==='choice'){const p=document.createElement('p');p.className='reader__item-text';p.textContent=ordinaryText(item.title==='영성체 예식 · 영성체 성가'?'영성체 예식 · 영성체 성가':item.title,find('mode').value);section.append(p);}
  else {const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source',spec.source);const p=document.createElement('p');p.className='reader__item-text';p.lang='ko';p.textContent=ordinaryText(item.title==='영성체 예식 · 영성체 성가'?'영성체 예식 · 영성체 성가':item.title,find('mode').value);card.append(p);section.append(card);}
 }
 section.id=item.id;section.tabIndex=-1;
 if(item.id===selectedItem){section.setAttribute('aria-current','location');}
 return section;
}

let selectedItem = null;
function jumpToItem(partIndex, item) {
 part=partIndex;selectedItem=item.id;render({anchorKey:item.id});
 const target=document.getElementById(item.id);target?.focus({preventScroll:true});
}

let part = 0, spread = 0, opener = null;
const position = parts.map(() => null);
const titles = {toc:'미사 목차',hymn:'회차별 성가',prayer:'주요 기도문',menu:'메뉴',settings:'보기 설정',info:'안내 · 프로토타입'};
function context() { updateParishSessions();updateLiturgicalHeading();updateContentReadiness();find('context').textContent = `${selectedSlotName()} · 날짜별 공통 미사 문서 · 통상문 경본 대조 1차 완료 · 날짜별 자료 상태는 아래 표시 · Hi-fi 프로토타입 v1`; }
function renderToc() {
 const visibleIds=viewerOrientation==='portrait'?new Set([selectedItem]):new Set(layouts.slice(spread*2,spread*2+2).flatMap(page=>page.blocks.map(block=>block.tocId)));const nav=find('toc-rail');const rail=nav.parentElement;const previousScroll=rail.scrollTop;let activeLink=null;nav.replaceChildren();
 parts.forEach((item,partIndex)=>{
  const group=document.createElement('section');const heading=document.createElement('h3');heading.className='reader__toc-group-title';heading.textContent=item.title;
  const list=document.createElement('ol');list.className='reader__toc-list';
  contents[partIndex].filter(isItemApplicable).forEach(entry=>{
   const li=document.createElement('li');const index=contents[partIndex].indexOf(entry);const isVisible=partIndex===part && visibleIds.has(entry.id);if(isVisible){li.className='reader__toc-visible';if(!visibleIds.has(contents[partIndex][index-1]?.id))li.className+=' reader__toc-visible--first';if(!visibleIds.has(contents[partIndex][index+1]?.id))li.className+=' reader__toc-visible--last';}const link=document.createElement('a');link.className='reader__toc-link';link.href=`#${entry.id}`;link.textContent=entry.title;
   if(entry.id===selectedItem){activeLink=link;link.setAttribute('aria-current','location');link.setAttribute('aria-label',`${entry.title} · 현재 위치`);}
   link.onclick=event=>{event.preventDefault();jumpToItem(partIndex,entry);};li.append(link);list.append(li);
  });const major=document.createElement('a');major.className='reader__toc-major';major.href='#'+contents[partIndex][0].id;major.textContent=item.title;major.setAttribute('aria-current',String(partIndex===part));major.onclick=event=>{event.preventDefault();go(partIndex);};group.append(heading,major,list);nav.append(group);
 });rail.scrollTop=previousScroll;if(activeLink && rail.getBoundingClientRect){const r=rail.getBoundingClientRect(),a=activeLink.getBoundingClientRect();rail.scrollTop=Math.max(0,rail.scrollTop+a.top-r.top-rail.clientHeight*0.25);}
}


let layouts=[],currentAnchor=null,pendingPrayerFocus=null,reflowFrame=null;
const dailyIntercessions20261018=[
 '교회를 위하여 기도합시다.\n거룩하신 주님, 주님의 교회에 그리스도의 빛을 비추시어, 교회가 구원의 신비를 깊이 깨닫고, 그 신비에 온전히 참여하며, 민족들의 복음화에 힘쓰게 하소서.',
 '세계 지도자들을 위하여 기도합시다.\n자비하신 주님, 세계 지도자들에게 사랑과 절제의 영을 주시어, 자국의 이익만을 생각하기보다 고통을 겪는 나라들을 살피며 공동선을 실현하도록 이끌어 주소서.',
 '감옥에 갇힌 이들을 위하여 기도합시다.\n위로의 샘이신 주님, 감옥에 갇힌 이들을 참된 회개로 이끌어 주시어, 죄를 진심으로 뉘우치며 새 삶을 준비하게 하시고, 그들의 범죄로 피해받은 이들에게 위로와 힘을 주소서.',
 '가정 공동체를 위하여 기도합시다.\n사랑이신 주님, 어려움에 있는 가정들을 돌보아 주시어, 주님의 한결같은 사랑과 자비를 믿고 온전히 의탁하며, 어머니인 교회 안에서 힘을 얻게 하소서.'
];
function universalPrayerBlocks(item){
 const record=dailySection('보편 지향 기도');const lines=record?.status==='verified'?record.paragraphs.map(p=>p.text):[];const petitions=[];let current=null;
 for(const line of lines){if(/^\d+\. /.test(line)){current={text:line.replace(/^\d+\. /,''),body:[]};petitions.push(current);}else if(current)current.body.push(line);}
 if(!petitions.length)return [{key:item.id,tocId:item.id,variant:{title:'보편 지향 기도',text:record?.paragraphs.length?'[원문에는 공동체가 기도를 준비하라는 안내만 있고 실제 지향은 제공되지 않았습니다. 본당의 지향을 확인해 주세요.]':'[이 날짜의 원문에는 보편 지향 기도가 수록되어 있지 않습니다. 본당에서 준비한 지향을 확인해 주세요.]'},group:'보편 지향 기도 미수록'}];
 const notes=record.paragraphs.filter(p=>p.role==='guidance').map(p=>'[원문 지침] '+p.text.replace(/^<|>$/g,'')).join('\n');const result=[];
 petitions.forEach((petition,i)=>{result.push({key:i?item.id+'-petition-'+(i+1):item.id,tocId:item.id,variant:{title:'보편 지향 기도',text:(i===0&&notes?notes+'\n':'')+'○ '+petition.text+'\n'+petition.body.join('\n')},hideHeading:i>0,group:'보편 지향 기도 지향'});result.push({key:item.id+'-response-'+(i+1),tocId:item.id,variant:{title:'',text:'◎ 주님, 저희의 기도를 들어주소서.'},hideHeading:true,group:'보편 지향 기도 합송'});});
 const conclusion=dailySection('사제 마침 기도');const text=conclusion?.status==='verified'?conclusion.paragraphs.map(p=>p.text).join('\n'):null;
 result.push({key:item.id+'-conclusion',tocId:item.id,variant:{title:'사제 마침 기도',text:text||'[사제 마침 기도는 이 자료에 수록되어 있지 않습니다. 집전 사제의 기도에 따릅니다.]'},group:'보편 지향 기도 마침'});
 if(text)result.push({key:item.id+'-amen',tocId:item.id,variant:{title:'',text:'◎ 아멘.'},hideHeading:true,group:'보편 지향 기도 아멘'});return result;
}

function flowBlocks(partIndex) {
 const blocks=[];
 contents[partIndex].filter(isItemApplicable).forEach(item=>{
  const addPrayer=(suffix,title)=>blocks.push({key:`${item.id}-${suffix}`,tocId:item.id,prayerTitle:title});
  if(item.title==='영성체 예식 · 영성체 성가')addPrayer('agnus','하느님의 어린양');
  if(item.title==='참회 예식'){blocks.push({key:item.id,tocId:item.id,penitential:true,group:'참회 예식'});
  }else if(item.title==='인사'){
   variantCards(item.title).forEach((variant,index)=>blocks.push({key:index===0?item.id:`${item.id}-variant-${index+1}`,tocId:item.id,variant:{...variant,text:variant.text+(index===2?'\n◎ 또한 사제의 영과 함께.':''),title:item.title==='인사'?'인사':variant.title},hideHeading:item.title==='인사' && index>0,alternative:item.title==='인사' && index<2,group:item.title}));

  }else if(item.title==='보편 지향 기도'){
   universalPrayerBlocks(item).forEach(block=>blocks.push(block));
  }else if(item.title==='복음 환호송'){
   ['first','choir','last'].forEach((acclamationPart,i)=>blocks.push({key:i?`${item.id}-${acclamationPart}`:item.id,tocId:item.id,acclamationPart}));
  }else if(item.title==='파견'){
   dismissalChoices().forEach((variant,index)=>blocks.push({key:index?`${item.id}-variant-${index+1}`:item.id,tocId:item.id,variant,hideHeading:index>0,alternative:index<3,group:'파견'}));blocks.push({key:`${item.id}-response`,tocId:item.id,variant:{title:'',text:'◎ 하느님, 감사합니다.'},hideHeading:true,group:'파견 합송'});
  }else if(item.title==='감사기도 제2양식'){
   const text=ordinaryText(item.title==='영성체 예식 · 영성체 성가'?'영성체 예식 · 영성체 성가':item.title,find('mode').value);
   const first=text.split('[거룩하시도다 · 별도 카드 참조]');const preface=dailyText('감사송');if(preface){const opening=first[0].split('+ 거룩하신 아버지')[0];first[0]=opening+'+ '+preface;}else if(selectedRubrics()?.prefaceHints.length){const opening=first[0].split('+ 거룩하신 아버지')[0];first[0]=opening+'[원문 지침] '+selectedRubrics().prefaceHints.map(t=>t.replace(/^<|>$/g,'')).join(' / ')+'\n[선택 날짜 감사송 전문 미연결 · 집전 사제의 선택에 따릅니다.]';}
   const rest=(first[1]||'').split('[신앙의 신비여 · 별도 카드 참조]');
   blocks.push({key:item.id,tocId:item.id,item,displayText:first[0]});
   addPrayer('sanctus','거룩하시도다');
   blocks.push({key:`${item.id}-institution`,tocId:item.id,item,displayTitle:'감사기도 제2양식 · 성찬 제정',displayText:rest[0]});
   addPrayer('memorial','신앙의 신비여');
   blocks.push({key:`${item.id}-offering`,tocId:item.id,item,displayTitle:'감사기도 제2양식 · 기념과 봉헌',displayText:(rest[1]||'').replace(/\n◎ 아멘\.$/,'')});
   addPrayer('amen','아멘');
  }else blocks.push({key:item.id,tocId:item.id,item});
  if(item.title==='주님의 기도')addPrayer('doxology','주님의 기도 맺음 환호');
  
 });blocks.forEach((block,index)=>{const next=blocks[index+1];block.joinNext=Boolean(next&&block.tocId===next.tocId&&(next.hideHeading||next.acclamationPart==='choir'||next.acclamationPart==='last'));});return blocks;
}
function renderBlock(block) {
 let node;
 if(block.penitential)node=renderPenitential();
 else if(block.group==='보편 지향 기도 합송')node=renderIntercessionResponse();
 else if(block.acclamationPart)node=renderAlleluia(block.acclamationPart);
 else if(block.variant){
  node=document.createElement('section');node.className='reader__item';const h=document.createElement('h3');h.className='reader__item-title';h.textContent=block.variant.title;
  const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-choice-group',block.group);const p=document.createElement('p');p.className='reader__item-text';p.textContent=block.variant.text;card.append(p);if(!block.hideHeading)node.append(h);node.append(card);
 }else if(block.transition!==undefined){
  node=document.createElement('section');node.className='reader__item';const h=document.createElement('h3');h.textContent='다음 순서';
  const p=document.createElement('p');p.textContent=block.transition<parts.length?`“${parts[block.transition].title}”로 넘겨주세요.`:'미사 순서 안내가 끝났습니다.';node.append(h,p);
  if(block.transition<parts.length){const b=createReaderButton();b.type='button';b.textContent=parts[block.transition].title+'로 이동 →';b.onclick=()=>go(block.transition);node.append(b);}
 }else node=block.item?renderItem(block.item):renderPrayerFrame(block.prayerTitle,block.prayerTitle);
 node.id=block.key;node.tabIndex=-1;node.setAttribute('data-flow-key',block.key);node.setAttribute('data-section-id',block.tocId||block.key);if(block.joinNext)node.classList.add('reader__item--joined');
 if(block.displayText!==undefined)replaceLiturgyText(node,block.displayText);
 if(block.displayTitle){node.classList.add('reader__item--flow');const h=node.querySelector('h3');if(h)h.textContent=block.displayTitle;}
 if(block.fragmentText!==undefined)replaceLiturgyText(node,block.fragmentText,block.fragmentRole||'text');
 if(block.continued){const heading=node.querySelector('h3');if(heading)heading.textContent+=' (계속)';}
 const rubricTitle=block.item?.title||block.prayerTitle||block.variant?.title||(block.acclamationPart==='first'?'복음 환호송':null);
 const sourceNote=missalOrdinary.boundaryNotes[rubricTitle];
 if(sourceNote&&!block.continued&&!block.hideHeading&&!['강론','신앙 고백','영성체 후 기도'].includes(rubricTitle)){
  const card=node.querySelector('.reader__content-card');const p=document.createElement('p');p.className='reader__guidance';p.setAttribute('data-source-kind','missal-rubric');p.setAttribute('data-pdf-page',String(sourceNote.pdfPage));p.title=`경본 ${sourceNote.item}항 · PDF ${sourceNote.pdfPage}쪽`;p.textContent=sourceNote.text;if(card)card.prepend(p);else node.append(p);
 }
 decorateLiturgy(node);compactLongGuidance(node);if(block.group==='보편 지향 기도 지향'&&!block.hideHeading&&!block.continued)appendDailySource(node,'보편 지향 기도');
 if(block.item?.title==='강복'){const priest=Array.from(node.querySelectorAll('.reader__speech-card--priest')).find(card=>card.textContent.includes('성부와'));const guide=Array.from(node.querySelectorAll('.reader__guidance')).find(p=>p.textContent.includes('성호를 긋는다'));const body=priest?.querySelector('.reader__speech-body');if(body&&guide)body.append(guide);}
 if(block.group==='보편 지향 기도 지향' && !block.hideHeading && !block.continued){const h=node.querySelector('h3');const row=document.createElement('div');row.className='reader__item-heading';h.replaceWith(row);row.append(h,intercessionControls(block.key));}
 if(block.item?.title==='복음'){const lit=node.querySelector('.reader__liturgy');if(lit?.children[0]?.textContent.includes('주님께서 여러분과 함께') && lit.children[1]?.textContent.includes('또한 사제의 영과 함께')){const pair=document.createElement('div');pair.className='reader__dialogue';const priest=lit.children[0],assembly=lit.children[1];lit.insertBefore(pair,priest);pair.append(priest,assembly);}}
 if(['제1독서','제2독서','복음'].includes(block.item?.title)){const lit=node.querySelector('.reader__liturgy');if(lit){const children=Array.from(lit.children);children.forEach((child,i)=>{const next=children[i+1];if(child.textContent.includes('주님의 말씀입니다.') && next?.getAttribute('data-speech-role')==='assembly'){const pair=document.createElement('div');pair.className='reader__dialogue';lit.insertBefore(pair,child);pair.append(child,next);}});}}
 if(block.group==='인사' && block.variant.text.includes('◎')){const lit=node.querySelector('.reader__liturgy');if(lit && lit.children.length===2){const pair=document.createElement('div');pair.className='reader__dialogue';const children=Array.from(lit.children);lit.append(pair);pair.append(...children);}}
 if(block.item?.title==='감사기도 제2양식'){const lit=node.querySelector('.reader__liturgy');if(lit){const children=Array.from(lit.children);children.forEach((child,i)=>{const next=children[i+1];if(child.getAttribute('data-speech-role')==='priest' && next?.getAttribute('data-speech-role')==='assembly' && child.textContent.length<=80 && next.textContent.length<=80){const pair=document.createElement('div');pair.className='reader__dialogue';lit.insertBefore(pair,child);pair.append(child,next);}});}}
 if(block.item?.title==='제1독서'&&find('mode').value==='beginner'){const heading=node.querySelector('h3');if(heading){const row=document.createElement('div');row.className='reader__reading-heading';heading.replaceWith(row);const note=document.createElement('span');note.className='reader__reading-note';note.textContent='앉아서 말씀을 듣습니다.';row.append(heading,note);}}
 if(['제1독서','제2독서','복음'].includes(block.item?.title)){node.classList.add('reader__item--reading');node.querySelector('.reader__content-card')?.classList.add('reader__reading-content');const lit=node.querySelector('.reader__liturgy');lit?.classList.add('reader__reading-liturgy');Array.from(lit?.children||[]).filter(child=>child.getAttribute('data-speech-role')==='text').forEach(child=>{child.classList.add('reader__reading-body');const paragraphs=Array.from(child.querySelectorAll('.reader__speech-text'));child.replaceChildren();let paragraphBody=null;paragraphs.forEach(p=>{const match=p.textContent.match(/^(▥|✠|\d{1,3})\s+/);if(match||!paragraphBody){const row=document.createElement('div');row.className='reader__speech-row'+(match?'':' reader__speech-row--unmarked');paragraphBody=document.createElement('div');paragraphBody.className='reader__speech-body';if(match){const marker=document.createElement('span');marker.className='reader__speech-marker';marker.textContent=match[1];row.append(marker);p.textContent=p.textContent.slice(match[0].length);}row.append(paragraphBody);child.append(row);}paragraphBody.append(p);});child.setAttribute('tabindex','0');child.setAttribute('aria-label',block.item.title+' 본문 스크롤');});}
 if(['제1독서','제2독서','복음','감사기도 제2양식'].includes(block.item?.title)){node.querySelectorAll('.reader__dialogue').forEach(pair=>pair.classList.add('reader__dialogue--stacked'));}
 if(block.alternative){const card=node.querySelector('.reader__speech-card');if(card){card.classList.add('reader__speech-card--alternative');card.setAttribute('aria-label',block.variant.key+' · 다른 양식 선택 가능');const marker=document.createElement('span');marker.className='reader__alternative-marker';marker.textContent='〈또는〉';marker.setAttribute('aria-hidden','true');card.append(marker);}}
 node.classList.add('reader__item--flow');const h=node.querySelector('h3');if(h){let row=h.parentElement;if(row===node||!row.className.includes('heading')){row=document.createElement('div');row.className='reader__item-heading';h.replaceWith(row);row.append(h);}row.classList.add('reader__sticky-heading');}normalizeGuidance(node);applyComponentStyles(node);
 return node;
}
function paginateFlow(blocks,fits,split) {
 const pages=[];let current=[];
 const flush=()=>{if(current.length){pages.push({blocks:current,oversize:false});current=[];}};
 blocks.forEach(block=>{
  if(fits([...current,block])){current.push(block);return;}
  flush();
  if(fits([block])){current=[block];return;}
  const fragments=split(block);
  fragments.forEach(fragment=>{
   if(fits([...current,fragment]))current.push(fragment);
   else {flush();if(fits([fragment]))current=[fragment];else pages.push({blocks:[fragment],oversize:true});}
  });
 });flush();return pages;
}
function spreadForAnchor(pages,key) {
 const index=pages.findIndex(page=>page.blocks.some(block=>block.key===key));return index<0?0:Math.floor(index/2);
}
function sectionFlowKey(block){if(['보편 지향 기도 지향','보편 지향 기도 합송'].includes(block.group))return 'intercession-petitions';if(['보편 지향 기도 마침','보편 지향 기도 아멘'].includes(block.group))return 'intercession-conclusion';if(['예물 준비 기도','예물 기도'].includes(block.item?.title))return 'offertory-prayers';if(block.item?.title==='성호경'||block.group==='인사')return 'opening-sign-and-greeting';return block.prayerTitle?'prayer:'+block.prayerTitle:block.displayTitle?'section:'+block.displayTitle:block.tocId||block.key;}
function paginateSections(blocks,fits,split,offset=0){const groups=[];blocks.forEach(block=>{const key=sectionFlowKey(block);if(groups.at(-1)?.key===key)groups.at(-1).blocks.push(block);else groups.push({key,blocks:[block]});});const pages=[];groups.forEach(group=>{let section=(['intercession-petitions','intercession-conclusion','offertory-prayers','opening-sign-and-greeting'].includes(group.key)||group.blocks.every(block=>block.item?.title==='감사기도 제2양식'))?[{blocks:group.blocks,oversize:!fits(group.blocks)}]:paginateFlow(group.blocks,fits,split);if(section.length>2)section=[section[0],{blocks:section.slice(1).flatMap(page=>page.blocks),oversize:true}];if(section.length===2 && (offset+pages.length)%2===1)section=[{blocks:section.flatMap(page=>page.blocks),oversize:true}];pages.push(...section);});return pages;}
function readingPagePlan(blocks){if(blocks[0]?.item?.title==='제1독서' && blocks[1]?.item?.title==='화답송' && blocks[2]?.item?.title==='제2독서')return {leading:[{blocks:blocks.slice(0,2),oversize:false,reading:true},{blocks:blocks.slice(2,3),oversize:false,reading:true}],rest:blocks.slice(3)};return {leading:[],rest:blocks};}
function composePages() {
 const probe=document.createElement('article');probe.className='reader__page reader__page--measure';probe.setAttribute('aria-hidden','true');probe.inert=true;find('book').append(probe);
 const fits=blocks=>{probe.replaceChildren(...blocks.map(renderBlock));return probe.scrollHeight<=probe.clientHeight+1;};
 const split=block=>{
  if(block.penitential || ['신앙 고백','본기도','복음 환호송','복음'].includes(block.item?.title))return [block];
  const node=renderBlock(block);if(node.querySelector('.reader__prayer-option'))return [block];const paragraph=node.querySelector('.reader__liturgy');
  if(!paragraph || paragraph.__sourceText.length<2)return [block];
  const result=[];let remaining=paragraph.__sourceText,index=0,offset=0;
  while(remaining.length){
   let low=1,high=remaining.length,best=0;
   const key=index?`${block.key}-continue-${index}`:block.key;
   while(low<=high){const mid=Math.floor((low+high)/2);const fragment={...block,key,continued:index>0,fragmentRole:spokenRoleAt(paragraph.__sourceText,offset,paragraph.__initialRole),fragmentText:remaining.slice(0,mid)};if(fits([fragment])){best=mid;low=mid+1;}else high=mid-1;}
   if(!best)return [block];
   if(best<remaining.length){const newline=remaining.lastIndexOf('\n',best);const boundary=newline>best/2?newline:remaining.lastIndexOf(' ',best);if(boundary>best/2)best=boundary+1;}
   result.push({...block,key,continued:index>0,fragmentRole:spokenRoleAt(paragraph.__sourceText,offset,paragraph.__initialRole),fragmentText:remaining.slice(0,best)});remaining=remaining.slice(best);offset+=best;index++;
  }return result;
 };
 try{const plan=readingPagePlan(flowBlocks(part));return [...plan.leading,...paginateSections(plan.rest,fits,split,plan.leading.length)];}finally{probe.remove();}
}
{{READER_STATE}}
let readerDate=null,readerPart=0,readerAnchor=null,readerScrolls={},restoringScroll=false,readerSaveTimer=null;
function loadReaderDate(date,restoreControls=false){let state=null;try{state=readState(localStorage,date);}catch{}readerScrolls=state?.scrolls||{};position.fill(null);part=state?.part||0;currentAnchor=state?.anchor||contents[part][0].id;if(restoreControls&&state){find('mode').value=state.mode;find('slot').value=state.slot;}}
function scrollEntries(){const book=find('book');const list=Array.from(book.querySelectorAll('*'));const counts={};const result=list.map(node=>{const block=node.closest?.('[data-flow-key]');const page=node.classList?.contains('reader__page');if(!block&&!page)return null;const key=block?.getAttribute('data-flow-key')||Array.from(node.children||[]).find(n=>n.getAttribute?.('data-flow-key'))?.getAttribute('data-flow-key');if(!key)return null;const kind=page?'page':node.classList?.contains('reader__reading-body')?'reading':node.classList?.contains('reader__psalm-content')?'psalm':node.classList?.contains('reader__collect-scroll')?'collect':node.classList?.contains('reader__score-scroll')?'score':node.classList?.contains('reader__text-scroll')?'text':null;if(!kind)return null;const base=key+':'+kind;const index=counts[base]||0;counts[base]=index+1;return {node,key:base+':'+index};}).filter(Boolean);if(book.classList.contains('reader__book--continuous'))result.push({node:book,key:'continuous-all'});return result;}
function captureReaderScroll(){if(restoringScroll)return;for(const {node,key} of scrollEntries()){const max=node.scrollHeight-node.clientHeight;if(max>0)readerScrolls[key]=Math.max(0,Math.min(1,node.scrollTop/max));}}
function persistReader(){if(!readerDate||!readerAnchor)return;try{writeState(localStorage,{version:1,date:readerDate,part:readerPart,anchor:readerAnchor,mode:find('mode').value,slot:find('slot').value,scrolls:readerScrolls});localStorage.setItem('missa.reader.selected-date.v1',readerDate);}catch{}}
function restoreReaderScroll(){restoringScroll=true;for(const {node,key} of scrollEntries())if(Number.isFinite(readerScrolls[key]))node.scrollTop=readerScrolls[key]*Math.max(0,node.scrollHeight-node.clientHeight);restoringScroll=false;}
function readerScrolled(event){if(restoringScroll)return;if(viewerOrientation==='portrait'&&event.target===find('book')){const blocks=Array.from(find('book').querySelectorAll('[data-flow-key]'));const visible=blocks.find(node=>node.offsetTop+node.offsetHeight>find('book').scrollTop);if(visible){const nextPart=Number(visible.getAttribute('data-flow-part'));if(Number.isInteger(nextPart)&&nextPart!==part){part=nextPart;readerPart=part;find('part-title').textContent=parts[part].title;}currentAnchor=visible.getAttribute('data-flow-key');readerAnchor=currentAnchor;const block=layouts.flatMap(page=>page.blocks).find(b=>b.key===currentAnchor);if(block&&selectedItem!==block.tocId){selectedItem=block.tocId;renderToc();}}}const block=event.target.closest?.('[data-flow-key]');if(block){readerAnchor=block.getAttribute('data-flow-key');currentAnchor=readerAnchor;}captureReaderScroll();if(readerSaveTimer!==null)clearTimeout(readerSaveTimer);readerSaveTimer=setTimeout(()=>{readerSaveTimer=null;persistReader();},200);}

function render(options={}) {const previousReaderAnchor=readerAnchor;
 if(reflowFrame!==null){cancelAnimationFrame(reflowFrame);reflowFrame=null;}
 if(readerDate===find('date').value)captureReaderScroll();
 const book=find('book');if(book.clientWidth<2||book.clientHeight<2)return;
 let anchor=options.anchorKey||currentAnchor||contents[part][0].id;
 const continuous=viewerOrientation==='portrait';book.className='reader__book'+(continuous?' reader__book--continuous':'');layouts=continuous?[{blocks:parts.flatMap((_,index)=>flowBlocks(index).map(block=>({...block,flowPart:index}))),continuous:true}]:composePages();if(!layouts.length)return;if(options.edge==='last')anchor=layouts.at(-1).blocks[0].key;
 spread=spreadForAnchor(layouts,anchor);
 const visible=layouts.slice(spread*2,spread*2+2);
 const anchorBlock=layouts.flatMap(page=>page.blocks).find(block=>block.key===anchor)||visible[0].blocks[0];
 currentAnchor=anchorBlock.key;selectedItem=anchorBlock.tocId;position[part]=currentAnchor;
 const nodes=visible.map((layout,index)=>{
  const page=document.createElement('article');page.className=layout.continuous?'reader__page reader__page--continuous':layout.reading?'reader__page reader__page--reading':layout.oversize?'reader__page reader__page--oversize':'reader__page';if(layout.reading&&layout.blocks.some(block=>block.item?.title==='화답송'))page.classList.add('reader__page--reading-psalm');
  page.setAttribute('aria-label',layout.blank?'빈 페이지 · 다음 섹션은 다음 펼침에서 시작':`${parts[part].title} ${spread*2+index+1}쪽`);
  layout.blocks.forEach(block=>{const node=renderBlock(block);if(continuous)node.setAttribute('data-flow-part',String(block.flowPart));page.append(node);});if(!continuous){const heading=page.querySelector('.reader__sticky-heading');if(heading){heading.classList.add('reader__fixed-heading');heading.remove();}const scroll=document.createElement('div');scroll.className='reader__page-scroll';scroll.tabIndex=0;scroll.setAttribute('aria-label','본문 스크롤');scroll.append(...page.childNodes);page.classList.add('reader__page--fixed');if(heading)page.append(heading);page.append(scroll);}return page;
 });
 if(!continuous&&nodes.length===1){const blank=document.createElement('article');blank.className='reader__page';blank.setAttribute('aria-label','빈 페이지');nodes.push(blank);}
 book.replaceChildren(...nodes);book.querySelectorAll('.reader__page-scroll').forEach(scroll=>scroll.classList.toggle('is-overlay-scrollbar',scroll.offsetWidth===scroll.clientWidth));readerDate=find('date').value;readerPart=part;readerAnchor=currentAnchor;restoreReaderScroll();if(continuous&&(options.anchorKey&&options.anchorKey!==previousReaderAnchor||!Number.isFinite(readerScrolls['continuous-all']))){const target=Array.from(book.querySelectorAll('[data-flow-key]')).find(node=>node.getAttribute('data-flow-key')===currentAnchor);if(target)book.scrollTop=target.offsetTop;}persistReader();find('part-title').textContent=parts[part].title;
 
 find('part-prev').textContent=part?`← ${parts[part-1].title}`:'미사 시작';find('part-prev').disabled=part===0;
 find('part-next').textContent=part<parts.length-1?`${parts[part+1].title} →`:'미사 마침';find('part-next').disabled=part===parts.length-1;
 find('page-context').textContent=`${parts[part].title} · ${spread*2+1}–${Math.min(spread*2+2,layouts.length)}쪽 / 총 ${layouts.length}쪽`;
 const turn=pageTurnState(part,spread,layouts.length);find('page-prev').disabled=!turn.previous;find('page-next').disabled=!turn.next;find('page-next').setAttribute('data-next-part',String(turn.nextPart));const previousLabel=turnDestination(-1),nextLabel=turnDestination(1);find('page-prev').title=previousLabel;find('page-next').title=nextLabel;find('page-prev').textContent='← '+previousLabel;find('page-next').textContent=nextLabel+' →';find('page-prev').setAttribute('aria-label',previousLabel+'로 이동');find('page-next').setAttribute('aria-label',nextLabel+'로 이동');hintNextPart(turn.nextPart);if(continuous){find('page-context').textContent=parts[part].title+' · 세로 연속 보기';find('page-prev').disabled=part===0;find('page-next').disabled=part===parts.length-1;find('page-prev').textContent=part?'← '+parts[part-1].title:'미사 시작';find('page-next').textContent=part<parts.length-1?parts[part+1].title+' →':'미사 마침';find('page-prev').setAttribute('aria-label',find('page-prev').textContent);find('page-next').setAttribute('aria-label',find('page-next').textContent);find('page-prev').title=find('page-prev').textContent;find('page-next').title=find('page-next').textContent;hintNextPart(false);}renderToc();applyComponentStyles(document);
 if(pendingPrayerFocus){const request=pendingPrayerFocus;pendingPrayerFocus=null;const block=Array.from(book.querySelectorAll('[data-flow-key]')).find(node=>node.getAttribute('data-flow-key')===request.key);block?.querySelector(`[data-prayer-mode="${request.mode}"]`)?.focus({preventScroll:true});}
}
function scheduleReflow(anchorKey=currentAnchor) {
 if(reflowFrame!==null)cancelAnimationFrame(reflowFrame);
 reflowFrame=requestAnimationFrame(()=>{reflowFrame=null;render({anchorKey});});
}
function go(index){part=index;currentAnchor=position[index]||contents[index][0].id;render({anchorKey:currentAnchor});}
function flowBlockTitle(block,partIndex=part){const title=block.displayTitle||block.prayerTitle||block.variant?.title||block.item?.title||contents[partIndex].find(item=>item.id===block.tocId)?.title||parts[partIndex].title;return title+(block.acclamationPart==='last'?' · 합송':block.acclamationPart==='choir'?' · 성가대':block.continued?' (계속)':'');}
function turnDestination(direction){const target=layouts[(spread+direction)*2];if(target?.blocks.length)return flowBlockTitle(target.blocks[0]);const index=part+direction;if(index<0)return '미사 시작';if(index>=parts.length)return '미사 마침';const item=direction<0?contents[index].at(-1):contents[index][0];return parts[index].title+' · '+item.title;}
function pageTurnState(partIndex,spreadIndex,pageCount){const first=spreadIndex===0,last=(spreadIndex+1)*2>=pageCount;return {previous:!first||partIndex>0,next:!last||partIndex<parts.length-1,previousPart:first&&partIndex>0,nextPart:last&&partIndex<parts.length-1};}
let nextPartHint=null;
function hintNextPart(active){if(nextPartHint){nextPartHint.cancel();nextPartHint=null;}const button=find('page-next');if(active && button.animate && !globalThis.matchMedia?.('(prefers-reduced-motion: reduce)').matches){nextPartHint=button.animate([{outlineWidth:'0px',outlineStyle:'solid',outlineColor:'currentColor',outlineOffset:'0px'},{outlineWidth:'3px',outlineStyle:'solid',outlineColor:'currentColor',outlineOffset:'3px'},{outlineWidth:'0px',outlineStyle:'solid',outlineColor:'currentColor',outlineOffset:'0px'}],{duration:1400,iterations:3});}}
function turnSpread(direction){if(viewerOrientation==='portrait'){const next=part+direction;if(next>=0&&next<parts.length)go(next);return;}const page=layouts[(spread+direction)*2];if(page){render({anchorKey:page.blocks[0].key});return;}const target=part+direction;if(target<0||target>=parts.length)return;part=target;currentAnchor=null;selectedItem=null;render(direction<0?{edge:'last'}:{anchorKey:contents[part][0].id});}
function swipeDirection(dx,dy){return Math.abs(dx)>=64 && Math.abs(dx)>Math.abs(dy)*1.5?(dx<0?1:-1):0;}
function bindPageSwipe(book){let gesture=null;book.addEventListener('pointerdown',event=>{if(!event.isPrimary || event.button!==0 || event.target.closest('button,a,input,select,textarea,[contenteditable="true"]'))return;gesture={id:event.pointerId,x:event.clientX,y:event.clientY};});book.addEventListener('pointermove',event=>{if(!gesture||gesture.id!==event.pointerId)return;const dx=event.clientX-gesture.x,dy=event.clientY-gesture.y;if(Math.abs(dy)>16 && Math.abs(dy)>Math.abs(dx)){gesture=null;return;}if(Math.abs(dx)>16 && Math.abs(dx)>Math.abs(dy)*1.5 && event.cancelable)event.preventDefault();});book.addEventListener('pointerup',event=>{if(!gesture||gesture.id!==event.pointerId)return;const start=gesture;gesture=null;const direction=swipeDirection(event.clientX-start.x,event.clientY-start.y);if(direction)turnSpread(direction);});book.addEventListener('pointercancel',()=>gesture=null);book.addEventListener('pointerleave',()=>gesture=null);book.addEventListener('dragstart',event=>{if(event.target.tagName==='IMG')event.preventDefault();});}



let readerBodyFont='serif';
function applyReaderBodyFont(value,persist=true){
 if(!['serif','sans'].includes(value))value='serif';if(persist){captureReaderScroll();persistReader();}readerBodyFont=value;document.documentElement?.setAttribute('data-reader-font',value);let saved=true;
 if(persist){try{localStorage.setItem('missa.reader.body-font.v1',value);}catch{saved=false;}scheduleReflow(currentAnchor);}return saved;
}
const readerThemes=[['a','A · 부드러운 미색'],['b','B · 짙은 종이색'],['c','C · 편안한 다크']];
let readerTheme='a';
function applyReaderTheme(value,persist=true){
 if(!readerThemes.some(([key])=>key===value))value='a';readerTheme=value;document.documentElement?.setAttribute('data-reader-theme',value);
 if(persist){try{localStorage.setItem('missa.reader.appearance.v1',value);}catch{return false;}}return true;
}
let orientationPreference='auto';
let viewerOrientation=window.innerHeight>window.innerWidth?'portrait':'landscape';
function setViewerOrientation(value){
 if(!['auto','portrait','landscape'].includes(value))return;
 captureReaderScroll();persistReader();orientationPreference=value;viewerOrientation=value==='auto'?(window.innerHeight>window.innerWidth?'portrait':'landscape'):value;find('reader').setAttribute('data-orientation',viewerOrientation);
 find('viewport-status').textContent=value==='auto'?'':'뷰어 미리보기 · '+(value==='portrait'?'세로 768 × 1024':'가로 1024 × 768')+' · 좁은 창에서는 너비 축소';
 find('viewport-rotate').hidden=value==='auto';find('viewport-reset').hidden=value==='auto';
 find('viewport-rotate').textContent=value==='portrait'?'가로로 전환':'세로로 전환';
 if(typeof requestAnimationFrame==='function')scheduleReflow(currentAnchor);
}

function showPanel(which, trigger) {
 opener = trigger; const body = find('drawer-body'); body.replaceChildren(); find('drawer-title').textContent = titles[which];
 const text = value => { const p = document.createElement('p'); p.textContent = value; body.append(p); };
 if (which === 'hymn') { appendHymnEditor(body); }
 if (which === 'prayer') {
  appendMajorPrayerSources(body);
  text('기도문 본문과 본당별 기도문 성가·악보를 카드에 표시합니다. 교중미사 사진 악보를 임시로 배치했습니다. 본문은 사용자 인쇄물의 판독 초안이며 공식 원문 대조 전입니다.');
  ['성호경','자비송','대영광송','거룩하시도다','신앙의 신비여','아멘','주님의 기도','주님의 기도 맺음 환호','하느님의 어린양','성모송','영광송'].forEach(title=>body.append(renderPrayerFrame(title,title,title!=='성호경')));
 }
 if(which==='menu'){[['hymn','성가'],['prayer','주요 기도문'],['settings','보기 설정'],['info','안내']].forEach(([panel,label])=>{const b=createReaderButton();b.type='button';b.textContent=label;b.onclick=()=>showPanel(panel,trigger);body.append(b);});}
 if (which === 'settings') {
  const parishForm=document.createElement('form');parishForm.className='reader__field';
  const parishLabel=document.createElement('label');parishLabel.textContent='본당명';
  const parishInput=document.createElement('input');parishInput.type='text';parishInput.maxLength=40;parishInput.required=true;parishInput.value=selectedParishName();parishInput.setAttribute('aria-label','본당명');parishLabel.append(parishInput);
  const parishStatus=document.createElement('p');parishStatus.setAttribute('role','status');
  const parishSave=createReaderButton('본당명 저장');parishSave.type='submit';
  const parishReset=createReaderButton('기본 본당명 사용');
  parishForm.onsubmit=event=>{event.preventDefault();const name=parishInput.value.trim();if(!name){parishStatus.textContent='본당명을 입력해 주세요.';return;}try{localStorage.setItem('missa.parish.name.v1',name);find('parish-name').textContent=name;parishInput.value=name;parishStatus.textContent='본당명을 저장했습니다. 미사 일정은 기존 설정을 유지합니다.';}catch{parishStatus.textContent='저장하지 못했습니다. 브라우저 저장소를 확인해 주세요.';}};
  parishReset.onclick=()=>{try{localStorage.removeItem('missa.parish.name.v1');parishInput.value=selectedParishName();find('parish-name').textContent=selectedParishName();parishStatus.textContent='설정파일의 기본 본당명으로 되돌렸습니다.';}catch{parishStatus.textContent='기본 본당명으로 되돌리지 못했습니다.';}};
  parishForm.append(parishLabel,parishSave,parishReset,parishStatus);body.append(parishForm);

  text('뷰어 방향 미리보기로 화면을 가로·세로 크기로 바꿔 볼 수 있습니다. 세로 화면이 창보다 높으면 브라우저를 스크롤하세요. 실제 기기의 터치·브라우저 UI까지 재현하지는 않습니다.');
  const orientationGroup=document.createElement('div');orientationGroup.className='reader__row';orientationGroup.setAttribute('role','group');orientationGroup.setAttribute('aria-label','뷰어 방향 미리보기');
  [['landscape','가로 1024 × 768'],['portrait','세로 768 × 1024'],['auto','현재 화면에 맞춤']].forEach(([value,label])=>{const b=createReaderButton();b.type='button';b.textContent=label;b.setAttribute('aria-pressed',String(orientationPreference===value));b.onclick=()=>{find('drawer').close();setViewerOrientation(value);find('part-next').focus({preventScroll:true});};orientationGroup.append(b);});body.append(orientationGroup);
  const fontLabel=document.createElement('label');fontLabel.className='reader__field';fontLabel.textContent='본문 글꼴';const fontSelect=document.createElement('select');fontSelect.setAttribute('aria-label','본문 글꼴');[['serif','명조'],['sans','고딕']].forEach(([value,label])=>{const option=document.createElement('option');option.value=value;option.textContent=label;fontSelect.append(option);});fontSelect.value=readerBodyFont;const fontStatus=document.createElement('p');fontStatus.setAttribute('role','status');fontSelect.onchange=()=>{fontStatus.textContent=applyReaderBodyFont(fontSelect.value)?'본문 글꼴을 저장했습니다.':'현재 화면에 적용했습니다. 저장소 제한으로 새로고침 후 유지되지 않을 수 있습니다.';};fontLabel.append(fontSelect);body.append(fontLabel,fontStatus);text('본문 기본: 18px · 줄 간격 1.6 · 기본 여백. 제목·버튼·메뉴는 고딕입니다.');
  const theme=document.createElement('label');theme.className='reader__field';theme.textContent='배경·글자색';const select=document.createElement('select');select.setAttribute('aria-label','배경·글자색 테마');readerThemes.forEach(([value,label])=>{const option=document.createElement('option');option.value=value;option.textContent=label;select.append(option);});select.value=readerTheme;const themeStatus=document.createElement('p');themeStatus.setAttribute('role','status');select.onchange=()=>{const saved=applyReaderTheme(select.value);themeStatus.textContent=saved?'테마를 저장했습니다.':'이 화면에는 적용했습니다. 저장소 제한으로 새로고침 후에는 유지되지 않을 수 있습니다.';};theme.append(select);body.append(theme,themeStatus);
  const reloadButton=createReaderButton();reloadButton.type='button';reloadButton.textContent='앱 새로고침';reloadButton.setAttribute('data-js','app-reload');reloadButton.onclick=()=>window.location.reload();body.append(reloadButton);
 }
 if (which === 'info') {
  const tutorialButton=createReaderButton();tutorialButton.type='button';tutorialButton.textContent='기호와 사용법';tutorialButton.onclick=()=>{find('drawer').close();requestAnimationFrame(()=>showTutorial(trigger||find('part-next')));};body.append(tutorialButton);
  text('가로 두 페이지는 같은 예식의 연속 내용입니다. 아래 버튼으로 페이지를 넘기고, 위 버튼으로 이전·다음 예식에 이동합니다.');
  text('목차를 접으면 본문 폭이 넓어집니다. 긴 본문과 악보는 바깥 페이지에서 스크롤하며, 가로 보기의 섹션 제목은 상단에 고정됩니다.');
  text('선택 버튼은 은은한 와인 면과 굵은 글씨로, 합송은 짙은 와인 면으로 표시합니다. 저장 버튼은 종이 바탕과 와인 테두리로 구분합니다.');
  text('프로토타입의 편성·설정은 별도 테스트 공간에 저장합니다. 처음 실행할 때 기존 앱 값을 읽어오지만, 테스트 변경은 기존 편성과 설정을 덮어쓰지 않습니다.');
  text('날짜별 공식 본문은 일부만 연결되어 있습니다. 미연결 항목·검증 전 판독 초안·본당 최종 교정 전 악보의 상태는 자료 상태에서 확인하세요. 새로운 공식 문구를 생성하지 않았습니다.');
  text('보기 설정에서 미색·종이색·와인 다크, 본문 명조·고딕을 바꿀 수 있습니다. 기본은 가로 보기, 본문18px·줄 간격1.6입니다.');
  const refs=document.createElement('p');[['../docs/references/교중미사_통상문_텍스트_초안.md','텍스트 참조'],['../docs/references/교중미사_통상문_텍스트_초안.json','텍스트 데이터']].forEach(([url,name])=>{const a=document.createElement('a');a.href=encodeURI(url);a.target='_blank';a.rel='noopener noreferrer';a.textContent=name;refs.append(a,document.createTextNode(' '));});body.append(refs);
 }
 applyComponentStyles(find('drawer'));if(!find('drawer').open)find('drawer').showModal();
}

const tutorialKey='missa.reader.symbol-tutorial.v1';
const tutorialSteps=[
 ['◎ 합송','동그라미 두 개(◎)는 신자가 함께 바치는 부분입니다. 와인색 면과 굵은 글씨로 구분된 본문을 함께 바칩니다.'],
 ['+ 사제의 부분','십자가 모양(+) 표시는 사제가 바치는 부분입니다. 신자는 듣고, 이어지는 ◎ 합송에 참여합니다.'],
 ['안내와 선택 양식','안내 색으로 구분된 문장은 자세나 행동에 대한 설명입니다. 〈또는〉은 사제가 선택할 수 있는 다른 양식이 이어진다는 뜻입니다.'],
 ['페이지와 악보','본문은 아래 페이지 버튼으로 넘깁니다. 긴 악보와 신앙 고백은 바깥 페이지에서 스크롤합니다. 이 설명은 오른쪽 아래 안내에서 언제든 다시 볼 수 있습니다.']
];
let tutorialIndex=0,tutorialOpener=null,tutorialSeen=false;
function paintTutorial(){const step=tutorialSteps[tutorialIndex];find('tutorial-title').textContent=step[0];find('tutorial-step').textContent=`${tutorialIndex+1} / ${tutorialSteps.length}`;find('tutorial-copy').textContent=step[1];find('tutorial-prev').disabled=tutorialIndex===0;find('tutorial-next').textContent=tutorialIndex===tutorialSteps.length-1?'시작하기':'다음';}
function showTutorial(trigger=null){tutorialOpener=trigger;tutorialIndex=0;paintTutorial();find('tutorial').showModal();find('tutorial-next').focus();}
function hasSeenTutorial(){try{return localStorage.getItem(tutorialKey)==='done';}catch{return tutorialSeen;}}
function finishTutorial(){tutorialSeen=true;try{localStorage.setItem(tutorialKey,'done');}catch{}find('tutorial').close();}
function nextTutorial(){if(tutorialIndex===tutorialSteps.length-1)finishTutorial();else{tutorialIndex++;paintTutorial();}}

find('toc-toggle').onclick=function(){const workspace=find('book').closest('.reader__workspace');const collapsed=workspace.classList.toggle('is-toc-collapsed');this.setAttribute('aria-expanded',String(!collapsed));this.setAttribute('aria-label',collapsed?'목차 펼치기':'목차 접기');this.title=collapsed?'목차 펼치기':'목차 접기';const path=this.querySelector('path');path.setAttribute('d',collapsed?'M15 4v16m-4-12-3 4 3 4':'M15 4v16m-5-12 3 4-3 4');scheduleReflow(currentAnchor);};
find('header-menu').onclick=event=>showPanel('menu',event.currentTarget);
find('viewport-rotate').onclick=()=>setViewerOrientation(viewerOrientation==='portrait'?'landscape':'portrait');
find('viewport-reset').onclick=()=>{setViewerOrientation('auto');find('part-next').focus({preventScroll:true});};
bindPageSwipe(find('book'));
find('part-prev').onclick = () => go(Math.max(0,part-1));
find('part-next').onclick = () => go(Math.min(parts.length-1,part+1));
find('page-prev').onclick = () => turnSpread(-1);
find('page-next').onclick = () => turnSpread(1);
find('mode').onchange = render; find('slot').onchange = () => { setViewerOrientation(orientationPreference);context(); render(); };
find('date').onchange = () => {captureReaderScroll();persistReader();collectView=0;readerScrolls={};position.fill(null);part=0;spread=0;currentAnchor=contents[0][0].id;readerDate=null;context();render({anchorKey:currentAnchor});};
document.querySelectorAll('[data-panel]').forEach(button => button.onclick = () => showPanel(button.dataset.panel,button));
find('close').onclick = () => find('drawer').close();
find('drawer').addEventListener('close', () => { render(); const target = selectedItem && document.getElementById(selectedItem); if(opener?.isConnected)opener.focus({preventScroll:true});else if(target)target.focus({preventScroll:true}); });
let viewportReflowTimer=null;
function bookSizeKey(){const book=find('book');return `${book.clientWidth}|${book.clientHeight}`;}
let observedBookSize=bookSizeKey();
function scheduleViewportReflow(){
 if(viewportReflowTimer!==null)clearTimeout(viewportReflowTimer);
 viewportReflowTimer=setTimeout(()=>{
  viewportReflowTimer=null;const size=bookSizeKey();
  if(find('book').clientWidth<2||find('book').clientHeight<2||size===observedBookSize)return;
  observedBookSize=size;scheduleReflow();
 },150);
}
if(typeof ResizeObserver!=='undefined')new ResizeObserver(scheduleViewportReflow).observe(find('book'));
window.addEventListener('resize',()=>{if(orientationPreference==='auto'){const next=window.innerHeight>window.innerWidth?'portrait':'landscape';if(next!==viewerOrientation)setViewerOrientation('auto');}scheduleViewportReflow();});
document.fonts?.ready.then(()=>scheduleReflow());
find('tutorial-prev').onclick=()=>{tutorialIndex=Math.max(0,tutorialIndex-1);paintTutorial();};
find('tutorial-next').onclick=nextTutorial;
find('tutorial-later').onclick=()=>find('tutorial').close();
find('tutorial').addEventListener('close',()=>{const target=find('drawer').open?tutorialOpener:find('part-next');target?.focus();});
find('score-modal-close').onclick=()=>find('score-modal').close();
find('score-modal').addEventListener('close',()=>{find('score-modal-body').replaceChildren();const replacement=[...document.querySelectorAll('.reader__score-enlarge')].find(button=>button.getAttribute('data-score-path')===scoreModalOpener?.getAttribute('data-score-path'));(scoreModalOpener?.isConnected?scoreModalOpener:replacement||find('part-next'))?.focus();});
find('liturgical-season').onclick=event=>showSeasonModal(event.currentTarget);
find('season-help-close').onclick=()=>find('season-help-modal').close();
find('season-help-modal').addEventListener('close',()=>seasonHelpOpener?.focus());
find('season-modal-close').onclick=()=>find('season-modal').close();
find('season-modal').addEventListener('close',()=>find('liturgical-season').focus());
find('guidance-close').onclick=()=>find('guidance-dialog').close();
find('guidance-dialog').addEventListener('close',()=>{const block=Array.from(find('book').querySelectorAll('[data-flow-key]')).find(node=>node.getAttribute('data-flow-key')===guidanceAnchor);const target=guidanceOpener?.isConnected?guidanceOpener:block?.querySelector('.reader__guidance-toggle');(target||find('part-next')).focus();});
find('source-dialog-close').onclick=()=>find('source-dialog').close();
find('source-dialog').addEventListener('close',()=>{(sourceDialogOpener?.isConnected?sourceDialogOpener:find('part-next'))?.focus();});
try{applyReaderBodyFont(localStorage.getItem('missa.reader.body-font.v1')||'serif',false);}catch{applyReaderBodyFont('serif',false);}
try{applyReaderTheme(new URLSearchParams(location.search).get('reviewTheme')||localStorage.getItem('missa.reader.appearance.v1')||'a',false);}catch{applyReaderTheme('a',false);}
const urlDateParam=new URLSearchParams(location.search).get('date');
if(/^\d{4}-\d{2}-\d{2}$/.test(urlDateParam||'')){
 find('date').value=urlDateParam;
}else{
 const today=new Date();find('date').value=[today.getFullYear(),String(today.getMonth()+1).padStart(2,'0'),String(today.getDate()).padStart(2,'0')].join('-');
}
loadReaderDate(find('date').value,true);
find('book').addEventListener('scroll',readerScrolled,true);
window.addEventListener('pagehide',()=>{captureReaderScroll();persistReader();});
setViewerOrientation(orientationPreference);context(); render();
if(!hasSeenTutorial())showTutorial();

function appendHymnBackupControls(body){
 const section=document.createElement('section'),heading=document.createElement('h3');heading.textContent='성가 편성 백업·복원';section.append(heading);
 const status=document.createElement('p');status.setAttribute('role','status');
 const out=createReaderButton();out.type='button';out.textContent='전체 편성 백업';out.onclick=()=>{try{const backup=exportHymnBackup(localStorage);const url=URL.createObjectURL(new Blob([JSON.stringify(backup,null,2)],{type:'application/json'}));const link=document.createElement('a');link.href=url;link.download='missa-hymns-backup.json';section.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);status.textContent=backup.records.length+'개 날짜·회차 편성을 백업했습니다.';}catch(error){status.textContent='백업 실패 · '+error.message;}};
 const label=document.createElement('label');label.textContent='복원할 JSON 백업 파일';const input=document.createElement('input');input.type='file';input.accept='.json,application/json';input.setAttribute('aria-label','복원할 JSON 백업 파일');label.append(input);
 const preview=document.createElement('div');let selection=0;input.onchange=async()=>{const token=++selection;preview.replaceChildren();try{const file=input.files[0];if(!file)return;if(file.size>2000000)throw Error('백업 파일이 너무 큽니다.');const backup=parseHymnBackup(await file.text());if(token!==selection)return;const note=document.createElement('p');note.textContent=backup.records.length+'개 편성 · 같은 날짜·회차는 아래 내용으로 바꾸며, 파일에 없는 편성은 유지합니다.';preview.append(note);for(const record of backup.records){const p=document.createElement('p');p.textContent=record.date+' · '+record.slot;preview.append(p);const before=readHymnSet(localStorage,record.date,record.slot);for(const [title,role] of Object.entries(hymnTitles)){const line=document.createElement('p');line.textContent=title+' · '+(before[role].join(', ')||'미등록')+' → '+(record.hymns[role].join(', ')||'미등록');preview.append(line);}}
 const apply=createReaderButton('', 'primary');apply.type='button';apply.textContent='확인한 편성 복원';apply.disabled=!backup.records.length;apply.onclick=()=>{try{const count=restoreHymnBackup(localStorage,backup);preview.replaceChildren();input.value='';showPanel('hymn',opener);const result=document.createElement('p');result.setAttribute('role','status');result.textContent=count+'개 편성을 복원했습니다.';find('drawer-body').append(result);scheduleReflow(currentAnchor);}catch(error){status.textContent=error.message;}};const cancel=createReaderButton();cancel.type='button';cancel.textContent='복원 취소';cancel.onclick=()=>{selection++;preview.replaceChildren();input.value='';status.textContent='복원을 취소했습니다. 기존 편성을 유지합니다.';};preview.append(apply,cancel);status.textContent='변경 내용을 확인해 주세요.';}catch(error){if(token===selection)status.textContent='파일을 읽지 못했습니다 · '+error.message;}};
 section.append(out,label,status,preview);body.append(section);
}

if(parent!==window){window.addEventListener('message',event=>{if(event.source!==parent)return;
if(event.data?.type==='missa-set-date'&&/^\d{4}-\d{2}-\d{2}$/.test(event.data.date)){
 find('date').value=event.data.date;
 find('date').dispatchEvent(new Event('change'));
 return;
}if(event.data?.type==='missa-system-inspection'){document.documentElement.setAttribute('data-review-frames',String(event.data.enabled===true));return;}if(event.data?.type!=='missa-system-preview')return;document.documentElement.setAttribute('data-review-frames',String(event.data.inspection===true));const {view,theme}=event.data;if(['a','b','c'].includes(theme))applyReaderTheme(theme,false);document.querySelectorAll('dialog[open]').forEach(d=>d.close());if(view==='entrance'){go(0);render({anchorKey:contents[0][0].id});}else if(view==='eucharist'){go(2);render({anchorKey:contents[2][0].id});}else if(view==='settings'){showPanel('settings');}else if(view==='hymn'){go(0);showPanel('hymn');}else if(view==='creed'){go(1);render({anchorKey:contents[1].find(x=>x.title==='신앙 고백').id});}else if(view==='opening'){go(0);render({anchorKey:contents[0].find(x=>x.title==='참회 예식').id});}else {go(1);render({anchorKey:contents[1][0].id});}});parent.postMessage({type:'missa-system-ready'},'*');}
