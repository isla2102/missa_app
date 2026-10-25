from pathlib import Path
import json,re,zipfile,hashlib
root=Path('.').resolve();entries=json.loads(Path('work/catholic-enc-inventory.json').read_text(encoding='utf-8'));archive=Path('C:/Users/imsup/Downloads/가톨릭성가(ENC).zip');z=zipfile.ZipFile(archive)
out=Path('docs/references/catholic-enc');out.mkdir(exist_ok=True)
keys={'자비송':'자비송','대영광송':'대영광송','거룩하시도다':'거룩하시도다','신앙의 신비여':'신앙의신비여','아멘':'아멘','주님의 기도':'주님의기도','하느님의 어린양':'하느님의어린양','복음 환호송':'복음환호송'}
catalog={}
for key,token in keys.items():
 candidates=[]
 for e in entries:
  normalized=re.sub(r'\s+','',e['name'])
  if token not in normalized:continue
  m=re.match(r'(\d+)(?:-(\d+))?',e['name']);assert m
  nums=list(range(int(m[1]),int(m[2] or m[1])+1))
  name=Path(e['name']).name;target=(out/name).resolve();assert target.is_relative_to(out.resolve())
  data=z.read(e['originalName']);target.write_bytes(data)
  candidates.append({'numbers':nums,'file':name,'path':'../docs/references/catholic-enc/'+name,'sha256':hashlib.sha256(data).hexdigest(),'matchStatus':'title-only-not-melody-confirmed','officialPages':['https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex='+str(n) for n in nums]})
 catalog[key]={'title':key,'confirmedNumber':365 if key=='복음 환호송' else None,'matchStatus':'user-confirmed-and-16-note-melody-checked' if key=='복음 환호송' else 'unresolved','candidates':candidates}
catalog['주님의 기도 맺음 환호']={'title':'주님의 기도 맺음 환호','confirmedNumber':None,'matchStatus':'unresolved','candidates':catalog['주님의 기도']['candidates'],'note':'주님의 기도 항목에 수록된 맺음 환호가 같은 곡인지 추가 대조 필요'}
catalog['복음 환호송']['sourceUrl']='https://app.catholic.or.kr/web/sungga/default.asp?flag=5&sunggaId=365'
package={'archiveName':archive.name,'archiveSha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'entryCount':len(entries),'scope':'local source reference, no Encore binary rendering/conversion claim','scores':catalog}
Path('docs/references/score-source-catalog.json').write_text(json.dumps(package,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
p=Path('docs/교중미사악보/reengraved/registry.json');Path('scratch/score-registry.before-kyrie-doxology-365.json').write_bytes(p.read_bytes());registry=json.loads(p.read_text(encoding='utf-8'))
for title,key in [('자비송','kyrie'),('주님의 기도 맺음 환호','doxology'),('복음 환호송','alleluia-365')]:
 registry[title]=[{'kind':'engraved','title':title,'path':f'../docs/교중미사악보/reengraved/{key}.pdf','preview':f'../docs/교중미사악보/reengraved/{key}.svg','scope':'parish-common' if key=='alleluia-365' else 'principal','sourceKey':title,'status':'원본 대조 · 본당 최종 교정 전'}]
p.write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
print('Source catalog:',len(catalog),'score groups; registry:',list(registry))
