from pathlib import Path
import xml.etree.ElementTree as E,re,json,shutil
assets=Path('docs/교중미사악보/reengraved')
def merge_svg(keys,outkey):
 root=E.Element('svg',xmlns='http://www.w3.org/2000/svg',width='1050',height='1',viewBox='0 0 1050 1');y=0
 for i,key in enumerate(keys):
  text=(assets/(key+'.svg')).read_text(encoding='utf-8');tree=E.fromstring(text);ids=[n.get('id') for n in tree.iter() if n.get('id')]
  for id in sorted(ids,key=len,reverse=True):text=text.replace('"'+id+'"','"p'+str(i)+'-'+id+'"').replace('#'+id+'"','#p'+str(i)+'-'+id+'"').replace('#'+id+')','#p'+str(i)+'-'+id+')')
  tree=E.fromstring(text);height=float(tree.get('height').removesuffix('px'))
  group=E.Element('g',transform='translate(0 '+str(y)+')')
  for child in tree:
   if child.tag.endswith('}svg'):
    vb=[float(x) for x in child.get('viewBox').split()]
    child.tag='{http://www.w3.org/2000/svg}g';child.attrib.clear();child.set('transform','scale('+str(1050/vb[2])+')')
   group.append(child)
  root.append(group);y+=height+20
 root.set('height',str(y-20));root.set('viewBox','0 0 1050 '+str(y-20));(assets/(outkey+'.svg')).write_text(E.tostring(root,encoding='unicode'),encoding='utf-8')
merge_svg(['gloria-a','gloria-b','gloria-c','gloria-d'],'gloria');merge_svg(['lords-a','lords-b'],'lords-prayer')
shutil.copy2('output/pdf/gloria-reengraved.pdf',assets/'gloria.pdf');shutil.copy2('output/pdf/lords-prayer-reengraved.pdf',assets/'lords-prayer.pdf')
p=assets/'registry.json';shutil.copy2(p,'scratch/registry.before-v25.json');r=json.loads(p.read_text(encoding='utf-8'))
def entry(key,title,systems,**kw):return {'kind':'engraved','title':title,'path':'../docs/교중미사악보/reengraved/'+key+'.pdf','preview':'../docs/교중미사악보/reengraved/'+key+'.svg','scope':'principal','sourceKey':title.split(' · ')[0],'systems':systems,'status':'사진 대조 · 본당 최종 교정 전',**kw}
r['대영광송']=[entry('gloria','대영광송',23)];r['주님의 기도']=[entry('lords-prayer','주님의 기도',10)];r['거룩하시도다']=[entry('sanctus','거룩하시도다',5)];r['신앙의 신비여']=[entry('memorial-'+season,'신앙의 신비여 · '+label,2,season=season) for season,label in [('ordinary','연중'),('lent','사순'),('easter','부활')]]
for key,number in [('아멘',1),('주님의 기도 맺음 환호',2),('복음 환호송',1),('하느님의 어린양',6),('자비송',6)]:
 for a in r[key]:a['systems']=number
p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
p=Path('review/02-ia-v25.html');s=p.read_text(encoding='utf-8');s=re.sub(r'const reengravedPrincipalScores = .*?;',lambda m:'const reengravedPrincipalScores = '+json.dumps(r,ensure_ascii=False)+';',s,count=1)
old="if(prayerId==='신앙의 신비여'){const response=memorialResponse();return find('slot')"
if old in s:
 a=s.index(old,s.index('function scoreAssets'));b=s.index('return (prayerId',a)
 s=s[:a]+"if(prayerId==='신앙의 신비여'){const season=currentSeason()?.key;return find('slot').value==='main' && season?(reengravedPrincipalScores[prayerId]||[]).filter(asset=>asset.season===season):[];}"+s[b:]
s=s.replace("const compactScore=prayerId==='주님의 기도 맺음 환호';", "const compactScore=assets.length===1 && assets[0].systems>0 && assets[0].systems<=2;")
s=s.replace('min(100%, 12rem)', 'min(100%, var(--draft-dialogue-width))')
p.write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v25-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
from pypdf import PdfWriter
writer=PdfWriter()
for key in ['gloria','sanctus','memorial-ordinary','memorial-lent','memorial-easter']:
 writer.append(str(assets/(key+'.pdf')))
with Path('output/pdf/remaining-scores-reengraved.pdf').open('wb') as f:writer.write(f)
