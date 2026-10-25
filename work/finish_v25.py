from pathlib import Path
import json,shutil,xml.etree.ElementTree as E
from pypdf import PdfReader
r=Path('docs/교중미사악보/reengraved')
expected={'gloria-a':80,'gloria-b':81,'gloria-c':73,'gloria-d':37,'sanctus':76,'memorial-ordinary':36,'memorial-lent':40,'memorial-easter':31}
for key,n in expected.items():
 root=E.parse(r/(key+'.musicxml')).getroot();assert len(root.findall('.//note/pitch'))==n,(key,n)
assert len(PdfReader('output/pdf/remaining-scores-reengraved.pdf').pages)==8
registry=json.loads((r/'registry.json').read_text(encoding='utf-8'))
for assets in registry.values():
 for a in assets:
  for f in ['path','preview']:
   if f in a:assert (Path('review')/a[f]).exists(),a[f]
p=Path('docs/references/score-engraving-status.json');shutil.copy2(p,'scratch/score-status-before-v25.json');status=json.loads(p.read_text(encoding='utf-8'));status['completed']+=['대영광송','거룩하시도다','신앙의 신비여 3양식'];status['pendingTranscription']=[];p.write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
entry='''\n## 2026-10-19 IA 보완 v25\n- 대영광송 4면(271음/92마디), 거룩하시도다(76음), 신앙의 신비여 3양식(36/40/31음) 재조판. 사진 대조 및 PDF 렌더 확인, 본당 최종 교정 전. 완료 9개 악보 묶음. 보편 지향 응답 선율은 미확정 유지.\n- 대영광송 4면과 주님의 기도 2면 각각 단일 연속 SVG 및 합본 PDF. 중간 캡션/버튼 제거, 한 카드에서 연속 스크롤. 짧은 악보 카드는 자연 높이, 긴 악보는 뷰어 높이 내 스크롤.\n- 복음 작은 십자 문구 수정, 첫 사제/회중 응답 좌우 배치. 보편 지향 기도 제목의 공통 낭송/악보 버튼이 네 응답 일괄 전환.\n- 사순/부활 사도 신경 기본값은 선택 가능한 전례 규정의 UI 기본값이며 강제 규정이 아님. 수동 전환 유지. 근거 https://missale.cbck.or.kr/OrdoMissae .\n- 순서 이동은 뷰어 제목 줄로, 중복 현재 위치 제거. 보기 설정/안내는 목차 위 제목 줄 우측, 목차는 책 영역 상단 정렬.\n- node syntax 및 test-reader-v25 회귀 통과. PDF 8쪽 및 음표 수/자산 경로/연속 SVG ID 검사 통과. 실제 브라우저 높이 및 PDF 플러그인 시각 QA 미실행. Stage 2 검토안이며 다음 단계 승인 아님. 최신 review/02-ia-v25.html.\n'''
for name in ['docs/progress.md','.ai-workspace/handoff.md','.ai-workspace/Project_Status.md']:
 p=Path(name);shutil.copy2(p,Path('scratch')/(p.name+'.before-v25'));p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
print('PASS: 8 PDF pages, note counts, registry files; status and handoff updated.')
