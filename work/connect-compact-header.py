from pathlib import Path
import re
s=Path('review/02-ia-v48.html').read_text(encoding='utf-8').replace('v48','v49')
s=s.replace(':root { ',':root { --draft-header-gap: .375rem; --draft-brand-size: 1.5rem; ',1)
s=s.replace(' .reader__header, .reader__footer { justify-content: space-between; }', ''' .reader__header, .reader__footer { justify-content: space-between; }
 .reader__header--navigation { flex-wrap: nowrap; gap: var(--draft-header-gap); overflow-x: auto; }
 .reader__header-group { display: flex; flex-wrap: nowrap; align-items: center; gap: var(--draft-header-gap); white-space: nowrap; flex-shrink: 0; }
 .reader__brand { font-size: var(--draft-brand-size); }
 .reader__label-hidden { position: absolute; inline-size: 1px; block-size: 1px; overflow: hidden; clip-path: inset(50%); }''')
s=s.replace('<header class="reader__header">','<header class="reader__header reader__header--navigation">',1)
s=s.replace('<div class="reader__row"><h1 class="reader__title">MISSA','<div class="reader__header-group"><h1 class="reader__title reader__brand">MISSA',1)
s=s.replace('<div class="reader__row"><label for="date">날짜</label>','<div class="reader__header-group"><label class="reader__label-hidden" for="date">날짜</label>',1)
s=s.replace('<label for="slot">회차</label>','<label class="reader__label-hidden" for="slot">회차</label>',1).replace('<label for="mode">모드</label>','<label class="reader__label-hidden" for="mode">모드</label>',1)
span='<span data-js="liturgical-day" aria-live="polite"></span>';s=s.replace(span,'',1)
button='<button type="button" class="reader__season-badge" data-js="liturgical-season" aria-haspopup="dialog" aria-controls="season-dialog"></button>';s=s.replace(button,button+span,1)
s=s.replace('<nav class="reader__row" aria-label="성가와 기도">','<nav class="reader__header-group" aria-label="성가와 기도">',1)
old="const day=selectedDailyData();find('liturgical-day').textContent=day?day.title+' · 전교 주일':'전례일 미연동';find('liturgical-season').textContent=currentSeason()?.title || (day?day.season:'시기 미확인');"
assert old in s
new="""const day=selectedDailyData();const season=currentSeason()?.title||(day?day.season:'시기 미확인');const shortSeason=season.replace(/ 시기$/,'');find('liturgical-season').textContent=shortSeason;find('liturgical-season').setAttribute('aria-label',season+' 알아보기');find('liturgical-day').textContent=day?day.title.replace(/^연중\\s*/,'')+' - 전교 주일':'전례일 미연동';"""
s=s.replace(old,new)
Path('review/02-ia-v49.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v49-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v48.cjs').read_text(encoding='utf-8').replace('02-ia-v48.html','02-ia-v49.html').replace("includes('연중 제29주일')","includes('제29주일')");t+='''\ndate.value='2026-10-18';run('updateLiturgicalHeading()');assert.equal(ui.get('liturgical-season').textContent,'연중');assert.equal(ui.get('liturgical-day').textContent,'제29주일 - 전교 주일');assert.equal((html.match(/data-js="liturgical-season"/g)||[]).length,1);assert.ok(html.includes('reader__header--navigation { flex-wrap: nowrap'));assert.ok(html.includes('class="reader__label-hidden" for="date"'));console.log('PASS v49 single season badge, shortened day label and nonwrapping accessible header.');\n''';t=t.replace("ui.get('liturgical-season').textContent,'연중 시기'","ui.get('liturgical-season').textContent,'연중'");Path('work/test-reader-v49.cjs').write_text(t,encoding='utf-8')
