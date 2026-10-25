from pathlib import Path
import re
s=Path('review/02-ia-v46.html').read_text(encoding='utf-8').replace('v46','v47')
s=s.replace(':root { ',':root { --draft-preview-portrait-width: 48rem; --draft-preview-portrait-height: 64rem; --draft-preview-landscape-width: 64rem; --draft-preview-landscape-height: 48rem; ',1)
s=s.replace(' .reader__header, .reader__row, .reader__footer {', ''' .reader[data-orientation="portrait"] { inline-size: min(100%, var(--draft-preview-portrait-width)); block-size: var(--draft-preview-portrait-height); margin-inline: auto; }
 .reader[data-orientation="landscape"] { inline-size: min(100%, var(--draft-preview-landscape-width)); block-size: var(--draft-preview-landscape-height); margin-inline: auto; }
 .reader__header, .reader__row, .reader__footer {''',1)
s=s.replace('<main class="reader">','<main class="reader" data-js="reader" data-orientation="auto">')
s=s.replace('<p class="reader__notice" data-js="context" role="status"></p>','<div class="reader__row"><p class="reader__notice" data-js="context" role="status"></p><span data-js="viewport-status" role="status"></span><button type="button" data-js="viewport-rotate" hidden>방향 전환</button><button type="button" data-js="viewport-reset" hidden>화면에 맞춤</button></div>')
helper='''
let viewerOrientation='auto';
function setViewerOrientation(value){
 if(!['auto','portrait','landscape'].includes(value))return;
 captureReaderScroll();persistReader();viewerOrientation=value;find('reader').setAttribute('data-orientation',value);
 find('viewport-status').textContent=value==='auto'?'':'뷰어 미리보기 · '+(value==='portrait'?'세로 768 × 1024':'가로 1024 × 768')+' · 좁은 창에서는 너비 축소';
 find('viewport-rotate').hidden=value==='auto';find('viewport-reset').hidden=value==='auto';
 find('viewport-rotate').textContent=value==='portrait'?'가로로 전환':'세로로 전환';
 if(typeof requestAnimationFrame==='function')scheduleReflow(currentAnchor);
}
'''
s=s.replace('function showPanel(',helper+'\nfunction showPanel(',1)
needle="  text('우측 하단에서 여는 e-book 보기 설정입니다. 이 단계는 항목 위치를 검토하며 실제 글자 크기·테마 적용은 후속 디자인 단계에서 구현합니다.');"
assert needle in s
s=s.replace(needle,'''  text('뷰어 방향 미리보기로 화면을 가로·세로 크기로 바꿔 볼 수 있습니다. 세로 화면이 창보다 높으면 브라우저를 스크롤하세요. 실제 기기의 터치·브라우저 UI까지 재현하지는 않습니다.');
  const orientationGroup=document.createElement('div');orientationGroup.className='reader__row';orientationGroup.setAttribute('role','group');orientationGroup.setAttribute('aria-label','뷰어 방향 미리보기');
  [['auto','현재 화면에 맞춤'],['landscape','가로 1024 × 768'],['portrait','세로 768 × 1024']].forEach(([value,label])=>{const b=document.createElement('button');b.type='button';b.textContent=label;b.setAttribute('aria-pressed',String(viewerOrientation===value));b.onclick=()=>{find('drawer').close();setViewerOrientation(value);find(value==='auto'?'part-next':'viewport-rotate').focus({preventScroll:true});};orientationGroup.append(b);});body.append(orientationGroup);''')
s=s.replace("bindPageSwipe(find('book'));", "find('viewport-rotate').onclick=()=>setViewerOrientation(viewerOrientation==='portrait'?'landscape':'portrait');\nfind('viewport-reset').onclick=()=>{setViewerOrientation('auto');find('part-next').focus({preventScroll:true});};\nbindPageSwipe(find('book'));")
Path('review/02-ia-v47.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v47-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
