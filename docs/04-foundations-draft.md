# 4단계 기본값 비교 v1

상태: 사용자 선택 전. 현행 앱 v77 유지.
- 인터뷰: 18/20/22px, 제목·본문 모두 명조 비교, 기본/여유 여백.
- 동일폭3카드에서 글꼴/크기/1.6·1.8·2.0줄간격/여백 선택. 미색·종이색·와인다크 전환.
- 독서/기도문은 기존 로컬 자료 일부 재사용, 새 공식문 수집 없음. 악보는 기존SVG 원본이며 음표·가사 자체 크기는 별도조판값 유지.
- 모든 값은 draft변수, tokens.css 발행/디자인시스템 확정은 선택 후. CSS고정폰트px없음, rem사용.

## 2026-10-22 실제 가로 리더 글꼴 비교 v2
- 사용자 정정: 카드나란히가아닌가로보기모드에서크기판단필요. review/04-foundations-v2.html 부모컨트롤+04-foundations-reader-v2.html 실제앱v77스냅샷리더로교체. v1보존.
- iframe1024x768 고정/축소없음. 좁은창은외부가로스크롤. A고딕18/B명조20/C명조22, 크기/줄간격/여백/3배경, 독서·기도·악보선택. 현재anchor재조판으로위치유지.
- 부모/자식postMessage는source확인+허용값목록검증. 자식저장소는메모리Map으로격리,원래앱localStorage무변경. 미리보기선택은확정아님.
- 실제Chrome innerWidth1024/innerHeight768, 2쪽/18·20·22computedfont/anchor유지/화면3종/800폭외부스크롤·축소없음/pageerror0 PASS. foundations-landscape-v2.png 직접확인.
- 현행앱v77변경없음. 비교후기본값선택대기.

## 2026-10-22 본문 기본값 확정·글꼴 설정 v78
- 사용자 “18 1.6 기본. 명조/고딕 전환, 제목은 두고 본문만명조” 승인.
- 본문기본1.125rem(기본16px에서18px)/lineheight1.6/기존기본여백유지. 제목·UI는고딕, 본문만명조기본. 보기설정명조/고딕 전환 및 missa.reader.body-font.v1 전역저장. 테마/날짜/성가와분리,손상값명조fallback/저장실패안내.
- styles/tokens.css에 기초→의미→컴포넌트 타이포토큰 발행, design.md동시기록. 생성기가임베드하므로단일HTML유지. 색상·나머지간격·형태토큰은draft검토잔여.
- 통합10검사 PASS. Chrome실측18px/28.8pxlineheight/본문Batang·제목Malgun유지/고딕전환/anchor/새로고침설정복원 PASS. 가로세로8화면axe0/overflow없음/pageerror0,3테마Draweraxe0/복원 PASS.
- 악보내음표·가사는원본SVG조판유지. 실제태블릿수동검수별도.

## 2026-10-22 간격·모서리 비교 시안
- review/04-spacing-v1.html 및04-spacing-reader-v1.html 실제v78기반1024x768격리미리보기. A촘촘/각짐,B기본/6px,C여유/12px;간격·모서리독립조합가능.
- 색상/본문명조18px/1.6/제목고딕유지,원앱무변경. Chrome3안색/글꼴/크기/leading동일,버튼44px이상/가로1024x768고정/혼합조합/pageerror0 PASS.
- 사용자선택전draft. spacing-a/b/c-v1.png 캡처.

## 2026-10-22 기본 간격·더 둥근 모서리 승인 v79
- 사용자 “기본 - 더 둥글게” 명시선택. 기본외부여백1rem/간격.75rem/본문카드.625rem유지,컨트롤패딩.5rem .625rem,모서리.75rem(기본12px),버튼최소44px.
- styles/tokens.css 기초→의미→reader컴포넌트토큰, design.md동시반영. 선택한간격의draft별칭제거. 제목/본문폰트·18px/1.6·색상유지.
- 초기검사세로상단넘침발견,상단전용inline패딩.25rem토큰으로보정. 재실행통합10검사/가로세로8화면axe0·상단및본문넘침0/pageerror0/위치복원/모달초점 PASS. 본문글꼴전환/저장복원PASS.
- landscape-verified.png 직접확인. 실기태블릿별도. 나머지색·반응형·상태토큰정리와디자인시스템전체검수는후속.
