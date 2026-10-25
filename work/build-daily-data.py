from pathlib import Path
import re,html,json,hashlib
raw=Path('work/daily-20261018.html').read_bytes();s=raw.decode('utf-8-sig')
assert '2026년 10월 18일' in re.sub('<[^>]*>','',s)
def clean(text):
 text=re.sub(r'<(?:script|style)\b.*?</(?:script|style)>','',text,flags=re.S)
 text=re.sub(r'<br\s*/?>|</(?:div|p|h5)>','\n',text,flags=re.I)
 return '\n'.join(line.strip() for line in html.unescape(re.sub('<[^>]*>','',text)).splitlines() if line.strip())
keys=[('제1독서','reading-1','reading'),('화답송','psalm','psalm'),('제2독서','reading-2','reading'),('복음 환호송','acclamation','acclamation'),('복음','gospel','gospel'),('예물 기도','offertory','prayer'),('감사송','preface','preface'),('영성체 후 기도','post-communion','prayer'),('보편 지향 기도','intercessions','intercession')]
sections=[]
for title,key,kind in keys:
 chunk=re.search(r'<h4>'+title+r'(?=<).*?</h4>(.*?)(?=<h4>|$)',s,re.S)
 if not chunk:raise ValueError(title)
 text=clean(chunk.group(1));lines=text.splitlines();paragraphs=[]
 for i,line in enumerate(lines):
  role='assembly' if line.startswith('◎') else 'lector' if line.startswith('▥') else 'priest' if line.startswith('✠') else 'text'
  paragraphs.append(dict(id=f'{key}-p{i+1}',role=role,text=line,sourceRef='cbck-20261018'))
 sections.append(dict(id=key,kind=kind,title=title,status='verified',paragraphs=paragraphs))
collect=json.loads(Path('docs/references/daily-missa-20261018.json').read_text(encoding='utf-8'))
sections.append(dict(id='collect',kind='prayer',title='본기도',status='verified',paragraphs=[dict(id=f'collect-p{i+1}',role='priest',text=t,sourceRef='cbck-20261018') for i,t in enumerate(collect['collectVariants'])]))
for key,title in [('intercession-conclusion','사제 마침 기도'),('psalm-score','주보 화답송 악보')]:sections.append(dict(id=key,kind='prayer' if 'conclusion' in key else 'psalm',title=title,status='missing',paragraphs=[]))
doc=dict(schemaVersion=1,documentId='mass-2026-10-18',date='2026-10-18',observance=collect['observance'],sourceRefs=['cbck-20261018'],sections=sections)
for folder in ['data/days','schemas']:Path(folder).mkdir(parents=True,exist_ok=True)
Path('data/days/2026-10-18.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding='utf-8')
sources={'cbck-20261018':dict(url='https://missa.cbck.or.kr/DailyMissa/20261018',checkedAt='2026-10-19',method='manual-reviewed-page-snapshot',sha256=hashlib.sha256(raw).hexdigest(),rightsStatus='copyright-notice-present-permission-not-confirmed',scope='local-review',note='공개 열람을 재배포 허가로 간주하지 않음. 본문 자동 추출 서비스와 인쇄 지면의 차이가 있을 수 있음.')}
Path('data/sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')
def obj(props):return dict(type='object',properties=props,required=list(props),additionalProperties=False)
string={'type':'string','minLength':1};paragraph=obj(dict(id=string,role={'enum':['text','priest','lector','assembly','guidance']},text=string,sourceRef=string))
section=obj(dict(id=string,kind={'enum':['reading','gospel','psalm','acclamation','prayer','intercession','preface','antiphon']},title=string,status={'enum':['verified','missing','needs-review']},paragraphs={'type':'array','items':paragraph}))
section['allOf']=[{'if':{'properties':{'status':{'const':'verified'}}},'then':{'properties':{'paragraphs':{'minItems':1}}}}]
schema=obj(dict(schemaVersion={'const':1},documentId=string,date={'type':'string','format':'date','pattern':'^\\d{4}-\\d{2}-\\d{2}$'},observance=string,sourceRefs={'type':'array','minItems':1,'uniqueItems':True,'items':string},sections={'type':'array','minItems':1,'items':section}));schema['$schema']='https://json-schema.org/draft/2020-12/schema'
Path('schemas/mass-document.schema.json').write_text(json.dumps(schema,ensure_ascii=False,indent=2),encoding='utf-8')
print('Built',len(sections),'sections; missing conclusion and parish score explicitly retained.')
