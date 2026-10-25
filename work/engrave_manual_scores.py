from pathlib import Path
import sys,io,re,json,xml.etree.ElementTree as E
sys.path.insert(0,'work/music-deps')
import verovio
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import String
from svglib.svglib import svg2rlg
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'));pdfmetrics.registerFontFamily('Malgun',normal='Malgun',bold='Malgun',italic='Malgun',boldItalic='Malgun')
verovio.setDefaultResourcePath('work/music-deps/verovio/data')
assets=Path('docs/교중미사악보/reengraved');out=Path('output/pdf');proof=Path('work/music-manual');proof.mkdir(exist_ok=True)
def note(p,d,lyric='',**kw):return dict(p=p,d=d,lyric=lyric,**kw)
def build(key,title,systems,roles,meter=None,tempo=None):
 r=E.Element('score-partwise',version='4.0');ident=E.SubElement(r,'identification');E.SubElement(ident,'creator',type='transcriber').text='Photo transcription'
 pl=E.SubElement(r,'part-list');sp=E.SubElement(pl,'score-part',id='P1');E.SubElement(sp,'part-name').text='';part=E.SubElement(r,'part',id='P1');num=0
 for si,measures in enumerate(systems):
  for mi,notes in enumerate(measures):
   num+=1;m=E.SubElement(part,'measure',number=str(num));
   if si and mi==0:E.SubElement(m,'print',{'new-system':'yes'})
   if num==1:
    a=E.SubElement(m,'attributes');E.SubElement(a,'divisions').text='12';k=E.SubElement(a,'key');E.SubElement(k,'fifths').text='-1'
    t=E.SubElement(a,'time',{} if meter else {'print-object':'no'})
    if meter:E.SubElement(t,'beats').text=str(meter[0]);E.SubElement(t,'beat-type').text=str(meter[1])
    else:E.SubElement(t,'senza-misura')
    c=E.SubElement(a,'clef');E.SubElement(c,'sign').text='G';E.SubElement(c,'line').text='2'
   if mi==0:
    direction=E.SubElement(m,'direction',placement='above');dt=E.SubElement(direction,'direction-type');E.SubElement(dt,'words',{'font-family':'Malgun'}).text=roles[si]
    if num==1 and tempo:E.SubElement(direction,'sound',tempo=str(tempo))
   for ni,info in enumerate(notes):
    n=E.SubElement(m,'note')
    if info['p'] is None:E.SubElement(n,'rest')
    else:
     pit=E.SubElement(n,'pitch');E.SubElement(pit,'step').text=info['p'][0];E.SubElement(pit,'octave').text=info['p'][1:]
    E.SubElement(n,'duration').text=str(info['d'])
    types={4:('eighth',False),6:('eighth',False),12:('quarter',False),18:('quarter',True),24:('half',False),36:('half',True)};typ,dot=types[info['d']];E.SubElement(n,'type').text=typ
    if dot:E.SubElement(n,'dot')
    if info.get('triplet'):
     tm=E.SubElement(n,'time-modification');E.SubElement(tm,'actual-notes').text='3';E.SubElement(tm,'normal-notes').text='2'
    if info.get('beam'):E.SubElement(n,'beam',number='1').text=info['beam']
    if info.get('tie'):E.SubElement(n,'tie',type=info['tie'])
    if info.get('tie') or info.get('slur') or info.get('tuplet') or info.get('fermata'):
     nt=E.SubElement(n,'notations')
     if info.get('fermata'):E.SubElement(nt,'fermata').text='normal'
     if info.get('tie'):E.SubElement(nt,'tied',type=info['tie'])
     if info.get('slur'):E.SubElement(nt,'slur',type=info['slur'],number='1',placement='below')
     if info.get('tuplet'):E.SubElement(nt,'tuplet',type=info['tuplet'],number='1',bracket='yes')
    if info['lyric']:
     ly=E.SubElement(n,'lyric',{'font-family':'Malgun'});E.SubElement(ly,'syllabic').text='single';E.SubElement(ly,'text').text=info['lyric']
   if si==len(systems)-1 and mi==len(measures)-1:E.SubElement(E.SubElement(m,'barline',location='right'),'bar-style').text='light-heavy'
 xml=E.tostring(r,encoding='unicode',xml_declaration=True);(assets/f'{key}.musicxml').write_text(xml,encoding='utf-8')
 tk=verovio.toolkit();tk.setOptions({'pageWidth':2100,'pageHeight':2970,'pageMarginLeft':40,'pageMarginRight':40,'pageMarginTop':20,'pageMarginBottom':20,'scale':50,'header':'none','footer':'none','breaks':'encoded','adjustPageHeight':True,'font':'Leipzig','lyricSize':4.5,'lyricTopMinMargin':6,'spacingSystem':10,'minLastJustification':0})
 assert tk.loadData(xml);assert tk.getPageCount()==1
 svg=tk.renderToSVG(1).replace('Times New Roman','Malgun').replace('Times, serif','Malgun')
 def flatten(m):
  text=''.join(E.fromstring(m.group(0)).itertext()).strip();opening=m.group(0).split('>')[0]+'>'
  opening=re.sub(r'font-size="0px"','font-size="405px" font-family="Malgun"',opening)
  return opening+text+'</text>'
 svg=re.sub(r'<text\b[^>]*>.*?</text>',flatten,svg,flags=re.S);(assets/f'{key}.svg').write_text(svg,encoding='utf-8')
 drawing=svg2rlg(io.BytesIO(svg.encode('utf-8')))
 def korean_fonts(node):
  if isinstance(node,String):node.fontName='Malgun'
  for child in getattr(node,'contents',[]):korean_fonts(child)
 korean_fonts(drawing)
 W=595.276;H=841.89 if len(systems)>2 else 300 if len(systems)==1 else 460
 c=canvas.Canvas(str(out/f'{key}-reengraved.pdf'),pagesize=(W,H));c.setTitle(title+' · 교중미사 재조판');c.setFont('Malgun',20);c.drawString(28,H-38,title);c.setFont('Malgun',9);c.drawString(28,H-58,'교중미사 악보 · 사진에서 음표·리듬·가사를 전사')
 scale=min((W-56)/drawing.width,(H-120)/drawing.height);drawing.scale(scale,scale);renderPDF.draw(drawing,c,28,H-82-drawing.height*scale)
 c.setFont('Malgun',8);c.drawString(28,24,'사진 원본 대조 · 본당 최종 교정 전');c.showPage();c.save();(assets/f'{key}.pdf').write_bytes((out/f'{key}-reengraved.pdf').read_bytes())
 meta={'title':title,'noteCount':sum(len(m) for sy in systems for m in sy),'systems':len(systems),'measureTicks':[[sum(n['d'] for n in m) for m in sy] for sy in systems],'status':'manually-transcribed-photo-compared-parish-proofreading-pending'};(assets/f'{key}-manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8');print(key,meta)
 return {'kind':'engraved','title':title,'path':f'../docs/교중미사악보/reengraved/{key}.pdf','preview':f'../docs/교중미사악보/reengraved/{key}.svg','status':'写真'}
