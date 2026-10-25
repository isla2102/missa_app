import xml.etree.ElementTree as E
r=E.parse('docs/교중미사악보/reengraved/autofit-readable/gloria.svg').getroot()
for n in r.iter():
 if n.tag.endswith('text'):print(n.attrib,n.text)
