from pathlib import Path
p=Path('work/engrave_amen.py');s=p.read_text(encoding='utf-8').replace('import sys,xml.etree.ElementTree as E,io,json','import sys,xml.etree.ElementTree as E,io,json,re')
s=s.replace("'lyricSize':5", "'lyricSize':5,'minLastJustification':0")
s=s.replace("(assets/'amen.svg').write_text", "def flatten_text(m):\n content=''.join(E.fromstring(m.group(0)).itertext()).strip()\n return re.sub(r'font-size=\"0px\"', 'font-size=\"450px\" font-family=\"Malgun\"',m.group(0).split('>')[0]+'>')+content+'</text>'\nsvg=re.sub(r'<text\\b[^>]*>.*?</text>',flatten_text,svg,flags=re.S)\n(assets/'amen.svg').write_text",1)
p.write_text(s,encoding='utf-8',newline='\r\n')
