from pathlib import Path
s=Path('work/engrave_manual_scores.py').read_text(encoding='utf-8').split('# Kyrie -')[0]
s=s.replace("6:('eighth',False)","3:('16th',False),9:('eighth',True),6:('eighth',False)")
s=s.replace("if si==len(systems)-1 and mi==len(measures)-1:","if key=='gloria-d' and si==len(systems)-1 and mi==len(measures)-1:")
s=s.replace("xml=E.tostring(r,", "postprocess(r,key)\n xml=E.tostring(r,")
def postprocess(root,key):
 for n in root.findall('.//pitch'):
  if n.findtext('step')=='B':
   alter=E.Element('alter');alter.text='-1';n.insert(1,alter)
 for number,data in changes.get(key,{}).items():
  measure=root.find('.//part/measure[@number="'+str(number)+'"]');kind=data.get('meter')
  if kind:
   a=E.Element('attributes');t=E.SubElement(a,'time');E.SubElement(t,'beats').text=str(kind[0]);E.SubElement(t,'beat-type').text=str(kind[1]);measure.insert(0,a)
  if data.get('words'):
   di=E.Element('direction',placement='above');measure.insert(list(measure).index(measure.find('note')),di);dt=E.SubElement(di,'direction-type');E.SubElement(dt,'words',{'font-family':'Malgun'}).text=data['words']
changes={}
exec(compile(s,'builder','exec'))
def m(ps,ds,ls):
 p=ps.split();d=list(map(int,ds.split()));l=ls.split('|');assert len(p)==len(d)==len(l),(ps,ds,ls);return [note(x,y,z) for x,y,z in zip(p,d,l)]
