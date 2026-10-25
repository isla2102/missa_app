# 읽기 시스템 추천안 · 2026-10-23 · 검수 대기

샘플: review/07-reading-system-v1.html. 실제 앱/확정 tokens.css는 변경하지 않음. 새 값은 샘플 상단 draft 변수로 분리.

| 항목 | 샘플 값 | 기존 시스템 | 판정 |
|---|---|---|---|
| 바깥/페이지/목차 | 16px / 균등 2쪽 / 176px | 16px / 균등 2쪽 / 192px | 목차 축소 제안 |
| 페이지 안쪽/거터 | 24px / 16px | 16px / 12px | 반복 여백 토큰 추가 제안 |
| 제목 | 24px 전례, 20px 섹션, 1.3 | 명시 역할 구분 부족 | 타이포 역할 추가 제안 |
| 본문 | 18px 명조, 1.6 | 18px 명조, 1.6 | 유지 |
| UI/보조 | 16px / 14px | UI16px, 안내16px | 안내 축소 제안 |
| 간격 | 4/8/12/16/24/32px | 4/6/8/10/12/16px 혼용 | 4px 리듬 제안 |
| 서피스 | 앱 바탕 / 종이 / 본문색6% 혼합 패널 | 바탕/종이, 패널 동일 | 패널 역할 분리 제안 |
| 내부 카드/악보 | border0 | A+C 승인 | 유지 |
| 안내 | 일반 투명, 합송 안 종이바탕 | 안내 보조 채움 | 변경 제안, 대비 예외 명시 |

기존 원칙: 차분한 독서, 와인색 역할 강조, 장식선 없음. 4px 단위와 기존 18px 본문을 기준으로 시작. 페이지 안쪽 24px는 책의 호흡과 조작부 분리를 위해 기존16px에서 확대. 목차는 본문 확보를 위해176px로 축소.

검수 화면: 독서·신앙고백·참회·성가편성·보기설정 × 미색/종이/다크. 실제 태블릿과 스크린리더 검수는 별도. 스타일 표준 CLI 미실행. 다음: 사용자 시각검수 → 조정 → 승인 후 foundation/semantic/component 3계층 토큰 및 design.md에 확정하고 원본 CSS 정규화.


## 안내·스크롤바 시각검수 수정
- 안내문 접두어 ‘안내 ·’ 제거. 안내 버튼·패널 이름 및 본문 내용에 쓰인 일반명사 안내는 유지. 원문 데이터 무변경, 렌더링 접두어만 제거.
- 샘플 합송 안 안내: 별도 종이 바탕 제거, 투명 배경·14px 고딕·400·여백8px. 합송 글자색을 사용해 대비 유지.
- 스크롤바 제안: thin, thumb=보조글자색72%+종이28%, track=종이(비교 바깥은 앱바탕). 세 테마 자동 연동. 운영체제 자동 숨김/형태는 브라우저 설정에 따름.
- 검사: 15개 화면/테마 axe0, 3테마 안내 접두어0·배경투명·14px/400·scrollbar-color 실측 PASS.
- 다음: 수정 샘플 시각검수 후 서피스·스크롤바 토큰 확정.


## 안내 색·악보 도구·버튼 역할·스크롤 구조 수정안
- 안내: 미색/종이 황토 #75501C, 다크 #E3C18C. 합송 안은 밝은골드 #F5DCA7 / 다크합송 안 #553119. 모두 draft, 본문18px과 별개14px고딕.
- 이동16px/40px, 선택14px/32px, 저장16px/44px, 악보도구14px/32px. 크게보기는 이미지위 출처행 우측으로 이동, 절대좌표 겹침 제거.
- 악보 실측: 카드 padding12px 0, figure margin8px 0 0. 페이지16px와 이미지 원본여백 별도.
- 가로보기 페이지: 제목을 고정영역으로 분리, 아래 본문만 overflow auto. 스크롤영역 radius12px, 바깥페이지 overflow hidden. 제목아래부터 스크롤바 시작.
- 검사: 15화면/테마 axe0, 페이지392px/목차접음488px, 제목20px/본문18px/페이지패딩16px 확인. 제목 스크롤전후 top191.59375 동일, 본문시작=제목끝231.59375, 악보버튼14px/32px/position static 실측 PASS.
- 실제 터치·OS별 스크롤바 외형은 별도 검수. 다음: 사용자 시각검수 후 토큰 확정.


