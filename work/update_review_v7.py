from pathlib import Path
import json,re

root=Path(__file__).resolve().parents[1]
html=(root/'review/02-ia-v6.html').read_text(encoding='utf-8').replace('검토 v6','검토 v7')
match=re.search(r'const frameSpecs = (.*?);\n',html)
specs=json.loads(match.group(1))
for title in ['성호경','자비송','대영광송','주님의 기도']:
    specs[title]['kind']='prayer'
    specs[title]['prayerId']=title
    specs[title]['scoreSlot']= title!='성호경'
specs['신앙 고백'].update(kind='prayer',prayerId='신앙 고백',scoreSlot=True)
html=html[:match.start(1)]+json.dumps(specs,ensure_ascii=False)+html[match.end(1):]
code='''
// The prototype holds parish presentation choices in memory only, shared by all Sunday sessions.
const parishPrayerPresentation = Object.create(null);
const prayerSourceRefs = {textRef:null, scoreRef:null, sourceUrl:null, licenseStatus:'unverified'};
function renderPrayerCard(title, prayerId, scoreSlot = true) {
 const card = document.createElement('div'); card.className = 'reader__content-card';
 card.setAttribute('data-content-source','ordinary+parishPrayerSetting');
 function fill() {
  card.replaceChildren();
  const mode = parishPrayerPresentation[prayerId] || 'recite';
  if (scoreSlot) {
   const label = document.createElement('label'); label.className = 'reader__prayer-option'; label.textContent = `${title} 표시 (mock) `;
   const select = document.createElement('select'); select.setAttribute('aria-label',`${title} 낭송 또는 성가`);
   [['recite','낭송 · 본문'],['chant','성가 · 악보']].forEach(([value,text])=>{const option=document.createElement('option');option.value=value;option.textContent=text;select.append(option);});
   select.value=mode; select.onchange=()=>{parishPrayerPresentation[prayerId]=select.value;fill();card.querySelector('select')?.focus();}; label.append(select); card.append(label);
  }
  const p = document.createElement('p'); p.className='reader__item-text';p.lang='la';p.textContent=mockParagraph;card.append(p);
  if (mode==='chant' && scoreSlot) {
   const figure=document.createElement('figure');figure.className='reader__score';
   const caption=document.createElement('figcaption');caption.textContent='악보 자리 · 미등록 (mock, 실제 악보 아님)';
   const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 400 60');svg.setAttribute('class','reader__staff');svg.setAttribute('role','img');svg.setAttribute('aria-label','악보가 들어갈 위치를 나타내는 빈 오선');
   [10,20,30,40,50].forEach(y=>{const line=document.createElementNS('http://www.w3.org/2000/svg','line');line.setAttribute('x1','0');line.setAttribute('x2','400');line.setAttribute('y1',String(y));line.setAttribute('y2',String(y));line.setAttribute('stroke','currentColor');svg.append(line);});
   figure.append(caption,svg);card.append(figure);
  }
 }
 fill(); return card;
}
'''
html=html.replace('function renderItem(item) {',code+'\nfunction renderItem(item) {')
html=html.replace(" if (spec.kind === 'choice') {", " if (spec.kind === 'prayer') {\n  section.append(renderPrayerCard(item.title,spec.prayerId,spec.scoreSlot));\n } else if (spec.kind === 'choice') {")
old="if (which === 'prayer') text('성호경 · 주님의 기도 · 성모송 · 영광송. 공식 원문은 아직 연결하지 않았습니다.');"
new="""if (which === 'prayer') {
  text('기도문 본문과 본당별 기도문 성가·악보를 카드에 표시합니다. 아래 선택은 mock 체험이며 실제 본당 편성·악보 등록은 미구현입니다.');
  ['성호경','주님의 기도','성모송','영광송'].forEach(title=>{const section=document.createElement('section');section.className='reader__item';const heading=document.createElement('h3');heading.className='reader__item-title';heading.textContent=title;section.append(heading,renderPrayerCard(title,title,title!=='성호경'));body.append(section);});
 }"""
assert old in html
html=html.replace(old,new)
# Refresh shared presentation when the drawer is dismissed, preserving current item and spread.
html=html.replace("find('drawer').addEventListener('close', () => { const target", "find('drawer').addEventListener('close', () => { render(); const target")
html=html.replace('고정 기도문은 카드 없는 본문','기도문은 본문·악보 카드')
html=html.replace("  text('영성체 프레임은", "  text('기도문 카드는 고정 공식 본문과 본당별 기도문 성가 악보 참조를 분리합니다. 본당 설정은 세 주일 회차에 공통 적용하며, 회차별 네 성가 배정을 변경하지 않습니다. 낭송/성가 선택은 mock 체험으로 새로고침 시 초기화됩니다. 악보는 출처·이용 조건 확인 후 이미지나 PDF를 연결할 자리이며 현재 빈 오선만 표시합니다.');\n  text('영성체 프레임은")
html=html.replace('--draft-item-gap: .75rem;', '--draft-score-height: 3rem; --draft-item-gap: .75rem;')
html=html.replace(' .reader__toc-link {', ''' .reader__prayer-option { display: block; margin-block-end: var(--draft-toc-gap); }
 .reader__score { margin: var(--draft-toc-gap) 0 0; }
 .reader__staff { display: block; width: 100%; height: var(--draft-score-height); }
 .reader__toc-link {''')
with (root/'review/02-ia-v7.html').open('w',encoding='utf-8',newline='\r\n') as f:f.write(html)
(root/'work/review-ia-v7-check.js').write_text(re.search(r'<script>(.*?)</script>',html,re.S).group(1),encoding='utf-8')
print('Created v7 prayer cards with mock score slots')
