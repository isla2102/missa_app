from pathlib import Path
p=Path('work/fix_svg_v26.py');s=p.read_text(encoding='utf-8');s=s.replace('import xml.etree.ElementTree as E','import xml.etree.ElementTree as E\nfrom copy import deepcopy')
s=s.replace(" E.ElementTree(root).write", """ ids={n.get('id'):n for n in root.iter() if n.get('id')}
 for parent in list(root.iter()):
  for n in list(parent):
   if n.tag.endswith('}use'):
    target=ids[n.get('{http://www.w3.org/1999/xlink}href').lstrip('#')]
    replacement=E.Element('{http://www.w3.org/2000/svg}g',transform=n.get('transform',''))
    copy=deepcopy(target)
    for glyph in copy.iter():glyph.attrib.pop('id',None)
    replacement.append(copy);index=list(parent).index(n);parent.remove(n);parent.insert(index,replacement)
 E.ElementTree(root).write""")
p.write_text(s,encoding='utf-8')

