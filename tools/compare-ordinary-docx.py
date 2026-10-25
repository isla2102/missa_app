"""Compare user-provided DOCX text, numbering and embedded media without changing sources."""
from pathlib import Path
import zipfile,xml.etree.ElementTree as E,re,json,hashlib,shutil,difflib,unicodedata,html,io
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'docs/research/ordinary-comparison';D.mkdir(parents=True,exist_ok=True);L=R/'data/source-library/ordinary';L.mkdir(parents=True,exist_ok=True)
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships';N={'w':W}
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
def norm(s):return ''.join(c for c in unicodedata.normalize('NFC',s) if c.isalnum())
def parse(key,name):
 src=R/name;dest=L/'originals'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest);z=zipfile.ZipFile(src);doc=E.fromstring(z.read('word/document.xml'));rels={r.get('Id'):r.get('Target') for r in E.fromstring(z.read('word/_rels/document.xml.rels'))};paras=[];media=[]
 for i,p in enumerate(doc.findall('.//w:body//w:p',N),1):
  pieces=[];images=[]
  for e in p.iter():
   if e.tag=='{'+W+'}t':pieces.append(e.text or '')
   elif e.tag in ['{'+W+'}br','{'+W+'}cr']:pieces.append('\n')
   elif e.tag=='{'+W+'}tab':pieces.append('\t')
   elif e.tag=='{'+A+'}blip':
    target=rels.get(e.get('{'+REL+'}embed'))
    if target:images.append(target)
  text=''.join(pieces)
  if text.strip() or images:paras.append({'p':i,'text':text,'images':images})
 for f in z.namelist():
  if not f.startswith('word/media/'):continue
  data=z.read(f);out=L/'media'/key/Path(f).name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
  im=Image.open(io.BytesIO(data));media.append({'name':Path(f).name,'path':str(out.relative_to(R)).replace('\\','/'),'width':im.width,'height':im.height,'sha256':hashlib.sha256(data).hexdigest()})
 text='\n'.join(p['text'] for p in paras if p['text'].strip());matches=[m for m in re.finditer(r'(?<!\d)(\d{1,3})\.(?!\d)',text) if 1<=int(m.group(1))<=146];blocks={int(m.group(1)):text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)].strip() for i,m in enumerate(matches)}
 write(L/'extracted'/(key+'.txt'),text);write(L/'extracted'/(key+'.json'),json.dumps(paras,ensure_ascii=False,indent=2))
 result={'key':key,'filename':name,'sourcePath':name,'copyPath':str(dest.relative_to(R)).replace('\\','/'),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'paragraphsNonemptyText':sum(bool(p['text'].strip()) for p in paras),'textChars':len(text),'media':media,'imagePlacements':sum(len(p['images']) for p in paras),'numberedItems':list(blocks),'hasApostlesBody':norm('천지의 창조주를 저는 믿나이다') in norm(text),'paragraphs':paras,'blocks':blocks}
 return result
seoul=parse('seoul','미사통상문_서울대교구.docx');cbck=parse('cbck','미사통상문_한국천주교주교회.docx');common=sorted(set(seoul['blocks'])&set(cbck['blocks']));comparisons=[]
for n in common:
 a,b=seoul['blocks'][n],cbck['blocks'][n];comparisons.append({'item':n,'strictEqual':a==b,'normalizedEqual':norm(a)==norm(b),'seoul':a,'cbck':b})
