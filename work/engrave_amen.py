from pathlib import Path
import sys,xml.etree.ElementTree as E,io,json,re
sys.path.insert(0,'work/music-deps')
import verovio
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
out=Path('output/pdf');out.mkdir(parents=True,exist_ok=True)
assets=Path('docs/교중미사악보/reengraved');assets.mkdir(parents=True,exist_ok=True)
work=Path('work/amen-engraving');work.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFontFamily('Malgun',normal='Malgun',bold='Malgun',italic='Malgun',boldItalic='Malgun')
r=E.Element('score-partwise',version='4.0');ident=E.SubElement(r,'identification');E.SubElement(ident,'creator',type='transcriber').text='Photo transcription'
pl=E.SubElement(r,'part-list');sp=E.SubElement(pl,'score-part',id='P1');E.SubElement(sp,'part-name').text=''
p=E.SubElement(r,'part',id='P1')
# Source has one flat, eleven notes, two six-quarter spans, three sung Amens.
notes=[('A',4,12,'quarter',False,'아'),('G',4,6,'eighth',False,''),('A',4,18,'quarter',True,'멘'),('G',4,12,'quarter',False,'아'),('F',4,6,'eighth',False,''),('G',4,18,'quarter',True,'멘'),('F',4,12,'quarter',False,'아'),('D',4,6,'eighth',False,''),('C',4,12,'quarter',False,''),('D',4,6,'eighth',False,''),('F',4,36,'half',True,'멘')]
for mi,items in enumerate([notes[:6],notes[6:]]):
 m=E.SubElement(p,'measure',number=str(mi+1))
 if mi==0:
  a=E.SubElement(m,'attributes');E.SubElement(a,'divisions').text='12';k=E.SubElement(a,'key');E.SubElement(k,'fifths').text='-1';t=E.SubElement(a,'time',{'print-object':'no'});E.SubElement(t,'beats').text='6';E.SubElement(t,'beat-type').text='4';c=E.SubElement(a,'clef');E.SubElement(c,'sign').text='G';E.SubElement(c,'line').text='2'
 for j,(step,octave,dur,typ,dot,lyric) in enumerate(items):
  index=j+(0 if mi==0 else 6);n=E.SubElement(m,'note');pitch=E.SubElement(n,'pitch');E.SubElement(pitch,'step').text=step;E.SubElement(pitch,'octave').text=str(octave);E.SubElement(n,'duration').text=str(dur);E.SubElement(n,'type').text=typ
  if dot:E.SubElement(n,'dot')
  E.SubElement(n,'stem').text='up'
  if index in [0,2,3,5,6,10]:
   notation=E.SubElement(n,'notations');E.SubElement(notation,'slur',type='start' if index in [0,3,6] else 'stop',number='1',placement='below')
  if lyric:
   l=E.SubElement(n,'lyric',{'font-family':'Malgun','font-size':'12'});E.SubElement(l,'syllabic').text='begin' if lyric=='아' else 'end';E.SubElement(l,'text').text=lyric
 if mi==1:E.SubElement(E.SubElement(m,'barline',location='right'),'bar-style').text='light-heavy'
xml=E.tostring(r,encoding='unicode',xml_declaration=True);(assets/'amen.musicxml').write_text(xml,encoding='utf-8')
verovio.setDefaultResourcePath('work/music-deps/verovio/data');tk=verovio.toolkit();tk.setOptions({'pageWidth':2100,'pageHeight':1000,'pageMarginTop':20,'pageMarginLeft':40,'pageMarginRight':40,'pageMarginBottom':20,'scale':50,'header':'none','footer':'none','breaks':'none','adjustPageHeight':True,'font':'Leipzig','lyricSize':5,'minLastJustification':0})
assert tk.loadData(xml);svg=tk.renderToSVG(1)
# Register Korean text in both vector preview and PDF; music glyphs remain path outlines.
svg=svg.replace('Times New Roman','Malgun').replace('font-family="Times"','font-family="Malgun"')
def flatten_text(m):
 content=''.join(E.fromstring(m.group(0)).itertext()).strip()
 return re.sub(r'font-size="0px"', 'font-size="450px" font-family="Malgun"',m.group(0).split('>')[0]+'>')+content+'</text>'
svg=re.sub(r'<text\b[^>]*>.*?</text>',flatten_text,svg,flags=re.S)
(assets/'amen.svg').write_text(svg,encoding='utf-8');drawing=svg2rlg(io.BytesIO(svg.encode('utf-8')))
W,H=595.276,300
pdf=canvas.Canvas(str(out/'amen-reengraved.pdf'),pagesize=(W,H));pdf.setTitle('아멘 · 교중미사 재조판');pdf.setAuthor('사용자 제공 사진에서 전사')
pdf.setFont('Malgun',21);pdf.drawString(28,H-40,'아멘')
pdf.setFont('Malgun',9);pdf.drawString(28,H-60,'교중미사 악보 · 사진에서 음표와 가사를 새로 조판')
scale=(W-56)/drawing.width;drawing.scale(scale,scale);renderPDF.draw(drawing,pdf,28,H-90-drawing.height*scale)
pdf.setFont('Malgun',8);pdf.drawString(28,24,'원본 사진 대조 · 본당 최종 교정 전 / 원본 표제 21 아멘')
pdf.showPage();pdf.save()
# Adjacent same-content PDF is the reader asset, output/pdf is the deliverable.
(assets/'amen.pdf').write_bytes((out/'amen-reengraved.pdf').read_bytes())
manifest={'title':'아멘','status':'manually-transcribed-photo-compared-parish-proofreading-pending','noteCount':len(notes),'measureDurations':[sum(n[2] for n in notes[:6]),sum(n[2] for n in notes[6:])],'pdf':'amen.pdf','preview':'amen.svg','editable':'amen.musicxml','sourcePrintedNumber':21}
(assets/'amen-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Created Amen PDF, vector SVG, editable MusicXML; 11 notes, 2 spans, 3 lyric pairs')
