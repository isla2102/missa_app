from pathlib import Path
import urllib.request,re
p=Path('work/goodnews');p.mkdir(exist_ok=True)
u='https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex=320'
b=urllib.request.urlopen(u,timeout=30).read();s=b.decode('euc-kr',errors='replace');(p/'320.html').write_text(s,encoding='utf-8')
for line in s.splitlines():
 if any(w in line.lower() for w in ['.mid','.nwc','2012040320','download(','filedown']):print(line.strip()[:800])
