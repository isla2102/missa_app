"""Link November/December HWP propers matching the cached GoodNews default Mass.
Other HWP forms remain separately archived, never assigned by parish session.
"""
from pathlib import Path
import collections,datetime,hashlib,json,re,shutil
from collect_goodnews_daily import parse
from link_monthly_propers import PRAYERS,ANTIPHONS,split_prayer,split_antiphon
ROOT=Path(__file__).resolve().parents[1]
TOKENS=['첫째 미사','둘째 미사','셋째 미사','전야 미사','밤 미사','새벽 미사','낮 미사']
def form_label(group):
    texts=[]
    for row in group['paragraphs'][1:]:
        if any(row['text'].startswith(t) for t in [*PRAYERS,*ANTIPHONS]):break
        texts.append(row['text'])
    return ' '.join(texts)
def choose_group(groups,observance):
    candidates=[g for g in groups if g['sections']]
    if not candidates:raise ValueError('no substantive proper group')
    token=next((t for t in TOKENS if t in observance),None)
    if token:candidates=[g for g in candidates if token in form_label(g)]
    elif len(candidates)>1:candidates=[g for g in candidates if not any(t in form_label(g) for t in TOKENS)]
    if len(candidates)!=1:raise ValueError('ambiguous or unmatched proper form')
    return candidates[0]
def norm(text):return re.sub(r'[\s,，.。]','',text)
def web_body_prefix(lines):
    end=next((i for i,line in enumerate(lines) if '…' in line and re.match(r'^(성부와 성령과|우리 주|성자께서는|주님께서는)',line)),len(lines))
    return ' '.join(lines[:end]).strip()
def encoded(data):return (json.dumps(data,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
def main():
    sources_path=ROOT/'data/sources.json';sources=json.loads(sources_path.read_text(encoding='utf-8'));inventory=json.loads((ROOT/'data/source-library/inventory.json').read_text(encoding='utf-8'));plans=[];audits=[];archive=[]
    for month in [11,12]:
        source=json.loads(next((ROOT/'data/source-library/extracted-hwp').glob(f'*2026{month:02}_*.json')).read_text(encoding='utf-8'))
        assert hashlib.sha256((ROOT/source['sourcePath']).read_bytes()).hexdigest()==source['sha256']
        assert next(x['sha256'] for x in inventory['originalFiles'] if x['libraryPath']==source['sourcePath'])==source['sha256']
        grouped=collections.defaultdict(list)
        for group in source['dates']:grouped[group['date']].append(group)
        ref=f'user-hwp-2026{month:02}'
        sources[ref]=dict(url='../'+source['sourcePath'],checkedAt='2026-10-24',method='HWP-record-boundary-validation-and-GoodNews-body-comparison',sha256=source['sha256'],scope='local-test',rightsStatus='release-permission-deferred',note='사용자 제공 HWP. 날짜별 기본 말씀 양식에 맞는 고유문만 연결. 굿뉴스 축약 종결구 제외 본문 일치 확인; 전체 지면 육안 교정 아님.')
        for date,groups in sorted(grouped.items()):
            page=parse((ROOT/'data/source-library/goodnews-daily/html'/f'{date}.html').read_bytes(),date)
            group=choose_group(groups,page.observance);assert len(group['sections'])==5 and {s['title'] for s in group['sections']}==set(PRAYERS)|set(ANTIPHONS)
            docpath=ROOT/'data/days'/f'{date}.json';doc=json.loads(docpath.read_text(encoding='utf-8'));before_words=[s for s in doc['sections'] if s['kind'] in ['reading','gospel','psalm','acclamation']]
            trace=[];sections=[]
            for section in group['sections']:
                title=section['title'];sid=(PRAYERS|ANTIPHONS)[title];body,tail=(split_prayer if title in PRAYERS else split_antiphon)(section['paragraphs']);text='\n'.join(p['text'] for p in body)
                if title in PRAYERS:
                    web=page.sections[title if title!='예물 기도' else '예물기도'];prefix=web_body_prefix(web)
                    assert len(prefix)>10 and norm(prefix) in norm(text),(date,title,'GoodNews/HWP mismatch')
                sections.append(dict(id=sid,kind='prayer' if title in PRAYERS else 'antiphon',title=title,status='verified',paragraphs=[dict(id=sid+'-p1',role='priest' if title in PRAYERS else 'text',text=text,sourceRef=ref)]))
                trace.append(dict(title=title,sourceHeading=section['heading'],bodyRecords=body,deferredFollowingRecords=tail,textSha256=hashlib.sha256(text.encode('utf-8')).hexdigest(),webBodyMatch=title in PRAYERS))
            doc['sections']=[s for s in doc['sections'] if s['title'] not in set(PRAYERS)|set(ANTIPHONS)]+sections
            if ref not in doc['sourceRefs']:doc['sourceRefs'].append(ref)
            assert before_words==[s for s in doc['sections'] if s['kind'] in ['reading','gospel','psalm','acclamation']]
            plans.append((docpath,doc));audits.append(dict(date=date,observance=page.observance,sourceRef=ref,selectedLabel=form_label(group) or group['heading'],sections=trace,wordLiturgySha256=hashlib.sha256(encoded(before_words)).hexdigest(),omittedHeaderGroups=sum(not g['sections'] for g in groups),otherForms=[form_label(g) for g in groups if g is not group and g['sections']]))
            for i,g in enumerate(groups):
                if g is not group:archive.append(dict(date=date,groupIndex=i,label=form_label(g) or g['heading'],kind='other-mass-form' if g['sections'] else 'date-header-only',sourcePath=source['sourcePath'],group=g))
    assert len(plans)==61
    backup=ROOT/'scratch'/('remaining-propers-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir()
    shutil.copy2(sources_path,backup/'sources.json')
    for path,doc in plans:shutil.copy2(path,backup/path.name);path.write_bytes(encoded(doc))
    sources_path.write_bytes(encoded(sources))
    (ROOT/'data/source-library/extracted-hwp/link-audit-20261112.json').write_bytes(encoded(dict(dates=audits,count=len(plans),matchedPrayers=183)))
    (ROOT/'data/reference-sources/proper-mass-forms-20261112.json').write_bytes(encoded(dict(status='reference-only-not-bound-to-app',groups=archive)))
    print(json.dumps(dict(linkedDates=len(plans),matchedPrayers=183,archivedGroups=len(archive)),ensure_ascii=False))
if __name__=='__main__':main()
