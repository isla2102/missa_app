import json
from pathlib import Path
D=json.loads(Path('work/goodnews/midi-notes.json').read_text(encoding='utf-8'))
for n in [306,310,315,320,325,350,354,387,388,377,378,379,380,381,382,383,384,385,386]:
 print(n,[(t['name'],[x['pitch'] for x in t['events'][:30]]) for t in D[str(n)][:2]])
