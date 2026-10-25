import urllib.request,json,concurrent.futures
from pathlib import Path
rows=json.loads(Path('work/gregorian/list.json').read_text())
def get(row):
 i,n=row;p=Path('work/gregorian')/(i+'.gabc')
 if p.exists():return
 try:p.write_bytes(urllib.request.urlopen('https://gregobase.selapa.net/download.php?elem=1&format=gabc&id='+i,timeout=25).read())
 except Exception as e:print(i,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:list(ex.map(get,rows))
print('GABC downloaded',len(list(Path('work/gregorian').glob('*.gabc'))))
