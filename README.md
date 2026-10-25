# MISSA — 매일미사 예비신자 앱

한국어 예비신자와 일반 신자가 전례문·순서·성가를 한 화면에서 확인하도록 돕는 개인용 로컬 MVP입니다. iPad·Android 태블릿 가로 두 페이지 리더가 목표입니다.

## 현재 상태 (2026-10-19)
- 현행 검토: review/02-ia-current.html. v53 동작과 데이터 유지.
- 생성: `node tools/build-review.cjs`
- 전체 검사: `node tools/check-review.cjs` (6개 명령, 상세 work/review-check.log)
- 원본/설정: review/source/README.md. 기존 버전 HTML과 과거 work 스크립트는 이력으로 보존합니다.
- 실제 태블릿/보조기기 검증, 전체 날짜 연동 및 디자인 후속 단계는 미완료입니다.

## 사용자 결정
- 실제 본당명은 미설정, ‘내 본당’ 하나로 시작합니다. 실제 시간·성가 번호를 생성하지 않습니다.
- 회차는 새벽미사·교중미사·주일 저녁 젊은이 미사입니다. 젊은이 미사는 일요일 저녁입니다.
- 세 회차는 동일한 전례일·본문·순서·안내 규칙을 공유하고 입당·봉헌·영성체·파견 성가만 다릅니다.
- 상단에는 날짜·회차·사용자 모드, 오른쪽 Drawer에는 보기 설정을 둡니다.
- 전례 시나리오 선택은 안내 패널의 ‘개발용 예시’로 구분합니다. 회차 선택으로 시나리오나 전례 날짜를 변경하지 않습니다.
- 모드는 같은 본문의 표시만 변경하며, 모드·회차 전환 시 읽기 위치를 유지합니다.

## 문서와 원본
- `.ai-workspace/agent.md`: 유일한 에이전트 작업 지침 (루트 agent.md 없음)
- `progress.md` → `docs/progress.md`: 진행·승인·검수 기록
- `design.md`: 제품·데이터·정보 구조 결정. 4단계 디자인 토큰 확정 문서로 오인하지 않습니다.
- `MISSA_MVP_v0.2.zip`: 수정하지 않은 원본
- `work/original-v02.html`: 원본 확인용 추출 HTML. 브라우저에서 열 수 있지만 알려진 임의 시간·가상 본당 문제가 남아 있습니다.

## 실행 및 검증 상태
앱 빌드·개발 서버·자동 테스트 명령은 아직 구성되지 않았습니다. Flutter·SQLite는 권장 아키텍처이며 구현된 스택이 아닙니다. 브라우저 동작·CSS·HTML·접근성 검사는 아직 실행하지 않았습니다.

최종 산출물은 수정 HTML, 검증용 JSON Schema, 설계 노트, ZIP, 검사 결과입니다. 기존 v0.2 JSON은 데이터 예시 객체이며 실제 JSON Schema는 아닙니다. 공식 문구를 추측 생성하지 않고 출처·이용 조건을 기록합니다.

## AI 에이전트 협업 체계
중앙 통제실은 `.ai-workspace/`입니다.
- `agent.md`: 행동 강령
- `design.md`: 설계 규칙
- `handoff.md`: 인수인계 및 다음 작업
- `Project_Status.md`: 진행 상태
- `project_skills/`: 프로젝트 전용 스킬
- `global_skills/`: 글로벌 스킬 연결

위 중앙 문서들은 `.ai-workspace/` 아래에 있습니다. 제품 결정은 루트 `design.md`, 현재 진행은 `docs/progress.md`를 기준으로 확인합니다.

`.claude`, `.codex`, `.gemini`, `.antigravity`, `.antigravity-ide`는 중앙 통제실에 연결됩니다.

인수인계: `/핸드오프 넘겨줘`, `/핸드오프 이어받아`

웹디자인은 사용자 지정 8단계 승인 절차를 따릅니다. 개발 실행 명령은 기술 스택 확정 후 기록합니다.

