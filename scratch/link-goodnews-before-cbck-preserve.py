from pathlib import Path
import sys,json,re,shutil,datetime
from collect_goodnews_daily import parse
ROOT=Path(__file__).resolve().parents[1]
def main():
 backup=ROOT/'scratch'/('intercession-link-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir();audit=[];plans=[]
 for path in sorted((ROOT/'data/days').glob('*.json')):
  page=parse((ROOT/'data/source-library/goodnews-daily/html'/path.name.replace('.json','.html')).read_bytes(),path.stem);lines=next((v for k,v in page.sections.items() if re.sub(r'\s','',k)=='보편지향기도'),None)
  if not lines:audit.append(dict(date=path.stem,status='absent',petitions=0));continue
  numbers=[int(re.match(r'^(\d+)\.',t)[1]) for t in lines if re.match(r'^\d+\. ',t)]
  if numbers and numbers!=[1,2,3,4]:raise ValueError('unexpected petition order '+path.stem)
  ref='goodnews-'+path.stem.replace('-','');doc=json.loads(path.read_text(encoding='utf-8'));doc['sections']=[s for s in doc['sections'] if s['title']!='보편 지향 기도'];doc['sections'].append(dict(id='intercessions',kind='intercession',title='보편 지향 기도',status='verified' if numbers else 'needs-review',paragraphs=[dict(id='intercessions-p'+str(i+1),role='guidance' if t.startswith('<') else 'text',text=t,sourceRef=ref) for i,t in enumerate(lines)]));plans.append((path,doc));audit.append(dict(date=path.stem,status='linked' if numbers else 'note-only',petitions=len(numbers),sourceRef=ref))
 for path,doc in plans:
  shutil.copy2(path,backup/path.name);path.write_bytes((json.dumps(doc,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8'))
 report=dict(dates=audit,linkedDates=sum(x['status']=='linked' for x in audit),noteOnlyDates=sum(x['status']=='note-only' for x in audit),petitions=sum(x['petitions'] for x in audit),scope='available sample petitions; source gives no priest conclusion')
 (ROOT/'data/source-library/goodnews-daily/intercession-audit.json').write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8'));print(json.dumps({k:v for k,v in report.items() if k!='dates'},ensure_ascii=False))
if __name__=='__main__':main()
