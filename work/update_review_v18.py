from pathlib import Path
import re,json
p=Path('review/02-ia-v17.html');s=p.read_text(encoding='utf-8').replace('검토 v17','검토 v18')
# Preserve existing item IDs while adding independently navigable subsections.
s=s.replace("[['예물 준비 · 봉헌 성가',0],['예물 기도',0],['감사 기도',1]", "[['봉헌 성가',0],['예물 기도',0],['감사기도 제2양식',1]",1)
marker='const frameSpecs = '
pos=s.index('\n',s.index(marker));s=s[:pos]+"\ncontents[2].splice(1,0,{id:'part-2-item-0-preparation',title:'예물 준비 기도',page:0});\ncontents[2].splice(contents[2].findIndex(x=>x.id==='part-2-item-5')+1,0,{id:'part-2-item-5-hymn',title:'영성체 성가',page:3});\nframeSpecs['봉헌 성가']={kind:'hymn',source:'hymnSet'};frameSpecs['예물 준비 기도']={kind:'prayer',source:'ordinary'};frameSpecs['감사기도 제2양식']=frameSpecs['감사 기도'];frameSpecs['영성체 성가']={kind:'hymn',source:'hymnSet'};\n"+s[pos:]
s=s.replace("<strong class=\"reader__season-badge\" data-js=\"liturgical-season\"></strong>","<button type=\"button\" class=\"reader__season-badge\" data-js=\"liturgical-season\" aria-haspopup=\"dialog\" aria-controls=\"season-dialog\"></button>",1)
s=s.replace('--draft-marker-width:', '--draft-modal-width: 90rem; --draft-modal-height: 92dvh; --draft-marker-width:',1)
s=s.replace(' .reader__score-photo {', ''' .reader__score-modal { width: min(96vw, var(--draft-modal-width)); height: var(--draft-modal-height); padding: var(--draft-padding); }
 .reader__score-modal[open] { display: grid; grid-template-rows: auto minmax(0, 1fr); gap: var(--draft-gap); }
 .reader__score-modal-body { min-block-size: 0; overflow: auto; }
 .reader__pdf-object { display: block; width: 100%; height: 100%; min-height: 60dvh; }
 .reader__modal-heading { display: flex; justify-content: space-between; align-items: center; gap: var(--draft-gap); }
 .reader__season-period { border: 1px solid; padding: var(--draft-content-inset); margin-block: var(--draft-item-gap); }
 .reader__season-period[aria-current="true"] { border-width: var(--draft-response-border); }
 .reader__score-photo {''',1)
