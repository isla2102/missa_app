from pathlib import Path
import re
s=Path('review/02-ia-v28.html').read_text(encoding='utf-8').replace('v28','v29')
s=s.replace("card.setAttribute('data-response-view',intercessionView);if(intercessionView", "card.setAttribute('data-response-view',intercessionView);if(intercessionView==='recite')card.className+=' reader__content-card--liturgy';if(intercessionView")
s=s.replace(' .reader__page--oversize {', ''' .reader__page--reading { display: flex; flex-direction: column; overflow: auto; }
 .reader__item--reading { flex: 1; min-block-size: 0; display: flex; flex-direction: column; }
 .reader__reading-content { flex: 1; min-block-size: 0; display: flex; flex-direction: column; }
 .reader__reading-liturgy { flex: 1; min-block-size: 0; display: flex; flex-direction: column; }
 .reader__reading-liturgy > * { flex-shrink: 0; }
 .reader__reading-body { flex: 1; min-block-size: 0; overflow: auto; }
 .reader__page--oversize {''',1)
s=s.replace(" if(block.alternative){const card=", """ if(['제1독서','제2독서'].includes(block.item?.title)){node.classList.add('reader__item--reading');node.querySelector('.reader__content-card')?.classList.add('reader__reading-content');const lit=node.querySelector('.reader__liturgy');lit?.classList.add('reader__reading-liturgy');Array.from(lit?.children||[]).filter(child=>child.getAttribute('data-speech-role')==='text').forEach(child=>child.classList.add('reader__reading-body'));}
 if(block.alternative){const card=""")
s=s.replace('function composePages() {',"""function readingPagePlan(blocks){if(blocks[0]?.item?.title==='제1독서' && blocks[1]?.item?.title==='화답송' && blocks[2]?.item?.title==='제2독서')return {leading:[{blocks:blocks.slice(0,2),oversize:false,reading:true},{blocks:blocks.slice(2,3),oversize:false,reading:true}],rest:blocks.slice(3)};return {leading:[],rest:blocks};}
function composePages() {""")
s=s.replace("try{return paginateFlow(flowBlocks(part),fits,split);}","try{const plan=readingPagePlan(flowBlocks(part));return [...plan.leading,...paginateFlow(plan.rest,fits,split)];}")
s=s.replace("page.className=layout.oversize?'reader__page reader__page--oversize':'reader__page';", "page.className=layout.reading?'reader__page reader__page--reading':layout.oversize?'reader__page reader__page--oversize':'reader__page';")
Path('review/02-ia-v29.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v29-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v28.cjs').read_text(encoding='utf-8').replace('02-ia-v28.html','02-ia-v29.html');Path('work/test-reader-v29.cjs').write_text(t,encoding='utf-8',newline='\r\n')
