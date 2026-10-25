# 6단계 컴포넌트 통합 최종 검수

2026-10-22 · 기준 review/06-integrated-v1.html. 단계 최종 승인은 대기. 승인된 개별 결정과 전체 단계 승인을 구분한다.

## 시스템 대조
<table><thead><tr><th>항목</th><th>시안 값</th><th>시스템 값</th><th>판정</th></tr></thead><tbody>
<tr><td>선택 버튼</td><td>와인12% 면+체크·굵기</td><td>button-selected-* / aria-pressed</td><td>일치</td></tr>
<tr><td>입력칸</td><td>테마 종이 surface, 얇은 실선</td><td>input-surface/ink/line, field.css</td><td>일치·Chrome 실제 배경색 대조</td></tr>
<tr><td>비활성</td><td>밝음#737373, 어두움#AAAAAA·옅은 실선</td><td>button-disabled-* / button.css</td><td>일치</td></tr>
<tr><td>타이포</td><td>본문1.125rem/1.6 명조, UI고딕</td><td>reader-body-* / reader-ui-font</td><td>일치</td></tr>
<tr><td>형태·간격</td><td>모서리.75rem, 기존기본간격, 높이44px</td><td>reader-radius/control-hit/padding/gap</td><td>일치</td></tr>
<tr><td>안내창</td><td>중앙32rem, 높이 최대90dvh</td><td>승인한 안내 시안 기준</td><td>일치·가로 중앙 실측</td></tr>
<tr><td>악보</td><td>폭100%, 추가확대버튼0, 닫기만 유지</td><td>사용자 모달 폭맞춤 결정</td><td>일치</td></tr>
<tr><td>메뉴·설정 패널</td><td>오른쪽28rem</td><td>기존 시안의 제안 값</td><td>통합 최종 확인 대상</td></tr>
<tr><td>레이어·모션</td><td>native dialog top layer, 신규모션없음</td><td>숫자 z-index 없이 기본 모달</td><td>일치</td></tr>
</tbody></table>

## 실행 결과
- tests/browser-components-integrated.cjs PASS. 3테마×(기본화면+메뉴+설정+안내+악보) 15건 axe WCAG2/2.1/2.2 A·AA 자동규칙 위반0, JS오류0.
- 버튼·입력·선택기 최소44px. 입력 정상→오류→정상 복구와 첫 오류 초점. 오류 문구 연결.
- Tab으로 배경 컨트롤에 초점이 가지 않음 확인. 네이티브 모달은 브라우저 주소창으로 Tab 이동할 수 있어 body가 activeElement인 경우는 구분했다. 실제 스크린리더 검증으로 주장하지 않는다.
- Esc 종료 및 원래 열기 버튼 복귀. 메뉴→설정 이동 후 종료 시 메뉴 열기 버튼으로 복귀.
- 악보 로드, 이미지폭=스크롤영역폭, 가로넘침0, 닫기버튼1개. 종이색 유지.
- 320px에서 문서 가로넘침0. 안내·설정·악보 모달이 화면 안에 들어옴. 가로1024 고정 비교 프레임은 자체 가로스크롤.
- localStorage 전후 동일. 실제 편성 저장 없음.
- work/browser-qa/integrated-v1.json / integrated-v1.png. PNG 직접 시각 확인.
- rg: 공용 button.css/field.css !important·인라인 style·숫자z-index·media/container 0건.

## 범위와 남은 확인
- stylelint/HTML validator CLI는 이번에 실행하지 않았다. axe·정적검사는 전체 웹 표준 준수의 대체 인증이 아니다.
- 컴포넌트 SSOT는 tokens.css 및 styles/components/button.css/field.css. 통합 HTML은 이를 임베드했다.
- 메뉴·안내·악보 모달 치수는 기존 시안의 draft 변수를 유지. 6단계 전체 승인 후 공용 오버레이 토큰/CSS 확정이 필요하다.
- 실제 태블릿·화면 낭독기·OS 글자 확대 검증, 실제 콘텐츠 연결 및 권리 확인은 별도다.
- 사용자 통합 승인 후 6단계 문서/토큰 확정, 7단계 실제 미사 흐름 Hi-fi 프로토타입으로 진행한다. 현재 앱 기능에 아직 이 모든 디자인을 적용했다고 주장하지 않는다.
