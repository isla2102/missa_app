from pathlib import Path
import json,re

root=Path(__file__).resolve().parents[1]
reference=json.loads((root/'docs/references/교중미사_통상문_텍스트_초안.json').read_text(encoding='utf-8'))
html=(root/'review/02-ia-v10.html').read_text(encoding='utf-8').replace('검토 v10','검토 v11')
old=re.search(r"const mockParagraph = .*?;\n",html).group(0)
data='const localOrdinaryReference = '+json.dumps(reference,ensure_ascii=False)+';\n'
data+='''function ordinaryText(key, mode='beginner') {
 const keys=key==='거룩하시도다 · 신앙의 신비여'?['거룩하시도다','신앙의 신비여']:[key];
 const text=keys.map(name=>localOrdinaryReference.records.find(record=>record.key===name)?.text || '[제공 통상문 자료에 이 본문 없음]').join('\\n\\n');
 return mode==='regular'?text.split('\\n').filter(line=>!line.startsWith('[안내]')).join('\\n'):text;
}
'''
html=html.replace(old,data)
html=html.replace('function scoreAssets(prayerId)', "temporaryPrincipalScores['거룩하시도다']=temporaryPrincipalScores['거룩하시도다 · 신앙의 신비여'];\ntemporaryPrincipalScores['신앙의 신비여']=temporaryPrincipalScores['거룩하시도다 · 신앙의 신비여'];\nfunction scoreAssets(prayerId)")
html=html.replace("p.lang='la';p.textContent=mockParagraph", "p.lang='ko';p.textContent=ordinaryText(prayerId,find('mode').value)",1)
html=html.replace("p.textContent=spec.guide;", "p.textContent=ordinaryText(item.title,find('mode').value);")
html=html.replace("p.lang='la';p.textContent=mockParagraph", "p.lang='ko';p.textContent=ordinaryText(item.title,find('mode').value)")
assert 'mockParagraph' not in html
html=html.replace('.reader__item-text { margin-block: 0; }', '.reader__item-text { margin-block: 0; white-space: pre-line; }')
html=html.replace(' .reader__score-scroll { block-size: min(var(--draft-score-scroll-max), 40cqh); overflow: auto; overscroll-behavior: contain; }', ''' .reader__score-scroll { block-size: auto; min-block-size: 0; flex: 1; overflow: auto; overscroll-behavior: contain; }
 .reader__item--score { block-size: calc(100cqh - (2 * var(--draft-padding)) - 2px); min-block-size: 0; display: grid; grid-template-rows: auto minmax(0, 1fr); gap: var(--draft-toc-gap); }
 .reader__content-card--score { min-block-size: 0; display: flex; flex-direction: column; }''')
html=html.replace('--draft-score-scroll-max: 14rem; ','')
start=html.index('function flowBlocks(partIndex) {')
end=html.index('function renderBlock(block)',start)
html=html[:start]+'''function flowBlocks(partIndex) {
 const blocks=[];
 contents[partIndex].forEach(item=>{
  const addPrayer=(suffix,title)=>blocks.push({key:`${item.id}-${suffix}`,tocId:item.id,prayerTitle:title});
  if(item.title==='영성체 예식 · 영성체 성가')addPrayer('agnus','하느님의 어린양');
  if(item.title==='감사 기도'){
   const text=ordinaryText(item.title,find('mode').value);
   const first=text.split('[거룩하시도다 · 별도 카드 참조]');
   const rest=(first[1]||'').split('[신앙의 신비여 · 별도 카드 참조]');
   blocks.push({key:item.id,tocId:item.id,item,displayText:first[0]});
   addPrayer('sanctus','거룩하시도다');
   blocks.push({key:`${item.id}-institution`,tocId:item.id,item,displayTitle:'감사 기도 · 성찬 제정',displayText:rest[0]});
   addPrayer('memorial','신앙의 신비여');
   blocks.push({key:`${item.id}-offering`,tocId:item.id,item,displayTitle:'감사 기도 · 기념과 봉헌',displayText:(rest[1]||'').replace(/\\n◎ 아멘\\.$/,'')});
   addPrayer('amen','아멘');
  }else blocks.push({key:item.id,tocId:item.id,item});
  if(item.title==='주님의 기도')addPrayer('doxology','주님의 기도 맺음 환호');
 });return blocks;
}
''' + html[end:]
html=html.replace(" node.id=block.key;node.tabIndex=-1;node.setAttribute('data-flow-key',block.key);", " node.id=block.key;node.tabIndex=-1;node.setAttribute('data-flow-key',block.key);\n if(block.displayText!==undefined){const p=node.querySelector('.reader__item-text');if(p)p.textContent=block.displayText;}\n if(block.displayTitle){const h=node.querySelector('h3');if(h)h.textContent=block.displayTitle;}")
needle="const mode=parishPrayerPresentation[prayerId] || (assets.length?'chant':'recite');"
assert needle in html
html=html.replace(needle,needle+'''
  const fullScorePage=mode==='chant' && assets.length>0;
  frame.className=fullScorePage?'reader__item reader__item--score':'reader__item';
  card.className=fullScorePage?'reader__content-card reader__content-card--score':'reader__content-card';''')
