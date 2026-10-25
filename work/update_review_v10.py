from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
html=(root/'review/02-ia-v9.html').read_text(encoding='utf-8').replace('검토 v9','검토 v10')
html=html.replace('--draft-score-photo-height: 22rem;', '--draft-score-scroll-max: 14rem;')
html=html.replace('.reader__book { min-height: 0;', '.reader__book { position: relative; container-type: size; min-height: 0;')
html=html.replace('padding: var(--draft-padding); overflow: auto; overflow-wrap: anywhere;', 'padding: var(--draft-padding); overflow: hidden; overflow-wrap: anywhere;')
html=html.replace(' .reader__item {', ''' .reader__page--measure { position: absolute; inset-block: 0; inset-inline-start: 0; width: calc((100% - var(--draft-gap)) / 2); visibility: hidden; pointer-events: none; }
 .reader__page--oversize { overflow: auto; }
 .reader__item:last-child { margin-block-end: 0; }
 .reader__item {''')
html=html.replace(' .reader__score-photo { display: block; width: 100%; max-height: var(--draft-score-photo-height); }', ''' .reader__score-photo { display: block; width: 100%; height: auto; }
 .reader__score-scroll { block-size: min(var(--draft-score-scroll-max), 40cqh); overflow: auto; overscroll-behavior: contain; }''')
html=html.replace('if(assets.length)assets.forEach(asset=>card.append(renderPhoto(asset)));', '''if(assets.length){
    const scoreWindow=document.createElement('div');scoreWindow.className='reader__score-scroll';scoreWindow.setAttribute('tabindex','0');scoreWindow.setAttribute('role','region');scoreWindow.setAttribute('aria-label',`${title} 악보 · 카드 안에서 스크롤`);
    assets.forEach(asset=>scoreWindow.append(renderPhoto(asset)));card.append(scoreWindow);
   }''')
old="button.onclick=()=>{parishPrayerPresentation[prayerId]=value;fill();group.querySelector(`[data-prayer-mode=\"${value}\"]`)?.focus();};group.append(button);"
new="""button.onclick=()=>{parishPrayerPresentation[prayerId]=value;fill();group.querySelector(`[data-prayer-mode="${value}"]`)?.focus();
     if(frame.closest('.reader__book')){pendingPrayerFocus={key:frame.getAttribute('data-flow-key'),mode:value};scheduleReflow(frame.getAttribute('data-flow-key'));}
    };group.append(button);"""
assert old in html
html=html.replace(old,new)
for line in [
 " if(item.title==='감사 기도') ['거룩하시도다 · 신앙의 신비여','아멘'].forEach(title=>section.append(renderPrayerFrame(title,title,true,4)));\n",
 " if(item.title==='주님의 기도') section.append(renderPrayerFrame('주님의 기도 맺음 환호','주님의 기도 맺음 환호',true,4));\n",
 " if(item.title==='영성체 예식 · 영성체 성가') section.append(renderPrayerFrame('하느님의 어린양','하느님의 어린양',true,4));\n"]:
 assert line in html
 html=html.replace(line,'')
