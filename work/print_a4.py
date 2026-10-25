from pathlib import Path
import sys,copy,io,json,xml.etree.ElementTree as E
sys.path.insert(0,'work/music-deps')
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import String
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from pypdf import PdfWriter,PdfReader
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'))
base=Path('docs/교중미사악보/reengraved');source=base/'autofit-readable';dest=base/'print-a4';dest.mkdir(exist_ok=True);meta=json.loads((source/'manifest.json').read_text(encoding='utf-8'));W,H=A4;margin=5*mm;gap=2*mm
for score in meta:
 key=score['key'];root=E.parse(source/(key+'.svg')).getroot();c=canvas.Canvas(str(dest/(key+'.pdf')),pagesize=A4);c.setTitle(score['title']);c.setFont('Malgun',11);c.drawString(margin,H-margin-11,score['title']);y=H-margin-20;pagecount=1
 for row in root:
  sub=copy.deepcopy(root);sub[:]=[copy.deepcopy(row)];d=svg2rlg(io.BytesIO(E.tostring(sub)))
  def fonts(n):
   if isinstance(n,String):n.fontName='Malgun'
   for child in getattr(n,'contents',[]):fonts(child)
  fonts(d);x0,y0,x1,y1=d.getBounds();scale=(W-margin*2)/(x1-x0);height=(y1-y0)*scale
  if y-height<margin:c.showPage();pagecount+=1;y=H-margin
  c.saveState();c.translate(margin-x0*scale,y-y1*scale);c.scale(scale,scale);renderPDF.draw(d,c,0,0);c.restoreState();y-=height+gap
 c.showPage();c.save();score['printA4Pages']=pagecount;score['printWidthMm']=210;score['printHeightMm']=297;print(key,pagecount,flush=True)
 for page in PdfReader(dest/(key+'.pdf')).pages:assert abs(float(page.mediabox.width)-W)<.01 and abs(float(page.mediabox.height)-H)<.01
assert next(x for x in meta if x['key']=='kyrie')['printA4Pages']==1
writer=PdfWriter()
for score in meta:writer.append(str(dest/(score['key']+'.pdf')))
with Path('output/pdf/parish-scores-a4.pdf').open('wb') as f:writer.write(f)
(dest/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8');print('PASS true portrait A4, Kyrie one page.')