html=html.replace('MOCK 본문(Lorem ipsum) · 공식 자료 미연동', '통상문 사진 판독 초안 · 공식 대조 전 · 날짜별 고유문 미연동')
html=html.replace('모든 라틴어 본문은 Lorem ipsum mock입니다.', '본문은 사용자 제공 인쇄물에서 판독한 검증 전 텍스트입니다. 선택지는 자동 확정하지 않습니다.')
html=html.replace('본문은 mock이며 실제 본당 편성 확정 자료가 아닙니다.', '본문은 사용자 인쇄물의 판독 초안이며 공식 원문 대조 전입니다.')
html=html.replace('본문은 Lorem ipsum mock이며 사진 악보는 사용자가 제공한 임시 교중미사 자료입니다.', '본문은 검증 전 판독 초안이며 사진 악보는 사용자가 제공한 임시 교중미사 자료입니다.')
html=html.replace("['성호경','자비송','대영광송','거룩하시도다 · 신앙의 신비여','아멘'", "['성호경','자비송','대영광송','거룩하시도다','신앙의 신비여','아멘'")
html=html.replace("text('공식 전례력·본문은 미연동입니다.", "text('공식 전례력과 날짜별 고유문은 미연동입니다. 통상문은 사용자 제공 인쇄물의 검증 전 판독 초안입니다.")
html=html.replace("  text('테마와 글자 크기는 이번 정보 구조 단계에서 확정하지 않습니다. 화면 조작은 승인으로 기록되지 않습니다.');", '''  text('통상문 사진 8장은 이번 뷰어의 이미지 자료로 연결하지 않았습니다. 사진에서 추출한 텍스트 참조(JSON/Markdown)를 로컬에 저장하고 HTML에는 생성 시점의 텍스트 스냅샷을 넣었습니다. 날짜별 고유문이 없는 곳은 미등록 표시합니다. 선택지와 인쇄된 교황·주교 이름은 실제 현재 미사 설정으로 확정하지 않습니다.');
  const refs=document.createElement('p');[['../docs/references/교중미사_통상문_텍스트_초안.md','텍스트 참조(Markdown)'],['../docs/references/교중미사_통상문_텍스트_초안.json','텍스트 데이터(JSON)']].forEach(([url,name])=>{const a=document.createElement('a');a.href=encodeURI(url);a.target='_blank';a.rel='noopener';a.textContent=name;refs.append(a,document.createTextNode(' '));});body.append(refs);
  text('악보 블록은 제목 줄을 제외한 한 페이지의 가용 높이를 사용하며, 사진이 더 길면 악보 카드 안에서 스크롤합니다.');
  text('테마와 글자 크기는 이번 정보 구조 단계에서 확정하지 않습니다. 화면 조작은 승인으로 기록되지 않습니다.');''')
with (root/'review/02-ia-v11.html').open('w',encoding='utf-8',newline='\r\n') as f:f.write(html)
(root/'work/review-ia-v11-check.js').write_text(re.search(r'<script>(.*?)</script>',html,re.S).group(1),encoding='utf-8')
assert '173855074' not in html and 'Downloads' not in html
print('Created v11: extracted text snapshot and page-height score cards; no new source photo references')
