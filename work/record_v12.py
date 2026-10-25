from pathlib import Path
p=Path('work/update_review_v12.py')
s=p.read_text(encoding='utf-8').replace("거룩한 복음입니다.\\\\n◎ 주님, 영광 받으소서.","거룩한 복음입니다.\\\\n[안내] 이마와 입술과 가슴에 십자 표시를 합니다.\\\\n◎ 주님, 영광 받으소서.")
p.write_text(s,encoding='utf-8',newline='\r\n')
entry='''\n\n## 2026-10-18 선택지·변동 본문 카드 보완 v12\n- 사용자 16개 브라우저 코멘트 반영 제안. 2단계 정보 구조 보완이며 단계 확정/3단계 승인을 의미하지 않음. v11 보존.\n- 인사 3개·참회 2개 선택지 카드를 분리. 참회 호칭 본문은 자비송 카드의 “참회 호칭 포함” 전환으로 통합하여 중복 표시하지 않음.\n- 대영광송 인쇄본 안내 복원. 펼친 악보 사진은 인쇄면 한 쪽씩 SVG 표시 영역을 나누어 카드 내부에 세로로 배치. 원본 사진 파일은 수정하지 않음.\n- 본기도 카드 안에 사제 기도 참여 안내 추가. 각 예식 끝에 다음 예식 이동 안내 및 버튼 배치(마침 예식은 종료 안내). 보이스·톤 미확정.\n- 제1·2독서, 복음, 보편 지향 기도는 매일미사 연결용 mock 카드. 실제 외부 연동 없음. 화답송은 주보 악보 카드 슬롯으로 표시하며 미제공 악보를 생성하지 않음.\n- 알렐루야에 낭송/악보 전환 적용. 신앙 고백은 두 카드 중 하나를 버튼으로 표시하며 한 쪽 높이 카드 내부 스크롤 사용. 긴 신경 본문을 다음 페이지로 분할하지 않음.\n- 보편 지향 기도 응답은 별도 낭송/성가 카드. 성가 표시로 시작하되 악보 미등록 상태를 명시.\n- 검증: node --check work/review-ia-v12-check.js 및 node work/test-frame-v12.cjs 통과. 모든 흐름 블록 렌더링, 선택지 수·중복 제거, 신경 전환, 악보 4개 표시 영역, 출처별 mock/미등록 카드, 이동 안내 검사. 대영광송 안내 행의 CSS 덮어쓰기 문제를 실패 검사 후 수정. 실제 브라우저 높이/이미지 렌더링·접근성 전체 검사는 미완료. 검토 승인 대기.\n- 이전 별도 요청인 악보 PDF 재조판은 아직 미완성. 자동 인식 결과에 누락·오인식이 있어 완성본으로 사용하지 않음.\n'''
for name in ['docs/progress.md','design.md','ENGINEERING.md']:
 p=Path(name)
 if name=='ENGINEERING.md':Path('scratch/ENGINEERING.before-v12.md').write_bytes(p.read_bytes())
 p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
p=Path('README.md');Path('scratch/README.before-v12.md').write_bytes(p.read_bytes())
p.write_text(p.read_text(encoding='utf-8')+'\n\n## 최신 검토 v12\nreview/02-ia-v12.html: 선택지별 카드, 참회 호칭/자비송 통합, 날짜별 mock 카드, 주보 악보 슬롯, 두 신경 전환 및 내부 스크롤, 다음 예식 안내. 검사: node work/test-frame-v12.cjs. 외부 데이터 연동·브라우저 실제 레이아웃 QA는 미완료.\n',encoding='utf-8',newline='\r\n')
