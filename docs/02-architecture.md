# 하루치 실제 전례문 연결 — 아키텍처 제안

상태: APPROVED. 사용자 “진행하세요”로 범위·구조 승인. 2026-10-19. 입력: docs/01-brief.md, docs/02-ia.md, v43.

## 데이터 흐름
확인된 출처 → 수동 검토한 날짜별 JSON → Schema/참조 검증 → 공통 MassDocument → 회차 HymnSet 및 모드 적용 → 기존 리더 조판.

## 파일 범위
- data/days/2026-10-18.json: 확인된 날짜별 본문, 선택지와 출처 참조.
- data/sources.json: URL·확인 시각·이용 조건 검토 상태·수집 방식. 공개 열람을 재배포 허가로 간주하지 않음.
- schemas/mass-document.schema.json: 실제 검증용 JSON Schema.
- work/daily-document.cjs: 순수 검증/선택 함수. 아직 본 앱 src 구현 단계로 이동하지 않음.
- work/test-daily-document.cjs: 정상/날짜 불일치/중복 ID/미제공/회차 동일성 테스트.
- review/02-ia-v44.html: 승인 후 작성할 단일 검토 파일. 검증된 JSON을 빌드 때 포함하여 file:// 실행과 오프라인 대응.
- docs/03-test-plan.md, docs/04-verification.md: 실행 결과·남은 실기 검증 기록.

## 모델과 인터페이스
MassDocument: schemaVersion, documentId, date, observance, sourceRefs, sections.
Section: id, kind, title, paragraphs, variants, status.
Paragraph: id, role, text, sourceRef. 문자열에 실행 HTML 저장 금지.
status: verified / missing / needs-review. null 본문은 공식 본문처럼 렌더하지 않음.
HymnSet: date, slotId, entrance/offertory/communion/recessional. 본문 override 필드 금지.
validateDocument(document, sources) → errors[]
selectDocument(documents, date) → document|null
resolveAnchor(document, anchor) → sectionId/paragraphId/offset

## ADR
1. 수동 확인한 하루치 저장본부터 연결. 실시간 API 존재를 가정하지 않고 네트워크 실패와 본문 오류를 분리.
2. 기존 브라우저 검토 HTML을 유지. Flutter/SQLite 도입은 이번 범위에서 제외.
3. 안정적인 콘텐츠 ID로 위치를 참조. 페이지 번호는 재조판으로 바뀌므로 저장 기준으로 사용하지 않음.
4. 공식 페이지 원문·판독 초안·본당 주보는 출처를 분리. 미제공 악보/기도는 기존 상태 표시 유지.

## 검증
Red: mock 대신 실제 문서 선택, 날짜 불일치 차단, 중복 ID 및 잘못된 sourceRef 차단 테스트를 먼저 실패 확인.
Green: 최소 데이터 어댑터와 렌더 연결. 회차 공통 본문 불변 및 모드/위치 보존 회귀 검사.
실제 태블릿: 긴 본문, 스크롤 끝, 글자 크기, 방향 전환, 키보드 초점, 새로고침 복원 확인. 모의 DOM 테스트를 실제 브라우저 통과로 간주하지 않음.

## 조사 기록
기존 daily-missa-20261018.json은 본기도 선택지 저장본이며 하루 전체 데이터가 아님.
공식 날짜 페이지 후보: https://missa.cbck.or.kr/460404 (2026-10-18 검색 결과 확인). 본문·출처·이용 조건 상세 확인은 구현 작업의 입력 검증에서 수행.

## 승인
이 문서의 범위와 데이터 구조 승인 후 cod-e Stage 3 TDD 진행. 새로운 시각 디자인 단계의 승인으로 간주하지 않음.
