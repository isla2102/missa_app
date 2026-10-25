from pathlib import Path
p=Path('work/engrave_manual_scores.py');s=p.read_text(encoding='utf-8')
s=s.replace("n=E.SubElement(m,'note');pit=E.SubElement(n,'pitch');E.SubElement(pit,'step').text=info['p'][0];E.SubElement(pit,'octave').text=info['p'][1:];E.SubElement(n,'duration').text=str(info['d'])", "n=E.SubElement(m,'note')\n    if info['p'] is None:E.SubElement(n,'rest')\n    else:\n     pit=E.SubElement(n,'pitch');E.SubElement(pit,'step').text=info['p'][0];E.SubElement(pit,'octave').text=info['p'][1:]\n    E.SubElement(n,'duration').text=str(info['d'])")
s=s.replace("if info.get('tie') or info.get('slur') or info.get('tuplet'):","if info.get('tie') or info.get('slur') or info.get('tuplet') or info.get('fermata'):")
s=s.replace("nt=E.SubElement(n,'notations')", "nt=E.SubElement(n,'notations')\n     if info.get('fermata'):E.SubElement(nt,'fermata').text='normal'")
s=s.replace("H=841.89 if len(systems)>2 else 460", "H=841.89 if len(systems)>2 else 300 if len(systems)==1 else 460")
p.write_text(s,encoding='utf-8',newline='\r\n')
# Reuse the verified engraving path without rebuilding the prior files.
code=s[:s.index('# Kyrie -')]
code+='''
ps=['F4','G4','A4','F4','G4','A4','G4','F4','D4','C4','F4','G4','A4','G4','F4','F4']
ds=[6,6,6,12,6,6,6,6,12,12,6,6,6,6,6,12]
lyrics=['알','렐','루','야','알','','렐','루','야','','알','렐','','루','','야']
line=[note(None,6)]+[note(p,d,ly) for p,d,ly in zip(ps,ds,lyrics)]
line[9]['slur']='start';line[10]['slur']='stop';line[-1]['fermata']=True
for a,b in [(5,6),(12,13),(14,15)]:line[a]['beam']='begin';line[b]['beam']='end'
build('alleluia-365','365번 복음 환호송 · 알렐루야',[[line]],['합송 후렴'])
'''
Path('work/engrave_365.py').write_text(code,encoding='utf-8',newline='\r\n')
