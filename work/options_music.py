import sys
sys.path.insert(0,'work/music-deps')
import verovio,json
verovio.setDefaultResourcePath('work/music-deps/verovio/data')
t=verovio.toolkit();o=t.getOptions();print({k:v for k,v in o.items() if any(x in k.lower() for x in ['break','spacing','page','justify'])})
