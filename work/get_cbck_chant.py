import urllib.request,re
from pathlib import Path
s=urllib.request.urlopen('https://missale.cbck.or.kr/Sound').read().decode()
Path('work/gregorian/cbck-sound.html').write_text(s,encoding='utf-8')
for line in s.splitlines():
 if any(x in line for x in ['대영광송','거룩하시도다','신앙의 신비여','하느님의 어린양','pdf','function Play','function play']): print(line[:700])