## 여백 정규화 및 목차 UX 감사
- 발견: 헤더 space-between에 따른 비대칭, 버튼 개별 좌우4/10/12px 혼용, 시즌버튼2px경계·별도패딩, p 기본1em여백, 선택그룹 하단여백 중복, 목차 전체 와인·밑줄·현재펼침 테두리.
- 샘플 수정: 상단 equal-side grid 중앙정렬. 버튼 좌우12px, 상하8px(이동/저장)·4px(선택/악보). 기본p margin0, 역할별8/12/16/24px. 페이지16px/gap16px 유지.
- 목차: 일반본문색, 현재만 와인·700·10%배경. 밑줄제거. 14px/1.5=21px, 행최소40px/패딩8px/항목gap4px, 그룹사이24px. 일반링크의 의미·키보드focus-visible 유지.
- 검수: browser-spacing-toc 9개 상태에서 중앙오차<1px·헤더넘침0·pagepadding16·gap16·보이는버튼상하/좌우대칭 및 좌우12px·목차최소40px PASS. browser-reading-system 15화면 axe0 PASS. 이미지 work/browser-qa/spacing-toc-review.png, 실측json spacing-toc-audit.json.
- 변경은 검토 샘플에만 적용. 다음: 사용자 시각검수 후 SSOT 확정.


## 2026-10-23 목차 밀도·펼침 묶음·상단 필드 축소
- 사용자 요청: 목차 간격 축소, 현재 화면 항목 묶음, 날짜/달력과 모드/화살표 간격 축소.
- 샘플: 목차 최소32px, 세로패딩4px, 행gap0, 그룹간격16px. 두줄항목50px 자동확장. 현재 펼침 li 배경을 연속 연결, 첫/끝 모서리만12px. 현재위치만 와인/700, 나머지본문색.
- 날짜: 8rem(128px), 좌우8px, native 날짜편집/달력 표시 유지. 모드/회차: native select 키보드 동작 유지, appearance none 및12px 화살표, 텍스트와화살표간8px·우측8px. field-sizing content, 모드실측102px.
- 검증: browser-compact-toc-fields 3테마 PASS. 날짜128/모드102/목차32px gap0/제1독서·화답송·제2독서 단일묶음/헤더넘침0/모드선택동작 확인. browser-reading-system 15상태 axe0 PASS.
- 검수이미지 work/browser-qa/compact-toc-fields.png, 수치 compact-toc-fields.json. 기존확정 앱/토큰 미변경. 다음: 사용자 수정샘플 시각검수 후 시스템 확정.


## 목차 축소 열·SVG 도구·곡선 스크롤 검토안
- 사용자 요청 반영: 목차 제목 삭제, 접기/펼치기 SVG, 설정 톱니 SVG. title/aria-label 및 aria-expanded 유지.
- 펼침176px, 축소84px의 목차 열을 항상 유지. 축소 때 세부목록 대신 시작예식·말씀전례·성찬전례·마침예식 링크4개와 현재 전례 강조. 단어중간 줄바꿈 방지. 현재읽기위치에서 scheduleReflow.
- 스크롤: Chromium scrollbar thumb16px곡률, track투명·상하8px,8px폭, 기본화살표숨김. 목차영역 radius12px, border0. 브라우저별 네이티브 외형은 차이 가능.
- 검증: 3테마 축소상태 axe0, SVG/라벨/설정창/4전례이동 PASS. 토글 전후x/y동일, 축소폭84px, thumb radius16px 실측 PASS.
- 샘플/확정 구분: review/07-reading-system-v1.html 및 07-system-sample-v1.html만 변경. 토큰승격 전 시각검수대기. 다음: 사용자 축소/펼침과 스크롤 마감 검수 후 시스템 확정.


