import sys
sys.path.insert(0,'work/music-deps')
import verovio
verovio.setDefaultResourcePath('work/music-deps/verovio/data')
t=verovio.toolkit()
print(t.getResourcePath())
