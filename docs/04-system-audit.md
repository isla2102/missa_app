# 4단계 시스템 검수 · 2026-10-22

범위: 승인된 색·본문 타이포·간격·모서리와 기존 상태/레이어 값의 토큰 정리. 기존 배치 수치는 호환 기준이며 5단계 시안을 승인한 것은 아니다.

<table><thead><tr><th>항목</th><th>시안 값</th><th>시스템 값</th><th>판정</th></tr></thead><tbody>
<tr><td>강조색</td><td>밝음 #70283F / 다크 #E0A3B5</td><td>foundation-theme-accent → ui-theme-accent → reader-theme-accent</td><td>일치</td></tr>
<tr><td>배경</td><td>A 미색 / B 종이 / C 와인 다크</td><td>테마별 foundation 값과 의미 별칭</td><td>일치</td></tr>
<tr><td>타이포</td><td>본문 명조 1.125rem / 1.6, 제목 고딕</td><td>reader-body-* / reader-ui-font</td><td>일치 · Chrome 실측</td></tr>
<tr><td>간격·모서리</td><td>기본 간격 / 모서리 .75rem</td><td>reader-padding/gap/content-inset/radius</td><td>일치</td></tr>
<tr><td>레이어</td><td>선택 카드0 / 선택 마커1 / 악보·안내2</td><td>foundation → ui → reader z 토큰</td><td>일치</td></tr>
<tr><td>상태</td><td>선택 와인색, focus 3px currentColor</td><td>reader-theme-* / state-focus-ring</td><td>기존 값 보존</td></tr>
<tr><td>레이아웃·모션</td><td>기존 가로/세로 배치, 신규 모션 없음</td><td>기존 치수만 토큰 이동</td><td>변경 없음 · 배치 개선은 5단계</td></tr>
</tbody></table>

## 실행한 검사
- Node 통합 10명령 PASS.
- Chrome 가로/세로 ×4예식: 8화면 axe 자동 규칙 위반0, 상단 가로 넘침0, 오류0. 읽기 위치 복원 / 악보 모달 Esc·초점 복귀 PASS.
- A/B/C 설정창 axe0, 테마 저장복원과 anchor 유지 PASS.
- 본문 명조18px/1.6, 제목 고딕 유지, 고딕 전환·저장복원 PASS.
- 정적 rg: reader.css의 !important / 인라인 style / 직접 hex색 / 숫자 z-index / media·container 0건. styles/tokens.css만 색 선언.
- 새 배치 시안: 1024×768, 목차 접기 전 페이지385px → 접은 뒤481px. 세로 전환 / 악보 전환 / axe0 PASS. PNG 직접 확인.

## 검사 한계와 다음 범위
- stylelint·html-validate CLI는 이번에 실행하지 않았다. rg와 axe가 이 도구들을 대신한 전체 표준 인증은 아니다.
- 컨트롤의 모든 상태 세부 설계는 6단계, 실제 기기 검증·공식 본문 연결·권리 확인은 별도다.
- 현행 CSS에 있는 구조적 상수와 요소별 기본 글자 크기 등의 전체 정규화는 컴포넌트 검수 때 추가 확인한다. 4단계 기초 토큰 검수와 앱 전체 최종 QA를 구분한다.
