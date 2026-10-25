from pathlib import Path
import sys
sys.path.insert(0,'work/music-deps')
from PIL import Image,ImageOps
for i,name in enumerate(['KakaoTalk_20261018_195716437.jpg','KakaoTalk_20261018_195716437_01.jpg']):
 im=ImageOps.exif_transpose(Image.open(Path('C:/Users/imsup/Downloads')/name));im=im.rotate(90,expand=True);im.thumbnail((1600,1600));im.save('work/new-score-'+str(i)+'.png')
