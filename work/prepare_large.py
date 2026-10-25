from pathlib import Path
s=Path('work/autofit_scores.py').read_text(encoding='utf-8').replace("dest=base/'autofit'","dest=base/'autofit-large'").replace("'pageWidth':2970","'pageWidth':2450")
Path('work/enlarge_scores.py').write_text(s,encoding='utf-8')
s=Path('work/bundle_autofit.py').read_text(encoding='utf-8').replace('reengraved/autofit','reengraved/autofit-large').replace('parish-scores-autofit.pdf','parish-scores-large.pdf');Path('work/bundle_large.py').write_text(s,encoding='utf-8')
