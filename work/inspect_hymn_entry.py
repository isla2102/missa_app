import urllib.request,re
from pathlib import Path
u='https://app.catholic.or.kr/web/sungga/default.asp?flag=5&sunggaId=1'
s=urllib.request.urlopen(u,timeout=25).read().decode('utf-8',errors='replace');Path('work/goodnews/app-1.html').write_text(s,encoding='utf-8')
for line in s.splitlines():
 if any(v in line.lower() for v in ['<img','sunggaid','수정','개정','악보','files/img','iframe']):print(line[:600])
