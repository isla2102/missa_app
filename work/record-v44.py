from pathlib import Path
import shutil

def write(name,text,append=False):
 p=Path(name)
 if p.exists():shutil.copy2(p,Path('scratch')/(p.name+'.before-v44'))
 if append:text=p.read_text(encoding='utf-8').rstrip()+'\n\n'+text
 p.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
write('docs/03-test-plan.md','''# 하루 실제 본문 연결 테스트
2026-10-19. 아키텍처 사용자 “진행하세요” 승인 후 실행.

## Red
node work/test-daily-document.cjs: 검증 모듈 없음으로 실패 확인. v44 통합 검사에서 복음 환호송을 복음으로 잘못 선택한 추출 오류를 발견해 제목 완전 일치로 수정. 예물기도 mock 예상 검사는 실제 저장본 검사로 갱신.

## Green
- node work/test-daily-document.cjs: 정상 문서, 실제 fixture, 날짜 불일치, 잘못된 날짜, 중복 ID, 미등록 출처, 빈 본문, 임의 override, 앵커 fallback/offset clamp 통과.
- 번들 Python work/test-daily-schema.py: JSON Schema 자체 유효성, 실제 fixture, 잘못된 날짜/본문 override/빈 verified 본문의 3개 거부 사례 통과.
- node --check work/review-ia-v44-check.js: 통과.
- node work/test-reader-v44.cjs: 23개 결과 그룹 통과. 기존 22개 그룹과 실제 본문·날짜 격리·회차/모드 공통 본문 검사. 일부 이전 로그 제목은 과거 버전 이름이며 실제 단언이 기준.
- 증거: work/test-daily-document.log, work/test-reader-v44.log.

## 아직 실행하지 않은 검사
실제 태블릿의 높이 측정·세로 끝 접근·방향/글자 크기 변경·새로고침 위치 복원·접근성 전체 검사. 테스트 커버리지 비율은 측정하지 않았음. 안정 ID와 앵커 함수 검사는 저장/복원 UI 구현 완료를 뜻하지 않음.
''')
write('docs/04-verification.md','''# 실제 본문 연결 검수 — v44
2026-10-19. cod-e Stage 4 검토 자료, 사용자 확인 대기.

## 변경 전후
- 제1·2독서와 복음: Lorem ipsum mock → 2026-10-18 공식 날짜 페이지 저장본.
- 화답송: 악보 미등록 안내만 표시 → 실제 화답송 텍스트와 주보 악보 미등록 안내.
- 예물 기도·영성체 후 기도: mock → 실제 본문+아멘.
- 복음 환호송·기도 지향: HTML에 중복된 날짜별 문자열 → 검증된 공통 문서에서 선택.
- 감사기도 서문: 기존 일반 초안 → 날짜 페이지의 감사송. 나머지 통상문과 악보는 유지.
- 미제공 날짜/사제 마침 기도: 임의 본문 없이 미연결 상태. 공지 사항은 본당 자료가 없어 mock 유지.

## 출처 및 추출 검토
https://missa.cbck.or.kr/DailyMissa/20261018 에서 날짜·독서 인용(이사 2,1-5 / 로마 10,9-18 / 마태 28,16-20), 네 지향, 기도문 확인. 출처·확인일·파일 해시·이용 조건 미확인 상태는 data/sources.json.
검색 결과의 /460404 주소는 열었을 때 다른 날짜를 표시하여 사용하지 않음. 안정적인 날짜 경로만 사용.
저작권 고지 존재. 공개 열람을 배포 허가로 간주하지 않으며 현재 개인 로컬 검토용. 주보 악보와 사제 마침 기도는 제공받지 않아 missing.

## 실행 및 증거
review/02-ia-v44.html은 데이터와 검증기를 내장하므로 file:// 열람에 fetch가 필요 없음. 이 사실은 외부 성가 이미지의 오프라인 보장을 뜻하지 않음.
명령과 통과 결과는 docs/03-test-plan.md 및 work/ 로그 참조.
브라우저 제어 목록은 비어 있어 실제 브라우저/태블릿 검증 미실행. 실제 기기에서 제1독서+화답송 왼쪽과 제2독서 오른쪽, 복음 스크롤, 예물 기도, 다른 날짜의 미연결 표시를 검토할 것.

## 검토 시 한계
하루치 데이터 연결과 모의 DOM 검사 완료. 전 날짜 연동·전체 전례력·읽기 위치 영구 저장·태블릿 시각 QA 완료를 의미하지 않음. 공식 페이지 본문과 인쇄 매일미사는 차이가 있을 수 있음.
''')
write('docs/progress.md','''## 2026-10-19 실제 본문 하루 연결 v44
- 사용자 “진행하세요”로 cod-e Stage 2 범위/구조 승인. Stage 3 데이터 검증/연결 구현 완료, Stage 4 검토 자료 작성·사용자 확인 대기, Stage 5 최종 품질 사인오프 미착수.
- data/days/2026-10-18.json, data/sources.json, 실제 JSON Schema, 검증/선택/앵커 함수 및 v44 작성. 공식 날짜 페이지 저장본 연결, 잘못된 날짜/ID/출처/override 차단. 본기도 선택지 기존 UI 유지.
- 독서/복음/화답송 텍스트/환호송/예물·영성체 후 기도/감사송/기도 지향 연결. 사제 마침 기도와 주보 악보 missing, 본당 공지 mock. mock 공식 본문을 보충 생성하지 않음.
- 테스트 Red→Green 및 스키마 정상/오류, 실제 fixture 참조, UI 23개 결과 그룹 통과. docs/03-test-plan.md, docs/04-verification.md. 실제 브라우저/태블릿 QA는 연결 부재로 미실행.
- 웹디자인 후속 단계로 임의 이동하지 않음. v43 보존, 검토 v44. 권장 커밋: feat: connect verified daily mass snapshot with schema guards.
''',True)
write('ENGINEERING.md','''## 2026-10-19 하루치 본문 연결 v44
사용자 “진행하세요”로 docs/02-architecture.md 승인. JSON Schema와 교차 참조 검증, 날짜별 선택, 앵커 fallback을 구현하고 Red→Green 확인. 실제 공식 날짜 저장본은 data/days/2026-10-18.json, 출처는 data/sources.json.
Stage 3 구현 완료. Stage 4 증거 docs/04-verification.md 작성 및 검토 대기. 안정 위치 영구 저장, 실제 태블릿·접근성 전체 검증은 남아 있음. Stage 5 최종 리뷰/승인을 추정하지 않음.
''',True)
write('README.md','''## 실제 전례문 검토 v44 (2026-10-19)
review/02-ia-v44.html을 열면 2026-10-18 하루 저장본을 사용합니다. 다른 날짜는 미연결로 표시합니다. 주보 화답송 악보·사제 마침 기도·본당 공지는 실제 자료 확인이 남아 있습니다.

검사: `node work/test-daily-document.cjs`, `node work/test-reader-v44.cjs`, 번들 Python으로 `work/test-daily-schema.py` 실행. JSON Schema 검사는 work/schema-deps의 jsonschema 4.26.0 사용. 재생성: 확보한 공식 HTML에서 `work/build-daily-data.py` → `work/connect-daily.py` 순서. 데이터 구조는 schemas/mass-document.schema.json, 출처와 재배포 조건 확인 상태는 data/sources.json. 상세 검수 한계는 docs/04-verification.md.
''',True)
p=Path('docs/02-architecture.md');text=p.read_text(encoding='utf-8').replace('상태: DRAFT, 구현 전 범위·구조 승인 대기.','상태: APPROVED. 사용자 “진행하세요”로 범위·구조 승인.');write(str(p),text)
print('Updated plan, evidence, approved architecture, engineering status and README.')
