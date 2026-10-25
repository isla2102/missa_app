from PIL import Image
from pathlib import Path
for n,box in [('04',(50,1250,2900,1750)),('07',(450,800,2600,1700))]:
 im=Image.open('work/music-inputs/score_'+n+'.png');im.crop(box).save('work/music-inputs/detail_'+n+'.png')
