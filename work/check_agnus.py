from pathlib import Path
from pypdf import PdfReader
import xml.etree.ElementTree as E,json,hashlib,shutil
p=Path('output/pdf/agnus-reengraved.pdf');r=PdfReader(p);assert len(r.pages)==1 and not list(r.pages[0].images);text=r.pages[0].extract_text();assert '■' not in text and '평' in text and '교정 전' in text
x=E.parse('docs/교중미사악보/reengraved/agnus.musicxml');assert len(x.findall('.//note/pitch'))==54
ps=[n.findtext('pitch/step')+n.findtext('pitch/octave') for n in x.findall('.//note')];assert ps[:11]==['A4','A4','G4','A4','G4','G4','A4','G4','F4','D4','C4'];assert ps[:18]==ps[18:36]==ps[36:]
assert p.read_bytes()==Path('docs/교중미사악보/reengraved/agnus.pdf').read_bytes()
root=Path('docs/교중미사악보/rescan-20261018');root.mkdir(exist_ok=True);sources=[]
for name in ['KakaoTalk_20261018_195716437.jpg','KakaoTalk_20261018_195716437_01.jpg']:
 src=Path('C:/Users/imsup/Downloads')/name;dest=root/name;shutil.copy2(src,dest);sources.append({'file':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source':'user-provided-rescan'})
(root/'manifest.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')
status=Path('docs/references/score-engraving-status.json');shutil.copy2(status,'scratch/score-status.before-v22.json');data=json.loads(status.read_text(encoding='utf-8'));data['completed'].append('하느님의 어린양');data['rescanRequests']=[r for r in data['rescanRequests'] if r['score']!='하느님의 어린양'];data['additionalScoreNeeded']={'score':'보편 지향 기도 응답','request':'본당에서 노래하는 주님, 저희의 기도를 들어주소서 악보 사진. 기존 자료에 선율 없음.','eveningStatus':'unknown; preserve text until confirmed'};status.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
note='''\n\n## 2026-10-18 어린양 재조판·주석6건 v22
- 새 사용자 사진2장을 rescan-20261018에 원본/해시 보존. 어린양을 54음/6시스템 PDF/SVG/MusicXML 조판, 1·2절 반복을 펼쳐 표기. 긴 낭송음/페르마타/3절 평화를 주소서 포함. 새 사진과 대조하고 PDF PNG 실제 열어 확인. 본당 최종 교정 전. 완료5항목, 재스캔4곡 남음.
- 4종 성가 카드 번호 엔트리(1~528)+악보 보기. 날짜/회차/성가종별 메모리 편성, 번호 임의 초기지정 없음. 공식 굿뉴스 단성 2012 이미지 경로를 원격 img로 표시, 로컬 미디어 다운로드하지 않음. 1/2/365/528 경로 확인, 전체528곡 로딩 미검증. 수정개정판과의 판본 일치 미확인, 공식 수정개정판으로 확정 표시하지 않음. 이미지 실패 안내.
- 악보 크게보기 버튼은 figure 상대 위치 위 compact overlay. 크기/패딩/z-index는 draft토큰. 기존 native dialog 유지.
- 참회 선택2의 호칭 안내, 본기도 확인자료 라벨/두수록본문 안내 제거. 강론 원문없음 대신 중립 카드: 앉아서 강론을 듣고 말씀을 삶에 새김.
- 보편 지향 기도 응답의 낭송/악보 버튼 없음. 사용자 확정된 교중은 chant-pending-score 표시, 선율 자료 요청 카드+본문fallback. 새벽/저녁은 선율 및 노래 여부 미확인으로 기존 본문. 실제 음표 악보는 자료가 없어 미완료, 임의 작곡하지 않음. 사용자 명시 변경으로 회차별 이 응답 표시정책 차이 허용.
- node --check work/review-ia-v22-check.js, node work/test-reader-v22.cjs, 번들 Python work/check_agnus.py 통과. 폼 번호/범위/remote경로/확대·모드/도움말삭제/강론카드/응답정책/기존흐름 회귀. PDF1쪽·벡터·54음·원본멜로디·가사·바이트동일 검사. 실제 브라우저 원격img·좌표·PDFplugin 검증 미실행.
- 최신 review/02-ia-v22.html, v21 보존. 2단계 보완, 다음 단계 승인 아님.
'''
for name in ['docs/progress.md','design.md','ENGINEERING.md','README.md']:
 q=Path(name);shutil.copy2(q,Path('scratch')/(q.name+'.before-v22'));q.write_text(q.read_text(encoding='utf-8')+note,encoding='utf-8',newline='\r\n')
print('PASS: Agnus vector PDF, 54 notes, three matching verse melodies, Korean lyrics, source hashes; progress updated.')
