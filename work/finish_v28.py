from pathlib import Path
import shutil
entry='''\n## 2026-10-19 페이지 안정화·이동 목적지 v28\n- 재조판 SVG 미리보기의 width/height를 원본 메타데이터에서 추출해 img 생성 시 지정. 처음 방문의 미로딩 이미지와 재방문의 캐시 이미지가 동일한 비율/높이를 확보하도록 하여 복음환호송 마지막 합송의 페이지 위치 변동 원인을 수정. 로딩 이벤트로 재페이지분할하지 않음.\n- 하단 이전/다음 버튼에 실제 목적지 펼침의 첫 순서명 표시. 계속 본문/복음환호송 성가대·합송 구분, 전례 경계는 전례명+순서명 표시. 전체 시작/끝은 미사 시작/마침. 긴 이름은 말줄임 및 title/aria-label 전체 이름, 고정 3열로 버튼 줄 높이 변동 방지.\n- node --check 및 test-reader-v28 전체 회귀 통과. 전체 재조판 미리보기 크기 지정, 최초/재생성 크기 동일, 이전/다음/전례경계 목적지명 검사. 실제 브라우저 캐시 왕복 시각 QA는 미실행. 2단계 보완 유지, 최신 review/02-ia-v28.html.\n'''
for name in ['docs/progress.md','design.md']:
 p=Path(name);shutil.copy2(p,'scratch/'+p.name+'.before-v28');p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
