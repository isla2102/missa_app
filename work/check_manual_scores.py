from pathlib import Path
from pypdf import PdfReader
import xml.etree.ElementTree as E,json,hashlib
for key,count in [('kyrie',72),('doxology',21),('alleluia-365',16)]:
 p=Path('output/pdf')/(key+'-reengraved.pdf');r=PdfReader(p);assert len(r.pages)==1;assert len(list(r.pages[0].images))==0
 t=r.pages[0].extract_text();assert '■' not in t and '교정 전' in t
 score=E.parse(Path('docs/교중미사악보/reengraved')/(key+'.musicxml'));assert len(score.findall('.//note/pitch'))==count
 if key=='kyrie':
  assert t.count('성가대')==3 and t.count('다 같이')==3
  assert len(score.findall('.//measure'))==24
  assert all(sum(int(n.findtext('duration')) for n in m.findall('note'))==36 for m in score.findall('.//measure'))
 assert p.read_bytes()==(Path('docs/교중미사악보/reengraved')/(key+'.pdf')).read_bytes()
cat=json.loads(Path('docs/references/score-source-catalog.json').read_text(encoding='utf-8'));assert cat['entryCount']==525
assert cat['scores']['복음 환호송']['confirmedNumber']==365
for key,entry in cat['scores'].items():
 if key!='복음 환호송':assert entry['confirmedNumber'] is None
 for c in entry['candidates']:
  p=Path('review')/c['path'];assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==c['sha256']
# First sixteen soprano notes of the official 365 MIDI match this refrain exactly.
s=Path('work/compare_reference_midi.py').read_text(encoding='utf-8');scope={};exec(s[:s.index('all_tracks=')],scope)
notes=scope['midi_tracks']('work/goodnews/365.mid')[0]['events'][:16];assert [n['pitch'] for n in notes]==[65,67,69,65,67,69,67,65,62,60,65,67,69,67,65,65]
print('PASS: three new single-page vector PDFs, Korean text and roles, 72+21+16 pitched notes, Kyrie measure totals, 365 official melody match, 525-entry archive catalog and extracted file hashes.')
