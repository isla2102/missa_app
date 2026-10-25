from pathlib import Path
import json,re
out=Path('docs/references/daily-missa-20261018.json')
data={'date':'2026-10-18','title':'연중 제29주일','observance':'민족들의 복음화를 위한 미사(전교 주일)','season':'연중 시기','sourceUrl':'https://missa.cbck.or.kr/DailyMissa/20261018','status':'verified-page-snapshot-not-live-api','collectVariants':[
'하느님,\n모든 사람이 진리를 깨달아 구원되기를 바라시니\n수확할 밭에 일꾼들을 많이 보내시어\n모든 이에게 복음을 전하게 하시고\n하느님의 백성이 생명의 말씀을 듣고 성사로 힘을 얻어\n구원과 사랑의 길을 걷게 하소서.\n성부와 성령과 함께 천주로서\n영원히 살아 계시며 다스리시는 성자\n우리 주 예수 그리스도를 통하여 비나이다.',
'하느님,\n참빛이신 성자를 이 세상에 보내셨으니\n약속하신 성령을 내리시어\n사람들 마음속에 언제나 진리의 씨앗을 심고\n신앙의 꽃을 피우게 하시며\n모든 이가 세례로 다시 태어나 새 생명을 얻고\n하느님 나라에서 한 백성을 이루게 하소서.\n성부와 성령과 함께 천주로서\n영원히 살아 계시며 다스리시는 성자\n우리 주 예수 그리스도를 통하여 비나이다.']}
out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
s=Path('review/02-ia-v13.html').read_text(encoding='utf-8').replace('검토 v13','검토 v14')
s=s.replace('data-js="date"><label','data-js="date"><span data-js="liturgical-day" aria-live="polite"></span><strong class="reader__season-badge" data-js="liturgical-season"></strong><label',1)
s=s.replace(' .reader__score-photo {',' .reader__item--collect { block-size: calc(100cqh - (2 * var(--draft-padding)) - 2px); display: grid; grid-template-rows: auto auto minmax(0, 1fr) auto; gap: var(--draft-item-gap); }\n .reader__collect-scroll { min-block-size: 0; overflow: auto; overscroll-behavior: contain; }\n .reader__season-badge { border: 2px solid; padding: var(--draft-toc-gap) var(--draft-content-inset); }\n .reader__score-photo {',1)
helpers='const dailyMissaSnapshot = '+json.dumps(data,ensure_ascii=False)+';\n'+r'''
function selectedDailyData(){return find('date').value===dailyMissaSnapshot.date?dailyMissaSnapshot:null;}
function updateLiturgicalHeading(){
 const day=selectedDailyData();find('liturgical-day').textContent=day?day.title+' · 전교 주일':'전례일 미연동';find('liturgical-season').textContent=day?day.season:'시기 미확인';
}
function renderCollect(){
 const section=document.createElement('section');section.className='reader__item reader__item--collect';
 const h=document.createElement('h3');h.className='reader__item-title';h.textContent='본기도';section.append(h);
 section.append(liturgyNode('+ 기도합시다.\n[안내] 모두 잠깐 침묵하며 기도합니다.'));
 const day=selectedDailyData();const card=document.createElement('div');card.className='reader__content-card reader__collect-scroll';card.setAttribute('tabindex','0');card.setAttribute('aria-label','매일미사 본기도 본문');card.setAttribute('data-content-source','cbck-daily-collect');
 const label=document.createElement('p');label.textContent=day?'오늘의 본기도 · 매일미사 확인 자료':'오늘의 본기도 · 매일미사 연결 영역 (mock)';card.append(label);
 const body=document.createElement('p');body.className='reader__item-text';
 if(day){
  const group=document.createElement('div');group.className='reader__prayer-option';group.setAttribute('role','group');group.setAttribute('aria-label','수록 본기도 표시');card.append(group);
  const buttons=[];const show=index=>{body.textContent=day.collectVariants[index];buttons.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));scheduleReflow(section.getAttribute('data-flow-key'));};
  day.collectVariants.forEach((text,i)=>{const b=document.createElement('button');b.type='button';b.textContent=`수록 본문 ${i+1}`;b.setAttribute('aria-pressed',String(i===collectView));b.onclick=()=>{collectView=i;show(i);};buttons.push(b);group.append(b);});
  body.textContent=day.collectVariants[collectView];
  const note=document.createElement('p');note.className='reader__guidance';note.textContent='안내 · 두 수록 본문의 표시 전환이며, 실제 미사에서 사용할 양식은 사제의 기도에 따릅니다.';card.append(note);
 }else body.textContent=frameMock;
 card.append(body);
 if(day){const source=document.createElement('a');source.href=day.sourceUrl;source.target='_blank';source.rel='noopener noreferrer';source.textContent='매일미사 출처 · 2026-10-18 (저장본, 실시간 연동 아님)';card.append(source);}
 section.append(card,liturgyNode('◎ 아멘.'));return section;
}
let collectView=0;
'''
s=s.replace('const frameMock=',helpers+'\nconst frameMock=',1)
s=s.replace(" if(item.title==='신앙 고백')return renderCreed();"," if(item.title==='본기도')return renderCollect();\n if(item.title==='신앙 고백')return renderCreed();",1)
# Keep source body in its own daily card, rather than treating it as a liturgical dialogue.
s=s.replace("const source=p.textContent;if(!source)return;", "const source=p.textContent;if(!source || p.parentElement?.getAttribute('data-content-source')==='cbck-daily-collect')return;",1)
s=s.replace("function context() { find('context')", "function context() { updateLiturgicalHeading();find('context')",1)
s=s.replace("find('date').onchange = () => { context(); find('context').textContent += ' · 선택 날짜의 공식 전례는 미확인'; };", "find('date').onchange = () => { collectView=0;context();render(); };")
s=s.replace("if(block.item?.title==='신앙 고백')return [block];","if(['신앙 고백','본기도'].includes(block.item?.title))return [block];")
Path('review/02-ia-v14.html').write_text(s,encoding='utf-8',newline='\r\n')
Path('work/review-ia-v14-check.js').write_text(re.search(r'<script>(.*?)</script>',s,re.S).group(1),encoding='utf-8')
