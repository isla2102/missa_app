from pathlib import Path
import shutil
entry='''\n## 2026-10-19 독서·복음 1열 복구 및 본문 전용 높이 v30\n- 제1/2독서 마침말·합송과 복음의 인사·마침말 합송을 세로 1열로 복구. 인사 마지막 양식/감사기도의 기존 2열은 요청 범위 밖으로 유지.\n- 독서 전용 flex 규칙이 layout 레이어에 있어 components의 기본 liturgy grid에 덮인 원인 수정. 독서 flex 규칙을 기본 규칙 뒤 같은 components 레이어로 이동. 안내·마침 응답은 자연 높이, 본문 카드만 남는 높이를 채우도록 복구. 첫 펼침 독서/화답송 배치는 유지.\n- node --check/test-reader-v30 전체 회귀 및 독서·복음 세로 변형/레이어 우선순위 검사 통과. 실제 브라우저 높이 시각 검사는 미실행. 최신 review/02-ia-v30.html, 2단계 보완 유지.\n'''
for name in ['docs/progress.md','design.md']:
 p=Path(name);shutil.copy2(p,'scratch/'+p.name+'.before-v30');p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
