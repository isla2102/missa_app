import zipfile,xml.etree.ElementTree as E
for name in ['08-amen.mxl','11-doxology.mxl']:
 z=zipfile.ZipFile('work/music-omr-output/'+name);f=next(n for n in z.namelist() if n.endswith('.xml') and not n.startswith('META'));r=E.fromstring(z.read(f));print(name)
 for m in r.findall('.//part/measure'):
  print('measure',m.get('number'),[((''.join(n.findtext('pitch/'+x,'') for x in ['step','alter','octave'])) if n.find('pitch') is not None else 'rest',n.findtext('type'),len(n.findall('dot')),n.findtext('duration'),n.findtext('lyric/text')) for n in m.findall('note')])
