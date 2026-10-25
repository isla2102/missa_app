from pathlib import Path
import re
s=Path('review/02-ia-v30.html').read_text(encoding='utf-8').replace('v30','v31')
helper="""function sectionFlowKey(block){return block.prayerTitle?'prayer:'+block.prayerTitle:block.displayTitle?'section:'+block.displayTitle:block.tocId||block.key;}
function paginateSections(blocks,fits,split,offset=0){const groups=[];blocks.forEach(block=>{const key=sectionFlowKey(block);if(groups.at(-1)?.key===key)groups.at(-1).blocks.push(block);else groups.push({key,blocks:[block]});});const pages=[];groups.forEach(group=>{let section=paginateFlow(group.blocks,fits,split);if(section.length>2)section=[section[0],{blocks:section.slice(1).flatMap(page=>page.blocks),oversize:true}];if(section.length===2 && (offset+pages.length)%2===1)pages.push({blocks:[],oversize:false,blank:true});pages.push(...section);});return pages;}
"""
s=s.replace('function readingPagePlan(',helper+'function readingPagePlan(',1)
s=s.replace('...plan.leading,...paginateFlow(plan.rest,fits,split)','...plan.leading,...paginateSections(plan.rest,fits,split,plan.leading.length)')
s=s.replace("page.setAttribute('aria-label',`${parts[part].title} ${spread*2+index+1}쪽`);", "page.setAttribute('aria-label',layout.blank?'빈 페이지 · 다음 섹션은 다음 펼침에서 시작':`${parts[part].title} ${spread*2+index+1}쪽`);")
Path('review/02-ia-v31.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v31-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v30.cjs').read_text(encoding='utf-8').replace('02-ia-v30.html','02-ia-v31.html').replace('...plan.leading,...paginateFlow(plan.rest,fits,split)','...plan.leading,...paginateSections(plan.rest,fits,split,plan.leading.length)');Path('work/test-reader-v31.cjs').write_text(t,encoding='utf-8',newline='\r\n')
