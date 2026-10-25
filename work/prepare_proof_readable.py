from pathlib import Path
s=Path('work/proof_fit_svg.py').read_text(encoding='utf-8').replace('autofit/gloria.svg','autofit-readable/kyrie.svg').replace('autofit-svg-proof','readable-svg-proof');Path('work/proof_readable.py').write_text(s,encoding='utf-8')
