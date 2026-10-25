from pathlib import Path
from pypdf import PdfReader,PdfWriter,Transformation,PageObject
import json
base=Path('docs/교중미사악보/reengraved/autofit-large');manifest=json.loads((base/'manifest.json').read_text(encoding='utf-8'));W=297*72/25.4;H=210*72/25.4;gap=3*72/25.4
writer=PdfWriter();target=None;used=0
for entry in manifest:
 for page in PdfReader(base/(entry['key']+'.pdf')).pages:
  low=float(page.mediabox.bottom);h=float(page.mediabox.height)
  if target is None or used+h>H:
   if target is not None:
    target.mediabox.lower_left=(0,H-used);target.cropbox=target.mediabox;writer.add_page(target)
   target=PageObject.create_blank_page(width=W,height=H);used=0
  page.add_transformation(Transformation().translate(0,-low));page.mediabox.lower_left=(0,0);page.mediabox.upper_right=(W,h);page.cropbox=page.mediabox
  target.merge_transformed_page(page,Transformation().translate(0,H-used-h));used+=h+gap
if target is not None:target.mediabox.lower_left=(0,max(0,H-used));target.cropbox=target.mediabox;writer.add_page(target)
with Path('output/pdf/parish-scores-large.pdf').open('wb') as f:writer.write(f)
print('Bundle pages:',len(writer.pages))
