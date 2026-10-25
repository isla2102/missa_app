from pathlib import Path
import urllib.request,concurrent.futures
urls={'copyright': 'https://www.cbck.or.kr/Copyright', 'cbck-dec': 'https://www.cbck.or.kr/Board/K7020/20262479', 'cbck-oct': 'https://www.cbck.or.kr/Board/K7020/20261395', 'daegu-view': 'https://maria.catholic.or.kr/jubo/jubo_view.asp?ju_no=9092'}
folder=Path('work/reference-research');folder.mkdir(exist_ok=True)
def fetch(item):
 key,url=item
 try:
  response=urllib.request.urlopen(url,timeout=30);raw=response.read();(folder/(key+'.html')).write_bytes(raw);print(key,len(raw),flush=True)
 except Exception as e:print(key,type(e).__name__,str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,urls.items()))
