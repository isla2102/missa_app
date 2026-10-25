from pathlib import Path
p=Path('work/readable_scores.py');s=p.read_text(encoding='utf-8');s=s.replace(' rows=[]\n', ''' # Fit each lyric to its existing horizontal slot without changing line breaks.
 for system in tree.iter():
  if system.get('class')!='system':continue
  baselines={}
  for text in system.iter(tag('text')):
   if text.text and text.get('x') is not None:baselines.setdefault(text.get('y'),[]).append(text)
  for texts in baselines.values():
   texts.sort(key=lambda n:float(n.get('x')))
   for text,nexttext in zip(texts,texts[1:]):
    size=float(text.get('font-size','405px').removesuffix('px'));slot=float(nexttext.get('x'))-float(text.get('x'))-35
    width=pdfmetrics.stringWidth(text.text,'Malgun',1)
    if slot>0 and width>0:text.set('font-size',str(min(size,slot/width))+'px')
 rows=[]
''')
p.write_text(s,encoding='utf-8')
