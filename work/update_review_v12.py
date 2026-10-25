from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[1]
html=(root/'review/02-ia-v11.html').read_text(encoding='utf-8').replace('검토 v11','검토 v12')
reference=json.loads((root/'docs/references/교중미사_통상문_텍스트_초안.json').read_text(encoding='utf-8'))
match=re.search(r'const localOrdinaryReference = .*?;\nfunction ordinaryText',html)
html=html[:match.start()]+('const localOrdinaryReference = '+json.dumps(reference,ensure_ascii=False)+';\nfunction ordinaryText')+html[match.end():]
helpers='''
const frameMock='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.';
let creedView='nicene',kyrieView='ordinary';
function referenceText(key){return localOrdinaryReference.records.find(x=>x.key===key)?.text || '';}
function variantCards(key){
 const text=referenceText(key);
 if(key==='인사')return text.split(/\\[(?:또는 )?선택지 [123]\\]/).slice(1).map((text,i)=>({key:`greeting-${i+1}`,title:`인사 · 선택지 ${i+1}`,text:text.trim()}));
 if(key==='참회 예식'){
  const parts=text.split(/\\[(?:또는 )?선택지 [12] ·[^\\]]*\\]/).slice(1);
  return parts.map((text,i)=>({key:`penitential-${i+1}`,title:`참회 예식 · 선택지 ${i+1}`,text:i===0?text.trim():text.split('+ 진심으로')[0].trim()+'\\n[프레임 안내] 호칭과 응답은 다음 자비송 카드의 “참회 호칭 포함” 표시에서 확인합니다. 실제 양식은 자동 선택하지 않습니다.'}));
 }return [];
}
function kyrieText(){
 if(kyrieView==='ordinary')return referenceText('자비송');
 const text=referenceText('참회 예식');const index=text.indexOf('+ 진심으로');return index>=0?text.slice(index):'[참회 호칭 자료 미등록]';
}
function creedVariants(){
 const text=referenceText('신앙 고백');
 const nicene=text.split(/\\[니케아[^\\]]*\\]/)[1]?.split('[또는 사도 신경]')[0]?.trim() || '';
 const apostles=text.split('[또는 사도 신경]')[1]?.trim() || '';
 return [{key:'nicene',title:'니케아 콘스탄티노플 신경',text:nicene},{key:'apostles',title:'사도 신경',text:apostles}];
}
function readingFrameText(title){
 if(title==='보편 지향 기도')return '[매일미사 연결용 본문 · mock]\\n'+frameMock;
 if(title==='복음')return '+ 주님께서 여러분과 함께.\\n◎ 또한 사제의 영과 함께.\\n+ (          )가(이) 전한 거룩한 복음입니다.\\n[안내] 이마와 입술과 가슴에 십자 표시를 합니다.\\n◎ 주님, 영광 받으소서.\\n[매일미사 복음 본문 · mock]\\n'+frameMock+'\\n+ 주님의 말씀입니다.\\n◎ 그리스도님 찬미합니다.';
 return (title==='제1독서'?'[안내] 앉아서 말씀을 듣습니다.\\n':'')+'[매일미사 독서 본문 · mock]\\n'+frameMock+'\\n◆ [독서자] 주님의 말씀입니다.\\n◎ 하느님, 감사합니다.';
}
'''
html=html.replace("function ordinaryText(key, mode='beginner') {", helpers+"\nfunction ordinaryText(key, mode='beginner') {\n if(key==='자비송')return kyrieText();\n if(key==='보편 지향 기도 응답')return '◎ 주님, 저희의 기도를 들어주소서.';")
# Source regions crop the viewport only; all original photo files remain intact.
regions='''
temporaryPrincipalScores['대영광송']=temporaryPrincipalScores['대영광송'].flatMap((asset,index)=>[
 {...asset,title:`대영광송 ${index*2+1}쪽`,crop:[0,0,2000,3000]},
 {...asset,title:`대영광송 ${index*2+2}쪽`,crop:[2000,0,2000,3000]}
]);
temporaryPrincipalScores['거룩하시도다']=temporaryPrincipalScores['거룩하시도다'].map(asset=>({...asset,crop:[0,0,2000,3000],title:'거룩하시도다'}));
temporaryPrincipalScores['신앙의 신비여']=temporaryPrincipalScores['신앙의 신비여'].map(asset=>({...asset,crop:[2000,0,2000,3000],title:'신앙의 신비여'}));
'''
html=html.replace('function scoreAssets(prayerId)',regions+"\nfunction scoreAssets(prayerId)")
html=html.replace("return find('slot').value === 'main' ?", "return (prayerId==='자비송' && kyrieView==='invocations') ? [] : find('slot').value === 'main' ?")
html=html.replace("svg.setAttribute('viewBox',`0 0 ${width} ${height}`);", "svg.setAttribute('viewBox',asset.crop?asset.crop.join(' '):`0 0 ${width} ${height}`);")
html=html.replace("const parishPrayerPresentation = Object.create(null);", "const parishPrayerPresentation = Object.create(null);\nparishPrayerPresentation['보편 지향 기도 응답']='chant';")
# Keep Gloria's printed guidance outside the card even when displaying the score.
needle='if(scoreSlot)headingRow.append(group);frame.append(headingRow,card);'
replacement='''if(scoreSlot)headingRow.append(group);frame.append(headingRow,card);
 let printedGuide=null;
 if(prayerId==='대영광송'){
  printedGuide=document.createElement('p');printedGuide.className='reader__item-text';printedGuide.textContent=referenceText('대영광송').split('\\n')[0].replace('[안내]','인쇄본 안내:');frame.insertBefore(printedGuide,card);
 }
 if(prayerId==='자비송'){
  const variants=document.createElement('div');variants.className='reader__prayer-option';variants.setAttribute('role','group');variants.setAttribute('aria-label','자비송 양식 표시');headingRow.append(variants);
  [['ordinary','일반 자비송'],['invocations','참회 호칭 포함']].forEach(([value,label])=>{const button=document.createElement('button');button.type='button';button.textContent=label;button.className='reader__prayer-button';button.setAttribute('aria-pressed',String(kyrieView===value));button.onclick=()=>{kyrieView=value;scheduleReflow(frame.getAttribute('data-flow-key'));};variants.append(button);});
 }'''
