from pathlib import Path
import urllib.request,concurrent.futures
urls={'ordinary':'https://maria.catholic.or.kr/mi_pr/missa/ordinary.asp?day=20261019&missaid=16875','jubo':'https://maria.catholic.or.kr/jubo/','prayer':'https://maria.catholic.or.kr/mi_pr/prayer/prayer.asp','hymn-post':'https://bbs.catholic.or.kr/pdsm/bbs_view.asp?num=6&id=212615&menu=4807'}
folder=Path('work/reference-research');folder.mkdir(exist_ok=True)
def fetch(item):
 key,url=item
 try:
  response=urllib.request.urlopen(url,timeout=30);raw=response.read();(folder/(key+'.html')).write_bytes(raw);print(key,len(raw),flush=True)
 except Exception as e:print(key,type(e).__name__,str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,urls.items()))
