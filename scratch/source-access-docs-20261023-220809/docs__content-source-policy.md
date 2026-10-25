# 콘텐츠 출처와 이용 조건 — 2026-10-19

## 사용자 지정 출처
- 통상문 순서 대조: https://maria.catholic.or.kr/mi_pr/missa/ordinary.asp?day=20261019&missaid=16875
- 대구대교구 주보: GOODNEWS 교구코드 21. https://maria.catholic.or.kr/jubo/jubo_list.asp?jgubun=G&s_gyocode=21
- 주요기도문: https://maria.catholic.or.kr/mi_pr/prayer/prayer.asp . 21개 명칭과 원문 링크를 연결, 새 전문을 앱에 내장하지 않음.
- 성가표: 사용자 첨부 2026년 10월 성가표(수정보완판).hwp. 출처 https://bbs.catholic.or.kr/pdsm/bbs_view.asp?id=212615&menu=4807 . 31일치 표 구조를 읽었으며 본당/회차 편성은 자동 확정하지 않음.
- 월간 고유기도문: https://www.cbck.or.kr/Board/K7020 . 2026년 12월 게시글 https://www.cbck.or.kr/Board/K7020/20262479 (2026-10-15 게시, HWP/HWPX 첨부 존재 확인). 10월은 /20261395.
- 고유기도문 게시판을 독서·복음까지 포함한 월간 미사 전체 데이터로 간주하지 않음. 첨부 전문 수록 범위는 내려받아 검사하지 않았음.

## 저작권 확인
일반 안내 https://www.cbck.or.kr/Copyright : 전재·복제 승인과 자동화 도구 이용 제한 명시.
사용 규정 https://www.cbck.or.kr/Board/K7300/20230535 : 제1·3조의 교구/본당 공적 사목과 개인 사용 범위 구분, 제8조의 앱 관련 제한 확인. 현재 개인 로컬 프로젝트가 면제 대상이라고 단정하지 않음.
새 전문 내장과 추가 자동 수집은 보류. 출처 링크와 사용자 제공 성가표 분석만 새로 연결. 기존 검토 데이터는 삭제하거나 이용 허가가 확인된 것으로 변경하지 않음. 앱 내장·배포·오프라인 저장·성가 악보 이용 범위를 저작권자에게 서면 확인하는 단계가 남아 있음. 문의는 실제 발송하지 않았음.
기록: data/reference-sources/rights.json . 원문을 임의 변경하거나 새 공식 문구를 생성하지 않음.

## 검증
단일 생성기와 tests/reference-catalogs.cjs 및 reader-regression 검사에 출처 연결을 추가. tools/check-review.cjs 7개 명령 성공.
실제 Chrome tests/browser-references.cjs: 주요 기도문 21개 링크, 10월18일 추천 번호, 날짜에 맞는 대구 PDF 링크 및 pageerror 0 확인.
현행 review/02-ia-current.html, 새 참고 기준 review/02-ia-v54.html. PDF 본문 복제나 주보 화답송 자동 인식·전례문 전체 수입을 구현한 것은 아님.


## 2026-10-23 사용자 자료실·교회음악 조사
- 요청: 고유기도문·성가표·ENC 정리 및 미사 순서/의미 중심 강의 조사자료 준비.
- 원본 7개를 유지하고 data/source-library에 SHA256 검증 사본 배치. ENC ZIP 525개 한글 파일명 복원. HWP 본문은 미판독, ENC 미변환.
- 수원교구 홍보국 게시글 112757(2026-08-26), 10월 고유기도문 제목·첨부명 확인. 원격 첨부 바이트 비교 및 11·12월 개별 게시글 대조는 미실행.
- docs/research/church-music: 전체83목록·관련16선별노트·미사흐름·60분강의초안·앱연결계획. 개인 해설/공식 지침/미판독 첨부 구분.
- 열람: review/07-research-library-v1.html. 앱 전문 자동 수입과 사용자 편성 변경은 하지 않음.
- 다음: review/07-state-review-v1.html에서 7단계 선택·설정·편성·안내 통합 검수. 이후 HWP 하루분 판독·연결 샘플 검토. 8단계 승인으로 취급하지 않음.
- 기존 전문 자동 수집 보류 원칙은 유지. 이번 사용자가 제공한 로컬 원본 정리와 공개 해설의 짧은 조사 요약만 수행. 공개 다운로드와 앱 재배포 이용 조건은 구별.