manifest={'checkedAt':'2026-10-24','inputs':[{k:v for k,v in d.items() if k not in ['paragraphs','blocks']} for d in [seoul,cbck]],'commonNumberedItems':common,'equalAfterNormalization':[x['item'] for x in comparisons if x['normalizedEqual']],'normalization':'NFC and alphanumeric comparison only; removes spaces,punctuation,role marks; original text preserved. Does not establish doctrinal equivalence.','scope':'OOXML text/media inspection; not Word page-layout rendering; numbered blocks include intervening headings and explanations. Inferred absence means absent from supplied capture, not absent from website.'}
write(D/'comparison.json',json.dumps(manifest,ensure_ascii=False,indent=2));write(D/'numbered-item-diff.json',json.dumps(comparisons,ensure_ascii=False,indent=2))
write(L/'manifest.json',json.dumps(manifest['inputs'],ensure_ascii=False,indent=2))
# Preserve all provided text and embed existing DOCX images in source order.
head=(R/'review/07-research-library-v1.html').read_text(encoding='utf-8').split('</head>')[0].replace('MISSA · 자료실과 7단계','MISSA · 사용자 DOCX 비교')
extra='@layer components { .comparison__text { white-space:pre-wrap; overflow-wrap:anywhere; font-size:var(--draft-note); } .comparison__image { max-inline-size:100%; block-size:auto; } .comparison__table { inline-size:100%; border-collapse:collapse; } .comparison__cell { padding:var(--draft-space-2); text-align:start; border-bottom:var(--draft-line); vertical-align:top; } }'
head=head.replace('</style>',extra+'</style>')+'</head>'
body='<body><main class="system"><header><p class="system__meta">사용자 제공 DOCX · 2026-10-24 · 원본 보존</p><h1>악보 외에도 내용 범위가 다릅니다</h1><p>해설 · 사도 신경 · 감사 기도 양식 · 지시문을 구분해 확인했습니다.</p></header><section class="system__card"><h2>주요 차이</h2><ul><li>서울: 해설·자세 안내가 많고 감사 기도 제2양식 본문이 포함됩니다.</li><li>주교회의: 사도 신경과 감사 기도 제1양식 본문, 내장 이미지 44개가 포함됩니다.</li><li>서울 내장 이미지 1개는 TOP 버튼 아이콘입니다. 악보 이미지로 보지 않습니다.</li><li>두 캡처 모두 감사 기도 전체 양식을 포함한 완전본으로 단정할 수 없습니다.</li></ul></section><section class="system__card"><h2>구조 비교</h2><table class="comparison__table"><thead><tr><th class="comparison__cell">항목</th><th class="comparison__cell">서울대교구</th><th class="comparison__cell">주교회의</th></tr></thead><tbody>'
for label,x,y in [('비어 있지 않은 본문 문단',seoul['paragraphsNonemptyText'],cbck['paragraphsNonemptyText']),('내장 이미지 파일',len(seoul['media']),len(cbck['media'])),('이미지 배치 횟수',seoul['imagePlacements'],cbck['imagePlacements']),('사도 신경 본문','미포함','포함'),('감사 기도 본문','제2양식 99–106항','제1양식 83–98항')]:body+=f'<tr><th class="comparison__cell">{label}</th><td class="comparison__cell">{x}</td><td class="comparison__cell">{y}</td></tr>'
body+='</tbody></table><p>문단 수는 글자만 있는 문단 기준입니다. 그림 안의 글씨·악보는 OCR로 교감하지 않았습니다.</p></section><section class="system__card"><h2>내용 차이 예시</h2><ul><li>주교회의 19항에 사도 신경 본문이 있으나 서울 캡처에는 없습니다.</li><li>서울 130항의 도입 지시가 더 구체적이고 ‘무릎을 꿇는다’ 자세 안내가 추가됩니다.</li><li>서울 해설에 ‘혀용된’ 표기가 있습니다. 원본은 수정하지 않았습니다.</li><li>124항과 144항 블록은 공백·기호 등을 제외한 글자 비교에서 일치합니다.</li></ul><p>단어·지시문 차이가 모두 교리·전례 규정 차이를 뜻하는 것은 아닙니다. 웹에서 펼친 양식과 복사 범위의 차이를 포함합니다.</p></section><section><h2>항 번호별 대조</h2><p>다음 번호 앞까지의 제목·해설도 포함됩니다. 불일치 건수는 공식 본문 오류 건수가 아닙니다.</p>'
for c in comparisons:
 body+=f'<details class="system__card"><summary>{c["item"]}항 · '+('공백·기호 제외 일치' if c['normalizedEqual'] else '차이 있음 / 해설·문단 경계 포함')+'</summary><h3>서울</h3><p class="comparison__text">'+html.escape(c['seoul'])+'</p><h3>주교회의</h3><p class="comparison__text">'+html.escape(c['cbck'])+'</p></details>'
body+='</section><section><h2>제공 문서 내용 전체 열람</h2><p>텍스트와 내장 이미지의 순서를 보존한 열람용 변환입니다. Word의 페이지 배치·폰트·색상을 그대로 재현한 결과는 아닙니다.</p>'
for d in [seoul,cbck]:
 body+='<details class="system__card"><summary>'+html.escape(d['filename'])+'</summary>'
 for p in d['paragraphs']:
  if p['text'].strip():body+='<p class="comparison__text">'+html.escape(p['text'])+'</p>'
  for target in p['images']:body+=f'<img class="comparison__image" src="../data/source-library/ordinary/media/{d["key"]}/{html.escape(Path(target).name)}" alt="제공 문서 내장 이미지">'
 body+='</details>'
body+='</section><section class="system__card"><h2>개발을 이어갈 기준</h2><p>공통 본문은 주교회의 문서를 우선 대조하고 서울 문서는 해설·역할 표시와 제2양식의 보조 출처로 관리하는 안을 권합니다. 자동 병합은 하지 않았습니다.</p><a href="../docs/research/ordinary-comparison/README.md">비교 결과·한계</a><a href="../docs/release-readiness.md">출시 준비 리마인드</a><a href="07-state-review-v1.html">7단계 검수 화면</a></section></main></body></html>'
write(R/'review/07-ordinary-comparison-v1.html',head+body)
print(json.dumps({'paragraphs':[seoul['paragraphsNonemptyText'],cbck['paragraphsNonemptyText']],'media':[len(seoul['media']),len(cbck['media'])],'placements':[seoul['imagePlacements'],cbck['imagePlacements']],'commonItems':len(common),'normalizedEqualItems':manifest['equalAfterNormalization'],'apostles':[seoul['hasApostlesBody'],cbck['hasApostlesBody']]},ensure_ascii=False))