## 최신 검토 화면
현재 검토: review/02-ia-v6.html. v5 외곽 구조 승인 후 2단계 본문 프레임을 추가 보완 중입니다. 본문은 Lorem ipsum mock이며 공식 데이터 연동·자동 조판은 미구현입니다. 회귀 검사: node work/test-frame-v6.cjs.

## 최신 검토 v9
review/02-ia-v9.html: 기본 교중미사, 제목 옆 낭송/성가 버튼, 사용자 제공 임시 사진 악보. HTML과 docs/교중미사악보 폴더의 상대 위치를 유지해야 합니다. 원본 사진은 보존하며 매핑은 해당 폴더의 temporary-score-manifest.json에 기록했습니다. 검사: node work/test-scores-v9.cjs. 실제 조판·공식 콘텐츠 자동 연동은 미구현입니다.

## 최신 검토 v10
review/02-ia-v10.html: 본문 높이 기반 페이지 분리, 악보 카드 내부 스크롤. 검사: node work/test-pagination-v10.cjs. 현재 mock 본문과 사용자 제공 임시 교중 악보를 이용한 프레임 검토이며 최종 자동 조판 QA는 미완료입니다.

## 최신 검토 v11
review/02-ia-v11.html: 사용자 제공 통상문 사진을 판독한 텍스트 초안과 한 쪽 높이의 악보 카드. 참조는 docs/references/교중미사_통상문_텍스트_초안.md 및 .json이며 원본 통상문 사진은 실행 참조하지 않습니다. 검사: node work/test-ordinary-v11.cjs, node work/test-reader-regression-v11.cjs.


## 최신 검토 v12
review/02-ia-v12.html: 선택지별 카드, 참회 호칭/자비송 통합, 날짜별 mock 카드, 주보 악보 슬롯, 두 신경 전환 및 내부 스크롤, 다음 예식 안내. 검사: node work/test-frame-v12.cjs. 외부 데이터 연동·브라우저 실제 레이아웃 QA는 미완료.


## 최신 검토 v13
review/02-ia-v13.html: 합송 강조 카드·안내 분리, 인사 사제 선택지 3개와 공통 합송 1개. 검사: node work/test-assembly-v13.cjs. 실제 브라우저 레이아웃 검증은 남아 있습니다.


## 최신 검토 v16
review/02-ia-v16.html: 기호/본문 별도 열 정렬, 인사 단일 제목·대안 카드, 첫 방문/재실행 튜토리얼, 날짜 옆 전례일·시기 배지, 매일미사 본기도 저장본 카드. 검사: node work/test-reader-v16.cjs. 악보 PDF 전체 교체 및 실제 브라우저 QA는 미완료. 본기도/전례일은 2026-10-18 확인 자료이며 실시간 API가 아닙니다.


## 최신 검토 v17
review/02-ia-v17.html: 아멘 재조판 부분 반영(PDF+SVG+MusicXML), 입당 성가 한 페이지 mock, 본문 컨테이너 내부 안내. 검사: node work/test-reader-v17.cjs, 번들 Python work/check_amen.py. 새 PDF는 output/pdf/amen-reengraved.pdf. 다른 곡의 전체 재조판은 미완료입니다.


## 최신 검토 v18
review/02-ia-v18.html: 공통 악보 모달(PDF/사진/mock), 봉헌·예물 준비 분리, 네 성가 mock, 매일미사/주보 mock 카드, 감사기도 제2양식, 본당 시기별 응답과 시기 기간 모달, 파견 4+1, 저녁미사 축약. 검사: node work/test-reader-v18.cjs. 시기 데이터는 2026 한정, 전체 전례력·외부 자료 API 미구현. 재조판 등록 목록: docs/교중미사악보/reengraved/registry.json(현재 아멘).


