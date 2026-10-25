from pathlib import Path
p=Path('work/engrave_lords.py');s=p.read_text(encoding='utf-8');start=s.index('s=s.replace(');end=s.index('exec(compile',start);s=s[:start]+'''s=s.replace("if num==1 and tempo:E.SubElement(direction,'sound',tempo=str(tempo))", "if num==1 and tempo:E.SubElement(dt,'words').text='점4분음표 = '+str(tempo);E.SubElement(direction,'sound',tempo=str(tempo*1.5))")
s=s.replace("if si==len(systems)-1 and mi==len(measures)-1:","if key!='lords-a' and si==len(systems)-1 and mi==len(measures)-1:")
'''+s[end:];s=s.replace("b,['']*4,(12,8)","b,['','','','천천히'],(12,8)");p.write_text(s,encoding='utf-8',newline='\r\n')