assert needle in html
html=html.replace(needle,replacement)
html=html.replace("frame.className=fullScorePage?'reader__item reader__item--score':'reader__item';", "frame.className=fullScorePage?'reader__item reader__item--score':'reader__item';\n  if(fullScorePage && printedGuide)frame.className+=' reader__item--guided-score';")
html=html.replace("p.textContent=ordinaryText(prayerId,find('mode').value)", "p.textContent=ordinaryText(prayerId,find('mode').value)")
# The creed has two actual cards, one visible at a time; it never splits across pages.
creed='''
function renderCreed(){
 const frame=document.createElement('section');frame.className='reader__item reader__item--score';
 const row=document.createElement('div');row.className='reader__item-heading';
 const h=document.createElement('h3');h.className='reader__item-title';h.textContent='신앙 고백';row.append(h);
 const group=document.createElement('div');group.className='reader__prayer-option';group.setAttribute('role','group');group.setAttribute('aria-label','신앙 고백 양식 표시');row.append(group);frame.append(row);
 const cards=[];const buttons=[];
 creedVariants().forEach(variant=>{
  const card=document.createElement('div');card.className='reader__content-card reader__content-card--score reader__creed-panel';card.setAttribute('data-variant',variant.key);
  const scroll=document.createElement('div');scroll.className='reader__text-scroll';scroll.tabIndex=0;scroll.setAttribute('role','region');scroll.setAttribute('aria-label',variant.title+' · 카드 내부 스크롤');
  const note=document.createElement('p');note.textContent='양식 표시 미리보기 · 실제 미사 양식 자동 선택 아님';
  const p=document.createElement('p');p.className='reader__item-text';p.textContent=variant.text;scroll.append(note,p);card.append(scroll);frame.append(card);cards.push([variant.key,card]);
  const b=document.createElement('button');b.type='button';b.className='reader__prayer-button';b.textContent=variant.title;b.setAttribute('data-creed-view',variant.key);b.onclick=()=>{creedView=variant.key;sync();};group.append(b);buttons.push([variant.key,b]);
 });
 function sync(){cards.forEach(([key,card])=>card.hidden=key!==creedView);buttons.forEach(([key,b])=>b.setAttribute('aria-pressed',String(key===creedView)));}
 sync();return frame;
}
'''
html=html.replace('function renderItem(item) {',creed+'\nfunction renderItem(item) {')
html=html.replace(" const spec=frameSpecs[item.title];", " const spec=frameSpecs[item.title];\n if(item.title==='신앙 고백')return renderCreed();\n if(item.title==='복음 환호송')return renderPrayerFrame('복음 환호송 · 알렐루야','복음 환호송',true);")
# Modify selected frames only: source text is retained separately in the reference files.
old="if(spec.kind==='choice'){const p=document.createElement('p');p.className='reader__item-text';p.textContent=ordinaryText(item.title,find('mode').value);section.append(p);}"
new="""if(['제1독서','제2독서','복음','보편 지향 기도'].includes(item.title)){
   const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source','cbck-daily-mock');const p=document.createElement('p');p.className='reader__item-text';p.textContent=readingFrameText(item.title);card.append(p);section.append(card);
  }else if(item.title==='화답송'){
   const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source','parish-bulletin-score');const p=document.createElement('p');p.textContent='주보 화답송 악보 표시 영역 · 악보 미등록';const note=document.createElement('p');note.textContent='주보 악보를 연결하면 이 카드 안에 표시합니다.';card.append(p,note);section.append(card);
  }else if(item.title==='본기도'){
   const card=document.createElement('div');card.className='reader__content-card';const p=document.createElement('p');p.className='reader__item-text';p.textContent='+ 기도합시다.\\n[안내] 잠깐 침묵하며 기도한 뒤, 사제가 바치는 오늘의 본기도를 듣습니다. 본문이 연결되기 전에는 사제의 기도를 따라 참여합니다.\\n◎ 아멘.';card.append(p);section.append(card);
  }else if(spec.kind==='choice'){const p=document.createElement('p');p.className='reader__item-text';p.textContent=ordinaryText(item.title,find('mode').value);section.append(p);}"""
