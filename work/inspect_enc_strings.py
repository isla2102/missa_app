import zipfile,json,re
from pathlib import Path
z=zipfile.ZipFile('C:/Users/imsup/Downloads/가톨릭성가(ENC).zip');entries=json.loads(Path('work/catholic-enc-inventory.json').read_text(encoding='utf-8'))
for e in entries:
 if re.match(r'(306|310|315|320|325|318|323|387|388|377|380|383|386)\D',e['name']):
  b=z.read(e['originalName']);print(e['name'],b[:16].hex())
  chunks=re.findall(rb'[\x20-\x7e\xa1-\xfe]{5,}',b)
  texts=[]
  for ch in chunks:
   for enc in ['cp949','utf-8']:
    try:
     t=ch.decode(enc)
     if re.search('[가-힣]',t):texts.append(t)
     break
    except UnicodeError:pass
  print(texts[-25:])
