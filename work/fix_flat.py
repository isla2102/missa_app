from pathlib import Path
p=Path('work/connect_remaining_v25.py');s=p.read_text(encoding='utf-8');a=s.index("  tree=E.fromstring(text);height=");b=s.index(" root.set('height'",a)
s=s[:a]+'''  tree=E.fromstring(text);height=float(tree.get('height').removesuffix('px'))
  group=E.Element('g',transform='translate(0 '+str(y)+')')
  for child in tree:
   if child.tag.endswith('}svg'):
    vb=[float(x) for x in child.get('viewBox').split()]
    child.tag='{http://www.w3.org/2000/svg}g';child.attrib.clear();child.set('transform','scale('+str(1050/vb[2])+')')
   group.append(child)
  root.append(group);y+=height+20
'''+s[b:];p.write_text(s,encoding='utf-8')
