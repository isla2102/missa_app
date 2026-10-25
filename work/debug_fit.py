import sys,xml.etree.ElementTree as E
sys.path.insert(0,'work/music-deps')
from svglib.svglib import svg2rlg
p='docs/교중미사악보/reengraved/autofit/gloria.svg';r=E.parse(p).getroot();print(r.attrib);print(list(r)[0].attrib);d=svg2rlg(p);print(d.width,d.height,d.getBounds())
