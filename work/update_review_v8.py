from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
html=(root/'review/02-ia-v7.html').read_text(encoding='utf-8').replace('검토 v7','검토 v8')
html=html.replace('--draft-score-height: 3rem;', '--draft-rail-max: 16rem; --draft-score-height: 3rem;')
html=html.replace(' .reader__body { min-height: 0;', ''' .reader__workspace { min-height: 0; display: grid; grid-template-columns: minmax(0, 1fr) fit-content(var(--draft-rail-max)); gap: var(--draft-gap); }
 .reader__rail { min-height: 0; max-width: min(var(--draft-rail-max), 28vw); overflow: auto; overflow-wrap: anywhere; border-inline-start: 1px solid; padding-inline-start: var(--draft-gap); }
 .reader__rail-title { margin: 0 0 var(--draft-gap); }
 .reader__toc-group-title { margin-block: var(--draft-gap) var(--draft-toc-gap); }
 .reader__toc-list { margin-block: 0; padding-inline-start: var(--draft-padding); }
 .reader__body { min-width: 0; min-height: 0;''')
html=html.replace(' .reader__prayer-option { display: block;', ' .reader__prayer-option { display: flex; flex-wrap: wrap; gap: var(--draft-toc-gap);')
html=html.replace(' .reader__toc-link {', ' .reader__prayer-button[aria-pressed="true"] { font-weight: bold; text-decoration: underline; }\n .reader__toc-link {')
html=html.replace('<section class="reader__body"', '<div class="reader__workspace"><section class="reader__body"',1)
html=html.replace('<button type="button" data-panel="toc"><span aria-hidden="true">☷</span> 목차</button>','')
html=html.replace('</section>\n<footer class="reader__footer">','</section>\n<aside class="reader__rail" aria-labelledby="rail-title"><h2 class="reader__rail-title" id="rail-title"><span aria-hidden="true">☷</span> 목차</h2><nav data-js="toc-rail" aria-label="미사 전체 세부 목차"></nav></aside></div>\n<footer class="reader__footer">',1)
start=html.index("   const label = document.createElement('label'); label.className = 'reader__prayer-option';")
end=html.index('\n  }\n  const p = ',start)
html=html[:start]+'''   const group = document.createElement('div'); group.className = 'reader__prayer-option'; group.setAttribute('role','group'); group.setAttribute('aria-label',`${title} 표시 방식`);
   [['recite','낭송 · 본문'],['chant','성가 · 악보']].forEach(([value,text])=>{
    const button=document.createElement('button');button.type='button';button.className='reader__prayer-button';button.textContent=text;
    button.setAttribute('aria-pressed',String(mode===value));button.setAttribute('data-prayer-mode',value);
    button.onclick=()=>{parishPrayerPresentation[prayerId]=value;fill();card.querySelector(`[data-prayer-mode="${value}"]`)?.focus();};group.append(button);
   });card.append(group);'''+html[end:]
html=html.replace(" render(); find('drawer').close();", " render(); const target=document.getElementById(item.id);target?.focus({preventScroll:true});target?.scrollIntoView({block:'nearest',inline:'nearest'});")
start=html.index(" if (which === 'toc') {")
end=html.index(" if (which === 'hymn')",start)
html=html[:start]+html[end:]
rail='''function renderToc() {
 const nav=find('toc-rail');const rail=nav.parentElement;const previousScroll=rail.scrollTop;nav.replaceChildren();
 parts.forEach((item,partIndex)=>{
  const group=document.createElement('section');const heading=document.createElement('h3');heading.className='reader__toc-group-title';heading.textContent=item.title;
  const list=document.createElement('ol');list.className='reader__toc-list';
  contents[partIndex].forEach(entry=>{
   const li=document.createElement('li');const link=document.createElement('a');link.className='reader__toc-link';link.href=`#${entry.id}`;link.textContent=entry.title;
   if(entry.id===selectedItem){link.setAttribute('aria-current','location');link.setAttribute('aria-label',`${entry.title} · 현재 위치`);}
   link.onclick=event=>{event.preventDefault();jumpToItem(partIndex,entry);};li.append(link);list.append(li);
  });group.append(heading,list);nav.append(group);
 });rail.scrollTop=previousScroll;
}
'''
html=html.replace('function render() {',rail+'\nfunction render() {')
html=html.replace(' position[part] = spread;',' position[part] = spread; renderToc();')
html=html.replace("text('목차 제안 A: 우측 Drawer(현재 체험). 대안 B: 목차 상시 고정(본문 가용 폭 감소). 두 페이지 공간을 확보하는 A를 추천합니다.');", "text('목차는 뷰어 오른쪽 상시 레일입니다. 안내 문구 없이 세부 링크와 현재 위치를 표시합니다. 성가·기도문·보기 설정·안내는 보조 Drawer를 유지합니다.');")
with (root/'review/02-ia-v8.html').open('w',encoding='utf-8',newline='\r\n') as f:f.write(html)
(root/'work/review-ia-v8-check.js').write_text(re.search(r'<script>(.*?)</script>',html,re.S).group(1),encoding='utf-8')
print('Created v8 permanent TOC rail and prayer mode buttons')
