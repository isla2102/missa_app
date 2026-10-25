from pathlib import Path
p=Path('work/enlarge_scores.py');s=p.read_text(encoding='utf-8');s=s.replace("return opening+''.join(E.fromstring(m.group(0)).itertext()).strip()+'</text>'", "text=''.join(E.fromstring(m.group(0)).itertext()).strip();opening=opening.replace('font-size=\"405px\"','font-size=\"355px\"') if len(text)>=5 and not any(role in text for role in ['합송','성가대','선창','음표','tempo','rit','Espressivo','천천히']) else opening;return opening+text+'</text>'")
p.write_text(s,encoding='utf-8')
