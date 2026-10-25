from pathlib import Path
import re,json
s=Path('review/02-ia-v16.html').read_text(encoding='utf-8').replace('검토 v16','검토 v17')
s=s.replace(' .reader__guidance--in-speech { margin-inline-start: calc(var(--draft-marker-width) + var(--draft-marker-gap)); }',' .reader__speech-body { min-inline-size: 0; }')
start=s.index('  parts.forEach(part=>{');end=s.index('stack.append(card);',start)
s=s[:start]+r'''
  let speechBody=null;
  const openRow=markerText=>{const row=document.createElement('div');row.className='reader__speech-row';const marker=document.createElement('span');marker.className='reader__speech-marker';marker.setAttribute('aria-hidden','true');marker.textContent=markerText;speechBody=document.createElement('div');speechBody.className='reader__speech-body';row.append(marker,speechBody);card.append(row);};
  parts.forEach(part=>{
   if(part.kind==='guide'){const p=document.createElement('p');p.className=segment.kind==='guide'?'reader__speech-text':'reader__speech-text reader__guidance';p.textContent='안내 · '+part.text.replace(/^\[(?:안내|프레임 안내|자료 안내)\]\s*|^인쇄본 안내:\s*/,'');if(segment.kind==='guide')card.append(p);else{if(!speechBody)openRow('');speechBody.append(p);}return;}
   const match=part.text.match(/^([+◎◆○●])\s*/);if(match||!speechBody)openRow(match?match[1]:'');
   const p=document.createElement('p');p.className='reader__speech-text';p.textContent=match?part.text.slice(match[0].length):part.text;speechBody.append(p);
  });
  '''.replace(chr(92)*2,chr(92))+s[end:]
# Prefer a prepared vector edition only for the parish session it belongs to.
registry="const reengravedPrincipalScores = { '아멘': [{kind:'engraved',title:'아멘',path:'../docs/교중미사악보/reengraved/amen.pdf',preview:'../docs/교중미사악보/reengraved/amen.svg',status:'사진 대조 완료 · 본당 최종 교정 전'}] };\n"
s=s.replace('function scoreAssets(prayerId)',registry+'function scoreAssets(prayerId)',1)
s=s.replace('(temporaryPrincipalScores[prayerId] || [])','(reengravedPrincipalScores[prayerId] || temporaryPrincipalScores[prayerId] || [])',1)
s=s.replace("function renderPhoto(asset) {",'''function renderPhoto(asset) {
 if(asset.kind==='engraved'){
  const figure=document.createElement('figure');figure.className='reader__score';figure.setAttribute('data-score-kind','reengraved');
  const caption=document.createElement('figcaption');caption.textContent=`교중미사 재조판 · ${asset.title} `;const link=document.createElement('a');link.href=encodeURI(asset.path);link.target='_blank';link.rel='noopener noreferrer';link.textContent='PDF 열기';caption.append(link);
  const preview=document.createElement('img');preview.className='reader__score-photo';preview.src=encodeURI(asset.preview);preview.alt=asset.title+' · PDF와 동일한 음표·가사 조판';
  const note=document.createElement('p');note.textContent=asset.status;figure.append(caption,preview,note);return figure;
 }
''',1)
# Entrance hymn: full page score mock, no missing-data/participation copy.
helper='''function renderEntranceScore(){
 const section=document.createElement('section');section.className='reader__item reader__item--score';
 const row=document.createElement('div');row.className='reader__item-heading';const title=document.createElement('h3');title.className='reader__item-title';title.textContent='입당 성가';row.append(title);
 const card=document.createElement('div');card.className='reader__content-card reader__content-card--score';card.setAttribute('data-content-source','hymn-score-mock');const label=document.createElement('p');label.textContent='악보 표시 영역 · mock';
 const scroll=document.createElement('div');scroll.className='reader__score-scroll';scroll.setAttribute('tabindex','0');scroll.setAttribute('role','region');scroll.setAttribute('aria-label','입당 성가 악보 목데이터');
 const preview=document.createElement('img');preview.className='reader__score-photo';preview.src='../docs/mock/entrance-score.svg';preview.alt='입당 성가 악보 배치용 목데이터';scroll.append(preview);card.append(label,scroll);section.append(row,card);return section;
}
'''
s=s.replace('function renderItem(item) {',helper+'\nfunction renderItem(item) {',1)
s=s.replace(" const spec=frameSpecs[item.title];", " if(item.title==='입당 성가')return renderEntranceScore();\n const spec=frameSpecs[item.title];",1)
s=s.replace("text('악보 블록은", "text('아멘은 사진 대조한 PDF 재조판본으로 부분 교체했습니다. 다른 곡은 기존 임시 사진을 유지합니다.');\n  text('악보 블록은",1)
Path('review/02-ia-v17.html').write_text(s,encoding='utf-8',newline='\r\n')
Path('work/review-ia-v17-check.js').write_text(re.search(r'<script>(.*?)</script>',s,re.S).group(1),encoding='utf-8')
# Deliberately fabricated music shapes for layout, never an assigned hymn.
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1100" role="img" aria-label="악보 목데이터"><rect width="800" height="1100" fill="white"/><text x="400" y="52" font-family="Malgun Gothic, sans-serif" font-size="24" text-anchor="middle">악보 목데이터</text>']
for system in range(6):
 y=110+system*155
 for line in range(5):svg.append(f'<path d="M45 {y+line*12} H755" stroke="black" fill="none"/>')
 for j in range(9):
  x=92+j*73;ny=y+48-[0,2,4,3,1,2,4,2,0][j]*6
  svg.append(f'<ellipse cx="{x}" cy="{ny}" rx="8" ry="5" transform="rotate(-15 {x} {ny})"/><path d="M{x+7} {ny} v-38" stroke="black"/>')
 svg.append(f'<text x="45" y="{y+85}" font-family="Malgun Gothic, sans-serif" font-size="16">mock</text>')
svg.append('</svg>');Path('docs/mock').mkdir(exist_ok=True);Path('docs/mock/entrance-score.svg').write_text(''.join(svg),encoding='utf-8')
