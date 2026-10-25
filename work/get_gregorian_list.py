import urllib.request,re,json
from pathlib import Path
u='https://gregobase.selapa.net/usage.php?id=ky'
h=urllib.request.urlopen(u).read().decode();rows=re.findall(r'<a[^>]+href="chant.php\?id=(\d+)"[^>]*>(.*?)</a>',h)
rows=[(i,re.sub('<.*?>','',n)) for i,n in rows if re.match(r'(Gloria|Sanctus|Agnus)',n)]
Path('work/gregorian').mkdir(exist_ok=True)
Path('work/gregorian/list.json').write_text(json.dumps(rows),encoding='utf-8')
print(len(rows), rows[:4])
