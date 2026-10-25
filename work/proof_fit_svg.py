from pathlib import Path
import sys,io
sys.path.insert(0,'work/music-deps')
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import String
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'))
p=Path('docs/교중미사악보/reengraved/autofit/gloria.svg');d=svg2rlg(str(p))
def font(n):
 if isinstance(n,String):n.fontName='Malgun'
 for c in getattr(n,'contents',[]):font(c)
font(d);c=canvas.Canvas('work/autofit-svg-proof.pdf',pagesize=(d.width,d.height));renderPDF.draw(d,c,0,0);c.showPage();c.save()
