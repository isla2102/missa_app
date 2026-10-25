from pathlib import Path
import shutil,json,xml.etree.ElementTree as E
p=Path('docs/교중미사악보/reengraved/registry.json');shutil.copy2(p,'scratch/registry-before-v26.json');r=json.loads(p.read_text(encoding='utf-8'))
for title,key in [('대영광송','gloria'),('주님의 기도','lords-prayer')]:
 for a in r[title]:a['preview']=a['preview'].replace(key+'.svg',key+'-v26.svg')
p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
entry='''\n## 2026-10-19 사용자 주석 수정 v26\n- 합본 SVG의 원래 루트가 없어져 오선·기둥 stroke CSS 범위가 소실된 버그 수정. 선 속성을 명시하고 음표 glyph 참조를 실제 벡터 경로로 펼쳐 보존. 대영광송/주님의기도 v26 SVG 별도 저장, v25 자산 보존. 두 합본을 PDF/PNG 렌더하여 오선·음표머리·기둥·깃발 확인.\n- 뷰어 제목 중앙, 이전 차례 왼쪽/다음 차례 오른쪽. 목차 프레임은 책과 동일 행 유지, 도구는 목차 아래 페이지 이동 행에 배치.\n- 현재 펼친 두 페이지의 모든 tocId를 집계해 연속 목차 항목을 테두리 프레임으로 강조. 기존 선택 위치 접근성 표시는 유지.\n- 제1/2독서의 [독서자] 제거. 독서/복음 마침말+합송, 인사 마지막 양식+공통 합송을 한 블록 안의 2열로 묶음. 좁은 폭은 자동 줄바꿈.\n- 보편지향 응답 악보 선택은 낭송 카드를 숨김. 실제 악보가 없으므로 준비 중만 표시, 선율 추정 없음. 거룩하시도다 카드 자연 높이/뷰어 최대 높이 적용.\n- node syntax, test-reader-v26 전체 회귀 및 주석별 검사 통과. 실제 브라우저 치수/스크롤 시각 QA는 미실행. 다음 단계 승인 없이 2단계 보완 유지. 최신 review/02-ia-v26.html.\n'''
for name in ['docs/progress.md','design.md']:
 p=Path(name);shutil.copy2(p,'scratch/'+p.name+'.before-v26');p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
for key in ['gloria','lords-prayer']:
 root=E.parse('docs/교중미사악보/reengraved/'+key+'-v26.svg').getroot();assert not any(n.tag.endswith('}use') for n in root.iter());assert any(n.get('stroke')=='black' for n in root.iter())
print('PASS: flattened glyph references and explicit strokes; review history saved.')
