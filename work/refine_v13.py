from pathlib import Path
p=Path('work/update_review_v13.py');s=p.read_text(encoding='utf-8')
s=s.replace("spokenSegments(text,initial).forEach(segment=>{", "spokenSegments(text,initial).forEach(segment=>{\n  const parts=find('mode').value==='regular'?segment.parts.filter(part=>part.kind!=='guide'):segment.parts;if(!parts.length)return;")
s=s.replace('segment.parts.forEach(part=>{const p=', 'parts.forEach(part=>{const p=')
s=s.replace("if(target)target.replaceWith(liturgyNode(text,initial));", "if(target){const parent=target.parentElement;target.replaceWith(liturgyNode(text,initial));if(parent?.classList.contains('reader__content-card') && !parent.classList.contains('reader__content-card--score'))parent.classList.add('reader__content-card--liturgy');}")
p.write_text(s,encoding='utf-8',newline='\r\n')
