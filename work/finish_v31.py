from pathlib import Path
import shutil
entry='''\n## 2026-10-19 섹션 단위 페이지 나눔 v31\n- 기존 빈 공간에 다음 섹션을 이어붙이던 흐름을 변경. tocId 기준 섹션을 함께 측정하고, 한 페이지에 들어가면 한 페이지로 완료. 감사기도의 별도 제목/악보 부분은 각각 독립 섹션.\n- 두 페이지가 필요한 섹션은 왼쪽에서 시작하도록 오른쪽 잔여 페이지를 비워 다음 펼침으로 이동. 다음 섹션은 새 페이지에서 시작. 보편지향 기도는 지향/응답/마침기도/아멘 모두 같은 섹션.\n- 두 페이지보다 긴 내용은 둘째 페이지 내부 스크롤로 원문 보존. 독서 첫 펼침의 제1독서+화답송/제2독서 고정 구성과 기존 악보 내부 스크롤 유지.\n- node --check/test-reader-v31 전체 회귀 및 1페이지 우선/새 페이지 경계/두 페이지 왼쪽 정렬/offset/긴 내용 손실 없음/보편기도 그룹 검사 통과. 실제 브라우저 측정 시각 QA 미실행. 최신 review/02-ia-v31.html, 2단계 보완 유지.\n'''
for name in ['docs/progress.md','design.md']:
 p=Path(name);shutil.copy2(p,'scratch/'+p.name+'.before-v31');p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
