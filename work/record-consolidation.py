from pathlib import Path
import shutil,re

def save(name,text):
 p=Path(name)
 if p.exists():shutil.copy2(p,Path('scratch')/(p.name+'.before-source-consolidation'))
 p.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
save('review/source/README.md','''# 검토 화면 원본

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
''')
save('docs/05-review.md','''# v53 기반 생성 과정 정리 — 4축 검수

2026-10-19. 상태: 검수 기록 완료, 최종 사용자 사인오프 대기. 코드 정리 범위는 사용자 “작업해” 지시로 승인. 웹디자인 후속 단계 승인을 뜻하지 않음.

## 정확성
- v53에서 shell/CSS/JS와 데이터 연결을 추출. JSON 직렬화 형식만 정규화해 생성 결과 전체를 v53과 비교, 동일 확인.
- 반복 생성 결과 동일 검사. 저장/데이터 모듈은 Node 테스트와 HTML 내장 코드가 같은 원본 사용.
- 과거 버전 HTML 덮어쓰기 금지, 프로젝트 밖 경로 차단. 등록된 PDF/SVG 실재 검사.
- 데이터·저장 정상/손상/거부·다른 날짜·범위 검사와 기존 렌더 회귀 검사 통과.

## 성능
- 실행 시 JSON fetch/추가 프레임워크 없음. 기존 v53 렌더 알고리즘 유지.
- 과거 버전을 순차 재생성하는 과정 제거. 모듈과 설정을 한 번 조합.
- 실제 기기 렌더 시간/스크롤 성능 수치는 측정하지 않았음. 연속 스크롤의 DOM 순회 비용은 그대로 남아 있음.

## 보안
- 내장 JSON의 < 및 U+2028/U+2029 escape로 script 종료 문자열 삽입 방지, roundtrip 테스트.
- 출력 경로 제한 및 보존 버전 보호. 실패한 날짜별 데이터 검증은 생성 중 중단.
- 데이터 본문은 기존 textContent 처리 유지. 로컬 저장 거부·손상은 예외로 리더를 중단시키지 않음.
- 외부 링크/성가 이미지는 기존 기능으로 유지. 배포 권한 검토는 별도 미완료.

## 유지보수성
- 공식 데이터와 악보 레지스트리를 원본 파일에서 읽는 단일 빌드. 새 버전을 문자열 치환해 만드는 연쇄 의존 제거.
- 테스트 시작점을 tests/로 통합. 전체 스크립트 초기화 경로와 모달 닫기 초점 복귀·내용 해제·리셋 초점·resize 연결 검사 추가.
- 기존 메인 렌더러는 동작 보존을 위해 크게 재작성하지 않음. 버전별 테스트의 역사적 로그 제목, 안내창의 과거 설명은 남아 있으며 별도 문구 정리가 필요.
- 음악 조판 엔진 통합·코드 커버리지 측정·실제 보조기기 접근성 검사는 이번에 완료하지 않음.

## 실행 증거
`node tools/check-review.cjs`: 6개 명령 모두 성공. 상세 work/review-check.log.
번들 Python `work/test-daily-schema.py`: 실제 문서와 3개 스키마 오류 사례 검사 성공.
VM 기반 전체 boot 검사는 화면 크기를 mock 처리하므로 실제 렌더/키보드 포커스 이동의 브라우저 검증을 대신하지 않음.

## 남은 최종 확인
실제 태블릿 방향 전환, 좁은 폭 상단 메뉴, 스크린리더, 새 파일의 file:// 저장 복원 확인. 이 검토만으로 프로덕션 배포 완료로 표시하지 않음.
''')
entry='''## 2026-10-19 v53 원본·생성·검사 통합
- 사용자 승인 범위: 화면 보존 코드 정리 및 품질 검수. review/source/에 shell/CSS/JS/공통 모듈/연결 설정 추출. tools/build-review.cjs가 독립적으로 review/02-ia-current.html 생성, 과거 HTML/패치 스크립트를 읽지 않음.
- tests/로 현행 회귀·저장·문서 검사 통합 및 full boot 검사 추가. tools/check-review.cjs 6명령 성공, 스키마 fixture/오류 검사 통과. work/review-check.log.
- v53과 JSON 형식 정규화 후 전체 내용 동일·결정성·경로보호·script escape·악보 파일 존재 검사. 모달 닫기 초점 복귀/정리·리셋 초점·resize 바인딩을 mock DOM에서 확인.
- docs/05-review.md에 4축 검수 및 미실행 범위 기록. 실제 기기·보조기기 QA와 최종 사인오프 미완료. 음악 조판 엔진의 통합은 별도 범위이며 현재 PDF/SVG 자산 보존.
'''
p=Path('docs/progress.md');s=p.read_text(encoding='utf-8');s=re.sub(r'## 현재 상태\n.*?(?=\n## 원본 확보)', '## 현재 상태\n- 2026-10-19: v53 기능 수정 누적. 2단계 정보 구조 보완 결과 정리 중이며 3~8단계 확정을 추정하지 않음.\n- 현행 검토: review/02-ia-current.html (v53과 동등한 단일 생성 결과).\n- cod-e: 코드 정리·자동 검수 완료, 실기 검증 및 최종 사인오프 대기.\n',s,flags=re.S);save(str(p),s.rstrip()+'\n\n'+entry)
for name in ['ENGINEERING.md','docs/04-verification.md','docs/03-test-plan.md']:
 p=Path(name);s=p.read_text(encoding='utf-8');save(str(p),s.rstrip()+'\n\n'+entry)
p=Path('README.md');s=p.read_text(encoding='utf-8');s=re.sub(r'## 현재 상태 \(2026-10-18\).*?(?=\n## 사용자 결정)', '''## 현재 상태 (2026-10-19)
- 현행 검토: review/02-ia-current.html. v53 동작과 데이터 유지.
- 생성: `node tools/build-review.cjs`
- 전체 검사: `node tools/check-review.cjs` (6개 명령, 상세 work/review-check.log)
- 원본/설정: review/source/README.md. 기존 버전 HTML과 과거 work 스크립트는 이력으로 보존합니다.
- 실제 태블릿/보조기기 검증, 전체 날짜 연동 및 디자인 후속 단계는 미완료입니다.
''',s,flags=re.S);save(str(p),s)
print('Recorded canonical generation, verification and four-axis review; preserved archives.')
