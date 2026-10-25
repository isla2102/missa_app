from pathlib import Path
p=Path('work/engrave_gloria.py');s=p.read_text(encoding='utf-8').replace("if n.findtext('step')=='B':E.SubElement(n,'alter').text='-1'", "if n.findtext('step')=='B':\n   alter=E.Element('alter');alter.text='-1';n.insert(1,alter)");p.write_text(s,encoding='utf-8',newline='\r\n')
p=Path('review/02-ia-v25.html');s=p.read_text(encoding='utf-8');s=s.replace(' .reader__turns { grid-column: 1; grid-row: 3; }\n','').replace(' .reader__turns { display:', ' .reader__turns { grid-column: 1; grid-row: 3; display:',1)
s=s.replace("frame.className=fullScorePage?'reader__item reader__item--score':'reader__item';", "frame.className=fullScorePage?'reader__item reader__item--score':compactScore && mode==='chant'?'reader__item reader__item--compact-score':'reader__item';")
s=s.replace("if(compactScore)card.setAttribute('data-score-layout','compact');", "if(compactScore){card.setAttribute('data-score-layout','compact');if(mode==='chant')card.className+=' reader__content-card--compact';}")
s=s.replace(' .reader__score-scroll {', ' .reader__item--compact-score { max-block-size: calc(100cqh - (2 * var(--draft-padding)) - 2px); min-block-size: 0; display: flex; flex-direction: column; }\n .reader__content-card--compact { min-block-size: 0; overflow: auto; }\n .reader__score-scroll {',1)
s=s.replace("block.group==='보편 지향 기도 지향' && !block.hideHeading", "block.group==='보편 지향 기도 지향' && !block.hideHeading && !block.continued")
p.write_text(s,encoding='utf-8',newline='\r\n')
