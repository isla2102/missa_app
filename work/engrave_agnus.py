from pathlib import Path
s=Path('work/engrave_manual_scores.py').read_text(encoding='utf-8').split('# Kyrie -')[0]
s=s.replace("36:('half',True)","36:('half',True),96:('breve',False)")
exec(compile(s,'builder','exec'))
systems=[];roles=[]
for verse in [1,2,3]:
 upper=[note('A4',96,str(verse)+'. 하느님의'),note('A4',6,'어'),note('G4',6,'린'),note('A4',12,'양')]
 upper +=[note(p,d,ly,**({'fermata':True} if i==6 else {})) for i,(p,d,ly) in enumerate(zip(['G4','G4','A4','G4','F4','D4','C4'],[24,6,6,6,6,12,12],['세상의 죄를','없','애','시','는','주','님']))]
 lower=[note(p,d,ly) for p,d,ly in zip(['G4','G4','G4','A4','G4','F4','F4'],[6,6,12,6,6,12,24],['평','화','를','주','','소','서'] if verse==3 else ['자','비','를','베','푸','소','서'])]
 systems += [[upper[:4],upper[4:]],[lower]];roles+=['합송','']
build('agnus','하느님의 어린양',systems,roles)
