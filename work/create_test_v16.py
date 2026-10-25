from pathlib import Path
s=Path('work/test-reader-v15.cjs').read_text(encoding='utf-8').replace('02-ia-v15.html','02-ia-v16.html').replace(".textContent.includes('◎ 아멘.')", ".textContent.includes('아멘.')")
s+='''
const hanging=run("liturgyNode('+ 사제의 긴 본문\\n이어지는 줄\\n◎ 신자의 응답\\n계속 바칩니다.')");
const speechRows=walk(hanging).filter(n=>n.classList.contains('reader__speech-row'));assert.equal(speechRows.length,4);assert.equal(speechRows[0].children[0].textContent,'+');assert.equal(speechRows[0].children[1].textContent,'사제의 긴 본문');assert.equal(speechRows[1].children[0].textContent,'');assert.equal(speechRows[2].children[0].textContent,'◎');assert.equal(speechRows[3].children[1].textContent,'계속 바칩니다.');assert.ok(speechRows.every(row=>row.children[0].attrs['aria-hidden']==='true'));
assert.ok(html.includes('grid-template-columns: var(--draft-marker-width) minmax(0, 1fr)'));
console.log('PASS: separate marker/body columns, hanging continuation indentation, guidance alignment and accessible role labels.');
'''
Path('work/test-reader-v16.cjs').write_text(s,encoding='utf-8',newline='\r\n')
