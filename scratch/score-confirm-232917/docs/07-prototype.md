# 7단계 Hi-fi 프로토타입 · v1

## 검토 화면
- prototype/index.html: 현재 프로토타입
- review/07-prototype-v1.html: 단일 HTML 검토본 (자산은 기존 로컬 상대 경로)
- 빌드: node tools/build-prototype.cjs

## 확정 기준 적용
- 5단계 가로 두 페이지·오른쪽 목차 접기·제목 고정·바깥 페이지 스크롤·상단 자료 기본 접기.
- 6단계 선택B/입력A/회색 비활성·실선/중앙 안내/오른쪽 패널/악보폭맞춤/저장과 합송 토큰분리.
- 전체 실제 흐름: 날짜·회차·모드·참회/기도 양식·성가 추천/편성/백업·기도문/주보 링크·악보 모달.
- 즉시전환 유지, 새로운 모션·새 공식 본문·새 악보 생성 없음.

## 데이터
- prototype/source/는 원 review/source/를 보존한 별도 소스.
- 최초 원 저장값을 읽고 독립된 missa.prototype.v1.snapshot 저장 공간으로 작업. 기존 키를 덮어쓰지 않음.
- 원 날짜별 자료의 부분 연결/미연결 상태를 그대로 표시. 공식 원문 완비로 주장하지 않음.

## 실행 검수
- node tools/check-review.cjs: 기존앱10명령 PASS.
- node tests/browser-prototype.cjs: 24화면(2방향×3테마×4예식) axe0, 상단/문서넘침0, 목차폭/anchor/제목틈/전례버튼정렬/설정복원/저장격리/악보이미지·Esc초점 PASS.
- node tests/browser-prototype-hymns.cjs: 추천적용/취소,복수곡저장/새로고침,회차분리 PASS.
- node tests/browser-prototype-pagination.cjs: 32조판조합 중간빈페이지0, 참회3양식/안내/제목한행 PASS.
- work/browser-qa/prototype-v1.json / prototype-pagination.json / prototype-landscape.png.
- stylelint·HTML validator CLI 미실행, 실제태블릿/스크린리더/OS확대는 수동검수 별도. 자동규칙위반0은 완전한 접근성 인증이 아님.

## 현재 상태
7단계 사용자 화면 검토 대기. 다음은 수정사항 반영→7단계 확정→8단계 구현·최종 QA. 아직 배포나 8단계 완료 아님.

## 디자인 시스템 대조
<table><thead><tr><th>항목</th><th>프로토타입 값</th><th>시스템 값</th><th>판정</th></tr></thead><tbody>
<tr><td>선택/저장/합송</td><td>B체크면 / 종이바탕실선 / 와인채움</td><td>button-selected / button-primary / assembly</td><td>일치</td></tr>
<tr><td>입력·비활성</td><td>종이surface / 뉴트럴회색실선</td><td>input-* / button-disabled-*</td><td>일치</td></tr>
<tr><td>타이포·형태</td><td>본문명조18px/1.6, UI고딕, .75rem모서리</td><td>reader-body-* / reader-ui-font / reader-radius</td><td>일치</td></tr>
<tr><td>패널</td><td>중앙안내32rem/오른쪽28rem/악보폭맞춤</td><td>overlay-* 공용토큰</td><td>일치</td></tr>
<tr><td>가로배치</td><td>목차12rem·접기, 제목sticky z2</td><td>reader-rail-width / reader-heading-z</td><td>5단계 확정값 재사용</td></tr>
<tr><td>동작·모션</td><td>즉시전환, native dialog</td><td>새모션 없음, 기본top layer</td><td>일치</td></tr>
</tbody></table>

상단 축약 패딩과 참회 제목행 간격은 기존 .25rem/.125rem 토큰을 재사용했다. 검사 범위에서 새로운 디자인값 위반0. 기존 IA CSS의 구조적 상수·전체 CSS 표준 정규화는 8단계 QA와 구분하며 미실행 CLI 검사를 통과로 표시하지 않는다.

## 2026-10-22 선택 날짜 복원 수정
- 사용자: 프로토타입 새로고침 시10/18로 돌아감. 날짜별 상태는 저장하지만 최종 선택일을 저장/복원하지 않는 문제 재현.
- 테스트 저장소 내부 missa.reader.selected-date.v1에 선택일 저장, 시작 시 유효한 날짜를 먼저 복원한 후 날짜별 회차·모드·본문위치 상태 로드. 원 앱 저장소 변경 없음.
- tests/browser-prototype-date-reload.cjs로 실제 검수 iframe 새로고침 재현/검증.

## 2026-10-22 사용자 새로고침 복원 확인
- 사용자: 프로토타입 새로고침 후 날짜와 성가 설정 모두 복원됨을 직접 확인. 해당 재현 문제 해결 확인.
- 이 확인을 모든 사용흐름/7단계 전체 승인으로 확장하지 않음.
- 다음: review/07-flow-review-v1.html의②읽기·표시에서 낭송/성가·기도양식 전환, 목차접기·테마·글꼴 변경 시 읽기위치 유지 확인.

## 2026-10-22 사용자 읽기·표시 검토 피드백
- ②읽기·표시 안내 후 사용자 “응 잘 되는 거 같아”. 현재 확인 범위에서 발견 문제 없음으로 기록. 명시적7단계 최종 승인이나 모든 체크 완료로 해석하지 않음.
- 다음: ③보조 화면의 메뉴/안내/악보 열기·닫기·복귀 확인. 이후7단계 최종 승인 검토.
