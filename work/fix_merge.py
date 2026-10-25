from pathlib import Path
p=Path('work/connect_remaining_v25.py');s=p.read_text(encoding='utf-8');s=s.replace("root.append(tree);y+=height+20", "\n  for child in tree:\n   if child.tag.endswith('}svg'):\n    child.set('width','1050');child.set('height',str(height))\n  root.append(tree);y+=height+20")
s=s.replace(".replace('--draft-score-action-z: 2;', '--draft-dialogue-width: 12rem; --draft-score-action-z: 2;',1)","")
p.write_text(s,encoding='utf-8')
p=Path('review/02-ia-v25.html');s=p.read_text(encoding='utf-8');import re;s=re.sub(r'(?:--draft-dialogue-width: 12rem;\s*)+', '--draft-dialogue-width: 12rem; ',s);p.write_text(s,encoding='utf-8',newline='\r\n')

