from PIL import Image
import numpy as np
im=np.array(Image.open('work/music-inputs/score_07.png').convert('L'))
for x in [700,730,760,800,900,1000,1300,1500]:
 a=im[700:1100,x-2:x+3].mean(1);indices=np.where(a<100)[0]+700;groups=[]
 for y in indices:
  if groups and y<=groups[-1][-1]+1:groups[-1].append(int(y))
  else:groups.append([int(y)])
 print(x,[(g[0],g[-1]) for g in groups])
