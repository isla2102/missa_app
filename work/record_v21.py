from pathlib import Path
import json,shutil
report={'date':'2026-10-18','userIncipits':{'대영광송':'레레레레레도레 솔파레도 레레','거룩하시도다':'라라라라솔라 솔솔솔솔파솔','신앙의 신비여':'파파파솔솔솔 라라라라라솔파솔레','하느님의 어린양':'라 라솔라 솔 솔라솔파레도'},'sources':['https://missale.cbck.or.kr/Sound','https://gregobase.selapa.net/usage.php?id=ky'],'examinedGabcCount':164,'method':'Exploratory diatonic interval comparison, collapsing repeated pitches to accommodate Korean syllables; Latin Gloria/Sanctus/Agnus candidates. Rhythmic/vernacular adaptation not conclusively identified.','result':'No full opening match confirmed. Partial internal matches do not establish identity. Memorial acclamation unresolved; not treated as a medieval Kyriale movement.','confirmedCatholicHymnNumbers':{'복음 환호송':365},'notes':'Do not replace parish scores with a guessed Gloria XV, Sanctus XVIII, Agnus XVIII, or Mass VIII. Official CBCK Sound has Korean chant score/audio options; direct remote score image inspection unavailable in current tools.'}
Path('docs/references/gregorian-incipit-search-20261018.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
text='''\n\n## 2026-10-18 주석5건 및 그레고리오 선율 탐색 v21
- 보편 지향 기도: 2026-10-18 CBCK 정적 자료의 4지향과 각 지향 직후 합송 응답, 끝에 사제 마침 카드/아멘. 별도 악보 미등록 응답 프레임 제거. 다른 날짜는 mock 지향+응답. 해당 날짜 공식 페이지에는 사제 마침 원문 미수록이므로 연결용 mock 명시, 공식 본문으로 꾸미지 않음.
- 감사기도 표시에서 (타대오와 협력 주교들)로 사용자 지정 변경. 원본 사진 판독 레퍼런스는 보존.
- 맺음 환호는 full-page score 해제, 실제 두 줄 이미지 높이에 따름. 어린양은 원본 불변 SVG viewBox [360,1800,2460,1960]로 해당 부분만 표시, 크게보기 동일 crop.
- 목차는 현재 항목을 스크롤 영역 높이의 25% 지점에 맞춤(끝 경계에서는 브라우저 clamp). 페이지 전체가 아닌 목차 rail만 이동.
- 사용자 제공 계명으로 기존 MIDI 및 GregoBase Gloria/Sanctus/Agnus 164개 GABC 후보의 이조/동음반복 축약 음형 탐색. 부분 일치는 있으나 도입 전체 일치곡 미확정, 추측 번호나 라틴 곡으로 교체하지 않음. CBCK Sound 공식 그레고리오 페이지 확인. 상세 docs/references/gregorian-incipit-search-20261018.json.
- node --check work/review-ia-v21-check.js, node work/test-reader-v21.cjs 통과. 이전 회귀와 4지향4응답/사제mock/아멘/다른날짜fallback/주교표기/짧은카드/crop 검사. 사진 미리보기 직접 확인. 실제 브라우저 높이 및 목차 좌표 시각 QA 미실행.
- 최신 review/02-ia-v21.html. v20 보존, 2단계 검토 보완이며 다음 단계 승인 아님.
'''
for name in ['docs/progress.md','design.md','ENGINEERING.md']:
 p=Path(name);shutil.copy2(p,Path('scratch')/(p.name+'.before-v21'));p.write_text(p.read_text(encoding='utf-8')+text,encoding='utf-8',newline='\r\n')
