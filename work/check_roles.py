import xml.etree.ElementTree as E
for k in ['memorial-ordinary','memorial-lent','memorial-easter','lords-a','amen','agnus']:
 r=E.parse('docs/교중미사악보/reengraved/'+k+'.musicxml').getroot();print(k,[(m.get('number'),len(m.findall('note')),[w.text for w in m.findall('.//words')]) for m in r.findall('.//measure')][:5])
