from pathlib import Path
import sys,zlib,struct,re,json
sys.path.insert(0,'work/hwp-deps');import olefile
p=Path('C:/Users/imsup/Downloads/2026년 10월 성가표(수정보완판).hwp');ole=olefile.OleFileIO(str(p));print(ole.listdir());header=ole.openstream('FileHeader').read();compressed=bool(struct.unpack_from('<I',header,36)[0]&1);out=[]
for name in ole.listdir():
 if name[0]=='BodyText':
  data=ole.openstream(name).read();data=zlib.decompress(data,-15) if compressed else data;pos=0
  while pos+4<=len(data):
   v=struct.unpack_from('<I',data,pos)[0];pos+=4;tag=v&1023;size=v>>20
   if size==4095:size=struct.unpack_from('<I',data,pos)[0];pos+=4
   payload=data[pos:pos+size];pos+=size
   if tag==67:
    text=payload.decode('utf-16le','replace');text=re.sub('[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]','',text);out.append(text)
Path('work/reference-research/hymn-hwp.txt').write_text('\n'.join(out),encoding='utf-8')
print(json.dumps(out[:55],ensure_ascii=True))
from lxml import html
for name in ['cbck-monthly','daegu-list','ordinary','prayer-2','suwon-dec']:
 doc=html.fromstring(Path('work/reference-research/'+name+'.html').read_bytes().decode('utf-8','replace'))
 if name=='cbck-monthly':print(name,json.dumps([(a.get('href'),a.text_content().strip()) for a in doc.xpath('//a') if '2026' in a.text_content()][:15],ensure_ascii=True))
 elif name=='daegu-list':print(name,json.dumps([(a.get('href'),a.get('onclick'),a.text_content().strip()[:70]) for a in doc.xpath('//a') if '대구' in a.text_content()][:5],ensure_ascii=True))
 elif name=='ordinary': print(name,json.dumps([(e.tag,e.text_content().strip()[:70]) for e in doc.xpath('//h2|//h3|//h4')][-50:],ensure_ascii=True))
 elif name=='prayer-2':print(name,json.dumps(doc.text_content()[:2500],ensure_ascii=True))
 else:print(name,json.dumps([(a.get('href'),a.text_content().strip()) for a in doc.xpath('//a') if '.hwp' in (a.get('href','')+a.text_content())],ensure_ascii=True))
