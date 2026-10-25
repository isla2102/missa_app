from pathlib import Path
s=Path('work/engrave_manual_scores.py').read_text(encoding='utf-8').split('# Kyrie -')[0]
s=s.replace("if num==1 and tempo:E.SubElement(direction,'sound',tempo=str(tempo))", "if num==1 and tempo:E.SubElement(dt,'words').text='점4분음표 = '+str(tempo);E.SubElement(direction,'sound',tempo=str(tempo*1.5))")
s=s.replace("if si==len(systems)-1 and mi==len(measures)-1:","if key!='lords-a' and si==len(systems)-1 and mi==len(measures)-1:")
exec(compile(s,'builder','exec'))
def measure(pitches,durations,lyrics):
 ns=[note(p,int(d),ly) for p,d,ly in zip(pitches.split(),durations.split(),lyrics.split('|'))];assert len(ns)==len(pitches.split())==len(durations.split())==len(lyrics.split('|'));assert sum(n['d'] for n in ns)==72;return ns
def row(p,d,l,p2,d2,l2):return [measure(p,d,l),measure(p2,d2,l2)]
a=[]
a.append(row('A4 G4 A4 G4 F4','18 12 6 18 18','하|늘|에|계|신','D4 C4 D4 F4 F4 F4','12 6 12 6 18 18','우|리|아|버|지|'))
a[0][1][-2]['tie']='start';a[0][1][-1]['tie']='stop'
a.append(row('G4 G4 G4 G4 G4 F4 G4','12 6 12 6 12 6 18','아|버|지|의|이|름|이','A4 A4 G4 A4 C5 A4 G4','18 12 6 12 6 12 6','거|룩|히|빛|나|시|'))
a.append(row('G4 A4 A4 A4 A4 D5 C5','18 12 6 12 6 12 6','며|아|버|지|의|나|라','A4 G4 A4 F4 D4 G4','18 12 6 12 6 18','가|오||시||며'))
a[2][0][0].update(fermata=True,slur='start');a[2][0][1]['slur']='stop';a[2][1][-1]['fermata']=True
# Carry the syllable 시 from previous row to 며 using the source's melisma.
a.append(row('A4 A4 A4 G4 A4 C5 A4','12 6 12 6 12 6 18','아|버|지|의|뜻||이','G4 F4 G4 A4 G4 F4 D4','12 6 12 6 12 6 18','하|늘|에|서|와|같|이'))
a.append(row('C4 D4 F4 G4 A4 C5 A4','12 6 12 6 12 6 18','땅|에|서|도|이|루|어','G4 A4 G4 F4 F4 F4','12 6 12 6 18 18','지||소||서|'))
a[4][1][-2]['tie']='start';a[4][1][-1]['tie']='stop'
a.append(row('A4 A4 G4 A4 F4 D4','18 18 6 6 6 18','오|늘|저|희|에|게','G4 G4 G4 G4 A4 G4 F4 G4 A4','6 6 6 6 6 6 12 6 18','일|용|할|양|식|을|주|시|고'))
b=[]
b.append(row('C5 C5 C5 C5 C5 D5 C5 A4 A4','6 6 6 18 6 6 6 12 6','저|희|에|게|잘|못|한|이|를','G4 A4 A4 C5 A4 G4 A4 D4','6 6 6 6 12 12 6 18','저|희|가|용|서|하|오|니'))
b.append(row('G4 G4 G4 G4 A4 G4 F4 G4','12 6 12 6 12 6 12 6','저|희|죄|를|용|서|하|시','A4 A4 C5 C5 A4 D5 C5 A4','18 18 6 6 6 6 6 6','고||저|희|를|유|혹|에'))
b[1][1][0]['tie']='start';b[1][1][1]['tie']='stop'
b.append(row('C5 C5 A4 G4 A4 C4 F4 G4','6 6 6 12 6 12 6 18','빠|지|지|않|게|하|시|고','G4 A4 G4 A4 A4','18 12 6 18 18','|악|에|서|'))
b[2][0][-1]['tie']='start';b[2][1][0]['tie']='stop';b[2][1][-2]['tie']='start';b[2][1][-1]['tie']='stop'
b.append(row('D4 C4 D4 A3 C4 D4','12 6 18 12 6 18','악|에|서|구|하|소','F4 F4 F4','18 18 36','서||'))
b[3][0][2]['fermata']=True;b[3][0][-1]['slur']='start';b[3][1][0]['slur']='stop';b[3][1][1]['tie']='start';b[3][1][2]['tie']='stop'
build('lords-a','주님의 기도 (2) · 앞부분',a,['합송']+['']*5,(12,8),72)
build('lords-b','주님의 기도 (2) · 이어서',b,['','','','천천히'],(12,8))
from pypdf import PdfWriter
writer=PdfWriter()
for key in ['lords-a','lords-b']:writer.append(str(out/(key+'-reengraved.pdf')))
with (out/'lords-prayer-reengraved.pdf').open('wb') as f:writer.write(f)
