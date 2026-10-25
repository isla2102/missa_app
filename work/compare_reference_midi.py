import struct,json,xml.etree.ElementTree as E,difflib
from pathlib import Path

def vlq(b,i):
 v=0
 while True:
  x=b[i];i+=1;v=(v<<7)|(x&127)
  if not(x&128):return v,i

def midi_tracks(file):
 b=Path(file).read_bytes();length=int.from_bytes(b[4:8],'big');i=8+length;result=[]
 while i<len(b):
  kind=b[i:i+4];n=int.from_bytes(b[i+4:i+8],'big');chunk=b[i+8:i+8+n];i+=8+n
  if kind!=b'MTrk':continue
  j=0;t=0;status=0;events=[];name='';active={}
  while j<len(chunk):
   delta,j=vlq(chunk,j);t+=delta;x=chunk[j]
   if x&128:status=x;j+=1
   else:x=status
   if x==255:
    typ=chunk[j];j+=1;size,j=vlq(chunk,j);data=chunk[j:j+size];j+=size
    if typ==3:name=data.decode('utf-8',errors='replace')
    continue
   if x in [240,247]:size,j=vlq(chunk,j);j+=size;continue
   count=1 if (x&240) in [192,208] else 2;data=chunk[j:j+count];j+=count
   if x&240==144 and data[1]>0:events.append({'time':t,'pitch':data[0],'channel':x&15})
  if events:result.append({'name':name,'events':events})
 return result

def xmlpitch(key):
 r=E.parse('docs/교중미사악보/reengraved/'+key+'.musicxml');ns=r.findall('.//note');p=[]
 for n in ns:
  if n.find('tie[@type="stop"]') is not None:continue
  step=n.findtext('pitch/step');oct=int(n.findtext('pitch/octave'));p.append((oct+1)*12+{'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}[step]+int(n.findtext('pitch/alter','0')))
 return p
all_tracks={int(f.stem):midi_tracks(f) for f in Path('work/goodnews').glob('*.mid')}
Path('work/goodnews/midi-notes.json').write_text(json.dumps(all_tracks,ensure_ascii=False),encoding='utf-8')
for key in ['kyrie','doxology','amen']:
 q=xmlpitch(key);scores=[]
 for num,tracks in all_tracks.items():
  for ti,tr in enumerate(tracks):
   # MIDI accompaniment chords can be in one track: compare the highest note at each onset too.
   seq=[e['pitch'] for e in tr['events']];onsets={}
   for e in tr['events']:onsets[e['time']]=max(onsets.get(e['time'],0),e['pitch'])
   for mode,seq in [('all',seq),('top',list(onsets.values()))]:
    for shift in range(-12,13):
     target=[v+shift for v in q];match=difflib.SequenceMatcher(None,target,seq,autojunk=False).find_longest_match(0,len(q),0,len(seq))
     scores.append({'number':num,'track':ti,'name':tr['name'],'mode':mode,'shift':shift,'matched':match.size,'queryLength':len(q),'queryOffset':match.a,'referenceOffset':match.b,'first':seq[:24]})
 scores.sort(key=lambda s:(s['matched'],-abs(s['shift'])),reverse=True)
 Path('work/goodnews/'+key+'-matches.json').write_text(json.dumps(scores[:30],ensure_ascii=False,indent=2),encoding='utf-8')
 print(key,'query',q,'TOP',scores[:4])
