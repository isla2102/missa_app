from pathlib import Path
import shutil
note='''\n\n## 2026-10-18 시기별 의미 도움말 v20
- 2단계 IA 보완: 전례 시기 목록의 각 카드 우측 상단에 ? 버튼. 연중 두 구간은 같은 의미 설명을 공유하고 사순/부활 설명은 각각 제공.
- 버튼 클릭/키보드 활성화로 별도 native dialog. 기존 기간 목록 유지, 닫기/ESC 후 해당 ? 버튼으로 초점 복귀. aria-label/haspopup/controls 및 설명 연결, 출처 링크 제공. hover 전용 도움말 대신 터치 가능한 모달.
- 설명 참고: GOODNEWS 유익한 교리여행32 전례력 https://home.catholic.or.kr/pdsm/bbs_view.asp?id=185256&menu=4798 . 원문 복사 없이 쉬운 말로 요약.
- node --check work/review-ia-v20-check.js 및 node work/test-reader-v20.cjs 통과: 기존 회귀와 카드4개/의미3종/부모 모달 유지 검사. 실제 브라우저 시각/스크린리더 검사는 미실행.
- 최신 review/02-ia-v20.html. v19 보존, 단계 승인으로 간주하지 않음.
'''
for name in ['docs/progress.md','design.md','ENGINEERING.md']:
 p=Path(name);shutil.copy2(p,Path('scratch')/(p.name+'.before-v20'));p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8',newline='\r\n')