## 최신 검토 v19
review/02-ia-v19.html: 자비송·맺음 환호 PDF 추가, 365번 알렐루야 후렴/성가대/후렴 카드, ZIP 출처·번호 확인 상태 연결. 재조판 총4항목, 추가5곡 재스캔 대기. 검사: node work/test-reader-v19.cjs 및 번들 Python work/check_manual_scores.py. 상태: docs/references/score-engraving-status.json.


## 2026-10-18 어린양 재조판·주석6건 v22
- 새 사용자 사진2장을 rescan-20261018에 원본/해시 보존. 어린양을 54음/6시스템 PDF/SVG/MusicXML 조판, 1·2절 반복을 펼쳐 표기. 긴 낭송음/페르마타/3절 평화를 주소서 포함. 새 사진과 대조하고 PDF PNG 실제 열어 확인. 본당 최종 교정 전. 완료5항목, 재스캔4곡 남음.
- 4종 성가 카드 번호 엔트리(1~528)+악보 보기. 날짜/회차/성가종별 메모리 편성, 번호 임의 초기지정 없음. 공식 굿뉴스 단성 2012 이미지 경로를 원격 img로 표시, 로컬 미디어 다운로드하지 않음. 1/2/365/528 경로 확인, 전체528곡 로딩 미검증. 수정개정판과의 판본 일치 미확인, 공식 수정개정판으로 확정 표시하지 않음. 이미지 실패 안내.
- 악보 크게보기 버튼은 figure 상대 위치 위 compact overlay. 크기/패딩/z-index는 draft토큰. 기존 native dialog 유지.
- 참회 선택2의 호칭 안내, 본기도 확인자료 라벨/두수록본문 안내 제거. 강론 원문없음 대신 중립 카드: 앉아서 강론을 듣고 말씀을 삶에 새김.
- 보편 지향 기도 응답의 낭송/악보 버튼 없음. 사용자 확정된 교중은 chant-pending-score 표시, 선율 자료 요청 카드+본문fallback. 새벽/저녁은 선율 및 노래 여부 미확인으로 기존 본문. 실제 음표 악보는 자료가 없어 미완료, 임의 작곡하지 않음. 사용자 명시 변경으로 회차별 이 응답 표시정책 차이 허용.
- node --check work/review-ia-v22-check.js, node work/test-reader-v22.cjs, 번들 Python work/check_agnus.py 통과. 폼 번호/범위/remote경로/확대·모드/도움말삭제/강론카드/응답정책/기존흐름 회귀. PDF1쪽·벡터·54음·원본멜로디·가사·바이트동일 검사. 실제 브라우저 원격img·좌표·PDFplugin 검증 미실행.
- 최신 review/02-ia-v22.html, v21 보존. 2단계 보완, 다음 단계 승인 아님.


## 2026-10-18 주님의 기도 우선 조판·참회 전환 v24
- 새 주님의 기도2 사진2장 원본/해시 보존. 앞부분80음+이어서55음, 12/8박자20마디 전부72tick. 점4분음표72, 페르마타·붙임줄·슬러·마지막 천천히 표시. PDF2쪽 합본/SVG2개/MusicXML2개. 원본 대조 및 PDF PNG 두 쪽 직접 열어 가사·레이아웃 확인, 본당 최종 교정 전. 뷰어 기존사진을 새PDF/SVG로 교체, 크게보기 각쪽PDF 유지. 완료6항목.
- 보편 지향 기도 응답: 사용자 요청으로 하나의 카드 안에 낭송/악보 버튼. 악보 탭에는 준비 중 및 실제 응답본문, 선율을 임의 생성하지 않음. 녹음 요청하지 않음.
- 참회 예식: 두 선택지 동시나열 대신 고정 높이 카드 내부 스크롤과 전능하신 하느님과/진심으로 뉘우치는 두 버튼. 전체 해당양식만 표시, 첫선택지 기본. 원본 텍스트 보존, 독립적 페이지분할 제외. 버튼 클릭은 메모리상 표시전환, 실제 사제양식 자동판정 아님.
- 대영광송 손글씨 수정은 실제 본당 역할구분으로 사용자가 확정. 대영광송/거룩하시도다/신앙의 신비여 새사진 수신, 재촬영 필요가 아니라 조판 대기. 이번 사용자 지정 우선 작업은 주님의 기도.
- node --check work/review-ia-v24-check.js, node work/test-reader-v24.cjs, 번들 Python work/check_lords.py 통과. PDF 벡터/2쪽/135음/20마디72tick/한글/파일동일 검증, 기존UI회귀+참회버튼/단일카드/본문전환/응답카드/주님의기도2assets 검사. 실제브라우저 높이/PDFplugin 시각QA는 미실행.
- 최신 review/02-ia-v24.html, v23 보존. 2단계 보완, 이후단계 승인 아님.

