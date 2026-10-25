from pathlib import Path
import re
p=Path('review/02-ia-v26.html');s=p.read_text(encoding='utf-8').replace('v26','v27')
# Keep fixed SVG version references from v26.
s=s.replace('gloria-v27.svg','gloria-v26.svg').replace('lords-prayer-v27.svg','lords-prayer-v26.svg')
s=s.replace(" });blocks.push({key:`part-${partIndex}-transition`,tocId:contents[partIndex].at(-1).id,transition:partIndex+1});return blocks;", " });return blocks;")
s=s.replace("const anchor=options.anchorKey||currentAnchor||contents[part][0].id;", "let anchor=options.anchorKey||currentAnchor||contents[part][0].id;")
s=s.replace("layouts=composePages();if(!layouts.length)return;", "layouts=composePages();if(!layouts.length)return;if(options.edge==='last')anchor=layouts.at(-1).blocks[0].key;")
s=s.replace("find('page-prev').disabled=spread===0;find('page-next').disabled=(spread+1)*2>=layouts.length;renderToc();", "const turn=pageTurnState(part,spread,layouts.length);find('page-prev').disabled=!turn.previous;find('page-next').disabled=!turn.next;find('page-next').setAttribute('data-next-part',String(turn.nextPart));find('page-next').setAttribute('aria-label',turn.nextPart?parts[part+1].title+'의 첫 두 페이지로 이동':'뒤쪽 두 페이지');find('page-prev').setAttribute('aria-label',turn.previousPart?parts[part-1].title+'의 마지막 두 페이지로 이동':'앞쪽 두 페이지');hintNextPart(turn.nextPart);renderToc();")
s=s.replace("function turnSpread(direction){const page=layouts[(spread+direction)*2];if(page)render({anchorKey:page.blocks[0].key});}", """function pageTurnState(partIndex,spreadIndex,pageCount){const first=spreadIndex===0,last=(spreadIndex+1)*2>=pageCount;return {previous:!first||partIndex>0,next:!last||partIndex<parts.length-1,previousPart:first&&partIndex>0,nextPart:last&&partIndex<parts.length-1};}
let nextPartHint=null;
function hintNextPart(active){if(nextPartHint){nextPartHint.cancel();nextPartHint=null;}const button=find('page-next');if(active && button.animate && !globalThis.matchMedia?.('(prefers-reduced-motion: reduce)').matches){nextPartHint=button.animate([{outlineWidth:'0px',outlineStyle:'solid',outlineColor:'currentColor',outlineOffset:'0px'},{outlineWidth:'3px',outlineStyle:'solid',outlineColor:'currentColor',outlineOffset:'3px'},{outlineWidth:'0px',outlineStyle:'solid',outlineColor:'currentColor',outlineOffset:'0px'}],{duration:1400,iterations:3});}}
function turnSpread(direction){const page=layouts[(spread+direction)*2];if(page){render({anchorKey:page.blocks[0].key});return;}const target=part+direction;if(target<0||target>=parts.length)return;part=target;currentAnchor=null;selectedItem=null;render(direction<0?{edge:'last'}:{anchorKey:contents[part][0].id});}
function swipeDirection(dx,dy){return Math.abs(dx)>=64 && Math.abs(dx)>Math.abs(dy)*1.5?(dx<0?1:-1):0;}
function bindPageSwipe(book){let gesture=null;book.addEventListener('pointerdown',event=>{if(!event.isPrimary || event.button!==0 || event.target.closest('button,a,input,select,textarea,[contenteditable="true"]'))return;gesture={id:event.pointerId,x:event.clientX,y:event.clientY};});book.addEventListener('pointermove',event=>{if(!gesture||gesture.id!==event.pointerId)return;const dx=event.clientX-gesture.x,dy=event.clientY-gesture.y;if(Math.abs(dy)>16 && Math.abs(dy)>Math.abs(dx)){gesture=null;return;}if(Math.abs(dx)>16 && Math.abs(dx)>Math.abs(dy)*1.5 && event.cancelable)event.preventDefault();});book.addEventListener('pointerup',event=>{if(!gesture||gesture.id!==event.pointerId)return;const start=gesture;gesture=null;const direction=swipeDirection(event.clientX-start.x,event.clientY-start.y);if(direction)turnSpread(direction);});book.addEventListener('pointercancel',()=>gesture=null);book.addEventListener('pointerleave',()=>gesture=null);book.addEventListener('dragstart',event=>{if(event.target.tagName==='IMG')event.preventDefault();});}
""")
s=s.replace('container-type: size; min-height:', 'container-type: size; touch-action: pan-y; min-height:')
# Pair only short adjacent EP responses, preserving long prayer paragraphs.
needle=" if(block.alternative){const card="
s=s.replace(needle,""" if(block.item?.title==='감사기도 제2양식'){const lit=node.querySelector('.reader__liturgy');if(lit){const children=Array.from(lit.children);children.forEach((child,i)=>{const next=children[i+1];if(child.getAttribute('data-speech-role')==='priest' && next?.getAttribute('data-speech-role')==='assembly' && child.textContent.length<=80 && next.textContent.length<=80){const pair=document.createElement('div');pair.className='reader__dialogue';lit.insertBefore(pair,child);pair.append(child,next);}});}}
"""+needle)
s=s.replace("find('part-prev').onclick", "bindPageSwipe(find('book'));\nfind('part-prev').onclick",1)
s=s.replace('aria-label="현재 예식 안에서 페이지 넘기기"','aria-label="두 페이지씩 이전·다음 전례로 넘기기"')
s=s.replace('길어지면 같은 예식 안에서 페이지를 넘깁니다. 아래 예식 이름 버튼은 이전·다음 예식으로 이동합니다.','아래 페이지 버튼이나 좌우 드래그로 두 페이지씩 넘기며, 끝에서는 다음 전례로 이어집니다. 제목 옆 버튼은 이전·다음 전례로 이동합니다.')
Path('review/02-ia-v27.html').write_text(s,encoding='utf-8',newline='\r\n')
Path('work/review-ia-v27-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
p=Path('work/test-reader-v26.cjs');t=p.read_text(encoding='utf-8').replace('02-ia-v26.html','02-ia-v27.html');Path('work/test-reader-v27.cjs').write_text(t,encoding='utf-8',newline='\r\n')