html=html.replace("section.querySelector('h3').textContent+=' · 현재 위치';",'')
old="""function jumpToItem(partIndex, item) {
 part = partIndex; spread = Math.floor(item.page / 2); selectedItem = item.id;
 render(); const target=document.getElementById(item.id);target?.focus({preventScroll:true});target?.scrollIntoView({block:'nearest',inline:'nearest'});
}"""
new="""function jumpToItem(partIndex, item) {
 part=partIndex;selectedItem=item.id;render({anchorKey:item.id});
 const target=document.getElementById(item.id);target?.focus({preventScroll:true});
}"""
assert old in html
html=html.replace(old,new).replace('const position = parts.map(() => 0);','const position = parts.map(() => null);')
start=html.index('let previousRenderKey = null;')
end=html.index('function showPanel(',start)
engine='''
let layouts=[],currentAnchor=null,pendingPrayerFocus=null,reflowFrame=null;
function flowBlocks(partIndex) {
 const blocks=[];
 contents[partIndex].forEach(item=>{
  blocks.push({key:item.id,tocId:item.id,item});
  const add=(suffix,title)=>blocks.push({key:`${item.id}-${suffix}`,tocId:item.id,prayerTitle:title});
  if(item.title==='감사 기도'){add('sanctus','거룩하시도다 · 신앙의 신비여');add('amen','아멘');}
  if(item.title==='주님의 기도')add('doxology','주님의 기도 맺음 환호');
  if(item.title==='영성체 예식 · 영성체 성가')add('agnus','하느님의 어린양');
 });return blocks;
}
function renderBlock(block) {
 const node=block.item?renderItem(block.item):renderPrayerFrame(block.prayerTitle,block.prayerTitle);
 node.id=block.key;node.tabIndex=-1;node.setAttribute('data-flow-key',block.key);
 if(block.fragmentText!==undefined){const p=node.querySelector('.reader__item-text');if(p)p.textContent=block.fragmentText;}
 if(block.continued){const heading=node.querySelector('h3');if(heading)heading.textContent+=' (계속)';}
 return node;
}
function paginateFlow(blocks,fits,split) {
 const pages=[];let current=[];
 const flush=()=>{if(current.length){pages.push({blocks:current,oversize:false});current=[];}};
 blocks.forEach(block=>{
  if(fits([...current,block])){current.push(block);return;}
  flush();
  if(fits([block])){current=[block];return;}
  const fragments=split(block);
  fragments.forEach(fragment=>{
   if(fits([...current,fragment]))current.push(fragment);
   else {flush();if(fits([fragment]))current=[fragment];else pages.push({blocks:[fragment],oversize:true});}
  });
 });flush();return pages;
}
function spreadForAnchor(pages,key) {
 const index=pages.findIndex(page=>page.blocks.some(block=>block.key===key));return index<0?0:Math.floor(index/2);
}
function composePages() {
 const probe=document.createElement('article');probe.className='reader__page reader__page--measure';probe.setAttribute('aria-hidden','true');probe.inert=true;find('book').append(probe);
 const fits=blocks=>{probe.replaceChildren(...blocks.map(renderBlock));return probe.scrollHeight<=probe.clientHeight+1;};
 const split=block=>{
  const node=renderBlock(block);const paragraph=node.querySelector('.reader__item-text');
  if(!paragraph || paragraph.textContent.length<2)return [block];
  const result=[];let remaining=paragraph.textContent,index=0;
  while(remaining.length){
   let low=1,high=remaining.length,best=0;
   const key=index?`${block.key}-continue-${index}`:block.key;
   while(low<=high){const mid=Math.floor((low+high)/2);const fragment={...block,key,continued:index>0,fragmentText:remaining.slice(0,mid)};if(fits([fragment])){best=mid;low=mid+1;}else high=mid-1;}
   if(!best)return [block];
   if(best<remaining.length){const boundary=remaining.lastIndexOf(' ',best);if(boundary>best/2)best=boundary+1;}
   result.push({...block,key,continued:index>0,fragmentText:remaining.slice(0,best)});remaining=remaining.slice(best);index++;
  }return result;
 };
 try{return paginateFlow(flowBlocks(part),fits,split);}finally{probe.remove();}
}
function render(options={}) {
 const book=find('book');if(book.clientWidth<2||book.clientHeight<2)return;
 const anchor=options.anchorKey||currentAnchor||contents[part][0].id;
 layouts=composePages();if(!layouts.length)return;
 spread=spreadForAnchor(layouts,anchor);
 const visible=layouts.slice(spread*2,spread*2+2);
 const anchorBlock=layouts.flatMap(page=>page.blocks).find(block=>block.key===anchor)||visible[0].blocks[0];
 currentAnchor=anchorBlock.key;selectedItem=anchorBlock.tocId;position[part]=currentAnchor;
 const nodes=visible.map((layout,index)=>{
  const page=document.createElement('article');page.className=layout.oversize?'reader__page reader__page--oversize':'reader__page';
  page.setAttribute('aria-label',`${parts[part].title} ${spread*2+index+1}쪽`);
  layout.blocks.forEach(block=>page.append(renderBlock(block)));return page;
 });
 if(nodes.length===1){const blank=document.createElement('article');blank.className='reader__page';blank.setAttribute('aria-label','빈 페이지');nodes.push(blank);}
 book.replaceChildren(...nodes);find('part-title').textContent=parts[part].title;
 find('part-current').textContent=`현재: ${parts[part].title}`;
 find('part-prev').textContent=part?`← ${parts[part-1].title}`:'미사 시작';find('part-prev').disabled=part===0;
 find('part-next').textContent=part<parts.length-1?`${parts[part+1].title} →`:'미사 마침';find('part-next').disabled=part===parts.length-1;
 find('page-context').textContent=`${parts[part].title} · ${spread*2+1}–${Math.min(spread*2+2,layouts.length)}쪽 / 총 ${layouts.length}쪽`;
 find('page-prev').disabled=spread===0;find('page-next').disabled=(spread+1)*2>=layouts.length;renderToc();
 if(pendingPrayerFocus){const request=pendingPrayerFocus;pendingPrayerFocus=null;const block=Array.from(book.querySelectorAll('[data-flow-key]')).find(node=>node.getAttribute('data-flow-key')===request.key);block?.querySelector(`[data-prayer-mode="${request.mode}"]`)?.focus({preventScroll:true});}
}
function scheduleReflow(anchorKey=currentAnchor) {
 if(reflowFrame!==null)cancelAnimationFrame(reflowFrame);
 reflowFrame=requestAnimationFrame(()=>{reflowFrame=null;render({anchorKey});});
}
function go(index){part=index;currentAnchor=position[index]||contents[index][0].id;render({anchorKey:currentAnchor});}
function turnSpread(direction){const page=layouts[(spread+direction)*2];if(page)render({anchorKey:page.blocks[0].key});}
'''
html=html[:start]+engine+'\n'+html[end:]
html=html.replace("find('page-prev').onclick = () => { selectedItem = null; spread = Math.max(0,spread-1); render(); };", "find('page-prev').onclick = () => turnSpread(-1);")
html=html.replace("find('page-next').onclick = () => { selectedItem = null; spread = Math.min(Math.ceil(parts[part].pages.length/2)-1,spread+1); render(); };", "find('page-next').onclick = () => turnSpread(1);")
html=html.replace("text('날짜·전례력 자동 판별은 미구현입니다. 본문은 조판 위치를 보여주는 개발용 예시입니다. 실제 조판기는 이후 글자·화면 크기에 맞게 페이지를 나누고 문단 식별자로 위치를 복원해야 합니다.');", "text('공식 전례력·본문은 미연동입니다. 현재 검토 화면은 실제 표시 높이를 측정하여 예식 안에서 다음 페이지로 내용을 넘깁니다. 긴 본문은 계속 페이지로 분리하고, 악보는 카드 안에서 스크롤합니다. 극도로 작은 화면 등에서 제목·조작부조차 한 쪽에 들어가지 않는 예외에만 해당 페이지의 스크롤을 허용합니다.');")
html=html.replace("\ncontext(); render();", '''
let observedBookSize='';
if(typeof ResizeObserver!=='undefined')new ResizeObserver(entries=>{
 const rect=entries[0].contentRect;const size=`${Math.round(rect.width)}|${Math.round(rect.height)}`;
 if(size!==observedBookSize){observedBookSize=size;scheduleReflow();}
}).observe(find('book'));
window.addEventListener('resize',()=>scheduleReflow());
document.fonts?.ready.then(()=>scheduleReflow());
context(); render();''')
with (root/'review/02-ia-v10.html').open('w',encoding='utf-8',newline='\r\n') as f:f.write(html)
(root/'work/review-ia-v10-check.js').write_text(re.search(r'<script>(.*?)</script>',html,re.S).group(1),encoding='utf-8')
print('Created v10 measured page packing and independently scrolling score cards')
