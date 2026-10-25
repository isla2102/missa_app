from pathlib import Path
import sys,struct,zlib,json
sys.path.insert(0,'work/hwp-deps');import olefile
o=olefile.OleFileIO('C:/Users/imsup/Downloads/2026년 10월 성가표(수정보완판).hwp');b=zlib.decompress(o.openstream('BodyText/Section0').read(),-15);i=0;cells=[];current=None
while i+4<=len(b):
 v=struct.unpack_from('<I',b,i)[0];i+=4;tag=v&1023;level=(v>>10)&1023;n=v>>20
 if n==4095:n=struct.unpack_from('<I',b,i)[0];i+=4
 p=b[i:i+n];i+=n
 if tag==72 and len(p)>=30:
  col,row,cs,rs=struct.unpack_from('<HHHH',p,8);current={'col':col,'row':row,'colspan':cs,'rowspan':rs,'text':[]};cells.append(current)
 if tag==67 and current:
  # HWP extended controls occupy eight UTF-16 code units including marker.
  chars=[];pos=0
  while pos+2<=len(p):
   code=struct.unpack_from('<H',p,pos)[0]
   if code in [1,2,3,11,12,14,15,16,17,18,21,22,23]:pos+=16;continue
   if code>=32 or code in [9,10,13]:chars.append(chr(code))
   pos+=2
  current['text'].append(''.join(chars).strip())
for c in cells:c['text']='\n'.join(t for t in c['text'] if t)
Path('work/reference-research/hymn-cells.json').write_text(json.dumps(cells,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(cells[:24],ensure_ascii=True))
