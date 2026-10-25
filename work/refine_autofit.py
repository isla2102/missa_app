from pathlib import Path
p=Path('work/autofit_scores.py');s=p.read_text(encoding='utf-8');s=s.replace("for m in E.parse(base/(k+'.musicxml')).getroot().findall('.//part/measure'):part.append(copy.deepcopy(m))", "for j,m in enumerate(E.parse(base/(k+'.musicxml')).getroot().findall('.//part/measure')):\n   m=copy.deepcopy(m)\n   if j==0:\n    for a in list(m.findall('attributes')):m.remove(a)\n   part.append(m)")
s=s.replace("words.text=text.replace('다 같이','합송').replace('사제 선창 · 합송','사제 선창')", "words.text=text.replace('다 같이','합송').replace('사제 선창 · 합송','사제 선창');words.text=re.sub(r'^사제(?! 선창)', '사제 선창',words.text)")
s=s.replace("raw=copy.deepcopy(system);g=", "raw=copy.deepcopy(system)\n  for element in raw.iter():element.attrib.pop('id',None)\n  g=")
s=s.replace("c.showPage();c.save();merged.set", """c.showPage();c.save()
 from pypdf import PdfReader,PdfWriter
 pdf=PdfReader(dest/(key+'.pdf'));last=pdf.pages[-1];last.mediabox.lower_left=(0,max(0,y+gap-margin));last.cropbox=last.mediabox;writer=PdfWriter()
 for page in pdf.pages:writer.add_page(page)
 with (dest/(key+'.pdf')).open('wb') as f:writer.write(f)
 merged.set""")
p.write_text(s,encoding='utf-8')
