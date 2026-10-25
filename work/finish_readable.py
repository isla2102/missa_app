from pathlib import Path
import json,xml.etree.ElementTree as E,shutil
base=Path('docs/교중미사악보/reengraved');old=json.loads((base/'autofit-large/manifest.json').read_text(encoding='utf-8'));new=json.loads((base/'autofit-readable/manifest.json').read_text(encoding='utf-8'))
for a,b in zip(old,new):
 assert a['key']==b['key'] and a['systems']==b['systems'];assert E.tostring(E.parse(base/'autofit-large'/(a['key']+'.musicxml')).getroot())==E.tostring(E.parse(base/'autofit-readable'/(a['key']+'.musicxml')).getroot())
a=E.parse(base/'autofit-large/kyrie.svg').getroot();b=E.parse(base/'autofit-readable/kyrie.svg').getroot();assert a.get('width')==b.get('width');ratio=float(b.get('height'))/float(a.get('height'));print('PASS identical width/line breaks/notes; Kyrie height ratio:',round(ratio,2))
entry=f'''\n## 2026-10-19 악보 가독성 추가 확대 v38\n- 사용자 화면에서 자비송 아래 여백 대비 악보가 작아 내부 배치 폭 2450→1500, 출력 폭은 297mm 유지. 음표/오선 크게 확대, 가사와 오선 사이 간격 3→8로 증가. 자비송 연속 미리보기 높이 v37 대비 {ratio:.2f}배.\n- 11양식 음표 XML/시스템 수/줄바꿈/가로 폭 동일 검사 통과. 가사는 기존 음표별 수평 슬롯 안에 들어가게 보정하여 과밀한 구간 겹침 방지. 연속 파일 유지, 넘치는 높이는 카드 세로 스크롤.\n- 새 자산 autofit-readable/, 최신 review/02-ia-v38.html. 전체 인쇄 합본은 큰 악보로 15쪽, 화면은 종이 페이지 구분 없이 연결. PDF 전체 렌더 후 시각 검수 및 500px 자비송 미리보기 확인. node syntax/test-reader-v38 회귀 통과. 실제 브라우저 시각 QA 미실행.\n'''
for name in ['docs/progress.md','design.md']:
 p=Path(name);shutil.copy2(p,'scratch/'+p.name+'.before-v38');p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
