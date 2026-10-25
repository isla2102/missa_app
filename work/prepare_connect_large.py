from pathlib import Path
s=Path('work/connect_autofit.py').read_text(encoding='utf-8').replace("dest=base/'autofit'","dest=base/'autofit-large'").replace('v36','v37').replace('v35','v36').replace('before-autofit.json','before-large.json');Path('work/connect_large.py').write_text(s,encoding='utf-8')
