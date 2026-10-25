from pathlib import Path
import re,json,xml.etree.ElementTree as E
sizes={}
for p in Path('docs/교중미사악보/reengraved').glob('*.svg'):
 root=E.parse(p).getroot();w=root.get('width','').removesuffix('px');h=root.get('height','').removesuffix('px')
 if w and h:sizes['../'+p.as_posix()]=[float(w),float(h)]
s=Path('review/02-ia-v27.html').read_text(encoding='utf-8').replace('v27','v28')
s=s.replace('function renderPhoto(asset,enlarged=false){','const scorePreviewSizes='+json.dumps(sizes,ensure_ascii=False)+';\nfunction renderPhoto(asset,enlarged=false){')
s=s.replace("preview.className='reader__score-photo';preview.src=", "preview.className='reader__score-photo';const dimensions=scorePreviewSizes[asset.preview||asset.path];if(dimensions){preview.setAttribute('width',String(dimensions[0]));preview.setAttribute('height',String(dimensions[1]));}preview.src=")
old="find('page-next').setAttribute('aria-label',turn.nextPart?parts[part+1].title+'의 첫 두 페이지로 이동':'뒤쪽 두 페이지');find('page-prev').setAttribute('aria-label',turn.previousPart?parts[part-1].title+'의 마지막 두 페이지로 이동':'앞쪽 두 페이지');"
new="const previousLabel=turnDestination(-1),nextLabel=turnDestination(1);find('page-prev').textContent='← '+previousLabel;find('page-next').textContent=nextLabel+' →';find('page-prev').setAttribute('aria-label',previousLabel+'로 이동');find('page-next').setAttribute('aria-label',nextLabel+'로 이동');"
assert old in s;s=s.replace(old,new)
helper="""function flowBlockTitle(block,partIndex=part){const title=block.displayTitle||block.prayerTitle||block.variant?.title||block.item?.title||contents[partIndex].find(item=>item.id===block.tocId)?.title||parts[partIndex].title;return title+(block.acclamationPart==='last'?' · 합송':block.acclamationPart==='choir'?' · 성가대':block.continued?' (계속)':'');}
function turnDestination(direction){const target=layouts[(spread+direction)*2];if(target?.blocks.length)return flowBlockTitle(target.blocks[0]);const index=part+direction;if(index<0)return '미사 시작';if(index>=parts.length)return '미사 마침';const item=direction<0?contents[index].at(-1):contents[index][0];return parts[index].title+' · '+item.title;}
"""
s=s.replace('function pageTurnState(',helper+'function pageTurnState(',1)
Path('review/02-ia-v28.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v28-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v27.cjs').read_text(encoding='utf-8').replace('02-ia-v27.html','02-ia-v28.html');Path('work/test-reader-v28.cjs').write_text(t,encoding='utf-8',newline='\r\n')
