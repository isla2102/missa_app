# 코디·웹디 8항목 재검수 · 2026-10-23

확정 전 샘플 수정. 원본 prototype/SSOT 토큰 변경 없음. 웹디 독립 읽기 검수 + 코디 렌더러 수정/실측.

| 항목 | 수정 샘플 | 기존 시스템/발견값 | 판정 |
|---|---|---|---|
| 제목 행 | 공통 최소32px·중앙정렬, 제목20px/1.3 | 제목26·선택32·입력44px가 행높이에 혼재 | 수정 제안 |
| 제목 하단 | 고정제목 padding0 + 페이지 row-gap8px | margin/padding 중첩 | 단일 gap으로 수정 |
| 숫자 입력 | 32px, 세로4px | 기본44px | 선택 컨트롤과 통일 |
| 악보 여백 | 카드상하12px, figure margin0, 도구영역 상하32px | top margin8·caption/source8 중첩 | 상하 대칭 |
| 크게 보기 | 우상단 absolute z3 | 문서흐름 static | 배치높이 영향 제거, 음표 영역은 침범하지 않음 |
| 기호/본문 열 | 공통 좌우12px, marker20px+gap6px | 합송만12px, 다른 발화0px | 3테마 시작선 일치 |
| 안내 열 | 빈 marker+본문셀,14px 고딕 | 독립안내 직접삽입/폰트상이 | 동일 구조 |
| 신앙고백 안내 | 제목우측 ⓘ→중앙 안내창,키보드지원 | 각양식 본문전 p | 중복제거·행내 배치 |

독서 표제(기호 없는 맨 첫 제목)는 전체폭 유지. 다음 기호 전 계속줄은 같은 paragraphBody에 누적하는 기존 규칙 유지. 본문·공식 문구는 변경하지 않음.

검사: browser-eight-point-review 3테마 제목32px/입력32px/기호20px·본문시작선동일/안내14px·2열/신경안내창/악보상하대칭/overlayz3 PASS. browser-frame-inspection 1024×768/모드변경치수동일 PASS. browser-rail-icons 3테마 축소목차/설정/좌표고정/axe0 PASS.

증거: work/browser-qa/eight-point-review.json, eight-point-title-entry.png, eight-point-columns.png. 실제 악보 원본 이미지 자체의 흰 여백은 CSS 여백과 구분하며 변경하지 않음.

다음: 검수 보더/실제 화면에서 사용자 8항목 시각 확인 후 제안 시스템 확정. 실제 태블릿/스크린리더 미검수, 표준 CSS/HTML CLI는 이번 실행 안 함.
