from pathlib import Path
import re,shutil
s=Path('review/02-ia-v32.html').read_text(encoding='utf-8').replace('v32','v33')
s=s.replace("['신앙 고백','본기도','복음 환호송'].includes(block.item?.title)","['신앙 고백','본기도','복음 환호송','복음'].includes(block.item?.title)")
Path('review/02-ia-v33.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v33-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v32.cjs').read_text(encoding='utf-8').replace('02-ia-v32.html','02-ia-v33.html');t+='''\nconst gospel33=run("flowBlocks(1).filter(b=>b.item?.title==='복음')");assert.equal(gospel33.length,1);const page33=run("paginateSections(flowBlocks(1).filter(b=>b.item?.title==='복음'),()=>false,b=>[b])");assert.equal(page33.length,1);assert.equal(page33[0].oversize,true);assert.equal(page33[0].blocks.length,1);assert.ok(html.includes("['신앙 고백','본기도','복음 환호송','복음'].includes(block.item?.title)"));console.log('PASS v33: Gospel is unsplit, one oversize page with vertical overflow.');\n''';Path('work/test-reader-v33.cjs').write_text(t,encoding='utf-8',newline='\r\n')
entry='''\n## 2026-10-19 복음 단일 스크롤 페이지 v33\n- 복음은 본문 길이로 분할하지 않음. 페이지에 넘치면 기존 oversize 페이지의 세로 스크롤로 인사부터 마지막 합송까지 한 페이지에 보존. 다른 섹션 분할 규칙 유지.\n- node syntax/test-reader-v33 전체 회귀 및 복음 단일 블록/단일 oversize 페이지 검사 통과. 실제 브라우저 스크롤 시각 QA 미실행. 최신 review/02-ia-v33.html.\n'''
for name in ['docs/progress.md','design.md']:
 p=Path(name);shutil.copy2(p,'scratch/'+p.name+'.before-v33');p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
