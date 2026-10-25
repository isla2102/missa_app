# 검토 화면 원본

현재 화면 기준은 승인된 변경을 누적한 v53입니다. 이 폴더는 검토 HTML 유지보수용이며 웹디자인 8단계의 src 앱 구현이나 디자인 시스템 확정을 뜻하지 않습니다.

## 생성
프로젝트 루트에서 `node tools/build-review.cjs` 실행. 결과는 `review/02-ia-current.html`. 브라우저에서 직접 열 수 있으며 실행 중 외부 JSON fetch가 필요하지 않습니다.
전체 검사: `node tools/check-review.cjs`. 세부 로그: `work/review-check.log`.

## 수정 위치
- shell.html: 시맨틱 마크업, 버튼·모달 구조.
- reader.css: 기존 draft 레이어 스타일. 시각 값 신규 확정 아님.
- reader.js: 렌더링·페이지·세로 연속 보기·이벤트. JSON/검증/저장 모듈은 placeholder로 포함.
- daily-document.cjs / reader-state.cjs: 날짜 데이터 검증·선택·앵커, 저장 값 검증·읽기·쓰기. Node 검사와 브라우저가 같은 구현을 사용.
- build.json: 데이터 파일 연결과 출력 위치. date fixture 추가 시 이 파일의 dailyDocuments 입력을 변경하고 검사.
- score-preview-sizes.json: 기존 v53의 악보 미리보기 크기 메타데이터.
- data/days/ 및 data/sources.json: 확인한 날짜 본문·출처.
- docs/교중미사악보/reengraved/registry.json: 현재 악보 PDF/SVG 연결. 조판 자산 변경 시 크기 메타데이터도 갱신.

## 보존 및 범위
과거 v1~v53 HTML, work/의 버전별 수정 스크립트와 악보 조판 자산은 이력으로 보존. 새 화면 생성은 과거 HTML 또는 버전별 패치 스크립트를 읽지 않습니다. 과거 스크립트는 최신 원본 수정에 사용하지 않습니다.
악보 재조판 알고리즘 자체의 통합은 이번 HTML 생성 정리의 범위에 포함하지 않았습니다. 현재 PDF/SVG를 그대로 연결하므로 음표와 조판이 바뀌지 않습니다.
기존 저장 키 유지. file://의 저장 공유 방식은 브라우저에 따라 다를 수 있어 새 파일에서 이전 파일의 위치가 반드시 자동 이전된다고 보장하지 않습니다.
