from pathlib import Path
from PIL import Image,ImageOps
root=Path(__file__).resolve().parents[1]
source=root/'docs/교중미사악보'
out=root/'work/music-inputs';out.mkdir(parents=True,exist_ok=True)
for suffix,turn in [('',0),('_01',90),('_02',180),('_03',180),('_04',0),('_05',0),('_06',0),('_07',0)]:
 file=source/f'KakaoTalk_20261018_172809020{suffix}.jpg'
 image=ImageOps.exif_transpose(Image.open(file)).convert('RGB')
 if turn:image=image.rotate(turn,expand=True)
 name='score'+(suffix or '_00')
 # Analysis images only: original files remain untouched; no photographs enter the vector PDF.
 image.save(out/f'{name}.png')
 preview=image.copy();preview.thumbnail((1600,1600));preview.save(out/f'{name}-preview.jpg',quality=90)
 print(name,image.size)
