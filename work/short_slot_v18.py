from pathlib import Path
p=Path('work/update_review_v18.py');s=p.read_text(encoding='utf-8');s=s.replace("Path('review/02-ia-v18.html').write_text", "s=s.replace('<option value=\"youth\">주일 저녁 젊은이 미사</option>','<option value=\"youth\">저녁미사</option>')\ns=s.replace('id=\"slot\" data-js=\"slot\"','id=\"slot\" class=\"reader__session-select\" data-js=\"slot\"')\ns=s.replace(' .reader__score-photo {',' .reader__session-select { width: max-content; }\\n .reader__score-photo {',1)\nPath('review/02-ia-v18.html').write_text")
p.write_text(s,encoding='utf-8',newline='\r\n')
