from pathlib import Path
p=Path('work/engrave_gloria.py');s=p.read_text(encoding='utf-8');s=s.replace("s=s.replace(\"xml=E.tostring(r,\"", "s=s.replace(\"if si==len(systems)-1 and mi==len(measures)-1:\",\"if key=='gloria-d' and si==len(systems)-1 and mi==len(measures)-1:\")\ns=s.replace(\"xml=E.tostring(r,\"")
s=s.replace("di=E.SubElement(measure,'direction',placement='above');dt=", "di=E.Element('direction',placement='above');measure.insert(list(measure).index(measure.find('note')),di);dt=")
p.write_text(s,encoding='utf-8',newline='\r\n')
p=Path('work/engrave_remaining.py');s=p.read_text(encoding='utf-8');s=s.replace("exec(compile(s,'builder','exec'))", "s=s.replace(\"E.SubElement(pit,'step').text=info['p'][0];\",\"E.SubElement(pit,'step').text=info['p'][0];E.SubElement(pit,'alter').text=str(-1 if info['p'][0]=='B' else 0);\")\nexec(compile(s,'builder','exec'))");p.write_text(s,encoding='utf-8',newline='\r\n')
