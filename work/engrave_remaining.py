from pathlib import Path
s=Path('work/engrave_manual_scores.py').read_text(encoding='utf-8').split('# Kyrie -')[0]
s=s.replace("6:('eighth',False)","3:('16th',False),9:('eighth',True),6:('eighth',False)")
s=s.replace("E.SubElement(pit,'step').text=info['p'][0];","E.SubElement(pit,'step').text=info['p'][0];E.SubElement(pit,'alter').text=str(-1 if info['p'][0]=='B' else 0);")
exec(compile(s,'builder','exec'))
def m(ps,ds,ls):
 p=ps.split();d=list(map(int,ds.split()));l=ls.split('|');assert len(p)==len(d)==len(l),(len(p),len(d),len(l));return [note(x,y,z) for x,y,z in zip(p,d,l)]
def tie(measure,i,j):measure[i]['tie']='start';measure[j]['tie']='stop'
s=[]
s.append([m('A4 A4 A4 A4 G4 A4 A4','12 6 6 6 6 18 18','거|룩|하|시|도|다|'),m('G4 G4 G4 G4 F4 G4 G4','12 6 6 6 6 18 18','거|룩|하|시|도|다|')]);[tie(x,5,6) for x in s[0]]
s.append([m('F4 F4 F4 F4 D4 C4','12 6 12 6 18 18','거|룩|하|시|도|'),m('D4 D4','36 36','다|'),m('F4 F4 F4 F4 G4 A4 G4','18 6 6 6 18 12 6','온|누|리|의|주|하|느'),m('A4 A4','36 36','님|')]);tie(s[1][1],0,1);tie(s[1][3],0,1)
s.append([m('C5 C5 C5 A4 A4','12 6 18 18 18','하|늘|과|땅|에'),m('G4 A4 G4 F4 D4 D4','12 6 18 12 6 18','가|득|찬|그|영|광'),m('F4 F4 F4 F4 G4 A4','12 6 12 6 18 18','높|은|데|서|호|산')])
s.append([m('A4 A4','36 36','나|'),m('C5 C5 C5 C5 D5 C5 A4','12 6 18 6 6 6 18','주|님|의|이|름|으|로'),m('C5 C5 A4 G4 F4','12 6 12 6 36','오|시|는||분')]);tie(s[3][0],0,1)
s.append([m('G4 G4 A4 F4 D4 C4','12 6 12 6 18 18','찬|미|받|으|소|서'),m('F4 F4 G4 A4 G4 F4','12 6 12 6 18 18','높|은|데|서|호|산'),m('F4 F4','36 36','나|')]);tie(s[4][2],0,1)
for row in s:
 for measure in row:assert sum(n['d'] for n in measure)==72
build('sanctus','거룩하시도다',s,['합송','','a tempo','','a tempo · rit.'],(12,8),88)
a=[m('F4 F4 F4 G4 G4 G4','6 6 6 12 6 36','신|앙|의|신|비|여'),m('A4 A4 A4 A4 A4 G4 F4 G4 D4 D4','3 3 6 6 6 6 6 6 12 18','주|님|께|서|오|실|때|까|지|')];tie(a[1],8,9)
b=[m('F4 F4 F4 G4 G4 G4 A4 C5 A4 A4','6 6 6 6 6 6 6 6 18 18','주|님|의|죽|음|을|전|하|며|'),m('D5 D5 A4 G4 C5 A4 G4 A4 F4 F4','12 6 18 6 12 6 6 6 18 18','부|활|을|선|포|하|나|이|다|')];tie(b[0],8,9);tie(b[1],8,9)
build('memorial-ordinary','신앙의 신비여 · 연중', [a,b],['사제 선창 · 합송','합송'])
a=[m('F4 F4 F4 D4 D4 D4','6 6 6 12 6 36','신|앙|의|신|비|여'),m('C4 D4 F4 F4 G4 G4 F4 D4 F4','6 6 6 6 6 6 6 6 24','주|님|께|서|오|실|때|까|지'),m('A4 A4 A4 C5 A4 A4','12 6 6 12 6 12','이|빵|을|먹|고|')];tie(a[2],4,5)
b=[m('G4 G4 G4 A4 G4 F4 G4 A4','12 6 6 6 6 6 6 24','이|잔|을|마|실|적|마|다'),m('D4 C4 D4 G4 F4 E4','6 6 12 6 6 12','주|님|의|죽|음|을'),m('C4 E4 E4 D4 D4','6 6 6 6 24','전|하|나|이|다')]
build('memorial-lent','신앙의 신비여 · 사순',[a,b],['사제 선창 · 합송','합송'])
a=[m('F4 F4 F4 G4 A4 A4','6 6 6 12 6 36','신|앙|의|신|비|여'),m('C5 C5 C5 A4 D5 D5 C5','6 6 6 6 6 6 12','십|자|가|와|부|활|로'),m('B4 A4 G4 F4 F4 G4 A4','6 6 12 6 6 6 6','저|희|를|구|원|하|신')]
b=[m('A4 G4','24 24','주|님'),m('A4 G4 A4 B4 C5','6 6 6 6 24','길|이|영||광'),m('D5 C5 B4 F4','6 6 12 24','받|으|소|서')]
build('memorial-easter','신앙의 신비여 · 부활',[a,b],['사제 선창 · 합송','합송'])