assert old in html
html=html.replace(old,new)
# Render independent alternative cards and transition callouts as pageable blocks.
needle=" const node=block.item?renderItem(block.item):renderPrayerFrame(block.prayerTitle,block.prayerTitle);"
replacement=""" let node;
 if(block.variant){
  node=document.createElement('section');node.className='reader__item';const h=document.createElement('h3');h.className='reader__item-title';h.textContent=block.variant.title;
  const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-choice-group',block.group);const p=document.createElement('p');p.className='reader__item-text';p.textContent=block.variant.text;card.append(p);node.append(h,card);
 }else if(block.transition!==undefined){
  node=document.createElement('section');node.className='reader__item';const h=document.createElement('h3');h.textContent='다음 순서';
  const p=document.createElement('p');p.textContent=block.transition<parts.length?`“${parts[block.transition].title}”로 넘겨주세요.`:'미사 순서 안내가 끝났습니다.';node.append(h,p);
  if(block.transition<parts.length){const b=document.createElement('button');b.type='button';b.textContent=parts[block.transition].title+'로 이동 →';b.onclick=()=>go(block.transition);node.append(b);}
 }else node=block.item?renderItem(block.item):renderPrayerFrame(block.prayerTitle,block.prayerTitle);"""
assert needle in html
html=html.replace(needle,replacement)
html=html.replace("  if(item.title==='감사 기도'){", "  if(item.title==='인사' || item.title==='참회 예식'){\n   variantCards(item.title).forEach((variant,index)=>blocks.push({key:index===0?item.id:`${item.id}-variant-${index+1}`,tocId:item.id,variant,group:item.title}));\n  }else if(item.title==='감사 기도'){")
html=html.replace("  if(item.title==='주님의 기도')addPrayer('doxology','주님의 기도 맺음 환호');", "  if(item.title==='주님의 기도')addPrayer('doxology','주님의 기도 맺음 환호');\n  if(item.title==='보편 지향 기도')addPrayer('response','보편 지향 기도 응답');")
html=html.replace(' });return blocks;\n}\nfunction renderBlock', " });blocks.push({key:`part-${partIndex}-transition`,tocId:contents[partIndex].at(-1).id,transition:partIndex+1});return blocks;\n}\nfunction renderBlock")
# The full-height creed is deliberately indivisible; its own card scrolls.
html=html.replace("  const node=renderBlock(block);const paragraph=node.querySelector('.reader__item-text');", "  if(block.item?.title==='신앙 고백')return [block];\n  const node=renderBlock(block);const paragraph=node.querySelector('.reader__item-text');")
html=html.replace(' .reader__score-scroll {', ' .reader__creed-panel[hidden] { display: none; }\n .reader__text-scroll { min-block-size: 0; flex: 1; overflow: auto; overscroll-behavior: contain; }\n .reader__item--score.reader__item--guided-score { grid-template-rows: auto auto minmax(0, 1fr); }\n .reader__score-scroll {')
html=html.replace("  text('테마와 글자 크기는今回", "  text('테마와 글자 크기는今回")
html=html.replace("  text('테마와 글자 크기는 이번 정보 구조 단계에서 확정하지 않습니다.", "  text('v12: 인사 3개·참회 2개 카드를 분리하고 참회 호칭을 자비송 카드로 통합했습니다. 신앙 고백은 두 양식 버튼과 카드 내부 스크롤을 사용합니다. 독서·복음·보편 지향 기도는 매일미사 연결용 mock, 화답송은 주보 악보 미등록 프레임입니다. 대영광송 사진은 인쇄면 한 쪽씩 나누어 세로로 표시하며 원본 파일은 수정하지 않았습니다.');\n  text('테마와 글자 크기는 이번 정보 구조 단계에서 확정하지 않습니다.")
with (root/'review/02-ia-v12.html').open('w',encoding='utf-8',newline='\r\n') as f:f.write(html)
(root/'work/review-ia-v12-check.js').write_text(re.search(r'<script>(.*?)</script>',html,re.S).group(1),encoding='utf-8')
print('Created v12 variants, integrated Kyrie, daily/bulletin slots, scrollable creed, score page regions, transition cues')
