from pathlib import Path
import zipfile,xml.etree.ElementTree as E,json,difflib
D=json.loads(Path('work/goodnews/midi-notes.json').read_text(encoding='utf-8'))
for f in sorted(Path('work/music-omr-output').glob('*.mxl')):
 z=zipfile.ZipFile(f);r=E.fromstring(z.read(next(n for n in z.namelist() if n.endswith('.xml') and not n.startswith('META'))));ps=[]
 for n in r.findall('.//part')[0].findall('.//note'):
  if n.find('pitch') is None:continue
  ps.append((int(n.findtext('pitch/octave'))+1)*12+{'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}[n.findtext('pitch/step')]+int(n.findtext('pitch/alter','0')))
 if not ps:continue
 scores=[]
 for num,ts in D.items():
  seq=[x['pitch'] for x in ts[0]['events']]
  for sh in range(-24,25):
   m=difflib.SequenceMatcher(None,[p+sh for p in ps],seq,autojunk=False).find_longest_match();scores.append((m.size,int(num),sh,m.a,m.b,len(ps)))
 print(f.name,ps[:18],sorted(scores,reverse=True)[:2])
