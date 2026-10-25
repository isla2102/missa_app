from pathlib import Path
p=Path('work/check_continuous_svg.py');s=p.read_text(encoding='utf-8').replace("(key+'.svg')","(key+'-v26.svg')").replace("+'-continuous-proof", "+'-v26-continuous-proof")
Path('work/check_continuous_v26.py').write_text(s,encoding='utf-8')