dialogs='''<dialog class="reader__score-modal" data-js="score-modal" aria-labelledby="score-modal-title"><div class="reader__modal-heading"><h2 id="score-modal-title" data-js="score-modal-title">악보 크게 보기</h2><button type="button" data-js="score-modal-close">닫기</button></div><div class="reader__score-modal-body" data-js="score-modal-body"></div></dialog>
<dialog class="reader__tutorial" id="season-dialog" data-js="season-modal" aria-labelledby="season-modal-title"><div class="reader__modal-heading"><h2 id="season-modal-title" data-js="season-modal-title">전례 시기</h2><button type="button" data-js="season-modal-close">닫기</button></div><div data-js="season-modal-body"></div></dialog>
'''
s=s.replace('<script>',dialogs+'<script>',1)
helpers=r'''
const seasonCalendar2026={year:2026,sourceUrl:'https://missa.cbck.or.kr/Liturgy',periods:[
 {key:'ordinary',title:'연중 시기',start:'2026-01-12',end:'2026-02-17',description:'1월 12일 ~ 2월 17일'},
 {key:'lent',title:'사순 시기',start:'2026-02-18',end:'2026-04-01',description:'2월 18일 재의 수요일 ~ 4월 2일 주님 만찬 미사 전'},
 {key:'easter',title:'부활 시기',start:'2026-04-05',end:'2026-05-24',description:'4월 5일 주님 부활 대축일 ~ 5월 24일 성령 강림 대축일 (부활 성야부터)'},
 {key:'ordinary',title:'연중 시기',start:'2026-05-25',end:'2026-11-28',description:'5월 25일 ~ 11월 28일'}
]};
function currentSeason(date=find('date').value){return seasonCalendar2026.periods.find(x=>date>=x.start && date<=x.end) || null;}
const parishMemorialResponses={
 ordinary:{label:'연중 시기',text:'◎ 주님께서 오실 때까지 주님의 죽음을 전하며 부활을 선포하나이다.',crop:[2050,540,1800,760]},
 lent:{label:'사순 시기',text:'◎ 주님께서 오실 때까지 이 빵을 먹고 이 잔을 마실 적마다 주님의 죽음을 전하나이다.',crop:[2050,1330,1800,710]},
 easter:{label:'부활 시기',text:'◎ 십자가와 부활로 저희를 구원하신 주님, 길이 영광 받으소서.',crop:[2050,2100,1800,700]}
};
function memorialResponse(){const season=currentSeason();return season?parishMemorialResponses[season.key]:null;}
let scoreModalOpener=null,seasonModalOpener=null;
function enlargeScoreButton(asset){const b=document.createElement('button');b.type='button';b.textContent='악보 크게 보기';b.setAttribute('aria-haspopup','dialog');b.onclick=()=>showScoreModal([asset],asset.title,b);return b;}
function showScoreModal(assets,title,trigger){
 scoreModalOpener=trigger;const body=find('score-modal-body');body.replaceChildren();find('score-modal-title').textContent=title+' · 악보 크게 보기';
 assets.forEach(asset=>{
  if(asset.kind==='engraved'){
   const pdf=document.createElement('object');pdf.className='reader__pdf-object';pdf.type='application/pdf';pdf.data=encodeURI(asset.path)+'#view=FitH';pdf.setAttribute('aria-label',asset.title+' PDF 악보');
   const fallback=document.createElement('a');fallback.href=encodeURI(asset.path);fallback.target='_blank';fallback.rel='noopener noreferrer';fallback.textContent='악보 파일 보기';pdf.append(fallback);body.append(pdf);
  }else body.append(renderPhoto(asset,true));
 });find('score-modal').showModal();find('score-modal-close').focus();
}
function showSeasonModal(trigger){
 seasonModalOpener=trigger;const body=find('season-modal-body');body.replaceChildren();const year=find('date').value.slice(0,4);find('season-modal-title').textContent=year+'년 전례 시기';
 if(year==='2026'){
  const current=currentSeason();seasonCalendar2026.periods.forEach(period=>{const card=document.createElement('section');card.className='reader__season-period';if(current===period)card.setAttribute('aria-current','true');const h=document.createElement('h3');h.textContent=period.title+(current===period?' · 현재 선택한 시기':'');const p=document.createElement('p');p.textContent=period.description;card.append(h,p);body.append(card);});
  const note=document.createElement('p');note.textContent='성주간 목요일 저녁부터 부활 성야 전까지는 파스카 성삼일입니다. 대림·성탄과 해당 경계의 상세 미사 구분은 후속 전례력 연결 대상입니다.';body.append(note);
  const source=document.createElement('a');source.href=seasonCalendar2026.sourceUrl;source.target='_blank';source.rel='noopener noreferrer';source.textContent='2026년 전례력 자료';body.append(source);
 }else{const p=document.createElement('p');p.textContent='선택한 연도의 전례 시기 자료 연결 전입니다.';body.append(p);}
 find('season-modal').showModal();find('season-modal-close').focus();
}
function renderMockTextCard(title,source){
 const section=document.createElement('section');section.className='reader__item';const h=document.createElement('h3');h.className='reader__item-title';h.textContent=title;
 const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source',source);const label=document.createElement('p');label.textContent=source==='parish-bulletin-mock'?'주보 공지 · mock · 신부님 안내':'매일미사 본문 · mock';const p=document.createElement('p');p.textContent=frameMock;card.append(label,p);section.append(h,card);
 if(title!=='공지 사항')section.append(liturgyNode('◎ 아멘.'));return section;
}
function dismissalChoices(){return referenceText('파견').split('\n').filter(line=>line.startsWith('+')).map((text,i)=>({key:'dismissal-'+i,title:'파견',text}));}
'''
s=s.replace('const frameMock=',helpers+'\nconst frameMock=',1)
s=s.replace("find('liturgical-season').textContent=day?day.season:'시기 미확인';", "find('liturgical-season').textContent=currentSeason()?.title || (day?day.season:'시기 미확인');",1)
s=s.replace(" if(key==='자비송')", " if(key==='신앙의 신비여'){const response=memorialResponse();return '+ 신앙의 신비여!\\n'+(response?response.text:'[선택 날짜의 시기 자료 연결 전]');}\n if(key==='감사기도 제2양식')key='감사 기도';\n if(key==='자비송')",1)
# Remove only the editorial labels requested; preserve genuine participation instructions.
s=s.replace("const text=keys.map(name=>", "let text=keys.map(name=>",1)
s=s.replace(" return mode==='regular'?text.split", " if(key==='감사 기도')text=text.split('\\n').filter(line=>!line.startsWith('[자료 안내] 인쇄본에 감사기도') && line!=='[감사송 대화]' && line!=='[인쇄본 수록 감사송 · 선택 미확정]').join('\\n');\n return mode==='regular'?text.split",1)
s=s.replace("function scoreAssets(prayerId) { return", "function scoreAssets(prayerId) { if(prayerId==='신앙의 신비여'){const response=memorialResponse();return find('slot').value==='main' && response?(temporaryPrincipalScores[prayerId]||[]).map(asset=>({...asset,crop:response.crop,title:'신앙의 신비여 · '+response.label})):[];}return",1)
start=s.index('function renderPhoto(asset)');end=s.index('function renderPrayerFrame',start)
s=s[:start]+r'''
function renderPhoto(asset,enlarged=false){
 const figure=document.createElement('figure');figure.className='reader__score';figure.setAttribute('data-score-kind',asset.kind==='engraved'?'reengraved':asset.kind==='mock'?'mock':'photo');
 const caption=document.createElement('figcaption');caption.textContent=(asset.kind==='engraved'?'교중미사 재조판 · ':asset.kind==='mock'?'악보 목데이터 · ':'교중미사 임시 악보 · ')+asset.title+' ';if(!enlarged)caption.append(enlargeScoreButton(asset));figure.append(caption);
 if(asset.kind==='engraved'||asset.kind==='mock'){
  const preview=document.createElement('img');preview.className='reader__score-photo';preview.src=encodeURI(asset.preview||asset.path);preview.alt=asset.title+(asset.kind==='mock'?' · 악보 목데이터':' · PDF와 동일한 조판');figure.append(preview);
 }else{
  const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('class','reader__score-photo');svg.setAttribute('role','img');svg.setAttribute('aria-label',asset.title+' · 사용자 제공 사진');
  const quarter=Math.abs(asset.rotation)===90;const width=quarter?asset.height:asset.width;const height=quarter?asset.width:asset.height;svg.setAttribute('viewBox',asset.crop?asset.crop.join(' '):`0 0 ${width} ${height}`);
  const image=document.createElementNS('http://www.w3.org/2000/svg','image');image.setAttribute('href',encodeURI(asset.path));image.setAttribute('width',String(asset.width));image.setAttribute('height',String(asset.height));if(asset.rotation===-90)image.setAttribute('transform',`translate(0 ${asset.width}) rotate(-90)`);if(asset.rotation===180)image.setAttribute('transform',`translate(${asset.width} ${asset.height}) rotate(180)`);svg.append(image);figure.append(svg);
 }return figure;
}
''' +s[end:]
# One reusable full-page hymn mock, including modal launch.
s=s.replace('function renderEntranceScore(){','function renderHymnScore(title){',1).replace("title.textContent='입당 성가';row.append(title);", "title.textContent=headingTitle;row.append(title);",1)
s=s.replace("function renderHymnScore(title){\n", "function renderHymnScore(headingTitle){\n",1)
s=s.replace("scroll.setAttribute('aria-label','입당 성가 악보 목데이터');", "scroll.setAttribute('aria-label',headingTitle+' 악보 목데이터');",1)
s=s.replace("const preview=document.createElement('img');preview.className='reader__score-photo';preview.src='../docs/mock/entrance-score.svg';preview.alt='입당 성가 악보 배치용 목데이터';scroll.append(preview);", "scroll.append(renderPhoto({kind:'mock',title:headingTitle,path:'../docs/mock/entrance-score.svg'}));",1)
s=s.replace("if(item.title==='입당 성가')return renderEntranceScore();", "if(['입당 성가','봉헌 성가','영성체 성가','파견 성가'].includes(item.title))return renderHymnScore(item.title);\n if(['예물 기도','영성체 후 기도'].includes(item.title))return renderMockTextCard(item.title,'cbck-daily-mock');\n if(item.title==='공지 사항')return renderMockTextCard(item.title,'parish-bulletin-mock');\n if(item.title==='예물 준비 기도'){const node=renderMockTextCard(item.title,'ordinary');node.replaceChildren();const h=document.createElement('h3');h.className='reader__item-title';h.textContent=item.title;node.append(h,liturgyNode(referenceText('예물 준비 · 봉헌 성가').split('\\n').filter(line=>!line.startsWith('[자료 안내]')).join('\\n')));return node;}",1)
s=s.replace("ordinaryText(item.title,find('mode').value)", "ordinaryText(item.title==='영성체 예식 · 영성체 성가'?'영성체 예식 · 영성체 성가':item.title,find('mode').value)")
# Remove communion hymn placeholder; the separate hymn section now owns it.
s=s.replace(" if(key==='감사 기도')text=", " if(key==='영성체 예식 · 영성체 성가')text=text.split('\\n').filter(line=>!line.startsWith('[자료에 오늘 영성체송')).join('\\n');\n if(key==='감사 기도')text=",1)
s=s.replace("}else if(item.title==='감사 기도'){", "}else if(item.title==='파견'){\n   dismissalChoices().forEach((variant,index)=>blocks.push({key:index?`${item.id}-variant-${index+1}`:item.id,tocId:item.id,variant,hideHeading:index>0,alternative:index<3,group:'파견'}));blocks.push({key:`${item.id}-response`,tocId:item.id,variant:{title:'',text:'◎ 하느님 감사합니다.'},hideHeading:true,group:'파견 합송'});\n  }else if(item.title==='감사기도 제2양식'){",1)
s=s.replace("displayTitle:'감사 기도 · 성찬 제정'", "displayTitle:'감사기도 제2양식 · 성찬 제정'").replace("displayTitle:'감사 기도 · 기념과 봉헌'", "displayTitle:'감사기도 제2양식 · 기념과 봉헌'")
# Modal cleanup and focus restoration. A reader reflow may have replaced the trigger.
s=s.replace("context(); render();\nif(!hasSeenTutorial())", "find('score-modal-close').onclick=()=>find('score-modal').close();\nfind('score-modal').addEventListener('close',()=>{find('score-modal-body').replaceChildren();(scoreModalOpener?.isConnected?scoreModalOpener:find('part-next'))?.focus();});\nfind('liturgical-season').onclick=event=>showSeasonModal(event.currentTarget);\nfind('season-modal-close').onclick=()=>find('season-modal').close();\nfind('season-modal').addEventListener('close',()=>find('liturgical-season').focus());\ncontext(); render();\nif(!hasSeenTutorial())",1)
s=s.replace('<option value="youth">주일 저녁 젊은이 미사</option>','<option value="youth">저녁미사</option>')
s=s.replace('id="slot" data-js="slot"','id="slot" class="reader__session-select" data-js="slot"')
s=s.replace(' .reader__score-photo {',' .reader__session-select { width: max-content; }\n .reader__score-photo {',1)
registry=json.loads(Path('docs/교중미사악보/reengraved/registry.json').read_text(encoding='utf-8'))
for assets in registry.values():
 for asset in assets:
  assert (Path('review')/asset['path']).is_file() and (Path('review')/asset['preview']).is_file()
s=re.sub(r'const reengravedPrincipalScores = .*?;\n','const reengravedPrincipalScores = '+json.dumps(registry,ensure_ascii=False)+';\n',s,count=1)
Path('review/02-ia-v18.html').write_text(s,encoding='utf-8',newline='\r\n')
Path('work/review-ia-v18-check.js').write_text(re.search(r'<script>(.*?)</script>',s,re.S).group(1),encoding='utf-8')
Path('docs/references/season-policy-2026.json').write_text(json.dumps({'sourceUrl':'https://missa.cbck.or.kr/Liturgy','scope':'2026-only-review','dates':{'baptism':'2026-01-11','ashWednesday':'2026-02-18','easter':'2026-04-05','pentecost':'2026-05-24','adventFirstSunday':'2026-11-29'},'memorialMapping':'user-provided-parish-booklet-and-request; not a universal mandatory mapping','eucharisticPrayer':'II, explicitly confirmed by user'},ensure_ascii=False,indent=2),encoding='utf-8')
