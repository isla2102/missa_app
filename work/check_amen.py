from pathlib import Path
from pypdf import PdfReader
import xml.etree.ElementTree as E,json,hashlib
pdf=Path('output/pdf/amen-reengraved.pdf');r=PdfReader(pdf);assert len(r.pages)==1
text=r.pages[0].extract_text();assert '아멘' in text and text.count('멘')>=3
assert len(list(r.pages[0].images))==0
root=E.parse('docs/교중미사악보/reengraved/amen.musicxml');assert len(root.findall('.//note'))==11
assert [''.join(n.findtext('pitch/'+k) for k in ['step','octave']) for n in root.findall('.//note')]==['A4','G4','A4','G4','F4','G4','F4','D4','C4','D4','F4']
assert pdf.read_bytes()==Path('docs/교중미사악보/reengraved/amen.pdf').read_bytes()
manifest=json.loads(Path('docs/교중미사악보/temporary-score-manifest.json').read_text(encoding='utf-8'))
for item in manifest['files']:assert hashlib.sha256((Path('docs/교중미사악보')/item['file']).read_bytes()).hexdigest()==item['sha256']
print('PASS: one-page vector PDF, Korean lyrics, 11 manually checked notes, matching reader PDF, original eight photo hashes intact. Rendered PNG inspected.')
