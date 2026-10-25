from pathlib import Path
import re,shutil
s=Path('review/02-ia-v31.html').read_text(encoding='utf-8').replace('v31','v32')
s=s.replace("function sectionFlowKey(block){return", "function sectionFlowKey(block){if(block.item?.title==='성호경'||block.group==='인사')return 'opening-sign-and-greeting';return")
Path('review/02-ia-v32.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v32-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v31.cjs').read_text(encoding='utf-8').replace('02-ia-v31.html','02-ia-v32.html');t+='''\nconst opening32=run("flowBlocks(0).filter(b=>b.item?.title==='성호경'||b.group==='인사')");assert.equal(opening32.length,4);assert.equal(new Set(run("flowBlocks(0).filter(b=>b.item?.title==='성호경'||b.group==='인사').map(sectionFlowKey)")).size,1);const openingPages32=run("paginateSections(flowBlocks(0).filter(b=>b.item?.title==='성호경'||b.group==='인사'),blocks=>blocks.length<=4,b=>[b])");assert.equal(openingPages32.length,1);assert.equal(openingPages32[0].blocks.length,4);console.log('PASS v32: sign of cross and all greeting choices share one section/page when they fit.');\n''';Path('work/test-reader-v32.cjs').write_text(t,encoding='utf-8',newline='\r\n')
entry='''\n## 2026-10-19 성호경·인사 결합 v32\n- 사용자 지정 예외: 성호경과 인사 3양식/공통 응답을 같은 페이지 그룹으로 측정·배치. 제목과 목차 링크는 각각 유지. 다른 섹션 단위 페이지 경계와 두 페이지 정렬 규칙 유지.\n- node syntax 및 test-reader-v32 전체 회귀/성호경+인사 동일 그룹과 한 페이지 배치 검사 통과. 실제 브라우저 높이 검사는 미실행. 최신 review/02-ia-v32.html, 2단계 보완 유지.\n'''
for name in ['docs/progress.md','design.md']:
 p=Path(name);shutil.copy2(p,'scratch/'+p.name+'.before-v32');p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