def t(ns,i=0,j=1):ns[i]['tie']='start';ns[j]['tie']='stop';return ns
def hold(p,d,ly):return t(m(p+' '+p,str(d)+' '+str(d),ly+'|'))
p=[]
p.append([m('D4 D4 D4 D4','6 6 6 6','하|늘|높|은'),m('D4 C4 D4','6 6 12','데|서|는'),m('G4 F4 D4 C4','6 6 6 6','하|느|님|께'),m('D4 D4','12 12','영|광'),m('D4','24','')])
t(p[0][3]+p[0][4],1,2)
p.append([m('D4 D4 D4 D4','6 6 6 6','땅|에|서|는'),m('G4 F4 D4 D4','6 6 6 6','주|님|께|서'),m('F4 F4 F4 F4 F4','6 6 3 3 6','사|랑|하|시|는')])
p.append([m('G4 G4 G4 G4 G4','6 6 3 3 6','사|람|들|에|게'),m('A4 A4','18 18','평|화'),m('A4 G4 A4 F4','18 9 3 6','주|하||느')])
p.append([hold('D4',18,'님'),m('F4 F4 F4 G4 G4','6 6 6 12 6','하|늘|의|임|금'),hold('A4',18,'님'),m('A4 A4 A4 A4','6 6 6 18','전|능|하|신')])
p.append([m('G4 A4 D4','12 6 18','아|버|지'),m('F4 G4','18 18','하|느'),hold('A4',18,'님'),m('C5 C5 C5 D5 D5','6 6 6 12 6','주|님|을|기|리')])
p.append([m('C5 D5 C5 A4','6 6 6 18','나||이|다'),m('G4 A4 A4 F4 G4 F4','6 6 6 6 6 6','찬||미|하|나|이'),hold('D4',18,'다'),m('C5 C5 C5 D5 D5','6 6 6 12 6','주|님|을|흠|숭')])
changes['gloria-a']={10:{'meter':(6,8),'words':'점4분음표 = 60'},11:{'words':'성가대'},15:{'words':'다 같이'},19:{'words':'성가대'},23:{'words':'다 같이'}}
build('gloria-a','대영광송 · 1',p,['사제','다 같이 · 4분음표 = 104','','','',''],(2,4))
p=[]
p.append([m('C5 D5 C5 A4','6 6 6 18','하|나|이|다'),m('G4 A4 A4 F4 G4 F4','6 6 6 6 6 6','찬||양|하|나|이'),hold('D4',18,'다'),m('F4 F4 G4 G4','12 6 12 6','주|님|영|광')])
p.append([m('A4 A4 G4 A4','6 6 6 18','크|시|오|니'),m('C5 C5 C5 D5 C5','12 6 6 6 6','감|사|하|나|이'),hold('A4',18,'다'),m('A4 G4 F4 D4','18 9 3 6','외|아||들')])
p.append([m('C4 D4 D4 D4','9 3 6 18','주||예|수'),m('F4 G4 A4','18 12 6','그리|스도|'),hold('A4',18,'님'),m('A4 C5 A4 G4','18 6 6 6','주|하||느')])
p.append([hold('A4',18,'님'),m('G4 G4 G4 F4 G4','6 6 6 12 6','성|부|의|아|드'),hold('E4',18,'님'),m('F4 F4 F4 F4','6 6 6 18','하|느|님|의')])
p.append([m('E4 C4','18 18','어|린'),hold('D4',18,'양'),m('A4 G4 A4 G4 F4','12 6 6 6 6','세|상|의|죄|'),m('D4','36','를')]);p[4][1][-1]['fermata']=True
p.append([m('F4 F4 E4 F4 E4 D4','6 6 6 6 6 6','없|애|시|는|주|'),m('D4','36','님'),m('C4 D4 D4 D4','6 6 12 12','저|희|에|게'),m('F4 F4 E4','12 12 12','자|비|를')])
changes['gloria-b']={4:{'words':'성가대'},8:{'words':'다 같이'},12:{'words':'성가대'},16:{'words':'다 같이'},19:{'meter':(3,4),'words':'성가대 · Espressivo · p · 4분음표 = 84'}}
build('gloria-b','대영광송 · 2',p,['','','','','',''],(6,8))
p=[]
p.append([m('D4 C4 D4','12 12 12','베|푸|소'),m('D4','36','서'),m('A4 G4 A4 G4 F4','12 6 6 6 6','세|상|의|죄|'),m('D4','36','를')])
p.append([m('F4 F4 E4 F4 E4 D4','6 6 6 6 6 6','없|애|시|는|주|'),m('D4','36','님'),m('C4 D4 D4 D4','6 6 12 12','저||희|의'),m('F4 F4 E4','12 12 12','기|도|를')])
p.append([m('D4 C4 D4 D4','12 12 6 6','들|어|주|소'),m('D4','36','서'),m('A4 A4 G4 A4 G4 F4','6 6 6 6 6 6','성|부|오|른|편|'),m('D4','36','에')])
p.append([m('F4 F4 E4 F4 E4 D4','6 6 6 6 6 6','앉|아|계|신|주|'),m('D4','36','님'),m('C4 D4 D4 D4','6 6 12 12','저|희|에|게'),m('F4 F4 E4','12 12 12','자|비|를')])
p.append([m('D4 C4 D4','12 12 12','베|푸|소'),m('D4','36','서'),m('A4 A4 G4 A4','6 6 6 6','홀|로|거|룩'),m('G4 F4 D4','6 6 12','하|시|고')])
p.append([m('G4 G4 F4 G4','6 6 6 6','홀|로|주|님'),m('A4 A4 A4','6 6 12','이|시|며'),m('G4 G4 C5 G4','6 6 6 6','홀|로|높|으'),m('G4','24','신')])
changes['gloria-c']={3:{'words':'다 같이 · mf'},11:{'words':'성가대 · f'},19:{'meter':(2,4),'words':'다 같이 · 4분음표 = 96'}}
build('gloria-c','대영광송 · 3',p,['','','','','',''],(3,4))
p=[]
p.append([m('G4 G4','12 12','예|수'),m('F4 G4','12 12','그리|스도'),m('A4','24','님'),m('A4','24','')]);p[0][2][0]['tie']='start';p[0][3][0]['tie']='stop'
p.append([m('D4 D4 D4 C4','6 6 6 6','성|령|과|함'),m('D4','24','께'),m('F4 F4 F4','6 6 12','아|버|지'),m('G4 G4 F4 G4','6 6 6 6','하|느|님|의')])
p.append([m('A4 A4 C5','6 12 6','영|광|안'),m('A4','24','에'),m('G4 G4','12 12','계|시'),m('F4 G4','12 12','나|이')])
p.append([m('A4','24','다'),m('C4 B3','12 12','아|'),m('C4','24','멘'),m('F4 E4','12 12','아|')])
p.append([m('F4','24','멘'),m('G4','24','아'),m('A4','24',''),m('A4','24','멘'),m('A4','24','')]);p[4][3][0]['tie']='start';p[4][4][0]['tie']='stop'
build('gloria-d','대영광송 · 4',p,['','','','',''],(2,4))
from pypdf import PdfWriter
w=PdfWriter()
for key in ['gloria-a','gloria-b','gloria-c','gloria-d']:w.append(str(out/(key+'-reengraved.pdf')))
with (out/'gloria-reengraved.pdf').open('wb') as f:w.write(f)
