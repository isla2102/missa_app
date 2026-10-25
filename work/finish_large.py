from pathlib import Path
import shutil
entry='''\n## 2026-10-19 악보 크기 확대 v37\n- 기존 297mm 가로 폭/역할별 줄 나눔 유지. Verovio 내부 배치 폭 2970→2450으로 축소 후 같은 출력 폭으로 맞춰 음표·오선·글자 약 20% 확대. 긴 다음절 가사는 겹침 방지를 위해 개별 크기 보정.\n- autofit-large/ 별도 자산 생성, v36 보존. 11양식의 MusicXML/시스템 수/실제 줄바꿈 전후 동일 검사 통과. 뷰어 연속 SVG 및 PDF 경로/로딩 전 크기 갱신.\n- 가로 줄은 추가하지 않음. 세로 크기 증가로 대영광송 PDF 3쪽, 전체 인쇄 합본 output/pdf/parish-scores-large.pdf 8쪽. 화면은 곡별 단일 연속 스크롤 유지.\n- 최종 합본 PNG 8쪽 직접 확인, note 데이터 동일·297mm 폭·줄바꿈 보존 검사, node syntax/test-reader-v37 전체 회귀 통과. 실제 브라우저 시각 QA 미실행. 최신 review/02-ia-v37.html.\n'''
for name in ['docs/progress.md','design.md']:
 p=Path(name);shutil.copy2(p,'scratch/'+p.name+'.before-v37');p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
