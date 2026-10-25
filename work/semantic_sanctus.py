from pathlib import Path
import sys,re,io,json,copy,xml.etree.ElementTree as E
sys.path.insert(0,'work/music-deps')
import verovio
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import String
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.units import mm
verovio.setDefaultResourcePath('work/music-deps/verovio/data');pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'))
base=Path('docs/교중미사악보/reengraved');dest=base/'semantic-source';dest.mkdir(exist_ok=True)
NS='http://www.w3.org/2000/svg';tag=lambda x:'{'+NS+'}'+x
jobs=[('gloria','대영광송',['gloria-a','gloria-b','gloria-c','gloria-d']),('lords-prayer','주님의 기도',['lords-a','lords-b'])]+[(k,t,[k]) for k,t in [('amen','아멘'),('kyrie','자비송'),('doxology','주님의 기도 맺음 환호'),('alleluia-365','복음 환호송'),('agnus','하느님의 어린양'),('sanctus','거룩하시도다'),('memorial-ordinary','신앙의 신비여 · 연중'),('memorial-lent','신앙의 신비여 · 사순'),('memorial-easter','신앙의 신비여 · 부활')]]
jobs=[job for job in jobs if job[0]=='sanctus']
results=[]
for key,title,keys in jobs:
 root=E.parse(base/(keys[0]+'.musicxml')).getroot();part=root.find('part');original=sum(len(E.parse(base/(k+'.musicxml')).getroot().findall('.//note')) for k in keys)
 for k in keys[1:]:
  for j,m in enumerate(E.parse(base/(k+'.musicxml')).getroot().findall('.//part/measure')):
   m=copy.deepcopy(m)
   if j==0:
    for a in list(m.findall('attributes')):m.remove(a)
   part.append(m)
 role='';count=0;systems=0
 for i,m in enumerate(part.findall('measure')):
  m.set('number',str(i+1))
  for p in list(m.findall('print')):m.remove(p)
  found=None
  for words in m.findall('.//words'):
   text=words.text or ''
   if '사제' in text:found='사제 선창'
   elif '성가대' in text:found='성가대'
   elif '다 같이' in text or '합송' in text:found='합송'
   if found:words.text=text.replace('다 같이','합송').replace('사제 선창 · 합송','사제 선창');words.text=re.sub(r'^사제(?! 선창)', '사제 선창',words.text)
  if key.startswith('memorial-') and i==1:found='합송';d=E.Element('direction',placement='above');dt=E.SubElement(d,'direction-type');E.SubElement(dt,'words').text=found;m.insert(0,d)
  if i==0 and not found:found='합송';d=E.Element('direction',placement='above');dt=E.SubElement(d,'direction-type');E.SubElement(dt,'words').text=found;m.insert(0,d)
  notes=len(m.findall('note'));new=i in {0,4,6,8,10,13}
  if new:
   if i:m.insert(0,E.Element('print',{'new-system':'yes'}))
   systems+=1;count=0
   if not found and role:d=E.Element('direction',placement='above');dt=E.SubElement(d,'direction-type');E.SubElement(dt,'words').text=role;m.insert(1,d)
  if found:role=found
  count+=notes
 assert len(root.findall('.//note'))==original
 xml=E.tostring(root,encoding='unicode');(dest/(key+'.musicxml')).write_text(xml,encoding='utf-8')
 tk=verovio.toolkit();tk.setOptions({'pageWidth':1500,'pageHeight':60000,'pageMarginLeft':20,'pageMarginRight':20,'pageMarginTop':20,'pageMarginBottom':20,'scale':50,'header':'none','footer':'none','breaks':'encoded','adjustPageHeight':True,'font':'Leipzig','lyricSize':4.5,'lyricTopMinMargin':8,'spacingSystem':4,'minLastJustification':0});assert tk.loadData(xml)
 svg=tk.renderToSVG(1).replace('Times New Roman','Malgun').replace('Times, serif','Malgun')
 def flat(m):
  opening=m.group(0).split('>')[0]+'>';opening=re.sub(r'font-size="0px"','font-size="405px" font-family="Malgun"',opening);text=''.join(E.fromstring(m.group(0)).itertext()).strip();opening=opening.replace('font-size="405px"','font-size="355px"') if len(text)>=5 and not any(role in text for role in ['합송','성가대','선창','음표','tempo','rit','Espressivo','천천히']) else opening;return opening+text+'</text>'
 svg=re.sub(r'<text\b[^>]*>.*?</text>',flat,svg,flags=re.S);tree=E.fromstring(svg);ids={n.get('id'):n for n in tree.iter() if n.get('id')}
 for parent in list(tree.iter()):
  for n in list(parent):
   if n.tag==tag('use'):
    g=E.Element(tag('g'),transform=n.get('transform',''));target=copy.deepcopy(ids[n.get('{http://www.w3.org/1999/xlink}href').lstrip('#')]);g.append(target);parent.insert(list(parent).index(n),g);parent.remove(n)
 for n in tree.iter():
  if n.tag.split('}')[-1] in ['path','ellipse','polygon','polyline','rect']:n.set('stroke','black')
 # Fit each lyric to its existing horizontal slot without changing line breaks.
 for system in tree.iter():
  if system.get('class')!='system':continue
  baselines={}
  for text in system.iter(tag('text')):
   if text.text and text.get('x') is not None:baselines.setdefault(text.get('y'),[]).append(text)
  for texts in baselines.values():
   texts.sort(key=lambda n:float(n.get('x')))
   for text,nexttext in zip(texts,texts[1:]):
    size=float(text.get('font-size','405px').removesuffix('px'));slot=float(nexttext.get('x'))-float(text.get('x'))-35
    width=pdfmetrics.stringWidth(text.text,'Malgun',1)
    if slot>0 and width>0:text.set('font-size',str(min(size,slot/width))+'px')
 rows=[]
 for system in tree.iter():
  if system.get('class')!='system':continue
  sub=E.Element(tag('svg'),width='29700',height='600000');sub.append(copy.deepcopy(system));drawing=svg2rlg(io.BytesIO(E.tostring(sub)))
  def fonts(n):
   if isinstance(n,String):n.fontName='Malgun'
   for c in getattr(n,'contents',[]):fonts(c)
  fonts(drawing);bounds=drawing.getBounds();rows.append((drawing,bounds,system))
 assert len(rows)==systems,(key,len(rows),systems)
 W,H=landscape(A4);margin=3*mm;usable=W-2*margin;gap=2*mm;c=canvas.Canvas(str(dest/(key+'.pdf')),pagesize=(W,H));c.setTitle(title);y=H-margin;pages=1
 c.setFont('Malgun',11);c.drawString(margin,y-11,title);y-=19
 merged=E.Element(tag('svg'),width=str(W),height='1',viewBox='0 0 '+str(W)+' 1');sy=0
 for drawing,(x0,y0,x1,y1),system in rows:
  scale=usable/(x1-x0);height=(y1-y0)*scale
  if y-height<margin:c.showPage();pages+=1;y=H-margin
  c.saveState();c.translate(margin-x0*scale,y-y1*scale);c.scale(scale,scale);renderPDF.draw(drawing,c,0,0);c.restoreState();y-=height+gap
  # SVG coordinates are y-down; reportlab bounds use bottom-up canvas coordinates.
  raw=copy.deepcopy(system)
  for element in raw.iter():element.attrib.pop('id',None)
  g=E.SubElement(merged,tag('g'),transform=f'translate({margin-x0*scale} {sy-(drawing.height-y1)*scale}) scale({scale*drawing.width/29700})');g.append(raw);sy+=height+gap
 c.showPage();c.save()
 from pypdf import PdfReader,PdfWriter
 pdf=PdfReader(dest/(key+'.pdf'));last=pdf.pages[-1];last.mediabox.lower_left=(0,max(0,y+gap-margin));last.cropbox=last.mediabox;writer=PdfWriter()
 for page in pdf.pages:writer.add_page(page)
 with (dest/(key+'.pdf')).open('wb') as f:writer.write(f)
 merged.set('height',str(sy-gap));merged.set('viewBox',f'0 0 {W} {sy-gap}');E.ElementTree(merged).write(dest/(key+'.svg'),encoding='utf-8',xml_declaration=True)
 results.append({'key':key,'title':title,'notes':original,'systems':len(rows),'pages':pages,'widthMm':297,'heightMm':210});print(results[-1],flush=True)
(dest/'manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')


