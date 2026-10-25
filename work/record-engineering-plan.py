from pathlib import Path
import shutil

def save(name,text):
 p=Path(name)
 if p.exists():shutil.copy2(p,Path('scratch')/(p.name+'.before-engineering-plan'))
 p.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
ia='''# MISSA 정보 구조 — v43 결정 정리

정리일: 2026-10-19. 근거: v5 구조 승인, 이후 사용자 수정 요청, v43 및 “결정 정리하고 코디 계획대로 작업 진행” 지시. 화면 동작 결정 정리이며 디자인 3~8단계 완료를 뜻하지 않는다. 이전 v5 문서는 scratch 백업 보존.

## 화면 및 이동
- 상단 날짜·회차·모드, 성가·주요 기도문. 현재 예식 제목 중앙, 이전/다음 예식 좌우.
- 가로 두 페이지는 같은 예식의 연속 내용. 목차는 오른쪽 상시 레일, 보기 설정·안내는 레일 아래.
- 페이지 버튼은 목적 순서명을 표시. 예식 경계를 넘어 이동하며 이전 예식에는 마지막 펼침으로 복귀. 전체 시작/끝만 비활성화.
- 다음 순서 안내만 있는 빈 펼침은 생략. 경계 버튼에 유한 강조, 모션 감소 설정 대응. 좌우 드래그 지원, 세로 스크롤 및 입력 조작 구분.

## 본문 배치
- 섹션은 새 페이지 시작, 가능한 한 한 페이지, 두 페이지면 같은 펼침에 정렬.
- 성호경+인사는 한 페이지로 결합.
- 제1독서+마침 응답+화답송은 왼쪽 한 페이지. 제2독서+마침 응답은 오른쪽 한 페이지. 본문 카드만 남은 높이를 채움. 복음 환호송은 다음 펼침.
- 독서·복음의 사제/독서자 및 합송은 세로 배치. 인사 마지막 선택지와 감사기도 짧은 대화는 2열 유지.
- 복음, 보편 지향 기도 전체, 예물 준비+예물 기도는 각각 단일 페이지 내부 세로 스크롤. 보편 지향 기도의 사제 마침 기도+아멘은 독립 페이지.
- 감사기도 제2양식은 본문 구간별 단일 스크롤 페이지. 중간 환호 악보는 별도 유지.

## 악보
- PDF 실제 A4 세로 210×297mm. 화면은 연속 SVG, 높으면 카드 내부 스크롤. v43 자산 registry.json 기준.
- 가사 크기 통일 기준 12.5pt, 촘촘한 가사는 가로 폭 보정. 시스템 간격 6mm.
- 대영광송 기본 4~5마디, 끝부분은 사용자 지정 의미 구절 5줄. 거룩하시도다는 의미 구절 6줄. 신앙의 신비여는 한 줄 2마디, 마지막 홀수 마디 예외.
- 음표 XML 동일 검사는 원본 판독의 음악적 정확성 보증과 구분. 본당 최종 교정은 남아 있음.

## 공통 데이터와 미완료
- 세 회차는 같은 전례일·본문·순서 공유, 네 성가 배정만 다름. 모드는 보조 안내 표시만 변경. 회차/모드 변경 시 읽기 위치 보존.
- 날짜별 공식 본문 전체 연결, 저장·복원 실기 검증, 태블릿 실제 배치/접근성 검증은 남아 있음.
- 주보 화답송 악보와 미확인 성가 번호/실제 미사 시간은 생성하지 않음. 일반 모드에도 공식 응답 본문 유지.
- 다음 검증 목표: 2026-10-18 하루의 확인된 본문을 연결. 상세 범위는 docs/02-architecture.md 제안 기준.
'''
save('docs/02-ia.md',ia)
save('docs/01-brief.md','''# 실제 본문 하루 연결 — 엔지니어링 브리프

2026-10-19. 사용자 “결정 정리하고 코디 계획대로 작업 진행”으로 작업 목표 승인. 기존 기획을 재사용하며 새 인터뷰로 재확인하지 않는다.

## 목표
2026-10-18 주일 하루를 확인된 데이터로 읽고, 실제 본문 길이에서 v43 조판 규칙을 검증한다. 대상은 개인용 로컬 MVP. 시각 디자인 단계 진행과 구분한다.

## 포함
- 날짜별 제1·2독서, 복음, 화답송 텍스트, 복음 환호송 구절, 본기도·예물 기도·영성체 후 기도 및 보편 지향 기도의 출처별 연결 상태 관리.
- 확인된 본문/미제공/검토 중 구분, 안정적 문단 ID, 실제 JSON Schema와 교차 참조 검증.
- 세 회차 공통 문서·네 성가 분리, 안내 모드와 본문 분리.
- 저장된 하루치 콘텐츠 오프라인 표시 및 읽기 위치 검증. 외부 링크 악보까지 오프라인이라고 주장하지 않음.

## 제외
전 날짜 자동 수집·전체 전례력 엔진·로그인·서버·새 디자인·모바일 앱 스택 전환. 주보 악보 미제공 시 상태 표시.

## 수용 기준
다른 날짜에 10월18일 본문을 재사용하지 않음. 출처 없는 공식 문구를 생성하지 않음. 세 회차의 본문과 순서는 동일. 실제 긴 복음/기도가 스크롤로 끝까지 접근 가능. 잘못된 문서·중복 ID·날짜 불일치를 거부. 기존 v43 회귀 검사 유지.
''')
save('docs/02-architecture.md','''# 하루치 실제 전례문 연결 — 아키텍처 제안

상태: DRAFT, 구현 전 범위·구조 승인 대기. 2026-10-19. 입력: docs/01-brief.md, docs/02-ia.md, v43.

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
''')
p=Path('ENGINEERING.md');s=p.read_text(encoding='utf-8');s+='\n\n## 2026-10-19 cod-e 재개\n- Stage 1: 기존 기획 재사용, 하루 실제 본문 연결 목표 사용자 승인. docs/01-brief.md 기록.\n- Stage 2: docs/02-architecture.md 구체 제안 작성, 구조 승인 대기.\n- Stage 3~5: 이번 데이터 연결 작업 미착수. 이전 UI 회귀/악보 검수와 분리.\n- v43 결정 docs/02-ia.md에 통합. 기존 v5 문서는 scratch에 보존.\n';save(str(p),s)
p=Path('docs/progress.md');s=p.read_text(encoding='utf-8');s+='\n\n## 2026-10-19 결정 정리 및 cod-e 실제 본문 계획\n- 사용자 진행 지시에 따라 v43 결정 docs/02-ia.md 통합, docs/01-brief.md 작성. 엔지니어링 Stage 1 목표 승인 기록.\n- docs/02-architecture.md에 하루치 데이터 모델/파일 범위/검증/실기 QA 제안. Stage 2 구조 승인 대기, 구현 미착수.\n- 웹디자인 2단계 보완 결과 정리. 3~8단계 승인·완료를 추정하지 않음.\n';save(str(p),s)
p=Path('README.md');s=p.read_text(encoding='utf-8');s+='\n\n## 2026-10-19 현재 계획\n최신 검토는 review/02-ia-v43.html, 통합 결정은 docs/02-ia.md. 다음은 2026-10-18 실제 본문 하루 연결이며 docs/01-brief.md와 docs/02-architecture.md에 범위/구조를 기록했습니다. 구조 승인 전으로 데이터 연결 구현은 미착수입니다.\n';save(str(p),s)
print('Saved consolidated decisions, brief, concrete architecture and progress; previous files backed up.')
