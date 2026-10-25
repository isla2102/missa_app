from pathlib import Path
import json,re,hashlib,xml.etree.ElementTree as E
root=Path.cwd();base=root/'docs/교중미사악보/reengraved';reg=json.loads((base/'registry.json').read_text(encoding='utf-8-sig'));cat=json.loads((root/'data/reference-sources/missal-ordinary.json').read_text(encoding='utf-8-sig'));records={r['key']:r for r in cat['records']}
def norm(s):return re.sub('[^가-힣]','',s)
def body(key):return '\n'.join(x for x in records[key]['text'].splitlines() if not x.startswith('['))
def svgtext(p):
 t=E.parse(p);parents={c:p for p in t.iter() for c in p};texts=[]
 for e in t.iter():
  if not e.tag.endswith('}text'):continue
  q=e;classes=[]
  while q in parents:q=parents[q];classes+=q.attrib.get('class','').split()
  if 'verse' in classes:texts.append(''.join(e.itertext()))
 return ''.join(texts)
def xmltext(p):return ''.join(''.join(e.itertext()) for e in E.parse(p).findall('.//lyric/text'))
mapfiles={'아멘':['amen'],'자비송':['kyrie'],'주님의 기도 맺음 환호':['doxology'],'복음 환호송':['alleluia-365'],'하느님의 어린양':['agnus'],'주님의 기도':['lords-a','lords-b'],'대영광송':['gloria-a','gloria-b','gloria-c','gloria-d'],'거룩하시도다':['sanctus']}
items=[];protected={}
for key,assets in reg.items():
 for asset in assets:
  season=asset.get('season');stem='memorial-'+season if season else None;xmls=[base/(n+'.musicxml') for n in ([stem] if season else mapfiles[key])];svg=root/asset['preview'].removeprefix('../');pdf=root/asset['path'].removeprefix('../')
  for p in [*xmls,svg,pdf]:protected[str(p.relative_to(root)).replace('\\','/')]=hashlib.sha256(p.read_bytes()).hexdigest()
  score=svgtext(svg);encoded=''.join(xmltext(p) for p in xmls)
  if key=='주님의 기도':reference=body(key).split('◎',1)[1].split('+ 주님, 저희를',1)[0]
  elif key=='복음 환호송':reference='알렐루야, 알렐루야, 알렐루야.'
  elif season:
   n={'ordinary':1,'lent':2,'easter':3}[season];text=records[key]['text'];reference='신앙의 신비여! '+text.split(f'[응답 {n}]',1)[1].split('[',1)[0]
  else:reference=body(key)
  a=norm(score);expected=norm(reference);adjusted=a;repeats=[]
  if key in ['아멘','대영광송'] and a.endswith('아멘아멘아멘'):
   adjusted=a[:-6]+'아멘';repeats.append('아멘 ×3 → 낭송문 ×1로 비교')
  if key=='주님의 기도' and '악에서악에서' in a:
   adjusted=adjusted.replace('악에서악에서','악에서',1);repeats.append('악에서 ×2 → 낭송문 ×1로 비교')
  item={'key':key,'season':season,'scorePath':str(svg.relative_to(root)).replace('\\','/'),'pdfPath':str(pdf.relative_to(root)).replace('\\','/'),'musicXmlPaths':[str(p.relative_to(root)).replace('\\','/') for p in xmls],'scoreLyrics':score,'referenceText':reference,'normalization':'한글 음절 비교: 띄어쓰기·문장부호·음절 배치·절 번호 제외; 가사 verse 요소만 추출, 역할·템포 표시는 제외','scoreMatchesMusicXml':a==norm(encoded),'literalNormalizedEqual':a==expected,'comparisonEqualAfterListedRepetitions':adjusted==expected,'repetitions':repeats,'scopeNote':'후렴 한 번의 음악적3회 알렐루야 반복을 앱 낭송 후렴3회와 비교. 날짜별 절 구절은 별도.' if key=='복음 환호송' else '주님의 기도 합송 부분만 비교. 사제 도입·이어지는 기도는 이 악보 범위 밖.' if key=='주님의 기도' else '현재 연결된 재조판 자산의 가사 범위. 경본 선율과 같다는 판정이 아님.'}
  item['status']='setting-repetition-only' if repeats and adjusted==expected else 'normalized-equal' if a==expected else 'needs-review';items.append(item)
report={'date':'2026-10-24','activeScoresReplaced':False,'items':items,'assetHashes':protected,'summary':{'assets':len(items),'svgXmlMatches':sum(i['scoreMatchesMusicXml'] for i in items),'normalizedEqual':sum(i['status']=='normalized-equal' for i in items),'repetitionOnly':sum(i['status']=='setting-repetition-only' for i in items),'needsReview':sum(i['status']=='needs-review' for i in items)},'limits':['음표·리듬·음정 교감 및 독립된 두 번째 교정은 미실행.','인쇄본 사진 전체의 OCR/가사 교감 완료를 뜻하지 않음. 현재 연결된 SVG와 MusicXML 가사를 검사.','사용자가 입력하는 성가번호의 원격 악보, 화답송 미등록 악보, 신경 및 보편 지향 기도 미등록 악보는 제외.','문장부호와 띄어쓰기는 음절별 악보 표기의 특성 때문에 자동 일치 판정에서 제외.']}
out=root/'docs/research/ordinary-comparison/parish-score-lyrics.json';out.write_bytes(json.dumps(report,ensure_ascii=False,indent=2).replace('\n','\r\n').encode('utf-8'))
print(json.dumps(report['summary']));print([(i['key'],i['season'],i['status']) for i in items])
