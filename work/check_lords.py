from pathlib import Path
import json,hashlib,shutil,xml.etree.ElementTree as E
from pypdf import PdfReader
root=Path('docs/교중미사악보/rescan-20261018');root.mkdir(exist_ok=True);sources=[]
for name in ['KakaoTalk_20261018_222822492.jpg','KakaoTalk_20261018_222822492_01.jpg']:
 src=Path('C:/Users/imsup/Downloads')/name;dst=root/name;shutil.copy2(src,dst);sources.append({'file':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
(root/'lords-sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')
for key,count in [('lords-a',80),('lords-b',55)]:
 score=E.parse('docs/교중미사악보/reengraved/'+key+'.musicxml');assert len(score.findall('.//note/pitch'))==count
 assert all(sum(int(n.findtext('duration')) for n in m.findall('note'))==72 for m in score.findall('.//measure'))
 r=PdfReader('output/pdf/'+key+'-reengraved.pdf');assert len(r.pages)==1 and not list(r.pages[0].images);assert '■' not in r.pages[0].extract_text();assert Path('output/pdf/'+key+'-reengraved.pdf').read_bytes()==Path('docs/교중미사악보/reengraved/'+key+'.pdf').read_bytes()
assert len(PdfReader('output/pdf/lords-prayer-reengraved.pdf').pages)==2
p=Path('docs/references/score-engraving-status.json');shutil.copy2(p,'scratch/score-status.before-v24.json');d=json.loads(p.read_text(encoding='utf-8'));d['completed'].append('주님의 기도 (2)');d['rescanRequests']=[];d['pendingTranscription']=['대영광송 4면 · 새 사진 수신 · 손글씨 성가대/합송 수정 사용자 확정','거룩하시도다 · 새 사진 수신','신앙의 신비여 3양식 · 새 사진 수신'];d['additionalScoreNeeded']={'score':'보편 지향 기도 응답','status':'사용자 요청으로 악보/낭송 카드만 구성. 선율 미확정, 녹음 요청하지 않음.'};p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
note='''\n\n## 2026-10-18 주님의 기도 우선 조판·참회 전환 v24
- 새 주님의 기도2 사진2장 원본/해시 보존. 앞부분80음+이어서55음, 12/8박자20마디 전부72tick. 점4분음표72, 페르마타·붙임줄·슬러·마지막 천천히 표시. PDF2쪽 합본/SVG2개/MusicXML2개. 원본 대조 및 PDF PNG 두 쪽 직접 열어 가사·레이아웃 확인, 본당 최종 교정 전. 뷰어 기존사진을 새PDF/SVG로 교체, 크게보기 각쪽PDF 유지. 완료6항목.
- 보편 지향 기도 응답: 사용자 요청으로 하나의 카드 안에 낭송/악보 버튼. 악보 탭에는 준비 중 및 실제 응답본문, 선율을 임의 생성하지 않음. 녹음 요청하지 않음.
- 참회 예식: 두 선택지 동시나열 대신 고정 높이 카드 내부 스크롤과 전능하신 하느님과/진심으로 뉘우치는 두 버튼. 전체 해당양식만 표시, 첫선택지 기본. 원본 텍스트 보존, 독립적 페이지분할 제외. 버튼 클릭은 메모리상 표시전환, 실제 사제양식 자동판정 아님.
- 대영광송 손글씨 수정은 실제 본당 역할구분으로 사용자가 확정. 대영광송/거룩하시도다/신앙의 신비여 새사진 수신, 재촬영 필요가 아니라 조판 대기. 이번 사용자 지정 우선 작업은 주님의 기도.
- node --check work/review-ia-v24-check.js, node work/test-reader-v24.cjs, 번들 Python work/check_lords.py 통과. PDF 벡터/2쪽/135음/20마디72tick/한글/파일동일 검증, 기존UI회귀+참회버튼/단일카드/본문전환/응답카드/주님의기도2assets 검사. 실제브라우저 높이/PDFplugin 시각QA는 미실행.
- 최신 review/02-ia-v24.html, v23 보존. 2단계 보완, 이후단계 승인 아님.
'''
for name in ['docs/progress.md','design.md','ENGINEERING.md','README.md']:
 q=Path(name);shutil.copy2(q,Path('scratch')/(q.name+'.before-v24'));q.write_text(q.read_text(encoding='utf-8')+note,encoding='utf-8',newline='\r\n')
print('PASS: two-page vector PDF, 135 notes, twenty complete 12/8 measures, Korean text, source hashes; status updated.')
