from pathlib import Path
import json,re,hashlib,shutil,datetime
root=Path('data/reference-sources');root.mkdir(parents=True,exist_ok=True)
index=json.loads(Path('work/reference-research/prayer-index.json').read_text(encoding='utf-8'))
prayers={'sourceUrl':'https://maria.catholic.or.kr/mi_pr/prayer/prayer.asp','checkedOn':'2026-10-19','storagePolicy':'links-only-pending-permission','items':[dict(id=x['id'],title=x['title'],url='https://maria.catholic.or.kr/mi_pr/prayer/prayer.asp?menu=prayer&pgubun=3&ingId='+x['id']) for x in index]}
(root/'major-prayers.json').write_text(json.dumps(prayers,ensure_ascii=False,indent=2),encoding='utf-8')
provider={'provider':'GOODNEWS','diocese':'대구대교구','dioceseCode':'21','indexUrl':'https://maria.catholic.or.kr/jubo/jubo_list.asp?jgubun=G&s_gyocode=21','storagePolicy':'source-links-no-bulk-copy','issues':[{'date':'2026-10-18','viewUrl':'https://maria.catholic.or.kr/jubo/jubo_view.asp?ju_no=9092','pdfUrl':'https://maria.catholic.or.kr/jubo/down/down.asp?filenm=261018.pdf&gyocode=21','filename':'261018.pdf','checkedOn':'2026-10-19'}]}
(root/'daegu-bulletin.json').write_text(json.dumps(provider,ensure_ascii=False,indent=2),encoding='utf-8')
cells=json.loads(Path('work/reference-research/hymn-cells.json').read_text(encoding='utf-8'));rows={}
for c in cells:rows.setdefault(c['row'],{})[c['col']]=c['text']
days=[]
for row in rows.values():
 m=re.match(r'^(\d+)\(',row.get(0,''))
 if not m:continue
 day=int(m[1]);roles={}
 for key,cols in [('entrance',[2]),('offertory',[3,4]),('communion',[5,6,7]),('recessional',[8])]:
  values=[row.get(c,'').strip() for c in cols if row.get(c,'').strip()];assert all(v.isdigit() for v in values),(day,values);roles[key]=[int(v) for v in values]
 days.append({'date':f'2026-10-{day:02}','observance':row.get(1,''),'recommendations':roles})
assert len(days)==31 and len({d['date'] for d in days})==31
source=Path('C:/Users/imsup/Downloads/2026년 10월 성가표(수정보완판).hwp')
hymns={'month':'2026-10','edition':'수정보완판','sourceFilename':source.name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceUrl':'https://bbs.catholic.or.kr/pdsm/bbs_view.asp?id=212615&menu=4807','status':'recommendation-not-parish-confirmed','slotAssignments':None,'days':days}
(root/'hymn-schedule-202610.json').write_text(json.dumps(hymns,ensure_ascii=False,indent=2),encoding='utf-8')
monthly={'indexUrl':'https://www.cbck.or.kr/Board/K7020','purpose':'monthly-proper-prayers-not-verified-full-readings','issues':[{'month':'2026-10','url':'https://www.cbck.or.kr/Board/K7020/20261395','formats':['hwp','hwpx']},{'month':'2026-12','url':'https://www.cbck.or.kr/Board/K7020/20262479','publishedAt':'2026-10-15 16:30','formats':['hwp','hwpx']}],'downloadPolicy':'no-automatic-download-pending-permission'}
(root/'monthly-propers.json').write_text(json.dumps(monthly,ensure_ascii=False,indent=2),encoding='utf-8')
rights={'checkedOn':'2026-10-19','generalUrl':'https://www.cbck.or.kr/Copyright','rulesUrl':'https://www.cbck.or.kr/Board/K7300/20230535','ruleTitle':'복음화를 위한 개별 교구의 저작권 사용에 관한 규정','ruleEffectiveOn':'2023-10-12','permissionStatus':'not-confirmed','autoCollection':'blocked-pending-written-permission','newFullTextEmbedding':'on-hold','notes':['교구/본당 공적 사목과 개인 사용의 적용 범위가 다름.','제3조 제2항 개인 사용 승인 절차, 제8조 애플리케이션 관련 제한 확인 필요.','웹 공개나 첨부파일 존재를 앱 내장/재배포 허가로 해석하지 않음.','기존 로컬 검토본은 자동 삭제하거나 허가 완료로 표기하지 않음.'],'contact':{'email':'mano@cbck.kr','phone':'02-460-7552'}}
(root/'rights.json').write_text(json.dumps(rights,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(index),'prayer links;',len(days),'daily hymn recommendations; Daegu code 21; monthly October/December metadata.')
