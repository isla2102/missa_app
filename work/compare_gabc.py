import re,json,difflib
from pathlib import Path
qs={'Gloria':'DDDDDCDGFDCDD','Sanctus':'AAAAGAGGGGFG','Agnus':'AAGAGGAGFDC'}
def collapse(a):return [x for i,x in enumerate(a) if not i or x!=a[i-1]]
for kind,q in qs.items():
 q=collapse(['CDEFGAB'.index(x) for x in q]);out=[]
 for id,name in json.loads(Path('work/gregorian/list.json').read_text()):
  if not name.startswith(kind):continue
  s=(Path('work/gregorian')/(id+'.gabc')).read_text(encoding='utf-8',errors='replace').split('%%')[-1]
  groups=re.findall(r'\(([^()]*)\)',s);seq=[]
  for g in groups:
   if re.fullmatch(r'[cf]b?[1-4]',g):continue
   g=re.sub(r'\[[^]]*\]','',g)
   seq +=[ord(x.lower())-97 for x in re.findall('[a-mA-M]',g)]
  seq=collapse(seq);best=(0,0,0)
  for shift in range(-15,16):
   target=[x+shift for x in q];m=difflib.SequenceMatcher(None,target,seq[:50],autojunk=False).find_longest_match()
   if m.size>best[0]:best=(m.size,m.a,m.b)
  out.append((best,id,name,seq[:18]))
 print(kind,'QUERY',q,'BEST',sorted(out,reverse=True)[:6])
