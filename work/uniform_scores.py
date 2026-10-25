from pathlib import Path
import sys,copy,io,json,re,xml.etree.ElementTree as E,shutil
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
base=Path('docs/교중미사악보/reengraved');src=base/'autofit-readable';dest=base/'uniform-a4';dest.mkdir(exist_ok=True)
NS='http://www.w3.org/2000/svg';tag=lambda s:'{'+NS+'}'+s
W,H=A4; margin=5*mm;gap=6*mm;target=12.5
meta=json.loads((src/'manifest.json').read_text(encoding='utf-8'))
def drawing(row):
 root=E.Element(tag('svg'),width='841.8897637795277',height='10000');root.append(copy.deepcopy(row));d=svg2rlg(io.BytesIO(E.tostring(root)))
 def fonts(n):
  if isinstance(n,String):n.fontName='Malgun'
  for child in getattr(n,'contents',[]):fonts(child)
 fonts(d);return d
for score in meta:
 key=score['key'];old=E.parse(src/(key+'.svg')).getroot();out=E.Element(old.tag,old.attrib);out[:]=[];sy=margin;c=canvas.Canvas(str(dest/(key+'.pdf')),pagesize=A4);c.setTitle(score['title']);c.setFont('Malgun',11);c.drawString(margin,H-margin-11,score['title']);y=H-margin-22;pages=1;count=0
 for original in old:
  row=copy.deepcopy(original);rawscale=float(re.search(r'scale\(([^)]+)\)',row.get('transform')).group(1));parents={child:parent for parent in row.iter() for child in parent};lyrics=[]
  for verse in row.iter():
   if verse.get('class')=='verse':lyrics.extend(verse.iter(tag('text')))
  d=drawing(row);x0,y0,x1,y1=d.getBounds();fit=(W-2*margin)/(x1-x0)
  for t in lyrics:t.set('font-size',str(target/(rawscale*.75*fit))+'px')
  # Compress only horizontal glyph width when a syllable group exceeds its note slot.
  baselines={}
  for t in lyrics:baselines.setdefault(t.get('y'),[]).append(t)
  for texts in baselines.values():
   texts.sort(key=lambda t:float(t.get('x')))
   for i,t in enumerate(texts):
    x=float(t.get('x'));size=float(t.get('font-size').removesuffix('px'));width=pdfmetrics.stringWidth(t.text or '', 'Malgun',size)
    slot=float(texts[i+1].get('x'))-x-35 if i+1<len(texts) else width
    ratio=min(1,max(.25,slot/width)) if width else 1
    if ratio<1:
     parent=parents[t];g=E.Element(tag('g'),transform=f'translate({x} 0) scale({ratio} 1) translate({-x} 0)');parent.insert(list(parent).index(t),g);parent.remove(t);g.append(t)
  d=drawing(row);x0,y0,x1,y1=d.getBounds();fit=(W-2*margin)/(x1-x0);height=(y1-y0)*fit
  if y-height<margin:c.showPage();pages+=1;y=H-margin
  c.saveState();c.translate(margin-x0*fit,y-y1*fit);c.scale(fit,fit);renderPDF.draw(d,c,0,0);c.restoreState();y-=height+gap
  # Preview uses exactly the same fixed-width rows and generous inter-system gap.
  g=E.SubElement(out,tag('g'),transform=f'translate({margin-x0*fit} {sy-(d.height-y1)*fit}) scale({fit*.75})');g.append(row);sy+=height+gap;count+=len(lyrics)
 c.showPage();c.save();out.set('width',str(W));out.set('height',str(sy-gap+margin));out.set('viewBox',f'0 0 {W} {sy-gap+margin}');E.ElementTree(out).write(dest/(key+'.svg'),encoding='utf-8',xml_declaration=True)
 score.update(printA4Pages=pages,printWidthMm=210,printHeightMm=297,lyricFontPt=target,systemGapMm=6,lyricCount=count)
 assert all(abs(float(p.mediabox.width)-W)<.01 and abs(float(p.mediabox.height)-H)<.01 for p in PdfReader(dest/(key+'.pdf')).pages)
 print(key,pages,count,flush=True)
(dest/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
writer=PdfWriter()
for score in meta:writer.append(str(dest/(score['key']+'.pdf')))
with Path('output/pdf/parish-scores-uniform-a4.pdf').open('wb') as f:writer.write(f)
rp=base/'registry.json';shutil.copy2(rp,'scratch/registry-before-v40.json');r=json.loads(rp.read_text(encoding='utf-8'))
for assets in r.values():
 for a in assets:
  key=Path(a['path']).stem;a['path']='../'+(dest/(key+'.pdf')).as_posix();a['preview']='../'+(dest/(key+'.svg')).as_posix()
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8',newline='\r\n')
s=Path('review/02-ia-v39.html').read_text(encoding='utf-8').replace('v39','v40');s=re.sub(r'const reengravedPrincipalScores = .*?;',lambda _:'const reengravedPrincipalScores = '+json.dumps(r,ensure_ascii=False)+';',s,count=1)
sizes={}
for p in base.rglob('*.svg'):
 root=E.parse(p).getroot();w=root.get('width','').removesuffix('px');h=root.get('height','').removesuffix('px')
 if w and h:sizes['../'+p.as_posix()]=[float(w),float(h)]
s=re.sub(r'const scorePreviewSizes=.*?;',lambda _:'const scorePreviewSizes='+json.dumps(sizes,ensure_ascii=False)+';',s,count=1)
Path('review/02-ia-v40.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v40-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
Path('work/test-reader-v40.cjs').write_text(Path('work/test-reader-v39.cjs').read_text(encoding='utf-8').replace('02-ia-v39.html','02-ia-v40.html'),encoding='utf-8')