# Kyrie - six original systems, four 3/4 measures each.
systems=[]
for row in range(6):
 first=['A4','A4','A4'] if row in [0,2,4] else ['D4' if row==1 else 'A4','D4','D4','F4']
 dur=[6,6,24] if len(first)==3 else [6,6,12,12]
 m1=[note(p,d) for p,d in zip(first,dur)]
 if row in [0,4]:m1[1]['tie']='start';m1[2]['tie']='stop'
 elif row in [1,5]:m1[1]['tie']='start';m1[2]['tie']='stop'
 if row in [1,3,5]:m1[2]['slur']='start';m1[3]['slur']='stop'
 if row in [0,4]:
  m2=[note(p,d,triplet=i<3) for i,(p,d) in enumerate(zip(['G4','F4','G4','D4'],[4,4,4,24]))];m2[0]['tuplet']='start';m2[2]['tuplet']='stop';m2[0]['beam']='begin';m2[1]['beam']='end'
 else:
  m2=[note(p,d) for p,d in zip(['C5','A4','A4','A4'] if row==2 else ['G4','A4','A4','G4'],[6,6,12,12])];m2[0]['beam']='begin';m2[1]['beam']='end'
 if row in [0,4]:ps=['F4','D4','C4','D4'] if row==0 else ['F4','D4','F4','G4'];ds=[12,12,6,6]
 elif row==2:ps=['D5','A4','G4','A4'];ds=[12,12,6,6]
 else:ps=['F4','A3','D4'];ds=[12,12,12]
 m3=[note(p,d) for p,d in zip(ps,ds)]
 if len(ps)==4:m3[2]['beam']='begin';m3[3]['beam']='end'
 m4=[note('A3' if row==0 else 'A4' if row==2 else 'G4' if row==4 else 'D4',36)]
 flat=m1+m2+m3+m4
 lyrics=(['그리','스도','님'] if row==2 else ['주','님',''])+['자','','비','를','베','푸','소','','서'] if len(first)==3 else (['그리','스도','님',''] if row==3 else ['주','님','',''])+['자','','비','를','베','푸','소','서']
 assert len(flat)==len(lyrics)==12
 for n,ly in zip(flat,lyrics):n['lyric']=ly
 systems.append([m1,m2,m3,m4])
build('kyrie','자비송',systems,['성가대','다 같이','성가대','다 같이','성가대','다 같이'],(3,4),60)
# Doxology - unmeasured original, two systems. Tied dotted quarters carry one syllable.
upper=[note(p,6,ly) for p,ly in zip(['A4','C5','C5','C5','A4','C5','D5','D5','D5'],['주','님','께','나','라','와','권','능','과'])]
for i in [0,3,6]:upper[i]['beam']='begin';upper[i+1]['beam']='continue';upper[i+2]['beam']='end'
upper += [note('C5',12,'영'),note('D5',6,'광'),note('A4',18,'이',tie='start'),note('A4',18,tie='stop')]
lower=[note('G4',12,'영'),note('A4',6,'원'),note('C5',18,'히',tie='start'),note('C5',18,tie='stop'),note('C4',12,'있'),note('D4',6,'나'),note('F4',18,'이'),note('F4',36,'다')]
build('doxology','주님의 기도 맺음 환호',[[upper],[lower]],['',''])

