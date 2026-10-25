# 지시문 스타일·2열 정렬 정규화

2026-10-24. 사용자 요청에 따라 지시문 규칙 통일. 7단계 유지.

## 원인과 수정
원문 지시문 추가 시 일부 섹션·악보 지시문은 p로 직접 삽입되어 기호 열을 건너뛰었다. 스피치 문단 margin:0은 지시문 상하 여백도 덮어썼다.
`normalizeGuidance`가 직접 삽입된 지시문을 빈 기호 열+본문 열의 공통 스피치 행으로 변환한다. 이미 본문 열 안인 지시문은 중복 래핑하지 않는다. 낭송/성가 전환 후에도 같은 처리를 적용한다. CSS는 원래 규칙을 수정하고 불필요한 중복 덮어쓰기를 제거했다.

## 시스템 대조
| 항목 | 화면 값 | 시스템 값 | 판정 |
|---|---|---|---|
| 지시문 글자 | 14px 고딕/400 | --reader-guidance-size / --reader-ui-font | 일치 |
| 줄간격 | 1.6 | --reader-system-leading-body | 일치 |
| 상하 여백 | 4px/4px | --reader-system-space-1 | 일치 |
| 자체 패딩 | 0 | 기존 지시문 규칙 | 일치 |
| 기호 열/열 간격 | 20px/6px | --reader-marker-width / --reader-marker-gap | 일치 |
| 독립 지시문 좌우 래퍼 | 12px/12px | --reader-system-space-3 | 일치 |
| 카드 흐름 간격 | 8px | --reader-system-flow-gap | 유지 |
| 미색·종이 지시문 | #75501C | --reader-system-note-ink | 일치 |
| 다크 지시문 | #E3C18C | 동일 토큰 테마 값 | 일치 |
| 합송 내 지시문 | 응답면 대비색 | --reader-system-note-on-response | 일치 |

## 검사
- `node tools/check-guidance-normalization.cjs`: 프로토타입·검수 샘플 각각 3테마×두 모드×전체 전례 블록. 총738회 표시 지시문 실측, 정렬/색상/글꼴/행간/마진/패딩 위반0.
- 기본 참회 양식 상태를 사용한 전체 블록 검사. 모든 사용자 입력·날짜 조합의 검사를 뜻하지 않는다.
- 기존 `node tools/check-missal-rubrics.cjs` 256검사 PASS, 브라우저 JS 오류0. 이 검사에서 참회 세 양식의 개별 렌더링도 확인.
- 캡처: work/browser-qa/guidance-normalized.png.
- 새 색상·간격 값이나 모션·z-index·반응형 조건을 추가하지 않음. 스타일린트/axe 전체 검사를 이번에 재실행한 것은 아님.

## 다음
현재 화면에서 독립/합송 내부/악보 위 지시문의 읽기 흐름을 확인하고, 현재 표시 통상문 전체의 경본 항별 문구 교감을 진행한다.
