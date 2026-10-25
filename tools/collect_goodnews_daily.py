"""Cache and parse explicitly requested GoodNews daily readings (2026 Q4).
No scripts are executed. A returned date mismatch or incomplete reading fails closed.
"""
from pathlib import Path
from html.parser import HTMLParser
import datetime,hashlib,json,re,time,urllib.parse,urllib.request
ROOT=Path(__file__).resolve().parents[1]
BASE='https://maria.catholic.or.kr/mi_pr/missa/missa.asp'
WANTED={'제1독서','제2독서','화답송','복음 환호송','복음'}
class Page(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.heading=None;self.htext=None;self.capture=None;self.depth=0;self.buf=[];self.sections={};self.date='';self.observance='';self.meta=None;self.meta_buf=[];self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);classes=a.get('class','').split()
  if tag=='a':self.links.append(a.get('href',''))
  if tag=='p' and ('today' in classes or 'm_t_today01' in classes):self.meta='date' if 'today' in classes else 'observance';self.meta_buf=[]
  if tag=='h3':self.htext=[]
  if tag=='div':
   if self.capture is not None:self.depth+=1
   elif self.heading and 'board_layout' in classes:self.capture=self.heading;self.depth=1;self.buf=[]
  if tag in ['br','p','li'] and self.capture is not None:self.buf.append('\n')
 def handle_endtag(self,tag):
  if tag=='h3' and self.htext is not None:self.heading=''.join(self.htext).strip();self.htext=None
  if tag=='p' and self.meta:
   text=''.join(self.meta_buf).strip()
   if self.meta=='date':self.date=text
   else:self.observance=text
   self.meta=None
  if tag=='div' and self.capture is not None:
   self.depth-=1
   if self.depth==0:
    text=''.join(self.buf).replace('\xa0',' ')
    lines=[line.strip() for line in text.splitlines() if line.strip()]
    if self.capture in self.sections:raise ValueError('duplicate section '+self.capture)
    self.sections[self.capture]=lines;self.capture=None;self.heading=None
 def handle_data(self,text):
  if self.htext is not None:self.htext.append(text)
  if self.meta:self.meta_buf.append(text)
  if self.capture is not None:self.buf.append(text)

def parse(data,date):
 p=Page();p.feed(data.decode('utf-8-sig'))
 match=re.search(r'(\d{4})년\s*(\d+)월\s*(\d+)일',p.date)
 if not match or '-'.join([match[1],match[2].zfill(2),match[3].zfill(2)])!=date:raise ValueError('returned date mismatch '+date+' '+p.date)
 for title in WANTED-{'제2독서'}:
  if not p.sections.get(title):raise ValueError('missing '+title+' '+date)
 for title in ['제1독서','제2독서','복음']:
  lines=p.sections.get(title)
  if not lines:continue
  if not any('주님의 말씀입니다.' in line for line in lines):raise ValueError('missing closing '+date+' '+title)
  if not any(('▥' if title!='복음' else '✠') in line or (title=='복음' and '전한 거룩한 복음' in line) for line in lines):raise ValueError('missing citation '+title)
 return p

def main():
 folder=ROOT/'data/source-library/goodnews-daily';(folder/'html').mkdir(parents=True,exist_ok=True);(folder/'parsed').mkdir(exist_ok=True)
 start=datetime.date(2026,10,1);end=datetime.date(2026,12,31);items=[]
 for offset in range((end-start).days+1):
  date=(start+datetime.timedelta(days=offset)).isoformat();url=BASE+'?'+urllib.parse.urlencode(dict(menu='missa',gomonth=date,missatype='DA'));path=folder/'html'/f'{date}.html'
  if path.exists():raw=path.read_bytes()
  else:
   request=urllib.request.Request(url,headers={'User-Agent':'MISSA-local-test/0.1 (user-requested date archive)'})
   raw=urllib.request.urlopen(request,timeout=40).read();parse(raw,date);path.write_bytes(raw);time.sleep(.5)
  page=parse(raw,date);sha=hashlib.sha256(raw).hexdigest();variants=[urllib.parse.urljoin(BASE,link) for link in page.links if 'missaid=' in link and 'gomonth='+date in link]
  result=dict(date=date,observance=page.observance,url=url,sha256=sha,checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),sections={title:page.sections[title] for title in WANTED if title in page.sections},availableLinks=sorted(set(variants)),status='parsed-date-and-boundaries-checked')
  (folder/'parsed'/f'{date}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  items.append(dict(date=date,observance=page.observance,sha256=sha,sections=list(result['sections']),alternatives={k:sum(line.startswith(('<또는','또는')) for line in v) for k,v in result['sections'].items() if any(line.startswith(('<또는','또는')) for line in v)}))
  if len(items)%10==0:print('Parsed '+str(len(items))+'/92 through '+date,flush=True)
 (folder/'manifest.json').write_text(json.dumps(dict(dates=items,count=len(items),scope='date-default Korean page; daily readings only; alternate source text preserved',copyright='release permission deferred; local testing'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('DONE '+str(len(items)),flush=True)
if __name__=='__main__':main()
