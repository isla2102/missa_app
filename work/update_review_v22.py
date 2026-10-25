from pathlib import Path
import json,hashlib,shutil
p=Path('docs/교중미사악보/reengraved/registry.json');shutil.copy2(p,'scratch/registry.before-v22.json');r=json.loads(p.read_text(encoding='utf-8'));r['하느님의 어린양']=[{'kind':'engraved','title':'하느님의 어린양','path':'../docs/교중미사악보/reengraved/agnus.pdf','preview':'../docs/교중미사악보/reengraved/agnus.svg','scope':'principal','sourceKey':'하느님의 어린양','status':'새 사진 대조 · 1·2절 반복을 펼쳐 표기 · 본당 최종 교정 전'}];p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
s=Path('review/02-ia-v21.html').read_text(encoding='utf-8').replace('검토 v21','검토 v22')
import re
s=re.sub(r'const reengravedPrincipalScores = .*?;',lambda m:'const reengravedPrincipalScores = '+json.dumps(r,ensure_ascii=False)+';',s,count=1)
s=s.replace("text.split('+ 진심으로')[0].trim()+'\\n[프레임 안내] 호칭과 응답은 다음 자비송 카드의 “참회 호칭 포함” 표시에서 확인합니다. 실제 양식은 자동 선택하지 않습니다.'","text.split('+ 진심으로')[0].trim()")
s=s.replace("const label=document.createElement('p');label.textContent=day?'오늘의 본기도 · 매일미사 확인 자료':'오늘의 본기도 · 매일미사 연결 영역 (mock)';card.append(label);", "if(!day){const label=document.createElement('p');label.textContent='선택 날짜 본문 연결 예정';card.append(label);}")
s=s.replace("const note=document.createElement('p');note.className='reader__guidance';note.textContent='안내 · 두 수록 본문의 표시 전환이며, 실제 미사에서 사용할 양식은 사제의 기도에 따릅니다.';card.append(note);",'')
s=s.replace("if(item.title==='공지 사항')", "if(item.title==='강론'){const node=document.createElement('section');node.className='reader__item';const h=document.createElement('h3');h.className='reader__item-title';h.textContent='강론';const card=document.createElement('div');card.className='reader__content-card';const p=document.createElement('p');p.textContent='자리에 앉아 신부님의 강론을 듣습니다. 오늘 들은 말씀을 우리 삶에서 어떻게 실천할지 마음에 새겨 보세요.';card.append(p);node.append(h,card);return node;}\n if(item.title==='공지 사항')",1)
# All enlarge controls are compact overlays on the score figure, which supplies containing block.
s=s.replace("b.textContent='악보 크게 보기';b.setAttribute", "b.textContent='악보 크게 보기';b.className='reader__score-enlarge';b.setAttribute",1)
s=s.replace(' .reader__score { margin: var(--draft-toc-gap) 0 0; }',' .reader__score { position: relative; margin: var(--draft-toc-gap) 0 0; }\n .reader__score-enlarge { position: absolute; inset-block-start: var(--draft-toc-gap); inset-inline-end: var(--draft-toc-gap); z-index: var(--draft-score-action-z); font-size: var(--draft-score-action-font); padding: var(--draft-score-action-padding); min-block-size: var(--draft-score-action-hit); }')
s=s.replace('@layer tokens {','@layer tokens {\n :root { --draft-score-action-z: 2; --draft-score-action-font: 0.75rem; --draft-score-action-padding: 0.25rem; --draft-score-action-hit: 1.5rem; }',1)
# Reuse the confirmed official remote image family; errors replace score with a clear source fallback.
pos=s.index('function renderHymnScore(');end=s.index('\nfunction renderItem(',pos)
s=s[:pos]+'''const hymnAssignments={};
function hymnAssignmentKey(title){return find('date').value+'|'+find('slot').value+'|'+title;}
function hymnScoreAsset(number,title){return {kind:'remote',title:'가톨릭성가 '+number+'번 · '+title,path:'https://maria.catholic.or.kr/sungga/Files/img/2012/201204'+String(number).padStart(4,'0')+'.jpg'};}
function renderHymnScore(headingTitle){
 const section=document.createElement('section');section.className='reader__item reader__item--score';
 const row=document.createElement('div');row.className='reader__item-heading';const title=document.createElement('h3');title.className='reader__item-title';title.textContent=headingTitle;row.append(title);
 const form=document.createElement('form');form.className='reader__prayer-option';
 const label=document.createElement('label');const id='hymn-number-'+({'입당 성가':'entrance','봉헌 성가':'offertory','영성체 성가':'communion','파견 성가':'recessional'})[headingTitle];label.htmlFor=id;label.textContent='성가 번호';const input=document.createElement('input');input.id=id;input.type='number';input.min='1';input.max='528';input.step='1';input.required=true;input.setAttribute('aria-label',headingTitle+' 성가 번호');input.value=hymnAssignments[hymnAssignmentKey(headingTitle)]||'';
 const submit=document.createElement('button');submit.type='submit';submit.textContent='악보 보기';form.append(label,input,submit);
 const card=document.createElement('div');card.className='reader__content-card reader__content-card--score';card.setAttribute('data-content-source','goodnews-monophonic-score');
 const scroll=document.createElement('div');scroll.className='reader__score-scroll';scroll.setAttribute('tabindex','0');scroll.setAttribute('role','region');scroll.setAttribute('aria-label',headingTitle+' 악보');
 const status=document.createElement('p');status.setAttribute('aria-live','polite');
 const fill=()=>{scroll.replaceChildren();const number=hymnAssignments[hymnAssignmentKey(headingTitle)];if(number){scroll.append(renderPhoto(hymnScoreAsset(number,headingTitle)));status.textContent='가톨릭성가 '+number+'번';}else status.textContent='성가 번호를 입력해 주세요.';};
 form.onsubmit=event=>{event.preventDefault();const n=Number(input.value);if(!Number.isInteger(n)||n<1||n>528){status.textContent='1부터 528 사이의 성가 번호를 입력해 주세요.';return;}hymnAssignments[hymnAssignmentKey(headingTitle)]=n;fill();};
 card.append(status,scroll);section.append(row,form,card);fill();return section;
}
function renderIntercessionResponse(){
 const node=document.createElement('section');node.className='reader__item';node.setAttribute('data-session-presentation',find('slot').value==='main'?'chant-pending-score':'recite');
 node.append(liturgyNode('◎ 주님, 저희의 기도를 들어주소서.'));
 if(find('slot').value==='main'){const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source','parish-response-score-pending');const p=document.createElement('p');p.textContent='합송 악보 · 본당 선율 자료 연결 예정';card.append(p);node.append(card);}return node;
}
'''+s[end:]
s=s.replace("if(asset.kind==='engraved'||asset.kind==='mock'){", "if(asset.kind==='engraved'||asset.kind==='mock'||asset.kind==='remote'){")
s=s.replace("asset.kind==='mock'?'악보 목데이터 · ':'교중미사 임시 악보 · '","asset.kind==='mock'?'악보 목데이터 · ':asset.kind==='remote'?'':'교중미사 임시 악보 · '")
s=s.replace("preview.alt=asset.title+(asset.kind==='mock'?' · 악보 목데이터':' · PDF와 동일한 조판');figure.append(preview);", "preview.alt=asset.title+(asset.kind==='mock'?' · 악보 목데이터':asset.kind==='remote'?' · 굿뉴스 단성 악보':' · PDF와 동일한 조판');if(asset.kind==='remote'){preview.onload=()=>{if(!enlarged)scheduleReflow(currentAnchor);};preview.onerror=()=>{preview.remove();const p=document.createElement('p');p.textContent='악보를 불러오지 못했습니다. 번호와 인터넷 연결을 확인해 주세요.';figure.append(p);};}figure.append(preview);")
s=s.replace("if(block.acclamationPart)node=", "if(block.group==='보편 지향 기도 합송')node=renderIntercessionResponse();\n else if(block.acclamationPart)node=")
Path('review/02-ia-v22.html').write_text(s,encoding='utf-8',newline='\r\n')
Path('work/review-ia-v22-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
