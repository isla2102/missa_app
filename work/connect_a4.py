from pathlib import Path
import json,re,shutil
base=Path('docs/교중미사악보/reengraved');p=base/'registry.json';shutil.copy2(p,'scratch/registry-before-a4.json');r=json.loads(p.read_text(encoding='utf-8'))
for assets in r.values():
 for a in assets:
  key=Path(a['path']).stem;a['path']='../'+(base/'print-a4'/(key+'.pdf')).as_posix();a['printSize']='A4 portrait 210 x 297 mm'
p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
s=Path('review/02-ia-v38.html').read_text(encoding='utf-8').replace('v38','v39');s=re.sub(r'const reengravedPrincipalScores = .*?;',lambda _:'const reengravedPrincipalScores = '+json.dumps(r,ensure_ascii=False)+';',s,count=1)
Path('review/02-ia-v39.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v39-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v38.cjs').read_text(encoding='utf-8').replace('02-ia-v38.html','02-ia-v39.html');Path('work/test-reader-v39.cjs').write_text(t,encoding='utf-8',newline='\r\n')
