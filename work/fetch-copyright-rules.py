from pathlib import Path
import urllib.request,concurrent.futures
urls={'copyright-rules':'https://www.cbck.or.kr/Board/K7300/20230535'}
folder=Path('work/reference-research');folder.mkdir(exist_ok=True)
def fetch(item):
 key,url=item
 try:
  response=urllib.request.urlopen(url,timeout=30);raw=response.read();(folder/(key+'.html')).write_bytes(raw);print(key,len(raw),flush=True)
 except Exception as e:print(key,type(e).__name__,str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,urls.items()))