### 악보 폭 자동맞춤 조판
- work/autofit_scores.py: 기존 MusicXML을 읽어 297mm 폭 조판 및 역할별 줄 나눔. work/music-deps의 Verovio/svglib/reportlab 및 pypdf 사용.
- work/bundle_autofit.py: 짧은 곡을 같은 쪽에 담아 output/pdf/parish-scores-autofit.pdf 생성.
- 검토 화면 review/02-ia-v36.html은 docs/교중미사악보/reengraved/autofit/ 자산을 사용.

악보 v40 재생성: 번들 Python으로 `work/uniform_scores.py` 실행. 기존 확대 SVG에서 가사 크기와 시스템 간격을 보정하고 A4 PDF, 연속 SVG, review/02-ia-v40.html을 생성합니다.


## 2026-10-19 현재 계획
최신 검토는 review/02-ia-v43.html, 통합 결정은 docs/02-ia.md. 다음은 2026-10-18 실제 본문 하루 연결이며 docs/01-brief.md와 docs/02-architecture.md에 범위/구조를 기록했습니다. 구조 승인 전으로 데이터 연결 구현은 미착수입니다.

## 실제 전례문 검토 v44 (2026-10-19)
review/02-ia-v44.html을 열면 2026-10-18 하루 저장본을 사용합니다. 다른 날짜는 미연결로 표시합니다. 주보 화답송 악보·사제 마침 기도·본당 공지는 실제 자료 확인이 남아 있습니다.

검사: `node work/test-daily-document.cjs`, `node work/test-reader-v44.cjs`, 번들 Python으로 `work/test-daily-schema.py` 실행. JSON Schema 검사는 work/schema-deps의 jsonschema 4.26.0 사용. 재생성: 확보한 공식 HTML에서 `work/build-daily-data.py` → `work/connect-daily.py` 순서. 데이터 구조는 schemas/mass-document.schema.json, 출처와 재배포 조건 확인 상태는 data/sources.json. 상세 검수 한계는 docs/04-verification.md.

## v46 읽기 위치 저장
review/02-ia-v46.html: 날짜별 순서/모드/회차/내부 스크롤 위치를 로컬 저장·복원합니다. 검사: `node work/test-reader-state.cjs`, `node work/test-reader-v46.cjs`. 스크롤은 비율 복원이며 실제 방향 전환 검증은 남아 있습니다. 재생성: `work/connect-reader-state.py`.

## v47 방향 미리보기
review/02-ia-v47.html → 보기 설정 → 가로/세로 선택. 상단 방향 전환으로 반복 확인, 화면에 맞춤으로 종료. 세로는 브라우저 스크롤로 하단에 접근합니다. 검사 `node work/test-reader-v47.cjs`, 재생성 `work/connect-viewer-orientation.py`. 실제 기기 회전 시뮬레이터가 아닌 뷰어 영역 크기 검증입니다.

## v48 세로 연속 보기
review/02-ia-v48.html → 보기 설정 → 세로: 현재 예식 전체가 한 열로 이어집니다. 가로는 두 페이지 유지. 검사 `node work/test-reader-v48.cjs`, 재생성 `work/connect-portrait-flow.py`.

