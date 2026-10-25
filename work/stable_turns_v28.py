from pathlib import Path
import re
p=Path('review/02-ia-v28.html');s=p.read_text(encoding='utf-8')
s=s.replace('.reader__turns { grid-column: 1; grid-row: 3; display: flex; justify-content: space-between; gap: var(--draft-gap); }','.reader__turns { grid-column: 1; grid-row: 3; display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); align-items: center; gap: var(--draft-gap); }\n .reader__turn-button { min-inline-size: 0; max-inline-size: 100%; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; justify-self: start; }\n .reader__turn-boundary { justify-self: end; }')
s=s.replace('type="button" data-js="page-prev"','type="button" class="reader__turn-button" data-js="page-prev"').replace('class="reader__turn-boundary" data-js="page-next"','class="reader__turn-button reader__turn-boundary" data-js="page-next"')
s=s.replace("find('page-prev').textContent='← '+previousLabel;", "find('page-prev').title=previousLabel;find('page-next').title=nextLabel;find('page-prev').textContent='← '+previousLabel;")
p.write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v28-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
