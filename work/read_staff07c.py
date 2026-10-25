from PIL import Image
import numpy as np
im=np.array(Image.open('work/music-inputs/score_07.png').convert('L'))
for x in [770,870,880,980,1100,1220,1350,1470,1590,1710,1840,1960]:
 a=im[700:1100,x-2:x+3].mean(1);indices=np.where(a<180)[0]+700;groups=[]
 for y in indices:
  if groups and y<=groups[-1][-1]+1:groups[-1].append(int(y))
  else:groups.append([int(y)])
 print(x,[(g[0],g[-1]) for g in groups])