## 검수용 프레임 표시 / 실제 화면 전환
- 사용자 요청: 모든 프레임 경계를 표시하고 실제모드로 전환,1024×768외곽프레임 표시.
- 샘플 상단 표시모드 추가, 기본검수보더. 배치보라점선/프레임파랑실선/텍스트주황점선/컨트롤초록실선 및범례. outline으로 레이아웃치수 무변경.
- 외곽 프레임은 iframe의 콘텐츠1024×768 바깥에 outline2px. 실제모드에서는 검수용 outline 제거, 접근성 focus-ring 유지. 모드변경시 재렌더하지 않아 읽기 위치 유지.
- browser-frame-inspection PASS: iframe1024×768, 모드양방향 전환, 페이지크기 전후동일, 실제모드 outline none, pageerror0.
- 다음: 검수용 보더를 켜서 여백 확인 후 실제 화면과 번갈아 시각검수. 확정앱/SSOT는 미변경.


## 코디·웹디 8항목 재검수
- 사용자 8항목 요청을 sample에 반영. 상세 원인/시안값/기존값/판정 docs/07-eight-point-review.md.
- 제목행·입력32, 악보상하대칭·크게보기z3오버레이, 기호/안내열통일, 신경안내는제목우측 도움창.
- 악보 버튼이 음표를 가리지 않도록 figure 내부 상하32px 대칭 도구공간 추가. 카드상하12px·figuremargin0. 원본이미지여백무변경.
- 3테마 실측·프레임전환·축소목차 회귀 PASS. 시각검수 대기, 시스템 미확정. 다음: 최신검수파일 사용자 확인 후 SSOT승격.


## 종이색 대비·상하0·페이지 외부 스크롤 검토안
- 사용자 5항목 반영. 종이색 b 본문 #29352D→#171C18, 보조 #4F5C4E→#333D32. 배경#E9DFCD·밝은글자·다크글자 무변경. 상대휘도 대비 본문9.6876→13.0798, 보조5.3480→8.5753. 기존도AA통과하지만 녹회색의 약한 인상 개선.
- 스피치/content margin/padding block0. liturgy/dialogue/section gap0. figure margin/padding0. heading행 최소32 및본문18/1.6은 글자줄간격이라 유지. 일반/중간안내 margin4 padding0. 기존32px 악보 도구빈공간 제거.
- page overflow visible, 본문스크롤 width+24/end margin-24/end padding16. 실측 외곽7px, elementFromPoint가스크롤영역반환하여 잘리지않음 확인. 목차미변경.
- browser-zero-spacing-paper PASS: 성호경/참회/독서/신경 카드간격0·외부스크롤실측. 15화면axe0 PASS. 원본이미지의 흰여백은무변경.
- 증거 work/browser-qa/zero-spacing-paper.json/png. 제안샘플만수정. 다음: 사용자 종이색·제로간격·외부스크롤 시각검수 후 시스템확정.


## 스페이싱 재복구 · 이전 제로간격안 폐기
- 사용자 지적 수용: 내부패딩/카드간격/제목간격을 일괄0으로한 이전안 폐기. 위상별 구분을복원.
- 최종검토 규칙: 제목행32px, 제목-카드8px, 스피치 카드 내부block8px/inline12px, 카드사이8px, 첫카드외부margin0, 섹션사이16px. 래퍼content-padding0, 악보추가상하여백0 유지.
- 실제 원인: 중간 섹션의 sticky-heading에 남은 음수margin·전체16pxpadding이 화답송등 여백불일치유발. 첫제목을제외한중간제목은static/marginbottom8/padding0로일원화. 다른양식card padding-bottom0 예외제거.
- 스크롤: width확장24→8px/endpadding8px, page overflowhidden. 전체스크롤영역이카드우측8px이상안쪽에들어감실측.
- 안내버튼: 공용component토큰으로 채움accent/inkpaper/border0 적용. Unicode문자대신 정보 SVG. 키보드/aria-label 유지.
- browser-spacing-recovery PASS: 성호경/참회/독서/신경의 제목8·간격8·패딩8·첫margin0·내부스크롤·SVGborder0. 증거 spacing-recovery.json/png.
- 확정전 샘플만수정. 다음: 사용자 회복안 시각검수 후 규칙확정.


