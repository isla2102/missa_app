import sys
sys.path.insert(0,'work/music-deps');import verovio
verovio.setDefaultResourcePath('work/music-deps/verovio/data');t=verovio.toolkit()
def walk(o):
 if isinstance(o,dict):
  for k,v in o.items():
   if 'lyric' in k.lower() or 'direction' in k.lower() or 'system' in k.lower() and 'margin' in k.lower():print(k,str(v)[:180])
   walk(v)
 elif isinstance(o,list):
  for v in o:walk(v)
walk(t.getAvailableOptions())
