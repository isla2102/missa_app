from pathlib import Path
import sys,io,xml.etree.ElementTree as E
sys.path.insert(0,'work/music-deps')
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import String
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'))
for key in ['gloria','lords-prayer']:
 p=Path('docs/교중미사악보/reengraved')/(key+'-v26.svg');root=E.parse(p).getroot();ids=[n.get('id') for n in root.iter() if n.get('id')];assert len(ids)==len(set(ids));assert len(list(root))==(4 if key=='gloria' else 2)
 drawing=svg2rlg(str(p))
 def fonts(node):
  if isinstance(node,String):node.fontName='Malgun'
  for child in getattr(node,'contents',[]):fonts(child)
 fonts(drawing);scale=0.55;drawing.scale(scale,scale);c=canvas.Canvas('work/music-manual/'+key+'-v26-continuous-proof.pdf',pagesize=(drawing.width*scale,drawing.height*scale));renderPDF.draw(drawing,c,0,0);c.showPage();c.save()
print('Continuous SVGs: unique IDs, correct page groups, rendered vector proof PDFs.')
