"""Import the six explicitly reviewed CBCK intercession pages; no date-range crawler."""
from pathlib import Path
from html.parser import HTMLParser
import re,json,hashlib,datetime,shutil,urllib.request,time
ROOT=Path(__file__).resolve().parents[1]
DATES=['2026-11-01','2026-11-02','2026-11-08','2026-11-15','2026-11-22','2026-11-29']
class Plain(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[]
 def handle_starttag(self,tag,attrs):
  if tag in ['br','p','div','h4','h5']:self.parts.append('\n')
 def handle_endtag(self,tag):
  if tag in ['p','div','h4','h5']:self.parts.append('\n')
 def handle_data(self,text):self.parts.append(text)
def parse_intercession(raw,date):
 html=raw.decode('utf-8-sig');date_text=re.search(r'<h2[^>]*>(.*?)</h2>',html,re.S)
 if not date_text:raise ValueError('date heading missing')
 d=Plain();d.feed(date_text[1]);match=re.search(r'(\d{4})년\s*(\d+)월\s*(\d+)일',''.join(d.parts))
 if not match or f'{match[1]}-{int(match[2]):02}-{int(match[3]):02}'!=date:raise ValueError('date mismatch')
 start=re.search(r'<h4[^>]*>\s*보편\s*지향\s*기도\s*</h4>',html)
 if not start:raise ValueError('section missing')
 stop=re.search(r'<h4\b',html[start.end():]);fragment=html[start.end():start.end()+stop.start()] if stop else html[start.end():]
 p=Plain();p.feed(fragment);lines=[t.strip() for t in ''.join(p.parts).splitlines() if t.strip()]
 numbers=[int(re.match(r'^(\d+)\.\s+',t)[1]) for t in lines if re.match(r'^\d+\.\s+',t)]
 if numbers!=[1,2,3,4]:raise ValueError('expected four ordered petitions')
 for i,line in enumerate(lines):
  if re.match(r'^\d+\.\s+',line) and (i+1>=len(lines) or re.match(r'^\d+\.\s+',lines[i+1])):raise ValueError('petition body missing')
 return lines

def encode(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
def main():
 folder=ROOT/'data/source-library/cbck-intercessions';folder.mkdir(exist_ok=True);sources=json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'));plans=[];report=[]
 for date in DATES:
  url='https://missa.cbck.or.kr/DailyMissa/'+date.replace('-','');file=folder/(date+'.html')
  if file.exists():raw=file.read_bytes()
  else:
   raw=urllib.request.urlopen(url,timeout=30).read();parse_intercession(raw,date);file.write_bytes(raw);time.sleep(.5)
  lines=parse_intercession(raw,date);ref='cbck-intercessions-'+date.replace('-','');sha=hashlib.sha256(raw).hexdigest();sources[ref]=dict(url=url,checkedAt='2026-10-24',sha256=sha,method='explicit-six-page-intercession-boundary-and-date-check',scope='local-test',rightsStatus='release-permission-deferred',note='굿뉴스 누락 지향 보완.사용자 요청한6일만 연결;정기 수집/주교회의 전체 출처 전환 아님.')
  path=ROOT/'data/days'/(date+'.json');doc=json.loads(path.read_text(encoding='utf-8'));old=[s for s in doc['sections'] if s['title']!='보편 지향 기도'];doc['sections']=old+[dict(id='intercessions',kind='intercession',title='보편 지향 기도',status='verified',paragraphs=[dict(id='intercessions-p'+str(i+1),role='guidance' if t.startswith('<') else 'text',text=t,sourceRef=ref) for i,t in enumerate(lines)])]
  if ref not in doc['sourceRefs']:doc['sourceRefs'].append(ref)
  plans.append((path,doc));report.append(dict(date=date,url=url,sha256=sha,petitions=4,unchangedOtherSectionsSha256=hashlib.sha256(encode(old)).hexdigest()))
 backup=ROOT/'scratch'/('cbck-intercessions-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir();shutil.copy2(ROOT/'data/sources.json',backup/'sources.json')
 for path,doc in plans:shutil.copy2(path,backup/path.name);path.write_bytes(encode(doc))
 (ROOT/'data/sources.json').write_bytes(encode(sources));(folder/'manifest.json').write_bytes(encode(dict(dates=report,count=6,petitions=24,scope='six reviewed date-default Masses only')));print('Linked 6 dates / 24 petitions, other sections preserved.')
if __name__=='__main__':main()
