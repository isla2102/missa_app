from pathlib import Path
import json,re,shutil,xml.etree.ElementTree as E
from pypdf import PdfReader
base=Path('docs/교중미사악보/reengraved');dest=base/'autofit';manifest=json.loads((dest/'manifest.json').read_text(encoding='utf-8'));lookup={x['key']:x for x in manifest}
# Small safety margin around the continuous preview, no page gaps.
for p in dest.glob('*.svg'):
 root=E.parse(p).getroot();margin=3*72/25.4;h=float(root.get('height'))
 for g in root:g.set('transform','translate(0 '+str(margin)+') '+g.get('transform',''))
 root.set('height',str(h+margin*2));root.set('viewBox',f'0 0 {root.get("width")} {h+margin*2}');E.ElementTree(root).write(p,encoding='utf-8',xml_declaration=True)
for x in manifest:
 pdf=PdfReader(dest/(x['key']+'.pdf'));x['pageHeightsMm']=[round(float(p.mediabox.height)*25.4/72,2) for p in pdf.pages]
 assert all(abs(float(p.mediabox.width)*25.4/72-297)<.01 for p in pdf.pages)
 sources={'gloria':['gloria-a','gloria-b','gloria-c','gloria-d'],'lords-prayer':['lords-a','lords-b']}.get(x['key'],[x['key']])
 def notes(path):return [E.tostring(n,encoding='unicode') for n in E.parse(path).getroot().findall('.//note')]
 old=[n for k in sources for n in notes(base/(k+'.musicxml'))];new=notes(dest/(x['key']+'.musicxml'));assert old==new,x['key']
 x['noteDataUnchanged']=True
(dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
rp=base/'registry.json';shutil.copy2(rp,'scratch/registry-before-autofit.json');r=json.loads(rp.read_text(encoding='utf-8'))
keys={'대영광송':'gloria','주님의 기도':'lords-prayer','아멘':'amen','자비송':'kyrie','주님의 기도 맺음 환호':'doxology','복음 환호송':'alleluia-365','하느님의 어린양':'agnus','거룩하시도다':'sanctus'}
for title,assets in r.items():
 for a in assets:
  key='memorial-'+a['season'] if title=='신앙의 신비여' else keys[title]
  a['preview']='../'+(dest/(key+'.svg')).as_posix();a['path']='../'+(dest/(key+'.pdf')).as_posix();a['systems']=lookup[key]['systems'];a['layout']='297mm-width-autofit-role-systems'
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
s=Path('review/02-ia-v35.html').read_text(encoding='utf-8').replace('v35','v36');s=re.sub(r'const reengravedPrincipalScores = .*?;',lambda _: 'const reengravedPrincipalScores = '+json.dumps(r,ensure_ascii=False)+';',s,count=1)
sizes={}
for p in base.rglob('*.svg'):
 root=E.parse(p).getroot();w=root.get('width','').removesuffix('px');h=root.get('height','').removesuffix('px')
 if w and h:sizes['../'+p.as_posix()]=[float(w),float(h)]
s=re.sub(r'const scorePreviewSizes=.*?;',lambda _:'const scorePreviewSizes='+json.dumps(sizes,ensure_ascii=False)+';',s,count=1)
Path('review/02-ia-v36.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v36-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v35.cjs').read_text(encoding='utf-8').replace('02-ia-v35.html','02-ia-v36.html');Path('work/test-reader-v36.cjs').write_text(t,encoding='utf-8',newline='\r\n')
print('PASS: all 11 score variants preserve exact note XML; PDFs 297mm wide; registry and previews connected.')
