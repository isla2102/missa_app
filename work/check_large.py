from pathlib import Path
import xml.etree.ElementTree as E,json
base=Path('docs/교중미사악보/reengraved');small=json.loads((base/'autofit/manifest.json').read_text(encoding='utf-8'));large=json.loads((base/'autofit-large/manifest.json').read_text(encoding='utf-8'))
for a,b in zip(small,large):
 assert a['key']==b['key'] and a['systems']==b['systems']
 ra=E.parse(base/'autofit'/(a['key']+'.musicxml')).getroot();rb=E.parse(base/'autofit-large'/(a['key']+'.musicxml')).getroot();assert E.tostring(ra)==E.tostring(rb)
print('PASS: 11 scores retain identical MusicXML, system counts, and exact line breaks.')
