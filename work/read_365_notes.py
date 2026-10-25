import runpy
from pathlib import Path
# Import parser definitions without rerunning comparisons.
s=Path('work/compare_reference_midi.py').read_text(encoding='utf-8');scope={};exec(s[:s.index('all_tracks=')],scope)
for t in scope['midi_tracks']('work/goodnews/365.mid'):
 print(t['name'],[(e['time'],e['pitch']) for e in t['events'][:30]])
