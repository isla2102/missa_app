# 디자인 정규화 검수 · 2026-10-22

| 항목 | 시안 값 | 시스템 값 | 판정 |
|---|---|---|---|
| UI 글꼴 | 고딕 1rem / 1.6 | 공용 button/input 토큰 | 일치 |
| 선택 B | 체크·굵기·부드러운 배경, 밑줄 없음 | 승인 B | 일치 |
| 합송 | 세 테마 border 0 / shadow none | 추가 스트로크 없음 | 일치 |
| 저장 | 종이색 바탕·와인 윤곽선 | action 역할 토큰 | 일치 |
| 동적 복원/취소 | 생성 시 공용 클래스 | 정적 버튼과 동일 | 일치 |
| 제목 간격 | 제목 행이 소유 | 중복 여백 제거 | 일치 |
| A/C 카드 경계·제목 | draft 변수 | 현재 시스템 변경 전 | 사용자 선택 대기 |

자동 검사: tests/design-system-contract.cjs, browser-normalization-contract.cjs, browser-prototype.cjs, browser-prototype-pagination.cjs, browser-prototype-date-reload.cjs, browser-prototype-score-confirm.cjs, browser-prototype-hymns.cjs, browser-hierarchy-comparison.cjs PASS.

이미지 증거: work/browser-qa/normalization-comparison.png. CSS/HTML 표준 CLI 검사는 미실행이며 이 검사가 이를 대체하지 않습니다.
