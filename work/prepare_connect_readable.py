from pathlib import Path
p=Path('work/readable_scores.py');s=p.read_text(encoding='utf-8').replace("'lyricTopMinMargin':3","'lyricTopMinMargin':8");p.write_text(s,encoding='utf-8')
s=Path('work/connect_large.py').read_text(encoding='utf-8').replace('autofit-large','autofit-readable').replace('v37','v38').replace('v36','v37').replace('before-large.json','before-readable.json');Path('work/connect_readable.py').write_text(s,encoding='utf-8')
