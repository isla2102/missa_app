import xml.etree.ElementTree as E
r=E.parse('docs/교중미사악보/reengraved/gloria-v26.svg').getroot()
for n in r.iter():
 if n.tag.endswith('use'):print(n.attrib);break
for n in r.iter():
 if n.tag.endswith('defs'):print(list(n)[0].attrib);break
for n in r.iter():
 if n.tag.endswith('style'):print(n.text[:400]);break
