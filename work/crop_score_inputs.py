from pathlib import Path
from PIL import Image,ImageOps
import json
root=Path(__file__).resolve().parents[1]
src=root/'work/music-inputs';out=root/'work/music-omr-inputs';out.mkdir(parents=True,exist_ok=True)
plan=[
 ('01-kyrie','score_00',(0.12,0.13,0.94,0.91),'자비송'),
 ('02-gloria-a','score_01',(0.015,0.12,0.475,0.93),'대영광송 1'),
 ('03-gloria-b','score_01',(0.515,0.12,0.985,0.93),'대영광송 2'),
 ('04-gloria-c','score_02',(0.025,0.12,0.475,0.94),'대영광송 3'),
 ('05-gloria-d','score_02',(0.52,0.15,0.98,0.9),'대영광송 4'),
 ('06-sanctus','score_03',(0.02,0.16,0.48,0.93),'거룩하시도다'),
 ('07-memorial','score_03',(0.52,0.12,0.985,0.95),'신앙의 신비여'),
 ('08-amen','score_04',(0.02,0.15,0.98,0.48),'아멘'),
 ('09-lords-a','score_05',(0.12,0.14,0.94,0.96),'주님의 기도 1'),
 ('10-lords-b','score_06',(0.10,0.06,0.92,0.84),'주님의 기도 2'),
 ('11-doxology','score_07',(0.12,0.12,0.94,0.43),'주님의 기도 맺음 환호'),
 ('12-agnus','score_07',(0.12,0.45,0.94,0.94),'하느님의 어린양')]
records=[]
for key,source,rect,title in plan:
 image=Image.open(src/f'{source}.png').convert('L');w,h=image.size
 crop=image.crop(tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(rect)))
 crop=ImageOps.autocontrast(crop,cutoff=1)
 crop.save(out/f'{key}.tif',compression='tiff_lzw',dpi=(300,300))
 records.append({'key':key,'title':title,'source':source,'rect':rect,'size':crop.size})
with (out/'manifest.json').open('w',encoding='utf-8') as f:json.dump(records,f,ensure_ascii=False,indent=2)
print('Prepared',len(records),'analysis-only score sections')
