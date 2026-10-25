from pathlib import Path
import re,xml.etree.ElementTree as E
base=Path('docs/교중미사악보/reengraved')
# Preserve the CSS selector scope AND materialize currentColor strokes for SVG consumers.
for key,parts in [('gloria',['gloria-a','gloria-b','gloria-c','gloria-d']),('lords-prayer',['lords-a','lords-b'])]:
 root=E.parse(base/(key+'.svg')).getroot()
 for i,(group,source) in enumerate(zip(root,parts)):
  original=E.parse(base/(source+'.svg')).getroot();group.set('id','p'+str(i)+'-'+original.get('id'))
  for n in group.iter():
   if n.tag.split('}')[-1] in ['path','ellipse','polygon','polyline','rect'] and n.get('stroke') is None:n.set('stroke','currentColor')
 E.ElementTree(root).write(base/(key+'-v26.svg'),encoding='utf-8',xml_declaration=True)
p=Path('review/02-ia-v25.html');s=p.read_text(encoding='utf-8').replace('v25','v26')
s=s.replace('/gloria.svg','/gloria-v26.svg').replace('/lords-prayer.svg','/lords-prayer-v26.svg')
s=s.replace('.reader__section-heading { grid-column: 1; grid-row: 1; display: flex; align-items: center; justify-content: space-between; gap: var(--draft-gap); }','.reader__section-heading { grid-column: 1; grid-row: 1; display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); align-items: center; gap: var(--draft-gap); }\n .reader__part-nav { display: contents; }\n .reader__part-prev { grid-column: 1; grid-row: 1; justify-self: start; }\n .reader__part-next { grid-column: 3; grid-row: 1; justify-self: end; }')
s=s.replace('.reader__title { margin: 0; }','.reader__title { margin: 0; grid-column: 2; grid-row: 1; text-align: center; }')
s=s.replace('.reader__tools { grid-column: 2; grid-row: 1;', '.reader__tools { grid-column: 2; grid-row: 3;')
s=s.replace('<nav class="reader__row" aria-label="미사 순서 이동"><button type="button" data-js="part-prev"></button><button type="button" data-js="part-next"></button>', '<nav class="reader__part-nav" aria-label="미사 순서 이동"><button type="button" class="reader__part-prev" data-js="part-prev"></button><button type="button" class="reader__part-next" data-js="part-next"></button>')
s=s.replace("card.append(p);}card.append(liturgyNode('◎ 주님, 저희의 기도를 들어주소서.'));", "card.append(p);}else card.append(liturgyNode('◎ 주님, 저희의 기도를 들어주소서.'));")
s=s.replace('◆ [독서자] 주님의 말씀입니다.', '◆ 주님의 말씀입니다.')
s=s.replace('assets[0].systems<=2', "(assets[0].systems<=2 || prayerId==='거룩하시도다')")
# Pair the closing dialogue as a single unsplittable grid within readings/gospel.
needle=" if(block.alternative){const card="
extra=""" if(['제1독서','제2독서','복음'].includes(block.item?.title)){const lit=node.querySelector('.reader__liturgy');if(lit){const children=Array.from(lit.children);children.forEach((child,i)=>{const next=children[i+1];if(child.textContent.includes('주님의 말씀입니다.') && next?.getAttribute('data-speech-role')==='assembly'){const pair=document.createElement('div');pair.className='reader__dialogue';lit.insertBefore(pair,child);pair.append(child,next);}});}}
"""
s=s.replace(needle,extra+needle)
# Every visible TOC entry is enclosed by a contiguous frame, preserving ordered-list semantics.
s=s.replace("const nav=find('toc-rail');const rail=nav.parentElement;", "const visibleIds=new Set(layouts.slice(spread*2,spread*2+2).flatMap(page=>page.blocks.map(block=>block.tocId)));const nav=find('toc-rail');const rail=nav.parentElement;")
s=s.replace("const li=document.createElement('li');const link=", "const li=document.createElement('li');const index=contents[partIndex].indexOf(entry);const isVisible=partIndex===part && visibleIds.has(entry.id);if(isVisible){li.className='reader__toc-visible';if(!visibleIds.has(contents[partIndex][index-1]?.id))li.className+=' reader__toc-visible--first';if(!visibleIds.has(contents[partIndex][index+1]?.id))li.className+=' reader__toc-visible--last';}const link=")
s=s.replace(' .reader__dialogue {', ' .reader__toc-visible { border-inline: var(--draft-response-border) solid; padding-inline: var(--draft-toc-gap); }\n .reader__toc-visible--first { border-block-start: var(--draft-response-border) solid; }\n .reader__toc-visible--last { border-block-end: var(--draft-response-border) solid; }\n .reader__dialogue {',1)
Path('review/02-ia-v26.html').write_text(s,encoding='utf-8',newline='\r\n')
Path('work/review-ia-v26-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