## v50 독서·복음·메뉴 수정
최신 review/02-ia-v50.html. 독서 본문 높이 확대, 복음 역할 분리, 낭송 이중 테두리 제거, 악보 SVG 모달, 신경 밑줄 및 세로 메뉴/목차 수정. 검사 `node work/test-reader-v50.cjs`, 재생성 `work/apply-comments-v50.py`.

## 실제 브라우저 검사
`node tests/browser-review.cjs`: Playwright와 로컬 Chrome을 사용하는 선택 검사. `MISSA_PLAYWRIGHT_MODULE` 및 `MISSA_CHROME`으로 설치 경로 지정 가능. axe-core는 `npm install --prefix work/browser-qa --no-save --package-lock=false axe-core`로 QA 폴더에 설치. 실제 브라우저 실행 권한 필요. 결과는 work/browser-qa/verified.json 및 두 PNG. 2026-10-19: 8화면 접근성 자동 위반 0, 실제 태블릿/스크린리더는 별도 미검증.

## v54 출처 연결
현행 화면은 21종 주요기도문 원문 링크·대구대교구 주보 링크·사용자 제공 수정보완판 성가표 추천 번호를 표시합니다. 통합 검사는 7개 명령이며 출처 카탈로그 테스트 포함. 권리 확인 전 새 기도문 전문 수입·추가 자동 수집은 보류. docs/content-source-policy.md 및 docs/ordinary-reference-review.md 참조.


v55: 날짜별 자료 준비 상태 표시. node tools/check-review.cjs 통합 검사 8개. node tests/browser-readiness.cjs로 실제 Chrome 날짜 격리 확인.


v56: 날짜·회차별 복수 성가 편성 저장 및 추천 검토/적용/취소. 통합 검사 node tools/check-review.cjs (9개), Chrome 검증 node tests/browser-hymns.cjs.


v57: 성가 패널에서 전체 편성 JSON 백업 → 파일 선택 → 전후 비교 → 복원. 복원 전 현재 편성을 백업하세요. 백업은 신규 번호 편성만 포함하며 구버전 가사·메모는 원래 저장소에 남습니다. 구버전 번호 가져오기는 현재 날짜/회차 내 본당만 지원. 악보 로딩/실패/재시도 제공.
검사: node tools/check-review.cjs (10명령), node tests/browser-backup.cjs, node tests/browser-hymns.cjs. 실제 태블릿 검수는 남음.

v72: 태블릿 가로 기본·스크롤·안내모달·짧은선택버튼·성가캡션 포함 IA 최종검토 후보. docs/02-ia-final-review.md 참조. 추가검사: node tests/browser-creed-native.cjs, node tests/browser-guidance.cjs. 실제기기검증과 IA최종승인은 남아 있습니다.

v73: 보기 설정 → 배경·글자색에서 A/B/C 세테마 선택. 선택은 새로고침후유지(저장소허용시), 날짜·회차편성과별도. node tests/browser-themes.cjs 검사.

v78: 본문명조18px기준/1.6/기본여백. 보기설정→본문글꼴에서명조/고딕전환·저장. 제목/UI고딕유지. styles/tokens.css 타이포토큰은빌드시HTML에임베드. node tests/browser-body-font.cjs 검사.

## 디자인 검토 최신 상태 (2026-10-22)
- 앱 v80: 승인된 기초 값의 토큰 정리. docs/04-system-audit.md 참고.
- 5단계 배치 시안: review/05-wireframe-v1.html. 현재 앱의 배치 변경은 시안 승인 후 진행.

## 6단계 통합 확인
- review/06-integrated-v1.html / docs/06-component-audit.md
- 검사: node tests/browser-components-integrated.cjs (기존 Playwright·Chrome·axe 런타임 필요)
- 사용자 최종 승인 대기. 실제 앱의 전체 Hi-fi 적용은 7단계.

