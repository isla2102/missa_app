from pathlib import Path
import re
s=Path('review/02-ia-v51.html').read_text(encoding='utf-8').replace('v51','v52')
s=s.replace(' .reader[data-orientation="portrait"] .reader__header--navigation { flex-wrap: wrap; overflow: visible; }',' .reader[data-orientation="portrait"] .reader__header--navigation { flex-wrap: nowrap; gap: var(--draft-header-gap); overflow-x: auto; }')
s=s.replace(' .reader[data-orientation="portrait"] .reader__header-controls { flex-basis: 100%; flex-wrap: wrap; order: 3; }',' .reader[data-orientation="portrait"] .reader__header-controls { flex-basis: auto; flex-wrap: nowrap; }')
s=s.replace(' .reader[data-orientation="portrait"] .reader__menu-toggle { display: block; }',' .reader[data-orientation="portrait"] .reader__menu-toggle { display: block; flex-shrink: 0; }')
Path('review/02-ia-v52.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v52-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v51.cjs').read_text(encoding='utf-8').replace('02-ia-v51.html','02-ia-v52.html');t+='''\nassert.ok(html.includes('.reader[data-orientation="portrait"] .reader__header--navigation { flex-wrap: nowrap;'));assert.ok(html.includes('.reader[data-orientation="portrait"] .reader__header-controls { flex-basis: auto; flex-wrap: nowrap; }'));assert.ok(!html.includes('flex-basis: 100%; flex-wrap: wrap; order: 3;'));console.log('PASS v52 portrait header stays on one line with menu.');\n''';Path('work/test-reader-v52.cjs').write_text(t,encoding='utf-8')
