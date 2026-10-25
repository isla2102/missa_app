from pathlib import Path
import json,shutil
policy='''# 콘텐츠 출처와 이용 조건 — 2026-10-19

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
'''
Path('docs/content-source-policy.md').write_text(policy,encoding='utf-8',newline='\r\n')
audit='''# 통상문 순서·범위 대조 기록

2026-10-19. 사용자 지정 GOODNEWS 통상문(2017-10-15 발행 표시)을 현재 v53 계열 검토본과 대조. 대상 URL의 day=20261019 고유문을 10월18일 데이터로 복사하지 않음. 통상문 구조와 고유문을 구분.

## 큰 순서
시작 예식 → 말씀 전례 → 성찬 전례 → 마침 예식의 순서는 일치. 참고 페이지에서 감사기도·영성체 예식이 별도 설명 장으로 나와도 성찬 전례 내부 단계이므로 앱의 4개 최상위 예식을 6개로 늘릴 근거는 아님.
입당/성호경/인사/참회/자비송/대영광송/본기도, 독서/화답송/환호송/복음/강론/신경/보편 지향 기도, 예물 준비·기도/감사기도/주님의 기도/평화/어린양/영성체/영성체 후 기도, 공지/강복/파견의 큰 흐름 확인.

## 부족하거나 분리해 보강할 항목
- 영성체 분배 때의 개별 응답: 현재 영성체 본문은 공동체 초대/응답까지만 포함. 성체를 모실 때의 개별 응답과 예비신자 참여 안내를 별도 안내로 검토할 필요가 있음.
- 빵 나눔: 어린양 악보가 표시되지만 해당 예식의 뜻과 자세 안내는 독립적으로 충분히 설명되지 않음.
- 영성체 후 침묵·감사: 영성체 후 기도와 별개로 침묵/감사 행위를 설명할 필요가 있음.
- 보편 지향 기도의 사제 시작·마침: 시작/마침 본문 및 본당 실제 선택이 미연결. 날짜별 기도 지향만으로 전체 예식 연결 완료라고 표시하지 않음.
- 성체를 모시기 전 사제의 속기도, 예물 준비 중 속기도·예물 봉헌, 성작 정리, 부제·주교 관련 예식은 참고 페이지에 더 자세함. 신자용 리더에서 생략한 보조 설명과 필수 공동 응답 누락을 구분해야 함.

## 선택 양식과 데이터 정확성
현재 감사기도 제2양식만 지원. 제1·3·4양식, 장엄 강복/백성을 위한 기도 등 선택 양식의 부재를 모든 미사의 필수 순서 누락으로 단정하지 않음. 실제 집전 선택을 연결할 확장 항목.
교황·교구장 이름과 시기별 신경 선택은 판독 초안/현재 코드 보정이 섞여 있음. 공식 검증 및 본당 실제 선택 확인 전 확정이라고 표기하지 않음.
새 공식 본문은 추가하지 않았으며 위 항목은 보강 목록으로 기록. 권리 확인 후 검증된 원문으로 연결할 것.

## 성가표 확인
첨부 HWP의 LIST_HEADER 표 셀과 본문 텍스트를 읽어 31일치 날짜/전례명과 번호를 추출. 원본 매크로·스크립트는 실행하지 않음. 첫 헤더의 열 병합에 따라 입당 1열, 예물 준비 2열, 영성체 3열, 파견 1열로 해석. 빈 칸 보존.
2026-10-18: 입당 416 / 예물 준비 238·221 / 영성체 154·153·152 / 파견 63. 수정보완판 추천 자료로 저장, 기존 회차별 선택 또는 재조판 악보의 성가 번호를 덮어쓰지 않음.
근거 파일: work/reference-research/hymn-cells.json, data/reference-sources/hymn-schedule-202610.json. 원본 해시는 JSON에 기록.
'''
Path('docs/ordinary-reference-review.md').write_text(audit,encoding='utf-8',newline='\r\n')
entry='''## 2026-10-19 사용자 출처·성가표·저작권 반영 v54
- GOODNEWS 통상문 순서/미지원 범위 대조 결과 docs/ordinary-reference-review.md. 큰 순서는 일치, 영성체 개별 응답·빵나눔·감사 침묵·보편기도 시작/마침 보강 목록 기록. 새 공식 본문 생성/추가 없음.
- 대구 주보 코드21/10월18일 PDF 링크, 주요기도문21개 원문 링크, 사용자 HWP31일 추천 번호를 data/reference-sources/로 정규화. 본당 회차 편성 미확정 유지.
- CBCK K7020 12월 게시글/첨부 확인. 사용자 제공 Copyright 및 K7300/20230535 규정 반영: 새 전문 내장/추가 자동 수집 보류, 개인 앱 허가 범위 미확인. docs/content-source-policy.md. 연락 발송 없음.
- 현행 생성기 연결, v54를 새 비교 스냅샷으로 보존. tests/reference-catalogs와 UI 링크/날짜 fallback 검사, 실제 Chrome에서21링크/추천번호/대구PDF 확인. 통합7개 명령 성공.
'''
for name in ['docs/progress.md','ENGINEERING.md','design.md']:
 p=Path(name);shutil.copy2(p,Path('scratch')/(p.name+'.before-content-references'));p.write_bytes((p.read_text(encoding='utf-8').rstrip()+'\n\n'+entry).replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
p=Path('README.md');shutil.copy2(p,'scratch/README.before-content-references.md');p.write_bytes((p.read_text(encoding='utf-8').rstrip()+'''\n\n## v54 출처 연결
현행 화면은 21종 주요기도문 원문 링크·대구대교구 주보 링크·사용자 제공 수정보완판 성가표 추천 번호를 표시합니다. 통합 검사는 7개 명령이며 출처 카탈로그 테스트 포함. 권리 확인 전 새 기도문 전문 수입·추가 자동 수집은 보류. docs/content-source-policy.md 및 docs/ordinary-reference-review.md 참조.\n''').replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
print('Recorded all requested sources, HWP findings, ordinary-order gaps and rights constraints.')
