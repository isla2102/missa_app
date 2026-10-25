from pathlib import Path
import zipfile,json
p=Path('C:/Users/imsup/Downloads/가톨릭성가(ENC).zip');z=zipfile.ZipFile(p)
entries=[]
for i in z.infolist():
 name=i.filename
 if not (i.flag_bits&0x800):
  try:name=name.encode('cp437').decode('cp949')
  except (UnicodeError,LookupError):pass
 entries.append({'name':name,'originalName':i.filename,'size':i.file_size,'directory':i.is_dir()})
Path('work/catholic-enc-inventory.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
print('Entries',len(entries),'bytes',sum(x['size'] for x in entries))
for e in entries:
 if any(t in e['name'] for t in ['자비','대영광','거룩','신비','아멘','주님의','어린양']):print(e['name'])
print('FIRST',repr(entries[:10]))
