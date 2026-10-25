from pathlib import Path
import re
s=Path('review/02-ia-v29.html').read_text(encoding='utf-8').replace('v29','v30')
rule=' .reader__reading-liturgy { flex: 1; min-block-size: 0; display: flex; flex-direction: column; }'
assert rule in s;s=s.replace(rule+'\n','')
anchor=' .reader__liturgy { display: grid; gap: var(--draft-item-gap); }'
s=s.replace(anchor,anchor+'\n'+rule+'\n .reader__dialogue--stacked { grid-template-columns: minmax(0, 1fr); }')
s=s.replace(" if(block.alternative){const card=", " if(['제1독서','제2독서','복음'].includes(block.item?.title)){node.querySelectorAll('.reader__dialogue').forEach(pair=>pair.classList.add('reader__dialogue--stacked'));}\n if(block.alternative){const card=")
Path('review/02-ia-v30.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v30-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v29.cjs').read_text(encoding='utf-8').replace('02-ia-v29.html','02-ia-v30.html').replace("n.className==='reader__dialogue'", "n.classList.contains('reader__dialogue')").replace("x.className==='reader__dialogue'", "x.classList.contains('reader__dialogue')")
Path('work/test-reader-v30.cjs').write_text(t,encoding='utf-8',newline='\r\n')
