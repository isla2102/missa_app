from pathlib import Path
import re
s=Path('review/02-ia-v52.html').read_text(encoding='utf-8').replace('v52','v53')
needle="if(['제1독서','제2독서','복음'].includes(block.item?.title)){node.querySelectorAll('.reader__dialogue').forEach(pair=>pair.classList.add('reader__dialogue--stacked'));}"
assert needle in s
s=s.replace(needle,needle.replace("'복음']","'복음','감사기도 제2양식']"))
Path('review/02-ia-v53.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v53-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v52.cjs').read_text(encoding='utf-8').replace('02-ia-v52.html','02-ia-v53.html');t+='''\nconst ep53=run("renderBlock(flowBlocks(2).find(b=>b.item?.title==='감사기도 제2양식'))");const pairs53=walk(ep53).filter(n=>n.classList.contains('reader__dialogue'));assert.equal(pairs53.length,3);assert.ok(pairs53.every(n=>n.classList.contains('reader__dialogue--stacked')));console.log('PASS v53 all three Eucharistic Prayer dialogue pairs stack vertically.');\n''';Path('work/test-reader-v53.cjs').write_text(t,encoding='utf-8')
