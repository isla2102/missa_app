from pathlib import Path
s=Path('work/enlarge_scores.py').read_text(encoding='utf-8').replace("dest=base/'autofit-large'","dest=base/'autofit-readable'").replace("'pageWidth':2450","'pageWidth':1500")
Path('work/readable_scores.py').write_text(s,encoding='utf-8')
s=Path('work/bundle_large.py').read_text(encoding='utf-8').replace('autofit-large','autofit-readable').replace('parish-scores-large.pdf','parish-scores-readable.pdf');Path('work/bundle_readable.py').write_text(s,encoding='utf-8')