## 6단계 최종 확정 (2026-10-22)
- review/06-integrated-v3.html · 6단계 전체 승인 완료.
- styles/components/: button / field / response / overlay 공용 CSS.
- 최종 검수: PowerShell 환경변수 MISSA_COMPONENT_REVIEW=review/06-integrated-v3.html 지정 후 node tests/browser-components-integrated.cjs.
- 다음 7단계에서 실제 미사 흐름과 배치에 디자인 결합.

## 7단계 프로토타입
- prototype/index.html / review/07-prototype-v1.html
- 빌드: node tools/build-prototype.cjs
- QA: node tests/browser-prototype.cjs, node tests/browser-prototype-hymns.cjs, node tests/browser-prototype-pagination.cjs
- 기존 앱과 별도 테스트 저장. 상세 docs/07-prototype.md.


## 2026-10-23 사용자 자료실·교회음악 조사
- 요청: 고유기도문·성가표·ENC 정리 및 미사 순서/의미 중심 강의 조사자료 준비.
- 원본 7개를 유지하고 data/source-library에 SHA256 검증 사본 배치. ENC ZIP 525개 한글 파일명 복원. HWP 본문은 미판독, ENC 미변환.
- 수원교구 홍보국 게시글 112757(2026-08-26), 10월 고유기도문 제목·첨부명 확인. 원격 첨부 바이트 비교 및 11·12월 개별 게시글 대조는 미실행.
- docs/research/church-music: 전체83목록·관련16선별노트·미사흐름·60분강의초안·앱연결계획. 개인 해설/공식 지침/미판독 첨부 구분.
- 열람: review/07-research-library-v1.html. 앱 전문 자동 수입과 사용자 편성 변경은 하지 않음.
- 다음: review/07-state-review-v1.html에서 7단계 선택·설정·편성·안내 통합 검수. 이후 HWP 하루분 판독·연결 샘플 검토. 8단계 승인으로 취급하지 않음.


## 2026-10-23 공식 전례 지침 조사
- docs/research/official-liturgy/: 공식 출처9건, 판본·확인범위, 주제별 항번호, 앱·강의 연결안, 추가 확인 사항.
- 한국 성음악 지침 공식 전자책 판권·목차 및 인쇄26·27·28·31·35·38·41쪽 직접 선별 판독. 전쪽 판독 아님.
- 총지침 영문의 미국 적응과 한국 적용을 구분. 국내 총지침 도서 소개를 전문으로 오인하지 않음. 전례력은 공식 해설 확인으로 범위 명시.
- review/07-official-liturgy-v1.html에서 열람. 앱 데이터·디자인 변경 없음.
- 다음: 7단계 통합 검수 후 공식 근거와 현재 앱 표시를 연결하는 콘텐츠 대조표 준비.


## 2026-10-24 사용자 DOCX 비교·문의 시점 변경
- 제공 문서2개 비교: 악보뿐 아니라 해설·사도 신경·감사기도양식 범위 차이. 상세 docs/research/ordinary-comparison/README.md 및 review/07-ordinary-comparison-v1.html.
- 사용자 결정: 현재 개인 비영리 테스트. 문의 초안 유지, 출시 준비 때까지 발송 보류. docs/release-readiness.md에 재개 시 리마인드 절차와 미완료 체크리스트 기록.
- 허가 미확인 상태와 사용자 개발 목적을 구분. 자동 크롤링·외부 발송 추가 없음. 사용자 제공 문서 비교·정리와 개발 계속.
- 다음: 7단계 통상문 공통본문·양식·안내 역할 대조. 완전한 모든 감사기도를 확보했다고 처리하지 않음.

### 경본 원문 지시문 연결 (2026-10-24)
- 출처/양식: data/reference-sources/missal-ordinary.json
- 반영 화면: prototype/index.html, review/07-system-sample-v1.html
- 확인 화면: review/07-ordinary-rubrics-v1.html
- 검사: node tools/check-missal-rubrics.cjs (Playwright 및 Chrome 로컬 런타임 필요)
- 구조와 검수 범위: docs/07-ordinary-rubrics.md

