from pathlib import Path
import re,shutil
s=Path('review/02-ia-v22.html').read_text(encoding='utf-8').replace('검토 v22','검토 v23')
s=s.replace("if(asset.kind==='remote'){preview.onload=()=>{if(!enlarged)scheduleReflow(currentAnchor);};preview.onerror", "if(asset.kind==='remote'){preview.onerror")
s=s.replace("caption.textContent=(asset.kind==='engraved'", "caption.textContent=asset.kind==='remote'?'':(asset.kind==='engraved'")
s=s.replace("card.append(status,scroll);section.append(row,form,card);fill();return section;", "row.append(form);card.append(status,scroll);section.append(row,card);fill();return section;")
s=s.replace("status.textContent='가톨릭성가 '+number+'번';", "status.textContent='';status.hidden=true;")
s=s.replace("else status.textContent='성가 번호를 입력해 주세요.';", "else{status.textContent='성가 번호를 입력해 주세요.';status.hidden=false;}")
s=s.replace("status.textContent='1부터 528 사이의 성가 번호를 입력해 주세요.';", "status.hidden=false;status.textContent='1부터 528 사이의 성가 번호를 입력해 주세요.';")
Path('review/02-ia-v23.html').write_text(s,encoding='utf-8',newline='\r\n')
Path('work/review-ia-v23-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v22.cjs').read_text(encoding='utf-8').replace('02-ia-v22.html','02-ia-v23.html')
t+='''\nconst hymn=run("renderHymnScore('입당 성가')");assert.equal(hymn.children.length,2);assert.ok(walk(hymn.children[0]).some(n=>n.tagName==='form'));const entry=walk(hymn).find(n=>n.tagName==='input');entry.value='123';walk(hymn).find(n=>n.tagName==='form').onsubmit({preventDefault(){}});const figure=walk(hymn).find(n=>n.tagName==='figure');assert.equal(figure.querySelector('figcaption').textContent,'악보 크게 보기');assert.ok(!hymn.textContent.includes('가톨릭성가 123번'));assert.equal(figure.querySelector('img').onload,undefined);assert.ok(figure.querySelector('img').src.endsWith('2012040123.jpg'));console.log('PASS: exactly two explicit grid rows; form stays in header; no duplicate captions; remote image load cannot trigger reflow/reset scroll.');\n'''
Path('work/test-reader-v23.cjs').write_text(t,encoding='utf-8',newline='\r\n')
