from pathlib import Path
import json,re,hashlib

root=Path(__file__).resolve().parents[1]
source=root/'docs/교중미사악보'
manifest=[]
for file in sorted(source.glob('KakaoTalk_20261018_172809020*.jpg')):
 manifest.append({'file':file.name,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
def asset(suffix, title, rotation=0, width=3000, height=4000):
 return {'path':f'../docs/교중미사악보/KakaoTalk_20261018_172809020{suffix}.jpg','title':title,'rotation':rotation,'width':width,'height':height,'temporary':True,'source':'user-provided','licenseStatus':'unverified'}
assets={
 '자비송':[asset('','자비송')],
 '대영광송':[asset('_01','대영광송 앞부분',-90),asset('_02','대영광송 이어지는 부분',180,4000,3000)],
 '거룩하시도다 · 신앙의 신비여':[asset('_03','거룩하시도다 · 신앙의 신비여 (함께 촬영)',180,4000,3000)],
 '아멘':[asset('_04','아멘')],
 '주님의 기도':[asset('_05','주님의 기도 앞부분'),asset('_06','주님의 기도 이어지는 부분')],
 '주님의 기도 맺음 환호':[asset('_07','주님의 기도 맺음 환호 · 하느님의 어린양 (함께 촬영)')],
 '하느님의 어린양':[asset('_07','하느님의 어린양 · 주님의 기도 맺음 환호 (함께 촬영)')]
}
html=(root/'review/02-ia-v8.html').read_text(encoding='utf-8').replace('검토 v8','검토 v9')
html=html.replace('<option>새벽미사</option><option>교중미사</option><option>주일 저녁 젊은이 미사</option>', '<option value="dawn">새벽미사</option><option value="main" selected>교중미사</option><option value="youth">주일 저녁 젊은이 미사</option>')
html=html.replace('--draft-score-height: 3rem;', '--draft-score-photo-height: 22rem; --draft-score-height: 3rem;')
html=html.replace(' .reader__item-title {', ' .reader__item-heading { display: flex; flex-wrap: wrap; align-items: center; gap: var(--draft-gap); margin-block-end: var(--draft-toc-gap); }\n .reader__item-title {')
html=html.replace(' .reader__prayer-option {', ' .reader__score-photo { display: block; width: 100%; max-height: var(--draft-score-photo-height); }\n .reader__prayer-option {')
start=html.index('function renderPrayerCard(')
end=html.index('let selectedItem = null;',start)
code='const temporaryPrincipalScores = '+json.dumps(assets,ensure_ascii=False)+';\n'
code+='''
function scoreAssets(prayerId) { return find('slot').value === 'main' ? (temporaryPrincipalScores[prayerId] || []) : []; }
function selectedSlotName() { return find('slot').selectedOptions[0].textContent; }
function renderPhoto(asset) {
 const figure=document.createElement('figure');figure.className='reader__score';
 const caption=document.createElement('figcaption');caption.textContent=`교중미사 임시 악보 · ${asset.title} `;
 const link=document.createElement('a');link.href=encodeURI(asset.path);link.target='_blank';link.rel='noopener noreferrer';link.textContent='원본 열기';caption.append(link);
 const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('class','reader__score-photo');svg.setAttribute('role','img');svg.setAttribute('aria-label',`${asset.title} · 사용자 제공 사진, 임시 배치`);
 const quarter=Math.abs(asset.rotation)===90;const width=quarter?asset.height:asset.width;const height=quarter?asset.width:asset.height;
 svg.setAttribute('viewBox',`0 0 ${width} ${height}`);
 const image=document.createElementNS('http://www.w3.org/2000/svg','image');image.setAttribute('href',encodeURI(asset.path));image.setAttribute('width',String(asset.width));image.setAttribute('height',String(asset.height));
 if(asset.rotation===-90)image.setAttribute('transform',`translate(0 ${asset.width}) rotate(-90)`);
 if(asset.rotation===180)image.setAttribute('transform',`translate(${asset.width} ${asset.height}) rotate(180)`);
 image.addEventListener('error',()=>{caption.textContent=`${asset.title} · 이미지 로딩 실패. 프로젝트의 docs/교중미사악보 경로를 확인해 주세요.`;});
 svg.append(image);figure.append(caption,svg);return figure;
}
function renderPrayerFrame(title, prayerId, scoreSlot=true, level=3) {
 const frame=document.createElement('section');frame.className='reader__item';
 const headingRow=document.createElement('div');headingRow.className='reader__item-heading';
 const heading=document.createElement(`h${level}`);heading.className='reader__item-title';heading.textContent=title;headingRow.append(heading);
 const group=document.createElement('div');group.className='reader__prayer-option';group.setAttribute('role','group');group.setAttribute('aria-label',`${title} 표시 방식`);
 const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source','ordinary+temporaryPrincipalScores');
 if(scoreSlot)headingRow.append(group);frame.append(headingRow,card);
 function fill() {
  card.replaceChildren();group.replaceChildren();const assets=scoreAssets(prayerId);
  const mode=parishPrayerPresentation[prayerId] || (assets.length?'chant':'recite');
  if(scoreSlot)[['recite','낭송 · 본문'],['chant','성가 · 악보']].forEach(([value,text])=>{
   const button=document.createElement('button');button.type='button';button.className='reader__prayer-button';button.textContent=text;button.setAttribute('aria-pressed',String(mode===value));button.setAttribute('data-prayer-mode',value);
   button.onclick=()=>{parishPrayerPresentation[prayerId]=value;fill();group.querySelector(`[data-prayer-mode="${value}"]`)?.focus();};group.append(button);
  });
  if(mode==='chant' && scoreSlot){
   if(assets.length)assets.forEach(asset=>card.append(renderPhoto(asset)));
   else{const p=document.createElement('p');p.textContent=`${selectedSlotName()} · 이 기도문의 임시 악보 미등록`;card.append(p);}
  } else {const p=document.createElement('p');p.className='reader__item-text';p.lang='la';p.textContent=mockParagraph;card.append(p);}
 }
 fill();return frame;
}
function renderItem(item) {
 const spec=frameSpecs[item.title];
 let section;
 if(spec.kind==='prayer') section=renderPrayerFrame(item.title,spec.prayerId,spec.scoreSlot);
 else {
  section=document.createElement('section');section.className='reader__item';
  const h=document.createElement('h3');h.className='reader__item-title';h.textContent=item.title;section.append(h);
  if(spec.kind==='choice'){const p=document.createElement('p');p.className='reader__item-text';p.textContent=spec.guide;section.append(p);}
  else {const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source',spec.source);const p=document.createElement('p');p.className='reader__item-text';p.lang='la';p.textContent=mockParagraph;card.append(p);section.append(card);}
 }
 section.id=item.id;section.tabIndex=-1;
 if(item.id===selectedItem){section.setAttribute('aria-current','location');section.querySelector('h3').textContent+=' · 현재 위치';}
 if(item.title==='감사 기도') ['거룩하시도다 · 신앙의 신비여','아멘'].forEach(title=>section.append(renderPrayerFrame(title,title,true,4)));
 if(item.title==='주님의 기도') section.append(renderPrayerFrame('주님의 기도 맺음 환호','주님의 기도 맺음 환호',true,4));
 if(item.title==='영성체 예식 · 영성체 성가') section.append(renderPrayerFrame('하느님의 어린양','하느님의 어린양',true,4));
 return section;
}

'''
html=html[:start]+code+html[end:]
html=html.replace("${find('slot').value}","${selectedSlotName()}")
old="['성호경','주님의 기도','성모송','영광송'].forEach(title=>{const section=document.createElement('section');section.className='reader__item';const heading=document.createElement('h3');heading.className='reader__item-title';heading.textContent=title;section.append(heading,renderPrayerCard(title,title,title!=='성호경'));body.append(section);});"
new="['성호경','자비송','대영광송','거룩하시도다 · 신앙의 신비여','아멘','주님의 기도','주님의 기도 맺음 환호','하느님의 어린양','성모송','영광송'].forEach(title=>body.append(renderPrayerFrame(title,title,title!=='성호경')));"
assert old in html
html=html.replace(old,new)
html=html.replace("본문은 Lorem ipsum mock입니다.","본문은 Lorem ipsum mock이며 사진 악보는 사용자가 제공한 임시 교중미사 자료입니다.")
html=html.replace("아래 선택은 mock 체험이며 실제 본당 편성·악보 등록은 미구현입니다.","교중미사 사진 악보를 임시로 배치했습니다. 본문은 mock이며 실제 본당 편성 확정 자료가 아닙니다.")
html=html.replace("현재 모든 자료 연동·성가 편집은 미구현입니다.","현재 공식 자료 자동 연동·성가 편집은 미구현이며 사용자 제공 사진 악보만 임시로 연결했습니다.")
html=html.replace("악보는 출처·이용 조건 확인 후 이미지나 PDF를 연결할 자리이며 현재 빈 오선만 표시합니다.","교중미사에 한해 사용자 제공 사진을 임시 표시합니다. 다른 회차에는 사진을 자동 배정하지 않습니다. 실제 기도문 본문·순서는 공통으로 유지하고 사진 리소스만 별도 참조합니다.")
html=html.replace("모든 라틴어 본문은 Lorem ipsum mock입니다.","모든 라틴어 본문은 Lorem ipsum mock입니다. 사진 악보는 교중미사 임시 첨부입니다.")
html=html.replace("find('mode').onchange = render; find('slot').onchange = context;", "find('mode').onchange = render; find('slot').onchange = () => { context(); render(); };")
# Keep the displayed spread and its scroll offsets during mode/session changes.
html=html.replace('function render() {', '''let previousRenderKey = null;
function render() {
 const renderKey=`${part}|${spread}`;const pageOffsets=Array.from(find('book').children).map(page=>page.scrollTop);''')
html=html.replace(' position[part] = spread; renderToc();', " if(previousRenderKey===renderKey)Array.from(find('book').children).forEach((page,index)=>{page.scrollTop=pageOffsets[index]||0;});previousRenderKey=renderKey;\n position[part] = spread; renderToc();")
with (root/'review/02-ia-v9.html').open('w',encoding='utf-8',newline='\r\n') as f:f.write(html)
(root/'work/review-ia-v9-check.js').write_text(re.search(r'<script>(.*?)</script>',html,re.S).group(1),encoding='utf-8')
with (root/'docs/교중미사악보/temporary-score-manifest.json').open('w',encoding='utf-8',newline='\r\n') as f:json.dump({'status':'temporary-user-provided','defaultSession':'main','attachmentsOnlyFor':'main','rightsStatus':'unverified','files':manifest,'mapping':assets},f,ensure_ascii=False,indent=2)
assert all(hashlib.sha256((source/x['file']).read_bytes()).hexdigest()==x['sha256'] for x in manifest)
print('Created v9 and score manifest; eight original photo hashes preserved')