- 지시문 스타일 실측: `node tools/check-guidance-normalization.cjs` · 기록 docs/07-guidance-normalization.md

### 표시 통상문 경본 교감
- 결과: review/07-ordinary-collation-v1.html
- 범위: docs/07-ordinary-collation.md / docs/research/ordinary-comparison/app-collation.json
- 원본 자료·기존 본당 설정은 유지하며 텍스트 표기를 교정했습니다.

- 교감 데이터/렌더러 검사: node tools/check-ordinary-collation.cjs (해시34개·교정문구22검사).


### 날짜 고유문·통상문 결합 검수
- 검사: node tools/check-daily-boundaries.cjs
- 결과: docs/07-daily-ordinary-boundaries.md / review/07-daily-boundaries-v1.html
- 실제 자료는2026-10-18 저장본. 검수용 새 날짜 fixture는 브라우저 내부에서만 생성합니다.

### 경본 악보 별도 보관
- 보관함: data/source-library/ordinary/missal-scores/
- 열람: review/07-missal-score-library-v1.html
- 현재 본당 악보 연결은 유지. 경본 악보는 참고용으로만 보관합니다.

### 본당 악보 가사 대조
- 실행: python tools/audit-score-lyrics.py
- 결과: review/07-parish-score-lyrics-v1.html / docs/07-parish-score-lyrics.md
- 악보·앱 연결은 변경하지 않는 참고용 대조입니다.

### 7단계 최종 흐름 검수
- 검수 화면: review/07-final-review-v1.html
- 자동 조작: node tools/check-final-flow.cjs (Chrome/Playwright 번들 런타임)
- 결과·범위: docs/07-final-flow-qa.md / work/browser-qa/final-flow.json
- 테스트는 독립 브라우저 저장소를 쓰며 실제 사용자 편성을 수정하지 않습니다.

## 8단계 날짜별 자료 추출
- 실행: `python tools/extract-monthly-hwp.py` (olefile 0.47을 scratch/hwp-deps에서 사용).
- 결과: data/source-library/extracted-hwp/coverage.json. 추출 후보이며 앱 확정 데이터와 구분한다.
- 진행 및 예외: docs/08-date-coverage.md / docs/08-qa.md.

### 10월 고유문 연결 및 검사
- 연결: `python tools/link_monthly_propers.py` (기존 날짜 보존, 10월만 대상).
- 경계 단위 검사: `python tests/test_monthly_propers.py`.
- 31일 앱 검사: `node tools/check-october-batch.cjs`.
- 원본 위치·분리 지시: data/source-library/extracted-hwp/link-audit-202610.json.
- 고유문 연결과 독서·복음 포함 전체 미사 완성을 구분한다.

### 굿뉴스 말씀 전례 (2026년10~12월)
- 수집: `python tools/collect_goodnews_daily.py` (92일, 캐시 재사용).
- 연결: `python tools/link_goodnews_daily.py` → `node tools/build-prototype.cjs`.
- 검사: `python tests/test_goodnews_daily.py` / `node tools/check-goodnews-daily.cjs`.
- 원본·추적: data/source-library/goodnews-daily/.
- 현재 날짜별 기본 미사 기준이며11~12월 고유기도문은 별도 연결 작업 중.

### 11~12월 고유문 연결
- 실행:`python tools/link_remaining_propers.py` → `node tools/build-prototype.cjs`.
- 검사:`python tests/test_remaining_propers.py` / `node tools/check-remaining-propers.cjs`.
- 기존 굿뉴스 기본 말씀과 일치하는 HWP 양식만 연결. 다른 양식은 data/reference-sources/proper-mass-forms-20261112.json에 참고 보존.
- 현재92일 말씀+고유기도3종 연결,시기별 전체 순서 검증은 진행 중.

