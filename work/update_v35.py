from pathlib import Path
import re,shutil
s=Path('review/02-ia-v34.html').read_text(encoding='utf-8').replace('v34','v35')
s=s.replace("['intercession-petitions','intercession-conclusion','offertory-prayers'].includes(group.key)?", "(['intercession-petitions','intercession-conclusion','offertory-prayers'].includes(group.key)||group.blocks.every(block=>block.item?.title==='감사기도 제2양식'))?")
Path('review/02-ia-v35.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v35-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v34.cjs').read_text(encoding='utf-8').replace('02-ia-v34.html','02-ia-v35.html');t+='''\nconst ep35=run("paginateSections(flowBlocks(2).filter(b=>b.item?.title==='감사기도 제2양식'),()=>false,()=>{throw new Error('must not split EP')})");assert.equal(ep35.length,3);assert.ok(ep35.every(p=>p.oversize&&p.blocks.length===1));assert.ok(ep35.some(p=>p.blocks[0].displayTitle==='감사기도 제2양식 · 성찬 제정'));console.log('PASS v35: each EP II text section stays on one scroll page without continuation fragments.');\n''';Path('work/test-reader-v35.cjs').write_text(t,encoding='utf-8',newline='\r\n')
entry='''\n## 2026-10-19 감사기도 본문 단일 스크롤 v35\n- 감사기도 제2양식의 서문/성찬 제정/기념과 봉헌 본문 구간은 각각 1페이지에 보존하고 넘치면 세로 스크롤. 계속 페이지로 분할하지 않음. 사이의 거룩하시도다/신앙의 신비여/아멘 악보 배치는 유지.\n- node syntax/test-reader-v35 전체 회귀 및 본문 3구간 단일 스크롤 페이지 검사 통과. 실제 브라우저 시각 QA 미실행. 최신 review/02-ia-v35.html.\n'''
for name in ['docs/progress.md','design.md']:
 p=Path(name);shutil.copy2(p,'scratch/'+p.name+'.before-v35');p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
