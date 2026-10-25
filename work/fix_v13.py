from pathlib import Path
p=Path('work/update_review_v13.py');s=p.read_text(encoding='utf-8');s=s.replace('s=s.replace("const frameMock=",helper+', 'helper=helper.replace("\\\\\\\\", "\\\\")\ns=s.replace("const frameMock=",helper+')
p.write_text(s,encoding='utf-8',newline='\r\n')
