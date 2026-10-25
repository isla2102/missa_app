from pathlib import Path
p=Path('work/update_review_v12.py')
s=p.read_text(encoding='utf-8').replace('.reader__item--guided-score { grid-template-rows:', '.reader__item--score.reader__item--guided-score { grid-template-rows:')
p.write_text(s,encoding='utf-8',newline='\r\n')
