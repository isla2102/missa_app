from pathlib import Path
import urllib.request,re,json,concurrent.futures,time
out=Path('work/goodnews');out.mkdir(exist_ok=True)
nums=[306,310,315,320,325,350,354,307,311,316,321,326,308,312,317,322,327,333,341,348,351,357,309,313,319,324,328,335,343,352,358,314,373,374,375,376,*range(377,387),318,323,387,388]
def fetch(n):
 try:
  page=f'https://maria.catholic.or.kr/sungga/search/sungga_view.asp?ctxtIndex={n}'
  b=urllib.request.urlopen(page,timeout=25).read();s=b.decode('utf-8',errors='replace');(out/f'{n}.html').write_text(s,encoding='utf-8')
  m=re.search(r"viewFile\('([^']+)','mid'",s)
  if not m:return {'number':n,'status':'no-midi','page':page}
  u='https://maria.catholic.or.kr/sungga/download.asp?strFileID='+m.group(1)+'&FileType=mid'
  r=urllib.request.urlopen(u,timeout=25);data=r.read()
  if data[:4]!=b'MThd':return {'number':n,'status':'not-midi','page':page,'url':u}
  (out/f'{n}.mid').write_bytes(data);return {'number':n,'status':'downloaded','page':page,'url':u,'bytes':len(data)}
 except Exception as e:return {'number':n,'status':'error','error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(fetch,nums))
(out/'sources.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');print({s:sum(r['status']==s for r in results) for s in set(r['status'] for r in results)})