### 상단 전례력 정보
- data/reference-sources/liturgical-calendar-2026q4.json:공식2026경계일 기반10~12월 시기·주차 계산표.전체 축일 판정 엔진 아님.
- 미사 양식명은 접힌 자료 상태에 표시하며 상단 주차와 분리한다.
- 검사:`node tools/check-calendar-heading.cjs`.

### 보편 지향 기도
- 현재 굿뉴스 저장본의 실제4일16지향 연결.원문 안내만 있는 경우와 항목 없는 경우 구분.
- 실행:`python tools/link_goodnews_intercessions.py` → `node tools/build-prototype.cjs`.
- 검사:`node tools/check-intercessions.cjs`.주교회의 원문의 추가 수록 현황은 docs/08-qa.md 참조.

### 주교회의 보편 지향 기도 보완
- `python tools/link_cbck_intercessions.py`:확인된11월6일24지향만 연결,캐시 재사용.
- `node tools/check-cbck-intercessions.cjs`:출처·다른본문보존·실제표시 검사.
- 현재 앱:10일40지향.실제현황:data/reference-sources/intercession-coverage-2026q4.json.


### 날짜별 대영광송·신경·감사송
- 원문지시:data/reference-sources/daily-rubrics-2026q4.json(92일,기본선택미사).
- 검사:`node tools/check-daily-rubrics.cjs` →558건.날짜별목차/본문표시·감사송연결·미연결구분.
- 감사송전문6일.명시지시만있는날은미연결표시,지시없는날은기존감사기도제2양식고유감사송유지.


### 홈 화면 앱 새로고침
보기 설정 → 앱 새로고침.저장한 날짜·성가 편성을 유지하며 페이지를 다시 불러옵니다.
검사:`node tools/check-pwa-reload.cjs`.캐시 강제삭제나오프라인업데이트기능은아닙니다.


화면크기안정화검사:`node tools/check-resize-stability.cjs`(Chrome/WebKit필요).반복resize알림과실제크기변경을구분합니다.


날짜동작:기본진입·새로고침은오늘(기기시간대),날짜필터변경은시작예식첫페이지.검수용`?date=YYYY-MM-DD`는지정날짜우선.검사:`node tools/check-date-navigation.cjs`.


스크롤가용폭검사:`node tools/check-scroll-width.cjs`(Chrome/WebKit).일반·겹침형스크롤바의제목/본문폭대조.


기본방향은기기자동전환입니다.수동가로/세로선택후자동으로돌리려면보기설정의현재화면에맞춤을선택하세요.세로도화면전체높이를사용합니다.검사:`node tools/check-device-orientation.cjs`.


세로모드는전체미사를연속스크롤하며하단페이지넘김은숨깁니다.가로는두페이지넘김유지.검사:`node tools/check-portrait-continuous.cjs`.


### 본당 미사 일정
`config/parish.json`에서본당명·요일·시간·회차를수정한뒤빌드·배포합니다.사용법은config/README.md참조.검사:`node tools/check-parish-config.cjs`.기존회차ID는성가저장호환을위해유지합니다.


본당명은보기설정에서직접입력·저장하며새로고침후유지됩니다.기본값은config/parish.json의name입니다.검사:`node tools/check-parish-name.cjs`.


오늘미사초기선택은현재시각과가장가까운회차이며필터는미사명만표시합니다.수동선택유지.검사:`node tools/check-auto-session.cjs`.


재조판악보는상하16px여백과테마기본글자색을사용합니다.검사:`node tools/check-score-ink.cjs`.


MVP리더는자료상태·개발정보패널을표시하지않습니다.자료확인과개발검증은프로젝트문서·검사도구에서진행합니다.


MVP성가패널은백업·복원/참고표상세를표시하지않고,저장편성또는성가표추천번호를입력란에채웁니다.성가표출처유지.검사:`node tools/check-mvp-hymn-panel.cjs`, `node tools/check-panel-width.cjs`.
