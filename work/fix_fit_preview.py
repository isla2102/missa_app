from pathlib import Path
p=Path('work/autofit_scores.py');s=p.read_text(encoding='utf-8');s=s.replace("{sy-(600000-y1)*scale}) scale({scale})", "{sy-(drawing.height-y1)*scale}) scale({scale*drawing.width/29700})")
p.write_text(s,encoding='utf-8')
