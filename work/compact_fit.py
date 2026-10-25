from pathlib import Path
import re
p=Path('review/02-ia-v36.html');s=p.read_text(encoding='utf-8').replace('assets[0].systems<=2','assets[0].systems<=3');p.write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v36-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
