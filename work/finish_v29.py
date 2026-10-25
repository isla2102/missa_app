from pathlib import Path
import shutil
entry='''\n## 2026-10-19 독서 첫 펼침 고정·응답 중복 테두리 v29\n- 보편 지향 응답은 일반 콘텐츠 카드 안에 합송 카드가 들어가 이중 테두리가 생김. 낭송 모드의 바깥 컨테이너에 기존 무테두리 liturgy 변형 적용, 합송 테두리만 유지. 악보 준비중 모드는 기존 단일 카드 유지.\n- 말씀 전례 첫 펼침을 독서 전용으로 계획: 왼쪽 제1독서+마침 응답 2열+화답송, 오른쪽 제2독서+마침 응답 2열. 이후 복음환호송은 다음 펼침 시작. 독서 본문 카드가 나머지 세로 공간을 채우며 긴 본문은 내부 스크롤. 극소 높이에는 페이지 스크롤 허용.\n- node --check 및 test-reader-v29 전체 회귀 통과. 독서 2페이지 그룹/복음환호송 경계/본문 신축 클래스/마침 응답 보존/낭송 외곽 무테두리 검사. 실제 브라우저 높이 시각 검사는 미실행. 2단계 보완 유지, 최신 review/02-ia-v29.html.\n'''
for name in ['docs/progress.md','design.md']:
 p=Path(name);shutil.copy2(p,'scratch/'+p.name+'.before-v29');p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
