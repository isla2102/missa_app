from pathlib import Path
import xml.etree.ElementTree as E
from copy import deepcopy
base=Path('docs/교중미사악보/reengraved')
for key in ['gloria','lords-prayer']:
 root=E.parse(base/(key+'.svg')).getroot()
 for group in root:
  for child in list(group):
   if child.tag.endswith('}style'):group.remove(child)
   elif not child.tag.endswith('}defs'):

    for n in child.iter():
     if n.tag.split('}')[-1] in ['path','ellipse','polygon','polyline','rect']:n.set('stroke','black')
 ids={n.get('id'):n for n in root.iter() if n.get('id')}
 for parent in list(root.iter()):
  for n in list(parent):
   if n.tag.endswith('}use'):
    target=ids[n.get('{http://www.w3.org/1999/xlink}href').lstrip('#')]
    replacement=E.Element('{http://www.w3.org/2000/svg}g',transform=n.get('transform',''))
    copy=deepcopy(target)
    for glyph in copy.iter():glyph.attrib.pop('id',None)
    replacement.append(copy);index=list(parent).index(n);parent.remove(n);parent.insert(index,replacement)
 E.ElementTree(root).write(base/(key+'-v26.svg'),encoding='utf-8',xml_declaration=True)

