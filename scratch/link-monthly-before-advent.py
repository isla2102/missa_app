"""Link the approved October proper-prayer batch from local HWP records.
Never replaces existing day documents; never synthesizes readings or selects variants.
"""
from pathlib import Path
import calendar,collections,datetime,hashlib,json,re,shutil
ROOT=Path(__file__).resolve().parents[1]
PRAYERS={'본기도':'collect','예물 기도':'offertory','영성체 후 기도':'postcommunion'}
ANTIPHONS={'입당송':'entrance-antiphon','영성체송':'communion-antiphon'}
END=re.compile(r'(?:비나이다|다스리시나이다)\.$')

def split_prayer(rows):
    ends=[i for i,p in enumerate(rows) if END.search(p['text'])]
    if len(ends)!=1:raise ValueError('expected exactly one prayer ending')
    body,tail=rows[:ends[0]+1],rows[ends[0]+1:]
    if any(p['text'].startswith(('<','감사송','또는')) for p in body):raise ValueError('instruction/alternative inside prayer')
    if tail and not tail[0]['text'].startswith(('<','감사송')):raise ValueError('unknown trailing content')
    return body,tail

def split_antiphon(rows):
    if not rows:raise ValueError('empty antiphon')
    if rows[-1]['text']=='<대영광송>':return rows[:-1],rows[-1:]
    if any(p['text'].startswith('<') for p in rows):raise ValueError('unreviewed antiphon instruction')
    return rows,[]

def group_observance(group):
    texts=[]
    for row in group['paragraphs'][1:]:
        text=row['text']
        if any(text.startswith(t) for t in [*PRAYERS,*ANTIPHONS]):break
        if text not in ['백','녹','홍','자','장미','흑']:texts.append(text)
    if not texts:raise ValueError('missing observance')
    return ' · '.join(texts)

def serialize(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')

def main():
    month=10;year=2026;source_path=next((ROOT/'data/source-library/extracted-hwp').glob('*202610_*.json'))
    source=json.loads(source_path.read_text(encoding='utf-8'))
    original=ROOT/source['sourcePath'];assert hashlib.sha256(original.read_bytes()).hexdigest()==source['sha256'],'source changed'
    inventory=json.loads((ROOT/'data/source-library/inventory.json').read_text(encoding='utf-8'))
    assert next(x['sha256'] for x in inventory['originalFiles'] if x['libraryPath']==source['sourcePath'])==source['sha256']
    groups=source['dates'];counts=collections.Counter(g['date'] for g in groups)
    expected={f'{year}-{month:02}-{d:02}' for d in range(1,calendar.monthrange(year,month)[1]+1)}
    assert set(counts)==expected and all(n==1 for n in counts.values()),'missing/ambiguous dates'
    ref='user-hwp-202610';planned=[];audit=[]
    for group in groups:
        date=group['date'];path=ROOT/'data/days'/f'{date}.json'
        if path.exists():
            audit.append(dict(date=date,status='existing-preserved',sha256=hashlib.sha256(path.read_bytes()).hexdigest()));continue
        titles=[s['title'] for s in group['sections']]
        assert len(titles)==5 and set(titles)==set(PRAYERS)|set(ANTIPHONS),date+' headings'
        sections=[];trace=[]
        for section in group['sections']:
            title=section['title'];sid=(PRAYERS|ANTIPHONS)[title]
            body,tail=split_prayer(section['paragraphs']) if title in PRAYERS else split_antiphon(section['paragraphs'])
            if not body:raise ValueError('empty section '+date+' '+title)
            text='\n'.join(p['text'] for p in body)
            sections.append(dict(id=sid,kind='prayer' if title in PRAYERS else 'antiphon',title=title,status='verified',paragraphs=[dict(id=sid+'-p1',role='priest' if title in PRAYERS else 'text',text=text,sourceRef=ref)]))
            trace.append(dict(title=title,sourceHeading=section['heading'],bodyRecords=body,deferredFollowingRecords=tail,textSha256=hashlib.sha256(text.encode('utf-8')).hexdigest()))
        for sid,title,kind in [('reading-1','제1독서','reading'),('psalm','화답송','psalm'),('reading-2','제2독서','reading'),('alleluia','복음 환호송','acclamation'),('gospel','복음','gospel'),('preface','감사송','preface'),('intercessions','보편 지향 기도','intercession')]:
            sections.append(dict(id=sid,kind=kind,title=title,status='missing',paragraphs=[]))
        doc=dict(schemaVersion=1,documentId='mass-'+date,date=date,observance=group_observance(group),sourceRefs=[ref],sections=sections)
        planned.append((path,doc));audit.append(dict(date=date,status='linked-propers-only',sections=trace))
    if not planned:
        print(json.dumps(dict(newDocuments=0,totalDates=len(groups),status='already-linked; original audit retained')))
        return
    # Validate the entire batch before any write. The baseline is read, never rewritten.
    backup=ROOT/'scratch'/('october-batch-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir()
    config_path=ROOT/'prototype/source/build.json';shutil.copy2(config_path,backup/'build.json')
    for path,doc in planned:path.write_bytes(serialize(doc))
    config=json.loads(config_path.read_text(encoding='utf-8'))
    config['bindings']['dailyDocuments']={'paths':[f'data/days/{date}.json' for date in sorted(expected)]}
    config_path.write_bytes(serialize(config))
    report=dict(month='2026-10',sourcePath=source['sourcePath'],sha256=source['sha256'],newDocuments=len(planned),totalDates=len(groups),verification='HWP record text, explicit headings, unique prayer ending and date boundaries; not full visual proofreading',entries=audit)
    (ROOT/'data/source-library/extracted-hwp/link-audit-202610.json').write_bytes(serialize(report))
    print(json.dumps(dict(newDocuments=len(planned),totalDates=len(groups),preserved=sum(x['status']=='existing-preserved' for x in audit)),ensure_ascii=False))
if __name__=='__main__':main()
