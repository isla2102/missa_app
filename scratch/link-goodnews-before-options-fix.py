"""Merge cached GoodNews word liturgy into date documents; keep existing prayers/scores."""
from pathlib import Path
import datetime,hashlib,json,shutil,re
ROOT=Path(__file__).resolve().parents[1]
TYPES={'제1독서':('reading-1','reading'),'제2독서':('reading-2','reading'),'화답송':('psalm','psalm'),'복음 환호송':('alleluia','acclamation'),'복음':('gospel','gospel')}
def split_reading(lines,title):
    response='◎ 그리스도님, 찬미합니다.' if title=='복음' else '◎ 하느님, 감사합니다.'
    ends=[i for i,t in enumerate(lines) if t=='주님의 말씀입니다.']
    if not ends:raise ValueError('no reading closure')
    result=[];start=0
    for end in ends:
        if end+1>=len(lines) or lines[end+1]!=response:raise ValueError('closing response mismatch')
        chunk=lines[start:end+2]
        while chunk and chunk[0] in ['<또는>','또는']:chunk=chunk[1:]
        intro='전한 거룩한 복음' if title=='복음' else '▥'
        if not any(intro in t for t in chunk):raise ValueError('reading citation missing')
        result.append(chunk);start=end+2
    return result,lines[start:]
def bytes_json(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
def main():
    folder=ROOT/'data/source-library/goodnews-daily';manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));assert manifest['count']==92
    sources=json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'));plans=[];audit=[]
    for record in manifest['dates']:
        date=record['date'];raw=(folder/'html'/f'{date}.html').read_bytes();assert hashlib.sha256(raw).hexdigest()==record['sha256']
        parsed=json.loads((folder/'parsed'/f'{date}.json').read_text(encoding='utf-8'));assert parsed['date']==date
        path=ROOT/'data/days'/f'{date}.json';existing=path.exists()
        doc=json.loads(path.read_text(encoding='utf-8')) if existing else dict(schemaVersion=1,documentId='mass-'+date,date=date,observance=parsed['observance'].strip('[]'),sourceRefs=[],sections=[])
        ref='goodnews-'+date.replace('-','');sources[ref]=dict(url=parsed['url'],checkedAt=parsed['checkedAt'],method='cached-html-date-citation-and-boundary-validation',sha256=parsed['sha256'],scope='local-test',rightsStatus='release-permission-deferred',note='해당 날짜 한국어 기본 미사 페이지. 복수 본문은 본문1/본문2로 구분. 편집 지면·음악·다른 미사 양식 전체 검증 아님.')
        if ref not in doc['sourceRefs']:doc['sourceRefs'].append(ref)
        deferred={};counts={}
        for title,(sid,kind) in TYPES.items():
            doc['sections']=[s for s in doc['sections'] if s['title']!=title and not s['title'].startswith(title+' · 대안 ')]
            lines=parsed['sections'].get(title)
            if not lines:
                if title!='제2독서':raise ValueError('required section missing')
                doc['sections'].append(dict(id=sid,kind=kind,title=title,status='not-applicable',paragraphs=[]));continue
            variants,tail=split_reading(lines,title) if title in ['제1독서','제2독서','복음'] else ([lines],[])
            counts[title]=len(variants);deferred[title]=tail
            for i,variant in enumerate(variants):
                optionid=sid if i==0 else sid+'-option-'+str(i+1);optiontitle=title if i==0 else title+' · 대안 '+str(i+1)
                paragraphs=[]
                for j,line in enumerate(variant):
                    role='assembly' if line.startswith('◎') else 'lector' if line.startswith('▥') else 'priest' if line.startswith('✠') else 'guidance' if line.startswith('<또는') or line=='또는' else 'text'
                    paragraphs.append(dict(id=optionid+'-p'+str(j+1),role=role,text=line,sourceRef=ref))
                doc['sections'].append(dict(id=optionid,kind=kind,title=optiontitle,status='verified',paragraphs=paragraphs))
        # A new date's missing proper prayers stay explicit; GoodNews abbreviations are not expanded.
        for sid,title,kind in [('collect','본기도','prayer'),('offertory','예물 기도','prayer'),('postcommunion','영성체 후 기도','prayer'),('preface','감사송','preface'),('intercessions','보편 지향 기도','intercession')]:
            if not any(s['title']==title for s in doc['sections']):doc['sections'].append(dict(id=sid,kind=kind,title=title,status='missing',paragraphs=[]))
        assert len({s['id'] for s in doc['sections']})==len(doc['sections']),date
        plans.append((path,doc));audit.append(dict(date=date,sourceRef=ref,observance=parsed['observance'],variantCounts=counts,deferredNotes=deferred,secondReading='present' if '제2독서' in parsed['sections'] else 'not-applicable',existingPrayersPreserved=existing))
    backup=ROOT/'scratch'/('goodnews-link-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir()
    for path,doc in plans:
        if path.exists():shutil.copy2(path,backup/path.name)
        path.write_bytes(bytes_json(doc))
    for file in ['data/sources.json','prototype/source/build.json']:shutil.copy2(ROOT/file,backup/file.replace('/','__'))
    (ROOT/'data/sources.json').write_bytes(bytes_json(sources))
    config_path=ROOT/'prototype/source/build.json';config=json.loads(config_path.read_text(encoding='utf-8'));config['bindings']['dailyDocuments']={'paths':['data/days/'+record['date']+'.json' for record in manifest['dates']]};config_path.write_bytes(bytes_json(config))
    (folder/'link-audit.json').write_bytes(bytes_json(dict(count=len(plans),dates=audit)))
    print(json.dumps(dict(linked=len(plans),secondReadingAbsent=sum(x['secondReading']=='not-applicable' for x in audit),extraOptions=sum(sum(n-1 for n in x['variantCounts'].values()) for x in audit)),ensure_ascii=False))
if __name__=='__main__':main()
