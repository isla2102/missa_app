from pathlib import Path
import shutil
note='''\n\n## 2026-10-18 성가 카드 겹침·스크롤 버그 v23
- 원인: 고정 높이 2행 score grid에 제목/폼/카드 3개 자식을 넣어 카드가 암시적 행으로 밀림. 번호 폼을 제목행 안에 넣어 제목행+minmax 악보행 2개로 복구.
- 원인: 원격 악보 img onload 때 전체 페이지를 재조합하여 이미지 생성/로드/재조합 반복 및 내부 스크롤 초기화 가능. 고정 스크롤 프레임이므로 해당 onload reflow 제거.
- 상태줄/figure 캡션의 중복 성가번호 제거. 악보 원본 제목만 유지, 오류/번호 미입력 상태만 별도 안내. 크게보기 overlay 유지.
- node --check work/review-ia-v23-check.js, node work/test-reader-v23.cjs 통과. 123번 경로/헤더 내부폼/2자식구조/중복문구없음/onload재조합없음 및 기존회귀. 실제 브라우저 스크롤 좌표/시각 QA는 미실행.
- review/02-ia-v23.html 검토용, v22 보존. 2단계 유지.
'''
for name in ['docs/progress.md','design.md','ENGINEERING.md']:
 p=Path(name);shutil.copy2(p,Path('scratch')/(p.name+'.before-v23'));p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8',newline='\r\n')
