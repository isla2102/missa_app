from pathlib import Path
import re,json
# Completed editions are registered explicitly; recognition-only files never enter this list.
registry={'아멘':[{'kind':'engraved','title':'아멘','path':'../docs/교중미사악보/reengraved/amen.pdf','preview':'../docs/교중미사악보/reengraved/amen.svg','status':'사진 대조 완료 · 본당 최종 교정 전'}]}
p=Path('docs/교중미사악보/reengraved/registry.json');p.write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
p=Path('work/update_review_v18.py');s=p.read_text(encoding='utf-8')
insert="""registry=json.loads(Path('docs/교중미사악보/reengraved/registry.json').read_text(encoding='utf-8'))
for assets in registry.values():
 for asset in assets:
  assert (Path('review')/asset['path']).is_file() and (Path('review')/asset['preview']).is_file()
s=re.sub(r'const reengravedPrincipalScores = .*?;\\n','const reengravedPrincipalScores = '+json.dumps(registry,ensure_ascii=False)+';\\n',s,count=1)
"""
s=s.replace("Path('review/02-ia-v18.html').write_text",insert+"Path('review/02-ia-v18.html').write_text")
p.write_text(s,encoding='utf-8',newline='\r\n')
entry='''\n\n## 2026-10-18 성찬·마침 세부 프레임 및 모달 v18\n- 악보 크게보기 공통 dialog 추가. 사진/목데이터는 큰 이미지, 완료된 아멘은 modal 내부 PDF object로 표시. PDF 열기/원본 열기를 악보 크게 보기 버튼으로 교체. 닫기·ESC·초점 복원 구조, PDF 미지원 시 파일 링크 fallback. 실제 PDF plugin 표시 검증은 미완료.\n- 입당/봉헌/영성체/파견 성가는 한 페이지 높이 mock 악보 카드. 봉헌 성가와 예물 준비 기도 분리(새 목차 항목·기존 ID 보존), 영성체 성가 별도 목차·카드 추가.\n- 예물 기도/영성체 후 기도는 매일미사 연결용 mock 카드, 아멘 별도 강조. 공지는 주보 mock 카드 및 신부님 안내 표시. 실제 주보·외부 본문 연동 아님.\n- 사용자 본당 선택으로 감사기도 제2양식 확정. 표시 타이틀 및 하위 계속 제목 수정, 양식 미확정/감사송 대화/인쇄본 수록 감사송 편집 안내 제거. 원본 텍스트 레퍼런스는 보존.\n- 사용자 요청의 본당 시기별 신앙의 신비여: 연중/사순/부활에 응답 한 가지와 사진의 해당 구간만 표시. 교회 보편 의무 규정으로 주장하지 않음. 2026 CBCK 이동 축일 자료(https://missa.cbck.or.kr/Liturgy)로 시기 범위 저장. 파스카 성삼일·주님 만찬 미사/성야 경계·대림/성탄 상세·다른 연도는 자동 응답 미적용, 미확인으로 처리.\n- 시기 배지를 dialog 여는 button으로 전환. 2026년 연중 두 구간, 사순·부활 기간, 선택한 현재 구간 강조, 출처 링크. 다른 연도는 자료 연결 전 표시.\n- 파견 사제 선택지 4개, 공통 합송 1개, 앞 세 선택지에 또는 표시. 미확정 안내 제거.\n- 회차 표시명 저녁미사로 축약, 원래 youth 값·주일 저녁 의미 유지. select는 최대 콘텐츠 고유 폭 사용(긴 주일 저녁 젊은이 미사 옵션 제거).\n- 재조판 완료 레지스트리 docs/교중미사악보/reengraved/registry.json 추가. 현재 아멘만 등록. 새 곡 조판·사진 대조·파일 검증 후 이 목록과 검토 HTML 스냅샷을 함께 갱신하여 순차 교체하는 작업 방침. 파일 감시/예약 작업을 생성한 것은 아님.\n- 검사: node --check work/review-ia-v18-check.js, node work/test-reader-v18.cjs 통과. 전체 흐름 DOM 회귀, 4종 mock 악보/사진/PDF 모달, 성찬 분리/기도·주보 출처, 제2양식 안내 제거, 시기 응답·세 crop·날짜 경계·미지원일, 파견 4+1, 시기 모달 현재 표시, 저녁 라벨·select 폭 검사. 실제 브라우저 크기·PDF 표시·전체 접근성 자동 검사는 미실행.\n- review/02-ia-v18.html 검토 대기. 이전 v17 보존, 단계 확정 아님.\n'''
for name in ['docs/progress.md','design.md','ENGINEERING.md','README.md']:
 p=Path(name);Path('scratch/'+p.name+'.before-v18').write_bytes(p.read_bytes())
 text=entry if name!='README.md' else '\n\n## 최신 검토 v18\nreview/02-ia-v18.html: 공통 악보 모달(PDF/사진/mock), 봉헌·예물 준비 분리, 네 성가 mock, 매일미사/주보 mock 카드, 감사기도 제2양식, 본당 시기별 응답과 시기 기간 모달, 파견 4+1, 저녁미사 축약. 검사: node work/test-reader-v18.cjs. 시기 데이터는 2026 한정, 전체 전례력·외부 자료 API 미구현. 재조판 등록 목록: docs/교중미사악보/reengraved/registry.json(현재 아멘).\n'
 p.write_text(p.read_text(encoding='utf-8')+text,encoding='utf-8',newline='\r\n')