## 중첩 카드 경계 간격 재검수
- 사용자 지적: 카드간격 불일치. 직접형제 측정만으로는 놓치는 래퍼간 경계를 추가 감사.
- Red: 같은섹션 안 leaf카드간격8/0px 혼재. 본기도 기도합시다-본문-아멘 사이 외부래퍼 경계0px 발견.
- 원인: layout레이어의 공통flow배치를 components레이어의 개별display:block이 덮어씀. 공통flow규칙을소유components레이어로이동, 각섹션에명시적flow변형적용. 제목margin과부모gap중복도제거.
- Green: 전체전례항목28개 순회, 반복펼침을포함한 같은섹션 카드경계77건 모두8px. 제목간격8/내부padding8/섹션간격16 구분유지.
- browser-reading-system 15화면axe0 PASS. 증거 work/browser-qa/card-gap-audit.json. 다음: 검수샘플에서 본기도·독서·통상문 카드경계 사용자확인 후 시스템확정.


## 래퍼·형제·보이는 카드 전계층 검수
- 기존77경계 검사는 가로 기본상태만이라 전체정규화 판정으로부족. 이번672조합(2날짜×2방향×2사용자×3테마×28항목) 수행.
- Red 세로전용block규칙으로1956개 반복위반 발견. 원예외규칙제거.
- Green 래퍼9744/직접형제3984/래퍼경계넘는보이는카드3984회 측정, 위반0. 반복표시포함.
- 구조를본문/악보등모두동일태그로바꾸는것이아닌 역할별간격소유권일치. 상세범위·예외 docs/07-structure-gap-audit.md.
- 다음: 사용자 수정샘플확인, 선택양식회귀 후시스템승격. 모든사용자입력/실제태블릿검증완료로확대해석하지않음.


## 〈또는〉 보조 위계 및 논리 형제 간격
- 〈또는〉은 본문에서분리된 보조표시: 안내와동일14px고딕/400/안내색.
- 인사·보편지향기도·사제마침기도는 같은목차항목을여러flow블록으로나눠이전검사의same-data-flow-key범위밖이었음. Red 인사대안16px,지향-응답16px,마침기도-아멘16px.
- 완전한flow목록에서tocId동일+다음hideHeading이면joinNext 명시. reader__item--joined 변형margin8. 새로운제목이시작되는경계는16 유지. data-section-id도명시해논리소속기록.
- Green 인사대안간8px, 지향/응답간8px, 사제마침기도/아멘8px 실측. tests/browser-logical-sibling-gap.cjs --assert.
- 이전672검사는같은flow키안의경계에한정이었음. 논리같은섹션/다른flow키 경계를이번추가. 범위구분보완. 다음: 수정샘플 인사·보편지향·사제마침기도 시각검수.


## 복음 환호송 및 제목 기준 카드 너비 통일
- 사용자 정정: 스크롤바공간을역마진으로이미빼낸의도 유지. 본문폭을다시줄이는설명/해결폐기.
- 실제너비차이: 스크롤영역확장8px에서 우측padding8+scrollbar8이 이중차감. 확장16px/endmargin-16px/padding8px로 제목과 내용카드 좌우경계 일치. 스크롤바는 페이지경계안쪽1px,페이지밖넘침없음.
- 복음환호송 choir/last는 제목없는논리계속블록으로joinNext 포함. 앞합송/성가대/뒤합송8px. 낭송/성가 모두측정.
- Red 목차축소인사dialogue auto-fit이2열198px씩으로분리(제목404px). 자동2열을제거해스피치카드전체폭일치.
- Green 전체28항목×목차두상태 너비불일치0. 복음환호송 낭송/성가×목차두상태×3테마12상태 제목/카드양끝일치·간격8·역마진유지·페이지내스크롤 PASS.
- 제목/카드 폭: 펼침358px,축소404px(페이지392/438,양쪽padding16+border각1 제외). 마커/본문의내부2열은유지.
- 증거 tests/browser-title-card-width.cjs, work/browser-qa/title-card-width.json. 다음: 사용자보더모드에서좌우경계확인후시스템승격.
