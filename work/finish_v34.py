from pathlib import Path
import shutil
entry='''\n## 2026-10-19 지정 기도 단일 스크롤 페이지 v34\n- 보편 지향 기도 네 지향/응답 전체를 1페이지로 묶고 넘치면 세로 스크롤. 사제 마침 기도+아멘은 별도 독립 1페이지.\n- 예물 준비 기도와 예물 기도를 같은 1페이지로 결합, 넘치면 세로 스크롤. 두 그룹 모두 본문 페이지 분할 제외.\n- node --check/test-reader-v34 전체 회귀 및 지향응답 8블록/마침+아멘 2블록 별도 페이지/예물기도 2블록 단일 페이지·스크롤 검사 통과. 실제 브라우저 시각 QA 미실행. 최신 review/02-ia-v34.html, 2단계 보완 유지.\n'''
for name in ['docs/progress.md','design.md']:
 p=Path(name);shutil.copy2(p,'scratch/'+p.name+'.before-v34');p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
