from pathlib import Path
s=Path('work/get_reference_midi.py').read_text(encoding='utf-8');a=s.index('nums=');b=s.index('\ndef fetch',a);s=s[:a]+'nums=[365]'+s[b:];s=s.replace("out/'sources.json'","out/'365-source.json'");Path('work/get_365_midi.py').write_text(s,encoding='utf-8')
