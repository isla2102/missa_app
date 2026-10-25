from pathlib import Path
s=Path('work/test-reader-v18.cjs').read_text(encoding='utf-8').replace('02-ia-v18.html','02-ia-v19.html')
s+='''
const acclamation=run('renderAlleluia()');const cards=walk(acclamation).filter(n=>n.attrs['data-acclamation-role']);assert.deepEqual(cards.map(n=>n.attrs['data-acclamation-role']),['assembly','choir','assembly']);assert.equal(cards[0].querySelector('img').src,cards[2].querySelector('img').src);assert.ok(cards[1].textContent.includes('너희는 가서 모든 민족들을'));
const aflow=run("flowBlocks(1).filter(b=>b.acclamationPart)");assert.equal(aflow.length,3);assert.deepEqual(Array.from(aflow,b=>b.acclamationPart),['first','choir','last']);for(const b of aflow)assert.ok(run('renderBlock')(b));
const a365=run("reengravedPrincipalScores['복음 환호송'][0]");run('showSourceDialog')(run("scoreSourceCatalog['복음 환호송']"));assert.ok(ui.get('source-dialog-body').textContent.includes('365번'));assert.ok(walk(ui.get('source-dialog-body')).some(n=>n.tagName==='a'&&n.href?.includes('sunggaId=365')));assert.ok(walk(ui.get('source-dialog-body')).some(n=>n.tagName==='a'&&n.download?.includes('365')));
assert.equal(run("scoreSourceCatalog['자비송'].confirmedNumber"),null);run('showSourceDialog')(run("scoreSourceCatalog['자비송']"));assert.ok(ui.get('source-dialog-body').textContent.includes('선율이 같은 번호는 아직 확인되지'));
assert.equal(run("scoreAssets('자비송')[0].kind"),'engraved');assert.equal(run("scoreAssets('주님의 기도 맺음 환호')[0].kind"),'engraved');slot.value='dawn';assert.equal(run("scoreAssets('복음 환호송')[0].kind"),'engraved');assert.equal(run("scoreAssets('자비송').length"),0);slot.value='main';
console.log('PASS: 365 refrain/choir/refrain ordered cards and identical one-line score, dated choir verse, confirmed-number source dialog/ENC link, unresolved candidates honestly labelled, additional finished PDFs and common-scope 365.');
'''
Path('work/test-reader-v19.cjs').write_text(s,encoding='utf-8',newline='\r\n')
