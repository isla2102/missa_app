import json,difflib
from pathlib import Path
tracks=json.loads(Path('work/goodnews/midi-notes.json').read_text(encoding='utf-8'))
queries={'Gloria':[62]*5+[60,62,67,65,62,60,62,62], 'Sanctus':[69]*4+[67,69]+[67]*4+[65,67], 'Memorial':[65]*3+[67]*3+[69]*5+[67,65,67,62], 'Agnus':[69,69,67,69,67,67,69,67,65,62,60]}
for title,q in queries.items():
 out=[]
 for num,ts in tracks.items():
  for ti,t in enumerate(ts):
   seq=[e['pitch'] for e in t['events']]
   for shift in range(-12,13):
    target=[x+shift for x in q];m=difflib.SequenceMatcher(None,target,seq,autojunk=False).find_longest_match()
    out.append((m.size,num,ti,shift,m.a,m.b,seq[:22]))
 print(title, sorted(out,reverse=True)[:4])
